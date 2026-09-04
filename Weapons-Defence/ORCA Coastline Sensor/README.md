# ORCA — Ocean Resonant Coastal Array

> **A simulation-validated passive distributed seabed electric-field surveillance array detecting submerged submarines and surface vessels via DC corrosion and propeller-shaft alternating fields.** Headline design: **28.49 km** submarine detection (Type-039 UEP), **45.22 km** large surface vessel; **54 nodes** at 57 km spacing for 3,000 km northern-coast persistent coverage; Tier 1 acquisition **$775k**, annual ops **~$299k/year** — **0.019%** of a single P-8A Poseidon acquisition cost for equivalent persistent coverage.

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or fielded prototype data is implied. **Detection-range and economics numbers trace to the standalone `orca_sim` package in this folder.**

---

## What this folder is

ORCA is a **complete platform subfolder**: operator specification, dedicated Python simulation suite (`orca_sim_package`), and cross-links to adjacent maritime surveillance assets in the portfolio. Unlike cartridge-level weapons in the parent [`../weapons_simulation.py`](../weapons_simulation.py), ORCA carries its own electrostatic detection physics because dipole field propagation, matched spatial filtering, DEMON cyclostationary classification, and array coverage geometry are outside the Tier-1/Tier-2 ballistics tables.

**Reading order for new readers:**

1. **This README** — surveillance and headline numbers.
2. [`papers/ORCA_System_Specification.md`](papers/ORCA_System_Specification.md) — full technical reference (Parts I–XII: physics, signal processing, node architecture, array design, economics, deployment, applications, roadmap).
3. [`papers/ORCA_Research_Paper.md`](papers/ORCA_Research_Paper.md) — formal design-and-validation narrative (Parts I–XII, convergence in Part X, 144 references).
4. [`SIM_README.md`](SIM_README.md) — how to re-run simulations and interpret detection-range vs coverage outputs.
5. Run [`platform_simulation.py`](platform_simulation.py) — consolidated detection and economics report.
6. [`orca_sim_package/Software readme.md`](orca_sim_package/Software%20readme.md) — package quick start.

---

## Source documents

| Document | Format | Role |
|---|---|---|
| [`papers/ORCA_System_Specification.md`](papers/ORCA_System_Specification.md) | Technical reference | Physical principles, signal processing, node BOM, array geometry, economics, deployment, applications — **start here** |
| [`papers/ORCA_Research_Paper.md`](papers/ORCA_Research_Paper.md) | Academic research paper | Parts I–XII: physics, array design, economics, **Part X convergence**, 144 references |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Module map, headline table, cross-refs |
| [`platform_simulation.py`](platform_simulation.py) | Local entry script | Runs full `orca_sim` suite |
| [`orca_sim_package/`](orca_sim_package/) | Python package | Dipole detection, array coverage, economics modules |

### Simulation modules (`orca_sim_package/orca_sim/`)

| Module | File | Role |
|---|---|---|
| Corrosion field | [`orca_sim_package/orca_sim/physics/corrosion_field.py`](orca_sim_package/orca_sim/physics/corrosion_field.py) | DC dipole lateral field, voltage across baseline |
| Propeller field | [`orca_sim_package/orca_sim/physics/propeller_field.py`](orca_sim_package/orca_sim/physics/propeller_field.py) | ELFE oscillating dipole with skin-depth attenuation |
| Detection range | [`orca_sim_package/orca_sim/detection/range.py`](orca_sim_package/orca_sim/detection/range.py) | SNR threshold solver, Type-039 and surface-vessel ranges |
| Array coverage | [`orca_sim_package/orca_sim/array/coverage.py`](orca_sim_package/orca_sim/array/coverage.py) | Node spacing, 54-node northern-coast geometry |
| Signal processing | [`orca_sim_package/orca_sim/processing/matched_filter.py`](orca_sim_package/orca_sim/processing/matched_filter.py), [`orca_sim_package/orca_sim/processing/demon.py`](orca_sim_package/orca_sim/processing/demon.py) | Matched spatial filter, DEMON cyclostationary gain |
| Economics | [`orca_sim_package/orca_sim/economics/unit_cost.py`](orca_sim_package/orca_sim/economics/unit_cost.py) | Tier 1 acquisition and annual operating cost rollup |
| Transit scenario | [`orca_sim_package/orca_sim/scenarios/transit.py`](orca_sim_package/orca_sim/scenarios/transit.py) | 8 kn submarine dwell time through detection zone |
| Config | [`orca_sim_package/orca_sim/config.py`](orca_sim_package/orca_sim/config.py) | Dipole moments, electrode noise, integration times |
| Report | [`orca_sim_package/orca_sim/reports/generate.py`](orca_sim_package/orca_sim/reports/generate.py) | Markdown + JSON consolidated output |

---

## Headline numbers (simulation-validated)

| Metric | Value |
|---|---|
| Detection — Type-039 SSK (UEP) | **28.49 km** @ 10 dB SNR |
| Detection — surface ISR vessel (UEP) | **45.22 km** @ 10 dB SNR |
| Classification — propeller (DEMON) | **0.88 km** (short-range fingerprint) |
| Node baseline | **200 m** tip-to-tip, **7** Ag/AgCl electrodes |
| Node spacing (100% coverage) | **57 km** (= 2 × submarine range) |
| Tier 1 array size | **54 nodes** |
| Coastline covered | **3,000 km** (northern Australia threat axis) |
| Per-node production cost (500+) | **~$4,160** |
| Tier 1 acquisition | **$775,676** |
| Annual operating cost | **$298,797** |
| 10-year TCO | **$4,109,322** |
| vs P-8A acquisition | **0.019%** for equivalent persistent coverage |
| P-8A Poseidon (reference) | **$345 M** per airframe, non-persistent |

See [`SIM_README.md`](SIM_README.md) for methodology, scenario matrix, and limitations.

---

## Simulation verification

```bash
python platform_simulation.py
```

Or from the package directory:

```bash
cd orca_sim_package
pip install -r orca_sim/requirements.txt
python run_all.py
```

Reports: `orca_sim_package/orca_sim/outputs/orca_sim_report.md`

Optional JSON summary:

```bash
python platform_simulation.py --json
```

---

## Cross-references

| Related system | Folder |
|---|---|
| GH-SR-IMM filter (track fusion at shore station) | [`../../Filtering/`](../../Filtering/) |
| ARIA-INTEL (maritime domain awareness adjacency) | [`../../Asset Tracking Algorithm/`](../../Asset%20Tracking%20Algorithm/) |
| MT-X Leviathan (platform consumer — coastal defence) | [`../Leviathon Tank/`](../Leviathon%20Tank/) |
| TAIPAN-1 (no direct coupling; portfolio missile family) | [`../TAIPAN Missile/`](../TAIPAN%20Missile/) |
| P-8A cueing integration | Spec §10.6 — ORCA detects, P-8A prosecutes |
| Battle Sim (combat modelling) | [`../../Battle Sim/`](../../Battle%20Sim/) |

---

## Honest framing

- **Not a fielded surveillance system.** Concept and simulation only; no instrumented ocean trials or Collins-class submarine validation.
- **Separate simulator.** Do not expect ORCA rows in [`../weapons_sim_results.md`](../weapons_sim_results.md).
- **Physics model scope.** Homogeneous half-space electrostatics; no bathymetric refraction, sediment layering, or biofouling degradation modelled in baseline sim.
- **Propeller field is classification, not detection.** Long-range contact is DC corrosion UEP; DEMON blade-rate fingerprint operates at sub-kilometre range.
- **Single-node failure creates gaps.** 57 km blind corridor until maintenance replaces the node (12–36 hr vessel transit).

[← Weapons-Defence](../README.md)
