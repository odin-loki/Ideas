# Electromechnical Inspired Algorithms — three historical computers, three Python rebuilds

> **Algorithms reconstructed from first principles after the machines that ran them.** Three classical electromechanical computers — Babbage's Difference Engine (1822 design, never fully built in his lifetime), the Antikythera mechanism (~150–100 BC) reframed as a "military" / strategic computer, and the WWII US Navy Torpedo Data Computer (TDC) — each documented as a research paper, a deeper companion document, and a working Python implementation.

---

## ⚙️ What this folder is

Three parallel triplets (paper + companion documentation + Python implementation), each rebuilding a historical electromechanical computer's algorithm in software.

---

## 📄 The three triplets

### 1. Babbage Difference Engine

| File | Role |
|---|---|
| [`paper1_babbage_difference_engine.md`](paper1_babbage_difference_engine.md) | Research paper |
| [`babbage_difference_engine_algorithm.md`](babbage_difference_engine_algorithm.md) | Algorithm-level companion document |
| [`babbage_python_implementation.py`](babbage_python_implementation.py) | Python implementation |

### 2. Military Antikythera

| File | Role |
|---|---|
| [`paper2_military_antikythera.md`](paper2_military_antikythera.md) | Research paper |
| [`complete_military_antikythera_specification.md`](complete_military_antikythera_specification.md) | Full mechanism specification |
| [`military_antikythera.py`](military_antikythera.py) | Python implementation |

### 3. Torpedo Data Computer (TDC)

| File | Role |
|---|---|
| [`paper3_torpedo_data_computer.md`](paper3_torpedo_data_computer.md) | Research paper |
| [`tdc_complete_documentation.md`](tdc_complete_documentation.md) | Full algorithm documentation |
| [`tdc_python_showcase.py`](tdc_python_showcase.py) | Python implementation |

> Earlier README copy missed the three companion documents (`babbage_difference_engine_algorithm.md`, `complete_military_antikythera_specification.md`, `tdc_complete_documentation.md`). They are the canonical reference for each device's algorithm; the three "paper" files are research-style overviews.

---

## ⚙️ What's actually being preserved

- **Babbage Difference Engine.** Polynomial evaluation by finite differences — the algorithm that drove the gear-and-wheel arithmetic columns. The Python implementation reproduces the engine's column logic and difference-table updates.
- **Antikythera mechanism (military framing).** Originally an astronomical / calendar device using nested gear trains and pin-and-slot mechanisms. The "military" framing here repositions the gear logic as a strategic / temporal-prediction computer. The full mechanism specification covers gear ratios, dial layouts, and prediction outputs.
- **TDC (US Navy WWII).** Analog electromechanical computer that solved the torpedo fire-control geometry: target bearing, range, course, speed → torpedo gyro angle. The Python showcase implements the cam-driven trigonometric computations and the "angle solver" that made fire-control achievable on a moving submarine.

Each implementation is a faithful *algorithmic* reconstruction — Python obviously isn't a gear train, but the computational structure (state held in column variables / cam positions, deterministic clocked update) preserves the mechanical original.

---

## 🚧 Honest framing

- These are pedagogical / historical reconstructions, not novel algorithms. The novelty is in the explicit mapping from mechanical state machines to software state machines.
- The "Military Antikythera" framing is a reinterpretation; the historical Antikythera mechanism was an astronomical device, not a military one.
- Folder name is misspelled (`Electromechnical` rather than `Electromechanical`); preserved for stable URLs.

---

## 🔗 Related work in this repo

- [`../CPU/`](../CPU/) — early Verilog OS-acceleration experiment (electronic counterpart to these mechanical computers)
- [`../Future C++/`](../Future%20C++/) — managed-language design conversation
- [`../RNGS/`](../RNGS/) — physical random-number sources (Turbulent Flow RNG)
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — modern intelligence engine (algorithmic descendant of the TDC fire-control problem)
- [`../Filtering/`](../Filtering/) — modern Bayesian-tracking analogue of TDC's geometry solver
- [`../Cypha/`](../Cypha/) — modern HRNA neural inference stack

---

[← Back to main README](../README.md)
