# TACT-1 Mark II — simulation reference

**Portfolio simulator (Tier C).** TACT-1 Mark II shelf-life and lipid-oxidation numbers trace to the parent script [`../weapons_simulation.py`](../weapons_simulation.py), not a standalone package in this folder.

---

## Relevant output

| Domain | `weapons_sim_results.md` section | Function area in `weapons_simulation.py` |
|---|---|---|
| Ration shelf life (Arrhenius Q10 = 2) | §22 TACT-1 shelf life | Tier-2 lipid oxidation model |

Sub-platform simulations:

| Subfolder | Simulator |
|---|---|
| [`PODS- Edible High Energy Protein/`](PODS-%20Edible%20High%20Energy%20Protein/) | Standalone [`pods_simulation.py`](PODS-%20Edible%20High%20Energy%20Protein/pods_simulation.py) |
| [`ASNP Sports Nutrition/`](ASNP%20Sports%20Nutrition/) | Prose formulation numbers; see [`ASNP Sports Nutrition/SIM_README.md`](ASNP%20Sports%20Nutrition/SIM_README.md) |

---

## Re-run

```bash
cd ..
python weapons_simulation.py
```

Regenerates [`../weapons_sim_results.md`](../weapons_sim_results.md) including §22.

---

[← Back to TACT-1 README](README.md)
