# Quantum Graph Optimisation — classical Quantum Approximate Optimisation Algorithm (QAOA) pipeline

> **A fully classical, quantum-shaped graph-optimisation pipeline that combines five layers — `SpectralCompressor` (rank-`k` truncation of the normalised Laplacian `L̃ = I − D^(-1/2) A D^(-1/2)`, recording relative-Frobenius-tail reconstruction error), `ChebyshevEncoder` (Chebyshev polynomial recursion with scale `2/λ_max`, error `O(exp(-Jδ/λ_max))`), `QuantumCircuitSimulator` (QAOA-style γ-phase + Pauli-X-mixing layers on the *compressed* `2^k`-dimensional Hilbert space, with depolarising noise, exact simulation cap `MAX_EXACT_QUBITS = 18` else mean-field, default `10×7` parameter grid), `NoiseSolutionRanker` (down-weight high-`‖η‖` shots with `w = exp(-λ‖η‖)`, default `noise_penalty = 3.0`, where `η` is the bit-marginal deviation between noisy and noiseless Born probabilities), and `SpectralLiftback` (`z = sign(U z_k)` with verified inequality `C(z) ≥ C_k(z_k) − ε_lift |E|`).** All five layers ship with named verification functions: `verify_eckart_young`, `verify_chebyshev_convergence`, `verify_noise_weighting`, `verify_liftback_quality`, `verify_noise_side_data`, plus a `run_full_pipeline_demo` on a Barabási–Albert `n = 80` example. The headline contribution is *noise-aware classical post-processing* (`‖η‖`-weighted aggregation) married to *spectrally-biased QAOA initialisation* — the ansatz is the amplitude-embedded normalised Chebyshev vector, a graph-prior that biases the simulated quantum state toward the Laplacian's leading subspace before any classical optimisation begins. There is no quantum hardware execution and no quantum-advantage claim — the empirical results are demo-level (BA(80,4) cut-fraction prints, planted-partition vs lift-back-bound vs classical-baseline comparisons), the README is explicit that compression yields *approximate* solutions on `G_k` for `G`, and the "Theorem N" labels are software-doc conventions backed by in-code tests (not external publications). What it offers in exchange is a clean, end-to-end *graph-signal → ansatz prior → robust aggregation* pipeline that is auditable layer by layer, with explicit error bookkeeping at each stage.

---

## What this folder is

The dominant approach to quantum-graph optimisation is "build a QAOA circuit, run it on hardware, hope the hardware noise doesn't dominate." This folder takes a different bet: assume we have a classical simulator, assume noise is real and *useful as a signal*, and build a pipeline where every step is auditable. The pipeline pre-compresses the graph spectrally so the QAOA circuit only ever runs on a small `2^k`-dimensional Hilbert space, encodes the compressed signal via Chebyshev polynomials so the ansatz inherits a graph-aware initialisation, and post-processes shots with noise-norm weighting so high-noise samples are systematically down-weighted before the spectral lift-back to the original graph. The result is a fully classical demo, but one that *could* in principle be ported to hardware with the noise-aware ranker remaining sensible.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`README.md`](README.md) | This file — pipeline architecture, layer-by-layer specification, verification functions, demo. |
| [`Quantum_Graph_Optimisation.py`](Quantum_Graph_Optimisation.py) | The implementation. Module docstring is the canonical spec. |

(The README explicitly notes: **no PDF companion**. The Python module is the canonical reference.)

---

## 🧠 The five-layer pipeline

```
Original graph G = (V, E)        ┌──────────────────────────────────────┐
        │                         │  Verification suite                  │
        ▼                         │  - verify_eckart_young               │
┌────────────────────────┐        │  - verify_chebyshev_convergence      │
│ Layer 1                │        │  - verify_noise_weighting            │
│ SpectralCompressor     │        │  - verify_liftback_quality           │
│ L̃ = I - D^(-1/2)A D^(-1/2)      │  - verify_noise_side_data           │
│ rank-k truncation      │        │  - run_full_pipeline_demo (n=80 BA) │
│ reconstruction_error   │        └──────────────────────────────────────┘
└────────────────────────┘
        │
        ▼
┌────────────────────────┐
│ Layer 2                │
│ ChebyshevEncoder       │
│ scale 2/λ_max          │
│ error O(exp(-Jδ/λ_max))│
└────────────────────────┘
        │
        ▼
┌────────────────────────┐
│ Layer 3                │
│ QuantumCircuitSimulator│
│ MaxCut Hamiltonian on  │
│ A_k = U^T A U          │
│ Initial state =         │
│  amplitude-embedded     │
│  normalised Chebyshev   │
│ MAX_EXACT_QUBITS = 18  │
│ depolarising noise     │
│ default 10×7 grid       │
└────────────────────────┘
        │
        ▼
┌────────────────────────┐
│ Layer 4                │
│ NoiseSolutionRanker    │
│ w = exp(-λ ‖η‖)        │
│ default noise_penalty  │
│ = 3.0                  │
└────────────────────────┘
        │
        ▼
┌────────────────────────┐
│ Layer 5                │
│ SpectralLiftback       │
│ z = sign(U z_k)        │
│ C(z) ≥ C_k(z_k) - ε_lift|E|
│ ε_lift = reconstruction_error
└────────────────────────┘
        │
        ▼
Original-graph cut + spectral_maxcut_baseline (Fiedler sign cut)
```

---

## 🚧 Honest framing

- **No quantum hardware execution.** All "quantum" steps are simulated.
- **No quantum-advantage claim.** Compression yields approximate solutions on `G_k` for `G`.
- **"Theorem N" labels are software-doc conventions** + in-code tests, not external publications.
- **Mean-field plus aggressive graph compression** can misalign with true MaxCut structure; lift-back is *not* guaranteed globally optimal.
- **Empirical claims are demo-level only** — `n = 80` BA graph print-outs and planted-partition examples; no peer-reviewed benchmark suite is bundled.

---

## 🎯 What this is genuinely interesting for

| Audience | Use |
|---|---|
| Quantum-classical algorithm researcher | Worked example of "what does noise-aware classical post-processing of QAOA shots look like?" |
| Graph-spectral methods practitioner | Spectrally-biased ansatz initialisation as a graph prior |
| Hardware QC architect | Auditable layer-by-layer error bookkeeping (Eckart–Young, Chebyshev decay, lift-back inequality) |
| Anyone wanting a runnable, fully-classical QAOA-shaped baseline | This is one |
| Anyone wanting hardware quantum advantage on graphs | Wrong folder |

---

## 🔗 Related work in this repo

- [`../Quantum Diamond Wafer/`](../Quantum%20Diamond%20Wafer/) — sibling QC research (NV / metamaterial substrate)
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — spectral / harmonic compression theory
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic foundations
- [`../General Math Papers/`](../General%20Math%20Papers/) — LCRP `O(n log n)` decision procedure
- [`../Filtering/`](../Filtering/) — sister Bayesian-inference pipeline
- [`../Statistical Generation/`](../Statistical%20Generation/) — sister classical-statistics framework
- [`../Veritas/`](../Veritas/) — verification framework

---

[← Back to main README](../README.md)
