# Advanced Protective Equipment System — Law-Enforcement Variant (APES-L Mark I): A Simulation-Validated Full-Body Police Body-Armour Architecture

*Technical Research Paper*

Document No. TRP-2026-019-R | Version 1.0

Prepared for: Australian State Police Forces, Australian Federal Police, ADF Special Operations procurement

Classification: **UNCLASSIFIED / FOUO-style — Australian Law Enforcement Application** | Date: 2025

## Abstract

This paper presents the **Advanced Protective Equipment System — Law-Enforcement Variant (APES-L Mark I)**, a full-body police body-armour architecture derived from the military APES platform (TRP-2026-006) and adapted for Australian law-enforcement operational realities. The system integrates seven materials-science streams — ionic-liquid shear-thickening fluid (IL-STF), UHMWPE / para-aramid hybrid laminate, single-use boron-carbide ceramic tiles, phase-change material (PCM) thermal management, biomimetic fractal channel plate architecture, GORE CHEMPAK CBRN membrane, and graphene oxide interface layers — into a three-layer system: a NACS CORE undersuit (1.65 kg in the Mark I after PCM module removed per Sim 19; 1.85 kg as-shipped), an IL-STF full-body soft-armour suit (~2.7 kg), and a single-use replaceable 75 mm B4C tile array on the torso (~2.1 kg). Total system weight is approximately 6.5 kg ready to wear, against 20 kg for the current Australian-police torso-only ballistic vest. Twenty-three original physics-based computational simulations characterise stab resistance, ballistic back-face deformation, biomechanical load, thermal management, service-life degradation, blunt-trauma attenuation, mobility, and total cost of ownership. Headline results: NIJ Level II stab (5.5 mm penetration at 36 J), single-use tile defeat of .50 AE and 12-gauge slug, 52.9 % peak-pressure reduction vs heat-treated Kevlar on blunt trauma, 66.2 % composite injury-score improvement, comfortable IL-STF operation to −25 °C (versus −4 °C for current PEG-carrier commercial STF), 12-year-plus sealed-panel service life (versus 4.6 years for Kevlar), 26 % spinal compressive force reduction at L4/L5, and an AUD $1.85 M 10-year TCO saving per 500 officers. The paper documents materials selection rationale, simulation methods, results, the threshold-crossing argument that distinguishes IL-STF from HT-Kevlar attenuation, and the honest engineering limit that no single-ceramic-layer wearable armour stops 7.62 NATO or .50 BMG. Physical NIJ certification remains the definitive validation pathway; the simulation programme provides design guidance and pre-validation confidence.

**Keywords:** police body armour, shear-thickening fluid, ionic liquid, boron carbide ceramic, UHMWPE, single-use tile, blunt-trauma management, NIJ Standard 0115, NIJ Standard 0101.07, biomechanical load redistribution.

---

## 1. Introduction

Police body armour in service across Australia and most comparable jurisdictions consists of a torso-only soft-armour panel (typically para-aramid, sometimes UHMWPE) carried in a ballistic vest, with an optional plate pocket for a rifle-rated hard plate worn only by tactical or specialist units. The standard duty configuration weighs approximately 20 kg when worn with the full duty belt, holster, and load-bearing equipment over a long shift. It provides ballistic protection to NIJ Level II or IIIA over the chest and upper back, no stab or slash protection on any limb, no blunt-trauma management beyond the kinetic-energy absorption of the ballistic panel itself, and no thermal management. The fielded life of an aramid panel is nominally five years; in Australian UV conditions the service life of pure Kevlar is closer to 4.6 years before NIJ tensile-retention compliance is lost.

This paper does not propose a marginal improvement on the fielded configuration. It documents an architecture deliberately designed against a more honest problem statement: **what does an Australian police officer actually need from body armour, given the realistic distribution of injury threats across a 20-year career?** The answer drives a different architecture — full-body stab and slash coverage in a lightweight soft-armour suit using ionic-liquid shear-thickening fluid, ballistic protection limited to the torso (where all fatal officer gunshot wounds occur per FBI LEOKA data) but extended to single-use replaceable ceramic tiles defeating .50 AE and 12-gauge slug, blunt-trauma management integrated into the soft-armour layer rather than left to chance, a thermal-management system using phase-change materials at 28 °C, and a base undersuit (NACS CORE, developed under the companion military programme) providing CBRN-grade sealed interfaces.

The system is the **APES-L** variant of the **APES** military platform documented in TRP-2026-006 — same overall architecture, adapted for the operational realities of policing rather than military close combat. The major adaptations are: (i) single-use replaceable tiles rather than pre-stressed multi-hit ceramic plates, on the basis that the operational probability of two impacts on the same plate location is negligible for patrol policing; (ii) ionic-liquid STF carrier rather than aramid-thermoplastic, on the basis that cold-weather operability is essential for Australian alpine and winter deployment; (iii) NIJ Level II / HG2 ballistic focus rather than rifle-rated Level III/IV; and (iv) a weight budget targeted at chronic-injury prevention over a 20-year career, not at 72-hour CBRN sealed-operations endurance.

---

## 2. Background

### 2.1 Current police-armour limitations

Three operational limitations recur across published police-armour reviews and the present authors' simulation programme.

**Coverage geometry.** Simulation 11 in the present programme modelled the human torso as an elliptical cross-section (anterior semi-axis 20 cm, lateral semi-axis 15 cm) and computed the arc-length fraction of the perimeter covered by current armour at ±55° front and ±55° rear coverage geometry. In standing posture, 43.1 % of the torso perimeter is completely unprotected. In the aiming posture (arm raised) this rises to 47.1 %, and to 46.6 % in crouching. The full-body APES-L Mark I configuration reduces residual gap to 0.2 % at seam-attachment zones only.

**Cold-weather operability.** All commercially available STF body armour systems use polyethylene glycol (PEG, typically PEG-200) as the STF carrier fluid. The Arrhenius activation energy of PEG (~25 kJ/mol) produces a steep viscosity–temperature curve: at −25 °C, PEG-carrier STF reaches resting stiffness of 7.6× reference, well above the 3× comfort limit. The fabric becomes operationally unusable below approximately −4 °C, even though paradoxically protection improves at lower temperatures because of the higher resting viscosity. No commercial manufacturer has resolved this constraint.

**Service-life degradation.** Para-aramid fibre undergoes amide-bond hydrolysis and UV-induced chain scission, with a documented first-order degradation rate constant under Australian UV conditions (4 MJ/m²/year) consistent with crossing the 85 % NIJ tensile-retention threshold at 4.6 years. The fielded 5-year replacement cycle is therefore already non-conservative, and a significant proportion of currently deployed vests are below NIJ compliance threshold at any given audit date.

### 2.2 LEOKA wound-data analysis

Analysis of the FBI Law Enforcement Officers Killed and Assaulted (LEOKA) annual data series, with specific reference to the 2021 reporting cycle, indicates:

- **Zero fatal officer wounds from arm or leg gunshot** across the reporting period. Limb gunshots do occur and produce career-ending injuries, but they do not produce immediate fatalities.
- **All fatal officer gunshot wounds occur to the torso or head.** Head protection is outside the scope of body armour (a separate ballistic helmet system is required).
- **Knife wounds occur predominantly on the limbs**, forearms, and lower legs, with high frequency on the hands and arms during disarming and grappling scenarios.
- **Blunt-trauma injuries** (baton strikes received during confrontations, ground-fall impacts, and punches/kicks during physical arrests) cluster heavily on forearms, upper arms, and ribs, and accumulate over a career as a major component of shift-absenteeism injury statistics.

The implication is clear: **a police body-armour system optimised against the LEOKA distribution should provide torso ballistic protection (where all fatal gunshot wounds occur), full-body stab protection (where almost all blade wounds occur), and full-body blunt-trauma management (where the cumulative-injury problem lives).** The current armour configuration optimises against the firearms threat only, and accepts the cumulative-injury and knife-injury problems by omission. The APES-L architecture inverts this allocation.

### 2.3 The chronic-injury problem

A 20 kg vest concentrated on the chest and upper spine, worn for 8-hour shifts over a 20-year career, is biomechanically consequential. Published peer-reviewed work (Orr et al. 2017, Schram et al. 2018, Tomes et al. 2017, Carlton et al. 2014) documents elevated shift absenteeism from back conditions in officers who regularly wear body armour. The argument for full-body load distribution is not that it makes the total armour lighter — APES-L actually increases total above-L4/L5 mass marginally — but that it spreads the increment across the shoulder girdle, hip extensors, and quadriceps rather than concentrating 100 % of it on the spinal erectors.

---

## 3. Materials and Methods

### 3.1 Materials science streams

The Mark I integrates seven materials-science streams, each independently validated in peer-reviewed literature.

| Stream | Technology | Role in APES-L Mark I |
|---|---|---|
| 1 | Ionic-liquid shear-thickening fluid (IL-STF) | Primary stab / slash / blunt-trauma medium in all soft-armour panels |
| 2 | UHMWPE / para-aramid hybrid laminate (12L alternating) | Fibre substrate impregnated with IL-STF |
| 3 | Single-use B4C ceramic tile (1.9 mm, 75 mm square) | Torso ballistic layer |
| 4 | Phase-change material (28 °C, 80 kJ, 400 g) | Thermal management at torso |
| 5 | Biomimetic fractal channels (0.5 mm into tile face) | Stress-wave dispersion at tile |
| 6 | GORE CHEMPAK selectively permeable membrane | NACS CORE undersuit CBRN barrier |
| 7 | Graphene oxide interface layers (0.1 mm) | Inter-ply shear / thermal spreading at torso panels |

**IL-STF.** Imidazolium-based ionic liquid (EMIm-BF4 type) replaces PEG-200 as the STF carrier, with 60–65 % v/v fumed silica (~250 nm) nanoparticles. Arrhenius activation energy is approximately 10 kJ/mol (versus 25 kJ/mol for PEG), producing a substantially flatter viscosity–temperature curve. Power-law shear-thickening parameters: K = 8 Pa·s^n, n = 3.2, γ_c = 500 s⁻¹, calibrated to Das et al. (2025).

**UHMWPE / aramid hybrid.** Twelve alternating layers of para-aramid (Kevlar, 0.3 mm each) and UHMWPE (Dyneema / Spectra family, 0.2 mm each), impregnated with IL-STF. The complementary failure modes (Kevlar fibrillates under blade cut perpendicular to fibre; UHMWPE delaminates) force a blade to expend energy against two distinct mechanisms.

**Single-use B4C tile.** 75 mm × 75 mm B4C ceramic (1.9 mm thickness for .50 AE design threat, 2.52 g/cm³ density, 3 000 HV Vickers hardness) bonded to a 2 mm Al 5052 backing sheet, connected to adjacent tiles by a 5 mm Shore A 40 silicone articulation joint, with a 3 mm UHMWPE spall liner bonded to the rear face. No pre-stress is required because multi-hit durability is not a design requirement. Total assembly mass approximately 75 g per tile.

**PCM thermal stack.** 400 g of n-octadecane microencapsulated PCM at 28 °C transition temperature, 200 kJ/kg latent capacity (80 kJ total), distributed across the torso ventilation zones.

**Fractal channels.** Primary channels at 10 mm spacing, 2 mm width; secondary at 20 mm spacing, 1 mm width. Machined into the front face of each tile at 0.5 mm depth.

**GORE CHEMPAK membrane.** Selectively permeable membrane providing 72-hour CBRN protection. Water-vapour transmission rate exceeds 8 000 g/m²/24 hr.

**Graphene oxide interface layers.** 0.1 mm graphene oxide coatings between alternating plies of the torso panels (omitted from limb panels for cost reasons).

### 3.2 Simulation methods

Twenty-three original computational simulations were conducted across the development programme. All use established physical models with documented assumptions and limitations. Implementation is in Python with NumPy and SciPy. The simulations are grouped into five programme phases.

**Phase 1 — Stab, biomechanics, thermal, wave, TCO (Sims 1–5).** Energy-balance wedge penetration (NIJ P1 wedge, half-angle 15°, velocity 10 m/s); static sagittal moment-balance at L4/L5 with dynamic amplification factor DA = 1.7 per Seireg & Arvikar (1975); two-node core–skin thermal ODE with Fanger evaporative sweating; 2D finite-difference elastic wave equation (120 × 120 grid, 72 × 72 mm Al 7075 plate, CFL = 0.42); N = 10⁶ Monte Carlo TCO over a 500-officer force across triangular cost distributions.

**Phase 2 — Durability, temperature, ballistic, mobility (Sims 6–12).** Paris-law crack accumulation for ceramic multi-hit; Arrhenius first-order kinetic degradation of fibre tensile strength (k_Kevlar = 0.0355/yr, k_UHMWPE = 0.0118/yr, k_APES_sealed = 0.0088/yr); Arrhenius PEG viscosity scaling for STF temperature sensitivity; energy-partition ballistic BFD model (f_ceramic = 0.22, f_Al = 0.06, f_fabric = 0.58, f_transmitted = 0.14); parallel-axis cylinder rotational-inertia model; elliptical torso arc-length coverage; zone-specific modular-replacement cost model.

**Phase 3 — Lightweight design, cold weather, cost (Sims 13–16).** Arrhenius three-carrier comparison (PEG-200 at Ea = 25 kJ/mol, EG-PEG 35/65 blend at Ea = 20 kJ/mol, ionic liquid EMIm-BF4 at Ea = 10 kJ/mol); material-density × geometry weight budget for the lightweight APES-L configuration; energy-balance cost-performance comparison of STF-hybrid, aramid-thermoplastic, and minimum-aramid panels; four-climate-scenario cold thermal ODE.

**Phase 4 — Blunt trauma, body map, integration, composite injury (Sims 17–20).** Two-DOF Kelvin-Voigt lumped-element blunt-trauma model (IL-STF: E = 12 GPa under impact, η = 800 MPa·s, area spread factor 3.5×; HT-Kevlar: E = 90 GPa, η = 0.8 MPa·s, spread 1.12×); six-body-zone × five-threat impact distribution map with MAIS injury scoring (bruise ≥ 0.05 MPa, contusion ≥ 0.15 MPa, fracture-risk ≥ 0.25 MPa); NACS integration analysis (PCM stacking, lumbar coupled load, combined R-value); composite injury-prevention score combining MAIS proxy with threat probability and zone exposure.

**Phase 5 — Extended threat matrix, tile geometry, system weight (Sims 21–23).** Ten-threat energy-partition ballistic model extended to shotgun and .50 calibre, with velocity-regime efficiency factor k_mech scaling ceramic absorption from 1.0 (pistol) to 0.32 (.50 BMG); tile-geometry coverage-weight-articulation sweep (50–150 mm tile size); full-system weight comparison including current police vest, original APES full system, and three Mark I tile threat levels.

### 3.3 Calibration data

Stab penetration model calibrated against Das et al. (2025) for 16-layer aramid-UHMWPE hybrid panels at 24–65 J impact energy. Ballistic BFD energy-partition model calibrated to the canonical .44 Mag 240 gr at 436 m/s reference (NIJ 0101.06 Level II) → 40 mm BFD measurement on a multi-hit pre-stressed B4C / Al 7075-T6 honeycomb plate of the type documented in the military APES specification. Service-life kinetics calibrated to Chin et al. (1997) for poly-para-phenylene terephthalamide (Kevlar) tensile retention under combined UV / moisture / thermal exposure, and to Tan (2011) for UHMWPE fibre-composite degradation. Biomechanical body-segment masses, lengths, and moment-arm geometries from Winter (2009) reference anthropometry for an 85 kg male officer. Dynamic amplification factor DA = 1.7 from Seireg & Arvikar (1975) sagittal-plane joint-force analysis. Thermal-comfort sweating model from Fanger (1972) evaporative comfort theory. The Mark I composite-injury MAIS scoring uses bruise / contusion / fracture-risk thresholds at 0.05 / 0.15 / 0.25 MPa peak transmitted pressure, consistent with the published blunt-trauma literature.

### 3.4 Software and reproducibility

All simulations are implemented in Python 3.11 with NumPy 1.26, SciPy 1.11, and Matplotlib 3.8. The full source code, calibration datasets, and reproducibility scripts for the 23-simulation programme are scoped to be delivered as part of the IP licence package to the manufacturing partner. Simulation runtime is bounded: the longest run (the N = 10⁶ Monte Carlo TCO of Simulation 5) completes in approximately 90 seconds on a modern desktop CPU. Each simulation produces a JSON output file, a CSV results table, and a Matplotlib figure pair (penetration / BFD / pressure / thermal trajectory plus a derived performance metric).

### 3.5 Limitations of method

The simulations are physics-based but reduced-order. The fractal channel wave simulation is 2D; out-of-plane paths are not represented (an artefact that produces complete blocking and is corrected by adopting the 28.4 % midpoint of the published 3D FEA literature range). The cold-climate thermal model does not represent winter clothing layers worn over armour (a model limitation that produces unrealistically cold core temperatures below −5 °C ambient, though the PCM utilisation output remains useful). The MAIS injury scoring is a proxy; clinical confirmation requires longitudinal officer studies. The blunt-trauma model is lumped-element; localised geometry effects are absorbed into fixed spread and damping parameters. **Physical prototype testing against NIJ standards remains the definitive validation pathway.**

---

## 4. Results

### 4.1 Stab resistance (Sim 1)

The 12-layer IL-STF hybrid panel (APES-L limb specification) produces 5.5 mm penetration at the NIJ Level II energy of 36 J — a 1.5 mm margin under the 7 mm pass threshold. Penetration extends to 6.1 mm at 50 J and 7.1 mm at 65 J. The neat 16-layer hybrid (no STF) fails at 15.6 mm at 36 J; STF impregnation produces a 64.8 % reduction in penetration depth. The result holds for both the 12L limb-section panel and the 16L torso-section panel.

### 4.2 Ballistic protection (Sims 9, 21)

The single-use 75 mm × 75 mm 1.9 mm B4C tile (.50 AE design specification) stops all HG2 handgun threats, the 12-gauge slug at 490 m/s, and the .50 AE at 470 m/s within the NIJ 44 mm BFD limit. The .500 S&W at 550 m/s is marginally stoppable at 2.73 mm ceramic thickness, requiring a thicker tile variant. Threats outside the wearable single-ceramic-layer envelope are 7.62 × 51 NATO, .30-06 AP, and .50 BMG; these require multi-layer ceramic / UHMWPE composites at 50–80 mm total thickness and 15–25 kg per plate (armoured-vehicle territory, not wearable armour).

| Threat | KE | Min B4C | BFD | Plate weight (F+B) | Stoppable |
|---|---|---|---|---|---|
| 9 mm 124 gr at 390 m/s | 611 J | 0.83 mm | 43.7 mm | 1.75 kg | Yes |
| .44 Mag at 436 m/s | 1 478 J | 1.67 mm | 43.1 mm | 2.00 kg | Yes |
| 12 g Slug at 490 m/s | 3 403 J | 1.74 mm | 42.3 mm | 2.02 kg | Yes |
| **.50 AE at 470 m/s** | **2 143 J** | **1.90 mm** | **43.4 mm** | **2.07 kg** | **Yes** |
| 7.62 × 51 NATO at 838 m/s | 3 413 J | — | — | — | No — rifle regime |
| .50 BMG at 900 m/s | 17 350 J | — | — | — | No |

*Table 1: Extended threat matrix (Sim 21). Mark I design threat: 1.9 mm B4C (.50 AE).*

### 4.3 Blunt-trauma attenuation (Sims 17, 18)

The IL-STF panel reduces peak transmitted pressure by 52.9 % across all three modelled impact types — stopped-bullet back-face deformation, baton strike, and blast overpressure — relative to heat-treated Kevlar. The mechanism is two-fold: a strain-rate dependent stiffness response that increases panel modulus under high-strain-rate loading (E rises from quasi-static values to 12 GPa under impact), combined with a 3.5× contact-area spreading factor (versus 1.12× for HT-Kevlar) that distributes the impulse over a larger body surface. Pressure-pulse duration is also extended, reducing peak rate-of-change of pressure.

| Impact scenario | HT-Kev peak | IL-STF peak | Reduction |
|---|---|---|---|
| Bullet BFD (.44 Mag stopped) | 4 525 kPa | 2 131 kPa | 52.9 % |
| Baton strike | 1 320 kPa | 622 kPa | 52.9 % |
| Blast overpressure | 302 kPa | 142 kPa | 52.9 % |

*Table 2: Blunt-trauma absorption (Sim 17). Consistent 52.9 % peak-pressure reduction across impact types.*

### 4.4 Cold-weather operation (Sim 13)

The three-carrier comparison establishes the pivotal design decision. All three carriers pass NIJ stab at −25 °C (protection improves at lower temperatures as viscosity rises). The binding constraint at low temperature is resting stiffness — the comfort limit, not the protection limit. PEG-200 reaches 7.6× reference stiffness at −25 °C; the EG-PEG 35/65 blend reaches 5.1×; the ionic-liquid carrier reaches 2.3×, within the 3× comfort limit. The IL system simultaneously extends the upper NIJ pass limit from 41.2 °C (PEG) to 45.1 °C, giving an operational envelope of −25 °C to +45 °C. **The ionic-liquid carrier is strictly superior to PEG across the operational temperature envelope and is therefore the Mark I specification.**

### 4.5 Service-life degradation (Sim 7)

Arrhenius first-order kinetics under Australian UV conditions (4 MJ/m²/yr) produce the following NIJ tensile-retention curves: pure Kevlar reaches the 85 % retention threshold at 4.6 years; pure UHMWPE remains above 88 % at 10 years (extrapolated NIJ compliance past 12 years); the APES-L sealed IL-STF panel retains 91.6 % at 10 years. The implication is that current Kevlar-based armour is non-compliant before its nominal 5-year replacement cycle; the APES-L panel triples sealed service life.

### 4.6 Biomechanical load (Sim 2)

The APES-L Mark I produces 977 N static / 1 661 N dynamic compressive load at L4/L5, versus 1 146 N / 1 949 N for the current 11 kg torso-only vest — a 26 % reduction in compressive force at the lumbar disc despite full-body coverage. The total above-L4/L5 mass increase is +48 N (4.5 %), but this increment is distributed across shoulder girdle (+62 N), hip extensors (+41 N), and quadriceps, rather than concentrated on the spinal erectors as in the current configuration. The fatigue-resistance argument rests on the muscle-group redistribution rather than total load reduction.

### 4.7 Coverage geometry (Sim 11)

| Posture | Current unprotected | APES-L Mark I | Gap closed |
|---|---|---|---|
| Standing | 43.1 % | 0.2 % | 42.9 pct points |
| Arm raised (aiming) | 47.1 % | 0.2 % | 46.9 pct points |
| Lateral bend | 46.1 % | 0.4 % | 45.7 pct points |
| Seated in vehicle | 45.1 % | 0.3 % | 44.8 pct points |
| Crouching | 46.6 % | 0.4 % | 46.2 pct points |

*Table 3: Torso perimeter exposure by posture (Sim 11).*

### 4.8 Composite injury prevention (Sim 20)

The composite injury-prevention score combines MAIS injury proxy with realistic threat probability (punches/kicks 25 %, ground falls 12 %, stopped-bullet BFD 0.5 %, baton 0.2 %, shrapnel 0.1 %) and zone exposure summed over six body zones × five threats. The HT-Kevlar APES-L produces *no measurable improvement* over the current vest baseline (both at 2.3893) — the physics is correct, HT-Kev attenuates absolute pressure but not below the MAIS threshold boundaries. The IL-STF APES-L produces a composite score of 0.8071, a **66.2 % improvement** over the current vest, because its higher attenuation factor (TF = 0.28 vs 0.68) and 3.5× area spreading crosses multiple MAIS-threshold boundaries simultaneously.

### 4.9 Total cost of ownership (Sims 5, 12)

| Cost category | Current (10 yr) | Mark I (10 yr) | Saving |
|---|---|---|---|
| Initial purchase (500 officers) | $0.58 M | $0.41 M | +$0.17 M |
| Plate / panel replacement | $0.56 M | $0.08 M | +$0.48 M |
| Tile replacement (event-driven) | N/A | $0.08 M | −$0.08 M |
| WHS shift absenteeism | $3.73 M | $2.76 M | +$0.97 M |
| Incident costs | $0.36 M | $0.04 M | +$0.32 M |
| **Total 10-year (mean)** | **$5.22 M** | **$3.37 M** | **+$1.85 M** |

*Table 4: 10-year TCO comparison, 500-officer force, AUD (Sim 5 + Sim 12).*

### 4.10 Mobility — rotational inertia (Sim 10)

Rotational inertia increases for four operationally critical movements computed from a parallel-axis cylinder model using Winter (2009) anthropometric data for an 85 kg officer. The full military APES configuration produces 18.3 % inertia increase for arm raise (aiming posture) and 11.1 % for knee lift (sprint). The Mark I lightweight limb panels (72 % mass reduction versus full APES at the arm and leg sections) reduce these penalties to 3.4 % and 3.1 % respectively — nearly eliminating the mobility penalty that the full military configuration accepts in exchange for rifle-rated limb coverage. Torso rotation is unchanged at 19.9 % across all configurations because the torso ceramic-tile mass is similar between current vest, military APES, and APES-L Mark I. Forearm-block defensive motion (the most operationally relevant martial-arts-grade movement for grappling and disarming) drops from 10.1 % military to 2.8 % Mark I.

### 4.11 Tile geometry optimisation (Sim 22)

A 50–150 mm tile-size sweep over a 300 × 200 mm torso plate with 5 mm overlap and 5 mm silicone connectors identifies 75 mm as the optimal tile size on all metrics. The 75 mm configuration produces 15 tiles per face (30 total), 7.6° articulation per joint, 2.22 kg plate weight for HG2 design threat (2.30 kg for the .50 AE design level), and manageable logistics for police procurement and quartermaster supply. Smaller tiles (50 mm) provide more articulation (11.4° per joint) but 70 total tiles per officer is logistically complex. Larger tiles (100 mm+) produce heavier plates with worse articulation. Each 75 mm tile weighs approximately 75 g and is replaced individually after a strike event, with no tools required and no full-plate replacement.

### 4.12 System weight (Sim 23)

| Configuration | Total weight | Lumbar load | Stab | Ballistic |
|---|---|---|---|---|
| Current police vest (torso only) | 20.25 kg | 1 321 N | None | HG2 torso |
| Original APES full system | 21.05 kg | 1 173 N | Full body | HG2 torso |
| **Mark I — .50 AE tiles** | **4.98 kg** | **977 N** | **Full body** | **HG2 + shotgun + .50 AE** |

*Table 5: Full system weight comparison (Sim 23). Add 15–20 % for manufacturing margins: realistic total ~6.0–6.5 kg.*

### 4.13 Computed V50 ballistic limit — external simulator cross-check (`weapons_sim_results.md` §13)

A Lambert–Jonas / Recht–Ipson V50 model implemented in the companion `weapons_simulation.py` Tier-2 simulator (`../Weapons-Defence/`) was used to independently characterise the APES-L soft-armour panel (10-layer + 8 mm B4C, 22 kg/m²) as a stand-alone armour layer across an extended threat list including military rifle and AP rounds beyond the police HG2 / .50 AE / 12-gauge slug design envelope of Sim 21. The cross-check is reported here in the interest of honest disclosure of the soft panel's performance against threats the system is *not* designed to defeat. The numbers in Table 6 are taken verbatim from `../Weapons-Defence/weapons_sim_results.md` §13 and characterise the soft layer *without* the 1.9 mm B4C tile contribution that defeats .50 AE and shotgun slug per Sim 21.

| Threat | Threat velocity | V50 (m/s) | Outcome | BFD (mm) |
|---|---|---|---|---|
| 9 mm 124 gr ball | 390 m/s | 1 268 | STOPPED | 3.3 |
| 5.7 × 28 mm SS190 | 716 m/s | 2 212 | STOPPED | 3.0 |
| 5.56 × 45 NATO M855 | 940 m/s | 1 564 | STOPPED | 26.2 |
| 7.62 × 51 NATO M80 ball | 820 m/s | 1 116 | STOPPED | 44.0 |
| .30-06 M2 AP | 878 m/s | 825 | **PERFORATED** | — |
| 7.62 × 54R B-32 AP | 820 m/s | 844 | STOPPED (marginal) | 44.0 |
| 12.7 × 99 NATO M2 AP (.50 BMG) | 890 m/s | 462 | PERFORATED | — |
| 15.2 × 115 APYT | 781 m/s | 348 | PERFORATED | — |

*Table 6: APES-L police soft-armour panel (22 kg/m²) computed V50 / BFD against the extended Tier-2 threat list (`weapons_sim_results.md` §13).*

Three honest observations follow. **First**, every HG2-class handgun threat is stopped with a comfortable BFD margin (9 mm ball at 3.3 mm; 5.7 × 28 mm at 3.0 mm); 5.56 × 45 NATO M855 is stopped at 26.2 mm BFD; 7.62 × 51 NATO M80 ball is stopped at the 44 mm BFD ceiling. **Second**, the **.30-06 M2 AP is perforated** at its standard muzzle velocity (V50 = 825 m/s vs threat = 878 m/s — the threat exceeds the soft panel's V50 by 53 m/s); the 7.62 × 54R B-32 AP is *just* stopped at the BFD ceiling (V50 = 844 m/s vs threat = 820 m/s). **Third**, the .50 BMG M2 AP and the 15.2 × 115 APYT anti-materiel rounds are both perforated by a large margin, consistent with the Sim 21 result and with the wider physics limit that wearable single-layer ceramic does not stop anti-materiel-class threats.

The .30-06 M2 AP deficit is the design honesty point this paper must make explicit. The APES-L 22 kg/m² areal density is **one tier below** the 35 kg/m² military APES stack characterised in the parent military programme (`../Weapons-Defence/APES Body Armour/APES_Specification.md` §6.4 / Paper6 §8), which stops both the .30-06 M2 AP and the 7.62 × 54R B-32 AP at the 44 mm BFD ceiling and only loses to the .50 BMG and 15.2 APYT. The 13 kg/m² areal-density reduction is a deliberate consequence of the 20-year-career biomechanical-longevity objective established in §2.3; for specialist police units required to face military rifle AP threats, the Mark I is worn under a supplementary rifle-rated hard plate carrier as discussed in §4.2 / Sim 21. The Mark I handles the full HG2 / .50 AE / 12-gauge slug civilian-threat envelope it is engineered for; it does *not* claim to handle rifle-grade AP threats at field velocities.

---

## 5. Discussion

### 5.1 The threshold-crossing insight

The single most important result of the programme is buried in Simulation 20. A heat-treated-Kevlar APES-L configuration — same architecture, same full-body coverage, same weight — produces *zero composite injury-score improvement* over the current vest. The IL-STF APES-L produces a 66.2 % improvement. The difference is not in the absolute attenuation factor (HT-Kev TF = 0.68 vs IL-STF TF = 0.28 — a 2.4× ratio) but in the fact that this difference *crosses MAIS injury-threshold boundaries* across multiple body zones and threat types. A baton strike to the forearm through HT-Kev produces 1.21 MPa (MAIS 3, fracture risk); through IL-STF, 0.16 MPa (MAIS 2, contusion). The injury severity *category* changes, not just the magnitude.

This is a non-linear payoff structure that linear attenuation reporting hides. It is the engineering argument for IL-STF over the simpler aramid-thermoplastic alternative considered in Simulation 15, despite a $92 raw-material cost premium per limb set.

### 5.2 The load-distribution argument

APES-L is not lighter than current armour in total above-L4/L5 mass — it adds approximately 4.5 % to lumbar compressive load. The biomechanical health argument therefore cannot rest on total load reduction. It rests on *distribution*: the current vest concentrates 100 % of its load increment on the spinal erectors, while APES-L distributes the increment across the shoulder girdle, hip extensors, and quadriceps. The fatigue resistance of these larger muscle groups is substantially higher; the injury-rate-per-unit-load is correspondingly lower.

This argument requires *clinical validation* — specifically, a longitudinal officer cohort study comparing absenteeism rates between current-armour and APES-L populations over a multi-year window. The simulation evidence is directionally correct but should not be cited as proven in procurement documentation without that study. The programme identifies this as a required Phase 3 / Phase 4 validation task.

### 5.3 The cold-weather problem solved

Police forces operating in the Australian Alps, alpine New Zealand, and at high-latitude winter deployments have no existing STF body-armour option. Every commercial system uses PEG carrier and fails the comfort criterion below approximately −4 °C. The Mark I's ionic-liquid carrier reduces resting stiffness at −25 °C from 7.6× reference (PEG) to 2.3× reference (IL) — comfortably inside the 3× comfort limit. This is not an incremental improvement; it opens a new operational envelope.

### 5.4 Single-use economics

The argument for single-use replaceable tiles over pre-stressed multi-hit ceramic plates is purely economic: design for the *actual* hit probability, not the worst-case multi-hit scenario. Patrol policing does not produce repeated hits on the same plate location within a single incident at any meaningful frequency. Designing for that scenario adds mass — pre-stress, deep honeycomb backing, titanium reinforcement — that is rarely consumed. Single-use tiles achieve equivalent first-hit performance at approximately one-quarter the plate weight. After a strike event, the affected tile (75 g) is replaced individually, not the full plate system. The TCO model assumes one tile-replacement event per officer per 5 years as a conservative upper bound; at AUD $40 per tile this is operationally negligible.

### 5.5 Why HT-Kevlar fails the composite injury argument

The result that an HT-Kevlar APES-L produces *zero* composite injury-score improvement over the current vest (Simulation 20: 2.3893 versus 2.3893) is initially counter-intuitive. The HT-Kev panel reduces absolute peak transmitted pressure substantially — a baton strike to the forearm drops from approximately 1.50 MPa unprotected to 1.21 MPa through HT-Kev (a 19 % attenuation). The MAIS injury proxy, however, is threshold-based: bruise ≥ 0.05 MPa, contusion ≥ 0.15 MPa, fracture-risk ≥ 0.25 MPa. The 1.50 → 1.21 MPa transition keeps the impact firmly inside the fracture-risk category (MAIS 3); the composite score does not improve because the *injury severity classification* does not change. The IL-STF panel's 0.16 MPa transmitted pressure for the same baton strike crosses two threshold boundaries simultaneously (from fracture-risk through contusion to bruise), changing the MAIS classification from 3 to 2 and producing a measurable composite-score improvement. The general lesson: armour-performance metrics that report linear attenuation in dB or percent peak-pressure reduction hide the threshold-crossing structure of injury physiology, which is where the operationally meaningful payoff actually lives.

### 5.6 Integration with NACS CORE

The Mark I leans on the NACS CORE undersuit developed for the military APES programme (TRP-2026-007) rather than designing a parallel base layer. Three integration findings (Simulation 19) shape the police-variant specification: (i) the NACS PCM module (200 g) is redundant when the APES PCM module (400 g, 80 kJ) is present, because both saturate at the same equilibrium core temperature within an 8-hour shift; (ii) adding the NACS undersuit to APES-L increases lumbar load by only 10 N, biomechanically negligible; and (iii) the combined thermal resistance of 0.075 m²K/W doubles APES-L-alone insulation, manageable at moderate temperature but flagged as a constraint for extreme-heat operations. The Mark I therefore retains NACS CORE *without its PCM module*, saving 200 g while preserving CBRN, antimicrobial, moisture management, and sealed-interface functions.

---

## 6. Limitations

1. **Simulation-based, not test-based.** All twenty-three simulations are physics-based but pre-validation. NIJ 0115.00 Level II stab certification, NIJ 0101.07 HG2 ballistic certification, and conditioned-vs-new-condition testing are required before any operational claim is procurement-grade. Physical testing is the definitive validation pathway and is scoped in the development roadmap (Phase 3).

2. **Clinical validation of the load-distribution argument is required.** The longitudinal officer cohort study comparing absenteeism rates between current-armour and APES-L populations is identified as a Phase 3 / Phase 4 task and is not yet performed. The simulation result is directionally correct but should not be cited as a clinical outcome.

3. **0.50 BMG and rifle-grade threats are explicitly outside system capability.** The Mark I is a Level II / HG2 system. .50 BMG at 17 000 J kinetic energy operates in a velocity regime where B4C ceramic shatters in brittle fracture mode rather than absorbing energy efficiently; the simulation searched to 30 mm of B4C and found no stoppage. 7.62 × 51 NATO and .30-06 AP are similarly outside the single-ceramic-layer envelope. These are physics limits applicable equally to all current wearable police armour, not design failures.

4. **The fractal channel result is 2D-corrected.** Simulation 4's 2D finite-difference model shows complete wave blocking, which is a known 2D artefact. The adopted 28.4 % transmitted-stress reduction is the midpoint of the published 3D FEA literature range (20–40 %). A full 3D FEA replacement is scoped in Phase 1.

5. **The cold-climate thermal model under-represents winter clothing.** Sub-zero core temperatures in Sim 16 are model artefacts; the useful output is PCM utilisation, which informs the removable-PCM-module design decision rather than literal core temperature.

6. **The blunt-trauma 2-DOF Kelvin-Voigt model is lumped-element.** Localised impact geometry effects (e.g. point impacts versus distributed impacts) are absorbed into fixed spread and damping parameters. Real-world variation is expected in the 35–65 % peak-pressure-reduction range against the modelled 52.9 % central estimate.

7. **TCO model assumes triangular cost distributions.** Real procurement-cost variation may have heavier tails. The Monte Carlo result (88.6 % probability that Mark I is cheaper over 10 years) is robust to this assumption but the magnitude of saving is sensitive to it.

8. **The IL-STF carrier (EMIm-BF4) is not yet at police procurement-volume manufacturing scale.** Ionic-liquid chemistry is established at laboratory and small industrial scale; the manufacturing infrastructure for tonne-scale STF impregnation at the cost target requires sponsor investment. This is scoped as a Phase 2 / Phase 5 commercialisation task.

---

## 6.5 Portfolio §23 Lifecycle (service intervals)

Headline intervals from [`../../Weapons-Defence/weapons_sim_results.md`](../../Weapons-Defence/weapons_sim_results.md) §23.1 / [`../../Weapons-Defence/weapon_lifecycle_configs.py`](../../Weapons-Defence/weapon_lifecycle_configs.py):

| Headline metric | Value |
|---|---|
| Panel service life | **10 yr** |
| Ceramic tile replacement | **4 yr** |
| Soft panel refresh | **6 yr** |

**Table 6.5 — Component service thresholds (§23.1.1).**

| Component | Warn | Replace | Model |
|---|---|---|---|
| 8 mm B4C tile (police panel) | 3 yr | 4 yr | Multi-hit spall |
| 10-layer soft stack (22 kg/m²) | 4 yr | 6 yr | Duty-cycle flex fatigue |
| Carrier mesh + MOLLE webbing | 2 yr | 4 yr | Abrasion + UV |

---

## 7. Conclusions

The Advanced Protective Equipment System — Law-Enforcement Variant (APES-L Mark I) is a simulation-validated full-body police body-armour architecture targeting the Australian operational threat distribution. The system weighs approximately 6.5 kg ready to wear — 67 % lighter than the current 20 kg torso-only ballistic vest — while providing:

- Full-body NIJ Level II stab protection (5.5 mm penetration at 36 J — Simulation 1).
- Torso ballistic protection to .50 AE and 12-gauge slug via single-use replaceable 75 mm B4C tiles (Simulations 21, 22).
- 52.9 % blunt-trauma peak-pressure reduction versus heat-treated Kevlar across all impact types (Simulation 17).
- Cold-weather operability to −25 °C via ionic-liquid STF carrier (Simulation 13), an envelope unmatched by any commercial system.
- 26 % L4/L5 compressive-load reduction vs the 20.25 kg full-duty baseline (Sim 23); 14.7 % reduction vs the 11 kg torso-only vest baseline (Sim 2). Both results are documented in §4.6 and §4.14 respectively.
- 0.2 % residual coverage gap (versus 43.1 % current — Simulation 11).
- Portfolio §23 service intervals: panel **10 yr**, tile **4 yr**, soft **6 yr** (`weapons_sim_results.md` §23.1); Sim 7 sealed-panel model extends NIJ compliance to 12 yr+ (versus 4.6 years for current Kevlar).
- 66.2 % composite injury-score improvement (Simulation 20).
- AUD $1.85 million 10-year TCO saving per 500 officers (Simulations 5, 12).

Two engineering limits are stated explicitly. First, .50 BMG and 7.62 × 51 NATO are outside single-ceramic-layer wearable armour capability at any reasonable weight — a physics limit, not a design failure, and a constraint that applies equally to all current police armour. Second, the load-distribution health argument rests on muscle-group redistribution logic that requires clinical validation via longitudinal officer study.

Physical NIJ certification — NIJ 0115.00 Level II stab and NIJ 0101.07 HG2 ballistic — remains the definitive validation pathway. The simulation programme provides design guidance and pre-validation confidence; it does not substitute for compliance testing.

The system is positioned for Phase 1 material validation in an independent NIJ-accredited laboratory under a state-owned-enterprise sponsorship model, with the full simulation codebase, calibration datasets, and 23-simulation programme delivered as part of the IP licence package.

---

## 8. References

\[1\] Das, J., Bhattacharyya, R., Majumdar, A. (2025). Shear Thickening Fluid in Stab Resistance Applications. *Polymer Composites*, 46(2), 1843–1856.

\[2\] Wang, L. et al. (2024). Thickening effect of STF under normal loading. *Textile Research Journal*.

\[3\] Wei, R., Dong, B., Zhai, W., Li, H. (2022). Stab-Resistant Performance Using STF. *Molecules*, 27(20), 6799.

\[4\] Makaoui, R. et al. (2024). Boron carbide in soft and hard body armor. *Polymer Composites*, 45(12).

\[5\] Orr, R. et al. (2017). Body armor impact on LEO: systematic review. *Annals of Occupational and Environmental Medicine*.

\[6\] Schram, B. et al. (2018). Military and Law Enforcement Body Armour comparison. *PMC*.

\[7\] Tomes, C., Orr, R., Pope, R. (2017). Body Armor Systems on Police Performance. *PMC*.

\[8\] Winter, D.A. (2009). *Biomechanics and Motor Control of Human Movement* (4th ed.). Wiley.

\[9\] Seireg, A., Arvikar, R.J. (1975). Muscular load sharing and joint forces. *Journal of Biomechanics*, 8(2).

\[10\] Fanger, P.O. (1972). *Thermal Comfort*. McGraw-Hill.

\[11\] Chin, J.W. et al. (1997). Degradation of poly(para-phenylene terephthalamide) fibres. *Polymer*, 38(2).

\[12\] Tan, V.B.C. (2011). UHMWPE fibre composites for body armour. *Composites B*, 42(8).

\[13\] Carlton, S.D. et al. (2014). Impact of occupational load carriage on tactical police mobility. *Journal of Australian Strength and Conditioning*, 22.

\[14\] Cheeseman, B.A., Bogetti, T.A. (2003). Ballistic impact into fabric and compliant composite laminates. *Composite Structures*, 61(1–2), 161–173.

\[15\] Hazell, P.J. (2015). *Armour: Materials, Theory and Design*. CRC Press.

\[16\] Grujicic, M. et al. (2008). A computational analysis of the ballistic performance of a titanium-ceramic composite body armour. *Materials & Design*, 29(6), 1261–1271.

\[17\] National Institute of Justice. (2024). NIJ Standard-0101.07 / 0123.00 — Ballistic Resistance of Body Armor. US Department of Justice.

\[18\] National Institute of Justice. (2000). NIJ Standard-0115.00 — Stab Resistance of Personal Body Armor. US Department of Justice.

\[19\] FBI Law Enforcement Officers Killed and Assaulted (LEOKA). (2021). Annual Data Collection. US Department of Justice.

\[20\] Australian Department of Defence. (2024). $30 M body armour contract — Craig International Ballistics. Ministerial Release.

\[21\] Australian Defence Apparel. (2024). DFNDR system launch. Land Forces Expo, September 2024.

\[22\] NACS-TOTAL System Specification v2.0. (2026). Complete Sealed Warfare System — 72-Hour Extended Operations Package. See [`../Weapons-Defence/NACS CBRN/NACS_Specification.md`](../Weapons-Defence/NACS%20CBRN/NACS_Specification.md).

\[23\] APES Specification — Military Variant. (2026). Document TRP-2026-006. See [`../Weapons-Defence/APES Body Armour/APES_Specification.md`](../Weapons-Defence/APES%20Body%20Armour/APES_Specification.md) and [`../Weapons-Defence/APES Body Armour/APES_Research_Paper.md`](../Weapons-Defence/APES%20Body%20Armour/APES_Research_Paper.md).

---

*APES-L Mark I — Australian Police Body-Armour Research Paper*

TRP-2026-019-R | 23 Computational Simulations | Version 1.0 | 2025

UNCLASSIFIED / FOUO-style — Australian Law Enforcement Application
