# ProteinLLMV1 — Phase 1 Complete

Enhanced protein function prediction system combining baseline organism classification with Protein Atlas-driven protein-type prediction.

## Status: Trainable & Runnable ✅

- **Baseline Model**: 3-class organism classifier (Human/Yeast/E. coli) — trained and checkpointed
- **Phase 1 Model**: 5-class protein-type classifier (from HPA v25) — trained and checkpointed
- **Website**: Live local demo with dual-task prediction + gradient BLOSUM62 visualization
- **Reproducibility**: Config-driven training pipeline, full data provenance logging

## Quick Start

```bash
# 1. Setup environment
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run the website (models pre-trained)
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000

# 3. Open http://127.0.0.1:8000
```

## Architecture

### Models
- **Organism Classifier**: Transformer Encoder (2 layers, 128D embeddings, 4 heads)
  - Classes: `human_swissprot`, `yeast_swissprot`, `ecoli_swissprot`
  - Dataset: 1500 sequences (500 per source from UniProt reviews)
  - Val Accuracy: ~76%
  
- **Protein Type Classifier**: Same architecture, 5 classes
  - Classes: Intracellular proteins, Transcription factors, Disease-related, Membrane proteins, Essential proteins
  - Dataset: 900 sequences (from HPA v25 with UniProt mapping)
  - Val Accuracy: ~42% (challenging 5-class task on small dataset)

### UI Features
- **Input**: Paste sequence or use built-in examples
- **Output**: 
  - Organism class + confidence + per-class probabilities
  - Protein type (if Phase 1 model exists) + confidence
  - BLOSUM62 substitution matrix with gradient coloring (red=negative, blue=positive)
- **Interactivity**: Live debounced predictions, keyboard shortcuts (Ctrl+Enter)

## Data Pipeline

### Public Datasets
- **UniProt Swiss-Prot** (3 organisms): 500 sequences each, automatic fetching
- **Human Protein Atlas v25**: 6949 accessions, batched UniProt mapping, 900 final samples

### Reproducibility
- `prepare_public_datasets.py`: Fetch & prepare organism data
- `prepare_proteinatlas_phase1_fast.py`: HPA to sequence mapping with batching
- `train_basic_model.py`: Config-driven training with checkpointing
- Label maps and manifests saved for full traceability

## Project Structure

```
backend/
  api/
    main.py                              # FastAPI + HTML UI + dual-model inference
  ml/
    basic_protein_model.py               # Transformer encoder classifier
    protein_tokenizer.py                 # Amino acid tokenizer
  training/
    prepare_public_datasets.py            # UniProt fetching
    prepare_proteinatlas_phase1_fast.py   # HPA preparation
    train_basic_model.py                  # Training entrypoint
    configs/
      basic_train.yaml                    # Organism model config
      protein_type_train.yaml             # Protein type config
      public_small_train.yaml             # (deprecated)
    dataset.py                            # Dataset + dataloader utilities
  checkpoints/
    basic_baseline/                       # Organism model (deprecated)
    protein_type/                         # Phase 1 protein-type model ✅
  data/
    processed/
      train_sequences.csv                 # Organism training data
      protein_type_train.csv              # HPA training data
      protein_type_label_map.json         # Label ID mapping
      protein_type_manifest.json          # Data provenance

docs/
  TRAINING_STARTER_PLAN.md               # Baseline setup guide
  PROTEIN_ATLAS_PHASE1.md                # HPA integration details

scripts/
  setup_environment.sh                    # Environment initialization

```

## Next Steps (Future Phases)

- **Phase 2**: Add ESMFold structure prediction + feature extraction
- **Phase 3**: Multi-task learning (jointly predict organism + type + GO terms)
- **Phase 4**: AlphaFold DB integration for confidence scoring
- **Phase 5**: Calibration & confidence calibration curves
- **Phase 6**: Model card, clinical disclaimer, evaluation metrics

## References

- **Human Protein Atlas**: https://www.proteinatlas.org/
- **UniProt**: https://www.uniprot.org/
- **ESMFold**: https://github.com/facebookresearch/esmfold
- **Protein LLM Baseline**: nanoGPT-inspired architecture

## Reproducibility & Science

- Seed fixed (`42`) across all pipelines
- Full data mapping logged in `protein_type_manifest.json`
- Config-based experiments for easy ablations
- Model checkpoints versioned with metadata
- No manual data curation (automated UniProt → sequence)

## Disclaimers

- Research-grade prototype, not clinical diagnostic
- Accuracy limited by small dataset (900 HPA samples)
- Protein type classification (42% val acc) requires larger dataset
- Structure predictions (future) should be validated experimentally

---

**Version**: 0.1-phase1  
**Last Updated**: Feb 23, 2026  
**Authors**: Aditya Sanil  
