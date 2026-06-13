# 57 mm Autocannon — portfolio simulation guide

**Tier-C validation** via the shared [`../weapons_simulation.py`](../weapons_simulation.py) suite. Output is written to [`../weapons_sim_results.md`](../weapons_sim_results.md).

---

## Simulator keys

| Role | Key in `weapons_simulation.py` |
|---|---|
| Cartridge | `57x347mm` |
| Weapon platform | `57 mm Autocannon` |
| Penetrator model | `PENETRATORS["57x347mm"]` — Lanz–Odermatt long-rod, DU-class |

---

## Requirements

```bash
pip install numpy scipy
```

Python 3.9+ required. No other dependencies.

---

## Quick start

```bash
cd ..
python weapons_simulation.py
```

Regenerates `weapons_sim_results.md` and `weapons_sim_results.json` in the parent `Weapons-Defence/` folder.

---

## Result tables for this platform

| Topic | `weapons_sim_results.md` section |
|---|---|
| Internal / external ballistics | §1 (cartridge row `57x347mm`) |
| Weapon mass, recoil, MV | §2 (weapon row `57 mm Autocannon`) |
| RHA penetration vs range | §3 (`57x347mm` heavy cartridge) |
| Velocity vs range | §4 |
| Muzzle blast / hearing stack | §6 |
| Hatcher max effective range | §9 |
| Barrel life / sustained rpm | §10 |
| Peak recoil force | §11 |
| NATO 60° obliquity | §12 |
| HE-Frag warhead (HEIAP-T) | §14 (`57 mm Autocannon HE-Frag`) |
| HEDP shaped-charge | §15 (`57 mm Autocannon HEDP`) |
| Wind drift | §8 (heavy cartridge row) |

---

## Headline numbers (default run)

| Metric | Value |
|---|---|
| MV | **948 m/s** |
| ME | **1 077 666 J** |
| P_max | **257 MPa** |
| Recoil impulse | **4 397 N·s** |
| RHA @ 0 m | **139.7 mm** |
| RHA @ 500 m | **125.4 mm** |
| RHA @ 1 000 m | **113.0 mm** |
| Free recoil (350 kg mount) | **27 621 J** |
| Peak mount force | **139 832 N** |
| Barrel life | **1 166 rounds** |
| Sustained rpm | **80** |

---

## Editing parameters

Cartridge geometry and propellant live in the `CARTRIDGES["57x347mm"]` entry; mount mass, magazine, and action in `WEAPONS["57 mm Autocannon"]`. After edits, re-run from the parent directory and update [`57mm_Autocannon_Specification.md`](57mm_Autocannon_Specification.md) against the new §1–§15 values.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)
