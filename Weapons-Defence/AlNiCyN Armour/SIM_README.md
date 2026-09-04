# AlNiCyN Armour — Simulation Coverage

**No standalone simulator.** AlNiCyN alloy mechanical properties (yield strength, hardness, RHA-equivalence factors, cost per tonne) live in [`AlNiCyN_Specification.md`](AlNiCyN_Specification.md) as prose engineering numbers. They are **not** recomputed by a dedicated script in this folder.

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio physics engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder. **It also documents scope limits** — alloy-tier properties are not individually modelled; portfolio §3 RHA penetration tables anchor heavy-threat ballistic context.

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

## Where armour interactions are modelled

Ballistic performance against portfolio threats is covered indirectly by the parent [`../weapons_simulation.py`](../weapons_simulation.py):

| Portfolio section | What it covers | Relevance to AlNiCyN |
|---|---|---|
| **§3 — Terminal ballistics / RHA penetration** | de Marre / Lanz / Krupp obliquity models vs standard RHA plate | Vehicle-hull threat interactions at normal and 60° obliquity |
| **§13 — Body-armour V50 + BFD** | Composite panel V50 and clay-witness BFD | Dismounted armour panels (APES, NIJ tiers) — not AlNiCyN plate coupons |

AlNiCyN-specific coupon V50 or ballistic-limit testing is **not** implemented as a separate panel type in the simulator.

---

## What is not modelled

| Domain | Status |
|---|---|
| AlNiCyN-5000 / 7000 / X yield and hardness from composition | Spec prose only |
| Alloy-specific penetration resistance vs KE rod | Uses generic RHA factors in §3 |
| Heat treatment / ageing effects on ballistic limit | Not in simulator |
| AlNiCyN-X metamaterial lattice mechanics | Not in simulator |

---

## Quick start (parent simulator)

```bash
cd ..
python weapons_simulation.py
```

Consult:

- [`../weapons_sim_results.md`](../weapons_sim_results.md) §3 for RHA penetration tables
- [`../weapons_sim_results.md`](../weapons_sim_results.md) §13 for composite body-armour V50/BFD

---






## §23 Lifecycle

Portfolio lifecycle for **`AlNiCyN Armour`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `AlNiCyN Armour` — plate_service_life_yr=15; spall_liner_refresh_yr=7; areal_density_kg_m2=28 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`AlNiCyN_Specification.md`](AlNiCyN_Specification.md) |
| Research paper | [`AlNiCyN_Research_Paper.md`](AlNiCyN_Research_Paper.md) |
| APES body-armour sim (§13) | [`../APES Body Armour/SIM_README.md`](../APES%20Body%20Armour/SIM_README.md) |
| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.1 |