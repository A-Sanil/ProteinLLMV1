from __future__ import annotations

import argparse
import csv
import random
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class DatasetSource:
    name: str
    organism_id: int
    label: int


SOURCES: List[DatasetSource] = [
    DatasetSource(name="human_swissprot", organism_id=9606, label=0),
    DatasetSource(name="yeast_swissprot", organism_id=559292, label=1),
    DatasetSource(name="ecoli_swissprot", organism_id=83333, label=2),
]


def parse_fasta_sequences(fasta_text: str) -> List[str]:
    sequences: List[str] = []
    current: List[str] = []
    for line in fasta_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current:
                sequences.append("".join(current))
                current = []
            continue
        current.append(line)
    if current:
        sequences.append("".join(current))
    return sequences


def fetch_sequences_from_uniprot(organism_id: int, size: int) -> List[str]:
    query = f"organism_id:{organism_id} AND reviewed:true"
    fetched_sequences: List[str] = []
    page_size = min(500, size)
    offset = 0

    while len(fetched_sequences) < size:
        params = {
            "query": query,
            "format": "fasta",
            "size": str(page_size),
            "offset": str(offset),
        }
        url = "https://rest.uniprot.org/uniprotkb/search?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=60) as response:
            fasta_text = response.read().decode("utf-8")

        sequences = parse_fasta_sequences(fasta_text)
        if not sequences:
            break

        fetched_sequences.extend(sequences)
        offset += page_size

    return fetched_sequences[:size]


def build_dataset(samples_per_source: int, seed: int) -> Tuple[List[Dict[str, object]], Dict[str, int]]:
    rng = random.Random(seed)
    rows: List[Dict[str, object]] = []
    counts: Dict[str, int] = {}

    for source in SOURCES:
        sequences = fetch_sequences_from_uniprot(source.organism_id, size=samples_per_source * 2)
        if len(sequences) > samples_per_source:
            sequences = rng.sample(sequences, k=samples_per_source)

        counts[source.name] = len(sequences)
        for sequence in sequences:
            rows.append({"sequence": sequence, "label": source.label})

    rng.shuffle(rows)
    return rows, counts


def write_csv(rows: List[Dict[str, object]], output_csv: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["sequence", "label"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare small public protein datasets")
    parser.add_argument("--samples-per-source", type=int, default=120)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output-csv",
        type=str,
        default="data/processed/train_sequences.csv",
        help="CSV path relative to backend/",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    rows, counts = build_dataset(samples_per_source=args.samples_per_source, seed=args.seed)
    output_csv = Path(args.output_csv)
    write_csv(rows=rows, output_csv=output_csv)

    print(f"Wrote dataset: {output_csv}")
    print(f"Total rows: {len(rows)}")
    for name, count in counts.items():
        print(f"{name}: {count}")
    print("Labels: 0=human, 1=yeast, 2=ecoli")


if __name__ == "__main__":
    main()
