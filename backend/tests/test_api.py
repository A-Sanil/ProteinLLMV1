from __future__ import annotations

import json
from types import SimpleNamespace

from fastapi.testclient import TestClient

import api.main as main
from ml.protein_tokenizer import ProteinTokenizer


def make_bundle() -> SimpleNamespace:
    tokenizer = ProteinTokenizer(max_length=128)
    type_label_map = {int(key): value for key, value in json.loads(main.TYPE_LABEL_MAP_PATH.read_text(encoding="utf-8")).items()}

    return SimpleNamespace(
        source="test_bundle",
        tokenizer=tokenizer,
        model=main.HeuristicProteinClassifier(
            num_classes=len(main.LABEL_MAP),
            pad_id=tokenizer.vocab.pad_id,
            token_to_idx=tokenizer.vocab.token_to_idx,
            max_length=tokenizer.max_length,
        ),
        type_model=main.HeuristicProteinClassifier(
            num_classes=len(type_label_map),
            pad_id=tokenizer.vocab.pad_id,
            token_to_idx=tokenizer.vocab.token_to_idx,
            max_length=tokenizer.max_length,
        ),
        type_label_map=type_label_map,
    )


def test_health_and_meta(monkeypatch) -> None:
    bundle = make_bundle()
    monkeypatch.setattr(main, "get_model_bundle", lambda: bundle)

    with TestClient(main.app) as client:
        health = client.get("/health")
        meta = client.get("/api/meta")

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert meta.status_code == 200
    assert meta.json()["model_source"] == "test_bundle"
    assert meta.json()["protein_type_model"] is True


def test_predict_returns_probability_payload(monkeypatch) -> None:
    bundle = make_bundle()
    monkeypatch.setattr(main, "get_model_bundle", lambda: bundle)

    with TestClient(main.app) as client:
        response = client.post(
            "/predict",
            json={"sequence": "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPIL"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["predicted_label"] in main.LABEL_MAP.values()
    assert len(payload["class_probabilities"]) == len(main.LABEL_MAP)
    assert abs(sum(payload["class_probabilities"].values()) - 1.0) < 1e-5
    assert len(payload["blosum_matrix"]["residues"]) > 0