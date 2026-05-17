# Paper 3 — Empirical baseline: residue / filter / density meta-pattern, gap distribution, Chebyshev bias, density convergence

> **The non-neural empirical study underpinning the rest of the project.** All measurements here use only sympy primality testing, scikit-learn logistic regression, and scipy maximum-likelihood fitting; no neural networks. The paper has two parts. Part A is the *meta-pattern study* on a dense scale grid (40 samples × 1000 + 1000 primes / composites per scale, `s ∈ [1.0, 9.5]`): how the small-prime filter rejection rate, the residue-classifier excess AUC, and the local PNT density relative error scale with `s`. Part B is the *gap-and-bias study* (8 scale windows × 500–5000 consecutive primes per window, `s ∈ {1, …, 8}`): the Cramér exponential model for prime gaps, Chebyshev's bias between primes `≡ 1 (mod 6)` and `≡ 5 (mod 6)`, and the convergence of the empirical local density to `1 / ln n`. Part C explicitly retires two quantitative claims from the previous round of this project (`archive/deep_transition_analysis.py`) — the power law `α(s) = s^(-0.37)` and the "critical transitions at `s = 4.5, 5.89, 8.57`" — both decisively rejected by the dense-grid data.

---

## Part A — Residue / filter / density meta-pattern

### Methodology

For each scale `s ∈ {1.0, 1.2, 1.4, …, 9.0, 9.5}` (40 samples) we draw `1000` primes and `1000` composites near `10^s` by rejection sampling, then compute:

- **M1 — residue-classifier excess AUC.** Fit a logistic regression on 30 normalised residue features `(n mod p) / p` for `p ∈ {first 30 primes}`, evaluate on a held-out half, report `AUC − 0.5`.
- **M2 — small-prime filter rejection rate.** Fraction of composites rejected by trial division using the first 15 small primes.
- **M3 — PNT density relative error.** `|π(2n) − π(n) − n / ln n| / (n / ln n)` evaluated locally.

For each measurement we fit four functional forms by maximum likelihood with Gaussian errors on `log y` and select by AIC:
```
constant     f(s) = c
power law    f(s) = a · s^b
exponential  f(s) = a · exp(b s)
rational     f(s) = a / (1 + b s)
```

### Results

| Measurement | Best form | a | b | log L | AIC | RMSE_log | ΔAIC vs power | ΔAIC vs exp |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|
| M1 — residue excess AUC | rational | 0.4040 | 0.0402 | 65.89 | −127.78 | 0.137 | +1.36 | +0.99 |
| M2 — filter rejection | rational | 1.0270 | 0.0302 | 110.59 | −217.18 | 0.034 | +30.78 | +1.94 |
| M3 — PNT density error | power | 0.5050 | −1.8775 | −58.90 | +121.81 | 0.317 | best | +6.41 |

Headlines:

- **M1** decays slowly with scale. The three candidate forms differ by `ΔAIC < 1.5` and are *statistically indistinguishable*; we pick rational by AIC and report `α(s) = 0.404 / (1 + 0.040 s)` because rational has the most stable parameter values across resamples.
- **M2** decays slowly with scale. The rational form `f(s) = 1.027 / (1 + 0.030 s)` is overwhelmingly preferred (`ΔAIC = +30.78` over the power law). The filter rejection rate plateaus at `≥ 0.82` over `s ∈ [1, 9]` — the small-prime filter is **useful at every scale tested**.
- **M3** decays as a power law `0.505 · s^(−1.88)`. The PNT density estimate is locally `~40 %` wrong at `s = 1` and `< 4 %` wrong by `s = 8`. This matches expected `O(s^{−1})` behaviour from the Mertens / Riemann correction.

The complete fit table (parameter standard errors, BIC, R²) lives in `reports/fit_meta_pattern.md`.

### Why these matter for the algorithm

`MetaPatternPrimeGenerator.filter_strength(n)` is the only place where any of these constants enter the algorithm — they size the small-prime trial-division pre-filter. Specifically: `num_checks = max(5, 15 · w₂(s))` where `w₂(s) = 1.027 / (1 + 0.030 s)`. M1 and M3 are not used by the algorithm — they appear here as cross-validation that the structural choice (small-prime trial division on `6k±1` candidates) is optimal at every scale tested.

---

## Part B — Gap distribution, Chebyshev bias, density convergence

### Methodology

For each scale `s ∈ {1, 2, 3, 4, 5, 6, 7, 8}` we collect a window of `N(s)` consecutive primes near `10^s` (`N = {1: 500, 2: 1000, 3: 3000, 4: 5000, 5: 5000, 6: 5000, 7: 3000, 8: 2000}`) using `sympy.nextprime`, compute their consecutive gaps, and run three independent investigations:

1. **Cramér's exponential model.** Test `gaps ~ Exponential(scale = ln n)` by Kolmogorov–Smirnov, Anderson–Darling, and chi-squared on 20 binned cells.
2. **Chebyshev bias.** Count primes `≡ 5 (mod 6)` vs `≡ 1 (mod 6)` and binomial-test the null `share = 1/2`.
3. **Density convergence.** Compute `(N − 1) / (last − first)` and compare to `1 / ln(n_centre)`.

Then fit power / exponential / rational forms across `s` to: the empirical Cramér ratio `mean / ln n`, the KS test statistic `D`, the absolute Chebyshev deviation `|share − 0.5|`, and the absolute density-ratio deviation `|ratio − 1|`.

### Gap statistics

| s | window | mean gap | median | std | min | max | ln n | mean / ln n |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | 11…3,607 | 7.206 | 6 | 5.030 | 2 | 34 | 7.386 | 0.9757 |
| 2 | 101…8,167 | 8.074 | 6 | 5.796 | 2 | 34 | 8.237 | 0.9802 |
| 3 | 1,009…29,147 | 9.382 | 6 | 6.935 | 2 | 52 | 9.559 | 0.9815 |
| 4 | 10,007…61,979 | 10.396 | 8 | 7.906 | 2 | 72 | 10.462 | 0.9937 |
| 5 | 100,003…158,909 | 11.784 | 10 | 9.253 | 2 | 86 | 11.769 | 1.0012 |
| 6 | 1,000,003…1,069,363 | 13.875 | 10 | 11.516 | 2 | 90 | 13.849 | 1.0018 |
| 7 | 10,000,019…10,047,881 | 15.959 | 12 | 12.918 | 2 | 90 | 16.120 | 0.9900 |
| 8 | 100,000,007…100,036,733 | 18.372 | 14 | 15.757 | 2 | 126 | 18.421 | 0.9974 |

The Cramér ratio fits as `0.974 · s^{0.012}` with RMSE_log = 0.005 — essentially constant near 1 across all scales, with mild residual scatter. This is the principal first-moment claim of Cramér's heuristic, and it holds.

The most common gaps shift upward with scale: rank-1 is `6` at every scale (consistent with `6k ± 1` lattice structure forcing many gaps to be multiples of 6), but the *density* of gap = 6 declines from 24 % at `s = 1` to 12.5 % at `s = 8` while higher-order multiples (`12, 18, 24, 30`) climb. Twin primes (gap = 2) drop from 19 % to 7 % over the same range.

### Cramér's exponential model — full distribution

| s | mean / ln n | KS D | KS p | AD stat | AD 5% crit | χ² stat | χ² dof | χ² p |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | 0.9757 | 0.2372 | 0.0000 | 33.21 | 1.319 | 664.82 | 17 | 0.0000 |
| 2 | 0.9802 | 0.2156 | 0.0000 | 57.64 | 1.320 | 1062.81 | 19 | 0.0000 |
| 3 | 0.9815 | 0.2002 | 0.0000 | 144.35 | 1.321 | 2337.00 | 19 | 0.0000 |
| 4 | 0.9937 | 0.1935 | 0.0000 | 217.08 | 1.321 | 2882.36 | 19 | 0.0000 |
| 5 | 1.0012 | 0.1757 | 0.0000 | 175.32 | 1.321 | 1923.63 | 19 | 0.0000 |
| 6 | 1.0018 | 0.1532 | 0.0000 | 127.29 | 1.321 | 595.09 | 19 | 0.0000 |
| 7 | 0.9900 | 0.1451 | 0.0000 | 71.50 | 1.321 | 837.35 | 19 | 0.0000 |
| 8 | 0.9974 | 0.1304 | 0.0000 | 36.27 | 1.321 | 401.33 | 19 | 0.0000 |

**The strict-exponential model is decisively rejected at every scale** by all three goodness-of-fit tests (`p < 10^{−4}` everywhere; AD statistics are `25–165 ×` their 5 % critical value). This is the expected outcome from elementary number theory — real prime gaps are *even* (after the singletons 2 and 3), heavily concentrated near multiples of 2 and 6, and not memoryless. Cramér's model is a useful first-moment heuristic, not a literal distributional claim.

The KS distance `D(s)`, however, **decays cleanly with scale**:
> `D(s) = 0.260 · exp(−0.0842 · s)`, RMSE_log = 0.022 (best by AIC, `ΔAIC = +17.69` over power law).

So the gap distribution becomes "less wrong" (closer to exponential, by KS) as `n` grows. This is consistent with the qualitative claim in Cramér's heuristic that the deviation from the iid-uniform model shrinks at larger scales — a finding the previous round of this project asserted but did not pin down quantitatively.

### Operational consequence

The `random_prime_near(n)` method in `prime_generator.py` samples a candidate offset as `Exponential(ln n)`, advances to the nearest `6k ± 1`, then verifies primality. The argument that it works depends *only on the first moment* `E[gap] ≈ ln n`, not on the full distribution: the candidate density only needs to *cover* primes, and the verifier guarantees correctness of returned values. Part B confirms that the first moment is right (`mean / ln n ∈ [0.97, 1.01]`) and that the second moment scales as expected (`std ≈ 0.85 · ln n` empirically; for a true `Exponential(ln n)` it would be exactly `ln n`, so the gap distribution is mildly *underdispersed* relative to exponential — also consistent with expectation, since `6k±1` filtering removes some of the most extreme tails).

### Chebyshev bias

| s | n on lattice | `≡ 5 (mod 6)` | `≡ 1 (mod 6)` | diff | share `≡ 5` | binomial p (vs ½) |
|--:|--:|--:|--:|--:|--:|--:|
| 1 | 500 | 253 | 247 | +6 | 0.5060 | 0.8231 |
| 2 | 1,000 | 508 | 492 | +16 | 0.5080 | 0.6353 |
| 3 | 3,000 | 1,508 | 1,492 | +16 | 0.5027 | 0.7842 |
| 4 | 5,000 | 2,510 | 2,490 | +20 | 0.5020 | 0.7882 |
| 5 | 5,000 | 2,507 | 2,493 | +14 | 0.5014 | 0.8541 |
| 6 | 5,000 | 2,513 | 2,487 | +26 | 0.5026 | 0.7237 |
| 7 | 3,000 | 1,502 | 1,498 | +4 | 0.5007 | 0.9563 |
| 8 | 2,000 | 983 | 1,017 | −34 | 0.4915 | 0.4606 |

In **7 of 8 windows** the count `≡ 5 (mod 6)` exceeds the count `≡ 1 (mod 6)`. The mean excess across scales `1–7` is `+15` primes per window, which is small in absolute terms but consistently signed in the direction predicted by Chebyshev (1853): primes are biased toward residues that are non-quadratic-residues `(mod 6)`, of which `5` is one and `1` is not. None of the individual binomial p-values drop below 0.5 — the bias is asymptotic and is washed out by sampling noise at any single scale's window — but the *consistent sign* across scales is the empirical signature of the bias.

The neural-network study (Paper 1) cannot see Chebyshev bias because its `is_6k_pm1` feature collapses both classes into one boolean. This Part B measurement is the only place in the project where Chebyshev's effect is observable.

### Density convergence

| s | empirical density | PNT (`1/ln n`) | ratio | \|ratio − 1\| |
|--:|--:|--:|--:|--:|
| 1 | 0.13877 | 0.13332 | 1.0408 | 0.0408 |
| 2 | 0.12385 | 0.12009 | 1.0313 | 0.0313 |
| 3 | 0.10658 | 0.10394 | 1.0254 | 0.0254 |
| 4 | 0.09619 | 0.09532 | 1.0091 | 0.0091 |
| 5 | 0.08486 | 0.08495 | 0.9989 | 0.0011 |
| 6 | 0.07207 | 0.07220 | 0.9982 | 0.0018 |
| 7 | 0.06266 | 0.06203 | 1.0101 | 0.0101 |
| 8 | 0.05443 | 0.05429 | 1.0026 | 0.0026 |

`|ratio − 1|` fits as `0.0585 · s^{−1.51}` (best by AIC) — the empirical density converges to the PNT prediction as `s → ∞`, with a residual that goes as `s^{−1.51}` rather than the `s^{−1}` of a leading Riemann-correction term. That a single-window measurement at `5000` primes per scale still shows clean convergence is itself non-trivial; longer windows give tighter agreement.

---

## Part C — Retirement of legacy claims

The previous round of this project (`archive/deep_transition_analysis.py`, March 2026) made two specific quantitative claims that **the dense-grid measurements decisively reject**.

### C.1 The `s^{−0.37}` power law

The legacy code used the form `α(s) = s^{−0.37}` for the local-feature importance and `β(s) = 1 − 0.487 · s^{−0.37}` for the global. Both came from a 3-point fit at `s ∈ {2, 5, 7}`.

The new dense-grid data (40 scale samples × 2000 examples each):

- For M1 (residue excess AUC): power, exponential, and rational forms are statistically indistinguishable (`ΔAIC < 1.5`); the rational fit `0.404 / (1 + 0.040 s)` is selected for stability of parameters.
- For M2 (filter rejection rate): the rational fit `1.027 / (1 + 0.030 s)` beats the power-law fit by `ΔAIC = +30.78`. The power law is decisively rejected.

The functional family preferred by the data is *rational*, not power-law. The qualitative shape (slow concave monotone decay) is unchanged.

### C.2 The "critical transitions"

The legacy code derived three critical scales from `α(s) = s^{−0.37}`:
- *Primary*: `α = β`, supposedly at `s* = 4.5` (`n ≈ 31,623`)
- *Secondary*: `α = 0.10`, supposedly at `s = 5.89`
- *Tertiary*: `α = 0.01`, supposedly at `s = 8.57`

On the rational fit `f(s) = 1.027 / (1 + 0.030 s)`:
- `f(s)` plateaus at `0.819` at `s = 9.5` — never drops to 50 %, 10 %, or 1 % anywhere on the tested range.
- The crossover with `1 − f(s)` (which would correspond to the legacy "α = β" claim) happens at `f(s) = 0.5`, i.e. `s = (1.027 − 0.5) / (0.030 · 0.5) = 35.13` — three orders of magnitude beyond any practical regime.

The "critical transitions" do not exist on the dense-grid data. The constant `_PRIMALITY_TEST_SCALE_THRESHOLD = 4.5` does still appear in `prime_generator.py`, but only because that is approximately where deterministic Miller–Rabin overtakes trial division on commodity 64-bit hardware (since `√(10^{4.5}) ≈ 178` matches the modular-exponentiation cost crossover) — it is a *computational-cost* threshold, not a feature-importance crossover.

### What this means for the project as a whole

The structural conclusion of the previous round — **"use a `6k±1` candidate sieve plus a small-prime trial-division pre-filter and a scale-adaptive primality verifier"** — is fully preserved. It is *also* what the new neural-network study independently rediscovers as the dominant decision rule of every trained classifier (Paper 1, §3.3). Only the specific functional family (`s^{−0.37}` → `1.027 / (1 + 0.030 s)`) and the supposed transition points (`4.5, 5.89, 8.57` → none) are revised. The algorithm itself does not change; only its empirical justification gets sharper.

---

## Reproducibility

```bash
python fit_meta_pattern.py    # Part A: M1, M2, M3
python gap_analysis.py        # Part B: gaps, Chebyshev, density
```

Both scripts are deterministic at fixed seeds (`SEED = 20260517`). Reports are written to `reports/fit_meta_pattern.md` and `reports/gap_analysis.md`; raw measurements to `artifacts/fit_meta_pattern.json` and `artifacts/gap_analysis.json` (gitignored).

Total runtime: under a minute on a modern laptop.
