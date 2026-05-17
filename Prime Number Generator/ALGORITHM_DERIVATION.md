# Algorithm derivation — one-page reference

A compact map from the empirical findings of Paper 1 to the structure of the three generators specified in Paper 2.

---

## Empirical inputs

| Source | Measurement | Best fit | Used for |
|---|---|---|---|
| `fit_meta_pattern.py` (M1) | residue-classifier excess AUC | rational `0.404 / (1 + 0.040 s)` | not used by algorithm; analysis only |
| `fit_meta_pattern.py` (M2) | small-prime filter rejection rate | rational `1.027 / (1 + 0.030 s)` | sets `filter_strength(n)` in `MetaPatternPrimeGenerator` |
| `fit_meta_pattern.py` (M3) | PNT density relative error | power `0.505 · s^(−1.881)` | sanity check; not used |
| `analyze_nn_weights.py` | residue-attribution share | exponential `0.543 · exp(−0.041 s)` | confirms M1 via independent route |
| `analyze_nn_weights.py` | binary-attribution magnitude | exponential `2.226 · exp(+0.219 s)` | analytical only |
| `analyze_nn_weights.py` | Hill α on `fc1` SVD | rational `3.194 / (1 − 0.0056 s)` | confirms heavy-tailed self-regularisation |
| `extract_function.py` | distilled tree top features | `is_6k_pm1`, `res_5`, `res_7`, `res_11`, `res_13`, `res_17`, `res_19` at every scale | confirms small-prime sieve as the right structural family |

---

## Algorithm structure

```
6k±1 candidate enumerator
        │
        ▼
[ filter ]   ← chosen variant
        │
        ▼
[ verifier ] ← scale-adaptive deterministic primality test
        │
        ▼
return candidate
```

The three variants differ only in the **filter**; the candidate enumerator and the verifier are shared.

| Generator | Filter | Verifier | Output |
|---|---|---|---|
| `MetaPatternPrimeGenerator` | small-prime trial division (first `15 · w₂(s)` primes; `w₂(s) = 1.027 / (1 + 0.030 s)` from M2) | trial division below `s = 4.5`, Sorenson–Webster Miller–Rabin up to `n < 3.317 × 10²⁴`, probabilistic (`k = 20`) above | exact for `n < 3.317 × 10²⁴`; `≤ 4⁻²⁰` per-call error above |
| `NNAugmentedPrimeGenerator` | trained MLP at closest scale; threshold `τ` on `sigmoid(model(featurize(n)))` | same as above | exact (verifier guarantees output) |
| `PureNNPrimeGenerator` | (none) | trained MLP at closest scale; threshold `τ` | bounded by NN error (recall 21–68 % at `τ = 0.5`) |

---

## Why this exact structure

1. **`6k±1` enumerator.** Every prime `> 3` lies on this lattice; enumerating it (rather than every integer) cuts candidate count by `2/3`.
2. **Filter.** Both M2 (rejection rate) and the trained MLP's distilled rule say the small-prime trial-division test is the right cheap pre-filter. The MLP variant is included to test whether the network *as such* offers any operational advantage; Paper 2 §5 shows it does not.
3. **Scale-adaptive verifier.**
   - Below `s = 4.5`: `√n ≤ 178`, trial division beats Miller–Rabin.
   - `4.5 ≤ s ≤ 24.5`: deterministic Miller–Rabin with Sorenson–Webster (2017) witness sets gives *exact* primality at `O(s²)` per call.
   - Above `s = 24.5`: probabilistic Miller–Rabin with `k = 20` rounds; per-call error `≤ 4⁻²⁰ ≈ 9.1 × 10⁻¹³`.
4. **Witness draws are `random.randrange`.** This avoids the `int32` overflow that bites `numpy.random.randint(2, n - 1)` for `n ≥ 2³¹`.

---

## What the NN study did *not* change

- The conventional generator's structure was fixed by `fit_meta_pattern.py` before the NN study began. Paper 1's distillation independently confirmed that structure is the right one. The NN study produced no new constants for the conventional algorithm.
- The deterministic-witness fast path (Sorenson–Webster) was integrated independently of the NN; it gives exact primality up to `n < 3.317 × 10²⁴` regardless of any ML choices.
- The strict `next_prime` semantics (no skipping) and the separate `random_prime_near` (Cramér-gap, for crypto) come from straightforward number-theoretic argument and are independent of the NN.

---

## What the NN study *did* add

- Two clean exponential scaling laws on the trained weights (residue and binary attribution shares).
- A crisp empirical demonstration that an MLP, given a redundant feature set and only classification supervision, recovers the small-prime sieve via gradient descent — and a quantitative cost-of-using-it as a generator (60–97× slower than the hand-coded baseline).
- A specification and benchmark of the `NNAugmentedPrimeGenerator` and `PureNNPrimeGenerator` variants, enabling reproducible head-to-head comparisons.
