# Hybrid Military Track Pad System

> **MIL-SPEC rubber track-pad procurement package for a notional 10 000-tank fleet:** HNBR 40 / NBR 30 / NR 25 / Neoprene 5 phr blend at Shore A 72 ± 4, scoring **6 679 / 10 000** across six terrain types. Headline claims: **15–20 dB acoustic reduction** vs bare steel (simulator §19: **20.8 dB** at 300 Hz), **80 % road-damage reduction**, **40 % better ice traction**. 25-year lifecycle **$282 235 per tank**.

> **Genre note.** TRP designator adopted for tonal coherence. Simulation-based, pre-FAT — no First Article Test on vulcanised pads completed.

---

## What this folder is

Rubber Tank Tracks is a **complete procurement subfolder**: executive summary, MIL-STD TDP, research paper, tread/lifecycle analyses (with PNG outputs), and Tier-2 acoustic modelling in [`../weapons_simulation.py`](../weapons_simulation.py) §19.

**Reading order:**

1. **This README** — navigation and headline numbers.
2. [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) — procurement-package overview.
3. [`MIL_SPEC_TRACK_PAD_TDP.md`](MIL_SPEC_TRACK_PAD_TDP.md) — technical data package.
4. [`Paper14_Military_Track_Pad.md`](Paper14_Military_Track_Pad.md) — academic research paper (TRP-2026-014).
5. [`SIM_README.md`](SIM_README.md) — §19 track-pad acoustic block.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) | Executive summary | Deliverables overview, key findings, readiness checklist. |
| [`MIL_SPEC_TRACK_PAD_TDP.md`](MIL_SPEC_TRACK_PAD_TDP.md) | TDP | MIL-STD-compliant pad specifications, QA, test matrix. |
| [`Paper14_Military_Track_Pad.md`](Paper14_Military_Track_Pad.md) | Research paper | Formulation science, tread scoring, lifecycle economics. |
| [`tread_analysis.png`](tread_analysis.png) | Analysis output | Tread-pattern computational scoring chart. |
| [`lifecycle_cost_analysis.png`](lifecycle_cost_analysis.png) | Analysis output | 25-year TCO visualisation. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Portfolio §19 coverage. |

---

## 🎯 Headline numbers

| Metric | Value |
|---|---|
| Tread performance score | 6 679 / 10 000 (Hybrid Military — top of five candidates) |
| Acoustic reduction vs steel | 15–20 dB (claim); **20.8 dB @ 300 Hz** (simulator §19) |
| Road infrastructure damage | 80 % reduction (engineering estimate) |
| Ice traction vs bare metal | 40 % improvement |
| 25-year lifecycle cost | $282 235 / tank ($5.64 / km duty cycle) |

Source (acoustic): [`../weapons_sim_results.md`](../weapons_sim_results.md) §19.

---

## 🚧 Honest framing

- **No FAT completed** — procurement readiness checklist marks field trials pending.
- **Diplomatic-value claims are estimates** — road-damage reduction not measured on NATO host-nation samples.
- **Battlefield debris / fragment strike** not in ASTM test matrix.

---

## 🔗 Related work in this repo

- [`../140mm Tank KE Round/`](../140mm%20Tank%20KE%20Round/) — tracked-vehicle munitions adjacency
- [`../README.md`](../README.md) — portfolio index

---

[← Back to Weapons-Defence README](../README.md)
