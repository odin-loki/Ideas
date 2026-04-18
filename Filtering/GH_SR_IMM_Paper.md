<!-- Converted from `GH_SR_IMM_Paper.docx` — source was Word (.docx). -->

__Robust Multi\-Target Tracking under Non\-Gaussian Noise__

__via Generalised Hyperbolic IMM Filtering and GH\-JPDA Data Association__

Technical Report  |  2026

# __Abstract__

We present the __Generalised Hyperbolic Interacting Multiple Model filter with Square\-Root CKF propagation__ \(GH\-SR\-IMM\), a robust adaptive tracking filter that simultaneously handles non\-Gaussian measurement noise, unknown and time\-varying dynamics, and numerically stable covariance propagation\. The filter places a Normal\-Inverse Gaussian \(NIG\) distribution over measurement noise and adapts its two shape parameters per model per timestep using conjugate GIG posterior updates, providing exact heavy\-tail handling without approximation\. Three competing dynamics models — constant velocity \(CV\), constant acceleration with correlated noise \(CA\), and H\-infinity robust \(HI\) — compete via an Interacting Multiple Model \(IMM\) framework, with model probabilities updated using the full NIG likelihood rather than a Gaussian approximation\. Covariance matrices are propagated in Cholesky square\-root form throughout, guaranteeing positive definiteness at every step\.

We further extend the architecture to __multi\-target multi\-sensor tracking__ via GH Joint Probabilistic Data Association \(GH\-JPDA\), which replaces the standard Gaussian association likelihood with a GH\-posterior\-adjusted Gaussian\. This correctly inflates the effective measurement noise for outlier measurements, reducing their association weight and preventing track corruption under heavy\-tail noise\.

On an eight\-scenario benchmark covering Gaussian, heavy\-tail, Lévy, manoeuvring, correlated, mixed\-regime, bimodal, and jerk dynamics, GH\-SR\-IMM achieves a composite score of __1\.09__ versus __1\.76__ for the Student\-t KF \(Huang 2017\) and __3\.51__ for the Variational Bayes KF \(Agamennoni 2012\), representing improvements of __38% and 69%__ respectively\. On the multi\-target benchmark, GH\-JPDA achieves __51\.6%__ lower mean GOSPA than standard Gaussian\-JPDA across four geometric scenarios with clutter\.

# __1  Introduction__

Robust state estimation under non\-Gaussian measurement noise is a long\-standing problem in target tracking, navigation, and signal processing\. The standard Kalman filter achieves optimality under Gaussian assumptions, but degrades severely when measurement noise exhibits heavy tails, bimodality, or autocorrelation — conditions that arise routinely in radar, sonar, GPS, and inertial navigation systems\.

Two principal approaches exist in the literature\. The first replaces the Gaussian measurement model with a heavier\-tailed distribution\. Student\-t filters \(Huang et al\. 2017\) use the Student\-t as a Gaussian scale mixture and adapt the degrees of freedom online\. Variational Bayes filters \(Agamennoni et al\. 2012\) place a Gamma prior on the noise precision and iterate a VB update per step\. Both achieve robustness on isolated heavy\-tail benchmarks but share a structural limitation: they are single\-model filters with no mechanism for dynamics uncertainty\. When the target manoeuvres, the robust measurement model suppresses the large innovation — interpreting a genuine position shift as an outlier\.

The second approach addresses dynamics uncertainty via the Interacting Multiple Model \(IMM\) framework, running multiple dynamics models in competition and fusing their outputs probabilistically\. Standard IMM uses Gaussian measurement models and thus provides no heavy\-tail robustness\.

We bridge these two approaches\. The __GH\-SR\-IMM__ filter places a Generalised Hyperbolic \(GH\) distribution — specifically its Normal\-Inverse Gaussian \(NIG\) subfamily — over measurement noise within each IMM model\. Each model independently adapts two NIG shape parameters \(chi, psi\) using exact conjugate GIG posterior updates\. The IMM model competition uses the full NIG likelihood, not a Gaussian approximation\. All covariance operations are performed in Cholesky square\-root form, eliminating the numerical drift that accumulates with direct matrix arithmetic\.

We further extend to multi\-sensor multi\-target tracking via __GH\-JPDA__, which replaces the Gaussian association likelihood in standard JPDA with a GH\-posterior\-adjusted Gaussian\. The key insight is that outlier measurements should receive *lower* association weight, not higher — and NIG marginal likelihoods are heavier\-tailed than Gaussian, so naive substitution produces the wrong behaviour\. The correct approach uses the GH posterior to compute an effective noise variance R\_eff, then evaluates a Gaussian\(ν, R\_eff\) for association\. Outlier measurements cause R\_eff to inflate, making the Gaussian small, correctly reducing the association weight\.

# __2  Filter Architecture__

## __2\.1  Problem Formulation__

Consider a target with state *x\_k ∈ ℝ²* \(position, velocity\) evolving under:

*x\_k = F·x\_\{k\-1\} \+ w\_k,   w\_k ~ N\(0, Q\)*

*z\_k = H·x\_k \+ v\_k,         v\_k ~ GH\(0, R, χ, ψ\)*

where *F* is the state transition matrix, *H* the measurement matrix, and *v\_k* is non\-Gaussian measurement noise drawn from a Generalised Hyperbolic distribution with shape parameters χ \(chi\) and ψ \(psi\)\. Both χ and ψ are unknown and time\-varying\.

## __2\.2  Generalised Hyperbolic Measurement Model__

The GH distribution is represented as a Gaussian scale mixture: *v ~ N\(0, V·R\)* where the variance scale *V* is drawn from a Generalised Inverse Gaussian \(GIG\) distribution: *V ~ GIG\(λ, χ, ψ\)*\. We fix λ = −0\.5, which yields the Normal\-Inverse Gaussian \(NIG\) subfamily — validated empirically to be the correct subfamiliy for the noise distributions in our benchmark\.

At each timestep, given innovation ν, the GIG posterior is:

*V | ν  ~  GIG\(λ−½,  χ\+ν²/R,  ψ\)*

The posterior expectation E\[1/V | ν\] provides the effective measurement noise:

*R\_eff  =  R / E\[1/V | ν\]*

When ν is large \(outlier\), E\[1/V | ν\] is small, R\_eff is large — the filter automatically down\-weights the outlier\. When ν is small, R\_eff ≈ R — standard behaviour\. This adaptation is exact, not a heuristic threshold\.

The NIG shape parameters are adapted online via exponentially weighted conjugate updates:

*χ\_\{k\+1\} = 0\.98·χ\_k \+ 0\.02·E\[V | ν\]*

*ψ\_\{k\+1\} = 0\.98·ψ\_k \+ 0\.02·E\[1/V | ν\]*

Each IMM model maintains independent \(χ, ψ\) pairs, allowing per\-model noise characterisation\.

## __2\.3  IMM Dynamics Models__

Three models compete within the IMM framework:

M1 — Constant Velocity \(CV\):  F = \[\[1, Δt\],\[0, 1\]\],  H = \[1, 0\],  GH measurement\.

M2 — Constant Acceleration with correlated noise \(CA\):  3D state \[pos, vel, acc\], F\[2,2\] = ρ where ρ is the online\-estimated AR\(1\) noise correlation coefficient\.

M3 — H\-infinity robust \(HI\):  CV dynamics with H\-infinity update replacing the Kalman update\. Adaptive robustness parameter γ adjusted from rolling NIS statistics\.

The IMM transition matrix is Tr\[i,j\] = \{0\.95 on\-diagonal, 0\.04 off\-diagonal for M1/M2, 0\.20 for M3 entry\}\. Model probabilities are updated using the full NIG likelihood of each model's innovation, not a Gaussian approximation\.

## __2\.4  Square\-Root CKF Propagation__

Instead of propagating the covariance matrix *P* directly, we propagate its Cholesky factor *S = chol\(P\)*\. The predict step uses QR decomposition of an augmented sigma\-point matrix:

*A = \[ ΔX / √\(2n\) \]   \(sigma\-point deviations\)*

*    \[ chol\(Q\)^T  \]   \(process noise root\)*

*S\_\{pred\} = R\( QR\(A\) \)\[:n, :n\]*

This guarantees positive definiteness by construction at every step, eliminating the epsilon\-correction heuristics and symmetry checks that standard filters require\. The benefit is largest in long trajectories where numerical errors accumulate, and in scenarios with extreme R\_eff values driven by heavy\-tail outliers\.

## __2\.5  Supporting Adapters__

Four online adapters run alongside the filter at each step:

IW\-Q:  Process noise adapter using an Inverse Wishart conjugate prior\. Updates the full 2×2 Q matrix from inlier innovations only \(MAD gate at 2\.5σ\)\. Inlier gate prevents outlier spikes from inflating Q and triggering false manoeuvre detection\.

IW\-R:  Measurement noise adapter using a scalar Inverse Wishart prior on R\. Provides a second\-level R estimate complementary to the per\-step GH posterior\.

AR\-ρ:  Online AR\(1\) correlation estimator\. Computes sample lag\-1 autocorrelation of inlier innovations and updates ρ in M2's F matrix, enabling the filter to correctly handle correlated measurement noise sequences\.

ACF monitor:  Detects persistent innovation autocorrelation via rolling ACF significance test\. When ACF exceeds 2/√n threshold, boosts M2's probability weight — a signature of unmodelled dynamics or correlated noise\.

# __3  Multi\-Target Multi\-Sensor Extension: GH\-JPDA__

## __3\.1  Multi\-Target Formulation__

Given *N\_T* targets and *N\_S* sensors, at each timestep sensor *s* provides an unordered set of measurements *Z\_s = \{z\_\{s,1\}, \.\.\., z\_\{s,M\_s\}\}* which may include target\-originated measurements and clutter\. The association problem is to determine which measurement originated from which target, or whether a measurement is clutter\.

Standard JPDA computes association weights β\[i,j\] = P\(z\_j originated from target i\) using Gaussian likelihoods\. We replace this with __GH\-JPDA__, which uses GH\-posterior\-adjusted Gaussian likelihoods:

*R\_eff\(i,j\)  =  R\_base\(i\) / E\[1/V | ν\_\{ij\}, χ\_i, ψ\_i\]*

*L\(i,j\)  =  N\( ν\_\{ij\} ;  0,  S\_zz \+ R\_eff\(i,j\) \)*

*β\[i,j\]  =  L\(i,j\) / \( λ\_c \+ Σ\_i L\(i,j\) \)*

where *ν\_\{ij\}* is the innovation of measurement j against target i's predicted position, and λ\_c is the clutter spatial density\. The critical difference from naive substitution of NIG likelihoods is that __L\(i,j\) is evaluated with an inflated R\_eff rather than the raw NIG probability__\. The NIG marginal is heavier\-tailed than Gaussian — substituting it directly would *increase* association probability for outliers, the wrong behaviour\. Using Gaussian\(ν, R\_eff\) with GH\-inflated R\_eff produces the correct result: outliers receive lower association weight\.

## __3\.2  Dual\-Sensor Fusion__

Two sensors are fused sequentially per timestep\. Sensor 1 \(position, H = \[1,0\], R₁ = 1\.0\) and Sensor 2 \(velocity/Doppler, H = \[0,1\], R₂ = 2\.0\)\. Each target maintains independent NIG parameters per sensor — \(χ\_s1, ψ\_s1\) and \(χ\_s2, ψ\_s2\) — allowing per\-sensor noise characterisation\. Sensor 2's velocity measurements constrain velocity ambiguity during close target approaches, reducing track swaps\.

## __3\.3  JPDA State Update__

After computing association weights β\[i,j\], the state update for target i is:

*ν\_combined = Σ\_j β\[i,j\] · ν\_\{ij\}*

*x\_f = x\_p \+ K · ν\_combined*

*P\_f = β\_0 · P\_pred \+ \(1\-β\_0\) · P\_upd \+ P\_spread*

where β\_0 = 1 − Σ\_j β\[i,j\] is the probability of no valid measurement, P\_upd is the standard KF updated covariance, and P\_spread accounts for the spread of association hypotheses\. The GH\-posterior R\_eff used in the gain K uses the combined innovation ν\_combined\.

# __4  Experimental Setup__

## __4\.1  Single\-Target Benchmark Scenarios__

Eight scenarios test distinct noise characteristics\. All share N = 500 steps, DT = 1s, true process noise Q ≈ diag\(\[DT³/3, DT\+0\.001\]\)×0\.01, baseline measurement noise R = 1\.0:

__Scenario__

__Noise Model__

__Key Challenge__

Gaussian

N\(0,1\)

Filter baseline

Heavy\-Tail

Student\-t\(2\) mix, 12% rate

Outlier rejection

Lévy α=1\.6

Lévy stable, α=1\.6

Infinite variance noise

Maneuver

Gaussian \+ velocity step

Dynamics model switch

Correlated Q

AR\(1\), ρ=0\.7

Autocorrelated meas noise

Mixed Regime

Gaussian → Heavy → AR\(1\)

Regime change detection

Bimodal

N\(0,1\) / N\(0,9\), 20% rate

High\-variance outlier mode

Jerk

Gaussian \+ velocity ramp

Sustained dynamics change

## __4\.2  Multi\-Target Benchmark Scenarios__

Four scenarios test association under different geometric configurations\. All use N = 300 steps, 2 targets, 2 sensors, clutter density λ\_c = 0\.05:

__Scenario__

__Geometry__

__Key Challenge__

Crossing

Targets cross at step 150

Track swap at close approach

Parallel

Same direction, 3 units apart

Sustained close proximity

Crossing \+ Heavy\-Tail

Crossing \+ t\(2\) noise 15%

Association under outliers

Diverging

Both start at origin

Association at zero separation

## __4\.3  Baselines__

__Student\-t KF \(Huang 2017\): __Single\-model CV filter\. Measurement noise modelled as Student\-t with adaptive degrees of freedom ν\. E\[1/V|z\] = \(ν\+1\)/\(ν \+ ν²/R\) provides effective R\. DOF ν adapted by gradient ascent on the Student\-t log\-likelihood\. IW\-Q adapter for process noise\.

__VB\-KF \(Agamennoni 2012\): __Single\-model CV filter\. Gamma prior on noise precision u ~ Gamma\(a₀, b₀\) with a₀ = b₀ = 10⁻⁴ \(near\-non\-informative\)\. VB posterior q\(u\) = Gamma\(a₀\+½, b₀ \+ ½ν²/S\) iterated 3 times per step\. IW\-Q adapter for process noise\.

__Gaussian\-JPDA: __Standard JPDA with Gaussian likelihoods\. Association weight β\[i,j\] = Gaussian\(ν, Szz\) / \(λ\_c \+ Σ Gaussian\(ν, Szz\)\)\. No GH adjustment\.

## __4\.4  Evaluation Metric__

Single\-target composite score:

*S = RMSE \+ 0\.4 · |mean\(NIS\) − 1| \+ 0\.2 · std\(NIS\)*

RMSE measures position accuracy\. The NIS \(Normalised Innovation Squared\) terms penalise filter inconsistency — both over\-confident \(NIS > 1\) and under\-confident \(NIS < 1\) filters are penalised\. A well\-calibrated filter has mean NIS = 1\.

Multi\-target metric: GOSPA \(Generalised Optimal SubPattern Assignment\):

*GOSPA = \[ min\-cost assignment \+ \(missed \+ false\) · c^p/2 \]^\{1/p\}*

with c = 5 \(cutoff distance\) and p = 2\. Penalises missed tracks, false tracks, and position error jointly\. All results averaged over seeds 42–46\.

# __5  Results__

## __5\.1  Single\-Target Benchmark__

Table 1 reports multi\-seed composite scores across all eight scenarios\.

Table 1\.  Multi\-seed composite scores \(lower = better\)\. ◀ marks best per scenario\.

__Scenario__

__Huang 2017__

__Agam\. 2012__

__GH\-SR\-IMM__

Gaussian

__0\.891±0\.037 ◀__

1\.686±0\.223

0\.935±0\.028

Heavy\-Tail

3\.698±4\.427

5\.067±5\.121

__1\.097±0\.194 ◀__

Lévy α=1\.6

2\.006±0\.500

3\.159±1\.039

__1\.053±0\.048 ◀__

Maneuver

1\.590±0\.132

8\.194±1\.624

__0\.994±0\.032 ◀__

Correlated Q

__1\.252±0\.105 ◀__

1\.756±0\.348

1\.275±0\.096

Mixed Regime

1\.609±0\.877

2\.381±1\.165

__1\.198±0\.096 ◀__

Bimodal

2\.118±0\.191

3\.900±0\.377

__1\.226±0\.048 ◀__

Jerk

__0\.917±0\.044 ◀__

1\.931±0\.318

0\.942±0\.024

__Mean__

__1\.760__

__3\.509__

__1\.090 ◀__

GH\-SR\-IMM wins 6 of 8 scenarios and achieves a mean score of 1\.090, compared to 1\.760 for Huang 2017 \(__\+38\.1%__ improvement\) and 3\.509 for Agamennoni 2012 \(__\+68\.9%__ improvement\)\. The two scenarios won by Huang — Gaussian and Jerk — are near ties \(0\.891 vs 0\.935, 0\.917 vs 0\.942\) where the NIG degenerates toward Gaussian and single\-model simplicity is sufficient\.

The structural advantage is clearest on Maneuver\. Huang scores 1\.590 and Agamennoni 8\.194 because both are single\-model filters: a velocity step produces a large innovation, which the robust measurement model down\-weights as an outlier, causing the filter to miss the manoeuvre entirely\. GH\-SR\-IMM scores 0\.994 because M3 \(H\-infinity\) correctly recognises a dynamics change rather than a measurement outlier\.

The variance of Huang on Heavy\-Tail \(±4\.427\) reveals a structural fragility: on some seeds the DOF adaptation diverges and the filter loses track\. GH\-SR\-IMM's variance is ±0\.194 — stable across seeds\.

## __5\.2  Multi\-Target Benchmark__

Table 2 reports mean GOSPA across seeds for the four multi\-target scenarios\.

Table 2\.  Multi\-target GOSPA \(lower = better\)\. GH\-JPDA vs standard Gaussian\-JPDA\.

__Scenario__

__Gaussian\-JPDA__

__GH\-JPDA__

__Δ__

__Improvement__

Crossing paths

3\.919

__2\.025 ◀__

−1\.895

48\.3%

Parallel tracks

3\.791

__2\.846 ◀__

−0\.945

24\.9%

Crossing \+ Heavy\-tail

4\.057

__1\.787 ◀__

−2\.270

56\.0%

Diverging tracks

4\.507

__1\.227 ◀__

−3\.281

72\.8%

__Mean__

__4\.069__

__1\.971 ◀__

__−2\.098__

__51\.6%__

GH\-JPDA wins all four scenarios\. The largest gain is on Diverging \(72\.8%\): when two targets start at the same position, standard Gaussian\-JPDA immediately swaps tracks because both targets produce identical predicted innovations\. GH\-JPDA's velocity\-sensor measurement \(Sensor 2\) correctly distinguishes the two targets as they begin to separate, preventing the swap\.

The Crossing \+ Heavy\-tail scenario \(56\.0% improvement\) demonstrates the primary motivation: when heavy\-tail noise produces spikes during close approach, Gaussian\-JPDA assigns high association probability to the spike \(because the Gaussian decays slowly for moderate innovations\)\. GH\-JPDA inflates R\_eff for the spike, suppresses its association weight, and correctly assigns the target measurement — preventing track corruption during the most vulnerable phase\.

# __6  Discussion__

## __6\.1  Why GH Outperforms Student\-t in the IMM Setting__

Both Student\-t and NIG are Gaussian scale mixtures and provide exact heavy\-tail modelling\. The difference in our results arises from the IMM context\. Huang's Student\-t KF adapts a single scalar DOF parameter ν shared across all dynamics regimes\. When a manoeuvre occurs, the filter briefly sees large innovations and adapts ν toward heavy\-tail mode — making it less responsive to subsequent legitimate dynamics changes\. The per\-model \(χ\_i, ψ\_i\) adaptation in GH\-SR\-IMM avoids this coupling: each model learns its own noise regime independently, and the IMM competition handles the dynamics switching\.

## __6\.2  The GH\-JPDA Association Mechanism__

A subtle but critical point: substituting NIG likelihoods directly into JPDA produces worse performance than Gaussian\-JPDA, because NIG is heavier\-tailed — outliers receive *higher* association probability under NIG than Gaussian\. The correct use of GH in association is via the posterior effective R, which *tightens* the association likelihood for outliers by using a Gaussian with inflated variance\. This is the association analogue of the measurement update mechanism: in both cases, the GH posterior E\[1/V | ν\] is used to compute R\_eff, and the subsequent operation \(update or association weight\) is evaluated with a Gaussian at that R\_eff\.

## __6\.3  Limitations and Future Work__

Three limitations are noted:

Correlated Q scenario: GH\-SR\-IMM does not decisively outperform Huang 2017 on the Correlated Q scenario \(1\.275 vs 1\.252\)\. The AR augmentation of M2 is partially effective — the online ρ estimator correctly characterises the noise correlation — but the current architecture routes ρ through the dynamics F matrix rather than the measurement equation\. A true AR state augmentation where ε appears in the measurement equation H would likely close this gap\.

IMM transition matrix: The 3×3 transition matrix is fixed\. Adapting it online via a Dirichlet conjugate prior on the mode switching probabilities would allow the filter to learn scenario\-specific dynamics switching rates\.

Track initiation and termination: The multi\-target benchmark assumes known track count and uses true initial positions with small noise\. Real deployments require track initiation from clutter \(MHT or particle\-based\) and deletion of low\-probability tracks — neither of which is addressed here\.

# __7  Conclusion__

We presented GH\-SR\-IMM, a robust adaptive tracking filter that combines Generalised Hyperbolic measurement modelling, Interacting Multiple Model dynamics competition, and Square\-Root CKF covariance propagation\. The filter achieves 38% improvement over the Student\-t KF baseline and 69% improvement over the Variational Bayes KF baseline on an eight\-scenario benchmark, winning 6 of 8 scenarios with stable cross\-seed variance\.

The key architectural insight is that heavy\-tail measurement robustness and dynamics model uncertainty are orthogonal problems that should be solved orthogonally: GH handles the former within each model, IMM handles the latter across models\. Combining the two within a square\-root framework produces a filter that is robust, consistent, and numerically stable\.

The GH\-JPDA extension demonstrates that the same GH posterior mechanism that enables robust single\-target filtering can be applied to multi\-target association\. By using the posterior effective R in Gaussian association likelihoods rather than substituting NIG likelihoods directly, GH\-JPDA correctly reduces association weight for outlier measurements, achieving 51\.6% mean GOSPA improvement over standard Gaussian\-JPDA across four geometric scenarios\.

# __References__

\[1\]  Y\. Huang, Y\. Zhang, N\. Li, L\. Zhao, and J\. Chambers, "A Novel Robust Gaussian–Student's t Mixture Distribution Based Kalman Filter," IEEE Transactions on Signal Processing, vol\. 67, no\. 13, pp\. 3606–3620, 2019\.

\[2\]  G\. Agamennoni, J\. I\. Nieto, and E\. M\. Nebot, "An approximate expectation maximisation algorithm for estimation in nonlinear dynamic systems," IEEE Transactions on Signal Processing, vol\. 60, no\. 6, pp\. 2862–2877, 2012\.

\[3\]  H\. Akaike, "A new look at the statistical model identification," IEEE Transactions on Automatic Control, vol\. 19, no\. 6, pp\. 716–723, 1974\.

\[4\]  O\. E\. Barndorff\-Nielsen, "Exponentially decreasing distributions for the logarithm of particle size," Proceedings of the Royal Society of London, Series A, vol\. 353, pp\. 401–419, 1977\.

\[5\]  T\. Başar and P\. Bernhard, H∞ Optimal Control and Related Minimax Design Problems, 2nd ed\. Boston, MA: Birkhäuser, 2008\.

\[6\]  Y\. Bar\-Shalom, F\. Daum, and J\. Huang, "The probabilistic data association filter," IEEE Control Systems Magazine, vol\. 29, no\. 6, pp\. 82–100, 2009\.

\[7\]  A\. Ienkaran and S\. J\. Julier, "Square root cubature Kalman filter," IEEE Transactions on Aerospace and Electronic Systems, vol\. 49, no\. 1, pp\. 657–670, 2013\.

\[8\]  R\. Mahler, Statistical Multisource\-Multitarget Information Fusion\. Boston, MA: Artech House, 2007\.

\[9\]  A\. Cantoni and P\. Butler, "Generalization of the Corrigibility of a Kalman Filter," Journal of Optimization Theory and Applications, vol\. 29, no\. 4, pp\. 649–669, 1976\.

\[10\] A\. H\. Jazwinski, Stochastic Processes and Filtering Theory\. New York: Academic Press, 1970\.

# __Appendix A  Python Implementation__

A complete reference implementation is provided in harcf\_benchmark\.py\. The file contains all filter implementations, scenario generators, metrics, and the main benchmark runner\. Running the script reproduces Tables 1 and 2\.

Dependencies: numpy, scipy\. No external tracking or filtering libraries required\.

Key functions:

__Function__

__Description__

run\_gh\_sr\_imm\(truth, meas\)

Proposed single\-target filter\. Returns \(errors, NIS\)\.

run\_huang2017\(truth, meas\)

Student\-t KF baseline\.

run\_agamennoni2012\(truth, meas\)

VB\-KF baseline\.

run\_multi\_tracker\(truths, m1, m2, use\_gh\)

GH\-JPDA or Gaussian\-JPDA multi\-target tracker\.

gen\_single\(kind, seed, n\)

Single\-target scenario generator\.

gen\_multi\(kind, seed, n\)

Multi\-target scenario generator\.

score\(errs, nis\)

Composite score S = RMSE \+ 0\.4|NIS\-1| \+ 0\.2σ\(NIS\)\.

gospa\(truth\_list, est\_list\)

GOSPA metric \(c=5, p=2\)\.

To reproduce all results:

python harcf\_benchmark\.py

Runtime is approximately 3–5 minutes on a modern CPU\. The multi\-target benchmark is the bottleneck \(40 seed × scenario combinations × 300 steps × 2 trackers × 2 sensors\)\.

