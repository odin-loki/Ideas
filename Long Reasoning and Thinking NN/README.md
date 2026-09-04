# Long Reasoning and Thinking NN — Unified Hash-Predictive Memory (UHPM)

> **Unified Hash-Predictive Memory (UHPM): a single variational framework that fuses LSH-based memory and hierarchical predictive coding under one free-energy functional `F_total = F_hierarchical + F_coupling + F_sparse`, replacing `O(N²)` self-attention over long contexts with `O(N)` memory and `O(log N)`-style hashed retrieval refined by `~10` Bayesian iterations — and reporting a `289 ×` query-latency speedup vs full attention at `100 K` tokens (`8.1 ms` vs `2 340 ms`) and `744 ×` memory reduction (`2.2 MB` vs `1 638 MB`) on its synthetic long-context benchmark.** The work is honest about its scope: experiments are on synthetic topic-cluster corpora with fixed non-overlapping segments and random static hashes (no learned hashing), retrieval fidelity is `80 – 90 %` of exact attention rather than 100 %, and the implementation note flags a learned-hashing extension as future work. What it offers in exchange is the explicit unification of two normally-disjoint architectures (hash memory and predictive coding) under one variational loss — and the empirical curves to show it is fast.

---

## What this folder is

The standard answer to "how do I attend to a million tokens?" is some form of hashing or sparse approximation grafted on top of an attention block. Reformer uses LSH attention; Linformer uses low-rank projection; FlashAttention reorders the kernel for better cache behaviour; sliding-window architectures decay older tokens. UHPM argues that all of these are partial answers to a more general question: *what is the variational objective that long-context inference is trying to optimise?* If memory retrieval and inference are both Bayesian operations — finding the maximum-posterior context given an evidence stream — they should live inside one loss function and one optimisation loop, not be welded together at runtime.

The folder ships the unification: a three-level memory hierarchy with segment sizes `100 / 1 000 / 10 000` tokens, 64-bit hyperplane LSH at each level, compressed centroid dimension `d′ = 64`, an iterative refinement loop with `T ≈ 10` query iterations and stopping criterion `‖Δs‖ < 10⁻³`, and an empirical demonstration on synthetic topic-cluster corpora that the resulting system is dramatically faster than full attention without unacceptable retrieval fidelity loss.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`UHPM_Research_Paper.md`](UHPM_Research_Paper.md) | Main research paper. Defines `F_total = F_hierarchical + F_coupling + F_sparse`. Theorem 3.1 (dual feedback). Theorem 4.1 / 4.2 (convergence and error schematic bounds, `σ/√s + 1/K + e^(−αT)` form). |
| [`unified_hash_predictive_framework.md`](unified_hash_predictive_framework.md) | Full unified math framework. **`60-page` derivation companion**. |
| [`Implementation_README.md`](Implementation_README.md) | Implementation overview. |
| [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md) | Implementation summary + caveats. |
| [`hash_memory.py`](hash_memory.py) | LSH memory implementation. |
| [`predictive_coding.py`](predictive_coding.py) | Predictive coding implementation. |
| [`unified_system.py`](unified_system.py) | Combined system. |
| [`demo.py`](demo.py) | Runnable demo. |
| [`benchmark.py`](benchmark.py) | Benchmark harness. |

---

## 🧠 The unified architecture

```
F_total = F_hierarchical + F_coupling + F_sparse

         ┌─── Level 0: 100-token segments    ──┐
Memory ──┼─── Level 1: 1 000-token segments  ──┤  64-bit LSH per level
         └─── Level 2: 10 000-token segments ──┘  d' = 64 compressed centroid

Query ──→ iterative refinement (T ≈ 10 iterations, stop when ‖Δs‖ < 10⁻³)
       ──→ Bayesian feedback between levels (Theorem 3.1)
       ──→ retrieved context with calibrated uncertainty
```

---

## 📊 Reported benchmarks (UHPM paper, synthetic 100 K tokens)

| Metric | UHPM | Full attention | k-NN centroid |
|---|---|---|---|
| Query time | **`8.1 ms`** | `2 340 ms` | `45 ms` |
| **Speedup vs full attention** | — | **`289 ×`** | `5.6 ×` |
| Memory | **`2.2 MB`** | `1 638 MB` | `245 MB` |
| **Memory reduction** | — | **`744 ×`** | `111 ×` |
| Per-token signature scaling | `~22 bytes / token` | — | — |

### Retrieval quality

| Metric | Value |
|---|---|
| Top-1 exact match vs brute-force centroid | `81.4 %` |
| Top-5 exact match | `77.1 %` |
| Same-topic presence in top-5 (level 0) | `89.3 %` |
| Same-topic presence in top-10 (level 0) | `82.7 %` |
| Convergence in 5 – 15 iterations | `97 %` of queries |

### Crossover point

UHPM is *slower* than k-NN centroid below `~7 500` tokens because the iterative refinement overhead dominates. The `289 ×` speedup vs full attention emerges as context length grows.

---

## 🚧 Honest caveats (paper §7.2 + IMPLEMENTATION_SUMMARY)

- **Synthetic topic-cluster corpora.** All benchmarks use a constructed long-context dataset, not real natural language with realistic topic structure.
- **Fixed non-overlapping segments.** Real long-context tasks need overlapping windows or dynamic segmentation.
- **Linear identity generative maps in the implementation discussion.** The full nonlinear case is sketched but not benchmarked.
- **Random static hashes — not learned.** The LSH planes are set once at init. Learned hashing is named as future work.
- **`80 – 90 %` retrieval fidelity vs 100 % exact attention.** This is the trade-off — not a regression, but a deliberate accuracy-for-speed exchange.
- **Preprint dated March 2026.** Not peer-reviewed.
- **Full test suite recommended** in implementation summary; some tests are optional / pending.
- **Below `~7 500` tokens, UHPM is slower than k-NN centroid.** Use accordingly.

---

## 🎯 What this displaces

| Standard | Limitation | What UHPM offers |
|---|---|---|
| Full self-attention | `O(N²)` memory + compute | `O(N)` memory, `289 ×` faster at `100 K` |
| Reformer LSH attention | LSH bolted on | LSH as part of unified variational objective |
| Linformer / Performer | Approximation without uncertainty | Iterative Bayesian refinement with calibrated uncertainty |
| Sliding window | Drops old context | Hierarchical 3-level retention |
| Centroid k-NN | Fast but no inference | UHPM = k-NN + predictive-coding inference loop |

---

## 🔗 Related work in this repo

- [`odin-loki/cellai`](https://github.com/odin-loki/cellai) — sister non-attention sequence architecture
- [`odin-loki/cypha`](https://github.com/odin-loki/cypha) — HRNA inference + training stack
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — Izaac shared-PRF + NMP harmonic-spectrum theory
- [`../Statistical Generation/`](../Statistical%20Generation/) — hash-compression sister technique (`M = 2³²`)
- [`../NN Shortcuts/`](../NN%20Shortcuts/) — Streaming Geometry Framework + Algebraic Autopsy (efficiency frame)
- [`../Veritas/`](../Veritas/) — formal-verification framework
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — adjacent Bayesian-inference architecture

---

[← Back to main README](../README.md)
