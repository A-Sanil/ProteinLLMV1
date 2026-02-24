from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

import torch
import torch.nn as nn
import yaml
from torch.utils.data import DataLoader

from ml.basic_protein_model import BasicProteinClassifier
from ml.protein_tokenizer import ProteinTokenizer
from training.dataset import (
    ProteinSequenceDataset,
    generate_synthetic_examples,
    load_examples_from_csv,
    split_dataset,
)


def load_config(config_path: Path) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def create_datasets(config: Dict[str, Any], tokenizer: ProteinTokenizer, synthetic: bool):
    data_cfg = config["data"]
    if synthetic:
        examples = generate_synthetic_examples(
            num_samples=data_cfg["synthetic_samples"],
            min_len=data_cfg["synthetic_min_length"],
            max_len=data_cfg["synthetic_max_length"],
            seed=config["seed"],
        )
    else:
        examples = load_examples_from_csv(Path(data_cfg["train_csv"]))

    dataset = ProteinSequenceDataset(examples=examples, tokenizer=tokenizer)
    return split_dataset(dataset, val_fraction=data_cfg["val_fraction"], seed=config["seed"])


def evaluate(model, dataloader, loss_fn, device):
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total_count = 0

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            labels = batch["label"].to(device)

            logits = model(input_ids)
            loss = loss_fn(logits, labels)

            total_loss += loss.item() * labels.size(0)
            predictions = torch.argmax(logits, dim=-1)
            total_correct += (predictions == labels).sum().item()
            total_count += labels.size(0)

    avg_loss = total_loss / max(total_count, 1)
    accuracy = total_correct / max(total_count, 1)
    return avg_loss, accuracy


def train(config_path: Path, synthetic: bool):
    config = load_config(config_path)
    torch.manual_seed(config["seed"])

    training_cfg = config["training"]
    model_cfg = config["model"]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = ProteinTokenizer(max_length=model_cfg["max_length"])
    train_dataset, val_dataset = create_datasets(config, tokenizer, synthetic=synthetic)

    train_loader = DataLoader(
        train_dataset,
        batch_size=training_cfg["batch_size"],
        shuffle=True,
        num_workers=0,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=training_cfg["batch_size"],
        shuffle=False,
        num_workers=0,
    )

    model = BasicProteinClassifier(
        vocab_size=len(tokenizer.vocab.token_to_idx),
        max_length=model_cfg["max_length"],
        embedding_dim=model_cfg["embedding_dim"],
        num_heads=model_cfg["num_heads"],
        num_layers=model_cfg["num_layers"],
        ff_dim=model_cfg["ff_dim"],
        dropout=model_cfg["dropout"],
        num_classes=model_cfg["num_classes"],
        pad_id=tokenizer.vocab.pad_id,
    ).to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=training_cfg["learning_rate"],
        weight_decay=training_cfg["weight_decay"],
    )
    loss_fn = nn.CrossEntropyLoss()

    output_dir = Path(training_cfg["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    best_val_loss = float("inf")
    epochs = training_cfg["epochs"]

    print(f"Training on device: {device}")
    print(f"Train samples: {len(train_dataset)} | Val samples: {len(val_dataset)}")

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        total_count = 0

        for batch in train_loader:
            input_ids = batch["input_ids"].to(device)
            labels = batch["label"].to(device)

            optimizer.zero_grad(set_to_none=True)
            logits = model(input_ids)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()

            batch_size = labels.size(0)
            running_loss += loss.item() * batch_size
            total_count += batch_size

        train_loss = running_loss / max(total_count, 1)
        val_loss, val_acc = evaluate(model, val_loader, loss_fn, device)

        print(
            f"Epoch {epoch:02d}/{epochs} | "
            f"train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.4f}"
        )

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            checkpoint_path = output_dir / "basic_protein_classifier.pt"
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "config": config,
                    "vocab": tokenizer.vocab.token_to_idx,
                },
                checkpoint_path,
            )
            print(f"Saved best checkpoint: {checkpoint_path}")

    metadata_path = output_dir / "training_metadata.json"
    metadata = {
        "best_val_loss": best_val_loss,
        "epochs": epochs,
        "synthetic": synthetic,
        "device": str(device),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Saved training metadata: {metadata_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Train a basic protein classifier")
    parser.add_argument(
        "--config",
        type=str,
        default="training/configs/basic_train.yaml",
        help="Path to YAML config",
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Use synthetic generated dataset instead of CSV",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(config_path=Path(args.config), synthetic=args.synthetic)
