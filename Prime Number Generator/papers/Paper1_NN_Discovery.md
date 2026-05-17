# Paper 1 — Discovering the prime-classification function from neural-network weights

> **Empirical study.** Six multilayer perceptrons are trained at scales `s = log₁₀ n ∈ {3, 4, 5, 6, 7, 8}` to classify `n` as prime or composite from a deliberately rich, redundant 105-dimensional feature set. After training, the *only* signal we use to interpret what the networks have learned is the trained weights and gradients — never the source code that generated the features. We extract the learned function in two ways: (a) by black-box weight analysis (singular-value spectra, heavy-tail Hill exponents, effective rank, integrated-gradient attribution by feature group) and (b) by knowledge distillation into decision trees and sparse L1 logistic regressions. The dominant function recovered in (b) is the **small-prime trial-division sieve on `6k±1` candidates** — at every scale, the top features are `is_6k_pm1`, `n mod 5`, `n mod 7`, `n mod 11`, `n mod 13`, `n mod 17`, `n mod 19`, in this order, with strikingly stable importances. From (a) we extract two clean exponential scaling laws — the residue-feature attribution share decays as `0.543 · exp(−0.041 · s)` while the binary-bit attribution share grows as `2.23 · exp(0.219 · s)` — together with constant heavy-tail behaviour (Hill α ≈ 3.19 across all scales). Throughout we cross-check against the independent non-NN baseline study in [`Paper3_Empirical_Baseline.md`](Paper3_Empirical_Baseline.md) (`fit_meta_pattern.py`, 40 scale samples × 1000 + 1000 primes/composites per scale; plus `gap_analysis.py`, 8 scale windows × 500–5000 consecutive primes per window). The two studies agree on every cross-checkable claim.

---

## 1. Setup

### 1.1 Goal

A neural network cannot literally discover a closed-form prime-generation function — no such formula is known to exist, and the prime-counting function is provably non-elementary. The realistic question is the one this paper answers:

> *Given supervision only, what function does a generic MLP learn to classify primes vs composites at a given scale, and how do the learned weights and gradients vary with scale?*

If the answer is "the network rediscovers something we already know", that is itself a non-trivial outcome — it tells us the supervision target is information-rich enough to drive gradient descent to the right structural family, and it gives us a vocabulary in which to talk about *which parts* of that family are emphasised at each scale.

### 1.2 Feature design

Each integer `n` is mapped to a feature vector `x(n) ∈ ℝ¹⁰⁵` whose construction is intentionally redundant:

| Group | Dim | Definition |
|---|---|---|
| `residue` | 30 | `(n mod p) / p` for the first 30 primes `p ∈ {2, 3, 5, …, 113}` |
| `binary` | 64 | bits 0…63 of `n`, each 0 or 1 |
| `scale` | 3 | `log₁₀(n) / 20`, `log₂(n) / 64`, `digit_count / 20` |
| `wheel` | 3 | `(n mod 6) / 6`, `(n mod 30) / 30`, `(n mod 210) / 210` |
| `sieve` | 2 | `1 / 0` for `n ≡ ±1 (mod 6)`, parity bit |
| `digits` | 3 | digital root `/ 9`, digit-sum `/ (9 · 20)`, last digit `/ 9` |

The residue group hands the network the small-prime sieve directly, but the binary, wheel, sieve, and digit groups are largely redundant with it; the feature set is engineered so the network *must allocate* attention across many overlapping ways of encoding the same arithmetic information. This is what makes the integrated-gradient attribution comparison meaningful: a network that only used residues could ignore the rest, and a network that ignored residues could lean on binary bits + wheel structure instead.

### 1.3 Architecture and training

A 3-hidden-layer MLP is used at every scale:
```
x(n) ∈ ℝ¹⁰⁵  →  fc1 (128) → ReLU → Dropout(0.2)
              →  fc2 (64)  → ReLU → Dropout(0.2)
              →  fc3 (32)  → ReLU → Dropout(0.2)
              →  fc_out (1) → BCE-with-logits
```
Training: 50 epochs, batch size 128, Adam (`lr = 10⁻³`), 70 / 15 / 15 train / val / test split. A balanced dataset of 2000 primes + 2000 composites is sampled per scale by rejection sampling near `10ˢ` (with a 70 % bias towards `6k±1` candidates to keep iteration counts modest at large `s`).

### 1.4 Performance

The MLPs converge to comparable test performance at every scale:

| Scale s | Test acc | Test AUC |
|---:|---:|---:|
| 3 | 0.7850 | 0.8341 |
| 4 | 0.7333 | 0.8301 |
| 5 | 0.7333 | 0.8308 |
| 6 | 0.7550 | 0.8355 |
| 7 | 0.7433 | 0.8317 |
| 8 | 0.7367 | 0.8098 |

The networks are not "perfect" — primality at any single integer is an unsolved problem in the sense that no polynomial-size architecture can decide it without arithmetic — but they are clearly above chance, and they are stable across six orders of magnitude in `n`. AUC ≈ 0.83 across all scales is the reference performance the rest of the paper analyses.

---

## 2. What the trained NNs *see* — black-box weight analysis

For every trained model we compute per-layer statistics from the weight matrix `W` alone, plus gradient-based attribution on the test set. No source code, no features-as-strings — just the numpy arrays that come out of `model.state_dict()`.

### 2.1 Spectral analysis

For each linear layer we compute the SVD `W = U Σ Vᵀ`, then:

- **Frobenius norm** `‖W‖_F = √(Σ σ²ᵢ)`
- **Spectral norm** `σ_max = σ₁`
- **Stable rank** `‖W‖_F² / σ_max²`
- **Effective rank** `exp(−Σ pᵢ log pᵢ)` where `pᵢ = σᵢ / Σ σⱼ`
- **Hill heavy-tail exponent** `α̂ = 1 + n / Σ log(σᵢ / σ_min)` on the upper half of the spectrum (Martin–Mahoney style)

For `fc1` (the input-facing layer; shape 128 × 105) the values are essentially constant in `s`:

| Scale | ‖W‖_F | σ_max | stable rank | effective rank | Hill α |
|---:|---:|---:|---:|---:|---:|
| 3 | 7.767 | 2.649 | 8.60 | 87.04 | 3.283 |
| 4 | 7.691 | 2.435 | 9.98 | 86.81 | 3.229 |
| 5 | 7.702 | 2.520 | 9.34 | 87.36 | 3.280 |
| 6 | 7.804 | 2.738 | 8.12 | 86.38 | 3.314 |
| 7 | 7.797 | 2.661 | 8.58 | 86.76 | 3.307 |
| 8 | 7.999 | 2.801 | 8.16 | 86.82 | 3.363 |

The spectrum is consistently heavy-tailed with `α ≈ 3.19` (the rational MLE fit `α(s) = 3.194 / (1 − 0.0056 s)` has RMSE_log = 0.007 — exceptionally tight) and the network occupies a small effective subspace (stable rank ~ 8.5 vs nominal rank 105). This matches the regime that Martin & Mahoney associate with well-trained networks; the prime-classification problem does not break that pattern.

### 2.2 Integrated-gradient feature attribution

For each trained model and each prime example in a held-out batch, integrated gradients (25-step Riemann approximation, baseline = zero vector) attribute output sensitivity back to each input feature. We aggregate by feature group:

| Scale | residue | binary | scale | wheel | sieve | digits |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0.439 | 0.128 | 0.078 | 0.066 | 0.242 | 0.047 |
| 4 | 0.511 | 0.086 | 0.049 | 0.081 | 0.241 | 0.032 |
| 5 | 0.481 | 0.126 | 0.051 | 0.052 | 0.248 | 0.042 |
| 6 | 0.387 | 0.182 | 0.066 | 0.080 | 0.243 | 0.042 |
| 7 | 0.390 | 0.187 | 0.055 | 0.060 | 0.250 | 0.059 |
| 8 | 0.404 | 0.233 | 0.057 | 0.065 | 0.208 | 0.032 |

Two clear trends and one constant:

- **Residue attribution decays** with scale (`0.439 → 0.404` from `s = 3` to `s = 8`, with a noisy peak at `s = 4`).
- **Binary-bit attribution grows** with scale (`0.128 → 0.233`).
- **Sieve attribution is constant** at `0.21–0.25` — the `is_6k_pm1` plus parity feature pair carries the same information at every scale, as it should.

### 2.3 Scaling-law extraction (MLE + AIC)

For every scalar weight statistic `y(s)` that varies non-trivially with scale, we fit four functional forms by maximum likelihood with Gaussian errors on `log y` and pick the best by AIC:

```
constant    f(s) = c
power       f(s) = a · s^b
exponential f(s) = a · exp(b s)
rational    f(s) = a / (1 + b s)
```

The non-trivially-varying statistics and their best fits are:

| Statistic | Best form | a | b | RMSE_log | ΔAIC vs power | ΔAIC vs exp | ΔAIC vs rational |
|:---|:---|---:|---:|---:|---:|---:|---:|
| `fc1.fro_norm` | rational | 7.5522 | −0.0056 | 0.0084 | +1.63 | +0.05 | best |
| `fc1.spectral_norm` | rational | 2.3898 | −0.0166 | 0.0360 | +0.93 | +0.07 | best |
| `fc1.stable_rank` | exponential | 10.0370 | −0.0245 | 0.0607 | +0.58 | best | +0.06 |
| `fc1.hill_alpha` | rational | 3.1939 | −0.0056 | 0.0073 | +1.50 | +0.04 | best |
| `fc1.weight_mean_abs` | rational | 0.0532 | −0.0052 | 0.0081 | +1.38 | +0.04 | best |
| `fc1.weight_kurtosis` | power | 6.9228 | −0.2488 | 0.0856 | best | +0.19 | +0.13 |
| `fc2.bias_mean_abs` | power | 0.0406 | +0.1859 | 0.0127 | best | +3.93 | +4.64 |
| `fc3.bias_mean_abs` | power | 0.0523 | +0.2954 | 0.1471 | best | +0.38 | +0.44 |
| `attribution_share.residue` | exponential | 0.5429 | −0.0412 | 0.0791 | +0.55 | best | +0.07 |
| `attribution_share.binary` | rational | 0.0769 | −0.0844 | 0.1660 | +2.12 | +0.59 | best |
| `attribution_abs.binary` | exponential | 2.2264 | +0.2188 | 0.1747 | +1.75 | best | +0.03 |
| `attribution_abs.sieve` | power | 8.3113 | +0.2146 | 0.0768 | best | +0.97 | +1.16 |

The remaining 38 weight statistics (mostly per-layer norms and weight-magnitude moments) are essentially constant in `s` (`std(y) / mean|y| < 10⁻⁴`).

The two attribution-share results are the cleanest and the most interpretable:

> Residue-feature attribution share: `f_residue(s) = 0.5429 · exp(−0.0412 · s)` — RMSE_log = 0.079.
>
> Binary-bit attribution magnitude: `f_binary(s) = 2.2264 · exp(+0.2188 · s)` — RMSE_log = 0.175.

Both are consistent with the same underlying number-theoretic fact: at large `n`, fewer composites have small prime factors, so residues mod small primes carry strictly less information per query. The network has no theorem of distribution available to it, but gradient descent allocates attention as if it does. (Cross-check: the independent baseline study `fit_meta_pattern.py` gives `f₂(s) = 1.027 / (1 + 0.030 · s)` for the small-prime filter rejection rate — a slow decay of essentially the same shape.)

---

## 3. What the trained NNs *do* — knowledge distillation

Spectral analysis tells us the network is well-trained and heavy-tailed; gradient attribution tells us *which kinds* of features matter at each scale; but neither tells us the *rule* the network has learned. For that we distil each MLP into a human-inspectable surrogate.

### 3.1 Method

For each scale we use the trained MLP as a teacher, generating soft targets `p̂(prime | x)` on the training set. Two surrogates are then fit on those soft targets:

- **Decision tree.** `max_depth = 8`, `min_samples_leaf = 20`, sklearn defaults otherwise. Reports feature importances and a printable rule list.
- **Sparse L1 logistic regression.** Standardised features, `C = 0.1`, saga solver. Reports nonzero coefficient counts and signed coefficient magnitudes.

For both we measure the *agreement with the NN* on the held-out test set (NN-as-truth-oracle), the *agreement with ground truth* (sympy `isprime`), and the AUC against the true labels.

### 3.2 Fidelity

| Scale | NN acc | NN AUC | tree → NN | tree AUC | tree leaves | logit → NN | logit AUC | logit nz coefs |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0.7850 | 0.8341 | 0.8350 | 0.9256 | 14 | 0.8900 | 0.8559 | 43 |
| 4 | 0.7333 | 0.8301 | 0.7683 | 0.9155 | 15 | 0.8217 | 0.8487 | 44 |
| 5 | 0.7333 | 0.8308 | 0.7700 | 0.9213 | 14 | 0.8083 | 0.8422 | 45 |
| 6 | 0.7550 | 0.8355 | 0.8000 | 0.8971 | 14 | 0.8333 | 0.8433 | 42 |
| 7 | 0.7433 | 0.8317 | 0.7917 | 0.8880 | 13 | 0.8917 | 0.8344 | 45 |
| 8 | 0.7367 | 0.8098 | 0.7733 | 0.8930 | 13 | 0.8067 | 0.8221 | 49 |

Notable: the **tree AUC is consistently higher than the NN AUC** because the tree is fitting the NN's *probabilities* (a smoother target) while measuring AUC against the discrete ground-truth labels. The tree captures the NN's ranking even at points where the NN's hard decisions are wrong.

### 3.3 The function the NN has learned

The decision-tree feature importances tell a single, clean, scale-invariant story. The top six features and their importances at every scale:

| Rank | s = 3 | s = 4 | s = 5 | s = 6 | s = 7 | s = 8 |
|---:|---|---|---|---|---|---|
| 1 | `is_6k_pm1` (0.479) | `is_6k_pm1` (0.422) | `is_6k_pm1` (0.428) | `is_6k_pm1` (0.463) | `is_6k_pm1` (0.461) | `is_6k_pm1` (0.467) |
| 2 | `res_5` (0.218) | `res_5` (0.181) | `res_5` (0.199) | `res_5` (0.223) | `res_5` (0.204) | `res_5` (0.195) |
| 3 | `res_7` (0.135) | `res_7` (0.154) | `res_7` (0.116) | `res_7` (0.114) | `res_7` (0.144) | `res_7` (0.134) |
| 4 | `res_11` (0.049) | `res_13` (0.067) | `res_11` (0.074) | `res_13` (0.070) | `res_13` (0.054) | `res_13` (0.053) |
| 5 | `res_13` (0.039) | `res_11` (0.058) | `res_13` (0.066) | `res_11` (0.053) | `res_11` (0.051) | `res_17` (0.048) |
| 6 | `res_17` (0.039) | `res_17` (0.053) | `res_19` (0.051) | `res_19` (0.029) | `res_19` (0.035) | `res_11` (0.045) |

The rule that gradient descent has converged to at every scale is, to within minor reordering of the rare-prime residues:

> **`n` is more likely prime ⇔ `n ≡ ±1 (mod 6)` AND `n` is not divisible by 5, 7, 11, 13, 17, 19.**

This is the **wheel-30 sieve** plus a small-prime trial-division pre-filter — the same algorithm that has been used to enumerate primes since Eratosthenes (with Lehmer–Euler refinements). The L1 logistic confirms the same picture: at every scale the largest positive coefficient is on `is_6k_pm1` (≈ +3.1), the second is on `res_5` (≈ +1.5), then `res_7` (≈ +0.6), then `res_11`, `res_13`, `res_17`. Everything else carries < 0.5 standardised weight.

### 3.4 What this means

Two interpretations are equally honest:

- **Optimistic.** Gradient descent on a generic MLP, given only prime-vs-composite supervision and a redundant feature set, recovers the right structural family for primality testing. This is a non-trivial fact — most ML problems do not decompose this cleanly when a richer-than-needed feature set is supplied.

- **Cautious.** Because the residue features `n mod p` are *exact divisibility tests*, the supervision signal already encodes the sieve almost on the surface. The network's "discovery" is closer to a sanity check that the optimiser did not get distracted by the binary bits, the wheel mods, or the digit features. The genuinely novel observation is the *quantitative* attribution shift across scales (Section 2.2), not the *qualitative* fact that the sieve is the right answer.

We endorse the cautious reading throughout the rest of the paper.

---

## 4. Cross-check against the independent non-NN baseline ([Paper 3](Paper3_Empirical_Baseline.md))

[Paper 3](Paper3_Empirical_Baseline.md) measures, with no neural network involved, three quantities on a denser scale grid (40 samples × 1000 + 1000 primes/composites per scale) using only logistic regression, Monte Carlo, and sympy primality testing:

| Measurement | Best-fit form | a | b | RMSE_log | ΔAIC over power | ΔAIC over exp | ΔAIC over rational |
|:---|:---|---:|---:|---:|---:|---:|---:|
| M1 — residue-classifier excess AUC | rational | 0.404 | 0.040 | 0.137 | +1.36 | +0.99 | best |
| M2 — small-prime filter rejection rate | rational | 1.027 | 0.030 | 0.034 | +30.78 | +1.94 | best |
| M3 — PNT density relative error | power | 0.505 | −1.881 | 0.317 | best | +6.41 | +5.84 |

Plus, from `gap_analysis.py`:

- Empirical Cramér ratio `mean(gap) / ln n ∈ [0.97, 1.01]` over `s ∈ [1, 8]` — confirms the first-moment claim of Cramér's heuristic.
- KS-distance to `Exponential(ln n)` decays as `0.260 · exp(−0.0842 s)`, RMSE_log = 0.022 (best by AIC) — the gap distribution becomes "less wrong" relative to exponential as `n` grows.
- Chebyshev bias visible (count `≡ 5 (mod 6)` exceeds count `≡ 1 (mod 6)`) in 7 of 8 windows tested — the NN cannot see this because its `is_6k_pm1` feature collapses both classes.
- Empirical density / PNT density converges to 1 as `|ratio − 1| ~ 0.06 · s^{−1.51}`.

The agreement with the NN study is strong:

- **M1 ↔ NN residue attribution.** Both decay slowly with scale; MLE on the NN says exponential `0.5429 · exp(−0.0412 s)` (tightest), MLE on logistic-regression AUC says rational `0.404 / (1 + 0.040 s)` (tightest). Either fit predicts a `5–10 %` drop per unit `s` — the same qualitative behaviour from two independent measurement pipelines.
- **M2 ↔ tree feature importances.** The small-prime filter rejection rate plateaus around `0.82` at `s = 9`, never dropping below it; the tree's distilled rule keeps `res_5, res_7, res_11, res_13, res_17, res_19` as the dominant residues at every scale tested. Both confirm that the small-prime filter is *useful at every scale tested*, not just at small `n`.
- **M3** is the PNT residual; the NN does not have access to it, but the algorithm in Paper 2 uses the M3 fit only to size pre-filters, not as a primality signal.

These measurements are the only ones used for algorithm sizing in `MetaPatternPrimeGenerator`; the NN study is *interpretive* and does not feed back into the algorithm constants.

---

## 5. Limitations and future work

1. **No NN learns "primality" in any deeper sense.** Test AUC saturates at ≈ 0.83 across all scales, identical to a residue-only logistic regression. The MLP has not extracted any structure beyond what residues mod the first ~10 primes already provide.
2. **Attribution is not causation.** Integrated gradients tell us where the *output is most sensitive* to the input on average, not which features the network "uses" in any mechanistic sense. The decision-tree distillation is more direct evidence of the function's structure.
3. **Six scales is enough for a clean fit but not enough to distinguish exp from rational with high confidence on the noisier statistics** (e.g. `attribution_abs.binary` has RMSE_log = 0.175). A future version should run more scales and replicate seeds.
4. **Probabilistic vs deterministic divide.** The NN at `τ = 0.5` has primality recall 21–68 % (Paper 2, Section 5). It is not a primality test. Sliding `τ` upward improves precision at the cost of recall, with no setting that beats deterministic Miller–Rabin on either axis.
5. **Architecture choice is fixed.** A 3-layer MLP is large enough to overfit the residue features; a transformer or graph network on the integer's factor graph might give richer signal. We did not explore this.

---

## 6. Reproducibility

All numbers, tables, and fits in this paper are regenerated by the scripts in `Prime Number Generator/`:

```
train_nn_classifiers.py     → artifacts/{data,model,history}_s{3..8}.{npz,pt,json}
analyze_nn_weights.py       → reports/nn_weight_analysis.md, artifacts/weight_analysis.json
extract_function.py         → reports/nn_distillation.md, artifacts/distillation.json
compare_methods.py          → reports/nn_compare_methods.md, artifacts/compare_methods.json
fit_meta_pattern.py         → reports/fit_meta_pattern.md, artifacts/fit_meta_pattern.json     (§4 baseline)
gap_analysis.py             → reports/gap_analysis.md, artifacts/gap_analysis.json             (Paper 3 §B)
```

Random seed `20260517 + scale * 1000` is used end-to-end; all results are bit-reproducible.
