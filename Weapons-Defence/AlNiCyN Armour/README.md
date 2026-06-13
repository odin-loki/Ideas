# AlNiCyN — Advanced Aluminium Armour Alloy Family

> **A three-tier aluminium-based armour alloy suite — AlNiCyN-5000 (baseline, TRL 7–8), AlNiCyN-7000 (high-performance), AlNiCyN-X (experimental metamaterial) — delivering rolled homogeneous armour (RHA) equivalent protection at ~60 % weight reduction. Material properties and ballistic performance claims are documented in the specification; terminal-ballistics interactions with portfolio cartridges are modelled in the parent simulator §3 (RHA penetration) and §13 (body-armour V50).**

> **Genre note.** TRP designator, FOUO banner, and "Advanced Materials Division" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or alloy test coupon data is implied.

---

## What this folder is

The **AlNiCyN Family** is a complete platform subfolder: operator specification and academic research paper for advanced aluminium armour alloys used in vehicle hulls, plate substrates, and structural armour applications.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`AlNiCyN_Specification.md`](AlNiCyN_Specification.md) — alloy compositions, mechanical properties, processing, selection guide, economics.
3. [`AlNiCyN_Research_Paper.md`](AlNiCyN_Research_Paper.md) — formal materials-science narrative.
4. [`SIM_README.md`](SIM_README.md) — material properties in spec; armour interactions via parent sim §13.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`AlNiCyN_Specification.md`](AlNiCyN_Specification.md) | Operator / product specification | Full technical reference — AlNiCyN-5000/7000/X compositions, comparative analysis, processing, testing standards, economics. **Start here for "what are the alloys."** |
| [`AlNiCyN_Research_Paper.md`](AlNiCyN_Research_Paper.md) | Academic research paper | Abstract, metallurgy background, alloy design, performance claims, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Where material numbers live vs. where portfolio simulator covers armour. |

---

## 🎯 Headline numbers (specification prose)

| Alloy | TRL | Cost | Performance vs RHA | Weight reduction |
|---|---|---|---|---|
| **AlNiCyN-5000** | 7–8 | $10,030/t | 1.0× RHA equivalent | ~60 % |
| **AlNiCyN-7000** | 5–6 | Higher | Enhanced hardening | ~60 % |
| **AlNiCyN-X** | 2–3 | Research | Metamaterial lattice | Targeted |

Ballistic interaction with portfolio threats uses generic RHA penetration models in `weapons_simulation.py` §3 — not alloy-specific coupon data.

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
