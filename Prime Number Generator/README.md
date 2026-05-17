# Prime Number Generator — empirically-grounded hybrid prime sieve + scale-adaptive primality test

> **An empirical study and a working prime generator built around the question "how does the relative usefulness of *local* divisibility filters and *global* PNT-style density heuristics change with scale `s = log₁₀ n`?". Originally claimed a `s^(-0.37)` power law and a "critical transition" at `n* ≈ 836`; on re-examination with `31` scale samples (instead of the original `3`) those specific claims do not hold up — the actual fits are dominated by the rational form `f(s) = 1.050 / (1 + 0.034 · s)` for the filter rejection rate (`ΔAIC = +17.5` vs power law) and the residue-classifier excess-AUC curve is roughly flat (`~0.30 ± 0.04`) across `s = 1 … 9` with power-law and exponential indistinguishable (`|ΔAIC| < 1`). What survives is a hybrid algorithm — a strict `6k±1` candidate sieve, a small-prime trial-division pre-filter, and a scale-adaptive primality test (deterministic trial division below `n ≈ 31 623`, deterministic Miller–Rabin witness sets up to `~3.3 × 10²⁴`, and probabilistic Miller–Rabin above that) — that is genuinely correct, has clean `O(√n · ln n)` and `O(log⁴ n)` complexity branches, and stays correct up to at least `n = 10¹⁵` in the audit. This README documents both the original claims and the corrections after a complete re-run, and the codebase is now self-consistent and unit-tested.**

---

## What this folder is

The Prime Number Theorem (PNT) gives a *global* asymptotic — primes near `n` are spaced about `ln n` apart. Divisibility tricks like `6k±1` and small-prime trial division are *local* — they cheaply reject composites that share a small factor. Most prime generators just compose them: sieve, then primality-test. The original write-up in this folder went further and asked: as a function of scale, what is the *relative* contribution of the local layer to the generation problem? Three measurements were claimed (filter effectiveness, density accuracy, residue-classifier importance) at three scale points (`s ∈ {2, 5, 7}`), the result was reported as a power law `α(s) = s^(-0.37)`, and a "critical transition" at `n* ≈ 836` was derived from the algebraic crossing `α = β` of two assumed forms. An external review correctly pointed out that with three scale points one cannot distinguish a power law from an exponential, and that the paper text reported the fit in *exponential* form (`0.258 · exp(-0.373 · s)`) while the algorithm code used *power-law* form (`s ** -0.37`) — values that disagree by a factor of ~6 at `s = 2`.

The folder has now been re-run with a proper experiment (`fit_meta_pattern.py`):

- **31 scale samples**, `s = 1.0, 1.25, 1.5, …, 8.0, 8.5, 9.0`
- **600 prime + 600 composite samples per scale**, balanced by rejection sampling
- **Three independent measurements**: residue-classifier excess AUC (M1), small-prime filter rejection rate (M2), PNT density relative error (M3)
- **Three candidate forms fit by maximum likelihood** (Gaussian on log-target, equivalent to log-least-squares): power law `A · s^(-γ)`, exponential `A · exp(-b · s)`, rational `A / (1 + B · s)`
- **Model selection by AIC and BIC**

The verdict, in [`fit_meta_pattern.md`](fit_meta_pattern.md):

| Curve | Best fit | Power-law fit | Exponential fit | Verdict |
|---|---|---|---|---|
| **M1** residue-classifier excess AUC | `0.391 · s^(-0.104)` (`AIC = -80.19`) | same | `0.382 · exp(-0.026·s)` (`AIC = -79.28`) | indistinguishable, `|ΔAIC| < 1` |
| **M2** filter rejection rate | `1.050 / (1 + 0.034·s)` (`AIC = -158.10`) | `1.057 · s^(-0.111)` (`AIC = -138.72`) | `1.040 · exp(-0.029·s)` (`AIC = -156.19`) | rational best; **power law strongly rejected**, `ΔAIC = +19.4` |
| **M3** PNT density rel. error | `0.660 · s^(-2.13)` | same | `0.345 · exp(-0.50·s)` | power law preferred but very noisy |

The original `−0.37` exponent is **not reproduced** at any of the 31 scale points: the actual measured exponent for M1 is `~ -0.10`, off by a factor of ~3.5×. The supposed coincidence with the `~ -0.37` power-law exponent in the singular-value spectra of trained neural-network weight matrices (Martin & Mahoney, 2021) is therefore an artefact of the original three-point fit; with proper sampling there is no numerical coincidence to interpret.

The "critical transition at `n* ≈ 836`" is also an artefact: it was derived from solving `1.487 · s^(-0.37) = 1`, with both the exponent and the algebraic form set by the bad fit. With the correct M2 fit, the filter rejection rate is monotonically slowly declining and **does not cross any threshold** — at `n = 10⁹` it is still `~0.83`, meaning the local filter is useful at every scale tested. There is no scale at which the algorithm "should switch" from local to global mode based on feature importance. The only switch that has any operational basis is the **primality-test cost crossover**: trial-division `O(√n)` overtakes Miller–Rabin `O(k log³ n)` near `n ≈ 31 623` (`s ≈ 4.5`), and *that* threshold is purely about CPU cost, not about prime structure.

What survives is a fully working, correctly verified, scale-adaptive prime generator with honest performance numbers. The v1 generator was also broken in two ways unrelated to the fitting issue, both fixed:

1. **`next_prime` skipped primes** at every scale beyond the artefactual `n* ≈ 836`, because in "global-dominant" mode it sampled a random `Exponential(ln n)` gap and jumped past intermediate primes. (At `n = 1009` it returned `1031`, skipping `1013, 1019, 1021`.) The corrected version is a strict "smallest prime ≥ n" sieve and is unit-tested for no-skipping over 20-prime sweeps from five seed scales.
2. **`miller_rabin` overflowed at `n ≥ 2³¹`** because it used `np.random.randint(2, n-1)` (int32). Witness draws now use Python's arbitrary-precision `random.randrange`, and there is a deterministic-witness fast path for all `n < 3.317 × 10²⁴` using the Sorenson–Webster witness sets.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`README.md`](README.md) | This file — corrected story. |
| [`prime_generator.py`](prime_generator.py) | Corrected v2 generator. Strict `next_prime`, arbitrary-precision Miller–Rabin, deterministic witness sets up to `~3.3 × 10²⁴`, empirically-fit weights. Has a `_self_test()` that asserts (a) first 25 primes match the textbook list, (b) `next_prime` correct on 17 hand-picked seeds, (c) no-skipping over 20-prime sweeps from 5 seeds, (d) correct at `n = 10⁸, 10¹⁰, 10¹², 10¹⁵`. |
| [`fit_meta_pattern.py`](fit_meta_pattern.py) | The MLE refit experiment — 31 scale samples, 600+600 balanced primes/composites per scale, three measurements, three forms, AIC/BIC model selection. |
| [`fit_meta_pattern.json`](fit_meta_pattern.json) | Raw measurements + all fitted parameters, std errors, log-likelihoods. |
| [`fit_meta_pattern.md`](fit_meta_pattern.md) | Human-readable refit report. |
| [`verify_generator.py`](verify_generator.py) | End-to-end audit: generates primes at 10 scales (up to `n = 10¹²`), independently verifies every output is prime via `sympy.isprime`, verifies no-skipping via `sympy.nextprime` where tractable, reports timings and gap statistics. |
| [`verify_generator.json`](verify_generator.json) | Audit results — `10/10` all-prime, `6/6` no-skip on verifiable scales. |
| [`Paper1_PrimeMetaPattern_Theory.md`](Paper1_PrimeMetaPattern_Theory.md) | Theory paper. **Now carries an "Erratum and 31-sample re-fit" section reflecting the corrections; original claims preserved with strikethroughs and the new fits documented.** |
| [`Paper2_MetaPattern_Algorithm.md`](Paper2_MetaPattern_Algorithm.md) | Algorithm paper. **Erratum updates the formulas, the random-gap-as-default behaviour is explicitly retracted, and the int32 Miller–Rabin overflow bug is documented.** |
| [`ALGORITHM_DERIVATION.md`](ALGORITHM_DERIVATION.md) | Derivation document. Updated to match the corrected fits and the corrected algorithm. |
| [`COMPLETE_PRIME_METAPATTERN_RESEARCH.md`](COMPLETE_PRIME_METAPATTERN_RESEARCH.md) | Combined research document. Updated. |
| [`deep_transition_analysis.py`](deep_transition_analysis.py) | Original transition-region analysis tool. Still present for historical reference; the "transition at `n* ≈ 836`" figure it produces is now known to be an artefact of the bad fit. |

---

## 🧠 The (corrected) meta-pattern

```
Scale  s = log₁₀ n

M1  residue-classifier excess AUC   ≈  0.30 ± 0.04   across s ∈ [1, 9]
                                       (mildly decaying, power-law and
                                        exponential fits indistinguishable)

M2  filter rejection rate           f_M2(s) = 1.050 / (1 + 0.034 · s)
                                       (rational form clearly best by AIC;
                                        ~0.98 at n=10², ~0.83 at n=10⁹)

M3  PNT density relative error      f_M3(s) ≈ 0.66 · s^(-2.13)
                                       (rapid decay; PNT becomes accurate)

There is no algorithmically meaningful local-to-global crossover.
The local filter is useful at every tested scale.
```

| Scale `n` | M1 (excess AUC) | M2 (filter rej.) | M3 (rel. dens. err.) |
|---|---:|---:|---:|
| `~10²` | `0.36` | `0.99` | `0.40` |
| `~10⁵` | `0.32` | `0.88` | `0.06` |
| `~10⁷` | `0.31` | `0.85` | `0.01` |
| `~10⁹` | `0.32` | `0.82` | `<0.01` |

The "critical transition at `n* ≈ 836`" referenced in the original Paper 1 §2.3 is **not present** in this data. It was derived analytically from the bad `s^(-0.37)` fit and does not survive the refit.

---

## ⚙️ The algorithm (as actually implemented and tested)

```
Given n:
  1.  Find the smallest m ≥ n with m ≡ 1 or 5 (mod 6).
  2.  Pre-filter m by trial-dividing against the first k small primes,
      where k scales smoothly with M2(s) (more primes at small s,
      still ≥5 at the largest tested s).
  3.  If m passes the pre-filter, primality-test:
        s < 4.5  →  trial division (deterministic, O(√n))
        s ≥ 4.5  →  Miller–Rabin
                       n < ~3.3·10²⁴  → deterministic Sorenson–Webster witnesses
                       n  ≥ ~3.3·10²⁴ → 20 random rounds
                                          (witness draw uses random.randrange,
                                           NOT np.random.randint, to avoid
                                           int32 overflow at n ≥ 2³¹)
  4.  If composite, advance to the next 6k±1 integer and goto 2.
```

The "next-prime" semantic is now strict (no skipping). The previous random-gap behaviour, which generated a prime *near* `n` rather than the *next* prime after `n`, is exposed separately as `random_prime_near(n)` for cryptographic uses where any prime of the right size will do.

### Audit timings (`verify_generator.py`, `count` consecutive primes from `start`, deterministic-witness path)

| `start` | `count` | mean gap | `ln(start)` | `ms/prime` | all prime | no-skip |
|---|---:|---:|---:|---:|---:|---:|
| `2` | 50 | 4.63 | 0.69 | 0.004 | yes | yes |
| `100` | 50 | 5.67 | 4.61 | 0.004 | yes | yes |
| `10³` | 50 | 7.18 | 6.91 | 0.005 | yes | yes |
| `10⁴` | 50 | 9.18 | 9.21 | 0.008 | yes | yes |
| `10⁵` | 50 | 12.00 | 11.51 | 0.011 | yes | yes |
| `10⁶` | 30 | 13.03 | 13.82 | 0.013 | yes | yes |
| `10⁷` | 20 | 18.95 | 16.12 | 0.020 | yes | not checked |
| `10⁸` | 15 | 18.00 | 18.42 | 0.023 | yes | not checked |
| `10⁹` | 10 | 19.33 | 20.72 | 0.027 | yes | not checked |
| `10¹²` | 6 | 24.80 | 27.63 | 0.071 | yes | not checked |

Every output is independently verified prime via `sympy.isprime`. Where computationally feasible, every output is verified to be the *true* next prime via `sympy.nextprime`. The mean gaps track `ln n` within `< 1.5` at every tested scale.

---

## 🚧 Honest framing (what the original draft over-claimed)

- **The exponent `−0.37` does not reproduce.** With 31 scale samples (vs the original 3) the actual M1 exponent is `~ -0.10` if interpreted as a power law, or `~ -0.026` if interpreted as exponential, and the two functional forms are statistically indistinguishable on that curve.
- **The "critical transition at `n* ≈ 836`" is an artefact** of inserting the bad fit into `1.487 · α = 1`. There is no operationally meaningful crossover at `n = 836` — or at any other specific scale — in the corrected data.
- **The renormalisation-group analogy was heuristic and remains heuristic.** No formal RG group acts on prime distributions; no β-function in the field-theoretic sense was identified. With `−0.37` no longer a measured value, the "universal critical exponent" framing is dropped.
- **The neural-network spectral-exponent connection is dropped.** Martin & Mahoney's `~0.35 – 0.45` exponents do exist, but matching them to a measured exponent of `~ -0.10` would not be a coincidence worth discussing.
- **This work does not bear on the Riemann Hypothesis or the Clay Prize.** That framing was rejected in the external review and is not retained anywhere in the corrected text.
- **Appropriate venue.** As an empirical-discovery + corrected-implementation note, this body of work is the right shape for *Experimental Mathematics* (Taylor & Francis) or *Integers*. It is not Annals-of-Mathematics-shape.
- **Two correctness bugs in v1 have been fixed and tested**: prime-skipping in the random-gap branch, and `int32` overflow in the Miller–Rabin witness draw.

---

## 🎯 What this displaces

| Standard | What it lacks | What this work adds |
|---|---|---|
| Sieve of Eratosthenes | No primality test; static; memory-bound | Single-target generator with scale-adaptive primality |
| Miller–Rabin alone | No local pre-filter; no deterministic-witness fast path beyond hand-coded sets | Combined `6k±1` + small-prime pre-filter + deterministic Sorenson–Webster witnesses below `3.317 × 10²⁴` |
| Random-gap "prime near `n`" generator | Skips primes; not a "next-prime" function | Strict `next_prime` (no skipping) **and** opt-in `random_prime_near` for crypto uses |
| Hand-tuned `sympy.nextprime` | Black-box; reasonable but not transparent | Transparent `O(√n · ln n)` / `O(log⁴ n)` branches with a documented switch threshold (`s = 4.5`) set by computational cost |

---

## 🔗 Related work in this repo

- [`../General Math Papers/`](../General%20Math%20Papers/) — LCRP and other number-theory adjacencies
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — separate `~0.85` exponent work (different family, different curve)
- [`../Math Question Generator/`](../Math%20Question%20Generator/) — number-theory domain
- [`../RNGS/`](../RNGS/) — the deterministic randomness used by `random_prime_near` could be plugged into the `Izaac` generator
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — NMP `α ≈ 0.851` spectral exponent (different family; the previous draft's claimed `0.37 ↔ 0.37` coincidence with this work is now retracted)
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — uses primality testing for cryptographic key generation; can call `random_prime_near` for that purpose

---

[← Back to main README](../README.md)
