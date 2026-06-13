# Project OBSIDIAN — concealable VIP body armour (hypothetical)

> **A hypothetical 11.8 kg torso-only secret-service protection study:** carbyne-UHMWPE hybrid coverall, carbon-fluoropolymer "Diamond Shell" plates, synthetic smart textile, and dress-shoe footwear. Design claims include theoretical small-arms resistance up to .50 caliber, 100+ multi-hit capability, and < 10 mm backface deformation — all **document-internal targets, not simulator-validated.**

> **Genre note.** Hypothetical / pre-physical-test. No prototype, no NIJ certification, no field trial. The portfolio simulator does **not** model OBSIDIAN ballistic performance.

---

## What this folder is

Project OBSIDIAN is the **torso-only / formal-attire predecessor** to [`../OBSIDIAN-X Body Armour/`](../OBSIDIAN-X%20Body%20Armour/). This subfolder pairs an operator specification with an academic research paper. Numbers are first-principles / aspirational unless stated otherwise.

**Reading order:**

1. **This README** — navigation and honest framing.
2. [`OBSIDIAN_Secret_Service_Suit_Specification.md`](OBSIDIAN_Secret_Service_Suit_Specification.md) — full operator spec (TRP-2026-109).
3. [`OBSIDIAN_Research_Paper.md`](OBSIDIAN_Research_Paper.md) — formal academic narrative.
4. [`SIM_README.md`](SIM_README.md) — confirms no runnable simulation.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`OBSIDIAN_Secret_Service_Suit_Specification.md`](OBSIDIAN_Secret_Service_Suit_Specification.md) | Operator specification | Layer stack, materials, concealment, cost analysis. **Start here.** |
| [`OBSIDIAN_Research_Paper.md`](OBSIDIAN_Research_Paper.md) | Academic research paper | Materials science, ballistic claims, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | No sim coverage statement. |

---

## 🎯 Headline numbers (design targets — unvalidated)

| Metric | Value |
|---|---|
| Total system weight | 11.8 kg (stated; exoskeleton/footwear accounting varies) |
| Soft foundation | 4.2 kg carbyne-UHMWPE hybrid |
| Hard plates ("Diamond Shell") | 3.6 kg |
| Theoretical unit cost | ~$40 M per suit |
| Simulator coverage | **None** |
| Lifecycle (§23) | *Hypothetical carbyne / STF suit — no runnable ballistic lifecycle model.* |

---

## 🔬 Simulation verification

**Scope-only — no runnable ballistic simulation.** Project OBSIDIAN carbyne/STF suit claims are document-internal design targets; portfolio `weapons_simulation.py` does not model this platform. The local script documents scope limits:

```bash
python platform_simulation.py
```

For **simulation-validated** body armour in this portfolio, see [`../APES Body Armour/`](../APES%20Body%20Armour/) (§13 V50/BFD).

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Scope documentation only |
| [`SIM_README.md`](SIM_README.md) | Confirms no sim coverage; APES cross-reference |

---

## 🚀 Quick start (simulator)

**From this folder** — print scope limits (no ballistic physics):

```bash
python platform_simulation.py
```

For simulation-validated armour numbers, see [`../APES Body Armour/`](../APES%20Body%20Armour/).

---

## 🚧 Honest framing

- **".50 caliber at 11.8 kg" is physically unsupportable** as a tested claim — read as design aspiration.
- **Bulk carbyne, macroscopic graphene laminates, and NiTi self-healing** are pre-commercial at spec volumes.
- **Successor system:** OBSIDIAN-X full-body combat armour at 18.5 kg.

---

## 🔗 Related work in this repo

- [`../OBSIDIAN-X Body Armour/`](../OBSIDIAN-X%20Body%20Armour/) — full-body combat evolution
- [`../APES Body Armour/`](../APES%20Body%20Armour/) — simulation-validated conventional armour (contrast)
- [`../README.md`](../README.md) — portfolio index

---

[← Back to Weapons-Defence README](../README.md)