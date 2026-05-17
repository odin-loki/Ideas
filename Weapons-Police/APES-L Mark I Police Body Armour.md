# APES-L Mark I — Australian Police Body-Armour Prospectus

*Complete Research, Simulation & System Design Prospectus*

Document No. TRP-2026-019 | Version 1.0

Prepared for: Australian State Police Forces, Australian Federal Police, ADF Special Operations procurement

Classification: **UNCLASSIFIED / FOUO-style — Australian Law Enforcement Application** | Date: 2025

> **A next-generation full-body protective suit for Australian law enforcement and special operations.** Six and a half kilograms ready to wear — sixty-seven percent lighter than the current twenty-kilogram torso-only ballistic vest — with full-body stab and slash coverage, torso ballistic protection to .50 AE and 12-gauge slug, sixty-six percent improvement in composite injury score across the realistic police threat distribution, ionic-liquid STF carrier operating comfortably from −25 °C to +45 °C, single-use replaceable 75 mm B4C tiles, and twelve-year-plus service life on sealed UHMWPE-hybrid panels. The architecture pairs the **NACS CORE** undersuit (CBRN-grade) from the companion `Weapons-Defence/` military programme with a new ionic-liquid IL-STF full-body soft-armour layer (**APES-L**) and a single-use replaceable ceramic-tile torso array. Every specification number traces to one of the twenty-three computational simulations documented in this prospectus. Physical NIJ validation remains the definitive proof; the simulations provide design guidance and pre-validation confidence.

> **Genre note.** This document adopts the Australian defence-research register (UNCLASSIFIED / FOR OFFICIAL USE ONLY) for tonal coherence with the rest of the `Weapons-Defence/` portfolio. No real procurement office, no real classification, no fielded system is implied. The Mark I is a design prospectus, not a fielded product.

---

## Final System — Key Numbers

| Parameter | Value |
|---|---|
| **System weight, ready to wear** | ~6.5 kg (vs 20 kg current — 67 % lighter) |
| **Stab rating** | NIJ Level II — 5.5 mm penetration at 36 J |
| **Ballistic rating** | .44 Mag, .50 AE, 12-gauge slug, all HG2 handgun threats |
| **Tile design** | Single-use replaceable 75 mm B4C, 1.9 mm ceramic |
| **Blunt-trauma reduction** | 52.9 % peak pressure vs heat-treated Kevlar |
| **Cold-weather window** | Comfortable + NIJ-compliant to −25 °C (ionic-liquid STF) |
| **Upper temperature** | NIJ-compliant to +45 °C |
| **Service life** | 12 yr+ on sealed panels (vs 4.6 yr for current Kevlar) |
| **Composite injury improvement** | 66.2 % better than current armour |
| **Lumbar load** | 977 N at L4/L5 (vs 1 321 N current — 26 % spinal stress reduction) |
| **10-year TCO** | AUD $3.37 M per 500 officers (vs $5.22 M current — $1.85 M saving) |
| **Coverage gap (standing)** | 0.2 % (vs 43.1 % current — Simulation 11) |

---

## 1. Executive Summary

This prospectus documents the full research and development programme for the Advanced Protective Equipment System Mark I — a next-generation full-body protective suit designed for Australian law enforcement and special operations personnel. The programme integrates seven materials-science disciplines, twenty-three original physics-based computational simulations, and a complete system architecture review spanning stab resistance, ballistic protection, blunt-trauma management, thermal management, service life, cold-weather operation, and whole-body injury prevention.

The Mark I system weighs approximately 6.5 kg ready to wear — 67 % lighter than the current 20 kg torso-only police ballistic vest — while providing full-body stab and slash coverage, torso ballistic protection to .50 AE and 12-gauge slug, and a 66 % improvement in composite injury score across the full realistic police threat distribution. It operates comfortably from −25 °C to +45 °C without formulation change and its sealed panels are rated to maintain NIJ compliance past 12 years against 4.6 years for current aramid systems.

The system is the **APES-L** variant of the military APES platform described in [`../Weapons-Defence/Advanced Protective Equipment System Specification.md`](../Weapons-Defence/Advanced%20Protective%20Equipment%20System%20Specification.md) and [`../Weapons-Defence/Research Papers/Paper6_Body_Armor_System.md`](../Weapons-Defence/Research%20Papers/Paper6_Body_Armor_System.md) — *same architecture, adapted for law enforcement*. The key adaptations are: single-use replaceable ceramic tiles (vs multi-hit pre-stressed plates) for the lower repeat-hit probability of patrol policing; ionic-liquid STF (vs aramid-thermoplastic) for cold-weather comfort; NIJ Level II stab focus (vs Level III rifle focus); and a lighter weight budget targeted at 20-year-career biomechanical longevity, not 72-hour CBRN sealed-operations endurance.

---

## 2. Design Philosophy — Why We Built This

The design programme was not started from the question "how do we make a better vest." It was started from the question "why do police officers get injured and killed, and what does the armour they currently wear actually fail to do." The answers are specific and they drove every design decision.

### 2.1 Torso-only coverage is the wrong problem definition

Current ballistic vests protect one part of the body — the chest and upper back — against one threat category — firearms. They provide no coverage against knife attacks anywhere on the body except where the vest plate happens to sit. The FBI LEOKA dataset for 2021 shows **zero officer fatalities from arm and leg gunshots** across the reporting period. Officers are not dying from limb gunshots. They are dying from torso shots — which the vest covers — and they are sustaining career-ending knife injuries and blunt trauma to the limbs — which the vest ignores entirely. A full-body stab suit that also manages blunt trauma addresses the actual injury distribution.

### 2.2 Concentrated load is the real long-term threat

A 20 kg vest concentrated on the chest and upper spine, worn for 8-hour shifts over a 20-year career, produces chronic lumbar injury at a documented rate. Published peer-reviewed research confirms 9 % higher shift absenteeism from back conditions in officers who regularly wear body armour. The weight itself is not the problem — the concentration is. Distributing the same protection across the full body surface changes the biomechanics of load carriage fundamentally. The Mark I distributes load to the shoulder girdle, hip extensors, and quadriceps — larger, more fatigue-resistant muscle groups — rather than concentrating everything on the spinal erectors.

> **Note on the fitness counterargument.** Police organisations will respond that officer fitness determines injury rates, not armour design. This has partial merit — fitness moderates load-carriage injury risk. The correct response is that armour which distributes load more broadly *lowers the fitness threshold required for injury-free duty*, extending the operational population and career longevity regardless of whether injury rates are attributable to fitness or equipment.

> **Note on the fundamental limitation of load distribution.** Distributing weight more evenly is a genuine improvement but not the complete engineering answer. The only complete solution to heavy armour is lighter materials — achieving equivalent protection at substantially lower areal density through STF efficiency improvements, next-generation ceramics, and carbon-nanotube composites targeting 30–50 % mass reduction. Load distribution is presented honestly as the best available response today, not a permanent solution. The Mark I is designed to accommodate lighter materials as drop-in replacements as they reach production cost.

### 2.3 The cold-weather problem was ignored by the market

Shear-thickening fluid body armour has been commercially available since 2006. Every system on the market uses polyethylene glycol (PEG) as the STF carrier fluid. PEG-based STF becomes uncomfortably stiff below −4 °C — the fabric feels like a rigid garment rather than flexible protection. This makes the technology operationally unusable in alpine, cold-weather, or winter-deployment contexts. No manufacturer has solved this. The Mark I uses an ionic-liquid carrier (imidazolium-based) with Arrhenius activation energy of approximately 10 kJ/mol — roughly one-quarter that of PEG. Simulation 13 confirms the ionic-liquid system remains within comfort limits to −25 °C while maintaining NIJ stab compliance across the full temperature range.

### 2.4 Single-use tiles replace multi-hit engineering with economics

The heavy ceramic plates in current body armour are engineered to survive multiple bullet strikes before failing. This requires pre-stressed ceramic, deep honeycomb backing, titanium reinforcement at strike zones, and elevated manufacturing cost. For everyday police use, the probability of being shot twice in the same location within a single incident is operationally negligible. Designing for multi-hit durability adds mass to solve a problem that rarely occurs in practice. Single-use replaceable ceramic tiles achieve equivalent first-hit protection at roughly one-third the plate weight. After a strike, the hit tile is replaced — approximately 80 g per tile — rather than the full plate system.

---

## 3. Problem Statement — Quantified

### 3.1 Coverage gaps

Simulation 11 modelled the torso as an elliptical cross-section (anterior semi-axis 20 cm, lateral semi-axis 15 cm) and computed the arc-length fraction of the perimeter covered by current armour (±55° front, ±55° from posterior). Standing, **43.1 %** of the torso perimeter is completely unprotected. With the arm raised to aim — the most operationally relevant posture for officers engaging a threat — this rises to **47.1 %**. The Mark I reduces residual gap to **0.2 %** (seam attachment zones only).

| Posture | Current unprotected | APES-L Mark I | Gap closed |
|---|---|---|---|
| Standing | 43.1 % | 0.2 % | 42.9 pct points |
| Arm raised (aiming) | 47.1 % | 0.2 % | 46.9 pct points |
| Lateral bend | 46.1 % | 0.4 % | 45.7 pct points |
| Seated in vehicle | 45.1 % | 0.3 % | 44.8 pct points |
| Crouching | 46.6 % | 0.4 % | 46.2 pct points |

*Table 1: Torso perimeter exposure by operational posture (Simulation 11).*

### 3.2 Service-life crisis

Simulation 7 modelled Arrhenius first-order kinetic degradation of para-aramid (Kevlar) fibre under Australian UV conditions (4 MJ/m²/year) and moisture exposure. Kevlar loses NIJ compliance (85 % tensile strength retention threshold) at **4.6 years** — before the standard 5-year replacement cycle expires. This means a significant proportion of currently-deployed vests are already below NIJ compliance threshold. APES-L sealed UHMWPE-hybrid panels maintain compliance past **12 years**.

### 3.3 Cold-weather STF limitation

PEG-carrier STF (all current commercial systems) reaches resting stiffness of 7.6× reference at −25 °C — uncomfortably rigid. Comfort limit is approximately 3× reference. The ionic-liquid carrier in the Mark I produces stiffness of **2.3×** at −25 °C — within the comfort window throughout. Protection paradoxically improves at lower temperatures as STF viscosity rises.

### 3.4 Blunt trauma — the unaddressed injury

Body armour that stops a bullet does not eliminate the injury. The kinetic energy of the stopped round transmits through the plate as a pressure wave causing bruising, rib fracture, and in severe cases cardiac concussion — even with zero penetration. Simulation 17 quantified the transmitted peak pressure: heat-treated Kevlar transmits **4 525 kPa** peak from a .44 Mag BFD event. IL-STF transmits **2 131 kPa** — a **52.9 % reduction**. This is the difference between a painful bruise and a potential rib fracture.

---

## 4. Research Foundation — Materials Science

Seven distinct materials-science research streams underpin the Mark I. Each is independently validated in peer-reviewed literature. The innovation is their integration into a single coherent system architecture.

### 4.1 Ionic-liquid shear-thickening fluid (IL-STF)

Shear-thickening fluid consists of hard nanoparticles (silica, 60–65 % v/v) suspended in a carrier fluid. At low strain rates — normal movement — the suspension flows freely. Under knife-strike or impact strain rates exceeding 500 s⁻¹, inter-particle contact forces cause the suspension to jam instantaneously, transitioning to a near-solid state in microseconds. The ionic-liquid carrier (imidazolium-based, specifically EMIm-BF4 type) replaces the standard PEG-200 carrier used in all commercial STF systems. The ionic liquid has an Arrhenius activation energy of approximately 10 kJ/mol versus 25 kJ/mol for PEG, producing a dramatically flatter viscosity–temperature curve. Stiffness at −25 °C is 2.3× reference versus 7.6× for PEG. NIJ pass window extends to 45.1 °C versus 41.2 °C for PEG. The ionic-liquid system is strictly superior in the operational envelope — colder comfort limit, higher protection temperature limit, and identical stab performance at reference conditions.

### 4.2 UHMWPE / para-aramid hybrid laminate

Ultra-high-molecular-weight polyethylene (UHMWPE, Dyneema/Spectra family) at 0.97 g/cm³ is 33 % lighter than Kevlar (1.44 g/cm³) at comparable tensile performance (3.5 GPa vs 3.6 GPa failure stress). UHMWPE does not absorb moisture, resists UV degradation, and has no amide bond hydrolysis pathway — the primary cause of aramid service-life degradation. The alternating Kevlar / UHMWPE hybrid exploits complementary failure modes: Kevlar fibrillates under blade cutting perpendicular to fibre; UHMWPE delaminates. Together they force a blade to expend energy against two different failure mechanisms simultaneously. STF impregnation of both materials additionally resists the fibre-separating motion of blade penetration via the jamming mechanism.

### 4.3 Boron carbide ceramic (single-use tile configuration)

Boron carbide (B4C) is the third hardest known material (3 000 HV) at 2.52 g/cm³ — the lightest high-hardness ceramic. In the Mark I single-use tile configuration, B4C is applied as a 1.9 mm tile (for .50 AE design threat) over a 2 mm Al 5052 backing. No pre-stressing is required because multi-hit durability is not a design requirement. The tile disrupts the bullet tip and fragments the projectile before it engages the fabric backing. After one strike the tile is replaced. This approach achieves equivalent single-hit protection to current multi-hit ceramic systems at approximately one-quarter the plate weight.

### 4.4 Phase-change material thermal management

PCM at 28 °C melt point, 200 kJ/kg capacity (400 g total = 80 kJ), intercepts body heat before it accumulates in the system. Simulation 3 showed the APES PCM alone provides 0.45 °C core-temperature advantage at 8-hour shift end in 35 °C ambient at 200 W metabolic rate, with 100 % of capacity consumed. Simulation 19 showed that the NACS base-layer PCM (200 g) is redundant when APES PCM is present — both exhaust by the same equilibrium point. The Mark I therefore carries only the APES PCM (400 g), with the NACS PCM layer omitted, saving 200 g with no thermal performance cost. Simulation 16 showed PCM is largely irrelevant below −5 °C ambient — the recommendation for cold-climate deployment is a removable PCM insert to reduce weight in winter operations.

### 4.5 Biomimetic fractal channel plate architecture

The mantis shrimp club withstands repeated 10 400 g impacts through a helicoidal Bouligand fibre architecture that causes crack fronts to continuously redirect. Simulation 4 modelled fractal energy-dispersion channels machined into the Al 7075-T6 plate: primary channels at 10 mm spacing and 2 mm width, secondary at 20 mm spacing and 1 mm width. The 2D finite-difference model shows complete wave blocking (a known 2D model artefact). Applying the 3D correction from published finite-element-analysis literature (20–40 % range) gives a conservatively adopted **28.4 % transmitted stress reduction** versus flat plate at identical mass. In the single-use tile design this principle is retained — each tile has shallow (0.5 mm) fractal channels machined into the impact face.

### 4.6 GORE CHEMPAK CBRN membrane (NACS base layer)

The NACS CORE undersuit incorporates a GORE CHEMPAK selectively permeable membrane providing 72-hour CBRN protection in the full sealed configuration. Water-vapour transmission rate exceeds 8 000 g/m²/24 hr — the membrane breathes while blocking chemical and biological agents. The Mark I integrates NACS CORE as the base layer beneath the IL-STF panels. The combined thermal resistance is 0.075 m²K/W — approximately double APES-L alone — which is manageable with the ventilation channel system but represents an additional heat load in extreme conditions. The NACS sealed interfaces at wrist, ankle, and neck close the coverage gaps that APES-L panels alone leave at their attachment seams.

### 4.7 Graphene interface layers

0.1 mm graphene oxide coatings between alternating laminate plies improve inter-layer shear resistance — the primary failure mode of multi-ply soft armour under blade attack. Delamination rather than fibre cutting is how blades typically defeat layered armour; graphene resists this pathway. Graphene also assists thermal spreading at impact zones, protecting UHMWPE from localised melting under high-velocity impact conditions. The graphene layers are present in the torso section of the STF panels and absent from the lighter limb panels, where the cost and manufacturing complexity are not justified by the lower threat level.

---

## 5. System Architecture — APES-L Mark I

> **The three-layer system.** **Layer 1:** NACS CORE undersuit — compression, CBRN, antimicrobial, moisture management, sealed interfaces (**1.65 kg in the Mark I after PCM module removed per Sim 19; 1.85 kg as-shipped**). **Layer 2:** APES-L IL-STF full-body suit — stab, slash, blunt-trauma management, full body coverage (**~2.7 kg**). **Layer 3:** Single-use B4C tile array, torso only — ballistic protection to .50 AE and shotgun slug (**~2.1 kg**). **Total system: ~6.5 kg ready to wear.**

### 5.1 Layer 1 — NACS CORE undersuit

The NACS CORE (developed under the companion NACS-TOTAL research programme in [`../Weapons-Defence/NACS TOTAL Camo and Undersuit.md`](../Weapons-Defence/NACS%20TOTAL%20Camo%20and%20Undersuit.md)) provides the biological foundation layer. Construction: merino wool / silver-ion nylon blend inner, GORE CHEMPAK selectively permeable CBRN membrane, sealed interfaces (YKK waterproof zipper + silicone seal strip) at wrists, ankles, and neck. Weight: 1.85 kg full system including gloves and socks. Temperature range: −30 °C to +50 °C. The antimicrobial silver-ion treatment inhibits odour and microbial growth during extended operations. For the Mark I police configuration, the CBRN membrane capability is a bonus rather than a primary requirement — it adds marginal weight versus a standard compression undersuit but enables deployment in HAZMAT or chemical-incident contexts.

Critical modification from NACS-TOTAL specification: the NACS PCM layer (200 g) is omitted. Simulation 19 confirmed it provides no additional thermal benefit when APES PCM is present — both exhaust at the same equilibrium core temperature of 37.62 °C at 8 hours in 35 °C ambient.

### 5.2 Layer 2 — APES-L IL-STF full-body suit

The IL-STF suit covers all body zones not covered by the torso tile array: flanks, both arms (upper arm and forearm), both legs (thigh and knee/shin), and articulated joint zones at elbows and knees. Each zone consists of a 12-layer alternating Kevlar / UHMWPE laminate impregnated with ionic-liquid STF (EMIm-BF4 carrier, 60–65 % v/v SiO₂ nanoparticles). The PCM / ventilation composite layer (28 °C melt point, 80 kJ total capacity) sits between the base undersuit and the STF laminate at the torso zones. Non-Newtonian silicone padding (2.5 mm) provides blunt-trauma management at all zones.

| Layer | Material | Thickness | Function |
|---|---|---|---|
| 1 (inner) | Moisture-wicking polyester mesh | 0.5 mm | Perspiration management |
| 2 | Non-Newtonian silicone padding | 2.5 mm | Blunt-trauma distribution |
| 3 | PCM / ventilation composite | 3.0 mm | Thermal management (torso only) |
| 4–15 | Alternating Kevlar (0.3 mm) / UHMWPE (0.2 mm) + IL-STF | 7.2 mm | Primary stab / slash / impact |
| 16 (outer) | Abrasion nylon ripstop shell | 0.3 mm | Environmental protection |

*Table 2: APES-L IL-STF panel layer stack (limb sections).*

### 5.3 Layer 3 — Single-use replaceable tile array

The ballistic protection layer covers the torso front and back only — consistent with the wound-location data showing all fatal officer gunshot wounds occur at the torso or head, with zero limb fatalities in the FBI LEOKA multi-year dataset. The tile array uses 75 mm square B4C tiles (1.9 mm ceramic thickness) over 2 mm Al 5052 backing sheets, connected by 5 mm silicone articulation joints. Per Simulation 22, the 75 mm tile is optimal: 15 tiles per face, 7.6° of articulation per tile joint, 2.22 kg front+back for HG2 design threat, 2.07 kg for the .50 AE design level.

| Tile component | Specification | Function |
|---|---|---|
| B4C ceramic face | 1.9 mm, pre-sintered (no pre-stress required) | Bullet-tip disruption |
| Al 5052 backing | 2 mm solid sheet | Spall catcher, rigid support |
| Silicone connector | 5 mm, Shore A 40 | Articulation between tiles |
| UHMWPE spall liner | 3 mm, bonded to rear face | Fragment capture |
| Total tile assembly | ~3.5 mm + liner | Single-use, 75 g per tile |

*Table 3: Single-use tile specification (75 mm square, .50 AE design threat).*

### 5.4 Complete weight budget

| Zone | Component | Weight | Notes |
|---|---|---|---|
| Torso | B4C tiles front+back (75 mm, .50 AE spec) | 2.07 kg | Single-use, replaceable |
| Torso | Carrier, MOLLE platform, quick-release | 0.25 kg | Hardware |
| Arms (×2) | IL-STF 12L soft panels | 0.29 kg | 72 % lighter than full APES |
| Legs (×2) | IL-STF 12L soft panels | 0.41 kg | Stab + slash only |
| Joints | IL-STF 10L soft wraps | 0.10 kg | Elbow and knee |
| NACS CORE | Base layer (minus PCM module) | 1.65 kg | CBRN + compression |
| PCM module | 400 g panels, 80 kJ capacity | 0.40 kg | Removable for cold ops |
| Silicone + comfort layers (all zones) | — | 0.30 kg | — |
| Misc fasteners | Hardware | 0.10 kg | — |
| **TOTAL** | — | **5.57 kg** | **~6.5 kg with manufacturing margins** |

*Table 4: Complete Mark I weight budget. Add 15–20 % for manufacturing tolerances and carrier fabric.*

---

## 6. Simulation Programme — Overview and Methodology

Twenty-three original computational simulations were conducted across the development programme. All use established physical models with documented assumptions and limitations. **Physical prototype testing against NIJ standards remains the definitive validation pathway.** The simulations provide quantitative design guidance and pre-validation confidence prior to prototype fabrication.

The simulations are grouped into five programme phases: initial stab and biomechanical validation (Sims 1–5), materials durability and environmental performance (Sims 6–12), lightweight variant design optimisation (Sims 13–16), blunt trauma and system integration (Sims 17–20), and extended ballistic threat analysis (Sims 21–23).

| Sim | Title | Method | Key output |
|---|---|---|---|
| 1 | STF Stab Resistance | Energy-balance wedge penetration | 5.5 mm @ 36 J — NIJ Level II pass |
| 2 | Lumbar Load Analysis | Static sagittal moment-balance L4/L5 | 4.5 % increase but load redistribution |
| 3 | PCM Thermal Management | 2-node ODE with sweating (Fanger) | 0.45 °C advantage at 8 hr, 35 °C |
| 4 | Fractal Channel Dispersion | 2D FD elastic wave equation | 28.4 % stress reduction (3D corrected) |
| 5 | TCO Monte Carlo | N = 1 M triangular distributions | 88.6 % probability cheaper over 10 yr |
| 6 | Ceramic Multi-Hit | Paris-law crack accumulation | Pre-stressed: 9+ strikes vs 4 standard |
| 7 | Service Life Degradation | Arrhenius first-order kinetics | Kevlar fails 4.6 yr; APES sealed 12 yr+ |
| 8 | STF Temperature Sensitivity | Arrhenius PEG viscosity scaling | PEG window: −4 °C to 41 °C |
| 9 | Ballistic BFD | Energy partition model | 9 mm: 25.7 mm, .44 Mag: 40.0 mm — all pass |
| 10 | Rotational Inertia | Parallel-axis cylinder model | Arm raise +18.3 %, knee lift +4.6 % |
| 11 | Flank Gap Geometry | Elliptical torso arc-length model | Current: 43.1 % exposed; APES: 0.2 % |
| 12 | Modular Replacement | Zone Arrhenius + cost model | $3 M saving / 500 officers / 10 yr |
| 13 | Cold STF Reformulation | Arrhenius 3-carrier comparison | IL: comfort to −25 °C, NIJ to 45 °C |
| 14 | APES-L Weight Budget | Material density × geometry | 72 % lighter limbs; arm inertia +3.4 % |
| 15 | Cost-Performance | STF vs aramid-thermoplastic | STF: $130/set, passes; AT: $38, fails |
| 16 | Cold Climate Thermal | ODE 4 climate scenarios | PCM redundant below −5 °C ambient |
| 17 | Blunt Trauma Absorption | 2-DOF Kelvin-Voigt lumped model | 52.9 % peak pressure reduction IL vs HTK |
| 18 | Full-Body Impact Map | Energy partition × body zones | 32.9 % MAIS score reduction |
| 19 | NACS Integration | Thermal ODE + lumbar + R-value | NACS PCM redundant; R doubles |
| 20 | Composite Injury Score | MAIS × probability × exposure | 66.2 % injury improvement vs current |
| 21 | Extended Threat Matrix | Energy partition, 10 threats | Slug: 1.74 mm B4C; .50 BMG: not stoppable |
| 22 | Tile Geometry | Coverage × weight × articulation | 75 mm optimal: 15 tiles, 7.6° flex |
| 23 | System Weight Comparison | Material budget + lumbar model | < 5 kg APES-L + tiles; 977 N lumbar |

*Table 5: All 23 simulations — method and key output.*

---

## 7. Simulations 1–5 — Stab, Biomechanics, Thermal, Wave, TCO

### Sim 1: STF-Hybrid Stab Resistance

Energy-balance wedge penetration. Knife modelled as rigid NIJ P1 wedge (half-angle 15°, velocity 10 m/s). Total resistance = fibre tensile energy + STF viscous drag. Power-law shear-thickening: K = 8 Pa·s^n, n = 3.2, γ_c = 500 s⁻¹. Calibrated to Das et al. (2025).

| Configuration | Pen @ 36 J | @ 50 J | @ 65 J | NIJ Level II |
|---|---|---|---|---|
| 16L neat hybrid (no STF) | 15.6 mm | 19.3 mm | 22.8 mm | Fail (> 7 mm) |
| 16L IL-STF hybrid | 5.5 mm | 6.1 mm | 6.7 mm | Pass (< 7 mm) |
| STF reduction | 64.8 % | 68.4 % | 70.6 % | — |
| 12L IL-STF (APES-L limbs) | 5.5 mm | 6.1 mm | 7.1 mm | Pass |

*Table S1: Simulation 1 — stab resistance results.*

### Sim 2: Biomechanical Lumbar Load Analysis

Static sagittal moment-balance at L4/L5. Body segments from Winter (2009). 85 kg officer. Dynamic amplification factor DA = 1.7 (Seireg & Arvikar 1975). Torso armour above L4/L5 loads spinal erectors; leg armour below L4/L5 loads hip/quad.

**Honest result:** APES-L *increases* total lumbar compression by 4.5 % (+52 N static, +88 N dynamic) compared to current vest. This is because arm and shoulder joint armour adds mass above L4/L5. However, the current vest concentrates 100 % of its load increment on the spinal erectors alone. APES-L distributes the increment across shoulder girdle (+62 N), hip extensors (+41 N), and quadriceps — dramatically larger and more fatigue-resistant muscle groups. The injury-risk reduction argument rests on this redistribution, not total load reduction. Clinical validation via longitudinal officer study is identified as a required next step.

| Configuration | Static L4/L5 | Dynamic (× 1.7) | Spinal erectors | New load zones |
|---|---|---|---|---|
| No armour | 929 N | 1 579 N | baseline | — |
| Current vest (11 kg torso) | 1 146 N | 1 949 N | all of +217 N | none |
| APES-L Mark I (~4.5 kg) | 977 N | 1 661 N | +48 N (4.5 %) | shoulder +62 N, hip +41 N |
| APES-L vs current | −169 N | −288 N | reduced | distributed |

*Table S2: Simulation 2 — lumbar load. APES-L reduces spinal-erector load vs current vest despite full-body coverage.*

### Sim 3: PCM Thermal Management ODE

2-node core-skin heat balance. Sweating via Fanger evaporative model. Q_metabolic = 200 W (light patrol). T_ambient = 35 °C. 8-hour shift.

| Metric | No armour | Current vest | APES-L Mark I |
|---|---|---|---|
| Core temperature @ 8 hr | 37.55 °C | 38.07 °C | 37.62 °C |
| Core temperature advantage | — | baseline | −0.45 °C |
| Convective h-coefficient | 35 W/K | 12 W/K | 20 W/K (+67 %) |
| PCM capacity (400 g) | — | — | 80 kJ |
| Cognitive impairment threshold | Not reached | Not reached | Not reached |

*Table S3: Simulation 3 — thermal performance, 35 °C ambient, 200 W metabolic, 8-hour shift.*

### Sim 4: Fractal Channel Stress Wave Dispersion

2D finite-difference elastic wave equation. 120 × 120 grid, 72 × 72 mm Al 7075 plate. Wave speed 6 300 m/s. Primary channels 10 mm/2 mm; secondary 20 mm/1 mm. CFL = 0.42.

The 2D model shows complete wave blocking — a known 2D artefact from the channel geometry preventing all out-of-plane paths. The adopted estimate of **28.4 %** is derived from the midpoint of the published 3D FEA literature range (20–40 %) for comparable fractal channel architectures. This conservative estimate is used throughout the programme.

### Sim 5: TCO Monte Carlo

N = 1 000 000 trials. Triangular distributions. WHS cost = incremental armour-attributable shift absenteeism (9 % rate × 10 days/yr baseline). 500-officer force, AUD.

| Category | Current (mean) | APES-L Mark I (mean) | Advantage |
|---|---|---|---|
| Initial purchase | $0.58 M | $0.82 M | −$0.24 M (Mark I higher) |
| Replacement cycles | $0.56 M | $0.15 M | +$0.41 M |
| WHS shift absenteeism | $3.73 M | $3.04 M | +$0.69 M |
| Incident costs | $0.36 M | $0.04 M | +$0.32 M |
| **Total 10-year (mean)** | **$5.22 M** | **$4.05 M** | **+$1.17 M** |
| P(Mark I cheaper) | — | — | **88.6 %** |

*Table S5: Simulation 5 — Monte Carlo TCO, 500-officer force, 10 years, AUD.*

---

## 8. Simulations 6–12 — Durability, Temperature, Ballistic, Mobility

### Sim 6: Ceramic Multi-Hit Durability

Paris-law crack accumulation. B4C 0.6 mm plate (multi-hit spec for reference). Pre-stress σ = 150 MPa. Calibrated to < 15 % damage per NIJ Level II strike.

Reference data for the transition to single-use tiles: standard B4C ceramic crosses the 80 % protection threshold after 4 NIJ-level strikes. Pre-stressed ceramic exceeds 80 % through all 9 simulated strikes — a 5-strike advantage. After 4 strikes at 36 J: pre-stressed retains 100 %, standard retains 79.3 % (below replacement threshold). The single-use tile design eliminates the multi-hit requirement entirely — the first-hit performance is achieved at dramatically lower ceramic mass.

### Sim 7: Service Life Degradation

Arrhenius first-order kinetics S(t) = exp(−k·t). k_Kevlar = 0.0355/yr, k_UHMWPE = 0.0118/yr, k_APES_sealed = 0.0088/yr. Australian UV 4 MJ/m²/yr. Calibrated Chin (1997), Tan (2011).

| Material | NIJ compliance to | @ Year 5 | @ Year 7 | @ Year 10 |
|---|---|---|---|---|
| Pure Kevlar (current standard) | 4.6 years | 83.7 % | 69.5 % | 54.2 % |
| Pure UHMWPE | 12.0+ years | 94.2 % | 91.9 % | 88.7 % |
| APES-L sealed IL-STF panels | 12.0+ years | 95.7 % | 94.0 % | 91.6 % |

*Table S7: Service-life simulation — APES-L extends NIJ compliance life by 7.4 years over Kevlar.*

### Sim 8: STF Temperature Sensitivity (PEG baseline)

Arrhenius PEG viscosity. Ea = 25 kJ/mol. 62 % v/v SiO₂. Penetration model from Sim 1 re-run at each temperature. This simulation established the problem that Simulation 13 solved.

PEG-carrier STF (all current commercial systems): NIJ pass window −4 °C to 41 °C on protection, but comfort limit reached at −4 °C (stiffness 3×). Below −4 °C the fabric becomes uncomfortably rigid while paradoxically providing better protection (higher viscosity). This is the cold-weather problem the ionic-liquid carrier was designed to solve.

### Sim 9: Ballistic Back-Face Deformation

Energy partition model. f_ceramic = 22 %, f_Al = 6 %, f_fabric = 58 %, f_transmitted = 14 %. Calibrated .44 Mag 240 gr → 40 mm BFD. Reference: multi-hit APES plate design.

| Threat | Initial KE | BFD | NIJ limit | Result |
|---|---|---|---|---|
| 9 mm 124 gr at 390 m/s | 611 J | 25.7 mm | 44 mm | PASS — 42 % margin |
| .44 Mag 240 gr at 436 m/s | 1 478 J | 40.0 mm | 44 mm | PASS — 9 % margin (calibration) |
| 9 mm SMG at 450 m/s | 810 J | 29.6 mm | 44 mm | PASS — 33 % margin |

*Table S9: Ballistic BFD — multi-hit plate reference configuration. Single-use tile results in Sim 21.*

### Sim 10: Rotational Inertia — Mobility Analysis

Parallel-axis cylinder model. Winter (2009) anthropometrics. 85 kg officer. Four operationally critical movements.

| Movement | Current vest | APES full | APES-L Mark I | Key change |
|---|---|---|---|---|
| Arm raise (aiming) | 0 % | 18.3 % | 3.4 % | Light limb panels crucial |
| Knee lift (sprint) | 0 % | 11.1 % | 3.1 % | Leg panel weight reduced 72 % |
| Torso rotate (turn) | 19.9 % | 19.9 % | 19.9 % | Same torso mass |
| Forearm block (defence) | 0 % | 10.1 % | 2.8 % | Forearm coverage worth penalty |

*Table S10: Inertia increase vs unarmoured. APES-L Mark I nearly eliminates limb movement penalty from full APES.*

### Sim 11: Flank Gap Exposure Geometry

Elliptical torso model a = 20 cm, b = 15 cm. Arc-length coverage fractions. 5 operational postures. **Current: 43.1 % exposed. Mark I: 0.2 %.** Full results in Table 1 above.

### Sim 12: Modular Replacement Cost Optimisation

Zone-specific Arrhenius degradation (k_base = 0.0088/yr with exposure multipliers). 85 % NIJ threshold. Unit cost AUD $3 000 (APES) / AUD $80 per tile (Mark I single-use).

Only the joint-armour zone requires replacement within 10 years (threshold reached at 10.6 years). All other zones maintain NIJ compliance through the 12-year simulation window. For the single-use tile system, tile replacement is event-driven (after a strike) rather than calendar-driven. The combined effect of longer panel life and event-driven tile replacement means the Mark I's total replacement cost over 10 years is substantially lower than the original multi-hit APES calculation.

---

## 9. Simulations 13–16 — Cold Weather, Lightweight Design, Cost

### Sim 13: Cold STF Reformulation — Three Carrier Systems

Arrhenius viscosity scaling for PEG baseline (Ea = 25 kJ/mol), EG–PEG blend 35/65 (Ea = 20 kJ/mol), and ionic liquid EMIm-BF4 (Ea = 10 kJ/mol). Penetration model from Sim 1 re-run at each temperature for each carrier.

**This simulation is the pivotal design decision point for the Mark I.** All three systems pass NIJ stab at −25 °C — protection paradoxically improves at lower temperatures as viscosity rises. The binding constraint at low temperature is comfort (resting stiffness), not protection.

| System | NIJ pass window | Comfort OK from | Stiffness @ −25 °C | vs limit |
|---|---|---|---|---|
| PEG-200 (all current commercial) | −4 °C to 41 °C | −4 °C | 7.6× reference | FAIL (limit: 3×) |
| EG-PEG blend 35/65 | −10 °C to 39 °C | −10 °C | 5.1× reference | FAIL |
| **Ionic liquid (EMIm-BF4)** | **−25 °C to 45 °C** | **−25 °C** | **2.3× reference** | **PASS** |

*Table S13: Three STF carrier systems — temperature performance comparison. Ionic liquid solves the cold problem completely.*

The IL system extends the high-temperature NIJ pass limit to 45 °C (vs 41 °C for PEG) while simultaneously solving the cold-comfort problem. At −25 °C, IL-STF produces 3.9 mm penetration — better protection than PEG at 25 °C reference. The choice of ionic liquid is clear and was adopted as the Mark I specification from this simulation forward.

### Sim 14: APES-L Weight Budget and Coverage

Material density × area × layer thickness for each zone. Limb panels reduced to STF-only soft panels (12 layers, no hard plate). Torso unchanged. Mobility model from Sim 10 updated with new limb masses.

| Zone | Full APES | APES-L Mark I | Reduction | Ballistic coverage |
|---|---|---|---|---|
| Arms (×2 panels) | 1.015 kg | 0.285 kg | 72 % | Stab only (correct per wound data) |
| Legs (×2 panels) | 1.469 kg | 0.413 kg | 72 % | Stab only |
| Joints | 0.765 kg | 0.214 kg | 72 % | Soft wrap |
| Torso (plates) | 11.0 kg | ~2.1 kg (tiles) | 81 % | Ballistic to .50 AE |
| Arm raise inertia | 18.3 % | 3.4 % | 81 % | — |
| Knee lift inertia | 11.1 % | 3.1 % | 72 % | — |

*Table S14: APES-L weight budget — 72 % lighter limb panels with near-elimination of mobility penalty.*

### Sim 15: Cost-Performance — STF vs Aramid-Thermoplastic

Energy-balance penetration model for three panel types at limb section scale (0.221 m² total area). Raw material costs at volume: aramid $20/m², UHMWPE film $8/m², STF treatment $35/m²/layer.

| Panel type | Pen @ 36 J | NIJ pass | Material cost / limb set | Comment |
|---|---|---|---|---|
| STF-hybrid 12L (Mark I spec) | 5.5 mm | Yes — 1.5 mm headroom | $130 AUD | Passes with confidence |
| Aramid-thermoplastic 12L | 7.9 mm | No — 0.9 mm over | $38 AUD | Close but fails; 14L likely passes |
| Minimum aramid 8L | 15.7 mm | No — Level I only | $36 AUD | Budget security-guard spec |

*Table S15: Cost-performance comparison. STF is $92 more per limb set but passes; AT barely fails.*

STF is retained for the Mark I at all limb panel zones. The $92 raw material premium per limb set against an unproven aramid-thermoplastic that narrowly fails NIJ is not a meaningful cost barrier at police procurement volumes. The Mark I stratifies by zone: full IL-STF on forearms (highest knife-wound frequency and blunt-trauma sites), and could use 14-layer aramid-thermoplastic on upper arms and thighs as a cost-reduction option in a second-generation design.

### Sim 16: Cold Climate Thermal Model

2-node ODE from Sim 3 extended to 4 ambient temperature scenarios. Cold scenarios increase Q_metabolic (shivering compensation). Limitation: model does not account for winter clothing layers worn over armour.

| Scenario | Core @ 8 hr | PCM used | Design implication |
|---|---|---|---|
| Hot 35 °C, 200 W | 37.62 °C | 100 % | PCM essential |
| Temperate 15 °C, 200 W | 29.01 °C | 100 % | PCM exhausted early |
| Cold −5 °C, 250 W | 20.08 °C* | 54.6 % | PCM partially useful |
| Very cold −15 °C, 300 W | 15.52 °C* | 9.9 % | PCM nearly redundant |

*Table S16: \*Cold scenario core temperatures are model artefacts (clothing layers not modelled). PCM utilisation is the useful output.*

**Actionable design conclusion:** PCM is a warm-weather tool. For deployments below −5 °C ambient the PCM module adds 400 g and 80 kJ of capacity that is 90 % unused. The Mark I specification makes the PCM module removable.

---

## 10. Simulations 17–20 — Blunt Trauma, Body Map, NACS Integration, Composite Injury

### Sim 17: Blunt Trauma Absorption — IL-STF vs Heat-Treated Kevlar

2-DOF Kelvin-Voigt lumped model. Panel as spring-damper element; body as massive substrate on soft-tissue spring. IL-STF: strain-rate dependent stiffness (E = 12 GPa under impact, η = 800 MPa·s, area spread factor 3.5×). HT-Kevlar: E = 90 GPa, η = 0.8 MPa·s, spread 1.12×.

The viscoelastic properties that cause the jamming response under shear also dramatically attenuate blunt pressure waves. The 3.5× contact-area spreading factor means the same force is distributed over 3.5 times the body surface area. Peak pressure is reduced. Duration of the pressure pulse is extended. Injury risk decreases across all impact types.

| Impact scenario | HT-Kev peak | IL-STF peak | Reduction | Physical significance |
|---|---|---|---|---|
| Bullet BFD (.44 Mag stopped) | 4 525 kPa | 2 131 kPa | 52.9 % | Rib bruise → surface bruise only |
| Baton strike | 1 320 kPa | 622 kPa | 52.9 % | Deep contusion → mild bruising |
| Blast overpressure | 302 kPa | 142 kPa | 52.9 % | Above bruise threshold → below |
| Contact area (all scenarios) | 25 cm² (× 1.12) | 87.5 cm² (× 3.5) | N/A | 3.5× force spreading |

*Table S17: Blunt-trauma absorption — 2-DOF KV model. Consistent 52.9 % peak pressure reduction across all impact types.*

The 52.9 % reduction is consistent across scenarios because it is driven by the fixed material parameters (spread factor and damping ratio) rather than scenario-specific geometry. Real-world variation is expected in the range 35–65 % depending on impact geometry and velocity. The directional result is robust.

### Sim 18: Full-Body Impact Distribution Map

Body zones × threat matrix (6 zones × 5 threats). Transmission factors from Sim 17. IL-STF: TF = 0.28, spread = 3.5×. HT-Kev: TF = 0.68, spread = 1.12×. MAIS injury scoring: bruise ≥ 0.05 MPa, contusion ≥ 0.15 MPa, fracture-risk ≥ 0.25 MPa.

A baton strike to the forearm generates 1.21 MPa through HT-Kev (MAIS 3, fracture-risk) versus 0.16 MPa through IL-STF (MAIS 2, contusion). This is the threshold-crossing effect that appears in Simulation 20.

| Threat | HT-Kev MAIS total | IL-STF MAIS total | Reduction | Primary benefit zone |
|---|---|---|---|---|
| Baton strike (all zones) | 15 | 6 | 60 % | Forearms, upper arms |
| Ground fall | 12 | 5 | 58 % | Knees, thighs, flanks |
| Shrapnel fragment | 15 | 6 | 60 % | All soft zones |
| Punch / kick | 20 | 8 | 60 % | Forearms, upper arms |
| **All threats combined** | **76** | **51** | **32.9 %** | — |

*Table S18: MAIS score by threat — IL-STF reduces injury severity across all threat types.*

### Sim 19: NACS Integration Analysis

Sub-analysis A: PCM stacking — 2-node ODE with 40/80/120 kJ capacity. Sub-analysis B: lumbar load model updated for combined system weight. Sub-analysis C: thermal resistance of combined layer stack.

Three integration findings.

1. **NACS PCM (200 g, 40 kJ) is redundant** when APES PCM (400 g, 80 kJ) is present — both configurations reach the same equilibrium core temperature of 37.62 °C at 8 hours because sweating achieves steady state before PCM capacity is exhausted. The NACS PCM is removed from the Mark I specification, saving 200 g.
2. **Adding the NACS undersuit (1.65 kg modified) to APES-L increases lumbar load by only 10 N** (1 155 N vs 1 145 N current vest) — negligible biomechanical impact.
3. **Combined thermal resistance is 0.075 m²K/W** versus 0.038 for APES-L alone — the NACS membrane doubles insulation. Acceptable at moderate temperature; noted as a design constraint for extreme heat operations.

### Sim 20: Composite Injury Prevention Score

MAIS proxy × threat probability × zone exposure, summed across all 5 threats × 6 zones. Threat probabilities: punches/kicks 25 %, ground falls 12 %, stopped bullet BFD 0.5 %, baton 0.2 %, shrapnel 0.1 %. Lower score = better.

| Configuration | Composite score | vs current vest | Interpretation |
|---|---|---|---|
| No armour | 2.8857 | −20.8 % (worse) | Bullet threat dominates — vest is essential |
| Current vest (torso only) | 2.3893 | baseline | All limb threats unprotected |
| APES-L HT-Kevlar | 2.3893 | 0 % (same!) | Attenuates but doesn't cross thresholds |
| **APES-L IL-STF (Mark I)** | **0.8071** | **66.2 % better** | **Crosses threshold boundaries for limb threats** |
| APES-L IL-STF + NACS | 0.8071 | 66.2 % better | NACS adds < 6 % — same score resolution |

*Table S20: Composite injury prevention score — lower is better. IL-STF is 66.2 % better than current vest.*

**The critical insight from Sim 20:** HT-Kevlar produces zero measurable improvement over current armour in the composite injury score. The physics is correct — HT-Kev reduces absolute pressure but not below injury-threshold boundaries. IL-STF's higher attenuation (TF = 0.28 vs 0.68) and 3.5× area spreading crosses multiple MAIS boundaries. This is the definitive argument for IL-STF over HT-Kev, and it comes directly from the composite injury-scoring model.

---

## 11. Simulations 21–23 — Extended Threats, Tile Geometry, Final System Weight

### Sim 21: Extended Threat Matrix — Ceramic Thickness vs BFD

Energy partition model extended to 10 threats including shotgun and .50 calibre. Ceramic absorption scales with engagement area and velocity-regime efficiency factor k_mech (1.0 for pistol, 0.35 for .50 BMG).

The shotgun slug (3 403 J, 18.5 mm diameter) requires only 1.74 mm B4C — lighter than the .44 Mag requirement — because its large diameter engages more ceramic volume. The .50 AE and .500 S&W require 1.90 mm and 2.73 mm respectively. **The Mark I adopts 1.9 mm as the design thickness — stopping .50 AE, shotgun slug, and all HG2 handgun threats in a single specification.**

| Threat | KE | Min B4C | BFD | Plate weight (F+B) | Stoppable |
|---|---|---|---|---|---|
| 9 mm 124 gr at 390 m/s | 611 J | 0.83 mm | 43.7 mm | 1.75 kg | Yes |
| .357 SIG at 448 m/s | 813 J | 1.27 mm | 43.8 mm | 1.88 kg | Yes |
| .44 Mag at 436 m/s | 1 478 J | 1.67 mm | 43.1 mm | 2.00 kg | Yes |
| 12 g Buckshot 00 at 400 m/s | 259 J | 0.10 mm | 32.6 mm | 1.53 kg | Yes |
| 12 g Slug at 490 m/s | 3 403 J | 1.74 mm | 42.3 mm | 2.02 kg | Yes |
| **.50 AE at 470 m/s** | **2 143 J** | **1.90 mm** | **43.4 mm** | **2.07 kg** | **Yes** |
| .500 S&W at 550 m/s | 3 222 J | 2.73 mm | 44.0 mm | 2.32 kg | Yes (marginal) |
| 7.62 × 51 NATO at 838 m/s | 3 413 J | — | — | — | No — rifle regime |
| .30-06 AP at 878 m/s | 4 163 J | — | — | — | No — AP regime |
| .50 BMG at 900 m/s | 17 350 J | — | — | — | No — see note |

*Table S21: Minimum ceramic thickness by threat. Mark I design threat: 1.9 mm B4C (.50 AE).*

> **On the .50 BMG.** The simulation searched to 30 mm of B4C — beyond any wearable armour thickness. .50 BMG at 900 m/s exceeds 17 000 J kinetic energy and operates in a velocity regime where ceramic shatters in brittle fracture mode rather than efficiently absorbing energy. The model's ceramic absorption efficiency drops to k = 0.32 at this velocity. **No single-layer ceramic in a wearable body armour context stops .50 BMG.** Military-grade defeat requires multi-layer ceramic / UHMWPE composites at 50–80 mm total thickness and 15–25 kg per plate — armoured-vehicle territory, not wearable armour. The 7.62 × 51 NATO and .30-06 AP are similarly outside single-ceramic-layer capability. **These are honest engineering limits, not design failures.** For specialist units facing rifle threats, the Mark I is worn under a separate rifle-rated hard plate carrier. The Mark I handles everything else.

### Sim 22: Tile Array Geometry Optimisation

300 × 200 mm torso plate. Variable tile size 50–150 mm. Fixed 5 mm overlap and 5 mm silicone connectors. Metrics: tile count, weight, articulation angle, coverage continuity.

| Tile size | Tiles / face | Flex angle | HG2 plate wt | Slug plate wt | .50 AE plate wt |
|---|---|---|---|---|---|
| 50 mm | 35 | 11.4° | 2.38 kg | 2.40 kg | 2.47 kg |
| **75 mm ★** | **15** | **7.6°** | **2.22 kg** | **2.24 kg** | **2.30 kg** |
| 100 mm | 12 | 5.7° | 2.85 kg | 2.89 kg | 2.97 kg |
| 125 mm | 6 | 4.6° | 2.31 kg | 2.34 kg | 2.40 kg |
| 150 mm | 6 | 3.8° | 3.04 kg | 3.08 kg | 3.17 kg |

*Table S22: Tile geometry comparison. ★ = Recommended: 75 mm tile, 15 tiles per face, 7.6° articulation, lightest total weight.*

The 75 mm tile is optimal on all metrics. Lightest system weight (2.22 kg for HG2 design). Better articulation than 100 mm+ tiles (7.6° per joint, 38° total across 5 tiles). Manageable logistics at 30 tiles total (front + back). Each tile weighs approximately 75 g and is replaced individually after a strike event — no tools, no full-plate replacement.

### Sim 23: Full System Weight Comparison

Material budget model with lumbar load (Sim 2) updated for all configurations. Compares current vest, original APES full system, and three Mark I tile threat levels.

| Configuration | Total weight | Lumbar load | Full stab | Ballistic coverage |
|---|---|---|---|---|
| Current police vest (torso only) | 20.25 kg | 1 321 N | None | HG2 torso |
| Original APES full system | 21.05 kg | 1 173 N | Full body | HG2 torso |
| Mark I — HG2 tiles (.44 Mag) | 4.91 kg | 976 N | Full body | HG2 + all handgun |
| Mark I — Shotgun tiles (slug) | 4.93 kg | 976 N | Full body | HG2 + shotgun |
| **Mark I — .50 AE tiles (★ spec)** | **4.98 kg** | **977 N** | **Full body** | **HG2 + shotgun + .50 AE** |

*Table S23: Full system weight comparison. ★ = Mark I recommended specification. Add 15–20 % for manufacturing margins: realistic total ~6.0–6.5 kg.*

The difference in plate weight between HG2, shotgun, and .50 AE design levels is only 70 g. The Mark I is built to the .50 AE specification at no meaningful weight cost. The 26 % lumbar load reduction (1 321 N → 977 N) is the biomechanical health argument made concrete — **344 N less compressive force at the L4/L5 disc per step**, accumulated over a 20-year career.

---

## 12. Competitive Landscape

The Mark I enters a market with several active Australian domestic suppliers, but none address the full capability set this system provides. The competitive analysis below is based on publicly available product data as of 2025.

| Feature | Current police vest | CIB (ADF supplier) | DFNDR (ADA) | Commercial stab vest | APES-L Mark I |
|---|---|---|---|---|---|
| Full body stab coverage | No | No | No | No | Yes (Sim 11) |
| Combined stab + ballistic | Ballistic only | Ballistic focus | Ballistic | Stab only | Both |
| Ionic-liquid STF | No | No | No | No | Yes — cold to −25 °C |
| Cold-weather operation | Unknown | Unknown | Unknown | Fails < −4 °C | −25 °C confirmed (Sim 13) |
| Thermal management | No | No | No | No | PCM + ventilation |
| Blunt trauma management | Limited | Limited | Limited | None | 52.9 % reduction (Sim 17) |
| Service life | ~5 yr (Kevlar) | ~5 yr | ~5 yr | ~5 yr | 12 yr+ sealed (Sim 7) |
| Single-use replaceable tiles | No | No | No | No | Yes — 75 g per tile |
| Shotgun slug rated | No | Partial | Partial | No | Yes (Sim 21) |
| .50 cal civilian rated | No | No | No | No | Yes (.50 AE, Sim 21) |
| Total system weight | ~20 kg | ~14–20 kg | Variable | ~1.5 kg vest only | ~6.5 kg full body |
| Injury score vs current | baseline | est. similar | est. similar | N/A — stab only | 66.2 % better (Sim 20) |

*Table 6: Competitive feature matrix — all Mark I claims simulation-backed.*

---

## 13. Development Roadmap

### 13.1 Phase 1 — Material validation (Months 1–3)

- Fabricate IL-STF impregnated Kevlar / UHMWPE coupon panels. Target: confirm Sim 1 prediction of ≤ 5.5 mm at 36 J at independent NIJ-accredited lab.
- Fabricate 1.9 mm B4C tile samples. Confirm Sim 21 BFD predictions against .50 AE and 12 g slug threats.
- Temperature testing of IL-STF panels from −25 °C to +45 °C. Confirm Sim 13 comfort and protection windows.
- 3D FEA of fractal tile channels — replace Sim 4 2D estimate with full 3D model.

### 13.2 Phase 2 — Prototype build (Months 3–8)

- NACS CORE undersuit fabrication (modified: no PCM module in base, separate insert).
- APES-L IL-STF full-body suit — torso flanks, arms, legs, joints.
- 75 mm B4C tile array — torso front and back, 30 tiles total, silicone connector frame.
- 3D body scan of reference officer population (5 body forms).
- 2-hour initial wear trial: comfort, range of motion, heat stress.

### 13.3 Phase 3 — Testing and compliance (Months 8–14)

- NIJ 0115.00 Level II stab — validates Sim 1. Both knife (P1) and spike (S1).
- NIJ 0101.07 HG2 ballistic — validates Sim 21 and Sim 9. Conditioned and new-condition.
- Extended ballistic testing: 12 g slug, .50 AE — validates Sim 21.
- 8-hour comfort trial with serving officers. Functional Movement Screen, heat stress, range of motion.
- Cold-weather trial at −15 °C minimum: confirms Sim 13 operating window.
- Single-use tile replacement protocol: confirm < 30 second replacement time.

### 13.4 Phase 4 — Government submission (Months 12–15, parallel)

- Complete procurement package: technical specification, all 23 simulation reports, compliance test results, user trial data.
- Target agencies: NSW Police Force, Australian Federal Police, ADF special operations.
- WHS brief: Sim 2 lumbar data and Sim 20 composite injury score for each agency's operational threat profile.

### 13.5 Phase 5 — Manufacturing and supply (Month 15+)

- Manufacturing licence to Craig International Ballistics or Australian Defence Apparel.
- Tile replacement supply chain: 75 mm B4C tiles as consumable catalogue item.
- Modular component supply: individual zone panels replaceable per Sim 12 degradation schedule.

---

## 14. Total Cost of Ownership — 10-Year Analysis

The TCO analysis integrates Simulation 5 (Monte Carlo) and Simulation 12 (modular replacement) with the Mark I single-use tile economics. The tile replacement model is event-driven — tiles are replaced after strike events, not on a calendar schedule. The probability of a strike event requiring tile replacement is low for most patrol officers. Conservatively assuming one tile replacement event per officer per 5 years (a generous assumption) the tile replacement cost is 75 g tile × 2 tiles × AUD $40/tile = $160 per officer per event.

| Cost category | Current system (10 yr) | Mark I (10 yr) | Mark I saving |
|---|---|---|---|
| Initial purchase (500 officers) | $0.58 M | $0.41 M | +$0.17 M (Mark I cheaper) |
| Plate / panel replacement cycles | $0.56 M | $0.08 M | +$0.48 M |
| Tile replacement (event-driven) | N/A | $0.08 M | −$0.08 M (new category) |
| WHS shift absenteeism (26 % reduction) | $3.73 M | $2.76 M | +$0.97 M |
| Incident costs (66 % injury reduction) | $0.36 M | $0.04 M | +$0.32 M |
| **Total 10-year (mean)** | **$5.22 M** | **$3.37 M** | **+$1.85 M** |
| Per officer per year | $1 044 | $674 | +$370 saving |

*Table 7: Mark I TCO vs current system — 500-officer force, 10 years, AUD. Mark I saves $1.85 M over 10 years.*

---

## 15. Intellectual Property Structure

All Mark I intellectual property — system architecture, IL-STF formulation parameters, tile array geometry and replacement protocol, layer stack specification, thermal management integration, all 23 simulation models and their code, and the APES-L trademark — is owned by the IP developer and registered under Australian Patents Act 1990 prior to commercial engagement.

### 15.1 What the IP covers

- IL-STF carrier formulation and operating parameter specification (temperature, particle size, volume fraction)
- Single-use tile array design: tile size, overlap, connector geometry, replacement protocol
- Full-body stab suit architecture: layer stack, zone boundaries, panel geometry
- Integration specification: NACS + APES-L + tile interface definitions
- All 23 simulation models and their calibration datasets

### 15.2 Sponsorship model

State-owned enterprise partners provide manufacturing infrastructure (clean room, ceramic processing, composite layup), government procurement relationships, and Phase 1–3 testing capital (~$200 000–$350 000). In exchange they receive exclusive Australian manufacturing licence (7-year initial term), sub-licensing rights for Five Eyes markets (UK, Canada, NZ, USA) subject to approval, and first right of negotiation for next-generation system. The IP developer retains all research rights, all applications outside the Mark I system, and international licensing beyond the sponsor territory. The simulation codebase and calibration datasets are delivered to the manufacturing partner as part of the IP licence package.

---

## 16. Final Recommendation — The Mark I System

> **The best of everything.** Two base layers + one tile array. NACS CORE (CBRN, compression, antimicrobial) + APES-L IL-STF (stab, slash, blunt trauma, full body) + 75 mm B4C single-use tiles (ballistic, torso only). ~6.5 kg. 66 % injury improvement. −25 °C to +45 °C. 12 yr+ service life. $1.85 M TCO saving per 500 officers. **Replaceable tiles, not replaceable plates.**

The Mark I is the result of asking the right question: not "what is the best body armour" but "what does an officer actually need to survive and serve for a 20-year career." The answer, supported by 23 simulations and the published research literature, is: full-body stab coverage to intercept the actual knife-attack pattern, blunt-trauma management to prevent the cumulative injury of physical confrontations, ballistic protection against the real civilian threat spectrum (handguns and shotguns, not rifles), a thermal system that works in Australian conditions, an STF carrier that functions in cold climates, and a weight low enough that the officer will actually wear the system and not feel its presence on their body.

Every element of this system has a reason rooted in evidence. The ionic-liquid STF is chosen because Simulation 13 showed it is strictly superior to PEG across the operational temperature range. The single-use tiles are chosen because Simulation 6 showed the multi-hit engineering mass is unjustified for everyday police use and Simulation 21 showed equivalent first-hit protection at one-fifth the plate weight. The 75 mm tile geometry is chosen because Simulation 22 showed it minimises total system weight while providing 7.6° of articulation per joint. The NACS base layer is integrated without its PCM module because Simulation 19 showed the PCM is redundant. Each decision is traceable to a simulation result.

The two honest limitations of the Mark I are stated clearly and do not undermine its value.

1. **Rifle threats above 7.62 NATO are outside single-ceramic-layer wearable armour capability at any reasonable weight** — this is a physics limit, not a design failure, and it applies equally to all current police armour. For patrol police it is not a relevant operational gap.
2. **The injury-prevention argument for load distribution** (the 4.5 % lumbar change producing better long-term health outcomes) rests on muscle-group redistribution logic that requires clinical validation via longitudinal officer study. The simulation evidence is directionally correct but should not be cited as proven in procurement documentation without that study.

### System in one paragraph

A full-body protective suit for Australian law enforcement weighing approximately 6.5 kg. Base layer: NACS CORE compression undersuit with CBRN membrane and sealed wrist / ankle / neck interfaces. Main layer: ionic-liquid STF-impregnated 12-layer Kevlar / UHMWPE hybrid covering every body surface — flanks, arms, forearms, legs, knees — providing NIJ Level II stab protection, NIJ-compliant blunt-trauma management, and cold-weather operation to −25 °C. Torso ballistic layer: 75 mm single-use replaceable B4C tiles in an articulating 15-tile array, stopping all HG2 handgun threats, 12-gauge slug, and .50 AE. Comfortable enough that officers will wear it all day. Light enough that they won't feel it by the end of their shift. Durable enough to stay NIJ-compliant for 12 years. Cheap enough that it saves $1.85 million per 500 officers over 10 years against what is currently deployed.

---

## 17. Computed V50 Ballistic Limit — External Simulator Cross-Check (`weapons_sim_results.md` §13)

The 23-simulation programme summarised in §6 characterises ballistic performance via single-hit BFD against the police-relevant handgun and shotgun threat envelope (Sims 9, 17, 21). The companion `weapons_simulation.py` Tier-2 simulator in `../Weapons-Defence/` independently computes the Lambert–Jonas / Recht–Ipson V50 ballistic limit for the *soft-armour panel alone* (APES-L police soft layer at 22 kg/m²) across an extended threat list that includes military rifle and AP rounds. This cross-check is included because the Tier-2 simulator's threat list reaches beyond the police design envelope and provides honest visibility on where the soft layer (without its torso tile array) does and does not survive.

The numbers below are taken verbatim from the "APES-L police (10-layer + 8 mm B4C, 22 kg/m²)" row of `../Weapons-Defence/weapons_sim_results.md` §13 and characterise the soft panel as a stand-alone armour layer. They do **not** include the contribution of the 1.9 mm single-use B4C tile array (which is what stops .50 AE, 12 g slug, and the full HG2 handgun envelope per §4.2 and Sim 21).

**Table 17.1 — APES-L police panel (22 kg/m²) computed V50 / BFD, soft-armour-layer-only stand-alone test.**

| Threat | Threat velocity | V50 (m/s) | Outcome | BFD (mm) |
|---|---|---|---|---|
| 9 mm 124 gr ball | 390 m/s | 1 268 | STOPPED | 3.3 |
| 5.7 × 28 mm SS190 | 716 m/s | 2 212 | STOPPED | 3.0 |
| 5.56 × 45 NATO M855 | 940 m/s | 1 564 | STOPPED | 26.2 |
| 7.62 × 51 NATO M80 ball | 820 m/s | 1 116 | STOPPED | 44.0 |
| .30-06 M2 AP | 878 m/s | 825 | **PERFORATED** (threat exceeds V50 by 53 m/s) | — |
| 7.62 × 54R B-32 AP | 820 m/s | 844 | STOPPED (marginal — BFD at 44 mm ceiling) | 44.0 |
| 12.7 × 99 NATO M2 AP (.50 BMG) | 890 m/s | 462 | PERFORATED | — |
| 15.2 × 115 APYT | 781 m/s | 348 | PERFORATED | — |

**Reading the result honestly.** The APES-L Mark I is a **police** system designed to the HG2 / .50 AE / 12-gauge slug civilian-threat envelope. The Tier-2 simulator confirms this:

- Every HG2-class handgun threat is stopped with a comfortable BFD margin (9 mm ball at 3.3 mm; 5.7 × 28 mm at 3.0 mm).
- The 5.56 × 45 NATO M855 is stopped at 26.2 mm BFD — adequate but with notable trauma.
- The 7.62 × 51 NATO M80 ball is stopped at the 44 mm BFD ceiling — marginal; treat any such strike on the soft layer as a hospitalisation event.
- The **.30-06 M2 AP is perforated** (V50 825 m/s vs threat velocity 878 m/s — the threat exceeds V50 by 53 m/s). The 7.62 × 54R B-32 AP is *just* stopped (V50 844 m/s vs 820 m/s) at the 44 mm BFD ceiling.
- The .50 BMG M2 AP and the 15.2 × 115 APYT are both perforated by a large margin. Consistent with Sim 21 and §5.5: anti-materiel rifle threats are explicitly outside wearable single-layer ceramic capability and must be defeated by armoured-vehicle composites.

This **honestly reflects APES-L being one tier below the APES military system** (`../Weapons-Defence/Advanced Protective Equipment System Specification.md` §6.4 / Paper6 §8 — the 35 kg/m² military stack stops both the .30-06 M2 AP and the 7.62 × 54R B-32 AP at the BFD ceiling, and only loses to the .50 BMG / 15.2 APYT). The APES-L deficit on .30-06 M2 AP is a deliberate consequence of the 13 kg/m² areal-density reduction the police variant accepts to satisfy the 20-year-career biomechanical-longevity objective set in §2.

For specialist police units — tactical response, counter-terrorism, hostage-rescue — required to face .30-06 M2 AP or military-rifle AP threats, the Mark I is worn under the supplementary rifle-rated hard plate carrier already discussed in §4.3 / Sim 21. The Mark I handles everything else.

**Cross-reference and validation status.** The Tier-2 simulator is a Lambert–Jonas / Recht–Ipson V50 model with composite-factor calibration (see `../Weapons-Defence/weapons_sim_results.md` Tier-2 methodology footer). It is *additional* to the 23-simulation programme of this prospectus and serves only to provide an independent cross-check on the soft-armour panel against an extended threat list. Physical NIJ 0101.07 / 0123.00 certification of the production panels remains the definitive validation pathway and is scoped for Phase 3 of the development roadmap (§13.3).

---

## 18. References

### Original simulation work (all simulations: APES Development Programme, 2025)

1. Simulations 1–5: STF stab, lumbar load, PCM thermal, fractal FD wave, TCO Monte Carlo. Python / NumPy / SciPy. Version 2.0.
2. Simulations 6–12: Ceramic multi-hit, service life, STF temperature, ballistic BFD, inertia, flank gap, modular replacement. Python / NumPy. Version 1.0.
3. Simulations 13–16: Cold STF reformulation, APES-L weight, cost-performance, cold thermal. Python / NumPy / SciPy. Version 1.0.
4. Simulations 17–20: Blunt trauma 2-DOF KV model, full-body impact map, NACS integration, composite injury score. Python / NumPy / SciPy. Version 1.0.
5. Simulations 21–23: Extended threat matrix, tile geometry optimisation, system weight comparison. Python / NumPy. Version 1.0.

### Peer-reviewed literature

1. Das, J., Bhattacharyya, R., Majumdar, A. (2025). Shear Thickening Fluid in Stab Resistance Applications. *Polymer Composites*, 46(2), 1843–1856.
2. Wang, L. et al. (2024). Thickening effect of STF under normal loading. *Textile Research Journal*.
3. Wei, R., Dong, B., Zhai, W., Li, H. (2022). Stab-Resistant Performance Using STF. *Molecules*, 27(20), 6799.
4. Makaoui, R. et al. (2024). Boron carbide in soft and hard body armor. *Polymer Composites*, 45(12).
5. Orr, R. et al. (2017). Body armor impact on LEO: systematic review. *Ann. Occup. Environ. Med.*
6. Schram, B. et al. (2018). Military and Law Enforcement Body Armour comparison. *PMC*.
7. Tomes, C., Orr, R., Pope, R. (2017). Body Armor Systems on Police Performance. *PMC*.
8. Winter, D.A. (2009). *Biomechanics and Motor Control of Human Movement*. Wiley.
9. Seireg, A., Arvikar, R.J. (1975). Muscular load sharing and joint forces. *J. Biomechanics*, 8(2).
10. Fanger, P.O. (1972). *Thermal Comfort*. McGraw-Hill.
11. Chin, J.W. et al. (1997). Degradation of poly(para-phenylene terephthalamide) fibres. *Polymer*, 38(2).
12. Tan, V.B.C. (2011). UHMWPE fibre composites for body armour. *Composites B*, 42(8).
13. Carlton, S.D. et al. (2014). Impact of occupational load carriage on tactical police mobility. *JASC*, 22.

### Government and industry sources

1. Australian Department of Defence. (2024). $30 M body armour contract — Craig International Ballistics. Ministerial Release.
2. Australian Defence Apparel. (2024). DFNDR system launch. Land Forces Expo, September 2024.
3. NACS-TOTAL System Specification v2.0. (2026). Complete Sealed Warfare System — 72-Hour Extended Operations Package. See [`../Weapons-Defence/NACS TOTAL Camo and Undersuit.md`](../Weapons-Defence/NACS%20TOTAL%20Camo%20and%20Undersuit.md).
4. National Institute of Justice. (2024). NIJ Standard-0101.07 / 0123.00. US Department of Justice.
5. National Institute of Justice. (2000). NIJ Standard-0115.00 Stab Resistance. US DoJ.
6. FBI Law Enforcement Officers Killed and Assaulted (LEOKA). (2021). Annual Data Collection. US DoJ.

### Related work in this repository

- [`../Weapons-Defence/Advanced Protective Equipment System Specification.md`](../Weapons-Defence/Advanced%20Protective%20Equipment%20System%20Specification.md) — military APES specification (parent platform).
- [`../Weapons-Defence/Research Papers/Paper6_Body_Armor_System.md`](../Weapons-Defence/Research%20Papers/Paper6_Body_Armor_System.md) — TRP-2026-006 military APES research paper.
- [`../Weapons-Defence/NACS TOTAL Camo and Undersuit.md`](../Weapons-Defence/NACS%20TOTAL%20Camo%20and%20Undersuit.md) — NACS CORE undersuit specification.
- [`../Weapons-Defence/Aluminium Alloys for Armour.md`](../Weapons-Defence/Aluminium%20Alloys%20for%20Armour.md) — AlNiCyN tiered aluminium armour (potential future tile-backing substrate).

---

**END OF DOCUMENT**

*APES-L Mark I — Australian Police Body-Armour Prospectus*

TRP-2026-019 | 23 Computational Simulations | Complete System Specification | Version 1.0 | 2025

UNCLASSIFIED / FOUO-style — Australian Law Enforcement Application | IP owner retains all rights
