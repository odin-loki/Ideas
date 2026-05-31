# BSG-10 "Goliath" — Simulation Suite

**10-Gauge Semi-Automatic Bullpup Combat Shotgun**  
Full system simulation: ballistics · action dynamics · recoil · geometry · lifecycle

---

## Overview

This package is the complete computational design tool for the BSG-10 Goliath —
a 10-gauge semi-automatic bullpup combat shotgun engineered from first principles.
It runs six independent physics simulations, passes results between them, and
generates a consolidated performance and lifecycle report.

**Validated headline numbers:**

| Result | Value |
|---|---|
| Peak chamber pressure | 73.5 MPa (10,665 PSI) — 3% below SAAMI limit |
| Muzzle velocity | 415 m/s (1,362 fps) |
| Magazine capacity | 45 rounds (200 mm Tommy-style drum) |
| Overall length | 1,012 mm (39.8 in) with 510 mm barrel |
| Loaded weight | ~8.9 kg (19.6 lb) |
| Peak shoulder force | ~490 N — softer than a 12-gauge field gun (1,800 N ref.) |
| Bolt lug fatigue SF | 4.3× — infinite fatigue life |
| Barrel life | ~19,000 rounds (Melonite-coated) |

---

## Package Structure

```
bsg10_sim/
├── __init__.py               Public API: BSG10Config, run_all()
├── config.py                 All design parameters (dataclasses)
├── run_all.py                CLI entry point — runs full suite
├── requirements.txt
│
├── ballistics/
│   └── internal.py           Module A — internal ballistics, propellant calibration
│
├── dynamics/
│   ├── balanced_action.py    Module B — bolt carrier + counter-mass ODE
│   └── recoil_chain.py       Module C — integrated recoil simulation
│
├── mechanical/
│   ├── dimensions.py         Module D — dimensional geometry and clearance checks
│   └── magazine.py           Module E — helical belt drum capacity and feed force
│
├── lifecycle/
│   └── parts_life.py         Module F — all component life models
│
├── reports/
│   └── generate.py           Consolidated text report generator
│
└── outputs/                  Generated figures and reports (created at runtime)
```

---

## Installation

### Requirements

- Python 3.10+
- NumPy ≥ 1.24
- SciPy ≥ 1.10
- Matplotlib ≥ 3.7

### Setup

```bash
git clone <repo>
cd bsg10_sim
pip install -r requirements.txt
```

No build or compilation step required. Pure Python.

---

## Quick Start

### Run the full suite (CLI)

```bash
python run_all.py
```

This runs all six modules, writes seven figures to `outputs/`, and writes a
text report to `outputs/simulation_report.txt`.

```bash
python run_all.py --no-plots         # skip figure generation (faster)
python run_all.py --variant heavy    # run 12-gauge comparison variant
python run_all.py --module ballistics # run a single module
```

### Use as a library

```python
from bsg10_sim import run_all, BSG10Config

# Run with default config
results = run_all()

# Access results from each module
print(results.ballistics.muzzle_vel)      # 415.0 m/s
print(results.ballistics.P_peak / 1e6)    # 73.5 MPa
print(results.ballistics.saami_pass)      # True

print(results.action.reduction_pct)       # 81.9%  cycling impulse reduction
print(results.recoil.peak_force_td)       # ~490 N  shoulder force
print(results.dimensions.all_pass)        # True   all geometry checks pass
print(results.magazine.capacity)          # 45 rounds
print(results.life.barrel_life)           # ~19,000 rounds
print(results.life.lug_SF_fatigue)        # 4.3×  infinite fatigue life
```

### Run individual modules

```python
from bsg10_sim import BSG10Config
from bsg10_sim.ballistics.internal import run as run_ballistics

cfg = BSG10Config()
bal = run_ballistics(cfg, plot_results=True)
print(f"{bal.P_peak/1e6:.2f} MPa — {'PASS' if bal.saami_pass else 'FAIL'}")
```

---

## Modules

### Module A — Internal Ballistics (`ballistics/internal.py`)

Computes chamber pressure vs. position, projectile velocity, and transit time.

**Physics model:**
- Rising phase (0 → x_peak = 9 mm): `P = P_peak × (x/x_peak)^0.35`
- Expansion phase (x_peak → 510 mm): `P = P_peak × (V_peak/V)^γ`  where γ = 1.12
- Calibration: binary search on P_peak until `v_muzzle = 415.0 m/s`
- Work–energy theorem: trapezoidal integration for velocity profile

**Key output: BallisticsResult**
```
P_peak        float   Pa    calibrated peak pressure
muzzle_vel    float   m/s   muzzle velocity
transit_time  float   s     barrel transit time
port_pressure float   Pa    pressure at gas port location
impulse_total float   N·s   total recoil impulse (shot + gas)
saami_pass    bool          True if P_peak ≤ 75.8 MPa
```

**Figure generated:** `A_internal_ballistics.png`
- Panel 1: Pressure vs position (with SAAMI limit and gas port marker)
- Panel 2: Velocity vs position
- Panel 3: Pressure vs time

---

### Module B — Balanced Action Dynamics (`dynamics/balanced_action.py`)

Solves the coupled ODE for the bolt carrier + counter-mass rack-and-pinion system.

**Physics model:**
- Effective system mass: `m_eff = m_carrier + m_counter / R²` where R = gear ratio
- Carrier driven by triangular gas pulse (1 ms rise, 4 ms decay, 8,500 N peak)
- Buffer: spring 18,000 N/m + damper 850 N·s/m
- Net cycling impulse: `(m_carrier − m_counter/R) × v_max`

**Key output: ActionResult**
```
carrier_stroke_mm   float   mm    max carrier travel
reduction_pct       float   %     cycling impulse reduction
impulse_raw         float   N·s   unbalanced cycling impulse
impulse_balanced    float   N·s   residual after balancing
stroke_pass         bool          True if within 80 mm limit
```

**Figure generated:** `B_balanced_action.png`
- Panel 1: Carrier and counter-mass displacement vs time
- Panel 2: Velocities vs time
- Panel 3: Momentum cancellation plot

---

### Module C — Integrated Recoil Chain (`dynamics/recoil_chain.py`)

Time-domain ODE simulation of the complete recoil path from powder burn to shoulder.

**Two models:**
1. **Analytical bound** — gun arrives at CBS-10 at full free-recoil velocity (conservative)
2. **Time-domain ODE** — firing impulse applied as half-sine pulse while CBS-10 acts simultaneously (accurate)

**Recoil stack applied in order:**
1. Bullpup bore-axis geometry (−15% muzzle flip torque)
2. 12-port hybrid compensator (−30% gas impulse)
3. Balanced action counter-mass (−82% cycling impulse)
4. Short-recoil floating barrel (impulse spread)
5. Hydraulic action buffer (carrier energy absorbed)
6. CBS-10 progressive springs (3-stage: 7/45/140 kN/m)
7. CBS-10 asymmetric dampers (240 N·s/m comp / 80 N·s/m ext)

**Key output: RecoilResult**
```
peak_force_td     float   N     time-domain shoulder force
peak_force_bound  float   N     analytical upper bound
cbs_max_travel_mm float   mm    CBS-10 peak compression
reduction_pct     float   %     vs raw unmitigated 10-gauge
travel_pass       bool          True if ≤ 52 mm limit
```

**Figure generated:** `C_recoil_chain.png`
- Panel 1: Gun velocity vs time
- Panel 2: CBS-10 compression vs time
- Panel 3: Shoulder force vs time (with references)
- Panel 4: Bar comparison: raw 10-ga / 12-ga ref / BSG-10

---

### Module D — Dimensional Geometry (`mechanical/dimensions.py`)

Checks all component dimensions fit within the bullpup envelope. Generates a
dimensioned side-elevation schematic.

**Checks performed:**
| Check | Limit |
|---|---|
| Overall Length | ≤ 1,100 mm |
| Bore height above stock | ≤ 160 mm |
| Foregrip balance zone | 450–720 mm from butt |
| CBS-10 damper gap | ≥ 22 mm |
| Barrel radial clearance | ≥ 0.30 mm |
| Carrier stroke clearance | ≤ 80 mm |
| CBS-10 travel | ≤ 52 mm |
| Drum below bore axis | ≥ 30 mm clearance |

**Key output: DimResult**
```
oal_mm        float   mm    Overall Length
all_pass      bool          True if all checks pass
checks        list          List[CheckItem] with individual results
```

**Figure generated:** `D_dimensions.png`
- Left: side-elevation schematic with all components annotated
- Right: pass/fail check table

---

### Module E — Magazine Geometry (`mechanical/magazine.py`)

Computes Tommy-style helical belt drum capacity and verifies feed reliability.

**Geometry model:**
- Shells arranged in a helical coil track inside the drum
- Belt driven by central clock spring
- Capacity = total track length / shell pitch
- Feed force modelled as proportional to clock spring wind

**Key output: MagazineResult**
```
capacity        int         shell count
drum_depth_mm   float   mm  (= shell length + 6 mm)
n_coils         float       number of spiral turns
feed_force_last float   N   feed force on last round
feed_pass       bool        True if ≥ 8 N minimum
```

**Figure generated:** `E_magazine.png`
- Left: helix cross-section with shell positions
- Right: feed force vs rounds remaining

---

### Module F — Parts Life Analysis (`lifecycle/parts_life.py`)

Physics-based lifecycle models for all major components.

**Models used:**

| Component | Physics Model |
|---|---|
| Barrel throat erosion | Power-law erosion: `dE = k × (P/P_ref)^α × f_material × f_shot` |
| Bolt lug fatigue | S-N curve comparison: `τ_op vs S_e` (Basquin) |
| Bolt lug fretting | Archard wear: `V = K × σ × δ_slip` |
| CBS-10 coil springs | Compression set: `CS(n) = CS_∞ × (1 − e^(−n/N))` |
| CBS-10 Belleville | Stress relaxation (same model, different constants) |
| CBS-10 damper seals | Archard wear (PTFE lip seal on chrome rod) |
| CBS-10 pads | Compression set (Sorbothane 50A, D3O polymer) |
| Gas piston | Power-law erosion (port face, 17-4PH SS) |
| Gas cylinder | Bore wear (Archard, chrome-lined) |
| Barrel bushings | Archard wear (PTFE-bronze composite, low-PV) |

**Key output: LifeResult**
```
barrel_life     int     rounds to pattern degradation
piston_warn     int     rounds to service warning
pad_life        int     rounds to pad replacement
lug_SF_fatigue  float   fatigue safety factor (>1.0 = infinite life)
components      list    List[ComponentLife] sorted by life
```

**Figures generated:**
- `F1_cbs10_life.png` — CBS-10 component degradation curves
- `F2_life_summary.png` — integrated life bar chart + maintenance cost model

---

## Config Reference

All design parameters live in `config.py` as Python dataclasses.
Edit them directly to explore design variants.

### CartridgeConfig

```python
cfg = BSG10Config()

# Change to lighter load
cfg.cartridge.shot_mass  = 0.050    # kg
cfg.cartridge.target_vel = 400.0    # m/s

# Change propellant (gamma affects pressure profile shape)
cfg.cartridge.gamma  = 1.10         # slower powder
cfg.cartridge.x_peak = 0.010        # m  peak position
```

### RecoilConfig — tune the CBS-10

```python
# Stiffer initial stage (less travel, higher peak force)
cfg.recoil.cbs_k1 = 10000.0   # N/m

# More aggressive compensator
cfg.recoil.comp_efficiency = 0.35

# Change damping ratio (compression / extension)
cfg.recoil.cbs_c_comp = 300.0  # N·s/m
cfg.recoil.cbs_c_ext  = 100.0  # N·s/m
```

### MagazineConfig — resize the drum

```python
# Larger drum for more capacity
cfg.magazine.drum_od = 0.240   # m  (240 mm)

# Tighter belt for higher capacity
cfg.magazine.link_gap = 0.002  # m  (2 mm between shells)
```

### ActionConfig — balanced action tuning

```python
# Change counter-mass (must rebalance gear ratio)
cfg.action.counter_mass = 0.400   # kg
# Gear ratio is computed automatically: carrier_mass / counter_mass
```

---

## Config Variants (CLI)

Three named variants are available via `--variant`:

| Variant | Description |
|---|---|
| `default` | BSG-10 as specified — 10-gauge, 415 m/s, all mitigations |
| `heavy` | 12-gauge conversion — same platform, smaller bore (comparison) |
| `light` | Reduced charge — 390 m/s, lower pressure (suppressed use) |

```bash
python run_all.py --variant heavy --no-plots
```

---

## Output Files

All outputs are written to `bsg10_sim/outputs/`:

| File | Module | Content |
|---|---|---|
| `A_internal_ballistics.png` | A | Pressure/velocity/time profiles |
| `B_balanced_action.png` | B | Carrier dynamics, momentum cancellation |
| `C_recoil_chain.png` | C | Full recoil simulation |
| `D_dimensions.png` | D | Schematic + pass/fail table |
| `E_magazine.png` | E | Drum geometry + feed force |
| `F1_cbs10_life.png` | F | CBS-10 degradation curves |
| `F2_life_summary.png` | F | Integrated life chart |
| `simulation_report.txt` | All | Consolidated text report |

---

## Physics Notes

### Propellant Model

The simulation uses an effective adiabatic index γ = 1.12 to model the
expansion phase. This corresponds to a progressive large-flake or disc-type
powder (e.g. Hodgdon Longshot or Winchester 296 at increased grain size).

Physically: γ < 1.25 (ideal adiabatic) because slower-burning propellants
release energy throughout the expansion phase rather than front-loading it.
This produces a broader, lower pressure peak — the key fix for SAAMI compliance.

The model does **not** implement a full thermodynamic burn model (Noble-Abel
equation + Saint-Robert burn rate). It uses a calibrated pressure profile
that:
1. Passes through P_peak at x_peak
2. Decays as (V_peak/V)^γ in the expansion phase
3. Is calibrated to hit the target muzzle velocity exactly

This is the standard approach for propellant trade studies where the goal
is comparing the effect of load changes on system-level performance, not
first-principles combustion chemistry.

### Archard Wear Model

Volumetric wear rate: `V_wear = K × F_normal × L_sliding`

where K is the Archard wear coefficient (mm³/(N·mm)). Values used:

| Interface | K (mm³/(N·mm)) | Source |
|---|---|---|
| PTFE lip seal on chrome rod | 3.0×10⁻⁸ | Tribology literature |
| PTFE-bronze bushing on SS shaft | 1.2×10⁻⁷ | DuPont bearing data |
| Ion-nitrided steel fretting | 0.25×10⁻⁷ | Gear fretting database |

### Compression Set Model

Spring set accumulates asymptotically: `CS(n) = CS_∞ × (1 − exp(−n/N_char))`

This is an empirical model calibrated to manufacturer compression set data
for the specified materials:
- Chrome-silicon (SAE 9254): CS_∞ = 5.5%, N_char = 95,000 rounds
- Sorbothane 50A: CS_∞ = 28%, N_char = 9,000 rounds
- D3O polymer: CS_∞ = 32%, N_char = 11,500 rounds

---

## Extending the Suite

### Adding a new module

1. Create `bsg10_sim/<package>/my_module.py`
2. Implement `simulate(cfg) -> MyResult` and `run(cfg, plot_results) -> MyResult`
3. Import and call from `run_all.py`
4. Add result field to `AllResults` in `__init__.py`

### Adding a new config variant

In `run_all.py`, add a case to `_load_variant()`:

```python
elif name == "suppressed":
    cfg = BSG10Config()
    cfg.gas.n_regulator = 3
    cfg.cartridge.target_vel = 370.0   # subsonic
    cfg.cartridge.powder_mass = 0.0052
    return cfg
```

### Sensitivity analysis

```python
import numpy as np
from bsg10_sim import BSG10Config, run_all

# Sweep peak position to find optimal gas port timing
peak_forces = []
for x_pk in np.linspace(0.006, 0.015, 10):
    cfg = BSG10Config()
    cfg.cartridge.x_peak = x_pk
    r = run_all(cfg, plots=False, save_report=False)
    peak_forces.append(r.recoil.peak_force_td)
    print(f"x_peak={x_pk*1e3:.1f}mm → peak={peak_forces[-1]:.0f}N")
```

---

## Licence

This simulation suite is proprietary software developed for the BSG-10
programme. All rights reserved.

For licencing enquiries regarding use in defence procurement, academic
research, or commercial firearms development, contact the author.

---

## Acknowledgements

Physics models draw on the following published sources:
- Carlucci & Jacobson, *Ballistics: Theory and Design of Guns and Ammunition*, 2nd ed.
- Budynas & Nisbett, *Shigley's Mechanical Engineering Design*, 10th ed. (spring fatigue)
- Archard (1953), *Contact and Rubbing of Flat Surfaces*, J. Appl. Phys. (wear model)
- Sorbothane Inc. technical data sheets (compression set model)
- MIL-HDBK-1839C, *Fuze Design, Safety and Arming* (gas port timing reference)

---

*BSG-10 "Goliath" — Simulation-validated. Ready for prototype.*
