# Long Reasoning and Thinking NN — Unified Hash-Predictive Memory (UHPM)

> **One unified architecture, two literatures.** The folder builds a single variational framework, **UHPM = Unified Hash-Predictive Memory**, in which locality-sensitive hashing memory retrieval and hierarchical predictive coding are coupled through one free-energy objective. Theoretical proofs, an algorithm, and a working NumPy reference implementation are all in scope.

---

## 🧠 What this folder is

A research paper, a unified-system framework writeup, an implementation summary, a working NumPy reference (split into hash memory, predictive coding, and a unified system), plus benchmark and demo harnesses. The design target is **long-context inference** at scales (≥ 10⁶ tokens) that defeat dense self-attention.

Earlier README copy expanded UHPM as "Unified Hypothesis Planning Machine" — that gloss does not appear in any source document and has been corrected. The actual expansion, taken from the title of `UHPM_Research_Paper.md`, is **Unified Hash-Predictive Memory**.

Attribution: **Odin · Independent Research · NSW, Australia · March 2026**.

---

## 📄 Files

| File | Role |
|------|------|
| [`UHPM_Research_Paper.md`](UHPM_Research_Paper.md) | Primary research paper — variational framework, theorems, benchmarks, references |
| [`unified_hash_predictive_framework.md`](unified_hash_predictive_framework.md) | System framework writeup |
| [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md) | Implementation notes |
| [`Implementation_README.md`](Implementation_README.md) | How to run the reference code |
| [`unified_system.py`](unified_system.py) | Top-level joint inference loop |
| [`hash_memory.py`](hash_memory.py) | Random-hyperplane LSH index, hierarchical multi-resolution memory |
| [`predictive_coding.py`](predictive_coding.py) | Hierarchical predictive coding inference module |
| [`benchmark.py`](benchmark.py) | Benchmark harness vs O(N²) attention and centroid k-NN |
| [`demo.py`](demo.py) | Worked example |

---

## 🔑 Core insight

Both processes — LSH bucket selection and predictive-state updating — emerge as gradient flows on **one** functional:

$$F_\text{total} = F_\text{hierarchical} + F_\text{coupling} + F_\text{sparse}$$

This produces automatic **bidirectional** feedback: inference states predict which hash buckets are relevant (Inference → Hash), while retrieved memories constrain inference states via coupling gradients (Hash → Inference). Neither feedback loop is engineered; both fall out of differentiating the same scalar objective.

---

## 📐 Architectural details

- **Hierarchical memory** — three resolution levels: 100-token / 1 000-token / 10 000-token segments.
- **LSH** — 64-bit random-hyperplane (SimHash) over compressed embeddings, Hamming-distance bucket lookup.
- **Predictive coding** — internal states evolve via $\partial s / \partial t = -\nabla_s F$, producing approximate Bayesian inference at runtime.
- **Memory representation** — ~20 bytes per token versus ~16 KB per token for dense KV caches (≈ 700× compression).

---

## 📊 Headline results (from §1 / §6 of the paper)

| Property | Value |
|----------|-------|
| Memory scaling | **O(N)** (linear) |
| Query complexity | **O(T · K · d)** (constant in N at fixed K) |
| Memory compression vs dense KV cache | **400–800×** |
| Retrieval fidelity retained | 80–90 % |
| Speedup vs O(N²) attention at 100 K tokens | **~290×** |
| Memory reduction vs naive k-NN at 100 K tokens | **~70×** |
| Convergence | 5–15 gradient steps regardless of context size |
| Demonstrated context length | up to 10 M+ tokens on commodity hardware |

Theoretical results in the paper:

- **Theorem 3.1** — single $F_\text{total}$ produces bidirectional coupling.
- **Theorem 4.1** — convergence to a fixed point under mild Lipschitz conditions.
- **Theorem 4.2** — approximation-error bounds in terms of hash precision, segment size, iteration count.

---

## 🧪 Reference implementation

~1 600 lines of pure NumPy across the five Python modules listed above. Designed as readable scaffolding rather than a production transformer; benchmark harness compares against O(N²) attention and centroid k-NN baselines.

---

## 🚧 Honest framing

- Benchmarks are on **synthetic corpora** up to 500 K tokens (with the implementation supporting 10 M+). The paper does not claim end-to-end LM perplexity competitive with dense transformers on natural-language benchmarks.
- The architecture targets a different operating point — long-context retrieval where dense attention is infeasible — not raw perplexity at short context.
- Coupling derivations require mild Lipschitz conditions made explicit in §4.

---

## 🔗 Related work in this repo

- [`Cell AI/`](../Cell%20AI/) — biologically-motivated alternative to attention; predictive-coding lineage shared
- [`NN Shortcuts/`](../NN%20Shortcuts/) — Streaming Geometry Framework / Algebraic Autopsy; complementary efficiency literature
- [`Compression Algorithms/`](../Compression%20Algorithms/) — Izaac / GRIA / NMP information-theoretic compression at the model level
- [`Cypha/`](../Cypha/) — full ML stack (HRNA architecture); could host UHPM as a memory module
- [`Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator with hash-based context compression

---

[← Back to main README](../README.md)
