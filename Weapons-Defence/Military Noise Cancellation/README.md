# TACS — Tactical Acoustic Cancellation System

> **Three-variant active-noise-cancellation platform for military acoustic signature management:** TACS-Personal (3–5 m zone, 16-element wearable), TACS-Mobile (8–15 m, 64-element vehicle), TACS-Fixed (30–60 m, 64-element installation). Nelson–Elliott asymmetric-power simulator (§18) yields **36.3 / 36.0 / 32.4 dB A-weighted** cancellation depth — upper half of the published 35–55 dB window. Detection-range reduction 55–75 % when stacked with suppressor + double-plug protection.

> **Genre note.** TRP designator adopted for tonal coherence. Simulation-based, pre-physical-test — no anechoic-chamber validation on proposed hardware.

---

## What this folder is

TACS is a **complete platform subfolder**: operator specification, two academic papers, an energy-conservation analysis, and Tier-2 cancellation modelling in [`../weapons_simulation.py`](../weapons_simulation.py) §18.

**Reading order:**

1. **This README** — navigation and headline numbers.
2. [`TACS_Complete_Specification.md`](TACS_Complete_Specification.md) — full operator spec (TRP-2026-303).
3. [`Paper11_TACS_System.md`](Paper11_TACS_System.md) — system architecture / FxLMS algorithm.
4. [`Paper12_TACS_Energy_Physics.md`](Paper12_TACS_Energy_Physics.md) — wave-superposition / anti-node physics.
5. [`TACS_Energy_Conservation_Analysis.md`](TACS_Energy_Conservation_Analysis.md) — anti-node hazard doctrine.
6. [`SIM_README.md`](SIM_README.md) — §18 simulator coverage.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`TACS_Complete_Specification.md`](TACS_Complete_Specification.md) | Operator specification | Three variants, doctrine, hardware, performance tables. **Start here.** |
| [`Paper11_TACS_System.md`](Paper11_TACS_System.md) | Research paper | FxLMS adaptive control, array architecture. |
| [`Paper12_TACS_Energy_Physics.md`](Paper12_TACS_Energy_Physics.md) | Research paper | Nelson–Elliott bounds, anti-node management. |
| [`TACS_Energy_Conservation_Analysis.md`](TACS_Energy_Conservation_Analysis.md) | Analysis memo | Energy redistribution and personnel positioning doctrine. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Portfolio §18 coverage. |

---

## 🎯 Headline numbers (simulator §18)

| Variant | A-weighted avg | 125 Hz | 500 Hz | 4 kHz |
|---|---|---|---|---|
| Personal (16-element) | **36.3 dB** | 40.0 dB | 40.0 dB | 25.1 dB |
| Mobile (64-element) | **36.0 dB** | 43.6 dB | 41.4 dB | 23.4 dB |
| Fixed (64-element) | **32.4 dB** | 43.6 dB | 37.4 dB | 19.4 dB |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §18.

---

## 🚧 Honest framing

- **Anti-nodes are physics, not malfunction** — asymmetric 30–50 % emitter power keeps anti-node SPL below 115 dB for a 110 dB source but cannot eliminate the hazard.
- **High-frequency degradation** — Personal drops to 25.1 dB at 4 kHz; jet/supersonic crack bands are outside the design envelope.
- **No field measurement** — all depths are Nelson–Elliott simulator outputs.

---

## 🔗 Related work in this repo

- [`../Hearing Protection/`](../Hearing%20Protection/) — passive double-plug stack (often combined with TACS)
- [`../HPR-X Rocketry/`](../HPR-X%20Rocketry/) — launch-site signature adjacency
- [`../README.md`](../README.md) — portfolio index

---

[← Back to Weapons-Defence README](../README.md)
