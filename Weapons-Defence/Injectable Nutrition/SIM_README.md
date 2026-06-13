# Injectable Nutrition — Simulation Coverage

**Portfolio simulator only.** Osmolality and safe-infusion-bound checks for GlycoDur-P / NutriComplete-P formulations are computed inside [`../weapons_simulation.py`](../weapons_simulation.py) and written to [`../weapons_sim_results.md`](../weapons_sim_results.md) **§21**.

---

## What is modelled

| Output | Method |
|---|---|
| Osmolality (mOsm/kg) | Plumb / Holliday–Segar solute-sum model from macronutrient + electrolyte composition |
| Safe-infusion check | Peripheral bound < 600 mOsm/kg; central bound < 1 800 mOsm/kg |

### Headline results (§21)

| Formulation | Osmolality | Peripheral safe? | Central safe? |
|---|---|---|---|
| Injectable Food baseline (1 200 kcal/L) | 3 037 mOsm/kg | NO | NO |
| Injectable Food field-ration (1 800 kcal/L) | 4 436 mOsm/kg | NO | NO |
| Saline reference (0.9 %) | 308 mOsm/kg | YES | YES |
| Standard TPN reference | 2 280 mOsm/kg | NO | NO |

---

## Quick start

```bash
cd ..
python weapons_simulation.py
```

Open `weapons_sim_results.md` and scroll to **§21. Injectable-nutrition osmolality**.

---

## Key functions in `weapons_simulation.py`

| Function | Role |
|---|---|
| `osmolality_mOsm_kg()` (~line 1370) | Computes mOsm/kg from glucose, amino acids, electrolytes |
| Tier-2 block (~line 1822) | Evaluates baseline + field-ration formulations |
| Markdown §21 writer | Renders results table with safe-infusion flags |

---

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`Injectable_Nutrition_Specification.md`](Injectable_Nutrition_Specification.md) |
| Research paper | [`Injectable_Nutrition_Research_Paper.md`](Injectable_Nutrition_Research_Paper.md) |
| Portfolio results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §21 |

---

*Injectable-nutrition simulation coverage — osmolality model only. Not validated against clinical infusion studies.*
