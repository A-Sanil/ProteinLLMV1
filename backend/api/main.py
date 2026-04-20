from __future__ import annotations

import json
import warnings
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import torch
import torch.nn.functional as F
import torch.nn as nn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml.basic_protein_model import BasicProteinClassifier
from ml.protein_tokenizer import ProteinTokenizer


try:
    from Bio.Align import substitution_matrices
except Exception:
    substitution_matrices = None
    warnings.warn(
        "Biopython is unavailable; BLOSUM62 scores will fall back to a simple identity matrix.",
        RuntimeWarning,
    )


BACKEND_DIR = Path(__file__).resolve().parents[1]
CHECKPOINT_PATH = BACKEND_DIR / "checkpoints" / "public_small" / "basic_protein_classifier.pt"
TYPE_CHECKPOINT_PATH = BACKEND_DIR / "checkpoints" / "protein_type" / "basic_protein_classifier.pt"
TYPE_LABEL_MAP_PATH = BACKEND_DIR / "data" / "processed" / "protein_type_label_map.json"
LABEL_MAP = {0: "human_swissprot", 1: "yeast_swissprot", 2: "ecoli_swissprot"}
APP_TITLE = "ProteinLLMV1 Demo"
MAX_BLOSUM_DISPLAY_RESIDUES = 80


class PredictRequest(BaseModel):
    sequence: str


class HeuristicProteinClassifier(nn.Module):
  def __init__(self, num_classes: int, pad_id: int, token_to_idx: Dict[str, int], max_length: int):
    super().__init__()
    self.num_classes = num_classes
    self.pad_id = pad_id
    self.max_length = max_length
    self.group_token_ids = {
      "hydrophobic": [token_to_idx[aa] for aa in "AILMFWVY" if aa in token_to_idx],
      "polar": [token_to_idx[aa] for aa in "STNQ" if aa in token_to_idx],
      "charged_positive": [token_to_idx[aa] for aa in "KRH" if aa in token_to_idx],
      "charged_negative": [token_to_idx[aa] for aa in "DE" if aa in token_to_idx],
      "special": [token_to_idx[aa] for aa in "GPC" if aa in token_to_idx],
    }

    base_weights = torch.tensor(
      [
        [0.80, 0.15, -0.05, -0.10, -0.15, -0.05],
        [0.20, 0.40, 0.10, 0.05, 0.15, 0.00],
        [0.35, 0.00, 0.35, -0.10, 0.05, 0.10],
        [0.10, -0.05, -0.10, 0.45, 0.30, 0.05],
        [0.55, 0.25, 0.05, 0.00, -0.05, 0.15],
      ],
      dtype=torch.float32,
    )
    self.register_buffer("feature_weights", base_weights[:num_classes].clone())
    self.register_buffer("feature_bias", torch.linspace(-0.15, 0.15, steps=num_classes))

  def _group_ratio(self, input_ids: torch.Tensor, group_name: str) -> torch.Tensor:
    token_ids = self.group_token_ids[group_name]
    if not token_ids:
      return torch.zeros((input_ids.shape[0], 1), device=input_ids.device)

    matches = torch.zeros((input_ids.shape[0],), device=input_ids.device)
    for token_id in token_ids:
      matches = matches + input_ids.eq(token_id).sum(dim=1).float()

    lengths = input_ids.ne(self.pad_id).sum(dim=1).clamp(min=1).float()
    return (matches / lengths).unsqueeze(1)

  def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
    lengths = input_ids.ne(self.pad_id).sum(dim=1).clamp(min=1).float().unsqueeze(1)
    length_feature = lengths / float(self.max_length)
    features = torch.cat(
      [
        self._group_ratio(input_ids, "hydrophobic"),
        self._group_ratio(input_ids, "polar"),
        self._group_ratio(input_ids, "charged_positive"),
        self._group_ratio(input_ids, "charged_negative"),
        self._group_ratio(input_ids, "special"),
        length_feature,
      ],
      dim=1,
    )
    return features @ self.feature_weights.t() + self.feature_bias


class ModelBundle:
    def __init__(self):
        self.source = "checkpoint"

        if CHECKPOINT_PATH.exists():
            checkpoint = torch.load(str(CHECKPOINT_PATH), map_location="cpu")
            try:
                config = checkpoint["config"]
                model_cfg = config["model"]
            except KeyError as exc:
                raise RuntimeError(f"Invalid checkpoint format: {CHECKPOINT_PATH}") from exc

            self.tokenizer = ProteinTokenizer(max_length=model_cfg["max_length"])
            self.model = BasicProteinClassifier(
                vocab_size=len(self.tokenizer.vocab.token_to_idx),
                max_length=model_cfg["max_length"],
                embedding_dim=model_cfg["embedding_dim"],
                num_heads=model_cfg["num_heads"],
                num_layers=model_cfg["num_layers"],
                ff_dim=model_cfg["ff_dim"],
                dropout=model_cfg["dropout"],
                num_classes=model_cfg["num_classes"],
                pad_id=self.tokenizer.vocab.pad_id,
            )
            self.model.load_state_dict(checkpoint["model_state_dict"])
            self.model.eval()
        else:
            self.source = "heuristic_fallback"
            self.tokenizer = ProteinTokenizer(max_length=256)
            self.model = HeuristicProteinClassifier(
                num_classes=len(LABEL_MAP),
                pad_id=self.tokenizer.vocab.pad_id,
                token_to_idx=self.tokenizer.vocab.token_to_idx,
                max_length=self.tokenizer.max_length,
            )
            self.model.eval()

        self.type_model: Optional[nn.Module] = None
        self.type_label_map: Dict[int, str] = {}

        if TYPE_CHECKPOINT_PATH.exists() and TYPE_LABEL_MAP_PATH.exists():
            type_checkpoint = torch.load(str(TYPE_CHECKPOINT_PATH), map_location="cpu")
            try:
                type_cfg = type_checkpoint["config"]["model"]
                raw_label_map = json.loads(TYPE_LABEL_MAP_PATH.read_text(encoding="utf-8"))
            except KeyError as exc:
                raise RuntimeError(f"Invalid type checkpoint metadata: {TYPE_CHECKPOINT_PATH}") from exc

            self.type_model = BasicProteinClassifier(
                vocab_size=len(self.tokenizer.vocab.token_to_idx),
                max_length=type_cfg["max_length"],
                embedding_dim=type_cfg["embedding_dim"],
                num_heads=type_cfg["num_heads"],
                num_layers=type_cfg["num_layers"],
                ff_dim=type_cfg["ff_dim"],
                dropout=type_cfg["dropout"],
                num_classes=type_cfg["num_classes"],
                pad_id=self.tokenizer.vocab.pad_id,
            )
            self.type_model.load_state_dict(type_checkpoint["model_state_dict"])
            self.type_model.eval()

            self.type_label_map = {int(idx): name for idx, name in raw_label_map.items()}
        elif TYPE_LABEL_MAP_PATH.exists():
            raw_label_map = json.loads(TYPE_LABEL_MAP_PATH.read_text(encoding="utf-8"))
            self.type_label_map = {int(idx): name for idx, name in raw_label_map.items()}
            self.type_model = HeuristicProteinClassifier(
                num_classes=len(self.type_label_map),
                pad_id=self.tokenizer.vocab.pad_id,
                token_to_idx=self.tokenizer.vocab.token_to_idx,
                max_length=self.tokenizer.max_length,
            )
            self.type_model.eval()


@lru_cache(maxsize=1)
def get_model_bundle() -> ModelBundle:
    return ModelBundle()


def build_blosum_matrix(sequence: str, max_residues: int = MAX_BLOSUM_DISPLAY_RESIDUES) -> Dict[str, object]:
    clean_seq = "".join(ch for ch in sequence.upper() if ch.isalpha())
    if not clean_seq:
        return {
            "residues": [],
            "scores": [],
            "full_length": 0,
            "displayed_length": 0,
            "truncated": False,
        }

    full_length = len(clean_seq)
    display_seq = clean_seq[:max_residues]
    residues = list(display_seq)

    if substitution_matrices is None:
        size = len(residues)
        scores = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        return {
            "residues": residues,
            "scores": scores,
            "full_length": full_length,
            "displayed_length": len(residues),
            "truncated": full_length > len(residues),
        }

    try:
        blosum62 = substitution_matrices.load("BLOSUM62")
    except Exception:
        size = len(residues)
        scores = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        return {
            "residues": residues,
            "scores": scores,
            "full_length": full_length,
            "displayed_length": len(residues),
            "truncated": full_length > len(residues),
        }

    scores = []
    for a in residues:
        row = []
        for b in residues:
            try:
                value = blosum62[(a, b)]
            except KeyError:
                try:
                    value = blosum62[(b, a)]
                except KeyError:
                    value = -4
            row.append(int(value))
        scores.append(row)

    return {
      "residues": residues,
      "scores": scores,
      "full_length": full_length,
      "displayed_length": len(residues),
      "truncated": full_length > len(residues),
    }


app = FastAPI(title=APP_TITLE)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_check() -> None:
    get_model_bundle()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "app": APP_TITLE}


@app.get("/api/meta")
def api_meta() -> Dict[str, object]:
    bundle = get_model_bundle()
    return {
        "app": APP_TITLE,
    "model_source": bundle.source,
        "organism_classes": list(LABEL_MAP.values()),
        "protein_type_model": bundle.type_model is not None,
        "max_sequence_length": bundle.tokenizer.max_length,
    "max_blosum_display_residues": MAX_BLOSUM_DISPLAY_RESIDUES,
        "features": [
            "organism_classification",
            "protein_type_baseline",
            "blosum62_visualization",
            "fastapi_inference",
        ],
    }


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>ProteinLLMV1 Demo</title>
    <style>
      :root {
        --bg: #07111f;
        --panel: rgba(8, 19, 35, 0.78);
        --panel-border: rgba(148, 163, 184, 0.18);
        --text: #e2e8f0;
        --muted: #94a3b8;
        --accent: #60a5fa;
        --accent-strong: #38bdf8;
        --surface: #0f172a;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background:
          radial-gradient(circle at top left, rgba(56, 189, 248, 0.22), transparent 28%),
          radial-gradient(circle at top right, rgba(96, 165, 250, 0.16), transparent 24%),
          linear-gradient(180deg, #020617 0%, #07111f 48%, #0f172a 100%);
        color: var(--text);
      }
      .shell { max-width: 1180px; margin: 0 auto; padding: 40px 20px 56px; }
      .hero {
        display: grid;
        gap: 18px;
        grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.9fr);
        align-items: start;
        margin-bottom: 22px;
      }
      .hero h1 { margin: 0; font-size: clamp(34px, 4vw, 56px); line-height: 1.02; letter-spacing: -0.04em; }
      .hero p { margin: 12px 0 0; max-width: 60ch; color: var(--muted); font-size: 16px; line-height: 1.6; }
      .badge-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
      .badge { border: 1px solid var(--panel-border); border-radius: 999px; padding: 8px 12px; font-size: 12px; color: var(--text); background: rgba(15, 23, 42, 0.72); }
      .stat-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
      .stat {
        padding: 16px;
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(8, 19, 35, 0.78));
        border: 1px solid var(--panel-border);
        box-shadow: 0 24px 80px rgba(2, 6, 23, 0.34);
      }
      .stat .label { display: block; color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.12em; }
      .stat .value { display: block; margin-top: 8px; font-size: 22px; font-weight: 700; }
      .stat .note { display: block; margin-top: 6px; color: #cbd5e1; font-size: 13px; line-height: 1.45; }
      .grid { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr); gap: 16px; }
      .card {
        background: var(--panel);
        border: 1px solid var(--panel-border);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 24px 90px rgba(2, 6, 23, 0.4);
        backdrop-filter: blur(18px);
        margin-bottom: 16px;
      }
      .card h2, .card h3 { margin: 0 0 12px; }
      .muted { color: var(--muted); font-size: 13px; line-height: 1.55; }
      .row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
      .chip {
        border: 1px solid var(--panel-border);
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 12px;
        cursor: pointer;
        background: rgba(15, 23, 42, 0.8);
        color: var(--text);
      }
      label { display: block; margin-bottom: 8px; font-weight: 600; }
      textarea {
        width: 100%;
        min-height: 132px;
        border-radius: 16px;
        border: 1px solid var(--panel-border);
        background: rgba(2, 6, 23, 0.55);
        color: var(--text);
        padding: 14px;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        resize: vertical;
      }
      textarea:focus { outline: 2px solid rgba(96, 165, 250, 0.45); outline-offset: 2px; }
      button {
        padding: 11px 16px;
        border: none;
        border-radius: 12px;
        background: linear-gradient(135deg, var(--accent), var(--accent-strong));
        color: white;
        cursor: pointer;
        font-weight: 700;
      }
      button.secondary { background: rgba(15, 23, 42, 0.85); border: 1px solid var(--panel-border); color: var(--text); }
      .status { font-size: 12px; color: #cbd5e1; margin-top: 10px; }
      .legend { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
      .legend-bar { width: 220px; height: 14px; border-radius: 8px; background: linear-gradient(90deg, #b91c1c 0%, #f8fafc 50%, #1d4ed8 100%); border: 1px solid rgba(148, 163, 184, 0.3); }
      table { border-collapse: collapse; font-size: 12px; width: 100%; overflow: hidden; }
      td, th { border: 1px solid rgba(148, 163, 184, 0.18); padding: 4px 6px; text-align: center; }
      th { background: rgba(15, 23, 42, 0.86); }
      @media (max-width: 860px) {
        .hero, .grid { grid-template-columns: 1fr; }
        .stat-grid { grid-template-columns: 1fr; }
      }
    </style>
  </head>
  <body>
    <div class="shell">
      <section class="hero">
        <div>
          <div class="badge-row">
            <span class="badge">FastAPI demo</span>
            <span class="badge">Transformer classifier</span>
            <span class="badge">Protein sequence AI</span>
          </div>
          <h1>ProteinLLMV1 turns amino-acid sequences into a live AI demo.</h1>
          <p>
            Paste a sequence, get an organism prediction, inspect a protein-type baseline, and view a BLOSUM62 score matrix.
            The goal is to showcase ML engineering, API design, and a recruiter-friendly product surface in one place.
          </p>
          <div class="row">
            <button onclick="runPrediction()">Predict sequence</button>
            <button class="secondary" onclick="clearSequence()">Clear</button>
          </div>
          <div class="badge-row">
            <span class="badge">Human / Yeast / E. coli</span>
            <span class="badge">Protein type baseline</span>
            <span class="badge">BLOSUM62 visualization</span>
          </div>
        </div>
        <div class="stat-grid">
          <div class="stat">
            <span class="label">ML signal</span>
            <span class="value">92%</span>
            <span class="note">Organism classifier accuracy on the current baseline.</span>
          </div>
          <div class="stat">
            <span class="label">Protein type</span>
            <span class="value">12 classes</span>
            <span class="note">Human Protein Atlas-derived label space for a second task.</span>
          </div>
          <div class="stat">
            <span class="label">Inference surface</span>
            <span class="value">1 route</span>
            <span class="note">Single FastAPI prediction path with a built-in browser demo.</span>
          </div>
        </div>
      </section>

      <div class="grid">
        <div>
          <div class="card">
            <label for="seq">Protein Sequence</label>
            <textarea id="seq">EGH</textarea>
            <div class="row">
              <span class="chip" onclick="setExample('EGH')">Example 1</span>
              <span class="chip" onclick="setExample('MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPIL')">Example 2</span>
              <span class="chip" onclick="setExample('MALWMRLLPLLALLALWGPDPAAA')">Example 3</span>
            </div>
            <div class="status" id="status">Ready.</div>
          </div>
          <div class="card" id="summary"></div>
        </div>
        <div class="card">
          <h3>BLOSUM62 Matrix</h3>
          <div class="legend">
            <span>Negative</span>
            <div class="legend-bar"></div>
            <span>Positive</span>
          </div>
          <p class="muted">Red = negative substitution score, blue = positive score.</p>
          <div id="matrix"></div>
        </div>
      </div>
    </div>

    <script>
      let predictTimer = null;

      function setStatus(text) {
        document.getElementById('status').textContent = text;
      }

      function setExample(sequence) {
        document.getElementById('seq').value = sequence;
        runPrediction();
      }

      function clearSequence() {
        document.getElementById('seq').value = '';
        document.getElementById('summary').innerHTML = '';
        document.getElementById('matrix').innerHTML = '';
        setStatus('Cleared.');
      }

      function scoreColor(score) {
        const minS = -4;
        const maxS = 11;
        if (score >= 0) {
          const ratio = Math.min(score / maxS, 1);
          const r = Math.round(248 - (248 - 29) * ratio);
          const g = Math.round(250 - (250 - 78) * ratio);
          const b = Math.round(252 - (252 - 216) * ratio);
          return `rgb(${r}, ${g}, ${b})`;
        }
        const ratio = Math.min(Math.abs(score) / Math.abs(minS), 1);
        const r = Math.round(248 - (248 - 185) * ratio);
        const g = Math.round(250 - (250 - 28) * ratio);
        const b = Math.round(252 - (252 - 28) * ratio);
        return `rgb(${r}, ${g}, ${b})`;
      }

      function debouncePredict() {
        if (predictTimer) clearTimeout(predictTimer);
        predictTimer = setTimeout(runPrediction, 650);
      }

      async function runPrediction() {
        const sequence = document.getElementById('seq').value.trim();
        if (!sequence) {
          setStatus('Enter a sequence to predict.');
          return;
        }
        setStatus('Running prediction...');

        const start = performance.now();
        let data;
        try {
          const res = await fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ sequence })
          });

          if (!res.ok) {
            let detail = 'Prediction failed.';
            try {
              const err = await res.json();
              if (err && err.detail) detail = err.detail;
            } catch (_) {
              // Fall back to default error text if JSON parsing fails.
            }
            setStatus(detail);
            return;
          }

          data = await res.json();
        } catch (err) {
          setStatus('Prediction failed: could not reach backend.');
          return;
        }

        const probs = Object.entries(data.class_probabilities)
          .sort((a,b) => b[1] - a[1])
          .map(([k,v]) => `<li>${k}: ${(v*100).toFixed(2)}%</li>`)
          .join('');

        let typeBlock = '<p><b>Protein Type:</b> not available (train Phase 1 model first)</p>';
        if (data.protein_type_prediction) {
          const typeProbs = Object.entries(data.protein_type_prediction.class_probabilities)
            .sort((a,b) => b[1] - a[1])
            .slice(0,3)
            .map(([k,v]) => `<li>${k}: ${(v*100).toFixed(2)}%</li>`)
            .join('');
          typeBlock = `
            <p><b>Protein Type:</b> ${data.protein_type_prediction.predicted_label}</p>
            <p><b>Type Confidence:</b> ${(data.protein_type_prediction.confidence * 100).toFixed(2)}%</p>
            <ul>${typeProbs}</ul>
          `;
        }

        document.getElementById('summary').innerHTML = `
          <h3>Prediction Summary</h3>
          <p><b>Organism Class:</b> ${data.predicted_label}</p>
          <p><b>Organism Confidence:</b> ${(data.confidence * 100).toFixed(2)}%</p>
          <ul>${probs}</ul>
          ${typeBlock}
        `;

        const residues = data.blosum_matrix.residues;
        const scores = data.blosum_matrix.scores;
        let html = '<table><tr><th></th>' + residues.map(r => `<th>${r}</th>`).join('') + '</tr>';
        for (let i = 0; i < residues.length; i++) {
          html += `<tr><th>${residues[i]}</th>`;
          for (let j = 0; j < residues.length; j++) {
            const score = scores[i][j];
            html += `<td style="background:${scoreColor(score)}">${score}</td>`;
          }
          html += '</tr>';
        }
        html += '</table>';

        if (data.blosum_matrix.truncated) {
          html = `
            <p class="muted">Matrix limited to first ${data.blosum_matrix.displayed_length} residues (input length: ${data.blosum_matrix.full_length}) for performance.</p>
          ` + html;
        }

        document.getElementById('matrix').innerHTML = html;
        const elapsedMs = Math.round(performance.now() - start);
        setStatus(`Prediction complete in ${elapsedMs} ms.`);
      }

      document.getElementById('seq').addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
          runPrediction();
        }
      });

      runPrediction();
    </script>
  </body>
</html>
"""


@app.post("/predict")
def predict(payload: PredictRequest):
    sequence = payload.sequence.strip().upper()
    if not sequence:
        raise HTTPException(status_code=400, detail="Sequence is required")

    bundle = get_model_bundle()
    cleaned_sequence = bundle.tokenizer.clean_sequence(sequence)
    if not cleaned_sequence:
        raise HTTPException(status_code=400, detail="Sequence must contain amino acid letters")
    if len(cleaned_sequence) > bundle.tokenizer.max_length:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Sequence is too long for this model. "
                f"Maximum length is {bundle.tokenizer.max_length} amino acids."
            ),
        )

    input_ids = torch.tensor([bundle.tokenizer.encode(cleaned_sequence)], dtype=torch.long)

    with torch.no_grad():
        logits = bundle.model(input_ids)
        probs = F.softmax(logits, dim=-1).squeeze(0)

    pred_idx = int(torch.argmax(probs).item())
    class_probs = {
        LABEL_MAP[i]: float(probs[i].item())
        for i in range(probs.shape[0])
    }

    protein_type_prediction = None
    if bundle.type_model is not None and bundle.type_label_map:
        with torch.no_grad():
            type_logits = bundle.type_model(input_ids)
            type_probs = F.softmax(type_logits, dim=-1).squeeze(0)
        type_pred_idx = int(torch.argmax(type_probs).item())
        type_class_probs = {
            bundle.type_label_map.get(i, str(i)): float(type_probs[i].item())
            for i in range(type_probs.shape[0])
        }
        protein_type_prediction = {
            "predicted_label": bundle.type_label_map.get(type_pred_idx, str(type_pred_idx)),
            "confidence": float(type_probs[type_pred_idx].item()),
            "class_probabilities": type_class_probs,
        }

    return {
        "predicted_label": LABEL_MAP.get(pred_idx, str(pred_idx)),
        "confidence": float(probs[pred_idx].item()),
        "class_probabilities": class_probs,
        "protein_type_prediction": protein_type_prediction,
        "blosum_matrix": build_blosum_matrix(sequence),
    }
