# MP-4.6M Guardian — suppressed service pistol

> **A simulation-validated 4.6 × 30 mm Enhanced single-action semi-automatic service pistol with integral suppressor, sharing cartridge and bolt-face geometry with the MP-4.6M Defender PDW.** Headline design: **501 m/s** muzzle velocity, **326 J** muzzle energy, **180 MPa** peak chamber pressure, **3.8 mm** RHA at the muzzle, **20-round** magazine, **0.92 kg** empty mass, **40 dB** modelled suppressor attenuation, **559 N** peak shoulder force.

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **Numbers trace to the portfolio-wide [`../weapons_simulation.py`](../weapons_simulation.py) — cartridge key `4.6x30mm`, tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md).**

---

## What this folder is

The MP-4.6M Guardian is a **complete platform subfolder**: operator specification, academic research paper, and simulation traceability via the shared portfolio simulator. Unlike the BSG-10 Goliath (which carries its own `bsg10_sim` package), the Guardian's ballistic, penetration, suppressor, hearing-protection, barrel-life, and recoil numbers are produced by the common Tier-1/Tier-2 toolchain in [`../weapons_simulation.py`](../weapons_simulation.py).

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`MP-4.6M_Guardian_Pistol_Specification.md`](MP-4.6M_Guardian_Pistol_Specification.md) — product and engineering spec (TRP-2026-001).
3. [`MP-4.6M_Guardian_Pistol_Research_Paper.md`](MP-4.6M_Guardian_Pistol_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — how to re-run and locate this platform's numbers in the portfolio simulator.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`MP-4.6M_Guardian_Pistol_Specification.md`](MP-4.6M_Guardian_Pistol_Specification.md) | Operator / product specification | Full TRP-style engineering doc — cartridge, action, barrel, suppressor, materials, lifecycle. **Start here for "what is the weapon."** |
| [`MP-4.6M_Guardian_Pistol_Research_Paper.md`](MP-4.6M_Guardian_Pistol_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, simulation framework, results, limitations — same numbers as the spec in journal structure. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Cartridge key, relevant `weapons_sim_results.md` tables, re-run command. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | Tier-1/Tier-2 physics engine for all small-arms entries except BSG-10 Goliath. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative tabulated numbers — cite this file in every spec edit. |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §§1–2, 3, 5, 10, 11. Re-run the simulator after cartridge or weapon-parameter edits.

| Metric | Value |
|---|---|
| Cartridge | **4.6 × 30 mm Enhanced** (`4.6x30mm`) |
| Muzzle velocity | **501 m/s** (1,644 fps) |
| Muzzle energy | **326 J** |
| Peak chamber pressure | **180 MPa** (26,107 psi) |
| RHA penetration @ muzzle | **3.8 mm** (290 BHN, 0°) |
| Empty mass | **0.92 kg** |
| Magazine capacity | **20 rounds** |
| Free recoil energy | **1.5 J** (1.1 ft·lb) |
| Peak shoulder force | **559 N** (126 lbf) |
| Integral suppressor attenuation | **40.0 dB** (modelled upper bound) |
| Barrel life (model) | **302,501 rounds** |
| Max effective range (Hatcher, KE > 80 J) | **878 m** |

---

## 🚀 Quick start (simulator)

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for which tables in `weapons_sim_results.md` correspond to this platform.

---

## 🚧 Honest framing

- **Not a fielded weapon.** Concept and simulation only; no instrumented prototype data.
- **Portfolio simulator, not standalone.** This folder does not contain a local Python package — all numbers come from the parent script.
- **40 dB suppressor figure is a modelled upper bound.** Real K-baffle suppressors typically achieve 25–35 dB.
- **Cartridge commonality with PDW.** The loaded round is identical to the Defender PDW; only barrel length differs (180 mm pistol vs 266.7 mm PDW — see [`../MP-4.6M Defender PDW/`](../MP-4.6M%20Defender%20PDW/)).

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — Weapons-Defence portfolio index
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — Shared 4.6 × 30 mm cartridge, bolt face, trigger pack
- [`../MP-4.6M Defender PDW/`](../MP-4.6M%20Defender%20PDW/) — Same cartridge, longer barrel, select-fire PDW variant
- [`../BSG10 Goliath/`](../BSG10%20Goliath/) — Adjacent small-arms entry with standalone `bsg10_sim` (not portfolio simulator)

---

[← Back to Weapons-Defence README](../README.md)
