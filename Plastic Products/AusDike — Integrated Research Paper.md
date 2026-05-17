# AusDike™ — Integrated Research Paper

**An Australian-manufactured, injection-moulded, open-bottom self-ballasting modular flood-levee system: concept feasibility, multi-physics simulation, and production engineering**

> Holloway Group Pty Ltd · New Product R&D Programme · 2026
> Commercial in Confidence — research register; no real classification or commercial obligation is implied.
> Integrated write-up of *Vol.1 — Feasibility & Market* and *Vol.2 — Engineering Simulation Report* (28 simulations, 9 design changes).

---

## Abstract

We document the concept-to-tooling feasibility programme for **AusDike™**, a 600 × 300 × 560 mm injection-moulded modular flood-levee panel intended to be the first domestically-produced Australian competitor to imported steel and HDPE deployable flood-barrier systems. The panel exploits an **open-bottom self-ballasting principle** — floodwater enters through the panel base and equalises hydrostatic pressure across the front and rear faces, reducing net lateral force on the barrier by **73 %** relative to a sealed cell. Empty mass is ~15 kg per panel (two-person carry, no tools, no machinery); a 50 m run deploys in ~10 minutes with two operators. The 28-simulation engineering programme establishes that the wall is **column-buckling-governed** rather than bending-governed: wall thickness was increased from 8 mm to 9 mm on the strength of analytical Euler and 20-element eigenvalue FEA agreement (0.0 % error), and the polymer specification was tightened from neat recycled polypropylene to a **15 % talc-filled rPP with HALS UV stabiliser** (heat-deflection temperature 55 °C → 85 °C) to cover Brisbane solar service. At the final spec the panel achieves tipping safety factor 4.9× and sliding safety factor 2.1× on a two-stack 600 mm flood with no bracing, anchors, or flanges; column-buckling SF is 15.7×, and Miner's-rule fatigue damage at 25 years is 0.00975 (a 103× life margin). One adverse finding: **empty two-stack panels lose tipping stability above 35 m/s wind**, mandating a pre-fill-or-stake deployment protocol. A four-SKU family (Standard / Cold-climate / Mine-chemical / 90° Corner) is derived from the simulation set. COGS is computed from first principles at **A$65.51 per panel** (material, machine time, labour, 35 % overhead) against a target sell price of A$109 / linear metre — 42 % cheaper than the nearest reusable competitor (Boxwall NZ at ~A$180/m). Tooling-breakeven is 3 500 panels; a single state-emergency-services tender (2 000 – 5 000 panels) would clear the A$382 500 advanced-tooling capex. Annual capacity on one 300-tonne machine running two shifts is 59 750 panels (A$6.2 M revenue). Limitations: PP is incompatible with petroleum and hydraulic-oil bunding (drives the Mine SKU to HDPE); PP Izod halves at 0 °C (drives the Cold SKU to rubber-toughened rTPP); SES procurement cycles and NATA-laboratory AS/NZS certification remain uncertain. We classify this as **concept feasibility plus engineering-simulation closure**: the structural envelope is sound, the manufacturing process is computed, the economics close — but no physical prototype has been built, no NATA certificate has been issued, and no purchase order has been placed.

---

## 1. Introduction

### 1.1 The Australian flood problem

Flooding is now the single most expensive recurring natural disaster in Australia. The 2022 South-East Queensland and Northern New South Wales floods caused an insurance-bill loss above **A$6.8 billion** in one event — the costliest natural disaster in Australian history. The five-year rolling average of declared-disaster flood damage across QLD and NSW alone exceeds **A$6 billion / year**, with secondary cycles in Victoria, South Australia, and the Northern Territory. Climate-attribution modelling at the Bureau of Meteorology consistently projects this trend to **intensify**, not regress, through the 2030s and 2040s.

The federal response is the **Disaster Ready Fund**, which has committed **A$200 million per year** from 2023 onwards specifically toward flood-resilience infrastructure. Most of this flows through State Emergency Services (SES) agencies and the 537+ Australian local-government councils with declared flood-risk zones, and most of it is currently absorbed by earthworks (levees, drainage, channel works) and by imported deployable-barrier hardware.

### 1.2 The domestic-manufacturing gap

Despite a A$200 M / yr structural budget line and the largest civil-engineering-plastics market in the southern hemisphere (4.2 % CAGR through 2035 — Mordor Intelligence / IBISWorld), **there is no Australian injection-moulded modular flood-barrier producer**. Every reusable system on the market is one of:

1. **Imported** (Boxwall NZ, Geodesign Germany, FloodFree-style aluminium imports),
2. **Single-use** (sandbags — the universal default; labour-intensive; ineffective above ~300 mm flood depth at scale), or
3. **Permanent and machinery-deployed** (concrete jersey barriers, compacted-earth levees).

This is the white-space problem AusDike™ is intended to occupy.

### 1.3 Procurement context

Three structural tailwinds make the timing of a domestic injection-moulded flood barrier unusually favourable in 2026:

1. **Disaster Ready Fund cadence.** The federal A$200 M / yr line is now on its third funding round, and SES procurement officers have multi-year budgets to spend on resilience hardware rather than reactive sandbag logistics.
2. **Australian-made procurement scoring.** Federal and state procurement frameworks (Australian Industry Participation Plans, state-level Buy-Australian rules) now assign weighted procurement points to domestic-manufacture share, and recycled-content thresholds appear in many council infrastructure tenders. An imported HDPE barrier with no recycled content scores below a 100 %-recycled-content Australian-injection-moulded one even before price is considered.
3. **WHS weight regulations.** Workplace Health and Safety rules in QLD, NSW, and VIC now constrain single-person lifts on flood-response deployments. A 15 kg empty panel is comfortably inside the safe-lift envelope for one operator; concrete jersey barriers (~2 tonne) and steel Geodesign panels (~40 kg each) increasingly are not.

The intersection of these three tailwinds with a A$6 B / yr recurring damage problem is the procurement environment AusDike™ is being designed into.

### 1.4 The Holloway pattern

Holloway Group is a Sydney-based, Australian-owned injection moulder with 35+ years of operation and an explicit corporate pattern of taking heavy / expensive / unsustainable civil-engineering incumbents (gravel soak-away pits → **Ausdrain™**, concrete-and-bitumen slope erosion control → **Geohex™**, polystyrene waffle-pod slab foundations → **Biax Foundations™**) and replacing them with modular, interlocking, recycled-PP injection-moulded units. AusDike™ is the same pattern applied to flood barriers (sandbags + imported steel → recycled-PP self-ballasting panel). The capability set (concept-and-CAD, tool design, recycled-PP processing, civil/council specifier relationships) is in place; the question this paper addresses is whether the **engineering envelope** closes.

---

## 2. Problem statement

### 2.1 What a flood barrier has to do

A deployable flood barrier must, in the operational case:

1. **Stop water** to a stated head, with seepage low enough that pumping can keep the protected zone dry.
2. **Self-stabilise** under hydrostatic loading — neither tip forward (overturning), nor slide forward (sliding-friction failure), nor leak unacceptably at joints.
3. **Deploy fast** — the post-2022 SES doctrine target is ≤ 30 minutes per 50 m run with two operators and no machinery, beating the sandbag baseline by ~10×.
4. **Stack** to handle floods deeper than a single panel height.
5. **Stand down clean** — be reusable, washable, and storable on a single pallet per 50 m run.
6. **Cost less than the imported incumbent** at delivered specifier price.
7. **Survive the climate** — Australian solar UV, Brisbane summer heat-soak, alpine cold, coastal salt, repeated wet-dry cycles, 25-year design life.

### 2.2 What the existing inventory does and doesn't do

| Solution | Origin | Material | Deploy time | Reusable | Approx cost | Key weakness |
|---|---|---|---|---|---|---|
| Sandbags | Universal | Hessian + sand | Hours | No | A$2 – 5 / bag | Labour, single-use, ineffective at scale |
| Boxwall™ | 🇳🇿 NZ import | HDPE plastic | 15 min | Yes | ~A$180/m | Imported, expensive, limited Australian stock |
| Geodesign | 🇩🇪 German import | Galvanised steel + Al | 20 min | Yes | ~A$250/m | Heavy, expensive, no recycled content |
| FloodFree | 🇦🇺 Australia | Aluminium | 30 – 60 min | Yes | ~A$300/m | Metal, no sustainability story, costly install |
| Concrete jersey | Universal | Concrete | Days (crane) | Limited | ~A$400/m | Permanent, crane required, no rapid deploy |
| Earth levees | Universal | Compacted earth | Weeks | No | A$500 – 2 000 / m | Permanent only, long lead time, large footprint |
| **AusDike™ (proposed)** | 🇦🇺 Australia | Recycled PP | 10 min | Yes | ~A$109 / m | None identified at this spec; wind-on-empty protocol required |

The market has **no Australian-manufactured, injection-moulded, self-ballasting, rapid-deploy plastic flood barrier**. Every competitor is imported, made from metal, single-use, or machinery-dependent. AusDike™ closes all four of those gaps simultaneously and (per § 6) does so at an estimated delivered cost 42 % below the nearest reusable competitor.

---

## 3. Design

### 3.1 The open-bottom self-ballasting principle

The defining design idea is to use the flood as its own ballast. The panel is hollow with an **open bottom**, sealed against the ground only by a perimeter TPE compression lip. As floodwater rises on the protected side, it enters through the base and fills the interior cavity to within the head difference between the flood face and the protected face. The hydrostatic pressure pushing the barrier rearward is therefore **largely cancelled** by an equal hydrostatic pressure inside the cavity; only the differential head — typically far smaller than the absolute flood head — exerts net force.

Quantitatively, at 300 mm flood depth on a single panel (Vol.1 § 5):

| Parameter | Value | Notes |
|---|---|---|
| Flood pressure at base | 2.94 kPa | `ρgh` at 300 mm |
| Gross lateral force | 264.9 N / panel | Triangular distribution |
| Internal fill pressure | ~2.49 kPa | 85 % fill level |
| **Net lateral force** | **73.5 N / panel** | **73 % reduction** |
| Net overturning moment | 10.2 N·m | About front-bottom edge |
| Restoring moment | 36.6 N·m | Mass × D / 2 |
| Tipping safety factor | 3.58× | Target ≥ 2.0 |
| Sliding safety factor | 2.11× | Target ≥ 1.5 |

The same principle is used by the imported Boxwall system; the contribution here is to deliver it at a fraction of the material cost via Australian injection moulding of recycled PP.

### 3.2 Geometry — three locked axes

The panel locks in three orthogonal axes:

- **Horizontal (side-to-side):** two male trapezoidal tabs (30 mm base × 22 mm tip × 25 mm deep) on the right edge engage matching female recesses on the left edge of the adjacent panel. Push-fit, tool-free, **0.60 mm** nominal clearance (Vol.2 finding — raised from the concept-stage 0.40 mm to clear worst-case tolerance jam).
- **Vertical (stack):** a **dovetail tongue** (22 mm base × 30 mm tip × 14 mm tall) runs the full 570 mm top edge. A matching dovetail groove on the bottom edge interlocks. Because the geometry is dovetail rather than rectangular, the joint **cannot peel** under lateral load — the upper panel can only separate by lifting straight up against its own weight plus the ground-seal grip of the lower panel. Peel safety factor at flood load: **1 243 000×**.
- **Forward-slide lock:** a 15 mm button-and-socket integral feature on the front face at 150 mm height prevents an upper stacked panel from creeping forward off the lower one under lateral load. Moulded directly into the part — no separate hardware.

### 3.3 The depth-iteration history (Vol.1)

The 560 mm base depth is the single most consequential geometric parameter — it sets the moment arm of the panel's self-weight (and therefore self-ballasted water mass) about the front-bottom edge that the flood is trying to overturn the panel around. Vol.1 ran a seven-iteration sweep through bottom-condition and depth combinations:

| Iteration | D (depth) | Bottom | Tip SF @ 300 mm (single) | Slide SF @ 300 mm (single) | 2-stack Tip SF | Decision |
|---|---|---|---|---|---|---|
| v1 — Original | 200 mm | Closed | 1.37× | 0.61× | 0.59× | ❌ Fails sliding |
| v2 — Open bottom | 200 mm | Open | 3.24× | 2.03× | 0.59× | ⚠️ Single OK, stack fails |
| v3 — Wider base | 350 mm | Open | 9.90× | 3.54× | 1.81× | ⚠️ Stack marginal |
| v4 — Min viable | 420 mm | Open | 13.2× | 1.51× | 2.61× | ⚠️ Slide borderline |
| v5 — Balanced | 500 mm | Open | 18.7× | 1.80× | 3.69× | ⚠️ Slide still low |
| **★ v6 — Final** | **560 mm** | **Open** | **22.2×** | **2.02×** | **4.63×** | **✅ All targets met** |
| v7 — Over-engineered | 700 mm | Open | 34.7× | 2.52× | 7.23× | Unnecessary bulk |

The v1 → v2 step (closing-to-open bottom) is the introduction of the self-ballasting principle and accounts for the bulk of the single-panel improvement. The v2 → v6 sweep is depth optimisation under the new principle. v6 was selected as the smallest depth that simultaneously cleared **all** tipping, sliding, and 2-stack targets without bracing, anchors, flanges, or any post-deployment accessories — the explicit design requirement.

### 3.4 The nine simulation-driven design changes

The concept-to-Vol.2 trajectory closed nine specific design changes, **all of them simulation-driven**:

| # | Change | Driver |
|---|---|---|
| 1 | **Wall 8 mm → 9 mm** | Column buckling under fill weight governs. Analytical Euler and 20-element eigenvalue FEA agree to 0.0 % error. SF 3.6× → 15.7× |
| 2 | **rPP → 15 % talc-filled rPP** | Brisbane solar service heats panel to ~72 °C; neat-PP HDT is 55 °C. Talc raises HDT to 85 °C |
| 3 | **HALS UV stabiliser mandatory** | Without HALS, `Sy` degrades 30 % by year 8 — structural failure within design life |
| 4 | **Tab clearance 0.40 → 0.60 mm** | Tolerance stack-up: worst-case clearance was 0.00 mm (assembly jam) |
| 5 | **Dovetail groove +0.5 mm wider** | Worst-case tolerance gave **0.20 mm interference**; panels physically would not stack |
| 6 | **Rib-wall fillet 5 mm → 8 mm** | FEA stress-concentration factor 1.87× → 1.53× |
| 7 | **Tab height 12 mm → 8 mm** | FEA SF at tab root = 858× — mass-saving without functional penalty |
| 8 | **Wind deployment protocol added** | Empty two-stack panel fails tipping above 35 m/s wind; pre-fill or stake mandatory |
| 9 | **Cold SKU + Mine SKU added** | PP Izod halves at 0 °C; PP chemical resistance to petroleum is 40 %. Two new material variants |

Changes 4 and 5 are **must-fix-before-tooling** — they cost nothing in CAD and would cost A$15 000+ to rework an already-cut tool. Changes 1 – 3 and 6 are simulation-driven specification choices that flow into the tooling package directly. Changes 7 – 9 are mass-saving or protocol additions that do not affect the primary geometry.

---

## 4. Methods

### 4.1 The 28-simulation programme

The simulation set was structured into five domains. Every analytical result was self-written from first principles; FEA codes (MITC4 Mindlin plate elements, Q4 plane-stress elements, 20-element Euler-Bernoulli beam) were also written from scratch and cross-validated against closed-form results where available.

| Domain | Analyses | Scope |
|---|---|---|
| **Structural** | 8 | Wall-thickness sensitivity, bending, buckling, tipping, sliding, shear, deflection, hydrostatic loading |
| **Multi-physics** | 10 | Bending / buckling / tipping / sliding · fatigue (25 yr) · creep (10 yr) · thermal (4-city) · UV degradation · seepage · chemical resistance · surge dynamics |
| **FEA** | 4 | Wall-panel MITC4 bending · rib-wall Q4 fillet SCF · tab-root Q4 SF · dovetail-peel Q4 |
| **System / advanced verification** | 7 | 50 m multi-panel (83-panel) system · uneven-ground rocking · wind-overturn (4 wind classes) · corner panel (45° mitre vs moulded 90°) · tolerance stack-up tab · tolerance stack-up dovetail · weld-line strength |
| **Tooling / process** | 4 | Cross-WLF rheology · 1-D thermal cooling · flow-path fill pressure · cycle-time decomposition |

### 4.2 Methodological insight: buckling governs

The wall acts as a vertical **column** carrying the compressive weight of the upper stacked panel and the water it contains (1 547 N/m width axial load). It does **not** act primarily as a plate carrying transverse flood pressure. At 9 mm wall thickness in talc-filled rPP, the various safety factors are:

| Failure mode | SF @ 9 mm talc-filled |
|---|---|
| Shear | 587× |
| Deflection (a / 100 limit) | 247× |
| Bending (plate) | 89× |
| **Column buckling** | **15.7×** ← governs |
| Thermal stress | 6.0× |

The bending plate stress under flood load is **less than 1 % of yield**. The wall is column-sized, not plate-sized. This single insight collapses an entire family of would-be design changes (more ribs, higher-yield PP grades, thicker-wall-for-bending) into a much smaller decision: pick the wall thickness that gives the right buckling SF, and pick a polymer with the right HDT and `E`. The 20-element Euler-Bernoulli beam FEA reproduces Euler's analytical buckling load to 0.0 % error — the analytical method is independently validated and is used as the primary sizing tool throughout.

This is the central methodological finding of Vol.2 and the one that most distinguishes the AusDike™ engineering from rule-of-thumb-driven plastic-panel design.

### 4.3 FEA implementation details

Four distinct FEA approaches were used. All were written from first principles and cross-validated against closed-form solutions where one existed:

| Analysis | Element type | Mesh | Verification |
|---|---|---|---|
| Wall-panel bending under hydrostatic load | MITC4 Mindlin plate (4-node, shear-locking-free) | 128 elements | Cross-checked against Roark's simply-supported plate formula; FEA returns deflections 21 % higher than Roark, consistent with FEA capturing the triangular load distribution more accurately than the uniform-load formula |
| Rib-wall junction stress concentration | Q4 plane stress | 80 elements | Peterson SCF chart at fillet radius / wall thickness = 5/9 yields `Kt ≈ 1.87`; FEA confirms; upgrade to 8 mm fillet gives `Kt ≈ 1.53` |
| Interlock tab root | Q4 plane stress | 50 elements | Hand-calc cantilever-beam bending; FEA agrees within 4 % |
| Eigenvalue column buckling | 20-element Euler-Bernoulli beam | 20 elements | Reproduces Euler `P_cr = π²EI/L²` to 0.0 % error — independently validates the analytical sizing method |

The MITC4 plate code, the Q4 plane-stress code, and the eigenvalue beam code together constitute approximately 800 lines of self-written analysis code. None of the structural conclusions of this report rest on a single commercial FEA package result.

### 4.4 Process-engineering methodology

The injection-moulding process window was computed rather than estimated. The Cross-WLF viscosity model

$$\eta(\dot\gamma, T) = \frac{\eta_0(T)}{1 + (\eta_0 \dot\gamma / \tau^*)^{1-n}}$$

(with `η₀ = 850 Pa·s`, `τ* = 25 000 Pa`, `n = 0.35` calibrated for 15 % talc-filled rPP at 230 °C) was solved across shear rates 1 – 10 000 s⁻¹. Gate shear stress at the operational injection rate works out to 81 847 Pa — well under the PP molecular-degradation threshold of 250 000 Pa. The 1-D heat-conduction cooling time `t = h² / (π²α) · ln(4ΔT / π)` for the 9 mm wall with thermal diffusivity `α = 1.38 × 10⁻⁷ m²/s` yields 122 s — the dominant phase of the 240-s cycle. Total injection pressure was traced flow-path-by-flow-path (worst case: 860 mm corner path, `L/t = 96` against an industry limit of 200) for a final 17.5 MPa — very low for the part size.

---

## 5. Results

### 5.1 Final dimensional and material specification

| Parameter | Value | Driver |
|---|---|---|
| Length | 600 mm | 1 panel = 1 lineal metre barrier |
| Height | 300 mm | 2-stack = 600 mm wall |
| Base depth | **560 mm** | Tipping-stability-governed (Vol.1 simulation) |
| **Wall thickness** | **9 mm** | **Column-buckling-governed** (Vol.2) |
| Internal ribs | 3 × vertical at 150 mm spacing | Bending span optimised |
| Draft angles | 2.0° all faces, 1.5° dovetail faces | Mould release |
| Internal fillets | 8 mm (upgraded from 5 mm) | FEA SCF analysis |
| External fillets | 3 mm | All external edges |
| Base opening corner | 8 mm radius (upgraded from 3 mm) | Peterson `Kt` reduction |
| Tab height | 8 mm (reduced from 12 mm) | FEA SF 858× |
| **Base polymer** | **Recycled PP homopolymer** | Post-consumer / post-industrial feedstock |
| **Filler** | **15 % talc by weight** | HDT 55 → 85 °C |
| **UV stabiliser** | **HALS — mandatory** | Without it, fails year 8 |
| `E` (talc-filled) | 1 800 MPa | vs 1 200 MPa neat |
| `Sy` (talc-filled) | 22 MPa | vs 18 MPa neat |
| HDT (talc-filled) | 85 °C | Covers Brisbane solar |
| MFI | ~10 g / 10 min @ 230 °C / 2.16 kg | Process window centre |
| Colour | Dark navy (moulded-in) | Carbon MB aids UV further |
| Empty mass | ~15 kg | 2-person carry; ~11 kg in Vol.1, raised by Vol.2 wall change |
| Filled mass | ~87 kg / panel (single), ~125 kg / position (2-stack) | Water self-fill |

### 5.2 Safety factors across all physics domains

| Domain | Quantity | Value | Target | Status |
|---|---|---|---|---|
| **Structural — single panel** | Tip SF @ 300 mm flood | 22.2× | ≥ 2.0 | ✅ |
|  | Slide SF @ 300 mm flood | 2.02× | ≥ 1.5 | ✅ |
| **Structural — 2-stack** | Tip SF @ 600 mm flood | 4.9× | ≥ 2.0 | ✅ |
|  | Slide SF @ 600 mm flood | 2.1× | ≥ 1.5 | ✅ |
| **Wall** | Buckling SF | 15.7× | ≥ 3.0 | ✅ |
|  | Bending SF | 89× | ≥ 2.0 | ✅ |
|  | Shear SF | 587× | ≥ 2.0 | ✅ |
| **Stacking joint** | Shear SF (tongue) | 1 255× | ≥ 2.0 | ✅ |
|  | Peel SF (dovetail) | 1 243 000× | ≥ 2.0 | ✅ |
| **Side connection** | Tab shear SF @ tab root | 858× | ≥ 2.0 | ✅ |
| **System (50 m / 83 panels)** | Max tab connection force | 81 N | — | ✅ (SF 39×) |
| **Uneven ground (20 mm spec)** | Tip SF | 11.6× | ≥ 2.0 | ✅ |
| **Surge (3 m/s)** | Wall SF | 3.2× | ≥ 2.0 | ✅ |
| **Weld line (62 % strength)** | SF | 63× | ≥ 2.0 | ✅ — impact test mandatory |
| **Wind — sheltered suburban (35 m/s)** | 2-stack tip SF (empty) | **0.79×** | ≥ 1.0 | **❌ — pre-fill or stake** |
| **Resonance** | Panel `fn` vs flood surge | 159 Hz vs ~1 Hz | — | ✅ (159× ratio) |
| **Seepage** | Per joint | 0.12 mL / min | < 1 L / min / panel | ✅ |

The one **non-passing** entry is wind on an empty deployed two-stack panel above 35 m/s — addressed by deployment protocol rather than geometry change (see § 8.1).

### 5.3 SKU family

| SKU | Designation | Polymer | Use case | Tooling impact |
|---|---|---|---|---|
| **AusDike-S** | Standard | 15 % talc-filled rPP + HALS, dark navy | Civil flood, council, SES — the primary SKU | Base tool |
| **AusDike-C** | Cold-climate | 8 % rubber-toughened rTPP | Alpine, southern councils; PP Izod halves at 0 °C | Same tool, different material |
| **AusDike-M** | Mine / chemical | HDPE | Mining bunding; PP chemical resistance to petroleum is 40 % | Same tool, different material |
| **AusDike-X** | 90° Corner | Talc-filled rPP + HALS, dark navy | Every install needs 4 – 8 corners; 560 × 560 mm footprint; tip SF 9.8× | Additional ~A$50 K corner tool |

### 5.4 Long-life and environmental performance

| Quantity | Value | Limit / target | Status |
|---|---|---|---|
| Fatigue — Miner's `D` (9 125 thermal + 125 flood cycles, 25 yr) | 0.00975 | < 1.0 | ✅ (103× life margin) |
| Creep deflection @ 10 yr sustained 0.02 kPa | 0.019 mm | < 2.0 mm | ✅ |
| UV — `Sy` @ 25 yr with HALS | 21.2 MPa | ≥ 12 MPa for SF 1.5× | ✅ (SF 85×) |
| UV — `Sy` @ 8 yr without HALS | ~15 MPa | ≥ 18 MPa | ❌ — HALS mandatory |
| Sydney summer service | 65 °C | < HDT 85 °C | ✅ |
| Brisbane peak solar | 72 °C | < HDT 85 °C | ✅ |
| Darwin storage | 58 °C | < HDT 85 °C | ✅ |
| Alpine winter | −5 °C | > Tmin −20 °C | ✅ (Cold SKU recommended) |
| Seawater chemical resistance | 100 % | — | ✅ |
| Dilute acid (runoff) | 90 % | — | ✅ |
| Sewage / biological | 95 % | — | ✅ |
| Petroleum / hydrocarbon | 40 % | — | ❌ → Mine SKU (HDPE) |

### 5.5 Injection-moulding process window

| Parameter | Range | Setpoint | Note |
|---|---|---|---|
| Melt temperature | 225 – 240 °C | 230 °C | Talc-filled rPP |
| Mould temperature | 40 – 55 °C | 45 °C | Conformal-cooled |
| Injection speed | 80 – 150 cm³/s | 120 cm³/s | Fan gate, no jetting |
| Pack pressure stage 1 | 50 – 65 MPa | 58 MPa | 80 % of inject; t = 0 – 5 s |
| Pack pressure stage 2 | 38 – 50 MPa | 43 MPa | 60 % of inject; t = 5 – 13 s |
| Pack pressure stage 3 | 25 – 40 MPa | 28 MPa | 40 % of inject; gate freeze t ≈ 20 s |
| Screw speed | 40 – 80 RPM | 55 RPM | Moderate — talc wear |
| Back pressure | 3 – 8 MPa | 5 MPa | Melt homogenisation |
| Total injection pressure | — | **17.5 MPa** | Very low for part size; L/t max 96 vs limit 200 |
| Gate shear stress | — | 81 847 Pa | Well under PP degradation 250 000 Pa |
| Clamp force | — | ~300 tonne | 0.336 m² × 7 MPa × 1.25 |
| Shot weight (1 cavity) | — | 14.9 kg | Hot runner, zero runner waste |
| **Cycle time** | — | **~240 s (4 min)** | Cooling is 51 % of cycle |
| Cooling-water flow | — | 83 L / min | 4 conformal circuits, Re ≈ 147 000 (turbulent) |
| Anisotropic shrinkage allowance | — | 0.84 % ∥, 1.38 % ⊥ | Toolmaker must scale anisotropically |

### 5.6 Advanced tooling cost breakdown

| Line item | A$ |
|---|---|
| Mould design + Moldflow simulation | 30 000 |
| Stavax ESR cavity (CNC + EDM + polish) | 85 000 |
| Orvar Supreme core (CNC + EDM) | 70 000 |
| DMLS conformal cooling (4 zones) | 45 000 |
| Elmax PM dovetail inserts (×2) | 14 000 |
| Vanadis 4 Extra PM tab / recess inserts (×4) | 12 000 |
| PVD TiAlN coating (all sliding faces) | 8 000 |
| Hot runner (Mold-Masters single-drop valve gate) | 35 000 |
| Hydraulic stripper plate | 22 000 |
| Glycodur bushings + air-ejection assist | 9 000 |
| Kistler cavity pressure sensors + monitoring | 20 500 |
| T1 trial + optimisation | 20 000 |
| T2 sign-off + first article inspection | 12 000 |
| **TOTAL — advanced tooling** | **382 500** |
| Baseline tooling (P20 / H13 / cold runner) for comparison | 160 000 |
| Premium over baseline | +222 500 |

Each premium item is independently justified. The hot runner (+A$35 K) eliminates cold-runner regrind of already-degraded recycled PP and pays back in under 10 months from material savings alone. Stavax ESR (+A$25 K over P20) resists trace acids in recycled-PP feedstock and breaks even versus a single P20 cavity repolish by year 3. Conformal cooling (+A$45 K) is justified on warpage control (±1 °C vs ±3 °C surface temperature uniformity), not cycle-time reduction — a 600 × 560 mm flat panel that warps 2 mm is scrap.

---

## 6. Economics

### 6.1 Unit cost breakdown

| Cost element | A$ / panel |
|---|---|
| Material — 14.9 kg talc-filled rPP @ ~A$1.55 / kg | 23.07 |
| Machine time — 4 min @ A$280 / hour rate | 18.67 |
| Labour + supervision | 4.40 |
| Overhead (35 %) | 16.22 |
| **COGS** | **65.51** |

### 6.2 Sell price and competitive position

| Quantity | Value |
|---|---|
| COGS | A$65.51 / panel |
| Target sell price | **A$109 / linear metre** |
| Gross margin | ~40 % |
| Boxwall NZ import | ~A$180 / m |
| Price advantage vs Boxwall | **42 % cheaper** |
| Geodesign DE steel import | ~A$250 / m |
| Council kit (50 m AusDike) | ~A$5 450 |
| Council kit (50 m Boxwall) | ~A$9 000 |

### 6.3 Tooling-breakeven volume

| Volume | Tool cost / unit | Total delivered sell | Viable? |
|---|---|---|---|
| 500 panels | A$765 | A$874 / m | ❌ Too early |
| 1 000 panels | A$383 | A$448 / m | ⚠️ Pre-orders only |
| 2 500 panels | A$153 | A$218 / m | ⚠️ Approaching |
| **3 500 panels** | **A$109** | **A$175 / m** | **✅ Competitive** |
| 5 000 panels | A$77 | A$143 / m | ✅ Strong margin |
| 10 000 panels | A$38 | A$124 / m | ✅ Full margin |

### 6.4 Capacity and revenue

One 300-tonne machine running two 8-hour shifts at 240-s cycle yields **239 panels / day**, **59 750 panels / year**. At A$109 / m sell price this is **A$6.51 M revenue / year / machine**, which the Vol.2 report rounds to A$6.2 M after delivery and discount allowances. A single SES NSW + QLD tender for flood-response equipment is estimated at 2 000 – 5 000 panels — sufficient on its own to clear the A$382 500 tooling capex and put the product into profitable territory from launch.

---

## 7. Discussion

### 7.1 Brand-family fit

Holloway's existing product portfolio follows one pattern across four generations:

| Brand | What it replaces | Where water is |
|---|---|---|
| **Ausdrain™** (1998) | Gravel soak-away pits | Drains it underground |
| **Geohex™** | Concrete and bitumen erosion control | Holds it on slopes |
| **Biax Foundations™** | Polystyrene waffle pods | Displaces it under slabs |
| **AusDike™** (proposed) | Sandbags + imported steel | **Stops it entirely** |

The brand story writes itself: *Ausdrain drains it. Geohex holds it. Biax displaces it. AusDike stops it.* This is not marketing dressing — it is the actual specifier-relationship leverage. Civil engineers and council infrastructure officers who already specify Ausdrain into stormwater designs and Geohex onto access roads are the **same** specifier audience that signs off SES procurement of deployable flood-protection hardware. AusDike inherits an existing channel.

### 7.2 White-space competitive position

The opportunity space is delimited cleanly. Every competitor fails at least one of *{Australian-made, modular, injection-moulded, recycled-content, self-ballasting, machinery-free, rapid-deploy, reusable}*. Sandbags fail seven of eight. Boxwall fails three (imported, expensive, no recycled content). Geodesign fails four. FloodFree fails three. Concrete jersey barriers fail five. AusDike, as specified, fails zero on its intended-use envelope (with the wind-on-empty caveat addressed by protocol).

### 7.3 Export TAM

South-East Asia (Vietnam, Thailand, Philippines, Bangladesh) is the largest flood-affected region globally outside South Asia, and the regional injection-moulding manufacturing base for civil-grade products is thin. A licensed-tooling or finished-goods export programme has been informally scoped at A$50 M + addressable annually. The same export channels Holloway uses for Ausdrain are open.

### 7.4 Simulation-driven engineering as a method

The Vol.2 programme is unusual in the SME injection-moulding world in two ways. First, **every design change is justified by a computed result**, not by industry rule-of-thumb. Second, **the methodological insight (buckling, not bending, governs)** was found by the simulation programme itself rather than imported from design experience — the original concept-stage wall thickness of 8 mm was sized by bending intuition and turned out to be the wrong dominant mode. This sort of engineering rigour is normally only seen in much larger civil-engineering products (aerospace, automotive, defence). Bringing it to a council-scale flood barrier is part of the value proposition.

### 7.5 Why advanced tooling — and why now

The A$222 500 premium of the advanced tooling package over a baseline P20 / H13 / cold-runner build is not optional optimisation. Each premium item maps onto a specific physical risk identified in the simulation programme:

- **Hot runner (+A$35 K)** eliminates cold-runner regrind. Recycled-PP feedstock is already at the lower end of the molecular-weight distribution; a single regrind pass degrades `Mw` by an additional ~5 – 8 %. Cold runners would silently compound this every shot. Payback under 10 months on material savings alone (zero runner waste vs ~452 g per shot).
- **Stavax ESR (+A$25 K over P20)** is stainless. Recycled-PP volatiles include trace acetic acid and chloride residues from PVC contamination in the post-consumer feedstock; P20 rusts inside the cavity within 12 – 18 months of recycled-PP operation. One P20 cavity repolish at A$40 K every 24 months makes Stavax cheaper by year 3.
- **Orvar Supreme core (+A$15 K over H13)** is premium-chemistry H13 with tighter inclusion control. The benefit is **polishability in deep ribs** (three vertical ribs the full panel height) — surface finish drives ejection-force consistency.
- **Elmax PM dovetail and Vanadis 4 Extra PM tab/recess inserts (+A$3 K total over baseline)** are powder-metallurgy steels with ~3× the wear resistance of S7 and D2 respectively. The tab inserts engage every shot (~60 000 shots / year / cavity); 3× wear life means insert replacement every 28 years rather than every 9.
- **PVD TiAlN coating (+A$8 K)** on sliding faces eliminates the mould-release-spray requirement entirely (40 % friction reduction) and prevents galling on the inserts.
- **DMLS conformal cooling (+A$45 K)** is the warpage-insurance item. Vol.2 found that warpage is the **#1 manufacturing risk** for a 600 × 560 mm flat panel with asymmetric ribs. ±1 °C cooling uniformity (conformal) vs ±3 °C (straight-drilled) is the difference between a flat panel and a 2 mm-bowed scrap part. The cooling-cycle-time reduction is secondary — for a 9 mm PP wall, polymer thermal conductivity is the bottleneck, not channel geometry.

The whole tooling package is also designed for **low ongoing maintenance** — Holloway's stated tooling philosophy. Annual maintenance cost is A$5 – 8 K against A$15 – 25 K for a conventional build. Over a 10-year tool life that recovers ~A$100 K, partially offsetting the upfront premium.

### 7.6 Recycled-PP supply chain leverage

Holloway already buys recycled PP for Geohex (interlocking erosion-control cells) and post-industrial PE/PP for Biax (slab pods). The talc-filled rPP feedstock for AusDike-S is a 15 % filler addition on the same base polymer Geohex consumes today — same supplier relationships, same quality-control regime, same MFI window (10 – 18 g / 10 min @ 230 °C). The Mine SKU's HDPE switch reuses an existing Ausdrain feedstock channel. No new supplier qualification is required to start production.

---

## 8. Limitations and risks

### 8.1 Wind on empty panels (the one adverse finding)

Empty two-stack panels lose tipping stability above **35 m/s wind** (sheltered suburban — Wind Region A serviceability). At 45 m/s (open terrain) even a single-stack empty panel fails. The mitigation is operational: **pre-fill with water or install ground stakes whenever forecast wind exceeds 35 m/s before flood arrival**. This must be embedded in the SES deployment-protocol documentation. It is not a geometry change because once the panel is filled (its operational state during a flood) it is self-stable to cyclonic-C wind on top of the flood.

### 8.2 Polymer chemistry incompatibilities

The Standard SKU is recycled PP and is acceptable for fresh / sea / sewage / dilute-acid / alkali service but **not** petroleum, hydraulic oil, or aviation fuel — chemical-resistance ratings of 40 % and 50 % respectively. Mining bund-wall service requires the Mine SKU (HDPE), which uses the **same tool** with a different polymer feed. Alpine and southern service (Izod halving at 0 °C) requires the Cold SKU (rubber-toughened rTPP).

### 8.3 SES procurement cycle uncertainty

SES procurement cycles run annually and are sensitive to political and budget timing. A single state-wide tender clears the entire tooling investment, but the timing of that tender is exogenous. Phase-1 council procurement provides a smaller but more diversified launch channel.

### 8.4 Tooling capex is a sunk cost

The A$382 500 advanced tooling package is not modular — once committed, it is committed. The two CAD-stage tolerance fixes (tab clearance, dovetail groove width) **must** be closed before tooling release; rework after the cavity has been cut is A$15 000+ per pass. The recommendation is to gate the tooling commitment behind a Letter of Intent from SES NSW or QLD, or a confirmed Phase-1 council order book of ≥ 1 000 panels.

### 8.5 Physical validation not yet performed

No physical prototype exists. No NATA-laboratory AS/NZS structural validation has been performed. The 28-simulation set establishes the engineering envelope and identifies what physical tests are mandatory (hydrostatic 72-hour test, stability test on inclined ground, UV-weathering 3 000-hour AS/NZS, drop-impact at weld-line locations, chemical immersion), but until those certificates are issued **no SES procurement is possible**. This is a feasibility programme, not a fielded product.

### 8.6 Path to physical validation

The recommended sequence is gated by dependency:

| # | Step | Duration | Cost | Gate |
|---|---|---|---|---|
| 1 | Close two CAD tolerance fixes (tab clearance 0.40 → 0.60 mm; dovetail groove +0.5 mm) | 1 week | nil | Done before tooling quote |
| 2 | File provisional patent on open-bottom + dovetail + front-face lateral lock combination | 2 weeks | ~A$4 K | Priority date established |
| 3 | Full parametric CAD (Fusion 360 / Solidworks); Moldflow run for fill, weld lines, warpage prediction; FEA with weld-line strength factors | 4 – 6 weeks | A$8 – 15 K | Mouldflow-passed CAD |
| 4 | SLS or FDM prototype for fit-and-function (dovetail engagement force, tab push-fit, stacking ease, gasket groove fit) | 2 – 3 weeks | A$2 – 4 K | Tolerance fixes confirmed |
| 5 | SES engagement using existing Ausdrain relationships; present this simulation set as proof of engineering rigour | Parallel | nil | Letter of Intent (target) |
| 6 | Commission advanced tooling package; T1 samples; fixture cooling jig | 5 – 7 months | A$382.5 K | T3 production-quality samples |
| 7 | NATA testing: hydrostatic 72 h, inclined-ground stability, UV 3 000 h AS/NZS, drop-impact at weld-line locations, chemical immersion | 4 – 6 months | ~A$50 – 80 K | Third-party certification |
| 8 | First commercial deployment — SES pilot or council pre-emptive stock | 3 – 4 months | — | First 500 units sold |

Total time to first sale: ~18 – 24 months from CAD commitment. Total pre-revenue capital: ~A$460 K.

---

## 9. Conclusions

The AusDike™ feasibility programme closes on a positive overall recommendation:

1. **Market gap confirmed.** No Australian manufacturer produces an injection-moulded plastic modular flood barrier. The domestic market is uncontested.
2. **Engineering feasible.** Open-bottom self-ballasting reduces net flood force by 73 % and produces a self-stable 2-high stack at 4.9× tipping SF and 2.1× sliding SF with no bracing or anchors.
3. **Wall is column-buckling-governed.** 9 mm wall, talc-filled rPP, buckling SF 15.7×. The single most important methodological finding of the engineering programme.
4. **Joint integrity confirmed.** Dovetail stacking joint peel SF 1 243 000×; tab-root SF 858×; weld-line SF 63× at 62 % strength reduction.
5. **Manufacturable on existing capability.** 2-part mould, no side actions, recycled-PP feedstock identical to Geohex and Biax. New tool only — no new equipment, no new process knowledge.
6. **Strong tailwinds.** A$200 M / yr federal Disaster Ready Fund, 537+ flood-prone councils, WHS weight regulations, Australian-made procurement scoring.
7. **Competitive pricing.** A$65.51 COGS, A$109 / m sell, 42 % cheaper than imported Boxwall, 40 % gross margin.
8. **Brand-family fit.** The fourth-generation Holloway product follows the same Ausdrain / Geohex / Biax pattern into the largest of those four water-management domains.
9. **One adverse finding (wind on empty panels)** addressed by deployment protocol rather than geometry change.
10. **SKU family of four** (Standard / Cold / Mine / 90° Corner) covers the full operational envelope.

The recommendation is to proceed to physical prototype and NATA certification, gated on Letter-of-Intent confirmation before committing the A$382 500 tooling capex.

---

## 10. References

The two foundational source documents this paper integrates:

1. **AusDike™ Volume 1 — New Product Feasibility Report.** Holloway Group Pty Ltd, April 2026. *Commercial in Confidence.* Concept design, market research, competitive landscape, hydrostatic-stability simulation, dimensional iteration v1 → v6, 2-part-mould DFM checklist, indicative pricing, go-to-market phasing, eight key findings.
2. **AusDike™ Volume 2 — Engineering Simulation Report.** Holloway Group Pty Ltd, 2026. *Commercial in Confidence.* 28-simulation programme spanning wall-thickness sensitivity, 10-domain multi-physics, four FEA analyses (MITC4 plate + Q4 plane stress + eigenvalue beam), seven advanced verification simulations (50 m system, uneven ground, wind, corner, two tolerance stack-ups, weld line), Cross-WLF rheology and 1-D thermal cooling, advanced-tooling specification (Stavax ESR + Orvar Supreme + Elmax PM + Vanadis 4E + DMLS conformal cooling + Mold-Masters hot runner + Kistler monitoring), first-principles COGS, four-SKU family.

Supporting market and economic context (no proprietary data reproduced here):

- Australian Bureau of Meteorology, *State of the Climate 2024.* Flood-frequency attribution and projection.
- Insurance Council of Australia, *2022 Catastrophe Report — South-East Queensland and Northern NSW Floods.* Insured-loss figure A$6.8 B.
- Australian Government, National Recovery and Resilience Agency. *Disaster Ready Fund — Programme Guidelines.* A$200 M / year, 2023 –.
- Mordor Intelligence / IBISWorld, *Australia Engineering Plastics Market 2024 – 2035.* 4.2 % CAGR.
- AS/NZS 4858 / AS/NZS 4020 / AS/NZS 1170.2 — relevant Australian/NZ standards for water-contact materials, structural wind loading, and flood-resilience certification (target standards for the NATA test programme; no test has yet been performed against them).
- Boxwall Ltd, *Boxwall Modular Flood Barrier — Product Specification.* New Zealand. Comparator system.
- Geodesign Barriers GmbH, *Mobile Flood Protection Systems.* Germany. Comparator system.

Internal Holloway product lines providing channel and capability leverage:

- Ausdrain™ — modular drainage cells and underground tanks (1998 –).
- Geohex™ — recycled-PP hexagonal erosion-control cells (1 200 t/m² loaded).
- Biax Foundations™ — patented voided slab pods (< 3 kg, 100 % recycled post-industrial PE/PP).
- A Plus Plastics — general-manufacturing arm; custom injection-moulding across agriculture, engineering, medical, and automotive sectors.

Engineering-method references (no proprietary content reproduced):

- Bathe, K.J. *Finite Element Procedures.* MITC4 Mindlin plate-element formulation used in the wall-bending FEA.
- Roark's *Formulas for Stress and Strain* (8th ed.) — simply-supported plate-deflection benchmark used to cross-check the MITC4 result.
- Peterson, R.E. *Stress Concentration Factors* (3rd ed.) — Kt charts for the rib-wall fillet upgrade (5 mm → 8 mm) and the base-opening corner radius (3 mm → 8 mm).
- Tadmor, Z. and Gogos, C.G. *Principles of Polymer Processing.* Cross-WLF viscosity model and 1-D thermal-cooling solution used in the moulding process-window calculation.
- Uddeholm AB tool-steel data sheets — Stavax ESR, Orvar Supreme, Elmax PM, Vanadis 4 Extra PM grade properties used in the tooling-steel-justification table.
- Mold-Masters Ltd — Master-Series single-drop valve-gate hot-runner reference specification.

---

*End of integrated paper. AusDike™ Vol.1 + Vol.2 unified write-up. Concept feasibility plus 28-simulation engineering closure. Commercial in Confidence label retained for tonal coherence with the source documents; no real commercial relationship with Holloway Group Pty Ltd is implied by this repository.*
