# Universal depot drug delivery systems

**A systematic framework for designing controlled-release injectable formulations spanning hours to months**

*Pharmaceutical Sciences — Controlled Release Drug Delivery & Depot Formulation Engineering*

## Abstract

Injectable depot drug delivery systems represent one of the most clinically impactful technologies in modern pharmaceutics, enabling sustained therapeutic drug concentrations over durations ranging from hours to more than twelve months from a single subcutaneous or intramuscular administration [1][2]. By eliminating the need for daily oral dosing or repeated injections, depot formulations dramatically improve patient adherence, stabilise plasma pharmacokinetics, and reduce peak-related adverse effects — advantages that have driven the commercial success of products spanning contraceptives, antipsychotics, hormone modulators, and antiretroviral prophylactics [3][7]. This paper presents a comprehensive systematic framework for the design of controlled-release injectable depot systems capable of delivering virtually any therapeutic compound across user-defined time windows. The framework encompasses multi-mechanism release architecture using PLGA polymer matrices [4][5][6], phase-inversion in situ forming depot technology [8][9][10], thermoreversible gel systems [25], lipid-based vehicle design, duration-specific formulation strategies from 2-hour to 12-month targets, drug-class compatibility analysis for hydrophilic and lipophilic small molecules and large biological molecules, dosage scaling methodology, mathematical release modelling [17][18][19], burst release minimisation strategies [31], Quality by Design (QbD) implementation under ICH Q8 [38], and a four-phase preclinical-to-clinical development workflow. This framework is intended as a technically rigorous reference for pharmaceutical formulation scientists designing depot systems for any therapeutic indication.

**Keywords:** *injectable depot, PLGA microspheres, in situ forming implant, controlled release, phase inversion, sustained release, NMP, poloxamer, long-acting injectable, pharmacokinetics, Quality by Design*

## 1. Introduction

The concept of a drug depot — a localised reservoir from which an active pharmaceutical ingredient is released gradually into systemic or local circulation — represents a fundamental departure from the bolus-dosing paradigm of conventional injectable formulations. Rather than achieving a transient concentration peak followed by rapid elimination, depot systems are engineered to deliver drug at a controlled, sustained rate that maintains therapeutic plasma concentrations over extended periods while minimising the peaks and troughs associated with repeated dosing [1][27].

The clinical benefits of this approach are well-documented. For psychiatric medications, long-acting injectable (LAI) antipsychotics such as paliperidone palmitate (Invega Trinza, 3-month dosing) and aripiprazole monohydrate (Abilify Maintena, monthly dosing) have been shown to reduce relapse rates and hospitalisation compared to oral formulations, primarily through elimination of the adherence failures that drive recurrence in schizophrenia [7][36]. In endocrinology, gonadotropin-releasing hormone (GnRH) agonist depots such as leuprolide acetate (Lupron Depot) have enabled once-monthly or once-quarterly management of prostate cancer and endometriosis. In reproductive health, medroxyprogesterone acetate (Depo-Provera) provides 3-month contraception from a single intramuscular injection. More recently, the utility of the depot paradigm has been extended to HIV pre-exposure prophylaxis with cabotegravir and rilpivirine (Cabenuva, bimonthly dosing) — demonstrating that the technology is applicable across pharmacological classes from small molecules to complex salts [3][21].

Despite this diversity of marketed applications, the underlying formulation science of depot systems is unified by a common set of principles: polymer selection, drug-polymer compatibility, release mechanism tuning, burst release management, and injectable vehicle design. The challenge for pharmaceutical scientists is that these principles must be applied in a drug-specific, indication-specific, and duration-specific manner — there is no single universal formulation. The Universal Depot System (UDS) framework presented in this paper addresses this challenge by providing a systematic, decision-tree-driven approach to depot formulation design that can be adapted to any therapeutic compound and any target release duration [8][11].

## 2. Release Mechanisms in Injectable Depot Systems

### 2.1 Classification of Release Mechanisms

Drug release from injectable depot systems proceeds through one or more of four fundamental mechanisms, which can be combined in a single formulation to achieve complex, multiphasic release profiles [2][6]:

**Mechanism**
**Driving Force**
**Polymer System**
**Release Kinetics**
Dissolution-controlled

Drug solubilisation into release medium

Rate-limiting polymer coat or matrix

Pseudo-zero-order if membrane-controlled

Diffusion-controlled

Concentration gradient across polymer

PLGA matrix, lipid vehicles

Higuchi (t^0.5) for matrix; first-order for reservoir

Degradation-controlled

Polymer chain hydrolysis / erosion

PLGA, PCL, polyanhydrides

First-order to zero-order depending on erosion mode

Osmotic-controlled

Osmotic pressure differential

Semi-permeable membrane systems

Near-zero-order for extended periods

Table 1. Four primary drug release mechanisms operative in injectable depot systems, with associated driving forces, polymer platforms, and kinetic models.

In practice, most PLGA-based depot systems operate through a combination of diffusion-controlled release (dominant in the early phase) and degradation-controlled release (dominant in the later phase), yielding a characteristic triphasic profile: an initial burst phase (hours to days, diffusion-driven), a lag phase (slow diffusion through intact polymer), and a terminal degradation phase (accelerating release as polymer molecular weight falls) [6][3]. Formulation design seeks to suppress the burst phase and flatten the overall release profile toward zero-order kinetics for maximum pharmacokinetic benefit [31].

### 2.2 PLGA: The Universal Depot Polymer

Poly(lactic-co-glycolic acid) is the most extensively characterised and clinically validated polymer for injectable depot applications [3][4]. Its appeal rests on a combination of properties unmatched by competing materials: (1) biodegradability by simple hydrolytic chain scission to lactic acid and glycolic acid, both normal metabolic intermediates; (2) regulatory approval in numerous marketed products; (3) release duration tunability over four orders of magnitude through manipulation of molecular weight and comonomer ratio; (4) compatibility with a broad range of drug chemistries; and (5) well-understood manufacturing characteristics amenable to scale-up [5][33].

**PLGA Ratio (LA:GA)**
**MW Range (kDa)**
**Degradation Time**
**Primary Applications**
**Release Duration**
50:50

10–25 kDa

1–3 months

Short-to-medium duration depots, microspheres

Days to 6 weeks

50:50

25–60 kDa

3–6 months

Monthly depot formulations

1–2 months

75:25

30–60 kDa

4–8 months

Bimonthly/quarterly depots

2–4 months

85:15

80–150 kDa

9–18 months

Long-acting hormone depots, implants

6–12+ months

100:0 (PLA)

100–300 kDa

12–36 months

Ultra-long implants, structural scaffolds

12–24+ months

Table 2. PLGA polymer composition and molecular weight effects on degradation rate and achievable release duration. LA:GA = lactide:glycolide molar ratio.

### 2.3 Phase-Inversion In Situ Forming Depot Systems

In situ forming depot (ISFD) systems, commercialised as the Atrigel technology platform, represent a complementary approach to preformed microsphere depots [8][9]. The formulation is a liquid at room temperature: PLGA dissolved in a water-miscible, biocompatible solvent — typically N-methyl-2-pyrrolidone (NMP) — with the drug dissolved or suspended in the polymer solution. Upon subcutaneous or intramuscular injection, the organic solvent diffuses into surrounding tissue fluids and water infiltrates the depot, driving phase inversion of the polymer solution into a solid or semi-solid PLGA matrix that entraps the drug and provides controlled release [10][13].

ISFD systems offer several manufacturing advantages over microsphere depots: no microsphere fabrication equipment is required, manufacturing is simpler, and the liquid formulation is easier to fill and more stable during storage. The primary challenges are controlling the burst release associated with the rapid solvent-water exchange at the depot surface, managing injection site tolerability of the organic solvent, and achieving predictable depot geometry in vivo [11][12]. NMP, the dominant solvent in commercial ISFD products (Eligard, Atridox), has an established human safety profile from its use in clinical ISFD products over two decades [9][22].

### 2.4 Thermoreversible Gel Depot Systems

Poloxamer-based thermoreversible gels (Pluronic F127, F68 blends) undergo sol-gel transition near physiological temperature: liquid below 15–20°C and gelling at 37°C, forming a semi-solid depot that releases drug by diffusion and erosion over days to weeks [25]. The gel depot is eventually cleared by dilution and metabolic degradation. Commercial examples include the ReGel technology platform (MacroMed). Poloxamer gels are well-suited for short-to-medium duration depots (hours to weeks), protein therapeutics that would be denatured by organic solvents in ISFD systems, and applications where a non-biodegradable but gradually eroding matrix is acceptable [15][25]. Their limitation is the relatively rapid erosion (days to weeks maximum) compared to PLGA systems.

### 2.5 Lipid-Based Depot Vehicles

Lipid-based vehicles — sesame oil, castor oil, benzyl benzoate blends — provide long-acting depots through slow partitioning of lipophilic drug molecules from the oil phase into aqueous tissue fluids [27]. The release rate is governed by the oil:water partition coefficient of the drug and the viscosity of the oil vehicle; addition of aluminium monostearate or other gelling agents increases viscosity and further retards release. This approach is the basis for classical steroid hormone depot injections (testosterone cypionate in cottonseed oil; estradiol valerate in castor oil) and remains clinically relevant for highly lipophilic compounds where polymer encapsulation adds unnecessary complexity [37].

## 3. Duration-Specific Formulation Strategies

### 3.1 Framework Overview

The Universal Depot System framework provides distinct formulation strategies for three duration tiers: short (2–24 hours), intermediate (1–14 days), and long (1–12 months). Each tier is characterised by its primary release mechanism, optimal polymer composition, solvent system, and drug loading range. These are not rigid boundaries but guideposts for initial formulation design that must be refined through in vitro release testing and in vivo pharmacokinetic studies [5][6][34].

### 3.2 Hours-Duration Formulations (2–24 Hours)

Short-duration depots are appropriate for post-surgical analgesia, acute antibiotic delivery, or as a bridge formulation during pharmacokinetic profiling. At this timescale, the dominant mechanism is rapid phase inversion combined with fast polymer swelling — controlled primarily by solvent composition and PLGA molecular weight rather than polymer degradation [8][10].

**Parameter**
**Specification**
**Rationale**
Drug loading

10–30% w/w

Low-MW PLGA accommodates moderate loading

PLGA grade

50:50, MW 10–20 kDa

Rapid hydrolysis; fast depot clearance

Primary solvent

NMP 60–80%

Rapid phase inversion on injection

Co-solvent

Benzyl benzoate 20–40%

Solubility enhancement; viscosity control

Porosity additive

PEG 400 at 2–5%

Hydrophilic channel formation; accelerates release

Release mechanism

Phase inversion + rapid polymer swelling

Solvent-driven diffusion dominates at this timescale

Table 3. Formulation parameters for hours-duration ISFD depot systems.

### 3.3 Days-Duration Formulations (1–14 Days)

Intermediate-duration depots address antibiotic courses, hormone pulses, or acute neuropsychiatric loading doses. Release is governed by controlled diffusion through a partially degraded PLGA matrix supplemented by drug salt form optimisation to reduce aqueous solubility and extend the concentration gradient [5][28]. Conversion of the free base or acid form of the drug to a lipophilic salt (docusate, palmitate) reduces intrinsic aqueous solubility up to 10-fold and is a well-validated strategy for extending depot duration [34].

**Parameter**
**Specification**
**Rationale**
Drug loading

15–40% w/w

Medium-MW PLGA accepts higher loads

PLGA grade

75:25, MW 30–60 kDa

Moderate degradation rate

Primary solvent

NMP 50–70%

Controlled phase inversion kinetics

Burst control

Chitosan palmitate 5–10%

Hydrophobic matrix retards surface burst

Salt form engineering

Docusate or palmitate salt

Reduces intrinsic solubility 3–10x

Release mechanism

Controlled diffusion + moderate degradation

Dual mechanism enables flatter profile

Table 4. Formulation parameters for days-duration ISFD depot systems.

### 3.4 Months-Duration Formulations (1–12 Months)

Long-duration depots represent the most technically demanding tier, requiring polymer degradation rates aligned with therapeutic duration over months. At this timescale, polymer degradation is the dominant release mechanism and the rate of polymer hydrolysis must be carefully matched to the drug release requirement [6][14]. High molecular weight PLGA (85:15 ratio, 80–150 kDa) combined with lipophilic crystalline drug phases within the matrix provides the slowest achievable release rates from injectable biodegradable systems. Crystal engineering — micronisation and habit modification of drug crystals — influences the rate of crystal dissolution within the polymer matrix and provides an additional tuning parameter [28][34].

**Parameter**
**Specification**
**Rationale**
Drug loading

20–50% w/w

High loading needed for months of release

PLGA grade

85:15, MW 80–150 kDa

Slow hydrolysis; degradation-controlled release

Primary solvent

NMP 30–50% + viscosity enhancer

Viscous depot; slower solvent exchange

Composite matrix

Alginate-palmitate 10–20%

Hydrophobic secondary matrix retards release

Crystal engineering

Micronised crystals in lipophilic carrier

Slow crystal dissolution controls terminal release

Release mechanism

Polymer degradation + crystal dissolution

Dual rate-limiting steps ensure extended profile

Table 5. Formulation parameters for months-duration depot systems.

## 4. Universal Drug Compatibility Matrix

### 4.1 High Aqueous Solubility Drugs (>1 mg/mL)

Highly water-soluble drugs present the principal challenge in depot formulation: their intrinsic solubility in the aqueous tissue environment ensures rapid dissolution from the depot surface, leading to unacceptably high burst release and short effective duration even from high-MW PLGA matrices [31]. Four strategies address this challenge:

- Salt form conversion to a sparingly soluble lipophilic counterion (docusate, palmitate, pamoate) reduces aqueous solubility 10- to 1000-fold and is the single most effective duration-extending modification for ionic drugs ${r34}
- Hydrophobic matrix additive incorporation (fatty acids, waxes) creates a secondary diffusion barrier at the depot surface
- Co-encapsulation with hydrophobic polymers increases tortuosity of the drug diffusion path
- Polymer percentage increase (60–80% w/w polymer content) reduces drug:polymer ratio and slows release by diluting the drug phase

### 4.2 Low Aqueous Solubility Drugs (<1 mg/mL)

Poorly water-soluble drugs present the opposite challenge: inadequate dissolution at the depot-tissue interface can lead to unpredictable, erratic release and prolonged depot persistence beyond the intended duration. Enabling strategies include [30][35]:

- Vitamin E TPGS micelle co-formulation to solubilise hydrophobic drug at the depot surface
- Lipid nanoparticle co-encapsulation providing a liquid-crystalline matrix with controlled dissolution
- Amorphous dispersion in PLGA matrix — reduces crystallinity and improves dissolution rate
- Cyclodextrin complexation to enhance local aqueous solubility while maintaining polymer entrapment

### 4.3 Large Biological Molecules (Proteins and Peptides)

Protein and peptide drugs require special protection from the organic solvents, high shear forces, acidic microenvironment, and elevated temperatures that can occur during depot manufacturing and in vivo release [21][32]. The acidic microenvironment generated by PLGA degradation products (lactic and glycolic acid) is particularly problematic, as it can catalyse protein hydrolysis and denaturation. Strategies include [5][12]:

- Double-wall microsphere architecture with protein core and PLGA shell, maintaining protein in an aqueous micro-environment
- Co-encapsulation of antacid excipients (magnesium carbonate, zinc carbonate) to neutralise lactic acid generated during PLGA degradation
- Trehalose or mannitol as lyoprotectant within the protein core
- Low-temperature manufacturing processes (spray freeze-drying for microsphere loading)
- PEGylation of the protein prior to encapsulation to improve thermodynamic stability

### 4.4 Small Molecule Drugs

Small molecules represent the most tractable class for depot formulation, with well-established approaches to salt form selection, crystal habit modification, and polymer compatibility screening. The primary design decision is salt form selection (free base vs acid vs lipophilic salt), which should be made before committing to a polymer system, as it determines the intrinsic solubility and therefore the feasible duration range for a given polymer grade [34][28]. Crystal habit modification through controlled recrystallisation can influence dissolution rate within the matrix and provides a fine-tuning parameter not available for amorphous drug forms.

## 5. Dosage Scaling Methodology

### 5.1 Low-Dose Drugs (<1 mg API)

Potent drugs requiring sub-milligram doses present a drug loading challenge: at typical PLGA loading efficiencies (10–40% w/w), the total microsphere mass needed to deliver <1 mg active ingredient is very small (2.5–10 mg polymer), which can be delivered in a 0.1–0.5 mL injection volume using a 25–27G needle. The primary formulation challenge at this dose range is homogeneous distribution of the drug within the microsphere population — dose variability is magnified at very low absolute doses, necessitating tight control of encapsulation efficiency and drug distribution uniformity [5].

### 5.2 Medium-Dose Drugs (1–100 mg API)

This is the classical dose range for most marketed depot products. Formulation volumes of 0.5–2.0 mL delivered by 21–23G needles are standard. Drug loading at 20–40% w/w provides polymer masses of 2.5–500 mg, well within the capacity of standard microsphere or ISFD depots. Injectability must be characterised — higher drug loading in PLGA microsphere suspensions increases viscosity and may require needle gauge reduction or formulation thinning with additional vehicle [8][14].

### 5.3 High-Dose Drugs (>100 mg API)

High drug doses — common in antibiotic depots, metabolic disorder therapies, and the macronutrient applications described in companion work on NutriComplete-P — require formulation volumes of 2–5 mL or multiple injection sites, which push the practical limits of subcutaneous depot tolerability. For very high doses, implantable biodegradable rod geometries (as used in Zoladex goserelin rods, Norplant levonorgestrel rods) offer a more practical depot architecture, enabling gram-scale drug loading in a geometrically defined implant that avoids the volumetric constraints of a syringe injection [7][33]. Large-bore needle (16–18G) or cannula-assisted insertion is required for implant systems.

## 6. Mathematical Modelling of Release Kinetics

### 6.1 Classical Release Models

Quantitative modelling of drug release from depot systems serves both mechanistic and regulatory functions: mechanistically, it enables parameter identification (diffusion coefficients, erosion rate constants) that guides formulation optimisation; regulatorily, it supports the in vitro–in vivo correlation (IVIVC) modelling required for bioequivalence assessments [40]. Four models dominate the controlled-release literature [17][18][19][20]:

**Model**
**Equation**
**Release Profile**
**Applicable System**
Zero-order

Mt = M0 + k0t

Constant (linear)

Membrane-controlled reservoir; osmotic systems

First-order

Mt = M0(1 - e^(-k1t))

Exponential decay

Porous systems; dissolution-controlled

Higuchi

Mt = kH \* sqrt(t)

Square-root of time

Matrix systems; diffusion through solid matrix

Korsmeyer-Peppas

Mt/M_inf = k \* t^n

Power law; n determines mechanism

Swellable polymeric matrices; coupled diffusion-relaxation

Hopfenberg

Mt/M_inf = 1 - (1 - k0t/C0a)^n

Surface-eroding

Surface-erosion controlled biodegradable polymers

Table 6. Classical mathematical models for drug release kinetics from depot systems. Mt = cumulative drug released at time t; M0 = initial drug content; k = rate constant; n = release exponent (Korsmeyer-Peppas); a = initial radius/half-thickness; C0 = initial drug loading; n = geometry factor (Hopfenberg).

### 6.2 The Korsmeyer-Peppas Power Law

The Korsmeyer-Peppas model is particularly valuable because the release exponent n encodes the dominant release mechanism: n = 0.43 (slab) or 0.45 (sphere) indicates Fickian diffusion-dominated release; n = 1.0 indicates Case II relaxation (anomalous transport driven by polymer swelling or erosion); intermediate values indicate coupled diffusion-relaxation [19]. For PLGA microspheres, n typically ranges from 0.5–0.8 in the diffusion-dominated early phase, transitioning toward higher values as polymer degradation becomes the rate-limiting step. Experimental determination of n from in vitro dissolution data provides a diagnostic tool for identifying the operative release mechanism at any given stage of the depot lifecycle.

### 6.3 Burst Release Quantification and Minimisation

Burst release — the rapid, often uncontrolled release of drug in the first hours to days following depot implantation — is the dominant formulation challenge in depot system design [31]. Burst release arises from drug at or near the depot surface that is poorly encapsulated, dissolved in the polymer-solvent interface, or accessible to tissue fluids before a coherent polymer matrix has formed. It can result in transient supratherapeutic plasma concentrations and is particularly problematic for drugs with narrow therapeutic indices. Quantification is achieved by AUC analysis of the early in vitro release fraction; targets are typically <20% of total dose released in 24 hours for systems designed for multi-week duration [36]. Mitigation strategies include:

- Pre-washing of microspheres after fabrication to remove surface-associated drug
- Core-shell microsphere design with a thin rate-controlling PLGA shell over a drug-loaded core
- Gradient drug loading within the microsphere (lower concentration at surface)
- Surface modification of the depot with a rate-controlling membrane applied post-fabrication
- ISFD systems: increasing polymer concentration or adding hydrophobic co-excipients to slow initial solvent exchange rate ${r10}${r11}

## 7. Advanced Release Rate Tuning

### 7.1 Accelerating Release Rate

When the target duration is shorter than what the base PLGA grade provides, or when release rate needs to be accelerated in later development stages, the following modifications increase release rate [2][6]:

- Increase PEG content (5–20% w/w) — hydrophilic channels created by PEG dissolution increase porosity and water penetration
- Decrease PLGA molecular weight (towards 10–20 kDa range)
- Shift lactide:glycolide ratio toward 50:50 (more hydrophilic glycolide accelerates hydrolysis)
- Add hydrophilic excipients (mannitol, sorbitol) to create water-wicking channels
- Reduce depot particle size — smaller microspheres have higher surface area:volume ratio

### 7.2 Decelerating Release Rate

Conversely, when release rate exceeds target, the following modifications slow release [2][14]:

- Add lipophilic components — fatty acid salts (palmitate, stearate) create hydrophobic barriers
- Increase PLGA molecular weight (toward 100–150 kDa)
- Use higher lactide content ratios (75:25 or 85:15) — more hydrophobic, slower degradation
- Add hydrophobic co-solvents (benzyl benzoate, ethyl oleate) to ISFD formulations
- Implement multi-layer coating (additional PLGA overcoat on microspheres)
- Convert drug to lipophilic salt form if not already done

## 8. Quality by Design Implementation

### 8.1 ICH Q8 Framework Application

Quality by Design (QbD), as formalised in ICH Q8(R2) [38] and Q9 [39], provides the regulatory-endorsed framework for systematic depot formulation development. For injectable depot systems, QbD implementation proceeds through the following structure:

- Quality Target Product Profile (QTPP): Define target release duration, route of administration, volume, acceptable burst release fraction, osmolality, sterility, and endotoxin limits
- Critical Quality Attributes (CQAs): Identify product attributes that must be controlled for safety and efficacy — for PLGA depots, these include drug content, encapsulation efficiency, particle size distribution, in vitro release profile, residual solvent (NMP), sterility, endotoxin, and container-closure integrity
- Critical Material Attributes (CMAs): Characterise input materials (PLGA MW, PDI, end group chemistry; drug polymorphic form; excipient moisture content)
- Critical Process Parameters (CPPs): Identify manufacturing parameters (emulsification speed, solvent evaporation temperature and rate, drying conditions, sterilisation cycle) that impact CQAs
- Design Space: Define the multidimensional combination of CPPs within which CQAs are reliably met — enabling post-approval manufacturing flexibility without regulatory resubmission

### 8.2 In Vitro Release Testing Protocol

The in vitro release test (IVRT) is the central analytical tool for depot system characterisation. Standard conditions for PLGA-based depots: phosphate-buffered saline pH 7.4, 37°C, sample collection with complete medium replacement to maintain sink conditions, 0.1% polysorbate 80 added for poorly water-soluble drugs to ensure sink. The reciprocating cylinder (USP Apparatus 3) or sample-and-separate method provides the most reproducible results for microsphere and ISFD systems [36]. Release data should be collected at minimum 8 timepoints spanning 100% of the intended release duration. Biorelevant media incorporating plasma proteins, lipases, or tissue homogenate may be employed to better predict in vivo behaviour in IVIVC models [40].

## 9. Four-Phase Development Workflow

## Phase 1: Drug Characterisation

Before any formulation work begins, the physicochemical and pharmacological profile of the drug must be fully characterised. The outputs of this phase determine the entire subsequent formulation strategy:

- Aqueous solubility profile across pH 1–8 and temperature 4–37°C
- Partition coefficient (LogP, LogD at pH 7.4)
- pKa determination — identifies salt form options
- Polymorphic screening — identifies stable crystalline forms
- Thermal stability (DSC, TGA) — sets maximum processing temperatures
- Compatibility with PLGA, NMP, common excipients (short-term stress testing at 40°C)
- Target plasma concentration, therapeutic window, and pharmacodynamic model

## Phase 2: Formulation Development

Using Phase 1 data, the formulation scientist selects the appropriate duration tier (Table 3–5), polymer grade, and excipient system. Design of Experiment (DoE) methodology is applied to systematically screen the formulation design space with minimum experimental runs. Key DoE responses are: encapsulation efficiency, in vitro release rate and profile, burst release fraction, particle size (if microsphere), injectability (force measurement through target needle gauge), and depot appearance [38].

## Phase 3: Preclinical Validation

Preclinical studies translate in vitro performance into in vivo pharmacokinetic and safety data. Rat or rabbit subcutaneous pharmacokinetic models are standard for systemic depots; the choice of species should be informed by the PLGA degradation rate (which is species-dependent due to tissue water content and pH differences). Local tissue response histology at 7, 14, 28, and 90 days quantifies inflammatory reaction to the polymer and solvent system. In vitro–in vivo correlation (IVIVC) development during this phase — establishing a quantitative relationship between in vitro release rate and in vivo plasma concentration — enables in vitro release testing to serve as a surrogate for bioequivalence in post-approval changes [40][36].

## Phase 4: Clinical Development and Regulatory Submission

Phase I trials in healthy volunteers or patients characterise single-dose pharmacokinetics, dose-linearity, local tolerability, and mass balance. Phase II establishes the dose-response relationship and optimal dose/frequency for the target indication. Phase III confirmatory studies provide the efficacy and safety database for regulatory submission. For depots, regulatory submissions under FDA 505(b)(1) or 505(b)(2) pathways must include full characterisation of in vitro release methodology, IVIVC Level A or B correlation, and manufacturing process validation including comparability of clinical and commercial manufacturing scale [38][40].

## 10. Troubleshooting Guide

**Problem**
**Root Cause**
**Solution Strategy**
Excessive burst release (>30% Day 1)

Surface-associated drug; solvent extraction artefact

Pre-wash microspheres; increase polymer MW; add rate-controlling membrane; increase polymer:drug ratio

Poor injectability (high force)

Microsphere aggregation; excess viscosity

Optimise particle size; add co-solvent; reduce PLGA concentration; use lower-viscosity NMP ratio

Incomplete drug release (<80% at target time)

Crystalline drug trapped in residual polymer; hydrophobic barrier

Add porosity enhancers (PEG, mannitol); reduce drug loading; use amorphous drug form; confirm sink conditions in IVRT

Variable release between batches

Inconsistent encapsulation; particle size variability

Tighten manufacturing controls; characterise CPPs via DoE; implement inline PAT monitoring

Shorter duration than target

PLGA degradation faster than expected; drug solubility too high

Increase PLGA MW; shift to higher lactide content; convert to lipophilic salt; add hydrophobic additives

Protein aggregation in depot

PLGA degradation acidification; organic solvent exposure

Add Mg(OH)2 or ZnCO3 antacid; use aqueous ISFD; core-shell design; PEGylate protein

Injection site reaction

NMP toxicity; PLGA particle size too large; inflammatory response to degradation products

Reduce NMP concentration; use benzyl benzoate as co-solvent; reduce particle size below 100 um; optimise PLGA grade

Table 7. Common depot formulation problems, root causes, and systematic solution strategies.

## 11. Discussion

The Universal Depot System framework presented here represents a systematic codification of the accumulated formulation science of injectable controlled-release systems. Its central insight is that depot design is not a single-solution problem but a multi-dimensional optimisation challenge whose feasible solution space is defined by the intersection of drug physicochemistry, target pharmacokinetics, manufacturing capability, and regulatory requirements. By organising the design parameters into explicit duration tiers, drug-class compatibility matrices, and a four-phase development workflow, the framework provides a navigable decision tree that reduces the dimensionality of the problem for practicing formulation scientists.

The selection between PLGA microsphere depots, phase-inversion ISFD systems, thermogel depots, and lipid vehicle systems is the first and most consequential formulation decision. Microsphere systems offer the most precise release rate control and the best characterised regulatory pathway but require sophisticated manufacturing infrastructure. ISFD systems are manufacturing-simpler and offer the advantage of liquid presentation but are limited by NMP tissue concentrations and more variable in vivo depot geometry. Thermogel systems are gentler on protein biologics but offer shorter maximum durations. Lipid vehicle systems remain the most practical for highly lipophilic small molecules requiring months of release [8][11][25].

The mathematical modelling framework (Section 6) provides a quantitative language for describing release kinetics that bridges in vitro measurement, in vivo pharmacokinetics, and IVIVC modelling. The power of Level A IVIVC — a quantitative point-to-point relationship between in vitro release rate and in vivo absorption rate — is that it enables in vitro release testing to predict human pharmacokinetic performance, substantially reducing the clinical testing burden for post-approval manufacturing changes and generic depot formulations [40].

A key limitation of the framework as presented is its agnosticism to drug-specific safety. The formulation strategies described are designed to optimise pharmacokinetic performance — release rate, duration, burst suppression — without consideration of the toxicological implications of specific drug-excipient combinations, novel drug entities without established safety profiles, or indications where depot-mediated overdose risk would be clinically unacceptable. Preclinical safety studies as described in Phase 3 of the development workflow are mandatory for any novel depot system regardless of the maturity of the formulation technology.

## 12. Conclusions

The Universal Depot System framework provides a comprehensive, scientifically grounded, and practically implementable roadmap for designing injectable controlled-release formulations across the full spectrum of clinically relevant release durations. Built on the established literature of PLGA depot technology, phase-inversion ISFD systems, thermoreversible gels, and lipid vehicle depots, and integrated with QbD methodology, mathematical release modelling, and drug-class compatibility analysis, the framework equips pharmaceutical scientists with the conceptual and technical tools needed to systematically translate any therapeutic compound into a viable long-acting injectable product. The development of this field will be driven by advances in smart polymer systems, personalised dosing algorithms, and real-time in vivo monitoring — all of which can be accommodated within the modular framework structure presented here.

## References
**[1]** Langer R. *"Drug delivery and targeting." *Nature. 392(Suppl):5–10 (1998).

**[2]** Uhrich KE, Cannizzaro SM, Langer RS, Shakesheff KM. *"Polymeric systems for controlled drug release." *Chem Rev. 99(11):3181–3198 (1999).

**[3]** Makadia HK, Siegel SJ. *"Poly lactic-co-glycolic acid (PLGA) as biodegradable controlled drug delivery carrier." *Polymers. 3(3):1377–1397 (2011).

**[4]** Anderson JM, Shive MS. *"Biodegradation and biocompatibility of PLA and PLGA microspheres." *Adv Drug Deliv Rev. 28(1):5–24 (1997).

**[5]** Jain RA. *"The manufacturing techniques of various drug loaded biodegradable poly(lactide-co-glycolide) (PLGA) devices." *Biomaterials. 21(23):2475–2490 (2000).

**[6]** Fredenberg S, Wahlgren M, Reslow M, Axelsson A. *"The mechanisms of drug release in poly(lactic-co-glycolic acid)-based drug delivery systems — a review." *Int J Pharm. 415(1-2):34–52 (2011).

**[7]** Siegel SJ, Winey KE, Gur RE, et al.. *"Surgically implantable long-term antipsychotic delivery systems for the treatment of schizophrenia." *Neuropsychopharmacology. 26(6):817–823 (2002).

**[8]** Packhaeuser CB, Schnieders J, Oster CG, Kissel T. *"In situ forming parenteral drug delivery systems: an overview." *Eur J Pharm Biopharm. 58(2):445–455 (2004).

**[9]** Dunn RL, Garrett S. *"The drug delivery and pharmacokinetic properties of the Atrigel drug delivery system." *Periodontal Clin Investig. 20(1):13–17 (1998).

**[10]** Parent M, Nouvel C, Koessler S, et al.. *"PLGA in situ implants formed by phase inversion: critical physicochemical parameters to modulate drug release." *J Control Release. 172(1):292–304 (2013).

**[11]** Kempe S, Mäder K. *"In situ forming implants — an attractive formulation principle for parenteral depot formulations." *J Control Release. 161(2):668–679 (2012).

**[12]** Lambert WJ, Peck KD. *"Development of an in situ forming biodegradable poly-lactide-co-glycolide system for the controlled release of proteins." *J Control Release. 33(1):189–195 (1995).

**[13]** Brodbeck KJ, DesNoyer JR, McHugh AJ. *"Phase inversion dynamics of PLGA solutions related to drug delivery. Part II. The role of solution thermodynamics and bath composition." *J Control Release. 62(3):333–344 (1999).

**[14]** Ravivarapu HB, Moyer KL, Dunn RL. *"Parameters affecting the efficacy of a sustained release polymeric implant of leuprolide." *Int J Pharm. 194(2):181–191 (2000).

**[15]** Zentner GM, Rathi R, Shih C, et al.. *"Biodegradable block copolymers for delivery of proteins and water-insoluble drugs." *J Control Release. 72(1-3):203–215 (2001).

**[16]** Izutsu K, Yomota C, Kawanishi T. *"Stabilization of pH in frozen aqueous solutions of weak acids and bases through preferential crystallization of buffer components." *J Pharm Sci. 100(5):1815–1822 (2011).

**[17]** Higuchi WI. *"Analysis of data on the medicament release from ointments." *J Pharm Sci. 52(12):1145–1149 (1963).

**[18]** Korsmeyer RW, Gurny R, Doelker E, Buri P, Peppas NA. *"Mechanisms of solute release from porous hydrophilic polymers." *Int J Pharm. 15(1):25–35 (1983).

**[19]** Peppas NA, Sahlin JJ. *"A simple equation for the description of solute release. III. Coupling of diffusion and relaxation." *Int J Pharm. 57(2):169–172 (1989).

**[20]** Grassi M, Grassi G. *"Mathematical modelling and controlled drug delivery: matrix systems." *Curr Drug Deliv. 2(1):97–116 (2005).

**[21]** Mitragotri S, Burke PA, Langer R. *"Overcoming the challenges in administering biopharmaceuticals: formulation and delivery strategies." *Nat Rev Drug Discov. 13(9):655–672 (2014).

**[22]** Tipton AJ, Dunn RL. *"In situ gelling systems." *Adv Polym Sci. 157:241–248 (2002).

**[23]** Bhattarai N, Gunn J, Zhang M. *"Chitosan-based hydrogels for controlled, localized drug delivery." *Adv Drug Deliv Rev. 62(1):83–99 (2010).

**[24]** Matricardi P, Di Meo C, Coviello T, Hennink WE, Alhaique F. *"Interpenetrating polymer networks polysaccharide hydrogels for drug delivery and tissue engineering." *Adv Drug Deliv Rev. 65(9):1172–1187 (2013).

**[25]** Ruel-Gariépy E, Leroux JC. *"In situ-forming hydrogels — review of temperature-sensitive systems." *Eur J Pharm Biopharm. 58(2):409–426 (2004).

**[26]** Packhaeuser CB, Kissel T. *"On the design of biodegradable and non-biodegradable in situ forming parenteral drug delivery systems." *J Control Release. 123(2):131–140 (2007).

**[27]** Washington N, Washington C, Wilson CG. *"Physiological Pharmaceutics: Barriers to Drug Absorption, 2nd edn.." *Taylor & Francis. London (2001).

**[28]** Gao ZH, Crowley WR, Shukla AJ, Harris JM, Doering JF. *"Controlled release of contraceptive steroids from biodegradable and crystalline polymer microspheres." *Pharm Res. 12(6):857–863 (1995).

**[29]** Bertrand N, Leroux JC. *"The journey of a drug-carrier in the body: an anatomo-physiological perspective." *J Control Release. 161(2):152–163 (2012).

**[30]** Soppimath KS, Aminabhavi TM, Kulkarni AR, Rudzinski WE. *"Biodegradable polymeric nanoparticles as drug delivery devices." *J Control Release. 70(1-2):1–20 (2001).

**[31]** Yeo Y, Park K. *"Control of encapsulation efficiency and initial burst in polymeric microparticle systems." *Arch Pharm Res. 27(1):1–12 (2004).

**[32]** Bhattarai SR, Bhattarai N, Yi HK, Hwang PH, Cha DI, Kim HY. *"Novel biodegradable electrospun membrane: scaffold for tissue engineering." *Biomaterials. 25(13):2595–2602 (2004).

**[33]** Nair LS, Laurencin CT. *"Biodegradable polymers as biomaterials." *Prog Polym Sci. 32(8-9):762–798 (2007).

**[34]** Okada H, Toguchi H. *"Biodegradable microspheres in drug delivery." *Crit Rev Ther Drug Carrier Syst. 12(1):1–99 (1995).

**[35]** Zhou S, Deng X, Yang H. *"Biodegradable poly(epsilon-caprolactone)-poly(ethylene glycol) block copolymers: characterization and their use as drug carriers for a controlled delivery system." *Biomaterials. 24(20):3563–3570 (2003).

**[36]** Amann LC, Gandal MJ, Lin R, Liang Y, Siegel SJ. *"In vitro-in vivo correlations of scalable PLGA-risperidone implants for the treatment of schizophrenia." *Pharm Res. 27(8):1730–1737 (2010).

**[37]** Ranade VV. *"Drug delivery systems: 6. Transdermal drug delivery." *J Clin Pharmacol. 31(5):401–418 (1990).

**[38]** ICH Q8(R2). *"Pharmaceutical Development." *International Council for Harmonisation. ICH Harmonised Guideline (2009).

**[39]** ICH Q9. *"Quality Risk Management." *International Council for Harmonisation. ICH Harmonised Guideline (2005).

**[40]** FDA Guidance. *"Bioavailability and Bioequivalence Studies Submitted in NDAs or INDs — General Considerations." *U.S. Food and Drug Administration. CDER Guidance Document (2014).
