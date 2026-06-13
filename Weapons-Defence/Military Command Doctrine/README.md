# Adaptive Command Military Doctrine

> **A hypothetical hierarchical infantry command-and-training framework across five named tiers — Fire Team (5) → Squad (25) → Platoon (100) → Company (1,000) → Battalion (50,000) — coupled to a 36-week training pipeline under a 40/30/20/10 skills allocation. Emphasises distributed command authority, universal leadership capability, and rapid succession on casualty.**

> **Genre note.** TRP designator, FOUO banner, and "Australian Department of Defence" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real adopted doctrine, programme office, or force-structure economics is implied. **`weapons_simulation.py` does not model command-and-control.**

---

## What this folder is

The **Adaptive Command Military Doctrine** is a doctrinal concept piece: operator specification and academic research paper describing a hierarchical command structure and training pipeline. This is **non-physical doctrine** — no weapons physics, no force-on-force simulation. [`platform_simulation.py`](platform_simulation.py) documents scope limits only; it produces **no physics numbers**.

**Reading order for new readers:**

1. **This README** — navigation and structure overview.
2. [`Command_Doctrine_Specification.md`](Command_Doctrine_Specification.md) — full doctrine spec (tiers, training pipeline, allocation).
3. [`Command_Doctrine_Research_Paper.md`](Command_Doctrine_Research_Paper.md) — formal doctrinal narrative.
4. [`SIM_README.md`](SIM_README.md) — honest note: no simulation.
5. Run [`platform_simulation.py`](platform_simulation.py) — scope limits only (no physics outputs).

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`Command_Doctrine_Specification.md`](Command_Doctrine_Specification.md) | Operator / doctrine specification | Command tiers, training pipeline, skills allocation, succession doctrine. **Start here.** |
| [`Command_Doctrine_Research_Paper.md`](Command_Doctrine_Research_Paper.md) | Academic research paper | Abstract, force-structure rationale, training design, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | No simulation — doctrinal content only. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | Scope limits only — no physics numbers. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Documents doctrinal scope limits via `platform_simulation.py`. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | Does not model command-and-control (not invoked for doctrine). |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | No doctrine section — not applicable. |

---

## 🎯 Headline structure (specification prose)

| Tier | Personnel | Composition |
|---|---|---|
| Fire Team | 5 | Team Leader + 4 operators |
| Squad | 25 | 5 Fire Teams |
| Platoon | 100 | 4 Squads |
| Company | 1,000 | 10 Platoons |
| Battalion | 50,000 | 50 Companies |

### Training pipeline

| Phase | Duration |
|---|---|
| Basic infantry | 16 weeks |
| Advanced squad operations | 12 weeks |
| Specialised role training | 8 weeks |
| **Total initial pipeline** | **36 weeks** |

Skills allocation: **40 %** individual technical / **30 %** small-unit leadership / **20 %** specialised roles / **10 %** cross-training.

---







### Portfolio §23 — service intervals

| Metric | Value |
|---|---|
| Lifecycle (§23) | *Doctrinal force-structure and training-duration targets — no physics lifecycle model.* |

Source: [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

## 🔬 Simulation verification

**Scope-only — no physics numbers.** [`../weapons_simulation.py`](../weapons_simulation.py) does not model command tiers, training throughput, or force-on-force outcomes. The local script documents those limits and prints no quantitative physics results:

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Scope limits only — tier sizes and training durations are prose targets |
| [`SIM_README.md`](SIM_README.md) | What is / is not modelled |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | No doctrine section — not applicable |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

Optional JSON summary:

```bash
python platform_simulation.py --json
```

---

## 🚀 Quick start (simulator)

**From this folder** — print scope limits (no physics verification):

```bash
python platform_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for the full list of domains not modelled.

---

## 🚧 Honest framing

- **Doctrinal proposal, not simulated outcome.** No wargame, agent-based model, or analytic output underwrites effectiveness claims.
- **Unit sizes are notional.** The 50,000-personnel "Battalion" is ~50–100× a standard NATO battalion; tier naming does not match standard ADF/NATO usage.
- **Personnel economics not modelled.** Recruiting, retention, and sustainment costs for a 50,000-personnel tier are not quantified.
- **Land-force only.** Silent on joint air, maritime, cyber, and logistics enablers.

---

## 🔗 Related work in this repo

- [`../README.md`](../README.md) — Weapons-Defence portfolio index
- [`../ADF Tactical Field Kit/`](../ADF%20Tactical%20Field%20Kit/) — dismounted operator sustainment (complementary, not C2)

---

[← Back to Weapons-Defence README](../README.md)