# Prime meta-pattern: complete research summary

> A consolidated narrative pulling together the empirical study (`Paper1_PrimeMetaPattern_Theory.md`), the algorithm specification (`Paper2_MetaPattern_Algorithm.md`), the derivation (`ALGORITHM_DERIVATION.md`), and the implementation (`prime_generator.py`, `fit_meta_pattern.py`, `verify_generator.py`) into one document. Read this for an overview; follow the cross-references for full details.

---

## Executive summary

This research investigates how the relative usefulness of *local* prime-generation rules (small-prime divisibility, the `6k±1` filter, sieving) and *global* rules (the Prime Number Theorem density `1/ln n`, Cramér gap heuristics) varies with scale `s = log₁₀ n`. Three independent quantities are measured at `40` scale points spanning `s = 1.0 – 9.5`, with `1000 + 1000` balanced primes / composites per scale, and each is fit by maximum likelihood to three candidate functional forms (power law, exponential, rational), with model selection by Akaike information criterion.

The empirical findings drive an algorithm: a `6k±1` candidate sieve plus a small-prime trial-division pre-filter sized by the measured filter-rejection-rate curve, plus a primality verifier whose only scale-dependent choice is which test to run (trial division below `s ≈ 4.5`, deterministic-witness Miller–Rabin via the Sorenson–Webster (2017) witness sets up to `n = 3.317 × 10²⁴`, probabilistic Miller–Rabin above). The implementation passes `5` self-test assertions and a `10`-scale end-to-end audit; per-prime wall-clock cost is `< 0.07 ms` up to `n = 10¹²`.

---

## 1. The investigation

### 1.1 Why study the scale dependence at all?

Two complementary frameworks have always coexisted in prime number theory:

- **Local / divisibility** — Eratosthenes-style sieving, `6k±1` filtering, small-prime trial division.
- **Global / density** — the PNT (`π(x) ∼ x/ln x`), Cramér's exponential-gap conjecture, random-prime + Miller–Rabin generators.

In production prime generators these are composed: cheap local rules first, expensive global / probabilistic verification second. But the *empirical functional form* of the relative contribution of the two — how much information do the local features actually carry at scale `s = 5`, scale `s = 8`, scale `s = 12`? — has not, to our knowledge, been measured at the level of dense scale grids and rigorous model selection. This study fills that gap.

### 1.2 Three measurements

```
M1  residue-classifier excess AUC
    Held-out AUC − 0.5 of a logistic regression on residue features
    {n mod 2, mod 3, …, mod 47} plus a 6k±1 indicator, trained at each
    scale on a balanced prime/composite sample.

M2  small-prime filter rejection rate
    Probability that a random composite at this scale is rejected by
    trial-dividing against the same small-prime list.

M3  PNT density relative error
    | observed_density − 1/ln(n_centre) | / (1/ln(n_centre)) on a
    uniform sample inside a window centred at 10**s.
```

### 1.3 Functional-form competition

Each of the three measurements is fit to:

```
Power law:     f(s) = A · s^(-γ)
Exponential:   f(s) = A · exp(-b · s)
Rational:      f(s) = A / (1 + B · s)
```

with maximum likelihood under a log-target Gaussian error model (the natural choice for strictly-positive quantities with multiplicative noise), and the forms are compared by AIC.

---

## 2. What the data shows

### 2.1 The local filter is useful at every tested scale (M2)

```
M2 best fit:    f_M2(s) = 1.027 / (1 + 0.030 · s)        (rational)

  s = 1   →  0.997    s = 5   →  0.892    s = 9   →  0.834
  s = 3   →  0.942    s = 7   →  0.847    s = 9.5 →  0.829
```

The power-law form is **decisively rejected**: `ΔAIC = +30.8` against the rational. The data shows a slow *plateau*, not a power-law decay. A heuristic explanation: the probability that a random composite has a small prime factor `≤ 47` is bounded below by `1 − ∏_{p ≤ 47}(1 − 1/p) ≈ 0.78`, independently of scale, so M2 must asymptote to a non-zero floor.

### 2.2 Residue features carry roughly comparable information at every scale (M1)

```
M1 best fit:    f_M1(s) ≈ 0.404 / (1 + 0.040 · s)        (rational)

Excess AUC ranges 0.29 – 0.41 across s ∈ [1, 9.5]; the three candidate
forms are statistically indistinguishable on this curve (|ΔAIC| < 1.5).
```

This makes sense because while *individual* residues mod small primes become uninformative as `s → ∞` (Dirichlet's theorem: primes equidistribute across residue classes), the *combination* of residues mod `2, 3, 5, …, 47` continues to encode useful primality information through the inclusion–exclusion structure of the sieve.

### 2.3 PNT becomes accurate above `s ≈ 4` (M3)

```
M3 best fit:    f_M3(s) ≈ 0.505 · s^(-1.88)              (power law)

  s = 1   →  ~50 %    relative error
  s = 4   →   ~4 %    relative error
  s = 6   →   ~2 %    relative error
```

The PNT density approximation `1/ln n` is reliable above `s ≈ 4` and is essentially exact above `s ≈ 6`. This validates Cramér-style random-gap candidate generation at large `s` — but only for "*a* prime near `n`" semantics, not for "the *next* prime ≥ `n`".

### 2.4 No algorithmic crossover

All three curves are monotone in `s` and do not cross any operationally meaningful threshold. There is **no scale-dependent point at which the algorithm should switch generation strategies based on these data**. The hybrid (`6k±1` sieve + small-prime pre-filter + primality verifier) is right at every scale.

---

## 3. The algorithm

### 3.1 Components

```
1.  6k±1 candidate sieve
    Visits every integer m ∈ {6k+1, 6k+5} ≥ n in order.
    Eliminates 2/3 of all integers a priori (those divisible by 2 or 3).

2.  Small-prime trial-division pre-filter
    Trial-divides each candidate by the first `num_checks` primes
    in {2, 3, 5, …, 47}, where
        num_checks = max(5, round(15 · f_M2(log₁₀ n)))
    (i.e., uses more primes at small s, fewer at large s, but always
    at least 5).

3.  Scale-adaptive primality verifier
    s = log₁₀(n)
    if s < 4.5:   trial division  (deterministic, O(√n))
    else:         Miller–Rabin
                    n < 3.317 × 10²⁴  →  Sorenson–Webster witnesses
                                           (deterministic, exact)
                    n ≥ 3.317 × 10²⁴  →  k = 20 random witnesses
                                           (probabilistic, ≤ 4⁻²⁰ per call)
```

The single scale-dependent choice — switching from trial division to Miller–Rabin at `s* = 4.5` — is set by **computational cost** (the empirical CPU crossover, `√n ≈ 178`), not by feature importance.

### 3.2 The deterministic-witness Miller–Rabin fast path

Sorenson and Webster (2017) tabulate witness sets that yield Miller–Rabin output exactly equal to true primality, deterministically, up to specific bounds:

| Largest `n` covered | Witness set |
|---|---|
| `2 047` | `{2}` |
| `1 373 653` | `{2, 3}` |
| `25 326 001` | `{2, 3, 5}` |
| `3 215 031 751` | `{2, 3, 5, 7}` |
| `2 152 302 898 747` | `{2, 3, 5, 7, 11}` |
| `3 474 749 660 383` | `{2, 3, 5, 7, 11, 13}` |
| `341 550 071 728 321` | `{2, 3, 5, 7, 11, 13, 17}` |
| `3 825 123 056 546 413 051` | `{2, 3, 5, 7, 11, 13, 17, 19, 23}` |
| `318 665 857 834 031 151 167 461` | `{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}` |
| `3 317 044 064 679 887 385 961 981` | `{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41}` |

Below the largest tabulated bound (`~ 3.3 × 10²⁴`) the algorithm has **no probabilistic error**. Only above this bound does it fall back to random witnesses — and even there the per-call false-positive bound is `4⁻²⁰ ≈ 9.1 × 10⁻¹³`.

### 3.3 Two semantics

```
next_prime(n)         → smallest prime p ≥ n.   Strict.   No primes skipped.
random_prime_near(n)  → a prime near n.        Cramér gap.   For crypto use.
```

Both go through the same primality verifier; the difference is candidate selection. The strict semantic is the default.

---

## 4. Correctness

| Range | Verifier | Correctness |
|---|---|---|
| `n < 31 623`                        | trial division                  | exact (deterministic) |
| `31 623 ≤ n < 3.317 × 10²⁴`         | Sorenson–Webster Miller–Rabin   | exact (deterministic witnesses) |
| `n ≥ 3.317 × 10²⁴`                  | Miller–Rabin, `k = 20` random   | error `≤ 4⁻²⁰` per call |

The `6k±1` sieve never skips a prime greater than `3` (every such prime is `6k±1`); the pre-filter is exact (it rejects only composites); the verifier is exact below `n = 3.317 × 10²⁴`; therefore `next_prime` is exact in that range. Above the Sorenson–Webster bound, the per-call false-positive probability is `≤ 9.1 × 10⁻¹³`.

A formal no-skipping unit test runs a 20-prime sweep from each of five seeds (`n = 97, 1009, 9999, 100 001, 999 983`), comparing against `sympy.nextprime`. Every output must match.

---

## 5. Performance

```
       label            start  count  ms/prime
        tiny                2     50     0.004
       small              100     50     0.004
   small-mid            1,000     50     0.004
      medium           10,000     50     0.007
   medium-hi          100,000     50     0.010
       large        1,000,000     30     0.012
    large-hi       10,000,000     20     0.018
  very-large      100,000,000     15     0.021
          xl    1,000,000,000     10     0.023
         xxl  1,000,000,000,000      6     0.064
                       10**15      3     0.189
```

Cost grows roughly as `O((log n)^c)` with `c ≈ 1` empirically over the tested range, consistent with the `O(log⁴ n)` asymptotic analysis once one accounts for the constant-fraction cost of the small-prime pre-filter and Python's BigInt machinery.

---

## 6. What this is, and what this is not

**This is.** An empirical, computationally-driven investigation of how local divisibility filters and global PNT heuristics combine across scale, with maximum-likelihood model selection on three independent measurements; an empirically grounded specification for a hybrid prime generator; and a thoroughly verified Python reference implementation with end-to-end timing benchmarks.

**This is not.** A proof of new mathematics about the distribution of primes. The PNT and Cramér model are taken as background; the primality tests used are standard. The contributions are: (a) the dense-scale-grid measurements and rigorous functional-form fitting, which rule out a power-law form for the filter-rejection-rate curve (`ΔAIC ≥ 28` against power law) and show that the local layer remains useful at every tested scale; (b) the algorithm specification and implementation, which combines standard primitives in a way that is operationally simple, exact below `n ≈ 3.3 × 10²⁴`, and well-benchmarked.

Appropriate venues for this work are *Experimental Mathematics* (Taylor & Francis) — explicitly chartered for computationally-driven empirical findings — or *Integers* (Electronic Journal of Combinatorial Number Theory). The work has no bearing on the Riemann Hypothesis or the Clay Millennium Prize.

---

## 7. Reproducibility

```
python fit_meta_pattern.py      # 40 scales × 1000+1000 samples; fits + AIC tables
python prime_generator.py       # self-test (5 assertions, ~ 5 s including 10**15 timing)
python verify_generator.py      # end-to-end audit across 10 scales (~ 1 s)
```

Dependencies: `numpy >= 2`, `scipy >= 1.10`, `scikit-learn >= 1.5`, `sympy >= 1.12`. Total wall time across all three runs is well under a minute on commodity 64-bit hardware. Outputs (`fit_meta_pattern.json`, `verify_generator.json`) are bit-identical from the same RNG seed.

---

## 8. Documents in this folder

| File | Role |
|---|---|
| `README.md` | Overview entry point. |
| `Paper1_PrimeMetaPattern_Theory.md` | Empirical paper — methodology, fits, model selection. |
| `Paper2_MetaPattern_Algorithm.md` | Algorithm paper — specification, correctness, benchmarks. |
| `ALGORITHM_DERIVATION.md` | One-page derivation linking the fits to the algorithm. |
| `COMPLETE_PRIME_METAPATTERN_RESEARCH.md` | This document. |
| `prime_generator.py` | Reference implementation + `_self_test()`. |
| `fit_meta_pattern.py` | Empirical-fit experiment driver. |
| `fit_meta_pattern.md`, `.json` | Fit report and raw data. |
| `verify_generator.py` | End-to-end audit harness. |
| `verify_generator.json` | Audit results. |
| `deep_transition_analysis.py` | Transition-region analysis tool (legacy; superseded by the dense-grid fit). |
| `prime_meta_patterns.png`, `transition_mechanics.png` | Original visualisation outputs. |
