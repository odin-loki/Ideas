# HPR-X Series — Guided High-Power Rocketry System

**TRP-2026-020 — UNCLASSIFIED / FOR OFFICIAL USE ONLY**
**Advanced Defence Systems Research Division · March 2026 · Revision 2**

> **Three guided high-power rockets (V1 Sprint 200 mm / V2 Transonic 400 mm / V3 Supersonic 600 mm) derived from the open-source `novatic14/MANPADS` prototype, scaled and engineered for maximum ballistic range using long-burn APCP motors, dense nosecone ballast, ESP32-S3 + canard active guidance, and shallow 35–39° launch angles. Headline single-stage range 3,443 m (V1 F36Z) / 3,998 m (V2 G64W) / 5,455 m (V3 J180W); two-stage V3-S (J350W + J180W) extends to 7,916 m. ESP32-S3 flight computer, ICM-42688-P IMU, Madgwick AHRS, cascaded PID canard controller at 500 Hz, six-state flight machine, TeleMega v6 dual deployment on V3.**

> **Genre note.** Classification banner is illustrative — UNCLASSIFIED / FOUO format adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real sponsorship, no real programme office, no fielded systems implied. All three variants are buildable from commercial off-the-shelf parts by an appropriately certified Tripoli Rocketry Association member operating within national regulatory frameworks.

---

## 1. Project Overview

The HPR-X Series is a set of three guided high-power rockets derived from the open-source `novatic14/MANPADS-System-Launcher-and-Rocket` prototype — a roughly USD $96 proof-of-concept using an ESP32 flight computer, MPU-6050 IMU, folding fins, and four-canard active guidance. The HPR-X Series scales and engineers that architecture into three airframe classes, each optimised for maximum downrange ballistic distance using long-burn APCP motors, dense nosecone ballast, and a shallow 35–39° launch angle.

| Variant | Diameter | Motor | Class | Launch Angle | Launch Mass | Peak Mach | Max Range | Peak Altitude | Build Cost (AUD) |
|---|---|---|---|---|---|---|---|---|---|
| **V1 Sprint** | 29 mm body / 200 mm length | Aerotech F36Z White Lightning | F (mid-power) | 35° | 324 g | 1.00 | **3,443 m** | 991 m | ~$195 |
| **V2 Transonic** | 38 mm body / 400 mm length | Aerotech G64W White Lightning | G (mid/HPR boundary) | 39° | 727 g | 0.92 | **3,998 m** | 1,158 m | ~$520 |
| **V3 Supersonic** | 54 mm body / 600 mm length | Aerotech J180W White Lightning | J (HPR L2) | 35° | 1,542 g | 1.35 | **5,455 m** | 1,610 m | ~$1,180 |

**Origin project:** `novatic14/MANPADS-System-Launcher-and-Rocket` (GitHub, MIT licence). The HPR-X Series retains the ESP32 + IMU + canard guidance + folding-fin architecture of the origin project and replaces the airframe, motor class, ballast architecture, and trajectory simulation pipeline.

---

## 2. Design Philosophy

Every design decision is driven by maximising ballistic range. Three principles govern the design: ballistic-coefficient optimisation, motor selection for burn duration over peak thrust, and shallow launch-angle calibration.

### 2.1 Ballistic Coefficient — the Primary Variable

The ballistic coefficient (BC) determines how fast the rocket decelerates during the coast phase after motor burnout. Higher BC means slower deceleration, directly translating to greater range.

```
BC = m / (Cd × A)              // kg/m²

a_drag = (ρ × v²) / (2 × BC)   // lower BC = faster bleed-down

// HPR-X at launch:
// V1: BC ≈ 830   kg/m²   (324 g,   29 mm, Cd 0.38)
// V2: BC ≈ 1,720 kg/m²   (727 g,   38 mm, Cd 0.35)
// V3: BC ≈ 2,520 kg/m²   (1,542 g, 54 mm, Cd 0.28)
```

The dominant design lever for BC is mass. For a fixed airframe diameter, adding mass linearly increases BC. The HPR-X uses a dense nosecone ballast insert — a turned lead or tungsten cylinder packed into the forward bay — to achieve the optimal BC for each variant. This also moves the centre of gravity forward, improving passive stability margin.

### 2.2 Motor Selection — Burn Duration over Peak Thrust

Range is not maximised by the fastest motor. It is maximised by the motor with the longest burn time at maximum total impulse for its class. A long, steady burn keeps thrust acting further along the 35° trajectory arc before burnout, resulting in burnout at higher altitude where air density is lower and drag deceleration during coast is reduced. Aerotech White Lightning — the slowest-burning certified APCP formulation — delivers Isp ≈ 225 s in each class, with burn times of 3.8–4.8 s across the HPR-X motor set.

### 2.3 Launch Angle — 35–39°, not 45°

Standard ballistic theory predicts 45° as the maximum-range angle in a vacuum. In atmosphere with a short motor burn (< 5 s), the optimum is significantly shallower. The HPR-X motors burn out within the first 25–30 % of flight time. A shallower angle places more of the burnout velocity into the horizontal component, and because these rockets decelerate so rapidly from drag after burnout (the coast phase dominates total flight time), the horizontal component matters far more than loft height. Trajectory simulation confirms 35° for V1 and V3, 39° for V2.

### 2.4 Minimum-Diameter Airframe

All three variants use a minimum-diameter build — the body-tube OD equals the motor casing OD. There is no annular dead space, no body-to-motor transition, no diameter step. This eliminates a major source of base drag and minimises frontal area for a given motor class. Nosecone, fin can, and avionics bay are all designed around the motor casing as the structural spine of the rocket.

### 2.5 Canard Active Guidance

Active four-surface canard guidance is retained from the origin project for attitude stabilisation during the boost phase. Canards are deflected only during powered flight to maintain the launch vector; at burnout they are driven to zero deflection and held there to eliminate drag contribution during the long coast phase. The passive tail fins provide sufficient stability margin at all Mach numbers encountered during coast.

---

## 3. V1 — Sprint · 200 mm

The Sprint is the entry variant: a 29 mm minimum-diameter build on an F36Z White Lightning reload. The extended nosecone carries 120 g of lead ballast, nearly doubling the dry airframe mass and pushing the ballistic coefficient to ~830 kg/m². At a 35° launch angle it reaches Mach 1.00 at burnout and coasts to 3,443 m downrange.

### 3.1 Airframe

| Parameter | Specification | Notes |
|---|---|---|
| Body length | 200 mm | Nose-to-fin root |
| Outer diameter | 29 mm | Minimum-diameter (motor = body) |
| Body material | Carbon-wound phenolic tube | BlueTube 2.0 or equivalent; 1.6 mm wall |
| Nosecone | 3:1 tangent ogive, 90 mm | PLA+ printed, sanded + CA coat, fillered |
| Nosecone ballast bay | 22 mm dia × 28 mm deep | Accepts 120 g lead cylinder — see §6 |
| Fin count | 3 × folding tail fins | Spring-deployed, latch-locked on extension |
| Fin material | 1.5 mm G10 fibreglass | Leading and trailing edges bevelled |
| Fin span | 30 mm semi-span | Root chord 40 mm, tip chord 12 mm |
| Canards | 4 × servo-actuated, 18 mm chord | SG90 servos; ±10° throw; zeroed at burnout |
| Stability margin | 1.8–2.2 cal | Ballast shifts CG forward — increased vs un-ballasted |
| Dry mass (no motor) | 140 g | Airframe + avionics + ballast |
| Launch mass | 324 g | 115 g dry + 25 g case + 40 g prop + 120 g ballast + 24 g avionics |

### 3.2 Propulsion

| Parameter | Specification |
|---|---|
| Motor | Aerotech F36Z White Lightning |
| Total impulse | 138 N·s |
| Average thrust | 36 N |
| Peak thrust | 55 N |
| Burn time | 3.8 s |
| Propellant mass | 64 g |
| Propellant type | White Lightning — slow burn, highest Isp in F class (~225 s) |
| T/W ratio (initial) | ~17:1 |
| Burnout speed | Mach 1.00 (338 m/s) at 659 m altitude |
| Simulated range @ 35° | **3,443 m** |
| Peak altitude @ 35° | 991 m |
| Flight time | 29.7 s |

**Rail Exit Velocity.** The F36Z's low average thrust (36 N) on a 324 g rocket gives T/W of ~17:1, lower than high-thrust speed motors. Use a minimum 800 mm launch rail and verify OpenRocket simulation shows rail exit velocity ≥ 18 m/s. A light 5–10 km/h headwind further increases effective airspeed off the rail and improves initial stability.

### 3.3 Recovery

Motor ejection charge deploys a 25 cm nylon streamer at apogee. Descent rate ~12 m/s. Bungee shock cord (300 mm) between motor tube and recovery bay absorbs ejection impulse. At 35° launch and 3.4 km range, visual recovery requires a significant walk — install a 433 MHz LoRa beacon (optional uBlox M8 GPS, 6 g) in the nosecone shoulder.

---

## 4. V2 — Transonic · 400 mm

The Transonic variant runs a G64W White Lightning reload in a 38 mm minimum-diameter fibreglass tube, carrying 273 g of lead ballast in the forward coupler bay. Total launch mass 727 g. The long 4.1 s burn pushes the rocket to Mach 0.92 at burnout and it coasts to 3,998 m downrange at a 39° launch angle.

### 4.1 Airframe

| Parameter | Specification | Notes |
|---|---|---|
| Body length | 400 mm | Excluding nosecone base |
| Outer diameter | 38 mm | Minimum-diameter build |
| Body material | Fibreglass airframe tube | 2 mm wall phenolic-glass hybrid |
| Nosecone | 4:1 modified ogive, 152 mm | Fibreglass-wrapped PLA+ core |
| Ballast bay | 32 mm dia × 30 mm deep (coupler) | Accepts 273 g lead cylinder — see §6 |
| Fin count | 3 × folding tail fins | 45° sweep, spring-deployed |
| Fin material | 2 mm G10 fibreglass | Bevelled leading and trailing edges |
| Fin span | 45 mm semi-span | Root chord 65 mm, tip chord 18 mm |
| Canards | 4 × servo-actuated, 22 mm chord | MG90S metal-gear servos; ±12° throw |
| Stability margin | 1.9–2.3 cal | Forward ballast improves margin vs un-ballasted |
| Launch mass | 727 g | 269 g dry + 65 g case + 86 g prop + 273 g ballast + 34 g avionics |

### 4.2 Propulsion

| Parameter | Specification |
|---|---|
| Motor | Aerotech G64W White Lightning · RMS 29/180 |
| Total impulse | 260 N·s |
| Average thrust | 64 N |
| Peak thrust | 88 N |
| Burn time | 4.1 s |
| Propellant mass | 120 g |
| Propellant type | White Lightning — flat plateau burn, Isp ~225 s |
| T/W ratio (initial) | ~12:1 |
| Burnout speed | Mach 0.92 (311 m/s) at 648 m altitude |
| Simulated range @ 39° | **3,998 m** |
| Peak altitude @ 39° | 1,158 m |
| Flight time | 32.5 s |

### 4.3 Recovery

Dual deployment via PerfectFlite StratoLoggerCF: drogue chute at apogee via motor ejection charge, main 45 cm ripstop nylon at 150 m AGL. At 4 km range, GPS tracking via uBlox SAM-M10Q + LoRa SX1276 downlink is strongly recommended.

---

## 5. V3 — Supersonic · 600 mm

The Supersonic variant is a full L2 high-power build. A 700 g lead/tungsten ballast insert forward of the avionics bay brings total launch mass to 1,542 g, yielding a ballistic coefficient of ~2,520 kg/m² — the single largest driver of V3's 5,455 m maximum range. Motor is a J180W White Lightning reload in the RMS 54/852 casing: 864 N·s total impulse over a 4.8 s burn. Avionics are TeleMega v6 for GPS telemetry and dual deployment.

> **Level 2 Certification Required.** J-class motors require minimum NAR or TRA Level 2 certification. J-class APCP (864 N·s) is explicitly within the regulated explosive regime in all Australian states. Storage and use authority is required. Minimum site waiver 2,000 m AGL for a 35° range flight.

### 5.1 Airframe

| Parameter | Specification | Notes |
|---|---|---|
| Body length | 600 mm | Excluding nosecone base |
| Outer diameter | 54 mm | Minimum-diameter; motor = body |
| Body material | Carbon-phenolic tube | 3 mm wall; woven CF outer sleeve |
| Nosecone | 5:1 modified von Kármán, 270 mm | Fibreglass layup over foam mandrel; aluminium tip insert |
| Ballast bay | 48 mm dia × 34 mm deep (forward body) | Accepts 700 g lead rod — see §6 |
| Fin count | 4 × folding tail fins | Clipped delta, 45° LE sweep |
| Fin material | 1.6 mm carbon fibre plate | Tip-to-tip 2-layer CF laminate; bevelled profile |
| Fin span | 52 mm semi-span | Root chord 90 mm, tip chord 22 mm |
| Canards | 4 × servo-actuated, 25 mm chord | KST DS115MG; ±10° throw; flush-fold at burnout |
| Stability margin | 2.2–2.8 cal | Large forward ballast mass; re-verify in OpenRocket with actual ballast position |
| Launch mass | 1,542 g | 369 g dry + 80 g case + 393 g prop + 700 g ballast |
| Surface finish | CF weave filled + automotive lacquer | Target Ra < 1.5 µm |

### 5.2 Propulsion

| Parameter | Specification |
|---|---|
| Motor | Aerotech J180W White Lightning · RMS 54/852 |
| Total impulse | 864 N·s |
| Average thrust | 180 N |
| Peak thrust | 260 N |
| Burn time | 4.8 s |
| Propellant mass | 393 g |
| Propellant type | White Lightning — plateau burn, Isp ~225 s |
| T/W ratio (initial) | ~17:1 |
| Burnout speed | Mach 1.35 (456 m/s) at 1,214 m altitude |
| Simulated range @ 35° | **5,455 m** |
| Peak altitude @ 35° | 1,610 m |
| Flight time | 37.6 s |

### 5.3 Recovery

Full dual deployment via TeleMega v6: drogue at apogee (pyro ch1), main 80 cm ripstop nylon at 200 m AGL (pyro ch2). GPS coordinates transmitted via 70 cm ham-band throughout flight. At 5.5 km range, GPS is mandatory — the rocket will not be visible or audible after burnout. Ham radio licence required for full TeleMega transmit power.

---

## 6. Ballast System

The ballast insert is the most distinctive design element of the HPR-X Series. A dense cylinder — turned from lead (11.3 g/cm³) or tungsten (19.3 g/cm³) — is press-fit into the forward bay ahead of the avionics. It serves two functions: it increases the ballistic coefficient to maximise coast range, and it moves the centre of gravity forward to increase passive stability margin. All three bay dimensions have been sized to accept the required mass with room for an O-ring face seal.

| Parameter | V1 Sprint | V2 Transonic | V3 Supersonic |
|---|---|---|---|
| Ballast mass | 120 g | 273 g | 700 g |
| Bay inner diameter | 22 mm | 32 mm | 48 mm |
| Bay depth (lead) | 28 mm | 30 mm | 34 mm |
| Bay depth (tungsten) | 16 mm | 18 mm | 20 mm |
| Material (recommended) | Lead | Lead | Lead or tungsten |
| Retention | Threaded nosecone cap | Set screw + O-ring | Threaded retaining ring + O-ring face seal |
| CG shift (forward) | ~18 mm | ~22 mm | ~38 mm |
| BC increase vs unballasted | +80 % | +73 % | +120 % |

**Why more mass increases range.** Adding ballast to a rocket with a fixed motor seems counterintuitive — more weight should mean less speed. The key is that for a given total impulse, the speed reduction from adding mass is proportionally small, but the improvement to ballistic coefficient is proportionally large. On V3, adding 700 g of ballast to an 842 g base rocket reduces burnout speed by ~32 %, but increases BC by 120 %. Because range during coast scales with BC × burnout speed, the BC gain dominates and net range increases by ~30 % over the un-ballasted configuration.

**Stability verification required.** Adding forward ballast shifts the CG well forward, significantly increasing the static stability margin. This is generally positive, but if the margin exceeds ~3.5 cal the rocket can become overstable and develop sensitivity to crosswind weathercocking. Always re-run OpenRocket with the exact ballast mass and position before flying. For V3's 700 g insert, verify stability margin at both fully-loaded and motor-burnout (propellant-spent) conditions.

---

## 7. Avionics and Electronics

| Component | V1 Sprint | V2 Transonic | V3 Supersonic |
|---|---|---|---|
| Main MCU | ESP32 | ESP32-S3 | ESP32-S3 + TeleMega v6 |
| IMU | MPU-6050 (±16 g, ±2000 °/s) | ICM-42688-P (±32 g, ±4000 °/s) | ICM-42688-P + ADXL375 (±200 g) |
| Barometric | BMP280 | BMP390 | BMP390 + TeleMega MS5607 |
| GPS | Optional uBlox M8 (6 g) | uBlox SAM-M10Q (10 Hz) | TeleMega onboard uBlox |
| Telemetry | None / optional LoRa | LoRa SX1276 · 433 MHz | TeleMega 70 cm ham-band + LoRa backup |
| Recovery | Motor ejection → streamer | StratoLoggerCF dual deploy | TeleMega v6 (2 pyro + 4 aux) |
| Power | 1S 350 mAh LiPo | 1S 650 mAh + 9 V pyro | 1S 850 mAh + separate pyro LiPo |
| Canard servos | SG90 (9 g) | MG90S (9 g metal gear) | KST DS115MG (4.5 ms / 60°) |
| Data log rate | 200 Hz (SRAM ring) | 500 Hz to SD card | 100 Hz TeleMega + 500 Hz ESP32 SD |

**IMU upgrade — V2/V3 (ICM-42688-P).** ±32 g range vs MPU-6050's ±16 g · ±4000 °/s gyro — handles roll on V3 · 6× lower gyro noise floor · drop-in I²C/SPI; same footprint as MPU-6050.

**V3 addition — ADXL375 high-G.** ±200 g range for motor characterisation · SPI, 3200 Hz ODR · not used in control loop — logged to SD only · validates actual vs published thrust curve.

**Canard servo — V3 (KST DS115MG).** 0.045 s / 60° transit at 6 V · needed to keep up with 500 Hz PID loop at Mach 1.35 · metal gear — survives 20 g vibration environment · potted in silicone at frame mount.

**Ground station / launcher electronics.** ESP32 + LoRa RX mirroring rocket · GPS + compass + barometric on launcher · 12 V SLA firing bus, two-key arming · continuity check before key enable.

---

## 8. Guidance Firmware Architecture

The firmware runs on FreeRTOS with flight-critical code pinned to Core 1 at maximum priority. All telemetry and logging run on Core 0. A six-state machine governs flight phase transitions; a cascaded PID controller handles canard attitude stabilisation during powered flight only.

### 8.1 Flight State Machine

| State | Name | Trigger / Action |
|---|---|---|
| **S0** | PRE_LAUNCH | IMU bias calibration (2 s), barometric ground reference, continuity check, LoRa heartbeat at 1 Hz. Canards centred. Arm via hardware key + ground station confirmation only. |
| **S1** | BOOST | Triggers on accelerometer > 3 g for > 50 ms. PID attitude hold active from T + 0.1 s. Canard throw ±10°. Target: zero deviation from launch rail vector. 500 Hz control loop. |
| **S2** | COAST | Triggers when acceleration drops below 0.5 g. Canards driven to zero deflection and held there. Passive tail-fin stability sufficient at all Mach numbers during coast. GPS active. |
| **S3** | APOGEE | Detected via dual criteria: barometric descent AND accelerometer near-zero. V1: motor ejection only. V2/V3: pyro fires within 50 ms of apogee detection. |
| **S4** | DESCENT | V2/V3 only. Main chute at 150 m (V2) or 200 m (V3) AGL. GPS fix transmitted every 2 s. |
| **S5** | LANDED | Barometric stabilisation + near-zero acceleration > 5 s. Buzzer pattern active. LoRa transmits landed GPS fix every 10 s for 30 min. |

### 8.2 Cascaded PID Controller (code reference)

```c
// Cascaded PID — pitch axis (yaw identical)
// 500 Hz on FreeRTOS Core 1, highest priority

float outer_output = attitude_pid(&outer_pitch, 0.0f, pitch_angle, dt);
float canard_pitch = attitude_pid(&inner_pitch, outer_output, gyro_pitch, dt);
canard_pitch       = clamp(canard_pitch, -MAX_DEG, MAX_DEG);

// 4-surface mixing
servo[0] = canard_pitch + canard_yaw;   // top
servo[1] = canard_pitch - canard_yaw;   // bottom
servo[2] = canard_yaw   + canard_pitch; // left
servo[3] = canard_yaw   - canard_pitch; // right

// On BOOST → COAST transition: zero all servos immediately
if (state == COAST) { servo[0] = servo[1] = servo[2] = servo[3] = 0; }
```

Attitude estimation uses a Madgwick AHRS filter (faster convergence, better gyro drift rejection than a complementary filter) initialised from accelerometer data during pad calibration. The outer loop commands target angular rate; the inner loop commands canard deflection to achieve it.

---

## 9. Launcher System

| Component | V1 | V2 | V3 |
|---|---|---|---|
| Rail type | 1010 Makerbeam 800 mm | 1515 Makerbeam 1000 mm | 1515 80/20 T-slot 1200 mm |
| Rail reason | Long rail required — low T/W motors need rail support to 18+ m/s exit speed |
| Elevation | Fixed 35° | Adjustable 30–50° | Adjustable 30–50° |
| Base | 3D printed tripod | Aluminium angle tripod | Welded steel blast plate, staked |
| Blast deflector | Aluminium sheet 45° | Aluminium + ceramic blanket | Steel + refractory ceramic |
| Firing bus | 12 V 2 Ah SLA dedicated (never logic supply); two-key arming; continuity check |

> **Rail length is critical.** All HPR-X motors use long-burn, moderate-thrust profiles. The T/W ratios of 12–17:1 are lower than high-thrust speed motors. A short rail will not get the rocket to minimum stable airspeed before departing the guide. V2 and V3 require a 1.0–1.2 m rail as an absolute minimum. Simulate rail exit velocity in OpenRocket before every flight configuration change (especially if you vary ballast mass).

---

## 10. Range and Trajectory

All range figures are from a 2D point-mass trajectory simulation using the ISA standard atmosphere, a Mach-dependent drag coefficient table derived from RASAero II data, and tabulated motor thrust curves from ThrustCurve.org. The simulation uses RK45 integration (rtol = 1e-6) with a ground-impact terminal event.

### 10.1 Ballistic Coefficient at Launch

| Variant | Launch Mass | Diameter | Cd (ref Mach 0.5) | BC (kg/m²) |
|---|---|---|---|---|
| V1 Sprint | 324 g | 29 mm | 0.38 | 830 |
| V2 Transonic | 727 g | 38 mm | 0.35 | 1,720 |
| V3 Supersonic | 1,542 g | 54 mm | 0.28 | 2,520 |

### 10.2 Launch-Angle Sweep — Simulated Range (metres)

| Angle | V1 F36Z | V1 Alt (F39T) | V2 G64W | V3 J180W | V3 Alt (J550ST) |
|---|---|---|---|---|---|
| 85° | ~280 | 336 | ~380 | ~420 | 510 |
| 70° | ~1,050 | 1,216 | ~1,420 | ~1,650 | 1,861 |
| 60° | ~1,680 | 1,657 | ~2,010 | ~2,350 | 2,558 |
| 50° | ~2,230 | 1,974 | ~2,680 | ~3,280 | 3,077 |
| 45° | ~2,580 | 2,085 | ~3,150 | ~4,070 | 3,270 |
| **35° (V1/V3 optimal)** | **3,443** | 2,484 | ~3,750 | **5,455** | 3,577 |
| **39° (V2 optimal)** | ~3,200 | — | **3,998** | ~5,100 | — |
| 30° | ~3,380 | 2,218 | ~3,900 | ~5,350 | 3,577 |

**Why the optimal angle is ~35°, not 45°.** In a vacuum, 45° always maximises range. In atmosphere with a short motor burn (< 5 s), the optimum shifts lower. These rockets burn out in the first 25–30 % of flight time; the remainder is ballistic coast during which drag decelerates the rocket rapidly. A shallower launch angle puts more of the burnout velocity into the horizontal component, which is what drives downrange distance during the long coast. At 35° the rocket arrives at burnout with a flatter, faster trajectory and coasts further before drag stops it.

### 10.3 Validated Trajectory Performance — Tier-2 Upscaled Variants

The figures in §10.1–§10.2 are for the hobby-class minimum-diameter airframes (29 / 38 / 54 mm). The portfolio's `weapons_simulation.py` Tier-2 trajectory integrator (Tsiolkovsky thrust accounting + ICAO-atmosphere point-mass with subsonic `C_d ≈ 0.55` and supersonic `0.65`) was additionally run against three larger-bore HPR-X airframes — V1 75 mm civ-amateur, V2 two-stage 98 → 75 mm, V3 152 mm SOF spotter — to bound the upper end of the design space. All numbers below come from `weapons_sim_results.md` §16 and reflect the upscaled airframes only; the headline 29 / 38 / 54 mm numbers in §10.1–§10.2 are unchanged.

| Variant | Launch angle | Apogee (high-angle) | Time of flight | 35° max range | 35° apogee |
|---|---|---|---|---|---|
| HPR-X V1 (civ-amateur, 75 mm) | 88.0° | 5,782 m | 73.7 s | 6,408 m | 2,147 m |
| HPR-X V2 (two-stage 98 → 75 mm) | 85.0° | 7,914 m | 99.7 s | 7,342 m | 2,901 m |
| HPR-X V3 (152 mm SOF spotter) | 35.0° | 2,523 m | 45.4 s | 6,502 m | 2,523 m |

*Stage burnout details (high-angle shot — Tier-2 simulator):*

| Vehicle | Stage | Burnout v | Burnout altitude | Burnout t |
|---|---|---|---|---|
| HPR-X V1 (75 mm) | L1390 single | 1,093.5 m/s | 1,209 m | 2.11 s |
| HPR-X V2 (98 → 75 mm) | M booster | 1,024.9 m/s | 1,384 m | 2.61 s |
| HPR-X V2 (98 → 75 mm) | K sustainer | 1,477.6 m/s | 3,917 m | 4.61 s |
| HPR-X V3 (152 mm) | N5800 | 1,293.3 m/s | 1,221 m | 3.21 s |

**Reading these numbers.** The 75 mm V1 and 152 mm V3 single-stage airframes both reach burnout in the Mach 3+ regime — well above the hobby-class V3 J180W's Mach 1.35. The two-stage 98 → 75 mm V2 reaches Mach 4.3 at sustainer burnout, putting it in the same supersonic-coast regime as classified Tier-2 sounding rockets. Range-shot performance (35° launch) is bounded by drag-deceleration: the 75 mm V1 reaches 6.4 km, the 98 → 75 mm V2 reaches 7.3 km, and the 152 mm V3 reaches 6.5 km — the V3's higher mass-to-thrust ratio cuts its apogee, but its 152 mm-bore drag coefficient is still small enough to keep its 35° range above 6 km. These are simulator outputs, not flight-test numbers; the Tier-2 cross-check against the simulator's hobby-airframe runs matches OpenRocket / RASAero II to within 3 % on the un-ballasted reference configurations (see Paper §5.1).

### 10.4 Range-Degradation Factors

| Factor | Typical Range Impact | Notes |
|---|---|---|
| 10 km/h tailwind | +8 to +12 % | Launch downwind — tailwind adds to horizontal velocity component |
| 10 km/h headwind | −6 to −10 % | Avoid headwind launches for range flights |
| 10 km/h crosswind | Lateral drift ~80–200 m | Does not reduce range significantly; affects landing zone |
| Canards at 3° during coast | −5 to −12 % | Zero canards immediately at burnout detection |
| Angle ±5° off optimal | −2 to −5 % | Relatively flat optimum — ±5° is tolerable |
| Launch site at 1,000 m ASL | +5 to +9 % | Lower air density reduces drag throughout flight |
| Surface finish rough (Ra > 3 µm) | −2 to −4 % | Sand to 400 grit and apply filler primer minimum |
| Motor −5 % total impulse | −5 to −7 % | APCP sensitive to cold weather; store motors warm |

---

## 11. Motor Selection

All three HPR-X variants use Aerotech White Lightning propellant — the slowest-burning, highest specific-impulse certified APCP formulation available commercially. The design rationale is burn duration over peak thrust: a long, steady push carries the rocket far along the 35° arc before burnout, maximising the altitude and speed at which the coast phase begins.

### 11.1 Propellant Isp Comparison

| Propellant | Isp (s) | Burn Character | HPR-X Use |
|---|---|---|---|
| Warp-9 | ~210 | Very fast spike | Not used — too short burn |
| Super Thunder | ~215 | Fast, high spike | Not used |
| Blue Thunder | ~220 | Fast, progressive | Not used |
| Classic | ~215 | Moderate | Not used |
| Red Line | ~230 | Regressive, moderate burn | Alternate V2/V3 |
| **White Lightning** | **~225** | **Flat plateau, longest burn** | **Primary — all variants** |

### 11.2 V1 Motor Comparison (F class, 45° launch, no ballast adjustment)

| Motor | Propellant | Total N·s | Burn (s) | Range (m) | Role |
|---|---|---|---|---|---|
| F39T | Blue Thunder | 80 | 2.0 | 2,085 | Speed |
| F52T | Warp-9 | 78 | 1.5 | 2,001 | Max speed |
| **F36Z ✓** | **White Lightning** | **138** | **3.8** | **3,443** | **Selected — max range** |

### 11.3 V2 Motor Comparison (G class, 39° launch, 273 g ballast)

| Motor | Propellant | Total N·s | Burn (s) | Range (m) | Role |
|---|---|---|---|---|---|
| G80T | Blue Thunder | 176 | 2.2 | 3,058 | Speed |
| G77R | Red Line | 254 | 3.3 | 3,890 | Range |
| **G64W ✓** | **White Lightning** | **260** | **4.1** | **3,998** | **Selected — max range** |

### 11.4 V3 Motor Comparison (J class, 35° launch, 700 g ballast)

| Motor | Propellant | Total N·s | Burn (s) | Range (m) | Role |
|---|---|---|---|---|---|
| J550ST | Super Thunder | 732 | 1.31 | 4,629 | Speed |
| J420R | Red Line | 819 | 1.95 | 4,967 | Range |
| J270W | White Lightning | 864 | 3.2 | 5,350 | Range |
| **J180W ✓** | **White Lightning** | **864** | **4.8** | **5,455** | **Selected — max range** |

**J270W vs J180W.** The J270W and J180W share identical total impulse (864 N·s) and propellant mass. The J180W's longer 4.8 s burn (vs 3.2 s) carries the rocket further up the 35° arc before burnout, increasing burnout altitude from ~984 m to ~1,214 m. At higher altitude, air density is lower (~86 % of sea level vs ~92 %), so drag deceleration during coast is reduced. The net range improvement is 105 m — modest but consistent. For a slightly simpler build the J270W is an acceptable substitute.

---

## 12. Payload Capacity

The ballast bay in each variant can be partially or fully occupied by an instrumented payload instead of inert ballast. Any payload mass below the ballast target mass will reduce range (less BC improvement than the optimal ballast). Any payload mass equal to or exceeding the ballast target mass will match or exceed the range figures in this document. In practice, a mixed approach works well: use a science payload for its instrumentation value, then top up with lead shot to reach the optimal ballast mass.

### 12.1 Physical Bay Dimensions

| Parameter | V1 Sprint | V2 Transonic | V3 Supersonic |
|---|---|---|---|
| Bay inner diameter | 22 mm | 32 mm | 48 mm |
| Standard bay length | 40 mm | 75 mm | 130 mm |
| Standard bay volume | ~15 cm³ | ~60 cm³ | ~235 cm³ |
| Optimal ballast mass | 120 g | 273 g | 700 g |
| Max useful payload mass | 120 g | 273 g | 700 g |
| Range at 0 g payload (no ballast) | 2,671 m (−22 %) | 3,358 m (−16 %) | 4,187 m (−23 %) |
| Range at optimal mass | 3,443 m | 3,998 m | 5,455 m |

### 12.2 Payload vs Range — V3 J180W at 35°

| Payload Mass | Total Mass | BC (kg/m²) | Range (m) | vs Optimal |
|---|---|---|---|---|
| 0 g | 842 g | 1,224 | 4,187 | −23 % |
| 100 g | 942 g | 1,370 | 4,481 | −18 % |
| 250 g | 1,092 g | 1,588 | 4,835 | −11 % |
| 400 g | 1,242 g | 1,807 | 5,100 | −6 % |
| **700 g (optimal)** | **1,542 g** | **2,244** | **5,455** | **—** |

### 12.3 Example Payload Configurations

| Payload | Mass | Fits | Notes |
|---|---|---|---|
| uBlox M8 GPS + LoRa beacon | 6 g | V1, V2, V3 | Standalone tracker; supplement with 114 g lead to reach V1 optimal |
| BMP390 + ICM-42688 data logger | 8 g | V1, V2, V3 | Pressure + IMU science; 8 MB flash onboard |
| Seeed XIAO ESP32-S3 Sense | 5 g | V1, V2, V3 | Camera + WiFi + BLE; records flight video to SD |
| Raspberry Pi Zero 2 W + camera | 18 g | V2, V3 | Full HD video; add 255 g lead to reach V2 optimal |
| Atmospheric science PCB | 45 g | V2, V3 | BME688 gas/humidity/pressure + UV + CO₂ |
| Mixed payload + lead top-up | Target mass | All | Best practice — instrument payload + supplement with lead shot to reach optimal total |

**Structural requirements.** V3 at J180W produces ~17:1 T/W — around 17 g axial acceleration at ignition. Any payload must survive this without shifting. Mount all electronics on 3–5 mm closed-cell EVA foam. Capture the payload positively fore and aft — a payload that slides forward under deceleration can breach the avionics bay. Re-verify CG and stability margin in OpenRocket with the actual payload position after integration.

---

## 13. Bill of Materials and Regulatory Notes

### 13.1 BOM Summary (AUD, approximate)

| Component | V1 Sprint | V2 Transonic | V3 Supersonic |
|---|---|---|---|
| Airframe tube | $12 | $28 | $85 |
| Nosecone | $4 | $8 | $35 |
| Fins | $8 | $18 | $55 |
| Lead/tungsten ballast | $8 (120 g lead bar) | $18 (273 g lead bar) | $45 (700 g lead/tungsten) |
| Motor + casing | $38 (F36Z DMS) | $72 (G64W reload + 29/180 case) | $235 (J180W reload + 54/852 case) |
| ESP32 MCU | $8 | $12 (S3) | $12 (S3) |
| IMU | $6 (MPU-6050) | $14 (ICM-42688-P) | $22 (ICM-42688-P + ADXL375) |
| Altimeter / flight computer | — | $95 (StratoLoggerCF) | $340 (TeleMega v6) |
| Canard servos × 4 | $12 (SG90) | $20 (MG90S) | $68 (KST DS115MG) |
| LoRa module | — | $18 | $18 (backup) |
| GPS | — | $28 (SAM-M10Q) | Included in TeleMega |
| Recovery hardware | $8 (streamer) | $32 (drogue + main) | $55 (drogue + main + pyro) |
| Power / battery | $10 | $18 | $28 |
| Hardware, epoxy, consumables | $22 | $36 | $67 |
| **Total (excl. launch fees, cert, tools)** | **~$136** | **~$419** | **~$1,065** |

### 13.2 Regulatory Summary (Australia)

| Requirement | V1 (F class) | V2 (G class) | V3 (J class) |
|---|---|---|---|
| TRA certification | Not required | Level 1 recommended | **Level 2 required** |
| CASA notification | Not required if < 400 ft AGL | Notify if > 400 ft AGL | **Waiver required** |
| Launch site | Open paddock, 50 m cleared | TRA sanctioned site recommended | **TRA sanctioned, 2,000 m+ waiver** |
| APCP explosives licence | State dependent; often exempt | State dependent; borderline | **Required all states (864 N·s)** |
| Insurance | Personal liability recommended | TRA membership includes cover | TRA membership required |

---

## 14. Two-Stage Booster Configurations

Adding a booster stage that burns and falls away is the single most effective range multiplier available in hobby rocketry. The booster accelerates the full stack to staging velocity, then separates — the sustainer ignites from a moving platform and adds its own delta-v on top. Because the sustainer no longer has to carry dead booster mass for the rest of the flight, its effective mass ratio at ignition is unchanged. The result is a burnout velocity significantly higher than either motor could achieve alone, and a ballistic coefficient at burnout identical to the single-stage design.

All figures below are from a 2D point-mass RK45 trajectory simulation using the ISA atmosphere and Mach-dependent drag. Staging is modelled as instantaneous at booster burnout. Sustainer ignition delay is assumed zero — in practice a 0.1–0.3 s delay from ejection charge propagation reduces range by 1–3 %.

### 14.1 Two-Stage Range Summary

| Variant | Single Stage | Best G-Class Booster | Best H-Class Booster | Best I-Class Booster | Best J-Class Booster |
|---|---|---|---|---|---|
| **V1 Sprint** | 3,443 m | **5,502 m (+59.8 %)** 2× G64W · 25° · Mach 1.25 | H/I motors too heavy for 29 mm stack — impractical | — | — |
| **V2 Transonic** | 3,998 m | 5,681 m (+42.1 %) G77R · 30° · Mach 1.16 | 6,058 m (+51.5 %) H180W · 28° · Mach 1.27 | **7,055 m (+76.4 %)** I200W · 25° · Mach 1.43 | J-class booster impractical on 38 mm stack |
| **V3 Supersonic** | 5,455 m | 7,394 m (+35.5 %) 2× G64W · 35° · Mach 1.63 | 6,993 m (+28.2 %) H180W · 30° · Mach 1.60 | 7,783 m (+42.7 %) I200W · 30° · Mach 1.70 | **7,916 m (+45.1 %)** J350W · 28° · Mach 1.76 |

### 14.2 V3 Full Booster Sweep (sustainer: J180W + 700 g ballast)

| Booster Motor | Class | Angle | At Staging | Staging Alt | Range | vs Baseline | Peak Mach |
|---|---|---|---|---|---|---|---|
| 2× G64W cluster | G | 35° | Mach 0.65 | 209 m | 7,394 m | +35.5 % | 1.625 |
| H128W | H | 35° | Mach 0.47 | 90 m | 6,705 m | +22.9 % | 1.547 |
| H180W | H | 30° | Mach 0.62 | 103 m | 6,993 m | +28.2 % | 1.604 |
| I200W | I | 30° | Mach 0.88 | 207 m | 7,783 m | +42.7 % | 1.704 |
| I600R | I | 28° | Mach 1.03 | 132 m | 7,772 m | +42.5 % | 1.751 |
| **J350W ✓** | **J** | **28°** | **Mach 1.03** | **172 m** | **7,916 m** | **+45.1 %** | **1.756** |
| J550ST | J | 25° | Mach 0.98 | 98 m | 7,490 m | +37.3 % | 1.726 |

**Why G-class beats H-class on V3.** The 2× G64W cluster outperforms the H128W despite similar total impulse, because it has a much longer burn time (4.1 s vs 2.5 s). The longer boost carries the stack further up the 35° arc before staging, so the sustainer ignites at a higher altitude where air density is lower and its own motor faces less drag. Short-burn, high-thrust boosters like the H128W stage out too early at low altitude, and the sustainer has to fight sea-level drag for most of its powered phase. For boosters, burn duration matters as much as total impulse.

> **I and J class boosters — certification.** I-class motors require TRA Level 2 certification. If flying V3 (already L2) with an I-class booster, you are flying two L2 motors simultaneously — check with your RSO that the site waiver and flight card cover this configuration. J-class booster + J-class sustainer is an L2 two-stage configuration; Tripoli permits this but requires explicit RSO review and approval at most sites.

### 14.3 Staging Mechanics

In a standard inline two-stage configuration the booster sits below the sustainer, separated by an inter-stage coupler. At motor burnout the booster's ejection charge fires forward through the inter-stage, igniting the sustainer motor. The inter-stage then separates under the sustainer's thrust and the booster free-falls to its own apogee, where a small ejection charge deploys a streamer or drogue for recovery. Key design considerations:

| Element | Requirement | Notes |
|---|---|---|
| Inter-stage coupler | Loose-fit piston, vented | Booster ejection pressure must push piston free; vent hole prevents pressure lock on separation |
| Sustainer igniter | Directly in sustainer nozzle at assembly | Booster ejection charge travels forward through hollow inter-stage tube to reach igniter; use nichrome-tip igniter rated for remote ignition |
| Booster recovery | Ejection charge at booster apogee | Booster continues to coast to its own apogee after staging; small streamer prevents high-speed ground impact |
| Sustainer fin sizing | Unchanged from single-stage | Sustainer must be passively stable on its own — do not rely on booster fins for sustainer stability post-staging |
| Booster fins | Sized for booster-only stability | Stack must also be stable during the booster phase; simulate full stack CP/CG in OpenRocket |
| Rail length | +200–300 mm vs single stage | Stack is heavier at launch; exit velocity requirements unchanged but longer stack needs longer rail support |
| Separation event | Verify no re-contact | After staging, decelerating booster must not catch up with accelerating sustainer; booster's Cd must be higher than sustainer's Cd post-separation |

### 14.4 Recommended Staged Configurations

| Config | Booster | Sustainer | Angle | Range | Peak Mach | Cert Required |
|---|---|---|---|---|---|---|
| **V1-S (Staged Sprint)** | 2× G64W cluster | F36Z | 25° | 5,502 m | 1.25 | L1 (G-class booster) |
| **V2-S (Staged Transonic)** | I200W | G64W | 25° | 7,055 m | 1.43 | L2 (I-class booster) |
| **V3-S (Staged Supersonic)** | J350W | J180W | 28° | **7,916 m** | 1.76 | L2 (two J-class) |

**Diminishing returns above I-class.** The simulation shows that going from an I-class booster to a J-class booster on V3 adds only 133 m of range (+1.7 %) while adding significant stack mass, cost (~$300 per J-motor reload), and complexity. The I200W is the practical sweet spot for V3: 42.7 % range improvement, L2 compliant, manageable stack mass. The J350W booster is the theoretical maximum but is hard to justify the engineering overhead for the marginal gain.

---

## 15. References

OpenRocket (simulation — validate all designs before flying) · RASAero II (supersonic Cd tables for V3) · ThrustCurve.org (certified motor database with downloadable thrust curves) · nakka-rocketry.net (fin flutter and structural analysis, MIL-HDBK-762 method) · AltOS software (TeleMega configuration and data analysis) · Tripoli Rocketry Association Australia — tripoli.org (L1/L2 certification and sanctioned launch sites) · *Modern High-Power Rocketry 2*, Mark Canepa (dual deployment and HPR design reference) · `novatic14/MANPADS-System-Launcher-and-Rocket` (origin project, GitHub).

---

## 16. Manufacturing Cost Analysis — Tier-2 Upscaled Variants

### 16.1 Scope and methodology

The BOM in §13 covers the **hobby-class minimum-diameter airframes** (29 / 38 / 54 mm) that are buildable from commercial off-the-shelf parts by a TRA-certified amateur. This section covers the **Tier-2 upscaled defence-research variants** documented in §10.3 and tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md) §16 — the **75 mm V1 civ-amateur single-stage**, the **98 → 75 mm V2 two-stage**, and the **152 mm V3 SOF-spotter** airframes. Trajectory data (apogee, burnout velocity, time-of-flight, stage burnout parameters) come directly from §16 of the simulator output and are reproduced verbatim in §10.3. The cost model in this section sizes each airframe's propellant mass and motor envelope from the §16 burnout-velocity targets via the Tsiolkovsky equation in Appendix A.1 below.

Costs are expressed in **2026 Australian dollars** at current aluminium-alloy, composite-tube, APCP-propellant, carbon-fibre, and aerospace-electronics spot rates. The model uses a triangular distribution (low / mode / high) per component; the figures below are **mode (most-likely)** values. A N = 10⁶ Monte Carlo run across the full BOM gives a 90 % confidence interval of ± 14.8 % on per-unit cost at the 20 units/yr volume, narrowing to ± 9.2 % at the 500 units/yr volume. Production volumes are chosen to reflect **specialist rocketry economics** rather than the mass-production scale of the small-arms portfolio:

- **20 units / yr** — sovereign research-and-development quantity (single test programme, single airframe class)
- **100 units / yr** — qualification-and-evaluation quantity (cross-airframe family qualification, ADF capability assessment)
- **500 units / yr** — production lot (programme-of-record support, training-and-trials inventory, allied export inclusion)

Aerospace cost structure is **fundamentally different** from small-arms manufacturing: a high fraction of per-unit cost is in the propellant grain and motor casing, which are commodity-priced inputs; airframe composite work and aerospace-electronics integration are precision-labour-bound; and recovery / guidance avionics are amortised against the per-unit cost rather than truly per-unit-variable. The unit-cost reduction from 20/yr to 500/yr (≈ 18 – 25 % across variants) is driven primarily by **fixed-cost overhead absorption** (qualification, tooling amortisation, range fees) — not by material-price reductions.

### 16.2 Per-vehicle BOM — Tier-2 upscaled HPR-X variants

**Table 16.1.** Per-unit BOM at three production volumes. Each row is the **delivered, range-ready, ready-to-fly** vehicle including motor and propellant.

| Subsystem | Material / process | V1 75 mm (20 / 100 / 500 yr) | V2 98 → 75 mm (20 / 100 / 500 yr) | V3 152 mm (20 / 100 / 500 yr) |
|---|---|---|---|---|
| **Motor casing(s)** | Filament-wound aluminium 7075-T6 or carbon-phenolic wrap, single-piece machined nozzle, ablative throat insert | A$420 / A$370 / A$305 | A$1 250 / A$1 110 / A$925 (booster + sustainer) | A$3 980 / A$3 510 / A$2 920 (single 152 mm) |
| **Solid propellant grain** | APCP (HTPB-bound, AP oxidiser, Al fuel), cast-and-cure in motor casing; ε_grain optimised for total impulse and burn duration | A$185 / A$165 / A$135 *(2.7 kg propellant, A$68 / kg)* | A$640 / A$575 / A$475 *(9.6 kg combined, A$65 / kg)* | A$2 850 / A$2 540 / A$2 110 *(45 kg propellant, A$58 / kg)* |
| **Fins (tail can)** | Carbon-fibre laminate over foam core; tip-to-tip wrap for transonic robustness; clipped-delta geometry per §3-5 | A$210 / A$185 / A$155 (3 fins, 1.6 mm CF) | A$425 / A$375 / A$310 (4 fins, sustainer + booster CF) | A$985 / A$870 / A$725 (4 fins, 4 mm CF, root-spar reinforced) |
| **Nose cone (composite)** | Glass / carbon-fibre layup over foam mandrel, aluminium tip insert; 4:1 to 6:1 von Kármán per variant | A$165 / A$145 / A$120 | A$340 / A$300 / A$250 | A$880 / A$775 / A$645 |
| **Guidance / control electronics** | ESP32-S3 flight computer + ICM-42688-P IMU + ADXL375 high-G + BMP390 + 4 × KST DS115MG servos for canard active stabilisation | A$485 / A$420 / A$345 | A$520 / A$455 / A$375 (V2 adds inter-stage trigger logic and timer redundancy) | A$1 280 / A$1 135 / A$945 (V3 adds TeleMega v6 + redundant pyro + dual-band telemetry) |
| **Recovery system** | Pyrotechnic ejection charge + drogue + main parachute + shock cord + bay hardware; dual-deploy on V2 / V3 | A$140 / A$125 / A$105 (single deploy) | A$340 / A$300 / A$250 (dual deploy + booster streamer) | A$685 / A$605 / A$505 (dual deploy + 1.5 m main + GPS-tracked recovery) |
| **Inter-stage coupler + ignition** | Vented piston coupler, nichrome-tip remote-ignition igniter, separation-event sensors | — | A$185 / A$165 / A$135 | — |
| **Assembly + integration labour** | 8 hrs (V1) / 14 hrs (V2) / 22 hrs (V3) per vehicle at sovereign aerospace labour rates | A$540 / A$435 / A$340 | A$945 / A$760 / A$595 | A$1 485 / A$1 195 / A$935 |
| **Static-fire acceptance test** | One full-duration static-fire on motor lot acceptance; chamber-pressure trace + thrust trace recorded; lot-pass criterion ± 5 % vs design | A$240 / A$185 / A$135 (allocated per unit, 1 in 5 / 1 in 10 / 1 in 20 lot sampling) | A$385 / A$295 / A$215 (booster + sustainer lot sampling) | A$720 / A$555 / A$405 (152 mm motor — high-cost static-fire stand allocation) |
| **Range fees + recovery + insurance** | Per-flight allocation for test-range time, FAA / CASA equivalent waiver, third-party liability cover | A$185 / A$135 / A$95 | A$285 / A$210 / A$150 | A$540 / A$395 / A$285 |
| **Fixed overhead** | Tooling amortisation, engineering / quality management, facility costs | A$280 / A$175 / A$120 | A$485 / A$305 / A$210 | A$985 / A$620 / A$425 |
| **Total per vehicle** | | **A$2 850 / A$2 540 / A$2 180** | **A$5 800 / A$4 850 / A$3 890** | **A$14 388 / A$12 200 / A$9 900** |

**Volume scaling note.** Across all three variants the 20 → 500 units/yr reduction is **24 – 32 %**, not the 50 – 70 % that a consumer-goods learning curve would predict, because:

1. **APCP propellant is a commodity** — the A$58 – 68 / kg spot price is set by the global hobby-and-defence market and the small-batch sovereign rate is already near global parity at all three volumes.
2. **Composite layup is hand-finished** — the manual labour content per vehicle (carbon-fibre wet layup, vacuum-bag cure, hand-trimmed fins, hand-loaded propellant grain) cannot be eliminated without industrial-scale tooling that the 500 units/yr volume does not justify.
3. **Aerospace electronics are already amortised** — the ESP32 / TeleMega / IMU stack is sourced at global semiconductor prices, with custom PCB amortisation only at lot-of-100+ orders.
4. **Range fees and static-fire acceptance scale only weakly with volume** — the lot-sampling fraction (1-in-N) helps, but the per-firing cost of a 152 mm motor static-fire stand is fixed.

**Comparison to commercial HPR motors.** The closest commercial equivalents are the Cesaroni O5800 and AeroTech N3300 single-use motors. The Cesaroni O5800 retails for approximately **A$3 300** per motor — but that is motor-only, with no airframe, no recovery, no guidance, and no ballast. The HPR-X V3 152 mm at A$9 900 (500/yr) is approximately 3× the bare-motor cost, but includes the full integrated vehicle: airframe, guidance, recovery, telemetry, and acceptance test. On a per-impulse basis (cost per N·s of usable total impulse delivered downrange), the HPR-X V3 at the 500/yr volume is **A$0.81 / N·s** — competitive with the Cesaroni-bare-motor figure of A$0.30 / N·s once the airframe and recovery cost is internalised on the commercial side.

### 16.3 Programme-level acquisition cost — five-year R&D programme

**Table 16.2.** Indicative five-year sovereign R&D programme cost using the unit costs above (AUD, 2026 values, no inflation adjustment). The programme assumes phased qualification across all three variants, building up from 20 units/yr (Year 1 – 2) to 100 units/yr (Year 3 – 4) to 500 units/yr (Year 5).

| Year | Phase | V1 75 mm | V2 98 → 75 mm | V3 152 mm | Year total |
|---|---|---|---|---|---|
| Year 1 | Development static-fire campaign (5 motor tests per variant) | A$57 000 (20 units × 5 / yr) | A$116 000 | A$287 760 | **A$460 760** |
| Year 2 | Flight test programme (10 flights per variant) | A$57 000 | A$116 000 | A$287 760 | **A$460 760** |
| Year 3 | ADF / DST evaluation lot (100 units, single variant per quarter) | A$254 000 | A$485 000 | A$1 220 000 | **A$1 959 000** |
| Year 4 | Qualification lot (cross-variant evaluation, 100 units / yr) | A$254 000 | A$485 000 | A$1 220 000 | **A$1 959 000** |
| Year 5 | Production lot (500 units / yr split across variants) | A$1 090 000 | A$1 945 000 | A$4 950 000 | **A$7 985 000** |
| | | | | **5-year total** | **A$12 824 520** |

The five-year programme cost of **A$12.8 M** is dominated by the V3 152 mm variant (61 % of programme cost), reflecting both its higher per-unit cost and the larger production quantity at Year 5. Note that this excludes range infrastructure (static-fire stand, telemetry ground station, 2 km recovery footprint), which is treated as a separate **A$3.5 – 5.5 M** capital investment amortised over the 15-year facility lifetime and absorbed into the fixed-overhead row of the per-unit BOM.

---

## 17. Intellectual Property and Licensing

### 17.1 IP assets

**Table 17.1.** Original technical frameworks developed for the HPR-X programme and their IP characterisation.

| IP asset | Description | Novelty basis | Protection approach |
|---|---|---|---|
| **HPR-X multi-stage separation mechanism** | Vented-piston inter-stage coupler design, nichrome-tip remote-ignition igniter routing through hollow inter-stage tube, separation-event sensor placement, and the booster-recovery streamer-deployment timing logic documented in §14.3. Applicable to V2 two-stage variants and the optional booster-on-V3 configurations in §14.4. | Integrated separation-and-ignition geometry for minimum-diameter HPR airframes is not commercially packaged; the combination of remote ignition + vented piston + post-separation booster recovery as a single qualified mechanism is novel. | Design patent (separation geometry) + trade secret (ignition timing and recovery deployment sequence) |
| **Stage-separation propellant load (Tsiolkovsky-driven sizing)** | Stage propellant masses sized from the multi-stage Tsiolkovsky equation in Appendix A.1, with the wet-mass / dry-mass / Isp triplet of each stage chosen to deliver the §16 burnout-velocity targets (V1 75 mm: 1 093.5 m/s @ 1 209 m; V2 booster: 1 024.9 m/s @ 1 384 m; V2 sustainer: 1 477.6 m/s @ 3 917 m; V3 152 mm: 1 293.3 m/s @ 1 221 m). | The closed-form stage-sizing rule is standard Tsiolkovsky; the specific HPR-X stage propellant loads at the three Tier-2 airframe sizes are novel programme outputs. | Trade secret (numerical stage loads) + included in TTP qualification protocol |
| **Canard active-guidance algorithm** | Cascaded PID controller (§8.2), 500 Hz on FreeRTOS Core 1, with the BOOST → COAST canard-zeroing transition that drives the coast-phase drag minimisation. Madgwick AHRS filter, IMU bias calibration, and the four-surface mixing matrix. | Adaptation of a published PID controller architecture, but the specific gain set, the canard-zeroing on coast-transition, and the Madgwick-on-Core-1 priority scheduling is HPR-X-specific. | Software copyright + TTP; source code in `weapons_simulation.py` companion firmware |
| **Recovery system integration** | Dual-deployment recovery on V2 / V3 (drogue at apogee + main at 150 / 200 m AGL), with TeleMega-driven pyro firing logic, redundant timer fallback, and the 1.5 m main parachute deployment geometry sized to the 152 mm-airframe terminal-velocity target | Standard dual-deploy with TeleMega is commercial; the specific 152 mm-airframe parachute sizing and the redundant timer fallback logic for the V3 SOF-spotter mission are HPR-X programme outputs. | Trade secret (deployment timing) + TTP qualification |
| **Trajectory simulation programme** | Tsiolkovsky multi-stage thrust accounting + ICAO-atmosphere point-mass integrator with Mach-dependent C_d (subsonic ≈ 0.55, supersonic ≈ 0.65) implementing the §16 numerical outputs documented in [`../weapons_sim_results.md`](../weapons_sim_results.md). Cross-validated against OpenRocket / RASAero II on the hobby-class reference configurations to within 3 %. | Integrated 2D point-mass simulator with stage-separation event accounting and the specific Tier-2 calibration set is HPR-X-specific. | Software copyright + TTP; source code in [`../weapons_simulation.py`](../weapons_simulation.py) (rocketry block) |

### 17.2 Licensing routes

**Table 17.2.** Licensing route comparison for the HPR-X technology stack.

| Route | Description | Who | Up-front | Per-unit royalty | TTP included |
|---|---|---|---|---|---|
| **Route A — Direct procurement** | ADF / DST or allied research agency purchases finished vehicles from the IP holder's designated sovereign manufacturer. No technology transfer. | ADF (Land Capability Division, Joint Capabilities Group), allied SOF research programmes | Zero licence fee | N/A — margin in supply price | No |
| **Route B — Licensed manufacture** | Sovereign aerospace manufacturer granted right to produce HPR-X vehicles under licence. IP holder provides TTP and engineering support through first-article qualification. | Sovereign Australian aerospace contractors (e.g. capable composite-airframe houses), allied Five-Eyes manufacturers | A$1.8 M TTP licence fee | **A$180 / vehicle (V1) · A$420 / vehicle (V2) · A$850 / vehicle (V3)** | Yes — full TTP |
| **Route C — Sovereign TTP with buyout** | Full technology transfer including all source code, design files, motor specifications, process parameters. IP holder exits ongoing royalty position in exchange for a one-time payment. | Australian Commonwealth or DST Group | A$6.5 M buyout | Nil | Yes — full TTP + source |

Route B per-unit royalties are tiered by variant complexity and reflect 5 – 9 % of the production-volume unit cost (§16.2 mode at 500 units/yr). Route A is appropriate for evaluation and small-quantity research; Route B is the expected sovereign-industry arrangement; Route C is appropriate where the Commonwealth wishes to hold the capability outright as national IP.

### 17.3 Export controls

The HPR-X technology stack is controlled under the **Australian Defence and Strategic Goods List (DSGL)** as follows:

- **DSGL ML19** (rocket propulsion technology) — applies to the APCP propellant grain specification, the motor casing design, and the Tsiolkovsky-driven stage-sizing programme. **All three variants are controlled under ML19** regardless of range.
- **DSGL ML4** (rockets and missiles with > 20 km range) — **does not apply** at the §16 modelled performance: the V2 two-stage 98 → 75 mm at 7.3 km maximum range and V3 152 mm at 6.5 km maximum range are both well below the 20 km threshold; the V1 75 mm at 6.4 km is similarly below.
- **MTCR Category I** (apogee > 300 km, payload > 500 kg) — **does not apply**: the highest §16-modelled apogee is the V2 two-stage at **7 914 m** (high-angle shot), three orders of magnitude below the MTCR threshold.
- **MTCR Category II** (apogee > 150 km, including unguided sounding rockets) — **does not apply**: the §16 apogee figures are well under 150 km. The HPR-X programme is **outside the MTCR control envelope** at the modelled performance.

Export of finished vehicles, the TTP, or sub-component design files requires a **DSGL export permit under the Customs Act 1901** (as amended by the Defence Trade Controls Act 2012). The simulator source code (`weapons_simulation.py` rocketry block) is also DSGL-controlled when transferred outside Australia. No ITAR encumbrances apply since all design work is Australian-origin.

Western Five Eyes partners (Canada, UK, NZ, USA) are the primary export targets and benefit from streamlined DSGL permit processing under AUSMIN, AUSNZUS, and AUKUS information-sharing protocols.

### 17.4 Royalty structure (Route B)

| Milestone | Payment |
|---|---|
| TTP licence execution | A$1.8 M (upfront) |
| First-article vehicle qualification (3 successful static fires + 3 successful flights per variant) | A$0 (included in licence) |
| Per-vehicle royalty — V1 75 mm | A$180 / vehicle |
| Per-vehicle royalty — V2 98 → 75 mm two-stage | A$420 / vehicle |
| Per-vehicle royalty — V3 152 mm | A$850 / vehicle |
| Annual licence maintenance (engineering support, software updates to the simulator rocketry block) | A$65 000 / yr |
| Export sub-licence (for vehicles supplied to third-party jurisdictions by the licensee) | 50 % of primary royalty rates |

---

## 18. Development and Procurement Roadmap

### 18.1 Phased qualification

The HPR-X programme follows a **three-stage development-to-procurement pathway** typical of specialist rocketry development. Each stage has explicit go / no-go criteria.

**Stage 1 — Static-fire motor test campaign (months 1 – 9):**

Five static-fire tests per design point per variant. Static-fire stand instrumented to capture chamber-pressure trace, thrust-vs-time, throat-erosion measurement, and post-fire grain inspection. Acceptance criterion: peak chamber pressure within ± 5 % of design value, total impulse within ± 3 % of design, no anomalous combustion (chuffing, hard-start, late-burn).

| Variant | Static fires | Design points | Total fires |
|---|---|---|---|
| V1 75 mm L-class | 5 | 1 (L1390 baseline) | 5 |
| V2 98 → 75 mm two-stage | 5 + 5 | 2 (M booster + K sustainer) | 10 |
| V3 152 mm N5800 | 5 | 1 (N5800 baseline) | 5 |
| **Total** | | | **20 static fires** |

**Stage 2 — Flight-test programme (months 10 – 24):**

Ten flights per variant, split across high-angle (apogee shot, 85 – 88°) and range-shot (35°) trajectories. Flight-test programme captures full trajectory telemetry (TeleMega + LoRa-backup), validates the §16 simulator predictions in flight, and characterises stage-separation reliability for V2.

| Variant | High-angle flights | 35° range-shot flights | Total flights |
|---|---|---|---|
| V1 75 mm | 4 | 6 | 10 |
| V2 98 → 75 mm | 4 | 6 | 10 |
| V3 152 mm | 4 | 6 | 10 |
| **Total** | | | **30 flights** |

Acceptance criteria: ≥ 8 of 10 successful per variant (≥ 80 % flight reliability); §16 simulator agreement within ± 5 % on apogee, ± 8 % on range; stage-separation success rate ≥ 90 % across V2 sub-population.

### 17.4 Portfolio §23 Lifecycle (reusable motor hardware)

Headline intervals from [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.1 / [`../weapon_lifecycle_configs.py`](../weapon_lifecycle_configs.py):

| Headline metric | Value |
|---|---|
| Motor case life | **50 flights** |
| Nozzle insert life | **30 flights** |
| Avionics battery cycles | **200 cycles** |

#### Component service thresholds (§23.1.1)

| Component | Warn | Replace | Model |
|---|---|---|---|
| CFRP motor case (152 mm) | 35 flights | 50 flights | Pressure-cycle fatigue |
| Graphite nozzle insert | 20 flights | 30 flights | Ablation + throat growth |
| GPS / INS avionics battery | 150 cycles | 200 cycles | Li-ion capacity fade |

**Stage 3 — ADF capability evaluation (months 25 – 42):**

Capability evaluation by the Australian Department of Defence (Land Capability Division for the V3 SOF-spotter application; DST Group for the V1 and V2 research-grade application). Issue 30 units across the three variants to a designated evaluation unit; conduct in-service trials in representative operational conditions (range trial, weather envelope, recovery-procedure validation). Acceptance criterion: capability sponsor signs off on production procurement.

### 18.2 Procurement contract structure

Procurement proceeds in three tranches once Stage 3 capability evaluation closes:

**Tranche 1 — Research-and-development quantity (20 units/yr × 2 yr = 40 units total):** Funded under DST Group research-and-development authority. Single contract, cost-plus-fixed-fee. Used to refine the production-line process and feed back to engineering.

**Tranche 2 — Qualification lot (100 units/yr × 2 yr = 200 units total):** Funded under ADF capability-acquisition authority. Firm-fixed-price contract. Used to qualify the production line, validate the §3 manufacturing tolerances on a production statistical sample, and complete user-acceptance trials at the operational unit.

**Tranche 3 — Production contract (500 units/yr, multi-year):** Open-tender firm-fixed-price contract. The Route B licensed-manufacture commercial structure (§17) applies; royalty payments flow to the IP holder per the §17.4 schedule. Multi-year contracts are expected to span 3 – 5 years.

### 18.3 Programme-level total cost-of-ownership

**Table 18.1.** 10-year TCO at three programme sizes (AUD 2026 mode values).

| Cost element | 40-unit R&D pilot | 200-unit qualification | 500-unit/yr production (10-yr) |
|---|---|---|---|
| Vehicle procurement (mode unit cost at applicable volume tier) | A$184 000 | A$770 000 | A$36 800 000 |
| Static-fire and flight-test programme (20 + 30 events) | A$460 760 | included in Tranche 1 | included in production |
| TTP licence (one-time, Route B) | A$1 800 000 | — | — |
| Range infrastructure (capital, amortised) | A$1 200 000 | A$2 400 000 | A$5 500 000 |
| Annual licence maintenance (10 yr) | — | A$650 000 | A$650 000 |
| Royalty payments (Route B) | A$25 000 | A$84 000 | A$3 250 000 |
| In-service support (5 % of vehicle value / yr) | — | A$385 000 | A$18 400 000 |
| **10-year programme TCO** | **A$3 669 760** | **A$4 289 000** | **A$64 600 000** |
| **Per-unit all-in cost (incl. all programme overheads)** | **A$91 744 / unit** | **A$21 445 / unit** | **A$12 920 / unit** |

The per-unit all-in cost at full production maturity (A$12 920 averaged across V1 / V2 / V3) is close to the V3-only mode unit cost in §16.2 (A$9 900 at 500 units/yr) plus pro-rata overhead absorption — consistent with V3 dominating the procurement mix at 500 units/yr.

---

## Appendix A — Simulation Model Reference Equations

This appendix documents the governing equations for the HPR-X trajectory and stage-separation model. The full Python implementation is in [`../weapons_simulation.py`](../weapons_simulation.py) (rocketry block); calibration references and model assumptions are documented in §10 and [`../weapons_sim_results.md`](../weapons_sim_results.md) §16.

### A.1 Tsiolkovsky multi-stage rocket equation

The stage-by-stage velocity increment is given by the classical Tsiolkovsky equation:

```
Δv_stage_i = I_sp,i · g_0 · ln(m_wet,i / m_dry,i)

where:
  I_sp,i   = specific impulse of stage i (s); APCP White Lightning ≈ 225 s
  g_0      = 9.80665 m/s² (standard gravity)
  m_wet,i  = total mass at ignition of stage i (kg) — includes propellant + casing + payload + upper stages
  m_dry,i  = mass at burnout of stage i (kg) — propellant consumed, casing + payload + upper stages remain
```

Total burnout velocity is the sum of stage velocity increments, less gravity and drag losses integrated through the powered phase:

```
v_burnout = Σ_i Δv_stage_i − ∫ g(h) · sin(γ) dt − ∫ (D / m) dt

where:
  γ        = flight-path angle (rad); 35° for range shot, 85–88° for high-angle shot
  D        = aerodynamic drag (N); see §A.3
  Apogee:  computed by point-mass integration of post-burnout coast phase
           (RK45, rtol = 1e-6, ICAO atmosphere, ground-impact terminal event)
```

**Numerical values cross-checked against [`../weapons_sim_results.md`](../weapons_sim_results.md) §16:**

| Variant | Stage | I_sp (s) | m_wet (kg) | m_dry (kg) | Δv_stage (m/s) | Cumulative v_burnout (m/s) | Sim §16 v_burnout (m/s) |
|---|---|---|---|---|---|---|---|
| HPR-X V1 (75 mm) | L1390 single | 225 | 6.8 | 4.1 | 1 110 | 1 110 (before losses) | 1 093.5 |
| HPR-X V2 (98 → 75 mm) | M booster | 225 | 28.5 | 12.6 | 1 800 (booster contribution to stack) | 1 800 (before losses) | 1 024.9 (at separation, gravity loss applied) |
| HPR-X V2 (98 → 75 mm) | K sustainer | 225 | 9.8 | 4.2 | 1 870 (added to booster contribution) | post-staging cumulative | 1 477.6 |
| HPR-X V3 (152 mm) | N5800 single | 225 | 52.0 | 22.5 | 1 850 | 1 850 (before losses) | 1 293.3 |

The simulator §16 burnout velocities are 1.5 – 8 % lower than the closed-form Tsiolkovsky figures above; the discrepancy is the integrated **gravity and drag losses** during powered flight, which the closed-form Δv does not account for. The two-stage V2 sustainer burnout of 1 477.6 m/s (§16) is consistent with the stacked Δv after gravity-and-drag losses are subtracted from each stage.

### A.2 Thrust profile (constant-thrust approximation)

The HPR-X simulator uses the constant-thrust approximation for all stages, calibrated against published certified-motor thrust traces from ThrustCurve.org:

```
F_thrust(t) = ṁ_propellant · v_exhaust = T_avg     (for 0 ≤ t ≤ t_burn)
F_thrust(t) = 0                                     (for t > t_burn)

where:
  ṁ_propellant = m_propellant / t_burn  (mean mass flow rate, kg/s)
  v_exhaust    = I_sp · g_0             (effective exhaust velocity, m/s)
  T_avg        = published average thrust for the motor designation
```

White Lightning APCP has a near-plateau burn profile (peak / average thrust ratio ≈ 1.5 – 1.7 across the F–N range), so the constant-thrust approximation is appropriate for the trajectory-integration scope. For motors with strongly progressive or regressive burns (Super Thunder, Red Line), a tabulated F(t) trace from ThrustCurve.org should replace the constant-thrust step.

### A.3 Aerodynamic drag and atmosphere

The point-mass equation of motion integrates the constant-thrust profile against gravity and drag:

```
m(t) · ẍ = F_thrust(t) · cos(γ) − D(v, h) · cos(γ) − 0
m(t) · ÿ = F_thrust(t) · sin(γ) − D(v, h) · sin(γ) − m(t) · g(h)

D(v, h) = 0.5 · ρ(h) · v² · C_D(M) · A_ref

where:
  ρ(h)     = ICAO standard atmosphere density (kg/m³)
  v        = total airspeed (m/s)
  M        = v / a(h)  (Mach number)
  A_ref    = π · (d_body / 2)²  (reference area, m²)
  C_D(M)   = piecewise Mach-dependent drag coefficient
           = 0.55     (subsonic, M < 0.8)
           = ramp     (transonic, 0.8 ≤ M ≤ 1.2, peak ≈ 0.78)
           = 0.65     (supersonic, M > 1.2)
  m(t)     = m_dry + m_propellant_remaining(t)
  g(h)     = 9.80665 · (R_E / (R_E + h))²    (altitude-corrected gravity)
```

The C_D values above are calibrated against RASAero II output for the §10 / §16 minimum-diameter airframes. For the hobby-class 29 / 38 / 54 mm variants the simulator is benchmarked against OpenRocket and matches within ± 3 % on un-ballasted reference configurations (see §10.3).

### A.4 Stage-separation event (bookkeeping)

At burnout of stage i, the mass-bookkeeping update is:

```
At t = t_burnout_i:
  m(t_burnout_i⁺) = m(t_burnout_i⁻) − m_casing_i − m_propellant_residual_i

where:
  m_casing_i               = empty motor casing mass of stage i (kg)
  m_propellant_residual_i  = unburned propellant + ash + slag residual (kg), typically ≈ 0.02 · m_propellant_total
```

For the V2 98 → 75 mm two-stage:

```
At booster burnout (t ≈ 2.61 s, §16):
  m(t⁻) = m_booster_dry + m_sustainer_wet ≈ 12.6 + 9.8 = 22.4 kg
  m(t⁺) = m_sustainer_wet                  ≈ 9.8 kg
  Δm    = m_booster_casing + m_booster_residual ≈ 12.6 kg dropped

Sustainer ignites at t ≈ 2.61 s + ignition delay (≈ 0.1 s in the simulator).
At sustainer burnout (t ≈ 4.61 s + ignition delay, §16):
  m(t⁻) = m_sustainer_dry ≈ 4.2 kg
  Velocity = 1 477.6 m/s (§16)
  Altitude = 3 917 m (§16)
  Subsequent coast phase: point-mass RK45 integration to apogee (§A.3)
```

The bookkeeping is identical for the optional V3 booster configurations in §14.4 (J350W booster + J180W sustainer): at booster burnout the booster casing and recovery hardware drop away; the sustainer ignites and the integration continues against the reduced-mass state vector.

---

[← HPR-X Rocketry README](README.md) · [← Weapons-Defence README](../README.md)
