#!/usr/bin/env python3
"""
prime_generator.py — Meta-Pattern Prime Generator (corrected)
═══════════════════════════════════════════════════════════════

A hybrid prime generator that combines a `6k±1` candidate sieve with a
small-prime trial-division pre-filter and a scale-adaptive primality test
(deterministic trial division at small scale, Miller–Rabin at large scale).

This file replaces the v1 implementation, which had three serious problems
identified in an external review:

  1. Functional-form inconsistency.  Paper §2.2 reported
     `f_L(s) = 0.258 · exp(-0.373·s)`  (exponential decay in s)
     but the algorithm used
     `alpha = scale ** (-0.37)`        (power law in s)
     These have completely different shapes, and the empirical claim that
     they were the same was false.  Re-fitting on 31 scale samples
     (`fit_meta_pattern.py`) shows that for the directly-meaningful
     "filter rejection rate" curve M2 the exponential and rational forms
     beat the power law decisively (ΔAIC ≥ +17), and for the residue-
     classifier excess-AUC curve M1 the two forms are statistically
     indistinguishable (|ΔAIC| < 1).  The original exponent value `-0.37`
     is also empirically wrong: with proper sampling the exponent is
     `~ -0.10` (M1, power law) or `~ -0.029` (M2, exponential).  See
     `fit_meta_pattern.md` for the full table.

  2. `next_prime` skipped primes at every scale > 836.  The original used
     a random exponential-gap jump in the "global-dominated" regime, which
     overshot intermediate primes.  Empirically: at `n = 1009` the true
     next prime is `1013` but v1 returned `1031`.  Fixed: the default
     `next_prime` is now a strictly correct "smallest prime >= n" sieve.
     The random-gap behaviour is moved to a separate `random_prime_near`
     method, which is the appropriate semantic for cryptographic key
     generation but not for "next prime" semantics.

  3. `miller_rabin` overflowed at `n >= 2**31` because it called
     `np.random.randint(2, n-1)` which returns int32.  Fixed: the witness
     draw now uses Python's `int(rng.integers(2, n-1, dtype=np.uint64))`
     for n < 2**63, and `random.randrange(2, n-1)` (arbitrary-precision)
     above that, with a deterministic-witness fast path for small n.

The "alpha/beta" weight functions are retained for backward compatibility
but their formulas are corrected to match the empirical fits in
`fit_meta_pattern.py`, and they now control only:

  * how many small primes to use in the pre-filter, and
  * which primality test to use (deterministic vs probabilistic).

They no longer drive a random-gap jump in candidate generation, because
that broke "next prime" semantics.
"""

from __future__ import annotations

import math
import random
import time
from math import log, log10, sqrt
from typing import List, Optional, Tuple

import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# Empirical scale-dependent weights (see fit_meta_pattern.py / .md / .json)
# ─────────────────────────────────────────────────────────────────────────────
#
# M2 (filter rejection rate) — best fit by AIC across 31 scale samples:
#   rational      f_M2(s) = 1.050 / (1 + 0.034·s)        AIC = -158.10
#   exponential   f_M2(s) = 1.040 · exp(-0.029·s)        AIC = -156.19
#   power-law     f_M2(s) = 1.057 · s^(-0.111)           AIC = -138.72   (worst)
#
# We use the rational form for M2 because it (a) wins on AIC and (b) is
# bounded above by 1, which is the right physical constraint for a
# rejection probability.
#
# M1 (residue-classifier excess AUC):
#   power-law     f_M1(s) = 0.391 · s^(-0.104)          AIC = -80.19
#   exponential   f_M1(s) = 0.382 · exp(-0.026·s)        AIC = -79.28
# These are statistically indistinguishable (|ΔAIC| < 1).  We retain the
# power-law form for backward compatibility with the paper's symbolism but
# document that the exponential is equally good.
# ─────────────────────────────────────────────────────────────────────────────

# Empirical fits (from fit_meta_pattern.json, 31 scale samples, seed 20260517).
_M1_POWER_A     = 0.391
_M1_POWER_GAMMA = 0.104
_M2_RAT_A       = 1.050
_M2_RAT_B       = 0.034

# Threshold above which we switch primality test from O(sqrt n) trial
# division to O(k log^3 n) Miller–Rabin.  Set by computational cost,
# *not* by the (artifactual) feature-importance crossover.  At s = 4.5,
# n ≈ 31_623, sqrt(n) ≈ 177, which is approximately where Miller–Rabin
# overtakes trial division on commodity hardware.
_PRIMALITY_TEST_SCALE_THRESHOLD = 4.5


# Deterministic Miller–Rabin witness sets known to give exact primality
# for all n below the listed bound.  Source: Sorenson and Webster (2017),
# "Strong pseudoprimes to twelve prime bases".
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
    Hybrid prime generator with corrected internals.

    Default semantics
    -----------------
    `next_prime(n)` returns the *smallest prime ≥ n*.  No primes are
    skipped.  For backward compatibility, the previous random-gap
    behaviour is available as `random_prime_near(n, rng=…)`.

    Backward-compatibility
    ----------------------
    The class also exposes `get_weights(n)` returning `(alpha, beta)`
    using the corrected empirical fits.  These are kept for analysis but
    no longer drive a random-gap jump in candidate generation.
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

    # ── Empirical scale weights ───────────────────────────────────────────

    @staticmethod
    def _scale(n: int) -> float:
        return log10(n) if n > 1 else 1.0

    def filter_weight(self, n: int) -> float:
        """
        M2 fit: empirical probability that a random composite at scale
        `s = log10(n)` is rejected by the small-prime trial-division
        pre-filter.  Best-fit form: `1.050 / (1 + 0.034·s)`.
        """
        s = self._scale(n)
        return _M2_RAT_A / (1.0 + _M2_RAT_B * s)

    def residue_information(self, n: int) -> float:
        """
        M1 fit: empirical "excess AUC" of a residue-only classifier.
        Best-fit form: `0.391 · s^(-0.104)` (power law, indistinguishable
        from `0.382 · exp(-0.026·s)`; |ΔAIC| < 1).
        """
        s = self._scale(n)
        return _M1_POWER_A * (s ** -_M1_POWER_GAMMA)

    def get_weights(self, n: int) -> Tuple[float, float]:
        """
        Backward-compatible weights, now grounded in the corrected fits.
        `alpha`  = local-feature strength  (M1 fit, power law in s)
        `beta`   = global-density-regime strength = 1 - alpha
        """
        alpha = float(self.residue_information(n))
        beta  = float(max(0.0, 1.0 - alpha))
        return alpha, beta

    # ── 6k±1 candidate utilities ──────────────────────────────────────────

    @staticmethod
    def next_6k_pm1(n: int) -> int:
        """Smallest m >= n with m % 6 in {1, 5}, except for 2, 3."""
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
        """Smallest m > n with m % 6 in {1, 5}.  Strictly forward step."""
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
        return n + 2  # mod6 == 5  →  next is 6k+1 four ahead? actually +2

    @staticmethod
    def nearest_6k_pm1(n: int) -> int:
        """Closest m to n with m % 6 in {1, 5}, ties rounding up."""
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
        return n + 1  # mod6 == 4  →  closer to n+1 (≡ 5) than to n-3 (≡ 1)

    # ── Primality tests ────────────────────────────────────────────────────

    @staticmethod
    def trial_division(n: int) -> bool:
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
        """Single Miller–Rabin round.  True = probably prime, False = composite."""
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
        Miller–Rabin primality test.  Uses deterministic witness sets when
        n is below a known bound (then exact for that bound), else
        probabilistic with `k` rounds (defaults to `self.mr_rounds`).

        Witness draws are arbitrary-precision-safe (the v1 implementation
        used `np.random.randint`, which silently overflowed at n >= 2**31).
        """
        n = int(n)
        if n < 2:
            return False
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
            if n == p:
                return True
            if n % p == 0:
                return False

        # Write n-1 as 2^r * d
        d, r = n - 1, 0
        while d % 2 == 0:
            d //= 2
            r += 1

        # Deterministic fast path for small n
        for bound, witnesses in _DETERMINISTIC_WITNESSES:
            if n < bound:
                for a in witnesses:
                    if a >= n:
                        continue
                    if not self._miller_rabin_round(n, a, d, r):
                        return False
                return True

        # Probabilistic for very large n.  Arbitrary-precision witness draw.
        rounds = int(k) if k is not None else self.mr_rounds
        for _ in range(rounds):
            a = random.randrange(2, n - 1)
            if not self._miller_rabin_round(n, a, d, r):
                return False
        return True

    def is_prime(self, n: int) -> bool:
        """Scale-adaptive primality test (the routine used by next_prime)."""
        n = int(n)
        if n < 2:
            return False
        s = self._scale(n)
        if s < _PRIMALITY_TEST_SCALE_THRESHOLD:
            return self.trial_division(n)
        return self.miller_rabin(n)

    # ── Pre-filter ─────────────────────────────────────────────────────────

    def _passes_pre_filter(self, n: int, num_checks: int) -> bool:
        """
        Reject n by trial-dividing with the first `num_checks` small primes.
        Returns True if `n` passes (i.e. is *not* known composite from the
        check), False if `n` is divisible by one of the small primes
        (and is not itself that small prime).
        """
        n = int(n)
        for p in self.small_primes[:num_checks]:
            if n == p:
                return True
            if n % p == 0:
                return False
        return True

    def _filter_strength(self, n: int) -> int:
        """
        How many small primes to filter against, scaled by the M2 weight.

        At small scales we use the full small-prime list; at the largest
        tested scales the M2 rejection rate is still ~0.82, so we still
        use most of the list.  This is a practical micro-optimisation,
        not a correctness consideration — the primality test that follows
        is exact (deterministic) or near-exact (Miller–Rabin).
        """
        w = self.filter_weight(n)
        # Use at least 5 small primes always; scale up to the full list.
        return max(5, min(len(self.small_primes), int(round(len(self.small_primes) * w))))

    # ── Core API ───────────────────────────────────────────────────────────

    def next_prime(self, n: int) -> int:
        """
        Smallest prime `p >= n`.  Strictly correct: never skips primes.

        At small scales (s < 4.5) primality is verified by trial division,
        which is exact.  At large scales (s >= 4.5) primality is verified
        by Miller–Rabin with deterministic witness sets up to the
        Sorenson–Webster bounds (exact below ~3.3 × 10^24) and `mr_rounds`
        random rounds above that.
        """
        n = int(n)
        if n <= 2:
            return 2
        if n <= 3:
            return 3
        # Find first 6k±1 candidate at or above n; do not move past it
        # initially because n itself might be prime (e.g. n = 7).
        candidate = self.next_6k_pm1(n)
        # Fast path: handle the case where `n` is one of {2, 3, 5} directly.
        if n in (2, 3, 5):
            return n
        if candidate < n:
            candidate = self.next_6k_pm1(n)
        num_checks = self._filter_strength(n)
        # Bound on how many candidates we'll test.  Cramér's conjecture gives
        # max gap ~ (ln n)^2; we use 100 ln^2 n as a safety margin.
        max_iter = max(64, int(100 * (math.log(max(n, 2)) ** 2)))
        for _ in range(max_iter):
            if self._passes_pre_filter(candidate, num_checks):
                if self.is_prime(candidate):
                    return candidate
            candidate = self.step_6k_pm1(candidate)
        raise RuntimeError(
            f"next_prime: exceeded {max_iter} candidates starting from {n}; "
            f"this should never happen below Cramér's bound."
        )

    def random_prime_near(self,
                          n: int,
                          rng: Optional[np.random.Generator] = None,
                          max_attempts: int = 1000) -> int:
        """
        Return *a* prime near `n`, sampled via the Cramér gap heuristic
        (gap ~ Exponential(mean = ln n)).  This is the appropriate
        semantic for cryptographic key generation, where any prime near
        the target bit length is acceptable; it is **not** guaranteed to
        be the next prime after `n` and may skip primes.

        Note: in v1 this behaviour was the default of `next_prime`,
        which led to incorrect "next prime" output at every scale > 836.
        It is now an explicit opt-in.
        """
        n = int(n)
        rng = rng or self._rng
        expected_gap = math.log(max(n, 2))
        for _ in range(max_attempts):
            gap = float(rng.exponential(expected_gap))
            candidate = self.nearest_6k_pm1(int(n + gap))
            if self.is_prime(candidate):
                return candidate
            for _step in range(64):
                candidate = self.step_6k_pm1(candidate)
                if self.is_prime(candidate):
                    return candidate
        raise RuntimeError(
            f"random_prime_near: failed after {max_attempts} attempts at n={n}."
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
    print("META-PATTERN PRIME GENERATOR — corrected v2 self-test")
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

    # 2. Verify "next_prime" returns true smallest prime >= n at several seeds.
    targeted_pairs = [
        (2, 2), (3, 3), (4, 5), (5, 5), (6, 7), (8, 11),
        (24, 29), (90, 97), (99, 101), (100, 101), (1000, 1009),
        (1009, 1009), (1010, 1013), (10_000, 10_007), (10_001, 10_007),
        (100_000, 100_003), (1_000_000, 1_000_003),
    ]
    for n, expected in targeted_pairs:
        got = gen.next_prime(n)
        assert got == expected, f"next_prime({n}) -> {got}, expected {expected}"
    print(f"[ ok ] next_prime correct on {len(targeted_pairs)} targeted seeds")

    # 3. No skipping in a sweep.
    from sympy import nextprime  # type: ignore[import-not-found]
    seeds = [97, 1009, 9999, 100_001, 999_983]
    for seed in seeds:
        prev = max(2, seed - 1)
        for _ in range(20):
            true_next = int(nextprime(prev))
            got_next = gen.next_prime(prev + 1)
            assert got_next == true_next, (
                f"skip from {prev}: true next = {true_next}, got {got_next}"
            )
            prev = true_next
    print(f"[ ok ] no skipping over 20-prime sweeps from {len(seeds)} seeds")

    # 4. Large-scale correctness (would have crashed v1 with int32 overflow).
    big_seeds = [10**8, 10**10, 10**12, 10**15]
    from sympy import isprime, nextprime  # type: ignore[import-not-found]
    for seed in big_seeds:
        p = gen.next_prime(seed)
        assert isprime(p)
        assert p == int(nextprime(seed - 1))
    print(f"[ ok ] correct at n = 10**{{8, 10, 12, 15}} (no int32 overflow)")

    # 5. Scale weights now use corrected empirical fits.
    a2, b2 = gen.get_weights(100)        # s = 2
    a8, b8 = gen.get_weights(10**8)      # s = 8
    assert 0.30 < a2 < 0.40, f"alpha at s=2 should be ~0.36, got {a2}"
    assert 0.30 < a8 < 0.40, f"alpha at s=8 should be ~0.32, got {a8}"
    assert abs(a2 - 0.391 * 2 ** -0.104) < 1e-6
    assert abs(gen.filter_weight(100)  - 1.050 / (1 + 0.034 * 2)) < 1e-6
    assert abs(gen.filter_weight(10**8) - 1.050 / (1 + 0.034 * 8)) < 1e-6
    print("[ ok ] scale weights match empirical fits in fit_meta_pattern.json")

    # 6. Performance smoke test.
    print("\nPerformance smoke test:")
    print(f"{'scale':>10s}  {'start':>15s}  {'count':>5s}  {'ms/prime':>10s}")
    print("-" * 50)
    for label, start, count in [
        ("100",  100,           20),
        ("10^4", 10_000,        20),
        ("10^6", 1_000_000,     20),
        ("10^8", 100_000_000,   10),
        ("10^10", 10**10,        5),
        ("10^12", 10**12,        5),
        ("10^15", 10**15,        3),
    ]:
        t0 = time.perf_counter()
        gen.generate_n_primes(start, count)
        ms = 1000.0 * (time.perf_counter() - t0) / count
        print(f"{label:>10s}  {start:>15,d}  {count:>5d}  {ms:>10.3f}")

    print("\nAll tests passed.")


if __name__ == "__main__":
    _self_test()
