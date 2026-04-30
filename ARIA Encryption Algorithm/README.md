# ARIA — Algebraic Resynchronisation and Integrity Architecture

> **🔐 Overview**: A stateless authenticated-encryption (AEAD) scheme for high-assurance communications, built on a three-layer algebraic tower over **GF(2²⁵⁶)** with **dual security reductions** (SHA-256 PRF and NP-hard Syndrome Decoding).

---

## 🔐 Overview

**ARIA** (the local scheme described in this folder, *not* the Korean ARIA block cipher) stands for **Algebraic Resynchronisation and Integrity Architecture**. It is an authenticated-encryption-with-associated-data (AEAD) construction whose central contribution is **syncable nonce derivation**: sender and receiver independently compute identical nonces from a shared session key and message content, eliminating any need for transmitted nonces or persistent counter state.

Authored by *O. [Redacted], Independent Defence Research, March 2026*. A Python reference implementation accompanies the papers; **all 61 automated test cases pass**.

> **Naming note.** This scheme shares an acronym with the Korean ARIA block cipher (Kwon et al., 2003) but is unrelated to it. The Korean ARIA is a 128-bit substitution-permutation network; this ARIA is an AEAD construction over a finite-field tower. Don't confuse them.

### Key features

- **Stateless syncability** — no transmitted nonce, no sender-side counter; receiver recomputes the nonce from the sequence number alone.
- **Three operational modes** for different tactical regimes: DAG stream injection, random salt injection, evaluation-point drift.
- **Dual security reductions** — collision advantage bounded by both SHA-256 PRF security *and* the NP-hardness of Syndrome Decoding on a [2048, 256] binary linear code.
- **Verified reference** — 61 passing tests, integrated profiler, executable security-reduction simulators.

---

## 📄 Core Documents

| Document | What it is |
|---|---|
| [`ARIA_Research_Paper.md`](ARIA_Research_Paper.md) | Full-length research paper: motivation, mathematical foundations, all proofs, performance, limitations |
| [`ARIA_Specification.md`](ARIA_Specification.md) | Implementable cryptographic specification (production prototype) |
| [`aria.py`](aria.py) | Python reference implementation with 61 tests + profiler |

---

## 🧮 Mathematical Foundations

The scheme is built on a three-layer algebraic tower:

| Layer | Definition | Element space |
|---|---|---|
| **F₁** | GF(2²⁵⁶) = GF(2)[x] / p(x), with p(x) = x²⁵⁶ + x¹⁰ + x⁵ + x² + 1 (irreducible pentanomial) | 2²⁵⁶ |
| **L₂** | F₁[y] / Q₂(y), Q₂(y) = y⁸ + y⁴ + y³ + y + 1 | 2²⁰⁴⁸ |
| **L₃** | L₂[z] / Q₃(z), Q₃(z) = z⁴ + z + 1 | 2⁸¹⁹² |

The **nonce map** is a linear function of the message coefficient matrix:

> **N(M, sk) = C(M, sk) · β_vec  in GF(2²⁵⁶)**

where β_vec = [1, β, β², …, β⁷]ᵀ is a Vandermonde evaluation vector and β = H("aria:beta:" ‖ sk). Linearity gives **N(M) ⊕ N(M′) = D(β)** for the difference polynomial D — and this is the structural property that connects nonce collisions to Syndrome Decoding (see Theorem 2 below).

---

## 🎲 Meta-DAG Random Number Generator

A deterministic shared-entropy source with **eight cross-mixed nodes**, each seeded from a distinct transcendental constant (π, e, √2, φ, ζ(3), γ, Catalan's constant G, Glaisher–Kinkelin A). After each round, node *i* is cross-mixed with nodes (*i*+3) mod 8 and (*i*+5) mod 8 — the prime step sizes guarantee the mixing graph covers all eight nodes with no subset evolving independently.

Both parties seeded identically from the session key produce identical GF(2²⁵⁶) output streams. After packet loss the receiver fast-forwards to step `seq × 64` from the session key — no stored state required.

Profiled throughput: **198,740 next_gf256() calls/sec** (Python reference).

---

## 🛰️ Operational Modes

| Mode | Wire overhead | DAG sync? | Same-plaintext protection | Best for |
|---|---|---|---|---|
| **Mode 1 — DAG stream injection** | 22 B (4 B seq + 16 B tag + headers) | Yes (seq-based) | Yes — DAG stream | Point-to-point radio, reliable ordering |
| **Mode 2 — Random salt injection** | 34 B | No | Yes — random salt | Multi-path, disruption-tolerant |
| **Mode 3 — Evaluation-point drift** | 22 B | No | Yes — point drift | Repeated-message retransmission |

The nonce is **never transmitted**. Each mode produces distinct ciphertexts for identical plaintexts under the same session key.

---

## 🛡️ Formal Security

**Main result:**

> Adv_COLL(A) ≤ min( ε_PRF + 7Q² / 2²⁵⁷ ,  2⁻⁸⁶ )

The first bound comes from **Theorem 1** (PRF reduction): any nonce-collision finder yields a SHA-256 PRF distinguisher. The second bound comes from **Theorem 2** (SDP reduction): finding a collision is at least as hard as decoding a [2048, 256] binary linear code — NP-complete by Berlekamp, McEliece & van Tilborg (1978). The best classical attack is Information Set Decoding at ~2⁸⁶ operations (Becker–Joux–May–Meurer 2012).

| Attack vector | Classical | Quantum | Basis |
|---|---|---|---|
| PRF key recovery | 2¹²⁸ | 2⁶⁴ (Grover) | SHA-256 PRF |
| Polynomial collision (SDP) | ~2⁸⁶ | ~2⁴³ (Grover + ISD) | NP-hard |
| Brute-force birthday | 2¹²⁸ at Q = 2¹²⁸ | 2⁶⁴ | Unconditional |
| GF(2⁵¹²) upgrade path | 2¹⁶² | ~2⁸¹ | Post-quantum margin |

Both reductions are **constructive and numerically validated** in the reference implementation.

---

## 📊 Performance

Pure Python 3.12 reference (algorithmic complexity, not production speed):

| Operation | Avg µs | Throughput |
|---|---|---|
| GF(2²⁵⁶) multiply | 46.1 | 21,714 /s |
| L2 Horner eval | 342 | 2,921 /s |
| L3 collapse to GF(2²⁵⁶) | 1,453 | 688 /s |
| DAG next_gf256 (4 rounds) | 5.0 | 198,740 /s |
| `aria_encrypt` Mode 1 | 6,447 | 155 /s |
| AEAD round-trip Mode 1 | 14,620 | 68 /s |

Production projections by acceleration tier:

| Stage | GF mul | AEAD throughput |
|---|---|---|
| Naive C (−O3) | ~652 ns | ~5,000 /s |
| C + PCLMULQDQ | ~33 ns | ~100,000 /s |
| C + PCLMULQDQ + AES-NI | ~5 ns | ~2,000,000 /s |
| AVX-512 (8-way parallel) | ~5 ns/lane | ~10,000,000 /s |

Sufficient for all STANAG tactical communication profiles up to high-speed data networks.

---

## ⚠️ Known Limitations

The reference is a research prototype, not a production primitive. Open issues (from the paper):

1. **No EUF-CMA proof** for the authentication tag — unforgeability argument is heuristic.
2. **DAG-RNG PRF security** is argued via SHA-256 but not independently proven for the meta-operation structure.
3. **SHA-256 keystream is a placeholder** — production must use AES-256-CTR keyed from the tag.
4. **Quantum SDP margin** is ~2⁴³ at GF(2²⁵⁶); upgrade to GF(2⁵¹²) raises this to ~2⁸¹.
5. **No external cryptographic audit** has been performed. **Required before any deployment.**
6. **No side-channel analysis** — constant-time arithmetic and timing/power-analysis assessment outstanding.
7. **L₃ security contribution** not formally quantified beyond the SDP bound.

---

## 🔗 Related Work

This work connects to:

- **GF2 Algebra and Applications** — algebraic foundations for binary fields used here
- **Cypha** — independent work also using GF(2ⁿ) extension fields
- **Compression Algorithms** — shared mathematical machinery (polynomial Horner evaluation, Vandermonde structure)
- **Break AES** — adjacent cryptanalytic research

---

## 📖 See Also

- [`EDITORIAL_ROADMAP.md`](../EDITORIAL_ROADMAP.md) — editorial standards and batch history
- [`EDITORIAL_STYLE.md`](../docs/EDITORIAL_STYLE.md) — house style guide
- [`GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — binary field theory
- [`Break AES/`](../Break%20AES/) — adjacent cryptanalytic notes
- [`Compression Algorithms/`](../Compression%20Algorithms/) — related algebraic-information work

---

## 🛡️ About This Project

This project documents an authenticated-encryption scheme with formal security reductions to two distinct hardness assumptions, accompanied by an executable Python reference. The goals are:

- Eliminate counter-state synchronisation as an operational liability in tactical communications
- Provide a structural NP-hardness floor (SDP) alongside the conventional PRF-based bound
- Expose the construction in implementable form for review, experimentation, and cryptanalytic scrutiny

**Not for production deployment.** External cryptographic audit and the engineering hardening listed in §10 of the research paper are prerequisites for any operational use.

[← Back to main README](../README.md)
