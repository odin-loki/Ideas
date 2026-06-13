# ACOUSTIC ENERGY CONSERVATION ANALYSIS
## Does TACS Cancel Noise "Completely"?

*Technical Analysis*

Document No. TRP-2026-304 | Version 1.0

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> **TACS acoustic energy-conservation analysis — wave-physics support paper.** First-principles physics analysis backing the anti-node hazard doctrine in `TACS_Complete_Specification.md` and `Paper12_TACS_Energy_Physics.md`. Two coherent sources of equal power superpose to give I = 0 at nodes (∆φ = π) and I = 4·A² at anti-nodes (∆φ = 0), which is **+6 dB above the bare-source SPL** at the anti-node and **4× the baseline intensity**; total acoustic power in the field is the **sum** of source and emitter powers (a 100 W + 100 W matched system puts 200 W into the room, not 0 W). The operational consequence is that active cancellation **redistributes** acoustic energy spatially rather than destroying it — quiet zones at nodes are bought by louder zones elsewhere. The recommended asymmetric-power policy (TACS emitter at 30–50 % of source power) trades ~20 % cancellation depth for ~50 % anti-node-SPL reduction and is the basis for the **35–45 dB cancellation envelope** quoted across the three TACS variants in `weapons_simulation.py` §18. The classification banner above is illustrative for tonal coherence with the rest of the Weapons-Defence portfolio; no real Australian Defence Force programme office, sponsorship, or end-use is implied.

## Honest framing

- **Simulation-based, pre-physical-test.** The 4× / +6 dB anti-node-amplitude figure is a textbook two-source wave-superposition result that requires no measurement to derive; the simulator-side cross-check is the per-octave-band cancellation-depth table in `weapons_simulation.py` §18. No anechoic-chamber free-field measurement of an actual TACS prototype underwrites the doctrine in this paper.
- **Specific physical-limit boundaries that are NOT addressed.** This analysis treats two ideal coherent monochromatic sources in free field. Real deployments involve multiple incoherent broadband sources (multiple engines, multiple weapons signatures), turbulent atmosphere that decorrelates phase over distance, reflective surfaces that create additional interference paths, and human listeners with finite-area ears that integrate over multiple nodes/anti-nodes simultaneously. The 4× / +6 dB figure is an upper bound on the anti-node amplitude penalty; the realised penalty in a complex acoustic environment may be lower for fully coherent threats but worse for partially-coherent multi-source fields where the cancellation control loop chases a moving target.
- **Single source of truth.** The simulator-side numbers (per-octave-band cancellation depth, A-weighted broadband depth, anti-node SPL bound) come from `weapons_simulation.py` and are tabulated in `../weapons_sim_results.md` §18. This analysis is the wave-physics justification for those numbers, not an independent simulator.
- **Power-draw and acoustic-window manufacturing caveats.** Asymmetric 30–50 % emitter power is the doctrine for keeping anti-node SPLs below the 115 dB hazard threshold for a 110 dB source, but the policy assumes the emitter array can sustain the duty cycle at the relevant TACS variant's power band (35–70 W Personal, 800 W–1.8 kW Mobile, 3–8 kW Fixed) — power-bus integration is a deployment-engineering question outside this analysis.
- **Anti-nodes are physics, not malfunction.** The conclusion that personnel must be positioned at calibrated nodes (not arbitrary positions inside the cancellation zone) is the operational corollary of conservation of energy in this paper. Deployment doctrine that treats the cancellation zone as a uniformly safe quiet bubble would expose personnel to anti-node SPLs that can exceed the bare-source SPL by 6 dB; this is a fundamental wave-physics consequence and cannot be engineered away.
- **Classification is illustrative.** UNCLASSIFIED // FOR OFFICIAL USE ONLY is adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real Australian Defence Force programme office, sponsorship, or end-use is implied or held.

---

### Question
If TACS generates anti-phase sound waves to cancel noise, where does the acoustic energy go?

### Physics Analysis

### Conservation of Energy (First Law of Thermodynamics)

Energy cannot be created or destroyed, only transformed or redistributed.

For acoustic systems:
**Total acoustic power = Source power + TACS emitter power**

### Scenario: Single Frequency Tone

**Source (Engine):**
- Frequency: 400 Hz
- Acoustic power: 10 watts
- Amplitude: A₁

**TACS Emitter:**
- Frequency: 400 Hz (same)
- Acoustic power: 10 watts (matching)
- Amplitude: A₂ = A₁
- Phase: 180° out of phase with source

### Wave Interference Mathematics

At any point in space, pressure amplitude:
**P(x,y,z) = A₁·sin(ωt - φ₁) + A₂·sin(ωt - φ₂)**

Where φ₁ and φ₂ are phase angles that depend on distance from each source.

### Case 1: Destructive Interference (Cancellation Node)

When φ₂ - φ₁ = 180° (π radians):
**P = A₁·sin(ωt) + A₂·sin(ωt + π)**
**P = A₁·sin(ωt) - A₁·sin(ωt)**
**P = 0**

Sound is CANCELLED at this location.

### Case 2: Constructive Interference (Anti-Node)

When φ₂ - φ₁ = 0° (sources in phase):
**P = A₁·sin(ωt) + A₂·sin(ωt)**
**P = 2A₁·sin(ωt)**

Sound amplitude is DOUBLED at this location.

### Energy Distribution

**Intensity is proportional to amplitude squared:**

At cancellation node: I = 0² = 0
At anti-node: I = (2A)² = 4A²

But baseline (single source): I = A²

**This means:**
- Cancellation nodes: 0% of baseline intensity
- Anti-nodes: 400% of baseline intensity (4× louder!)

### Total Acoustic Power in the Field

Integrating over all space:

**P_total = ∫∫∫ I(x,y,z) dV**

For two coherent sources of equal power P₀:

**P_total = P₀ + P₀ = 2P₀**

The total acoustic power is the SUM of both sources.

Energy is NOT destroyed - it's redistributed:
- Some locations (nodes): very quiet
- Other locations (anti-nodes): much louder than original source

## The Critical Insight

**TACS does NOT reduce total acoustic energy in the environment.**

**TACS redistributes acoustic energy spatially.**

### Spatial Distribution Example

For TACS-Personal with 3m cancellation zone:

**Volume of cancellation zone:** ~113 m³ (4/3πr³)
**Volume of surrounding space affected:** ~thousands of m³

If 60% of cancellation zone volume experiences good cancellation (60-80% quiet):
- Cancellation volume: ~68 m³

The remaining acoustic energy is pushed into:
- Anti-nodes within the zone (40% of zone volume): ~45 m³ at 2-4× intensity
- Surrounding space outside zone: Distributed at slightly elevated levels

### Energy Accounting

**Original source alone:**
- 100 watts acoustic power
- Spreads uniformly (roughly) over space
- Intensity follows inverse-square law

**With TACS (100W source + 100W emitters = 200W total):**
- 200 watts acoustic power total
- Concentrated in anti-nodes, absent from nodes
- Highly non-uniform spatial distribution

**Net result:**
- Quiet zones exist (mission value)
- But TWICE the acoustic energy is in the environment
- That energy concentrates in anti-nodes (danger zones)

## Why User Experienced Pain

**Possible explanations:**

1. **Position in anti-node:**
   - User was in constructive interference zone
   - Amplitude 2-4× higher than source alone
   - Painful exposure (120+ dB if source was 110 dB)

2. **Near-field emitter exposure:**
   - Close to TACS emitters before cancellation occurs
   - Direct exposure to 120-130 dB emitter output
   - Plus reflected/scattered energy from source

3. **Multiple sources creating complex interference:**
   - Real TACS has many emitters (not just one)
   - Creates complex 3D interference pattern
   - Multiple anti-nodes scattered throughout space
   - User wandered into high-intensity region

## Implications for TACS Design

### Problem: Anti-Nodes Are Hazardous

Traditional TACS concept assumes:
- "Cancellation zone = safe zone"
- "Outside cancellation zone = normal ambient"

**Reality:**
- Cancellation zone contains BOTH nodes (quiet) AND anti-nodes (loud)
- Anti-nodes can be 6-12 dB LOUDER than original source alone
- Personnel in anti-nodes experience WORSE exposure than without TACS

### Solution: Controlled Energy Redistribution

**Design principle:** Push anti-nodes into unoccupied space

**Methods:**

1. **Directional emitters:**
   - Focus cancellation energy toward target zone
   - Anti-nodes form in opposite direction (away from operators)

2. **Asymmetric power:**
   - Don't match emitter power to source power
   - Use LESS emitter power (accept partial cancellation)
   - Reduces anti-node intensity

3. **Spatial design:**
   - Map interference pattern (nodes and anti-nodes)
   - Position operators at guaranteed nodes
   - Ensure anti-nodes are in exclusion zones

### Example: Revised TACS-Personal Design

**Original concept:**
- 100W source, 100W TACS emitters
- Creates 50 dB cancellation in zone
- But also creates +6 dB anti-nodes

**Revised concept:**
- 100W source, 50W TACS emitters (half power)
- Creates 40 dB cancellation (reduced performance)
- Anti-nodes only +3 dB (safer)
- Directional emitters (anti-nodes pushed behind operator)

**Trade-off:**
- 20% less cancellation performance
- 50% reduction in anti-node hazard
- Safer for personnel

## The Uncomfortable Truth

**TACS cannot reduce total acoustic energy in an environment.**

**At best, TACS can:**
1. Create localized quiet zones (tactical value)
2. By concentrating acoustic energy elsewhere (anti-nodes)
3. Total energy in environment INCREASES (source + emitters)

**This means:**
- TACS is fundamentally a "robbing Peter to pay Paul" technology
- It makes some areas quieter by making others louder
- Poor design = anti-nodes in occupied spaces = hearing damage
- Good design = anti-nodes in unoccupied spaces = acceptable

## Recommended Physics-Aware Design

### 1. Accept Partial Cancellation

Don't try for 60 dB cancellation (requires high emitter power, creates dangerous anti-nodes).

Target 35-45 dB cancellation (requires moderate emitter power, manageable anti-nodes).

### 2. Asymmetric Systems

Use emitter power = 30-50% of source power (not 100%).

**Benefits:**
- Reduced anti-node intensity
- Lower electrical power consumption
- Safer for personnel

**Cost:**
- Reduced cancellation depth (but still tactically valuable)

### 3. Predictable Interference Patterns

Design for simple, predictable node/anti-node geometry:

**Good:** Linear array of emitters creates plane-wave pattern (nodes and anti-nodes in parallel planes, easy to predict)

**Bad:** Random emitter positions create chaotic interference (anti-nodes scattered unpredictably)

### 4. Active Anti-Node Suppression

Advanced concept: Monitor SPL throughout space, detect anti-nodes, adjust emitter phases to minimize anti-node amplitude.

**Challenge:** Computationally intensive, requires many sensors

**Benefit:** Flatten spatial distribution (less extreme nodes/anti-nodes)

## Conclusion

**TACS does NOT cancel noise "completely" or "at the source."**

**TACS creates interference patterns with:**
- Quiet zones (nodes): Desired tactical effect
- Loud zones (anti-nodes): Unavoidable byproduct, potential hazard

**Design must:**
1. Map interference patterns
2. Position personnel at nodes
3. Ensure anti-nodes are in safe/unoccupied areas
4. Use moderate emitter power (not maximum)
5. Accept that total acoustic energy INCREASES with TACS operation

**The user's painful experience was likely exposure to an anti-node or near-field emitter output.**

This is not a malfunction - it's fundamental physics of wave interference.

---

## Appendix A — Governing Equations

### A.1 Active Noise Reduction power budget

```
P_ANC = P_DSP + P_mic_array + P_speaker
P_DSP = f_clock × C_switch × V_DD²  (CMOS switching power)
Typical values: f_clock = 200 MHz, C_switch = 50 pF, V_DD = 1.8 V → P_DSP ≈ 32 mW
P_mic (4× MEMS array) ≈ 4 × 0.8 mW = 3.2 mW
P_speaker (dynamic, 8Ω, 0.5W RMS) ≈ 500 mW
Total per channel: ≈ 535 mW
```

### A.2 Acoustic intensity and energy flux

```
I = p²_rms / (ρ × c)   [W/m²]
where p_rms = RMS sound pressure (Pa), ρ = 1.225 kg/m³ (air density), c = 343 m/s
Energy density: E = I / c  [J/m³]
At 166 dB SPL (rifle muzzle): p_rms = 20×10⁻⁶ × 10^(166/20) = 1 262 Pa → I = 4 637 W/m²
```

### A.3 ANC energy conservation

```
E_acoustic_cancelled = E_acoustic_input − E_residual
η_ANC = E_cancelled / E_electrical_input  (system efficiency)
For a well-designed feedforward ANC: η_ANC ≈ 0.15–0.40 (15–40% of electrical input appears as acoustic cancellation)
The Nelson-Elliott bound (from weapons_sim_results.md §18) sets the maximum cancellation depth independent of power; above the bound, additional electrical power does not increase cancellation.
```

### A.4 Battery / power-supply sizing

```
E_battery = P_total × t_operation  [J]
t_operation = 40 h (HANC-1 spec from Hearing Protection/Hearing_Protection_Specification.md)
P_total ≈ 1.07 W per channel (two channels = 2.14 W for full headset)
E_battery = 2.14 × 40 × 3600 = 307 kJ = 85.4 Wh
Nominal Li-ion energy density: 180–250 Wh/kg → battery mass ≈ 340–475 g
→ Matches the 40 h rated life from the spec; confirms feasibility of the Li-ion pack cited in the HANC-1 section.
```
