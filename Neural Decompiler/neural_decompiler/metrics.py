"""Training-time metrics (masked token accuracy; corpus BLEU without extra deps)."""

from __future__ import annotations

import math
from collections import Counter
from typing import List, Sequence, Tuple

import torch
import torch.nn.functional as F


def masked_token_accuracy(
    logits: torch.Tensor,
    targets: torch.Tensor,
    pad_id: int,
) -> float:
    """
    logits: [B, T, V]
    targets: [B, T] aligned with logits (teacher positions)
    """
    pred = logits.argmax(dim=-1)
    mask = targets != pad_id
    if mask.sum().item() == 0:
        return 0.0
    correct = (pred == targets) & mask
    return (correct.sum().float() / mask.sum().float()).item()


@torch.no_grad()
def eval_batch_loss_and_acc(
    model: torch.nn.Module,
    src: torch.Tensor,
    tgt: torch.Tensor,
    pad_id: int,
    label_smoothing: float,
    moe_weight: float,
) -> Tuple[float, float, float]:
    logits, info = model(src, tgt)
    loss = F.cross_entropy(
        logits.reshape(-1, logits.size(-1)),
        tgt[:, 1:].reshape(-1),
        ignore_index=pad_id,
        label_smoothing=label_smoothing,
    )
    aux = info.get("aux_loss", torch.tensor(0.0, device=loss.device))
    if isinstance(aux, torch.Tensor):
        loss = loss + moe_weight * aux
    acc = masked_token_accuracy(logits, tgt[:, 1:], pad_id)
    aux_val = float(aux.item()) if isinstance(aux, torch.Tensor) else 0.0
    return float(loss.item()), acc, aux_val


def _ngram_counts(tokens: Sequence[str], n: int) -> Counter[Tuple[str, ...]]:
    return Counter(tuple(tokens[i : i + n]) for i in range(max(0, len(tokens) - n + 1)))


def corpus_bleu(
    references: List[Sequence[str]],
    hypotheses: List[Sequence[str]],
    max_n: int = 4,
    smooth: float = 1e-9,
) -> float:
    """
    Corpus-level BLEU (unigram–4-gram) with simple smoothing.
    Each reference/hypothesis is an iterable of string tokens.
    """
    if not references or len(references) != len(hypotheses):
        return 0.0
    log_precisions: List[float] = []
    for n in range(1, max_n + 1):
        match = 0
        total = 0
        for ref, hyp in zip(references, hypotheses):
            rc = _ngram_counts(ref, n)
            hc = _ngram_counts(hyp, n)
            for g, c in hc.items():
                total += c
                match += min(c, rc.get(g, 0))
        if total == 0:
            log_precisions.append(float("-inf"))
        else:
            log_precisions.append(math.log((match + smooth) / (total + smooth)))
    if any(math.isinf(p) and p < 0 for p in log_precisions):
        return 0.0
    geo = sum(log_precisions) / max_n
    ref_len = sum(len(r) for r in references)
    hyp_len = sum(len(h) for h in hypotheses)
    if hyp_len == 0:
        return 0.0
    bp = 1.0 if hyp_len > ref_len else math.exp(1.0 - float(ref_len) / float(hyp_len))
    return bp * math.exp(geo)
