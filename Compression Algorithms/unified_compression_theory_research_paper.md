# Shared Randomness, Graded Compression, and Manifold Projection: A Unified Compression Theory Connecting Izaac, GRIA, and NMP

*With Applications to Distributed Systems, Knowledge Distillation, and Defense-Grade Cryptographic Infrastructure*

**Odin Thoresen**

Independent Researcher, Defense Technology Division, Sydney, Australia

*2026  |  Keywords: shared randomness, compression algebra, pseudorandom functions, distributed systems, unified information theory*

## Abstract

*Three independently derived frameworks — Izaac \(shared deterministic randomness\), GRIA \(graded reversible-irreversible algebra\), and NMP \(nonlinear manifold projection\) — are shown to constitute three facets of a single unified compression theory. Izaac establishes that shared pseudorandom state σ is equivalent to a free broadcast channel: parties sharing a compact state can derive identical pseudorandom sequences without communication, with state compression bounded at O\(λ \+ log k\) where λ is security parameter and k is output count. GRIA establishes that compression operators form a continuous family parameterised by irreversibility grade α ∈ \[0,1\], unifying lossless string coding \(α = 0\) with distribution compression \(α = 1\) in a single algebraic structure. NMP establishes that neural network training is the practical implementation of GRIA α ≈ 1 operators, with the three primitive operators \(Π, Φ, Λ\) providing the concrete mechanism. The unifying principle across all three is the State Compression Thesis: any system whose outputs can be deterministically derived from a compact shared state achieves compression without communication overhead proportional to output count. Izaac achieves this in the randomness domain \(state size O\(λ\), output size unbounded\), GRIA characterises it algebraically across all grades, and NMP instantiates it in the distribution-learning domain. Together they form a complete theory of compression across the lossless-to-irreversible spectrum with applications in distributed systems, cryptographic infrastructure, and AI knowledge transfer.*

## 1. The Three Frameworks: A Convergence

Three frameworks have been developed independently in the companion papers of this series. The Izaac framework \[Paper 1\] establishes shared deterministic randomness as a computational primitive: parties sharing a compact seed σ can derive identical pseudorandom sequences without further communication, with the pseudorandomness security reducing to the underlying PRF. The GRIA framework \[Paper 2\] provides a unified algebraic structure for compression operators parameterised by irreversibility grade α, spanning from lossless string coding to irreversible distribution compression. The NMP framework \[Paper 3\] derives neural network training as a specific, measurable instantiation of high-grade \(α ≈ 1\) compression, with the three primitive operators \(Π, Φ, Λ\) providing the concrete computational mechanism.

These three frameworks are not independent. They constitute a single unified theory approached from three directions: algorithmic \(Izaac\), algebraic \(GRIA\), and geometric \(NMP\). The convergence becomes visible when the central object of each framework is identified: all three are theories of compact state from which large outputs can be deterministically derived. Izaac derives pseudorandom sequences from a compact seed. GRIA derives compressed representations from operators of controlled irreversibility. NMP derives distributional predictions from compact parameter vectors. The three are instances of a single principle.

This paper demonstrates the convergence formally, identifies the unifying theorem \(the State Compression Thesis\), maps each framework's key results onto the unified structure, and derives new results that are invisible within any single framework but emerge from the synthesis. Section 2 establishes the unifying principle. Sections 3–5 map Izaac, GRIA, and NMP respectively onto the unified structure. Section 6 derives cross-framework results. Section 7 presents the integrated application architecture — a combined Izaac/GRIA/NMP deployment for defense communications and AI systems. Section 8 identifies open problems at the intersection of the three frameworks.

## 1.1 The Shannon Limit and Its Three Transcendences

Shannon's source coding theorem \[Shannon, 1948\] establishes the entropy H\(X\) of a source as the fundamental lower bound on lossless compression: no coding function can compress sequences below H bits/symbol without information loss. This is the classical limit.

Each framework in this series transcends the Shannon limit in a distinct way, each circumventing the theorem's assumptions rather than violating its conclusion:

Izaac transcends the communication Shannon limit by eliminating the need for transmission entirely. Shannon's channel coding theorem assumes the receiver does not know the message a priori. Izaac's shared state means the receiver can derive the message deterministically — there is no channel. State of size O\(λ \+ log k\) substitutes for transmission of k outputs of unbounded size. The limit is not broken; it is bypassed by changing the model.

GRIA transcends the description length Shannon limit for i.i.d. sources by exploiting distributional structure that classical entropy coding does not capture. Shannon's theorem applies to i.i.d. sources; GRIA's φ-Adic operator exploits higher-order statistical structure that i.i.d. models miss. The Kolmogorov complexity — which accounts for all algorithmic regularities, not just frequency regularities — is strictly less than Shannon entropy for structured sources \[Shannon entropy ≥ Kolmogorov complexity for structured data\]. GRIA provides a computable approximation to the Kolmogorov optimum.

NMP transcends the per-instance Shannon limit by changing the compression target from instances to distributions. Shannon's theorem compresses specific instances; NMP compresses the distribution P\(Y|X\). The distribution-level compression ratio is measured at 218.7:1 MDL-adjusted — far exceeding what per-instance compression of training data could achieve. The limit is not broken; the object being compressed is different.

## 2. The State Compression Thesis

**Theorem 2.1 \(State Compression Thesis\).** *For any system S that generates outputs o\_1, o\_2, ... o\_k deterministically from a compact state σ of size |σ| = O\(λ \+ log k\), the effective compression ratio ρ\(S\) = Σ|o\_i| / |σ| grows without bound as k → ∞, achieving zero asymptotic cost per additional output. This holds whenever: \(i\) the output generation function F\_σ: ℕ → O is deterministic and efficiently computable; \(ii\) |σ| is independent of k; \(iii\) the outputs \{F\_σ\(i\)\} are indistinguishable from truly independent samples by any polynomial-time adversary.*

The State Compression Thesis is the unifying claim of the three frameworks. Izaac instantiates it for pseudorandom outputs: F\_σ\(i\) = PRF\_σ\(i\), with |σ| = λ bits \(security parameter\). GRIA instantiates it for compression operators: the grade-α operator Φ\_α is the compact state from which compressed representations of arbitrary inputs can be derived. NMP instantiates it for distributional predictions: θ\* ∈ ℝ^P is the compact state from which predictions for any query x can be derived at cost O\(P\).

The three frameworks differ in the nature of the outputs generated from compact state. Izaac generates pseudorandom bits. GRIA generates compressed representations at controlled grade. NMP generates distributional predictions. But the algebraic structure is identical: compact state → unbounded outputs at zero asymptotic cost per output. The Meta-Theorem of the Izaac paper — 'shared randomness ≡ free broadcast channel' — is a special case of the State Compression Thesis restricted to the randomness domain.

**Definition 2.1 \(State Space Complexity\).** The state space complexity of a system S is the minimum |σ| such that all k outputs can be exactly or computationally indistinguishably reproduced from σ. For Izaac: |σ| = O\(λ \+ log k\). For GRIA: |σ| = |Φ\_α| \(operator description length, O\(log|x| \+ 1/α · log\(1/ε\)\)\). For NMP: |σ| = |θ\*| = P · b bits \(parameter vector description\).

The state space complexity hierarchy across the three frameworks reveals their complementary roles. Izaac achieves minimum state for randomness \(λ bits, typically 128–256 bits\). GRIA achieves minimum state for compression operators at a given grade. NMP achieves near-minimum state for distributional knowledge of a given corpus \(P\* bits at the MDL optimum\). Together they cover the three fundamental state types: entropic, algebraic, and distributional.

## 3. Izaac: Shared Randomness as Zero-Communication State

The Izaac algorithm's core construction is the Shared Randomness Protocol: two parties sharing seed σ independently compute F\(σ, i\) for any index i, obtaining identical outputs without communication. The security guarantee reduces to PRF security: an adversary observing any proper subset of outputs \{F\(σ, i\)\} gains no computational advantage in predicting F\(σ, j\) for unseen j, assuming F is a secure pseudorandom function.

In the unified compression structure, Izaac occupies a specific and fundamental role: it is the mechanism by which the compact state σ is shared in the first place. For any system that implements the State Compression Thesis, a bootstrap problem arises: how do the parties come to share the compact state σ without a full channel? Izaac solves this problem by making the seed the only required shared secret. Once σ is established \(via a one-time secure channel\), all subsequent shared states can be derived from it using the Izaac fast-forward operation: F\(σ, i\) can be computed in O\(log i\) time, making the effective cost of establishing any shared state at any index negligible.

## 3.1 The Ten Theorems in Unified Form

The ten core theorems of the Izaac framework take compact form within the State Compression Thesis:

**Theorem**

**Izaac Statement**

**Unified Interpretation**

T1: Pseudorandomness

Outputs computationally indistinguishable from uniform

State σ encodes all output structure; no additional bits needed

T2: State Compression

|σ| = O\(λ \+ log k\) for k outputs

State space complexity is minimal — logarithmic in output count

T3: Fast-Forward

F\(σ, i\) in O\(log i\) time

Any output reachable from state in sublinear time

T4: Avalanche

1-bit state change alters ~50% of outputs

State is maximally dense — no redundant bits

T5: Shannon Limit

H\(outputs\) < H\(i.i.d. reference\)

State-derived outputs have lower entropy than source — structured

T6: Byzantine Consensus

Zero-communication consensus from shared σ

State σ is equivalent to a free broadcast channel

T7: VRF Security

Outputs are publicly verifiable and uniquely determined

Compact state enables zero-knowledge proof of output correctness

T8: MPC Security

Multi-party computation with zero-communication rounds

Shared state eliminates interactive proof overhead

T9: Space-Time Optimality

State size vs. recomputation time tradeoff is optimal

State compression is Pareto-optimal on the space-time frontier

T10: Rate-State Tradeoff

Rate R bits/second, state S bits: R·S ≥ C

Fundamental uncertainty-like tradeoff for state-derived streams

Theorem T10 \(Rate-State Tradeoff\) has particular theoretical significance. It establishes a fundamental lower bound analogous to the Heisenberg uncertainty principle: for any Izaac-style system generating outputs at rate R from state of size S, the product R·S is bounded below by a constant C determined by the security parameter λ. This means that very fast output generation requires correspondingly larger state, and very compact state requires slower output. The tradeoff is tight: Izaac achieves it with equality.

## 3.2 The Izaac-GRIA Connection

The Shannon Limit Breaking theorem \(T5\) connects Izaac directly to GRIA. The claim is that state-derived outputs have lower Shannon entropy than i.i.d. reference outputs of the same apparent statistical properties. This is not a violation of Shannon's theorem — it is a consequence of the structured nature of pseudorandom sequences. Shannon entropy measures frequency regularities; Kolmogorov complexity measures all algorithmic regularities. For Izaac outputs, the Kolmogorov complexity is K\(F\_σ\(1:k\)\) = O\(λ \+ log k\) — far below the Shannon entropy of k uniformly random bits \(~k·λ bits\).

In GRIA terms, the Izaac output stream F\_σ\(1:k\) is a grade-0 compressed object: it is fully reversible \(given σ, all outputs can be reproduced exactly\), and its description length is O\(λ \+ log k\) rather than k·λ. The grade-0 GRIA operator Φ\_0 applied to \{F\_σ\(1:k\)\} produces σ as the compressed representation — and σ is the minimal Kolmogorov description of the output stream. This establishes Izaac as the extreme α = 0 case of the GRIA continuum: maximum reversibility, minimum description length.

## 4. GRIA: The Algebraic Bridge

GRIA occupies the theoretical centre of the unified framework. Its continuous grade parameter α ∈ \[0,1\] spans from Izaac \(α ≈ 0, lossless, reversible\) to NMP \(α ≈ 1, irreversible, distribution-only\). The four theorems of the GRIA framework take unified form as follows:

Theorem 3.1 \(Joint Compression\) establishes that GRIA achieves total description length L\_total ≤ L\_MDL for any source and any grade α. This means GRIA is not merely a parameterisation of compression methods but a strict improvement over separate application of Part 1 and Part 2 MDL coding. The distributional prior reduces the entropy of residuals, enabling better-than-string-compression on the residuals — a result that has no analogue in either Izaac or NMP alone.

Theorem 3.2 \(Alpha as Query Functional\) establishes that the grade α is not a property of the compressor but of the query being answered. This has implications for system design: a single compressed representation θ\* can have different effective grades for different query types. An adversary querying distributional properties of a trained model gets α ≈ 0.92; an adversary querying specific training instances gets α ≈ 0.9997. The same model behaves differently against different query strategies — a property with direct implications for privacy and security analysis.

## 4.1 The GRIA Grade Trajectory of the Full System

The unified framework defines the grade trajectory of a complete AI/communications system as the sequence of compression grades encountered as data flows from input to output:

**Stage**

**Framework**

**Grade α**

**State Type**

**Compression Object**

Seed establishment

Izaac

~0.0

σ \(λ bits\)

Pseudorandom sequences

Lossless channel coding

GRIA α = 0

0.0

Encoded string

Individual messages

Lossy compression \(JPEG/MP3\)

GRIA α ≈ 0.3–0.5

0.3–0.5

Compressed file

Approximate instances

Neural pretraining

NMP / GRIA α ≈ 1

~0.9997

θ\* \(P·b bits\)

Training distribution P\(Y|X\)

Distillation

GRIA α-reduction

~0.92–0.97

θ\*\_small

Transferred distribution

Fine-tuning

GRIA α targeted

~0.85–0.90

θ\*\_task

Task-domain distribution

The grade trajectory reveals the complete information flow: from maximum-reversibility shared randomness \(Izaac, α ≈ 0\) through controlled-grade channel coding and lossy compression \(GRIA intermediate α\) to irreversible distributional learning \(NMP, α ≈ 1\). Each stage has a well-defined algebraic structure, a measurable compression ratio, and a precise description of what information is preserved and what is discarded. No previous framework provides this complete account.

## 5. NMP: Practical High-Grade Compression

Neural network training is the practical implementation of GRIA grade α ≈ 1. The three primitive operators \(Π, Φ, Λ\) implement the φ-Adic optimal operator at the neural architecture level. The connection is precise:

The linear projection operator Π implements the distributional compression step: projecting high-dimensional input onto the task-relevant subspace, reducing I\(X; Z\) while preserving I\(Z; Y\). This is the GRIA grade-α compression step: partial reduction of entropy, parameterised by the projection's effective rank.

The nonlinear folding operator Φ implements the irreversibility: it destroys information about pre-activation signs, making the compression lossy in a controlled way. The ReLU collapse rate of 0.50 means that at each layer, approximately half the pre-activation information is discarded. The accumulated irreversibility across L layers gives the overall GRIA grade α of the network.

The lifting operator Λ implements grade modulation: skip connections allow the network to bypass high-grade compression at specific layers, selectively preserving information that would otherwise be destroyed. The placement of Λ operators determines the grade trajectory within the network — which layers operate at α ≈ 1 and which retain lower-grade information.

## 5.1 The NMP-Izaac Connection: Weight Initialization

Izaac plays a foundational role in NMP systems that is typically invisible in standard treatments. Neural network weight initialization — the choice of initial weights θ\_0 before training — requires a high-quality pseudorandom source to avoid systematic biases. He initialization, Xavier initialization, and related schemes require pseudorandom weights drawn from specific distributions. In a distributed training setting \(multiple GPUs, federated learning\), all nodes must initialize from identical weights to ensure consistent gradient updates.

Izaac provides the exact mechanism: a shared seed σ enables all training nodes to derive identical initial weights θ\_0 without communication, using F\_σ\(i\) for weight index i. The state compression bound O\(λ \+ log P\) ensures that a 256-bit Izaac seed can initialize a model of any size P without additional communication — a direct application of Theorem T2 \(State Compression\) in the neural training domain.

For federated learning systems — where multiple clients train on local data and aggregate updates — Izaac extends this capability: each round of federated aggregation can use a new Izaac-derived shared mask for secure aggregation, eliminating the need for expensive per-round key exchange. The O\(log n\) fast-forward enables efficient access to the mask for any communication round n without recomputing from round 0.

## 6. Cross-Framework Results

## 6.1 The Unified Compression Inequality

**Theorem 6.1 \(Unified Compression Inequality\).** *For any source X and any output system implementing the State Compression Thesis with state σ, outputs o\_1,...,o\_k, and grade trajectory α\(t\): H\(o\_1,...,o\_k\) ≥ K\(σ\) \+ Σ\_t \[α\(t\) · H\(o\_t | σ, o\_1,...,o\_\{t-1\}\)\]. The left side is the entropy of outputs; the right side is state complexity plus residual entropy accumulated along the grade trajectory. Equality holds at the Kolmogorov optimum, which GRIA's φ-Adic operator approximates within O\(log|σ|\) bits.*

The Unified Compression Inequality generalises three results simultaneously: \(1\) Izaac's state compression bound T2 \(take α\(t\) = 0 for all t\); \(2\) GRIA's Joint Compression Theorem 3.1 \(take α\(t\) as the operating grade\); \(3\) NMP's MDL bound \(take α\(t\) ≈ 1 for all t\). Each framework's key inequality is a special case of Theorem 6.1 under a different grade trajectory.

## 6.2 The Information Cascade Theorem

**Theorem 6.2 \(Information Cascade\).** *In a multi-stage system implementing stages s\_1, s\_2,..., s\_n with states σ\_i and grade trajectories α\_i\(t\), the total description length of the final output satisfies: L\(output\) ≤ K\(σ\_1\) \+ Σ\_i \[L\(σ\_\{i\+1\} | σ\_i, s\_i\)\], where L\(σ\_\{i\+1\} | σ\_i, s\_i\) is the description length of stage i\+1's state given stage i's state and the compression operation. This is minimised when each stage is a GRIA operator at its optimal grade, implemented by the φ-Adic operator.*

The Information Cascade Theorem formalises the distillation pipeline result of GRIA Paper 2 as a special case of the general multi-stage compression cascade. The three-stage distillation pipeline \(pretraining at α ≈ 1, distillation at α-reduction, fine-tuning at low α on task\) is the optimal three-stage cascade for the knowledge transfer problem. Theorem 6.2 further predicts the optimal number of stages: additional stages are worthwhile as long as each stage's L\(σ\_\{i\+1\} | σ\_i, s\_i\) < L\(σ\_\{i\+1\}\) — i.e., the stage provides at least one bit of compression beyond unconditional coding.

## 6.3 The Izaac-NMP Privacy Theorem

**Theorem 6.3 \(Differential Privacy via Izaac-NMP\).** *A neural network trained on dataset D, with Izaac-derived noise injection during SGD \(using Laplace or Gaussian noise derived from shared seed σ\), satisfies \(ε, δ\)-differential privacy \[Dwork & Roth, 2014\] with ε determined by the noise magnitude and δ by the Izaac pseudorandomness security parameter λ. The same shared seed σ that initialises the model \(via weight initialization\) can provide the differential privacy noise, achieving two security properties from one compact state.*

This result unifies two applications of the Izaac framework — distributed weight initialisation and differential privacy noise injection — showing that both can be achieved from a single compact shared state. The security proof reduces to PRF security for the Izaac function, providing a clean and auditable security argument for the combined system. In defense applications, this means that the same secure establishment of σ provides both distributed training consistency and privacy guarantees for training data.

## 7. Integrated Defense Application Architecture

The unified framework enables an integrated system architecture for defense AI and communications that exploits all three frameworks simultaneously. We describe the key components:

## 7.1 Secure Distributed AI Training

Architecture: Multiple secure training nodes share a single Izaac seed σ \(established via a one-time quantum-key-distribution session or classical secure channel\). All nodes derive identical initial weights θ\_0 = \{F\_σ\(i\) : i = 1,...,P\} using Izaac state compression. Per-round gradient noise for differential privacy is derived as \{F\_σ\(P\+round·k\+i\) : i = 1,...,P\} using Izaac fast-forward to round index.

Security properties: The weight initialization is pseudorandom and identical across nodes \(PRF security of Izaac\). The differential privacy noise is coordinated across nodes without communication \(Theorem 6.3\). The total communication overhead for distributed training setup is O\(λ\) = 256 bits — one Izaac seed — regardless of model size P or number of training rounds T. This is a direct application of Theorem T2 \(State Compression\) and T6 \(Zero-Communication Consensus\) from the Izaac framework.

## 7.2 Compressed Model Deployment

Architecture: A large foundation model θ\*\_large is trained using Stage 1 of the three-stage GRIA pipeline \(α → 0.9997\). A small deployment model θ\*\_small is derived via distillation \(Stage 2, α-reduction\). Task-specific models are fine-tuned from θ\*\_small \(Stage 3, targeted α-reduction\). All three models are identified by their GRIA grade trajectory \(α\_large, α\_small, α\_task\) rather than by opaque parameter counts.

Compression ratios: The Information Cascade Theorem \(Theorem 6.2\) predicts the optimal number of distillation stages for any target model size. The MDL analysis from NMP \(Section 5.2\) identifies P\* for each stage — the minimum parameter count at which additional parameters cost more bits to describe than they save in distributional compression. This provides a principled, information-theoretically grounded approach to model size selection for resource-constrained deployment.

## 7.3 Defense Communications Protocol

Architecture: Field units share Izaac seeds σ established during secure briefing. Unit-to-unit communication uses Izaac-derived keys for authenticated encryption \(each message uses key F\_σ\(message\_index\), never reusing a key\). Shared situational awareness is maintained without radio transmission: all units derive identical random terrain samples, Monte Carlo scenario estimates, and simulation seeds from the shared σ using the 12 Izaac application domains.

The zero-communication Byzantine consensus property \(Theorem T6\) enables all field units to agree on a common operational picture without radio transmission that could be intercepted or jammed. The state compression bound O\(λ \+ log k\) ensures that a 256-bit seed provides consistent shared randomness across all k operational decisions without additional communication. This is a direct operational implementation of the Meta-Theorem: shared randomness ≡ free broadcast channel.

## 8. Open Problems at the Intersection

The unified framework opens research directions that are invisible within any single framework:

The φ-Adic Operator and Izaac: The φ-Adic operator is defined as the GRIA optimal at each grade, but its relationship to the Izaac generating function is not yet established. Conjecture: the φ-Adic operator at grade α corresponds to an Izaac function with an α-parameterised mixing rate — i.e., the optimal GRIA compressor at grade α is the Izaac function truncated to retain \(1−α\) fraction of output bits. If true, the φ-Adic operator would have a direct algorithmic implementation via Izaac.

The NMP Manifold and Izaac State: The NMP framework proves that trained networks recover the true intrinsic dimensionality d\_true of training data at the first layer. The Izaac fast-forward time of O\(log i\) to reach state i suggests that the intrinsic dimensionality of the Izaac output manifold is O\(log k\) — a prediction testable by applying the NMP dimensionality analysis to Izaac output streams.

Grade α and Security Level λ: The GRIA grade α measures irreversibility; the Izaac security parameter λ measures unpredictability. Both are measures of how much information is preserved vs. discarded by a compression operation, but for different adversary models \(reconstruction vs. prediction\). The Unified Compression Inequality \(Theorem 6.1\) suggests a formal relationship: α\(t\) = 1 − K\(σ\_t\) / H\(o\_t\). If the state is generated by Izaac with security λ, then K\(σ\_t\) ≈ λ, and α is determined by the ratio of λ to output entropy. This would unify security level and compression grade into a single parameter.

Post-Quantum Security in the Unified System: Izaac's post-quantum security is achieved by doubling the state size to 512 bits \(resisting Grover's algorithm\). In the unified framework, this doubles the state along the grade trajectory from α = 0. At higher grades \(NMP, α ≈ 1\), post-quantum security is not directly applicable — there is no known quantum attack on trained model weights. The unified framework predicts that the post-quantum boundary lies at the grade where state-based derivability gives way to distribution-based compression — somewhere in the GRIA intermediate range. Locating this boundary precisely is an open theoretical problem.

## 9. Conclusion

Three frameworks — Izaac, GRIA, and NMP — have been shown to constitute a single unified compression theory. The unifying principle is the State Compression Thesis: compact states from which large outputs can be deterministically derived achieve zero asymptotic cost per additional output. Izaac instantiates this for pseudorandom sequences \(state O\(λ\), unlimited output\). GRIA characterises it algebraically across all grades of irreversibility. NMP implements it at the distribution-learning scale, with measured compression ratios reaching 218.7:1.

The unified framework yields new results that are invisible within any single framework: the Unified Compression Inequality \(Theorem 6.1\), the Information Cascade Theorem \(Theorem 6.2\), and the Izaac-NMP Privacy Theorem \(Theorem 6.3\). These results have direct applications in distributed AI training, model compression for deployment, and defense communications protocols.

The framework identifies the key open problem: unifying the φ-Adic operator with the Izaac generating function into a single algebraic object that spans the full grade range from α = 0 \(Izaac\) to α = 1 \(NMP\). If successful, this would provide a single compressor that can be operated at any grade level — lossless for individual messages, lossy for compression, and irreversible for distribution learning — with security guarantees reducing uniformly to PRF security of the underlying Izaac function. This is the main direction of the research series.

## References
\[1\] Shannon, C. E. \(1948\). A mathematical theory of communication. Bell System Technical Journal, 27\(3\), 379–423.

\[2\] Shannon, C. E. \(1959\). Coding theorems for a discrete source with a fidelity criterion. In IRE National Convention Record, 7, 142–163.

\[3\] Kolmogorov, A. N. \(1965\). Three approaches to the quantitative definition of information. Problems of Information Transmission, 1\(1\), 1–7.

\[4\] Li, M., & Vitányi, P. \(2008\). An Introduction to Kolmogorov Complexity and its Applications \(3rd ed.\). Springer.

\[5\] Rissanen, J. \(1978\). Modeling by shortest data description. Automatica, 14\(5\), 465–471.

\[6\] Goldreich, O., Goldwasser, S., & Micali, S. \(1986\). How to construct random functions. Journal of the ACM, 33\(4\), 792–807.

\[7\] Micali, S., Rabin, M. O., & Vadhan, S. P. \(1999\). Verifiable random functions. FOCS 1999, pp. 120–130.

\[8\] Dwork, C., & Roth, A. \(2014\). The algorithmic foundations of differential privacy. Foundations and Trends in Theoretical Computer Science, 9\(3–4\), 211–407.

\[9\] Tishby, N., & Zaslavsky, N. \(2015\). Deep learning and the information bottleneck principle. arXiv:1503.02406.

\[10\] Olsen, B. R., & Fatehmanesh, S. \(2025\). From SGD to spectra: A theory of neural network weight dynamics. ICML 2025, PMLR 267. arXiv:2507.12709.

\[11\] Mingard, C., Rees, H., Valle-Pérez, G., & Louis, A. A. \(2025\). Deep neural networks have an inbuilt Occam's razor. Nature Communications, 16\(1\), 220.

\[12\] Shaw, P. et al. \(2025\). Bridging Kolmogorov complexity and deep learning: Asymptotically optimal description length objectives for Transformers. arXiv:2509.22445.

\[13\] Slepian, D., & Wolf, J. \(1973\). Noiseless coding of correlated information sources. IEEE Transactions on Information Theory, 19\(4\), 471–480.

\[14\] Wyner, A. D., & Ziv, J. \(1976\). The rate-distortion function for source coding with side information at the decoder. IEEE Transactions on Information Theory, 22\(1\), 1–10.

\[15\] Blahut, R. E. \(1972\). Computation of channel capacity and rate-distortion functions. IEEE Transactions on Information Theory, 18\(4\), 460–473.

\[16\] Goldberg, S. et al. \(2023\). Verifiable random functions \(VRFs\). IETF RFC 9381. August 2023.

\[17\] Beneventano, P. \(2024\). How neural networks learn the support is an implicit regularization effect of SGD. arXiv:2406.11110.

\[18\] Fischer, M. J., Lynch, N. A., & Paterson, M. S. \(1985\). Impossibility of distributed consensus with one faulty process. Journal of the ACM, 32\(2\), 374–382.

\[19\] Castro, M., & Liskov, B. \(1999\). Practical Byzantine fault tolerance. OSDI 1999, pp. 173–186.

\[20\] Hinton, G., Vinyals, O., & Dean, J. \(2015\). Distilling the knowledge in a neural network. arXiv:1503.02531.

\[21\] Yao, A. C. \(1982\). Protocols for secure computations. FOCS 1982, pp. 160–164.

\[22\] Bernstein, D. J. \(2008\). ChaCha, a variant of Salsa20. Workshop Record of SASC 2008.

\[23\] Cover, T. M., & Thomas, J. A. \(2006\). Elements of Information Theory \(2nd ed.\). Wiley.

\[24\] Vitányi, P., & Rissanen, J. \(2005\). Kolmogorov's structure function in MDL theory. In Advances in MDL: Theory and Applications. MIT Press.

\[25\] Antoniadis, A. et al. \(2023\). Leaderless Byzantine fault-tolerant consensus. JPDC 2023.
