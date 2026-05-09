# Rockwell 50 to 70 Carbide — HX-70 GradePlex™ Sintered Carbide for Hard Machining

> **🔩 Overview**: A ground-up sintered-carbide tooling system engineered to **machine hardened steels from HRC 40 to HRC 70** — closing the production-tooling gap currently bridged only by CBN inserts, at 60–70% lower cost.

---

## 🔩 Overview

This folder documents **HX-70 GradePlex™**, a complete sintered-carbide tool system targeting the full hardness spectrum of defence-grade hardened steels. The "50 to 70" in the folder title refers to the **Rockwell C hardness of the workpiece** (the steel being cut), not the carbide grain size — the scale is named after Stanley P. Rockwell.

> **Naming corrections from earlier README.** A previous README revision claimed the folder was about "tungsten-carbide grain sizes in the 50–70 micron range" with hardness "20–22 HRA". Both were wrong by orders of magnitude:
>
> - Actual surface-zone WC grain size in the design: **0.25–0.35 µm** (nano-grain), not 50–70 µm.
> - Actual surface-zone hardness target: **2050–2100 HV30** (Vickers), equivalent to ~92 HRA — not 20–22 HRA, which would be softer than rubber.

---

## 🎯 The Problem HX-70 Solves

Industry practice today bifurcates the machining of hardened steels:

| Workpiece hardness | Conventional tool | Limitation |
|---|---|---|
| ≤ HRC 55 | Premium coated carbide | Operates within rated envelope |
| HRC 55 – 70 | CBN inserts / ceramics | Insert-only — cannot be made as small-diameter end mills; 10–15× cost premium |

Defence components (receivers, breech assemblies, locking grooves, pin bores, pocket profiles) require small-diameter end milling at HRC 60+. **No carbide tool in current production survives this regime with acceptable life.** HX-70 was designed from first principles to close exactly this gap.

---

## 📄 Research Documents

| Document | Description |
|---|---|
| [`HX70_Research_Paper.md`](HX70_Research_Paper.md) | Primary technical paper — full engineering rationale, materials science, process architecture, and performance projections from HRC 40 to HRC 70 |
| [`HX70_Sintered_Carbide_Design_Spec.md`](HX70_Sintered_Carbide_Design_Spec.md) | Design specification — GradePlex™ substrate, coating system, edge geometry, parameter framework |
| [`ForgeMachine_Research_Paper.md`](ForgeMachine_Research_Paper.md) | The forge-to-machine production architecture HX-70 enables — 40–45% cost reduction, 65–70% lead-time reduction, ADF supply-chain agility |
| [`Forge_to_Machine_Defence_Analysis.md`](Forge_to_Machine_Defence_Analysis.md) | Defence-specific analysis of forge-to-machine routes |

---

## 🏗️ The Three-Innovation Architecture

HX-70 is a coordinated system, not a single invention. Three innovations operate simultaneously:

### 1. Functionally graded substrate (GradePlex™)

Three compositional zones with different WC / Co / cubic-carbide ratios:

| Zone | Depth | WC | Co | Cubic carbide | Role |
|---|---|---|---|---|---|
| **A — Surface** | 0–30 µm | 92.5% | 5.5% | 2.0% (TaC/NbC) | Maximum hardness, wear resistance — **2050–2100 HV30** |
| **B — Subsurface** | 30–300 µm | 88.0% | 9.0% | 3.0% (TaC/NbC/Cr₃C₂) | Crack arrest, thermal buffer |
| **C — Core** | 300 µm–bulk | 84.5% | 13.0% | 2.5% (TaC/Cr₃C₂) | Toughness, vibration damping — **1500–1600 HV30**, K_IC ≈ 13–14 MPa·m½ |

Surface-zone WC grain size: **D₅₀ = 0.25–0.35 µm** (nano-grain).

The grain-growth inhibitor system uses **TaC** (Zener pinning at WC grain-boundary triple junctions), **NbC** (secondary inhibition + Co-phase strengthening), and **Cr₃C₂** (suppression of WO₃ oxidative volatilisation via preferential Cr₂O₃ scale).

### 2. Five-layer PVD/PECVD nanocomposite coating stack

The "Triboshield" coating architecture uses **AlCrN / AlTiSiN** multilayers — nano-crystalline (Al,Ti,Si)N grains embedded in an amorphous Si₃N₄ matrix — combined with a DLC-Si top layer. Target stoichiometry (Al₀.₅₅Ti₀.₃₀Si₀.₁₅)N is calibrated to ~50 GPa peak hardness and oxidation resistance to 1000 °C, consistent with published AlCrN/AlTiSiN multilayer characterisation (Xiao et al. 2022).

### 3. Geometry / parameter framework

Edge geometry, helix, rake, trochoidal toolpath strategy, MQL and cryogenic cooling envelopes — all calibrated to the physics of hardened-steel chip formation. Above HRC 55 flood coolant is *avoided* (thermal-shock cracking); compressed air, MQL, or LN₂ delivery are used instead.

---

## 📊 Tool Life Projections

| Workpiece hardness | Improvement vs. premium AlTiN carbide | vs. CBN |
|---|---|---|
| HRC 55 | **+40 – 55%** | Carbide-form available; CBN limited to indexable inserts |
| HRC 60 | **+85 – 100%** | First-in-class carbide capability |
| HRC 65 – 70 | New regime — no current carbide competitor | Comparable life at ~30% of CBN cost |

Cost: **60–70% reduction relative to CBN** at HRC 65–70.

---

## 🏭 Forge-to-Machine Architecture

The companion paper ([`ForgeMachine_Research_Paper.md`](ForgeMachine_Research_Paper.md)) examines the production-economics consequence of having a carbide tool that survives at HRC 70. Conventional defence-component routing —

> forge → anneal → soft pre-machine → harden → finish machine → grind → inspect

— consolidates into a single forge-to-machine pipeline:

> near-net-shape forge → (deliver at service hardness) → finish machine in one setup

Modelled outcomes on a representative H13 breech component (HRC 52–56, 1.8 kg finished, 3.5 kg raw forging):

| Metric | Conventional | Forge-to-machine | Δ |
|---|---|---|---|
| Material waste | 1.7 kg/part | ~0.3 kg/part | −82% |
| Total processing cost | baseline | −40 to −45% | substantial |
| Lead time | baseline | −65 to −70% | substantial |
| Process stages | 4–6 | 1 | structural simplification |

The strategic case (eliminating furnace scheduling as the dominant supply-chain bottleneck) is developed explicitly with reference to ADF procurement and aerospace lead-time pressures.

---

## 🔗 Related Work

This work connects to:

- **Diffusion Welding** — joining of hardened components; complementary process science
- **Diamond Batterys** / **Quantum Diamond Wafer** — adjacent advanced materials work
- **Weapons** — defence components targeted by HX-70 (receivers, breeches, armour brackets)
- **Physics** — materials physics underpinning grain-boundary diffusion, Zener pinning, oxidation kinetics

---

## 📖 See Also

- [`EDITORIAL_ROADMAP.md`](../EDITORIAL_ROADMAP.md) — editorial standards and batch history
- [`EDITORIAL_STYLE.md`](../docs/EDITORIAL_STYLE.md) — house style guide
- [`Diffusion Welding/`](../Diffusion%20Welding/) — UCDW joining
- [`Diamond Batterys/`](../Diamond%20Batterys/) — diamond materials
- [`Weapons/`](../Weapons/) — defence components

---

## 🛡️ About This Project

HX-70 GradePlex™ is a **complete tool-system design**, not a coating tweak or substrate variant. The deliverable is a coherent sintered-carbide solution for the full HRC 40–70 hardness range, plus the production-architecture argument (forge-to-machine) for why having such a tool matters strategically. Source documents are technical specifications and engineering analyses; numbers cited in this README come directly from those documents.

[← Back to main README](../README.md)
