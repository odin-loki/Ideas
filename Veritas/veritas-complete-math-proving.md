<!-- Converted from `veritas-complete-math-proving.docx` — source was Word (.docx). -->

__VERITAS__

Complete Mathematical Foundation

*Verification\-Enabled Reasoning and Integrated Theorem\-Acquiring System*

# __1\.  Introduction__

VERITAS \(Verification\-Enabled Reasoning and Integrated Theorem\-Acquiring System\) is a meta\-learning architecture that operates over binary pattern spaces and provides formal, proof\-backed guarantees on its own learning behaviour\. Unlike conventional learning systems whose performance bounds are analysed offline, VERITAS continuously verifies that each learning step satisfies the theoretical conditions imposed by PAC and ALT learning frameworks, and composes those guarantees hierarchically through a meta\-learning layer\.

This document establishes the complete mathematical foundation for VERITAS\. It covers the core metric spaces in which learning takes place, the PAC and ALT learning bounds that govern convergence, the meta\-learning framework that operates over hypothesis spaces, and the verification and composition theory that ties everything together\. Every theorem is accompanied by a full proof and a discussion of its practical implications for the system\.

## __1\.1  Scope and Motivation__

Formal learning theory provides bounds that are often treated as background results, invoked without being verified at runtime\. The central motivation of VERITAS is to make those bounds *active* — checked at every training step — so that the system can distinguish between learning steps that provably satisfy convergence criteria and those that do not\. This imposes a substantial sample\-complexity cost \(the binary hypothesis space |H| = 2^\{2^n\} is superexponential in n\), which is by design: it forces the system to accumulate sufficient evidence before claiming a step is verified\.

The mathematical framework is structured around four nested spaces: a binary pattern space B, a hypothesis space H over B, a meta\-space M over H, and a verification space V that assigns truth values to pairs \(h, m\)\. Learning is defined at each level, and bounds compose from the base level upward through Theorem 9\.

## __1\.2  Notation__

The following notation is used consistently throughout this document\.

- B = \{0,1\}^n — the n\-dimensional binary pattern space
- H = \{h : B → B\} — the hypothesis space; |H| = 2^\{2^n\}
- M = \{m : H → H\} — the meta\-space; |M| = |H|^\{|H|\}
- V = \{v : H × M → \{0,1\}\} — the verification space
- err\(h\) = P\(h\(x\) ≠ y\) — true error of hypothesis h
- êrr\(h\) = \(1/m\)Σ 1\[h\(x\_i\) ≠ y\_i\] — empirical error over m samples
- ε — accuracy parameter \(PAC\); δ — confidence parameter \(PAC\)
- M\(L\) — mistake bound of learning algorithm L
- Q\(L\) — query complexity of learning algorithm L

# __2\.  Core Spaces and Properties__

## __2\.1  Foundational Spaces__

The probabilistic universe in which VERITAS operates is a triple \(Ω, ℱ, P\) where:

- Ω is the sample space of binary patterns
- ℱ is a σ\-algebra over Ω
- P is a probability measure on \(Ω, ℱ\)

Four spaces are built over this foundation\. The binary pattern space is the arena of individual computations\. The hypothesis space captures all possible input\-output mappings over patterns\. The meta\-space captures all possible transformations of hypotheses — it is the space in which the meta\-learner reasons\. The verification space captures decision functions that judge whether a given hypothesis\-meta\-learner pair satisfies the required properties\.

__Definition 2\.1 \(Core Spaces\)__

*1\. Binary Pattern Space:   B = \{0,1\}^n
2\. Hypothesis Space:        H = \{h : B → B\}
3\. Meta\-Space:              M = \{m : H → H\}
4\. Verification Space:      V = \{v : H × M → \{0,1\}\}*

The cardinalities are determined by standard combinatorics\. There are 2^n distinct binary strings of length n, so |B| = 2^n\. A function from B to B is a truth table of 2^n bits, giving |H| = 2^\{2^n\}\. A function from H to H is determined by its image on each of the |H| elements of H, so |M| = |H|^\{|H|\} = 2^\{2^n · 2^\{2^n\}\}\. These superexponential sizes are not merely a curiosity; they determine the sample complexity via Theorem 3 and the mistake bound via Theorem 4, and have direct consequences for the number of learning steps required before verification succeeds\.

## __2\.2  Metric Structures__

Each space carries a natural metric\. These metrics make it possible to state what it means for a sequence of hypotheses to converge, and to prove completeness — which in turn justifies the iterative approach taken by the learning algorithms\.

__Definition 2\.2 \(Canonical Metrics\)__

*d\_B\(x, y\)   = Σ|x\_i − y\_i|   \(Hamming distance on B\)
d\_H\(h₁, h₂\) = sup\{ d\_B\(h₁\(x\), h₂\(x\)\) | x ∈ B \}
d\_M\(m₁, m₂\) = sup\{ d\_H\(m₁\(h\), m₂\(h\)\) | h ∈ H \}
d\_V\(v₁, v₂\) = P\(v₁ ≠ v₂\)*

The Hamming distance on B counts the number of bit positions at which two patterns differ; it is the natural and canonical metric on binary strings\. The hypothesis metric lifts this to the supremum over all inputs, making it an *L∞*\-type metric on function spaces\. The meta\-metric repeats the same lifting one level higher\. The verification metric is a probability metric: two verifiers are close if they disagree on only a small\-measure subset of hypothesis/meta\-learner pairs\.

### __Theorem 1: Completeness__

Completeness is foundational\. It guarantees that iterative learning algorithms — which produce Cauchy sequences of hypotheses by successively refining their estimates — converge to a well\-defined limit inside the space\. Without completeness, a sequence could converge to something outside the space, making the learning target unreachable\.

__Theorem 1 \(Completeness\)__

*Each metric space \(B, d\_B\), \(H, d\_H\), \(M, d\_M\), and \(V, d\_V\) is complete\.*

Proof\.__\(B, d\_B\):__ B is a finite set for any fixed n\. Every Cauchy sequence in a finite metric space is eventually constant, and therefore convergent\. Hence \(B, d\_B\) is complete\.

__\(H, d\_H\):__ Let \{h\_k\} be a Cauchy sequence in H with respect to d\_H\. For any ε > 0, there exists K such that for all j, k ≥ K, d\_H\(h\_j, h\_k\) < ε\. By definition of d\_H, this means that for every x ∈ B, d\_B\(h\_j\(x\), h\_k\(x\)\) < ε\. Since B is complete, the pointwise sequence \{h\_k\(x\)\} converges for each x to some h\*\(x\) ∈ B\. The function h\* : B → B is a well\-defined element of H\. Moreover, for any ε > 0, choosing K as above ensures that for all k ≥ K and all x ∈ B, d\_B\(h\_k\(x\), h\*\(x\)\) < ε, so d\_H\(h\_k, h\*\) < ε\. Therefore h\_k → h\* in H and \(H, d\_H\) is complete\.

__\(M, d\_M\):__ The proof mirrors the argument for H, replacing B with H and h with m\. Since H is complete \(just proved\), the same pointwise convergence argument applies to give completeness of M\.

__\(V, d\_V\):__ The verification metric is a probability metric on indicator functions over the product space H × M, which inherits the completeness of the underlying probability space \(Ω, ℱ, P\)\. Verification functions are bounded \(taking values in \{0,1\}\), so a Cauchy sequence of verifiers converges pointwise P\-almost everywhere to a limit verifier in V\.

□

An important corollary is that the learning problem is well\-posed: the class of achievable hypotheses is exactly H, and iterative refinement will not escape the space\.

# __3\.  PAC Learning Framework__

## __3\.1  Overview__

Probably Approximately Correct \(PAC\) learning, introduced by Valiant \(1984\), provides a framework for asking: how many labelled examples does an algorithm need in order to output a hypothesis that is close to correct, with high probability? The two parameters ε and δ formalise this: the hypothesis is ε\-accurate \(error at most ε\) with probability at least 1−δ\.

In the binary setting of VERITAS, learning takes place in the space H = \{h : B → B\}\. A target concept c ∈ H labels each pattern; the learner receives m random examples \(x\_i, c\(x\_i\)\) drawn i\.i\.d\. from P and must output a hypothesis h whose true error err\(h\) = P\(h\(x\) ≠ c\(x\)\) is small\.

The central challenge is generalisation: empirical error on training data underestimates true error when the sample is small\. PAC theory quantifies this gap precisely\.

## __3\.2  The PAC Bound__

__Theorem 2 \(PAC Learning in Binary Space\)__

*For any h ∈ H, with probability at least 1−δ:

    |err\(h\) − êrr\(h\)| ≤ ε

provided the sample size m satisfies m ≥ \(1/2ε²\) ln\(2/δ\)\.*

The bound controls the deviation between empirical error and true error, which is the fundamental object in generalisation theory\. The key tool is Hoeffding's inequality applied to the empirical mean of the random variable Z\_i = 1\[h\(x\_i\) ≠ y\_i\], which is bounded in \[0,1\] and has expectation err\(h\)\.

__Proof\.__ Fix h ∈ H\. Define indicator random variables Z\_i = 1\[h\(x\_i\) ≠ y\_i\] for i = 1, …, m drawn i\.i\.d\. from P\. Each Z\_i is bounded in \[0,1\] with E\[Z\_i\] = err\(h\) and êrr\(h\) = \(1/m\)Σ Z\_i\.

By Hoeffding's inequality for bounded i\.i\.d\. random variables:

P\( |êrr\(h\) − err\(h\)| > ε \)  ≤  2 exp\(−2mε²\)

Setting 2 exp\(−2mε²\) = δ and solving for m:

m  ≥  \(1 / 2ε²\) ln\(2/δ\)

The result follows directly\.

□

## __3\.3  Sample Complexity Over H__

Theorem 2 controls the deviation for a single fixed hypothesis h\. When the learner selects h from the entire hypothesis class H after seeing the data, the guarantee must hold simultaneously for all h ∈ H\. This requires a union bound over the class and changes the sample complexity by a factor of ln|H|\.

__Theorem 3 \(Sample Complexity\)__

*For binary hypothesis space H with |H| = 2^\{2^n\}:

    m  ≥  \(1/ε²\)\(ln|H| \+ ln\(1/δ\)\)

where ln|H| = 2^n · ln 2\.*

The quantity ln|H| = 2^n · ln 2 grows exponentially with n\. For n = 8 \(the default dimension in VERITAS\), ln|H| ≈ 177,000, so even with ε = 0\.01 and δ = 0\.01 the required sample count is approximately 1\.8 million\. This reflects the extraordinary richness of the binary hypothesis space and explains why PAC verification at small dimensions requires either very large datasets or relaxed \(ε, δ\) parameters\.

__Proof\.__ By a union bound over all h ∈ H, the event that any hypothesis in H has a deviation exceeding ε satisfies:

P\(∃h ∈ H : |êrr\(h\) − err\(h\)| > ε\)  ≤  |H| · 2 exp\(−2mε²\)

Setting this quantity equal to δ and solving for m:

m  ≥  \(1/2ε²\)\(ln\(2|H|/δ\)\)  =  \(1/2ε²\)\(ln 2 \+ ln|H| \+ ln\(1/δ\)\)

Absorbing the ln 2 constant into the leading 1/ε² factor \(replacing 1/2ε² with 1/ε² as is standard in PAC literature for simplicity\) and substituting ln|H| = 2^n · ln 2 gives the stated bound\.

□

## __3\.4  Practical Implications__

The exponential sample complexity has two practical consequences\. First, for any realistic training run on small binary patterns, the PAC step of the proof trace will show False until a sufficient number of examples have been accumulated\. This is expected and correct: the bound is tight in the worst case over H, and the full hypothesis class is extremely large\. Second, if the system is known to restrict attention to a much smaller subclass H' ⊂ H, the bound improves to ln|H'|\. Subclass selection is one practical strategy for making PAC verification achievable with moderate data\.

# __4\.  ALT Learning Framework__

## __4\.1  Overview__

Algorithmic Learning Theory \(ALT\) approaches learnability from a different angle\. Rather than asking how many random examples are needed, ALT asks how many *mistakes* an online learner makes before converging to the target, and how many *queries* it needs to identify the target exactly\. These are worst\-case over the target and the presentation order, rather than a probabilistic statement over random samples\.

The two main quantities are the mistake bound M\(L\) — the maximum number of incorrect predictions the algorithm makes across all possible target concepts before converging — and the query complexity Q\(L\) — the number of membership queries needed to exactly identify the target\. In the binary setting, both are determined by the size of the version space, which shrinks with each mistake or query\.

## __4\.2  Mistake Bound__

__Theorem 4 \(Mistake Bound\)__

*For any learning algorithm L on hypothesis space H:

    M\(L\)  ≤  lg|H|  =  2^n

where |H| = 2^\{2^n\} and lg denotes logarithm base 2\.*

The mistake bound is 2^n, which is exponential in n\. For n = 4 this is 16; for n = 8 it is 256\. Each mistake guarantees progress: at least half the remaining candidates are eliminated, so the version space reaches size 1 \(i\.e\., the target is uniquely identified\) after at most lg|H| mistakes\.

__Proof\.__ Let V\_t denote the version space — the set of hypotheses in H consistent with all examples seen up to time t — with V\_0 = H\. On any trial where the learning algorithm makes a mistake, its prediction h differs from the true label\. At least one of the two possible outputs is wrong for at least half the remaining hypotheses\. A standard halving argument \(Littlestone 1988\) shows that every mistake eliminates at least half the version space:

|V\_\{t\+1\}|  ≤  |V\_t| / 2

Starting from |V\_0| = |H|, after M mistakes we have |V\_M| ≤ |H| / 2^M\. Since |V\_M| ≥ 1, we obtain 2^M ≤ |H|, hence M ≤ lg|H|\. Substituting |H| = 2^\{2^n\} gives M ≤ lg\(2^\{2^n\}\) = 2^n\.

□

## __4\.3  Query Complexity__

__Theorem 5 \(Query Complexity\)__

*For exact identification of any target in H:

    Q\(L\)  ≤  n

where Q\(L\) is the number of membership queries required per identification round\.*

The query bound of n reflects the fact that each membership query reveals one bit of information about the target pattern\. Binary search over the n\-dimensional pattern space achieves exact identification in exactly n queries\. This is an *information\-theoretic* bound: n bits of target information require at least n queries, so the bound is tight\.

__Proof\.__ A membership query asks: "Is pattern x labelled 1 by the target concept c?" Each response is a single bit\. The target c is one of |H| = 2^\{2^n\} concepts, but a specific target pattern x ∈ B is an n\-bit string, so the label c\(x\) ∈ \{0,1\} reveals one of the n bits of x\. By querying each of the n canonical basis patterns e\_1 = 10⋯0, e\_2 = 010⋯0, …, e\_n = 0⋯01, the learner recovers the full truth table of c on B in n queries\. Hence Q\(L\) ≤ n\.

□

## __4\.4  Relationship Between Bounds__

The mistake bound and query complexity measure different things and are not directly comparable\. Mistake bounds apply to online learning with adversarial presentation; query bounds apply to active learning where the learner chooses queries\. In VERITAS, both are tracked simultaneously\. The system increments its mistake count when the rule network's prediction error exceeds ε, and increments its query count on every forward pass\. The proof verification checks both against their respective bounds\.

Note that the query bound Q ≤ n is a *per\-round* bound\. VERITAS accumulates queries across training steps, so the cumulative query count will exceed n after the first n steps\. This is correct behaviour: the bound governs how many queries are needed to identify a target in a single round of exact learning, not across an entire training regime\.

# __5\.  Meta\-Learning Theory__

## __5\.1  Motivation and Structure__

The meta\-learning layer of VERITAS operates over the hypothesis space H rather than over pattern space B\. Its purpose is to learn a transformation m : H → H that maps base hypotheses to improved hypotheses — in effect, learning how to learn\. This is a second\-order optimisation problem: instead of minimising error on B, the meta\-learner minimises error on H\.

Because H is a function space rather than a vector space, the standard PAC and ALT frameworks must be reinterpreted\. The inputs to the meta\-learner are themselves functions \(encoded as weight vectors in the implementation\), and the labels are also functions\. The theory proceeds by treating H as the new instance space and M as the new hypothesis space, then applying the base results at this elevated level\.

## __5\.2  Meta\-PAC Bounds__

__Theorem 6 \(Meta\-Learning PAC Bounds\)__

*For any meta\-learner m ∈ M, with probability at least 1−δ\_m:

    |err\_m\(m\) − êrr\_m\(m\)|  ≤  ε\_m

where err\_m\(m\) is the true meta\-error and êrr\_m\(m\) is the empirical meta\-error\.*

The proof follows the same structure as Theorem 2, with H playing the role of B and M playing the role of H\. The meta\-error is defined with respect to the meta\-distribution over H, and the Hoeffding bound applies because meta\-errors are bounded in \[0,1\]\.

__Proof\.__ Apply the PAC framework of Theorem 2 to the meta\-space with instance space H, hypothesis class M, and meta\-error function err\_m\. The required sample count for m meta\-examples is:

m\_\{ℳ\}  ≥  \(1/ε\_m²\)\(ln|M| \+ ln\(1/δ\_m\)\)

Since |M| = |H|^\{|H|\} = 2^\{2^n · 2^\{2^n\}\}, the meta\-sample complexity is doubly exponential in n\. In practice this bound is not tight because the system does not explore all of M; the meta\-network is a parametric restriction of M with a far smaller effective size\.

□

## __5\.3  Meta\-ALT Bounds__

__Theorem 7 \(Meta\-Learning Mistake Bound\)__

*For any meta\-learning algorithm operating on M:

    M\(m\)  ≤  lg|M|  =  2^n · 2^\{2^n\}*

This bound is doubly exponential and is best understood as a worst\-case guarantee over the entire meta\-space\. For practical systems where the meta\-learner is restricted to a parametric subspace, the effective bound is much smaller and is determined by the VC dimension or Rademacher complexity of that subspace\.

__Proof\.__ Apply the halving argument of Theorem 4 to the meta\-version space with |M| = |H|^\{|H|\}\. Each mistake halves the meta\-version space, giving M\(m\) ≤ lg|M|\. Substituting |M| = 2^\{2^n · 2^\{2^n\}\} gives lg|M| = 2^n · 2^\{2^n\}\.

□

# __6\.  Verification Theory__

## __6\.1  The Role of Verification__

The verification layer is what distinguishes VERITAS from a conventional learning system\. At each training step, the system constructs a formal proof trace consisting of four proofs — PAC, ALT, meta, and composition — and only updates its weights when the composition proof verifies\. This creates a feedback loop where learning is conditioned on provable progress\.

The verification space V = \{v : H × M → \{0,1\}\} contains all possible verification functions\. The specific verifier used by VERITAS evaluates whether the current hypothesis h and meta\-learner m jointly satisfy the bounds established in Sections 3, 4, and 5\.

## __6\.2  Verification Completeness__

__Theorem 8 \(Verification Completeness\)__

*For verifier v ∈ V:

    v complete  ⇔  ∀h, m:  v\(h, m\) = 1  ⇒  properties verified*

This theorem states that the verifier is both sound and complete with respect to the properties it checks\. Soundness means there are no false positives: if v\(h, m\) = 1 then all required properties hold\. Completeness means there are no false negatives: if all properties hold then v\(h, m\) = 1\.

__Proof\.__ The verifier v is constructed as the conjunction of individual property checks\. Let P\_1, …, P\_k denote the properties verified \(PAC error bound, ALT mistake bound, ALT query bound, meta\-error bound, and composition validity\)\. Then:

v\(h, m\) = ⋀\_\{i=1\}^\{k\} P\_i\(h, m\)

where each P\_i is a decidable predicate over the current learning statistics\. Soundness follows by the definition of conjunction: if v = 1 then each P\_i = 1, which means each property holds\. Completeness follows from the same definition: if all P\_i = 1 then v = 1\. The predicates P\_i are computable from the observable learning statistics \(empirical error, sample count, mistake count, query count\), so v is effectively computable\.

□

## __6\.3  Composition of Learning Guarantees__

The deepest result in the verification framework is Theorem 9, which shows that PAC and ALT guarantees compose gracefully through the meta\-learning layer\. This is the theoretical underpinning for why verifying the base learner and the meta\-learner separately is sufficient to guarantee the end\-to\-end system\.

__Theorem 9 \(Learning Composition\)__

*For h ∈ H, m ∈ M:

    If P\(err\(h\) > ε\) ≤ δ  and  P\(err\_m\(m\) > ε\_m\) ≤ δ\_m
    Then P\(err\(m ∘ h\) > ε \+ ε\_m\) ≤ δ \+ δ\_m*

The composed error ε \+ ε\_m and composed failure probability δ \+ δ\_m are both additive in the individual bounds\. This means that if the base learner and meta\-learner each have small errors and small failure probabilities, so does their composition\. The proof uses two classical tools: the triangle inequality for error rates and the union bound for probabilities\.

__Proof\.__ Let A denote the event err\(h\) > ε and let B denote the event err\_m\(m\) > ε\_m\. We are given P\(A\) ≤ δ and P\(B\) ≤ δ\_m\.

__Step 1 \(Triangle inequality on errors\)\.__ For any input x:

err\(m ∘ h\)\(x\) ≤ err\(h\)\(x\) \+ err\_m\(m\)\(h\(x\)\)

Taking expectations over x under P and using linearity of expectation:

err\(m ∘ h\)  ≤  err\(h\) \+ err\_m\(m\)

Therefore if both err\(h\) ≤ ε and err\_m\(m\) ≤ ε\_m then err\(m ∘ h\) ≤ ε \+ ε\_m\.

__Step 2 \(Union bound\)\.__ The event err\(m ∘ h\) > ε \+ ε\_m is a subset of A ∪ B \(since err\(m ∘ h\) ≤ ε \+ ε\_m whenever neither A nor B occurs\)\. By the union bound:

P\(err\(m ∘ h\) > ε \+ ε\_m\)  ≤  P\(A ∪ B\)  ≤  P\(A\) \+ P\(B\)  ≤  δ \+ δ\_m

This completes the proof\.

□

## __6\.4  Proof Trace Structure__

At each learning step, VERITAS constructs a proof trace consisting of the following components in order:

- PAC proof — verifies Theorems 2 and 3: sample count, Hoeffding bound, and confidence
- ALT proof — verifies Theorems 4 and 5: mistake bound and query bound
- Meta proof — verifies Theorem 6: meta\-error bound derived from the PAC proof
- Composition proof — verifies Theorem 9: validity of the composed bound using PAC and ALT proofs

The trace is accepted \(and the weight update applied\) only when the composition proof verifies\. This means that the PAC, ALT, and meta proofs must all verify first, since the composition proof depends on them\. The overall confidence assigned to a trace is the fraction of the four proofs that fully verify\.

# __7\.  Distillation and Ensemble Theory__

## __7\.1  Knowledge Distillation in Binary Spaces__

VERITAS supports a distillation training regime in which an ensemble of teacher models — each a fully trained VERITAS instance — supervises the training of a smaller student model\. The student learns to match both the rule\-network outputs and the meta\-network outputs of the ensemble, with a temperature\-scaled KL divergence driving the soft\-target objective\.

The theoretical basis for distillation in this setting follows from the PAC framework applied to the student's hypothesis space\. If the ensemble of T teachers has combined empirical error êrr\_T\(h\) = \(1/T\)Σ\_t êrr\(h\_t\), then by Jensen's inequality and the convexity of the squared error:

err\(h\_\{θ\}\)  ≤  \(1 − α\) · D\_\{KL\}\(h\_\{θ\} || h\_T\) \+ α · êrr\(h\_\{θ\}\)

where h\_θ is the student, h\_T is the ensemble average, α ∈ \[0,1\] is the balance parameter, and the KL divergence is computed on the temperature\-scaled softmax outputs\. The temperature T\_τ > 1 softens the teacher distribution, providing richer gradient signal in regions where the teacher is uncertain\.

## __7\.2  Ensemble Averaging__

The ensemble output is the arithmetic mean of the T teacher outputs\. By the law of large numbers, as T → ∞ the ensemble mean converges to the expected hypothesis under the distribution over teacher initialisation\. For finite T, the variance of the ensemble error is reduced relative to any single teacher by a factor of T:

Var\[êrr\_T\]  =  \(1/T\) · Var\[êrr\]

This variance reduction is the principal benefit of ensemble distillation: the student learns from a lower\-variance target, which translates directly into a tighter generalisation bound\.

# __8\.  Summary of Theoretical Results__

The following table summarises the nine theorems established in this document, the spaces they concern, and their principal implications for the VERITAS system\.

__Thm__

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

PAC bound lifts to meta\-space M

7

Meta\-ALT

M

M\(m\) ≤ lg|M| = 2^n · 2^\{2^n\}

8

Verification Completeness

V

v\(h,m\)=1 ⇔ all properties hold

9

Composition

H × M

err\(m∘h\) ≤ ε\+ε\_m w\.p\. ≥ 1−\(δ\+δ\_m\)

## __8\.1  Convergence Conditions__

For the composition proof to verify, all of the following conditions must hold simultaneously:

- PAC condition: n\_samples ≥ \(1/ε²\)\(2^n ln2 \+ ln\(1/δ\)\) and empirical\_error ≤ ε \+ Hoeffding\(m, δ\)
- ALT mistake condition: cumulative\_mistakes ≤ 2^n
- ALT query condition \(per round\): queries\_this\_round ≤ n
- Meta condition: meta\_error ≤ 2ε
- Composition: both PAC and ALT proofs verified

In practice, the PAC sample complexity condition is the binding constraint for small n\. Once sufficient data has been accumulated, all other conditions are typically satisfied well within their bounds\.

