# AlNiCyN Armour — Simulation Coverage

**No standalone simulator.** AlNiCyN alloy mechanical properties (yield strength, hardness, RHA-equivalence factors, cost per tonne) live in [`AlNiCyN_Specification.md`](AlNiCyN_Specification.md) as prose engineering numbers. They are **not** recomputed by a dedicated script in this folder.

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

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`AlNiCyN_Specification.md`](AlNiCyN_Specification.md) |
| Research paper | [`AlNiCyN_Research_Paper.md`](AlNiCyN_Research_Paper.md) |
| APES body-armour sim (§13) | [`../APES Body Armour/SIM_README.md`](../APES%20Body%20Armour/SIM_README.md) |

---

*AlNiCyN simulation coverage — material properties in spec; ballistic interactions via parent portfolio simulator only.*
