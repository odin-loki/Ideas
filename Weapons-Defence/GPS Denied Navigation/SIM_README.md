# AGINS — simulation guide

**Dedicated platform simulation** via the local [`agins_sim_package/`](agins_sim_package/) suite. AGINS fuses five passive sensor modalities through the **GH-SR-IMM** filter defined in [`../../Filtering/`](../../Filtering/). Ship (FOG-grade) and soldier (MEMS) platforms are modelled in separate scenario modules that converge in a consolidated report.

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the full `agins_sim` package and prints headline numbers. Use this from the platform folder root:

```bash
python platform_simulation.py
python platform_simulation.py --json
```

Full suite (same engine, more verbose):

```bash
cd agins_sim_package
pip install -r agins_sim/requirements.txt
python run_all.py
```

Outputs land in [`agins_sim_package/agins_sim/outputs/`](agins_sim_package/agins_sim/outputs/):

| File | Role |
|---|---|
| `agins_sim_report.md` | Human-readable consolidated report |
| `agins_sim_results.json` | Machine-readable full results |

---

## Requirements

```bash
pip install numpy scipy matplotlib
```

Python 3.9+ required. Matplotlib is optional (scenario plots only).

---

## Simulation modules

| Module | Path | Models |
|---|---|---|
| **GH-SR-IMM filter** | `filter/gh_sr_imm.py` | NIG/GIG posterior, SR-CKF propagation, 3-model IMM (CV / CA / HI), scalar PDR speed update, GRIA α gate |
| **Standard KF** | `filter/standard_kf.py` | Baseline Kalman + PDR + compass comparison |
| **Ship platform** | `platforms/ship.py` | FOG IMU (0.05°/hr), atomic MagNav, celestial two-body, polar compass, storm degradation |
| **Soldier platform** | `platforms/soldier.py` | MEMS IMU (2°/hr), PDR speed decoupling, star fix, urban magnetic disturbance |
| **Environments** | `scenarios/environments.py` | Sky fraction, urban disturbance, night / mixed route profiles |
| **Celestial** | `sensors/celestial.py` | Sun/moon/star fixes, refraction NIG model |
| **MagNav** | `sensors/magnav.py` | Anomaly map matching, Student-t outliers, α rejection |
| **Polar compass** | `sensors/polar_compass.py` | Rayleigh sky polarisation, blunder mode |
| **PDR** | `sensors/pdr.py` | Step-counter speed (σ≈3%), ZUPT anchoring |
| **IMU / DR** | `sensors/imu.py` | MEMS and FOG dead-reckoning baselines |
| **Report** | `reports/generate.py` | Markdown + JSON export *(invoked by `run_all.py`)* |

All parameters live in [`agins_sim_package/agins_sim/config.py`](agins_sim_package/agins_sim/config.py).

---

## Cross-portfolio references

| Subsystem | Portfolio folder | Sim role |
|---|---|---|
| GH-SR-IMM filter | [`../../Filtering/`](../../Filtering/) | **Authoritative filter definition** — NIG noise, IMM bank, SR-CKF, GH-JPDA fix |
| GH-SR-IMM paper | [`../../Filtering/GH_SR_IMM_Research_Paper.md`](../../Filtering/GH_SR_IMM_Research_Paper.md) | Formal algorithm and benchmark methodology |
| GRIA α gate | [`../../Compression Algorithms/`](../../Compression%20Algorithms/) | Information-theoretic fix quality metric |
| Leviathan (vehicle nav consumer) | [`../Leviathon Tank/`](../Leviathon%20Tank/) | Platform that would mount vehicle-grade AGINS |
| Legacy soldier script | [`archive/nav_sim_soldier.py`](archive/nav_sim_soldier.py) | **Superseded** — monolithic prototype; do not cite for headline numbers |

### Filter — dual documentation track

The [`Filtering/`](../../Filtering/) folder documents GH-SR-IMM for **multi-target tracking** (GH-JPDA, GOSPA benchmarks). AGINS applies the same NIG + IMM + square-root core to **single-platform navigation fusion** with navigation-specific adapters (GRIA α gate, scalar PDR speed observation, MagNav map interface). Use **Filtering** papers for filter mathematics; use **this package** for navigation scenario numbers.

---

## Headline numbers (default run)

| Metric | Value |
|---|---|
| **Ship — clear sky** | **37 m** sim mean, **66 m** P90 *(spec target 30 m / 50 m — ~22% high)* |
| **Ship — 6 hr storm** | **56 m** mean, **96 m** P90 *(spec 57 m / 91 m)* |
| **Soldier — open night** | **26 m** mean, **57 m** P90 |
| **Soldier — urban patrol** | **61 m** mean, **91 m** P90 |
| **Soldier — mixed route** | **30 m** mean |
| PDR DR only (no filter) | **103 m** mean |
| Raw MEMS DR (no filter) | **336 m** mean |
| KF + PDR + compass (baseline) | **48–76 m** mean (scenario-dependent) |
| GH-SR-IMM manoeuvre gain vs KF | **+52 % to +87 %** |
| PDR speed accuracy | **σ ≈ 3 %** of speed |
| Soldier IMU drift | **2°/hr** MEMS |
| Ship IMU drift | **0.05°/hr** FOG |
| Star fix σ (soldier / ship) | **350 m** / **70–100 m** |
| MagNav σ (surveyed / open ocean) | **50–180 m** / rejected (α gate) |

---

## Known model limitations

1. **Synthetic maps** — MagNav uses simplified anomaly fields, not live EMAG2 tiles; open-ocean α rejection is modelled, not survey-validated.
2. **Celestial refraction** — NIG heavy-tail model; no full atmospheric profile integration.
3. **Urban magnetic disturbance** — Parametric rebar/vehicle noise; not building-scale FEM.
4. **No visual odometry** — Urban remedies (camera VO, OSM map matching) documented in spec but not simulated.
5. **Monte Carlo variance** — Default seeds are fixed for reproducibility; ± few metres on mean error across seed sweeps.
6. **Legacy script drift** — [`archive/nav_sim_soldier_report.md`](archive/nav_sim_soldier_report.md) may differ slightly from package output after refactor; cite package reports only.
7. **Ship clear-sky calibration** — FOG maritime module runs ~37 m mean vs 30 m specification; storm track matches within 2 m. Tune `config.py` ship sensor sigmas if tighter spec alignment is required.

Re-run after editing `config.py` and update [`papers/AGINS_Specification.md`](papers/AGINS_Specification.md) and [`papers/AGINS_Research_Paper.md`](papers/AGINS_Research_Paper.md) to match.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)
