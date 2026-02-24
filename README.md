# ProteinLLMV1

A protein sequence analyzer that predicts protein types and generates substitution matrices.

## What It Does

1. Organism Classification (Human, Yeast, E. coli)
2. Protein Type Classification (12 classes)
3. BLOSUM62 substitution matrix with color visualization

## Quick Start

cd backend && pip install -r requirements.txt
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

Open http://127.0.0.1:8000

## Training Data

- 900+ organism sequences from UniProt
- 3,830 protein sequences from Human Protein Atlas v25

## Model

PyTorch Transformer Encoder with:
- 128D embeddings
- 2 layers, 4 attention heads
- Amino acid tokenization

## Performance

- Organism: 92% accuracy
- Protein Type: 36% accuracy (12 classes)

## Data Sources

- UniProt Swiss-Prot
- Human Protein Atlas v25

## License

MIT

Built with PyTorch + FastAPI
