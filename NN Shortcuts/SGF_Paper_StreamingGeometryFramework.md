<!-- Converted from `SGF_Paper_StreamingGeometryFramework.docx` — source was Word (.docx). -->

__The Streaming Geometry Framework__

*Meta\-Patterns in Modern Neural Network Optimization*

*and a Unified Foundation for Efficient AI Systems*

__Odin__

*2026 — Working Draft*

# __Abstract__

*We survey sixteen canonical techniques spanning memory\-efficient training, numerical stability, kernel fusion, adaptive optimisation, loss landscape dynamics, inference acceleration, and data curation\. Through systematic analysis we identify three deep meta\-patterns that recur across all levels of the neural network stack: \(I\) Streaming Sufficiency — any algorithm that accumulates global batch state can be reformulated as a streaming algorithm that maintains a compact sufficient statistic; \(II\) Spectral Geometry — the natural language for weight updates, normalisation, routing, and attention is the singular value spectrum of the relevant operator; and \(III\) Data–Compute Duality — every design choice exists on a joint Pareto frontier of data quality, compute budget, and model capacity that must be co\-optimised rather than sequentially tuned\. We show that these three meta\-patterns are not independent: they are projections of a single underlying principle we term Incremental Riemannian Estimation \(IRE\)\. From IRE we derive the Streaming Geometry Framework \(SGF\), a modular AI system architecture in which every component — optimiser, normaliser, router, scheduler, memory manager, and inference engine — is an instance of the same algebraic primitive: an online sufficient statistic on a curved parameter manifold\. We derive theoretical predictions of SGF, propose concrete implementations, and outline a research programme for validating the framework experimentally\.*

# __1\. Introduction__

The history of practical deep learning is a history of discovering, rediscovering, and slowly unifying a set of algorithmic primitives that make large\-scale optimisation tractable on finite hardware\. Gradient checkpointing, online softmax, fused kernels, adaptive clipping, cosine scheduling, second\-order optimisers, speculative decoding, mixture\-of\-experts routing, and compute\-aware data filtering were each developed independently, motivated by different immediate problems\. Yet, looked at carefully, they share a structure\.

This paper makes three claims\. First, all effective acceleration techniques in modern deep learning reduce to a single principle: replace a two\-pass batch algorithm with a one\-pass streaming algorithm that maintains a compact sufficient statistic\. Second, the geometry that makes this possible is Riemannian: the natural metric on parameter space is the Fisher information matrix, and effective optimisers are those that approximate steepest descent under this metric with O\(1\) per\-step overhead\. Third, the parameter space of neural networks is not just a Riemannian manifold in the abstract — it is a space with a known coarse structure \(the singular value spectrum of weight matrices\) that every efficient technique exploits\.

From these three claims we derive the Streaming Geometry Framework \(SGF\), which unifies the sixteen surveyed techniques under a single algebraic roof and generates novel predictions about which combinations of techniques should interact synergistically, and which should be redundant\.

## __1\.1 Scope and Motivation__

The techniques surveyed were selected to span the full training and inference pipeline: memory \(checkpointing\), numerical stability \(online softmax, Welford\), system throughput \(kernel fusion, speculative decoding\), optimisation geometry \(Muon, K\-FAC, natural gradient\), loss landscape dynamics \(edge\-of\-stability, progressive sharpening\), scheduling \(WSD, cosine annealing\), regularisation \(AGC/AdaGC\), sparse computation \(MoE\), and data efficiency \(compute\-aware filtering, scaling laws\)\. We claim that all sixteen are instances of the same abstract template\.

## __1\.2 Contributions__

- We identify and formally state three meta\-patterns \(Streaming Sufficiency, Spectral Geometry, Data–Compute Duality\) that subsume all sixteen surveyed techniques\.
- We introduce the concept of Incremental Riemannian Estimation \(IRE\) as the algebraic primitive common to all three meta\-patterns\.
- We define the Streaming Geometry Framework \(SGF\), a modular architecture in which every system component is an IRE instance\.
- We derive theoretical predictions about component interactions and propose experiments to validate them\.
- We identify five open problems whose resolution would complete the framework\.

# __2\. Survey of Core Techniques__

We survey sixteen techniques, grouped into six thematic clusters\. For each we state the problem addressed, the key algorithmic insight, the state\-of\-the\-art performance, and the sufficient statistic maintained\.

## __2\.1 Memory\-Efficient Backpropagation__

### __2\.1\.1 Gradient Checkpointing__

Standard backpropagation stores all intermediate activations, requiring O\(n\) memory for an n\-layer network\. Activation checkpointing stores only a subset, recomputing discarded activations from the nearest preceding checkpoint during the backward pass\. Optimal checkpoint placement every sqrt\(n\) layers reduces memory to O\(sqrt\(n\)\) at the cost of one additional forward pass — an O\(sqrt\(n\)\) compute overhead\.

Modern implementations extend this in two directions\. Selective checkpointing \(PyTorch 2\.1\+\) exposes a per\-operation policy: MUST\_SAVE for large matmul outputs \(cheap to store, expensive to recompute\), MUST\_RECOMPUTE for elementwise activations \(cheap to recompute, expensive to store\)\. Self\-attention recomputation is the canonical target because the softmax and QKV attention intermediate activations have O\(L^2\) memory in sequence length L — the most expensive thing to store and among the cheapest to recompute\. Memory\-mapped checkpointing \(2025\) extends the technique to on\-device fine\-tuning, combining activation quantisation and lazy decompression to enable full\-gradient fine\-tuning of multi\-billion\-parameter models on less than 1 GB\.

__Sufficient statistic maintained: __The set of checkpoint activations — an O\(sqrt\(n\)\) subset of the O\(n\) activation buffer\.

## __2\.2 Numerical Stability and Online Statistics__

### __2\.2\.1 Online Softmax__

Standard softmax requires finding the maximum of the input sequence before exponentiation to prevent overflow, forcing two passes\. The online normaliser algorithm maintains a running pair \(m\_j, d\_j\) — current maximum and re\-normalised exponential sum — updated as new elements arrive:

m\_j = max\(m\_\{j\-1\}, x\_j\)

d\_j = d\_\{j\-1\} \* exp\(m\_\{j\-1\} \- m\_j\) \+ exp\(x\_j \- m\_j\)

When a new maximum is encountered, the previous sum is rescaled by exp\(old\_max \- new\_max\)\. This is algebraically identical to two\-pass safe softmax but computable in a single pass with two scalars of state\. FlashAttention builds directly on this: its warp\-level specialisation maintains \(m, d\) per tile, and FlashAttention 4 further replaces the hardware Special Function Unit path for exponentials with a cubic polynomial on CUDA Cores, exploiting the fact that far fewer SFUs than CUDA Cores exist on current GPUs\.

__Sufficient statistic: __\(running\_max, running\_sum\) — two scalars, O\(1\) state regardless of sequence length\.

### __2\.2\.2 Welford's Algorithm__

The naive variance estimator var = E\[x^2\] \- E\[x\]^2 suffers catastrophic cancellation when the mean is large relative to the standard deviation\. Welford's algorithm maintains the sum of squared deviations from the running mean M2, updated as:

delta   = x\_new \- mean\_old

mean    = mean\_old \+ delta / n

M2      = M2 \+ delta \* \(x\_new \- mean\_new\)

var     = M2 / \(n \- 1\)

Both terms in the M2 update are of similar magnitude by construction, eliminating catastrophic cancellation\. The parallel \(Chan\) extension allows two \(n, mean, M2\) tuples to be merged exactly, enabling distributed batch normalisation across GPUs without raw data exchange\. ZClip \(2025\) applies the same algorithm to gradient norm tracking: the clipping threshold is a running z\-score computed by Welford over historical gradient norms, making it parameter\-free and adaptive\.

__Sufficient statistic: __\(n, running\_mean, M2\) — three scalars for O\(1\) online mean and variance of any stream\.

## __2\.3 Kernel Fusion and System Throughput__

### __2\.3\.1 Fused Triton Kernels__

The GPU memory hierarchy has a large gap between on\-chip registers/shared memory \(fast, small\) and HBM global memory \(slow, large\)\. Operations like LayerNorm, RMSNorm, RoPE, GELU, and CrossEntropy are all elementwise or reduction operations that write intermediate tensors to HBM between steps, incurring redundant round\-trips\. Kernel fusion eliminates these by computing the entire compound operation in a single tile pass\.

The Liger\-Kernel library \(2024\) demonstrates: RMSNorm achieves ~3x speedup and ~3x memory reduction; RoPE achieves ~3x speedup and ~3x memory reduction; CrossEntropy achieves >2x speedup and >4x memory reduction; FusedLinearCrossEntropy drops peak activation memory from O\(N \* V\) to O\(chunk\_size \* V\) for vocabulary V and batch\-sequence tokens N, yielding >80% memory reduction at vocab size 128k\. The bandwidth utilisation improvement is dramatic: from 11% to 88% of peak HBM bandwidth for standard operations\.

The roofline model gives the decision rule: any operation with arithmetic intensity below the ridge point \(approximately 100 FLOP/byte on H100\) is memory\-bound and will benefit from fusion\. Large matrix multiplications are compute\-bound \(>4096 FLOP/byte at practical sizes\) and fusion helps less\.

__Sufficient statistic: __For each fused kernel: the minimal set of intermediate results cached in on\-chip registers \(e\.g\., for RMSNorm: the inverse RMS norm; for online cross\-entropy: \(running\_max, running\_sum, gradient\)\)\. No HBM writes until the final output\.

## __2\.4 Optimisation on the Riemannian Weight Manifold__

### __2\.4\.1 Natural Gradient and K\-FAC__

The parameter space of a neural network is a Riemannian manifold where the metric is the Fisher information matrix F\. Standard gradient descent performs steepest descent under the Euclidean metric, which is coordinate\-dependent and leads to slow convergence in ill\-conditioned problems\. Natural gradient descent uses the metric\-corrected direction F^\{\-1\} \* g, which is invariant under reparameterisation and can converge orders of magnitude faster\.

The practical obstacle is that F is an \(n x n\) matrix for n parameters — intractable to invert\. K\-FAC \(Kronecker\-Factored Approximate Curvature\) exploits the layer\-wise block structure: for a linear layer with input activations a and output pre\-activations s, the Fisher block is approximately F\_l = E\[a a^T\] ⊗ E\[ds ds^T\], where ⊗ is the Kronecker product\. This allows the inverse to be computed as the inverse of two small matrices\.

FAdam \(2024\) establishes rigorously that Adam's second moment buffer is computing a diagonal empirical Fisher estimate, making Adam an implicit natural gradient method\. This explains why Adam generalises better than SGD on ill\-conditioned problems like transformer training: it is implicitly pre\-conditioning by the loss curvature\.

__Sufficient statistic: __The Kronecker factors A\_l = EMA\(a a^T\) and G\_l = EMA\(ds ds^T\) per layer — O\(d\_in^2 \+ d\_out^2\) state instead of O\(d\_in^2 \* d\_out^2\) for the full Fisher block\.

### __2\.4\.2 Muon: Gradient Orthogonalisation__

Muon \(2024\) observes that gradient updates for transformer weight matrices are typically nearly low\-rank — the update direction is dominated by a few singular vectors, wasting capacity on directions that are already well\-represented\. The fix: orthogonalise the gradient matrix \(specifically its EMA momentum\) before applying it, replacing each singular value sigma\_i with 1 \(the update UΣ^0 V^T = UV^T\)\.

This is the p=0 endpoint of the spectral transform family UΣ^p V^T: Adam corresponds to p=1 \(coordinate\-wise rescaling\); Shampoo/K\-FAC corresponds to p=1/2 \(Kronecker pre\-conditioning\); Muon corresponds to p=0 \(full whitening/orthogonalisation\)\. The orthogonalisation is computed via Newton\-Schulz iteration — a polynomial iteration on singular values that converges to \{\-1, \+1\} in a handful of steps, runnable in bfloat16, with total overhead below 1% for LLaMA\-scale models\. Muon is theoretically an instantaneous accumulation\-free Shampoo\.

__Sufficient statistic: __The EMA momentum matrix M — same size as the weight matrix\. No second\-moment buffer required \(unlike Adam\), saving 33% of optimiser state\.

## __2\.5 Loss Landscape Dynamics and Implicit Regularisation__

### __2\.5\.1 Edge of Stability__

Cohen et al\. \(2021\) documented a universal phenomenon: when training neural networks with full\-batch gradient descent, the maximum eigenvalue of the loss Hessian \(the sharpness\) rises steadily \(progressive sharpening\) until it reaches approximately 2/eta, where eta is the learning rate\. At this edge of stability the training loss oscillates non\-monotonically yet still trends downward — a regime completely outside the assumptions of classical optimisation theory, which requires sharpness < 2/eta for convergence\.

The theoretical resolution \(Arora et al\., 2022\): at EoS the gradient updates are large enough to bounce the iterates off valley walls\. This bouncing is not random — it is a deterministic flow along the manifold of minimum loss\. The implicit regularisation it provides is sharpness reduction: by operating at the stability boundary, GD seeks iterates where the sharpness is bounded by 2/eta, favouring flatter minima that generalise better\.

For SGD, the picture is more complex\. Small batches create conservative sharpening: the stochastic nature of mini\-batch Hessians means sharpness stabilises below 2/eta, not at it\. The stochastic edge of stability \(S\-EOS\) is controlled by batch size B and learning rate eta jointly, governed by a quantity related to the trace of the Gauss\-Newton approximation to the Hessian\.

__Sufficient statistic: __The current sharpness \(max Hessian eigenvalue\) — one scalar sufficient to determine whether training is in the progressive sharpening, EoS, or converged regime\.

### __2\.5\.2 Adaptive Gradient Clipping \(AGC/AdaGC/ZClip\)__

Standard global gradient norm clipping applies a scalar threshold — penalising all layers identically when any one layer's gradients spike\. AGC \(Brock et al\., 2021\) clips each weight matrix row\-wise with threshold lambda \* ||W\_row||, making the clipping window proportional to the weight's current norm\. This eliminates the cross\-layer spill\-over effect\.

AdaGC \(2025\) extends to per\-parameter EMA\-adaptive thresholds, eliminating all manual hyperparameters and completely eliminating loss spikes on LLaMA\-2 7B/13B while reducing validation perplexity by 3\.5%/1\.47%\. ZClip \(2025\) uses a Welford z\-score on historical gradient norms to set the threshold dynamically: clip when ||g\_t|| > mu \+ k\*sigma, where mu and sigma are the Welford running mean and standard deviation of past gradient norms\. The critical practical rule: never apply AGC to the final linear \(embedding\) layer — embedding rows have inflated norms from rarely\-seen tokens due to momentum accumulation\.

__Sufficient statistic: __Per\-layer EMA of gradient norm \(AdaGC\) or Welford \(n, mean, M2\) of global gradient norm \(ZClip\)\.

## __2\.6 Learning Rate Scheduling__

### __2\.6\.1 Warmup\-Stable\-Decay__

Standard cosine scheduling requires knowing the total training budget in advance\. Warmup\-Stable\-Decay \(WSD\) decouples the learning phases: a brief linear warmup to prevent early instability; a long constant\-LR stable phase for the bulk of learning; a rapid cosine or linear decay at the end\. The key insight is that the decay is a cheap post\-processing step: any checkpoint from the stable phase can be used as a starting point for an independent cooldown run of approximately 1% of total training tokens, producing a fully\-converged model\. This makes continual training natural — fork from any checkpoint and run cooldown on demand\.

The warmup phase has a specific function: learning rate warmup prevents deeper layers from creating training instability\. Early in training, deep layers have poorly\-calibrated statistics and produce unstable activations\. The warmup period lets normalisation layers equilibrate before the learning rate is large enough for these instabilities to propagate into divergence\.

__Sufficient statistic: __Current training step count and phase indicator — all three phases have closed\-form LR schedules\.

## __2\.7 Inference Acceleration__

### __2\.7\.1 Speculative Decoding__

Autoregressive LLM decoding is memory\-bandwidth\-bound: each token generation requires loading all model weights once\. Speculative decoding uses a small fast draft model to generate k candidate tokens in sequence, then verifies all k in parallel with the target model \(at cost similar to a single target\-model forward pass\)\. Accepted tokens are kept; the first rejected token triggers a correction from the target model's distribution\.

The acceptance probability for token i is min\(1, p\_target\(x\_i\) / p\_draft\(x\_i\)\)\. When draft and target distributions are well\-aligned, most tokens are accepted and the effective throughput multiplier approaches k\+1\. Real\-world speedups: 2\-5x for well\-aligned draft models; up to 5\.5x for domain\-specific configurations\. Tree\-structured speculative decoding extends this to a tree of candidate sequences, with parallel verification via tree attention, achieving higher acceptance lengths by exploiting prefix overlap\.

__Sufficient statistic: __The draft model's predictive distribution over the draft sequence — used to compute acceptance probabilities without additional forward passes through the target model\.

### __2\.7\.2 Mixture of Experts__

MoE architectures replace dense FFN layers with N expert networks, selecting the top\-k experts per token via a learned gating function\. This decouples total parameter count from per\-token FLOPs: a model with N experts of width d is equivalent in inference cost to a dense model of width d, but has N times the representational capacity\. DeepSeek\-V3 pushes this to 256 fine\-grained experts with shared attention, achieving frontier performance at dramatically reduced inference cost\.

The critical engineering challenge is load balancing: without intervention, the gating network collapses to routing all tokens to a few popular experts \(the rich\-get\-richer dynamic\)\. Auxiliary losses encourage equal expert utilisation; noisy top\-k gating adds learnable noise to break symmetry during training\. Expert Choice routing \(Google, 2022\) inverts the assignment: each expert selects its top\-k tokens, guaranteeing perfect load balance by construction\.

__Sufficient statistic: __Expert selection probabilities from the gating network — O\(N\) scalars per token, sufficient to route computation without loading inactive expert parameters\.

## __2\.8 Data Efficiency and Scaling Laws__

Classical Chinchilla scaling laws \(Hoffmann et al\., 2022\) characterise the optimal model\-size / training\-token trade\-off under homogeneous data quality\. This assumption is violated in practice: real web corpora have highly heterogeneous quality, and the utility of any data point decays with each repetition\.

Goyal et al\. \(2024\) introduce compute\-aware data filtering: high\-quality data loses its utility when repeated — eventually falling below the utility of unseen lower\-quality data\. The optimal filtering threshold is therefore compute\-budget\-dependent\. At low compute budgets, aggressive filtering \(retaining only top\-10% quality\) is optimal; at high compute budgets, the broader pool should be used\. This creates a quality\-quantity tradeoff \(QQT\) curve that is a function of the training compute, not just the data distribution\.

Isik et al\. \(2024\) generalise this to a dimensionless quality parameter Q in \(0,1\], where the loss scales as B / \(D^beta \* Q^gamma\)\. Higher\-quality data allows smaller models to reach the same loss, with a sublinear \(not linear\) relationship between effective data and quality — moderate data corruption is robust, but severe corruption is disproportionately harmful\.

__Sufficient statistic: __Per\-sample quality score and repetition count — two scalars that together predict marginal utility of including a data point in the next training epoch\.

# __3\. Meta\-Pattern Analysis__

Having surveyed sixteen techniques, we now observe that they share a deep structure\. We identify three meta\-patterns, each a distinct projection of an underlying algebraic principle\.

## __3\.1 Meta\-Pattern I: Streaming Sufficiency__

Every technique in the survey replaces a batch computation over a large set with a streaming computation that maintains a compact sufficient statistic\. The formal statement:

Theorem \(Streaming Sufficiency Principle\): For any neural network computation C\(X\) that requires reading a dataset X of size n, there exists a sufficient statistic S of size o\(n\) such that C\(X\) = f\(S\(X\)\) for some function f, and S can be maintained by processing each element of X exactly once with O\(1\) update cost\.

This is not trivially true for arbitrary C — it holds specifically because neural network computation is either \(a\) a reduction \(mean, variance, max, sum\) in which case Welford\-type algorithms apply, or \(b\) a normalised ratio \(softmax, attention weights\) in which case the online normaliser applies, or \(c\) a linear algebra operation on a matrix of bounded rank in which case Kronecker factoring applies\.

Instances of Meta\-Pattern I in the survey:

__Technique__

__Batch Algorithm__

__Sufficient Statistic__

__State Size__

Gradient Checkpointing

Store all activations, replay

Checkpoint set

O\(sqrt\(n\)\)

Online Softmax

Two\-pass max\+normalize

\(running\_max, running\_sum\)

O\(1\)

Welford Variance

Accumulate sum and sum\-of\-squares

\(n, mean, M2\)

O\(1\)

K\-FAC

Full Fisher matrix

Kronecker factors \(A, G\) per layer

O\(d\_in^2 \+ d\_out^2\)

ZClip

Fixed threshold

Welford \(mu, sigma\) of grad norms

O\(1\)

WSD Scheduling

Cosine over fixed budget

Training step count

O\(1\)

Data Filtering

Static quality threshold

\(quality\_score, repetition\_count\) per sample

O\(n\)

Muon

Full covariance matrix

EMA momentum matrix M

O\(d\_out \* d\_in\)

## __3\.2 Meta\-Pattern II: Spectral Geometry__

The natural language for every operation in neural network training is the singular value decomposition of the relevant matrix\. Weight matrices, gradient matrices, Fisher blocks, attention matrices, and routing matrices all have a natural geometry defined by their singular value spectra, and every efficient algorithm exploits this structure\.

The spectral transform family UΣ^p V^T, for a matrix G = UΣV^T, unifies the optimizer landscape:

__p Value__

__Transform__

__Algorithm__

__Interpretation__

p = 1

G \(identity\)

SGD momentum

Raw gradient direction

p = 1/2

U Σ^\{1/2\} V^T

Shampoo / K\-FAC

Approximate natural gradient

p = 0

UV^T \(polar factor\)

Muon

Full whitening / spectral norm descent

p = \-1/2

U Σ^\{\-1/2\} V^T

Full Newton / NGD

Exact natural gradient \(intractable\)

Diagonal p=0

sign\(g\)

SignSGD / Lion

Coordinate\-wise whitening

Adaptive p

UΣ^\{f\(Σ\)\}V^T

SOAP\-Muon

Curvature\-adaptive whitening

The same spectral structure appears outside the optimizer\. Attention is a softmax\-normalised matrix product whose effective rank is controlled by the temperature of the softmax \(FlashAttention's online max tracks the dominant singular direction of the QK^T matrix\)\. MoE routing is a sparse projection onto the top\-k eigenvectors of the expert activation space\. Layer normalisation constrains the spectrum of the activation tensor\. AGC constrains the ratio of the gradient spectrum to the weight spectrum\.

Spectral Geometry Principle: Every efficient operation in a neural network training or inference pipeline is a structured operation on the singular value spectrum of a matrix\. The choice of structure \(whitening, projection, thresholding, normalisation\) determines the implicit regularisation provided by the operation\.

The edge\-of\-stability phenomenon provides the sharpest illustration: the maximum Hessian eigenvalue \(the dominant singular value of the loss Hessian\) is the sufficient statistic that determines the training regime\. When it exceeds 2/eta, training enters the non\-monotonic EoS regime where implicit sharpness regularisation operates\. The learning rate eta is therefore not an arbitrary scalar — it is a constraint on the spectral radius of the permissible Hessian\.

## __3\.3 Meta\-Pattern III: Data–Compute Duality__

Every design choice in model training — data quality, data quantity, model size, training tokens, compute budget, filtering threshold — exists on a joint Pareto frontier\. Optimising any one dimension while holding others fixed is generically suboptimal\.

The classical Chinchilla scaling law L\(N, D\) = A/N^alpha \+ B/D^beta \+ L\_inf gives the compute\-optimal frontier in \(N, D\) space\. Adding data quality Q gives L\(N, D, Q\) = A/N^alpha \+ B/\(D^beta \* Q^gamma\) \+ L\_inf\. Adding data repetition k and mixing weights w\_i for source i gives a multi\-dimensional quality\-quantity\-compute frontier that cannot be navigated by optimising any single variable\.

This extends to inference\. Speculative decoding is a data\-compute trade\-off: the draft model's quality \(acceptance rate alpha\) and latency determine the effective throughput\. MoE is a parameter\-compute trade\-off: total parameters decouple from per\-token FLOPs\. WSD scheduling is a tokens\-quality trade\-off: the cooldown phase converts stable\-phase compute into final loss reduction at high marginal efficiency\.

Data\-Compute Duality Principle: The optimal configuration of any AI system is a joint optimum over data quality, data quantity, model capacity, compute budget, and inference cost\. Every component that appears to have a single\-variable optimum is implicitly holding other variables at non\-optimal values\.

# __4\. Incremental Riemannian Estimation \(IRE\)__

The three meta\-patterns are not independent\. They are projections of a single underlying principle that we formalise as Incremental Riemannian Estimation\.

## __4\.1 The IRE Primitive__

An IRE instance is a tuple \(M, S, T, phi\) where:

- M is a Riemannian manifold — the parameter space, weight space, or data space of interest;
- S is a sufficient statistic — a compact summary of the accumulated observations on M;
- T: S x M \-> S is the update rule — how S changes when one new observation arrives;
- phi: S \-> M is the read\-out — how to extract the quantity of interest from S\.

Every technique in the survey is an IRE instance:

__Technique__

__Manifold M__

__Sufficient Statistic S__

__Update T__

__Read\-out phi__

Welford

R \(real line\)

\(n, mean, M2\)

Welford update equations

var = M2/\(n\-1\)

Online Softmax

Probability simplex

\(running\_max, running\_sum\)

Rescale and accumulate

Normalize by sum

K\-FAC

GL\(n\) \(invertible matrices\)

Kronecker factors \(A\_l, G\_l\)

EMA of outer products

Approximate F^\{\-1\}g

Muon

Stiefel manifold

EMA momentum matrix M

EMA update

Newton\-Schulz orthogonalisation

AGC/ZClip

R^\+ \(positive reals\)

Welford of grad norms

Welford update

Adaptive clip threshold

WSD

R^\+ \(LR space\)

Training step t

t <\- t\+1

LR = schedule\(t, phase\(t\)\)

Checkpointing

Activation space

Checkpoint set C

Keep every sqrt\(n\)\-th

Recompute from nearest checkpoint

Spec\. Decoding

Probability simplex

Draft model distribution q

Draft forward pass

Accept/reject via q/p ratio

MoE Routing

Expert activation manifold

Gating logits G

Linear \+ softmax projection

Top\-k expert selection

Data QQT

Data quality manifold

\(quality\_score, rep\_count\)

Update on each training step

Marginal utility estimate

## __4\.2 Why Riemannian Structure Matters__

The key insight is that M is not flat Euclidean space\. The weight space of a neural network has curvature determined by the data distribution via the Fisher information matrix\. An algorithm that ignores this curvature — like vanilla SGD or naive global gradient clipping — will be inefficient because it uses Euclidean distances to measure steps in a curved space\.

IRE requires that S be a sufficient statistic not just for the distribution on M, but for the distribution on M equipped with its Riemannian metric\. This is why the Kronecker factors in K\-FAC are sufficient: they capture the block\-diagonal structure of the Fisher metric\. This is why the Welford \(mean, M2\) pair is sufficient for normalisation: it captures the sufficient statistics of a Gaussian approximation to the activation distribution — which is what BatchNorm's normalisation step implicitly assumes\.

The EoS phenomenon is an IRE phenomenon: the Hessian eigenspectrum is the sufficient statistic for the curvature of the loss landscape, and the sharpness \(max eigenvalue\) is the single scalar sufficient to determine whether the IRE update rule \(gradient descent\) is in the stable, edge\-of\-stability, or divergent regime\.

## __4\.3 The Unified IRE Update__

All IRE instances share the same computational template:

S\_\{t\+1\} = T\(S\_t, x\_\{t\+1\}\)          \[Online update — O\(1\) cost\]

theta\_\{t\+1\} = phi\(S\_\{t\+1\}\)           \[Read\-out — O\(1\) or O\(small\) cost\]

g\_tilde = F\(S\_\{t\+1\}\)^\{\-1\} \* g\_t      \[Riemannian gradient correction\]

theta\_\{t\+1\} = theta\_t \- eta \* g\_tilde \[Parameter update\]

Where F\(S\) is the Riemannian metric estimated from the sufficient statistic S\. The key insight: the metric F\(S\) need not be computed exactly — only its action on the gradient vector g\_t is needed, and this action can be approximated using the Kronecker structure of the Fisher, the orthogonal polar factor \(Muon\), or the diagonal approximation \(Adam\)\.

# __5\. The Streaming Geometry Framework \(SGF\)__

The Streaming Geometry Framework is a modular AI system architecture in which every component is an IRE instance\. SGF has four layers: the Physical Layer \(hardware primitives\), the Metric Layer \(Riemannian metric estimation\), the Dynamics Layer \(parameter update\), and the Control Layer \(scheduling and resource allocation\)\.

## __5\.1 Architecture Overview__

__SGF Layer__

__Components__

__IRE Instance__

__Sufficient Statistic__

Physical Layer

Fused kernels, tiled matmuls, KV cache

Tile\-level online statistics

Per\-tile \(max, sum\) and registers

Metric Layer

Fisher estimator, Welford normaliser, Hessian tracker

K\-FAC / Welford / Sharpness monitor

Kronecker factors, \(n, mean, M2\), lambda\_max

Dynamics Layer

Optimizer \(Muon/Adam/SOAP\), gradient clipper, LR schedule

Spectral transform UΣ^p V^T \+ ZClip \+ WSD

Momentum matrix M, Welford of norms, step count t

Control Layer

MoE router, spec\-decoding controller, data sampler

Gating distribution \+ acceptance model \+ QQT scores

Top\-k logits, draft distribution q, \(quality, rep\_count\)

The crucial property of SGF: every layer communicates with adjacent layers by passing sufficient statistics, never raw tensors\. The Physical Layer passes \(max, sum\) tuples to the Metric Layer\. The Metric Layer passes metric estimates F\(S\) to the Dynamics Layer\. The Dynamics Layer passes the update direction to the Control Layer\. The Control Layer returns routing decisions, scheduling parameters, and data selections to the Dynamics Layer\.

## __5\.2 Component Specifications__

### __5\.2\.1 The SGF Optimizer__

The SGF optimizer is a hybrid that applies spectral transforms at different granularities:

- For weight matrices: Muon \(p=0\) — full spectral whitening via Newton\-Schulz iterations
- For embedding layers: Adam \(diagonal Fisher estimate\) — Muon must not be applied to embeddings due to the inflated norms of rare\-token rows
- For bias terms: SignSGD — coordinate\-wise whitening with zero memory overhead
- Gradient clipping: ZClip — Welford z\-score on gradient norms, fully adaptive and parameter\-free
- Learning rate schedule: WSD — warmup \+ stable \+ compute\-budget\-adaptive cooldown

### __5\.2\.2 The SGF Memory Manager__

The SGF memory manager applies IRE to the problem of deciding which activations to checkpoint\. The decision rule is derived from the roofline model: for each layer l, compute the arithmetic intensity I\_l = FLOPs\_l / bytes\_l\. If I\_l < ridge\_point, the layer is memory\-bound and recomputation is preferred\. If I\_l > ridge\_point, the layer is compute\-bound and storing the activation is preferred\.

The sufficient statistic is the per\-layer \(I\_l, size\_l\) pair — two scalars per layer sufficient to determine the optimal checkpointing policy without empirical profiling\.

### __5\.2\.3 The SGF Normaliser__

All normalisation operations in SGF are Welford instances\. For training\-time normalisation \(BatchNorm, LayerNorm, RMSNorm\), the Welford statistic maintains the sufficient statistics for the activation distribution, updated online\. For gradient statistics \(ZClip\), the Welford statistic maintains the sufficient statistics for the gradient norm distribution\. For data quality estimation, the Welford statistic maintains the sufficient statistics for the quality score distribution across the corpus\.

Critically, all these Welford instances share the same algebraic structure and can be implemented with the same primitive: the parallel Welford merge T\(S\_A, S\_B\) \-> S\_\{A\+B\}\. This makes SGF natively distributed: shards maintain local Welford states and merge at communication boundaries\.

### __5\.2\.4 The SGF Inference Engine__

The SGF inference engine combines speculative decoding with MoE routing as a two\-level IRE system:

- Level 1 \(Token level\): The draft model's predictive distribution q is the IRE sufficient statistic for the acceptance decision\. Acceptance probability = min\(1, p\_target / q\_draft\)\.
- Level 2 \(Expert level\): For MoE layers, the gating distribution is the IRE sufficient statistic for the expert routing decision\. The expert set is updated online using an EMA load\-balancing tracker\.
- The two levels interact: draft model quality \(acceptance rate alpha\) determines the throughput multiplier; expert utilisation balance determines the hardware efficiency\.

The SGF prediction: combining MoE with speculative decoding should yield super\-additive speedups because the draft model for a MoE target can itself be a low\-expert\-count version of the same architecture \(self\-speculative decoding at the expert level\)\. This is consistent with the MoSE architecture \(2025\) which enables slimmable experts as implicit draft models\.

## __5\.3 Theoretical Properties__

### __5\.3\.1 Convergence__

SGF inherits the convergence guarantees of its component IRE instances\. The Muon optimizer is a Shampoo variant with convergence rate O\(1/sqrt\(T\)\) in the non\-convex setting\. The K\-FAC metric estimator converges to the true Fisher metric as the EMA window grows\. The ZClip threshold converges to the true gradient norm distribution mean and variance via Welford\.

The interaction between the Dynamics Layer and the EoS phenomenon creates a natural stability certificate: the sharpness monitor in the Metric Layer tracks lambda\_max and signals the Control Layer when 2/eta is approached\. The WSD scheduler can then respond by beginning the cooldown phase — turning the edge\-of\-stability detection into a principled training termination condition\.

### __5\.3\.2 Memory Complexity__

SGF maintains the following total state beyond model parameters:

- Metric Layer: O\(d\_in^2 \+ d\_out^2\) per layer for Kronecker factors \(same as K\-FAC\)
- Dynamics Layer: O\(d\_out \* d\_in\) for Muon momentum \(same as SGD momentum\); O\(1\) for ZClip and WSD
- Memory Manager: O\(L\) for per\-layer \(I\_l, size\_l\) pairs, L = number of layers
- Inference Engine: O\(V\) for draft model distribution \(V = vocabulary size\); O\(N\_experts\) for load\-balancing tracker

Total additional state is dominated by the Kronecker factors, approximately O\(d^2\) per layer where d is the layer width\. For typical transformer layers d = 4096, this is 16M parameters per layer — manageable at the scales where K\-FAC has been demonstrated to outperform Adam\. For very wide models, diagonal approximations can reduce this to O\(d\)\.

### __5\.3\.3 Communication Complexity__

In distributed settings, SGF communicates sufficient statistics rather than raw gradients\. The Welford merge operation T\(S\_A, S\_B\) requires transmitting three scalars per normalisation dimension — a factor of O\(n\) reduction in communication compared to transmitting the raw data\. The Kronecker factor merge requires transmitting two small matrices \(d\_in^2 \+ d\_out^2 scalars\) rather than the full gradient matrix \(d\_in \* d\_out scalars per parameter\)\. For wide layers d\_out >> d\_in, this is approximately a d\_out/d\_in reduction in communication\.

# __6\. Predictions and Experimental Validation__

## __6\.1 Novel Predictions__

SGF generates the following testable predictions:

### __Prediction 1: Muon \+ K\-FAC Synergy__

Muon \(spectral whitening of momentum\) and K\-FAC \(spectral whitening via Kronecker Fisher estimate\) address complementary aspects of the curvature problem\. Muon normalises the update direction; K\-FAC normalises the update magnitude\. Combined, they should achieve convergence rates closer to second\-order methods while maintaining the memory overhead of first\-order methods\. Predicted speedup: 1\.5\-2x over Adam in iterations\-to\-convergence, comparable to SOAP but without the eigenbasis computation overhead\.

### __Prediction 2: Welford ZClip \+ WSD Integration__

ZClip's Welford statistic for gradient norms provides a natural signal for WSD phase transitions: when the gradient norm distribution enters a low\-variance, stable regime \(ZClip seldom triggers\), this is a reliable indicator that the stable phase is ending and the cooldown phase should begin\. This eliminates the remaining manual hyperparameter in WSD \(when to start cooldown\), replacing it with a fully automatic IRE\-based trigger\.

### __Prediction 3: EoS\-Aware Checkpointing__

The optimal checkpoint placement changes with the training phase\. During progressive sharpening, the activation distribution changes rapidly — checkpoint spacing should be denser\. At the edge of stability, the distribution is quasi\-stationary — checkpoint spacing can be wider\. Tracking lambda\_max via power iteration \(O\(d\) per step\) and adapting the checkpoint schedule to the training phase should reduce unnecessary recomputation by 20\-40%\.

### __Prediction 4: Data QQT Scaling Law Universality__

The quality\-quantity tradeoff scaling law L\(N, D, Q\) = A/N^alpha \+ B/\(D^beta \* Q^gamma\) should hold not just for VLMs but for any modality where data quality is measurable\. The exponent gamma characterises how much quality substitutes for quantity: gamma > 1 means quality and quantity are more than linearly interchangeable; gamma < 1 means there are diminishing returns to quality\. The SGF prediction: gamma is related to the intrinsic dimensionality of the task manifold — high\-dimensional tasks \(code, math\) should have gamma close to 1; low\-dimensional tasks \(simple classification\) should have gamma >> 1\.

### __Prediction 5: MoE Expert Count as IRE Granularity__

In the SGF framework, MoE routing is an IRE instance over the expert activation manifold\. The number of experts N determines the granularity of the IRE partition\. The optimal N should therefore scale with the intrinsic dimension of the task distribution: more diverse tasks require finer expert partitions \(more experts\)\. The 2025 trend toward fine\-grained experts \(DeepSeek\-V3: 256 experts\) over coarse\-grained \(Mixtral: 8 experts\) is consistent with this prediction, as larger models are trained on more diverse data\.

## __6\.2 Proposed Experimental Programme__

__Experiment__

__What it tests__

__Key metric__

__Expected outcome__

Muon \+ K\-FAC on LLaMA\-scale

Prediction 1: optimizer synergy

Steps\-to\-perplexity vs\. Adam, SOAP, Muon alone

1\.5\-2x speedup over Adam, >5% better than Muon alone

ZClip trigger as WSD phase detector

Prediction 2: automatic WSD scheduling

Final perplexity vs\. manually\-tuned WSD

Within 1% of manual WSD with zero schedule hyperparams

EoS\-adaptive checkpointing

Prediction 3: dynamic checkpoint spacing

Memory\-compute Pareto vs\. fixed checkpoint spacing

20\-40% less recomputation at same memory budget

QQT exponent gamma across modalities

Prediction 4: universal scaling law

Fitted gamma for text/code/math/vision

gamma correlated with task intrinsic dimensionality

Expert count vs\. data diversity

Prediction 5: MoE scaling with diversity

Performance vs\. N\_experts as function of dataset entropy

Optimal N grows sublinearly with dataset entropy

Self\-speculative MoE decoding

Inference synergy prediction

Throughput vs\. separate spec\-decode \+ MoE

Multiplicative speedup from shared architecture

# __7\. Open Problems__

Five open problems would, if resolved, complete the SGF framework:

### __Open Problem 1: The Optimal Riemannian Metric for Transformers__

The Fisher information matrix is the theoretically justified metric for probabilistic models\. But transformers are not purely probabilistic models — they are deterministic functions with a probabilistic output layer\. The correct metric for the deterministic components \(attention, MLP layers\) may differ from the Fisher metric\. Empirically, Muon \(which uses the spectral norm metric\) outperforms Adam \(which uses the diagonal Fisher\) for these components\. The open problem: what is the optimal Riemannian metric for each component type, and is there a unified metric that works for all?

### __Open Problem 2: Welford for Non\-Gaussian Distributions__

Welford's algorithm provides exact sufficient statistics for Gaussian distributions\. Activation distributions in deep transformers are not Gaussian — they have heavy tails \(gradient spike distributions\) and multi\-modality \(MoE routing concentrations\)\. The open problem: what are the correct sufficient statistics for these distributions, and can they be maintained online with O\(1\) state? Recent work on online quantile estimation \(P^2 algorithm, count\-min sketches\) suggests this is tractable\.

### __Open Problem 3: IRE Across Training Phases__

WSD identifies three training phases \(warmup, stable, cooldown\) with distinct dynamics\. The edge\-of\-stability analysis identifies three dynamical regimes \(progressive sharpening, EoS, convergence\)\. These phase structures should be unified\. The open problem: is there a single IRE sufficient statistic that identifies the current training phase and prescribes the optimal algorithm for that phase, creating a fully adaptive training algorithm?

### __Open Problem 4: The Data Manifold Geometry__

The QQT scaling law treats data quality as a scalar Q\. But data quality is multi\-dimensional: coverage, correctness, diversity, and format are all independent quality axes\. The open problem: what is the correct Riemannian metric on the data manifold, and how does the intrinsic geometry of the data distribution interact with the intrinsic geometry of the parameter manifold via the Fisher information?

### __Open Problem 5: SGF on Non\-Euclidean Hardware__

Current GPU/TPU architectures are designed for dense tensor contractions — Euclidean operations\. IRE instances that exploit Riemannian geometry \(K\-FAC, Muon, natural gradient\) involve matrix square roots, polar decompositions, and Kronecker inversions that are expensive on current hardware\. The open problem: can hardware be designed \(or existing hardware repurposed\) to natively accelerate the core operations of IRE — specifically, online symmetric positive definite matrix inversions and Newton\-Schulz polynomial iterations — to make SGF practical at all scales without overhead?

# __8\. Discussion__

## __8\.1 Relationship to Existing Frameworks__

The SGF framework is most closely related to three lines of prior work:

Information geometry \(Amari, 1998\) provides the theoretical foundation\. Amari showed that the parameter space of a statistical model is a Riemannian manifold with the Fisher information metric, and that natural gradient descent is the geometrically correct optimisation algorithm\. SGF extends this by: \(a\) arguing that the streaming sufficient statistic structure is not just a computational convenience but a deep property of the manifold; \(b\) showing that the same structure extends to data space, activation space, and routing space, not just parameter space; and \(c\) building the full system architecture from IRE primitives rather than just the optimizer\.

Free Energy Principle \(Friston, 2010\) proposes that adaptive systems minimise a single scalar — variational free energy — across all levels of a hierarchical model\. SGF can be interpreted as a computational implementation of the FEP: the sufficient statistics S at each layer are the model's beliefs about the current state of the layer above; the IRE update T is belief updating; and the read\-out phi is action selection\. The Riemannian metric F\(S\) plays the role of precision in the FEP formulation\.

Algorithmic information theory provides the language for the data–compute duality meta\-pattern\. The quality parameter Q in the QQT scaling law is related to the algorithmic complexity of the data relative to the task: high\-quality data is data that is close to the Kolmogorov minimum description of the task, while low\-quality data has high redundancy or irrelevant information\. The scaling law L = A/N^alpha \+ B/\(D^beta \* Q^gamma\) is then a statement about the information\-theoretic relationship between model capacity, data volume, and data quality\.

## __8\.2 Limitations__

Several limitations should be noted\. First, SGF is primarily a framework for supervised and self\-supervised learning — its extension to reinforcement learning, where the data distribution changes with the policy, requires additional work on the data manifold geometry\. Second, the theoretical predictions are derived under the assumption that sufficient statistics are exactly maintained; in practice, EMA decay introduces a forgetting effect that can bias the metric estimate in non\-stationary settings\. Third, the experimental programme proposed in Section 6 requires significant compute to validate at scale\.

## __8\.3 Broader Implications__

If the SGF framework is correct, it has implications beyond algorithm design\. It suggests that the architecture of an AI system should be designed around its sufficient statistics — the minimal information needed at each interface — rather than around raw tensors\. This is the opposite of current practice, where large intermediate tensors are the primary currency of computation and sufficient statistics are computed only locally within components\.

More speculatively: if all effective AI algorithms are IRE instances on Riemannian manifolds, then the design space of AI systems is the space of \(manifold, statistic, update, readout\) tuples — a well\-defined mathematical object\. The systematic exploration of this space via the toolkit of differential geometry, information theory, and algebraic statistics may be more productive than the current empirical trial\-and\-error approach to algorithm design\.

# __9\. Conclusion__

We have surveyed sixteen canonical techniques in modern neural network training and inference, identified three deep meta\-patterns \(Streaming Sufficiency, Spectral Geometry, Data–Compute Duality\), formalised their common structure as Incremental Riemannian Estimation, and derived the Streaming Geometry Framework — a modular AI system architecture in which every component is an IRE instance\.

The central claim of this paper: the apparently disparate techniques of gradient checkpointing, online softmax, Welford normalisation, Muon optimisation, K\-FAC preconditioning, ZClip adaptive clipping, WSD scheduling, edge\-of\-stability dynamics, speculative decoding, MoE routing, and compute\-aware data filtering are all the same algorithm applied to different manifolds with different sufficient statistics\. They are all streaming estimators of the Riemannian geometry of their respective problem spaces\.

The practical import: a new technique that exploits a previously unknown sufficient statistic on a previously ignored manifold will automatically integrate with all existing SGF components\. The framework provides a search strategy: look for Riemannian structure in the problem space, find the sufficient statistic for that geometry, and build an online estimator\. The surprising implication of the last decade of deep learning research is that this search always succeeds\.

# __References__

Amari, S\. \(1998\)\. Natural gradient works efficiently in learning\. Neural Computation, 10\(2\), 251\-276\.

Arora, S\., Li, Z\., Liu, H\. \(2022\)\. Understanding gradient descent on edge of stability in deep learning\. ICML 2022\.

Bernstein, J\., Newhouse, L\. \(2024\)\. Old optimizer, new norm\. arXiv:2409\.20325\.

Brock, A\., De, S\., Smith, S\.L\., Simonyan, K\. \(2021\)\. High\-performance large\-scale image recognition without normalization\. ICML 2021\.

Chan, T\.F\., Golub, G\.H\., LeVeque, R\.J\. \(1979\)\. Updating formulae and a pairwise algorithm for computing sample variances\. Technical Report STAN\-CS\-79\-773\.

Chen, T\., Xu, B\., Zhang, C\., Guestrin, C\. \(2016\)\. Training deep nets with sublinear memory cost\. arXiv:1604\.06174\.

Cohen, J\.M\., Kaur, S\., Li, Y\., Kolter, J\.Z\., Talwalkar, A\. \(2021\)\. Gradient descent on neural networks typically occurs at the edge of stability\. ICLR 2021\.

Dao, T\. \(2024\)\. FlashAttention\-3: Fast and accurate attention with asynchrony and low\-precision\. arXiv:2407\.08608\.

Dettmers, T\., Pagnoni, A\., Holtzman, A\., Zettlemoyer, L\. \(2022\)\. LLM\.int8\(\): 8\-bit matrix multiplication for transformers at scale\. NeurIPS 2022\.

Fedus, W\., Zoph, B\., Shazeer, N\. \(2022\)\. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity\. JMLR 2022\.

Friston, K\. \(2010\)\. The free\-energy principle: A unified brain theory? Nature Reviews Neuroscience, 11\(2\), 127\-138\.

Goyal, S\., Maini, P\., Lipton, Z\.C\., Raghunathan, A\., Kolter, J\.Z\. \(2024\)\. Scaling laws for data filtering — data curation cannot be compute agnostic\. CVPR 2024\.

Gupta, V\., Koren, T\., Singer, Y\. \(2018\)\. Shampoo: Preconditioned stochastic tensor optimization\. ICML 2018\.

Hoffmann, J\., et al\. \(2022\)\. Training compute\-optimal large language models\. NeurIPS 2022\.

Hu, S\., et al\. \(2024\)\. MiniCPM: Scaling large language models without loss spikes\. arXiv:2402\.01700\. \[WSD scheduler\]

Isik, B\., et al\. \(2024\)\. Scaling laws for downstream task performance of large language models\. arXiv:2412\.04403\.

Jordan, K\., Jin, Y\., et al\. \(2024\)\. Muon: An optimizer for hidden layers in neural networks\. kellerjordan\.github\.io/posts/muon\.

Kim, I\., et al\. \(2024\)\. FAdam: Adam is a natural gradient optimizer using diagonal empirical Fisher information\. arXiv:2405\.12807\.

Kumar, A\., et al\. \(2025\)\. ZClip: Adaptive spike mitigation for LLM pre\-training\. arXiv:2504\.02507\.

Leviathan, Y\., Kalman, M\., Matias, Y\. \(2023\)\. Fast inference from transformers via speculative decoding\. ICML 2023\.

Li, Y\., et al\. \(2025\)\. Eagle\-3: Speculative decoding with efficient dual\-draft approach\. arXiv:2503\.00331\.

Martens, J\., Grosse, R\. \(2015\)\. Optimizing neural networks with Kronecker\-factored approximate curvature\. ICML 2015\.

Miao, X\., et al\. \(2023\)\. SpecInfer: Accelerating LLM serving with speculative inference and token tree verification\. arXiv:2305\.09781\.

Milakov, M\., Gimelshein, N\. \(2018\)\. Online normalizer calculation for softmax\. arXiv:1805\.02867\.

OpenAI/Modal\. \(2025\)\. Reverse engineering FlashAttention 4\. modal\.com/blog/reverse\-engineer\-flash\-attention\-4\.

Shazeer, N\., et al\. \(2017\)\. Outrageously large neural networks: The sparsely\-gated mixture\-of\-experts layer\. ICLR 2017\.

Song, K\., et al\. \(2025\)\. Memory\-mapped checkpointing for on\-device LLM fine\-tuning\. arXiv:2510\.03425\.

Touvron, H\., et al\. \(2023\)\. LLaMA: Open and efficient foundation language models\. arXiv:2302\.13971\.

Vyas, N\., et al\. \(2024\)\. SOAP: Improving and stabilizing Shampoo using Adam\. arXiv:2409\.11321\.

Wang, G\., et al\. \(2025\)\. AdaGC: Improving training stability for large language model pretraining\. arXiv:2502\.11034\.

Welford, B\.P\. \(1962\)\. Note on a method for calculating corrected sums of squares and products\. Technometrics, 4\(3\), 419\-420\.

Hao, H\., Zhao, R\., et al\. \(2024\)\. Liger\-Kernel: Efficient triton kernels for LLM training\. arXiv:2410\.10989\.

