# Caseless Bullets — Simulation Coverage

**No dedicated BPC simulator.** The Biopolymère Caseless (BPC) System has no standalone Python module and no bespoke row in [`../weapons_simulation.py`](../weapons_simulation.py). Ballistic design targets are **conceptually anchored** to the conventional **5.56 × 45 mm NATO** entry in portfolio results **§1**.

---

## What is modelled (indirectly)

The BPC spec targets sit inside the existing 5.56 × 45 mm simulator envelope:

| Parameter | Simulator §1 (5.56 × 45) | BPC design target |
|---|---|---|
| Muzzle velocity | 939 m/s | 900–960 m/s |
| Muzzle energy | 1 764 J | ~1 700–1 800 J |
| Peak chamber pressure | 374 MPa | 414–483 MPa (60–70 ksi) |

Cook-off temperature (> 270 °C), protein-casing chemistry, volumetric energy density (5.2 MJ/L), and chamber-sealing mechanics are **not modelled** in the portfolio simulator.

---

## Quick start (conventional baseline only)

```bash
cd ..
python weapons_simulation.py
```

Open `weapons_sim_results.md` and scroll to **§1. Small-arms internal ballistics** for the 5.56 × 45 mm reference row.

---

## Future work

A dedicated BPC module would need to model:
- Nitrated poly-amino-acid propellant thermochemistry (Ω% oxygen balance)
- Protein-casing ablation and chamber-seal dynamics
- Cook-off vs ambient temperature (HITP-analogous threshold)

None of these exist in the current codebase.

---

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`Caseless_Bullets_Specification.md`](Caseless_Bullets_Specification.md) |
| Research paper | [`Caseless_Bullets_Research_Paper.md`](Caseless_Bullets_Research_Paper.md) |
| Portfolio results (5.56 baseline) | [`../weapons_sim_results.md`](../weapons_sim_results.md) §1 |

---

*Caseless-bullets simulation coverage — conceptual only. No runnable BPC simulator.*
