# Biopolymère Caseless (BPC) — fully consumable small-arms cartridge

> **A protein-cartridge concept for 5.56 mm-class fully consumable ammunition:** 9–11 g round (vs ~12.3 g M855A1) with recombinant-spidroin casing and nitrated poly-amino-acid propellant, targeting **900–960 m/s** MV and **~1 700–1 800 J** ME at 60 000–70 000 psi chamber pressure. Cook-off resistance target **> 270 °C** (HITP-analogous). **1.33× firepower-per-kilogram** vs conventional 5.56 loadout.

> **Genre note.** TRP designator adopted for tonal coherence. Concept-stage design — no prototype, no live firing. Ballistic envelope maps to the 5.56 × 45 mm row in the portfolio simulator §1.

---

## What this folder is

The BPC System is a **complete platform subfolder**: operator specification (formerly the standalone `Caseless Bullets_README.md`) and academic research paper. No dedicated BPC simulator exists — conventional **5.56 × 45 mm** ballistics in portfolio **§1** anchor the performance envelope; protein-casing chemistry is **not** simulated.

**Reading order:**

1. **This README** — navigation and headline numbers.
2. [`Caseless_Bullets_Specification.md`](Caseless_Bullets_Specification.md) — full TRP-style engineering doc (TRP-2026-106).
3. [`Caseless_Bullets_Research_Paper.md`](Caseless_Bullets_Research_Paper.md) — formal biopolymère caseless research narrative.
4. [`SIM_README.md`](SIM_README.md) — §1 baseline reference; BPC chemistry scope limits.
5. Run [`platform_simulation.py`](platform_simulation.py) — §1 5.56 baseline + BPC target comparison.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`Caseless_Bullets_Specification.md`](Caseless_Bullets_Specification.md) | Operator specification | Cartridge, propellant, thermal management, weapon system, manufacturing. **Start here.** |
| [`Caseless_Bullets_Research_Paper.md`](Caseless_Bullets_Research_Paper.md) | Academic research paper | Theoretical framework, chemistry, cook-off analysis, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | §1 5.56 baseline; BPC chemistry not modelled. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | §1 baseline vs BPC design-target comparison. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | Lifecycle simulator | §23 service-life and storage intervals. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | §1 cartridge internal / external ballistics. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative §1 5.56 × 45 mm row. |

---

## 🎯 Headline numbers

### BPC design targets (spec prose — not simulated)

| Metric | Value |
|---|---|
| Round mass | 9–11 g (vs 12.3 g M855A1) |
| Projectile | 4.02 g (62 gr) |
| Muzzle velocity | 900–960 m/s |
| Muzzle energy | ~1 700–1 800 J |
| Cook-off ignition temp | > 270 °C (target) |
| Firepower-per-kg vs M855A1 | ~1.33× (400 vs 300 rounds same weight) |
| Protein case shelf (§23) | **24 mo** |

### Portfolio §1 — 5.56 × 45 mm NATO baseline (simulation-validated)

| Metric | Value |
|---|---|
| Cartridge | **5.56 × 45 mm** (`5.56x45mm`) |
| Muzzle velocity | **939 m/s** (3,081 fps) |
| Muzzle energy | **1 764 J** |
| Peak chamber pressure | **374 MPa** (54,295 psi) |
| RHA @ muzzle | **7.7 mm** (290 BHN, 0°) |
| Recoil impulse | **6.42 N·s** |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §1. BPC chemistry (spidroin casing, nitrated poly-amino-acid propellant, cook-off) is **not** in the portfolio simulator.

---

## 🔬 Simulation verification

**BPC protein-casing chemistry, cook-off, and chamber-sealing mechanics are not modelled.** The local script prints the conventional **5.56 × 45 mm §1 baseline** and compares it to BPC design targets:

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | §1 baseline + BPC target comparison |
| [`SIM_README.md`](SIM_README.md) | Scope limits; §1 cross-reference |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | §1 authoritative 5.56 × 45 mm row |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

To regenerate the **full portfolio** (updates §1):

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

**From this folder** — verify §1 baseline vs BPC targets:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for future BPC module requirements.

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