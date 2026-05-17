# Weapons-Police — law-enforcement equipment R&D

> **Two Australian law-enforcement equipment prospectuses, each documented as a paired operator spec-sheet and academic research paper.** **APES-L Mark I** — full-body police body armour at 6.5 kg (versus 20 kg torso-only current): ionic-liquid STF carrier (cold-comfortable to −25 °C), 75 mm single-use B4C tiles to .50 AE, NIJ Level II stab full-body, 52.9 % blunt-trauma reduction, 66.2 % composite injury-score improvement, 14.7 % L4/L5 compressive-load reduction vs 11 kg torso-only vest (26 % vs 20.25 kg full-duty baseline), 12-year-plus panel service life, AUD $1.85 M TCO saving per 500 officers over 10 years — 23 physics-based simulations. **MP-4.6P Guardian LE** — police combat pistol in 4.6 × 22 mm DPAP at 396 m/s / 259 J: defeats NIJ IIIA soft armour (78 mm; 7.8× margin) and NIJ III hard plate (14.8 mm; 1.48× margin) plus all four common intermediate barriers; felt recoil 0.084 ft-lbf (≈ 50× lower than 9 mm); MRBF 20 548 rounds analytic / 27 778 simulated (90 % CI [15 152 – 29 412]); FTF rate 1:80 000; per-unit cost A$164 – 180 at mature production — 7-phase simulation programme. **Classification banners are stylistic — UNCLASSIFIED / FOUO format adopted for tonal coherence with the `../Weapons-Defence/` portfolio.** No real classification, sponsorship, or fielded materiel is implied.

> **Genre note.** Documents adopt the defence-research register used across the rest of this repository's defence portfolio (TRP designators, compliance-test framing, comparative tables, classification banners). No real procurement office, no real classification, no fielded system is implied. Both the APES-L Mark I and the MP-4.6P Guardian LE are design prospectuses, not fielded products.

---

## What this folder is

The `Weapons-Police/` folder is the law-enforcement-application cousin of the larger `../Weapons-Defence/` folder. It contains **two systems**, each documented as a paired operator specification sheet and academic-register research paper — matching the format used throughout the defence portfolio.

**APES-L Mark I** is the police variant of the military APES system documented in [`../Weapons-Defence/Advanced Protective Equipment System Specification.md`](../Weapons-Defence/Advanced%20Protective%20Equipment%20System%20Specification.md), adapted for the operational realities of Australian policing. Same three-layer architecture (NACS CORE undersuit + IL-STF full-body soft armour + ceramic torso tile array); four meaningful adaptations (single-use B4C tiles, ionic-liquid STF carrier, NIJ II / HG2 rather than rifle-grade ballistics, 6.5 kg vs 20.8 kg).

**MP-4.6P Guardian LE** is the police variant of the 4.6 mm family documented in [`../Weapons-Defence/MP-4.6M Pistol.md`](../Weapons-Defence/MP-4.6M%20Pistol.md) and [`../Weapons-Defence/MP-4.6M Defender PDW.md`](../Weapons-Defence/MP-4.6M%20Defender%20PDW.md). Same bore diameter, primer chemistry, projectile-tooling family, and parts-commonality targets; shortened 22 mm case (vs 30 mm military) reduces operating velocity to 396 m/s — the overpenetration-controlled regime appropriate for urban LE engagement.

---

## 📑 Source documents

### APES-L Mark I (body armour)

| Document | Role | Approx. length |
|---|---|---|
| [`APES-L Mark I Police Body Armour.md`](APES-L%20Mark%20I%20Police%20Body%20Armour.md) | Operator specification sheet — full system design prospectus, 17 sections, all 23 simulation summaries, weight budgets, TCO analysis, IP structure, final recommendation | ~700 lines |
| [`Research Paper - APES-L Police Body Armour.md`](Research%20Paper%20-%20APES-L%20Police%20Body%20Armour.md) | Academic-register research paper — abstract, introduction, background (current armour limitations + LEOKA wound data), materials & methods (7 materials streams + 23 simulation methods), results, discussion, limitations, conclusions, references | ~500 lines |

### MP-4.6P Guardian LE (combat pistol)

| Document | Role | Approx. length |
|---|---|---|
| [`MP-4.6P Guardian LE.md`](MP-4.6P%20Guardian%20LE.md) | Operator specification sheet — 17 sections covering all seven simulation phases, recoil / gas / structural / reliability results, Tier-2 surface engineering, compliance table, cost analysis, IP and procurement framework | ~700 lines |
| [`Research Paper - MP-4.6P Guardian LE.md`](Research%20Paper%20-%20MP-4.6P%20Guardian%20LE.md) | Academic-register research paper — abstract, introduction, background (LE handgun threat envelope), 7-phase methods with calibration references, results tables, discussion (LE landscape comparison, recoil, reliability), limitations, conclusions, 16 references | ~340 lines |

---

## 🧠 Headline numbers

| Parameter | APES-L Mark I | Current police vest |
|---|---|---|
| Total system weight (ready to wear) | **~6.5 kg** | 20.25 kg |
| Stab protection | **NIJ Level II — full body** | None |
| Ballistic protection | .44 Mag + 12 g slug + .50 AE (single-use tile) | HG2 torso (multi-hit aramid) |
| Blunt-trauma peak-pressure reduction | **52.9 %** vs HT-Kevlar | baseline |
| Composite injury-score improvement | **66.2 %** better | baseline |
| Coverage gap (standing) | **0.2 %** | 43.1 % |
| Cold-weather comfort limit | **−25 °C** (ionic-liquid STF) | −4 °C (PEG-carrier STF) |
| Upper temperature NIJ limit | **+45 °C** | +41 °C |
| Sealed-panel service life | **12 yr+** | 4.6 yr (Kevlar) |
| L4/L5 compressive load | **977 N** | 1 321 N (26 % lower) |
| 10-year TCO (500 officers, AUD) | **$3.37 M** | $5.22 M |
| 10-year saving | **+$1.85 M / 500 officers** | — |

All headline numbers trace to one of the twenty-three computational simulations documented in the operator spec sheet (Tables S1–S23). Physical NIJ testing remains the definitive validation pathway.

---

## 📐 The three-layer architecture at a glance

| Layer | Component | Weight | Function |
|---|---|---|---|
| 1 (skin) | **NACS CORE** undersuit — merino / silver-ion inner, GORE CHEMPAK CBRN membrane, sealed YKK + silicone interfaces at wrist / ankle / neck, PCM module removed for police variant | 1.65 kg base + 0.40 kg removable PCM | Compression, CBRN, antimicrobial, moisture management, sealed interfaces |
| 2 (middle) | **APES-L IL-STF** full-body soft armour — 12-layer alternating Kevlar 0.3 mm / UHMWPE 0.2 mm impregnated with ionic-liquid STF (EMIm-BF4 carrier, 60–65 % v/v SiO₂); covers flanks, arms, forearms, legs, knees, joints | ~2.7 kg | NIJ Level II stab + slash + blunt-trauma + cold-weather operation |
| 3 (outer torso) | **Single-use B4C tile array** — 75 mm square × 1.9 mm B4C tiles over 2 mm Al 5052 backing, 5 mm silicone connectors, 3 mm UHMWPE spall liner; 15 tiles per face, 30 tiles total | ~2.1 kg | Ballistic protection to .50 AE and 12 g slug, single-use replacement after strike |
| — | Carrier, MOLLE platform, quick-release, fasteners | ~0.35 kg | Hardware |
| **Total** | — | **~6.5 kg** | — |

Layer 1 is the same NACS CORE undersuit used as the foundation layer of the military APES platform documented in [`../Weapons-Defence/NACS TOTAL Camo and Undersuit.md`](../Weapons-Defence/NACS%20TOTAL%20Camo%20and%20Undersuit.md), minus its PCM module (Simulation 19 showed the NACS PCM is redundant when the APES PCM is present). Layer 2 is new — the ionic-liquid STF carrier is the materials-science delta that solves the cold-weather problem unaddressed by every commercial PEG-carrier system since 2006. Layer 3 is the police-specific economic delta — single-use replaceable tiles instead of pre-stressed multi-hit ceramic plates.

---

## 🔁 How this differs from the military APES

The Mark I is the **law-enforcement variant** of the APES platform whose military version is documented at [`../Weapons-Defence/Advanced Protective Equipment System Specification.md`](../Weapons-Defence/Advanced%20Protective%20Equipment%20System%20Specification.md) and [`../Weapons-Defence/Research Papers/Paper6_Body_Armor_System.md`](../Weapons-Defence/Research%20Papers/Paper6_Body_Armor_System.md). Same overall three-layer architecture (NACS CORE undersuit + soft-armour middle layer + ceramic torso layer). Four meaningful adaptations:

| Aspect | Military APES | APES-L Mark I (police) |
|---|---|---|
| Ceramic plates | Pre-stressed multi-hit B4C on Al 7075-T6 honeycomb + Ti-6Al-4V reinforcement, 5.5 kg per face | Single-use replaceable 75 mm B4C tiles, ~75 g per tile, 2.07 kg front + back combined |
| Soft-armour carrier | Aramid-thermoplastic + PEG-carrier STF (the standard) | Ionic-liquid carrier (EMIm-BF4) — cold-comfortable to −25 °C |
| Ballistic focus | NIJ Level III/IV (rifle threats) — torso + limbs | NIJ Level II / HG2 (handgun + shotgun + .50 AE) — torso only |
| Weight budget | 20.8 kg full system (military close combat, 72-hour CBRN) | 6.5 kg full system (20-year career biomechanical longevity) |

The rationale for each adaptation is documented under "Design Philosophy" (Section 2) of the operator spec sheet. In short: the operational hit-probability distribution for patrol policing does not justify the mass of pre-stressed multi-hit ceramic; the cold-weather problem is unsolved by all current commercial STF systems; the realistic threat is handgun + shotgun, not rifle; and the chronic-injury problem from 20 kg of concentrated torso load is the real long-term threat to officer health.

---

## 🛡 Honest framing

### APES-L Mark I

- **Simulation-based, pre-physical-test.** All twenty-three simulations are physics-based but reduced-order. **Physical NIJ certification testing — NIJ 0115.00 Level II stab and NIJ 0101.07 HG2 ballistic — remains the definitive validation pathway.** The simulation programme provides design guidance and pre-validation confidence; it does not substitute for compliance testing. Phase 1 of the development roadmap (Section 13 of the spec sheet) places independent-laboratory testing first.
- **0.50 BMG and rifle-grade threats are explicitly outside system capability.** The simulation searched to 30 mm of B4C and found no stoppage for .50 BMG. 7.62 × 51 NATO and .30-06 AP are similarly outside the single-ceramic-layer envelope. **This is a physics limit, not a design failure** — it applies equally to all current wearable police armour. For specialist units facing rifle threats, the Mark I is worn under a separate rifle-rated hard plate carrier.
- **The clinical injury-prevention argument needs longitudinal validation.** The lumbar-load reduction (26 % vs the 20.25 kg full-duty configuration baseline / 14.7 % vs the 11 kg torso-only vest baseline — both documented in Sim 2 and Sim 23) is biomechanically correct in the model, but the claim that this reduces officer career-injury rates requires a longitudinal officer cohort study. This study is identified as a required Phase 3 / Phase 4 task and is not yet performed.
- **Cost numbers assume triangular distributions.** Real procurement-cost variation may have heavier tails. The N = 10⁶ Monte Carlo result (88.6 % probability that Mark I is cheaper over 10 years) is robust to this assumption but the *magnitude* of saving is sensitive to it.
- **The IL-STF carrier (EMIm-BF4) is not at police procurement-volume manufacturing scale yet.** Ionic-liquid chemistry is established at laboratory and small industrial scale; the manufacturing infrastructure for tonne-scale STF impregnation at the cost target requires sponsor investment. This is scoped as a Phase 2 / Phase 5 commercialisation task in the spec sheet.
- **Classification banners are illustrative, not real.** UNCLASSIFIED / FOUO format adopted for tonal coherence with `../Weapons-Defence/`. No actual security classification, sponsorship, or procurement office is implied or held.

### MP-4.6P Guardian LE

- **Simulation-based, pre-physical-test.** Every performance claim is the output of the seven-phase Python simulation programme. Physical testing remains the definitive validation pathway. The simulator is deliberately conservative — the presented numbers are floor estimates.
- **The 4.6 × 22 mm DPAP cartridge has not been loaded or fired.** First-article proof loads are the only thing that closes the modelling loop on the interior-ballistics numbers.
- **Hard-armour envelope is bounded.** Defeats NIJ IIIA and NIJ III; does not defeat 15 mm RHA, NIJ IV SiC ceramic, or rifle-grade AP threats.
- **Reliability claims are Monte Carlo, not prototype-validated.** Per-mode rates are from surface-engineering literature; a 5 – 10 weapon × 5 000 round endurance programme is required to validate them on production hardware.
- **Tier-2 surface engineering (DLC + PVD-CrN + precision magazine + 100 % ammo QC) is load-bearing.** The 20 548-round MRBF specification is not met without the full Tier-2 package.

---

## 🧪 Validation pathways

**APES-L Mark I:** Bench coupon panels → independent NIJ-accredited lab → prototype build → NIJ 0115.00 Level II stab certification → NIJ 0101.07 HG2 ballistic certification (conditioned and new-condition) → extended ballistic testing against 12 g slug and .50 AE → 8-hour serving-officer comfort trial → cold-weather trial at −15 °C minimum → tile-replacement-protocol trial (target < 30 s replacement) → state-police procurement submission → manufacturing licence to Craig International Ballistics or Australian Defence Apparel → consumable tile-replacement supply chain. Full roadmap is Section 13 of the APES-L spec sheet.

**MP-4.6P Guardian LE:** First-article DPAP cartridge manufacture (100 rounds; chronograph + pressure test against simulator predictions) → 10 first-article weapon builds → bench test + 5 000-round endurance test across 10 weapons → NIJ-accredited terminal-ballistics testing → state-police user-acceptance trial (50 officers, 90-day carry) → procurement decision. Full roadmap is §15 of the Guardian LE spec sheet.

---

## 🔗 Related work in this repo

- [`../Weapons-Defence/`](../Weapons-Defence/) — the larger defence-engineering R&D portfolio, including the military APES specification ([`Advanced Protective Equipment System Specification.md`](../Weapons-Defence/Advanced%20Protective%20Equipment%20System%20Specification.md), [`Research Papers/Paper6_Body_Armor_System.md`](../Weapons-Defence/Research%20Papers/Paper6_Body_Armor_System.md)), the NACS CORE undersuit used as the Mark I base layer ([`NACS TOTAL Camo and Undersuit.md`](../Weapons-Defence/NACS%20TOTAL%20Camo%20and%20Undersuit.md)), and the AlNiCyN tiered aluminium armour ([`Aluminium Alloys for Armour.md`](../Weapons-Defence/Aluminium%20Alloys%20for%20Armour.md)) that is a candidate future tile-backing substrate.
- [`../Weapons-Defence/MP-4.6M Pistol.md`](../Weapons-Defence/MP-4.6M%20Pistol.md) — military parent of the 4.6 mm pistol family (4.6 × 30 mm Enhanced, 180 mm barrel, 501 m/s)
- [`../Weapons-Defence/MP-4.6M Defender PDW.md`](../Weapons-Defence/MP-4.6M%20Defender%20PDW.md) — PDW sibling (4.6 × 30 mm Enhanced, 266.7 mm barrel, 542 m/s)
- [`../Weapons-Defence/Common Architecture and Components.md`](../Weapons-Defence/Common%20Architecture%20and%20Components.md) — portfolio parts-commonality matrix; includes the 4.6 × 22 mm DPAP cartridge entry
- [`../Weapons-Defence/weapons_simulation.py`](../Weapons-Defence/weapons_simulation.py) — the single source of truth for all ballistic numbers
- [`../Drugs/`](../Drugs/) — pharmacology research, including the combat-drug and injectable-nutrition documents that the military APES variant references for extended operations endurance.
- [`../GM Enhancements/`](../GM%20Enhancements/) — HSA enhancement protocol (super-soldier programme adjacency to the military APES variant; not police-relevant in the Mark I configuration).
- [`../Diffusion Welding/`](../Diffusion%20Welding/) — UCDW field-repair-tier joining process, relevant to tile-backing substrate manufacturing and field replacement of tile-array components.
- [`../Rockwell 50 to 70 Carbide/`](../Rockwell%2050%20to%2070%20Carbide/) — sovereign carbide manufacturing platform (the H13 breech exemplar uses the same forge-to-machine economic logic as the tile manufacturing cost model).

---

[← Back to main README](../README.md)
