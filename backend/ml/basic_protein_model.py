from __future__ import annotations

import torch
import torch.nn as nn


class BasicProteinClassifier(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        max_length: int,
        embedding_dim: int,
        num_heads: int,
        num_layers: int,
        ff_dim: int,
        dropout: float,
        num_classes: int,
        pad_id: int,
    ):
        super().__init__()
        self.pad_id = pad_id
        self.token_embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=pad_id)
        self.position_embedding = nn.Embedding(max_length, embedding_dim)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim,
            nhead=num_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True,
            activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(embedding_dim, num_classes)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len = input_ids.shape
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0).expand(batch_size, -1)

        token_embeddings = self.token_embedding(input_ids)
        positional_embeddings = self.position_embedding(positions)
        hidden_states = token_embeddings + positional_embeddings

        padding_mask = input_ids.eq(self.pad_id)
        encoded = self.encoder(hidden_states, src_key_padding_mask=padding_mask)

        non_pad_mask = (~padding_mask).unsqueeze(-1)
        sum_embeddings = (encoded * non_pad_mask).sum(dim=1)
        lengths = non_pad_mask.sum(dim=1).clamp(min=1)
        pooled = sum_embeddings / lengths

        logits = self.classifier(self.dropout(pooled))
        return logits
