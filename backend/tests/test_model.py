from __future__ import annotations

import torch

from ml.basic_protein_model import BasicProteinClassifier
from ml.protein_tokenizer import ProteinTokenizer


def test_classifier_forward_shape() -> None:
    torch.manual_seed(0)

    tokenizer = ProteinTokenizer(max_length=12)
    model = BasicProteinClassifier(
        vocab_size=len(tokenizer.vocab.token_to_idx),
        max_length=12,
        embedding_dim=16,
        num_heads=4,
        num_layers=2,
        ff_dim=32,
        dropout=0.0,
        num_classes=3,
        pad_id=tokenizer.vocab.pad_id,
    )

    input_ids = torch.tensor(
        [tokenizer.encode("MKTAYIAKQRQI"), tokenizer.encode("GGGPPPAAA")],
        dtype=torch.long,
    )
    logits = model(input_ids)

    assert logits.shape == (2, 3)
    assert torch.isfinite(logits).all()