# ProteinLLMV1

ProteinLLMV1 is a protein-sequence AI demo that combines lightweight language-model style inference with a polished web interface. It predicts organism class, surfaces a protein-type baseline, and visualizes BLOSUM62 residue relationships in the browser.

## Why this is recruitable

- Shows end-to-end ML product thinking: data prep, model inference, API serving, and UI delivery.
- Uses practical SWE patterns: typed request handling, cached model loading, health checks, and a self-contained demo server.
- Gives recruiters something they can run in minutes instead of reading a notebook-only project.

## What it does today

- Organism classification for human, yeast, and E. coli sequences.
- Protein-type classification on a Human Protein Atlas-derived baseline.
- Interactive BLOSUM62 substitution matrix rendering with color-coded scores.
- FastAPI backend with a built-in HTML demo page.

## Tech Stack

- Python, PyTorch, FastAPI, Pydantic
- Biopython for substitution matrices and protein utilities
- Torch-based Transformer encoder for classification

## Results Snapshot

- Organism classification: 92% accuracy
- Protein-type baseline: 36% accuracy across 12 classes
- Training data: 3,000+ organism sequences from UniProt and 3,830 protein sequences from Human Protein Atlas v25

## Run It Locally

Recommended: Python 3.11, which matches the Docker image and CI workflow.

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 in your browser.

If the private checkpoints are not available, the backend falls back to a deterministic heuristic model so the demo still runs in a clean checkout.

## Test It

```bash
cd backend
pytest tests
```

## Container Run

```bash
docker build -f backend/Dockerfile -t proteinllmv1 backend
docker run --rm -p 8000:8000 proteinllmv1
```

## API

- `GET /` serves the interactive demo.
- `POST /predict` returns predictions and the BLOSUM62 matrix for a sequence.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/predict \
	-H "Content-Type: application/json" \
	-d '{"sequence":"MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPIL"}'
```

## What to improve next

- Add a small frontend app or upgrade the current demo into a multi-page dashboard.
- Add automated tests for tokenization, inference, and API responses.
- Publish a short model card and evaluation report with precision, recall, and confusion matrices.
- Add Docker and CI so the project looks production-shaped to SWE recruiters.

## Data Sources

- UniProt Swiss-Prot
- Human Protein Atlas v25

## License

MIT
