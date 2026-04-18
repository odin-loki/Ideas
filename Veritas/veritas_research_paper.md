<!-- Converted from `veritas_research_paper.docx` — source was Word (.docx). -->

__VERITAS__

*Verification\-Enabled Reasoning and Integrated Theorem\-Acquiring System*

__A Complete Mathematical Framework with Formal Proofs,__

__PAC/ALT Learning Bounds, Meta\-Learning Theory, and Reference Implementation__

Technical Report · March 2026

# __Abstract__

We present VERITAS \(Verification\-Enabled Reasoning and Integrated Theorem\-Acquiring System\), a meta\-learning architecture that operates over binary pattern spaces and provides formal, proof\-backed guarantees on its own learning behaviour at every training step\. Unlike conventional learning systems whose performance bounds are analysed offline, VERITAS continuously verifies that each learning step satisfies the theoretical conditions imposed by PAC and ALT learning frameworks, and composes those guarantees hierarchically through a meta\-learning layer\.

This document establishes the complete mathematical foundation for VERITAS across nine theorems covering metric space completeness, PAC learning bounds, ALT learning bounds, meta\-learning theory, verification completeness, and composition guarantees\. We further describe a distillation regime for ensemble\-to\-student knowledge transfer, and present a complete NumPy reference implementation\. The central result is Theorem 9, which shows that PAC and ALT learning guarantees compose additively through the meta\-learning layer: if the base learner achieves error ε with confidence 1−δ, and the meta\-learner achieves meta\-error ε\_m with confidence 1−δ\_m, then the composed system achieves error ε \+ ε\_m with confidence 1−\(δ \+ δ\_m\)\. The system imposes a superexponential sample complexity cost \(ln|H| = 2^n · ln 2 for hypothesis space H over n\-dimensional binary patterns\) by design, forcing the accumulation of sufficient evidence before any learning step is certified\.

Keywords: PAC Learning, Algorithmic Learning Theory, Meta\-Learning, Online Learning, Mistake Bounds, Binary Hypothesis Spaces, Knowledge Distillation, Formal Verification, Ensemble Methods\.

# __1\. Introduction__

Formal learning theory provides asymptotic and finite\-sample bounds that are almost universally treated as background results: derived once, invoked in a paper's analysis section, and never checked again at runtime\. VERITAS was designed to break this convention\. Its central thesis is that learning bounds should be active constraints, verified at every training step, so that the system can distinguish between learning iterations that provably satisfy convergence criteria and those that do not\.

The PAC \(Probably Approximately Correct\) learning framework, introduced by Valiant \[1\], asks how many labelled examples an algorithm needs to output a hypothesis with low generalisation error and high probability\. The ALT \(Algorithmic Learning Theory\) framework asks how many mistakes an online learner makes before converging, and how many queries suffice for exact identification \[2\]\. Both frameworks rest on clean combinatorial arguments — Hoeffding's inequality \[3\] and the halving argument of Littlestone \[4\] — and both produce bounds whose constants and exponents depend on the size of the hypothesis space\.

For VERITAS the hypothesis space is H = \{h : B → B\}, the set of all Boolean functions from n\-dimensional binary patterns to binary patterns\. This space has cardinality |H| = 2^\(2^n\), which is superexponential in n\. The logarithm of |H| — the key quantity in both PAC and ALT bounds — is ln|H| = 2^n · ln 2, exponential in n\. This choice is deliberate: it imposes a substantial sample\-complexity cost that forces the system to accumulate large amounts of evidence before any step is certified as verified\.

The meta\-learning layer operates one level above H, in the space M = \{m : H → H\} of all hypothesis transformers\. Meta\-learning in the sense of 'learning to learn' has a long history \[5\], and has recently been formalised in gradient\-based frameworks such as MAML \[6\]\. VERITAS takes a different approach: it applies the same PAC and ALT frameworks at the meta\-level, using H as the new instance space and M as the new hypothesis space, and composes the resulting bounds through Theorem 9\.

The verification architecture maintains four nested proof traces at each training step: a PAC proof, an ALT proof, a meta proof, and a composition proof\. Weight updates are applied only when the composition proof verifies\. The distillation module allows an ensemble of teacher VERITAS instances to supervise a student model, with temperature\-scaled KL divergence as the soft\-target objective, following the framework of Hinton, Vinyals, and Dean \[7\]\.

## __1\.1  Contributions__

This work makes the following contributions:

1. A complete mathematical foundation for learning over binary pattern spaces, comprising nine theorems with full proofs\.
2. A runtime verification architecture that constructs and checks PAC, ALT, meta\-learning, and composition proofs at every training step\.
3. A distillation theory for ensemble\-to\-student transfer in binary spaces, with connections to the original Hinton et al\. temperature\-scaling framework\.
4. A complete, self\-contained NumPy reference implementation \(veritas\_core\.py, veritas\_verification\.py, veritas\_distillation\.py, veritas\_integration\.py\) with documented bug fixes relative to an earlier PyTorch prototype\.

## __1\.2  Notation__

The following notation is used consistently throughout this paper\.

__Symbol__

__Meaning__

B = \{0,1\}^n

n\-dimensional binary pattern space

H = \{h : B → B\}

Hypothesis space; |H| = 2^\(2^n\)

M = \{m : H → H\}

Meta\-space; |M| = |H|^|H|

V = \{v : H×M → \{0,1\}\}

Verification space

err\(h\)

True error: P\(h\(x\) ≠ y\)

êrr\(h\)

Empirical error over m labelled samples

ε, δ

PAC accuracy and confidence parameters

M\(L\), Q\(L\)

Mistake bound and query complexity of algorithm L

# __2\. Core Spaces and Metric Structures__

## __2\.1  Foundational Spaces__

VERITAS operates over a probabilistic universe \(Ω, ℱ, P\) where Ω is the sample space of binary patterns, ℱ is a σ\-algebra over Ω, and P is a probability measure on \(Ω, ℱ\)\. Four nested spaces are constructed above this foundation\.

__Definition 2\.1 \(Core Spaces\)\.  __*1\. Binary Pattern Space: B = \{0,1\}^n\. 2\. Hypothesis Space: H = \{h : B → B\}, |H| = 2^\(2^n\)\. 3\. Meta\-Space: M = \{m : H → H\}, |M| = |H|^|H|\. 4\. Verification Space: V = \{v : H × M → \{0,1\}\}\.*

The cardinalities follow from elementary combinatorics\. There are 2^n distinct binary strings of length n, giving |B| = 2^n\. A function B → B is determined by its truth table of 2^n output bits, giving |H| = 2^\(2^n\)\. A meta\-function H → H is determined by its image on each element of H, giving |M| = |H|^|H| = 2^\(2^n · 2^\(2^n\)\)\. These superexponential sizes are not curiosities — they directly determine sample complexity \(Theorem 3\) and mistake bounds \(Theorem 4\), and have concrete runtime consequences for the number of steps required before verification succeeds\.

## __2\.2  Canonical Metrics__

__Definition 2\.2 \(Canonical Metrics\)\.  __*d\_B\(x, y\) = Σ|x\_i − y\_i|  \(Hamming distance on B\)  d\_H\(h₁, h₂\) = sup\{ d\_B\(h₁\(x\), h₂\(x\)\) | x ∈ B \}  d\_M\(m₁, m₂\) = sup\{ d\_H\(m₁\(h\), m₂\(h\)\) | h ∈ H \}  d\_V\(v₁, v₂\) = P\(v₁ ≠ v₂\)*

The Hamming metric on B counts differing bit positions\. The hypothesis metric d\_H is an L∞\-type lifting: two hypotheses are close if they agree on every input pattern up to a small Hamming tolerance\. The meta\-metric repeats this lifting one level higher\. The verification metric is a probability metric over the product space H × M\.

## __2\.3  Completeness \(Theorem 1\)__

__Theorem 1 \(Completeness\)\.  __*Each metric space \(B, d\_B\), \(H, d\_H\), \(M, d\_M\), and \(V, d\_V\) is a complete metric space\.*

*Proof\.  *\(B, d\_B\): B is finite for any fixed n\. Every Cauchy sequence in a finite metric space is eventually constant and therefore convergent\. \(H, d\_H\): Let \{h\_k\} be a Cauchy sequence in H\. For any ε > 0, there exists K such that for all j, k ≥ K, d\_H\(h\_j, h\_k\) < ε\. By definition of d\_H, for every x ∈ B the sequence \{h\_k\(x\)\} is Cauchy in the complete space B, and hence converges to some h\*\(x\) ∈ B\. The function h\* ∈ H satisfies d\_H\(h\_k, h\*\) < ε for all k ≥ K\. \(M, d\_M\): The argument mirrors the H case, replacing B with H\. \(V, d\_V\): The probability metric inherits completeness from the underlying probability space \(Ω, ℱ, P\)\. ∎

Completeness is foundational because it guarantees that iterative learning algorithms — which produce Cauchy sequences of hypotheses by successive refinement — converge to well\-defined limits inside the space\. Without completeness, a sequence of approximate hypotheses could converge toward a function outside H, making the learning target unreachable\.

# __3\. PAC Learning Framework__

## __3\.1  Overview__

Probably Approximately Correct \(PAC\) learning, introduced by Valiant \[1\] in 1984, provides a rigorous framework for analysing sample complexity\. A learner receives m random examples \{\(x\_i, c\(x\_i\)\)\} drawn i\.i\.d\. from distribution P, where c ∈ H is an unknown target concept\. The learner must output a hypothesis h ∈ H whose true error err\(h\) = P\(h\(x\) ≠ c\(x\)\) is at most ε with probability at least 1−δ over the random draw of training data\. The two parameters ε ∈ \(0,1\) and δ ∈ \(0,1\) respectively quantify accuracy and confidence\.

The central challenge is the generalisation gap: empirical error on training data systematically underestimates true error when the sample is small\. PAC theory quantifies this gap precisely using Hoeffding's inequality \[3\], which bounds the probability that a sample mean deviates from its expectation\.

## __3\.2  PAC Bound \(Theorem 2\)__

__Theorem 2 \(PAC Learning in Binary Space\)\.  __*For any h ∈ H, with probability at least 1−δ over a sample of size m: |err\(h\) − êrr\(h\)| ≤ ε,  provided  m ≥ \(1/2ε²\) ln\(2/δ\)\.*

*Proof\.  *Fix h ∈ H\. Define Z\_i = 1\[h\(x\_i\) ≠ y\_i\] for i = 1, \.\.\., m drawn i\.i\.d\. from P\. Each Z\_i ∈ \[0,1\] with E\[Z\_i\] = err\(h\) and êrr\(h\) = \(1/m\)Σ Z\_i\. By Hoeffding's inequality for bounded i\.i\.d\. random variables: P\(|êrr\(h\) − err\(h\)| > ε\) ≤ 2 exp\(−2mε²\)\. Setting 2 exp\(−2mε²\) = δ and solving for m yields m ≥ \(1/2ε²\) ln\(2/δ\)\. ∎

## __3\.3  Sample Complexity Over H \(Theorem 3\)__

Theorem 2 controls the deviation for a single fixed hypothesis h\. When the learner selects h from H after seeing the data, the guarantee must hold simultaneously for all h ∈ H\. This requires a union bound over the class, adding a factor of ln|H| to the sample requirement\.

__Theorem 3 \(Sample Complexity\)\.  __*For the binary hypothesis space H with |H| = 2^\(2^n\): m ≥ \(1/ε²\)\(ln|H| \+ ln\(1/δ\)\),  where  ln|H| = 2^n · ln 2\.*

*Proof\.  *Applying a union bound over all h ∈ H to Theorem 2: P\(∃h ∈ H : |êrr\(h\) − err\(h\)| > ε\) ≤ |H| · 2 exp\(−2mε²\)\. Setting this equal to δ and solving gives m ≥ \(1/2ε²\)\(ln 2 \+ ln|H| \+ ln\(1/δ\)\)\. Absorbing the ln 2 constant into the leading factor \(standard in PAC literature\) and substituting ln|H| = 2^n · ln 2 yields the stated bound\. ∎

For the default dimension n = 8, ln|H| ≈ 177,000\. With ε = δ = 0\.01, the required sample count is approximately 1\.8 million\. This reflects the extraordinary richness of B → B and explains why PAC verification at small dimensions requires either very large datasets or relaxed parameters\. If the learner is restricted to a subclass H' ⊂ H, the bound improves to ln|H'|; subclass selection is one practical strategy for making PAC verification achievable\.

## __3\.4  Practical Implications__

The exponential sample complexity has two concrete runtime consequences\. First, for any realistic training run on small binary patterns, the PAC step of the proof trace will return False until sufficient examples have accumulated — this is expected and correct behaviour\. Second, the bound is tight in the worst case over the full hypothesis class; any algorithm must inspect at least Ω\(\(1/ε²\)\(ln|H| \+ ln\(1/δ\)\)\) examples to guarantee ε\-accuracy with probability 1−δ\. The code correctly implements Theorem 3's ln|H| = 2^n · ln 2 formula, fixing a prior bug in which the formula was ln|H| = n · ln 2 \(dimension times log two, rather than 2\-to\-the\-n times log two\)\.

# __4\. ALT Learning Framework__

## __4\.1  Overview__

Algorithmic Learning Theory \(ALT\) approaches learnability through worst\-case combinatorial analysis rather than probabilistic sample complexity\. Two central quantities characterise a learning algorithm L on hypothesis class H: the mistake bound M\(L\) — the maximum number of incorrect predictions before convergence, over all target concepts and all presentation orderings — and the query complexity Q\(L\) — the minimum number of membership queries needed to exactly identify any target in a single identification round\.

Both quantities are determined by the size of the version space: the set of hypotheses in H consistent with all examples seen so far\. Each mistake or query provides information that shrinks the version space, and both bounds follow from the rate of this shrinkage\.

## __4\.2  Mistake Bound \(Theorem 4\)__

The foundational result in mistake\-bounded learning is the Halving Algorithm, due to Littlestone \[4\]\. On each trial, the Halving Algorithm predicts the majority vote over the current version space\. Every mistake eliminates at least half the remaining candidates, yielding a logarithmic bound\.

__Theorem 4 \(Mistake Bound\)\.  __*For any learning algorithm L on H: M\(L\) ≤ lg|H| = 2^n, where |H| = 2^\(2^n\) and lg denotes log base 2\.*

*Proof\.  *Let V\_t denote the version space after t examples, with V\_0 = H\. On any trial where the algorithm makes a mistake, at least half the remaining consistent hypotheses are eliminated \(Littlestone \[4\], Theorem 2\)\. Formally: |V\_\{t\+1\}| ≤ |V\_t| / 2\. Starting from |V\_0| = |H|, after M mistakes we have |V\_M| ≤ |H| / 2^M\. Since |V\_M| ≥ 1 \(the target concept remains consistent\), 2^M ≤ |H| and hence M ≤ lg|H|\. Substituting |H| = 2^\(2^n\) gives M ≤ lg\(2^\(2^n\)\) = 2^n\. ∎

## __4\.3  Query Complexity \(Theorem 5\)__

In the active learning model, the learner may choose which patterns to query rather than receiving random examples\. This is the model of Angluin \[8\], who showed that membership queries can exponentially reduce the number of examples required for exact identification\.

__Theorem 5 \(Query Complexity\)\.  __*For exact identification of any target in H: Q\(L\) ≤ n, where Q\(L\) is the number of membership queries required per identification round\.*

*Proof\.  *A membership query asks 'Is x labelled 1 by target c?' and receives a single bit\. The target pattern x\* ∈ B is an n\-bit string\. Querying each canonical basis pattern e\_i = \(0,\.\.\.,0,1,0,\.\.\.,0\) \(the i\-th standard basis vector for i = 1,\.\.\.,n\) reveals c\(e\_i\) ∈ \{0,1\}, recovering one bit of the truth table per query\. After n queries the full labelling of B is determined\. Hence Q\(L\) ≤ n\. The bound is information\-theoretically tight: the target is one of |B| = 2^n patterns, requiring at least n bits, and each query yields exactly one bit\. ∎

## __4\.4  Relationship Between Bounds and Runtime Tracking__

The mistake bound and query complexity are complementary, not comparable\. Mistake bounds apply to online adversarial learning where the presentation sequence is chosen by nature; query bounds apply to active learning where the learner selects queries\. In VERITAS, both are tracked simultaneously\. The mistake counter increments when the rule network's prediction error exceeds ε; the query counter increments on every forward pass\. The ALT proof verifier checks mistakes ≤ 2^n and \(per\-round\) queries ≤ n\.

The query bound Q ≤ n is a per\-round quantity governing a single exact\-identification episode, not a cumulative budget\. The implementation correctly distinguishes these semantics: cumulative query count will exceed n after the first n training steps, but per\-round verification uses the round\-local count\.

# __5\. Meta\-Learning Theory__

## __5\.1  Motivation and Architecture__

The meta\-learning layer of VERITAS operates over the hypothesis space H, not over the pattern space B\. Its purpose is to learn a transformation m : H → H that maps base hypotheses to improved hypotheses — learning how to learn, in the sense of Thrun and Pratt \[5\]\. In the implementation, hypotheses are encoded as flattened parameter vectors of the rule network, so m operates on parameter\-space representations of functions\.

This is a second\-order optimisation problem\. Rather than minimising error on B, the meta\-learner minimises error on H\. Standard PAC and ALT frameworks must be reinterpreted: H is now the instance space and M is the hypothesis class\. Because M has cardinality |H|^|H| — doubly exponential in n — the meta\-level bounds are orders of magnitude larger than the base\-level bounds, but they remain finite and mathematically well\-posed\.

This approach connects to MAML \[6\] and related gradient\-based meta\-learning frameworks \[5\], with the key distinction that VERITAS derives explicit combinatorial bounds from the structure of M rather than relying on gradient\-based fine\-tuning\. The meta\-network in the implementation is a two\-layer MLP operating on rule\-network parameter vectors, with theorem discovery triggered when binary\-thresholded meta\-outputs satisfy both PAC and ALT proof traces simultaneously\.

## __5\.2  Meta\-PAC Bounds \(Theorem 6\)__

__Theorem 6 \(Meta\-Learning PAC Bound\)\.  __*For any meta\-learner m ∈ M, with probability at least 1−δ\_m: |err\_m\(m\) − êrr\_m\(m\)| ≤ ε\_m, where err\_m\(m\) is the true meta\-error and êrr\_m\(m\) is the empirical meta\-error\.*

*Proof\.  *Apply the PAC framework of Theorem 2 to the meta\-space: instance space H, hypothesis class M, error function err\_m\. Meta\-errors are bounded in \[0,1\], so Hoeffding's inequality applies\. The required number of meta\-examples for the uniform bound to hold is m\_M ≥ \(1/ε\_m²\)\(ln|M| \+ ln\(1/δ\_m\)\)\. Since |M| = |H|^|H| = 2^\(2^n · 2^\(2^n\)\), the meta\-sample complexity is doubly exponential in n, but finite for any fixed n\. In practice the parametric restriction of M to the meta\-network's parameter space gives a far smaller effective size\. ∎

## __5\.3  Meta\-ALT Bound \(Theorem 7\)__

__Theorem 7 \(Meta\-Learning Mistake Bound\)\.  __*For any meta\-learning algorithm operating on M: M\(m\) ≤ lg|M| = 2^n · 2^\(2^n\)\.*

*Proof\.  *Apply the halving argument of Theorem 4 to the meta\-version space with size |M| = |H|^|H|\. Each mistake halves the meta\-version space: |V\_\{t\+1\}^M| ≤ |V\_t^M| / 2\. Starting from |V\_0^M| = |M| and noting |V\_M^M| ≥ 1, we obtain M\(m\) ≤ lg|M|\. Substituting |M| = 2^\(2^n · 2^\(2^n\)\) gives lg|M| = 2^n · 2^\(2^n\)\. ∎

This bound is doubly exponential and is best understood as a theoretical ceiling over the full meta\-space\. For practical systems where the meta\-learner is restricted to a parametric subspace \(as in VERITAS\), the effective bound is determined by the VC dimension or Rademacher complexity of that subspace, which scales polynomially in the number of network parameters\.

# __6\. Verification Theory__

## __6\.1  Architecture__

The verification layer distinguishes VERITAS from a conventional learning system\. At each training step, the system constructs four sequential proofs: a PAC proof \(Theorems 2 and 3\), an ALT proof \(Theorems 4 and 5\), a meta proof \(Theorem 6\), and a composition proof \(Theorem 9\)\. Weight updates are applied only when the composition proof verifies\. This creates a feedback loop where learning is conditioned on provable progress\.

Each proof is represented as a TheoremProof dataclass containing a list of ProofStep objects\. Each ProofStep records its statement, justification, assumptions, conclusion \(a boolean\), and a verification trace \(a list of boolean sub\-checks\)\. A proof is verified if and only if all its steps conclude True\. A VerificationTrace aggregates the four proofs, computes per\-type step\-pass\-rates, and assigns an overall confidence equal to the fraction of proofs that fully verify\.

## __6\.2  Verification Completeness \(Theorem 8\)__

__Theorem 8 \(Verification Completeness\)\.  __*For verifier v ∈ V: v is complete ⟺ ∀h, m: v\(h, m\) = 1 ⟹ all required properties hold\.*

*Proof\.  *The verifier v is the conjunction v\(h, m\) = ⋀\_\{i=1\}^k P\_i\(h, m\) of decidable property predicates P\_1, \.\.\., P\_k \(PAC error bound, ALT mistake bound, ALT query bound, meta\-error bound, composition validity\)\. Soundness: if v = 1 then each P\_i = 1 and each property holds\. Completeness: if all P\_i = 1 then v = 1\. The predicates are computable from observable statistics \(empirical error, sample count, mistake count, query count\), so v is effectively decidable\. ∎

## __6\.3  Learning Composition \(Theorem 9\)__

The deepest result in the framework is the composition theorem\. It establishes that PAC and ALT guarantees compose additively through the meta\-learning layer, providing the theoretical underpinning for why verifying the base learner and the meta\-learner separately is sufficient to certify the end\-to\-end system\.

__Theorem 9 \(Learning Composition\)\.  __*For h ∈ H, m ∈ M: if P\(err\(h\) > ε\) ≤ δ  and  P\(err\_m\(m\) > ε\_m\) ≤ δ\_m, then  P\(err\(m ∘ h\) > ε \+ ε\_m\) ≤ δ \+ δ\_m\.*

*Proof\.  *Let A = \{err\(h\) > ε\} and B = \{err\_m\(m\) > ε\_m\}, with P\(A\) ≤ δ and P\(B\) ≤ δ\_m\. Step 1 \(Triangle inequality\): For any x, err\(m ∘ h\)\(x\) ≤ err\(h\)\(x\) \+ err\_m\(m\)\(h\(x\)\)\. Taking expectations: err\(m ∘ h\) ≤ err\(h\) \+ err\_m\(m\)\. Therefore on the event A^c ∩ B^c \(neither error bound violated\), err\(m ∘ h\) ≤ ε \+ ε\_m\. Step 2 \(Union bound\): The event \{err\(m ∘ h\) > ε \+ ε\_m\} ⊆ A ∪ B\. By the union bound: P\(err\(m ∘ h\) > ε \+ ε\_m\) ≤ P\(A ∪ B\) ≤ P\(A\) \+ P\(B\) ≤ δ \+ δ\_m\. ∎

The additive error and additive failure probability mean that if the base learner and meta\-learner are each well\-calibrated, the composed system degrades gracefully\. In particular, setting ε = ε\_m = ε\_total/2 and δ = δ\_m = δ\_total/2 achieves the target \(ε\_total, δ\_total\) guarantee at the composition level\.

## __6\.4  Proof Trace Structure and Convergence Conditions__

For the composition proof to verify, all of the following conditions must hold simultaneously at a given training step:

- PAC sample condition: n\_samples ≥ \(1/ε²\)\(2^n ln 2 \+ ln\(1/δ\)\)
- PAC error condition: empirical\_error ≤ ε \+ √\(ln\(2/δ\) / \(2m\)\)
- ALT mistake condition: cumulative\_mistakes ≤ 2^n
- ALT query condition \(per round\): queries\_this\_round ≤ n
- Meta condition: meta\_error ≤ 2ε \(composition triangle inequality\)
- Composition: both PAC and ALT proofs verified \(Theorem 9 applies\)

The PAC sample complexity condition is typically the binding constraint for small n, because the required sample count grows as 2^n\. Once sufficient data has been accumulated, the other conditions are satisfied within their bounds in the vast majority of cases\. Early in training the proof trace will show False across most steps; this is correct and expected behaviour — the system is reporting that insufficient evidence exists to certify learning\.

# __7\. Distillation and Ensemble Theory__

## __7\.1  Knowledge Distillation in Binary Spaces__

VERITAS supports an ensemble distillation training regime inspired by the framework of Hinton, Vinyals, and Dean \[7\]\. An ensemble of T teacher VERITAS instances — each independently trained — supervises the training of a smaller student model\. The student learns to match both the rule\-network outputs and the meta\-network outputs of the ensemble, using temperature\-scaled KL divergence as the soft\-target objective and MSE as the hard\-target objective\.

Temperature scaling follows the prescription of \[7\]: the teacher's output is passed through a softmax at temperature T\_τ > 1 to produce a softer probability distribution over patterns, providing richer gradient signal in regions where the teacher is uncertain\. The student is trained with the same temperature T\_τ during distillation\. After training, T\_τ is set to 1\. As Hinton et al\. prove, the T\_τ² factor in the gradient magnitude must be accounted for when combining soft\-target and hard\-target loss terms to maintain correct relative weighting\.

The theoretical basis for distillation in the PAC framework follows from Jensen's inequality applied to the squared error\. Let h\_θ denote the student hypothesis and h\_T = \(1/T\)Σ\_t h\_t the ensemble average\. Then:

*err\(h\_θ\) ≤ \(1 − α\) · D\_KL\(h\_θ || h\_T\) \+ α · êrr\(h\_θ\)*

where α ∈ \[0,1\] is the balance parameter and D\_KL is the temperature\-scaled KL divergence\. This bound shows that minimising the distillation objective controls the true error of the student through a combination of ensemble alignment and empirical accuracy\.

## __7\.2  Ensemble Variance Reduction__

The ensemble output h\_T = \(1/T\)Σ\_t h\_t is the arithmetic mean of T teacher rule\-network outputs\. By the law of large numbers, as T → ∞ the ensemble mean converges to the expected hypothesis under the distribution over teacher initialisations\. For finite T, the variance of the ensemble error is reduced by a factor of T relative to any single teacher:

*Var\[êrr\_T\] = \(1/T\) · Var\[êrr\]*

This variance reduction is the principal benefit of ensemble distillation: the student learns from a lower\-variance target, which translates into a tighter generalisation bound through the Hoeffding inequality\. Specifically, replacing individual teacher error with ensemble error in Theorem 3 reduces the effective noise term by √T\.

## __7\.3  Implementation__

The VERITASDistiller class initialises an ensemble of VERITAS teacher instances and a student VERITAS instance\. At each training step, it computes the ensemble rule\-network and meta\-network outputs by averaging over teachers, computes the distillation loss as a weighted combination of KL divergence \(soft\) and MSE \(hard\) components, and performs an SGD step on the student's rule network\. The teacher models are frozen — only the student is updated\. The distillation loss function correctly applies the T² gradient scaling required by the Hinton et al\. framework\.

# __8\. Reference Implementation__

## __8\.1  Architecture Overview__

The NumPy reference implementation consists of four modules\. veritas\_core\.py provides the core mathematical machinery: BinarySpace, PACLearner, ALTLearner, MetaLearner, RuleNetwork, MetaNetwork, and the top\-level VERITAS class\. veritas\_verification\.py provides the proof construction and verification system: ProofVerifier, VerifiedLearningSystem, and the associated dataclasses\. veritas\_distillation\.py provides the ensemble distillation system: VERITASDistiller and DistillationConfig\. veritas\_integration\.py ties everything together in IntegratedVERITAS with end\-to\-end verified training\.

All neural components are implemented from scratch using NumPy, without PyTorch or any autograd framework\. The MLP class implements a two\-layer fully\-connected network with He initialisation, ReLU activations, and manual forward/backward passes\. The sgd\_step method applies stochastic gradient descent directly to parameter arrays\. This makes the implementation fully inspectable and eliminates hidden abstractions\.

## __8\.2  Bug Fixes Relative to Prior Implementation__

Three significant bugs were identified and corrected relative to the earlier PyTorch prototype:

__Module__

__Bug__

__Fix__

veritas\_core\.py

Sample complexity used ln|H| = n·ln2 \(dimension times ln2\)

Corrected to ln|H| = 2^n·ln2, consistent with Theorem 3 and |H| = 2^\(2^n\)

veritas\_core\.py

log\(0\) division error in ALTLearner\.computation\_bound when dimension = 1

Guard added: log\(max\(dimension, 2\)\) ensures domain safety

veritas\_verification\.py

Meta error bound compared float against 2\*bool \(2\*True=2, 2\*False=0\), giving nonsensical results

Fixed to compare against computed float epsilon\_meta = 2\.0 \* base\_epsilon extracted from PAC proof assumptions

Additional fixes included: replacing gradient\-free parameter mutation in \_update\_networks with a proper SGD backward\-forward cycle; replacing the torch DataLoader with a NumPy batch iterator in VERITASDistiller\.train; replacing min\(\) over boolean proof\-step fields with meaningful float pass\-rate aggregation in create\_verification\_trace; and adding missing imports \(from typing import Any in veritas\_integration\.py\)\.

## __8\.3  Summary of Theorems__

__Thm\.__

__Name__

__Space__

__Key Result__

1

Completeness

B, H, M, V

All four spaces are complete metric spaces

2

PAC Bound

H

|err − êrr| ≤ ε w\.p\. 1−δ given m ≥ \(1/2ε²\)ln\(2/δ\)

3

Sample Complexity

H

m ≥ \(1/ε²\)\(2^n ln2 \+ ln\(1/δ\)\)

4

Mistake Bound

H

M\(L\) ≤ lg|H| = 2^n

5

Query Complexity

H

Q\(L\) ≤ n queries per identification round

6

Meta\-PAC

M

PAC bound lifts to meta\-space: |err\_m − êrr\_m| ≤ ε\_m

7

Meta\-ALT

M

M\(m\) ≤ lg|M| = 2^n · 2^\(2^n\)

8

Verification Completeness

V

v\(h,m\) = 1 ⟺ all checked properties hold

9

Composition

H × M

err\(m∘h\) ≤ ε \+ ε\_m w\.p\. ≥ 1 − \(δ \+ δ\_m\)

# __9\. Discussion__

## __9\.1  Relationship to Existing Work__

VERITAS occupies an unusual position in the learning theory landscape\. PAC learning theory since Valiant \[1\] has been primarily concerned with efficient learnability \(polynomial sample and time complexity\), and the binary function class B → B is well\-known to be not efficiently PAC learnable under cryptographic hardness assumptions \[9\]\. The super\-polynomial sample complexity of Theorem 3 is therefore expected\.

The ALT mistake\-bound framework connects to Littlestone's work \[4\] on the halving algorithm and its relationship to VC dimension\. The query complexity bound of Theorem 5 connects to Angluin's \[8\] membership query model\. The composition theorem \(Theorem 9\) is a specialisation of standard union\-bound and triangle\-inequality arguments, but its instantiation at the meta\-learning level — where the 'learner' is itself a learning algorithm — is non\-standard\.

The meta\-learning component connects conceptually to MAML \[6\] and related gradient\-based frameworks, but differs in that VERITAS derives explicit combinatorial bounds from the structure of M rather than relying on gradient sensitivity\. The distillation component directly implements the Hinton\-Vinyals\-Dean \[7\] temperature\-scaling framework, with the T² gradient correction and the weighted combination of soft\-target KL divergence and hard\-target MSE losses\.

## __9\.2  Practical Interpretation of Non\-Verification__

A frequent misinterpretation of verification\-conditioned learning is that training steps with failed proofs are wasted\. This is incorrect\. When the composition proof fails, it is because the learning bounds have not been satisfied — the system genuinely does not have sufficient evidence to certify the step\. Non\-verified steps still contribute to the accumulation of evidence \(incrementing sample counts\), and they provide diagnostic information about which bounds are currently violated\. In particular, the confidence output of each VerificationTrace \(fraction of four proofs that fully verify\) provides a continuous signal tracking progress toward full certification\.

The PAC sample complexity condition is almost always the first to bind for small binary dimensions\. The ALT mistake and query conditions are usually satisfied early in training, since the mistake bound 2^n is large relative to actual mistake counts for well\-initialised networks\. The meta\-error condition requires that the meta\-network's RMS output magnitude stays below 2ε, which is a mild constraint on representational magnitude rather than a learning accuracy constraint per se\.

## __9\.3  Limitations and Extensions__

Several limitations of the current framework are worth noting\. First, the hypothesis class B → B is extremely large and not efficiently PAC learnable, which means full PAC verification will require unrealistically large datasets for any non\-trivial dimension\. For defence and intelligence applications with restricted function subclasses, the effective complexity is much smaller and the bounds tighten accordingly\.

Second, the current composition theorem \(Theorem 9\) is linear in errors and probabilities\. Tighter composition results using information\-theoretic tools \(e\.g\., mutual information bounds or chaining arguments from Talagrand's generic chaining \[10\]\) could reduce the composed error to O\(max\(ε, ε\_m\)\) under additional assumptions\. This is a natural direction for future work\.

Third, the meta\-network is currently parameterised as a fixed\-architecture two\-layer MLP, which is a parametric restriction of M\. A principled treatment of the effective meta\-complexity — using, for instance, the PAC\-Bayes framework or the Rademacher complexity of the meta\-network's function class — would provide sharper meta\-level bounds than the combinatorial bound of Theorem 7\.

# __References__

\[1\]  Valiant, L\.G\. \(1984\)\. A theory of the learnable\. Communications of the ACM, 27\(11\), 1134–1142\. https://doi\.org/10\.1145/1968\.1972

\[2\]  Kearns, M\.J\., and Vazirani, U\.V\. \(1994\)\. An Introduction to Computational Learning Theory\. MIT Press\.

\[3\]  Hoeffding, W\. \(1963\)\. Probability inequalities for sums of bounded random variables\. Journal of the American Statistical Association, 58\(301\), 13–30\.

\[4\]  Littlestone, N\. \(1988\)\. Learning quickly when irrelevant attributes abound: A new linear\-threshold algorithm\. Machine Learning, 2\(4\), 285–318\. https://doi\.org/10\.1007/BF00116827

\[5\]  Thrun, S\., and Pratt, L\. \(1998\)\. Learning to learn\. Springer Science & Business Media\.

\[6\]  Finn, C\., Abbeel, P\., and Levine, S\. \(2017\)\. Model\-agnostic meta\-learning for fast adaptation of deep networks\. Proceedings of the 34th International Conference on Machine Learning \(ICML 2017\), PMLR 70, 1126–1135\. https://arxiv\.org/abs/1703\.03400

\[7\]  Hinton, G\., Vinyals, O\., and Dean, J\. \(2015\)\. Distilling the knowledge in a neural network\. arXiv preprint arXiv:1503\.02531\. https://arxiv\.org/abs/1503\.02531

\[8\]  Angluin, D\. \(1988\)\. Queries and concept learning\. Machine Learning, 2\(4\), 319–342\.

\[9\]  Kearns, M\.J\., and Valiant, L\.G\. \(1994\)\. Cryptographic limitations on learning Boolean formulae and finite automata\. Journal of the ACM, 41\(1\), 67–95\.

\[10\] Talagrand, M\. \(2014\)\. Upper and Lower Bounds for Stochastic Processes\. Springer\.

\[11\] Blumer, A\., Ehrenfeucht, A\., Haussler, D\., and Warmuth, M\.K\. \(1989\)\. Learnability and the Vapnik\-Chervonenkis dimension\. Journal of the ACM, 36\(4\), 929–965\.

\[12\] Shalev\-Shwartz, S\., and Ben\-David, S\. \(2014\)\. Understanding Machine Learning: From Theory to Algorithms\. Cambridge University Press\.

