# Fungal Network Algorithm — bio-inspired self-organising network

> **Pattern recognition through physical network reorganisation, not neural-network style.** A bio-inspired algorithm modelled on how fungi search for food without central control: the network *itself* changes topology in response to inputs, and patterns are matched by the resulting structure rather than learned weights. Geometric state evolution (exploration → connection → optimisation → stabilisation), resource-driven decision making, fully decentralised.

---

## 🍄 What this folder is

A long design-conversation log, plus a `Fungal Network v1/` subfolder with three concept / math papers and a Python implementation.

| File | Role |
|---|---|
| [`Fungal NA Convo Log.txt`](Fungal%20NA%20Convo%20Log.txt) | Design-discussion transcript |
| [`Fungal Network v1/`](Fungal%20Network%20v1/) | v1 papers + implementation (see below) |

### `Fungal Network v1/` — papers and implementation

| File | Role |
|---|---|
| [`Fungal NA Intro.md`](Fungal%20Network%20v1/Fungal%20NA%20Intro.md) | "Bio-Inspired Network Algorithm: From Fungi to Computation" — design philosophy, novel techniques, applications. Pattern recognition by physical reorganisation; geometric state evolution; resource-driven decisions. |
| [`Fungal NA Math Model.md`](Fungal%20Network%20v1/Fungal%20NA%20Math%20Model.md) | Single-instance mathematical model |
| [`Fungal NA Parallel Math Model.md`](Fungal%20Network%20v1/Fungal%20NA%20Parallel%20Math%20Model.md) | Parallel / distributed extension of the math model |
| [`FungalNA.py`](Fungal%20Network%20v1/FungalNA.py) | Python reference implementation |

> Earlier README copy listed `Fungal NA Parallel Math Model.md` at the top level of this folder — it is actually inside `Fungal Network v1/` along with the other math files.

---

## 🌐 Design properties (per `Fungal NA Intro.md`)

- **Physical pattern recognition** — patterns are matched by topology change, not weights.
- **Network evolution states** — exploration → connection → optimisation → stabilisation, each state emerging from simple local rules.
- **Resource feedback** — the network sends more "hyphae" to productive areas, prunes unproductive ones.
- **No central control** — every routing / allocation decision is local; intelligence is emergent.

This makes the algorithm structurally different from standard graph / ant-colony / neural approaches: weights and edges are not the long-term memory — *the topology itself is the memory*.

---

## 🚧 Honest framing

- **One implementation generation** (v1). The structure suggests v2/v3 were planned but only v1 ships in this folder.
- Bio-inspired metaphors are kept honest: the algorithm doesn't claim to *simulate* fungi, only to formalise four principles drawn from fungal foraging into a computational framework.
- Performance characterisation in the v1 papers is theoretical / qualitative — not benchmarked against standard graph algorithms.

---

## 🔗 Related work in this repo

- [`../Cell AI/`](../Cell%20AI/) — biologically-inspired non-attention sequence modelling (CellularPDE, Hebbian plasticity)
- [`../VDJ Inspired Algorithm/`](../VDJ%20Inspired%20Algorithm/) — immune-inspired combinatorial pattern recognition
- [`../Statistical Scheduler/`](../Statistical%20Scheduler/) — neural-heuristic distributed task scheduler (LinTS / PID / CFS)
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — distributed multi-target tracking
- [`../Ashby Optimiser/`](../Ashby%20Optimiser/) — homeostatic multi-scale optimisation
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic structure for emergent computation

---

[← Back to main README](../README.md)
