# MP-6.8 Mark II Rifle — simulation traceability

This platform's numbers are produced by the portfolio-wide simulator at [`../weapons_simulation.py`](../weapons_simulation.py), output to [`../weapons_sim_results.md`](../weapons_sim_results.md).

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio physics engine ([`../weapons_simulation.py`](../weapons_simulation.py) via [`../sim_common.py`](../sim_common.py)) and prints a **platform-specific verification slice**—headline numbers and table cross-references for this platform only.

Quick start (from this folder):

```bash
python platform_simulation.py
```

To regenerate the full portfolio results, use `cd .. && python weapons_simulation.py`.

---

## Cartridge key

| Parameter | Simulator key |
|---|---|
| Cartridge | **`6.8x51mm`** |
| Weapon name in `WEAPONS` dict | **`MP-6.8 Mark II Rifle`** |
| Barrel length | 406 mm |
| Bullet mass | 8.7 g WC-cored AP |

---

## Relevant tables in `weapons_sim_results.md`

| Section | Content for this platform |
|---|---|
| **§1 Cartridges** | `6.8x51mm` row — 731 m/s MV, 2,324 J ME, 307 MPa P_max |
| **§2 Weapons** | `MP-6.8 Mark II Rifle` row — 4.10 kg empty, 20 rd mag, 11.3 J free recoil |
| **§3 RHA penetration** | `6.8x51mm` column — 11.1 mm @ 0 m, 8.1 mm @ 300 m, 3.9 mm @ 1,000 m |
| **§4 Trajectory** | Velocity vs range for `6.8x51mm` |
| **§5 Suppressor attenuation** | `MP-6.8 Mark II Rifle` — 410 cm³, 7 baffles, 40.0 dB |
| **§6 Muzzle blast & hearing protection** | SPL stack for 6.8 rifle |
| **§7 Bullet drop** | Zeroed drop for `6.8x51mm` (100 m zero) |
| **§8 Wind drift** | Crosswind drift for `6.8x51mm` |
| **§9 Hatcher max effective range** | > 3,500 m effective (sim cap), 1,030 m supersonic |
| **§10 Barrel life** | 80,398 rounds, 250 rpm sustained |
| **§11 Peak recoil force** | 358 N peak shoulder force, 35 % brake, 20.0 mm stock travel |
| **§12 Obliquity penetration** | 60° RHA — 3.7 mm @ 0 m normal-equivalent |
| **§13 Body-armour V50** | 5.56 × 45 and 7.62 × 51 threat rows for armour comparison context |
| **§23 Lifecycle** | `MP-6.8 Mark II Rifle` — bore life 25,000 rd, MRBF 15,656 analytic / 15,000 simulated, felt recoil 1.63 ft·lb, barrel SF 1.99, FTF 1:55,000 |

---

## Re-run command

Regenerate portfolio output after parameter edits (see **Local verification script** above).

---

## Implementation notes

- **Cartridge block** (~line 479): `6.8x51mm` — SIG-XM7-class geometry, 8.7 g projectile.
- **Weapon block** (~line 622): `MP-6.8 Mark II Rifle` → `cartridge="6.8x51mm"`, `weight_kg=4.10`, `magazine=20`.
- **Muzzle brake:** 35 % impulse redirection in §11 peak-recoil model.

---

## Not a standalone sim package

All physics lives in the parent [`../weapons_simulation.py`](../weapons_simulation.py). This folder contains specification and research documents only.


## §23 Lifecycle

Portfolio lifecycle for **`MP-6.8 Mark II Rifle`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `MP-6.8 Mark II Rifle` — bore life 25,000 rd, MRBF 15,656 analytic / 15,000 simulated, felt recoil 1.63 ft·lb, barrel SF 1.99, FTF 1:55,000 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |