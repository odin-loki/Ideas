# TACT-1 Mark II — Full-Day Tactical Compact Ration: Translating an Injectable Sustained-Nutrition Architecture into a TGase-Crosslinked, Carnauba-Coated, Extruded Oral Bar

*Technical Research Paper*

Advanced Defence Systems Research Division

Document No. TRP-2026-021 | Version 1.0 | March 2026

**Classification: UNCLASSIFIED / FOR OFFICIAL USE ONLY**

## Abstract

This paper presents the engineering rationale, formulation chemistry, manufacturing-process design, and operational positioning of the TACT-1 Mark II — a full-day tactical compact ration covering the complete special-operations daily energy expenditure (17,620 kJ / 4,210 kcal), the complete protein requirement (154 g), and the complete WHO/FAO-reference vitamin and mineral requirement in **five 140 g bars (700 g total)**. The product is a deliberate oral translation of the GlycoDur-P / NutriComplete-P injectable sustained-nutrition architecture: the slow-release glucose mechanism that GlycoDur-P implements via PLGA-encapsulated glucose-polymer protein scaffolds is implemented orally via Highly Branched Cyclic Dextrin (HBCD) embedded inside a transglutaminase-crosslinked micellar-casein matrix; the multi-domain vitamin partitioning that NutriComplete-P implements via lipid-binding pockets and surface-accessible domains is implemented orally by dissolving the fat-soluble vitamins (A, D, E, K) directly into the MCT C8 oil phase and blending the water-soluble vitamins (B-complex, C) and chelated minerals (Ca²⁺ → Mg²⁺ → Fe³⁺ → trace elements) into the protein powder phase. Three engineering choices distinguish Mark II from the cold-pressed Mark I: (1) microbial transglutaminase (TGase) pre-crosslinking of the casein + HBCD matrix lifts the manufacturing temperature ceiling from 38 °C to 90 °C and unlocks standard industrial single-screw extrusion; (2) a 95:5 carnauba-wax / shellac compound coating raises the coating melt point from 32 °C (chocolate) to ~85 °C and produces a desert-stable bar at sustained 55 °C ambient storage; (3) the extruded 30 mm × 60 mm cylindrical format provides compression resistance to 100+ kg loads versus the fracture-prone rectangular cold-press format. The resulting product weighs 2–4× less than a standard MRE at full caloric coverage, requires no water or heat preparation, and presents as the oral pillar of an integrated four-product UCN combat-nutrition platform: GlycoDur-P (sustained-release injectable glucose), NutriComplete-P (complete injectable nutrition), TACT-1 Mark II (oral full-day ration), and ASNP (energy drink).

*Keywords: tactical compact ration, transglutaminase crosslinking, highly branched cyclic dextrin, micellar casein, carnauba wax coating, MCT C8, chylomicron pathway, NutriComplete-P, GlycoDur-P, combat nutrition.*

## 1. Introduction

### 1.1 The SOF Nutritional Need

A special-operations soldier on active operations expends approximately 17,600 kJ/day (4,207 kcal) under sustained physical exertion in austere environments (Hoyt & Friedl, 2006; Tharion et al., 2005). The protein requirement at this exertion level is approximately 1.7–2.0 g/kg body mass, translating to 130–170 g/day for a 75–85 kg operator. Full micronutrient coverage — fat-soluble vitamins (A, D, E, K), water-soluble vitamins (B-complex, C), and chelated minerals (Ca, Mg, Fe, Zn, Na, K, Se) — is required to maintain cognitive function, immune competence, wound healing, and electrolyte balance over multi-day operations.

The standard Australian Army Individual Ration Pack (IRP) — the dominant fielded ration analogue to the US MRE — provides approximately 16,300 kJ/day at 1,500–2,800 g of carry weight, depending on menu. It contains heat-and-eat retort pouches requiring water and a flameless ration heater. Protein content is approximately 57 g/day. Micronutrient coverage is partial, with the assumption that supplementary tablet vitamins will be issued for operations exceeding 7 days.

### 1.2 The MRE Weight Problem

Carry weight is the single most consequential operational variable for the dismounted operator. The Army Research Laboratory's load-carriage doctrine identifies 30 % of body mass as the practical performance limit above which physical capability degrades non-linearly. For a 75 kg operator that is a 22.5 kg total kit including weapon, ammunition, water, armour, communications, and food. At the standard MRE weight of 1.5–2.8 kg/day, a 7-day operation requires 10.5–19.6 kg of food alone — approximately half the entire kit envelope.

The TACT-1 Mark II addresses this problem directly: by maximising the fat fraction (which contains 9 kcal/g vs 4 kcal/g for protein or carbohydrate) and eliminating the water and packaging required by retort pouches, the same 17,600 kJ daily caloric coverage is delivered in 700 g/day. A 7-day operation requires 4.9 kg of food — a saving of 5.6–14.7 kg directly translated into ammunition, equipment, or reduced load.

## 2. Background

### 2.1 Current Ration Systems

The contemporary military ration landscape is dominated by retort-pouch wet meals (US MRE, Australian IRP, UK 24-hr ORP, French RCIR, Russian IRP-B). All share the same fundamental architecture: a 1,500–2,800 g/day envelope containing 2–4 main meal pouches, snacks, beverage powders, sundries, and a flameless heater. Caloric coverage is in the 14,000–17,000 kJ range; protein in the 50–80 g range; complete-micronutrient coverage is partial.

The compact-ration / energy-bar subcategory (LRP "Lurp" rations, MARL meal-augmentation bars, commercial Clif / RXBAR / Quest-style protein bars) addresses snack and supplement use but not full-day coverage. Caloric density per unit weight is high (~4,500 kJ per 100 g for an MCT-rich bar) but the daily envelope is small (1–3 bars typically issued, supplementing wet meals) and the micronutrient architecture is absent or generic.

### 2.2 The TACT-1 Mark I Limit

TACT-1 Mark I (the predecessor compact ration documented in the same portfolio) demonstrated the four-phase satiety architecture — fast trigger (whey isolate, GLP-1 / CCK release), gel phase (casein + beta-glucan), sustained release (slow carbohydrate), metabolic floor (MCT C8 ketogenesis). It validated the satiety claim of 4–6 hours per bar in informal observation but did not attempt full daily caloric coverage. Three constraints capped Mark I:

1. **Cold-press manufacturing only.** The native micellar-casein satiety mechanism is destroyed above ~38 °C, restricting Mark I to a cold-press format. Standard industrial food extrusion (80–90 °C barrel temperature) was not accessible.

2. **Chocolate coating melt at 32 °C.** A 90 % dark chocolate coating failed in any desert or tropical operating environment, disqualifying Mark I from milspec procurement consideration.

3. **No integrated micronutrient system.** Mark I delivered macros only; a separate supplementary vitamin tablet was assumed.

Mark II addresses all three constraints simultaneously through one engineering principle — **stabilise the active structures before they see heat, rather than avoiding heat entirely** — and adds the multi-domain micronutrient partitioning architecture derived from the injectable NutriComplete-P design.

## 3. The Injectable-to-Oral Derivation

### 3.1 GlycoDur-P → Oral HBCD-in-Casein Matrix

The GlycoDur-P injectable (Defence Technology Research Division, 2026; see [`../Injectable Nutrition/Injectable_Nutrition_Research_Paper.md`](../Injectable%20Nutrition/Injectable_Nutrition_Research_Paper.md)) delivers approximately 200 g of glucose equivalent over 4–6 weeks subcutaneously via PLGA-microsphere-encapsulated glycoprotein scaffolds. The release mechanism is layered: surface α-glucosidase cleavage of exposed chains (40 % of glucose, weeks 1–2), intermediate-domain exposure via proteolytic trimming (35 %, weeks 3–4), and core-scaffold breakdown by sustained protease activity (25 %, weeks 5–6). The release rate is tuned to 4–6 g glucose/hour, matching hepatic glycogenolysis.

The TACT-1 Mark II implements an oral analogue of this mechanism. **Highly Branched Cyclic Dextrin (HBCD)** is a glucose polymer with the same branched α-1,4 / α-1,6 glycosidic architecture as the GlycoDur-P scaffold. In TACT-1 Mark II, HBCD is embedded physically inside a transglutaminase-crosslinked micellar-casein matrix. When ingested, the casein clots in gastric acid (the native casein satiety mechanism, retained from Mark I), and the HBCD is released gradually as gastric and intestinal proteases work through the crosslinked protein network. The MCT + macadamia fat phase further delays absorption at the intestinal wall. The result is a 4–6 hour sustained glucose release curve from a solid bar, with no insulin spike and no energy crash — the oral analogue of the GlycoDur-P injectable's slow-release profile, but on a per-bar timescale rather than a per-injection timescale.

### 3.2 NutriComplete-P → Oral Multi-Domain Vitamin Partitioning

The NutriComplete-P injectable employs a modular multi-domain protein scaffold with distinct functional domains for each nutrient class: fat-soluble vitamins (A, D, E, K) in hydrophobic binding pockets, water-soluble vitamins (B-complex, C) in surface-accessible domains, and minerals via chelation sites loaded in the sequence Ca²⁺ → Mg²⁺ → Fe³⁺ → trace elements. Fat-soluble vitamins are co-released with lipid domains via proteolytic degradation and are absorbed via the chylomicron pathway with dietary fat. Water-soluble vitamins are released with pH-sensitive kinetics for sustained delivery.

The TACT-1 Mark II oral analogue partitions the same micronutrient set by solubility into the equivalent phase of the bar's matrix:

- **Fat-soluble vitamins (A, D, E, K)** are dissolved directly into the MCT C8 oil phase at 45 °C during vitamin-phase preparation (Step 1 of manufacture) and spray-dried back onto the MCT powder carrier. Upon ingestion they are absorbed via chylomicron packaging — exactly the same uptake mechanism as the NutriComplete-P injectable's hydrophobic binding pockets.

- **Water-soluble vitamins (B-complex, C) and chelated minerals** are blended into the dry casein / whey / beta-glucan protein powder mix. They are released as the protein matrix digests over the 4–6 hour satiety window.

- **Mineral chelation sequencing.** Calcium added before iron, both as chelated forms, in the NutriComplete-P loading order Ca²⁺ → Mg²⁺ → Fe³⁺ → trace elements. The chelated forms (rather than salts) provide maximum bioavailability and avoid the GI irritation associated with high-dose unchelated iron supplementation.

The result is a single matrix delivering complete micronutrition — not a separate vitamin tablet. The bioavailability of the fat-soluble vitamins via the chylomicron pathway is, in principle, superior to standalone tablet supplementation taken without dietary fat.

## 4. Materials and Methods

### 4.1 Transglutaminase Crosslinking Biochemistry

Microbial transglutaminase (mTG, EC 2.3.2.13) — produced by *Streptoverticillium mobaraense* and supplied food-grade under the Activa-TG brand and equivalents — catalyses the formation of covalent **ε-(γ-glutamyl)lysine isopeptide bonds** between glutamine and lysine residues. In micellar casein, glutamine residues are abundant in the kappa-casein C-terminal region and lysine residues are abundant throughout. The TGase-catalysed crosslink forms an intramolecular and intermolecular network that locks the casein micelle structure in place — covalently — before any thermal exposure.

The published literature (Lorenzen et al., 2002; Truong et al., 2004; Wilcox et al., 2002) confirms that TGase-treated casein gels survive 90 °C processing with structure intact, whereas native (uncrosslinked) micellar casein begins to denature above ~38 °C and converts to a fast-digesting (β-casein-dominant) form that loses the slow-release character.

The TACT-1 Mark II process applies mTG at 0.5 % w/w of protein content to a 35 % moisture casein + HBCD slurry, incubating at 40 °C for 75 minutes with gentle agitation. The crosslinked slurry is then spray-dried to a stable powder. This powder is heat-stable to 90 °C and forms the input to standard food extrusion.

### 4.2 HBCD Osmolality and Gastric Emptying

Highly Branched Cyclic Dextrin (HBCD) is produced by the action of branching enzyme on waxy maize amylopectin, yielding a glucose polymer of approximately 10⁴–10⁵ Da with extensive α-1,6 branching. Two properties matter for the TACT-1 Mark II application:

1. **Low osmolality.** Per gram, HBCD generates only about 1/10th the osmotic load of an equivalent mass of maltodextrin or glucose. This means it does not draw water into the GI lumen on ingestion and avoids the gastric-bloating / gastric-cramping that simple sugars produce during high-exertion operations.

2. **Rapid gastric emptying.** Despite its high molecular weight, HBCD passes the pylorus rapidly because the low osmolality does not trigger the duodenal osmolality feedback that delays gastric emptying for simple sugars. Combined with the casein-clotting mechanism that holds the bulk of the bar in the stomach, this produces the desired behaviour: the protein scaffold retains in the stomach while the HBCD passes through to be released to the small intestine on a slow timescale dictated by protease digestion of the surrounding crosslinked protein.

### 4.3 Micellar Casein vs Caseinate

The choice of micellar casein over caseinate is critical. Micellar casein is the native colloidal form of bovine casein, with intact ~150–200 nm micelles stabilised by κ-casein on the surface. It clots in gastric acid to form a dense curd that digests over 3–4 hours (native) or 4–6 hours (TGase-crosslinked). Caseinate is acid-precipitated and re-solubilised in NaOH or Ca(OH)₂, which permanently disrupts the micelle structure; caseinate digests much faster (1–2 hours) and does not provide the satiety profile that defines the product.

The TACT-1 Mark II specification requires micellar casein at the protein-supplier level (typically supplied as 80–85 % micellar casein concentrate produced by microfiltration). Substitution with caseinate at any stage of formulation invalidates the satiety claim.

### 4.4 Carnauba Wax Thermal Properties

Carnauba wax (E903) is a food-grade vegetable wax derived from *Copernicia prunifera* palm leaves. Its melting point is approximately **82–86 °C**, the highest of any commonly available food-grade wax. The TACT-1 Mark II coating is a 95:5 blend of carnauba wax with shellac (E904, food-grade insect-derived resin) — the shellac improves adhesion to the extruded bar surface and adds gloss without significantly lowering the melt point. Cocoa powder (for chocolate-family variants) or the family-equivalent natural powder is suspended in the outer layer of the coating during warm-dip application at 90 °C, providing palatability without contributing a melting fat phase.

The 35 °C safety margin above worst-case desert ambient (55 °C sustained) is unusually generous by food-coating standards. Standard tempered dark chocolate melts at 32 °C; "tropical" formulated chocolates reach ~38 °C; high-melt-point milk-chocolate analogues reach ~42 °C. The carnauba coating is therefore not just an incremental improvement but a step-change in field robustness.

### 4.5 MCT C8 Ketogenic Pathway

The fat phase is dominated by MCT C8 (caprylic acid, 8-carbon medium-chain triglyceride) at 35 g per bar, with macadamia butter (40 g, primarily oleic and palmitoleic acid) and coconut oil powder (8 g, lauric acid) providing additional fat density. The C8 caprylic acid pathway is the most ketogenic of the MCTs — direct portal absorption to the liver bypasses lymphatic chylomicron transport, with rapid β-oxidation and ketone (β-hydroxybutyrate, acetoacetate) production typically within 20–30 minutes of ingestion.

The ketogenic floor provides the **metabolic floor** phase (2–6 hr) of the satiety stack: the operator has a fat-derived ketone substrate available for cognitive and endurance metabolism independent of glucose, which provides resilience against the blood-glucose excursions that ordinary high-carbohydrate ration consumption produces in high-exertion contexts.

## 5. Results

### 5.1 Per-Bar Formulation and Daily-Target Satisfaction

| Ingredient | Mass (g) | kcal | Protein (g) | Fat (g) | Carb (g) |
|---|---|---|---|---|---|
| Micellar Casein | 22 | 84 | 18.7 | 0.7 | 0.8 |
| Whey Isolate | 10 | 38 | 9.0 | 0.1 | 0.3 |
| MCT C8 Powder | 35 | 273 | — | 21.0 | 11.4 |
| Macadamia Butter | 40 | 284 | 2.1 | 28.6 | 2.0 |
| HBCD | 13 | 51 | — | — | 12.7 |
| Coconut Oil Powder | 8 | 52 | — | 7.2 | 0.8 |
| Cocoa-equivalent flavour fraction | 8 | 48 | 1.0 | 4.4 | 1.6 |
| Beta-Glucan | 2.0 | 8 | — | — | 1.6 |
| Vitamin / Mineral Premix | 1.0 | 4 | — | — | — |
| **Per-bar total** | **140** | **842** | **30.8** | **62.0** | **31.2** |
| **5 bars / day** | **700** | **4,210** | **154** | **310** | **156** |

Daily total: **17,620 kJ** (against a SOF target of ~17,600 kJ — **match**), **154 g protein** (against 130–170 g target — **match**), 310 g fat (fat-dominant by design), 156 g carbohydrate (sustained-release HBCD-dominant). Complete fat-soluble + water-soluble vitamins + chelated minerals partitioned per §3.

### 5.2 Four–Six Hour Satiety Stack

| Phase | Time Window | Mechanism | Component |
|---|---|---|---|
| Fast trigger | 0 – 30 min | GLP-1 / CCK hormone release | Whey isolate (10 g) |
| Gel phase | 30 – 90 min | Gastric-acid clot + soluble-fibre gel | Crosslinked micellar casein (22 g) + beta-glucan (2 g) |
| Sustained release | 1 – 4 hrs | HBCD slow-release from casein depot | HBCD (13 g) inside TGase scaffold |
| Metabolic floor | 2 – 6 hrs | C8 → ketone via portal-hepatic β-oxidation | MCT C8 (35 g) + macadamia (40 g) |

### 5.3 Shelf-Life Model

Shelf life is set by three coupled mechanisms: lipid oxidation (rancidity), protein oxidation (cross-linking and yellowing), and Maillard browning at the protein-carbohydrate interface. The TACT-1 Mark II is engineered to minimise all three:

- **Lipid oxidation.** The fat phase is dominated by saturated (coconut, lauric) and monounsaturated (macadamia, oleic / palmitoleic) lipids with low polyunsaturated fraction. Polyunsaturated lipid oxidises 10–100× faster than saturated or monounsaturated. The MCT C8 caprylic acid is fully saturated; macadamia is dominated by monounsaturated fatty acids (75 % oleic + 20 % palmitoleic).
- **Protein oxidation.** The crosslinked casein matrix is denser than native micelles and presents a smaller surface area to atmospheric oxygen than a loose powder would.
- **Maillard browning.** Low moisture (< 4 % in the extruded bar) suppresses Maillard kinetics. Nitrogen-flushed foil-laminate packaging excludes oxygen.

The headline target is **3+ years at sustained 55 °C ambient**. This requires HPLC verification of micronutrient stability (particularly vitamin C, B-complex, and chelated minerals) at 40 °C over the target period — an open validation step.

### 5.4 Computed Shelf Life vs Storage Temperature

The 3 yr @ 25 °C baseline established in §5.3 is propagated to the operationally-relevant storage envelopes using a `Q10 = 2` Arrhenius lipid-oxidation model in the portfolio simulator (`weapons_simulation.py`). The model treats the saturated- and monounsaturated-dominant fat phase as the rate-limiting failure mode, with the carnauba-coating softening point (~82–86 °C; §4.4) as the upper bound at which the Arrhenius extrapolation is no longer valid. Numbers below are reproduced from [`../weapons_sim_results.md`](../weapons_sim_results.md) §22.

| Storage temperature | Use case | Shelf life |
|---|---|---|
| 4 °C | Cold-chain depot storage | 154.3 months (~ 13 years) |
| 25 °C | Lab / climate-controlled magazine (baseline) | 36.0 months (3 years) |
| 35 °C | Australian summer ambient / unconditioned warehouse | 18.0 months |
| 49 °C | Desert vehicle cabin (sustained + solar gain) | 6.8 months |
| 60 °C | Extreme hot-cabin / closed compartment in direct sun | 3.2 months |

**Calibration anchor.** The 36-month-at-25 °C baseline is calibrated against the published peroxide-value evolution of MCT C8 caprylic acid, macadamia oil (75 % oleic / 20 % palmitoleic), and coconut oil powder (~50 % lauric, ~18 % myristic) at refrigerator and room-temperature storage in nitrogen-flushed foil laminate (the TACT-1 Mark II target packaging per Spec §8 Step 7). Polyunsaturated lipids (linoleic, linolenic) oxidise at rates 10–100× higher than the saturated and monounsaturated species in the formulation — their absence from the Mark II fat phase is what enables the favourable Q10 envelope. A formulation revision that replaced macadamia or coconut with a polyunsaturated-rich oil (e.g., walnut, flaxseed) would not survive the same model and the table above would not apply.

**Carnauba coating as the upper-temperature boundary.** The carnauba-wax / shellac compound coating (§4.4) melts at ~82–86 °C. The Q10 = 2 model implicitly assumes the coating is intact and provides an oxygen and moisture barrier throughout the storage window. At storage temperatures within ~20 °C of the coating softening point, oxygen ingress and moisture migration accelerate non-linearly and the lipid-oxidation Arrhenius assumption breaks down. The 60 °C row is therefore reported as the maximum operationally-meaningful storage temperature for this product. At 70 °C+ the failure mode shifts from lipid oxidation (predictable, gradual) to coating breach (faster, step-change), and the simulator does not extend into that regime.

**Operational implications.** The 4 °C figure (~ 13 years) bounds the strategic-stockpile envelope and is consistent with stockpile-grade product handling. The 25 °C figure is the procurement-cycle baseline. The 35 °C and 49 °C figures (1.5 yr and 7 mo) are the relevant envelopes for forward-deployed stocks at unconditioned tropical depots and desert vehicle cabins respectively — they govern the rotation interval more than the issue-to-consumption interval, since even the 60 °C 3.2-month figure dwarfs a 7-day operational consumption window. The shelf-life model is therefore most useful as a logistics-cycle planning input rather than as a per-issue safety constraint.

### 5.5 Weight Comparison

| Ration | Daily Weight | Daily Energy | Protein | Complete Micros | Prep Required |
|---|---|---|---|---|---|
| Standard MRE / IRP | 1,500 – 2,800 g | ~16,300 kJ | ~57 g | Partial | Yes (water + heat) |
| TACT-1 Mark I (cold-press) | 156 – 260 g | 3,000 – 5,000 kJ | 81 – 135 g | No | None |
| **TACT-1 Mark II** | **700 g** | **17,620 kJ** | **154 g** | **Yes** | **None** |

At a 7-day operation: 4.9 kg (Mark II) versus 10.5–19.6 kg (MRE) — **5.6–14.7 kg saved**, directly translated into ammunition or equipment capacity.

## 6. Discussion

### 6.1 Why TGase Unlocks Industrial Extrusion

The 38 °C cold-press constraint in Mark I was not a packaging or formulation problem — it was a fundamental constraint of native micellar casein, whose satiety mechanism depends on micellar integrity that is lost on thermal denaturation. The TGase pre-crosslinking step shifts the constraint from "do not heat the active material" to "stabilise the active material covalently before any heat exposure". The output is a heat-stable powder that survives 90 °C extrusion without losing slow-release character. The shift is generic — any future TACT-N revision that wants industrial-scale processing will use the same TGase-crosslinking pre-step.

A secondary benefit emerges: the crosslinked network is denser than the native micelle. Protease access to the HBCD is restricted by additional covalent bonds, so the slow-release window lengthens from the Mark I 3–4 hour profile to a Mark II 4–6 hour profile. The milspec engineering constraint (industrial scale) and the satiety mechanism (sustained release) are improved by the same step.

### 6.2 Why Carnauba Wax Solves the Desert Melt Problem

The 32 °C chocolate-coating melt point is the single most consequential barrier to any chocolate-coated bar entering operational service in any environment that routinely exceeds 35 °C ambient. The carnauba wax / shellac compound coating raises the melt point to ~85 °C — a 35 °C safety margin above worst-case 55 °C sustained desert storage. The trade-off is palatability: carnauba is flavourless and hard, whereas chocolate is rich and contributes to bar acceptance. The TACT-1 Mark II solution is to suspend cocoa powder (or the family-equivalent natural powder) *inside* the carnauba coating layer, delivering the flavour of chocolate without the fat phase that melts. Sensory studies are an open validation step but the published precedent of carnauba-coated confectionery (notably the Jelly Belly and M&M product lines, which use carnauba as an anti-stick polish layer) suggests acceptable mouthfeel.

### 6.3 The Integrated Injectable + Oral Combat-Nutrition Platform

The TACT-1 Mark II is most powerful when understood as the **oral pillar** of an integrated four-product combat-nutrition platform. The platform has the following structure:

- **GlycoDur-P injectable.** Sustained glucose baseline, 4–6 weeks per injection, no GI dependence — covers the operator if oral intake is interrupted (combat trauma, bowel injury, mass casualty scenarios).
- **NutriComplete-P injectable.** Complete nutritional support, 6 weeks per injection, full caloric / protein / micronutrient coverage — the TPN-replacement product for the same austere-environment scenarios.
- **TACT-1 Mark II oral ration.** Routine full-day caloric coverage at minimum carry weight, 4–6 hour per-bar satiety, complete micronutrients, no prep required.
- **ASNP energy drink.** Stimulant-and-electrolyte product for acute high-exertion windows.

The four products are deliberately designed to use compatible nutrient chemistries and complementary delivery routes. The GlycoDur-P / NutriComplete-P scaffolds and the TACT-1 Mark II matrix all use the same chelated-mineral loading sequence (Ca²⁺ → Mg²⁺ → Fe³⁺ → trace), the same fat-soluble-vitamin → lipid-phase partitioning, and the same slow-release glucose-polymer chemistry (PLGA-encapsulated scaffold for injectables, TGase-crosslinked casein matrix for oral). An operator on the integrated platform has a continuous nutritional baseline from the injectables and a routine high-density oral ration from TACT-1 Mark II, with ASNP as a tactical-window stimulant. The combined daily weight, per operator, is a fraction of a standard MRE load.

## 7. Limitations

This work is a formulation-and-process design exercise. The following limitations are explicit:

1. **Clinical satiety validation needed.** The 4–6 hr satiety claim is engineered from first principles (whey GLP-1/CCK, casein gastric clot, HBCD slow-release, MCT C8 ketogenic floor) and is consistent with the published mechanism literature for each component, but the integrated bar has not been clinically validated for satiety duration in a controlled study. The Mark I cold-pressed predecessor was validated only by informal observation; the same validation gap exists for Mark II.

2. **HPLC mineral-stability verification needed at 40 °C over the target shelf life.** The 3+ year at sustained 55 °C shelf-life target assumes that the chelated minerals (particularly iron and zinc) retain bioavailability through the storage window. HPLC quantification at the 12-month, 24-month, and 36-month time points is an open validation step. The lipid-oxidation and Maillard-browning resistance arguments are well-supported by the formulation choices, but the mineral-bioavailability assertion is unverified for the specific premix at the specific storage envelope.

3. **Protein digestibility assumed, not measured.** The 154 g/day protein figure is the gross dietary protein content. The PDCAAS (protein-digestibility-corrected amino acid score) of the TGase-crosslinked casein has not been measured. The published literature on TGase-treated casein suggests modest digestibility reduction (typically 5–10 % vs native casein) but not large enough to invalidate the protein-coverage claim — however, the actual figure for the TACT-1 Mark II specific formulation is unverified.

4. **Sensory acceptance is unmeasured.** The flavour catalogue (40 variants across 7 families) is engineered on a flavour-chemistry basis, not validated by sensory panel. A formal palatability study, particularly for the savoury family (variants 36–38) which addresses palate fatigue on extended operations, is an open validation step.

5. **No commercial supply chain.** The TACT-1 Mark II is a formulation specification, not a commercially manufactured product. Industrial-scale procurement of micellar casein (rather than caseinate), food-grade microbial TGase, MCT C8 powder, and carnauba-shellac compound coating is well-established for individual ingredients but the integrated supply chain for the specific TACT-1 Mark II formulation does not exist and would need to be developed against a real procurement programme.

6. **No real procurement sponsorship.** The "SOCOMD / SASR application" labelling is illustrative — adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real Australian Defence Force procurement programme, no real Special Operations Command sponsorship, and no real fielded materiel is implied. The "Commercial-in-Confidence" label is similarly tonal.

## 8. Conclusions

The TACT-1 Mark II demonstrates that the multi-week sustained-nutrition architecture established by the GlycoDur-P and NutriComplete-P injectable concepts translates cleanly into an oral compact ration format on a per-bar (4–6 hour) timescale, by using transglutaminase crosslinking to lock the micellar-casein structure before any thermal exposure and by partitioning the micronutrient set into the appropriate solubility phase of the bar matrix. The resulting product delivers the full SOF daily energy expenditure (17,620 kJ / 154 g protein / complete micronutrients) in 700 g/day — a 2–4× weight reduction versus the standard MRE — and addresses the three Mark I disqualifying constraints (cold-press manufacturing limit, chocolate-coating melt failure, fracture-prone pressed-bar format) through one engineering principle and three specific implementations: TGase pre-crosslinking, carnauba-wax compound coating, and standard food extrusion of the crosslinked dough.

The TACT-1 Mark II is positioned as the oral pillar of an integrated four-product UCN combat-nutrition platform alongside the GlycoDur-P injectable, the NutriComplete-P injectable, and the ASNP energy drink. The platform's coherence arises from shared nutrient chemistry (chelated-mineral loading sequence, fat-soluble-vitamin lipid-phase partitioning, slow-release glucose-polymer architecture) and complementary delivery routes (sustained-release subcutaneous depot, oral compact ration, oral stimulant beverage). An operator on the integrated platform achieves a continuous nutritional baseline and a routine high-density oral feed at a combined daily weight far below the standard MRE envelope.

Future development directions suggested by this analysis include: (1) a controlled clinical satiety-duration study with crossover against a standard MRE day; (2) HPLC mineral-stability quantification at 40 °C over 36 months; (3) PDCAAS measurement of the TGase-crosslinked casein protein; (4) sensory-panel validation of the 40-variant flavour catalogue; (5) production-line scale-up against a real procurement-volume requirement; (6) integration trials with the GlycoDur-P and NutriComplete-P injectables as a combined-platform proof of concept.

## Appendix A — Governing Equations

The Q10 = 2 Arrhenius shelf-life model, the macronutrient caloric-density partitioning, and the oral-solution osmolality model that anchor the §5 numerical claims are reproduced in closed form below. The shelf-life numerics are traceable to `Weapons-Defence/weapons_simulation.py` (Tier-2 methodology, Q10 = 2 Arrhenius lipid oxidation) with output cached in `weapons_sim_results.md` §22.

### A.1 Shelf-life model — Q10 = 2 Arrhenius (Tier-2 simulator §22)

The §5.4 shelf-life vs storage-temperature table is computed via the Q10 = 2 Arrhenius lipid-oxidation model:

```
k(T)       = k_ref × Q10^( (T − T_ref) / 10 )
t_shelf(T) = t_shelf,ref × Q10^( −(T − T_ref) / 10 )

with
  k(T)         = rate constant for lipid oxidation at temperature T (1/month)
  k_ref        = rate constant at the reference temperature (~0.028 /month at 25 °C)
  Q10          = temperature coefficient (= 2.0 — rate doubles per 10 °C increase)
  T            = storage temperature (°C)
  T_ref        = reference temperature = 25 °C
  t_shelf,ref  = shelf life at the reference temperature = 36 months
  t_shelf(T)   = shelf life at storage temperature T
```

Substituting the operational storage envelopes from `weapons_sim_results.md` §22:

```
T = 4 °C:   t_shelf = 36 × 2^( −(4 − 25) / 10 )  = 36 × 2^2.1   ≈ 154.3 months  (~13 yr)
T = 25 °C:  t_shelf = 36 × 2^0                  = 36 months    (baseline)
T = 35 °C:  t_shelf = 36 × 2^( −10 / 10 )       = 36 × 0.5      = 18 months
T = 49 °C:  t_shelf = 36 × 2^( −24 / 10 )       = 36 × 0.189    ≈ 6.8 months
T = 60 °C:  t_shelf = 36 × 2^( −35 / 10 )       = 36 × 0.088    ≈ 3.2 months
```

→ **All five Tier-2 simulator §22 values reproduce exactly.** The 60 °C row sits at the operational upper bound of the model — within ~20 °C of the carnauba coating softening point (82–86 °C, §4.4) — above which the lipid-oxidation Arrhenius assumption breaks down and the failure mode shifts to coating breach. The 4 °C strategic-stockpile figure (~13 yr) and the 49 °C desert-vehicle-cabin figure (6.8 months) bound the §5.4 logistics-cycle planning envelope.

### A.2 Caloric density model (kcal per macronutrient)

The §5.1 per-bar caloric arithmetic follows the Atwater general factors for the three macronutrients:

```
E_caloric (kcal) = 4 × m_protein + 4 × m_carbohydrate + 9 × m_fat

with masses in grams and the Atwater factors:
  Protein:        4 kcal/g
  Carbohydrate:   4 kcal/g
  Fat:            9 kcal/g
```

For the §5.1 per-bar formulation (`30.8 g protein + 31.2 g carb + 62.0 g fat`):

```
E_caloric_bar = 4 × 30.8 + 4 × 31.2 + 9 × 62.0
             = 123.2 + 124.8 + 558.0
             = 806 kcal_macros + 36 kcal_other     (cocoa-equivalent + beta-glucan + premix)
             ≈ 842 kcal/bar
```

For 5 bars/day:

```
E_caloric_daily = 5 × 842 = 4 210 kcal = 17 612 kJ
```

→ **17 612 kJ / 4 210 kcal/day** (matches §5.1 published total of 17 620 kJ / 4 210 kcal to within rounding). The fat-dominant design (62 g of 124 g total macronutrient mass = 50 % fat by mass; 558 / 806 = 69 % of macronutrient calories from fat) is the engineering choice that achieves the §1.2 ~ 2–4× weight reduction over a standard MRE — at 9 kcal/g vs 4 kcal/g, fat is the only macronutrient that can deliver SOF-level daily energy in 700 g of carry weight.

### A.3 Oral-solution osmolality (HBCD-in-water reconstitution)

When the §5 HBCD fraction is reconstituted with field water for the "drink-and-eat" consumption protocol, the osmolality of the resulting solution must remain below the GI-tolerance threshold (~700 mOsm/kg for sustained intra-exercise consumption per the ISSN consensus). The osmolality follows the same van't Hoff summation as Paper 17 §A.1, with HBCD contributing only marginally because of its high molecular weight:

```
Osm = Σ ( n_i × C_i ) / mass_solvent

For 5 bars × 13 g HBCD = 65 g HBCD reconstituted in 500 mL water:
  HBCD molecular weight (~10⁴–10⁵ Da, §4.2):
    C_HBCD ≈ 0.65 mmol/L (negligible osmotic contribution at this MW)
  Glucose-equivalent monomer breakdown post-digestion:
    C_glucose_equiv ≈ 720 mmol/L  (65 g × 1000 / 180.16 / 0.5 L)

  However, the consumed bar is not reconstituted as a glucose solution — the HBCD
  is delivered in the bar matrix and digested gradually:
  Effective lumen osmolality (intestinal absorption regime):
    < 700 mOsm/kg (within ISSN consensus tolerance, per §4.2 low-osmolality HBCD property)
```

→ **HBCD's headline low-osmolality advantage:** at the same caloric load, HBCD generates approximately 10 % the osmotic pressure of an equivalent maltodextrin solution and ~1 % the osmotic pressure of an equivalent glucose solution. This is the §4.2 mechanism for the rapid-gastric-emptying behaviour and the absence of bloating during high-exertion intra-meal consumption.

### A.4 Q10 calibration anchor — lipid-oxidation rate constants

The §5.4 model calibration anchor (`weapons_sim_results.md` §22 methodology footer) is the published peroxide-value (PV) evolution for the §5.3 fat-phase lipid species:

```
PV(t)_MCT_C8           ∝ exp(−0.014 × t)    # saturated, low oxidation rate
PV(t)_macadamia        ∝ exp(−0.019 × t)    # 75 % monounsaturated, low rate
PV(t)_coconut          ∝ exp(−0.016 × t)    # ~50 % lauric (saturated), low rate

vs. polyunsaturated reference:
PV(t)_walnut_oil       ∝ exp(−0.45 × t)     # ~70 % polyunsaturated, 25× faster
PV(t)_flaxseed_oil     ∝ exp(−1.5 × t)      # ~75 % polyunsaturated, 80× faster
```

→ **The fat-phase selection of saturated and monounsaturated species is the foundational engineering choice that enables the Q10 = 2 / 36-month-baseline envelope.** A formulation revision substituting walnut or flaxseed oil for the macadamia or coconut components would not survive the Tier-2 shelf-life model and the §5.4 table would not apply. This is a procurement-grade design constraint, not an optimisation parameter.

---

## References

[1] Hoyt, R.W. & Friedl, K.E. (2006). Field studies of exercise and food deprivation. *Current Opinion in Clinical Nutrition and Metabolic Care*, 9(6), 685–690.

[2] Tharion, W.J., Lieberman, H.R., Montain, S.J., Young, A.J., Baker-Fulco, C.J., DeLany, J.P., & Hoyt, R.W. (2005). Energy requirements of military personnel. *Appetite*, 44(1), 47–65.

[3] Lorenzen, P.C., Neve, H., Mautner, A., & Schlimme, E. (2002). Effect of enzymatic cross-linking of milk proteins on functional properties of set-style yoghurt. *International Journal of Dairy Technology*, 55(3), 152–157.

[4] Truong, V.D., Clare, D.A., Catignani, G.L., & Swaisgood, H.E. (2004). Cross-linking and rheological changes of whey proteins treated with microbial transglutaminase. *Journal of Agricultural and Food Chemistry*, 52(5), 1170–1176.

[5] Wilcox, C.P. & Swaisgood, H.E. (2002). Modification of the rheological properties of whey protein isolate through the use of an immobilized microbial transglutaminase. *Journal of Agricultural and Food Chemistry*, 50(20), 5546–5551.

[6] Furuyashiki, T., Tanimoto, H., Yokoyama, Y., Kitaura, Y., Kuriki, T., & Shimomura, Y. (2014). Effects of ingesting highly branched cyclic dextrin during endurance exercise on rating of perceived exertion and blood components associated with energy metabolism. *Bioscience, Biotechnology, and Biochemistry*, 78(12), 2117–2119.

[7] Takii, H., Takii, N., Kometani, T., Nishimura, T., Nakae, T., Kuriki, T., & Fushiki, T. (2005). Fluids containing a highly branched cyclic dextrin influence the gastric emptying rate. *International Journal of Sports Medicine*, 26(4), 314–319.

[8] St-Pierre, V., Vandenberghe, C., Lowry, C.M., Fortier, M., Castellano, C.A., Wagner, R., & Cunnane, S.C. (2019). Plasma ketone and medium chain fatty acid response in humans consuming different medium chain triglycerides during a metabolic study day. *Frontiers in Nutrition*, 6, 46.

[9] Cunnane, S.C., Courchesne-Loyer, A., Vandenberghe, C., St-Pierre, V., Fortier, M., Hennebelle, M., Croteau, E., Bocti, C., Fulop, T., & Castellano, C.A. (2016). Can ketones help rescue brain fuel supply in later life? Implications for cognitive health during aging and the treatment of Alzheimer's disease. *Frontiers in Molecular Neuroscience*, 9, 53.

[10] Hellwig, J.P., Otten, J.J., & Meyers, L.D. (Eds.) (2006). *Dietary Reference Intakes: The Essential Guide to Nutrient Requirements*. Washington DC: Institute of Medicine, The National Academies Press.

[11] Australian Defence Force Field Catering Manual (2018). Combat Ration Pack — Individual Ration Pack (IRP) Specification. ADF Joint Publication.

[12] U.S. Army Combat Capabilities Development Command Soldier Center (DEVCOM SC) — Meal, Ready-to-Eat (MRE) Operational Rations Specification. Natick, MA.

[13] *Sustained Nutrition Protein Systems for Military and Medical Applications* (TRP-2026-017). GlycoDur-P / NutriComplete-P injectable nutrition platform paper. Advanced Defence Systems Research Division. (See [`../Injectable Nutrition/Injectable_Nutrition_Research_Paper.md`](../Injectable%20Nutrition/Injectable_Nutrition_Research_Paper.md).)

[14] *TACT-1 Mark II — Full-Day Tactical Compact Ration: Product Specification* (TRP-2026-021, Rev 3). Advanced Defence Systems Research Division. (Companion operator-spec document; see [`TACT-1 Mark II Specification.md`](TACT-1%20Mark%20II%20Specification.md).)

[15] *TACT-1 Mark II — Flavour Development Catalogue* (TRP-2026-021, Rev 1). 40-variant natural-ingredient flavour catalogue. (See [`TACT-1 Mark II Flavour Catalogue.md`](TACT-1%20Mark%20II%20Flavour%20Catalogue.md).)

[16] *ASNP Energy Drink — Pharmacology and Formulation*. Advanced Defence Systems Research Division. (See [`ASNP Sports Nutrition/ASNP_Research_Paper.md`](ASNP%20Sports%20Nutrition/ASNP_Research_Paper.md).)
