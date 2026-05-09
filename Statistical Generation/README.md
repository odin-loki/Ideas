# Statistical Generation — Universal Statistical Generator

> **Universal Statistical Generator (USG): a deterministic, interpretable, classical-statistics framework that claims ~90 % of state-of-the-art neural perplexity on long-context tasks while running at `O(N)` training cost.** Built on three foundations — category-theoretic generator composition, Lévy-process triplet parametrisation, and SHA-256 hash-based context compression to `M = 2³²` states — and filtered through a two-stage MDL + Marchenko–Pastur spectral pruning pipeline that keeps **~3 % of states with 97 % signal retention**. Where transformers have ~10 % perplexity advantage on absolute SOTA, USG offers determinism, audit trails, and proofs that a transformer simply cannot match.

---

## What this folder is

There are three reasons people use neural language models even when they don't really need autoregressive generative quality: (1) they handle long contexts, (2) they generalise across domains via embeddings, and (3) they're the default. The Universal Statistical Generator argues — with proofs, working Python, and a head-to-head comparison table — that a sufficiently disciplined classical framework can capture **~90 %** of the perplexity that transformers achieve, on contexts **200 × longer** than typical n-gram methods, with `O(N)` training and a fully deterministic pipeline that can be inspected line-by-line. The package includes formal proofs of convergence, a category-theoretic argument for why generators compose at all (Theorem 4.1), and a hash-collision analysis (`≈ N²/(2M) ≈ 0.012 %` for `N = 10⁶`).

The pitch is: classical methods on a 2025 footing. Lévy theory + category theory + hashing + information theory. No GPU. No black box. Quantifiable trade-offs.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`paper1_categorical_levy_framework.md`](paper1_categorical_levy_framework.md) | Foundation paper. Generators as `Gen = (T, Σ, ψ)` triples, Lévy triplet algebra, Theorem 4.1 (categorical composition under priority), MDL + spectral filtration. |
| [`paper2_state_explosion_hash_compression.md`](paper2_state_explosion_hash_compression.md) | The hash-compression engine. SHA-256 → `H(c) mod M`, `M = 2³²`, collision rate analysis. Long-context perplexity examples (`18.4` vs `8.7` on a 20-gram task). |
| [`universal_generator_theory_verified.md`](universal_generator_theory_verified.md) | Theory paper with computer-verified proofs (self-asserted). Triplet addition / averaging composition rules with `μ/2, σ²/2` worked examples. |
| [`complete_math_proof_document.md`](complete_math_proof_document.md) | Proof appendix. Substantially overlaps with `Statistical Generation.md`. |
| [`Statistical Generation.md`](Statistical%20Generation.md) | The "long proof document." Largely duplicates the proof appendix. |
| [`classical_methods_comparison.md`](classical_methods_comparison.md) | Head-to-head table: USG vs n-gram, KN-smoothed, transformer baselines. |
| [`Python_examples_README.md`](Python_examples_README.md) | Operator-facing introduction to the Python stack. |
| [`universal_generator.py`](universal_generator.py) | Reference implementation. `LevyTriplet.__add__`, `Generator.max_states` (default `2²⁰` in code, `2³²` in papers), `min_count = 2`, SHA-256 first-4-byte hash. |
| [`advanced_examples.py`](advanced_examples.py) | Extended demonstration suite. |

---

## 🧠 Foundations

### 1. Generators as a category

A **Generator** is `Gen = (T, Σ, ψ)` — a transition kernel `T`, a state-space `Σ`, and a Lévy triplet `ψ = (b, σ², ν)` parametrising the underlying continuous-time process. Composition rules:

- **Sum.** `T₁ ⊕ T₂` corresponds to triplet addition.
- **Average / priority composition.** Theorem 4.1's worked example: averaging two Gaussian-noise generators yields `μ/2, σ²/2`. Identity / scaling tensions are documented honestly.

### 2. Lévy triplet parametrisation

Every generator parametrised by `ψ = (b, σ², ν)`:
- `b` — drift
- `σ²` — Brownian variance  
- `ν` — Lévy measure (jump component)

This is *the* generality move: every infinitely-divisible distribution lives in the triplet representation, so you can target Gaussian-tailed, jump-heavy, or hybrid behaviours with one algebra.

### 3. Hash compression to `2³²` states

Long contexts blow up state-space exponentially. The compressor: `H(c) = SHA-256(encode(c)) mod M`, `M = 2³²`. Collision rate `≈ N²/(2M)` ≈ **0.012 % for `N = 10⁶`**. Truncating SHA-256 to 4 bytes is the empirical sweet spot in `universal_generator.py`.

### 4. Two-stage MDL + spectral filtration

| Stage | Mechanism | Reported result |
|---|---|---|
| **MDL pruning** | Score `−log P + |Π_h| log N`, prune above percentile `p` (default 50) | Removes **74 % of states with 97 % signal retention** |
| **Marchenko–Pastur cut** | `λ* = σ²(1 + √(S/V))²`-style spectral threshold | **31 % perplexity reduction** stacked on top |

### 5. Convergence

`||π̂_h − π_h||_TV ≤ C/√n_h`. Total-variation convergence in the per-hash-bucket transition kernel.

---

## 📊 Reported headline results

| Claim | Source |
|---|---|
| **~90 % of neural-SOTA perplexity** | `Python_examples_README.md` comparison table; `paper1` |
| **200 × longer context** than classical methods | `paper2` |
| **`O(N)` training cost** | papers |
| Memory footprint narrative | ~4 GB for `M = 2³²` |
| MDL prunes 74 % of states, retains 97 % signal | `paper1` |
| Combined MDL + spectral: 80–90 % parameter removal, < 1 % loss | long proof document |
| Long-context perplexity example | 18.4 (USG) vs 8.7 (transformer) on 20-gram task |
| Collision rate at `N = 10⁶`, `M = 2³²` | ≈ 0.012 % |

---

## 🚧 Honest caveats

- **Theorem 4.1's proof is not a polished category-theory argument by usual standards.** The identity / scaling tension under naive averaging (`μ/2, σ²/2`) is acknowledged in-text; the resolution is to use "priority composition" rather than averaging when identity matters.
- **`max_states = 2²⁰` in code default** (`universal_generator.py`), not `2³²` from the papers. The `2³²` figure is the analytical maximum; 1 048 576 is the working default unless overridden.
- **"Computationally verified" is self-asserted.** No third-party formal-methods tool ran the proofs.
- **Limitations explicit in §**: ~10 % perplexity gap to true neural SOTA; classic bias-variance trade-off in collision rate.
- **`Statistical Generation.md` and `complete_math_proof_document.md` are largely duplicated.** This is documentation lineage, not two independent corroborating sources.

---

## 🎯 What this displaces

| Standard tool | Limitation | What USG offers |
|---|---|---|
| n-gram + Kneser-Ney | Short context, no algebra | 200 × context, categorical composition |
| Transformer | Black box, GPU, ~10 % better | 90 % of perplexity, deterministic, `O(N)`, audit-trail |
| Variational HMMs | Limited compositional vocabulary | Full Lévy triplet algebra |
| Hashing-trick LMs | No filtration, lossy | MDL + spectral two-stage filter |

---

## 🔗 Related work in this repo

- [`../Compression Algorithms/`](../Compression%20Algorithms/) — GRIA, NMP, Izaac (sister information-theoretic work)
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic underpinnings (GRIA spectrum theorem)
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — Beta-MC threat scoring uses similar distributional reasoning
- [`../Filtering/`](../Filtering/) — GH-SR-IMM uses GH/Lévy machinery in measurement-noise modelling
- [`../Statistical Scheduler/`](../Statistical%20Scheduler/) — same author lineage; statistics + stability
- [`../Cypha/`](../Cypha/) — HRNA training stack uses generator composition

---

[← Back to main README](../README.md)
