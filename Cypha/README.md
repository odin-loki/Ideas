# Cypha — Harmonic Recursive Neural Architecture (HRNA) inference, training, and tooling

> **A complete inference-and-training stack for HRNA (Harmonic Recursive Neural Architecture): a Python reference, a CMake-built native C++ core with byte-identical parity fixtures, a REST server, optional CUDA acceleration, and a Qt-based desktop Studio IDE — `188` pytest tests + `33` CTest cases keep the Python and native paths bit-exact via 13+ named parity harnesses (`cypha_parity`, `memory_train_parity`, `quantile_dif_train_parity`, `mke_train_step_parity`, `regression_m4_parity`, …).** Cypha is the *implementation leg* of the HRNA research programme — the theoretical backbone (`σ_k ∝ 1/k` harmonic spectra, `α ≈ 0.85` SGD narrative) lives in the [NMP neural-compression research paper in `../Compression Algorithms/`](../Compression%20Algorithms/NMP_neural_compression_research_paper.md). The unusual move is the dual-stack trust model: every research-grade Python feature has a byte-for-byte native equivalent, validated by parity tests, so research code and runtime production are the same artefact.

---

## What this folder is

Most ML research repositories are Python-only and slow; most production ML runtimes are C++-only and inscrutable. The trade-off is real — research velocity vs deployment speed — and it is what most teams accept. Cypha tries to refuse the trade-off by maintaining a *parity contract* between a clear Python implementation and a fast native C++ core, with `188 + 33 = 221` automated tests verifying that they produce byte-identical outputs on a battery of named fixtures. Add a REST server, optional CUDA acceleration, a SQLite-backed persistent state (amalgamated `3.47.2` build option), a Qt desktop Studio for interactive exploration, and you have a stack that is genuinely production-shaped while preserving research debuggability.

The `InferenceEngine` defaults to `OOD_THRESHOLD = 3.0` for out-of-distribution flagging, exposes batch and single-prediction paths, integrates a GH (generalised-hyperbolic) gate for heavy-tailed input handling, supports online corrections, and reports regression uncertainty. The `TrainerConfig` is a `CyphaDIF` (differential-information-field) classifier with `feat_dim = 128`, `field_dim = 128`, `rff_D = 256`, expert-mixture configurable at `n_experts = 8`, temperature `1.15`, context window `32`, and three independently-tuned learning rates: world `0.008`, delta `0.05`, encoder `0.002`. Online and batch training both supported.

The folder is engineering, not theory. Read [`../Compression Algorithms/NMP_neural_compression_research_paper.md`](../Compression%20Algorithms/NMP_neural_compression_research_paper.md) for the harmonic-spectrum theory it claims to implement.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`README.md`](README.md) | This file. |
| [`native/README.md`](native/README.md) | Native C++ core build & test guide. CTest harness, parity test inventory, SQLite amalgamation, CUDA smoke test. |
| [`docs/README.md`](docs/README.md) | Documentation index. |
| [`docs/port/PORT_CONTRACT.md`](docs/port/PORT_CONTRACT.md) | The parity contract — what Python and native must agree on, fixture by fixture. |
| [`docs/verify/VERIFICATION_STATUS.md`](docs/verify/VERIFICATION_STATUS.md) | Verification status — current parity test results across all fixtures. |
| [`cypha_studio/core/inference.py`](cypha_studio/core/inference.py) | Python `InferenceEngine`. Batch + single predict, GH gate, OOD detection, online corrections, regression uncertainty. |
| [`cypha_studio/core/trainer.py`](cypha_studio/core/trainer.py) | Python `Trainer`. `TrainerConfig` defaults, online + batch training. |
| [`cypha_studio/server/api.py`](cypha_studio/server/api.py) | REST API server. |
| [`cypha_studio/`](cypha_studio/) | Qt-based desktop Studio IDE. |
| [`native/`](native/) | C++ native core. CMake build. |

> **Note on file paths.** The repository's HRNA research paper is *not* inside `Cypha/`; it lives at [`../Compression Algorithms/NMP_neural_compression_research_paper.md`](../Compression%20Algorithms/NMP_neural_compression_research_paper.md). Cypha is the engineering implementation; NMP is the theoretical paper.

---

## 🧠 The dual-stack architecture

```
┌─────────────────────────────────────────────────────┐
│                  Cypha Studio (Qt)                   │
│           Interactive desktop GUI / IDE              │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│            REST Server (cypha_studio/server)         │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
       ┌─────────────────────────────────────┐
       │   InferenceEngine (Python reference) │
       │   Trainer / TrainerConfig            │
       │   CyphaDIF differential-info-field   │
       └─────────────────────────────────────┘
                           │
                           ▼ ↕ parity contract: 188 pytest + 33 CTest
       ┌─────────────────────────────────────┐
       │       Native C++ core (CMake)        │
       │       SQLite 3.47.2 persistence      │
       │       Optional CUDA acceleration     │
       └─────────────────────────────────────┘
```

---

## ⚙️ Reference defaults

### `InferenceEngine`

| Parameter | Default |
|---|---|
| `OOD_THRESHOLD` | `3.0` |
| Batch / single prediction | both supported |
| GH gate | yes (heavy-tailed input handling) |
| Online corrections | yes |
| Regression uncertainty | yes |

### `TrainerConfig` (`CyphaDIF`)

| Parameter | Default |
|---|---|
| `feat_dim` | `128` |
| `field_dim` | `128` |
| `rff_D` | `256` |
| `n_experts` | `8` |
| `temperature` | `1.15` |
| `context_win` | `32` |
| LR — world | `0.008` |
| LR — delta | `0.05` |
| LR — encoder | `0.002` |
| Modes | online, batch |

---

## 🧪 Parity test inventory (selected, from `native/README.md`)

| Test | What it verifies |
|---|---|
| `cypha_parity` | Top-level Python ↔ native parity |
| `memory_train_parity` | Memory-module training step |
| `quantile_dif_train_parity` | Quantile DIF training step |
| `mke_train_step_parity` | MKE training step |
| `regression_m4_parity` | M4 regression |
| `cuda_smoke` | CUDA path smoke test |

(Full inventory in [`native/README.md`](native/README.md). Total: **`188 pytest + 33 CTest`** tests.)

---

## 🚧 Honest framing

- **HRNA theory lives elsewhere.** The harmonic-spectrum / `σ_k ∝ 1/k` / `α ≈ 0.85` claims are in [`../Compression Algorithms/NMP_neural_compression_research_paper.md`](../Compression%20Algorithms/NMP_neural_compression_research_paper.md), not derived inside this folder.
- **The proof surface is parity correctness, not leaderboard ML accuracy.** No "we beat X on benchmark Y" — instead, "Python and native produce byte-identical results across this fixture matrix."
- **Future waves** (in the engineering docs): Qt streaming, packaged binaries, multi-model REST.
- **Optional CUDA** — the native core works without GPU; CUDA is a build flag.

---

## 🎯 What this displaces

| Standard | Limitation | What Cypha offers |
|---|---|---|
| Python-only research repo | Slow at deploy time | Native parity-validated C++ |
| C++-only production runtime | Hard to iterate on | Python reference is canonical |
| ML framework + serve-from-Python | Glue code is fragile | One stack, two backends, parity tests |
| Notebook + flask script | No persistence | SQLite-backed state |
| Custom REST + Python | No GUI | Qt Studio integration |

---

## 🔗 Related work in this repo

- [`../Compression Algorithms/`](../Compression%20Algorithms/) — **HRNA / NMP theoretical home** (`NMP_neural_compression_research_paper.md`)
- [`../Cell AI/`](../Cell%20AI/) — sister neural architecture (CellularAI)
- [`../Long Reasoning and Thinking NN/`](../Long%20Reasoning%20and%20Thinking%20NN/) — UHPM long-context architecture
- [`../Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator framework
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — Paper 7 explicitly bridges to Cypha
- [`../Statistical Scheduler/`](../Statistical%20Scheduler/) — sister Python+monitoring stack
- [`../New Classes of Electrical Components/`](../New%20Classes%20of%20Electrical%20Components/) — adjacent `Cypha.py` (Omega DIF encoder, separate work)

---

[← Back to main README](../README.md)
