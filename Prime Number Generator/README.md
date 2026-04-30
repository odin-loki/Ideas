# Prime Number Generator — Scale-Dependent Meta-Pattern Theory

> **🔢 Overview**: An empirically discovered **power-law transition** governing the optimal generative structure of prime numbers as a function of scale, plus a working algorithm derived from it.

---

## 🔢 Overview

This folder is **not** a generic library of sieve methods or primality tests. It documents a specific empirical discovery and the algorithm derived from it: a continuous power-law transition between **local (divisibility-based)** and **global (density-based)** generative methods for prime numbers, parameterised by scale s = log₁₀(n).

The central empirical finding is the weight function

> **α(s) = s^(−0.37)**

which interpolates between local divisibility generation (dominant at small *n*) and global density-based generation (dominant at large *n*). The two regimes have equal weight at the **critical transition point n* ≈ 836** (s* ≈ 2.92).

The exponent **−0.37** is empirically analogous to the running of coupling constants in the **Renormalization Group** (RG) framework from quantum field theory — and matches power-law exponents observed in the singular-value spectra of trained neural-network weight matrices, suggesting a structural connection between prime distributions and learned representations.

> **Naming correction.** Earlier README revisions described this folder in terms of the Sieve of Eratosthenes, Sieve of Atkin, Miller-Rabin testing, "10⁶+ primes per second", and RSA / ECC key generation. None of that reflects what the source papers actually contain. This corrected README describes the actual research.

---

## 📄 Research Documents

| Document | What it is |
|---|---|
| [`Paper1_PrimeMetaPattern_Theory.md`](Paper1_PrimeMetaPattern_Theory.md) | **Theory paper** — empirical discovery of the α(s) = s^(−0.37) power law across scales 10¹ to 10⁸; RG-flow analogy; connection to NN spectra |
| [`Paper2_MetaPattern_Algorithm.md`](Paper2_MetaPattern_Algorithm.md) | **Algorithm paper** — the MetaPattern Prime Generator derived from the power law; complete Python reference; correctness guarantees; benchmarks across eight orders of magnitude |
| [`COMPLETE_PRIME_METAPATTERN_RESEARCH.md`](COMPLETE_PRIME_METAPATTERN_RESEARCH.md) | Comprehensive research consolidation across both papers |
| [`ALGORITHM_DERIVATION.md`](ALGORITHM_DERIVATION.md) | Step-by-step derivation of the algorithm from the theory |

---

## 🧮 The Meta-Pattern Equations

For a prime near value *n* at scale s = log₁₀(n):

> **Generation Method = α(s) · Local_Method + β(s) · Global_Method**
>
> where  α(s) = s^(−0.37)   [local / divisibility weight]
>
> and    β(s) = 1 − 0.487 · s^(−0.37)   [global / density weight]

### Critical transition

The methods have equal weight at:

> **s* ≈ 2.92  →  n* ≈ 836**

Below n ≈ 836, divisibility rules dominate. Above, density / statistical methods dominate. The transition is **smooth** — there is no hard phase boundary.

---

## 🔬 Empirical Methodology

The theory paper analyses prime distributions across three primary scale regimes (n ~ 10², 10⁵, 10⁷), using contiguous windows of 10,000 primes per scale, measuring:

| Feature class | Specific measurements |
|---|---|
| **Local (divisibility) features** | 6k±1 filter pass-rate, composite rejection effectiveness, residue-class uniformity across mod-6 classes |
| **Global (density) features** | Observed prime density vs. PNT prediction (1/ln n), mean gap vs. expected ln(n), gap-distribution chi-squared deviation from exponential, gap variance-to-mean ratio |

Power-law fits to the measured importances:

| Curve | Form | Notes |
|---|---|---|
| Local importance | f_L(s) = 0.258 · exp(−0.373·s) | Decays with scale |
| Global importance | f_G(s) = 1 − 0.487 · exp(−0.371·s) | Approaches 1 with scale |

The exponents −0.373 and −0.371 are statistically indistinguishable; both are reported as the canonical **−0.37**.

---

## ⚙️ The MetaPattern Prime Generator (Paper 2)

The algorithm uses α(s) to mix two prime-generation strategies. It does not blend outputs (which would be undefined), but blends **how candidates are selected** and **how primality is verified**:

### Adaptive candidate generation

| Regime | Behaviour |
|---|---|
| **α(s) > β(s)** (s < s*) | Initial candidate from `next_6k±1(n)`; subsequent candidates advanced by +1 in 6k±1 space |
| **α(s) ≤ β(s)** (s ≥ s*) | Initial candidate sampled from Exponential(mean = ln n) gap distribution; subsequent candidates advanced by ln(n) in 6k±1 space |
| Pre-check intensity | `num_primes_to_precheck = int(N_small_primes · α(s))` — more divisibility filtering at small scales |

### Scale-adaptive primality verification

| Scale | Verifier |
|---|---|
| Small n | Deterministic trial division within √n |
| Large n | Miller-Rabin probabilistic test, k rounds, error ≤ 4⁻ᵏ per round |

### Properties

- **Correctness** at all tested scales (verified deterministic methods at small s; Miller-Rabin probabilistic verification at large s).
- **Smooth performance** — no hard phase boundaries.
- **Theoretically grounded** — the −0.37 exponent comes from measurement, not tuning.
- **Optional integration** with the **Izaac** deterministic randomness framework (see [`../Compression Algorithms/izaac_algorithm_research_paper.md`](../Compression%20Algorithms/izaac_algorithm_research_paper.md)) for fully deterministic operation.

---

## 🌐 Connections to Other Phenomena

### Renormalization Group analogy

The α(s) flow is structurally analogous to RG flow in quantum field theory: microscopic (local) interactions yield to macroscopic (statistical/thermodynamic) behaviour as observation scale increases. The connection is empirical, not formal — but it suggests that universality classes of prime-generation methods exist in the same way universality classes of critical phenomena do.

### Neural-network singular-value spectra

The α = −0.37 exponent matches power-law exponents measured in the singular-value spectra of trained NN weight matrices (see [`../Compression Algorithms/NMP_neural_compression_research_paper.md`](../Compression%20Algorithms/NMP_neural_compression_research_paper.md), measured α ≈ 0.851 — though note the relationship between these specific values is hypothesised, not yet derived). The shared exponent class hints at a common organisational principle for information across scales.

---

## 🔗 Related Work

This work connects to:

- **Compression Algorithms** — particularly the NMP paper's measured power-law exponents in NN singular spectra, and the Izaac framework which can supply deterministic randomness for the global-regime generator
- **GF2 Algebra and Applications** — number-theoretic / algebraic substrate
- **Statistical Generation** — heavy-tailed distributions, combinatorial ML
- **RNGS** — random / pseudorandom generation; complementary to deterministic prime generation

---

## 📖 See Also

- [`EDITORIAL_ROADMAP.md`](../EDITORIAL_ROADMAP.md) — editorial standards and batch history
- [`EDITORIAL_STYLE.md`](../docs/EDITORIAL_STYLE.md) — house style guide
- [`Compression Algorithms/`](../Compression%20Algorithms/) — NMP power laws; Izaac primitive
- [`Statistical Generation/`](../Statistical%20Generation/) — heavy-tailed / combinatorial work
- [`RNGS/`](../RNGS/) — randomness families

---

## 🛡️ About This Project

This is preliminary empirical research — the discovery of a power-law structure in prime-generation method efficacy, and the algorithm that comes out of it. Claims are grounded in measurements at the eight-orders-of-magnitude scale; the RG and NN analogies are noted as suggestive empirical observations, not formal mathematical equivalences. The reference Python implementation is verified against established deterministic primality tests at small scales and uses Miller-Rabin at large scales, so correctness does not depend on the meta-pattern theory itself.

[← Back to main README](../README.md)
