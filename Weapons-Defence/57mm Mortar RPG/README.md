# 57 mm Enhanced Dual-Purpose System (EDPS) — Mortar / RPG

> **A simulation-validated muzzle-loaded dual-mode infantry support tube firing a 1.40 kg HEAT + frag warhead at 187 m/s for 24.4 kJ muzzle energy and 111 MPa peak chamber pressure.** Headline mount: 7.20 kg tube, ~1 500 m RPG direct-fire / ~2 500 m mortar indirect, 4 966 J free recoil (53 632 N peak mount force), 33 m² HE lethal area.

> **Genre note.** Commercial Sensitive / defence-technology register for tonal coherence. No real procurement or prototype data implied. **Numbers trace to [`../weapons_simulation.py`](../weapons_simulation.py) — cartridge key `57mm_mortar`, weapon key `57 mm Mortar/RPG`.**

---

## What this folder is

The 57 mm EDPS is a **complete platform subfolder**: operator specification, academic research paper, and **Tier-C portfolio simulation**. One smoothbore tube serves both shoulder-anchored RPG direct-fire and tripod mortar indirect-fire modes.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`57mm_Mortar_RPG_Specification.md`](57mm_Mortar_RPG_Specification.md) — product and engineering spec (TRP-2026-104).
3. [`57mm_Mortar_RPG_Research_Paper.md`](57mm_Mortar_RPG_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — portfolio sim guide.
5. Run [`platform_simulation.py`](platform_simulation.py) — PASS/FAIL claim verification against the portfolio sim.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`57mm_Mortar_RPG_Specification.md`](57mm_Mortar_RPG_Specification.md) | Operator / product specification | Dual-mode tube, warhead, recoil, deployment, Tier-2 imports. |
| [`57mm_Mortar_RPG_Research_Paper.md`](57mm_Mortar_RPG_Research_Paper.md) | Academic research paper | HEAT + frag terminal models, mortar trajectory, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Keys, CLI, result-table map. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | Runs portfolio engine; prints PASS/FAIL checks for this platform's spec claims. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Simulator source | Cartridge `57mm_mortar`, weapon `57 mm Mortar/RPG`. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative output | Single source of truth for all numbers. |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §§1–2, 8–11, 14–15, **§23**.

| Metric | Value |
|---|---|
| Cartridge | **57 mm mortar mode** (`57mm_mortar`) |
| Muzzle velocity | **187 m/s** (613 fps) |
| Muzzle energy | **24 427 J** |
| Peak chamber pressure | **111 MPa** (16 048 psi) |
| Mount mass | **7.20 kg** |
| Free recoil | **4 966 J** (3 663 ft·lb) |
| Peak mount force | **53 632 N** (12 058 lbf) |
| Mortar HE lethal area | **33 m²** (r_eff 3.3 m) |
| HEAT penetration (CL-20) | **43 mm RHA** |
| Barrel life | **21 122 rounds** |
| Sustained rpm (thermal) | **57** |
| Wind drift @ 500 m | **0.98 m** (10 mph crosswind) |
| Bore life service (§23) | **8,000 rounds** |
| MRBF analytic (§23) | **~11,041 rounds** |
| MRBF simulated (§23) | **~15,000 rounds** |
| Felt recoil (§23) | **~227.710 ft·lb** |
| Barrel SF_yield (§23) | **3.69** |
| FTF rate (§23) | **1:25,000** |

---

## 🔬 Simulation verification

All headline numbers in this README trace to [`../weapons_sim_results.md`](../weapons_sim_results.md), produced by [`../weapons_simulation.py`](../weapons_simulation.py) and [`../weapon_lifecycle.py`](../weapon_lifecycle.py) (§23). Use the local verification script to confirm spec claims without regenerating the full portfolio:

```bash
python platform_simulation.py
```

The script prints **PASS/FAIL** checks for each claim in the specification and research paper.

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Local PASS/FAIL verification slice for this platform |
| [`SIM_README.md`](SIM_README.md) | Cartridge/weapon keys, table cross-references, methodology |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative tabulated output — cite in every spec edit |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | §23 lifecycle — structural SF, parts-life, reliability MC |

To regenerate the **full portfolio** after editing shared parameters:

```bash
cd ..
python weapons_simulation.py
```

Optional JSON summary:

```bash
python platform_simulation.py --json
```

---

## 🚀 Quick start (simulator)

**From this folder** — verify platform claims:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for cartridge key `57mm_mortar`, weapon key `57 mm Mortar/RPG`, and result-table map.

---

## 🚧 Honest framing

- **Not a fielded weapon.** Simulation only; no dual-mode live-fire demonstration.
- **Recoil class.** 4 966 J per shot is 120 mm-mortar territory — hydraulic buffer and tripod / baseplate are mandatory.
- **Manual reload bound.** Operational rate is 6–8 rpm (reload cycle), not the 57 rpm thermal ceiling.

---

## 🔗 Related work in this repo

- [`../57mm Autocannon/`](../57mm%20Autocannon/) — high-velocity 57 mm APFSDS (shared bore §3)
- [`../57mm Underbarrel Grenade/`](../57mm%20Underbarrel%20Grenade/) — light under-barrel HE-FRAG
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — 57 mm bore commonality

---

[← Back to Weapons-Defence README](../README.md)