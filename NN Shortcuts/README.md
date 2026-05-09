# NN Shortcuts — Streaming Geometry Framework + Algebraic Autopsy

> **Two papers, one programme.** A unified framework (**SGF** — Streaming Geometry Framework) showing that every effective neural-network acceleration technique reduces to one underlying principle (Incremental Riemannian Estimation), plus a companion **Algebraic Autopsy** paper that diagnoses the *implicit* computational algebra of trained networks (tropical routing + Grassmannian low-rank + dense $(\mathbb{R}, +, \times)$). The autopsy directly generates the structural priors that SGF exploits.

---

## ⚡ What this folder is

Two long research papers, each shipping a "paper" version and a longer / more recent variant, plus the C++17 / CUDA library specification embedded in the SGF paper.

---

## 📄 Files

| File | Role |
|---|---|
| [`sgf_paper.md`](sgf_paper.md) | **The Streaming Geometry Framework** — surveys 16 canonical NN acceleration techniques, identifies three meta-patterns (Streaming Sufficiency, Spectral Geometry, Data–Compute Duality), and derives the *Incremental Riemannian Estimation* (IRE) principle that unifies them. SGF realises IRE as an architecture in which every component (optimiser, normaliser, router, scheduler, memory manager, inference engine) is an online sufficient statistic on a curved parameter manifold. Includes specifications for the `sgf_lib` C++17 / CUDA library. |
| [`SGF_Paper_StreamingGeometryFramework.md`](SGF_Paper_StreamingGeometryFramework.md) | Extended / consolidated SGF paper |
| [`algebraic_autopsy.md`](algebraic_autopsy.md) | **Algebraic Autopsy** — post-hoc analysis of trained NNs using four diagnostics: (i) SV power-law exponent α, (ii) Marchenko–Pastur bulk deviation, (iii) ReLU dead-unit sparsity (tropical content), (iv) effective-rank Grassmannian backbone. Demonstrated on a prime-classification MLP: implicit algebra is **tropical + Grassmannian + 11 % dense** (ℝ, +, ×); $α = 0.427$ sits between data-prior $α = 0.37$ and reference architecture $α = 0.85$. |
| [`algebraic_autopsy_paper.md`](algebraic_autopsy_paper.md) | Extended / consolidated autopsy paper |

> Earlier README copy referenced a single `research_paper.md` that does not exist; the actual scope is the SGF + Algebraic Autopsy pair above.

---

## 🧠 The unifying principle

The two papers describe a single closed loop:

1. **Algebraic Autopsy → structural diagnosis.** Diagnose what algebra a *trained* network actually uses (tropical / Grassmannian / dense fractions; α exponent; effective rank).
2. **Five algebraic moves.** Semiring substitution, symmetry exploitation, basis factorisation, idempotent sparsification, sufficient-statistic compression — argued to be exhaustive over known architectural-efficiency improvements.
3. **SGF → architectural realisation.** Replace each batch component with an *online sufficient statistic on a curved parameter manifold*, derived from one of the three meta-patterns (Streaming Sufficiency, Spectral Geometry, Data–Compute Duality).
4. **IRE as the hidden principle.** All three meta-patterns are projections of *Incremental Riemannian Estimation* — the proper unit of computation in NN training is a streaming statistic on a Riemannian (Fisher-metric) manifold.

Concrete predictions in the SGF paper include ZClip-triggered automatic WSD cooldown, EoS-adaptive checkpointing, spectral-health monitoring derived from the autopsy, and algebra-aware layer primitives.

---

## 🚧 Honest framing

- **Theoretical / framework work** rather than a fielded benchmark suite. The SGF paper specifies a C++17 / CUDA library (`sgf_lib`) that realises every prediction; *the library itself is not in this folder*.
- The **Algebraic Autopsy** prime-classification MLP demonstration shows a low-rank variant achieving identical accuracy at 0.76× parameter count and 0.75× FLOPs — small-scale, intentionally so, to make the autopsy methodology auditable.
- Folder name "NN Shortcuts" is broader than what these papers actually do — they propose a *unifying framework* for shortcut techniques, not a catalogue of new shortcuts.

---

## 🔗 Related work in this repo

- [`../Cypha/`](../Cypha/) — HRNA inference + training stack (parity-validated native core); a candidate test bed for the SGF library
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — NMP / GRIA / Izaac frameworks; spectral-geometry overlap
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic primitive structure (semiring substitution is one of SGF's five moves)
- [`../Long Reasoning and Thinking NN/`](../Long%20Reasoning%20and%20Thinking%20NN/) — UHPM long-context architecture (relevant to streaming-sufficiency acceleration)
- [`../Cell AI/`](../Cell%20AI/) — non-attention sequence modelling (parallel architectural research)
- [`../Prime Number Generator/`](../Prime%20Number%20Generator/) — the prime-classification task in the Algebraic Autopsy demo connects naturally to prime-pattern theory
- [`../Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator (category theory + Lévy + IT)

---

[← Back to main README](../README.md)
