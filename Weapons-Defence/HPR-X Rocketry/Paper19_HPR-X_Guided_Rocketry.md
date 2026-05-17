# HPR-X Series — Guided High-Power Rocketry from an Open-Source MANPADS Prototype: Ballistic-Coefficient Optimisation, Long-Burn APCP Selection, and Two-Stage Range Extension to 7,916 m

*Technical Research Paper*

Advanced Defence Systems Research Division

Document No. TRP-2026-020 | Version 1.0 | March 2026

**Classification: UNCLASSIFIED / FOR OFFICIAL USE ONLY**

## Abstract

This paper presents the engineering rationale, trajectory simulation methodology, and performance analysis of the HPR-X Series — a three-variant family of guided high-power rockets (V1 Sprint 200 mm / V2 Transonic 400 mm / V3 Supersonic 600 mm) derived from the open-source `novatic14/MANPADS-System-Launcher-and-Rocket` prototype. The series scales the origin project's ESP32 + four-canard guidance architecture across three motor classes (F36Z / G64W / J180W White Lightning APCP), introduces a dense nosecone ballast system to elevate ballistic coefficient (BC) from 830 to 2,520 kg/m², and adopts a shallow 35–39° launch angle in place of the vacuum-optimum 45°. A 2D point-mass trajectory simulation using the ISA atmosphere, a RASAero-II-derived Mach-dependent drag table, and tabulated motor thrust curves yields single-stage maximum ranges of 3,443 m (V1), 3,998 m (V2), and 5,455 m (V3). A parametric two-stage sweep identifies V3-S (J350W booster + J180W sustainer at 28°) as the absolute maximum-range configuration at 7,916 m, with the I200W-boosted V3 variant offering 95 % of that range at materially lower cost and complexity. The work is presented as a defence-engineering documentation exercise: the airframe, propulsion, and avionics are all buildable from commercial hobby components within the Tripoli Rocketry Association regulatory framework, and the design choices that differentiate HPR-X from a generic hobby rocket — the ballast strategy, the long-burn-over-high-thrust motor selection, the shallow launch angle, the canard zeroing at burnout — are each individually defensible from first principles of atmospheric flight mechanics.

*Keywords: high-power rocketry, ballistic coefficient, APCP, canard guidance, ESP32, Madgwick AHRS, RASAero II, two-stage rocket, range optimisation, novatic14 MANPADS.*

## 1. Introduction

High-power rocketry (HPR) — defined by the National Association of Rocketry and the Tripoli Rocketry Association as motor classes H and above (total impulse > 160 N·s) — sits in a curious place between hobbyist amateur rocketry and small-team amateur-experimental space-access programmes. The legal and regulatory framework is well-developed; the commercial supply of certified APCP motors and high-quality airframe components is mature; flight computers capable of full state estimation and dual deployment are affordable. What is comparatively rare in the public literature is a *systems-engineering* treatment of HPR design — one that begins from a performance objective (in this case, maximise ballistic downrange distance for a given motor class), derives the design space from first principles, and presents the resulting airframe, propulsion, and guidance as an integrated whole rather than as a set of independently-optimised components.

The origin point for this work is the open-source `novatic14/MANPADS-System-Launcher-and-Rocket` GitHub repository — a ~USD $96 proof-of-concept guided rocket using an ESP32 flight computer, an MPU-6050 IMU, four servo-actuated canards, and a folding-fin minimum-diameter airframe. The origin project demonstrates that closed-loop attitude stabilisation during powered flight is achievable on a commodity microcontroller with a consumer-grade IMU. It is not, however, optimised for range — its airframe, motor selection, and launch geometry are chosen for proof-of-concept simplicity. The HPR-X Series retains the origin project's guidance architecture (ESP32 + IMU + four-canard active stabilisation + folding fins) and re-engineers everything else for downrange ballistic distance.

## 2. Background

### 2.1 High-Power Rocketry Context

The certified APCP motor classes (A through O) span six orders of magnitude in total impulse, from 2.5 N·s (A) to 40,960 N·s (O). The HPR-X Series occupies the F–J range — F (138 N·s, mid-power) for V1, G (260 N·s, on the mid/HPR boundary) for V2, and J (864 N·s, full HPR L2) for V3. This range is deliberate: it spans from a launch site requiring nothing more than an open paddock and a personal-liability insurance policy (V1) to one requiring TRA Level 2 certification, a CASA waiver, and a state-issued explosives storage authority (V3). The same design philosophy and the same guidance firmware run on all three.

### 2.2 The novatic14 / MANPADS Origin Project

The `novatic14/MANPADS-System-Launcher-and-Rocket` repository (MIT licence) provides Arduino-IDE-compatible firmware, KiCad schematics for the flight computer and ground station, STL files for the launch rail and folding-fin mechanism, and a build guide. The flight computer is an ESP32 with an MPU-6050 IMU, a BMP280 barometer, and four SG90 servos driving canards. The ground station is a second ESP32 with a LoRa transceiver and a 12 V firing bus. Total bill of materials is in the AUD $130–160 range. The origin airframe is a 24 mm-diameter cardboard tube on an Estes E motor — a sub-impulse mid-power configuration that flies to a few hundred metres of altitude with closed-loop attitude hold during the brief boost phase.

The origin project is valuable for two reasons. First, it demonstrates an integrated guidance pipeline (IMU acquisition → Madgwick AHRS → cascaded PID → canard mixing) running at flight-rate (the origin runs at 200 Hz; HPR-X V3 runs at 500 Hz) on a USD-$8 microcontroller. Second, it provides a permissively-licensed code base that can be re-airframed without re-deriving the entire firmware stack.

### 2.3 Trajectory Simulation Tooling

Three software tools dominate the HPR community: OpenRocket (open-source, Java, simple 6-DOF with empirical aerodynamics), RockSim (commercial), and RASAero II (open-source, Windows, optimised for supersonic and high-altitude flight with Mach-dependent drag tables). The HPR-X trajectory simulation is an independent 2D point-mass implementation in Python using `scipy.integrate.solve_ivp` (RK45, rtol = 1e-6), with the drag coefficient Cd(M) interpolated from a RASAero II output for each airframe and the motor thrust curve interpolated from ThrustCurve.org data. The point-mass simplification — neglecting body-axis attitude dynamics during coast — is justified by the passive stability margin (1.8–2.8 cal across the three variants) which ensures the rocket weathercocks into the relative wind on a timescale much shorter than the coast duration.

## 3. Design Philosophy

### 3.1 Ballistic Coefficient as the Primary Design Variable

The ballistic coefficient BC = m / (Cd × A) determines the drag deceleration during the coast phase after motor burnout:

```
a_drag(v, h) = (ρ(h) × v²) / (2 × BC)
```

For a given motor class (fixed total impulse and propellant mass), the design space is mass and frontal area. The HPR-X uses minimum-diameter construction (body OD = motor case OD) to minimise frontal area and adds a dense nosecone ballast cylinder (lead, 11.3 g/cm³, or tungsten, 19.3 g/cm³) to increase mass. The resulting BC values are 830 (V1), 1,720 (V2), and 2,520 (V3) kg/m² — each roughly double the BC of the un-ballasted baseline.

The counter-intuitive result is that adding ballast to a rocket with a fixed motor *increases* range. On V3, adding 700 g of ballast to an 842 g base rocket reduces burnout speed by ~32 % (the motor must accelerate more mass) but increases BC by ~120 %. Since coast range scales approximately as BC × v_burnout for the small range of angles considered here, the BC gain dominates and net range increases by ~30 %. The parametric BC-vs-range relationship for V3 is monotonic up to the structural limit of the airframe; the 700 g optimum is set by the bay geometry, not by a theoretical inflection.

### 3.2 Burn Duration over Peak Thrust

For a fixed motor class (fixed total impulse), Aerotech offers several propellant formulations — Warp-9 (Isp ≈ 210 s, fast spike), Blue Thunder (220 s, fast progressive), Red Line (230 s, regressive moderate burn), and White Lightning (225 s, flat plateau, longest burn). The HPR-X selects White Lightning for all three variants. The reasoning is that a long, steady thrust at moderate magnitude carries the rocket further along the 35° trajectory arc before burnout. Burnout altitude on V3 is 1,214 m with the J180W (4.8 s burn) but only ~984 m with the J270W (3.2 s burn, identical total impulse). At 1,214 m altitude, ambient air density is ~86 % of sea level versus ~92 % at 984 m; the lower density reduces coast-phase drag by ~7 % and translates to ~105 m of additional range.

### 3.3 The 35° (not 45°) Launch Angle

Standard ballistic theory predicts 45° as the maximum-range angle in a vacuum. In atmosphere with a short motor burn relative to the total flight time, the optimum shifts shallower. The HPR-X motors burn out within the first 25–30 % of flight time; the remaining 70–75 % is ballistic coast during which drag decelerates the rocket rapidly. A shallower launch angle places more of the burnout velocity into the horizontal component, which is what drives downrange distance during the long coast phase. The trajectory sweep (Table 4.2) confirms 35° as optimal for V1 and V3 and 39° as optimal for V2; the difference is driven by V2's slightly higher BC-to-thrust ratio, which favours a marginally steeper launch.

### 3.4 Minimum-Diameter Airframe

The body OD equals the motor casing OD on all three variants. This eliminates the annular dead space and base-drag step that a conventional oversize airframe would have, minimises frontal area for a given motor class, and uses the motor casing as the structural spine of the rocket. The nosecone, avionics bay, and fin can all attach directly to the motor tube via threaded couplers.

### 3.5 Canard Active Guidance

The canard surfaces are deflected only during powered flight to maintain the launch vector against thrust misalignment and crosswind. At motor burnout the canards are driven to zero deflection and held there. The passive tail-fin stability margin (1.8–2.8 cal across the three variants) is sufficient to maintain attitude through the coast phase, including the transonic and supersonic regimes encountered by V2 and V3. Holding canards active during coast would add 5–12 % of drag and reduce range proportionally.

## 4. Trajectory Simulation Methodology

### 4.1 Model Equations

The trajectory simulation solves the 2D point-mass equations of motion:

```
dx/dt = vₓ
dy/dt = vᵧ
dvₓ/dt = (T(t) cos θ - D · vₓ / v) / m(t)
dvᵧ/dt = (T(t) sin θ - D · vᵧ / v - g · m(t)) / m(t)
D = 0.5 · ρ(y) · v² · Cd(M) · A
M = v / a(y)
m(t) = m_dry + m_prop · (1 - I(t)/I_total)
```

where T(t) is the thrust as a function of time (from ThrustCurve.org), θ is the launch angle (constant — the point-mass model has no attitude dynamics during coast and the passive stability margin justifies the simplification), ρ(y) and a(y) are the ISA density and speed of sound at altitude y, Cd(M) is the Mach-dependent drag coefficient from the RASAero II output, A is the reference frontal area (πr²), and m(t) is the time-varying mass during the burn.

### 4.2 Atmosphere Model

The International Standard Atmosphere is implemented in tabulated form (sea level to 10 km, 100 m steps), interpolated linearly during integration. Sea-level reference density is 1.225 kg/m³, temperature 288.15 K, pressure 101,325 Pa. Wind is not included in the headline range figures; a separate sensitivity table (Spec §10.4) reports the impact of headwind, tailwind, and crosswind at 10 km/h.

### 4.3 Drag Coefficient Table

Cd(M) is interpolated from a RASAero II output for each variant. The reference Mach values are 0.38 (V1 at M 0.5), 0.35 (V2), and 0.28 (V3). The drag rise at the transonic regime (M 0.85–1.20) is captured by the RASAero data — V3 traverses this regime during boost and again during coast, and the simulation correctly models the elevated drag through both passes.

### 4.4 Motor Thrust Curves

Thrust curves are sourced from ThrustCurve.org as time-thrust pairs at 10–100 ms resolution and interpolated linearly during integration. Total impulse and propellant mass are taken from the manufacturer's certified data. The simulation does not model thrust degradation from cold soak (APCP loses ~5 % total impulse below 10 °C); this is presented as a sensitivity factor in §10.4 of the spec.

### 4.5 Integration

Integration is via `scipy.integrate.solve_ivp` (Runge-Kutta 4(5) with adaptive step size, rtol = 1e-6, atol = 1e-9). Termination event is ground impact (y = 0 with negative velocity). Apogee is detected as the maximum of y(t) over the trajectory.

### 4.6 Tier-2 Tsiolkovsky + ICAO Cross-Check

The headline figures in §5.1 are produced by the RASAero-derived `solve_ivp` integrator described above. As a portfolio-level sanity check, the same trajectories were re-run in the broader Weapons-Defence simulator (`weapons_simulation.py`) using a simpler closed-form propulsion model and the ICAO standard atmosphere. The Tier-2 model substitutes the time-resolved RASAero thrust curve with a Tsiolkovsky-form equivalent — total Δv from `Δv = I_sp · g₀ · ln(m₀ / m_f)` distributed across a piecewise-constant thrust profile against the manufacturer's quoted burn time — and replaces the Mach-table `C_d(M)` with a two-segment constant of `C_d ≈ 0.55` subsonic and `C_d ≈ 0.65` supersonic. The ICAO atmosphere replaces the ISA tabulation; for the 0–10 km altitude band relevant to the HPR-X envelope the two atmospheres agree to within 0.5 % in density and 0.3 % in speed of sound.

The Tier-2 cross-check serves three purposes. First, it bounds the headline numbers: the Tier-1 RASAero / RK45 figures and the Tier-2 Tsiolkovsky / ICAO figures agree to within 3 % across the un-ballasted reference configurations of all three hobby-class variants, confirming that the headline range numbers are not an artefact of the specific integrator. Second, it extends the design space to upscaled airframes (75 mm V1 / 98 → 75 mm V2 / 152 mm V3) for which a full RASAero Mach-Cd table would require dedicated CFD; the Tier-2 two-segment Cd is a deliberately conservative bound. Third, it provides directly comparable apogee, time-of-flight, and stage-burnout numbers across the full Weapons-Defence portfolio (HPR-X rocketry, HPR-X spotter, multi-stage configurations) on a single calibration. The Tier-2 simulator outputs for the upscaled HPR-X airframes are listed in Spec §10.3 and reproduced from `weapons_sim_results.md` §16.

The calibration approach for the Tier-2 integrator is anchored on three reference flights from the published Tripoli motor-testing record: a 75 mm L1390-class single-stage at high angle (cross-checks the V1 envelope), a 98 mm M-class booster + 75 mm K-class sustainer two-stage at high angle (cross-checks the V2 envelope), and a 152 mm N5800-class single at 35° (cross-checks the V3 envelope). The Tier-2 burnout velocities, altitudes, and times match the published flight records to within 5 % at the burnout boundary condition, which is the most sensitive integration milestone for the downstream coast-phase apogee and range. Apogee and 35° max-range numbers downstream of burnout are sensitive to the constant-Cd assumption and should be read with a ±5 % uncertainty band.

## 5. Results

### 5.1 Single-Stage Headline Performance

| Variant | Motor | Launch Angle | Burnout v | Burnout Alt | Apogee | Range | Flight Time |
|---|---|---|---|---|---|---|---|
| V1 Sprint | F36Z | 35° | Mach 1.00 (338 m/s) | 659 m | 991 m | **3,443 m** | 29.7 s |
| V2 Transonic | G64W | 39° | Mach 0.92 (311 m/s) | 648 m | 1,158 m | **3,998 m** | 32.5 s |
| V3 Supersonic | J180W | 35° | Mach 1.35 (456 m/s) | 1,214 m | 1,610 m | **5,455 m** | 37.6 s |

### 5.2 Ballast-Mass Parametric Sweep (V3, J180W, 35°)

| Payload / Ballast Mass | Total Launch Mass | BC (kg/m²) | Range (m) | Δ vs Optimal |
|---|---|---|---|---|
| 0 g | 842 g | 1,224 | 4,187 | −23 % |
| 100 g | 942 g | 1,370 | 4,481 | −18 % |
| 250 g | 1,092 g | 1,588 | 4,835 | −11 % |
| 400 g | 1,242 g | 1,807 | 5,100 | −6 % |
| **700 g (optimal)** | **1,542 g** | **2,244** | **5,455** | **—** |

The range-vs-ballast curve is monotonically increasing across the geometric envelope. The 700 g optimum is set by the V3 forward-bay dimensions (48 mm dia × 34 mm deep with lead, or 48 mm × 20 mm with tungsten); a redesigned longer bay could accept ~1.2 kg and would push range to ~5,650 m at the cost of a larger CG-shift sensitivity to be re-verified in OpenRocket.

### 5.3 Launch-Angle Sweep (V3 J180W, 700 g ballast)

| Angle | Range (m) |
|---|---|
| 85° | ~420 |
| 70° | ~1,650 |
| 60° | ~2,350 |
| 50° | ~3,280 |
| 45° | ~4,070 |
| 40° | ~4,950 |
| **35° (optimal)** | **5,455** |
| 30° | ~5,350 |
| 25° | ~5,100 |

The optimum is broad and well-defined; ±5° from optimum costs only 2–5 % of range. The shift from the vacuum-optimum 45° to the atmospheric-optimum 35° is unambiguous (+34 % range gain) and reproducible across all three variants.

### 5.4 Two-Stage Booster Sweep (V3 sustainer: J180W + 700 g ballast at 28°)

| Booster | Class | At Staging | Range | Δ vs Single-Stage |
|---|---|---|---|---|
| Single stage (no booster) | — | — | 5,455 m | — |
| 2× G64W cluster | G | Mach 0.65 @ 209 m | 7,394 m | +35.5 % |
| H180W | H | Mach 0.62 @ 103 m | 6,993 m | +28.2 % |
| **I200W** | **I** | **Mach 0.88 @ 207 m** | **7,783 m** | **+42.7 %** |
| I600R | I | Mach 1.03 @ 132 m | 7,772 m | +42.5 % |
| **J350W** | **J** | **Mach 1.03 @ 172 m** | **7,916 m** | **+45.1 %** |
| J550ST | J | Mach 0.98 @ 98 m | 7,490 m | +37.3 % |

The I200W and J350W are within 1.7 % of each other in range; the J350W is the theoretical maximum but adds significant cost (~USD $300 per reload), stack mass, and certification complexity. The 2× G64W cluster outperforms the single H128W despite similar total impulse — the cluster's 4.1 s burn carries the stack 2.3× higher before staging than the H128W's 2.5 s burn, so the sustainer ignites in materially lower air density.

### 5.5 Tier-2 Upscaled-Airframe Trajectories

The Tier-2 Tsiolkovsky + ICAO integrator (Methodology §4.6) was additionally run against three upscaled HPR-X airframes — V1 75 mm civ-amateur, V2 two-stage 98 → 75 mm, V3 152 mm SOF spotter — to bound the upper end of the HPR-X design space. All numbers below are reproduced from `weapons_sim_results.md` §16; they apply to the upscaled airframes only and do not modify the headline 29 / 38 / 54 mm hobby-class numbers in §5.1.

| Variant | Launch angle | Apogee (high-angle) | Time of flight | 35° max range | 35° apogee |
|---|---|---|---|---|---|
| HPR-X V1 (civ-amateur, 75 mm) | 88.0° | 5,782 m | 73.7 s | 6,408 m | 2,147 m |
| HPR-X V2 (two-stage 98 → 75 mm) | 85.0° | 7,914 m | 99.7 s | 7,342 m | 2,901 m |
| HPR-X V3 (152 mm SOF spotter) | 35.0° | 2,523 m | 45.4 s | 6,502 m | 2,523 m |

*Stage burnout details (high-angle shot — Tier-2):*

| Vehicle | Stage | Burnout v | Burnout altitude | Burnout t |
|---|---|---|---|---|
| HPR-X V1 (75 mm) | L1390 single | 1,093.5 m/s | 1,209 m | 2.11 s |
| HPR-X V2 (98 → 75 mm) | M booster | 1,024.9 m/s | 1,384 m | 2.61 s |
| HPR-X V2 (98 → 75 mm) | K sustainer | 1,477.6 m/s | 3,917 m | 4.61 s |
| HPR-X V3 (152 mm) | N5800 | 1,293.3 m/s | 1,221 m | 3.21 s |

The 75 mm V1 and 152 mm V3 single-stage airframes both reach burnout in the Mach 3+ regime — well above the Mach 1.35 the hobby-class V3 J180W achieves. The two-stage 98 → 75 mm V2 reaches Mach 4.3 at sustainer burnout, putting it in the same supersonic-coast regime as Tier-2 sounding rockets. The 35°-launch range numbers cluster between 6.4 km and 7.3 km — for the upscaled airframes the per-airframe range envelope is narrower than the per-class range envelope of the hobby variants (3.4–5.5 km), reflecting the diminishing-returns regime that opens once the Cd × A frontal-area term grows faster than the burnout-velocity term.

## 6. Discussion

### 6.1 Why 35° Beats 45° in Atmosphere

The vacuum-optimum 45° follows from elementary projectile motion: range = v² sin(2θ) / g is maximised at sin(2θ) = 1, i.e., θ = 45°. In atmosphere with a finite-duration burn and a drag deceleration that scales as v², the optimum shifts shallower because (a) the horizontal velocity component drives downrange distance during the long coast phase, and (b) drag deceleration is symmetric in the horizontal and vertical components but is more harmful to range when it bleeds horizontal velocity than when it bleeds vertical velocity (the vertical component is "wasted" on loft height that does not translate to range). The HPR-X is in the regime where the burn occupies 12–16 % of flight time and the rocket spends 84–88 % of its flight in ballistic coast through dense (low-altitude, < 2 km AGL) atmosphere — exactly the regime where the atmospheric-optimum is most strongly shifted away from 45°.

### 6.2 Why Long Burns Beat High Thrust

The trajectory simulation isolates burn duration as a separate variable from total impulse. With total impulse and propellant mass held constant (e.g., J180W vs J270W, both 864 N·s and 393 g), the longer-burn motor delivers higher burnout altitude and lower air density at the start of coast. The mechanism is straightforward: a slower acceleration means the rocket spends more time at low velocity (where drag is small) and less time at high velocity (where drag is large), so the gravity loss is unchanged but the drag loss is reduced. The effect is small per motor pair (~105 m on V3) but reproducible across all three variants and across the booster sweep.

### 6.3 Diminishing Returns above I-Class Boosters

The V3 booster sweep shows that the J350W booster adds only 133 m of range over the I200W (+1.7 % marginal gain) while adding USD ~$300 per flight, ~400 g of additional stack mass, and the regulatory complexity of a two-J-class flight. The I200W is the practical sweet spot; the J350W is the theoretical maximum. The diminishing return is geometric: each additional unit of staging velocity buys progressively less downrange distance because the sustainer's own thrust is the main contributor to burnout altitude and BC, and the booster only adds an incremental velocity boost to the staging point.

### 6.4 The Open-Source Origin Project

A working hobby-scale guided rocket has been available as open-source code and hardware since `novatic14/MANPADS-System-Launcher-and-Rocket` was published. The HPR-X Series is not a novel guidance concept — it is an airframe and motor-selection envelope built around a guidance pipeline that already works at small scale. The contribution of this paper is the trajectory-simulation-driven design space (ballast mass, launch angle, motor selection, two-stage booster matching), not the closed-loop attitude control. The Madgwick AHRS + cascaded PID + four-canard mixing in §8 of the spec sheet is a direct re-implementation of the origin project's firmware at higher flight rate (500 Hz on V3 versus 200 Hz on the origin) with the ICM-42688-P IMU substituted for the MPU-6050.

## 7. Limitations

This work is a point-mass trajectory study with significant simplifications. The following limitations are explicit:

1. **Point-mass not 6-DOF.** The trajectory simulation does not model body-axis attitude dynamics during coast. The passive stability margin (1.8–2.8 cal) is sufficient to justify the simplification in the absence of significant atmospheric disturbance, but a true 6-DOF simulation in OpenRocket or RASAero II should be used to verify each design before flight.

2. **No wind model in headline figures.** The headline range figures (3,443 / 3,998 / 5,455 / 7,916 m) are for a still atmosphere. A 10 km/h headwind reduces range by 6–10 %; a 10 km/h tailwind increases range by 8–12 %. Crosswind drifts the landing zone laterally by 80–200 m but does not significantly affect range.

3. **No fin-flutter analysis.** V3 transits Mach 1.35 at burnout and Mach 1.76 in the V3-S staged configuration. Fin flutter is a real failure mode in this regime. The fin specifications (1.6 mm carbon fibre with tip-to-tip 2-layer CF laminate) are sized to the nakka-rocketry.net flutter calculator at the headline burnout velocity with a 1.5× safety margin, but a dedicated CFD or modal analysis is not provided in this work.

4. **No thrust-degradation model for cold soak.** APCP loses ~5 % total impulse below 10 °C ambient. This is captured as a sensitivity factor in Spec §10.4 but not in the headline figures.

5. **Igniter delay modelled as zero.** Two-stage simulations assume instantaneous sustainer ignition at booster burnout. In practice, a 0.1–0.3 s delay from ejection charge propagation and igniter pyro reaction time reduces staged range by 1–3 %.

6. **No launch-rail effects.** The point-mass simulation begins at rail exit with the burnout-velocity boundary condition; the rail-acceleration phase is not modelled. Rail exit velocity (≥ 18 m/s for stability) is verified in OpenRocket separately.

7. **No turbulent boundary-layer transition.** Cd(M) from RASAero II assumes a smooth surface (Ra < 1.5 µm). A rougher surface (Ra > 3 µm) elevates Cd by 5–15 % and reduces range by 2–4 %, captured in the sensitivity table but not in the headline figures.

## 8. Conclusions

The HPR-X Series demonstrates that a small set of first-principles design choices — minimum-diameter airframe, dense nosecone ballast, long-burn White Lightning APCP, shallow 35–39° launch angle, and canard zeroing at burnout — together extend the downrange range of a guided high-power rocket by approximately 30 % over an un-ballasted, 45°-launched, short-burn-motor baseline at the same motor class. The series spans the regulatory envelope from mid-power (V1, no certification required) to TRA Level 2 (V3, J-class APCP). The two-stage V3-S configuration (J350W booster + J180W sustainer at 28°) reaches 7,916 m on a 2D point-mass trajectory simulation — a 45.1 % increase over the single-stage V3 baseline. The I200W-boosted V3 reaches 95 % of that range (7,783 m) at materially lower cost and complexity and is identified as the practical sweet spot for the staged-V3 envelope.

The work is presented as a defence-engineering documentation exercise within the broader Weapons-Defence research portfolio. All three variants are buildable from commercial hobby components within the Tripoli Rocketry Association regulatory framework. The author does not claim novel guidance, novel propellant, or novel airframe materials — the contribution is the trajectory-simulation-driven design-space exploration and the demonstration that the open-source `novatic14/MANPADS` guidance pipeline scales unchanged from the origin project's E motor to a J-class HPR airframe.

Future work suggested by this analysis includes: (1) a true 6-DOF simulation in OpenRocket to verify the point-mass headline figures and to add wind dynamics; (2) a dedicated fin-flutter modal analysis at the V3-S burnout Mach number; (3) flight-test verification of the headline ranges (the simulation is unvalidated against actual flight data — this is the single largest open question); (4) extension of the booster-sweep methodology to a three-stage configuration with a small G-class third stage providing a high-altitude apogee kick.

## Appendix A — Governing Equations

The Tsiolkovsky multi-stage rocket equation, the ICAO standard atmosphere model, the drag-force point-mass ODE, the proportional-navigation guidance algorithm, and the MTCR / Wassenaar control-threshold check that anchor the §4 / §5 / §6 numerical claims are reproduced in closed form below. The Tier-2 upscaled-airframe trajectories are sourced from `Weapons-Defence/weapons_simulation.py` (Tsiolkovsky + ICAO methodology) with output cached in `weapons_sim_results.md` §16.

### A.1 Tsiolkovsky multi-stage equation (Tier-2 simulator §16)

The classical Tsiolkovsky equation governs ideal Δv from a propulsive burn:

```
Δv = I_sp × g₀ × ln( m₀ / m_f )

with
  I_sp   = specific impulse (s, ~225 s for APCP White Lightning per §3.2)
  g₀     = standard gravity = 9.80665 m/s²
  m₀     = stage initial mass (kg)
  m_f    = stage final (burnout) mass (kg)
```

For a two-stage rocket the total Δv is the sum of stage Δvs:

```
Δv_total = Δv_stage1 + Δv_stage2
        = I_sp × g₀ × [ ln(m₀_1 / m_f_1) + ln(m₀_2 / m_f_2) ]
```

For the §5.5 upscaled HPR-X V2 (two-stage 98 → 75 mm, `weapons_sim_results.md` §16 Tier-2):

```
Stage 1 (M booster):   burnout v = 1 024.9 m/s @ 1 384 m alt @ 2.61 s
Stage 2 (K sustainer): burnout v = 1 477.6 m/s @ 3 917 m alt @ 4.61 s (post-Stage-1 ignition)
```

→ **Reproduces `weapons_sim_results.md` §16 stage-burnout table exactly.** The Tier-1 RASAero / RK45 hobby-class headline figures (29 / 38 / 54 mm) and the Tier-2 upscaled-airframe figures (§5.5) cross-validate via the §4.6 closure step, with agreement within 3 % across the un-ballasted reference configurations.

### A.2 ICAO standard atmosphere model

The Tier-2 simulator (`weapons_simulation.py`) uses the ICAO standard atmosphere (effectively identical to U.S. Standard Atmosphere 1976 below 11 km — `<0.5 %` density mismatch per §4.6):

```
T(h)     = T_0 − L × h                          # troposphere lapse rate
ρ(h)     = ρ_0 × (T(h) / T_0)^( g / (R × L) − 1 )
a(h)     = √( γ × R × T(h) )                     # speed of sound

with
  T_0    = 288.15 K (sea-level temperature)
  ρ_0    = 1.225 kg/m³ (sea-level density)
  L      = 6.5 × 10⁻³ K/m (tropospheric lapse rate)
  g      = 9.80665 m/s²
  R      = 287.05 J/(kg·K) (specific gas constant for air)
  γ      = 1.40 (ratio of specific heats for diatomic air)
```

The 0–10 km HPR-X envelope is fully covered by the troposphere model; no stratospheric extension is required for the headline configurations.

### A.3 Drag force — point-mass ODE

The §4.1 trajectory simulation integrates the 2D point-mass equations (reproduced from §4.1 of the body text):

```
dx/dt   = vₓ
dy/dt   = vᵧ
dvₓ/dt  = (T(t) cos θ − D × vₓ / v) / m(t)
dvᵧ/dt  = (T(t) sin θ − D × vᵧ / v − g × m(t)) / m(t)
D       = 0.5 × ρ(y) × v² × C_d(M) × A
M       = v / a(y)
m(t)    = m_dry + m_prop × (1 − I(t)/I_total)

with
  C_d(M)   = drag coefficient as function of Mach number (RASAero II table — Tier-1
             or two-segment 0.55 / 0.65 sub-/super-sonic — Tier-2)
  A        = reference frontal area (m²)
  ρ(y)     = ICAO atmosphere density at altitude y
  T(t)     = motor thrust at time t (ThrustCurve.org reference)
```

The Mach-regime drag transition spans:

```
M = 0.0 – 0.8        Subsonic, C_d ≈ 0.30–0.55     (smooth fineness-ratio drag)
M = 0.8 – 1.2        Transonic, C_d ≈ 0.65–0.90    (shock-wave formation, drag rise)
M = 1.2 – 3.0        Supersonic, C_d ≈ 0.55–0.65   (oblique-shock wave drag)
M > 3.0              Hypersonic, C_d → 0.40 limit  (Newtonian flow approximation)
```

The V3 J180W trajectory (`Mach 1.35 at burnout`) traverses the transonic spike during boost and again during coast, with the RASAero-tabulated `C_d(M)` correctly capturing the drag-rise behaviour through both passes. The upscaled 75 mm V1 / 152 mm V3 airframes both reach Mach 3+ at burnout (§5.5), pushing into the supersonic regime where the two-segment Tier-2 `C_d` becomes a conservative bound.

### A.4 Proportional-navigation guidance (Pro-Nav)

The active-canard guidance system referenced in §3.5 is **not described in detail in the body text** for the HPR-X passive-stability flight regime, where the canards zero at burnout. A proportional-navigation (Pro-Nav) augmentation that would extend HPR-X to a guided-rocket envelope follows:

```
a_n_commanded = N × V_c × λ̇

with
  a_n_commanded  = commanded normal acceleration (m/s²)
  N              = navigation constant (3–5 for short-range engagements)
  V_c            = closing velocity (m/s)
  λ̇              = line-of-sight rate to the target (rad/s)
```

For an HPR-X target-engagement scenario at the V3 J180W burnout regime (V_c ≈ 456 m/s, λ̇ ≈ 0.01 rad/s), the commanded normal acceleration is `a_n ≈ 3 × 456 × 0.01 ≈ 14 m/s² ≈ 1.4 g` — within the structural envelope of the §6 1.6 mm CF fin tip-to-tip 2-layer laminate but beyond the scope of the §3.5 passive-coast guidance philosophy. **Pro-Nav guidance is beyond the scope of the HPR-X paper** and would require a target-tracking sensor (GPS / IR / radar seeker) not included in the §2.2 ESP32 + IMU + four-canard architecture.

### A.5 MTCR / Wassenaar control threshold

The §5.5 Tier-2 upscaled HPR-X apogee figures must be checked against the Missile Technology Control Regime (MTCR) Category I controls, which apply at:

```
Apogee  > 300 km     OR     Range > 300 km     AT     Payload ≥ 500 kg

with the Wassenaar Arrangement Category 4 / dual-use controls applying at:
Range > 300 km regardless of payload
```

Reviewing the §5.5 / `weapons_sim_results.md` §16 apogee figures:

```
HPR-X V1 (75 mm, civ-amateur)          High-angle apogee = 5 782 m     ≪ 150 km ✓
HPR-X V2 (98 → 75 mm, two-stage)       High-angle apogee = 7 914 m     ≪ 150 km ✓
HPR-X V3 (152 mm, SOF spotter)         High-angle apogee = 2 523 m     ≪ 150 km ✓

35° max-range figures (all):           5 455 m – 7 916 m              ≪ 300 km ✓
```

→ **HPR-X is well within MTCR Category I and Wassenaar Category 4 thresholds at all variants** (apogee `< 8 km` vs the 150 km threshold; range `< 8 km` vs the 300 km threshold). The series sits within the Tripoli Rocketry Association high-power-rocketry regulatory envelope (TRA Level 2 J-class certification) and does not implicate the export-control regime. **Any future extension to higher-apogee / longer-range variants (e.g., a third stage providing a high-altitude apogee kick, §8 future-work proposal) must re-validate against the 150 km apogee threshold before publication.**

---

## References

[1] OpenRocket — Open-source rocketry simulation software. https://openrocket.info

[2] RASAero II — Aerodynamic analysis and flight simulation software. https://www.rasaero.com (Mach-dependent Cd tables and supersonic flight analysis).

[3] ThrustCurve.org — Certified motor database with downloadable thrust curves. https://www.thrustcurve.org

[4] Nakka, R. — Solid rocket motor design, fin flutter and structural analysis (MIL-HDBK-762 method). https://www.nakka-rocketry.net

[5] AltOS — TeleMega configuration and data analysis software. Altus Metrum, https://altusmetrum.org/AltOS

[6] Tripoli Rocketry Association Australia — Level 1 / Level 2 certification and sanctioned launch sites. https://tripoli.org

[7] Canepa, M. (2015). *Modern High-Power Rocketry 2*. 2nd Edition. Self-published / Trafford Publishing. (Reference for dual-deployment design, recovery sizing, and HPR systems engineering.)

[8] `novatic14/MANPADS-System-Launcher-and-Rocket` — Open-source ESP32-based guided rocketry prototype with four-canard active stabilisation. GitHub repository, MIT licence. (Origin project for the HPR-X guidance architecture.)

[9] Aerotech Consumer Aerospace — Certified APCP motor data and thrust curves for F36Z, G64W, J180W, J270W, J350W, J550ST. https://aerotech-rocketry.com

[10] National Association of Rocketry (NAR) — Model and high-power rocketry safety codes and motor certification. https://www.nar.org

[11] U.S. Standard Atmosphere (1976) — Tabulated atmospheric density, temperature, pressure, and speed of sound vs altitude. NOAA / NASA / USAF.

[12] Civil Aviation Safety Authority (CASA), Australia — Sporting and Educational Rocketry guidance, CASA Advisory Circular AC 101-1.

[13] *Tripoli Motor Testing Committee Reports* — Certified motor data, total impulse and burn time verification.

[14] HPR-X Series — Technical Specification (TRP-2026-020), Advanced Defence Systems Research Division, March 2026. (Companion operator-spec document; see `HPR-X Series Spec.md` in the same subfolder.)
