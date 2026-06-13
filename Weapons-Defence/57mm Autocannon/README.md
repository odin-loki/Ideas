# 57 mm Advanced Mechanical Autocannon System (AMAS) Mark IV

> **A simulation-validated externally-powered dual-feed 57 mm autocannon firing 57 × 347 mm SR APFSDS-T at 948 m/s for 1.08 MJ muzzle energy, 139.7 mm RHA at the muzzle, and 257 MPa peak chamber pressure.** Headline mount: 350 kg empty, 120-round dual-feed, 220 rpm cyclic / 80 rpm thermal ceiling, 27.6 kJ free recoil absorbed through hydraulic dashpots (139 832 N peak mount force).

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **Numbers trace to the portfolio-wide [`../weapons_simulation.py`](../weapons_simulation.py) — cartridge key `57x347mm`, weapon key `57 mm Autocannon`.**

---

## What this folder is

The 57 mm AMAS is a **complete platform subfolder**: operator specification, academic research paper, and **Tier-C portfolio simulation** via the shared [`../weapons_simulation.py`](../weapons_simulation.py) suite. Unlike BSG-10 Goliath (which carries its own `bsg10_sim` package), this weapon is validated through the common cartridge and weapon tables in the parent simulator.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`57mm_Autocannon_Specification.md`](57mm_Autocannon_Specification.md) — product and engineering spec (TRP-2026-103).
3. [`57mm_Autocannon_Research_Paper.md`](57mm_Autocannon_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — how to re-run and which `weapons_sim_results.md` sections apply.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`57mm_Autocannon_Specification.md`](57mm_Autocannon_Specification.md) | Operator / product specification | Full TRP-style engineering doc — cartridge, mount, recoil, feed, materials, Tier-2 simulation imports. **Start here for “what is the weapon.”** |
| [`57mm_Autocannon_Research_Paper.md`](57mm_Autocannon_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, simulation framework, results, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Portfolio sim keys, result-table map, CLI usage. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Simulator source | Cartridge `57x347mm`, weapon `57 mm Autocannon`, Tier-1 + Tier-2 models. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative output | Human-readable tables — cite this file in every spec claim. |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md). Re-run the simulator to refresh after parameter edits.

| Metric | Value |
|---|---|
| Cartridge | **57 × 347 mm SR** (`57x347mm`) |
| Muzzle velocity | **948 m/s** (3 109 fps) |
| Muzzle energy | **1.08 MJ** (1 077 666 J) |
| Peak chamber pressure | **257 MPa** (37 308 psi) |
| RHA penetration (0°) | **139.7 / 125.4 / 113.0 mm** @ 0 / 500 / 1 000 m |
| RHA @ NATO 60° | **86.0 mm** @ muzzle |
| Magazine capacity | **120 rounds** (dual-feed) |
| Empty mount mass | **350 kg** |
| Free recoil | **27 621 J** (20 372 ft·lb) |
| Peak mount force | **139 832 N** (31 437 lbf) |
| Barrel life | **1 166 rounds** |
| Sustained rpm (thermal) | **80 rpm** |
| HE-Frag lethal area | **117 m²** (r_eff 6.1 m) |
| HEDP shaped-charge | **37 mm RHA** |

---

## 🚀 Quick start (simulator)

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for cartridge key, weapon key, and relevant result sections.

---

## 🚧 Honest framing

- **Not a fielded weapon.** Concept and simulation only; no instrumented prototype or live-armour test data.
- **Portfolio simulator.** All numbers live in [`../weapons_sim_results.md`](../weapons_sim_results.md) §1–§15.
- **Hydrodynamic floor.** RHA penetration collapses beyond ~1 km as striking velocity falls below ~800 m/s.
- **57 mm bore family.** Shares bore tooling with [`../57mm Underbarrel Grenade/`](../57mm%20Underbarrel%20Grenade/) and [`../57mm Mortar RPG/`](../57mm%20Mortar%20RPG/) per [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) §3.

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — Weapons-Defence portfolio index
- [`../57mm Underbarrel Grenade/`](../57mm%20Underbarrel%20Grenade/) — low-velocity 57 mm HE-FRAG under-barrel launcher
- [`../57mm Mortar RPG/`](../57mm%20Mortar%20RPG/) — dual-mode mortar / RPG tube
- [`../140mm Tank KE Round/`](../140mm%20Tank%20KE%20Round/) — main-armament long-rod KE round
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — shared 57 mm bore and Stellite-21 liner matrix

---

[← Back to Weapons-Defence README](../README.md)
