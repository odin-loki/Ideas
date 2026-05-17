# Complete prime meta-pattern research — combined narrative

> One single read-through of the entire project, from motivation through methods, results, and operational consequences. Composed of the same material as Paper 1, Paper 2, and the algorithm-derivation reference, restructured for linear reading.

---

## Part I — Motivation

The original aim of this research project was direct:

> **Train a neural network on prime-vs-composite classification, then attempt to extract the function it has learned from its trained weights — and use that as the basis of a prime generator. Compare to conventional sieve-based methods.**

Two things had to be done before the question could be answered honestly. First, the supervisory signal had to be made meaningful: the network's input features could not silently leak the answer. Second, "extract the function from the weights" had to be operationalised — neural networks do not surrender closed-form rules to inspection, but they do surrender (a) gradient-based attribution maps over inputs, (b) singular-value spectra over weight matrices, and (c) decision-boundary surrogates obtainable by knowledge distillation. We use all three.

A baseline empirical study was also performed independently, without any neural network, to give a reference point against which the NN's "discovery" could be judged.

---

## Part II — Baseline empirical study (no NN)

In `fit_meta_pattern.py` we measure three quantities at 40 scale samples `s ∈ [1.0, 9.5]`, with 1000 + 1000 balanced primes / composites per scale (3.2 million primality tests total via `sympy.isprime`):

- **M1 — residue-classifier excess AUC.** Train a logistic regression on the 30 residue features `(n mod p) / p` for `p ∈ {first 30 primes}`, evaluate on a held-out half, report `AUC − 0.5`.
- **M2 — small-prime filter rejection rate.** Fraction of composite samples rejected by the first 15 small primes' trial divisions.
- **M3 — PNT density relative error.** `|π(2n) − π(n) − n / ln n| / (n / ln n)` evaluated empirically.

For each, four functional forms are fit by maximum likelihood with Gaussian errors on `log y`, model selected by AIC:

| Measurement | Best form | a | b | RMSE_log | ΔAIC vs power | ΔAIC vs exp | ΔAIC vs rational |
|:---|:---|---:|---:|---:|---:|---:|---:|
| M1 | rational | 0.404 | 0.040 | 0.137 | +1.36 | +0.99 | best |
| M2 | rational | 1.027 | 0.030 | 0.034 | +30.78 | +1.94 | best |
| M3 | power | 0.505 | −1.881 | 0.317 | best | +6.41 | +5.84 |

M1 and M2 are best fit by a *rational plateau* — both decay slowly with `s` and never approach zero on the tested range. The small-prime filter retains rejection rate ≥ 0.82 over the whole interval, refuting any naive expectation that "as `n` grows, small primes lose all power as a filter". Power-law forms are decisively rejected for M2 (`ΔAIC = +30.78`).

This study fixes the constants used by the conventional algorithm. The trained-NN study below is an *independent* line of evidence that arrives at compatible conclusions.

---

## Part III — Neural network study

### Architecture and training

Six MLPs are trained (one per scale `s ∈ {3, 4, 5, 6, 7, 8}`):

```
x(n) ∈ ℝ¹⁰⁵  → fc1 (128) → ReLU → Dropout(0.2)
              → fc2 (64)  → ReLU → Dropout(0.2)
              → fc3 (32)  → ReLU → Dropout(0.2)
              → fc_out (1) → BCE-with-logits
```

50 epochs, batch 128, Adam `lr = 10⁻³`, 70 / 15 / 15 train / val / test split, balanced 2000 + 2000 prime / composite per scale. Inputs are a deliberately rich, redundant 105-dimensional feature set: 30 normalised prime residues, 64 binary bits, 3 scale features, 3 wheel modular features, 2 sieve indicators (`is_6k_pm1`, parity), 3 digit features.

Test AUC settles at `0.81–0.83` across all six scales.

### What the trained networks see — black-box analysis

For every trained model we extract weights and gradients only — no source-code introspection. Per-layer SVD gives spectral statistics; integrated gradients give per-feature attribution.

**Per-layer (fc1, layer-1) summary, all scales:**

- Frobenius norm `‖W‖_F`: 7.69–8.00, essentially constant
- Effective rank: ≈ 87 (out of 105) — full-rank-ish
- Stable rank: 8.1–10.0 — the network occupies a small effective subspace
- Hill α on the upper SVD: `3.19–3.36` — heavy-tailed, consistent with well-trained networks (Martin–Mahoney "self-regularisation" regime)

**Feature-group attribution (integrated gradients):**

| Scale | residue | binary | scale | wheel | sieve | digits |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0.439 | 0.128 | 0.078 | 0.066 | 0.242 | 0.047 |
| 8 | 0.404 | 0.233 | 0.057 | 0.065 | 0.208 | 0.032 |

Two scaling laws emerge from MLE + AIC over all six scales:

> **Residue-attribution share decays:** `0.5429 · exp(−0.0412 · s)`, RMSE_log = 0.079.
>
> **Binary-bit attribution magnitude grows:** `2.2264 · exp(+0.2188 · s)`, RMSE_log = 0.175.

Both are consistent with the underlying number-theoretic fact that small-prime divisibility carries less information at large `n`, *even though the network has no theorem of distribution to consult*. The residue shift is also consistent with M1 from Part II (rational plateau, slow decay) — two independent measurement pipelines, the same qualitative behaviour.

### What the trained networks have learned — knowledge distillation

For each scale we use the trained MLP as a teacher, distil its soft predictions into a depth-8 decision tree and an L1-regularised logistic regression. Tree fidelity to the NN is `0.77–0.84`; logistic fidelity is `0.81–0.89`.

**The decision tree's top features are nearly identical at every scale:**

| Rank | s = 3 | s = 8 |
|---:|---|---|
| 1 | `is_6k_pm1` (0.479) | `is_6k_pm1` (0.467) |
| 2 | `res_5` (0.218) | `res_5` (0.195) |
| 3 | `res_7` (0.135) | `res_7` (0.134) |
| 4 | `res_11` (0.049) | `res_13` (0.053) |
| 5 | `res_13` (0.039) | `res_17` (0.048) |
| 6 | `res_17` (0.039) | `res_11` (0.045) |

The L1-logistic confirms the same picture: largest positive coefficient `+3.14` on `is_6k_pm1`, `+1.55` on `res_5`, `+0.64` on `res_7`, then `res_11`, `res_13`, `res_17`. Everything else has standardised coefficient magnitude `< 0.5`.

The function the network has converged to at every scale is, modulo minor reordering of low-importance residues:

> ***`n` is more likely prime ⇔ `n ≡ ±1 (mod 6)` AND `n` is not divisible by 5, 7, 11, 13, 17, 19.***

This is the **wheel-30 sieve plus small-prime trial division** — Eratosthenes' algorithm with a Lehmer wheel acceleration. The non-trivial finding is not the rule itself but its robustness across six orders of magnitude in `n`.

---

## Part IV — Three prime generators

The structural conclusion of Part III suggests an obvious algorithm:

```
6k±1 candidate enumerator → filter → verifier → return
```

We specify three variants by the choice of filter, all sharing the same enumerator and verifier:

### 4.1 `MetaPatternPrimeGenerator` — conventional baseline

Filter: small-prime trial division (the first `15 · w₂(s)` primes, where `w₂(s) = 1.027 / (1 + 0.030 s)` from M2).

Verifier: trial division below `s = 4.5`, Sorenson–Webster (2017) deterministic Miller–Rabin up to `n < 3.317 × 10²⁴`, probabilistic Miller–Rabin (`k = 20`, error `≤ 4⁻²⁰ ≈ 9.1 × 10⁻¹³`) above.

Two semantics are exposed:
- `next_prime(n)` — the smallest prime `≥ n`. Strictly correct.
- `random_prime_near(n)` — a Cramér-gap random prime near `n` for cryptographic key-generation use.

### 4.2 `NNAugmentedPrimeGenerator`

Filter: trained MLP at the closest scale, threshold at `τ` on `sigmoid(model(featurize(n)))`.

Verifier: same as 4.1.

Output is exactly correct (verifier guarantees it). The NN's only role is to filter candidates before the verifier runs.

### 4.3 `PureNNPrimeGenerator`

Filter and verifier collapsed: NN scoring at threshold `τ`. No deterministic test. Output is what the NN says it is.

---

## Part V — Head-to-head benchmark

50 starting points × 5 consecutive primes per start, per scale. Tau = 0.5 for both NN variants.

| Scale | Conv ms/prime | NN-aug ms/prime | Pure-NN ms/value | Pure-NN recall | Pure-NN skip rate | NN-aug speed ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0.006 | 0.469 | 0.291 | 0.6840 | 0.0000 | 78× |
| 4 | 0.010 | 0.972 | 0.564 | 0.4040 | 0.2240 | 97× |
| 5 | 0.019 | 1.307 | 0.581 | 0.4680 | 0.0200 | 69× |
| 6 | 0.021 | 1.277 | 0.446 | 0.3520 | 0.0360 | 61× |
| 7 | 0.024 | 2.022 | 0.585 | 0.2600 | 0.1440 | 84× |
| 8 | 0.030 | 1.798 | 0.458 | 0.2120 | 0.0960 | 60× |

The accept rate of the NN filter (49–56 %) is **higher** than that of the small-prime filter (23–25 %). The NN does not even reduce the number of candidates that reach the verifier. Combined with the per-candidate inference cost (`~22 800` flops + Python featurization vs `~60` flops for trial division), the NN-augmented variant ends up `60–97 ×` slower than the conventional baseline.

The pure-NN at τ = 0.5 has primality recall `21–68 %` and produces a returned-value-is-actually-prime rate that drops with scale. It is decisively not a primality test on its own.

---

## Part VI — Honest interpretation

### What the project demonstrates

1. **A generic MLP, given a redundant feature set, recovers known sieve mathematics from raw classification supervision.** This is itself a non-trivial fact — most ML problems do not decompose this cleanly. Gradient descent does not get distracted by the binary bits, the wheel mods, or the digit features.
2. **The trained network's allocation of attention shifts with scale in a measurable, regular way.** Two clean exponential laws govern the residue-vs-binary trade-off; both are consistent with the diminishing usefulness of small-prime divisibility at large `n`.
3. **The learned function distils, at every scale, into the same canonical algorithm:** `is_6k_pm1 ∧ ¬(n divisible by any of 5, 7, 11, 13, 17, 19)`. This is the wheel-30 sieve.
4. **As a generator, the NN-augmented variant is dominated by the conventional baseline on speed** (60–97 × slower) and ties on correctness (verifier guarantees both). The NN's "discovery" produces no operational improvement.

### What the project does *not* demonstrate

1. **A closed-form prime-generation function.** There is no such formula. The "function discovered from the NN's weights" is the small-prime sieve — already known mathematics, rederived here from data.
2. **An NN-only primality test.** Pure-NN recall at τ = 0.5 is `21–68 %`. Adjusting τ trades recall for precision but does not reach a useful regime.
3. **Faster prime generation.** The conventional baseline strictly dominates.

### Why this is still worth doing

Two things make the study valuable in spite of the negative operational result:

- **It is a rare instance of "interpretability-by-construction": gradient descent on a redundant feature set converges on a known optimal algorithm, and the path to that algorithm is reconstructable from the weights alone.** This is the kind of validation that mechanistic-interpretability literature is usually short on.
- **The two attribution scaling laws are quantitatively meaningful** — they describe how an *unaware* learning system reallocates attention as the underlying problem scales, which is a transferable observation about how any feature-redundant classifier behaves on increasingly difficult problem instances.

---

## Part VII — Reproducibility

Everything in this document is regenerated by the scripts in `Prime Number Generator/`:

```
fit_meta_pattern.py       → Part II, baseline study
train_nn_classifiers.py   → Part III training
analyze_nn_weights.py     → Part III analysis
extract_function.py       → Part III distillation
compare_methods.py        → Part V benchmark
verify_generator.py       → audit of MetaPatternPrimeGenerator
prime_generator.py        → built-in self-tests
```

Random seeds are fixed (`20260517 + scale * 1000`); CPU-only PyTorch; total runtime under five minutes on a modern laptop.
