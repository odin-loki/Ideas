"""Training loop for the neural decompiler (synthetic demo by default)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split

from .config import EnhancedDecompilerConfig
from .dataset import SyntheticDecompilerDataset, collate_fn
from .metrics import eval_batch_loss_and_acc
from .model import NeuralDecompilerModel


def train_main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Train neural decompiler on synthetic assembly→C pairs.")
    p.add_argument("--epochs", type=int, default=None)
    p.add_argument("--device", type=str, default="cpu")
    p.add_argument("--samples", type=int, default=800)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--val-ratio", type=float, default=0.12, help="Fraction of data for validation (0 disables).")
    p.add_argument("--checkpoint", type=Path, default=None, help="Optional path to save weights (.pt).")
    args = p.parse_args(argv)

    config = EnhancedDecompilerConfig()
    if args.epochs is not None:
        config.num_epochs = args.epochs

    device = torch.device(args.device)
    ds = SyntheticDecompilerDataset(num_samples=args.samples, seed=args.seed)

    pad_id = ds.pad
    collate = collate_fn(pad_id, pad_id, config.max_src_len, config.max_tgt_len)

    gen = torch.Generator().manual_seed(args.seed)
    if args.val_ratio > 0.0 and len(ds) > 2:
        n_val = max(1, int(len(ds) * args.val_ratio))
        n_train = len(ds) - n_val
        train_ds, val_ds = random_split(ds, [n_train, n_val], generator=gen)
        train_loader = DataLoader(
            train_ds,
            batch_size=config.batch_size,
            shuffle=True,
            collate_fn=collate,
            drop_last=True,
        )
        val_loader = DataLoader(
            val_ds,
            batch_size=config.batch_size,
            shuffle=False,
            collate_fn=collate,
            drop_last=False,
        )
    else:
        train_loader = DataLoader(
            ds,
            batch_size=config.batch_size,
            shuffle=True,
            collate_fn=collate,
            drop_last=True,
        )
        val_loader = None

    model = NeuralDecompilerModel(
        config,
        src_vocab_size=ds.src_vocab_size,
        tgt_vocab_size=ds.tgt_vocab_size,
        pad_id=pad_id,
    ).to(device)

    opt = torch.optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)

    for epoch in range(config.num_epochs):
        model.train()
        total = 0.0
        n = 0
        for src, tgt in train_loader:
            src, tgt = src.to(device), tgt.to(device)
            opt.zero_grad(set_to_none=True)
            logits, info = model(src, tgt)
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)),
                tgt[:, 1:].reshape(-1),
                ignore_index=pad_id,
                label_smoothing=config.label_smoothing,
            )
            aux = info.get("aux_loss", torch.tensor(0.0, device=device))
            if isinstance(aux, torch.Tensor):
                loss = loss + config.moe_aux_loss_weight * aux
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.gradient_clip)
            opt.step()
            total += loss.item()
            n += 1

        msg = f"epoch {epoch + 1}/{config.num_epochs}  train_loss={total / max(n, 1):.4f}"
        if val_loader is not None:
            model.eval()
            v_loss = 0.0
            v_acc = 0.0
            m_batches = 0
            with torch.no_grad():
                for src, tgt in val_loader:
                    src, tgt = src.to(device), tgt.to(device)
                    batch_loss, batch_acc, _ = eval_batch_loss_and_acc(
                        model,
                        src,
                        tgt,
                        pad_id,
                        config.label_smoothing,
                        config.moe_aux_loss_weight,
                    )
                    v_loss += batch_loss
                    v_acc += batch_acc
                    m_batches += 1
            msg += f"  val_loss={v_loss / max(m_batches, 1):.4f}  val_tok_acc={v_acc / max(m_batches, 1):.4f}"
        print(msg, flush=True)

    if args.checkpoint:
        args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "model": model.state_dict(),
                "config": config,
                "src_vocab": ds.src_vocab,
                "tgt_vocab": ds.tgt_vocab,
                "samples": args.samples,
                "seed": args.seed,
            },
            args.checkpoint,
        )
        print(f"saved {args.checkpoint}", flush=True)


if __name__ == "__main__":
    train_main(sys.argv[1:])
