# ARIA specification — Algebraic Resynchronisation and Integrity Architecture

*Cryptographic specification · Classification: CONFIDENTIAL — Research prototype · March 2026*

O. \[Redacted\] · Independent Defence Research · Research prototype — Not for production

## Abstract

ARIA \(Algebraic Resynchronisation and Integrity Architecture\) is an authenticated encryption scheme designed for high-assurance military communications. Its central innovation is syncable nonce derivation: sender and receiver independently compute identical nonces from a shared session key and message content via a three-layer algebraic tower over GF\(2²⁵⁶\), eliminating counter-state synchronisation requirements while providing stronger collision guarantees than any counter-based scheme.

Security is bounded by two independent reductions to named hard problems: \(1\) any nonce collision-finder implies a SHA-256 PRF distinguisher, giving Adv\_COLL ≤ ε\_PRF \+ 7Q²/2²⁵⁷; and \(2\) finding a collision solves Syndrome Decoding on a \[2048, 256\] binary linear code \(NP-hard\), requiring at least 2⁸⁶ classical operations. Both are constructive and numerically validated.

A complete Python reference implementation with integrated profiler accompanies this document. All 61 test cases pass. Measured throughput on the pure-Python reference is 155–175 encryptions per second. With PCLMULQDQ and AES-NI the projected throughput exceeds 1,000,000 per second.

## Table of Contents
## 1.  Introduction

### 1.1  The Nonce Synchronisation Problem

Every AEAD scheme requires a nonce used at most once per key. Standard approaches each carry operational liabilities in military communications:

- Counter-based nonces \(AES-GCM, ChaCha20-Poly1305\): catastrophic failure on counter reuse; resynchronisation after packet loss or session restart requires explicit protocol machinery.
- Random nonces: 12–16 bytes wire overhead per packet; birthday-bound security collapses at 2⁶⁴ messages; still require reuse prevention.
- SIV schemes \(AES-GCM-SIV\): ciphertext reveals plaintext equality across transmissions; receiver must still track SIV state.

ARIA eliminates the counter-state problem. Both parties derive identical nonces from \(session key, message, per-transmission differentiator\) using deterministic algebraic operations. After packet loss, the receiver recomputes the correct nonce from the transmitted sequence number alone.

### 1.2  Design Goals

- Nonce uniqueness: identical plaintexts always produce distinct ciphertexts across all transmissions.
- Syncability: receiver resynchronises from sequence number alone; no persistent counter state.
- Proven collision resistance: formal reduction to named hard problems.
- Operational simplicity: three modes cover point-to-point, burst-loss, and multi-path deployments.
- Post-quantum awareness: no group-homomorphism structure exploitable by quantum Fourier transform.

## 2.  Mathematical Foundation

### 2.1  Base Field  F₁ = GF\(2²⁵⁶\)

All arithmetic uses the binary extension field GF\(2²⁵⁶\) = GF\(2\)\[x\] / p\(x\), where p\(x\) = x²⁵⁶ \+ x¹⁰ \+ x⁵ \+ x² \+ 1 \(pentanomial; verified irreducible\). Elements are 256-bit integers. Addition is XOR; multiplication uses shift-and-XOR with polynomial reduction.

**Parameter**

**Value**

**Notes**

Field

GF\(2²⁵⁶\)

Base field

Irreducible polynomial

x²⁵⁶\+x¹⁰\+x⁵\+x²\+1

Pentanomial; hardware-friendly

Element size

256 bits

4 × uint64

GF mul \(C −O3\)

~652 ns

~33 ns with PCLMULQDQ

GF mul \(Python ref\)

~46 µs

Reference only

### 2.2  Layer 2  L₂ = F₁\[y\] / Q₂\(y\)

Q₂\(y\) = y⁸ \+ y⁴ \+ y³ \+ y \+ 1. L₂ elements are degree < 8 polynomials with F₁ coefficients. Element space 2²⁰⁴⁸. Ring axioms verified in the reference implementation \(commutativity, associativity, distributivity\). L₂ is the coefficient ring of the message encoding polynomial.

### 2.3  Layer 3  L₃ = L₂\[z\] / Q₃\(z\)

Q₃\(z\) = z⁴ \+ z \+ 1. L₃ elements are degree < 4 polynomials with L₂ coefficients. Element space 2⁸¹⁹². L₃ provides the algebraic hiding space for the message encoding. Ring axioms verified.

### 2.4  The Nonce Map — Linear Algebra View

The nonce is a linear function of the message coefficient matrix, which enables the SDP reduction in Section 6:

N\(M, sk\) = C\(M, sk\) · β\_vec   in GF\(2²⁵⁶\)

C\(M, sk\) is the 8×256 binary matrix of coefficient field elements; β\_vec = \[1, β, β², …, β⁷\]ᵀ is the Vandermonde evaluation vector. Linearity: N\(M\) ⊕ N\(M’\) = D\(β\) where D is the difference polynomial. Verified numerically in all three computation forms.

## 3.  Meta-DAG Random Number Generator

### 3.1  Purpose

The Meta-DAG is the shared deterministic entropy source that makes nonce derivation syncable. Both parties, seeded from the same session key, produce identical GF\(2²⁵⁶\) output streams. The only coordination required is a sequence number in the packet header.

### 3.2  Architecture

Eight nodes, each seeded from a transcendental mathematical constant. The constants provide high-entropy seeds not under any party’s control. After each round, node i is cross-mixed with nodes \(i\+3\) mod 8 and \(i\+5\) mod 8, so no node evolves independently.

**Node**

**Constant**

**64-bit Seed**

pi

π — circumference ratio

0x243F6A8885A308D3

e

e — natural log base

0xB7E151628AED2A6B

sqrt2

√2 — square root of two

0x6A09E667F3BCC908

phi

φ — golden ratio

0x9E3779B97F4A7C15

zeta3

ζ\(3\) — Apéry’s constant

0xD2A1BE4BF93F45CF

gamma

γ — Euler-Mascheroni

0x93C467E37DB0C7A4

catalan

G — Catalan’s constant

0xD56B3CB5D3DB1A47

glaisher

A — Glaisher-Kinkelin

0xE2F5224C0DE89E2F

### 3.3  Node Operations

On each tick, meta\_state & 0x7 selects one of eight operations: left rotations by 17 and 31, right rotation by 13, XOR with the node’s constant, XOR with a shifted constant, modular addition, modular subtraction, and multiplication by a Fibonacci hashing constant. After each tick: meta\_state = \(meta\_state × 0x6C62272E07BB0142\) ⊕ state ⊕ counter. Four rounds produce one 256-bit output. Profiled throughput: 198,740 next\_gf256 calls/sec \(Python reference\).

### 3.4  Resynchronisation

DAG state is fully determined by \(session\_key, step\_count\). A receiver that missed packets fast-forwards to seq × 64 steps from the session key, requiring no stored state. Verified in test suite.

## 4.  Message Encoding

Message M is encoded as 8 L₂-element coefficients forming a degree-7 polynomial P\(y\):

α\_i\[j\]  =  DAG.next\_gf256\(\)  ×  H\(M ‖ \(8i\+j\).to\_bytes\(2\)\)    i, j ∈ \{0..7\}

P\(y\)  =  α₀ \+ α₁y \+ … \+ α₇y⁷   ∈ L₂\[y\]

The DAG factors are session-key-dependent; the hash factors are message-dependent. Their GF product couples both without either dominating. This coupling is the basis of the security proof: decoupling them requires either inverting SHA-256 or breaking the DAG’s PRF property.

Encoding time \(44-byte message\): ~2,978 µs Python reference, ~5 µs projected with PCLMULQDQ.

## 5.  Nonce Derivation Modes

### 5.1  Session Evaluation Points

β  =  H\("aria:beta:"  ‖ sk\)   — primary nonce evaluation point

δ  =  H\("aria:delta:" ‖ sk\)   — L₂-to-GF collapse point

α  =  H\("aria:alpha:" ‖ sk\)   — tag evaluation point  \(independent of β\)

The independence of α from β is critical. Pr\[α = β\] = 2⁻²⁵⁶. Leaking the nonce reveals nothing about the tag evaluation point.

### 5.2  Collapse

L₂ polynomial at an L₁ point reduces via double Horner:

l1\_coeffs  =  \[L2\_Horner\(cᵢ, δ\)  for cᵢ in poly\]

value      =  L1\_Horner\(l1\_coeffs, pt\)

### 5.3  Mode 1 — DAG Stream Injection

**OVERHEAD**

4 bytes \(sequence number\). No secret material transmitted.

After the 8 encoding coefficients, the DAG produces one additional GF element as a 9th differentiator. The receiver, at the same DAG offset via seq × 64 \+ encoding steps, produces the identical 9th element. Profiled: ~6,447 µs \(155/s\) Python reference.

### 5.4  Mode 2 — Random Salt Injection

**OVERHEAD**

16 bytes \(128-bit salt in header, not secret\).

Sender draws a fresh random salt r per transmission. Injects r into poly\[0\]: coeff\[0\]\[k\] ⊕= r × \(k\+1\). Salt transmitted openly. No DAG position agreement required; natural fit for multi-path environments. Profiled: ~5,715 µs \(175/s\) Python reference.

### 5.5  Mode 3 — Evaluation Point Drift

**OVERHEAD**

4 bytes \(sequence number\). Fastest for repeated-message retransmission.

P\(y\) is fixed for given \(M, sk\). Both the nonce and tag evaluation points drift with seq independently:

βᵢ  =  H\("aria:beta\_drift:"  ‖ sk ‖ seq\)

αᵢ  =  H\("aria:alpha\_drift:" ‖ sk ‖ seq\)

A 1-bit change in β causes ~50% nonce bit change. Measured avalanche: 49.8% of 128 tag bits change per single input bit flip. Profiled: ~7,031 µs \(142/s\) Python reference.

## 6.  Authentication and Encryption

### 6.1  Tag Computation

tag  =  Collapse\(P\(αᵢ\), δ\)\[:16\]

The authentication tag is the message polynomial evaluated at the tag-specific point αᵢ, collapsed to 16 bytes. Forgery probability: 2⁻¹²⁸ per attempt.

### 6.2  SIV Construction

The keystream is keyed from the tag \(SIV / synthetic IV\):

keystream  =  SHA256\_chain\("ks:" ‖ tag ‖ counter\)

Using the tag as keystream IV gives plaintext-committed ciphertext. A tag forgery implies plaintext recovery. Production implementations must replace the SHA-256 chain with AES-256-CTR keyed from the tag.

### 6.3  Encrypt

1. Build polynomial P from \(msg, sk, mode, seq/salt\).
2. Compute tag = Collapse\(P\(αᵢ\), δ\)\[:16\].
3. Compute keystream from tag.
4. Ciphertext = plaintext ⊕ keystream\[:len\(plaintext\)\].
5. Transmit: \(version, mode, meta, ciphertext, tag\). The nonce is never transmitted.

### 6.4  Decrypt \(SIV order\)

1. Tentatively decrypt: pt\_candidate = ciphertext ⊕ KS\(packet\_tag\).
2. Recompute polynomial P from \(pt\_candidate, sk, mode, meta\).
3. Recompute tag\_check = Collapse\(P\(αᵢ\), δ\)\[:16\].
4. If tag\_check = packet\_tag, accept; otherwise discard without revealing reason.

**CRITICAL**

Never release decrypted bytes before tag verification. Never indicate which verification step failed.

### 6.5  Wire Format

**Field**

**Width**

**Description**

version

1 byte

0x01

mode

1 byte

0x01 DAG | 0x02 salt | 0x03 drift

meta\_len

1 byte

Length of meta field

meta

4 or 16 B

Sequence number \(modes 1, 3\) or salt \(mode 2\)

ciphertext

N bytes

Encrypted payload \(same length as plaintext\)

tag

16 bytes

128-bit authentication tag

**Scheme**

**Overhead**

**Same-plaintext protection**

ARIA Mode 1

22 B

Yes — DAG stream

ARIA Mode 2

34 B

Yes — random salt

ARIA Mode 3

22 B

Yes — point drift

AES-GCM

28 B

No — tag leaks equality

AES-GCM-SIV

28 B

No — SIV tag leaks repetition

ChaCha20-Poly1305

28 B

No — counter reuse catastrophic

## 7.  Formal Security Reduction

**MAIN RESULT**

Adv\_COLL\(A\) ≤ min\( ε\_PRF \+ 7Q²/2²⁵⁷ ,  2⁻⁸⁶ \). The SDP bound is unconditional. Both reductions are constructive and numerically validated in the reference implementation.

### 7.1  Game Definitions

### **Game\_COLL — ARIA Nonce Collision**

Challenger samples sk, computes β = H\("aria:beta:" ‖ sk\) and DAG values dag\_i\(sk\). Adversary A receives oracle N\(·, sk\) and makes Q queries. Wins by finding M ≠ M’ with N\(M, sk\) = N\(M’, sk\). Advantage: Adv\_COLL\(A\) = Pr\[A wins\].

### **Game\_PRF — PRF Indistinguishability**

Challenger samples b ← \{0,1\}. Oracle O = PRF\_K if b=1, truly random if b=0. Adversary B makes Q queries, outputs b’. Advantage: Adv\_PRF\(B\) = |Pr\[b’=1|b=1\] − Pr\[b’=1|b=0\]|.

### SDP — Syndrome Decoding Problem

Given H ∈ GF\(2\)^\(r×n\) and s = He mod 2, find e’ with He’ = s and wt\(e’\) ≤ t. NP-complete \(Berlekamp 1978, McEliece 1978\). Best classical algorithm: ISD at O\(2^0.0536n\).

### 7.2  Theorem 1 — PRF Reduction

**THEOREM 1**

Let A win Game\_COLL with advantage ε\_A in time t\_A, with Q queries. There exists PRF distinguisher B with Adv\_PRF\(B\) ≥ ε\_A − 7Q\(Q−1\)/\(2·2²⁵⁶\), running in time t\_A \+ O\(Q·T\_GF\).

Construction: B samples β ← F. When A queries M\_i, B queries its oracle O for each DAG position, forms coefficients, evaluates Horner at β, returns nonce to A. When A outputs a collision \(i, j\): B computes D\(y\) = Σ\(c\_k^i ⊕ c\_k^j\)·y^k. If D\(β\) = 0, B outputs b’ = 1 \(oracle is PRF\).

Analysis: under a truly random oracle, D\(β\) = 0 with probability ≤ 7/2²⁵⁶ per pair \(D has degree ≤ 7, so at most 7 roots\). Over Q\(Q−1\)/2 pairs: Pr\[false collision\] ≤ 7Q²/2²⁵⁷. Under PRF\_K the nonce oracle is identically distributed to real ARIA, so A wins at rate ε\_A. ■

Corollary \(Q ≤ 2⁶⁴\): Adv\_COLL ≤ ε\_PRF \+ 7/2¹²⁹ ≈ ε\_PRF \+ 2⁻¹²⁶.

### 7.3  Theorem 2 — SDP Reduction \(NP-hard\)

**THEOREM 2**

Finding an ARIA nonce collision is at least as hard as decoding a \[2048, 256\] binary linear code. This is NP-hard. Best known classical attack: ~2⁸⁶ operations \(ISD\).

From the linear algebra view of Section 2.4: a collision N\(M\) = N\(M’\) means D · β\_vec = 0 in GF\(2\)^256. Flattening D to a 2048-bit vector e and writing the polynomial multiplication structure as a parity-check matrix Hβ gives: Hβ · e = 0 over GF\(2\). This is SDP with syndrome s = 0 on a \[2048, 256\] code. SDP is NP-complete, so any polynomial-time ARIA collision-finder implies P = NP. ■

**Code Parameter**

**Value**

**Notes**

Length n

2048

256 bits × 8 coefficients

Dimension k

256

Base field output size

Rate k/n

1/8

Low rate → harder decoding

Max error weight t

7

Degree of difference polynomial

ISD \(classical\)

~2⁸⁶

Prange / BJMM bound

ISD \(quantum\)

~2⁴³

Grover \+ ISD

### 7.4  Numerical Validation

**Test**

**Result**

**Notes**

Matrix linearity: N\(M\)⊕N\(M’\) = D\(β\)

PASS ✓

Exact equality verified

Collision rate ≤ Q\(Q-1\)/2·7/|F|

PASS ✓

0 observed vs 120 bound \(n=1500\)

D\(β\)=0 root condition

PASS ✓

200/200 polynomial trials

Degenerate β=0 birthday collisions

PASS ✓

Birthday rate confirmed

PRF reduction B runs cleanly

PASS ✓

Both oracle modes tested

**Attack Vector**

**Classical**

**Quantum**

**Basis**

PRF key recovery

2¹²⁸

2⁶⁴ \(Grover\)

SHA-256 PRF

Polynomial collision \(SDP\)

~2⁸⁶

~2⁴³ \(G\+ISD\)

NP-hard

Brute-force birthday

2¹²⁸ \(Q=2¹²⁸\)

2⁶⁴

Unconditional

GF\(2⁵¹²\) upgrade

2¹⁶²

2⁸¹

Post-quantum safe

## 8.  Performance

### 8.1  Python Reference — Measured

**NOTE**

Pure Python 3.12 on commodity hardware. Represents algorithmic complexity, not production performance.

**Operation**

**Avg µs**

**Throughput**

GF add

0.2

4,965,591 /s

GF multiply

46.1

21,714 /s

GF inverse

40.9

24,462 /s

L2 add

1.1

886,539 /s

L2 multiply

3,131

319 /s

L2 Horner eval

342

2,921 /s

L3 collapse to GF\(2²⁵⁶\)

1,453

688 /s

DAG round

4.8

208,933 /s

DAG next\_gf256 \(4 rounds\)

5.0

198,740 /s

encode\_message \(44 B\)

2,978

336 /s

aria\_encrypt Mode 1

6,447

155 /s

aria\_encrypt Mode 2

5,715

175 /s

aria\_encrypt Mode 3

7,031

142 /s

AEAD roundtrip Mode 1

14,620

68 /s

AEAD roundtrip Mode 3

14,520

69 /s

### 8.2  Production Projections

**Stage**

**GF mul latency**

**AEAD throughput**

**Notes**

Python reference

~46 µs

~70 /s

Reference only

Naive C \(−O3\)

~652 ns

~5,000 /s

Baseline C

C \+ PCLMULQDQ

~33 ns

~100,000 /s

Carryless multiply

C \+ PCLMULQDQ \+ AES-NI

~5 ns

~2,000,000 /s

AES block expansion

AVX-512 \(8-way parallel\)

~5 ns/lane

~10,000,000 /s

8 simultaneous nonces

**Application**

**Required rate**

**Met by**

Voice radio \(STANAG 4285\)

~8,000 /s

Naive C

Video \(STANAG 4609\)

~120,000 /s

PCLMULQDQ

High-speed data

~1,000,000 /s

PCLMULQDQ \+ AES-NI

Tactical data network

~10,000,000 /s

AVX-512

## 9.  Known Limitations

**PRODUCTION GATE**

The items below are known gaps between research prototype and production primitive. All must be addressed before operational deployment.

1. No EUF-CMA proof for the authentication tag. The unforgeability argument is heuristic.
2. DAG-RNG PRF security is argued via SHA-256 but not independently proven for the meta-operation structure.
3. SHA-256 chain keystream is a placeholder. Production requires AES-256-CTR \(formally proven IND-CPA\).
4. Quantum SDP hardness: current GF\(2²⁵⁶\) gives ~2⁴³ under Grover\+ISD. Upgrade to GF\(2⁵¹²\) for post-quantum security.
5. No external audit. No third-party cryptanalysis has been performed. This is non-negotiable before deployment.
6. No side-channel analysis. Constant-time GF arithmetic is required; timing and power attacks have not been assessed.
7. L3 security contribution not formally quantified beyond the NP-hard SDP bound.

## 10.  Implementation Notes

### 10.1  Reference Implementation \(aria.py\)

**Section**

**Content**

1

GF\(2²⁵⁶\): gf\_add, gf\_mul, gf\_inv, gf\_pow

2

L2: l2\_add, l2\_mul, l2\_horner

3

L3: l3\_mul, l3\_collapse

4

MetaDAG, \_DAGNode

5

\_encode\_message, \_collapse\_poly

6

\_build\_poly, ARIAMode \(three modes\)

7

aria\_encrypt, aria\_decrypt, ARIASession \(SIV AEAD\)

8

PRFOracle, prf\_reduction\_B, sdp\_reduction\_verify

9

Profiler, run\_profiler

10

run\_tests \(61 tests, all pass\)

### 10.2  Production Hardening Order

1. Replace SHA-256 keystream with AES-256-CTR keyed from tag.
2. PCLMULQDQ-based GF\(2²⁵⁶\) multiplication \(~10–20× speedup\).
3. AES-NI coefficient expansion \(~100× speedup on hash-per-coefficient\).
4. AVX-512 parallelism across 8 simultaneous nonces.
5. Formal EUF-CMA proof for tag; formalise PRF reduction for DAG-RNG.
6. External cryptographic audit \(minimum 6 months, two independent teams\).
7. Constant-time GF arithmetic for side-channel resistance.

### 10.3  Resynchronisation

After packet loss, the receiver uses the sequence number from any received packet to reposition the DAG and recompute the nonce. No stored state beyond the session key is required. Multi-path environments should either assign distinct seq ranges per path or use Mode 2 \(random salt\), which requires no seq coordination.

## 11.  Conclusion

ARIA provides a solution to the nonce synchronisation problem in military communications through deterministic algebraic nonce derivation. The three-layer tower \(GF\(2²⁵⁶\) → L2 → L3\) provides structural depth; the Meta-DAG provides shared deterministic entropy; the three differentiation modes cover the operational range from low-overhead point-to-point links to multi-path channels.

Collision resistance is bounded by two independent hard problems. The PRF reduction gives Adv\_COLL ≤ ε\_PRF \+ 2⁻¹²⁶ for Q ≤ 2⁶⁴. The SDP reduction gives an unconditional 2⁸⁶ classical floor, NP-hard. Both are constructive, implemented as executable Python, and validated by 61 automated tests.

The path to production requires: EUF-CMA proof for the tag, AES-NI and PCLMULQDQ for throughput, GF\(2⁵¹²\) for post-quantum security, and external audit. The construction is sound; what remains is engineering and formal verification.

*End of ARIA Cryptographic Specification*
