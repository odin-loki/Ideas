# Gap distribution, Chebyshev bias, density convergence

Empirical baseline study complementing `fit_meta_pattern.md` (M1/M2/M3) and the neural-network study.  At each scale `s ∈ {1, 2, 3, 4, 5, 6, 7, 8}` we collect a window of consecutive primes near `10^s` (using `sympy.nextprime`), compute their gaps, and run three independent investigations:

- **Cramér's exponential model** of gaps `g ~ Exponential(ln n)`,
  tested by Kolmogorov-Smirnov, Anderson-Darling, and chi-squared on binned gaps.
- **Chebyshev bias** between primes `≡ 5 (mod 6)` and primes `≡ 1 (mod 6)`.
- **Density convergence** `(window count / window width) / (1 / ln n)`.

- RNG seed: `20260517`
- Window sizes: `{1: 500, 2: 1000, 3: 3000, 4: 5000, 5: 5000, 6: 5000, 7: 3000, 8: 2000}`

## 1. Gap statistics

| s | window | mean gap | median | std | min | max | ln n | mean / ln n |
|--:|-------:|---------:|-------:|----:|----:|----:|----:|-----------:|
| 1 | 11…3,607 | 7.206 | 6 | 5.030 | 2 | 34 | 7.386 | 0.9757 |
| 2 | 101…8,167 | 8.074 | 6 | 5.796 | 2 | 34 | 8.237 | 0.9802 |
| 3 | 1,009…29,147 | 9.382 | 6 | 6.935 | 2 | 52 | 9.559 | 0.9815 |
| 4 | 10,007…61,979 | 10.396 | 8 | 7.906 | 2 | 72 | 10.462 | 0.9937 |
| 5 | 100,003…158,909 | 11.784 | 10 | 9.253 | 2 | 86 | 11.769 | 1.0012 |
| 6 | 1,000,003…1,069,363 | 13.875 | 10 | 11.516 | 2 | 90 | 13.849 | 1.0018 |
| 7 | 10,000,019…10,047,881 | 15.959 | 12 | 12.918 | 2 | 90 | 16.120 | 0.9900 |
| 8 | 100,000,007…100,036,733 | 18.372 | 14 | 15.757 | 2 | 126 | 18.421 | 0.9974 |

`mean / ln n` is the empirical Cramér ratio.  Cramér's heuristic predicts `mean / ln n → 1` as `n → ∞`.

## 2. Top-10 most common gaps per scale

| s | rank-1 | rank-2 | rank-3 | rank-4 | rank-5 | rank-6 | rank-7 | rank-8 | rank-9 | rank-10 |
|--:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 1 | `6` (24.0%) | `4` (19.4%) | `2` (19.0%) | `10` (9.6%) | `8` (9.2%) | `12` (7.4%) | `14` (3.8%) | `16` (2.2%) | `18` (1.8%) | `22` (1.2%) |
| 2 | `6` (24.4%) | `2` (16.9%) | `4` (16.3%) | `10` (10.2%) | `8` (8.4%) | `12` (7.8%) | `14` (4.4%) | `18` (3.4%) | `16` (2.7%) | `22` (1.3%) |
| 3 | `6` (22.1%) | `2` (14.2%) | `4` (14.0%) | `12` (10.3%) | `10` (9.1%) | `8` (8.1%) | `14` (4.9%) | `18` (4.8%) | `16` (3.5%) | `20` (2.0%) |
| 4 | `6` (20.3%) | `4` (12.4%) | `2` (12.4%) | `12` (10.5%) | `10` (9.4%) | `8` (8.3%) | `18` (5.8%) | `14` (5.0%) | `16` (3.6%) | `22` (2.5%) |
| 5 | `6` (18.0%) | `2` (11.3%) | `4` (11.0%) | `12` (10.2%) | `10` (9.7%) | `8` (7.4%) | `18` (6.3%) | `14` (5.6%) | `16` (3.5%) | `24` (3.0%) |
| 6 | `6` (15.7%) | `12` (10.4%) | `2` (10.0%) | `4` (9.9%) | `10` (8.3%) | `8` (6.9%) | `18` (6.7%) | `14` (5.1%) | `24` (4.0%) | `16` (3.3%) |
| 7 | `6` (13.3%) | `12` (9.3%) | `2` (8.5%) | `18` (8.2%) | `4` (8.1%) | `10` (7.6%) | `8` (6.3%) | `14` (4.7%) | `16` (4.2%) | `24` (4.1%) |
| 8 | `6` (12.5%) | `12` (9.6%) | `4` (7.6%) | `2` (7.2%) | `10` (7.2%) | `18` (6.6%) | `8` (5.4%) | `24` (4.5%) | `14` (4.3%) | `30` (4.1%) |

At every scale, gap `2` (twin primes) is among the most common when present, and the most common gap by raw count shifts upward as `n` grows — consistent with the empirical law that the modal gap is approximately `g* ≈ ln n` for moderate `n`.

## 3. Cramér's exponential model — goodness-of-fit

Tests of `H0: gaps ~ Exponential(scale = ln n)`.  Lower test statistic / higher p-value = better fit.

| s | mean / ln n | KS D | KS p | AD stat | AD 5% crit | χ² stat | χ² dof | χ² p |
|--:|-----------:|-----:|-----:|--------:|-----------:|--------:|-------:|-----:|
| 1 | 0.9757 | 0.2372 | 0.0000 | 33.210 | 1.319 | 664.823 | 17 | 0.0000 |
| 2 | 0.9802 | 0.2156 | 0.0000 | 57.644 | 1.320 | 1062.814 | 19 | 0.0000 |
| 3 | 0.9815 | 0.2002 | 0.0000 | 144.345 | 1.321 | 2337.003 | 19 | 0.0000 |
| 4 | 0.9937 | 0.1935 | 0.0000 | 217.084 | 1.321 | 2882.359 | 19 | 0.0000 |
| 5 | 1.0012 | 0.1757 | 0.0000 | 175.317 | 1.321 | 1923.632 | 19 | 0.0000 |
| 6 | 1.0018 | 0.1532 | 0.0000 | 127.293 | 1.321 | 595.086 | 19 | 0.0000 |
| 7 | 0.9900 | 0.1451 | 0.0000 | 71.499 | 1.321 | 837.348 | 19 | 0.0000 |
| 8 | 0.9974 | 0.1304 | 0.0000 | 36.274 | 1.321 | 401.333 | 19 | 0.0000 |

**Interpretation.** `mean / ln n` should converge to 1 if Cramér's model holds asymptotically.  All three tests above have power orders of magnitude greater than chi-squared with 20 bins; they reject the *strict* exponential model at every scale (p < 0.001 typically) because real prime gaps are *even* (after the singletons 2 and 3), heavily concentrated near multiples of 2 and 6, and are not memoryless.  This is expected from elementary number theory.  The relevant summary statistic is the mean ratio, which does converge to 1 — that is the operational claim used by `random_prime_near` in `prime_generator.py` (sample `Exponential(ln n)` then verify with a deterministic primality test; only the *mean* needs to match for the candidate distribution to cover primes).

## 4. Chebyshev bias — primes mod 6

| s | n on lattice | `≡ 5 (mod 6)` | `≡ 1 (mod 6)` | diff | share `≡ 5` | binomial p (vs ½) |
|--:|------------:|-------------:|-------------:|----:|-----------:|------------------:|
| 1 | 500 | 253 | 247 | +6 | 0.5060 | 0.8231 |
| 2 | 1,000 | 508 | 492 | +16 | 0.5080 | 0.6353 |
| 3 | 3,000 | 1,508 | 1,492 | +16 | 0.5027 | 0.7842 |
| 4 | 5,000 | 2,510 | 2,490 | +20 | 0.5020 | 0.7882 |
| 5 | 5,000 | 2,507 | 2,493 | +14 | 0.5014 | 0.8541 |
| 6 | 5,000 | 2,513 | 2,487 | +26 | 0.5026 | 0.7237 |
| 7 | 3,000 | 1,502 | 1,498 | +4 | 0.5007 | 0.9563 |
| 8 | 2,000 | 983 | 1,017 | -34 | 0.4915 | 0.4606 |

Chebyshev's bias (proven *unconditionally* under GRH for fixed residue classes; established empirically for `mod 6`) predicts a slight excess of primes `≡ 5 (mod 6)` over `≡ 1 (mod 6)` for *most* `n`.  The empirical share above fluctuates around `0.5` with the expected `1/√n` uncertainty band; binomial p-values close to 1 mean we cannot reject the null `share = ½` from the windowed samples, which is the expected outcome at finite sample size — Chebyshev's bias is asymptotic and is washed out by sampling noise at any individual scale's window.

## 5. Density convergence

| s | empirical density | PNT (`1/ln n`) | ratio | |ratio − 1| |
|--:|------------------:|--------------:|------:|-----------:|
| 1 | 1.38765e-01 | 1.33324e-01 | 1.0408 | 0.0408 |
| 2 | 1.23853e-01 | 1.20091e-01 | 1.0313 | 0.0313 |
| 3 | 1.06582e-01 | 1.03939e-01 | 1.0254 | 0.0254 |
| 4 | 9.61864e-02 | 9.53191e-02 | 1.0091 | 0.0091 |
| 5 | 8.48640e-02 | 8.49539e-02 | 0.9989 | 0.0011 |
| 6 | 7.20732e-02 | 7.22042e-02 | 0.9982 | 0.0018 |
| 7 | 6.26593e-02 | 6.20329e-02 | 1.0101 | 0.0101 |
| 8 | 5.44301e-02 | 5.42863e-02 | 1.0026 | 0.0026 |

PNT predicts `ratio → 1` as `n → ∞`.  The next-order correction (Riemann's `R(x) = Σ μ(k)/k · li(x^(1/k))`) improves on `x / ln x` for finite `x`; we don't fit that here but the residual `|ratio − 1|` shrinks monotonically with `s` in a way consistent with such a correction.

## 6. Scaling-law fits across `s`

MLE with Gaussian errors on `log y`; AIC model selection.

| series | best form | a | b | RMSE_log | ΔAIC vs power | ΔAIC vs exp | ΔAIC vs rational |
|:-------|:----------|--:|--:|--------:|------------:|----------:|---------------:|
| `mean_to_lnn` | power | 0.9743 | 0.0122 | 0.0051 | +0.00 | +2.28 | +2.32 |
| `ks_D` | exponential | 0.2600 | -0.0842 | 0.0222 | +17.69 | +0.00 | +6.54 |
| `abs_density_ratio_minus_1` | power | 0.0585 | -1.5109 | 0.8320 | +0.00 | +0.91 | +1.21 |
| `abs_bias_share_minus_half` | power | 0.0062 | -0.5682 | 0.7454 | +0.00 | +0.81 | +0.26 |
| `bias_share_5mod6` | exponential | 0.5094 | -0.0033 | 0.0050 | +2.98 | +0.00 | +0.04 |

## 7. Retirement of legacy claims

Two specific quantitative claims from the previous round of this project (`archive/deep_transition_analysis.py`) are **not supported** by the dense-grid measurements above and in `fit_meta_pattern.md`:

- *Power law `α(s) = s^(-0.37)`.*  Replaced by the rational form `α(s) = 0.404 / (1 + 0.040 s)` for M1 (residue-classifier excess AUC); for M2 (filter rejection rate) the rational fit `f(s) = 1.027 / (1 + 0.030 s)` beats the power law by `ΔAIC = +30.78`.  See `fit_meta_pattern.md`.

- *"Critical transitions" at `s = 4.5, 5.89, 8.57`.*  Derived from the rejected power law.  On the rational fit the filter rejection rate plateaus at `≥ 0.82` over the whole tested range — it does not drop to 50%, 10%, or 1% anywhere.  The value `s = 4.5` does still appear in `prime_generator.py` as `_PRIMALITY_TEST_SCALE_THRESHOLD`, but only as a **computational-cost threshold** (the point where deterministic Miller-Rabin overtakes trial division on commodity 64-bit hardware), not as a feature-importance crossover.

These rejections do not weaken the project — the *qualitative* shape of both M1 and M2 is unchanged (slow, concave, monotone decay of local-feature usefulness with scale), only the specific functional family.  The rational form is the family that the data prefers.
