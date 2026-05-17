#!/usr/bin/env python3
"""
train_nn_classifiers.py
═══════════════════════

Phase 1 + Phase 2 of the NN-based prime meta-pattern study.

  Phase 1.  At each scale s = log10(n_centre) ∈ {3, 4, 5, 6, 7, 8}
            sample 2000 primes + 2000 composites near 10**s,
            featurise them with a rich (deliberately redundant) feature
            set so the network has to discover what matters:

              * residues `n mod p` for the first 30 small primes
                normalised to [0, 1)                                    (30)
              * binary representation: lowest 64 bits as 0/1 features    (64)
              * scale features: log10(n)/20, log2(n)/64, digit count/20  (3)
              * wheel structure: n mod 6, mod 30, mod 210                (3)
              * 6k±1 indicator + parity                                  (2)
              * digital root, digit-sum, last decimal digit              (3)

            Total dimension D = 105.  Save the data as numpy npz files.

  Phase 2.  Train a 3-layer MLP (D → 128 → 64 → 32 → 1) at each scale
            with ReLU activations, dropout 0.2, Adam optimiser
            (lr = 1e-3), binary cross-entropy loss, 50 epochs, batch
            size 128.  70 / 15 / 15 train / val / test split.  Save:

              * the trained weights (state_dict)
              * the training / validation accuracy history
              * the final test accuracy and AUC

Outputs go into  artifacts/  (one .npz + one .pt + one .json per scale,
plus a summary training_summary.json).
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sympy import isprime
from sklearn.metrics import roc_auc_score


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

SCALES: List[int] = [3, 4, 5, 6, 7, 8]
SAMPLES_PER_CLASS = 2000

SMALL_PRIMES_30 = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
]
N_BIN_FEATURES = 64

EPOCHS     = 50
BATCH_SIZE = 128
LR         = 1e-3
DROPOUT    = 0.2
HIDDEN     = (128, 64, 32)

ARTIFACT_DIR = Path("artifacts")
SEED         = 20260517


# ─────────────────────────────────────────────────────────────────────────────
# Featurisation
# ─────────────────────────────────────────────────────────────────────────────

FEATURE_GROUPS: Dict[str, List[int]] = {}

def _build_feature_index() -> Tuple[int, Dict[str, List[int]]]:
    """Return (D, mapping group_name -> list of feature indices)."""
    idx = 0
    groups: Dict[str, List[int]] = {}

    groups["residue"] = list(range(idx, idx + len(SMALL_PRIMES_30)))
    idx += len(SMALL_PRIMES_30)

    groups["binary"] = list(range(idx, idx + N_BIN_FEATURES))
    idx += N_BIN_FEATURES

    groups["scale"] = list(range(idx, idx + 3))
    idx += 3

    groups["wheel"] = list(range(idx, idx + 3))
    idx += 3

    groups["sieve"] = list(range(idx, idx + 2))
    idx += 2

    groups["digits"] = list(range(idx, idx + 3))
    idx += 3

    return idx, groups


D, FEATURE_GROUPS = _build_feature_index()
print(f"Total feature dimension D = {D}")
print(f"Feature groups: { {g: len(v) for g, v in FEATURE_GROUPS.items()} }")


def featurize(n: int) -> np.ndarray:
    n = int(n)
    feats: List[float] = []

    # Group A: prime residues normalised to [0, 1)
    for p in SMALL_PRIMES_30:
        feats.append((n % p) / p)

    # Group B: binary representation (lowest 64 bits)
    for i in range(N_BIN_FEATURES):
        feats.append(float((n >> i) & 1))

    # Group C: scale features
    feats.append(math.log10(max(n, 1)) / 20.0)
    feats.append(math.log2(max(n, 1)) / 64.0)
    feats.append(len(str(n)) / 20.0)

    # Group D: wheel structure
    feats.append((n % 6) / 6.0)
    feats.append((n % 30) / 30.0)
    feats.append((n % 210) / 210.0)

    # Group E: sieve indicators
    feats.append(1.0 if (n % 6 == 1 or n % 6 == 5) else 0.0)
    feats.append(float(n & 1))

    # Group F: digits
    digital_root = ((n - 1) % 9 + 1) if n > 0 else 0
    digit_sum    = sum(int(d) for d in str(n))
    feats.append(digital_root / 9.0)
    feats.append(digit_sum / (9.0 * 20.0))
    feats.append((n % 10) / 9.0)

    return np.array(feats, dtype=np.float32)


# ─────────────────────────────────────────────────────────────────────────────
# Sampling
# ─────────────────────────────────────────────────────────────────────────────

def sample_balanced_pairs(scale: int, n_each: int, rng: np.random.Generator):
    n_centre = 10 ** scale
    width = max(int(0.10 * n_centre) + 1, 2 * n_each * 30)

    primes: List[int] = []
    composites: List[int] = []
    seen_p: set = set()
    seen_c: set = set()

    target = n_each
    iters = 0
    max_iters = 800 * n_each + 50_000
    while (len(primes) < target or len(composites) < target) and iters < max_iters:
        iters += 1
        x = int(rng.integers(max(2, n_centre - width), n_centre + width + 1))
        if x < 2:
            continue
        # Bias to 6k±1 to keep iters modest at large s
        biased = rng.random() < 0.7
        if biased and not (x % 6 == 1 or x % 6 == 5):
            continue
        if isprime(x):
            if len(primes) < target and x not in seen_p:
                primes.append(x); seen_p.add(x)
        else:
            if len(composites) < target and x not in seen_c:
                composites.append(x); seen_c.add(x)

    if len(primes) < n_each // 2 or len(composites) < n_each // 2:
        raise RuntimeError(
            f"Could not collect a balanced sample at s={scale}: "
            f"got {len(primes)} primes, {len(composites)} composites in {iters} iters."
        )

    return primes, composites


# ─────────────────────────────────────────────────────────────────────────────
# Model
# ─────────────────────────────────────────────────────────────────────────────

class PrimeMLP(nn.Module):
    """3-layer MLP with dropout.  Tracks per-layer weight matrices for analysis."""

    def __init__(self, in_dim: int, hidden: Tuple[int, int, int] = HIDDEN, p_drop: float = DROPOUT):
        super().__init__()
        h1, h2, h3 = hidden
        self.fc1 = nn.Linear(in_dim, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.fc3 = nn.Linear(h2, h3)
        self.fc_out = nn.Linear(h3, 1)
        self.act = nn.ReLU()
        self.drop = nn.Dropout(p_drop)

    def forward(self, x):
        x = self.drop(self.act(self.fc1(x)))
        x = self.drop(self.act(self.fc2(x)))
        x = self.drop(self.act(self.fc3(x)))
        return self.fc_out(x).squeeze(-1)


# ─────────────────────────────────────────────────────────────────────────────
# Training
# ─────────────────────────────────────────────────────────────────────────────

def train_one_scale(scale: int,
                    rng: np.random.Generator,
                    epochs: int = EPOCHS) -> Dict:
    print(f"\n┌─ scale s = {scale}  (n_centre = 10^{scale}) ──────────────────────")
    t_data = time.perf_counter()
    primes, composites = sample_balanced_pairs(scale, SAMPLES_PER_CLASS, rng)
    print(f"│  sampled {len(primes)} primes, {len(composites)} composites in "
          f"{time.perf_counter() - t_data:.1f}s")

    Xp = np.stack([featurize(p) for p in primes])
    Xc = np.stack([featurize(c) for c in composites])
    X = np.vstack([Xp, Xc])
    y = np.array([1] * len(Xp) + [0] * len(Xc), dtype=np.float32)

    perm = rng.permutation(len(y))
    X = X[perm]; y = y[perm]

    n_train = int(0.70 * len(y))
    n_val   = int(0.15 * len(y))
    X_tr, y_tr = X[:n_train],          y[:n_train]
    X_va, y_va = X[n_train:n_train+n_val], y[n_train:n_train+n_val]
    X_te, y_te = X[n_train+n_val:],    y[n_train+n_val:]

    Xt = torch.tensor(X_tr); yt = torch.tensor(y_tr)
    Xv = torch.tensor(X_va); yv = torch.tensor(y_va)
    Xs = torch.tensor(X_te); ys = torch.tensor(y_te)

    torch.manual_seed(SEED + scale)
    model = PrimeMLP(in_dim=D)
    opt   = optim.Adam(model.parameters(), lr=LR)
    bce   = nn.BCEWithLogitsLoss()

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": [],
               "val_auc": []}

    t_train = time.perf_counter()
    for epoch in range(epochs):
        model.train()
        idx = torch.randperm(len(Xt))
        ep_loss = 0.0; ep_correct = 0
        for i in range(0, len(Xt), BATCH_SIZE):
            j = idx[i:i + BATCH_SIZE]
            xb, yb = Xt[j], yt[j]
            opt.zero_grad()
            logits = model(xb)
            loss = bce(logits, yb)
            loss.backward()
            opt.step()
            ep_loss += float(loss.detach()) * len(j)
            ep_correct += int(((logits.detach() > 0) == (yb > 0.5)).sum())
        train_loss = ep_loss / len(Xt)
        train_acc  = ep_correct / len(Xt)

        model.eval()
        with torch.no_grad():
            logits_v = model(Xv)
            val_loss = float(bce(logits_v, yv))
            preds_v  = (logits_v > 0).int()
            val_acc  = float((preds_v == yv.int()).float().mean())
            try:
                val_auc = float(roc_auc_score(y_va, torch.sigmoid(logits_v).numpy()))
            except ValueError:
                val_auc = 0.5

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        history["val_auc"].append(val_auc)

        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"│   epoch {epoch+1:3d}/{epochs}  "
                  f"train_loss={train_loss:.4f}  train_acc={train_acc:.4f}  "
                  f"val_acc={val_acc:.4f}  val_auc={val_auc:.4f}")

    train_time = time.perf_counter() - t_train

    model.eval()
    with torch.no_grad():
        logits_t = model(Xs)
        test_acc = float(((logits_t > 0).int() == ys.int()).float().mean())
        test_auc = float(roc_auc_score(y_te, torch.sigmoid(logits_t).numpy()))
    print(f"│  test_acc={test_acc:.4f}  test_auc={test_auc:.4f}  "
          f"({train_time:.1f}s training)")
    print("└────────────────────────────────────────────────────────────────")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    npz_path = ARTIFACT_DIR / f"data_s{scale}.npz"
    np.savez(npz_path,
             X_train=X_tr, y_train=y_tr,
             X_val=X_va,   y_val=y_va,
             X_test=X_te,  y_test=y_te,
             primes=np.array(primes), composites=np.array(composites))
    pt_path = ARTIFACT_DIR / f"model_s{scale}.pt"
    torch.save({"state_dict": model.state_dict(),
                "in_dim": D,
                "hidden": HIDDEN,
                "scale":  scale}, pt_path)
    json_path = ARTIFACT_DIR / f"history_s{scale}.json"
    json.dump({"scale": scale, "history": history,
               "test_acc": test_acc, "test_auc": test_auc,
               "train_time_sec": train_time,
               "n_train": len(Xt), "n_val": len(Xv), "n_test": len(Xs),
               "feature_dim": D, "feature_groups": FEATURE_GROUPS,
               "small_primes_30": SMALL_PRIMES_30,
               "n_bin_features": N_BIN_FEATURES,
               "epochs": epochs, "batch_size": BATCH_SIZE, "lr": LR,
               "dropout": DROPOUT, "hidden": HIDDEN, "seed": SEED + scale},
              open(json_path, "w"), indent=2)

    return {"scale": scale, "test_acc": test_acc, "test_auc": test_auc,
            "train_time_sec": train_time, "n_train": len(Xt),
            "model_path": str(pt_path), "data_path": str(npz_path),
            "history_path": str(json_path)}


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    summary = []
    t0 = time.perf_counter()
    for scale in SCALES:
        rng_scale = np.random.default_rng(SEED + scale * 1000)
        summary.append(train_one_scale(scale, rng_scale))
    print(f"\nTotal time: {time.perf_counter() - t0:.1f}s")
    out = ARTIFACT_DIR / "training_summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump({"summary": summary,
               "scales": SCALES,
               "samples_per_class": SAMPLES_PER_CLASS,
               "feature_dim": D,
               "feature_groups": FEATURE_GROUPS,
               "epochs": EPOCHS, "batch_size": BATCH_SIZE,
               "lr": LR, "dropout": DROPOUT, "hidden": HIDDEN,
               "seed": SEED}, open(out, "w"), indent=2)
    print(f"\nWrote {out}")
    print("\nSummary:")
    print(f"  {'scale':>5}  {'test_acc':>8}  {'test_auc':>8}  {'train_time':>10}")
    for r in summary:
        print(f"  {r['scale']:>5}  {r['test_acc']:>8.4f}  {r['test_auc']:>8.4f}  "
              f"{r['train_time_sec']:>9.1f}s")
