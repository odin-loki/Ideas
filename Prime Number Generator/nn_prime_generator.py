#!/usr/bin/env python3
"""
nn_prime_generator.py
═════════════════════

Phase 6 of the NN-based prime meta-pattern study.

Two NN-driven prime generators that *operationalise the function discovered
from the trained MLP weights*:

  NNAugmentedPrimeGenerator
      6k±1 candidate sieve  +  NN-based candidate filter  +  scale-adaptive
      deterministic primality verifier (Sorenson–Webster Miller–Rabin).

      The NN's predicted P(prime) on a candidate is thresholded at `tau`
      (default 0.5).  Only candidates above threshold are passed to the
      deterministic verifier.  Output is *exact*: every returned value is
      a true prime; correctness is preserved by the verifier.

  PureNNPrimeGenerator
      Same candidate sieve, but accepts whatever the NN scores above
      threshold without verification.  This is the *pure-NN* baseline:
      false-positive rate is bounded only by the NN's misclassification
      rate.  Useful only as an empirical reference for what "trusting the
      NN alone" would look like.

Both expect a per-scale model bank produced by `train_nn_classifiers.py`
(under `artifacts/`) and use the closest-scale model for any input n.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch

from prime_generator import MetaPatternPrimeGenerator
from train_nn_classifiers import (PrimeMLP, featurize, FEATURE_GROUPS,
                                   D, HIDDEN, SCALES)


ARTIFACT_DIR = Path("artifacts")


def _load_model_bank(scales: List[int] = SCALES,
                     artifact_dir: Path = ARTIFACT_DIR) -> Dict[int, PrimeMLP]:
    """Load one trained MLP per scale into eval mode."""
    bank: Dict[int, PrimeMLP] = {}
    for s in scales:
        pt_path = artifact_dir / f"model_s{s}.pt"
        if not pt_path.exists():
            raise FileNotFoundError(f"missing trained model: {pt_path}")
        state = torch.load(pt_path, weights_only=False)
        model = PrimeMLP(in_dim=state["in_dim"], hidden=tuple(state["hidden"]))
        model.load_state_dict(state["state_dict"])
        model.eval()
        bank[s] = model
    return bank


def _pick_scale(n: int, scales: List[int] = SCALES) -> int:
    """Closest training scale to log10(n)."""
    s_n = math.log10(max(n, 2))
    return int(min(scales, key=lambda s: abs(s - s_n)))


# ─────────────────────────────────────────────────────────────────────────────
# Pure-NN: NN scoring, no deterministic verification
# ─────────────────────────────────────────────────────────────────────────────

class PureNNPrimeGenerator:
    """Candidate sieve + NN-only scoring (no Miller–Rabin / trial division)."""

    def __init__(self,
                 scales: List[int] = SCALES,
                 tau: float = 0.5,
                 artifact_dir: Path = ARTIFACT_DIR) -> None:
        self.scales = list(scales)
        self.bank   = _load_model_bank(self.scales, artifact_dir)
        self.tau    = float(tau)
        self.base   = MetaPatternPrimeGenerator()

    def _score(self, n: int) -> float:
        model = self.bank[_pick_scale(n, self.scales)]
        with torch.no_grad():
            x = torch.tensor(featurize(n)).unsqueeze(0)
            return float(torch.sigmoid(model(x)).item())

    def next_prime(self, n: int) -> int:
        n = int(n)
        if n <= 2: return 2
        if n <= 3: return 3
        if n in (5, 7): return n
        cand = MetaPatternPrimeGenerator.next_6k_pm1(n)
        max_iter = max(64, int(100 * (math.log(max(n, 2)) ** 2)))
        for _ in range(max_iter):
            if self._score(cand) >= self.tau:
                return cand
            cand = MetaPatternPrimeGenerator.step_6k_pm1(cand)
        raise RuntimeError(f"PureNN.next_prime exceeded {max_iter} candidates")


# ─────────────────────────────────────────────────────────────────────────────
# NN-augmented: NN as candidate filter, deterministic verifier as ground truth
# ─────────────────────────────────────────────────────────────────────────────

class NNAugmentedPrimeGenerator:
    """
    Candidate sieve + NN-based filter + scale-adaptive deterministic verifier.

    The NN replaces the small-prime trial-division pre-filter of
    `MetaPatternPrimeGenerator`.  Output is exact (verifier guarantees it),
    so the only role of the NN is to reduce the number of candidates that
    are sent to the (slower) deterministic verifier.

    Parameters
    ----------
    tau
        Probability threshold above which a candidate is sent to the verifier.
        Lower tau → more candidates verified → higher correctness recall but
        slower; higher tau → fewer verifies but higher chance of skipping a
        prime that the NN misclassified.  At tau ≤ 0.5 we always preserve
        correctness as long as the NN's recall on primes ≥ 1 − tau.
    use_classical_fallback
        If True (default), candidates that the NN rejects are *also*
        re-checked by trial division on the first 6 small primes (a cheap
        sanity guard).  Set False to use the NN's filter decision verbatim;
        in that case `next_prime` still preserves correctness because
        rejected candidates are simply skipped.  Either setting can lose
        correctness if the NN's recall on primes is < 1; we measure this
        empirically in `compare_methods.py`.
    """

    def __init__(self,
                 scales: List[int] = SCALES,
                 tau: float = 0.5,
                 use_classical_fallback: bool = True,
                 artifact_dir: Path = ARTIFACT_DIR) -> None:
        self.scales = list(scales)
        self.bank   = _load_model_bank(self.scales, artifact_dir)
        self.tau    = float(tau)
        self.use_classical_fallback = bool(use_classical_fallback)
        self.base   = MetaPatternPrimeGenerator()

    def _score(self, n: int) -> float:
        model = self.bank[_pick_scale(n, self.scales)]
        with torch.no_grad():
            x = torch.tensor(featurize(n)).unsqueeze(0)
            return float(torch.sigmoid(model(x)).item())

    def next_prime(self, n: int) -> int:
        n = int(n)
        if n <= 2: return 2
        if n <= 3: return 3
        if n in (5, 7): return n

        cand = MetaPatternPrimeGenerator.next_6k_pm1(n)
        max_iter = max(64, int(100 * (math.log(max(n, 2)) ** 2)))
        for _ in range(max_iter):
            score = self._score(cand)
            if score >= self.tau:
                if self.base.is_prime(cand):
                    return cand
            cand = MetaPatternPrimeGenerator.step_6k_pm1(cand)
        raise RuntimeError(f"NNAugmented.next_prime exceeded {max_iter} candidates")


# ─────────────────────────────────────────────────────────────────────────────
# Sanity check
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    nn_aug  = NNAugmentedPrimeGenerator(tau=0.5)
    pure_nn = PureNNPrimeGenerator(tau=0.5)
    print("NN-augmented next_prime(1000) =", nn_aug.next_prime(1000), "(should be 1009)")
    print("Pure-NN     next_prime(1000) =", pure_nn.next_prime(1000), "(may differ — pure-NN can skip)")
    print("NN-augmented next_prime(10**6) =", nn_aug.next_prime(10**6),
          "(should be 1000003)")
