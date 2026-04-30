# Cypha — HRNA inference, training, and tooling

> **🔷 Overview**: A neural-network inference and training framework with a Python core, native (C++/CMake) hot path, REST API, and a desktop **Studio** GUI. The architectural concept is **HRNA — Harmonic Recursive Neural Architecture**.

---

## 🔷 Overview

**Cypha** is a working software project — not a paper folder. It implements an end-to-end neural inference and training stack, with a Python reference and a parity-validated native (C++) hot path. The acronym **HRNA** (referenced in companion papers in `Compression Algorithms/`) stands for **Harmonic Recursive Neural Architecture** — a hierarchical Nonlinear Manifold Projection (NMP) codec whose recursive stages each correspond to one level of manifold projection, predicting harmonic singular-value spectra σ_k ∝ 1/k.

The folder is a real codebase with tests, parity fixtures, native bindings, a REST server, and a Qt-based studio.

### What's actually here

- **Python core** + **native C++ core** (`native/`, built via CMake)
- **REST API** (FastAPI / Uvicorn — `cypha_studio/server/api`)
- **Studio GUI** (PySide6 + pyqtgraph, `cypha_studio/`)
- **Parity fixtures** — committed assets that verify Python ↔ native equivalence
- **Acceleration backends** — CPU, CUDA via CuPy (optional), GPU benches

### How HRNA fits the wider research

The HRNA concept is described in [`Compression Algorithms/NMP_neural_compression_research_paper.md`](../Compression%20Algorithms/NMP_neural_compression_research_paper.md): "the Cypha HRNA (Harmonic Recursive Neural Architecture) system reframes neural networks as hierarchical NMP codecs where each recursive stage corresponds to one level of manifold projection." The harmonic structure of HRNA predicts singular-value spectra governed by σ_k ∝ 1/k (α = 1.0), distinct from the standard SGD power-law value α ≈ 0.85.

---

## 📂 Repository Layout

| Folder | What it contains |
|---|---|
| [`cypha_accel/`](cypha_accel/) | Acceleration backends (GPU/CPU dispatch helpers) |
| [`cypha_studio/`](cypha_studio/) | Desktop GUI + REST server (PySide6, pyqtgraph, FastAPI) |
| [`config/`](config/) | Configuration assets |
| [`docs/`](docs/) | Documentation tree (use / verify / port / studio / benchmarks) |
| [`examples/`](examples/) | Example scripts and use cases |
| [`native/`](native/) | C++ core, CMake build, REST binary, optional Qt stub |
| [`parity_fixtures/`](parity_fixtures/) | Committed parity assets for Python ↔ native equivalence checks |
| [`scripts/`](scripts/) | Helper scripts (profile, benchmark, regen, regression gate) |
| [`tests/`](tests/) | pytest suite (~188 tests + GUI subsets) |

---

## 📚 Key Documentation

| Doc | What it is |
|---|---|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Setup, PR checklist, extended verify commands |
| [`docs/README.md`](docs/README.md) | Documentation hub — organised by use / verify / port |
| [`docs/verify/VERIFICATION_STATUS.md`](docs/verify/VERIFICATION_STATUS.md) | Snapshot: 188 pytest / 33 CTest, known gaps |
| [`docs/verify/ROADMAP.md`](docs/verify/ROADMAP.md) | Milestones M1–M6 (complete) and current engineering horizon |
| [`docs/verify/MAINTENANCE.md`](docs/verify/MAINTENANCE.md) | When to regen fixtures / rebuild native / align schema & REST |
| [`docs/FUTURE.md`](docs/FUTURE.md) | Depth: CUDA, Qt packaging, Web UI, multi-model, ONNX |
| [`docs/port/PORT_CONTRACT.md`](docs/port/PORT_CONTRACT.md) | Normative: `.cypha` v3 binary format, LLR/softmax/GH, REST JSON |
| [`docs/port/PORT_FULL_STACK.md`](docs/port/PORT_FULL_STACK.md) | Replacing Python core + Studio + REST + Qt |
| [`docs/port/PREPROCESSOR_CONTRACT.md`](docs/port/PREPROCESSOR_CONTRACT.md) | `preprocessor.json` next to `model.cypha` |
| [`docs/port/EXPERIMENTS_SCHEMA.md`](docs/port/EXPERIMENTS_SCHEMA.md) | SQLite layout for `ExperimentDB` |

---

## 🧪 Parity Fixtures

`parity_fixtures/` is the contract surface between the Python and native implementations. Each fixture has its own README:

| Fixture | Purpose |
|---|---|
| [`batch_llr/`](parity_fixtures/batch_llr/) | Batch LLR computation parity |
| [`dif_train_replay/`](parity_fixtures/dif_train_replay/) | DIF train replay parity |
| [`memory_train/`](parity_fixtures/memory_train/) | Memory-train parity |
| [`mke_train_step/`](parity_fixtures/mke_train_step/), [`mke_train_extended/`](parity_fixtures/mke_train_extended/) | MKE train-step parity (basic + extended) |
| [`preprocessor/`](parity_fixtures/preprocessor/) | Preprocessor fit/transform parity |
| [`quantile_dif_train/`](parity_fixtures/quantile_dif_train/) | Quantile DIF train parity |
| [`regression_m4/`](parity_fixtures/regression_m4/) | Regression M4 parity |
| [`rff_regression/`](parity_fixtures/rff_regression/) | Random-Fourier-features regression parity |
| [`two_stage_e2e_ridge/`](parity_fixtures/two_stage_e2e_ridge/) | End-to-end two-stage ridge parity |
| [`two_stage_pipeline/`](parity_fixtures/two_stage_pipeline/) | Two-stage pipeline parity |
| [`two_stage_ridge_fit/`](parity_fixtures/two_stage_ridge_fit/) | Two-stage ridge-fit parity |

Regen with `python scripts/generate_parity_fixtures.py` after changing inference or state format. See [`parity_fixtures/README.md`](parity_fixtures/README.md).

---

## 🚀 Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-verify.txt
pip install -r cypha_studio/requirements.txt   # GUI + studio extras
```

Run the studio:

```bash
python cypha_studio/main.py
```

Run headless API:

```bash
python cypha_studio/main.py --headless
```

Run tests:

```bash
pytest tests/
python test_cypha.py
python cypha_studio/test_cypha_studio.py
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full verify-and-test recipe.

---

## 🔗 Related Work

This codebase realises ideas described in adjacent research folders:

- [`Compression Algorithms/`](../Compression%20Algorithms/) — **NMP** (Nonlinear Manifold Projection) and **GRIA** papers; the HRNA acronym is defined in the NMP paper
- [`GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic backbone (Paper 7 explicitly references "Cypha.py classifier (discriminative information field architecture)")
- [`NN Shortcuts/`](../NN%20Shortcuts/) — neural-network shortcut work
- [`Long Reasoning and Thinking NN/`](../Long%20Reasoning%20and%20Thinking%20NN/) — extended reasoning networks
- [`Filtering/`](../Filtering/) — signal-processing context
- [`Statistical Generation/`](../Statistical%20Generation/), [`Statistical Scheduler/`](../Statistical%20Scheduler/) — adjacent statistical ML work

---

## 📖 See Also

- [`EDITORIAL_ROADMAP.md`](../EDITORIAL_ROADMAP.md) — editorial standards and batch history
- [`EDITORIAL_STYLE.md`](../docs/EDITORIAL_STYLE.md) — house style guide

---

## 🛡️ About This Project

Cypha is the *implementation* leg of a research programme whose theoretical leg lives in `Compression Algorithms/` and `GF2 Algebra and Applications/`. The goal is to produce a working, verifiable, parity-tested neural inference and training stack that realises the HRNA concept end-to-end — Python reference for clarity, native core for speed, parity fixtures for trust, and a desktop studio for hands-on experimentation.

[← Back to main README](../README.md)
