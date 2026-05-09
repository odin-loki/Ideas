# Prime Number Generator — Scale-Dependent Meta-Pattern Theory

> **An empirical "meta-pattern" theory of primality in which local divisibility / 6k±1 effects and global PNT-style gap heuristics make different *scale-dependent* contributions to where the next prime is, with the two contributions crossing over at `n* ≈ 836` (`s* = log₁₀ n ≈ 2.92`) — derived from a fit of the form `α(s) = s^(−0.37)` and `β(s) = 1 − 0.487 · s^(−0.37)`, and operationalised into a hybrid `MetaPattern` algorithm with a Python implementation, a deterministic-vs-stochastic information-contribution analysis (`~96–98 %` deterministic vs `~2–4 %` stochastic), and a renormalisation-group-flavoured hypothesis that the `−0.37` exponent might be related to spectral exponents observed in neural networks (the paper labels this connection speculative).** The deliverables include a Miller–Rabin-based primality switch (`k = 20`, error bound `≤ 4⁻²⁰ ≈ 9 × 10⁻¹³`), an explicit complexity discussion (`O(√n · ln n)` local mode vs `O(log⁴ n)` global mode), and a measurement table showing densities tracking PNT to `100.2 %` at `~10⁷`.

---

## What this folder is

The Prime Number Theorem says that the density of primes near `n` is asymptotically `1 / ln n`. That is a global statement. Locally, divisibility filters (`6k ± 1`, sieving) eliminate most candidates with cheap arithmetic, and that is a local statement. Most prime-generation algorithms simply compose them — sieve-then-test — without modelling the *relative weight* of the two as a function of scale. This folder argues that the relative weight is itself an empirical regularity: at small `n` the local filter dominates; at large `n` the PNT regime takes over; and the crossover happens around `n ≈ 836`. The fit `α(s) = s^(−0.37)`, with `s = log₁₀ n`, parameterises the local contribution; `β(s) = 1 − 0.487 · s^(−0.37)` parameterises the global. The crossover comes from solving `1.487 · s^(−0.37) = 1`, giving `s* ≈ 2.92`, `n* ≈ 836`.

The work is honest about its empirical status: the exponent `−0.37` was fit from only a few scale samples (`s = 2, 5, 7`), and the renormalisation-group analogy is heuristic — there is no formal RG group action here. The neural-network connection (the same `−0.37` shows up in NN spectral exponents elsewhere in the repo) is flagged as speculative.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`Paper1_PrimeMetaPattern_Theory.md`](Paper1_PrimeMetaPattern_Theory.md) | Theory paper. Scale `s = log₁₀ n`, fitted forms `f_L(s) = 0.258 · exp(−0.373 s)` and `f_G(s) = 1 − 0.487 · exp(−0.371 s)` (exponents `−0.373 / −0.371` collapsed to `−0.37`). **Critical equality `1.487 · s^(−0.37) = 1 ⇒ s* ≈ 2.92 ⇒ n* ≈ 836`.** Table near `787…911` showing primes `839` etc. dominated by GLOBAL mode. **Filter effectiveness `10.7 % / 33.1 % / 51.4 %` at `~10² / 10⁵ / 10⁷`. Density vs PNT `103.2 % / 99.5 % / 100.2 %`.** **`~96–98 %` deterministic vs `~2–4 %` stochastic information contribution.** |
| [`Paper2_MetaPattern_Algorithm.md`](Paper2_MetaPattern_Algorithm.md) | Algorithm paper. **Miller–Rabin `k = 20`, error bound `≤ 4⁻²⁰ ≈ 9 × 10⁻¹³`.** Primality switch: `s < 4.5` → trial division; `s ≥ 4.5` → Miller–Rabin. Timing table on author hardware: `< 0.01 ms` at `n = 100` up to `~0.09 ms` at `10⁸`. Complexity: `O(√n · ln n)` local mode vs `O(log⁴ n)` global mode. |
| [`ALGORITHM_DERIVATION.md`](ALGORITHM_DERIVATION.md) | Derivation document. Repeats equations and benchmarks. |
| [`COMPLETE_PRIME_METAPATTERN_RESEARCH.md`](COMPLETE_PRIME_METAPATTERN_RESEARCH.md) | Combined research document. |
| [`prime_generator.py`](prime_generator.py) | Python reference implementation. |
| [`deep_transition_analysis.py`](deep_transition_analysis.py) | Transition-region analysis tool. |

---

## 🧠 The meta-pattern

```
Scale s = log₁₀ n

Local-filter weight    α(s) = s^(−0.37)            ──→ dominant at small s
Global-PNT weight       β(s) = 1 − 0.487·s^(−0.37)   ──→ dominant at large s

Critical scale          s*  ≈ 2.92                  ──→ n* ≈ 836
```

| Scale `n` | `α(s)` | `β(s)` | Mode | Filter effectiveness | Density / PNT |
|---|---|---|---|---|---|
| ~10² | dominant | weak | LOCAL | 10.7 % | 103.2 % |
| ~10⁵ | ~equal | ~equal | TRANSITION | 33.1 % | 99.5 % |
| ~10⁷ | weak | dominant | GLOBAL | 51.4 % | 100.2 % |

---

## ⚙️ The algorithm

```
Given n:
  s = log₁₀(n)
  if s < 4.5:
    use trial division up to √n        # O(√n · ln n)
  else:
    use Miller–Rabin with k = 20       # O(log⁴ n)
                                       # error ≤ 4⁻²⁰ ≈ 9 × 10⁻¹³
```

The switch threshold `s = 4.5` (`n ≈ 31 600`) is chosen to be *slightly above* the meta-pattern's critical scale `s* ≈ 2.92`, ensuring the algorithm is in the global-dominant regime when it makes the switch — a regime where Miller–Rabin's polylog cost is the right tool.

### Reported timings (author hardware, Paper 2 Table 1)

| `n` | Time |
|---|---|
| `10²` | `< 0.01 ms` |
| `10⁵` | `~0.02 ms` |
| `10⁷` | `~0.05 ms` |
| `10⁸` | `~0.09 ms` |

---

## 🚧 Honest caveats (Paper 1 §6.2, explicit)

- **Only a few scale samples (`s = 2, 5, 7`) were used to fit the exponent.** The `−0.37` is empirical, not derived from first principles.
- **Renormalisation-group analogy is heuristic.** "No formal RG group" is stated explicitly — it's a description, not a derivation.
- **Neural-network spectral-exponent `−0.37` connection is speculative.** The same exponent appears elsewhere in the repo (see [`../GF2 Algebra and Applications/paper7_synthesis.md`](../GF2%20Algebra%20and%20Applications/paper7_synthesis.md) and adjacent NN work) but the connection is flagged as a coincidence to investigate, not as established science.
- **Manuscript is labelled "Preliminary / empirical."**
- **Auxiliary outputs** (`transition_mechanics.png`, `deep_transition_analysis.json`) are referenced as expected-to-be-produced; their existence on disk is not guaranteed.

---

## 🎯 What this displaces

| Standard | What it lacks | What this work adds |
|---|---|---|
| Sieve of Eratosthenes | No primality test; static | Hybrid sieve + MR in scale-dependent mix |
| AKS / Miller–Rabin standalone | No local optimisation regime | Trial-division branch for small `n` |
| Heuristic `6k ± 1` filters | No global-regime pivot | Explicit `s*` crossover |
| Probabilistic primality | No theoretical framework | Deterministic vs stochastic information accounting |

---

## 🔗 Related work in this repo

- [`../General Math Papers/`](../General%20Math%20Papers/) — LCRP (the `O(log⁴ n)` MR cost is in the LCRP family)
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — `α` exponent shows up in Paper 7 GRIA-spectrum synthesis
- [`../Math Question Generator/`](../Math%20Question%20Generator/) — number-theory domain
- [`../RNGS/`](../RNGS/) — adjacent randomness questions
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — NMP `α ≈ 0.851` spectral exponent (different family, same neighbourhood)
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — primality for cryptographic key generation

---

[← Back to main README](../README.md)
