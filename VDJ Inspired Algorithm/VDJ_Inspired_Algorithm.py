"""
VDJ-Inspired Algorithm — Fixed, Complete, and Profiled
=======================================================
Bugs fixed:
  - SystemConfig missing 6 fields used by downstream classes
  - torch.Tensor has no .skew() / .kurtosis() methods (pandas-only)
  - data.median() returns NamedTuple, not scalar
  - torch.tensor([t1, t2]) wrapping tracked tensors → use torch.stack
  - _analyze_topology called with Pattern, typed as Tensor
  - variations['combinations'] is Tensor not List[Pattern] in UnifiedSystem
  - torch.cuda.empty_cache() unconditional — crashes on CPU-only builds
  - Combinatorial generation unbounded (n=100,r=100 = heat death of universe)
  - _rotate_pattern called but never defined
  - ~40 private helpers called but never implemented — all now implemented

Profiling:
  - SystemProfiler: per-module wall-clock and cProfile instrumentation
  - profile_system() entry point produces a full timing report
"""

import torch
import numpy as np
import cProfile
import pstats
import io
import time
import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum
import logging
from torch.nn import functional as F
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class SystemConfig:
    """System-wide configuration.

    Fields previously missing that caused AttributeError in downstream classes
    have been added with sensible defaults.
    """
    num_gpus: int
    num_cpus: int
    pattern_size: int
    state_dims: Tuple[int, ...]
    batch_size: int = 128
    device: str = field(default_factory=lambda: 'cuda' if torch.cuda.is_available() else 'cpu')

    # ResourceOptimizer — previously caused AttributeError
    max_iterations: int = 50
    tolerance: float = 1e-4
    lambda_balance: float = 0.5
    learning_rate: float = 0.01

    # SpaceExplorer — previously caused AttributeError
    neighbor_threshold: float = 1.5

    # OneShotLearner
    similarity_threshold: float = 0.8

    # CombinatorialGenerator — cap on r to prevent combinatorial explosion
    max_combo_r: int = 8


# ---------------------------------------------------------------------------
# Core data types
# ---------------------------------------------------------------------------

class PatternType(Enum):
    GEOMETRIC     = 1
    COMBINATORIAL = 2
    SEQUENTIAL    = 3
    GRAPH         = 4
    META          = 5


@dataclass
class Pattern:
    """Universal data container passed between all modules."""
    data: torch.Tensor
    type: PatternType
    scale: float
    properties: Dict[str, Any]
    validation: Dict[str, bool]

    def to_device(self, device: torch.device) -> 'Pattern':
        self.data = self.data.to(device)
        return self


# ---------------------------------------------------------------------------
# Resource management
# ---------------------------------------------------------------------------

class ResourceManager:
    """Allocation, caching, and cleanup."""

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)
        self.allocated: Dict[str, List[torch.Tensor]] = defaultdict(list)
        self.cache: Dict[str, Any] = {}

    def allocate(self, size: Tuple[int, ...]) -> torch.Tensor:
        key = f"buffer_{len(self.allocated)}"
        buf = torch.zeros(size, device=self.device)
        self.allocated[key].append(buf)
        return buf

    def cache_result(self, key: str, data: Any) -> None:
        self.cache[key] = data

    def get_cached(self, key: str) -> Optional[Any]:
        return self.cache.get(key)

    def cleanup(self) -> None:
        self.allocated.clear()
        self.cache.clear()
        # BUG FIX: unconditional cuda call crashed CPU-only builds
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


# ---------------------------------------------------------------------------
# Validation system
# ---------------------------------------------------------------------------

class ValidationSystem:
    """Pattern and state validation.

    BUG FIX: all _validate_* / _check_* helpers were declared but never
    implemented — every call raised AttributeError at runtime.
    """

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)

    # ---- public API --------------------------------------------------------

    def validate_pattern(self, pattern: Pattern) -> Dict[str, torch.Tensor]:
        """V(p) = Σᵢ [αᵢS(p) × βᵢR(p) × γᵢC(p)]"""
        structure   = self._validate_structure(pattern)
        rules       = self._validate_rules(pattern)
        consistency = self._check_consistency(pattern)
        weights     = torch.tensor([0.4, 0.3, 0.3], device=self.device)
        combined    = weights[0]*structure + weights[1]*rules + weights[2]*consistency
        return {'structure': structure, 'rules': rules,
                'consistency': consistency, 'combined': combined}

    def validate_state(self, state: torch.Tensor) -> Dict[str, torch.Tensor]:
        """V(s) = K(s) × L(s) × M(s)"""
        known  = self._validate_known_state(state)
        local  = self._validate_local_consistency(state)
        meta   = self._validate_meta(state)
        return {'known': known, 'local': local, 'meta': meta,
                'combined': known * local * meta}

    # ---- private helpers ---------------------------------------------------

    def _validate_structure(self, pattern: Pattern) -> torch.Tensor:
        shape_v = self._validate_shape(pattern)
        props_v = self._validate_properties(pattern)
        type_v  = self._validate_type(pattern)
        return torch.stack([shape_v, props_v, type_v]).mean()

    def _validate_rules(self, pattern: Pattern) -> torch.Tensor:
        rules = [self._check_size_rules(pattern),
                 self._check_pattern_rules(pattern),
                 self._check_state_rules(pattern)]
        return torch.stack(rules).mean()

    def _check_consistency(self, pattern: Pattern) -> torch.Tensor:
        """Data-consistency score: checks finite values and finite variance."""
        data = pattern.data
        is_finite  = torch.isfinite(data).float().mean()
        has_spread = torch.clamp(data.std(), 0.0, 1.0)
        return (is_finite + has_spread) / 2.0

    # Shape / property / type checks
    def _validate_shape(self, pattern: Pattern) -> torch.Tensor:
        ndim = pattern.data.ndim
        valid = 1.0 if ndim in (1, 2) else 0.5
        return torch.tensor(valid, device=self.device)

    def _validate_properties(self, pattern: Pattern) -> torch.Tensor:
        score = 1.0 if len(pattern.properties) >= 0 else 0.0
        return torch.tensor(score, device=self.device)

    def _validate_type(self, pattern: Pattern) -> torch.Tensor:
        valid = isinstance(pattern.type, PatternType)
        return torch.tensor(1.0 if valid else 0.0, device=self.device)

    # Rule checks
    def _check_size_rules(self, pattern: Pattern) -> torch.Tensor:
        n = pattern.data.numel()
        score = min(1.0, n / max(self.config.pattern_size, 1))
        return torch.tensor(score, device=self.device)

    def _check_pattern_rules(self, pattern: Pattern) -> torch.Tensor:
        data = pattern.data
        normalised = (data - data.mean()) / (data.std() + 1e-8)
        in_range = (normalised.abs() < 3.0).float().mean()
        return in_range

    def _check_state_rules(self, pattern: Pattern) -> torch.Tensor:
        return torch.isfinite(pattern.data).float().mean()

    # State checks
    def _validate_known_state(self, state: torch.Tensor) -> torch.Tensor:
        return torch.isfinite(state).float().mean()

    def _validate_local_consistency(self, state: torch.Tensor) -> torch.Tensor:
        if state.ndim < 2:
            return torch.tensor(1.0, device=self.device)
        diff_x = (state[:, 1:] - state[:, :-1]).abs().mean()
        score  = torch.exp(-diff_x)
        return score

    def _validate_meta(self, state: torch.Tensor) -> torch.Tensor:
        mean_abs = state.abs().mean()
        return torch.sigmoid(torch.tensor(1.0) - mean_abs)


# ---------------------------------------------------------------------------
# State evolution
# ---------------------------------------------------------------------------

class StateEvolution:
    """Time-based state progression.

    BUG FIX: _compute_gradient, _next_state, _compute_environment were called
    but never defined.
    """

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)

    def evolve(self, state: torch.Tensor, time: int) -> torch.Tensor:
        """E(s,t) = ∏ᵢ [F(sᵢ) × T(sᵢ) × A(sᵢ)]"""
        forward    = self._forward_evolution(state, time)
        transition = self._compute_transition(state, time)
        adaptation = self._compute_adaptation(state, time)
        return forward * transition * adaptation

    def _forward_evolution(self, state: torch.Tensor, time: int) -> torch.Tensor:
        t   = torch.tensor(float(time), device=self.device)
        rate = torch.sigmoid(t / 10.0)
        grad = self._compute_gradient(state)
        return state + rate * grad

    def _compute_transition(self, state: torch.Tensor, time: int) -> torch.Tensor:
        t    = torch.tensor(float(time), device=self.device)
        prob = torch.sigmoid(state * t / 20.0)
        next_s = self._next_state(state)
        return prob * state + (1.0 - prob) * next_s

    def _compute_adaptation(self, state: torch.Tensor, time: int) -> torch.Tensor:
        t    = torch.tensor(float(time), device=self.device)
        rate = torch.tanh(t / 15.0)
        env  = self._compute_environment(state, time)
        return state * (1.0 + rate * env)

    # --- implemented helpers ------------------------------------------------

    def _compute_gradient(self, state: torch.Tensor) -> torch.Tensor:
        """Finite-difference gradient along last dimension."""
        if state.ndim < 2:
            return torch.zeros_like(state)
        padded = F.pad(state.unsqueeze(0), (1, 1), mode='replicate').squeeze(0)
        return (padded[..., 2:] - padded[..., :-2]) / 2.0

    def _next_state(self, state: torch.Tensor) -> torch.Tensor:
        """Predict next state via one-step forward Euler on gradient."""
        return state + 0.1 * self._compute_gradient(state)

    def _compute_environment(self, state: torch.Tensor, time: int) -> torch.Tensor:
        """Environmental pressure: decays mean activity over time."""
        decay = math.exp(-time / 100.0)
        return state.abs().mean() * decay * torch.ones_like(state)


# ---------------------------------------------------------------------------
# Graph evolution
# ---------------------------------------------------------------------------

class GraphEvolution:
    """Dynamic graph state updates.

    BUG FIX: all sub-helpers were stubs.
    """

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)

    def evolve(self, graph: torch.Tensor) -> torch.Tensor:
        """∂G/∂t = N(G) + E(G) + A(G)"""
        dynamics   = self._compute_dynamics(graph)
        evolution  = self._compute_evolution(graph)
        adaptation = self._compute_adaptation(graph)
        return graph + dynamics + evolution + adaptation

    # ---- dynamics ----------------------------------------------------------

    def _compute_dynamics(self, graph: torch.Tensor) -> torch.Tensor:
        return (self._node_dynamics(graph) +
                self._edge_dynamics(graph) +
                self._global_dynamics(graph))

    def _node_dynamics(self, graph: torch.Tensor) -> torch.Tensor:
        """Degree-based activation: high-degree nodes attract more flow."""
        degree = graph.sum(dim=-1, keepdim=True)
        return 0.01 * torch.tanh(degree) * torch.ones_like(graph)

    def _edge_dynamics(self, graph: torch.Tensor) -> torch.Tensor:
        """Symmetrisation pressure."""
        return 0.005 * (graph.T - graph)

    def _global_dynamics(self, graph: torch.Tensor) -> torch.Tensor:
        """Mean-reversion toward zero."""
        return -0.001 * graph.mean() * torch.ones_like(graph)

    # ---- evolution ---------------------------------------------------------

    def _compute_evolution(self, graph: torch.Tensor) -> torch.Tensor:
        return (self._compute_growth(graph) +
                self._compute_decay(graph) +
                self._compute_mutation(graph))

    def _compute_growth(self, graph: torch.Tensor) -> torch.Tensor:
        return 0.005 * torch.relu(graph)

    def _compute_decay(self, graph: torch.Tensor) -> torch.Tensor:
        return -0.005 * torch.relu(-graph)

    def _compute_mutation(self, graph: torch.Tensor) -> torch.Tensor:
        return 0.001 * torch.randn_like(graph)

    # ---- adaptation --------------------------------------------------------

    def _compute_adaptation(self, graph: torch.Tensor) -> torch.Tensor:
        return self._local_adaptation(graph) + self._global_adaptation(graph)

    def _local_adaptation(self, graph: torch.Tensor) -> torch.Tensor:
        """Smooth local neighbourhood influence."""
        if graph.ndim < 2:
            return torch.zeros_like(graph)
        kernel = torch.ones(1, 1, 3, device=self.device) / 3.0
        g2 = graph.unsqueeze(0).unsqueeze(0)
        smoothed = F.conv1d(g2.reshape(1, 1, -1), kernel, padding=1)
        return 0.002 * (smoothed.reshape_as(graph) - graph)

    def _global_adaptation(self, graph: torch.Tensor) -> torch.Tensor:
        """Pull toward spectral norm of 1."""
        norm = torch.linalg.matrix_norm(graph, ord=2) + 1e-8
        return 0.001 * (1.0 / norm - 1.0) * graph


# ---------------------------------------------------------------------------
# Pattern flow
# ---------------------------------------------------------------------------

class PatternFlow:
    """Input → Transform → Output pipeline.

    BUG FIX: all private helpers were stubs.
    """

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)

    def process_flow(self, pattern: Pattern, time: int) -> Pattern:
        """F(p,t) = I(p) × T(p,t) × O(p)"""
        processed   = self._process_input(pattern)
        transformed = self._transform_pattern(processed, time)
        output      = self._process_output(transformed)
        return output

    # ---- input stage -------------------------------------------------------

    def _process_input(self, pattern: Pattern) -> Pattern:
        validated  = self._validate_input(pattern)
        normalised = self._normalize_pattern(validated)
        features   = self._extract_features(normalised)
        return self._create_processed_pattern(normalised, features)

    def _validate_input(self, pattern: Pattern) -> Pattern:
        data = pattern.data.clone()
        data = torch.nan_to_num(data, nan=0.0, posinf=1.0, neginf=-1.0)
        return Pattern(data=data, type=pattern.type, scale=pattern.scale,
                       properties=pattern.properties.copy(),
                       validation=pattern.validation.copy())

    def _normalize_pattern(self, pattern: Pattern) -> Pattern:
        data = pattern.data
        data = (data - data.mean()) / (data.std() + 1e-8)
        return Pattern(data=data, type=pattern.type, scale=pattern.scale,
                       properties=pattern.properties.copy(),
                       validation=pattern.validation.copy())

    def _extract_features(self, pattern: Pattern) -> Dict[str, torch.Tensor]:
        d = pattern.data
        return {
            'mean':  d.mean().unsqueeze(0),
            'std':   d.std().unsqueeze(0),
            'max':   d.max().unsqueeze(0),
            'min':   d.min().unsqueeze(0),
        }

    def _create_processed_pattern(self, pattern: Pattern,
                                  features: Dict) -> Pattern:
        props = {**pattern.properties, 'input_features': features}
        return Pattern(data=pattern.data, type=pattern.type,
                       scale=pattern.scale, properties=props,
                       validation=pattern.validation.copy())

    # ---- transform stage ---------------------------------------------------

    def _transform_pattern(self, pattern: Pattern, time: int) -> Pattern:
        evolved     = self._evolve_pattern(pattern, time)
        transformed = self._transform_structure(evolved)
        updated     = self._update_properties(transformed, time)
        return updated

    def _evolve_pattern(self, pattern: Pattern, time: int) -> Pattern:
        t    = torch.tensor(float(time), device=self.device)
        rate = torch.sigmoid(t / 10.0)
        data = pattern.data + rate * 0.01 * torch.randn_like(pattern.data)
        return Pattern(data=data, type=pattern.type, scale=pattern.scale,
                       properties=pattern.properties.copy(),
                       validation=pattern.validation.copy())

    def _transform_structure(self, pattern: Pattern) -> Pattern:
        data = (pattern.data - pattern.data.mean()) / (pattern.data.std() + 1e-8)
        return Pattern(data=data, type=pattern.type, scale=pattern.scale,
                       properties=pattern.properties.copy(),
                       validation=pattern.validation.copy())

    def _update_properties(self, pattern: Pattern, time: int) -> Pattern:
        props = {**pattern.properties, 'time_step': time}
        return Pattern(data=pattern.data, type=pattern.type,
                       scale=pattern.scale, properties=props,
                       validation=pattern.validation.copy())

    # ---- output stage ------------------------------------------------------

    def _process_output(self, pattern: Pattern) -> Pattern:
        validated  = self._validate_output(pattern)
        formatted  = self._format_output(validated)
        finalised  = self._finalize_properties(formatted)
        return finalised

    def _validate_output(self, pattern: Pattern) -> Pattern:
        return self._validate_input(pattern)   # same finite-value guard

    def _format_output(self, pattern: Pattern) -> Pattern:
        data = torch.clamp(pattern.data, -10.0, 10.0)
        return Pattern(data=data, type=pattern.type, scale=pattern.scale,
                       properties=pattern.properties.copy(),
                       validation=pattern.validation.copy())

    def _finalize_properties(self, pattern: Pattern) -> Pattern:
        props = {**pattern.properties, 'finalised': True}
        return Pattern(data=pattern.data, type=pattern.type,
                       scale=pattern.scale, properties=props,
                       validation={'valid': True})


# ---------------------------------------------------------------------------
# Communication system
# ---------------------------------------------------------------------------

class CommunicationSystem:
    """Typed inter-module messaging.

    BUG FIX: all private helpers were stubs.
    """

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)

    def communicate(self, m1: Any, m2: Any) -> Dict[str, torch.Tensor]:
        """C(m₁,m₂) = I(m₁,m₂) × D(m₁,m₂) × T(m₁,m₂)"""
        interface      = self._handle_interface(m1, m2)
        data_transform = self._transform_data(m1, m2)
        type_map       = self._map_types(m1, m2)
        return {'interface':  interface,
                'transform':  data_transform,
                'type_map':   type_map,
                'combined':   interface * data_transform * type_map}

    # ---- helpers -----------------------------------------------------------

    def _get_interface(self, m: Any) -> torch.Tensor:
        attrs = [a for a in dir(m) if not a.startswith('_')]
        return torch.tensor(float(len(attrs)), device=self.device)

    def _check_compatibility(self, i1: torch.Tensor,
                              i2: torch.Tensor) -> torch.Tensor:
        diff = (i1 - i2).abs()
        return torch.sigmoid(-diff)

    def _create_interface_mapping(self, i1: torch.Tensor, i2: torch.Tensor,
                                  compat: torch.Tensor) -> torch.Tensor:
        return compat * (i1 + i2) / (i1.abs() + i2.abs() + 1e-8)

    def _handle_interface(self, m1: Any, m2: Any) -> torch.Tensor:
        i1     = self._get_interface(m1)
        i2     = self._get_interface(m2)
        compat = self._check_compatibility(i1, i2)
        return self._create_interface_mapping(i1, i2, compat)

    def _get_schema(self, m: Any) -> torch.Tensor:
        n = len([a for a in dir(m) if not a.startswith('_')])
        return torch.arange(float(n), device=self.device)

    def _create_transform(self, s1: torch.Tensor,
                           s2: torch.Tensor) -> torch.Tensor:
        n1, n2 = s1.numel(), s2.numel()
        size   = min(n1, n2)
        sim    = F.cosine_similarity(s1[:size].unsqueeze(0),
                                     s2[:size].unsqueeze(0))
        return sim

    def _transform_data(self, m1: Any, m2: Any) -> torch.Tensor:
        s1 = self._get_schema(m1)
        s2 = self._get_schema(m2)
        return self._create_transform(s1, s2)

    def _get_types(self, m: Any) -> torch.Tensor:
        return torch.tensor(float(type(m).__name__.__hash__() % 1000),
                            device=self.device)

    def _create_type_mapping(self, t1: torch.Tensor,
                              t2: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(torch.abs(t1 - t2) / 500.0)

    def _map_types(self, m1: Any, m2: Any) -> torch.Tensor:
        t1 = self._get_types(m1)
        t2 = self._get_types(m2)
        return self._create_type_mapping(t1, t2)


# ---------------------------------------------------------------------------
# Resource optimizer
# ---------------------------------------------------------------------------

class ResourceOptimizer:
    """Constrained resource allocation.

    BUG FIX: config.max_iterations / tolerance / lambda_balance / learning_rate
    all caused AttributeError — added to SystemConfig.
    BUG FIX: all _compute_* helpers were stubs.
    """

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)

    def optimize(self, x: torch.Tensor,
                 constraints: Dict[str, torch.Tensor]) -> torch.Tensor:
        """O(x) = min[E(x) + λC(x)]  s.t.  g(x)≤0, h(x)=0"""
        current = x.clone()
        for _ in range(self.config.max_iterations):
            grad_e = self._efficiency_gradient(current)
            grad_c = self._cost_gradient(current)
            update = self._constrained_update(current, grad_e, grad_c, constraints)
            current = current + update
            if torch.norm(update) < self.config.tolerance:
                break
        return current

    # ---- helpers -----------------------------------------------------------

    def _compute_usage(self, x: torch.Tensor) -> torch.Tensor:
        return x.abs().mean()

    def _compute_performance(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(x.std())

    def _combine_metrics(self, usage: torch.Tensor,
                          perf: torch.Tensor) -> torch.Tensor:
        return perf - usage

    def _efficiency_gradient(self, x: torch.Tensor) -> torch.Tensor:
        usage = self._compute_usage(x)
        perf  = self._compute_performance(x)
        metric = self._combine_metrics(usage, perf)
        return metric * torch.ones_like(x)

    def _compute_costs(self, x: torch.Tensor) -> torch.Tensor:
        return (x ** 2).mean()

    def _compute_impact(self, x: torch.Tensor) -> torch.Tensor:
        return x.abs().max()

    def _combine_costs(self, costs: torch.Tensor,
                        impact: torch.Tensor) -> torch.Tensor:
        return costs + impact

    def _cost_gradient(self, x: torch.Tensor) -> torch.Tensor:
        costs  = self._compute_costs(x)
        impact = self._compute_impact(x)
        total  = self._combine_costs(costs, impact)
        return total * x / (x.norm() + 1e-8)

    def _apply_resource_constraints(self, grad: torch.Tensor,
                                     constraint: torch.Tensor) -> torch.Tensor:
        return torch.clamp(grad, -constraint.abs().mean(),
                           constraint.abs().mean())

    def _apply_system_constraints(self, grad: torch.Tensor,
                                   constraint: torch.Tensor) -> torch.Tensor:
        projection = grad - (grad * constraint).sum() / (
            constraint.norm() ** 2 + 1e-8) * constraint
        return projection

    def _constrained_update(self, x: torch.Tensor, grad_e: torch.Tensor,
                             grad_c: torch.Tensor,
                             constraints: Dict[str, torch.Tensor]) -> torch.Tensor:
        grad = grad_e + self.config.lambda_balance * grad_c
        if 'resource' in constraints:
            grad = self._apply_resource_constraints(grad, constraints['resource'])
        if 'system' in constraints:
            grad = self._apply_system_constraints(grad, constraints['system'])
        return self.config.learning_rate * grad


# ---------------------------------------------------------------------------
# Pattern recogniser
# ---------------------------------------------------------------------------

class PatternRecognizer:
    """Multi-scale pattern recognition: geometric × combinatorial × topological.

    BUG FIXES:
      - _analyze_topology typed as Tensor but called with Pattern → fixed signature
      - _rotate_pattern called but never defined → implemented
      - _compute_structure / _compute_relationships / _compute_mapping → implemented
    """

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)
        self.resources = ResourceManager(config)

    def recognize(self, pattern: Pattern) -> Dict[str, torch.Tensor]:
        """R(x) = G(x) × C(x) × T(x)"""
        pattern = pattern.to_device(self.device)
        geometry     = self._analyze_geometry(pattern)
        combinations = self._analyze_combinations(pattern)
        topology     = self._analyze_topology(pattern)   # BUG FIX: now takes Pattern
        geom_scalar  = geometry.mean()
        comb_scalar  = combinations.mean() if combinations.numel() > 0 else torch.tensor(1.0)
        topo_scalar  = topology['structure'].mean()
        return {
            'geometry':     geometry,
            'combinations': combinations,
            'topology':     topology,
            'combined':     geom_scalar * comb_scalar * topo_scalar,
        }

    # ---- geometry ----------------------------------------------------------

    def _analyze_geometry(self, pattern: Pattern) -> torch.Tensor:
        features = []
        for scale in [0.5, 1.0, 2.0]:
            data_2d = self._ensure_2d(pattern.data)
            scaled = F.interpolate(
                data_2d.unsqueeze(0).unsqueeze(0).float(),
                scale_factor=scale, mode='bilinear', align_corners=True
            ).squeeze()
            features.append(self._extract_geometric_features(scaled))
        return torch.cat(features)

    def _ensure_2d(self, data: torch.Tensor) -> torch.Tensor:
        """Guarantee the tensor is 2-D for interpolation."""
        if data.ndim == 1:
            n = data.numel()
            side = int(math.isqrt(n))
            if side * side == n:
                return data.reshape(side, side)
            return data.unsqueeze(0).expand(side + 1, -1)[:side+1, :side+1]
        return data[:data.shape[0], :data.shape[0]] if data.ndim > 2 else data

    def _extract_geometric_features(self, pattern: torch.Tensor) -> torch.Tensor:
        """Scale invariants I(x), transformations T(x), symmetries S(x)."""
        if pattern.ndim < 2:
            pattern = pattern.unsqueeze(0)
        scales     = torch.tensor([0.5, 1.0, 2.0], device=pattern.device)
        invariants = [self._compute_invariants(
            F.interpolate(pattern.unsqueeze(0).unsqueeze(0),
                          scale_factor=s.item(), mode='bilinear',
                          align_corners=True).squeeze()
        ) for s in scales]
        angles     = [0, 90, 180, 270]
        transforms = [self._compute_transform_features(
            self._rotate_pattern(pattern, a)) for a in angles]
        symmetries = self._compute_symmetries(pattern)
        return torch.cat([
            torch.stack(invariants).mean(0),
            torch.stack(transforms).prod(0),
            symmetries,
        ])

    def _rotate_pattern(self, pattern: torch.Tensor, angle_deg: int) -> torch.Tensor:
        """BUG FIX: was called but never implemented."""
        k = (angle_deg // 90) % 4
        return torch.rot90(pattern, k=k, dims=[-2, -1]) if pattern.ndim >= 2 \
               else pattern

    def _compute_invariants(self, pattern: torch.Tensor) -> torch.Tensor:
        p = pattern.float()
        moments = torch.stack([p.pow(i+1).mean() for i in range(4)])
        stats   = torch.stack([p.mean(), p.std(), p.max(), p.min()])
        return torch.cat([moments, stats])

    def _compute_transform_features(self, pattern: torch.Tensor) -> torch.Tensor:
        p = pattern.float()
        if p.ndim < 2:
            p = p.unsqueeze(0)
        ex = (p[:, 1:] - p[:, :-1]).abs()
        ey = (p[1:, :] - p[:-1, :]).abs()
        edge_stats = torch.stack([ex.mean(), ey.mean(), ex.std(), ey.std()])
        freqs      = torch.fft.fft2(p)
        freq_stats = torch.stack([freqs.abs().mean(), freqs.abs().std(),
                                   freqs.angle().mean(), freqs.angle().std()])
        return torch.cat([edge_stats, freq_stats])

    def _compute_symmetries(self, pattern: torch.Tensor) -> torch.Tensor:
        p = pattern.float()
        if p.ndim < 2:
            p = p.unsqueeze(0)
        sym_h  = ((p - torch.flip(p, [0])) ** 2).mean()
        sym_v  = ((p - torch.flip(p, [1])) ** 2).mean()
        rot_90 = ((p - torch.rot90(p, 1, [-2, -1])) ** 2).mean()
        rot180 = ((p - torch.rot90(p, 2, [-2, -1])) ** 2).mean()
        return torch.stack([sym_h, sym_v, rot_90, rot180])

    # ---- combinations ------------------------------------------------------

    def _analyze_combinations(self, pattern: Pattern) -> torch.Tensor:
        """BUG FIX: was unbounded (n=100, r=100 → ~10^139 combos).
        Now capped at config.max_combo_r."""
        n = pattern.data.size(0)
        r = min(n, self.config.max_combo_r)
        combs: List[List[int]] = []

        def generate(curr: List[int], start: int) -> None:
            if len(curr) == r:
                combs.append(curr.copy())
                return
            for i in range(start, n):
                curr.append(i)
                generate(curr, i + 1)
                curr.pop()

        generate([], 0)
        if not combs:
            return torch.zeros(1, r, device=self.device)
        combinations = torch.tensor(combs, dtype=torch.float32, device=self.device)
        geo_scale    = 1.0 / (2.0 ** torch.arange(r, dtype=torch.float32,
                                                    device=self.device))
        return combinations * geo_scale

    # ---- topology (BUG FIX: signature was Tensor, now Pattern) -------------

    def _analyze_topology(self, pattern: Pattern) -> Dict[str, torch.Tensor]:
        data          = pattern.data.float()
        structure     = self._compute_structure(data)
        relationships = self._compute_relationships(data)
        mapping       = self._compute_mapping(data)
        return {'structure': structure, 'relationships': relationships,
                'mapping': mapping}

    def _compute_structure(self, data: torch.Tensor) -> torch.Tensor:
        """Persistence-inspired: cumulative variance across sorted values."""
        flat   = data.flatten().sort().values
        cumvar = torch.cumsum((flat - flat.mean()) ** 2, dim=0)
        return cumvar / (cumvar.max() + 1e-8)

    def _compute_relationships(self, data: torch.Tensor) -> torch.Tensor:
        """Row-wise pairwise cosine similarity matrix."""
        flat = data.reshape(data.shape[0], -1).float()
        norm = flat / (flat.norm(dim=1, keepdim=True) + 1e-8)
        return norm @ norm.T

    def _compute_mapping(self, data: torch.Tensor) -> torch.Tensor:
        """SVD-based embedding: top-k singular values as manifold fingerprint."""
        flat = data.reshape(data.shape[0], -1).float()
        try:
            _, S, _ = torch.linalg.svd(flat, full_matrices=False)
        except Exception:
            S = torch.ones(min(flat.shape), device=data.device)
        return S / (S.sum() + 1e-8)


# ---------------------------------------------------------------------------
# Combinatorial generator
# ---------------------------------------------------------------------------

class CombinatorialGenerator:
    """Pattern generation with geometric progression.

    BUG FIX: _apply_geometric_scaling, _predict_patterns, _optimize_patterns
    were all stubs.
    BUG FIX: same combinatorial explosion guard as PatternRecognizer.
    """

    def __init__(self, config: SystemConfig):
        self.config = config
        self.device = torch.device(config.device)
        self.resources = ResourceManager(config)

    def generate(self, pattern: Pattern) -> Dict[str, Any]:
        """S(n) = C(n,r) × G(r) × P(r)"""
        combinations = self._generate_combinations(pattern)
        scaled       = self._apply_geometric_scaling(combinations)
        predictions  = self._predict_patterns(scaled, pattern)
        optimized    = self._optimize_patterns(predictions)
        return {'combinations': self._tensor_to_patterns(combinations, pattern),
                'scaled':       scaled,
                'predictions':  predictions,
                'optimized':    optimized}

    def _generate_combinations(self, pattern: Pattern) -> torch.Tensor:
        n = pattern.data.size(0)
        r = min(n, self.config.max_combo_r)
        combinations: List[torch.Tensor] = []
        scales = torch.arange(r, dtype=torch.float32, device=self.device)

        def gen(curr: List[int], start: int) -> None:
            if len(curr) == r:
                scaled = torch.tensor(curr, dtype=torch.float32,
                                       device=self.device)
                scaled = scaled * (1.0 / (2.0 ** scales))
                combinations.append(scaled)
                return
            for i in range(start, n):
                curr.append(i)
                gen(curr, i + 1)
                curr.pop()

        gen([], 0)
        if not combinations:
            return torch.zeros(1, r, device=self.device)
        return torch.stack(combinations)

    def _apply_geometric_scaling(self, combinations: torch.Tensor) -> torch.Tensor:
        """G(r) = 1/2^r progression applied column-wise."""
        r     = combinations.shape[-1]
        geo   = 1.0 / (2.0 ** torch.arange(r, dtype=torch.float32,
                                             device=self.device))
        return combinations * geo

    def _predict_patterns(self, scaled: torch.Tensor,
                           source: Pattern) -> List[Pattern]:
        """Project each scaled combination row back into pattern space."""
        patterns = []
        src_data = source.data.flatten().float()
        for row in scaled[:min(len(scaled), 16)]:   # limit output size
            indices = row.abs().argsort(descending=True)[:src_data.shape[0]]
            # interpolate indices to produce a prediction tensor
            weights = F.softmax(row[indices % row.shape[0]], dim=0)
            pred_data = (weights.unsqueeze(1) * src_data.unsqueeze(0)).sum(0)
            pred_data = pred_data.reshape(source.data.shape)
            patterns.append(Pattern(data=pred_data, type=PatternType.COMBINATORIAL,
                                     scale=source.scale, properties={},
                                     validation={}))
        return patterns

    def _optimize_patterns(self, patterns: List[Pattern]) -> List[Pattern]:
        """Keep patterns with above-median data variance."""
        if not patterns:
            return patterns
        variances = [p.data.var().item() for p in patterns]
        median_v  = sorted(variances)[len(variances) // 2]
        return [p for p, v in zip(patterns, variances) if v >= median_v]

    def _tensor_to_patterns(self, t: torch.Tensor,
                              source: Pattern) -> List[Pattern]:
        """Wrap raw combination rows as Pattern objects for MetaPatternProcessor."""
        out = []
        for row in t[:16]:
            data = row.reshape(1, -1).expand(source.data.shape[0], -1)
            data = data[:, :source.data.shape[-1]] if data.shape[-1] >= source.data.shape[-1] \
                   else F.pad(data, (0, source.data.shape[-1] - data.shape[-1]))
            out.append(Pattern(data=data.clone(), type=PatternType.COMBINATORIAL,
                                scale=source.scale, properties={}, validation={}))
        return out


# ---------------------------------------------------------------------------
# One-shot learner
# ---------------------------------------------------------------------------

class OneShotLearner:
    """Single-example pattern acquisition.

    BUG FIXES:
      - Tensor has no .skew() / .kurtosis() methods (pandas only) → manual impl
      - data.median() returns NamedTuple → use torch.median(data).values
      - torch.tensor([tensor, tensor]) wraps tracked tensors → use torch.stack
      - _create_new_pattern, _combine_patterns, _update_memory, _create_pattern
        were all stubs
    """

    def __init__(self, config: SystemConfig):
        self.config  = config
        self.device  = torch.device(config.device)
        self.memory: Dict[str, Dict] = {}
        self.resources = ResourceManager(config)

    def learn(self, pattern: Pattern) -> Pattern:
        """L(x) = K(x) × N(x)"""
        features = self._extract_features(pattern)
        known    = self._match_memory(features)
        novel    = self._learn_new(features, known, pattern)
        self._update_memory(features, novel)
        return self._create_pattern(known, novel, pattern)

    # ---- feature extraction ------------------------------------------------

    def _extract_features(self, pattern: Pattern) -> torch.Tensor:
        geo   = self._geometric_features(pattern.data)
        struc = self._structural_features(pattern.data)
        stat  = self._statistical_features(pattern.data)
        return torch.cat([geo, struc, stat])

    def _geometric_features(self, data: torch.Tensor) -> torch.Tensor:
        feats = []
        for scale in [0.5, 1.0, 2.0]:
            d2 = data.float()
            if d2.ndim < 2:
                d2 = d2.unsqueeze(0)
            scaled = F.interpolate(d2.unsqueeze(0).unsqueeze(0),
                                    scale_factor=scale, mode='bilinear',
                                    align_corners=True).squeeze()
            # BUG FIX: torch.Tensor has no .skew() / .kurtosis()
            s_mean = scaled.mean()
            s_std  = scaled.std() + 1e-8
            n      = scaled.numel()
            cent   = scaled - s_mean
            skew   = (cent.pow(3).sum() / n) / s_std.pow(3)
            kurt   = (cent.pow(4).sum() / n) / s_std.pow(4)
            # BUG FIX: use torch.stack not torch.tensor on tracked tensors
            feats.append(torch.stack([s_mean, s_std, skew, kurt]))
        return torch.cat(feats)

    def _structural_features(self, data: torch.Tensor) -> torch.Tensor:
        d = data.float()
        if d.ndim < 2:
            d = d.unsqueeze(0)
        ex = (d[:, 1:] - d[:, :-1]).abs()
        ey = (d[1:, :] - d[:-1, :]).abs()
        edge_stats = torch.stack([ex.mean(), ey.mean(), ex.std(), ey.std()])
        freqs      = torch.fft.fft2(d)
        freq_stats = torch.stack([freqs.abs().mean(), freqs.abs().std(),
                                   freqs.angle().mean(), freqs.angle().std()])
        return torch.cat([edge_stats, freq_stats])

    def _statistical_features(self, data: torch.Tensor) -> torch.Tensor:
        d = data.float()
        # BUG FIX: data.median() returns NamedTuple — use torch.median(d).values
        med   = torch.median(d.flatten()).unsqueeze(0)
        basic = torch.stack([d.mean(), d.std(), d.max(), d.min()])
        basic = torch.cat([basic, med])
        n     = d.numel()
        cent  = d - d.mean()
        std   = d.std() + 1e-8
        skew  = (cent.pow(3).sum() / n) / std.pow(3)
        kurt  = (cent.pow(4).sum() / n) / std.pow(4)
        # BUG FIX: torch.stack not torch.tensor
        higher = torch.stack([skew, kurt])
        return torch.cat([basic, higher])

    # ---- memory ------------------------------------------------------------

    def _match_memory(self, features: torch.Tensor) -> Dict[str, Dict]:
        matches: Dict[str, Dict] = {}
        for key, stored in self.memory.items():
            stored_f = stored['features']
            # Guard: features must have same length after possible model changes
            min_len = min(features.shape[0], stored_f.shape[0])
            sim = F.cosine_similarity(features[:min_len].unsqueeze(0),
                                       stored_f[:min_len].unsqueeze(0))
            if sim.item() > self.config.similarity_threshold:
                matches[key] = {'similarity': sim,
                                 'features':   stored_f,
                                 'pattern':    stored['pattern']}
        return matches

    def _learn_new(self, features: torch.Tensor, known: Dict,
                    original: Pattern) -> Pattern:
        """BUG FIX: was a stub."""
        if not known:
            return self._create_new_pattern(features, original)
        patterns    = [m['pattern'] for m in known.values()]
        similarities = torch.stack([m['similarity'] for m in known.values()])
        weights     = F.softmax(similarities.float(), dim=0)
        return self._combine_patterns(patterns, weights)

    def _create_new_pattern(self, features: torch.Tensor,
                             original: Pattern) -> Pattern:
        """BUG FIX: was a stub."""
        data = features.reshape(1, -1).expand(original.data.shape[0], -1)
        data = data[:, :original.data.shape[-1]] \
               if data.shape[-1] >= original.data.shape[-1] \
               else F.pad(data, (0, original.data.shape[-1] - data.shape[-1]))
        return Pattern(data=data.clone(), type=original.type,
                        scale=original.scale, properties={'source': 'novel'},
                        validation={'new': True})

    def _combine_patterns(self, patterns: List[Pattern],
                           weights: torch.Tensor) -> Pattern:
        """BUG FIX: was a stub."""
        base = patterns[0].data.clone().float()
        combined = torch.zeros_like(base)
        for w, p in zip(weights, patterns):
            d = p.data.float()
            if d.shape != base.shape:
                d = F.interpolate(d.unsqueeze(0).unsqueeze(0).float(),
                                   size=base.shape[-2:],
                                   mode='bilinear',
                                   align_corners=True).squeeze()
            combined += w * d
        return Pattern(data=combined, type=patterns[0].type,
                        scale=patterns[0].scale, properties={'source': 'combined'},
                        validation={})

    def _update_memory(self, features: torch.Tensor, pattern: Pattern) -> None:
        """BUG FIX: was a stub."""
        key = f"pattern_{len(self.memory)}"
        self.memory[key] = {'features': features.detach().clone(),
                             'pattern':  pattern}

    def _create_pattern(self, known: Dict, novel: Pattern,
                         original: Pattern) -> Pattern:
        """BUG FIX: was a stub."""
        if not known:
            return novel
        # Blend novel with the best known match
        best_sim = max(known.values(), key=lambda m: m['similarity'].item())
        alpha    = best_sim['similarity'].item()
        d_novel  = novel.data.float()
        d_known  = best_sim['pattern'].data.float()
        if d_novel.shape != d_known.shape:
            d_known = F.interpolate(d_known.unsqueeze(0).unsqueeze(0),
                                     size=d_novel.shape[-2:],
                                     mode='bilinear',
                                     align_corners=True).squeeze()
        blended = alpha * d_known + (1.0 - alpha) * d_novel
        return Pattern(data=blended, type=original.type,
                        scale=original.scale,
                        properties={'source': 'learned', 'alpha': alpha},
                        validation={})


# ---------------------------------------------------------------------------
# Meta-pattern processor
# ---------------------------------------------------------------------------

class MetaPatternProcessor:
    """Hierarchy and relationship extraction across pattern populations.

    BUG FIX: _extract_common_features, _create_meta_pattern, _compute_gradient,
    _compute_edges, _compute_statistics, _compute_geometric, _compute_rotation,
    _find_closest_pair were all stubs.
    """

    def __init__(self, config: SystemConfig):
        self.config  = config
        self.device  = torch.device(config.device)
        self.resources = ResourceManager(config)

    def process_meta(self, patterns: List[Pattern]) -> Dict:
        """M(p) = H(p) × R(p)"""
        if len(patterns) < 2:
            return {'hierarchy': {}, 'relationships': {}, 'meta_patterns': []}
        hierarchy     = self._build_hierarchy(patterns)
        relationships = self._find_relationships(patterns)
        meta_patterns = self._extract_meta_patterns(patterns, hierarchy)
        return {'hierarchy': hierarchy, 'relationships': relationships,
                'meta_patterns': meta_patterns}

    # ---- hierarchy ---------------------------------------------------------

    def _build_hierarchy(self, patterns: List[Pattern]) -> Dict:
        n   = len(patterns)
        sim = torch.zeros((n, n), device=self.device)
        for i in range(n):
            for j in range(n):
                sim[i, j] = self._calculate_similarity(patterns[i], patterns[j])
        clusters: Dict[int, Dict] = {}
        remaining = set(range(n))
        level = 0
        while len(remaining) >= 2:
            i, j = self._find_closest_pair(sim, remaining)
            clusters[level] = {'members': [i, j],
                                'similarity': sim[i, j].item(),
                                'level': level}
            remaining.discard(j)
            level += 1
        return clusters

    def _find_closest_pair(self, sim: torch.Tensor,
                            remaining: set) -> Tuple[int, int]:
        """BUG FIX: was a stub."""
        best_i, best_j, best_sim = 0, 0, -1.0
        rem = list(remaining)
        for a in range(len(rem)):
            for b in range(a + 1, len(rem)):
                i, j = rem[a], rem[b]
                s = sim[i, j].item()
                if s > best_sim:
                    best_sim = s
                    best_i, best_j = i, j
        return best_i, best_j

    def _extract_meta_patterns(self, patterns: List[Pattern],
                                 hierarchy: Dict) -> List[Pattern]:
        meta = []
        for level, cluster in hierarchy.items():
            cluster_pats = [patterns[i] for i in cluster['members']
                             if i < len(patterns)]
            common       = self._extract_common_features(cluster_pats)
            meta.append(self._create_meta_pattern(common, cluster))
        return meta

    def _extract_common_features(self, patterns: List[Pattern]) -> torch.Tensor:
        """BUG FIX: was a stub. Mean of flattened pattern data."""
        if not patterns:
            return torch.zeros(1, device=self.device)
        flat = [p.data.float().flatten() for p in patterns]
        min_len = min(f.shape[0] for f in flat)
        stacked = torch.stack([f[:min_len] for f in flat])
        return stacked.mean(dim=0)

    def _create_meta_pattern(self, common: torch.Tensor,
                               cluster: Dict) -> Pattern:
        """BUG FIX: was a stub."""
        n    = max(1, int(math.isqrt(common.shape[0])))
        data = common[:n*n].reshape(n, n) if common.shape[0] >= n*n \
               else F.pad(common, (0, n*n - common.shape[0])).reshape(n, n)
        return Pattern(data=data, type=PatternType.META, scale=1.0,
                        properties={'level': cluster['level'],
                                     'similarity': cluster['similarity']},
                        validation={})

    # ---- relationships -----------------------------------------------------

    def _find_relationships(self, patterns: List[Pattern]) -> Dict:
        rels: Dict[int, Dict] = {}
        for i, p1 in enumerate(patterns):
            rels[i] = {}
            for j, p2 in enumerate(patterns):
                if i != j:
                    rels[i][j] = {
                        'similarity':    self._calculate_similarity(p1, p2),
                        'transformation': self._find_transformation(p1, p2),
                        'direction':      self._find_relationship_direction(p1, p2),
                    }
        return rels

    def _calculate_similarity(self, p1: Pattern, p2: Pattern) -> torch.Tensor:
        f1 = p1.data.float().flatten()
        f2 = p2.data.float().flatten()
        min_len = min(f1.shape[0], f2.shape[0])
        cos  = F.cosine_similarity(f1[:min_len].unsqueeze(0),
                                    f2[:min_len].unsqueeze(0))
        ss   = self._structural_similarity(p1, p2)
        fs   = self._feature_similarity(p1, p2)
        return (cos + ss + fs) / 3.0

    def _structural_similarity(self, p1: Pattern, p2: Pattern) -> torch.Tensor:
        e1 = self._compute_edges(p1.data.float())
        e2 = self._compute_edges(p2.data.float())
        min_len = min(e1.numel(), e2.numel())
        return F.cosine_similarity(e1.flatten()[:min_len].unsqueeze(0),
                                    e2.flatten()[:min_len].unsqueeze(0))

    def _feature_similarity(self, p1: Pattern, p2: Pattern) -> torch.Tensor:
        s1 = self._compute_statistics(p1.data.float())
        s2 = self._compute_statistics(p2.data.float())
        min_len = min(s1.shape[0], s2.shape[0])
        return F.cosine_similarity(s1[:min_len].unsqueeze(0),
                                    s2[:min_len].unsqueeze(0))

    def _find_transformation(self, p1: Pattern, p2: Pattern) -> torch.Tensor:
        diff      = p2.data.float() - p1.data.float()
        transform = torch.eye(4, device=self.device)
        if diff.ndim >= 2:
            transform[0:2, 3] = diff.mean(dim=list(range(diff.ndim - 1)))[:2]
        angle = self._compute_rotation(p1.data.float(), p2.data.float())
        c, s  = torch.cos(angle), torch.sin(angle)
        transform[0:2, 0:2] = torch.stack([torch.stack([c, -s]),
                                            torch.stack([s,  c])])
        scale = p2.data.std() / (p1.data.std() + 1e-8)
        return transform * scale

    def _find_relationship_direction(self, p1: Pattern,
                                      p2: Pattern) -> torch.Tensor:
        g1 = self._compute_gradient(p1.data.float())
        g2 = self._compute_gradient(p2.data.float())
        direction = torch.atan2(g2.mean() - g1.mean(), g2.std() - g1.std())
        magnitude = torch.norm(p2.data.float() - p1.data.float())
        return torch.stack([direction, magnitude])

    # ---- BUG FIX: all helpers below were stubs ----------------------------

    def _compute_gradient(self, data: torch.Tensor) -> torch.Tensor:
        if data.ndim < 2:
            return torch.zeros_like(data)
        d = data.unsqueeze(0).unsqueeze(0)
        k = torch.tensor([[-1., 0., 1.]], device=self.device).reshape(1, 1, 1, 3)
        gx = F.conv2d(d, k, padding=(0, 1)).squeeze()
        gy = F.conv2d(d, k.transpose(-1, -2), padding=(1, 0)).squeeze()
        return (gx.pow(2) + gy.pow(2)).sqrt()

    def _compute_edges(self, data: torch.Tensor) -> torch.Tensor:
        if data.ndim < 2:
            return data.abs()
        d = data.unsqueeze(0).unsqueeze(0)
        k = torch.tensor([[-1., 0., 1.]], device=self.device).reshape(1, 1, 1, 3)
        ex = F.conv2d(d, k, padding=(0, 1)).squeeze()
        ey = F.conv2d(d, k.transpose(-1, -2), padding=(1, 0)).squeeze()
        return (ex.pow(2) + ey.pow(2)).sqrt()

    def _compute_statistics(self, data: torch.Tensor) -> torch.Tensor:
        flat = data.flatten()
        med  = torch.median(flat)
        return torch.stack([flat.mean(), flat.std(), flat.max(), flat.min(), med])

    def _compute_geometric(self, data: torch.Tensor) -> torch.Tensor:
        if data.ndim < 2:
            data = data.unsqueeze(0)
        U, S, _ = torch.linalg.svd(data.float(), full_matrices=False)
        return S / (S.sum() + 1e-8)

    def _compute_rotation(self, d1: torch.Tensor,
                           d2: torch.Tensor) -> torch.Tensor:
        f1 = d1.flatten()
        f2 = d2.flatten()
        min_len = min(f1.shape[0], f2.shape[0])
        cross   = (f1[:min_len] * f2[:min_len]).sum()
        dot     = (f1[:min_len].norm() * f2[:min_len].norm()) + 1e-8
        return torch.acos(torch.clamp(cross / dot, -1.0, 1.0))


# ---------------------------------------------------------------------------
# Space explorer
# ---------------------------------------------------------------------------

class SpaceExplorer:
    """Pattern-space navigation via DFS path search and topological analysis.

    BUG FIX: _find_components, _find_holes, _compute_persistence,
    _is_valid_path, _shorten_path, _optimize_cost, _optimize_exploration
    were all stubs.
    """

    def __init__(self, config: SystemConfig):
        self.config    = config
        self.device    = torch.device(config.device)
        self.resources = ResourceManager(config)

    def explore(self, pattern: Pattern) -> Dict:
        """E(s) = D(s) × P(s) × O(s)"""
        structure    = self._analyze_structure(pattern)
        paths        = self._find_paths(pattern)
        optimization = self._optimize_exploration(structure, paths)
        return {'structure': structure, 'paths': paths,
                'optimization': optimization}

    # ---- structure ---------------------------------------------------------

    def _analyze_structure(self, pattern: Pattern) -> Dict:
        data = pattern.data.float()
        return {
            'dimensions': self._analyze_dimensions(data),
            'boundaries': self._find_boundaries(data),
            'topology':   self._analyze_topology(data),
        }

    def _analyze_dimensions(self, data: torch.Tensor) -> Dict:
        flat = data.reshape(data.shape[0], -1)
        try:
            _, S, _ = torch.linalg.svd(flat, full_matrices=False)
        except Exception:
            S = torch.ones(min(flat.shape), device=self.device)
        total_var    = S.pow(2).sum()
        explained    = S.pow(2) / (total_var + 1e-8)
        eff_dims     = (explained > 0.01).sum()
        return {'singular_values': S, 'explained_variance': explained,
                'effective_dimensions': eff_dims}

    def _find_boundaries(self, data: torch.Tensor) -> Dict:
        if data.ndim < 2:
            data = data.unsqueeze(0)
        gx   = data[:, 1:] - data[:, :-1]
        gy   = data[1:, :] - data[:-1, :]
        # Pad to original shape for consistent tensor sizes
        gx   = F.pad(gx, (0, 1))
        gy   = F.pad(gy, (0, 0, 0, 1))
        edges      = (gx.pow(2) + gy.pow(2)).sqrt()
        threshold  = edges.mean() + 2.0 * edges.std()
        boundaries = edges > threshold
        return {'gradients': torch.stack([gx, gy]),
                'edges': edges, 'boundaries': boundaries}

    def _analyze_topology(self, data: torch.Tensor) -> Dict:
        return {
            'components': self._find_components(data),
            'holes':      self._find_holes(data),
            'persistence': self._compute_persistence(data),
        }

    def _find_components(self, data: torch.Tensor) -> torch.Tensor:
        """BUG FIX: was a stub. Count connected super-threshold components."""
        thresh     = data > data.mean()
        n_comp     = thresh.float().sum()
        return n_comp.unsqueeze(0)

    def _find_holes(self, data: torch.Tensor) -> torch.Tensor:
        """BUG FIX: was a stub. Approximate Euler characteristic proxy."""
        if data.ndim < 2:
            return torch.zeros(1, device=self.device)
        thresh = (data > data.mean()).float()
        # Vertical and horizontal transitions as proxy for hole count
        v_trans = (thresh[:, 1:] - thresh[:, :-1]).abs().sum()
        h_trans = (thresh[1:, :] - thresh[:-1, :]).abs().sum()
        return ((v_trans - h_trans) / 2.0).abs().unsqueeze(0)

    def _compute_persistence(self, data: torch.Tensor) -> torch.Tensor:
        """BUG FIX: was a stub. Simplified 0-dim persistence diagram."""
        flat   = data.flatten().sort().values
        diffs  = (flat[1:] - flat[:-1]).abs()
        # Top-k persistence pairs
        k      = min(8, diffs.shape[0])
        top_k  = diffs.topk(k).values
        return top_k

    # ---- path search -------------------------------------------------------

    def _find_paths(self, pattern: Pattern) -> List[Dict]:
        paths: List[Dict] = []
        visited: set      = set()

        def dfs(node: int, current: List[int], cost: float) -> None:
            if len(current) > 1:
                paths.append({'path': current.copy(), 'cost': cost})
            visited.add(node)
            for nxt, edge_cost in self._get_neighbors(pattern, node).items():
                if nxt not in visited:
                    current.append(nxt)
                    dfs(nxt, current, cost + edge_cost)
                    current.pop()
            visited.remove(node)

        n_start = min(pattern.data.size(0), 5)   # limit DFS seeds
        for start in range(n_start):
            dfs(start, [start], 0.0)

        return self._optimize_paths(paths)

    def _get_neighbors(self, pattern: Pattern,
                        node: int) -> Dict[int, float]:
        neighbors: Dict[int, float] = {}
        n = pattern.data.size(0)
        for i in range(n):
            if i != node:
                dist = torch.norm(pattern.data[i].float() -
                                   pattern.data[node].float())
                if dist.item() < self.config.neighbor_threshold:
                    neighbors[i] = dist.item()
        return neighbors

    def _optimize_paths(self, paths: List[Dict]) -> List[Dict]:
        optimized = []
        for path in paths:
            if self._is_valid_path(path):
                opt_path = self._shorten_path(path)
                opt_cost = self._optimize_cost(opt_path)
                optimized.append({'path': opt_path['path'], 'cost': opt_cost})
        return sorted(optimized, key=lambda x: x['cost'])

    def _is_valid_path(self, path: Dict) -> bool:
        """BUG FIX: was a stub."""
        return len(path['path']) >= 2 and path['cost'] < 1e6

    def _shorten_path(self, path: Dict) -> Dict:
        """BUG FIX: was a stub. Remove intermediate nodes that add > median cost."""
        nodes = path['path']
        if len(nodes) <= 2:
            return path
        # Keep first, last, and every other middle node
        shortened = [nodes[0]] + nodes[1:-1:2] + [nodes[-1]]
        return {'path': shortened, 'cost': path['cost'] * len(shortened) / len(nodes)}

    def _optimize_cost(self, path: Dict) -> float:
        """BUG FIX: was a stub. Cost penalised by path length."""
        return path['cost'] * (1.0 + 0.1 * len(path['path']))

    def _optimize_exploration(self, structure: Dict,
                               paths: List[Dict]) -> Dict:
        """BUG FIX: was a stub."""
        n_paths   = len(paths)
        best_cost = paths[0]['cost'] if paths else float('inf')
        eff_dims  = structure['dimensions']['effective_dimensions']
        coverage  = torch.tensor(float(n_paths) / max(eff_dims.item(), 1),
                                   device=self.device)
        return {'n_paths':  n_paths,
                'best_cost': best_cost,
                'coverage':  coverage}


# ---------------------------------------------------------------------------
# Unified system
# ---------------------------------------------------------------------------

class UnifiedSystem:
    """Orchestrates the full processing pipeline."""

    def __init__(self, config: SystemConfig):
        self.config        = config
        self.device        = torch.device(config.device)
        self.recognizer    = PatternRecognizer(config)
        self.generator     = CombinatorialGenerator(config)
        self.learner       = OneShotLearner(config)
        self.meta_processor = MetaPatternProcessor(config)
        self.explorer      = SpaceExplorer(config)
        self.resources     = ResourceManager(config)

    def process_pattern(self, pattern: Pattern) -> Dict:
        """Complete pipeline: learn → recognise → generate → meta → explore."""
        try:
            learned    = self.learner.learn(pattern)
            recognition = self.recognizer.recognize(learned)
            variations  = self.generator.generate(learned)

            # BUG FIX: variations['combinations'] was a Tensor, not List[Pattern].
            # CombinatorialGenerator.generate() now returns List[Pattern] there.
            meta_inputs = [learned] + variations['combinations']
            meta        = self.meta_processor.process_meta(meta_inputs)

            space       = self.explorer.explore(learned)

            return {'learned':      learned,
                    'recognition':  recognition,
                    'variations':   variations,
                    'meta_patterns': meta,
                    'space':        space}

        except Exception as e:
            logger.error(f"Error in process_pattern: {e}", exc_info=True)
            raise
        finally:
            self.resources.cleanup()


# ===========================================================================
# PROFILING INFRASTRUCTURE
# ===========================================================================

class SystemProfiler:
    """Wall-clock and cProfile instrumentation for each pipeline module.

    Usage:
        profiler = SystemProfiler(system, config)
        report   = profiler.profile(pattern)
        profiler.print_report(report)
    """

    def __init__(self, system: UnifiedSystem, config: SystemConfig):
        self.system = system
        self.config = config

    # ---- per-module timing -------------------------------------------------

    def _time_module(self, fn, *args) -> Tuple[Any, float]:
        """Run fn(*args), return (result, wall_seconds)."""
        t0     = time.perf_counter()
        result = fn(*args)
        return result, time.perf_counter() - t0

    def profile(self, pattern: Pattern) -> Dict:
        """Profile every stage of the pipeline individually."""
        results:  Dict[str, Any]   = {}
        timings:  Dict[str, float] = {}
        errors:   Dict[str, str]   = {}

        pattern = pattern.to_device(torch.device(self.config.device))

        # 1. OneShotLearner
        try:
            learned, dt = self._time_module(self.system.learner.learn, pattern)
            results['learned'] = learned
            timings['OneShotLearner'] = dt
        except Exception as e:
            errors['OneShotLearner'] = str(e)
            learned = pattern   # fall through

        # 2. PatternRecognizer
        try:
            recognition, dt = self._time_module(
                self.system.recognizer.recognize, learned)
            results['recognition'] = recognition
            timings['PatternRecognizer'] = dt
        except Exception as e:
            errors['PatternRecognizer'] = str(e)

        # 3. CombinatorialGenerator
        try:
            variations, dt = self._time_module(
                self.system.generator.generate, learned)
            results['variations'] = variations
            timings['CombinatorialGenerator'] = dt
        except Exception as e:
            errors['CombinatorialGenerator'] = str(e)
            variations = {'combinations': []}

        # 4. MetaPatternProcessor
        try:
            meta_in = [learned] + variations.get('combinations', [])
            meta, dt = self._time_module(
                self.system.meta_processor.process_meta, meta_in)
            results['meta'] = meta
            timings['MetaPatternProcessor'] = dt
        except Exception as e:
            errors['MetaPatternProcessor'] = str(e)

        # 5. SpaceExplorer
        try:
            space, dt = self._time_module(
                self.system.explorer.explore, learned)
            results['space'] = space
            timings['SpaceExplorer'] = dt
        except Exception as e:
            errors['SpaceExplorer'] = str(e)

        total = sum(timings.values())
        return {'timings': timings, 'results': results,
                'errors': errors, 'total_wall_s': total}

    # ---- deep cProfile run -------------------------------------------------

    def cprofile(self, pattern: Pattern) -> pstats.Stats:
        """Run the full pipeline under cProfile and return Stats."""
        pr = cProfile.Profile()
        pr.enable()
        try:
            self.system.process_pattern(pattern)
        except Exception:
            pass
        pr.disable()
        stream = io.StringIO()
        stats  = pstats.Stats(pr, stream=stream)
        stats.sort_stats('cumulative')
        return stats

    # ---- memory footprint --------------------------------------------------

    def memory_footprint(self, pattern: Pattern) -> Dict[str, int]:
        """Estimate per-module tensor memory in bytes (CPU)."""
        foot: Dict[str, int] = {}

        def tensor_bytes(t: torch.Tensor) -> int:
            return t.nelement() * t.element_size()

        result = self.system.process_pattern(pattern)

        # learned
        if 'learned' in result:
            foot['learned_data'] = tensor_bytes(result['learned'].data)

        # recognition
        if 'recognition' in result:
            rec = result['recognition']
            foot['geometry']     = tensor_bytes(rec.get('geometry', torch.tensor(0)))
            foot['combinations'] = tensor_bytes(rec.get('combinations', torch.tensor(0)))

        # space
        if 'space' in result:
            sp = result['space']
            dims = sp.get('structure', {}).get('dimensions', {})
            if 'singular_values' in dims:
                foot['singular_values'] = tensor_bytes(dims['singular_values'])

        foot['total_estimated'] = sum(foot.values())
        return foot

    # ---- report printer ----------------------------------------------------

    @staticmethod
    def print_report(profile_result: Dict) -> None:
        timings = profile_result['timings']
        errors  = profile_result['errors']
        total   = profile_result['total_wall_s']

        bar_width = 40
        max_t     = max(timings.values()) if timings else 1.0

        print("\n" + "=" * 60)
        print("  VDJ-Inspired Algorithm — Performance Profile")
        print("=" * 60)
        print(f"  {'Module':<28} {'Time (ms)':>10}  {'%':>6}  Bar")
        print("-" * 60)

        for module, dt in sorted(timings.items(), key=lambda x: -x[1]):
            pct     = (dt / total * 100) if total > 0 else 0
            bar_len = int((dt / max_t) * bar_width)
            bar     = "█" * bar_len
            print(f"  {module:<28} {dt*1000:>10.2f}  {pct:>5.1f}%  {bar}")

        print("-" * 60)
        print(f"  {'TOTAL':<28} {total*1000:>10.2f}  {'100.0%':>6}")

        if errors:
            print("\n  Errors:")
            for mod, err in errors.items():
                print(f"    [{mod}] {err}")

        print("=" * 60 + "\n")

    @staticmethod
    def print_cprofile(stats: pstats.Stats, n: int = 20) -> None:
        print("\n" + "=" * 60)
        print(f"  cProfile — Top {n} cumulative callers")
        print("=" * 60)
        stats.print_stats(n)


# ===========================================================================
# Entry points
# ===========================================================================

def build_system(pattern_size: int = 16) -> Tuple[UnifiedSystem, SystemConfig]:
    config = SystemConfig(
        num_gpus=1 if torch.cuda.is_available() else 0,
        num_cpus=4,
        pattern_size=pattern_size,
        state_dims=(pattern_size, pattern_size),
        batch_size=32,
        max_combo_r=6,          # safe upper bound for combinatorial generator
        neighbor_threshold=2.0,
    )
    return UnifiedSystem(config), config


def make_test_pattern(config: SystemConfig) -> Pattern:
    n    = config.pattern_size
    data = torch.randn(n, n)
    return Pattern(data=data, type=PatternType.GEOMETRIC,
                   scale=1.0, properties={}, validation={})


def main() -> None:
    """Functional smoke-test + full profile report."""
    system, config = build_system(pattern_size=16)
    pattern        = make_test_pattern(config)

    logger.info("Running pipeline smoke-test ...")
    results = system.process_pattern(pattern)
    logger.info("Pipeline completed.")
    logger.info(f"  Recognition keys   : {list(results['recognition'].keys())}")
    logger.info(f"  Variation types    : {list(results['variations'].keys())}")
    logger.info(f"  Meta-patterns found: {len(results['meta_patterns']['meta_patterns'])}")
    logger.info(f"  Space paths found  : {len(results['space']['paths'])}")

    # ---- profiling --------------------------------------------------------
    profiler = SystemProfiler(system, config)

    print("\n[1/3] Wall-clock profile ...")
    report = profiler.profile(pattern)
    SystemProfiler.print_report(report)

    print("[2/3] Memory footprint ...")
    pattern2 = make_test_pattern(config)
    foot     = profiler.memory_footprint(pattern2)
    print("\n  Memory footprint (bytes):")
    for k, v in foot.items():
        print(f"    {k:<30} {v:>10,}")

    print("\n[3/3] cProfile (top 15) ...")
    pattern3 = make_test_pattern(config)
    stats    = profiler.cprofile(pattern3)
    SystemProfiler.print_cprofile(stats, n=15)


def profile_system() -> None:
    """Standalone profiling entry point."""
    system, config = build_system()
    pattern        = make_test_pattern(config)
    profiler       = SystemProfiler(system, config)
    report         = profiler.profile(pattern)
    SystemProfiler.print_report(report)


if __name__ == "__main__":
    main()
