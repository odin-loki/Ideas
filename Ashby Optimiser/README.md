# Ashby Optimiser — multi-scale homeostatic optimisation

> **W. Ross Ashby's 1948 homeostat reframed as a black-box optimiser.** Independent parallel search units at geometrically-spaced search radii, strict round-robin scheduling, homeostatic restarts on stagnation. Benchmarked against random search and (1+1)-ES on Sphere / Rastrigin / Rosenbrock / Ackley up to dimension 50.

---

## 🧠 What this folder is

A research paper plus a working Python optimiser and its test suite. The paper presents **MultiscaleAshbyOptimizer**, an audit-first rebuild of an earlier "Boolean-guided Ashby optimiser" that contained two significant errors (miscalibrated stability threshold and a broken update rule that confused history indices with positions).

The credited inspiration is **W. Ross Ashby**'s 1948 homeostat, the **Law of Requisite Variety**, and the theory of ultrastability. (Earlier README copy attributed the work to "C. Northcote Ashby" — that is incorrect; the source paper credits W. Ross Ashby.)

Attribution: **Odin · March 2026**.

---

## 📄 Files

| File | Role |
|------|------|
| [`Multiscale_Homeostatic_Optimization.md`](Multiscale_Homeostatic_Optimization.md) | Full research paper — method, benchmarks, audit of the prior implementation, limitations |
| [`multiscale_ashby.py`](multiscale_ashby.py) | Reference Python implementation (`HomeostasisUnit` + `MultiscaleAshbyOptimizer`) |
| [`test_multiscale_ashby.py`](test_multiscale_ashby.py) | Unit tests |

---

## 🏗 Algorithm

### `HomeostasisUnit`

Each unit independently maintains:

- A **position vector** in the search space.
- A short **history buffer** of (position, fitness) pairs.
- A **stagnation counter**.

On each evaluation, proposals are drawn uniformly from a hypercube of side $2g$ centred on the current position, where $g$ is the unit's **gear ratio**. The unit then moves to the best position in its recent history window. If relative improvement over the last five steps falls below tolerance for `stagnation_limit` consecutive steps, the unit performs a **homeostatic restart**: jump to a new random position within $3g$ of the origin and clear history.

**Critical isolation:** each unit only ever processes its own proposals. A proposal from unit $i$ is **never** passed to unit $j$. This prevents fine-scale units from being polluted by coarse-scale proposals.

### `MultiscaleAshbyOptimizer`

Spawn $N$ units with geometrically-spaced gear ratios:

$$g_i = g_\text{coarsest} / d^i,\quad i = 0,1,\dots,N-1.$$

With `coarsest_gear = 2.0` and `gear_decay = 10`, four units cover radii **2.0, 0.2, 0.02, 0.002** — four orders of magnitude.

Evaluations are allocated by **strict round-robin**: unit 0 fires on steps $0,N,2N,\dots$; unit 1 on steps $1,N+1,2N+1,\dots$; etc. Each unit therefore receives exactly $\lfloor\text{max\_evals}/N\rfloor$ evaluations — no unit can dominate the budget.

---

## 📐 Theoretical motivation (from §2 of the paper)

- **Ashby's homeostat (1948):** four interconnected feedback units, each with a threshold detector on its essential variables; on excursions the unit applies a random parameter step until stable behaviour is recovered.
- **Law of Requisite Variety:** a regulator must possess at least as much variety as the disturbances it must absorb. In optimisation terms: a landscape with structure at $K$ scales requires response variety at those same $K$ scales.
- **Relation to existing methods:** structurally related to multi-start local search, evolutionary island models, and IPOP-CMA-ES restart strategies; differs in (a) **fixing scales geometrically in advance** rather than adapting them, and (b) **sharing zero information** between units — maximising diversity at the cost of inter-unit correlation exploitation.

---

## 📊 Benchmark results (§4 of the paper)

Benchmarks vs **random search** and **(1+1)-ES with 1/5-success-rule step-size adaptation** on four standard test functions across dimensions 2–50. Headline:

| Function | Configuration | Median error |
|----------|---------------|---------------|
| Rastrigin (dim 10, 500 evals, **1 unit**) | Single-scale | **74.7** |
| Rastrigin (dim 10, 500 evals, **4 units**) | Multi-scale | **0.002** |
| Sphere / Rastrigin / Rosenbrock / Ackley (dim ≤ 50, 1000 evals) | Multi-scale | **near-zero** |

Multi-scale structure produces substantial gains specifically on **multi-modal** problems; on unimodal landscapes the single-scale (1+1)-ES is competitive.

---

## 🚧 Honest framing (paper §1.1, §5)

- **Audit-first paper.** §1.1 documents two real bugs in a prior "Boolean-guided" implementation: (i) the stability threshold τ = 0.01 was ~8× below the minimum essential variable for unit 0, making it unconditionally unstable regardless of position; (ii) the update rule used `argmin(history[-5:])`, returning a history-array index rather than the position that produced the best fitness — i.e. the optimiser had no memory of which positions were good. Apparent "Boolean stability laws" in the prior work were tautologies. The rebuild presented here corrects both.
- The optimiser is **not adaptive in scale** — gear ratios are fixed at start. CMA-ES-class adaptive approaches outperform on smooth unimodal landscapes.
- Inter-unit isolation deliberately sacrifices the ability to exploit correlations between scales.
- Benchmarks are on **standard synthetic test functions** (Sphere / Rastrigin / Rosenbrock / Ackley) up to dim 50; production use on larger or ill-conditioned problems requires further validation.

---

## 🔗 Related work in this repo

- [`Statistical Scheduler/`](../Statistical%20Scheduler/) — neural-heuristic distributed task scheduler (CFS / LinTS / PID); shares the homeostatic / control-theoretic framing
- [`Cell AI/`](../Cell%20AI/) — biologically-inspired sequence model with homeostatic-style metaplasticity layer
- [`VDJ Inspired Algorithm/`](../VDJ%20Inspired%20Algorithm/) — alternative bio-inspired optimisation
- [`Fungal Network Algorithm/`](../Fungal%20Network%20Algorithm/) — bio-inspired routing / growth optimisation
- [`Electromechnical Inspired Algorithms/`](../Electromechnical%20Inspired%20Algorithms/) — historical computing devices reframed algorithmically

---

[← Back to main README](../README.md)
