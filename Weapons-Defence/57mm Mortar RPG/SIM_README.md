# 57 mm Mortar / RPG — portfolio simulation guide

**Tier-C validation** via [`../weapons_simulation.py`](../weapons_simulation.py). Output: [`../weapons_sim_results.md`](../weapons_sim_results.md).

---

## Simulator keys

| Role | Key in `weapons_simulation.py` |
|---|---|
| Cartridge | `57mm_mortar` |
| Weapon platform | `57 mm Mortar/RPG` |

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
| Ballistics | §1 (`57mm_mortar`), §2 (`57 mm Mortar/RPG`) |
| Velocity vs range | §4 |
| Wind drift | §8 (heavy cartridge) |
| Muzzle blast / hearing | §6 |
| Max effective range | §9 |
| Barrel life | §10 |
| Peak recoil force | §11 |
| Mortar HE fragmentation | §14 (`57 mm Mortar HE`) |
| HEAT warhead | §15 (`57 mm Mortar/RPG HEAT`) |

---

## Headline numbers (default run)

| Metric | Value |
|---|---|
| MV | **187 m/s** |
| ME | **24 427 J** |
| P_max | **111 MPa** |
| Recoil impulse | **267.41 N·s** |
| Free recoil | **4 966 J** |
| Peak mount force | **53 632 N** |
| A_L (mortar HE) | **33 m²** |
| r_eff | **3.3 m** |
| HEAT pen | **43 mm RHA** |
| Barrel life | **21 122 rounds** |

---

## Editing parameters

Edit `CARTRIDGES["57mm_mortar"]` and `WEAPONS["57 mm Mortar/RPG"]`, re-run, then update the spec against §1–§15.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)
