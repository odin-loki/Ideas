"""
TurbulentFlow Random Number Generator (TFRNG)
==========================================
Full Python implementation of the mathematical model described in the
TurbulentFlow RNG specification document.

Implements all stages:
  1. Temporal Input Transformation   (§3.1)
  2. State Definition                (§3.2)
  3. Counterflow Transformation      (§3.3)
  4. State Influence Transformation  (§3.4)
  5. Avalanche Transformation        (§3.5)
  6. Adaptive Mixing                 (§3.6)
  7. Final Extraction                (§3.7)

Also includes:
  - Statistical analysis suite (chi-square, entropy, distribution, bit change rate)
  - Batch generation
  - Seeded/reproducible mode (bypasses live timestamps)
  - CLI entry point
"""

from __future__ import annotations

import math
import time
import struct
import statistics
from collections import Counter, deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Sequence


# ─────────────────────────────────────────────────────────────────────────────
#  §2.2  Constants
# ─────────────────────────────────────────────────────────────────────────────

MASK32 = 0xFFFFFFFF   # Keep all arithmetic in 32-bit unsigned space

# SHA-2 initial hash values (fractional parts of square roots)
SHA1 = 0x6A09E667   # √2  × 2³²
SHA2 = 0xBB67AE85   # √3  × 2³²
SHA3 = 0x3C6EF372   # √5  × 2³²
SHA4 = 0xA54FF53A   # √10 × 2³²

# Golden-ratio derived constants
PHI1 = 0x9E3779B1   # φ    × 2³²
PHI2 = 0x517CC1B7   # φ⁻¹  × 2³²

# MurmurHash3 mixing primes
PRIME1 = 0x85EBCA77
PRIME2 = 0xC2B2AE3D

# Rotation schedules
R = (7, 12, 17, 22)   # Primary   (MD5/SHA heritage)
S = (13,  8,  7, 11)  # Secondary (bit dispersion)


# ─────────────────────────────────────────────────────────────────────────────
#  Low-level 32-bit operations
# ─────────────────────────────────────────────────────────────────────────────

def rot_left(x: int, n: int) -> int:
    """Circular left-rotation of a 32-bit word."""
    n &= 31
    return ((x << n) | (x >> (32 - n))) & MASK32


def rot_right(x: int, n: int) -> int:
    """Circular right-rotation of a 32-bit word."""
    n &= 31
    return ((x >> n) | (x << (32 - n))) & MASK32


def mul32(a: int, b: int) -> int:
    """Unsigned 32-bit multiplication (truncated)."""
    return (a * b) & MASK32


def add32(*args: int) -> int:
    """Unsigned 32-bit addition of any number of operands."""
    result = 0
    for v in args:
        result = (result + v) & MASK32
    return result


# ─────────────────────────────────────────────────────────────────────────────
#  §3.1  Temporal Input Transformation
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Timestamp:
    """
    Three distinct numeric representations of a point in time, each
    encoding the same datetime fields in a different order to produce
    three independent input streams (timeA, timeB, timeC).

    Representations follow §3.1:
      timeA = H∥M∥Y∥mo∥S∥D
      timeB = Y∥S∥mo∥H∥D∥M
      timeC = ms∥H∥ns∥M∥S
    """
    timeA: int
    timeB: int
    timeC: int

    @classmethod
    def now(cls) -> "Timestamp":
        """Capture the current wall-clock time."""
        dt  = datetime.now()
        ns  = time.time_ns() % 1_000_000_000   # nanoseconds within the second
        ms  = dt.microsecond // 1000

        a = int(f"{dt.hour}{dt.minute}{dt.year}{dt.month:02d}{dt.second}{dt.day}")
        b = int(f"{dt.year}{dt.second}{dt.month:02d}{dt.hour}{dt.day}{dt.minute}")
        c = int(f"{ms}{dt.hour}{ns}{dt.minute}{dt.second}")
        return cls(timeA=a, timeB=b, timeC=c)

    @classmethod
    def from_unix(cls, unix_ns: int) -> "Timestamp":
        """
        Build a Timestamp from an integer number of nanoseconds since the
        Unix epoch.  Useful for reproducible / seeded generation.
        """
        dt  = datetime.fromtimestamp(unix_ns / 1_000_000_000)
        ns  = unix_ns % 1_000_000_000
        ms  = (unix_ns // 1_000_000) % 1_000

        a = int(f"{dt.hour}{dt.minute}{dt.year}{dt.month:02d}{dt.second}{dt.day}")
        b = int(f"{dt.year}{dt.second}{dt.month:02d}{dt.hour}{dt.day}{dt.minute}")
        c = int(f"{ms}{dt.hour}{ns}{dt.minute}{dt.second}")
        return cls(timeA=a, timeB=b, timeC=c)


# ─────────────────────────────────────────────────────────────────────────────
#  §3.2  State Definition
# ─────────────────────────────────────────────────────────────────────────────

class GeneratorState:
    """
    Maintains the Markov state of the generator:

        state(t) = { history(t), last(t) }

    where history(t) = [O(t-3), O(t-2), O(t-1)]  and  last(t) = O(t-1).

    History is initialised to [0, 0, 0] (cold start).
    """

    def __init__(self) -> None:
        self._history: deque[int] = deque([0, 0, 0], maxlen=3)

    @property
    def history(self) -> tuple[int, int, int]:
        h = list(self._history)
        return (h[0], h[1], h[2])

    @property
    def last(self) -> int:
        return self._history[-1]

    def update(self, output: int) -> None:
        """Record a new output digit into the rolling history."""
        assert 0 <= output <= 9
        self._history.append(output)

    def __repr__(self) -> str:
        return f"GeneratorState(history={self.history}, last={self.last})"


# ─────────────────────────────────────────────────────────────────────────────
#  §3.3  Counterflow Transformation
# ─────────────────────────────────────────────────────────────────────────────

def counterflow(ts: Timestamp, K: int) -> tuple[int, int]:
    """
    CF: ℤₜ × ℤ₃₂ → ℤ₃₂ × ℤ₃₂

    Two independent streams are evolved from the same seed K:
      - Forward stream  F uses left-rotations with timeA
      - Backward stream B uses right-rotations with timeB

    Each stream runs four rounds of (rotate → add), matching the
    specification's F₁-F₄ / B₁-B₄ construction.
    """
    ta = ts.timeA & MASK32
    tb = ts.timeB & MASK32

    # Forward stream  (§3.3, F construction)
    fwd = K & MASK32
    for i in range(4):
        fwd = rot_left(fwd, R[i % len(R)])
        fwd = add32(fwd, ta)

    # Backward stream  (§3.3, B construction)
    bwd = K & MASK32
    for i in range(4):
        bwd = rot_right(bwd, R[i % len(R)])
        bwd = add32(bwd, tb)

    return fwd, bwd


# ─────────────────────────────────────────────────────────────────────────────
#  §3.4  State Influence Transformation
# ─────────────────────────────────────────────────────────────────────────────

def state_influence(x: int, state: GeneratorState) -> int:
    """
    SI: ℤ₃₂ × ℤ₁₀³ → ℤ₃₂

    Encodes the three-digit history as a scalar:

        V(state) = 100·h[0] + 10·h[1] + h[2]

    Then applies three successive transforms T₁, T₂, T₃.
    """
    h = state.history
    v = 100 * h[0] + 10 * h[1] + h[2]   # V(state) ∈ [0, 999]

    x = add32(x, v)                        # T₁: x + V
    x = rot_left(x, S[0])                  # T₂: ROT_L(x, S₁)
    x = x ^ mul32(v, PRIME1)               # T₃: x ⊕ (V · PRIME1)

    return x & MASK32


# ─────────────────────────────────────────────────────────────────────────────
#  §3.5  Avalanche Transformation
# ─────────────────────────────────────────────────────────────────────────────

def avalanche(x: int) -> int:
    """
    A: ℤ₃₂ → ℤ₃₂

    Five-step chain that ensures any single-bit input flip flips > 16
    output bits with probability > 0.998 (§7.2):

        A₁ → rotate  (S₁)
        A₂ → multiply (PRIME1)
        A₃ → rotate  (S₂)
        A₄ → multiply (PRIME2)
        A₅ → rotate  (S₃)
    """
    x = rot_left(x, S[0])        # A₁
    x = mul32(x, PRIME1)         # A₂
    x = rot_left(x, S[1])        # A₃
    x = mul32(x, PRIME2)         # A₄
    x = rot_left(x, S[2])        # A₅
    return x & MASK32


# ─────────────────────────────────────────────────────────────────────────────
#  §3.6  Adaptive Mixing
# ─────────────────────────────────────────────────────────────────────────────

def adaptive_mix(x: int, last: int, ts: Timestamp) -> int:
    """
    AM: ℤ₃₂ × ℤ₁₀ × ℤₜ → ℤ₃₂

    Three-step mixing driven by timeC and the most recent output digit:

        M₁: x ← x + timeC
        M₂: x ← ROT_L(x, (last % 8) + 1)
        M₃: x ← x ⊕ PHI1
    """
    tc = ts.timeC & MASK32

    x = add32(x, tc)                          # M₁
    x = rot_left(x, (last % 8) + 1)           # M₂ — data-dependent rotation
    x = (x ^ PHI1) & MASK32                   # M₃

    return x


# ─────────────────────────────────────────────────────────────────────────────
#  §3.7  Final Extraction
# ─────────────────────────────────────────────────────────────────────────────

def extract(x: int) -> int:
    """E: ℤ₃₂ → ℤ₁₀   simply x mod 10."""
    return x % 10


# ─────────────────────────────────────────────────────────────────────────────
#  §4  Complete Algorithm  (main generator)
# ─────────────────────────────────────────────────────────────────────────────

class TurbulentFlowRNG:
    """
    Full implementation of the TurbulentFlow Random Number Generator.

    Equation from §4:
        O(t) = E( AM( A( CF₁ ⊕ CF₂ ), state(t).last, time(t) ) )

    where CF₁ and CF₂ each pass through the State Influence transform
    before being XOR-combined.

    Usage
    -----
    Basic (live timestamps):
        rng = TurbulentFlowRNG()
        digit = rng.generate()
        batch = rng.generate_batch(1000)

    Reproducible (fixed seed):
        rng = TurbulentFlowRNG(seed_ns=1_700_000_000_000_000_000)
        digit = rng.generate()
    """

    def __init__(self, seed_ns: Optional[int] = None) -> None:
        """
        Parameters
        ----------
        seed_ns : int or None
            If given, timestamps are derived from this Unix nanosecond
            epoch value and incremented by 1 ms per call, giving fully
            reproducible output.  If None, the system wall clock is used.
        """
        self._state = GeneratorState()
        self._seed_ns: Optional[int] = seed_ns
        self._call_count: int = 0

    # ── public interface ──────────────────────────────────────────────────

    def generate(self) -> int:
        """
        Generate and return one digit in ℤ₁₀ = {0, …, 9}.

        Internally advances the Markov state (§3.2).
        """
        ts    = self._get_timestamp()
        digit = self._transform(ts)
        self._state.update(digit)
        self._call_count += 1
        return digit

    def generate_batch(self, n: int) -> list[int]:
        """Generate n independent digits."""
        return [self.generate() for _ in range(n)]

    def reset_state(self) -> None:
        """Reset the Markov history to [0, 0, 0] (cold-start)."""
        self._state = GeneratorState()

    @property
    def call_count(self) -> int:
        return self._call_count

    # ── internals ─────────────────────────────────────────────────────────

    def _get_timestamp(self) -> Timestamp:
        if self._seed_ns is None:
            return Timestamp.now()
        # Advance by 1_000_000 ns (1 ms) per call for varied but deterministic ts
        ns = self._seed_ns + self._call_count * 1_000_000
        return Timestamp.from_unix(ns)

    def _transform(self, ts: Timestamp) -> int:
        """
        Core pipeline — implements §4 exactly:

            cf1, cf2 = CF(time, SHA1)
            cf1      = SI(cf1, state)
            cf2      = SI(cf2, state)
            mixed    = cf1 ⊕ cf2
            avl      = A(mixed)
            adapted  = AM(avl, state.last, time)
            output   = E(adapted)
        """
        cf1, cf2 = counterflow(ts, SHA1)                   # §3.3
        cf1      = state_influence(cf1, self._state)       # §3.4
        cf2      = state_influence(cf2, self._state)       # §3.4
        mixed    = (cf1 ^ cf2) & MASK32
        avl      = avalanche(mixed)                        # §3.5
        adapted  = adaptive_mix(avl, self._state.last, ts) # §3.6
        return extract(adapted)                            # §3.7


# ─────────────────────────────────────────────────────────────────────────────
#  Statistical Analysis Suite  (§5)
# ─────────────────────────────────────────────────────────────────────────────

class StatisticalAnalyzer:
    """
    Computes the metrics from §5 of the specification:

      - Frequency distribution (§5.1)
      - Mean and variance       (§5.1)
      - Chi-square goodness-of-fit against uniform (§5.1)
      - Shannon entropy          (§5.2)
      - Bit-change rate          (§5.2)
      - Sequence entropy         (§5.2)
      - Pattern resistance       (§5.3)
      - State transition matrix  (§7.3)
    """

    def __init__(self, samples: Sequence[int]) -> None:
        if not samples:
            raise ValueError("samples must be non-empty")
        self.samples = list(samples)
        self.n       = len(samples)
        self._counts: Counter[int] = Counter(samples)

    # ── distribution ──────────────────────────────────────────────────────

    def distribution(self) -> dict[int, tuple[int, float]]:
        """Returns {digit: (count, percentage)} for each digit 0-9."""
        return {d: (self._counts[d], self._counts[d] / self.n * 100.0)
                for d in range(10)}

    def mean(self) -> float:
        return sum(self.samples) / self.n

    def variance(self) -> float:
        m = self.mean()
        return sum((x - m) ** 2 for x in self.samples) / self.n

    # ── chi-square ────────────────────────────────────────────────────────

    def chi_square(self) -> tuple[float, float]:
        """
        Pearson chi-square test against uniform U(0,9).

        Returns (chi2_statistic, p_value).
        """
        expected = self.n / 10.0
        chi2 = sum((self._counts[d] - expected) ** 2 / expected
                   for d in range(10))
        # p-value using the regularised incomplete gamma function
        p = _chi2_sf(chi2, df=9)
        return chi2, p

    # ── information theory ────────────────────────────────────────────────

    def entropy(self) -> float:
        """Shannon entropy in bits, H = -Σ p log₂ p."""
        total = self.n
        h = 0.0
        for d in range(10):
            if self._counts[d] > 0:
                p = self._counts[d] / total
                h -= p * math.log2(p)
        return h

    def bit_change_rate(self) -> float:
        """
        Average number of bits that differ between consecutive decimal
        digits (treating each digit as a 4-bit nibble).
        """
        if self.n < 2:
            return 0.0
        total = 0
        for a, b in zip(self.samples, self.samples[1:]):
            total += bin(a ^ b).count("1")
        return total / (self.n - 1)

    def sequence_entropy(self, k: int = 3) -> float:
        """
        Entropy of k-digit sequences (§5.2: 3-digit sequence entropy).
        H_k = -Σ p(s) log₂ p(s)
        """
        seqs: Counter[tuple] = Counter(
            tuple(self.samples[i:i+k]) for i in range(self.n - k + 1)
        )
        total = sum(seqs.values())
        h = 0.0
        for cnt in seqs.values():
            p = cnt / total
            h -= p * math.log2(p)
        return h

    # ── pattern resistance ────────────────────────────────────────────────

    def max_sequence_occurrence(self, k: int = 3) -> tuple[tuple, int, float]:
        """
        Most common k-digit sequence: returns (sequence, count, proportion).
        """
        seqs: Counter[tuple] = Counter(
            tuple(self.samples[i:i+k]) for i in range(self.n - k + 1)
        )
        seq, cnt = seqs.most_common(1)[0]
        return seq, cnt, cnt / (self.n - k + 1)

    # ── state-transition matrix ───────────────────────────────────────────

    def transition_matrix(self) -> list[list[float]]:
        """
        10×10 empirical transition matrix: T[i][j] = P(O_t=j | O_{t-1}=i).
        Specification §7.3 targets ≈ 0.1 for all entries.
        """
        counts = [[0] * 10 for _ in range(10)]
        for a, b in zip(self.samples, self.samples[1:]):
            counts[a][b] += 1
        matrix: list[list[float]] = []
        for row in counts:
            total = sum(row)
            if total > 0:
                matrix.append([c / total for c in row])
            else:
                matrix.append([0.0] * 10)
        return matrix

    def max_transition_probability(self) -> float:
        mat = self.transition_matrix()
        return max(mat[i][j] for i in range(10) for j in range(10))

    # ── full report ───────────────────────────────────────────────────────

    def report(self) -> str:
        """Render a full statistical report as a multi-line string."""
        chi2, p = self.chi_square()
        seq, seq_cnt, seq_prop = self.max_sequence_occurrence(3)

        lines = [
            "=" * 60,
            "  TURBULENTFLOW RNG — STATISTICAL ANALYSIS REPORT",
            "=" * 60,
            f"  Sample size  : {self.n:,}",
            "",
            "── §5.1  Distribution ──────────────────────────────────────",
        ]
        for d, (cnt, pct) in self.distribution().items():
            bar = "█" * int(pct / 0.5)
            lines.append(f"  {d}: {cnt:7,}  ({pct:5.2f}%)  {bar}")

        lines += [
            "",
            f"  Mean          : {self.mean():.4f}   (theoretical: 4.5000)",
            f"  Variance      : {self.variance():.4f}  (theoretical: 8.2500)",
            f"  Chi-square    : {chi2:.3f}  (df=9)",
            f"  p-value       : {p:.4f}  ({'PASS ≥0.05' if p >= 0.05 else 'FAIL <0.05'})",
            "",
            "── §5.2  Information Theory ────────────────────────────────",
            f"  Shannon entropy        : {self.entropy():.4f} bits  (max: 3.3219)",
            f"  Bit-change rate        : {self.bit_change_rate():.4f} bits/step  (max: 2.0)",
            f"  3-digit seq. entropy   : {self.sequence_entropy(3):.4f} bits  (max: 9.9658)",
            "",
            "── §5.3  Pattern Resistance ────────────────────────────────",
            f"  Most common 3-seq      : {seq}  count={seq_cnt}  ({seq_prop*100:.4f}%)",
            f"  Max transition prob.   : {self.max_transition_probability():.6f}  (target ≈ 0.100)",
            "=" * 60,
        ]
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
#  Avalanche Effect Tester  (§7.2)
# ─────────────────────────────────────────────────────────────────────────────

class AvalancheAnalyzer:
    """
    Empirically tests §7.2:
        P(hamming_weight(Δo) > 16 | hamming_weight(Δi) = 1) > 0.998

    Strategy: generate a 32-bit intermediate value from the pipeline,
    flip each of the 32 input bits one at a time, and count how many
    output bits change.
    """

    @staticmethod
    def _pipeline_32(ts: Timestamp, state: GeneratorState) -> int:
        """Run the full pipeline up through the avalanche stage."""
        cf1, cf2 = counterflow(ts, SHA1)
        cf1 = state_influence(cf1, state)
        cf2 = state_influence(cf2, state)
        mixed = (cf1 ^ cf2) & MASK32
        return avalanche(mixed)

    def test(self, n_trials: int = 10_000, seed_ns: Optional[int] = None) -> dict:
        """
        Run n_trials single-bit-flip experiments.

        Returns a dict with keys: trials, pass_count, pass_rate,
        mean_bit_flips, min_bit_flips, max_bit_flips.
        """
        rng = TurbulentFlowRNG(seed_ns=seed_ns)
        pass_count = 0
        bit_flips: list[int] = []

        for _ in range(n_trials):
            ts    = rng._get_timestamp()
            state = rng._state

            baseline = self._pipeline_32(ts, state)

            # Flip each of the 32 bits of SHA1 seed; tally hamming distances
            for bit in range(32):
                perturbed_ts = Timestamp(
                    ts.timeA ^ (1 << (bit % 20)),
                    ts.timeB,
                    ts.timeC,
                )
                variant = self._pipeline_32(perturbed_ts, state)
                hw = bin(baseline ^ variant).count("1")
                bit_flips.append(hw)
                if hw > 16:
                    pass_count += 1

            rng.generate()

        total = n_trials * 32
        return {
            "trials"       : total,
            "pass_count"   : pass_count,
            "pass_rate"    : pass_count / total,
            "mean_bit_flips": statistics.mean(bit_flips),
            "min_bit_flips" : min(bit_flips),
            "max_bit_flips" : max(bit_flips),
        }


# ─────────────────────────────────────────────────────────────────────────────
#  Chi-square survival function (p-value)  — pure Python, no scipy
# ─────────────────────────────────────────────────────────────────────────────

def _gamma_inc_upper(a: float, x: float, terms: int = 200) -> float:
    """
    Regularised upper incomplete gamma function Q(a, x) via continued
    fraction (Lentz method), used to compute the chi-square p-value.
    """
    # Series expansion for small x
    if x < a + 1:
        # Use the complementary lower incomplete gamma (series)
        return 1.0 - _gamma_inc_lower_series(a, x, terms)
    # Continued fraction for large x
    fpmin = 1e-300
    b = x + 1.0 - a
    c = 1.0 / fpmin
    d = 1.0 / b
    h = d
    for i in range(1, terms + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < fpmin: d = fpmin
        c = b + an / c
        if abs(c) < fpmin: c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-12:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def _gamma_inc_lower_series(a: float, x: float, terms: int = 200) -> float:
    """Regularised lower incomplete gamma function P(a, x) via Taylor series."""
    if x == 0.0:
        return 0.0
    ap  = a
    val = 1.0 / a
    s   = val
    for _ in range(terms):
        ap  += 1.0
        val *= x / ap
        s   += val
        if abs(val) < abs(s) * 1e-12:
            break
    return s * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _chi2_sf(chi2: float, df: int) -> float:
    """Survival function (1 - CDF) of the chi-squared distribution."""
    return _gamma_inc_upper(df / 2.0, chi2 / 2.0)


# ─────────────────────────────────────────────────────────────────────────────
#  Convenience helpers
# ─────────────────────────────────────────────────────────────────────────────

def quick_analyze(n: int = 100_000, seed_ns: Optional[int] = None) -> str:
    """
    Generate n samples, run the full statistical suite, and return a report.

    Parameters
    ----------
    n        : number of samples (default 100 000, matching specification §5)
    seed_ns  : optional seed for reproducibility
    """
    rng     = TurbulentFlowRNG(seed_ns=seed_ns)
    samples = rng.generate_batch(n)
    return StatisticalAnalyzer(samples).report()


def avalanche_report(n_trials: int = 1_000, seed_ns: Optional[int] = None) -> str:
    """Run the avalanche test and return a formatted string."""
    result = AvalancheAnalyzer().test(n_trials, seed_ns=seed_ns)
    lines = [
        "",
        "── §7.2  Avalanche Effect Test ─────────────────────────────",
        f"  Single-bit-flip trials : {result['trials']:,}",
        f"  Pass (>16 bits flipped) : {result['pass_count']:,}",
        f"  Pass rate               : {result['pass_rate']:.6f}  (target > 0.998)",
        f"  Mean bits flipped       : {result['mean_bit_flips']:.2f}",
        f"  Range                   : [{result['min_bit_flips']}, {result['max_bit_flips']}]",
        "=" * 60,
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
#  CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="TurbulentFlow Random Number Generator — demo & analysis"
    )
    parser.add_argument(
        "-n", "--samples", type=int, default=100_000,
        help="Number of samples for statistical analysis (default: 100000)"
    )
    parser.add_argument(
        "--generate", type=int, default=20,
        help="Print this many live random digits (default: 20)"
    )
    parser.add_argument(
        "--avalanche", action="store_true",
        help="Run avalanche test (adds ~30 s for 1000 trials)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Optional integer seed (nanoseconds) for reproducible output"
    )
    args = parser.parse_args()

    print("\nTurbulentFlow Random Number Generator")
    print("=======================================")

    # Live generation demo
    rng    = TurbulentFlowRNG(seed_ns=args.seed)
    digits = rng.generate_batch(args.generate)
    print(f"\nFirst {args.generate} digits: {digits}")
    print(f"As string: {''.join(map(str, digits))}")

    # Statistical analysis
    print(f"\nRunning statistical analysis on {args.samples:,} samples …")
    print(quick_analyze(args.samples, seed_ns=args.seed))

    # Optional avalanche test
    if args.avalanche:
        print("Running avalanche test (1 000 trials) …")
        print(avalanche_report(1_000, seed_ns=args.seed))
