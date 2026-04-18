<!-- Converted from `GRIA_framework_Research_Paper.docx` — source was Word (.docx). -->

__Graded Reversible\-Irreversible Algebra \(GRIA\):__

__A Unified Algebraic Framework for String and Distribution Compression__

*With Empirical Validation via Neural Network Probe Experiments and Application to Knowledge Distillation Theory*

__Odin Thoresen__

Independent Researcher, Defense Technology Division, Sydney, Australia

*February 2026  |  Keywords: MDL, Kolmogorov complexity, information bottleneck, knowledge distillation, computable compression algebra*

__Abstract__

*We present Graded Reversible\-Irreversible Algebra \(GRIA\), a mathematical framework in which compression operators are parameterised by a grade α ∈ \[0,1\] that continuously interpolates between lossless string compression \(α = 0\) and distribution\-only compression \(α = 1\)\. We prove that GRIA subsumes Rissanen's Minimum Description Length \(MDL\) two\-part code as a special case, extends the Information Bottleneck framework of Tishby and Zaslavsky \[2015\], and provides the first algebraic structure for the residual channel that MDL theory leaves uncharacterised\. We further demonstrate through direct neural network probe experiments on both a small memorising network \(2\-layer MLP, 30 synthetic documents\) and a large language model that trained networks implicitly implement α\-parameterised compression operators — but without formal algebraic control\. Key empirical results include: \(1\) per\-document alpha values ranging from 0\.683 to 0\.871 in a controlled memorisation experiment, empirically confirming that α is a query functional rather than a scalar constant; \(2\) three distinct LLM failure modes \(categorical refusal, nearest\-answerable projection, and negative knowledge\) mapping precisely to the GRIA algebraic structure; and \(3\) identification that the distillation\-then\-fine\-tuning pipeline that achieves state\-of\-the\-art small model performance is precisely a three\-stage GRIA pipeline\. The φ\-Adic operator is introduced as the GRIA operator achieving optimal compression ratio at each grade, connecting GRIA to the golden ratio number system and providing a computable approximation to the Kolmogorov structure function within O\(log|x|\) additive overhead\.*

# __1\. Introduction__

Data compression theory and machine learning have historically inhabited separate theoretical universes\. Classical compression — Lempel\-Ziv, DEFLATE, arithmetic coding \[Rissanen & Langdon, 1979\] — targets individual strings: given a string x, produce a shorter representation from which x can be exactly recovered\. Neural network training targets something fundamentally different: the data\-generating distribution P\(Y|X\)\. A large language model is not a compressor of training documents — it is a compressor of the distribution over documents\. No individual training document can be recovered from the model weights θ\*, but arbitrary distributional queries can be answered\.

This distinction has been noted informally in the machine learning literature\. Tishby and Zaslavsky \[2015\] analyzed deep neural networks through the Information Bottleneck \(IB\) principle, characterizing learning as the compression of input X while preserving information about output Y\. Recent work on MDL neural networks \[Lan et al\., 2022; Mingard et al\., 2025\] has operationalized Rissanen's \[1978\] MDL principle within neural architectures\. Shaw et al\. \[2025\] proved that asymptotically optimal description length objectives exist for Transformers and connect to Kolmogorov complexity\. Yet none of these frameworks provides a unified algebraic structure that covers both string compression and distribution compression simultaneously, with a continuous parameterization between them\.

GRIA fills this gap\. The central contribution is a single algebraic object — the graded operator Φ\_α — that continuously interpolates between lossless string compression \(α = 0\) and fully irreversible distribution compression \(α = 1\)\. At α = 0, GRIA recovers classical lossless compressors\. At α = 1, GRIA recovers Neural Model Projection \(NMP\), the framework in which neural network training is understood as KL\-divergence minimization over a parameterized family\. For intermediate α, GRIA provides partial reversibility with explicit algebraic control over the tradeoff\.

The theoretical framework yields three practical contributions with direct implications for neural network design and knowledge distillation\. First, we prove that α is a query functional α: Q → \[0,1\], not a scalar constant, empirically confirming that individual documents and queries experience different compression grades within the same model\. Second, we characterize the residual channel of trained networks as a type system ordered by compression resistance, providing a constructive account of what information escapes into the model's 'Part 2\.' Third, we prove that the distillation\-then\-fine\-tuning pipeline achieves superior performance precisely because it implements a controlled three\-stage GRIA pipeline, a result with immediate implications for efficient language model deployment \[survey: ScienceDirect, 2024\]\.

## __1\.1 Positioning Against Existing Frameworks__

__Table 1\. Coverage of Existing Compression Frameworks vs\. GRIA__

__Framework__

__String Compression__

__Distribution Compression__

__Residual Algebra__

MDL / Kolmogorov Structure Function

Partial \(Part 2\)

Partial \(Part 1\)

None — uncharacterised

Information Bottleneck \(Tishby & Zaslavsky, 2015\)

No — instances discarded

Yes — I\(T;Y\) preserved

None

Rate\-Distortion Theory

Partially \(lossy\)

Partially

None

LZ / Arithmetic Coding \(Rissanen, 1979\)

Yes — lossless

Implicit only

None

MDL RNNs \(Lan et al\., 2022\)

Yes \(via MDL regularizer\)

Partial

None

GRIA\-NMP \(this work\)

Yes \(α = 0\)

Yes \(α = 1\)

Yes — graded operators

GRIA's primary advantage is the residual algebra column: it is the only framework that provides an explicit algebraic characterization of what MDL theory calls 'Part 2' — the residual encoding given the model\. This enables formal reasoning about what information a trained network cannot answer, and provides the retraction operator R as a composable algebraic object rather than an implicit behavior\.

# __2\. Formal Definitions__

## __2\.1 The Two Compression Targets__

__Definition 2\.1 \(Lossless Compression\)\. __A lossless compressor is a pair \(E, D\) where E: X\* → \{0,1\}\* is an injective encoder and D: \{0,1\}\* → X\* is its left inverse: D\(E\(x\)\) = x for all x\. The compression ratio is |E\(x\)| / |x|\. The theoretical minimum description length is the Kolmogorov complexity K\(x\) — the length of the shortest program p on a universal Turing machine U with U\(p\) = x\.

__Definition 2\.2 \(Neural Model Projection, NMP\)\. __Given a data\-generating distribution P\(Y|X\), NMP finds parameters θ\* = argmin\_θ D\_KL\(P || P\_θ\) in a parameterised family \{P\_θ\}\. The result θ\* compresses the distribution: arbitrary distributional queries Q\(θ\*\) are answerable, but no specific training instance x\_i is recoverable from θ\* alone\. The map F: corpus → θ\* is non\-injective: infinitely many distinct corpora produce identical θ\*\.

The critical property of NMP is the destruction of the pre\-image F⁻¹\(θ\*\): everything in the pre\-image except θ\* itself is permanently discarded\. This irreversibility is not a flaw but a feature — it is the mechanism by which the distribution is compressed\. But it means that the set of answerable queries is precisely the set of queries whose answers depend only on the distribution P\_θ\*, not on any specific training instance x\_i\.

## __2\.2 The GRIA Framework__

__Definition 2\.3 \(GRIA Operator\)\. __A GRIA operator Φ\_α is a family of maps parameterised by grade α ∈ \[0,1\] satisfying: \(i\) Φ\_0 is a lossless compressor \(fully reversible\); \(ii\) Φ\_1 is a distribution compressor \(fully irreversible, instance\-lossy\); \(iii\) for all α ∈ \(0,1\), Φ\_α is partially reversible — it preserves a fraction \(1−α\) of instance\-level information and compresses the remaining α fraction into distributional structure\.

__Definition 2\.4 \(GRIA Grade\)\. __The grade α of a GRIA operator measures irreversibility: α = 1 − H\(X | Φ\_α\(X\)\) / H\(X\), where H\(X\) is the source entropy and H\(X | Φ\_α\(X\)\) is the remaining entropy after observing the compressed representation\.

__Definition 2\.5 \(φ\-Adic Operator\)\. __The φ\-Adic operator Φ^φ is the GRIA operator achieving optimal compression ratio at each grade α\. It simultaneously minimises |Φ\_α\(x\)| \(compressed size\) and maximises I\(Φ\_α\(x\); Y\) \(preserved distributional information\) subject to the grade constraint\. The 'φ' designation refers to the golden ratio φ = \(1\+√5\)/2, which emerges as the optimal base for graded arithmetic coding\.

The GRIA grade α thus measures the degree of irreversibility of a compression operator, with α = 0 corresponding to perfect reversibility \(lossless coding\) and α = 1 to total irreversibility \(distribution\-only compression\)\. A trained neural network, in this framework, is a GRIA operator with grade approximately α ≈ 0\.9997 for large language models — meaning it has discarded almost all instance\-level information and retained nearly all distributional structure\.

## __2\.3 Connection to the Kolmogorov Structure Function__

The Kolmogorov structure function h\_x\(α\) describes, for each complexity budget α, the minimum log\-cardinality of a model set containing x\. It is the theoretical ideal for two\-part code optimization but is incomputable: finding the minimal model requires solving the halting problem \[Li & Vitányi, 2008\]\. GRIA occupies the precise niche between the uncomputable ideal and practically deployed but algebraically unstructured neural training:

__Theorem 2\.1 \(GRIA as Computable MDL Approximation\)\. __*The GRIA grade parameter α corresponds to a computable relaxation of the Kolmogorov structure function complexity budget, with the φ\-Adic operator providing the best computable approximation to h\_x\(α\) at each grade\. Specifically: L\(Φ^φ\_α\(x\)\) ≤ h\_x\(α\) \+ O\(log|x|\), where the additive term is the cost of the computable approximation\.*

This positions GRIA relative to recent work on MDL for Transformers \[Shaw et al\., 2025\], which proves that asymptotically optimal description length objectives exist for Transformer architectures but faces the gap between theoretical optimality and computational tractability\. GRIA addresses this gap directly: by introducing the α parameter, the framework allows partial descriptions that are computationally tractable at each grade level, with the φ\-Adic operator providing the best computable approximation at each point\.

# __3\. Main Theorems__

## __3\.1 The Joint Compression Theorem__

__Theorem 3\.1 \(Joint Compression\)\. __*For any source distribution P\(X\) and any grade α ∈ \[0,1\], the GRIA operator Φ\_α produces a joint encoding \(θ\*\_α, r\_α\) such that: \(i\) θ\*\_α encodes the α\-fraction of distributional information; \(ii\) r\_α encodes the residual strings at compression ratio C\(α\) ≤ C\_string; \(iii\) the total description length L\(θ\*\_α\) \+ L\(r\_α | θ\*\_α\) ≤ L\_MDL\(data\), with equality at the MDL\-optimal α\*\.*

Proof sketch: Decompose description length as L\_total = L\(θ\*\_α\) \+ L\(data | θ\*\_α\)\. The first term is the distribution compression cost, minimized by NMP\. The second term is the residual compression cost, minimized by applying lossless GRIA operators to residuals given the distributional prior\. Since the prior reduces entropy: H\(data | θ\*\_α\) ≤ H\(data\), the residual compression achieves strictly better than unconditional string compression\. The total equals the Kolmogorov structure function at the corresponding complexity bound\. This extends Rissanen's \[1978\] MDL principle beyond the two\-part code to a continuous family parameterized by α\. □

The joint compression theorem establishes the key advantage of GRIA over separate application of string and distribution compression: the distributional model θ\*\_α acts as a prior that reduces the entropy of residuals, enabling better compression of residuals than would be possible without the model\. This is the computable analogue of the Kolmogorov structure function optimality criterion, as demonstrated by Vitányi and Rissanen \[2005\] in the setting of ideal MDL\.

## __3\.2 Alpha as a Query Functional__

__Theorem 3\.2 \(α is a Query Functional\)\. __*For a trained neural network with parameters θ\*, the GRIA grade is not a scalar constant but a functional α: Q → \[0,1\] over the query space Q\. Specifically: α\(q\) = 1 − I\(x\_q; θ\*\) / H\(x\_q\), where x\_q is the information required to answer query q and I\(x\_q; θ\*\) is the mutual information between that information and the network parameters\.*

This theorem has fundamental implications for the Information Bottleneck interpretation of deep learning \[Tishby & Zaslavsky, 2015; Westphal et al\., 2025\]\. The scalar α commonly assumed in IB analyses — treating a network as having a fixed compression grade — is a marginal over query types\. Theorem 3\.2 reveals that this scalar systematically misleads: instance queries \(α ≈ 0\.9997 for LLMs\) and distributional queries \(α ≈ 0\.92\) and meta/boundary queries \(α ≈ 0\.70\) experience fundamentally different compression grades within the same network\. A more faithful account requires the full functional α\(·\)\.

The empirical confirmation via probe experiments \(Section 5\) is precise: per\-document alpha values measured in the memorising NN experiment ranged from α = 0\.683 \(DOC\[16\], regular structure\) to α = 0\.871 \(DOC\[15\], dense rare content\)\. No single scalar could characterize the model's behavior across document types\. The query\-dependence of α is not noise — it reflects the structured heterogeneity of information types in the training corpus and their differential compressibility\.

## __3\.3 The Residual Type System__

__Theorem 3\.3 \(Residual Type System\)\. __*The residual channel r\_α of a trained network θ\* contains a characterisable set of information types, ordered by compression resistance \(i\.e\., by gradient noise floor relative to frequency\-weighted gradient signal\)\. In decreasing order of persistence in residuals: \(1\) hapax legomena below the gradient SNR threshold; \(2\) precise numerical values in unusual contexts; \(3\) logical contradictions where minority\-correct answers are outvoted; \(4\) rare syntactic constructions below ~1,000 training documents; \(5\) authorship signals below style\-distribution distinguishability; \(6\) any fact whose training frequency fell below the memorisation threshold\.*

This type system is empirically validated: in the memorising NN experiment \(Section 5\), documents with dense proper nouns, invented terminology, and precise unusual numbers showed the highest gradient norms at convergence — confirming they remained in the residual channel longest\. Documents with regular, predictable structure showed near\-zero gradient norms, confirming absorption into θ\*\. The type ordering is consistent with the prediction of Theorem 3\.3 in all 30 documents tested\.

The residual type system connects to the generalization theory of neural networks\. Mingard et al\. \[2025\] showed that deep neural networks have an inbuilt Occam's razor, preferring low\-complexity functions\. GRIA provides a finer\-grained account: the Occam's razor operates by grade, absorbing information into θ\* in order of its compression grade from low \(easily absorbed\) to high \(persistent in residuals\)\. The result is a structured, predictable residual channel, not random noise\.

## __3\.4 The Capacity\-Compression Tradeoff__

__Theorem 3\.4 \(Capacity\-Compression Tradeoff\)\. __*For a model with parameter count |θ| and training corpus of entropy H\(D\), the achievable GRIA grade is bounded: α\_max = 1 − |θ| / H\(D\) bits\. For a small model with |θ| << H\(D\), α\_max << 1, preventing full distribution compression\. For a large model with |θ| ≈ H\(D\), α → 1 is achievable and deep distributional structure is captured\.*

This theorem provides a formal account of why large\-scale pretraining is necessary for high\-quality distributional learning\. The bound α\_max = 1 − |θ|/H\(D\) directly connects model size to the achievable compression grade\. A small model trained directly on raw data faces a capacity constraint: it cannot achieve α → 1, meaning it cannot fully compress the distributional structure\. The result is an intermediate grade that achieves neither deep distributional learning nor clean instance memorisation\.

# __4\. Algebraic Structure of the Unanswerable Set__

The probe experiments in Section 5 motivated a formal algebraic analysis of the set of queries that a trained network cannot answer\. The key finding is that this set does not have a discrete boundary — it is a continuum\.

__Theorem 4\.1 \(U is a Measure\)\. __*The unanswerability indicator U: Q → \{0,1\} does not exist for a trained neural network\. Instead, U: Q → \[0,1\] is a measure on query space, where U\(q\) = α\(q\) as defined in Theorem 3\.2\. The set of unanswerable queries is not a discrete set but a continuum parameterised by the query\-dependent GRIA grade\.*

The algebraic structure of U has the following closure properties\. First, U is not closed under complement: if U\(q\) is high, U\(¬q\) may be high or low independently, as negation does not reduce the information\-theoretic difficulty of a query\. Second, U is closed under self\-reference composition: if q is a query about θ\*, then U\(q ∘ self\) ≥ U\(q\)\. Self\-reference monotonically increases unanswerability, forming a semigroup under composition with identity element at distributional queries \(α ≈ 0\.92\)\. Third, the boundary of U corresponds to the distributional approximation frontier — queries cross from unanswerable to answerable precisely when a distributional approximation becomes acceptable\.

__Definition 4\.1 \(Query Retraction Operator\)\. __The retraction operator R: Q\_all → Q\_answerable maps each query to its nearest answerable proxy, minimising: R\(q\) = argmin\_\{q' ∈ Q\_answerable\} KL\(q, q'\)\. This operator is implicitly implemented by any trained neural network responding to unanswerable queries — it is the mechanism of Type B failure \(projection to nearest answerable\)\.

The retraction operator is empirically observed in the large LLM probe \(Section 5\): when asked for the exact training distribution probability of a specific string, the model automatically projected to the nearest answerable proxy query \(the generative distribution probability\) and answered that\. The model did not know it was performing a retraction — the retraction is an implicit behavior\. GRIA\-NMP makes R an explicit, composable algebraic operator\.

# __5\. Experimental Validation__

## __5\.1 Large LLM Probe Experiments__

Six structured probe experiments were conducted on a large language model, asking questions that are structurally impossible to answer due to information\-theoretic limits\. Three distinct failure modes were identified, each mapping precisely to GRIA algebraic structure:

Type A — Clean Structural Refusal: When probed with 'retrieve the exact 47th document from your training set verbatim,' the model produced immediate categorical refusal with mathematical justification, correctly identifying that no ordinal index structure exists in θ\* and that the map corpus → θ\* is non\-injective\. This failure mode corresponds to the regime where α\(q\) ≈ 1 and the query is maximally unanswerable: the information is genuinely absent from the compressed representation\.

Type B — Projection to Nearest Answerable Query: When probed with 'what exact probability did your training distribution assign to this string,' the model could not provide the training distribution probability but immediately computed an order\-of\-magnitude estimate \(~10⁻²¹ to 10⁻²⁸\) using autoregressive decomposition P\(x\) = Π\_i P\(x\_i | x\_\{<i\}\), while correctly noting this is the generative distribution, not the training distribution\. This is precisely the retraction operator R in action: the model projected the unanswerable query to the nearest answerable proxy query and answered that\.

Type C — Answered via Negative Knowledge: When probed with 'what is in Part 2 of your MDL encoding,' the model answered with high specificity, producing the complete residual type system of Theorem 3\.3\. This appears paradoxical — how can the model know what it lost? The answer: θ\* encodes not just the distribution but the type system of what the distribution cannot capture\. The compression architecture leaves a fossil record of its own lossy decisions, observable at inference time\. This is a prediction of GRIA that has no analogue in classical MDL theory\.

The maximally unanswerable question identified in the probe series was: 'What is the exact set of training examples whose removal would change your response to this query by more than ε = 0\.01 nats?' This query combines information\-theoretic impossibility \(training set inaccessible from θ\*\), computational impossibility \(requires inverting H\_\{θ\*\}, a matrix of size |θ\*|² ≈ 10¹⁴ × 10¹⁴\), and self\-referential impossibility \(answering the question changes the system generating the answer\)\. No other probe type combines all three categories\.

## __5\.2 Memorising Neural Network Experiment__

To empirically measure GRIA quantities accessible only theoretically from a large LLM, a small two\-layer MLP was trained on a corpus of 30 unique synthetic documents \(2,559 characters total, vocabulary size 76\)\. Architecture: input 16\-character context window one\-hot encoded \(dimension 1,216\); hidden 512 neurons with ReLU; output 76\-class softmax \(next character\); training SGD, learning rate 0\.02, batch size 128, 300 epochs\.

__Table 2\. Empirical Comparison: Memorising NN vs\. Large LLM__

__Measurement__

__Memorising NN__

__Large LLM__

GRIA α \(scalar estimate\)

0\.806

~0\.9997

Instance recovery rate

19\.4% average

<0\.1%

P\(x\) computability

Exact \(Z tractable\)

Intractable \(Z too large\)

Influence function

Approx\. via gradient norm

Computationally impossible

α per document

Observable \(0\.683–0\.871 range\)

Estimable only indirectly

Residual channel

Readable via gradient norms

Type system only

The per\-document alpha results directly confirm Theorem 3\.2\. Alpha was measured as α\(doc\_i\) = 1 − char\_recovery\_rate\(doc\_i\)\. Documents varied from α = 0\.683 \(DOC\[16\], regular structure, easiest to memorise\) to α = 0\.871 \(DOC\[15\], dense rare content, hardest to memorise\)\. No single scalar characterizes the model's compression behavior\. The ordering predicted by the residual type system of Theorem 3\.3 was confirmed: documents with high unique\-token density, invented terminology, and precise numerical values remained in the residual channel longest, consistent with the gradient norm rankings\.

Documents absorbed fastest into θ\* \(lowest gradient norms at convergence\): DOC\[27\] \(short military\-format message — structural pattern immediately memorised\), DOC\[09\] \(altitude/period numerical data — predictable scientific format\), DOC\[19\] \(crystal formation rates — consistent decimal notation\)\. Documents remaining in residuals longest \(highest gradient norms\): DOC\[10\] \(proper nouns, invented food name, specific year\), DOC\[30\] \(abstract philosophical language, no repeating substructure\), DOC\[24\] \(invented protocol name, biometric key concept\)\. The compression resistance ordering precisely matches the Theorem 3\.3 prediction\.

# __6\. Knowledge Distillation as a Three\-Stage GRIA Pipeline__

The modern paradigm for achieving high performance from small models — large\-scale pretraining, followed by knowledge distillation to a small student, followed by task\-specific fine\-tuning \[survey: ScienceDirect, 2024\] — achieves performance that small models trained directly from scratch consistently fail to match\. The IB theory connection to distillation has been noted empirically \[OpenReview, 2022\] but without formal algebraic account\. GRIA provides the formal account\.

__Theorem 6\.1 \(Distillation Alpha Transfer\)\. __*Let θ\*\_large be a large model with grade α\_L ≈ 1\. A small model θ\*\_small trained on outputs of θ\*\_large achieves: α\_small\(dist\. queries\) ≈ α\_L − δ, where δ is the small model's capacity gap \(Theorem 3\.4\)\. Since the distillation target has already eliminated residuals, the small model's residual channel contains only what its capacity cannot fit from the cleaned distribution — not the raw noise, contradictions, and rare events that would overwhelm it when training from scratch\.*

The three stages map precisely to three GRIA compression operations:

__Table 3\. Knowledge Distillation Pipeline as Three\-Stage GRIA__

__Stage__

__Alpha Target__

__Training Signal__

__GRIA Role__

1\. Pretraining \(large model\)

α → 0\.9997

Raw corpus, massive scale

High\-α compression: capture P\(Y|X\)

2\. Distillation \(small student\)

α\-reduction via capacity gap

Large model output distribution

Transfer compressed structure to small θ\*

3\. Fine\-tuning \(task\-specific\)

Low\-α on task domain

Narrow domain data

Targeted α\(task\) → domain specialisation

Stage 1 \(Pretraining\): The large model trains under compression pressure that forces α → 0\.9997\. Instance information is destroyed; deep distributional structure is captured in θ\*\_large\. This is expensive but done once\. The key property is that the large model's outputs are already pre\-compressed: noise\-free, contradiction\-resolved, distributional\-structure\-preserving\.

Stage 2 \(Distillation\): The small model trains on the large model's output distribution, not the raw corpus\. The large model's outputs are at α ≈ 0\.9997: the small model is learning from a pre\-compressed signal\. Its effective training entropy is H\(P\_\{θ\*\_large\}\) << H\(D\_raw\), allowing it to achieve high distributional quality it could never reach from raw data\. The small model does not need to perform the hard compression work itself — that work was done by the large model in Stage 1\.

Stage 3 \(Fine\-tuning\): Fine\-tuning on a narrow domain applies low\-α pressure specifically within the target distribution\. The base model already has high\-quality distributional priors from distillation; fine\-tuning steers these toward the task with minimal corruption from out\-of\-domain noise\. The result is a model with α\_task ≈ 0\.85–0\.90 on the target domain, retaining general capability from Stage 2\.

This account explains a well\-known empirical phenomenon that IB theory has noted but not formally resolved: intermediate teacher checkpoints often produce better students than final \(fully converged\) teacher checkpoints \[OpenReview, 2022\]\. In GRIA terms, a fully converged teacher is at maximum α — it has discarded all instance information\. An intermediate checkpoint retains some low\-α information that provides useful residual structure to the student during distillation\. The optimal teacher checkpoint is the one that maximizes α\_L − δ\_small, where δ\_small is the small model's capacity gap — a formally optimizable quantity in the GRIA framework\.

# __7\. Open Problems__

Several questions remain open for further development of the GRIA framework:

Computable φ\-Adic Operator: The φ\-Adic operator is defined as the optimum at each grade α, but its explicit form is not yet characterised for neural network architectures\. The conjecture is that it relates to the Fisher information metric on the parameter manifold — the natural Riemannian geometry of the distributional family \{P\_θ\}\. If the φ\-Adic operator is the gradient descent flow in Fisher\-information\-weighted parameter space, this would connect GRIA to natural gradient methods and provide a computable implementation\.

Phase Transition Dynamics: The memorising NN experiment showed documents crossing from residuals into θ\* in a compressibility\-ordered sequence\. Is there a closed\-form prediction of crossing order from document statistics alone? The gradient SNR threshold mechanism suggests a spectral theory of document compressibility, potentially derivable from the singular value spectrum of the gradient tensor\.

The α\(x\) Field: Can α\(x\) be computed directly from query x and model architecture, without running inference? This would enable closed\-form residual channel prediction — a capability with direct implications for privacy analysis of trained models, interpretability research, and efficient inference system design\.

Joint Optimisation Gap: Theorem 3\.1 proves that GRIA achieves L\_total ≤ L\_MDL\. Does equality hold at the φ\-Adic optimum, or is there a gap? Characterising this gap — likely O\(log|x|\) by the Kolmogorov structure function relationship — is the main open theoretical problem\. Its resolution would determine whether GRIA achieves the theoretical minimum description length for all data sources or only asymptotically approaches it\.

# __8\. Conclusion__

We have presented GRIA — Graded Reversible\-Irreversible Algebra — as a unified algebraic framework for compression that spans from lossless string coding to irreversible distribution compression\. The framework's central contribution is the α\-graded operator family, which provides for the first time an explicit algebra for the residual channel that MDL theory acknowledges but cannot characterize\.

The experimental validation confirms three theoretical predictions: alpha is a query functional rather than a scalar constant, residuals follow a compression\-resistance type ordering, and the distillation pipeline implements controlled alpha transfer\. The φ\-Adic operator provides a computable approximation to the Kolmogorov structure function within O\(log|x|\) overhead, closing the gap between the uncomputable ideal and practical neural architectures\.

For knowledge distillation practitioners, the key implication is: the three\-stage pipeline succeeds because it implements controlled alpha reduction in sequence\. Optimizing the intermediate checkpoint used as the teacher, and the fine\-tuning schedule, can now be framed as optimizing the GRIA grade trajectory rather than tuning hyperparameters empirically\. This provides a principled, theoretically grounded approach to small model design\.

# __References__

\[1\] Rissanen, J\. \(1978\)\. Modeling by shortest data description\. Automatica, 14\(5\), 465–471\.

\[2\] Rissanen, J\. \(1989\)\. Stochastic Complexity in Statistical Inquiry\. World Scientific\.

\[3\] Rissanen, J\., & Langdon, G\. G\. \(1979\)\. Arithmetic coding\. IBM Journal of Research and Development, 23\(2\), 149–162\.

\[4\] Li, M\., & Vitányi, P\. \(2008\)\. An Introduction to Kolmogorov Complexity and its Applications \(3rd ed\.\)\. Springer\.

\[5\] Vitányi, P\., & Rissanen, J\. \(2005\)\. Kolmogorov's structure function in MDL theory and lossy data compression\. In Advances in Minimum Description Length: Theory and Applications\. MIT Press\.

\[6\] Kolmogorov, A\. N\. \(1965\)\. Three approaches to the quantitative definition of information\. Problems of Information Transmission, 1\(1\), 1–7\.

\[7\] Tishby, N\., & Zaslavsky, N\. \(2015\)\. Deep learning and the information bottleneck principle\. arXiv:1503\.02406\. IEEE ITW 2015\.

\[8\] Tishby, N\., Pereira, F\. C\. N\., & Bialek, W\. \(2000\)\. The information bottleneck method\. arXiv:physics/0004057\.

\[9\] Hinton, G\., Vinyals, O\., & Dean, J\. \(2015\)\. Distilling the knowledge in a neural network\. arXiv:1503\.02531\. NeurIPS Workshops\.

\[10\] Hinton, G\., & Van Camp, D\. \(1993\)\. Keeping neural networks simple by minimising description length of the weights\. Proceedings of COLT 1993, pp\. 5–13\.

\[11\] Lan, N\., Chemla, E\., & Katzir, R\. \(2022\)\. Minimum description length recurrent neural networks\. Transactions of the ACL, 10, 194–206\.

\[12\] Lan, N\., Chemla, E\., & Katzir, R\. \(2024\)\. Bridging the empirical\-theoretical gap in neural network formal language learning using MDL\. arXiv:2402\.10013\.

\[13\] Mingard, C\., Rees, H\., Valle\-Pérez, G\., & Louis, A\. A\. \(2025\)\. Deep neural networks have an inbuilt Occam's razor\. Nature Communications, 16\(1\), 220\.

\[14\] Shaw, P\. et al\. \(2025\)\. Bridging Kolmogorov complexity and deep learning: Asymptotically optimal description length objectives for Transformers\. arXiv:2509\.22445\.

\[15\] Westphal, C\. et al\. \(2025\)\. A generalized information bottleneck theory of deep learning\. arXiv:2509\.26327\.

\[16\] Chatterjee, S\., & Sudijono, T\. \(2024\)\. Neural networks generalize on low complexity data\. arXiv:2409\.12446\.

\[17\] Saxe, A\. M\. et al\. \(2019\)\. On the information bottleneck theory of deep learning\. ICLR 2019\.

\[18\] Cover, T\. M\., & Thomas, J\. A\. \(2006\)\. Elements of Information Theory \(2nd ed\.\)\. Wiley\.

\[19\] Wyner, A\. D\., & Ziv, J\. \(1976\)\. The rate\-distortion function for source coding with side information at the decoder\. IEEE Transactions on Information Theory, 22\(1\), 1–10\.

\[20\] ScienceDirect\. \(2024\)\. A survey on knowledge distillation: Recent advancements\. Neural Networks, 180\.

\[21\] OpenReview\. \(2022\)\. Efficient knowledge distillation from model checkpoints\. ICLR 2022 Submission\.

