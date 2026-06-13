# MP-4.6M Guardian Pistol — simulation traceability

This platform's numbers are **not** produced by a local simulation package. They come from the portfolio-wide simulator at [`../weapons_simulation.py`](../weapons_simulation.py), which writes human-readable output to [`../weapons_sim_results.md`](../weapons_sim_results.md) and machine-readable output to [`../weapons_sim_results.json`](../weapons_sim_results.json).

---

## Cartridge key

| Parameter | Simulator key |
|---|---|
| Cartridge | **`4.6x30mm`** |
| Weapon name in `WEAPONS` dict | **`MP-4.6M Pistol`** |
| Barrel length | 180 mm (pistol configuration) |
| Bullet mass | 2.6 g tungsten-cored AP |

The PDW variant uses the **same loaded round** but a separate simulator entry **`4.6x30mm_PDW`** with a 266.7 mm barrel — do not confuse the two when editing parameters.

---

## Relevant tables in `weapons_sim_results.md`

| Section | Content for this platform |
|---|---|
| **§1 Cartridges** | Internal ballistics row for `4.6x30mm` — MV, ME, P_max, recoil impulse |
| **§2 Weapons** | Per-platform row for `MP-4.6M Pistol` — empty mass, magazine, action, free recoil |
| **§3 RHA penetration** | `4.6x30mm` column — 3.8 mm @ 0 m through 1.3 mm @ 1,000 m |
| **§4 Trajectory** | Velocity vs range for `4.6x30mm` |
| **§5 Suppressor attenuation** | `MP-4.6M Pistol integral` — 80 cm³, 6 baffles, 40.0 dB |
| **§6 Muzzle blast & hearing protection** | Unsuppressed/suppressed SPL and layered protection stack |
| **§7 Bullet drop** | Zeroed drop table for `4.6x30mm` (100 m zero) |
| **§8 Wind drift** | 10 mph crosswind drift for `4.6x30mm` |
| **§9 Hatcher max effective range** | 878 m (KE > 80 J), 301 m supersonic |
| **§10 Barrel life** | 302,501 rounds, 250 rpm sustained thermal bound |
| **§11 Peak recoil force** | 559 N peak shoulder force, 4.0 mm stock travel |
| **§12 Obliquity penetration** | NATO 60° RHA reduction for `4.6x30mm` |
| **§13 Body-armour V50** | Threat interactions (4.6 mm not individually tabulated; see 5.7 × 28 mm and 9 mm anchors) |

---

## Re-run command

From this folder:

```bash
cd ..
python weapons_simulation.py
```

The script regenerates `weapons_sim_results.md` and `weapons_sim_results.json`. After editing cartridge geometry, barrel length, weapon mass, suppressor volume, or armour layup in `weapons_simulation.py`, re-run and update the specification and research paper to match.

---

## Implementation notes

- **Tier-1:** Le Duc / Powley closed-form internal ballistics (`η = 0.72`), G7 drag external integration, De Marre terminal ballistics (`K = 7.80 × 10⁻⁴`).
- **Tier-2:** Westin muzzle-blast SPL, suppressor adiabatic-expansion cap at 40 dB, sprung-stock peak recoil force, barrel-life erosion model calibrated against M4 anchor.
- **Weapon block** in `weapons_simulation.py` (~line 616): `MP-4.6M Pistol` → `cartridge="4.6x30mm"`, `weight_kg=0.92`, `magazine=20`.

---

## Not a standalone sim package

Unlike [`../BSG10 Goliath/bsg10_sim_package/`](../BSG10%20Goliath/bsg10_sim_package/) or [`../OAM-VEST Non Lethal Sonic Weapon/OAM-VEST_Simulation_Package/`](../OAM-VEST%20Non%20Lethal%20Sonic%20Weapon/OAM-VEST_Simulation_Package/), this folder contains **no local Python modules**. All physics lives in the parent script. To change Guardian numbers, edit `weapons_simulation.py` and re-run — do not add a per-platform sim fork unless the physics model itself diverges from the portfolio toolchain.

---

[← Back to platform README](README.md) · [← Weapons-Defence README](../README.md)
