# ASNP — Advanced Sports Nutrition Powder

> **Caffeine-free RTM combat-sports powder for acute high-exertion tactical windows:** HBCD slow-release carbohydrates, electrolyte matrix, citrulline / beta-alanine / adaptogen stack. Fourth oral pillar of the integrated UCN combat-nutrition platform alongside GlycoDur-P injectable, NutriComplete-P injectable, and TACT-1 Mark II bars.

> **Genre note.** Formulation specification — not a manufactured product. No clinical validation of integrated performance claims.

---

## What this folder is

ASNP (Advanced Sports Nutrition Powder) is a **subfolder of [`../`((../)** (TACT-1 Tactical Ration platform). It pairs an operator specification with an academic research paper. No dedicated ASNP simulator — formulation osmolality rationale is prose + shared HBCD chemistry with TACT-1 (portfolio §22 covers TACT-1 shelf life, not ASNP directly).

**Reading order:**

1. **This README** — navigation.
2. [`ASNP_Specification.md`((ASNP_Specification.md) — full formulation spec.
3. [`ASNP_Research_Paper.md`((ASNP_Research_Paper.md) — formal research narrative (TRP-2026-201).
4. [`SIM_README.md`((SIM_README.md) — simulation scope (prose / parent sim).

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`ASNP_Specification.md`((ASNP_Specification.md) | Operator specification | Per-serving formulation, manufacturing, usage protocol. |
| [`ASNP_Research_Paper.md`((ASNP_Research_Paper.md) | Academic research paper | Formulation science, performance mechanism literature. |
| [`SIM_README.md`((SIM_README.md) | Simulation documentation | No dedicated sim; parent-platform coverage. |

---

## 🎯 Headline formulation (per serving)

| Component | Amount |
|---|---|
| Highly Branched Cyclic Dextrin | 15 g |
| Dextrose + fructose | 5 g + 2.5 g |
| Sodium / potassium / magnesium / calcium | 600 / 300 / 150 / 150 mg |
| L-Citrulline | 6 g |
| Beta-alanine | 3.2 g |
| BCAAs (2:1:1) | 5 g |
| Caffeine | **0 mg** (by design) |

### §23 Lifecycle (product shelf)

| Metric | Value |
|---|---|

Source: [`../../weapon_lifecycle.py`((../../weapon_lifecycle.py) / [`../../weapons_sim_results.md`((../../weapons_sim_results.md) §23.1.

---

## 🔬 Simulation verification

**Scope-limited formulation numbers** — no dedicated ASNP simulator. Per-serving osmolality, electrolyte, and ergogenic-stack amounts are **spec- and literature-derived**, not computed by a standalone script. The local script anchors nearest portfolio coverage via parent TACT-1 ration shelf life:

```bash
python platform_simulation.py
```

Adjacent portfolio **§22** (TACT-1 Arrhenius Q10 = 2 shelf-life model) covers the parent platform's lipid-oxidation envelope — shared HBCD chemistry rationale, not ASNP-specific formulation validation.

| Artifact | Role |
|---|---|
| [`platform_simulation.py`((platform_simulation.py) | Scope documentation + §22 parent anchor |
| [`../../weapon_lifecycle.py`((../../weapon_lifecycle.py) | §23 product shelf-life model (**24 mo**) |
| [`SIM_README.md`((SIM_README.md) | Formulation scope limits, §22 + §23 cross-reference |
| [`../weapons_sim_results.md`((../weapons_sim_results.md) | §22 TACT-1 shelf-life table (adjacent coverage) |
| [`ASNP_Specification.md`((ASNP_Specification.md) | Authoritative per-serving formulation numbers |

---

## 🚀 Quick start (simulator)

**From this folder** — scope anchor + parent §22 shelf-life cross-reference:

```bash
python platform_simulation.py
```

Per-serving formulation numbers are authoritative in [`ASNP_Specification.md`((ASNP_Specification.md).

---

## 🚧 Honest framing

- **Pillar 4 of four-pillar UCN stack** — see parent [`../README.md`((../README.md) for integrated platform context.
- **Sensory acceptance unmeasured** — no sensory panel data cited.
- **Shared HBCD chemistry** with TACT-1 Mark II bars and GlycoDur-P injectable scaffold.

---

## 🔗 Related work

- [`../README.md`((../README.md) — TACT-1 Mark II parent platform
- [`../../Injectable Nutrition/`((../../Injectable%20Nutrition/) — injectable nutrition pillars 1–2
- [`../PODS- Edible High Energy Protein/`((../PODS-%20Edible%20High%20Energy%20Protein/) — synthetic lipid energy-density subfolder

---

[← Back to TACT-1 README((../README.md)