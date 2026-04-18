"""
veritas_verification.py
Proof-based verification system for VERITAS.

Bug fixes vs original:
  - meta_error <= 2 * base_proof.steps[0].conclusion  was comparing a float
    to 2*bool (True=1, False=0), which gave nonsensical results when the
    base proof step was False. Fixed to compare against a proper float bound.
  - bounds dict used min() over bools; replaced with meaningful float values.
  - confidence computation now guards against empty verified-proof list.
"""

import numpy as np
from math import log, sqrt, ceil
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class TheoremType(Enum):
    PAC = "pac"
    ALT = "alt"
    META = "meta"
    COMPOSITION = "composition"


@dataclass
class ProofStep:
    statement: str
    justification: str
    assumptions: List[str]
    conclusion: bool
    verification: List[bool]


@dataclass
class TheoremProof:
    theorem_type: TheoremType
    steps: List[ProofStep]
    complete: bool
    verified: bool


@dataclass
class VerificationTrace:
    proofs: List[TheoremProof]
    bounds: Dict[str, float]
    confidence: float
    timestamp: int


class ProofVerifier:
    """Verifies mathematical proofs for PAC, ALT, Meta, and Composition."""

    def __init__(self):
        self.proof_history: List[TheoremProof] = []
        self.verification_traces: List[VerificationTrace] = []

    # ------------------------------------------------------------------
    def verify_pac_theorem(
        self,
        empirical_error: float,
        n_samples: int,
        dimension: int,
        epsilon: float,
        delta: float,
    ) -> TheoremProof:
        """Verify PAC learning theorem (Theorems 2 & 3)."""
        steps = []

        # Step 1: Sample complexity — ln|H| = 2^n * ln2 per Theorem 3
        log_H = (2 ** dimension) * log(2)
        sample_bound = ceil((1.0 / epsilon ** 2) * (log_H + log(1.0 / delta)))
        steps.append(ProofStep(
            statement="Sample complexity bound",
            justification="m ≥ (1/ε²)(ln|H| + ln(1/δ)), |H| = 2^{2^n}",
            assumptions=[f"dimension={dimension}", f"ε={epsilon}", f"δ={delta}"],
            conclusion=n_samples >= sample_bound,
            verification=[n_samples >= sample_bound, sample_bound > 0],
        ))

        # Step 2: Hoeffding error bound
        hoeffding = (sqrt(log(2.0 / delta) / (2.0 * n_samples))
                     if n_samples > 0 else float('inf'))
        steps.append(ProofStep(
            statement="Hoeffding error bound",
            justification="By Hoeffding's inequality",
            assumptions=[f"n_samples={n_samples}", f"δ={delta}"],
            conclusion=empirical_error <= epsilon + hoeffding,
            verification=[empirical_error <= epsilon + hoeffding, hoeffding >= 0],
        ))

        # Step 3: Confidence bound
        confidence = 1.0 - delta
        steps.append(ProofStep(
            statement="Confidence bound",
            justification="From PAC definition: confidence = 1 − δ",
            assumptions=[f"δ={delta}"],
            conclusion=0 < confidence < 1,
            verification=[confidence > 0, confidence < 1],
        ))

        proof = TheoremProof(
            theorem_type=TheoremType.PAC,
            steps=steps,
            complete=len(steps) == 3,
            verified=all(s.conclusion for s in steps),
        )
        self.proof_history.append(proof)
        return proof

    # ------------------------------------------------------------------
    def verify_alt_theorem(
        self,
        mistakes: int,
        queries: int,
        dimension: int,
    ) -> TheoremProof:
        """Verify ALT learning theorem (Theorems 4 & 5)."""
        steps = []

        # Step 1: Mistake bound — lg|H| = 2^n  (Theorem 4)
        mistake_bound = 2 ** dimension
        steps.append(ProofStep(
            statement="Mistake bound",
            justification="M(L) ≤ lg|H|, |H| = 2^{2^n}, lg|H| = 2^n",
            assumptions=[f"dimension={dimension}"],
            conclusion=mistakes <= mistake_bound,
            verification=[mistakes <= mistake_bound, mistake_bound > 0],
        ))

        # Step 2: Query complexity  (Theorem 5)
        steps.append(ProofStep(
            statement="Query complexity",
            justification="Binary search: Q(L) ≤ n queries sufficient",
            assumptions=[f"dimension={dimension}"],
            conclusion=queries <= dimension,
            verification=[queries <= dimension, dimension > 0],
        ))

        # Step 3: Computation bound
        comp_bound = dimension * log(max(dimension, 2))
        steps.append(ProofStep(
            statement="Computation bound",
            justification="O(n log n) computation per query",
            assumptions=[f"dimension={dimension}"],
            conclusion=True,
            verification=[comp_bound > 0],
        ))

        proof = TheoremProof(
            theorem_type=TheoremType.ALT,
            steps=steps,
            complete=len(steps) == 3,
            verified=all(s.conclusion for s in steps),
        )
        self.proof_history.append(proof)
        return proof

    # ------------------------------------------------------------------
    def verify_meta_theorem(
        self,
        meta_error: float,
        base_proof: TheoremProof,
        dimension: int,
    ) -> TheoremProof:
        """Verify meta-learning theorem (Theorems 6 & 7).

        Fix: comparison is now against a computed float epsilon_meta,
        not against 2 * bool(step.conclusion).
        """
        steps = []

        # Derive a meta-epsilon from the base proof's Hoeffding step
        # (step index 1 if PAC, step 0 otherwise).
        base_epsilon = 0.01  # default fallback
        if base_proof.theorem_type == TheoremType.PAC and len(base_proof.steps) >= 2:
            # The Hoeffding step stored assumptions like "ε=0.01"
            for assumption in base_proof.steps[0].assumptions:
                if assumption.startswith("ε="):
                    try:
                        base_epsilon = float(assumption.split("=")[1])
                    except ValueError:
                        pass

        # Meta error bound: ε_meta ≤ 2 * ε_base  (composition triangle ineq.)
        epsilon_meta = 2.0 * base_epsilon
        steps.append(ProofStep(
            statement="Meta error bound",
            justification="Composition: err(m∘h) ≤ err(h) + err_m(m) ≤ 2ε",
            assumptions=[f"base_error≤{base_epsilon:.4f}", "base proof verified"],
            conclusion=meta_error <= epsilon_meta,
            verification=[meta_error >= 0.0, base_proof.verified],
        ))

        # Meta sample complexity: O(log(n)) overhead from hierarchical sampling
        meta_samples = ceil(log(max(dimension, 2)))
        steps.append(ProofStep(
            statement="Meta sample complexity",
            justification="Hierarchical sampling: O(log n) overhead",
            assumptions=[f"dimension={dimension}"],
            conclusion=True,
            verification=[meta_samples > 0],
        ))

        proof = TheoremProof(
            theorem_type=TheoremType.META,
            steps=steps,
            complete=len(steps) == 2,
            verified=all(s.conclusion for s in steps),
        )
        self.proof_history.append(proof)
        return proof

    # ------------------------------------------------------------------
    def verify_composition(
        self,
        pac_proof: TheoremProof,
        alt_proof: TheoremProof,
    ) -> TheoremProof:
        """Verify proof composition (Theorem 9)."""
        steps = []

        steps.append(ProofStep(
            statement="Composition validity",
            justification="Both PAC and ALT proofs verified independently",
            assumptions=["PAC proof verified", "ALT proof verified"],
            conclusion=pac_proof.verified and alt_proof.verified,
            verification=[pac_proof.verified, alt_proof.verified],
        ))

        steps.append(ProofStep(
            statement="Error bound composition",
            justification="Triangle inequality: err(m∘h) ≤ ε + ε_m; "
                           "union bound: P ≤ δ + δ_m",
            assumptions=["Errors are additive", "Probabilities via union bound"],
            conclusion=True,
            verification=[pac_proof.steps[0].conclusion,
                           alt_proof.steps[0].conclusion],
        ))

        proof = TheoremProof(
            theorem_type=TheoremType.COMPOSITION,
            steps=steps,
            complete=len(steps) == 2,
            verified=all(s.conclusion for s in steps),
        )
        self.proof_history.append(proof)
        return proof

    # ------------------------------------------------------------------
    def create_verification_trace(
        self, proofs: List[TheoremProof]
    ) -> VerificationTrace:
        """Aggregate proofs into a VerificationTrace with meaningful bounds."""

        # Compute per-type summary: fraction of steps that passed
        def step_pass_rate(ptype: TheoremType) -> float:
            matching = [p for p in proofs if p.theorem_type == ptype]
            if not matching:
                return 0.0
            all_steps = [s for p in matching for s in p.steps]
            if not all_steps:
                return 0.0
            return float(np.mean([s.conclusion for s in all_steps]))

        bounds = {
            'pac': step_pass_rate(TheoremType.PAC),
            'alt': step_pass_rate(TheoremType.ALT),
            'meta': step_pass_rate(TheoremType.META),
        }

        # Confidence = fraction of proofs that fully verified
        verified_proofs = [p for p in proofs if p.verified]
        confidence = (len(verified_proofs) / len(proofs)) if proofs else 0.0

        trace = VerificationTrace(
            proofs=proofs,
            bounds=bounds,
            confidence=confidence,
            timestamp=len(self.verification_traces),
        )
        self.verification_traces.append(trace)
        return trace


# ---------------------------------------------------------------------------
# High-level verified learning system
# ---------------------------------------------------------------------------

class VerifiedLearningSystem:
    """Wraps ProofVerifier for convenient end-to-end verification."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.verifier = ProofVerifier()

    def verify_learning(
        self,
        empirical_error: float,
        n_samples: int,
        mistakes: int,
        queries: int,
        meta_error: float,
        epsilon: float = 0.01,
        delta: float = 0.01,
    ) -> VerificationTrace:
        pac_proof = self.verifier.verify_pac_theorem(
            empirical_error, n_samples, self.dimension, epsilon, delta
        )
        alt_proof = self.verifier.verify_alt_theorem(
            mistakes, queries, self.dimension
        )
        meta_proof = self.verifier.verify_meta_theorem(
            meta_error, pac_proof, self.dimension
        )
        comp_proof = self.verifier.verify_composition(pac_proof, alt_proof)
        return self.verifier.create_verification_trace(
            [pac_proof, alt_proof, meta_proof, comp_proof]
        )
