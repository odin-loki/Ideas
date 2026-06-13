# 140 mm Tank KE Round — portfolio simulation guide

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
| Cartridge | `140mm_KE` |
| Weapon platform | `140 mm Tank Gun` |
| Penetrator model | `PENETRATORS["140mm_KE"]` — Lanz–Odermatt DU long-rod |

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
| Ballistics | §1 (`140mm_KE`), §2 (`140 mm Tank Gun`) |
| RHA penetration vs range | §3 (`140mm_KE` heavy cartridge) |
| Velocity vs range | §4 |
| Wind drift | §8 |
| Muzzle blast / hearing | §6 |
| Max effective range | §9 |
| Barrel life | §10 |
| Peak recoil force | §11 |
| NATO 60° obliquity | §12 |
| HE-Frag warhead | §14 (`140 mm Multi-Effect HE-Frag`) |
| HEAT warhead | §15 (`140 mm Multi-Effect HEAT`) |
| CL-20 detonation chemistry | §17 |
| **§23 Lifecycle** | `140 mm Tank Gun` — bore life 700 rd, MRBF 3,502 analytic / 3,750 simulated, felt recoil 22914.36 ft·lb, barrel SF 2.23, FTF 1:8,000 |

---

## Headline numbers (default run)

| Metric | Value |
|---|---|
| MV | **1 698 m/s** |
| ME | **9 227 097 J** |
| P_max | **199 MPa** |
| Recoil impulse | **48 905 N·s** |
| RHA @ 0 m | **867.1 mm** |
| RHA @ 500 m | **698.1 mm** |
| RHA @ 1 000 m | **540.9 mm** |
| RHA @ 2 000 m | **326.7 mm** |
| RHA @ 60° / 0 m | **533.8 mm** |
| Free recoil | **351 715 J** |
| Peak mount force | **178 056 N** |
| Barrel life | **618 rounds** |
| HE-Frag A_L | **1 173 m²** |
| HEAT pen | **103 mm RHA** |
| Bore life service (§23) | **618 rounds** |
| MRBF analytic (§23) | **~3 502 rounds** |
| MRBF simulated (§23) | **~3 750 rounds** |
| Felt recoil (§23) | **~22 915.411 ft·lb** |
| Barrel SF_yield (§23) | **2.23** |
| FTF rate (§23) | **1:8 000** |

---

## Editing parameters

Edit `CARTRIDGES["140mm_KE"]`, `PENETRATORS["140mm_KE"]`, and `WEAPONS["140 mm Tank Gun"]`. Re-run and sync [`140mm_Tank_KE_Specification.md`](140mm_Tank_KE_Specification.md) against updated §1–§15 and §17.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)

## §23 Lifecycle

Portfolio lifecycle for **`140 mm Tank Gun`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `140 mm Tank Gun` — bore life 700 rd, MRBF 3,502 analytic / 3,750 simulated, felt recoil 22914.36 ft·lb, barrel SF 2.23, FTF 1:8,000 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |