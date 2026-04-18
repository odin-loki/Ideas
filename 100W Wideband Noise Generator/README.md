# 100W Wideband Noise Generator
## FPGA Control System — Technical Reference and Research Documentation

**Project:** Wideband-White-Noise-Generator  
**Architecture:** Chua-circuit chaotic oscillator + Class AB RF power chain  
**Target output:** 100 W, 1 Hz – 14 GHz  
**Control platform:** FPGA (Verilog RTL, synthesis-ready)  
**Author:** Odin  

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Chua Circuit Theory](#3-chua-circuit-theory)
4. [RF Chain Design](#4-rf-chain-design)
5. [Digital Control System](#5-digital-control-system)
6. [Protection Architecture](#6-protection-architecture)
7. [Mathematical Analysis and Proofs](#7-mathematical-analysis-and-proofs)
8. [Thermal Management](#8-thermal-management)
9. [Power Control Loop](#9-power-control-loop)
10. [Impedance Matching](#10-impedance-matching)
11. [Startup and Shutdown Sequencing](#11-startup-and-shutdown-sequencing)
12. [Timing Analysis](#12-timing-analysis)
13. [Safety and Operational Notes](#13-safety-and-operational-notes)
14. [References](#14-references)

---

## 1. Project Overview

This project implements a 100-watt wideband RF noise generator spanning 1 Hz to 14 GHz, controlled by a synthesisable Verilog state machine targeting FPGA deployment. The noise source is a Chua circuit — the canonical minimal chaotic electronic oscillator — whose broadband, continuous-spectrum chaotic output is conditioned and amplified through a multi-stage RF chain to the rated power level.

Wideband noise sources at this power level have direct applications in RF conducted and radiated susceptibility testing, electromagnetic compatibility (EMC) pre-compliance screening, jamming system characterization, antenna range calibration, and receiver blocking/desensitisation evaluation in defense and telecommunications contexts.

The Chua circuit was selected over avalanche-diode or zener-based noise sources for two reasons. First, its power spectral density is tunable via the LC component values — allowing the spectral shaping of the noise floor across sub-bands without external filters. Second, its chaotic output exhibits sensitivity to initial conditions that makes it cryptographically unpredictable in a way that resistor thermal noise (Johnson-Nyquist) is not, which is advantageous in some ECM and test-signal applications.

The digital controller manages the complete system lifecycle: power supply sequencing, RF chain bias, real-time power control, automatic impedance matching, multi-sensor thermal management, and a comprehensive protection system covering overcurrent, VSWR, arc detection, over-temperature, airflow failure, and door interlock.

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FPGA Control Domain                           │
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │  State   │───▶│  Sequencer   │───▶│  Protection Monitor  │   │
│  │ Machine  │    │  (6 phases)  │    │  (every cycle)       │   │
│  └──────────┘    └──────────────┘    └──────────────────────┘   │
│        │                │                       │                │
│        ▼                ▼                       ▼                │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│  │  Power   │    │  Chua Tune   │    │  Thermal + Fan       │   │
│  │ Control  │    │  (16 bands)  │    │  Management          │   │
│  │  Loop    │    └──────────────┘    └──────────────────────┘   │
│  └──────────┘           │                       │                │
└───────────────┬──────────┴───────────────────────┴───────────────┘
                │ DAC outputs / GPIO
┌───────────────▼─────────────────────────────────────────────────┐
│                    Analogue Hardware Domain                       │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Chua    │───▶│  Driver  │───▶│    PA    │───▶│  Output  │  │
│  │ Circuit  │    │  Stage   │    │  Stage   │    │ Matching  │  │
│  │(chaotic) │    │ (linear) │    │ (100W)   │    │  + Filter │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │   Main   │    │  Bias    │    │ Dir.Cplr │                   │
│  │  SMPS    │    │  Supply  │    │ Fwd/Ref  │───▶ ADC inputs    │
│  └──────────┘    └──────────┘    └──────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### Key sub-systems

**Chua Circuit Core:** Three-state-variable chaotic oscillator implemented with two op-amps, a switched LC network, and a piecewise-linear nonlinear resistor (Chua diode). Variable capacitor bank (16 settings), magnetically-tuned inductor, and switchable resistor network allow the chaotic attractor to be tuned across the intended frequency range.

**RF Amplifier Chain:** Two-stage architecture. A linear driver stage conditions the chaotic signal to a consistent drive level. The power amplifier stage is technology-specific per band: LDMOS for sub-GHz, bipolar / GaAs MESFET for L through C-band, GaN HEMT or InGaP HBT for X-band and above.

**Digital Control (this RTL):** Verilog state machine running on FPGA. Interfaces to all DACs, ADCs, digital I/O, and LCD via parallel buses. Implements closed-loop power control, automatic impedance matching, multi-sensor thermal monitoring, and a two-level protection system (soft + hard).

**Power Supply System:** Sequenced multi-rail architecture. Auxiliary supplies (bias rails) precede the main high-current SMPS. Voltage is ramped to full level under digital control. An SCR crowbar provides sub-microsecond overvoltage / arc protection.

---

## 3. Chua Circuit Theory

### 3.1 Mathematical Model

The Chua circuit is the minimal autonomous electronic circuit satisfying the three necessary conditions for chaos: one or more nonlinear elements, one or more locally active resistors, and three or more energy storage elements. It was first described by Leon O. Chua in 1983 and has since become the canonical experimental platform for chaos research.

The circuit dynamics are described by three coupled nonlinear ordinary differential equations in the dimensionless state variables x(t), y(t), z(t), representing the voltages across capacitors C₁ and C₂ and the inductor current through L₁ respectively:

```
dx/dt = α [ y - x - f(x) ]
dy/dt = x - y + z
dz/dt = -βy
```

The function f(x) is the piecewise-linear voltage–current characteristic of the Chua diode (nonlinear resistor):

```
f(x) = m₁·x + ½(m₁ - m₀)(|x + 1| - |x - 1|)
```

where m₀ and m₁ are the inner and outer slopes of the characteristic respectively. For the canonical double-scroll attractor:

```
m₀ = -1/7  (negative resistance inner segment)
m₁ =  2/7  (positive resistance outer segments)
```

### 3.2 Chaotic Attractor Conditions

The double-scroll chaotic attractor — characterised by bounded aperiodic oscillation between two spiral arms in the (x, y, z) phase space — exists when the physical circuit parameters satisfy:

```
8.5 < α < 10.5
14  < β  < 18
```

where:

```
α_phys = C₂ / (C₁ · R · G)       G = conductance of linear part of Chua diode
β_phys = C₂ / (L₁ · G²)
```

The parameter α controls the time-scale separation between the C₁ dynamics (fast) and the C₂ / L₁ dynamics (slow). The parameter β determines the resonant frequency of the L₁–C₂ loop.

### 3.3 Physical Parameter Mapping from Digital Control Words

The FPGA provides three digital control paths that together set α_phys and β_phys:

**opamp_gain_sel [3:0]:** Selects among 16 gain resistor configurations for the op-amp implementing the negative-resistance Chua diode. Increasing this word increases the transconductance G_m and therefore increases α_phys.

**ind_tune [7:0]:** Drives the DAC controlling the ferrite-core variable inductor L₁. Increasing this word reduces inductance and increases β_phys.

**cap_bank_sel [3:0]:** Selects among 16 switched capacitor configurations setting the C₁/C₂ ratio. Both α_phys and β_phys depend on capacitances; the 16-entry lookup table in `tune_chua_circuit` is designed to track the LC time constant product and maintain the α/β ratio in the chaotic regime as ind_tune sweeps the frequency.

The digital words are dimensionless control ratios. The physical α_phys and β_phys values are determined by the hardware component values; the digital control spans a continuous monotonic range over both parameters simultaneously, with the lookup table encoding the invariant manifold that keeps the system within the chaotic bounds across the frequency sweep.

### 3.4 Noise Power Spectral Density

A Chua circuit operating in the double-scroll regime produces a broadband, continuous-spectrum output with noise-like correlation properties. The power spectral density of x(t) under double-scroll conditions has been shown empirically and analytically to be approximately flat below the characteristic frequency ω₀ = 1/√(LC) and to roll off above it. This makes the circuit functionally equivalent to a wideband noise source whose centre frequency is tunable via L and C.

Research by Muthuswamy, Kennedy, and others has characterised the statistical properties of Chua circuit outputs. Among 40+ continuous-time chaotic systems analysed in recent literature, the Chua double-scroll and the Lorenz system were identified as producing the most Gaussian-like output distributions with the lowest excess kurtosis — a desirable property for noise sources intended to simulate thermal or additive white Gaussian noise (AWGN) channels.

The sum of three independent Chua outputs was shown to closely approximate a true Gaussian distribution via the central limit theorem, with the convergence being measurable to within statistical bounds by the 3-system case.

### 3.5 Sensitivity to Initial Conditions and the Butterfly Effect

A defining property of chaotic systems is sensitive dependence on initial conditions. Two trajectories starting at arbitrarily close initial points in state space diverge exponentially with time, characterised by a positive Lyapunov exponent λ > 0:

```
|δx(t)| ≈ |δx(0)| · e^(λt)
```

For the Chua double-scroll, the largest Lyapunov exponent is approximately λ ≈ 0.16 in normalised time units at α = 9.4, β = 14.3. This exponential divergence means that after a characteristic time τ ≈ 1/λ ≈ 6 time constants, the output is effectively unpredictable from knowledge of the initial state, making the source suitable for applications requiring non-repeating, uncorrelated noise.

---

## 4. RF Chain Design

### 4.1 Band Architecture

The 1 Hz–14 GHz range cannot be served by a single transistor technology. The system uses a switched-matrix output architecture with four PA stages, each optimised for a sub-band:

| Sub-band | Frequency range | Technology | pa_band_sel |
|---|---|---|---|
| 0 | DC – 500 MHz | LDMOS | 0x0 |
| 1 | 500 MHz – 2 GHz | Bipolar / GaAs MESFET | 0x1 |
| 2 | 2 – 6 GHz | GaAs MESFET / GaN | 0x2 |
| 3 | 6 – 14 GHz | InGaP HBT / GaN HEMT | 0x3 |

Selection is automatic via `select_pa_band`, which decodes freq_pot[11:8] and drives both pa_band_sel and filter_bank simultaneously to ensure the correct output harmonic filter is engaged for each band.

### 4.2 Power Amplifier Operating Class

The PA operates in Class AB for all bands. Class AB provides a practical compromise between efficiency (Class B asymptote of 78.5% theoretical) and linearity, which is important here not for spectral purity (a noise source is intentionally non-coherent) but to prevent the amplifier from generating spurious narrowband tones that would corrupt the flat noise PSD.

The quiescent bias current is set via pa_bias according to:

```
pa_bias = 0x600 + (power_pot[11:4] << 4)
```

This scales the quiescent bias upward with increasing power demand, maintaining the Class AB operating point as the transistor moves up its load line.

### 4.3 Driver Stage

The driver provides the pre-amplification and impedance transformation necessary to drive the PA input to the required drive level. It operates in Class A for best linearity, ensuring that the noise signal presented to the PA is a faithful replica of the Chua output rather than a compressed version. The driver bias is:

```
driver_bias = 0x400 + (power_pot[11:4] << 4)
```

### 4.4 Output Filtering and Harmonic Suppression

The filter_bank output selects among output low-pass filters to suppress harmonics of the chaotic signal above the intended operating band. Without filtering, a 100 W source in the 2–6 GHz band would produce significant harmonic power in the 4–14 GHz range, making the output PSD non-flat and potentially interfering with out-of-band measurements.

### 4.5 VSWR Considerations at 100 W

At 100 W output power, the instantaneous voltage across a 50 Ω output port is:

```
V_peak = √(2 · P · R) = √(2 × 100 × 50) = 100 V
```

Under an open-circuit fault (VSWR = ∞), the standing-wave voltage peak doubles to 200 V. Under a short-circuit fault, the peak current doubles to 4 A peak (2 A RMS at 50 Ω). Both conditions are immediately destructive to GaAs and GaN transistors. The protection system must respond within a fraction of a microsecond — which is why the arc_detect and vswr_trip paths bypass the digital state machine and drive fast_shutdown and ps_crowbar directly via the hardware comparator inputs.

---

## 5. Digital Control System

### 5.1 State Machine

The top-level controller implements a seven-state Moore machine:

```
STATE_OFF ──(power_switch ∧ interlocks)──▶ STATE_INIT
STATE_INIT ──(init_complete)──────────────▶ STATE_STANDBY
STATE_STANDBY ──(!standby ∧ ready)────────▶ STATE_STARTUP
STATE_STARTUP ──(startup_done)────────────▶ STATE_RUN
STATE_RUN ──(protection_active)───────────▶ STATE_FAULT
STATE_FAULT ──(!power_switch)─────────────▶ STATE_SHUTDOWN
STATE_SHUTDOWN ──(shutdown_complete)───────▶ STATE_OFF
```

The machine is Moore-encoded (outputs depend on state only). Four tasks (`update_protection`, `manage_cooling`, `update_display`, `measure_fan_tach`) execute unconditionally on every clock edge, independent of the current state.

### 5.2 DAC Interface

All analogue control outputs use a notional 12-bit DAC word. The physical interface (SPI, I²C, or parallel depending on the DAC chosen) is outside the RTL boundary; the Verilog module drives the DAC register words only. The 12-bit resolution provides 4096 control steps across each range, corresponding to approximately 0.024% resolution for power and bias control.

### 5.3 ADC Interface

All analogue monitoring inputs are presented as 12-bit unsigned integers. The ADC sampling rate must be sufficient to support the protection latency requirements (§12). A minimum ADC rate of 1 MSPS is recommended for the protection-critical channels (fwd_power, ref_power, pa_current, temp_sense).

### 5.4 LCD Interface

The HD44780-compatible LCD interface uses 8-bit parallel mode. The format_display task drives a 16-state sequence that writes "Freq: NNNNNN kz" to line 1 of the display. Line 2 carries power level and fault status, updated on alternating display refresh cycles. The enable strobe is explicitly toggled (high then low) within each state to ensure the HD44780 controller latches the data correctly — the data is latched on the falling edge of E according to the HD44780 datasheet.

---

## 6. Protection Architecture

### 6.1 Two-Level Protection Philosophy

The protection system operates at two levels with different response speeds and actions:

**Hardware level (sub-microsecond):** Analogue comparators on vswr_trip, arc_detect, and current_trip directly drive hardware relays or gate turn-off devices. These paths do not pass through the FPGA and are therefore immune to clock-domain latency. The FPGA monitors these inputs and records them in the fault register, but the physical shutdown has already occurred before the FPGA can react.

**Digital level (1–4 clock cycles):** All other protection conditions (over-temperature, ps_fault, airflow failure, door interlock) are evaluated in the `update_protection` task on every clock cycle. Response latency is bounded at 2 clock cycles (sample to output change).

### 6.2 Fault Code Register

A 4-bit priority-encoded fault_code register captures the primary fault condition for display and logging. The priority order reflects destructive potential:

```
Priority 1 (highest): Arc detection        — immediate crowbar
Priority 2:           Overcurrent          — immediate crowbar
Priority 3:           Power supply fault   — controlled shutdown
Priority 4:           Over-temperature    — controlled shutdown
Priority 5:           VSWR trip           — controlled shutdown
Priority 6:           Door interlock      — controlled shutdown
Priority 7 (lowest):  Airflow / EMC       — controlled shutdown
```

### 6.3 Crowbar Operation

The ps_crowbar output triggers an SCR crowbar across the main supply bus. Once triggered, the SCR latches on and clamps the bus to near zero until the gate drive is removed and the SCR is debiased. The crowbar_timer register holds the crowbar active for 256 clock cycles before releasing, giving the supply capacitors time to discharge below the safe level before the SCR turns off. This prevents the crowbar from being inadvertently re-asserted by recovery of the supply voltage before a true safe state has been reached.

### 6.4 Current Fold-Back

In addition to the hard overcurrent trip, a soft current fold-back mechanism reduces the PA drive ceiling proportionally when pa_current exceeds SOFT_CURRENT (0x700). The dynamic drive ceiling foldback_limit is computed each cycle as:

```
foldback_limit = MAX_CURRENT - pa_current   (when pa_current > SOFT_CURRENT)
foldback_limit = 0xFFF                      (otherwise)
```

The pa_drive is then clamped to min(pa_drive, foldback_limit), preventing the control loop from commanding a drive level that would push the transistor into current-limit. This provides a graceful power reduction under marginal load conditions without a hard trip.

---

## 7. Mathematical Analysis and Proofs

### 7.1 Chua Circuit Stability

**Theorem 7.1 (Double-scroll existence):** The Chua circuit exhibits a double-scroll chaotic attractor for all (α, β, m₀, m₁) satisfying the Shil'nikov conditions, which for the canonical parameters (m₀ = -1/7, m₁ = 2/7) reduce to 8.5 < α < 10.5, 14 < β < 18.

**Proof sketch:** The existence proof relies on the presence of a homoclinic orbit in the three-dimensional vector field defined by the Chua equations. Chua, Komuro, and Matsumoto (1986) provided the first rigorous proof via a computer-assisted verification of positive topological entropy. Subsequent work by Galias (1998) provided a fully rigorous interval arithmetic proof. The proof establishes that for the stated parameter ranges, the invariant set of the system has positive topological entropy and therefore the dynamics are chaotic in the mathematical sense (sensitive dependence on initial conditions + topological mixing + dense periodic orbits).

**Implementation note:** The digital control words opamp_gain_sel, ind_tune, and cap_bank_sel are not themselves equal to α and β. They are analogue tuning controls whose effect on α_phys and β_phys is mediated by the physical component values. The digital control system ensures continuous monotonic coverage of the physical parameter space; the hardware design must ensure the covered range includes the chaotic regime.

### 7.2 PA Stability — Rollett Conditions

**Theorem 7.2 (Unconditional PA stability):** A two-port network is unconditionally stable if and only if:

```
K = (1 - |S₁₁|² - |S₂₂|² + |Δ|²) / (2|S₁₂S₂₁|) > 1

|Δ| = |S₁₁S₂₂ - S₁₂S₂₁| < 1
```

**Proof:** Rollett (1962); see also Pozar, "Microwave Engineering," Section 12.3.

The FPGA control system contributes to stability by ensuring the PA is never enabled until bias voltages are stable (§11, Phase 1) and never driven above its characterised stable load-line region. The pa_bias and pa_drive outputs are initialised to safe levels and only increased under closed-loop power control.

### 7.3 VSWR Protection Thresholds

**Definition 7.3:** The voltage standing wave ratio is:

```
VSWR = (1 + |Γ|) / (1 - |Γ|)

|Γ| = sqrt(P_reflected / P_forward)
```

**Proposition 7.4 (Soft threshold):** The condition `ref_power > (fwd_power >> 4)` corresponds to:

```
P_ref / P_fwd > 1/16
|Γ|² > 1/16
|Γ| > 0.25
VSWR > (1 + 0.25)/(1 - 0.25) = 1.25/0.75 ≈ 1.67 : 1
```

**Proof:** Direct substitution into the VSWR formula. The ADC codes are proportional to power (directional coupler + detector diode), so the ratio of codes equals the ratio of powers. ∎

**Proposition 7.5 (Hard threshold):** The vswr_trip hardware input asserts when VSWR exceeds 3:1, corresponding to:

```
|Γ| = (3-1)/(3+1) = 0.5
P_ref / P_fwd = |Γ|² = 0.25
ref_power > fwd_power / 4   (i.e., >> 2 in integer arithmetic)
```

**Two-level interpretation:** The soft threshold (1.67:1, software) triggers impedance matching network adjustment before the hard threshold (3:1, hardware) is reached. The gap provides approximately:

```
ΔVSWR = 3.0 - 1.67 = 1.33   (matching network correction window)
```

within which the 15-step hill-climbing algorithm has time to converge and reduce reflected power to below the hard trip level. At 15 steps × 1 clock cycle per step, the correction window at a 10 MHz clock is 1.5 µs — fast enough for slowly-varying impedance mismatch but not for sudden hard fault conditions (open/short), which are handled by the hardware trip.

### 7.4 Thermal Protection

**Proposition 7.6 (Fan control law correctness):** The fan control law:

```verilog
if (max_temp > WARN_TEMP)      // WARN_TEMP = MAX_TEMP - 0x080
    fan_speed = 0xFF;
else
    fan_speed = 0x20 + max_temp[11:4];
```

provides monotonically non-decreasing fan speed with increasing temperature, with maximum speed engaged 8 °C before the protection trip threshold.

**Proof:**

In the linear regime (max_temp ≤ WARN_TEMP = 0x4D0):

```
fan_speed = 0x20 + (max_temp >> 4)

At max_temp = 0:        fan_speed = 0x20 = 32
At max_temp = WARN_TEMP: fan_speed = 0x20 + 0x4D = 0x6D = 109
```

The function is strictly increasing since max_temp >> 4 is non-decreasing.

In the emergency regime (max_temp > 0x4D0):

```
fan_speed = 0xFF = 255   (maximum)
```

The transition from linear to emergency regime occurs at 77 °C (8 °C below the 85 °C trip), providing full fan speed while there is still a temperature margin, preventing a thermal runaway scenario where the temperature reaches the trip point before cooling is maximised. ∎

**Corollary 7.7:** The linear formula does not reach 0xFF — its maximum is 0x6D = 109 at the 77 °C boundary. Full speed is only reached via the emergency threshold.

### 7.5 Power Control Loop Convergence

**Setup:** Define the power error at step t as:

```
e(t) = target_power - current_power(t)
```

The control law applies:

```
pa_drive(t+1) = pa_drive(t) - step_down    if e(t) < 0  (over-power)
pa_drive(t+1) = pa_drive(t) + step_up      if e(t) > 0  (under-power)

step_down = 0x010 = 16
step_up   = 0x001 = 1
```

**Theorem 7.8 (Convergence bound):** The steady-state error satisfies:

```
lim(t→∞) |e(t)| ≤ step_down + step_up = 0x011 = 17
```

**Proof:** In steady state, the loop either:
1. Has converged to within step_up of target (monotone case, plant gain G is large enough to resolve individual step_up increments): |e_ss| ≤ step_up = 1.
2. Hunts between two consecutive decision points when the plant response to a single step_down places current_power below target, requiring one step_down followed by up to 16 step_up increments before crossing target again. The peak error in this hunt is bounded by step_down + step_up = 17 ADC counts.

The asymmetric step ratio (16:1) is an intentional design choice: over-power is far more dangerous than under-power in a 100 W system, so large corrective steps downward are applied immediately, while power is increased slowly to prevent overshoot. ∎

**Remark:** current_power uses an 8-sample ring-buffer average, which reduces high-frequency noise in the power measurement and prevents limit cycling caused by ADC quantisation noise at the decision threshold.

### 7.6 Impedance Matching Convergence

**Algorithm:** Perturb-and-observe hill climbing over match_ctrl ∈ {0, 1, ..., 15}:

```
if ref_power > fwd_power >> 4:   match_ctrl++  (VSWR above soft threshold)
else:                             match_ctrl--  (VSWR below threshold)
```

**Theorem 7.9 (Convergence under unimodal assumption):** If the function |Γ(k)| = sqrt(P_ref/P_fwd) is unimodal over k ∈ [0, 15] (i.e., has a unique minimum), then the algorithm converges to the minimiser in at most 15 clock cycles from any initial state.

**Proof:** The algorithm implements a binary search on the sign of (|Γ(k)| - threshold). If |Γ(k)| < threshold, the algorithm decrements match_ctrl (moving toward lower k). If |Γ(k)| ≥ threshold, it increments. Under unimodal |Γ|, the threshold crossing occurs exactly once in each direction, and the algorithm cannot cycle without converging because each step reduces |k - k*| by at least one (where k* is the minimiser), unless it is already at the minimum. From any starting k₀, at most |k₀ - k*| ≤ 15 steps are required. ∎

**Physical validity condition:** The unimodal assumption holds when the matching network is a monotone impedance transformation — that is, when increasing match_ctrl monotonically moves the presented impedance in one direction on the Smith chart. This is guaranteed by standard L-network, T-network, and π-network matching topologies but must be verified for the specific hardware implementation.

### 7.7 Current Power Measurement Width

**Proposition 7.10:** The expression `(fwd_power × fwd_power) >> 4` requires a 20-bit result register.

**Proof:**

```
fwd_power ∈ [0, 4095]   (12-bit ADC)
max(fwd_power²) = 4095² = 16,769,025   requires ceil(log₂(16,769,025)) = 24 bits
max(fwd_power² >> 4) = 1,048,064       requires ceil(log₂(1,048,064)) = 20 bits
```

A 12-bit register truncates to 4095. Since 1,048,064 > 4095, truncation occurs for any fwd_power > 255 ADC counts. At typical operating levels (fwd_power ≈ 2048 for 50 W), the truncated value would be approximately:

```
(2048² >> 4) mod 4096 = 1,048,576 >> 4 mod 4096 = 65,536 mod 4096 = 0
```

The power measurement would read zero, completely disabling the control loop. The register must be ≥ 20 bits wide. ∎

---

## 8. Thermal Management

### 8.1 Sensor Array

Eight 12-bit temperature ADC channels are monitored:

| Index | Sensor location |
|---|---|
| 0 | PA transistor case (stage 1) |
| 1 | PA transistor case (stage 2) |
| 2 | Driver transistor case |
| 3 | Inductor core |
| 4 | Primary heatsink (PA mounting face) |
| 5 | Secondary heatsink (driver mounting) |
| 6 | Ambient inlet air |
| 7 | Exhaust air |

The digital controller takes the maximum across all eight sensors as the governing temperature for fan control and protection decisions. This ensures that a localised hot spot (e.g., a single PA transistor running hot due to load imbalance) triggers full cooling and protection regardless of the overall heatsink temperature.

### 8.2 Thermal Margins

At MAX_TEMP = 0x550 (85 °C):

```
WARN_TEMP = MAX_TEMP - 0x080 = 0x4D0 ≈ 77 °C

Warning margin:   85 - 77 = 8 °C before protection trip
Fan linear range: 0 to 77 °C → fan_speed 0x20 to 0x6D
Emergency range:  77 to 85 °C → fan_speed 0xFF
```

The 8 °C margin was chosen to be larger than the expected thermal step response of the heatsink over one fan ramp time, ensuring that the temperature does not coast through the trip point while waiting for the fan to reach full speed.

### 8.3 Rate-of-Rise Monitoring

The digital controller records prev_max_temp each cycle. Systems operating near their thermal limit may be protected by rate-of-rise detection (dT/dt > threshold → preemptive shutdown) in addition to absolute temperature limits. The framework is present in monitor_system; the threshold comparison can be added as needed for specific hardware.

---

## 9. Power Control Loop

### 9.1 Power Measurement

Power is estimated from the forward power ADC via a squared-voltage proxy:

```
P_estimate = (fwd_power)² >> 4   [units: ADC counts²/16]
```

This is proportional to instantaneous RF power delivered to the 50 Ω directional coupler port, assuming a constant-impedance detection diode. For absolute power calibration:

```
P_actual [W] = (fwd_power × V_fs / 4096)² / (R_load × G_coupler × G_detector)
```

where V_fs is the ADC reference voltage, R_load = 50 Ω, G_coupler is the coupler insertion loss, and G_detector is the diode detector conversion factor (V/W).

### 9.2 8-Sample Moving Average

The instantaneous power measurement is noisy due to ADC quantisation and RF envelope fluctuations. An 8-sample ring-buffer average smooths this noise by a factor of √8 ≈ 2.8 in RMS noise amplitude, reducing the threshold for resolving the step_up = 1 count minimum increment.

The averaging introduces a latency of up to 8 clock cycles between a physical power change and its full effect on the control decision. This is acceptable given that the slowest changing target (power_pot, set by a mechanical potentiometer) has a time constant orders of magnitude longer than 8 clock cycles.

---

## 10. Impedance Matching

### 10.1 Matching Network Topology

The match_ctrl output drives a 4-bit (16-state) digitally controlled matching network. Common implementations for wideband use include:

- Switched L-network (series + shunt capacitors, binary-weighted)
- PIN diode switched transmission line sections
- MEMS tunable capacitor arrays

The control algorithm is topology-agnostic; it requires only that |Γ(match_ctrl)| be unimodal over the 16 states, which is typically satisfied by monotone reactive transformations.

### 10.2 Soft vs Hard VSWR Thresholds

The system uses a deliberate gap between the soft matching threshold (VSWR ≈ 1.67:1) and the hard fault threshold (VSWR = 3:1):

```
Soft threshold (adjust):  ref > fwd >> 4    →   |Γ| > 0.25   →   VSWR > 1.67:1
Hard threshold (fault):   vswr_trip input   →   |Γ| > 0.50   →   VSWR > 3.0:1
```

This gap gives the matching algorithm 15 steps and several microseconds to correct a developing impedance mismatch (e.g., due to cable movement or antenna de-tuning) before it escalates to a destructive level. The design follows industry practice for high-power amplifier protection as described by Analog Devices (log-amp VSWR detection, 2017) and Empower RF Systems.

---

## 11. Startup and Shutdown Sequencing

### 11.1 Startup Sequence

The six-phase startup sequence is designed around a monotone partial order on system safety states:

```
s₀(all off) ≼ s₁(aux supplies) ≼ s₂(bias) ≼ s₃(main PS) ≼ s₄(driver) ≼ s₅(PA on)
```

Each phase adds exactly one energised subsystem. No reverse transitions occur during startup. If a fault is detected during startup, the system transitions directly to STATE_FAULT and then STATE_SHUTDOWN, which traverses the de-energisation sequence from phase 0 — the seq_state register is explicitly reset to 8'h00 before entering shutdown to guarantee this.

**Phase timing:**

| Phase | Action | Minimum duration |
|---|---|---|
| 0 | Aux supplies enable | 256 cycles (T_AUX_SETTLE) |
| 1 | Bias voltages up | 512 cycles (T_BIAS_SETTLE) |
| 2 | Main SMPS enable | 768 cycles (T_PS_SETTLE) |
| 3 | Voltage ramp | 255 cycles (0xFF0 / 0x010 steps) |
| 4 | Driver stage on | 1024 cycles (T_DRV_SETTLE) |
| 5 | PA enable | — |
| **Total** | | **≥ 2814 cycles** |

**Voltage ramp design:** The ramp increments ps_voltage by RAMP_STEP = 0x010 each cycle until RAMP_TOP = 0xFF0 is reached. The ceiling is set at 0xFF0 (not 0xFFF) to prevent 12-bit arithmetic wrap-around (0xFF0 + 0x010 = 12'h1000 truncates to 0x000, restarting the ramp indefinitely). At 0xFF0 = 4080 out of 4095 full scale (99.6%), the supply is at rated voltage within measurement precision.

### 11.2 Shutdown Sequence

The shutdown sequence reverses the startup order in four phases: RF disable → voltage ramp-down → supply disable → final de-energisation. The crowbar is de-asserted after the supply has ramped to zero (the SCR latches off once current falls below holding current as the supply discharges).

---

## 12. Timing Analysis

### 12.1 Critical Path Latencies

| Path | Latency | Criticality |
|---|---|---|
| ADC sample → protection output | 2 clock cycles | Critical (100W safety) |
| Power measurement → pa_drive update | 1 cycle (plus avg latency) | High |
| Match_ctrl update per step | 1 cycle | Medium |
| LCD full-refresh (16 states × strobe) | 32 cycles | Low |
| BCD frequency conversion | ≤ 6 cycles | Low |

The protection path (2 cycles) determines the minimum safe clock period. For hardware comparator inputs (vswr_trip, arc_detect, current_trip), the latency is zero — these bypass the digital domain entirely.

### 12.2 Minimum Clock Frequency

The minimum clock frequency is determined by the ADC sampling rate required for protection:

```
T_clk ≤ T_adc / 2    (Nyquist for protection sampling)
```

For a 1 MSPS ADC:

```
f_clk ≥ 2 MHz
```

In practice, FPGA clock rates of 10–100 MHz are typical, providing significant margin and allowing the averaging, display, and matching tasks to run with negligible overhead.

### 12.3 Startup Minimum Time

At a 10 MHz clock (100 ns per cycle):

```
≥ 2814 cycles × 100 ns = 281.4 µs minimum startup time
```

This is dominated by T_DRV_SETTLE (1024 cycles = 102.4 µs). For slower clocks (e.g., 1 MHz), startup time scales proportionally to ≈ 2.8 ms, which remains within all practical limits for a 100 W system.

---

## 13. Safety and Operational Notes

**Before operation:**
- Verify all eight temperature sensors are connected and reading valid values.
- Confirm door interlock and airflow sensor wiring before any power-on.
- Do not defeat the VSWR protection for any reason; at 100 W, a reflected-power event lasts only microseconds before causing permanent transistor damage.
- The SCR crowbar is a one-shot protection device that requires manual inspection before recommissioning after a crowbar event.

**During operation:**
- Monitor the VSWR log register (vswr_log) during initial load connection.
- The soft VSWR threshold will cause match_ctrl adjustments during normal operation; this is expected.
- If fault_latch asserts, the fault_code register captures the cause. Fault_latch requires a manual reset (power cycle or explicit rst_n pulse) to clear.
- Maintain minimum fan speed (MIN_FAN = 0x20) at all times; setting fan_speed to zero risks bearing failure.

**EMC:**
- The emc_filter_ok input must be asserted for the system to enter run state. Do not bypass this interlock — the mains EMC filter is mandatory for regulatory compliance and for protecting the control electronics from RF conducted emissions from the 100 W output stage.

---

## 14. References

1. Chua, L.O., Komuro, M., Matsumoto, T. (1986). "The Double Scroll Family." *IEEE Transactions on Circuits and Systems*, 33(11), 1072–1118.

2. Galias, Z. (1998). "Positive topological entropy of Chua's circuit: A computer-assisted proof." *International Journal of Bifurcation and Chaos*, 7(2), 331–349.

3. Madan, R.N. (1993). *Chua's Circuit: A Paradigm for Chaos*. World Scientific.

4. Kennedy, M.P. (1992). "Robust OP amp realization of Chua's circuit." *Frequenz*, 46(3–4), 66–80.

5. Muthuswamy, B., Kokate, P.P. (2009). "Memristor-based chaotic circuits." *IETE Technical Review*, 26(6), 417–429.

6. Drutarovsky, M., Galajda, P. (2007). "A robust chaos-based true random number generator embedded in reconfigurable switched-capacitor hardware." *Radioengineering*, 16(3), 120–127.

7. Anastasio, V., et al. (2024). "A Deterministic Chaos-Model-Based Gaussian Noise Generator." *Electronics*, 13(7), 1387. https://doi.org/10.3390/electronics13071387

8. Callegari, S., Rovatti, R., Setti, G. (2020). "Generating and Detecting Solvable Chaos at Radio Frequencies with Consideration to Multi-User Ranging." *Sensors*, 20(3), 774. https://doi.org/10.3390/s20030774

9. Pozar, D.M. (2011). *Microwave Engineering*, 4th ed. Wiley. Chapters 11–12 (amplifier design, stability).

10. Rollett, J.M. (1962). "Stability and power-gain invariants of linear two-ports." *IRE Transactions on Circuit Theory*, 9(1), 29–32.

11. Analog Devices (2017). "Log Amps and Directional Couplers Enable VSWR Detection." Technical Article, Analog Devices Inc. https://www.analog.com/en/resources/technical-articles/2017/07/07/log-amps-and-directional-couplers-enable-vswr-detection.html

12. Empower RF Systems. "RF Amplifiers Engineering Notes: Load VSWR and Protection." https://www.empowerrf.com/rf-amplifiers/index.php?topic=load_protection

13. Carrara, F., et al. (2008). "A Methodology for Fast VSWR Protection Implemented in a Monolithic 3-W 55% PAE RF CMOS Power Amplifier." *IEEE Journal of Solid-State Circuits*, 43(10), 2245–2255.

14. Triad RF Systems. "RF Power Amplifiers & High-Power RF Solutions — PA Monitoring and Control." https://triadrf.com/power-amplifiers/

15. HD44780 Datasheet. Hitachi Semiconductor. Rev. 0.0, 1998. (LCD controller interface specification.)

---

*Document generated from verified RTL and mathematical analysis. All proofs are original derivations from cited foundations.*
