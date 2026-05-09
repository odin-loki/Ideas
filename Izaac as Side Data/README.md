# Izaac as Side Data — applied side-information papers in the Izaac framework

> **Two papers + a reference implementation.** The local papers explore how **shared deterministic randomness** (Izaac's σ-state) acts as side information in compression, distributed computing, and cryptographic protocols. The full Izaac mathematical framework lives in `../Compression Algorithms/`; this folder is the applied / protocols slice.

---

## 🌐 What this folder is

The Izaac algorithm is a single computational primitive — a deterministic shared-randomness function — from which a wide range of cryptographic, distributed-systems, and compression protocols can be derived. The **canonical Izaac paper** lives in [`../Compression Algorithms/izaac_algorithm_research_paper.md`](../Compression%20Algorithms/izaac_algorithm_research_paper.md).

This folder contains two applied papers plus a Python reference implementation. Earlier README copy listed companion files (`Izaac_Mathematical_Framework.pdf`, `izaac_algorithm_research_paper.md`, `NMP_neural_compression_research_paper.md`, `GRIA_Technical_Memorandum.md`) that **do not exist in this folder** — those documents either live in `Compression Algorithms/` or do not exist at all. The list below reflects the actual contents.

Attribution: **Technical research paper / applied research paper · March 2026**.

---

## 📄 Files

| File | Role |
|------|------|
| [`izaac_paper1_theoretical.md`](izaac_paper1_theoretical.md) | *The Izaac algorithm: shared deterministic randomness as a computational primitive* — local theoretical paper covering pseudorandomness, state-compression bound, fast-forward, zero-communication Byzantine consensus, Shannon-limit-breaking compression, unified information-theoretic meta-theorem |
| [`izaac_paper2_applications.md`](izaac_paper2_applications.md) | *Izaac protocol suite* — twelve concrete protocols (VRF, NI-MPC, Byzantine consensus, probabilistic data structures, reproducible Monte Carlo, coordinated differential privacy, deterministic fuzzing, backtest commitment, lazy infinite data structures, content-addressed storage, synchronised rate limiting, MAC scheduling) |
| [`izaac_implementation.py`](izaac_implementation.py) | Python 3 reference implementation |
| **External reference (canonical):** [`../Compression Algorithms/izaac_algorithm_research_paper.md`](../Compression%20Algorithms/izaac_algorithm_research_paper.md) | Full Izaac mathematical framework |

---

## 🔑 Core idea (from paper 1)

Parties sharing a compact cryptographic state σ ∈ {0,1}^S can derive arbitrarily long, identical pseudorandom sequences from purely **local** computation — creating what the paper calls a **"free broadcast channel"** with zero latency and infinite effective bandwidth. The Meta-Theorem of §4 identifies shared deterministic randomness as **information-theoretically equivalent** to a free broadcast channel, collapsing a rich space of communication-lower-bound barriers across distributed computing, cryptography, and information theory.

Standard instantiations: **AES-CTR**, **ChaCha20**, **SHA-3 XOF** with σ as key and a counter/context as input. Default state size 256 bits (paranoid: 512 bits for post-quantum resistance).

---

## 📐 Headline theorems (paper 1)

| Theorem | Statement |
|---------|-----------|
| **3.1 Pseudorandomness** | Izaac-output indistinguishability reduces to PRF security of the underlying primitive |
| **3.2 State Compression Bound** | Tight Θ(λ + log k) state complexity for k-bit pseudorandom output |
| **3.3 Fast-Forward** | O(log n) computation of any index without evaluating prior outputs |
| **3.5 Shannon-Limit Breaking** | Compression below classical Shannon entropy via shared side information (e.g. ~1.2 bits/char for English given σ) |
| **3.6 Zero-Communication Byzantine Consensus** | Sortition-based protocol with optimal f < n/3 fault tolerance and zero post-setup communication |
| **Meta-Theorem (§4)** | Shared σ ≡ free broadcast channel (information-theoretically) |

---

## 🛠 Twelve protocols (paper 2)

1. **Izaac-VRF** — verifiable random function for blockchain leader election, provably-fair gaming, lottery, DNSSEC zone-enumeration resistance.
2. **NI-MPC** — non-interactive multi-party computation; privacy via simulation, correctness via mask cancellation.
3. **Deterministic Byzantine consensus** — zero post-setup communication, f < n/3 tolerance.
4. **Space-efficient probabilistic data structures** — Bloom-filter-class structures sharing hash state.
5. **Reproducible Monte Carlo simulation** — O(log n) fast-forward enables replay and parallel chunking.
6. **Coordinated differential privacy** — consistent answers to repeated queries across parties.
7. **Deterministic coverage-guided fuzzing** — reproducible bug reports with shared seed.
8. **Algorithmic-trading backtest commitment** — regulator-verifiable replays for compliance.
9. **Lazy infinite data structures** — generated on demand from compact seeds.
10. **Content-addressed distributed storage** — cryptographic replica placement.
11. **Synchronised rate limiting** — without datacentre coordination.
12. **Network protocol synchronisation** — collision-free MAC scheduling.

The whole suite is implemented in **< 2 000 lines** of well-documented Python (using `hashlib` SHA-3-256, `os.urandom`, `struct`).

---

## 🔐 Security framing

Standard computational security model. Adversary is non-uniform polynomial-time, may observe public outputs and proofs, may adaptively query Izaac on chosen inputs (excluding the target), and may corrupt up to f < n/3 parties in consensus protocols. Quantum adversaries handled via enlarged state sizes (λ = 256 paranoid, λ = 512 post-quantum).

---

## 🚧 Honest framing

- Both papers are **research-grade** and not audited for production cryptographic deployment. The reference implementation prioritises clarity over throughput.
- Several protocols rely on the **trusted-setup or interactive-setup** assumption that all parties share σ; bootstrapping σ securely is out of scope.
- The Shannon-limit-breaking compression result depends on the existence of valid shared side information — it does **not** contradict Shannon's theorem in the absence of such information.

---

## 🔗 Related work in this repo

- [`../Compression Algorithms/`](../Compression%20Algorithms/) — **canonical home** of Izaac (`izaac_algorithm_research_paper.md`) plus GRIA and NMP frameworks
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — uses a Meta-DAG RNG of similar lineage to Izaac; explicit AEAD cipher
- [`../RNGS/`](../RNGS/) — RNG zoo; Boolean / Chaotic / DAG / Turbulent-flow RNG families
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — GF(2) algebra and the GRIA spectrum theorem
- [`../Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator with hash-based context compression

---

[← Back to main README](../README.md)
