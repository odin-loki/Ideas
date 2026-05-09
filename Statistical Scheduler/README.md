# Statistical Scheduler

> **A neural-heuristic distributed task scheduler that fuses CFS-style fair-share scoring, Linear Thompson Sampling exploration in 24-dimensional context space, PID-controlled stability override, and a full statistical monitoring stack (Holt–Winters forecasting, Page–Hinkley CUSUM change detection, EWMA alerting) — with reported sub-millisecond placement latency, formal `O(d√T·polylog T)` regret on the LinTS layer, and a BIBO bound on the PID layer.** Most schedulers do one of these things well. This one tries to do all of them in a single pipeline that is auditable end-to-end.

---

## What this folder is

Distributed task scheduling is usually one of three things: a fairness algorithm (Linux CFS, Hadoop fair-share), a learned bandit (LinUCB / LinTS in cloud auto-scaling research), or a control loop (PID over CPU utilisation). They are rarely combined because each has its own failure mode and combining them naively means inheriting all three failure modes simultaneously. This folder argues — with proofs, code, and a measurement harness — that you can stack them carefully if you (a) gate the bandit's outputs through a confidence threshold so it never overrides fairness when it isn't sure, (b) run the PID layer as a *safety override* rather than a primary placement decision, and (c) instrument the monitoring layer so you actually see the wheels coming off before they do.

The result, as documented, is a scheduler that places tasks at **p50 = 0.48 ms, p95 = 0.83 ms, p99 = 1.00 ms** on 500-task / 16-node workloads, and degrades gracefully into 4–128-node configurations with Jain fairness `1.00`.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`paper.md`](paper.md) | Full research paper. Defines the eight-step pipeline, scoring formulas, regret/BIBO proofs, monitoring statistics, and §9 limitations. |
| [`scheduler_core.py`](scheduler_core.py) | Reference Python implementation of the eight-step pipeline. |
| [`monitoring_system.py`](monitoring_system.py) | Holt–Winters / CUSUM / EWMA monitoring stack. |
| [`Cypha.py`](Cypha.py) | A large `CyphaDIF` (differential information field) classifier — a separate research artefact that lives in this folder but is **not** the LinTS scheduler described in `paper.md`. Treat as adjacent work. |

---

## 🧠 The eight-step pipeline (paper §3.1)

1. **Dependency gate.** Reject if `dep_count > 0` (task has unmet dependencies).
2. **Hard filters.** Reject if any node-level constraint fails.
3. **Pre-placement snapshot.** Capture node state for monitoring/audit.
4. **Context featurisation.** Build `φ ∈ ℝ²⁴` — 24-dimensional context vector.
5. **LinTS or CFS.** If LinTS confidence `≥ 0.70` (the empirical threshold `Θ`), use the bandit's chosen node; otherwise fall back to CFS composite score.
6. **PID swap if utilisation deviates `> 0.15`.** PID override `δ = 0.15`.
7. **Commit placement.**
8. **Async reward update.**

### CFS scoring

`score = 0.30·gap + 0.35·fit + 0.25·deadline + 0.10·affinity` over normalised vruntime gap, fit, deadline urgency, and affinity. `NICE_0_LOAD = 1024`. New tasks initialised at `min_vruntime − tick`.

### LinTS

Sherman–Morrison rank-one updates `O(d²)`. Prior `λ = 1.0`. Reward `0.5·util + 0.5·deadline`, capped `R_MAX = 10`. Sub-millisecond per-decision. Confidence is the `1/(1 + tr(A⁻¹))` formulation; below `Θ = 0.70`, decisions hand back to CFS.

### PID safety override

`Kp = 0.5, Ki = 0.1, Kd = 0.2`, derivative cap `D_MAX = 10`, anti-windup integral cap `10`. Bounded-input-bounded-output bound `|output| ≤ 3.5` proved in §.

### Monitoring stack

| Component | Statistics | Threshold |
|---|---|---|
| Holt–Winters | `σ_h²` formula in paper | MAPE 3.85 % on synthetic sinusoid |
| Page–Hinkley CUSUM | `n₀ = 30`, drift `k = 1`, threshold `h = 5`, cooldown `50` | empirical ARL₀ ≈ 3 485 vs theoretical ~22 000 |
| EWMA | `λ = 0.95` | warn `μ + 2σ`, crit `μ + 3σ` |
| ACF period detector | `min_lag = 4`, `max_lag = 120` | for periodic-load detection |

A `+3σ` step change is detected with **median 3 samples, p95 5 samples**.

---

## 📊 Reported benchmarks (paper.md)

| Workload | Result |
|---|---|
| **500 tasks / 16 nodes** | **p50 = 0.48 ms, p95 = 0.83 ms, p99 = 1.00 ms, max 16.6 ms cold** |
| Placement success | 100 % |
| Scaling | 4 → 128 nodes documented |
| Jain fairness | **1.00** |
| Holt–Winters MAPE on sinusoidal load | 3.85 % |
| ZScore experiment | precision 0.741, recall 1.000 |
| BatchOptimiser | 0.23 – 19.17 ms |
| Test cases | 80+ |

---

## 🚧 Honest caveats (paper §9)

- **No distributed coordination** in v1 — the scheduler is single-leader, in-memory state. A real distributed deployment would need consensus on the bandit's parameters or per-node bandits with sync.
- **Five recovery coroutines are stubs** — fault-recovery paths are sketched, not implemented.
- **Confidence threshold `Θ = 0.70` is empirical.** The paper does not provide a derivation; it's tuned on the synthetic workload.
- In a synthetic LinTS convergence test, confidence reached only `~0.042` after 500 observations — the full 24-d activation needs more data than that to dominate. Production deployments need to either (a) start with CFS dominant and let the bandit warm up, or (b) accept early-life behaviour will be CFS-only.
- **Holt–Winters underperforms on non-seasonal data** — known weakness of the family.
- Per-decision scoring is `O(n_nodes × d)` and **not parallelised**.

---

## 🎯 What this displaces

| Standard | What it lacks | What this scheduler adds |
|---|---|---|
| Linux CFS | No exploration; can't escape suboptimal-stable placements | LinTS exploration gated by confidence |
| LinTS / LinUCB | No fairness guarantee; can starve tasks | CFS fall-back below confidence |
| PID-only auto-scaler | No allocation policy | Bandit + fairness underneath |
| Kubernetes HPA | Simple metrics, no change-point detection | Page–Hinkley CUSUM, ARL₀ ≈ 3 500 |

---

## 🔗 Related work in this repo

- [`../Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — ARIA-INTEL (also Beta-MC + Bayesian fusion)
- [`../Filtering/`](../Filtering/) — GH-SR-IMM (also IMM-style mixing)
- [`../Cell AI/`](../Cell%20AI/) — Cypha-related differential information classifier shares lineage

---

[← Back to main README](../README.md)
