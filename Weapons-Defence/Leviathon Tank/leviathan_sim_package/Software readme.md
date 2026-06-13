# MT-X Mk.II Leviathan — Simulation Suite

**Multi-role armoured combat vehicle**  
Full platform simulation: mobility · armour · powertrain · suspension · armament · APS · amphibious · FCS · weight · logistics · cost

---

## Overview

This package is the computational design tool for the MT-X Mk.II Leviathan — a 38-tonne amphibious armoured vehicle with 140 mm main gun, AlNiCyN-5000 armour, and PPU-1300 boxer engine. It runs twelve independent physics and engineering modules and generates a consolidated Markdown + JSON report.

**Validated headline numbers (default `LeviathanConfig`):**

| Result | Value |
|---|---|
| Combat mass | 38,000 kg |
| Power-to-weight | 34.2 hp/t |
| Max road speed | 65 km/h |
| Ground pressure | 66.9 kPa |
| Upper glacis (ERA) | 779 mm eff. RHA |
| Main gun ROF | 8 rpm |
| Portfolio KE @ 2 km | 326.7 mm RHA |
| Swim speed | 7 km/h |
| Unit cost (ex ammo) | $5.82M |

---

## Package structure

```
leviathan_sim/
├── __init__.py
├── config.py                 All design parameters (dataclasses)
├── requirements.txt
├── armour/effective.py       Oblique RHA, ERA, zone mass
├── mobility/performance.py   Speed, range, gradient, ground pressure
├── powertrain/engine.py      PPU-1300 torque curve, fuel
├── suspension/ride.py        Torsion-bar ride dynamics
├── armament/main_gun.py      140 mm autoloader + dual penetration
├── armament/secondary.py     Coax + RWS
├── aps/engagement.py         Hard-kill timeline
├── amphibious/flotation.py   Buoyancy and swim
├── fcs/hit_probability.py    First-round hit probability
├── weight/budget.py          Part XIX reconciliation
├── logistics/maintenance.py  Crew, intervals, transport
├── cost/unit_cost.py         Unit/program cost
├── reports/generate.py       Report generator
└── outputs/                  Generated at runtime
```

---

## Installation

```bash
cd leviathan_sim_package
pip install -r leviathan_sim/requirements.txt
```

Python 3.9+, NumPy only.

---

## Quick start

```bash
python run_all.py
```

From the parent tank folder:

```bash
python platform_simulation.py
```

### Library use

```python
import sys
sys.path.insert(0, "leviathan_sim_package")
from run_all import run_all

results, report_path = run_all()
print(results["mobility"]["power_to_weight_hp_t"])
```

---

## Editing parameters

All constants are in [`leviathan_sim/config.py`](leviathan_sim/config.py). After edits, re-run `run_all.py` and update [`../papers/MT-X_Leviathan_Specification.md`](../papers/MT-X_Leviathan_Specification.md) and [`../SIM_README.md`](../SIM_README.md).

---

[← Platform README](../README.md) · [← SIM_README](../SIM_README.md)
