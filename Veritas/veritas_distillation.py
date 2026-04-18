"""
veritas_distillation.py
Ensemble teacher → student distillation for VERITAS.

Fixes vs original:
  - VERITAS imported from veritas_core (was undefined).
  - KL divergence computed manually (no torch.nn.functional).
  - DataLoader replaced with a simple numpy batch iterator.
  - Temperature scaling applied correctly.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from veritas_core import VERITAS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _softmax(x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    x = x / temperature
    e = np.exp(x - np.max(x))
    return e / e.sum()

def _log_softmax(x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    x = x / temperature
    x = x - np.max(x)
    return x - np.log(np.sum(np.exp(x)))

def _kl_divergence(log_p: np.ndarray, q: np.ndarray) -> float:
    """KL(q || p)  where log_p = log(p)."""
    return float(np.sum(q * (np.log(q + 1e-12) - log_p)))


@dataclass
class DistillationConfig:
    temperature: float = 2.0
    alpha: float = 0.5        # balance: direct vs distillation loss
    meta_weight: float = 0.3  # weight of meta-learning objective
    ensemble_size: int = 3    # number of teacher VERITAS instances
    hidden_size: int = 64
    batch_size: int = 16


# ---------------------------------------------------------------------------
# VERITASDistiller
# ---------------------------------------------------------------------------

class VERITASDistiller:

    def __init__(self, config: DistillationConfig):
        self.config = config
        self.teacher_models: List[VERITAS] = []
        self.student_model: VERITAS = None

    def initialize_teachers(self, input_size: int) -> None:
        self.teacher_models = [
            VERITAS(input_size, self.config.hidden_size)
            for _ in range(self.config.ensemble_size)
        ]

    def initialize_student(self, input_size: int) -> None:
        self.student_model = VERITAS(input_size, self.config.hidden_size)

    # ------------------------------------------------------------------
    def compute_ensemble_outputs(
        self, x: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        rule_outputs, meta_outputs = [], []
        for teacher in self.teacher_models:
            rule_out, pac_bound, alt_bound = teacher.rule_network.forward(x)
            rule_outputs.append(rule_out)
            state = teacher.rule_network.flat_params()
            meta_out, _ = teacher.meta_network.forward(state, pac_bound, alt_bound)
            meta_outputs.append(meta_out)
        rule_ensemble = np.mean(rule_outputs, axis=0)
        meta_ensemble = np.mean(meta_outputs, axis=0)
        return rule_ensemble, meta_ensemble

    # ------------------------------------------------------------------
    def distillation_loss(
        self,
        student_rule: np.ndarray, student_meta: np.ndarray,
        teacher_rule: np.ndarray, teacher_meta: np.ndarray,
        x: np.ndarray,
    ) -> float:
        T = self.config.temperature

        # KL distillation losses
        rule_distill = _kl_divergence(
            _log_softmax(student_rule, T),
            _softmax(teacher_rule, T),
        ) * (T ** 2)

        meta_distill = _kl_divergence(
            _log_softmax(student_meta, T),
            _softmax(teacher_meta, T),
        ) * (T ** 2)

        # Direct MSE losses
        rule_direct = float(np.mean((student_rule - x.astype(np.float64)) ** 2))
        meta_direct = float(np.mean((student_meta - teacher_meta) ** 2))

        total_rule = (self.config.alpha * rule_direct
                      + (1 - self.config.alpha) * rule_distill)
        total_meta = (self.config.alpha * meta_direct
                      + (1 - self.config.alpha) * meta_distill)

        return ((1 - self.config.meta_weight) * total_rule
                + self.config.meta_weight * total_meta)

    # ------------------------------------------------------------------
    def train_step(self, x: np.ndarray) -> Dict[str, float]:
        teacher_rule, teacher_meta = self.compute_ensemble_outputs(x)

        student_rule, pac_bound, alt_bound = \
            self.student_model.rule_network.forward(x)
        state = self.student_model.rule_network.flat_params()
        student_meta, theorem = self.student_model.meta_network.forward(
            state, pac_bound, alt_bound
        )

        loss = self.distillation_loss(
            student_rule, student_meta,
            teacher_rule, teacher_meta, x
        )

        # Simple gradient step: push student rule toward teacher_rule
        rule_grad = 2.0 * (student_rule - teacher_rule) / student_rule.shape[0]
        self.student_model.rule_network.net.backward(rule_grad)
        self.student_model.rule_network.net.sgd_step(lr=1e-3)

        return {
            'distillation_loss': loss,
            'pac_confidence': pac_bound.confidence,
            'theorem_discovered': float(theorem is not None),
        }

    # ------------------------------------------------------------------
    def train(
        self,
        data: np.ndarray,
        num_epochs: int,
        batch_size: Optional[int] = None,
    ) -> None:
        bs = batch_size or self.config.batch_size
        n = len(data)

        for epoch in range(num_epochs):
            idx = np.random.permutation(n)
            epoch_losses = []

            for start in range(0, n, bs):
                batch_idx = idx[start:start + bs]
                for i in batch_idx:
                    m = self.train_step(data[i])
                    epoch_losses.append(m['distillation_loss'])

            print(f"Epoch {epoch}: avg distillation loss = "
                  f"{np.mean(epoch_losses):.4f}")


