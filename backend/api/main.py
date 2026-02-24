from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ml.basic_protein_model import BasicProteinClassifier
from ml.protein_tokenizer import ProteinTokenizer


try:
    from Bio.Align import substitution_matrices
except Exception:
    substitution_matrices = None


BACKEND_DIR = Path(__file__).resolve().parents[1]
CHECKPOINT_PATH = BACKEND_DIR / "checkpoints" / "public_small" / "basic_protein_classifier.pt"
TYPE_CHECKPOINT_PATH = BACKEND_DIR / "checkpoints" / "protein_type" / "basic_protein_classifier.pt"
TYPE_LABEL_MAP_PATH = BACKEND_DIR / "data" / "processed" / "protein_type_label_map.json"
LABEL_MAP = {0: "human_swissprot", 1: "yeast_swissprot", 2: "ecoli_swissprot"}


class PredictRequest(BaseModel):
    sequence: str


class ModelBundle:
    def __init__(self):
        checkpoint = torch.load(str(CHECKPOINT_PATH), map_location="cpu")
        config = checkpoint["config"]
        model_cfg = config["model"]

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

        self.type_model: Optional[BasicProteinClassifier] = None
        self.type_label_map: Dict[int, str] = {}

        if TYPE_CHECKPOINT_PATH.exists() and TYPE_LABEL_MAP_PATH.exists():
            type_checkpoint = torch.load(str(TYPE_CHECKPOINT_PATH), map_location="cpu")
            type_cfg = type_checkpoint["config"]["model"]
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

            raw_label_map = json.loads(TYPE_LABEL_MAP_PATH.read_text(encoding="utf-8"))
            self.type_label_map = {int(idx): name for idx, name in raw_label_map.items()}


@lru_cache(maxsize=1)
def get_model_bundle() -> ModelBundle:
    return ModelBundle()


def build_blosum_matrix(sequence: str) -> Dict[str, List]:
    clean_seq = "".join(ch for ch in sequence.upper() if ch.isalpha())
    if not clean_seq:
        return {"residues": [], "scores": []}

    residues = list(clean_seq)

    if substitution_matrices is None:
        size = len(residues)
        scores = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        return {"residues": residues, "scores": scores}

    blosum62 = substitution_matrices.load("BLOSUM62")
    scores = []
    for a in residues:
        row = []
        for b in residues:
            try:
                value = blosum62[(a, b)]
            except Exception:
                try:
                    value = blosum62[(b, a)]
                except Exception:
                    value = -4
            row.append(int(value))
        scores.append(row)

    return {"residues": residues, "scores": scores}


app = FastAPI(title="ProteinLLMV1 Demo")


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
      body { font-family: Arial, sans-serif; margin: 24px; background: #f8fafc; color: #0f172a; }
      .card { background: white; border-radius: 10px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 16px; }
      textarea { width: 100%; min-height: 120px; font-family: monospace; }
      button { padding: 10px 16px; border: none; border-radius: 8px; background: #2563eb; color: white; cursor: pointer; }
      table { border-collapse: collapse; font-size: 12px; }
      td, th { border: 1px solid #cbd5e1; padding: 4px 6px; text-align: center; }
      .muted { color: #64748b; font-size: 13px; }
      .row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px; }
      .chip { border: 1px solid #cbd5e1; border-radius: 999px; padding: 4px 10px; font-size: 12px; cursor: pointer; background: #fff; }
      .status { font-size: 12px; color: #475569; margin-top: 8px; }
      .legend { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
      .legend-bar { width: 220px; height: 14px; border-radius: 8px; background: linear-gradient(90deg, #b91c1c 0%, #f8fafc 50%, #1d4ed8 100%); border: 1px solid #cbd5e1; }
    </style>
  </head>
  <body>
    <h1>ProteinLLMV1 — Prediction Demo</h1>
    <p class="muted">Enhanced demo with organism prediction + Phase 1 protein-type prediction + BLOSUM gradient view.</p>
    <div class="card">
      <label for="seq">Protein Sequence</label>
      <textarea id="seq">EGH</textarea>
      <div class="row">
        <button onclick="runPrediction()">Predict</button>
        <button onclick="clearSequence()">Clear</button>
      </div>
      <div class="row">
        <span class="chip" onclick="setExample('EGH')">Example 1</span>
        <span class="chip" onclick="setExample('MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPIL')">Example 2</span>
        <span class="chip" onclick="setExample('MALWMRLLPLLALLALWGPDPAAA')">Example 3</span>
      </div>
      <div class="status" id="status">Ready.</div>
    </div>
    <div class="card" id="summary"></div>
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
        predictTimer = setTimeout(runPrediction, 450);
      }

      async function runPrediction() {
        const sequence = document.getElementById('seq').value.trim();
        if (!sequence) {
          setStatus('Enter a sequence to predict.');
          return;
        }
        setStatus('Running prediction...');

        const res = await fetch('/predict', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ sequence })
        });

        if (!res.ok) {
          setStatus('Prediction failed.');
          return;
        }

        const data = await res.json();

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
        document.getElementById('matrix').innerHTML = html;
        setStatus('Prediction complete.');
      }

      document.getElementById('seq').addEventListener('input', debouncePredict);
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
    input_ids = torch.tensor([bundle.tokenizer.encode(sequence)], dtype=torch.long)

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
