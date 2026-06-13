# APES Body Armour — Simulation Coverage

**No standalone simulator.** Ballistic-limit and back-face deformation numbers for APES panels are computed inside the portfolio-wide [`../weapons_simulation.py`](../weapons_simulation.py) script and written to [`../weapons_sim_results.md`](../weapons_sim_results.md) **§13**.

---

## What is modelled

| Panel | Areal density | Composition |
|---|---|---|
| **APES military** | 35 kg/m² | 16-layer soft stack + 12 mm B4C ceramic tile |
| **APES-L police** | 22 kg/m² | 10-layer soft stack + 8 mm B4C tile |

Both panels use `composite_factor = 1.65` in the Lambert-Jonas / Recht-Ipson V50 fit (`armour_v50_ms()` in `weapons_simulation.py`).

### Threat set (§13)

| Threat | Velocity | Mass | Diameter |
|---|---|---|---|
| 9 mm 124 gr ball | 390 m/s | 8.0 g | 9.0 mm |
| 5.7 × 28 SS190 | 716 m/s | 2.0 g | 5.7 mm |
| 5.56 × 45 M855 | 940 m/s | 4.0 g | 5.7 mm |
| 7.62 × 51 M80 ball | 820 m/s | 9.5 g | 7.82 mm |
| .30-06 M2 AP | 878 m/s | 10.8 g | 7.82 mm |
| 7.62 × 54R B-32 AP | 820 m/s | 10.4 g | 7.92 mm |
| 12.7 × 99 M2 AP | 890 m/s | 46.0 g | 12.7 mm |
| 15.2 × 115 APYT (sabot) | 781 m/s | 64.0 g | 8.5 mm |

### BFD rule

For threats **below** V50, clay-witness back-face deformation is reported via `back_face_deformation_mm()`. NIJ 0101.06 pass limit: **< 44 mm**. Threats at or above V50 are marked **PERFORATED** (BFD undefined).

---

## Quick start

```bash
cd ..
python weapons_simulation.py
```

Open `weapons_sim_results.md` and scroll to **§13. Body-armour V50 ballistic-limit + back-face deformation**.

---

## Key functions in `weapons_simulation.py`

| Function | Lines (approx.) | Role |
|---|---|---|
| `armour_v50_ms()` | ~921 | V50 from areal density, projectile mass/diameter, composite factor |
| `back_face_deformation_mm()` | ~955 | Clay-witness BFD when impact velocity < V50 |
| Tier-2 armour block | ~1654–1693 | Panel/threat matrix → `tier2.armour_v50` |
| Markdown §13 writer | ~2088–2102 | Renders results table |

---

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`APES_Specification.md`](APES_Specification.md) |
| Research paper | [`APES_Research_Paper.md`](APES_Research_Paper.md) |
| Portfolio results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §13 |

---

*APES simulation coverage — for research and design study use only. Not validated against physical ballistic test data.*
