# Compression Algorithms — A Unified Theory of Compression Across Reversibility Grades

> **📦 Overview**: Three independently developed frameworks — **Izaac**, **GRIA**, and **NMP** — synthesised into a single algebraic theory of compression spanning lossless string coding through irreversible distribution learning.

---

## 📦 Overview

This folder contains a connected research programme in compression theory by *Odin Thoresen* (Defense Technology Division, Sydney). Three frameworks, each developed in its own paper and capable of standing alone, are shown to be three faces of a single unified theory. The unifying claim is the **State Compression Thesis**: any system whose outputs can be deterministically derived from a compact shared state achieves compression with no per-output communication overhead.

### The three frameworks

| Acronym | Stands for | One-line summary |
|---|---|---|
| **Izaac** | (project name; not an acronym) | Shared deterministic randomness as a computational primitive — pseudorandom outputs from a compact state σ of size O(λ + log k), with applications to Byzantine consensus, beyond-Shannon compression, VRFs, and non-interactive MPC |
| **GRIA** | **Graded Reversible-Irreversible Algebra** | Compression operators parameterised by a continuous grade α ∈ [0, 1] interpolating from lossless string coding (α = 0) through edge-of-chaos (α = 0.5) to irreversible distribution compression (α = 1) |
| **NMP** | **Nonlinear Manifold Projection** | A three-operator decomposition (Π / Φ / Λ) showing that neural-network training is a high-α GRIA instance, with measured singular-value power laws S_k ~ a·k^(−α) and α ≈ 0.851 |

> **Naming correction.** Earlier README revisions in this repo carried fabricated acronym expansions ("Generalised Random Information Algorithm", "Neural Multi-Precision"). These were wrong. The expansions above come directly from the source papers.

---

## 📄 Research Papers

| Paper | Description |
|---|---|
| [`izaac_algorithm_research_paper.md`](izaac_algorithm_research_paper.md) | **Izaac** — shared deterministic randomness as a primitive; ten theorems including the meta-theorem that shared randomness is information-theoretically equivalent to a free broadcast channel |
| [`GRIA_Technical_Memorandum.md`](GRIA_Technical_Memorandum.md) | **GRIA** technical memorandum — graded operator framework, MDL connection, three-stage GRIA pipeline (pretraining → distillation → fine-tuning) |
| [`GRIA/GRIA_Research_Paper.md`](GRIA/GRIA_Research_Paper.md) | **GRIA** full paper — eleven axioms; five novel operators (Grade-Exponential, Modular Transcendental, Quantum Interference, Entropy-Minimizing, **Phi-Adic**); proven J ≤ 0.951 upper bound; Phi-Adic achieves J = 0.889 (93.4% of theoretical max) at compression ratio 1/φ |
| [`GRIA/GRIA_framework_Research_Paper.md`](GRIA/GRIA_framework_Research_Paper.md) | GRIA framework — extended treatment |
| [`NMP_neural_compression_research_paper.md`](NMP_neural_compression_research_paper.md) | **NMP** — neural networks as compression algorithms; the three primitive operators Π (linear projection), Φ (half-space folding), Λ (lifting); empirical power law α = 0.851 ± 0.122 |
| [`NN_Compression_Algebra_Framework.md`](NN_Compression_Algebra_Framework.md) | Algebraic framing of NN compression as the 6-tuple **F_NN = (Θ, D, C, R, δ, ρ)** |
| [`compression_algebra_framework.md`](compression_algebra_framework.md) | Compression-algebra framework supporting the above |
| [`unified_compression_theory_research_paper.md`](unified_compression_theory_research_paper.md) | **Synthesis** — the State Compression Thesis; mapping Izaac, GRIA, and NMP onto a single structure; cross-framework results |

---

## 🧮 Key Results at a Glance

### State Compression Thesis (Theorem 2.1 of the synthesis paper)

> For any system *S* generating outputs o₁, o₂, …, o_k deterministically from a compact state σ of size |σ| = O(λ + log k), the effective compression ratio ρ(S) = Σ|o_i| / |σ| grows without bound as k → ∞.

### GRIA J-score landscape

| Operator | J-score | Notes |
|---|---|---|
| **Theoretical maximum (proven upper bound)** | **0.951** | No GRIA operator can exceed this |
| Phi-Adic ⊕_Φ (Zeckendorf / golden ratio) | **0.889** | 93.4% of max; compression ratio 1/φ ≈ 0.618 |
| Quantum Interference ⊕_QI | — | Best avalanche effect (0.49) |
| XORTropicalHybrid | best practical composite | Highest practical composite score among ten benchmarked algebras |
| XOR + Tropical baseline | 0.742 | Reference baseline; novel operators outperform by 20–40% |

### NMP measurements

- **Intrinsic dimensionality**: trained networks recover 3-d ground-truth manifold in 20-d embedding space exactly at the first layer.
- **Singular-value power law**: S_k ~ a·k^(−α), α = 0.851 ± 0.122; fit quality improves with depth (R² = 0.75 → 0.87 → 0.97).
- **MDL optimum**: P* = 45 parameters at 218.7:1 effective compression on benchmark dataset.
- **Connection**: α_NN = 0.851 connects to SDE theory of SGD via Dyson Brownian motion and gamma-type spectral distributions.

### How the three frameworks transcend Shannon's bound (each in a different way)

| Framework | What Shannon's bound assumes | How the framework escapes it |
|---|---|---|
| **Izaac** | Receiver doesn't know the message | Shared state means the receiver derives the message — no channel needed |
| **GRIA** | Source is i.i.d. | φ-Adic and other graded operators exploit higher-order structure i.i.d. models miss |
| **NMP** | Compression target is the instance | Compression target is the *distribution* P(Y\|X), not any specific x |

---

## 🔬 Conceptual Map

```
                              State Compression Thesis
                                       ▲
                       ┌───────────────┼───────────────┐
                       │               │               │
                  Izaac (algorithmic)  │            NMP (geometric)
                       │           GRIA (algebraic)    │
                       │               │               │
                shared seed σ      grade α ∈ [0,1]   θ* ∈ ℝᴾ
                  → PRF outputs    → operator family → distribution
                                                       predictions
```

GF(2) algebra (see [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/)) provides the discrete substrate; the Cypha codebase ([`../Cypha/`](../Cypha/)) is the engineering instantiation of the **HRNA** (Harmonic Recursive Neural Architecture) NMP codec.

---

## 🔗 Related Work

This work connects to:

- **GF2 Algebra and Applications** — the algebraic substrate (Paper 7's GRIA Spectrum Theorem unifies the GF(2) results with the GRIA grade)
- **Cypha** — practical realisation of the HRNA / NMP codec
- **ARIA Encryption Algorithm** — shares Vandermonde / Horner / GF(2ⁿ) machinery
- **Statistical Generation** — distributional learning context for NMP
- **Veritas** — formal verification of learning bounds; complementary to GRIA's algebraic grading
- **Izaac as Side Data** — the `Izaac` paper here is the foundational write-up for that adjacent folder

---

## 📖 See Also

- [`EDITORIAL_ROADMAP.md`](../EDITORIAL_ROADMAP.md) — editorial standards and batch history
- [`EDITORIAL_STYLE.md`](../docs/EDITORIAL_STYLE.md) — house style guide
- [`Cypha/`](../Cypha/) — HRNA inference / training framework (NMP codec)
- [`GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic foundations
- [`Izaac as Side Data/`](../Izaac%20as%20Side%20Data/) — Izaac applications

---

## 🛡️ About This Project

This folder collects an integrated research programme on compression. The deliverables are:

- **Algorithmic** — the Izaac primitive and its protocol library (consensus, VRFs, MPC, beyond-Shannon coding)
- **Algebraic** — the GRIA framework, eleven axioms, five proven operators, the J ≤ 0.951 upper bound
- **Geometric** — the NMP decomposition of neural networks and its measured spectral signature
- **Synthetic** — the State Compression Thesis tying all three together

Each paper stands alone. Read in series — Izaac → GRIA → NMP → synthesis — they form a coherent theory.

[← Back to main README](../README.md)
