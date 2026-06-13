# 57 mm Mortar / RPG — portfolio simulation guide

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

Run [`platform_simulation.py`](platform_simulation.py) from this folder (see **Local verification script** above). After parameter edits, regenerate the full portfolio with `cd .. && python weapons_simulation.py`.

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
| **§23 Lifecycle** | `57 mm Mortar/RPG` — bore life 8,000 rd, MRBF 11,041 analytic / 15,000 simulated, felt recoil 227.71 ft·lb, barrel SF 3.69, FTF 1:25,000 |

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
| Bore life service (§23) | **8 000 rounds** |
| MRBF analytic (§23) | **~11 041 rounds** |
| MRBF simulated (§23) | **~15 000 rounds** |
| Felt recoil (§23) | **~227.281 ft·lb** |
| Barrel SF_yield (§23) | **1.84** |
| FTF rate (§23) | **1:25 000** |

---

## Editing parameters

Edit `CARTRIDGES["57mm_mortar"]` and `WEAPONS["57 mm Mortar/RPG"]`, re-run, then update the spec against §1–§15.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)

## §23 Lifecycle

Portfolio lifecycle for **`57 mm Mortar/RPG`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `57 mm Mortar/RPG` — bore life 8,000 rd, MRBF 11,041 analytic / 15,000 simulated, felt recoil 227.71 ft·lb, barrel SF 3.69, FTF 1:25,000 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |