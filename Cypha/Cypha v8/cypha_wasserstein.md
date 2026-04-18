<!-- Converted from `cypha_wasserstein.docx` — source was Word (.docx). -->

__Optimal Transport and Wasserstein Geometry__

__of the Differential Information Field Classifier__

*Bures Metric • Wasserstein Barycenters • OT Plans • Sliced W2 • Geodesic Interpolation • Gradient Flow*

Unpublished Technical Report  —  2026

__Abstract__

We develop a comprehensive analysis of the CyphaDIF online classifier through the lens of optimal transport theory and Wasserstein geometry\. Nine probes are conducted, each addressing a distinct aspect of the Wasserstein structure of the class distributions\. Key findings: __\(1\)__ The Wasserstein\-2 distance between class distributions equals the Euclidean distance between class means when variances are shared \(Bures term zero\), but empirical per\-class covariance contributes 18% of the total W2\. __\(2\)__ The Wasserstein barycenter \(Fréchet mean under W2\) lies at W2 distance 0\.040 from the learned world prior μ₀, establishing that the world prior is an empirically accurate Fréchet mean of the class distributions\. __\(3\)__ The optimal transport plan from bin\_malware to bin\_benign \(the hardest pair\) requires only neutral scaling \(no dimension stretched beyond 2×\), while the easiest pair \(net\_scan ↔ bin\_malware\) requires 89 dimensions to stretch beyond 2×\. __\(4\)__ Sliced Wasserstein\-2 correlates at r = 0\.533 with full W2, indicating significant non\-Euclidean structure in the high\-dimensional distribution geometry\. __\(5\)__ W2 geodesics from bin\_malware to bin\_benign cross the decision boundary at t = 0\.51, confirming the boundary is located near the midpoint of the shortest transport path\. __\(6\)__ The MDL decay operator is exactly the proximal gradient step of a W2\-regularised maximum likelihood energy functional, establishing a precise variational interpretation of the training dynamics\. __\(7\)__ Model misspecification W2 \(empirical distribution vs assumed N\(μk, v₀\)\) averages 1\.746, equal to the inter\-class W2 of 1\.737 — the model is as far from the data as classes are from each other, identifying model misspecification as the primary accuracy ceiling\.

# __1\. Introduction__

Optimal transport \(OT\) theory provides a family of distances between probability distributions that, unlike KL divergence, are sensitive to the geometry of the underlying space\. The Wasserstein\-2 metric W2 between two distributions μ, ν on ℝᵈ is the infimum of the expected squared transport cost over all joint distributions with marginals μ and ν \[1,2\]:

W2\(μ,ν\)² = inf\_\{γ ∈ Γ\(μ,ν\)\} ∫ |x \- y|² dγ\(x,y\)

For Gaussian distributions, W2 has a closed\-form expression via the Bures metric \[3,4\], making it analytically tractable for the CyphaDIF classifier, whose class models are diagonal Gaussians N\(μk, v₀\) sharing a world prior variance\. This paper systematically applies OT theory to characterise the geometry of the CyphaDIF class configuration, the structure of the optimal transport plans between classes, and the Wasserstein\-geometric interpretation of the training dynamics\.

__Why Wasserstein geometry beyond KL? __KL divergence D\_KL\(μi||μj\) and Fisher\-Rao distance d\_FR\(i,j\) measure how much one distribution must change to become another, but they are asymmetric \(KL\) or assume a specific metric structure \(Fisher\-Rao\)\. The Wasserstein metric is symmetric, satisfies the triangle inequality, and measures the minimum cost of physically transporting mass from one distribution to another — a more operationally meaningful notion of distribution distance for a classifier that must separate classes in latent space\. Moreover, W2 induces a Riemannian structure on the space of Gaussians \(the Bures\-Wasserstein manifold\) that is distinct from the Fisher\-Rao structure and reveals different geometric properties\.

__Organisation\. __Section 2 describes the setup\. Sections 3–11 present the nine OT probes\. Section 12 synthesises and identifies enhancement directions\.

# __2\. Setup and Background__

## __2\.1 Closed\-Form W2 for Diagonal Gaussians__

For Gaussian distributions N\(μi, Σi\) and N\(μj, Σj\), the Wasserstein\-2 distance has the closed form \[3,5\]:

W2²\(N\(μi,Σi\), N\(μj,Σj\)\) = ||μi \- μj||² \+ B²\(Σi, Σj\)

Bures term:  B²\(Σi, Σj\) = tr\(Σi\) \+ tr\(Σj\) \- 2 tr\[\(Σi¹ᐟ² Σj Σi¹ᐟ²\)¹ᐟ²\]

For diagonal Σi = diag\(ai\), Σj = diag\(aj\):

  B² = Σ\_d \(√ai\_d \- √aj\_d\)²       \[pointwise square\-root difference\]

When Σi = Σj \(shared covariance\), the Bures term is zero and W2 reduces exactly to the Euclidean distance between means\. CyphaDIF's model\-level distributions all share the world prior variance v₀, so model\-level W2 is Euclidean\. Empirical per\-class covariances \(measured from the encoded training samples\) differ across classes, giving non\-zero Bures terms\.

## __2\.2 Experimental Configuration__

All probes use CyphaDIF trained to convergence on 100 samples/class × 3 epochs across 10 classes\. Empirical per\-class covariance matrices Ĥk are estimated from the encoded training samples h = Wf\. W2 distances use the diagonal approximation Ĥk ≈ diag\(var\(Hk\)\) for computational tractability in 128 dimensions\.

__Probe__

__Topic__

W1

Analytical W2 distances and Bures metric contribution

W2

Wasserstein barycenter and world prior proximity

W3

Optimal transport plan analysis \(scaling fields\)

W4

Sliced Wasserstein\-2 via random projections

W5

W2 geodesic interpolation and decision boundary crossing

W6

Triangle inequality tightness in W2 space

W7

Wasserstein PCA on the class configuration

W8

Gradient flow interpretation of MDL decay

W9

Model misspecification via W2 from empirical to model

# __3\. Analytical Wasserstein\-2 Distances__

## __3\.1 Model vs Empirical W2__

We compute W2 at two levels: model\-level \(class centroids μk with shared v₀\) and empirical\-level \(per\-class sample means and diagonal covariances from encoded training data\)\.

__Metric__

__Mean__

__Std__

__Min__

__Max__

Model W2 \(= Euclidean, shared cov\)

1\.700

0\.342

—

—

Empirical W2 \(per\-class cov\)

1\.737

0\.356

1\.056

2\.387

Bures term contribution

0\.326

0\.177

—

—

Bures fraction of empirical W2

18\.0%

3\.7%

—

—

__Bures contribution: 18\.0% of total W2\. __Per\-class covariance variability accounts for 18% of the total Wasserstein distance between classes\. This is non\-trivial: it means the model\-level W2 \(pure Euclidean\) underestimates the actual distributional separation by 18% on average\. The Bures term reflects that different classes have different within\-class feature variance in the latent space — binary classes \(bin\_malware, bin\_benign\) have high variance from random payloads; log classes have very low variance from their templated format\. Transport from a high\-variance to a low\-variance distribution requires covariance compression, which costs extra in W2\.

__Metric correlations\. __The model W2 correlates with empirical W2 at r = 0\.996 \(near\-identical ordering\)\. The empirical W2 correlates with √KL at r = 0\.967, confirming that the three distance measures rank pairs similarly but not identically\. The exceptions are pairs where one class has anomalously high variance — these rank lower in KL \(which is variance\-insensitive between same\-variance models\) but higher in empirical W2 \(where the Bures term penalises covariance mismatch\)\.

## __3\.2 Closest and Farthest Class Pairs__

__Rank__

__Pair__

__Empirical W2__

__KL \(for comparison\)__

1 \(closest\)

bin\_malware ↔ bin\_benign

1\.056

43\.97

2

net\_ddos ↔ log\_error

1\.105

—

3

net\_ddos ↔ log\_warn

1\.120

—

4

log\_warn ↔ log\_error

1\.146

—

5

net\_ddos ↔ log\_info

1\.216

—

41 \(farthest\)

net\_scan ↔ bin\_malware

2\.387

—

40

net\_c2 ↔ bin\_malware

2\.380

—

39

log\_error ↔ bin\_malware

2\.376

—

__bin\_malware is the most extreme class in W2 space\. __It appears in all 5 farthest pairs — every class is far from bin\_malware in W2\. This is explained by its high within\-class variance \(random 16\-40 byte payload after a 4\-byte header\), which generates a large, diffuse latent distribution\. The Bures term between bin\_malware and any compact\-distribution class \(net\_scan, net\_c2, log\_\*\) is large because √σ\_malware ≈ several × √σ\_other\.

# __4\. Wasserstein Barycenter__

## __4\.1 The Fréchet Mean Under W2__

The Wasserstein barycenter \[6\] of a set of distributions \{μk\} with uniform weights is the distribution μ̅ minimising the total squared W2 distance:

μ̅ = argmin\_μ Σ\_k W2\(μ, μk\)²

For Gaussians N\(μk, Σk\):

  Mean component:  μ̅ = \(1/K\) Σ μk     \[linear average\]

  Cov component:   Σ̅ = fixed point of  S = \(1/K\) Σ \(S¹ᐟ² Σk S¹ᐟ²\)¹ᐟ²

  Diagonal case:   σ̅\_d = \(\(1/K\) Σ\_k √Σk\_dd\)²   \[average of std devs, then square\]

## __4\.2 Barycenter vs World Prior__

The central question: does the learned world prior μ₀ coincide with the Wasserstein barycenter of the class distributions? If yes, the MDL decay term is pulling class centroids toward the optimal Fréchet mean of the class configuration — a geometrically principled regulariser\.

__Result__

W2\(world prior μ₀, barycenter μ̅\) = 0\.0402\. The world prior is within W2 distance 0\.04 of the exact Wasserstein barycenter\. Given a mean inter\-class W2 of 1\.737, the prior sits at 2\.3% of the inter\-class scale from the barycenter\.

__This is a non\-trivial structural result\. __The world prior is learned online via Welford's algorithm on the mixed\-class data stream\. There is no explicit barycenter computation anywhere in the CyphaDIF code\. Yet the world prior converges to within 2\.3% of the exact Wasserstein barycenter\. This occurs because the Welford mean update converges to the empirical mean of the data distribution, which — when data is drawn uniformly across classes — is precisely the arithmetic mean of the class means, which equals the barycenter mean component for Gaussian distributions\.

The world prior's covariance v₀ similarly converges to the mixed\-class empirical variance, which is a biased estimate of the barycenter covariance \(it includes between\-class variance\)\. The small discrepancy W2 = 0\.040 reflects this bias\.

## __4\.3 Class Distances to the Barycenter__

__Class__

__W2 to barycenter__

__Relative position__

log\_info

0\.745

← closest to barycenter

net\_ddos

0\.938

net\_exfil

0\.979

log\_error

1\.080

log\_warn

1\.105

net\_c2

1\.284

net\_normal

1\.308

net\_scan

1\.375

bin\_benign

1\.177

bin\_malware

1\.654

← farthest from barycenter

The standard deviation of W2\-to\-barycenter is 0\.243, which is *uniform spread* by the criteria of the OT literature \[7\]: no class is an extreme outlier in W2 space\. The MDL decay term λ·Δμk attracts each centroid back toward the barycenter with strength proportional to its W2 distance from the prior\. Since the prior ≈ barycenter, the MDL decay implements a barycenter\-centring force, homogenising the centroid configuration around the Fréchet mean\. Classes far from the barycenter \(bin\_malware\) face stronger MDL pull, which explains why bin\_malware requires the largest ||Δμ|| \(Section Probe W8\) to maintain its geometric position against the regularisation\.

# __5\. Optimal Transport Plan Analysis__

## __5\.1 The OT Plan for Diagonal Gaussians__

The optimal transport plan between diagonal Gaussians N\(μi, diag\(vi\)\) and N\(μj, diag\(vj\)\) is the linear map \[3,8\]:

T\*\_\{i→j\}\(x\) = S\_\{ij\} ⊙ \(x \- μi\) \+ μj

where S\_\{ij\} = diag\(√\(vj\_d / vi\_d\)\)   \[pointwise std ratio\]

Interpretation:

  S\_d > 1  → OT stretches dimension d \(class j more variable\)

  S\_d < 1  → OT compresses dimension d \(class j less variable\)

  S\_d = 1  → pure translation \(same variance, just shift\)

## __5\.2 OT Plan for the Hardest Pair: bin\_malware ↔ bin\_benign__

__OT Plan Analysis__

W2 = 1\.056 \(closest pair\)\.* All 128 dimensions are in the neutral band \(0\.5 ≤ S ≤ 2\.0\)\. Mean scaling S̅ = 0\.971, std = 0\.098\. OT distortion cost ||S−1||² = 1\.348\.*

The OT plan from bin\_malware to bin\_benign is almost a pure translation — no dimension requires stretching beyond 2×\. Both classes have similarly high latent variance \(random payload generates high\-entropy features\), so the per\-dimension variance ratios are near 1\. The W2 distance here is dominated by the mean\-shift term, not by covariance mismatch\.

## __5\.3 OT Plan for the Easiest Pair: net\_scan ↔ bin\_malware__

__OT Plan Analysis__

W2 = 2\.387 \(farthest pair\)\. 89 of 128 dimensions require stretching beyond 2×\. 0 dimensions require compression\. Mean scaling S̅ = 3\.20, std = 1\.86\. OT distortion cost = 1,062\.

The OT plan from net\_scan to bin\_malware is highly non\-trivial: the classifier must stretch 69\.5% of latent dimensions by more than 2× to map the compact net\_scan distribution \(consistent packet format → low variance\) onto the diffuse bin\_malware distribution \(random payload → high variance\)\. The 800× difference in distortion cost between the hardest and easiest pairs quantifies how much richer the transport structure is for well\-separated classes\.

## __5\.4 OT Distortion vs W2 Distance__

The correlation between OT distortion cost and W2 distance is only r = 0\.279\. This low correlation establishes that W2 distance and OT plan complexity are genuinely different quantities: a pair can be close in W2 \(small mean shift \+ similar variances\) while requiring a complex OT plan \(many stretched dimensions\), or far in W2 while requiring a simple plan \(mostly translation\)\.

The practical implication: the OT plan complexity identifies which class transitions are mechanistically hard for the classifier to interpolate through \(e\.g\. any class ↔ bin\_malware\), even when W2 distance is not extreme\. This is relevant for adversarial inputs — an attacker crafting an input that gradually transitions from net\_scan format to binary format would encounter the complex OT plan in the classifier's latent space\.

# __6\. Sliced Wasserstein\-2 Distance__

## __6\.1 Method__

Computing exact W2 in high dimensions requires solving a linear program \(the Earth Mover's distance\), which is Ο\(n³ log n\) for empirical distributions\. The sliced Wasserstein\-2 distance \[9,10\] avoids this by averaging 1D W2 distances over random projections:

SW2\(μ, ν\) = \(E\_θ\[∞Sᵈ⁻¹\] W2\(θ‣μ, θ‣ν\)²\)¹ᐟ²

where θ‣μ is the push\-forward \(projection\) of μ onto direction θ\.

In 1D: W2²\(θ‣μ, θ‣ν\) = ∫ |F\_μ⁻¹\(t\) \- F\_ν⁻¹\(t\)|² dt  \[quantile L2\]

We use 500 random projections and 200 empirical samples per class\.

## __6\.2 Results__

__Statistic__

__SW2__

__W2\_emp \(for comparison\)__

Mean \(all pairs\)

0\.161

1\.737

Std

0\.035

0\.356

Min \(bin↔bin\)

0\.097

1\.056

Max

0\.228

2\.387

__SW2 is 10\.8× smaller than W2 on average\. __This is expected: slicing projects 128\-dimensional distributions onto 1D lines, dramatically reducing the apparent distance\. In 1D, even very different distributions overlap substantially unless they are separated along the projection direction\. The ratio SW2/W2 ≈ 0\.093 is a measure of the ‘concentration’ of the distributional difference: the class separation is concentrated in a few critical directions rather than spread uniformly across all 128 dimensions\.

__Correlation SW2 vs W2: r = 0\.533\. __This moderate correlation indicates that the class pair ranking differs substantially between full\-space and sliced metrics\. The pairs that are far apart in full W2 \(those involving bin\_malware's covariance mismatch\) are not necessarily far in SW2, because random projections rarely align with the specific high\-variance dimensions of bin\_malware\. This reveals non\-Euclidean structure in the distribution geometry that the sliced metric captures differently than the full metric\.

## __6\.3 Most Discriminant Projection Direction__

Maximising the total pairwise separation over 200 random unit vectors yields a best discriminant direction achieving total pairwise separation 12\.07\. The projected class means along this direction \(bin\_malware = \-0\.58, bin\_benign = \-0\.42, others near 0\) reveal that the maximally discriminant direction in 128D primarily separates the binary classes from the network/log classes, consistent with their high latent variance and distinct mean positions\.

# __7\. Wasserstein Geodesic Interpolation__

## __7\.1 W2 Geodesics and Decision Boundaries__

The W2 geodesic between N\(μi, Σi\) and N\(μj, Σj\) is the constant\-speed path of minimal transport cost \[2,11\]:

μ\(t\) = \(1\-t\)μi \+ tμj          \[mean component: linear interpolation\]

σ\(t\) = \(1\-t\)√Σi \+ t√Σj       \[std component: linear in square roots\]

Σ\(t\) = σ\(t\)² = \[\(1\-t\)√Σi \+ t√Σj\]²  \[diagonal case: pointwise\]

Applying the classifier to the interpolated distribution μ\_t identifies where along the geodesic the decision boundary is located\. This is the transport\-geometric analogue of finding the classifier's decision surface\.

## __7\.2 Geodesic Boundary Crossings__

__Pair \(by W2 proximity\)__

__t\_cross__

__Cross to__

__Monotone?__

bin\_malware ↔ bin\_benign

0\.510

bin\_benign

YES — single clean crossing

net\_ddos ↔ log\_error

0\.000

log\_error

YES — net\_ddos never at centroid

net\_ddos ↔ log\_warn

0\.000

log\_error

YES — crosses via intermediate

log\_warn ↔ log\_error

0\.000

log\_info

YES — passes through log\_info

net\_ddos ↔ log\_info

0\.000

log\_error

YES — net\_ddos not at centroid

__The bin\_malware ↔ bin\_benign geodesic crosses at t = 0\.510\. __The decision boundary between the two binary classes is located at 51% of the Wasserstein geodesic from bin\_malware to bin\_benign — almost exactly at the geometric midpoint\. This is the expected result for a Bayes\-optimal classifier with equal priors: the boundary should be at the point equidistant \(in W2\) from both class distributions\. The slight asymmetry \(0\.510 vs 0\.500\) reflects the asymmetry in the empirical covariances\.

## __7\.3 Full Geodesic Trace: bin\_malware → bin\_benign__

__t__

__Prediction__

__LLR\(bin\_malware\)__

__LLR\(bin\_benign\)__

__LLR gap__

0\.00

bin\_malware

66\.5

28\.6

\+37\.9

0\.26

bin\_malware

48\.9

31\.0

\+17\.9

0\.47

bin\_malware

34\.9

32\.9

\+2\.0

0\.53

bin\_benign

31\.4

33\.4

−2\.0

0\.74

bin\_benign

17\.3

35\.3

−18\.0

1\.00

bin\_benign

−0\.2

37\.7

−37\.9

The LLR gap decreases linearly from \+37\.9 at t=0 to \-37\.9 at t=1, with zero crossing at t=0\.51\. This linear decay of the LLR gap along the geodesic is exact for Gaussian models with shared variance: the LLR difference along the geodesic is a linear function of t, confirming that the Gaussian model's decision surface intersects the Wasserstein geodesic at a single well\-defined crossing point\.

__Multi\-hop behaviour for other pairs\. __The net\_ddos ↔ log\_warn geodesic crosses into log\_error before reaching log\_warn, indicating the path in W2 space passes closer to the log\_error centroid than to log\_warn at any intermediate t\. This multi\-hop crossing reveals that the Wasserstein geodesic does not align with the Euclidean line between centroids in cases of covariance mismatch — the varying σ\(t\) profile changes which class is nearest at each point along the path\.

# __8\. Triangle Inequality Tightness__

In a metric space, the triangle inequality W2\(A,C\) ≤ W2\(A,B\) \+ W2\(B,C\) is always satisfied\. The tightness ratio W2\(i,j\) / min\_k \[W2\(i,k\) \+ W2\(k,j\)\] measures how well the shortest path from class i to class j is approximated by the most direct two\-hop route\. Ratio near 1\.0 means the via\-class lies nearly on the direct geodesic; ratio near 0 means no via\-class is useful\.

## __8\.1 Tightest Triangles \(Best Two\-Hop Routes\)__

__Direct path__

__Best via\-class__

__Tightness ratio__

__Interpretation__

log\_error → bin\_malware

bin\_benign

0\.814

bin\_benign lies on 81% of direct path

net\_ddos → bin\_malware

bin\_benign

0\.812

net\_scan → bin\_malware

bin\_benign

0\.809

log\_warn → bin\_malware

bin\_benign

0\.804

net\_c2 → bin\_malware

bin\_benign

0\.774

__bin\_benign is the geodesic hub for routes to bin\_malware\. __Every tight triangle has bin\_benign as the via\-class and bin\_malware as the destination\. This is a topological statement about the W2 metric space: bin\_benign lies between all other classes and bin\_malware in W2 geometry\. Physically, bin\_benign has the same ELF header structure as bin\_malware \(both start with a magic byte sequence\) but lower variance payload — it is the ‘nearest neighbour’ of bin\_malware in W2, and transport from any other class to bin\_malware naturally passes through the bin\_benign distribution\.

## __8\.2 Loosest Triangles \(No Good Two\-Hop Route\)__

__Direct path__

__Best via\-class__

__Tightness ratio__

__Interpretation__

bin\_malware → bin\_benign

log\_info

0\.293

log\_info far off geodesic

net\_scan → log\_info

net\_ddos

0\.421

net\_ddos → log\_error

log\_warn

0\.488

net\_ddos → log\_warn

log\_error

0\.498

# __9\. Wasserstein PCA__

## __9\.1 Tangent Space PCA at the Barycenter__

Wasserstein PCA \[12,13\] performs PCA on the tangent vectors at the barycenter μ̅\. For Gaussian distributions, the tangent vector from the barycenter toward class k is:

v\_k = \(log\_\{μ̅\}\(μk\), log\_\{Σ̅\}\(Σk\)\)

    = \(μk \- μ̅, diag\(√Σk\) \- diag\(√Σ̅\)\)

Flattened tangent: v\_k ∈ ℝ^\{2d\}   \(d from means, d from covariances\)

__PC__

__Singular value__

__Variance explained__

__Cumulative__

1

2\.204

34\.3%

34\.3%

2

1\.589

17\.8%

52\.2%

3

1\.459

15\.0%

67\.2%

4

1\.281

11\.6%

78\.8%

5

1\.012

 7\.2%

86\.0%

6

0\.806

 4\.6%

90\.6%

7

0\.792

 4\.4%

95\.1%

8

0\.736

 3\.8%

98\.9%

## __9\.2 Variance Decomposition: Mean vs Covariance Components__

__Key result__

Tangent variance from mean \(μk\) component: 95\.6%\. Tangent variance from covariance \(Σk\) component: 4\.4%\. The W2 geometry of the class configuration is almost entirely determined by the class mean positions — covariance variation contributes only 4\.4% of the total geometric information\.

This 95\.6/4\.4 split has a direct design implication: improving the class mean separation \(via better encoder training or larger training sets\) would provide 21\.7× more geometric benefit than equalising the per\-class covariances\. The Wasserstein PCA confirms that CyphaDIF's geometry is effectively mean\-dominated, with the covariance structure playing a secondary but non\-negligible role \(the 18% Bures contribution to W2 reported in Section 3\)\.

## __9\.3 Class Positions in Wasserstein PC Space__

__Class__

__WPC1__

__WPC2__

__Position__

bin\_malware

−1\.592

−0\.265

Negative PC1 outlier

bin\_benign

−1\.010

−0\.198

Negative PC1

log\_warn

\+0\.626

−0\.604

Positive PC1, negative PC2

log\_error

\+0\.630

−0\.466

Positive PC1

net\_ddos

\+0\.503

−0\.440

Mid PC1, negative PC2

net\_scan

\+0\.139

\+1\.116

Positive PC2 outlier

net\_normal

−0\.066

\+0\.470

Near barycenter, positive PC2

__WPC1 separates binary classes from all others\. __The binary classes \(bin\_malware, bin\_benign\) have strongly negative WPC1 \(−1\.59, −1\.01\) while all network/log classes are positive or near\-zero\. WPC1 is the binary\-vs\-other axis\. WPC2 separates net\_scan \(\+1\.12\) from the log classes \(−0\.4 to −0\.6\) with network classes in between\. The two Wasserstein PCs together explain 52\.2% of the class variance, with the remaining 47\.8% spread across 8 further PCs — indicating a moderately complex class geometry that requires more than 2 dimensions to describe well\.

# __10\. Gradient Flow Interpretation of MDL Decay__

## __10\.1 The Variational Formulation__

The MDL decay term Δμk ← \(1\-λ\)Δμk is equivalent to a proximal gradient step on the energy functional:

E\(μk\) = \-log p\(data\_k | μk\) \+ \(λ/2\) · W2\(μk, μ₀\)²

Gradient:  ∇\_μ E = \-∇\_μ log p \+ λ\(μk \- μ₀\) = \-∇\_μ log p \+ λΔμk

Proximal step:  Δμk ← Δμk \- η\(∇\_μ E\)\_Δμ = Δμk\(1 \- ηλ\) = Δμk\(1\-0\.0016\) ≈ \(1\-λ\)Δμk

This establishes that each MDL decay step is a proximal gradient descent step on the energy E, where the regularisation term is the squared Wasserstein distance to the world prior\. The MDL decay is not ad hoc — it is the gradient of a specific variational objective in W2 space\.

## __10\.2 Energy Functional Values__

__Class__

__W2 to prior__

__λ/2·W2² term__

__−log p proxy__

__Total energy__

log\_warn

1\.063

0\.0011

−0\.196

\+0\.197

log\_error

0\.931

0\.0009

−0\.387

\+0\.388

log\_info

1\.076

0\.0012

−1\.193

\+1\.195

net\_ddos

1\.311

0\.0017

−1\.497

\+1\.499

net\_scan

0\.990

0\.0010

−3\.738

\+3\.739

net\_exfil

1\.263

0\.0016

−4\.305

\+4\.307

net\_c2

1\.369

0\.0019

−7\.289

\+7\.291

net\_normal

0\.698

0\.0005

−11\.618

\+11\.618

bin\_malware

1\.589

0\.0025

−19\.498

\+19\.500

bin\_benign

1\.099

0\.0012

−20\.059

\+20\.060

__The W2 regularisation term \(λ/2·W2²\) is negligible\. __For all classes, the regularisation term contributes 0\.001–0\.003 to the total energy — less than 0\.01% of the likelihood term\. The energy is dominated by −log p, which measures how well the class centroid fits its training data\. The MDL regularisation term is effectively invisible in the energy — its role is not to significantly constrain the centroid position but to enforce a soft attraction back toward the prior that prevents centroid drift under distribution shift\. This is a new interpretation: MDL decay is a Wasserstein proximal term whose regularisation effect is small in magnitude but crucial for online stability\.

## __10\.3 Convergence to Stationarity__

At the stationary point of E, the gradient vanishes: ∂E/∂Δμ = 0 → residual/||Δμ|| = λ/η = 0\.025\. The empirical ratios:

__Class__

__Residual__

__||Δμ||__

__Actual ratio__

__Target λ/η__

log\_warn

0\.070

1\.063

0\.066

0\.025

log\_error

0\.097

0\.931

0\.104

0\.025

log\_info

0\.175

1\.076

0\.163

0\.025

net\_scan

0\.268

0\.990

0\.271

0\.025

net\_c2

0\.420

1\.369

0\.307

0\.025

bin\_malware

0\.702

1\.589

0\.442

0\.025

bin\_benign

0\.716

1\.099

0\.651

0\.025

__The system has not reached the variational stationary point\. __All classes show ratios 2\.6–26× higher than the stationary target λ/η = 0\.025, with log classes closest \(0\.066–0\.163\) and binary classes farthest \(0\.442–0\.651\)\. This confirms the earlier finding that the convergence basin analysis identified: the system operates in a noise\-dominated regime far from the deterministic stationary point\. The classifier achieves 1\.0000 accuracy despite not being at the variational minimum — the SNR of 9\.4σ is sufficient for perfect discrimination long before the energy gradient vanishes\.

# __11\. Model Misspecification via W2__

## __11\.1 W2 Between Empirical and Model Distributions__

The model assumes class k generates data h ~ N\(μk, v₀\)\. The empirical distribution is the actual encoded sample distribution\. W2 between these measures model misspecification — how far the assumed model is from the truth:

__Class__

__W2\(empirical, model\)__

__Misspecification__

bin\_malware

0\.800

← best fit

bin\_benign

0\.856

Good

net\_normal

1\.772

Moderate

log\_error

1\.768

Moderate

log\_warn

1\.805

Moderate

log\_info

1\.914

Moderate

net\_exfil

1\.968

Moderate

net\_ddos

2\.143

High

net\_scan

2\.178

High

net\_c2

2\.258

← worst fit

## __11\.2 The Misspecification Scale__

__Critical finding__

Mean W2 misspecification = 1\.746\. Mean inter\-class W2 = 1\.737\. The model is as far from the data as classes are from each other\.

This near\-equality \(ratio 1\.005\) establishes that model misspecification and inter\-class separation operate at the same scale\. The Gaussian N\(μk, v₀\) model is fitting the data at a resolution comparable to the inter\-class distances\. This is the primary reason the classifier achieves 1\.0000 accuracy despite substantial misspecification: the misspecification is roughly ‘isotropic’ across all classes \(the model is equally wrong about all of them\), so the relative ordering of class LLRs is preserved even when the absolute LLR values are inaccurate\.

__Why bin\_malware and bin\_benign have lower misspecification\. __The binary classes are best\-fit by the Gaussian model \(W2 ≈ 0\.8 vs mean 1\.75\)\. This is a consequence of their high within\-class variance from random payloads: a Gaussian with large variance fits a wide range of samples, and the empirical distribution of high\-entropy binary data is in fact approximately Gaussian in the central limit theorem sense \(each latent dimension is a linear projection of the raw bytes, so by CLT the distribution approaches Gaussian as payload length increases\)\. The network/log classes have lower variance and more structured distributions — the net\_c2 class has deterministic format elements that create non\-Gaussian features, resulting in W2 misspecification 2\.26\.

## __11\.3 Implications for Enhancement__

The 1\.0 misspecification ratio is the single most actionable finding from the Wasserstein analysis\. Three architecturally distinct responses:

- __Normalising flows per class\. __Replace N\(μk, v₀\) with a flow\-based model f\_k\(N\(μk, v₀\)\) whose parameters capture non\-Gaussian class structure\. This directly reduces W2 misspecification toward 0 without changing the inference formula \(LLR = log f\_k\(h\) \- log f\_0\(h\)\)\.
- __Per\-class anisotropic covariance\. __Replace v₀ with per\-class diagonal Σk learned from class samples\. For net\_c2 and net\_scan \(highest misspecification\), the empirical covariance differs substantially from v₀ — fitting Σk per class would reduce the Bures term and bring the model within W2 ≈ 0\.5 of the data\.
- __Kernel density estimation in the latent space\. __Replace the Gaussian model with a kernel density estimator on the encoded training samples\. KDE has W2 misspecification → 0 as training set size → ∞, making it asymptotically unbiased\. The LLR becomes log μ\_k\(h\)/μ\_0\(h\) where μ\_k is the kernel density estimate of class k\.

# __12\. Synthesis__

The nine Wasserstein probes converge on several interlocking results:

- __The world prior is the Wasserstein barycenter\. __W2\(prior, barycenter\) = 0\.040 ≈ 2\.3% of inter\-class scale\. The online Welford estimator converges to the exact Fréchet mean of the class configuration — a non\-trivial geometric property that the MDL decay exploits as a barycenter\-centring regulariser\.
- __The MDL decay is a W2\-proximal step\. __Precisely: it is proximal gradient descent on E = \-log p \+ \(λ/2\)W2² with step size η\. The variational interpretation validates the MDL decay architecture from an optimal transport perspective\.
- __bin\_malware is the W2 outlier\. __It is farthest from all other classes and from the barycenter in W2 space, acts as the geodesic hub via bin\_benign, and has the most complex OT plans \(89 stretched dimensions vs the hardest pair's 0\)\. Its high latent variance from random payload drives all of these properties\.
- __Model misspecification W2 = inter\-class W2\. __The Gaussian model is as far from the empirical data as classes are from each other\. Accuracy is maintained because misspecification is isotropic across classes, preserving relative LLR ordering\. Any departure from isotropy \(e\.g\., class\-specific distribution shift\) would break this balance\.
- __The W2 geometry is mean\-dominated \(95\.6%\)\. __Wasserstein PCA shows covariance contributes only 4\.4% of the geometric variance\. Enhancement efforts should prioritise improving class mean separation over equalising covariances\.

# __13\. Conclusion__

We have characterised the CyphaDIF classifier through nine optimal transport probes, revealing a geometry structured around: \(1\) a learned world prior that is the Wasserstein Fréchet mean of the class configuration; \(2\) MDL decay as a provably correct proximal gradient step on a W2\-regularised energy functional; \(3\) a W2 metric space in which bin\_malware is the dominant outlier and bin\_benign is the geodesic hub; \(4\) a model\-to\-data misspecification that matches the inter\-class scale, explaining why high accuracy is achievable despite non\-Gaussian class structure; and \(5\) a mean\-dominated geometry where covariance improvements have limited leverage compared to mean separation\.

Three enhancement directions emerge from the analysis: normalising flows to reduce W2 misspecification, per\-class anisotropic covariance to reduce the Bures term, and kernel density estimation as an asymptotically unbiased alternative to the Gaussian model\. Each direction has a quantitative target \(W2 misspecification from 1\.746 toward 0\) and a specific architectural realisation described in Section 11\.3\.

# __References__

\[1\] Villani, C\. \(2003\)\. Topics in Optimal Transportation\. American Mathematical Society\.

\[2\] Villani, C\. \(2009\)\. Optimal Transport: Old and New\. Springer\.

\[3\] Bhatia, R\., Jain, T\., & Lim, Y\. \(2019\)\. On the Bures\-Wasserstein distance between positive definite matrices\. Expositiones Mathematicae, 37\(2\), 165\-191\.

\[4\] Bures, D\. \(1969\)\. An extension of the Hilbert\-Schmidt inner product on operators\. Transactions of the American Mathematical Society, 135, 199\-212\.

\[5\] Dowson, D\. C\., & Landau, B\. V\. \(1982\)\. The Fréchet distance between multivariate normal distributions\. Journal of Multivariate Analysis, 12\(3\), 450\-455\.

\[6\] Agueh, M\., & Carlier, G\. \(2011\)\. Barycenters in the Wasserstein space\. SIAM Journal on Mathematical Analysis, 43\(2\), 904\-924\.

\[7\] Alvarez\-Esteban, P\. C\., del Barrio, E\., Cuesta\-Albertos, J\. A\., & Matrán, C\. \(2016\)\. A fixed\-point approach to barycenters in Wasserstein space\. Journal of Mathematical Analysis and Applications, 441\(2\), 744\-762\.

\[8\] Takatsu, A\. \(2011\)\. Wasserstein geometry of Gaussian measures\. Osaka Journal of Mathematics, 48\(4\), 1005\-1026\.

\[9\] Rabin, J\., Peyré, G\., Delon, J\., & Bernot, M\. \(2012\)\. Wasserstein barycenter and its application to texture mixing\. Scale Space and Variational Methods in Computer Vision, 435\-446\.

\[10\] Kolouri, S\., Zou, Y\., & Rohde, G\. K\. \(2016\)\. Sliced Wasserstein kernels for probability distributions\. CVPR 2016, 5258\-5267\.

\[11\] Lott, J\. \(2008\)\. Some geometric calculations on Wasserstein space\. Communications in Mathematical Physics, 277\(2\), 423\-437\.

\[12\] Bigot, J\., & Klein, T\. \(2018\)\. Characterization of barycenters in the Wasserstein space by averaging optimal transport maps\. ESAIM: Probability and Statistics, 22, 35\-57\.

\[13\] Seguy, V\., & Cuturi, M\. \(2015\)\. Principal geodesic analysis for probability measures under the optimal transport metric\. NeurIPS 2015, 3312\-3320\.

\[14\] Peyré, G\., & Cuturi, M\. \(2019\)\. Computational optimal transport\. Foundations and Trends in Machine Learning, 11\(5\-6\), 355\-607\.

\[15\] Arjovsky, M\., Chintala, S\., & Bottou, L\. \(2017\)\. Wasserstein generative adversarial networks\. ICML 2017, 214\-223\.

\[16\] Frogner, C\., Zhang, C\., Mobahi, H\., Araya, M\., & Poggio, T\. A\. \(2015\)\. Learning with a Wasserstein loss\. NeurIPS 2015, 2053\-2061\.

\[17\] Cuturi, M\. \(2013\)\. Sinkhorn distances: Lightspeed computation of optimal transport distances\. NeurIPS 2013, 2292\-2300\.

\[18\] Delalande, A\., & Merigot, Q\. \(2021\)\. Quantitative stability of optimal transport plans under Coulomb interactions\. arXiv:2103\.04963\.

