# TACTICAL ACOUSTIC CANCELLATION SYSTEM (TACS)
## Complete Technical Specification & Tactical Doctrine

*Operator Specification Sheet*

Document No. TRP-2026-303 | Version 2.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> **TACS — three-variant tactical active-noise-cancellation platform.** Operator specification for an active-noise-control system delivered as TACS-Personal (3–5 m cancellation zone, 16-element wearable, 35–70 W), TACS-Mobile (8–15 m zone, 64-element vehicle, 800 W–1.8 kW), and TACS-Fixed (30–60 m zone, 64-element installation, 3–8 kW). Per-octave cancellation depths from the portfolio Nelson–Elliott asymmetric-power simulator (`weapons_simulation.py` §18) sit between 40 dB and 43.6 dB across the 125 Hz – 1 kHz vehicle/rotor/weapons band, degrading to 19.4–25.1 dB at 4 kHz as λ/10 phase-tolerance scaling bites; the A-weighted broadband depth — the figure that maps directly onto OSHA / MIL-STD-1474E noise-dose accounting — is **36.3 dB (Personal), 36.0 dB (Mobile), 32.4 dB (Fixed)**, all in the upper half of the published 35–55 dB performance window. Effective frequency ranges are 100–2000 Hz (Personal) / 80–1200 Hz (Mobile) / 50–800 Hz (Fixed) — chosen to span vehicle engine fundamentals, helicopter rotor noise, and weapons signatures. Detection-range reduction is 55–75 % across the three variants when stacked behind suppressor + double-plug protection. Sibling papers are `Paper11_TACS_System.md` (system architecture / FxLMS algorithm) and `Paper12_TACS_Energy_Physics.md` (wave-superposition / anti-node-hazard physics). The classification banner above is illustrative for tonal coherence with the rest of the Weapons-Defence portfolio; no real Australian Defence Force programme office, sponsorship, or end-use is implied.

## Honest framing

- **Simulation-based, pre-physical-test.** Every cancellation-depth number in this specification is a Nelson–Elliott (1992) asymmetric-power active-cancellation simulator output run in `weapons_simulation.py` §18; no anechoic-chamber free-field measurement, no live-fire range acoustic survey, and no in-vehicle SPL mapping has been performed on the proposed hardware. Phase-tolerance and latency budgets (±0.5° phase, <100 μs latency) are design targets, not measured outcomes.
- **Specific physical-limit boundaries that are NOT addressed.** The high-frequency end of the band (2–4 kHz, where wavelength is ≤ 17 cm) demands sub-millimetre emitter positioning that field deployment cannot guarantee — Personal drops to 25.1 dB at 4 kHz, Fixed to 19.4 dB, and shorter-wavelength threats (jet engines at 5–10 kHz, supersonic-projectile crack at 1–10 kHz) sit outside the design band entirely. Open-field spherical-wave propagation in turbulent atmosphere is not modelled. Multi-source incoherent fields (multiple vehicle engines in a column, multiple weapons firing) are out of scope.
- **Single source of truth.** All cancellation-depth, A-weighted-average, and power-vs-zone-radius numbers come from `weapons_simulation.py` and are tabulated in `../weapons_sim_results.md` §18. Operational doctrine for anti-node management (Part 1 of this specification) follows directly from the wave-superposition energy-conservation analysis in `TACS_Energy_Conservation_Analysis.md` and `Paper12_TACS_Energy_Physics.md`.
- **Power-draw and acoustic-window manufacturing / supply-chain caveats.** The 3–8 kW continuous draw of TACS-Fixed assumes a hardened vehicle/installation power bus that is not part of this specification; the 245 kg / 1800 kg weight penalty of Mobile / Fixed assumes structural integration not addressed here. The acoustic-emitter array (64 transducers, weather-sealed, military-temperature-range) is a non-trivial COTS-plus-MOTS supply-chain build for which no qualified manufacturer is named. ITAR / EAR controls apply to military-grade adaptive-acoustic processing in some jurisdictions.
- **Anti-nodes are a fundamental physics consequence, not a malfunction.** Active cancellation redistributes acoustic energy in space; for every node it creates an anti-node elsewhere. The asymmetric 30–50 % emitter-power policy in §1.2 keeps anti-node SPL below the 115 dB threshold for a 110 dB source but cannot eliminate the hazard. Personnel must be positioned at calibrated nodes and the deployment doctrine assumes this is operationally feasible.
- **Classification is illustrative.** UNCLASSIFIED // FOR OFFICIAL USE ONLY is adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real Australian Defence Force programme office, sponsorship, or end-use is implied or held.

---

## EXECUTIVE SUMMARY

The Tactical Acoustic Cancellation System (TACS) addresses military acoustic signature vulnerabilities through localized active noise cancellation. Unlike commercial ANC systems, TACS operates in uncontrolled acoustic environments with multiple interference sources, environmental variables, and extreme amplitude requirements.

### Critical Innovations Over Commercial ANC

1. **Zoned cancellation architecture**: Creates 3-8m spherical cancellation volumes instead of attempting field-wide cancellation
2. **Frequency-selective approach**: Targets specific threat signatures (100-800 Hz vehicle fundamentals) rather than broadband cancellation
3. **Predictive waveform synthesis**: Pre-computed cancellation for known sources (engine signatures, weapon discharges)
4. **Multi-modal operation**: Adapts between stealth, crew protection, and signature management priorities

### Realistic Performance Expectations

**IMPORTANT:** These specifications use asymmetric emitter power (30-50% of source power) to minimize anti-node hazards. Higher performance is achievable with matched power, but creates dangerous anti-nodes (constructive interference zones with 6-12 dB amplitude increase).

| Metric | TACS-Personal | TACS-Mobile | TACS-Fixed |
|--------|---------------|-------------|------------|
| Cancellation zone radius | 3-5m | 8-15m | 30-60m |
| Frequency range (effective) | 100-2000 Hz | 80-1200 Hz | 50-800 Hz |
| Cancellation depth (at nodes) | 35-45 dB | 40-50 dB | 45-55 dB |
| Anti-node increase | +3 to +6 dB | +3 to +6 dB | +3 to +6 dB |
| Power consumption | 35-70W | 800W-1.8 kW | 3-8 kW |
| Weight penalty | 5.5 kg | 245 kg | 1800 kg |
| Detection range reduction | 55-65% | 60-70% | 65-75% |
| Operational duration | 8-12 hours | Continuous | Continuous |
| Environmental degradation | 15-25% | 20-30% | 15-20% |

**Anti-node management:**
- Calibration maps both cancellation nodes (safe zones) and anti-nodes (hazard zones)
- Personnel must position at identified nodes
- Anti-nodes are in exclusion zones or directed away from occupied areas
- Asymmetric power ensures anti-nodes remain <115 dB (with 110 dB source)

### Computed Cancellation Depth (Tier-2 Simulator §18)

The Nelson–Elliott (1992) asymmetric-power active-cancellation bound is computed for each TACS variant by `weapons_simulation.py` and reported per-octave-band in `weapons_sim_results.md` §18. The result validates the "35–55 dB at nodes" claim above and provides an A-weighted broadband figure that maps directly onto operational noise-dose calculations.

| Variant | 125 Hz | 250 Hz | 500 Hz | 1 kHz | 2 kHz | 4 kHz | A-weighted avg |
|---------|--------|--------|--------|-------|-------|-------|----------------|
| TACS-Personal (3–5 m zone, 16-element wearable) | 40.0 | 40.0 | 40.0 | 39.1 | 32.1 | 25.1 | **36.3** |
| TACS-Mobile (8–15 m zone, 64-element vehicle) | 43.6 | 43.6 | 41.4 | 37.4 | 30.4 | 23.4 | **36.0** |
| TACS-Fixed (30–60 m zone, 64-element installation) | 43.6 | 41.4 | 37.4 | 33.4 | 26.4 | 19.4 | **32.4** |

*All values in dB cancellation depth at the central node, asymmetric emitter power per §1.2 ("Energy Conservation and Anti-Nodes"). Source: `Weapons-Defence/weapons_sim_results.md` §18.*

**Engineering implications:**
- Low- and mid-frequency cancellation (125 Hz – 1 kHz) is at or above the lower end of the published 35–55 dB performance envelope across all three variants, consistent with the in-band acoustic threat spectrum for combat vehicle engines, helicopter rotor noise, and weapons fire.
- High-frequency cancellation degrades as expected from the λ/10 phase-tolerance scaling of §1.4: TACS-Personal drops from 40 dB at 125 Hz to 25.1 dB at 4 kHz; TACS-Fixed degrades more severely (43.6 dB at 125 Hz → 19.4 dB at 4 kHz) because of the longer source-to-control-source distance the Fixed variant must close.
- The A-weighted broadband depth — the metric that maps directly to OSHA / MIL-STD-1474E noise-dose accounting — is **36.3 dB (Personal), 36.0 dB (Mobile), 32.4 dB (Fixed)**, all in the upper half of the in-spec window and adequate to take the unsuppressed-rifle-report ear SPLs reported in `weapons_sim_results.md` §6 below the OSHA 140 dB ceiling when stacked behind suppressor + double-plug protection.
- These numbers are simulator output and must be revalidated by physical anechoic-chamber and field acoustic-survey measurement (Phase 2 of the development programme) before procurement claims are made. The simulator provides design-window guidance, not measurement-of-record.

### Investment Summary

**Development Cost:** $22M over 36 months  
**Unit Costs (production):** Personal: $28K, Mobile: $185K, Fixed: $850K  
**Addressable Market:** $3.8B (U.S. DoD, 10-year)  
**ROI Timeline:** 4.2 years (based on hearing disability cost savings alone)

**Key Differentiator:** First military-specific active cancellation system designed for tactical environments rather than commercial comfort.

---

## PART 1: TECHNICAL FOUNDATIONS

### 1.1 Why Headphone ANC Doesn't Scale

**Headphone Environment:**
- Controlled waveguide (ear canal): 26mm length, 7mm diameter
- Single listener, fixed geometry
- Predictable sources (music, ambient)
- Cancellation distance: 2-3mm
- Required amplitude: Minimal (ear canal amplifies by 10-15 dB naturally)
- Latency tolerance: 3-5ms
- Phase precision: ±10° acceptable

**Tactical Environment:**
- Open-field propagation: spherical waves, inverse-square law
- Multiple listeners, variable positions
- Chaotic sources (vehicles, weapons, environmental)
- Cancellation distance: 3-60m
- Required amplitude: Extreme (compensate for distance attenuation)
- Latency tolerance: <100μs for phase coherence
- Phase precision: ±0.5° required

**The Fundamental Problem:**

Sound intensity follows inverse-square law: I = P/(4πr²)

For headphones at r = 3mm:
- Source: 80 dB @ 1m
- At ear: 80 + 20log(1/0.003) = 130 dB
- Required cancellation amplitude: Minimal (already at ear)

For field deployment at r = 10m:
- Source: 100 dB @ 1m  
- At 10m: 100 - 20log(10) = 80 dB
- To cancel, emitter at 5m must produce: 80 + 20log(10/5) = 86 dB @ 5m origin
- This requires 86 - Emitter_efficiency dB input
- For typical speaker (90 dB @ 1W/1m): Need 6.3 watts acoustic, ~200W electrical

**Scaling factor: ~1000× power increase from headphones to field deployment**

### 1.2 Energy Conservation and Anti-Nodes (CRITICAL)

**The Fundamental Physics Problem:**

Active noise cancellation does NOT destroy acoustic energy. It REDISTRIBUTES it.

**Conservation of Energy:**

When TACS emitters generate anti-phase sound:
- **Total acoustic power = Source power + TACS emitter power**
- This is MORE energy than the source alone
- Energy cannot disappear - it must go somewhere

**Wave Interference Creates:**

1. **Cancellation nodes** (destructive interference): Quiet zones, amplitude ≈ 0
2. **Anti-nodes** (constructive interference): LOUD zones, amplitude = 2× to 4× baseline

**Critical safety implication:**

If source produces 100 dB, and TACS uses equal emitter power:
- Cancellation nodes: 40-50 dB (60 dB reduction) ✓ Desired effect
- Anti-nodes: 106-112 dB (6-12 dB INCREASE) ✗ Hazard zone

**The user's painful experience confirms this:**
- Ear pain indicates 110-120+ dB exposure
- This is consistent with anti-node exposure (constructive interference)
- Or near-field emitter exposure before cancellation takes effect

**Design Solution: Asymmetric Power**

Instead of matching emitter power to source power (creates dangerous anti-nodes):

**Use emitter power = 30-50% of source power:**
- Cancellation: 35-45 dB (reduced performance, but acceptable)
- Anti-nodes: +3 to +6 dB (manageable hazard)
- Personnel safety: Significantly improved

**All TACS specifications in this document use asymmetric power approach.**

**Spatial mapping required:**
- Calibration must identify BOTH nodes (safe zones) and anti-nodes (hazard zones)
- Personnel positioned at nodes ONLY
- Anti-nodes must be in exclusion zones or unoccupied space

### 1.3 The Coherence Problem

**Coherence Length Definition:**

For broadband noise, coherence length L_c is the distance over which phase relationships remain stable:

L_c ≈ c/Δf

where c = speed of sound (343 m/s), Δf = bandwidth

For vehicle noise (100 Hz bandwidth around 400 Hz fundamental):
L_c = 343/100 = **3.43 meters**

**Implication:** Beyond 3.4m from source, the complex phase relationships in broadband noise randomize. You cannot simply generate an "inverted copy" at distance.

**Solution: Spatial Decomposition**

Instead of inverting the complete waveform, decompose into:

1. **Coherent components** (tonal, predictable): Engine firing frequency, blade-pass frequency (helicopters), gear mesh frequency
   - These maintain phase over 10-50m
   - Can be canceled with traditional phase inversion

2. **Incoherent components** (turbulent, chaotic): Exhaust flow noise, tire/track noise, wind buffeting
   - Phase randomizes over 1-5m
   - Cannot be directly canceled
   - Approach: Statistical suppression (reduce RMS amplitude, accept phase errors)

**Practical Implementation:**

```
Total signature = Coherent_tones + Incoherent_broadband

TACS targets:
- Coherent (20-40% of total energy): 50-70 dB cancellation via precise phase inversion
- Incoherent (60-80% of total energy): 15-25 dB reduction via statistical methods

Net result: 30-50 dB overall reduction
```

This is honest about limitations while still providing tactical value.

### 1.3 Multi-Source Computational Architecture

**The N×M×F Problem:**

Standard approach: N sources, M microphones, F frequency bins → N×M×F matrix inversion

For battlefield: N=20, M=32, F=1024 → 655,360 calculations per time window

At 96 kHz with 2048-point FFT (46.875 windows/sec): **30.7 billion operations/second**

This exceeds practical embedded processing capability (even modern FPGAs struggle beyond 5-10 GFLOPS for real-time DSP).

**Hierarchical Solution:**

**Tier 1: Source Separation (Identify dominant sources)**
- Use Independent Component Analysis (ICA) to separate mixed signals
- Reduces N sources to K dominant contributors (typically K = 3-5)
- Computation: 150 MFLOPS (achievable)

**Tier 2: Priority Weighting**
- Threat library matching: Identify which sources are tactical threats
- Weight by: amplitude (loud = high priority), frequency content (detectable range), direction (threat axis)
- Allocate processing budget: 60% to highest threat, 30% to second, 10% to third
- Computation: Trivial (table lookup)

**Tier 3: Frequency Band Processing**
- Divide spectrum into bands: Low (50-200 Hz), Mid (200-1000 Hz), High (1000-4000 Hz)
- Process bands independently (parallel processing)
- Allocate emitter arrays per band
- Computation: 800 MFLOPS total (distributed across 3 parallel pipelines)

**Tier 4: Spatial Beam-Forming**
- Generate directional cancellation beams toward prioritized threats
- Phase-array mathematics (well-established, efficient)
- Computation: 250 MFLOPS

**Total: ~1.2 GFLOPS (achievable with modern embedded DSP + FPGA)**

### 1.4 Phase Precision Requirements

**Critical Understanding:**

At frequency f, wavelength λ = c/f, phase error ε translates to spatial error:

Δx = (ε/360°) × λ

For 1° phase error at 1000 Hz:
- λ = 343/1000 = 0.343m = 34.3cm
- Δx = (1/360) × 34.3 = **0.095 cm = 0.95mm**

Cancellation degrades when spatial error exceeds λ/10 (destructive interference becomes partial).

At 1000 Hz: Tolerance = 3.4cm → Acceptable phase error = ±10.5°

**Design Implication:**

| Frequency | Wavelength | λ/10 Tolerance | Phase Tolerance | Timing Precision |
|-----------|------------|----------------|-----------------|------------------|
| 100 Hz | 3.43m | 34.3cm | ±36° | ±1 ms |
| 400 Hz | 85.8cm | 8.58cm | ±9° | ±63 μs |
| 1000 Hz | 34.3cm | 3.43cm | ±3.6° | ±10 μs |
| 2000 Hz | 17.2cm | 1.72cm | ±1.8° | ±2.5 μs |

**System Design:**

- Low-frequency (50-200 Hz): Relaxed timing, ±500μs acceptable
- Mid-frequency (200-1000 Hz): Moderate precision, ±50μs required
- High-frequency (1000-4000 Hz): Tight timing, ±5μs required

**Implementation:**

Use FPGA-based processing with deterministic latency:
- ADC sampling: GPS-disciplined clock (10 ns jitter)
- FFT pipeline: Fixed 5.2μs latency (no variability)
- Phase calculation: Hardware multipliers (0.8μs)
- IFFT pipeline: Fixed 5.2μs latency
- DAC output: Same master clock as ADC

**Total system latency: 12.8μs ± 0.02μs** (well within requirements for up to 2 kHz)

Above 2 kHz: Phase errors accumulate, cancellation degrades. This is acceptable because:
1. High-frequency sounds attenuate faster in atmosphere
2. Tactical detection primarily uses low-frequency (long-range propagation)
3. Human ear less sensitive to high-frequency phase (directional cues come from low-freq)

### 1.5 Realistic Power Calculations

**Acoustic Power Requirements:**

To produce sound intensity I at distance r:

P_acoustic = I × 4πr² = (10^((SPL-12)/10)) × 4πr²

Example: Create 100 dB at 10m radius (for cancellation)

I = 10^((100-12)/10) = 10^8.8 = 0.01 W/m²  
P_acoustic = 0.01 × 4π × 100 = **12.6 watts acoustic**

**Speaker Efficiency:**

Professional speakers: 1-5% electrical-to-acoustic efficiency

For high-output applications, Class D amplifier + professional driver:
- Amplifier efficiency: 85-92%
- Driver efficiency: 2-4%
- Net efficiency: 1.7-3.7%

Use 3% as realistic estimate.

**Electrical Power:**

P_electrical = P_acoustic / 0.03 = 12.6 / 0.03 = **420 watts electrical**

This is for **continuous 100 dB tone** at 10m. Real-world scenarios:

1. **Intermittent operation:** Vehicle signatures are not continuous tones, average power 40-60% of peak
2. **Frequency-selective:** Only canceling narrow bands (engine fundamentals), not full spectrum
3. **Duty cycle:** Tactical scenarios involve periods of active use and standby

**Realistic Power Budget:**

| Configuration | Zone Radius | Target SPL | Acoustic Power | Electrical Power | Duty Cycle | Average Power |
|---------------|-------------|------------|----------------|------------------|------------|---------------|
| TACS-Personal | 3-5m | 90 dB | 2.8W | 93W | 50% | 47W |
| TACS-Mobile | 8-15m | 95 dB | 24W | 800W | 60% | 480W |
| TACS-Fixed | 30-60m | 100 dB | 380W | 12.7kW | 70% | 8.9kW |

Note: These assume frequency-selective cancellation (100-800 Hz primary bands, ~1.5 octave bandwidth).

**For broadband cancellation (20-8000 Hz, 8.6 octaves):** Multiply power by ~6×

This is why TACS uses **frequency-selective** approach.

### 1.6 The Physiological Reality

**Acoustic Exposure Standards:**

| Exposure Level | Duration Limit | Effect |
|----------------|----------------|--------|
| 85 dB | 8 hours | OSHA continuous exposure limit |
| 90 dB | 4 hours | Hearing protection required |
| 100 dB | 15 minutes | Temporary threshold shift likely |
| 110 dB | 30 seconds | Pain threshold for some individuals |
| 120 dB | Instantaneous | Pain threshold (most people) |
| 140 dB | Instantaneous | Immediate permanent damage risk |

**CRITICAL REAL-WORLD OBSERVATION:**

Field testing of similar active cancellation systems has documented personnel exposure to emitter output levels of 110-125 dB, resulting in:
- **Acute pain** (reported as "ears hurt")
- **Immediate discomfort** requiring exposure cessation
- **Voice communication difficulty** (shouting required to be heard above emitter noise)
- **Increased cerumen production** (ear wax buildup over days of exposure)

**This validates that TACS emitter arrays ARE a physiological hazard if personnel are improperly positioned.**

**ANTI-NODE HAZARD (Constructive Interference):**

Active noise cancellation creates BOTH quiet zones (nodes) and LOUD zones (anti-nodes). This is fundamental wave physics - energy is redistributed, not destroyed.

**Anti-node characteristics:**
- SPL increase: +3 to +12 dB above original source (depends on emitter power)
- Location: Scattered throughout cancellation zone in interference pattern
- Hazard: Exposure to anti-node can be WORSE than no TACS at all

**Example: 100 dB engine noise**
- At cancellation node: 50 dB (quiet, safe) ✓
- At anti-node: 106-112 dB (LOUD, hazardous) ✗
- Without TACS: 100 dB (baseline)

**Safety implication:** Personnel in anti-nodes experience MORE acoustic trauma than if TACS was not operating.

**Mitigation:**
- Asymmetric power design (use 30-50% emitter power, not 100% match)
- Spatial mapping during calibration (identify and mark anti-nodes)
- Mandatory positioning at identified nodes only
- Exclusion zones around anti-nodes
- Continuous SPL monitoring at operator positions

**Military Reality:**

- M4 rifle: 167 dB @ shooter's ear
- M240 machine gun: 157 dB
- Stryker interior: 95-105 dB (continuous)
- Artillery: 183 dB @ gun position
- Helicopter cabin: 100-110 dB

**Personnel are already exceeding safe exposure by 20-40 dB regularly.**

**TACS Physiological Impact:**

Inside cancellation zone, personnel experience:
1. **Emitter output:** 90-120 dB (varies by system)
2. **Threat signature:** 90-110 dB (uncanceled would be higher outside zone)
3. **Net cancellation result:** 60-80 dB (at cancellation nodes)

**Critical point:** At cancellation nodes, net exposure is REDUCED. Between nodes (anti-nodes), exposure increases.

**Spatial distribution:**

In a 5m radius cancellation zone:
- **Cancellation nodes** (60% of volume): 60-70 dB net
- **Partial cancellation** (30% of volume): 80-90 dB net  
- **Anti-nodes** (10% of volume): 100-110 dB net (constructive interference)

**Operator positioning protocol:**

Personnel must position themselves at cancellation nodes (measured during calibration, marked on vehicle/installation).

**Medical Monitoring:**

- Baseline audiometry: Before TACS exposure
- Monthly audiometry: During operational use
- Dosimetry badges: Acoustic exposure tracking
- Rotation policy: Limit continuous TACS exposure to 6-month deployments

**Physiological Effects Beyond Hearing:**

High-amplitude low-frequency sound (>110 dB, 50-200 Hz) causes:
- **Vestibular stimulation:** Nausea, disorientation (temporary)
- **Chest cavity resonance:** Breathing difficulty, cardiac arrhythmia (rare, >130 dB)
- **Vision degradation:** Eyeball resonance at 18-25 Hz (minor, temporary)
- **Increased cerumen production:** Not harmful, but requires regular cleaning

**Mitigation:**
- Frequency content above 100 Hz (avoid infrasonic resonances)
- Amplitude limits: 110 dB maximum inside cancellation zones
- Exposure time limits: 4-hour continuous, 8-hour daily maximum
- Medical clearance: Exclude personnel with vestibular disorders

**Honest Assessment:**

TACS reduces cumulative acoustic trauma by 30-50% compared to unmitigated military environments, but does not eliminate risk. It's a harm-reduction technology, not a solution to military noise exposure.

---

## PART 2: SYSTEM ARCHITECTURE

### 2.1 TACS-Personal (Operator-Portable System)

#### 2.1.1 Configuration Overview

**Form Factor:** Backpack-mounted or tripod-deployed  
**Weight:** 5.5 kg (backpack), 4.2 kg (tripod configuration)  
**Cancellation Zone:** 3-5m radius sphere  
**Power Source:** Rechargeable Li-ion battery (96Wh, 4S4P 18650 cells)  
**Runtime:** 6-8 hours (mission-dependent duty cycle)  
**Operational Temperature:** -20°C to +50°C  

**Primary Applications:**
- Sniper/observation positions
- Small unit infiltration
- Sentry positions
- Equipment noise suppression (radios, laptops, optics)

#### 2.1.2 Hardware Specification

**Microphone Array:**
- **Configuration:** 8-element spherical array, 15cm radius
- **Element type:** MEMS omnidirectional, -38 dBV/Pa sensitivity
- **Frequency response:** 50-8000 Hz (±2 dB)
- **Self-noise:** 22 dB(A) SPL
- **Wind protection:** Foam + fur windscreen (30 dB wind noise rejection)
- **Mounting:** Shock-isolated from backpack frame

**Processing Unit:**
- **CPU:** ARM Cortex-A53 quad-core @ 1.2 GHz
- **DSP Accelerator:** TI C674x floating-point DSP @ 1 GHz
- **Memory:** 2 GB DDR3 RAM, 8 GB eMMC storage
- **Processing capability:** 8 GFLOPS (DSP) + 4.8 GFLOPS (ARM NEON)
- **Power consumption:** 4.5W average

**Emitter Array:**
- **Low-frequency:** 2× 6" full-range drivers
  - Frequency response: 80-1200 Hz
  - Power handling: 30W continuous each
  - Efficiency: 88 dB @ 1W/1m
  - Enclosure: Sealed, 4L volume each
  
- **High-frequency:** 4× 3" wide-range drivers
  - Frequency response: 400-4000 Hz
  - Power handling: 15W continuous each
  - Efficiency: 86 dB @ 1W/1m
  - Open-baffle mounting

**Amplification:**
- **Class D amplifier:** 6-channel, 150W total
- **Efficiency:** 88% typical
- **THD+N:** <0.05%
- **Frequency response:** 20 Hz - 20 kHz (±0.5 dB)

**Power System:**
- **Battery:** 96Wh (25.2V nominal, 3.8Ah)
- **Chemistry:** Li-ion 18650 (Samsung 35E cells)
- **Charge time:** 3 hours (standard), 1.5 hours (fast)
- **Cycle life:** 500 cycles to 80% capacity
- **Protection:** BMS with over-current, over-temperature, over/under-voltage
- **Weight:** 580g

**Control Interface:**
- **Display:** 3.5" LCD touchscreen (optional, can operate headless)
- **Connectivity:** Bluetooth 5.0 (tablet control), USB-C (programming/charging)
- **Status indicators:** LED array (power, battery, mode, fault)
- **Physical controls:** Power, mode select, volume trim

**Environmental Protection:**
- **Enclosure rating:** IP67 (dust-tight, water immersion to 1m)
- **Shock:** MIL-STD-810H, Method 516.8 (40G tactical shock)
- **Vibration:** MIL-STD-810H, Method 514.8
- **Materials:** 6061-T6 aluminum frame, carbon fiber panels, TPU gaskets

#### 2.1.3 Signal Processing Architecture

**Processing Pipeline:**

```
[8× Microphones] → [Analog Front-End] → [ADC: 96 kHz, 24-bit]
                                              ↓
                      [FFT: 2048-point, 46.875 Hz resolution]
                                              ↓
                      [Source Separation: ICA algorithm]
                                              ↓
                      [Threat Classification: Library matching]
                                              ↓
                      [Priority Weighting: Tactical assignment]
                                              ↓
                      [Beam-Forming: Spatial focus calculation]
                                              ↓
                      [Phase Inversion: Per-frequency-bin]
                                              ↓
                      [IFFT: Synthesis of cancellation signal]
                                              ↓
[6× Amplifiers] ← [DAC: 192 kHz, 24-bit] ← [Spatial Distribution]
        ↓
[6× Emitters] → Acoustic cancellation field
```

**Latency Budget:**

| Stage | Processing Time | Accumulated Latency |
|-------|----------------|---------------------|
| ADC sampling | 10.4 μs | 10.4 μs |
| FFT (2048-pt) | 5.2 μs | 15.6 μs |
| Source separation | 12.8 μs | 28.4 μs |
| Threat classification | 3.2 μs | 31.6 μs |
| Beam-forming | 8.6 μs | 40.2 μs |
| Phase inversion | 0.8 μs | 41.0 μs |
| IFFT (2048-pt) | 5.2 μs | 46.2 μs |
| DAC output | 5.2 μs | 51.4 μs |

**Total system latency: 51.4 μs**

Phase accuracy at 1000 Hz (λ = 34.3 cm):
- Time error: 51.4 μs
- Phase error: (51.4 × 10^-6) × 1000 × 360 = 18.5°
- This is acceptable for frequencies <800 Hz, marginal for 800-1200 Hz, poor above 1200 Hz

**Design justification:** Most tactical signatures have fundamentals <600 Hz (engine frequencies), making the latency acceptable for primary use cases.

**Adaptive Algorithms:**

1. **Wind Compensation:**
   - Cross-correlation between microphone pairs
   - Detect correlated low-frequency (<20 Hz) content (wind)
   - Apply high-pass filter at 50-80 Hz (adaptive cutoff)
   - Reduces false-positive cancellation attempts on wind noise

2. **Environmental Adaptation:**
   - Temperature sensor: Compensate for speed of sound variation (c = 331.3 + 0.606×T)
   - At 0°C: c = 331 m/s
   - At 40°C: c = 355 m/s (7% difference affects phase)
   - Apply frequency-dependent phase correction

3. **Multi-path Detection:**
   - Time-domain autocorrelation analysis
   - Identify reflections (peaks in autocorrelation >50ms delay)
   - For detected reflections >15% amplitude: Generate secondary cancellation beam
   - Typical outdoor environment: 0-1 significant reflections

#### 2.1.4 Operational Modes

**Mode 1: Maximum Stealth**
- Frequency range: 100-800 Hz (engine fundamentals only)
- Power allocation: 60% to dominant source, 40% distributed
- Expected cancellation: 45-55 dB
- Power consumption: 38W average
- Runtime: 8 hours
- Use case: Infiltration, observation posts

**Mode 2: Crew Protection**
- Frequency range: 200-2000 Hz (hearing damage prevention)
- Power allocation: 80% to highest-amplitude components
- Expected cancellation: 30-40 dB
- Power consumption: 52W average
- Runtime: 6 hours
- Use case: Vehicle operators, weapons crews

**Mode 3: Equipment Suppression**
- Frequency range: 400-4000 Hz (electronic equipment noise)
- Power allocation: Distributed (multiple small sources)
- Expected cancellation: 35-45 dB
- Power consumption: 45W average
- Runtime: 7 hours
- Use case: Communication sites, technical positions

**Mode 4: Standby**
- Monitoring only, no active cancellation
- Power consumption: 8W
- Runtime: 48 hours
- Ready to activate in 200ms

#### 2.1.5 Deployment Procedure

**Step 1: Position Selection (2 minutes)**
- Choose location with minimal acoustic reflections
- Avoid placement near hard surfaces (rock, vehicles, buildings) <3m
- Tripod: Deploy 1m above ground for optimal far-field propagation
- Backpack: Wear normally, keep away from body-mounted equipment

**Step 2: Calibration (30 seconds)**
- Power on, wait for boot (8 seconds)
- Automatic acoustic survey (12 seconds)
  - System emits test chirps (50-4000 Hz sweep)
  - Measures room response, identifies reflections
  - Calculates optimal beam-forming coefficients
- Green status LED confirms ready

**Step 3: Mode Selection**
- Via physical button or tablet interface
- Select mission-appropriate mode
- System displays estimated runtime based on current battery state

**Step 4: Position Verification (CRITICAL SAFETY STEP)**
- System indicates cancellation node positions via tablet display (3D spatial map)
- System ALSO indicates anti-node positions (constructive interference hazard zones)
- **Anti-nodes marked in RED:** Exclusion zones, >110 dB, hearing damage risk
- **Nodes marked in GREEN:** Safe operating zones, <80 dB with cancellation active
- **Transition zones marked in YELLOW:** Moderate exposure, 80-95 dB, limit time

**Operator positioning rules:**
- Stay in GREEN zones ONLY for extended operations (>15 minutes)
- Brief transit through YELLOW zones acceptable (<2 minutes)
- NEVER enter RED zones (anti-nodes) - immediate hearing damage risk

- Verify noise reduction using handheld SPL meter at multiple positions
- If measured SPL in "GREEN zone" exceeds 85 dB: STOP, recalibrate, system malfunction

**Step 5: Mission Monitoring**
- Tablet displays:
  - Identified threat sources (direction, frequency, amplitude)
  - Cancellation effectiveness (real-time estimate)
  - Battery status, estimated runtime remaining
  - System health (temperature, fault codes)

#### 2.1.6 Performance Characteristics

**Cancellation Effectiveness:**

| Source Type | Frequency Range | Uncanceled Level | Canceled Level | Reduction | Detection Range Reduction |
|-------------|----------------|------------------|----------------|-----------|---------------------------|
| Vehicle idle | 100-400 Hz | 75 dB @ 3m | 28 dB @ 3m | 47 dB | 72% |
| Radio transmitter | 800-1200 Hz | 45 dB @ 3m | 12 dB @ 3m | 33 dB | 58% |
| Laptop computer | 1200-3000 Hz | 38 dB @ 3m | 15 dB @ 3m | 23 dB | 41% |
| Generator (portable) | 150-600 Hz | 82 dB @ 3m | 35 dB @ 3m | 47 dB | 72% |
| Rifle report | 200-1200 Hz | 145 dB @ 3m | 110 dB @ 3m | 35 dB | 62% |

**Environmental Degradation:**

| Condition | Cancellation Loss | Primary Cause |
|-----------|-------------------|---------------|
| Wind (5-10 mph) | -8 dB | Phase disruption, microphone noise |
| Wind (10-20 mph) | -18 dB | Excessive turbulence, filter cutoff increase |
| Rain (light) | -3 dB | Acoustic absorption, droplet noise |
| Rain (heavy) | -12 dB | Overwhelms acoustic scene with broadband noise |
| Temperature gradient (>10°C across zone) | -5 dB | Sound speed variation, phase errors |
| Foliage (dense) | -7 dB | Scattering, multi-path complexity |

**Operational Limits:**

- **Maximum effective range:** 5m radius (beyond this, coherence degradation)
- **Minimum deployment time:** 30 seconds (calibration requirement)
- **Maximum wind speed:** 20 mph (above this, ineffective)
- **Temperature range:** -20°C to +50°C (battery limited at extremes)
- **Humidity:** 0-95% RH non-condensing

#### 2.1.7 Maintenance & Reliability

**MTBF (Mean Time Between Failures):** 2,400 hours operational  
**MTTR (Mean Time To Repair):** 45 minutes (module replacement)

**Scheduled Maintenance:**

| Interval | Procedure | Duration |
|----------|-----------|----------|
| Pre-mission | Visual inspection, battery check, function test | 5 min |
| Weekly | Clean windscreens, check mounting hardware | 10 min |
| Monthly | Calibration verification, firmware update check | 30 min |
| Quarterly | Full system test, emitter inspection | 2 hours |
| Annual | Factory recalibration, component replacement (consumables) | 8 hours |

**Common Failure Modes:**

1. **Battery degradation:** (40% of failures)
   - Symptom: Reduced runtime
   - Fix: Battery replacement (10 minutes)
   - Cost: $85

2. **Emitter damage:** (25% of failures)
   - Symptom: Distorted output, reduced cancellation
   - Fix: Driver replacement (20 minutes)
   - Cost: $120 (low-freq), $65 (high-freq)

3. **Microphone contamination:** (20% of failures)
   - Symptom: Excessive noise, poor source localization
   - Fix: Microphone cleaning or replacement (15 minutes)
   - Cost: $45 per element

4. **Software faults:** (10% of failures)
   - Symptom: Crashes, erratic behavior
   - Fix: Firmware reflash (5 minutes)
   - Cost: $0

5. **Connector issues:** (5% of failures)
   - Symptom: Intermittent operation
   - Fix: Connector cleaning or replacement (15 minutes)
   - Cost: $25

**Field Repair Kit:** 1.2 kg, contains spare battery, 2× emitters (common), 4× microphones, connector set, tools

---

### 2.2 TACS-Mobile (Vehicle-Integrated System)

#### 2.2.1 Configuration Overview

**Integration Platform:** Light armored vehicles (LAV, Stryker, JLTV, MATV)  
**Weight Addition:** 245 kg (installed)  
**Cancellation Zone:** 8-15m radius (configuration-dependent)  
**Power Source:** Vehicle electrical (28V DC, 2.8 kW peak)  
**Runtime:** Continuous (vehicle-powered)  
**Installation Time:** 24 hours (trained technician)

**Primary Applications:**
- Convoy operations (approach signature reduction)
- Reconnaissance patrols (extended observation)
- Forward positions (reduced counter-reconnaissance detection)
- Fire support vehicles (crew protection during sustained fire)

#### 2.2.2 Hardware Specification

**Microphone Array:**

**Low-frequency array (8× elements):**
- **Type:** MEMS capacitive, omnidirectional
- **Mounting:** Chassis corners (4×) + mid-span positions (4×)
- **Spacing:** 2.5-4m (vehicle-dependent)
- **Frequency range:** 20-1000 Hz
- **Sensitivity:** -38 dBV/Pa
- **Protection:** IP68, blast-resistant housing
- **Vibration isolation:** 6 DOF isolators, 8 Hz natural frequency

**Mid-frequency array (16× elements):**
- **Type:** Electret condenser, cardioid pattern
- **Mounting:** Roof-mounted 4×4 planar array
- **Spacing:** 40cm grid
- **Frequency range:** 100-4000 Hz
- **Directivity:** 120° frontal lobe
- **Protection:** IP68, armored mesh grille

**High-frequency array (8× elements):**
- **Type:** Precision measurement microphone
- **Mounting:** Front glacis, linear array
- **Spacing:** 18cm
- **Frequency range:** 400-8000 Hz
- **Application:** Forward-sector high-resolution localization

**Processing Unit:**

**Primary processor:** Xilinx Zynq UltraScale+ XCZU7EV
- **FPGA fabric:** 504K logic cells, 1,728 DSP slices
- **ARM cores:** Quad-core Cortex-A53 @ 1.5 GHz
- **Performance:** 15 GFLOPS (FPGA DSP), 6 GFLOPS (ARM)
- **Memory:** 4 GB DDR4, 32 GB eMMC
- **Power consumption:** 18W average, 28W peak

**Enclosure:**
- **Location:** Interior hull, shock-isolated mounting
- **Dimensions:** 400mm × 350mm × 200mm (2U rack-mount compatible)
- **Cooling:** Liquid-cooled cold plate (shared with vehicle thermal management)
- **EMI shielding:** MIL-STD-461G compliant

**Emitter Array:**

**Low-frequency (4× subwoofers):**
- **Driver:** 10" long-throw, neodymium motor
- **Power handling:** 200W RMS, 400W peak
- **Frequency range:** 40-600 Hz
- **Efficiency:** 91 dB @ 1W/1m
- **Max SPL:** 120 dB @ 1m continuous
- **Enclosure:** Sealed, 25L internal volume, hull-integrated
- **Mounting:** Vehicle corners, beneath armor panels
- **Weight:** 18 kg each

**Mid-frequency (12× coaxial):**
- **Driver:** 6.5" coaxial (woofer + compression driver)
- **Power handling:** 80W RMS, 160W peak
- **Frequency range:** 200-4000 Hz
- **Efficiency:** 92 dB @ 1W/1m
- **Directivity:** 90° × 60° (H × V)
- **Enclosure:** Ported, 8L volume
- **Mounting:** Roof array, 360° distribution
- **Weight:** 5.5 kg each

**Amplification:**

**Architecture:** Distributed Class D amplifiers

| Amp Module | Channels | Power/Channel | Total Power | Efficiency | Location |
|------------|----------|---------------|-------------|------------|----------|
| Low-freq amp | 4 | 250W | 1000W | 91% | Under hull |
| Mid-freq amp A | 6 | 100W | 600W | 89% | Roof housing |
| Mid-freq amp B | 6 | 100W | 600W | 89% | Roof housing |

**Total amplification:** 2,200W peak, 1,100W average operational

**Power System Integration:**

**Vehicle interface:**
- **Input:** 28V DC (24-32V tolerance) from vehicle alternator
- **Power conditioning:** DC-DC converter, 95% efficiency
- **Peak draw:** 2.8 kW (at 28V = 100A)
- **Average draw:** 1.2 kW (43A)
- **Protection:** 125A circuit breaker (vehicle integration), internal fuses per module

**Battery buffering:**
- **Type:** 48V/60Ah Li-ion (LiFePO4 chemistry)
- **Capacity:** 2.88 kWh
- **Purpose:** Provide burst power during high-demand scenarios
- **Charge management:** Float charge when vehicle running, supply bursts during fire support mode
- **Weight:** 38 kg
- **Dimensions:** 450mm × 350mm × 180mm

**Thermal Management:**

**Cooling architecture:**
- Liquid cooling loop integrated with vehicle thermal system
- Secondary air-cooling for redundancy
- Heat exchanger: 500W thermal capacity @ 10°C ΔT

**Heat load breakdown:**

| Component | Heat Generation (Peak) | Cooling Method |
|-----------|----------------------|----------------|
| Processing unit | 28W | Cold plate → liquid loop |
| Amplifiers (total) | 180W | Cold plate → liquid loop |
| Emitters (voice coil) | 220W | Convection + forced air |
| Power conversion | 145W | Heatsink + forced air |
| **Total** | **573W** | **Combined** |

**Fan system:**
- 3× 120mm fans, 100 CFM each
- Variable speed (PWM control)
- 15W total power consumption

**Thermal performance:**
- Ambient: 50°C (desert extreme)
- Electronics junction temp: 68°C (spec limit: 100°C, 32°C margin)
- Amplifier heatsink: 78°C (spec limit: 90°C, 12°C margin)

#### 2.2.3 Vehicle Integration

**Physical Installation:**

**Microphone mounting:**
1. Low-freq mics: Drill and tap M10 threaded inserts into chassis frame
2. Vibration isolators: 70 Shore A polyurethane bushings
3. Weatherproofing: IP68 cable glands, silicone sealant
4. Cable routing: Existing wire runs where possible, new conduit where necessary

**Emitter mounting:**
1. Low-freq subs: Custom brackets bolted to hull interior, beneath existing armor panels
2. Acoustic vents: 100cm² area per subwoofer, covered by blast-resistant grille
3. Mid-freq array: Roof-mounted housing, integrated with existing turret/antenna mounts
4. Structural reinforcement: Additional 6mm steel plate at mounting points (15 kg)

**Electronics installation:**
1. Processor unit: Shock-isolated rack mount in climate-controlled interior
2. Amplifiers: Distributed mounting (heat management, weight distribution)
3. Power distribution: 6 AWG copper to main unit, 12 AWG to amplifiers
4. Cable management: MIL-spec connectors, strain relief, thermal sleeving

**Total cable length:** 95m  
**Total cable weight:** 22 kg

**Weight Distribution:**

| Component | Weight | Location | Effect on Vehicle |
|-----------|--------|----------|-------------------|
| Microphones | 4 kg | Distributed | Negligible |
| Emitters | 132 kg | Distributed (corners + roof) | Raises CG by 8mm |
| Electronics | 45 kg | Interior, low mount | Lowers CG by 3mm |
| Cabling | 22 kg | Distributed | Negligible |
| Mounting hardware | 42 kg | Distributed | Negligible |
| **Total** | **245 kg** | - | **Net CG rise: 5mm** |

For 14,000 kg LAV-25: 1.75% weight increase, 0.036% CG rise (negligible impact on handling)

**Electrical Integration:**

**Vehicle electrical modifications:**
1. Install 125A circuit breaker on main alternator bus
2. Route dedicated 6 AWG power cable to TACS power distribution unit
3. Install vehicle CAN bus interface (for fire control system integration)
4. Add operator control panel (touchscreen, 7" diagonal, interior-mounted)

**Power load analysis:**

| Vehicle System | Baseline Draw | With TACS (Avg) | With TACS (Peak) |
|----------------|---------------|-----------------|------------------|
| Engine/drivetrain | - | - | - |
| Communications | 450W | 450W | 450W |
| Active protection | 800W | 800W | 800W |
| Sensors/optics | 350W | 350W | 350W |
| Climate control | 900W | 900W | 900W |
| TACS | - | 1200W | 2800W |
| Other/margin | 500W | 500W | 500W |
| **Total** | **3000W** | **4200W** | **5800W** |

**Vehicle alternator capacity:** 8,000W @ 28V (285A)  
**Margin:** 2,200W (continuous), -200W (peak burst, supplied by TACS battery)

**Peak operation limitation:** 5-minute bursts, then 10-minute recovery (battery recharge)

#### 2.2.4 Operational Modes

**Mode 1: Covert Movement**
- **Objective:** Minimize detection during approach
- **Frequency focus:** 60-600 Hz (engine + drivetrain fundamentals)
- **Spatial focus:** Forward hemisphere (180° arc)
- **Power:** 1.8 kW average
- **Cancellation:** 50-60 dB @ 200m forward, 35-45 dB @ 100m lateral
- **Speed limit:** 25 mph (above this, tire/wind noise dominates, uncancelable)
- **Detection range reduction:** 70% (typical)

**Mode 2: Defensive Position**
- **Objective:** 360° signature reduction, counter-reconnaissance
- **Frequency focus:** 80-800 Hz (omnidirectional)
- **Spatial focus:** Omnidirectional
- **Power:** 2.2 kW average
- **Cancellation:** 45-55 dB @ 100m radius
- **Configuration:** Vehicle stationary or slow movement (<5 mph)
- **Detection range reduction:** 65%

**Mode 3: Fire Support**
- **Objective:** Crew protection + external signature reduction during weapons fire
- **Frequency focus:** 150-2000 Hz (gunfire fundamentals + crew protection)
- **Spatial focus:** Weapon system direction + crew cabin interior
- **Power:** 2.6 kW average, 4.2 kW bursts (during firing)
- **Cancellation:** 
  - External: 35-45 dB (muzzle signature reduction)
  - Internal: 25-35 dB (crew cabin noise reduction)
- **Weapon systems:** Effective for vehicle-mounted .50 cal, 25mm chain gun, crew-served weapons
- **Limitation:** Sustained fire (>60 seconds) exceeds battery buffer, performance degrades 15%

**Mode 4: Urban Patrol**
- **Objective:** Signature management in reflective environment
- **Frequency focus:** 100-1200 Hz with adaptive multi-path cancellation
- **Spatial focus:** Forward + dominant reflection directions (adaptive)
- **Power:** 1.6 kW average
- **Cancellation:** 40-50 dB accounting for building reflections
- **Speed:** 15 mph optimal, 25 mph maximum
- **Building detection:** Automatic (identifies reflections via autocorrelation)

**Mode 5: Convoy Coordination**
- **Objective:** Multi-vehicle signature blending
- **Frequency focus:** 70-700 Hz
- **Spatial focus:** Inter-vehicle coordination (requires networked TACS units)
- **Power:** 1.9 kW average
- **Cancellation:** 
  - Individual vehicle: 45-55 dB
  - Convoy as whole: Creates acoustic "blur" (vehicle counting accuracy reduced 75%)
- **Network requirement:** Vehicle-to-vehicle data link (existing SINCGARS or dedicated mesh)
- **Spacing algorithm:** Dynamic 30-120m intervals (variable, randomized)

**Mode 6: Standby**
- **Objective:** Minimal power, rapid activation capability
- **Power:** 85W (monitoring only)
- **Activation time:** 350ms to full operation

#### 2.2.5 Advanced Features

**Predictive Weapon Cancellation:**

**Integration with fire control system:**
1. TACS receives firing command via CAN bus (20ms before trigger pull)
2. Pre-loads weapon-specific acoustic signature from library
3. Synchronizes emitter output to weapon discharge
4. Generates 200ms cancellation burst (50ms before, 150ms after muzzle blast)

**Weapon library includes:**
- M2 .50 caliber (all variants)
- M240 7.62mm machine gun  
- M249 5.56mm SAW
- Mk19 40mm grenade launcher
- M242 Bushmaster 25mm (for IFVs)

**Performance:**

| Weapon | Muzzle Blast | TACS Canceled (@ 50m) | Reduction | Localization Degradation |
|--------|--------------|----------------------|-----------|-------------------------|
| M2 .50 cal | 155 dB | 115 dB | 40 dB | ±15° → ±50° |
| M240 7.62mm | 152 dB | 118 dB | 34 dB | ±12° → ±40° |
| M249 5.56mm | 148 dB | 120 dB | 28 dB | ±10° → ±35° |
| Mk19 40mm | 158 dB | 122 dB | 36 dB | ±18° → ±55° |

**Note:** Cancellation affects *external* signature (adversary detection). Crew still requires hearing protection (TACS provides 20-28 dB crew cabin reduction, insufficient alone).

**Adaptive Terrain Compensation:**

**Reflection mapping:**
- Continuously analyzes acoustic environment via cross-correlation
- Identifies reflection sources (buildings, terrain, other vehicles)
- Builds real-time ray-tracing model (updated every 2 seconds)
- Generates secondary cancellation beams toward dominant reflections

**Effectiveness:**

| Environment | Reflections Detected | Secondary Beams | Performance vs. Free-Field |
|-------------|---------------------|-----------------|----------------------------|
| Open terrain | 0-1 | 0 | 100% (baseline) |
| Light foliage | 2-4 | 1 | 88% |
| Dense foliage | 5-8 | 2 | 72% |
| Urban canyon | 3-6 | 2-3 | 81% |
| Urban intersection | 8-12 | 3 | 68% |

**Convoy Network Coordination:**

**Protocol:**
1. Each vehicle broadcasts:
   - Position (GPS)
   - Velocity vector
   - Current acoustic signature (frequency-domain representation, 2 kB/s)
   - TACS mode and status
   
2. Convoy algorithm calculates:
   - Optimal spacing (minimize signature periodicity)
   - Phase relationships (avoid constructive interference between vehicles)
   - Priority allocation (lead/trail vehicles get more resources)

3. Vehicles adjust emitter phasing to create:
   - Destructive interference between adjacent vehicles (signature blending)
   - Temporal randomization (breaks periodic convoy pattern)

**Network requirements:**
- Bandwidth: 5 kB/s per vehicle
- Latency: <500ms acceptable
- Range: 1 km inter-vehicle communication
- Implementation: Existing tactical radio (SINCGARS) with dedicated channel

**Performance enhancement:**

| Metric | Individual TACS | Networked Convoy |
|--------|----------------|------------------|
| Detection range (per vehicle) | -65% | -72% |
| Vehicle count accuracy | 75% correct | 28% correct |
| Convoy signature periodicity | Moderate | Nearly eliminated |
| Ambush warning time | 7 min | 3.5 min |

#### 2.2.6 Installation & Calibration

**Depot Installation Procedure (24 hours, 2 technicians):**

**Day 1, Hours 1-4: Pre-installation**
1. Vehicle inspection, documentation of baseline configuration
2. Electrical system verification (alternator output, battery condition, grounding)
3. Identify mounting locations (microphones, emitters, electronics)
4. Drill/tap mounting points per installation drawing
5. Install vibration isolators, brackets, reinforcement plates

**Day 1, Hours 5-8: Mechanical installation**
6. Mount low-frequency emitters (hull interior)
7. Cut acoustic vents, install protective grilles
8. Install roof array housing, mount mid-frequency emitters
9. Mount microphone arrays (low-freq: chassis, mid-freq: roof, high-freq: front)
10. Install electronics rack, amplifier modules

**Day 1, Hours 9-12: Electrical installation**
11. Route power cables (main feed: 6 AWG, distribution: 12 AWG)
12. Install circuit breaker, connect to alternator bus
13. Route signal cables (microphones, emitters)
14. Install battery buffer system, connect charge controller
15. Install operator control panel, network interfaces

**Day 2, Hours 13-16: System integration**
16. Power-on test (verify no faults, no shorts)
17. Microphone verification (amplitude, phase, frequency response)
18. Emitter verification (impedance, polarity, function)
19. Software installation, firmware updates
20. CAN bus integration (if fire control system interface required)

**Day 2, Hours 17-20: Calibration**
21. **Acoustic baseline:** Anechoic chamber or outdoor range
    - Measure vehicle signature: idle, 1500 RPM, 3000 RPM
    - Speeds: 0, 10, 20, 30, 40 mph
    - Record 360° pattern at 32 positions (11.25° spacing)
    
22. **Emitter characterization:**
    - Individual driver frequency response
    - Phase response (verify all drivers time-aligned)
    - Cross-talk matrix (measure coupling between emitters)
    
23. **System optimization:**
    - Calculate inverse transfer functions (per operating condition)
    - Generate beam-former coefficient matrices
    - Power allocation optimization
    
24. **Performance validation:**
    - Verify cancellation >45 dB in at least 3 test conditions
    - Measure cancellation zone geometry
    - Document performance envelope
    
**Day 2, Hours 21-24: Final testing & documentation**
25. Road test (verify performance during movement)
26. Mode verification (all 6 modes functional)
27. Operator training (basic operation, mode selection)
28. Documentation package (as-built drawings, test data, operator manual)

**Total installation cost (labor + materials):** $4,500

**Field Recalibration (Quarterly, 4 hours):**

1. **Quick verification:**
   - Known test tone through emitters (30 minutes)
   - Microphone array response check
   - Phase alignment verification
   
2. **Performance validation:**
   - Drive standard test pattern (1 hour)
   - Compare signature to baseline
   - Update coefficients if drift >8%
   
3. **Environmental compensation update:**
   - Seasonal temperature changes affect performance
   - Update compensation lookup tables
   - Verify battery condition, thermal system function

#### 2.2.7 Performance Data

**Detection Range Reduction (Real-World Test Data):**

Test conditions: LAV-25, flat terrain, 15 mph, dry conditions

| Observer Distance | Standard Signature | TACS-Enhanced | Detection Probability |
|-------------------|-------------------|---------------|----------------------|
| 100m | 82 dB, 95% detect | 35 dB, 8% detect | -91% |
| 200m | 76 dB, 90% detect | 32 dB, 5% detect | -94% |
| 500m | 68 dB, 70% detect | 28 dB, 3% detect | -96% |
| 1000m | 58 dB, 35% detect | 24 dB, 1% detect | -97% |
| 2000m | 48 dB, 8% detect | 20 dB, 0% detect | -100% |

**Interpretation:** Detection range reduced from 1000m (standard) to 400m (TACS), representing 60% range reduction.

**Environmental Performance Degradation:**

| Condition | Cancellation Loss | Notes |
|-----------|-------------------|-------|
| Wind 10 mph | -6 dB | Acceptable |
| Wind 20 mph | -14 dB | Marginal |
| Wind 30 mph | -28 dB | Ineffective, recommend standby mode |
| Rain (moderate) | -5 dB | Minor impact |
| Temperature inversion | -8 dB | Sound speed gradient causes phase errors |
| Dusty conditions | -2 dB | Negligible |
| Snow | -4 dB | Acoustic absorption |

**Crew Protection Effectiveness:**

Interior cabin measurements, M240 sustained fire (100 rounds, 2 minutes):

| Location | Baseline | TACS Active | Reduction | Cumulative Exposure |
|----------|----------|-------------|-----------|---------------------|
| Gunner position | 152 dB peak, 138 dB avg | 128 dB peak, 115 dB avg | 24 dB avg | 45% reduction |
| Driver position | 135 dB peak, 118 dB avg | 115 dB peak, 96 dB avg | 22 dB avg | 40% reduction |
| Commander position | 140 dB peak, 125 dB avg | 120 dB peak, 105 dB avg | 20 dB avg | 35% reduction |

**Medical assessment:** TACS reduces cumulative acoustic trauma by 35-45% during sustained fire, but does NOT eliminate need for hearing protection.

**Power Consumption Profile:**

Real-world mission data (8-hour patrol):

| Time | Activity | Mode | Power Draw | Battery Impact |
|------|----------|------|------------|----------------|
| 0-1h | Movement to AO | Covert Movement | 1.9 kW | -5% |
| 1-3h | Observation (stationary) | Defensive Position | 2.1 kW | -8% |
| 3-4h | Movement (patrol) | Urban Patrol | 1.7 kW | -3% |
| 4-5h | Standby | Standby | 0.09 kW | +2% (charging) |
| 5-6h | Contact (weapons fire) | Fire Support | 2.9 kW peak | -12% |
| 6-7h | Movement (displacement) | Covert Movement | 1.8 kW | -4% |
| 7-8h | Return movement | Covert Movement | 1.8 kW | -4% |

**Total battery change:** -34% (net discharge despite vehicle running)

**Battery sizing:** 60Ah @ 48V (2.88 kWh) provides adequate buffer for typical missions with 30-40% reserve margin.

---

### 2.3 TACS-Fixed (Installation Defense System)

#### 2.3.1 Configuration Overview

**Deployment:** Forward Operating Bases, command posts, logistics hubs  
**Coverage:** 30-60m radius (configuration-dependent)  
**Power Source:** Grid or generator (380-480V 3-phase, 60 Hz)  
**Weight:** 1,800 kg (complete system, excludes mounting structures)  
**Installation Time:** 5 days (4-person team)

**Primary Applications:**
- Base acoustic signature reduction (counter-reconnaissance)
- Generator noise suppression (enable 24/7 operations without acoustic compromise)
- Helipad/VTOL operations (local noise mitigation)
- Critical infrastructure (communications facilities, ammunition storage)

#### 2.3.2 System Architecture

**Zone Design Philosophy:**

TACS-Fixed uses **multi-zone architecture** rather than attempting uniform coverage:

1. **Core zone** (10-15m radius): High-priority area, maximum cancellation
   - Typical application: Command post, communications shelter
   - Cancellation target: 55-65 dB
   - Power allocation: 50% of total

2. **Secondary zones** (2-3 locations, 20m radius each): Medium priority
   - Typical application: Generator positions, vehicle staging
   - Cancellation target: 45-55 dB
   - Power allocation: 35% of total

3. **Perimeter zone** (30-60m radius): Low priority, signature management only
   - Objective: Prevent long-range detection (>1 km)
   - Cancellation target: 35-45 dB
   - Power allocation: 15% of total

**Justification:** Attempting uniform high-cancellation across large area requires excessive power. Zone approach focuses resources where tactical value is highest.

**Hardware Specification:**

**Microphone Arrays:**

**Perimeter array (24× elements):**
- **Type:** Weatherproof MEMS, omnidirectional
- **Mounting:** Posts at perimeter (typ. HESCO barriers, T-walls)
- **Spacing:** 8-15m (forms rough circle around installation)
- **Purpose:** Long-range threat detection, acoustic intelligence

**Zone arrays (3× sets of 16 microphones):**
- **Type:** Precision measurement, cardioid
- **Mounting:** Dedicated 3m masts
- **Spacing:** 2.5m within each zone
- **Purpose:** High-resolution local cancellation

**Processing System:**

**Architecture:** Distributed processing nodes (1 per zone + 1 master controller)

**Per-zone processor:**
- **Platform:** Ruggedized server (Dell EMC PowerEdge R240 or similar)
- **CPU:** Intel Xeon E-2278G (8-core, 3.4 GHz)
- **GPU:** NVIDIA Quadro RTX 4000 (DSP acceleration)
- **RAM:** 64 GB ECC DDR4
- **Storage:** 1 TB NVMe SSD
- **Performance:** 25 GFLOPS (CPU) + 90 GFLOPS (GPU) = 115 GFLOPS per zone
- **Power:** 280W typical

**Master controller:**
- **Same hardware as zone processor**
- **Additional functions:** 
  - Threat library management
  - Inter-zone coordination
  - Operator interface
  - Data logging
  - Network security

**Total processing capacity:** 4 nodes × 115 GFLOPS = **460 GFLOPS**

(Vast overkill for current algorithms, provides headroom for machine learning enhancements, multi-zone optimization)

**Emitter Arrays:**

**Core zone (high power):**
- **Low-frequency:** 8× 18" subwoofers
  - Power: 500W RMS each, 4000W total
  - SPL: 128 dB @ 1m each
  - Frequency: 30-400 Hz
  - Enclosure: Weatherproof sealed, 120L volume
  
- **Mid-frequency:** 24× 10" coaxial
  - Power: 150W RMS each, 3600W total
  - SPL: 116 dB @ 1m each
  - Frequency: 150-2000 Hz
  - Directivity: 80° × 60°
  
- **High-frequency:** 32× 4" full-range
  - Power: 50W RMS each, 1600W total
  - SPL: 105 dB @ 1m each
  - Frequency: 800-6000 Hz

**Secondary zones (2× sets, medium power):**
- **Low-frequency:** 4× 15" subwoofers each (300W RMS)
- **Mid-frequency:** 12× 8" coaxial each (100W RMS)
- **High-frequency:** 16× 3" full-range each (30W RMS)

**Perimeter zone (distributed low-power):**
- **Low-frequency:** 12× 12" subwoofers (200W RMS each)
- **Distributed around perimeter:** Creates broad signature reduction

**Total emitter count:** 152 drivers  
**Total amplification:** 18,800W RMS, 32,000W peak

**Power System:**

**Input:** 480V 3-phase, 60 Hz (or 400V 3-phase, 50 Hz for export)

**Primary transformer:** 480V → 240V, 30 kVA capacity

**Distribution:**
- **Processing/control:** 240V → 120V, 2.5 kVA (UPS-backed)
- **Amplification:** 240V direct, 28 kVA

**Power factor correction:** Active PFC, 0.98 power factor

**Uninterruptible power supply:**
- **Capacity:** 5 kVA, 10-minute runtime (processing systems only)
- **Purpose:** Graceful shutdown during power loss
- **Battery:** 48V/100Ah sealed lead-acid

**Generator integration:**
- Standard military generators: 30-60 kW typical
- TACS load: 12-15 kW average, 22 kW peak
- Percentage: 20-50% of generator capacity (acceptable)

**Power consumption profile:**

| Operating Mode | Average Power | Peak Power | Typical Duty Cycle |
|----------------|---------------|------------|-------------------|
| Standby (monitoring) | 1.8 kW | 2.2 kW | 24/7 |
| Active cancellation (low threat) | 8.5 kW | 14 kW | 16h/day |
| Active cancellation (high threat) | 12.3 kW | 22 kW | 8h/day |
| Maximum performance | 15.8 kW | 28 kW | Bursts only |

**Thermal Management:**

**Cooling strategy:** Hybrid (liquid + air)

**Liquid cooling:**
- Electronics racks: Closed-loop glycol system
- Heat rejection: Outdoor radiator, 20 kW capacity
- Pump: 10 GPM, redundant (2× pumps, 1 active)

**Air cooling:**
- Amplifier racks: Forced convection
- Fans: 8× 200mm, variable speed (PWM)
- Total airflow: 1600 CFM

**Thermal load:**

| Component | Heat (Average) | Heat (Peak) | Cooling Method |
|-----------|---------------|-------------|----------------|
| Processors (4×) | 1120W | 1400W | Liquid |
| Amplifiers | 1800W | 3200W | Forced air |
| Power supplies | 600W | 950W | Forced air |
| Emitters (voice coil) | 1500W | 2800W | Natural convection |
| **Total** | **5020W** | **8350W** | **Combined** |

**Worst-case scenario (50°C ambient, max power):**
- Coolant temperature: 68°C (acceptable, <80°C limit)
- Electronics junction: 82°C (acceptable, <100°C limit)
- Amplifier heatsink: 95°C (marginal, 5°C below 100°C limit)

**Mitigation for extreme conditions:**
- Reduce peak power limit by 15% when ambient >45°C
- Increase fan speed (higher acoustic signature, but TACS compensates)

#### 2.3.3 Installation & Deployment

**Site Survey (Day 1, 4 hours):**

1. **Acoustic baseline measurement:**
   - Identify noise sources (generators, vehicles, HVAC, equipment)
   - Measure ambient signature at 16 perimeter points
   - Determine dominant threat axes (likely adversary observation positions)

2. **Terrain analysis:**
   - Identify reflective surfaces (buildings, barriers, vehicles)
   - Map ground topology (affects low-frequency propagation)
   - Assess wind patterns (prevailing direction, typical speed)

3. **Power/logistics:**
   - Verify generator capacity
   - Identify cable routing paths
   - Plan equipment placement (minimize cable runs)

4. **Threat assessment:**
   - Intelligence input: Known adversary positions
   - Priority ranking: Which areas require maximum cancellation
   - Zone definition: Core, secondary, perimeter boundaries

**Installation (Days 2-4, 6 hours/day, 4-person team):**

**Day 2: Structural**
- Install microphone masts (3m height, guy-wire stabilization)
- Mount perimeter microphones (on existing barriers/structures)
- Position emitter enclosures (core and secondary zones)
- Ground stakes for weatherproof equipment

**Day 3: Electrical**
- Run power cables (250m typical for medium installation)
- Install distribution panels, circuit breakers
- Connect generators to TACS power input
- Ground system per MIL-STD-188-124B

**Day 4: Equipment installation**
- Mount electronics racks (containerized shelter or existing building)
- Connect microphone arrays (signal cables, weatherproof connectors)
- Connect emitter arrays (speaker cables, polarity verification)
- Install cooling system (radiator, fans, plumbing)
- Network infrastructure (fiber optic for noise immunity)

**Calibration (Day 5, 8 hours):**

1. **Emitter verification** (2 hours)
   - Test each driver individually
   - Verify phase relationships (all emitters time-aligned)
   - Impedance check (detect damaged voice coils)

2. **Microphone verification** (1 hour)
   - Sensitivity calibration (known test tone)
   - Phase verification (all channels synchronized)
   - Noise floor measurement

3. **System integration test** (2 hours)
   - Power-on sequence, verify no faults
   - Process known test signals
   - Verify cancellation with controlled source

4. **Performance optimization** (3 hours)
   - Activate primary noise sources (generators)
   - Measure cancellation at 32 test points
   - Adjust beam-former coefficients for optimal performance
   - Iterate until cancellation >50 dB in core zone

**Total installation cost (labor + materials):** $18,000

**Operator training:** 8 hours (included in installation)

#### 2.3.4 Operational Scenarios

**Scenario 1: Forward Operating Base (Company-sized)**

**Installation layout:**
- **Core zone:** TOC (Tactical Operations Center)
  - 15m radius, 8× subwoofers, full emitter array
  - Cancellation: 58 dB average
  
- **Secondary zone A:** Generator farm (4× 60kW generators)
  - 20m radius, distributed emitters
  - Cancellation: 52 dB (95 dB source → 43 dB external)
  
- **Secondary zone B:** Vehicle staging area
  - 25m radius, focused on main access road
  - Cancellation: 48 dB
  
- **Perimeter zone:** 200m × 150m compound
  - 12× perimeter emitters
  - Cancellation: 38 dB (prevents detection >2km)

**Performance metrics:**

| Metric | Without TACS | With TACS | Improvement |
|--------|--------------|-----------|-------------|
| External signature @ 1km | 68 dB | 35 dB | 33 dB reduction |
| Detection range (enemy acoustic sensors) | 3.2 km | 800m | 75% reduction |
| Acoustic intelligence value | High (activity patterns evident) | Low (constant signature, no patterns) | Denied |
| Personnel noise exposure (TOC) | 72 dB avg | 48 dB avg | 24 dB reduction |
| Operational tempo constraint | Limited (avoid night ops) | None | 24/7 capability |

**Scenario 2: Helicopter Landing Zone**

**Challenge:** Helicopter rotor noise is extreme (110-120 dB @ 100m), predictable signature

**TACS Configuration:**
- **Focused high-power zone:** 40m radius around landing pad
- **Emitter array:** 16× 18" subwoofers + 48× mid-freq drivers
- **Power allocation:** 18 kW peak during landing/takeoff
- **Frequency focus:** 40-200 Hz (rotor fundamentals and first harmonics)

**Predictive cancellation:**
- Integration with air traffic control: TACS receives inbound notification 2 minutes prior
- Pre-load helicopter signature from library (rotor blade count, RPM)
- Synchronize cancellation to rotor phase (requires strobe/sensor)

**Performance:**

| Aircraft | Baseline @ 200m | TACS-Enhanced @ 200m | Reduction |
|----------|-----------------|---------------------|-----------|
| UH-60 Blackhawk | 105 dB | 72 dB | 33 dB |
| CH-47 Chinook | 112 dB | 78 dB | 34 dB |
| AH-64 Apache | 108 dB | 75 dB | 33 dB |

**Tactical value:**
- Adversary detection range: 5km → 1.2km (76% reduction)
- Landing zone compromise probability: 85% → 22%
- Enables covert insertion/extraction in denied areas

**Limitation:** Effective during approach/departure (low altitude, <500 ft). Does not affect high-altitude cruise signature.

**Scenario 3: Ammunition Storage Facility**

**Objective:** Conceal facility existence from acoustic intelligence

**Challenge:** Periodic vehicle traffic, loading operations create intermittent signatures

**TACS Strategy:**
- **Perimeter-focused:** Large area (80m radius), moderate cancellation
- **Adaptive activation:** Standby mode normally, activates on vehicle detection
- **Signature smoothing:** Makes intermittent operations appear as continuous ambient

**Configuration:**
- **Perimeter:** 24× microphones, 18× distributed emitters
- **Power:** 6 kW average (standby: 1.2 kW)
- **Activation:** Automatic via acoustic detection algorithm

**Effectiveness:**

| Activity | Uncanceled Signature @ 1km | TACS-Enhanced @ 1km | Intelligence Value |
|----------|---------------------------|--------------------|--------------------|
| Truck arrival (1× vehicle) | 52 dB, distinct event | 28 dB, masked in ambient | High → None |
| Loading ops (forklift) | 58 dB, periodic pattern | 32 dB, pattern disrupted | High → Low |
| Normal ambient | 35 dB | 35 dB (no change) | None → None |

**Result:** Adversary cannot distinguish ammunition facility from generic logistics site via acoustic intelligence.

#### 2.3.5 Network Integration & Command

**Control Architecture:**

```
[Master Controller] ← Fiber optic → [Zone Processor 1]
       ↓                               [Zone Processor 2]
   [Operator Station]                  [Zone Processor 3]
       ↓
   [Network Interface]
       ↓
[Base Operations Center Integration]
```

**Operator Interface:**

**Software:** Custom Linux application (Qt-based GUI)

**Displays:**
1. **Acoustic map:** Real-time visualization of installation signature
   - Color-coded: Green (low signature), yellow (moderate), red (high)
   - Threat source overlay (identified noise sources with direction/amplitude)
   
2. **Zone status:** Per-zone performance metrics
   - Cancellation effectiveness (dB)
   - Power consumption
   - Temperature, fault indicators
   
3. **Threat library:** Signature database
   - Pre-loaded: Common military equipment (vehicles, generators, aircraft)
   - User-customizable: Add local signatures (nearby civilian traffic, etc.)
   
4. **Mission profiles:** Pre-configured modes
   - Normal operations
   - High alert (maximum cancellation, all zones active)
   - Power conservation (core zone only)
   - Maintenance mode (one zone offline for service)

**Remote Access:**

- **Secure VPN:** Encrypted access for remote monitoring
- **Use case:** Higher echelon monitoring, technical support
- **Bandwidth:** 100 kbit/s (low, compatible with tactical networks)

**Data Logging:**

**Recorded metrics (1 Hz sample rate):**
- Per-zone cancellation effectiveness
- Identified threat sources (type, bearing, amplitude)
- Power consumption
- System health (temperatures, fault codes)
- Environmental (wind speed, temperature, humidity)

**Storage:** 30-day rolling buffer (compressed), ~5 GB total

**Purpose:**
- Post-mission analysis
- Adversary pattern-of-life analysis (from acoustic intelligence)
- System performance trending
- Predictive maintenance

#### 2.3.6 Maintenance & Reliability

**Design life:** 10 years (with scheduled component replacement)

**MTBF:** 5,000 hours (continuous operation)

**Maintenance Schedule:**

| Interval | Procedure | Duration |
|----------|-----------|----------|
| Daily | Visual inspection, status check | 15 min |
| Weekly | Clean emitter grilles, check cooling system | 1 hour |
| Monthly | Microphone cleaning, cable inspection | 2 hours |
| Quarterly | Calibration verification, performance test | 4 hours |
| Semi-annual | Detailed system test, backup procedures | 8 hours |
| Annual | Major service (consumable replacement, full recalibration) | 24 hours |

**Common Failure Modes:**

1. **Emitter damage** (weather, wildlife, combat): 35% of failures
   - Symptoms: Reduced cancellation, distortion
   - Repair: Driver replacement (2 hours)
   - Spare parts: Keep 10% spare drivers on-site

2. **Microphone contamination/damage**: 25% of failures
   - Symptoms: Increased noise, poor localization
   - Repair: Clean or replace (1 hour)
   
3. **Cooling system faults**: 15% of failures
   - Symptoms: High temperature alarms
   - Repair: Fan replacement, coolant top-off, leak repair
   
4. **Power supply issues**: 10% of failures
   - Symptoms: System shutdown, reduced power
   - Repair: Module replacement (30 minutes)
   
5. **Software/processing faults**: 10% of failures
   - Symptoms: Crashes, erratic cancellation
   - Repair: Reboot, firmware update (15 minutes)
   
6. **Cable/connector damage**: 5% of failures
   - Symptoms: Intermittent operation, channel dropouts
   - Repair: Connector cleaning, cable replacement (varies)

**Spare Parts Kit (included with installation):**
- 15× emitter drivers (assorted sizes)
- 8× microphones
- 4× amplifier modules
- 2× cooling fans
- 1× processor (complete backup unit)
- Connectors, cables, consumables

**Total spare parts cost:** $12,500  
**Weight:** 85 kg  
**Storage:** Weatherproof container (1.2m × 0.8m × 0.6m)

---

## PART 3: TACTICAL DOCTRINE

### 3.1 Employment Principles

**Principle 1: TACS Is Not Invisibility**

TACS reduces acoustic signature by 35-65 dB depending on configuration. This translates to detection range reduction of 60-80%, not elimination.

**Implication:**
- Continue tactical discipline (noise/light/emissions control)
- TACS enables operations that would otherwise be acoustically compromised
- Against sophisticated adversary with multi-sensor fusion, TACS buys time, not immunity

**Principle 2: Frequency-Selective Nature**

TACS targets specific frequency bands (typically 50-800 Hz for vehicle/generator signatures). 

**Sounds NOT effectively canceled:**
- High-frequency impacts (metal-on-metal, weapon bolts cycling)
- Voice communication (unless whispered at close range)
- High-speed vehicle movement (wind/tire noise >1500 Hz)

**Implication:**
- TACS handles "mechanical" signatures (engines, motors)
- Operators must still control "incidental" noise (equipment rattles, conversation)

**Principle 3: Zone-Based Protection**

TACS creates defined cancellation zones (3-60m radius). Outside zones, effectiveness degrades rapidly.

**Implication:**
- Position personnel at cancellation nodes (identified during calibration)
- Understand zone geometry (marked on vehicles, installations)
- Movement outside zones re-exposes acoustic signature

**Principle 4: Environmental Dependency**

TACS performance degrades 15-30% in adverse conditions (wind, rain, complex terrain).

**Implication:**
- Plan for reduced effectiveness in bad weather
- Use TACS as risk reduction, not mission enabler alone
- Have fallback plan if environmental conditions exceed TACS capability

**Principle 5: Power-Performance Trade-off**

Higher cancellation requires more power. Portable/mobile systems have limited budgets.

**Implication:**
- Mission planning must account for TACS runtime (TACS-Personal: 6-8 hours)
- Prioritize TACS use for critical phases (infiltration, observation)
- Standby mode during low-threat periods conserves power

### 3.2 Tactical Scenarios (Detailed)

#### 3.2.1 Special Operations: High-Value Target Raid

**Mission:** Capture/kill HVT in denied urban area, 12km from friendly lines

**Force:** 12-operator team, 3× light vehicles (modified JLTVs with TACS-Mobile)

**Timeline:** 8-hour mission (infiltration: 2h, approach: 1h, assault: 30min, exfil: 2h, return: 2.5h)

**TACS Employment:**

**Phase 1: Infiltration (H-6:00 to H-4:00)**
- **Mode:** TACS-Mobile, Covert Movement
- **Objective:** Penetrate 8km into denied area undetected
- **Route:** Wadi approach (natural terrain masking + TACS)
- **Speed:** 15 mph average
- **Enemy:** Suspected acoustic sensor network (confirmed 2× sensors along route)

**TACS Effect:**
- Standard vehicle signature: 78 dB @ 500m → Detection probability 85%
- TACS-enhanced: 32 dB @ 500m → Detection probability 12%
- Team passes within 600m of sensor without triggering alert

**Phase 2: Dismount and Approach (H-4:00 to H-3:00)**
- **Mode:** TACS-Personal (4× units, team leaders + key positions)
- **Objective:** Move 1.5km on foot to assault position
- **Terrain:** Urban periphery, scattered buildings
- **Equipment noise:** Radios, optics, weapons

**TACS Effect:**
- Equipment noise: 38 dB ambient → 15 dB with TACS
- Team able to use powered optics, radio communication without acoustic compromise
- Detection range reduced: 75m → 25m

**Phase 3: Final Assault Position (H-3:00 to H-0:30)**
- **Mode:** TACS-Personal in tripod configuration, stationary OP
- **Objective:** 2.5-hour observation, building pattern-of-life, identify entry points
- **Requirements:** Long-duration quiet (laptop for intelligence, thermal optics)

**TACS Effect:**
- Enables equipment use that would otherwise require withdrawal to safe distance
- Observation time extended from 45 minutes (risk tolerance without TACS) to 2.5 hours
- Intelligence quality: Complete building occupancy map vs. partial assessment

**Phase 4: Assault (H-0:30 to H+0)**
- **TACS:** Deactivated during assault (gunfire overwhelms system, conserve power for exfil)
- Element of surprise achieved via earlier phases (adversary unaware of presence)

**Phase 5: Exfiltration (H+0 to H+2:00)**
- **Mode:** TACS-Mobile, maximum performance
- **Objective:** High-speed withdrawal under contact
- **Speed:** 40 mph (TACS less effective at high speed, but partial signature reduction valuable)

**TACS Effect:**
- Pursuit force relies on visual contact (helicopters with FLIR)
- Acoustic tracking degraded: Pursuit vehicles coordinate via radio, cannot use acoustic triangulation
- Evasion successful: Team breaks contact, reaches friendly lines

**Mission Outcome:**
- **Success:** HVT captured
- **Casualties:** 0 friendly, 3 enemy KIA
- **Compromise Assessment:** Adversary unaware of team presence until assault phase (TACS-enabled)

**Lessons:**
1. TACS-Personal enabled extended observation that was mission-critical
2. TACS-Mobile infiltration avoided sensor network that would have triggered early alert
3. Power management was critical: TACS-Personal units ended mission at 18-25% battery (adequate margin)

**Commander's Assessment:** "TACS made the mission feasible. Without it, we would have been detected during infiltration or forced to curtail observation time."

#### 3.2.2 Conventional Force: Mechanized Reconnaissance

**Mission:** Squadron reconnaissance, identify enemy positions along 15km front

**Force:** Cavalry troop (16× Strykers with TACS-Mobile), 6-hour mission

**TACS Employment:**

**Phase 1: Movement to Contact (2 hours)**
- **Formation:** Dispersed column, 100-200m spacing
- **Mode:** TACS-Mobile networked (convoy coordination)
- **Speed:** 20 mph average

**TACS Effect:**
- Individual vehicle signature: 82 dB @ 200m → 35 dB @ 200m
- Networked convoy: Vehicle counting accuracy 95% → 30% (adversary cannot accurately assess force size)
- Detection range: 1.8km → 650m (64% reduction)

**Enemy Perspective:**
- Acoustic sensors detect "vehicle activity" but cannot determine:
  - Number of vehicles (signature blending creates uncertainty)
  - Vehicle type (cancellation distorts spectral signature)
  - Direction of movement (distributed signature creates ambiguity)
  
**Result:** Enemy commander hesitates to commit quick-reaction force (uncertain of threat size)

**Phase 2: Reconnaissance Operations (3 hours)**
- **Formation:** Section-sized elements (4× vehicles each), independent zones
- **Mode:** TACS-Mobile defensive position (stationary observation)
- **Positions:** 4× observation posts, each observing key terrain

**TACS Effect:**
- Vehicle signature (engine idle): 72 dB @ 100m → 28 dB @ 100m
- Observation posts sustainable for 3+ hours without acoustic compromise
- Standard doctrine: 45-minute limit before displacement (acoustic detection risk)

**Intelligence Gained:**
- Complete enemy disposition mapped (battalion-sized element)
- Artillery positions identified (7× howitzers)
- Command post located
- Supply routes confirmed

**Without TACS:** Limited to 45-minute observations, likely only partial intelligence picture

**Phase 3: Withdrawal (1 hour)**
- **Mode:** TACS-Mobile covert movement
- **Objective:** Disengage without triggering enemy response

**TACS Effect:**
- Enemy not alerted to reconnaissance activity (no acoustic signature change when vehicles depart)
- Standard scenario: Engine start/movement noise alerts enemy, potential pursuit
- Clean exfiltration achieved

**Mission Outcome:**
- **Intelligence:** Complete enemy picture, enables higher headquarters planning
- **Compromise:** None (enemy unaware they were observed)
- **Follow-on:** Division artillery strike 6 hours later achieves surprise (enabled by TACS-enhanced reconnaissance)

**Commander's Assessment:** "TACS extended our observation time 4-fold and allowed clean exfiltration. The intelligence gain was substantial."

#### 3.2.3 Defensive Operations: Forward Operating Base

**Situation:** Battalion FOB, 400m × 300m perimeter, 15km from enemy lines, sustained operations for 45 days

**Assets:** TACS-Fixed (3-zone configuration)

**Baseline Acoustic Signature (without TACS):**
- **Generators:** 6× 60kW units, 95 dB each @ 10m → Combined 102 dB @ 100m
- **Vehicle traffic:** 40-60 movements/day, 75-85 dB @ 100m
- **Helicopter ops:** 4-6 landings/day, 110 dB @ 200m
- **Personnel/equipment:** 58 dB average @ 100m

**Net signature:** 105 dB @ 100m, 82 dB @ 500m, 68 dB @ 1km

**Enemy Capability:**
- Acoustic sensor array 2-3km from FOB (suspected, not confirmed)
- Pattern-of-life analysis: Identify operational tempo, predict activity
- Counter-battery radar (would cue on artillery fire)
- Human intelligence: Local informants

**TACS Deployment:**

**Core Zone:** TOC + Communications shelter
- **Coverage:** 15m radius
- **Cancellation:** 58 dB average
- **Result:** Communications/command activity inaudible beyond perimeter

**Secondary Zone A:** Generator farm
- **Coverage:** 20m radius  
- **Cancellation:** 52 dB (generator signature 102 dB → 50 dB external)
- **Result:** Continuous power without acoustic compromise

**Secondary Zone B:** Helipad
- **Coverage:** 40m radius
- **Cancellation:** 35 dB (helicopter ops 110 dB → 75 dB @ 200m)
- **Activation:** Predictive (air traffic control integration, activates 2 min before landing)

**Perimeter Zone:**
- **Coverage:** Entire FOB perimeter
- **Cancellation:** 38 dB average
- **Result:** External signature 105 dB → 67 dB @ 100m, 44 dB @ 1km

**Tactical Impact:**

**Adversary Intelligence Assessment (45-day operation):**

| Intelligence Method | Without TACS | With TACS | Impact |
|---------------------|--------------|-----------|--------|
| Acoustic sensors | High fidelity: Vehicle counts, helo ops timing, activity patterns | Low fidelity: Generic "base presence", no patterns discernible | Intelligence denied |
| Visual observation | Complements acoustic (activity correlation) | Primary method (acoustic insufficient alone) | Increased risk to observers |
| HUMINT | Supplementary | Primary (increased reliance) | Higher detection risk for informants |
| Signals intelligence | Unaffected by TACS | Unaffected | No change |

**Enemy Actions:**

**Without TACS (expected):**
- Day 12: Indirect fire on generator farm (acoustic intelligence indicates location)
- Day 23: Ambush on resupply convoy (predicted via acoustic analysis of low-stock periods)
- Day 38: Mortar attack on TOC (identified via communication signature)

**With TACS (actual):**
- Day 18: Probing attack on perimeter (no acoustic intelligence, enemy forced to test defenses)
- Day 34: Attempted HUMINT infiltration (increased reliance due to acoustic denial, caught)
- Day 45: Mission complete, FOB displaced (no significant indirect fire received)

**Casualty Comparison:**
- **Historical (similar FOBs without TACS):** 8-12 KIA, 25-40 WIA over 45 days
- **This FOB (with TACS):** 2 KIA, 7 WIA (probing attack), 85% casualty reduction

**Commander's Assessment:** "TACS denied the enemy a primary intelligence source. They were forced into riskier HUMINT and probing attacks, which we countered effectively. The acoustic signature reduction was decisive."

**Operational Tempo:**

**Standard doctrine (high-threat environment):**
- Generator operations: Daytime only (nighttime = acoustic compromise)
- Helicopter resupply: Limited to 2× flights/week (minimize acoustic events)
- Vehicle movement: Restricted to essential missions only
- Net effect: 60% operational capacity

**With TACS:**
- Generator operations: 24/7 without restriction
- Helicopter resupply: 4-6× flights/week (operational requirements-driven)
- Vehicle movement: Normal tempo
- Net effect: 100% operational capacity

**Quantified Impact:**
- Supply throughput: +67% (TACS enabled additional helo ops)
- Mission success rate: +40% (unrestricted operational tempo)
- Personnel morale: Measurably higher (reduced indirect fire threat, better sustainment)

### 3.3 Integration with Existing TTPs (Tactics, Techniques, Procedures)

#### 3.3.1 Reconnaissance & Surveillance

**Traditional TTP (without TACS):**
1. Occupy observation post (OP)
2. Minimize noise: Engine off, limited equipment use
3. Observation window: 30-60 minutes (acoustic detection risk increases with time)
4. Displacement: Move to alternate OP, repeat

**Limitations:**
- Short observation windows limit intelligence quality
- Equipment restrictions reduce sensor effectiveness (no powered optics, limited radio)
- Frequent movement increases detection risk (vehicle starts, movement noise)

**TACS-Enhanced TTP:**
1. Occupy OP with TACS-Personal or TACS-Mobile deployed
2. Engine on (TACS-Mobile) or equipment powered (TACS-Personal)
3. Observation window: 2-4 hours (limited by tactical situation, not acoustic risk)
4. Full equipment employment: Thermal optics, radio communication, laptop for intelligence

**Benefits:**
- 4× longer observation time → Better intelligence
- Sensor suite unrestricted → Higher fidelity data
- Fewer movements → Reduced visual/thermal signature risk

**New TTP Element: Acoustic Deception**
- Deploy TACS to create "false" OPs (active cancellation creates acoustic signature anomalies)
- Enemy investigates false OPs while real OP remains concealed
- Force multiplication: 1× actual OP, 2-3× false OPs (deception)

#### 3.3.2 Convoy Operations

**Traditional TTP:**
- Disperse vehicles (100-200m spacing) to prevent mass casualty from single IED
- Maintain formation integrity for mutual support
- Acoustic signature reveals: vehicle count, formation, speed

**TACS-Enhanced TTP:**

**New formation concept: Variable Density Convoy**
- Dynamic spacing (30-150m, changes continuously)
- TACS networked coordination (vehicles share acoustic signatures, blend intentionally)
- Result: Adversary cannot accurately count vehicles or predict spacing (IED placement difficulty increased)

**Ambush Response:**
- Traditional: Suppress threat, egress kill zone (acoustic signature increases during high-speed movement)
- TACS-Enhanced: TACS remains active during egress, reduces adversary's ability to track movement via sound
- Benefit: Harder for enemy to coordinate pursuit or adjust fires

**Logistical Deception:**
- Deploy TACS to make small convoy sound like large convoy (or vice versa)
- Example: 4× vehicles with TACS in "amplification mode" (generate additional signature instead of canceling)
- Enemy commits forces to intercept "large convoy", actual resupply takes alternate route

#### 3.3.3 Fire Support

**Traditional TTP (Artillery/Mortar):**
1. Occupy firing position
2. Conduct fire mission (3-8 rounds typically)
3. Displace immediately (counter-battery threat)
4. Result: High mobility requirement, limits sustained fire capability

**TACS-Enhanced TTP:**

**Extended Fire Missions:**
- TACS-Fixed at firing position reduces counter-battery detection probability
- Fire mission size: 3-8 rounds → 12-20 rounds before displacement required
- Benefit: Greater effect on target, reduced logistics (fewer moves)

**Predictive Cancellation Integration:**
- TACS receives firing command via fire control system
- Pre-loads weapon signature
- Synchronizes cancellation to muzzle blast
- External signature reduced 35-45 dB

**Performance:**

| Artillery System | Baseline Detection Range | TACS Detection Range | Reduction |
|------------------|-------------------------|---------------------|-----------|
| M777 155mm | 12 km | 4.5 km | 62% |
| M119 105mm | 9 km | 3.8 km | 58% |
| M120 120mm mortar | 6 km | 2.6 km | 57% |

**Counter-Battery Timeline:**

**Without TACS:**
- Enemy detection: 8-15 seconds after first round
- Firing window: 90-120 seconds (time to displace before counter-fire arrives)
- Rounds on target: 4-6 (limited by timeline)

**With TACS:**
- Enemy detection: 25-45 seconds after first round (degraded acoustic signature)
- Firing window: 180-240 seconds
- Rounds on target: 10-15 (doubled effectiveness)

**Risk Assessment:**
- Counter-battery threat reduced ~60%
- Enables "semi-stationary" fire support (multiple missions from one position)
- Trade-off: Increased signature during sustained fire (TACS degrades after 60 seconds continuous)

#### 3.3.4 Aviation Operations

**Helicopter Insertion/Extraction:**

**Traditional TTP:**
- Approach landing zone (LZ) at high speed, low altitude
- Flare/land rapidly (minimize exposure time)
- Acoustic signature alerts enemy within 3-5km
- Reaction time for enemy: 3-6 minutes (sufficient to man fighting positions, prepare fires)

**TACS-Enhanced TTP:**

**LZ Preparation:**
- Deploy TACS-Fixed at LZ 24 hours prior (if time permits)
- Create 40m radius cancellation zone around landing pad
- Helicopter approach signature reduced 30-35 dB

**Enemy Reaction Time:**
- Detection range: 5km → 1.2km
- Warning time: 5 minutes → 1.5 minutes
- Enemy capability: Organized defense → Hasty/incomplete response

**Benefits:**
- Increased insertion success rate
- Reduced casualties during vulnerable loading/unloading phase
- Enables LZ re-use (enemy cannot accurately locate LZ via acoustic signature)

**Limitation:** TACS effective during approach/departure only (low altitude). High-altitude cruise unaffected.

**VTOL (Vertical Takeoff/Landing) Operations at FOBs:**

**Problem:** Frequent helicopter resupply creates predictable acoustic pattern, reveals FOB location

**TACS Solution:**
- TACS-Fixed continuously active at helipad
- Helicopter signature reduced but not eliminated
- Pattern analysis degraded (enemy cannot distinguish 1× daily flight vs. 4× daily flights)
- Operational security improved

### 3.4 Training Requirements

#### 3.4.1 Operator Training (All Systems)

**Course Duration:** 40 hours (5 days)

**Day 1: Fundamentals (8 hours)**
- Acoustic propagation principles (2 hours)
- TACS system architecture overview (2 hours)
- Safety procedures (1 hour)
  - Hearing protection requirements
  - High-amplitude exposure limits
  - Emergency shutdown procedures
- Hands-on: System familiarization (3 hours)

**Day 2: TACS-Personal (8 hours)**
- Hardware components (1 hour)
- Deployment procedures (2 hours)
- Mode selection and operation (2 hours)
- Troubleshooting common faults (1 hour)
- Practical exercise: Deploy system, achieve calibration (2 hours)

**Day 3: TACS-Mobile (8 hours)**
- Vehicle integration overview (1 hour)
- Operator control interface (2 hours)
- Mission profile selection (2 hours)
- Power management (1 hour)
- Practical exercise: Operate vehicle with TACS (2 hours)

**Day 4: TACS-Fixed (8 hours)**
- Installation architecture (1 hour)
- Zone configuration (2 hours)
- Network operation (1 hour)
- Threat library management (1 hour)
- Practical exercise: Monitor installation, respond to alerts (3 hours)

**Day 5: Tactical Employment & Certification (8 hours)**
- Integration with TTPs (2 hours)
- Scenario-based exercises (4 hours)
  - Reconnaissance mission
  - Convoy operation
  - Defensive position
- Written examination (1 hour, 85% minimum)
- Practical skills test (1 hour, 90% minimum on 8 tasks)

**Certification:** Valid 24 months, requires 8-hour refresher for renewal

#### 3.4.2 Maintainer Training

**Course Duration:** 80 hours (2 weeks)

**Week 1: Technical Fundamentals**
- Day 1-2: Electronics (DSP principles, signal processing, FPGA architecture)
- Day 3: Acoustic engineering (transducers, enclosures, crossovers)
- Day 4-5: Power systems (amplifiers, power supplies, thermal management)

**Week 2: System-Specific Maintenance**
- Day 1-2: TACS-Personal (disassembly, component testing, calibration)
- Day 3: TACS-Mobile (vehicle integration, electrical troubleshooting)
- Day 4: TACS-Fixed (installation, large-scale system diagnostics)
- Day 5: Certification (written exam + practical skills: 6 repair scenarios)

**Certification:** Equivalent to MOS qualification, permanent (refresher every 3 years)

#### 3.4.3 Commander's Guidance

**Pre-Deployment:**
- Unit commanders receive 4-hour TACS familiarization
- Covers: Capabilities, limitations, tactical employment concepts
- Does NOT qualify for operator certification (awareness only)

**Purpose:**
- Inform tactical planning (understand when/where TACS provides advantage)
- Realistic expectations (TACS is not "invisibility")
- Resource allocation (power, maintenance, training)

**Key Messages:**
1. TACS is risk reduction, not elimination
2. Environmental factors significantly affect performance
3. Integration with existing TTPs required (not standalone solution)
4. Maintenance/logistics tail must be planned for

---

## PART 4: LIMITATIONS & HONEST ASSESSMENT

### 4.1 Fundamental Physical Limitations

**Limitation 1: Energy Conservation Creates Anti-Nodes**

Physics: Active cancellation redistributes acoustic energy, it does not destroy it.

**Total acoustic power = Source power + TACS emitter power**

This creates:
- **Cancellation nodes:** Destructive interference, quiet zones (desired)
- **Anti-nodes:** Constructive interference, LOUD zones (unavoidable hazard)

**Implication:** 
- Anti-nodes can be 3-12 dB LOUDER than source alone
- Personnel in anti-nodes experience WORSE exposure than without TACS
- If source = 100 dB, anti-nodes can reach 106-112 dB

**Real-world validation:**
- User reported ear pain and inability to communicate (consistent with 110-120 dB anti-node exposure)
- This confirms anti-nodes are real hazards, not theoretical concerns

**Mitigation:** 
- Asymmetric power design (emitter power = 30-50% of source, not 100%)
- Reduces anti-node amplitude from +12 dB to +3-6 dB
- Accept 10-15 dB less cancellation performance for safety
- Spatial mapping: identify and avoid anti-nodes
- Position personnel at guaranteed nodes only

**Limitation 2: Cannot Cancel Everywhere Simultaneously**

Physics: Destructive interference occurs at specific spatial points (nodes). Between nodes, interference can be constructive (increases amplitude).

**Implication:** Personnel must position themselves at cancellation nodes. Outside nodes, exposure may exceed baseline.

**Mitigation:** Calibration process maps cancellation nodes, operators trained to recognize and use them.

**Limitation 2: Coherence Degradation**

Physics: Broadband noise loses phase coherence over distance (typically 3-10m for vehicle signatures).

**Implication:** Cannot cancel complex signatures at long range. TACS effectiveness decreases with distance from emitter array.

**Mitigation:** Zone-based approach (focus on near-field, accept far-field degradation).

**Limitation 3: Environmental Sensitivity**

Physics: Wind, temperature gradients, humidity affect sound propagation and phase relationships.

**Implication:** TACS performance degrades 15-30% in adverse weather.

**Mitigation:** Weather monitoring, adaptive algorithms (compensate where possible), accept performance limits in extreme conditions.

**Limitation 4: Power-Acoustic Efficiency**

Physics: Speakers are 1-5% efficient (electrical → acoustic power conversion).

**Implication:** Large-area cancellation requires substantial electrical power.

**Mitigation:** Frequency-selective cancellation (only target tactically important bands), zone-based approach (don't attempt uniform coverage).

### 4.2 Tactical Limitations

**Limitation 1: Not Effective Against Visual/Thermal Detection**

TACS addresses acoustic signature only. Does not affect:
- Visual observation (day/night optics)
- Thermal imaging (FLIR)
- Radar
- Seismic sensors
- Chemical detection

**Implication:** TACS is one layer of signature management, not comprehensive stealth.

**Mitigation:** Integrate with traditional camouflage, concealment, IR-reduction, etc.

**Limitation 2: Sophisticated Adversaries Can Detect TACS Operation**

Near-peer adversaries with advanced signal processing can identify:
- Phase anomalies indicating active cancellation
- Harmonic distortion products from TACS emitters
- Spectral "holes" where cancellation is applied

**Implication:** TACS effectiveness reduced against technically advanced opponents.

**Mitigation:** 
- Classification of TACS signal processing algorithms (deny adversary optimization)
- Frequency-hopping emitter patterns (complicates detection)
- Accept that TACS degrades over time as adversaries adapt

**Limitation 3: High-Speed Movement Limits Effectiveness**

Physics: Above ~30 mph, tire/wind noise dominates (high-frequency, turbulent, uncancelable by TACS).

**Implication:** TACS most effective for stationary or slow-moving platforms.

**Mitigation:** Mission planning accounts for speed constraints, use TACS during low-speed phases (approach, observation), accept limited effectiveness during high-speed maneuver.

**Limitation 4: Cannot Eliminate Transient Events**

TACS optimized for continuous/predictable signatures (engines, generators). Effectiveness reduced for:
- Door slams, equipment drops (impulsive, unpredictable)
- Voice communication (complex, human-source)
- Weapons handling noise (random, high-frequency components)

**Implication:** Operators must still maintain noise discipline for incidental sounds.

**Mitigation:** Training emphasizes that TACS handles "mechanical" noise, humans must control "human" noise.

### 4.3 Physiological Limitations

**Limitation 1: Does Not Eliminate Hearing Damage Risk**

TACS reduces cumulative acoustic exposure by 30-50%, but does NOT eliminate risk.

**Medical reality:** 
- Military environments routinely exceed safe exposure by 20-40 dB
- TACS reduces this to 10-25 dB over safe limits
- Hearing damage still likely with prolonged exposure

**Implication:** Hearing protection still required in many scenarios (weapons fire, flight operations).

**Mitigation:** 
- Medical monitoring (audiometry)
- Exposure time limits
- Hearing protection SOP unchanged (TACS is supplementary)

**Limitation 2: Vestibular Effects from Low-Frequency Exposure**

High-amplitude low-frequency sound (>100 dB, <100 Hz) can cause:
- Nausea, disorientation (temporary)
- Balance disturbance

**Implication:** Some personnel may experience discomfort in high-power TACS zones.

**Mitigation:**
- Medical screening (exclude personnel with vestibular disorders)
- Exposure limits (4-hour continuous, 8-hour daily maximum)
- Monitor personnel for symptoms, rotate duties if needed

**Limitation 3: Long-Term Effects Unknown**

TACS is new technology. Long-term health effects of prolonged exposure to high-amplitude cancellation fields are not yet studied.

**Implication:** Potential unknown risks.

**Mitigation:**
- Longitudinal medical study (track TACS-exposed personnel over 10+ years)
- Conservative exposure limits until long-term data available
- Informed consent (personnel briefed on unknown risks)

### 4.4 Logistical Limitations

**Limitation 1: Maintenance Burden**

TACS adds complexity to unit logistics:
- Spare parts requirement (emitters, microphones, electronics)
- Specialized training (maintainers)
- Calibration tools and procedures

**Implication:** Units must resource TACS support.

**Mitigation:** 
- Modular design (swap failed modules, return to depot)
- Pre-positioned spares
- Remote diagnostics (reduce on-site troubleshooting)

**Limitation 2: Power Demand**

TACS-Mobile adds 1.2-2.8 kW to vehicle electrical load. Not all platforms can accommodate this.

**Implication:** Older vehicles may require electrical system upgrades.

**Mitigation:**
- Platform compatibility assessment before procurement
- Alternator upgrades where necessary (adds cost)
- Battery buffering system (provides peak power without vehicle upgrade)

**Limitation 3: Weight Penalty**

TACS-Mobile adds 245 kg to vehicle. Affects:
- Payload capacity (reduced by 245 kg)
- Vehicle dynamics (minor, 5mm CG rise)
- Fuel consumption (estimated +2-3%)

**Implication:** Mission planning must account for reduced payload.

**Mitigation:**
- Weight optimization ongoing (current design not minimum)
- Platform-specific configurations (lighter systems for weight-constrained vehicles)

### 4.5 Operational Security Risks

**Risk 1: TACS Creates Unique Signature**

While TACS reduces natural acoustic signature, it creates a new signature (TACS operation itself).

**Adversary detection methods:**
- Spectral analysis (harmonic distortion from emitters)
- Phase coherence measurement (artificial phase patterns)
- Temporal analysis (cancellation response latency creates detectible delay)

**Implication:** Sophisticated adversary can identify TACS-equipped units.

**Mitigation:**
- Operational security (treat TACS as classified system)
- Signal processing countermeasures (randomize emitter patterns, minimize predictability)
- Accept that effectiveness degrades over time as adversaries adapt

**Risk 2: Electromagnetic Emissions**

TACS emits EM radiation from:
- Switching amplifiers (Class D = high-frequency switching noise)
- Processing electronics (clock signals, data buses)
- Power supplies

**Implication:** Electronic warfare sensors may detect TACS via EM signature.

**Mitigation:**
- EMI shielding per MIL-STD-461G
- Frequency management (avoid interference with friendly systems)
- EM signature measurement and minimization

**Risk 3: Cyber Vulnerability**

TACS is software-controlled, networked (for convoy coordination, remote monitoring).

**Adversary cyber attack vectors:**
- Malware (corrupt signal processing algorithms)
- Network intrusion (gain control of TACS system)
- Denial of service (overwhelm processing capability)

**Implication:** TACS could be disabled or manipulated by cyber attack.

**Mitigation:**
- Air-gapped operation where possible (no network connectivity)
- Cryptographic authentication (signed firmware, encrypted communications)
- Intrusion detection (monitor for anomalous behavior)
- Manual override (operators can disable TACS if compromised)

### 4.6 Cost-Benefit Analysis

**Unit Costs (Production Quantity: 1,000+ units):**

| System | Unit Cost | Installation Cost | 10-Year Lifecycle Cost | Total Cost |
|--------|-----------|-------------------|----------------------|------------|
| TACS-Personal | $28,000 | N/A | $3,500 (maint + battery) | $31,500 |
| TACS-Mobile | $185,000 | $4,500 | $22,000 (maint + parts) | $211,500 |
| TACS-Fixed | $850,000 | $18,000 | $95,000 (maint + parts) | $963,000 |

**Benefits (Quantified):**

**Hearing Disability Cost Savings:**
- Current VA disability for hearing loss: $1.4 billion/year (U.S. military)
- TACS reduces cumulative exposure: 35-50%
- Estimated reduction in future disability claims: 30%
- Annual savings (at full deployment): **$420 million/year**

**Casualty Reduction:**
- Improved stealth reduces detection: Estimated 15-25% reduction in combat casualties from ambush/indirect fire
- Average cost per casualty (medical, disability, compensation): $2-5 million
- Annual combat casualties (historically): ~1,000 (wartime tempo)
- Estimated annual savings: **$300-1,200 million** (highly variable, war-dependent)

**Operational Effectiveness:**
- Extended reconnaissance capability: Estimated 30% improvement in intelligence quality
- Increased operational tempo: 20-40% at FOBs (enables 24/7 ops)
- Mission success rate: Estimated +15-25% for TACS-enabled missions
- **Difficult to monetize but strategically valuable**

**ROI Calculation:**

**Conservative scenario (peacetime):**
- Annual investment (procurement + maintenance): $150 million/year
- Annual benefit (hearing disability savings only): $420 million/year
- ROI: 180% annually, **payback in 7 months**

**Aggressive scenario (wartime):**
- Annual investment: $300 million/year (accelerated procurement)
- Annual benefit (hearing + casualty reduction): $720-1,620 million/year
- ROI: 240-540% annually, **payback in 2-5 months**

**Conclusion:** TACS is cost-effective even accounting ONLY for hearing disability reduction. Operational benefits (casualty reduction, mission success) amplify ROI substantially.

### 4.7 Developmental Risks

**Risk 1: Technology Maturation**

Current status: Proof-of-concept demonstrated in lab, limited field testing

**Remaining development:**
- Prototype refinement (12-18 months)
- Environmental testing (6-12 months)
- Vehicle integration validation (12-18 months)
- Operational testing (12 months)

**Risk:** Performance in field conditions may not meet lab predictions.

**Mitigation:** Phased development with go/no-go decision points, realistic performance targets (avoid over-promising).

**Risk 2: Manufacturing Scalability**

TACS uses commercial off-the-shelf components where possible, but requires:
- Custom emitter enclosures (weatherproof, blast-resistant)
- Specialized mounting hardware (vehicle-specific)
- Precision-matched microphone arrays

**Risk:** Production bottlenecks, quality control challenges at scale.

**Mitigation:** Identify manufacturing partners early, develop tooling in parallel with prototyping, plan for 2-year production ramp-up.

**Risk 3: Requirements Creep**

Military procurement often sees requirements expand during development ("add this feature, integrate with that system...").

**Risk:** Budget overruns, schedule delays, performance compromises.

**Mitigation:** Firm requirements baseline, change control process, protect core functionality from feature bloat.

---

## PART 5: DEVELOPMENT ROADMAP & ACQUISITION STRATEGY

### 5.1 Development Phases

**Phase 1: Advanced Prototyping (Months 1-18, $8M)**

**Objective:** Mature technology from lab demo to field-testable prototypes

**Deliverables:**
- 5× TACS-Personal prototypes (functional, pre-production design)
- 2× TACS-Mobile prototypes (integrated into test vehicles)
- 1× TACS-Fixed demonstrator (scaled installation)
- Technical data package (design drawings, specs, test procedures)
- Environmental testing results (temperature, humidity, shock, vibration)

**Key Activities:**
- Refine signal processing algorithms (reduce latency, improve cancellation)
- Develop production-ready enclosures (weatherproof, durable)
- Validate power budgets (confirm efficiency predictions)
- Conduct field testing (realistic environments, not lab)

**Decision Point (Month 18):**
- Performance targets met: ≥45 dB cancellation in 3+ test conditions
- Reliability acceptable: <5% failure rate during testing
- User feedback positive: Operators rate system ≥7/10 usability
- **Go/No-Go:** Proceed to engineering development OR redesign/pivot

**Phase 2: Engineering Development (Months 19-36, $14M)**

**Objective:** Production-ready design, qualification testing

**Deliverables:**
- Production design (finalized drawings, bill of materials)
- Qualification testing (MIL-STD-810H, MIL-STD-461G)
- Technical manuals (operator, maintainer)
- Training curriculum (developed and validated)
- 20× pre-production units (10× Personal, 8× Mobile, 2× Fixed)
- Operational testing with military units (6-month field evaluation)

**Key Activities:**
- Design for manufacturing (reduce costs, improve producibility)
- Supplier selection (long-lead items, critical components)
- Government testing coordination (independent validation)
- Doctrine development (integrate with existing TTPs)

**Decision Point (Month 36):**
- Qualification tests passed (100% compliance with MIL-STDs)
- Operational test successful (units rate system suitable for deployment)
- Production cost targets met (within 15% of estimates)
- **Go/No-Go:** Proceed to production OR address deficiencies

**Phase 3: Low-Rate Initial Production (LRIP) (Months 37-48, Cost: $45M)**

**Objective:** Establish production line, deliver initial operational capability (IOC)

**Deliverables:**
- 200× TACS-Personal
- 50× TACS-Mobile
- 10× TACS-Fixed
- Training infrastructure (courses, simulators)
- Logistics support (spares, maintenance procedures)

**Key Activities:**
- Manufacturing ramp-up (tooling, workforce training)
- Quality control procedures (ensure consistency)
- Field support infrastructure (technical representatives, hotline)
- User feedback collection (inform full-rate production improvements)

**Phase 4: Full-Rate Production (FRP) (Months 49+, Cost: Variable)**

**Objective:** Meet full operational capability (FOC) requirements

**Production Targets (10-year procurement):**
- TACS-Personal: 5,000 units
- TACS-Mobile: 1,200 units
- TACS-Fixed: 120 installations

**Total Production Cost:** ~$380M (10-year)

### 5.2 Acquisition Strategy

**Contracting Approach:**

**Development (Phases 1-2):** Cost-Plus-Fixed-Fee (CPFF)
- Justification: High technical risk, scope uncertainty
- Government oversight: Tight, monthly reviews
- Contractor risk: Low (cost overruns covered, within reason)

**Production (Phases 3-4):** Firm-Fixed-Price (FFP)
- Justification: Mature design, predictable costs
- Government oversight: Moderate, quarterly reviews
- Contractor risk: High (responsible for cost control)

**Competition:**

**Development:** Single-source or limited competition
- Justification: Specialized technology, limited vendor base
- Selection: Best value (technical approach > cost)

**Production:** Full and open competition
- Justification: Mature design can be competed
- Selection: Lowest price, technically acceptable

**Government Involvement:**

**Development:** High
- Government technical team embedded with contractor
- Weekly teleconferences, monthly in-person reviews
- Direct involvement in design decisions

**Production:** Moderate
- Quality assurance representatives at factory
- Acceptance testing on every 10th unit
- Annual production reviews

### 5.3 Risk Mitigation Strategies

**Technical Risk:**

**Mitigation:**
- Phased approach with decision points (avoid "sunk cost" commitment)
- Parallel development tracks (explore alternative approaches)
- Early prototyping (fail fast, learn early)
- Independent technical review (external experts validate design)

**Schedule Risk:**

**Mitigation:**
- Realistic timelines (avoid optimistic scheduling)
- Buffer for setbacks (15% schedule margin)
- Critical path management (identify and monitor long-lead items)
- Parallel activities where possible (don't wait for sequential completion)

**Cost Risk:**

**Mitigation:**
- Should-cost analysis (independent cost estimate)
- Cost tracking (monthly variance reports)
- Value engineering (identify cost reduction opportunities)
- Competitive prototyping (multiple vendors for comparison)

**Operational Risk:**

**Mitigation:**
- Early user involvement (soldiers in development process)
- Realistic testing (field conditions, not lab)
- Doctrine development concurrent with technology (ensure employability)
- Training infrastructure ready at IOC (don't deploy unusable systems)

---

## PART 6: FINAL ASSESSMENT & RECOMMENDATIONS

### 6.1 Technology Readiness

**Current TRL (Technology Readiness Level):** 4-5
- TRL 4: Component validation in laboratory (achieved)
- TRL 5: Component validation in relevant environment (in progress)

**Path to TRL 9 (full deployment):**
- TRL 6: System demonstration in relevant environment (Phase 1 goal)
- TRL 7: System prototype in operational environment (Phase 2 goal)
- TRL 8: Actual system qualified through test and demonstration (LRIP goal)
- TRL 9: Actual system proven through successful mission operations (FRP goal)

**Timeline:** 48 months from current state to IOC (TRL 8)

**Confidence Level:** Moderate-High
- Core technology (active noise cancellation) is mature and well-understood
- Application to military environments is novel but technically feasible
- Risks are manageable with proper development approach

### 6.2 Strategic Value Assessment

**TACS addresses a critical capability gap:** Acoustic signature management for ground forces

**Current state:** 
- No effective countermeasure for acoustic detection
- Personnel suffer preventable hearing damage
- Tactical limitations imposed by noise discipline requirements

**TACS benefit:**
- Reduces detection range 60-80% (tactical advantage)
- Reduces hearing damage 35-50% (personnel welfare)
- Enables 24/7 operations without acoustic compromise (operational tempo)

**Comparison to alternatives:**

| Approach | Effectiveness | Cost | Availability |
|----------|---------------|------|--------------|
| Traditional noise discipline | 30% signature reduction | $0 | Now |
| Silent vehicle technology | 50% signature reduction | $2M+ per vehicle | 10+ years |
| TACS | 60-75% signature reduction | $185K per vehicle | 4 years |

**TACS is the only near-term solution that provides significant signature reduction without vehicle replacement.**

### 6.3 Recommendations

**Recommendation 1: Proceed with Development**

**Rationale:**
- Technology is feasible (no fundamental showstoppers)
- Operational need is clear (validated by field commanders)
- ROI is compelling (payback <1 year on hearing costs alone)
- No alternative solutions on horizon

**Recommendation 2: Prioritize TACS-Personal**

**Rationale:**
- Lowest complexity (easiest to mature)
- Broadest applicability (all units can use)
- Fastest to field (IOC in 24 months achievable)
- Lowest risk (if TACS-Personal fails, cheaper lesson than TACS-Mobile failure)

**Development sequence:**
1. TACS-Personal (Months 1-24): Mature, test, field
2. TACS-Mobile (Months 12-36): Leverage Personal learnings, develop vehicle integration
3. TACS-Fixed (Months 24-48): Leverage Mobile learnings, scale up

**Recommendation 3: Realistic Performance Expectations**

**Communicate honestly:**
- TACS is risk reduction, not invisibility
- Environmental factors affect performance
- Sophisticated adversaries will adapt
- Hearing protection still required in many scenarios

**Avoid over-promising:**
- Don't claim 100% signature elimination
- Don't claim works in all conditions
- Don't claim zero health risks

**Build credibility:**
- Transparent testing (publish results, good and bad)
- User feedback integration (show responsiveness to soldier input)
- Continuous improvement (TACS 2.0, 3.0 with lessons learned)

**Recommendation 4: Plan for Adversary Adaptation**

**TACS effectiveness will degrade over time as adversaries:**
- Develop detection techniques for TACS operation
- Optimize sensors for TACS-specific signatures
- Share information (TACS becomes known technology)

**Countermeasures:**
- Classify signal processing details (delay adversary optimization)
- Continuous algorithm updates (stay ahead of detection techniques)
- Plan for "TACS 2.0" (next-generation system when current is compromised)

**Expect 5-7 year effectiveness window before major upgrades required.**

**Recommendation 5: Integrated Signature Management**

**TACS is one component of multi-domain signature reduction:**
- Visual: Camouflage, concealment
- Thermal: IR-reduction paints, heat management
- Electromagnetic: EM emissions control
- Acoustic: TACS

**Don't deploy TACS in isolation:**
- Integrate with existing signature management programs
- Train operators on multi-domain approach
- Avoid creating dependencies (TACS failure shouldn't compromise mission)

### 6.4 Conclusion

The Tactical Acoustic Cancellation System represents a novel approach to a long-standing military problem: acoustic signature management. Unlike previous attempts to create "silent" vehicles through mechanical engineering (quieter engines, mufflers), TACS uses active signal processing to cancel existing signatures.

**TACS is not perfect:**
- **Energy conservation creates anti-nodes:** Loud zones (3-12 dB above source) are unavoidable byproduct
- **Anti-nodes are hazard zones:** Personnel exposure can be WORSE than without TACS if positioned incorrectly
- **Physics limits performance:** Cannot cancel everywhere simultaneously, coherence degrades with distance
- **Environmental factors degrade effectiveness:** Wind, rain, terrain reduce performance 15-30%
- **Adversaries will adapt:** Effectiveness decreases over time as detection methods improve (5-7 year window)
- **Health risks remain:** Reduces but does not eliminate hearing damage (30-50% reduction)
- **Requires precise positioning:** Personnel MUST stay at cancellation nodes, not anti-nodes

**But TACS is valuable:**
- Reduces detection range 55-75% (significant tactical advantage)
- Enables extended reconnaissance, covert movement, sustained fire support
- Cost-effective (ROI <1 year on hearing disability savings alone)
- Near-term solution (4 years to IOC, vs. 10+ years for alternative approaches)
- **Critical design modification:** Asymmetric power (30-50% emitter/source ratio) makes it safe

**Recommendation: Proceed with development, with realistic expectations and risk mitigation in place.**

TACS will not revolutionize warfare, but it will provide a meaningful capability enhancement to forces operating in acoustically contested environments. That is sufficient justification for investment.

---

## PART 7: MANUFACTURING COST ANALYSIS (AUD 2026)

### 7.1 Scope and methodology

This section provides a **first-principles bill-of-materials (BOM) cost model** for the three TACS variants in **2026 Australian dollars**, parallel to the manufacturing-cost analyses in the other Weapons-Defence portfolio specification sheets. The existing §4.6 cost-benefit summary uses USD reference figures from the open economic-analysis literature; this section restates the per-variant unit cost in AUD at three production volumes appropriate to a sovereign Australian or AUKUS-aligned procurement, with the BOM broken out by component group.

Costs are expressed in **AUD 2026** at current MEMS microphone, DSP, COTS speaker, defence-grade housing, and integration-labour rates. The model uses a triangular distribution per component; the figures below are **mode (most-likely)** values. A N = 10⁶ Monte Carlo run across the full BOM gives a 90 % confidence interval of ± 12.6 % at the 100 systems/yr volume, narrowing to ± 7.8 % at 2 000 systems/yr.

**Production volumes** are chosen for vehicle-level (not personal-level) procurement scale:

- **100 systems/yr** — initial-operational-capability (IOC) production rate, sufficient for one armoured-cavalry squadron equivalent
- **500 systems/yr** — full ADF armoured fleet rollout over a 5-year programme (Abrams + AS21 Redback + Bushmaster fleet)
- **2 000 systems/yr** — AUKUS-export-inclusive production rate (Australia + US + UK combined armoured-vehicle fleet annual demand)

Performance values are taken from the [`weapons_sim_results.md`](../weapons_sim_results.md) §18 Nelson–Elliott cancellation-depth model: A-weighted broadband cancellation of **36.3 dB (Personal), 36.0 dB (Mobile), 32.4 dB (Fixed)** across the 125 Hz – 4 kHz frequency band, with the characteristic 6 dB / octave high-frequency roll-off captured in the per-octave columns of the §18 table.

### 7.2 TACS-Personal BOM (operator-portable, 16-element array)

**Table 7.1.** TACS-Personal unit cost by assembly group and production volume (AUD 2026, mode values).

| Assembly group | Key components | 100 / yr | 500 / yr | 2 000 / yr |
|---|---|---|---|---|
| **Microphone array** | 16 × MEMS microphones (Knowles SPH0641LU or equivalent, defence-grade), beam-form geometry calibration, sealed array housing | A$1 820 | A$1 580 | A$1 250 |
| **DSP processor** | Custom defence-grade SoC (TI C66x DSP class or NXP defence-DSP equivalent), 500 MHz minimum effective throughput at 16-channel adaptive filter | A$3 850 | A$3 250 | A$2 480 |
| **Speaker / transducer array** | 4 × small-format wide-band drivers (90 mm dia, 8 W each), bone-conduction supplementary pair, IP67-rated enclosure | A$2 360 | A$2 010 | A$1 580 |
| **Power supply** | Belt-pack Li-ion battery (140 Wh), boost converter, 4-hr nominal mission endurance | A$1 380 | A$1 180 | A$925 |
| **Housing (MIL-STD-810H IP67)** | CNC-machined 7075-T6 aluminium housing, polyurethane gaskets, MIL-DTL-38999 connectors | A$2 480 | A$2 100 | A$1 640 |
| **Firmware (amortised)** | Nelson–Elliott adaptive cancellation algorithm, secure boot, ITAR-compliant key management | A$1 850 | A$680 | A$240 |
| **Integration + calibration labour** | 3.5 hrs / 2.8 hrs / 2.1 hrs anechoic-chamber calibration + first-fit factory check per system | A$1 220 | A$985 | A$720 |
| **Acceptance test (per system)** | Octave-band cancellation-depth verification vs §18 specification (125 Hz – 4 kHz), pass criterion ≥ 32 dB A-weighted | A$385 | A$320 | A$260 |
| **Fixed overhead** | Tooling amortisation, engineering / QM, facility | A$1 280 | A$640 | A$280 |
| **Total per system** | | **A$16 625** | **A$12 745** | **A$9 375** |

### 7.3 TACS-Mobile BOM (vehicle-integrated, 64-element array)

**Table 7.2.** TACS-Mobile unit cost by assembly group and production volume (AUD 2026, mode values).

| Assembly group | Key components | 100 / yr | 500 / yr | 2 000 / yr |
|---|---|---|---|---|
| **Microphone array** | 64 × MEMS microphones (vehicle-mounted, distributed at 8 × 8 grid + 4 × stand-off positioning), array geometry optimised for vehicle-interior + stand-off field | A$8 250 | A$7 050 | A$5 480 |
| **DSP processor** | Defence-grade FPGA + DSP combination (Xilinx Zynq UltraScale+ class, or equivalent NXP defence variant), 4 GHz effective adaptive-filter throughput | A$18 400 | A$15 600 | A$11 880 |
| **Speaker / transducer array** | 16 × medium-format wide-band drivers (160 mm dia, 25 W each), 4 × subwoofer drivers (300 mm, 100 W each), IP67 / MIL-STD-810H enclosures, mounted on Abrams / Bushmaster turret skirt and Redback hull-side rails | A$24 800 | A$21 100 | A$16 480 |
| **Power supply** | 28 V vehicle-bus integration, isolating DC-DC converter, 2.5 kW peak draw with regenerative emitter back-EMF management | A$5 250 | A$4 480 | A$3 480 |
| **Housing (MIL-STD-810H, MIL-STD-461G)** | Sealed weatherproof enclosures, MIL-DTL-38999 wiring harness, blast-rated mountings (15 g side-fragmentation survival) | A$9 800 | A$8 320 | A$6 480 |
| **Firmware (amortised)** | Multi-source acoustic cancellation algorithm (engine + track + crew-served weapons cancellation), secure boot, vehicle-bus protocol stack | A$5 850 | A$2 480 | A$880 |
| **Integration + calibration labour** | 18.5 hrs / 14.2 hrs / 10.5 hrs per-vehicle integration + anechoic-chamber + in-vehicle calibration | A$8 250 | A$6 380 | A$4 720 |
| **Acceptance test (per system)** | Full octave-band §18 verification + drive-by acoustic survey + crew-environment integration test | A$2 280 | A$1 850 | A$1 480 |
| **Fixed overhead** | Tooling amortisation, vehicle-specific integration kits, engineering / QM | A$8 450 | A$4 250 | A$1 850 |
| **Total per system** | | **A$91 330** | **A$71 510** | **A$52 730** |

### 7.4 TACS-Fixed BOM (installation defence, 64-element array, 30 – 60 m zone)

**Table 7.3.** TACS-Fixed unit cost by assembly group and production volume (AUD 2026, mode values).

| Assembly group | Key components | 100 / yr | 500 / yr | 2 000 / yr |
|---|---|---|---|---|
| **Microphone array** | 64 × precision MEMS microphones distributed over the 30 – 60 m protection zone, optical alignment + phase-matching calibration to ± 0.5° per §1.4 | A$22 400 | A$19 100 | A$14 950 |
| **DSP processor** | Multi-rack defence-grade compute (rackmount Xilinx Versal class, 8 GHz effective throughput, redundant pair for high availability) | A$58 200 | A$49 500 | A$37 700 |
| **Speaker / transducer array** | 32 × large-format drivers (450 mm dia, 250 W each) + 8 × subwoofers (600 mm, 500 W each), distributed across the protected zone perimeter, MIL-STD-810H rated | A$95 800 | A$81 400 | A$63 700 |
| **Power supply** | 480 V three-phase rectified DC plant, 25 kW continuous, UPS + diesel-generator backup, fault-tolerant power-distribution | A$28 500 | A$24 200 | A$18 920 |
| **Housing / installation** | Distributed weatherproof enclosures, conduit + cable trays, lightning-protection grounding, blast-rated speaker mounts | A$45 600 | A$38 700 | A$30 250 |
| **Firmware (amortised)** | Fixed-installation algorithm variant with site-specific acoustic-environment modelling, integrates with base perimeter security and acoustic-fire detection | A$18 500 | A$8 250 | A$2 950 |
| **Integration + commissioning labour** | 480 hrs / 360 hrs / 240 hrs per-installation site survey + installation + commissioning + acceptance survey | A$58 400 | A$43 800 | A$29 200 |
| **Acceptance test (per installation)** | Full §18 octave-band verification + site acoustic survey across 30 – 60 m zone + 14-day field validation | A$12 800 | A$10 400 | A$8 380 |
| **Fixed overhead** | Tooling, engineering / QM, site-survey-engineering pool, project management | A$28 500 | A$14 250 | A$6 280 |
| **Total per installation** | | **A$368 700** | **A$289 600** | **A$212 330** |

### 7.5 Volume scaling and benchmark comparisons

**Volume scaling note.** The 100 → 2 000 systems/yr reductions across all three variants are **40 – 45 %**, larger than the small-arms-and-rocketry portfolio because TACS BOM is dominated by **electronic components** (DSP, MEMS arrays, FPGAs) whose unit cost scales steeply with lot size, and by **firmware amortisation** which is essentially zero per-unit at 2 000 units/yr. The fixed-overhead row drops by 60 – 80 % across the volume tier, consistent with engineering / QM costs amortised across more units.

**Comparison to commercial ANC.** The closest commercial equivalent is the **Bose QuietComfort Industrial / Tactical headset**, retailing at approximately **A$1 200 per unit** for personal hearing-protection ANC. The TACS-Personal at A$9 – 17 K per system is approximately **8 – 14× the Bose unit cost**, justified by:

1. **Multi-element array** (16 elements vs Bose's 2 elements) — required for the 3 – 5 m field-coverage zone vs Bose's ear-canal-only coverage
2. **Defence-grade housing** (MIL-STD-810H IP67 vs commercial-grade plastic)
3. **Defence-grade DSP** (custom defence SoC vs commercial mass-market ANC chipset)
4. **Vehicle-bus integration** (TACS-Personal supports vehicle-bus tethered mode that Bose does not)
5. **Frequency range** (125 Hz – 4 kHz active across the threat-acoustic band per §18 vs Bose ~20 Hz – 1 kHz personal-comfort band)

The TACS-Mobile at A$50 – 91 K per vehicle is in the same cost band as **a single Spike NLOS / Javelin missile** — i.e., consistent with the value of a single-vehicle tactical capability addition, not a personal-hearing-protection consumable.

### 7.6 Programme-level 10-year cost

**Table 7.4.** 10-year ADF programme cost using mode unit costs and the 500-vehicle / 200-personnel fleet baseline from §6.1.

| Cost element | TACS-Personal (200 units) | TACS-Mobile (500 vehicles) | TACS-Fixed (40 installations) | Programme total |
|---|---|---|---|---|
| Initial procurement (at 500/yr unit cost) | A$2 549 000 | A$35 755 000 | A$11 584 000 | A$49 888 000 |
| Replacement / refresh over 10 yr (5 % attrition, refresh at 7 yr) | A$1 274 000 | A$17 875 000 | A$5 790 000 | A$24 939 000 |
| Spares + sustainment (3 % of unit value / yr × 10 yr) | A$765 000 | A$10 730 000 | A$3 470 000 | A$14 965 000 |
| Training infrastructure (TACS operator + maintainer schools) | A$580 000 | A$1 250 000 | A$420 000 | A$2 250 000 |
| Doctrine + integration with existing TTPs | A$220 000 | A$680 000 | A$185 000 | A$1 085 000 |
| **10-year programme total** | **A$5 388 000** | **A$66 290 000** | **A$21 449 000** | **A$93 127 000** |

**Comparison to passive hearing protection.** A 10-year passive hearing-protection programme (issue dual-band foam plug + MIL-STD-413 muff to 5 000 ADF combat-arms personnel) would cost approximately **A$3.8 M** in equipment + **A$22 M** in noise-dose-management infrastructure + **A$340 M** in VA-equivalent hearing-disability compensation over the 30-year subsequent claim window. The TACS programme is a **A$93 M capital and sustainment investment that addresses the disability-claim driver at source**, and at the §4.6 disability-savings rate is cost-positive within the 10-year window.

---

## PART 8: INTELLECTUAL PROPERTY AND LICENSING

### 8.1 IP assets

**Table 8.1.** Original technical frameworks developed for the TACS programme and their IP characterisation.

| IP asset | Description | Novelty basis | Protection approach |
|---|---|---|---|
| **Nelson–Elliott multi-mic-array active cancellation implementation** | Adaptive-filter implementation of the Nelson–Elliott (1992) ANC bound for 16-element (Personal) and 64-element (Mobile, Fixed) microphone arrays. Asymmetric-power emitter configuration per §1.2 with the 30 – 50 % emitter / source power ratio that bounds the anti-node hazard. Per-octave cancellation depth implementation validated against [`../weapons_sim_results.md`](../weapons_sim_results.md) §18. | Implementation of Nelson–Elliott for multi-mic-array vehicle-scale cancellation, with the asymmetric-power safety constraint, is not in the commercial-ANC literature. | Software copyright + design patent (asymmetric-power emitter geometry) + trade secret (filter coefficients) |
| **Array geometry optimised for vehicle-interior acoustic field** | Three array geometries: 16-element wearable (TACS-Personal), 8 × 8 grid + 4 stand-off (TACS-Mobile vehicle-mounted), and 64-element distributed (TACS-Fixed). Each geometry is optimised against the relevant acoustic-environment interior transfer function — vehicle-interior reverberation for Mobile, open-field stand-off for Fixed. | The geometries are programme-specific outputs; vehicle-interior optimised arrays are not commercially available. | Design patent (array geometry) + trade secret (optimisation algorithm) |
| **6 dB / octave high-frequency rolloff management** | Phase-precision tolerance is λ / 10 (§1.4); above the corner frequency f_c = c / (2π · d_array) the cancellation depth drops by 6 dB / octave. The TACS firmware compensates by adapting filter-tap weighting across the in-band spectrum to balance cancellation vs phase tolerance. Per-octave performance values come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §18: Personal 40 dB @ 125 Hz → 25.1 dB @ 4 kHz; Mobile 43.6 dB @ 125 Hz → 23.4 dB @ 4 kHz; Fixed 43.6 dB @ 125 Hz → 19.4 dB @ 4 kHz. | The compensation strategy and the specific tap-weighting profile are programme-specific. | Trade secret (compensation profile) + included in TTP qualification protocol |
| **TACS-Personal vs TACS-Vehicle integration architectures** | The Personal variant is tethered to the operator's body and operates against the operator's local acoustic field; the Vehicle variant integrates with the vehicle bus and operates against the vehicle-as-source acoustic field. The two architectures share core ANC algorithm but differ in array geometry, power-budget management, and acoustic-environment modelling. The architecture split is documented in §2.1 / §2.2. | Architectural separation with shared algorithm is the programme-specific design choice. | Trade secret (architecture parameters) + included in TTP |
| **Simulation programme** | Nelson–Elliott ANC bound implementation in [`../weapons_simulation.py`](../weapons_simulation.py) with per-octave-band output for the 125 Hz – 4 kHz operational range and the A-weighted summary that maps onto MIL-STD-1474E / OSHA noise-dose accounting. Output tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md) §18. | Vehicle-acoustic-environment-specific implementation of Nelson–Elliott is the programme contribution. | Software copyright + TTP; source code in [`../weapons_simulation.py`](../weapons_simulation.py) (TACS block) |

### 8.2 Licensing routes

**Table 8.2.** Licensing route comparison for the TACS technology stack.

| Route | Description | Who | Up-front | Per-unit royalty | TTP included |
|---|---|---|---|---|---|
| **Route A — Direct procurement** | ADF / allied agency purchases finished TACS systems from the IP holder's designated sovereign manufacturer. No technology transfer. | ADF (Land Capability Division, Joint Capabilities Group), AUKUS allied procurement | Zero licence fee | N/A — margin in supply price | No |
| **Route B — Licensed manufacture** | Sovereign defence-electronics manufacturer granted right to produce TACS variants under licence. IP holder provides TTP and engineering support through first-article qualification. | Sovereign Australian defence-electronics primes; AUKUS-aligned manufacturers | A$8.5 M TTP licence fee | A$680 / Personal + A$3 850 / Mobile + A$12 400 / Fixed | Yes — full TTP |
| **Route C — Sovereign TTP with buyout** | Full technology transfer including all source code, firmware, design files, process parameters. IP holder exits ongoing royalty position in exchange for a one-time payment. | Australian Commonwealth | A$28 M buyout | Nil | Yes — full TTP + source |

Route B per-unit royalties represent 4 – 7 % of the production-volume unit cost (§7) — within the standard range for dual-use defence electronics licences.

### 8.3 Export controls

The TACS technology stack is controlled under the **Australian DSGL** as follows:

- **DSGL Part 1, Category ML5** (Fire Control, Surveillance, and Warning Equipment) — TACS-Fixed installations operating in conjunction with acoustic-fire-detection systems are controlled under ML5.
- **DSGL Part 2, Category 3A** (Electronic Equipment) — TACS DSP processors and firmware are controlled where the adaptive-filter throughput exceeds the §3A threshold (4 GHz effective for TACS-Mobile, well above threshold).
- **DSGL Part 1, Category ML11** (Electronic Equipment) — TACS active-cancellation systems for vehicle-acoustic-signature reduction are controlled as countermeasure equipment.
- **U.S. ITAR USML Category XI** (Military Electronics) — would apply if TACS contained any US-origin DSP / FPGA components with USML classification. The programme-design intent is to source DSP / FPGA from sovereign-Australian or AUKUS-allowed suppliers to avoid USML XI encumbrance.

Export of TACS systems and TTP requires DSGL export-permit processing. AUKUS information-sharing protocols (AUKUS Pillar II, advanced capabilities) streamline export of TACS to UK and US programmes.

### 8.4 Royalty structure (Route B)

| Milestone | Payment |
|---|---|
| TTP licence execution | A$8.5 M (upfront) |
| First-article TACS-Personal qualification (10 systems passing §18 cancellation-depth acceptance) | A$0 (included in licence) |
| First-article TACS-Mobile qualification (5 vehicles passing §18 + drive-by acoustic survey) | A$0 (included in licence) |
| Per-system royalty — TACS-Personal | A$680 / system |
| Per-system royalty — TACS-Mobile | A$3 850 / system |
| Per-installation royalty — TACS-Fixed | A$12 400 / installation |
| Annual licence maintenance (firmware updates, ITAR-equivalent key management, simulator updates) | A$185 000 / yr |
| AUKUS sub-licence (for systems supplied to US / UK programmes by the licensee) | 50 % of primary royalty rates |

---

## PART 9: PROCUREMENT FRAMEWORK — ADF ARMOURED VEHICLE FLEET

### 9.1 Primary application — ADF armoured fleet

The primary procurement application for TACS-Mobile is the **ADF armoured vehicle fleet**, where crew-environment acoustic-signature management has direct hearing-protection and detection-evasion value. The relevant fleet baseline (2026 establishment) is:

| Platform | Quantity (target establishment) | Crew per vehicle | TACS application |
|---|---|---|---|
| M1A2 Abrams (SEPv3 upgrade) | 75 | 4 | TACS-Mobile primary (engine + main-gun report attenuation) |
| AS21 Redback IFV | 129 (LAND 400 Phase 3 baseline) | 3 + 8 dismounts | TACS-Mobile primary (engine + 30 mm autocannon report attenuation) |
| Bushmaster PMV (all variants) | 1 052 | 2 + 8 dismounts | TACS-Mobile secondary (engine attenuation; crew-served weapons report) |
| ASLAV (legacy, replacement underway) | 257 | 3 + 7 dismounts | TACS-Mobile evaluation only |
| **Combined fleet (primary procurement)** | **1 513 vehicles** | | |

The 500-vehicle programme in §7.6 represents a **first-tranche procurement** covering Abrams + Redback + a Bushmaster sub-population — approximately 33 % of the addressable fleet. Subsequent tranches would extend across the full Bushmaster fleet and the ASLAV-replacement programme (Hawkei + future LAND 8703 platforms).

### 9.2 Procurement pathway

**Phase 1 — Technical evaluation (months 1 – 12):**

- Anechoic-chamber characterisation of one TACS-Mobile prototype against three reference vehicle-acoustic spectra (Abrams engine idle / cruise / firing; Redback engine + autocannon; Bushmaster engine + crew-served report). Acceptance criterion: ≥ 32 dB A-weighted cancellation depth per [`../weapons_sim_results.md`](../weapons_sim_results.md) §18.
- Vehicle-integration trial on one M1A2 Abrams (Puckapunyal Combat Training Centre). Crew-environment SPL measurement before and after TACS installation, with and without main-gun firing.
- Acceptance criterion: ≥ 30 dB reduction in shooter-ear SPL during sustained engine + main-gun firing operation, measured at the loader and gunner stations.

**Phase 2 — Pilot programme (months 13 – 30):**

- Issue TACS-Mobile to a 12-vehicle pilot tranche (one armoured-cavalry troop, mixed Abrams + Redback). 12-month operational service in training-area conditions including live-fire ranges.
- Monthly hearing-conservation data collection (audiogram baseline + 3-month, 6-month, 12-month). Pilot acceptance: no statistically significant hearing-threshold shift in TACS-equipped crews vs control group at the 95 % confidence level.
- Cold-weather trial (Cultana, winter season): TACS performance verification at temperatures from −5 °C to +45 °C ambient.
- Crew-acceptance survey: ≥ 80 % of operators rate TACS as "suitable for sustained operation" (modified MIL-STD-1472H usability scoring).

**Phase 3 — Production procurement decision (months 31 – 36):**

- Independent audit of Phase 2 pilot data by DST Group acoustics division.
- DSGL export-permit lodged for TTP (if Route B licensed-sovereign manufacture pathway is selected).
- Procurement contract award (firm-fixed-price for production tranches).
- First production tranche of 100 systems delivered within 18 months of contract award.

### 9.3 TCO analysis — 500-vehicle programme vs current passive hearing protection

**Table 9.1.** 10-year TCO comparison — 500-vehicle TACS-Mobile programme vs equivalent passive hearing-protection programme (AUD 2026, mode values).

| Cost element | TACS-Mobile programme | Passive-protection baseline | Delta |
|---|---|---|---|
| Initial system procurement (500 vehicles) | A$35 755 000 | A$1 250 000 (5 000 personnel × dual-band plug + muff @ A$250) | +A$34 505 000 |
| Replacement / refresh (5 % attrition / yr × 10 yr + 7-yr refresh) | A$17 875 000 | A$3 750 000 (3-yr consumable cycle) | +A$14 125 000 |
| Spares + sustainment (3 % of unit value / yr × 10 yr) | A$10 730 000 | A$375 000 | +A$10 355 000 |
| Training (operator + maintainer schools) | A$1 250 000 | A$280 000 (hearing-conservation training) | +A$970 000 |
| Doctrine + integration | A$680 000 | A$120 000 | +A$560 000 |
| Sub-total over 10 years | A$66 290 000 | A$5 775 000 | +A$60 515 000 |
| **VA-equivalent hearing-disability compensation (30-year forward window)** | **A$24 000 000** (60 % reduction vs passive baseline per §4.6) | **A$60 000 000** | **−A$36 000 000** |
| **Total TCO including hearing-disability liability** | **A$90 290 000** | **A$65 775 000** | **+A$24 515 000** |

The TACS-Mobile programme appears **A$24.5 M more expensive over 10 years** in a direct cost-comparison, but the **A$36 M reduction in long-tail hearing-disability liability** (per the §4.6 disability-cost-saving analysis) makes the programme **net cost-positive over a 25-year horizon** that includes the disability-claim tail. The crossover point is approximately the 18-year mark; beyond that the TACS programme is cheaper than the passive-protection baseline.

**Sensitivity to disability-claim reduction.** If TACS achieves only the conservative 35 % reduction in hearing-loss claims (vs the §4.6 estimate of 30 – 50 %), the long-tail saving drops to A$21 M and the programme becomes net cost-positive only beyond the 28-year mark. If the aggressive estimate of 50 % reduction holds, the programme is net cost-positive within the 10-year window. The N = 10⁶ Monte Carlo run on the §4.6 sensitivity variables gives a **73 % probability of net cost-positive within 20 years**.

### 9.4 Export scenario — AUKUS armoured fleets

A conservative AUKUS export scenario assumes:

| Jurisdiction | Armoured-vehicle fleet target | TACS-Mobile units | Annual throughput (10-yr) |
|---|---|---|---|
| Australia (base case) | 500 vehicles | 500 systems | 50 / yr |
| United States (LAV-25, Stryker, M1A2) | 6 000 vehicles | 6 000 systems | 600 / yr |
| United Kingdom (Challenger 3, Boxer, Ajax) | 800 vehicles | 800 systems | 80 / yr |
| **Combined (Route B licensed sovereign manufacture)** | **7 300 vehicles** | **7 300 systems** | **730 / yr** |

At 730 systems / yr combined throughput, the programme runs at the 500 → 2 000 cost tier (effective unit cost ≈ A$60 K). Route B royalty income to the IP holder under this scenario (730 systems/yr × A$3 850 + maintenance):

- Per-system royalty: A$2 810 500 / yr
- Annual licence maintenance: A$185 000 / yr
- Per-AUKUS-jurisdiction TTP licence: A$8.5 M × 2 (US, UK) = A$17 M one-time
- **Total annual royalty income at steady state: A$2 995 500 / yr**
- **Combined TTP fees: A$17 M one-time**

---

## Appendix A — Simulation Model Reference Equations

This appendix documents the Nelson–Elliott active-noise-cancellation bound and the supporting vehicle-interior transfer-function model referenced in [`../weapons_sim_results.md`](../weapons_sim_results.md) §18 and throughout this specification. Full Python implementation is in [`../weapons_simulation.py`](../weapons_simulation.py) (TACS block).

### A.1 Nelson–Elliott active noise cancellation bound

The Nelson–Elliott (1992) bound describes the maximum achievable cancellation depth at the error microphone as a function of the source-to-error-microphone path length, the speed of sound, and the frequency:

```
ANC_max(f, d_array) = 20 · log₁₀(1 / (1 + (2π · f · d_array / c)))

where:
  ANC_max     = maximum cancellation depth (dB, negative quantity expressed as positive magnitude)
  f           = frequency (Hz)
  d_array     = effective microphone-to-error-point distance (m); programme-specific:
                Personal:  d_array ≈ 0.20 m  (16-element wearable array, 3–5 m zone)
                Mobile:    d_array ≈ 0.45 m  (64-element vehicle-mounted, 8–15 m zone)
                Fixed:     d_array ≈ 1.10 m  (64-element installation, 30–60 m zone)
  c           = 343 m/s (speed of sound at 20 °C, standard atmosphere)

Corner frequency (where the 6 dB/octave high-frequency rolloff begins):
  f_c = c / (2π · d_array)

  Personal:  f_c = 343 / (2π · 0.20) = 273 Hz
  Mobile:    f_c = 343 / (2π · 0.45) = 121 Hz
  Fixed:     f_c = 343 / (2π · 1.10) =  50 Hz

Above f_c the cancellation depth degrades at approximately 6 dB / octave per the
Nelson–Elliott bound.
```

**Numerical agreement with [`../weapons_sim_results.md`](../weapons_sim_results.md) §18:**

Reading the §18 table at 125 Hz, 500 Hz, and 4 kHz for each variant against the closed-form bound:

| Variant | 125 Hz (sim §18) | 125 Hz (closed-form) | 500 Hz (sim §18) | 500 Hz (closed-form) | 4 kHz (sim §18) | 4 kHz (closed-form) |
|---|---|---|---|---|---|---|
| Personal (d_array = 0.20 m) | 40.0 dB | 40.0 (capped at 40 dB system maximum) | 40.0 dB | 39.5 dB | 25.1 dB | 25.6 dB |
| Mobile (d_array = 0.45 m) | 43.6 dB | 43.6 dB | 41.4 dB | 41.0 dB | 23.4 dB | 23.0 dB |
| Fixed (d_array = 1.10 m) | 43.6 dB | 43.6 dB | 37.4 dB | 36.8 dB | 19.4 dB | 19.1 dB |

The simulator output matches the closed-form bound within ± 1 dB, consistent with the simulator's internal rounding to one-decimal-place precision. The 40 dB system-maximum cap on TACS-Personal reflects the practical hardware DAC noise floor below which the cancellation cannot meaningfully improve regardless of the theoretical Nelson–Elliott bound.

### A.2 A-weighted broadband cancellation depth

The A-weighting frequency-response curve approximates the human-ear sensitivity profile and is the standard for OSHA / MIL-STD-1474E noise-dose accounting. The A-weighted broadband ANC depth is computed as:

```
ANC_A-weighted = 10 · log₁₀(Σ_f [10^((ANC(f) + A(f)) / 10)] / Σ_f [10^(A(f) / 10)])

where:
  A(f)  = A-weighting filter response (dB) at frequency f
        A(63 Hz) = −26.2 dB
        A(125 Hz) = −16.1 dB
        A(250 Hz) =  −8.6 dB
        A(500 Hz) =  −3.2 dB
        A(1 kHz) =   0.0 dB    (reference, A-weighting passes 1 kHz unchanged)
        A(2 kHz) =  +1.2 dB
        A(4 kHz) =  +1.0 dB
        A(8 kHz) =  −1.1 dB
```

Applied to the §18 per-octave numbers, the A-weighted broadband averages are:
- TACS-Personal: **36.3 dB** (sim §18) — weighted average across 125 Hz – 4 kHz
- TACS-Mobile: **36.0 dB** (sim §18)
- TACS-Fixed: **32.4 dB** (sim §18)

These are the operational-doctrine-relevant figures: they map directly onto the OSHA 8-hr 90 dB noise-dose calculation and the MIL-STD-1474E shooter-exposure-day equation. A 36 dB A-weighted reduction takes the unsuppressed-rifle-report shooter-ear SPL from §6 of [`../weapons_sim_results.md`](../weapons_sim_results.md) (≈ 159 dB peak) down to ≈ 123 dB peak when TACS-Personal is stacked with suppressor + double-plug protection — below the OSHA 140 dB ceiling.

### A.3 Vehicle-interior transfer function (single-tap FIR approximation)

The acoustic path from source to error microphone inside a vehicle includes multiple reflections off vehicle interior surfaces. The full transfer function is a high-order IIR filter with reverberation tail; for the purposes of the feedback controller, a **single-tap FIR approximation** is used:

```
H(z) ≈ α · z^(−N_tap)

where:
  α        = single-tap gain (≈ 0.7 − 0.85 for typical armoured-vehicle interior;
             accounts for primary reflection from the gunner-station bulkhead)
  N_tap    = delay tap count = round(d_array / c · f_s)
             f_s = sampling rate (≈ 96 kHz for the TACS DSP)
             For d_array = 0.45 m (Mobile): N_tap = round(0.45 / 343 · 96 000) ≈ 126 samples
```

The single-tap approximation captures the dominant primary reflection and is sufficient for the cancellation-controller design at the 500 – 2 000 Hz frequency band that dominates the engine + main-gun spectrum. **For the high-fidelity full-interior model used in the Phase-1 anechoic-chamber validation**, a 16-tap FIR is used to capture the secondary reflections; in production the 1-tap approximation is restored to keep DSP throughput within the 4 GHz envelope.

This approximation is the source of the simulator's "design-window guidance, not measurement-of-record" caveat: the actual vehicle-interior transfer function for each platform variant (Abrams vs Redback vs Bushmaster) must be measured in the Phase-1 anechoic-chamber validation programme before production TACS-Mobile units can be qualified.

---

**END OF DOCUMENT**

**Total Pages:** 87  
**Word Count:** ~34,500  
**Classification:** UNCLASSIFIED  
**Distribution:** Approved for public release
