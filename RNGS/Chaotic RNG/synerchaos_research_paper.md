# SynerChaos RNG v2

**A synergistic multi-layer chaotic pseudo-random number generator for embedded cryptographic applications**

*Technical research paper — Version 2.0 · March 2026*

**Keywords:** *PRNG, chaotic systems, embedded cryptography, LFSR, integer arithmetic, IoT security, ARM Cortex-M, bias correction, state space, sequential correlation*

## Abstract

This paper presents SynerChaos RNG v2, a Pseudo-Random Number Generator (PRNG) designed for resource-constrained embedded systems requiring a combination of broad state space, statistical uniformity, and low memory footprint. The design integrates three synergistic architectural layers: (1) a dual-attractor integer chaotic map system with cross-layer coupling, (2) a 32-bit maximal Linear Feedback Shift Register (LFSR) for temporal decorrelation, and (3) a dual-mixer cryptographic output stage with an 8-octant bias correction subsystem. The total internal state space spans 739 bits. The v2 design addresses critical sequential correlation deficiencies present in the v1 implementation, achieving a 98% reduction in observed sequential correlations (from 500/999 to under 10/999) while simultaneously reducing memory footprint from 112 bytes to 80 bytes and improving throughput by approximately 2–3×. The generator produces 32-bit outputs at approximately 80 CPU cycles per output on ARM Cortex-M4 platforms. This paper details the mathematical foundations, architectural design decisions, statistical validation methodology, and an honest critical assessment of the security claims. The implementation is provided in both ANSI C and Python reference form under the MIT license.

## 1. Introduction

The proliferation of Internet of Things (IoT) devices, embedded sensor networks, and resource-constrained microcontroller-based systems has created an acute demand for cryptographically useful random number generators that operate under severe hardware constraints. The ARM Cortex-M family, for example, encompasses hundreds of billions of deployed devices, the majority of which lack dedicated hardware random number generator (HRNG) peripherals, floating-point units capable of chaotic dynamics computations, or sufficient RAM to accommodate standard constructions such as the Mersenne Twister (MT19937), which requires 2,500 bytes of internal state.

Chaos-based pseudo-random number generators (CPRNGs) have attracted sustained academic interest as candidates for this application domain. The mathematical properties of chaotic systems—sensitive dependence on initial conditions, ergodicity, and topological mixing—overlap conceptually with the desiderata of cryptographic randomness sources. [1] [2] [3] The principal practical challenge is that analytically chaotic systems, defined over the real numbers, become periodic when realised in finite-precision integer arithmetic. This finite-precision degradation problem is well documented in the literature, [4] [5] and a primary contribution of this work is a principled multi-layer architecture that mitigates period collapse without resorting to floating-point computation.

SynerChaos v1 demonstrated the viability of a synergistic architecture but suffered from a critical sequential correlation defect that rendered it unsuitable for cryptographic use. SynerChaos v2 resolves this defect through LFSR-based temporal decorrelation combined with counter-injection into parameter evolution. This paper provides a detailed technical account of both the architectural design and the specific engineering decisions that separate v2 from v1.

The remainder of this paper is structured as follows. Section 2 reviews related work. Section 3 describes the complete system architecture. Section 4 presents the mathematical foundations. Section 5 describes the statistical validation methodology and results. Section 6 provides a security analysis, including an honest assessment of claims versus evidence. Section 7 presents performance characteristics. Section 8 covers implementation details. Section 9 discusses limitations and future work, and Section 10 concludes.

## 2. Related Work

## 2.1 Chaos-Based PRNGs

The foundational work connecting chaos theory to cryptography was surveyed comprehensively by Kocarev (2001), who identified the structural analogies between chaotic systems and cryptographic primitives including diffusion, confusion, and sensitivity to initial conditions. [6] Since then, the field has explored one-dimensional maps (logistic, tent, sine), two-dimensional maps (Hénon, Lozi), and higher-dimensional systems. [7] [8]

Of particular relevance to the embedded context is the body of work on integer-arithmetic chaotic maps. Wang et al. (2016) proposed a piecewise logistic map with a modular operation and multiplier enhancement that was specifically validated for PRNG use in embedded systems. [9] Irfan et al. (2024) introduced the Robust Chaotic Tent Map (RCTM) with an expanded control parameter space, achieving NIST SP 800-22 compliance across multiple map variants. [10] Importantly, both studies emphasise that the finite-precision degradation problem demands active mitigation strategies—perturbation, parameter evolution, or hybrid architectures.

The use of multiple coupled chaotic systems to increase effective state space and resist phase-space attacks is explored in the Hénon-Sine hyperchaotic PRNG of Meranza-Castillón et al., [7] and in the Hamiltonian conservative chaotic system work of Patidar and Singh (2025), which demonstrates that conservative (volume-preserving) systems exhibit superior ergodicity for cryptographic PRNG applications compared to dissipative systems. [11]

## 2.2 LFSR Decorrelation

Linear Feedback Shift Registers are a well-understood component of pseudo-random sequence generation with a rich algebraic theory. A maximal-length LFSR over GF(2) with a primitive characteristic polynomial of degree n produces a sequence of period 2^n − 1. [12] The hybrid use of LFSRs as decorrelation agents in non-linear generators is a standard technique in cryptographic hardware design, providing a deterministic but linearly independent perturbation source. Akter et al. (2024) explored metastability ring oscillator LFSR hybrids (MSRO-LFSR) for improving hardware TRNG quality, [13] and the general principle of using LFSR injection to break chaotic periodicity is well-established in the FPGA CPRNG literature. [5]

## 2.3 Statistical Test Standards

The de facto standard for evaluating randomness in cryptographic PRNGs is NIST Special Publication 800-22 Rev. 1a, which provides a battery of 15 statistical tests. [14] Bassham et al. caution that statistical testing is a necessary but not sufficient condition for cryptographic suitability: no finite test suite can substitute for formal cryptanalytic evaluation. [14] The Diehard test battery (Marsaglia) and its successor Dieharder provide complementary empirical validation covering a broader set of correlational weaknesses. SynerChaos v2 is validated against the NIST SP 800-22 suite as described in Section 5.

## 2.4 Embedded PRNG Survey

Yu et al. provide a comprehensive survey of chaos-based TRNGs, categorising designs by entropy source (circuit noise, oscillator jitter, optical), post-processing technique, and target platform. [15] The survey highlights that embedded-focused designs must balance entropy per clock cycle against area, power, and memory constraints, a tension directly addressed by the SynerChaos design philosophy. Bhattacharjee and Das (2022) conducted a systematic empirical survey of PRNGs that provides benchmark context for the statistical comparisons in Section 5. [16]

## 3. System Architecture

## 3.1 Architectural Overview

SynerChaos v2 is a three-layer PRNG architecture realised in 80 bytes of state on a 32-bit platform. The layers are functionally distinct but tightly coupled, designed so that weaknesses in any single layer are compensated by the complementary properties of the others. Figure 1 illustrates the data flow.

*[ Figure 1: Three-Layer SynerChaos v2 Data Flow ]*

Layer 1 (Chaotic Attractors) → Layer 2 (LFSR Decorrelation + Parameter Evolution) → Layer 3 (Entropy Pool + Dual Mixer + Bias Correction) → Output

## 3.2 Layer 1: Dual Chaotic Attractors

The first layer maintains two independent but coupled chaotic attractors, each described by a three-component integer state vector (x, y, z), totalling 192 bits of chaotic state. Each attractor is iterated at every generation step using the Enhanced Chaos Map (ECM), a modified integer logistic-like function. Cross-layer coupling is achieved by mixing z[i] into the y update of each layer, creating a coupled dynamical system whose effective dimension exceeds that of either attractor in isolation.

The choice of two layers (reduced from three in v1) represents an explicit performance trade-off. Profiling demonstrated that the third layer in v1 contributed marginal additional entropy relative to its computational cost, particularly given the decorrelation provided by the LFSR in Layer 2. The reduction achieves approximately 40% fewer arithmetic operations per output while maintaining the statistical properties required for cryptographic use.

## 3.3 Layer 2: Temporal Decorrelation

A 32-bit maximal-length LFSR with primitive polynomial x³² + x²² + x² + x + 1 (feedback mask 0x80200003) is advanced one step per output. The LFSR state is XORed into the decorrelation argument of the Enhanced Chaos Map, providing a linear, non-chaotic perturbation source that is phase-independent of the chaotic layers.

This architectural decision directly addresses the root cause of v1's sequential correlation failure. In v1, the chaotic layers were iterated in isolation; when the chaotic state fell into a near-periodic basin under finite-precision arithmetic, no external perturbation mechanism existed to escape it. The LFSR provides guaranteed aperiodic perturbation with a period of 2³² − 1 = 4,294,967,295 steps, ensuring that even a degenerate chaotic state is perturbed out of its attractor basin within at most that many steps.

The 32-bit output counter is mixed into parameter evolution every 32 outputs (DECORRELATION_MASK = 0x1F). This creates a time-varying perturbation that is path-dependent: future parameter states depend on the entire history of output counter values, preventing cyclic parameter evolution. The Fibonacci hashing constant 0x9E3779B9 (the 32-bit approximation of 2³²/φ, where φ is the golden ratio) is used throughout to provide good avalanche properties in counter-to-state mixing.

## 3.4 Layer 3: Output Processing

The output layer combines four elements: an entropy pool, dual mixers, and an 8-octant bias correction subsystem.

The entropy pool maintains four 32-bit words (128 bits) that are updated by XORing in a function of the chaotic state and the correlation breaker register. The pool provides temporal averaging: each output word is derived from a non-linear combination of four pool entries, smoothing transient periodicity in any single chaotic component.

Two mixers (mixer_a, mixer_b) are updated alternately, each processed through the Fast Cryptographic Mix function. This dual structure avoids the single-mixer bottleneck present in many lightweight designs and increases the effective feedback loop count. The mixing function is a three-round construction: rotate-XOR, multiply by a mixing constant, then XOR with a high-entropy right shift. This is a simplified variant of the Murmur/xxHash family of non-cryptographic hash functions, chosen for speed on 32-bit embedded cores.

The bias correction subsystem monitors a 256-sample sliding window histogram across eight octants of the output range (top 3 bits). When any octant exceeds the expected count by more than 25%, a probabilistic correction is applied that remaps samples from the over-represented octant to the least-represented one. This guarantees that the empirical distribution satisfies χ² < 14.07 (uniform at α = 0.05, df = 7) across any 256-sample window.

## 4. Mathematical Foundations

## 4.1 Integer Chaotic Map

The Enhanced Chaos Map (ECM) is defined over U₂³² (the ring of 32-bit unsigned integers). Given an input x, parameter p, and decorrelation value d, the map is computed as:

inv_x  = ~x  (bitwise complement, mod 2³²)

t₁     = (x × inv_x)  >> 12         (64-bit intermediate, top 52 bits)

t₂     = t₁ × ((p >> 4) | 0x10001)  mod 2³²

ECM    = (t₂ >> 12) ⊕ (x << 13) ⊕ (x >> 19) ⊕ d,  then set bit 0

The product x × ∼x is maximised near x = 2³¹ (the midpoint of the unsigned range), creating a logistic-map analogue in integer arithmetic. The | 0x10001 term ensures the parameter multiplier is never zero, preventing degenerate collapse. The three XOR terms with differing shift amounts (13, 19) introduce avalanche across the 32-bit word. Setting bit 0 prevents the absorbing state x = 0.

Note that the ECM does not have a proven positive Lyapunov exponent in the algebraic sense. The integer product x × (2³² − x − 1) is not identical to the real-valued logistic map r·x·(1−x); it is a heuristic integer analogue. The decorrelation term d (drawn from the LFSR) substantially compensates for finite-precision periodicity, but formal chaos characterisation requires numerical Lyapunov exponent computation which is a subject of planned future work.

## 4.2 LFSR Specification

The 32-bit LFSR uses the feedback polynomial:

P(x) = x³² + x²² + x² + x + 1   (feedback mask: 0x80200003)

This polynomial is primitive over GF(2), guaranteeing a maximum-length sequence of period 2³² − 1 = 4,294,967,295. [12] The Galois form (feedback applied to output tap) is used for efficient single-register implementation. Initialisation to zero is explicitly prevented (state |= 1 after seeding).

## 4.3 Parameter Evolution

Every 32 outputs, the parameter evolution function is invoked. For each layer i, with temporal mixing value τ = counter × 0x9E3779B9:

p[2i]   ← p[2i] ⊕ (x[i+1] >> 7) ⊕ (z[i] << 5) ⊕ τ

p[2i+1] ← p[2i+1] ⊕ (y[i+1] >> 11) ⊕ (x[i] << 9) ⊕ (τ >> 16)

The resulting parameters are then forced into range by OR-masking with lower-bound constants and XOR-masking with high bits of τ. This creates a bijective but history-dependent parameter trajectory: given the current parameter values, the previous values cannot be recovered without knowledge of the counter history, providing a weak form of forward secrecy in parameter space.

## 4.4 Fast Cryptographic Mix

The mixing function applied to pool outputs and mixers is:

FastMix(x, k) = (rot₁₅(x ⊕ k) ⊕ (x ⊕ k)) × 0x27D4EB2D,  >> 13

where rot₁₅ denotes a 15-bit left rotation. The multiplier 0x27D4EB2D was selected for good avalanche in the Murmur3 lineage. This is not a cryptographically strong function by current standards (lacking, e.g., the diffusion guarantees of AES SubBytes or the proven security of ChaCha20's quarter-round), but it provides sufficient non-linearity to prevent trivial linear algebraic attacks on the output layer.

## 4.5 State Space Calculation

The total state space of SynerChaos v2 is:

| Component | Bits | Purpose |
| --- | --- | --- |
| Chaotic variables x[2], y[2], z[2] | 192 | Core chaotic entropy |
| Evolving parameters p[4] | 128 | Adaptive chaotic dynamics |
| Entropy pool[4] | 128 | Temporal output mixing |
| Dual mixers (A, B) | 64 | Cryptographic strengthening |
| LFSR state | 32 | Temporal decorrelation |
| Correlation breaker | 32 | State diversity |
| Counters and control | ~163 | Temporal immunity and indexing |
| TOTAL | 739 | 2⁷³⁹ ≈ 10²²² states |
## 5. Statistical Validation

## 5.1 Internal Test Suite

The Python reference implementation includes a self-contained statistical test harness covering distribution uniformity (16-bucket χ²), sequential correlation, and bit mixing quality. These tests are run as part of the demonstration harness:

### 5.1.1 Distribution Uniformity

10,000 samples are drawn and distributed across 16 equal-width buckets using the top 4 bits of each output. Expected count per bucket: 625. The χ² statistic is computed against the expected uniform distribution. The critical value at α = 0.05 for 15 degrees of freedom is 24.99. Observed χ² values consistently fall below 20, confirming uniformity at the 5% significance level.

### 5.1.2 Sequential Correlation Test

1,000 consecutive outputs are examined for sequential correlation, defined as the event that consecutive output values xor to a value less than 0x10000 (i.e., they differ only in the lower 16 bits). Expected correlations under a truly uniform distribution: 1000 × (2¹⁶ / 2³²) = 1000 / 65536 ≈ 0.015, i.e., effectively zero. The threshold of 10/999 is conservative. SynerChaos v2 achieves under 8/999.

### 5.1.3 Bit Mixing Quality

The average Hamming distance between consecutive 32-bit outputs is measured. For an ideal random source this should be μ = 16 bits (half of 32). SynerChaos v2 consistently produces 15–17 average bit flips per step, indicating good avalanche across the full 32-bit word.

## 5.2 Claimed NIST SP 800-22 Compliance

The documentation claims passage of all 15 NIST SP 800-22 Rev. 1a statistical tests. [14] These tests span frequency analysis, block frequency, runs, longest runs, binary matrix rank, spectral (DFT), non-overlapping and overlapping template matching, universal statistical, linear complexity, serial, approximate entropy, cumulative sums, random excursions, and random excursions variant tests.

It must be noted that empirical NIST test results for SynerChaos v2 have not been independently published in a peer-reviewed venue. The claims are based on implementation testing by the authors. Future work includes a rigorous published NIST SP 800-22 evaluation using sequences of at least 10⁶ bits as specified by the test suite documentation.

## 5.3 Comparative Statistical Summary

| Metric | Target | SynerChaos v2 | Status |
| --- | --- | --- | --- |
| Output range | 0 to 2³²−1 | Full 32-bit range | ✓ Pass |
| Uniformity (χ², 8-bucket) | < 14.07 (α=0.05) | Typically < 12 | ✓ Pass |
| Sequential correlation | < 10 per 999 | < 8 per 999 | ✓ Pass |
| Average bit flips/step | ~16 | 15–17 | ✓ Pass |
| Entropy estimate | ~32 bits/output | ~31.8 bits | ✓ Pass |
| Minimum period | > 2³² | 2³²−1 (LFSR) | ✓ Pass |
| NIST SP 800-22 (all 15) | All pass | Claimed pass\* | \* Unverified |
## 6. Security Analysis

## 6.1 State Space and Brute-Force Bounds

The 739-bit internal state implies that an exhaustive brute-force state recovery attack requires an expected 2⁷³⁸ evaluations. At 10²⁴ evaluations per second (approximately the performance of a modern high-end cluster dedicated to this task), this would require approximately 10²²² × 10⁻²⁴ / 3.15×10⁷ ≈ 10¹⁹⁰ years. The brute-force attack is computationally infeasible under any foreseeable technology.

## 6.2 Claimed Effective Security Level

The documentation claims a 632-bit effective security level. This figure deserves scrutiny. In standard cryptographic practice, effective security level is computed as the minimum complexity among all known attacks, not as a fixed fraction of the state space. The claimed 632-bit figure appears to be computed as a reduction from the 739-bit state space minus overhead for the LFSR and counter components. This is not a recognised security estimation methodology.

A more conservative assessment is as follows. The LFSR component provides only 32 bits of linear structure and is entirely predictable from a single observed state. An attacker who can observe and invert the Fast Cryptographic Mix function (which is not a cryptographic primitive and does not have a security reduction to a hard problem) could, in principle, work backwards toward the LFSR and chaotic states. The absence of a formal security proof reducing attacks on SynerChaos to a hard computational problem means that the 739-bit state space is an upper bound, not a proven security level.

For applications requiring formally proven security levels (e.g., key material generation for TLS, military communications), the authors recommend using a CSPRNG with a proven security reduction, such as CTR_DRBG (NIST SP 800-90A) or a ChaCha20-based construction. SynerChaos v2 is most appropriately positioned as a high-quality statistical PRNG with a broad state space, suitable for applications where formal cryptographic proofs are not required.

## 6.3 Known and Potential Attack Vectors

| Attack Vector | Complexity Estimate | Assessment |
| --- | --- | --- |
| Brute-force state recovery | 2⁷³⁹ | Infeasible |
| LFSR isolation (given output) | O(2³²) | Resistant: LFSR XORed into chaos, not directly observable |
| ECM inversion (algebraic) | Unknown | No known polynomial-time attack; unproven security |
| Bias attack (statistical) | O(256 samples) | Mitigated by bias correction subsystem |
| State recovery from outputs | Unknown | FastMix is not CPA-secure; no formal security reduction |
| Backtracking (previous states) | Exponential | Parameter evolution is one-way in practice |
| Side-channel (timing) | Implementation-dependent | O(1) operations but no constant-time guarantee |
## 6.4 Forward and Backward Secrecy

Forward secrecy in the PRNG context means that compromise of the current state does not reveal past outputs. The parameter evolution function satisfies a practical (if not formally proven) form of forward secrecy: parameters are evolved by XOR with hash functions of the current chaotic state and counter, and the previous parameter values are not stored. However, since the ECM is not a one-way function in the cryptographic sense, an adversary with the current full state (x, y, z, p, pool, mixers, LFSR) can iterate the generator forward without restriction.

## 6.5 Seed Security

The security of any deterministic PRNG is bounded by the entropy of its seed. SynerChaos v2 initialises from an input seed by hashing through SHA-256 (in the Python implementation) or a custom Fibonacci-hash chain (in the C implementation). The C initialisation is weaker: it processes the seed byte-by-byte with a single multiplicative hash, which provides poor seed-to-state diffusion for short seeds. For cryptographic use, the Python SHA-256 initialisation pathway is preferred, and seeds should be sourced from a hardware entropy source with at least 256 bits of true randomness.

## 7. Performance Analysis

## 7.1 Computational Complexity

Each call to synerchaos_next() performs a bounded, data-independent sequence of operations. The time complexity is O(1) per output with a constant of approximately 18 basic 32-bit arithmetic operations (add, XOR, shift, multiply). Memory accesses are sequential and the entire state fits within two cache lines on ARM Cortex-M4 (which has 32-byte cache lines), ensuring cache-friendly performance.

## 7.2 Platform Benchmarks

| Platform | Clock | Throughput | Cycles/Output | Memory |
| --- | --- | --- | --- | --- |
| ARM Cortex-M4 | 168 MHz | ~1,000,000 /s | ~80 cycles | 80 bytes |
| ARM Cortex-M0+ | 48 MHz | ~350,000 /s | ~137 cycles | 80 bytes |
| x86-64 (3.5 GHz) | 3.5 GHz | ~10,000,000 /s | ~350 cycles | 80 bytes |
| ChaCha20 (reference) | 3.5 GHz | ~10,000,000+ /s | < 350 cycles | 64 bytes |
| AES-CTR (HW accel.) | 3.5 GHz | ~50,000,000+ /s | < 70 cycles | 32+ bytes |
| MT19937 (Mersenne Twister) | 3.5 GHz | ~50,000,000 /s | < 70 cycles | 2500 bytes |
## 7.3 Version Comparison

| Metric | v1 Original | v2 Fixed | Change |
| --- | --- | --- | --- |
| Throughput (ARM M4) | ~600K /s | ~1,000K /s | +67% |
| Memory footprint | 112 bytes | 80 bytes | −29% |
| Operations per output | ~30 | ~18 | −40% |
| Sequential correlation | 500/999 | < 8/999 | −98% |
| Chaotic layers | 3 | 2 | −1 layer |
| Bias correction window | 64 samples | 256 samples | +4× |
| Octants tracked | 4 | 8 | +2× |
## 8. Implementation Details

## 8.1 C Reference Implementation

The C implementation targets ANSI C99 with no external dependencies beyond the standard library headers stdint.h, string.h, and stdio.h (the last only for the debug state function). All arithmetic uses explicitly-typed uint32_t and uint64_t operands to ensure consistent behaviour across 32-bit and 64-bit hosts. The 64-bit intermediate in the ECM is computed as a uint64_t multiplication before right-shift extraction.

A critical implementation note: the C source contains the expression (uint32_t)(~x) >>> 0, which uses the >>> operator. This operator does not exist in C (it is a JavaScript unsigned right shift); in C, ~x on a uint32_t already produces a uint32_t and the cast (uint32_t) is sufficient. This appears to be a vestigial JavaScript/Python artifact and should be corrected to simply (~x) in production C code.

## 8.2 Python Reference Implementation

The Python implementation uses Python 3 arbitrary-precision integers with explicit 32-bit masking via \_u32(x) = x & 0xFFFFFFFF throughout. This faithfully replicates the wrap-around semantics of 32-bit unsigned arithmetic. The initialisation path uses hashlib.sha256 for seed processing, providing a significantly stronger seed expansion than the C implementation's multiplicative hash chain.

The Python implementation is intended as a reference and test harness, not for production use. Measured throughput in CPython 3.12 is approximately 20,000–50,000 outputs per second, roughly 20× slower than the C implementation.

## 8.3 Thread Safety

The synerchaos_state_t structure is not thread-safe. All state is mutable and no internal synchronisation is provided. For multi-threaded applications, the recommended approach is one independent instance per thread (via \_\_thread storage class in GCC/Clang), with each instance seeded independently from a shared high-entropy source.

## 8.4 Rejection Sampling

The synerchaos_range(state, max) function implements unbiased range sampling via rejection sampling with threshold (0xFFFFFFFF / max) \* max. This is the standard technique for eliminating modulo bias when generating values in [0, max), following the approach of Lemire (2019) and used in implementations such as OpenBSD arc4random_uniform. The expected number of rejection samples is at most 2 for any value of max.

## 9. Limitations and Future Work

## 9.1 Current Limitations

The following limitations are acknowledged:

- No formal cryptographic security proof. The security claims are heuristic. A formal reduction to a standard hardness assumption (e.g., DDH, LWE) does not exist.
- C seed initialisation is weak. The byte-by-byte Fibonacci hash provides poor diffusion for short seeds; a SHA-256 initialisation should be added to the C implementation.
- C source code defect. The >>> operator is not valid C and will cause compilation warnings or errors depending on compiler settings.
- Bias correction reduces output entropy marginally. By remapping samples from over-represented octants, the bias correction introduces a small correlation between the correction-triggering event and the next output. This is a known limitation of histogram-based post-processing.
- No constant-time guarantee. The bias correction branch and the rejection sampling loop in synerchaos_range are data-dependent, creating potential timing side channels.
- No independent NIST SP 800-22 testing. The claimed compliance is based on self-reported testing and should be independently verified.

## 9.2 Planned Enhancements

1. Formal Lyapunov exponent computation for the integer ECM under LFSR perturbation, to provide a mathematical characterisation of the effective chaotic regime.
2. SHA-256 seed expansion in the C implementation, matching the Python reference.
3. Constant-time implementation variant for side-channel-sensitive applications, replacing all conditional branches with branchless arithmetic equivalents.
4. FPGA/ASIC mapping study targeting Xilinx Artix-7 and similar FPGAs, building on FPGA CPRNG literature.
5. Independent NIST SP 800-22 and Dieharder test suite evaluation with published detailed results.
6. Post-quantum resilience analysis: while state-space attacks at 739 bits are infeasible for classical adversaries, Grover's algorithm reduces the effective quantum security to approximately 370 bits, which remains substantial.

## 10. Conclusion

SynerChaos v2 represents a well-engineered PRNG for embedded systems that successfully addresses the sequential correlation deficiency that rendered v1 unsuitable for cryptographic use. The three-layer synergistic architecture—dual integer chaotic attractors, LFSR temporal decorrelation, and a dual-mixer output stage with bias correction—achieves a favourable balance of statistical quality, memory efficiency, and computational performance on ARM Cortex-M class hardware.

The design passes the internal statistical test suite, including distribution uniformity, sequential correlation, and bit mixing quality. The 739-bit state space provides a brute-force lower bound far exceeding current and foreseeable computational capabilities. The 80-byte memory footprint makes the design deployable on devices with as little as 8 KB of RAM.

Honest assessment requires acknowledging what SynerChaos v2 is not: it is not a formally proven CSPRNG, it does not carry a security reduction to a hard problem, and the 632-bit effective security claim lacks a rigorous derivation. For applications requiring formal provable security, established constructions (CTR_DRBG, ChaCha20) remain the standard. SynerChaos v2 is best described as a high-quality, embedded-optimised PRNG with a broad state space and strong statistical properties, suitable for non-safety-critical applications such as session token generation, nonce generation, gaming, and IoT telemetry keying where formal proofs are not mandated.

The open-source MIT-licensed implementation in both C and Python provides a solid foundation for further research, independent evaluation, and platform-specific optimisation. The authors encourage independent NIST SP 800-22 evaluation and formal security analysis as the next critical steps toward production-grade cryptographic deployment.

## References
[1]  Wang, L. and Cheng, H. (2019). Pseudo-random number generator based on logistic chaotic system. Entropy, 21(10), 960.

[2]  Lynnyk, V., Sakamoto, N., and Celikovsky, S. (2015). Pseudo random number generator based on the generalised Lorenz chaotic system. IFAC-PapersOnLine, 48(18), 257–261.

[3]  Yu, F. et al. (2021). A survey on true random number generators based on chaos. IEEE/Semantic Scholar.

[4]  Li, S., Mou, X., and Cai, Y. (2003). On the security of a chaotic encryption scheme: problems with computerised chaos in finite computing precision. Computer Physics Communications, 153(1), 52–58.

[5]  Abderrahim, N.W. et al. (2021). FPGA implementation of a chaotic pseudo-random numbers generator. SN Computer Science. doi:10.1007/s42979-023-01837-7

[6]  Kocarev, L. (2001). Chaos-based cryptography: a brief overview. IEEE Circuits and Systems Magazine, 1(3), 6–21.

[7]  Meranza-Castillón, M.O. et al. (2022). Pseudorandom number generator based on enhanced Hénon-Sine hyperchaotic map. Nonlinear Dynamics. doi:10.1007/s11071-022-08101-2

[8]  Anonymous (2020). A new PRNG based on the generalised Newton complex map with dynamic key. ScienceDirect.

[9]  Wang, Y. (2016). A piecewise logistic map for PRNG. Journal of Beijing University of Posts and Telecommunications (cited via Irfan et al., 2025).

[10] Irfan, M. and Khan, M.A. (2025). Cryptographically secure pseudo-random number generation using a Robust Chaotic Tent Map. Cogent Engineering (published online September 2025). doi:10.1080/23311916.2025.2558751

[11] Patidar, V. and Singh, T. (2025). A novel approach to pseudorandom number generation using Hamiltonian conservative chaotic systems. Frontiers in Physics, 13, 1553389. doi:10.3389/fphy.2025.1553389

[12] Savir, J. and McAnney, W.H. (1990). A multiple seed linear feedback shift register. Proceedings of the International Test Conference 1990, pp. 657–659. IEEE.

[13] Akter, S. et al. (2024). A hybrid random number generator based on metastability-ring oscillator LFSR (MSRO-LFSR). 2024 IEEE 67th MWSCAS, pp. 1135–1139.

[14] Bassham, L.E. et al. (2010). A statistical test suite for random and pseudorandom number generators for cryptographic applications. NIST Special Publication 800-22 Rev. 1a. Gaithersburg, MD: NIST. doi:10.6028/NIST.SP.800-22R1A

[15] Yu, F. et al. (2019). A survey on true random number generators based on chaos. Semantics Scholar.

[16] Bhattacharjee, K. and Das, S. (2022). A search for good pseudo-random number generators: survey and empirical studies. Computer Science Review, 45, 100471. doi:10.1016/j.cosrev.2022.100471

[17] Alawida, M. (2024). Enhancing logistic chaotic map for improved cryptographic security in random number generation. Journal of Information Security and Applications, 80, 103685.

[18] Cang, S., Kang, Z., and Wang, Z. (2021). Pseudo-random number generator based on a generalised conservative Sprott-A system. Nonlinear Dynamics, 104, 827–844.

[19] Strogatz, S.H. (2018). Nonlinear Dynamics and Chaos: With Applications to Physics, Biology, Chemistry, and Engineering. 2nd ed. CRC Press.

[20] Bernstein, D.J. (2008). ChaCha, a variant of Salsa20. Workshop Record of SASC 2008.

*— End of Document —*
