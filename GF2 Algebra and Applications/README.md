# GF2 Algebra and Applications

> **A seven-paper sweep that starts with an exhaustive computer-verified taxonomy of all 16 binary operations on `{0, 1}` (with a proven uniqueness theorem: **AND** is the *only* nontrivial operation that forms a ring with **XOR** over GF(2)), extends through finite-field permutation polynomials over `GF(2ⁿ)` (the AES inverse `x⁻¹ = x²⁵⁴` is one of `φ(255) = 128` such permutations on `GF(2⁸)`), introduces a graded reversibility coordinate `α(f) = 1 − H(f(X))/H(X)` with bifurcation at `α = 0.5`, derives gate-count benchmarks via algebraic normal form (ANF/Zhegalkin) — Rule 110 dropping from 19 to 6 gates (`68 %` reduction), full-adder sum dropping `78 %`, XOR `80 %` — and culminates in a Differentiable Logic Gate Network experiment showing the network *learns* to favour `AND` (`10/96` slots) and `NOR` (`11/96`) over the uniform `6/96` expectation.** The point is unification: from the smallest finite field through to learning systems, the same algebraic spine runs through.

---

## What this folder is

GF(2) — the two-element field — is the structural backbone of digital computing, finite-field cryptography, error-correcting codes, and the algebraic underpinnings of much of machine learning's "low-level" theory. Treatments of it are usually fragmented: cryptographers know AES inverse polynomials, EE folks know Boolean ANF, and the reversibility / entropy literature lives in physics. This folder is one author's attempt to do all of it at once, anchored to a single seven-paper series that starts with the smallest possible algebraic question (what are *all* the binary ops on `{0, 1}` and how do they relate?) and works upward through finite-field extensions, graded reversibility, dynamical-systems bifurcations, ANF gate-count benchmarks, neural learning of logic gates, and a closing synthesis paper.

The headline structural result is the **GF(2) Ring Uniqueness Theorem** in Paper 1: of the 16 binary operations on `{0, 1}`, **AND** is the unique non-trivial choice that forms a commutative ring with **XOR**. Every algebraic structure that uses GF(2) is thus *forced* into this exact pair.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`paper1_binary_algebra_taxonomy.md`](paper1_binary_algebra_taxonomy.md) | **All 16 binary ops on `{0,1}` enumerated** (FALSE, AND, AB̄, A, ĀB, B, XOR, OR, NOR, XNOR, B̄, A→B, Ā, B→A, NAND, TRUE). **GF(2) Ring Uniqueness Theorem.** **12** original theorems claimed. ANF / Zhegalkin polynomial for each op. **Four Galois residuation pairs**, **six De Morgan pairs**. Exhaustive `{0,1}²` verification claimed. |
| [`paper2_permutation_polynomials.md`](paper2_permutation_polynomials.md) | **Monomial Permutation Criterion: `xᵏ` is a permutation of `GF(2ⁿ)` iff `gcd(k, 2ⁿ − 1) = 1`.** Verification claimed for `n = 3, 4, 5, 6` (116 cases). Table with `φ(2ⁿ − 1)` permutation counts: `GF(2⁸): φ(255) = 128`. **AES inverse `x⁻¹ = x²⁵⁴`, `gcd(254, 255) = 1`** confirms it as a valid permutation. **Frobenius automorphism order `n`; Galois group cyclic of order `n`.** Theorem 5: degree vs depth, `depth ≥ ⌈log₂(d + 1)⌉`. |
| [`paper3_neural_networks_graded_contractions.md`](paper3_neural_networks_graded_contractions.md) | **GRIA grade `α(f) = 1 − H(f(X)) / H(X)` for uniform `X`.** Numerical Jacobian / contraction values (`0.02 – 0.14`, max singular value `0.1435`) demonstrating Banach contraction for small MLPs. |
| [`paper4_edge_of_chaos.md`](paper4_edge_of_chaos.md) | **`f_α` map dynamics. Bifurcation at `α = 0.5`** (21 test points across `0.49 → 0.50`). **Rule 110 ANF: `c ⊕ b ⊕ bc ⊕ abc`.** **6-gate optimum vs 19-gate naive (`68 %` reduction).** 3-gate implementations enumerated; **4096 configurations** tested. Table of CA rules with `α ≈ 0.824` for Rule 110, etc. |
| [`paper5_circuit_simplification.md`](paper5_circuit_simplification.md) | ANF conversion table for all 16 ops. **Benchmark gate-count reductions: XOR `80 %`, Rule 110 `68 %`, full-adder sum `78 %`, majority `29 %`, carry `29 %`** vs SOP baseline. |
| [`paper6_dlgn_validation.md`](paper6_dlgn_validation.md) | **Differentiable Logic Gate Network experiment.** 2-layer net, `8 + 8 + 1 = 17` gates, `2 000` training steps, `6` random seeds per task. **96 gate slots: AND chosen `10` times, NOR `11` — vs `6/96` uniform expectation.** Network *learns* the algebraic skeleton. |
| [`paper7_synthesis.md`](paper7_synthesis.md) | **GRIA Spectrum Theorem.** Synthesis. Links to Izaac, Cypha.py, ECE (expected calibration error) discussion. Irreducibility as compression bound. |

---

## 🧠 The seven-paper arc

```
Paper 1  ─ All 16 binary ops + GF(2) ring uniqueness
   │
Paper 2  ─ GF(2ⁿ) permutation polynomials (AES, Frobenius, Galois)
   │
Paper 3  ─ α(f) = 1 - H(f(X))/H(X)  ── reversibility grade
   │
Paper 4  ─ f_α dynamics  ── bifurcation at α = 0.5, Rule 110 ANF
   │
Paper 5  ─ Gate-count benchmarks  ── 80 % XOR, 78 % full-adder, 68 % Rule 110
   │
Paper 6  ─ DLGN learning the algebra  ── AND 10/96, NOR 11/96
   │
Paper 7  ─ GRIA Spectrum Theorem  ── synthesis; bridges to Izaac, Cypha
```

---

## 📊 Headline empirical results

| Result | Source paper | Number |
|---|---|---|
| AND is the unique non-trivial bilinear over XOR | Paper 1 | structural theorem |
| Permutation count on `GF(2⁸)` | Paper 2 | `φ(255) = 128` |
| Bifurcation in `f_α` | Paper 4 | at `α = 0.5` |
| Rule 110 gate reduction | Paper 4 / 5 | `19 → 6` (`68 %`) |
| XOR gate reduction vs SOP | Paper 5 | `80 %` |
| Full-adder sum reduction | Paper 5 | `78 %` |
| DLGN AND preference | Paper 6 | `10/96` vs uniform `6/96` |
| DLGN NOR preference | Paper 6 | `11/96` vs uniform `6/96` |
| Banach contraction range | Paper 3 | `0.02 – 0.14`, max σ `0.1435` |

---

## 🚧 Honest caveats

- Several papers explicitly note that empirical demonstrations are **small-network / synthetic verification** rather than industrial-scale benchmarks.
- **Paper 7's `ECE ∝ |α − α*|`** is a framework / heuristic relationship, not a proven law.
- The **neural-prime exponent "coincidence"** elsewhere in the repo (`Prime Number Generator/`) is flagged speculative — see that folder's README for the same caveat.
- Self-asserted "computer verified" — no third-party formal-methods tool ran the proofs.

---

## 🎯 Why this is unusual

| Standard treatment | Limitation | What this series adds |
|---|---|---|
| Boolean algebra in EE textbooks | Stops at gate equivalence | Full ring-uniqueness theorem |
| Finite field for crypto | Permutation polys treated case-by-case | Unified `gcd(k, 2ⁿ − 1) = 1` criterion |
| Reversibility in physics | Disconnected from CS | `α` grade + `f_α` dynamics + bifurcation |
| Logic gates in deep learning | Discretisation hack | DLGN learns the algebraic preferences |
| Compression as engineering | Empirical | Irreducibility-as-compression-bound |

---

## 🔗 Related work in this repo

- [`../3 to 8 Value Boolean Algebra/`](../3%20to%208%20Value%20Boolean%20Algebra/) — sister enumeration over `n`-variable Boolean function space
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — GRIA framework's canonical home (this folder hosts the spectrum theorem)
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — `GF(2²⁵⁶)` AEAD (Paper 2 finite-field machinery)
- [`../Veritas/`](../Veritas/) — PAC bounds on `H = {h : {0,1}ⁿ → {0,1}ⁿ}` complement Paper 3's `α` grade
- [`../Cypha/`](../Cypha/) — HRNA inference (Paper 7 explicitly bridges)
- [`../RNGS/Boolean RNG/`](../RNGS/Boolean%20RNG/) — Boolean LCG analysis benefits from the operator taxonomy
- [`../Prime Number Generator/`](../Prime%20Number%20Generator/) — sister `α(s) = s^(-0.37)` exponent discussion

---

[← Back to main README](../README.md)
