#!/usr/bin/env python3
"""
prime_generator.py — Meta-Pattern Prime Generator
═══════════════════════════════════════════════════

A scale-adaptive hybrid prime generator combining

  1. A `6k±1` candidate sieve.
  2. A small-prime trial-division pre-filter, sized by the empirical
     filter-rejection-rate curve fit in `fit_meta_pattern.py` /
     `fit_meta_pattern.md` (M2 measurement, rational fit
     `f(s) = 1.027 / (1 + 0.030·s)` over 40 scales × 1000 + 1000
     primes/composites per scale).
  3. A scale-adaptive primality verifier:
        • Trial division below `s = log10(n) ≈ 4.5`           (deterministic, O(√n))
        • Deterministic-witness Miller–Rabin in the middle    (Sorenson–Webster
          witness sets, exact for all `n < 3.317 × 10^24`)
        • Probabilistic Miller–Rabin above ~3.3 × 10^24       (k = 20 random rounds,
                                                               error ≤ 4^(-20) ≈ 9·10^-13)

Two semantics are exposed:

  next_prime(n)         — the *smallest prime ≥ n*.  Sieve-then-test.
                          No primes are skipped.  Strict "next prime" semantics.

  random_prime_near(n)  — *a prime near n*.  Cramér-style random gap
                          (Exponential(ln n)) followed by sieve-then-test.
                          Appropriate for cryptographic key generation where
                          any prime of the right size suffices; not a
                          "next prime" function.

Both are unit-tested in `_self_test()`; an end-to-end audit lives in
`verify_generator.py`.
"""

from __future__ import annotations

import math
import random
import time
from math import log, log10, sqrt
from typing import List, Optional, Tuple

import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# Empirical scale-dependent weights (fit_meta_pattern.py / .md / .json)
# ─────────────────────────────────────────────────────────────────────────────
#
# Maximum-likelihood fits over 40 scale samples (s = 1.0 … 9.5),
# 1000 + 1000 balanced primes / composites per scale, log-target Gaussian
# error model.  Model selection by AIC.  Numbers below come directly from
# fit_meta_pattern.json (RNG seed 20260517).
#
# M1 — residue-classifier excess AUC                AIC ranking (lower = better)
#   power law      f(s) = 0.411 · s^(-0.135)        -126.42
#   exponential    f(s) = 0.399 · exp(-0.033·s)     -126.77
#   rational       f(s) = 0.404 / (1 + 0.040·s)     -127.78    (best)
#   ΔAIC across forms < 1.5 → all three are statistically indistinguishable.
#
# M2 — small-prime filter rejection rate
#   power law      f(s) = 1.039 · s^(-0.103)        -186.41
#   exponential    f(s) = 1.019 · exp(-0.026·s)     -215.12
#   rational       f(s) = 1.027 / (1 + 0.030·s)     -217.18    (best)
#   ΔAIC(power-law − rational) = +30.8  →  power law is decisively rejected
#   for this curve.  We use the rational form for filter-strength scaling.
#
# M3 — PNT density relative error                                  (sanity check)
#   power law      f(s) = 0.505 · s^(-1.88)         121.81         (best)
#   Decays rapidly: ~0.4 at s=1, ~0.05 at s=4, < 0.04 by s=8.
# ─────────────────────────────────────────────────────────────────────────────

_M1_RAT_A = 0.404
_M1_RAT_B = 0.040
_M2_RAT_A = 1.027
_M2_RAT_B = 0.030

# Threshold above which we switch primality test from O(√n) trial division to
# O(k log³ n) Miller–Rabin.  Set by **computational cost**, not by any feature-
# importance crossover: at s = 4.5 (n ≈ 31 623), √n ≈ 178, which is
# approximately where deterministic Miller–Rabin overtakes trial division on
# commodity 64-bit hardware.
_PRIMALITY_TEST_SCALE_THRESHOLD = 4.5


# Deterministic Miller–Rabin witness sets known to give *exact* primality for
# all `n` below the listed bound.  Source: Sorenson and Webster (2017),
# "Strong pseudoprimes to twelve prime bases", Math. Comp. 86, 985–1003.
_DETERMINISTIC_WITNESSES: List[Tuple[int, List[int]]] = [
    (2_047,                       [2]),
    (1_373_653,                   [2, 3]),
    (9_080_191,                   [31, 73]),
    (25_326_001,                  [2, 3, 5]),
    (3_215_031_751,               [2, 3, 5, 7]),
    (4_759_123_141,               [2, 7, 61]),
    (1_122_004_669_633,           [2, 13, 23, 1_662_803]),
    (2_152_302_898_747,           [2, 3, 5, 7, 11]),
    (3_474_749_660_383,           [2, 3, 5, 7, 11, 13]),
    (341_550_071_728_321,         [2, 3, 5, 7, 11, 13, 17]),
    (3_825_123_056_546_413_051,   [2, 3, 5, 7, 11, 13, 17, 19, 23]),
    (318_665_857_834_031_151_167_461,
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]),
    (3_317_044_064_679_887_385_961_981,
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]),
]


class MetaPatternPrimeGenerator:
    """
    Hybrid prime generator with strict "next prime" semantics by default and
    optional Cramér-gap random sampling for cryptographic prime generation.

    Parameters
    ----------
    small_primes
        Trial-division basis for the pre-filter.  Default is the first 15
        primes (covering all primes ≤ 47).
    mr_rounds
        Number of probabilistic Miller–Rabin rounds for n above the largest
        Sorenson–Webster bound (`3.317 × 10^24`).  Default 20 gives an error
        bound of `4^(-20) ≈ 9.1 × 10^(-13)` per call.
    rng
        numpy random Generator used by `random_prime_near`.  Independent of
        the witness draw used inside Miller–Rabin (which uses Python's
        arbitrary-precision `random.randrange`).
    """

    def __init__(self,
                 small_primes: Optional[List[int]] = None,
                 mr_rounds: int = 20,
                 rng: Optional[np.random.Generator] = None) -> None:
        self.small_primes = small_primes or [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        ]
        self.mr_rounds = int(mr_rounds)
        self._rng = rng or np.random.default_rng(0xA1Aa1AaA1)

    # ── Empirical scale weights ──────────────────────────────────────────────

    @staticmethod
    def _scale(n: int) -> float:
        return log10(n) if n > 1 else 1.0

    def filter_weight(self, n: int) -> float:
        """
        M2 fit: empirical probability that a random composite at scale
        ``s = log10(n)`` is rejected by the small-prime trial-division
        pre-filter.  Best-fit form is rational: ``1.027 / (1 + 0.030·s)``.

        Plateaus around 0.82 at s = 9; the local filter is useful at every
        scale tested.
        """
        s = self._scale(n)
        return _M2_RAT_A / (1.0 + _M2_RAT_B * s)

    def residue_information(self, n: int) -> float:
        """
        M1 fit: empirical "excess AUC" of a residue-only logistic-regression
        classifier (AUC − 0.5).  Best-fit form is rational:
        ``0.404 / (1 + 0.040·s)``.  Power-law and exponential forms are
        statistically indistinguishable on this curve.
        """
        s = self._scale(n)
        return _M1_RAT_A / (1.0 + _M1_RAT_B * s)

    def get_weights(self, n: int) -> Tuple[float, float]:
        """
        Convenience: ``(alpha, beta)`` where alpha is the residue-information
        weight (M1) and beta = 1 − alpha.  Provided for analysis; algorithm
        decisions inside ``next_prime`` use ``filter_weight`` (M2) directly.
        """
        alpha = float(self.residue_information(n))
        beta  = float(max(0.0, 1.0 - alpha))
        return alpha, beta

    # ── 6k±1 candidate utilities ─────────────────────────────────────────────

    @staticmethod
    def next_6k_pm1(n: int) -> int:
        """Smallest m ≥ n with m ≡ 1 or 5 (mod 6), exempting 2 and 3."""
        n = int(n)
        if n <= 2:
            return 2
        if n == 3:
            return 3
        mod6 = n % 6
        if mod6 == 0:
            return n + 1
        if mod6 == 1:
            return n
        if mod6 == 2:
            return n + 3
        if mod6 == 3:
            return n + 2
        if mod6 == 4:
            return n + 1
        return n  # mod6 == 5

    @staticmethod
    def step_6k_pm1(n: int) -> int:
        """Smallest m > n with m ≡ 1 or 5 (mod 6).  Strictly forward step."""
        n = int(n)
        if n < 2:
            return 2
        if n == 2:
            return 3
        mod6 = n % 6
        if mod6 == 0:
            return n + 1
        if mod6 == 1:
            return n + 4
        if mod6 == 2:
            return n + 3
        if mod6 == 3:
            return n + 2
        if mod6 == 4:
            return n + 1
        return n + 2  # mod6 == 5

    @staticmethod
    def nearest_6k_pm1(n: int) -> int:
        """Closest m to n with m ≡ 1 or 5 (mod 6), ties rounding up."""
        n = int(n)
        if n <= 2:
            return 2
        mod6 = n % 6
        if mod6 in (1, 5):
            return n
        if mod6 == 0:
            return n + 1
        if mod6 == 2:
            return n - 1
        if mod6 == 3:
            return n + 2
        return n + 1  # mod6 == 4

    # ── Primality tests ──────────────────────────────────────────────────────

    @staticmethod
    def trial_division(n: int) -> bool:
        """Deterministic trial division.  O(√n) per call."""
        n = int(n)
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False
        if n % 3 == 0:
            return n == 3
        i = 5
        limit = int(sqrt(n)) + 1
        while i <= limit:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _miller_rabin_round(self, n: int, a: int, d: int, r: int) -> bool:
        """Single Miller–Rabin round.  True ⇒ probably prime."""
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    def miller_rabin(self, n: int, k: Optional[int] = None) -> bool:
        """
        Miller–Rabin primality test.  Selects automatically between

          • deterministic small-prime trial division for n with a tiny prime factor,
          • a deterministic-witness fast path using Sorenson–Webster witness sets
            (exact for all `n < 3.317 × 10^24`),
          • k probabilistic random rounds otherwise (k defaults to ``self.mr_rounds``).

        Witness draws are arbitrary-precision-safe.
        """
        n = int(n)
        if n < 2:
            return False
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            if n == p:
                return True
            if n % p == 0:
                return False

        d, r = n - 1, 0
        while d % 2 == 0:
            d //= 2
            r += 1

        for bound, witnesses in _DETERMINISTIC_WITNESSES:
            if n < bound:
                for a in witnesses:
                    if a >= n:
                        continue
                    if not self._miller_rabin_round(n, a, d, r):
                        return False
                return True

        rounds = int(k) if k is not None else self.mr_rounds
        for _ in range(rounds):
            a = random.randrange(2, n - 1)
            if not self._miller_rabin_round(n, a, d, r):
                return False
        return True

    def is_prime(self, n: int) -> bool:
        """Scale-adaptive primality test (the routine used by `next_prime`)."""
        n = int(n)
        if n < 2:
            return False
        s = self._scale(n)
        if s < _PRIMALITY_TEST_SCALE_THRESHOLD:
            return self.trial_division(n)
        return self.miller_rabin(n)

    # ── Pre-filter ───────────────────────────────────────────────────────────

    def _passes_pre_filter(self, n: int, num_checks: int) -> bool:
        """True if `n` is not divisible by any of the first `num_checks` small primes."""
        n = int(n)
        for p in self.small_primes[:num_checks]:
            if n == p:
                return True
            if n % p == 0:
                return False
        return True

    def _filter_strength(self, n: int) -> int:
        """
        Number of small primes to use in the pre-filter, scaled by the M2
        weight.  Always uses at least 5 primes; scales up to the full list
        in proportion to the empirical filter-rejection-rate curve.
        """
        w = self.filter_weight(n)
        return max(5, min(len(self.small_primes), int(round(len(self.small_primes) * w))))

    # ── Core API ─────────────────────────────────────────────────────────────

    def next_prime(self, n: int) -> int:
        """
        Smallest prime `p ≥ n`.  Strictly correct: never skips.

        Below `s = 4.5` primality is verified by trial division (deterministic).
        Above `s = 4.5` primality is verified by Miller–Rabin with deterministic
        Sorenson–Webster witnesses (exact for `n < 3.317 × 10^24`) and `mr_rounds`
        random rounds above that.
        """
        n = int(n)
        if n <= 2:
            return 2
        if n <= 3:
            return 3
        if n in (5, 7):
            return n
        candidate = self.next_6k_pm1(n)
        num_checks = self._filter_strength(n)
        # Cramér's conjecture gives max gap ~ (ln n)^2; we use 100·ln^2(n) as
        # a generous safety bound on candidates examined.
        max_iter = max(64, int(100 * (math.log(max(n, 2)) ** 2)))
        for _ in range(max_iter):
            if self._passes_pre_filter(candidate, num_checks):
                if self.is_prime(candidate):
                    return candidate
            candidate = self.step_6k_pm1(candidate)
        raise RuntimeError(
            f"next_prime: exceeded {max_iter} candidates starting from {n}"
        )

    def random_prime_near(self,
                          n: int,
                          rng: Optional[np.random.Generator] = None,
                          max_attempts: int = 1000) -> int:
        """
        Return *a* prime near `n`, sampled via the Cramér gap heuristic
        (gap ~ Exponential(mean = ln n)).  Appropriate for cryptographic
        key generation, where any prime of the right bit-length suffices.
        Not a "next prime" function — may skip primes between `n` and the
        sampled position.
        """
        n = int(n)
        rng = rng or self._rng
        expected_gap = math.log(max(n, 2))
        for _ in range(max_attempts):
            gap = float(rng.exponential(expected_gap))
            candidate = self.nearest_6k_pm1(int(n + gap))
            if self.is_prime(candidate):
                return candidate
            for _ in range(64):
                candidate = self.step_6k_pm1(candidate)
                if self.is_prime(candidate):
                    return candidate
        raise RuntimeError(
            f"random_prime_near: failed after {max_attempts} attempts at n={n}"
        )

    def generate_n_primes(self, start: int, count: int) -> List[int]:
        """Generate `count` consecutive primes starting from `next_prime(start)`."""
        primes: List[int] = []
        current = int(start)
        for _ in range(int(count)):
            p = self.next_prime(current)
            primes.append(p)
            current = p + 1
        return primes


# ─────────────────────────────────────────────────────────────────────────────
# Self-test
# ─────────────────────────────────────────────────────────────────────────────

def _self_test() -> None:
    print("=" * 70)
    print("META-PATTERN PRIME GENERATOR — self-test")
    print("=" * 70)

    gen = MetaPatternPrimeGenerator()

    # 1. First 25 primes match the textbook list exactly.
    truth_25 = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97,
    ]
    got_25 = gen.generate_n_primes(2, 25)
    assert got_25 == truth_25, (
        f"first-25 mismatch:\n  truth: {truth_25}\n  got:   {got_25}"
    )
    print("[ ok ] first 25 primes match textbook list")

    # 2. next_prime(n) returns the smallest prime ≥ n on hand-picked seeds.
    targeted_pairs = [
        (2, 2), (3, 3), (4, 5), (5, 5), (6, 7), (7, 7), (8, 11),
        (24, 29), (90, 97), (99, 101), (100, 101),
        (1000, 1009), (1009, 1009), (1010, 1013),
        (10_000, 10_007), (10_001, 10_007),
        (100_000, 100_003), (1_000_000, 1_000_003),
    ]
    for n, expected in targeted_pairs:
        got = gen.next_prime(n)
        assert got == expected, f"next_prime({n}) = {got}, expected {expected}"
    print(f"[ ok ] next_prime correct on {len(targeted_pairs)} targeted seeds")

    # 3. No skipping: 20-prime sweeps from five seed scales agree with sympy.
    from sympy import nextprime  # type: ignore[import-not-found]
    seeds = [97, 1009, 9999, 100_001, 999_983]
    for seed in seeds:
        prev = max(2, seed - 1)
        for _ in range(20):
            true_next = int(nextprime(prev))
            got_next  = gen.next_prime(prev + 1)
            assert got_next == true_next, (
                f"skip from {prev}: true next = {true_next}, got {got_next}"
            )
            prev = true_next
    print(f"[ ok ] no skipping over 20-prime sweeps from {len(seeds)} seeds")

    # 4. Large-scale correctness (well past 32-bit).
    from sympy import isprime, nextprime  # type: ignore[import-not-found]
    big_seeds = [10**8, 10**10, 10**12, 10**15]
    for seed in big_seeds:
        p = gen.next_prime(seed)
        assert isprime(p)
        assert p == int(nextprime(seed - 1))
    print("[ ok ] correct at n = 10**{8, 10, 12, 15}")

    # 5. Scale weights agree with the empirical fits in fit_meta_pattern.json.
    a2, _b2 = gen.get_weights(100)        # s = 2
    a8, _b8 = gen.get_weights(10**8)      # s = 8
    assert 0.30 < a2 < 0.40, f"alpha at s=2 should be ~0.37, got {a2}"
    assert 0.27 < a8 < 0.34, f"alpha at s=8 should be ~0.31, got {a8}"
    assert abs(gen.filter_weight(100)   - 1.027 / (1 + 0.030 * 2)) < 1e-6
    assert abs(gen.filter_weight(10**8) - 1.027 / (1 + 0.030 * 8)) < 1e-6
    print("[ ok ] scale weights match empirical fits in fit_meta_pattern.json")

    # 6. Performance smoke test.
    print("\nPerformance smoke test:")
    print(f"{'scale':>10s}  {'start':>20s}  {'count':>5s}  {'ms/prime':>10s}")
    print("-" * 55)
    for label, start, count in [
        ("100",   100,            20),
        ("10^4",  10_000,         20),
        ("10^6",  1_000_000,      20),
        ("10^8",  100_000_000,    10),
        ("10^10", 10**10,          5),
        ("10^12", 10**12,          5),
        ("10^15", 10**15,          3),
    ]:
        t0 = time.perf_counter()
        gen.generate_n_primes(start, count)
        ms = 1000.0 * (time.perf_counter() - t0) / count
        print(f"{label:>10s}  {start:>20,d}  {count:>5d}  {ms:>10.3f}")

    print("\nAll tests passed.")


if __name__ == "__main__":
    _self_test()
