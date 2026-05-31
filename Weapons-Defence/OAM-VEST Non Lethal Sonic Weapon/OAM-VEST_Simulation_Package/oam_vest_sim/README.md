# OAM-VEST Simulation Package

Acoustic physics simulation suite for the OAM-VEST (Orbital Angular Momentum Vestibular Disruption System) non-lethal acoustic area denial weapon.

All simulations are first-principles physics. No empirical fudge factors.

---

## Package Structure

```
oam_vest_sim/
├── physics.py          Core acoustic physics, propagation, biological thresholds
├── acoustic_array.py   Phased array geometry, gain, OAM beam, phase computation
├── pulse.py            Pulsed regime, power system, LiDAR interleave, dwell timer
├── wavefield.py        2D FDTD acoustic wavefield simulation
├── safety.py           Safety analysis, engagement envelope, interlock simulation
├── report.py           Runs all simulations and writes full markdown report
└── README.md           This file
```

---

## Dependencies

```
numpy
scipy
matplotlib   (optional, for any future plotting extensions)
```

Install:
```bash
pip install numpy scipy matplotlib
```

---

## Quick Start

Run the full simulation suite and generate the report:

```bash
python report.py
```

Output: `OAM-VEST_Simulation_Report.md`

Custom output path:

```bash
python report.py --output /path/to/report.md
```

---

## Module Reference

### `physics.py`

Core acoustic physics constants and functions.

**Constants:**

| Name | Value | Description |
|---|---|---|
| `C_SOUND` | 343.0 m/s | Speed of sound in air at 20°C |
| `RHO_AIR` | 1.21 kg/m³ | Air density |
| `P_REF` | 20×10⁻⁶ Pa | Acoustic reference pressure (0 dB SPL) |
| `BETA_AIR` | 1.2 | Air nonlinearity parameter |

**Key functions:**

```python
spl_to_pa(spl_db)                       # dB SPL → Pascals
pa_to_spl(pressure_pa)                  # Pascals → dB SPL
spl_at_range(spl0, freq_hz, range_m)    # SPL at range (geometric + atmospheric)
required_source_spl(target, freq, r)    # Inverse: what source SPL hits target at r?
max_range_for_effect(spl0, freq, effect)# Max range for 'pain', 'disorientation', etc.
shock_formation_distance(spl0, freq)    # Rankine-Hugoniot shock distance (m)
classify_effect(spl_db)                 # Returns effect string for given SPL
effect_with_earplug(spl_db, bone_conducted=False)  # Effect after earplug attenuation
```

**Biological thresholds (`THRESHOLD` dict):**

| Key | dB SPL |
|---|---|
| `annoyance` | 85 |
| `disorientation` | 115 |
| `pain` | 130 |
| `incapacitation` | 147 |
| `eardrum_rupture` | 160 |
| `cardiac_stress` | 170 |
| `lung_rupture` | 185 |

---

### `acoustic_array.py`

Phased array geometry, gain, beam steering, and OAM phase computation.

**`Ring` dataclass:**

```python
ring = Ring(n_elements=200, radius_m=0.6, label="outer", primary_mode="deterrence")
positions = ring.element_positions()   # (N, 3) array of (x, y, z) in metres
```

**`ArrayPanel` class:**

```python
panel = ArrayPanel(freq_hz=3000.0, spl_per_elem=108.0)

panel.n_elements            # total elements across all rings
panel.source_spl()          # on-axis SPL at 1m (dB)
panel.on_axis_gain_db()     # array gain: 20*log10(N)
panel.beam_half_angle_deg() # approximate 3dB beam half-angle

# Phase computation
phases = panel.focus_phases(focus_point)          # focus at 3D point (m)
phases = panel.oam_phases(topological_charge=1)   # OAM vortex, ring 1
phases = panel.steering_phases(az_deg, el_deg)    # far-field steering
phases = panel.null_steering_phases(null_pt, base_phases)  # add holographic null

# Multi-target superposition
combined, penalty_db = panel.superpose_targets([phases1, phases2, phases3])
```

**`DualPanelArray` class:**

```python
dual = DualPanelArray(panel_sep_m=0.5, freq_hz=3000.0)
dual.source_spl()           # 173.2 dB combined
dual.coherent_gain_db()     # 11 dB
phases_l, phases_r = dual.focus_phases(focus_point)
```

**OAM analysis functions:**

```python
oam_canal_stimulus(mod_freq_hz, topological_charge)  # rad/s to semicircular canal
oam_nystagmus_margin(mod_freq_hz, l)                 # ratio to nystagmus threshold
```

**Default ring configuration (512 elements per panel):**

| Ring | Elements | Radius | Mode |
|---|---|---|---|
| 1 (outer) | 200 | 600 mm | Deterrence (l=0) |
| 2 | 152 | 500 mm | OAM vortex (l=1) |
| 3 | 100 | 350 mm | AM vestibular |
| 4 (inner) | 60 | 150 mm | Parametric / null steering |

---

### `pulse.py`

Pulsed operation, biological accumulation models, power system sizing.

**`PulseRegime` dataclass:**

```python
regime = PulseRegime(prf_hz=2.0, pulse_width_s=0.1, peak_spl_db=173.0)

regime.duty_cycle             # 0.20
regime.time_averaged_spl_db   # 166.0 dB
regime.off_time_s             # 0.4 s
regime.spl_at_range_peak(freq, r)  # peak SPL at range during pulse
regime.spl_at_range_avg(freq, r)   # time-averaged SPL at range
```

**`CochlearFatigueModel` — NIOSH dose accumulation:**

```python
model = CochlearFatigueModel()
model.step(spl_db, dt_s, is_pulse_on)   # advance model
model.dose_percent   # cumulative NIOSH dose (>100% = damage)
model.is_safe        # True while dose < 100%
```

**Cochlear simulation:**

```python
result = simulate_cochlear_dose(regime, freq_hz=3000, range_m=20, duration_s=60)
# result["time_s"], result["dose_percent"], result["max_dose"], result["safe_at_end"]
```

**`VestibularIntegrationModel` — cupula dynamics:**

```python
model = VestibularIntegrationModel()
model.step(stimulus_rad_per_s, dt_s, is_pulse_on)
model.nystagmus_active   # True above 13% saturation deflection
model.disorientation_level  # "NONE", "ONSET", "MODERATE", "SEVERE"
```

**Vestibular simulation:**

```python
result = simulate_vestibular(regime, oam_stimulus_rad_s=12.6, duration_s=30)
# result["nystagmus_onset_s"] — seconds until nystagmus induced
```

**`PowerSystem` validation:**

```python
power = PowerSystem()
pv = power.validate(regime)
# pv["supercap_adequate"], pv["recharge_adequate"], pv["vehicle_supply_ok"]
```

**`LiDARInterleave` timing:**

```python
lidar = LiDARInterleave(regime)
lidar.lidar_reads_per_period    # reads available in off-window
lidar.phase_update_latency_s    # total beam update latency
lidar.max_target_velocity_ms    # max trackable target velocity (m/s)
lidar.timing_summary()          # dict of all timing parameters
```

**`DwellTimer` safety enforcement:**

```python
timer = DwellTimer(max_dwell_s=5.0, cooldown_s=3.0)
permitted = timer.step(dt_s, beam_active)  # returns False when limit hit
```

---

### `wavefield.py`

2D Finite-Difference Time-Domain acoustic pressure solver.

Models the x-z plane cross-section (principal plane). First-order Mur absorbing boundaries. Suitable for beam pattern verification and OAM phase topology visualisation.

```python
from wavefield import FDTD2D, build_linear_array_fdtd, oam_phase_map

# Build and run a linear array simulation
sim = build_linear_array_fdtd(
    n_elements=32,
    spacing_m=0.057,
    freq_hz=3000.0,
    spl_per_elem=108.0,
    domain_z_m=50.0,
)
sim.run(n_periods=20.0)

# Extract results
spl_field = sim.spl_field         # (Nx, Nz) SPL array in dB
x_axis    = sim.x_axis            # physical x coordinates (m)
z_axis    = sim.z_axis            # physical z coordinates (m)
x, spl_at_10m = sim.beam_pattern(z_m=10.0)   # transverse cut at 10m
z, axial_spl  = sim.axial_profile(x_m=0.0)   # on-axis profile

# OAM phase map for visualisation
phases = oam_phase_map(n_elements=152, topological_charge=1)
```

**Stability requirement:** `dx < λ/8`. At 3 kHz (λ = 114 mm): `dx < 14 mm`. Default uses `dx = λ/10`.

**Note:** Full 3D FDTD is computationally expensive and not included. The 2D simulation provides accurate far-field beam patterns in the principal plane. Safety zone calculations are validated analytically in `safety.py` using the verified propagation model.

---

### `safety.py`

Safety analysis, engagement envelope, and interlock simulation.

```python
from safety import (lethality_margins, engagement_envelope, effect_matrix,
                    thermal_analysis_table, shock_analysis_table,
                    multi_target_budget, simulate_interlock_scenario,
                    full_safety_report)

# Lethality margins at key ranges
margins = lethality_margins(source_spl=173.0, freq_hz=3000.0)
# List of dicts: threshold, crossover_range_m, margin_Xm for all ranges

# Engagement envelope
env = engagement_envelope()
# {"disorientation": {"max_range_m": 410, "cone_area_m2": 44000}, ...}

# Full effect matrix (unprotected, earplugged, Mode B bone-conducted)
matrix = effect_matrix()

# Multi-target power budget at 20m
budget = multi_target_budget()

# Simulate advancing target engagement with interlocks
scenario = simulate_interlock_scenario(n_seconds=30, target_profile="advancing")
# scenario["time_s"], scenario["range_m"], scenario["spl_db"], scenario["beam_active"]

# Full consolidated report
report = full_safety_report()  # runs all sub-analyses, returns dict
```

---

## Physical Models

### Propagation

```
SPL(r) = SPL₀ − 20·log₁₀(r) − α(f)·r
```

Atmospheric absorption `α(f)` from ISO 9613-1. Inverse-square spreading dominates below 200 m at 3 kHz.

### Array gain

```
G = 20·log₁₀(N)  dB  (on-axis, coherent)
```

Dual panel coherent combination: +6 dB power sum + 5 dB phase coherence = +11 dB.
Total combined: 162.2 + 11 = **173.2 dB**.

### OAM beam phase winding

```
φₙ = 2π·l·n/N   for element n of N, topological charge l
```

Angular velocity stimulus to semicircular canal: `ω = 2π·f_mod·l` rad/s.
Design point (l=1, 2 Hz): **12.6 rad/s = 6.3× nystagmus threshold**.

### Shock formation (Rankine-Hugoniot)

```
x_shock = ρ·c³ / (β·ω·P₀)
```

At 173 dB, 500 Hz: x_shock = 0.05 m (instantaneous nonlinear regime at source).

### Cochlear fatigue (NIOSH equal energy)

```
D = Σ(tᵢ / Tᵢ)   D > 1.0 → damage threshold
```

Recovery: exponential decay, τ = 300 s. Pulsed operation keeps D well below 1.0 at all operational ranges.

### Cupula dynamics (first-order)

```
d(x)/dt = (stimulus/x_sat - x) / τ_cupula
```

τ_cupula = 10 s. Nystagmus at x > 0.13 (normalised). Design achieves SEVERE disorientation (x > 0.8) within 30 s continuous exposure.

---

## Design Verification Results

Running `python report.py` verifies all design requirements. Key numbers:

| Metric | Target | Achieved |
|---|---|---|
| Combined source SPL | ≥173 dB | 173.2 dB |
| Disorientation range | ≥400 m | 410 m |
| Incapacitation range | — | 19.3 m |
| OAM nystagmus margin | ≥3× | 6.3× |
| Average power (pulsed) | ≤15 kW | 10.2 kW |
| Lung rupture margin @ 100m | ≥40 dB | +53 dB |
| Eardrum rupture crossover | <5 m | 4.5 m |
| Thermal hazard (3kHz, 5s) | None | ΔT < 0.001°C |

---

## Extending the Package

**Add a new propagation environment (rain, humidity):**
Modify `alpha_db_per_m()` in `physics.py` — replace ISO 9613-1 values with environment-specific coefficients.

**Change operating frequency:**
Construct `ArrayPanel(freq_hz=2500.0)` and adjust element spacing to `C_SOUND / (2 * freq_hz)` for λ/2 spacing.

**Add metamaterial lens gain:**
In `acoustic_array.py`, add `lens_gain_db` parameter to `ArrayPanel.source_spl()` — passive gain of 8–10 dB from transfer matrix model.

**3D FDTD:**
Extend `FDTD2D` to `FDTD3D` — requires 3D pressure and velocity field arrays. Memory scales as O(Nx·Ny·Nz); expect ~4 GB for 100 m domain at λ/10 resolution at 3 kHz.

**Custom target tracking:**
Subclass `DwellTimer` and `LiDARInterleave` in `pulse.py` to add track-while-scan or Kalman filter target state estimation.

---

## Safety Notes

This simulation package models a non-lethal weapon system. All results should be validated against empirical measurements before hardware construction. The safety margins computed here assume:

- Ideal free-field propagation (no reflections, no ground effect)
- Standard atmosphere (20°C, 50% RH)
- Target is a standing adult human in the beam axis
- All safety interlocks are functioning correctly

Do not reduce minimum engagement range below 15 m without formal re-analysis. Do not disable LiDAR interlock or dwell timer under any operational circumstances.

Formal Article 36 legal review (Geneva Convention Additional Protocol I) is required before acquisition by any state party.

---

*OAM-VEST Simulation Package — Odin Loch — odin.loch@outlook.com.au*
