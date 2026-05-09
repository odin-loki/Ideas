# Statistical Generation — Universal Statistical Generator framework

> **Category theory + Lévy processes + information theory, unified.** A framework for data generation in which generators form a mathematical *category* with composition rules, the underlying random measure is built from Lévy triplets $(\mu,\sigma^2,\Pi)$, and information-theoretic filtration controls efficiency. Every claim is paired with computational verification; a working Python implementation ships with the papers.

---

## 📊 What this folder is

A research codebase: a unified-framework writeup, two technical papers, a complete-proof document, a separate verification document, plus a working NumPy/Python implementation and worked examples.

---

## 📄 Documents

| File | Role |
|---|---|
| [`Statistical Generation.md`](Statistical%20Generation.md) | **Universal Statistical Generator Framework** — the unified writeup. Provable correctness via category theory, universal applicability via Lévy-process theory, optimal efficiency via information-theoretic filtration, deterministic / reproducible behaviour. |
| [`paper1_categorical_levy_framework.md`](paper1_categorical_levy_framework.md) | Paper 1 — categorical-Lévy framework |
| [`paper2_state_explosion_hash_compression.md`](paper2_state_explosion_hash_compression.md) | Paper 2 — state-explosion and hash compression |
| [`complete_math_proof_document.md`](complete_math_proof_document.md) | All theorem statements with full proofs |
| [`universal_generator_theory_verified.md`](universal_generator_theory_verified.md) | Computational-verification companion to the proofs |
| [`classical_methods_comparison.md`](classical_methods_comparison.md) | Side-by-side comparison vs. classical generative methods |

## 🐍 Code

| File | Role |
|---|---|
| [`universal_generator.py`](universal_generator.py) | Reference implementation. Core data structures include `LevyTriplet(μ, σ², Π)`; framework primitives for composing generators as categorical morphisms |
| [`advanced_examples.py`](advanced_examples.py) | Worked examples |
| [`Python_examples_README.md`](Python_examples_README.md) | Companion notes for running the examples |

---

## 🧠 What's actually in the framework

- **Category-theoretic composition.** Data generators are objects, composition is the categorical morphism. Modular construction of complex systems from simple components is a theorem, not an aspiration.
- **Lévy-process unification.** The Lévy triplet $(\mu, \sigma^2, \Pi)$ unifies continuous diffusion ($\sigma^2$) and discrete jumps ($\Pi$, the Lévy measure) under one parameterisation — heavy-tailed categorical distributions are a special case.
- **Information-theoretic filtration.** Filtration steps are proven optimal in the Shannon-entropy sense; this gates the state-explosion / hash-compression result of Paper 2.
- **Computational verification.** Every theorem has a paired numerical check in `universal_generator_theory_verified.md` and the Python harness.

---

## 🚧 Honest framing

- The framework's strongest claims (categorical composition, Lévy-process universality) are mathematical results, not empirical performance numbers. Earlier README copy listed application areas ("financial modelling", "queueing theory") that are not covered in the source papers.
- The hash-compression result is the only place where "state-explosion management" is rigorously argued; treat that as the canonical reference rather than the README summary.

---

## 🔗 Related work in this repo

- [`../Statistical Scheduler/`](../Statistical%20Scheduler/) — application of the same statistical-ML toolkit to distributed scheduling (LinTS / PID / CFS)
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — Izaac (deterministic shared randomness) and NMP/GRIA frameworks; complementary information-theoretic backbone
- [`../Izaac as Side Data/`](../Izaac%20as%20Side%20Data/) — applied Izaac protocols
- [`../Filtering/`](../Filtering/) — GH-SR-IMM heavy-tailed Bayesian filter; uses generalised hyperbolic priors that fit naturally into the Lévy-triplet view
- [`../Math Question Generator/`](../Math%20Question%20Generator/) — adjacent generation work in a different domain

---

[← Back to main README](../README.md)
