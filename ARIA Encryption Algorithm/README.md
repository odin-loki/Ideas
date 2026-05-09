# ARIA Encryption Algorithm — Algebraic Resynchronisation and Integrity Architecture (ARIA)

> **ARIA = Algebraic Resynchronisation and Integrity Architecture.** An AEAD-style authenticated-encryption scheme whose distinguishing property is **synchronous, receiver-recomputable nonces** that are *never transmitted* — the receiver derives its nonce from the message and a session key the same way the sender did, so loss of nonce sync (a well-known operational pain point in AES-GCM, ChaCha20-Poly1305, and GCM-SIV deployments) becomes structurally impossible. Built on a **three-layer algebraic tower** over `GF(2²⁵⁶)`, with a **session-key-seeded Meta-DAG RNG** as the entropy pump and **dual collision analyses** (a PRF-style bound and a syndrome-decoding-style bound on a [2048, 256] code).

> **Naming caveat.** This is *not* the Korean ARIA block cipher. The local ARIA acronym expands to **Algebraic Resynchronisation and Integrity Architecture**. The two are unrelated.

---

## What this folder is

Modern authenticated encryption is dominated by AES-GCM, ChaCha20-Poly1305, and AES-GCM-SIV, all of which are excellent at the cryptographic primitive layer and *terrible* at one specific operational concern: **nonce management under loss-of-state**. If a sender and receiver fall out of sync — link drop, restart, replay defence at the wrong granularity — recovering nonce uniqueness without leaking key material or repeating IVs is genuinely hard, and most deployment incidents in the wild are nonce mishandling rather than primitive failures. ARIA's pitch is structural: by making the nonce a deterministic function of the message and the session key (`N(M, sk) = C(M, sk) · β_vec`), the receiver can recompute it; nothing transmitted, nothing to lose, nothing to mismatch.

The cost is that the nonce isn't a fresh random value, so the security argument has to handle a different threat model: collision resistance of the nonce-derivation function under chosen-message attack, plus all the usual AEAD properties on top. The papers in this folder argue the bound `Adv_COLL ≤ min(ε_PRF + 7Q²/2²⁵⁷, 2⁻⁸⁶)` and provide a constructive Python "reduction simulator" that walks the proof's syndrome-decoding step on a `GF(2¹⁶)` toy field for sanity-checking.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`ARIA_Research_Paper.md`](ARIA_Research_Paper.md) | Full research paper. Defines the three-layer tower, the nonce derivation, the Meta-DAG RNG, the collision bound, and the SDP-style alternative bound. |
| [`ARIA_Specification.md`](ARIA_Specification.md) | Implementation specification. Modes 1–3, packet layouts, profile table, projected throughput tiers. |
| [`aria.py`](aria.py) | Reference Python implementation. `ARIASession` class, three-mode `aria_encrypt` / `aria_decrypt`, `run_tests` (61 tests), `sdp_reduction_verify` toy-field sanity checks. |

---

## 🧠 The three-layer algebraic tower

| Layer | Definition | Role |
|---|---|---|
| **F₁ = GF(2²⁵⁶)** | irreducible `p(x) = x²⁵⁶ + x¹⁰ + x⁵ + x² + 1` | Base field. Word-sized arithmetic. |
| **L₂ = F₁[y] / (y⁸ + y⁴ + y³ + y + 1)** | Degree-8 extension over `F₁` | Mid-layer mixing. |
| **L₃ = L₂[z] / (z⁴ + z + 1)** | Degree-4 extension over `L₂` | "Hiding" space (~8192 bits of structure for diffusion). |

**Nonce derivation.** `N(M, sk) = C(M, sk) · β_vec` with Vandermonde `β = H("aria:beta:" ‖ sk)`. Mixing operators `δ` (collapse) and `α` (tag).

**Modes.** Three operating modes target different threat / overhead profiles:

| Mode | Mechanism | Overhead vs. AES-GCM |
|---|---|---|
| **Mode 1** | DAG-stream-based | +22 B |
| **Mode 2** | Random salt + DAG | +22 B |
| **Mode 3** | Evaluation-point drift | +34 B |

---

## 🌀 Meta-DAG RNG

The entropy pump. Eight-node DAG with **transcendental-derived 64-bit seeds** (π, e, √2, φ, ζ(3), γ, Catalan's constant, Glaisher–Kinkelin), cross-mixing edges to nodes `(i+3)` and `(i+5)`, a `meta_state` mix step, and a four-round emission producing one `GF(2²⁵⁶)` word per call.

The same DAG architecture appears in [`../RNGS/DAG RNG/`](../RNGS/DAG%20RNG/) as a standalone PRNG; here it is the keyed entropy pump for AEAD.

---

## 📊 Reported reference-implementation profile (paper / spec)

Pure-Python timings on author hardware:

| Operation | Throughput |
|---|---|
| GF(2²⁵⁶) multiply | ~46.1 µs |
| Meta-DAG `next_gf256` | ~198 740 / s |
| `aria_encrypt` (Modes 1–3) | ~155–175 / s |
| AEAD round-trip (encrypt + decrypt + verify) | ~68–69 / s |

**Avalanche.** ~49.8 % of the 128 tag bits flip per single-bit flip in `β` (Mode 3 narrative).

**Projected throughputs** (PCLMULQDQ + AES-NI, native speed): GF mul ~33 ns, encryption tier `>10⁶ enc/s`. **These are projections, not measurements.**

---

## 🛡 Security analysis (two bounds)

**Bound 1 (PRF-style).** `Adv_COLL ≤ ε_PRF + 7Q²/2²⁵⁷`. With `Q ≤ 2⁶⁴` queries, this gives the headline corollary `~ε_PRF + 2⁻¹²⁶`.

**Bound 2 (SDP / syndrome-decoding-style).** Maps the collision problem to syndrome decoding on a `[2048, 256]` code with `t = 7` errors, rate `1/8`. Stated complexities: classical ISD `~2⁸⁶`, quantum (Grover-aided) `~2⁴³`. **The quantum margin is what motivates the paper's upgrade path to `GF(2⁵¹²)` for post-quantum work.**

The take-away is `min(ε_PRF + 7Q²/2²⁵⁷, 2⁻⁸⁶)` — quoted as the active bound for any realistic adversary.

---

## 🚧 Honest caveats (paper §, lines L1–L7)

- **No formal EUF-CMA proof of the tag yet.** The collision bound is the cornerstone; tag unforgeability under chosen-message attack is argued informally.
- **Meta-DAG PRF security is not fully formally proven.** The transcendental-seed claim is "looks like a CSPRNG" rather than reduced to a hardness assumption.
- **`aria.py` uses SHA-256 as a keystream placeholder.** A production version should use AES-256-CTR keyed off the tag. The keystream choice is implementation, not protocol.
- **Post-quantum margin requires the field upgrade** to `GF(2⁵¹²)`. As shipped, ISD-Grover gives only `~2⁴³` advantage — too thin against a sufficiently-resourced quantum adversary.
- **No external audit.** No third-party cryptographer has reviewed the construction.
- **No side-channel analysis.** Timing-side-channel hardening is not addressed.
- **`L₃` contribution is not quantified.** The spec asserts `L₃` adds diffusion but does not pin the marginal effect.
- The folder labels itself **prototype, not for production**.

---

## 🎯 What this displaces

| Standard scheme | Pain point | What ARIA solves |
|---|---|---|
| AES-GCM | Nonce reuse → catastrophic key recovery | Nonce derived deterministically from message + sk |
| ChaCha20-Poly1305 | Counter management across reboots / link drops | Same nonce-recompute property |
| AES-GCM-SIV | Higher overhead, still requires nonce input | Nonce *recomputed* not transmitted |

ARIA does not claim to be faster than AES-NI-accelerated AEAD; it claims to be **structurally robust to the operational class of failure modes that produces most real-world AEAD incidents**.

---

## 🔗 Related work in this repo

- [`../Compression Algorithms/`](../Compression%20Algorithms/) — Izaac framework (shared deterministic-PRF idea, applied to side-information rather than encryption)
- [`../RNGS/DAG RNG/`](../RNGS/DAG%20RNG/) — standalone Meta-DAG RNG (same architecture, unkeyed application)
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — finite-field arithmetic foundations
- [`../Break AES/`](../Break%20AES/) — adjacent cryptanalysis research (different direction)
- [`../Veritas/`](../Veritas/) — formal-verification framework that could be applied to the missing EUF-CMA proof

---

[← Back to main README](../README.md)
