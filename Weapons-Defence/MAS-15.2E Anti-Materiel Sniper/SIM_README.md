# MAS-15.2E Anti-Materiel Sniper — simulation traceability

This platform's numbers are produced by the portfolio-wide simulator at [`../weapons_simulation.py`](../weapons_simulation.py), output to [`../weapons_sim_results.md`](../weapons_sim_results.md).

---

## Cartridge key

| Parameter | Simulator key |
|---|---|
| Cartridge | **`15.2x115mm`** |
| Weapon name in `WEAPONS` dict | **`MAS-15.2E Sniper`** |
| Barrel length | 720 mm |
| Bullet mass | 64.0 g (saboted sub-calibre WC penetrator, 8.5 mm sabot diameter) |

---

## Relevant tables in `weapons_sim_results.md`

| Section | Content for this platform |
|---|---|
| **§1 Cartridges** | `15.2x115mm` row — 781 m/s MV, 19,505 J ME, 258 MPa P_max, 82.07 N·s impulse |
| **§2 Weapons** | `MAS-15.2E Sniper` row — 13.20 kg empty, 8 rd mag, bolt action, 255.2 J free recoil |
| **§3 RHA penetration** | `15.2x115mm` column — 42.0 mm @ 0 m, 22.3 mm @ 1,000 m, 16.0 mm @ 1,500 m |
| **§4 Trajectory** | Velocity vs range for `15.2x115mm` |
| **§5 Suppressor attenuation** | `MAS-15.2E Sniper` — 1,800 cm³, 10 baffles, 40.0 dB |
| **§6 Muzzle blast & hearing protection** | SPL stack — 165.0 dB muzzle unsuppressed, 125.0 dB suppressed |
| **§7 Bullet drop** | Zeroed drop for `15.2x115mm` (500 m zero per sim note) |
| **§8 Wind drift** | Crosswind drift — 1.2 cm @ 100 m, 147.1 cm @ 1,000 m |
| **§9 Hatcher max effective range** | > 3,500 m effective (sim cap), supersonic > 3,500 m |
| **§10 Barrel life** | 22,753 rounds, 131 rpm sustained thermal bound |
| **§11 Peak recoil force** | 1,042 N peak shoulder force, 65 % brake, 45.0 mm stock travel |
| **§12 Obliquity penetration** | 60° RHA — 13.9 mm @ 0 m, 7.4 mm @ 1,000 m |
| **§13 Body-armour V50** | `15.2 × 115 APYT` threat row — perforates all modelled armour panels |

---

## Re-run command

```bash
cd ..
python weapons_simulation.py
```

---

## Implementation notes

- **Cartridge block** (~line 515): `15.2x115mm` — APYT saboted geometry, 64 g projectile, 8.5 mm sabot diameter for terminal-ballistics model.
- **Weapon block** (~line 625): `MAS-15.2E Sniper` → `cartridge="15.2x115mm"`, `weight_kg=13.2`, `magazine=8`.
- **Muzzle brake:** 65 % impulse redirection in §11 — mandatory for shoulder-firing safety envelope per spec.
- **Penetration note:** The spec sheet may cite adjusted figures (e.g. 48.4 mm @ muzzle) derived from saboted-core geometry; the simulator's De Marre correlation in §3 reports **42.0 mm @ 0 m** for the `15.2x115mm` cartridge key. Treat `weapons_sim_results.md` as authoritative when numbers diverge.

---

## Not a standalone sim package

All physics lives in the parent [`../weapons_simulation.py`](../weapons_simulation.py). This folder contains specification and research documents only.

---

[← Back to platform README](README.md) · [← Weapons-Defence README](../README.md)
