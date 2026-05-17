#!/usr/bin/env python3
"""
compare_methods.py
══════════════════

Phase 7 of the NN-based prime meta-pattern study.

Head-to-head comparison of three prime generators at every trained scale
`s ∈ {3, 4, 5, 6, 7, 8}`:

  Conventional   MetaPatternPrimeGenerator
                  6k±1 sieve  +  small-prime trial-division pre-filter (15 primes)
                  +  scale-adaptive deterministic primality verifier.

  NN-augmented   NNAugmentedPrimeGenerator
                  6k±1 sieve  +  trained MLP candidate filter
                  +  scale-adaptive deterministic primality verifier.
                  Output is exact (verifier guarantees it).

  Pure-NN        PureNNPrimeGenerator
                  6k±1 sieve  +  trained MLP scoring (no verifier).
                  Output is whatever the NN scores above tau.
                  Allowed to be wrong; we measure how wrong empirically.

Metrics per scale, averaged over a fixed seed window of K = 50 starting
points uniformly placed in `[10^s, 10^s + ε]`:

  * mean ms per produced prime
  * mean candidates examined per prime
  * fraction of candidates accepted by the filter
  * (Pure-NN only) prime-correctness rate of returned values
  * (Pure-NN only) skip rate vs sympy.nextprime ground truth

Output:  artifacts/nn/compare_methods.json
         artifacts/nn/compare_methods.md
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch
from sympy import isprime, nextprime

from prime_generator import MetaPatternPrimeGenerator
from nn_prime_generator import (NNAugmentedPrimeGenerator,
                                 PureNNPrimeGenerator,
                                 _load_model_bank, _pick_scale)
from train_nn_classifiers import featurize, SCALES


ARTIFACT_DIR = Path("artifacts") / "nn"

K_PER_SCALE = 50      # starting points per scale
M_PRIMES    = 5       # primes generated from each starting point
TAU         = 0.5


def _seeds_for_scale(s: int, k: int = K_PER_SCALE,
                     rng: np.random.Generator | None = None) -> List[int]:
    rng = rng or np.random.default_rng(20260517 + s)
    n_centre = 10 ** s
    span = max(int(0.001 * n_centre) + 1, 100)
    return [int(rng.integers(n_centre, n_centre + span)) for _ in range(k)]


def _measure_conventional(gen: MetaPatternPrimeGenerator,
                          seeds: List[int]) -> Dict:
    """Measure conventional generator on the seed list."""
    t_start = time.perf_counter()
    n_primes = 0
    n_candidates = 0
    n_filter_accepts = 0
    bad = 0

    for seed in seeds:
        cur = seed
        for _ in range(M_PRIMES):
            iter_count = [0]
            accept_count = [0]

            cand = MetaPatternPrimeGenerator.next_6k_pm1(cur)
            num_checks = gen._filter_strength(cur)
            max_iter = max(64, int(100 * (math.log(max(cur, 2)) ** 2)))

            p = None
            for _ in range(max_iter):
                iter_count[0] += 1
                if gen._passes_pre_filter(cand, num_checks):
                    accept_count[0] += 1
                    if gen.is_prime(cand):
                        p = cand
                        break
                cand = MetaPatternPrimeGenerator.step_6k_pm1(cand)
            assert p is not None, "conventional failed to find prime"
            if not isprime(p):
                bad += 1
            n_primes += 1
            n_candidates += iter_count[0]
            n_filter_accepts += accept_count[0]
            cur = p + 1

    elapsed = time.perf_counter() - t_start
    return {"name": "conventional",
            "ms_per_prime": elapsed * 1000.0 / n_primes,
            "candidates_per_prime": n_candidates / n_primes,
            "filter_accept_rate": n_filter_accepts / max(1, n_candidates),
            "n_primes": n_primes, "n_bad": bad}


def _measure_nn_augmented(gen: NNAugmentedPrimeGenerator,
                          seeds: List[int]) -> Dict:
    t_start = time.perf_counter()
    n_primes = 0
    n_candidates = 0
    n_filter_accepts = 0
    bad = 0

    for seed in seeds:
        cur = seed
        for _ in range(M_PRIMES):
            cand = MetaPatternPrimeGenerator.next_6k_pm1(cur)
            max_iter = max(64, int(100 * (math.log(max(cur, 2)) ** 2)))
            iters = 0
            accepts = 0
            p = None
            for _ in range(max_iter):
                iters += 1
                score = gen._score(cand)
                if score >= gen.tau:
                    accepts += 1
                    if gen.base.is_prime(cand):
                        p = cand
                        break
                cand = MetaPatternPrimeGenerator.step_6k_pm1(cand)
            assert p is not None, "NN-augmented failed to find prime"
            if not isprime(p):
                bad += 1
            n_primes += 1
            n_candidates += iters
            n_filter_accepts += accepts
            cur = p + 1

    elapsed = time.perf_counter() - t_start
    return {"name": "nn_augmented",
            "ms_per_prime": elapsed * 1000.0 / n_primes,
            "candidates_per_prime": n_candidates / n_primes,
            "filter_accept_rate": n_filter_accepts / max(1, n_candidates),
            "n_primes": n_primes, "n_bad": bad}


def _measure_pure_nn(gen: PureNNPrimeGenerator, seeds: List[int]) -> Dict:
    """
    Run pure-NN to "find primes" with no verifier; record candidates examined,
    timing, and how many returned values are actually prime / are skips
    relative to sympy ground truth.
    """
    t_start = time.perf_counter()
    n_returns = 0
    n_candidates = 0
    n_correct = 0
    n_skips = 0

    for seed in seeds:
        cur = seed
        for _ in range(M_PRIMES):
            true_next = int(nextprime(cur - 1))
            cand = MetaPatternPrimeGenerator.next_6k_pm1(cur)
            max_iter = max(64, int(100 * (math.log(max(cur, 2)) ** 2)))
            iters = 0
            returned = None
            for _ in range(max_iter):
                iters += 1
                if gen._score(cand) >= gen.tau:
                    returned = cand
                    break
                cand = MetaPatternPrimeGenerator.step_6k_pm1(cand)
            assert returned is not None, "pure-NN found nothing above tau"
            n_returns += 1
            n_candidates += iters
            if isprime(returned):
                n_correct += 1
            if returned > true_next:
                n_skips += 1
            cur = returned + 1

    elapsed = time.perf_counter() - t_start
    return {"name": "pure_nn",
            "ms_per_prime": elapsed * 1000.0 / n_returns,
            "candidates_per_prime": n_candidates / n_returns,
            "n_returns": n_returns,
            "primality_recall": n_correct / n_returns,
            "skip_rate_vs_sympy": n_skips / n_returns}


def main() -> None:
    print("Loading models...")
    conv  = MetaPatternPrimeGenerator()
    nn_aug  = NNAugmentedPrimeGenerator(tau=TAU)
    pure_nn = PureNNPrimeGenerator(tau=TAU)

    results: List[Dict] = []
    for s in SCALES:
        print(f"\n── scale s = {s}  (n_centre = 10^{s}) ──────────────────────")
        seeds = _seeds_for_scale(s)

        print(f"   running conventional...")
        r_conv  = _measure_conventional(conv, seeds);   r_conv["scale"]  = s
        print(f"     {r_conv['ms_per_prime']:.3f} ms/prime,  "
              f"{r_conv['candidates_per_prime']:.2f} cand/prime,  "
              f"{r_conv['n_bad']} bad")

        print(f"   running NN-augmented...")
        r_aug   = _measure_nn_augmented(nn_aug, seeds); r_aug["scale"]   = s
        print(f"     {r_aug['ms_per_prime']:.3f} ms/prime,  "
              f"{r_aug['candidates_per_prime']:.2f} cand/prime,  "
              f"{r_aug['n_bad']} bad")

        print(f"   running pure-NN...")
        r_pure  = _measure_pure_nn(pure_nn, seeds);     r_pure["scale"]  = s
        print(f"     {r_pure['ms_per_prime']:.3f} ms/prime,  "
              f"{r_pure['candidates_per_prime']:.2f} cand/prime,  "
              f"recall={r_pure['primality_recall']:.4f},  "
              f"skip_rate={r_pure['skip_rate_vs_sympy']:.4f}")

        results.append({"scale": s, "conv": r_conv,
                        "nn_aug": r_aug, "pure_nn": r_pure})

    out_json = ARTIFACT_DIR / "compare_methods.json"
    json.dump({"scales": SCALES, "k_per_scale": K_PER_SCALE,
               "m_primes": M_PRIMES, "tau": TAU,
               "results": results},
              open(out_json, "w"), indent=2)

    md = ["# Conventional vs NN-augmented vs pure-NN prime generation\n",
          "Each row is the average over "
          f"`K = {K_PER_SCALE}` random starting points × "
          f"`M = {M_PRIMES}` consecutive primes per start.  "
          f"Pure-NN threshold τ = {TAU}.\n",
          ("`ms/prime` is the wall-clock cost per produced prime; "
           "`cand/prime` is the number of 6k±1 candidates examined per produced prime; "
           "`accept_rate` is the fraction of candidates that pass the filter.\n"),
          "## Conventional\n",
          "| scale | ms/prime | cand/prime | accept_rate | bad |",
          "|------:|---------:|-----------:|------------:|----:|"]
    for r in results:
        c = r["conv"]
        md.append(f"| {r['scale']} | {c['ms_per_prime']:.3f} | "
                  f"{c['candidates_per_prime']:.2f} | "
                  f"{c['filter_accept_rate']:.3f} | {c['n_bad']} |")
    md.append("")
    md.append("## NN-augmented (NN filter + deterministic verifier)\n")
    md.append("| scale | ms/prime | cand/prime | accept_rate | bad |")
    md.append("|------:|---------:|-----------:|------------:|----:|")
    for r in results:
        c = r["nn_aug"]
        md.append(f"| {r['scale']} | {c['ms_per_prime']:.3f} | "
                  f"{c['candidates_per_prime']:.2f} | "
                  f"{c['filter_accept_rate']:.3f} | {c['n_bad']} |")
    md.append("")
    md.append("## Pure-NN (NN scoring only, no verifier)\n")
    md.append("| scale | ms/value | cand/value | primality_recall | skip_rate |")
    md.append("|------:|---------:|-----------:|-----------------:|----------:|")
    for r in results:
        c = r["pure_nn"]
        md.append(f"| {r['scale']} | {c['ms_per_prime']:.3f} | "
                  f"{c['candidates_per_prime']:.2f} | "
                  f"{c['primality_recall']:.4f} | {c['skip_rate_vs_sympy']:.4f} |")
    md.append("")
    md.append("## Speed ratio (NN-augmented / conventional)\n")
    md.append("| scale | conv ms | NN-aug ms | ratio |")
    md.append("|------:|--------:|---------:|------:|")
    for r in results:
        ratio = r["nn_aug"]["ms_per_prime"] / r["conv"]["ms_per_prime"]
        md.append(f"| {r['scale']} | "
                  f"{r['conv']['ms_per_prime']:.3f} | "
                  f"{r['nn_aug']['ms_per_prime']:.3f} | {ratio:.1f}× |")
    out_md = ARTIFACT_DIR / "compare_methods.md"
    out_md.write_text("\n".join(md), encoding="utf-8")

    print(f"\nWrote {out_json}")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
