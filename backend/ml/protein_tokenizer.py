from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")


@dataclass(frozen=True)
class ProteinVocab:
    token_to_idx: Dict[str, int]
    idx_to_token: Dict[int, str]
    pad_token: str = "<PAD>"
    unk_token: str = "<UNK>"

    @property
    def pad_id(self) -> int:
        return self.token_to_idx[self.pad_token]

    @property
    def unk_id(self) -> int:
        return self.token_to_idx[self.unk_token]


def build_protein_vocab() -> ProteinVocab:
    tokens = ["<PAD>", "<UNK>"] + AMINO_ACIDS
    token_to_idx = {token: idx for idx, token in enumerate(tokens)}
    idx_to_token = {idx: token for token, idx in token_to_idx.items()}
    return ProteinVocab(token_to_idx=token_to_idx, idx_to_token=idx_to_token)


class ProteinTokenizer:
    def __init__(self, max_length: int):
        self.vocab = build_protein_vocab()
        self.max_length = max_length

    def clean_sequence(self, sequence: str) -> str:
        sequence = sequence.strip().upper()
        return "".join(ch for ch in sequence if ch.isalpha())

    def encode(self, sequence: str) -> List[int]:
        cleaned = self.clean_sequence(sequence)
        token_ids = [
            self.vocab.token_to_idx.get(ch, self.vocab.unk_id)
            for ch in cleaned[: self.max_length]
        ]
        if len(token_ids) < self.max_length:
            token_ids.extend([self.vocab.pad_id] * (self.max_length - len(token_ids)))
        return token_ids

    def batch_encode(self, sequences: Iterable[str]) -> List[List[int]]:
        return [self.encode(sequence) for sequence in sequences]
