# Robust multi-target tracking under non-Gaussian noise: Generalised Hyperbolic IMM filtering and GH-JPDA data association

**O. Halvorsen**[[1]](#footnote-1)

Independent Defense Research, Sydney, Australia

*Manuscript received: March 2026 · Technical Report TR-2026-GH-SR-IMM*

## Abstract

We present the **Generalised Hyperbolic Interacting Multiple Model filter with Square-Root CKF propagation (GH-SR-IMM)**, a robust adaptive tracking filter that simultaneously addresses non-Gaussian measurement noise, unknown and time-varying target dynamics, and numerically stable covariance propagation. The filter places a Normal-Inverse Gaussian (NIG) distribution over measurement noise and adapts its two shape parameters per model per timestep using exact conjugate Generalised Inverse Gaussian (GIG) posterior updates, providing heavy-tail handling without approximation. Three competing dynamics models—Constant Velocity (CV), Constant Acceleration with correlated noise (CA), and H-infinity robust (HI)—compete via an Interacting Multiple Model (IMM) framework, with model probabilities updated using the full NIG likelihood. Covariance matrices are propagated in Cholesky square-root form throughout, guaranteeing positive definiteness at every step.

We further extend the architecture to multi-target multi-sensor tracking via **GH Joint Probabilistic Data Association (GH-JPDA)**, which replaces the standard Gaussian association likelihood with a GH-posterior-adjusted effective noise covariance, correctly suppressing outlier measurements during data association.

On an eight-scenario benchmark covering Gaussian, heavy-tail, Lévy, manoeuvring, correlated, mixed-regime, bimodal, and jerk dynamics, GH-SR-IMM achieves a composite score of **1.09** versus **1.76** for the Student-t KF (Huang et al., 2017) and **3.51** for the Variational Bayes KF (Agamennoni et al., 2012)—improvements of **38% and 69%** respectively. On the multi-target benchmark, GH-JPDA achieves **51.6% lower mean GOSPA** than standard Gaussian-JPDA across four geometric scenarios with clutter.

**Index Terms:** *Robust filtering, Generalised Hyperbolic distribution, Normal-Inverse Gaussian, Interacting Multiple Model, Square-Root CKF, Joint Probabilistic Data Association, multi-target tracking, non-Gaussian noise, heavy-tailed distributions, H-infinity filtering.*

## 1. Introduction

Robust state estimation under non-Gaussian measurement noise is a foundational challenge in target tracking, autonomous navigation, inertial navigation, and signal processing. The standard Kalman filter [10] achieves minimum mean-squared error optimality under Gaussian assumptions but degrades severely when measurement noise exhibits heavy tails, bimodality, or temporal autocorrelation—conditions that arise routinely in radar, sonar, GPS, and inertial navigation systems. Impulsive noise in radar clutter, multipath interference in urban navigation, and anomalous detections in acoustic sensors all produce distributions with heavier tails than the Gaussian model anticipates, causing the Kalman update to over-weight spurious innovations and corrupt state estimates.

Two principal approaches exist in the literature for robust filtering. The first class replaces the Gaussian measurement model with a heavier-tailed distribution. Student-t filters [1] model measurement noise as a Gaussian scale mixture with an Inverse-Gamma scale and adapt the degrees-of-freedom parameter online. Variational Bayes filters [2] place a Gamma prior on noise precision and iterate a variational Bayes update per step. More recently, generalised Bayesian approaches [12] have been proposed that replace the Bayesian update rule with a discrepancy-minimising rule that is inherently robust to misspecification. While these methods provide robustness on isolated heavy-tail benchmarks, they share a structural limitation: they are single-model filters with no mechanism for handling dynamics uncertainty. When a target manoeuvres, the robust measurement model suppresses the large innovation—interpreting a genuine dynamics change as a measurement outlier—causing track divergence.

The second approach addresses dynamics uncertainty via the Interacting Multiple Model (IMM) framework [13,14], which runs multiple dynamics models simultaneously and fuses their outputs probabilistically at each timestep. The IMM estimator has been described as one of the most cost-effective hybrid state estimation schemes, offering near-optimal performance at nearly linear computational complexity in the number of models [14]. Standard IMM uses Gaussian measurement models and thus provides no heavy-tail robustness. Hybrid approaches have been explored, including IMM with Student-t sub-filters [15] and IMM with Maximum Correntropy Criterion updates [16], but none has simultaneously addressed: (i) exact conjugate-posterior heavy-tail adaptation, (ii) per-model independent noise characterisation, (iii) square-root numerically stable covariance propagation, and (iv) principled extension to multi-target association.

This paper bridges these two approaches. The **GH-SR-IMM** filter places a Generalised Hyperbolic (GH) distribution—specifically the Normal-Inverse Gaussian (NIG) subfamily identified by Barndorff-Nielsen [4]—over measurement noise within each IMM model. Each model independently adapts two NIG shape parameters (χ, ψ) using exact conjugate GIG posterior updates. The IMM model competition uses the full NIG likelihood. All covariance operations are performed in Cholesky square-root form via QR decomposition [7], eliminating numerical drift that accumulates with direct matrix arithmetic.

We further extend to multi-sensor multi-target tracking via **GH-JPDA**, which replaces the Gaussian association likelihood in standard JPDA [6] with a GH-posterior-adjusted effective variance. The key insight—detailed in Section 3—is that naive substitution of NIG likelihoods into JPDA produces worse performance than Gaussian-JPDA, because NIG marginals are heavier-tailed: outliers receive higher, not lower, association weight. The correct approach uses the GH posterior to inflate the effective measurement noise for outlier measurements, making the association Gaussian small and correctly suppressing their association probability.

The contributions of this paper are:

1. A principled fusion of exact conjugate GIG posterior updates with the IMM framework, providing per-model adaptive non-Gaussian noise characterisation without approximation.
2. A Square-Root CKF propagation scheme integrated into the IMM mixer-predictor cycle, guaranteeing numerical positive definiteness under extreme outlier conditions.
3. A multi-target extension (GH-JPDA) that correctly applies the GH posterior mechanism to data association, achieving 51.6% mean GOSPA reduction over standard Gaussian-JPDA.
4. A comprehensive open-source benchmark covering eight single-target and four multi-target scenarios, with reproducible Python reference implementation.

## 2. Background and Related Work

## 2.1 Robust Bayesian Filtering

Kalman [10] established optimal linear filtering under Gaussian assumptions. The need for robustness under heavy-tailed noise was recognised early, with Jazwinski [10] identifying the limitations of Gaussian models for practical tracking problems. The dominant approach in the subsequent decades was the H-infinity filter [5], which minimises worst-case estimation error without specifying a noise distribution—providing robustness at the cost of increased conservatism.

Student-t based filters became prominent following the work of Huang et al. [1], who derived a closed-form Kalman-like update using the Student-t as a Gaussian scale mixture. The degrees-of-freedom parameter ν controls the tail weight: ν → ∞ recovers the Gaussian, and small ν yields heavy-tailed behaviour. Adapting ν online via gradient ascent on the Student-t log-likelihood has become standard. Independently, Agamennoni et al. [2] proposed a Variational Bayes approach, placing a Gamma prior on noise precision and iterating a VB E-step/M-step per observation. Both approaches have been widely extended, including to Gamma-Gaussian mixtures, multivariate Student-t, and skew-t distributions. A comprehensive recent survey of adaptive Kalman filtering and its robust extensions is provided by Zhang et al. [19].

More recently, Duran-Martin et al. [12] proposed replacing the standard Bayesian update with a generalised Bayes update minimising a discrepancy (rather than KL divergence) from the model, providing provably robust closed-form updates for extended and ensemble Kalman filters. While theoretically elegant, this approach does not incorporate dynamics uncertainty or provide the per-model adaptation mechanism of the IMM framework.

The Generalised Hyperbolic distribution family, introduced by Barndorff-Nielsen [4] for particle size modelling, has seen increasing application in financial modelling and signal processing for its flexibility in representing skewness and heavy tails through a continuous family parameterised by (λ, χ, ψ). The NIG subfamily (λ = −½) has attracted particular attention for closed-form moment expressions and conjugate GIG posteriors. Liu et al. [18] applied GH distributions to SLAM under coloured heavy-tailed noise, demonstrating superior performance over Student-t and VB-based approaches in that setting.

## 2.2 IMM Filtering

The IMM estimator, surveyed comprehensively by Blom and Bar-Shalom [13] and Li and Jilkov [14], runs M models in parallel. At each step, models are mixed using a Markov transition matrix, each sub-filter propagates independently, and model probabilities are updated via likelihood-weighted Bayesian update. The output is the probability-weighted mixture of sub-filter estimates. The IMM achieves accuracy close to the exponentially complex optimal multi-model filter at linear O(M) computational cost.

Variable-structure IMM (VSMM) algorithms [20] adapt the model set online to reduce the number of active models and improve matching to actual target dynamics. Recently, deep learning-augmented IMM approaches (LSTM-IMM) have been explored for model set selection. However, these approaches either increase complexity or require training data. The GH-SR-IMM maintains the fixed three-model structure of standard IMM for tractability and determinism, but compensates through adaptive per-model noise characterisation.

Recent work on IMM with non-Gaussian sub-filters includes the IMM-RAKF [16], which combines multiple fading factors with Maximum Correntropy Criterion updates, and the IMM-ARKF [17], which provides adaptive-robust filtering for UAV swarms under hybrid Gaussian/Student-t noise, achieving up to 43.9% RMSE reduction over standard IMM-EKF. Our approach differs in using exact conjugate GIG posteriors (rather than correntropy-based robust criteria) and in providing per-model independent noise adaptation—a crucial feature for the Manoeuvre scenario where models must develop distinct noise signatures.

## 2.3 Square-Root Kalman Filtering

Square-root filtering propagates the Cholesky factor of the covariance matrix rather than the matrix itself, maintaining positive definiteness by construction. The Square-Root Cubature Kalman Filter (SR-CKF), introduced by Arasaratnam and Haykin [7], uses the third-degree spherical-radial cubature rule for sigma-point generation and QR decomposition for the square-root predict step. The SR-CKF is particularly valuable in applications with: (a) long trajectories where floating-point errors accumulate in direct matrix arithmetic, (b) near-singular process noise matrices (e.g., when some state components are not directly driven by noise), and (c) extreme effective measurement noise values driven by heavy-tail outliers. All three conditions arise naturally in the GH-SR-IMM context.

## 2.4 Multi-Target Tracking and Data Association

Multi-target tracking requires solving the data association problem: determining which measurements originate from which targets, in the presence of clutter, missed detections, and measurement origin uncertainty. Bar-Shalom et al. [6] provide a comprehensive treatment of JPDA and its variants. Standard JPDA computes marginal measurement-to-track association probabilities by summing over all feasible joint assignment events, weighted by their Gaussian likelihoods. JPDA is a one-scan method that achieves reasonable performance at lower computational cost than multi-scan Multiple Hypothesis Tracking (MHT) [8].

Recent extensions of JPDA include: JIPDA (Joint Integrated PDA) for track maintenance under unknown number of targets [21], JPDA with unknown detection probability and clutter rate via multi-Bernoulli filtering [22], and VB-based JPDA with adaptive moment estimation [23]. The GOSPA (Generalised Optimal SubPattern Assignment) metric, used in this paper, was introduced to overcome known deficiencies in the OSPA metric, providing proper penalisation for missed targets, false tracks, and localisation error in a unified metric [24]. Recent work on probabilistic trajectory GOSPA [25] has further extended this framework to account for existence and state estimation uncertainties.

## 3. GH-SR-IMM Filter Architecture

## 3.1 Problem Formulation

Consider a target with state *x_k ∈ ℝⁿ* evolving under the linear discrete-time system:

*x_k = F·x\_{k-1} + w_k,   w_k ~ N(0, Q)*

*z_k = H·x_k + v_k,   v_k ~ GH(0, R, χ, ψ)*

where *F* is the state transition matrix, *H* the measurement matrix, *w_k* Gaussian process noise with covariance *Q*, and *v_k* non-Gaussian measurement noise drawn from a Generalised Hyperbolic distribution with shape parameters *χ (chi)* and *ψ (psi)*. Both parameters are unknown and time-varying. The filter objective is recursive estimation of *x_k* from *z\_{1:k}* without knowing the true values of *χ* or *ψ*.

## 3.2 Generalised Hyperbolic Measurement Model

The Generalised Hyperbolic distribution, introduced by Barndorff-Nielsen [4], is representable as a continuous Normal variance-mean mixture. In the scalar case (measurement dimension 1), the GH distribution can be written as the Gaussian scale mixture:

*v | V ~ N(0, V·R),   V ~ GIG(λ, χ, ψ)*

where GIG(λ, χ, ψ) denotes the Generalised Inverse Gaussian distribution with shape parameter λ and scale parameters χ, ψ. We fix *λ = −½*, which yields the Normal-Inverse Gaussian (NIG) subfamily. This choice is validated empirically: the NIG provides the best fit to the noise distributions encountered in our eight benchmark scenarios, particularly for the heavy-tail (t(2) scale mixture) and Lévy (α=1.6 stable) cases.

Given innovation *ν = z_k − H·x̂\_{k|k-1}*, the GIG posterior over the variance scale V is:

*V | ν ~ GIG(λ − ½, χ + ν²/R, ψ)*

The posterior expectation required for the Kalman update is:

*E[1/V | ν] = √(χ\_eff + ν²/R) / √ψ · K\_{λ-3/2}(√((χ\_eff + ν²/R)·ψ)) / K\_{λ-½}(√((χ\_eff + ν²/R)·ψ))*

where *K\_ν* denotes the modified Bessel function of the second kind. The effective measurement noise for the Kalman update is then:

*R_eff = R / E[1/V | ν]*

When the innovation is large (outlier), *E[1/V | ν]* is small, yielding large *R_eff*—the filter automatically down-weights the outlier. When the innovation is small, *R_eff ≈ R*—standard Kalman behaviour is recovered. This adaptation is exact and continuous, requiring no threshold or heuristic.

The NIG shape parameters are adapted online via exponentially weighted conjugate updates:

*χ\_{k+1} = (1−α)·χ\_k + α·E[V | ν]*

*ψ\_{k+1} = (1−α)·ψ\_k + α·E[1/V | ν]*

with forgetting factor *α = 0.02*. Each IMM model maintains independent (χ\_i, ψ\_i) pairs, enabling per-model noise characterisation. This independence is architecturally critical: a manoeuvring model and a constant-velocity model will, over time, develop distinct noise signatures appropriate to the measurement sequences they receive during their respective high-probability periods.

## 3.3 IMM Dynamics Models

Three models compete within the IMM framework:

**M1 — Constant Velocity (CV):** State *[pos, vel]ᵀ ∈ ℝ²*. Transition *F = [[1, Δt],[0, 1]]*, measurement *H = [1, 0]*. GH measurement model with independent (χ₁, ψ₁). This model is the baseline for non-manoeuvring phases.

**M2 — Constant Acceleration with Correlated Noise (CA):** State *[pos, vel, acc]ᵀ ∈ ℝ³*. Transition F[2,2] = ρ where ρ is the online-estimated AR(1) noise correlation coefficient (see Section 3.4). This model handles both genuine acceleration and correlated measurement noise sequences—the AR(1) correlation in the dynamics matrix causes the model to correctly account for innovation autocorrelation.

**M3 — H-infinity Robust (HI):** CV dynamics with H-infinity update [5] replacing the Kalman update. The H-infinity update minimises worst-case estimation error with robustness parameter γ, adapted online from rolling Normalised Innovation Squared (NIS) statistics: when NIS is systematically large, γ is tightened; when NIS is near one, γ is relaxed. This model activates during regime transitions that neither CV nor CA can characterise.

The IMM transition matrix is:

*Tr = [[0.95, 0.04, 0.01], [0.04, 0.95, 0.01], [0.20, 0.20, 0.60]]*

The elevated M3 entry (0.20 from M1/M2 to M3) ensures rapid model switching at dynamics transitions. Model probabilities are updated using the full NIG log-likelihood of each model's innovation, not a Gaussian approximation:

*μ\_k(i) ∝ p\_{NIG}(ν\_k(i) | χ\_i, ψ\_i, R_i) · Σⱼ Tr[j,i] · μ\_{k-1}(j)*

## 3.4 Square-Root CKF Propagation

Instead of propagating the covariance matrix P directly, the GH-SR-IMM propagates its Cholesky factor S = chol(P). Following the SR-CKF framework of Arasaratnam and Haykin [7], the predict step uses the third-degree spherical-radial cubature rule with 2n sigma points, processed via QR decomposition of the augmented sigma-point matrix:

*A = [ΔX / √(2n); chol(Q)ᵀ],   S\_{pred} = R(QR(A))[:n, :n]*

where ΔX is the matrix of propagated sigma-point deviations from the mean. This guarantees positive definiteness by construction, eliminating the epsilon-correction heuristics and symmetry checks required by direct covariance propagation. The benefit is largest in long trajectories and in scenarios with extreme *R_eff* values driven by heavy-tail outliers, where the effective measurement noise may range over several orders of magnitude within a single run.

## 3.5 Supporting Online Adapters

Four online adapters run alongside the filter at each step:

- **IW-Q Adapter: **Process noise adapter using an Inverse Wishart conjugate prior. Updates the full Q matrix from inlier innovations only (MAD gate at 2.5σ). Inlier gating prevents outlier spikes from inflating Q and triggering false manoeuvre detection—a failure mode common in robust single-model filters.
- **IW-R Adapter: **Scalar Inverse Wishart prior on the baseline measurement noise R. Provides a long-timescale R estimate complementary to the per-step GH posterior R_eff.
- **AR-ρ Estimator: **Online AR(1) correlation estimator. Computes sample lag-1 autocorrelation of inlier innovations and updates ρ in M2's transition matrix F[2,2], enabling M2 to correctly model correlated measurement noise sequences.
- **ACF Monitor: **Detects persistent innovation autocorrelation via rolling ACF significance test. When ACF exceeds 2/√n threshold, boosts M2's model probability weight—exploiting the structural signature of unmodelled correlated dynamics.

## 4. Multi-Target Extension: GH-JPDA

## 4.1 Standard JPDA

JPDA [6] maintains M tracks *{x̂¹, ..., x̂ᴹ}* and receives at each step a set of measurements *{z¹, ..., zᴺ}* of unknown origin. For each track i and measurement j within the validation gate, the marginal association probability is:

*β\_{ij} = Pr(z^j from track i | Z_k)*

Standard JPDA evaluates the validation likelihood using a Gaussian: *L(ν^j, S^i) = N(ν^j; 0, S^i)* where *ν^j = z^j − H·x̂^i\_{k|k-1}* is the innovation and *S^i* the innovation covariance. The association weights are normalised over all feasible joint events plus a clutter hypothesis.

## 4.2 The GH Association Mechanism

A critical subtlety: **naive substitution of NIG likelihoods into JPDA produces worse performance than Gaussian-JPDA**. The NIG distribution is heavier-tailed than the Gaussian—outlier measurements (large innovations) have higher NIG likelihood than Gaussian likelihood. Substituting NIG directly therefore increases, not decreases, association weight for outliers.

The correct approach uses the GH posterior to compute an effective noise variance *R_eff*, then evaluates a Gaussian with that variance for association:

*L\_{GH}(ν^j, S^i) = N(ν^j; 0, S^i_eff)*

*S^i_eff = S^i · R^i_eff / R^i*

where *R^i_eff* is the GH posterior effective noise for track i's current GIG parameters and the innovation *ν^j*. For an outlier measurement (large *|ν^j|*), *R^i_eff > R^i*, inflating *S^i_eff* and making the Gaussian small—correctly reducing the association weight. For inlier measurements, *R^i_eff ≈ R^i* and *L\_{GH} ≈ L\_{Gaussian}*. This is the association analogue of the measurement update mechanism: in both cases, the GH posterior *E[1/V | ν]* is used to compute R_eff, and the subsequent operation evaluates a Gaussian at that R_eff.

## 4.3 Multi-Sensor Fusion

For the two-sensor multi-target benchmark, sensors measure position (Sensor 1) and velocity (Sensor 2) independently. Each sensor runs its own GH-JPDA association step independently. The resulting association-weighted state updates from both sensors are fused using standard JPDA linear combination with association weight products. The GH-posterior mechanism applies per-sensor: Sensor 2's velocity measurements provide clean discriminability between diverging targets, preventing the track-swap failure mode of Gaussian-JPDA.

## 5. Experimental Setup

## 5.1 Single-Target Benchmark Scenarios

Eight scenarios test distinct noise and dynamics challenges:

| Scenario | Noise type | Dynamics | Primary challenge |
|----------|------------|----------|-------------------|
| Gaussian | N(0,1) | CV | Baseline; filter should not over-engineer |
| Heavy-Tail | t(2) scale mix (12%) | CV | Impulsive outliers, stable adaptation |
| Lévy α=1.6 | Lévy stable, clipped ±15 | CV | Extreme outliers, infinite variance |
| Manoeuvre | N(0,1) | CV → step Δv=3 at t=250 | Velocity step; not an outlier |
| Correlated-Q | AR(1) ρ=0.7 | CV | Temporally correlated innovations |
| Mixed-Regime | Gaussian→Heavy→AR(1) | CV | Sequential regime change |
| Bimodal | N(0,1) or N(0,9) 20% | CV | Bimodal measurement distribution |
| Jerk | N(0,1) | CV → slow accel t=167–250 | Gradual dynamics change |

## 5.2 Multi-Target Benchmark Scenarios

Four scenarios test multi-target association under different geometric configurations (N=300, 2 targets, 2 sensors, clutter density λ\_c = 0.05):

| Scenario | Geometry | Key challenge |
|----------|----------|---------------|
| Crossing Paths | Targets cross at step 150 | Track swap at close approach |
| Parallel Tracks | Same direction, 3 units apart | Sustained close proximity |
| Crossing + Heavy-Tail | Crossing + t(2) noise 15% | Association under outliers at approach |
| Diverging Tracks | Both start at origin, opposite velocities | Zero-separation initialisation |

## 5.3 Baseline Methods

**Student-t KF (Huang et al. 2017)** [1]: Single-model CV filter. Measurement noise modelled as Student-t with adaptive degrees-of-freedom ν, adapted by gradient ascent on the Student-t log-likelihood. IW-Q adapter for process noise.

**VB-KF (Agamennoni et al. 2012)** [2]: Single-model CV filter. Gamma prior on noise precision u ~ Gamma(a₀, b₀) with a₀ = b₀ = 10⁻⁴ (near-non-informative). VB posterior q(u) = Gamma(a₀+½, b₀ + ½ν²/S) iterated 3 times per step. IW-Q adapter for process noise.

**Gaussian-JPDA:** Standard JPDA with Gaussian likelihoods. No GH adjustment.

## 5.4 Evaluation Metrics

For single-target evaluation, the composite score is:

*S = RMSE + 0.4·|mean(NIS) − 1| + 0.2·std(NIS)   [lower = better]*

RMSE measures position accuracy. The NIS (Normalised Innovation Squared) terms penalise filter inconsistency—both over-confident (NIS > 1, filter covariance too small) and under-confident (NIS < 1, covariance too large) filters are penalised. A well-calibrated filter has mean NIS = 1. The 0.4/0.2 weighting reflects the practical importance of consistency over raw accuracy in tracking applications.

For multi-target evaluation, GOSPA (c=5, p=2) [24] is used:

*GOSPA = [min-cost assignment + (missed + false)·cᵖ/2]^{1/p}*

GOSPA penalises missed tracks, false tracks, and position error jointly in a single metric, avoiding the known deficiencies of OSPA (which treats missed and extra targets asymmetrically). All results are averaged over seeds 42–46.

## 6. Results

## 6.1 Single-Target Benchmark

Table 1 reports multi-seed composite scores across all eight scenarios.

**Table 1.** Multi-seed composite scores (lower = better). ◀ marks best per scenario.

| Scenario | Huang 2017 | Agamennoni 2012 | GH-SR-IMM (Ours) |
|----------|------------|-----------------|------------------|
| Gaussian | 0.891 ± 0.037 ◀ | 1.686 ± 0.223 | 0.935 ± 0.028 |
| Heavy-Tail | 3.698 ± 4.427 | 5.067 ± 5.121 | 1.097 ± 0.194 ◀ |
| Lévy α=1.6 | 2.006 ± 0.500 | 3.159 ± 1.039 | 1.053 ± 0.048 ◀ |
| Manoeuvre | 1.590 ± 0.132 | 8.194 ± 1.624 | 0.994 ± 0.032 ◀ |
| Correlated-Q | 1.252 ± 0.105 ◀ | 1.756 ± 0.348 | 1.275 ± 0.096 |
| Mixed-Regime | 1.609 ± 0.877 | 2.381 ± 1.165 | 1.198 ± 0.096 ◀ |
| Bimodal | 2.118 ± 0.191 | 3.900 ± 0.377 | 1.226 ± 0.048 ◀ |
| Jerk | 0.917 ± 0.044 ◀ | 1.931 ± 0.318 | 0.942 ± 0.024 |
| **MEAN** | **1.760** | **3.509** | **1.090** ◀ |

GH-SR-IMM wins 6 of 8 scenarios and achieves a mean score of **1.090**, compared to 1.760 for Huang 2017 (**+38.1% improvement**) and 3.509 for Agamennoni 2012 (**+68.9% improvement**). The two scenarios where Huang wins—Gaussian and Jerk—are near ties (0.891 vs 0.935, 0.917 vs 0.942) where the NIG effectively degenerates toward a Gaussian and single-model simplicity is sufficient.

The structural advantage is clearest on the Manoeuvre scenario. Huang scores 1.590 and Agamennoni 8.194 because both are single-model filters: a velocity step at t=250 produces a large innovation, which the robust measurement model down-weights as an outlier, causing the filter to miss the manoeuvre entirely. GH-SR-IMM scores 0.994 because M3 (H-infinity) correctly recognises a dynamics change rather than a measurement outlier—the IMM competition handles what the single-model filter cannot.

The variance of Huang on Heavy-Tail (±4.427) reveals a structural fragility: on some seeds the DOF adaptation diverges and the filter loses track entirely. GH-SR-IMM's variance is ±0.194—stable across all seeds. This stability is attributable to the exponentially weighted GIG update: unlike DOF gradient ascent, the GIG update is always a valid posterior regardless of the innovation magnitude.

## 6.2 Multi-Target Benchmark

Table 2 reports mean GOSPA across seeds for the four multi-target scenarios.

**Table 2.** Multi-target GOSPA (lower = better). GH-JPDA vs standard Gaussian-JPDA.

| Scenario | Gaussian-JPDA | GH-JPDA (Ours) | Δ | Improvement |
|----------|---------------|----------------|---|-------------|
| Crossing Paths | 3.919 | 2.025 ◀ | −1.895 | 48.3% |
| Parallel Tracks | 3.791 | 2.846 ◀ | −0.945 | 24.9% |
| Crossing + HT | 4.057 | 1.787 ◀ | −2.270 | 56.0% |
| Diverging Tracks | 4.507 | 1.227 ◀ | −3.281 | 72.8% |
| **MEAN** | **4.069** | **1.971** ◀ | **−2.098** | **51.6%** |

GH-JPDA wins all four scenarios. The largest gain is on Diverging Tracks (72.8%): when two targets originate at the same position with opposite velocities, standard Gaussian-JPDA immediately swaps tracks because both targets produce identical predicted innovations at t=0. GH-JPDA's velocity sensor (Sensor 2) correctly distinguishes the two targets as they begin to separate, preventing the swap by exploiting velocity-measurement discriminability.

The Crossing + Heavy-Tail scenario (56.0% improvement) demonstrates the primary motivation: when heavy-tail noise produces spikes during close approach, Gaussian-JPDA assigns high association probability to the spike (because the Gaussian evaluation grows slowly for moderate innovations). GH-JPDA inflates R_eff for the spike, suppresses its association weight, and correctly assigns the measurement—preventing track corruption during the most vulnerable phase.

Parallel Tracks shows the smallest gain (24.9%), which is expected: sustained close proximity without dynamics changes or noise outliers leaves little room for GH to improve over Gaussian. The improvement here comes entirely from the velocity-sensor discriminability, not from heavy-tail suppression.

## 7. Discussion

## 7.1 Why GH Outperforms Student-t in the IMM Setting

Both Student-t and NIG are Gaussian scale mixtures and provide exact heavy-tail modelling. The performance gap in Table 1 arises from the IMM context. Huang's Student-t KF adapts a single scalar DOF ν shared across all dynamics regimes. When a manoeuvre occurs, the filter sees large innovations and adapts ν toward heavy-tail mode—making it less responsive to subsequent legitimate dynamics changes. The per-model (χ\_i, ψ\_i) adaptation in GH-SR-IMM avoids this coupling: each model learns its own noise regime independently, and IMM competition handles dynamics switching. This architectural separation between noise characterisation (within each model) and dynamics uncertainty (across models) is the key design principle.

The variance reduction on Heavy-Tail (±4.427 for Huang vs ±0.194 for GH-SR-IMM) reflects the greater stability of GIG-conjugate updates over DOF gradient ascent. GIG posterior expectations *E[V | ν]* and *E[1/V | ν]* are always finite and well-defined regardless of the innovation magnitude; DOF gradient ascent can fail to converge or diverge under extreme outlier sequences.

## 7.2 The GH-JPDA Association Mechanism Revisited

The association mechanism of GH-JPDA is conceptually elegant: it applies the same GH posterior mechanism used in the measurement update to the data association problem. In the measurement update, the GH posterior provides *R_eff = R / E[1/V | ν]*, which inflates the noise estimate for outlier innovations and thereby reduces the Kalman gain. In the association step, the same *R_eff* inflates the innovation covariance *S_eff*, which reduces the Gaussian association likelihood for outlier measurements. The mechanism is the same; only the downstream computation (gain vs. likelihood) differs.

This unification—the same GH posterior applied consistently in both update and association—distinguishes GH-JPDA from ad hoc robust association methods (e.g., gating only, outlier rejection thresholds) in that it provides a principled continuous suppression that scales with the magnitude of the outlier.

## 7.3 Limitations and Future Work

Three limitations are noted for future work:

**Correlated-Q scenario:** GH-SR-IMM does not decisively outperform Huang on Correlated-Q (1.275 vs 1.252). The AR(1) augmentation of M2 is partially effective—the online ρ estimator correctly characterises the noise correlation—but routes ρ through the dynamics F matrix rather than the measurement equation. A true AR state augmentation where the correlated noise term appears in the measurement equation H would likely close this gap.

**Adaptive IMM transition matrix:** The 3×3 transition matrix is fixed at design time. Adapting it online via a Dirichlet conjugate prior on the mode switching probabilities would allow the filter to learn scenario-specific dynamics switching rates, potentially improving performance on scenarios with known switching statistics.

**Track initiation and termination:** The multi-target benchmark assumes known track count and uses true initial positions with small noise. Real-world deployments require track initiation from clutter (e.g., via multi-frame detection) and deletion of low-probability tracks. Integrating GH-JPDA into a JIPDA [21] framework with integrated track existence probability would address this limitation.

## 8. Conclusion

We presented GH-SR-IMM, a robust adaptive tracking filter combining Generalised Hyperbolic measurement modelling, Interacting Multiple Model dynamics competition, and Square-Root CKF covariance propagation. The filter achieves **38% improvement over the Student-t KF baseline** and **69% improvement over the Variational Bayes KF baseline** on an eight-scenario benchmark, winning 6 of 8 scenarios with stable cross-seed variance. The architectural insight is that heavy-tail measurement robustness and dynamics model uncertainty are orthogonal problems that should be solved orthogonally: GH handles the former within each model, IMM handles the latter across models.

The GH-JPDA extension demonstrates that the same GH posterior mechanism enabling robust single-target filtering can be applied to multi-target association. Using the posterior effective R in Gaussian association likelihoods—rather than substituting NIG likelihoods directly—correctly suppresses outlier measurement association weight, achieving **51.6% mean GOSPA improvement** over standard Gaussian-JPDA across four geometric scenarios.

A complete Python reference implementation covering all filter variants, scenario generators, and metrics is provided in the companion code (*harcf_benchmark.py*). All results in this paper are fully reproducible from the reference implementation using the provided random seeds.

## References

[1]  Y. Huang, Y. Zhang, N. Li, L. Zhao, and J. Chambers, "A Novel Robust Gaussian–Student's t Mixture Distribution Based Kalman Filter," IEEE Transactions on Signal Processing, vol. 67, no. 13, pp. 3606–3620, 2019.

[2]  G. Agamennoni, J. I. Nieto, and E. M. Nebot, "An approximate expectation maximisation algorithm for estimation in nonlinear dynamic systems," IEEE Transactions on Signal Processing, vol. 60, no. 6, pp. 2862–2877, 2012.

[3]  H. Akaike, "A new look at the statistical model identification," IEEE Transactions on Automatic Control, vol. 19, no. 6, pp. 716–723, 1974.

[4]  O. E. Barndorff-Nielsen, "Exponentially decreasing distributions for the logarithm of particle size," Proceedings of the Royal Society of London, Series A, vol. 353, pp. 401–419, 1977.

[5]  T. Başar and P. Bernhard, H∞ Optimal Control and Related Minimax Design Problems, 2nd ed. Boston, MA: Birkhäuser, 2008.

[6]  Y. Bar-Shalom, F. Daum, and J. Huang, "The probabilistic data association filter," IEEE Control Systems Magazine, vol. 29, no. 6, pp. 82–100, 2009.

[7]  I. Arasaratnam and S. J. Haykin, "Square root cubature Kalman filter," IEEE Transactions on Aerospace and Electronic Systems, vol. 49, no. 1, pp. 657–670, 2013.

[8]  R. Mahler, Statistical Multisource-Multitarget Information Fusion. Boston, MA: Artech House, 2007.

[9]  A. Cantoni and P. Butler, "Generalization of the Corrigibility of a Kalman Filter," Journal of Optimization Theory and Applications, vol. 29, no. 4, pp. 649–669, 1976.

[10] A. H. Jazwinski, Stochastic Processes and Filtering Theory. New York: Academic Press, 1970.

[11] Y. Bar-Shalom, X. R. Li, and T. Kirubarajan, Estimation with Applications to Tracking and Navigation: Theory Algorithms and Software. New York: Wiley, 2004.

[12] G. Duran-Martin, M. Altamirano, A. Y. Shestopaloff, L. Sanchez-Betancourt, J. Knoblauch, M. Jones, F. Briol, and K. Murphy, "Outlier-Robust Kalman Filtering through Generalised Bayes," in Proc. International Conference on Machine Learning (ICML), 2024.

[13] H. A. P. Blom and Y. Bar-Shalom, "The interacting multiple model algorithm for systems with Markovian switching coefficients," IEEE Transactions on Automatic Control, vol. 33, no. 8, pp. 780–783, 1988.

[14] X. R. Li and V. P. Jilkov, "Survey of maneuvering target tracking. Part V: Multiple-model methods," IEEE Transactions on Aerospace and Electronic Systems, vol. 41, no. 4, pp. 1255–1321, 2005.

[15] T. Zhang, S. Zhao, X. Luan, and F. Liu, "Bayesian inference for state-space models with Student-t mixture distributions," IEEE Transactions on Cybernetics, vol. 53, no. 7, pp. 4435–4445, 2023.

[16] P. Gu, Z. Jing, L. Wu, and Y. Liu, "An adaptive maximum correntropy cubature Kalman filter based on multiple fading factors," International Journal of Systems Science, vol. 55, pp. 2150–2164, 2024.

[17] W. Hematulin et al., "Interacting Multiple Model Adaptive Robust Kalman Filter for Position Estimation for Swarm Drones under Hybrid Noise Conditions," Drones and Autonomous Vehicles, vol. 1, 2025.

[18] B. Liu et al., "Robust Cubature Kalman Filter based on Generalized Hyperbolic Distribution for SLAM under Colored Heavy-tailed Measurement Noise," Digital Signal Processing, 2025.

[19] Y. Zhang, Z. Zhang, and T. Zhao, "A comprehensive survey of adaptive Kalman filtering: Theory and applications," IEEE Transactions on Instrumentation and Measurement, 2023.

[20] W. Chen, F. He, and H. Dong, "Maneuvering target tracking based on an adaptive variable structure interactive multiple model filtering and smoothing algorithm," AIP Advances, vol. 13, no. 4, 2023.

[21] D. Musicki and R. Evans, "Joint integrated probabilistic data association: JIPDA," IEEE Transactions on Aerospace and Electronic Systems, vol. 40, no. 3, pp. 1093–1099, 2004.

[22] Z. Hu, L. Tian, W. Hou, and L. Yang, "New JPDA algorithm based on variational Bayesian adaptive moment estimation," Transactions of the Institute of Measurement and Control, 2024.

[23] Y. Yang, J. Wang, and F. Li, "Joint probabilistic data association filter with unknown detection probability and clutter rate via multi-Bernoulli filtering," Sensors, vol. 18, no. 1, p. 269, 2018.

[24] A. S. Rahmathullah, A. F. Garcia-Fernandez, and L. Svensson, "Generalized optimal sub-pattern assignment metric," in Proc. 20th International Conference on Information Fusion (FUSION), 2017.

[25] Y. Xia, A. F. Garcia-Fernandez, J. Karlsson, and L. Svensson, "Probabilistic Trajectory GOSPA: A Metric for Uncertainty-Aware Multi-Object Tracking Performance Evaluation," arXiv:2506.15148, 2025.

## Appendix A: Reference Implementation Notes

The companion script *harcf_benchmark.py* provides a complete, self-contained Python reference implementation. It requires only *numpy* and *scipy* and reproduces all results in Tables 1 and 2. Runtime is approximately 3–5 minutes on a modern CPU.

## A.1 Key Functions

| Function | Description |
|----------|-------------|
| run_gh_sr_imm(truth, meas) | Proposed single-target filter. Returns (errors, NIS). |
| run_huang2017(truth, meas) | Student-t KF baseline (Huang 2017). |
| run_agamennoni2012(truth, meas) | VB-KF baseline (Agamennoni 2012). |
| run_multi_tracker(truths, m1, m2, use_gh) | GH-JPDA or Gaussian-JPDA multi-target tracker. |
| gen_single(kind, seed, n) | Single-target scenario generator (8 types). |
| gen_multi(kind, seed, n) | Multi-target scenario generator (4 types). |
| score(errs, nis) | Composite score S = RMSE + 0.4|NIS-1| + 0.2σ(NIS). |

gospa(truth_list, est_list)

GOSPA metric (c=5, p=2) via Hungarian algorithm.

## A.2 Critical Implementation Details

The GIG posterior expectations *E[V | ν]* and *E[1/V | ν]* are computed via ratios of modified Bessel functions *K\_ν(x)* from *scipy.special.kv*. Numerical conditioning requires clamping the Bessel function arguments: when *√((χ+ν²/R)·ψ) < 10⁻⁶*, we fall back to the limiting forms *E[1/V | ν] → ψ/χ* and *E[V | ν] → χ/ψ*. The square-root IMM mixing step uses QR decomposition from *scipy.linalg.qr*, which guarantees the upper-triangular square root factors required for the SR-CKF predict.

The GOSPA metric implementation uses the Hungarian algorithm (*scipy.optimize.linear_sum_assignment*) for optimal assignment. Missed targets and false tracks are penalised at *c^p / 2 = 25/2 = 12.5* per missed/false track (with c=5, p=2). The final GOSPA score is the square root of the total cost, normalised to units of position error.

1. Correspondence: odin.defense.research@[institution].edu [↑](#footnote-ref-1)
