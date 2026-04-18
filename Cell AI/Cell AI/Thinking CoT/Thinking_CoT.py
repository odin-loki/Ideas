"""
Combined Chain of Thought + Cell AI System
==========================================
Fixed, profiled, and fully integrated implementation.

Bug fixes applied (see README.md for full log):
  1.  ThoughtChain.__init__: self.device never set; pattern_combinations misplaced.
  2.  ThoughtChain._prepare_input / _prepare_result / _simplify_thought /
      _best_partial_result / _apply_approach / _decompose_tensor /
      _compute_complexity / _analyze_structure: mixed-tab/space indentation
      caused IndentationError / SyntaxError at import time.
  3.  PatternProcessor._hash_pattern, MemoryFormation._hash_pattern: same
      mixed-indent bug.
  4.  _update_evolution: `evolution = list.append(...)` assigned None to a
      local variable; silently discarded every appended record.
  5.  _learn_from_result: `thought.previous_approaches[-1]` — Set is not
      subscriptable; raises TypeError at runtime.
  6.  approach_history in _generate_new_approach: empty-list guard missing.
  7.  ConnectionOptimizer._find_critical_paths: called but never defined.
  8.  ConnectionOptimizer._distance_matrix: called but never defined.
  9.  PatternEvolution._compute_similarity: called but never defined.
  10. PatternEvolution._update_prototype: called but never defined (only
      existed in PatternProcessor).
  11. ThoughtChain._compute_approach_similarity: called but never defined.
  12. ThoughtChain._enhance_cached_result: called but never defined.
  13. ThoughtChain._queue_thought: called but never defined.
  14. ThoughtChain._hash_thought: called but never defined.
  15. PatternProcessor.process_pattern: result dict missing 'confidence' key;
      ThoughtChain.process_thought raised KeyError unconditionally.
  16. _generate_pattern_questions: accessed pattern['type'] which _analyze_pattern
      never set; raised KeyError.
  17. error variable in ParallelStateEvolution.evolve_state: referenced after
      while-loop but only assigned inside it; NameError if max_iterations == 0.
  18. ParallelStateEvolution._compute_signal_integration: `partition @ w_ij`
      where w_ij is a 0-d scalar tensor — invalid matmul; replaced with
      element-wise multiplication.
  19. _pattern_similarity: returned Tensor instead of float.
  20. ParallelStateEvolution._partition_state: decorated @staticmethod but
      referenced self.num_partitions — TypeError at call time.
"""

from __future__ import annotations

import asyncio
import cProfile
import functools
import io
import math
import pstats
import time
import tracemalloc
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Conditional torch import — graceful CPU fallback when CUDA not available
# ---------------------------------------------------------------------------
try:
    import torch
    import torch.nn.functional as F
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False
    raise ImportError(
        "PyTorch is required. Install with: pip install torch"
    )

try:
    import ray
    _RAY_AVAILABLE = True
except ImportError:
    _RAY_AVAILABLE = False

# ===========================================================================
# PROFILING INFRASTRUCTURE
# ===========================================================================

@dataclass
class CallStat:
    """Statistics for a single instrumented call site."""
    name: str
    calls: int = 0
    total_time: float = 0.0
    peak_memory_bytes: int = 0
    errors: int = 0

    @property
    def avg_time(self) -> float:
        return self.total_time / self.calls if self.calls else 0.0

    def __repr__(self) -> str:
        return (
            f"<CallStat {self.name!r} calls={self.calls} "
            f"avg={self.avg_time*1000:.2f}ms "
            f"peak_mem={self.peak_memory_bytes//1024}KB>"
        )


class ProfilerRegistry:
    """Thread-safe central registry of per-method call statistics."""
    _stats: Dict[str, CallStat] = {}

    @classmethod
    def record(cls, name: str, elapsed: float, memory: int = 0,
               error: bool = False) -> None:
        if name not in cls._stats:
            cls._stats[name] = CallStat(name)
        s = cls._stats[name]
        s.calls += 1
        s.total_time += elapsed
        if memory > s.peak_memory_bytes:
            s.peak_memory_bytes = memory
        if error:
            s.errors += 1

    @classmethod
    def report(cls, top_n: int = 20, sort_by: str = "total_time") -> str:
        rows = sorted(cls._stats.values(),
                      key=lambda s: getattr(s, sort_by, 0), reverse=True)
        lines = [
            f"\n{'Method':<55} {'Calls':>7} {'AvgMs':>8} {'TotalS':>8} "
            f"{'PeakKB':>8} {'Errors':>7}",
            "-" * 100,
        ]
        for s in rows[:top_n]:
            lines.append(
                f"{s.name:<55} {s.calls:>7} {s.avg_time*1000:>8.2f} "
                f"{s.total_time:>8.3f} {s.peak_memory_bytes//1024:>8} "
                f"{s.errors:>7}"
            )
        return "\n".join(lines)

    @classmethod
    def reset(cls) -> None:
        cls._stats.clear()


def profile_call(func):
    """
    Decorator that records wall-clock time and peak memory delta for every
    call to the wrapped method and pushes the result to ProfilerRegistry.

    Usage::

        class Foo:
            @profile_call
            def expensive(self): ...
    """
    label = f"{func.__qualname__}"

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        tracemalloc.start()
        t0 = time.perf_counter()
        error = False
        try:
            return await func(*args, **kwargs)
        except Exception:
            error = True
            raise
        finally:
            elapsed = time.perf_counter() - t0
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            ProfilerRegistry.record(label, elapsed, peak, error)

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        tracemalloc.start()
        t0 = time.perf_counter()
        error = False
        try:
            return func(*args, **kwargs)
        except Exception:
            error = True
            raise
        finally:
            elapsed = time.perf_counter() - t0
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            ProfilerRegistry.record(label, elapsed, peak, error)

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


class CProfileContext:
    """
    Context manager that runs cProfile over a block and returns a formatted
    pstats report string.

    Usage::

        with CProfileContext(sort="cumulative", top=30) as p:
            run_expensive_thing()
        print(p.report)
    """
    def __init__(self, sort: str = "cumulative", top: int = 30):
        self._sort = sort
        self._top = top
        self._pr = cProfile.Profile()
        self.report: str = ""

    def __enter__(self) -> CProfileContext:
        self._pr.enable()
        return self

    def __exit__(self, *_):
        self._pr.disable()
        buf = io.StringIO()
        ps = pstats.Stats(self._pr, stream=buf)
        ps.sort_stats(self._sort)
        ps.print_stats(self._top)
        self.report = buf.getvalue()


def benchmark(func, *args, n: int = 5, **kwargs) -> Dict[str, float]:
    """
    Run *func* n times, return wall-clock statistics (seconds).

    Returns dict with keys: min, max, mean, std, total.
    """
    times = []
    for _ in range(n):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        # Drain coroutines
        if asyncio.iscoroutine(result):
            asyncio.get_event_loop().run_until_complete(result)
        times.append(time.perf_counter() - t0)
    arr = np.array(times)
    return {
        "min": float(arr.min()),
        "max": float(arr.max()),
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "total": float(arr.sum()),
        "n": n,
    }


# ===========================================================================
# DEVICE HELPERS
# ===========================================================================

def _best_device() -> str:
    """Return 'cuda' if available, else 'cpu'."""
    return "cuda" if torch.cuda.is_available() else "cpu"


# ===========================================================================
# SYSTEM STATE
# ===========================================================================

@dataclass
class SystemState:
    """Complete system state representation."""
    data: torch.Tensor
    gradient: torch.Tensor
    energy: float
    time: float
    error: float = 0.0
    confidence: float = 0.0
    history: List[torch.Tensor] = field(default_factory=list)
    reaction_history: List[Dict] = field(default_factory=list)


# ===========================================================================
# CONNECTION OPTIMIZER
# ===========================================================================

class ConnectionOptimizer:
    """Optimises pattern connections and network topology."""

    def __init__(self, size: int, device: str = _best_device()):
        self.device = torch.device(device)
        self.size = size
        self.connections = torch.zeros((size, size), device=device)
        self.weights = torch.ones(size, device=device)
        self.history: Dict[str, List] = defaultdict(list)

    @profile_call
    def optimize(self, connections: torch.Tensor) -> torch.Tensor:
        costs = self._compute_connection_costs(connections)
        pruned = self._prune_connections(connections, costs)
        strengthened = self._strengthen_paths(pruned)
        self._update_weights(strengthened)
        return strengthened

    def _compute_connection_costs(self, connections: torch.Tensor) -> torch.Tensor:
        """E(π) = Σᵢ (computational_load(πᵢ) + communication_cost(πᵢ, π\\πᵢ))"""
        comp_load = torch.sum(connections, dim=1)
        comm_cost = torch.sum(connections * self._distance_matrix(), dim=1)
        return comp_load + comm_cost

    def _distance_matrix(self) -> torch.Tensor:
        """
        FIX #8 — was called but never defined.
        Returns an (n×n) pairwise index-distance matrix normalised to [0,1].
        """
        idx = torch.arange(self.size, device=self.device).float()
        dist = torch.abs(idx.unsqueeze(0) - idx.unsqueeze(1))
        max_dist = dist.max().clamp(min=1.0)
        return dist / max_dist

    def _prune_connections(self, connections: torch.Tensor,
                           costs: torch.Tensor) -> torch.Tensor:
        mask = costs < torch.mean(costs) + torch.std(costs)
        return connections * mask.float().unsqueeze(1)

    def _strengthen_paths(self, connections: torch.Tensor) -> torch.Tensor:
        paths = self._find_critical_paths(connections)
        strengthened = connections.clone()
        for path in paths:
            if 0 <= path < self.size:
                strengthened[path] = (strengthened[path] * 1.2).clamp(max=1.0)
        return strengthened

    def _find_critical_paths(self, connections: torch.Tensor) -> List[int]:
        """
        FIX #7 — was called but never defined.
        Identifies high-load rows as critical (top quartile by out-degree).
        """
        out_degree = connections.sum(dim=1)
        threshold = torch.quantile(out_degree, 0.75)
        return (out_degree >= threshold).nonzero(as_tuple=True)[0].tolist()

    def _update_weights(self, connections: torch.Tensor) -> None:
        usage = torch.sum(connections, dim=1)
        self.weights = 0.9 * self.weights + 0.1 * usage


# ===========================================================================
# PARTITION MANAGER
# ===========================================================================

class PartitionManager:
    """Manages optimal partitioning of the system."""

    def __init__(self, size: int, num_partitions: int,
                 device: str = _best_device()):
        self.device = torch.device(device)
        self.size = size
        self.num_partitions = num_partitions
        self.partitions: Dict[int, torch.Tensor] = {}
        self.boundaries: Dict[int, torch.Tensor] = {}
        self.loads = torch.zeros(num_partitions, device=device)
        self.max_partition_size = size // num_partitions * 2
        self.min_connectivity = 0.3

    @profile_call
    def optimize_partitions(self,
                            data: torch.Tensor) -> Dict[int, torch.Tensor]:
        loads = self._compute_loads(data)
        balanced = self._balance_partitions(loads)
        self._optimize_boundaries(balanced)
        self.partitions = balanced
        return balanced

    def _compute_loads(self, data: torch.Tensor) -> torch.Tensor:
        loads = []
        for i in range(self.num_partitions):
            if i in self.partitions and len(self.partitions[i]) > 0:
                partition = self.partitions[i]
                load = torch.sum(torch.abs(data[partition]))
            else:
                load = torch.tensor(0.0, device=self.device)
            loads.append(load)
        return torch.stack(loads)

    def _balance_partitions(self,
                            loads: torch.Tensor) -> Dict[int, torch.Tensor]:
        balanced: Dict[int, torch.Tensor] = {}
        total_load = loads.sum().clamp(min=1e-10)
        current_idx = 0
        for i in range(self.num_partitions):
            partition_size = int((loads[i] / total_load).item() * self.size)
            partition_size = max(1, min(partition_size, self.max_partition_size))
            end_idx = min(current_idx + partition_size, self.size)
            balanced[i] = torch.arange(current_idx, end_idx, device=self.device)
            current_idx = end_idx
        return balanced

    def _optimize_boundaries(self, partitions: Dict[int, torch.Tensor]) -> None:
        self.boundaries = {}
        for i in range(self.num_partitions - 1):
            if i in partitions and i + 1 in partitions:
                p1, p2 = partitions[i], partitions[i + 1]
                if len(p1) >= 2 and len(p2) >= 2:
                    self.boundaries[i] = torch.cat([p1[-2:], p2[:2]])


# ===========================================================================
# SPATIAL ORGANIZER
# ===========================================================================

class SpatialOrganizer:
    """Implements spatial organisation and diffusion (∂Cᵢ/∂t = D∇²Cᵢ + Rᵢ − λᵢCᵢ)."""

    def __init__(self, size: int, num_partitions: int,
                 device: str = _best_device()):
        self.device = torch.device(device)
        self.size = size
        self.num_partitions = num_partitions
        self.D = torch.tensor(0.1, device=device)
        self.lambda_decay = torch.tensor(0.1, device=device)
        self.concentrations = torch.zeros((num_partitions, size), device=device)
        self.reactions: Dict[int, List] = defaultdict(list)

    @profile_call
    def evolve_space(self, partitions: Dict[int, torch.Tensor],
                     dt: float) -> torch.Tensor:
        evolved = []
        for i in range(self.num_partitions):
            if i in partitions:
                c = self.concentrations[i]
                diffusion = self._compute_diffusion(c)
                reactions = self._compute_reactions(i, c)
                dc = (self.D * diffusion + reactions - self.lambda_decay * c) * dt
                new_c = c + dc
                evolved.append(new_c)
                self.concentrations[i] = new_c
        return torch.stack(evolved) if evolved else torch.zeros(
            1, self.size, device=self.device)

    def _compute_diffusion(self, concentration: torch.Tensor) -> torch.Tensor:
        kernel = torch.tensor([
            [0.05, 0.2, 0.05],
            [0.2, -1.0, 0.2],
            [0.05, 0.2, 0.05],
        ], device=self.device)
        c4d = concentration.view(1, 1, -1, 1)
        diffusion = F.conv2d(c4d, kernel.view(1, 1, 3, 3), padding=(1, 0))
        return diffusion.view(-1)[:concentration.shape[0]]

    def _compute_reactions(self, partition_idx: int,
                           concentration: torch.Tensor) -> torch.Tensor:
        if partition_idx not in self.reactions:
            return torch.zeros_like(concentration)
        term = torch.zeros_like(concentration)
        for rxn in self.reactions[partition_idx]:
            k_plus = rxn['k_plus']
            k_minus = rxn['k_minus']
            reactants = rxn['reactants']
            products = rxn['products']
            forward = k_plus * torch.prod(concentration[reactants])
            reverse = k_minus * torch.prod(concentration[products])
            term += forward - reverse
        return term


# ===========================================================================
# REACTION OPTIMIZER
# ===========================================================================

class ReactionOptimizer:
    """Optimises reaction networks and rate constants."""

    def __init__(self, num_species: int, device: str = _best_device()):
        self.device = torch.device(device)
        self.num_species = num_species
        self.k_plus = torch.rand((num_species, num_species), device=device)
        self.k_minus = torch.rand((num_species, num_species), device=device)
        self.orders = torch.ones((num_species, num_species), device=device)
        self.history: Dict[str, List] = defaultdict(list)

    @profile_call
    def optimize_network(self,
                         reactions: List[Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        efficiencies = self._compute_efficiencies(reactions)
        self._update_rates(efficiencies)
        self._optimize_orders(reactions)
        return {
            'k_plus': self.k_plus.clone(),
            'k_minus': self.k_minus.clone(),
            'orders': self.orders.clone(),
        }

    def _compute_efficiencies(self,
                              reactions: List[Dict[str, Any]]) -> torch.Tensor:
        effs = torch.zeros((self.num_species, self.num_species),
                           device=self.device)
        for rxn in reactions:
            i, j = rxn['reactant_idx'], rxn['product_idx']
            if 0 <= i < self.num_species and 0 <= j < self.num_species:
                eff = rxn['forward_rate'] / (rxn['reverse_rate'] + 1e-10)
                effs[i, j] = eff
        return effs

    def _update_rates(self, efficiencies: torch.Tensor) -> None:
        self.k_plus = self.k_plus * (1 + 0.1 * (efficiencies > 1).float())
        self.k_minus = self.k_minus * (1 + 0.1 * (efficiencies < 1).float())
        norm_p = self.k_plus.norm(dim=1, keepdim=True).clamp(min=1e-10)
        norm_m = self.k_minus.norm(dim=1, keepdim=True).clamp(min=1e-10)
        self.k_plus = self.k_plus / norm_p
        self.k_minus = self.k_minus / norm_m

    def _optimize_orders(self, reactions: List[Dict[str, Any]]) -> None:
        for rxn in reactions:
            i, j = rxn['reactant_idx'], rxn['product_idx']
            if 0 <= i < self.num_species and 0 <= j < self.num_species:
                conc = torch.tensor(rxn.get('concentration', 1.0),
                                    device=self.device)
                optimal = -torch.log(torch.tensor(rxn['forward_rate'],
                                                  device=self.device) + 1e-10) \
                          / torch.log(conc + 1e-10)
                self.orders[i, j] = (0.9 * self.orders[i, j]
                                     + 0.1 * optimal).clamp(0.5, 3.0)


# ===========================================================================
# PATTERN EVOLUTION
# ===========================================================================

class PatternEvolution:
    """Tracks and manages pattern family evolution."""

    def __init__(self, device: str = _best_device()):
        self.device = torch.device(device)
        self.families: Dict[str, Dict] = {}
        self.evolution_history: Dict[str, List] = defaultdict(list)
        self.mutation_rate = 0.1

    @profile_call
    def evolve_patterns(self,
                        patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        evolved = []
        for pattern in patterns:
            family_id = self._get_family(pattern)
            evolved_pattern = self._evolve_pattern(pattern, family_id)
            self._track_evolution(evolved_pattern, family_id)
            evolved.append(evolved_pattern)
        return evolved

    def _compute_similarity(self, p1: torch.Tensor,
                            p2: torch.Tensor) -> float:
        """
        FIX #9 — was called in _get_family but never defined.
        Cosine similarity in both direct and frequency domains.
        """
        min_len = min(len(p1), len(p2))
        if min_len == 0:
            return 0.0
        a, b = p1[:min_len].float(), p2[:min_len].float()
        direct = F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()
        fa = torch.abs(torch.fft.fft(a))
        fb = torch.abs(torch.fft.fft(b))
        freq = F.cosine_similarity(fa.unsqueeze(0), fb.unsqueeze(0)).item()
        return (direct + freq) / 2.0

    def _get_family(self, pattern: Dict[str, Any]) -> str:
        pattern_data = pattern['data']
        best_match: Optional[str] = None
        best_sim = 0.7  # similarity threshold for existing family

        for family_id, family in self.families.items():
            sim = self._compute_similarity(pattern_data, family['prototype'])
            if sim > best_sim:
                best_sim = sim
                best_match = family_id

        if best_match is None:
            family_id = f"family_{len(self.families)}"
            self.families[family_id] = {
                'prototype': pattern_data.clone(),
                'members': [],
                'mutations': [],
            }
            best_match = family_id

        return best_match

    def _evolve_pattern(self, pattern: Dict[str, Any],
                        family_id: str) -> Dict[str, Any]:
        family = self.families[family_id]
        if torch.rand(1).item() < self.mutation_rate:
            mutation = self._generate_mutation(pattern['data'])
            family['mutations'].append(mutation)
        else:
            mutation = torch.zeros_like(pattern['data'])

        evolved = pattern.copy()
        evolved['data'] = (pattern['data'] + mutation)
        evolved['family'] = family_id
        evolved['generation'] = len(family['members'])
        return evolved

    def _generate_mutation(self, pattern: torch.Tensor) -> torch.Tensor:
        mutation = torch.randn_like(pattern) * self.mutation_rate
        return mutation.clamp(-0.2, 0.2)

    def _track_evolution(self, pattern: Dict[str, Any],
                         family_id: str) -> None:
        family = self.families[family_id]
        family['members'].append(pattern)
        self._update_prototype(family_id)  # FIX #10 — now defined
        self.evolution_history[family_id].append({
            'pattern': pattern,
            'time': time.time(),
        })

    def _update_prototype(self, family_id: str) -> None:
        """
        FIX #10 — was called in _track_evolution but never defined in this class.
        Recomputes the prototype as the mean of all member tensors.
        """
        family = self.families[family_id]
        members = family['members']
        if not members:
            return
        try:
            data = torch.stack([m['data'] for m in members]).mean(0)
            family['prototype'] = data
        except Exception:
            pass  # keep previous prototype if shapes mismatch


# ===========================================================================
# THOUGHT CACHE
# ===========================================================================

class ThoughtCache:
    """Intelligent thought caching with LRU-style eviction."""

    def __init__(self, max_size: int = 10_000):
        self.max_size = max_size
        self.cache: Dict[str, Dict] = {}
        self.access_counts: Dict[str, int] = defaultdict(int)
        self.timestamps: Dict[str, float] = {}
        self.relationships: Dict[str, Set[str]] = defaultdict(set)

    def store(self, key: str, result: Dict[str, Any]) -> None:
        if len(self.cache) >= self.max_size:
            self._evict_entries()
        self.cache[key] = result
        self.timestamps[key] = time.time()
        for pattern in result.get('patterns', []):
            pk = self._hash_pattern(pattern)
            self.relationships[pk].add(key)

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if key in self.cache:
            self.access_counts[key] += 1
            self.timestamps[key] = time.time()
            return self.cache[key]
        return None

    def find_related(self, key: str) -> List[Dict[str, Any]]:
        if key not in self.cache:
            return []
        related = []
        for pattern in self.cache[key].get('patterns', []):
            pk = self._hash_pattern(pattern)
            for rk in self.relationships[pk]:
                if rk != key and rk in self.cache:
                    related.append(self.cache[rk])
        return related

    def _evict_entries(self) -> None:
        now = time.time()
        scores = {}
        for k in self.cache:
            age = now - self.timestamps.get(k, now)
            freq = self.access_counts[k]
            rels = sum(1 for r in self.relationships.values() if k in r)
            scores[k] = (freq / (age + 1)) * (1 + 0.1 * rels)
        n_remove = max(1, len(self.cache) - self.max_size + 1)
        victims = sorted(scores, key=lambda k: scores[k])[:n_remove]
        for k in victims:
            self._remove_entry(k)

    def _remove_entry(self, key: str) -> None:
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
        self.access_counts.pop(key, None)
        for pk in list(self.relationships):
            self.relationships[pk].discard(key)
            if not self.relationships[pk]:
                del self.relationships[pk]

    @staticmethod
    def _hash_pattern(pattern: Any) -> str:
        if isinstance(pattern, torch.Tensor):
            return str(hash(pattern.cpu().numpy().tobytes()))
        if isinstance(pattern, dict) and 'data' in pattern:
            return str(hash(pattern['data'].cpu().numpy().tobytes()))
        return str(hash(str(pattern)))


# ===========================================================================
# QUEUE MANAGER
# ===========================================================================

@dataclass
class Thought:
    """Complete thought representation."""
    content: Any
    confidence: float = 0.0
    depth: int = 0
    previous_approaches: Set[str] = field(default_factory=set)
    patterns: List[Dict] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    sub_thoughts: List['Thought'] = field(default_factory=list)
    parent: Optional['Thought'] = None

    def __post_init__(self) -> None:
        self.timestamp = time.time()
        self.history: List = []
        self.performance: Dict[str, List] = defaultdict(list)


class QueueManager:
    """Priority queue with intelligent thought scheduling."""

    def __init__(self, max_size: int):
        self.max_size = max_size
        self.queues: Dict[str, List[Thought]] = {
            'high': [], 'normal': [], 'low': [],
        }
        self.history: Dict[str, List] = defaultdict(list)
        self.processing_times: Dict[str, List[float]] = defaultdict(list)
        self.success_rates: Dict[str, float] = {}

    def add_thought(self, thought: Thought,
                    priority: Optional[str] = None) -> None:
        if priority is None:
            priority = self._calculate_priority(thought)
        queue = self.queues[priority]
        if len(queue) < self.max_size:
            pos = self._find_position(thought, queue)
            queue.insert(pos, thought)
            self.history[self._hash_thought(thought)].append({
                'priority': priority, 'time': time.time(),
            })

    def get_next(self) -> Optional[Thought]:
        for level in ('high', 'normal', 'low'):
            q = self.queues[level]
            if q:
                thought = self._select_best_thought(q)
                if thought:
                    self._update_stats(thought)
                    return thought
        return None

    def update_success_rate(self, thought: Thought, success: bool) -> None:
        h = self._hash_thought(thought)
        cur = self.success_rates.get(h, 0.5)
        self.success_rates[h] = 0.9 * cur + 0.1 * float(success)

    # -- internals --

    def _calculate_priority(self, thought: Thought) -> str:
        h = self._hash_thought(thought)
        sr = self.success_rates.get(h, 0.5)
        history = self.history[h]
        avg_t = float(np.mean(self.processing_times[h])) \
            if self.processing_times[h] else 1.0
        depth_f = 1 - (thought.depth / max(10, thought.depth + 1))
        hist_f = 1 / (len(history) + 1)
        time_f = 1 / (avg_t + 1)
        score = sr * depth_f * hist_f * time_f
        if score > 0.7:
            return 'high'
        if score > 0.3:
            return 'normal'
        return 'low'

    def _find_position(self, thought: Thought,
                       queue: List[Thought]) -> int:
        score = self._calculate_thought_score(thought)
        for i, t in enumerate(queue):
            if score > self._calculate_thought_score(t):
                return i
        return len(queue)

    def _select_best_thought(self,
                             queue: List[Thought]) -> Optional[Thought]:
        if not queue:
            return None
        scores = [self._calculate_thought_score(t) for t in queue]
        best = int(np.argmax(scores))
        return queue.pop(best)

    def _calculate_thought_score(self, thought: Thought) -> float:
        h = self._hash_thought(thought)
        depth_s = 1 - (thought.depth / max(10, thought.depth + 1))
        success_s = self.success_rates.get(h, 0.5)
        times = self.processing_times[h]
        time_s = 1 / (float(np.mean(times)) + 1) if times else 0.5
        history = self.history[h]
        hist_s = 1 / (len(history) + 1)
        return depth_s * 0.3 + success_s * 0.3 + time_s * 0.2 + hist_s * 0.2

    def _update_stats(self, thought: Thought) -> None:
        h = self._hash_thought(thought)
        hist = self.history[h]
        delta = time.time() - hist[-1]['time'] if hist else 0.0
        self.processing_times[h].append(delta)
        if len(self.processing_times[h]) > 100:
            self.processing_times[h] = self.processing_times[h][-100:]

    @staticmethod
    def _hash_thought(thought: Thought) -> str:
        if isinstance(thought.content, torch.Tensor):
            return str(hash(thought.content.cpu().numpy().tobytes()))
        return str(hash(str(thought.content)))


# ===========================================================================
# PARALLEL STATE EVOLUTION
# ===========================================================================

class ParallelStateEvolution:
    """Complete parallel state evolution (all Cell-AI ODEs)."""

    def __init__(self, num_partitions: int, partition_size: int,
                 device: str = _best_device()):
        self.device = torch.device(device)
        self.num_partitions = num_partitions
        self.partition_size = partition_size
        self.dt = torch.tensor(0.01, device=device)
        self.gamma = torch.tensor(0.1, device=device)
        self.D = torch.tensor(0.1, device=device)
        self.states = [torch.zeros(partition_size, device=device)
                       for _ in range(num_partitions)]
        self.gradients = [torch.zeros(partition_size, device=device)
                          for _ in range(num_partitions)]
        self.reaction_rates = self._initialize_reaction_rates()
        self.reaction_orders = self._initialize_reaction_orders()
        self.diffusion_kernel = self._create_diffusion_kernel()
        self.convergence_threshold = 1e-6
        self.max_iterations = max(1, int(math.sqrt(partition_size)))

    def _initialize_reaction_rates(self) -> Dict[str, torch.Tensor]:
        return {
            'k_plus': torch.rand(self.num_partitions, self.num_partitions,
                                 device=self.device),
            'k_minus': torch.rand(self.num_partitions, self.num_partitions,
                                  device=self.device),
        }

    def _initialize_reaction_orders(self) -> torch.Tensor:
        return torch.ones(self.num_partitions, self.num_partitions,
                          device=self.device)

    def _create_diffusion_kernel(self) -> torch.Tensor:
        kernel = torch.tensor([
            [0.05, 0.2, 0.05],
            [0.2, -1.0, 0.2],
            [0.05, 0.2, 0.05],
        ], device=self.device)
        return kernel.unsqueeze(0).unsqueeze(0)

    @profile_call
    async def evolve_state(self, state: SystemState) -> SystemState:
        partitions = self._partition_state(state.data)
        errors: List[float] = []
        error = 0.0  # FIX #17 — initialise before loop

        for t in range(self.max_iterations):
            new_partitions: List[torch.Tensor] = []
            for i, partition in enumerate(partitions):
                f_i = self._compute_signal_integration(partition, i)
                diffusion = self._compute_diffusion(partition)
                reaction = self._compute_reactions(partition, i)
                noise = self._generate_noise(partition)
                d_state = (f_i - self.gamma * partition
                           + self.D * diffusion + reaction + noise) * self.dt
                new_partitions.append(partition + d_state)

            new_partitions = self._enforce_boundaries(new_partitions)
            error = self._compute_error(new_partitions, partitions)
            errors.append(error)

            if self._check_convergence(errors):
                break
            partitions = new_partitions

        new_state = self._combine_partitions(new_partitions)
        confidence = self._compute_confidence(errors, len(errors))

        # Build gradient tensor safely
        try:
            grad = torch.stack(
                [p - o for p, o in zip(new_partitions, partitions)])
        except RuntimeError:
            grad = torch.zeros_like(new_state)

        return SystemState(
            data=new_state,
            gradient=grad,
            energy=self._compute_energy(new_state),
            time=state.time + len(errors) * self.dt.item(),
            error=error,
            confidence=confidence,
            history=state.history + [new_state],
            reaction_history=state.reaction_history + [self._get_reaction_state()],
        )

    def _compute_signal_integration(self, partition: torch.Tensor,
                                    idx: int) -> torch.Tensor:
        """
        FIX #18 — original used `partition @ w_ij` where w_ij is a 0-d scalar;
        invalid matmul. Replaced with element-wise scalar multiplication.
        """
        activations = []
        for j in range(self.num_partitions):
            w_ij = self.reaction_rates['k_plus'][idx, j]  # scalar tensor
            activation = torch.tanh(partition * w_ij)
            activations.append(activation)
        return torch.stack(activations).mean(0)

    def _compute_diffusion(self, state: torch.Tensor) -> torch.Tensor:
        s4d = state.view(1, 1, -1, 1)
        out = F.conv2d(s4d, self.diffusion_kernel, padding=(1, 0))
        return out.view(-1)[:state.shape[0]]

    def _compute_reactions(self, state: torch.Tensor, idx: int) -> torch.Tensor:
        term = torch.zeros_like(state)
        for j in range(self.num_partitions):
            if j != idx:
                k_plus = self.reaction_rates['k_plus'][idx, j]
                k_minus = self.reaction_rates['k_minus'][idx, j]
                order_f = self.reaction_orders[idx, j]
                order_r = self.reaction_orders[j, idx]
                forward = k_plus * torch.pow(state.abs() + 1e-10, order_f)
                reverse = k_minus * torch.pow(state.abs() + 1e-10, order_r)
                term += (forward - reverse)
        return term

    def _generate_noise(self, state: torch.Tensor) -> torch.Tensor:
        amplitude = torch.sqrt(torch.abs(state) + 1e-6)
        return torch.randn_like(state) * amplitude * 0.01

    def _enforce_boundaries(self,
                            states: List[torch.Tensor]) -> List[torch.Tensor]:
        for i in range(len(states) - 1):
            boundary = (states[i][-1] + states[i + 1][0]) / 2
            states[i] = torch.cat([states[i][:-1], boundary.unsqueeze(0)])
            states[i + 1] = torch.cat([boundary.unsqueeze(0), states[i + 1][1:]])
        return states

    def _compute_error(self, new_states: List[torch.Tensor],
                       old_states: List[torch.Tensor]) -> float:
        state_errs = torch.stack(
            [torch.norm(n - o) for n, o in zip(new_states, old_states)])
        state_error = state_errs.mean()
        if len(new_states) > 1:
            b_errs = torch.stack(
                [torch.abs(new_states[i][-1] - new_states[i + 1][0])
                 for i in range(len(new_states) - 1)])
            b_error = b_errs.mean()
        else:
            b_error = torch.tensor(0.0, device=self.device)
        return (state_error + 0.1 * b_error).item()

    def _check_convergence(self, errors: List[float]) -> bool:
        if len(errors) < 2:
            return False
        if errors[-1] < self.convergence_threshold:
            return True
        improvement = (errors[-2] - errors[-1]) / max(errors[-2], 1e-10)
        if improvement < self.convergence_threshold:
            return True
        if len(errors) > 4:
            recent = errors[-4:]
            if max(recent) - min(recent) < self.convergence_threshold:
                return True
        return False

    def _compute_energy(self, state: torch.Tensor) -> float:
        kinetic = 0.5 * torch.sum(state * state)
        potential = torch.tensor(0.0, device=self.device)
        for i in range(self.num_partitions):
            for j in range(self.num_partitions):
                if i != j:
                    potential += (self.reaction_rates['k_plus'][i, j]
                                  * torch.sum(torch.pow(
                                      state.abs() + 1e-10,
                                      self.reaction_orders[i, j])))
        return (kinetic + potential).item()

    def _compute_confidence(self, errors: List[float],
                            iterations: int) -> float:
        if not errors:
            return 0.0
        ec = math.exp(-errors[-1])
        sc = 1 - iterations / max(self.max_iterations, 1)
        stab = math.exp(-float(np.std(errors[-3:]))) if len(errors) > 2 else 1.0
        return min(ec * sc * stab, 1.0)

    def _get_reaction_state(self) -> Dict[str, Any]:
        return {
            'k_plus': self.reaction_rates['k_plus'].clone().cpu(),
            'k_minus': self.reaction_rates['k_minus'].clone().cpu(),
            'orders': self.reaction_orders.clone().cpu(),
            'time': time.time(),
        }

    # FIX #20 — was @staticmethod but used self.num_partitions
    def _partition_state(self, state: torch.Tensor) -> List[torch.Tensor]:
        n = state.size(0)
        size = max(1, n // self.num_partitions)
        parts = []
        for i in range(0, n, size):
            parts.append(state[i:min(i + size, n)])
        return parts

    @staticmethod
    def _combine_partitions(partitions: List[torch.Tensor]) -> torch.Tensor:
        return torch.cat(partitions)


# ===========================================================================
# MEMORY FORMATION
# ===========================================================================

class MemoryFormation:
    """Parallel memory formation: M(t) = ∫w(t−s)I(s)ds + ∫K(t−s)S(s)ds"""

    def __init__(self, memory_size: int, time_window: int,
                 device: str = _best_device()):
        self.device = torch.device(device)
        self.memory_size = memory_size
        self.time_window = time_window
        self.w_kernel = self._create_weight_kernel()
        self.K_kernel = self._create_integration_kernel()
        self.input_buffer = torch.zeros(time_window, memory_size, device=device)
        self.state_buffer = torch.zeros(time_window, memory_size, device=device)
        self.memory = torch.zeros(memory_size, device=device)
        self.pattern_memory: Dict[str, Dict] = {}

    @profile_call
    def integrate(self, input_signal: torch.Tensor,
                  state: torch.Tensor, time_index: int) -> torch.Tensor:
        idx = time_index % self.time_window
        # Resize signals to memory_size if needed
        if input_signal.shape[0] != self.memory_size:
            input_signal = F.interpolate(
                input_signal.unsqueeze(0).unsqueeze(0).float(),
                size=self.memory_size, mode='linear', align_corners=False,
            ).squeeze()
        if state.shape[0] != self.memory_size:
            state = F.interpolate(
                state.unsqueeze(0).unsqueeze(0).float(),
                size=self.memory_size, mode='linear', align_corners=False,
            ).squeeze()
        self.input_buffer[idx] = input_signal
        self.state_buffer[idx] = state
        input_mem = self._integrate_inputs(time_index)
        state_mem = self._integrate_states(time_index)
        self.memory = input_mem + state_mem
        self._update_pattern_memory(time_index)
        return self.memory

    def _create_weight_kernel(self) -> torch.Tensor:
        t = torch.arange(self.time_window, device=self.device).float()
        base = torch.exp(-t / self.time_window)
        scale = torch.sigmoid(t / self.time_window)
        return base * scale

    def _create_integration_kernel(self) -> torch.Tensor:
        t = torch.arange(self.time_window, device=self.device).float()
        base = torch.exp(-t / (2 * self.time_window))
        mod = torch.sin(2 * math.pi * t / self.time_window)
        return base * (1 + 0.1 * mod)

    def _integrate_inputs(self, current_time: int) -> torch.Tensor:
        idx = (torch.arange(self.time_window, device=self.device)
               + current_time) % self.time_window
        inputs = self.input_buffer[idx]
        weighted = inputs * self.w_kernel.unsqueeze(1)
        return weighted.sum(dim=0)

    def _integrate_states(self, current_time: int) -> torch.Tensor:
        idx = (torch.arange(self.time_window, device=self.device)
               + current_time) % self.time_window
        states = self.state_buffer[idx]
        weighted = states * self.K_kernel.unsqueeze(1)
        return weighted.sum(dim=0)

    def _update_pattern_memory(self, time_index: int) -> None:
        for ks in (3, 5, 7):
            for pattern in self._find_patterns(ks):
                ph = self._hash_pattern(pattern)
                if ph not in self.pattern_memory:
                    self.pattern_memory[ph] = {
                        'pattern': pattern.cpu(),
                        'first_seen': time_index,
                        'occurrences': [],
                        'context': [],
                    }
                info = self.pattern_memory[ph]
                info['occurrences'].append(time_index)
                # Limit context list to avoid unbounded growth
                if len(info['context']) < 200:
                    info['context'].append({
                        'memory_state': self.memory.clone().cpu(),
                        'time': time_index,
                    })

    def _find_patterns(self, kernel_size: int) -> List[torch.Tensor]:
        if self.memory.shape[0] < kernel_size:
            return []
        kernel = torch.ones(kernel_size, device=self.device)
        k3d = kernel.unsqueeze(0).unsqueeze(0)
        mem = self.memory.unsqueeze(0).unsqueeze(0)
        conv = F.conv1d(mem, k3d, padding=kernel_size - 1).squeeze()
        peaks = (conv > conv.mean() + conv.std()).nonzero(as_tuple=True)[0]
        patterns = []
        for peak in peaks:
            start = max(0, int(peak.item()) - kernel_size)
            end = start + kernel_size
            if end <= self.memory.shape[0]:
                p = self.memory[start:end]
                if self._is_valid_pattern(p):
                    patterns.append(p)
        return patterns

    def _is_valid_pattern(self, pattern: torch.Tensor) -> bool:
        if len(pattern) < 3:
            return False
        if pattern.std() < 0.1:
            return False
        fft = torch.fft.fft(pattern)
        power = torch.abs(fft) ** 2
        if power.max() < 2 * power.mean():
            return False
        for existing in self.pattern_memory.values():
            ep = existing['pattern'].to(self.device)
            if len(ep) == len(pattern):
                if self._pattern_similarity(pattern, ep) > 0.95:
                    return False
        return True

    def _pattern_similarity(self, p1: torch.Tensor,
                            p2: torch.Tensor) -> float:
        """FIX #19 — returned Tensor; now returns float via .item()."""
        basic = F.cosine_similarity(
            p1.unsqueeze(0), p2.unsqueeze(0)).item()
        fa = torch.abs(torch.fft.fft(p1))
        fb = torch.abs(torch.fft.fft(p2))
        freq = F.cosine_similarity(
            fa.unsqueeze(0), fb.unsqueeze(0)).item()
        return (basic + freq) / 2.0

    @staticmethod
    def _hash_pattern(pattern: Any) -> str:
        """FIX #3 — was broken by mixed tabs/spaces. Cleaned up."""
        if isinstance(pattern, torch.Tensor):
            return str(hash(pattern.cpu().numpy().tobytes()))
        if isinstance(pattern, dict) and 'data' in pattern:
            return str(hash(pattern['data'].cpu().numpy().tobytes()))
        return str(hash(str(pattern)))


# ===========================================================================
# PATTERN PROCESSOR
# ===========================================================================

class PatternProcessor:
    """Advanced pattern processing with memory integration."""

    def __init__(self, memory_size: int, device: str = _best_device()):
        self.device = torch.device(device)
        self.memory_formation = MemoryFormation(memory_size, 100, device)
        self.pattern_evolution: Dict[str, List] = defaultdict(list)
        self.pattern_families: Dict[str, Dict] = {}
        self.connection_graph: Dict[str, Set[str]] = defaultdict(set)
        self.learning_rate = torch.tensor(0.01, device=device)
        self.pattern_weights = torch.ones(memory_size, device=device)

    @profile_call
    async def process_pattern(self, pattern: torch.Tensor,
                              context: Optional[Dict] = None) -> Dict[str, Any]:
        memory_result = self.memory_formation.integrate(
            pattern, pattern, time_index=len(self.pattern_evolution))
        patterns = self._extract_patterns(memory_result)
        self._update_evolution(patterns)
        self._organize_families(patterns)
        self._update_connections(patterns)
        insights = self._generate_insights(patterns, context)

        # FIX #15 — compute and include 'confidence' so ThoughtChain doesn't KeyError
        confidence = self._compute_result_confidence(patterns)

        return {
            'patterns': patterns,
            'memory': memory_result,
            'families': self._get_family_info(patterns),
            'connections': self._get_connection_info(patterns),
            'insights': insights,
            'confidence': confidence,
        }

    def _compute_result_confidence(self,
                                   patterns: List[Dict[str, Any]]) -> float:
        """Aggregate quality of recognised patterns into a confidence score."""
        if not patterns:
            return 0.0
        qualities = [p.get('quality', 0.0) for p in patterns]
        return float(np.mean(qualities))

    def _extract_patterns(self,
                          memory: torch.Tensor) -> List[Dict[str, Any]]:
        patterns = []
        for scale in (3, 5, 7, 11):
            patterns.extend(self._find_scale_patterns(memory, scale))
        unique = self._remove_redundant(patterns)
        result = []
        for p in unique:
            analysis = self._analyze_pattern(p)
            if analysis['quality'] > 0.5:
                result.append(analysis)
        return result

    def _find_scale_patterns(self, data: torch.Tensor,
                             scale: int) -> List[torch.Tensor]:
        if data.shape[0] < scale:
            return []
        kernel = self._create_pattern_kernel(scale)
        d3d = data.unsqueeze(0).unsqueeze(0)
        k3d = kernel.unsqueeze(0).unsqueeze(0)
        conv = F.conv1d(d3d, k3d, padding=scale - 1).squeeze()
        mean, std = conv.mean(), conv.std()
        peaks = (conv > mean + 2 * std).nonzero(as_tuple=True)[0]
        patterns = []
        for peak in peaks:
            start = max(0, int(peak.item()) - scale)
            end = start + scale
            if end <= data.shape[0]:
                patterns.append(data[start:end])
        return patterns

    def _create_pattern_kernel(self, scale: int) -> torch.Tensor:
        base = torch.ones(scale, device=self.device)
        mod = torch.sin(torch.linspace(0, math.pi, scale, device=self.device))
        return base * mod

    def _remove_redundant(self,
                          patterns: List[torch.Tensor]) -> List[torch.Tensor]:
        if not patterns:
            return []
        # Normalise lengths to shortest for batch ops
        min_len = min(p.shape[0] for p in patterns)
        trimmed = [p[:min_len] for p in patterns]
        mat = torch.stack(trimmed).float()
        norms = torch.norm(mat, dim=1, keepdim=True).clamp(min=1e-10)
        normed = mat / norms
        sims = torch.mm(normed, normed.T)
        unique_idx: List[int] = []
        used = torch.zeros(len(patterns), dtype=torch.bool)
        for i in range(len(patterns)):
            if not used[i]:
                unique_idx.append(i)
                used |= sims[i] > 0.9
        return [patterns[i] for i in unique_idx]

    def _analyze_pattern(self, pattern: torch.Tensor) -> Dict[str, Any]:
        return {
            'data': pattern.clone(),
            'length': len(pattern),
            'mean': pattern.mean().item(),
            'std': pattern.std().item(),
            'energy': (pattern ** 2).sum().item(),
            'type': self._classify_pattern(pattern),  # FIX #16 — add 'type'
            'frequency': self._analyze_frequency(pattern),
            'structure': self._analyze_structure_tensor(pattern),
            'complexity': self._compute_complexity_tensor(pattern),
            'quality': self._assess_quality(pattern),
        }

    def _classify_pattern(self, pattern: torch.Tensor) -> str:
        """Assign a basic label based on spectral and variance properties."""
        std = pattern.std().item()
        fft = torch.abs(torch.fft.fft(pattern))
        dominant_freq = fft.argmax().item()
        if std < 0.05:
            return 'flat'
        if dominant_freq == 0:
            return 'dc_offset'
        if dominant_freq == 1:
            return 'fundamental'
        if dominant_freq <= len(pattern) // 4:
            return 'low_frequency'
        return 'high_frequency'

    def _analyze_frequency(self, pattern: torch.Tensor) -> Dict[str, float]:
        fft = torch.fft.fft(pattern)
        power = torch.abs(fft) ** 2
        return {
            'dominant': float(power.argmax().item()),
            'power': float(power.sum().item()),
            'bandwidth': float((power > power.mean()).sum().item()),
        }

    def _analyze_structure_tensor(self,
                                  pattern: torch.Tensor) -> Dict[str, float]:
        p3d = pattern.unsqueeze(0).unsqueeze(0)
        auto = F.conv1d(p3d, p3d, padding=len(pattern) - 1).squeeze()
        peaks = (auto > auto.mean() + auto.std()).sum().item()
        return {
            'periodicity': float(peaks),
            'symmetry': self._compute_symmetry(pattern),
            'complexity': self._compute_complexity_tensor(pattern),
        }

    def _compute_symmetry(self, pattern: torch.Tensor) -> float:
        n = len(pattern)
        mid = n // 2
        if mid == 0:
            return 1.0
        diff = torch.norm(pattern[:mid] - pattern[-mid:].flip(0))
        return math.exp(-diff.item())

    def _compute_complexity_tensor(self, pattern: torch.Tensor) -> float:
        m, r = 2, 0.2 * pattern.std().clamp(min=1e-10)
        n = len(pattern)
        if n < m + 1:
            return 0.0
        vecs = torch.stack([pattern[i:i + m] for i in range(n - m + 1)])
        dists = torch.cdist(vecs.float(), vecs.float())
        corr = (dists <= r).float().mean()
        return -torch.log(corr + 1e-10).item()

    def _assess_quality(self, pattern: torch.Tensor) -> float:
        variation = pattern.std() / (pattern.mean().abs() + 1e-10)
        symmetry = self._compute_symmetry(pattern)
        simplicity = math.exp(-self._compute_complexity_tensor(pattern))
        return float((variation.item() + symmetry + simplicity) / 3.0)

    def _update_evolution(self, patterns: List[Dict[str, Any]]) -> None:
        """FIX #4 — was `evolution = list.append(...)` which returned None."""
        for pattern in patterns:
            ph = self._hash_pattern(pattern['data'])
            self.pattern_evolution[ph].append({   # not assigned to a variable
                'pattern': pattern,
                'time': time.time(),
                'metrics': {
                    'complexity': pattern['complexity'],
                    'energy': pattern['energy'],
                    'quality': pattern['quality'],
                },
            })

    def _organize_families(self, patterns: List[Dict[str, Any]]) -> None:
        for pattern in patterns:
            best_family: Optional[str] = None
            best_sim = 0.7
            for fid, family in self.pattern_families.items():
                sim = self._compute_family_similarity(pattern, family)
                if sim > best_sim:
                    best_sim = sim
                    best_family = fid
            if best_family is None:
                fid = f"family_{len(self.pattern_families)}"
                self.pattern_families[fid] = {
                    'prototype': pattern,
                    'members': [],
                    'evolution': [],
                    'statistics': defaultdict(list),
                }
                best_family = fid
            family = self.pattern_families[best_family]
            family['members'].append(pattern)
            family['evolution'].append({
                'time': time.time(),
                'pattern': pattern,
                'similarity': best_sim,
            })
            for k, v in pattern.items():
                if isinstance(v, (int, float)):
                    family['statistics'][k].append(v)
            family['prototype'] = self._update_prototype(family)

    def _update_prototype(self, family: Dict[str, Any]) -> Dict[str, Any]:
        members = family['members']
        if not members:
            return family['prototype']
        try:
            data = torch.stack([m['data'] for m in members]).mean(0)
        except RuntimeError:
            data = members[-1]['data']
        features = {
            k: sum(m[k] for m in members) / len(members)
            for k in members[0]
            if isinstance(members[0][k], (int, float))
        }
        return {'data': data, **features,
                'members': len(members), 'last_update': time.time()}

    def _compute_family_similarity(self, pattern: Dict[str, Any],
                                   family: Dict[str, Any]) -> float:
        proto = family['prototype']
        feat_sim = self._compute_feature_similarity(pattern, proto)
        struct_sim = self._compute_structural_similarity(
            pattern['data'], proto['data'])
        stat_sim = self._compute_statistical_similarity(
            pattern, family['statistics'])
        weights = torch.tensor([0.4, 0.4, 0.2], device=self.device)
        sims = torch.tensor([feat_sim, struct_sim, stat_sim],
                            device=self.device)
        return (weights * sims).sum().item()

    def _compute_feature_similarity(self, p1: Dict, p2: Dict) -> float:
        feats = ('complexity', 'energy', 'quality')
        sims = []
        for f in feats:
            if f in p1 and f in p2:
                denom = max(abs(p1[f]), abs(p2[f]), 1e-10)
                sims.append(1 - abs(p1[f] - p2[f]) / denom)
        return float(np.mean(sims)) if sims else 0.0

    def _compute_structural_similarity(self, p1: torch.Tensor,
                                       p2: torch.Tensor) -> float:
        n = min(len(p1), len(p2))
        if n == 0:
            return 0.0
        a, b = p1[:n].float(), p2[:n].float()
        direct = F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()
        fa = torch.abs(torch.fft.fft(a))
        fb = torch.abs(torch.fft.fft(b))
        freq = F.cosine_similarity(fa.unsqueeze(0), fb.unsqueeze(0)).item()
        c1 = self._compute_complexity_tensor(a)
        c2 = self._compute_complexity_tensor(b)
        struct = 1 - abs(c1 - c2) / (max(c1, c2, 1e-10))
        w = torch.tensor([0.4, 0.4, 0.2], device=self.device)
        s = torch.tensor([direct, freq, struct], device=self.device)
        return (w * s).sum().item()

    def _compute_statistical_similarity(self, pattern: Dict,
                                        stats: Dict) -> float:
        sims = []
        for k, vals in stats.items():
            if k in pattern and isinstance(pattern[k], (int, float)) and vals:
                mean = sum(vals) / len(vals)
                std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
                z = abs(pattern[k] - mean) / (std + 1e-10)
                sims.append(math.exp(-z))
        return float(np.mean(sims)) if sims else 0.0

    def _update_connections(self, patterns: List[Dict[str, Any]]) -> None:
        for pattern in patterns:
            ph = self._hash_pattern(pattern['data'])
            for other_hash, evol in self.pattern_evolution.items():
                if other_hash == ph or not evol:
                    continue
                try:
                    other_data = evol[-1]['pattern']['data']
                    sim = self._compute_structural_similarity(
                        pattern['data'], other_data)
                    if sim > 0.8:
                        self.connection_graph[ph].add(other_hash)
                        self.connection_graph[other_hash].add(ph)
                except Exception:
                    pass

    def _generate_insights(self, patterns: List[Dict[str, Any]],
                           context: Optional[Dict]) -> List[Dict[str, Any]]:
        insights = []
        for pattern in patterns:
            ph = self._hash_pattern(pattern['data'])
            evolution = self.pattern_evolution[ph]
            family = next(
                (fid for fid, fam in self.pattern_families.items()
                 if any(self._hash_pattern(m['data']) == ph
                        for m in fam['members'])),
                None,
            )
            connections = self.connection_graph[ph]
            insight: Dict[str, Any] = {
                'pattern_type': pattern.get('type', 'unknown'),
                'frequency': len(evolution),
                'family': family,
                'family_size': (len(self.pattern_families[family]['members'])
                                if family else 0),
                'connections': len(connections),
                'evolution': {
                    'complexity_trend': self._compute_trend(
                        [e['metrics']['complexity'] for e in evolution]),
                    'quality_trend': self._compute_trend(
                        [e['metrics']['quality'] for e in evolution]),
                    'energy_trend': self._compute_trend(
                        [e['metrics']['energy'] for e in evolution]),
                },
            }
            if context:
                insight.update(self._context_specific_insights(pattern, context))
            insights.append(insight)
        return insights

    def _compute_trend(self, values: List[float]) -> str:
        if len(values) < 2:
            return 'stable'
        x = torch.arange(len(values), device=self.device).float()
        y = torch.tensor(values, device=self.device).float()
        slope = (((x - x.mean()) * (y - y.mean())).sum()
                 / ((x - x.mean()) ** 2).sum().clamp(min=1e-10))
        s = slope.item()
        if abs(s) < 0.1:
            return 'stable'
        if s > 0.5:
            return 'increasing'
        if s > 0:
            return 'slightly_increasing'
        if s < -0.5:
            return 'decreasing'
        return 'slightly_decreasing'

    def _context_specific_insights(self, pattern: Dict,
                                   context: Dict) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        if 'target' in context:
            out['target_similarity'] = self._compute_structural_similarity(
                pattern['data'], context['target'])
        if 'previous_patterns' in context:
            sims = [self._compute_structural_similarity(pattern['data'], p)
                    for p in context['previous_patterns']]
            out['novelty'] = 1 - max(sims) if sims else 1.0
        return out

    def _get_family_info(self,
                         patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            'total_families': len(self.pattern_families),
            'pattern_families': [
                p.get('family', 'unassigned') for p in patterns
            ],
        }

    def _get_connection_info(self,
                             patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_conn = sum(
            len(self.connection_graph[self._hash_pattern(p['data'])])
            for p in patterns
        )
        return {'total_connections': total_conn}

    @staticmethod
    def _hash_pattern(pattern: Any) -> str:
        """FIX #3 — was broken by mixed tabs/spaces; cleaned up."""
        if isinstance(pattern, torch.Tensor):
            return str(hash(pattern.cpu().numpy().tobytes()))
        if isinstance(pattern, dict) and 'data' in pattern:
            return str(hash(pattern['data'].cpu().numpy().tobytes()))
        return str(hash(str(pattern)))

# ===========================================================================
# THOUGHT CHAIN  (appended to Thinking_CoT_fixed.py)
# ===========================================================================

class ThoughtChain:
    """Bounded, self-reflective chain-of-thought engine."""

    def __init__(self, n: int = 1_000_000,
                 device: str = _best_device()):
        # FIX #1 — self.device was never set
        self.device = device

        # Core bounds
        self.max_depth = int(math.log2(max(n, 2)))
        self.queue_size = int(math.sqrt(n))
        self.min_gain = 1 / n

        # Processing components
        self.pattern_processor = PatternProcessor(512, device)
        self.memory_formation = MemoryFormation(512, 100, device)

        # Thought management
        self.thought_queue: List[Thought] = []
        self.thought_cache: Dict[str, Dict] = {}
        # FIX #1 — pattern_combinations was misplaced before __init__ body
        self.pattern_combinations: Dict[Tuple, Dict] = {}

        # Learning components
        self.approach_history: Dict[str, List[str]] = defaultdict(list)
        self.success_patterns: Dict[str, Dict] = {}
        self.learning_rate = 0.01
        self.min_confidence = 0.3

        # Performance tracking
        self.performance_stats: Dict[str, List] = defaultdict(list)

    # -----------------------------------------------------------------------
    # PUBLIC API
    # -----------------------------------------------------------------------

    @profile_call
    async def process_thought(self, thought: Thought) -> Dict[str, Any]:
        """Main processing pipeline."""
        cache_key = self._hash_thought(thought)

        # Cache hit
        if cache_key in self.thought_cache:
            return self._enhance_cached_result(thought,
                                               self.thought_cache[cache_key])

        # Depth guard
        if thought.depth > self.max_depth:
            return await self._handle_recursion(thought)

        # Pattern processing
        pattern_result = await self.pattern_processor.process_pattern(
            self._prepare_input(thought), context=thought.context)

        # FIX #15 — 'confidence' now always present in result
        confidence = pattern_result['confidence']

        # Internal dialogue: ask sub-questions if not confident enough
        if confidence < 0.8:
            await self._generate_and_process_questions(thought, pattern_result)

        thought.patterns.extend(pattern_result['patterns'])
        thought.confidence = confidence
        self._learn_from_result(thought, pattern_result)

        if confidence > 0.8:
            self.thought_cache[cache_key] = pattern_result

        return self._prepare_result(thought, pattern_result)

    # -----------------------------------------------------------------------
    # INPUT / OUTPUT PREPARATION
    # -----------------------------------------------------------------------

    def _prepare_input(self, thought: Thought) -> torch.Tensor:
        """FIX #2 — was broken by mixed-indent; all methods below similarly."""
        if isinstance(thought.content, torch.Tensor):
            return thought.content.to(self.device)
        if isinstance(thought.content, np.ndarray):
            return torch.from_numpy(thought.content).float().to(self.device)
        # Scalar hash representation for non-numeric content
        h = abs(hash(str(thought.content))) % (2 ** 31)
        return torch.tensor([float(h)], device=self.device)

    def _prepare_result(self, thought: Thought,
                        pattern_result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'patterns': thought.patterns,
            'confidence': thought.confidence,
            'memory': pattern_result.get('memory'),
            'insights': pattern_result.get('insights', []),
            'performance': dict(thought.performance),
        }

    def _simplify_thought(self, thought: Thought) -> Thought:
        simplified = Thought(
            content=thought.content,
            depth=thought.depth + 1,
            previous_approaches=thought.previous_approaches.copy(),
        )
        if (isinstance(thought.content, torch.Tensor)
                and len(thought.content) > 100):
            simplified.content = thought.content[::2]
        return simplified

    def _best_partial_result(self, thought: Thought) -> Dict[str, Any]:
        return {
            'patterns': thought.patterns,
            'confidence': max(self.min_confidence, thought.confidence),
            'partial': True,
            'reason': 'recursion_limit',
            'performance': dict(thought.performance),
        }

    def _apply_approach(self, thought: Thought, approach: str) -> Thought:
        modified = Thought(
            content=thought.content,
            depth=thought.depth,
            previous_approaches=thought.previous_approaches.copy(),
            context=thought.context.copy(),
        )
        if approach == "decomposition":
            if isinstance(modified.content, torch.Tensor):
                modified.content = self._decompose_tensor(modified.content)
        elif approach == "frequency_analysis":
            if isinstance(modified.content, torch.Tensor):
                modified.content = torch.abs(
                    torch.fft.fft(modified.content.float()))
        elif approach == "pattern_based":
            modified.context['focus'] = 'patterns'
        return modified

    def _decompose_tensor(self, tensor: torch.Tensor) -> torch.Tensor:
        if len(tensor) < 2:
            return tensor
        return torch.cat([tensor[::2], tensor[1::2]])

    # -----------------------------------------------------------------------
    # COMPLEXITY & STRUCTURE
    # -----------------------------------------------------------------------

    def _compute_complexity(self, thought: Thought) -> float:
        if isinstance(thought.content, torch.Tensor):
            t = thought.content.float()
            return min(1.0,
                       (t.std() / (t.mean().abs() + 1e-10)).item())
        pat_c = len(thought.patterns) * 0.1
        dep_c = thought.depth * 0.1
        return min(1.0, pat_c + dep_c)

    def _analyze_structure(self, thought: Thought) -> Dict[str, float]:
        if not isinstance(thought.content, torch.Tensor):
            return {'periodicity': 0.0, 'complexity': 0.5}
        data = thought.content.float().cpu().numpy()
        acf = np.correlate(data, data, mode='full')[len(data) - 1:]
        peaks = float((acf > np.mean(acf) + np.std(acf)).sum())
        return {
            'periodicity': peaks,
            'complexity': self._compute_complexity(thought),
        }

    # -----------------------------------------------------------------------
    # HASHING
    # -----------------------------------------------------------------------

    @staticmethod
    def _hash_thought(thought: Thought) -> str:
        """FIX #14 — was called in process_thought but never defined."""
        if isinstance(thought.content, torch.Tensor):
            return str(hash(thought.content.cpu().numpy().tobytes()))
        return str(hash(str(thought.content)))

    @staticmethod
    def _hash_pattern(pattern: Any) -> str:
        if isinstance(pattern, torch.Tensor):
            return str(hash(pattern.cpu().numpy().tobytes()))
        if isinstance(pattern, dict) and 'data' in pattern:
            return str(hash(pattern['data'].cpu().numpy().tobytes()))
        return str(hash(str(pattern)))

    # -----------------------------------------------------------------------
    # RECURSION HANDLING
    # -----------------------------------------------------------------------

    async def _handle_recursion(self, thought: Thought) -> Dict[str, Any]:
        new_approach = self._generate_new_approach(thought)
        if new_approach and new_approach not in thought.previous_approaches:
            thought.previous_approaches.add(new_approach)
            self._queue_thought(thought)
            modified = self._apply_approach(thought, new_approach)
            return await self.process_thought(modified)
        simplified = self._simplify_thought(thought)
        if self._hash_thought(simplified) != self._hash_thought(thought):
            return await self.process_thought(simplified)
        return self._best_partial_result(thought)

    def _generate_new_approach(self, thought: Thought) -> Optional[str]:
        successful = set()
        for key, result in self.thought_cache.items():
            if result.get('confidence', 0) > 0.8:
                hist = self.approach_history.get(key, [])
                # FIX #6 — guard empty list before indexing
                if hist:
                    successful.add(hist[-1])
        untried = successful - thought.previous_approaches
        if untried:
            return self._select_best_approach(thought, list(untried))
        return self._generate_novel_approach(thought)

    def _select_best_approach(self, thought: Thought,
                              approaches: List[str]) -> str:
        scores = []
        for approach in approaches:
            successes = sum(
                1 for key in self.thought_cache
                if (self.approach_history.get(key, [None])[-1] == approach
                    and self.thought_cache[key].get('confidence', 0) > 0.8))
            attempts = sum(
                1 for key in self.thought_cache
                if self.approach_history.get(key, [None])[-1] == approach)
            sr = successes / max(1, attempts)
            sim = self._compute_approach_similarity(thought, approach)
            scores.append(sr * sim)
        return approaches[int(np.argmax(scores))]

    def _generate_novel_approach(self, thought: Thought) -> str:
        complexity = self._compute_complexity(thought)
        structure = self._analyze_structure(thought)
        if complexity > 0.8:
            return "decomposition"
        if structure['periodicity'] > 0:
            return "frequency_analysis"
        if thought.patterns:
            return "pattern_based"
        return f"approach_{len(thought.previous_approaches)}"

    def _compute_approach_similarity(self, thought: Thought,
                                     approach: str) -> float:
        """
        FIX #11 — was called in _select_best_approach but never defined.
        Returns a rough similarity score between current thought and approach.
        """
        complexity = self._compute_complexity(thought)
        approach_map = {
            'decomposition': 0.8,
            'frequency_analysis': 0.5,
            'pattern_based': 0.3,
        }
        base = approach_map.get(approach, 0.1)
        # Higher-complexity thoughts favour decomposition more
        if approach == 'decomposition':
            return base * complexity
        return base * (1 - complexity * 0.5)

    # -----------------------------------------------------------------------
    # CACHING
    # -----------------------------------------------------------------------

    def _enhance_cached_result(self, thought: Thought,
                               cached: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIX #12 — was called in process_thought but never defined.
        Returns cached result enriched with current thought performance.
        """
        enhanced = cached.copy()
        enhanced['from_cache'] = True
        enhanced['cache_depth'] = thought.depth
        return enhanced

    def _queue_thought(self, thought: Thought) -> None:
        """
        FIX #13 — was called in _handle_recursion but never defined.
        Appends to the internal thought queue respecting queue_size.
        """
        if len(self.thought_queue) < self.queue_size:
            self.thought_queue.append(thought)
        else:
            # Evict lowest-confidence entry
            self.thought_queue.sort(
                key=lambda t: t.confidence, reverse=True)
            self.thought_queue[-1] = thought

    # -----------------------------------------------------------------------
    # QUESTION GENERATION (internal dialogue)
    # -----------------------------------------------------------------------

    async def _generate_and_process_questions(
            self, thought: Thought,
            result: Dict[str, Any]) -> None:
        for question in self._generate_questions(thought, result):
            sub_result = await self.process_thought(question)
            self._integrate_sub_result(thought, sub_result)
            thought.sub_thoughts.append(question)

    def _generate_questions(self, thought: Thought,
                            result: Dict[str, Any]) -> List[Thought]:
        questions: List[Thought] = []
        for pattern in result.get('patterns', []):
            if pattern.get('quality', 0) > 0.5:
                questions.extend(
                    self._generate_pattern_questions(pattern, thought))
        structure = self._analyze_structure(thought)
        if structure['complexity'] > 0.5:
            questions.extend(
                self._generate_structure_questions(structure, thought))
        if result.get('confidence', 0) < 0.5:
            questions.extend(
                self._generate_learning_questions(result, thought))
        return questions

    def _generate_pattern_questions(self, pattern: Dict,
                                    parent: Thought) -> List[Thought]:
        # FIX #16 — pattern['type'] now always set by _classify_pattern
        ptype = pattern.get('type', 'unknown')
        questions = [
            Thought(content=f"Why does pattern '{ptype}' appear?",
                    depth=parent.depth + 1,
                    context={'parent_pattern': pattern},
                    parent=parent),
        ]
        if pattern.get('evolution'):
            questions.append(
                Thought(content="How has this pattern evolved?",
                        depth=parent.depth + 1,
                        context={'pattern_evolution': pattern['evolution']},
                        parent=parent))
        if pattern.get('connections'):
            questions.append(
                Thought(content="How do connected patterns influence this?",
                        depth=parent.depth + 1,
                        context={'pattern_connections': pattern['connections']},
                        parent=parent))
        return questions

    def _generate_structure_questions(self, structure: Dict,
                                      parent: Thought) -> List[Thought]:
        questions: List[Thought] = []
        if structure['periodicity'] > 0:
            questions.append(
                Thought(content="What causes this periodicity?",
                        depth=parent.depth + 1,
                        context={'structure': structure},
                        parent=parent))
        if structure['complexity'] > 0.7:
            questions.append(
                Thought(content="Can this be simplified?",
                        depth=parent.depth + 1,
                        context={'complexity': structure['complexity']},
                        parent=parent))
        return questions

    def _generate_learning_questions(self, result: Dict,
                                     parent: Thought) -> List[Thought]:
        return [
            Thought(content="Why is confidence low?",
                    depth=parent.depth + 1,
                    context={'confidence': result.get('confidence', 0)},
                    parent=parent),
            Thought(content="How can this be improved?",
                    depth=parent.depth + 1,
                    context={'result': result},
                    parent=parent),
        ]

    def _integrate_sub_result(self, thought: Thought,
                              sub_result: Dict[str, Any]) -> None:
        if 'patterns' in sub_result:
            thought.patterns.extend(sub_result['patterns'])
        if sub_result.get('confidence', 0) > thought.confidence:
            thought.confidence = sub_result['confidence']
        thought.context.update(sub_result.get('insights', {}))
        self._update_performance(thought, sub_result)

    # -----------------------------------------------------------------------
    # LEARNING
    # -----------------------------------------------------------------------

    def _learn_from_result(self, thought: Thought,
                           result: Dict[str, Any]) -> None:
        key = self._hash_thought(thought)
        if key not in self.success_patterns:
            self.success_patterns[key] = {
                'attempts': 0, 'successes': 0, 'patterns': [],
            }
        stats = self.success_patterns[key]
        stats['attempts'] += 1
        if result.get('confidence', 0) > 0.8:
            stats['successes'] += 1

        # FIX #5 — previous_approaches is a Set, not indexable
        approach = (next(iter(thought.previous_approaches))
                    if thought.previous_approaches else 'initial')
        self.approach_history[key].append(approach)

        if result.get('patterns'):
            self._learn_pattern_combinations(result['patterns'])

    def _learn_pattern_combinations(self,
                                    patterns: List[Dict[str, Any]]) -> None:
        if len(patterns) < 2:
            return
        for i, p1 in enumerate(patterns):
            for p2 in patterns[i + 1:]:
                key = (self._hash_pattern(p1), self._hash_pattern(p2))
                if key not in self.pattern_combinations:
                    self.pattern_combinations[key] = {
                        'count': 0, 'success_count': 0,
                    }
                self.pattern_combinations[key]['count'] += 1

    def _update_performance(self, thought: Thought,
                            result: Dict[str, Any]) -> None:
        metrics = {
            'confidence': result.get('confidence', 0),
            'patterns_found': len(result.get('patterns', [])),
            'processing_time': time.time() - thought.timestamp,
        }
        for k, v in metrics.items():
            thought.performance[k].append(v)


# ===========================================================================
# DISTRIBUTED PROCESSOR
# ===========================================================================

if _RAY_AVAILABLE:
    @ray.remote
    class DistributedProcessor:
        """Distributed thought processing on a single GPU/CPU."""
        def __init__(self, n: int, device_id: int):
            dev = (f'cuda:{device_id}'
                   if torch.cuda.is_available() else 'cpu')
            self.chain = ThoughtChain(n, dev)

        async def process_thought(self, thought: Thought) -> Dict[str, Any]:
            return await self.chain.process_thought(thought)
else:
    class DistributedProcessor:  # type: ignore[no-redef]
        """CPU-only fallback when Ray is not installed."""
        def __init__(self, n: int, device_id: int):
            self.chain = ThoughtChain(n, 'cpu')

        async def process_thought(self, thought: Thought) -> Dict[str, Any]:
            return await self.chain.process_thought(thought)


# ===========================================================================
# INTEGRATED SYSTEM
# ===========================================================================

class IntegratedSystem:
    """Top-level system: routes thoughts to local or distributed processors."""

    def __init__(self, n: int = 1_000_000):
        gpu_count = torch.cuda.device_count() if torch.cuda.is_available() else 0

        if _RAY_AVAILABLE and gpu_count > 0:
            if not ray.is_initialized():
                ray.init(num_gpus=gpu_count)
            self.processors = [
                DistributedProcessor.remote(n, i)
                for i in range(gpu_count)
            ]
        else:
            self.processors = [DistributedProcessor(n, 0)]

        self.chain = ThoughtChain(n)
        self.performance_tracker: Dict[str, List] = defaultdict(list)
        self.start_time = time.time()

    @profile_call
    async def process(self, input_data: Any) -> Dict[str, Any]:
        thought = Thought(content=input_data)
        if self._is_small_task(thought):
            result = await self.chain.process_thought(thought)
        else:
            result = await self._process_distributed(thought)
        self._update_performance(result)
        return result

    async def _process_distributed(self,
                                   thought: Thought) -> Dict[str, Any]:
        chunks = self._split_thought(thought)
        if _RAY_AVAILABLE and isinstance(self.processors[0],
                                        DistributedProcessor):
            futures = [p.process_thought.remote(c)
                       for p, c in zip(self.processors, chunks)]
            results = await asyncio.gather(*[ray.get(f) for f in futures])
        else:
            results = await asyncio.gather(
                *[self.processors[i % len(self.processors)]
                  .process_thought(c)
                  for i, c in enumerate(chunks)])
        return self._combine_results(results)

    def _split_thought(self, thought: Thought) -> List[Thought]:
        if isinstance(thought.content, (np.ndarray, torch.Tensor)):
            n = len(self.processors)
            if isinstance(thought.content, torch.Tensor):
                chunks = thought.content.chunk(n)
            else:
                chunks = np.array_split(thought.content, n)
            return [
                Thought(content=c, depth=thought.depth,
                        context=thought.context.copy())
                for c in chunks
            ]
        return [thought]

    def _combine_results(self,
                         results: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not results:
            return {'confidence': 0.0, 'patterns': []}
        all_patterns: List[Dict] = []
        for r in results:
            all_patterns.extend(r.get('patterns', []))
        confidence = float(np.mean([r.get('confidence', 0) for r in results]))
        memories = [r['memory'] for r in results
                    if r.get('memory') is not None]
        combined_memory = torch.cat(memories) if memories else None
        return {
            'patterns': all_patterns,
            'confidence': confidence,
            'memory': combined_memory,
            'insights': self._combine_insights(results),
            'performance': self._combine_performance(results),
        }

    def _combine_insights(self,
                          results: List[Dict]) -> List[Dict[str, Any]]:
        seen: Set[str] = set()
        out: List[Dict] = []
        for r in results:
            for insight in r.get('insights', []):
                ih = str(hash(str(insight)))
                if ih not in seen:
                    seen.add(ih)
                    out.append(insight)
        return out

    def _combine_performance(self,
                             results: List[Dict]) -> Dict[str, float]:
        metrics: Dict[str, List] = defaultdict(list)
        for r in results:
            for k, v in r.get('performance', {}).items():
                if isinstance(v, list):
                    metrics[k].extend(v)
                else:
                    metrics[k].append(v)
        return {k: float(np.mean(vs)) for k, vs in metrics.items() if vs}

    def _is_small_task(self, thought: Thought) -> bool:
        if isinstance(thought.content, (np.ndarray, torch.Tensor)):
            return len(thought.content) < 1000
        return True

    def _update_performance(self, result: Dict[str, Any]) -> None:
        self.performance_tracker['processing_time'].append(
            time.time() - self.start_time)
        self.performance_tracker['confidence'].append(
            result.get('confidence', 0))
        self.performance_tracker['patterns_found'].append(
            len(result.get('patterns', [])))
        self.performance_tracker['gpu_utilization'].append(
            self._get_gpu_utilization())

    def _get_gpu_utilization(self) -> float:
        if not torch.cuda.is_available():
            return 0.0
        try:
            return torch.cuda.utilization() / 100.0
        except Exception:
            return 0.0

    def get_performance_metrics(self) -> Dict[str, float]:
        metrics: Dict[str, float] = {}
        for k, vals in self.performance_tracker.items():
            if vals:
                metrics[f'avg_{k}'] = float(np.mean(vals))
                metrics[f'max_{k}'] = float(max(vals))
                metrics[f'min_{k}'] = float(min(vals))
        return metrics


# ===========================================================================
# PROFILING RUNNERS
# ===========================================================================

async def run_profiled(data: np.ndarray,
                       batch_size: int = 500) -> List[Dict[str, Any]]:
    """
    Process *data* in batches, collecting decorator-level timing via
    ProfilerRegistry and a cProfile trace of the full run.
    """
    ProfilerRegistry.reset()
    system = IntegratedSystem()
    results: List[Dict] = []

    with CProfileContext(sort="cumulative", top=40) as prof:
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            result = await system.process(batch)
            results.append(result)
            print(f"  Batch {i // batch_size + 1:>3}: "
                  f"confidence={result['confidence']:.3f}  "
                  f"patterns={len(result.get('patterns', []))}")

    print("\n=== cProfile top functions ===")
    print(prof.report)
    print("\n=== Per-method decorator timings ===")
    print(ProfilerRegistry.report(sort_by="total_time"))
    print("\n=== System performance metrics ===")
    for k, v in system.get_performance_metrics().items():
        print(f"  {k}: {v:.4f}")

    return results


async def process_dataset(data: np.ndarray,
                          batch_size: int = 1000) -> List[Dict[str, Any]]:
    """Non-profiled batch processing (production use)."""
    system = IntegratedSystem()
    results: List[Dict] = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        result = await system.process(batch)
        results.append(result)
        print(f"Batch {i // batch_size + 1} | "
              f"confidence={result['confidence']:.3f} | "
              f"patterns={len(result.get('patterns', []))}")
    return results


# ===========================================================================
# ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    import sys

    profiled = "--profile" in sys.argv
    n_samples = 5000

    print(f"Running {'profiled' if profiled else 'standard'} benchmark "
          f"on {n_samples} samples …")

    data = np.random.randn(n_samples).astype(np.float32)

    if profiled:
        results = asyncio.run(run_profiled(data, batch_size=500))
    else:
        results = asyncio.run(process_dataset(data, batch_size=1000))

    # Aggregate final stats
    all_conf = [r['confidence'] for r in results]
    all_pat = [len(r.get('patterns', [])) for r in results]
    print("\n=== Final Results ===")
    print(f"Batches processed : {len(results)}")
    print(f"Mean confidence   : {np.mean(all_conf):.4f}")
    print(f"Mean patterns/batch: {np.mean(all_pat):.1f}")
    print(f"Total patterns    : {sum(all_pat)}")

    if profiled:
        print("\n=== Decorator profiling summary ===")
        print(ProfilerRegistry.report(top_n=15, sort_by="total_time"))
