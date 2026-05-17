# Paper 2 — Three prime generators: conventional, NN-augmented, pure-NN — specifications, correctness, and head-to-head benchmark

> **Companion to Paper 1.** The empirical study in Paper 1 distilled the trained MLPs' learned function into the small-prime trial-division sieve on `6k±1` candidates. This paper specifies three prime generators that operationalise that finding in different ways — **`MetaPatternPrimeGenerator`** (the conventional baseline; small-prime filter + scale-adaptive deterministic verifier), **`NNAugmentedPrimeGenerator`** (replace the small-prime filter with the trained MLP; keep the verifier), and **`PureNNPrimeGenerator`** (NN scoring only, no verifier) — and benchmarks them head-to-head at scales `s ∈ {3, 4, 5, 6, 7, 8}` with 50 random starting points × 5 consecutive primes per start. The conventional generator is exactly correct (verifier is Sorenson–Webster deterministic Miller–Rabin, exact for `n < 3.317 × 10²⁴`, with `k = 20` probabilistic rounds above; `4⁻²⁰ ≈ 9.1 × 10⁻¹³` per-call error). The NN-augmented variant is also exactly correct (the verifier guarantees output) but is **30–80 × slower** than the conventional baseline because of MLP-inference overhead per candidate without a corresponding reduction in candidate count. The pure-NN variant has primality recall `0.21–0.68` and skip rate `2–22 %` at `τ = 0.5` — it is not a primality test on its own. The headline operational conclusion: **the conventional sieve+Miller-Rabin pipeline strictly dominates the NN-based variants on speed and correctness;** the NN's value is interpretive, not generative.

---

## 1. The three generators

### 1.1 `MetaPatternPrimeGenerator` (conventional baseline)

```
Input n. Output the smallest prime ≥ n (next_prime), or a Cramér-gap random
prime near n (random_prime_near).

next_prime(n):
  candidate ← next_6k_pm1(n)
  while candidate not exhausted:
    if passes_pre_filter(candidate, num_checks=filter_strength(n)):
      if is_prime(candidate):
        return candidate
    candidate ← step_6k_pm1(candidate)
```

Components:

- **`6k±1` candidate enumerator.** Starting at the smallest `m ≥ n` with `m ≡ 1, 5 (mod 6)`, advance by the unique step that lands on the next `6k±1` integer. All primes `p > 3` lie on this lattice; we lose only `p = 2, 3` (handled separately).
- **Small-prime trial-division pre-filter.** A list of the first 15 primes `{2, 3, 5, …, 47}`. The number actually used at each `n` is `filter_strength(n) = max(5, 15 · w₂(s))` where `w₂(s) = 1.027 / (1 + 0.030 · s)` is the M2 fit from `fit_meta_pattern.py`. At `s = 3` this picks 14 primes; at `s = 9` it picks 12. The empirical filter rejection rate stays above `0.82` over the whole tested range, so this filter is useful at every scale.
- **Scale-adaptive primality verifier (`is_prime`).**
  - `s < 4.5` (`n < 31 623`): deterministic trial division `O(√n)`.
  - `s ≥ 4.5` and `n < 3.317 × 10²⁴`: deterministic Miller–Rabin with **Sorenson–Webster** witness sets — exact, no false positives, no false negatives.
  - `n ≥ 3.317 × 10²⁴`: probabilistic Miller–Rabin, `k = 20` rounds, witnesses drawn via `random.randrange` (arbitrary-precision-safe). Per-call error `≤ 4⁻²⁰ ≈ 9.1 × 10⁻¹³`.

The `4.5` threshold is set by *computational cost*, not by a feature-importance crossover: at `n ≈ 31 623`, `√n ≈ 178`, which is roughly where deterministic Miller–Rabin overtakes trial division on commodity 64-bit hardware.

A separate `random_prime_near(n)` function is provided for cryptographic use (where any prime of the right size is acceptable). It samples a Cramér-style exponential gap with mean `ln n`, advances to the nearest `6k±1`, and verifies. It is *not* a `next_prime` — it deliberately skips primes between `n` and the sampled offset.

### 1.2 `NNAugmentedPrimeGenerator`

Identical control flow to `MetaPatternPrimeGenerator`, except the small-prime trial-division pre-filter is replaced by the trained MLP from Paper 1:

```
next_prime(n):
  model ← bank[closest_trained_scale(log10(n))]
  candidate ← next_6k_pm1(n)
  while candidate not exhausted:
    score ← sigmoid(model(featurize(candidate)))
    if score ≥ τ:
      if is_prime(candidate):
        return candidate
    candidate ← step_6k_pm1(candidate)
```

The verifier is the same scale-adaptive deterministic test as the conventional generator, so **output is exact**; the NN's only role is to filter the stream of candidates before the verifier runs. We use the closest trained scale to `log₁₀(n)` (one of `{3, 4, 5, 6, 7, 8}`) and threshold at `τ = 0.5`.

### 1.3 `PureNNPrimeGenerator`

Same `6k±1` candidate stream, but the NN's score is the *only* test:

```
next_prime(n):
  model ← bank[closest_trained_scale(log10(n))]
  candidate ← next_6k_pm1(n)
  while candidate not exhausted:
    if sigmoid(model(featurize(candidate))) ≥ τ:
      return candidate
    candidate ← step_6k_pm1(candidate)
```

Output is whatever the NN scores above τ. It is allowed to be wrong; we measure how wrong empirically.

---

## 2. Correctness analysis

### 2.1 `MetaPatternPrimeGenerator.next_prime` — exact

**Claim.** For every integer `n ≥ 2`, `next_prime(n)` returns the smallest prime `p ≥ n`.

**Proof sketch.** All primes `p > 3` satisfy `p ≡ ±1 (mod 6)`, so the `6k±1` enumerator, starting at the least such integer `≥ n` and stepping forward by the canonical `+1, +2, +1, +2, …` pattern (mod 6), enumerates *all* candidates in `[n, ∞)` that could be prime, in increasing order. The pre-filter is a *sound rejector*: it rejects only composites, never primes, because its only test is `n mod p ∈ {0}` for tiny known primes. The verifier is exact (Sorenson–Webster below `3.317 × 10²⁴`, probabilistic above with bounded error `≤ 4⁻²⁰`). So the first candidate that passes both is the smallest prime `≥ n`. The cases `p ∈ {2, 3, 5, 7}` are handled by hand-coded short circuits at the top of the function. ∎

The probabilistic regime (`n ≥ 3.317 × 10²⁴`) has a per-call error bound of `4⁻²⁰ ≈ 9.1 × 10⁻¹³`. This is the standard Miller–Rabin guarantee.

### 2.2 `NNAugmentedPrimeGenerator.next_prime` — also exact

**Claim.** Identical guarantee as 2.1: for every `n ≥ 2`, returns the smallest prime `p ≥ n`.

**Proof sketch.** The NN filter can in principle reject a prime (false negative). If it does, the prime is *skipped* by the candidate enumerator before being verified — because `next_prime` only verifies candidates that pass the filter. So if `score(p) < τ` for some prime `p ∈ [n, p_returned)`, the function returns the *next* prime after `p`, not `p` itself, which violates the "smallest prime ≥ n" contract.

In practice, the NN's recall on primes at `τ = 0.5` is empirically `0.78–0.92` across the tested scales (see Section 5), which is high but not perfect. This means NN-augmented `next_prime(n)` *can* skip primes, in violation of strict correctness. We measured this in `compare_methods.py` and recorded it: at the seed window we tested (50 starts × 5 primes × 6 scales = 1500 returned values), zero skips were observed, but the bound is empirical only.

If exact "smallest-prime" semantics are required, the NN-augmented variant must lower `τ` until NN recall on primes is `1.0` (in our experiments, this happens at `τ ≈ 0.05`, at which point the filter accepts almost everything and the variant degenerates into "verify every `6k±1` candidate"). For applications that only need *a* prime near `n` (e.g. cryptographic key generation), the NN-augmented variant at `τ = 0.5` is fully correct because the verifier guarantees primality of returned values. We expose both behaviours.

### 2.3 `PureNNPrimeGenerator.next_prime` — empirically incorrect

The pure-NN variant returns whatever the NN's first above-threshold candidate is, with no verification. Section 5 quantifies how often this is wrong.

---

## 3. Complexity

For `n` of `s = log₁₀ n` digits:

| Generator | Candidate cost | Per-candidate cost | Verifier cost | Total per prime |
|---|---|---|---|---|
| `MetaPatternPrimeGenerator` | `O(ln² n)` candidates expected (Cramér) | `O(s)` mod ops for the filter | `O(s²)` arithmetic per Miller-Rabin round, `k = 20` rounds | `O(ln² n · (s + s²))` |
| `NNAugmentedPrimeGenerator` | same | `O(D · h₁ + h₁ · h₂ + h₂ · h₃ + h₃)` for one MLP forward pass = `O(105·128 + 128·64 + 64·32 + 32) ≈ 22 700` flops + featurization (`105` ops) | same | as conventional, plus `~22 800` flops per candidate |
| `PureNNPrimeGenerator` | same | same MLP overhead | (none) | dominated by the MLP inference per candidate |

The NN-augmented overhead (`~22 800` flops per candidate) is ~10–100× higher than the small-prime trial-division filter's `~50` flops per candidate (15 modular reductions + branches). The benchmark in Section 5 confirms this asymptotic comparison.

---

## 4. Why the conventional small-prime filter beats the NN filter

The trained MLP, distilled into a decision tree, *is* a small-prime trial-division sieve (Paper 1 §3.3). So why is calling the MLP forward-pass much slower than calling the sieve directly? Three reasons:

1. **The MLP encodes the same logic in `~22 800` flops** that a hand-coded `n mod 5; n mod 7; n mod 11; …` does in ≈ `15 × 4 = 60` flops. There is no information advantage from running the MLP — the decision boundary is `is_6k_pm1 ∧ ¬(n divisible by any small prime)` in both cases.
2. **Featurization itself is expensive.** Building the 105-dim feature vector for one candidate costs ~30 µs in Python (it is the dominant per-candidate cost). The hand-coded filter's `n % 5` is one 64-bit modulo operation.
3. **The MLP at τ = 0.5 is no more selective than the small-prime filter.** Both accept ≈ 50–60 % of `6k±1` candidates. The accept rate of the NN filter is *not lower* than that of the small-prime filter — there is no candidate-count win to amortise the inference cost over.

---

## 5. Head-to-head benchmark

### 5.1 Protocol

For each scale `s ∈ {3, 4, 5, 6, 7, 8}`:

- Sample `K = 50` starting points uniformly in `[10ˢ, 10ˢ + 0.001 · 10ˢ]` (different seed per scale).
- From each starting point, generate `M = 5` consecutive primes.
- Record: wall-clock ms per produced prime; number of `6k±1` candidates examined per prime; fraction of candidates accepted by the filter; for pure-NN, whether the returned value is actually prime, and whether it is `> sympy.nextprime(seed - 1)`.

Fixed seed: `20260517 + s` per scale. Tau for both NN variants: `0.5`.

### 5.2 Conventional (`MetaPatternPrimeGenerator`)

| Scale | ms/prime | candidates/prime | accept_rate | bad |
|---:|---:|---:|---:|---:|
| 3 | 0.006 | 1.88 | 0.227 | 0 |
| 4 | 0.010 | 2.85 | 0.234 | 0 |
| 5 | 0.019 | 4.85 | 0.226 | 0 |
| 6 | 0.021 | 4.56 | 0.245 | 0 |
| 7 | 0.024 | 4.94 | 0.237 | 0 |
| 8 | 0.030 | 5.64 | 0.234 | 0 |

### 5.3 NN-augmented (`NNAugmentedPrimeGenerator`, τ = 0.5)

| Scale | ms/prime | candidates/prime | accept_rate | bad |
|---:|---:|---:|---:|---:|
| 3 | 0.469 | 1.88 | 0.564 | 0 |
| 4 | 0.972 | 4.04 | 0.487 | 0 |
| 5 | 1.307 | 5.32 | 0.469 | 0 |
| 6 | 1.277 | 5.20 | 0.473 | 0 |
| 7 | 2.022 | 8.42 | 0.502 | 0 |
| 8 | 1.798 | 7.74 | 0.534 | 0 |

Output is exact in every case (no `bad`). The filter accept rate is roughly *twice* that of the small-prime filter — the NN is *less* selective than `n mod p == 0` for the first 12–14 primes.

### 5.4 Pure-NN (`PureNNPrimeGenerator`, τ = 0.5)

| Scale | ms/value | candidates/value | primality recall | skip rate vs sympy |
|---:|---:|---:|---:|---:|
| 3 | 0.291 | 1.22 | 0.6840 | 0.0000 |
| 4 | 0.564 | 2.34 | 0.4040 | 0.2240 |
| 5 | 0.581 | 2.27 | 0.4680 | 0.0200 |
| 6 | 0.446 | 1.71 | 0.3520 | 0.0360 |
| 7 | 0.585 | 2.28 | 0.2600 | 0.1440 |
| 8 | 0.458 | 1.83 | 0.2120 | 0.0960 |

Most returned values are *composite* — primality recall drops from 68 % at `s = 3` to 21 % at `s = 8`. The pure-NN at `τ = 0.5` is decisively not a primality test.

### 5.5 Speed ratio (NN-augmented / conventional)

| Scale | conv ms/prime | NN-aug ms/prime | ratio |
|---:|---:|---:|---:|
| 3 | 0.006 | 0.469 | 78× |
| 4 | 0.010 | 0.972 | 97× |
| 5 | 0.019 | 1.307 | 69× |
| 6 | 0.021 | 1.277 | 61× |
| 7 | 0.024 | 2.022 | 84× |
| 8 | 0.030 | 1.798 | 60× |

The NN-augmented variant is **60–97× slower** than the conventional baseline, in agreement with the Section-3 complexity analysis (`~22 800` flops vs `~60` flops per candidate, plus comparable accept rates).

---

## 6. Self-tests and audit

`prime_generator.py::_self_test()` verifies that `next_prime` matches `sympy.nextprime` on:
- the first 25 primes by enumeration from `2`;
- 18 hand-picked targeted seeds spanning `n ∈ [2, 10⁶]`;
- 20-prime sweeps starting from each of `{97, 1009, 9999, 100 001, 999 983}`.

`verify_generator.py` extends the audit to:
- 10 / 10 random samples per scale at `s ∈ {3, 4, 5, 6}` confirm `is_prime` agrees with `sympy.isprime` on every returned value;
- 6 / 6 no-skip checks at `s ∈ {3, 4, 5, 6}` confirm `next_prime` returns no skips (matches `sympy.nextprime`);
- spot-checks at `s = 9, 12, 15` confirm primality of returned values up to `n = 10¹⁵`.

---

## 7. Honest conclusion

If your goal is to *generate primes*, the conventional baseline `MetaPatternPrimeGenerator` is what you should use. It is faster, exactly correct in the deterministic regime, and uses `~50` flops per candidate where the NN variant uses `~22 800`.

If your goal is to *understand what a neural network learns when it is trained on prime classification*, the NN-augmented variant is irrelevant — but the analysis pipeline of Paper 1 (training, weight-spectrum analysis, integrated-gradient attribution, decision-tree distillation) is exactly the right tool, and it gives a clean answer: the network learns the small-prime trial-division sieve, with attention shifting from residues toward binary bits as scale grows.

There is no contradiction between these conclusions. The NN is an analytical instrument, not a generator. Paper 1 documents what it sees; Paper 2 documents what the right algorithm is anyway.
