# GlycoDur-P / NutriComplete-P — sustained injectable nutrition

> **Hypothetical recombinant protein + PLGA microsphere depots for sustained glucose delivery (GlycoDur-P, ~200 g glucose over 4–6 weeks) and complete macronutrient + micronutrient coverage (NutriComplete-P, 6-week release).** Critical simulator finding: as-proposed IV formulations compute **3 037–4 436 mOsm/kg** — failing both peripheral (< 600) and central (< 1 800) safe-infusion bounds. Remediation required before any human exposure.

> **Genre note.** TRP designator and FOUO banner adopted for tonal coherence. **PRE-CLINICAL / NOT FOR HUMAN USE.** No real programme office or clinical validation implied.

---

## What this folder is

The Injectable Nutrition platform is a **complete subfolder**: operator specification, academic research paper, and Tier-2 osmolality validation in [`../weapons_simulation.py`](../weapons_simulation.py) **§21**. The protein-engineering work is internally consistent; the IV-delivery assumption is what the simulator flags as unsafe.

**Reading order:**

1. **This README** — navigation and headline numbers.
2. [`Injectable_Nutrition_Specification.md`](Injectable_Nutrition_Specification.md) — full operator spec (TRP-2026-110); read §0 boxed warning first.
3. [`Injectable_Nutrition_Research_Paper.md`](Injectable_Nutrition_Research_Paper.md) — formal research narrative.
4. [`SIM_README.md`](SIM_README.md) — §21 osmolality model and safe-infusion bounds.
5. Run [`platform_simulation.py`](platform_simulation.py) — §21 osmolality + safe-infusion flags.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`Injectable_Nutrition_Specification.md`](Injectable_Nutrition_Specification.md) | Operator specification | GlycoDur-P + NutriComplete-P design, synthesis, regulatory pathway. **Start here.** |
| [`Injectable_Nutrition_Research_Paper.md`](Injectable_Nutrition_Research_Paper.md) | Academic research paper | Abstract, materials/methods, osmolality finding, remediation paths. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Portfolio §21 coverage. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | §21 osmolality + peripheral/central safe-infusion flags. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | Lifecycle simulator | §23 service-life and storage intervals. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | §21 Plumb / Holliday–Segar osmolality model. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative §21 osmolality table. |

---

## 🎯 Headline numbers (simulator §21)

| Formulation | Osmolality | Peripheral safe? | Central safe? |
|---|---|---|---|
| Baseline (1 200 kcal/L) | **3 037 mOsm/kg** | NO (5.1× bound) | NO (1.7× bound) |
| Field-ration (1 800 kcal/L) | **4 436 mOsm/kg** | NO (7.4× bound) | NO (2.5× bound) |
| 0.9 % saline (reference) | 308 mOsm/kg | YES | YES |
| Standard TPN (reference) | 2 280 mOsm/kg | NO | NO |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §21.







### Portfolio §23 — service intervals

| Metric | Value |
|---|---|
| Formulation shelf @ 25 °C (§23) | **18 mo** |

Source: [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

## 🔬 Simulation verification

All osmolality numbers trace to [`../weapons_sim_results.md`](../weapons_sim_results.md) **§21**, produced by [`../weapons_simulation.py`](../weapons_simulation.py). Use the local verification script to confirm safe-infusion flags:

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | §21 osmolality + safe-infusion PASS/FAIL |
| [`SIM_README.md`](SIM_README.md) | Plumb / Holliday–Segar bounds; methodology |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | §21 authoritative osmolality table |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

To regenerate the **full portfolio** (updates §21):

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

**From this folder** — verify §21 osmolality claims:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for §21 table cross-reference.

---

## 🚧 Honest framing

- **Hyperosmolar for IV use.** Ententeral/gastric redesign or 5–7× dilution required.
- **Pre-clinical only.** No animal PK, no Phase I.
- **Mirrored in [`../../Drugs/`](../../Drugs/)** for pharmacology portfolio cross-linking.
- **Oral pillar:** [`../TACT-1 Tactical Ration/`](../TACT-1%20Tactical%20Ration/) derives bar architecture from this injectable concept.

---

## 🔗 Related work in this repo

- [`../TACT-1 Tactical Ration/`](../TACT-1%20Tactical%20Ration/) — TACT-1 Mark II oral ration (derived from GlycoDur-P chemistry)
- [`../Combat Drug/`](../Combat%20Drug/) — pharmacology adjacency in the UCN stack
- [`../README.md`](../README.md) — portfolio index

---

[← Back to Weapons-Defence README](../README.md)