# ORCA — Simulation Suite

**Ocean Resonant Coastal Array**  
Passive seabed electric-field detection: DC corrosion UEP · propeller DEMON · matched spatial filter · array coverage · Tier 1 economics

---

## Quick start

```bash
cd orca_sim_package
pip install -r orca_sim/requirements.txt
python run_all.py
python run_all.py --no-plots
```

From platform root: `python platform_simulation.py`

---

## Headline numbers (default config)

| Scenario | Range |
|----------|-------|
| Type-039 SSK — UEP (DC corrosion) | 28.49 km |
| Surface ISR vessel — UEP | 45.22 km |
| Type-039 SSK — propeller (DEMON) | 0.88 km |
| Tier 1 array | 54 nodes, 57 km spacing |
| Tier 1 acquisition | $775,676 |
| Annual operating cost | $298,797 |
| vs P-8A acquisition | 0.019% |

Physics cross-reference: [`../papers/ORCA_System_Specification.md`](../papers/ORCA_System_Specification.md) Appendix A

[← Platform README](../README.md) · [← SIM_README](../SIM_README.md)
