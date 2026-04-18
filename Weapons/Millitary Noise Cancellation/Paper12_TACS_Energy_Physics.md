# Acoustic Energy Conservation in Tactical Active Noise Control: Wave Interference Physics and Anti-Node Hazard Analysis

*Technical Research Paper*

Document No. TRP-2026-012 | Version 1.0

Prepared for: Australian Department of Defence | March 2026

## Abstract
This paper provides a rigorous physics analysis of acoustic energy behaviour in Tactical Active Noise Control \(TACS\) systems, addressing the fundamental question of what happens to acoustic energy when destructive interference cancellation is achieved. The first law of thermodynamics establishes that acoustic energy cannot be created or destroyed—only redistributed. A mathematical analysis of two-source wave superposition demonstrates that while cancellation nodes achieve zero intensity, anti-nodes formed elsewhere in the field achieve 4× baseline intensity \(4A² vs A²\), creating regions substantially louder than the original source alone. The total acoustic power in the field equals the sum of source and emitter powers. This analysis has critical implications for TACS deployment doctrine: anti-nodes are not a malfunction but a fundamental consequence of wave physics, and their location must be determined and managed to prevent hearing damage in the deployed force. Asymmetric emitter power \(30-50% of source power\) is recommended to reduce anti-node severity while accepting a moderate reduction in cancellation depth.

## 1. Introduction

Active noise cancellation is commonly described in terms of what it achieves—quiet zones—rather than what it requires: spatial redistribution of acoustic energy. This framing leads to a misunderstanding of the physics with potentially dangerous operational consequences. If TACS is deployed with the understanding that it "cancels" sound in a zone, operators may position themselves in anti-node regions with no awareness that they are exposed to higher sound intensities than would exist without TACS.

This paper presents the wave physics of two-source acoustic superposition, derives the energy distribution consequences mathematically, and draws practical conclusions for TACS deployment design and doctrine. The analysis is consistent with the conservation of energy \(First Law of Thermodynamics\) and established acoustic wave theory.

## 2. Fundamental Physics

### 2.1 Wave Superposition and Destructive Interference

For a single-frequency tone, the acoustic pressure at any point in space is the sum of contributions from all sources. Consider a noise source and a TACS emitter, both at frequency ω, amplitudes A₁ and A₂:

P\(x,y,z\) = A₁·sin\(ωt − φ₁\) \+ A₂·sin\(ωt − φ₂\)

where φ₁ and φ₂ are phase angles determined by distance from each source to the evaluation point.

At cancellation nodes \(φ₂ − φ₁ = π\): P = A·sin\(ωt\) − A·sin\(ωt\) = 0. Sound intensity I = 0.

At anti-nodes \(φ₂ − φ₁ = 0\): P = 2A·sin\(ωt\). Sound intensity I = \(2A\)² = 4A².

Compared to baseline \(source only\): I\_baseline = A². Therefore, anti-nodes have 4× baseline intensity, corresponding to \+6 dB above the original source. If the original source is 110 dB SPL, anti-nodes can reach 116 dB SPL—well into hearing damage territory for sustained exposure.

### 2.2 Conservation of Energy Accounting

Integrating acoustic intensity over all space, total acoustic power with TACS operating equals source power plus emitter power. For a 100W source with 100W TACS emitters \(matched power\), total acoustic power = 200W. This energy is redistributed—concentrated in anti-nodes, absent from nodes—but the total is conserved. TACS does not remove acoustic energy; it relocates it.

**Condition**
**Total Acoustic Power**
Source only \(100W\)

100 W

TACS operating \(100W source \+ 100W emitters\)

200 W

Asymmetric TACS \(100W source \+ 50W emitters\)

150 W

## 3. Anti-Node Hazard Analysis

### 3.1 Intensity at Anti-Nodes

For a practical TACS-Personal installation with a 100W vehicle engine as the source and 100W TACS emitters:

Source-only intensity at 5m \(inverse-square law\): I = P/\(4πr²\) = 100/\(4π×25\) ≈ 0.32 W/m². Corresponding SPL ≈ 115 dB.

Anti-node intensity: 4 × 0.32 = 1.27 W/m². Corresponding SPL ≈ 121 dB.

NIOSH occupational noise exposure limits specify 95 dB for 1 hour, 100 dB for 15 minutes. At 121 dB, permissible exposure time is approximately 30 seconds. Personnel in anti-nodes of a matched-power TACS system face acute hearing damage risk.

### 3.2 Anti-Node Location Prediction

For a simple two-source system \(one noise source, one TACS emitter\), anti-nodes form on a set of hyperboloids of revolution symmetrically about the axis connecting the two sources. In practice, with multiple emitters and a complex noise source, anti-node geometry becomes three-dimensional and irregular. Computational acoustic modelling is required to map anti-node positions before personnel deployment. This is a non-negotiable design step for any TACS installation.

## 4. Recommended Design Principles

### 4.1 Asymmetric Emitter Power

Using emitter power at 30-50% of source power rather than matched power:

Benefit: Reduces anti-node intensity. At 50% emitter power, anti-node intensity is \(1.5A\)² = 2.25A²—approximately \+3.5 dB above baseline, compared to \+6 dB for matched power. Significantly reduces hearing damage risk in occupied anti-node regions.

Cost: Cancellation depth at nodes is reduced. With 50W emitters cancelling a 100W source, maximum theoretical cancellation depth decreases from complete cancellation to approximately 40-45 dB, depending on geometry and frequency.

Conclusion: For practical TACS deployment, 30-50% emitter power is recommended as the default operating mode, accepting reduced cancellation depth in exchange for manageable anti-node hazard.

### 4.2 Directional Emitter Arrays

Directional emitter arrays concentrate anti-noise energy toward the target zone and form anti-nodes in the opposite direction, away from operators. This requires careful array design and computational optimisation but can substantially improve the ratio of quiet zone volume to anti-node hazard zone volume.

### 4.3 Active Anti-Node Suppression

Advanced TACS designs can monitor sound pressure level \(SPL\) throughout the operational area using a distributed microphone array, detect anti-nodes in real-time, and adjust emitter phases to minimise anti-node amplitude. This approach is computationally intensive and requires high microphone and emitter density, but provides the most comprehensive hazard management. It is recommended for the Fixed variant where the static installation justifies higher sensor infrastructure investment.

## 5. Human Factors: The "Painful Experience" Case

The source document references a user experiencing pain when positioned near a TACS installation. The physics analysis explains this clearly. The user was most likely positioned in an anti-node—a region of constructive interference where TACS emitters combined with the source to produce intensity 3-6 dB above the source alone. This is not a system malfunction; it is an expected consequence of wave physics. The appropriate response is: \(1\) map anti-node positions before personnel entry; \(2\) establish anti-node exclusion zones; \(3\) brief all operators on anti-node hazard before system deployment.

## 6. Mathematical Summary

**Parameter**
**Formula**
Node Intensity

0 × A²

Anti-Node Intensity

4 × A²

Total Power

P\_source \+ P\_emitters

50% Emitter Anti-Node

\(1.5A\)²=2.25A²

## 7. Conclusion

Active noise control systems redistribute acoustic energy—they do not destroy it. Anti-nodes formed in TACS systems can expose personnel to sound intensities substantially exceeding both the original source and safe exposure limits. Asymmetric emitter power \(30-50% of source\), directional emitter arrays, and active anti-node monitoring are the three recommended mitigation strategies. No TACS system should be deployed in personnel-occupied environments without prior anti-node mapping and exclusion zone establishment. The FxLMS algorithm and TACS hardware performance are sufficient for the stated tactical missions; the primary deployment challenge is acoustic safety management, not cancellation performance.

## 8. References

\[1\] Kuo, S.M. & Morgan, D.R. \(1996\). Active Noise Control Systems: Algorithms and DSP Implementations. Wiley.

\[2\] Elliott, S.J. \(2001\). Signal Processing for Active Control. Academic Press.

\[3\] Nelson, P.A. & Elliott, S.J. \(1991\). Active Control of Sound. Academic Press.

\[4\] NIOSH. \(1998\). Criteria for a Recommended Standard: Occupational Noise Exposure. DHHS\(NIOSH\) Publication 98-126.

\[5\] ResearchGate. \(2022\). Active Control for Marine Engine Room Noise Using FxLMS. Scientific Programming, Wiley.

\[6\] Lueg, P. \(1936\). US Patent 2,043,416: Process of Silencing Sound Oscillations.
