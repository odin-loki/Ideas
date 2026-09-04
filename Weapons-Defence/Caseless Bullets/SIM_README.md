# Caseless Bullets — Simulation Coverage

**No dedicated BPC simulator.** The Biopolymère Caseless (BPC) System has no standalone Python module and no bespoke row in [`../weapons_simulation.py`](../weapons_simulation.py). Ballistic design targets are **conceptually anchored** to the conventional **5.56 × 45 mm NATO** entry in portfolio results **§1**.

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio physics engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder. **It also documents scope limits** — protein-casing chemistry and cook-off are not modelled; the 5.56 × 45 mm baseline from §1 anchors ballistic envelope targets.

```bash
python platform_simulation.py
```

To regenerate the full portfolio output, from this folder:

```bash
cd ..
python weapons_simulation.py
```

That writes [`../weapons_sim_results.md`](../weapons_sim_results.md) and [`../weapons_sim_results.md`](../weapons_sim_results.md).

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







## §23 Lifecycle

Portfolio lifecycle for **`Caseless Bullets (BPC)`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `Caseless Bullets (BPC)` — protein_case_shelf_mo=24; cook_off_safe_temp_C=93; humidity_storage_max_pct=60 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Operator specification | [`Caseless_Bullets_Specification.md`](Caseless_Bullets_Specification.md) |
| Research paper | [`Caseless_Bullets_Research_Paper.md`](Caseless_Bullets_Research_Paper.md) |
| Portfolio results (5.56 baseline) | [`../weapons_sim_results.md`](../weapons_sim_results.md) §1 |