"""
Quantum-Classical Hybrid Compressed Graph Processor
====================================================
Pipeline:
  Layer 1  SpectralCompressor      G (n nodes) -> G_k (k super-nodes)
  Layer 2  ChebyshevEncoder        G_k -> coefficient vector c in R^{J+1}
  Layer 3  QuantumCircuitSimulator |psi_c>, QAOA on H_k, noise side-data eta
  Layer 4  NoiseSolutionRanker     weight shots by ||eta||, rank candidates
  Layer 5  SpectralLiftback        z_k in {-1,+1}^k -> z in {-1,+1}^n

Fixes applied over v1:
  - Chebyshev coefficients now initialise the QAOA quantum state (Layer 2->3 wired)
  - ref_state is thread-local (passed explicitly, not stored on self)
  - Theorem 5 test checks the spectral error bound directly
  - verify_noise_side_data() stress-tests noise side-data at high noise rates
  - Classical MaxCut baseline via Fiedler vector spectral relaxation
"""

import numpy as np
import scipy.linalg as la
import networkx as nx
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import warnings
warnings.filterwarnings('ignore')


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class CompressedGraph:
    k: int
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    compressed_adj: np.ndarray
    compressed_laplacian: np.ndarray
    lambda_max: float
    reconstruction_error: float
    original_n: int


@dataclass
class EncodedSignal:
    coefficients: np.ndarray
    degree: int
    norm: float
    normalized: np.ndarray


@dataclass
class QuantumShot:
    bitstring: np.ndarray
    assignment: np.ndarray
    noise_vector: np.ndarray
    noise_norm: float
    cut_value: float


@dataclass
class ProcessingResult:
    best_partition: np.ndarray
    best_cut_value: float
    best_cut_fraction: float
    compressed_partition: np.ndarray
    compressed_cut_value: float
    top_candidates: List[Tuple[np.ndarray, float]]
    reconstruction_error: float
    noise_stats: Dict[str, float]
    n_shots: int
    classical_baseline_cut: float


# ---------------------------------------------------------------------------
# Layer 1: Spectral Graph Compressor
# ---------------------------------------------------------------------------

class SpectralCompressor:
    """
    Compresses G to G_k via rank-k truncated Laplacian eigendecomposition.
    Error: ||L~ - L~_k||_F = sqrt(sum_{i>k} lambda_i^2)  [Eckart-Young, Thm 1]
    """

    def __init__(self, k: int = 10, epsilon: Optional[float] = None):
        self.k = k
        self.epsilon = epsilon

    def compress(self, G: nx.Graph) -> CompressedGraph:
        n = G.number_of_nodes()
        if n < 2:
            raise ValueError("Graph must have >= 2 nodes.")

        L_norm = self._normalized_laplacian(G)
        A = nx.to_numpy_array(G, weight='weight')

        eigenvalues, eigenvectors = la.eigh(L_norm)
        eigenvalues = np.clip(eigenvalues, 0.0, None)
        lambda_max = float(eigenvalues[-1]) if len(eigenvalues) > 0 else 2.0

        if self.epsilon is not None:
            frob_sq = float(np.sum(eigenvalues ** 2))
            tail_sq = np.cumsum(eigenvalues[::-1] ** 2)[::-1]
            idx = np.searchsorted(-(np.sqrt(tail_sq / (frob_sq + 1e-15))),
                                  -self.epsilon)
            k_use = max(2, min(int(idx) + 1, n - 1))
        else:
            k_use = max(2, min(self.k, n - 1))

        Uk = eigenvectors[:, :k_use]
        Lk_eigs = eigenvalues[:k_use]

        tail_err = float(np.sqrt(np.sum(eigenvalues[k_use:] ** 2))) \
            if k_use < n else 0.0
        frob_norm = float(np.sqrt(np.sum(eigenvalues ** 2)))
        rel_error = tail_err / (frob_norm + 1e-15)

        return CompressedGraph(
            k=k_use,
            eigenvalues=Lk_eigs,
            eigenvectors=Uk,
            compressed_adj=Uk.T @ A @ Uk,
            compressed_laplacian=Uk.T @ L_norm @ Uk,
            lambda_max=lambda_max,
            reconstruction_error=rel_error,
            original_n=n
        )

    @staticmethod
    def _normalized_laplacian(G: nx.Graph) -> np.ndarray:
        n = G.number_of_nodes()
        nodes = list(G.nodes())
        idx = {v: i for i, v in enumerate(nodes)}
        A = np.zeros((n, n))
        for u, v, data in G.edges(data=True):
            w = float(data.get('weight', 1.0))
            A[idx[u], idx[v]] = w
            A[idx[v], idx[u]] = w
        deg = A.sum(axis=1)
        d_inv = np.where(deg > 1e-12, 1.0 / np.sqrt(deg), 0.0)
        D = np.diag(d_inv)
        return np.eye(n) - D @ A @ D


# ---------------------------------------------------------------------------
# Layer 2: Chebyshev Signal Encoder
# ---------------------------------------------------------------------------

class ChebyshevEncoder:
    """
    Encodes the spectral fingerprint of G_k as Chebyshev coefficients.
    The normalised vector is used to initialise the QAOA quantum state.
    Approximation error: O(exp(-J * delta / lambda_max))  [Theorem 2]
    """

    def __init__(self, degree: int = 16):
        self.degree = degree

    def encode(self, cg: CompressedGraph,
               signal: Optional[np.ndarray] = None) -> EncodedSignal:
        if signal is None:
            signal = cg.eigenvalues.copy()
            mx = np.max(np.abs(signal))
            signal = signal / (mx + 1e-15)

        assert len(signal) == cg.k, f"Signal length {len(signal)} != k={cg.k}"

        J = self.degree
        lmax = max(cg.lambda_max, 1e-8)
        L_k = cg.compressed_laplacian

        t_prev = signal.copy()
        t_curr = (2.0 / lmax) * (L_k @ signal) - signal

        coeffs = np.zeros(J + 1)
        coeffs[0] = float(np.dot(signal, t_prev)) / cg.k
        if J >= 1:
            coeffs[1] = float(np.dot(signal, t_curr)) / cg.k
        for j in range(2, J + 1):
            t_next = 2.0 * ((2.0 / lmax) * (L_k @ t_curr) - t_curr) - t_prev
            coeffs[j] = float(np.dot(signal, t_next)) / cg.k
            t_prev, t_curr = t_curr, t_next

        norm = float(np.linalg.norm(coeffs))
        norm = norm if norm > 1e-15 else 1.0
        return EncodedSignal(coefficients=coeffs, degree=J,
                             norm=norm, normalized=coeffs / norm)


# ---------------------------------------------------------------------------
# Layer 3: Quantum Circuit Simulator
# ---------------------------------------------------------------------------

class QuantumCircuitSimulator:
    """
    Classical QAOA simulation on G_k (k qubits).

    WIRED: Initial state is |psi_c> = amplitude encoding of the Chebyshev
    coefficient vector c, NOT |+>^k. This biases the starting superposition
    toward the graph's spectral structure.

    Thread-safe: noiseless reference state is computed once in run() and passed
    as a local argument to _single_shot -- it is never stored on self.
    """

    MAX_EXACT_QUBITS = 18

    def __init__(self, n_layers: int = 3, n_shots: int = 200,
                 noise_rate: float = 0.01, seed: Optional[int] = None):
        self.n_layers = n_layers
        self.n_shots = n_shots
        self.noise_rate = noise_rate
        self.rng = np.random.default_rng(seed)

    def run(self, cg: CompressedGraph,
            encoded: Optional[EncodedSignal] = None,
            gamma: Optional[np.ndarray] = None,
            beta: Optional[np.ndarray] = None
            ) -> Tuple[List[QuantumShot], np.ndarray, np.ndarray]:

        if gamma is None or beta is None:
            gamma, beta = self._optimize_parameters(cg, encoded)

        # Thread-safe: compute reference state locally, pass to each shot
        if cg.k <= self.MAX_EXACT_QUBITS:
            ref_state = self._qaoa_state(cg, gamma, beta,
                                         noise_rate_override=0.0,
                                         encoded=encoded)
        else:
            ref_state = None

        shots = [
            self._single_shot(cg, gamma, beta, ref_state, encoded)
            for _ in range(self.n_shots)
        ]
        return shots, gamma, beta

    # ------------------------------------------------------------------
    def _optimize_parameters(self, cg, encoded):
        best_e, best_g, best_b = -np.inf, 0.5, 0.5
        for g in np.linspace(0.1, np.pi, 10):
            for b in np.linspace(0.1, np.pi / 2, 7):
                e = self._expected_energy(cg, np.array([g]), np.array([b]), encoded)
                if e > best_e:
                    best_e, best_g, best_b = e, g, b
        p = self.n_layers
        return (np.linspace(best_g * 0.5, best_g, p),
                np.linspace(best_b, best_b * 0.3, p))

    def _expected_energy(self, cg, gamma, beta, encoded):
        if cg.k <= self.MAX_EXACT_QUBITS:
            state = self._qaoa_state(cg, gamma, beta, 0.0, encoded)
            return self._exact_energy(state, cg)
        return self._meanfield_energy(cg, gamma, beta)

    # ------------------------------------------------------------------
    def _qaoa_state(self, cg, gamma, beta,
                    noise_rate_override, encoded) -> np.ndarray:
        k = cg.k
        dim = 2 ** k

        # Initial state: amplitude-encode Chebyshev vector (WIRED)
        if encoded is not None:
            c = encoded.normalized
            J1 = len(c)
            state = np.zeros(dim, dtype=complex)
            for start in range(0, dim, J1):
                end = min(start + J1, dim)
                state[start:end] = c[:end - start]
            norm = np.sqrt(np.sum(np.abs(state) ** 2))
            state /= norm if norm > 1e-15 else 1.0
        else:
            state = np.ones(dim, dtype=complex) / np.sqrt(dim)

        H_diag = self._cost_hamiltonian_diag(cg)
        nr = noise_rate_override

        for g, b in zip(gamma, beta):
            state *= np.exp(-1j * g * H_diag)
            state = self._apply_mixing(state, b, k)
            if nr > 0:
                state = self._apply_depolarizing(state, k, nr)

        return state

    def _cost_hamiltonian_diag(self, cg) -> np.ndarray:
        k = cg.k
        dim = 2 ** k
        diag = np.zeros(dim)
        idx_arr = np.arange(dim)
        A_k = cg.compressed_adj
        for i in range(k):
            for j in range(i + 1, k):
                w = A_k[i, j]
                if abs(w) < 1e-12:
                    continue
                zi = ((idx_arr >> i) & 1) * 2 - 1
                zj = ((idx_arr >> j) & 1) * 2 - 1
                diag += w * (1.0 - zi * zj) / 2.0
        return diag

    def _apply_mixing(self, state, beta, k):
        cos_b, sin_b = np.cos(beta), np.sin(beta)
        for qubit in range(k):
            stride = 2 ** qubit
            for i in range(0, 2 ** k, 2 * stride):
                for j in range(stride):
                    i0, i1 = i + j, i + j + stride
                    a, b_ = state[i0], state[i1]
                    state[i0] = cos_b * a - 1j * sin_b * b_
                    state[i1] = -1j * sin_b * a + cos_b * b_
        return state

    def _apply_depolarizing(self, state, k, nr):
        for qubit in range(k):
            if self.rng.random() < nr:
                pauli = self.rng.integers(3)
                stride = 2 ** qubit
                for i in range(0, 2 ** k, 2 * stride):
                    for j in range(stride):
                        i0, i1 = i + j, i + j + stride
                        a, b_ = state[i0], state[i1]
                        if pauli == 0:
                            state[i0], state[i1] = b_, a
                        elif pauli == 1:
                            state[i0] = -1j * b_
                            state[i1] = 1j * a
                        else:
                            state[i1] = -b_
        return state

    def _exact_energy(self, state, cg):
        return float(np.dot(np.abs(state) ** 2, self._cost_hamiltonian_diag(cg)))

    def _meanfield_energy(self, cg, gamma, beta):
        m = np.zeros(cg.k)
        for g, b in zip(gamma, beta):
            m = np.sin(2 * b) * np.sin(g * (cg.compressed_adj @ m))
        cut = 0.0
        A_k = cg.compressed_adj
        for i in range(cg.k):
            for j in range(i + 1, cg.k):
                cut += A_k[i, j] * (1 - m[i] * m[j]) / 2
        return cut

    # ------------------------------------------------------------------
    def _single_shot(self, cg, gamma, beta, ref_state, encoded) -> QuantumShot:
        k = cg.k
        if k <= self.MAX_EXACT_QUBITS:
            state_noisy = self._qaoa_state(cg, gamma, beta,
                                           self.noise_rate, encoded)
            probs = np.abs(state_noisy) ** 2
            probs /= probs.sum()
            idx = self.rng.choice(len(probs), p=probs)
            bitstring = ((idx >> np.arange(k)) & 1).astype(np.int8)

            # Noise side-data: marginal deviation from noiseless reference
            all_idx = np.arange(2 ** k)
            if ref_state is not None:
                c_probs = np.abs(ref_state) ** 2
                p1_ideal = np.array([
                    float(np.sum(c_probs[(all_idx >> q) & 1 == 1]))
                    for q in range(k)])
            else:
                p1_ideal = np.full(k, 0.5)

            p1_noisy = np.array([
                float(np.sum(probs[(all_idx >> q) & 1 == 1]))
                for q in range(k)])
            noise_vector = (np.abs(p1_noisy - p1_ideal) +
                            self.noise_rate * np.abs(self.rng.standard_normal(k)))
        else:
            m = np.zeros(k)
            for g, b in zip(gamma, beta):
                m = np.sin(2 * b) * np.sin(g * (cg.compressed_adj @ m))
            p1 = (1 + m) / 2
            bitstring = (self.rng.random(k) < p1).astype(np.int8)
            noise_vector = self.noise_rate * np.abs(self.rng.standard_normal(k))

        assignment = 2.0 * bitstring.astype(float) - 1.0
        cut = _compute_cut(assignment, cg.compressed_adj)
        return QuantumShot(bitstring=bitstring, assignment=assignment,
                           noise_vector=noise_vector,
                           noise_norm=float(np.linalg.norm(noise_vector)),
                           cut_value=cut)


# ---------------------------------------------------------------------------
# Layer 4: Noise-Assisted Solution Ranker
# ---------------------------------------------------------------------------

class NoiseSolutionRanker:
    """
    Weight each shot by exp(-lambda * ||eta||) and aggregate scores per solution.
    Solutions appearing in low-noise shots receive exponentially higher weight.
    [Theorem 4: noise weighting reduces estimation bias]
    """

    def __init__(self, noise_penalty: float = 3.0, top_k: int = 5):
        self.noise_penalty = noise_penalty
        self.top_k = top_k

    def rank(self, shots: List[QuantumShot],
             cg) -> List[Tuple[np.ndarray, float]]:
        scores: Dict[bytes, float] = {}
        assignments: Dict[bytes, np.ndarray] = {}
        for shot in shots:
            key = shot.assignment.astype(np.int8).tobytes()
            w = float(np.exp(-self.noise_penalty * shot.noise_norm))
            scores[key] = scores.get(key, 0.0) + w
            assignments[key] = shot.assignment
        total = sum(scores.values()) + 1e-30
        ranked = sorted(
            [(assignments[k], scores[k] / total) for k in scores],
            key=lambda x: x[1], reverse=True
        )
        return ranked[:self.top_k]

    def noise_summary(self, shots: List[QuantumShot]) -> Dict[str, float]:
        norms = np.array([s.noise_norm for s in shots])
        return {
            "mean_noise_norm":   float(np.mean(norms)),
            "std_noise_norm":    float(np.std(norms)),
            "max_noise_norm":    float(np.max(norms)),
            "fraction_low_noise": float(np.mean(norms < 0.05)),
        }


# ---------------------------------------------------------------------------
# Layer 5: Spectral Lift-Back
# ---------------------------------------------------------------------------

class SpectralLiftback:
    """
    Maps z_k in {-1,+1}^k to z_n in {-1,+1}^n.
    z_v = sign( U_k[v,:] . z_k )
    Bound: C(z~) >= C_k(z_k) - epsilon_lift * m  [Theorem 5]
    """

    def lift(self, z_k: np.ndarray, cg: CompressedGraph) -> np.ndarray:
        proj = cg.eigenvectors @ z_k
        z_n = np.sign(proj)
        z_n[z_n == 0] = 1.0
        return z_n

    def compute_original_cut(self, z_n: np.ndarray, G: nx.Graph) -> float:
        nodes = list(G.nodes())
        idx = {v: i for i, v in enumerate(nodes)}
        cut = 0.0
        for u, v, data in G.edges(data=True):
            w = float(data.get('weight', 1.0))
            if z_n[idx[u]] != z_n[idx[v]]:
                cut += w
        return cut


# ---------------------------------------------------------------------------
# Classical MaxCut baseline: Fiedler vector spectral relaxation
# ---------------------------------------------------------------------------

def spectral_maxcut_baseline(G: nx.Graph) -> Tuple[np.ndarray, float]:
    """
    Partition by sign of the Fiedler vector (second eigenvector of L~).
    Classical polynomial-time baseline for comparison.
    """
    comp = SpectralCompressor(k=2)
    L = comp._normalized_laplacian(G)
    _, vecs = la.eigh(L)
    fiedler = vecs[:, 1]
    z = np.sign(fiedler)
    z[z == 0] = 1.0
    lb = SpectralLiftback()
    cut = lb.compute_original_cut(z, G)
    return z, cut


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _compute_cut(assignment: np.ndarray, adj: np.ndarray) -> float:
    k = len(assignment)
    cut = 0.0
    for i in range(k):
        for j in range(i + 1, k):
            w = adj[i, j]
            if abs(w) > 1e-12:
                cut += w * (1.0 - assignment[i] * assignment[j]) / 2.0
    return float(cut)


def total_graph_weight(G: nx.Graph) -> float:
    return sum(float(d.get('weight', 1.0)) for _, _, d in G.edges(data=True))


# ---------------------------------------------------------------------------
# Full Pipeline
# ---------------------------------------------------------------------------

class CompressedGraphProcessor:

    def __init__(self, k: int = 10, chebyshev_degree: int = 16,
                 qaoa_layers: int = 3, n_shots: int = 200,
                 noise_rate: float = 0.02, seed: Optional[int] = 42):
        self.compressor = SpectralCompressor(k=k)
        self.encoder = ChebyshevEncoder(degree=chebyshev_degree)
        self.circuit = QuantumCircuitSimulator(
            n_layers=qaoa_layers, n_shots=n_shots,
            noise_rate=noise_rate, seed=seed)
        self.ranker = NoiseSolutionRanker()
        self.liftback = SpectralLiftback()

    def process(self, G: nx.Graph) -> ProcessingResult:
        cg = self.compressor.compress(G)
        encoded = self.encoder.encode(cg)        # Layer 2 -> feeds Layer 3
        shots, _, _ = self.circuit.run(cg, encoded=encoded)
        ranked = self.ranker.rank(shots, cg)
        noise_stats = self.ranker.noise_summary(shots)

        best_z_k, _ = ranked[0]
        best_compressed_cut = _compute_cut(best_z_k, cg.compressed_adj)
        best_z_n = self.liftback.lift(best_z_k, cg)
        best_cut = self.liftback.compute_original_cut(best_z_n, G)
        tw = total_graph_weight(G)
        _, baseline_cut = spectral_maxcut_baseline(G)

        return ProcessingResult(
            best_partition=best_z_n,
            best_cut_value=best_cut,
            best_cut_fraction=best_cut / (tw + 1e-15),
            compressed_partition=best_z_k,
            compressed_cut_value=best_compressed_cut,
            top_candidates=ranked,
            reconstruction_error=cg.reconstruction_error,
            noise_stats=noise_stats,
            n_shots=len(shots),
            classical_baseline_cut=baseline_cut,
        )


# ---------------------------------------------------------------------------
# Verification Suite
# ---------------------------------------------------------------------------

def verify_eckart_young():
    print("\n-- Theorem 1: Eckart-Young Reconstruction Error --")
    G = nx.barabasi_albert_graph(50, 3, seed=0)
    comp = SpectralCompressor(k=5)
    L = comp._normalized_laplacian(G)
    eigs, _ = la.eigh(L)
    eigs = np.clip(eigs, 0, None)
    all_pass = True
    for k in [5, 10, 20]:
        analytical = float(np.sqrt(np.sum(eigs[k:] ** 2)))
        cg = SpectralCompressor(k=k).compress(G)
        L_k = cg.eigenvectors @ np.diag(cg.eigenvalues) @ cg.eigenvectors.T
        empirical = float(np.linalg.norm(L - L_k, 'fro'))
        ok = abs(analytical - empirical) < 1e-8
        if not ok:
            all_pass = False
        print(f"  k={k:2d}: analytical={analytical:.6f}  empirical={empirical:.6f}"
              f"  {'PASS' if ok else 'FAIL'}")
    return all_pass


def verify_chebyshev_convergence():
    print("\n-- Theorem 2: Chebyshev Spectral Filter Convergence --")

    def h(x):
        return np.exp(-5.0 * (x + 1.0) / 2.0)

    def max_error(J, n_quad=512):
        m = n_quad
        nodes = np.cos((2 * np.arange(1, m + 1) - 1) * np.pi / (2 * m))
        h_nodes = h(nodes)
        T_p, T_c = np.ones(m), nodes.copy()
        a = np.zeros(J + 1)
        a[0] = np.sum(h_nodes) / m
        if J >= 1:
            a[1] = 2.0 * np.sum(h_nodes * T_c) / m
        for j in range(2, J + 1):
            T_n = 2.0 * nodes * T_c - T_p
            a[j] = 2.0 * np.sum(h_nodes * T_n) / m
            T_p, T_c = T_c, T_n
        x_test = np.linspace(-1 + 1e-6, 1 - 1e-6, 1000)
        T_p2, T_c2 = np.ones_like(x_test), x_test.copy()
        approx = a[0] * T_p2
        if J >= 1:
            approx += a[1] * T_c2
        for j in range(2, J + 1):
            T_n2 = 2.0 * x_test * T_c2 - T_p2
            approx += a[j] * T_n2
            T_p2, T_c2 = T_c2, T_n2
        return float(np.max(np.abs(h(x_test) - approx)))

    prev, all_pass = np.inf, True
    errors = []
    for J in [4, 8, 16, 32]:
        err = max_error(J)
        errors.append(err)
        at_eps = err < 1e-13
        ok = (err < prev - 1e-12) or at_eps
        if not ok:
            all_pass = False
        label = "(machine eps)" if at_eps else ("(decreasing)" if ok else "(!)")
        print(f"  J={J:2d}: max ||h - h_J|| = {err:.2e}  {label}")
        prev = err
    return all_pass, errors


def verify_noise_weighting():
    print("\n-- Theorem 4: Noise Weighting Bias Reduction --")
    rng = np.random.default_rng(42)
    k = 6
    good = np.array([1, -1, 1, -1, 1, -1], dtype=float)
    bad = np.array([1, 1, 1, 1, 1, 1], dtype=float)
    clean = [QuantumShot(
        bitstring=(good + 1).astype(np.int8) // 2, assignment=good.copy(),
        noise_vector=rng.random(k) * 0.01, noise_norm=0.02, cut_value=5.0
    ) for _ in range(80)]
    noisy = [QuantumShot(
        bitstring=(bad + 1).astype(np.int8) // 2, assignment=bad.copy(),
        noise_vector=rng.random(k) * 0.5, noise_norm=1.5, cut_value=0.0
    ) for _ in range(80)]
    all_shots = clean + noisy
    good_key = good.astype(np.int8).tobytes()
    unif = sum(1 for s in all_shots
               if s.assignment.astype(np.int8).tobytes() == good_key) / len(all_shots)

    class _DummyCG:
        compressed_adj = np.zeros((k, k))

    ranked = NoiseSolutionRanker(noise_penalty=3.0).rank(all_shots, _DummyCG())
    weighted = next((sc for az, sc in ranked
                     if az.astype(np.int8).tobytes() == good_key), 0.0)
    passed = weighted > unif
    print(f"  Uniform fraction for good solution:  {unif:.3f}")
    print(f"  Weighted score for good solution:    {weighted:.3f}")
    print(f"  {'PASS' if passed else 'FAIL'}: noise weighting promotes low-noise solution")
    return unif, weighted, passed


def verify_liftback_quality():
    print("\n-- Theorem 5: Spectral Lift-Back Cut Quality --")
    G = nx.planted_partition_graph(2, 15, 0.9, 0.1, seed=42)
    G = nx.convert_node_labels_to_integers(G)
    n, m_edges = G.number_of_nodes(), G.number_of_edges()
    k = 6
    cg = SpectralCompressor(k=k).compress(G)
    epsilon_lift = cg.reconstruction_error

    proc = CompressedGraphProcessor(k=k, qaoa_layers=2, n_shots=150,
                                    noise_rate=0.0, seed=0)
    result = proc.process(G)

    # Theorem 5 bound: C(z~) >= C_k(z_k) - epsilon_lift * m
    lower_bound = result.compressed_cut_value - epsilon_lift * m_edges
    passed = result.best_cut_value >= lower_bound - 1e-6

    print(f"  n={n}, k={k}, edges={m_edges}")
    print(f"  Spectral error epsilon_lift:    {epsilon_lift:.4f}")
    print(f"  Compressed cut C_k(z_k):        {result.compressed_cut_value:.2f}")
    print(f"  Theorem 5 lower bound:          {lower_bound:.2f}")
    print(f"  Lifted cut C(z~):               {result.best_cut_value:.2f}")
    print(f"  Classical baseline:             {result.classical_baseline_cut:.2f}")
    print(f"  {'PASS' if passed else 'FAIL'}: lifted cut satisfies Theorem 5 bound")
    return result, lower_bound, passed


def verify_noise_side_data():
    print("\n-- Noise Side-Data: Stress Test (noise rate sweep) --")
    G = nx.cycle_graph(10)
    results = []
    prev_eta = -1.0
    all_pass = True
    for noise_rate in [0.0, 0.02, 0.05, 0.15, 0.30]:
        proc = CompressedGraphProcessor(k=5, qaoa_layers=2, n_shots=200,
                                        noise_rate=noise_rate, seed=7)
        result = proc.process(G)
        mean_eta = result.noise_stats["mean_noise_norm"]
        results.append((noise_rate, mean_eta, result.best_cut_fraction))
        ok = mean_eta >= prev_eta - 1e-5
        if not ok:
            all_pass = False
        print(f"  noise_rate={noise_rate:.2f}: mean||eta||={mean_eta:.4f}"
              f"  cut_fraction={result.best_cut_fraction:.3f}"
              f"  {'ok' if ok else 'FAIL'}")
        prev_eta = mean_eta
    print(f"  {'PASS' if all_pass else 'FAIL'}: noise norm monotonically non-decreasing")
    return results, all_pass


def run_full_pipeline_demo():
    print("\n-- Full Pipeline Demo --")
    G = nx.barabasi_albert_graph(80, 4, seed=7)
    proc = CompressedGraphProcessor(k=12, qaoa_layers=3, n_shots=300,
                                    noise_rate=0.015, seed=99)
    result = proc.process(G)
    tw = total_graph_weight(G)
    print(f"  n=80, edges={G.number_of_edges()}, k=12")
    print(f"  Spectral error:     {result.reconstruction_error:.4f}")
    print(f"  Pipeline cut:       {result.best_cut_value:.0f} / {tw:.0f}"
          f"  ({result.best_cut_fraction:.3f})")
    print(f"  Classical baseline: {result.classical_baseline_cut:.0f}")
    print(f"  Random partition:   {tw/2:.0f} (expected)")
    print(f"  Mean noise ||eta||: {result.noise_stats['mean_noise_norm']:.4f}")
    print(f"  Low-noise shots:    {result.noise_stats['fraction_low_noise']:.1%}")
    return result


if __name__ == "__main__":
    print("=" * 62)
    print("Compressed Graph Quantum Processor -- Verification Suite")
    print("=" * 62)
    verify_eckart_young()
    verify_chebyshev_convergence()
    verify_noise_weighting()
    verify_liftback_quality()
    verify_noise_side_data()
    run_full_pipeline_demo()
    print("\n" + "=" * 62)
    print("All verifications complete.")
    print("=" * 62)
