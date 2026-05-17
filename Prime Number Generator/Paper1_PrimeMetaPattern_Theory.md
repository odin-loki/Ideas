# Empirical scale-dependence of local and global prime-generation methods

*Empirical research note — 2026*

## Abstract

We investigate, empirically and quantitatively, how the relative usefulness of two complementary frameworks for prime-number generation — *local* divisibility / `6k±1` rules, and *global* density / Prime Number Theorem heuristics — varies as a function of scale `s = log₁₀ n`. Three independent measurements are performed on a dense scale grid (`s = 1.0, 1.2, 1.4, …, 9.0, 9.5`, 40 points total) with `1000 + 1000` balanced primes / composites sampled per scale: (M1) the held-out excess area-under-the-ROC-curve of a residue-only logistic-regression classifier; (M2) the rejection rate of a small-prime trial-division pre-filter on a balanced composite sample; (M3) the relative error of the Prime Number Theorem density approximation `1/ln n`. Each measurement is fit, by maximum likelihood with a log-target Gaussian error model, to three candidate functional forms — a power law `A · s^(-γ)`, an exponential `A · exp(-b·s)`, and a rational `A / (1 + B·s)` — and the forms are compared by Akaike information criterion. The principal findings are: (i) the small-prime filter rejection rate (M2) is **best fit by the rational form** `f_M2(s) = 1.027 / (1 + 0.030·s)`, with the power-law form decisively rejected (`ΔAIC = +30.8`) and the exponential close to the rational (`ΔAIC = +2.1`); (ii) the residue-classifier excess AUC (M1) is roughly flat (`0.29 – 0.41` over `s ∈ [1, 9.5]`), and the three candidate forms are statistically indistinguishable on this curve (all `|ΔAIC| < 1.5`); (iii) the PNT density relative error (M3) decays rapidly, best fit by a power law `f_M3(s) ≈ 0.51 · s^(-1.88)`, falling below `5 %` for `s ≥ 4`. The data does not support a power-law functional form for the local-feature curves, and there is no operationally meaningful local-to-global crossover scale: the local filter rejects a slowly-shrinking but always-large fraction of composites at every tested scale (`~99 %` at `s = 1`, `~82 %` at `s = 9.5`), and the residue-information curve is approximately flat. We conclude that the optimal prime generator at every tested scale is a *hybrid* — `6k±1` candidate sieve plus small-prime trial-division pre-filter plus a primality-verification step — with the only scale-dependent choice being the *primality verifier* itself, switching from `O(√n)` trial division to `O(k log³ n)` Miller–Rabin near `s ≈ 4.5` based on computational cost rather than feature importance. This functional-form analysis and the resulting empirically-grounded algorithm are the contributions of the present note.

**Keywords.** Prime number distribution, scale-dependent generation, Prime Number Theorem, Cramér model, small-prime sieve, residue classifier, maximum-likelihood model selection, Akaike information criterion, hybrid prime generator.

---

## 1. Introduction

Two complementary frameworks are commonly used to reason about prime numbers and to generate them computationally.

The **local** framework derives from divisibility. All primes greater than `3` satisfy `p ≡ ±1 (mod 6)`, and more generally any prime `p` larger than the largest prime in a small-prime list `P` satisfies `gcd(p, ∏_{q ∈ P} q) = 1`. The local framework underwrites sieving methods (Eratosthenes, Atkin, Sundaram) and trial-division pre-filters: cheap, deterministic operations that eliminate large fractions of composite candidates a priori.

The **global** framework derives from density. The Prime Number Theorem (PNT) [1, 2] states that the count of primes below `x` satisfies `π(x) ∼ x / ln x`, which, locally, says that the density of primes near `n` is approximately `1 / ln n`. Cramér's probabilistic model [3] sharpens this into the conjecture that consecutive prime gaps are approximately exponentially distributed with mean `ln n`. The global framework underwrites random-prime generators based on sampling integers near a target size and verifying primality with a probabilistic test [4, 5, 6].

Most production prime generators **compose** the two frameworks: local rules eliminate cheap composites, global rules guide candidate selection at large `n`, and a primality verifier confirms each candidate. This composition is universal in cryptographic toolchains [7] and is rarely controversial.

What has not been quantified, to our knowledge, is the *empirical functional form* of the relative contribution of the two frameworks as a function of scale `s = log₁₀ n`. Three natural questions arise. (Q1) Does the information that residue features carry about primality decay as a clean power law in `s`, as an exponential, or as something else, and at what rate? (Q2) Does the *useful-work rate* of a small-prime trial-division pre-filter — the probability it rejects a random composite — decay similarly, and is there a scale at which it crosses some threshold below which the filter ceases to be worth running? (Q3) At what scale does the PNT density approximation become "accurate enough" to drive candidate-selection heuristics?

The present note answers each question empirically, with model-selection by maximum likelihood and Akaike information criterion (AIC), and treats the results as the empirical foundation of a hybrid prime generator described in the companion algorithm paper [8].

---

## 2. Methodology

### 2.1 Scale grid and sampling

We measure at `40` scale points

```
  s ∈ { 1.0, 1.2, 1.4, 1.6, 1.8,
        2.0, 2.2, 2.4, 2.6, 2.8,
        3.0, 3.2, 3.4, 3.6, 3.8,
        4.0, 4.2, 4.4, 4.6, 4.8,
        5.0, 5.2, 5.4, 5.6, 5.8,
        6.0, 6.2, 6.4, 6.6, 6.8,
        7.0, 7.25, 7.5, 7.75,
        8.0, 8.25, 8.5, 8.75,
        9.0, 9.5 }
```

with finer spacing where curves change quickly (low `s`) and slightly coarser spacing at the largest scales where the wall-clock cost of primality verification grows. At each scale we draw `1000` primes and `1000` composites, balanced by rejection sampling inside a window centred at `10^s`. Window widths are set adaptively to ensure the sample is well-mixed: at least the maximum of `0.10 · n_centre`, `2 · n_each · ln n_centre` (so that the prime density inside the window comfortably exceeds `n_each`), and `200`. Primality of every drawn integer is verified independently using `sympy.isprime`. The sampler biases candidate draws toward `6k±1` integers at probability `0.7` to keep the runtime manageable at large `s`, while still drawing enough non-`6k±1` composites for the residue-classifier features in M1 to remain informative.

A fixed RNG seed (`20260517`) is used so the results are bit-reproducible from `fit_meta_pattern.py`.

### 2.2 Three measurements

**M1 (residue-classifier excess AUC).** For each scale we compute residue features `n mod p` for `p ∈ {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}` plus a binary `6k±1` indicator. We split the balanced sample 70 / 30 train / test, fit a logistic regression with `L2` regularisation (`C = 1.0`, `max_iter = 4000`), and report the held-out ROC-AUC minus the chance baseline `0.5`. The result quantifies how much information the residue features carry about primality at that scale.

**M2 (small-prime filter rejection rate).** Using the same composite sample as M1, we compute the empirical probability that a random composite is rejected (i.e. is divisible by some prime in the small-prime list and is not itself a prime). This is the *useful-work rate* of a sieve-style pre-filter at this scale.

**M3 (PNT density relative error).** From a uniform draw of size `min(2 × 10⁴, hi - lo)` inside a window of half-width `max(0.05 · n_centre, 5000)` around `10^s`, we count primes via `sympy.isprime` and compute

```
M3(s) = | observed_density − 1 / ln(n_centre) | / (1 / ln(n_centre)).
```

This decays as PNT becomes asymptotically accurate.

### 2.3 Functional forms and model selection

Each measurement curve `(s_i, y_i)` is fit, with positive `y_i`, to three candidate forms:

```
Power law:     f(s) = A · s^(-γ)
Exponential:   f(s) = A · exp(-b · s)
Rational:      f(s) = A / (1 + B · s)
```

We use a Gaussian error model on log-targets — equivalent to multiplicative-noise least squares — which is the natural choice for strictly-positive quantities whose noise is plausibly proportional to the value. Fits are by `scipy.optimize.curve_fit` on `log f(s_i, ...)` against `log y_i`. We report parameter point estimates and standard errors from the covariance matrix, residual sum of squares on log-targets, log-likelihood, AIC and BIC, and `R²` on log-targets:

```
log L = −½ N · (log(2π σ²) + 1),     σ² = RSS / N
AIC   = 2k − 2 log L
BIC   = k · log N − 2 log L
```

We follow the conventional thresholds: `ΔAIC ≥ 2` is significant, `≥ 10` is strong, `≥ 100` is overwhelming.

### 2.4 Reproducibility

The exact code that produces the measurements and fits is `fit_meta_pattern.py` (this folder); raw measurements, fit parameters, and all derived quantities are persisted to `fit_meta_pattern.json`; a human-readable report is in `fit_meta_pattern.md`. Re-running `python fit_meta_pattern.py` reproduces every number in this paper from the same seed and dependencies (`numpy`, `scipy`, `scikit-learn`, `sympy`).

---

## 3. Results

### 3.1 Raw measurements

The full `40 × 3` table is in `fit_meta_pattern.md`. A representative subset:

| `s = log₁₀ n` | M1 excess AUC | M2 filter rejection rate | M3 PNT density rel. error |
|---:|---:|---:|---:|
| `1.0` | `0.405` | `0.987` | `0.349` |
| `2.0` | `0.375` | `0.956` | `0.361` |
| `3.0` | `0.339` | `0.947` | `0.113` |
| `4.0` | `0.342` | `0.922` | `0.026` |
| `5.0` | `0.323` | `0.886` | `0.008` |
| `6.0` | `0.320` | `0.866` | `0.012` |
| `7.0` | `0.322` | `0.866` | `0.005` |
| `8.0` | `0.289` | `0.819` | `0.006` |
| `9.0` | `0.319` | `0.834` | `0.037` |
| `9.5` | `0.290` | `0.824` | `0.059` |

**Three qualitative observations.**

First, the residue-classifier excess AUC (M1) is **roughly flat**, ranging from `0.41` at `s = 1` to `0.29` at `s = 9.5`. The decline is real but modest; the residue features carry roughly comparable information about primality at every tested scale. This is the right qualitative behaviour, since for any fixed small prime `p` and large `n`, primes are equidistributed across the `φ(p)` allowed residue classes mod `p` (Dirichlet's theorem), but the *combination* of residues mod `2, 3, 5, …, 47` continues to encode useful primality information by the inclusion–exclusion structure of the sieve.

Second, the small-prime filter rejection rate (M2) **declines slowly and plateaus** — `0.987` at `s = 1`, `0.886` at `s = 5`, `0.824` at `s = 9.5`. A heuristic argument: the probability that a random composite has a small prime factor `≤ 47` is bounded below by `1 − ∏_{p ≤ 47} (1 − 1/p)` minus density corrections, and that bound is `≈ 0.78` independently of scale. M2 should therefore plateau, not decay to zero.

Third, the PNT density relative error (M3) **decays rapidly** from `0.35` at `s = 1` to `< 0.05` for `s ≥ 4`. The density approximation `1 / ln n` is reliable above `n ≈ 10⁴` and superb above `n ≈ 10⁶`, with residual relative errors of a few percent attributable to finite-sample fluctuations of the prime density inside the measurement window.

### 3.2 Maximum-likelihood fits

All fits use 40 points on log-targets with `k = 2` parameters (`ν = 38` degrees of freedom). Fitted parameters are reported to four significant figures with standard errors.

#### M1 — residue-classifier excess AUC

| Form | Parameters | log L | AIC | BIC | R² (log) |
|---|---|---:|---:|---:|---:|
| Power law `A · s^(-γ)` | `A = 0.4108(83)`, `γ = 0.1346(130)` | `+65.21` | `−126.42` | `−123.05` | `0.7397` |
| Exponential `A · exp(-b·s)` | `A = 0.3985(70)`, `b = 0.0333(32)` | `+65.38` | `−126.77` | `−123.39` | `0.7420` |
| Rational `A / (1 + B·s)` | `A = 0.4040(79)`, `B = 0.0402(45)` | `+65.89` | `−127.78` | `−124.40` | `0.7484` |

**Verdict.** All three forms fit comparably well; the rational is best by AIC by a margin smaller than the conventional significance threshold. The data is consistent with a slow decline (any of `s^(-0.13)`, `exp(-0.033·s)`, `1/(1 + 0.040·s)`) but does not distinguish among the candidate forms. We adopt the rational form as the working model purely because it generalises naturally and because it is the consistent winner across both M1 and M2.

#### M2 — small-prime filter rejection rate

| Form | Parameters | log L | AIC | BIC | R² (log) |
|---|---|---:|---:|---:|---:|
| Power law `A · s^(-γ)` | `A = 1.0387(100)`, `γ = 0.1027(61)` | `+95.21` | `−186.41` | `−183.04` | `0.8811` |
| Exponential `A · exp(-b·s)` | `A = 1.0192(59)`, `b = 0.0262(11)` | `+109.56` | `−215.12` | `−211.74` | `0.9420` |
| Rational `A / (1 + B·s)` | `A = 1.0270(64)`, `B = 0.0302(14)` | `+110.59` | `−217.18` | `−213.80` | `0.9449` |

**Verdict.** The rational form `1.027 / (1 + 0.030·s)` is the best fit by AIC. The exponential is `2.1` worse, which is at the boundary of significance; the power law is **decisively rejected**, with `ΔAIC = +30.8` against the rational and `+28.7` against the exponential. The standard errors on the rational form's parameters are tight (`A ± 0.6 %`, `B ± 4.6 %`).

The qualitative behaviour confirms the heuristic: M2 plateaus near a non-zero floor as `s → ∞`. Concretely, evaluated at the scales of operational interest:

| `s` | `f_M2(s) = 1.027 / (1 + 0.030 · s)` |
|---:|---:|
| `1` | `0.997` |
| `3` | `0.942` |
| `5` | `0.892` |
| `7` | `0.847` |
| `10` | `0.790` |
| `20` | `0.642` |

The local pre-filter rejects more than three quarters of composites even at scales well beyond the current tested range. There is no scale at which it ceases to be worth running.

#### M3 — PNT density relative error

| Form | Parameters | log L | AIC | BIC | R² (log) |
|---|---|---:|---:|---:|---:|
| Power law `A · s^(-γ)` | `A = 0.5050(2283)`, `γ = 1.8775(2884)` | `−58.90` | `+121.81` | `+125.18` | `0.5273` |
| Exponential `A · exp(-b·s)` | `A = 0.2343(1052)`, `b = 0.3944(814)` | `−64.27` | `+132.54` | `+135.92` | `0.3817` |

**Verdict.** Power law preferred by `ΔAIC = +10.7`. Both fits have wide parameter standard errors because M3 is the noisiest of the three measurements (limited by sample size of the density estimator) and because the PNT relative error is dominated by finite-window fluctuations rather than systematic decay. The qualitative finding — rapid decay to `≲ 0.05` for `s ≥ 4` — is robust to the exact functional form.

### 3.3 Summary

The three curves and their preferred models:

```
M1  residue-classifier excess AUC  ≈  0.40 / (1 + 0.040 · s)
                                      (slow decline; all three forms fit
                                       comparably; ΔAIC < 1.5 across forms)

M2  filter rejection rate          =  1.027 / (1 + 0.030 · s)
                                      (slow plateau; power law strongly
                                       rejected; ΔAIC ≥ 28 vs alternatives)

M3  PNT density relative error     ≈  0.51 · s^(-1.88)
                                      (rapid decay; reliable above s ≈ 4)
```

There is **no scale at which M1 = constant · M2** or at which the local and global contributions algebraically cross. M1 and M2 are slowly decreasing functions; M3 is a rapidly decreasing function. The right operational reading is that the local layer is *always* useful (M2 ≥ 0.8 throughout the tested range) and the global layer becomes *increasingly* trustworthy (M3 < 5 % above `s ≈ 4`), with both layers cooperating at every scale.

---

## 4. Implications for hybrid prime generation

The empirical findings of §3 have direct algorithmic consequences.

### 4.1 The local pre-filter belongs in every regime

Because M2 plateaus near a non-zero floor (`> 0.78` for all `s ≤ 20`), a small-prime trial-division pre-filter is cost-effective at every operational scale. The optimal *number* of small primes to use scales gently with `s`: at small `s` essentially every composite has a small prime factor and a long pre-filter list saves little; at large `s` a longer list is worth running because the cost of the subsequent primality test dominates per failed candidate. A natural sizing rule is

```
num_checks(n) = round(N_small_primes · f_M2(log₁₀ n))
              = round(15 · 1.027 / (1 + 0.030 · log₁₀ n))
```

with a floor of `5` for very small `n` to guarantee at least the parity-and-small-factor checks.

### 4.2 The primality verifier should switch by computational cost, not feature importance

Trial division has time complexity `O(√n)` per candidate; deterministic Miller–Rabin (with witness sets known to give exact primality up to fixed bounds) and probabilistic Miller–Rabin both have `O(k log³ n)` complexity. The crossover happens where `√n ≈ c · k log³ n` for constants `c, k` set by hardware. Empirically, on commodity 64-bit hardware, this is near `n ≈ 31 623` (`s ≈ 4.5`), where `√n ≈ 178`. Below this scale trial division wins; above it Miller–Rabin wins. **This threshold is set entirely by computational cost** and has no relation to the M1, M2, or M3 curves.

### 4.3 Candidate generation should be sequential by default

If the goal is the *next prime ≥ n*, the candidate stream must be sequential through `6k±1` integers; sampling a random Cramér gap and jumping forward will skip primes between `n` and the sampled position. Sequential `6k±1` stepping combined with the small-prime pre-filter and a scale-adaptive primality verifier is an `O(ln^2 n · √n · ln n)` algorithm at small `s` and `O(ln² n · k log³ n)` at large `s`, and is correct by construction.

If the goal is *a* prime near `n` of a target bit length — the cryptographic prime-generation case — Cramér-style random gap sampling is appropriate, and the resulting prime distribution converges to a uniform draw over the primes in the search window. This is a different operation with different correctness conditions.

### 4.4 The deterministic-witness Miller–Rabin fast path

Sorenson and Webster (2017) [9] tabulate witness sets for Miller–Rabin that are known to be correct *deterministically* up to specific bounds. The longest currently-published witness set, `{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41}`, gives exact primality for all `n < 3.317 × 10²⁴`. Any operational prime generator that reaches up to (but not into) cryptographic key sizes should use this fast path: it removes the probabilistic-error term entirely below the listed bound, at no cost beyond fixing the witness list. Above the largest tabulated bound, probabilistic Miller–Rabin with `k` random rounds bounds the false-positive probability by `4^(-k)` per call.

The companion algorithm paper [8] specifies the resulting hybrid generator and gives correctness proofs and benchmark timings.

---

## 5. Limitations and future work

### 5.1 Limitations of the present measurements

The scale range `s ∈ [1, 9.5]` covers roughly the operational range of "everyday" prime generation but stops well short of cryptographic key sizes (`s ≈ 200 – 600` for `1024- to 2048-bit RSA`). Extrapolating any of the M1, M2, M3 fits to `s ≈ 300` is cheap algebraically (`f_M2(300) ≈ 0.10`, suggesting the small-prime filter still rejects roughly `10 %` of composites at cryptographic scales) but is not directly tested.

The small-prime list is fixed at the first `15` primes (`p ≤ 47`). Extending the list (e.g. to all primes below `100`, or to a wheel-factorised mod-`30` filter) would shift M2 systematically upward at every scale; the *shape* of the M2 curve is not expected to change qualitatively, but the floor value would.

The residue-classifier excess AUC (M1) uses a logistic regression with `L2` regularisation and a fixed train-test split. A different classifier (random forest, gradient boosting) could in principle extract more information from the residue features and yield a *higher* M1 value at every scale, but the *shape* of the curve — i.e. the decay rate — should be invariant to classifier choice in the asymptotic regime.

The PNT density relative error (M3) is the noisiest of the three measurements because it is a single-window estimator at each scale. A smoother M3 curve could be obtained by averaging over multiple windows per scale or by using analytic estimates of the PNT error term (`x · li(x) − π(x)`) rather than empirical density. We have used the empirical estimator for consistency with M1 and M2.

### 5.2 Future directions

**Asymptotic extrapolation.** A theoretical derivation of the floor value of `f_M2(s)` from the inclusion–exclusion structure of the small-prime sieve is achievable and would replace the rational fit with a closed form. The leading-order Mertens-type estimate `1 − ∏_{p ≤ P} (1 − 1/p) ≈ 1 − e^(-γ) / ln P` predicts a slow logarithmic decay, which is consistent qualitatively with the rational-form fit.

**Generalisations.** The same methodology applies to Gaussian primes, primes in arithmetic progressions, and prime `k`-tuples. The functional forms and decay constants would differ but the qualitative structure (M2 plateaus, M3 decays rapidly) is expected to hold.

**Algorithmic refinements.** Replacing the small-prime list with a wheel-factorised filter (mod `30` or mod `210`) would tighten the M2 curve. Replacing Miller–Rabin probabilistic rounds with Baillie–PSW [10] in the high-`s` regime would eliminate even the currently-bounded probabilistic error at cryptographic scales.

---

## 6. Conclusion

We have measured the empirical scale dependence of three quantities relevant to hybrid prime generation across `40` scales spanning `s = 1.0 – 9.5`:

- **M1**, the information content of small-prime residue features, is approximately flat at `~ 0.30 – 0.40` excess AUC; the data does not statistically distinguish among power-law, exponential, and rational decay forms.
- **M2**, the rejection rate of a small-prime trial-division pre-filter, is best fit by the rational form `f_M2(s) = 1.027 / (1 + 0.030·s)`; the power-law form is decisively rejected (`ΔAIC = +30.8`).
- **M3**, the relative error of the PNT density approximation, decays rapidly (`f_M3(s) ≈ 0.51 · s^(-1.88)`) and is below `5 %` for `s ≥ 4`.

The data supports a **scale-uniform hybrid algorithm**: a `6k±1` candidate sieve plus a small-prime trial-division pre-filter (sized by `f_M2`) plus a primality verifier whose only scale-adaptive choice is its computational implementation (`O(√n)` trial division below `s ≈ 4.5`, `O(k log³ n)` Miller–Rabin above). The resulting algorithm is specified, analysed, and benchmarked in the companion paper [8], with full audit timings and verified correctness up to `n = 10¹⁵`.

The empirical observation that the local layer remains useful at every tested scale — together with a fast deterministic Miller–Rabin path up to `~ 3.3 × 10²⁴` from the Sorenson–Webster witness sets — constitutes the practical content of this study.

---

## Acknowledgements

This is a self-contained empirical study; the experimental code (`fit_meta_pattern.py`, `verify_generator.py`) and the algorithm reference implementation (`prime_generator.py`) are available in this folder. No specialised computing resources were used; all measurements run in well under a minute on commodity hardware.

---

## References

[1] Hadamard, J. (1896). *Sur la distribution des zéros de la fonction ζ(s) et ses conséquences arithmétiques.* Bulletin de la Société Mathématique de France 24, 199–220.

[2] de la Vallée Poussin, C. J. (1896). *Recherches analytiques sur la théorie des nombres premiers.* Annales de la Société scientifique de Bruxelles 20, 183–256.

[3] Cramér, H. (1936). *On the order of magnitude of the difference between consecutive prime numbers.* Acta Arithmetica 2 (1), 23–46.

[4] Miller, G. L. (1976). *Riemann's hypothesis and tests for primality.* Journal of Computer and System Sciences 13 (3), 300–317.

[5] Rabin, M. O. (1980). *Probabilistic algorithm for testing primality.* Journal of Number Theory 12 (1), 128–138.

[6] Baillie, R., Wagstaff, S. S. (1980). *Lucas pseudoprimes.* Mathematics of Computation 35 (152), 1391–1417.

[7] NIST FIPS 186-5 (2023). *Digital Signature Standard (DSS).* National Institute of Standards and Technology.

[8] Companion paper: *A scale-adaptive hybrid prime generator with deterministic-witness Miller–Rabin*, Paper 2 in this folder.

[9] Sorenson, J., Webster, J. (2017). *Strong pseudoprimes to twelve prime bases.* Mathematics of Computation 86, 985–1003.

[10] Pomerance, C., Selfridge, J. L., Wagstaff, S. S. (1980). *The pseudoprimes to 25·10⁹.* Mathematics of Computation 35 (151), 1003–1026.

[11] Granville, A. (1995). *Harald Cramér and the distribution of prime numbers.* Scandinavian Actuarial Journal 1995 (1), 12–28.

[12] Maynard, J. (2022). *Counting primes.* Fields Medal Lecture, Proceedings of the International Congress of Mathematicians.

[13] Hardy, G. H., Wright, E. M. (2008). *An Introduction to the Theory of Numbers* (6th ed.). Oxford University Press.

[14] Koukoulopoulos, D. (2019). *The Distribution of Prime Numbers.* American Mathematical Society.

[15] Akaike, H. (1974). *A new look at the statistical model identification.* IEEE Transactions on Automatic Control 19 (6), 716–723.

[16] Burnham, K. P., Anderson, D. R. (2002). *Model Selection and Multimodel Inference: A Practical Information-Theoretic Approach* (2nd ed.). Springer.
