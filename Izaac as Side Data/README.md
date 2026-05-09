# Izaac as Side Data — applied shared-PRF coordination protocols

> **The engineered protocol suite that operationalises the Izaac meta-theorem ("shared deterministic PRF ≡ free broadcast channel") into twelve concrete protocols spanning verifiable random functions, non-interactive MPC sum, leader election, coordinated Bloom filters, Monte Carlo checkpointing, distributed rate limiting, fuzz-test seed coordination, and more.** Where the canonical Izaac framework in [`../Compression Algorithms/`](../Compression%20Algorithms/) develops the theory, this folder turns the meta-theorem into a < 2000-LOC Python reference implementation with explicit complexity tables, soundness bounds, and side-by-side comparisons against PBFT, HotStuff, and the standard 384-bit-per-element Bloom-filter construction. The headline operational claim: a Bloom filter coordinated by an Izaac shared seed saves `N × 384` bits of message overhead — for `N = 10⁶`, that is **48 MB** moved off-wire per coordination round.

---

## What this folder is

The Izaac framework lives or dies by what you can actually *do* with shared deterministic randomness. This folder is the answer in twelve concrete protocols, each with: an algorithmic specification, a soundness or correctness bound, and a comparison to the standard non-Izaac approach. The framing is "side data" — the σ stream is auxiliary information that both parties already have, so any protocol step that classically requires a coordination message can be eliminated.

Most ambitious of the twelve is the **non-interactive MPC sum**: each participant masks their input with `Izaac(σ, encode(i, j))`, contributions are added, masks cancel, and the aggregate emerges with **perfect privacy under the semi-honest model**. The folder cites a sister line of work showing **30 % throughput improvement / 100 % privacy** on sum-MPC benchmarks vs. masked-noise baselines.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`izaac_paper1_theoretical.md`](izaac_paper1_theoretical.md) | Theoretical foundations. `CTR-mode O(1)` vs `tree O(log n)` fast-forward analysis; Grover-bound discussion (`σ` doubling for post-quantum margin). |
| [`izaac_paper2_applications.md`](izaac_paper2_applications.md) | Twelve-protocol catalogue. VRF, NI-MPC sum, leader election, Bloom-filter coordination, Monte Carlo checkpoints, rate limiting, fuzz seeds, etc. **§4.3 explicitly clarifies** that "zero-communication" applies to leader selection, not proposal propagation, and cites Dolev–Reischuk's `Ω(n²)` bits worst-case lower bound. |
| [`izaac_implementation.py`](izaac_implementation.py) | **< 2000 LOC** Python reference. |

---

## 🧠 The twelve protocols (selected)

### Verifiable Random Function (VRF)

`pk = SHA-3-256(σ)`. `Eval(x)` returns `y = Izaac(σ, x)` and a zero-knowledge proof. **Soundness: `2⁻¹²⁸`.**

### Non-interactive MPC sum

Each participant masks input `x_i` with `Izaac(σ, encode(i, j))` for round `j`. Contributions sum; masks cancel by construction. Perfect privacy under semi-honest model. Cited literature alignment: SRFG benchmark `30 % throughput / 100 % privacy` for sums.

### Leader election

PBFT round needs `~10 000` messages at `n = 100, f = 33`. HotStuff: `~100`. **Izaac leader-select: `0` messages post-setup** — but the paper immediately clarifies that the *leader still broadcasts its proposal*, so the saving applies to *selection*, not to the entire round.

| n = 100, f = 33 | Round messages |
|---|---|
| PBFT | ~10 000 |
| HotStuff | ~100 |
| **Izaac leader-select** | **0 (post-setup)** |

### Coordinated Bloom filter

For `N = 10⁶`, `k = 10` hashes per element, classical seeded Bloom transmits `N × 384 = 48 MB` of seed material per coordination round. Izaac eliminates this — both sides derive identical seeds from σ. **48 MB saved per round.**

### Monte Carlo checkpointing

Cross-machine reproducibility without serialising RNG state.

### Rate limiting

Distributed per-user limits without coordination round-trips.

### Fuzz-test seed coordination

Eight machines fuzzing the same target without duplicating effort or missing seeds.

(Six more in the paper.)

---

## 🚧 Honest caveats (paper §4.3 explicit)

- **"Zero communication" applies to leader selection only.** The leader still broadcasts proposals; consensus is not magically free.
- **Dolev–Reischuk lower bound: `Ω(n²)` bits in the worst case for Byzantine consensus.** Izaac doesn't violate this; it amortises setup so the *amortised steady-state* messages drop, not the worst-case.
- **Malicious-security extensions** (additive MPC against active adversaries) need additional rounds beyond the semi-honest construction.
- **Suite §9 benchmarks** are referenced as measured on x86, but the spec-level portions of the paper review here are not yet anchored to measured tables.
- **σ compromise = entire suite compromised** — this is a property of the underlying Izaac framework, not specific to applications.

---

## 🎯 What this displaces

| Standard | Cost | What Izaac side-data eliminates |
|---|---|---|
| Distributed Bloom filter | `N × 384` bits seed exchange | All of it |
| PBFT consensus | `~10 000` msgs / round at n=100 | Selection cost (proposal still broadcast) |
| Coordinator-elected fuzzing | round-trips per seed assignment | All of it |
| Cryptographic VRFs (e.g. RFC 9381) | full key infrastructure | Lighter setup, same soundness target |
| Synchronised RNG checkpointing | serialise + ship RNG state | σ is identical on both sides |

---

## 🔗 Related work in this repo

- [`../Compression Algorithms/`](../Compression%20Algorithms/) — Izaac canonical home (theorems and meta-theorem live there)
- [`../RNGS/`](../RNGS/) — RNG portfolio: Izaac's σ stream needs a CSPRNG underneath
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — keyed entropy pump using a sister Meta-DAG RNG
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — finite-field algebraic foundations
- [`../Statistical Generation/`](../Statistical%20Generation/) — sister information-theoretic framework

---

[← Back to main README](../README.md)
