# MP-4.6M Defender — personal defence weapon

> **A simulation-validated 4.6 × 30 mm Enhanced select-fire PDW sharing cartridge and bolt-face geometry with the MP-4.6M Guardian Pistol, with a longer barrel for higher muzzle velocity and a buffered bolt-carrier for sustained automatic fire.** Headline design: **542 m/s** muzzle velocity, **382 J** muzzle energy, **180 MPa** peak chamber pressure, **4.2 mm** RHA at the muzzle, **40-round** magazine, **2.10 kg** empty mass, **40 dB** modelled suppressor attenuation, **63 N** peak shoulder force.

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **Numbers trace to the portfolio-wide [`../weapons_simulation.py`](../weapons_simulation.py) — cartridge key `4.6x30mm_PDW`, tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md).**

---

## What this folder is

The MP-4.6M Defender is a **complete platform subfolder**: operator specification, academic research paper, and simulation traceability via the shared portfolio simulator. The Defender fires the **identical loaded round** as the Guardian Pistol; the simulator models the longer 266.7 mm barrel as a separate cartridge entry (`4.6x30mm_PDW`) yielding ~8 % higher muzzle velocity.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`MP-4.6M_Defender_PDW_Specification.md`](MP-4.6M_Defender_PDW_Specification.md) — product and engineering spec (TRP-2026-002).
3. [`MP-4.6M_Defender_PDW_Research_Paper.md`](MP-4.6M_Defender_PDW_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — how to re-run and locate this platform's numbers in the portfolio simulator.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`MP-4.6M_Defender_PDW_Specification.md`](MP-4.6M_Defender_PDW_Specification.md) | Operator / product specification | Full TRP-style engineering doc — cartridge commonality, action, barrel, suppressor, fire-control. **Start here for "what is the weapon."** |
| [`MP-4.6M_Defender_PDW_Research_Paper.md`](MP-4.6M_Defender_PDW_Research_Paper.md) | Academic research paper | Abstract, prior art, subsystem design, simulation framework, results, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Cartridge key, relevant `weapons_sim_results.md` tables, re-run command. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | Tier-1/Tier-2 physics engine. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative tabulated numbers. |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §§1–2, 3, 5, 10, 11.

| Metric | Value |
|---|---|
| Cartridge | **4.6 × 30 mm Enhanced** (`4.6x30mm_PDW` — same loaded round as Guardian) |
| Muzzle velocity | **542 m/s** (1,778 fps) |
| Muzzle energy | **382 J** |
| Peak chamber pressure | **180 MPa** (26,107 psi) |
| RHA penetration @ muzzle | **4.2 mm** (290 BHN, 0°) |
| Empty mass | **2.10 kg** |
| Magazine capacity | **40 rounds** |
| Free recoil energy | **0.8 J** (0.6 ft·lb) |
| Peak shoulder force | **63 N** (14 lbf) — buffered bolt-carrier + 18 mm stock travel |
| Suppressor attenuation | **40.0 dB** (180 cm³, 8 baffles) |
| Barrel life (model) | **302,501 rounds** |
| Max effective range (Hatcher, KE > 80 J) | **928 m** |

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
- **Same ammunition as the Guardian.** Logistical commonality is the design intent — only barrel length and fire-control differ.
- **40 dB suppressor figure is a modelled upper bound.** Real prototypes typically achieve 25–35 dB.

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — Weapons-Defence portfolio index
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — Shared 4.6 × 30 mm cartridge and action components
- [`../MP-4.6M Guardian Pistol/`](../MP-4.6M%20Guardian%20Pistol/) — Pistol variant, same cartridge, 180 mm barrel
- [`../MP-6.8 Mark II Rifle/`](../MP-6.8%20Mark%20II%20Rifle/) — Next calibre step in the small-arms family

---

[← Back to Weapons-Defence README](../README.md)
