# 57 mm Underbarrel Grenade — portfolio simulation guide

**Tier-C validation** via [`../weapons_simulation.py`](../weapons_simulation.py). Output: [`../weapons_sim_results.md`](../weapons_sim_results.md).

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

```bash
cd ..
python weapons_simulation.py
```

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

---

## Editing parameters

Edit `CARTRIDGES["57mm_LV_grenade"]` and `WEAPONS["57 mm Underbarrel GL"]`, re-run, then sync the spec against updated §1, §2, §11, §14, and §15.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)
