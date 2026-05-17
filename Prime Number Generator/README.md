# Prime Number Generator — discovering the prime-classification function from neural-network weights, and operationalising it

> **A black-box study of what a neural network *learns* when it is trained on prime-vs-composite classification, paired with a hybrid prime generator that operationalises the findings.**
>
> Six MLPs are trained at scales `s = log₁₀ n ∈ {3, 4, 5, 6, 7, 8}` on a deliberately rich, redundant 105-dimensional feature set (residues, binary bits, wheel structure, scale, digits). After training we never look at any source code; we only **measure the weights and gradients** to extract the function the network has learned. Across all six scales, the function distils — through both decision-tree and sparse-logistic surrogates — into the **small-prime trial-division sieve** (top features: `is_6k_pm1`, `n mod 5`, `n mod 7`, `n mod 11`, `n mod 13`, `n mod 17`, `n mod 19`). Gradient descent rediscovers the wheel sieve from raw classification supervision alone. The trained weights additionally exhibit two clean scaling laws: residue-feature attribution decays as `0.543 · exp(−0.041 · s)` while binary-feature attribution grows as `2.23 · exp(0.219 · s)`, consistent with the diminishing usefulness of small-prime divisibility at large `n`. The companion `MetaPatternPrimeGenerator` and `NNAugmentedPrimeGenerator` then ask: can the network *be* the generator? Direct head-to-head benchmarking shows the NN-augmented variant is **30–80× slower** than the hand-coded conventional variant despite producing identical exact output, and the pure-NN variant has primality recall of only `21–68 %`. The honest finding: **the NN is valuable as an analytical instrument that recovers known sieve mathematics from data, not as a faster prime-generation kernel.**

This folder is laid out as a small reproducible research project. Every number quoted in the papers comes from one of the scripts below; all artifacts are written under `artifacts/` and are gitignored.

---

## What's here

| File | What it is |
|---|---|
| [`Paper1_PrimeMetaPattern_Theory.md`](Paper1_PrimeMetaPattern_Theory.md) | Theory paper. Trains MLPs at six scales, performs black-box weight analysis (SVD spectra, Hill heavy-tail exponents, effective rank, Frobenius norms, integrated-gradient feature attribution by group), fits four functional forms (constant / power / exponential / rational) to every scalar weight statistic by maximum likelihood with AIC model selection, and distils each NN into a decision tree plus a sparse L1 logistic regression for human inspection of the learned rules. |
| [`Paper2_MetaPattern_Algorithm.md`](Paper2_MetaPattern_Algorithm.md) | Algorithm paper. Specifies three prime generators (conventional `MetaPatternPrimeGenerator`, `NNAugmentedPrimeGenerator`, `PureNNPrimeGenerator`), proves correctness of the conventional and NN-augmented variants via Sorenson–Webster deterministic Miller–Rabin (`exact for n < 3.317 × 10²⁴`) plus probabilistic fallback (`k = 20 rounds, error ≤ 4⁻²⁰`), and benchmarks all three head-to-head. |
| [`ALGORITHM_DERIVATION.md`](ALGORITHM_DERIVATION.md) | One-page reference linking every empirical fit (M1, M2, M3, NN scaling laws) to the algorithm structure it justifies. |
| [`COMPLETE_PRIME_METAPATTERN_RESEARCH.md`](COMPLETE_PRIME_METAPATTERN_RESEARCH.md) | Combined narrative — the intended single read-through. |
| [`prime_generator.py`](prime_generator.py) | Reference implementation of `MetaPatternPrimeGenerator`. Strictly correct `next_prime`, separate `random_prime_near` for cryptographic use, scale-adaptive primality verifier, deterministic-witness Miller–Rabin with arbitrary-precision-safe random fallback. |
| [`nn_prime_generator.py`](nn_prime_generator.py) | `NNAugmentedPrimeGenerator` (NN candidate filter + deterministic verifier; output is exact) and `PureNNPrimeGenerator` (NN scoring only; output bounded by NN error). |
| [`fit_meta_pattern.py`](fit_meta_pattern.py) | Baseline empirical study. At 40 scale samples × 1000 + 1000 balanced primes / composites per scale, measures three quantities and fits four functional forms to each by MLE + AIC. Independent of the NN study; used to size the small-prime filter in `MetaPatternPrimeGenerator`. |
| [`train_nn_classifiers.py`](train_nn_classifiers.py) | Trains the six MLPs (input → 128 → 64 → 32 → 1, ReLU + dropout, Adam, 50 epochs, batch 128, BCE loss) on a balanced 2000 + 2000 prime / composite dataset per scale. Saves data, weights, history. |
| [`analyze_nn_weights.py`](analyze_nn_weights.py) | Loads each trained model, computes per-layer SVD / norm / heavy-tail / effective-rank statistics and per-feature integrated gradients, then fits scaling laws to every scalar across scales. |
| [`extract_function.py`](extract_function.py) | Knowledge distillation: trains a depth-8 decision tree and an L1 logistic regression to mimic each MLP, reports fidelity to the NN, top features, and tree rules. |
| [`compare_methods.py`](compare_methods.py) | Head-to-head benchmark of conventional, NN-augmented, and pure-NN generators at every trained scale (50 starting points × 5 primes each). |
| [`verify_generator.py`](verify_generator.py) | End-to-end audit of `MetaPatternPrimeGenerator`: 10 / 10 all-prime correctness, 6 / 6 no-skip correctness up to `n = 10⁶`, all-prime correctness verified up to `n = 10¹⁵`. |
| [`fit_meta_pattern.md`](fit_meta_pattern.md) | Human-readable report from `fit_meta_pattern.py`. |
| `artifacts/` | All generated outputs (gitignored): trained models, JSON measurements, Markdown reports. |

---

## Reproducing every number in the papers

```bash
pip install numpy scipy scikit-learn sympy torch

python fit_meta_pattern.py        # baseline empirical fits  (M1, M2, M3)
python train_nn_classifiers.py    # six MLPs (≈ 25 s on CPU)
python analyze_nn_weights.py      # weight statistics + scale fits
python extract_function.py        # tree + sparse-logistic distillation
python compare_methods.py         # conventional vs NN-augmented vs pure-NN
python verify_generator.py        # end-to-end correctness audit
python prime_generator.py         # built-in self-tests
```

Total run-time on a modern laptop CPU is under five minutes. Every Markdown report under `artifacts/` is regenerated each time; every JSON contains the raw measurements.

---

## The headline findings

1. **Top features identical at every scale.** Across all six trained MLPs, the dominant features (by both decision-tree importance and L1-logistic coefficient magnitude) are `is_6k_pm1` (importance ≈ 0.45–0.48), then `n mod 5` (≈ 0.20), `n mod 7` (≈ 0.13), `n mod 11`, `n mod 13`, `n mod 17`, `n mod 19`. The network rediscovered the small-prime trial-division sieve without ever being told it.

2. **Two clean scaling laws in the trained weights.**
   - residue-feature attribution share: `0.543 · exp(−0.041 · s)` (RMSE_log = 0.079, AIC ≤ all alternatives)
   - binary-bit-feature attribution share: `0.077 / (1 + (−0.084) s)` rational fit; absolute attribution grows exponentially `2.23 · exp(0.219 · s)`
   - Both are consistent with the well-known fact that small-prime divisibility carries less information at large `n` (small factors become rarer); the NN reallocates attention accordingly.

3. **Constant heavy-tail spectra.** Hill exponent α on the upper half of the singular-value distribution of `fc1` is `3.19 + ε(s)` with ε(s) negligible across scales (RMSE_log = 0.007). Effective rank, stable rank, Frobenius norm — all essentially constant.

4. **As a generator, the NN is dominated by the conventional method.**
   - Conventional `MetaPatternPrimeGenerator`: `0.006–0.030 ms/prime` across scales.
   - `NNAugmentedPrimeGenerator` (NN filter + deterministic verifier): `30–80 ×` slower; produces identical exact primes.
   - `PureNNPrimeGenerator` (NN scoring, no verifier, τ = 0.5): primality recall `21–68 %`, skip-rate vs ground truth `2–22 %` — not a usable primality test on its own.

5. **Honest interpretation.** Neural networks do not "discover the formula for primes" because no such formula exists. What this study does demonstrate is that gradient-descent training on raw prime-classification supervision *recovers known sieve mathematics* (small-prime trial division on `6k±1` candidates), and that the recovery is robust across six orders of magnitude in `n`. The trained weights also display clean, non-trivial scaling behaviour for two specific feature-importance statistics — that is the empirical "meta-pattern".

---

## License

AGPL-3.0 — see [`../LICENSE`](../LICENSE) at the repository root.
