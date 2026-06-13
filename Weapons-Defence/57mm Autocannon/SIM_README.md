# 57 mm Autocannon — portfolio simulation guide

**Tier-C validation** via the shared [`../weapons_simulation.py`](../weapons_simulation.py) suite. Output is written to [`../weapons_sim_results.md`](../weapons_sim_results.md).

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio physics engine ([`../weapons_simulation.py`](../weapons_simulation.py) via [`../sim_common.py`](../sim_common.py)) and prints a **platform-specific verification slice**—headline numbers and table cross-references for this platform only.

Quick start (from this folder):

```bash
python platform_simulation.py
```

To regenerate the full portfolio results (`weapons_sim_results.md` and `weapons_sim_results.json`), use `cd .. && python weapons_simulation.py`.

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

Run [`platform_simulation.py`](platform_simulation.py) from this folder (see **Local verification script** above). After editing parameters in `weapons_simulation.py`, regenerate the full portfolio with `cd .. && python weapons_simulation.py`, then update [`57mm_Autocannon_Specification.md`](57mm_Autocannon_Specification.md) against the new §1–§15 values.

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
| **§23 Lifecycle** | `57 mm Autocannon` — bore life 2,500 rd, MRBF 8,375 analytic / 10,000 simulated, felt recoil 3678.12 ft·lb, barrel SF 1.45, FTF 1:35,000 |

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

## §23 Lifecycle

Portfolio lifecycle for **`57 mm Autocannon`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `57 mm Autocannon` — bore life 2,500 rd, MRBF 8,375 analytic / 10,000 simulated, felt recoil 3678.12 ft·lb, barrel SF 1.45, FTF 1:35,000 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |