# Biopolymère Caseless (BPC) — fully consumable small-arms cartridge

> **A protein-cartridge concept for 5.56 mm-class fully consumable ammunition:** 9–11 g round (vs ~12.3 g M855A1) with recombinant-spidroin casing and nitrated poly-amino-acid propellant, targeting **900–960 m/s** MV and **~1 700–1 800 J** ME at 60 000–70 000 psi chamber pressure. Cook-off resistance target **> 270 °C** (HITP-analogous). **1.33× firepower-per-kilogram** vs conventional 5.56 loadout.

> **Genre note.** TRP designator adopted for tonal coherence. Concept-stage design — no prototype, no live firing. Ballistic envelope maps to the 5.56 × 45 mm row in the portfolio simulator §1.

---

## What this folder is

The BPC System is a **complete platform subfolder**: operator specification (formerly the standalone `Caseless Bullets_README.md`) and academic research paper. No dedicated BPC simulator exists — conventional 5.56 ballistics in [`../weapons_simulation.py`](../weapons_simulation.py) §1 anchor the performance envelope.

**Reading order:**

1. **This README** — navigation and headline numbers.
2. [`Caseless_Bullets_Specification.md`](Caseless_Bullets_Specification.md) — full TRP-style engineering doc (TRP-2026-106).
3. [`Caseless_Bullets_Research_Paper.md`](Caseless_Bullets_Research_Paper.md) — formal biopolymère caseless research narrative.
4. [`SIM_README.md`](SIM_README.md) — conceptual-only simulation scope.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`Caseless_Bullets_Specification.md`](Caseless_Bullets_Specification.md) | Operator specification | Cartridge, propellant, thermal management, weapon system, manufacturing. **Start here.** |
| [`Caseless_Bullets_Research_Paper.md`](Caseless_Bullets_Research_Paper.md) | Academic research paper | Theoretical framework, chemistry, cook-off analysis, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Why no dedicated sim; §1 baseline reference. |

---

## 🎯 Headline numbers (design targets)

| Metric | Value |
|---|---|
| Round mass | 9–11 g (vs 12.3 g M855A1) |
| Projectile | 4.02 g (62 gr) |
| Muzzle velocity | 900–960 m/s |
| Muzzle energy | ~1 700–1 800 J |
| Cook-off ignition temp | > 270 °C (target) |
| Firepower-per-kg vs M855A1 | ~1.33× (400 vs 300 rounds same weight) |
| Simulator anchor (5.56 × 45 §1) | 939 m/s / 1 764 J / 374 MPa |

---

## 🚧 Honest framing

- **No prototype.** Spidroin casing, nitrated poly-amino-acid propellant, and CNT ignition are unintegrated.
- **No SAAMI/NATO certification path** exists for protein caseless rounds.
- **Three open chemistry problems:** oxygen balance, casing dimensional tolerance, electrothermal primer at scale.

---

## 🔗 Related work in this repo

- [`../HPR-X Rocketry/`](../HPR-X%20Rocketry/) — adjacent propellant chemistry portfolio
- [`../MP-6.8 Mark II Rifle/`](../MP-6.8%20Mark%20II%20Rifle/) — conventional small-arms reference platform
- [`../README.md`](../README.md) — portfolio index

---

[← Back to Weapons-Defence README](../README.md)
