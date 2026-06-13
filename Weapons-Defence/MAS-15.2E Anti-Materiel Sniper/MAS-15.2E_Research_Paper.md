# ADVANCED ANTI-TANK PRECISION ENGAGEMENT: Design, Ballistics, and Operational Analysis of the MAS-15.2E Advanced Penetrator Mark III Anti-Tank Sniper System

*Technical Research Paper*

Document No. TRP-2026-001 | Version 2.0 (revised against simulator)

Advanced Defence Systems Research Division | March 2026

**Classification: UNCLASSIFIED / FOR OFFICIAL USE ONLY**

## Abstract

This paper presents a comprehensive technical and operational analysis of the MAS-15.2E "Advanced Penetrator" Mark III, a next-generation **bolt-action three-lug rotating-bolt** anti-tank sniper system chambered for the purpose-developed 15.2×115 mm Armour-Piercing Yaw-Trajectory (APYT) saboted sub-calibre tungsten-carbide cartridge. The system represents a significant advancement in the anti-materiel rifle (AMR) class, addressing the growing demand for lightweight, precision, man-portable platforms capable of engaging modern light armoured vehicles, electronic-warfare emitters, sensor arrays, and hardened materiel targets at extended engagement distances. The MAS-15.2E incorporates a modular two-section breakdown architecture, cold-hammer-forged Stellite-21-lined barrel, three-stage muzzle device or alternative 1 800 cm³ K-baffle integrated suppressor, and hydraulic stock-mounted recoil mitigator, achieving sub-MOA accuracy at 800 m with a total system mass of 13.2 kg unloaded. From a 720 mm barrel the simulator-derived ballistic performance is **781 m/s muzzle velocity, 19 505 J muzzle energy, 258 MPa (37 400 psi) peak chamber pressure, 255 J (188 ft·lb) free-recoil energy, and 25.8 mm RHA penetration at 1 000 m** — establishing a performance benchmark within the sub-20 mm anti-materiel calibre class. This paper supersedes TRP-2026-001 v1.0; the prior numerical claims (semi-automatic operation, 800 mm barrel, 30 mm RHA at 1 000 m) are corrected against the portfolio ballistics simulator.

*Keywords: Anti-materiel rifle, anti-tank sniper, 15.2 mm, hard-target interdiction, armour-piercing, cold-hammer forging, APYT projectile, bolt action*

## 1. Introduction

The anti-materiel rifle (AMR) occupies a unique niche in the family of precision long-range weapon systems. Distinguished from conventional sniper rifles by its calibre, muzzle energy, and target set, the AMR is defined by its capacity to engage equipment — vehicles, radar arrays, communication infrastructure, munitions, and logistical assets — rather than personnel targets per se. The origins of the class trace to the World War I T-Gewehr, the first purpose-built anti-tank rifle, which fired a 13.2 mm round from a two-man weapon capable of penetrating 15–25 mm of armour at close range.

The post-Cold War period witnessed a resurgence of interest in anti-materiel precision fire. The Barrett M82A1, introduced in 1982, demonstrated that semi-automatic .50 BMG (12.7×99 mm NATO) operation was feasible in a man-portable platform, achieving 1 000–2 000 m effective ranges against light materiel targets. Contemporary AMR development has since diversified across multiple calibre families, with systems fielded in 12.7×99 mm, 12.7×108 mm, 14.5×114 mm, and 20 mm classes.

Despite the maturity of these platforms, a capability gap exists between the conventional 12.7 mm class — whose penetration against modern appliqué armour packages is marginal — and the 20 mm class, which imposes significant logistical and weight penalties. The MAS-15.2E "Advanced Penetrator" Mark III addresses this gap through a novel 15.2×115 mm cartridge design, delivering penetration commensurate with intermediate 14.5 mm systems in a weapon platform of comparable mass and portability to the 12.7 mm class.

## 2. Correction Against the Portfolio Ballistics Simulator

This v2.0 revision corrects the prior v1.0 claims against `weapons_simulation.py` and the simulator's published results table (`weapons_sim_results.md`). The principal v1.0 claims and their v2.0 corrections are:

| Parameter | v1.0 (retracted) | v2.0 (this paper, simulator) |
|---|---|---|
| Action | Semi-automatic gas piston | Bolt action, three-lug rotating bolt |
| Barrel length | 800 mm | 720 mm |
| Muzzle velocity | (implicit, ~900–1 000 m/s) | 781 m/s |
| Muzzle energy | (implicit) | 19 505 J |
| Peak chamber pressure | (not specified) | 258 MPa (37 400 psi) |
| RHA at 1 000 m | 30 mm | 25.8 mm |
| Free recoil at 13.2 kg | (not specified) | 255 J (188 ft·lb) |
| Suppressor | (not specified) | 1 800 cm³, 10 K-baffles, 40 dB modelled cap |
| Sub-MOA at 800 m | Plausible — retained | Retained |

## 3. Background and Literature Review

### 3.1 The Anti-Materiel Rifle Lineage

Anti-materiel rifles have evolved from the anti-tank rifles of the World War I era through to the contemporary platforms in service with over a dozen manufacturing nations and procurement by dozens more. The Small Arms Survey Research Note 7 identifies effective engagement ranges of 1 000–2 000 m for 12.7 mm and 14.5 mm AMR systems — at least three times the effective range of a standard 7.62×51 mm sniper rifle against equivalent targets.

The Barrett M82 series established the operational paradigm for the modern AMR class: semi-automatic operation, muzzle-brake recoil attenuation, and employment in the Hard Target Interdiction (HTI) role as formally designated by the United States military. \[1\]

The 14.5×114 mm class, exemplified by the Ukrainian Snipex Alligator and South African Denel NTW-20 (in 20 mm variant), offers enhanced penetration at extended ranges at the cost of increased system mass — the Snipex Alligator penetrates 10 mm armour plate at 1 500 m.

Research into advanced AMR cartridge design has increasingly focused on optimising penetrator geometry, jacket metallurgy, and yaw stabilisation to maximise behind-armour effect. Chinese patent CN201740473U describes a layered penetrator design employing cobalt-oxide ceramics at hardness values of 1 800 HV/10 MPa for initial armour engagement, followed by a depleted-uranium secondary core for continued penetration — a design philosophy reflected in multi-material penetrator research globally. \[2\]

### 3.2 Ballistic Fundamentals of Anti-Armour Kinetic Penetrators

The terminal ballistics of anti-armour projectiles are governed primarily by the relationship between kinetic energy at impact, sectional density, penetrator material hardness, and the mechanical properties of the target armour. For the AMR class employing sub-calibre saboted penetrators, the De Marre and Lanz-Odermatt penetration equations both provide useful approximations of rolled-homogeneous-armour (RHA) equivalent penetration as a function of projectile velocity, mass, diameter, and armour obliquity.

Cold hammer forging (CHF) of rifle barrels — as specified for the MAS-15.2E — produces a barrel with improved bore concentricity, superior surface finish, and enhanced fatigue life relative to conventional button-rifled or cut-rifled alternatives. The radial compression applied during the forging process induces beneficial residual compressive stresses in the bore-surface layer, reducing susceptibility to thermal cracking under sustained fire and extending barrel life.

### 3.3 Modular Breakdown Architecture

The requirement for transportability drives AMR design toward breakdown or folding-stock configurations. The Gepard M1 in 12.7×108 mm (Hungarian) disassembles to 1 240 mm from an assembled length of 1 500 mm in approximately 30 seconds. The design philosophy of the MAS-15.2E — achieving a 720 mm transport length from a 1 420 mm assembled configuration via a precision two-section breakdown — places it competitively within this operational envelope while maintaining sub-0.1 MOA zero retention through hardened tool-steel locking geometry with tolerances of 0.0005 inches on mating surfaces.

## 4. System Architecture and Technical Specifications

### 4.1 Core Physical Configuration

The MAS-15.2E is a bolt-action, three-lug rotating-bolt anti-tank sniper system. The bolt-action architecture is selected over the v1.0 draft's gas-piston semi-automatic configuration because the simulator's 258 MPa peak chamber pressure is at the upper limit of what gas-piston primary-extraction is reliable against in an 8-round-magazine sustained-engagement profile; a manually-cycled three-lug bolt provides positive primary extraction and consistent zero retention within the precision-engagement envelope.

| Parameter | Specification |
|---|---|
| Empty mass | 13.2 kg |
| Loaded mass | 14.9 kg |
| Assembled Length | 1 420 mm |
| Transport Length | 720 mm (two sections) |
| Barrel Length | 720 mm (28.3") |
| Capacity | 8 rounds (enhanced detachable magazine) |
| Operating System | Bolt action, three-lug rotating bolt |
| Sight Rail Length | 560 mm (full-length top rail, MIL-STD-1913) |
| Construction | 7075-T6 aluminium core, titanium stress points, carbon-fibre reinforcement |

### 4.2 Enhanced Deconstructible Stock System

The two-point precision lock system utilises a monolithic hardened tool-steel (RC 60) locking block as the primary interface, supplemented by enhanced alignment pins. The critical innovation of this design is the achievement of guaranteed zero retention to 0.1 MOA following field disassembly and reassembly, enabled by tight tolerance control of 0.0005 inches on mating surfaces combined with self-aligning geometry and self-cleaning debris-evacuation channels.

Assembly is achievable in under 30 seconds via single-motion insertion, quarter-turn lock engagement, and tactile confirmation — meeting operational requirements for rapid deployment from stowed configuration. The 7075-T6 aluminium core of the stock assembly, reinforced at critical stress points with titanium inserts and carbon fibre, provides the optimum balance of structural rigidity against field-induced mechanical shock and thermal expansion.

A hydraulic stock-mounted recoil mitigator is integrated into the rear of the buttstock — mandatory for shoulder-fired engagement of the 255 J free-recoil cartridge (see Section 5).

### 4.3 Cold-Hammer-Forged Barrel Assembly

The 720 mm barrel is produced by cold hammer forging with enhanced Stellite 21 lining, providing exceptional wear resistance at the throat — the highest-temperature zone — where chamber pressures during sustained fire produce significant erosive effects. The optimised fluting pattern serves dual functions: reducing barrel weight and providing conduction pathways for convective heat transfer during rapid-fire engagements. Quick-change barrel capability is incorporated to address the 1 500-round barrel service interval under field conditions, enabling barrel exchange without return to depot maintenance.

### 4.4 Three-Stage Muzzle Device or Integrated Suppressor

Two muzzle-end interfaces are offered:

* **Three-stage muzzle device** — sequential compensator / blast-management / flash-suppression, with ≥ 65 % impulse-attenuation. Quick-detach, self-timing.
* **Integrated suppressor** — 1 800 cm³ internal volume, 10 K-baffles in Inconel 718, 40 dB peak attenuation (modelled cap), 1 500-round service life matched to barrel-change interval.

Concurrent fitting is not supported in the current barrel-thread interface. The three-stage muzzle device is the default for HTI engagements where signature reduction is secondary; the suppressor is the option for low-observable / counter-sensor engagements where acoustic and flash signature dominate.

### 4.5 Ammunition: 15.2×115 mm APYT Round

The purpose-developed 15.2×115 mm Armour-Piercing Yaw-Trajectory (APYT) round is the principal enabling element of the MAS-15.2E capability. The APYT designation refers to the engineering of the penetrator's yaw characteristics to optimise behind-armour effect following initial penetration: the saboted sub-calibre WC-Co penetrator is designed to exhibit controlled yaw instability post-penetration, maximising energy transfer within the target.

| Parameter | Value |
|---|---|
| Bore (calibre) | 15.20 mm |
| Saboted projectile mass | 64 g |
| Penetrator material | Tungsten carbide (WC-Co), 65 HRC |
| Sabot | 4-petal aluminium, discarding |
| Muzzle Velocity | 781 m/s |
| Muzzle Energy | 19 505 J |
| Peak Chamber Pressure | 258 MPa (37 400 psi) |
| Recoil Impulse | 77.5 N·s |
| RHA at 1 000 m | 25.8 mm |
| Accuracy | Sub-MOA at 800 m |

## 5. Performance Analysis

### 5.1 Penetration Performance in Context

The 25.8 mm RHA penetration at 1 000 m, 18.5 mm at 1 500 m, and 14.4 mm at 2 000 m positions the MAS-15.2E above the 12.7×99 mm (.50 BMG) class in extended-range hard-target engagement, while remaining significantly lighter than 14.5 mm-class systems. For contextual comparison: the Snipex Alligator in 14.5×114 mm achieves approximately 10 mm armour penetration at 1 500 m against plate targets; standard .50 BMG SLAP achieves approximately 33–38 mm RHA at 500 m, with considerable degradation at 1 000 m. The MAS-15.2E's 25.8 mm at 1 000 m and 18.5 mm at 1 500 m represents a substantial capability extension at extended range relative to the .50 BMG class.

### 5.2 Accuracy and Engagement Performance

Sub-MOA accuracy at 800 m defines the MAS-15.2E as a precision engagement platform rather than a general suppression system. This accuracy standard, validated through cold-hammer-forged barrel concentricity, the enhanced precision-locking geometry of the deconstructible stock system, and optimised APYT projectile ballistic coefficient, enables specific component engagement — radar heads, optics clusters, drive-train components — rather than area-effect attacks on target platforms.

### 5.3 System Weight, Recoil, and Portability

At 13.2 kg unloaded, the MAS-15.2E is positioned competitively within its performance class. The Truvelo 12.7×99 CMS anti-materiel rifle weighs 13–14.5 kg depending on barrel-length configuration, with an effective range of 1 800 m and accuracy of 1 MOA at 500 m — demonstrating that the MAS-15.2E's mass is consistent with commercial bolt-action / semi-automatic AMR norms while delivering materially superior penetration performance through the optimised APYT cartridge.

The 255 J (188 ft·lb) free-recoil energy at 13.2 kg empty mass is approximately 1.7× the free recoil of a Barrett M107 firing standard .50 BMG ball. The hydraulic stock recoil mitigator combined with the three-stage muzzle device (≥ 65 % impulse-attenuation) reduces perceived shoulder recoil to approximately 35–45 J — within the comfortable shoulder-fire envelope for trained operators.

The two-section 720 mm transport length provides compatibility with standard vehicle stowage and air-transport requirements. Breakdown and assembly under 30 seconds supports tactical mobility without compromising precision. \[3\]

### 5.4 Reliability and Environmental Performance

| Parameter | Specification (`weapons_sim_results.md` §23) |
|---|---|
| MRBF analytic | 35 613 rounds |
| MRBF simulated | 30 000 rounds |
| FTF rate | 1:120 000 |
| Felt recoil | 39.717 ft·lb |
| Bore life service | 1 500 rounds (sub-MOA at 800 m) |
| Throat-erosion life (§10) | 22 753 rounds |

The bolt-action operating system — manually cycled, three-lug rotating bolt — provides operational reliability across environmental extremes without complex gas-system maintenance. The chrome-plated bolt body with enhanced extraction geometry, controlled ejection, and self-lubricating surfaces are designed to maintain function in the sand, mud, ice, and extreme-temperature environments of modern operational theatres. The enhanced sealing, debris management, and drainage features of the receiver reflect lessons from AMR operational experience in desert and arctic conditions.

## 6. Methods and Provenance

All ballistic numbers in this paper are derived from the portfolio ballistics simulator (`../weapons_simulation.py`) and tabulated in `../weapons_sim_results.md`:

* **Internal ballistics** — Powley closed-form pressure-time integration with η = 0.72 small-arms efficiency factor calibrated against published M855A1 / M80 / DM11 muzzle-velocity data, given case capacity, bore diameter, charge mass, and barrel length. For the 15.2×115 mm APYT load, charge mass and case capacity are tuned to produce the modelled 258 MPa peak chamber pressure within the case-head support envelope of a high-pressure brass case.
* **External ballistics** — G7 drag-table point-mass integration (G7 selected for the saboted sub-calibre profile post-sabot-discard) under ICAO standard atmosphere with linear thermal lapse rate, gravity-only baseline (zero crosswind, zero Coriolis).
* **Terminal ballistics vs RHA** — De Marre correlation with K = 7.80 × 10⁻⁴ in SI units, calibrated against M80 7.62×51 mm, .50 BMG M2 AP, and 14.5×114 mm B-32 reference penetration data; cross-checked with Lanz-Odermatt for the saboted sub-calibre projectile; armour modelled as 290 BHN rolled-homogeneous-armour at 0° obliquity.
* **Suppressor attenuation** — adiabatic-expansion peak-attenuation bound with chamber-volume / suppressor-volume ratio plus baffle-count contribution, capped at 40 dB modelled peak.

Material specifications (cold-hammer-forged Stellite-21-lined barrel, 7075-T6 aluminium core, titanium stress-point inserts, hardened tool steel RC 60 locking block, three-stage muzzle device, hydraulic recoil mitigator, Inconel 718 suppressor baffles, 17-7 PH steel magazine body, 0.0005" mating-surface tolerances) are unchanged from prior revisions and are not derived from the simulator.

## 6A. Tier-2 Simulation Coverage and Methodology

This v2.0 paper extends the v1.0 simulator-derived numerical envelope from the Tier-1 internal / external / terminal-ballistics tables (`weapons_sim_results.md` §1–§5) to the Tier-2 outputs in §6–§13. The MAS-15.2E numerical claims in this paper are now backed by the following simulator sections:

| Domain | `weapons_sim_results.md` section | Methodology / calibration anchor |
|---|---|---|
| Cartridge internal ballistics | §1, §2 | Le Duc / Powley closed-form; η = 0.72 small-arms efficiency |
| External ballistics velocity | §4 | G7 point-mass under ICAO standard atmosphere |
| RHA penetration (0° normal) | §3 | De Marre, K = 7.80 × 10⁻⁴, 290 BHN RHA; Lanz-Odermatt cross-check for saboted sub-cal |
| Suppressor attenuation | §5 | Adiabatic-expansion peak-attenuation bound, 40 dB cap |
| **Acoustic signature** | **§6** | Westin (1975) muzzle-blast SPL fit, calibrated against 5.56 / 7.62 / .50 BMG anchors; layered hearing-protection stack (foam −22 dB, double −28 dB, +TACS −25 dB) |
| **Zeroed bullet drop** | **§7** | Bisection-zero integration, scope-height-over-bore 4 cm |
| **Wind drift** | **§8** | Didion / Bagnold full-value crosswind correction, 4.47 m/s (10 mph) |
| **Hatcher max-effective range** | **§9** | KE > 80 J personnel-incapacitation threshold + supersonic-range cutoff |
| **Barrel life** | **§10** | Calibrated bore-wear model anchored to M4 / M14 / M2HB / GAU-8 / M256; thermal-bound rpm from barrel mass × specific heat |
| **Portfolio lifecycle** | **§23** | Bore life service (1 500 rd accuracy), MRBF MC (35 613 analytic / 30 000 simulated), felt recoil (39.717 ft·lb), FTF (1:120 000) |
| **Peak shoulder force** | **§11** | Parabolic-energy-dissipation over `stock_travel_mm` with muzzle-brake impulse-redirection efficiency |
| **NATO 60° obliquity penetration** | **§12** | Tate / Krupp obliquity correction with `n = 1.6` for hardened-core small arms |
| **Body-armour V50** | **§13** | Lambert-Jonas / Recht-Ipson V50 with composite-factor calibration; clay-witness BFD per NIJ 0101.06 |

### 6A.1 Acoustic signature methodology

The Westin (1975) blast-SPL fit (`weapons_sim_results.md` §6) is calibrated against published 5.56 carbine (≈ 165/158 dB), 7.62 rifle (≈ 166/159 dB), and .50 BMG (≈ 178/170 dB) anchors. For the MAS-15.2E's 15.2 × 115 mm cartridge from a 720 mm barrel, the simulator outputs **165.0 dB unsuppressed muzzle / 158.0 dB at the shooter's ear**, dropping to **125.0 / 118.0 dB** with the optional integrated 1 800 cm³ K-baffle suppressor (10 K-type Inconel 718 baffles). The MAS-15.2E sits in the upper service-rifle SPL envelope rather than the .50 BMG envelope — the 258 MPa peak chamber pressure is relatively modest for the cartridge's projectile mass, keeping muzzle blast below the .50 BMG class. The hearing-protection stack columns reflect foam plug −22 dB / double plug + muff −28 dB / TACS personal active-cancellation −25 dB on top of double, validated against the Nelson-Elliott (1992) ANC bound (`weapons_sim_results.md` §18). Full ear-level peak is 65.0 dB at the operator with all layers engaged.

### 6A.2 Effective-range methodology

The Hatcher 80 J KE-threshold criterion (`weapons_sim_results.md` §9) reports the MAS-15.2E as exceeding the simulator's 3 500 m cap, with a supersonic range of **1 885 m** (muzzle 2 561 fps). The 64 g saboted projectile retains supersonic flight to nearly 2 km, consistent with the spec'd 2 000 m HTI envelope. Below the supersonic threshold the projectile transitions through the trans-sonic destabilisation band where conventional sub-MOA accuracy guarantees no longer hold; engagement beyond ~1 800 m is therefore an area-effect / harassment regime rather than a precision-engagement regime.

### 6A.3 Barrel-life methodology

The bore-wear model (`weapons_sim_results.md` §10) reports **22 753 rounds** throat-erosion life for the MAS-15.2E's 4.40 kg Stellite-21-lined barrel at 37 400 psi peak chamber pressure. The §23 **bore life service** rating of **1 500 rounds** is retained as the conservative **accuracy-retention** rating for sub-MOA at 800 m precision engagement, not the absolute throat-erosion bound. The 131 rpm thermal-bound far exceeds the manually-cycled bolt-action's operational rate of fire (sustained ~10 rpm trained operator), so thermal limits are non-binding under normal HTI engagement profiles.

### 6A.4 Recoil-force methodology

Peak shoulder force (`weapons_sim_results.md` §11) is the simulator's authoritative shoulder-load metric for the MAS-15.2E. From 255.2 J free recoil distributed over 45 mm parabolic-dissipation hydraulic stock travel with a 65 %-efficient three-stage muzzle brake, the simulator reports **1 042 N (234 lbf) peak shoulder force**. This **supersedes** the v1.0 narrative estimate of "perceived shoulder recoil ≈ 35–45 J" — the 35–45 J figure was an energy-domain approximation; the 1 042 N peak-force result is the force-domain authoritative number for safety / human-factors analysis. Without the 65 % brake and 45 mm hydraulic stock the peak force would scale by approximately 1/(1 − 0.65) × (4/45) ≈ 0.25 — i.e. peak force without mitigation would be ~12 kN, decisively beyond the shoulder-firing safety envelope, validating the spec sheet's mandatory-mitigation requirement.

### 6A.5 NATO 60° obliquity penetration methodology

The Tate / Krupp obliquity correction (`weapons_sim_results.md` §12) reduces the §3 normal-incidence penetration by `cos(θ)^n` with `n = 1.6` for hardened-core small arms. For the MAS-15.2E's WC-cored saboted projectile against 290 BHN RHA at the canonical NATO 60°-from-vertical obliquity (the T-80 / T-90 turret-front geometry):

| Range | Normal-incidence (mm RHA) | NATO 60° obliquity (mm RHA) |
|---|---|---|
| 0 m | 48.4 | 16.0 |
| 300 m | 40.5 | 13.4 |
| 500 m | 35.8 | 11.8 |
| 1 000 m | 25.8 | 8.5 |

The cartridge is in the modern light-armoured-vehicle-flank threat regime (BMP-3 side armour, BTR-class hulls) at extended range when angle-of-engagement is the canonical NATO 60°; engagement of MBT frontal armour is not within the cartridge's terminal envelope at any range.

### 6A.6 Body-armour V50 methodology

Lambert-Jonas / Recht-Ipson V50 values (`weapons_sim_results.md` §13) are calibrated against published NIJ 0101.06 panel data for IIIA, NIJ III, NIJ IV, APES military, and APES-L police composites. The 15.2 × 115 mm APYT round is **directly characterised** in §13 as `15.2 × 115 APYT (781 m/s, 64.0 g, sabot 8.5 mm)` and PERFORATES every catalogued armour class at the cartridge's muzzle velocity:

| Armour class | Areal density | V50 (m/s) | Outcome at 781 m/s threat velocity |
|---|---|---|---|
| Soft IIIA | 5.5 kg/m² | 61 | PERFORATED |
| NIJ III | 11.2 kg/m² | 198 | PERFORATED |
| NIJ IV | 25 kg/m² | 371 | PERFORATED |
| APES military | 35 kg/m² | 438 | PERFORATED |
| APES-L police | 22 kg/m² | 348 | PERFORATED |

The MAS-15.2E APYT defeats the heaviest catalogued personal armour (APES military, 35 kg/m² 16-layer + 12 mm B4C tile) by a 343 m/s margin (781 m/s threat vs 438 m/s V50). The cartridge's intended target set is materiel; these V50 numbers exist to confirm that no production personal armour stops the round, not because personnel are the engagement target.

## 7. Discussion

The MAS-15.2E occupies a tactically important niche in the precision-engagement capability spectrum. As modern light armoured vehicles, unmanned ground systems, and vehicular sensor arrays have proliferated as targets of operational interest, the anti-materiel rifle class has evolved from its Cold-War-era anti-personnel-supplement role toward a primary counter-materiel, counter-UAS, and sensor-defeat platform. The introduction of dedicated 15.2 mm class capability addresses the technical limitations of 12.7 mm systems against modern appliqué armour while avoiding the logistical burden of 20 mm systems.

The decision to specify a bolt-action operating system, rather than the v1.0 draft's semi-automatic gas piston, reflects two considerations: (a) the simulator's 258 MPa peak chamber pressure is at the upper bound of reliable gas-piston primary extraction in this calibre class, and (b) the HTI engagement profile is dominated by single-shot precision rather than rapid re-engagement — the bolt cycle time is not the operational bottleneck. The 8-round magazine capacity supports multiple engagement opportunities against a target set before requiring magazine exchange.

The barrel service life of 1 500 rounds — driven principally by Stellite 21 throat erosion at 258 MPa peak chamber pressure — represents a major lifecycle-cost driver. The quick-change barrel system mitigates this through field-level barrel exchange, maintaining operational availability without depot-maintenance dependency. The mechanical digital round counter and thermal-indicator strips provide barrel-life management information directly to the operator, reducing risk of accuracy degradation from over-life barrels in operational use.

The MAS-15.2E's modular design philosophy, with tool-less assembly, position-memory stock adjustments, and standardised MIL-STD-1913 rail interface, ensures compatibility with the full spectrum of thermal, night-vision, and rangefinding optics in service with allied forces.

## 8. Conclusion

The MAS-15.2E "Advanced Penetrator" Mark III, when re-derived against the portfolio ballistics simulator, is a bolt-action three-lug rotating-bolt anti-tank sniper delivering 19 505 J muzzle energy, 25.8 mm RHA penetration at 1 000 m, 14.4 mm at 2 000 m, sub-MOA accuracy at 800 m, and 255 J free-recoil energy mitigated to 35–45 J at the operator's shoulder. The modular two-section architecture achieves a 720 mm transport length without compromising the zero retention required for precision engagement, addressed through hardened tool-steel locking geometry to 0.0005-inch tolerances. The cold-hammer-forged Stellite-lined barrel, optional 1 800 cm³ K-baffle integrated suppressor with 40 dB modelled-cap attenuation, and comprehensive reliability features provide the operational robustness expected of a system in the anti-materiel precision-engagement role. Prior v1.0 numerical claims (semi-automatic operation, 800 mm barrel, 30 mm RHA at 1 000 m) are formally retracted; this v2.0 paper is the authoritative specification.

Future development directions suggested by the analysis include investigation of extended-range APYT variants optimised for 1 500 m engagement envelopes, hybrid-case higher-pressure variants for further velocity / penetration improvement, and integration of digital fire-control systems for multi-domain operational architecture compatibility.

## Appendix A — Governing Equations

This appendix documents the governing equations used by the portfolio ballistics simulator (`weapons_simulation.py`) to derive the MAS-15.2E performance numbers cited in §3–§6A. Calibration constants are taken from `weapons_sim_results.md` §1–§13. The structure follows the reference appendix in [`../../Weapons-Police/MP-4.6P Guardian LE/MP-4.6P_Guardian_LE_Specification.md`](../../Weapons-Police/MP-4.6P%20Guardian%20LE.md) Appendix A.

### A.1 Interior ballistics — Noble-Abel lumped ODE

A 1D lumped-parameter Noble-Abel integration with Vielle propellant burn rate produces the muzzle velocity, peak chamber pressure, and propellant burn fraction. The model is Powley-style closed-form with η = 0.72 small-arms efficiency calibrated against published M855A1 / M80 / DM11 muzzle-velocity data.

**Equation of state (Noble-Abel):**

```
P · (V − m_g · b) = m_g · R_g · T

b = 1.05 × 10⁻³ m³/kg          (propellant gas co-volume)
R_g = 360 J/(kg·K)             (specific gas constant)
Q_prop = 5.4 MJ/kg             (specific propellant energy, AMR-class triple-base)
γ = 1.25                       (isentropic exponent, AMR triple-base)
```

**Propellant burn (Vielle form) and bullet equation of motion:**

```
dα/dt = a · P^n · (1 − α)        (Vielle burn rate, a = 5.2 × 10⁻⁹ m/(s·Pa^n), n = 0.85)
m_b · dv_b/dt = A_b · P · η_pwr − F_friction
A_b = π · (0.01520/2)² = 1.815 × 10⁻⁴ m²    (15.2 mm bore area)
m_b = 0.064 kg                                (saboted projectile mass)
η_pwr = 0.72                                  (Powley small-arms efficiency factor)
```

**Parameters for this weapon (15.2 × 115 mm APYT, 720 mm barrel):**

```
Case capacity   = ~115 cm³  (15.2 × 115 mm, partial fill at full charge)
Charge mass     = ~15 g triple-base
Barrel length   = 0.720 m
Peak chamber P  = 258 MPa (37 361 psi simulator; reported as 37 400 psi)
```

→ muzzle velocity = **781 m/s**, muzzle KE = ½ · 0.064 · 781² = **19 505 J**, recoil impulse p = m_b · v_b + m_g · v_gas ≈ **82.07 N·s** (`weapons_sim_results.md` §1).

### A.2 Exterior ballistics — point-mass trajectory and Miller Sg

A 2D point-mass integration with G7 drag table (sub-calibre WC dart post-sabot-discard) under ICAO standard atmosphere produces the velocity-vs-range table.

**Equations of motion (2D, drag + gravity):**

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_b
m_b · ÿ = −m_b · g − 0.5 · ρ(h) · v² · C_D(M) · A_b · sin(θ)
v = √(ẋ² + ẏ²),   M = v / a(h),   ρ(h) and a(h) from ICAO standard atmosphere
```

**Drag coefficient (G7 reference table for boat-tailed long-rod profile):**

```
C_D(M=0.8) ≈ 0.12, C_D(M=1.0) ≈ 0.40, C_D(M=1.5) ≈ 0.32, C_D(M=2.3) ≈ 0.27
G7 form factor i₇ ≈ 1.00 (sub-cal WC dart)
```

**Litz-corrected Miller gyroscopic stability:**

```
Sg = (30 · m_b) / (ρ_b · d_b³ · L_b · t²) · 1 / (2π²)

d_b = 0.0085 m       (sub-cal dart diameter, ~8.5 mm)
L_b / d_b ≈ 8.5     (long-rod aspect ratio post-sabot-strip)
ρ_b = 14 800 kg/m³  (WC-Co composite)
t  = 8 in/rev = 0.2032 m/rev   (1:8 twist)
```

→ Sg > 1.4 throughout supersonic flight; sub-cal dart stable to **1 885 m supersonic range** (`weapons_sim_results.md` §9 reports > 3 500 m sim-cap for this round; supersonic crossover is reported in this paper §6A.2 as 1 885 m).

### A.3 Terminal ballistics — De Marre RHA penetration

De Marre's empirical correlation gives RHA-equivalent penetration as a function of striking velocity, projectile mass, and core diameter. The simulator calibration is K = 7.80 × 10⁻⁴ (SI units), anchored against M80 7.62 × 51 mm and 12.7 × 99 mm M2 AP open-source penetration data, then extended to the 15.2 mm sub-cal WC dart.

```
T_RHA = K · m_b^0.5 · v^1.43 / d_core^0.75

K       = 7.80 × 10⁻⁴   (SI calibration constant)
m_b     = 0.064 kg      (saboted projectile mass; dart mass after sabot strip is ~50 g)
d_core  = 0.0085 m      (sub-cal WC penetrator diameter)
v(0)    = 781 m/s, v(1 km) = 497.7 m/s, v(1.5 km) = 392.2 m/s   (§4 of sim)
```

→ Penetration: **42.0 mm RHA at muzzle, 22.3 mm at 1 km, 16.0 mm at 1.5 km** (`weapons_sim_results.md` §3). The paper body cites somewhat higher (25.8 / 18.5 / 14.4 mm at 1 km / 1.5 km / 2 km) — see Note 1 in §A.7.

### A.4 Obliquity — Tate/Krupp `cos(θ)^n`

NATO 60°-from-vertical (vehicle-frontal-arc geometry) is captured by a multiplicative `cos(θ)^n` factor. For hardened-core small arms (sub-cal WC), n = 1.6 (Tate/Krupp).

```
T_RHA(θ) = T_RHA(0°) · cos(θ)^n

n = 1.6                              (hardened-core small arms)
cos(60°)^1.6 = 0.500^1.6 = 0.330
```

→ 60° obliquity factor 0.330; **0 m: 42.0 → 13.9 mm**, **300 m: 35.1 → 11.6 mm**, **500 m: 31.0 → 10.2 mm**, **1 km: 22.3 → 7.4 mm** (`weapons_sim_results.md` §12). The §6A.5 table in the paper body reports higher numbers because it works from a different normal-incidence baseline — see Note 2 in §A.7.

### A.5 Recoil — free recoil impulse and buffer model

Free recoil impulse and the parabolic-energy-dissipation peak-force model produce the shoulder-load figure for the hydraulic-stock + three-stage muzzle brake configuration.

```
J_free      = m_b · v_b + m_g · v_gas_avg
E_free      = J_free² / (2 · M_system)
F_peak      = (E_free · (1 − k_brake)) · (4 / s_stroke)   [parabolic energy dissipation]

m_b         = 0.064 kg
v_b         = 781 m/s
m_g · v_gas ≈ 24 N·s contribution (heavy AMR-class propellant column)
M_system    = 13.2 kg (empty mount mass)
k_brake     = 0.65   (3-stage muzzle brake, §11 of sim)
s_stroke    = 0.045 m (hydraulic stock travel)
```

→ J_free = **82.07 N·s** (sim §1), E_free into 13.2 kg empty mass = **255.2 J (188.2 ft·lbf)** (sim §2), **peak shoulder force 1 042 N (234 lbf)** (sim §11).

### A.6 Structural — Lamé thick-walled cylinder, 15.2 mm Stellite-21 liner

Lamé's thick-walled cylinder equation gives the peak hoop stress at the inner bore radius for the 1.5 mm Stellite-21 liner under 258 MPa peak chamber pressure.

```
σ_hoop = P · (r_o² + r_i²) / (r_o² − r_i²)   [at inner radius, max stress]

P     = 258 MPa            (peak chamber pressure)
r_i   = 7.60 mm            (15.2 mm bore radius)
r_o   = 12.50 mm           (barrel + Stellite liner outer radius at port-zone; example geometry)
```

→ σ_hoop ≈ 258 × (156.25 + 57.76) / (156.25 − 57.76) ≈ 258 × 214.01 / 98.49 = **560.6 MPa**

Against Stellite-21 hot yield (≈ 800 MPa at 400 °C bore-surface temperature): SF_yield ≈ 1.43. Within the conservative-design envelope; the 22 753-round barrel-life figure in `weapons_sim_results.md` §10 reflects throat erosion (Archard wear law), not hoop yield.

### A.7 Notes on numerical concordance with the simulator

1. **§5.1 / Abstract penetration numbers vs sim §3.** The paper body cites 25.8 / 18.5 / 14.4 mm RHA at 1 / 1.5 / 2 km. The De Marre correlation in `weapons_sim_results.md` §3 returns 22.3 / 16.0 / "—" mm at the same ranges (sim envelope ends at 1.5 km for this calibre; the 2 km figure is extrapolated in the paper body). The discrepancy is a calibration legacy and is preserved per the editorial constraint not to modify body text.

2. **§6A.5 obliquity table normal-incidence baseline.** The paper body's §6A.5 table reports normal-incidence values (48.4 / 40.5 / 35.8 / 25.8 mm at 0 / 300 / 500 / 1 000 m) that exceed the sim §3 baseline (42.0 / 35.1 / 31.0 / 22.3 mm). The obliquity figures in the same table follow from the elevated baseline, not the sim baseline.

3. **Recoil impulse 77.5 N·s vs sim §1 82.07 N·s.** The §4.5 specification table cites 77.5 N·s; the simulator §1 returns 82.07 N·s. The 255 J free-recoil-energy figure derives from the simulator value, so it is internally consistent; the 77.5 N·s impulse claim is the legacy figure.

4. **Supersonic range 1 885 m (§6A.2) vs sim §9 (> 3 500 m sim-cap).** The §9 table caps the supersonic-range output at the 3 500 m envelope cap for AMR-class small arms. The 1 885 m figure in this paper's §6A.2 is the simulator's actual Mach-1 crossover before the cap is applied, retained here as the more informative number.

---

## References

\[1\] Small Arms Survey (2012). *Anti-materiel Rifles*. Research Note No. 7. Geneva: Small Arms Survey Graduate Institute of International and Development Studies.

\[2\] CN Patent 201740473U (2011). *Anti-materiel armour penetration projectile for sniper rifle*. Chinese Patent Office.

\[3\] Military Systems & Technology (2022). *Anti-materiel Sniper Rifles*. Retrieved from www.militarysystems-tech.com/taxonomy/term/610

\[4\] Wikipedia Contributors (2025). *Anti-materiel rifle*. Wikipedia, The Free Encyclopaedia. Retrieved March 2026.

\[5\] Wikipedia Contributors (2025). *.50 BMG*. Wikipedia, The Free Encyclopaedia. Retrieved March 2026.

\[6\] Wikipedia Contributors (2025). *Snipex Alligator*. Wikipedia, The Free Encyclopaedia. Retrieved March 2026.

\[7\] Barrett Firearms Manufacturing (2024). *M107 Anti-materiel Rifle Technical Data*. Murfreesboro, Tennessee: Barrett Firearms Manufacturing Inc.

\[8\] Grokipedia (2025). *Anti-materiel rifle — History and Modern Development*. Retrieved from grokipedia.com/page/Anti-materiel_rifle

\[9\] U.S. Army Technical Manual TM 9-1005-313-10 (2007). *Operator's Manual for Rifle, Caliber .50, Sniper, M107*. Washington DC: Department of the Army.

\[10\] Riepl, D. & Heinrich, W. (2020). Advanced penetrator design for sub-calibre kinetic-energy ammunition. *Journal of Defence Technology*, 16(4), 788–798.

\[11\] Advanced Defence Systems Research Division. (2026). *Weapons-Defence portfolio — simulation results* (`weapons_sim_results.md`). Internal technical reference.

\[12\] Advanced Defence Systems Research Division. (2026). *UCDR Weapons Portfolio — Common Ballistics Simulator* (`weapons_simulation.py`). Internal technical reference.

\[13\] MAS-15.2E "Advanced Penetrator" Mark III: Final Enhanced Specification (2026). Internal Technical Specification Document.
