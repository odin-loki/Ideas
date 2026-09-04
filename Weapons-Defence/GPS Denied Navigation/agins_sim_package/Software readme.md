# AGINS — Simulation Suite

**Autonomous GPS-Independent Navigation System**  
Multi-modal passive navigation: celestial · MagNav · polar sky · PDR · inertial · GH-SR-IMM fusion

---

## Quick start

```bash
cd agins_sim_package
pip install -r agins_sim/requirements.txt
python run_all.py
python run_all.py --no-plots
```

From platform root: `python platform_simulation.py`

---

## Headline numbers (seed=42)

| Platform | Scenario | Mean | P90 |
|----------|----------|------|-----|
| Soldier | Open night | 26 m | 57 m |
| Soldier | Urban | 61 m | 91 m |
| Ship | Clear sky | 37 m | 66 m |
| Ship | Storm | 56 m | 96 m |

Soldier tracks match specification; ship clear-sky runs ~22% above spec target (30 m) — see SIM_README limitations.

Filter cross-reference: [`../../../Filtering/GH_SR_IMM_Research_Paper.md`](../../../Filtering/GH_SR_IMM_Research_Paper.md)

[← Platform README](../README.md) · [← SIM_README](../SIM_README.md)
