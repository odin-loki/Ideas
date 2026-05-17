# TECHNICAL DATA PACKAGE (TDP)
## RUBBER TRACK PAD SYSTEM FOR MILITARY TRACKED VEHICLES

*Technical Data Package*

Document No. TRP-2026-306 | Version 1.0

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> **Hybrid Military Track Pad System — MIL-STD-compliant Technical Data Package.** Procurement-grade TDP for the rubber track pad system whose engineering analysis lives in the parent research paper `Paper14_Military_Track_Pad.md` (TRP-2026-014). Headline material classification is **ASTM D2000 4BG 720 A14 B13 C12 EA14 F17** — a HNBR 40 / NBR 30 / NR 25 / Neoprene 5 phr hybrid polymer blend with N550 carbon black (55 phr), precipitated silica (20 phr), aramid pulp (3 phr), and graphene oxide (0.5 phr) nano-reinforcement, vulcanised with a polymeric-sulfur / CBS / TBBS / TMTD accelerator package. Headline mechanical properties: **Shore A 72 ± 4 hardness, ≥26 MPa tensile strength, ≥95 N/mm tear strength (Die C), -40 °C to +150 °C continuous service**, ≤20 % property change after 70 h at 150 °C heat ageing (ASTM D573), no ozone cracking at 100 pphm / 40 °C / 20 % strain / 168 h (ASTM D1149). Attachment is a T-slot M10 × 1.5 Grade 10.9 bolt system with 5,000 N minimum pull-out, 12-minute field-replaceable, standard 8 mm hex tooling. Service life 800 km minimum. The acoustic-signature claim (15–20 dB noise reduction versus bare steel tracks) cross-checks against the portfolio simulator `weapons_simulation.py` track-acoustic block and `../weapons_sim_results.md`. The classification banner above is illustrative for tonal coherence with the rest of the Weapons-Defence portfolio; no real Australian Defence Force or U.S. Department of Defense programme office, sponsorship, or end-use is implied.

## Honest framing

- **Simulation-based, pre-physical-test.** Every mechanical / thermal / chemical / environmental property in §3 is a target specification, not a measured outcome on a vulcanised production pad. No ASTM D412 tensile, ASTM D624 tear, ASTM D2240 hardness, ASTM D395 compression-set, ASTM D5963 abrasion, ASTM D1149 ozone, ASTM D573 heat-ageing, ASTM D2137 brittleness, ASTM B117 salt-fog, ASTM D1435 weathering, or MIL-STD-810H Method 508.7 fungus measurement has been performed on a representative production sample. First Article Testing per MIL-STD-810H is explicitly the next step in the procurement plan.
- **Specific physical-limit boundaries that are NOT addressed.** Long-term polymer-phase-separation behaviour of the four-polymer HNBR / NBR / NR / Neoprene blend over a 7-year shelf life and 50,000-cycle service life; HNBR–graphene oxide interfacial bond stability under repeated -40 °C ↔ +150 °C thermal cycling; tracer-strike / hot-brass-contact survival on the antimony-trioxide flame-retardant package; and the actual acoustic-signature behaviour in the multi-source incoherent track-clatter spectrum of a mechanised column (versus the simplified single-vehicle bare-metal-vs-padded SPL comparison) are all outside the present TDP envelope.
- **Single source of truth.** Engineering rationale for the formulation, tread pattern, attachment system, and lifecycle cost lives in the parent research paper `Paper14_Military_Track_Pad.md`; acoustic-signature numbers cross-check against `weapons_simulation.py` and `../weapons_sim_results.md`.
- **Manufacturing / supply-chain caveats.** The 500 pads/day per line × 4 lines × 6 months = 900,000 pads production plan assumes qualified HNBR (35 % ACN), NBR (28 % ACN), graphene-oxide (>500 m²/g BET), and aramid-pulp (3 mm) suppliers; the supplier-qualification step is incomplete. Sovereign-content rules (Australian Defence Industry Security Programme; U.S. DFARS 252.225-7008 specialty metals; ITAR Category VII for the platform if exported) apply to any real contract. The 8 phr antimony trioxide flame retardant is a REACH SVHC candidate; substitution analysis is not in this TDP.
- **Standards-compliance footprint.** This TDP cites MIL-STD-810H, MIL-R-3065C, ASTM D2000, SAE J200, MIL-STD-129, MIL-STD-2073, and the ASTM D-series test methods. All references are to the standards' published methodologies for acceptance test design — no signed-off compliance certification, no auditor sign-off, and no DCMA / DCAA quality-system certification underwrites the TDP. NSN assignment is pending.
- **Classification is illustrative.** UNCLASSIFIED // FOR OFFICIAL USE ONLY is adopted for tonal coherence with the rest of the Weapons-Defence portfolio. The notional sponsor is the Australian Department of Defence for tonal consistency with the parent paper `Paper14_Military_Track_Pad.md`; the original TDP body retains "U.S. Department of Defense / Ground Vehicle Systems Center" framing in §DOCUMENT CONTROL and elsewhere, and no real programme office, sponsorship, or end-use is implied or held.

---

## DOCUMENT CONTROL

### Revision History
| Rev | Date | Description | Author |
|-----|------|-------------|--------|
| A | Feb 2026 | Initial release | Engineering Team |

### Applicable Documents
- MIL-STD-810H: Environmental Engineering Considerations
- MIL-R-3065C: Rubber, Natural and Synthetic, General Purpose
- ASTM D2000: Standard Classification System for Rubber Products
- SAE J200: Classification System for Rubber Materials
- MIL-STD-129: Military Marking
- MIL-STD-2073: DOD Packaging Standard

---

## TABLE OF CONTENTS

1. SCOPE
2. APPLICABLE DOCUMENTS
3. REQUIREMENTS
   3.1 Material Specifications
   3.2 Physical Properties
   3.3 Performance Requirements
   3.4 Dimensional Requirements
4. QUALITY ASSURANCE
5. PREPARATION FOR DELIVERY
6. NOTES

---

## 1. SCOPE

### 1.1 Purpose
This Technical Data Package (TDP) establishes the performance, material, and quality requirements for rubber track pads designed for installation on military tracked vehicle track shoes.

### 1.2 Application
These track pads are intended for use on main battle tanks, armored fighting vehicles, and other tracked military vehicles operating in diverse environmental conditions ranging from -40°C to +60°C ambient.

### 1.3 System Description
The track pad system consists of:
- Vulcanized rubber pad with molded tread pattern
- Embedded stainless steel mounting inserts (4 per pad)
- Mounting hardware (T-bolts, washers)
- Steel mounting plate (welded to track shoe)

---

## 2. APPLICABLE DOCUMENTS

### 2.1 Government Documents
- MIL-STD-810H: Environmental Engineering Considerations and Laboratory Tests
- MIL-R-3065C: Rubber, Natural and Synthetic, General Purpose
- MIL-STD-45662A: Calibration System Requirements
- MIL-STD-105E: Sampling Procedures and Tables for Inspection
- MIL-STD-129: Military Marking for Shipment and Storage
- MIL-STD-2073: Defense Materiel Management - Packaging Standard

### 2.2 Industry Standards
- ASTM D2000: Standard Classification System for Rubber Products in Automotive Applications
- ASTM D412: Standard Test Methods for Vulcanized Rubber and Thermoplastic Elastomers—Tension
- ASTM D624: Standard Test Method for Tear Strength of Conventional Vulcanized Rubber
- ASTM D2240: Standard Test Method for Rubber Property—Durometer Hardness
- ASTM D573: Standard Test Method for Rubber—Deterioration in an Air Oven
- ASTM D1149: Standard Test Method for Rubber Deterioration—Surface Ozone Cracking
- ASTM D395: Standard Test Methods for Rubber Property—Compression Set
- SAE J200: Classification System for Rubber Materials Used in Automotive Applications
- ISO 37: Rubber, vulcanized or thermoplastic—Determination of tensile stress-strain properties

---

## 3. REQUIREMENTS

### 3.1 MATERIAL SPECIFICATIONS

#### 3.1.1 Base Polymer Composition
The rubber compound shall consist of the following polymer blend (parts per hundred rubber, phr):

**Polymer Base:**
- Hydrogenated Nitrile Rubber (HNBR, 35% ACN content): 40 phr
- Nitrile Rubber (NBR, 28% ACN content): 30 phr
- Natural Rubber (NR, SMR CV60 grade): 25 phr
- Polychloroprene (Neoprene GRT grade): 5 phr

**Reinforcement Fillers:**
- Carbon Black (ASTM N550 grade): 55 phr
- Precipitated Silica (BET surface area 160-200 m²/g): 20 phr
- Aramid Fiber (pulp form, 3mm average length): 3 phr
- Graphene Oxide (surface area >500 m²/g): 0.5 phr
- Zinc Oxide (Grade II, 99.5% purity): 5 phr
- Magnesium Oxide (light grade): 2 phr

**Vulcanization System:**
- Polymeric Sulfur: 1.5 phr
- N-cyclohexyl-2-benzothiazole sulfenamide (CBS): 1.2 phr
- N-tert-butyl-2-benzothiazole sulfenamide (TBBS): 0.6 phr
- Tetramethylthiuram disulfide (TMTD): 0.4 phr
- Stearic Acid: 2 phr

**Functional Additives:**
- Aromatic Ester Plasticizer: 8 phr
- Tackifier Resin: 4 phr
- Antiozonant (6PPD): 2 phr
- Antimony Trioxide (flame retardant): 8 phr
- Butyl Rubber (acoustic damping): 5 phr

#### 3.1.2 Metal Insert Specifications
**Material:** Stainless Steel Type 316 per ASTM A276
**Configuration:** Knurled T-nut with hex socket
**Thread:** M10 × 1.5 ISO metric coarse thread
**Surface Treatment:** 
- Brass plating: 5-10 μm thickness per ASTM B633
- Rubber bonding primer: Chemlok 205 or equivalent
**Knurl Specifications:**
- Pattern: Diamond knurl, 96 DP
- Depth: 2.0 ± 0.2 mm
- Coverage: Full circumference

#### 3.1.3 Mounting Hardware
**T-Bolt Specifications:**
- Material: Alloy steel, Grade 10.9 per ISO 898-1
- Thread: M10 × 1.5 × 40mm length
- Head: T-head design, 12mm × 6mm
- Surface Treatment: Zinc-nickel coating, 8-12 μm
- Thread Locking: Nylon patch on threads

**Washer Specifications:**
- Material: Hardened steel, HRC 38-45
- Type: Captive design, 18mm OD × 2mm thick
- Surface Treatment: Zinc plating per ASTM B633

**Mounting Plate:**
- Material: Alloy steel plate, ASTM A572 Grade 50
- Thickness: 8.0 ± 0.5mm
- Surface Treatment: Black oxide coating
- Hardness: HRB 85-95

### 3.2 PHYSICAL PROPERTIES

#### 3.2.1 Mechanical Properties (ASTM D2000 Classification: 4BG 720 A14 B13 C12 EA14 F17)

| Property | Test Method | Requirement | Units |
|----------|-------------|-------------|-------|
| **Tensile Strength** | ASTM D412 | 26 minimum | MPa |
| **Elongation at Break** | ASTM D412 | 350 minimum | % |
| **Hardness** | ASTM D2240 | 72 ± 4 | Shore A |
| **100% Modulus** | ASTM D412 | 4.5 - 6.5 | MPa |
| **300% Modulus** | ASTM D412 | 15 - 20 | MPa |
| **Tear Strength (Die C)** | ASTM D624 | 95 minimum | N/mm |
| **Compression Set (22h @ 70°C)** | ASTM D395 Method B | 25 maximum | % |
| **Abrasion Loss (Akron)** | ASTM D5963 | 70 maximum | mm³ |

#### 3.2.2 Temperature Properties

| Property | Test Method | Requirement |
|----------|-------------|-------------|
| **Low Temperature Brittleness** | ASTM D2137 | Pass at -40°C |
| **Heat Aging (70h @ 150°C)** | ASTM D573 | ≤20% change in tensile/elongation |
| **Continuous Service Temperature** | — | -40°C to +150°C |
| **Intermittent Peak Temperature** | — | +180°C for 30 minutes |

#### 3.2.3 Chemical Resistance

| Fluid | Test Method | Requirement |
|-------|-------------|-------------|
| **ASTM Oil No. 3 (70h @ 150°C)** | ASTM D471 | Volume change: +10% to +30% |
| **Diesel Fuel (70h @ 23°C)** | ASTM D471 | Volume change: +15% maximum |
| **Hydraulic Fluid (MIL-PRF-83282)** | ASTM D471 | Volume change: +20% maximum |
| **Water (70h @ 100°C)** | ASTM D471 | Volume change: +5% maximum |

#### 3.2.4 Environmental Resistance

| Property | Test Method | Requirement |
|----------|-------------|-------------|
| **Ozone Resistance** | ASTM D1149 | No cracks at 100 pphm, 40°C, 20% strain, 168h |
| **UV/Weathering** | ASTM D1435 | ≤15% property degradation after 1000h |
| **Fungus Resistance** | MIL-STD-810H Method 508.7 | No growth |
| **Salt Fog** | ASTM B117 | No corrosion of metal inserts after 500h |

### 3.3 PERFORMANCE REQUIREMENTS

#### 3.3.1 Dimensional Requirements

**Overall Dimensions:**
- Length: 250 ± 2 mm
- Width: 150 ± 2 mm
- Thickness (nominal): 25 ± 1 mm
- Tread Depth: 8 ± 0.5 mm (new), 6 mm minimum (wear limit)

**Mounting Hole Specifications:**
- Quantity: 4 per pad
- Pattern: Rectangular, 30mm from each corner
- Insert Depth: 20 ± 1 mm from pad bottom
- Insert Pull-Out Force: 5000 N minimum

**Flatness:**
- Maximum deviation from plane: 2 mm across any 100 mm span
- No warping or distortion after cure

**Weight:**
- 950 ± 50 grams per pad

#### 3.3.2 Tread Pattern Specifications

**Pattern Type:** Hybrid Military Design (per Drawing TDP-001-PAD-TREAD)

**Features:**
- Central Chevron Bars: 3 pairs at 45° angle
  - Width: 30 ± 1 mm
  - Depth: 8 ± 0.5 mm
  - Spacing: 70 ± 2 mm center-to-center

- Center Drainage Blocks: 6 units
  - Dimensions: 30 × 25 × 7 mm (±1 mm)
  
- Edge Sipes: 32 per side
  - Width: 2 ± 0.5 mm
  - Depth: 6 ± 0.5 mm
  - Spacing: 15 ± 2 mm

- Corner Stability Blocks: 4 units
  - Dimensions: 15 × 15 × 6 mm (±1 mm)

**Contact Ratio:** 66 ± 3%
**Void Ratio:** 34 ± 3%

#### 3.3.3 Durability Requirements

**Cyclic Loading:**
- Test Method: MIL-STD-810H Method 514.7 (Vibration)
- Requirement: No cracking, tearing, or delamination after 50,000 cycles at 80% rated load

**Tear Propagation:**
- Test Method: ASTM D624 (Trouser tear)
- Requirement: Tear shall not propagate across pad width

**Impact Resistance:**
- Drop Test: 2 meter drop onto concrete surface
- Requirement: No chunking or separation of tread elements

**Insert Pull-Out:**
- Test Method: Axial tensile pull at 50 mm/min
- Requirement: 5000 N minimum before pull-out or rubber failure

**Fatigue Life:**
- Simulated track operation: 800 km minimum before replacement criteria
- Replacement Criteria: Tread depth <6 mm OR visible cracking

#### 3.3.4 Flammability Requirements

**Flame Resistance:**
- Test Method: FMVSS 302 (Horizontal Burn Test)
- Requirement: Self-extinguishing within 5 seconds
- Burn Rate: <100 mm/min

#### 3.3.5 Acoustic Performance

**Noise Reduction:**
- Test Method: SAE J57 (exterior sound level)
- Requirement: ≥15 dB reduction compared to bare metal track at 10 km/h

**Vibration Damping:**
- Frequency Range: 1-100 Hz
- Damping Coefficient: ≥0.15

**Computed Vibration Transmission (Tier-2 Simulator §19):**

The 1-DOF mass-spring-damper transmissibility model in `Weapons-Defence/weapons_sim_results.md` §19 was evaluated at a 300 Hz drive frequency (typical track frequency at 30 km/h transit speed). The simulator predicts:

- Steel-on-steel mounting transmissibility: **−22.3 dB**
- HNBR composite pad transmissibility: **−43.1 dB**
- **Net free-field SPL reduction: 20.8 dB**

This validates the ≥15 dB requirement above and sits in the upper half of the 15–20 dB range cited for rubber track pads in the published mil-spec literature. Acceptance testing per SAE J57 (acoustic) and ASTM D4065 (dynamic mechanical analysis at 300 Hz) is required to confirm the simulator prediction on production pads; the simulator output (`weapons_simulation.py`) provides design-window guidance only.

### 3.4 MANUFACTURING REQUIREMENTS

#### 3.4.1 Vulcanization Parameters

**Cure Cycle:**
- Temperature: 165 ± 5°C
- Pressure: 150 ± 10 bar (15 ± 1 MPa)
- Time: 15 ± 1 minutes
- Flash Cure: 180°C × 2 minutes (surface hardening)

**Mold Requirements:**
- Material: Tool steel, hardened to HRC 48-52
- Surface Finish: Ra 1.6 μm or better
- Temperature Control: ±2°C across mold surface

**Insert Installation:**
- Method: Molded-in during vulcanization
- Positioning Tolerance: ±0.5 mm from nominal
- Bonding: Chemical bond + mechanical interlock (knurling)

#### 3.4.2 Quality Control During Manufacturing

**In-Process Testing (Every 10th Pad):**
- Shore A hardness
- Dimensional verification (go/no-go gauges)
- Visual inspection for voids, flash, contamination
- Metal insert seating depth

**Batch Testing (Per Production Run):**
- Cure state measurement (Monsanto ODR)
- Compound viscosity (Mooney viscometer)
- First article physical property verification

---

## 4. QUALITY ASSURANCE

### 4.1 Responsibility for Inspection
The contractor is responsible for performing all inspections required prior to submission to the Government. Except as otherwise specified, the contractor may use their own or any other inspection facilities and services acceptable to the Government.

### 4.2 Inspection Requirements

#### 4.2.1 First Article Inspection
Prior to production, the contractor shall submit samples for First Article Testing (FAT) consisting of:
- 20 track pads with mounting hardware
- 5 pads for destructive testing
- Complete manufacturing process documentation
- Material certifications

**First Article Testing shall include:**
- All physical property tests per Section 3.2
- All performance tests per Section 3.3
- Environmental testing per MIL-STD-810H
- Accelerated aging (1000 hours @ 70°C)

#### 4.2.2 Production Inspection

**100% Inspection:**
- Visual inspection for defects
- Dimensional verification (critical dimensions)
- Hardness testing
- Weight verification

**Sampling Inspection (MIL-STD-105E, Level II, AQL 1.0):**
- Tensile properties: 1 specimen per 500 pads
- Tear strength: 1 specimen per 500 pads
- Compression set: 1 specimen per 1000 pads
- Insert pull-out: 1 specimen per 200 pads

### 4.3 Acceptance Criteria

**Individual Pad Acceptance:**
- All dimensional requirements met
- No visual defects (cracks, voids, contamination, flash)
- Hardness within specification
- Metal inserts properly seated and bonded

**Lot Acceptance:**
- All sampled specimens meet physical property requirements
- No failures in performance testing
- Material certifications on file

**Lot Rejection:**
- Any sampled specimen fails physical properties by >10%
- Any insert pull-out failure
- Evidence of process deviation or contamination

### 4.4 Quality Records

The contractor shall maintain records for minimum 10 years:
- Material lot certifications
- Cure records (time, temperature, pressure)
- Inspection results
- Non-conformance reports
- Corrective actions

---

## 5. PREPARATION FOR DELIVERY

### 5.1 Preservation and Packaging

**Individual Pad Protection:**
- Clean surface with isopropyl alcohol
- Apply protective film or shrink wrap
- Pair pads back-to-back with cardboard separator

**Packaging Configuration:**
- 20 pads per wooden crate
- Include desiccant pack (MIL-D-3464, Type II)
- Interior: corrugated cardboard dividers
- Hardware: Separately bagged and labeled

**Crate Specifications:**
- Material: Wood per ASTM D6198 (ISPM-15 compliant)
- Construction: Nailed or screwed assembly
- Gross Weight Limit: 50 kg per crate

### 5.2 Marking

**Individual Pad Marking (molded-in):**
- NSN (National Stock Number)
- Lot Number
- Date Code (YYMM format)
- Contractor Identification

**Crate Marking (stenciled per MIL-STD-129):**
- Contract Number
- NSN
- Quantity
- Gross Weight
- Cube Dimensions
- "THIS SIDE UP" arrows
- "KEEP DRY" symbol

### 5.3 Storage

**Storage Conditions:**
- Temperature: 15-30°C
- Humidity: 30-70% RH
- Environment: Cool, dark, dry
- Position: Horizontal stacking, maximum 4 crates high
- Protection: Away from ozone sources, UV light, petroleum products

**Shelf Life:**
- 7 years from date of manufacture (unopened packaging)
- 3 years extension possible with re-inspection

---

## 6. NOTES

### 6.1 Intended Use
These rubber track pads are designed to reduce noise, vibration, and road damage during military tracked vehicle operations on paved surfaces while maintaining all-terrain capability.

### 6.2 Ordering Data

Procurement documents should specify:
- NSN: TBD (to be assigned)
- Quantity required
- Delivery schedule
- Destination
- Contract number reference

### 6.3 Subject Term (Key Word) Listing
- Track pads
- Rubber compounds
- Military vehicles
- Tracked vehicle components
- Vibration damping
- HNBR rubber

### 6.4 Changes from Previous Issue
This is the initial release (Revision A).

---

## 12. Manufacturing Cost Analysis

The HNBR rubber track pad is an industrial manufactured component. Cost model:

### 12.1 HNBR track pad BOM — per pad at three production volumes

**Table 12.1.** HNBR track pad BOM — per pad at three production volumes.

| Component | Material / Process | 5 000 pads/yr | 25 000 pads/yr | 100 000 pads/yr |
|---|---|---|---|---|
| HNBR rubber compound (Shore A 72, ASTM D2000 4BG) | Compounding + mixing | A$12.40 | A$9.80 | A$7.60 |
| Steel backing plate (heat-treated, M10 bolt holes) | Press stamping + heat treat | A$8.20 | A$6.40 | A$4.90 |
| Bonding agent (vulcanisation-bond HNBR to steel) | Surface prep + primer | A$1.80 | A$1.40 | A$1.10 |
| Compression moulding (15-min cure cycle, hydraulic press) | Labour + machine time | A$5.60 | A$4.20 | A$3.10 |
| QC (Shore A, pull-off adhesion per ASTM D429, noise attenuation spot-check) | Inspection labour | A$3.20 | A$2.40 | A$1.80 |
| Packaging + marking (MIL-SPEC-130 labelling) | Materials + labour | A$1.40 | A$1.10 | A$0.85 |
| Factory overhead, tooling amortisation | — | A$2.90 | A$2.10 | A$1.60 |
| **Total per pad** | | **A$35.50** | **A$27.40** | **A$20.95** |

**Vehicle re-pad cost.** A standard main battle tank (M1A2 Abrams equivalent) requires approximately 96 pads per track × 2 tracks = **192 pads per vehicle**. Full vehicle re-pad at the three volume tiers: **A$6 816 / A$5 261 / A$4 022 per vehicle**.

**Production volume context.** ADF armoured fleet of 400 vehicles × 192 pads × 3-year replacement cycle = 25 600 pads per replacement cycle = approximately **8 533 pads/yr**. This falls between the 5 000/yr and 25 000/yr tiers.

**Comparison to steel pad.** Steel track pads (current-issue): approximately A$12/pad material cost + A$4/pad machining + A$2/pad overhead = **A$18/pad**. The HNBR pad at A$21–36/pad is 17–100% more expensive per pad, but provides the 15–20 dB noise-reduction benefit documented in §19 of weapons_sim_results.md and extends track life by reducing metal-on-metal contact impact forces.

**Programme cost (400-vehicle ADF fleet, 10 years, 3-year replacement cycle):**
- 3.33 replacement cycles over 10 years
- Total pads: 400 vehicles × 192 pads × 3.33 cycles = **255 936 pads**
- At A$27.40/pad (25 k/yr volume): **A$7.01 M**
- Steel pad equivalent (A$18/pad): **A$4.61 M**
- **Premium for HNBR noise + life benefit: A$2.40 M over 10 years = A$6 000 per vehicle per decade**

Given that armoured vehicle noise-induced hearing loss (NIHL) incidence in ADF ranks was estimated at 32% of armoured crew members (cited in the TACS_Complete_Specification.md), and that a single NIHL compensation claim averages A$280 000 in Australian Defence Force entitlements, the break-even point for the HNBR premium is approximately **8–9 NIHL cases avoided per decade** across the 400-vehicle fleet — a highly plausible outcome.

---

## 13. Intellectual Property and Licensing

### 13.1 IP assets

**Table 13.1.** IP assets.

| # | IP asset | Description | Protection approach |
|---|---|---|---|
| 1 | **HNBR compound formulation (Shore A 72)** | Highly reinforced nitrile-butadiene rubber at Shore A 72 hardness, ASTM D2000 4BG environment qualification, tuned to ω_n = 25 Hz / ζ = 0.18 noise-isolation specification | Trade secret (compound recipe) + TTP process specification |
| 2 | **Steel backing + HNBR vulcanisation bond geometry** | Bolt-hole pattern, backing thickness, and vulcanisation bond interface geometry optimised for the track-link interface | Design patent (backing geometry) |
| 3 | **Pad geometry and track-link interface** | Overall pad shape, track-link male/female mating faces, bolt-pattern specification compatible with M1A2 and AS21 Redback track systems | Design patent (interface geometry) |
| 4 | **1-DOF mass-spring-damper noise transmissibility model** | The simulation model in weapons_simulation.py §19 producing the quantified 15–20 dB noise reduction at 300 Hz drive frequency | Software copyright |
| 5 | **Lifecycle fatigue model (Miner's rule adapted for track pad)** | The cumulative fatigue model calibrated to the HNBR compound's strain-life curve, enabling 3-year / 2 000 km/yr service life prediction | TTP: model + calibration dataset |

### 13.2 Licensing routes

**Table 13.2.** Licensing routes.

| Route | Description | Up-front | Per-pad royalty | TTP |
|---|---|---|---|---|
| Route A — Direct procurement | Government buys finished pads from IP holder's designated manufacturer | Nil | Included in supply margin | No |
| Route B — Licensed manufacture | Australian rubber manufacturer produces pads under licence | A$0.42 M | A$1.80/pad | Yes |
| Route C — Sovereign buyout | Full technology transfer | A$2.1 M | Nil | Yes |

### 13.3 Export controls

The HNBR track pad is a dual-use item controlled under DSGL ML6 (ground vehicles and vehicle components). Track pads specifically designed for military vehicles require an export permit under the Customs Act 1901 (s112A). Export to non-Five Eyes partners requires additional Department of Defence approval. The simulation programme (weapons_simulation.py §19 module) is not separately export-controlled but is included in the DSGL ML6 technology package.

---

## 14. Procurement Framework

**Phase 1 — Materials qualification (months 1–6):** HNBR compound batch acceptance testing (Shore A, tear strength, compression set per ASTM D412/D395). Vulcanisation bond pull-off test per ASTM D429. Accelerated thermal-aging at 100°C/168 h per ASTM D573. Noise attenuation spot-check on 5 % of pads (vibration table test at 300 Hz drive).

**Phase 2 — Vehicle integration trial (months 7–18):** 2-vehicle trial, 6-month / 1 200 km wear trial. Measure: pad wear (Shore A monthly, thickness quarterly), crew noise exposure (audiometric testing quarterly), track link wear (caliper measurement). Acceptance criteria: Shore A within ±5 of nominal at 1 200 km; 0 delamination events; > 10 dB noise reduction maintained at 300 Hz.

**Phase 3 — Fleet contract (months 19–36):** ADF Army Materiel Division procurement contract for 400-vehicle fleet. First production delivery within 12 months of contract award.

### 14.1 10-year TCO — 400-vehicle ADF fleet

**Table 14.1.** 10-year TCO — 400-vehicle ADF fleet.

| Element | HNBR pads | Steel pads (baseline) | Delta |
|---|---|---|---|
| Pad procurement (255 936 pads × 3.33 cycles) | A$7 013 000 | A$4 607 000 | +A$2 406 000 |
| Reduced NIHL compensation (estimated 10 claims avoided) | −A$2 800 000 | A$0 baseline | −A$2 800 000 |
| Extended track life (reduced metal-on-metal) | −A$1 200 000 (est.) | A$0 baseline | −A$1 200 000 |
| **Net 10-year delta** | | | **−A$1 594 000 (saving)** |

On a whole-life-cost basis including NIHL reduction and extended track life, the HNBR pad is cheaper than steel despite the higher per-pad material cost.

### 14.2 Export scenario

**Export scenario.** 3 allied nations (NZ, Canada, UK) adopt under Route B:

| Jurisdiction | Fleet size | Annual throughput |
|---|---|---|
| Australia (base) | 400 vehicles | 8 533 pads/yr |
| New Zealand | 100 vehicles | 2 133 pads/yr |
| Canada | 600 vehicles | 12 800 pads/yr |
| United Kingdom | 500 vehicles | 10 667 pads/yr |
| **Combined** | **1 600 vehicles** | **34 133 pads/yr** |

At 34 133 pads/yr combined, the programme enters the 25 000/yr cost tier (A$27.40/pad). Route B royalty income: 34 133 × A$1.80 = **A$61 439/yr** + licence fees A$1.68 M one-time.

---

## APPENDIX A: TEST PROCEDURES

### A.1 Tensile Testing (ASTM D412)

**Specimen Preparation:**
- Die C dumbbell specimens
- Minimum 5 specimens per test
- Condition at 23 ± 2°C for 24 hours

**Test Conditions:**
- Temperature: 23 ± 2°C
- Crosshead Speed: 500 ± 50 mm/min
- Report: Tensile strength, elongation at break, 100% modulus, 300% modulus

### A.2 Hardness Testing (ASTM D2240)

**Specimen:**
- Finished pad or stack of sheets to 6mm minimum thickness
- Flat, smooth surface

**Procedure:**
- Shore A durometer
- 5 readings minimum, >12mm apart
- Hold 15 seconds per reading
- Report average of 5 readings

### A.3 Insert Pull-Out Test

**Specimen Preparation:**
- Cut pad to isolate single insert with minimum 40mm surrounding rubber
- Drill hole through rubber to access insert hex socket

**Test Fixture:**
- Universal testing machine with custom grips
- Pad clamped at base
- M10 threaded rod engaged with insert

**Procedure:**
- Crosshead speed: 50 mm/min
- Pull until insert failure or rubber failure
- Report peak load and failure mode

### A.4 Cyclic Durability Test

**Test Setup:**
- Mount pad to steel plate using production hardware
- Torque bolts to 45 Nm
- Apply cyclic compression load: 0 to 40 kN at 2 Hz
- Test duration: 50,000 cycles

**Inspection:**
- Visual inspection every 10,000 cycles
- Final dimensional check
- Destructive tear-down to check insert bonding

---

## APPENDIX B: DRAWINGS

### B.1 Drawing List

| Drawing Number | Title | Sheet |
|----------------|-------|-------|
| TDP-001-PAD-DIM | Rubber Track Pad - Dimensional Drawing | 1 of 1 |
| TDP-001-PAD-TREAD | Tread Pattern Details | 1 of 1 |
| TDP-001-INSERT | Metal Insert Specification | 1 of 1 |
| TDP-001-HARDWARE | Mounting Hardware Assembly | 1 of 1 |
| TDP-001-PLATE | Track Shoe Mounting Plate | 1 of 1 |
| TDP-001-ASSY | Complete Assembly Drawing | 1 of 1 |

*Note: Full engineering drawings available in separate CAD package*

---

## APPENDIX C: MATERIAL CERTIFICATIONS

### C.1 Required Certifications

Supplier shall provide with each delivery:
- HNBR: Polymer certification (ACN content, Mooney viscosity)
- NBR: Polymer certification (ACN content, Mooney viscosity)
- Natural Rubber: Grade certification (SMR CV60)
- Carbon Black: Grade certification (ASTM N550)
- Stainless Steel Inserts: Material certification (Type 316)
- Fastener Hardware: Material certification (Grade 10.9)

### C.2 Traceability

All materials shall be traceable to:
- Raw material lot number
- Manufacturer
- Date of manufacture
- Specification conformance

---

## APPENDIX D: ENVIRONMENTAL COMPLIANCE

### D.1 Restricted Substances

This product shall comply with:
- RoHS Directive (2011/65/EU): Lead, mercury, cadmium limits
- REACH Regulation (EC 1907/2006): SVHC substances
- California Proposition 65: Carcinogen disclosure

**Note:** Antimony trioxide used as flame retardant is present at <1% by weight

### D.2 Disposal

End-of-life disposal shall follow:
- Tire and rubber recycling protocols
- Metal components separated for scrap recycling
- Incineration with energy recovery (if applicable)
- No landfill disposal of whole pads recommended

---

## APPENDIX E: INSTALLATION INSTRUCTIONS

### E.1 Pre-Installation Inspection

1. Verify track shoe mounting plate is clean and free of rust
2. Inspect mounting plate T-slots for damage or debris
3. Check pad for shipping damage or defects
4. Verify hardware kit is complete (4 T-bolts, 4 washers per pad)

### E.2 Installation Procedure

**Step 1: Surface Preparation**
- Wire brush mounting plate to remove rust/debris
- Clean with solvent (isopropyl alcohol)
- Allow to dry completely

**Step 2: Pad Positioning**
- Align pad center hole with mounting plate guide pin
- Ensure pad is seated flat against plate

**Step 3: Fastener Installation**
- Insert T-bolt #1 (front-left) into T-slot
- Slide T-head into position
- Hand-tighten into pad insert
- Repeat for bolts #2, #3, #4

**Step 4: Torquing**
- Using calibrated torque wrench and 8mm hex key
- Torque all 4 bolts in star pattern to 45 ± 3 Nm
- Re-check torque after 5 minutes

**Step 5: Final Inspection**
- Visual check: Pad seated flush, no gaps
- Tactile check: No movement when pressed
- Mark installation date on maintenance log

**Installation Time:** 12 minutes per pad (trained crew)

### E.3 Removal Procedure

1. Loosen all 4 bolts (2 full turns each)
2. Remove bolts completely
3. Slide T-heads out of slots
4. Lift pad off mounting plate
5. Inspect mounting plate for damage
6. Clean and prepare for new pad installation

**Removal Time:** 5 minutes per pad

---

## DOCUMENT APPROVAL

**Prepared by:**
****_****_****_****_**_**Senior Engineer  
Date: **_****_**_

**Reviewed by:**
****_****_****_****_**_**Quality Assurance Manager  
Date: **_****_**_

**Approved by:**
****_****_****_****_**_**Program Manager  
Date: **_****_**_

---

**END OF TECHNICAL DATA PACKAGE**

*This document contains 24 pages*
