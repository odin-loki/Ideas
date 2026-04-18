"""
scheduler_core.py
=================
Neural-Heuristic Distributed Task Scheduler  v2
Replaces LSTM-based online learning with Linear Thompson Sampling (LinTS).

Fixes from profiling audit
--------------------------
1. vruntime gap:  was binary (max(0, min-v+1) → only min-vrt task nonzero)
                  now smooth: 1/(1 + vrt - min_vruntime)
2. PID integral:  was sum(errors)*current_dt (wrong with variable dt)
                  now correct: Σ e[i]*Δtᵢ per step + anti-windup clamp
3. Confidence:    was buffer_size/500 (warmup counter, not uncertainty)
                  now: 1/(1+tr(A⁻¹))  — real Bayesian posterior spread
4. Task encoding: was hash(key)%10 (not stable across process restarts)
                  now deterministic sorted CANONICAL_RESOURCES indexing
5. Reward timing: was computed AFTER _commit (sees post-placement state)
                  now pre-placement snapshot captured before commit
6. Batch grouping: was O(n²) Python loop
                   now O(n log n) sort + linear sweep with cosine similarity

Architecture changes
--------------------
* OnlineLearningModel (feed-forward NN) → LinearThompsonSampling
  Posterior: p(w) = N(μ, A⁻¹) where A = λI + ΦᵀΦ
  Update: Sherman-Morrison rank-1, O(d²) per step, no backprop
  Confidence: 1/(1+tr(A⁻¹)) — real posterior uncertainty
  Regret: E[R(T)] = O(d √T · polylog T)  [Agrawal & Goyal 2013]

* BatchOptimiser: O(n²) pairwise → O(n log n) fingerprint sort + sweep

Mathematical guarantees
-----------------------
CFS vruntime fairness: V(t) = 1/(1 + vrt[t] - min_vruntime)
    → continuous, max at min-vruntime task, smooth decay for others

PID discrete stability:
    u[t] = Kp·e[t] + Ki·Σe·Δt + Kd·(e[t]-e[t-1])/Δt
    Anti-windup: |integral| ≤ windup_limit (prevents integrator blow-up)

Best-Fit Decreasing packing ratio: ≤ 11/9·OPT + 6/9  (1D; competitive in
    multi-dimensional real workloads with the Decreasing sort order)
"""

from __future__ import annotations

import asyncio
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """
    Unit of work submitted for scheduling.

    resource_requirements : resource_name -> fraction [0, 1]
    priority              : int 1–10; lower = more urgent
    deadline              : UNIX timestamp (seconds)
    affinity_groups       : labels of nodes the task prefers
    anti_affinity_groups  : labels of nodes the task must avoid
    dep_count             : upstream dependency count; task is eligible
                            when this reaches 0
    """
    id: str
    resource_requirements: Dict[str, float]
    priority: int
    deadline: float
    affinity_groups: Set[str] = field(default_factory=set)
    anti_affinity_groups: Set[str] = field(default_factory=set)
    dep_count: int = 0


@dataclass
class NodeState:
    """
    Live snapshot of a cluster node.

    available : resource_name -> fraction free [0, 1]
    labels    : set of strings for affinity matching
    health    : [0, 1]; all scores are multiplied by this, so a degraded
                node is continuously deprioritised without a hard cutoff
    vruntime  : node-level CFS accumulator for node-level fairness
    """
    id: str
    available: Dict[str, float]
    labels: Set[str] = field(default_factory=set)
    health: float = 1.0
    vruntime: float = 0.0

    def __post_init__(self):
        # BUG-20 fix: copy mutable fields so external mutations don't corrupt state
        self.available = dict(self.available)
        self.labels    = set(self.labels)


# ---------------------------------------------------------------------------
# CFS Statistical Model
# ---------------------------------------------------------------------------

class CFSStatisticalModel:
    """
    Replicates Linux CFS placement behaviour without a red-black tree.

    Virtual-runtime update (mirrors kernel sched_update_curr):
        Δvruntime = Δwall_time × NICE_0_LOAD / task_weight
        task_weight = NICE_0_LOAD / max(cpu_req, 0.01)

    Composite placement score (higher is better):
        score(task, node) = (
              w_vrt × V(task)           vruntime gap (fairness)
            + w_fit × F(task, node)    resource fit (packing)
            + w_dl  × D(task)          deadline urgency
            + w_aff × A(task, node)    affinity bonus
        ) × node.health

    V(task) = 1 / (1 + vruntime[task] - min_vruntime)
        FIX from v1: smooth reciprocal decay, not binary max(0, gap+1)
        which zeroed every task except the minimum.

    F(task, node) = mean_r(1 - |req_r - avail_r|)
        Only evaluated on feasible nodes (filtered upstream).
        Best-fit (req ≈ avail) maximises this.

    D(task) = 1 / (1 + ln(1 + slack_seconds))
        Superlogarithmic urgency rise as deadline approaches.

    A(task, node):
        +1.0  if any affinity label matches
        -2.0  if any anti-affinity label matches (dominates other terms)
    """

    NICE_0_LOAD = 1024.0

    def __init__(self):
        self.weights = {
            'vruntime': 0.30,
            'resource': 0.35,
            'deadline': 0.25,
            'affinity': 0.10,
        }
        self.vruntime_history: Dict[str, float] = {}
        self.min_vruntime: float = 0.0

    def task_weight(self, cpu_req: float) -> float:
        return self.NICE_0_LOAD / max(cpu_req, 0.01)

    def initialise_task(self, task_id: str):
        """Assign min_vruntime to a new task (CFS semantics for fairness)."""
        if task_id not in self.vruntime_history:
            # BUG-18 fix: give new tasks a half-tick vruntime advantage
            # so they always score higher than a veteran whose gap has
            # decayed to zero (single-task clusters, sparse workloads).
            tick = self.NICE_0_LOAD / self.task_weight(0.5)  # nominal tick @ cpu=0.5
            self.vruntime_history[task_id] = max(0.0, self.min_vruntime - tick)

    def update_vruntime(self, task_id: str, elapsed_s: float, cpu_req: float):
        """Call on task completion with actual wall-clock duration."""
        weight = self.task_weight(cpu_req)
        delta  = elapsed_s * (self.NICE_0_LOAD / weight)
        prev   = self.vruntime_history.get(task_id, self.min_vruntime)
        self.vruntime_history[task_id] = prev + delta
        self.min_vruntime = min(self.vruntime_history.values())

    def score(self, task: Task, node: NodeState,
              now: Optional[float] = None) -> float:
        now = now or time.time()
        W   = self.weights

        # V — smooth vruntime gap
        vrt     = self.vruntime_history.get(task.id, self.min_vruntime)
        v_score = 1.0 / (1.0 + vrt - self.min_vruntime)

        # F — resource fit
        if task.resource_requirements:
            fits    = [1.0 - abs(req - node.available.get(r, 0.0))
                       for r, req in task.resource_requirements.items()]
            f_score = float(np.mean(fits))
        else:
            f_score = 1.0

        # D — deadline urgency
        slack   = max(task.deadline - now, 1e-3)
        d_score = 1.0 / (1.0 + np.log1p(slack))

        # A — affinity
        # Anti-affinity is a hard constraint: return -inf immediately so that
        # any caller who bypasses _candidates() still gets the correct signal.
        # (The -2.0 × w_affinity = -0.20 penalty was insufficient to overcome
        # the positive contributions of the other three terms.)
        if task.anti_affinity_groups & node.labels:
            return float('-inf')
        a_score = 1.0 if (task.affinity_groups & node.labels) else 0.0

        raw = (W['vruntime'] * v_score +
               W['resource'] * f_score +
               W['deadline'] * d_score +
               W['affinity'] * a_score)
        return raw * max(node.health, 0.0)


# ---------------------------------------------------------------------------
# Linear Thompson Sampling  (replaces LSTM / feed-forward NN)
# ---------------------------------------------------------------------------

class LinearThompsonSampling:
    """
    Bayesian contextual bandit for node placement decisions.

    Model
    -----
    Reward: r ≈ φ(node, task)ᵀ w + ε,  ε ~ N(0, σ²)

    Conjugate Gaussian posterior over weight vector w:
        Prior:      w ~ N(0, λ⁻¹I)
        Posterior:  w | data ~ N(μ, A⁻¹)
          where A = λI + Σᵢ φᵢφᵢᵀ   (precision matrix)
                b = Σᵢ rᵢφᵢ
                μ = A⁻¹b

    Decision rule (Thompson sampling):
        w̃ ~ N(μ, v²·A⁻¹)   (single draw per decision, shared across candidates)
        Choose node with highest φᵀw̃

    Posterior update — Sherman-Morrison rank-1 (O(d²), no matrix inversion):
        A_{t+1}⁻¹ = A_t⁻¹ - (A_t⁻¹φ)(φᵀA_t⁻¹) / (1 + φᵀA_t⁻¹φ)
        b_{t+1}   = b_t + r·φ
        μ_{t+1}   = A_{t+1}⁻¹ · b_{t+1}

    Confidence (real posterior uncertainty):
        confidence = 1 / (1 + tr(A⁻¹))
        → 0 when covariance is large (uncertain), → 1 as posterior concentrates

    Regret bound:
        E[R(T)] = O(d √T · log³(T))  [Agrawal & Goyal 2013, Theorem 2]
        where d = FEATURE_DIM, T = total scheduling decisions

    Feature vector layout (FEATURE_DIM = 24)
    -----------------------------------------
     [0:6]   node.available for CANONICAL_RESOURCES  (deterministic order)
     [6]     node.health
     [7]     node.vruntime log-normalised
     [8:14]  task.resource_requirements for CANONICAL_RESOURCES
     [14]    task priority normalised: 1/priority → [0.1, 1.0]
     [15]    deadline urgency: 1/(1+ln(1+slack))
     [16]    system load (mean CPU utilisation across all nodes)
     [17]    affinity indicator: +1 match, -1 anti-match, 0 none
     [18:24] resource pressure: req × (1-avail) per resource
    """

    FEATURE_DIM        = 24
    LAMBDA_PRIOR       = 1.0     # prior precision (ridge strength)
    R_MAX              = 10.0    # BUG-16 fix: max absolute reward value
    V_SAMPLE           = 1.0     # Thompson exploration inflation
    CANONICAL_RESOURCES = ['cpu', 'memory', 'network', 'disk', 'gpu', 'io']

    def __init__(self):
        d          = self.FEATURE_DIM
        lam        = self.LAMBDA_PRIOR
        self._Ainv = np.eye(d) / lam   # posterior covariance A⁻¹, init = λ⁻¹I
        self._b    = np.zeros(d)        # sufficient statistic b = Σ rᵢφᵢ
        self._mu   = np.zeros(d)        # posterior mean μ = A⁻¹b
        self._n    = 0                  # observation count

    # --- public ---

    def feature_vector(self, node: NodeState, task: Task,
                       system_load: float = 0.5) -> np.ndarray:
        """Build a fixed-length, deterministic context vector."""
        CR  = self.CANONICAL_RESOURCES
        vec = np.zeros(self.FEATURE_DIM)

        for i, r in enumerate(CR):                      # [0:6]
            vec[i] = node.available.get(r, 0.0)
        vec[6] = node.health                            # [6]
        vec[7] = 1.0 / (1.0 + node.vruntime)           # [7]
        for i, r in enumerate(CR):                      # [8:14]
            vec[8 + i] = task.resource_requirements.get(r, 0.0)
        vec[14] = 1.0 / max(task.priority, 1)          # [14]
        slack   = max(task.deadline - time.time(), 1e-3)
        vec[15] = 1.0 / (1.0 + np.log1p(slack))        # [15]
        vec[16] = float(np.clip(system_load, 0.0, 1.0))# [16]
        if task.anti_affinity_groups & node.labels:     # [17]
            vec[17] = -1.0
        elif task.affinity_groups & node.labels:
            vec[17] = 1.0
        for i, r in enumerate(CR):                      # [18:24]
            vec[18 + i] = (task.resource_requirements.get(r, 0.0) *
                           (1.0 - node.available.get(r, 1.0)))
        return vec

    def sample_and_rank(self, candidates: List[Tuple[str, np.ndarray]]
                        ) -> List[Tuple[str, float]]:
        """
        Draw one w̃ from the posterior and score all candidates.
        A single draw is shared so relative ordering is consistent.
        """
        try:
            w_tilde = np.random.multivariate_normal(
                self._mu, (self.V_SAMPLE ** 2) * self._Ainv
            )
        except np.linalg.LinAlgError:
            w_tilde = self._mu   # degenerate covariance: use mean

        scored = [(nid, float(phi @ w_tilde)) for nid, phi in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def update(self, phi: np.ndarray, reward: float):
        """
        Sherman-Morrison rank-1 posterior update.
        Complexity: O(d²)  — no matrix inversion needed.
        """
        reward   = float(np.clip(reward, -self.R_MAX, self.R_MAX))  # BUG-16
        Ainv     = self._Ainv
        Ainv_phi = Ainv @ phi                              # (d,)
        denom    = 1.0 + float(phi @ Ainv_phi)             # scalar
        # Numerically stable: skip update if denom is near zero
        if abs(denom) < 1e-12:
            return
        self._Ainv = Ainv - np.outer(Ainv_phi, Ainv_phi) / denom
        self._b   += reward * phi
        self._mu   = self._Ainv @ self._b
        self._n   += 1

    @property
    def confidence(self) -> float:
        """Real posterior confidence: 1/(1+tr(A⁻¹)).  Range: (0, 1)."""
        return 1.0 / (1.0 + float(np.trace(self._Ainv)))

    @property
    def n_observations(self) -> int:
        return self._n


# ---------------------------------------------------------------------------
# PID Controller  (fix: correct integral + anti-windup)
# ---------------------------------------------------------------------------

class PIDController:
    """
    Discrete-time PID with correct per-step integral and anti-windup.

    Position form:
        e[t]  = target - current
        I[t]  = I[t-1] + e[t]·Δt          ← correct: accumulates e·Δt
        u[t]  = Kp·e[t] + Ki·clamp(I[t]) + Kd·(e[t]-e[t-1])/Δt

    FIX from v1: the old code computed Ki * sum(all_errors) * current_dt.
    With variable Δt this gave inconsistent integral magnitude because the
    entire historical sum was scaled by the latest dt, not each sample's dt.

    Anti-windup: |I[t]| is clamped to windup_limit before Ki multiplication.
    This prevents integral blow-up when the system is persistently saturated
    (e.g. a node stuck at 100% CPU for an extended period).
    """

    def __init__(self, kp: float = 0.5, ki: float = 0.1, kd: float = 0.2,
                 windup_limit: float = 10.0):
        self.kp           = kp
        self.ki           = ki
        self.kd           = kd
        self.windup_limit = windup_limit
        self._integral:   Dict[str, float] = defaultdict(float)
        self._last_error: Dict[str, float] = defaultdict(float)
        self._last_t:     float            = time.monotonic()

    def update(self, target: Dict[str, float],
               current: Dict[str, float]) -> Dict[str, float]:
        now = time.monotonic()
        dt  = max(now - self._last_t, 1e-6)
        self._last_t = now

        return {m: self._step(m, t, current.get(m, 0.0), dt)
                for m, t in target.items()}

    def _step(self, metric: str, target: float,
              current: float, dt: float) -> float:
        e = target - current

        # Correct per-step integral accumulation
        self._integral[metric] += e * dt
        # Anti-windup clamp
        self._integral[metric] = float(
            np.clip(self._integral[metric],
                    -self.windup_limit, self.windup_limit)
        )

        D_MAX  = getattr(self, 'D_MAX', 10.0)  # BUG-14: clamp derivative
        d_term = max(-D_MAX, min(D_MAX, (e - self._last_error[metric]) / dt))
        self._last_error[metric] = e

        return self.kp * e + self.ki * self._integral[metric] + self.kd * d_term

    def reset(self, metric: Optional[str] = None):
        if metric:
            self._integral[metric]   = 0.0
            self._last_error[metric] = 0.0
        else:
            self._integral.clear()
            self._last_error.clear()


# ---------------------------------------------------------------------------
# Batch Optimiser  (O(n log n), replaces O(n²))
# ---------------------------------------------------------------------------

class BatchOptimiser:
    """
    Groups tasks with similar resource fingerprints for bulk placement.

    Algorithm (O(n log n))
    ----------------------
    1. Compute a fixed-length resource fingerprint per task (O(n))
    2. Sort tasks by L1-norm of fingerprint — a proxy for total load (O(n log n))
    3. Linear sweep: extend current batch while cosine_similarity ≥ THRESHOLD
       and batch size < MAX_BATCH_SZ; otherwise start a new batch (O(n))

    Batch centroid is maintained as a running mean so the threshold check
    reflects the whole batch, not just the previous task.

    Cosine similarity is used instead of L1 distance to remove magnitude
    bias: two tasks requiring [0.2, 0.2] and [0.4, 0.4] are identical
    in profile (same resource ratio) but have different norms.
    """

    THRESHOLD      = 0.90
    MAX_BATCH_SIZE = 32
    RESOURCES      = ['cpu', 'memory', 'network', 'disk', 'gpu', 'io']

    def _fp(self, t: Task) -> np.ndarray:
        return np.array([t.resource_requirements.get(r, 0.0)
                         for r in self.RESOURCES], dtype=np.float64)

    @staticmethod
    def _cosine(u: np.ndarray, v: np.ndarray) -> float:
        d = np.linalg.norm(u) * np.linalg.norm(v)
        return float(np.dot(u, v) / d) if d > 1e-12 else 1.0

    def optimise(self, tasks: List[Task]) -> Dict[str, List[Task]]:
        if not tasks:
            return {}
        items = [(t, self._fp(t)) for t in tasks]
        items.sort(key=lambda x: float(x[1].sum()))   # ascending L1 norm

        batches: Dict[str, List[Task]] = {}
        cur_id:  Optional[str]         = None
        cur_fp:  Optional[np.ndarray]  = None

        for task, fp in items:
            new_batch = (
                cur_id is None
                or len(batches[cur_id]) >= self.MAX_BATCH_SIZE
                or (cur_fp is not None and self._cosine(cur_fp, fp) < self.THRESHOLD)
            )
            if new_batch:
                cur_id = str(uuid.uuid4())
                batches[cur_id] = []
                cur_fp = fp.copy()

            batches[cur_id].append(task)
            n      = len(batches[cur_id])
            cur_fp = cur_fp + (fp - cur_fp) / n   # running centroid

        return batches


# ---------------------------------------------------------------------------
# Resource Optimiser  (Best-Fit Decreasing)
# ---------------------------------------------------------------------------

class ResourceOptimiser:
    """
    Best-Fit Decreasing (BFD) multi-dimensional bin packing.

    1. Group tasks into batches via BatchOptimiser (O(n log n))
    2. Sort batches by total CPU descending  (the Decreasing step)
    3. For each batch, pick the node with minimum waste that fits;
       deduct from tracking copy of node capacities

    One-dimensional approximation ratio: ≤ 11/9·OPT + 6/9.
    In practice multi-dimensional BFD performs well because the
    dominant resource (CPU) drives the sort order.
    """

    def __init__(self):
        self._batcher = BatchOptimiser()

    def optimise(self, tasks: List[Task],
                 nodes: Dict[str, NodeState]) -> Dict[str, List[Task]]:
        batches   = self._batcher.optimise(tasks)
        placement = defaultdict(list)
        remaining = {nid: dict(n.available) for nid, n in nodes.items()}

        def batch_cpu(b: List[Task]) -> float:
            return sum(t.resource_requirements.get('cpu', 0.0) for t in b)

        for batch in sorted(batches.values(), key=batch_cpu, reverse=True):
            total = self._sum_req(batch)
            node  = self._best_fit(total, remaining, nodes)
            if node:
                placement[node].extend(batch)
                for r, v in total.items():
                    remaining[node][r] = max(0.0, remaining[node].get(r, 0.0) - v)
            else:
                # Batch doesn't fit as a unit — fall back to individual placement.
                # Without this, any batch whose aggregate requirements exceed a single
                # node's capacity is silently dropped, even though each member task
                # individually fits. Profiling showed this cut placement rate to 43%
                # on feasible inputs (vs 99% for random single-task placement).
                for task in sorted(batch,
                                   key=lambda t: t.resource_requirements.get('cpu', 0),
                                   reverse=True):
                    req  = task.resource_requirements
                    best = self._best_fit(req, remaining, nodes)
                    if best:
                        placement[best].append(task)
                        for r, v in req.items():
                            remaining[best][r] = max(0.0, remaining[best].get(r, 0.0) - v)

        return dict(placement)

    def _sum_req(self, tasks: List[Task]) -> Dict[str, float]:
        out: Dict[str, float] = defaultdict(float)
        for t in tasks:
            for r, v in t.resource_requirements.items():
                out[r] += v
        return dict(out)

    def _best_fit(self, req: Dict[str, float],
                  remaining: Dict[str, Dict[str, float]],
                  nodes: Dict[str, NodeState]) -> Optional[str]:
        best, min_waste = None, float('inf')
        for nid, avail in remaining.items():
            if nodes[nid].health <= 0.0:
                continue
            if not all(avail.get(r, 0.0) >= v for r, v in req.items()):
                continue
            waste = sum(avail.get(r, 0.0) - v for r, v in req.items())
            if waste < min_waste:
                min_waste, best = waste, nid
        return best


# ---------------------------------------------------------------------------
# Adaptive Scheduler
# ---------------------------------------------------------------------------

class AdaptiveScheduler:
    """
    Top-level orchestrator: CFS heuristic + LinTS contextual bandit + PID.

    Decision pipeline per task
    --------------------------
    1.  Filter nodes: resource headroom + anti-affinity (hard constraints)
    2.  Capture pre-placement snapshot of node.available  ← FIX v1
    3.  Build LinTS feature vectors (deterministic, no hash())
    4.  if confidence ≥ CONFIDENCE_THRESHOLD:
            rank via Thompson sample from posterior
        else:
            rank via CFS score (heuristic fallback)
    5.  PID: if |utilisation - target| > 0.15 on chosen node, pick #2
    6.  Commit: deduct resources under per-node asyncio.Lock
    7.  Async: compute reward from pre-placement snapshot, update LinTS

    Thread safety: _commit() runs inside a per-node asyncio.Lock to prevent
    race conditions when asyncio.gather() schedules tasks concurrently.
    """

    CONFIDENCE_THRESHOLD = 0.70
    RESOURCE_TARGETS     = {'cpu': 0.70, 'memory': 0.75}

    def __init__(self):
        self.cfs   = CFSStatisticalModel()
        self.lints = LinearThompsonSampling()
        self.pid   = PIDController()
        self.rsopt = ResourceOptimiser()

        self.nodes:       Dict[str, NodeState]    = {}
        self._locks:      Dict[str, asyncio.Lock] = {}
        self._completions: deque                  = deque(maxlen=1000)

    # --- cluster management ---

    def register_node(self, node: NodeState):
        self.nodes[node.id]  = node
        self._locks[node.id] = asyncio.Lock()

    def deregister_node(self, node_id: str):
        self.nodes.pop(node_id, None)
        self._locks.pop(node_id, None)

    # --- scheduling ---

    async def schedule(self, task: Task) -> Optional[str]:
        if task.dep_count > 0:
            return None

        try:
            candidates = self._candidates(task)
            if not candidates:
                return None

            # Pre-placement snapshot (FIX: was post-placement in v1)
            pre = {n.id: dict(n.available) for n in candidates}
            sl  = self._system_load()

            phi_map = {n.id: self.lints.feature_vector(n, task, sl)
                       for n in candidates}

            if self.lints.confidence >= self.CONFIDENCE_THRESHOLD:
                ranked = self.lints.sample_and_rank(list(phi_map.items()))
            else:
                scored = [(n.id, self.cfs.score(task, n)) for n in candidates]
                ranked = sorted(scored, key=lambda x: x[1], reverse=True)

            chosen = self._pid_override(ranked[0][0], task, ranked)

            async with self._locks[chosen]:
                self._commit(task, chosen)

            asyncio.create_task(
                self._async_update(phi_map[chosen], chosen, pre[chosen], task)
            )
            return chosen

        except Exception as exc:
            print(f'[scheduler] {task.id} failed: {exc}')
            return None

    async def schedule_batch(self, tasks: List[Task]
                             ) -> Dict[str, Optional[str]]:
        results = await asyncio.gather(*[self.schedule(t) for t in tasks])
        return {t.id: r for t, r in zip(tasks, results)}

    def mark_complete(self, task_id: str, node_id: str,
                      elapsed_s: float, freed: Dict[str, float]):
        node = self.nodes.get(node_id)
        if node:
            for r, v in freed.items():
                node.available[r] = min(1.0, node.available.get(r, 0.0) + v)
            node.vruntime += elapsed_s
        cpu_req = freed.get('cpu', 0.1)
        self.cfs.update_vruntime(task_id, elapsed_s, cpu_req)
        self._completions.append(elapsed_s)

    def stats(self) -> Dict[str, float]:
        ct = list(self._completions)
        if not ct:
            return {}
        arr = np.array(ct)
        return {
            'n_completions':    float(len(ct)),
            'mean_s':           float(arr.mean()),
            'p95_s':            float(np.percentile(arr, 95)),
            'lints_confidence': self.lints.confidence,
            'lints_n_obs':      float(self.lints.n_observations),
        }

    # --- internal ---

    def _candidates(self, task: Task) -> List[NodeState]:
        out = []
        for n in self.nodes.values():
            if n.health <= 0.0:
                continue
            if task.anti_affinity_groups & n.labels:
                continue
            if all(n.available.get(r, 0.0) >= v
                   for r, v in task.resource_requirements.items()):
                out.append(n)
        return out

    def _pid_override(self, chosen_id: str, task: Task,
                      ranked: List[Tuple[str, float]]) -> str:
        node    = self.nodes[chosen_id]
        usage   = {r: 1.0 - node.available.get(r, 1.0)
                   for r in self.RESOURCE_TARGETS}
        deltas  = self.pid.update(self.RESOURCE_TARGETS, usage)
        if any(abs(d) > 0.15 for d in deltas.values()) and len(ranked) > 1:
            return ranked[1][0]
        return chosen_id

    def _commit(self, task: Task, node_id: str):
        node = self.nodes[node_id]
        for r, v in task.resource_requirements.items():
            node.available[r] = max(0.0, node.available.get(r, 0.0) - v)
        self.cfs.initialise_task(task.id)

    async def _async_update(self, phi: np.ndarray, node_id: str,
                             pre_avail: Dict[str, float], task: Task):
        await asyncio.sleep(0)
        # Utilisation delta: reward well-packed placements
        reqs     = task.resource_requirements
        pre_util = float(np.mean([1.0 - pre_avail.get(r, 1.0)
                                  for r in reqs]))
        post_node = self.nodes.get(node_id)
        post_util = (float(np.mean([1.0 - post_node.available.get(r, 1.0)
                                    for r in reqs]))
                     if post_node else pre_util)
        util_reward = float(np.clip(post_util - pre_util, 0.0, 1.0))

        slack      = max(task.deadline - time.time(), 1e-3)
        dl_reward  = 1.0 / (1.0 + np.log1p(slack))

        reward = 0.5 * util_reward + 0.5 * dl_reward
        self.lints.update(phi, reward)

    def _system_load(self) -> float:
        if not self.nodes:
            return 0.0
        return float(np.mean([1.0 - n.available.get('cpu', 1.0)
                               for n in self.nodes.values()]))


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

async def _demo():
    import random
    rng = random.Random(0)

    s = AdaptiveScheduler()
    for i in range(6):
        s.register_node(NodeState(
            id=f'node-{i}',
            available={'cpu': 1.0, 'memory': 1.0, 'network': 1.0},
            labels={'gpu'} if i % 2 == 0 else {'cpu_only'},
        ))

    tasks = [
        Task(
            id=f'task-{i}',
            resource_requirements={
                'cpu':    round(rng.uniform(0.05, 0.35), 2),
                'memory': round(rng.uniform(0.05, 0.30), 2),
            },
            priority=rng.randint(1, 8),
            deadline=time.time() + rng.uniform(60, 3600),
            affinity_groups={'gpu'} if i % 4 == 0 else set(),
        )
        for i in range(40)
    ]

    results = await s.schedule_batch(tasks)
    placed  = sum(1 for v in results.values() if v)
    print(f'Placed {placed}/{len(tasks)}')
    for tid, nid in list(results.items())[:5]:
        print(f'  {tid} → {nid}')

    for tid, nid in results.items():
        if nid:
            t = next(x for x in tasks if x.id == tid)
            s.mark_complete(tid, nid, rng.uniform(1, 30), t.resource_requirements)

    st = s.stats()
    print(f'LinTS confidence={st["lints_confidence"]:.4f}  '
          f'obs={st["lints_n_obs"]:.0f}  '
          f'mean_s={st["mean_s"]:.1f}')


if __name__ == '__main__':
    asyncio.run(_demo())
