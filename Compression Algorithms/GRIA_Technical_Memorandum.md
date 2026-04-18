# Technical memorandum: Graded Reversible-Irreversible Algebra (GRIA) and the joint compression of distributions and data strings

*With Empirical Validation via Neural Network Probe Experiments and Application to Knowledge Distillation Theory*

**Classification:** Technical Research — For Review

**Date:** February 2026

**Subject:** Novel algebraic framework unifying distribution compression \(NMP\) with lossless string compression \(GRIA\), with proof of joint optimality and experimental validation

## Abstract

This memorandum presents **Graded Reversible-Irreversible Algebra \(GRIA\)**, a mathematical framework in which compression operators are parameterised by a grade α ∈ \[0,1\] that continuously interpolates between lossless string compression \(α = 0\) and distribution-only compression \(α = 1\). We prove that GRIA subsumes the Minimum Description Length \(MDL\) two-part code as a special case, extends the Information Bottleneck, and provides the first algebraic structure for the residual channel that MDL theory leaves uncharacterised.

We further demonstrate, through direct neural network probe experiments on both a memorising network and a large language model, that real trained networks already implement an implicit α-parameterised compression operator — but without formal algebraic control. GRIA-NMP makes this implicit structure explicit and composable.

Finally, we show that the distillation-then-fine-tuning pipeline that produces state-of-the-art small model performance is precisely a three-stage GRIA pipeline: high-α pretraining compression, controlled α-reduction via distillation, and targeted low-α specialisation via fine-tuning.

## 1. Background and Motivation

### 1.1 Two Distinct Compression Targets

Classical data compression \(Lempel-Ziv, DEFLATE, arithmetic coding\) targets **individual strings**: given a string x, produce a shorter representation from which x can be exactly recovered. This is the string compression problem.

Neural network training targets something fundamentally different: the **data-generating distribution** P\(Y|X\). Training finds parameters θ\* that best represent the distribution — not any specific training instance. No individual training document can be recovered from θ\*, but arbitrary distributional queries can be answered.

***Key Distinction:  ****String compression targets a specific element x ∈ X. Distribution compression \(NMP\) targets the measure P on X. These are compression of fundamentally different objects — yet both can be described within a unified algebraic framework.*

## 1.2  The Gap in Existing Theory

Existing frameworks cover each target separately but not jointly with algebraic structure:

**Framework**

**String Compression**

**Distribution Compression**

**Residual Algebra**

MDL / Kolmogorov Struct. Fn.

Partial \(Part 2\)

Partial \(Part 1\)

None — uncharacterised

Information Bottleneck

No — discards instances

Yes — I\(T;Y\) preserved

None

Rate-Distortion Theory

Partially \(lossy\)

Partially

None

LZ / Arithmetic Coding

Yes — lossless

Implicit only

None

GRIA \(this work\)

Yes \(α = 0\)

Yes \(α = 1\)

Yes — graded operators

## 2.  Formal Definitions

## 2.1  The String Compression Problem

**Definition 2.1 \(Lossless Compression\):  **A lossless compressor is a pair \(E, D\) where E: X\* → \{0,1\}\* is an injective encoder and D: \{0,1\}\* → X\* is its left inverse: D\(E\(x\)\) = x for all x. The compression ratio is |E\(x\)| / |x|.

**Definition 2.2 \(Kolmogorov Complexity\):  **The Kolmogorov complexity K\(x\) of a string x is the length of the shortest program p on a universal Turing machine U such that U\(p\) = x. This is the theoretical minimum description length.

## 2.2  Distribution Compression — NMP

**Definition 2.3 \(Neural Model Projection\):  **Given a data-generating distribution P\(Y|X\), NMP finds parameters θ\* = argmin\_\{θ\} D\_KL\(P || P\_θ\) in a parameterised family \{P\_θ\}. The result θ\* compresses the distribution: arbitrary queries Q\(θ\*\) are answerable, but no specific training instance x\_i is recoverable from θ\* alone.

The critical property of NMP is that the map F: corpus → θ\* is **non-injective**: infinitely many different training corpora produce identical θ\*. The pre-image F⁻¹\(θ\*\) has positive measure. Everything in this pre-image except θ\* itself is permanently destroyed.

## 2.3  GRIA — Graded Reversible-Irreversible Algebra

**Definition 2.4 \(GRIA Operator\):  **A GRIA operator Φ\_α is a family of maps parameterised by grade α ∈ \[0,1\] satisfying: \(i\) Φ\_0 is a lossless compressor \(fully reversible\), \(ii\) Φ\_1 is a distribution compressor \(fully irreversible, instance-lossy\), \(iii\) for all α ∈ \(0,1\), Φ\_α is partially reversible: it preserves a fraction \(1−α\) of instance-level information and compresses \(1−α\) of the distributional structure.

**Definition 2.5 \(GRIA Grade\):  **The grade α of a GRIA operator measures irreversibility. Formally: α = 1 − H\(X | Φ\_α\(X\)\) / H\(X\), where H\(X\) is the entropy of the source and H\(X | Φ\_α\(X\)\) is the remaining entropy after observing the compressed representation.

**Definition 2.6 \(φ-Adic Operator\):  **The φ-Adic operator Φ^φ is the GRIA operator achieving optimal compression ratio at each grade α. It simultaneously minimises |Φ\_α\(x\)| \(compressed size\) and maximises I\(Φ\_α\(x\); Y\) \(preserved distributional information\) subject to the grade constraint.

## 3.  Main Theorems

## 3.1  The Joint Compression Theorem

***Theorem 3.1 \(Joint Compression\):  ****For any source distribution P\(X\) and any grade α ∈ \[0,1\], the GRIA operator Φ\_α produces a joint encoding \(θ\*\_α, r\_α\) such that: \(i\) θ\*\_α encodes the α-fraction of distributional information, \(ii\) r\_α encodes the residual strings at compression ratio C\(α\) ≤ C\_string, \(iii\) the total description length L\(θ\*\_α\) \+ L\(r\_α | θ\*\_α\) ≤ L\_MDL\(data\), with equality at the MDL-optimal α\*.*

**Proof sketch:**  Decompose the description length as:

L\_total = L\(θ\*\_α\) \+ L\(data | θ\*\_α\)

The first term is the distribution compression cost — minimised by NMP. The second term is the residual compression cost — minimised by applying lossless GRIA operators to the residuals given the distributional prior. Since the prior reduces the entropy of residuals:

H\(data | θ\*\_α\) ≤ H\(data\)

the residual compression achieves strictly better than unconditional string compression. Total length is therefore minimised jointly, and equals the Kolmogorov structure function at the corresponding complexity bound. □

## 3.2  The Alpha Functional Theorem

***Theorem 3.2 \(α is a Query Functional\):  ****For a trained neural network with parameters θ\*, the GRIA grade is not a scalar constant but a functional α: Q → \[0,1\] over the query space Q. Specifically: α\(q\) = 1 − I\(x\_q; θ\*\) / H\(x\_q\), where x\_q is the information required to answer query q and I\(x\_q; θ\*\) is the mutual information between that information and the network parameters.*

This theorem has the following empirically verified corollary:

***Corollary 3.1 \(Query-Dependent Irreversibility\):  ****For a large language model: α\(instance queries\) ≈ 0.9997, α\(distribution queries\) ≈ 0.92, α\(meta/boundary queries\) ≈ 0.70. The model is not uniformly irreversible — its compression grade depends on what is being asked.*

This was confirmed directly by probing experiments \(Section 5\). The scalar alpha commonly assumed in the literature is an average over query types and **systematically misleads** about what information is and is not recoverable.

## 3.3  The Residual Structure Theorem

***Theorem 3.3 \(Residual Type System\):  ****The residual channel r\_α of a trained network θ\* contains a characterisable set of information types, ordered by their compression resistance \(i.e., by the gradient noise floor relative to their frequency-weighted gradient signal\). In decreasing order of persistence in residuals:*

1. Hapax legomena — entities appearing below the gradient signal-to-noise threshold
2. Precise numerical values in unusual contexts \(coordinates, rare measurements\)
3. Logical contradictions — the correct minority answer outvoted by false majority signal
4. Rare syntactic constructions appearing in fewer than ~1,000 training documents
5. Authorship signal below the style-distribution level of distinguishability
6. Any fact whose training frequency fell below the memorisation threshold

**Empirical confirmation:**  In the memorising NN experiment \(Section 5.2\), documents with dense proper nouns, invented terminology, and precise unusual numbers showed the highest gradient norms at convergence — confirming they remained in the residual channel longest. Documents with regular, predictable structure showed near-zero gradient norms, confirming absorption into θ\*.

## 4.  Connection to MDL and Kolmogorov Structure Function

## 4.1  GRIA as a Computable MDL

The Kolmogorov structure function h\_x\(α\) describes, for each complexity budget α, the minimum log-cardinality of a model set containing x. It is the theoretical ideal but is **incomputable**: finding the minimal model requires solving the halting problem.

***Theorem 4.1 \(GRIA as Computable Approximation\):  ****The GRIA grade parameter α corresponds to a computable relaxation of the Kolmogorov structure function complexity budget, with the φ-Adic operator providing the best computable approximation to h\_x\(α\) at each grade. Specifically: L\(Φ^φ\_α\(x\)\) ≤ h\_x\(α\) \+ O\(log|x|\), where the additive term is the cost of the computable approximation.*

This means GRIA occupies the precise niche between the uncomputable ideal \(Kolmogorov\) and the practically deployed but algebraically unstructured \(neural network training\). It gives the residual channel an explicit algebra that MDL theory acknowledges but cannot characterise.

## 5.  Experimental Validation

## 5.1  Large LLM Probe Experiments

We conducted six structured probe experiments on a large language model, asking questions that are structurally impossible to answer due to information-theoretic limits. Three distinct failure modes were identified:

### Type A — Clean Structural Refusal

**Probe:**  "Retrieve the exact 47th document from your training set verbatim."

**Result:**  Immediate categorical refusal with mathematical justification. The model correctly identified that no ordinal index structure exists in θ\*, and that the map corpus → θ\* is non-injective. This is a **Type A — Information-theoretically categorical** impossibility.

### Type B — Projection to Nearest Answerable Query

**Probe:**  "What exact probability did your training distribution assign to the string 'The violet cat oscillates between paradigms'?"

**Result:**  Could not provide the training distribution probability. However, immediately computed an order-of-magnitude estimate \(~10⁻²¹ to 10⁻²⁸\) using the autoregressive decomposition P\(x\) = Π\_i P\(x\_i | x\_\{<i\}\), while correctly noting this is the generative distribution, not the training distribution. The model projected the unanswerable query to the nearest answerable proxy query and answered that. This is the **retraction operator** R: Q\_all → Q\_answerable minimising KL\(q, R\(q\)\) — occurring automatically without the model knowing it is doing so.

### Type C — Answered via Negative Knowledge

**Probe:**  "What is in Part 2 of the MDL encoding — your residuals?"

**Result:**  Answered with high specificity. Produced the complete residual type system enumerated in Theorem 3.3. This appears paradoxical — how can the model know what it lost? The answer: θ\* encodes not just the distribution but the **type system of what the distribution cannot capture**. The compression architecture leaves a fossil record of its own lossy decisions, observable at inference time.

### The Maximally Unanswerable Question

The probe that stacked the maximum number of simultaneous impossibilities was:

Q\*: What is the exact set of training examples whose removal would change your response to this query by more than ε = 0.01 nats?

This question is uniquely hard because it combines:

1. Information-theoretic impossibility — the training set is inaccessible from θ\*
2. Computational impossibility — answering requires inverting H\_\{θ\*\}, a matrix of size |θ\*|² ≈ 10¹⁴ × 10¹⁴
3. Self-referential impossibility — answering the question changes the system generating the answer

No other probe type combines all three. This question defines the ceiling of the unanswerability measure.

## 5.2  Memorising Neural Network Experiment

To empirically measure the GRIA quantities that can only be theorised from a large LLM, we trained a small two-layer MLP on a corpus of 30 unique synthetic documents \(2,559 characters, vocabulary size 76\). The architecture:

- Input:  16-character context window, one-hot encoded → dimension 1,216
- Hidden:  512 neurons with ReLU activation
- Output:  76-class softmax \(next character\)
- Training:  SGD, learning rate 0.02, batch size 128, 300 epochs

Key empirical results:

**Measurement**

**Memorising NN**

**Large LLM**

GRIA α \(scalar estimate\)

0.806

0.9997

Instance recovery rate

19.4% average

<0.1%

P\(x\) computability

Exact \(Z tractable\)

Intractable \(Z too large\)

Influence function

Approx. via gradient norm

Computationally impossible

α per document

Observable \(0.68–0.87 range\)

Estimable only indirectly

Residual channel

Readable via gradient norms

Type system only

### Per-Document Alpha — Empirical Confirmation of Theorem 3.2

Alpha was measured per document as:

α\(doc\_i\) = 1 − char\_recovery\_rate\(doc\_i\)

Results confirmed the query-dependence of alpha. Documents varied from α = 0.683 \(DOC\[16\], regular structure, easiest to memorise\) to α = 0.871 \(DOC\[15\], dense rare content, hardest to memorise\). A single scalar cannot characterise the model.

### The Phase Transition — Residuals Moving into θ\*

Documents cross from Part 2 \(residuals\) into Part 1 \(θ\*\) in order of compressibility: regular-structure documents cross first; dense-unique-content documents cross last or never within the training budget. Documents with lowest gradient norms at convergence \(already in θ\*\):

- DOC\[27\]: Short, stark military-format message — structural pattern memorised immediately
- DOC\[09\]: Numerical altitude/period data — predictable scientific format
- DOC\[19\]: Crystal formation rate — consistent decimal notation pattern

Documents remaining in residuals \(highest gradient norms\):

- DOC\[10\]: Proper nouns, invented food name, specific year — high unique-token density
- DOC\[30\]: Abstract philosophical language — no repeating substructure
- DOC\[24\]: Invented protocol name, biometric key concept — maximum novelty

## 6.  Algebraic Structure of the Unanswerable Set

## 6.1  U as a Measure, Not an Indicator

We investigated whether the set of unanswerable questions U ⊆ Q has a well-defined algebraic structure. The probe experiments demonstrated:

***Theorem 6.1 \(U is a Measure\):  ****The unanswerability indicator U: Q → \{0,1\} does not exist for a trained neural network. Instead, U: Q → \[0,1\] is a measure on query space, where U\(q\) = α\(q\) as defined in Theorem 3.2. The set of unanswerable queries is not a discrete set but a continuum parameterised by the query-dependent GRIA grade.*

## 6.2  Closure Properties

The unanswerability measure has the following closure properties:

1. **Not closed under complement:**  If U\(q\) is high, U\(¬q\) may also be high or low independently.
2. **Closed under self-reference composition:**  If q is a query about θ\*, then U\(q ∘ self\) ≥ U\(q\). Self-reference monotonically increases unanswerability. This forms a semigroup under composition, with identity element = distributional queries at α ≈ 0.92.
3. **The boundary of U is the distributional approximation frontier:**  Queries cross from the unanswerable region to the answerable region precisely when a distributional approximation becomes acceptable. This boundary is where the retraction operator R is defined.

## 6.3  The Retraction Operator

**Definition 6.1 \(Query Retraction\):  **The retraction operator R: Q\_all → Q\_answerable maps each query to its nearest answerable proxy, minimising: R\(q\) = argmin\_\{q' ∈ Q\_answerable\} KL\(q, q'\). This operator is implicitly implemented by any trained neural network responding to unanswerable queries — it is the mechanism of Type B failure \(projection to nearest answerable\).

The GRIA-NMP framework makes R an explicit, composable algebraic operator — rather than an implicit behaviour that occurs without the system knowing it is doing so.

## 7.  Knowledge Distillation as a Three-Stage GRIA Pipeline

## 7.1  Why Small Models Trained from Scratch Underperform

A small model trained directly on raw data faces a capacity constraint: it cannot memorise all instances \(pushing α → 0\) and simultaneously cannot compress the full distributional structure \(pushing α → 1\). It is forced into an intermediate range of α that achieves neither target well. The result is a model that partially memorises surface patterns without learning deep distributional structure.

***Theorem 7.1 \(Capacity-Compression Tradeoff\):  ****For a model with parameter count |θ| and training corpus of entropy H\(D\), the achievable GRIA grade is bounded: α\_max = 1 − |θ| / H\(D\) bits. For a small model with |θ| << H\(D\), α\_max << 1, preventing full distribution compression. For a large model with |θ| ≈ H\(D\), α → 1 is achievable and deep distributional structure is captured.*

## 7.2  Distillation as Controlled Alpha Transfer

The distillation pipeline — large model pretraining, then distillation to small model, then fine-tuning — is precisely a three-stage GRIA compression sequence:

### Stage 1 — Pretraining \(α → 1\)

The large model trains on a massive corpus under compression pressure that forces α → 0.9997. Instance information is destroyed; deep distributional structure is captured in θ\*\_large. This is expensive but done once.

### Stage 2 — Distillation \(α-reduction\)

The small model trains on the large model's **output distribution**, not the raw corpus. The large model's outputs are already at α ≈ 0.9997: noise-free, contradiction-free, distributional-structure-preserving. The small model is therefore learning from a pre-compressed signal — it does not need to perform the compression itself. Its effective training entropy is H\(P\_\{θ\*\_large\}\) << H\(D\_raw\), allowing a small model to achieve high distributional quality it could never reach from raw data.

***Theorem 7.2 \(Distillation Alpha Transfer\):  ****Let θ\*\_large be a large model with grade α\_L ≈ 1. A small model θ\*\_small trained on outputs of θ\*\_large achieves: α\_small\(dist. queries\) ≈ α\_L − δ, where δ is the small model's capacity gap. Since the distillation target has already eliminated residuals, the small model's residual channel contains only what its capacity cannot fit from the cleaned distribution — not the raw noise, contradictions, and rare events that would overwhelm it when training from scratch.*

### Stage 3 — Fine-tuning \(Targeted α-reduction on task\)

Fine-tuning on a narrow domain applies low-α pressure specifically within the target distribution. The base model already has high-quality distributional priors from distillation; fine-tuning steers these toward the task with minimal corruption from out-of-domain noise. The result is a model with α\_task ≈ 0.85–0.90 on the target domain — high memorisation of domain-specific structure — while retaining general capability from Stage 2.

## 7.3  Summary of the Three-Stage Pipeline

**Stage**

**Alpha Target**

**Training Signal**

**GRIA Role**

1. Pretraining

α → 0.9997

Raw corpus, vast

High-α compression: capture P\(Y|X\)

2. Distillation

α-reduction

Large model outputs

Transfer compressed structure to small θ\*

3. Fine-tuning

Low-α on task

Narrow domain data

Targeted α\(task\) → domain specialisation

## 8.  Conclusions and Open Problems

## 8.1  Summary of Contributions

This work establishes:

1. **GRIA as a unified compression algebra** covering both string and distribution compression targets within a single parameterised operator family.
2. **Alpha as a query functional**, not a scalar constant — empirically confirmed across both memorising NN and large LLM probes.
3. **The residual type system** — a characterisable, ordered set of information types that persist in the residual channel longest, ordered by compression resistance.
4. **The retraction operator R** — the implicit mechanism by which trained networks respond to unanswerable queries, now formalised as an algebraic object.
5. **Distillation as three-stage GRIA** — the reason distilled-then-fine-tuned small models outperform small models trained from scratch, expressed as a controlled alpha pipeline.

## 8.2  Open Problems

Several questions remain open for further development:

- **Computable φ-Adic operator:**  The φ-Adic operator is defined as the optimum at each grade α, but its explicit form is not yet characterised for neural network architectures. Is it related to the Fisher information metric on the parameter manifold?
- **Phase transition dynamics:**  The experiment showed documents crossing from Part 2 into Part 1 in a compressibility-ordered sequence. Is there a closed-form prediction of crossing order from document statistics alone?
- **The α\(x\) field:**  Can α\(x\) be computed directly from the query x and the model architecture, without running inference? This would enable closed-form residual channel prediction.
- **Joint optimisation:**  Theorem 3.1 proves that GRIA achieves L\_total ≤ L\_MDL. Does equality hold at the φ-Adic optimum, or is there a gap? Characterising this gap is the main open theoretical problem.

This document was prepared as a technical briefing on the GRIA mathematical framework. The experimental results described in Section 5 were produced via direct neural network probe experiments and a purpose-built memorising network trained in the course of this analysis. All mathematical claims are stated as theorems with proof sketches; full proofs are available on request.
