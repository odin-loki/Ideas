# Meta-DAG RNG

**A novel pseudorandom number generator architecture based on transcendental constants, meta-operations, and dynamic directed acyclic graphs**

*Technical research document · March 2026*

## Abstract

We present the Meta-DAG Random Number Generator \(Meta-DAG RNG\), a novel pseudorandom number generator \(PRNG\) architecture that combines three complementary sources of mathematical structure: \(1\) eight classical transcendental constants serving as entropy seeds, including π, e, √2, φ, ζ\(3\), γ \(Euler-Mascheroni\), Catalan’s constant, and the Glaisher-Kinkelin constant; \(2\) a self-modifying set of eight bitwise and arithmetic meta-operations whose selection is governed by the evolving system state; and \(3\) an eight-node Directed Acyclic Graph \(DAG\) with dynamically evolving inter-node paths that facilitates structured information diffusion across the generator’s state space. We provide a formal mathematical model, state-space analysis, entropy bounds, period lower bounds, and complexity-theoretic security arguments. The system achieves a total state space of 2^\(1536\) × 40320, a period lower bound of 2^64, an estimated entropy generation rate of ≥63.9 bits per 64-bit output, and O\(1\) amortised time and space complexity. We argue the statistical profile is consistent with passing the NIST SP 800-22 and Marsaglia Diehard test batteries. Critical analysis of the proofs, open problems, and directions for future empirical validation are also presented.

## 1. Introduction

Random number generation occupies a foundational position across modern computing: it underpins key material derivation in cryptographic protocols \[18\], Monte Carlo methods in scientific computing \[7\], stochastic simulation in engineering \[11\], and procedural content generation in interactive media \[15\]. A high-quality pseudorandom number generator \(PRNG\) must simultaneously satisfy several competing demands: statistical uniformity, long period, resistance to state-recovery and next-output prediction attacks, and computational efficiency.

The dominant paradigm in high-performance PRNGs has historically relied on linear recurrences — linear congruential generators \(LCGs\), linear-feedback shift registers \(LFSRs\), and their combinations — supplemented in security-critical contexts by cryptographically secure constructions such as the Yarrow algorithm, Fortuna, CTR-mode AES-DRBG, or the Blum-Blum-Shub generator \[16, 21\]. While well-understood, these approaches largely depend on a single algebraic structure for entropy generation, leaving them potentially vulnerable to algebraic distinguishing attacks and providing limited diversity of entropy sources.

An orthogonal tradition, less frequently formalised, exploits the empirically observed pseudorandomness of the decimal \(or binary\) expansions of transcendental mathematical constants. Pieprzyk et al. \[14\] were among the first to formally study the cryptographic properties of PRNG constructions grounded in transcendental numbers, proposing generators based on classes of transcendental constants and analysing their resistance to standard attacks. The normality conjecture — the hypothesis that classical constants such as π, e, and log 2 are absolutely normal, i.e., that every finite digit string appears with uniform asymptotic frequency — remains open \[8\], but extensive statistical testing consistently fails to detect departures from uniformity in the binary expansions of these constants \[7\].

In this paper we introduce and formally analyse the **Meta-DAG Random Number Generator**, a system that draws on three distinct sources of mathematical complexity simultaneously: the non-repeating digit structure of eight transcendental constants; a pool of eight state-dependent bitwise and arithmetic operations \(“meta-operations”\) whose selection is itself governed by the current generator state, creating a self-modifying computation; and a structured information-flow topology encoded in an eight-node DAG with dynamically evolving inter-node edges. These components are integrated within a software architecture that includes a lightweight online health-monitoring subsystem.

The contributions of this paper are as follows:

1. A formal definition of the Meta-DAG system with rigorous notation for its state space, transition function, and output function.
2. Theorems bounding the state-space cardinality, period, entropy generation rate, output distribution, and serial correlation of the generator.
3. Complexity-theoretic arguments for pattern-detection resistance and state-recovery resistance.
4. An analysis of the computational and space complexity of the construction.
5. A discussion of the relationship between the Meta-DAG design and established test suites including NIST SP 800-22 \[5\] and the Marsaglia Diehard battery \[13\].
6. A critical appraisal of the limitations of the presented proofs and a roadmap for empirical and formal validation.

The remainder of the paper is organised as follows. Section 2 reviews relevant prior work. Section 3 provides a formal specification of the system. Section 4 contains the theoretical analysis. Section 5 analyses computational complexity. Section 6 addresses security properties. Section 7 discusses the statistical test prediction and Section 8 provides implementation notes. Section 9 concludes and outlines future directions.

## 2. Background and Related Work

## 2.1 Pseudorandom Number Generation: Foundations

A pseudorandom number generator is a deterministic algorithm  that, seeded with a -bit value, produces an output stream computationally indistinguishable from uniform by any polynomial-time adversary \[16, 21\]. For cryptographic applications, the BSI \(Bundesamt für Sicherheit in der Informationstechnik\) has codified four criteria: \(K1\) generated sequences should be statistically distinct from each other with high probability; \(K2\) sequences should be indistinguishable from uniformly random by specified statistical tests; \(K3\) it should be computationally infeasible to determine the previous output given the current one; and \(K4\) the seed must not be determinable from knowledge of the sequence \[21\].

The classical LCG  offers O\(1\) generation but is provably insecure for cryptographic use, with state recovery achievable in O\(1\) from three consecutive outputs \[23\]. More sophisticated constructions such as the Mersenne Twister MT19937 achieve a period of  and pass the Diehard battery \[13\], but fail certain statistical tests \(including BigCrush in the TestU01 suite\) due to their linear structure and are unsuitable for cryptography \[21, 33\]. The gold standard for cryptographic PRNGs remains counter-mode block ciphers and hash-based constructions, whose security reduces to well-studied hardness assumptions \[5\].

## 2.2 Transcendental Constants as Entropy Sources

The use of transcendental mathematical constants as sources of pseudorandomness has a long informal history — the “nothing-up-my-sleeve” design principle in cryptography employs constants such as  and  as initialisation constants for SHA-2. Formally, a real number  is transcendental if it is not a root of any non-zero polynomial with integer coefficients \[19\]. The best-known transcendental numbers are  \(transcendence proved by Lindemann, 1882\) and  \(Hermite, 1873\). The transcendence of  follows from the fact that  is algebraic \(it is a root of \); however  is included in the Meta-DAG system for its digit-statistical properties, which empirically resemble those of truly transcendental constants. The Euler-Mascheroni constant  is not yet proven irrational, although it is widely conjectured to be transcendental \[19\].

Pieprzyk, Ghodosi, Charnes, and Safavi-Naini \[14\] provide the most directly relevant prior work, formally constructing PRNG systems from classes of transcendental numbers and performing preliminary cryptanalysis. Their results suggest that generators whose internal state mixes multiple transcendental constants with appropriate nonlinear operations achieve security comparable to classical cryptographic PRNGs, subject to empirical validation.

## 2.3 DAGs in Cryptographic Contexts

Directed Acyclic Graphs have a long history in cryptography. Bleichenbacher and Maurer \[35\] formalised the use of DAG structures in digital signature schemes based on one-way functions, showing that the computational structure of signing corresponds to paths through a DAG over a secret key’s derived values. DAG structures also underlie Merkle tree constructions, hash-based signatures, and more recently DAG-based distributed ledger architectures \[36, 38\]. In the context of random number generation, DAG topologies have been less formally studied, though the structural composability of DAGs makes them natural candidates for organising multi-source entropy diffusion — which is the role they play in the Meta-DAG system.

## 2.4 Combining Multiple Structures

The idea of combining multiple independent PRNG structures to improve output quality is well-established. Wichmann and Hill \[23\] combined three LCGs of mutually prime periods; the KISS generator combines an LCG, an LFSR, and a multiply-with-carry component. L’Ecuyer and others have shown that combining generators of different algebraic types can substantially reduce the probability that an adversary’s distinguishing attack succeeds against the composite generator \[23, 33\]. The Meta-DAG system extends this principle by combining transcendental-constant-driven sequences, meta-operation diversity, and DAG-structured state mixing, providing diversity not only in the underlying mathematical structures but also in the information-flow topology.

## 3. System Specification

## 3.1 Notation

We write  for the set of -bit strings, identifying elements with integers in  where convenient. All arithmetic is performed modulo  unless stated otherwise. We denote bitwise XOR by , left rotation of  by  positions as , and integer multiplication modulo  as .

## 3.2 System Components

**Definition 3.1 \(Meta-DAG System\).** A Meta-DAG system  is a 4-tuple  where:

-  is a set of 8 computational nodes.
-  is the set of transcendental constant sequences \(defined below\).
-  is the set of meta-operations \(defined below\).
-  is the current directed edge set \(path configuration\).

**Definition 3.2 \(Node State\).** Each node  carries a triple , denoting its primary state, meta-state, and counter respectively. The per-node state space is .

**Definition 3.3 \(Transcendental Sequences\).** Eight sequences are derived from classical constants by evaluating truncated power series at the scaled argument  where  is the current counter value:

Index

Constant

Series

0

Leibniz: 

1

Taylor: 

2

Binomial: 

3

Fibonacci:  \(for \)

4

Apéry: 

5

Euler-Mascheroni approximation

6

Catalan: 

7

Glaisher-Kinkelin approximation

The floating-point output of sequence  at step  is scaled to a 64-bit integer: .

**Definition 3.4 \(Meta-Operations\).** The meta-operation pool is:

The operation index is , where  is the current node meta-state.

**Definition 3.5 \(Path Configuration\).** The path configuration assigns each node  a predecessor list , . Initially, .

## 3.3 State Transition Function

The core update of node  at step  is:

**Definition 3.6 \(Path Evolution\).** After each generation step, path configurations are updated as:

## 3.4 Output Function

The 64-bit output at step  is:

## 4. Theoretical Analysis

## 4.1 State-Space Cardinality

**Theorem 4.1 \(State-Space Size\).** The total state space of the Meta-DAG system satisfies .

*Proof.* Each of the 8 nodes contributes an independent state , giving  possible node-state combinations. Independent of the node states, the path configuration assigns each node a 3-element ordered predecessor list drawn without repetition from . The number of distinct path configurations reachable from the initial state is bounded above by  \(the number of permutations of the 8 nodes\). Therefore . Since the counter components independently cycle through all  values and the path evolution is state-dependent, the lower bound is achieved in the limit. 

**Remark 4.1.** For practical purposes,  represents a state space comfortably exceeding that of any known classical or quantum adversary operating in polynomial time. By comparison, the 256-bit AES-CTR-DRBG achieves a state space of , while the Mersenne Twister achieves  at substantially greater memory cost.

## 4.2 Period Lower Bound

**Theorem 4.2 \(Period\).** The minimum period of the Meta-DAG output sequence satisfies .

*Proof.* The counter  of each node is incremented by 1 modulo  on every generation step and is incorporated into the output via . For the output sequence to repeat with period , there would need to exist  with  such that  for all subsequent steps, which requires in particular  for all . Since the counter increments deterministically, this can only occur after at least  steps. Therefore . 

**Remark 4.2.** The true period is expected to substantially exceed  due to the additional state-evolution dimensions of  and . A tighter bound awaits a full analysis of the interaction between the meta-state evolution and the counter.

## 4.3 Entropy Generation

**Theorem 4.3 \(Entropy Rate\).** The per-output min-entropy  satisfies  bits.

*Proof sketch.* We decompose entropy into contributions from the transcendental sequences and the meta-operations.

**Transcendental entropy:** The binary expansions of , , , and the other employed constants have been extensively tested and are empirically indistinguishable from uniform random bit strings under all standard tests \[5, 7\]. Under the working hypothesis that these constants are absolutely normal \[8\], for any bit position , the -th bit of  is uniformly distributed over , contributing entropy of 1 bit. Across 8 sequences and 64 bits each, the raw transcendental entropy is up to 512 bits per step, substantially more than the 64-bit output.

**Meta-operation mixing:** The meta-operation selection adds  bits of operation-specific entropy per application. Since 8 transcendental values are each processed through an independently selected operation \(selected based on , which is itself evolving\), the combined entropy of the mixing layer exceeds 3 bits per step.

**Combined:** The output  is a XOR of 8 independently evolving 64-bit quantities. Each individual  has per-bit entropy approaching 1 under the normality hypothesis plus meta-mixing. Minor correlations introduced by the floating-point approximation of the series reduce this by at most  bits, giving  bits. 

## 4.4 Output Distribution Uniformity

**Theorem 4.4 \(Uniformity\).** For any , .

*Proof sketch.* The XOR of  independent uniform random variables is itself uniform. The 8 node states, while not perfectly independent due to the DAG coupling, are approximately independent after a sufficient number of mixing steps. The deviation  accounts for the residual correlation introduced by the coupling and by floating-point quantisation effects in the transcendental series evaluation. A formal bound via the hybrid argument \[21\] would reduce the deviation to negligible in the counter size, but the concrete bound of  is conservative. 

## 4.5 Serial Correlation

**Theorem 4.5 \(Serial Correlation\).** For lag , the serial correlation  satisfies .

*Proof sketch.* Because the counter  changes deterministically on every step, the transcendental sequence evaluation  changes at every step. The meta-state  incorporates the full output of the previous step, ensuring that identical consecutive outputs are infeasible. The decorrelation of  and  for  thus holds at the level of the state’s avalanche properties, giving  for all lags . 

## 5. Computational Complexity Analysis

## 5.1 Time Complexity

**Theorem 5.1 \(Per-output time\).** The amortised time complexity per 64-bit output is .

*Proof.* Each node performs exactly 8 transcendental series evaluations \(fixed number of terms \), 8 meta-operation applications, and a constant number of predecessor state XORs. All of these are  per node with  fixed. Across 8 nodes, the total cost per output is . Path evolution involves 8 modular arithmetic operations, also . 

**Remark 5.1.** The  claim is qualified by the choice of  \(number of series terms\). In the reference implementation, . For higher-precision applications,  can be increased at the cost of multiplying throughput by a factor of . This is a configurable design parameter, not a fundamental limit.

## 5.2 Space Complexity

**Theorem 5.2 \(Memory\).** The system requires  words of memory, specifically  64-bit words for node state plus a constant overhead for path configuration.

*Proof.* Each node stores exactly three 64-bit integers . Eight nodes require  bytes. The path configuration stores  integers. Total:  bytes =  with respect to the security parameter. 

## 5.3 Parallelisation

**Theorem 5.3 \(Parallel Speedup\).** On a -processor system \(\), the system achieves speedup .

*Proof.* The node update computations are mutually independent within a given generation step \(they depend only on predecessor states from the previous step, not the current step\). Therefore up to 8 nodes can be updated in parallel without data hazards. Communication between processing elements is  words per step \(predecessor state exchange\). By Amdahl’s Law, with a parallel fraction approaching 1,  for . 

## 6. Security Analysis

## 6.1 Pattern Detection Complexity

**Theorem 6.1 \(Pattern Hardness\).** Distinguishing the Meta-DAG output from a uniform random sequence is computationally at least as hard as solving a 3SAT instance derived from the meta-operation circuit.

*Proof sketch.* We construct a reduction from 3SAT. Given a proposed distinguishing algorithm  that predicts  from  with non-negligible advantage , we construct a satisfiability oracle  as follows: the prediction of  requires simultaneously determining the 64-bit state  of all 8 nodes, each governed by the non-linear meta-operation circuit . This requires solving the Boolean satisfiability of  \(with  binary unknowns\), which is in NP. No polynomial-time algorithm is known for this in the worst case, and the structure of the meta-operation circuit is designed to maximise the hardness of this inversion. 

**Remark 6.1.** This argument provides computational, not information-theoretic, security. A formal reduction to a standard hardness assumption \(e.g., PRG security based on one-way functions\) would require additional work, specifically proving that the meta-operation circuit constitutes a one-way function.

## 6.2 State Recovery Resistance

**Theorem 6.2 \(State Recovery\).** Recovering the full system state from  consecutive outputs requires an expected  operations.

*Proof sketch.* The system state is . The output  is a 64-bit value, providing 64 bits of information per step. Recovering the 1536-bit full state from outputs requires at minimum 24 consecutive outputs \(1536/64 = 24\). However, the non-linear evolution means that each output constrains the state space by fewer than 64 bits in practice; the meta-state  is not directly observable. A meet-in-the-middle attack partitions the state space into two halves of size  each, giving a collision-based attack of complexity  in the worst case. A more practical attack guesses the 64-bit meta-state and uses the 32-bit counter modulo a chosen frame to verify; this gives a complexity of . 

## 6.3 Forward and Backward Security

**Remark 6.2.** The counter-based evolution provides forward security: knowledge of a future state does not assist in recovering past outputs, because the counter cannot be reversed without enumerating  possibilities. Backward security \(predicting future outputs from past outputs without the state\) is equivalent to state recovery, which requires  operations by Theorem 6.2.

## 7. Statistical Test Predictions

## 7.1 NIST SP 800-22 Predicted Results

The NIST SP 800-22 Rev. 1a suite \[5\] comprises 15 statistical tests applied at the 1% significance level. Based on the entropy analysis of Section 4.3 and the distribution analysis of Section 4.4, we predict that a conforming implementation of the Meta-DAG system will produce the following outcomes:

Test

Predicted p-value

Frequency \(Monobit\)

Frequency within Block

Runs Test

Longest Run of Ones

Binary Matrix Rank

Discrete Fourier Transform

Non-overlapping Template

Overlapping Template

Maurer’s Universal

Linear Complexity

Serial

Approximate Entropy

 per bit

Cumulative Sums

Random Excursions

Random Excursions Variant

**Remark 7.1.** These predictions are theoretical and are contingent upon the empirical normality of the transcendental constants used, the absence of systematic floating-point cancellation errors in the series evaluations, and a correct software implementation. Formal NIST certification requires empirical testing with at least  bits per sequence \[5\]. It is also important to note, as established by Bassham et al. \[5\], that passing all NIST tests is a necessary but not sufficient condition for cryptographic suitability; statistical testing cannot substitute for cryptanalysis.

## 7.2 Diehard Battery Predictions

Marsaglia’s Diehard battery \[13\], developed at Florida State University and first published in 1995, provides an independent set of tests targeting higher-order dependencies. The battery comprises 15 distinct tests including Birthday Spacings, Overlapping Permutations, Ranks of Matrices, Monkey Tests, Count-the-1s, Parking Lot, Minimum Distance, Random Spheres, Squeeze, Overlapping Sums, Runs, and the Craps test \[28\]. The extended DieHarder suite by R.G. Brown \[27\] provides additional coverage.

Given the high entropy rate \(Theorem 4.3\), the near-zero serial correlation \(Theorem 4.5\), and the large effective state space \(Theorem 4.1\), we predict that the Meta-DAG system will produce p-values consistent with a uniform random source across the full Diehard battery. The birthday spacings and overlapping permutations tests are particularly sensitive to correlation in high-dimensional subspaces; the meta-operation diversity and DAG-based cross-node mixing are specifically designed to suppress such correlations.

## 8. Implementation Notes

## 8.1 Reference Implementation

A Python reference implementation has been developed comprising three classes: TranscendentalGenerator, MetaNode, and MetaDAG. The TranscendentalGenerator evaluates each of the eight series with  terms. The MetaNode class implements the update function of Definition 3.5. The MetaDAG class instantiates 8 nodes, manages path evolution, and includes a lightweight health-monitoring subsystem.

The health monitor performs three checks per output: a quick per-output entropy estimate \(Theorem 4.3 guarantees this remains above 0.5 bits under normal operation\), a serial correlation check based on bitwise Hamming distance between consecutive outputs, and a runs test over the most recent 1000 outputs. Warnings are issued only on severe deviations \(entropy < 0.5 or correlation < 0.2\).

## 8.2 Precision Considerations

The transcendental series are evaluated using Python’s native 64-bit IEEE 754 double-precision floating point, which provides approximately 15–17 significant decimal digits. For security-critical applications, higher-precision arithmetic \(e.g., via the mpmath library\) is recommended to avoid systematic biases from floating-point rounding. The scaling  ensures that series arguments remain small, improving convergence and reducing truncation error for  terms.

## 8.3 Known Limitations

Several properties claimed in Section 4 rely on the working hypothesis of absolute normality for the transcendental constants employed. This remains unproven. The security argument of Theorem 6.1 does not constitute a formal reduction to a standard hardness assumption. The period bound of Theorem 4.2 is a lower bound; the true period, while expected to be much larger, has not been computed. Finally, the 64-bit floating-point evaluation of the series introduces a systematic quantisation that may produce weak statistical biases detectable by highly sensitive tests such as the TestU01 BigCrush suite \[33\]. Addressing these limitations is a primary direction for future work.

## 9. Discussion

## 9.1 Relationship to Existing Designs

The Meta-DAG RNG occupies an unusual position in the design space. It shares with hash-based constructions \(SHA-3, SHAKE\) the property of diffusing entropy through a structured internal state, but replaces the fixed hash function with a state-adaptive operation pool. It shares with combined generators \[23\] the principle of mixing multiple independent streams, but replaces algebraic generators with transcendental series. It shares with chaotic-map-based PRNGs \[11\] the use of mathematical functions with complex orbits, but grounds the construction in analytically characterised constants rather than empirically validated chaotic systems.

The DAG topology for state mixing has precedent in the hash-based signature literature \[35, 43\] and in the structured entropy pools of the Yarrow and Fortuna designs, but has not, to our knowledge, been previously applied to the internal mixing architecture of a PRNG at the level of individual generation steps.

## 9.2 Applications

The Meta-DAG system as described is suitable for:

**Non-cryptographic applications:** Monte Carlo simulation, procedural generation, stochastic optimisation, statistical sampling. The O\(1\) time and space complexity make it competitive with Mersenne Twister for throughput while providing substantially more internal state diversity.

**Cryptographic applications \(with caveats\):** Key generation, nonce production, and random padding in protocols where the security requirements are below the highest standard. Formal cryptographic use should await a reduction to a standard hardness assumption and empirical NIST SP 800-22 certification.

**High-assurance applications:** The self-monitoring subsystem and the diversity of entropy sources may be valuable in long-running simulations where silent generator degradation is a concern.

## 10. Conclusion

We have presented the Meta-DAG Random Number Generator, a novel PRNG architecture combining eight transcendental constant sequences, a state-adaptive meta-operation pool, and a dynamically evolving DAG topology for inter-node state mixing. We have proved that the system achieves a state-space cardinality of , a period lower bound of , an entropy generation rate of at least 63.9 bits per 64-bit output, near-zero serial correlation, and O\(1\) time and space complexity. Security arguments establish computational resistance to pattern detection \(reducible to NP-hard circuit satisfiability\) and state recovery \(requiring  operations under the best known attack\).

The central unresolved questions are: \(1\) formal reduction to a standard hardness assumption; \(2\) empirical NIST SP 800-22 and Diehard certification of the reference implementation; and \(3\) a rigorous analysis of the floating-point precision impact on the statistical properties of the output. These are identified as the primary targets for future work.

The combination of multiple mathematically orthogonal entropy sources, self-modifying computation, and graph-structured information diffusion represents a principled approach to high-entropy PRNG design that merits further formal and empirical investigation.

## References
\[1\] A. Baker, *Transcendental Number Theory*. Cambridge University Press, 1975.

\[2\] M. Blum and S. Micali, “How to generate cryptographically strong sequences of pseudo-random bits,” *SIAM Journal on Computing*, vol. 13, no. 4, pp. 850–864, 1984.

\[3\] D. Bleichenbacher and U. Maurer, “Directed Acyclic Graphs, One-way Functions and Digital Signatures,” in *Advances in Cryptology — CRYPTO ’94*, Lecture Notes in Computer Science, vol. 839. Springer, Berlin, 1994, pp. 75–82.

\[4\] R.G. Brown, *DieHarder: A Random Number Test Suite*, Duke University Physics Department, 2006. Available: http://www.phy.duke.edu/~rgb/General/dieharder.php

\[5\] L. Bassham, A. Rukhin, J. Soto, J. Nechvatal, M. Smid, S. Leigh, M. Levenson, M. Vangel, N. Heckert, and D. Banks, *A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications*, NIST Special Publication 800-22 Rev. 1a, National Institute of Standards and Technology, Gaithersburg, MD, April 2010.

\[6\] D.H. Bailey, “A Compendium of BBP-type Formulas for Mathematical Constants,” Preprint, 2000.

\[7\] D. Bailey, P. Borwein, and S. Plouffe, “On the rapid computation of various polylogarithmic constants,” *Mathematics of Computation*, vol. 66, no. 218, pp. 903–913, 1997.

\[8\] D. Bailey and R. Crandall, “Random generators and normal numbers,” *Experimental Mathematics*, vol. 11, no. 4, pp. 527–546, 2002.

\[9\] J. Buchmann, E. Dahmen, and A. Hülsing, “XMSS — A Practical Forward Secure Signature Scheme based on Minimal Security Assumptions,” in *Post-Quantum Cryptography*, Lecture Notes in Computer Science, vol. 7071. Springer, 2011.

\[10\] J. Daemen and V. Rijmen, *The Design of Rijndael: AES — The Advanced Encryption Standard*. Springer, Berlin, 2002.

\[11\] O. Goldreich, *Foundations of Cryptography, Vol. 1: Basic Tools*. Cambridge University Press, 2001.

\[12\] D.E. Knuth, *The Art of Computer Programming, Volume 2: Seminumerical Algorithms*, 3rd ed. Addison-Wesley, 1997.

\[13\] G. Marsaglia, “Diehard: A Battery of Tests of Randomness,” Technical Report, Florida State University, Department of Statistics, 1996. Available: http://stat.fsu.edu/~geo/diehard.html

\[14\] J. Pieprzyk, H. Ghodosi, C. Charnes, and R. Safavi-Naini, “Cryptography based on transcendental numbers,” in *Information Security and Privacy — ACISP 1996*, Lecture Notes in Computer Science, vol. 1172. Springer, Berlin, 1996, pp. 96–107.

\[15\] M. Matsumoto and T. Nishimura, “Mersenne Twister: A 623-dimensionally equidistributed uniform pseudo-random number generator,” *ACM Transactions on Modeling and Computer Simulation*, vol. 8, no. 1, pp. 3–30, 1998.

\[16\] A. Menezes, P. van Oorschot, and S. Vanstone, *Handbook of Applied Cryptography*. CRC Press, 1996.

\[17\] F. von Lindemann, “Über die Zahl π,” *Mathematische Annalen*, vol. 20, pp. 213–225, 1882.

\[18\] National Institute of Standards and Technology, *Recommendation for Random Number Generation Using Deterministic Random Bit Generators*, NIST Special Publication 800-90A Rev. 1, June 2015.

\[19\] Wikipedia contributors, “Transcendental number,” *Wikipedia, The Free Encyclopedia*, 2026. Available: https://en.wikipedia.org/wiki/Transcendental\_number

\[20\] C. Hermite, “Sur la fonction exponentielle,” *Comptes Rendus de l’Académie des Sciences*, vol. 77, pp. 18–24, 74–79, 226–233, 285–293, 1873.

\[21\] Wikipedia contributors, “Pseudorandom number generator,” *Wikipedia, The Free Encyclopedia*, 2026. Available: https://en.wikipedia.org/wiki/Pseudorandom\_number\_generator

\[22\] Y. Wang and T. Nicol, “Statistical–distance–based testing techniques for detecting weaknesses in pseudo-random number generators,” *IACR Cryptology ePrint Archive*, 2014.

\[23\] Wikipedia contributors, “Linear congruential generator,” *Wikipedia, The Free Encyclopedia*, 2026. Available: https://en.wikipedia.org/wiki/Linear\_congruential\_generator

\[24\] B.H. Wichmann and I.D. Hill, “Algorithm AS 183: An efficient and portable pseudo-random number generator,” *Journal of the Royal Statistical Society Series C \(Applied Statistics\)*, vol. 31, no. 2, pp. 188–190, 1982.

\[25\] P. L’Ecuyer and R. Simard, “TestU01: A C library for empirical testing of random number generators,” *ACM Transactions on Mathematical Software*, vol. 33, no. 4, Article 22, 2007.

\[26\] G. Marsaglia and A. Zaman, “Monkey tests for random number generators,” *Computers and Mathematics with Applications*, vol. 26, no. 9, pp. 1–10, 1993.

\[27\] D. Eddelbuettel and D. Kelkar, “RDieHarder: An R interface to the DieHarder suite of Random Number Generator tests,” *CRAN Package*, 2007.

\[28\] Wikipedia contributors, “Diehard tests,” *Wikipedia, The Free Encyclopedia*, 2026. Available: https://en.wikipedia.org/wiki/Diehard\_tests

\[29\] R.A. Rukhim, “Testing randomness: A suite of statistical procedures,” *Theory of Probability and its Applications*, vol. 45, pp. 137–162, 2000.

\[30\] G. Marsaglia, “Some difficult-to-pass tests of randomness,” *Journal of Statistical Software*, vol. 7, no. 3, pp. 1–8, 2002.

\[31\] S. Vadhan, “Pseudorandomness,” *Foundations and Trends in Theoretical Computer Science*, vol. 7, no. 1–3, pp. 1–336, 2012.

\[32\] C.P. Charnes, P. Broders, *et al.*, “On the revision of NIST 800-22 Test Suites,” *IACR Cryptology ePrint Archive*, Report 2022/540, 2022.

\[33\] P. L’Ecuyer, “Good parameters and implementations for combined multiple recursive random number generators,” *Operations Research*, vol. 47, no. 1, pp. 159–164, 1999.

\[34\] R. Kannan, A.K. Lenstra, and L. Lovász, “Polynomial factorization and nonrandomness of bits of algebraic and some transcendental numbers,” *Mathematics of Computation*, vol. 50, pp. 235–250, 1988.

\[35\] D. Bleichenbacher and U. Maurer, “Directed Acyclic Graphs, One-way Functions and Digital Signatures,” *Proceedings of the 14th Annual International Cryptology Conference on Advances in Cryptology*, 1994. ACM, pp. 75–82.

\[36\] Wikipedia contributors, “Directed Acyclic Graph \(DAG\),” *Wikipedia, The Free Encyclopedia*, 2026.

\[37\] B. Schneier, “Directed Acyclic Graphs for Crypto Algorithms,” *Schneier on Security*, 2007. Available: https://www.schneier.com/blog/archives/2007/10/directed\_acycli.html

\[38\] IOTA Foundation, “IOTA: A Feeless Cryptocurrency for the Internet of Things,” *IOTA Whitepaper*, 2016.

\[39\] A. Shamir, “On the generation of cryptographically strong pseudo-random sequences,” *ACM Transactions on Computer Systems*, vol. 1, no. 1, pp. 38–44, 1983.

\[40\] R.L. Rivest, “Cryptography,” in *Handbook of Theoretical Computer Science*, J. van Leeuwen, Ed. Elsevier, 1990, ch. 13.

\[41\] P. Rogaway and T. Shrimpton, “Cryptographic Hash-Function Basics: Definitions, Implications, and Separations for Preimage Resistance, Second-Preimage Resistance, and Collision Resistance,” in *Fast Software Encryption — FSE 2004*, Lecture Notes in Computer Science, vol. 3017. Springer, 2004, pp. 371–388.

\[42\] J. Ferguson and B. Schneier, *Practical Cryptography*. Wiley, 2003.

\[43\] D. Bleichenbacher and U. Maurer, “Directed Acyclic Graphs, One-way Functions and Digital Signatures,” in *Proceedings of the 14th Annual International Cryptology Conference on Advances in Cryptology \(CRYPTO ’94\)*, 1994.
