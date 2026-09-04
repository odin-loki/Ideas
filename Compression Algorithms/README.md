# Compression Algorithms — shared-PRF coordination, graded reversibility, and neural-matrix pruning (Izaac, GRIA, NMP)

> **The canonical home of the Izaac framework, the GRIA graded reversible–irreversible algebra, and the NMP neural-manifold projection codec — three frameworks that, taken together, attempt to unify lossless coding, distribution compression, and neural representation under one information-theoretic vocabulary.** Izaac introduces a deterministic shared-PRF coordination primitive that the meta-theorem of the paper frames as a "free broadcast channel"; GRIA grades systems on a real-valued axis `α ∈ [0, 1]` from fully reversible to fully irreversible (entropy-based); NMP treats neural networks as compression operators with a measurable spectral exponent `α ≈ 0.851 ± 0.122` and an MDL-optimal bottleneck dimension that the paper finds at `P* = 45` for `218.7:1` effective compression.

---

## What this folder is

Compression as practiced in 2025 is split across communities that don't talk to each other: classical source coding (Huffman, Lempel–Ziv, arithmetic), distribution learning (autoencoders, normalising flows), and "shared randomness" tricks (Wyner–Ziv, common-randomness MPC). This folder is an attempt to unify all three by introducing one underlying mechanism — **σ, a deterministic shared pseudo-random stream of size `Θ(λ + log k)`** — and then showing the same mechanism powers (a) coordination protocols that look like they have a free broadcast channel, (b) graded coding schemes that interpolate between lossless and distribution-fitting via a single `α` knob, and (c) neural codecs whose compression ratio is a function of an empirically measurable manifold geometry.

The pitch is: the right primitive isn't compression *or* coordination, it's a deterministic PRF stream that both sides hold, and from there you can build everything else.

---

## 📑 Source documents

### Izaac (the foundation)

| File | Role |
|---|---|
| [`izaac_algorithm_research_paper.md`](izaac_algorithm_research_paper.md) | The Izaac framework. Stream `\|σ\| = Θ(λ + log k)`, fast-forward `O(log n)` (CTR-mode `O(1)`). The **meta-theorem**: shared RNG ≡ "free broadcast channel." Application table claims `gzip ~3.2 → ~1.2 bits/char`-style wins. Ten theorems. |
| [`unified_compression_theory_research_paper.md`](unified_compression_theory_research_paper.md) | State Compression Thesis. Ten Izaac theorems mapped to unified `R · S ≥ C` rate-state inequality rows. |

> **Mirror notice.** Applied Izaac protocols (VRF, NI-MPC sum, leader election, Bloom filter coordination, twelve total) live in [`../Izaac as Side Data/`](../Izaac%20as%20Side%20Data/). This folder is the canonical theoretical home; `Izaac as Side Data/` is the engineered protocol suite.

### GRIA (graded reversible-irreversible algebra)

| File | Role |
|---|---|
| [`compression_algebra_framework.md`](compression_algebra_framework.md) | Algebraic framework. `α ∈ [0, 1]` continuum from fully reversible (`α = 0`) to fully irreversible distribution compression (`α = 1`). |
| [`NN_Compression_Algebra_Framework.md`](NN_Compression_Algebra_Framework.md) | Neural-network-specific extension. |
| [`GRIA_Technical_Memorandum.md`](GRIA_Technical_Memorandum.md) | Technical memo. `α` as a query functional with probe-scale numbers `α(instance) ≈ 0.9997`, `α(distribution) ≈ 0.92`, `α(meta) ≈ 0.70`. Memoriser experiment specs (30 documents, 512 hidden, 300 epochs). |
| [`GRIA/GRIA_framework_Research_Paper.md`](GRIA/GRIA_framework_Research_Paper.md) | Operator-theory paper. **11 axioms**, Jeffries-style `J ≤ 0.951` theoretical ceiling, Phi-Adic ratio `1/φ ≈ 0.618`, J-score `0.889` vs baseline `0.742`. Benchmark exemplars: `XORTropicalHybrid 5072.9 / 100`, Quantum Interference avalanche `~0.49`. |
| [`GRIA/GRIA_Research_Paper.md`](GRIA/GRIA_Research_Paper.md) | Companion paper. |
| [`GRIA/gria_complete.py`](GRIA/gria_complete.py) | Reference Python implementation. |

### NMP (neural manifold projection)

| File | Role |
|---|---|
| [`NMP_neural_compression_research_paper.md`](NMP_neural_compression_research_paper.md) | Functor `F_NN = (Θ, D, C, R, δ, ρ)`; rate `ρ = N · d / P`. **MDL-optimal `P* = 45`** giving **`218.7 : 1`** effective compression on the benchmark. **Power-law spectrum `S_k ~ a · k^(−α)` with `α ≈ 0.851 ± 0.122`**. Intrinsic-dimension profile `{3, 8, 3, 1, 1}` measured on a 3D-manifold-in-ℝ²⁰ synthetic. |

---

## 🧠 The unified frame

| Framework | Primitive | Headline |
|---|---|---|
| **Izaac** | Shared deterministic PRF stream σ | "Free broadcast channel" meta-theorem; `O(log n)` fast-forward; **10 theorems** |
| **GRIA** | `α ∈ [0, 1]` reversibility grade | 11-axiom algebra; `J` operator metric; `J = 0.889` on Phi-Adic vs `0.742` baseline |
| **NMP** | Spectral / manifold geometry | `α = 0.851 ± 0.122`; MDL → `P* = 45`; `218.7 : 1` ratio |

---

## 🚧 Honest caveats

- **Izaac §8.1** explicitly acknowledges:
  - Needs **secure setup** of σ between participants.
  - **σ compromise ⇒ predictability** (entire scheme collapses).
  - **"Shannon-breaking" claims tie to Wyner–Ziv-style side-information setups** — they are not unconditional Shannon violations; the side-info channel exists, it's just amortised over many transmissions.
- **Consensus tables under-specify** that value dissemination still requires messages — the "0 messages" claim applies to *leader selection*, not *proposal propagation*. Companion paper `Izaac as Side Data/izaac_paper2_applications.md` §4.3 spells this out (and cites Dolev–Reischuk's `Ω(n²)` bits worst-case lower bound).
- **GRIA** ceilings (`J ≤ 0.951`, `α` triple) are author-reported; some are framework / heuristic in nature.
- **NMP** spectral fits are author-reported; `R²` ranges from `0.75` to `0.97` across configurations.
- **Author-reported, single-author**. No third-party benchmarks.

---

## 🎯 What this displaces (positioning)

| Standard | What's missed | What the triad adds |
|---|---|---|
| gzip / Lempel–Ziv | No coordination layer | Izaac shared-σ free broadcast |
| Lossless vs lossy split | Hard binary choice | GRIA `α ∈ [0,1]` continuous grade |
| Autoencoders | Black-box bottleneck | NMP measurable manifold geometry, MDL-optimal `P*` |
| Wyner–Ziv | Theoretical, not protocol-engineered | Izaac as engineered drop-in primitive |

---

## 🔗 Related work in this repo

- [`../Izaac as Side Data/`](../Izaac%20as%20Side%20Data/) — applied protocols (VRF, NI-MPC sum, Bloom coordination, leader election, twelve total)
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic underpinnings; GRIA Spectrum Theorem lives here
- [`../Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator (parallel framework, sister information theory)
- [`../RNGS/`](../RNGS/) — RNG portfolio that supports Izaac's σ generator
- [`odin-loki/cellai`](https://github.com/odin-loki/cellai), [`../Long Reasoning and Thinking NN/`](../Long%20Reasoning%20and%20Thinking%20NN/) — neural systems that NMP analyses
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — Meta-DAG RNG used as keyed entropy pump there

---

[← Back to main README](../README.md)
