# The Streaming Geometry Framework: Meta-Patterns in Modern Neural Network Optimization and a Unified Foundation for Efficient AI Systems

**Odin**

*Independent Research — 2026 Working Draft*

## Abstract

We survey sixteen canonical techniques spanning memory-efficient training, numerical stability, kernel fusion, adaptive optimisation, loss landscape dynamics, inference acceleration, and data curation. Through systematic analysis we identify three deep meta-patterns that recur across all levels of the neural network stack: \(I\) *Streaming Sufficiency* — any algorithm that accumulates global batch state can be reformulated as a streaming algorithm that maintains a compact sufficient statistic; \(II\) *Spectral Geometry* — the natural language for weight updates, normalisation, routing, and attention is the singular value spectrum of the relevant operator; and \(III\) *Data–Compute Duality* — every design choice exists on a joint Pareto frontier of data quality, compute budget, and model capacity that must be co-optimised rather than sequentially tuned. We show that these three meta-patterns are not independent: they are projections of a single underlying principle we term *Incremental Riemannian Estimation* \(IRE\). From IRE we derive the Streaming Geometry Framework \(SGF\), a modular AI system architecture in which every component — optimiser, normaliser, router, scheduler, memory manager, and inference engine — is an instance of the same algebraic primitive: an online sufficient statistic on a curved parameter manifold. We provide a complete C\+\+17/CUDA implementation of SGF \(the sgf\_lib library\), derive theoretical predictions, and outline a research programme for validating the framework experimentally. The SGF library implements all novel predictions, including ZClip-triggered automatic WSD cooldown, EoS-adaptive checkpointing, spectral health monitoring derived from the Algebraic Autopsy, and algebra-aware layer primitives.

## 1. Introduction

The history of practical deep learning is a history of discovering, rediscovering, and slowly unifying a set of algorithmic primitives that make large-scale optimisation tractable on finite hardware. Gradient checkpointing, online softmax, fused kernels, adaptive clipping, cosine scheduling, second-order optimisers, speculative decoding, mixture-of-experts routing, and compute-aware data filtering were each developed independently, motivated by different immediate problems. Yet, looked at carefully, they share a structure.

This paper makes three claims. First, all effective acceleration techniques in modern deep learning reduce to a single principle: replace a two-pass batch algorithm with a one-pass streaming algorithm that maintains a compact sufficient statistic. Second, the geometry that makes this possible is Riemannian: the natural metric on parameter space is the Fisher information matrix, and effective optimisers are those that approximate steepest descent under this metric with O\(1\) per-step overhead. Third, the parameter space of neural networks is not just a Riemannian manifold in the abstract — it is a space with a known coarse structure \(the singular value spectrum of weight matrices\) that every efficient technique exploits.

From these three claims we derive the Streaming Geometry Framework \(SGF\), which unifies the sixteen surveyed techniques under a single algebraic roof and generates novel predictions about which combinations of techniques should interact synergistically, and which should be redundant.

### 1.1 Scope and Motivation

The techniques surveyed were selected to span the full training and inference pipeline: memory \(checkpointing\), numerical stability \(online softmax, Welford\), system throughput \(kernel fusion, speculative decoding\), optimisation geometry \(Muon, K-FAC, natural gradient\), loss landscape dynamics \(edge-of-stability, progressive sharpening\), scheduling \(WSD, cosine annealing\), regularisation \(AGC/AdaGC/ZClip\), sparse computation \(MoE\), and data efficiency \(compute-aware filtering, scaling laws\). We claim that all sixteen are instances of the same abstract template.

Additionally, in sgf\_lib\_v2, we incorporate the findings of the Algebraic Autopsy \(companion paper\) into the SGF architecture, adding two new IRE component families: spectral health monitors \(SpectralPowerLawMonitor, MarchenkoPasturMonitor, AlgebraClassifier\) and algebra-aware layer primitives \(LowRankLinear, KWinnerLinear, TropicalLinear, HybridAlgebraicLayer\).

### 1.2 Contributions

- We identify and formally state three meta-patterns \(Streaming Sufficiency, Spectral Geometry, Data–Compute Duality\) that subsume all sixteen surveyed techniques.
- We introduce the concept of Incremental Riemannian Estimation \(IRE\) as the algebraic primitive common to all three meta-patterns.
- We define the Streaming Geometry Framework \(SGF\), a modular architecture in which every system component is an IRE instance.
- We provide a complete, production-quality C\+\+17/CUDA implementation \(sgf\_lib\), including all five novel predictions as implemented features.
- We derive theoretical predictions about component interactions and propose experiments to validate them.
- We identify five open problems whose resolution would complete the framework.

## 2. Related Work

### 2.1 Information Geometry and Natural Gradient

The theoretical foundation of SGF is Amari’s information geometry \(1998\). Amari showed that the parameter space of a statistical model is a Riemannian manifold with the Fisher information matrix as its metric, and that natural gradient descent — gradient descent corrected by the Fisher metric — converges orders of magnitude faster than ordinary gradient descent on ill-conditioned problems. The practical obstacle is the O\(n²\) cost of inverting the Fisher matrix for an n-parameter model.

The K-FAC algorithm \(Martens and Grosse, 2015\) made natural gradient practical by exploiting the layer-wise Kronecker structure of the Fisher: the block corresponding to layer l factors as a Kronecker product of two small matrices, whose inverse is the product of their inverses. This reduces the per-layer Fisher inverse from O\(d⁴\) to O\(d²\) cost — tractable for typical transformer layers.

More recently, FAdam \(Kim et al., 2024\) established rigorously that Adam’s second-moment buffer is computing a diagonal empirical Fisher estimate, providing theoretical justification for why Adam generalises well on ill-conditioned problems: it is implicitly performing preconditioned gradient descent, approximating the natural gradient via a diagonal approximation to the Fisher metric.

### 2.2 Spectral Methods in Deep Learning Optimisation

The spectral transform family — transformations of the form G → UΣᵖV^T for a matrix G = UΣV^T — has emerged as a unifying framework for optimizer design. Shampoo \(Gupta et al., 2018\) corresponds to p = 1/2 \(approximate natural gradient via Kronecker preconditioner\). The connection to Muon \(Jordan and Newhouse, 2024\) at p = 0 — full spectral whitening via orthogonalisation — was established in the SOAP paper \(Vyas et al., 2024\), which showed that Shampoo with Adam in the eigenbasis unifies the two approaches and outperforms either individually.

The Newton-Schulz iteration used by Muon for computing the polar factor \(p = 0 transform\) deserves independent discussion. Newton-Schulz is a polynomial iteration Y\_\{k\+1\} = Y\_k \(3I - Y\_k^T Y\_k\) / 2 that converges to the polar factor \(UV^T\) of any full-rank matrix in a fixed number of iterations. In bfloat16, 5 iterations are sufficient with overhead below 1% of total training compute for LLaMA-scale models — making exact spectral whitening practically free.

### 2.3 Online Statistics and Streaming Algorithms

Welford’s algorithm \(1962\) for online mean and variance estimation is the canonical example of the sufficient-statistic compression principle: the three scalars \(n, mean, M2\) are provably sufficient for computing the sample mean and variance of any stream without storing the raw data. The parallel merge rule \(Chan et al., 1979\) extends this to distributed computation: two \(n, mean, M2\) tuples can be merged exactly, enabling sharded batch statistics without raw data exchange.

The online softmax algorithm \(Milakov and Gimelshein, 2018\) applies the same principle to the numerically stable computation of softmax: the running pair \(max, sum\) is provably sufficient for computing any softmax output in a single pass. FlashAttention \(Dao et al., 2020, 2022, 2024\) builds directly on this insight, achieving its memory efficiency by maintaining the \(max, sum\) state per tile rather than materialising the full attention matrix.

### 2.4 Edge of Stability

Cohen et al. \(2021\) documented the edge-of-stability \(EoS\) phenomenon: gradient descent with fixed learning rate drives the maximum Hessian eigenvalue \(sharpness\) to exactly 2/η and sustains training in a non-monotone but converging regime beyond the classical stability threshold. Arora et al. \(2022\) provided the theoretical resolution: EoS dynamics correspond to a flow along the minimum-loss manifold at the stability boundary, providing implicit sharpness regularisation that favours flatter minima with better generalisation properties.

The stochastic variant \(Lee et al., 2023\) analysed EoS for mini-batch gradient descent, establishing that the stochastic edge of stability \(S-EOS\) is controlled jointly by batch size and learning rate through the trace of the Gauss-Newton approximation.

### 2.5 Scaling Laws and Data Quality

Hoffmann et al. \(2022\) established the Chinchilla scaling law: compute-optimal training requires model size and training tokens to scale in approximately equal proportion, with the optimal token-to-parameter ratio ≈ 20. Goyal et al. \(2024\) extended this to data quality, demonstrating that high-quality data loses utility under repeated exposure — the marginal utility of a data point after k repetitions falls below that of fresh lower-quality data at sufficiently high compute budgets.

Isik et al. \(2024\) further generalised the scaling law to include a dimensionless quality parameter Q, yielding L\(N, D, Q\) = A/N^α \+ B/\(D^β × Q^γ\) \+ L\_∞ — a three-dimensional Pareto frontier that cannot be optimised by tuning any single variable. The SGF Data–Compute Duality meta-pattern formalises this as a statement about the joint geometry of the data-model-compute space.

## 3. Survey of Core Techniques

We survey sixteen techniques, grouped into six thematic clusters. For each we state the problem addressed, the key algorithmic insight, the state-of-the-art performance, and the sufficient statistic maintained.

### 3.1 Memory-Efficient Backpropagation

**Gradient Checkpointing**

Standard backpropagation stores all intermediate activations, requiring O\(n\) memory for an n-layer network. Activation checkpointing stores only a subset, recomputing discarded activations from the nearest preceding checkpoint during the backward pass. Optimal checkpoint placement every √n layers reduces memory to O\(√n\) at the cost of one additional forward pass — an O\(√n\) compute overhead \(Chen et al., 2016\).

Modern implementations extend this in two directions. Selective checkpointing \(PyTorch 2.1\+\) exposes a per-operation policy: MUST\_SAVE for large matmul outputs \(cheap to store, expensive to recompute\), MUST\_RECOMPUTE for elementwise activations \(cheap to recompute, expensive to store\). Memory-mapped checkpointing \(Song et al., 2025\) extends the technique to on-device fine-tuning, combining activation quantisation and lazy decompression to enable full-gradient fine-tuning of multi-billion-parameter models on less than 1 GB.

*Sufficient statistic maintained:* The set of checkpoint activations — an O\(√n\) subset of the O\(n\) activation buffer.

### 3.2 Numerical Stability and Online Statistics

**Online Softmax**

Standard softmax requires finding the maximum of the input sequence before exponentiation to prevent overflow, forcing two passes. The online normaliser algorithm \(Milakov and Gimelshein, 2018\) maintains a running pair \(m\_j, d\_j\) — current maximum and re-normalised exponential sum — updated as:

- m\_j = max\(m\_\{j-1\}, x\_j\)
- d\_j = d\_\{j-1\} × exp\(m\_\{j-1\} - m\_j\) \+ exp\(x\_j - m\_j\)

When a new maximum is encountered, the previous sum is rescaled by exp\(old\_max - new\_max\). This is algebraically identical to two-pass safe softmax but computable in a single pass with two scalars of state. FlashAttention 4 \(Dao, 2024\) further replaces the hardware Special Function Unit path for exponentials with a cubic polynomial approximation on CUDA Cores, exploiting the fact that far fewer SFUs than CUDA Cores exist on current GPUs.

*Sufficient statistic:* \(running\_max, running\_sum\) — two scalars, O\(1\) state regardless of sequence length.

**Welford’s Algorithm**

The naive variance estimator var = E\[x²\] - E\[x\]² suffers catastrophic cancellation when the mean is large relative to the standard deviation. Welford’s algorithm \(1962\) maintains M2, the sum of squared deviations from the running mean, eliminating cancellation by construction. The parallel Chan merge \(Chan et al., 1979\) allows two \(n, mean, M2\) tuples to be merged exactly, enabling distributed batch normalisation across GPUs without raw data exchange. ZClip \(Kumar et al., 2025\) applies the same algorithm to gradient norm tracking.

*Sufficient statistic:* \(n, running\_mean, M2\) — three scalars for O\(1\) online mean and variance of any stream.

### 3.3 Kernel Fusion and System Throughput

**Fused Triton Kernels**

The GPU memory hierarchy has a large gap between on-chip registers/shared memory \(fast, small\) and HBM global memory \(slow, large\). Operations like LayerNorm, RMSNorm, RoPE, GELU, and CrossEntropy are all elementwise or reduction operations that write intermediate tensors to HBM between steps, incurring redundant round-trips. Kernel fusion eliminates these by computing the entire compound operation in a single tile pass.

The Liger-Kernel library \(Hao et al., 2024\) demonstrates: RMSNorm achieves ~3× speedup and ~3× memory reduction; CrossEntropy achieves >2× speedup and >4× memory reduction; FusedLinearCrossEntropy drops peak activation memory from O\(N × V\) to O\(chunk\_size × V\) for vocabulary V, yielding >80% memory reduction at vocab size 128k. Bandwidth utilisation improves from 11% to 88% of peak HBM bandwidth.

The roofline model gives the decision rule: any operation with arithmetic intensity below the ridge point \(approximately 60–100 FLOP/byte on H100\) is memory-bound and will benefit from fusion.

*Sufficient statistic:* For each fused kernel: the minimal set of intermediate results cached in on-chip registers. No HBM writes until the final output.

### 3.4 Optimisation on the Riemannian Weight Manifold

**Natural Gradient and K-FAC**

The parameter space of a neural network is a Riemannian manifold where the metric is the Fisher information matrix F. Standard gradient descent performs steepest descent under the Euclidean metric, which is coordinate-dependent and leads to slow convergence in ill-conditioned problems. K-FAC \(Martens and Grosse, 2015\) exploits the layer-wise block structure: for a linear layer with input activations a and output pre-activations s, the Fisher block is approximately F\_l = E\[aa^T\] ⊗ E\[ds ds^T\], where ⊗ is the Kronecker product.

FAdam \(Kim et al., 2024\) establishes rigorously that Adam’s second moment buffer is computing a diagonal empirical Fisher estimate, making Adam an implicit natural gradient method.

*Sufficient statistic:* The Kronecker factors A\_l = EMA\(aa^T\) and G\_l = EMA\(ds ds^T\) per layer — O\(d\_in² \+ d\_out²\) state instead of O\(d\_in² × d\_out²\) for the full Fisher block.

**Muon: Gradient Orthogonalisation**

Muon \(Jordan and Newhouse, 2024\) observes that gradient updates for transformer weight matrices are typically nearly low-rank — the update direction is dominated by a few singular vectors, wasting capacity on directions that are already well-represented. The fix: orthogonalise the gradient matrix \(specifically its EMA momentum\) before applying it, replacing each singular value σᵢ with 1 \(the update UΣ⁰V^T = UV^T\).

This is the p = 0 endpoint of the spectral transform family UΣᵖV^T \(Vyas et al., 2024\): Adam corresponds to p = 1; Shampoo/K-FAC to p = 1/2; Muon to p = 0; exact natural gradient to p = -1/2. The orthogonalisation is computed via Newton-Schulz iteration, runnable in bfloat16 with total overhead below 1%.

*Sufficient statistic:* The EMA momentum matrix M — same size as the weight matrix. No second-moment buffer required, saving 33% of optimiser state versus Adam.

### 3.5 Loss Landscape Dynamics and Implicit Regularisation

**Edge of Stability**

Cohen et al. \(2021\) documented a universal phenomenon: when training with full-batch gradient descent, the maximum Hessian eigenvalue \(sharpness\) rises until it reaches approximately 2/η, where η is the learning rate. At this edge of stability the training loss oscillates non-monotonically yet still trends downward — a regime outside classical optimisation theory, which requires sharpness < 2/η for convergence.

The theoretical resolution \(Arora et al., 2022\): at EoS the gradient updates are large enough to bounce iterates off valley walls. This bouncing corresponds to a flow along the minimum-loss manifold, providing implicit sharpness regularisation that favours flatter minima.

*Sufficient statistic:* The current sharpness \(max Hessian eigenvalue\) — one scalar sufficient to determine whether training is in the progressive sharpening, EoS, or converged regime.

**Adaptive Gradient Clipping \(AGC/AdaGC/ZClip\)**

Standard global gradient norm clipping applies a scalar threshold — penalising all layers identically when any one layer’s gradients spike. AGC \(Brock et al., 2021\) clips each weight matrix row-wise with threshold λ × ‖W\_row‖, making the clipping window proportional to the weight’s current norm. AdaGC \(Wang et al., 2025\) extends to per-parameter EMA-adaptive thresholds, eliminating all manual hyperparameters. ZClip \(Kumar et al., 2025\) uses Welford z-scores on historical gradient norms to set the threshold dynamically: clip when ‖g\_t‖ > μ \+ k × σ, where μ and σ are running statistics of past gradient norms.

*Sufficient statistic:* Per-layer EMA of gradient norm \(AdaGC\) or Welford \(n, mean, M2\) of global gradient norm \(ZClip\).

### 3.6 Learning Rate Scheduling

**Warmup-Stable-Decay \(WSD\)**

Standard cosine scheduling requires knowing the total training budget in advance. WSD \(Hu et al., 2024\) decouples the learning phases: brief linear warmup; long constant-LR stable phase; rapid cosine or linear decay at the end. Any checkpoint from the stable phase can be used as a starting point for an independent cooldown run of approximately 1% of total training tokens — making continual training natural.

*Sufficient statistic:* Current training step count and phase indicator — all three phases have closed-form LR schedules.

### 3.7 Inference Acceleration

**Speculative Decoding**

Autoregressive LLM decoding is memory-bandwidth-bound. Speculative decoding \(Leviathan et al., 2023\) uses a small fast draft model to generate k candidate tokens, then verifies all k in parallel with the target model. Accepted tokens are kept; the first rejected token triggers a correction. The acceptance probability for token i is min\(1, p\_target\(x\_i\) / p\_draft\(x\_i\)\). Real-world speedups: 2–5× for well-aligned draft models \(Miao et al., 2023; Li et al., 2025\).

*Sufficient statistic:* The draft model’s predictive distribution over the draft sequence — used to compute acceptance probabilities without additional target-model forward passes.

**Mixture of Experts**

MoE architectures replace dense FFN layers with N expert networks, selecting the top-k experts per token via a learned gating function. DeepSeek-V3 pushes this to 256 fine-grained experts with shared attention. Expert Choice routing \(Fedus et al., 2022\) inverts the assignment: each expert selects its top-k tokens, guaranteeing perfect load balance by construction.

*Sufficient statistic:* Expert selection probabilities from the gating network — O\(N\) scalars per token.

### 3.8 Data Efficiency and Scaling Laws

Goyal et al. \(2024\) show that compute-aware data filtering is necessary because high-quality data loses its utility when repeated — eventually falling below the utility of unseen lower-quality data at sufficient compute. Isik et al. \(2024\) generalise to L\(N, D, Q\) = A/N^α \+ B/\(D^β × Q^γ\) \+ L\_∞ with a dimensionless quality parameter Q in \(0, 1\].

*Sufficient statistic:* Per-sample quality score and repetition count — two scalars that together predict marginal utility.

## 4. Meta-Pattern Analysis

### 4.1 Meta-Pattern I: Streaming Sufficiency

**Theorem \(Streaming Sufficiency Principle\):** For any neural network computation C\(X\) that requires reading a dataset X of size n, there exists a sufficient statistic S of size o\(n\) such that C\(X\) = f\(S\(X\)\) for some function f, and S can be maintained by processing each element of X exactly once with O\(1\) update cost.

This holds specifically because neural network computation is either \(a\) a reduction \(mean, variance, max, sum\) in which case Welford-type algorithms apply, \(b\) a normalised ratio \(softmax, attention weights\) in which case the online normaliser applies, or \(c\) a linear algebra operation on a matrix of bounded rank in which case Kronecker factoring applies.

**Technique**

**Batch Algorithm**

**Sufficient Statistic**

**State Size**

Gradient Checkpointing

Store all activations, replay

Checkpoint set

O\(√n\)

Online Softmax

Two-pass max \+ normalize

\(running\_max, running\_sum\)

O\(1\)

Welford Variance

Accumulate sum and sum-of-squares

\(n, mean, M2\)

O\(1\)

K-FAC

Full Fisher matrix

Kronecker factors \(A, G\) per layer

O\(d\_in² \+ d\_out²\)

ZClip

Fixed threshold

Welford \(μ, σ\) of grad norms

O\(1\)

WSD Scheduling

Cosine over fixed budget

Training step count

O\(1\)

Data Filtering

Static quality threshold

\(quality\_score, rep\_count\)

O\(n\)

Muon

Full covariance matrix

EMA momentum matrix M

O\(d\_out × d\_in\)

### 4.2 Meta-Pattern II: Spectral Geometry

The natural language for every operation in neural network training is the singular value decomposition of the relevant matrix. The spectral transform family UΣᵖV^T unifies the optimiser landscape:

**p Value**

**Transform**

**Algorithm**

**Interpretation**

p = 1

G \(identity\)

SGD momentum

Raw gradient direction

p = 1/2

UΣ\{1/2\}VT

Shampoo / K-FAC

Approximate natural gradient

p = 0

UV^T \(polar factor\)

Muon

Full whitening / spectral norm descent

p = -1/2

UΣ\{-1/2\}VT

Full NGD

Exact natural gradient \(intractable\)

Diagonal p=0

sign\(g\)

SignSGD / Lion

Coordinate-wise whitening

The same spectral structure appears outside the optimiser. Attention is a softmax-normalised matrix product whose effective rank is controlled by the temperature of the softmax. MoE routing is a sparse projection onto the top-k eigenvectors of the expert activation space. AGC constrains the ratio of the gradient spectrum to the weight spectrum.

**Spectral Geometry Principle:** Every efficient operation in a neural network training or inference pipeline is a structured operation on the singular value spectrum of a matrix. The choice of structure \(whitening, projection, thresholding, normalisation\) determines the implicit regularisation provided by the operation.

### 4.3 Meta-Pattern III: Data–Compute Duality

The classical Chinchilla scaling law L\(N, D\) = A/N^α \+ B/D^β \+ L\_∞ gives the compute-optimal frontier in \(N, D\) space. Adding data quality Q and repetition k gives a multi-dimensional frontier that cannot be navigated by optimising any single variable.

**Data-Compute Duality Principle:** The optimal configuration of any AI system is a joint optimum over data quality, data quantity, model capacity, compute budget, and inference cost. Every component that appears to have a single-variable optimum is implicitly holding other variables at non-optimal values.

## 5. Incremental Riemannian Estimation \(IRE\)

### 5.1 The IRE Primitive

An IRE instance is a tuple \(M, S, T, φ\) where:

- **M** is a Riemannian manifold — the parameter space, weight space, or data space of interest;
- **S** is a sufficient statistic — a compact summary of the accumulated observations on M;
- **T: S × M → S** is the update rule — how S changes when one new observation arrives;
- **φ: S → M** is the read-out — how to extract the quantity of interest from S.

Every technique in the survey is an IRE instance:

**Technique**

**Manifold M**

**Sufficient Statistic S**

**Update T**

**Read-out φ**

Welford

ℝ \(real line\)

\(n, mean, M2\)

Welford update equations

var = M2/\(n-1\)

Online Softmax

Probability simplex

\(running\_max, running\_sum\)

Rescale and accumulate

Normalize by sum

K-FAC

GL\(n\) \(invertible\)

Kronecker factors \(A\_l, G\_l\)

EMA of outer products

Approximate F^\{-1\}g

Muon

Stiefel manifold

EMA momentum matrix M

EMA update

Newton-Schulz orthogonalisation

AGC/ZClip

ℝ⁺ \(positive reals\)

Welford of grad norms

Welford update

Adaptive clip threshold

WSD

ℝ⁺ \(LR space\)

Training step t

t ← t \+ 1

LR = schedule\(t, phase\(t\)\)

Checkpointing

Activation space

Checkpoint set C

Roofline policy

Recompute from nearest

Spec. Decoding

Probability simplex

Draft model distribution q

Draft forward pass

Accept/reject via q/p ratio

MoE Routing

Expert simplex

Gating logits G

Linear \+ softmax

Top-k expert selection

Data QQT

Data quality manifold

\(quality\_score, rep\_count\)

Update on training step

Marginal utility estimate

### 5.2 Why Riemannian Structure Matters

An algorithm that ignores curvature — like vanilla SGD or naive global gradient clipping — will be inefficient because it uses Euclidean distances to measure steps in a curved space. IRE requires that S be a sufficient statistic for the distribution on M *equipped with its Riemannian metric*. This is why the Kronecker factors in K-FAC are sufficient: they capture the block-diagonal structure of the Fisher metric. This is why the Welford \(mean, M2\) pair is sufficient for normalisation: it captures the sufficient statistics of a Gaussian approximation to the activation distribution.

The EoS phenomenon is an IRE phenomenon: the Hessian eigenspectrum is the sufficient statistic for the curvature of the loss landscape, and the sharpness \(max eigenvalue\) is the single scalar sufficient to determine the current training regime.

### 5.3 The Unified IRE Update

All IRE instances share the same computational template:

S\_\{t\+1\} = T\(S\_t, x\_\{t\+1\}\)              \[Online update — O\(1\) cost\]  
theta\_\{t\+1\} = phi\(S\_\{t\+1\}\)             \[Read-out — O\(1\) or O\(small\) cost\]  
g\_tilde = F\(S\_\{t\+1\}\)^\{-1\} \* g\_t        \[Riemannian gradient correction\]  
theta\_\{t\+1\} = theta\_t - eta \* g\_tilde  \[Parameter update\]

Where F\(S\) is the Riemannian metric estimated from the sufficient statistic S. The key insight: the metric F\(S\) need not be computed exactly — only its action on the gradient vector g\_t is needed.

## 6. The Streaming Geometry Framework \(SGF\)

SGF has four layers: the Physical Layer \(hardware primitives\), the Metric Layer \(Riemannian metric estimation\), the Dynamics Layer \(parameter update\), and the Control Layer \(scheduling and resource allocation\).

### 6.1 Architecture Overview

┌─────────────────────────────────────────────────────┐  
│  CONTROL LAYER   MoE router · Spec-decode · QQT     │  
│  Statistic: gating logits, draft dist, quality EMA  │  
├─────────────────────────────────────────────────────┤  
│  DYNAMICS LAYER  Muon · ZClip · WSD                 │  
│  Statistic: momentum M, Welford\(‖g‖\), step count    │  
├─────────────────────────────────────────────────────┤  
│  METRIC LAYER    K-FAC · EoS monitor · Welford norm │  
│  Statistic: Kronecker factors \(A,G\), λ\_max EMA      │  
├─────────────────────────────────────────────────────┤  
│  PHYSICAL LAYER  Tiled matmuls · KV cache · norms   │  
│  Statistic: tile \(max, sum\) · register-resident     │  
└─────────────────────────────────────────────────────┘

The crucial property: every layer communicates with adjacent layers by passing sufficient statistics, never raw tensors.

**SGF Layer**

**Components**

**IRE Instance**

**Sufficient Statistic**

Physical

Fused kernels, tiled ops

Tile-level online statistics

Per-tile \(max, sum\) and registers

Metric

K-FAC, Welford norm, EoS

K-FAC / Welford / Sharpness

Kronecker factors, \(n, mean, M2\), λ\_max

Dynamics

Muon/Adam, ZClip, WSD

Spectral UΣᵖV^T \+ ZClip \+ WSD

Momentum M, Welford of norms, step t

Control

MoE, Spec-decode, Sampler

Gating \+ draft dist \+ QQT

Top-k logits, draft q, \(quality, rep\)

### 6.2 SGF Optimizer

The SGF optimizer applies spectral transforms at different granularities:

- **Weight matrices:** Muon \(p=0\) — full spectral whitening via Newton-Schulz iterations
- **Embedding layers:** Adam \(diagonal Fisher estimate\) — Muon must not be applied to embeddings due to the inflated norms of rare-token rows
- **Bias terms:** SignSGD — coordinate-wise whitening with zero memory overhead
- **Gradient clipping:** ZClip — Welford z-score on gradient norms, fully adaptive and parameter-free
- **Learning rate schedule:** WSD — warmup \+ stable \+ compute-budget-adaptive cooldown

### 6.3 SGF Memory Manager

The decision rule is derived from the roofline model: for each layer l, compute the arithmetic intensity I\_l = FLOPs\_l / bytes\_l. If I\_l < ridge\_point, the layer is memory-bound and recomputation is preferred. If I\_l > ridge\_point, the layer is compute-bound and storing the activation is preferred. The sufficient statistic is the per-layer \(I\_l, size\_l\) pair — two scalars per layer sufficient to determine the optimal checkpointing policy without empirical profiling.

### 6.4 SGF Normaliser

All normalisation operations in SGF are Welford instances sharing the same algebraic structure, implemented with the same primitive: the parallel Welford merge T\(S\_A, S\_B\) → S\_\{A\+B\}. This makes SGF natively distributed: shards maintain local Welford states and merge at communication boundaries.

### 6.5 SGF Inference Engine

The SGF inference engine combines speculative decoding with MoE routing as a two-level IRE system:

- **Level 1 \(Token level\):** The draft model’s predictive distribution q is the IRE sufficient statistic for the acceptance decision. Acceptance probability = min\(1, p\_target / q\_draft\).
- **Level 2 \(Expert level\):** For MoE layers, the gating distribution is the IRE sufficient statistic for the expert routing decision.

The SGF prediction: combining MoE with speculative decoding should yield super-additive speedups because the draft model for a MoE target can itself be a low-expert-count version of the same architecture \(self-speculative decoding at the expert level\).

### 6.6 Integration with the Algebraic Autopsy \(sgf\_lib\_v2\)

The second version of the SGF library \(sgf\_lib\_v2\) integrates the findings of the companion Algebraic Autopsy paper into the SGF architecture. This adds two new component families:

**Spectral Health Monitors \(spectral\_monitor.cuh\):**

- SpectralPowerLawMonitor: IRE instance on ℝ that maintains OLS sufficient statistics \(Σ log k, Σ log σ, Σ \(log k\)², n\) and reads out the power-law exponent α. Classifies spectral health relative to autopsy reference values \(α\_data\_prior = 0.37, α\_dense = 0.427, α\_cypha = 0.85, α\_lowrank = 1.223\).
- MarchenkoPasturMonitor: IRE instance on PSD manifold tracking signal fraction, effective rank, and dominant singular value ratio.
- AlgebraClassifier: IRE instance on the algebra simplex that outputs scores for Low-Rank, Sparse, Tropical, and Dense algebraic structure based on EMA-smoothed spectral statistics.
- LayerwiseSpectralReport: Network-level aggregator that detects the monotone-α-with-depth property \(confirmed for the prime-task MLP: 0.31 → 0.43 → 0.54\).

**Algebra-Aware Layer Primitives \(algebraic\_layer.cuh\):**

- LowRankLinear: Grassmannian-constrained layer y = U\(V^Tx\) \+ b with r << min\(d\_in, d\_out\). CPU \+ GPU \(cuBLAS\). FLOPs reduction = \(m\+n\)r / mn — at autopsy-derived r=8, d=64: 0.57× \(matching paper\).
- KWinnerLinear: k-winner sparse activation with straight-through gradient estimator. k set from autopsy k₉₀/N = 0.33 → k = ceil\(0.33 × d\_out\).
- TropicalLinear: max-plus semiring layer y\_i = max\_j\(W\_ij \+ x\_j\) with argmax-cached backward pass \(straight-through\).
- HybridAlgebraicLayer: LowRankLinear backbone \+ k-Winner sparse gating, implementing the autopsy’s dominant algebra directly.
- OnlineSpectralRegularizer: Penalty term L\_spectral = λ × max\(0, α\_target - α\_current\)² that encourages networks toward the Cypha HRNA reference \(α = 0.85\).

## 7. Theoretical Properties

### 7.1 Convergence

SGF inherits the convergence guarantees of its component IRE instances. The Muon optimizer is a Shampoo variant with convergence rate O\(1/√T\) in the non-convex setting. The K-FAC metric estimator converges to the true Fisher metric as the EMA window grows. The ZClip threshold converges to the true gradient norm distribution mean and variance via Welford.

The interaction between the Dynamics Layer and the EoS phenomenon creates a natural stability certificate: the sharpness monitor in the Metric Layer tracks λ\_max and signals the Control Layer when 2/η is approached. The WSD scheduler can then begin the cooldown phase — turning edge-of-stability detection into a principled training termination condition.

### 7.2 Memory Complexity

SGF maintains the following total state beyond model parameters:

- **Metric Layer:** O\(d\_in² \+ d\_out²\) per layer for Kronecker factors
- **Dynamics Layer:** O\(d\_out × d\_in\) for Muon momentum; O\(1\) for ZClip and WSD
- **Memory Manager:** O\(L\) for per-layer \(I\_l, size\_l\) pairs
- **Inference Engine:** O\(V\) for draft model distribution; O\(N\_experts\) for load-balancing tracker

Total additional state is dominated by the Kronecker factors, approximately O\(d²\) per layer.

### 7.3 Communication Complexity

In distributed settings, SGF communicates sufficient statistics rather than raw gradients. The Welford merge requires transmitting three scalars per normalisation dimension — O\(n\) reduction versus transmitting raw data. The Kronecker factor merge requires transmitting two small matrices \(d\_in² \+ d\_out²\) rather than the full gradient matrix \(d\_in × d\_out per parameter\).

## 8. Predictions and Experimental Validation

### 8.1 Novel Predictions

**Prediction 1: Muon \+ K-FAC Synergy**

Muon normalises the update direction; K-FAC normalises the update magnitude. Combined, they should achieve convergence rates closer to second-order methods while maintaining the memory overhead of first-order methods. Predicted speedup: 1.5–2× over Adam in iterations-to-convergence.

**Prediction 2: Welford ZClip \+ WSD Integration**

ZClip’s Welford statistic for gradient norms provides a natural signal for WSD phase transitions: when the gradient norm distribution enters a low-variance, stable regime \(ZClip seldom triggers\), this signals that the stable phase is ending and the cooldown phase should begin. Implemented in sgf\_lib via WSDConfig::auto\_cooldown = true.

**Prediction 3: EoS-Aware Checkpointing**

The optimal checkpoint placement changes with the training phase. During progressive sharpening, the activation distribution changes rapidly — checkpoint spacing should be denser. At the edge of stability, the distribution is quasi-stationary — spacing can be wider. Tracking λ\_max via power iteration and adapting the checkpoint schedule should reduce unnecessary recomputation by 20–40%.

**Prediction 4: Data QQT Scaling Law Universality**

The quality-quantity tradeoff exponent γ characterises how much quality substitutes for quantity. The SGF prediction: γ is related to the intrinsic dimensionality of the task manifold — high-dimensional tasks \(code, math\) should have γ close to 1; low-dimensional tasks \(simple classification\) should have γ >> 1.

**Prediction 5: MoE Expert Count as IRE Granularity**

The optimal N experts should scale with the intrinsic dimension of the task distribution. The 2025 trend toward fine-grained experts \(DeepSeek-V3: 256 experts\) over coarse-grained \(Mixtral: 8 experts\) is consistent with this prediction.

### 8.2 Proposed Experimental Programme

**Experiment**

**Tests**

**Key Metric**

**Expected Outcome**

Muon \+ K-FAC on LLaMA

Optimizer synergy

Steps-to-perplexity vs. Adam

1.5–2× speedup over Adam

ZClip trigger as WSD detector

Auto WSD scheduling

Final perplexity vs. manual

Within 1% of manual with zero hyperparams

EoS-adaptive checkpointing

Dynamic checkpoint spacing

Memory-compute Pareto

20–40% less recomputation

QQT exponent γ across modalities

Universal scaling law

Fitted γ for text/code/math/vision

γ correlated with task intrinsic dimension

Expert count vs. data diversity

MoE scaling

Performance vs. N\_experts

Optimal N grows sublinearly with entropy

Self-speculative MoE decoding

Inference synergy

Throughput vs. separate systems

Multiplicative speedup

## 9. Open Problems

**Open Problem 1: The Optimal Riemannian Metric for Transformers**

The Fisher information matrix is the theoretically justified metric for probabilistic models. But transformers are not purely probabilistic — they are deterministic functions with a probabilistic output layer. Empirically, Muon \(spectral norm metric\) outperforms Adam \(diagonal Fisher\) for deterministic components. The open problem: what is the optimal Riemannian metric for each component type?

**Open Problem 2: Welford for Non-Gaussian Distributions**

Welford’s algorithm provides exact sufficient statistics for Gaussian distributions. Activation distributions in deep transformers have heavy tails and multi-modality. The open problem: what are the correct sufficient statistics for these distributions, maintainable online with O\(1\) state?

**Open Problem 3: IRE Across Training Phases**

WSD identifies three training phases; EoS analysis identifies three dynamical regimes. The open problem: is there a single IRE sufficient statistic that identifies the current training phase and prescribes the optimal algorithm for that phase, creating a fully adaptive training algorithm?

**Open Problem 4: The Data Manifold Geometry**

The QQT scaling law treats data quality as a scalar Q. But data quality is multi-dimensional: coverage, correctness, diversity, and format are all independent quality axes. The open problem: what is the correct Riemannian metric on the data manifold?

**Open Problem 5: SGF on Non-Euclidean Hardware**

Current GPU/TPU architectures are designed for dense tensor contractions. IRE instances that exploit Riemannian geometry involve matrix square roots, polar decompositions, and Kronecker inversions that are expensive on current hardware. The open problem: can hardware be designed to natively accelerate the core operations of IRE — online SPD matrix inversions and Newton-Schulz polynomial iterations?

## 10. Discussion

### 10.1 Relationship to Existing Frameworks

**Information Geometry \(Amari, 1998\):** Provides the theoretical foundation. SGF extends this by arguing that the streaming sufficient statistic structure is not just a computational convenience but a deep property of the manifold, and by showing that the same structure extends to data space, activation space, and routing space.

**Free Energy Principle \(Friston, 2010\):** SGF can be interpreted as a computational implementation of the FEP: the sufficient statistics S at each layer are the model’s beliefs about the current state of the layer above; the IRE update T is belief updating; the Riemannian metric F\(S\) plays the role of precision in the FEP formulation.

**Algorithmic Information Theory:** The quality parameter Q in the QQT scaling law is related to the algorithmic complexity of the data relative to the task: high-quality data is data close to the Kolmogorov minimum description of the task.

### 10.2 Limitations

Several limitations should be noted. First, SGF is primarily a framework for supervised and self-supervised learning — its extension to reinforcement learning requires additional work on the data manifold geometry. Second, the theoretical predictions are derived under the assumption that sufficient statistics are exactly maintained; in practice, EMA decay introduces a forgetting effect that can bias the metric estimate in non-stationary settings. Third, the experimental programme proposed in Section 8 requires significant compute to validate at scale.

### 10.3 Broader Implications

If the SGF framework is correct, it has implications beyond algorithm design. It suggests that the architecture of an AI system should be designed around its sufficient statistics — the minimal information needed at each interface — rather than around raw tensors. This is the opposite of current practice, where large intermediate tensors are the primary currency of computation.

More speculatively: if all effective AI algorithms are IRE instances on Riemannian manifolds, then the design space of AI systems is the space of \(manifold, statistic, update, readout\) tuples — a well-defined mathematical object. The systematic exploration of this space via the toolkit of differential geometry, information theory, and algebraic statistics may be more productive than the current empirical trial-and-error approach.

## 11. Conclusion

We have surveyed sixteen canonical techniques in modern neural network training and inference, identified three deep meta-patterns \(Streaming Sufficiency, Spectral Geometry, Data–Compute Duality\), formalised their common structure as Incremental Riemannian Estimation, and derived the Streaming Geometry Framework — a modular AI system architecture in which every component is an IRE instance.

The central claim: gradient checkpointing, online softmax, Welford normalisation, Muon optimisation, K-FAC preconditioning, ZClip adaptive clipping, WSD scheduling, edge-of-stability dynamics, speculative decoding, MoE routing, and compute-aware data filtering are all the same algorithm applied to different manifolds with different sufficient statistics. They are all streaming estimators of the Riemannian geometry of their respective problem spaces.

The practical import: a new technique that exploits a previously unknown sufficient statistic on a previously ignored manifold will automatically integrate with all existing SGF components. The framework provides a search strategy: look for Riemannian structure in the problem space, find the sufficient statistic for that geometry, and build an online estimator. The surprising implication of the last decade of deep learning research is that this search always succeeds.

The sgf\_lib\_v2 library provides a complete, production-quality, header-only C\+\+17/CUDA implementation of all SGF components, including the novel Algebraic Autopsy integration. All five novel predictions are implemented as first-class library features, making them directly testable without additional engineering.

## References

Amari, S. \(1998\). Natural gradient works efficiently in learning. *Neural Computation, 10*\(2\), 251–276.

Arora, S., Li, Z., Liu, H. \(2022\). Understanding gradient descent on edge of stability in deep learning. *ICML 2022*.

Bernstein, J., Newhouse, L. \(2024\). Old optimizer, new norm. *arXiv:2409.20325*.

Brock, A., De, S., Smith, S.L., Simonyan, K. \(2021\). High-performance large-scale image recognition without normalization. *ICML 2021*.

Chan, T.F., Golub, G.H., LeVeque, R.J. \(1979\). Updating formulae and a pairwise algorithm for computing sample variances. *Technical Report STAN-CS-79-773*.

Chen, T., Xu, B., Zhang, C., Guestrin, C. \(2016\). Training deep nets with sublinear memory cost. *arXiv:1604.06174*.

Cohen, J.M., Kaur, S., Li, Y., Kolter, J.Z., Talwalkar, A. \(2021\). Gradient descent on neural networks typically occurs at the edge of stability. *ICLR 2021*.

Dao, T. \(2024\). FlashAttention-3: Fast and accurate attention with asynchrony and low-precision. *arXiv:2407.08608*.

Dettmers, T., Pagnoni, A., Holtzman, A., Zettlemoyer, L. \(2022\). LLM.int8\(\): 8-bit matrix multiplication for transformers at scale. *NeurIPS 2022*.

Fedus, W., Zoph, B., Shazeer, N. \(2022\). Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. *JMLR 2022*.

Friston, K. \(2010\). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience, 11*\(2\), 127–138.

Goyal, S., Maini, P., Lipton, Z.C., Raghunathan, A., Kolter, J.Z. \(2024\). Scaling laws for data filtering — data curation cannot be compute agnostic. *CVPR 2024*.

Gupta, V., Koren, T., Singer, Y. \(2018\). Shampoo: Preconditioned stochastic tensor optimization. *ICML 2018*.

Hao, H., Zhao, R., et al. \(2024\). Liger-Kernel: Efficient Triton kernels for LLM training. *arXiv:2410.10989*.

Hoffmann, J., et al. \(2022\). Training compute-optimal large language models. *NeurIPS 2022*.

Hu, S., et al. \(2024\). MiniCPM: Scaling large language models without loss spikes. *arXiv:2402.01700*.

Isik, B., et al. \(2024\). Scaling laws for downstream task performance of large language models. *arXiv:2412.04403*.

Jordan, K., Jin, Y., et al. \(2024\). Muon: An optimizer for hidden layers in neural networks. *kellerjordan.github.io/posts/muon*.

Kim, I., et al. \(2024\). FAdam: Adam is a natural gradient optimizer using diagonal empirical Fisher information. *arXiv:2405.12807*.

Kumar, A., et al. \(2025\). ZClip: Adaptive spike mitigation for LLM pre-training. *arXiv:2504.02507*.

Leviathan, Y., Kalman, M., Matias, Y. \(2023\). Fast inference from transformers via speculative decoding. *ICML 2023*.

Li, Y., et al. \(2025\). Eagle-3: Speculative decoding with efficient dual-draft approach. *arXiv:2503.00331*.

Martin, C.H., Mahoney, M.W. \(2018\). Implicit self-regularization in deep neural networks. *arXiv:1810.01075*.

Martin, C.H., Mahoney, M.W. \(2021\). Predicting trends in the quality of state-of-the-art neural networks without access to training or testing data. *Nature Communications, 12*, 4122.

Martens, J., Grosse, R. \(2015\). Optimizing neural networks with Kronecker-factored approximate curvature. *ICML 2015*.

Miao, X., et al. \(2023\). SpecInfer: Accelerating LLM serving with speculative inference and token tree verification. *arXiv:2305.09781*.

Milakov, M., Gimelshein, N. \(2018\). Online normalizer calculation for softmax. *arXiv:1805.02867*.

Pilanci, M., Ergen, T. \(2020\). Neural networks are convex regularizers: Exact polynomial-time convex optimization formulations for two-layer networks. *ICML 2020*, 7695–7705.

Shazeer, N., et al. \(2017\). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. *ICLR 2017*.

Song, K., et al. \(2025\). Memory-mapped checkpointing for on-device LLM fine-tuning. *arXiv:2510.03425*.

Vyas, N., et al. \(2024\). SOAP: Improving and stabilizing Shampoo using Adam. *arXiv:2409.11321*.

Wang, G., et al. \(2025\). AdaGC: Improving training stability for large language model pretraining. *arXiv:2502.11034*.

Welford, B.P. \(1962\). Note on a method for calculating corrected sums of squares and products. *Technometrics, 4*\(3\), 419–420.
