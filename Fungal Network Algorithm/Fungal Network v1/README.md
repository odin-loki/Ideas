# Fungal Network v1 — bio-inspired self-organising network (v1 papers + reference implementation)

> **The implementation generation behind the parent folder.** Three concept / mathematical papers and a working Python reference implementation of the Fungal Network Algorithm. The algorithm matches patterns by *physically reorganising* its own network topology — exploration → connection → optimisation → stabilisation — with no central control.

---

## 🍄 What this folder is

The v1 implementation slice of [`../`](../) (Fungal Network Algorithm).

| File | Role |
|---|---|
| [`Fungal NA Intro.md`](Fungal%20NA%20Intro.md) | **Bio-Inspired Network Algorithm: From Fungi to Computation** — design philosophy, novel techniques, network properties. Pattern recognition by physical reorganisation; geometric state evolution (exploration → connection → optimisation → stabilisation); resource-driven decision making. |
| [`Fungal NA Math Model.md`](Fungal%20NA%20Math%20Model.md) | Single-instance / single-network mathematical model |
| [`Fungal NA Parallel Math Model.md`](Fungal%20NA%20Parallel%20Math%20Model.md) | Parallel / distributed extension of the model |
| [`FungalNA.py`](FungalNA.py) | Python reference implementation |

---

## 🧠 Core principles (from `Fungal NA Intro.md`)

| Principle | Realisation |
|---|---|
| **Physical pattern recognition** | The network's *topology* (not its weights) is the long-term memory. New patterns are matched by structural fit, not by tuned coefficients. |
| **Network evolution states** | Exploration → Connection → Optimisation → Stabilisation. Each state emerges from simple local rules; no global scheduler. |
| **Resource-driven decisions** | Productive branches receive more "hyphae"; unproductive branches are pruned. Decision-making is local and bottom-up. |
| **No central control** | Every routing and allocation choice is made by individual nodes. Intelligence is emergent rather than programmed. |
| **Geometric progression of states** | State transitions follow geometric sequences, supporting natural multi-scale exploration. |

The single-instance model (`Fungal NA Math Model.md`) covers a single self-organising network; the parallel model (`Fungal NA Parallel Math Model.md`) extends to multiple cooperating networks — the natural deployment shape for distributed sensing, robot swarms, and multi-tenant cloud workloads.

---

## 🚧 Honest framing

- **One generation only.** v1 is the only implementation generation present; later generations were planned but not shipped.
- **Bio-inspired, not bio-simulating.** The algorithm formalises four principles drawn from fungal foraging — it does not pretend to model mycelium biology.
- **Theoretical / qualitative performance.** No standardised benchmark vs. classical graph algorithms (BFS / Dijkstra / ant-colony / etc.) is included.

---

## 🔗 Related work in this repo

- [`../`](../) — Fungal Network Algorithm parent folder (design-conversation log + this v1 directory)
- [`../../Cell AI/`](../../Cell%20AI/) — biologically-inspired non-attention sequence modelling (CellularPDE, Hebbian plasticity)
- [`../../VDJ Inspired Algorithm/`](../../VDJ%20Inspired%20Algorithm/) — immune-inspired combinatorial pattern recognition
- [`../../Statistical Scheduler/`](../../Statistical%20Scheduler/) — neural-heuristic distributed task scheduler (LinTS / PID / CFS)
- [`../../Asset Tracking Algorithm/`](../../Asset%20Tracking%20Algorithm/) — distributed multi-target tracking (ARIA-INTEL)
- [`../../Ashby Optimiser/`](../../Ashby%20Optimiser/) — multi-scale homeostatic optimisation

---

[← Up to Fungal Network Algorithm/](../README.md) · [← Back to main README](../../README.md)
