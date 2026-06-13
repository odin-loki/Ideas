# APES-L Mark I — police body armour

> **6.5 kg full-body police armour** — ionic-liquid STF carrier (−25 °C comfort), single-use 75 mm B4C tiles to .50 AE, NIJ Level II stab full-body, **66.2 %** composite injury-score improvement, **12+ yr** panel life. Twenty-three physics-based simulations in the operator spec; portfolio **§13** cross-checks soft-panel V50.

---

## Reading order

1. **This README**
2. [`APES-L_Specification.md`](APES-L_Specification.md) — operator spec (23 simulations)
3. [`APES-L_Research_Paper.md`](APES-L_Research_Paper.md) — research paper
4. [`SIM_README.md`](SIM_README.md)
5. [`platform_simulation.py`](platform_simulation.py)

---

## Headline numbers

| Metric | Value |
|---|---|
| Ready-to-wear mass | **~6.5 kg** |
| vs current police vest | **20.25 kg** (67 % lighter) |
| Ballistic envelope | .44 Mag + 12 g slug + .50 AE (single-use tile) |
| Stab | **NIJ Level II — full body** |
| Composite injury-score improvement | **66.2 %** |
| 10-year TCO saving (500 officers) | **+$1.85 M AUD** |
| Panel service life (§23) | **10 yr** |
| Ceramic tile replacement (§23) | **4 yr** |
| Soft panel refresh (§23) | **6 yr** |

---

## Simulation verification

**Dual path:** 23 reduced-order simulations in the spec (Sims 1–23) + portfolio **§13** V50/BFD for the soft-panel cross-check + **§23.1** lifecycle service intervals via [`../../Weapons-Defence/weapon_lifecycle.py`](../../Weapons-Defence/weapon_lifecycle.py).

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | `apes_l_body_armour` — §13 slice |
| [`../../Weapons-Defence/weapons_sim_results.md`](../../Weapons-Defence/weapons_sim_results.md) | APES-L police panel row (§13) + lifecycle (§23.1) |
| [`../../Weapons-Defence/weapon_lifecycle.py`](../../Weapons-Defence/weapon_lifecycle.py) | §23 lifecycle — panel, tile, soft-stack intervals |

---

## Quick start

```bash
python platform_simulation.py
```

---

## Related work

- [`../../Weapons-Defence/APES Body Armour/`](../../Weapons-Defence/APES%20Body%20Armour/) — military APES parent
- [`../MP-4.6P Guardian LE/`](../MP-4.6P%20Guardian%20LE/) — sibling police pistol
- [`../README.md`](../README.md)

---

[← Back to Weapons-Police README](../README.md)