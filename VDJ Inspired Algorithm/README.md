# VDJ-Inspired Algorithm

A general-purpose pattern recognition, combinatorial generation, and one-shot learning system. Built from the mathematical philosophy of V(D)J recombination: minimal states, combinatorial diversity, geometric progression, pattern-driven transitions, and single-example generalisation. Designed for strong decoupling, embedded-friendly resource use, and modular extension.

---

## Table of Contents

1. [Conceptual Foundation](#1-conceptual-foundation)
2. [System Architecture](#2-system-architecture)
3. [Data Model](#3-data-model)
4. [Core Mathematics](#4-core-mathematics)
5. [Module Reference](#5-module-reference)
6. [Profiling System](#6-profiling-system)
7. [Configuration](#7-configuration)
8. [Usage](#8-usage)
9. [Design Principles](#9-design-principles)
10. [Complexity and Scaling](#10-complexity-and-scaling)

---

## 1. Conceptual Foundation

### What V(D)J recombination actually does

In vertebrate adaptive immunity, the RAG1/RAG2 enzyme complex assembles antibody receptor genes from a library of discrete gene segments — Variable (V), Diversity (D), and Joining (J). The process works as follows:

- Each segment is flanked by a **Recombination Signal Sequence (RSS)**: a conserved heptamer and nonamer separated by either a 12 or 23 base-pair spacer
- RAG recognises these RSS patterns directly from structural features — not by exhaustive sequence comparison
- The **12/23 rule** governs which segments can join: a 12-spacer RSS can only recombine with a 23-spacer RSS, enforcing a typed interface contract
- After RAG cuts the DNA, **junctional diversity** is introduced at the join site through imprecise hairpin opening, P-nucleotide addition, and template-independent N-nucleotide addition
- The result: a library of ~50 V segments, ~25 D segments, and 6 J segments produces an estimated 10^18 distinct receptor sequences

The immune system sees a new antigen pattern **once** and the RAG machinery responds immediately — there is no iterative learning loop. This is one-shot generalisation implemented in biochemistry.

### What this algorithm inherits

This system does not model immunology. It inherits the *mathematical structure* underlying VDJ:

| Biological mechanism | Algorithmic analogue |
|---|---|
| RSS heptamer/nonamer recognition | Multi-scale structural pattern detection |
| C(V,D,J) combinatorial assembly | C(n,r) combinatorial generation with geometric scaling |
| 12/23 rule interface constraint | Typed `Pattern` dataclass + module interface contracts |
| One-shot RAG activation | `OneShotLearner`: memory update on first contact |
| Junctional diversity (P/N additions) | `CombinatorialGenerator` softmax-weighted projections |
| Minimal RAG state machine | Small set of discrete `PatternType` states |
| Population-level clonal selection | `MetaPatternProcessor` hierarchical clustering + variance filtering |

The biological VDJ mechanism is actually limited in scope — it handles one specific DNA recombination task. This algorithm takes the underlying mathematical ideas and generalises them into a framework applicable to arbitrary pattern spaces: signal detection, state-space search, anomaly detection, graph analysis, evolutionary optimisation, and embedded sensor processing.

### Why these mathematics work

The core insight from VDJ is that **combinatorial coverage of a space is efficient when structured by geometric progression**. The 1/2^r scaling used throughout this system means that successive combination terms have exponentially decreasing weight — the most significant structural components dominate, minor components contribute fractionally, and the system naturally compresses the most important signal without discarding the rest.

This gives the algorithm three properties that are hard to achieve simultaneously:

- **Scale invariance** — patterns are analysed at multiple resolutions; their geometric structure is preserved across scales
- **Combinatorial completeness** — all valid combinations of pattern elements are considered, not a sampled subset
- **Computational tractability** — geometric weighting means the effective information content per combination decays rapidly, so early termination and caps on r are mathematically principled rather than arbitrary

---

## 2. System Architecture

### Top-level structure

```
UnifiedSystem
│
├── OneShotLearner
│     Single-example pattern acquisition and persistent memory
│
├── PatternRecognizer
│     Multi-scale geometric, combinatorial, and topological analysis
│
├── CombinatorialGenerator
│     C(n,r) enumeration with geometric scaling and pattern projection
│
├── MetaPatternProcessor
│     Cross-pattern hierarchy and pairwise relationship extraction
│
├── SpaceExplorer
│     Internal geometry navigation, path search, topology fingerprinting
│
└── ResourceManager
      Buffer allocation, result caching, and deterministic cleanup

Supporting systems (independently instantiable)
│
├── ValidationSystem      — pattern and state validity scoring
├── StateEvolution        — time-indexed state progression
├── GraphEvolution        — dynamic adjacency matrix evolution
├── PatternFlow           — three-stage input/transform/output pipeline
├── CommunicationSystem   — typed inter-module compatibility scoring
├── ResourceOptimizer     — constrained gradient-based resource allocation
└── SystemProfiler        — wall-clock, cProfile, and memory instrumentation
```

### Pipeline execution order

`UnifiedSystem.process_pattern()` runs the five primary modules in strict sequence. Each stage's output feeds the next:

```
Input: Pattern
  │
  │── OneShotLearner.learn(pattern)
  │     → Pattern  (learned)
  │
  │── PatternRecognizer.recognize(learned)
  │     → Dict[geometry, combinations, topology, combined]
  │
  │── CombinatorialGenerator.generate(learned)
  │     → Dict[combinations: List[Pattern], scaled, predictions, optimized]
  │
  │── MetaPatternProcessor.process_meta([learned] + combinations)
  │     → Dict[hierarchy, relationships, meta_patterns: List[Pattern]]
  │
  │── SpaceExplorer.explore(learned)
  │     → Dict[structure, paths, optimization]
  │
Output: Dict with all five stage results
```

### Module independence

Every module is independently instantiable and testable. The only shared contract is the `Pattern` dataclass. Modules do not call each other — all orchestration happens in `UnifiedSystem`. This means any module can be replaced, subclassed, or bypassed without touching the others.

---

## 3. Data Model

### `SystemConfig`

The single configuration object passed to every module at construction time. Centralising all parameters here means changing one value propagates everywhere without hunting through class internals.

```python
@dataclass
class SystemConfig:
    # Hardware
    num_gpus:             int
    num_cpus:             int
    device:               str        # 'cuda' or 'cpu', auto-detected

    # Pattern space
    pattern_size:         int        # reference size for analysis and validation
    state_dims:           Tuple[int, ...]
    batch_size:           int = 128

    # Combinatorial generation
    max_combo_r:          int   = 8  # maximum r in C(n,r)

    # OneShotLearner
    similarity_threshold: float = 0.8   # cosine sim threshold for memory match

    # SpaceExplorer
    neighbor_threshold:   float = 1.5   # L2 distance for adjacency

    # ResourceOptimizer
    max_iterations:       int   = 50
    tolerance:            float = 1e-4
    lambda_balance:       float = 0.5
    learning_rate:        float = 0.01
```

### `Pattern`

The universal data container. Every module input and output is either a `Pattern`, a `List[Pattern]`, or a `Dict` whose leaf values are `Pattern` or `torch.Tensor`.

```python
@dataclass
class Pattern:
    data:       torch.Tensor        # the actual pattern data (1-D or 2-D)
    type:       PatternType         # categorical label
    scale:      float               # current scale factor (1.0 = original)
    properties: Dict[str, Any]      # module-specific metadata
    validation: Dict[str, bool]     # validity flags set during processing

    def to_device(self, device: torch.device) -> 'Pattern':
        ...
```

`properties` is intentionally open-ended. Modules write their own keys into it (e.g., `'source': 'novel'`, `'time_step': 42`, `'alpha': 0.73`) and downstream modules can inspect them or ignore them. This avoids hard coupling while preserving auditability.

### `PatternType`

```python
class PatternType(Enum):
    GEOMETRIC     = 1    # spatially structured data
    COMBINATORIAL = 2    # index or combination arrays
    SEQUENTIAL    = 3    # time-ordered or ordered data
    GRAPH         = 4    # adjacency or feature matrices
    META          = 5    # cluster centroids or hierarchy patterns
```

Type is used by `ValidationSystem` to score type-appropriateness and by modules to select processing paths. `META` patterns are produced exclusively by `MetaPatternProcessor`.

---

## 4. Core Mathematics

### 4.1 Multi-scale recognition

The top-level recognition function:

```
R(x) = G(x) × C(x) × T(x)
```

where G, C, T are the geometric, combinatorial, and topological analysis functions respectively. The product structure means that a pattern must score well on all three dimensions to produce a high combined score — any single dimension being near-zero suppresses the result.

### 4.2 Geometric analysis

At each scale s ∈ {0.5, 1.0, 2.0}, the pattern is interpolated and three feature classes are computed:

**Scale invariants** `I(x) = Σᵢ sᵢ(x)`:
Statistical moments at each scale — mean, std, max, min, and raw moments 1–4. The sum across scales gives a representation that is stable under uniform rescaling.

**Transformation features** `T(x) = ∏ᵢ tᵢ(x)`:
For each rotation angle θ ∈ {0°, 90°, 180°, 270°}, edge gradient statistics (∂x, ∂y means and stds) and FFT statistics (magnitude mean/std, phase mean/std) are computed. The product across angles captures transformation-stable structure — features that survive rotation contribute positively; rotationally-sensitive features are suppressed.

**Symmetry measures** `S(x) = Σᵢ σᵢ(x)`:
Four symmetry scores computed as mean squared error between the pattern and each of its reflections/rotations:
- Horizontal reflection: MSE(x, flip(x, axis=0))
- Vertical reflection: MSE(x, flip(x, axis=1))
- 90° rotational: MSE(x, rot90(x, k=1))
- 180° rotational: MSE(x, rot90(x, k=2))

Low MSE = high symmetry. These are recorded as-is (not inverted), so they serve as asymmetry metrics — high values indicate rich directional structure.

### 4.3 Combinatorial analysis

```
S(n) = C(n,r) × G(r) × P(r)
```

**Combination enumeration** `C(n,r)`:
All C(n, min(n, max_combo_r)) index combinations are enumerated recursively. Each combination is a length-r vector of indices into the pattern's first dimension.

**Geometric scaling** `G(r) = 1/2^r`:
Column k of the combination matrix is multiplied by 1/2^k. This gives exponentially decreasing weight to successive elements — the first selected index contributes fully, the second at half weight, the third at a quarter, and so on. This mirrors the geometric progression that makes VDJ's segment assembly tractable: significant choices dominate, marginal ones fade.

**Pattern prediction** `P(r)`:
Each scaled row is projected back into the original data space. Row indices are used as a softmax-weighted selector over the source pattern's flattened values, producing a prediction tensor of the same shape as the input.

### 4.4 Topological analysis

Three components characterise the pattern's intrinsic structure:

**Structure** — normalised cumulative variance of sorted values:
```
S(x) = cumsum((x_sorted - mean(x))²) / max(cumsum(...))
```
This is a discrete approximation to a persistence curve: it describes how variance accumulates as you threshold the data from minimum to maximum. Patterns with a few dominant features produce a step function; uniform patterns produce a straight line.

**Relationships** — pairwise cosine similarity matrix:
```
R(x,y) = (x/‖x‖) · (y/‖y‖)ᵀ
```
Row-wise normalised dot product over all row pairs of the 2-D pattern matrix. Captures which rows (structural subunits) are geometrically aligned.

**Mapping** — SVD-based manifold fingerprint:
```
M(x) = σ / Σσ
```
Normalised singular values from the full SVD of the flattened pattern matrix. These describe the intrinsic dimensionality of the pattern — how many independent directions carry meaningful variance. Useful for comparing patterns across different scales and types.

### 4.5 State evolution

```
E(s,t) = ∏ᵢ [F(sᵢ) × T(sᵢ) × A(sᵢ)]
```

Three time-dependent factors applied element-wise:

**Forward evolution** `F(s,t)`:
```
F(s,t) = s + σ(t/10) × ∇s
```
Sigmoid-gated finite-difference gradient step. At t=0 the gate is 0.5 and the step is half-magnitude. As t→∞ the gate approaches 1 and evolution proceeds at full rate.

**Transition** `T(s,t)`:
```
T(s,t) = σ(s·t/20) × s + (1 - σ(s·t/20)) × s_next
```
Probabilistic blend between current state and the one-step Euler prediction. At low t the blend is near-50/50; at high t the current state dominates.

**Adaptation** `A(s,t)`:
```
A(s,t) = s × (1 + tanh(t/15) × env(s,t))
```
Environmental pressure term. `env(s,t)` is the mean absolute value of s decayed exponentially with time — a measure of overall activity level. As activity decreases, the adaptation factor approaches 1 and state evolution stabilises.

### 4.6 Graph evolution

```
∂G/∂t = N(G) + E(G) + A(G)
```

**Network dynamics** `N(G)`:
- Node: degree-weighted tanh activation — high-degree nodes attract more flow
- Edge: antisymmetric symmetrisation pressure — `0.005 × (Gᵀ - G)`
- Global: mean-reversion — `-0.001 × mean(G)`

**Evolution** `E(G)`:
- Growth: `+0.005 × ReLU(G)` — positive edges strengthen
- Decay: `-0.005 × ReLU(-G)` — negative edges weaken
- Mutation: `0.001 × N(0,1)` — low-amplitude random perturbation

**Adaptation** `A(G)`:
- Local: 1-D convolution smoothing with a uniform 3-tap kernel
- Global: spectral-norm-toward-1 pull — `0.001 × (1/‖G‖₂ - 1) × G`

### 4.7 Pattern validation

```
V(p) = Σᵢ [αᵢS(p) × βᵢR(p) × γᵢC(p)]     weights: (0.4, 0.3, 0.3)
```

**Structure score** `S(p)`:
Average of three binary-ish checks: dimensionality is 1 or 2, `properties` is a dict, `type` is a valid `PatternType`.

**Rule score** `R(p)`:
Average of: size ratio to `pattern_size`, fraction of values within 3 standard deviations, fraction of finite values.

**Consistency score** `C(p)`:
`(finite_fraction + clamp(std, 0, 1)) / 2` — rewards patterns that are both numerically clean and have meaningful spread.

**State validation** `V(s) = K(s) × L(s) × M(s)`:
- Known `K`: fraction of finite elements
- Local `L`: `exp(-mean|∇s|)` — rewards smooth, locally consistent states
- Meta `M`: `sigmoid(1 - mean|s|)` — rewards unit-scale states

### 4.8 Resource optimisation

```
O(x) = min[E(x) + λC(x)]
subject to: g(x) ≤ 0  (resource constraints)
            h(x) = 0  (system constraints)
```

Gradient descent with two constraint projections applied per step:

- Resource constraint: clamp gradient to ±mean(|constraint|)
- System constraint: project gradient onto the constraint's null space (orthogonal projection)

`λ` (`lambda_balance`) controls the efficiency/cost trade-off. `E(x)` is measured by performance minus usage; `C(x)` by squared mean plus max absolute value.

### 4.9 One-shot learning dynamics

```
L(x) = K(x) × N(x)
∂L/∂t = F(L) + M(L) + A(L)
```

The learning function decomposes into known-pattern recall K and novel-pattern integration N. On first contact with an empty memory bank, K is zero and the output is entirely novel. On subsequent contacts with similar patterns, K scales up via cosine similarity, blending known structure into the result.

Memory update is unconditional — every processed pattern updates the bank, regardless of novelty. This ensures the bank always reflects the most recent contact and enables drift tracking over time.

---

## 5. Module Reference

### 5.1 OneShotLearner

Acquires patterns from single examples and maintains a persistent key-value memory bank.

**Feature extraction pipeline:**

Three feature classes are concatenated into a single feature vector:

*Geometric* (12 values): For each scale s ∈ {0.5, 1.0, 2.0}, compute mean μ, standard deviation σ, skewness `E[(x-μ)³]/σ³`, and excess kurtosis `E[(x-μ)⁴]/σ⁴` of the scaled pattern. Manual centred-moment computation — not library statistics functions.

*Structural* (8 values): Finite-difference gradient magnitudes |∂x|, |∂y| and their standard deviations; FFT magnitude statistics (mean, std) and phase statistics (mean, std) over the 2-D frequency domain.

*Statistical* (7 values): Mean, std, max, min, median (scalar), skewness, kurtosis of the raw data.

**Memory matching:**

For each stored pattern, cosine similarity is computed between the new feature vector and the stored one:

```
similarity = (f_new · f_stored) / (‖f_new‖ × ‖f_stored‖)
```

If similarity > `similarity_threshold` (default 0.8), the stored pattern is a match. Multiple matches are softmax-weighted and blended. The blending coefficient for the final output is the similarity score of the best match:

```
output = α × best_known + (1 - α) × novel
```

where α is the best-match cosine similarity.

**Memory bank:** Simple dict keyed by sequential integer strings. No eviction policy — the bank grows monotonically. For long-running applications, implement your own eviction by replacing `self.memory` with an `OrderedDict` and popping the oldest entry when a size limit is reached.

---

### 5.2 PatternRecognizer

Multi-scale structural analysis. Runs geometric, combinatorial, and topological analysis independently and multiplies their scalar summaries for the combined score.

**Geometric analysis:** Three-scale interpolation (0.5×, 1.0×, 2.0×) using bilinear interpolation. At each scale: scale invariants (8 values) + transformation features (8 values × 4 rotations, product-combined) + symmetry measures (4 values). Feature vectors are concatenated across scales.

**Combinatorial analysis:** C(n, r) enumeration with r = min(n, max_combo_r). Each combination row is scaled by the 1/2^k geometric series. Returns a tensor of shape (num_combinations, r).

**Topological analysis:** Returns a dict with three entries — the cumulative variance curve (structure), the row-wise cosine similarity matrix (relationships), and the normalised singular value vector (mapping).

**Combined score:** `mean(geometry) × mean(combinations) × mean(topology['structure'])` — a single scalar summarising all three dimensions.

---

### 5.3 CombinatorialGenerator

Generates a population of pattern variants through combinatorial enumeration, geometric scaling, and pattern-space projection.

**Generation steps:**

1. Enumerate C(n, r) index combinations with r = min(n, max_combo_r)
2. Scale column k of each row by 1/2^k
3. For each scaled row (up to 16 emitted):
   - Take the top-n indices by absolute value
   - Softmax-weight them
   - Produce a prediction as a weighted sum over the source pattern's rows
4. Filter predictions: keep only those with variance ≥ median variance

**Output dict:**

| Key | Type | Description |
|---|---|---|
| `combinations` | `List[Pattern]` | Combination rows wrapped as Patterns for downstream use |
| `scaled` | `torch.Tensor` | Raw scaled combination matrix, shape (C(n,r), r) |
| `predictions` | `List[Pattern]` | Pattern-space projections of each combination |
| `optimized` | `List[Pattern]` | Variance-filtered subset of predictions |

---

### 5.4 MetaPatternProcessor

Extracts hierarchical structure and pairwise relationships from a population of patterns. Input is typically `[learned_pattern] + generator.generate(learned)['combinations']`.

**Similarity metric** (three-component average):

```
sim(p1, p2) = (cosine(p1, p2) + struct_sim(p1, p2) + feat_sim(p1, p2)) / 3
```

- *Cosine*: on flattened data tensors
- *Structural*: cosine similarity on Sobel edge magnitude maps
- *Feature*: cosine similarity on [mean, std, max, min, median] statistics vectors

**Hierarchy construction:**

Agglomerative clustering by closest-pair merging. At each step: find the pair (i, j) with highest similarity from the remaining set, create a cluster dict with `members`, `similarity`, and `level`, remove j from the remaining set. Continues until fewer than 2 patterns remain.

**Relationship map:**

For each ordered pair (i, j):
- `similarity`: the three-component score above
- `transformation`: a 4×4 matrix encoding translation (from mean difference), rotation (from normalised cross-product angle), and scale (from std ratio)
- `direction`: 2-vector of [angle, magnitude] between the two patterns' gradient fields

**Meta-patterns:**

Per cluster, member feature vectors are averaged and reshaped into the nearest square (n = floor(√length)), then wrapped as a `PatternType.META` Pattern. The cluster's similarity score and level are stored in `properties`.

---

### 5.5 SpaceExplorer

Characterises the pattern's internal geometry and navigates it via depth-first path search.

**Dimensionality analysis:**

Full SVD of the pattern data reshaped to (n, -1). Effective dimensionality = count of singular values whose explained variance exceeds 1%:

```
eff_dims = |{i : σᵢ² / Σσⱼ² > 0.01}|
```

**Boundary detection:**

Finite-difference gradients in x and y, padded to original shape. Edge magnitude = √(∂x² + ∂y²). Boundary mask = edge_magnitude > mean + 2σ.

**Topological fingerprint:**

- *Components*: count of pixels exceeding the mean (connected region proxy)
- *Holes*: |vertical_transitions - horizontal_transitions| / 2 — Euler characteristic proxy
- *Persistence*: top-k differences between consecutive sorted values — approximates 0-dimensional persistence diagram birth/death pairs

**Path search:**

DFS from each of the first 5 nodes. Nodes i and j are adjacent if `‖data[i] - data[j]‖₂ < neighbor_threshold`. Paths of length ≥ 2 are collected. Path optimisation: validate (length ≥ 2, cost < 10⁶), shorten (keep every other intermediate node), penalise by length (`cost × (1 + 0.1 × length)`). Paths are returned sorted by penalised cost.

**Exploration optimisation:**

```
coverage = n_paths / max(eff_dims, 1)
```

Reports number of paths found, best path cost, and coverage ratio.

---

### 5.6 ValidationSystem

Independently applicable to both `Pattern` objects and raw `torch.Tensor` states.

**Pattern validation** returns four tensors: `structure`, `rules`, `consistency`, and `combined` (weighted sum at 0.4 / 0.3 / 0.3).

**State validation** returns four tensors: `known`, `local`, `meta`, and `combined` (element-wise product K × L × M).

Validation is non-destructive — it scores without modifying the input.

---

### 5.7 StateEvolution

Applies the three-factor evolution `F × T × A` to a state tensor at a given integer time step. All three factors produce tensors of the same shape as the input; they are multiplied element-wise.

The time parameter is an integer representing discrete time steps, not wall-clock time. The sigmoid, tanh, and exponential gates all use the time value divided by scale constants (10, 15, 20) to control the rate at which evolution, transition, and adaptation kick in.

---

### 5.8 GraphEvolution

Applies the additive update `N + E + A` to a square graph tensor (adjacency matrix or feature matrix). The returned tensor is the same shape as the input.

Suitable for iterative calling: `G_t+1 = evolution.evolve(G_t)`. The update is deliberately small-magnitude (all components scaled below 0.01) so the graph evolves gradually and does not diverge.

---

### 5.9 PatternFlow

Three-stage pipeline for pre/post-processing a pattern independently of the main recognition pipeline.

**Input stage:** NaN/Inf replacement, z-score normalisation, feature extraction (mean, std, max, min stored in properties).

**Transform stage:** Sigmoid-gated noise injection scaled by time step, renormalisation, time step recorded in properties.

**Output stage:** Clamp to [-10, 10], finalisation flag set in `validation`.

Each stage returns a new `Pattern` — the pipeline is non-destructive and the original input is not modified.

---

### 5.10 CommunicationSystem

Scores the compatibility between any two module objects based on three interface properties:

- *Interface*: ratio of public method counts, modulated by compatibility sigmoid
- *Data transform*: cosine similarity between method-count schema vectors
- *Type mapping*: sigmoid of type-hash difference / 500

The `combined` output is the element-wise product of all three scalars. All values are in (0, 1). Use to audit whether two modules are well-matched before wiring them together in a custom pipeline.

---

### 5.11 ResourceOptimizer

Gradient descent under two optional constraint types:

- Resource constraint: clamps gradient magnitude to the mean absolute value of the constraint tensor
- System constraint: projects gradient onto the null space of the constraint (removes the component parallel to the constraint)

Convergence is checked every step: if `‖update‖ < tolerance`, optimisation terminates early. The efficiency objective rewards high performance (stddev-based) and low resource usage (mean absolute value). The cost objective penalises squared mean and max absolute value.

---

## 6. Profiling System

`SystemProfiler` provides three independent instrumentation modes. It wraps an existing `UnifiedSystem` instance and does not modify it.

### 6.1 Wall-clock profiling

```python
report = profiler.profile(pattern)
SystemProfiler.print_report(report)
```

Each pipeline stage is run independently and timed with `time.perf_counter()`. Stage errors are caught individually — if one stage fails, the timer still reports the others. The printed report shows:

- Per-module time in milliseconds
- Percentage of total time
- ASCII bar chart proportional to time
- Error log if any stage raised

**Return dict:**

| Key | Type | Content |
|---|---|---|
| `timings` | `Dict[str, float]` | Stage name → wall seconds |
| `results` | `Dict[str, Any]` | Stage name → stage output |
| `errors` | `Dict[str, str]` | Stage name → error message (if any) |
| `total_wall_s` | `float` | Sum of all stage times |

### 6.2 cProfile instrumentation

```python
stats = profiler.cprofile(pattern)
SystemProfiler.print_cprofile(stats, n=20)
```

Wraps the full `UnifiedSystem.process_pattern()` call in a `cProfile.Profile` context. Returns a `pstats.Stats` object sorted by cumulative time. `n` controls how many rows to print. The raw `Stats` object can be redirected to file or further filtered using standard `pstats` methods.

### 6.3 Memory footprint estimation

```python
foot = profiler.memory_footprint(pattern)
```

Runs the full pipeline and estimates per-component tensor memory in bytes using `tensor.nelement() × tensor.element_size()`. Reports learned data, geometry tensor, combination tensor, singular values, and a total. This is an estimate of live tensor memory — it does not include Python object overhead, gradient history, or intermediate allocations that have already been freed.

### 6.4 Standalone profiling entry point

```python
python VDJ_Inspired_Algorithm.py
```

Runs in sequence: pipeline smoke-test, wall-clock profile with printed report, memory footprint, and cProfile top-15 callers.

---

## 7. Configuration

### `SystemConfig` parameter reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `num_gpus` | int | required | Number of available GPUs (0 for CPU-only) |
| `num_cpus` | int | required | Number of available CPUs |
| `pattern_size` | int | required | Reference pattern dimensionality |
| `state_dims` | Tuple | required | State tensor shape |
| `batch_size` | int | 128 | Processing batch size |
| `device` | str | auto | `'cuda'` or `'cpu'` |
| `max_combo_r` | int | 8 | Maximum r in C(n,r) |
| `similarity_threshold` | float | 0.8 | Memory match cosine threshold |
| `neighbor_threshold` | float | 1.5 | L2 adjacency radius in SpaceExplorer |
| `max_iterations` | int | 50 | ResourceOptimizer steps |
| `tolerance` | float | 1e-4 | ResourceOptimizer convergence |
| `lambda_balance` | float | 0.5 | Efficiency/cost balance in ResourceOptimizer |
| `learning_rate` | float | 0.01 | ResourceOptimizer step size |

### Combinatorial scaling

The number of combinations generated is `C(n, r)` where `r = min(n, max_combo_r)`. This grows rapidly:

| n | r=4 | r=6 | r=8 | r=10 |
|---|---|---|---|---|
| 10 | 210 | 210 | 45 | 1 |
| 20 | 4,845 | 38,760 | 125,970 | 184,756 |
| 50 | 230,300 | 15,890,700 | 536,878,650 | ~10^10 |
| 100 | 3,921,225 | ~10^9 | ~10^11 | ~10^13 |

For `n > 30`, keep `max_combo_r` at 6 or below. For `n > 50`, keep it at 4 or below. The 1/2^r geometric weighting means that r=4 captures the vast majority of the information content anyway — subsequent terms contribute less than 6% of the weight of the first.

### Device selection

`SystemConfig.device` is auto-set to `'cuda'` if `torch.cuda.is_available()`, otherwise `'cpu'`. All modules respect this setting and move tensors to the correct device at construction time. CUDA memory is only cleared during `ResourceManager.cleanup()` when CUDA is actually available — there is no unconditional CUDA call in the pipeline.

### Embedded tuning

For resource-constrained targets:

```python
config = SystemConfig(
    num_gpus=0,
    num_cpus=1,
    pattern_size=8,
    state_dims=(8, 8),
    batch_size=8,
    max_combo_r=4,        # C(8,4) = 70 combinations — fast
    neighbor_threshold=1.0,
    max_iterations=10,
    tolerance=1e-3,
)
```

For maximum throughput with CUDA:

```python
config = SystemConfig(
    num_gpus=1,
    num_cpus=8,
    pattern_size=64,
    state_dims=(64, 64),
    batch_size=256,
    max_combo_r=8,
    neighbor_threshold=2.0,
    max_iterations=100,
    tolerance=1e-5,
)
```

---

## 8. Usage

### Minimal

```python
from VDJ_Inspired_Algorithm import build_system, make_test_pattern

system, config = build_system(pattern_size=16)
pattern        = make_test_pattern(config)
results        = system.process_pattern(pattern)
```

### Custom input

```python
import torch
from VDJ_Inspired_Algorithm import Pattern, PatternType, build_system

system, config = build_system(pattern_size=32)

data    = torch.tensor(my_2d_array, dtype=torch.float32)
pattern = Pattern(
    data=data,
    type=PatternType.GEOMETRIC,
    scale=1.0,
    properties={'source': 'sensor_array_7'},
    validation={}
)

results = system.process_pattern(pattern)

# Access results
learned_pattern = results['learned']
combined_score  = results['recognition']['combined']
meta_patterns   = results['meta_patterns']['meta_patterns']
best_path       = results['space']['paths'][0] if results['space']['paths'] else None
```

### Using individual modules

Any module can be used standalone without `UnifiedSystem`:

```python
from VDJ_Inspired_Algorithm import (
    SystemConfig, PatternRecognizer, OneShotLearner,
    Pattern, PatternType
)
import torch

config    = SystemConfig(num_gpus=0, num_cpus=4, pattern_size=16,
                          state_dims=(16, 16), max_combo_r=5)
learner   = OneShotLearner(config)
recognizer = PatternRecognizer(config)

for raw in data_stream:
    pattern = Pattern(data=raw.float(), type=PatternType.SEQUENTIAL,
                       scale=1.0, properties={}, validation={})
    learned = learner.learn(pattern)
    result  = recognizer.recognize(learned)
    process(result['combined'])
```

### Profiling

```python
from VDJ_Inspired_Algorithm import build_system, make_test_pattern, SystemProfiler

system, config = build_system(pattern_size=16)
profiler       = SystemProfiler(system, config)
pattern        = make_test_pattern(config)

# Wall-clock breakdown
report = profiler.profile(pattern)
SystemProfiler.print_report(report)

# Function-level cProfile
stats = profiler.cprofile(pattern)
SystemProfiler.print_cprofile(stats, n=25)

# Memory estimate
foot = profiler.memory_footprint(pattern)
print(f"Total estimated memory: {foot['total_estimated']:,} bytes")
```

### Graph evolution (standalone)

```python
from VDJ_Inspired_Algorithm import GraphEvolution, SystemConfig
import torch

config    = SystemConfig(num_gpus=0, num_cpus=1, pattern_size=10,
                          state_dims=(10, 10))
evolution = GraphEvolution(config)

G = torch.randn(10, 10)
for step in range(100):
    G = evolution.evolve(G)

print(G)   # converged graph
```

### State evolution (standalone)

```python
from VDJ_Inspired_Algorithm import StateEvolution, SystemConfig
import torch

config    = SystemConfig(num_gpus=0, num_cpus=1, pattern_size=50,
                          state_dims=(50,))
evolution = StateEvolution(config)

state = torch.randn(50)
for t in range(20):
    state = evolution.evolve(state, t)
```

---

## 9. Design Principles

### Minimal states, maximal output

Following VDJ's biological example: five `PatternType` states, three analysis dimensions, and a handful of scalar configuration parameters produce a highly flexible recognition and generation system. Complexity lives in the mathematics, not in a sprawling state machine.

### Combinatorics over statistics

Where possible, decisions are made combinatorially and geometrically rather than probabilistically. The 1/2^r weighting makes the combination space tractable without sampling — you get the full combinatorial coverage with mathematically principled decay. Statistical methods (softmax, cosine similarity) appear at the output layer for weighting and matching, not as the primary reasoning mechanism.

### Geometric progression as the fundamental primitive

The 1/2^r series appears in four distinct places:

1. `PatternRecognizer._analyze_combinations` — scaling combination columns
2. `CombinatorialGenerator._generate_combinations` — scaling generated combinations
3. `CombinatorialGenerator._apply_geometric_scaling` — post-processing scaling pass
4. Multi-scale analysis at {0.5×, 1.0×, 2.0×} — a geometric scale space

This is deliberate. The progression is the system's primary tool for achieving scale invariance and controlling information density across combinatorial space.

### One-shot generalisation

The memory bank is updated on every call to `OneShotLearner.learn()`. There is no minimum-examples requirement, no batch-size constraint, no epoch loop. A pattern seen once is immediately available for future matching. This is not a limitation — it is a design choice that mirrors VDJ's immediate-response philosophy.

For applications that require more conservative memory updates (e.g., you only want to commit a pattern after seeing it N times), wrap `_update_memory` with a counter gate. The module's interface makes this straightforward without touching any other code.

### Strong decoupling

Modules communicate through the `Pattern` dataclass and Python dicts. No module holds a reference to another. `UnifiedSystem` is thin orchestration — it instantiates modules and sequences calls. Replacing any module is a one-line change in `UnifiedSystem.__init__`.

This decoupling also means modules can be parallelised: `PatternRecognizer` and `CombinatorialGenerator` both operate on the same `learned` pattern and have no dependency on each other's output. They could run concurrently.

### Embedded-first resource management

`ResourceManager` tracks all allocated buffers explicitly. `cleanup()` is called in the `finally` block of `UnifiedSystem.process_pattern()`, guaranteeing buffer release even if a stage raises. All tensor operations are in-place where possible. No dynamic Python structures are grown inside the hot path — lists are pre-bounded by `max_combo_r` and the 16-pattern output cap in `_predict_patterns`.

---

## 10. Complexity and Scaling

### Time complexity per pipeline stage

| Stage | Dominant operation | Complexity |
|---|---|---|
| OneShotLearner | Memory scan (cosine similarity) | O(M × d) where M = memory size, d = feature dim |
| PatternRecognizer (geometric) | Bilinear interpolation × 3 scales | O(n²) |
| PatternRecognizer (combinatorial) | C(n,r) enumeration | O(C(n,r) × r) |
| PatternRecognizer (topology) | SVD | O(min(n,d) × n × d) |
| CombinatorialGenerator | C(n,r) enumeration + projection | O(C(n,r) × n) |
| MetaPatternProcessor (hierarchy) | Pairwise similarity matrix | O(P² × d) where P = population size |
| MetaPatternProcessor (clustering) | Closest-pair search | O(P² × steps) |
| SpaceExplorer (paths) | DFS from 5 seeds | O(n²) worst case |
| SpaceExplorer (SVD) | Full SVD | O(n³) |

The bottleneck for most configurations is the combinatorial enumeration in `PatternRecognizer` and `CombinatorialGenerator`. The 1/2^r geometric weighting provides mathematical justification for the `max_combo_r` cap: beyond r=8, the additional combinations contribute less than 0.4% to the weighted sum.

### Memory complexity

| Component | Memory |
|---|---|
| Feature vector (OneShotLearner) | 27 float32 values = 108 bytes |
| Geometry output | 3 scales × ~36 features = ~432 bytes |
| Combination matrix | C(n,r) × r × 4 bytes |
| Similarity matrix (MetaPatternProcessor) | P² × 4 bytes |
| SVD output (SpaceExplorer) | 3 matrices, dominated by U at n×n |

For `n=16`, `r=6`, `P=17` (16 combinations + 1 learned): total live tensor memory is under 50 KB. For `n=64`, `r=8`, `P=17`: under 5 MB. The system scales well into embedded environments at the recommended settings.

### Throughput characteristics

The system is designed for single-pattern processing with meaningful per-pattern computation, not batched throughput. For high-throughput applications:

- Parallelise at the `process_pattern()` level across independent patterns
- Disable `MetaPatternProcessor` (O(P²) cost) for single-pattern pipelines
- Disable `SpaceExplorer` for patterns where topology is not required
- Reduce `max_combo_r` to 4–5 for real-time constraints

The `OneShotLearner` memory bank is the only shared mutable state in the system. If parallelising, either give each worker its own `UnifiedSystem` instance (separate memory banks) or protect the bank with a lock.
