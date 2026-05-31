# BSG-10 "Goliath" — 10-gauge bullpup combat shotgun

> **A simulation-validated 10-gauge semi-automatic bullpup combat shotgun engineered for maximum firepower at shoulder recoil below a field-load 12-gauge.** Headline design: 45-round helical drum, seven-layer recoil stack including CBS-10 compensating butt stock, gas-operated balanced action, 415 m/s muzzle velocity at 73.5 MPa peak chamber pressure (3% below SAAMI ceiling), ~490 N peak shoulder force.

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **Numbers trace to the standalone `bsg10_sim` package in this folder — not to the portfolio-wide `weapons_simulation.py`.**

---

## What this folder is

The BSG-10 Goliath is a **complete platform subfolder**: operator specification, academic research paper, and a dedicated six-module Python simulation suite. Unlike most small-arms entries in the parent portfolio (which share [`../weapons_simulation.py`](../weapons_simulation.py)), Goliath carries its own physics toolchain because shotgun internal ballistics, balanced-action ODEs, helical-drum feed mechanics, and multi-layer recoil integration are outside the Tier-1/Tier-2 cartridge tables in the common simulator.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`BSG10_Goliath_Full_Specification.md`](BSG10_Goliath_Full_Specification.md) — product and engineering spec (Parts I–V, simulation results embedded).
3. [`BSG10_Research_Paper.md`](BSG10_Research_Paper.md) — formal design-and-validation narrative.
4. [`bsg10_sim_package/`](bsg10_sim_package/) — re-run modules and regenerate consolidated reports.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`BSG10_Goliath_Full_Specification.md`](BSG10_Goliath_Full_Specification.md) | Operator / product specification | Full TRP-style engineering doc — cartridge, action, recoil, magazine, materials, simulation Part II, lifecycle, manufacturing, commercial. **Start here for “what is the weapon.”** |
| [`BSG10_Research_Paper.md`](BSG10_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, simulation framework, results, limitations — same numbers as the spec in journal structure. |
| [`bsg10_sim_package/Software readme.md`](bsg10_sim_package/Software%20readme.md) | Simulation documentation | Package-level overview, module map, CLI usage, validated headline table. |
| [`bsg10_sim_package/bsg10_sim/README.md`](bsg10_sim_package/bsg10_sim/README.md) | Simulation documentation (in-package copy) | Duplicate of `Software readme.md` for developers who open the Python package directly. |
| [`bsg10_sim_package/run_all.py`](bsg10_sim_package/run_all.py) | CLI launcher | Thin wrapper into `bsg10_sim.run_all`. |
| [`bsg10_sim_package/bsg10_sim/run_all.py`](bsg10_sim_package/bsg10_sim/run_all.py) | CLI entry | Runs one or all modules; supports `default` / `heavy` / `light` variants via [`config.py`](bsg10_sim_package/bsg10_sim/config.py). |

### Simulation modules (`bsg10_sim_package/bsg10_sim/`)

| Module | File | Role |
|---|---|---|
| **A — Internal ballistics** | [`ballistics/internal.py`](bsg10_sim_package/bsg10_sim/ballistics/internal.py) | Chamber pressure, muzzle velocity, gas-port timing |
| **B — Balanced action** | [`dynamics/balanced_action.py`](bsg10_sim_package/bsg10_sim/dynamics/balanced_action.py) | Bolt carrier + counter-mass ODE |
| **C — Recoil chain** | [`dynamics/recoil_chain.py`](bsg10_sim_package/bsg10_sim/dynamics/recoil_chain.py) | Shoulder force through compensator → CBS-10 stack |
| **D — Geometry** | [`mechanical/dimensions.py`](bsg10_sim_package/bsg10_sim/mechanical/dimensions.py) | Bullpup envelope and clearance checks |
| **E — Magazine** | [`mechanical/magazine.py`](bsg10_sim_package/bsg10_sim/mechanical/magazine.py) | 45-round helical belt drum capacity and feed force |
| **F — Parts life** | [`lifecycle/parts_life.py`](bsg10_sim_package/bsg10_sim/lifecycle/parts_life.py) | Barrel, lugs, CBS-10, gas-system fatigue and wear |
| **Report** | [`reports/generate.py`](bsg10_sim_package/bsg10_sim/reports/generate.py) | Consolidated text report from all modules |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`bsg10_sim_package/bsg10_sim/README.md`](bsg10_sim_package/bsg10_sim/README.md) / default `BSG10Config` run. Re-run to refresh after parameter edits.

| Metric | Value |
|---|---|
| Peak chamber pressure | **73.5 MPa** (10,665 PSI) — ~3% below SAAMI limit |
| Muzzle velocity | **415 m/s** (1,362 fps) |
| Magazine capacity | **45 rounds** (200 mm Tommy-style helical drum) |
| Overall length | **1,012 mm** (39.8 in) with **510 mm** barrel |
| Loaded weight | **~8.9 kg** (19.6 lb) |
| Peak shoulder force | **~490 N** (reference: ~1,800 N for 12-gauge field load) |
| Bolt lug fatigue safety factor | **4.3×** (infinite fatigue life in model) |
| Barrel life | **~19,000 rounds** (Melonite-coated, modelled erosion) |

---

## 🚀 Quick start (simulator)

```bash
cd bsg10_sim_package
pip install -r bsg10_sim/requirements.txt
python run_all.py
```

See [`bsg10_sim_package/Software readme.md`](bsg10_sim_package/Software%20readme.md) for per-module flags and output paths under `bsg10_sim/outputs/`.

---

## 🚧 Honest framing

- **Not a fielded weapon.** Concept and simulation only; no instrumented prototype data.
- **Separate simulator.** Do not expect numbers in [`../weapons_sim_results.md`](../weapons_sim_results.md) unless Goliath is later integrated into the portfolio script.
- **10-gauge regulatory reality.** Civilian and export constraints for 10-gauge combat shotguns are not modelled; the spec assumes a defence R&D context.

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — Weapons-Defence portfolio index
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — Shared small-arms parts matrix (Goliath is not yet in the common-cartridge table)
- [`../MP-4.6M Defender PDW.md`](../MP-4.6M%20Defender%20PDW.md) — Adjacent small-arms portfolio entry
- [`../../Rockwell 50 to 70 Carbide/`](../../Rockwell%2050%20to%2070%20Carbide/) — Tooling and materials supply-chain context

---

[← Back to Weapons-Defence README](../README.md)
