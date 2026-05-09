# Quantum Graph Optimisation — quantum-classical hybrid compressed graph processor

> **Quantum-inspired classical pipeline, not a physical quantum algorithm.** A five-layer hybrid optimiser: spectral Laplacian compression → Chebyshev coefficient encoding → **classical QAOA simulation** on the compressed graph → noise-side-data ranking of candidate cuts → spectral lift-back to the original graph. Reference Python implementation only.

---

## 📊 What this folder is

A single Python module (`Quantum_Graph_Optimisation.py`) implementing a **quantum-classical hybrid compressed graph processor** — a classical simulator that runs a QAOA-style routine on a spectrally-compressed graph, ranks candidates using noise-as-side-information, and lifts the result back to the original graph. The "quantum" in the title refers to **quantum-inspired structure simulated classically**, not execution on quantum hardware.

Earlier README copy referenced a `Quantum_Graph_Optimisation.pdf` that **does not exist** and a `quantum_graph_optimisation.py` (lowercase) that does not exist either; the actual file is `Quantum_Graph_Optimisation.py`. Both have been corrected.

---

## 📄 Files

| File | Role |
|------|------|
| [`Quantum_Graph_Optimisation.py`](Quantum_Graph_Optimisation.py) | Full reference implementation — five-layer pipeline, classical QAOA simulator, theorem stress tests |

---

## 🏗 The five-layer pipeline (from the module docstring)

| Layer | Function | Operation |
|-------|----------|-----------|
| 1 | `SpectralCompressor` | $G$ ($n$ nodes) $\to G_k$ ($k$ super-nodes) via spectral Laplacian compression |
| 2 | `ChebyshevEncoder` | $G_k\to$ coefficient vector $c\in\mathbb{R}^{J+1}$ (Chebyshev expansion) |
| 3 | `QuantumCircuitSimulator` | Initialise $|\psi_c\rangle$ from Chebyshev coefficients; run **classical QAOA** simulation on $H_k$; collect noise side-data $\eta$ |
| 4 | `NoiseSolutionRanker` | Weight shots by $\|\eta\|$; rank candidate cuts |
| 5 | `SpectralLiftback` | Lift compressed solution $z_k\in\{-1,+1\}^k$ back to $z\in\{-1,+1\}^n$ |

### v2 fixes recorded in the docstring

- Chebyshev coefficients now actually initialise the QAOA quantum state (Layer 2 → 3 wired correctly).
- `ref_state` is thread-local (passed explicitly, not stored on `self`).
- Theorem 5 test checks the spectral error bound directly.
- `verify_noise_side_data()` stress-tests noise-as-side-information at high noise rates.
- Classical MaxCut baseline added via Fiedler-vector spectral relaxation.

---

## 🧪 Comparators

The module includes a classical MaxCut baseline using **Fiedler-vector spectral relaxation** so the QAOA-simulator output can be compared against a sane non-quantum baseline on the same compressed graph.

---

## 🚧 Honest framing

- This is **classical software**. There is no execution on a quantum device, and the README does not claim quantum advantage.
- The "QAOA simulation" refers to a small-state classical simulation of the QAOA ansatz on the spectrally-compressed graph — useful for studying compressed-graph optimisation, not as a stand-in for hardware QAOA on the full graph.
- Spectral compression introduces a **reconstruction error** (tracked in the `CompressedGraph` dataclass); solutions on $G_k$ approximate solutions on $G$.
- No companion paper is currently in this folder — the module's own docstrings, theorem-stress-tests, and inline comments are the authoritative specification.

---

## 🔗 Related work in this repo

- [`Quantum Diamond Wafer/`](../Quantum%20Diamond%20Wafer/) — physical quantum-computing substrate research (QDMP framework, CVD pathways)
- [`GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — Boolean / spectral structures relevant to QAOA encodings
- [`Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator framework (heavy-tailed sampling and hash-based context compression)
- [`Compression Algorithms/`](../Compression%20Algorithms/) — Izaac / GRIA / NMP information-theoretic compression
- [`Fungal Network Algorithm/`](../Fungal%20Network%20Algorithm/) — alternative bio-inspired graph routing

---

[← Back to main README](../README.md)
