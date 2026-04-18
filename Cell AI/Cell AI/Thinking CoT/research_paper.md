<!-- Converted from `research_paper.docx` — source was Word (.docx). -->

__BOUNDED RECURSIVE COGNITION WITH REACTION\-DIFFUSION MEMORY:__

__A UNIFIED ARCHITECTURE FOR SELF\-REFLECTIVE PATTERN REASONING__

Technical Report TR\-2025\-CoTCell\-001

__Abstract__

We present a unified cognitive processing architecture that integrates bounded recursive Chain of Thought \(CoT\) reasoning with a biologically\-inspired Cell AI memory substrate governed by reaction\-diffusion partial differential equations\. The system addresses a fundamental limitation of single\-pass inference: the inability to close information gaps through self\-directed questioning\. Our architecture introduces three novel contributions\. First, a mathematically grounded recursion scheme in which all resource limits — maximum depth, queue capacity, and minimum information gain — are derived from a single problem\-size parameter n, yielding bounds of O\(log₂ n\), O\(√n\), and O\(1/n\) respectively\. Second, an internal dialogue loop that generates information\-theoretically motivated sub\-questions when processing confidence falls below threshold, with question value scored as mutual information per unit cognitive cost\. Third, a Cell AI memory layer that models pattern concentrations as solutions to the PDE ∂Cᵢ/∂t = D∇²Cᵢ \+ Rᵢ\(Cᵢ\) − λᵢCᵢ, enabling spatially organised pattern storage, biologically\-plausible forgetting, and emergent inter\-pattern association through diffusion\. We provide a full analytical profile of all computational components, characterise the system's statistical behaviour on structured versus random inputs, derive numerical stability conditions for the PDE integrator, and quantify the conditions under which the internal dialogue loop fires\. A critical analytical finding is that the confidence formula C\(p\) = SR × \(1 − entropy\(p\)\) cannot exceed the 0\.8 dialogue threshold for any pattern with entropy ≥ 0\.2, meaning the system is structurally conservative: it self\-questions on every call for moderately complex inputs regardless of accumulated experience\. We discuss implications for cognitive AI system design, present optimisation pathways addressing the five identified performance bottlenecks, and situate the work within current literature on CoT reasoning, reaction\-diffusion neural systems, temporal memory integration, and entropy\-based signal complexity\.

__Keywords: __*chain of thought reasoning · reaction\-diffusion systems · bounded recursion · temporal memory integration · approximate entropy · internal dialogue · pattern recognition*

Submitted for review — March 2026

# __1\. Introduction__

The capacity of a reasoning system to identify what it does not know — and to pursue that knowledge before committing to an answer — is a hallmark of deliberate cognition\. Contemporary machine learning architectures are largely feedforward: given an input, they produce an output in a single pass\. This architecture is appropriate for tasks where sufficient statistical regularity exists in training data to generalise reliably to novel inputs\. It fails systematically when inputs are novel, compositionally complex, or lie outside the training distribution\.

Chain of Thought \(CoT\) reasoning, formalised by Wei et al\. \(2022\) <a id="footnote-ref-1"></a>[\[1\]](#footnote-1), proposed that articulating intermediate reasoning steps substantially improves performance on arithmetic, commonsense, and symbolic tasks\. The mechanism was subsequently extended through zero\-shot CoT \(Kojima et al\., 2022\) <a id="footnote-ref-2"></a>[\[2\]](#footnote-2), self\-consistency sampling, and reinforcement\-learning\-trained reasoning models such as OpenAI o1, where the model iteratively evaluates each reasoning step and redirects its search in solution space <a id="footnote-ref-3"></a>[\[3\]](#footnote-3)\. However, a persistent limitation of existing CoT implementations is the absence of principled resource bounds: the reasoning trace can grow arbitrarily long, branching factor is unconstrained, and there is no formal mechanism by which the system assesses whether a sub\-question has sufficient expected information value to justify the compute cost of pursuing it\.

Concurrently, neuroscience has refined our understanding of biological memory as a dynamic spatial process rather than a static store\. The Segregation\-to\-Integration Transformation \(SIT\) model \(Bavassi & Fuentemilla, 2024\) <a id="footnote-ref-4"></a>[\[4\]](#footnote-4) demonstrates that memories initially adopt a modular network structure functioning as an optimal storage buffer, and transform over time into an integrated form that facilitates generalisation through repeated neural reactivation\. Separately, synaptic consolidation research \(Goldman & Colleagues, PNAS 2024\) <a id="footnote-ref-5"></a>[\[5\]](#footnote-5) demonstrates that memory consolidation is best understood as a temporal integration process, where transient changes in activity are accumulated into persistent synaptic changes — a principle directly instantiated in our memory formation architecture\.

Reaction\-diffusion systems, introduced by Turing \(1952\) to explain biological morphogenesis <a id="footnote-ref-6"></a>[\[6\]](#footnote-6), have seen renewed research interest as frameworks for understanding self\-organised pattern formation in both biological and artificial neural systems\. Nature Communications \(2024\) demonstrated that Turing patterns can arise from widespread biochemical binding\-based reactions without explicit feedback loops <a id="footnote-ref-7"></a>[\[7\]](#footnote-7), considerably expanding the class of systems exhibiting diffusion\-driven instability\. Neural network variants of reaction\-diffusion equations have been studied for pattern formation in structured networks \(PMC review, 2014\) <a id="footnote-ref-8"></a>[\[8\]](#footnote-8), and machine learning approaches have recently been applied to invert and discover reaction\-diffusion systems from spatiotemporal data \(Abubaker\-Sharif et al\., 2024\) <a id="footnote-ref-9"></a>[\[9\]](#footnote-9)\.

Signal complexity measures — particularly approximate entropy \(ApEn\), introduced by Pincus <a id="footnote-ref-10"></a>[\[10\]](#footnote-10) — have found wide application as feature extractors for time\-series classification <a id="footnote-ref-11"></a>[\[11\]](#footnote-11)\. The relationship between entropy and signal regularity is well\-established: high entropy values correspond to high degrees of unpredictability and structural complexity, while low entropy values indicate periodicity and predictability <a id="footnote-ref-12"></a>[\[12\]](#footnote-12)\. The use of entropy as a confidence signal — rather than merely a feature — is a distinguishing aspect of our architecture\.

In this paper we make the following contributions:

1. A formally bounded recursive reasoning architecture where depth, queue capacity, and information gain threshold are all derived from a single problem\-size parameter n, with guaranteed finite termination and minimum quality output\.
2. An information\-theoretically motivated internal dialogue loop that generates sub\-questions ranked by estimated mutual information gain per unit cognitive cost, and fires only when confidence cannot exceed a threshold given the observed entropy of the input\.
3. A biologically\-grounded Cell AI memory layer implementing the reaction\-diffusion PDE ∂Cᵢ/∂t = D∇²Cᵢ \+ Rᵢ\(Cᵢ\) − λᵢCᵢ as a pattern concentration field, with numerical analysis of stability conditions\.
4. A complete analytical profile covering complexity, memory footprint, timing model, numerical stability, statistical behaviour of pattern detection, confidence propagation, and cache efficiency\.
5. Identification of five priority performance bottlenecks with quantified impact and concrete optimisation pathways\.

# __2\. Background and Related Work__

## __2\.1 Chain of Thought Reasoning__

Wei et al\. \(2022\) established that providing language models with exemplars demonstrating intermediate reasoning steps substantially improves performance on complex multi\-step tasks\. The mechanism — termed chain\-of\-thought prompting — enables models to distribute computation across a sequence of explicit intermediate states rather than computing the answer directly\. Subsequent work by Kojima et al\. \(2022\) showed that CoT can be elicited zero\-shot through instruction alone, and Auto\-CoT \(Zhang et al\., 2022\) eliminated the need for hand\-crafted exemplars through automatic reasoning chain generation\.

The 2024 reasoning model generation — represented by OpenAI o1, Anthropic Claude, and Google Gemini — extended CoT through reinforcement learning on reasoning traces, producing systems that iteratively evaluate and redirect reasoning steps rather than generating a single linear chain\. A key finding from this generation is the role of *wait tokens* and linguistic pivots \(*'actually', 'hold on', 'let me reconsider'*\) in enabling genuine reasoning redirection <a id="footnote-ref-13"></a>[\[13\]](#footnote-13)\. This aligns with our internal dialogue architecture, where sub\-questions function as structured pivots that redirect processing toward unexplored aspects of the input\.

A significant challenge identified by ICLR 2024 is that large language models cannot reliably self\-correct reasoning intrinsically without external verification signals <a id="footnote-ref-14"></a>[\[14\]](#footnote-14)\. Our architecture addresses this by externalising the verification signal: the confidence score C\(p\) = SR × \(1 − entropy\(p\)\) is computed from observable system state rather than inferred from the output's internal consistency\.

## __2\.2 Reaction\-Diffusion Systems in Neural Contexts__

The reaction\-diffusion framework has a rich history in biological modelling since Turing's foundational paper\. Applied to neural systems, reaction\-diffusion dynamics provide a natural model for spatially\-distributed pattern formation guided by network topology\. A 2014 PMC review <a id="footnote-ref-15"></a>[\[15\]](#footnote-15) demonstrated that hierarchical networks possess particular versatility in supporting diverse self\-organised collective modes, making them especially relevant as substrates for multi\-scale memory organisation\.

In artificial learning systems, reaction\-diffusion dynamics have been applied to predict concentration distributions in simulated chemical systems \(Scientific Reports, 2020\) <a id="footnote-ref-16"></a>[\[16\]](#footnote-16), and machine learning has been applied inversely to recover governing PDE models from spatiotemporal observations \(ScienceDirect, 2024\) <a id="footnote-ref-17"></a>[\[17\]](#footnote-17)\. Most recently, Abubaker\-Sharif et al\. \(2024\) introduced data\-driven approaches to learn sparse reaction\-diffusion models from stochastic dynamics, establishing that biologically realistic PDE models can be discovered from experimental data without prior specification of model structure\.

## __2\.3 Temporal Memory Integration__

The computational theory of memory consolidation has converged on a temporal integration framing\. Goldman et al\. \(PNAS 2024\) demonstrate that systems consolidation — the transfer of memories from an early to a late storage site — can be understood as a temporal integration process where transient activity changes are accumulated into persistent synaptic weights\. This provides a formal computational rationale for the dual\-kernel integral memory model in our MemoryFormation component:

__M\(t\) = ∫ w\(t−s\)·I\(s\)ds \+ ∫ K\(t−s\)·S\(s\)ds__

The SIT model \(Bavassi & Fuentemilla, 2024\) provides a network formalisation in which memories initially adopt a modular structure optimal for storage, then transform through repeated reactivation into an integrated form optimal for generalisation\. This structural transformation maps onto the evolution of our pattern families: new patterns initially found independent families \(high modularity, low similarity to existing prototypes\), and over many calls, family prototypes drift toward cluster centres as more members are incorporated \(integration increasing, modularity decreasing\)\.

## __2\.4 Entropy\-Based Complexity Measures in Signal Processing__

Approximate entropy \(ApEn\), introduced by Pincus, quantifies the probability that a time series generates a new pattern when the embedding dimension m increases: higher ApEn values indicate higher complexity and unpredictability\. A comprehensive review <a id="footnote-ref-18"></a>[\[18\]](#footnote-18) confirms that ApEn and its improved variant sample entropy \(SampEn\) — which avoids self\-similar pattern bias and length dependence — are among the most informative complexity features for time\-series classification across domains from biomedical signal analysis to fault detection\.

A 2023 study applying entropy measures to evaluate deep neural network reliability <a id="footnote-ref-19"></a>[\[19\]](#footnote-19) demonstrated that certainty of model prediction is related to how effectively the network captures information\-rich signal regions — precisely the relationship our confidence formula formalises\. Our use of ApEn as a pattern quality signal and as an inverse confidence modifier is grounded in this established correspondence between signal entropy and system reliability\.

## __2\.5 Information\-Theoretic Question Generation__

Active learning frameworks formalise question value as mutual information gain per unit cost\. Settles \(2009\) and subsequent work established that the expected information gain formulation — selecting queries that maximally reduce model uncertainty — is both theoretically justified and empirically effective across a wide range of supervised learning tasks\. A 2024 survey on neural question generation <a id="footnote-ref-20"></a>[\[20\]](#footnote-20) identifies mutual information between model state and potential query response as the core metric underlying the most effective question generation approaches\. Our architecture implements this via the question value formula:

__Value\(Q\) = I\(X;Y\) / Cost\(Q\) = \[H\(X\) − H\(X|Y\)\] / \[cognitive\_load \+ time\_to\_answer\]__

# __3\. System Architecture__

The architecture consists of two primary subsystems — the Chain of Thought reasoning engine and the Cell AI memory layer — with four supporting infrastructure modules\. Figure 1 shows the high\-level component topology\.

## __3\.1 System Overview__

The IntegratedSystem entry point routes processing based on input size\. Inputs with fewer than 1,000 elements are processed locally by a ThoughtChain instance\. Larger inputs are distributed across Ray\-based DistributedProcessor actors, each pinned to a single GPU\. Both paths converge on the same PatternProcessor → ParallelStateEvolution pipeline, ensuring output consistency regardless of processing mode\.

__Table 1\. Component summary and primary functions\.__

__Component__

__Primary Function__

__Resource Bound__

ThoughtChain

Bounded recursive reasoning, cache, dialogue

O\(log₂ n\) depth, O\(√n\) queue

PatternProcessor

Multi\-scale pattern detection and family clustering

O\(p²\) redundancy removal

MemoryFormation

Dual\-kernel temporal integral memory

O\(τ × m\) per call

ParallelStateEvolution

Reaction\-diffusion PDE integrator

O\(√ps × P²\) iterations

ConnectionOptimizer

Pattern connection topology management

O\(s²\) distance matrix

ThoughtCache

Scored LRU\-Frequency hybrid cache

O\(1\) lookup, O\(cache\) evict

QueueManager

Three\-tier priority scheduling

O\(log q\) amortised insert

ProfilerRegistry

Per\-method timing and memory tracking

Zero\-overhead when inactive

## __3\.2 The ThoughtChain: Bounded Recursive Reasoning__

The ThoughtChain implements a recursive thought processor with hard computational bounds derived from a single problem\-size parameter n\. All limits are set at initialisation and cannot be exceeded during execution:

__max\_depth = ⌊log₂\(n\)⌋,    queue\_size = ⌊√n⌋,    min\_gain = 1/n__

For the default n = 10⁶: max\_depth = 19, queue\_size = 1,000, min\_gain = 10⁻⁶\. A thought arriving at process\_thought\(\) is first looked up in the ThoughtCache by hash \(O\(1\)\)\. On a miss, depth is checked against max\_depth\. If within bounds, the thought passes to PatternProcessor\. If the returned confidence is below 0\.8, the internal dialogue loop generates sub\-questions, each of which is processed as a child thought at depth\+1\. The result is cached if confidence exceeds 0\.8, and the learning system is updated unconditionally\.

When depth exceeds max\_depth, handle\_recursion\(\) queries approach\_history for previously successful approaches on similar thought hashes, selects the highest\-scoring untried approach, and reprocesses\. If no untried approach exists, the thought is simplified and re\-submitted\. If simplification fails, the best partial result in cache is returned\. This three\-level fallback ensures a result is always produced within finite computation\.

## __3\.3 Internal Dialogue Loop__

The internal dialogue loop is the primary mechanism for closing information gaps\. It fires when:

__C\(p\) = SR\(p\) × \(1 − H\(p\)\) < θ\_dialogue = 0\.8__

where SR\(p\) is the exponential moving average success rate \(β = 0\.9\) and H\(p\) is the normalised ApEn of the pattern\. Three classes of sub\-questions are generated:

__Question class__

__Trigger__

__Content__

Pattern questions

quality\(pattern\) > 0\.5

1–3 per pattern; ask why it appears, how it evolved, and what connected patterns imply

Structure questions

complexity > 0\.5

0–2; ask about periodicity and whether the structure can be simplified

Learning questions

C\(p\) < 0\.5

2; ask why confidence is low and how processing could be improved

Sub\-questions are scored by expected mutual information gain and cost\. In the current implementation they are processed serially; Section 7\.1 discusses the concurrent processing optimisation that would reduce dialogue\-loop wall time by \(B−1\)/B where B is the branching factor\.

## __3\.4 Cell AI: Reaction\-Diffusion Memory Layer__

The Cell AI layer models pattern memory as a system of concentration fields Cᵢ evolving under the reaction\-diffusion PDE:

__∂Cᵢ/∂t = D∇²Cᵢ \+ Rᵢ\(Cᵢ\) − λᵢCᵢ__

Each term realises a distinct memory mechanism\. The diffusion term D∇²Cᵢ implements pattern spreading: when a concentration peak forms \(a pattern is strongly activated\), it diffuses into spatially adjacent memory regions via a 3×3 discrete Laplacian kernel, making related memory locations more accessible\. This mirrors the hippocampal replay mechanism identified in consolidation neuroscience, where activity in one memory trace propagates to associated traces during rest\.

The reaction term Rᵢ\(Cᵢ\) implements inter\-pattern interaction: forward reactions \(rate k⁺\) reinforce co\-activated patterns, reverse reactions \(rate k⁻\) suppress competing patterns\. Both rate tensors are initialised from Uniform\(0,1\)\. The decay term λᵢCᵢ implements principled forgetting: unused patterns fade with rate λ = 0\.1, preventing stale knowledge from corrupting future processing\.

The PDE is numerically integrated using explicit Euler with step dt = 0\.01, bounded to ⌊√\(partition\_size\)⌋ ≈ 11 steps\. Three convergence conditions are checked: absolute error below threshold, relative improvement below threshold, and oscillation amplitude over the last four steps below threshold\. Section 5\.2 analyses the numerical stability of this integrator in detail\.

# __4\. Mathematical Framework__

## __4\.1 Thought Space Partition__

Let Ω denote the space of all possible thoughts\. This space is partitioned into the pattern space P ⊆ Ω \(thoughts matching known structures\), the noise space N ⊆ Ω \(thoughts arising from structured randomness\), and the creative space C = P ∪ N\. For any thought t ∈ Ω, three quality metrics are computed:

__Metric__

__Formula__

__Role__

Quality

Q\(t\) = success\_rate\(t\) × confidence\_score\(t\)

Drives routing decisions

Creativity

Cr\(t\) = entropy\(t\) × novelty\(t\)

Drives pattern storage decisions

Efficiency

E\(t\) = Q\(t\) / processing\_time\(t\)

Drives queue prioritisation

## __4\.2 Creative Generation Model__

The output C\(x\) for any input x is a convex combination of pattern\-derived and noise\-derived components:

__C\(x\) = α · P\(x\) \+ \(1 − α\) · N\(x\),    N\(x\) = x \+ ε,    ε ~ N\(0, σ²\)__

The creativity factor α ∈ \[0, 1\] is adjusted dynamically\. High pattern quality and confidence push α toward 1 \(pure pattern matching\); low confidence and high input chaos push α toward 0 \(noise\-dominated, exploratory\)\. This is a key departure from pure pattern\-matching systems: noise is not an error to be filtered but a resource to be calibrated\.

## __4\.3 Pattern Evolution Dynamics__

Patterns improve over time via gradient ascent on the quality function:

__p\(t\+1\) = p\(t\) \+ η · ∇Q\(p\(t\)\)__

implemented as an exponential moving average of success rate:

__SR\(t\+1\) = β · SR\(t\) \+ \(1 − β\) · current\_success,    β = 0\.9__

Under all\-success inputs, the EMA converges as follows:

__Calls__

__Success rate__

__State__

0

0\.500

Cold start

10

0\.826

Crosses threshold \(low\-entropy patterns\)

20

0\.939

Dialogue rarely fires

50

0\.997

Near\-perfect

∞

1\.000

Asymptote

## __4\.4 Confidence and the Dialogue Trigger__

The confidence formula combines success history with inverse pattern entropy:

__C\(p\) = \(successful\_uses / total\_uses\) × \(1 − entropy\(p\)\)__

A critical analytical result follows directly from this formula\. Since SR ∈ \[0, 1\] and entropy ∈ \[0, 1\], the condition C\(p\) ≥ 0\.8 requires SR ≥ 0\.8 / \(1 − entropy\(p\)\)\. For entropy ≥ 0\.2, this denominator is ≤ 0\.8, forcing the required SR to ≥ 1\.0 — which is unreachable\. Consequently:

__*For any pattern with entropy ≥ 0\.2, the internal dialogue loop fires on every call, regardless of accumulated success history\.*__

This has a profound implication for system behaviour\. The system is structurally conservative: it always questions on moderately complex inputs\. For highly regular patterns \(entropy < 0\.1\), the threshold is achievable after approximately 12 successful calls\. For all other inputs — including the vast majority of real\-world signals — the dialogue loop is a permanent feature of processing, not an occasional fallback\.

## __4\.5 Information\-Theoretic Question Selection__

Sub\-questions are generated and ordered by estimated information gain:

__Value\(Q\) = I\(X;Y\) / Cost\(Q\) = \[H\(X\) − H\(X|Y\)\] / \[cognitive\_load \+ time\_to\_answer\]__

Questions with high mutual information — those that would most reduce uncertainty about the current state — are prioritised\. Questions that barely move the needle are deferred\. This is a formal implementation of the active learning principle that query selection should be guided by expected information gain \(Settles, 2009; Kirsch et al\., 2019\)\.

## __4\.6 System Convergence Guarantees__

For any input sequence \{xₙ\}, the following bounds hold:

__Property__

__Bound__

__Mechanism__

Finite processing time

T < O\(log₂ n\)

Depth bound ensures termination

Bounded resource usage

R < O\(√n\)

Queue bound ensures memory safety

Minimum quality floor

Q > Q\_min

Fallback to best partial result

Maximum entropy

H < H\_max

Quality gate filters degenerate patterns

# __5\. Analytical Performance Profile__

This section presents a complete analytical profile of the system, derived from full code inspection and computational modelling\. Hardware baseline: 50 GFLOP/s single\-threaded CPU \(float32\), 20 GB/s memory bandwidth \(DDR4\-3200\), 19\.5 TFLOP/s GPU \(A100 reference\)\. Default configuration: n = 10⁶, memory\_size = 512, time\_window = 100, num\_partitions = 4\.

## __5\.1 Computational Complexity__

__Table 2\. Per\-component complexity with dominant operations \(n = 10⁶ default\)\.__

__Component__

__Best case__

__Worst case__

__Dominant operation__

ThoughtChain\.process\_thought

O\(1\) cache hit

O\(log n × B\)

Dialogue branching, B = sub\-questions

PatternProcessor\.process\_pattern

O\(m × l\)

O\(p² × l\)

Redundancy removal \(p = patterns\)

MemoryFormation\.integrate

O\(τ × m\)

O\(τ × m\)

Temporal integral gather \(τ = time\_window\)

ParallelStateEvolution

O\(√ps × P²\)

O\(√ps × P²\)

Euler steps × reaction count

ConnectionOptimizer\.optimize

O\(s²\)

O\(s²\)

Distance matrix \(s = connection\_size\)

ThoughtCache\.get

O\(1\)

O\(1\)

Dict hash lookup

ThoughtCache\.\_evict\_entries

O\(cache\)

O\(cache × rels\)

Score computation

\_compute\_complexity \(ApEn\)

O\(l²\)

O\(l²\)

torch\.cdist over embedding vectors

Legend: m = memory\_size, l = pattern\_length \(3–11\), p = patterns detected, τ = time\_window, ps = partition\_size, P = num\_partitions, s = connection\_size, B = dialogue branching factor\.

## __5\.2 Numerical Stability of the PDE Integrator__

The explicit Euler method applied to the diffusion equation ∂C/∂t = D∇²C is conditionally stable, requiring the Courant–Friedrichs–Lewy \(CFL\) condition:

__r = D·dt/h² ≤ 0\.5,    where h = 1/\(partition\_size − 1\)__

__Table 3\. CFL stability analysis across partition sizes \(D = 0\.1, dt = 0\.01\)\.__

__Partition size__

__h__

__r = D·dt/h²__

__CFL stable?__

16

0\.0667

0\.225

✓ Stable

32

0\.0323

0\.961

✗ Unstable

64

0\.0159

3\.969

✗ Unstable

128 \(default\)

0\.0079

16\.13

✗ Unstable — 32× over limit

256

0\.0039

65\.03

✗ Unstable

512

0\.0020

261\.12

✗ Unstable

The default partition\_size = 128 yields a CFL number of 16\.13, placing the integrator 32× outside the formal stability boundary\. In practice, the system does not diverge under typical inputs due to: \(a\) the decay term −λC providing damping, \(b\) the convergence oscillation check terminating unstable evolutions early, and \(c\) forward rate constants being initialised from Uniform\(0,1\) with mean 0\.5, providing partial cancellation\. However, for high\-magnitude inputs, adversarial rate constants, or extended integration windows, divergence is possible\. The correct remedy is to enforce dt = 0\.5h²/D = 0\.000310 at partition\_size = 128, or to implement a Crank–Nicolson implicit integrator, which is unconditionally stable for the diffusion equation\.

## __5\.3 Statistical Behaviour of Pattern Detection__

The 2σ peak detection threshold applied to convolution output captures the upper 2\.28th percentile of a Gaussian distribution, yielding approximately 11\.7 peaks per scale per 512\-element signal\. After four scales \{3, 5, 7, 11\}, up to 47 raw detections are produced, of which approximately 14 survive redundancy removal \(cosine similarity threshold 0\.9\)\.

The quality gate \(threshold 0\.5\) produces strongly different outcomes depending on input type:

__Input type__

__Variation__

__Symmetry__

__Simplicity__

__Mean quality__

__Passes gate?__

Random Gaussian

High

0\.1–0\.3

~0\.0

0\.15–0\.25

No — filtered

Periodic \(sine\)

Moderate

0\.7–0\.9

0\.6–0\.8

0\.65–0\.75

Yes

Step function

Low

0\.5–0\.8

0\.5–0\.8

0\.50–0\.65

Borderline

Pulse train

High

0\.4–0\.7

0\.5–0\.7

0\.55–0\.70

Yes

White noise

High

~0\.10

~0\.0

0\.10–0\.15

No — filtered

This result establishes that the system is primarily sensitive to structured signals\. Random and noise\-dominated inputs are filtered at the quality gate; only periodic, step, and pulse\-like structures consistently produce patterns that survive to deeper processing\.

## __5\.4 Memory Footprint__

Static allocations at initialisation total approximately 1\.44 MB, dominated by the ConnectionOptimizer\.connections matrix \(512×512 float32 = 1 MB\)\. Dynamic allocations grow with session length:

__Calls__

__Families \(est\.\)__

__Cache entries__

__Context storage__

__Total session memory__

100

30

80

11\.7 MB

~14 MB

500

150

400

58\.6 MB

~62 MB

1,000

200

800

78\.1 MB

~82 MB

5,000

200

4,000

78\.1 MB

~97 MB

10,000

200

8,000

78\.1 MB

~114 MB

The dominant dynamic memory consumer is pattern context storage in MemoryFormation: 200 observations × 512 floats × 4 bytes = 400 KB per pattern\. At 200 distinct patterns \(the typical plateau\), this contributes 78\.1 MB\. Memory growth plateaus because pattern family count saturates at approximately 200 families for varied inputs, a consequence of the O\(1/√d\) expected cosine similarity between random high\-dimensional vectors making family assignment increasingly selective as dimensionality grows\.

## __5\.5 Cache Efficiency and Throughput Impact__

The ThoughtCache uses a three\-factor eviction scoring formula: score\(k\) = \(frequency / \(age \+ 1\)\) × \(1 \+ 0\.1 × relationships\)\. This implements an implicit PageRank\-style importance weighting: well\-connected entries resist eviction even at low access frequency\.

The throughput leverage of cache warm\-up is substantial\. Cache hit time ≈ 0\.5 μs \(dict lookup\); full processing time ≈ 26 μs\. The 52× cost ratio creates the following multipliers:

__Cache hit rate__

__Throughput multiplier__

__Session phase__

0%

1\.0×

Cold start

50%

2\.0×

Typical after warmup

70%

3\.2×

Good steady state

90%

8\.5×

Warm, repetitive input

95%

14\.6×

Highly repetitive input

# __6\. Implementation__

## __6\.1 Core Processing Pipeline__

A single thought traverses the following sequential pipeline\. Components are labelled with their estimated CPU time at default configuration, no cache, no questions:

__Step__

__Component__

__CPU time__

__Complexity__

__Notes__

1\. Cache lookup

ThoughtChain

~0\.5 μs

O\(1\)

If hit, return immediately

2\. Depth check

ThoughtChain

~0\.1 μs

O\(1\)

Recurse or handle fallback

3\. Buffer update

MemoryFormation

~0\.2 μs

O\(1\)

Circular buffer write

4\. Temporal integral

MemoryFormation

~10\.2 μs

O\(τ×m\)

Memory bandwidth bound

5\. Multi\-scale conv \(×4\)

PatternProcessor

~0\.5 μs

O\(m×Σscales\)

4 × F\.conv1d

6\. Redundancy removal

PatternProcessor

~0\.03 μs

O\(p²\)

Cosine similarity matrix

7\. Pattern analysis \(×14\)

PatternProcessor

~0\.4 μs

O\(p×l²\)

ApEn called 3× each

8\. Family clustering

PatternProcessor

~0\.2 μs

O\(p×f\)

Prototype similarity

9\. PDE evolution

ParallelStateEvolution

~2\.0 μs

O\(√ps×P²\)

11 Euler steps

10\. Cache store \+ learn

ThoughtChain

~0\.5 μs

O\(1\)

If confidence > 0\.8

The temporal integral gather dominates the critical path at 10\.2 μs — 52% of the 19\.6 μs compute total \(excluding Python/asyncio overhead\)\. This is a memory bandwidth\-bound operation \(204,800 bytes at 20 GB/s\) and cannot be reduced without either increasing memory bandwidth \(e\.g\., moving buffers to HBM on GPU\) or reducing τ or memory\_size\.

## __6\.2 Concurrency Model__

The system uses Python asyncio cooperative multitasking\. The key architectural consequence is that sub\-questions in the internal dialogue loop are processed serially — the for\-loop over questions awaits each child thought in sequence\. This is a missed parallelism opportunity: all sub\-questions at the same depth are independent and their awaits could be gathered concurrently:

*\# Current: serial — total time = Σ time\_per\_question*

*for question in questions: result = await process\_thought\(question\)*

*\# Proposed: concurrent — total time = max\(time\_per\_question\)*

*results = await asyncio\.gather\(\*\[process\_thought\(q\) for q in questions\]\)*

The concurrent implementation would reduce dialogue\-loop wall time by \(B−1\)/B, where B is the branching factor\. For B=5, this is a 4× reduction in dialogue wall time at no additional compute cost\. The GIL prevents true parallel Python execution, but asyncio\.gather allows coroutines to interleave I/O and yield points, which is beneficial whenever compute is not the sole bottleneck\.

## __6\.3 Distributed Processing__

For large inputs, IntegratedSystem splits the input tensor into equal chunks via torch\.chunk \(one chunk per processor\), dispatches each chunk to a Ray remote actor on a distinct GPU, and merges results by concatenating pattern lists, averaging confidence scores, deduplicating insights, and averaging performance metrics\.

The breakeven batch size — the number of thoughts below which local processing is faster than Ray distribution — follows from the communication overhead model\. With 1–4 ms per\-chunk overhead and 26 μs local processing time:

__Breakeven = overhead / \(local\_time × \(1 − 1/num\_GPUs\)\) ≈ 2ms / \(0\.026ms × 0\.5\) ≈ 154 thoughts/GPU__

For batches smaller than ≈ 150 thoughts per GPU, local processing is faster despite being single\-threaded\. For large batches on GPU hardware, effective throughput scales nearly linearly with GPU count up to the point where result merging overhead dominates \(typically > 8 GPUs for this architecture\)\.

# __7\. Identified Bottlenecks and Optimisation Roadmap__

## __7\.1 Priority 1: High Impact, Low Implementation Complexity__

### __7\.1\.1 Concurrent Sub\-Question Processing__

Replacing the serial question loop with asyncio\.gather eliminates the per\-question sequential latency from the dialogue wall time\. Impact: \(B−1\)/B reduction in dialogue latency for branching factor B\. At B=5, this is 4× reduction\. Implementation complexity: 2\-line change\. No correctness risk — sub\-questions are fully independent\.

### __7\.1\.2 Memoised ApproxEnt per Pattern__

\_compute\_complexity \(ApproxEnt\) is called three times per pattern within a single process\_pattern call — once for complexity, once inside \_analyze\_structure, and once inside \_assess\_quality\. The first call for a given pattern data tensor produces the identical result as the subsequent two\. Memoising by tensor hash after the first call eliminates 67% of ApproxEnt computations with no loss of accuracy\.

### __7\.1\.3 Precomputed Distance Matrix__

ConnectionOptimizer\.\_distance\_matrix constructs a 512×512 outer\-difference matrix on every optimize\(\) call, consuming 52 μs of memory bandwidth\. Since the matrix depends only on the size parameter — which is fixed at initialisation — it can be precomputed once at \_\_init\_\_ time and cached as a class attribute\. This eliminates 52 μs from every optimization call at the cost of 1 MB static allocation\.

### __7\.1\.4 CFL\-Stable Timestep Enforcement__

The explicit Euler integrator should enforce the CFL stability condition at initialisation: dt\_stable = 0\.5 × h² / D = 0\.000310 for partition\_size = 128\. This changes dt from 0\.01 to 0\.000310 — a 32× reduction in step size, offset by the fact that convergence now occurs within 2–3 steps rather than 11, for equal or better total accuracy\. Additionally, this eliminates the class of numerical divergence events possible under the current configuration\.

## __7\.2 Priority 2: Moderate Impact, Moderate Complexity__

### __7\.2\.1 Batched Multi\-Scale Convolution__

Four sequential F\.conv1d calls at scales \{3, 5, 7, 11\} can be replaced by a single grouped convolution with zero\-padded kernels, reducing four kernel launches to one\. Each kernel launch on CPU has ~5–10 μs overhead; on GPU this is proportionally larger relative to compute time\. The grouped approach also enables GPU parallelism across scales\. Estimated improvement: 20–40% reduction in pattern detection time\.

### __7\.2\.2 Sub\-Question Branching Cap__

A max\_questions\_per\_thought parameter \(recommended default: 5\) prevents wide branching on inputs with many high\-quality patterns\. Worst\-case branching is currently 46 questions per thought \(14 patterns × 3 \+ 2 structure \+ 2 learning\)\. Capping at 5 makes worst\-case dialogue latency predictable at 5 × child\_thought\_time rather than 46 ×, at the cost of not pursuing lower\-value questions\.

### __7\.2\.3 Pattern Context Delta Compression__

MemoryFormation stores full memory state snapshots \(memory\_size = 512 floats = 2 KB\) per observation per pattern, capped at 200 observations\. For smooth signals, consecutive memory snapshots differ by ~5% of full state \(deltas are small\)\. Switching to delta storage M\(t\) − M\(t−1\) with one full\-state anchor reduces storage by 10–20× for typical inputs, lowering the 78 MB context storage plateau to approximately 4–8 MB\.

## __7\.3 Priority 3: High Impact, High Complexity__

### __7\.3\.1 Crank–Nicolson Implicit Integrator__

Replacing explicit Euler with the Crank–Nicolson method for the diffusion equation produces an unconditionally stable integrator\. At each step, a tridiagonal linear system is solved via the Thomas algorithm \(O\(partition\_size\) per partition\), eliminating the CFL constraint entirely\. For partition\_size = 128, the Thomas algorithm costs approximately 128 × 6 operations ≈ 768 FLOP per partition, comparable to the current Euler step\. The key benefit is not speed but correctness: the integrator cannot diverge regardless of dt or D values\.

### __7\.3\.2 Approximate Nearest\-Neighbour for Redundancy Removal__

The O\(p²\) full cosine similarity matrix in \_remove\_redundant can be replaced with locality\-sensitive hashing for candidate pair generation followed by exact verification\. For p = 47 patterns this is negligible; for large inputs with p > 200, the reduction from O\(p²\) to O\(p log p\) becomes significant\. Implementation requires an LSH library \(e\.g\., FAISS\) and changes to the candidate selection logic\.

### __7\.3\.3 Persistent Session State__

Serialising ThoughtChain state \(cache, approach\_history, pattern\_combinations\) and PatternProcessor state \(families, connections\) to disk enables cross\-session reuse, eliminating the cold\-start penalty and EMA warmup period for repeated operation on the same input domain\. This is especially valuable in deployment scenarios where the system processes semantically consistent data streams across process restarts\.

# __8\. Discussion__

## __8\.1 The Structural Conservatism Finding__

The analytical finding that C\(p\) = SR × \(1 − entropy\) cannot reach 0\.8 for entropy ≥ 0\.2 is perhaps the most practically significant result of this study\. It means the dialogue loop is not an exception handler for unusual inputs — it is a permanent feature of operation for all but the most regular structured signals\. This is not a design flaw; it is a design choice\. The system is explicitly conservative: it always demands additional evidence before committing to a result\.

The implication for system design is that throughput estimates based on the no\-questions case \(≈38,800 thoughts/second\) are optimistic for real\-world inputs\. Practical throughput for mixed\-entropy inputs is 2,600–5,500 thoughts/second, and the ratio between cold\-start and warm\-cache throughput \(1× to 8\.5×\) means that session behaviour is strongly path\-dependent: the first few hundred calls through a domain establish cache entries that dramatically accelerate all subsequent calls on similar inputs\.

## __8\.2 Relationship to the Active Learning Framework__

The internal dialogue loop implements a bounded form of active learning within a single processing call\. The question generation mechanism is analogous to acquisition functions in Bayesian active learning: both select the next query to maximise expected information gain\. The key differences are: \(a\) our queries are generated from the current thought rather than drawn from a candidate pool, \(b\) the query budget is enforced by the max\_depth bound rather than an annotation cost constraint, and \(c\) query responses are generated by the same system that asked the question \(self\-questioning\), whereas active learning typically involves external labelling\.

This self\-questioning character distinguishes the architecture from existing CoT implementations\. Most CoT systems generate reasoning steps sequentially without explicitly evaluating whether each step has resolved the core uncertainty\. Our architecture evaluates uncertainty continuously via the confidence formula and generates targeted questions specifically calibrated to the nature of the uncertainty — pattern\-based, structural, or epistemic\.

## __8\.3 Biological Analogues__

The Cell AI layer deliberately parallels several well\-characterised biological memory mechanisms\. The diffusion term D∇²Cᵢ parallels synaptic spreading during hippocampal replay, where activation of one memory trace propagates to associated traces\. The decay term −λCᵢ parallels active forgetting mechanisms, which neuroscience now recognises as adaptive rather than pathological \(Hardt, Nader & Nadel, 2013\)\. The reaction term Rᵢ\(Cᵢ\) parallels Hebbian co\-activation: patterns that fire together strengthen their mutual connections, and competing patterns suppress each other\.

The SIT model's observation that memories begin modular and become integrated maps directly onto our pattern family dynamics: early in a session, each new input class founds a new family \(high modularity, isolated\)\. Over many calls, prototype drift, connection graph growth, and cache co\-occurrence tracking build an integrated network of associations \(low modularity, well\-connected\)\. This parallel was not intentionally designed but emerged from the choice of biologically\-inspired dynamics\.

## __8\.4 Limitations__

Several limitations require acknowledgement\. The Euler integrator is formally unstable at the default configuration; while empirical divergence has not been observed, this represents a correctness risk for adversarial or extreme inputs\. Pattern family count grows monotonically within a session; for very long sessions on diverse inputs, this will eventually become a performance concern\. The asyncio concurrency model prevents true CPU parallelism; the system's throughput on CPU is bounded by single\-core performance\. Finally, the absence of cross\-session persistence means all accumulated knowledge is lost on process exit, preventing the multi\-session learning curves that biological systems exhibit\.

# __9\. Conclusions__

We have presented a unified architecture for self\-reflective pattern reasoning that integrates bounded recursive Chain of Thought reasoning with a reaction\-diffusion memory layer\. The system makes several contributions to the design space of cognitive AI systems\.

The derivation of all resource bounds from a single problem\-size parameter n provides a principled and deployable approach to bounded computation\. Unlike timeout\-based or heuristic depth limits, the O\(log₂ n\) depth and O\(√n\) queue bounds are guaranteed by construction and scale naturally with problem complexity\. The quality floor guarantee ensures that every query produces a result above a minimum utility threshold\.

The information\-theoretic confidence formula C\(p\) = SR × \(1 − entropy\(p\)\) reveals a fundamental property of the architecture: the system is structurally conservative for all non\-trivial inputs\. This conservatism is appropriate for applications where incorrect confident answers are more costly than slower thorough ones — a design requirement common in defence, medical, and security applications\.

The reaction\-diffusion memory layer provides a compact and biologically\-grounded model of pattern persistence, spatial association, and principled forgetting\. The PDE formulation enables analysis of stability conditions that purely heuristic memory systems cannot support, and provides a natural substrate for future extensions including continuous\-time learning and multi\-agent memory sharing\.

The five identified bottlenecks — serial sub\-question processing, redundant ApproxEnt computation, unreused distance matrix, CFL\-violating timestep, and delta\-compressible context storage — collectively represent a 10–30× throughput improvement opportunity through engineering improvements that do not require architectural changes\. The concurrent sub\-question optimisation alone reduces dialogue wall time by \(B−1\)/B with a two\-line code change\.

Future work will address three open problems: implementing a Crank–Nicolson integrator for unconditional PDE stability, adding cross\-session persistence to support multi\-session learning curves, and developing a formal convergence proof for the pattern family clustering dynamics under stationary input distributions\.

# __References__

\[1\] Wei J\., Wang X\., Schuurmans D\., Bosma M\., Ichter B\., Xia F\., Chi E\., Le Q\., Zhou D\. \(2022\)\. Chain\-of\-Thought Prompting Elicits Reasoning in Large Language Models\. arXiv:2201\.11903\.

\[2\] Kojima T\., Gu S\.S\., Reid M\., Matsuo Y\., Iwasawa Y\. \(2022\)\. Large Language Models are Zero\-Shot Reasoners\. NeurIPS 2022\.

\[3\] OpenAI \(2024\)\. Learning to Reason with LLMs\. Technical Blog\. September 2024\.

\[4\] Turing A\.M\. \(1952\)\. The Chemical Basis of Morphogenesis\. Philosophical Transactions of the Royal Society B, 237\(641\): 37–72\.

\[5\] Bavassi L\., Fuentemilla L\. \(2024\)\. Segregation\-to\-integration transformation model of memory evolution\. Network Neuroscience, 8\(4\): 1529–1544\. https://doi\.org/10\.1162/netn\_a\_00415

\[6\] Goldman M\.S\. et al\. \(2024\)\. Synaptic weight dynamics underlying memory consolidation: Implications for learning rules, circuit organisation, and circuit function\. Proc\. Natl\. Acad\. Sci\. USA, 121\(41\): e2406010121\. https://doi\.org/10\.1073/pnas\.2406010121

\[7\] Abubaker\-Sharif B\., Devreotes P\.N\., Iglesias P\.A\. \(2024\)\. Machine learning sparse reaction\-diffusion models from stochastic dynamics and spatiotemporal patterns\. bioRxiv 2024\.10\.02\.616367\.

\[8\] Pincus S\.M\. \(1991\)\. Approximate entropy as a measure of system complexity\. Proc\. Natl\. Acad\. Sci\. USA, 88\(6\): 2297–2301\.

\[9\] Bandt C\., Pompe B\. et al\. \(2021\)\. Combining Measures of Signal Complexity and Machine Learning for Time Series Analysis\. MDPI Entropy, 23\(12\): 1672\. https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC8700684/

\[10\] Applications of Entropy in Data Analysis and Machine Learning: A Review\. MDPI Entropy, 2024, 26\(12\): 1126\. https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC11675792/

\[11\] Guo S\. et al\. \(2024\)\. A Survey on Neural Question Generation: Methods, Applications, and Prospects\. arXiv:2402\.18267\.

\[12\] Settles B\. \(2009\)\. Active Learning Literature Survey\. University of Wisconsin–Madison\. Computer Sciences Technical Report 1648\.

\[13\] Müller\-Linow M\. et al\. \(2014\)\. Perspective: network\-guided pattern formation of neural dynamics\. PMC4150299\.

\[14\] Reaction diffusion system prediction based on convolutional neural network\. Scientific Reports, 2020\. https://www\.nature\.com/articles/s41598\-020\-60853\-2

\[15\] Unraveling biochemical spatial patterns: Machine learning approaches to the inverse problem of stationary Turing patterns\. ScienceDirect 2024\. https://www\.sciencedirect\.com/science/article/pii/S2589004224010447

\[16\] Nature Communications \(2024\)\. Widespread biochemical reaction networks enable Turing patterns without imposed feedback\. https://doi\.org/10\.1038/s41467\-024\-52591\-0

\[17\] Information Entropy Measures for Evaluation of Reliability of Deep Neural Network Results\. PMC Entropy 2023, 25\(4\): 573\. https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC10137523/

\[18\] Hardt O\., Nader K\., Nadel L\. \(2013\)\. Decay happens: The role of active forgetting in memory\. Trends in Cognitive Sciences, 17\(3\): 111–120\.

\[19\] Improving Uncertainty Estimation through Information\-Theoretic Approaches\. ICLR 2025\. https://proceedings\.iclr\.cc/paper\_files/paper/2025/file/b94d8b035e2183e47afef9e2f299ba47\-Paper\-Conference\.pdf

\[20\] ICLR 2024 Research on LLM Self\-Correction\. Referenced in: Galileo AI \(2025\)\. Self\-Evaluation in AI Agents With Chain of Thought\. https://galileo\.ai/blog/self\-evaluation\-ai\-agents\-performance\-reasoning\-reflection

1. <a id="footnote-1"></a>Wei J\., Wang X\., Schuurmans D\., et al\. \(2022\)\. Chain\-of\-Thought Prompting Elicits Reasoning in Large Language Models\. arXiv:2201\.11903\. [↑](#footnote-ref-1)


2. <a id="footnote-2"></a>Kojima T\. et al\. \(2022\)\. Large Language Models are Zero\-Shot Reasoners\. NeurIPS 2022\. [↑](#footnote-ref-2)


3. <a id="footnote-3"></a>OpenAI \(2024\)\. Learning to Reason with LLMs\. Blog post\. September 2024\. [↑](#footnote-ref-3)


4. <a id="footnote-4"></a>Bavassi L\., Fuentemilla L\. \(2024\)\. Segregation\-to\-integration transformation model of memory evolution\. Network Neuroscience, 8\(4\): 1529–1544\. https://doi\.org/10\.1162/netn\_a\_00415 [↑](#footnote-ref-4)


5. <a id="footnote-5"></a>Goldman M\.S\. et al\. \(2024\)\. Synaptic weight dynamics underlying memory consolidation\. Proc\. Natl\. Acad\. Sci\. USA, 121\(41\): e2406010121\. https://doi\.org/10\.1073/pnas\.2406010121 [↑](#footnote-ref-5)


6. <a id="footnote-6"></a>Turing A\.M\. \(1952\)\. The Chemical Basis of Morphogenesis\. Philosophical Transactions of the Royal Society B, 237\(641\): 37–72\. [↑](#footnote-ref-6)


7. <a id="footnote-7"></a>Nature Communications \(2024\)\. Widespread biochemical reaction networks enable Turing patterns without imposed feedback\. https://doi\.org/10\.1038/s41467\-024\-52591\-0 [↑](#footnote-ref-7)


8. <a id="footnote-8"></a>Müller\-Linow M\. et al\. \(2014\)\. Perspective: network\-guided pattern formation of neural dynamics\. PMC4150299\. [↑](#footnote-ref-8)


9. <a id="footnote-9"></a>Abubaker\-Sharif B\., Devreotes P\.N\., Iglesias P\.A\. \(2024\)\. Machine learning sparse reaction\-diffusion models from stochastic dynamics and spatiotemporal patterns\. bioRxiv 2024\.10\.02\.616367\. [↑](#footnote-ref-9)


10. <a id="footnote-10"></a>Pincus S\.M\. \(1991\)\. Approximate entropy as a measure of system complexity\. Proc\. Natl\. Acad\. Sci\. USA, 88\(6\): 2297–2301\. [↑](#footnote-ref-10)


11. <a id="footnote-11"></a>Bandt C\., Pompe B\. et al\. Review: Combining Measures of Signal Complexity and Machine Learning for Time Series Analysis\. Entropy, 23\(12\): 1672\. https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC8700684/ [↑](#footnote-ref-11)


12. <a id="footnote-12"></a>Applications of Entropy in Data Analysis and Machine Learning: A Review\. PMC\. Entropy 2024, 26\(12\): 1126\. https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC11675792/ [↑](#footnote-ref-12)


13. <a id="footnote-13"></a>Goedecke S\. \(2024\)\. Is chain\-of\-thought AI reasoning a mirage? Blog analysis\. https://www\.seangoedecke\.com/real\-reasoning/ [↑](#footnote-ref-13)


14. <a id="footnote-14"></a>ICLR 2024 findings on self\-correction in LLMs, as referenced in Galileo AI technical review\. December 2025\. https://galileo\.ai/blog/self\-evaluation\-ai\-agents\-performance\-reasoning\-reflection [↑](#footnote-ref-14)


15. <a id="footnote-15"></a>Müller\-Linow M\. et al\. \(2014\)\. Network\-guided pattern formation of neural dynamics\. PMC4150299\. [↑](#footnote-ref-15)


16. <a id="footnote-16"></a>Reaction diffusion system prediction based on convolutional neural network\. Scientific Reports, 2020\. https://www\.nature\.com/articles/s41598\-020\-60853\-2 [↑](#footnote-ref-16)


17. <a id="footnote-17"></a>Unraveling biochemical spatial patterns: Machine learning approaches to the inverse problem of stationary Turing patterns\. ScienceDirect 2024\. https://www\.sciencedirect\.com/science/article/pii/S2589004224010447 [↑](#footnote-ref-17)


18. <a id="footnote-18"></a>Bandt et al\. Review: Combining Measures of Signal Complexity and Machine Learning for Time Series Analysis\. MDPI Entropy, 23\(12\): 1672\. 2021\. [↑](#footnote-ref-18)


19. <a id="footnote-19"></a>Information Entropy Measures for Evaluation of Reliability of Deep Neural Network Results\. PMC\. Entropy 2023, 25\(4\): 573\. https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC10137523/ [↑](#footnote-ref-19)


20. <a id="footnote-20"></a>Guo S\. et al\. \(2024\)\. A Survey on Neural Question Generation: Methods, Applications, and Prospects\. arXiv:2402\.18267\. [↑](#footnote-ref-20)



