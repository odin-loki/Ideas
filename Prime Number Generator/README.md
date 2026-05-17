# Prime Number Generator — discovering the prime-classification function from neural-network weights, and operationalising it

A research project that asks two questions: **(1)** if you train a neural network to classify integers as prime or composite, what function does it actually learn? and **(2)** can that learned function be used as the basis of a useful prime generator? The answer to (1) — derived through black-box weight analysis and knowledge distillation across six scales — is that gradient descent rediscovers the small-prime trial-division sieve on `6k±1` candidates, the same algorithm we have been using since Eratosthenes. The answer to (2) is no: the conventional hand-coded sieve is `60–97×` faster than the NN-augmented variant, and the NN-only variant has primality recall of only `21–68 %`. The NN turns out to be a useful **analytical instrument** that recovers known sieve mathematics from data, rather than a faster generation kernel. The repository ships the empirical study, the NN study, three generator implementations (conventional, NN-augmented, pure-NN), an end-to-end audit, and five research papers documenting every claim.

---

> **A black-box study of what a neural network *learns* when it is trained on prime-vs-composite classification, paired with a hybrid prime generator that operationalises the findings, all cross-checked against an independent non-NN empirical baseline.**
>
> Six MLPs are trained at scales `s = log₁₀ n ∈ {3, 4, 5, 6, 7, 8}` on a deliberately rich, redundant 105-dimensional feature set (residues, binary bits, wheel structure, scale, digits). After training we never look at any source code; we only **measure the weights and gradients** to extract the function the network has learned. Across all six scales, the function distils — through both decision-tree and sparse-logistic surrogates — into the **small-prime trial-division sieve on `6k±1` candidates** (top features: `is_6k_pm1`, `n mod 5`, `n mod 7`, `n mod 11`, `n mod 13`, `n mod 17`, `n mod 19`). Gradient descent rediscovers the wheel sieve from raw classification supervision alone. The trained weights additionally exhibit two clean exponential scaling laws — residue-feature attribution decays as `0.543 · exp(−0.041 · s)` while binary-feature attribution grows as `2.23 · exp(0.219 · s)` — together with constant heavy-tail Hill α ≈ 3.19 across all scales. An independent non-NN study (`fit_meta_pattern.py` over 40 scale samples × 1000 + 1000 primes/composites per scale, plus `gap_analysis.py` over 8 scale windows × 500–5000 consecutive primes per window) confirms: filter rejection rate `f(s) = 1.027 / (1 + 0.030 s)` (rational, `ΔAIC = +30.78` over power law); empirical Cramér ratio `mean(gap) / ln n ∈ [0.97, 1.01]`; KS distance to `Exponential(ln n)` decays as `0.260 · exp(−0.084 s)`; small but consistently signed Chebyshev bias toward primes `≡ 5 (mod 6)` over `≡ 1 (mod 6)` in 7 of 8 windows. The `MetaPatternPrimeGenerator` and `NNAugmentedPrimeGenerator` then ask: can the network *be* the generator? Direct head-to-head benchmarking shows the NN-augmented variant is **60–97× slower** than the hand-coded conventional variant despite producing identical exact output, and the pure-NN variant has primality recall of only `21–68 %` at τ = 0.5. The honest finding: **the NN is valuable as an analytical instrument that recovers known sieve mathematics from data, not as a faster prime-generation kernel.**

---

## Quick start

```python
from prime_generator import MetaPatternPrimeGenerator

gen = MetaPatternPrimeGenerator()

gen.next_prime(10**9)            # 1000000007    — the smallest prime ≥ 10⁹
gen.is_prime(10**9 + 7)          # True          — primality test
gen.random_prime_near(10**12)    # e.g. 1000000028327  — a random prime near 10¹², for crypto
gen.generate_n_primes(10**6, 5)  # [1000003, 1000033, 1000037, 1000039, 1000081]
```

Output is **exact** for `n < 3.317 × 10²⁴` (deterministic Miller–Rabin with Sorenson–Webster (2017) witness sets), and probabilistic with per-call error `≤ 4⁻²⁰ ≈ 9 × 10⁻¹³` above that bound. No primes are skipped by `next_prime`; `random_prime_near` deliberately samples a Cramér-style gap so it can serve cryptographic key generation where any prime of the right size suffices.

---

## What this project is

### The research question

The original aim was direct: train a neural network on prime-vs-composite classification, then attempt to extract the function it has learned **from its trained weights**, and use that as the basis of a prime generator. Compare to conventional sieve-based methods.

A neural network cannot literally "discover the formula for primes" — no such formula exists, the prime-counting function is provably non-elementary, and the decision boundary between primes and composites is not algebraic. But two well-defined questions remain:

1. **What function does a generic MLP, trained only on classification supervision, converge on at a given scale?**
2. **Can that learned function be operationalised as a prime generator that is competitive with or better than the hand-coded baseline?**

The project answers both. The answer to (1) is the small-prime trial-division sieve on `6k±1` candidates, robust across six orders of magnitude in `n`. The answer to (2) is **no** — the NN is `60–97×` slower as a generator, with no improvement in correctness.

### Two parallel studies

The project performs two independent empirical studies that converge on the same structural conclusion via different measurement pipelines:

- **The non-NN baseline study** (`fit_meta_pattern.py` + `gap_analysis.py`, written up in [Paper 3](papers/Paper3_Empirical_Baseline.md)) measures, with no neural network involved, six quantities across scales using only logistic regression, Monte Carlo, and `sympy.isprime`: the residue-classifier excess AUC, the small-prime filter rejection rate, the PNT density relative error, the empirical Cramér ratio `mean(gap)/ln n`, the KS distance to `Exponential(ln n)`, and the Chebyshev bias between primes `≡ 5 (mod 6)` and `≡ 1 (mod 6)`.
- **The neural-network study** (`train_nn_classifiers.py` + `analyze_nn_weights.py` + `extract_function.py`, written up in [Paper 1](papers/Paper1_NN_Discovery.md)) trains six MLPs on a 105-dimensional redundant feature set, then extracts the learned function in two ways: by black-box weight analysis (SVD spectra, heavy-tail Hill exponents, integrated-gradient attribution) and by knowledge distillation into decision trees and sparse L1 logistic regressions.

### Three generators

[Paper 2](papers/Paper2_Algorithm_Specification.md) specifies and benchmarks three generators that share a candidate enumerator and a verifier but differ in the candidate filter:

| Generator | Filter | Verifier | Output | Speed |
|---|---|---|---|---|
| `MetaPatternPrimeGenerator` | small-prime trial division (size set by `f₂(s) = 1.027 / (1 + 0.030 s)` from M2) | scale-adaptive: trial division → Sorenson–Webster det. Miller–Rabin → probabilistic Miller–Rabin (`k = 20`) | exact for `n < 3.317 × 10²⁴`; `≤ 4⁻²⁰` per-call error above | `0.006–0.030 ms/prime` |
| `NNAugmentedPrimeGenerator` | trained MLP at closest scale (threshold τ on `sigmoid(model(x))`) | same as above | exact (verifier guarantees output) | `60–97 ×` slower than baseline |
| `PureNNPrimeGenerator` | (none) | trained MLP at closest scale | bounded by NN error | recall `21–68 %` at τ = 0.5 |

---

## Folder structure

```
Prime Number Generator/
├── README.md                              ← you are here
├── papers/                                ← five curated research documents
│   ├── Paper1_NN_Discovery.md             — NN black-box analysis + distillation
│   ├── Paper2_Algorithm_Specification.md  — three generators + correctness + benchmark
│   ├── Paper3_Empirical_Baseline.md       — non-NN baseline (M1/M2/M3 + gap + Chebyshev)
│   ├── Algorithm_Derivation.md            — one-page reference card
│   └── Combined_Research_Summary.md       — single linear read of the whole project
├── reports/                               ← auto-generated reports (regenerated by the scripts)
│   ├── fit_meta_pattern.md                — M1, M2, M3 measurement report
│   ├── gap_analysis.md                    — gap distribution + Chebyshev + density
│   ├── nn_weight_analysis.md              — black-box weight statistics + scaling laws
│   ├── nn_distillation.md                 — decision-tree + L1-logistic distillations
│   └── nn_compare_methods.md              — head-to-head generator benchmark
├── prime_generator.py                     — core generator (MetaPatternPrimeGenerator)
├── nn_prime_generator.py                  — NN-augmented + pure-NN variants
├── verify_generator.py                    — end-to-end audit (10 scales, 6 no-skip checks)
├── fit_meta_pattern.py                    — empirical baseline (M1, M2, M3)
├── gap_analysis.py                        — gap distribution + Chebyshev + density
├── train_nn_classifiers.py                — train six MLPs (one per scale)
├── analyze_nn_weights.py                  — black-box weight analysis
├── extract_function.py                    — knowledge distillation
├── compare_methods.py                     — head-to-head benchmark
├── artifacts/                             — generated json / npz / pt / pkl (gitignored)
└── archive/                               — legacy material with explanatory README
    ├── README.md
    ├── deep_transition_analysis.py
    ├── prime_meta_patterns.png
    └── transition_mechanics.png
```

Python scripts live at the top level so cross-imports stay simple. All Markdown is in `papers/` (curated) or `reports/` (auto-generated). Generated binaries and JSON are in `artifacts/` and gitignored. The `archive/` folder preserves the previous round's material for traceability — its README explains what was kept, what was retired, and why.

---

## Where to start reading

If you have an hour or less, read in this order:

1. **`papers/Combined_Research_Summary.md`** — the whole project in one linear pass; the right document to read first if you want a single self-contained narrative.
2. **`papers/Algorithm_Derivation.md`** — one-page reference card mapping every empirical input to a concrete algorithm decision; read second to pin down "where does each constant come from".
3. **`papers/Paper3_Empirical_Baseline.md`** — the *non-NN* baseline (M1/M2/M3 measurements, gap distribution, Chebyshev bias, density convergence). Foundational; the algorithm constants come from here.
4. **`papers/Paper1_NN_Discovery.md`** — the NN study. What the trained networks see, two scaling laws on the weights, the distilled small-prime sieve.
5. **`papers/Paper2_Algorithm_Specification.md`** — the three generators, their correctness arguments, and the head-to-head benchmark.

If you only have ten minutes, read the abstract above, [Paper 3 §C](papers/Paper3_Empirical_Baseline.md) (what was retired between rounds), and [Paper 1 §3.3](papers/Paper1_NN_Discovery.md) (the function the NN has learned).

---

## Installation

Standard scientific-Python stack; no GPU required, no native build steps.

```bash
pip install numpy scipy scikit-learn sympy torch
```

Tested with Python 3.10–3.13 on Windows / Linux / macOS. PyTorch is needed only for the NN study; the conventional `MetaPatternPrimeGenerator` runs on `numpy` alone.

---

## Programmatic API

### `MetaPatternPrimeGenerator` — the core generator

```python
import numpy as np
from prime_generator import MetaPatternPrimeGenerator

gen = MetaPatternPrimeGenerator()                                 # defaults are fine
gen = MetaPatternPrimeGenerator(rng=np.random.default_rng(42))    # for reproducible random_prime_near
gen = MetaPatternPrimeGenerator(mr_rounds=40)                     # tighten probabilistic Miller–Rabin
```

| Method | Returns | Semantics |
|---|---|---|
| `gen.next_prime(n)` | `int` | The smallest prime `≥ n`. Strict — no primes are skipped. |
| `gen.is_prime(n)` | `bool` | Primality test (scale-adaptive: trial division / det. MR / prob. MR). |
| `gen.random_prime_near(n, rng=None, max_attempts=1000)` | `int` | A prime "near" `n`, sampled by Cramér gap `Exponential(ln n)`. Suitable for cryptographic key generation; **may skip primes** between `n` and the sampled position. |
| `gen.generate_n_primes(start, count)` | `list[int]` | `count` consecutive primes starting from `next_prime(start)`. |
| `gen.miller_rabin(n, k=None)` | `bool` | Direct access to the Miller–Rabin primality test. With `k=None` chooses deterministic witnesses for `n < 3.317 × 10²⁴` and `k = 20` probabilistic rounds above. |
| `gen.trial_division(n)` | `bool` | Direct access to `O(√n)` trial division. |
| `gen.next_6k_pm1(n)` / `step_6k_pm1(n)` / `nearest_6k_pm1(n)` | `int` | `6k±1` candidate-lattice helpers. |
| `gen.filter_weight(n)` | `float` | The empirical filter rejection rate `f₂(s) = 1.027 / (1 + 0.030 s)` evaluated at `s = log₁₀ n`. Used internally to size the small-prime pre-filter. |
| `gen.residue_information(n)` | `float` | The empirical residue-classifier excess AUC `f₁(s) = 0.404 / (1 + 0.040 s)` evaluated at `s = log₁₀ n`. Analytical only — not used by the algorithm. |
| `gen.get_weights(n)` | `(float, float)` | `(α, β) = (residue_information(n), 1 − residue_information(n))` — exposed for callers who want to size their own algorithms by scale. |

### `NNAugmentedPrimeGenerator` — the NN-as-filter variant

```python
from nn_prime_generator import NNAugmentedPrimeGenerator
nn_gen = NNAugmentedPrimeGenerator(tau=0.5)
nn_gen.next_prime(10**6)   # exact: NN filter + deterministic verifier
```

Runs a trained MLP (loaded from `artifacts/model_s{3..8}.pt`, picking the closest-scale model for the input `n`) as a candidate filter; passes only candidates with `sigmoid(model(featurize(n))) ≥ tau` to the deterministic verifier. Output is exact regardless of NN performance, because the verifier guarantees it. Requires the NN to have been trained — run `train_nn_classifiers.py` first.

### `PureNNPrimeGenerator` — the NN-only variant (research baseline)

```python
from nn_prime_generator import PureNNPrimeGenerator
pure_gen = PureNNPrimeGenerator(tau=0.5)
pure_gen.next_prime(10**6)   # NOT exact: returns whatever the NN scores above tau
```

Same NN, no verifier. Returns whatever the NN classifies as prime; not a primality test on its own (recall `21–68 %` at `τ = 0.5`). Provided only to characterise *what the NN alone can do* in head-to-head comparisons; **do not use in production**.

---

## Reproducing every number in the papers

Each script is independent, idempotent, and seeded for bit-exact reproduction.

| Script | Time | Inputs | Outputs | Used for |
|---|---|---|---|---|
| `python prime_generator.py` | ~1 s | — | console (self-tests + perf smoke test) | Paper 2 §3, sanity check |
| `python verify_generator.py` | ~1 s | — | `artifacts/verify_generator.json` + console table | Paper 2 §3 audit (10 scales, 6 no-skip checks) |
| `python fit_meta_pattern.py` | ~22 s | — | `reports/fit_meta_pattern.md`, `artifacts/fit_meta_pattern.json` | Paper 3 §A (M1, M2, M3) |
| `python gap_analysis.py` | ~1 s | — | `reports/gap_analysis.md`, `artifacts/gap_analysis.json` | Paper 3 §B (Cramér, Chebyshev, density) |
| `python train_nn_classifiers.py` | ~25 s | — | `artifacts/data_s{3..8}.npz`, `model_s{3..8}.pt`, `history_s{3..8}.json`, `training_summary.json` | Paper 1 §1.4 (six trained MLPs) |
| `python analyze_nn_weights.py` | ~10 s | trained models | `reports/nn_weight_analysis.md`, `artifacts/weight_analysis.json` | Paper 1 §2 (SVD, Hill, integrated gradients) |
| `python extract_function.py` | ~5 s | trained models | `reports/nn_distillation.md`, `artifacts/distillation.json`, `distilled_*_s{3..8}.pkl` | Paper 1 §3 (decision-tree + L1-logistic distillation) |
| `python compare_methods.py` | ~20 s | trained models | `reports/nn_compare_methods.md`, `artifacts/compare_methods.json` | Paper 2 §5 (head-to-head benchmark) |

Run from inside the `Prime Number Generator/` directory. The recommended order is empirical → NN — all of the NN scripts assume `train_nn_classifiers.py` has been run:

```bash
cd "Prime Number Generator"
python fit_meta_pattern.py        # Paper 3 §A baseline (M1, M2, M3)
python gap_analysis.py            # Paper 3 §B (gap distribution + Chebyshev + density)
python train_nn_classifiers.py    # Paper 1   (six MLPs)
python analyze_nn_weights.py      # Paper 1   (weight statistics + scale fits)
python extract_function.py        # Paper 1   (decision-tree + L1-logistic distillation)
python compare_methods.py         # Paper 2   (conventional vs NN-augmented vs pure-NN)
python verify_generator.py        # audit
python prime_generator.py         # built-in self-tests
```

Total runtime end-to-end is under five minutes on a modern laptop CPU. All scripts are deterministic at fixed seeds (`SEED = 20260517 + scale * 1000`); rerunning produces bit-identical Markdown reports and JSON.

---

## The algorithm at a glance

```
                        ┌─────────────────────────────────┐
input n   ──────────►   │  6k±1 candidate enumerator      │   covers every prime > 3
                        │  (cuts candidate stream by 2/3) │
                        └─────────────┬───────────────────┘
                                      ▼
                        ┌─────────────────────────────────┐
                        │  Small-prime trial-division     │   size ≈ 15 · f₂(s)
                        │  pre-filter                     │   f₂(s) = 1.027/(1+0.030·s)
                        └─────────────┬───────────────────┘
                                      ▼
                        ┌─────────────────────────────────┐
                        │  Scale-adaptive verifier:       │
                        │   s < 4.5  → trial division     │
                        │   s small  → det. Miller–Rabin  │   Sorenson–Webster
                        │              with fixed witnesses│   (exact for n < 3.317·10²⁴)
                        │   s large  → prob. Miller–Rabin │   k = 20 → error ≤ 4⁻²⁰
                        └─────────────┬───────────────────┘
                                      ▼
                                 prime ≥ n
```

Three observations that make this structure right:

- **The `6k±1` enumerator** captures every prime `> 3` and skips two-thirds of integers; the algorithm starts here for free.
- **The small-prime filter** stays useful at every scale tested: `f₂(s) ≥ 0.82` over `s ∈ [1, 9]` (Paper 3 §A). The decision tree distilled from the trained MLP picks `is_6k_pm1`, `n mod 5, 7, 11, 13, 17, 19` as its top features at every scale (Paper 1 §3.3) — the network independently confirms the small-prime filter is the right choice.
- **The verifier is split by computational cost.** Below `s = 4.5` (`n ≈ 31,623`, `√n ≈ 178`), trial division is faster than Miller–Rabin. Above that bound, Sorenson–Webster's deterministic witness sets give exact primality at `O(s²)` per call up to `n < 3.317 × 10²⁴`. Above that, only probabilistic Miller–Rabin is feasible — `k = 20` rounds give per-call error `≤ 4⁻²⁰ ≈ 9 × 10⁻¹³`.

The `_PRIMALITY_TEST_SCALE_THRESHOLD = 4.5` constant is a **computational-cost** threshold, not a feature-importance crossover. The previous round of the project incorrectly claimed it was a "critical transition" between local-feature and global-density dominance; that claim has been retired (Paper 3 §C, `archive/README.md`).

---

## Performance

From `prime_generator.py`'s built-in performance smoke test:

| Scale | Start | Count | ms / prime |
|---|---|---|---|
| 10² | 100 | 20 | 0.004 |
| 10⁴ | 10,000 | 20 | 0.007 |
| 10⁶ | 1,000,000 | 20 | 0.012 |
| 10⁸ | 100,000,000 | 10 | 0.025 |
| 10¹⁰ | 10,000,000,000 | 5 | 0.055 |
| 10¹² | 1,000,000,000,000 | 5 | 0.062 |
| 10¹⁵ | 1,000,000,000,000,000 | 3 | 0.188 |

From the `compare_methods.py` head-to-head (`reports/nn_compare_methods.md`, 50 random starts × 5 consecutive primes each):

| Scale | Conventional | NN-augmented | Pure-NN | NN-aug / conv |
|---:|---:|---:|---:|---:|
| 3 | 0.006 ms | 0.469 ms | 0.291 ms | **82.8 ×** |
| 4 | 0.010 ms | 0.972 ms | 0.564 ms | **97.5 ×** |
| 5 | 0.019 ms | 1.307 ms | 0.581 ms | **67.1 ×** |
| 6 | 0.021 ms | 1.277 ms | 0.446 ms | **60.2 ×** |
| 7 | 0.024 ms | 2.022 ms | 0.585 ms | **84.4 ×** |
| 8 | 0.030 ms | 1.798 ms | 0.458 ms | **59.0 ×** |

The NN-augmented variant is dominated on every axis: slower wall-clock, no improvement in correctness (both produce only true primes; the verifier guarantees it), and the NN's accept-rate (49–56 %) is actually **higher** than the small-prime filter's (23–25 %), so it doesn't even reduce the number of candidates the verifier has to check.

The pure-NN variant has primality recall of `21–68 %` at `τ = 0.5` and skip-rate vs `sympy.nextprime` of `2–22 %`. It is not a primality test.

---

## Testing & verification

| Layer | Where | What it checks |
|---|---|---|
| Unit tests | `prime_generator.py::_self_test()` | Known small primes, the first 25 primes, deterministic witness sets at the bound boundaries, scale weights match the empirical fits, primality at `n = 10⁸ … 10¹⁵`. Also runs a performance smoke test. |
| Audit | `verify_generator.py` | At 10 scales (`100 → 10¹²`): runs `next_prime` on `15–50` consecutive starting points, cross-checks every output against `sympy.isprime` (all-prime check) and against `sympy.nextprime` for "no-skipping" (where computationally feasible). |
| Reproducibility | every script | Fixed RNG seed (`20260517` and `+scale*1000` for per-scale work). Outputs are bit-identical between runs. |

The current `verify_generator.py` audit shows **10 / 10 all-prime checks** and **6 / 6 no-skip checks** (at the four largest scales the no-skip cross-check is skipped because `sympy.nextprime` becomes the cost bottleneck rather than the generator).

---

## The headline findings

### Neural-network black-box analysis

1. **Top features identical at every scale.** Across all six trained MLPs, the dominant features (by both decision-tree importance and L1-logistic coefficient magnitude) are `is_6k_pm1` (importance ≈ 0.45–0.48), then `n mod 5` (≈ 0.20), `n mod 7` (≈ 0.13), `n mod 11`, `n mod 13`, `n mod 17`, `n mod 19`. Gradient descent rediscovered the small-prime trial-division sieve without ever being told it.

2. **Two clean exponential scaling laws on the trained weights.**
   - residue-feature attribution share: `0.543 · exp(−0.041 · s)` (RMSE_log = 0.079, AIC ≤ all alternatives)
   - binary-bit attribution magnitude: `2.226 · exp(+0.219 · s)`
   - Hill α on `fc1` SVD spectrum is essentially constant at `≈ 3.19` across scales.

### Independent non-NN baseline

3. **Filter rejection rate plateaus.** `f(s) = 1.027 / (1 + 0.030 s)` over `s ∈ [1, 9.5]` (40 scale samples, 1000 + 1000 primes / composites per scale). The rational form beats the power law by `ΔAIC = +30.78`; the filter never falls below `0.82` rejection rate on the tested range.

4. **Cramér's mean prediction holds.** Empirical `mean(gap) / ln n ∈ [0.97, 1.01]` over `s ∈ [1, 8]` (8 windows, 500–5000 consecutive primes per window). The strict-distributional claim is rejected at every scale (`p < 10⁻⁴`) — gaps are even and concentrated near multiples of 6, not memoryless — but the KS distance to `Exponential(ln n)` decays as `0.260 · exp(−0.084 · s)`, so the gap distribution becomes "less wrong" relative to exponential as `n` grows.

5. **Chebyshev's bias is empirically visible.** Counts `≡ 5 (mod 6)` exceed counts `≡ 1 (mod 6)` in 7 of 8 windows tested. Small in absolute terms, but consistently signed in the direction predicted in 1853. The NN study cannot see this because its `is_6k_pm1` feature collapses both classes.

### Operational consequence

6. **As a generator, the NN is dominated by the conventional method.**
   - Conventional `MetaPatternPrimeGenerator`: `0.006–0.030 ms/prime` across scales.
   - `NNAugmentedPrimeGenerator` (NN filter + deterministic verifier): `60–97 ×` slower; produces identical exact primes.
   - `PureNNPrimeGenerator` (NN scoring, no verifier, τ = 0.5): primality recall `21–68 %`, skip-rate vs ground truth `2–22 %` — not a usable primality test on its own.

### Honest interpretation

7. Neural networks do not "discover the formula for primes" because no such formula exists. What this study does demonstrate is that gradient-descent training on raw prime-classification supervision *recovers known sieve mathematics* (small-prime trial division on `6k±1` candidates), and that the recovery is robust across six orders of magnitude in `n`. The trained weights also display clean, non-trivial scaling behaviour for two specific feature-importance statistics — that is the empirical "meta-pattern". The independent non-NN study confirms the same structural conclusion via two completely different measurement pipelines.

---

## Limitations

What this project does **not** do, and is honest about not doing:

- **Does not produce a closed-form prime generator.** No such formula is known to exist; the project's "function discovered from the NN's weights" is the small-prime trial-division sieve, already-known mathematics rederived from data.
- **Does not improve on conventional speed.** The NN-augmented generator is `60–97 ×` slower than the hand-coded baseline at the scales tested. The conventional generator's per-prime cost grows as `O(ln² n)` (Cramér expectation × `O(s²)` Miller–Rabin), which is already optimal for asymptotically large `n` modulo log factors.
- **Does not provide an NN-only primality test.** Pure-NN recall at `τ = 0.5` is `21–68 %`. Sliding `τ` upward improves precision at the cost of recall but does not reach a useful regime; the trained MLPs are not primality tests.
- **Does not scale the NN study beyond `s = 8`.** `train_nn_classifiers.py`'s rejection sampling becomes expensive at `n > 10⁸`; the NN study uses six scales only. The non-NN baseline scales to `s = 9.5` (`n ≈ 3 × 10⁹`); the conventional generator scales to `n < 3.317 × 10²⁴` deterministically and unboundedly probabilistically.
- **Does not explore richer architectures.** A 3-layer MLP is large enough to overfit the residue features; a transformer or graph network on the integer's factor graph might give richer signal. We did not explore this.
- **Does not address the Riemann hypothesis or prime-gap conjectures.** The empirical gap study verifies Cramér's first-moment heuristic and visualises Chebyshev's bias, but does not advance the theory of either.

---

## License

AGPL-3.0 — see [`../LICENSE`](../LICENSE) at the repository root.
