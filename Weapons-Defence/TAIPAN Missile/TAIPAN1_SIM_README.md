# TAIPAN-1 Simulation Suite

**`taipan1_sim.py`** — Complete Python simulation toolkit for the TAIPAN-1
guided ballistic interceptor rocket.

---

## Requirements

```bash
pip install numpy scipy matplotlib
```

Python 3.9+ required. No other dependencies.

---

## Quick Start

```bash
# Full verification run (recommended first — runs everything at design point)
python taipan1_sim.py --sim verify

# Run all analyses
python taipan1_sim.py --sim all --output ./results

# Custom trajectory
python taipan1_sim.py --sim trajectory --ballast 80 --angle 65

# Find optimal launch angle for 50 kg ballast
python taipan1_sim.py --sim launch_angle --ballast 50
```

---

## Simulations

| Flag | Description | Output file |
|---|---|---|
| `verify` | Full verification dashboard — all key numbers | `taipan1_verification.png` |
| `engine` | Engine performance: Isp vs O/F, thrust vs altitude, nozzle profile | `taipan1_engine.png` |
| `trajectory` | Single trajectory at specified ballast and angle | `taipan1_trajectory.png` |
| `ballast` | Ballast sweep 10–250 kg — range, Mach, stability table + plots | `taipan1_ballast.png` |
| `launch_angle` | Launch angle sweep 30–88° — find max range | `taipan1_launch_angle.png` |
| `thrust_profiles` | Compare flat / tapered / hybrid thrust curves | `taipan1_thrust_profiles.png` |
| `engine_sensitivity` | Range vs engine dry mass — shows electric pump advantage | `taipan1_engine_sensitivity.png` |
| `optimise` | Bayesian GP optimisation over fin/nose/ballast geometry | `taipan1_optimise.png` |
| `all` | Runs every analysis above in sequence | All files above |

---

## Arguments

```
--sim           Simulation to run (default: verify)
--ballast       Ballast mass in kg (default: 14.0)
--angle         Launch angle from vertical in degrees (default: 70.4)
--n-init        Bayesian optimiser LHS samples (default: 20)
--n-iter        Bayesian optimiser GP iterations (default: 40)
--output        Output directory for plot files (default: current dir)
```

---

## Design Point

The default configuration matches the TAIPAN-1 specification:

| Parameter | Value |
|---|---|
| Engine | RP-1/LOX, electric pump-fed |
| Thrust (vacuum) | 50.0 kN |
| Isp (vacuum) | 293.1 s |
| Burn time | 30.0 s |
| Propellant mass | 521.8 kg (147 kg RP-1 + 375 kg LOX) |
| Body diameter | 275 mm |
| Total length | 4.87 m |
| Wet mass | 630.8 kg |
| Dry mass | 109.0 kg |
| Mass ratio | 5.787 |
| Ideal Δv | 5,046 m/s |
| Ballast (design) | 14 kg tungsten at 50 mm from nose |
| Launch angle | 70.4° from vertical |
| Max range | ~1,967 km |
| Apogee | ~449 km |
| Max Mach | ~14.5 |
| SM (launch) | 5.29 cal |
| SM (burnout) | 1.57 cal |

---

## Code Architecture

```
taipan1_sim.py
│
├── Constants
│   └── G0, R_AIR, GAMMA_AIR, thermochemical constants for RP-1/LOX
│
├── AtmosphereModel
│   └── US Standard Atmosphere 1976 (0–86 km)
│       .state(alt_m)  →  (pressure, density, temperature, speed_of_sound)
│
├── EngineConfig  (dataclass)
│   └── thrust_vac_N, burn_time_s, of_ratio, p_chamber_pa,
│       expansion_ratio, c_star_eff, cf_efficiency
│
├── EngineResults (dataclass)
│   └── All computed performance parameters
│
├── EngineModel
│   └── .build()                →  EngineResults
│       .thrust_at_altitude(h)  →  float (N)
│       .print_summary()
│
├── VehicleGeometry (dataclass)
│   └── All body/fin dimensions
│       .A_ref, .l_total, .d_ref
│       .from_calibers() classmethod
│
├── AeroModel
│   └── .cp_location()       →  float (m, Barrowman)
│       .cd(Mach, alt)       →  float (total drag coefficient)
│       .cd_curve()          →  (mach_array, cd_array)
│
├── MassModel (dataclass)
│   └── .m_dry, .m_wet       →  float
│       .cg(geo, with_prop)  →  float (m from nose)
│       .stability_margin()  →  float (calibers)
│       .stability_vs_propellant()  →  (fracs%, sm_array)
│       .print_summary()
│
├── FlightSim
│   └── .run()               →  Dict of time-series + scalar metrics
│       .print_summary()
│       Keys: t, h, x, v, mach, cd, thrust, gload,
│             apogee_km, range_km, max_mach, peak_g,
│             max_q_kpa, burnout_v, burnout_h,
│             t_above_100, flight_time
│
├── GaussianProcess
│   └── .fit(X, y)
│       .predict(X_star)     →  (mu, std)
│       .expected_improvement(mu, std, y_best)  →  EI array
│
├── BayesOptimiser
│   └── .run(ecfg, eng)      →  (best_design_dict, y_all_array)
│
└── Analysis functions
    ├── default_vehicle()    →  (ecfg, eng, geo, aero, mass)
    ├── analysis_engine()
    ├── analysis_trajectory()
    ├── analysis_ballast()
    ├── analysis_launch_angle()
    ├── analysis_thrust_profiles()
    ├── analysis_engine_sensitivity()
    ├── analysis_optimise()
    └── analysis_verify()
```

---

## Using as a Library

All classes are importable for use in your own scripts:

```python
from taipan1_sim import (
    EngineConfig, EngineModel,
    VehicleGeometry, AeroModel, MassModel,
    FlightSim, AtmosphereModel
)

# Build engine
cfg = EngineConfig(thrust_vac_N=50_000, burn_time_s=30.0)
em  = EngineModel(cfg)
eng = em.build()
print(f"Isp = {eng.isp_vac:.1f} s")

# Build vehicle
geo  = VehicleGeometry(m_ballast=50.0)  # 50 kg ballast
aero = AeroModel(geo)
mass = MassModel(m_ballast=50.0)

print(f"CP  = {aero.cp_location():.3f} m")
print(f"SM  = {mass.stability_margin(geo, aero):.2f} cal")

# Simulate
sim = FlightSim(geo, aero, mass, cfg, eng, launch_angle_deg=65.0)
R   = sim.run()
print(f"Range  = {R['range_km']:.0f} km")
print(f"Mach   = {R['max_mach']:.2f}")
print(f"Apogee = {R['apogee_km']:.0f} km")
```

---

## Physics Notes

### Atmosphere
US Standard Atmosphere 1976, piecewise model valid 0–86 km.
Gravity is constant at 9.80665 m/s² — adequate for trajectories below 500 km.

### Engine thermochemistry
Gas properties (γ=1.235, Mw=23.3 g/mol, T_chamber=3,670 K) from
NASA CEA at O/F=2.56 for RP-1/LOX. c* and CF computed analytically
from isentropic nozzle flow relations with efficiency factors.

### Aerodynamics
Barrowman equations for centre of pressure (slender body + fin panel method).
Drag uses four-component semi-empirical model:
- Nose wave drag: modified Newton theory with transonic correction
- Skin friction: Schlichting turbulent flat-plate with Van Driest compressibility
- Base drag: empirical Mach function
- Fin drag: bluntness pressure drag

All CD referenced to body cross-sectional area Aref = π(d/2)².

### Trajectory
3-DOF point-mass gravity turn in vertical plane.
Explicit Euler integration at dt=0.05 s (dt=0.1 s for sweeps).
Thrust is altitude-corrected using exact nozzle exit area pressure term:
`F(h) = CF_vac × pc × A_throat − pa(h) × A_exit`

### Stability
Barrowman CP with combined nose + fin CNα weighting.
CG computed from component mass fractions along vehicle length.
Stability margin = (XCP − XCG) / D_body [calibers].

### Bayesian Optimiser
Latin hypercube initialisation followed by Gaussian process surrogate
with squared-exponential kernel and Expected Improvement acquisition.
Optimises: nose_cal, nose_shape, fin_span_cal, fin_root_cal, fin_taper,
fin_sweep, ballast_frac, ballast_pos_cal, launch_angle.
Objective: maximise apogee − 80×max(0, 1.5−SM_burnout) penalty.

---

## Known Limitations

- **3-DOF only** — no angle-of-attack dynamics, no roll, no Earth rotation
- **Point-mass** — structural flexibility and sloshing not modelled
- **No wind** — trajectory is in calm atmosphere
- **Constant gravity** — G0=9.81 m/s² (adequate below ~500 km)
- **Simplified drag** — semi-empirical, not CFD. Transonic regime (M=0.9–1.1)
  is least accurate. Use SU2 or OpenFOAM for higher fidelity.
- **Aerothermal** — no heating model. Nose tip at Mach 14+ re-entry
  requires separate thermal analysis.
- **Guidance** — no GNC model. Trajectory is open-loop gravity turn.

---

## Companion Documents

| Document | File |
|---|---|
| Technical specification | `TAIPAN-1_Technical_Specification_Rev1.0.md` |
| Geometry reference | `TAIPAN-1_Geometry_Reference_Rev1.0.md` |
| Financial analysis | `TAIPAN-1_Financial_Analysis_Rev1.0.md` |

---

## Simulation Output Reference

`FlightSim.run()` returns a dict with the following keys:

| Key | Type | Units | Description |
|---|---|---|---|
| `t` | array | s | Time |
| `h` | array | km | Altitude |
| `x` | array | km | Downrange distance |
| `v` | array | m/s | Speed |
| `mach` | array | — | Mach number |
| `cd` | array | — | Drag coefficient |
| `thrust` | array | N | Engine thrust |
| `gload` | array | g | Structural G-load |
| `apogee_km` | float | km | Maximum altitude |
| `range_km` | float | km | Maximum downrange |
| `max_mach` | float | — | Peak Mach number |
| `peak_g` | float | g | Peak structural G |
| `max_q_kpa` | float | kPa | Max dynamic pressure |
| `burnout_v` | float | m/s | Velocity at burnout |
| `burnout_h` | float | km | Altitude at burnout |
| `t_above_100` | float | s | Time above Kármán line |
| `flight_time` | float | s | Total flight time |

---

*TAIPAN-1 Simulation Suite — for research and design study use only.*
*Not validated against physical test data. See companion spec for disclaimers.*
