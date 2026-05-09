# New Classes of Electrical Components — discrete-continuous hybrid devices

> **A complete catalogue + simulation programme.** Three tiers of hybrid passive devices that combine discrete (digital / quantised) and continuous (analog) behaviour in a single component — quantum tunnel resistors, memcapacitors / meminductors, sample-hold passives, spin-resistors, magnetoelectric inductors, programmable gyrators, and more — together with a five-phase Python simulation programme that verifies the device equations end-to-end.

---

## ⚡ What this folder is

Two interlocking tracks: a device catalogue (theory, math/physics, fabrication, components list) and a multi-phase simulation effort that exercises and validates the device models. Plus an embedded `Cypha.py` classifier used as glue / analysis.

---

## 📄 Theory and design documents

| Document | Role |
|---|---|
| [`discrete_continuous_hybrid_components.md`](discrete_continuous_hybrid_components.md) | Theory and taxonomy — what makes a component "hybrid" |
| [`complete_hybrid_components_catalog.md`](complete_hybrid_components_catalog.md) | The full catalogue, organised in three tiers (Tier 1: standard-equipment-achievable today; Tier 2: specialised-equipment / lab-proven; Tier 3 / further: programmable gyrators, multi-level ladder capacitors, delta-sigma capacitors, etc.) |
| [`hybrid_components_mathematics_physics.md`](hybrid_components_mathematics_physics.md) | Underlying math / physics derivations |
| [`hybrid_component_fabrication_guide.md`](hybrid_component_fabrication_guide.md) | Fabrication and manufacturing pathways for each device class |
| [`hybrid_research_papers.md`](hybrid_research_papers.md) | Bundle of research-paper-style writeups |

## 🧪 Five-phase simulation programme

| Phase | Document |
|---|---|
| Setup | [`hybrid_simulation_master.md`](hybrid_simulation_master.md), [`hybrid_component_simulation.md`](hybrid_component_simulation.md) |
| Phase 1 | [`hybrid_simulation_phase1.md`](hybrid_simulation_phase1.md) |
| Phase 2 | [`hybrid_simulation_phase2.md`](hybrid_simulation_phase2.md) |
| Phase 3 | [`hybrid_simulation_phase3.md`](hybrid_simulation_phase3.md) |
| Phase 4 | [`hybrid_simulation_phase4.md`](hybrid_simulation_phase4.md) + [`Phase4_Verification_Report.md`](Phase4_Verification_Report.md) |
| Phase 5 | [`hybrid_simulation_phase5.md`](hybrid_simulation_phase5.md) |
| Full verification | [`HybridSim_FullVerification_AllPhases.md`](HybridSim_FullVerification_AllPhases.md) |

## 🐍 Code

| File | Role |
|---|---|
| [`Cypha.py`](Cypha.py) | A Cypha-style classifier (see [`../Cypha/`](../Cypha/) for the canonical implementation). Used here for analysis / classification of simulated device behaviours rather than as the canonical Cypha codebase. |

> Earlier README copy listed device classes ("Hybrid Diodes", "Phase-Shifting Elements", "Multi-State Devices", "Hybrid Amplifiers") that are *paraphrases* rather than items in the canonical catalogue. The actual Tier 1 list begins with **Quantum Tunnel Resistor**, **Magnetic Domain Inductor**, **Sample-Hold Capacitor/Resistor**, **Memcapacitor**, **Meminductor**, **Brownian Resistor**, **Piezo-Quantum Capacitor**, **Dual-Mode Memristor** — see [`complete_hybrid_components_catalog.md`](complete_hybrid_components_catalog.md) for the authoritative table.

---

## 🔗 Related work in this repo

- [`../Cypha/`](../Cypha/) — canonical Cypha (HRNA) codebase referenced by the local `Cypha.py`
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — NMP / GRIA theoretical backbone
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic structure for discrete-side device behaviour
- [`../Physics/`](../Physics/) — non-local field theory framework
- [`../Diffusion Welding/`](../Diffusion%20Welding/) — joining of metallic structures relevant to fabrication
- [`../Rockwell 50 to 70 Carbide/`](../Rockwell%2050%20to%2070%20Carbide/) — process science for machining tooling

---

[← Back to main README](../README.md)
