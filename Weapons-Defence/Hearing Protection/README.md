# Military-Grade Hearing Protection Systems

> **A two-system hearing-protection stack for ADF infantry and combat-support roles: APE-1 (Advanced Passive Earmuff) delivers 37.8 dB NRR through a six-layer composite shell; HANC-1 (Hybrid Active Noise Cancellation) layers MEMS + DSP + balanced-armature ANC on the passive platform for 42.6 dB NRR total with four operational modes and 40+ hour battery life. Threat environment quantified in portfolio simulator §6 (muzzle SPL across portfolio weapons).**

> **Genre note.** TRP designator, FOUO banner, and "Australian Department of Defence" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, ANSI S3.19 KEMAR measurement, or prototype test data is implied.

---

## What this folder is

This folder contains complete technical specifications for two advanced hearing protection systems — **APE-1** (passive) and **HANC-1** (hybrid active/passive) — designed for the 140–190 dB peak SPL gunfire / vehicle / artillery threat environment. Product NRR claims are spec-internal acoustic models; threat-side SPL stacks come from portfolio **§6**.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`Hearing_Protection_Specification.md`](Hearing_Protection_Specification.md) — full engineering spec for APE-1 and HANC-1.
3. [`Hearing_Protection_Research_Paper.md`](Hearing_Protection_Research_Paper.md) — formal design-and-validation narrative.
4. [`SIM_README.md`](SIM_README.md) — portfolio §6 muzzle SPL + layered protection stacks.
5. Run [`platform_simulation.py`](platform_simulation.py) — §6 per-weapon ear SPL stacks.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`Hearing_Protection_Specification.md`](Hearing_Protection_Specification.md) | Operator / product specification | APE-1 and HANC-1 full specs — acoustic architecture, electronics, modes, environmental protection, supply chain, cost. **Start here.** |
| [`Hearing_Protection_Research_Paper.md`](Hearing_Protection_Research_Paper.md) | Academic research paper | Abstract, threat environment, passive/hybrid design, performance claims, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Portfolio §6 muzzle blast and layered protection columns. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | §6 per-weapon ear SPL stacks (not product NRR). |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | §6 muzzle SPL + plug/muff/TACS stacks. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative §6 SPL table. |

---

## 🎯 Headline numbers

### Product targets (specification prose — not ANSI-measured)

| Metric | APE-1 | HANC-1 |
|---|---|---|
| Noise Reduction Rating | **37.8 dB** | **42.6 dB** |
| Weight per cup | 320 g | 368 g |
| Battery life | N/A | **40+ hours** |
| Operational modes | 1 | 4 |
| Unit cost (10k volume) | ~$280 | ~$665 |

### Portfolio simulator §6 (muzzle SPL + layered protection stacks)

Threat-side peak SPL at shooter ear — **not** APE-1 / HANC-1 product NRR. Generic plug (−22 dB), double plug+muff (−28 dB), and double + TACS personal ANC (−28 + 25 dB) stacks:

| Weapon | Ear (unsup) | Ear (sup) | Ear + double | Ear + double + TACS |
|---|---|---|---|---|
| MP-6.8 Mark II Rifle | 159.2 dB | 119.2 dB | 91.2 dB | 66.2 dB |
| MAS-15.2E Sniper | 158.0 dB | 118.0 dB | 90.0 dB | 65.0 dB |
| MP-4.6M Defender PDW | 157.0 dB | 117.0 dB | 89.0 dB | 64.0 dB |
| 57 mm Autocannon | 157.2 dB | 157.2 dB | 129.2 dB | 104.2 dB |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §6. TACS personal bound: §18.

---







### Portfolio §23 — service intervals

| Metric | Value |
|---|---|
| Foam plug life (§23) | **6 mo** |
| Electronic muff seal (§23) | **24 mo** |

Source: [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

## 🔬 Simulation verification

**APE-1 / HANC-1 product NRR (37.8 / 42.6 dB) is from spec acoustic models — not the portfolio simulator.** The local script prints portfolio **§6** threat-side muzzle SPL and layered protection stacks per weapon:

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | §6 ear SPL stacks (not product NRR) |
| [`SIM_README.md`](SIM_README.md) | §6 methodology; NRR vs SPL distinction |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | §6 authoritative SPL table |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

To regenerate the **full portfolio** (updates §6):

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

**From this folder** — verify §6 threat SPL stacks:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for §6 table cross-reference and §18 TACS adjacency.

---

## 🚧 Honest framing

- **Pre-physical-test / paper-stage.** 37.8 / 42.6 dB NRR are predicted from acoustic models, not ANSI S3.19 KEMAR measurement.
- **Simulator anchor is §6, not product NRR.** `weapons_simulation.py` models muzzle SPL and generic plug/muff/TACS stacks — not APE-1/HANC-1 cup geometry directly.
- **Bone-conduction ceiling ~50 dB.** Physiological limit regardless of cup design.

---

## 🔗 Related work in this repo

- [`../Military Noise Cancellation/`](../Military%20Noise%20Cancellation/) — TACS personal active-cancellation array (§18 in portfolio results)
- [`../README.md`](../README.md) — Weapons-Defence portfolio index

---

[← Back to Weapons-Defence README](../README.md)