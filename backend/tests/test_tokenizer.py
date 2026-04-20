from __future__ import annotations

from ml.protein_tokenizer import ProteinTokenizer


def test_clean_sequence_removes_non_letters() -> None:
    tokenizer = ProteinTokenizer(max_length=8)

    assert tokenizer.clean_sequence("acd-efg123") == "ACDEFG"


def test_encode_pads_and_maps_unknowns() -> None:
    tokenizer = ProteinTokenizer(max_length=6)

    encoded = tokenizer.encode("ABZ")

    assert encoded[0] == tokenizer.vocab.token_to_idx["A"]
    assert encoded[1] == tokenizer.vocab.unk_id
    assert encoded[2] == tokenizer.vocab.unk_id
    assert encoded[3:] == [tokenizer.vocab.pad_id, tokenizer.vocab.pad_id, tokenizer.vocab.pad_id]


def test_batch_encode_returns_fixed_length_batches() -> None:
    tokenizer = ProteinTokenizer(max_length=4)

    batch = tokenizer.batch_encode(["ACD", "W"])

    assert len(batch) == 2
    assert all(len(item) == 4 for item in batch)