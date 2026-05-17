# TACT-1 Mark II — full-day tactical compact ration

> **A full-day SOF tactical ration covering the complete daily caloric expenditure (17,620 kJ / 4,210 kcal), the complete protein requirement (154 g), and the complete WHO/FAO-reference vitamin and mineral profile in 5 bars × 140 g = 700 g/day — a 2–4× weight reduction over the standard MRE/IRP envelope. Derived from the GlycoDur-P / NutriComplete-P injectable sustained-nutrition architecture: TGase-crosslinked micellar-casein + HBCD matrix delivers the slow-release glucose curve over a per-bar 4–6 hour window; MCT C8 + macadamia + coconut fat phase carries fat-soluble vitamins via the chylomicron pathway; chelated minerals are loaded in the NutriComplete-P sequence Ca²⁺ → Mg²⁺ → Fe³⁺ → trace; the 95:5 carnauba-wax / shellac compound coating melts at ~85 °C (versus 32 °C for chocolate) and produces a desert-stable bar at sustained 55 °C ambient. Shelf life target 3+ years at 55 °C. 40-variant natural-ingredient flavour catalogue across 7 families, all sharing identical macros and micros. Positioned as the oral pillar of an integrated four-product UCN combat-nutrition platform alongside the GlycoDur-P injectable, the NutriComplete-P injectable, and the ASNP energy drink.**

> **Genre note.** TRP designator, FOUO banner, and "SOCOMD / SASR application · Commercial-in-Confidence" labels are adopted for tonal coherence with the rest of the `Weapons-Defence/` portfolio. No real Australian Defence Force procurement programme, no real Special Operations Command sponsorship, and no clinically validated product is implied or held. The TACT-1 Mark II is a formulation-and-process specification, not a commercially manufactured product.

---

## 📑 Source documents

| Document | Format | Purpose |
|---|---|---|
| [`TACT-1 Mark II Specification.md`](TACT-1%20Mark%20II%20Specification.md) | Operator specification (TRP-2026-021) | Full product spec — concept, derivation from GlycoDur-P + NutriComplete-P, four-phase satiety stack, per-bar formulation, micronutrient architecture, operational comparison vs MRE / Mark I, milspec engineering (TGase + carnauba + extrusion), 7-step manufacturing method, IP position. |
| [`TACT-1 Mark II Flavour Catalogue.md`](TACT-1%20Mark%20II%20Flavour%20Catalogue.md) | 40-variant catalogue (TRP-2026-021 companion) | 40 natural-ingredient flavour variants organised by 7 families (Chocolate 01–08, Coffee & Tea 09–14, Nut & Seed 15–21, Fruit 22–29, Spice & Sweet 30–35, Savoury 36–38, Floral & Botanical 39–40). Fixed nutrient lock on all variants. |
| [`Paper20_TACT-1_Mk_II_Ration.md`](Paper20_TACT-1_Mk_II_Ration.md) | Academic research paper (TRP-2026-021) | Abstract / introduction (SOF nutritional needs, MRE weight problem) / background (current rations, Mark I limits) / injectable-to-oral derivation / materials and methods (TGase biochemistry, HBCD properties, micellar casein vs caseinate, carnauba thermals, MCT C8 ketogenic pathway) / results / discussion / limitations / conclusions / references. |

---

## 🎯 Headline numbers

| Metric | Value |
|---|---|
| Daily ration | **5 bars × 140 g** |
| Daily mass | **700 g** |
| Daily energy | **17,620 kJ** (4,210 kcal) — full SOF requirement |
| Daily protein | **154 g** |
| Daily fat | 310 g (fat-dominant by design, 9 kcal/g) |
| Daily carbohydrate | 156 g (HBCD slow-release) |
| Complete micronutrients | **Yes** — fat-soluble in MCT phase, water-soluble + chelated minerals in protein phase |
| Per-bar satiety | **4 – 6 hours** (four-phase satiety stack) |
| Shelf life target | **3+ years at sustained 55 °C ambient** |
| Weight reduction vs MRE | **2 – 4× lighter** (700 g vs 1,500 – 2,800 g) |
| Carry-weight saving (7-day op) | **5.6 – 14.7 kg** versus standard MRE |
| Flavour variants | **40** across 7 families |
| Prep required | **None** — no water, no heat |

---

## 🔧 Three key engineering innovations

| # | Innovation | What it solves | How |
|---|---|---|---|
| **1** | **TGase pre-crosslinking** | Mark I's 38 °C cold-press manufacturing limit | Microbial transglutaminase forms covalent ε-(γ-glutamyl)lysine bonds in the casein + HBCD slurry at 40 °C for 75 min, locking the slow-release architecture before any heat exposure. Output powder is heat-stable to 90 °C and accepts standard single-screw extrusion. Bonus: denser network extends slow-release window from 3–4 hr (Mark I) to 4–6 hr (Mark II). |
| **2** | **Carnauba-wax compound coating** | Chocolate's 32 °C melt point fails in desert / tropical operating environments | 95:5 carnauba wax + shellac compound coating melts at ~85 °C — a 35 °C safety margin above worst-case 55 °C sustained desert storage. Cocoa powder (or family-equivalent natural powder) suspended in the outer layer delivers chocolate flavour without the melting fat phase. |
| **3** | **HBCD in TGase casein matrix** | Insulin-spike-and-crash on conventional carbohydrate rations during high-exertion ops | Highly Branched Cyclic Dextrin has very low osmolality (~1/10th of maltodextrin) and rapid gastric emptying despite its high molecular weight. Embedded inside the crosslinked casein scaffold, it is released gradually as proteases digest the surrounding network — producing a 4–6 hr flat blood-glucose curve with no insulin spike. The oral analogue of the GlycoDur-P injectable's 4–6 week sustained-release profile, on a per-bar timescale. |

---

## 🌡️ Computed shelf life vs storage temperature

Shelf life is propagated from the 36-month-at-25 °C baseline using a `Q10 = 2` Arrhenius lipid-oxidation model in the portfolio simulator (`weapons_simulation.py`). The carnauba-wax / shellac compound coating softening point (~ 82–86 °C) is the upper bound at which the Arrhenius extrapolation remains valid. Numbers below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §22.

| Storage temperature | Use case | Shelf life |
|---|---|---|
| **4 °C** | Cold-chain depot storage | **154.3 months (~ 13 years)** |
| **25 °C** | Lab / climate-controlled magazine (baseline) | **36.0 months (3 years)** |
| **35 °C** | Australian summer ambient / unconditioned warehouse | **18.0 months** |
| **49 °C** | Desert vehicle cabin (sustained + solar gain) | **6.8 months** |
| **60 °C** | Extreme hot-cabin / closed compartment | **3.2 months** |

The 4 °C figure (~ 13 years) bounds the strategic-stockpile envelope; the 35 °C and 49 °C figures govern the rotation interval for forward-deployed stocks at unconditioned tropical depots and desert vehicle cabins. Even the 60 °C extreme-cabin 3.2-month figure dwarfs any plausible 7-day operational consumption window — the shelf-life model is most useful as a **logistics-cycle planning input**, not as a per-issue safety constraint. The model relies on the saturated- and monounsaturated-dominant fat phase (MCT C8 / macadamia / coconut, with no polyunsaturated lipids); a future revision that introduces polyunsaturated oils would not survive this Q10 envelope.

---

## 🧩 The integrated four-pillar UCN combat-nutrition stack

TACT-1 Mark II is one component of an integrated four-product combat-nutrition platform that uses shared nutrient chemistries and complementary delivery routes to cover the full operational nutrition envelope. The platform is structured as:

- **Pillar 1 — GlycoDur-P (injectable, sustained-release glucose).** PLGA-microsphere-encapsulated glycoprotein scaffold delivering ~200 g glucose equivalent over 4–6 weeks subcutaneously. Covers the operator if oral intake is interrupted (combat trauma, bowel injury, mass casualty). See [`../Injectable Food.md`](../Injectable%20Food.md) and [`../Research Papers/Paper17_Injectable_Nutrition.md`](../Research%20Papers/Paper17_Injectable_Nutrition.md).
- **Pillar 2 — NutriComplete-P (injectable, complete nutrition).** Multi-domain protein scaffold delivering full caloric + protein + vitamin + mineral coverage over 6 weeks per ~50 mL subcutaneous injection. The TPN-replacement product for the same austere-environment scenarios.
- **Pillar 3 — TACT-1 Mark II (oral, full-day routine ration).** **This document.** Routine full-day caloric coverage at minimum carry weight (700 g/day), 4–6 hr per-bar satiety, complete micronutrients, no prep required.
- **Pillar 4 — ASNP (oral, energy-drink stimulant).** Caffeine + electrolyte + functional-ingredient product for acute high-exertion tactical windows. See [`../Research Papers/ASNP_Energy_Drink_Research_Paper.md`](../Research%20Papers/ASNP_Energy_Drink_Research_Paper.md).

The coherence of the stack arises from shared design choices: the chelated-mineral loading sequence (Ca²⁺ → Mg²⁺ → Fe³⁺ → trace) is identical across GlycoDur-P, NutriComplete-P, and TACT-1 Mark II; the fat-soluble-vitamin partitioning into the lipid phase is identical between NutriComplete-P (hydrophobic binding pockets) and TACT-1 Mark II (dissolution into MCT C8 oil); the slow-release glucose-polymer chemistry (branched α-1,4 / α-1,6 glycosidic architecture) is shared between the GlycoDur-P scaffold and the HBCD in the TACT-1 Mark II matrix. An operator on the integrated platform achieves a continuous nutritional baseline from the injectables and a routine high-density oral feed at a combined daily weight far below the standard MRE envelope.

---

## 🚧 Honest framing

- **Not clinically validated.** The 4–6 hour per-bar satiety claim is engineered from first principles (whey GLP-1/CCK release, casein gastric clot, HBCD slow-release, MCT C8 ketogenic floor) and is consistent with the published mechanism literature for each component, but the integrated bar has not been clinically validated for satiety duration in a controlled study. No HPLC mineral-stability verification at 40 °C over the target shelf life has been performed for the specific premix. The PDCAAS of the TGase-crosslinked casein is assumed (typical 5–10 % digestibility reduction vs native casein per the literature) but not measured for the specific TACT-1 Mark II formulation.
- **Commercial-in-Confidence label retained for tonal coherence.** No real SOCOMD or SASR sponsorship is implied. The "Commercial-in-Confidence" classification on the source spec is illustrative — adopted for register coherence with the rest of the Weapons-Defence portfolio.
- **No commercial supply chain exists.** The TACT-1 Mark II is a formulation specification, not a manufactured product. Industrial-scale procurement of each ingredient class (micellar casein vs caseinate, food-grade microbial TGase, MCT C8 powder, food-grade carnauba wax, food-grade shellac, chelated-mineral premix) is well-established for individual ingredients but the integrated supply chain for the specific TACT-1 Mark II formulation does not exist and would need to be developed against a real procurement programme.
- **Sensory acceptance is unmeasured.** The 40-variant flavour catalogue is engineered on a flavour-chemistry basis, not validated by sensory panel. The savoury family (variants 36–38) is included specifically to address palate fatigue on extended (> 72 hr) operations but the palatability claim is unverified.
- **The injectable pillars (GlycoDur-P, NutriComplete-P) are themselves hypothetical.** They are described in [`../Injectable Food.md`](../Injectable%20Food.md) and [`../Research Papers/Paper17_Injectable_Nutrition.md`](../Research%20Papers/Paper17_Injectable_Nutrition.md) as a design concept; no fielded injectable nutrition product exists at the spec-claimed performance. The integrated four-pillar platform is therefore a research portfolio's worth of *concept-level coherence*, not a fielded capability.

---

## 🔗 Related work in this repo

- [`../Injectable Food.md`](../Injectable%20Food.md) — GlycoDur-P / NutriComplete-P injectable nutrition concept (the architecture TACT-1 Mark II is derived from).
- [`../Research Papers/Paper17_Injectable_Nutrition.md`](../Research%20Papers/Paper17_Injectable_Nutrition.md) — Sustained-release injectable nutrition research paper.
- [`../Research Papers/ASNP_Energy_Drink_Research_Paper.md`](../Research%20Papers/ASNP_Energy_Drink_Research_Paper.md) — Companion energy-drink product within the same combat-nutrition stack.
- [`../Combat Drug.md`](../Combat%20Drug.md) and [`../Research Papers/Paper18_HyperSynergy_X7_Combat_Drug.md`](../Research%20Papers/Paper18_HyperSynergy_X7_Combat_Drug.md) — Pharmacology adjacency: the combat-drug stack that the nutrition platform operates alongside.
- [`../../Drugs/`](../../Drugs/) — Wider pharmacology research portfolio with cross-mirrored injectable-food and combat-drug documents.

---

[← Back to Weapons-Defence README](../README.md)
