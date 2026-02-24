from __future__ import annotations

import argparse
import csv
import json
import random
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"


def parse_primary_class(raw_value: str) -> Optional[str]:
    if not isinstance(raw_value, str) or not raw_value.strip():
        return None
    parts = [part.strip() for part in raw_value.split(";") if part.strip()]
    return parts[0] if parts else None


def parse_primary_accession(raw_value: str) -> Optional[str]:
    if not isinstance(raw_value, str) or not raw_value.strip():
        return None
    parts = [part.strip() for part in raw_value.replace(",", ";").split(";") if part.strip()]
    return parts[0] if parts else None


def parse_fasta_to_map(fasta_text: str) -> Dict[str, str]:
    """Parse FASTA response and extract all sequences by accession."""
    sequence_map: Dict[str, str] = {}
    current_accession: Optional[str] = None
    current_sequence: List[str] = []

    for line in fasta_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current_accession and current_sequence:
                sequence_map[current_accession] = "".join(current_sequence)
            parts = line.split("|")
            current_accession = parts[1].strip() if len(parts) >= 3 else None
            current_sequence = []
        else:
            current_sequence.append(line)

    if current_accession and current_sequence:
        sequence_map[current_accession] = "".join(current_sequence)

    return sequence_map


def fetch_uniprot_sequences_batch(accessions: List[str], batch_size: int = 80) -> Dict[str, str]:
    """Fetch sequences for multiple accessions in batches."""
    all_sequences: Dict[str, str] = {}

    for start_idx in range(0, len(accessions), batch_size):
        batch = accessions[start_idx : start_idx + batch_size]
        query_str = " OR ".join(f"accession:{acc}" for acc in batch)
        params = {
            "query": f"({query_str}) AND reviewed:true",
            "format": "fasta",
            "size": str(len(batch) * 2),
        }
        url = "https://rest.uniprot.org/uniprotkb/search?" + urllib.parse.urlencode(params)

        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                fasta_text = response.read().decode("utf-8")
                batch_seqs = parse_fasta_to_map(fasta_text)
                all_sequences.update(batch_seqs)
                print(f"Fetched batch {start_idx // batch_size + 1}: got {len(batch_seqs)} sequences")
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(f"Error fetching batch starting at {start_idx}: {e}")
            continue

    return all_sequences


def build_phase1_dataset(
    proteinatlas_tsv_zip: Path,
    output_csv: Path,
    label_map_json: Path,
    manifest_json: Path,
    top_classes: int,
    samples_per_class: int,
    seed: int,
) -> None:
    random.seed(seed)

    print(f"Loading Protein Atlas from {proteinatlas_tsv_zip}...")
    dataframe = pd.read_csv(proteinatlas_tsv_zip, sep="\t", compression="zip")

    required_columns = ["Gene", "Uniprot", "Protein class", "Ensembl"]
    missing = [col for col in required_columns if col not in dataframe.columns]
    if missing:
        raise ValueError(f"Missing required Protein Atlas columns: {missing}")

    dataframe = dataframe[["Gene", "Uniprot", "Protein class", "Ensembl"]].copy()
    dataframe["protein_type"] = dataframe["Protein class"].apply(parse_primary_class)
    dataframe["uniprot_accession"] = dataframe["Uniprot"].apply(parse_primary_accession)
    dataframe = dataframe.dropna(subset=["protein_type", "uniprot_accession", "Gene"])

    class_counts = Counter(dataframe["protein_type"].tolist())
    selected_classes = [name for name, _ in class_counts.most_common(top_classes)]
    print(f"Selected classes: {selected_classes}")

    selected_df = dataframe[dataframe["protein_type"].isin(selected_classes)].copy()
    grouped = defaultdict(list)
    for row in selected_df.itertuples(index=False):
        grouped[row.protein_type].append(row)

    label_map = {name: idx for idx, name in enumerate(selected_classes)}

    unique_accessions = sorted(set(selected_df["uniprot_accession"].tolist()))
    print(f"Fetching {len(unique_accessions)} unique accessions...")

    sequence_map = fetch_uniprot_sequences_batch(unique_accessions)

    output_rows: List[Dict[str, object]] = []
    skipped_no_sequence = 0

    for protein_type in selected_classes:
        rows = grouped[protein_type]
        random.shuffle(rows)
        kept = 0

        for row in rows:
            if kept >= samples_per_class:
                break
            accession = row.uniprot_accession

            sequence = sequence_map.get(accession)
            if not sequence:
                skipped_no_sequence += 1
                continue

            output_rows.append(
                {
                    "sequence": sequence,
                    "label": label_map[protein_type],
                    "label_name": protein_type,
                    "gene": row.Gene,
                    "ensembl": row.Ensembl,
                    "uniprot": accession,
                    "source": "HumanProteinAtlas_v25",
                }
            )
            kept += 1

    random.shuffle(output_rows)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sequence", "label", "label_name", "gene", "ensembl", "uniprot", "source"],
        )
        writer.writeheader()
        writer.writerows(output_rows)

    label_map_json.parent.mkdir(parents=True, exist_ok=True)
    label_map_json.write_text(json.dumps({str(v): k for k, v in label_map.items()}, indent=2), encoding="utf-8")

    manifest = {
        "input_file": str(proteinatlas_tsv_zip),
        "rows_total": int(len(dataframe)),
        "selected_classes": selected_classes,
        "label_map": {str(v): k for k, v in label_map.items()},
        "samples_per_class_target": samples_per_class,
        "rows_output": len(output_rows),
        "skipped_no_sequence": skipped_no_sequence,
        "seed": seed,
    }
    manifest_json.parent.mkdir(parents=True, exist_ok=True)
    manifest_json.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Wrote: {output_csv}")
    print(f"Rows: {len(output_rows)}")
    print(f"Label map: {label_map_json}")
    print(f"Manifest: {manifest_json}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare Phase 1 Protein Atlas protein-type dataset")
    parser.add_argument(
        "--proteinatlas-tsv-zip",
        type=str,
        default=str(ROOT_DIR / "data" / "raw" / "proteinatlas" / "proteinatlas.tsv.zip"),
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default=str(BACKEND_DIR / "data" / "processed" / "protein_type_train.csv"),
    )
    parser.add_argument(
        "--label-map-json",
        type=str,
        default=str(BACKEND_DIR / "data" / "processed" / "protein_type_label_map.json"),
    )
    parser.add_argument(
        "--manifest-json",
        type=str,
        default=str(BACKEND_DIR / "data" / "processed" / "protein_type_manifest.json"),
    )
    parser.add_argument("--top-classes", type=int, default=5)
    parser.add_argument("--samples-per-class", type=int, default=180)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_phase1_dataset(
        proteinatlas_tsv_zip=Path(args.proteinatlas_tsv_zip),
        output_csv=Path(args.output_csv),
        label_map_json=Path(args.label_map_json),
        manifest_json=Path(args.manifest_json),
        top_classes=args.top_classes,
        samples_per_class=args.samples_per_class,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
