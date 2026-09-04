# OAM-VEST — non-lethal acoustic area denial

> **A vehicle-mounted non-lethal acoustic area denial system that incapacitates via vestibular disruption rather than auditory pain compliance.** Dual 1.2 m phased-array panels deliver OAM vortex beams and amplitude-modulated bone-conducted stimulation at **173.2 dB** combined source level — **410 m** disorientation range, **19.3 m** incapacitation range, **earplug-immune** against Modes B and C. Numbers trace to the standalone `oam_vest_sim` package in this folder — not to the portfolio-wide `weapons_simulation.py`.

> **Genre note.** Commercial-in-confidence / defence-application register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, fielded prototype, or government demonstration is implied. Formal Article 36 legal review is recommended before any acquisition discussion.

---

## What this folder is

OAM-VEST (**Orbital Angular Momentum Vestibular Disruption System**) is a **complete platform subfolder**: operator specification, academic research paper, and a dedicated six-module Python acoustic-physics simulation suite. Unlike LRAD-class auditory-pain systems (defeated by foam earplugs), OAM-VEST attacks balance and spatial orientation through vestibulo-ocular pathways that conventional hearing protection does not block.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`OAM-VEST_System_Specification.md`](OAM-VEST_System_Specification.md) — product and engineering spec (physics, hardware, safety, roadmap, commercial analysis).
3. [`OAM-VEST_Research_Paper.md`](OAM-VEST_Research_Paper.md) — formal design-and-validation narrative with simulation results.
4. [`OAM-VEST_Simulation_Package/`](OAM-VEST_Simulation_Package/) — re-run modules and regenerate the consolidated report.
5. **Verify claims** — see **🔬 Simulation verification** below.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`OAM-VEST_System_Specification.md`](OAM-VEST_System_Specification.md) | Operator / product specification | Executive summary, physics and signal design, hardware, safety and legal framework, development roadmap, costs and market analysis. **Start here for “what is the system.”** |
| [`OAM-VEST_Research_Paper.md`](OAM-VEST_Research_Paper.md) | Academic research paper | Abstract, physical background, array architecture, signal modes, pulsed operation, safety and lethality analysis, simulation results, legal considerations. |
| [`OAM-VEST_Simulation_Package/OAM-VEST_Simulation_README.md`](OAM-VEST_Simulation_Package/OAM-VEST_Simulation_README.md) | Simulation documentation | Package-level overview, module map, CLI usage, verified headline table. |
| [`OAM-VEST_Simulation_Package/oam_vest_sim/README.md`](OAM-VEST_Simulation_Package/oam_vest_sim/README.md) | Simulation documentation (in-package copy) | Duplicate of `OAM-VEST_Simulation_README.md` for developers who open the Python package directly. |
| [`OAM-VEST_Simulation_Package/run_simulations.py`](OAM-VEST_Simulation_Package/run_simulations.py) | CLI launcher | Thin wrapper into `oam_vest_sim.report`. |
| [`OAM-VEST_Simulation_Package/oam_vest_sim/report.py`](OAM-VEST_Simulation_Package/oam_vest_sim/report.py) | CLI entry | Runs all modules; writes `OAM-VEST_Simulation_Report.md`. |

### Simulation modules (`OAM-VEST_Simulation_Package/oam_vest_sim/`)

| Module | File | Role |
|---|---|---|
| **Physics** | [`OAM-VEST_Simulation_Package/oam_vest_sim/physics.py`](OAM-VEST_Simulation_Package/oam_vest_sim/physics.py) | Propagation, SPL conversion, biological thresholds, earplug attenuation model |
| **Array** | [`OAM-VEST_Simulation_Package/oam_vest_sim/acoustic_array.py`](OAM-VEST_Simulation_Package/oam_vest_sim/acoustic_array.py) | Dual-panel phased array, OAM phase winding, beam steering, multi-target superposition |
| **Pulse** | [`OAM-VEST_Simulation_Package/oam_vest_sim/pulse.py`](OAM-VEST_Simulation_Package/oam_vest_sim/pulse.py) | Pulsed regime, cochlear NIOSH dose, vestibular cupula dynamics, LiDAR interleave, dwell timer |
| **Wavefield** | [`OAM-VEST_Simulation_Package/oam_vest_sim/wavefield.py`](OAM-VEST_Simulation_Package/oam_vest_sim/wavefield.py) | 2D FDTD acoustic pressure solver for beam-pattern verification |
| **Safety** | [`OAM-VEST_Simulation_Package/oam_vest_sim/safety.py`](OAM-VEST_Simulation_Package/oam_vest_sim/safety.py) | Engagement envelope, lethality margins, interlock scenario simulation |
| **Report** | [`OAM-VEST_Simulation_Package/oam_vest_sim/report.py`](OAM-VEST_Simulation_Package/oam_vest_sim/report.py) | Consolidated markdown report from all modules |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`OAM-VEST_Simulation_Package/OAM-VEST_Simulation_README.md`](OAM-VEST_Simulation_Package/OAM-VEST_Simulation_README.md) / default design run. Re-run to refresh after parameter edits.

| Metric | Value |
|---|---|
| Combined source SPL | **173.2 dB** @ 1 m (dual 512-element panels) |
| Disorientation range | **410 m** (48 778 m² cone footprint) |
| Pain / deterrence range | **117 m** |
| Incapacitation range | **19.3 m** |
| OAM nystagmus margin | **6.3×** threshold (l = 1, f_mod = 2 Hz) |
| Average power (pulsed, 20% duty) | **10.2 kW** (51.2 kW peak) |
| Earplug countermeasure (Modes B/C) | **Ineffective** |
| Lung rupture margin @ 100 m | **+53 dB** |
| Minimum safe engagement range | **15 m** (LiDAR hardware interlock) |
| Simultaneous independent beams | **Up to 4** |

---

## 🔬 Simulation verification

OAM-VEST does **not** use the portfolio [`../weapons_simulation.py`](../weapons_simulation.py). All headline numbers trace to the standalone **`oam_vest_sim`** package in this folder.

```bash
cd OAM-VEST_Simulation_Package
python run_simulations.py
```

| Artifact | Role |
|---|---|
| [`OAM-VEST_Simulation_Package/run_simulations.py`](OAM-VEST_Simulation_Package/run_simulations.py) | Full six-module verification run |
| [`OAM-VEST_Simulation_Package/OAM-VEST_Simulation_README.md`](OAM-VEST_Simulation_Package/OAM-VEST_Simulation_README.md) | Module map + validated headline table |
| [`OAM-VEST_Simulation_Package/oam_vest_sim/`](OAM-VEST_Simulation_Package/oam_vest_sim/) | Physics, array, pulse, safety modules |

Output: `OAM-VEST_Simulation_Report.md` with PASS/FAIL verification table vs spec claims.

---

## 🚀 Quick start (simulator)

```bash
cd OAM-VEST_Simulation_Package
pip install -r requirements.txt
python run_simulations.py
```

Output: `OAM-VEST_Simulation_Report.md` (or path passed via `--output`).

See [`OAM-VEST_Simulation_Package/OAM-VEST_Simulation_README.md`](OAM-VEST_Simulation_Package/OAM-VEST_Simulation_README.md) for per-module API reference and extension notes.

---

## 🚧 Honest framing

- **Not a fielded system.** Concept and simulation only; no instrumented prototype or human-effects trial data.
- **Separate simulator.** Do not expect numbers in [`../weapons_sim_results.md`](../weapons_sim_results.md).
- **Non-lethal does not mean harmless.** Lethality crossover ranges exist; LiDAR interlock and dwell timer are modelled as mandatory safety layers.
- **Legal review required.** Article 36 (Geneva Convention AP I) review recommended before any government demonstration.

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — Weapons-Defence portfolio index
- [`../Military Noise Cancellation/`](../Military%20Noise%20Cancellation/) — **TACS** active noise cancellation (defensive hearing protection; opposite mission set to OAM-VEST)
- [`../Hearing Protection/Hearing_Protection_Specification.md`](../Hearing%20Protection/Hearing_Protection_Specification.md) — Passive and active hearing-protection stack (LRAD countermeasure context)
- [`../Hearing Protection/Hearing_Protection_Research_Paper.md`](../Hearing%20Protection/Hearing_Protection_Research_Paper.md) — Paired research paper for hearing protection
- [`../../Threat Asessments/`](../../Threat%20Asessments/) — Hypothetical threat-intelligence briefs (intelligence register)

---

[← Back to Weapons-Defence README](../README.md)
