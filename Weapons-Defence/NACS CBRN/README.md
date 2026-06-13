# NACS-TOTAL — Complete Sealed Warfare System

> **A 72-hour extended-operations CBRN protection and camouflage platform: universal multi-biome camo (56–63 % concealment), full-spectrum IR reduction (65–92 %), breathable CBRN undersuit (4+ hours), PCM temperature regulation, antimicrobial protection (7+ days), plus sealed oversuit, powered air-purifying respirator, and pharmaceutical sustainment for contaminated-environment operations.**

> **Genre note.** TRP designator, FOUO banner, and "Special Operations Procurement" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **Performance numbers in the specification are prose engineering targets — not portfolio-simulator outputs.**

---

## What this folder is

**NACS-TOTAL** extends the NACS base camouflage and undersuit system with four additional components to create a completely sealed, self-contained soldier system for 72+ hour continuous operations in contaminated environments. This folder contains the operator specification and academic research paper only.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`NACS_Specification.md`](NACS_Specification.md) — full system architecture, component specs, 72-hour operational profile, cost analysis.
3. [`NACS_Research_Paper.md`](NACS_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — honest note on simulation coverage (none dedicated).

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`NACS_Specification.md`](NACS_Specification.md) | Operator / product specification | Full TRP-style engineering doc — system architecture, component specifications, 72-hour profile, pharmaceutical protocol, sealing integration, cost. **Start here for "what is the system."** |
| [`NACS_Research_Paper.md`](NACS_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, performance analysis, limitations — journal structure paired with the spec. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | No dedicated simulator; explains where numbers come from. |

---

## 🎯 Headline numbers (specification prose)

These values are stated in the specification document, not derived from `weapons_simulation.py`.

| Metric | Value |
|---|---|
| Universal camouflage (all biomes) | **56–63 %** concealment |
| Full-spectrum IR reduction | **65–92 %** |
| Breathable CBRN protection | **4+ hours** continuous |
| PCM temperature regulation | Active thermal buffering |
| Antimicrobial protection | **7+ days** |
| Extended operations envelope | **72+ hours** sealed |

---

## 🚧 Honest framing

- **No dedicated simulator.** CBRN permeation, camo effectiveness, and 72-hour sustainment numbers are engineering estimates in the spec prose — not outputs of `weapons_simulation.py`.
- **Not a fielded system.** Concept specification only; no instrumented CBRN chamber test data.
- **Pharmaceutical protocol is hypothetical.** Drug sustainment schedules in the spec are portfolio-internal design targets, not approved clinical protocols.

---

## 🔗 Related work in this repo

- [`../APES Body Armour/`](../APES%20Body%20Armour/) — ballistic protection worn over NACS undersuit
- [`../ADF Tactical Field Kit/`](../ADF%20Tactical%20Field%20Kit/) — field kit integrating NACS-compatible load carriage
- [`../README.md`](../README.md) — Weapons-Defence portfolio index

---

[← Back to Weapons-Defence README](../README.md)
