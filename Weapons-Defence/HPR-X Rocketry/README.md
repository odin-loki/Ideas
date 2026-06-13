# HPR-X Series — guided high-power rocketry

> **A three-variant family of guided high-power rockets (V1 Sprint 200 mm / V2 Transonic 400 mm / V3 Supersonic 600 mm) derived from the open-source `novatic14/MANPADS` prototype. ESP32-S3 flight computer, ICM-42688-P IMU, Madgwick AHRS, cascaded PID at 500 Hz, four-canard active stabilisation during boost only. Dense nosecone lead/tungsten ballast to push ballistic coefficient to 2,520 kg/m². Long-burn White Lightning APCP (F36Z / G64W / J180W). Shallow 35–39° launch angle. Single-stage ranges 3,443 m / 3,998 m / 5,455 m on a 2D point-mass trajectory simulation; the two-stage V3-S (J350W + J180W at 28°) extends V3 to 7,916 m. Build cost AUD $195 / $520 / $1,180 from commercial hobby parts. Australian regulatory framework: TRA Level 2 + CASA waiver + state explosives storage authority required for V3.**

> **Genre note.** TRP designator and FOUO banner adopted for tonal coherence with the rest of the `Weapons-Defence/` portfolio. No real sponsorship, no real programme office, no fielded systems implied. All three variants are buildable from commercial off-the-shelf parts by an appropriately certified Tripoli Rocketry Association member operating within national regulatory frameworks.

---

## 📑 Source documents

| Document | Format | Purpose |
|---|---|---|
| [`HPR-X Series Spec.md`](HPR-X%20Series%20Spec.md) | Operator specification (TRP-2026-020) | Full three-variant spec — airframe, propulsion, recovery, avionics, launcher, ballast system, flight state machine, canard PID code reference, range / trajectory tables, motor selection rationale, payload capacity, BOM, regulatory summary, two-stage booster configurations. |
| [`Paper19_HPR-X_Guided_Rocketry.md`](Paper19_HPR-X_Guided_Rocketry.md) | Academic research paper (TRP-2026-020) | Abstract / introduction / background (HPR context and the open-source MANPADS origin) / design philosophy (BC optimisation, burn-duration-over-thrust, 35–39° launch angle, minimum-diameter airframe, canard guidance) / trajectory simulation methodology (ISA atmosphere, RASAero-II Cd table, RK45) / results (three-variant performance, ballast / angle / booster parametric sweeps) / discussion / limitations / conclusions / references. |

---

## 🎯 Headline performance — three variants side-by-side

| Parameter | **V1 Sprint** | **V2 Transonic** | **V3 Supersonic** |
|---|---|---|---|
| Diameter / length | 29 mm / 200 mm | 38 mm / 400 mm | 54 mm / 600 mm |
| Motor | Aerotech F36Z White Lightning | Aerotech G64W White Lightning | Aerotech J180W White Lightning |
| Motor class | F (138 N·s) | G (260 N·s) | J (864 N·s) |
| Burn time | 3.8 s | 4.1 s | 4.8 s |
| Launch mass | 324 g | 727 g | 1,542 g |
| Nosecone ballast | 120 g lead | 273 g lead | 700 g lead / tungsten |
| Ballistic coefficient | 830 kg/m² | 1,720 kg/m² | 2,520 kg/m² |
| Launch angle (optimal) | 35° | 39° | 35° |
| Peak Mach | 1.00 | 0.92 | 1.35 |
| Burnout altitude | 659 m | 648 m | 1,214 m |
| Peak altitude | 991 m | 1,158 m | 1,610 m |
| **Single-stage range** | **3,443 m** | **3,998 m** | **5,455 m** |
| **Best two-stage range** | **5,502 m** (V1-S, 2× G64W booster) | **7,055 m** (V2-S, I200W booster) | **7,916 m** (V3-S, J350W booster) |
| Flight computer | ESP32 + MPU-6050 | ESP32-S3 + ICM-42688-P + StratoLoggerCF | ESP32-S3 + ICM-42688-P + ADXL375 + TeleMega v6 |
| Telemetry | Optional LoRa 433 MHz | LoRa SX1276 + uBlox SAM-M10Q GPS | TeleMega 70 cm ham-band + LoRa backup + onboard uBlox |
| Recovery | Motor ejection → streamer | Dual deployment, main at 150 m AGL | Dual deployment, main at 200 m AGL |
| Build cost (AUD, excl. cert / fees) | ~$195 | ~$520 | ~$1,180 |

---







### Portfolio §23 — service intervals

| Metric | Value |
|---|---|
| Motor case life (§23) | **50 flights** |
| Nozzle insert life (§23) | **30 flights** |

Source: [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

## 🛰️ Staged-flight summary (six-state machine, identical firmware on all variants)

- **S0 PRE_LAUNCH** — IMU bias calibration (2 s), barometric ground reference, continuity check, LoRa heartbeat at 1 Hz, canards centred, two-key hardware arming.
- **S1 BOOST** — Accelerometer > 3 g for > 50 ms; PID attitude hold active from T + 0.1 s; canards ±10°; 500 Hz cascaded PID loop on FreeRTOS Core 1.
- **S2 COAST** — Acceleration < 0.5 g; canards driven to zero and held; passive tail-fin stability throughout the transonic/supersonic regime; GPS active.
- **S3 APOGEE** — Dual criteria (barometric descent AND accelerometer near-zero); pyro fires within 50 ms on V2/V3.
- **S4 DESCENT** — V2/V3 only; main chute at 150 m / 200 m AGL; GPS fix transmitted every 2 s.
- **S5 LANDED** — Barometric stabilisation; buzzer pattern; LoRa transmits landed GPS fix every 10 s for 30 min.

---

## 🚀 Validated trajectory performance — Tier-2 upscaled variants

The hobby-class numbers above (3,443 / 3,998 / 5,455 / 7,916 m) come from the Tier-1 RASAero / RK45 trajectory pipeline and apply to the 29 / 38 / 54 mm minimum-diameter airframes. Separately, the portfolio's `weapons_simulation.py` Tier-2 integrator (Tsiolkovsky thrust accounting + ICAO atmosphere; subsonic `C_d ≈ 0.55`, supersonic `0.65`) was additionally run against three larger-bore HPR-X airframes to bound the upper end of the design space. Numbers below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §16 and reflect the upscaled airframes only.

| Variant | High-angle apogee | TOF | 35° max range | 35° apogee | Burnout (high-angle) |
|---|---|---|---|---|---|
| HPR-X V1 (civ-amateur, 75 mm, L1390) | 5,782 m | 73.7 s | 6,408 m | 2,147 m | 1,093.5 m/s @ 1,209 m @ 2.11 s |
| HPR-X V2 (two-stage 98 → 75 mm, M+K) | 7,914 m | 99.7 s | 7,342 m | 2,901 m | M booster 1,024.9 m/s @ 1,384 m @ 2.61 s · K sustainer 1,477.6 m/s @ 3,917 m @ 4.61 s |
| HPR-X V3 (152 mm SOF spotter, N5800) | 2,523 m (35°) | 45.4 s (35°) | 6,502 m | 2,523 m | 1,293.3 m/s @ 1,221 m @ 3.21 s |

The 75 mm V1 and 152 mm V3 single-stage airframes both reach burnout in the Mach 3+ regime; the 98 → 75 mm two-stage V2 reaches Mach 4.3 at sustainer burnout. The Tier-2 numbers cross-check against the Tier-1 RASAero / RK45 hobby-airframe outputs to within 3 % on the un-ballasted reference configurations.

---

## 🔬 Simulation verification

Portfolio **§16** (Tsiolkovsky thrust + ICAO atmosphere trajectory integrator) validates the Tier-2 upscaled HPR-X variants. Re-run the local verification slice:

```bash
python platform_simulation.py
```

The script prints **PASS/FAIL** checks; headline anchor: **HPR-X V3 @ 35° launch angle → 6,502 m range** (152 mm SOF spotter, N5800 motor).

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Local §16 rocketry verification slice |
| [`SIM_README.md`](SIM_README.md) | Tier-1 vs Tier-2 airframe mapping, integrator keys |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative §16 tabulated output |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

Tier-1 hobby-airframe numbers (3,443 / 3,998 / 5,455 m) come from the spec's RASAero / RK45 pipeline — not from §16. To regenerate the **full portfolio**:

```bash
cd ..
python weapons_simulation.py
```

---

## 🚀 Quick start (simulator)

**From this folder** — verify §16 rocketry claims:

```bash
python platform_simulation.py
```

**Regenerate full portfolio:**

```bash
cd ../..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for Tier-1 vs Tier-2 airframe mapping.

---

## ⚖️ Regulatory framework (Australia)

- **V1 (F class).** No TRA certification required. Notify CASA only if flight exceeds 400 ft AGL. State APCP explosives licence often exempt for F-class. Personal liability insurance recommended.
- **V2 (G class).** TRA Level 1 recommended. CASA notification for any flight above 400 ft AGL. State APCP licensing borderline — check your jurisdiction.
- **V3 (J class).** **TRA Level 2 certification required.** CASA site waiver required for any flight to the headline 5,455 m / 7,916 m altitudes. J-class APCP (864 N·s) is explicitly within the regulated explosive regime in all Australian states — state-issued storage and use authority is mandatory before purchasing J-class reloads. Minimum site waiver 2,000 m AGL for a 35° range flight.

---

## 🚧 Honest framing

- **The HPR-X Series is open-source-derived.** The guidance pipeline (ESP32 + IMU + Madgwick AHRS + cascaded PID + four-canard mixing) is a direct re-implementation of the `novatic14/MANPADS-System-Launcher-and-Rocket` GitHub project at higher flight rate. The contribution of HPR-X is the trajectory-simulation-driven design space (ballast mass, launch angle, motor selection, two-stage booster matching), not the closed-loop guidance.
- **The trajectory simulation is 2D point-mass, not 6-DOF.** The headline range figures (3,443 / 3,998 / 5,455 / 7,916 m) come from a Python `scipy.integrate.solve_ivp` RK45 simulation with ISA atmosphere and a RASAero-II-derived Mach-dependent Cd table. The point-mass simplification neglects body-axis attitude dynamics during coast; passive stability margin (1.8–2.8 cal) justifies the simplification but a true 6-DOF run in OpenRocket or RASAero II should be the verification step before flight.
- **Tripoli L2 certification is required to actually fly V3.** A J-class motor in an HPR airframe is not a build-and-fly project — TRA L2 certification (a written test, a witnessed L1 flight, and a witnessed L2 flight) is mandatory at every Tripoli-sanctioned site, and the V3 design assumes the operator already holds L2.
- **J-class APCP is a regulated explosive in all Australian states.** The Dangerous Goods Act in each state requires a storage and use authority before a J-class reload can be purchased or held. Penalties for unlicensed possession are substantial. Check your state's regime before purchasing.
- **No flight-test validation.** The range figures are simulation outputs. The headline 5,455 m for V3 has not been demonstrated by the author in a real flight; it is a design-target derived from the trajectory simulation. The simulation has been cross-checked against OpenRocket and RASAero II for the un-ballasted reference configurations and matches to within ~3 %, but a full flight-test programme is the open verification step.
- **No fin-flutter modal analysis is provided.** Fin sizing is from the nakka-rocketry.net flutter calculator with a 1.5× safety margin at the headline burnout Mach number. V3 transits Mach 1.35 single-stage and Mach 1.76 in the V3-S staged configuration — fin flutter is a real failure mode in this regime and a dedicated modal analysis is open future work.

---

## 🔗 Related work in this repo

- [`../Military Noise Cancellation/`](../Military%20Noise%20Cancellation/) — TACS (Tactical Acoustic Cancellation System) for launch-site signature management.
- [`../CL-20 High Explosive/`](../CL-20%20High%20Explosive/) — companion energetic-materials portfolio (proteinated CL-20 safe-handling explosive).
- [`../Caseless Bullets/`](../Caseless%20Bullets/) — caseless / cartridgeless propulsion work, adjacent propellant chemistry.
- [`../../Rockwell 50 to 70 Carbide/`](../../Rockwell%2050%20to%2070%20Carbide/) — sovereign manufacturing context for motor casings and airframe metallics.

---

[← Back to Weapons-Defence README](../README.md)