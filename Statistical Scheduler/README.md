# Neural-Heuristic Distributed Task Scheduler

A production-ready async Python scheduler combining Completely Fair Scheduling (CFS), Linear Thompson Sampling (LinTS), PID control, and a full real-time monitoring stack. Designed for heterogeneous compute clusters where placement quality, fairness, and load balance must all be maintained simultaneously without a central coordinator.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Scheduling Pipeline](#scheduling-pipeline)
3. [Core Components — Scheduler](#core-components--scheduler)
4. [Core Components — Monitoring](#core-components--monitoring)
5. [Mathematical Foundations](#mathematical-foundations)
6. [Configuration Reference](#configuration-reference)
7. [API Reference](#api-reference)
8. [Usage Examples](#usage-examples)
9. [Known Limitations](#known-limitations)

---

## Architecture Overview

The system is split across two modules:

**`scheduler_core.py`** — Placement decisions. Accepts tasks, maintains cluster state, runs the CFS/LinTS/PID decision pipeline, and returns node assignments.

**`monitoring_system.py`** — Continuous observation. Ingests metric time series, detects anomalies and change-points, fires alerts, and dispatches recovery actions.

Both modules run inside a single asyncio event loop and communicate through shared Python objects — no IPC, sockets, or message queues are required for single-host deployments.

```
             ┌──────────────────────────────────────────┐
             │           AdaptiveScheduler              │
             │                                          │
             │  ┌────────┐  ┌────────┐  ┌──────────┐   │
             │  │  CFS   │  │ LinTS  │  │   PID    │   │
             │  │(fair-  │  │(bandit │  │(load     │   │
             │  │ness)   │  │ rank)  │  │ balance) │   │
             │  └────────┘  └────────┘  └──────────┘   │
             └──────────────────┬───────────────────────┘
                                │ placement decisions
             ┌──────────────────▼───────────────────────┐
             │           RealTimeMonitor                │
             │                                          │
             │  HoltWinters · CUSUM · ZScore · Period   │
             │  MetricsManager (EWMA thresholds+alerts) │
             │  RecoverySystem (strategy dispatch)      │
             └──────────────────────────────────────────┘
```

---

## Scheduling Pipeline

Each call to `AdaptiveScheduler.schedule(task)` executes the following stages in order.

**1. Dependency gate.** If `task.dep_count > 0` the task is not yet eligible and `None` is returned immediately.

**2. Candidate filtering.** Nodes are filtered against three hard constraints: `node.health > 0` (dead nodes are excluded regardless of resources); anti-affinity (any node whose labels intersect `task.anti_affinity_groups` is excluded); and resource headroom (every resource in `task.resource_requirements` must fit on the node).

**3. Pre-placement snapshot.** The current `available` dict of every candidate node is captured before any modification. This snapshot is passed to the async reward computation so the reward reflects the actual utilisation gain, not the post-commit state.

**4. Feature engineering.** A 24-dimensional feature vector φ is constructed for each (task, node) pair.

**5. Ranking.** If LinTS posterior confidence ≥ 0.70, candidates are ranked by Thompson sampling from the learned posterior. Otherwise the CFS composite score is used as a heuristic fallback. The threshold prevents the bandit from acting on an uninformed prior at startup.

**6. PID override.** If the top-ranked node's utilisation deviates from target by more than 0.15 on any resource, the second-ranked candidate is used instead. This prevents piling tasks onto a node trending toward saturation even when LinTS prefers it.

**7. Commit.** Resources are deducted from the chosen node under a per-node `asyncio.Lock` to prevent double-booking under concurrent `asyncio.gather()` scheduling.

**8. Async reward update.** An `asyncio.create_task()` fires after the lock releases to compute the reward signal and update the LinTS posterior without blocking the caller.

---

## Core Components — Scheduler

### Task

```python
@dataclass
class Task:
    id:                    str
    resource_requirements: Dict[str, float]   # resource → fraction [0, 1]
    priority:              int                # 1 (urgent) to 10 (background)
    deadline:              float             # UNIX timestamp
    affinity_groups:       Set[str]          # preferred node labels
    anti_affinity_groups:  Set[str]          # forbidden node labels
    dep_count:             int               # blocked while > 0
```

`resource_requirements` uses fractions of node capacity rather than absolute units, so a task with `cpu: 0.25` requires 25% of a node's CPU regardless of its physical core count. This makes placement logic hardware-independent.

`priority` affects CFS task weight: lower numbers yield a higher weight, causing those tasks to accumulate vruntime more slowly and stay at the front of the scheduling queue longer.

`dep_count` is a gate the caller decrements as upstream tasks complete. The scheduler makes no attempt to track dependency graphs internally.

---

### NodeState

```python
@dataclass
class NodeState:
    id:        str
    available: Dict[str, float]   # resource → fraction free [0, 1]
    labels:    Set[str]           # for affinity matching
    health:    float              # [0, 1]; 0 = dead
    vruntime:  float              # node-level CFS accumulator
```

`available` is the live free-capacity dict, decremented by `_commit()` and restored by `mark_complete()`. Both `available` and `labels` are deep-copied on construction so that external mutation of the caller's dicts after `register_node()` cannot corrupt node state.

`health` acts as a continuous multiplicative penalty on the CFS score. At health = 0.0 the node is hard-excluded from all candidate sets regardless of available resources.

---

### CFSStatisticalModel

A statistical analogue of the Linux Completely Fair Scheduler — without a red-black tree. Maintains per-task virtual runtime history and uses it as a fairness signal in the composite placement score.

**Virtual runtime update** (mirrors `sched_update_curr`):

```
task_weight  = NICE_0_LOAD / max(cpu_req, 0.01)
Δvruntime    = Δwall_time × NICE_0_LOAD / task_weight
vruntime[t] += Δvruntime
min_vruntime  = min over all tracked tasks
```

CPU-heavy tasks accumulate vruntime quickly; tasks with small CPU requirements accumulate it slowly, so they receive proportionally more wall-clock time — preserving the CFS fairness invariant.

**New task initialisation.** A new task is assigned `vruntime = min_vruntime − one_tick` where `one_tick = NICE_0_LOAD / task_weight(cpu=0.5)`. This gives the new task a small advantage over any veteran whose own gap has decayed to zero, preserving fairness in sparse-workload conditions.

**Composite placement score:**

```
score(task, node) = W_vrt·V + W_fit·F + W_dl·D + W_aff·A
```

| Component | Formula | Meaning |
|-----------|---------|---------|
| V (vruntime gap) | `1 / (1 + vrt[task] − min_vruntime)` | Tasks furthest behind score highest |
| F (resource fit) | `mean(1 − |req − avail|)` over resources | Packing quality |
| D (deadline urgency) | `1 / (1 + ln(1 + slack))` | Imminent deadlines score highest |
| A (affinity) | 1.0 if labels intersect, 0.0 otherwise | Soft affinity bonus |

Anti-affinity is a hard constraint: if `task.anti_affinity_groups ∩ node.labels ≠ ∅`, `score()` returns `float('-inf')`.

**Default weights:** `W_vrt = 0.30`, `W_fit = 0.35`, `W_dl = 0.25`, `W_aff = 0.10`. `NICE_0_LOAD = 1024`.

---

### LinearThompsonSampling

A contextual bandit that learns which (task, node) feature combinations lead to good utilisation outcomes. Posterior inference is exact under a Bayesian linear regression model with Gaussian prior.

**Model.** The reward for placing a task with features φ is modelled as `r = wᵀφ + ε`, where `ε ~ N(0,1)` and the prior is `p(w) = N(0, λ⁻¹I)` with `λ = LAMBDA_PRIOR = 1.0`.

**Posterior update** (Sherman-Morrison rank-1, O(d²) per step, no matrix inversion):

```
A⁻¹[t] = A⁻¹[t-1] − (A⁻¹φ)(A⁻¹φ)ᵀ / (1 + φᵀA⁻¹φ)
b[t]    = b[t-1] + r·φ
μ[t]    = A⁻¹[t]·b[t]
```

**Thompson sampling.** At decision time: `w̃ ~ N(μ, V_SAMPLE²·A⁻¹)`. Each candidate is scored by `w̃ᵀφ` and ranked descending. `V_SAMPLE = 1.0` gives standard exploration.

**Confidence:** `1 / (1 + tr(A⁻¹))` — a decreasing function of total posterior variance. Starts near zero and increases asymptotically toward 1 as observations accumulate.

**Regret bound:** `E[R(T)] = O(d√T · polylog T)` (Agrawal & Goyal 2013), d = 24.

**Feature vector** (`FEATURE_DIM = 24`):

| Dims | Content |
|------|---------|
| 0–5 | `node.available[r]` for each of `['cpu','memory','network','disk','gpu','io']` |
| 6–11 | `task.req[r]` for the same canonical resources |
| 12 | `node.health` |
| 13 | system-wide mean CPU usage |
| 14 | deadline urgency `1/(1+ln(1+slack))` |
| 15 | `task.priority / 10` |
| 16 | posterior confidence |
| 17 | `node.vruntime / 1000` |
| 18 | `task.dep_count` |
| 19–23 | reserved (zero-padded) |

Missing resources default to 0 for availability and the task's stated requirement for demand. The vector is always exactly 24 dimensions.

**Reward signal:**

```
util_reward = clip(post_utilisation − pre_utilisation, 0, 1)
dl_reward   = 1 / (1 + ln(1 + slack))
reward      = 0.5·util_reward + 0.5·dl_reward
```

Utilisation is computed over the task's own resource keys only (not the full node resource dict). Rewards are clamped to `[−R_MAX, +R_MAX]` where `R_MAX = 10.0` before the posterior update, preventing outliers from dominating the posterior mean.

---

### PIDController

A discrete-time PID controller. Detects when a node's utilisation is trending away from its configured target, triggering the step-6 pipeline override.

**Control law:**

```
u[t] = Kp·e[t] + Ki·∑ e[i]·Δtᵢ + Kd·clamp((e[t] − e[t−1]) / Δt, ±D_MAX)
```

**Parameters (defaults):** `Kp = 0.5`, `Ki = 0.1`, `Kd = 0.2`, `windup_limit = 10.0`, `D_MAX = 10.0`.

The integral uses per-step `e·Δt` accumulation with variable time deltas and is hard-clamped to `±windup_limit`. The derivative is clamped to `±D_MAX` to handle near-zero-dt cases — without clamping, a microsecond-scale tick gap produces corrections four orders of magnitude larger than normal. Each metric tracked by the controller maintains independent integral and last-error state.

---

### BatchOptimiser

Groups tasks into batches by resource profile similarity using cosine similarity on a normalised fingerprint vector. Tasks within the same batch are co-schedulable.

**Algorithm:** compute a unit-normalised fingerprint over `['cpu','memory','network','disk','gpu','io']` for each task; sort by L2 norm (O(n log n)); greedily assign each task to the first batch whose centroid cosine similarity ≥ `THRESHOLD = 0.90`, or start a new batch; cap batches at `MAX_BATCH_SIZE = 32`. Zero-norm vectors (tasks with no resource requirements) are handled without division.

This replaces an O(n²) pairwise comparison with an O(n log n) sort + linear sweep.

---

### ResourceOptimiser

Best-Fit Decreasing (BFD) bin packing. Assigns a batch of tasks to nodes maximising packing density.

Sort tasks descending by total resource demand; for each task, select the node with the least remaining capacity that still fits all requirements (best-fit). If no single node fits the whole batch, fall back to per-task individual best-fit to avoid silently dropping tasks.

**Competitive ratio:** ≤ 11/9·OPT + 6/9 in 1D (Coffman et al.). Competitive in multi-dimensional workloads with the decreasing sort.

---

### AdaptiveScheduler

The top-level orchestrator. Owns the node registry, all sub-components, and per-node async locks.

| Method | Description |
|--------|-------------|
| `register_node(node)` | Add node to active pool |
| `deregister_node(node_id)` | Remove node; in-flight tasks are not migrated |
| `schedule(task)` → `Optional[str]` | Place single task; returns node ID or None |
| `schedule_batch(tasks)` → `Dict[str, Optional[str]]` | Concurrent placement via `asyncio.gather` |
| `mark_complete(task_id, node_id, elapsed_s, freed)` | Free resources and update CFS vruntime |
| `stats()` → `Dict[str, float]` | Completion latencies, LinTS confidence, observation count |

If `node_id` is not in the registry when `mark_complete` is called (node deregistered between placement and completion), the call is silently ignored. CFS vruntime is always updated regardless.

---

## Core Components — Monitoring

### HoltWinters

Additive Holt-Winters exponential smoothing. Decomposes a univariate series into level, trend, and seasonal components and produces multi-step forecasts with approximate prediction intervals.

**Update equations** (Hyndman & Athanasopoulos §8.5):

```
l[t] = α·(y[t] − s[t−m]) + (1−α)·(l[t−1] + b[t−1])
b[t] = β·(l[t] − l[t−1]) + (1−β)·b[t−1]
s[t] = γ·(y[t] − l[t])   + (1−γ)·s[t−m]
```

**h-step ahead forecast:**

```
ŷ[t+h] = l[t] + h·b[t] + s[t − m + ((h−1) mod m) + 1]
```

The seasonal index wraps correctly for arbitrary h > m.

**Prediction interval** (Hyndman 2008):

```
σ²_h ≈ σ²_ε · (1 + (h−1)·(α + β·h)²)
95% PI: ŷ ± 1.96·√σ²_h
```

**Initialisation.** Requires `m` observations before activating. During burn-in, `forecast()` returns `(NaN, NaN)`. Bootstrap: level = mean of first m samples; trend = OLS slope; seasonal indices = deviations from the level.

**NaN/Inf guard.** Non-finite inputs are silently dropped. A single bad sensor reading cannot corrupt the model state.

**Parameters (defaults):** `period = 60`, `alpha = 0.3`, `beta = 0.1`, `gamma = 0.2`.

---

### CUSUMDetector

Online Page-Hinkley CUSUM change-point detector.

**Algorithm.** Baseline μ₀, σ₀ estimated from `burnin` samples. After burn-in:

```
z[t]  = (x[t] − μ₀) / σ₀
S⁺[t] = max(0, S⁺[t−1] + z[t] − k)
S⁻[t] = max(0, S⁻[t−1] − z[t] − k)
detect if S⁺[t] > h or S⁻[t] > h
```

Both accumulators reset after a detection; a cooldown period prevents re-triggering.

**ARL₀.** Defaults `k=1.0, h=5.0` give theoretical ARL₀ ≈ 22,000 steps (standard normal null). Empirical ARL₀ with burn-in and cooldown is ≈ 500–2000, adequate for 1 Hz monitoring.

**`reset_baseline(new_mu, new_sig)`.** Resets both accumulators and the cooldown counter so the detector can immediately fire on the first genuine change in the new regime.

**Parameters (defaults):** `burnin = 30`, `k = 1.0`, `h = 5.0`, `cooldown = 50`.

---

### ZScoreAnomaly

Online EWMA-based anomaly detector.

```
μ[t]  = α·x[t] + (1−α)·μ[t−1]
σ²[t] = α·(x[t] − μ[t])² + (1−α)·σ²[t−1]
z[t]  = (x[t] − μ[t]) / max(σ[t], ε)
```

Flag when `|z[t]| > k`. Default `k=3.0` gives 0.3% false-positive rate under Gaussian assumptions; Chebyshev bound is 1/k² = 11% distribution-free. The variance denominator is floored at ε — after long exposure to a constant signal, any deviation correctly produces a very large z-score.

**Parameters (defaults):** `k = 3.0`, `ewma_alpha = 0.05`.

---

### PeriodEstimator

ACF-based period estimation. Computes autocorrelation from lag `min_lag` to `max_lag`, identifies local maxima, and returns the smallest lag exceeding the mean ACF value — the fundamental period, not a harmonic. Returns `strength` as the ACF value at the dominant lag.

Run every 60 samples inside PatternDetector to amortise O(n²) cost.

**Parameters (defaults):** `max_lag = 120`, `min_lag = 4`.

---

### PatternDetector

Composable per-metric analyser. Wraps HoltWinters, CUSUMDetector, ZScoreAnomaly, and PeriodEstimator into a single call. Each metric gets its own independent instances, lazily initialised on first observation.

**`analyse(metric, value)` output:**

| Key | Type | Description |
|-----|------|-------------|
| `forecast` | float | HW 1-step prediction; NaN before initialisation |
| `forecast_lo` | float | Lower 95% prediction bound |
| `forecast_hi` | float | Upper 95% prediction bound |
| `trend` | float | Current trend component b[t] |
| `z_score` | float | Standardised anomaly score |
| `is_anomaly` | bool | Whether z-score exceeded threshold |
| `change_point` | bool | Whether CUSUM triggered this step |
| `period` | float | Dominant period; NaN if not detected |
| `period_strength` | float | ACF strength at dominant lag |

`forecast` is `NaN` during HoltWinters burn-in. Callers must not treat the warm-up period as a genuine model prediction.

---

### MetricsManager

Ingests metric samples into rolling deques, computes adaptive EWMA thresholds, and dispatches `Alert` objects to registered handlers.

**Threshold model:**

```
μ[t]  = λ·μ[t−1] + (1−λ)·m[t]
σ²[t] = λ·σ²[t−1] + (1−λ)·(m[t] − μ[t])²

warning threshold:  τ_w = μ[t] + 2·σ[t]
critical threshold: τ_c = μ[t] + 3·σ[t]
```

By Chebyshev: `k=2` ≤ 25% exceedance probability; `k=3` ≤ 11%. For Gaussian metrics: 4.6% and 0.3%.

Alert handlers are each wrapped in `try/except`. A crashing handler is logged and skipped; all subsequent handlers always fire.

**Default alert configurations:**

| Metric | Action |
|--------|--------|
| `cpu_usage` | reduce_load |
| `memory_usage` | clear_cache |
| `latency_p99` | circuit_break |
| `error_rate` | network_retry |

Unknown metrics are ingested and stored but generate no alerts.

**Parameters (defaults):** `EWMA_LAMBDA = 0.95`, `MIN_HISTORY = 60`, `WINDOW = 1000`.

| Method | Description |
|--------|-------------|
| `ingest(data)` | Async. Ingest `Dict[str, float]` metric tick |
| `add_handler(fn)` | Register alert callback `fn(alert: Alert)` |
| `series(name, n=200)` | Last n values in chronological order |
| `summary(name)` | Dict with mean, std, min, max |

---

### RecoverySystem

Async strategy dispatcher. Maps failure type strings to recovery coroutines, records outcomes, and exposes per-strategy success rates.

| Canonical / Alias | Default action |
|---|---|
| `reduce_load` / `resource_exhaustion` / `cpu_usage` | stub — implement pod eviction / load shedding |
| `clear_cache` / `memory_usage` | stub — implement cache flush |
| `circuit_break` / `latency_p99` | stub — implement circuit breaker |
| `network_retry` / `error_rate` | exponential backoff, 3 attempts |
| `cascade_isolate` / `cascade_failure` | stub — implement node isolation |

Every execution is recorded to `history[failure_type]` with UUID, start timestamp, duration, and outcome. `success_rate(failure_type)` returns the empirical success proportion across all recorded attempts. Unknown failure types record as failed with zero duration.

The strategy coroutines are stubs; replace each body with real system calls before production deployment.

---

### RealTimeMonitor

1 Hz async orchestration loop. Polls registered metric sources, feeds data into MetricsManager and PatternDetector, and triggers RecoverySystem actions on change-points and critical alerts.

**Automatic actions:**
- Change-point detected by PatternDetector → `RecoverySystem.execute('reduce_load', ...)`
- Critical alert from MetricsManager → `RecoverySystem.execute('circuit_break', ...)`

Source errors are caught per-source without stopping the loop. `TICK_S = 1.0` is a class constant; set before instantiation to change cadence.

```python
monitor = RealTimeMonitor()
monitor.register_source('app', my_async_metric_fn)
await monitor.run()     # cancel to stop
```

The source coroutine must return `Dict[str, float]`. Multiple sources are all polled every tick.

---

## Mathematical Foundations

### CFS Fairness Invariant

`V(t) = 1 / (1 + vrt[t] − min_vruntime)` is maximum (= 1.0) for the task with the smallest vruntime, strictly decreasing as the lag grows, continuous, and bounded in (0, 1]. New tasks start at `min_vruntime − one_tick`, guaranteeing they always score higher than any veteran whose gap has decayed to zero.

### PID Discrete Stability

Per-step `e·Δt` integral accumulation with hard anti-windup clamping at `±windup_limit` makes the controller unconditionally BIBO stable under bounded utilisation input. Derivative clamping at `±D_MAX` handles singular near-zero-dt cases without introducing discontinuous corrections.

### LinTS PSD Guarantee

`A[t] = λI + ΦᵀΦ` with `λ > 0` and `ΦᵀΦ ≽ 0` guarantees `A[t] ≻ 0` for all t. The Sherman-Morrison rank-1 update preserves positive definiteness analytically. Minimum eigenvalue of `A⁻¹` stays strictly positive across 10,000 updates under randomised input.

### HoltWinters PI Coverage

With default smoothing parameters on sinusoidal signals with additive Gaussian noise, the approximate 95% prediction interval achieves ≥ 90% empirical coverage on held-out test points. The Hyndman (2008) variance inflation `σ²_h = σ²_ε·(1 + (h−1)·(α + β·h)²)` correctly widens intervals with forecast horizon.

### CUSUM ARL₀

Default `k=1.0, h=5.0` gives theoretical ARL₀ ≈ 22,000 (standard normal null). Empirical ARL₀ with burn-in and cooldown is ≈ 500–2000 — adequate for 1 Hz monitoring where false positives incur unnecessary recovery overhead.

---

## Configuration Reference

### Scheduler

| Constant | Location | Default | Description |
|----------|----------|---------|-------------|
| `CONFIDENCE_THRESHOLD` | `AdaptiveScheduler` | `0.70` | LinTS confidence below which CFS fallback is used |
| `RESOURCE_TARGETS` | `AdaptiveScheduler` | `{cpu:0.70, mem:0.75}` | PID utilisation setpoints |
| `NICE_0_LOAD` | `CFSStatisticalModel` | `1024` | CFS base weight |
| `FEATURE_DIM` | `LinearThompsonSampling` | `24` | φ vector length |
| `LAMBDA_PRIOR` | `LinearThompsonSampling` | `1.0` | Ridge prior precision λ |
| `R_MAX` | `LinearThompsonSampling` | `10.0` | Reward clamp bound |
| `V_SAMPLE` | `LinearThompsonSampling` | `1.0` | Thompson exploration inflation |
| `THRESHOLD` | `BatchOptimiser` | `0.90` | Cosine similarity grouping threshold |
| `MAX_BATCH_SIZE` | `BatchOptimiser` | `32` | Maximum tasks per batch |
| `Kp / Ki / Kd` | `PIDController` | `0.5 / 0.1 / 0.2` | PID gains |
| `windup_limit` | `PIDController` | `10.0` | Anti-windup integral cap |
| `D_MAX` | `PIDController` | `10.0` | Derivative term clamp |

### Monitoring

| Constant | Location | Default | Description |
|----------|----------|---------|-------------|
| `period` | `HoltWinters` | `60` | Seasonal period in samples |
| `alpha / beta / gamma` | `HoltWinters` | `0.3 / 0.1 / 0.2` | Level / trend / seasonal smoothing |
| `burnin` | `CUSUMDetector` | `30` | Samples before detection |
| `k` | `CUSUMDetector` | `1.0` | CUSUM slack |
| `h` | `CUSUMDetector` | `5.0` | CUSUM threshold |
| `cooldown` | `CUSUMDetector` | `50` | Steps silenced after detection |
| `k` | `ZScoreAnomaly` | `3.0` | Anomaly z-score threshold |
| `ewma_alpha` | `ZScoreAnomaly` | `0.05` | EWMA forgetting factor |
| `max_lag / min_lag` | `PeriodEstimator` | `120 / 4` | ACF lag range |
| `EWMA_LAMBDA` | `MetricsManager` | `0.95` | Threshold adaptation speed |
| `MIN_HISTORY` | `MetricsManager` | `60` | Samples before alerts |
| `WINDOW` | `MetricsManager` | `1000` | Rolling history deque size |
| `TICK_S` | `RealTimeMonitor` | `1.0` | Monitoring cadence (seconds) |

---

## API Reference

### scheduler_core

```python
# Cluster management
scheduler = AdaptiveScheduler()
scheduler.register_node(NodeState(id='n0', available={'cpu': 1.0, 'memory': 1.0}))
scheduler.deregister_node('n0')

# Placement
node_id: Optional[str] = await scheduler.schedule(task)
results: Dict[str, Optional[str]] = await scheduler.schedule_batch(tasks)
scheduler.mark_complete(task_id, node_id, elapsed_s=12.3, freed={'cpu': 0.2})

# Telemetry
stats = scheduler.stats()
# {'n_completions': 47, 'mean_s': 8.1, 'p95_s': 22.3,
#  'lints_confidence': 0.83, 'lints_n_obs': 47.0}

# Sub-components independently
batches: Dict[str, List[Task]] = BatchOptimiser().optimise(tasks)
placements: Dict[str, Optional[str]] = ResourceOptimiser().optimise(tasks, nodes)

cfs = CFSStatisticalModel()
cfs.initialise_task(task_id)
cfs.update_vruntime(task_id, elapsed_s=5.0, cpu_req=0.3)
score: float = cfs.score(task, node)

lts = LinearThompsonSampling()
phi: np.ndarray = lts.feature_vector(node, task, system_load=0.4)
ranked = lts.sample_and_rank(candidates)     # List[Tuple[str, np.ndarray]]
lts.update(phi, reward=0.72)
lts.confidence        # float [0, 1)
lts.n_observations    # int
```

### monitoring_system

```python
# Pattern analysis
detector = PatternDetector()
result = detector.analyse('cpu_usage', 0.73)
# {'forecast': 0.71, 'forecast_lo': 0.65, 'forecast_hi': 0.77,
#  'trend': 0.002, 'z_score': 0.4, 'is_anomaly': False,
#  'change_point': False, 'period': 3600.0, 'period_strength': 0.82}

# Metrics management
mm = MetricsManager()
mm.add_handler(lambda alert: print(alert.metric, alert.severity, alert.value))
await mm.ingest({'cpu_usage': 0.91, 'memory_usage': 0.55})
mm.series('cpu_usage', n=60)    # List[float], chronological
mm.summary('cpu_usage')         # {'mean': ..., 'std': ..., 'min': ..., 'max': ...}

# Recovery
rs = RecoverySystem()
ok: bool = await rs.execute('resource_exhaustion', {'node': 'n0'})
rate: float = rs.success_rate('resource_exhaustion')

# Full monitoring loop
monitor = RealTimeMonitor()
monitor.register_source('cluster', async_metric_fn)
await monitor.run()

# Individual components
hw = HoltWinters(period=24, alpha=0.2, beta=0.05, gamma=0.15)
hw.update(42.3)
point, half_width = hw.forecast(h=6)    # (NaN, NaN) before init

cusum = CUSUMDetector(burnin=30, k=1.0, h=5.0, cooldown=50)
changed: bool = cusum.update(x)
cusum.reset_baseline(new_mu=10.0, new_sig=2.0)

zs = ZScoreAnomaly(k=3.0, ewma_alpha=0.05)
is_anomaly, z_score = zs.update(x)

pe = PeriodEstimator(max_lag=120, min_lag=4)
result = pe.estimate(series)    # {'period': 24.0, 'strength': 0.87}
```

---

## Usage Examples

### Basic cluster setup

```python
import asyncio, time
from scheduler_core import AdaptiveScheduler, NodeState, Task

async def main():
    s = AdaptiveScheduler()
    for i in range(4):
        s.register_node(NodeState(
            id=f'node-{i}',
            available={'cpu': 1.0, 'memory': 1.0, 'gpu': 1.0 if i < 2 else 0.0},
            labels={'gpu'} if i < 2 else {'cpu'},
        ))

    tasks = [
        Task(id=f'job-{i}', resource_requirements={'cpu': 0.25, 'memory': 0.10},
             priority=3, deadline=time.time() + 300)
        for i in range(12)
    ]

    results = await s.schedule_batch(tasks)
    print(f'Placed {sum(1 for v in results.values() if v)}/{len(tasks)}')

    for task_id, node_id in results.items():
        if node_id:
            task = next(t for t in tasks if t.id == task_id)
            s.mark_complete(task_id, node_id, elapsed_s=45.0,
                            freed=task.resource_requirements)

asyncio.run(main())
```

### Affinity and anti-affinity

```python
# Must land on a GPU node
gpu_task = Task('train-0', {'cpu': 0.5, 'gpu': 0.8}, priority=1,
                deadline=time.time()+60, affinity_groups={'gpu'})

# Must NOT co-locate with other shards
shard = Task('shard-0', {'cpu': 0.2, 'memory': 0.4}, priority=5,
             deadline=time.time()+3600, anti_affinity_groups={'shard'})
```

### Dependency-gated tasks

```python
task_a = Task('a', {'cpu': 0.3}, priority=2, deadline=time.time()+100)
task_b = Task('b', {'cpu': 0.2}, priority=4, deadline=time.time()+200, dep_count=1)

node_a = await scheduler.schedule(task_a)
scheduler.mark_complete('a', node_a, elapsed_s=10.0, freed={'cpu': 0.3})
task_b.dep_count -= 1   # now eligible
node_b = await scheduler.schedule(task_b)
```

### Monitoring integration

```python
from monitoring_system import RealTimeMonitor, Alert

async def read_metrics() -> dict:
    return {'cpu_usage': get_cpu(), 'memory_usage': get_mem(), 'latency_p99': get_p99()}

def handle_alert(alert: Alert):
    if alert.severity == 'critical':
        page_on_call(alert.metric, alert.value, alert.threshold)

async def main():
    monitor = RealTimeMonitor()
    monitor.register_source('cluster', read_metrics)
    monitor.metrics.add_handler(handle_alert)
    await monitor.run()
```

### Standalone pattern analysis

```python
import math
from monitoring_system import PatternDetector

detector = PatternDetector(hw_period=24)
for t, value in enumerate(metric_stream):
    result = detector.analyse('request_rate', value)
    if not math.isnan(result['forecast']):
        print(f't={t}: {result["forecast"]:.3f} [{result["forecast_lo"]:.3f}, {result["forecast_hi"]:.3f}]')
    if result['change_point']:
        print(f't={t}: regime shift')
    if result['is_anomaly']:
        print(f't={t}: anomaly z={result["z_score"]:.2f}')
```

---

## Known Limitations

**No distributed coordination.** The per-node `asyncio.Lock` prevents double-booking within a single event loop. Multiple `AdaptiveScheduler` instances targeting the same physical cluster will over-allocate resources without an external coordinator or distributed lock.

**Recovery strategy stubs.** The five recovery coroutines (`_reduce_load`, `_clear_cache`, `_circuit_break`, `_network_retry`, `_cascade_isolate`) sleep and return `True`. They must be replaced with real system calls (Kubernetes API, cgroup adjustments, load balancer reconfiguration, etc.) before production use. Outcome tracking and success rates function correctly regardless.

**No state persistence.** All state — LinTS posterior, CFS vruntime history, node registry, metric history — lives in memory. A process restart begins from a cold start. Serialise `lints._Ainv`, `lints._b`, `cfs.vruntime_history`, and `mm._series` to an external store if continuity across restarts is required.

**HoltWinters on non-seasonal signals.** The additive HW model assumes a periodic component. On purely linear or random-walk signals, the seasonal indices introduce systematic forecast error. Use the `trend` component directly and treat `forecast` as unreliable when the signal is known to be non-seasonal.

**LinTS feature space is fixed.** The feature vector has 5 reserved zero-padding dimensions for minor extensions. Substantive extensions beyond those 5 dimensions require restarting from a cold posterior, since `A` and `b` are fixed-shape matrices allocated at construction.

**Single-event-loop throughput.** Per-node locks serialise commits per node but do not parallelise candidate scoring. Under very high concurrency (thousands of tasks per second across hundreds of nodes), scoring may become a bottleneck. Partitioning the node pool into independently scheduled shards is the recommended scaling path.
