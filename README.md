# ProteinLLMV1

ProteinLLMV1 is an end-to-end protein sequence analysis project built with PyTorch and FastAPI. The system provides organism classification, baseline protein-type classification, protein trait estimation, and ESMFold-based structure prediction through a local web demo and REST API.

## Project Overview

The project is organized as a practical ML application pipeline:

- Data preparation and curation scripts for protein datasets.
- Transformer-based classification model training and evaluation.
- Inference service with FastAPI.
- Browser-based interactive demo for sequence analysis.

Current prediction tasks:

- Organism classification: human, yeast, and E. coli.
- Protein-type baseline classification from Human Protein Atlas labels.
- Sequence-derived protein trait analysis (ProtParam + heuristic fallback).
- ESMFold structure prediction with PDB summary metrics.
- BLOSUM62 substitution matrix generation for input sequence residues.

## Key Results

- Organism classifier: 92% accuracy.
- Protein-type baseline: 36% accuracy across 12 classes.

## Repository Structure

```text
backend/
	api/            FastAPI app and endpoints
	ml/             Model and tokenizer code
	training/       Training and data preparation scripts
	data/processed/ Processed datasets and label maps
	tests/          Unit and API tests
docs/             Planning and technical notes
data/             Top-level data documentation
```

## Datasets

Primary datasets used in this project:

- UniProt Swiss-Prot for curated protein sequences.
- Human Protein Atlas v25 for protein-type labels.

Current processed artifacts include:

- Organism training sequences (`backend/data/processed/train_sequences.csv`).
- Protein-type training set (`backend/data/processed/protein_type_train.csv`).
- Protein-type label map and manifest.

See `data/README.md` for broader dataset guidance.

## Technology Stack

- Python 3.11
- PyTorch
- FastAPI + Pydantic
- Biopython
- PyTest
- Docker
- GitHub Actions (CI)

## Local Development Setup

Recommended Python version: 3.11 (matches Docker image and CI workflow).

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`.

Note: if private model checkpoints are not available in `backend/checkpoints/`, the service automatically uses a deterministic heuristic fallback model so the app still runs.

## Running Tests

```bash
cd backend
pytest tests
```

## Docker

Build and run:

```bash
docker build -f backend/Dockerfile -t proteinllmv1 backend
docker run --rm -p 8000:8000 proteinllmv1
```

## API Endpoints

- `GET /` interactive HTML demo
- `GET /health` service health status
- `GET /api/meta` model/runtime metadata
- `POST /predict` organism + protein-type + trait predictions and BLOSUM matrix
- `POST /predict_structure` ESMFold structure prediction with PDB summary and downloadable PDB text

Example request:

```bash
curl -X POST http://127.0.0.1:8000/predict \
	-H "Content-Type: application/json" \
	-d '{"sequence":"MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPIL"}'
```

ESMFold structure request example:

```bash
curl -X POST http://127.0.0.1:8000/predict_structure \
	-H "Content-Type: application/json" \
	-d '{"sequence":"MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPIL"}'
```

## Structure + Traits UI

The web app includes two tabs:

- `Classification + Traits`: organism/protein-type predictions plus trait panel.
- `Structure + Traits`: runs ESMFold, shows structure summary (residue count, chain count, pLDDT summary), and allows PDB download.

If ESMFold dependencies are unavailable, the API returns a clear `503` message from `/predict_structure`.

To enable ESMFold in your environment, install compatible dependencies in your backend environment:

```bash
cd backend
pip install fair-esm
```

Depending on your platform, you may also need a compatible PyTorch build (CPU or CUDA) for ESMFold weights to load correctly.

## Continuous Integration

GitHub Actions workflow runs tests on pushes and pull requests:

- Workflow file: `.github/workflows/ci.yml`
- Job: install backend dependencies and run `pytest tests`

## Roadmap

- Improve model performance and expand evaluation metrics.
- Add richer model card and experiment tracking.
- Extend UI into a multi-page dashboard.

## License

MIT
