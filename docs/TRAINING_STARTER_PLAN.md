# ProteinLLMV1 — PyTorch Starter Plan

This is the minimal, practical path to initialize and train a first working protein model.

## 1) System Design (MVP)

### Components
1. **Data Layer**
   - Input format: CSV with columns `sequence,label`
   - Sequence validation: keep only valid amino acid characters
   - Tokenization: amino-acid character-level tokenizer

2. **Model Layer**
   - Baseline architecture: `Embedding + Positional Encoding + Transformer Encoder + Mean Pool + Linear Head`
   - Task: sequence-level classification (single-label)

3. **Training Layer**
   - Config-driven hyperparameters from YAML
   - AdamW optimizer + cross entropy loss
   - Train/validation split
   - Checkpoint saving to `backend/checkpoints/`

4. **Evaluation Layer**
   - Metrics: validation loss + validation accuracy
   - Save best checkpoint by validation loss

## 2) Initialization Checklist

1. Create and activate a Python environment.
2. Install backend dependencies:
   - `pip install -r backend/requirements.txt`
3. Prepare data:
   - Option A: provide `backend/data/processed/train_sequences.csv`
   - Option B: run synthetic data mode to verify pipeline first.
4. Confirm config file:
   - `backend/training/configs/basic_train.yaml`

## 3) Creation Steps (What to Build)

1. Tokenizer utility in `backend/ml/`
2. Baseline model in `backend/ml/`
3. Dataset + dataloader in `backend/training/`
4. Train entrypoint in `backend/training/`
5. Base config YAML in `backend/training/configs/`

## 4) Start Training

From the repository root:

```bash
cd backend
python -m training.train_basic_model --config training/configs/basic_train.yaml
```

Synthetic sanity training (if no dataset yet):

```bash
cd backend
python -m training.train_basic_model --config training/configs/basic_train.yaml --synthetic
```

## 5) Next Upgrade Path

1. Replace baseline encoder with nanoGPT-style causal stack.
2. Add multi-label output for GO terms.
3. Add mixed precision and gradient accumulation.
4. Add evaluation report (precision/recall/F1).
5. Add experiment tracking and reproducibility logging.
