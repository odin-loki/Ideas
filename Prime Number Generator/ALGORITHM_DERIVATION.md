# Algorithm derivation — quick reference

> One-page derivation linking the empirical fits in `fit_meta_pattern.md` to the algorithm in `prime_generator.py`. The companion theory paper (`Paper1_PrimeMetaPattern_Theory.md`) explains the methodology; the companion algorithm paper (`Paper2_MetaPattern_Algorithm.md`) contains the full specification, correctness proofs, and benchmarks.

---

## 1. The three empirical curves

Three measurements were taken at `40` scale points `s = log₁₀ n ∈ [1.0, 9.5]`, with `1000 + 1000` balanced primes / composites per scale, and fit by maximum likelihood (log-target Gaussian errors) to three candidate functional forms. Model selection was by AIC. Full tables in `fit_meta_pattern.md`.

| Curve | Quantity measured | Best fit | AIC ranking |
|---|---|---|---|
| **M1** | residue-classifier excess AUC | `0.404 / (1 + 0.040·s)` | rational ≈ exponential ≈ power law (`\|ΔAIC\| < 1.5`) |
| **M2** | small-prime filter rejection rate | `1.027 / (1 + 0.030·s)` | rational > exponential > **power law (rejected, ΔAIC = +30.8)** |
| **M3** | PNT density relative error | `0.505 · s^(-1.88)` | power law > exponential |

---

## 2. What the fits mean operationally

### M2: the local filter is useful at every tested scale

```
  s        f_M2(s)        rejection rate of small-prime trial-division pre-filter
  1        0.997          almost every composite has a small prime factor
  3        0.942          most composites still caught
  5        0.892          slow plateau begins
  9        0.834          still useful
  20       0.642          still worth running (asymptote of fit)
```

Therefore the algorithm runs the small-prime pre-filter at every scale.

### M1: residue features carry roughly constant information

```
  s        f_M1(s)
  1        0.389          residue features distinguish primes from composites
  5        0.337          slightly less informative at large n, but still strong
  9        0.297
```

Statistically indistinguishable across the three candidate forms. We use the rational form for consistency with M2.

### M3: PNT is reliable above `s ≈ 4`

```
  s        f_M3(s)        relative error of 1/ln(n) density approximation
  1        0.505          ±50 %, density approximation poor
  4        0.044          ±4 %, accurate enough
  6        0.020          ±2 %, very accurate
```

Therefore *random*-prime generation (`random_prime_near`) using a Cramér exponential gap can be expected to behave correctly above `s ≈ 4` and is acceptable above `s ≈ 6`.

---

## 3. The single scale-adaptive choice

**M1, M2, M3 do not motivate any algorithmic crossover.** All three curves are monotone in `s` and do not cross any operationally meaningful threshold. The hybrid algorithm runs the same `6k±1` sieve plus small-prime pre-filter at every scale.

The **one** scale-dependent choice is the *primality verifier*, set by computational cost:

```
  s* = 4.5    (n* ≈ 31 623)

  s < s* :   trial division   O(√n)         deterministic
  s ≥ s* :   Miller–Rabin     O(k log³ n)
              n < 3.317 × 10²⁴   →  Sorenson–Webster witness sets    (deterministic, exact)
              n ≥ 3.317 × 10²⁴   →  k = 20 random witnesses          (probabilistic, ≤ 4⁻²⁰)
```

The threshold `s* = 4.5` is the scale at which `√n ≈ 178` — the empirical CPU crossover between trial division and Miller–Rabin on commodity 64-bit hardware.

---

## 4. The full algorithm in five lines

```
ALGORITHM next_prime(n):
    candidate    ← next_6k_pm1(n)
    num_checks   ← max(5, round(15 · 1.027 / (1 + 0.030 · log₁₀ n)))
    while True:
        if passes_pre_filter(candidate, num_checks) and is_prime(candidate):
            return candidate
        candidate ← step_6k_pm1(candidate)
```

with `is_prime` selecting trial division below `s* = 4.5`, deterministic-witness Miller–Rabin below `n = 3.317 × 10²⁴`, and probabilistic Miller–Rabin (`k = 20`) above. The full specification is in `Paper2_MetaPattern_Algorithm.md`; the implementation is `prime_generator.py`.

---

## 5. Correctness summary

| Range | Verifier | Correctness |
|---|---|---|
| `n < 31 623` | trial division | exact |
| `31 623 ≤ n < 3.317 × 10²⁴` | Sorenson–Webster Miller–Rabin | exact (deterministic witnesses) |
| `n ≥ 3.317 × 10²⁴` | Miller–Rabin (`k = 20` random) | error `≤ 4⁻²⁰ ≈ 9.1 × 10⁻¹³` per call |

The candidate stream visits every `6k±1` integer in order, never skipping. No prime greater than `3` is excluded a priori (all primes greater than `3` are `6k±1`).

---

## 6. Audit summary

`verify_generator.py` confirms across `10` scales `n = 2 … 10¹²`:

- `10 / 10` scales: every output is prime (verified by `sympy.isprime`).
- `6 / 6` scales (where verifiable): no primes are skipped (every output equals `sympy.nextprime(prev)`).
- Mean prime gap tracks `ln n` to within `< 1.5` at every scale.
- Per-prime wall-clock cost: `< 0.07 ms` up to `n = 10¹²`.

`prime_generator.py::_self_test` adds further checks at `n = 10¹⁵` (independent verification via `sympy.isprime` and `sympy.nextprime`), with per-prime cost `< 0.2 ms` at that scale.
