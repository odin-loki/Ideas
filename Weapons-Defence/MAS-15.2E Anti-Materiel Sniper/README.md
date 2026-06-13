# MAS-15.2E — anti-materiel sniper system

> **A simulation-validated 15.2 × 115 mm APYT bolt-action anti-materiel rifle firing a 64 g saboted sub-calibre tungsten-carbide penetrator.** Headline design: **781 m/s** muzzle velocity, **19,505 J** muzzle energy, **258 MPa** peak chamber pressure, **42.0 mm** RHA at the muzzle (sim), **8-round** magazine, **13.20 kg** empty mass, **65 %** muzzle-brake efficiency, **1,042 N** peak mitigated shoulder force.

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **Numbers trace to the portfolio-wide [`../weapons_simulation.py`](../weapons_simulation.py) — cartridge key `15.2x115mm`, tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md).**

---

## What this folder is

The MAS-15.2E "Advanced Penetrator" Mark III is a **complete platform subfolder**: operator specification, academic research paper, and simulation traceability via the shared portfolio simulator. It is the portfolio's hard-target-interdiction / anti-materiel sniper platform — bolt-action (not semi-auto) because primary extraction is marginal at 258 MPa peak chamber pressure.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`MAS-15.2E_Specification.md`](MAS-15.2E_Specification.md) — product and engineering spec (TRP-2026-102).
3. [`MAS-15.2E_Research_Paper.md`](MAS-15.2E_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — how to re-run and locate this platform's numbers in the portfolio simulator.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`MAS-15.2E_Specification.md`](MAS-15.2E_Specification.md) | Operator / product specification | Full TRP-style engineering doc — cartridge, bolt action, muzzle brake, hydraulic stock, suppressor. **Start here for "what is the weapon."** |
| [`MAS-15.2E_Research_Paper.md`](MAS-15.2E_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, simulation framework, results, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Cartridge key, relevant tables, re-run command. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | Tier-1/Tier-2 physics engine. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative tabulated numbers. |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §§1–2, 3, 5, 10, 11.

| Metric | Value |
|---|---|
| Cartridge | **15.2 × 115 mm APYT** (`15.2x115mm`) |
| Muzzle velocity | **781 m/s** (2,561 fps) |
| Muzzle energy | **19,505 J** |
| Peak chamber pressure | **258 MPa** (37,361 psi) |
| RHA penetration @ muzzle | **42.0 mm** (290 BHN, 0° — sim §3) |
| RHA @ 1,000 m | **22.3 mm** |
| Empty mass | **13.20 kg** |
| Magazine capacity | **8 rounds**, bolt-action |
| Free recoil energy | **255.2 J** (188.2 ft·lb) |
| Peak shoulder force (mitigated) | **1,042 N** (234 lbf) — 65 % brake, 45 mm stock travel |
| Suppressor attenuation | **40.0 dB** (1,800 cm³, 10 baffles) |
| Barrel life (model) | **22,753 rounds** |
| Max effective range (Hatcher, KE > 80 J) | **> 3,500 m** (sim cap) |

---

## 🚀 Quick start (simulator)

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for table cross-reference.

---

## 🚧 Honest framing

- **Not a fielded weapon.** Concept and simulation only; no instrumented prototype data.
- **Portfolio simulator, not standalone.** No local Python package in this folder.
- **Anti-materiel, not anti-MBT.** Penetration figures are against 290 BHN plate at 0° — the system does not engage modern MBT frontal arc.
- **Shoulder firing requires full recoil stack.** Both the ≥ 65 % muzzle brake and the 45 mm hydraulic stock must be engaged; unmitigated free recoil is 255 J (~14× a 7.62 × 51 mm sniper rifle).
- **Bolt-action is permanent.** Semi-automatic gas action was rejected at 258 MPa peak chamber pressure.

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — Weapons-Defence portfolio index
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — 14.5 × 114 mm tooling commonality intent
- [`../MP-6.8 Mark II Rifle/`](../MP-6.8%20Mark%20II%20Rifle/) — Adjacent infantry rifle in the small-arms family
- [`../Hearing Protection/Hearing_Protection_Specification.md`](../Hearing%20Protection/Hearing_Protection_Specification.md) — Layered hearing protection stack (sim §6)

---

[← Back to Weapons-Defence README](../README.md)
