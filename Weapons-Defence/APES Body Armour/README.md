# APES — Advanced Protective Equipment System

> **A composite body-armour platform for dismounted operators: 16-layer Kevlar/UHMWPE soft stack, non-Newtonian impact padding, dragon-scale B4C ceramic tiles on 7075-T6 honeycomb, and titanium strike-point reinforcement. Military configuration (16-layer + 12 mm B4C tile, 35 kg/m²) stops 7.62 × 51 M80 ball and .30-06 M2 AP at threat velocity with NIJ 0101.06 BFD within the 44 mm pass limit — numbers trace to portfolio simulator §13.**

> **Genre note.** TRP designator, FOUO banner, and "Australian Department of Defence" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied.

---

## What this folder is

The **Advanced Protective Equipment System (APES)** is a complete platform subfolder: operator specification, academic research paper, and simulator-backed V50 / back-face deformation (BFD) validation via [`platform_simulation.py`](platform_simulation.py) and the shared portfolio engine in [`../weapons_simulation.py`](../weapons_simulation.py).

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`APES_Specification.md`](APES_Specification.md) — product and engineering spec (layer stack, plate geometry, thermal management, procurement).
3. [`APES_Research_Paper.md`](APES_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — how to re-run §13 body-armour V50/BFD in the portfolio simulator.
5. Run [`platform_simulation.py`](platform_simulation.py) — PASS/FAIL claim verification against portfolio §13.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`APES_Specification.md`](APES_Specification.md) | Operator / product specification | Full TRP-style engineering doc — base layer, impact management, plate system, integration, lifecycle, cost. **Start here for "what is the armour."** |
| [`APES_Research_Paper.md`](APES_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, simulation framework, results, limitations — same numbers as the spec in journal structure. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Portfolio §13 V50/BFD coverage for APES military and APES-L police panels. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | Runs portfolio engine; prints PASS/FAIL checks for this platform's spec claims. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | Lambert-Jonas / Recht-Ipson V50 + clay-witness BFD models. |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | Lifecycle simulator | §23 service-interval model for panel, tile, and soft stack. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative tabulated numbers — cite this file in every spec edit. |

---

## 🎯 Headline numbers (simulation-validated)

Values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §13 for the **APES military** panel (16-layer + 12 mm B4C tile, 35 kg/m²).

| Threat | Threat v | V50 | Outcome | BFD |
|---|---|---|---|---|
| 9 mm 124 gr ball | 390 m/s | 1,600 m/s | STOPPED | 1.5 mm |
| 5.56 × 45 M855 | 940 m/s | 1,972 m/s | STOPPED | 11.6 mm |
| 7.62 × 51 M80 ball | 820 m/s | 1,407 m/s | STOPPED | 28.4 mm |
| .30-06 M2 AP | 878 m/s | 1,041 m/s | STOPPED | 44.0 mm |
| 12.7 × 99 M2 AP | 890 m/s | 583 m/s | PERFORATED | — |

Full APES-L police panel matrix: [`../weapons_sim_results.md`](../weapons_sim_results.md) §13.

### §23 Lifecycle (service intervals)

Values from [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.1 / [`../weapon_lifecycle.py`](../weapon_lifecycle.py).

| Component | Service life |
|---|---|

---







### Portfolio §23 — service intervals

| Metric | Value |
|---|---|
| Panel service life (§23) | **12 yr** |
| Ceramic tile replacement (§23) | **5 yr** |
| Soft panel refresh (§23) | **8 yr** |

Source: [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

## 🔬 Simulation verification

All headline numbers in this README trace to [`../weapons_sim_results.md`](../weapons_sim_results.md) **§13** (ballistics) and **§23.1** (lifecycle), produced by [`../weapons_simulation.py`](../weapons_simulation.py) and [`../weapon_lifecycle.py`](../weapon_lifecycle.py). Use the local verification script to confirm spec claims without regenerating the full portfolio:

```bash
python platform_simulation.py
```

The script prints **PASS/FAIL** checks for APES military and APES-L police panels against the full §13 threat matrix.

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Local PASS/FAIL verification slice for APES military + APES-L |
| [`SIM_README.md`](SIM_README.md) | Panel definitions, threat set, BFD rule, methodology |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative tabulated output — cite in every spec edit |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | §23 lifecycle — panel, tile, and soft-stack service intervals |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

To regenerate the **full portfolio** after editing shared parameters:

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

**From this folder** — verify platform claims:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for panel keys and §13 table cross-reference.

---

## 🚧 Honest framing

- **Not a fielded system.** Concept and simulation only; no instrumented ballistic test data.
- **V50 model is calibrated, not measured.** Lambert-Jonas / Recht-Ipson composite-factor fit in `weapons_simulation.py`; NIJ 0101.06 lab certification is not claimed.
- **Police variant available.** APES-L (10-layer + 8 mm B4C, 22 kg/m²) is also modelled in §13 — see SIM_README for full threat matrix.

---

## 🔗 Related work in this repo

- [`../AlNiCyN Armour/`](../AlNiCyN%20Armour/) — aluminium armour alloy family for vehicle and plate substrates
- [`../NACS CBRN/`](../NACS%20CBRN/) — sealed CBRN undersuit worn under APES
- [`../README.md`](../README.md) — Weapons-Defence portfolio index

---

[← Back to Weapons-Defence README](../README.md)