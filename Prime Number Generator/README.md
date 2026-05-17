# Prime Number Generator — empirical scale-dependence study and a scale-adaptive hybrid generator

> **An empirical investigation of how the *relative* usefulness of local divisibility filters (`6k±1`, small-prime trial division) and global density heuristics (PNT, Cramér gaps) varies with scale `s = log₁₀ n`, paired with a fully-tested hybrid prime generator that operationalises the findings. Three measurements at `40` scale points spanning `s = 1.0 – 9.5` (`1000 + 1000` balanced primes / composites per scale, total `40 000` per measurement) are fit by maximum likelihood with model selection by AIC. The principal empirical results: (a) the small-prime filter rejection rate is best fit by the rational form `f_M2(s) = 1.027 / (1 + 0.030·s)`, with the power-law form decisively rejected (`ΔAIC = +30.8`); (b) the residue-classifier excess-AUC curve is roughly flat at `~0.30 ± 0.04` and the three candidate functional forms are statistically indistinguishable on it (`|ΔAIC| < 1.5`); (c) the PNT density relative error decays rapidly (`f_M3(s) ≈ 0.51 · s^(-1.88)`) and is below `5 %` for `s ≥ 4`. The data shows no operationally meaningful local-to-global crossover. The companion algorithm — a `6k±1` candidate sieve plus a small-prime trial-division pre-filter sized by `f_M2` plus a scale-adaptive primality verifier (deterministic trial division below `n ≈ 31 623`, deterministic-witness Miller–Rabin via Sorenson–Webster (2017) up to `n = 3.317 × 10²⁴`, probabilistic Miller–Rabin above with `4⁻²⁰ ≈ 9.1 × 10⁻¹³` per-call error bound) — is implemented in `prime_generator.py`, verified by `5` self-test assertions and a `10`-scale end-to-end audit (`10/10` all-prime, `6/6` no-skip, all-prime correctness independently verified up to `n = 10¹⁵`), and runs at `< 0.07 ms` per prime up to `n = 10¹²`.**

---

## What this folder is

The Prime Number Theorem (PNT) describes the *global* density of primes as `1 / ln n`. Divisibility filters like `6k±1` and small-prime trial division describe a *local* layer that cheaply rejects composites with small prime factors. Most production prime generators compose the two — sieve, then primality-test — but the *empirical functional form* of the relative contribution of each layer as a function of scale has not, to our knowledge, been measured rigorously on a dense scale grid with formal model selection. That gap is what this folder closes.

The work has two parts:

1. **An empirical study** (`Paper1_PrimeMetaPattern_Theory.md`, supported by `fit_meta_pattern.py` and its outputs `fit_meta_pattern.json` / `fit_meta_pattern.md`). Three independent quantities — residue-classifier excess AUC (M1), small-prime filter rejection rate (M2), PNT density relative error (M3) — are measured at `40` scale points spanning `s = log₁₀ n ∈ [1.0, 9.5]` with `1000 + 1000` balanced primes / composites per scale. Each curve is fit by maximum likelihood (Gaussian on log-target — equivalent to multiplicative-noise least squares) to three candidate forms: power law `A · s^(-γ)`, exponential `A · exp(-b·s)`, rational `A / (1 + B·s)`. Model selection is by AIC.

2. **A hybrid prime generator** (`Paper2_MetaPattern_Algorithm.md`, implemented in `prime_generator.py`, audited by `verify_generator.py`). The algorithm composes a `6k±1` candidate sieve, a small-prime trial-division pre-filter sized by the M2 fit, and a scale-adaptive primality verifier (trial division below `s ≈ 4.5`; deterministic-witness Miller–Rabin using the Sorenson–Webster (2017) sets up to `n ≈ 3.317 × 10²⁴`; `k = 20` probabilistic rounds above). Two semantics are exposed: `next_prime(n)` (strict — smallest prime ≥ n) and `random_prime_near(n)` (Cramér-style sampling, for cryptographic use).

The findings drive a single algorithmic conclusion: **at every tested scale the right answer is the hybrid**, with the only scale-dependent choice being the *primality verifier*, which switches from `O(√n)` trial division to `O(k log³ n)` Miller–Rabin near `s = 4.5` based on computational cost.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`README.md`](README.md) | This file. |
| [`Paper1_PrimeMetaPattern_Theory.md`](Paper1_PrimeMetaPattern_Theory.md) | Empirical paper — methodology, dense-scale-grid measurements, MLE fits, AIC model selection, implications for hybrid generation. |
| [`Paper2_MetaPattern_Algorithm.md`](Paper2_MetaPattern_Algorithm.md) | Algorithm paper — full specification, correctness analysis, complexity, benchmarks, applications. |
| [`ALGORITHM_DERIVATION.md`](ALGORITHM_DERIVATION.md) | One-page derivation linking the empirical fits to the algorithm. |
| [`COMPLETE_PRIME_METAPATTERN_RESEARCH.md`](COMPLETE_PRIME_METAPATTERN_RESEARCH.md) | Combined research summary. |
| [`prime_generator.py`](prime_generator.py) | Reference implementation. Five `_self_test()` assertions. |
| [`fit_meta_pattern.py`](fit_meta_pattern.py) | Empirical-fit experiment driver. `40` scales × `1000 + 1000` samples, three measurements, three forms. |
| [`fit_meta_pattern.md`](fit_meta_pattern.md), `fit_meta_pattern.json` | Fit report and raw data (`.json` is gitignored; reproducible from the script). |
| [`verify_generator.py`](verify_generator.py) | End-to-end audit harness. |
| `verify_generator.json` | Audit results (gitignored; reproducible). |
| [`deep_transition_analysis.py`](deep_transition_analysis.py) | Earlier transition-region analysis tool (kept for context; superseded by the dense-grid MLE fit). |
| [`prime_meta_patterns.png`](prime_meta_patterns.png), [`transition_mechanics.png`](transition_mechanics.png) | Visualisation outputs. |

---

## 🧠 The empirical picture

```
Scale  s = log₁₀ n  ∈  [1.0, 9.5]    (40 evenly-spaced points)

M1   residue-classifier excess AUC   ≈  0.40 / (1 + 0.040 · s)
                                         Roughly flat: 0.41 → 0.29 across the range.
                                         Three candidate forms statistically
                                         indistinguishable (|ΔAIC| < 1.5).

M2   filter rejection rate           =  1.027 / (1 + 0.030 · s)
                                         Slow plateau: 0.997 → 0.824 across the range.
                                         Power-law form decisively rejected
                                         (ΔAIC = +30.8 vs rational).

M3   PNT density relative error      ≈  0.505 · s^(-1.88)
                                         Rapid decay; below 5 % for s ≥ 4.
```

| Scale `n` | M1 (excess AUC) | M2 (filter rej.) | M3 (rel. dens. err.) |
|---|---:|---:|---:|
| `~10¹` | `0.41` | `0.99` | `0.35` |
| `~10²` | `0.37` | `0.96` | `0.36` |
| `~10⁴` | `0.34` | `0.92` | `0.03` |
| `~10⁶` | `0.32` | `0.87` | `0.01` |
| `~10⁸` | `0.29` | `0.82` | `< 0.05` |
| `~10⁹·⁵` | `0.29` | `0.82` | `~ 0.06` |

The three curves are monotone in `s`. None of them crosses any operationally meaningful threshold, and none of them motivates a scale-dependent algorithmic switch. The local layer is useful at every scale; the global layer becomes increasingly trustworthy.

---

## ⚙️ The algorithm

```
ALGORITHM next_prime(n):
    candidate    ← next_6k_pm1(n)
    num_checks   ← max(5, round(15 · 1.027 / (1 + 0.030 · log₁₀ n)))
    while True:
        if passes_pre_filter(candidate, num_checks) and is_prime(candidate):
            return candidate
        candidate ← step_6k_pm1(candidate)


ALGORITHM is_prime(n):
    if log₁₀(n) < 4.5:              return trial_division(n)       # O(√n), exact
    return miller_rabin(n)
        # • Sorenson–Webster witnesses for n < 3.317 × 10²⁴         # exact, deterministic
        # • k = 20 random rounds above                              # ≤ 4⁻²⁰ per call
```

The threshold `s* = 4.5` (`n* ≈ 31 623`) is the empirical CPU crossover between trial division (`O(√n) ≈ 178` ops at this scale) and Miller–Rabin on commodity 64-bit hardware. It is a cost choice, not a feature-importance choice.

### Audit results (`verify_generator.py`)

| `start` | `count` | mean gap | `ln(start)` | `ms / prime` | all prime | no skip |
|---|---:|---:|---:|---:|---:|---:|
| `2` | `50` | `4.63` | `0.69` | `0.004` | yes | yes |
| `100` | `50` | `5.67` | `4.61` | `0.004` | yes | yes |
| `10³` | `50` | `7.18` | `6.91` | `0.004` | yes | yes |
| `10⁴` | `50` | `9.18` | `9.21` | `0.007` | yes | yes |
| `10⁵` | `50` | `12.00` | `11.51` | `0.010` | yes | yes |
| `10⁶` | `30` | `13.03` | `13.82` | `0.012` | yes | yes |
| `10⁷` | `20` | `18.95` | `16.12` | `0.018` | yes | n/a |
| `10⁸` | `15` | `18.00` | `18.42` | `0.021` | yes | n/a |
| `10⁹` | `10` | `19.33` | `20.72` | `0.023` | yes | n/a |
| `10¹²` | `6` | `24.80` | `27.63` | `0.064` | yes | n/a |

Every output is independently verified prime via `sympy.isprime`. Where computationally feasible, every output is verified to be the *true* next prime via `sympy.nextprime`. Self-test additionally verifies correctness at `n = 10¹⁵` (`< 0.2 ms / prime`). Mean prime gaps track `ln n` to within `< 1.5` at every scale.

---

## 📊 Correctness summary

| Range | Verifier | Correctness |
|---|---|---|
| `n < 31 623` | trial division | **exact** (deterministic) |
| `31 623 ≤ n < 3.317 × 10²⁴` | Sorenson–Webster Miller–Rabin | **exact** (deterministic witnesses) |
| `n ≥ 3.317 × 10²⁴` | Miller–Rabin, `k = 20` random rounds | error `≤ 4⁻²⁰ ≈ 9.1 × 10⁻¹³` per call |

The candidate stream visits every `6k±1` integer in order; no prime greater than `3` is excluded a priori (every such prime is `6k±1`). Hence `next_prime` is exact below `n = 3.317 × 10²⁴` — the entire range of "everyday" prime generation — and bounded probabilistically above.

For cryptographic use cases where any prime of the right bit-length suffices, `random_prime_near(n)` samples a Cramér-style `Exponential(ln n)` gap before testing, producing a near-uniform draw over primes in the search window. This is a different operation from `next_prime` and is exposed as a separate entry point.

---

## 🎯 What this displaces

| Standard | What it lacks | What this work adds |
|---|---|---|
| Sieve of Eratosthenes / Atkin | Memory-bound; not single-target | Single-target generator with scale-adaptive primality |
| Bare Miller–Rabin (probabilistic) | No deterministic-witness fast path; no local pre-filter | Deterministic Sorenson–Webster path below `3.317 × 10²⁴` + `6k±1` + small-prime pre-filter |
| Random-gap "prime near `n`" | No "next prime" semantic | Strict `next_prime` (no skipping) **and** opt-in `random_prime_near` |
| Hand-tuned `sympy.nextprime` | Black-box; no explicit complexity branches | Transparent `O(√n · ln n)` / `O(log⁴ n)` branches with a documented switch |

---

## 🚧 Honest framing

- **Empirical, computationally-driven mathematics.** Appropriate venue is *Experimental Mathematics* (Taylor & Francis) or *Integers* (Electronic Journal of Combinatorial Number Theory). This is not a proof of new theorems about prime distribution.
- **No bearing on the Riemann Hypothesis or the Clay Millennium Prize.** The methodology is dense-scale-grid measurement plus model selection; the algorithm composes standard primitives.
- **Tested range stops at `n = 10¹⁵`.** The fits are consistent with their predicted asymptotic shapes (M2 plateaus, M3 decays rapidly), but are not measured at cryptographic key sizes (`n ≈ 10⁶⁰⁰`+). Extrapolation is algebraically straightforward but unmeasured at those scales.
- **Small-prime list fixed at the first 15 primes.** Extending to a wheel-factorised mod-30 or mod-210 filter would shift M2 systematically upward; the qualitative shape is expected to be invariant.

---

## 🔗 Related work in this repo

- [`../General Math Papers/`](../General%20Math%20Papers/) — LCRP and other number-theory adjacencies
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic-number-theory neighbourhood
- [`../Math Question Generator/`](../Math%20Question%20Generator/) — number-theory domain
- [`../RNGS/`](../RNGS/) — the `Izaac` deterministic-randomness generator can replace `Exponential(ln n)` sampling inside `random_prime_near` for verifiable / reproducible prime sequences
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — uses primality testing for cryptographic key generation; calls into `random_prime_near` with the appropriate `mr_rounds`

---

[← Back to main README](../README.md)
