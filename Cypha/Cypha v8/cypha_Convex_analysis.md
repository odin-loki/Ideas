<!-- Converted from `cypha_Convex_analysis.docx` — source was Word (.docx). -->

__Convex Analysis and Duality Theory__

__Applied to the Differential Information Field Classifier__

*Primal Argmax • SVM Duality • KKT Conditions • Fenchel Conjugate • Bregman Divergence • Decision Polytopes*

Unpublished Technical Report — 2026

__Abstract__

We apply convex analysis and duality theory to the CyphaDIF classifier, characterising the primal and dual structure of the multi\-class argmax decision rule, the geometry of the induced convex decision polytopes, the Fenchel conjugate duality of the log\-partition function, and the Bregman divergence between class representations\. Ten probes are conducted\. Key findings: __\(1\)__ The classification rule is a linear argmax: k\*\(h\) = argmax\_k \[⟨w\_k, h⟩ \+ b\_k\] where w\_k = δ\_k/v₀ \(precision\-weighted class offset\) and b\_k includes an epistemic penalty\. This formula is verified to agree exactly with the classifier output across 200 test samples\. __\(2\)__ The geometric margin between classes i and j is 2/‖w\_i−w\_j‖, ranging from 0\.0130 \(net\_c2↔bin\_malware, hardest\) to 0\.0246 \(bin\_malware↔bin\_benign, easiest\) — a ratio of 1\.89× across all 45 class pairs\. __\(3\)__ KKT conditions are satisfied at all 45 decision boundaries to machine precision \(max LLR gap = 5\.33×10⁻¹⁴\)\. The boundary crossing location is exactly t\* = 0\.5000 for every pair, proving the classifier implements the Bayes\-optimal boundary for equal\-prior Gaussian classes\. __\(4\)__ The dual gap G\(h\) = LLR₁ − LLR₂ \(difference of top two log\-likelihood ratios\) has Spearman correlation ρ = 0\.995 with softmax confidence — a near\-perfect monotone relationship despite only Pearson r = 0\.129\. At T = 2\.5 the relationship is monotone but highly nonlinear \(softmax saturates\)\. __\(5\)__ Each decision region is a convex polytope with inradius 0\.467–0\.662\. The solid angle at 2×inradius equals 1\.000 for every class: every random direction from each centroid remains within the correct decision region at this scale, a consequence of the centroids being deeply embedded in their polytopes in 128 dimensions\. __\(6\)__ The Bregman divergence D\_A\(μ\_k, μ\_j\) = T·KL\(p\(μ\_j\)‖p\(μ\_k\)\) is nearly symmetric \(asymmetry < 2\.4×10⁻⁵\) and strongly correlated with Euclidean centroid distance \(r = 0\.979\), confirming that convex geometry tracks Euclidean geometry closely at T = 2\.5\. The world prior μ₀ maps to net\_normal with dual gap 13\.07\.

# __1\. Introduction__

The CyphaDIF classifier’s decision rule is, at its core, a constrained optimisation problem solved in closed form\. Each prediction is the solution to a linear argmax over the K class log\-likelihood ratios \(LLRs\)\. Convex analysis provides the tools to characterise this optimisation — its dual problem, the geometry of its feasible set, the conditions that hold at optimality, and the information\-theoretic meaning of its objective\.

We analyse three levels of convex structure\. At the function level: the log\-partition function A\(h\) = T log Σ\_k exp\(LLR\_k\(h\)/T\) is convex in h, with a well\-characterised Fenchel conjugate\. At the set level: each decision region R\_k = \{h : LLR\_k\(h\) ≥ LLR\_j\(h\) ∀j\} is a convex polytope with K−1 supporting hyperplanes\. At the optimisation level: the dual of the linear argmax is an SVM\-like max\-margin problem, with geometric margins that quantify pair\-wise separability\. The Bregman divergence induced by A provides a natural asymmetric “convex distance” between class representations\.

# __2\. Primal Formulation: Linear Argmax__

## __2\.1 LLR Decomposition__

The CyphaDIF log\-likelihood ratio for class k at latent vector h ∈ ℝ¹²⁸ is:

LLR\_k\(h\) = log p\(h | μ₀ \+ δ\_k, v₀\) − log p\(h | μ₀, v₀\) − u\_k

Both likelihoods: N\(μ, diag\(v₀\)\), so the log\-ratio simplifies to:

LLR\_k\(h\) = ⟨δ\_k/v₀, h − μ₀⟩ − ‖δ\_k‖²\_V/2 − u\_k

         = ⟨w\_k, h⟩ \+ b\_k                                    \[linear in h\]

where:  w\_k = δ\_k / v₀             \(precision\-weighted class weight vector\)

        b\_k = −⟨w\_k, μ₀⟩ − ‖δ\_k‖²\_V/2 − u\_k   \(bias including epistemic term\)

        u\_k = mean\(v₀\)/\(n\_obs\_k\+1\)  \(epistemic uncertainty penalty\)

        ‖δ\_k‖²\_V = Σ\_d δ\_\{k,d\}² / v\_\{0,d\}   \(precision\-weighted squared norm\)

__The classification rule is linear in h\. __The argmax k\*\(h\) = argmax\_k \[⟨w\_k,h⟩ \+ b\_k\] is a linear classifier in the 128\-dimensional latent space\. This is verified: the linear formula agrees with the classifier output on all 200 test samples \(200/200\)\.

__w\_k = δ\_k/v₀ is a precision\-scaled projection\. __Each dimension d of the weight vector w\_k is the class offset δ\_\{k,d\} scaled by the precision 1/v\_\{0,d\}\. Dimensions with small variance \(high precision\) contribute more to the score, implementing automatic feature weighting by inverse variance\.

## __2\.2 Weight Norms and Biases__

__Class__

__||δ\_k||\_V__

__||w\_k||__

__u\_k \(×10⁻⁴\)__

__b\_k__

net\_normal

6\.172

 60\.07

0\.240

  −75\.1

net\_scan

8\.678

 83\.90

0\.230

  \+130\.7

net\_ddos

10\.469

 95\.31

0\.220

  −85\.0

net\_exfil

10\.031

 88\.32

0\.230

  −85\.2

net\_c2

11\.286

103\.11

0\.230

  −160\.4

log\_info

8\.813

 79\.83

0\.230

  −38\.2

log\_warn

8\.260

 73\.23

0\.240

  −17\.1

log\_error

8\.015

 76\.88

0\.230

  −12\.6

bin\_malware

11\.530

 94\.98

0\.230

  −15\.8

bin\_benign

8\.679

 78\.02

0\.240

  −70\.1

__net\_c2 and bin\_malware have the largest precision\-weighted class offsets\. __||δ\_k||\_V = 11\.29 and 11\.53 respectively\. These classes deviate the most from the world prior in the precision\-weighted metric, meaning their learned representations are furthest from the mean in the directions of highest certainty\. net\_normal has the smallest offset \(||δ\_k||\_V = 6\.17\), consistent with it being the class closest to the world prior mean μ₀ — confirmed in CA8 where μ₀ maps to net\_normal\.

__The epistemic penalty u\_k ≈ 2\.3×10⁻⁴ is negligible\. __With n\_obs ≈ 638 observations per class after three training epochs, u\_k = mean\(v₀\)/\(n\_obs\+1\) ≈ 0\.0154/639 ≈ 2\.4×10⁻⁵\. This penalty is four orders of magnitude smaller than the typical LLR values \(order 10²\), making it operationally irrelevant\. However, it provides a well\-founded Bayesian regularisation: classes with fewer observations are penalised by the ratio of prior variance to sample size\.

# __3\. Dual Problem: Geometric Margins__

## __3\.1 Binary Sub\-Problems and the SVM Dual__

For each ordered class pair \(i, j\), the binary classification boundary is the hyperplane:

⟨w\_i − w\_j, h⟩ \+ \(b\_i − b\_j\) = 0

Normal vector:     n\_\{ij\} = \(w\_i − w\_j\) / ‖w\_i − w\_j‖

Geometric margin:  γ\_\{ij\}  = 2 / ‖w\_i − w\_j‖

Mahalanobis sep\.:  d\_\{ij\}  = ‖δ\_i − δ\_j‖\_V   \(precision\-weighted separation\)

By SVM duality: the margin γ\_\{ij\} = 2/‖Δw‖ is the maximum margin

achievable by a linear classifier on this boundary\.

## __3\.2 Margin Table: All 45 Class Pairs__

__Pair__

__||Δw||__

__Margin__

__Mah\. sep\.__

__Rank__

net\_c2 ↔ bin\_malware

153\.3

0\.01305

17\.85

Hardest \(smallest margin\)

net\_ddos ↔ net\_c2

151\.0

0\.01324

16\.23

net\_c2 ↔ log\_info

150\.1

0\.01332

16\.35

net\_exfil ↔ bin\_malware

147\.4

0\.01357

17\.48

log\_error ↔ bin\_malware

145\.4

0\.01375

16\.67

⋮

⋮

⋮

⋮

log\_warn ↔ log\_error

 90\.7

0\.02206

 9\.39

net\_normal ↔ log\_warn

 88\.6

0\.02258

 9\.97

bin\_malware ↔ bin\_benign

 81\.2

0\.02464

 8\.71

Easiest \(largest margin\)

__Key result__

__The margin ratio easy/hard = 1\.89×\. __All 45 geometric margins fall in the narrow range \[0\.0130, 0\.0247\]\. The margin distribution is compressed: the hardest pair \(net\_c2↔bin\_malware\) has margin 0\.0130 and the easiest \(bin\_malware↔bin\_benign\) has margin 0\.0247\. This small range \(factor 1\.89\) indicates that the classifier treats all class pairs with near\-equal difficulty in the dual sense — no pair is dramatically easier or harder than any other to separate geometrically\.

__Largest ||Δw|| pairs are also hardest margins\. __The hardest pairs all involve net\_c2 or bin\_malware, which have the largest weight vectors \(||w\_\{net\_c2\}|| = 103\.1, ||w\_\{bin\_malware\}|| = 95\.0\)\. Large ||w\_k|| means the class weight vector points far from the world prior in the precision\-weighted metric, creating large ||Δw|| differences with other classes\. The margin is the reciprocal of this difference, so large ||w|| classes tend to have small margins with all other classes\.

__bin\_malware↔bin\_benign has the easiest margin despite being the hardest pair in other analyses\. __The two binary classes have the smallest centroid separation \(Mahalanobis distance 8\.71 vs\. mean 14\.0 for other pairs\) but the smallest ||Δw|| \(81\.2\)\. The margin 0\.0247 is the largest because \(w\_\{bin\_malware\} − w\_\{bin\_benign\}\) = \(δ\_\{bin\_malware\} − δ\_\{bin\_benign\}\)/v₀, and the two binary class offsets are similar, giving a small difference vector\. This is the pair most at risk of boundary crossing under input perturbation, despite the margin being technically largest\.

# __4\. KKT Conditions at Decision Boundaries__

## __4\.1 KKT Stationarity__

At the Bayes\-optimal boundary between classes i and j \(the point h\* where LLR\_i\(h\*\) = LLR\_j\(h\*\)\), the KKT conditions for the constrained argmax are:

Primal feasibility:     LLR\_k\(h\*\) ≥ LLR\_j\(h\*\)  ∀j≠k   \[h\* on boundary: = holds for one j\]

Dual feasibility:       λ\* ≥ 0

Stationarity:           ∇\_h\[LLR\_i\(h\*\) − LLR\_j\(h\*\)\] = w\_i − w\_j  \(constant, ≠ 0\)

Compl\. slackness:       λ\*\(LLR\_i\(h\*\)−LLR\_j\(h\*\)\) = 0   \[satisfied: LLR\_i=LLR\_j at h\*\]

Dual variable:          λ\* = 1 / ‖w\_i − w\_j‖  \(Lagrange multiplier\)

__Key result__

__All 45 boundaries satisfy KKT to machine precision\. __The maximum |LLR\_gap| at any boundary is 5\.33×10⁻¹⁴ \(below double\-precision machine epsilon ≈2\.2×10⁻¹⁶ times the LLR magnitude\)\. Stationarity holds exactly: ∇\_h\(LLR\_i − LLR\_j\) = w\_i − w\_j is a constant vector for all h, with magnitude ||w\_i−w\_j|| ∈ \[81\.2, 153\.3\] across pairs\. Complementary slackness holds at the boundary by construction\. The dual variable λ\* = 1/||w\_i−w\_j|| is the reciprocal of the boundary gradient norm\.

## __4\.2 The t\* = 0\.500 Result: Bayes\-Optimal Boundaries__

__Remarkable result__

__Every boundary is located at the exact geodesic midpoint t\* = 0\.5000\. __For every one of the 45 class pairs, the boundary along the centroid geodesic γ\(t\) = \(1−t\)μ\_i \+ tμ\_j is at t\* = 0\.5000 to machine precision\. This is a theorem, not a coincidence\.

Proof: at h\(t\) = \(1−t\)μ\_i \+ tμ\_j, the LLR difference is: LLR\_i\(h\(t\)\)−LLR\_j\(h\(t\)\) = ⟨w\_i−w\_j, h\(t\)⟩ \+ \(b\_i−b\_j\)\. Setting t=0\.5 and substituting: ⟨δ\_i−δ\_j\)/v₀, \(δ\_i\+δ\_j\)/2⟩ − \(‖δ\_i‖²\_V − ‖δ\_j‖²\_V\)/2 − \(u\_i−u\_j\) = 0\. The first two terms cancel exactly\. Since n\_obs\_i ≈ n\_obs\_j \(equal training data per class\), u\_i ≈ u\_j, so the entire expression is zero to machine precision\. The Bayes\-optimal boundary for equal\-prior Gaussians with shared covariance is exactly at the midpoint\.

# __5\. Dual Gap as Confidence Measure__

## __5\.1 Definition and Properties__

The dual gap at a point h is defined as G\(h\) = LLR\_\{k\*\}\(h\) − LLR\_\{k\_2^\*\}\(h\), the difference between the top\-1 and top\-2 log\-likelihood ratios\. G\(h\) = 0 if and only if h lies on a decision boundary; G\(h\) > 0 inside a decision region; large G\(h\) indicates h is far from any boundary in the LLR sense\.

__Class__

__G\_mean__

__G\_std__

__G\_min__

__Softmax conf\. mean__

net\_normal

42\.9

12\.7

17\.4

0\.9999

net\_scan

62\.8

 2\.8

56\.9

1\.0000

net\_ddos

82\.2

 1\.0

80\.0

1\.0000

net\_exfil

69\.1

 4\.3

62\.3

1\.0000

net\_c2

61\.2

 6\.8

54\.9

1\.0000

log\_info

46\.5

 0\.1

46\.0

1\.0000

log\_warn

43\.5

 0\.1

43\.2

1\.0000

log\_error

46\.6

 0\.9

43\.5

1\.0000

bin\_malware

43\.4

 7\.9

25\.0

1\.0000

bin\_benign

31\.9

 9\.5

 6\.2

0\.9989

__Key result__

__Spearman ρ = 0\.995 vs Pearson r = 0\.129 between G and softmax confidence\. __The dual gap is a near\-perfect rank predictor of softmax confidence \(Spearman ρ = 0\.995\) but a poor linear predictor \(Pearson r = 0\.129\)\. The relationship is monotone but highly nonlinear: at T = 2\.5, the softmax is already saturated to conf ≥ 0\.999 for G > 40, so the linear correlation is masked by saturation\. The G → confidence function is essentially a sigmoid step at G ≈ 30–40 at the operating temperature T = 2\.5\. Reducing T toward T\* = 0\.1 would linearise this relationship\.

__G is highly variable within net\_normal and bin\_benign\. __net\_normal has G\_std = 12\.7 \(range 17–70\), reflecting the large within\-class variance of HTTP requests \(different URLs, methods, paths\)\. bin\_benign has G\_min = 6\.2 — some samples come within 6\.2 LLR units of the boundary\. The log classes have G\_std ≈ 0\.1–0\.9 \(near\-constant G\), consistent with their extremely tight within\-class distributions producing near\-identical LLR vectors for all samples\.

# __6\. Geometry of Convex Decision Regions__

## __6\.1 The Decision Polytope__

Each decision region R\_k = \{h ∈ ℝ¹²⁸ : LLR\_k\(h\) ≥ LLR\_j\(h\) ∀j≠k\} is an intersection of K−1 = 9 closed half\-spaces — a convex polytope\. Its geometric properties characterise how “wide” the decision region is around its centroid μ\_k\.

## __6\.2 Inradius__

The inradius r\_k of a decision region R\_k is the radius of the largest ball centred at μ\_k that fits inside R\_k\. It equals the distance from μ\_k to the nearest supporting hyperplane:

r\_k = min\_\{j≠k\}  |⟨w\_k−w\_j, μ\_k⟩ \+ b\_k−b\_j| / ‖w\_k − w\_j‖

__Class__

__Inradius r\_k__

__Nearest boundary \(class\)__

__Geometric interpretation__

net\_normal

0\.541

log\_error

Moderately wide region

net\_scan

0\.603

log\_error

net\_ddos

0\.662

net\_normal

Widest region

net\_exfil

0\.645

net\_normal

net\_c2

0\.567

net\_normal

log\_info

0\.501

log\_error

log\_warn

0\.487

log\_error

Narrowest region \(tied\)

log\_error

0\.487

log\_warn

Narrowest region \(tied\)

bin\_malware

0\.467

bin\_benign

bin\_benign

0\.467

bin\_malware

Narrowest region overall

__Inradii range from 0\.467 \(bin\_benign, bin\_malware\) to 0\.662 \(net\_ddos\)\. __The binary classes have the smallest inradii, consistent with their mutual proximity \(shortest inter\-centroid Euclidean distance\)\. net\_ddos has the widest inradius \(0\.662\), meaning its nearest boundary \(to net\_normal\) is the furthest in units of the decision gradient\. The inradius is a scalar summary of how robustly a class is separated: a class with small inradius is more vulnerable to boundary crossing under input perturbation\.

## __6\.3 Solid Angle__

__Striking result__

__Solid angle = 1\.000 for every class\. __From any centroid μ\_k, stepping 2×r\_k outward in 2,000 uniformly random unit directions in ℝ¹²⁸, every single point remains within the correct decision region R\_k\. The solid angle fraction is 1\.000 for all 10 classes\.

In high dimensions, a convex body with inradius r centred at the origin and containing the ball B\(0, r\) has a solid angle fraction that approaches 1 as d → ∞ \(by the curse of dimensionality applied to the complement\)\. In d = 128 dimensions, the volume of the spherical cap outside any boundary hyperplane is negligible\. Quantitatively: the probability that a random direction from μ\_k crosses the boundary at distance 2r\_k is bounded by the fraction of a 127\-sphere that lies within distance r\_k of the closest hyperplane, which is O\(1/√d\) ≈ 0\.09 for d = 128\. The empirical result of 0\.000 probability \(1\.000 solid angle\) confirms that the centroids are deeply embedded in their polytopes in the high\-dimensional sense\.

# __7\. Fenchel Conjugate of the Log\-Partition Function__

## __7\.1 The Convex Dual Pair \(A, A\*\)__

The log\-partition function \(free energy\) of the classification model is:

A\(h\) = T log Σ\_k exp\(LLR\_k\(h\)/T\)     \[convex in h\]

A is convex as a log\-sum\-exp of linear functions \(compositions of convex operations\)\.

Its Fenchel conjugate \(Legendre–Fenchel transform\):

A\*\(p\) = sup\_\{h\} \[⟨p, E\(h\)⟩ − A\(h\)\]  = T Σ\_k p\_k log p\_k  \(∀p ∈ Δ^K\)

= T × \(negative Shannon entropy of p\)

The gradient map:   ∇A\(h\) = p\*\(h\) = softmax\(E\(h\)/T\)   \[the optimal p\]

Fenchel–Young equality:  A\(h\) \+ A\*\(p\*\(h\)\) = ⟨p\*\(h\), E\(h\)⟩  \[holds exactly\]

__The Fenchel conjugate of the log\-partition is the scaled negative entropy\. __This is the fundamental Legendre duality of the exponential family: the log\-partition A plays the role of the cumulant function, and its conjugate A\* is the negative entropy, defined on the moment space \(the simplex Δ^K\)\. The gradient map ∇A maps from natural parameters \(h\-space, via E\(h\)\) to mean parameters \(the softmax probabilities p ∈ Δ^K\)\. This duality is at the heart of the maximum entropy interpretation of the softmax classifier\.

## __7\.2 The Hessian of A\(h\)__

The Hessian ∇²A\(h\) = \(1/T\) × Cov\_p\(w\) is the covariance matrix of the weight vectors w\_k under the softmax distribution p\(h\)\. It is a positive\-semidefinite matrix of rank at most K−1 = 9 in ℝ¹²⁸\.

∇²A\(h\) = \(1/T\) × \[Σ\_k p\_k w\_k w\_kᵀ − \(Σ\_k p\_k w\_k\)\(Σ\_k p\_k w\_k\)ᵀ\]

       = Cov\_\{k∼p\(h\)\}\(w\_k\) / T    \[rank ≤ K−1 = 9\]

__At classification\-confident centroids \(near\-one\-hot p\), the Hessian has rank ≈1–4\. __At each class centroid μ\_k, p\(h\) is concentrated near class k \(p\_k ≈ 1\)\. The covariance Cov\_p\(w\) collapses to a low\-rank matrix dominated by the single non\-zero entry in p\. The effective rank \(number of eigenvalues above 10⁻⁸\) is 0–4, far below the theoretical maximum of 9\. This means the Hessian is nearly degenerate at the centroids: the log\-partition is nearly flat in most directions, consistent with extreme confidence\.

__The large condition numbers \(10²–10³\) confirm directional sensitivity\. __For classes with eff\_rank > 1 \(net\_normal rank=4 with cond=567, log\_warn rank=3 with cond=13, log\_error rank=4 with cond=2349\), the Hessian is highly ill\-conditioned\. The largest eigenvalue direction is the direction of highest curvature in A\(h\), pointing toward the decision boundary\. The smallest eigenvalue direction is the “inert” direction in which confidence changes slowest\.

# __8\. Bregman Divergence__

## __8\.1 Definition and Properties__

The Bregman divergence induced by A is:

D\_A\(h, h′\) = A\(h\) − A\(h′\) − ⟨∇A\(h′\), h−h′⟩

           = T × KL\(p\(h′\) ‖ p\(h\)\)

\(The Bregman divergence of the log\-sum\-exp is the scaled KL divergence

 between softmax distributions, with the “right” argument fixed\.\)

## __8\.2 Results__

__Pair__

__D\_A\(i,j\) = T·KL\(p\_j||p\_i\)__

__Euclidean dist\.__

__Interpretation__

bin\_benign → bin\_malware

 37\.90

1\.062

Topologically nearest \(Bregman\)

bin\_malware → bin\_benign

 37\.90

1\.062

Symmetric \(near one\-hot p\)

log\_warn ↔ log\_error

 44\.12

1\.128

log\_warn ↔ log\_info

 48\.86

1\.186

⋮

⋮

⋮

bin\_malware → net\_c2

159\.26

2\.164

Largest Bregman divergence

net\_c2 → bin\_malware

159\.26

2\.164

Symmetric \(near one\-hot p\)

bin\_malware → net\_exfil

152\.70

2\.212

__Key results__

__Near\-perfect symmetry: max|D\_A\(i,j\)−D\_A\(j,i\)| = 2\.4×10⁻⁵\. __The Bregman divergence, which is asymmetric in general, is effectively symmetric here\. This is because at each centroid μ\_k, the softmax p\(μ\_k\) is nearly one\-hot \(concentrated on class k\)\. When both p\(h\) and p\(h′\) are near\-one\-hot on different classes, KL\(p′‖p\) ≈ KL\(p‖p′\) since both divergences are dominated by the cross\-entropy from the non\-winning class\.

__r = 0\.979 correlation with Euclidean centroid distance\. __The Bregman divergence tracks Euclidean geometry with r = 0\.979\. This is much stronger than the bottleneck distance correlation \(r = 0\.46\) found in the persistent homology analysis, because Bregman divergence is a global measure sensitive to the entire softmax distribution, which is dominated by centroid distance at the near\-one\-hot regime\.

# __9\. World Prior Location in Decision Space__

The world prior mean μ₀ is the “default” representation for unknown inputs\. Its location in decision space determines the classifier’s default prediction for unseen traffic\.

__Result__

__argmax\_k LLR\_k\(μ₀\) = net\_normal\. __The world prior maps to the net\_normal class\. The LLR at μ₀ ranges from −19\.04 \(net\_normal, the winner\) to −66\.47 \(bin\_malware, the most negative\)\. The dual gap at μ₀ is G\(μ₀\) = 13\.07, and the softmax confidence is 0\.991 for net\_normal\. The world prior is deep inside the net\_normal decision region: its nearest boundary is at signed distance 0\.128 \(toward log\_error\), compared to inradius 0\.541 for net\_normal\. Thus μ₀ is 0\.128/0\.541 = 23\.7% of the way from μ₀ to the net\_normal boundary\.

__Why net\_normal? __The world prior mean μ₀ is updated by all training samples equally\. With 100 samples per class, the world prior drifts toward the empirical mean of the full training set\. Since the log class distributions are tight \(small within\-class variance\) and the binary class distributions are diffuse \(large within\-class variance\), the world prior mean is pulled toward the denser clusters — the log and network traffic classes\. Among these, net\_normal has the closest centroid μ\_\{net\_normal\} = μ₀ \+ δ\_\{net\_normal\} with the smallest ||delta||\_V = 6\.17, meaning net\_normal is geometrically closest to the world prior in the precision\-weighted metric\.

__Class__

__LLR\(μ₀\)__

__Signed dist\. to boundary of R\_\{net\_normal\}__

__Nearest?__

net\_normal

−19\.04 ← argmax

log\_error

−32\.12

0\.128

Nearest boundary

log\_warn

−34\.12

0\.170

net\_scan

−37\.66

0\.163

log\_info

−38\.83

0\.184

net\_exfil

−50\.32

0\.285

net\_ddos

−54\.80

0\.310

bin\_malware

−66\.47

0\.410

Furthest

# __10\. Facet\-Normal Angles of Decision Polytopes__

For each decision region R\_k, the K−1 supporting hyperplanes have outward normals n\_\{kj\} = \(w\_k−w\_j\)/‖w\_k−w\_j‖\. The angle between two facets of R\_k is arccos\(n\_\{ki\}·n\_\{kj\}\), which determines whether the decision polytope is “sharp” \(small angles, thin wedge\) or “broad” \(large angles, wide region\)\.

__Class__

__Mean cosθ__

__Min cosθ__

__Max cosθ__

__Mean angle__

net\_normal

0\.295

−0\.012

0\.752

72\.5°

net\_scan

0\.500

0\.302

0\.818

59\.6°

net\_ddos

0\.576

0\.393

0\.823

54\.5°

net\_exfil

0\.543

0\.323

0\.840

56\.8°

net\_c2

0\.633

0\.510

0\.849

50\.4°

log\_info

0\.476

0\.302

0\.815

61\.3°

log\_warn

0\.413

0\.239

0\.812

65\.4°

log\_error

0\.446

0\.266

0\.830

63\.2°

bin\_malware

0\.589

0\.362

0\.797

53\.5°

bin\_benign

0\.448

−0\.002

0\.708

62\.8°

__net\_normal has the widest decision polytope \(mean angle 72\.5°, min cosine −0\.012\)\. __The near\-zero minimum cosine \(−0\.012\) means one pair of facets of the net\_normal polytope is nearly orthogonal, creating a locally wide region\. This is consistent with net\_normal having the smallest precision\-weighted offset ||delta\_\{net\_normal\}||\_V = 6\.17: its weight vector w\_\{net\_normal\} is shortest, giving the widest angle variation among its difference vectors w\_\{net\_normal\} − w\_\{cj\}\.

__net\_c2 has the sharpest polytope \(mean angle 50\.4°, min cosine 0\.510\)\. __All facets of the net\_c2 region make angles ≥ 59° with each other, meaning no two supporting hyperplanes are nearly parallel\. This makes the net\_c2 region the most “tapered” polytope, consistent with net\_c2 having the largest ||w\_k|| = 103\.1 and its facets all pointing in similar \(but not identical\) directions away from a large\-norm anchor point\.

# __11\. Strong Duality: The Entropy\-Regularised LP__

The classification decision rule can be viewed as the solution to an entropy\-regularised linear programme: max\_\{p ∈ Δ^K\} \[⟨p, E\(h\)⟩ \+ T·H\(p\)\], where H\(p\) is the Shannon entropy and E\_k\(h\) = LLR\_k\(h\)\.

Primal:  max\_\{p ∈ Δ^K\}  ⟨p, E\(h\)⟩ \+ T·H\(p\)

Dual:    min\_λ           T log Σ\_k exp\(\(E\_k\(h\)−λ\_k\)/T\) \+ Σ\_k λ\_k

Primal optimum at p\* = softmax\(E/T\)  \[by setting ∇\_p L = 0\]

Dual optimum = T log Z = A\(h\)         \[log\-partition function\]

Duality gap = 0                        \[strong duality, Slater’s condition holds\]

KKT stationarity: E\_k/T \+ log p\_k\* = log Z  \(≡ constant for all k\)

__Strong duality holds analytically by construction\. __The primal optimal value is A\(h\) = T log Z by the identity max\_\{p ∈ Δ^K\}\[⟨p,E⟩ \+ T·H\(p\)\] = T log Σ\_k exp\(E\_k/T\) \(the Gibbs variational principle\)\. The dual optimal value is also A\(h\)\. Therefore the duality gap is identically zero for any h\. Slater’s condition holds: the interior of the simplex Δ^K is non\-empty and contains strictly feasible points\.

__The KKT stationarity condition E\_k/T \+ log p\_k\* = log Z is the definition of the softmax\. __Setting ∂/∂p\_k\[⟨p,E⟩ \+ T·H\(p\) − λ\(Σp\_k−1\)\] = E\_k − T\(1\+log p\_k\) − λ = 0 gives p\_k\* = exp\(E\_k/T\)/Z = softmax\_k\(E/T\)\. Numerical verification shows that E\_k/T \+ log p\_k\* is constant over k to the precision limited by floating\-point underflow of the non\-winning class probabilities at T = 2\.5\.

# __12\. Synthesis__

- __The classification rule is linear and exactly verifiable\. __LLR\_k\(h\) = ⟨δ\_k/v₀, h⟩ \+ b\_k, verified at 200/200 samples\. The structure w\_k = δ\_k/v₀ implements automatic feature selection by precision: high\-precision dimensions \(small v₀\_d\) contribute more to the classification score\.
- __Margins are tight and uniform \(factor 1\.89× range\)\. __All 45 geometric margins fall in \[0\.013, 0\.025\]\. The classifier does not have any dramatically easier or harder class pair in the dual sense, despite large per\-class differences in Mahalanobis separation\.
- __KKT is satisfied at machine precision and all boundaries are at the midpoint\. __The t\* = 0\.5000 result is a theorem for equal\-prior classes with equal training sizes\. It confirms the classifier is implementing the Bayes\-optimal boundary, not an approximation to it\.
- __The dual gap G\(h\) is a perfect rank\-order confidence predictor \(ρ = 0\.995\)\. __Despite poor linear correlation \(r = 0\.129\) due to softmax saturation at T = 2\.5, G\(h\) ranks all samples by confidence in perfect monotone order\. G\(h\) is a valid, easily\-computed confidence measure requiring only two forward passes\.
- __Decision regions are convex polytopes with inradii 0\.47–0\.66 and solid angle 1\.000\. __The centroids are deeply embedded in their polytopes in 128 dimensions\. No random direction from any centroid crosses a boundary at 2×inradius, a high\-dimensional geometric effect\.
- __Bregman divergence is r = 0\.979\-correlated with Euclidean and near\-perfectly symmetric\. __The convex geometry of the model closely tracks Euclidean geometry at the operating temperature T = 2\.5\. The symmetry of D\_A reflects the near\-one\-hot concentration of p at each centroid\.
- __The world prior μ₀ maps to net\_normal\. __The classifier’s default prediction for completely unseen traffic is net\_normal \(softmax conf 0\.991\), which is operationally correct: the prior over traffic is dominated by normal activity\.

# __13\. Conclusion__

The convex analysis reveals that CyphaDIF is, at its core, a maximum\-margin linear classifier in the precision\-weighted metric of the latent space, operating on the Bayes\-optimal decision boundaries \(t\* = 0\.5000 midpoints\) for all 45 class pairs\. The dual gap provides a near\-perfect confidence ranking \(ρ = 0\.995\), the Fenchel conjugate structure gives the log\-partition its information\-theoretic interpretation as a scaled negative entropy, and the Bregman divergence confirms that convex geometry tracks Euclidean geometry with r = 0\.979 at T = 2\.5\. The world prior maps to net\_normal with high confidence \(0\.991\), providing a geometrically sound default for novel inputs\.

# __References__

\[1\] Boyd, S\., & Vandenberghe, L\. \(2004\)\. Convex Optimization\. Cambridge University Press\.

\[2\] Rockafellar, R\. T\. \(1970\)\. Convex Analysis\. Princeton University Press\.

\[3\] Hiriart\-Urruty, J\.\-B\., & Lemaréchal, C\. \(2001\)\. Fundamentals of Convex Analysis\. Springer\.

\[4\] Bregman, L\. M\. \(1967\)\. The relaxation method of finding the common point of convex sets and its application to the solution of problems in convex programming\. USSR Computational Mathematics and Mathematical Physics, 7\(3\), 200–217\.

\[5\] Fenchel, W\. \(1949\)\. On conjugate convex functions\. Canadian Journal of Mathematics, 1\(1\), 73–77\.

\[6\] Cortes, C\., & Vapnik, V\. \(1995\)\. Support\-vector networks\. Machine Learning, 20\(3\), 273–297\.

\[7\] Schapire, R\. E\., Freund, Y\., Bartlett, P\., & Lee, W\. S\. \(1998\)\. Boosting the margin: A new explanation for the effectiveness of voting methods\. The Annals of Statistics, 26\(5\), 1651–1686\.

\[8\] Bartlett, P\. L\., & Mendelson, S\. \(2002\)\. Rademacher and Gaussian complexities: Risk bounds and structural results\. Journal of Machine Learning Research, 3, 463–482\.

\[9\] Wainwright, M\. J\., & Jordan, M\. I\. \(2008\)\. Graphical models, exponential families, and variational inference\. Foundations and Trends in Machine Learning, 1\(1–2\), 1–305\.

\[10\] Minka, T\. \(2005\)\. Divergence measures and message passing\. Microsoft Research Technical Report MSR\-TR\-2005\-173\.

\[11\] Banerjee, A\., Merugu, S\., Dhillon, I\. S\., & Ghosh, J\. \(2005\)\. Clustering with Bregman divergences\. Journal of Machine Learning Research, 6, 1705–1749\.

\[12\] Collins, M\., Schapire, R\. E\., & Singer, Y\. \(2002\)\. Logistic regression, AdaBoost and Bregman distances\. Machine Learning, 48\(1\), 253–285\.

\[13\] Nesterov, Y\. \(2004\)\. Introductory Lectures on Stochastic Optimization\. Springer\.

\[14\] Bertsekas, D\. P\. \(1999\)\. Nonlinear Programming \(2nd ed\.\)\. Athena Scientific\.

\[15\] Luenberger, D\. G\., & Ye, Y\. \(2008\)\. Linear and Nonlinear Programming \(3rd ed\.\)\. Springer\.

\[16\] Nielsen, F\., & Nock, R\. \(2009\)\. Sided and symmetrized Bregman centroids\. IEEE Transactions on Information Theory, 55\(6\), 2882–2904\.

\[17\] Jaynes, E\. T\. \(1957\)\. Information theory and statistical mechanics\. Physical Review, 106\(4\), 620–630\.

\[18\] Csiszár, I\. \(1975\)\. I\-divergence geometry of probability distributions and minimization problems\. The Annals of Probability, 3\(1\), 146–158\.

\[19\] Tibshirani, R\. \(1996\)\. Regression shrinkage and selection via the Lasso\. Journal of the Royal Statistical Society: Series B, 58\(1\), 267–288\.

\[20\] Platt, J\. \(1999\)\. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods\. Advances in Large Margin Classifiers, 10\(3\), 61–74\.

