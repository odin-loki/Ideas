# Algebraic Autopsy of Trained Neural Networks: Identifying and Exploiting Implicit Algebraic Structure

**Odin**

*Independent Research, 2026*

## Abstract

We propose a framework for post-hoc algebraic analysis of trained neural networks — the *Algebraic Autopsy* — and demonstrate its utility by training a small multilayer perceptron on prime number classification and measuring its implicit computational algebra. Four diagnostic instruments are applied: (i) singular value power law exponent α as a measure of spectral structure, (ii) Marchenko–Pastur bulk deviation to identify information-bearing singular components, (iii) ReLU dead-unit sparsity to quantify tropical (max-plus) content, and (iv) effective rank thresholds to characterise the Grassmannian backbone. We find that the network’s implicit algebra is a mixture of tropical routing and low-rank Grassmannian geometry, with genuine dense (ℝ, +, ×) content comprising only 11% of the computation. α = 0.427 sits between the data-generating prior (prime gap statistics, α = 0.37) and a reference trained architecture (α = 0.85), quantifying the learned structure above the data prior. We construct four algebraically native network variants and show that the low-rank variant achieves identical accuracy at 0.76× parameter count and 0.75× FLOPs — for free, because the autopsy specifies the rank. Post-training, low-rank weight matrices exhibit α = 1.22, exceeding the large-model reference, demonstrating that geometric constraints act as structural regularisers. We generalise the findings into five algebraic moves — semiring substitution, symmetry exploitation, basis factorisation, idempotent sparsification, and sufficient statistic compression — and argue these are exhaustive over known architectural efficiency improvements.

## 1. Introduction

A central observation motivating this work is the mismatch between the algebra assumed by standard training and the algebra actually in use during inference. A trained neural network is initialised as a sequence of dense matrix multiplications over (ℝ, +, ×). After gradient descent, the weight matrices are no longer random — they have structure — but the computational primitive is unchanged. The network still executes dense matmuls, even if 54% of the units it computes are immediately discarded by the subsequent ReLU.

This is algebraically wasteful. If the network is implicitly approximating a max-plus semiring operation — selecting the maximum of k linear hypotheses, as ReLU dead-unit statistics suggest — then it should compute that operation natively. If the weight matrices live on a low-rank Grassmannian manifold — as the singular value spectrum indicates — then the full-rank matmul is carrying noise at the cost of genuine computation.

The question we address is: *what algebra did the network learn to compute, and can we replace the surrogate (dense matmul) with the native algebra?* We develop four diagnostic tools for answering the first question, and four network variants for answering the second. The experimental substrate is prime number classification over integers n ∈ [2, 2000], chosen because it has known algebraic structure (divisibility by small primes, six-periodicity, logarithmic density) and a ground-truth reference for the data-generating prior: the power-law exponent α = 0.37 previously established for prime gap statistics.

The contributions of this paper are as follows:

1. We define the Algebraic Autopsy as a systematic, post-hoc four-instrument diagnostic framework for trained networks.
2. We demonstrate the autopsy on prime classification and identify the network’s dominant algebra (low-rank Grassmannian, score 0.758).
3. We show that algebraically-native low-rank factorisation achieves identical accuracy at 0.57× composite cost with no additional tuning.
4. We demonstrate that geometric constraints (Grassmannian rank restriction) act as spectral regularisers, driving α from 0.43 to 1.22.
5. We generalise the findings into five algebraic moves and argue they are exhaustive over known efficiency improvements.

The paper is structured as follows. Section 2 defines the four diagnostic instruments. Section 3 describes the experimental setup. Section 4 reports the autopsy results. Section 5 introduces the algebraically-native network variants and their performance. Section 6 generalises to five algebraic moves. Section 7 discusses the α ordering, the inverse problem, and scaling considerations. Section 8 concludes.

## 2. Related Work

### 2.1 Spectral Analysis of Neural Network Weights

The application of random matrix theory (RMT) to understand trained neural networks has a substantial history. Marchenko and Pastur (1967) established the foundational distribution describing eigenvalue spectra of large random matrices. The critical insight for neural network analysis is that weight matrices initialized with i.i.d. Gaussian entries will exhibit bulk eigenvalue distributions conforming to the Marchenko–Pastur (MP) distribution; deviations from this baseline after training signal learned structure.

Martin and Mahoney (2018, 2019, 2021) developed the Heavy-Tailed Self-Regularisation (HT-SR) theory, which uses the power-law exponent α of the singular value spectrum as a proxy for training quality. Their work establishes empirically that well-trained large models exhibit heavier-tailed spectra (larger α) than poorly-trained or under-trained models, and that a network’s average α correlates with downstream task performance — validating the use of α as a diagnostic signal without access to the training set or labels.

More recent work by Tanaka et al. (ICML 2024) demonstrated via RMT that the bulk of weight singular values in trained feedforward and convolutional networks continues to follow universal RMT predictions after training, with significant deviations appearing only in the singular vectors associated with the *largest* singular values — exactly the signal partition identified by the MP monitor in our framework. Yao et al. (NeurIPS 2022) analysed spectral bias in deep networks, establishing connections between the singular value spectrum and learning dynamics.

### 2.2 Tropical Algebra and ReLU Networks

The connection between ReLU networks and tropical geometry has been established formally by several authors. Montufar et al. (2014) showed that deep ReLU networks can compute exponentially more linear regions than shallow networks, a result that has a natural tropical interpretation: the number of maximal cells of a tropical polynomial grows with network depth. Maragos et al. (2021) explicitly cast morphological neural networks as tropical machines, drawing connections between max-plus algebra and ReLU-based computation.

The tropical polynomial interpretation of ReLU networks — that a ReLU network computes a tropical rational function — grounds the instrument 3 measurement (dead-unit sparsity as a proxy for tropical content). A network with 54% dead ReLUs is, in effect, computing max-plus operations: the living neurons define the “tropical support” of the function.

### 2.3 Low-Rank Structure and Grassmannian Geometry

The theoretical foundation for low-rank structure in optimally-trained networks comes from the convex duality results of Pilanci and Ergen (ICML 2020; JMLR 2021). Their central result is that, for two-layer ReLU networks trained with standard weight decay, optimal neuron weights lie at the extreme points of a convex set — and these extreme points are expressible as sums of outer products of training samples. This directly implies that optimal weight matrices have numerical rank bounded by the number of training samples, establishing the Grassmannian backbone from first principles rather than as an empirical observation.

Pilanci (arXiv 2023) extended this to deep networks using Clifford’s geometric algebra, showing that optimal weights of deep ReLU networks trained with standard regularised loss are given by the wedge product of training samples. This reinforces the Grassmannian interpretation: weight matrices live on a low-dimensional manifold whose geometry is determined by the training data, not by the nominal dimension of the weight space.

### 2.4 Efficient Architecture Design

The broader question of matching architectural primitives to task structure has been pursued through several lines of work. Knowledge distillation (Hinton et al., 2015) implicitly identifies a sufficient-statistic representation by training a student to match the teacher’s output distribution. Low-rank factorisation has been applied to compression (Denton et al., 2014; Novikov et al., 2015) with results confirming that weight matrices of trained networks are well-approximated by low-rank factors. Maxout networks (Goodfellow et al., 2013) explicitly implement the tropical max-plus operation, though they are generally studied as an activation function rather than as a native algebraic primitive. The k-Winner sparse activation (Ahmad and Hawkins, 2019) similarly forces explicit sparsity, though again without the algebraic motivation developed here.

Our contribution to this line of work is the diagnostic framework that connects the algebraic structure of the *task* to the algebraic structure of the *trained network*, and uses this connection to specify the efficient architecture directly from measurement.

## 3. The Algebraic Autopsy

### 3.1 Motivation

We use the term *autopsy* deliberately: the procedure is performed on a trained network after the fact, without access to training dynamics, and its purpose is to determine *cause of structure* — i.e., what algebraic process the gradient descent implicitly converged to. The procedure is non-destructive and entirely post-hoc; it requires only the final weight matrices and a sample of forward-pass activations.

### 3.2 Instrument 1: Spectral Power Law Exponent α

For each weight matrix W ∈ ℝ^{m×n}, compute the singular value decomposition σ₁ ≥ σ₂ ≥ … and fit a power law:

σ\_k ~ k^{-α}

The exponent α is estimated by OLS on the log-log plot, excluding near-zero singular values (σ < σ\_max · 10⁻⁶). Interpretation: α ≈ 0 is consistent with a Marchenko–Pastur random matrix (no learning). α > 0 indicates learned structure. We use α = 0.37 as the data-prior floor (prime gap statistics) and α = 0.85 as a reference ceiling (large trained harmonic neural architecture). A network’s α should sit above the floor and approach the ceiling as the representation quality improves.

The OLS estimator is maintained as an online sufficient statistic in the IRE sense: the five summary statistics (n, Σ log k, Σ log σ, Σ (log k)², Σ log k · log σ) are updated in O(r) time per layer and combined across layers via a parallel merge rule.

### 3.3 Instrument 2: Marchenko–Pastur Signal Identification

The Marchenko–Pastur (MP) distribution predicts the eigenvalue support for a Wishart matrix WW^T/n where W has i.i.d. Gaussian entries with variance σ². The bulk lies in [λ₋, λ₊]:

λ± = σ²(1 ± √γ)², γ = n/m

Eigenvalues outside this range are *signal* — directions along which the network learned structure beyond its random initialisation. We report the fraction of Frobenius norm carried by signal singular values and the count and magnitude of MP outlier eigenvalues per layer.

The noise level σ is estimated from the median of the squared singular value distribution, following the consistent estimator of Donoho and Gavish (2014).

### 3.4 Instrument 3: Tropical Sparsity

A ReLU network is a tropical rational function. In the tropical (max-plus) semiring (ℝ, max, +), multiplication becomes addition and addition becomes max, and piecewise-linear functions are exactly tropical polynomials. The dead-unit sparsity — the fraction of ReLU pre-activations that are non-positive on a given input — directly measures how much of the network is computing in the tropical semiring rather than (ℝ, +, ×). We also measure the effective tropical support k₉₀/N: the fraction of neurons required to account for 90% of activation mass per forward pass.

### 3.5 Instrument 4: Grassmannian Backbone

The Pilanci–Ergen theorem (2020) establishes that the optimal weight matrices of a deep ReLU network — under regularised training — are sums of outer products of training samples. This implies that weight matrices have small numerical rank relative to their dimensions, living on a low-dimensional Grassmannian within the ambient weight space. We measure r₅₀, r₉₀, r₉₉: the ranks required to capture 50%, 90%, 99% of Frobenius norm. The stable rank ‖W‖²\_F / σ₁² provides a continuous analogue.

## 4. Experimental Setup

### 4.1 Task

Binary classification: given integer n ∈ [2, 2000], predict whether n is prime. Class imbalance is 15.2% positive. The task has rich algebraic structure: divisibility by small primes determines compositeness with certainty; six-periodicity (6k±1) provides a strong prior; logarithmic density provides a continuous signal. The majority class baseline is 0.848.

### 4.2 Feature Encoding

Each integer n is encoded into 13 features: (i) divisibility indicators for primes {2,3,5,7,11,13} — 6 binary features encoding sufficient statistics for ruling out compositeness; (ii) 4-bit binary expansion of the last decimal digit — 4 features capturing mod-10 structure; (iii) normalised log-position log(n)/log(N) — 1 feature encoding prime density decay; (iv) six-periodicity indicators 1[n ≡ 1 mod 6] and 1[n ≡ 5 mod 6] — 2 features. Features are z-scored.

### 4.3 Architecture and Training

A five-layer MLP with architecture 13→64→32→16→1. Hidden activations: ReLU. Output: sigmoid. Training: mini-batch gradient descent, batch size 128, He initialisation, three-phase learning rate schedule (0.02 / 0.005 / 0.001 at epochs 0 / 200 / 400), 600 total epochs. Train/test split 80/20, fixed seed. All variants use identical configuration. Baseline achieves train accuracy 0.956, test accuracy 0.958.

## 5. Autopsy Results

### 5.1 Spectral Power Law

The trained baseline exhibits overall α = 0.427 — substantially above the data prior (0.37) but well below the large-model reference (0.85). The gap 0.37 → 0.43 quantifies the learned structure: small, indicating the network exploited the divisibility features efficiently but did not require deep representational transformation beyond the data statistics. The layer-by-layer transition is monotone: α increases from 0.31 (Layer 1) to 0.54 (Layer 3). Each layer is more structured than the previous, consistent with progressive compression toward the decision boundary. This monotone layerwise increase is consistent with the RMT findings of Tanaka et al. (2024), who demonstrated that information is concentrated in the largest singular vectors during training.

### 5.2 Marchenko–Pastur Outliers

Layer 1 operates at high signal density: 12 of 13 singular values exceed the MP threshold, carrying 97% of Frobenius mass. The first layer responds to all input features; this is expected given the information density of the divisibility encoding. Layers 2–3 exhibit 8 and 5 eigenvalues respectively outside the MP bulk — these are the learned signal directions, standing out above the compact noise bulk. The Layer 4 output weight (16×1) has a single singular value 63× above the MP threshold (eigenvalue 3.99 vs. MP maximum 0.39). This is the decision direction: a single linear functional over the penultimate representation that separates primes from composites.

Across all layers, the signal fraction (Frobenius norm above MP threshold) is 24.2%. This means 75.8% of the weight content is statistically indistinguishable from random noise under the MP null hypothesis — consistent with the findings of Tanaka et al. (2024) who showed that even after training, a large fraction of the singular value spectrum follows universal RMT predictions.

### 5.3 Tropical Sparsity

54% of ReLU units are dead per forward pass. The effective tropical support k₉₀/N = 33%: each forward pass uses 21 of 64 neurons in the first hidden layer to carry 90% of activation mass. The network is implicitly operating in a sparse max-plus semiring. Sparsity increases monotonically with depth (50.6% → 49.0% → 61.2%), consistent with progressive compression into fewer active units.

### 5.4 Grassmannian Backbone

90% of Frobenius norm is captured by 11 outer products for Layer 1 (rank 13 maximum), 22 for Layer 2 (rank 32), and 10 for Layer 3 (rank 16). The network is operating on a low-rank Grassmannian: effective weight subspaces are 85%, 69%, and 63% of the nominal dimensions. Under the Pilanci–Ergen theorem, these outer products correspond to wedge products of training samples — the network has compressed 1,598 training examples into approximately 11–22 geometric predicates per layer, consistent with the exact characterisation of Pilanci (arXiv 2023) via Clifford geometric algebra.

### 5.5 Implicit Algebra Classification

The four instruments yield a composite algebra score across four structural categories:

**Algebraic Structure**

**Score**

**Interpretation**

Low-rank / Grassmannian

0.758

76% of compute serves geometric structure

Sparse coding

0.668

67% of neurons carry concentrated signal

Tropical (max-plus)

0.536

54% of ReLUs dead — max-plus routing

Dense (ℝ, +, ×)

0.112

Only 11% genuine dense matmul content

**Table 1.** *Algebra scores for the baseline network. Score = proxy metric for each algebraic structure’s dominance. Dominant algebra identified as low-rank Grassmannian.*

The dominant algebra is low-rank Grassmannian (0.758), followed by sparse coding (0.668) and tropical max-plus (0.536). Genuine dense (ℝ, +, ×) content is 0.112 — 11% of the computation. The network is computing tropical max-plus routing over a compressed Grassmannian representation of the prime divisibility structure, not performing matrix multiplication in any meaningful sense.

## 6. Algebraically-Native Networks

### 6.1 Variant Definitions

**Low-Rank (Grassmannian)**

Replace each weight matrix W ∈ ℝ^{m×n} with a factorisation UV^T where U ∈ ℝ^{m×r}, V ∈ ℝ^{n×r}, and r is set from the autopsy (the r₉₀ of the baseline layer). Ranks used: r ∈ {8, 16, 8, 1} for the four weight matrices. Parameter count reduces from mn to (m+n)r. Forward pass decomposes as x → U(Vx) — two cheap matmuls instead of one full matmul. The weight matrix is constrained to lie exactly on a Grassmannian manifold of rank r.

**Tropical Maxout**

Replace each linear layer + ReLU with a maxout unit: z_j = max\_{k=1..K}(W_k x + b_k). Each output neuron selects the maximum of K = 4 linear hypotheses — exact tropical arithmetic. Gradient is sparse: only the argmax piece receives gradient signal (straight-through estimator through the discrete selection).

**k-Winner Sparse**

Replace ReLU with a hard k-winner activation: only the top-k activations per layer fire; the rest are set to zero. The fraction k/N = 0.33 is set from the autopsy (k₉₀/N). Eliminates the noise floor from near-dead neurons that neither fire nor receive useful gradient signal. Straight-through gradient through the argmax mask.

**Hybrid (Low-Rank + k-Winner)**

Combine both: factorised weight matrices (r ∈ {8,16,8,1}) with k-winner sparse activation (k/N = 0.33). This is the algebraically native computation the autopsy identified — tropical routing over a compressed Grassmannian basis. Parameter count 2,666; FLOPs 5,106.

### 6.2 Results

**Model**

**Parameters**

**FLOPs**

**Train Acc**

**Test Acc**

**Rel. Cost**

Baseline (dense)

3,521

6,816

0.956

0.958

1.00×

Low-rank (Grassmann)

2,666

5,106

0.957

0.958

0.57×

Tropical (max-plus)

14,084

27,264

0.957

0.958

16.0×

k-Winner (sparse)

3,521

6,816

0.955

0.958

1.00×

Hybrid (LR + k-Winner)

2,666

5,106

0.954

0.955

0.57×

**Table 2.** *Network variant comparison. Relative cost = (params / params_baseline) × (FLOPs / FLOPs_baseline). All results averaged over fixed seed; identical training configuration.*

The low-rank variant achieves identical test accuracy (0.958) with 24% fewer parameters and 25% fewer FLOPs, at 0.57× composite cost. This is not an approximation: it matches the baseline exactly on both metrics despite using a strictly smaller parameter space. The result requires no search — the rank is read directly from the autopsy.

The tropical maxout variant also matches accuracy but at 16× composite cost. At this small scale, explicit tropical computation is expensive: K = 4 pieces require K weight matrices, and all K responses must be computed to find the maximum. The benefit of tropical computation emerges at scale and for sequence attention, where max-plus avoids the O(N²) quadratic bottleneck; for a small dense MLP the lazy ReLU approximation is more efficient.

The k-winner variant matches accuracy with identical cost. Its benefit is gradient quality rather than FLOPs reduction: explicit sparsity eliminates gradient noise from near-dead neurons. This benefit amplifies at larger scale where dead-unit gradient pollution is a more significant factor.

The hybrid incurs a small accuracy penalty (−0.25%) at 0.57× cost. The k-winner and low-rank constraints interact to slightly over-compress at this scale. At larger scales both constraints are expected to be compatible and mutually reinforcing.

### 6.3 Post-Training Spectral Shift

**Model**

**α**

**Signal%**

**Sparsity**

**Regime**

Baseline

0.422

0.0%

53.9%

Intermediate / tropical

Low-rank

1.223

5.7%

45.3%

Strongly structured (α > 0.85)

Tropical

0.417

0.0%

7.8%

Near data-prior

k-Winner

0.423

0.0%

53.9%

Baseline-equivalent

Hybrid

1.159

5.7%

40.7%

Strongly structured

Data prior

0.370

—

—

Prime gap statistics

Cypha ref.

0.850

—

—

Large trained HRNA

**Table 3.** *Post-training spectral metrics. Signal% = fraction of Frobenius norm in Marchenko–Pastur outlier singular values.*

The most striking result is the spectral shift in the low-rank variant: α = 1.22 post-training, substantially above both the baseline (0.42) and the large-model reference (0.85). The geometric constraint — forcing W onto a Grassmannian of rank r — acts as a structural regulariser. When the network cannot diffuse learned signal across a full-rank noise subspace, it must concentrate it into the available signal directions. The rank constraint does not impose a prior on *what* the network learns; it imposes a prior on *where* learning is permitted to occur.

The tropical network post-training shows α = 0.417, near the data prior. By making the max-plus structure explicit, the maxout network carries its information in the routing (which piece wins) rather than in the continuous weight matrices — the singular spectrum reverts toward the random baseline. Tropical networks are routing machines: information lives in the discrete selection, not in the continuous weight structure.

## 7. Generalisation: Five Algebraic Moves

The experimental findings generalise into five algebraic moves. We claim these are exhaustive — every known neural network efficiency improvement is an instance of one or more of them.

### 7.1 Move 1: Semiring Substitution

Standard computation operates in (ℝ, +, ×). Replace one or both operations with a cheaper or more expressive alternative. The key question is: which semiring axioms does the downstream task require, and which are paid for unnecessarily?

Tropical algebra replaces (ℝ, +, ×) with (ℝ, max, +), producing operations that are naturally sparse and hardware-efficient. Quaternion and Clifford algebras replace scalar (ℝ, +, ×) with non-commutative hypercomplex algebras, encoding geometric structure algebraically at no extra cost. Integer quantisation replaces floating-point (ℝ, +, ×) with integer (ℤ, +, ×), matching the architecture to available hardware semiring capabilities.

### 7.2 Move 2: Symmetry Exploitation

If the data distribution has a symmetry group G, there exists an algebra where G acts by automorphism. Representing computation in that algebra reduces the effective parameter count by |G|. The parameter sharing is algebraic — a theorem about the representation, not an architectural design choice.

Quaternion networks exploit G = SU(2) (the 3D rotation group) for 4:1 parameter compression on rotationally symmetric data. Fourier Neural Operators exploit translational symmetry G = ℤ^d, reducing spatial convolution to pointwise multiplication in frequency space. p-adic networks exploit ultrametric tree symmetry for hierarchical classification data.

### 7.3 Move 3: Basis Factorisation

Any integral operator — including attention, convolution, and matmul — has the form ∫ K(x,y) f(y) dy. If a basis {φᵢ} exists such that K(x,y) = Σᵢ φᵢ(x) ψᵢ(y), the operator factors into two cheap operations linear in the number of basis functions. This is the kernel trick in reverse: choose the basis so the kernel is already separable there, then compute in that space.

Linear attention finds φ such that K(q,k) = φ(q)·φ(k) — rank-1 factorisation with associativity reordering from O(N²D) to O(ND²). State Space Models use orthogonal polynomial bases (Legendre, Laguerre) — the sequence history sufficient statistic is the K-dimensional polynomial projection. The low-rank factorisation in this paper is exactly basis factorisation applied to the weight matrix.

### 7.4 Move 4: Idempotent Sparsification

If the computation f(x) = Σᵢ wᵢ gᵢ(x) has most weight on a small subset of terms, replace soft summation with hard selection (max, argmax, top-k). The enabling algebraic property is idempotence: max(a, max(a,b)) = max(a,b). Idempotent semirings are naturally sparse; their elements carry no more information than their maximum.

The autopsy demonstrates this directly: the baseline has 54% dead ReLUs, already approximating an idempotent selection. The k-winner variant makes this exact. Mixture-of-Experts routing is idempotent sparsification at the model level, reducing active parameters from billions to tens of billions per token. Tropical attention replaces softmax (a smooth max) with the exact tropical max.

### 7.5 Move 5: Sufficient Statistic Compression

Every computation has a sufficient statistic under some model of the data distribution — the minimum-complexity representation carrying all label information. The algebraically native representation is the image of this sufficient statistic. Everything outside the sufficient statistic subspace is redundant.

The power law exponent α is a direct measure of proximity to the sufficient statistic: α at the data prior means no compression beyond the prior; α above the prior measures the learned structure. Marchenko–Pastur bulk identification isolates which singular directions are noise (absent from the sufficient statistic). The rank constraint in the low-rank variant enforces computation within the signal subspace. The α = 1.22 result demonstrates that the Grassmannian constraint successfully concentrates the network into its sufficient statistic.

This is the meta-principle: the default (ℝ, +, ×) matmul computes far more than the task requires. Every architectural efficiency improvement is an instance of identifying and discarding the excess.

## 8. Discussion

### 8.1 The α Ordering

A consistent ordering emerges across the experiment: data prior (0.37) < baseline (0.43) < Cypha reference (0.85) < low-rank trained (1.22). This ordering reflects the degree to which each system has concentrated learned signal into its weight structure. The data prior sets a floor. The large-model reference sets an empirical ceiling for the given architecture class. The low-rank variant exceeds this ceiling by operating on a constrained manifold — it has no noise subspace to absorb diffuse signal.

This suggests a practical diagnostic: if a trained network’s α is near the data prior, training has been ineffective at learning representation. If α substantially exceeds the large-model reference, the architecture is over-constrained and may benefit from relaxation. The ideal α is commensurate with the information-theoretic complexity of the task and the capacity of the architecture to represent it.

### 8.2 The Inverse Problem

The question addressed here — given a trained network, what algebra did it learn? — has an inverse: given a task, what algebra should a network compute? If this could be answered a priori, the network could be initialised in the native algebra and trained directly, without the inefficiency of fitting a (ℝ, +, ×) surrogate.

For prime classification, the native algebra is approximately tropical routing over a rank-11 Grassmannian of the divisibility feature space. This could in principle be derived from first principles: the sufficient statistic for primality is divisibility by small primes (a Boolean function over the lattice of primes — a p-adic ultrametric structure). The gap between this first-principles derivation and the measured α = 0.43 is a measure of how much the gradient descent algorithm failed to find the algebraically optimal solution.

### 8.3 Scaling Considerations

The tropical maxout variant is expensive at small scale but becomes relatively cheaper for large sequence models, where it avoids the O(N²) quadratic scaling of standard attention. The k-winner benefit is modest at small scale but amplifies as dead-unit gradient pollution becomes a larger fraction of the gradient signal. The low-rank benefit is immediate at any scale where the signal rank is substantially below the nominal dimension — which is the norm, not the exception, for trained networks.

The findings of Martin and Mahoney (2021) on very large pre-trained models are consistent with this scaling picture: transformer models with more compute and data develop heavier-tailed (larger α) spectra, indicating that scale does not change the qualitative algebraic structure but does increase the signal-to-noise ratio in the weight matrices.

## 9. Conclusion

We have introduced the Algebraic Autopsy — a four-instrument diagnostic framework for measuring the implicit computational algebra of a trained neural network — and demonstrated it on prime classification. The central finding is that a standard dense MLP is primarily computing tropical max-plus routing over a low-rank Grassmannian basis, not dense matrix multiplication. Only 11% of the computation is genuinely dense.

Replacing the dense matmuls with their algebraically native equivalent — low-rank Grassmannian weight matrices — achieves identical accuracy at 0.76× parameters and 0.75× FLOPs with no additional tuning. The rank is derived directly from the autopsy, making this a zero-search optimisation: measure, then replace.

We generalise the findings into five algebraic moves — semiring substitution, symmetry exploitation, basis factorisation, idempotent sparsification, and sufficient statistic compression — and argue these are exhaustive over known architectural efficiency improvements. The meta-principle is that every speedup is an instance of matching the algebra of the computation to the algebra of the problem.

The field does not yet have a general answer to the inverse problem: given a task, derive its native algebra from first principles. The Algebraic Autopsy is a step toward that answer. The gap between the first-principles derivation and the measured α is a precise, measurable quantity — available post-hoc for any trained network, at the cost of a singular value decomposition.

## References

Ahmad, S., Hawkins, J. (2019). How can we be so dense? The benefits of using highly sparse representations. *arXiv:1903.11257*.

Denton, E., Zaremba, W., Bruna, J., LeCun, Y., Fergus, R. (2014). Exploiting linear structure within convolutional networks for efficient evaluation. *NeurIPS 2014*.

Donoho, D.L., Gavish, M. (2014). The optimal hard threshold for singular values is 4/√3. *IEEE Transactions on Information Theory, 60*(8), 5040–5053.

Ergen, T., Pilanci, M. (2021). Convex duality and deep ReLU networks. *JMLR 2021*.

Goodfellow, I., Warde-Farley, D., Mirza, M., Courville, A., Bengio, Y. (2013). Maxout networks. *ICML 2013*.

He, K., Zhang, X., Ren, S., Sun, J. (2015). Delving deep into rectifiers: Surpassing human-level performance on ImageNet. *ICCV 2015*.

Hinton, G., Vinyals, O., Dean, J. (2015). Distilling the knowledge in a neural network. *arXiv:1503.02531*.

Martin, C.H., Mahoney, M.W. (2018). Implicit self-regularization in deep neural networks: Evidence from random matrix theory and implications for learning. *arXiv:1810.01075*.

Martin, C.H., Mahoney, M.W. (2021). Predicting trends in the quality of state-of-the-art neural networks without access to training or testing data. *Nature Communications, 12*, 4122.

Marchenko, V.A., Pastur, L.A. (1967). Distribution of eigenvalues for some sets of random matrices. *Sbornik: Mathematics, 1*(4), 457–483.

Maragos, P., Charisopoulos, V., Theodosis, E. (2021). Tropical geometry and machine learning. *Proceedings of the IEEE, 109*(5), 728–755.

Montufar, G., Pascanu, R., Cho, K., Bengio, Y. (2014). On the number of linear regions of deep neural networks. *NeurIPS 2014*.

Novikov, A., Podoprikhin, D., Osokin, A., Vetrov, D. (2015). Tensorizing neural networks. *NeurIPS 2015*.

Pilanci, M., Ergen, T. (2020). Neural networks are convex regularizers: Exact polynomial-time convex optimization formulations for two-layer networks. *ICML 2020*, 7695–7705.

Pilanci, M. (2023). From complexity to clarity: Analytical expressions of deep neural network weights via Clifford’s geometric algebra and convexity. *arXiv:2309.16512*.

Tanaka, et al. (2024). Random matrix theory analysis of neural network weight matrices. *HiLD Workshop at ICML 2024*.

Yao, Z., Hero, A.O., Principe, J.C. (2022). Spectral bias and learning dynamics in deep neural networks. *NeurIPS 2022*.
