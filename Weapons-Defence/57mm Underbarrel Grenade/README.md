# 57 mm Underbarrel Grenade Round (UGR)

> **A simulation-validated single-shot break-action under-barrel HE-FRAG launcher firing a 350 g grenade at 149 m/s for 3 872 J muzzle energy and 109 MPa peak chamber pressure.** Headline mount: 2.40 kg launcher, 11 m² Carlton lethal area (1.9 m effective radius), 48 237 N raw peak rail force (buffered to < 200 N at shoulder).

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme or prototype test data is implied. **Numbers trace to [`../weapons_simulation.py`](../weapons_simulation.py) — cartridge key `57mm_LV_grenade`, weapon key `57 mm Underbarrel GL`.**

---

## What this folder is

The 57 mm UGR is a **complete platform subfolder**: operator specification, academic research paper, and **Tier-C portfolio simulation** via the shared parent simulator. The round shares 57 mm bore geometry with the autocannon and mortar/RPG family but operates at a deliberately low-pressure envelope.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`57mm_Underbarrel_Grenade_Specification.md`](57mm_Underbarrel_Grenade_Specification.md) — product and engineering spec (TRP-2026-105).
3. [`57mm_Underbarrel_Grenade_Research_Paper.md`](57mm_Underbarrel_Grenade_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — portfolio sim keys and result-table map.
5. Run [`platform_simulation.py`](platform_simulation.py) — PASS/FAIL claim verification against the portfolio sim.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`57mm_Underbarrel_Grenade_Specification.md`](57mm_Underbarrel_Grenade_Specification.md) | Operator / product specification | Full TRP-style doc — launcher, warhead, buffer, rail interface, Tier-2 imports. |
| [`57mm_Underbarrel_Grenade_Research_Paper.md`](57mm_Underbarrel_Grenade_Research_Paper.md) | Academic research paper | Methods, fragmentation model, shaped-charge, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Cartridge / weapon keys, CLI, result sections. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | Runs portfolio engine; prints PASS/FAIL checks for this platform's spec claims. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Simulator source | Cartridge `57mm_LV_grenade`, weapon `57 mm Underbarrel GL`. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative output | Cite this file for every numerical claim. |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §§1–2, 10–11, 14–15, **§23**.

| Metric | Value |
|---|---|
| Cartridge | **57 mm LV grenade** (`57mm_LV_grenade`) |
| Muzzle velocity | **149 m/s** (488 fps) |
| Muzzle energy | **3 872 J** |
| Peak chamber pressure | **109 MPa** (15 788 psi) |
| Launcher mass | **2.40 kg** |
| Free recoil | **578.8 J** (426.9 ft·lb) |
| Peak rail force (unbuffered) | **48 237 N** (10 845 lbf) |
| HE-Frag lethal area | **11 m²** (r_eff 1.9 m) |
| Fragment velocity (Gurney) | **1 909 m/s** (720 pre-scored fragments) |
| HEAT penetration | **41 mm RHA** |
| Barrel life | **69 500 rounds** |
| Bore life service (§23) | **5,000 rounds** |
| MRBF analytic (§23) | **~13,857 rounds** |
| MRBF simulated (§23) | **~30,000 rounds** |
| Felt recoil (§23) | **~160.749 ft·lb** |
| Spring fatigue SF (§23) | **9.5** |
| Barrel SF_yield (§23) | **3.67** |
| FTF rate (§23) | **1:40,000** |

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

See [`SIM_README.md`](SIM_README.md) for cartridge key `57mm_LV_grenade`, weapon key `57 mm Underbarrel GL`, and result-table map.

---

## 🚧 Honest framing

- **Not a fielded weapon.** Simulation only; no live fragmentation pattern data.
- **Lethality vs 40 mm M433.** Simulator-grounded 1.9 m effective radius is comparable to, not dramatically greater than, 40 mm grenades — the procurement case rests on bore commonality and cost.
- **Mandatory buffer.** The 48 kN raw rail force requires the hydraulic / elastomeric buffer in §4.2 of the spec.

---

## 🔗 Related work in this repo

- [`../57mm Autocannon/`](../57mm%20Autocannon/) — high-pressure 57 × 347 mm APFSDS mount
- [`../57mm Mortar RPG/`](../57mm%20Mortar%20RPG/) — dual-mode mortar / RPG (33 m² A_L)
- [`../MP-6.8 Mark II Rifle/`](../MP-6.8%20Mark%20II%20Rifle/) — intended host rifle (Picatinny rail)
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — shared 57 mm bore §3

---

[← Back to Weapons-Defence README](../README.md)