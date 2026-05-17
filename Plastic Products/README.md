# Plastic Products — injection-moulded civil infrastructure R&D (AusDike™ programme)

> **An Australian-manufactured, open-bottom self-ballasting, recycled-polypropylene modular flood-levee system in concept-feasibility and engineering-simulation closure.** This folder holds the new-product R&D programme for **AusDike™**, commissioned (in the framing of these documents) by **Holloway Group Pty Ltd** — the Sydney-based Australian injection moulder behind **Ausdrain™** (modular drainage cells, 1998 –), **Geohex™** (recycled-PP erosion-control cells), and **Biax Foundations™** (patented voided slab pods). The programme covers concept and market research (Vol.1), 28 engineering simulations across structural, multi-physics, FEA, system, and tooling domains (Vol.2), and a unified integrated write-up in academic-paper register. AusDike™ targets a real and documented A$6 B + / year Australian flood-damage problem with **no existing domestic manufacturer** of injection-moulded modular flood barriers; the engineering envelope closes (tipping SF 4.9× and sliding SF 2.1× on a self-stable 2-stack with no bracing); the economics close (A$65.51 COGS, A$109 / m sell, 42 % cheaper than imported Boxwall); and the one adverse finding (empty 2-stack panels fail tipping above 35 m/s wind) is addressed by deployment protocol rather than geometry change.

> **Genre note.** The Vol.1 and Vol.2 source documents adopt a *Commercial in Confidence — Holloway Group New Product Research Report* register for tonal coherence with how a real new-product feasibility programme inside an Australian injection moulder would be written. **No real commercial relationship between Holloway Group Pty Ltd and this repository is implied here.** The technical content (28 simulations, 9 simulation-driven design changes, the four-SKU family, the advanced-tooling cost breakdown) is real engineering work; only the Commercial-in-Confidence framing is stylistic.

---

## What this folder is

A single-product R&D programme captured in three documents plus this README. The product is **AusDike™** — a 600 × 300 × 560 mm recycled-PP injection-moulded panel designed to interlock side-to-side via push-fit trapezoidal tabs, stack vertically via a dovetail tongue (peel SF 1 243 000×), and self-ballast by allowing floodwater to enter through an open bottom and equalise hydrostatic pressure across the front and rear faces (**73 % net flood-force reduction**).

The folder is structured as the kind of documentation that would survive a transition from concept to tooling commitment: a feasibility & market volume, an engineering simulation volume, and a unified academic-style write-up that consolidates both into one paper a civil-engineering specifier, council infrastructure officer, or SES procurement reviewer could read end-to-end.

---

## 📑 Source documents

| Document | Role |
|---|---|
| **`AusDike Vol1 — Feasibility and Market.md`** | Vol.1 — concept design, hydrostatic-stability simulation v1 → v6 (depth iteration to 560 mm), 2-part-mould DFM checklist, Australian competitive landscape, indicative pricing, eight key findings, go-to-market phasing (SES → councils → critical infrastructure → mining / defence / export). |
| **`AusDike Vol2 — Engineering Simulation.md`** | Vol.2 — 28-simulation engineering closure across structural (wall-thickness sensitivity), 10-domain multi-physics (fatigue, creep, thermal, UV, seepage, chemistry, surge), four FEA analyses (MITC4 plate, Q4 plane stress, 20-element Euler-Bernoulli buckling), seven advanced verification sims (50 m / 83-panel system, uneven ground, wind, corner, two tolerance stack-ups, weld line), Cross-WLF rheology + 1-D cooling, advanced-tooling specification, first-principles COGS, four-SKU family. |
| **`AusDike — Integrated Research Paper.md`** | Unified academic-style write-up. Abstract, problem statement, design, 28-simulation methods, results (six tables: dimensional & material spec / safety factors / SKU family / fatigue-creep-UV / moulding process window / advanced-tooling cost breakdown), economics, brand-family discussion, limitations, conclusions, references. ~720 lines. |
| **`README.md`** | This file — folder-level orientation, headline numbers, SKU table, honest framing, cross-links. |

The Vol.1 and Vol.2 source documents were originally authored as HTML decks (`ausdike_report_final.html`, `ausdike_vol2_final.html`, and the visualisation deck `ausdike_visualisation.html`) and then converted to the Markdown files above; the HTML originals are not retained in the repository — the Markdown files are the canonical record.

---

## 🆚 Competitive landscape (snapshot)

| Solution | Origin | Material | Deploy | Reusable | Approx cost | Key weakness |
|---|---|---|---|---|---|---|
| Sandbags | Universal | Hessian + sand | Hours | No | A$2 – 5 / bag | Labour, single-use, ineffective at scale |
| Boxwall™ | 🇳🇿 NZ import | HDPE | 15 min | Yes | ~A$180 / m | Imported, expensive, limited AU stock |
| Geodesign | 🇩🇪 DE import | Galvanised steel + Al | 20 min | Yes | ~A$250 / m | Heavy, expensive, no recycled content |
| FloodFree | 🇦🇺 Aluminium | Aluminium | 30 – 60 min | Yes | ~A$300 / m | No sustainability story, costly install |
| Concrete jersey | Universal | Concrete | Days (crane) | Limited | ~A$400 / m | Permanent, crane-required |
| Earth levees | Universal | Compacted earth | Weeks | No | A$500 – 2 000 / m | Permanent, long lead time |
| **★ AusDike™ (proposed)** | 🇦🇺 Australia | Recycled PP | **10 min** | Yes | **~A$109 / m** | Pre-fill above 35 m/s wind |

The market has **no Australian-manufactured, injection-moulded, self-ballasting, rapid-deploy plastic flood barrier**. Every competitor is imported, made from metal, single-use, or machinery-dependent. AusDike™ closes all four gaps simultaneously.

---

## 🧠 Headline numbers

| Quantity | Value | Note |
|---|---|---|
| Length × Height × Depth | **600 × 300 × 560 mm** | 1 panel = 1 lineal metre barrier; 2-stack = 600 mm wall |
| **Wall thickness** | **9 mm** | **Column-buckling-governed**, not bending — central methodological finding of Vol.2 |
| Internal ribs | 3 × vertical at 150 mm | Bending span optimised |
| Polymer | **15 % talc-filled recycled PP + HALS** | HDT 55 → 85 °C; UV-stable for 25 yr |
| Empty mass | **~15 kg** | 2-person carry, no tools, no machinery |
| Filled mass (2-stack position) | ~125 kg | Water self-fill |
| Deploy time | **10 min for 50 m, 2 people, no tools** | vs ~15 min for Boxwall, hours for sandbags |
| **Net flood-force reduction** | **73 %** | Open-bottom self-ballasting — equalises hydrostatic pressure |
| **Tipping SF (2-stack, 600 mm flood, no bracing)** | **4.9×** | Target ≥ 2.0 ✅ |
| **Sliding SF (2-stack, 600 mm flood)** | **2.1×** | Target ≥ 1.5 ✅ |
| Column-buckling SF (9 mm wall) | 15.7× | Target ≥ 3.0 ✅ |
| Dovetail stacking-joint peel SF | 1 243 000× | Effectively un-peelable |
| 25-year Miner's fatigue damage `D` | 0.00975 | 103× life margin |
| Wind limit (empty 2-stack) | **35 m/s** | **Adverse finding — pre-fill or stake mandatory** above this |
| **COGS** | **A$65.51 / panel** | First-principles: material + machine + labour + 35 % overhead |
| **Sell price** | **A$109 / m** | 40 % gross margin; **42 % cheaper than imported Boxwall NZ at ~A$180 / m** |
| Tooling-breakeven volume | **3 500 panels** | Single SES tender (2 000 – 5 000 panels) clears tooling |
| Advanced tooling capex | A$382 500 | Hot runner + Stavax / Orvar / Elmax / Vanadis + DMLS conformal cooling + Kistler monitoring |
| Cycle time | 240 s (4 min) | Cooling is 51 % of cycle |
| Annual capacity | **59 750 panels** | 1 × 300-tonne machine, 2 shifts → **~A$6.2 M revenue / yr** |
| Design life | **25 years** | 100 % recycled-content polypropylene |

---

## 🧩 SKU family

The simulation programme produced a four-SKU family, with three of them sharing the primary mould tool:

| SKU | Designation | Polymer | Use case | Notes |
|---|---|---|---|---|
| **AusDike-S** | **Standard** | 15 % talc-filled recycled PP + HALS, dark navy | Council, SES, residential, commercial flood mitigation | The primary SKU; covers Brisbane summer service (72 °C) under 85 °C HDT |
| **AusDike-C** | **Cold climate** | 8 % rubber-toughened rTPP | Alpine resorts, southern councils, sub-zero storage | PP Izod halves at 0 °C — Vol.2 multi-physics finding |
| **AusDike-M** | **Mine / chemical** | HDPE | Hydrocarbon-bund walls, mining containment | PP chemical resistance to petroleum is 40 % — drives polymer switch (same tool) |
| **AusDike-X** | **90° Corner** | Talc-filled rPP + HALS | Every install needs 4 – 8 corners | 560 × 560 mm moulded corner piece, tipping SF 9.8×, **separate ~A$50 K tool** |

---

## 🛣 Development roadmap

| Phase | Milestone | Duration | Cumulative spend | Gate |
|---|---|---|---|---|
| 0 | CAD tolerance fixes (tab 0.40 → 0.60 mm; dovetail groove +0.5 mm) | 1 week | A$0 | Cleared CAD |
| 0 | Provisional patent on open-bottom + dovetail + front-face lock combination | 2 weeks | A$4 K | Priority date filed |
| 1 | Full parametric CAD + Moldflow + FEA-with-weld-lines | 4 – 6 weeks | ~A$15 K | Mouldflow-passed CAD |
| 2 | SLS / FDM prototype for fit-and-function | 2 – 3 weeks | ~A$20 K | Prototype validated |
| 3 | SES NSW / QLD engagement (Ausdrain relationships) — Letter of Intent target | parallel | A$20 K | LoI or council order ≥ 1 000 panels |
| 4 | Advanced tooling build + T1 / T2 / T3 samples | 5 – 7 months | ~A$405 K | Production-quality T3 samples |
| 5 | NATA AS/NZS certification (hydrostatic 72 h, UV 3 000 h, drop, chemical) | 4 – 6 months | ~A$465 K | Third-party certificate |
| 6 | Market launch — SES pilot, council channel via Ausdrain network | 3 – 4 months | — | First 500 units sold |
| 7 | Scale + SE Asia export + Mine SKU + Corner SKU additional tooling | year 2+ | +A$50 K (Corner tool) | A$2 M+ ARR |

Total time-to-first-sale: ~18 – 24 months from CAD commitment. Total pre-revenue capital: ~A$460 – 480 K.

---

## 🚧 Honest framing

- **This is a concept-feasibility programme, not a fielded product.** Vol.1 closed the market and concept stage; Vol.2 closed the engineering envelope with 28 first-principles simulations; the integrated paper unifies both. **No physical prototype has been built. No NATA-laboratory AS/NZS certification has been issued. No SES procurement has been placed.**
- **One adverse engineering finding.** Empty deployed two-stack panels lose tipping stability above ~35 m/s wind. The fix is operational, not geometric: **pre-fill with water or install ground stakes whenever forecast wind exceeds 35 m/s before flood arrival**. Once filled (the panel's operational state during a flood), it is stable to cyclonic-C conditions on top of the flood.
- **Polymer chemistry limits drive two SKUs.** The Standard SKU is recycled PP and is **not** rated for petroleum, hydraulic oil, or aviation fuel; mining bund-wall service uses the Mine SKU (HDPE, same tool, different feed). Alpine / southern service uses the Cold SKU (rubber-toughened rTPP).
- **The tooling commitment is sunk.** A$382 500 advanced tooling is not modular. The two CAD-stage tolerance fixes (tab clearance 0.40 → 0.60 mm; dovetail groove +0.5 mm) **must** be closed before tooling release. The recommended commercial gate is a Letter of Intent from SES NSW or QLD, or a confirmed council-channel order book ≥ 1 000 panels.
- **Commercial-in-Confidence framing is stylistic.** The Vol.1 and Vol.2 documents are written in the register of a real Holloway Group internal R&D report because that is the most honest register for the kind of work they contain. **No actual commercial relationship between Holloway Group Pty Ltd and this repository is implied.** The technical content is real engineering work; only the cover-page framing is stylistic.
- **Numbers are computed, not assumed.** Every safety factor, every cost element, every cycle-time component is computed from first principles in Vol.2. Where Vol.1 carried industry-rule-of-thumb estimates, Vol.2 superseded them — most notably the wall thickness (8 mm → 9 mm) and the empty mass (~11 kg → ~15 kg).

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — main repository index. This folder sits alongside the other Australian-manufacturing-feasibility work.
- [`../Weapons-Defence/`](../Weapons-Defence/) — the simulation-driven engineering register used here echoes the defence-engineering portfolio's pattern of paired operator-spec + research-paper documents with first-principles safety-factor tables. AusDike™ is a *civil* product (council and SES procurement, not defence procurement), but the documentation discipline is the same. The Vol.2 advanced-tooling cost breakdown also parallels the production-cost methodology used in the Rubber Tank Tracks TDP.
- [`../Rockwell 50 to 70 Carbide/`](../Rockwell%2050%20to%2070%20Carbide/) — sovereign Australian-manufacturing work; the forge-to-machine supply-chain economics and the explicit advanced-tooling cost build-up are written in the same register as Vol.2 § 06 (the AusDike advanced-tooling specification with Stavax / Orvar / Elmax / Vanadis grade choices).
- [`../Diffusion Welding/`](../Diffusion%20Welding/) — a Holloway-adjacency note. Where AusDike™ is a *primary* injection-moulded product, the UCDW diffusion-welding platform is the join-process counterpart for the metallic side of the same Australian-sovereign civil-engineering manufacturing pattern (modular hardware → field assembly → certified install). Both folders share the assumption that domestic manufacturing of large-format civil products is undervalued and capability-constrained rather than demand-constrained.
- The Vol.1 brand-family analysis (Ausdrain drains it → Geohex holds it → Biax displaces it → **AusDike stops it**) is the structural argument for why this product slots into an existing specifier channel.

---

## 🔤 Acronym key

| Term | Expansion | Note |
|---|---|---|
| **AusDike™** | (Brand — *Aus*tralian *dike*) | The flood-levee product family in this folder |
| **rPP** | Recycled polypropylene | Primary polymer (15 % talc-filled for the Standard SKU) |
| **HALS** | Hindered Amine Light Stabiliser | UV stabiliser; mandatory — without it, `Sy` degrades 30 % by year 8 |
| **HDT** | Heat-deflection temperature | 55 °C neat PP → 85 °C talc-filled PP |
| **HDPE** | High-density polyethylene | Mine SKU base polymer (petroleum-resistant) |
| **rTPP** | Rubber-toughened polypropylene | Cold SKU base polymer (Izod retention at 0 °C) |
| **MFI** | Melt-flow index | Polymer processability metric, g / 10 min @ 230 °C / 2.16 kg |
| **SF** | Safety factor | Ratio of capacity to demand; ≥ 2.0 tipping, ≥ 1.5 sliding, ≥ 3.0 buckling |
| **FEA** | Finite Element Analysis | Four codes used: MITC4 plate, Q4 plane stress, 20-element Euler beam, eigenvalue buckling |
| **MITC4** | Mixed-Interpolated Tensorial Components, 4-node | Shear-locking-free plate-bending element used for wall analysis |
| **SCF / Kt** | Stress Concentration Factor | Fillet-radius driver (1.87× → 1.53× on the 5 mm → 8 mm fillet change) |
| **DMLS** | Direct Metal Laser Sintering | Used for the 17-4 PH conformal-cooling inserts |
| **Stavax ESR / Orvar / Elmax / Vanadis** | Uddeholm tool-steel grades | Cavity / core / dovetail / tab insert steels in the advanced tooling package |
| **SES** | State Emergency Service | Primary launch customer (QLD / NSW / VIC / SA) |
| **NATA** | National Association of Testing Authorities | Required laboratory accreditation for AS/NZS certification |
| **AS/NZS** | Australian / New Zealand Standards | 4858 (water-contact), 4020 (drinking-water), 1170.2 (wind loading) are the target standards |
| **COGS** | Cost of Goods Sold | A$65.51 per panel, first-principles computed |
| **TPE** | Thermoplastic Elastomer | Base perimeter compression-lip gasket, Shore 45A |

---

[← Back to main README](../README.md)
