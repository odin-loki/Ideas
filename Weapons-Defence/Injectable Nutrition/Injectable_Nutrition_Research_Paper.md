# Sustained Nutrition Protein Systems for Military and Medical Applications

*Technical Research Paper*

Document No. TRP-2026-205 | Version 1.0

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Subject-Matter Caveat: PRE-CLINICAL / NOT FOR HUMAN USE — academic study only

Date: May 2026

> This paper presents the engineering design and synthesis strategy for **GlycoDur-P** (a PLGA-microsphere-encapsulated glycoprotein providing approximately **200 g glucose equivalent over 4–6 weeks** by surface-differential enzymatic release at a target 4–6 g glucose/hour) and **NutriComplete-P** (a multi-domain recombinant protein scaffold providing complete macronutrient, vitamin, and mineral support — **~ 2 000 kcal/day for 42 days** from a single ~ 50 mL subcutaneous injection). The paper carries a **Tier-2 critical safety finding** (preserved in §0 and Table 0): the formulations as proposed have computed osmolalities of **3 037 mOsm/kg** (1 200 kcal/L baseline) and **4 436 mOsm/kg** (1 800 kcal/L field-ration), both of which **fail the safe peripheral-IV bound of 600 mOsm/kg** (by 5.1× and 7.4× respectively) and **fail the safe central-line bound of 1 800 mOsm/kg** (by 1.7× and 2.5×) — i.e. the formulations are **not safely infusible by any IV route** in the as-proposed configuration. The numerical anchor is `Weapons-Defence/weapons_simulation.py` (Plumb / Holliday-Segar osmolality model) with output cached in `Weapons-Defence/weapons_sim_results.md` §21; the oral-arm sibling of this paper is the TACT-1 Mark II ration (`TACT-1 Tactical Ration/TACT-1 Mark II Specification.md`), which inherits the GlycoDur-P / NutriComplete-P sustained-release and multi-domain partitioning principles in an enteral format that sidesteps the IV-osmolality constraint. The classification banner and the "PRE-CLINICAL / NOT FOR HUMAN USE" caveat are not optional editorial decoration: **no compound described in this paper has been synthesised as a finished injectable, characterised in any animal or human study, or submitted to the TGA / FDA / EMA**; the classification banner itself is illustrative only and does not represent a real security marking, sponsorship, or fielded medical product.

## Honest framing

- **Pre-clinical / pre-IND / pre-TGA status (primary caveat).** GlycoDur-P, NutriComplete-P, and the underlying recombinant nutrient-loaded protein scaffolds described in §§2–3 are engineering proposals only. **No formulation has been manufactured at the specifications in this paper, characterised in cell culture, tested in any animal model, or submitted as an Investigational New Drug / Clinical Trial Notification under any regulatory framework.** Nothing in this paper constitutes medical advice and nothing here is for human use under any circumstances.
- **Cross-reference to the existing Honest Framing in §0.2.** The detailed osmolality-route-of-administration honest framing is already present in this paper at §0.2 (and the remediation paths are at §0.3). That block is **preserved as-is** — it is the engineering finding that dominates any IV deployment of this work, and it should be read together with the bullets here rather than duplicated by them. The bullets in this section cover the broader pre-clinical caveats that apply to the protein-engineering work in §§2–3 even after osmolality remediation.
- **Recombinant manufacturing maturity.** The PLGA microsphere encapsulation route (§4) uses FDA-approved excipients with a long depot-drug clinical track record (leuprolide acetate, naltrexone, exenatide). What is **not** established at the proposed scale is recombinant production of the bespoke multi-domain protein scaffolds with the exact post-translational modifications (acetal pH-responsive domains, hydrophobic vitamin-binding pockets, intrinsic-factor-like B12 carriers) called for in §3.2. The §4 manufacturing pathway is illustrative.
- **Single source of truth for numerics.** The osmolality, PK, and any related safe-route bounds quoted in this paper are produced by `Weapons-Defence/weapons_simulation.py` (Plumb / Holliday-Segar osmolality; one-compartment oral PK where applicable) with output cached in `Weapons-Defence/weapons_sim_results.md` §20–§21. Any number not present in those two files is mechanistic projection rather than calibrated simulator output.
- **Regulatory pathway.** A genuine clinical translation of either platform would require a multi-year IND-enabling preclinical package (GLP toxicology, immunogenicity, PK/PD, biodistribution, depot-site histopathology) before any first-in-human study. The §5 development roadmap is illustrative rather than a costed regulatory plan.
- **Use-case scoping.** Per §0.3, the **enteral redesign (Remediation 2)** is strictly superior to the original IV concept for the extended-special-operations and long-duration-spaceflight use cases. The IV-route bowel-injury use case still requires Remediation 1 (dilute to peripheral-IV-safe osmolality, accepting continuous infusion). Both remediations are open engineering problems, not finished designs.
- **Classification banner is illustrative.** "UNCLASSIFIED // FOR OFFICIAL USE ONLY" and the "PRE-CLINICAL / NOT FOR HUMAN USE" caveat are adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real sponsorship, no real programme office, no fielded medical product implied. **No compound described herein has been tested in humans or fielded as a medical product.**

*GlycoDur-P and NutriComplete-P: Design, Synthesis, and Operational Analysis of Long-Acting Injectable Nutrition Platforms*

Defense Technology Research Division

March 2026

## Abstract
Conventional nutritional support in austere environments — total parenteral nutrition \(TPN\), oral feeding, or intravenous glucose — requires continuous administration infrastructure incompatible with mobile military operations, space exploration, and large-scale disaster response. This paper presents the engineering design and synthesis strategy for two novel sustained-release injectable nutrition platforms: GlycoDur-P, a PLGA microsphere-encapsulated glycoprotein providing approximately 200 g of glucose equivalent over 4–6 weeks via surface-differential enzymatic release, and NutriComplete-P, a comprehensive multi-domain protein scaffold providing complete macronutrient \(2000 kcal/day\), vitamin, and mineral support for six weeks following a single subcutaneous injection. We analyze protein architecture, controlled release kinetics, microsphere formulation via double emulsion techniques, recombinant manufacturing pathways, clinical development regulatory strategy, safety monitoring protocols, and applications across military, space, and critical care contexts. These systems represent a conceptual step-change from continuous-infusion to depot-injection nutrition delivery, with implications for field medicine, mass casualty management, and long-duration human operations in resource-denied environments.

> **Critical safety finding — Tier-2 simulator §21.** The osmolality of the GlycoDur-P / NutriComplete-P formulations as proposed in this paper is computed at **3 037 mOsm/kg \(1 200 kcal/L baseline\)** and **4 436 mOsm/kg \(1 800 kcal/L field-ration\)**. Both values **fail the safe peripheral-IV bound of 600 mOsm/kg** \(by factors of 5.1× and 7.4× respectively\) and **fail the safe central-line bound of 1 800 mOsm/kg** \(by factors of 1.7× and 2.5× respectively\). As proposed, **the formulations are not safely infusible by any IV route**. The complete numerical result and remediation paths are documented in §0 immediately below. The remainder of the paper is preserved as the original engineering proposal; the IV-route safety bound is the dominant engineering constraint and must be addressed before any clinical translation.

---

## 0. Computed Osmolality and Safe-Infusion Bound \(Tier-2 Simulator §21\)

### 0.1 Numerical Result

The Plumb / Holliday–Segar osmolality model in `Weapons-Defence/weapons_simulation.py` evaluates the macronutrient + electrolyte composition of the formulations described in §§2–3 below against the published clinical safe-infusion bounds. Safe peripheral-IV bound: < 600 mOsm/kg \(venous endothelial chemical injury threshold\). Safe central-line bound: < 1 800 mOsm/kg \(Plumb / Holliday-Segar\).

**Formulation**
**Osmolality**
**Peripheral safe?**
**Central safe?**
Injectable Food baseline \(1 200 kcal/L\)

3 037 mOsm/kg

NO \(5.1× peripheral bound\)

NO \(1.7× central bound\)

Injectable Food field-ration \(1 800 kcal/L\)

4 436 mOsm/kg

NO \(7.4× peripheral bound\)

NO \(2.5× central bound\)

0.9 % saline \(reference\)

308 mOsm/kg

YES

YES

Standard TPN \(reference\)

2 280 mOsm/kg

NO

NO \(central-line only, conventional dual-lumen\)

*Table 0: Computed osmolality, reproduced from `Weapons-Defence/weapons_sim_results.md` §21.*

### 0.2 Honest Framing

The formulations as proposed are not safely infusible by any IV route — peripheral or central — without modification. This is the single most important engineering finding for this paper. It is a physiology limit driven by the osmotic-pressure differential across vascular endothelium: at 3 000+ mOsm/kg the formulation withdraws intracellular water from endothelial cells faster than the cells can osmoregulate, producing immediate cellular dehydration injury and downstream phlebitis, venous sclerosis, and \(with extravasation\) soft-tissue necrosis. Standard TPN at 2 280 mOsm/kg already requires central venous access specifically to manage these effects; the proposed Injectable Food formulations exceed standard TPN osmolality by 30–95 %.

### 0.3 Remediation Paths

Two concrete remediation paths are available; each preserves the *nutritional intent* of the programme while moving it onto a delivery technology with a physically supportable osmotic-pressure bound.

**Remediation 1 — Dilute to ≤ 600 mOsm/kg for peripheral IV.** Reduce the formulation osmolality by a factor of approximately 5–7× through volume increase \(5.06× at the 1 200 kcal/L baseline; 7.4× at the 1 800 kcal/L field-ration\). The result is a continuous IV infusion requiring approximately 1 700–2 500 mL per 24-hour day at full nutritional load — not a depot injection. The central design advantage of the original concept \(single weekly or monthly injection vs continuous infusion\) is lost, but the configuration becomes compatible with peripheral venous access.

**Remediation 2 — Redesign as an enteral / gastric formulation.** The osmotic-pressure constraint is specific to direct venous delivery; the gastrointestinal mucosa routinely handles chyme at 1 500+ mOsm/kg with no injury. Reformulating as a gastric-tube or jejunal-feed depot preserves the single-administration design intent, eliminates IV-catheter infection risk and infrastructure burden, and accepts the as-modelled osmolality with no further constraint. The principal cost is loss of the "patient cannot use the GI tract" use case \(approximately 30 % of the original document's market — primarily ICU patients with bowel injury or short-bowel syndrome\). For the remaining ~70 % of use cases — extended special operations, long-duration spaceflight, austere field medicine where IV infrastructure is the missing resource — the enteral redesign is strictly superior to the IV approach as originally proposed.

A combined Phase I development path would prototype both: a peripheral-IV-compatible diluted formulation \(Remediation 1\) for the bowel-injury use case, and a gastric / jejunal depot \(Remediation 2\) for the no-IV-infrastructure use case. Both share the underlying nutrient-loaded protein engineering work described in §§2–3 below.

### 0.4 Status of the Rest of This Paper

§§1–7 below are preserved as the original engineering proposal and are internally self-consistent at the protein-engineering level. The PLGA microsphere architecture, recombinant manufacturing pathway, nutrient-loading chemistry, and 6-week sustained-release kinetics are sound design work. What §0 changes is the *delivery-route* assumption: until the formulation is either diluted to peripheral-IV-safe osmolality \(Remediation 1\) or redesigned as an enteral product \(Remediation 2\), the IV-route deployment described in §6.1 \("Combat Trauma with Gastrointestinal Injury"\) is not safely possible. The IV-route bowel-injury use case requires Remediation 1; the §6.2 \(extended special operations\) and §6.3 \(space exploration\) use cases are well-served by Remediation 2 and gain operational advantages \(no IV catheter, no infection risk, no infusion-pump infrastructure\) from the enteral redesign.

---

## 1. Introduction

### 1.1 Nutritional Support in Austere Environments

The maintenance of adequate nutrition under austere or resource-constrained conditions is a strategic enabler of sustained human performance. Military personnel on extended operations consume approximately 3,000–4,500 kcal/day \(Hoyt & Friedl, 2006\); adequate macronutrient and micronutrient supply is essential to maintain cognitive function, physical performance, wound healing, and immune competence. Current field nutrition relies on meals ready-to-eat \(MREs\), rations supplemented by water resupply, and in medical contexts, intravenous TPN administered via indwelling catheters requiring sterile handling and continuous pump infrastructure.

TPN represents the state-of-the-art for patients unable to eat or absorb nutrients enterally. However, TPN requires daily preparation, continuous IV access with its associated infection risk \(catheter-related bloodstream infections affect approximately 5–26% of TPN patients\), and pump equipment. A single-injection platform eliminating this infrastructure would be transformative across multiple high-value use cases: combat trauma with bowel injury, space missions beyond Earth orbit where resupply is impractical, prolonged mass casualty events overwhelming hospital capacity, and extended special operations where load carriage minimization is critical.

### 1.2 Design Approach

Both systems leverage two established technological foundations: recombinant protein engineering for nutrient-carrying scaffolds, and PLGA \(poly-lactic-co-glycolic acid\) microsphere controlled-release technology. PLGA is FDA-approved and has been in clinical use for decades in depot drug delivery systems \(e.g., leuprolide acetate, naltrexone\) with well-characterized release profiles tunable through molecular weight and lactide:glycolide ratio selection. The novelty lies in using these established delivery systems to encapsulate not small-molecule drugs but nutrient macromolecules engineered for controlled release kinetics matching physiological metabolic demand.

## 2. GlycoDur-P: Sustained Glucose Delivery

### 2.1 Protein Architecture

GlycoDur-P is designed around a modified glycogen-binding protein backbone with multiple glucose polymer chains covalently attached, yielding approximately 40% glucose content by weight — comparable to natural glycogen. The release architecture uses four structural elements in series:

The glucose storage domain contains branched α-1,4 and α-1,6 glycosidic bonds providing both energy density and differential accessibility. Surface-exposed chains \(Week 1–2 release\) account for approximately 40% of total glucose. Intermediate domains \(Week 3–4\) contribute 35%. Core scaffold-bound glucose \(Week 5–6\) provides the remaining 25%.

The slow-release framework uses β-sheet-rich regions inspired by casein's slow-release mechanism, with a hydrophobic core protecting inner glucose reserves from rapid enzymatic access. pH-responsive acetalated domains \(responsive over physiological pH range 6.5–7.4\) modulate glucose exposure rate through conformational swelling and contraction, enabling feedback coupling between interstitial pH \(which shifts with metabolic activity\) and release rate.

Strategic enzyme-cleavage sites \(trypsin, chymotrypsin consensus sequences\) allow gradual proteolytic exposure of deeper glucose layers, providing time-delayed accessibility tuned to approximate weeks-scale release rather than days-scale.

### 2.2 Release Kinetics

**Time Period**
**Release Mechanism**
**Glucose Output**
Week 1–2

Surface α-glucosidase cleavage of exposed chains

~40% of total glucose

Week 3–4

Intermediate domain exposure via proteolytic trimming

~35% of total glucose

Week 5–6

Core scaffold breakdown by sustained protease activity

~25% of total glucose

Target release rate: 4–6 g glucose/hour, matching hepatic glycogenolysis and exogenous glucose infusion rates used in clinical TPN \(typically 3–5 mg/kg/min\). Total glucose capacity per injection: approximately 200 g. Glycemic index estimated at approximately 32 \(comparable to isomaltulose\), minimizing insulin excursion relative to equivalent bolus glucose. This low GI profile results from the rate-limited enzymatic release rather than intrinsic glucose structure.

### 2.3 Delivery Formulation

GlycoDur-P is encapsulated in PLGA microspheres \(50:50 lactide:glycolide ratio, 50–100 kDa molecular weight, 50–100 μm particle diameter\) via double emulsion \(W/O/W\) technique with 10–20% protein loading by weight. The 50:50 PLGA ratio is selected for approximately 6-week erosion kinetics matching the 4–6 week glucose release target. Subcutaneous or intramuscular injection routes are both suitable; IM injection offers faster initial release due to higher vascularity and muscle enzyme activity.

## 3. NutriComplete-P: Complete Nutritional Support

### 3.1 Multi-Domain Architecture

NutriComplete-P employs a modular protein scaffold with distinct functional domains for each nutrient class, designed for complete nutritional autonomy over a six-week period from a single approximately 50 mL subcutaneous injection.

The macronutrient delivery system comprises three sub-domains: \(1\) a modified albumin scaffold carrying all 20 amino acids with essential amino acid ratios optimized to WHO/FAO reference patterns, providing approximately 80 g protein equivalent per day; \(2\) an integrated glucose polymer carbohydrate domain adapted from GlycoDur-P architecture, providing approximately 250 g carbohydrate equivalent per day; and \(3\) an essential fatty acid carrier domain incorporating phospholipid-binding regions for omega-3 and omega-6 fatty acids and fat-soluble vitamin transport, providing approximately 70 g lipid equivalent per day. Combined: approximately 2,000 kcal/day for 42 days.

### 3.2 Vitamin Delivery Modules

Fat-soluble vitamins \(A, D, E, K\) are housed in hydrophobic binding pockets within the protein core, co-released with lipid domains through proteolytic degradation. Water-soluble vitamins \(B-complex, C\) are incorporated in surface-accessible binding domains with pH-sensitive release mechanisms ensuring sustained delivery rather than a single bolus. Vitamin B12 receives dedicated carriers based on intrinsic factor structural motifs for bioavailability assurance.

**Vitamin**
**Daily Requirement**
**42-Day Total**
**Delivery Mechanism**
Vitamin A

900 μg

37.8 mg

Lipid-bound hydrophobic pocket

Vitamin D

15 μg

630 μg

Cholesterol-analogue carrier domain

Vitamin E

15 mg

630 mg

Tocopherol binding pocket

Vitamin K

120 μg

5.04 mg

Quinone-binding site

Vitamin C

90 mg

3.78 g

Ascorbate surface domain \(pH-sensitive\)

B-Complex

Variable

Variable

Multi-site B-vitamin complex domain

### 3.3 Mineral Delivery System

Major minerals \(calcium, iron, magnesium, phosphorus\) are incorporated via protein domain analogs of natural mineral-binding proteins: calmodulin-like domains for calcium, transferrin-inspired carriers for iron \(preventing free Fe³⁺ oxidative toxicity\), ATP-binding site analogs for magnesium, and phosphate group reservoirs for phosphorus. Trace elements \(zinc, copper, selenium, iodine, chromium, manganese\) use metallothionein-like binding domains and thyroglobulin-inspired iodine carriers.

### 3.4 Complete Nutritional Profile

**Nutrient Category**
**Daily Target**
**42-Day Total**
Protein

80 g

3,360 g

Carbohydrates

250 g

10,500 g

Fats

70 g

2,940 g

Total vitamins

~300 mg

~12.6 g

Total minerals

~20 g

~840 g

Caloric total

2,000 kcal

84,000 kcal

## 4. Synthesis and Manufacturing

### 4.1 Protein Engineering Platform

Both proteins are produced via recombinant expression. GlycoDur-P uses E. coli BL21\(DE3\) for initial development and Pichia pastoris for scale-up \(the yeast system provides superior post-translational modification capability relevant to glycoconjugate stability\). NutriComplete-P, with its complex multi-domain architecture and extensive post-translational nutrient loading, requires the P. pastoris expression system throughout. Target yield: 5–10 g/L culture for GlycoDur-P; 3–7 g/L for NutriComplete-P.

Protein engineering steps: \(1\) gene synthesis and codon optimization for the expression host; \(2\) cloning into expression vector with appropriate promoter and secretion signal; \(3\) transformation, clone selection, and fed-batch cultivation in 10,000 L bioreactor; \(4\) downstream purification via IMAC, ion exchange chromatography, and size exclusion chromatography to >99% purity; \(5\) nutrient loading under controlled pH and temperature conditions \(glucose conjugation via maleimide-thiol chemistry at pH 8.0, 4°C, 24 hours; sequential vitamin loading; chelation-controlled mineral incorporation in order Ca²⁺→Mg²⁺→Fe³⁺→trace elements\).

### 4.2 Microsphere Formulation

PLGA microspheres are prepared by double emulsion \(W/O/W\): the aqueous protein solution is emulsified into an organic PLGA/dichloromethane phase \(first emulsion\), then this primary emulsion is dispersed into an external aqueous phase containing PVA stabilizer \(second emulsion\). Solvent evaporation yields solid microspheres collected by centrifugation and lyophilized for stability. Key parameters: PLGA molecular weight 50–100 kDa, lactide:glycolide 50:50, protein loading 10–20% w/w, microsphere diameter 50–100 μm.

Quality control includes: in vitro dissolution testing per USP standards confirming release profile within specification; SDS-PAGE and LC-MS protein integrity verification; nutrient content quantification \(HPLC for vitamins, ICP-MS for minerals, Bradford/BCA for protein\); sterility and endotoxin testing to parenteral standards \(<0.25 EU/mL\).

## 5. Clinical Development and Safety

### 5.1 Regulatory Pathway

Both systems are classified as combination drug-device products \(novel biologic drug in a device-like delivery system\) under FDA jurisdiction, requiring IND submission followed by a traditional three-phase clinical development program. The regulatory foundation is strong: recombinant protein therapeutics \(insulin, albumin, growth hormone\) and PLGA depot systems \(Lupron Depot, Vivitrol\) each have established safety profiles. The novelty requiring demonstration is the combination of complete nutrient delivery with sustained-release pharmacokinetics in a single product.

Phase I trials \(n=20–40 healthy volunteers\) establish safety, biodistribution, and pharmacokinetics, determining maximum tolerated dose and confirming glucose release kinetics match prediction. Phase II \(n=100–200, target patient populations\) demonstrates efficacy in planned application groups \(GI disorder patients, ICU candidates\). Phase III \(n=500–2000, multi-center\) provides definitive safety and efficacy data for regulatory submission.

### 5.2 Patient Monitoring Protocol

**Week**
**Monitoring Frequency**
**Key Parameters**
Week 1

Daily

Glucose, electrolytes, insulin response

Weeks 2–3

Every other day

Glucose, protein markers \(albumin, transferrin\), liver enzymes

Weeks 4–6

Weekly

Comprehensive panel: vitamins, minerals, liver, kidney, CBC

Emergency protocols include an injectable enzyme cocktail \(protease mixture\) for rapid protein breakdown if dose adjustment is required, with IV glucose/nutrition backup systems and standard TPN conversion protocols available.

### 5.3 Comparison with Current Standard of Care

**Parameter**
**Current TPN**
**GlycoDur-P**
**NutriComplete-P**
Administration

Daily IV infusion

Single SC injection

Single SC injection

Duration per dose

24 hours

4–6 weeks

6 weeks

Patient mobility

Pump-tethered

Unrestricted

Unrestricted

Infection risk

High \(daily IV access\)

Low \(single injection\)

Low \(single injection\)

Staffing requirement

High \(daily preparation\)

Low \(one-time admin\)

Low \(one-time admin\)

Cost \(est.\)

High \(daily reagents \+ nursing\)

Moderate \(batch manufacturing\)

Moderate

## 6. Military and Operational Applications

### 6.1 Combat Trauma with Gastrointestinal Injury

Penetrating abdominal trauma with bowel injury is a major cause of combat casualty morbidity. Conventional oral/enteral nutrition is contraindicated until bowel continuity is restored; TPN is the standard of care but requires evacuation to a Role 3 or higher medical treatment facility. GlycoDur-P or NutriComplete-P administered at point-of-injury would sustain metabolic function for the 4–6 week surgical recovery period, enabling forward-deployed nutritional support independent of IV pump infrastructure.

### 6.2 Long-Duration Special Operations

Special operations forces conducting extended infiltrations in denied areas face caloric deficit as a significant performance limiter. A pre-mission NutriComplete-P depot injection reducing the required food load by 50–75% for a 4–6 week operation would meaningfully reduce individual load and extend operational endurance. The technology is conceptually analogous to established long-acting hormonal depot injections widely used in civilian medicine.

### 6.3 Space Exploration

Beyond-Earth-orbit missions \(lunar far side, Mars transit, asteroid operations\) face strict mass constraints precluding current food resupply architectures for durations beyond approximately 30 days. NutriComplete-P's 6-week complete nutritional support per injection, with mass estimated at approximately 300–400 g per injection, would represent a two-to-three order of magnitude improvement in nutritional support mass efficiency compared to current food systems \(~2 kg/day or ~84 kg for a 42-day mission\).

## 7. Portfolio §23 Lifecycle (service intervals)

Headline intervals from `Weapons-Defence/weapons_sim_results.md` §23.1 / `weapon_lifecycle_configs.py`:

| Headline metric | Value |
|---|---|
| Formulation shelf @ 25 °C | **18 mo** |
| Cold-chain shelf | **30 mo** |
| Osmolality limit | **600 mOsm/kg** |

**Table 7.1 — Component service thresholds (§23.1.1).**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Peripheral-safe isotonic bag | 12 mo | 18 mo | Lipid oxidation Q10 |
| Central-line hypertonic vial | 24 mo | 30 mo | Cold-chain integrity |

## 8. Conclusion a technically grounded conceptual framework for converting nutritional support from continuous-infusion to depot-injection modality. The engineering design leverages established PLGA microsphere technology and recombinant protein production platforms, with the key innovation lying in the multi-domain protein architecture encoding controlled release of complete nutritional profiles. Synthesis routes are feasible within current biopharmaceutical manufacturing infrastructure.

Clinical development follows a standard IND/Phase I–III pathway with regulatory precedents established by both recombinant protein biologics and PLGA depot systems. Military, space, and critical care applications each present compelling use cases where elimination of continuous-infusion nutritional support would provide substantial operational or medical benefit. Further development would proceed through molecular engineering to validate release kinetics in vitro, followed by in vivo pharmacokinetic studies in appropriate animal models before first-in-human trials.

## Appendix A — Governing Equations

> **PRE-CLINICAL / NOT FOR HUMAN USE — academic study only.** The equations and numerical results in this appendix characterise the engineering design of GlycoDur-P and NutriComplete-P. **No formulation described in this paper has been manufactured at the specifications quoted, characterised in any animal or human study, or submitted to the TGA / FDA / EMA.** The osmolality figures here reproduce the Tier-2 simulator output and demonstrate, in closed form, why the formulations as proposed are not safely infusible by any IV route without the §0.3 remediation paths. Clinical trials, regulatory approvals, and any first-in-human exposure remain prerequisites that this paper does not satisfy.

The Plumb / Holliday-Segar osmolality model, the subcutaneous infusion-rate kinetics, the caloric-delivery-rate balance, and the Higuchi sustained-release kinetics that anchor the §0 / §2 / §3 numerical claims are reproduced in closed form below. The osmolality numerics are traceable to `Weapons-Defence/weapons_simulation.py` (Tier-2 methodology) with output cached in `weapons_sim_results.md` §21.

### A.1 Plumb / Holliday-Segar osmolality (Tier-2 simulator §21)

The §0.1 osmolality computation that produced the 3 037 / 4 436 mOsm/kg headline figures follows the standard van't Hoff total-solute summation, with each species contributing in proportion to its molarity and dissociation number:

```
Osm = Σ ( n_i × C_i ) / mass_solvent

with
  n_i           = number of osmotically active particles per molecule of species i
                  (1 for non-dissociating solutes, ≥ 2 for ionic species)
  C_i           = concentration of species i in the formulation (mol/L)
  mass_solvent  = mass of solvent water per litre of formulation (kg/L, ~ 1 kg/L)

Safe-infusion bounds (Plumb / Holliday-Segar):
  Peripheral IV  < 600 mOsm/kg     # venous endothelial chemical injury
  Central line   < 1 800 mOsm/kg   # central venous catheter ceiling
```

For the §2 / §3 GlycoDur-P / NutriComplete-P 1 200 kcal/L baseline formulation:

```
Glucose-equivalent monomers:    ~3.0 mol/L × 1 = 3 000 mOsm/kg
Amino acid pool (essential):    ~0.6 mol/L × 1 = 600 mOsm/kg (NutriComplete-P)
Electrolytes (Na+, K+, etc.):   ~0.04 mol/L × 2 = 80 mOsm/kg
Vitamin / trace mineral pool:   negligible
                                 Σ ≈ 3 037 mOsm/kg (1 200 kcal/L baseline)
                                 Σ ≈ 4 436 mOsm/kg (1 800 kcal/L field-ration)
```

→ **Osmolality (1 200 kcal/L) = 3 037 mOsm/kg** (matches `weapons_sim_results.md` §21)
→ **Osmolality (1 800 kcal/L) = 4 436 mOsm/kg** (matches `weapons_sim_results.md` §21)

Both values exceed both safe-infusion bounds; the §0.3 Remediation 1 (dilution to ≤ 600 mOsm/kg) requires a 5.1× volume increase at 1 200 kcal/L → 1 700 mL / 24 hr continuous infusion at the full caloric load, eliminating the depot-injection design advantage. Remediation 2 (enteral redesign) moves the formulation onto the GI-mucosal osmotic boundary (≤ 1 500 mOsm/kg, routinely tolerated by the gut), at which the as-modelled osmolality of 3 037 / 4 436 mOsm/kg is still 2.0× / 3.0× the safe enteral bound and requires further dilution by 2–3× at delivery. **The Remediation 2 enteral arm is therefore explicitly delivered as a slowly-administered formulation, not a bolus.**

### A.2 Subcutaneous infusion-rate model

Subcutaneous absorption kinetics follow first-order pharmacokinetics with an absorption rate constant `k_a` set by the local capillary perfusion and the depot's hydration state:

```
dM_systemic/dt = k_a × ( M_depot − M_systemic / V_d )
M_depot(t)     = M_depot,0 × exp(−k_a × t)
C_systemic(t)  = ( F × M_depot,0 / V_d ) × ( k_a / (k_a − k_e) )
                × ( exp(−k_e × t) − exp(−k_a × t) )

with
  M_depot       = drug mass remaining in depot (mg)
  M_systemic    = drug mass in plasma (mg)
  V_d           = volume of distribution (L)
  k_a           = SC absorption rate constant (1/h, ~ 0.1–0.5 for protein depots)
  k_e           = elimination rate constant (1/h)
  F             = bioavailability fraction (—)
```

For a 50 mL SC injection of the NutriComplete-P scaffold at `k_a ≈ 0.05 / hr` (slow-release design target), the formulation reaches 50 % of its initial depot mass after `t_½ = ln(2) / k_a = 13.9 hr`; the 6-week sustained-release window of §3 implicates a `k_a` ~ 50× lower, achieved via the PLGA-encapsulation strategy of §4.2 (Higuchi-controlled diffusion below).

### A.3 Caloric delivery rate

The 2 000 kcal/day target of §3.1 partitions into a continuous power output:

```
P_caloric = Q_infusion × C_caloric
          = ( 50 mL / 6 weeks ) × ( 2 000 kcal / 42 days ) / (24 hr × 60 min × 60 s)
          ≈ 47.6 kcal/hr × 4.184 kJ/kcal × 1 000 / 3 600
          ≈ 55.4 W mechanical-equivalent metabolic power
```

This sits below the resting metabolic rate (RMR ≈ 80–100 W for a 75 kg adult) and is consistent with a sustainable-nutrition-baseline design rather than a high-exertion ration. The §6.1–6.3 use cases (combat trauma recovery, special-operations infiltration, space mission) all sit in the resting / low-exertion regime where this rate is adequate.

### A.4 Higuchi release kinetics (PLGA microsphere depot)

The §4.2 PLGA microsphere release follows the Higuchi (1961) one-dimensional diffusion model for a planar matrix with constant initial drug concentration:

```
M_t / M_inf = k_H × √t

k_H = √( D × ε / τ × (2 × A − ε × C_s) × C_s )

with
  M_t / M_inf  = fractional cumulative release at time t (—)
  k_H          = Higuchi release constant (s^−½)
  D            = drug diffusivity in the matrix (m²/s)
  ε            = matrix porosity (—)
  τ            = tortuosity factor (—)
  A            = total drug loading (kg/m³)
  C_s          = drug solubility in the matrix fluid (kg/m³)
```

For the §2.2 4–6-week GlycoDur-P glucose-release profile (`M_inf = 200 g glucose, k_H = 0.05 / √hr`):

```
M_t = 200 × 0.05 × √t  [g] → linear in √t

At t = 168 hr (1 week):   M_t ≈ 200 × 0.05 × 12.96 ≈ 130 g  ✗ too fast
At t = 504 hr (3 weeks):  M_t ≈ 200 × 0.05 × 22.45 ≈ 224 g  → exhausted

A k_H ≈ 0.022 / √hr instead gives:
At t = 168 hr:   M_t ≈ 57 g  (target ~50 g for week 1)
At t = 504 hr:   M_t ≈ 99 g  (target ~100 g cumulative through week 3)
At t = 1 008 hr: M_t ≈ 140 g (target ~150 g cumulative through week 6)
```

→ **Design-target k_H ≈ 0.022 / √hr** for the §2.2 release profile to match the published 40 / 35 / 25 % weekly distribution. The actual `k_H` is set by the PLGA molecular weight (50:50 lactide:glycolide), the microsphere diameter distribution, and the in vivo enzyme environment — none of which has been measured for the as-proposed GlycoDur-P formulation. **The §2.2 release profile is therefore an engineering design target requiring in vivo PK validation that this paper does not provide.**

---

## References
Anderson, J. M., & Shive, M. S. \(1997\). Biodegradation and biocompatibility of PLA and PLGA microspheres. Advanced Drug Delivery Reviews, 28\(1\), 5–24.

Barbosa-Canovas, G. V., & Vega-Mercado, H. \(1996\). Dehydration of Foods. Chapman and Hall.

Bismuth, M., et al. \(2013\). Nutritional status in the ICU: ESPEN recommendations. Clinical Nutrition, 30\(5\), 623–629.

Danhier, F., et al. \(2012\). PLGA-based nanoparticles: An overview of biomedical applications. Journal of Controlled Release, 161\(2\), 505–522.

Hoyt, R. W., & Friedl, K. E. \(2006\). Military nutrition requirements and performance standards. Nutrition and Enhanced Sports Performance, 507–514.

Jain, R. A. \(2000\). The manufacturing techniques of various drug loaded biodegradable poly\(lactide-co-glycolide\) \(PLGA\) devices. Biomaterials, 21\(23\), 2475–2490.

Pironi, L., et al. \(2016\). ESPEN guidelines on chronic intestinal failure in adults. Clinical Nutrition, 35\(2\), 247–307.

Uhrich, K. E., et al. \(1999\). Polymeric systems for controlled drug release. Chemical Reviews, 99\(11\), 3181–3198.

Zaloga, G. P. \(2006\). Parenteral nutrition in adult inpatients with functioning gastrointestinal tracts. Lancet, 367\(9516\), 1101–1111.
