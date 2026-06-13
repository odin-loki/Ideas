# APES-L Mark I — simulation documentation

## Engine path

| Layer | File | Role |
|---|---|---|
| Spec simulations | [`APES-L_Specification.md`](APES-L_Specification.md) §6 | 23 physics-based Sims 1–23 (weight, BFD, TCO, IL-STF, tiles) |
| Portfolio cross-check | [`../../Weapons-Defence/weapons_simulation.py`](../../Weapons-Defence/weapons_simulation.py) §13 | `APES-L police (10-layer + 8 mm B4C, 22 kg/m²)` V50/BFD |
| Tier-3 lifecycle | [`../../Weapons-Defence/weapon_lifecycle.py`](../../Weapons-Defence/weapon_lifecycle.py) | §23.1 — panel, tile, soft-stack service intervals |
| Results | [`../../Weapons-Defence/weapons_sim_results.md`](../../Weapons-Defence/weapons_sim_results.md) | §13 armour table; §23.1 lifecycle |

## Platform ID

`apes_l_body_armour`

## Re-run

```bash
python platform_simulation.py
```
