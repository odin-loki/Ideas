# 140 mm Tank KE Round — portfolio simulation guide

**Tier-C validation** via [`../weapons_simulation.py`](../weapons_simulation.py). Output: [`../weapons_sim_results.md`](../weapons_sim_results.md).

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

```bash
cd ..
python weapons_simulation.py
```

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

---

## Editing parameters

Edit `CARTRIDGES["140mm_KE"]`, `PENETRATORS["140mm_KE"]`, and `WEAPONS["140 mm Tank Gun"]`. Re-run and sync [`140mm_Tank_KE_Specification.md`](140mm_Tank_KE_Specification.md) against updated §1–§15 and §17.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)
