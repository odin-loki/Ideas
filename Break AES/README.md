# Break AES — Transformer + RL Distillation: Convergence Sketch and Reference Code

> **🔐 Warning**: A **sketch-level** convergence argument for a transformer / distillation / RL pipeline applied to AES, plus reference code. Treat as research notes, not a recipe.

---

## 🔐 Overview

**Break AES** is a small, self-contained exploration of whether a transformer student trained via teacher distillation followed by an RL phase could be applied to AES cryptanalysis. The folder contains:

- A **mathematical sketch** of two-phase convergence (distillation phase, then policy-gradient RL phase, then combined-loss analysis)
- A **reference Python implementation** of the transformer + distillation + RL pipeline
- An **architecture diagram** in Mermaid

> **Honesty note.** The math-proof document is explicit: it is a *sketch*, with informal arguments. Quoting from the source: *"The arguments are informal; a venue-ready version would state measure-theoretic assumptions, learning rates, and non-convexity caveats explicitly."* Don't read it as a finished proof. Read it as a structured outline of which results would need to be made rigorous.

> **Don't use this on real systems.** AES is a deployed standard and is considered secure. The work here is theoretical / pedagogical. **Never attempt cryptanalysis on systems you do not own or are not explicitly authorised to test.**

---

## 📄 Files in this folder

| File | What it is |
|---|---|
| [`math-proof.md`](math-proof.md) | Sketch-level convergence argument (Theorems 1–3 + sample complexity) |
| [`complete-transformer-rl.py`](complete-transformer-rl.py) | Reference Python implementation: transformer student, teacher distillation, RL phase |
| [`transformer-architecture.mermaid`](transformer-architecture.mermaid) | Mermaid diagram of the transformer architecture |

---

## 🧮 What the math-proof actually shows (and doesn't)

The document defines:

- Teacher T(x), student S(x), policy π(a\|s), reward R(a, s), KL divergence D(P‖Q)
- **Distillation loss** L_D = τ² · D(softmax(T(x)/τ) ‖ softmax(S(x)/τ))
- **Policy-gradient objective** J(θ) = 𝔼[Σ_t γ^t R(s_t, a_t)] with advantage A(s, a) = Q(s, a) − V(s)
- **Combined loss** L(θ) = α·L_D(θ) + (1−α)·L_RL(θ)

It then sketches three theorems:

| # | Theorem | What's claimed | Caveat |
|---|---|---|---|
| **1** | Distillation convergence | L_D(θ_t) decreases monotonically; ∇L_D → 0 | Assumes smoothness; doesn't formalise it |
| **2** | Combined-system convergence | Under "appropriate learning rate conditions", Kushner–Clark gives ∇L → 0 | "Appropriate" is left informal |
| **3** | Error bound | ε ≤ ε_D + ε_RL via triangle inequality | Assumes both individual bounds hold; doesn't derive them tightly |

**Sample complexity** is given as N = O(1/ε²) for distillation + O(1/(1−γ)³ε²) for RL, with the RL phase dominating.

The proofs do not address: non-convexity of transformer losses; policy-gradient bias; specific assumptions on the AES distribution; or any cryptanalytic claim that would survive a rigorous adversarial setting. Those are *open problems*, not settled results.

---

## 🧠 Pipeline at a Glance

```
        Teacher T (e.g., Llama)
                │
                ▼  distillation loss  L_D = τ² · D(softmax(T/τ) || softmax(S/τ))
                │
        Student S  (transformer)
                │
                ▼  RL phase            J(θ) = 𝔼[Σ γ^t R(s_t, a_t)]
                │
        Combined loss  L = α · L_D + (1−α) · L_RL
```

---

## ⚠️ Security Considerations

1. **AES remains secure.** No claim in this folder — sketched or otherwise — undermines deployed AES.
2. **Theoretical ≠ practical.** Even rigorous attack-model analyses typically require oracle access or attacker-chosen distributions absent in real deployments.
3. **Do not use this against systems you do not own** or are not authorised to test. Cryptanalysis on someone else's system is illegal in most jurisdictions.
4. **Stay informed.** Cryptographic standards evolve; follow NIST guidance for production use.

---

## 🔗 Related Work

This work connects to:

- **GF2 Algebra and Applications** — Paper 2's permutation-polynomial criterion gcd(k, 2ⁿ−1) = 1 underlies the AES S-box's algebraic structure
- **ARIA Encryption Algorithm** — adjacent algebraic-cryptographic construction
- **Cypha** — the transformer / inference codebase that the reference implementation here resembles
- **Compression Algorithms** — distillation theory is also developed in the GRIA technical memorandum (three-stage GRIA pipeline)
- **Veritas** — formal verification of learning bounds; complementary to this folder's sketch-level analysis

---

## 📖 See Also

- [`GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic crypto foundations
- [`ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — adjacent algebraic AEAD
- [`Compression Algorithms/`](../Compression%20Algorithms/) — distillation theory in GRIA

---

## 🛡️ About This Project

This folder exists to capture the *shape* of an idea — what would a sketch of a transformer-distillation-RL convergence story for cryptanalysis look like? — together with reference code that gives the sketch concrete form. It is **not** a finished cryptanalytic result. The goal is pedagogical and exploratory: useful for understanding the algebra of distillation and policy-gradient, useful as a starting point for someone wanting to make these arguments rigorous. Not useful as an attack on deployed AES.

[← Back to main README](../README.md)
