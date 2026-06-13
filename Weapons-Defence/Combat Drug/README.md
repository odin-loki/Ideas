# HyperSynergy-X7™ — 7-day combat pharmacology depot

> **A hypothetical 7-day single-injection subcutaneous depot delivering a six-compound synthetic performance stack (MetaMax-2034, MetaFlow-47, MitoBoost-47, NeuroFlow-23, VasoMax-16, RecoveryX-88) plus natural-product and synergy tiers, targeted at sustained-operations military and elite-athletic use cases.** Headline design: 2.0 mL / 249.5 mg/mL PLGA microsphere depot, four release phases over 168 h, 300–500 % bioavailability improvement vs oral per spec claims. **PK anchor:** portfolio simulator §20 models FDA-approved reference stimulants only (caffeine, modafinil, dextroamphetamine) — not the six novel compounds.

> **Genre note.** TRP designator and FOUO banner adopted for tonal coherence with the rest of `Weapons-Defence/`. **PRE-CLINICAL / NOT FOR HUMAN USE.** No real programme office, no IND, no clinical validation implied.

---

## What this folder is

HyperSynergy-X7 (HSX7) is a **complete platform subfolder**: operator specification, academic research paper, and a Tier-2 PK reference block in the portfolio [`../weapons_simulation.py`](../weapons_simulation.py). The novel depot compounds have no published human PK; the simulator deliberately uses fielded stimulants as the only honest calibration anchor in **§20** — **HSX7 depot PK is not simulated**.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`Combat_Drug_Specification.md`](Combat_Drug_Specification.md) — full TRP-style operator spec (TRP-2026-107).
3. [`Combat_Drug_Research_Paper.md`](Combat_Drug_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — what §20 actually models (and what it does not).
5. Run [`platform_simulation.py`](platform_simulation.py) — §20 reference-stimulant PK only.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`Combat_Drug_Specification.md`](Combat_Drug_Specification.md) | Operator specification | Full engineering doc — depot architecture, compound tiers, release phases, regulatory pathway, manufacturing. **Start here for “what is the product.”** |
| [`Combat_Drug_Research_Paper.md`](Combat_Drug_Research_Paper.md) | Academic research paper | Abstract, prior art, formulation science, PK discussion, limitations — journal structure. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Portfolio §20 scope limits; HSX7 depot not modelled. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | §20 reference-stimulant oral PK only. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | Lifecycle simulator | §23 service-life and storage intervals. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | §20 one-compartment oral PK models. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative §20 PK table. |

---

## 🎯 Headline numbers

### Reference stimulant PK (simulator §20 — 80 kg subject, oral)

| Drug | Dose | t_max | C_max | t½ | AUC |
|---|---|---|---|---|---|
| Caffeine | 200 mg PO | 0.8 h | 4 069.5 ng/mL | 5.0 h | 32 652 ng·h/mL |
| Modafinil | 200 mg PO | 2.24 h | 2 113.1 ng/mL | 14.0 h | 47 496 ng·h/mL |
| Dextroamphetamine | 10 mg PO | 2.26 h | 21.4 ng/mL | 10.0 h | 359 ng·h/mL |
| HSX7 proxy — caffeine 100 mg | 100 mg | 0.8 h | 2 034.7 ng/mL | 5.0 h | 16 326 ng·h/mL |
| HSX7 proxy — modafinil 100 mg | 100 mg | 2.24 h | 1 056.5 ng/mL | 14.0 h | 23 748 ng·h/mL |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §20. **HSX7 six-novel-compound depot PK is not simulated.**

### Depot design targets (spec-only — not simulator outputs)

| Metric | Value |
|---|---|
| Injection volume | 2.0 mL SC |
| Active concentration | 249.5 mg/mL |
| Release duration | 168 h (7 days) |
| Release phases | 4 (onset → peak → sustain → taper) |
| Novel compounds | 6 (no published human PK) |

---






### Portfolio §23 — service intervals

| Metric | Value |
|---|---|
| Depot shelf cold-chain (§23) | **36 mo** |

Source: [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

## 🔬 Simulation verification

**HSX7 six-novel-compound depot PK is not simulated.** Portfolio **§20** models one-compartment **oral** PK for FDA-approved reference stimulants only (caffeine, modafinil, dextroamphetamine) at a standardised 80 kg subject:

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | §20 reference-stimulant PK + HSX7 scope limits |
| [`SIM_README.md`](SIM_README.md) | What §20 models; depot compounds excluded |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | §20 authoritative PK table |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

To regenerate the **full portfolio** (updates §20):

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

**From this folder** — verify §20 reference-stimulant PK:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for §20 table cross-reference.

---

## 🚧 Honest framing

- **Pre-clinical / paper-only.** No animal toxicology, no Phase I, no IND.
- **Simulator does not model the depot.** §20 is a reference-stimulant benchmark only.
- **Regulatory reality.** Combination novel-compound depot ≈ 8–12 years and hundreds of millions AUD.
- **Mirrored in [`../../Drugs/`](../../Drugs/)** for pharmacology portfolio cross-linking.

---

## 🔗 Related work in this repo

- [`../Injectable Nutrition/`](../Injectable%20Nutrition/) — GlycoDur-P / NutriComplete-P injectable nutrition (adjacent UCN stack)
- [`../TACT-1 Tactical Ration/`](../TACT-1%20Tactical%20Ration/) — oral nutrition pillar of the integrated combat-nutrition platform
- [`../README.md`](../README.md) — Weapons-Defence portfolio index

---

[← Back to Weapons-Defence README](../README.md)