# Project OBSIDIAN-X
*Technical Research Paper*

Document No. TRP-2026-208 | Version 1.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

*Advanced Full-Body Combat Armour System for Next-Generation Warfare Protection*

Comprehensive Specification with Integrated HUD, Adaptive Camouflage, CBRN Protection, and Exoskeletal Enhancement

Defense Research Division   |   January 2025   |   Classification: Hypothetical / For Academic Study

## Abstract
Project OBSIDIAN-X is a hypothetical horizon-specification for a deployable full-body combat armour system, conceived as the operational evolution of the concealed-protection OBSIDIAN programme. Where OBSIDIAN prioritised concealability for principal-protection roles, OBSIDIAN-X pursues total warfighter protection across ballistic, blast, CBRN, electronic, and environmental threat dimensions at 18.5 kg total system weight. The specification integrates a multi-material coverall using carbyne-UHMWPE-metamaterial composite fibre, a Universal MultiCam adaptive camouflage suite with active electronic signature management, an advanced tactically integrated helmet system with 4K augmented-reality HUD derived from the US Army IVAS programme, armoured 'Fortress' combat boots, and a distributed nuclear-battery power architecture. Performance targets include rifle-round immunity across the body, 50\+ multi-hit capability without degradation, complete CBRN environmental sealing, and an integrated exoskeleton providing 5× strength multiplication. The paper grounds each subsystem in current peer-reviewed materials science and established defence programme precedents, provides Technology Readiness Level assessments for all major components, and projects a 25-year phased development timeline at an estimated programme investment of $3.1 trillion. A critical engineering assessment identifies the power system, exoskeleton energy density, and multi-spectrum invisibility cloaking as the most speculative elements of the design, while ballistic and CBRN protection at the specified performance levels are assessed as achievable within a 10–15 year research trajectory.

## 1. Introduction

The concept of comprehensive individual soldier protection has driven military equipment development across centuries, from plate armour to Kevlar. The modern threat environment — encompassing small-arms fire from sub-10 m to 800 m, blast and fragmentation from improvised explosive devices, chemical warfare agents, biological contamination, radiological dispersal, directed energy weapons, and persistent adversary surveillance — demands a paradigm shift beyond incremental improvements to existing systems.

Project OBSIDIAN-X emerges from the recognition that three convergent technology trajectories have reached sufficient maturity to justify a coherent speculative system specification. First, advanced carbon allotrope research has established theoretical performance limits for materials that, even partially realised, would substantially exceed current ballistic solutions \[1,2,3\]. Second, the US Army's Integrated Visual Augmentation System \(IVAS\) programme has demonstrated that a $22 billion investment can bring military-grade augmented reality to battalion-level fielding \[4,5\]. Third, DARPA's decade-long Warrior Web programme has validated the soft exosuit concept for strength and endurance augmentation of dismounted soldiers \[6,7\].

OBSIDIAN-X is explicitly designated a horizon specification — a structured extrapolation of what becomes possible when current research trajectories are projected 15–25 years forward. It is not a procurement document, nor does it claim all described capabilities are simultaneously achievable within a single engineering programme. Its value lies in establishing a coherent set of requirements that can serve as long-range targets for component-level research investment.

The operational philosophy — 'Total protection through synthetic perfection and battlefield supremacy' — is understood in this context as a design aspiration rather than a literal engineering claim. The following sections systematically examine each major subsystem against the baseline of current capability.

## 2. State of Practice: Current Military Armour Systems

### 2.1 Body Armour

Contemporary military body armour systems reflect four decades of progressive development from the late-1970s ceramic plate carrier to the current US Army Soldier Protection System \(SPS\). The SPS Torso and Extremity Protection \(TEP\) subsystem provides NIJ Level IV protection — stopping 7.62×63 mm M2 AP — at a combined weight of approximately 8.8 kg for a large-size system. UHMWPE soft armour inserts meeting NIJ Level IIIA \(9 mm at 436 m/s, .44 Magnum at 436 m/s\) are commercially available at 1.24 kg per large insert in Dyneema SB71 \[8,9\].

The principal engineering tension in all body armour design is the protection-mobility trade-off. Defence industry research documents that heavy loads negatively impact soldiers' mobility, shooting response time, and cognitive performance during combat operations \[10\]. Spine and back injuries accounted for 28.3% of all non-combat wounds in the US Army in 2021, predominantly caused by overuse and heavy lifting — a figure that exoskeleton research directly targets \[11\].

### 2.2 Helmet-Mounted Displays and Tactical AR

Helmet-mounted display \(HMD\) systems have transitioned from cockpit-specific applications to dismounted infantry in the past decade. The US Army's Tactical Augmented Reality \(TAR\) system, developed at CERDEC's Night Vision and Electronic Sensors Directorate, was among the earliest infantry HUD implementations: a 1-inch-by-1-inch eyepiece mounted to existing night-vision goggles, overlaying GPS-tracked friendly and enemy positions onto the soldier's field of vision and wirelessly connected to a waist-mounted tablet and rifle-mounted thermal sight \[12\].

The Integrated Visual Augmentation System \(IVAS\), developed with Microsoft on the HoloLens 2 platform under a $22 billion Army contract, represents the current frontier \[4,5\]. IVAS version 1.2 — fielded in battalion assessments in 2024 — delivers combined night vision, thermal imaging, and AR tactical overlay in a flip-up helmet-mount visor weighing 1.5 kg \(target 1.3 kg\). Its display provides a 60-degree field of view; navigation, friendly/enemy position display, targeting reticle linked to a weapon-mounted sight, and a 'Squad Immersive Virtual Trainer' AR training mode \[4\]. In 2025, Microsoft transferred programme oversight to Anduril Industries for production and future development.

USSOCOM's Day and Night HUD \(DANHUD\) Assessment Event in 2024 sought solutions providing heads-up situational awareness both standalone in daylight and integrated with next-generation night vision goggles, including L3Harris Fusion Binocular \(F-BINO\) and Fused Panoramic NVG \(F-PANO\) systems, without requiring the operator to look down at a chest-mounted device \[13\].

### 2.3 Exoskeleton Development Programmes

DARPA's Exoskeleton for Human Performance Augmentation \(EHPA\) programme, inaugurated in FY 2001 with a $50 million Phase I investment, established the research trajectory for military exoskeletons. The Warrior Web programme subsequently commissioned Harvard University's Wyss Institute to develop the 'exosuit' — a soft, flexible undergarment with artificial muscle actuators — tested at the US Army Research Laboratory at Aberdeen Proving Ground on soldiers carrying 100-pound-plus loads over 3-mile courses \[6,7\]. SRI International's SuperFlex suit under the same programme provided 20–30% strength augmentation in core and lower-body loading scenarios \[14\].

The US Army Tactical Assault Light Operator Suit \(TALOS\) programme, while ultimately cancelled before fielding, articulated the design requirement framework that OBSIDIAN-X inherits: anti-ballistic full-body armour, visual augmentation, multi-sensor situational awareness, integrated communication, and strength/endurance enhancement \[15\]. Its architecture informs the OBSIDIAN-X specification at the subsystem integration level.

## 3. Primary Coverall Construction

### 3.1 Theoretical Advanced Material Matrix

The OBSIDIAN-X coverall system proposes a four-component material matrix at the following target mass fractions:

- Ultra-Carbyne Nanorope Framework \(40%\): Stabilised linear carbon chains \(–C≡C–\)n with chain lengths of 6,400\+ atoms, produced inside double-walled carbon nanotube host structures as demonstrated in 2016 \[1\]. First-principles calculations by Liu et al. \(ACS Nano, 2013\) established carbyne's specific tensile strength at up to 7.5 × 10⁷ N·m/kg — exceeding graphene, carbon nanotubes, and diamond — while requiring approximately 10 nN to break a single atomic chain \[2\]. Experimental measurements achieved 251 GPa critical stress at 77 K \[16\].
- Quantum Topological Insulator Weave \(25%\): Bismuth telluride \(Bi₂Te₃\) based topological insulator materials that exhibit metallic surface conduction while remaining bulk insulators. This property, arising from topological protection of electronic surface states, provides quantum-mechanically protected conductive pathways for sensor networks that are immune to backscattering by defects or surface contamination — a critical advantage in a garment subject to ballistic and environmental stress \[17\].
- Programmable Metamaterial Fibres \(20%\): Materials with dynamically adjustable mechanical properties in response to external stimuli \(electrical, thermal, or photic\). Space-time programmable metamaterials have been demonstrated in research settings; their integration into weavable fibre formats remains an active research challenge.
- Self-Healing Shape Memory Matrix \(10%\): Nickel-titanium shape memory alloys \(SMA\), which exploit the thermoelastic martensitic transformation to recover deformation through temperature-induced phase transitions. Dual in-situ self-healing SMA systems capable of autonomous micro-damage repair have been demonstrated in aerospace composite applications.

The resulting composite is proposed at approximately 18.5 kg total system weight distributed across the coverall, helmet, and boots. For reference, the US Army SPS provides torso and extremity protection at approximately 11–14 kg; the OBSIDIAN-X total-system target is within the range considered operationally viable for high-intensity tasks.

*Carbyne specific strength 7.5 × 10⁷ N·m/kg \(Liu et al., ACS Nano 2013\); experimental tensile stress 251 GPa at 77 K \(Kotrechko et al., Nanoscale Res. Lett. 2015\); 6,400-atom chains in DWCNT hosts \(Nature Communications 2016\) \[1,2,16\].*

### 3.2 Articulated Joint System

Full-body armour protection historically compromises mobility at the joints. The OBSIDIAN-X specification addresses this through an articulated joint architecture at six major sites: shoulder \(360° rotation with dynamic tension management\), elbow \(dual-axis with biomechanical load distribution\), hip \(full range-of-motion with exoskeleton integration\), knee \(enhanced hinge with lateral stability\), and ankle \(multi-directional flex interfacing with the boot\).

Auxetic fabric panels — materials with negative Poisson's ratio that expand transversely when stretched — provide the elastic reserve at stretch zones. This counter-intuitive mechanical property has been demonstrated in macroscopic polymer foams, carbon nanotube networks, and 3D-printed polymer lattices, and is directly applicable to woven textile formats. Combined with shape memory PTFE-based fibres returning to dimensional equilibrium after loading, the system targets unconstrained operator biomechanics.

## 4. Universal MultiCam Adaptive Camouflage System

### 4.1 MultiCam Foundation

The US Army's MultiCam pattern \(Crye Precision\) was selected in 2010 as the Operational Camouflage Pattern \(OCP\) for Army Combat Uniforms following a decade of development and operational testing. Its seven-colour scheme — ranging from brown through green with overlaid dark green, olive green, and lime green gradients against a brown-to-light-tan background — was optimised for effectiveness across the widest range of operating environments, from arid to forested terrain, rather than specialised performance in any single biome \[18\].

The OBSIDIAN-X specification builds upon the proven MultiCam geometry, adding adaptive capability through a three-tier enhancement stack. The base MultiCam geometry provides passive broadband disruption of the human visual system's shape recognition. Smart pigment technology — thermochromic elements that adjust tone with environmental temperature — provides dynamic passive adaptation. Electronic enhancement — micro-LED integration and active thermal signature dispersion — provides active multi-spectral management.

### 4.2 Electronic Signature Management

Modern combat threat detection spans multiple electromagnetic spectra beyond the visible band. Near-infrared \(NIR\) surveillance is standard in remotely-operated aircraft and ground-force night-vision systems. Thermal infrared imaging detects body heat at ranges exceeding 1,500 m under suitable atmospheric conditions. Radar-band detection is increasingly relevant against ground surveillance radar and autonomous drone systems.

The OBSIDIAN-X active signature management stack proposes:

- Active pattern modulation: Micro-LED arrays embedded in the outer textile layer for dynamic pattern adjustment to background reflectance.
- Thermal signature dispersion: An integrated heat redistribution network — likely comprising PTFE liquid-metal microchannels — actively spreads metabolic heat over the full suit surface area, reducing peak thermal contrast.
- Radar absorption: Carbon nanotube mesh optimised for absorptance across C/X/Ku radar bands. CNT-based radar-absorbing structures have been demonstrated in laboratory settings with absorption exceeding 90% at target frequencies.

Full multi-spectrum active invisibility — achieving simultaneous visual, thermal, and radar concealment — remains a research challenge. The thermal active dispersion approach imposes significant power requirements that must be balanced against the overall system energy budget.

## 5. OBSIDIAN-X Tactical Helmet System

### 5.1 Ballistic Shell Architecture

The helmet shell is specified in a multi-layer architecture: carbyne-diamond composite primary shell for rifle-round protection, 6 mm multi-scale graphene composite secondary layer, and PTFE-based auxetic foam trauma mitigation. This configuration builds upon established helmet materials science — current Advanced Combat Helmet \(ACH\) shells use UHMWPE laminate or aramid composite to achieve NIJ Level IIIA equivalent protection — extending the ballistic performance ceiling to intermediate rifle threats.

Graphene's tensile wave speed of 21.3 km/s \(versus 17.5 km/s for diamond\) enables faster stress wave propagation away from the impact site, reducing peak localised stress and improving multi-hit performance \[19\]. The theoretical unlimited service life claim — based on the chemical stability of synthetic carbon materials — is directionally correct as a durability aspiration, though practical service limits imposed by microcrack accumulation and fastener system wear will apply.

### 5.2 Integrated HUD: Display Specifications

The OBSIDIAN-X HUD specification derives its architecture from the IVAS programme, projecting forward to 2030–2035 display technology. The target specifications are:

**Parameter**
OBSIDIAN-X Target

**Resolution**
4K per eye \(3840 × 2160\) micro-OLED

**Field of View**
120° horizontal, 90° vertical

**Brightness**
10,000 nits \(outdoor visibility\)

**Response Latency**
<5 ms

**Power Consumption**
Ultra-low power, 72-hour operation

**Current IVAS 1.2 Baseline**
60° FoV, 3.4 lbs, FY2025 fielding target

The 120°/90° field-of-view target represents a significant extension from IVAS 1.2's 60° FoV. Current micro-OLED display technology, as used in VR/AR headsets at the consumer frontier, achieves approximately 4K resolution per eye at brightness levels of 1,000–5,000 nits; the 10,000 nit target for outdoor combat visibility will require further micro-display development. Sub-5 ms latency is achievable with current GPU rendering pipelines at 4K resolution in single-scene rendering but presents challenges for photorealistic sensor-fusion rendering.

The projected 2030–2035 timeframe is consistent with published roadmaps from major micro-display manufacturers \(eMagin, Kopin, Sony Semiconductor\) for 4K micro-OLED panels in the 0.5–1 inch diagonal range suitable for HMD applications.

### 5.3 HUD Information Architecture

The information architecture of the OBSIDIAN-X HUD builds on the IVAS information set — navigation, friendly/enemy positions, targeting reticle, thermal/NV overlay — and adds:

- Biometric monitoring overlay: Heart rate, core temperature, fatigue indicators derived from the Layer 3 smart textile sensor network. This data supports both operator self-awareness and remote medical monitoring by unit leadership.
- CBRN threat indicators: Real-time chemical and biological detection data from the suit sensor network, displayed as colour-coded threat zones overlaid on terrain.
- Weapon integration: Ballistic compensation overlay accounting for wind, range, and atmospheric density, linked to a weapon-mounted sensor suite.
- Environmental data: Wind speed/direction, temperature, visibility — relevant to both CBRN exposure assessment and marksmanship.

Voice command and eye-tracking interfaces reduce the cognitive and manual overhead of display management during high-tempo operations. The US Army IVAS programme has already validated eye-tracking as a practical HMD interaction modality in field conditions; natural language processing for hands-free command has been demonstrated in multiple consumer and military voice-assistant platforms.

### 5.4 Multi-Spectral Vision Systems

The OBSIDIAN-X vision suite integrates visible light \(full-colour, auto-exposure\), thermal infrared \(high-resolution overlay\), near-infrared \(low-light enhancement\), and ultraviolet \(chemical/biological contamination detection\) channels into a unified fused display. AI-powered image optimisation — currently in development as part of the IVAS programme's 'extensibility' roadmap — provides adaptive enhancement across channels.

Generation IV\+ night vision image intensification, combined with digital image processing and thermal fusion, is a known development trajectory. Current Generation III intensified tubes achieve moonlight-level performance; Generation IV research targets starlight-and-below capability. The IVAS 1.2 programme reached the limits of its analog NV technology in 2024, driving adoption of digital sensor fusion approaches. The OBSIDIAN-X specification projects this convergence to a fully integrated multi-spectral digital sensor suite by 2030–2035.

## 6. Fortress Combat Boots

The OBSIDIAN-X boot specification extends the material architecture of the coverall into a combat-boot format, addressing the three principal foot-and-ankle threats in modern ground combat: landmine blast, ballistic projectile \(from ground level engagements and IED fragmentation\), and CBRN contamination.

The structural specification proposes UHMWPE fibre composite upper construction with integrated ceramic plate inserts at the toe, heel, and ankle — analogous to the established UHMWPE-ceramic hybrid approach used in torso plates. Carbyne-reinforced fluoropolymer blast-resistant sole plate, graphene spring energy-return system in the midsole, and adaptive grip sole patterns complete the protective substrate.

**Feature**
Specification

**Upper material**
UHMWPE fibre composite with MultiCam pattern

**Ballistic zones**
Ceramic inserts at toe, heel, ankle

**Blast sole**
Carbyne-reinforced fluoropolymer

**CBRN interface**
PTFE gasket system, sealed to coverall at ankle

**Kinetic harvesting**
Piezoelectric stack in heel for system charging

**Emergency beacon**
Integrated GPS \+ distress signalling

The boot integrates pressure sensors for real-time gait analysis — feeding data to the exoskeleton control system for predictive actuation timing — and a foot-mounted backup communication antenna. The PTFE gasket CBRN interface provides continuity of the sealed system boundary from coverall to boot.

## 7. Power Systems Architecture

### 7.1 Nuclear Diamond Battery Concept

The OBSIDIAN-X specification proposes a nuclear betavoltaic battery as the primary power source, drawing on research into carbon-14 and nickel-63 diamond betavoltaic cells. These devices embed radioactive isotopes within synthetic diamond matrices, generating electricity from beta-particle emission over timescales governed by isotopic half-lives.

Carbon-14 beta diamond batteries were demonstrated at the University of Bristol in 2016 and commercialised by Arkenlight \(UK\) and NDB Inc. \(US\) by the mid-2020s. At the time of specification, carbon-14 has a half-life of 5,730 years; power density remains modest \(microwatts per gram range\), though ongoing research targets milliwatt-scale output from enriched isotope configurations.

The OBSIDIAN-X 'nuclear waste battery' claim — providing energy density more than 3,000 times that of gasoline over a 50-year operational life — is assessed as highly speculative at present power density levels. The energy density of chemical fuels \(gasoline: ~46 MJ/kg\) vastly exceeds current betavoltaic output per unit mass. The theoretical maximum betavoltaic efficiency using C-14 is constrained by the 156 keV beta endpoint energy and semiconductor conversion efficiency limits. A realistic near-term assessment places nuclear diamond batteries as supplementary trickle-charge sources rather than primary drive systems.

The practical power architecture for a 2030–2035 OBSIDIAN-X system would more plausibly be: high-capacity solid-state lithium primary cells supplemented by kinetic energy harvesting \(piezoelectric boot stack\), solar micro-array in the outer coverall, and betavoltaic trickle charge for standby power maintenance.

### 7.2 Graphene Supercapacitor Network

Graphene supercapacitors provide high-power-density energy storage for burst demands — exoskeleton actuation peaks, HUD display startup, active signature management pulses. Distributed through the Layer 3 textile as woven graphene elements, they support load-levelling between the primary battery and variable-demand subsystems. Published research documents graphene supercapacitor energy densities of up to 85 Wh/kg, exceeding lithium-ion batteries in power density \(kW/kg\) if not energy density \[20\].

## 8. Integrated CBRN Protection System

Full CBRN protection in a combat armour system requires positive-pressure sealed enclosure, filtered respiratory air supply, and complete skin-barrier integrity across all suit interfaces. The OBSIDIAN-X architecture achieves this through:

- All-synthetic material chemistry: PTFE coatings on all external surfaces provide near-universal chemical resistance. No organic materials to support microbial colonisation or radioactive surface contamination adhesion.
- Sealed joint gaskets: PTFE gaskets at wrist, ankle, and neck provide positive-pressure-compatible barrier continuity across limb interfaces.
- Positive-pressure life support: Backpack-integrated air filtration unit with activated carbon and HEPA filtration and optional oxygen-enrichment for extended sealed operations.
- CNT chemical sensor network: Real-time agent detection providing <500 ms warning for vapour-phase chemical agents, enabling seal-check alert and decontamination initiation.

Complete CBRN protection compatible with normal combat operations has been achieved in Mission Oriented Protective Posture \(MOPP\) Level 4 equipment for decades; the OBSIDIAN-X advance is integrating this protection level within a wearable combat system without the mobility penalty of conventional CBRN overgarments. The all-synthetic material architecture is a significant enabler: conventional CBRN suits use activated carbon layers in butyl rubber or polyethylene substrates, adding 3–6 kg and substantial thermal penalty.

## 9. Integrated Strength Enhancement System

### 9.1 Performance Targets vs Current State

The OBSIDIAN-X exoskeleton specification targets 5× upper body strength multiplication, 600 kg operational load carrying, 2.5× running speed, and unlimited operational duration. These targets must be assessed against current exoskeleton programme achievements.

The SRI SuperFlex suit under DARPA Warrior Web provides 20–30% strength augmentation in core and lower body loading \[14\]. Lockheed Martin's Onyx lower-body exoskeleton reduces metabolic load during load-carrying but does not multiply lifting strength. No current fielded or prototype system approaches 5× strength multiplication in a wearable format. The Human Load Carrier \(HULC\) — a hydraulic-powered titanium exoskeleton — demonstrated partial load-carrying augmentation but weighed 24 kg itself, negating much of the load-carrying benefit.

AFCEA analysis assesses the 'Iron Man' full-body robotic exoskeleton paradigm as 'mostly a fallacy' for current engineering realities \[11\], while acknowledging a projected 25-year evolution pathway toward 'exponential evolution in wearable technologies' with 'substantial augmentation of human strength through powered exoskeletons' \[15\]. The OBSIDIAN-X targets are most accurately characterised as the 25-year end-point of this evolution trajectory, not achievable within a single near-term programme cycle.

### 9.2 Realistic Architecture

A credible OBSIDIAN-X exoskeleton architecture for 2040\+ timeframe would require: actuator power-density improvements of approximately 15–20× over 2025 soft actuator baselines; lightweight power storage providing sustained kilowatt-level output for hours; and control systems with millisecond-resolution movement prediction from distributed inertial and plantar sensors. Research directions include electroactive polymer artificial muscles, shape memory alloy hybrid actuators, and carbon nanotube-based synthetic muscle fibres — all of which have demonstrated relevant properties at laboratory scale.

## 10. Performance Specifications and Technology Assessment

### 10.1 Protection Performance Summary

**Parameter**
Target

**Soft armour: handgun**
NIJ IIIA equivalent

**Hard plate: rifle**
NIJ IV equivalent

**Multi-hit capability**
50\+ impacts without degradation

**CBRN: chemical vapour**
Full protection, <500 ms warning

**CBRN: biological**
Full barrier integrity

**Temperature range**
-60°C to \+60°C

**Underwater operation**
100 m depth

### 10.2 Enhancement Performance Summary

**Parameter**
Target

**Strength multiplication**
5× natural strength

**Running speed increase**
2.5×

**HUD field of view**
120° × 90°

**HUD brightness \(outdoor\)**
10,000 nits

**Multi-spectral vision**
Visible/IR/NIR/UV fusion

**Adaptive camouflage**
Visible band passive\+active

**Thermal signature suppression**
Active redistribution

**Radar signature reduction**
CNT absorption mesh

## 11. Development Investment and Cost Modelling

### 11.1 Research Infrastructure Requirements

The OBSIDIAN-X programme requires simultaneous progress across five research disciplines, each requiring dedicated national-scale investment:

**Research Domain**
Estimated Investment

**Carbyne synthesis mastery**
$500 billion

**Topological insulator engineering**
$300 billion

**Metamaterial fibre programming**
$400 billion

**Shape memory integration**
$200 billion

**Quantum manufacturing infrastructure**
$800 billion

**Quantum materials sciences**
$300 billion

**Programmable matter physics**
$250 billion

**Self-healing material biology**
$150 billion

**Metamaterial engineering**
$200 billion

**Total Advanced Materials Investment: **$3.1 trillion over 25 years

### 11.2 Per-Unit Economics \(Theoretical Maturity\)

**Cost Element**
Estimated Per-Unit Cost

**Carbyne synthesis**
$25 million

**Topological insulator integration**
$18 million

**Programmable metamaterials**
$22 million

**Shape memory systems**
$12 million

**Quantum manufacturing**
$35 million

**Advanced system integration**
$15 million

**Theoretical validation**
$8 million

**Total per complete OBSIDIAN-X system**
~$135 million

For context, the F-35A unit cost is approximately $80 million in FY2025; the programme comparison demonstrates that the OBSIDIAN-X per-unit cost, while extraordinary, is not unprecedented within the envelope of modern defence capital investment. A force of 10,000 OBSIDIAN-X-equipped special operations personnel would represent a $1.35 trillion procurement.

### 11.3 Phased Development Timeline

**Phase**
Duration

**Phase 1: Advanced Development**
Years 1–8

**Phase 2: System Integration**
Years 9–15

**Phase 3: Initial Deployment**
Years 16–20

**Phase 4: Full Operational Capability**
Years 21–25

## 12. Critical Assessment: Achievable vs Speculative

### 12.1 What Is Achievable Within 10–15 Years

Several elements of the OBSIDIAN-X specification are achievable within a 10–15 year focused research and development programme:

- UHMWPE-graphene composite hard and soft armour: Current graphene-enhanced soft armour already provides Level III\+ equivalent protection at 1.25 kg and 21 mm. Scaling to full-body coverall coverage with articulated joint panels is a manufacturing challenge, not a materials science frontier.
- IVAS-derived HUD at 90°\+ FoV: The IVAS roadmap explicitly targets increased FoV and reduced weight; micro-OLED display technology development trajectories support 90° FoV at 4K resolution within a 2030–2035 timeframe.
- CNT-based biometric and chemical sensor network: Lab-demonstrated CNT chemical sensing and biometric monitoring are achievable in a woven textile format within the decade.
- CBRN integration: All-synthetic material chemistry with PTFE gasket sealed system is a current engineering capability; the challenge is weight and thermal management, not barrier performance.
- Passive soft exoskeleton \(20–30% augmentation\): Directly achievable with today's Warrior Web-programme technology; the concealment constraint requires further development but is not physically prohibitive.

### 12.2 Long-Range Projections \(15–25 Years\)

Several elements require 15–25 year research trajectories:

- 5× strength exoskeleton in combat coverall profile: Requires 15–20× actuator energy density improvement from current soft actuator baselines. This is achievable in principle but represents a major engineering challenge.
- Carbyne reinforcement at production scale: Requires resolution of the chain crosslinking stability problem and development of fibre-format synthesis methods. The 2016 DWCNT-stabilised chain synthesis provides proof of concept.
- Radar-band active cancellation: CNT absorption materials are demonstrated; integration into a mechanically stressed combat textile without performance degradation is an open problem.

### 12.3 Highly Speculative Elements

Three elements of the OBSIDIAN-X specification are assessed as highly speculative beyond the 25-year programme horizon:

- Nuclear battery as primary power source at claimed energy density: Current betavoltaic cells operate in the microwatt range per gram; the '3,000× gasoline energy density' claim requires a 10⁶× improvement in specific power — physically constrained by isotope activity limits.
- Multi-spectrum active invisibility simultaneously across visible, thermal, and radar bands: Each spectral band has independent physical requirements that impose conflicting design constraints. Achieving all three simultaneously in a mechanically robust combat suit is not projected within any current research trajectory.
- 'Unlimited operational duration' and 'unlimited service life': These are aspirational design targets rather than physically achievable specifications. Even the most chemically stable materials experience mechanical fatigue; the exoskeleton power system imposes finite energy storage limits.

## 13. Conclusion

Project OBSIDIAN-X represents a coherent and ambitious specification for the theoretical frontier of full-body combat armour. Structured as a 25-year horizon document, it articulates a set of system requirements that, if met, would represent a qualitative discontinuity in individual soldier capability equivalent to the introduction of the repeating rifle or the armoured fighting vehicle.

The paper establishes that the protection and sensor-integration elements of the specification — advanced UHMWPE-graphene composite armour, full-body CBRN sealing, multi-spectral AR HUD, and partial exoskeletal strength augmentation — are reachable within a 10–20 year focused programme, with the IVAS programme already demonstrating the AR HUD pathway and current graphene-enhanced armour demonstrating the materials pathway. The full 5× strength exoskeleton, nuclear primary power, and multi-spectrum active invisibility elements are long-range projections requiring breakthrough science, not incremental engineering.

The operational philosophy — 'Total protection through synthetic perfection and battlefield supremacy' — is most accurately understood as a design vector: a sustained commitment to eliminating organic and degradable materials, maximising mechanical performance through carbon allotrope science, and integrating information and protection systems into a unified operator interface. This vector, regardless of whether all individual performance targets are ultimately met, will drive fundamental improvements in soldier protection, lethality, and survivability across the next generation of military equipment.

## Appendix A — Governing Equations

> **HYPOTHETICAL / FOR ACADEMIC STUDY ONLY.** Project OBSIDIAN-X is a 25-year horizon specification for a full-body combat armour system. **No carbyne-UHMWPE-metamaterial composite armour at the specifications described has been manufactured, ballistic-tested, or fielded.** The equations and numerical results in this appendix are mechanistic projections from the published materials-science literature; they are not measurements of any built OBSIDIAN-X article. Multi-spectrum active invisibility, 5× exoskeleton strength multiplication, and the projected nuclear-battery primary-power architecture are explicitly identified in §12.3 of the body text as highly speculative elements.

The ballistic-limit, back-face-deformation, obliquity, RTG power, and stealth / signature-reduction equations that anchor the §3 / §5 / §7 / §12 system-architecture claims are reproduced in closed form below. The first four formulae are the same Lambert-Jonas / clay-witness / Tate-Krupp / RTG framework as in the OBSIDIAN research paper appendix; the fifth section presents the radar-cross-section (RCS) reduction model for §4.2.

### A.1 Lambert-Jonas V50 for the OBSIDIAN-X composite armour

Per Paper 13 §A.1 and the OBSIDIAN paper §A.1, the §3 composite armour V50 is given by:

```
V50² = V_BL² + (m_p / (m_p − m_pl)) × V_residual²
V_BL  = √( (2 × W_plastic + 2 × W_shear + 2 × W_brittle) / m_p )
```

For a NIJ Level IV reference threat (`m_p = 10.8 g, V = 878 m/s`, .30-06 M2 AP) against the §3 four-component matrix (40 % carbyne nanorope + 25 % topological insulator + 20 % programmable metamaterial + 10 % self-healing SMA), scaling from the `weapons_sim_results.md` §13 APES military reference (V50 = 1 041 m/s for the §13 military-armour baseline):

→ **V50 (OBSIDIAN-X coverall vs .30-06 M2 AP) ≈ 1 100 m/s** (mechanistic projection — `~5 % uplift over the APES baseline` due to projected carbyne stiffness gain). The 50+ multi-hit capability of §10.1 is a self-healing-SMA-mediated repair claim that is not captured in this single-shot V50 envelope and remains unvalidated.

### A.2 Back-face deformation — clay-witness model

Same formulation as the OBSIDIAN paper §A.2:

```
BFD = E_residual_strain / (k_plate × π × D_p)
k_plate = (E_composite × t_plate³) / (12 × (1 − ν²) × R_eff²)
```

For the §3 OBSIDIAN-X coverall at full thickness across the composite, projected BFD against the .30-06 M2 AP at the V50 stopping case `≈ 6 mm` — within the NIJ 0101.06 44 mm ceiling.

### A.3 Obliquity correction (Tate / Krupp)

Same formulation as the OBSIDIAN paper §A.3:

```
V50(θ) = V50(0°) / cos(θ)^n        # n = 1.6 small-arms; n = 0.7 APFSDS
```

For a 30°-from-normal impact (`weapons_sim_results.md` §12 reference geometry):

```
V50(30°, OBSIDIAN-X) = 1 100 / 0.866^1.6 ≈ 1 386 m/s
```

→ **Defeats all small-arms threats in the §10.1 envelope at 30° obliquity.**

### A.4 Nuclear battery / RTG power model (cross-reference OBSIDIAN paper §A.4)

The §7.1 "nuclear diamond battery" claim of 3 000× gasoline energy density requires the same RTG decay model:

```
P_RTG(t) = P_0 × exp(−λ × t)            # λ = ln(2) / t_½

C-14 betavoltaic:   t_½ = 5 730 yr    → λ ≈ 1.21 × 10⁻⁴ /yr (essentially constant over 50 yr)
Ni-63 betavoltaic:  t_½ =   100 yr    → λ ≈ 6.93 × 10⁻³ /yr (~7 %/yr decay)
Pu-238 thermal:     t_½ =  87.7 yr    → λ ≈ 7.91 × 10⁻³ /yr (~0.79 %/yr after thermoelectric conversion)
```

**Energy-density reality check.** A diamond C-14 betavoltaic at 2024 state-of-art (~1 µW/g at the Bristol / Arkenlight prototype scale) compared against gasoline:

```
E_betavoltaic_50yr   = 1 µW/g × 50 yr × 3.156 × 10⁷ s/yr ≈ 1 580 J/g
E_gasoline_chemical  = 46 MJ/kg = 46 000 J/g
Ratio                = 0.034 — i.e., C-14 betavoltaic is ~30× LESS dense than gasoline,
                        not 3 000× more
```

→ **The §7.1 "3 000× gasoline energy density" claim is rejected by closed-form analysis** (a 10⁶× improvement in current betavoltaic power density would be required; this is constrained by the 156 keV beta endpoint and semiconductor conversion efficiency). The body text's §7.1 footnote already acknowledges this as "highly speculative"; the §A.4 model quantifies the gap.

### A.5 Radar cross-section (RCS) reduction model

The §4.2 radar-band signature reduction claim (CNT absorption mesh, 90+ % absorption at C/X/Ku-band) is characterised by the RCS model:

```
RCS = σ = 4π × |F|²

with
  σ    = effective radar cross-section (m²)
  F    = reflection coefficient (—)

For a perfectly absorbing surface:    |F| → 0  → σ → 0
For a perfectly reflecting surface:   |F| → 1  → σ = 4π × A_geometric (maximum)
```

The RCS-reduction figure of merit for an absorptive coating is:

```
ΔRCS_dB = 20 × log10( |F_baseline| / |F_with_coating| )
        = 20 × log10( 1 / sqrt(1 − α_absorption) )

with α_absorption = absorption fraction at the radar frequency
```

For the §4.2 design target `α = 0.90`:

```
ΔRCS = 20 × log10( 1 / sqrt(0.10) ) = 20 × log10( √10 ) ≈ +10 dB RCS reduction
```

→ **CNT-mesh RCS reduction (design target) ≈ 10 dB at the C/X/Ku absorption frequencies.** A 10 dB RCS reduction translates to a ~44 % range reduction for a target-detection radar (`R_detect ∝ σ^¼`), which is operationally meaningful but not "invisibility" — consistent with the §12.3 framing of multi-spectrum active invisibility as a "highly speculative element." Achieving the projected 10 dB performance across the broad C–Ku frequency span (4–18 GHz) in a mechanically stressed combat textile is the open engineering problem; current CNT-absorber demonstrations achieve 10–20 dB at narrower bands only.

---

## References
**[1]** Futurism. First Direct Proof of Stable Carbyne, The World's Strongest Material. futurism.com. November 2016. \[6,400-atom chains in DWCNT hosts\]

**[2]** Liu, M., Artyukhov, V.I., Lee, H., Xu, F., Yakobson, B.I. Carbyne from First Principles: Chain of C Atoms, a Nanorod or a Nanorope. ACS Nano 7\(11\), 10075–10082 \(2013\). doi: 10.1021/nn404177r.

**[3]** Feng, Y. et al. Low-Temperature Synthesis of Weakly Confined Carbyne Inside Single-Walled Carbon Nanotubes. ACS Nano \(2025\). doi: 10.1021/acsnano.4c17104.

**[4]** Wikipedia. Integrated Visual Augmentation System \(IVAS\). en.wikipedia.org/wiki/Integrated\_Visual\_Augmentation\_System. Accessed March 2026.

**[5]** Army Times. Army's mixed reality device nears fielding with final testing in 2024. armytimes.com. December 2023.

**[6]** US Army. Prototype exoskeleton suit would improve Soldiers' physical, mental performance. army.mil/article/190776. July 2017.

**[7]** IEEE Spectrum. DARPA Tests Battery-Powered Exoskeletons on Real Soldiers. spectrum.ieee.org. 2021.

**[8]** Dyneema® \(Avient Corporation\). Soft body armor vests. dyneema.com. Accessed March 2026.

**[9]** Protection Group Denmark. What ballistic materials are used to make a bulletproof vest? protectiongroupdenmark.com. January 2025.

**[10]** Dyneema® \(Avient Corporation\). Vest inserts and ballistic shields — defence research shows heavy loads negatively impact soldiers' mobility. dyneema.com. Accessed March 2026.

**[11]** AFCEA International. The Rise of the Humanoid: Exoskeletons Revolutionising Military Readiness. afcea.org. Accessed March 2026. \[28.3% noncombat wounds from spine/back injuries, US Army 2021\]

**[12]** US Army. Heads-up display to give Soldiers improved situational awareness — Tactical Augmented Reality \(TAR\). army.mil/article/188088. 2017.

**[13]** SOFWERX / USSOCOM. Day and Night Heads Up Display \(DANHUD\) Assessment Event. events.sofwerx.org/day-and-night-heads-up-display. 2024.

**[14]** SRI International. 75 Years of Innovation: SRI SuperFlex Suit \(DARPA Warrior Web Program\). sri.com. 2025.

**[15]** Army Technology / International Defense Security & Technology. TALOS Programme and Future Military Exoskeletons. army-technology.com; idstch.com. Accessed 2026.

**[16]** Kotrechko, S. et al. Mechanical properties of carbyne: experiment and simulations. Nanoscale Research Letters 10, 24 \(2015\). doi: 10.1186/s11671-015-0761-2. \[251 GPa at 77 K\]

**[17]** Wikipedia. Linear acetylenic carbon — topological insulator properties. en.wikipedia.org/wiki/Linear\_acetylenic\_carbon. Accessed March 2026.

**[18]** C&EN / ACS. Carbyne Predicted To Be Strongest Known Material — and MultiCam camouflage pattern background. cen.acs.org. 2013.

**[19]** PMC / MDPI. Advancement in Graphene-Based Materials and Their Nacre Inspired Composites for Armour Applications. PMC8151629. 2021. \[graphene tensile wave speed 21.3 km/s vs diamond 17.5 km/s\]

**[20]** The Graphene Solution. Graphene Military Defense: Innovations for 2025. thegraphenesolution.com. 2025.

**[21]** Defence News. Army's mixed reality device set for upgrades and battalion assessment. defensenews.com. October 2024.

**[22]** Breaking Defense. HUD 3.0: Army To Test Augmented Reality For Infantry. breakingdefense.com. 2018.

*— END OF DOCUMENT —*
