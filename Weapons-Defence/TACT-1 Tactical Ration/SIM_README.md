# TACT-1 Mark II — simulation reference

**Portfolio simulator (Tier C).** TACT-1 Mark II shelf-life and lipid-oxidation numbers trace to the parent script [`../weapons_simulation.py`](../weapons_simulation.py), not a standalone package in this folder.

---

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder (ration shelf life §22).

```bash
python platform_simulation.py
```

To regenerate the full portfolio results file, still run:

```bash
cd ..
python weapons_simulation.py
```

---

## Relevant output

| Domain | `weapons_sim_results.md` section | Function area in `weapons_simulation.py` |
|---|---|---|
| Ration shelf life (Arrhenius Q10 = 2) | §22 TACT-1 shelf life | Tier-2 lipid oxidation model |

Sub-platform simulations:

| Subfolder | Simulator |
|---|---|
| [`PODS- Edible High Energy Protein/`](PODS-%20Edible%20High%20Energy%20Protein/) | Standalone [`PODS- Edible High Energy Protein/pods_simulation.py`](PODS-%20Edible%20High%20Energy%20Protein/pods_simulation.py) |
| [`ASNP Sports Nutrition/`](ASNP%20Sports%20Nutrition/) | Prose formulation numbers; see [`ASNP Sports Nutrition/SIM_README.md`](ASNP%20Sports%20Nutrition/SIM_README.md) |

---

## Re-run

```bash
cd ..
python weapons_simulation.py
```

Regenerates [`../weapons_sim_results.md`](../weapons_sim_results.md) including §22.

---

## §23 Lifecycle

Portfolio lifecycle for **`TACT-1 Mark II Ration`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `TACT-1 Mark II Ration` — shelf_life_25C_mo=36; shelf_life_49C_mo=12; shelf_life_4C_mo=48 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |