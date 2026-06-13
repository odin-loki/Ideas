# MP-4.6M Defender PDW — simulation traceability

This platform's numbers are produced by the portfolio-wide simulator at [`../weapons_simulation.py`](../weapons_simulation.py), output to [`../weapons_sim_results.md`](../weapons_sim_results.md).

---

## Cartridge key

| Parameter | Simulator key |
|---|---|
| Cartridge | **`4.6x30mm_PDW`** |
| Weapon name in `WEAPONS` dict | **`MP-4.6M Defender PDW`** |
| Barrel length | 266.7 mm (PDW configuration) |
| Bullet mass | 2.6 g (identical loaded round to `4.6x30mm`) |

The `_PDW` suffix denotes the **same projectile, case, and powder charge** with a longer barrel allowing more complete propellant burn. Editing the base `4.6x30mm` cartridge affects both pistol and PDW entries unless barrel-length parameters are changed independently.

---

## Relevant tables in `weapons_sim_results.md`

| Section | Content for this platform |
|---|---|
| **§1 Cartridges** | `4.6x30mm_PDW` row — 542 m/s MV, 382 J ME, 180 MPa P_max |
| **§2 Weapons** | `MP-4.6M Defender PDW` row — 2.10 kg empty, 40 rd mag, 0.8 J free recoil |
| **§3 RHA penetration** | `4.6x30mm_PDW` column — 4.2 mm @ 0 m |
| **§4 Trajectory** | Velocity vs range for `4.6x30mm_PDW` |
| **§5 Suppressor attenuation** | `MP-4.6M Defender PDW` — 180 cm³, 8 baffles, 40.0 dB |
| **§6 Muzzle blast & hearing protection** | SPL stack for Defender PDW |
| **§7 Bullet drop** | Zeroed drop for `4.6x30mm_PDW` (100 m zero) |
| **§8 Wind drift** | Crosswind drift for `4.6x30mm_PDW` |
| **§9 Hatcher max effective range** | 928 m effective, 376 m supersonic |
| **§10 Barrel life** | 302,501 rounds, 250 rpm sustained |
| **§11 Peak recoil force** | 63 N peak shoulder force, 18.0 mm stock travel |
| **§12 Obliquity penetration** | 60° RHA for `4.6x30mm_PDW` |

---

## Re-run command

```bash
cd ..
python weapons_simulation.py
```

---

## Implementation notes

- **Weapon block** (~line 619): `MP-4.6M Defender PDW` → `cartridge="4.6x30mm_PDW"`, `weight_kg=2.10`, `magazine=40`.
- **Cartridge block** (~line 454): `4.6x30mm_PDW` shares projectile geometry with `4.6x30mm` but uses `barrel_length_mm=266.7`.

---

## Not a standalone sim package

All physics lives in the parent [`../weapons_simulation.py`](../weapons_simulation.py). This folder contains specification and research documents only.

---

[← Back to platform README](README.md) · [← Weapons-Defence README](../README.md)
