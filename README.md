# ProteinLLMV1

ProteinLLMV1 is an end-to-end protein sequence classification project built with PyTorch and FastAPI. The current system provides organism classification, baseline protein-type classification, and BLOSUM62 visualization through a local web demo and REST API.

## Project Overview

The project is organized as a practical ML application pipeline:

- Data preparation and curation scripts for protein datasets.
- Transformer-based classification model training and evaluation.
- Inference service with FastAPI.
- Browser-based interactive demo for sequence analysis.

Current prediction tasks:

- Organism classification: human, yeast, and E. coli.
- Protein-type baseline classification from Human Protein Atlas labels.
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
- `POST /predict` organism + protein-type predictions and BLOSUM matrix

Example request:

```bash
curl -X POST http://127.0.0.1:8000/predict \
	-H "Content-Type: application/json" \
	-d '{"sequence":"MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPIL"}'
```

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
