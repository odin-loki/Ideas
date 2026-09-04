# New Classes of Electrical Components

> **A four-tier catalogue of discrete-continuous hybrid passive devices — from quantum-tunnelling diodes (Tier 1, achievable today) through memtransistors and graphene-stacked composites (Tier 2/3) to fully-conceptual Shannon-limit / topological-protection / phononic-crystal devices (Tier 4) — paired with a five-phase Python simulation programme that claims a full Modified Nodal Analysis + Newton–Raphson + TR-BDF2 solver pipeline, GPU-batched solves at billions of fused operations per second, adjoint-method inverse design at `526 ×` finite-difference speedup, and SPICE / Verilog-AMS / SystemC-AMS export with `< 2.1 %` accuracy claim.** The catalogue covers `≥ 21` numbered device concepts with concrete process parameters (ALD Al₂O₃ cycle counts, PECVD SiN, tunnel area `50 µm²`, shot-noise spectral density `S_I = 2eI`); the simulator side claims `2.34 × 10⁹` fused solves/s on RTX 3090 and `4.37 × 10⁹` on A100 at `N = 262 144`. Documentation-level claims throughout — these are extensive design specifications, not a foundry run-sheet plus measured results.

---

## What this folder is

The standard discrete-passive component catalogue (R, L, C, plus diode and transistor variants) has been stable since the 1950s. Modern materials science has added a steady trickle of new candidates — memristors (Williams 2008), spintronic devices, MEMS resonators, quantum-tunnelling diodes — but they remain niche, with no unified taxonomy, no standardised simulation flow, and no direct path from "interesting physics paper" to "device usable in a circuit simulator." This folder is one author's attempt to close that gap by simultaneously (a) cataloguing the device space across four tiers from "fab-ready today" to "purely conceptual," (b) writing the simulation infrastructure that would be needed to *use* such a catalogue (a 5-phase MNA + Newton–Raphson + adaptive-stepping solver with GPU batching and adjoint-method inverse design), and (c) targeting export formats that connect to the legacy SPICE / Verilog-AMS / SystemC-AMS toolchains so the new devices don't live in isolation.

The folder also contains `Cypha.py` — a large `Omega` differential-information-field encoder/engine that lives in this directory but is *not* the hybrid-passive simulator. Treat it as adjacent work in the same neighbourhood.

---

## 📑 Source documents

### Catalogue + fabrication

| File | Role |
|---|---|
| [`complete_hybrid_components_catalog.md`](complete_hybrid_components_catalog.md) | Complete device catalogue. **`≥ 21` numbered concepts** across Tiers 1 – 4. |
| [`hybrid_component_fabrication_guide.md`](hybrid_component_fabrication_guide.md) | Fabrication processes. ALD Al₂O₃ cycle counts, PECVD SiN, tunnel area `50 µm²`, shot-noise `S_I = 2eI`. |
| [`hybrid_components_mathematics_physics.md`](hybrid_components_mathematics_physics.md) | Physics + mathematics. |
| [`hybrid_research_papers.md`](hybrid_research_papers.md) | Literature index. |
| [`discrete_continuous_hybrid_components.md`](discrete_continuous_hybrid_components.md) | Discrete-continuous hybrid framing. |

### Simulation programme (5 phases)

| File | Role |
|---|---|
| [`hybrid_component_simulation.md`](hybrid_component_simulation.md) | Simulation overview. |
| [`hybrid_simulation_master.md`](hybrid_simulation_master.md) | Master document. **`32` component models**, **MNA + Newton–Raphson + TR-BDF2** solver stack, GPU themes (CUDA, Radau IIA stiffness `10` vs RK4 `300 000` steps anecdote), adjoint-method differentiability (`~3.8 ×` one forward pass; **`526 ×` vs finite-difference at `N = 100`**). |
| [`hybrid_simulation_phase1.md`](hybrid_simulation_phase1.md) … [`hybrid_simulation_phase5.md`](hybrid_simulation_phase5.md) | Five phase documents. |
| [`HybridSim_FullVerification_AllPhases.md`](HybridSim_FullVerification_AllPhases.md) | Verification across all five phases. |
| [`Phase4_Verification_Report.md`](Phase4_Verification_Report.md) | Phase 4 verification report. |

### Adjacent

| File | Role |
|---|---|
| [`Cypha.py`](Cypha.py) | **Separate** Omega differential-information-field encoder / engine. Defines `Omega(x)` feature stack: moments `M(x), M(D(x)), M(D²(x))`, spectral bands `R(x, K)` with `N_BANDS = 16`, autocorrelation `N_LAGS = 8`. Discriminator correlation `r = 0.9985`. Default `output_dim = 512`. **Not the hybrid-passive simulator.** Adjacent work. |

---

## 🧠 The four-tier catalogue

| Tier | Examples | Status |
|---|---|---|
| **Tier 1** | Quantum-tunnelling diodes, ferroelectric capacitors | Fab-ready today |
| **Tier 2** | Memtransistors, graphene-stacked composites | Active research |
| **Tier 3** | Spintronic-photonic hybrids | Frontier |
| **Tier 4** | Shannon-limit toys, topological-protection devices, phononic crystals | **Conceptual only** |

---

## ⚙️ The simulation programme (5 phases)

| Phase | Role |
|---|---|
| **Phase 1** | Modified Nodal Analysis (MNA) base solver |
| **Phase 2** | Newton–Raphson nonlinear iteration |
| **Phase 3** | TR-BDF2 adaptive-step time integration with discrete-event handling |
| **Phase 4** | GPU batching (CUDA), Radau IIA stiff-equation handling |
| **Phase 5** | Adjoint-method differentiability + SPICE / Verilog-AMS / SystemC-AMS export |

### Reported headline metrics (master doc)

| Metric | Number | Context |
|---|---|---|
| **Fused solves/s** | **`2.34 × 10⁹`** | RTX 3090, 5-node, `N = 65 536` |
| **Fused solves/s** | **`4.37 × 10⁹`** | A100, `N = 262 144` |
| **Real-time stepping** | **`3 ns / timestep`** | (claim) |
| **Crossbar throughput** | **`10 000 GOPS/W`** vs A100's **`780 GOPS/W`** | claim |
| **Adjoint inverse design** | **`526 ×` faster** than finite-diff at `N = 100` | claim |
| **SPICE export accuracy** | **`< 2.1 %`** | claim |
| **Stiffness anecdote** | Radau IIA `10` steps vs RK4 `300 000` steps | claim |

---

## 🚧 Honest caveats

- **Catalogue mixes "achievable today" with "conceptual."** Marketing language risks overstating fabrication readiness across tiers — the tier label is the discipline.
- **Simulation claims should be treated as documentation-level assertions** unless you locate executable benchmark harnesses in the repo. The README authoring this folder did not turn up runnable GPU benchmark logs.
- **`Cypha.py` is not obviously the same scope** as "hybrid passive simulator" despite living in the same folder. It is an adjacent work — read it as such.
- **No measured silicon.** No fabrication results. The catalogue is *intent*, not yield.

---

## 🎯 What this displaces

| Standard | Limitation | What this offers |
|---|---|---|
| SPICE / commercial simulators | Locked component library | Open hybrid catalogue + extensible MNA pipeline |
| Memristor-only research | Narrow device class | Four-tier, `~21+` device-concept span |
| Hand-coded adjoint sensitivities | Slow, error-prone | `526 ×` automatic-differentiation speedup claim |
| Discrete + continuous separated | Two toolchains | Single discrete-event-aware adaptive integrator |

---

## 🔗 Related work in this repo

- [`../CPU/`](../CPU/) — sister hardware-design conversation
- [`../100W Wideband Noise Generator/`](../100W%20Wideband%20Noise%20Generator/) — sister single-file HDL design
- [`../Diffusion Welding/`](../Diffusion%20Welding/) — sister manufacturing-process work
- [`../Diamond Batterys/`](../Diamond%20Batterys/) — power architectures these components might support
- [`../Quantum Diamond Wafer/`](../Quantum%20Diamond%20Wafer/) — diamond-substrate fabrication science
- [`../Statistical Generation/`](../Statistical%20Generation/) — adjacent algorithmic frame for `Cypha.py`'s feature stack
- [`odin-loki/cypha`](https://github.com/odin-loki/cypha) — separate, larger HRNA inference stack

---

[← Back to main README](../README.md)
