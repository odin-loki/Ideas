# ADF Tactical Field Kit — Simulation Coverage

**No standalone simulator.** The ADF Tactical Field Kit is an aggregate procurement specification. Weight budgets, component masses, cost analysis, and operational claims are prose engineering numbers in [`ADF_Tactical_Field_Kit_Specification.md`](ADF_Tactical_Field_Kit_Specification.md) — not outputs of a dedicated Python script in this folder.

---

## What is not modelled here

| Domain | Status |
|---|---|
| Pack load-transfer biomechanics | Not in portfolio simulator |
| Water filtration throughput / contaminant rejection | Not in portfolio simulator |
| Titanium tool fatigue life | Not in portfolio simulator |
| Total field-kit weight budget optimisation | Not in portfolio simulator |

---

## Linked subfolder simulations

Nutrition components referenced by the field kit have partial simulator coverage elsewhere:

| Component | Simulator | Section / file |
|---|---|---|
| **TACT-1 Mark II shelf life** | [`../weapons_simulation.py`](../weapons_simulation.py) | §22 — Arrhenius Q10 lipid-oxidation model; see [`../weapons_sim_results.md`](../weapons_sim_results.md) §22 |
| **PODS energy density** | [`../TACT-1 Tactical Ration/PODS- Edible High Energy Protein/pods_simulation.py`](../TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/pods_simulation.py) | Standalone PODS cleavage and density model |
| **ASNP** | None dedicated | Prose numbers in ASNP operator spec |

### TACT-1 folder

- README: [`../TACT-1 Tactical Ration/README.md`](../TACT-1%20Tactical%20Ration/README.md)
- PODS sim: [`../TACT-1 Tactical Ration/PODS- Edible High Energy Protein/PODS_README.md`](../TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/PODS_README.md)

### ASNP

- Operator spec: [`../TACT-1 Tactical Ration/ASNP Sports Nutrition/ASNP_Specification.md`](../TACT-1%20Tactical%20Ration/ASNP%20Sports%20Nutrition/ASNP_Specification.md)
- Research paper: [`ASNP Sports Nutrition/ASNP_Research_Paper.md`](ASNP%20Sports%20Nutrition/ASNP_Research_Paper.md)

---

## Parent portfolio simulator

```bash
cd ../..
python weapons_simulation.py
```

Relevant sections for field-kit *nutrition integration* only:

- §22 — TACT-1 shelf life vs storage temperature

---

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`ADF_Tactical_Field_Kit_Specification.md`](ADF_Tactical_Field_Kit_Specification.md) |

---

*ADF Tactical Field Kit — aggregate specification; no dedicated simulation package.*
