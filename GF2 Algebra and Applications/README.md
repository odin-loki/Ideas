# GF2 Algebra and Applications — A Unified Algebraic Theory of Binary Computation

> **⚡ Overview**: A seven-paper series treating **{0, 1} as the field GF(2)** rather than as Boolean logic, building from a complete operator taxonomy through neural-network learning theory and circuit synthesis to a unified GRIA / Izaac / Cypha synthesis.

---

## ⚡ Overview

**GF2 Algebra and Applications** is a seven-paper research programme by *Odin* (Independent Researcher, Sydney) that treats binary computation as a **field-theoretic** rather than logical phenomenon. The base-2 constraint imposes a uniquely rigid algebraic structure — the field GF(2) — that does not follow from Boolean logic alone. The series develops this structure formally, then connects it to circuit theory, dynamical systems, and neural-network learning.

The central organising claim of the synthesis paper (Paper 7) is the **GRIA Spectrum Theorem**: every binary computational system, from a single logic gate to a deep neural network, is characterised by its reversibility grade α ∈ [0, 1]:

| α | Regime | Concrete instance |
|---|---|---|
| **α = 0** | GF(2ⁿ) permutation regime — fully reversible | Izaac algorithm structure (max-length LFSRs, gcd(k, 2ⁿ−1) = 1) |
| **α = 0.5** | Edge of chaos — maximum computational complexity | Rule 110 (universal cellular automaton) |
| **α > 0.5** | Contracting pattern-recognition regime | Cypha learned classifiers; trained NNs |

---

## 📄 The Paper Series

| Paper | Title / focus | Key result |
|---|---|---|
| [`paper1_binary_algebra_taxonomy.md`](paper1_binary_algebra_taxonomy.md) | A computational taxonomy of binary algebraic structures over {0, 1} | Complete classification of all 16 binary operators across 12 algebraic properties; **GF(2) Ring Uniqueness Theorem** — AND is the unique non-trivial operator bilinear over XOR, making (GF(2), XOR, AND) the unique ring on {0, 1} |
| [`paper2_permutation_polynomials.md`](paper2_permutation_polynomials.md) | Permutation polynomials over GF(2ⁿ) | Permutation criterion **gcd(k, 2ⁿ−1) = 1 ↔ reversible**; foundations for LFSR design, AES S-box analysis, reversible circuits |
| [`paper3_neural_networks_graded_contractions.md`](paper3_neural_networks_graded_contractions.md) | Neural networks as graded contraction maps | Contraction theorem: trained networks are Banach contractions; basis for NN compression and generalisation bounds |
| [`paper4_edge_of_chaos.md`](paper4_edge_of_chaos.md) | Edge-of-chaos phenomena | Bifurcation at **α = 0.5** identifies the edge-of-chaos regime; Rule 110 universality |
| [`paper5_circuit_simplification.md`](paper5_circuit_simplification.md) | AND-XOR circuit simplification calculus | Rewrite calculus for circuit minimisation grounded in Paper 1's ring uniqueness |
| [`paper6_dlgn_validation.md`](paper6_dlgn_validation.md) | Differentiable Logic Gate Network validation | Empirical validation of the framework via DLGNs |
| [`paper7_synthesis.md`](paper7_synthesis.md) | **Synthesis** — algebraic neural-network compression, irreducibility, the GRIA spectrum | **GRIA Spectrum Theorem** (above); connection to Izaac algorithm; connection to Cypha.py (discriminative information field architecture); irreducibility as the formal lower bound on compression |

---

## 🧮 GF(2) Field Properties (the genuine ones)

| Property | Description |
|---|---|
| **Addition** | XOR: 0+0=0, 0+1=1, 1+0=1, 1+1=0 |
| **Multiplication** | AND: 0·0=0, 0·1=0, 1·0=0, 1·1=1 |
| **Additive identity** | 0 |
| **Multiplicative identity** | 1 |
| **Additive inverse** | Every element is its own inverse: x + x = 0 |
| **Multiplicative group** | (GF(2)\\{0}, ·) = ({1}, ·) — the trivial group |
| **Characteristic** | 2 (i.e., 1 + 1 = 0) |
| **Algebraic closure** | GF(2̄) is the union of all GF(2ⁿ) |

> **The point.** Boolean algebra is base-independent; GF(2) is not. The base-2 constraint is what makes (XOR, AND) a *ring* with multiplicative inverses where they exist — a structure not derivable from Boolean logic alone, and the foundation for everything in this series.

---

## 🔬 Headline Results

### From Paper 1 — The 16-operator taxonomy

The paper classifies all 16 binary operators on {0, 1} across **12 algebraic properties**: commutativity, associativity, idempotency, **bilinearity**, self-duality, group structure, lattice structure, threshold realisability, affine representability, and functional completeness. The **Algebraic Normal Form** (Zhegalkin polynomial) is computed for every operator. Four Galois residuation pairs and six De Morgan dualities are identified. Every result is verified by exhaustive enumeration.

### From Paper 2 — Permutation polynomial criterion

A monomial map x → x^k on GF(2ⁿ) is a permutation iff **gcd(k, 2ⁿ − 1) = 1**. This is the formal criterion underlying max-length LFSRs, the AES S-box's invertibility, and reversible-circuit design.

### From Paper 7 — The GRIA Spectrum

| Paper | Domain | Field | Key result | Application |
|---|---|---|---|---|
| Paper 1 | 16 binary ops | Binary algebra | GF(2) ring uniqueness | Circuit rewrite calculus foundation |
| Paper 2 | GF(2ⁿ) maps | Galois field | Permutation criterion | LFSR design, AES S-box, reversible circuits |
| Paper 3 | Neural networks | Dynamical systems | Banach contraction theorem | NN compression, generalisation bounds |
| Paper 4 | Edge of chaos | Bifurcation theory | Edge bifurcation at α = 0.5 | Rule 110 universality, complexity placement |
| Paper 5 | Circuits | Algebraic | AND-XOR rewrite calculus | Boolean circuit minimisation |
| Paper 6 | DLGN | Empirical | Validation of grades | Differentiable logic gate networks |
| Paper 7 | All | Unified | **GRIA spectrum** | Algebraic neural architecture search |

---

## 🔗 Related Work

This series is the algebraic foundation for several adjacent projects:

- **Compression Algorithms** — the GRIA framework (Paper 7) is the algebraic core; the synthesis paper there extends the GRIA spectrum to NMP and Izaac
- **Cypha** — Paper 7 explicitly connects to the Cypha codebase as the contracting-regime (high-α) instance
- **Izaac as Side Data** — Paper 7's α = 0 regime is the Izaac algorithm structure
- **3 to 8 Value Boolean Algebra** — multi-valued generalisations of Paper 1
- **ARIA Encryption Algorithm** — uses GF(2²⁵⁶) machinery related to Paper 2's permutation theory
- **Break AES** — AES S-box analysis intersects Paper 2's permutation-polynomial criterion

---

## 📖 See Also

- [`Compression Algorithms/`](../Compression%20Algorithms/) — GRIA, NMP, Izaac, synthesis
- [`Cypha/`](../Cypha/) — high-α contracting-regime instance
- [`3 to 8 Value Boolean Algebra/`](../3%20to%208%20Value%20Boolean%20Algebra/) — multi-valued logic
- [`ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — GF(2²⁵⁶) cryptographic use
- [`Break AES/`](../Break%20AES/) — S-box / linear cryptanalysis

---

## 🛡️ About This Project

The series is intended as a **foundational reference**: a complete, computationally verified treatment of GF(2) algebra plus the bridges from there to circuits, dynamical systems, and neural-network learning. All proofs in Paper 1 are constructive and accompanied by exhaustive computational verification. Subsequent papers build on this foundation rather than restating it.

[← Back to main README](../README.md)
