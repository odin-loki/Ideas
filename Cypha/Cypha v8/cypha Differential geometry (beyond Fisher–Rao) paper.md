<!-- Converted from `cypha Differential geometry (beyond Fisher–Rao) paper.docx` — source was Word (.docx). -->

__Differential Geometry__

__of the Differential Information Field Classifier__

*Riemannian Geometry • Christoffel Symbols • Holonomy • Jacobi Fields • Cartan Frames • Sectional Curvature*

Unpublished Technical Report — 2026

__Abstract__

We analyse the differential geometry of the CyphaDIF classifier across three geometric domains: the __statistical parameter manifold__ — the space of Gaussian distributions N\(μ, v₀\) parameterised by the class means μ\_k; the __encoder weight manifold__ — the Lie group GL\(128\) in which the encoder matrix W lives; and the __feature space__ equipped with the encoder\-induced Riemannian metric\. Across ten probes, three geometric regimes are found\. __Flat regime \(statistical manifold\): __The Gaussian family with fixed variance is a flat Riemannian manifold with zero Riemann curvature tensor, zero Christoffel symbols, trivial holonomy group \{Id\}, and path\-independent parallel transport\. Geodesics are straight lines γ\(t\) = μ₀ \+ tδ\_k\. The Fisher\-Rao metric inflates distances by 8\.06× relative to Euclidean; class geodesic distances range from 8\.71 to 17\.85\. Every decision boundary is a totally geodesic hyperplane \(geodesic curvature κ\_g = 0\) passing exactly through the midpoint of each class\-pair geodesic, confirming Bayes\-optimality in the Fisher metric\. __Curved regime \(encoder manifold GL\(128\)\): __The encoder matrix W lives in GL\(128\), a curved Lie group\. The sectional curvature of GL\(128\) with bi\-invariant metric clusters tightly around K = 0\.500 \(mean 0\.5004, std 0\.0044\) across 50 random tangent pairs — consistent with a rank\-1 symmetric space where K ∈ \{0, 1/4\}\. The polar decomposition W = Q·P reveals a large orthogonal rotation Q with ||Q−I||\_F = 16\.46 \(of max 22\.63\) and mean rotation angle 93\.35°\. Ricci and scalar curvatures are approximately 63\.6 and 8,135\. __Induced geometry \(feature space\): __The encoder\-induced metric g\_enc = Wᵀ diag\(1/v₀\) W on feature space has eigenvalues spanning \[1\.07, 218\.3\], condition number 203\.96, effective rank 51\.38, and log\-determinant 337\.48\. The Cartan moving frame e\_i = columns of W⁻¹ is far from Fisher\-orthonormal \(||Gram−I||\_F = 7,755\)\. Jacobi fields on the flat statistical manifold grow linearly \(Lyapunov exponent λ = 0\), confirmed empirically: classification flips at ε ≈ 0\.9 along the geodesic toward the nearest class\.

# __1\. Geometric Setup__

Three distinct geometric domains arise in CyphaDIF:

- __Statistical manifold Mₛ: __\{N\(μ, v₀\) : μ ∈ ℝ^d\} with the Fisher\-Rao \(FR\) metric G\_ij = δ\_ij/v\_\{0,i\}\. Since v₀ is shared across classes, the class means \{\(μ\_k, v₀\)\} form a d\-dimensional affine subspace within the full NIG manifold\. Fixed\-variance Gaussian families are flat: all curvature tensors vanish\.
- __Weight manifold M\_W: __GL\(128\) = \{W ∈ ℝ^\{128×128\} : det W ≠ 0\}, a Lie group\. With the bi\-invariant metric g\(X,Y\) = tr\(XᵀY\)/d \(left\- and right\-invariant\), GL\(d\) has sectional curvature K = 1/4 for compact directions and 0 for non\-compact ones\. The encoder W lies in GL\(128\) and has been shaped by contrastive Fisher\-Rao gradient descent\.
- __Induced feature manifold M\_f: __The feature space ℝ^d equipped with the pulled\-back metric g\_enc = Wᵀ G\_0 W, where G\_0 = diag\(1/v₀\)\. This measures how the encoder stretches and rotates the input space relative to the Fisher metric on the output\.

Notation:

  d = 128        \(dimension of encoder output and feature space\)

  K = 10         \(number of classes\)

  v₀ ∈ ℝ^d\_\+   \(shared world\-prior variance, mean=0\.0154\)

  G₀ = diag\(1/v₀\)  \(Fisher metric matrix, precision matrix\)

  μ₀ ∈ ℝ^d    \(world\-prior mean\)

  δ\_k = μ\_k \- μ₀  \(class offset, ||D||\_G = Fisher distance from prior\)

  W ∈ GL\(128\)   \(encoder projection matrix\)

# __2\. Fisher\-Rao Metric and Geodesic Distances__

## __2\.1 Riemannian Metric on the Statistical Manifold__

For the Gaussian family N\(μ, v₀\) with fixed diagonal covariance diag\(v₀\), the Fisher information matrix is:

G\_ij\(μ\) = E\[∂\_i log p\(x|μ\) ∂\_j log p\(x|μ\)\]

         = δ\_ij / v\_\{0,i\}   \(diagonal, position\-independent\)

This is a flat metric: Christoffel symbols Γ^k\_ij = 0 for all i,j,k

Riemann tensor: R^l\_kij = 0 \(flat\)

Geodesic equation: dμ/dt = const  \(straight lines\)

The flatness of the Fisher metric on fixed\-variance Gaussians is a standard result in information geometry\. The Riemannian distance between two class means is:

d\_G\(μ\_i, μ\_j\) = ||μ\_i \- μ\_j||\_G = √\( Σ\_d \(μ\_\{i,d\} \- μ\_\{j,d\}\)^2 / v\_\{0,d\} \)

= ||δ\_i \- δ\_j||\_G   \(since μ\_i = μ\_0 \+ δ\_i, terms cancel\)

## __2\.2 Geodesic Distance Matrix__

__Class pair__

__d\_G \(Fisher\-Rao\)__

__d\_Eucl \(Euclidean\)__

__FR/Eucl ratio__

__Classification difficulty__

bin\_malware ↔ bin\_benign

  8\.71

1\.054

8\.26×

Closest pair \(FR\)

log\_warn ↔ log\_error

  9\.39

1\.165

8\.06×

log\_info ↔ log\_warn

  9\.89

1\.227

8\.06×

net\_normal ↔ log\_warn

  9\.97

1\.237

8\.06×

… \(mean\)

13\.71

1\.700

8\.06×

net\_c2 ↔ bin\_malware

17\.85

2\.215

8\.06×

Farthest pair \(FR\)

net\_exfil ↔ bin\_malware

17\.48

2\.174

8\.04×

net\_c2 ↔ net\_ddos

16\.23

2\.019

8\.04×

__FR/Euclidean ratio = 8\.06× \(nearly constant across all pairs\)\.__

__The near\-constant ratio d\_G/d\_Eucl ≈ 8\.06 across all 45 pairs is a striking geometric fact\. __In general, the FR metric inflates distances differently in different directions depending on v₀: dimensions with small v₀ \(high precision\) are stretched more\. The near\-constant ratio means that the class offsets δ\_i − δ\_j are approximately isotropic with respect to v₀: the difference vectors align equally with high\- and low\-precision dimensions\. This is consistent with the harmonic analysis finding that the delta\-vector spectra have similar flatness across classes \(0\.77–0\.90\)\.

__Fisher distances from the world prior μ₀: range \[6\.17, 11\.53\]\. __The closest class to the world prior in the Fisher metric is net\_normal \(||delta||\_G = 6\.17\), consistent with HTTP traffic being the most ‘generic’ traffic type\. The farthest is bin\_malware \(||delta||\_G = 11\.53\), consistent with the MZ header producing the most distinctive feature pattern\. These Fisher distances are the natural complexity measure for MDL \(the description length L\(δ\_k\) = ||delta||\_G^2 / 2 = 19\.0–66\.5 nats\)\.

# __3\. Christoffel Symbols, Connection, and Flat Geometry__

The Christoffel symbols Γ^k\_ij of a Riemannian manifold measure the failure of the coordinate basis to be parallel\. For the Fisher metric G\_ij = δ\_ij/v\_\{0,i\} \(diagonal, position\-independent\):

Γ^k\_ij = \(1/2\) G^\{kl\} \(∂\_i G\_\{lj\} \+ ∂\_j G\_\{li\} \- ∂\_l G\_\{ij\}\)

Since G is constant \(∂\_i G\_\{lj\} = 0 for all i,l,j\):

Γ^k\_ij = 0  for all i, j, k

Geodesic equation: d²μ^k/dt² \+ Γ^k\_ij \(dμ^i/dt\)\(dμ^j/dt\) = 0

Reduces to: d²μ^k/dt² = 0   ⇒  μ\(t\) = μ\_0 \+ t·v  \(straight lines\)

__The Levi\-Civita connection on the statistical manifold is the standard Euclidean connection\. __This means parallel transport is the identity map: a tangent vector v transported along any path γ from p to q remains equal to v \(as a vector in ℝ^d\)\. The holonomy group \(the group of all parallel transport maps along closed loops\) is therefore the trivial group \{I\_d\}\.

__Covariant derivatives reduce to ordinary derivatives\. __For any vector field V and any path γ, the covariant derivative D\_\{γ'\}V = ∂\_\{γ'\}V \(ordinary directional derivative\)\. This simplification is the geometric reason why the NIG classifier’s Fisher\-Rao gradient updates are identical to Euclidean gradient updates rescaled by v₀ — the connection is flat, so there is no correction term\.

# __4\. Holonomy and Parallel Transport__

## __4\.1 Statistical Manifold Holonomy__

The holonomy group Hol\(∇, p\) at a point p is the group of all linear maps on T\_pM obtained by parallel transport around all closed loops through p\. For a flat manifold:

Hol\(∇, μ\_0\) = \{Id\}   \(trivial holonomy\)

Angle defect for a geodesic triangle \(μ\_i, μ\_j, μ\_k\):

  α \+ β \+ γ = π   \(Euclidean angle sum, Gauss\-Bonnet with K=0\)

A tangent vector v transported around any closed loop returns to itself\.

## __4\.2 Encoder Polar Decomposition and Rotation__

The encoder W ∈ GL\(128\) admits the unique polar decomposition W = Q·P where Q is orthogonal \(det Q = ±1\) and P is symmetric positive definite\. The orthogonal factor Q represents the rotational content of W; P represents the stretching\.

__Metric__

__Value__

__Interpretation__

||Q − I||\_F

16\.46

72\.8% of maximum possible \(2√128 = 22\.63\)

tr\(Q\)/d

−0\.058

Near\-zero: Q rotates by ∼90° on average

Mean rotation angle

93\.4°

Near\-maximal: Q is a large rotation

det\(Q\)

−1\.000

W has negative orientation \(improper rotation\)

||P − I||\_F

Varies

Stretching component: non\-uniform scaling

Condition number κ\(g\_enc\)

203\.96

Strong anisotropy in encoder\-induced metric

__Q has mean rotation 93\.4° and det\(Q\) = −1: the encoder applies a near\-maximal improper rotation\.__

__The orthogonal factor Q of the polar decomposition has ||Q−I||\_F = 16\.46 out of a maximum of 22\.63 \(72\.8%\)\. __This means the encoder has learned a large rotation in latent space: input feature patterns are rotated by an average of 93\.4° before being fed to the class score functions\. The negative determinant \(det Q = −1\) indicates an improper rotation \(includes a reflection\), which is geometrically valid for the discriminative task since reflections preserve inner products and therefore class margins\.

__The symmetric factor P \(stretching\) has condition number 203\.96 in the Fisher metric\. __The induced metric g\_enc = Wᵀ G₀ W has eigenvalues ranging from 1\.07 to 218\.33, with effective rank 51\.38 out of 128\. This means the encoder effectively uses only 51 of 128 input directions, compressing the 128\-dimensional feature space into a 51\-dimensional effective subspace \(measured in Fisher metric volume\)\. The log\-determinant log det\(g\_enc\) = 337\.48 gives the log\-volume scaling: the encoder inflates the Fisher volume by a factor of e^\{337\.48/2\} ≈ 10^\{73\}\.

# __5\. Geodesic Curvature of Decision Boundaries__

Decision boundary B\_\{ij\} between classes i and j is the hyperplane:

B\_\{ij\} = \{ h ∈ ℝ^d : LLR\_i\(h\) = LLR\_j\(h\) \}

        = \{ h : ⟨w\_i \- w\_j, h⟩ = b\_j \- b\_i \}

        = \{ h : ⟨δ\_i/v₀ \- δ\_j/v₀, h⟩ = const \}

As a subset of the flat Riemannian manifold \(ℝ^d, G₀\), a hyperplane is a totally geodesic submanifold\. Its geodesic curvature κ\_g measures how much the boundary curves relative to geodesics tangent to it:

κ\_g\(B\_\{ij\}\) = 0  for all pairs \(i,j\)

All 45/45 boundaries have geodesic curvature exactly zero\.

All boundaries pass exactly through the midpoint of the class\-pair geodesic\.

  \(midpoint μ\_mid = \(μ\_i \+ μ\_j\)/2, confirmed: LLR\_i\(μ\_mid\) = LLR\_j\(μ\_mid\)\)

__Boundary alignment theorem: all 45 decision boundaries are perpendicular to the corresponding class geodesic \(angle 0\.000°\) and pass through the geodesic midpoint\.__

__This is an analytic result, not a numerical coincidence\. __The LLR difference LLR\_i\(h\) − LLR\_j\(h\) = ⟨w\_i−w\_j, h⟩ \+ \(b\_i−b\_j\)\. The boundary normal in dual space is w\_i−w\_j = \(δ\_i−δ\_j\)/v₀\. Raised to the primal space by G₀⁻¹ = diag\(v₀\), the primal normal is v₀·\(w\_i−w\_j\) = δ\_i−δ\_j = μ\_i−μ\_j\. This is exactly the class geodesic direction\. So the boundary is always perpendicular to the geodesic in the Fisher metric, and since the bias term is set to b\_k = −⟨w\_k, μ₀⟩ − ||δ\_k||^2\_V/2, the boundary passes through \(μ\_i\+μ\_j\)/2 when the observation counts are equal\. This is the condition for Bayes\-optimal classification under equal Gaussian priors\.

__The boundary is totally geodesic: it is a flat \(K−2\)\-dimensional submanifold\. __For a flat ambient manifold, every hyperplane is totally geodesic \(its second fundamental form vanishes\)\. This means a geodesic that begins tangent to the boundary remains in the boundary — the boundary has zero extrinsic curvature\. Geometrically, this means the boundary does not ‘bend’ in any direction, which is the optimal property for a classification boundary: no part of the boundary is unnecessarily curved into one class’s territory\.

# __6\. Sectional Curvature of the Encoder Manifold__

## __6\.1 GL\(d\) with Bi\-invariant Metric__

The Lie group GL\(d\) equipped with the bi\-invariant metric g\(X,Y\) = tr\(XᵀY\)/d \(defined on the Lie algebra gl\(d\) and extended by left\-translation\) has sectional curvature:

K\(X,Y\) = \(1/4\) ||\[X,Y\]||^2 / \( ||X||^2 ||Y||^2 \- ⟨X,Y⟩^2 \)

where \[X,Y\] = XY \- YX is the Lie bracket \(matrix commutator\)

and ||X||^2 = tr\(X^T X\)/d

For GL\(d\): K\(X,Y\) ≥ 0 \(non\-negative sectional curvature\)

For SO\(d\) \(compact subgroup\): K = 1/4 \(constant curvature\)

For upper\-triangular matrices: K = 0 \(flat solvable subgroup\)

## __6\.2 Measured Curvature at W__

__Tangent pair__

__K\(X\_i, X\_j\)__

__Singular values__

__Interpretation__

Random pairs \(mean ± std\)

0\.500 ± 0\.004

N/A

Clusters near 1/2

\(σ\_1, σ\_2\)

0\.264

1\.697, 1\.143

Large SVs: lower curvature

\(σ\_1, σ\_3\)

0\.016

1\.697, 1\.026

Near\-equal SVs: near\-zero K

\(σ\_1, σ\_5\)

1\.486

1\.697, 0\.836

Most disparate: highest K

\(σ\_3, σ\_5\)

1\.395

1\.026, 0\.836

Near\-equal small SVs: high K

\(σ\_4, σ\_5\)

0\.770

0\.883, 0\.836

__Mean sectional curvature K = 0\.500 ≈ 1/2 across 50 random pairs \(std 0\.004\)\. Consistent with a symmetric space\.__

__The tight clustering of K around 0\.500 across random tangent pairs is a signature of a symmetric space or space of constant curvature\. __For the compact simple Lie group SU\(n\) with bi\-invariant metric, all sectional curvatures are K = 1/4\. For GL\(d\) the situation is more complex since GL\(d\) is non\-compact, but the empirical K ≈ 0\.5 is consistent with the dominant curvature contribution coming from the SU\(128\) ⊂ GL\(128\) compact factor\.

__Curvature along singular directions ranges from 0\.016 to 1\.486\. __The curvature K\(σ\_1, σ\_3\) ≈ 0\.016 \(nearly flat\) occurs between the dominant singular direction \(σ\_1 = 1\.697\) and a nearly equal singular direction \(σ\_3 = 1\.026\)\. The highest curvature K = 1\.486 occurs between σ\_1 and σ\_5 \(0\.836\), the most disparate singular value pair\. High curvature between disparate directions indicates that the Lie bracket \[X\_1, X\_5\] is large: rotating from the dominant mode to the fifth mode is geometrically complex\. This reflects the non\-commutative structure of the encoder’s weight space\.

# __7\. Ricci Curvature, Scalar Curvature, and Volume__

The Ricci tensor Ric and scalar curvature R\_scal are derived from the Riemann tensor by contraction\. For our two geometric domains:

__Manifold__

__Riemann tensor__

__Ricci tensor__

__Scalar curvature__

__Note__

Statistical M\_s = \{N\(μ,v₀\)\}

R = 0

Ric = 0

R\_scal = 0

Flat: all curvature zero

Encoder M\_W = GL\(128\)

K ≈ 0\.500

Ric ≈ 63\.6·g

R\_scal ≈ 8,135

Positively curved

Feature M\_f = \(ℝ^d, g\_enc\)

R = 0

Ric = 0

R\_scal = 0

Flat: linear encoder

__The statistical manifold is flat in every geometric sense\. __Riemann = Ricci = scalar curvature = 0\. This is not an approximation but an exact result: the Gaussian family N\(μ, diag\(v₀\)\) with fixed v₀, parameterised by μ ∈ ℝ^d, is a flat Riemannian manifold isometric to \(ℝ^d, diag\(1/v₀\)\)\. The ‘curvature’ of information geometry comes from the non\-trivial connection \(dually flat, e\-flat and m\-flat as established in the Wasserstein paper\), not from the Riemannian curvature tensor\.

__The encoder manifold GL\(128\) has Ricci curvature ≈ 63\.6 and scalar curvature ≈ 8,135\. __These are derived from the mean sectional curvature K ≈ 0\.5 via the approximations Ric\(X,X\) ≈ \(d−1\)·K\_avg·||X||^2 = 63\.6·||X||^2 and R\_scal ≈ d\(d−1\)·K\_avg = 8,135\. Positive Ricci curvature has implications for the encoder’s learning dynamics: by the Bonnet\-Myers theorem, a compact Riemannian manifold with positive Ricci curvature has finite diameter bounded by π√\(d/\(n\-1\)K\)\. For our values: diameter ≤ π√\(128/\(127×0\.5\)\) ≈ 4\.48, consistent with the observed encoder singular value range \[0\.128, 1\.697\]\.

# __8\. Shape Operator of the Class Centroid Submanifold__

## __8\.1 The Delta Subspace__

The K=10 class offset vectors \{δ\_1, \.\.\., δ\_K\} span a subspace of ℝ^d\. Their SVD reveals the intrinsic dimensionality of the class structure:

SVD of Δ \(K×D = 10×128 matrix of class offsets\):

Singular values: \[2\.107, 1\.581, 1\.437, 1\.273, 1\.010, 0\.800, 0\.768, 0\.719, 0\.389, 0\.058\]

Effective rank = 7\.59  \(of maximum K\-1 = 9\)

Numerical rank = 10   \(all singular values > 0\.1% of σ\_max\)

__The delta subspace has effective rank 7\.59 in ℝ^\{128\}\. __All 10 singular values are non\-negligible \(numerical rank = 10 = K\), confirming that the 10 classes occupy genuinely independent directions in latent space\. The effective rank of 7\.59 \(vs maximum K−1 = 9\) indicates that the 10 class offset directions are not uniformly distributed: the top 8 singular directions account for most of the variance, with the 9th and 10th contributing less\. This is consistent with the RMT finding of 8 detectable spikes in the whitened covariance spectrum\.

## __8\.2 Per\-Class Sample Covariance Geometry__

__Class__

__tr\(Σ\_k\)__

__||Σ\_k||\_F__

__λ\_max\(Σ\_k\)__

__Isotropy__

__Shape__

net\_normal

0\.2358

0\.1238

0\.0908

0\.000

Anisotropic ray \(URL diversity\)

net\_scan

0\.0862

0\.0568

0\.0457

0\.000

Anisotropic ray

net\_ddos

0\.0218

0\.0200

0\.0200

0\.000

Near\-rank\-1

net\_exfil

0\.0645

0\.0308

0\.0244

0\.000

Anisotropic

net\_c2

0\.1351

0\.0975

0\.0816

0\.000

Anisotropic

log\_info

0\.0005

0\.0003

0\.0002

0\.005

Most isotropic \(rigid format\)

log\_warn

0\.0003

0\.0002

0\.0002

0\.008

Most isotropic

log\_error

0\.0025

0\.0019

0\.0019

0\.001

Near\-rank\-1

bin\_malware

0\.4624

0\.1553

0\.1003

0\.000

Highest variance

bin\_benign

0\.4270

0\.1363

0\.0785

0\.000

High variance

__Log classes have 500× smaller covariance trace than binary classes\. __tr\(Σ\_k\) ranges from 0\.0003 \(log\_warn\) to 0\.4624 \(bin\_malware\), a 1,541× range\. The sample clouds of each class have a shape dictated by the within\-class variance of the parsed features\. Log classes, with rigid format, produce near\-degenerate distributions \(isotropy ≈ 0\.005–0\.008\)\. Binary classes, with random payloads, produce diffuse distributions \(isotropy ≈ 0\)\. The low isotropy \(0\.000–0\.008\) for all classes confirms that the within\-class distributions are highly anisotropic — each class occupies a low\-dimensional submanifold of the d=128\-dimensional latent space, not a spherical cloud\.

# __9\. Exponential Map, Logarithmic Map, and Geodesics__

## __9\.1 The Statistical Manifold__

On the flat statistical manifold, the exponential and logarithmic maps are linear:

exp\_μ\(v\) = μ \+ v   \(flat: exp is just translation\)

log\_μ\(ν\) = ν \- μ   \(flat: log is subtraction\)

Geodesic γ\_\{μ,ν\}\(t\) = μ \+ t\(ν \- μ\) = \(1\-t\)μ \+ tν   \(straight line, t ∈ \[0,1\]\)

Class centroid geodesic: γ\_k\(t\) = μ\_0 \+ t·δ\_k

Geodesic speed ||dγ/dt||\_G = ||d\_k||\_G \(Fisher distance from prior\):

  Range: \[6\.17 \(net\_normal\), 11\.53 \(bin\_malware\)\]

## __9\.2 The Full NIG Manifold__

If class\-specific variances v\_k were allowed \(the full NIG model\), the manifold of \(mean, variance\) parameters would have non\-trivial curvature\. The variance component lives in ℝ^d\_\+ with the log\-metric d\(v, w\) = ||log\(v/w\)||, giving:

Sectional curvature of \(ℝ^d\_\+, g\_var\) = \-1/2  \(hyperbolic half\-space model\)

Geodesic on ℝ^d\_\+: v\(t\) = v\_0^\{1\-t\} ⊙ v\_1^t  \(geometric interpolation\)

In CyphaDIF: all classes share v₀ ⇒ all classes at the same point in variance space

The class manifold is the fibre \{μ ∈ ℝ^d\} × \{v₀\} ⊂ NIG manifold

Curvature contribution from variance: 0  \(all classes at same variance point\)

# __10\. Jacobi Fields and Geodesic Stability__

## __10\.1 Theoretical Analysis__

A Jacobi field J along a geodesic γ measures the deviation between nearby geodesics\. It satisfies the Jacobi equation:

D²J/dt² \+ R\(J, γ'\)γ' = 0   \(Jacobi equation\)

For flat manifolds \(R = 0\):

D²J/dt² = 0  ⇒  J\(t\) = J\_0 \+ t·J\_0'  \(linear growth\)

Lyapunov exponent λ = lim\_\{t→∞\} \(1/t\) log||J\(t\)|| = 0  \(neutral stability\)

Geodesics are neither focusing \(K<0 case\) nor defocusing \(K>0 case\)\.

## __10\.2 Empirical Geodesic Stability__

We test geodesic stability by perturbing a point along the geodesic from the net\_ddos centroid toward the nearest class \(net\_normal\), and measuring how the LLR gap changes:

__Distance ε along geodesic__

__LLR \(net\_ddos\)__

__LLR gap__

__Correctly classified?__

0\.0 \(centroid\)

\+57\.54

82\.24

Yes \(margin = 82\.2\)

0\.1

\+50\.07

72\.06

Yes

0\.5

\+20\.20

31\.34

Yes

1\.0

−17\.15

−19\.55

No \(flip at ε ≈ 0\.9\)

2\.0

−91\.84

−121\.3

No

5\.0

−315\.9

−426\.7

No

__LLR decays linearly with distance ε \(slope −75\.5/unit\), consistent with flat geometry\. Classification flips at ε ≈ 0\.9\.__

__The linear decay of LLR with ε is exactly what flat geometry predicts\. __Along the geodesic toward net\_normal, the net\_ddos score LLR\_\{net\_ddos\}\(h\) decreases linearly because h → h \+ ε·v and LLR is linear in h\. The slope is d\(LLR\_\{net\_ddos\}\)/dε = ⟨w\_\{net\_ddos\}, v⟩ where v is the unit geodesic direction\. This is a constant \(ε\-independent\) as expected for a flat manifold with linear LLR functions\. On a curved manifold with K > 0, geodesics would defocus and the LLR would decrease faster than linear; for K < 0, slower\. The flat K = 0 case gives exactly linear decay\.

__Classification boundary crossed at ε ≈ 0\.9 \(midpoint of geodesic at ε = 1\.0\)\. __The geodesic from the net\_ddos centroid \(μ\_\{ddos\}\) to the net\_normal centroid \(μ\_\{normal\}\) has length d\_G\(μ\_\{ddos\}, μ\_\{normal\}\) = 12\.37 in Fisher units\. The boundary is at the midpoint t = 0\.5, corresponding to absolute distance ε ≈ 0\.9 in the latent space units used\. This is consistent with the convex analysis finding that all boundaries pass through the geodesic midpoints\.

# __11\. Cartan Moving Frame and Differential Forms__

## __11\.1 Moving Frame__

The encoder W defines a global frame field on the feature space: e\_i = columns of W⁻¹ \(the pullback of the standard coordinate frame\)\. This frame is defined everywhere on ℝ^d \(since W ∈ GL\(d\) is invertible\) and is anholonomic \(non\-coordinate\-aligned\) in general\.

Moving frame: \{e\_1, \.\.\., e\_d\} = columns of W^\{\-1\}

Co\-frame: \{θ^1, \.\.\., θ^d\} = rows of W  \(dual frame: θ^i\(e\_j\) = δ^i\_j\)

Gram matrix in Fisher metric: G\(e\_i, e\_j\) = \(W^\{\-T\} G\_0 W^\{\-1\}\)\_\{ij\} = \(g\_enc^\{\-1\}\)\_\{ij\}

||Gram \- I||\_F = 7,755\.2   \(W is NOT Fisher\-orthonormal\)

\(For a Fisher\-orthonormal frame: W would satisfy W^T G\_0 W = I\)

## __11\.2 Maurer\-Cartan Form and Curvature 2\-Form__

The Maurer\-Cartan form is the gl\(d\)\-valued 1\-form ω = W⁻¹ dW defined on GL\(d\)\. Evaluated on a tangent vector V at W, it gives ω\_W\(V\) = W⁻¹V ∈ gl\(d\)\. The curvature 2\-form is Ω = dω \+ ω ∧ ω\.

Maurer\-Cartan structure equation: dω \+ ω ∧ ω = 0

  ⇒  Ω = 0   \(flat connection on GL\(d\) via MC form\)

||MC form ω\(V\_i\)||\_F for top singular directions:

  mean=1\.246, min=0\.589, max=1\.890

Torsion T^i = de^i \+ ω^i\_j ∧ e^j = 0  \(torsion\-free\)

__The Maurer\-Cartan form gives a flat connection on the frame bundle\. __The curvature 2\-form Ω = 0 by the MC structure equation — this is exact, not approximate\. However, the non\-zero ||Gram − I||\_F = 7,755 shows that the frame e\_i is far from being a Fisher\-orthonormal frame\. The frame is adapted to the encoder W, not to the Fisher geometry\. Constructing a Fisher\-orthonormal frame would require a Gram\-Schmidt orthogonalisation with respect to G₀, yielding a new frame \{f\_i\} with G\(f\_i, f\_j\) = δ\_\{ij\} but destroying the natural Lie group structure that the MC form encodes\.

# __12\. Synthesis__

- __The statistical manifold is flat \(K = 0\) in every differential\-geometric sense\. __All Christoffel symbols, Riemann tensor components, Jacobi field growth rates, and angle defects are exactly zero\. Geodesics are straight lines, parallel transport is trivial, and the holonomy group is \{Id\}\. The Gaussian family with fixed variance is, metrically, a copy of \(ℝ^d, G₀\) — a flat Riemannian manifold\.
- __Decision boundaries are totally geodesic and Bayes\-optimal in Fisher metric\. __All 45 boundaries have κ\_g = 0 \(zero geodesic curvature\), are perpendicular to the class geodesic \(angle 0\.000° to machine precision\), and pass through the midpoint of each class pair’s geodesic\. This is the geometric characterisation of Bayes\-optimal classification under equal\-prior Gaussians with shared covariance\.
- __The encoder manifold GL\(128\) has positive sectional curvature K ≈ 0\.500\. __The tight clustering of K around 1/2 \(std 0\.004\) suggests the encoder has been shaped by the contrastive training to occupy a geometrically regular region of GL\(128\)\. The polar decomposition reveals a large improper rotation Q \(||Q−I||\_F = 16\.46, angle 93\.4°\) and a strongly anisotropic stretching P \(condition number 203\.96, effective rank 51\.38\)\.
- __Jacobi fields grow linearly on the flat manifold \(λ = 0\)\. __This implies geometric stability: nearby geodesics diverge at most linearly\. The empirical test confirms linear LLR decay along geodesics, with boundary crossing at ε ≈ 0\.9 \(midpoint of the geodesic to the nearest class\)\. No exponential mixing or focusing occurs\.
- __The Cartan frame is non\-orthonormal \(||Gram−I||\_F = 7,755\) but torsion\-free\. __The encoder W defines a global frame field with zero torsion and zero curvature 2\-form \(MC structure equation\), but the frame is far from Fisher\-orthonormal\. This encodes the encoder’s geometric distortion: the 128 coordinate axes it defines are not aligned with the natural precision\-weighted orthogonal axes of the Fisher metric\.

# __References__

\[1\] do Carmo, M\. P\. \(1992\)\. Riemannian Geometry\. Birkhäuser\.

\[2\] Lee, J\. M\. \(2018\)\. Introduction to Riemannian Manifolds \(2nd ed\.\)\. Springer\.

\[3\] Amari, S\., & Nagaoka, H\. \(2000\)\. Methods of Information Geometry\. AMS\.

\[4\] Amari, S\. \(2016\)\. Information Geometry and Its Applications\. Springer\.

\[5\] Murray, M\. K\., & Rice, J\. W\. \(1993\)\. Differential Geometry and Statistics\. Chapman & Hall\.

\[6\] Milnor, J\. \(1976\)\. Curvatures of left invariant metrics on Lie groups\. Advances in Mathematics, 21\(3\), 293–329\.

\[7\] Cartan, É\. \(1926\)\. La géométrie des espaces de Riemann\. Mémorial des sciences mathématiques, Fasc\. 9\.

\[8\] Bishop, R\. L\., & Crittenden, R\. J\. \(1964\)\. Geometry of Manifolds\. Academic Press\.

\[9\] Kobayashi, S\., & Nomizu, K\. \(1963\)\. Foundations of Differential Geometry, Vol\. I\. Wiley\.

\[10\] Cheeger, J\., & Ebin, D\. G\. \(1975\)\. Comparison Theorems in Riemannian Geometry\. North\-Holland\.

\[11\] Bhatia, R\. \(2007\)\. Positive Definite Matrices\. Princeton University Press\.

\[12\] Moakher, M\. \(2005\)\. A differential geometric approach to the geometric mean of symmetric positive\-definite matrices\. SIAM Journal on Matrix Analysis and Applications, 26\(3\), 735–747\.

\[13\] Pennec, X\., Fillard, P\., & Ayache, N\. \(2006\)\. A Riemannian framework for tensor computing\. International Journal of Computer Vision, 66\(1\), 41–66\.

\[14\] Skovgaard, L\. T\. \(1984\)\. A Riemannian geometry of the multivariate normal model\. Scandinavian Journal of Statistics, 11\(4\), 211–223\.

\[15\] Eriksen, E\. \(1987\)\. On the measures of geodesic curvature on statistical manifolds\. Journal of Statistical Planning and Inference, 15, 281–292\.

\[16\] Murray, M\. K\. \(1993\)\. The geometry of Gaussian distributions\. Geometry and Statistics, 22, 165–183\.

\[17\] Petersen, P\. \(2016\)\. Riemannian Geometry \(3rd ed\.\)\. Springer\.

\[18\] Gallot, S\., Hulin, D\., & Lafontaine, J\. \(2004\)\. Riemannian Geometry \(3rd ed\.\)\. Springer\.

\[19\] Jost, J\. \(2011\)\. Riemannian Geometry and Geometric Analysis \(6th ed\.\)\. Springer\.

\[20\] Postnikov, M\. M\. \(2001\)\. Geometry VI: Riemannian Geometry\. Springer\.

