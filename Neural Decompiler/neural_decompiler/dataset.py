"""Synthetic assembly → C-like pairs for smoke training (extend with real corpora)."""

from __future__ import annotations

import random
from typing import Dict, List, Sequence, Tuple

import torch
from torch.utils.data import Dataset


SPECIAL = ("<pad>", "<sos>", "<eos>", "<unk>")


def build_vocab(pairs: Sequence[Tuple[str, str]]) -> Dict[str, int]:
    tokens: List[str] = list(SPECIAL)
    for src, tgt in pairs:
        tokens.extend(src.split())
        tokens.extend(tgt.split())
    uniq = sorted(set(tokens))
    return {t: i for i, t in enumerate(uniq)}


def encode_line(line: str, vocab: Dict[str, int]) -> List[int]:
    unk = vocab["<unk>"]
    return [vocab.get(t, unk) for t in line.split()]


class SyntheticDecompilerDataset(Dataset):
    """Tiny hand-written patterns; expands with random register / immediate noise."""

    def __init__(self, num_samples: int = 500, seed: int = 0):
        rng = random.Random(seed)
        self.pairs = self._templates(rng, num_samples)
        self.src_vocab = build_vocab(self.pairs)
        self.tgt_vocab = build_vocab(self.pairs)
        self.pad = self.src_vocab["<pad>"]
        self.src_sos = self.src_vocab.get("<sos>", 1)
        self.tgt_sos = self.tgt_vocab["<sos>"]
        self.tgt_eos = self.tgt_vocab["<eos>"]

    @property
    def src_vocab_size(self) -> int:
        return len(self.src_vocab)

    @property
    def tgt_vocab_size(self) -> int:
        return len(self.tgt_vocab)

    @staticmethod
    def _templates(rng: random.Random, n: int) -> List[Tuple[str, str]]:
        base = [
            ("mov eax , 1", "int x = 1 ;"),
            ("add eax ebx", "x = x + y ;"),
            ("sub ecx 5", "z = z - 5 ;"),
            ("ret", "return ;"),
            ("push ebp", "// prologue"),
            ("pop ebp", "// epilogue"),
            ("cmp eax 0", "if ( x == 0 )"),
            ("jmp L1", "goto L1 ;"),
            ("call foo", "foo ( ) ;"),
            ("mov ebx eax", "y = x ;"),
        ]
        out: List[Tuple[str, str]] = []
        for i in range(n):
            s, t = base[i % len(base)]
            imm = rng.randint(0, 99)
            if rng.random() > 0.5:
                s = s + f" ; imm {imm}"
                t = t + f" // {imm}"
            out.append((s, t))
        return out

    def __len__(self) -> int:
        return len(self.pairs)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        src_raw, tgt_raw = self.pairs[idx]
        src_ids = [self.src_sos] + encode_line(src_raw, self.src_vocab)
        tgt_ids = [self.tgt_sos] + encode_line(tgt_raw, self.tgt_vocab) + [self.tgt_eos]
        return torch.tensor(src_ids, dtype=torch.long), torch.tensor(tgt_ids, dtype=torch.long)


def collate_fn(
    pad_src: int,
    pad_tgt: int,
    max_src: int,
    max_tgt: int,
):
    def _collate(batch: List[Tuple[torch.Tensor, torch.Tensor]]) -> Tuple[torch.Tensor, torch.Tensor]:
        src_list, tgt_list = zip(*batch)
        src = torch.full((len(batch), max_src), pad_src, dtype=torch.long)
        tgt = torch.full((len(batch), max_tgt), pad_tgt, dtype=torch.long)
        for i, (s, t) in enumerate(zip(src_list, tgt_list)):
            src[i, : min(len(s), max_src)] = s[:max_src]
            tgt[i, : min(len(t), max_tgt)] = t[:max_tgt]
        return src, tgt

    return _collate
