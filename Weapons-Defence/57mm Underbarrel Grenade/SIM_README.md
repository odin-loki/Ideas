# 57 mm Underbarrel Grenade — portfolio simulation guide

**Tier-C validation** via [`../weapons_simulation.py`](../weapons_simulation.py). Output: [`../weapons_sim_results.md`](../weapons_sim_results.md).

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio physics engine ([`../weapons_simulation.py`](../weapons_simulation.py) via [`../sim_common.py`](../sim_common.py)) and prints a **platform-specific verification slice**—headline numbers and table cross-references for this platform only.

Quick start (from this folder):

```bash
python platform_simulation.py
```

To regenerate the full portfolio results, use `cd .. && python weapons_simulation.py`.

---

## Simulator keys

| Role | Key in `weapons_simulation.py` |
|---|---|
| Cartridge | `57mm_LV_grenade` |
| Weapon platform | `57 mm Underbarrel GL` |

---

## Requirements

```bash
pip install numpy scipy
```

Python 3.9+ required.

---

## Quick start

Run [`platform_simulation.py`](platform_simulation.py) from this folder (see **Local verification script** above). After parameter edits, regenerate the full portfolio with `cd .. && python weapons_simulation.py`.

---

## Result tables for this platform

| Topic | `weapons_sim_results.md` section |
|---|---|
| Ballistics | §1 (`57mm_LV_grenade`), §2 (`57 mm Underbarrel GL`) |
| Velocity vs range | §4 |
| Muzzle blast / hearing | §6 |
| Max effective range | §9 |
| Barrel life | §10 |
| Peak recoil force | §11 |
| HE-Frag warhead | §14 (`57 mm Underbarrel HE-Frag`) |
| HEAT warhead | §15 (`57 mm Underbarrel HEAT`) |
| **§23 Lifecycle** | `57 mm Underbarrel GL` — bore life 5,000 rd, MRBF 13,857 analytic / 30,000 simulated, felt recoil 160.75 ft·lb, barrel SF 3.67, FTF 1:40,000 |

---

## Headline numbers (default run)

| Metric | Value |
|---|---|
| MV | **149 m/s** |
| ME | **3 872 J** |
| P_max | **109 MPa** |
| Recoil impulse | **52.71 N·s** |
| Free recoil | **578.8 J** |
| Peak force (18 mm travel) | **48 237 N** |
| A_L (HE-Frag) | **11 m²** |
| r_eff | **1.9 m** |
| HEAT pen | **41 mm RHA** |
| Barrel life | **69 500 rounds** |
| Bore life service (§23) | **5 000 rounds** |
| MRBF analytic (§23) | **~13 857 rounds** |
| MRBF simulated (§23) | **~30 000 rounds** |
| Felt recoil (§23) | **~160.262 ft·lb** |
| Barrel SF_yield (§23) | **1.41** |
| FTF rate (§23) | **1:40 000** |

---

## Editing parameters

Edit `CARTRIDGES["57mm_LV_grenade"]` and `WEAPONS["57 mm Underbarrel GL"]`, re-run, then sync the spec against updated §1, §2, §11, §14, and §15.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)

## §23 Lifecycle

Portfolio lifecycle for **`57 mm Underbarrel GL`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `57 mm Underbarrel GL` — bore life 5,000 rd, MRBF 13,857 analytic / 30,000 simulated, felt recoil 160.75 ft·lb, barrel SF 3.67, FTF 1:40,000 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |