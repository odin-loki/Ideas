"""
veritas_integration.py
IntegratedVERITAS: combines RuleNetwork, MetaNetwork, and the
full ProofVerifier pipeline into a single verified training system.

Fixes vs original:
  - Missing `from typing import Any` added.
  - All cross-module classes now imported from veritas_core /
    veritas_verification.
  - _update_networks uses a real SGD step, not gradient-free param mutation.
"""

import numpy as np
from typing import Any, Dict, List, Optional

from veritas_core import (
    RuleNetwork, MetaNetwork, BinarySpace,
    PACBound, ALTBound, MetaTheorem,
)
from veritas_verification import (
    ProofVerifier, VerifiedLearningSystem, VerificationTrace,
)


class IntegratedVERITAS:
    """Complete integrated learning system with end-to-end verification."""

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        epsilon: float = 0.01,
        delta: float = 0.01,
        lr: float = 0.001,
    ):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.epsilon = epsilon
        self.delta = delta
        self.lr = lr

        self.rule_network = RuleNetwork(input_size, hidden_size)
        self.meta_network = MetaNetwork(
            self.rule_network.numel(), hidden_size
        )
        self.verification_system = VerifiedLearningSystem(input_size)
        self.verifier = ProofVerifier()

        self.samples_seen = 0
        self.mistakes_made = 0
        self.queries_made = 0
        self.verification_traces: List[VerificationTrace] = []

    # ------------------------------------------------------------------
    def train_step(
        self, x: np.ndarray, verify: bool = True
    ) -> Dict[str, Any]:
        if not np.all((x == 0) | (x == 1)):
            raise ValueError("Input must be binary (0 / 1 values only)")

        output, pac_bound, alt_bound = self.rule_network.forward(x)

        error = float(np.mean(np.abs(output - x)))

        self.samples_seen += 1
        if error > self.epsilon:
            self.mistakes_made += 1
        self.queries_made += 1

        state = self.rule_network.flat_params()
        meta_output, theorem = self.meta_network.forward(
            state, pac_bound, alt_bound
        )
        # meta_error: RMS of meta-output (tracks representational magnitude)
        meta_error = float(np.sqrt(np.mean(meta_output ** 2)))

        verification_trace: Optional[VerificationTrace] = None
        if verify:
            verification_trace = self._verify_complete_learning(
                error, meta_error, output, theorem
            )
            self.verification_traces.append(verification_trace)

        metrics: Dict[str, Any] = {
            'error': error,
            'meta_error': meta_error,
            'samples': self.samples_seen,
            'mistakes': self.mistakes_made,
            'queries': self.queries_made,
            'verified': (verification_trace.proofs[-1].verified
                         if verification_trace else None),
            'confidence': (verification_trace.confidence
                           if verification_trace else None),
        }

        # Only do a gradient step when the verification passes
        if verification_trace is None or verification_trace.proofs[-1].verified:
            self._update_networks(x, output, state, meta_output)

        return metrics

    # ------------------------------------------------------------------
    def _verify_complete_learning(
        self,
        error: float,
        meta_error: float,
        output: np.ndarray,
        theorem: Optional[MetaTheorem],
    ) -> VerificationTrace:
        pac_proof = self.verifier.verify_pac_theorem(
            error, self.samples_seen, output.shape[0],
            self.epsilon, self.delta
        )
        alt_proof = self.verifier.verify_alt_theorem(
            self.mistakes_made, self.queries_made, output.shape[0]
        )
        meta_proof = self.verifier.verify_meta_theorem(
            meta_error, pac_proof, output.shape[0]
        )
        comp_proof = self.verifier.verify_composition(pac_proof, alt_proof)
        return self.verifier.create_verification_trace(
            [pac_proof, alt_proof, meta_proof, comp_proof]
        )

    # ------------------------------------------------------------------
    def _update_networks(
        self,
        x: np.ndarray,
        rule_output: np.ndarray,
        state: np.ndarray,
        meta_output: np.ndarray,
    ) -> None:
        """Gradient update via MSE loss."""
        # Rule network backward: dL/d(output) = 2*(output - x) / n
        rule_grad = 2.0 * (rule_output - x) / x.shape[0]
        self.rule_network.net.backward(rule_grad)
        self.rule_network.net.sgd_step(self.lr)

        # Meta network backward: push output toward zero (regularise magnitude)
        meta_grad = 2.0 * meta_output / meta_output.shape[0]
        self.meta_network.net.backward(meta_grad)
        self.meta_network.net.sgd_step(self.lr * 0.1)

    # ------------------------------------------------------------------
    def train(
        self,
        data: np.ndarray,
        epochs: int,
        verify_each_step: bool = True,
    ) -> List[Dict[str, float]]:
        history = []

        for epoch in range(epochs):
            epoch_metrics: List[Dict[str, Any]] = []

            for i in range(len(data)):
                metrics = self.train_step(data[i], verify=verify_each_step)
                epoch_metrics.append(metrics)

            float_keys = ['error', 'meta_error', 'verified', 'confidence']
            avg: Dict[str, float] = {
                key: float(np.mean([m[key] for m in epoch_metrics
                                    if m[key] is not None]))
                for key in float_keys
            }
            avg['epoch'] = float(epoch)
            history.append(avg)

            # Epoch-level verification against final sample
            epoch_trace = self._verify_complete_learning(
                avg['error'], avg['meta_error'],
                data[-1], None
            )

            print(f"\nEpoch {epoch} | error={avg['error']:.4f} "
                  f"meta_err={avg['meta_error']:.4f} "
                  f"conf={avg['confidence']:.3f}")
            print(f"  PAC verified:  {epoch_trace.proofs[0].verified}")
            print(f"  ALT verified:  {epoch_trace.proofs[1].verified}")
            print(f"  Meta verified: {epoch_trace.proofs[2].verified}")
            print(f"  Composition:   {epoch_trace.proofs[3].verified}")

        return history

    # ------------------------------------------------------------------
    def get_verification_summary(self) -> Dict[str, float]:
        if not self.verification_traces:
            return {}
        recent = self.verification_traces[-10:]
        return {
            'avg_confidence': float(np.mean([t.confidence for t in recent])),
            'pac_verification_rate': float(np.mean(
                [t.proofs[0].verified for t in recent])),
            'alt_verification_rate': float(np.mean(
                [t.proofs[1].verified for t in recent])),
            'meta_verification_rate': float(np.mean(
                [t.proofs[2].verified for t in recent])),
            'composition_verification_rate': float(np.mean(
                [t.proofs[3].verified for t in recent])),
        }
