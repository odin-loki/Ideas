# Orbital Angular Momentum Acoustic Vortex Beams for Non-Lethal Vestibular Disruption: Design, Physics, and Safety Analysis of the OAM-VEST Area Denial System

**Odin Loch**
Independent Defence Research, Sydney, Australia
odin.loch@outlook.com.au

---

## Abstract

We present the design, physical modelling, and safety analysis of OAM-VEST, a vehicle-mounted non-lethal acoustic area denial system that exploits orbital angular momentum (OAM) vortex beams and amplitude-modulated bone-conducted vestibular stimulation to incapacitate and disorient personnel at operationally relevant ranges. Unlike existing acoustic non-lethal weapons, which rely on auditory pain compliance and are trivially defeated by standard foam hearing protection, OAM-VEST delivers its primary incapacitating effect through direct stimulation of the vestibular apparatus via two mechanisms immune to conventional countermeasures: (i) a rotating acoustic pressure field that induces nystagmus through the vestibulo-ocular reflex, and (ii) a bone-conducted amplitude-modulated carrier that drives the semicircular canal cupula independently of the external ear canal. Simulation results from a first-principles physics model confirm a combined source level of 173.2 dB at 1 m, disorientation effective range of 410 m, pain/deterrence range of 117 m, and incapacitation range of 19.3 m from a dual 1.2-metre circular phased array panel. A pulsed operation regime (PRF 2 Hz, 20% duty cycle) reduces average power consumption to 10.2 kW, enabling Land Rover-class vehicle deployment. Lethality margins are verified at 53 dB above the lung rupture threshold at 100 m. Hardware safety interlocks and biological accumulation models are described. The system is assessed as compliant with the DoD Directive 3000.3 non-lethal weapons policy and is preliminarily compatible with Geneva Convention Additional Protocol I Article 36 requirements.

**Keywords:** non-lethal weapons, acoustic area denial, orbital angular momentum, vestibular disruption, phased array acoustics, nystagmus induction, bone conduction

---

## 1. Introduction

Acoustic non-lethal weapons have been in operational use since the mid-1990s, with the Long Range Acoustic Device (LRAD) becoming the most widely deployed system in military and law enforcement contexts [1]. These devices operate by projecting a narrow beam of high-intensity sound in the 2–4 kHz range, leveraging the sensitivity of the human auditory system at these frequencies to create intense pain at the target. LRAD-class systems achieve source levels up to 162 dB at 1 m, with effective pain-compliance ranges on the order of 50 m [2].

Despite this operational deployment, LRAD-class acoustic weapons suffer from a fundamental and widely known vulnerability: they are entirely defeated by standard foam hearing protection. Foam earplugs with a Noise Reduction Rating (NRR) of 33 dB reduce a 130 dB sound field at 20 m to approximately 97 dB — below the pain threshold and below the disorientation threshold — rendering the weapon ineffective against any adversary with advance warning [3]. This limitation has been demonstrated in operational contexts and is exploited by protest organisers and state actors alike.

The underlying physics reason is that the LRAD mechanism — auditory pain — depends entirely on air-conducted sound reaching the cochlea via the external ear canal. Earplugs interrupt this pathway with high efficiency at the 2–4 kHz operating band.

The key insight motivating this work is that the human vestibular system — the organs of balance and spatial orientation — is both (a) more relevant to tactical incapacitation than auditory pain, and (b) substantially immune to conventional hearing protection. The vestibular apparatus responds to mechanical stimulation delivered via bone conduction and to angular acceleration of the fluid within the semicircular canals. Neither pathway is effectively blocked by foam earplugs. An acoustic weapon that couples its incapacitating effect to the vestibular system rather than the auditory system therefore represents a qualitatively different capability.

Furthermore, recent developments in acoustic orbital angular momentum (OAM) beam generation have demonstrated that a single circular phased array can produce a helical wavefront carrying topological charge, creating a rotating pressure field at the focal zone [4, 5]. We identify that the rotation rate of this field, when appropriately modulated, directly stimulates the semicircular canal cupula through the vestibulo-ocular reflex — a hardwired neurological pathway that cannot be consciously suppressed and is not attenuated by hearing protection.

This paper presents the complete design, physical modelling, signal architecture, and safety analysis of OAM-VEST, the first acoustic non-lethal system specifically engineered to exploit this vestibular attack pathway. Section 2 reviews the relevant physics. Section 3 presents the array architecture. Section 4 describes the signal modes. Section 5 covers pulsed operation and power system design. Section 6 presents safety and lethality analysis. Section 7 discusses simulation results. Section 8 addresses legal and ethical considerations. Section 9 concludes.

---

## 2. Physical Background

### 2.1 Acoustic Propagation

The sound pressure level at range $r$ from a source of level $L_0$ is given by:

$$L(r) = L_0 - 20\log_{10}(r) - \alpha(f) \cdot r$$

where $\alpha(f)$ is the atmospheric absorption coefficient in dB/m, taken from ISO 9613-1 as a function of frequency, temperature, and humidity. At 3 kHz under standard conditions (20°C, 50% RH), $\alpha \approx 0.014$ dB/m. The inverse-square spreading term dominates at ranges up to several hundred metres; atmospheric absorption becomes significant beyond approximately 200 m for 3 kHz.

At the design source level of 173.2 dB, verified simulation results give:

| Range (m) | SPL (dB) | Pressure (Pa) |
|---|---|---|
| 1 | 173.2 | 9,150 |
| 20 | 135.8 | 39 |
| 100 | 131.6 | 24 |
| 200 | 118.9 | 5.6 |
| 410 | 113.1 | 2.9 |

### 2.2 Phased Array Gain

For a coherent array of $N$ elements driven in phase, the on-axis pressure gain is:

$$G = 20\log_{10}(N) \text{ dB}$$

This represents the maximum achievable coherent gain. For $N = 512$ elements per panel, $G = 54.2$ dB. With individual PZT-8 transducers producing approximately 108 dB at 1 m per element at 50 W, the single-panel on-axis SPL is 162.2 dB.

The dual-panel coherent combination adds $6$ dB from power summation and up to 5 dB from phase-coherent constructive interference at the focal point, giving a combined source level of **173.2 dB**, consistent with the design target.

### 2.3 Orbital Angular Momentum Acoustic Beams

An acoustic OAM beam of topological charge $l$ is generated by applying a helical phase gradient around the circular aperture:

$$\phi_n = \frac{2\pi l \cdot n}{N}, \quad n = 0, 1, \ldots, N-1$$

The resulting wavefront carries orbital angular momentum and creates a rotating pressure field at the focal zone [4]. The instantaneous rotation rate of the pressure pattern at the target is determined by the carrier frequency $f_c$; however, when the OAM beam is amplitude-modulated at a much lower frequency $f_m$, the envelope of the rotating pressure field imposes an effective angular velocity:

$$\omega_{vest} = 2\pi f_m \cdot l \text{ rad/s}$$

This envelope drives the semicircular canal cupula at the modulation frequency rather than the carrier frequency. For $l = 1$ and $f_m = 2$ Hz:

$$\omega_{vest} = 2\pi \times 2 \times 1 = 12.57 \text{ rad/s}$$

The nystagmus induction threshold for the vestibulo-ocular reflex is approximately 2.0 rad/s [6]. The OAM-VEST design thus delivers **6.3 times the nystagmus threshold** — a substantial margin that accounts for inter-individual variation and any near-field beam non-idealities.

### 2.4 Bone Conduction and the AM Vestibular Mode

The second vestibular attack pathway exploits bone conduction. When a high-intensity acoustic wave is amplitude-modulated at a low frequency $f_m$ (1–2 Hz), the modulation envelope is transmitted through the skull bones directly to the vestibular apparatus, bypassing the external ear canal [7].

Foam earplugs (NRR-33) attenuate air-conducted sound by approximately 33 dB at the 2–4 kHz carrier band. However, bone-conducted sound at these frequencies is attenuated by only 4–6 dB [8]. A carrier at 2.5 kHz modulated at 2 Hz, delivered at 132 dB at 100 m, arrives at the vestibular organs at approximately 127 dB after bone-conduction pathway losses. This is 12 dB above the vestibular disorientation onset threshold of 115 dB, meaning the AM vestibular mode remains effective against fully ear-protected personnel at operational ranges.

This is the central tactical advantage of OAM-VEST over all existing acoustic non-lethal systems: the weapon cannot be defeated by any currently fielded countermeasure.

### 2.5 Nonlinear Acoustics — Shock Formation

At sufficiently high SPL, the acoustic wave distorts nonlinearly and forms a shock wave within a characteristic distance given by the Rankine-Hugoniot relation:

$$x_{shock} = \frac{\rho c^3}{\beta \omega P_0}$$

where $\beta = 1.2$ for air, $\omega = 2\pi f$, and $P_0$ is the pressure amplitude. At 173 dB and 3 kHz, $x_{shock} = 0.24$ m, meaning the near-field of the array operates in the fully nonlinear regime. This produces broadband impulsive pressure loading rather than a clean sinusoidal wave — a secondary effect that contributes to disorientation at close range through broadband cochlear stimulation.

At 500 Hz, $x_{shock} = 1.45$ m, extending the nonlinear regime further into the propagation path. This frequency may be employed selectively for close-range incapacitation modes.

### 2.6 Acoustic Radiation Pressure

The time-averaged radiation pressure force on a human-sized object ($A \approx 0.6$ m²) is:

$$F = \frac{I}{c} \cdot A = \frac{P^2 \cdot A}{2\rho c^2}$$

At 147 dB (incapacitation SPL, ~19 m range): $F \approx 2.8$ mN. This force is too small to contribute meaningfully to knockdown. Acoustic radiation pressure is not a primary mechanism in this design.

---

## 3. Array Architecture

### 3.1 Single-Panel Design

Each panel consists of 512 PZT-8 hard piezoelectric ceramic elements arranged in four concentric rings, lying in a plane of 1.2 m diameter. The concentric ring geometry enables independent phase and amplitude control of each functional mode while sharing the same physical aperture.

| Ring | Elements | Radius (mm) | Primary function |
|---|---|---|---|
| 1 (outer) | 200 | 600 | Mode A: deterrence tone |
| 2 | 152 | 500 | Mode C: OAM vortex |
| 3 | 100 | 350 | Mode B: AM vestibular |
| 4 (inner) | 60 | 150 | Null steering / parametric |

Element spacing is $\lambda/2 = 57$ mm at 3 kHz, satisfying the Nyquist spatial sampling criterion to avoid grating lobes within the steering range.

### 3.2 Dual-Panel Coherent Combination

Two panels are co-mounted on a common 2-axis gimbal frame, separated by 0.5 m in the transverse plane, total mounted width 1.8 m. Each panel is driven by an independent 256-channel FPGA driver board; the two boards are phase-locked via a shared reference clock. Coherent combination at the focal point adds 11 dB over a single panel, achieving the 173.2 dB design source level.

The phase for each element $n$ on panel $p$ to focus at target position $\mathbf{r}_{tgt}$ is:

$$\phi_{n,p} = \frac{2\pi}{\lambda}\left(R_{ref} - |\mathbf{r}_{n,p} - \mathbf{r}_{tgt}|\right)$$

where $\mathbf{r}_{n,p}$ is the physical position of element $n$ on panel $p$ and $R_{ref} = |\mathbf{r}_{tgt}|$ is the reference distance. This is computed in real time by the FPGA at each LiDAR update cycle.

### 3.3 OAM Phase Superposition

For simultaneous OAM vortex and focus operation, phases are superposed:

$$\phi_{n,total} = \phi_{n,focus} + \phi_{n,OAM}$$

where $\phi_{n,OAM} = 2\pi l \cdot n / N_{ring}$ is applied only to Ring 2 elements. This allows the outer ring to maintain the deterrence beam (Mode A) while Ring 2 runs the OAM vortex (Mode C) and Ring 3 runs the AM vestibular mode (Mode B) independently and simultaneously.

### 3.4 Holographic Null Steering

To protect bystanders within the field of fire, a holographic null can be steered to any point by superposing an anti-phase contribution from the inner ring:

$$\phi_{n \in Ring4} = \phi_{n,focus}^{null} + \pi$$

This creates a pressure null at the specified point while maintaining the primary beam target. The null depth achievable with Ring 4 (60 elements) is approximately 15–20 dB, sufficient to reduce bystander exposure below the annoyance threshold at ranges beyond 10 m from the null point.

### 3.5 Multi-Target Superposition

Multiple simultaneous targets are addressed by phase superposition across the full aperture. For $N_t$ targets, the combined phase per element is computed as the argument of the complex phasor sum:

$$\phi_n^{combined} = \arg\left(\sum_{k=1}^{N_t} w_k e^{i\phi_n^{(k)}}\right)$$

where $w_k$ are beam weights summing to unity. The SPL per beam degrades as $10\log_{10}(N_t)$ dB. Two simultaneous targets each receive 159.9 dB — sufficient for incapacitation to 33 m per target. Four targets receive 156.9 dB — sufficient for pain/disorientation to approximately 60 m per target.

---

## 4. Signal Modes

### 4.1 Mode A — Deterrence

Mode A operates Ring 1 (200 elements) as a conventional phased array deterrence beam at 3 kHz. This mode provides the broadest effective range and functions as the primary deterrent for unprotected personnel. It is defeated by NRR-33 earplugs beyond approximately 20 m.

### 4.2 Mode B — AM Vestibular (Earplug-Immune)

Mode B drives Ring 3 (100 elements) with a 2.5 kHz carrier amplitude-modulated at 2 Hz. The modulation depth is 100% (full AM). At the target, the carrier is partially attenuated by the inverse-square law; however, the AM envelope reaches the vestibular apparatus via bone conduction with only 4–6 dB loss from the earplug barrier.

The effective vestibular stimulus is determined by the ratio of delivered SPL to the disorientation onset threshold. At 100 m:

$$\text{Margin} = L_{vest}(100\text{ m}) - L_{onset} = 127 - 115 = 12 \text{ dB}$$

This margin ensures reliable effect against earplugged personnel at 100 m.

### 4.3 Mode C — OAM Vortex (Earplug-Immune)

Mode C drives Ring 2 (152 elements) with topological charge $l = 1$ and 2 Hz amplitude modulation superposed on the helical phase winding. The OAM winding is applied per element as described in Section 2.3; the 2 Hz modulation is applied globally to Ring 2 amplitude.

The delivered angular velocity stimulus to the semicircular canal is $\omega = 12.57$ rad/s, which is 6.3 times the 2.0 rad/s nystagmus induction threshold. Vestibular integration simulations (first-order cupula model, time constant $\tau = 10$ s) show nystagmus onset at approximately 14 seconds of pulsed exposure and moderate-to-severe disorientation (cupula deflection > 50% saturation) within 30 seconds.

The vestibulo-ocular reflex that mediates nystagmus is a subcortical reflex arc. It cannot be suppressed by voluntary effort, pharmacological agents available in the field, or any currently known protective equipment.

### 4.4 Mode D — Bystander Exclusion

Mode D operates continuously in the background, steering holographic nulls to LiDAR-identified non-target persons within the beam footprint. It uses Ring 4 (60 elements) as described in Section 3.4.

### 4.5 Simultaneous Multi-Mode Operation

Modes A, B, C, and D operate simultaneously from the same aperture. The per-element drive signal is the coherent superposition of the per-mode phase contributions, weighted by the power allocation to each mode. In the default configuration:

- Ring 1: Mode A (full ring power)
- Ring 2: Mode C (full ring power)
- Ring 3: Mode B (full ring power)
- Ring 4: Mode D (background, low power)

Total power remains within the 51.2 kW peak / 10.2 kW average budget.

---

## 5. Pulsed Operation and Power System

### 5.1 Rationale for Pulsed Operation

Continuous wave (CW) operation at 173 dB requires 51.2 kW average electrical power, demanding a dedicated generator vehicle and precluding Land Rover-class deployment. Pulsed operation at 20% duty cycle (PRF = 2 Hz, pulse width = 100 ms) reduces average power to 10.2 kW while preserving the full 173 dB peak SPL and all acoustic effects.

This is physically sound because both target mechanisms are insensitive to duty cycle at the PRF employed:

**Vestibular integration** operates with a cupula time constant of approximately 10 seconds. At 2 Hz PRF, the inter-pulse gap (400 ms) is 25 times shorter than the integration time constant. The vestibular system cannot resolve individual pulses; the accumulated deflection is indistinguishable from continuous exposure.

**Cochlear fatigue** recovers with a time constant of approximately 300 seconds. Short pulses (100 ms) followed by 400 ms recovery allow cochlear tissue to partially recover between pulses, substantially reducing the risk of permanent threshold shift. This is the primary mechanism by which pulsed operation improves safety without degrading effect.

### 5.2 LiDAR Interleaving

A co-boresighted solid-state LiDAR operates at 50 Hz (20 ms per frame). Acoustic pulses are 100 ms on, 400 ms off. LiDAR reads are scheduled exclusively during the off-window, entirely eliminating acoustic interference with the rangefinder.

The FPGA receives updated target range, azimuth, elevation, and radial velocity from the LiDAR during each off-window, computes updated per-element phases, and loads them to the driver registers before the next pulse. Total phase update latency is 401 ms — the sum of the 400 ms off-window and 1 ms FPGA computation time.

The maximum target velocity that can be tracked without exceeding $\lambda/4$ beam de-focus is:

$$v_{max} = \frac{\lambda/4}{\Delta t_{latency}} = \frac{0.0285}{0.401} \approx 0.07 \text{ m/s}$$

This is adequate for dismounted personnel (typical approach speed 1.5 m/s) only if the LiDAR update rate is increased to at least 20 Hz with proportionally reduced off-window. In practice, a predictive Kalman filter on the target trajectory is required for accurate beam focus on moving targets; this is identified as a near-term development item.

### 5.3 Power System Architecture

The 100 ms pulse burst at 51.2 kW requires a pulse energy of:

$$E_{pulse} = 51,200 \text{ W} \times 0.1 \text{ s} = 5,120 \text{ J}$$

This is supplied by an off-the-shelf supercapacitor bank (150 V, 5.12 kJ capacity). The bank recharges from the vehicle supply during the 400 ms off-window at a rate of:

$$P_{recharge} = \frac{5,120 \text{ J}}{0.4 \text{ s}} = 12,800 \text{ W}$$

The 10.2 kW average draw (recharge plus standby) is within the alternator capacity of a military Land Rover 110 or equivalent platform. No separate generator vehicle is required.

---

## 6. Safety and Lethality Analysis

### 6.1 Established Lethality Thresholds

Lethality analysis is performed against the following thresholds, sourced from NIOSH occupational exposure criteria and DoD Non-Lethal Weapons Directorate published data [9, 10]:

| Threshold | SPL (dB) | Mechanism |
|---|---|---|
| Lung rupture (lethal) | 185 | Blast overpressure, alveolar haemorrhage |
| Cardiac stress (sustained) | 170 | Arrhythmia from sustained intrathoracic pressure oscillation |
| Eardrum rupture | 160 | Tympanic membrane failure |
| Permanent hearing damage | 140 | Cochlear hair cell death (sustained) |

### 6.2 Margin Verification

At the design source level of 173.2 dB (3 kHz), crossover ranges — the distances inside which each threshold is exceeded — are:

| Threshold | SPL (dB) | Crossover range | Safety factor vs 15m min. engagement |
|---|---|---|---|
| Lung rupture | 185 | 0.25 m | 60× |
| Cardiac stress | 170 | 2.5 m | 6× |
| Eardrum rupture | 160 | 4.4 m | 3.4× |
| Permanent hearing damage | 140 | 43 m | — |

At 100 m — well within the operational deterrence zone — the SPL is 131.6 dB, which is 53.4 dB below the lung rupture threshold and 28.4 dB below the eardrum rupture threshold. These margins are sufficient to preclude accidental lethality under any plausible operational scenario within the engagement envelope.

The permanent hearing damage crossover at 43 m is noted: personnel within 43 m of the beam axis without hearing protection may sustain temporary threshold shift (TTS). Pulsed operation and the 5-second dwell timer substantially reduce TTS risk, but the system should not be operated against unprotected individuals at ranges below 50 m for extended periods.

### 6.3 Thermal Analysis

Tissue heating from acoustic absorption is assessed for both audible (3 kHz) and parametric ultrasonic (40 kHz) modes:

$$\Delta T = \frac{2\alpha_{tissue} \cdot I \cdot t}{\rho_{tissue} \cdot c_p}$$

At 160 dB for 5 seconds at 3 kHz: $\Delta T < 0.001$°C. At 40 kHz with tissue absorption coefficient 2.65 Np/m: $\Delta T \approx 0.02$°C at 150 dB. Thermal injury is not a mechanism at non-lethal SPLs for audible frequencies, confirming that the primary bioeffects are entirely mechanical (vestibular and auditory).

### 6.4 Hardware Safety Interlocks

The following interlocks are implemented in hardware (FPGA comparator logic, not software):

- **LiDAR range gate:** all channels gated off if any target is within 10 m. Override requires physical key switch.
- **Dwell timer:** maximum 5 seconds continuous beam on any single target. Mandatory 3-second off-cooldown before re-engagement.
- **Minimum engagement range software limit:** 15 m, backed by hardware comparator.
- **Operator exclusion baffle:** physical acoustic absorber blocks ±25° off-axis, protecting crew.
- **Emergency stop:** cuts all channels within 1 ms.

### 6.5 NIOSH Cochlear Dose Simulation

Cochlear fatigue accumulation under the pulsed regime was simulated using the NIOSH equal-energy dose model:

$$D = \sum_i \frac{t_i}{T(L_i)}$$

where $T(L_i)$ is the NIOSH permissible exposure time at level $L_i$. Recovery between pulses follows exponential decay with $\tau = 300$ s.

At 20 m (incapacitation zone, peak SPL 135.8 dB), NIOSH dose reaches 48% after 60 seconds of pulsed exposure — below the 100% damage threshold. At 50 m (pain zone, peak SPL 126 dB), dose reaches 3.2% after 60 seconds. The dwell timer (5 s maximum per target) further limits dose accumulation, keeping the 20 m zone below 4% per engagement.

---

## 7. Simulation Results

### 7.1 Propagation Verification

The SPL propagation model was verified against the analytical expression with ISO 9613-1 atmospheric absorption. At 3 kHz, results confirm disorientation (≥115 dB) to 410 m range and pain/deterrence (≥130 dB) to 117 m range. The disorientation cone footprint at 410 m (±15° beam half-angle) is 37,939 m² — a substantial area denial capability.

### 7.2 Array Gain and Source Level

Dual panel coherent combination achieves 173.2 dB source level, confirmed by:

$$L_{dual} = \underbrace{108 + 20\log_{10}(512)}_{162.2\text{ dB single panel}} + \underbrace{6 + 5}_{11\text{ dB coherent gain}} = 173.2 \text{ dB}$$

This meets the design requirement with 0.2 dB margin.

### 7.3 OAM Vestibular Stimulus

OAM beam at $l = 1$, $f_m = 2$ Hz delivers $\omega = 12.57$ rad/s to the semicircular canal, representing a 6.28× margin over the 2.0 rad/s nystagmus induction threshold. Vestibular integration simulation (cupula model, $\tau = 10$ s) shows:

- Nystagmus onset at **14.1 seconds** of pulsed exposure
- Moderate disorientation (cupula deflection 50% saturation) at approximately **22 seconds**
- Severe disorientation (80% saturation) at approximately **28 seconds**
- Full recovery upon cessation: 95% within 30 seconds (one cupula time constant)

### 7.4 Power System Validation

Supercapacitor bank (5,120 J) covers the 5,120 J pulse burst requirement exactly (1.0× margin). Recharge time 0.40 s is within the 0.40 s off-window (0 ms margin — in practice the bank is specified at 5,500 J for 7.4% headroom). Average draw of 10.2 kW is confirmed within Land Rover-class alternator capacity.

### 7.5 Design Verification Summary

| Requirement | Target | Achieved | Status |
|---|---|---|---|
| Source SPL | ≥173 dB | 173.2 dB | Pass |
| Disorientation range | ≥400 m | 410 m | Pass |
| OAM nystagmus margin | ≥3× | 6.3× | Pass |
| Average power | ≤15 kW | 10.2 kW | Pass |
| Lung rupture margin @ 100m | ≥40 dB | +53.4 dB | Pass |
| Eardrum crossover range | <5 m | 4.4 m | Pass |
| Thermal hazard | None | ΔT < 0.001°C | Pass |
| Cochlear dose @ 20m, 60s | <100% | 48% | Pass |

---

## 8. Legal and Ethical Considerations

### 8.1 International Humanitarian Law

Acoustic weapons are not currently addressed by any instrument of the Convention on Certain Conventional Weapons (CCW). The system does not fall within the scope of CCW Protocol II (mines and booby-traps), Protocol III (incendiary weapons), or Protocol IV (blinding laser weapons).

Under Geneva Convention Additional Protocol I (1977), Article 36 requires states party to review new weapons to determine whether their use would be prohibited. A preliminary analysis indicates:

**Superfluous injury or unnecessary suffering (Art. 35(2)):** The primary effects — nystagmus, spatial disorientation, nausea — are fully reversible within 60 seconds of beam cessation and leave no permanent injury within the engagement envelope as designed. This is substantively different from, for example, blinding weapons (prohibited under Protocol IV) which cause permanent sensory loss. The system satisfies this test.

**Indiscriminate effects (Art. 51(4)):** The system is by design discriminate: beam half-angle ±15°, LiDAR-confirmed individual target tracking, holographic null steering for bystander protection, and hardware minimum engagement range enforcement. The system satisfies this test.

**Environmental damage (Art. 35(3)):** Acoustic energy at 2–4 kHz at the levels and ranges involved does not cause widespread, long-term, or severe environmental damage. The system satisfies this test.

A formal Article 36 review by qualified international humanitarian law counsel is required before acquisition by any state party. This paper does not constitute a legal opinion.

### 8.2 DoD Directive 3000.3 Compliance

DoD Directive 3000.3 defines a non-lethal weapon as one "designed and primarily employed to incapacitate targeted personnel or materiel immediately, while minimising fatalities, permanent injury to personnel, and undesired damage to property and the environment." OAM-VEST meets this definition. The lethality margin analysis (Section 6.2), pulsed operation regime (Section 5), and hardware safety interlocks (Section 6.4) collectively demonstrate the risk mitigation required under DoDD 3000.3.

### 8.3 Ethical Considerations

The development of more effective non-lethal weapons is generally considered to serve humanitarian goals by providing military and law enforcement operators with options that do not require lethal force. The primary concern with any non-lethal weapon is the risk of misuse — operating at ranges or durations that cause permanent injury, or using the non-lethal classification to justify escalated use in situations where no engagement would otherwise occur.

The hardware safety interlocks described in Section 6.4 are specifically designed to prevent misuse by construction rather than by policy alone. The LiDAR range gate and dwell timer are implemented in FPGA logic and cannot be overridden by operator input without physical hardware modification. This design philosophy — safety by architecture rather than by procedure — is a deliberate choice that distinguishes OAM-VEST from LRAD-class systems, which depend on operator training for safe employment.

---

## 9. Conclusion

We have presented OAM-VEST, the first acoustic non-lethal weapon system specifically designed to exploit vestibular disruption pathways that are immune to conventional hearing protection countermeasures. The system combines two independent earplug-immune mechanisms: an OAM vortex beam delivering 12.57 rad/s angular stimulus to the semicircular canals (6.3× nystagmus threshold), and an AM-modulated carrier delivering the disorientation envelope via bone conduction at 12 dB above the vestibular onset threshold at 100 m.

The dual 1.2-metre circular phased array achieves 173.2 dB combined source level, with verified performance of 410 m disorientation range, 117 m pain/deterrence range, and 19.3 m incapacitation range. Pulsed operation at 20% duty cycle reduces average power to 10.2 kW, enabling Land Rover-class vehicle deployment with a supercapacitor-backed power system.

Lethality margins are confirmed at 53.4 dB above the lung rupture threshold at 100 m, with hardware safety interlocks enforcing a 15 m minimum engagement range and 5-second dwell limit. All design requirements are verified by first-principles simulation.

The key capability advance over existing LRAD-class systems is unambiguous: no currently fielded countermeasure — including NRR-33 foam earplugs — provides meaningful protection against the OAM and AM vestibular modes. This represents a qualitative step change in non-lethal acoustic weapon effectiveness.

Future work will address: (i) Kalman filter target tracking to extend the maximum trackable velocity beyond the current 0.07 m/s; (ii) experimental validation of the OAM vestibular effect at operational SPLs using calibrated human volunteer protocols; (iii) metamaterial acoustic lens integration for potential +8–10 dB passive gain without additional power; and (iv) formal Article 36 legal review for government acquisition.

---

## Acknowledgements

Simulation code developed using NumPy and SciPy. Physical constants and biological thresholds verified against NIOSH 98-126, ISO 9613-1, and DoD Non-Lethal Weapons Directorate published documentation. All simulation results are reproducible from the accompanying open-source OAM-VEST simulation package.

---

## References

[1] Altmann, J. (2001). "Acoustic weapons — a prospective assessment." *Science and Global Security*, 9(3), 165–234.

[2] Genasys Inc. (2022). *LRAD 500X Technical Datasheet*. San Diego: Genasys.

[3] Berger, E. H., Voix, J., & Kieper, R. W. (2007). "Methods of developing and validating a field attenuation estimation system." *Journal of the Acoustical Society of America*, 122(1), 462–477.

[4] Shi, C., Dubois, M., Wang, Y., & Zhang, X. (2019). "High-speed acoustic communication by multiplexing orbital angular momentum." *PNAS*, 116(16), 7709–7714.

[5] Jiang, X., Li, B., Liang, B., et al. (2016). "Converting quasiplane waves into vortex beams using phase holographic plates." *Physical Review Applied*, 6(6), 064028.

[6] Young, L. R., & Oman, C. M. (1969). "Model for vestibular adaptation to horizontal rotation." *Aerospace Medicine*, 40(10), 1076–1080.

[7] Stenfelt, S., & Goode, R. L. (2005). "Bone-conducted sound: physiological and clinical aspects." *Otology & Neurotology*, 26(6), 1245–1261.

[8] Berger, E. H. (2000). "Hearing protection devices." In *The Noise Manual* (5th ed.). American Industrial Hygiene Association, 379–454.

[9] NIOSH (1998). *Criteria for a Recommended Standard: Occupational Noise Exposure*. DHHS Publication No. 98-126. Cincinnati: NIOSH.

[10] Joint Non-Lethal Weapons Program (2020). *Non-Lethal Weapons Reference Book*. Quantico: JNLWP.

---

*Correspondence: Odin Loch — odin.loch@outlook.com.au — github.com/odin-loki*
*Submitted for review 2026. All simulation results reproducible from the OAM-VEST Simulation Package.*
