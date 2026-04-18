"""
veritas_core.py
Core VERITAS components: BinarySpace, PACLearner, ALTLearner,
MetaLearner, RuleNetwork, MetaNetwork, VERITAS.

Ported from PyTorch to NumPy.
Bug fixes:
  - Sample complexity now uses ln|H| = 2^n * ln2, consistent with Theorem 3.
  - log(0) guard in computation_bound when dimension == 1.
"""

import numpy as np
from math import log, sqrt, ceil
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Lightweight numpy neural-network primitives
# ---------------------------------------------------------------------------

class Linear:
    """Fully-connected layer with He initialisation."""

    def __init__(self, in_features: int, out_features: int):
        scale = sqrt(2.0 / in_features)
        self.W = np.random.randn(out_features, in_features).astype(np.float64) * scale
        self.b = np.zeros(out_features, dtype=np.float64)
        # gradient buffers
        self.dW: Optional[np.ndarray] = None
        self.db: Optional[np.ndarray] = None
        self._input: Optional[np.ndarray] = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self._input = x.copy()
        return self.W @ x + self.b

    def backward(self, grad_out: np.ndarray) -> np.ndarray:
        assert self._input is not None, "forward() must be called before backward()"
        self.dW = np.outer(grad_out, self._input)
        self.db = grad_out.copy()
        return self.W.T @ grad_out

    @property
    def parameters(self) -> List[np.ndarray]:
        return [self.W, self.b]

    @property
    def gradients(self) -> List[Optional[np.ndarray]]:
        return [self.dW, self.db]

    def numel(self) -> int:
        return self.W.size + self.b.size

    def flat_params(self) -> np.ndarray:
        return np.concatenate([self.W.flatten(), self.b.flatten()])


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, x)

def relu_grad(x: np.ndarray, grad: np.ndarray) -> np.ndarray:
    return grad * (x > 0).astype(np.float64)

def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


class MLP:
    """Two-layer MLP: Linear → ReLU → Linear (→ optional sigmoid)."""

    def __init__(self, in_size: int, hidden_size: int, out_size: int,
                 output_activation: bool = False):
        self.fc1 = Linear(in_size, hidden_size)
        self.fc2 = Linear(hidden_size, out_size)
        self.output_activation = output_activation
        self._h: Optional[np.ndarray] = None  # pre-relu hidden
        self._h_relu: Optional[np.ndarray] = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self._h = self.fc1.forward(x)
        self._h_relu = relu(self._h)
        out = self.fc2.forward(self._h_relu)
        if self.output_activation:
            out = sigmoid(out)
        return out

    def backward(self, grad_out: np.ndarray) -> None:
        grad_h2 = self.fc2.backward(grad_out)
        grad_h1 = relu_grad(self._h, grad_h2)
        self.fc1.backward(grad_h1)

    def sgd_step(self, lr: float) -> None:
        for layer in [self.fc1, self.fc2]:
            for p, g in zip(layer.parameters, layer.gradients):
                if g is not None:
                    p -= lr * g

    def flat_params(self) -> np.ndarray:
        return np.concatenate([self.fc1.flat_params(), self.fc2.flat_params()])

    def numel(self) -> int:
        return self.fc1.numel() + self.fc2.numel()


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class BinaryPattern:
    pattern: np.ndarray
    dimension: int
    verified: bool
    verification_trace: List[bool]


@dataclass
class PACBound:
    epsilon: float
    delta: float
    samples_required: int
    empirical_error: float
    true_error_bound: float
    confidence: float
    proof_trace: List[bool]


@dataclass
class ALTBound:
    mistake_bound: int
    query_complexity: int
    computation_bound: float
    current_mistakes: int
    current_queries: int
    proof_trace: List[bool]


@dataclass
class MetaTheorem:
    pattern: np.ndarray
    type: str          # 'pac' or 'alt'
    confidence: float
    proof_trace: List[bool]
    applications: int
    success_rate: float


# ---------------------------------------------------------------------------
# BinarySpace
# ---------------------------------------------------------------------------

class BinarySpace:
    """Complete binary pattern space."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.patterns: List[BinaryPattern] = []

    def verify_pattern(self, pattern: np.ndarray) -> BinaryPattern:
        verification = [
            pattern.ndim == 1,
            pattern.shape[0] == self.dimension,
            bool(np.all((pattern == 0) | (pattern == 1))),
            not bool(np.any(np.isnan(pattern))),
        ]
        return BinaryPattern(
            pattern=pattern,
            dimension=self.dimension,
            verified=all(verification),
            verification_trace=verification,
        )

    def hamming_distance(self, p1: np.ndarray, p2: np.ndarray) -> int:
        return int(np.sum(p1 != p2))

    def is_complete(self, patterns: List[np.ndarray]) -> bool:
        if len(patterns) < 2:
            return True
        distances = [self.hamming_distance(patterns[i], patterns[i + 1])
                     for i in range(len(patterns) - 1)]
        return all(d1 >= d2 for d1, d2 in zip(distances, distances[1:]))


# ---------------------------------------------------------------------------
# PAC Learner
# ---------------------------------------------------------------------------

class PACLearner:
    """PAC Learning bound calculator.

    Bug fix: sample complexity uses ln|H| = 2^n * ln(2) per Theorem 3,
    not dimension * ln(2) as the original code had.
    """

    def __init__(self, epsilon: float = 0.01, delta: float = 0.01):
        self.epsilon = epsilon
        self.delta = delta
        self.samples_seen = 0
        self.error_history: List[float] = []

    def calculate_bound(self, empirical_error: float,
                        n_samples: int, dimension: int) -> PACBound:
        # ln|H| where |H| = 2^{2^n}  →  ln|H| = 2^n * ln2  (Theorem 3)
        log_H = (2 ** dimension) * log(2)
        samples_required = ceil(
            (1.0 / self.epsilon ** 2) * (log_H + log(1.0 / self.delta))
        )

        # Hoeffding-based true error bound (Theorem 2)
        if n_samples > 0:
            true_error_bound = empirical_error + sqrt(
                log(2.0 / self.delta) / (2.0 * n_samples)
            )
        else:
            true_error_bound = float('inf')

        proof_trace = [
            n_samples >= samples_required,
            empirical_error <= self.epsilon,
            true_error_bound <= 2 * self.epsilon,
            self.samples_seen >= samples_required,
        ]

        return PACBound(
            epsilon=self.epsilon,
            delta=self.delta,
            samples_required=samples_required,
            empirical_error=empirical_error,
            true_error_bound=true_error_bound,
            confidence=1.0 - self.delta,
            proof_trace=proof_trace,
        )


# ---------------------------------------------------------------------------
# ALT Learner
# ---------------------------------------------------------------------------

class ALTLearner:
    """ALT Learning bound calculator."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.mistakes = 0
        self.queries = 0
        self.computations = 0

    def calculate_bound(self) -> ALTBound:
        # Mistake bound: lg|H| where |H| = 2^{2^n}  →  lg|H| = 2^n (Theorem 4)
        mistake_bound = 2 ** self.dimension  # = ceil(log2(2^{2^n})) = 2^n

        # Query complexity: n queries sufficient (Theorem 5)
        query_bound = self.dimension

        # Computation bound — guard log(1) edge case
        comp_bound = (self.dimension * log(max(self.dimension, 2)))

        proof_trace = [
            self.mistakes <= mistake_bound,
            self.queries <= query_bound,
            self.computations <= comp_bound,
        ]

        return ALTBound(
            mistake_bound=mistake_bound,
            query_complexity=query_bound,
            computation_bound=comp_bound,
            current_mistakes=self.mistakes,
            current_queries=self.queries,
            proof_trace=proof_trace,
        )


# ---------------------------------------------------------------------------
# Meta Learner
# ---------------------------------------------------------------------------

class MetaLearner:
    """Meta-Learning theorem discoverer."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.meta_space = BinarySpace(dimension)
        self.discovered_theorems: List[MetaTheorem] = []

    def discover_theorem(self, pattern: np.ndarray,
                         pac_bound: PACBound,
                         alt_bound: ALTBound) -> Optional[MetaTheorem]:
        binary_pattern = self.meta_space.verify_pattern(pattern)
        if not binary_pattern.verified:
            return None

        if all(pac_bound.proof_trace):
            theorem_type = 'pac'
            confidence = pac_bound.confidence
        elif all(alt_bound.proof_trace):
            theorem_type = 'alt'
            ratio = (alt_bound.current_mistakes / alt_bound.mistake_bound
                     if alt_bound.mistake_bound > 0 else 1.0)
            confidence = 1.0 - ratio
        else:
            return None

        theorem = MetaTheorem(
            pattern=pattern,
            type=theorem_type,
            confidence=confidence,
            proof_trace=[*binary_pattern.verification_trace, confidence > 0.9],
            applications=0,
            success_rate=1.0,
        )

        if all(theorem.proof_trace):
            self.discovered_theorems.append(theorem)
            return theorem
        return None


# ---------------------------------------------------------------------------
# Rule Network
# ---------------------------------------------------------------------------

class RuleNetwork:
    """Binary rule-learning network (MLP wrapper)."""

    def __init__(self, input_size: int, hidden_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.net = MLP(input_size, hidden_size, input_size,
                       output_activation=True)
        self.binary_space = BinarySpace(input_size)
        self.pac_learner = PACLearner()
        self.alt_learner = ALTLearner(input_size)

    def forward(self, x: np.ndarray) -> Tuple[np.ndarray, PACBound, ALTBound]:
        binary_pattern = self.binary_space.verify_pattern(x)
        if not binary_pattern.verified:
            raise ValueError("Input pattern failed binary verification")

        output = self.net.forward(x.astype(np.float64))

        error = float(np.mean(np.abs(output - x)))

        pac_bound = self.pac_learner.calculate_bound(
            error, self.pac_learner.samples_seen, x.shape[0]
        )
        alt_bound = self.alt_learner.calculate_bound()

        self.pac_learner.samples_seen += 1
        self.pac_learner.error_history.append(error)

        if error > self.pac_learner.epsilon:
            self.alt_learner.mistakes += 1
        self.alt_learner.queries += 1

        return output, pac_bound, alt_bound

    def flat_params(self) -> np.ndarray:
        return self.net.flat_params()

    def numel(self) -> int:
        return self.net.numel()


# ---------------------------------------------------------------------------
# Meta Network
# ---------------------------------------------------------------------------

class MetaNetwork:
    """Meta-learning network over rule-network parameter space."""

    def __init__(self, input_size: int, hidden_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.net = MLP(input_size, hidden_size, hidden_size)
        self.meta_learner = MetaLearner(hidden_size)

    def forward(self, state: np.ndarray,
                pac_bound: PACBound,
                alt_bound: ALTBound) -> Tuple[np.ndarray, Optional[MetaTheorem]]:
        meta_output = self.net.forward(state)
        # Binarise for theorem discovery (threshold at 0.5)
        binary_out = (sigmoid(meta_output) > 0.5).astype(np.float64)
        theorem = self.meta_learner.discover_theorem(
            binary_out, pac_bound, alt_bound
        )
        return meta_output, theorem


# ---------------------------------------------------------------------------
# VERITAS top-level
# ---------------------------------------------------------------------------

class VERITAS:
    """Complete VERITAS learning system."""

    def __init__(self, input_size: int, hidden_size: int):
        self.rule_network = RuleNetwork(input_size, hidden_size)
        self.meta_network = MetaNetwork(
            self.rule_network.numel(), hidden_size
        )
        self.verified_patterns: List[BinaryPattern] = []
        self.verified_theorems: List[MetaTheorem] = []

    def learn(self, x: np.ndarray) -> Dict[str, float]:
        output, pac_bound, alt_bound = self.rule_network.forward(x)

        state = self.rule_network.flat_params()
        meta_output, theorem = self.meta_network.forward(
            state, pac_bound, alt_bound
        )

        if theorem is not None:
            self.verified_theorems.append(theorem)

        pattern = self.rule_network.binary_space.verify_pattern(output)
        if pattern.verified:
            self.verified_patterns.append(pattern)

        return {
            'error': float(pac_bound.empirical_error),
            'pac_confidence': pac_bound.confidence,
            'alt_mistakes': float(alt_bound.current_mistakes),
            'theorem_discovered': float(theorem is not None),
            'verified_patterns': float(len(self.verified_patterns)),
            'verified_theorems': float(len(self.verified_theorems)),
        }

    def get_theoretical_insights(self) -> Dict[str, List[Dict]]:
        return {
            'pac_theorems': [
                {'confidence': t.confidence,
                 'success_rate': t.success_rate,
                 'applications': t.applications}
                for t in self.verified_theorems if t.type == 'pac'
            ],
            'alt_theorems': [
                {'confidence': t.confidence,
                 'success_rate': t.success_rate,
                 'applications': t.applications}
                for t in self.verified_theorems if t.type == 'alt'
            ],
        }
