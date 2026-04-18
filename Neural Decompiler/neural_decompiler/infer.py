"""Load a checkpoint and print greedy decode vs reference (synthetic data)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

from .dataset import SyntheticDecompilerDataset, encode_line
from .model import NeuralDecompilerModel
from .text import invert_vocab, ids_to_tokens


def load_checkpoint(path: Path, device: torch.device) -> tuple:
    ckpt = torch.load(path, map_location=device, weights_only=False)
    return ckpt


def infer_main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Greedy-decode examples from a training checkpoint.")
    p.add_argument("checkpoint", type=Path, help="Path to .pt from neural_decompiler.train")
    p.add_argument("--device", type=str, default="cpu")
    p.add_argument("--samples", type=int, default=None, help="Must match training if using synthetic data (default: from ckpt or 800).")
    p.add_argument("--seed", type=int, default=None, help="Must match training for identical lines (default from ckpt or 0).")
    p.add_argument("--num-examples", type=int, default=8)
    args = p.parse_args(argv)

    device = torch.device(args.device)
    ckpt = load_checkpoint(args.checkpoint, device)

    config = ckpt["config"]
    src_vocab: dict = ckpt["src_vocab"]
    tgt_vocab: dict = ckpt["tgt_vocab"]
    pad_id = tgt_vocab["<pad>"]
    tgt_sos = tgt_vocab["<sos>"]
    tgt_eos = tgt_vocab["<eos>"]

    samples = args.samples if args.samples is not None else ckpt.get("samples", 800)
    seed = args.seed if args.seed is not None else ckpt.get("seed", 0)

    model = NeuralDecompilerModel(
        config,
        src_vocab_size=len(src_vocab),
        tgt_vocab_size=len(tgt_vocab),
        pad_id=pad_id,
    ).to(device)
    model.load_state_dict(ckpt["model"])
    model.eval()

    inv_src = invert_vocab(src_vocab)

    ds = SyntheticDecompilerDataset(num_samples=samples, seed=seed)
    if ds.src_vocab != src_vocab or ds.tgt_vocab != tgt_vocab:
        print(
            "Warning: rebuilt dataset vocab differs from checkpoint. "
            "Use the same --samples and --seed as training, or re-export vocabs only.",
            flush=True,
        )

    n = min(args.num_examples, len(ds.pairs))
    inv = invert_vocab(tgt_vocab)

    for i in range(n):
        src_raw, tgt_raw = ds.pairs[i]
        src_ids = [src_vocab["<sos>"]] + encode_line(src_raw, src_vocab)
        ref_tgt = [tgt_sos] + encode_line(tgt_raw, tgt_vocab) + [tgt_eos]

        src = torch.tensor([src_ids], dtype=torch.long, device=device)
        max_len = min(config.max_tgt_len, len(ref_tgt) + 16)
        with torch.no_grad():
            out = model.greedy_decode(src, max_len=max_len, bos_id=tgt_sos, eos_id=tgt_eos)

        hyp_str = " ".join(ids_to_tokens(out[0].tolist(), inv))
        ref_str = " ".join(ids_to_tokens(ref_tgt, inv))
        src_str = " ".join(ids_to_tokens(src_ids, inv_src))

        print(f"--- example {i} ---", flush=True)
        print(f"src: {src_str}", flush=True)
        print(f"ref: {ref_str}", flush=True)
        print(f"hyp: {hyp_str}", flush=True)
        print(flush=True)


if __name__ == "__main__":
    infer_main(sys.argv[1:])
