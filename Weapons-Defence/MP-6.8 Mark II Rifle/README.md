# MP-6.8 Mark II — advanced combat rifle

> **A simulation-validated 6.8 × 51 mm Common Cartridge infantry rifle with short-stroke gas piston, rotating bolt, and quick-detach suppressor.** Headline design: **731 m/s** muzzle velocity, **2,324 J** muzzle energy, **307 MPa** peak chamber pressure, **11.1 mm** RHA at the muzzle, **20-round** magazine, **4.10 kg** empty mass, **35 %** muzzle-brake efficiency, **358 N** peak shoulder force.

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **Numbers trace to the portfolio-wide [`../weapons_simulation.py`](../weapons_simulation.py) — cartridge key `6.8x51mm`, tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md).**

---

## What this folder is

The MP-6.8 Mark II is a **complete platform subfolder**: operator specification, academic research paper, and simulation traceability via the shared portfolio simulator. It represents the portfolio's primary infantry rifle calibre step above the 4.6 × 30 mm family.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`MP-6.8_Mark_II_Rifle_Specification.md`](MP-6.8_Mark_II_Rifle_Specification.md) — product and engineering spec (TRP-2026-003).
3. [`MP-6.8_Mark_II_Rifle_Research_Paper.md`](MP-6.8_Mark_II_Rifle_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — how to re-run and locate this platform's numbers in the portfolio simulator.
5. Run [`platform_simulation.py`](platform_simulation.py) — PASS/FAIL claim verification against the portfolio sim.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`MP-6.8_Mark_II_Rifle_Specification.md`](MP-6.8_Mark_II_Rifle_Specification.md) | Operator / product specification | Full TRP-style engineering doc — cartridge, gas system, barrel, suppressor, fire-control. **Start here for "what is the weapon."** |
| [`MP-6.8_Mark_II_Rifle_Research_Paper.md`](MP-6.8_Mark_II_Rifle_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, simulation framework, results, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Cartridge key, relevant tables, re-run command. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | Runs portfolio engine; prints PASS/FAIL checks for this platform's spec claims. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | Tier-1/Tier-2 physics engine. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative tabulated numbers. |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §§1–2, 3, 5, 10, 11, 23.

| Metric | Value |
|---|---|
| Cartridge | **6.8 × 51 mm Common Cartridge** (`6.8x51mm`) |
| Muzzle velocity | **731 m/s** (2,398 fps) |
| Muzzle energy | **2,324 J** |
| Peak chamber pressure | **307 MPa** (44,538 psi) |
| RHA penetration @ muzzle | **11.1 mm** (290 BHN, 0°) |
| RHA @ 300 m | **8.1 mm** |
| Empty mass | **4.10 kg** |
| Magazine capacity | **20 rounds** |
| Free recoil energy | **11.3 J** (8.3 ft·lb) |
| Peak shoulder force | **358 N** (80 lbf) — 35 % muzzle brake, 20 mm stock travel |
| Suppressor attenuation | **40.0 dB** (410 cm³, 7 baffles) |
| Barrel life (model) | **80,398 rounds** |
| Max effective range (Hatcher, KE > 80 J) | **> 3,500 m** (sim cap) |
| Bore life service (§23) | **25,000 rounds** |
| MRBF analytic (§23) | **~15,656 rounds** |
| MRBF simulated (§23) | **~15,000 rounds** |
| Felt recoil (§23) | **~1.631 ft·lb** |
| Spring fatigue SF (§23) | **4.5** |
| Barrel SF_yield (§23) | **1.99** |
| FTF rate (§23) | **1:55,000** |

---

## 🔬 Simulation verification

All headline numbers in this README trace to [`../weapons_sim_results.md`](../weapons_sim_results.md), produced by [`../weapons_simulation.py`](../weapons_simulation.py) and [`../weapon_lifecycle.py`](../weapon_lifecycle.py) (§23). Use the local verification script to confirm spec claims without regenerating the full portfolio:

```bash
python platform_simulation.py
```

The script prints **PASS/FAIL** checks for each claim in the specification and research paper.

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Local PASS/FAIL verification slice for this platform |
| [`SIM_README.md`](SIM_README.md) | Cartridge/weapon keys, table cross-references, methodology |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative tabulated output — cite in every spec edit |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | §23 lifecycle — structural SF, parts-life, reliability MC |

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

See [`SIM_README.md`](SIM_README.md) for cartridge key `6.8x51mm`, weapon key `MP-6.8 Mark II Rifle`, and result-table map.

---

## 🚧 Honest framing

- **Not a fielded weapon.** Concept and simulation only; no instrumented prototype data.
- **Portfolio simulator, not standalone.** No local Python package in this folder.
- **20-round magazine corrected from prior 50-round draft.** 50-round magazines are SAW spec, not rifle spec.
- **40 dB suppressor figure is a modelled upper bound.** Real prototypes typically achieve 25–35 dB.

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — Weapons-Defence portfolio index
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — Shared Stellite-21 barrel liner, S7 trigger pack
- [`../MP-4.6M Defender PDW/`](../MP-4.6M%20Defender%20PDW/) — Adjacent PDW in the 4.6 mm family
- [`../MAS-15.2E Anti-Materiel Sniper/`](../MAS-15.2E%20Anti-Materiel%20Sniper/) — Next calibre step — 15.2 mm anti-materiel

---

[← Back to Weapons-Defence README](../README.md)