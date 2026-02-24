from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

import pandas as pd
import torch
from torch.utils.data import Dataset, random_split

from ml.protein_tokenizer import AMINO_ACIDS, ProteinTokenizer


@dataclass
class SequenceExample:
    sequence: str
    label: int


class ProteinSequenceDataset(Dataset):
    def __init__(self, examples: Sequence[SequenceExample], tokenizer: ProteinTokenizer):
        self.examples = list(examples)
        self.tokenizer = tokenizer

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> dict:
        example = self.examples[idx]
        return {
            "input_ids": torch.tensor(self.tokenizer.encode(example.sequence), dtype=torch.long),
            "label": torch.tensor(example.label, dtype=torch.long),
        }


def load_examples_from_csv(csv_path: Path) -> List[SequenceExample]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    dataframe = pd.read_csv(csv_path)
    required_columns = {"sequence", "label"}
    if not required_columns.issubset(set(dataframe.columns)):
        raise ValueError(
            f"CSV must contain columns {required_columns}, but found {set(dataframe.columns)}"
        )

    examples: List[SequenceExample] = []
    for row in dataframe.itertuples(index=False):
        examples.append(SequenceExample(sequence=str(row.sequence), label=int(row.label)))
    return examples


def generate_synthetic_examples(
    num_samples: int,
    min_len: int,
    max_len: int,
    seed: int,
) -> List[SequenceExample]:
    rng = random.Random(seed)
    examples: List[SequenceExample] = []

    hydrophobic = set("AILMFWYV")
    for _ in range(num_samples):
        length = rng.randint(min_len, max_len)
        sequence = "".join(rng.choice(AMINO_ACIDS) for _ in range(length))
        hydrophobic_ratio = sum(ch in hydrophobic for ch in sequence) / float(length)
        label = 1 if hydrophobic_ratio > 0.45 else 0
        examples.append(SequenceExample(sequence=sequence, label=label))

    return examples


def split_dataset(dataset: Dataset, val_fraction: float, seed: int) -> Tuple[Dataset, Dataset]:
    total_size = len(dataset)
    if total_size < 2:
        raise ValueError("Dataset requires at least 2 samples for train/val split")

    val_size = max(1, int(total_size * val_fraction))
    train_size = total_size - val_size
    if train_size == 0:
        train_size = total_size - 1
        val_size = 1

    generator = torch.Generator().manual_seed(seed)
    return random_split(dataset, [train_size, val_size], generator=generator)
