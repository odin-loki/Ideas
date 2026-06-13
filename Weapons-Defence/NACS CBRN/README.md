# NACS-TOTAL — Complete Sealed Warfare System

> **A 72-hour extended-operations CBRN protection and camouflage platform: universal multi-biome camo (56–63 % concealment), full-spectrum IR reduction (65–92 %), breathable CBRN undersuit (4+ hours), PCM temperature regulation, antimicrobial protection (7+ days), plus sealed oversuit, powered air-purifying respirator, and pharmaceutical sustainment for contaminated-environment operations.**

> **Genre note.** TRP designator, FOUO banner, and "Special Operations Procurement" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **CBRN, camouflage, and 72-hour sustainment numbers are prose engineering targets — not portfolio-simulator outputs.** Adjacent ballistic protection worn under/over NACS is validated via APES panels in portfolio §13.

---

## What this folder is

**NACS-TOTAL** extends the NACS base camouflage and undersuit system with four additional components to create a completely sealed, self-contained soldier system for 72+ hour continuous operations in contaminated environments. This folder contains the operator specification and academic research paper. [`platform_simulation.py`](platform_simulation.py) documents scope limits and prints adjacent APES §13 ballistic protection.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`NACS_Specification.md`](NACS_Specification.md) — full system architecture, component specs, 72-hour operational profile, cost analysis.
3. [`NACS_Research_Paper.md`](NACS_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — honest note on simulation coverage (CBRN prose-only; adjacent APES §13).
5. Run [`platform_simulation.py`](platform_simulation.py) — scope limits + adjacent APES military panel from §13.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`NACS_Specification.md`](NACS_Specification.md) | Operator / product specification | Full TRP-style engineering doc — system architecture, component specifications, 72-hour profile, pharmaceutical protocol, sealing integration, cost. **Start here for "what is the system."** |
| [`NACS_Research_Paper.md`](NACS_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, performance analysis, limitations — journal structure paired with the spec. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | CBRN prose-only scope; adjacent APES §13 cross-reference. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | Documents scope limits; prints adjacent APES military panel (§13). |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | §13 body-armour V50/BFD for adjacent APES panels. |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | Lifecycle simulator | §23 filter cartridge and suit fabric service intervals. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative tabulated numbers for ballistic adjacency and §23.1 lifecycle. |

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
| Filter cartridge life (§23) | **6 mo** |

### Adjacent ballistic protection (simulator §13 — APES military worn with NACS)

| Threat | Threat v | V50 | Outcome | BFD |
|---|---|---|---|---|
| 5.56 × 45 M855 | 940 m/s | 1,972 m/s | STOPPED | 11.6 mm |
| 7.62 × 51 M80 ball | 820 m/s | 1,407 m/s | STOPPED | 28.4 mm |
| .30-06 M2 AP | 878 m/s | 1,041 m/s | STOPPED | 44.0 mm |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §13 — APES military panel. Full matrix: [`../APES Body Armour/SIM_README.md`](../APES%20Body%20Armour/SIM_README.md).

---

## 🔬 Simulation verification

**NACS CBRN claims are prose-only** — permeation, camouflage percentages, PCM buffering, and pharmaceutical sustainment are **not** in [`../weapons_simulation.py`](../weapons_simulation.py). Filter and suit service intervals trace to portfolio **§23.1** via [`../weapon_lifecycle.py`](../weapon_lifecycle.py). The local script documents scope limits and prints the **adjacent APES military panel** from portfolio **§13** (ballistic protection worn with the undersuit):

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Scope limits + adjacent APES §13 verification slice |
| [`SIM_README.md`](SIM_README.md) | What is / is not modelled; APES cross-reference |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | §13 APES military / APES-L tables; §23.1 filter/suit lifecycle |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | §23 lifecycle — filter cartridge and suit fabric intervals |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

To regenerate the **full portfolio** (updates §13 tables):

```bash
cd ..
python weapons_simulation.py
```

Optional JSON summary:

```bash
python platform_simulation.py --json
```

---

## 🚀 Quick start (simulator)

**From this folder** — verify scope limits and adjacent APES §13:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for the full list of domains **not** modelled.

---

## 🚧 Honest framing

- **No dedicated NACS simulator.** CBRN permeation, camo effectiveness, and 72-hour sustainment numbers are engineering estimates in the spec prose — not outputs of `weapons_simulation.py`.
- **Not a fielded system.** Concept specification only; no instrumented CBRN chamber test data.
- **Pharmaceutical protocol is hypothetical.** Drug sustainment schedules in the spec are portfolio-internal design targets, not approved clinical protocols.

---

## 🔗 Related work in this repo

- [`../APES Body Armour/`](../APES%20Body%20Armour/) — ballistic protection worn over NACS undersuit
- [`../ADF Tactical Field Kit/`](../ADF%20Tactical%20Field%20Kit/) — field kit integrating NACS-compatible load carriage
- [`../README.md`](../README.md) — Weapons-Defence portfolio index

---

[← Back to Weapons-Defence README](../README.md)