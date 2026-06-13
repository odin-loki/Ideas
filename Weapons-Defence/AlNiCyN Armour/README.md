# AlNiCyN — Advanced Aluminium Armour Alloy Family

> **A three-tier aluminium-based armour alloy suite — AlNiCyN-5000 (baseline, TRL 7–8), AlNiCyN-7000 (high-performance), AlNiCyN-X (experimental metamaterial) — delivering rolled homogeneous armour (RHA) equivalent protection at ~60 % weight reduction. Material properties and ballistic performance claims are documented in the specification; terminal-ballistics interactions with portfolio cartridges are modelled in the parent simulator §3 (RHA penetration) and §13 (body-armour V50).**

> **Genre note.** TRP designator, FOUO banner, and "Advanced Materials Division" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or alloy test coupon data is implied.

---

## What this folder is

The **AlNiCyN Family** is a complete platform subfolder: operator specification and academic research paper for advanced aluminium armour alloys used in vehicle hulls, plate substrates, and structural armour applications. [`platform_simulation.py`](platform_simulation.py) anchors heavy-threat ballistic context via portfolio **§3** RHA penetration tables — alloy-tier properties remain spec prose.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`AlNiCyN_Specification.md`](AlNiCyN_Specification.md) — alloy compositions, mechanical properties, processing, selection guide, economics.
3. [`AlNiCyN_Research_Paper.md`](AlNiCyN_Research_Paper.md) — formal materials-science narrative.
4. [`SIM_README.md`](SIM_README.md) — material properties in spec; §3 penetration context via parent sim.
5. Run [`platform_simulation.py`](platform_simulation.py) — §3 RHA penetration sample + scope limits.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`AlNiCyN_Specification.md`](AlNiCyN_Specification.md) | Operator / product specification | Full technical reference — AlNiCyN-5000/7000/X compositions, comparative analysis, processing, testing standards, economics. **Start here for "what are the alloys."** |
| [`AlNiCyN_Research_Paper.md`](AlNiCyN_Research_Paper.md) | Academic research paper | Abstract, metallurgy background, alloy design, performance claims, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Alloy properties in spec; §3 RHA penetration context via portfolio sim. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | §3 penetration sample + scope limits for alloy-tier claims. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | §3 terminal ballistics vs standard RHA plate. |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | Lifecycle simulator | §23 plate and spall-liner service intervals. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative §3 penetration tables — cite for ballistic context. |

---

## 🎯 Headline numbers (specification prose)

| Alloy | TRL | Cost | Performance vs RHA | Weight reduction |
|---|---|---|---|---|
| **AlNiCyN-5000** | 7–8 | $10,030/t | 1.0× RHA equivalent | ~60 % |
| **AlNiCyN-7000** | 5–6 | Higher | Enhanced hardening | ~60 % |
| **AlNiCyN-X** | 2–3 | Research | Metamaterial lattice | Targeted |

### §23 Lifecycle (service intervals)

Values from [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.1 / [`../weapon_lifecycle.py`](../weapon_lifecycle.py).

| Component | Service life |
|---|---|

### Portfolio §3 — RHA penetration context (standard 290 BHN plate)

Small-arms and heavy-cartridge penetration depths modelled in the portfolio simulator — generic RHA baseline, not AlNiCyN coupon data:

| Cartridge | 0 m | 300 m | 500 m | 1 000 m | 2 000 m | 3 000 m |
|---|---|---|---|---|---|---|
| 6.8 × 51 mm | 11.1 mm | 8.1 mm | 6.5 mm | — | — | — |
| 7.62 × 51 mm | 9.7 mm | 6.7 mm | 5.1 mm | 2.7 mm | — | — |
| 57 × 347 mm | 139.7 mm | — | — | 113.0 mm | 0.0 mm | — |
| 140 mm KE | 867.1 mm | — | — | 540.9 mm | 326.7 mm | 215.7 mm |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §3. Obliquity tables: §12.

---







### Portfolio §23 — service intervals

| Metric | Value |
|---|---|
| Plate service life (§23) | **15 yr** |

Source: [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

## 🔬 Simulation verification

**AlNiCyN alloy-tier yield, hardness, and RHA-equivalence factors are spec prose only** — not individually modelled. The local script prints portfolio **§3** RHA penetration samples as heavy-threat ballistic context:

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | §3 penetration sample + alloy-tier scope limits |
| [`SIM_README.md`](SIM_README.md) | What is / is not modelled; §3 vs §13 distinction |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | §3 RHA penetration tables — cite for ballistic context |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | §23 lifecycle — plate and spall-liner service intervals |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

To regenerate the **full portfolio** (updates §3 tables):

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

**From this folder** — verify §3 penetration context and scope limits:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for §3 table cross-reference. Dismounted composite armour: [`../APES Body Armour/`](../APES%20Body%20Armour/) §13.

---

## 🚧 Honest framing

- **Material properties are specification prose.** Yield strength, hardness, and RHA-equivalence factors are design targets in the spec, not independently measured in this repo.
- **No dedicated AlNiCyN simulator.** Terminal ballistics use the portfolio's generic RHA and composite-armour models.
- **AlNiCyN-X is conceptual.** Metamaterial lattice variant sits at TRL 2–3.

---

## 🔗 Related work in this repo

- [`../APES Body Armour/`](../APES%20Body%20Armour/) — dismounted body armour using B4C ceramic (complementary protection tier)
- [`../140mm Tank KE Round/`](../140mm%20Tank%20KE%20Round/) — KE penetrator vs RHA interactions in portfolio sim §3
- [`../README.md`](../README.md) — Weapons-Defence portfolio index

---

[← Back to Weapons-Defence README](../README.md)