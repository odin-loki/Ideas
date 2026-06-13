# ADF Tactical Field Kit

> **A next-generation individual field kit for ADF dismounted operators: titanium-alloy tool suite, 32 L MOLLE load-carriage system, inline water filtration, IFAK, navigation/signalling, and integrated nutrition via TACT-1 Mark II + ASNP. Targets < 7 kg kit weight excluding food and water, with TACT-1 delivering 5–14 kg savings over standard IRP for a 72-hour operation.**

> **Genre note.** TRP designator, FOUO banner, and "Advanced Defence Systems Research Division" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real ADF procurement programme or issued equipment is implied.

---

## What this folder is

The **ADF Tactical Field Kit** is an aggregate sustainment-platform specification covering load carriage, water, tools, medical, navigation, hygiene, lighting, and nutrition integration. This folder contains the operator specification only — **no paired research paper exists**.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`ADF_Tactical_Field_Kit_Specification.md`](ADF_Tactical_Field_Kit_Specification.md) — full procurement spec (18 sections).
3. [`SIM_README.md`](SIM_README.md) — aggregate spec; no dedicated sim; links to TACT-1/ASNP subfolders.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`ADF_Tactical_Field_Kit_Specification.md`](ADF_Tactical_Field_Kit_Specification.md) | Operator / procurement specification | Complete design, materials, manufacture, weight budget, cost analysis. **Start here.** |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | No dedicated simulator; nutrition sub-sim links. |

**No research paper.** Unlike other platform folders in this reorganisation, ADF Tactical Field Kit has no paired academic paper in `Research Papers/`. All technical content is in the specification above.

---

## 🎯 Headline numbers (specification prose)

| Metric | Value |
|---|---|
| Target field kit weight | **< 7 kg** (excluding food and water) |
| TACT-1 weight saving (72 hr) | **5–14 kg** vs standard IRP |
| Water carry requirement | **≤ 1.5 L** treated (inline filtration) |
| Main pack capacity | **32 L** MOLLE-compatible |
| Empty pack weight | **~2,155 g** |
| Operating temperature | **−20 °C to +65 °C** |

---

## 🧩 Nutrition subfolders (integrated components)

| Subfolder | Role |
|---|---|
| [`../TACT-1 Tactical Ration/`](../TACT-1%20Tactical%20Ration/) | TACT-1 Mark II full-day compact ration — 700 g/day, 4,210 kcal |
| [`../TACT-1 Tactical Ration/ASNP Sports Nutrition/ASNP_Specification.md`](../TACT-1%20Tactical%20Ration/ASNP%20Sports%20Nutrition/ASNP_Specification.md) | ASNP combat-sports energy drink powder |
| [`../TACT-1 Tactical Ration/PODS- Edible High Energy Protein/`](../TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/) | PODS high-density lipid nanoparticle (optional energy supplement) |

---

## 🚧 Honest framing

- **Aggregate specification only.** No standalone simulator; weight and cost numbers are prose engineering targets in the spec.
- **No research paper.** Portfolio reorganisation note: Paper numbering skips a dedicated ADF field-kit paper.
- **Nutrition numbers partially simulator-backed.** TACT-1 shelf-life uses `weapons_simulation.py` §22 (see TACT-1 README); the field kit itself does not.

---

## 🔗 Related work in this repo

- [`../TACT-1 Tactical Ration/README.md`](../TACT-1%20Tactical%20Ration/README.md) — oral nutrition pillar
- [`../APES Body Armour/`](../APES%20Body%20Armour/) — ballistic protection (separate load)
- [`../README.md`](../README.md) — Weapons-Defence portfolio index

---

[← Back to Weapons-Defence README](../README.md)
