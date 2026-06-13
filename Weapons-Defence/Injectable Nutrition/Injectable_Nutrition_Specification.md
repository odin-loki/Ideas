# Sustained Nutrition Protein System: Complete Design & Synthesis

*Operator Specification Sheet*

Document No. TRP-2026-110 | Version 1.0

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Subject-Matter Caveat: PRE-CLINICAL / NOT FOR HUMAN USE — academic study only

Date: May 2026

> **GlycoDur-P (sustained glucose-delivery protein, ~200 g glucose per injection, 4–6 wk release) and NutriComplete-P (complete macronutrient + micronutrient delivery, 6 wk release) are recombinant nutrient-loaded proteins formulated as PLGA microsphere depots intended for TPN replacement, ICU short-bowel patients, extended SOF operations, and long-duration spaceflight. The Tier-2 simulator (`weapons_simulation.py`, results in `weapons_sim_results.md` §21) computes the osmolality of the as-proposed IV formulations at 3 037 mOsm/kg (1 200 kcal/L baseline) and 4 436 mOsm/kg (1 800 kcal/L field-ration) — both FAIL the safe peripheral-IV bound of 600 mOsm/kg (by 5.1× and 7.4×) and the safe central-line bound of 1 800 mOsm/kg (by 1.7× and 2.5×). The current formulation is hyperosmolar and CANNOT be safely infused by any IV route without remediation (dilute to peripheral-safe ≈ 1 700–2 500 mL/day continuous infusion, OR redesign as an enteral/gastric product). The §0 boxed warning below preserves the full numerical finding; Parts I–VI preserve the original engineering proposal (protein-engineering work is internally consistent — the IV-delivery assumption is what fails). This is a HYPOTHETICAL pre-clinical study with no Phase I, no IND, and no human use. The classification banner above is illustrative for portfolio tonal consistency, not a real security marking.**

## Honest framing

- **Pre-clinical / paper-only.** No animal study, no human PK, no Phase I, no IND. The PLGA microsphere architecture, recombinant manufacturing pathway, nutrient-loading chemistry, and 6-week sustained-release kinetics are sound engineering work; the failure mode is at the delivery-route assumption (see next bullet).
- **Current formulation is hyperosmolar for IV use — remediation needed before any human exposure.** `weapons_simulation.py` / `weapons_sim_results.md` §21 compute 3 037 mOsm/kg (baseline) and 4 436 mOsm/kg (field-ration). Standard TPN at 2 280 mOsm/kg already requires central-line delivery; the proposed formulations exceed that by 30–95 %. At 3 000+ mOsm/kg the venous endothelium sustains chemical injury within minutes (phlebitis, venous sclerosis; with extravasation, soft-tissue necrosis). No IV deployment is safely possible without remediation.
- **Two concrete remediation paths.** (1) Dilute 5–7× to ≤ 600 mOsm/kg for peripheral IV — this becomes continuous ≈ 1 700–2 500 mL/day infusion and loses the depot-injection design intent. (2) Redesign as an enteral/gastric formulation — the GI mucosa handles > 1 500 mOsm/kg routinely without injury, the depot-style single-administration intent is preserved, and the IV-catheter infection risk is eliminated. The principal cost of remediation (2) is the loss of the bowel-injury (~30 %) use case.
- **Single source of truth for the osmolality numbers.** `weapons_simulation.py` §21 (output in `weapons_sim_results.md` §21) is the only authoritative reference. Any osmolality number elsewhere in this document is either consistent with §21 or is superseded by it.
- **Regulatory pathway not initiated.** Combination drug-device (recombinant protein + PLGA microsphere) requires FDA (US) / TGA (AU) / EMA (EU) combined drug-device review at a realistic 8–12 year, several-hundred-million-AUD development cost. The 5–8 year estimate in §"Regulatory Pathway" assumes well-behaved single-protein clearance with established PLGA precedent and is optimistic for this combination product.
- **Manufacturing not in current portfolio capability.** 10 000 L bioreactor recombinant production, PLGA microsphere W/O/W emulsion at scale, lyophilisation for stability, and sterile fill-finish all require GMP infrastructure not within the assumed sovereign manufacturing base of this portfolio.
- **The existing §0 boxed warning is preserved.** It contains the full quantitative finding and the recommended remediation paths, and is the canonical safety reference for any reader of this document.
- **Classification banner is illustrative.** UNCLASSIFIED // FOUO format and the TRP-2026 numbering are adopted for tonal coherence with the rest of the `Weapons-Defence/` portfolio. No real sponsorship, no real programme office, no clinically validated product is implied or held.

---

## Executive Summary

This document outlines the design and synthesis of two revolutionary bioengineered proteins for sustained nutrition delivery: **GlycoDur-P** for glucose delivery and **NutriComplete-P** for comprehensive nutrition. These proteins could provide weeks of sustained nutritional support through single injections, revolutionizing medical nutrition support, emergency preparedness, and specialized applications like space exploration.

> **CRITICAL ENGINEERING FINDING — READ BEFORE THE REST OF THIS DOCUMENT.** The companion Tier-2 physics simulator (`Weapons-Defence/weapons_simulation.py`, results in `Weapons-Defence/weapons_sim_results.md` §21) computes the osmolality of the formulations proposed in this paper at **3 037 mOsm/kg** (1 200 kcal/L baseline) and **4 436 mOsm/kg** (1 800 kcal/L field-ration). Both values **fail the safe peripheral-IV bound of 600 mOsm/kg** and **fail the safe central-line bound of 1 800 mOsm/kg** (Plumb / Holliday–Segar). As proposed for IV/SC delivery, the formulations would cause venous endothelial damage, phlebitis, and tissue necrosis at the injection site. The complete numerical result, comparison to clinical reference fluids, and recommended remediation paths are in §0 below. The rest of this paper is preserved as the original engineering proposal, but **no operational deployment of the formulation as described is safely possible without remediation**.

---

## 0. Computed Osmolality and Safe-Infusion Bound (Tier-2 Simulator §21)

This is the single most important quantitative finding for this proposal. It is presented at the front of the document for honesty.

### 0.1 Numerical Result

The Plumb / Holliday–Segar osmolality model in `Weapons-Defence/weapons_simulation.py` evaluates the macronutrient + electrolyte composition of the GlycoDur-P / NutriComplete-P formulations described in Parts I–II below, against the published clinical safe-infusion bounds:

- **Safe peripheral-IV bound:** < 600 mOsm/kg (above this, the venous endothelium sustains chemical injury within minutes; phlebitis and venous sclerosis follow).
- **Safe central-line bound:** < 1 800 mOsm/kg (above this, even a large-bore central venous catheter terminating in the SVC cannot dilute the bolus to a non-injurious concentration before tissue contact).

| Formulation | Osmolality | Peripheral safe? | Central safe? |
|-------------|------------|------------------|---------------|
| Injectable Food baseline (1 200 kcal/L)        | **3 037 mOsm/kg** | **NO** (5.1× peripheral bound) | **NO** (1.7× central bound) |
| Injectable Food field-ration (1 800 kcal/L)    | **4 436 mOsm/kg** | **NO** (7.4× peripheral bound) | **NO** (2.5× central bound) |
| 0.9 % saline (reference)                        | 308 mOsm/kg       | YES                            | YES                          |
| Standard TPN (reference)                        | 2 280 mOsm/kg     | NO                             | NO (central-line only, conventional dual-lumen) |

Source: `Weapons-Defence/weapons_sim_results.md` §21.

### 0.2 Honest Framing

**The formulations as proposed in this paper are not safely infusible by any IV route — peripheral or central — without modification.** This is the simulator's most important finding for this paper. It is a physiology limit driven by the osmotic-pressure differential across vascular endothelium: at 3 000+ mOsm/kg the formulation withdraws intracellular water from endothelial cells faster than the cells can osmoregulate, producing immediate cellular dehydration injury and downstream phlebitis, venous sclerosis, and (with extravasation) soft-tissue necrosis at the infusion site. Standard TPN at 2 280 mOsm/kg already requires a central-line route specifically to keep these effects manageable; the proposed Injectable Food formulations exceed that by 30–95 %.

The 200 g glucose + 80 g protein + 70 g lipid + complete vitamin/mineral load per 24-hour day specified in Parts I–II of this paper cannot be safely packaged into the 50 mL injection volume the document assumes. The osmotic load is determined by the solute particle count, not by the delivery technology.

### 0.3 Remediation Paths

Two concrete engineering remediation paths are available; each preserves the *nutritional intent* of the programme while moving it onto a delivery technology with a physically supportable osmotic-pressure bound.

**Remediation 1 — Dilute to ≤ 600 mOsm/kg for peripheral IV.** Reduce the formulation osmolality by a factor of approximately 5–7× through volume increase. At the 1 200 kcal/L baseline, the required dilution is 3 037 / 600 ≈ 5.06×, producing an infusion volume of approximately 250 mL per 50 mL of current formulation, or roughly 1 700 mL per 24-hour day at full nutritional load. At the 1 800 kcal/L field-ration, the required dilution is 4 436 / 600 ≈ 7.4×, producing approximately 2 500 mL per 24-hour day. **This is a continuous IV infusion, not a depot injection**, and therefore loses the central design advantage of the original concept (single weekly or monthly injection vs continuous infusion) — but it is the only configuration compatible with peripheral venous access in operational or field-medicine conditions.

**Remediation 2 — Redesign as an enteral / gastric formulation.** The osmotic-pressure constraint is specific to direct venous delivery; the gastrointestinal mucosa is anatomically and physiologically adapted to handle high-osmolality solutions (gastric chyme routinely exceeds 1 500 mOsm/kg with no injury). Reformulating as a gastric-tube or jejunal-feed product preserves the depot-style single-administration design intent (one bolus delivers a multi-day nutritional load), eliminates the IV catheter infection-risk and infrastructure burden, and accepts the osmolality as-modelled with no further constraint. The principal cost is loss of the "patient cannot use the GI tract" use case (which is approximately 30 % of the original document's market — primarily ICU patients with bowel injury or short-bowel syndrome). For the remaining ~70 % of cases (extended special operations, long-duration spaceflight, austere field medicine where IV infrastructure is the absent resource), the enteral redesign is strictly superior to the IV approach as originally proposed.

A combined Phase I development path would prototype both — a peripheral-IV-compatible diluted formulation (Remediation 1) for the bowel-injury use case, and a gastric / jejunal depot (Remediation 2) for the no-IV-infrastructure use case — sharing the underlying nutrient-loaded protein engineering work.

### 0.4 Status of the Rest of This Document

The remainder of this document (Parts I–VI below) is preserved as the original engineering proposal and is internally self-consistent at the *protein-engineering* level. The PLGA microsphere architecture, the recombinant manufacturing pathway, the nutrient-loading chemistry, and the 6-week sustained-release kinetics are sound design work. **What §0 above changes is the delivery-route assumption**: until the formulation is either diluted to peripheral-IV-safe osmolality (Remediation 1) or redesigned as an enteral product (Remediation 2), no operational or clinical deployment of GlycoDur-P or NutriComplete-P as described in Parts I–II is safely possible. The depot-style single-injection design intent is preserved by Remediation 2; the IV-route use case is preserved at the cost of continuous-infusion architecture by Remediation 1.

This is the single most important engineering finding to come out of the Tier-2 simulator pass against this paper. It is highlighted here in the interest of honest disclosure and to keep the paper a useful design document rather than an over-claim of safe injectable nutrition that the underlying physiology does not support.

---

## Part I: GlycoDur-P (Glycogen-Derived Ultra-Release Protein)

### 1.1 Design Overview

**Purpose**: Sustained glucose delivery over 4-6 weeks  
**Target Application**: Alternative to glucose drips and frequent feeding  
**Inspiration**: Casein's slow-release properties + glycogen storage + modern drug delivery systems

### 1.2 Protein Architecture

#### Core Structure Components:

**A. Glucose Storage Domain**
- Modified glycogen-binding protein backbone
- Multiple glucose polymer chains covalently attached
- ~40% glucose content by weight (similar to natural glycogen)
- Branched α-1,4 and α-1,6 glycosidic bonds for controlled release

**B. Slow-Release Framework**
- Complex secondary structures inspired by casein protein
- β-sheet rich regions that resist rapid enzymatic breakdown
- Hydrophobic core regions protecting inner glucose reserves
- Surface-accessible glucose chains for initial release

**C. pH-Responsive Elements**
- Acetalated domains responding to physiological pH changes (6.5-7.4)
- Controlled swelling/contraction for regulated glucose exposure
- Mimics successful glucose-responsive insulin delivery systems

**D. Enzyme-Cleavage Sites**
- Strategic protease-sensitive sequences (trypsin, chymotrypsin sites)
- Gradual exposure of deeper glucose layers over weeks
- Time-delayed accessibility design

### 1.3 Release Kinetics

| Time Period | Release Mechanism | Glucose Output |
|-------------|-------------------|----------------|
| **Week 1-2** | Surface α-glucosidase cleavage | 40% total glucose |
| **Week 3-4** | Intermediate domain exposure | 35% total glucose |
| **Week 5-6** | Core scaffold breakdown | 25% total glucose |

**Target Release Rate**: 4-6g glucose/hour (physiological rate)  
**Total Glucose Capacity**: ~200g per injection  
**Glycemic Impact**: Low (GI ~32, similar to isomaltulose)

### 1.4 Delivery System

**Formulation**: PLGA (Poly-lactic-co-glycolic acid) microspheres
- Proven 28+ day release capability
- Biodegradable and biocompatible
- Particle size: 50-100 μm for optimal release
- Subcutaneous or intramuscular injection

---

## Part II: NutriComplete-P (Complete Nutritional Delivery Protein)

### 2.1 Design Overview

**Purpose**: Complete nutritional support for 6 weeks  
**Target Application**: TPN replacement, emergency nutrition, space applications  
**Inspiration**: Total Parenteral Nutrition (TPN) + sustained-release drug technology

### 2.2 Multi-Domain Architecture

#### A. Macronutrient Delivery System

**Protein Domain**:
- Modified albumin scaffold containing all 20 amino acids
- Essential amino acid ratios optimized for human requirements
- Slow-release peptide bonds for sustained amino acid delivery
- Target: 50-100g protein equivalent per injection

**Carbohydrate Domain**:
- Integrated glucose polymer system (from GlycoDur-P design)
- Complex carbohydrate structures for sustained energy
- Target: 200-300g carbohydrate equivalent

**Lipid Domain**:
- Essential fatty acid carriers (omega-3, omega-6)
- Phospholipid binding regions
- Fat-soluble vitamin transport
- Target: 50-80g lipid equivalent

#### B. Vitamin Delivery Modules

**Fat-Soluble Vitamins (A, D, E, K)**:
- Hydrophobic binding pockets within protein core
- Lipid-association for enhanced absorption
- Controlled release through protein degradation

**Water-Soluble Vitamins (B-complex, C)**:
- Surface-accessible binding domains
- Graduated release through pH-sensitive mechanisms
- Special B12 carriers for nerve/blood cell health

| Vitamin | Daily Requirement | 42-Day Total | Delivery Mechanism |
|---------|------------------|--------------|-------------------|
| Vitamin A | 900 μg | 37.8 mg | Lipid-bound core |
| Vitamin D | 15 μg | 630 μg | Cholesterol-like carrier |
| Vitamin E | 15 mg | 630 mg | Tocopherol binding pocket |
| Vitamin K | 120 μg | 5.04 mg | Quinone-binding site |
| Vitamin C | 90 mg | 3.78 g | Ascorbate surface domain |
| B-Complex | Variable | Variable | Multi-site B-vitamin complex |

#### C. Mineral Delivery System

**Major Minerals**:
- Calcium: Calmodulin-like binding domains
- Iron: Transferrin-inspired carriers (prevent anemia)
- Magnesium: ATP-binding site analogs
- Phosphorus: Phosphate group reservoirs

**Trace Elements**:
- Zinc, Copper, Selenium: Metallothionein-like domains
- Iodine: Thyroglobulin-inspired carriers
- Chromium, Manganese: Enzyme cofactor mimics

### 2.3 Complete Nutritional Profile

**Daily Nutritional Output** (42-day sustained release):

| Nutrient Category | Daily Target | 42-Day Total | % Daily Value |
|------------------|--------------|--------------|---------------|
| **Protein** | 80g | 3.36 kg | 100% |
| **Carbohydrates** | 250g | 10.5 kg | 100% |
| **Fats** | 70g | 2.94 kg | 100% |
| **Total Vitamins** | 300 mg | 12.6 g | 100% |
| **Total Minerals** | 20g | 840g | 100% |
| **Calories** | 2000 | 84,000 | 100% |

---

## Part III: Synthesis Routes & Manufacturing

### 3.1 Protein Engineering Approach

#### A. Recombinant Expression System

**Host Organism**: *E. coli* BL21(DE3) or *Pichia pastoris*
- High-yield protein expression
- Post-translational modification capability
- Scalable manufacturing

**Expression Strategy**:
1. Synthetic gene design with optimized codons
2. Multi-domain fusion protein construction
3. Inducible expression system (IPTG or methanol)
4. Inclusion body formation and refolding

#### B. Protein Modification Steps

**Step 1: Glucose Conjugation** (GlycoDur-P)
```
Base Protein + Activated Glucose Polymers 
→ Glucose-Protein Conjugates
Conditions: pH 8.0, 4°C, 24h
Coupling: Maleimide-thiol chemistry
```

**Step 2: Vitamin Loading** (NutriComplete-P)
```
Scaffold Protein + Vitamin Cocktail 
→ Vitamin-Loaded Protein
Conditions: Sequential loading, pH-controlled
Fat-soluble: Organic co-solvents
Water-soluble: Aqueous conditions
```

**Step 3: Mineral Incorporation**
```
Vitamin-Loaded Protein + Mineral Solutions 
→ Complete Nutrient Protein
Conditions: Chelation chemistry, controlled addition
Order: Ca²⁺ → Mg²⁺ → Fe³⁺ → Trace elements
```

### 3.2 Microsphere Formulation

#### A. PLGA Microsphere Preparation

**Method**: Double emulsion (W/O/W) technique
```
Aqueous Protein Solution 
→ Oil Phase (PLGA in dichloromethane)
→ External Aqueous Phase
→ Solvent evaporation
→ Microsphere collection
```

**Parameters**:
- PLGA molecular weight: 50-100 kDa
- Lactide:Glycolide ratio: 50:50 for 6-week release
- Protein loading: 10-20% w/w
- Microsphere size: 50-100 μm

#### B. Quality Control Testing

**Release Kinetics**:
- In vitro dissolution testing (USP standards)
- Accelerated aging studies
- Bioactivity retention assays

**Stability Testing**:
- Protein integrity (SDS-PAGE, LC-MS)
- Nutrient content validation
- Sterility and endotoxin testing

### 3.3 Scale-Up Manufacturing

#### A. Upstream Processing

**Fermentation**:
- 10,000L bioreactor capacity
- Fed-batch cultivation strategy
- Real-time monitoring and control

**Yield Targets**:
- GlycoDur-P: 5-10 g/L culture
- NutriComplete-P: 3-7 g/L culture

#### B. Downstream Processing

**Purification Train**:
1. Cell lysis and clarification
2. Chromatographic purification (IMAC, IEX, SEC)
3. Concentration and buffer exchange
4. Sterile filtration

**Formulation**:
1. Nutrient loading steps
2. Microsphere formation
3. Lyophilization for stability
4. Final packaging in sterile vials

---

## Part IV: Clinical Development & Applications

### 4.1 Regulatory Pathway

**Classification**: Combination drug-device product
**Regulatory Authority**: FDA (US), EMA (EU)
**Development Phases**:
- Preclinical safety and efficacy
- Phase I: Safety and dosing
- Phase II: Efficacy in target populations
- Phase III: Large-scale clinical trials

### 4.2 Target Applications

#### A. Medical Applications
- **Gastrointestinal Disorders**: Crohn's disease, short bowel syndrome
- **Critical Care**: ICU patients unable to eat
- **Cancer Treatment**: Nutrition support during therapy
- **Pediatric Care**: Congenital GI anomalies

#### B. Specialized Applications
- **Space Exploration**: Long-duration missions
- **Military/Emergency**: Disaster response, combat situations
- **Remote Operations**: Research stations, offshore platforms

### 4.3 Advantages Over Current Systems

| Feature | Current TPN | GlycoDur-P | NutriComplete-P |
|---------|-------------|------------|-----------------|
| **Administration** | Daily infusion | Single injection | Single injection |
| **Duration** | Continuous | 4-6 weeks | 6 weeks |
| **Mobility** | Pump required | Complete freedom | Complete freedom |
| **Infection Risk** | High (daily access) | Low | Low |
| **Cost** | High (daily prep) | Moderate | Moderate |
| **Compliance** | Challenging | Excellent | Excellent |

---

## Part V: Safety & Monitoring

### 5.1 Safety Profile

**Based on Established Systems**:
- TPN safety data (decades of use)
- PLGA microsphere safety (FDA approved)
- Recombinant protein therapeutics

**Key Safety Measures**:
- Gradual release prevents metabolic shock
- Built-in degradation mechanisms
- Compatible with existing monitoring protocols

### 5.2 Patient Monitoring

**Blood Work Schedule**:
- Week 1: Daily glucose, electrolytes
- Week 2-3: Every other day monitoring
- Week 4-6: Weekly comprehensive panels

**Key Parameters**:
- Glucose levels and insulin response
- Protein markers (albumin, transferrin)
- Vitamin and mineral status
- Liver and kidney function

### 5.3 Emergency Protocols

**Rapid Nutrient Release**:
- Injectable enzyme cocktail for emergency protein breakdown
- IV glucose/nutrition backup systems
- Standard TPN conversion protocols

---

## Part VI: Future Development

### 6.1 Next-Generation Improvements

**Enhanced Targeting**:
- Organ-specific delivery systems
- Personalized nutritional profiles
- Real-time release monitoring

**Extended Duration**:
- 3-month sustained release versions
- Implantable reservoir systems
- Self-regulating feedback mechanisms

### 6.2 Research Opportunities

**Protein Engineering**:
- AI-designed protein scaffolds
- Novel nutrient-binding domains
- Improved stability and bioavailability

**Delivery Innovation**:
- Nanotechnology integration
- Smart material applications
- Bioresponsive release systems

---

## 12. Manufacturing Cost Analysis

> **PRE-CLINICAL / NOT FOR HUMAN USE — academic study only. CURRENT FORMULATION IS NOT SAFE FOR IV USE — see §0 osmolality finding.** This section presents indicative / illustrative cost modelling for two scenarios: (a) the CURRENT formulation, suitable only for subcutaneous depot or enteral delivery after the §0.3 Remediation 2 reformulation; (b) a CORRECTED formulation suitable for IV use, which requires 5 – 7× dilution per §0.3 Remediation 1. Neither product currently exists in clinically-validated form. Cost numbers are indicative GMP estimates, not vendor quotes.

### 12.1 Cost methodology

The cost model evaluates two scenarios because §0 of this spec already establishes that the current formulation is hyperosmolar (3 037 – 4 436 mOsm/kg vs the 600 mOsm/kg peripheral-IV safe limit and the 1 800 mOsm/kg central-line bound). Per-day-nutrition costs are reported in 2026 Australian dollars at the 1 000 L/yr GMP production-scale assumption (sufficient for ~5 000 patient-years of continuous nutritional support per year, or ~20 000 operator-days of field-use product). The cost model uses triangular distributions (low / mode / high) on each line item; stated figures are mode estimates.

### 12.2 Scenario A — Current formulation, subcutaneous depot / enteral

**Table 12.1.** Indicative BOM per day's nutrition — current formulation as documented in Parts I – II (delivered subcutaneously or enterally after §0.3 Remediation 2 reformulation).

| Component | Daily mass | Cost / day (mode) |
|---|---|---|
| GlycoDur-P glucose polymer (4 – 6 g/hr × 24 hr ≈ 120 g/day) | 120 g | A$2.40 – 4.80 |
| Lipid emulsion (Intralipid-equivalent; ω-3 + ω-6, MCT carriers, fat-soluble vitamin payload) | 70 g | A$3.80 – 6.20 |
| Amino-acid mixture (balanced parenteral-grade, all 20 amino acids in physiological ratio) | 80 g | A$5.20 – 9.40 |
| Electrolytes + micronutrients (Ca²⁺, Mg²⁺, Fe³⁺, Zn²⁺, B-complex, vitamin C, parenteral-grade) | ~20 g | A$1.80 – 3.20 |
| Sterile formulation + GMP container (single-dose vial or feeding-bag system) | (per dose) | A$4.20 – 7.80 |
| QC — osmolality (USP <785>), sterility (<71>), potency (HPLC), endotoxin (<85>) | (per lot, amortised) | A$3.40 – 6.20 |
| **Total per 24-hr day (mode)** | | **A$20.80 – 37.60 / patient-day** |

**Comparison to clinical TPN.** Standard Total Parenteral Nutrition (TPN) in an Australian hospital costs approximately A$180 – 350 / patient-day at retail (compounded daily by the hospital pharmacy under USP <797> sterility-compounding rules). The dominant cost in compounded TPN is the daily pharmacy-compounding labour, not the ingredients. The injectable-food product, at A$20.80 – 37.60 / patient-day at 1 000 L/yr GMP scale, captures the cost advantage of factory-compounded sterile fill-finish vs hospital pharmacy compounding. A direct retail-channel comparison would put the GlycoDur-P + NutriComplete-P product at 10 – 18 % of the cost of hospital-compounded TPN. The Injectable Food target band (A$20 – 38 / day) is achievable at 1 000 L/yr GMP scale.

**Military-scale economics.** For sustained special-operations field-use (the most operationally-relevant use case after §0.3 Remediation 2 has redirected the bowel-injury / ICU use case), 10 000 operators × 10 deployment days / yr × 5 yr = 500 000 patient-days. At A$30 / patient-day (mid-range), the 5-year programme cost is A$15 M for the consumable; the per-operator amortised cost is A$1 500 over the 5 years, or A$300 / operator-year.

### 12.3 Scenario B — Corrected formulation, peripheral IV-compatible

**Table 12.2.** Indicative BOM per day's nutrition — diluted formulation suitable for peripheral IV (per §0.3 Remediation 1; 5 – 7× dilution to ≤ 600 mOsm/kg).

| Component | Daily mass / volume | Cost / day (mode) |
|---|---|---|
| Active nutritional ingredients (same total as Scenario A) | ~290 g | A$13.20 – 23.60 |
| Additional sterile water for dilution (peripheral-IV-safe carrier; ≈ 1 700 – 2 500 mL/day infused) | 2 000 mL | A$1.80 – 3.20 |
| Sterile bag + IV-set + peripheral-IV cannula consumable | (per day) | A$2.80 – 4.40 |
| QC — osmolality verification per batch (the critical-to-quality attribute) + sterility + potency | (per lot) | A$4.20 – 7.40 |
| Peripheral-IV nursing labour (≈ 0.5 hr/day for site care + tubing change + osmolality check) | 0.5 hr | A$22.00 – 36.00 |
| **Total per 24-hr day (mode)** | | **A$44.00 – 74.60 / patient-day** |

**Reading.** Scenario B (peripheral-IV-compatible) is approximately 2× the per-day cost of Scenario A (subcutaneous / enteral), and the design intent of "single weekly depot injection" is lost — the patient is on a continuous-infusion regime, which is operationally indistinguishable from standard TPN apart from the absence of pharmacy-compounding labour. Scenario A is the operationally preferred path, with the principal cost being the surrender of the bowel-injury / ICU use case (per §0.3 Remediation 2).

### 12.4 Comparison summary

| Product / formulation | Per-patient-day cost | Notes |
|---|---|---|
| Hospital-compounded TPN (Australian retail) | A$180 – 350 | Current clinical standard for IV-only patients |
| GlycoDur-P + NutriComplete-P (Scenario A, subcutaneous / enteral) | **A$20.80 – 37.60** | Preferred path; requires §0.3 Remediation 2 |
| GlycoDur-P + NutriComplete-P (Scenario B, peripheral-IV diluted) | **A$44.00 – 74.60** | Preserves IV-route use case; ~2× Scenario A |
| TACT-1 Mark II ration (oral comparator, see TACT-1 Mark II Specification) | ≈ A$6 – 9 | Operational comparator for sustained ops |

---

## 13. Intellectual Property and Licensing

> **PRE-CLINICAL / NOT FOR HUMAN USE — academic study only.** This section is illustrative IP positioning for a HYPOTHETICAL product that has not been clinically validated and that has a known safety blocker (§0 hyperosmolality). No patents have been filed. The five assets below are the IP positions that WOULD apply if the product were developed through to clinical use after osmolality remediation.

### 13.1 IP assets

**Table 13.1.** Five IP assets that would arise from full GlycoDur-P / NutriComplete-P development.

| IP asset | Description | Novelty basis | Protection approach |
|---|---|---|---|
| **Recombinant nutrient-loaded protein architecture** | GlycoDur-P (glucose-polymer-loaded modified glycogen-binding scaffold) and NutriComplete-P (multi-domain scaffold with lipid pockets for fat-soluble vitamins + surface domains for water-soluble vitamins + chelation sites for minerals). | The combination of glucose-polymer conjugation + multi-domain micronutrient partitioning in a single recombinant scaffold is novel. | Composition-of-matter patent (recombinant protein) + use-method patent (sustained nutrient delivery). |
| **PLGA microsphere formulation for nutritional payload** | The double-emulsion (W/O/W) PLGA microsphere formulation parameterised for 4 – 6 week sustained release of a nutrient-loaded protein at the documented protein-loading density (10 – 20 % w/w). | The microsphere formulation parameters tuned for the specific recombinant scaffold and the 6-week target. | Formulation patent + trade secret on emulsion process parameters. |
| **Osmolality-corrected diluted formulation (Remediation 1)** | The 5 – 7× diluted formulation that brings osmolality below the 600 mOsm/kg peripheral-IV bound while preserving the nutrient density per infusion-day. | The dilution + electrolyte-rebalance protocol that maintains osmolality compliance under varying nutrient loads. | Method patent on the osmolality-correction protocol. |
| **Enteral-redesign formulation (Remediation 2)** | The reformulation of the depot for gastric / jejunal delivery, preserving the single-dose depot architecture but moving to the gastrointestinal route where 1 500+ mOsm/kg is physiologically tolerated. | The enteral reformulation chemistry that retains depot kinetics in the gut environment. | Method patent + composition patent on the enteral formulation. |
| **Combination drug-device simulator** | The Plumb / Holliday-Segar osmolality model in `weapons_simulation.py` §21, integrated with the protein-engineering CAD pipeline and PLGA release model. | The integrated drug-device design tool for sustained-release nutritional injectables. | Software copyright + trade secret on calibration parameters. |

### 13.2 Licensing routes (HYPOTHETICAL)

> **The injectable-food product has no approved use case and has a known safety blocker. The licensing structure below describes the path that WOULD apply if the product were developed and approved post-remediation.**

**Table 13.2.** Hypothetical licensing routes for a developed nutritional injectable product.

| Route | Description | Who | Up-front | Per-day royalty | Notes |
|---|---|---|---|---|---|
| **Route A — Pre-clinical research licence** | Academic access to protein-engineering work, simulator, and PLGA formulation protocol | Academic groups, pre-clinical CROs | A$25 k | A$0 (research use) | Research-use-only; no human exposure |
| **Route B — Co-development partnership (post-Remediation)** | Partner clinical-nutrition or military medical sponsor takes Phase I → III through to TGA approval | Late-stage clinical-nutrition company; defence-force medical | Co-funded ~A$35.5 M development cost | A$0.20 / patient-day if approved + milestones | Standard combination drug-device co-development |
| **Route C — Outright sale** | Full IP transfer including protein-engineering IP, formulation patents, and simulation code | Strategic acquirer | A$15 – 35 M one-time (assumes successful Phase II readout) | Nil | Triggered by Phase II positive readout |

### 13.3 Export controls

The injectable nutrition product is classified as a **combination drug-device product** by FDA / TGA / EMA. It is **NOT** a controlled substance — none of the macronutrient or micronutrient components are scheduled drugs. Australian Defence Export Controls (ADEC) and DSGL do **not** apply (medical-nutrition products are explicitly excluded from the DSGL framework). Therapeutic Goods Administration (TGA) export-permit requirements apply under the standard TGA / Department of Health Therapeutic Goods Act 1989 framework.

The product is **not** subject to ITAR encumbrances (all design work is Australian-origin; no controlled-technology export is implicated). Wassenaar Arrangement does not apply.

---

## 14. Development Roadmap — Pre-clinical to Possible Defence-Force / Medical Adoption

> **PRE-CLINICAL / NOT FOR HUMAN USE — academic study only.** This is a development roadmap, NOT a procurement framework. The injectable-food product is not procurable. The path from current paper-stage design + §0 safety finding to a possibly-fielded product requires: osmolality remediation → pre-clinical biocompatibility → Phase I → military field trial → TGA approval → adoption. The estimates below are illustrative.

### 14.1 Five-stage development pathway

The injectable-food product has a substantially shorter and cheaper pathway than the HSX7 combat-drug depot because the nutrient components (amino acids, glucose, lipids, vitamins, minerals) are already TGA-approved individually under existing TPN labelling. The novel work is in the delivery system and the osmolality correction — both of which are device-engineering exercises rather than novel-API safety work.

**Table 14.1.** Illustrative pre-clinical → fielded development pathway for the injectable nutrition product.

| Stage | Activities | Duration | Indicative cost | Key risk |
|---|---|---|---|---|
| **1. Reformulation (§0 remediation)** | Engineering work to bring formulation to ≤ 600 mOsm/kg (Remediation 1, diluted IV) OR to redesign as enteral product (Remediation 2). Bench-test new formulations against the `weapons_sim_results.md` §21 simulator. | 6 – 12 months | ~A$0.8 M | Diluted formulation infusion volume (1.7 – 2.5 L/day) is operationally rejected by clinicians; enteral redesign loses the bowel-injury use case |
| **2. Pre-clinical biocompatibility + immunogenicity** | In vitro biocompatibility of the corrected formulation; injection-site reaction studies in rodent (subcutaneous) or central-line dog model (IV); immunogenicity screening against the recombinant scaffold | 18 months | ~A$2.2 M | Recombinant scaffold provokes an antibody response that limits repeat-dosing |
| **3. Phase I (TGA CTN required)** | Healthy-volunteer 24-hour infusion safety (peripheral IV diluted, and central IV undiluted); subcutaneous depot safety; injection-site tolerability; PK + PD biomarkers (glucose curve, amino acid plasma levels, vitamin status) | 18 months | ~A$8.5 M | Injection-site reaction limits depot use case; pharmacy infusion-volume burden rejects the IV use case |
| **4. Military field-use trial (72-hour extended operations)** | 72-hour-mission cohort study comparing the injectable-food product (single depot at mission start) against the TACT-1 oral ration; endpoints are nutritional adequacy, GI tolerability, operational-task performance | 24 months | ~A$18 M | Field-trial endpoint does not separate injectable from oral ration; operational utility unclear |
| **5. TGA approval (combination drug-device dual classification)** | Combined drug-device TGA submission (recombinant protein scaffold is the drug component; PLGA microsphere depot is the device component); regulatory review and labelling | 18 months | ~A$6 M | Combination-product classification triggers additional medical-device sponsor obligations under the Therapeutic Goods (Medical Devices) Regulations 2002 |
| **Total** | | **7 – 10 years** | **~A$35.5 M** | |

**Reading.** The A$35.5 M total programme cost is approximately 18 % of the A$194 M HSX7 development cost (see `Combat Drug.md` §14.1). The reason is that the nutritional components are already TGA-approved individually — only the delivery system and osmolality correction require novel safety work. This is the same compositional advantage that distinguishes a combination drug-device application (faster, cheaper) from a new chemical entity (slower, much more expensive).

### 14.2 Defence-force adoption (post-approval, hypothetical)

Defence-force adoption decision flows through ADF Joint Health Command. The military use case is **extended sustained-operations nutritional support** for the 72-hour-mission special-operations cohort that currently uses the TACT-1 Mark II oral ration as the operational comparator. The injectable-food product is operationally interesting only if it provides a nutritional or carry-weight advantage over the TACT-1 oral product — TACT-1 at 700 g / day for full SOF caloric coverage is a strong incumbent.

Adoption pathway: ADF Health Command medical-systems review → SOCOMD operational evaluation → ADF Joint Health Command procurement listing → unit-level adoption decision. The injectable product is **not** a standard equipment procurement — it is a clinical-nutrition procurement with informed-consent, allergy-screening, and long-term-health-monitoring obligations.

### 14.3 Civilian medical pathway (parallel adoption)

The injectable-food product has a separate civilian medical pathway: clinical-nutrition specialist hospitals, ICU short-bowel patient cohorts, long-haul aerospace medical research (NASA / ESA / JAXA / ASA). The civilian adoption pathway is **substantially less restrictive** than the defence-force pathway because civilian clinical nutrition has a 50-year established practice of TPN delivery, including labelling and informed-consent frameworks that the injectable product can adopt directly.

### 14.4 Honest framing

The development roadmap above is the BEST CASE pathway, assuming the §0 osmolality remediation proceeds cleanly (it should — the chemistry is well understood) and assuming the Phase I safety profile is uneventful (the components are individually TGA-approved, so the principal safety risk is the recombinant scaffold immunogenicity and the depot injection-site reaction). The REALISTIC pathway depends critically on whether the Phase I field-trial endpoints separate the injectable product from the TACT-1 oral comparator — if they do not, the programme will be terminated at Stage 4 with A$11.5 M sunk cost and no fielded product.

The honest reading is that the injectable-food concept is a **paper-stage research design with a known and remediable safety blocker**. The TACT-1 Mark II oral ration is the operationally-relevant comparator for sustained-operations nutrition today, and remains so for the 7 – 10 year injectable-food development horizon.

---

## Appendix A — Simulation Model Reference Equations

This appendix documents the governing equations relevant to the injectable-food product. The full Python implementation is in `Weapons-Defence/weapons_simulation.py` §21 (osmolality model). The osmolality result (3 037 / 4 436 mOsm/kg) IS a simulator output and IS the canonical safety reference for this document — see §0.

### A.1 Osmolality model (Plumb / Holliday-Segar — from `weapons_sim_results.md` §21)

```
Osmolality (mOsm/kg)  =  Σᵢ (nᵢ · Cᵢ) / M_water

nᵢ        = number of osmotically active particles per solute molecule
            (e.g. NaCl ≈ 1.9, glucose = 1.0, amino acid = 1.0)
Cᵢ        = molal concentration of solute i (mmol per kg water)
M_water   = mass of water (kg) in the formulation
```

**Safe-infusion bounds (Plumb / Holliday-Segar):**

```
Peripheral IV safe:    Osmolality < 600 mOsm/kg
  Above this, the venous endothelium sustains chemical injury within minutes;
  phlebitis and venous sclerosis follow.

Central IV safe:        Osmolality < 1 800 mOsm/kg
  Above this, even a large-bore central venous catheter terminating in the SVC
  cannot dilute the bolus to a non-injurious concentration before tissue contact.

Oral / enteral safe:    Osmolality < ~1 500 mOsm/kg sustained; > 2 000 mOsm/kg tolerated short-term
  The GI mucosa is anatomically adapted to high-osmolality solutions; gastric chyme
  routinely exceeds 1 500 mOsm/kg with no injury.
```

**Calculation for the current Injectable Food formulation (1 200 kcal/L baseline, per §0.1):**

```
Per 1 L of formulation at 1 200 kcal/L:
  Glucose:           200 g  →  200 / 180 = 1 111 mmol  →  n=1, contribution = 1 111 mOsm
  Amino acids:        80 g  →  mixed AA average MW 130, ≈ 615 mmol  →  n=1, contribution = 615 mOsm
  Lipid emulsion:     70 g  →  emulsion particles, ≈ 50 mOsm
  Electrolytes (Na⁺ K⁺ Cl⁻ Ca²⁺ Mg²⁺ phosphate):                        ≈ 280 mOsm (physiological)
  Vitamins / micronutrients:                                              ≈ 30 mOsm

  Total per L of formulation:  ≈ 2 086 mOsm
  Adjusted for water-mass denominator (≈ 690 g water in 1 L formulation):  ≈ 3 037 mOsm/kg ✓

Compare to safe peripheral-IV bound 600 mOsm/kg:    5.1× over (FAILS)
Compare to safe central-line bound 1 800 mOsm/kg:   1.7× over (FAILS)
```

The simulator output matches the §0.1 reported value of **3 037 mOsm/kg** for the baseline and **4 436 mOsm/kg** for the 1 800 kcal/L field-ration (which scales by the additional caloric load).

### A.2 Subcutaneous absorption model

```
C_tissue(t) = C_blood × (1 − exp(−k_abs · t))    (first-order absorption from subcutaneous depot)

k_abs        = subcutaneous absorption rate constant (h⁻¹)
               Typical for PLGA microsphere depot: k_abs ≈ 0.005 – 0.02 h⁻¹
               (vs oral k_a ≈ 1 – 5 h⁻¹; the depot is ~100× slower than oral)

Time to therapeutic plasma glucose (target: 4 – 6 mmol/L plasma glucose):
   t_therapeutic = −ln(1 − C_target / C_blood_max) / k_abs

For the GlycoDur-P depot at k_abs = 0.01 h⁻¹ and C_blood_max = 8 mmol/L (target 4 mmol/L):
   t_therapeutic = −ln(1 − 4/8) / 0.01 = 69.3 h ≈ 2.9 days to reach steady state
```

The 2.9-day rise time is consistent with the §1.3 release-kinetics table (Week 1-2: 40 % glucose released).

### A.3 Caloric delivery model

```
P_delivered (kcal/hr) = Q_infusion · C_caloric

Q_infusion  = infusion rate (mL/hr)
C_caloric   = energy density (kcal/mL)

Target for full nutritional support:  2 000 kcal / 24 hr = 83.3 kcal/hr

For Scenario A (subcutaneous / enteral, current formulation):
  C_caloric  = 1.2 kcal/mL  (1 200 kcal/L baseline)
  Q_infusion = 83.3 / 1.2 = 69.4 mL/hr → 1 667 mL/day  (consistent with §0.3 estimate)

For Scenario B (peripheral-IV-compatible, 5× diluted):
  C_caloric  = 0.24 kcal/mL  (post 5× dilution)
  Q_infusion = 83.3 / 0.24 = 347 mL/hr → 8 333 mL/day  (clinically unacceptable for peripheral IV)
  → Scenario B as a 5× peripheral-IV dilution is not operationally feasible at full caloric support;
    central-line delivery (which tolerates 1 800 mOsm/kg, requiring only ≈ 1.7× dilution) is the
    only physiologically viable IV route at full caloric load.
```

This caloric-delivery model is the key engineering finding that motivates §0.3 Remediation 2 (enteral redesign) over §0.3 Remediation 1 (peripheral-IV dilution) for any sustained-deployment use case at full caloric load.

---

## Portfolio §23 Lifecycle (service intervals)

Headline intervals from [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.1 / [`../weapon_lifecycle_configs.py`](../weapon_lifecycle_configs.py):

| Headline metric | Value |
|---|---|
| Formulation shelf @ 25 °C | **18 mo** |
| Cold-chain shelf | **30 mo** |
| Osmolality limit | **600 mOsm/kg** |

#### Component service thresholds (§23.1.1)

| Component | Warn | Replace | Model |
|---|---|---|---|
| Peripheral-safe isotonic bag | 12 mo | 18 mo | Lipid oxidation Q10 |
| Central-line hypertonic vial | 24 mo | 30 mo | Cold-chain integrity |

---

## Conclusion

The GlycoDur-P and NutriComplete-P protein systems represent a revolutionary approach to sustained nutrition delivery. By combining advanced protein engineering with proven drug delivery technologies, these systems could transform medical nutrition support and enable new applications in extreme environments.

The synthesis routes are feasible using current biotechnology infrastructure, and the regulatory pathway follows established precedents. With proper development and testing, these sustained nutrition proteins could provide life-changing benefits for patients and enable new frontiers in human exploration and emergency preparedness.

**Key Innovation**: Converting the concept of IV nutrition from a continuous infusion to a long-acting injection, providing unprecedented freedom and quality of life for patients requiring nutritional support.

---

*Document prepared for research and development purposes. All designs are hypothetical and require extensive testing and validation before any clinical application.*
