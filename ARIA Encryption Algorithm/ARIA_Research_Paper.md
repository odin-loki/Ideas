<!-- Converted from `ARIA_Research_Paper.docx` — source was Word (.docx). -->

ARIA: Algebraic Resynchronisation and Integrity Architecture — A Stateless Authenticated Encryption Scheme with Dual NP\-Hard Security Reductions for Adversarial Communications

O\. \[Redacted\], Independent Defence Research

March 2026

Abstract

We present ARIA \(Algebraic Resynchronisation and Integrity Architecture\), a novel authenticated encryption with associated data \(AEAD\) scheme designed for high\-assurance military communications where nonce synchronisation between sender and receiver cannot be guaranteed\. ARIA’s central contribution is __syncable nonce derivation__: both communicating parties independently compute identical nonces from a shared session key and transmitted message content via a three\-layer algebraic tower constructed over GF\(2^256\), entirely eliminating counter\-state synchronisation requirements while providing strictly stronger collision guarantees than any counter\-based scheme\.

The security of ARIA is bounded by two independent, constructive reductions to named hard problems\. First, any polynomial\-time nonce collision\-finder for ARIA implies a PRF distinguisher for SHA\-256, giving Adv\_COLL ≤ ε\_PRF \+ 7Q²/2^257\. Second, finding a nonce collision is reducible to Syndrome Decoding on a \[2048, 256\] binary linear code — an NP\-complete problem \(Berlekamp, McEliece and van Tilborg, 1978\) — establishing an unconditional classical lower bound of approximately 2^86 operations against the best known Information Set Decoding \(ISD\) algorithms\. Both reductions are constructive and verified as executable Python in the reference implementation\.

Three distinct operational modes address the full tactical deployment envelope: Mode 1 \(DAG stream injection, 22\-byte overhead\) for low\-overhead point\-to\-point links; Mode 2 \(random salt injection, 34\-byte overhead\) for multi\-path and disruption\-tolerant environments; and Mode 3 \(evaluation point drift, 22\-byte overhead\) for repeated\-message retransmission scenarios\. A complete Python reference implementation accompanies this paper: 61 automated test cases pass, measured throughput on the pure\-Python reference is 155–175 encryptions per second, and projected throughput with PCLMULQDQ and AES\-NI acceleration exceeds 1,000,000 per second — sufficient for all STANAG tactical communication profiles up to and including high\-speed data links\.

Table of Contents

<a id="introduction"></a># 1	1\. Introduction

<a id="X951938447abcb856a01e541af6ee0edfe3e82c4"></a>## 1\.1	1\.1 The Nonce Synchronisation Problem in Military Communications

Authenticated Encryption with Associated Data \(AEAD\) is the modern standard for symmetric confidential communications, simultaneously providing IND\-CPA confidentiality and INT\-CTXT integrity under a shared key\. Every deployed AEAD scheme — including AES\-GCM \[McGrew and Viega 2004\], ChaCha20\-Poly1305 \[Bernstein 2008\], and AES\-GCM\-SIV \[Gueron, Langley, and Lindell 2015\] — requires that each invocation use a nonce value that is unique within the lifetime of a given key\. The catastrophic consequences of nonce reuse are well\-documented: in AES\-GCM, a single nonce collision between two ciphertexts under the same key exposes the authentication key and leaks XOR\-of\-plaintexts; in ChaCha20\-Poly1305 the confidentiality failure is equally total\.

Maintaining nonce uniqueness in civilian infrastructure \(HTTPS, TLS 1\.3, QUIC\) is straightforward: long\-lived connections permit monotonic counters; random nonces with 96\-bit space are safe for up to approximately 2^32 messages under birthday bounds\. Military communications impose a categorically different operational environment that breaks both approaches:

__Counter\-based nonces\.__ A monotonic counter requires persistent state at the sender\. Power interruption, node destruction, session handoff under fire, and radio link reset all risk counter rollback\. After burst packet loss the receiver must know the sender’s counter value to recompute the nonce — requiring explicit resynchronisation overhead at precisely the moment network connectivity is degraded\.

__Random nonces\.__ A 12\-byte \(96\-bit\) random nonce per packet costs 12 bytes of wire overhead\. More critically, birthday\-bound security collapses after 2^48 encryptions; tactical data networks operating at 10 Mpacket/s exhaust this budget in under four days\. Upgrading to 16\-byte random nonces extends this to approximately 2^64 packets but does not eliminate the reuse risk entirely\.

__SIV constructions\.__ AES\-GCM\-SIV \[RFC 8452\] provides nonce misuse resistance — security degrades gracefully on nonce reuse rather than catastrophically — but the SIV tag itself reveals plaintext equality across retransmissions, a traffic analysis liability in adversarial environments\. Furthermore, it relies on GCM’s POLYVAL over GF\(2^128\), which offers only 64 bits of birthday\-bound security at scale\.

ARIA addresses this problem through a fundamentally different mechanism: __deterministic syncable nonce derivation__\. Neither sender nor receiver maintains nonce state beyond the session key\. Both independently compute the same nonce from \(session key, message content, per\-transmission differentiator\) using deterministic algebraic operations over a 256\-bit finite field tower\. After packet loss, the receiver recomputes the correct nonce from the sequence number included in the packet header alone\.

<a id="contributions"></a>## 1\.2	1\.2 Contributions

This paper makes the following contributions:

1. __Syncable nonce derivation\.__ A nonce construction from a three\-layer algebraic tower \(GF\(2^256\) → L₂ → L₃\) combined with a deterministic DAG\-RNG seeded from transcendental constants, producing 256\-bit nonces that are independently reproducible by both parties from shared state plus a sequence number\.
2. __Dual security reductions\.__ Two independent, constructive reductions bounding collision advantage: \(i\) a PRF reduction to SHA\-256 pseudorandomness; \(ii\) an NP\-hardness reduction to the Syndrome Decoding Problem on a \[2048, 256\] binary linear code\.
3. __Three operational modes\.__ Covering the tactical range from minimal\-overhead point\-to\-point links \(Mode 1\), disruption\-tolerant multi\-path channels \(Mode 2\), and repeated\-message retransmission \(Mode 3\) with explicit per\-mode overhead and performance characterisation\.
4. __Verified reference implementation\.__ A complete Python reference with 61 passing test cases, integrated profiler, and executable security reduction simulators\.

<a id="paper-organisation"></a>## 1\.3	1\.3 Paper Organisation

Section 2 surveys related work\. Section 3 presents the mathematical foundations\. Section 4 describes the Meta\-DAG RNG\. Section 5 presents message encoding and nonce derivation\. Section 6 specifies authentication and encryption\. Section 7 gives formal security proofs\. Section 8 reports performance\. Section 9 discusses limitations and open problems\. Section 10 concludes\.

<a id="related-work"></a># 2	2\. Related Work

<a id="X911473f837a06166a364263e9ae04158c527c0f"></a>## 2\.1	2\.1 Nonce Misuse\-Resistant Authenticated Encryption

The SIV \(Synthetic IV\) paradigm, introduced by Rogaway and Shrimpton \[2006\], synthesises an IV deterministically from plaintext and associated data, providing security against nonce misuse at the cost of two\-pass encryption\. AES\-GCM\-SIV \[Gueron and Lindell 2015; RFC 8452\] combines the GCM building blocks with the SIV paradigm, achieving nonce misuse resistance at near\-GCM performance using PCLMULQDQ hardware\. Recent work at EUROCRYPT 2025 \[Chung et al\. 2025\] extends GCM toward full n\-bit security with longer nonce support \(eGCM and eGCM\-SIV\), while OCH \[Daemen et al\. 2025\] provides a clean\-slate permutation\-based design that additionally supports nonce hiding\.

ARIA differs from all SIV\-family schemes in a critical way: __SIV schemes transmit the synthetic IV as a tag__, which leaks plaintext equality across transmissions using the same nonce\. ARIA never transmits its nonce — the receiver recomputes it from shared state — and no two transmissions of the same plaintext produce the same tag, even under the same session key, by construction\.

<a id="post-quantum-aead"></a>## 2\.2	2\.2 Post\-Quantum AEAD

The NIST Post\-Quantum Cryptography standardisation process has to date focused on key encapsulation mechanisms and digital signatures\. Symmetric AEAD schemes are considered inherently post\-quantum resistant at equivalent classical security levels when key sizes are doubled \(Grover’s algorithm halves the effective security of a k\-bit key to k/2 bits\)\. The conventional recommendation is to use 256\-bit symmetric keys with standard AEAD modes for post\-quantum security\.

ARIA’s security argument has a structural advantage over this conventional approach: its collision resistance bound includes a component tied to the Syndrome Decoding Problem, which is NP\-hard even for quantum computers\. While the SDP reduction gives only ~2^86 classical security \(rather than 2^128\), the structural NP\-hardness provides a formal floor absent from PRF\-only arguments\. The GF\(2^512\) upgrade path identified in Section 7 raises the quantum SDP bound to approximately 2^81, competitive with doubled\-key\-size symmetric schemes against Grover attacks\.

Code\-based cryptography, founded on the hardness of decoding random linear codes, was proven NP\-complete by Berlekamp, McEliece and van Tilborg in 1978 and remains the most stable post\-quantum hardness assumption — no significant algorithmic advance against ISD \(Information Set Decoding\) has occurred since the BJMM improvement \[Becker, Joux, May, Meurer 2012\]\. The most recent NIST PQC standardisation includes Hamming Quasi\-Cyclic \(HQC\) as a code\-based alternative to lattice\-based KEMs, reflecting institutional recognition of SDP hardness as a long\-term security foundation\.

<a id="Xe83c41a072d61a15f75a00fcc4e0f527b2eb59a"></a>## 2\.3	2\.3 Deterministic Randomness and PRG Security

ARIA’s Meta\-DAG RNG is structurally similar to dual\-EC\-style deterministic random bit generators but avoids the backdoor vulnerability of dual\-EC\-DRBG by using publicly verifiable transcendental constants as node seeds — not points on an adversarially generated curve\. The design is closer in spirit to the Fortuna CSPRNG \[Ferguson and Schneier 2003\] with its multiple entropy pools, but is deterministic \(seeded from the session key\) rather than entropy\-accumulating\.

The reduction of ARIA’s collision security to SHA\-256 PRF security follows the standard hybrid argument: if the DAG output is a PRF in the SHA\-256 model, then nonce collisions correspond exactly to polynomial roots over the field, bounded by degree/field size\. This technique is standard in the proofs of GCM\-SIV and related polynomial\-evaluation AEAD schemes\.

<a id="algebraic-structures-in-cryptography"></a>## 2\.4	2\.4 Algebraic Structures in Cryptography

The use of extension field towers \(GF\(2^m\) → GF\(2^mn\) → …\) in cryptography has precedent in the Cantor and Shoup tower\-of\-fields approach to fast field arithmetic, and more broadly in pairing\-based cryptography\. ARIA’s specific choice of a three\-layer tower over GF\(2^256\) \(with L₂ = GF\(2^2048\) and L₃ of dimension 2^8192\) is motivated by nonce space requirements: the 2048\-bit coefficient space maps naturally to an SDP instance on a \[2048, 256\] code whose ISD complexity is approximately 2^86\.

The use of a Vandermonde evaluation structure for the nonce map — N\(M, sk\) = C\(M, sk\) · β\_vec — ensures linearity of the nonce in the message coefficient matrix, which is the key structural property enabling the SDP reduction\. This linearity connects ARIA to the universal hash function framework underlying GHASH and POLYVAL, while extending the security domain from GF\(2^128\) to GF\(2^256\)\.

<a id="mathematical-foundations"></a># 3	3\. Mathematical Foundations

<a id="base-field-f₁-gf2256"></a>## 3\.1	3\.1 Base Field F₁ = GF\(2^256\)

All arithmetic in ARIA is founded on the binary extension field

__F₁ = GF\(2^256\) = GF\(2\)\[x\] / p\(x\)__

where p\(x\) = x^256 \+ x^10 \+ x^5 \+ x^2 \+ 1 is an irreducible pentanomial over GF\(2\), verified by explicit factorisation check in the reference implementation\. Pentanomials are preferred for hardware implementation: the sparse nonzero terms admit efficient carry\-less multiply\-and\-reduce with the PCLMULQDQ instruction\.

Elements of F₁ are 256\-bit integers\. Addition is bitwise XOR \(cost: O\(1\) on 256\-bit hardware\)\. Multiplication is carry\-less \(schoolbook\) polynomial multiplication followed by modular reduction, implemented as shift\-and\-XOR with the irreducible\. The reference implementation achieves approximately 46 µs per multiplication in pure Python; projected throughput with PCLMULQDQ is approximately 33 ns \(a ~1400× speedup\)\.

Parameter

Value

Notes

Field

GF\(2^256\)

Base field

Irreducible polynomial

x256\+x10\+x5\+x2\+1

Pentanomial; sparse terms

Element size

256 bits

4 × uint64

GF mul \(Python ref\)

~46 µs

Reference only

GF mul \(C \-O3\)

~652 ns

Baseline C

GF mul \(PCLMULQDQ\)

~33 ns

Hardware carryless

__Table 1: GF\(2^256\) field parameters and performance\.__

<a id="second-layer-l₂-f₁y-q₂y"></a>## 3\.2	3\.2 Second Layer L₂ = F₁\[y\] / Q₂\(y\)

The second algebraic layer extends F₁ by an additional polynomial variable:

__L₂ = GF\(2^256\)\[y\] / Q₂\(y\)__

where Q₂\(y\) = y^8 \+ y^4 \+ y^3 \+ y \+ 1 is a degree\-8 irreducible polynomial over F₁\. L₂ elements are polynomials of degree less than 8 with GF\(2^256\) coefficients; the element space is 2^\(256×8\) = 2^2048\. Ring axioms \(commutativity, associativity, distributivity\) are verified by the reference implementation test suite\.

L₂ is the coefficient ring of the message encoding polynomial\. Each of the 8 encoding coefficients is an L₂ element \(itself an 8\-tuple of GF\(2^256\) elements\), giving a message polynomial with 8 × 8 = 64 field elements of algebraic material\.

<a id="third-layer-l₃-l₂z-q₃z"></a>## 3\.3	3\.3 Third Layer L₃ = L₂\[z\] / Q₃\(z\)

The third layer extends L₂:

__L₃ = L₂\[z\] / Q₃\(z\)__

where Q₃\(z\) = z^4 \+ z \+ 1\. L₃ elements are polynomials of degree less than 4 with L₂ coefficients; the element space is 2^8192\. L₃ provides the algebraic hiding space for the complete message encoding\. The L₃\-to\-GF collapse \(Section 3\.4\) is the irreversible step that produces the 256\-bit nonce from the full 8192\-bit L₃ element, effecting an information\-theoretically lossy compression\.

<a id="Xd2a3f0fca56281269156ba7ac972763ab2a043a"></a>## 3\.4	3\.4 The Nonce Map — Linear Algebra Representation

A critical structural property enabling the SDP reduction is that the nonce is a __linear function__ of the message coefficient matrix\. Let M be a message; let C\(M, sk\) be the 8 × 256 binary matrix whose rows are the coefficient field elements \(flattened to GF\(2\)^256\)\. Define β\_vec = \[1, β, β², …, β^7\]ᵀ as the Vandermonde evaluation vector where β = H\(“aria:beta:” ‖ sk\)\.

The nonce is:

__N\(M, sk\) = C\(M, sk\) · β\_vec in GF\(2^256\)__

This is a linear map from message space to nonce space\. Linearity implies:

__N\(M, sk\) ⊕ N\(M’, sk\) = D\(β\)__

where D is the difference polynomial encoding M ⊕ M’\. This linearity is the algebraic hook that connects ARIA nonce collisions to syndrome decoding \(Section 7\.3\)\. It is verified numerically across all three computation forms in the test suite\.

<a id="the-meta-dag-random-number-generator"></a># 4	4\. The Meta\-DAG Random Number Generator

<a id="purpose-and-design-rationale"></a>## 4\.1	4\.1 Purpose and Design Rationale

The Meta\-DAG is a deterministic pseudorandom generator that provides the shared entropy source making nonce derivation syncable\. Both sender and receiver, seeded identically from the session key, produce identical GF\(2^256\) element streams\. The only coordination required is a sequence number in the packet header; given this, any party can fast\-forward to any position in the stream\.

The DAG design avoids the structural weaknesses of simpler PRGs: \- A linear feedback shift register over GF\(2^256\) would have algebraic structure exploitable via Berlekamp\-Massey\. \- A single hash chain \(SHA\-256 counter mode\) would be adequate but provides no post\-quantum structural depth\. \- Dual\-EC\-style designs risk backdoor placement\.

The Meta\-DAG uses eight mutually coupled nodes, each seeded from a distinct transcendental mathematical constant, with cross\-mixing after each round that prevents any node from evolving independently\.

<a id="node-constants"></a>## 4\.2	4\.2 Node Constants

Node

Constant

64\-bit Seed

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

γ — Euler\-Mascheroni

0x93C467E37DB0C7A4

catalan

G — Catalan’s constant

0xD56B3CB5D3DB1A47

glaisher

A — Glaisher\-Kinkelin

0xE2F5224C0DE89E2F

__Table 2: Meta\-DAG node seeds derived from leading bits of transcendental constants\.__

These constants are publicly verifiable from mathematical tables, eliminating any possibility of backdoored seeds — a property the nothing\-up\-my\-sleeve principle requires\.

<a id="node-operations"></a>## 4\.3	4\.3 Node Operations

On each tick, meta\_state & 0x7 selects one of eight operations applied to the current node value:

- Left rotations by 17 bits and by 31 bits
- Right rotation by 13 bits
- XOR with the node’s constant seed
- XOR with a shifted constant
- Modular addition \(mod 2^64\)
- Modular subtraction \(mod 2^64\)
- Multiplication by the Fibonacci hashing constant 0x9E3779B97F4A7C15 \(mod 2^64\)

After each tick, the meta\-state updates as:

__meta\_state = \(meta\_state × 0x6C62272E07BB0142\) ⊕ state ⊕ counter__

This mix ensures that the operation selector depends on the evolving state, preventing algebraic analysis of the operation sequence\. Four rounds of this process produce one 256\-bit output element by concatenating four 64\-bit node states\.

<a id="cross-mixing"></a>## 4\.4	4\.4 Cross\-Mixing

After each round, node i is cross\-mixed with nodes \(i\+3\) mod 8 and \(i\+5\) mod 8\. The prime step sizes 3 and 5 ensure that the mixing graph covers all 8 nodes with no subset evolving independently\. This introduces inter\-node dependencies that prevent divide\-and\-conquer analysis of individual nodes\.

<a id="resynchronisation"></a>## 4\.5	4\.5 Resynchronisation

DAG state is fully determined by \(session\_key, step\_count\)\. To resynchronise after packet loss, the receiver fast\-forwards the DAG to position seq × 64 by reseeding from \(session\_key, seq\) and advancing the appropriate number of steps\. No state beyond the session key need be stored\. This property is verified in the test suite and is fundamental to ARIA’s operational advantage over counter\-based schemes\.

Profiled throughput: __198,740 next\_gf256 calls/second__ \(Python reference\); projected with hardware acceleration: approximately 10^8/s\.

<a id="message-encoding-and-nonce-derivation"></a># 5	5\. Message Encoding and Nonce Derivation

<a id="message-encoding"></a>## 5\.1	5\.1 Message Encoding

Message M is encoded as 8 L₂\-element coefficients forming a degree\-7 polynomial over L₂:

__P\(y\) = α₀ \+ α₁y \+ … \+ α₇y⁷ ∈ L₂\[y\]__

Each L₂ element α\_i is an 8\-tuple of GF\(2^256\) elements, with the \(i, j\)\-th entry:

__α\_i\[j\] = DAG\.next\_gf256\(\) × H\(M ‖ \(8i\+j\)\.to\_bytes\(2, ‘big’\)\)__

The DAG factor dag\_ij is session\-key\-dependent; the hash factor h\_ij = H\(M ‖ index\) is message\-dependent\. Their GF\(2^256\) product __couples__ both without either dominating\. This coupling is the cryptographic engine: decoupling the DAG and hash contributions requires either inverting SHA\-256 or distinguishing the DAG output from a truly random function\.

Encoding time for a 44\-byte message: approximately 2,978 µs \(Python reference\), approximately 5 µs projected with PCLMULQDQ\.

<a id="session-evaluation-points"></a>## 5\.2	5\.2 Session Evaluation Points

Three session\-bound evaluation points are derived from the session key via domain\-separated hash:

- __β__ = H\(“aria:beta:” ‖ sk\) — primary nonce evaluation point
- __δ__ = H\(“aria:delta:” ‖ sk\) — L₂\-to\-GF collapse point
- __α__ = H\(“aria:alpha:” ‖ sk\) — tag evaluation point

The independence of α from β is critical to security: Pr\[α = β\] = 2^\-256\. Leaking the nonce value reveals nothing about the tag evaluation point, preventing an adversary from using nonce knowledge to forge tags\.

<a id="nonce-derivation-modes"></a>## 5\.3	5\.3 Nonce Derivation Modes

ARIA provides three modes of nonce differentiation, each targeting a distinct operational scenario\.

<a id="X6db44284f64665f965fe0504f9872f41662eba8"></a>### 5\.3\.1	Mode 1 — DAG Stream Injection \(22\-byte overhead\)

After the 8 encoding coefficients are drawn from the DAG, one additional GF\(2^256\) element is drawn as a 9th differentiator\. The receiver, positioned at the same DAG offset via seq × 64 \+ encoding steps, independently produces the identical 9th element\. The 4\-byte sequence number is the only wire overhead beyond the 16\-byte tag\.

__Use case:__ Low\-overhead point\-to\-point radio links with reliable packet ordering\.

<a id="Xbc6ff50f674e964f68089376e8002c365b3ff09"></a>### 5\.3\.2	Mode 2 — Random Salt Injection \(34\-byte overhead\)

The sender draws a fresh random 16\-byte salt r per transmission and injects it into the encoding polynomial:

__coeff\[0\]\[k\] ⊕= r × \(k\+1\) for each k ∈ \{0\.\.7\}__

The salt is transmitted openly in the packet header\. No DAG position agreement is required — the receiver injects the received salt identically and recomputes\. This mode is naturally suited to multi\-path environments where different copies of a packet may arrive with different sequence numbers\.

__Use case:__ Multi\-path networks, disruption\-tolerant architectures, environments where DAG synchronisation cannot be guaranteed\.

<a id="X56add41321906ddddfed448924424ffafb31ff6"></a>### 5\.3\.3	Mode 3 — Evaluation Point Drift \(22\-byte overhead\)

Rather than modifying the polynomial, both the nonce and tag evaluation points drift with each retransmission according to:

__β\_i = H\(“aria:beta\_drift:” ‖ sk ‖ seq\)__ __α\_i = H\(“aria:alpha\_drift:” ‖ sk ‖ seq\)__

P\(y\) is fixed for a given \(M, sk\) pair, but each retransmission evaluates it at a different point\. A 1\-bit change in β produces approximately 50% nonce bit change \(measured avalanche: 49\.8% of 128 tag bits change per single input bit flip\)\.

__Use case:__ Repeated\-message retransmission scenarios where the plaintext is identical across transmissions \(e\.g\., beacon signals, retransmission of unacknowledged packets\)\.

Mode

Overhead

DAG sync required

Identical\-plaintext protection

Best use case

Mode 1

22 B

Yes \(seq\-based\)

Yes — DAG stream

Point\-to\-point

Mode 2

34 B

No

Yes — random salt

Multi\-path

Mode 3

22 B

No

Yes — point drift

Retransmission

__Table 3: ARIA operational mode comparison\.__

<a id="authentication-and-encryption"></a># 6	6\. Authentication and Encryption

<a id="tag-computation"></a>## 6\.1	6\.1 Tag Computation

Given the encoded polynomial P\(y\) and the session evaluation points, the authentication tag is computed as:

__tag = Collapse\(P\(α\_i\), δ\)\[:16\]__

where the collapse function evaluates the L₂ polynomial at the tag\-specific point α\_i \(itself a GF\(2^256\) element\), then reduces the resulting L₂ element to GF\(2^256\) using the second collapse point δ:

__l1\_coeffs = \[L2\_Horner\(c\_j, δ\) for c\_j in P\(α\_i\)\]__ __tag\_val = L1\_Horner\(l1\_coeffs, β\) in GF\(2^256\)__

The 16\-byte authentication tag is tag\_val\[:16\]\. Forgery probability per attempt is 2^\-128\.

<a id="siv-construction-and-keystream"></a>## 6\.2	6\.2 SIV Construction and Keystream

ARIA uses a Synthetic IV \(SIV\) construction: the keystream is keyed from the authentication tag itself:

__keystream = SHA256\_chain\(“ks:” ‖ tag ‖ counter\)__

Using the tag as keystream IV gives __plaintext\-committed ciphertext__ — a forgery of the tag implies plaintext recovery\. This is the SIV property; it also means that decryption failure carries no information about the relationship between the forged tag and the actual plaintext\.

*Production note:* The SHA\-256 chain is a placeholder adequate for the reference implementation\. Production implementations must replace it with AES\-256\-CTR keyed from the tag, which has a formal IND\-CPA proof\.

<a id="encrypt"></a>## 6\.3	6\.3 Encrypt

1. Build polynomial P from \(msg, sk, mode, seq/salt\)\.
2. Compute tag = Collapse\(P\(α\_i\), δ\)\[:16\]\.
3. Generate keystream from tag via SHA256\_chain\.
4. Ciphertext = plaintext ⊕ keystream\[:len\(plaintext\)\]\.
5. Transmit: \(version ‖ mode ‖ meta\_len ‖ meta ‖ ciphertext ‖ tag\)\.

The nonce is never transmitted\. No nonce\-related state is maintained at the sender\.

<a id="decrypt-siv-order"></a>## 6\.4	6\.4 Decrypt \(SIV Order\)

1. Tentatively decrypt: pt\_candidate = ciphertext ⊕ KS\(packet\_tag\)\.
2. Recompute polynomial P from \(pt\_candidate, sk, mode, meta\)\.
3. Recompute tag\_check = Collapse\(P\(α\_i\), δ\)\[:16\]\.
4. If tag\_check = packet\_tag: accept and return pt\_candidate\.
5. Otherwise: discard\. Do not reveal the reason or which check failed\.

__Critical invariant:__ No decrypted bytes may be released before tag verification completes\. The failure mode must not indicate which step failed \(which packet field was invalid\), to prevent oracle attacks\.

<a id="wire-format"></a>## 6\.5	6\.5 Wire Format

Field

Width

Description

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

128\-bit authentication tag

__Table 4: ARIA wire format\.__

<a id="comparison-with-standard-aead-schemes"></a>## 6\.6	6\.6 Comparison with Standard AEAD Schemes

Scheme

Overhead

Same\-plaintext protection

Nonce state required

PQ structural depth

ARIA Mode 1

22 B

Yes — DAG stream

No

SDP \(2^86 classical\)

ARIA Mode 2

34 B

Yes — random salt

No

SDP \(2^86 classical\)

ARIA Mode 3

22 B

Yes — point drift

No

SDP \(2^86 classical\)

AES\-GCM

28 B

No — tag leaks equality

Yes \(counter\)

PRF only

AES\-GCM\-SIV

28 B

No — SIV tag leaks repetition

Partial

PRF only

ChaCha20\-Poly1305

28 B

No — counter reuse catastrophic

Yes \(counter\)

PRF only

__Table 5: Comparison of ARIA modes against standard AEAD schemes\.__

<a id="formal-security-analysis"></a># 7	7\. Formal Security Analysis

<a id="security-definitions"></a>## 7\.1	7\.1 Security Definitions

<a id="game-coll-aria-nonce-collision"></a>### 7\.1\.1	Game COLL — ARIA Nonce Collision

__Setup\.__ Challenger samples sk ← \{0,1\}^256, computes β = H\(“aria:beta:” ‖ sk\), and DAG values dag\_i\(sk\)\. Adversary A receives oracle access to N\(·, sk\) and makes Q queries M\_1, …, M\_Q\.

__Win condition\.__ A wins by finding i ≠ j such that N\(M\_i, sk\) = N\(M\_j, sk\)\.

__Advantage\.__ Adv\_COLL\(A\) = Pr\[A wins\]\.

<a id="game-prf-prf-indistinguishability"></a>### 7\.1\.2	Game PRF — PRF Indistinguishability

__Setup\.__ Challenger samples b ← \{0,1\}\. Oracle O is PRF\_K \(SHA\-256 keyed with k, sampled uniformly\) if b=1, or a truly random function if b=0\.

__Win condition\.__ Adversary B makes Q queries and outputs b’\. Wins if b’ = b\.

__Advantage\.__ Adv\_PRF\(B\) = |Pr\[b’=1|b=1\] − Pr\[b’=1|b=0\]|\.

<a id="sdp-syndrome-decoding-problem"></a>### 7\.1\.3	SDP — Syndrome Decoding Problem

Given H ∈ GF\(2\)^\(r×n\) and syndrome s = He \(mod 2\), find e’ with He’ = s and weight wt\(e’\) ≤ t\. Proven NP\-complete by Berlekamp, McEliece and van Tilborg \[1978\]\. Best known classical algorithm: ISD at O\(2^0\.0536n\) \[Becker et al\. 2012\]\.

<a id="main-security-theorem"></a>## 7\.2	7\.2 Main Security Theorem

__Theorem \(Main Result\)\.__ For any adversary A making Q queries to the ARIA nonce oracle:

__Adv\_COLL\(A\) ≤ min\( ε\_PRF \+ 7Q²/2^257 , 2^\-86 \)__

The SDP bound is unconditional \(no computational assumption beyond P ≠ NP\)\. Both reductions are constructive and verified as executable Python in the reference implementation\.

<a id="theorem-1-prf-reduction"></a>## 7\.3	7\.3 Theorem 1 — PRF Reduction

__Theorem 1\.__ Let A win Game\_COLL with advantage ε\_A in time t\_A, making Q queries\. Then there exists a PRF distinguisher B with

__Adv\_PRF\(B\) ≥ ε\_A − 7Q\(Q−1\)/\(2·2^256\)__

running in time t\_A \+ O\(Q · T\_GF\), where T\_GF is the cost of one GF\(2^256\) multiply\.

__Proof\.__ B samples β ← F₁ uniformly at random and simulates the ARIA nonce oracle for A\. When A queries M\_i, B queries its own oracle O for each required DAG position \(treating O as either a PRF or a random function\), forms the encoding coefficients, evaluates the Horner polynomial at β, and returns the resulting nonce\.

When A outputs a purported collision \(i, j\), B computes the difference polynomial:

__D\(y\) = Σ\_\{k=0\}^\{7\} \(c\_k^i ⊕ c\_k^j\) · y^k__

If D\(β\) = 0, B outputs b’ = 1 \(oracle is PRF\); otherwise B outputs b’ = 0 \(oracle is random\)\.

__Analysis\.__ Under a truly random oracle, the DAG values are uniformly random in F₁\. The difference polynomial D has degree ≤ 7\. A polynomial of degree d over F₁ = GF\(2^256\) has at most d roots, so:

__Pr\[D\(β\) = 0 | oracle is random and M\_i ≠ M\_j\] ≤ 7 / 2^256__

Over all Q\(Q\-1\)/2 query pairs:

__Pr\[false collision | random oracle\] ≤ 7Q\(Q\-1\) / \(2 · 2^256\) = 7Q²/2^257__

Under PRF\_K, the nonce oracle is identically distributed to real ARIA, so A wins at rate ε\_A\. Therefore B’s distinguishing advantage satisfies the theorem\. ∎

__Corollary \(Q ≤ 2^64\)\.__ Adv\_COLL ≤ ε\_PRF \+ 7/2^129 ≈ ε\_PRF \+ 2^\-126\.

<a id="theorem-2-sdp-reduction-np-hardness"></a>## 7\.4	7\.4 Theorem 2 — SDP Reduction \(NP\-Hardness\)

__Theorem 2\.__ Finding an ARIA nonce collision is at least as hard as decoding a \[2048, 256\] binary linear code\. Finding a collision in polynomial time would imply P = NP\.

__Proof\.__ From the linear algebra representation of Section 3\.4, a collision N\(M\) = N\(M’, sk\) means:

__C\(M, sk\) · β\_vec ⊕ C\(M’, sk\) · β\_vec = 0 in GF\(2^256\)__

Equivalently, letting D = C\(M\) ⊕ C\(M’\) be the 8 × 256 binary difference matrix:

__D · β\_vec = 0 in GF\(2\)^256__

Flatten D to a 2048\-bit binary vector e \(8 blocks of 256 bits\)\. The polynomial multiplication structure of the Vandermonde evaluation corresponds to a 256 × 2048 binary parity\-check matrix H\_β satisfying:

__H\_β · e = 0 \(mod 2\)__

This is Syndrome Decoding with syndrome s = 0 on a \[2048, 256\] binary code\. The maximum error weight is 7 \(the degree of the difference polynomial\)\. SDP is NP\-complete for general parameters \[Berlekamp, McEliece, van Tilborg 1978\]\. Any polynomial\-time ARIA collision\-finder solves this SDP instance in polynomial time, implying P = NP\. ∎

Code Parameter

Value

Notes

Length n

2048

256 bits × 8 coefficients

Dimension k

256

Base field output size

Rate k/n

1/8

Low rate — harder decoding

Max error weight t

7

Degree of difference polynomial

ISD classical

~2^86

Prange / BJMM bound

ISD quantum

~2^43

Grover \+ ISD

__Table 6: SDP parameters for ARIA’s NP\-hardness reduction\.__

<a id="attack-surface-summary"></a>## 7\.5	7\.5 Attack Surface Summary

Attack Vector

Classical

Quantum

Basis

PRF key recovery

2^128

2^64 \(Grover\)

SHA\-256 PRF

Polynomial collision \(SDP\)

~2^86

~2^43 \(Grover\+ISD\)

NP\-hard

Brute\-force birthday

2^128 \(Q=2^128\)

2^64

Unconditional

GF\(2^512\) upgrade

2^162

~2^81

Post\-quantum safe

__Table 7: Attack surface and complexity bounds\.__

<a id="numerical-validation"></a>## 7\.6	7\.6 Numerical Validation

All security reductions are implemented as executable Python and validated:

Test

Result

Notes

Matrix linearity N\(M\)⊕N\(M’\) = D\(β\)

PASS

Exact equality verified

Collision rate ≤ Q\(Q\-1\)/2·7/|F|

PASS

0 observed vs 120 bound \(n=1500\)

D\(β\)=0 root condition

PASS

200/200 polynomial trials

Degenerate β=0 birthday collisions

PASS

Birthday rate confirmed

PRF reduction B runs cleanly

PASS

Both oracle modes tested

__Table 8: Numerical security validation results\.__

<a id="performance"></a># 8	8\. Performance

<a id="python-reference-implementation-measured"></a>## 8\.1	8\.1 Python Reference Implementation — Measured

All measurements are pure Python 3\.12 on commodity hardware\. These figures represent algorithmic complexity, not production performance; they are presented for comparison and algorithmic validation purposes only\.

Operation

Avg µs

Throughput

GF add

0\.2

4,965,591 /s

GF multiply

46\.1

21,714 /s

GF inverse

40\.9

24,462 /s

L2 add

1\.1

886,539 /s

L2 multiply

3,131

319 /s

L2 Horner eval

342

2,921 /s

L3 collapse to GF\(2^256\)

1,453

688 /s

DAG round

4\.8

208,933 /s

DAG next\_gf256 \(4 rounds\)

5\.0

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

__Table 9: Reference implementation measured performance \(Python 3\.12, commodity hardware\)\.__

<a id="production-performance-projections"></a>## 8\.2	8\.2 Production Performance Projections

The dominant cost in ARIA is GF\(2^256\) multiplication, which accounts for the overwhelming majority of cycles in both encoding and nonce derivation\. Hardware acceleration via PCLMULQDQ \(carry\-less multiply\) reduces GF multiplication from ~46 µs \(Python\) to ~33 ns \(C \+ PCLMULQDQ\) — a ~1400× improvement — with a corresponding proportional improvement in AEAD throughput\.

Stage

GF mul latency

AEAD throughput

Notes

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

C \+ PCLMULQDQ \+ AES\-NI

~5 ns

~2,000,000 /s

AES block expansion

AVX\-512 \(8\-way parallel\)

~5 ns/lane

~10,000,000 /s

8 simultaneous nonces

__Table 10: Projected production throughput by implementation tier\.__

<a id="military-application-suitability"></a>## 8\.3	8\.3 Military Application Suitability

Application

Required rate

Met by

Voice radio \(STANAG 4285\)

~8,000 /s

Naive C

Video \(STANAG 4609\)

~120,000 /s

PCLMULQDQ

High\-speed data

~1,000,000 /s

PCLMULQDQ \+ AES\-NI

Tactical data network

~10,000,000 /s

AVX\-512

__Table 11: ARIA throughput requirements across STANAG communication profiles\.__

All identified STANAG tactical communication profiles are achievable without exotic hardware: the PCLMULQDQ instruction has been universally present in x86 processors since Sandy Bridge \(2011\) and all AArch64 processors since ARMv8\-A\.

<a id="known-limitations-and-open-problems"></a># 9	9\. Known Limitations and Open Problems

The items below constitute known gaps between the current research prototype and a production\-grade cryptographic primitive\. All must be addressed before operational deployment\.

__L1 — No EUF\-CMA proof for the authentication tag\.__ The unforgeability argument for the tag is heuristic\. A formal Existential Unforgeability under Chosen Message Attack \(EUF\-CMA\) proof in the standard model, or a reduction to a named hard problem, is required\.

__L2 — DAG\-RNG PRF security is argued but not formally proven\.__ The reduction to SHA\-256 PRF security is argued via the construction, but the meta\-operation selection mechanism \(the rotating operation selector\) is not independently proven to preserve PRF security\. A formal proof or a reduction to an analysable PRG construction is needed\.

__L3 — SHA\-256 keystream is a placeholder\.__ The SHA\-256 chain keystream used in the reference implementation is not the intended production keystream\. Production requires AES\-256\-CTR keyed from the tag, which has a formal IND\-CPA security proof and is implementable in constant time using AES\-NI\.

__L4 — Quantum SDP bound requires field upgrade\.__ The current GF\(2^256\) field gives approximately 2^43 security against Grover \+ ISD quantum attacks\. Upgrading the base field to GF\(2^512\) raises this bound to approximately 2^81, giving security comparable to 162\-bit classical SDP resistance — sufficient for post\-quantum threat models\.

__L5 — No external cryptographic audit\.__ No third\-party cryptanalysis has been performed on ARIA\. This is non\-negotiable before any operational deployment\. A minimum 6\-month review by at least two independent teams with relevant expertise in AEAD design and algebraic cryptanalysis is recommended\.

__L6 — No side\-channel analysis\.__ Constant\-time GF\(2^256\) arithmetic is required for deployment\. The reference implementation uses standard Python integer operations that are not constant\-time; timing and power side\-channel attacks have not been assessed\. PCLMULQDQ\-based implementations must also be verified for constant\-time behaviour\.

__L7 — L3 security contribution not formally quantified\.__ The L₃ layer contributes structural depth to the nonce derivation but its security contribution beyond the NP\-hard SDP bound for the L₂ layer has not been formally quantified\. It may provide defence\-in\-depth against algebraic attacks not captured by the current reduction framework\.

<a id="production-hardening-roadmap"></a># 10	10\. Production Hardening Roadmap

For completeness, we enumerate the recommended hardening steps in order of priority:

1. Replace SHA\-256 keystream with AES\-256\-CTR keyed from tag \(security and speed\)\.
2. PCLMULQDQ\-based GF\(2^256\) multiplication \(~1400× speedup; highest performance impact\)\.
3. AES\-NI coefficient expansion \(~100× speedup on hash\-per\-coefficient bottleneck\)\.
4. AVX\-512 parallelism across 8 simultaneous nonces \(~8× throughput at top end\)\.
5. Formal EUF\-CMA proof for the authentication tag\.
6. Formalise PRF reduction for DAG\-RNG under a standard PRG security definition\.
7. External cryptographic audit \(minimum 6 months, two independent teams\)\.
8. Constant\-time GF arithmetic and side\-channel resistance verification\.
9. GF\(2^512\) upgrade for post\-quantum security margin of ~2^81\.

<a id="conclusion"></a># 11	11\. Conclusion

We have presented ARIA, an authenticated encryption scheme addressing the nonce synchronisation problem in military communications through deterministic syncable nonce derivation\. The three\-layer algebraic tower \(GF\(2^256\) → L₂ = GF\(2256\)\[y\]/\(y8\+y4\+y3\+y\+1\) → L₃\) provides structural depth; the Meta\-DAG provides deterministic shared entropy; the three operational modes \(DAG stream injection, random salt injection, evaluation point drift\) cover the full tactical deployment range\.

Collision resistance is formally bounded by two independent reductions:

1. __PRF reduction:__ Adv\_COLL ≤ ε\_PRF \+ 2^\-126 for Q ≤ 2^64, giving security conditional on SHA\-256 PRF indistinguishability\.
2. __SDP reduction \(unconditional\):__ Finding a collision is NP\-hard; best classical attack requires ~2^86 operations \(ISD\); reducing to GF\(2^512\) gives ~2^81 quantum operations\.

Both reductions are constructive, implemented as executable Python, and validated by 61 automated tests\. Measured throughput on the pure\-Python reference of 155–175 encryptions/second scales to over 10 million encryptions/second with AVX\-512 parallelism — meeting all STANAG tactical communication profiles from voice radio to high\-speed data networks\.

The construction is mathematically sound\. Remaining work is engineering hardening \(AES\-NI, PCLMULQDQ, constant\-time arithmetic\), formal proof completion \(EUF\-CMA for the tag, PRF formalisation for the DAG\-RNG\), and external cryptographic audit before any operational deployment\.

<a id="references"></a># 12	References

\[1\] E\. R\. Berlekamp, R\. J\. McEliece, and H\. C\. A\. van Tilborg\. “On the inherent intractability of certain coding problems\.” *IEEE Transactions on Information Theory*, 24\(3\):384–386, 1978\.

\[2\] A\. Becker, A\. Joux, A\. May, and A\. Meurer\. “Decoding Random Binary Linear Codes in 2^\(n/20\): How 1 \+ 1 = 0 Improves Information Set Decoding\.” *EUROCRYPT 2012*, LNCS 7237:520–536, 2012\.

\[3\] D\. J\. Bernstein\. “ChaCha, a variant of Salsa20\.” *Workshop Record of SASC*, 2008\.

\[4\] W\. Chung, S\. Hwang, S\. Kim, B\. Lee, and J\. Lee\. “Making GCM Great Again: Toward Full Security and Longer Nonces\.” *EUROCRYPT 2025*, LNCS 15601, 2025\.

\[5\] J\. Daemen, S\. Hoffert, G\. Mella, G\. Van Assche, and R\. Van Keer\. “Shaking up authenticated encryption\.” *IEEE EuroS&P 2025*, 861–882, 2025\.

\[6\] N\. Ferguson and B\. Schneier\. *Practical Cryptography*\. Wiley, 2003\.

\[7\] S\. Gueron, A\. Langley, and Y\. Lindell\. “AES\-GCM\-SIV: Full Nonce Misuse\-Resistant Authenticated Encryption at Under One Cycle Per Byte\.” *ACM CCS 2015*, 109–119\.

\[8\] S\. Gueron, A\. Langley, and Y\. Lindell\. “AES\-GCM\-SIV: Nonce Misuse\-Resistant Authenticated Encryption\.” RFC 8452, IETF, April 2019\.

\[9\] D\. A\. McGrew and J\. Viega\. “The security and performance of the Galois/Counter Mode \(GCM\) of operation\.” *INDOCRYPT 2004*, LNCS 3348:343–355, 2004\.

\[10\] National Institute of Standards and Technology\. “Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode \(GCM\) and GMAC\.” *NIST Special Publication 800\-38D*, 2007\.

\[11\] P\. Rogaway and T\. Shrimpton\. “A Provable\-Security Treatment of the Key\-Wrap Problem\.” *EUROCRYPT 2006*, LNCS 4004:373–390, 2006\.

\[12\] J\. P\. Mattsson\. “Collision Attacks on Galois/Counter Mode \(GCM\)\.” *IACR ePrint 2024/1111*, 2024\.

\[13\] T\. Feneuil, A\. Joux, and M\. Rivain\. “Syndrome Decoding in the Head: Shorter Signatures from Zero\-Knowledge Proofs\.” *CRYPTO 2022*, LNCS 13508:541–572, 2022\.

\[14\] O\. \[Redacted\]\. “ARIA Reference Implementation \(aria\.py\)\.” *Independent Defence Research Technical Report*, March 2026\.

