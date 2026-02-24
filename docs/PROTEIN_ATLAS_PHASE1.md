# Protein Atlas Phase 1

Phase 1 objective: add a first **protein-type prediction task** using Human Protein Atlas labels mapped to UniProt sequences.

## Data Source

- Download source: `https://www.proteinatlas.org/download/proteinatlas.tsv.zip`
- Core columns used:
  - `Gene`
  - `Uniprot`
  - `Ensembl`
  - `Protein class`

## Label Strategy

1. Parse `Protein class` and select the first class token as the primary type.
2. Keep top-N most frequent classes.
3. Map classes to numeric labels (`0..N-1`).

## Sequence Mapping

1. Parse primary accession from `Uniprot` column.
2. Fetch FASTA from UniProt REST (`/uniprotkb/{accession}.fasta`).
3. Keep rows with valid sequence.

## Generated Outputs

- Training dataset: `backend/data/processed/protein_type_train.csv`
- Label map: `backend/data/processed/protein_type_label_map.json`
- Manifest: `backend/data/processed/protein_type_manifest.json`

## Commands

Prepare dataset:

```bash
cd backend
python -m training.prepare_proteinatlas_phase1 --top-classes 5 --samples-per-class 180
```

Train protein-type model:

```bash
cd backend
python -m training.train_basic_model --config training/configs/protein_type_train.yaml
```
