"""Vocabulary inverse maps and token-id → string for inspection / evaluation."""

from __future__ import annotations

from typing import Dict, Iterable, List, Set

import torch


def invert_vocab(vocab: Dict[str, int]) -> Dict[int, str]:
    return {i: t for t, i in vocab.items()}


def ids_to_tokens(
    ids: Iterable[int],
    inv: Dict[int, str],
    *,
    skip: Set[str] | None = None,
    stop_at: Set[str] | None = None,
) -> List[str]:
    skip = skip or {"<pad>", "<sos>"}
    stop_at = stop_at or {"<eos>"}
    out: List[str] = []
    for i in ids:
        t = inv.get(int(i), "<unk>")
        if t in stop_at:
            break
        if t in skip:
            continue
        out.append(t)
    return out


def ids_tensor_to_string(ids: torch.Tensor, inv: Dict[int, str]) -> str:
    flat = ids.detach().cpu().view(-1).tolist()
    return " ".join(ids_to_tokens(flat, inv))
