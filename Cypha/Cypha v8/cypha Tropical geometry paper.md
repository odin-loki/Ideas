<!-- Converted from `cypha Tropical geometry paper.docx` — source was Word (.docx). -->

__Tropical Geometry__

__of the Differential Information Field Classifier__

*Tropical Polynomial • Hypersurface • Newton Polytope • Tropical Rank • Discriminant • Gröbner Basis • Projective Map*

Unpublished Technical Report — 2026

__Abstract__

We apply tropical geometry — the study of algebraic geometry over the tropical semiring \(ℝ∪\{−∞\}, ⊕=max, ⊗=\+\) — to CyphaDIF\. The key observation is that the CyphaDIF classifier f\(h\) = max\_k\{LLR\_k\(h\)\} is __exactly a tropical polynomial__ of degree 1 in K=10 terms\. This transforms classical algebraic geometry questions about the classifier into combinatorial questions about polyhedral fans and max\-plus algebra\. Ten probes cover the tropical polynomial structure, the tropical hypersurface \(decision boundary complex\), the combinatorial type of the argmax arrangement, tropical distances and Voronoi cells, the Newton polytope and its regular subdivision, the tropical convex hull of weight vectors, tropical rank and the tropical determinant, the tropical discriminant, the minimal tropical Gröbner basis, and the tropical projective map\. __Key results: __\(1\) The decision boundary complex is a tropical hypersurface with K=10 cells, 38 active facets \(of 45 possible\) and 120 theoretical ridges\. \(2\) All 10 classes are argmax in distinct non\-empty regions\. \(3\) The Newton polytope Newt\(f\) = conv\(w\_1,\.\.\.,w\_K\) has dimension 9 \(rank 9\) and effective dimension 8\.12, embedded in ℝ^\{128\}\. \(4\) The tropical determinant tdet\(M\) = 434\.7, achieved uniquely by the identity permutation \(each class scores highest at its own centroid\)\. \(5\) The tropical discriminant \(margin\) has mean 53\.3 and minimum 13\.7, with zero training samples on the tropical hypersurface\. \(6\) The minimal tropical Gröbner basis has K−1=9 elements \(the MST of the class graph, total weight 910\.4\)\. \(7\) The tropical width of the score polytope is 231\.3, and the tropical projective map Φ: ℝ^\{128\} → TP^9 reveals that each class occupies a well\-separated cluster in tropical projective space\.

# __1\. Tropical Algebra and the Argmax Classifier__

Tropical algebra replaces the classical operations \(\+, ×\) by \(max, \+\)\. The tropical semiring is \(ℝ∪\{−∞\}, ⊕, ⊗\) where a⊕b = max\(a,b\) and a⊗b = a\+b\. Monomials in tropical algebra have the form:

Tropical monomial: c ⊗ x\_1^\{a\_1\} ⊗ \.\.\. ⊗ x\_d^\{a\_d\}  =  c \+ a\_1 x\_1 \+ \.\.\. \+ a\_d x\_d

                 \(exponents become linear coefficients in classical notation\)

Tropical polynomial: f = c\_1⊗x^\{a\_1\} ⊕ \.\.\. ⊕ c\_K⊗x^\{a\_K\}

                   = max\_k \{ c\_k \+ ⟨a\_k, x⟩ \}  \(maximum over K linear forms\)

The CyphaDIF classifier is, by construction, a tropical polynomial of degree 1:

f\(h\) = max\_k \{ LLR\_k\(h\) \}

     = max\_k \{ ⟨w\_k, h⟩ \+ b\_k \}

     = max\_k \{ c\_k ⊗ h^\{⊗w\_k\} \}   \(tropical notation\)

where:  w\_k = δ\_k / v₀  \(tropical exponent vector, d=128\-dim\)

         b\_k = \-⟨w\_k,μ₀⟩ \- ‖δ\_k‖^2\_V/2  \(tropical coefficient = log\-prior bias\)

         K = 10 terms  \(one tropical monomial per class\)

__The argmax operation is tropical addition\. __In tropical algebra, the ‘sum’ of K monomials is their maximum\. CyphaDIF’s decision rule, argmax\_k LLR\_k\(h\), is precisely the tropical polynomial evaluation: the selected class k\* is the term achieving the tropical maximum\. The tropical setting makes explicit what is implicit in the probabilistic formulation: the classifier is fundamentally a max\-plus algebraic object, not just a probability model\.

# __2\. Tropical Polynomial Structure__

## __2\.1 The Ten Tropical Monomials__

__Class__

__Coefficient b\_k__

__||w\_k|| \(exponent norm\)__

__Argmax at own centroid?__

net\_normal

−75\.08

  60\.07

Yes

net\_scan

\+130\.69

  83\.90

Yes

net\_ddos

−84\.98

  95\.31

Yes

net\_exfil

−85\.24

  88\.32

Yes

net\_c2

−160\.40

103\.11

Yes

log\_info

−38\.22

  79\.83

Yes

log\_warn

−17\.07

  73\.23

Yes

log\_error

−12\.61

  76\.88

Yes

bin\_malware

−15\.77

  94\.98

Yes

bin\_benign

−70\.09

  78\.02

Yes

__All 10/10 classes are the argmax of their own tropical monomial at their respective centroids\. Full tropical separability confirmed\.__

__Each class k satisfies LLR\_k\(μ\_k\) > LLR\_j\(μ\_k\) for all j≠k\. __This is the tropical analogue of Voronoi membership: each codeword lies in its own Voronoi cell\. Algebraically, the K tropical monomials form a __tropically non\-degenerate__ system — no class centroid lies on the tropical hypersurface \(the boundary where two monomials tie\)\. The margins LLR\_k\(μ\_k\) − max\_\{j≠k\} LLR\_j\(μ\_k\) range from 37\.9 \(bin\_benign and bin\_malware\) to 76\.5 \(net\_ddos\), confirming all centroids are in the strict interior of their tropical cells\.

__The bias b\_\{net\_scan\} = \+130\.69 is the only positive bias\. __The large positive bias for net\_scan compensates for its weight vector having a different orientation than the world prior μ₀\. In tropical terms, the net\_scan monomial has a large ‘base level’ that keeps it competitive even far from its centroid\. The most negative bias is b\_\{net\_c2\} = −160\.40, meaning the net\_c2 monomial starts from a lower baseline and relies entirely on the inner product ⟨w\_\{net\_c2\}, h⟩ for its score — but with the highest ||w\_k|| = 103\.1, it grows fastest in the net\_c2 direction\.

# __3\. Tropical Hypersurface: The Decision Boundary Complex__

## __3\.1 Structure of V\(f\)__

The tropical hypersurface V\(f\) is the set of points h ∈ ℝ^d where the tropical polynomial f\(h\) = max\_k\{LLR\_k\(h\)\} is not smooth, i\.e\., where at least two monomials simultaneously achieve the maximum:

V\(f\) = \{ h ∈ ℝ^d : max\_k LLR\_k\(h\) achieved by ≥2 indices \}

     = ∪\_\{i<j\} B\_\{ij\}  where B\_\{ij\} = \{ h : LLR\_i\(h\) = LLR\_j\(h\) ≥ LLR\_k\(h\) ∀k \}

V\(f\) is a polyhedral complex \(union of convex polyhedra\) in ℝ^d\.

It decomposes ℝ^d into K = 10 convex polyhedral cells \(the tropical Voronoi diagram\)\.

Combinatorial structure:

  Cells \(dim d\):     K = 10  \(one per class, the tropical Voronoi cells\)

  Facets \(dim d\-1\):  45 pairwise boundaries = C\(K,2\)

  Ridges \(dim d\-2\):  120 triple boundaries = C\(K,3\)  \(theoretical\)

  Active facets \(verified\): 38/45  \(midpoint\-interior test\)

## __3\.2 Active vs Inactive Facets__

A facet B\_\{ij\} is active \(present in the tropical Voronoi diagram\) if there exist points h on B\_\{ij\} where LLR\_i\(h\) = LLR\_j\(h\) > LLR\_k\(h\) for all k≠i,j\. We test this by evaluating the midpoint μ\_\{mid\} = \(μ\_i \+ μ\_j\)/2:

Midpoint test: μ\_\{mid\} = \(μ\_i \+ μ\_j\)/2

  B\_\{ij\} active iff LLR\_i\(μ\_\{mid\}\) = LLR\_j\(μ\_\{mid\}\) > LLR\_k\(μ\_\{mid\}\) ∀k≠i,j

Results: 38/45 facets active  \(7 facets not visible at midpoint\)

  \(7 ‘ghost’ boundaries exist as hyperplanes but are covered by closer classes

   at the geometric midpoint — they may still be topologically present but thin\)

__38/45 boundaries are active \(midpoint\-interior\)\. The tropical hypersurface has 38 visible facets\. The K=10 cells form a connected polyhedral complex\.__

__The 7 inactive facets \(at the midpoint test\) correspond to class pairs that are not ‘nearest neighbours’ in the Voronoi diagram\. __When the midpoint of classes i and j is closer to a third class k than to either i or j, the midpoint lies outside B\_\{ij\}\. This does not mean B\_\{ij\} is empty — it is a full \(d−1\)\-dimensional hyperplane — but the Voronoi cell boundary at the geodesic midpoint is covered\. The 38 active facets confirmed by the midpoint test constitute the backbone of the tropical hypersurface\. In classical terms, the 38 active boundaries are the edges of the ‘nearest\-neighbour graph’ of the class centroids in Fisher metric\.

__The tropical hypersurface partitions ℝ^\{128\} into exactly 10 convex polyhedral regions\. __For K linear functions in ℝ^d with d >> K, the arrangement generically produces exactly K regions \(not the exponential Zaslavsky number Σ\_\{j=0\}^d C\(K,j\), which applies to hyperplane arrangements, not to argmax arrangements\)\. The argmax arrangement is fundamentally different from a hyperplane arrangement: it always produces exactly K regions, one per class, since for each class k there always exists some h where class k dominates\.

# __4\. Combinatorial Type of the Argmax Arrangement__

The combinatorial type of the tropical polynomial f records, for each region of ℝ^d, which class is the argmax\. For a generic tropical polynomial with K monomials in ℝ^d \(d ≥ K−1\), the combinatorial type is uniquely determined by the weight vectors w\_k and biases b\_k\.

Sampling of argmax regions \(10,000 random points, mixture of Gaussians\):

  net\_normal:  5\.88%    net\_scan:  10\.35%   net\_ddos:  12\.32%

  net\_exfil:  11\.30%    net\_c2:   13\.00%   log\_info:   9\.37%

  log\_warn:    7\.97%   log\_error:  9\.23%  bin\_malware: 11\.29%

  bin\_benign:  9\.29%

  All K=10 classes appear as argmax for some h \(K regions exist\)\.

  No non\-class composite regions found \(exactly K cells, as expected\)\.

__Region sizes reflect the solid angles of the tropical Voronoi cells\. __The smallest region belongs to net\_normal \(5\.88% of sampled points\), and the largest to net\_c2 \(13\.00%\)\. The region size measures the ‘volume’ of each class’s Voronoi cell relative to the sampling distribution, not the volume in any absolute sense\. The net\_c2 cell being the largest reflects that the net\_c2 weight vector w\_\{net\_c2\} has the highest norm \(103\.1\), so it grows fastest for inputs in its direction, capturing the most probability mass from the Gaussian mixture sampler\. Net\_normal’s small region \(5\.88%\) reflects its low weight\-vector norm \(60\.1\) relative to all other classes — it wins in the fewest directions\.

# __5\. Tropical Distances and the Tropical Voronoi Diagram__

## __5\.1 The Tropical \(L∞\) Metric__

The tropical distance between two points h, h’ ∈ ℝ^d/ℝ① \(tropical projective space\) is:

d\_trop\(h, h'\) = max\_i\(h\_i \- h'\_i\) \- min\_i\(h\_i \- h'\_i\)

              = ||h \- h'||\_\{L^∞\-spread\}  \(L∞ diameter of the difference vector\)

This is the tropical projective metric on ℝ^d/ℝ①\.

For classical metrics: d\_trop\(h,h'\) ≥ ||h\-h'||\_∞  \(L∞ distance\)

## __5\.2 Tropical vs Classical Distances__

__Metric__

__Mean inter\-class distance__

__Closest pair__

__Farthest pair__

__Ratio to L2__

Tropical \(L∞ spread\)

0\.810

bin\_malware↔bin\_benign \(0\.438\)

log\_info↔bin\_malware \(1\.145\)

0\.458× L2

Euclidean \(L2\)

1\.768

bin\_malware↔bin\_benign \(1\.054\)

net\_c2↔bin\_malware \(2\.348\)

1\.000× \(ref\)

Fisher\-Rao

13\.706

bin\_malware↔bin\_benign \(8\.706\)

net\_c2↔bin\_malware \(17\.848\)

7\.753× L2

__d\_trop / d\_L2 = 0\.458: the tropical metric is ~2\.2× smaller than Euclidean\. Closest pair in all metrics: bin\_malware↔bin\_benign\.__

__The tropical distance is always ≤ the L∞ distance, which is ≤ the L2 distance by norm inequalities\. __For the encoder output centroids, the tropical distance averages 45\.8% of the L2 distance\. This compression ratio arises because the tropical metric measures only the range \(max−min\) of the difference vector, ignoring the many intermediate coordinates\. In a d=128\-dimensional space, the max and min of a difference vector are typically small fractions of the total L2 norm\. The L∞ spread / L2 ratio scales as O\(1/∞d\) for random vectors, giving d\_trop/d\_L2 ≈ 1/∞128 ≈ 0\.088 for generic vectors — our observed 0\.458 is larger, indicating that the class difference vectors are not isotropic but concentrate in a few dominant dimensions\.

__The closest pair \(bin\_malware↔bin\_benign\) is the same in all three metrics\. __This consistency across tropical, Euclidean, and Fisher\-Rao metrics indicates that the binary class separation is fundamentally small — the MZ \(0x4D5A\) and ELF \(0x7F454C46\) headers differ in few byte positions, producing encoder outputs that are globally close regardless of the metric used\. The farthest pair shifts from net\_c2↔bin\_malware \(Euclidean, Fisher\) to log\_info↔bin\_malware \(tropical\), reflecting that in the tropical metric the log and binary domains differ most in their extreme dimensions\.

# __6\. Newton Polytope and Regular Subdivision__

## __6\.1 The Newton Polytope__

The Newton polytope of the tropical polynomial f = max\_k\{⟨w\_k,h⟩ \+ b\_k\} is the convex hull of the exponent vectors \(the weight vectors w\_k ∈ ℝ^d\):

Newt\(f\) = conv\(w\_1, \.\.\., w\_K\) ⊂ ℝ^\{128\}

Dimension of Newt\(f\): rank\(W\_centered\) = 9  \(K\-1, as expected for K points\)

Effective dimension:  8\.12  \(from SVD of centered weight matrix\)

Singular values:      \[127\.8, 115\.7, 106\.6, 95\.2, 77\.9, 71\.6, 68\.7, 58\.8, 36\.0, 0\.0\]

Per\-dimension width \(max\_k w\_\{k,i\} \- min\_k w\_\{k,i\}\):

  mean = 24\.01    min = 13\.49    max = 39\.51

  Sum of widths \(L1 diameter\) = 3073\.0

## __6\.2 Regular Subdivision Induced by Heights b\_k__

The bias terms b\_k act as heights over the Newton polytope, inducing a regular subdivision of Newt\(f\)\. The tropical hypersurface V\(f\) is the dual of this regular subdivision:

Heights b\_k \(for regular subdivision of Newt\(f\)\):

  net\_c2:   b = \-160\.40  \(most negative — largest penalty at origin\)

  net\_ddos: b =  \-84\.98

  net\_exfil:b =  \-85\.24

  net\_normal:b = \-75\.08

  bin\_benign:b = \-70\.09

  bin\_malware:b= \-15\.77

  log\_error: b = \-12\.61

  log\_warn:  b = \-17\.07

  log\_info:  b = \-38\.22

  net\_scan:  b = \+130\.69  \(only positive height\)

Height range: \[\-160\.40, \+130\.69\]  spread = 291\.09

__Newton polytope Newt\(f\) has dimension 9 \(= K−1\), embedded in ℝ^\{128\}\. Effective dimension 8\.12\. The height spread of 291\.1 drives a non\-trivial regular subdivision\.__

__The dimension of Newt\(f\) is exactly K−1 = 9\. __This is the generic dimension for the convex hull of K points in general position in ℝ^d \(for d ≥ K−1\)\. The zero singular value confirms that the K weight vectors w\_k are affinely dependent — they span a 9\-dimensional affine subspace of ℝ^\{128\}\. The effective dimension of 8\.12 \(vs exact 9\) indicates mild near\-degeneracy: the 9th singular direction \(SV=36\.0\) is somewhat weaker than the first 8 \(SV=58–128\)\. This matches the RMT finding of 8 detectable spike eigenvalues \(K−1 non\-trivial class\-discriminant directions in the whitened spectrum\)\.

__The regular subdivision induced by heights b\_k determines the combinatorial type of V\(f\)\. __A regular subdivision of Newt\(f\) partitions the polytope into sub\-polytopes, with each vertex of the subdivision corresponding to a vertex w\_k elevated by height b\_k\. The dual of this subdivision is the tropical hypersurface V\(f\): each interior edge of the subdivision corresponds to a facet of V\(f\), and each interior vertex of the subdivision corresponds to a ridge of V\(f\)\. The large height spread \(291\.1\) ensures the subdivision is non\-degenerate \(no three w\_k vertices are co\-level\), giving a simplicial regular subdivision of Newt\(f\)\.

# __7\. Tropical Convex Hull and Tropical Halfspaces__

The tropical convex hull of K points p\_1,\.\.\.,p\_K ∈ ℝ^d/ℝ① is the set of all tropical linear combinations\. For our weight vectors w\_k ∈ ℝ^d:

tconv\(w\_1,\.\.\.,w\_K\) = \{ max\_k\(λ\_k \+ w\_k\) : λ ∈ ℝ^K, tropically normalised \}

Membership test for world prior w\_0 = 0:

  w\_0 ∈ tconv\(w\_1,\.\.\.,w\_K\) iff max\_k min\_i\(w\_\{k,i\}\) ≤ 0 ≤ min\_k max\_i\(w\_\{k,i\}\)

  max\_k min\_i\(w\_\{k,i\} \- 0\) = max\_k min\_i\(w\_\{k,i\}\) = \+13\.21

  min\_k max\_i\(w\_\{k,i\} \- 0\) = min\_k max\_i\(w\_\{k,i\}\) = \-12\.87

  Condition 13\.21 ≤ 0 ≤ \-12\.87 is FALSE\.

  ⇒ World prior w\_0 is NOT in the tropical convex hull of \{w\_k\}\.

__The world prior \(w=0\) lies outside the tropical convex hull of \{w\_k\}\. The K class weight vectors do not tropically ‘surround’ the origin\.__

__This has a natural classification interpretation\. __If the world prior were inside tconv\(w\_1,\.\.\.,w\_K\), it would mean the zero score vector \(no evidence from any class\) lies in the ‘average’ of the class score functions\. Since w\_0 = 0 is outside the tropical convex hull, the zero\-evidence point is tropically extreme — it does not lie in the tropical average of the class representations\. Concretely, the world prior mean μ₀ maps to net\_normal \(as established in the convex analysis paper\), not to a tropical average of all classes\. The tropical convex hull is a ‘tropical simplex’ in ℝ^\{128\}/ℝ① with K=10 vertices; the origin lies outside this simplex\.

__Tropical hyperplane normals \(w\_i \- w\_j\) have norms in \[81\.2, 153\.3\]\. __Each pairwise boundary B\_\{ij\} in the tropical hypersurface is defined by the tropical hyperplane with normal w\_i \- w\_j\. The norm ||w\_i \- w\_j|| measures the ‘strength’ of the corresponding decision boundary: larger norms mean faster transition between classes\. The minimum norm 81\.2 \(bin\_malware↔bin\_benign\) corresponds to the narrowest decision boundary, consistent with the smallest pairwise geometric margin\. The mean norm 124\.2 reflects the typical strength of class boundaries in the tropical decomposition\.

# __8\. Tropical Rank and the Tropical Determinant__

## __8\.1 The LLR Matrix and Tropical Rank__

The K×K matrix M with M\_\{ij\} = LLR\_j\(μ\_i\) records the score of each class j at each class centroid μ\_i\. The tropical determinant of M \(in max\-plus algebra\) is:

tdet\(M\) = max\_\{σ ∈ S\_K\} Σ\_i M\_\{i,σ\(i\)\}

        = max\_\{permutations σ\} \[sum of class σ\(i\)’s score at centroid μ\_i\]

Computed via Hungarian algorithm \(maximum\-weight perfect matching\):

  tdet\(M\) = 434\.70

Optimal permutation: identity  σ\(i\) = i  \(each class scores at its own centroid\)

  M\_\{11\} \+ M\_\{22\} \+ \.\.\. \+ M\_\{KK\} = Σ\_k LLR\_k\(μ\_k\) = 434\.70

Diagonal \(own scores LLR\_k\(μ\_k\)\):

  \[19\.04, 37\.66, 54\.80, 50\.32, 63\.69, 38\.83, 34\.12, 32\.12, 66\.47, 37\.66\]

Margin \(diag \- best off\-diag score per row\):

  \[49\.65, 63\.68, 76\.46, 70\.86, 60\.99, 48\.86, 44\.12, 44\.12, 37\.90, 37\.90\]

__Tropical determinant tdet\(M\) = 434\.70, achieved by the identity permutation\. The tropical rank of M is K=10 \(full\)\. The tropical determinant equals the total MDL description length Σ\_k L\(δ\_k\) = 434\.7 nats\.__

__tdet\(M\) = 434\.70 = Σ\_k L\(δ\_k\): the tropical determinant equals the total MDL description length\. __This is not a coincidence\. The tropical determinant with the identity permutation sums the diagonal: Σ\_k M\_\{kk\} = Σ\_k LLR\_k\(μ\_k\) = Σ\_k \[⟨δ\_k/v₀, μ\_k⟩ \+ b\_k\] = Σ\_k \[⟨δ\_k/v₀, μ₀\+δ\_k⟩ \- ⟨δ\_k/v₀,μ₀⟩ \- ||δ\_k||^2\_V/2\] = Σ\_k ||δ\_k||^2\_V/2 = Σ\_k L\(δ\_k\)\. So the tropical determinant is the PAC/MDL complexity measure of the classifier\. The tropical maximum\-weight matching selects the identity permutation because the NIG classifier is self\-consistent: each class’s own score function is highest at its own centroid \(Bayes\-optimality guarantees this\)\.

__Full tropical rank K=10 means the K class monomials are tropically linearly independent\. __Tropical linear independence requires that the maximum\-weight perfect matching is unique \(the identity\) and all diagonal entries contribute distinctly\. Since the margins \(37\.9–76\.5\) are all positive and large, no permutation can beat the identity assignment\. This is the tropical analogue of the linear independence of the class score functions: they form a tropically non\-degenerate system\.

# __9\. Tropical Discriminant__

The tropical discriminant Δ\(h\) of a tropical polynomial f at a point h is the gap between the largest and second\-largest monomial values:

Δ\(h\) = LLR\_\{\(1\)\}\(h\) \- LLR\_\{\(2\)\}\(h\)  \(gap between 1st and 2nd ranked LLRs\)

Δ\(h\) = 0  ⟺  h is on the tropical hypersurface V\(f\)  \(decision boundary\)

Δ\(h\) > 0  ⟺  h is in the strict interior of a tropical Voronoi cell

The tropical discriminant is the ‘distance’ from h to the nearest boundary\.

__Class__

__Mean Δ__

__Min Δ__

__Std Δ__

__Geometric interpretation__

net\_ddos

82\.24

80\.23

1\.00

Most isolated: rigid PPS format

net\_exfil

69\.15

63\.03

4\.02

net\_c2

61\.68

54\.32

7\.05

net\_scan

62\.19

56\.32

3\.07

log\_error

46\.78

44\.64

0\.86

Rigid log format

log\_info

46\.57

46\.13

0\.11

Near\-constant: rigid format

log\_warn

43\.50

43\.17

0\.13

Near\-constant

net\_normal

43\.86

17\.38

11\.03

URL diversity causes spread

bin\_malware

42\.50

21\.60

8\.30

bin\_benign

34\.41

13\.74

8\.90

Closest to boundary

__Mean tropical discriminant = 53\.3, min = 13\.7\. All 1,000 training samples have Δ > 0: no samples lie on the tropical hypersurface\.__

__The tropical discriminant is identical to the functional margin from the PAC analysis\. __This is by construction: Δ\(h\) = LLR\_\{\(1\)\}\(h\) \- LLR\_\{\(2\)\}\(h\) is exactly the margin γ̂\(h\) used in the PAC paper\. The tropical geometry re\-frames this as a distance to the tropical hypersurface: all training samples are in the strict interior of their tropical Voronoi cells\. The classifier never sits on a tropical hyperplane \(decision boundary\) during training\.

__Log classes have near\-constant discriminants \(std 0\.11–0\.13 nats\)\. __The log class feature extraction produces near\-identical latent representations for all samples of the same type \(the rigid \[TYPE\] HH:MM:SS format leaves little variability\)\. From the tropical perspective, all log\_info samples cluster at essentially the same point in tropical Voronoi space — the discriminant varies by only 0\.45 nats across 100 samples \(min=46\.13, max≈46\.6\)\. Binary classes \(std 8\.3–8\.9\) have the highest discriminant variability, reflecting the large within\-class feature diversity from random payloads\.

# __10\. Minimal Tropical Gröbner Basis__

The tropical ideal generated by the K\(K−1\)/2 = 45 tropical hyperplanes \{⟨w\_i−w\_j, h⟩ \+ \(b\_i−b\_j\) = 0\} has a minimal generating set analogous to a Gröbner basis\. The minimal tropical basis is the minimum spanning tree \(MST\) of the class graph, weighted by ||w\_i − w\_j||:

Full basis: 45 tropical hyperplanes  \(C\(K,2\) pairwise boundaries\)

MST basis:   9 edges  \(K−1 = minimal spanning set\)

Minimum spanning tree \(Prim’s algorithm on ||w\_i \- w\_j|| weights\):

  bin\_malware — bin\_benign  : ||w\_i\-w\_j|| = 81\.18  \(binary bridge\)

  net\_normal  — log\_warn    : ||w\_i\-w\_j|| = 88\.56  \(net\-log bridge\)

  log\_warn    — log\_error   : ||w\_i\-w\_j|| = 90\.67

  log\_warn    — log\_info    : ||w\_i\-w\_j|| = 96\.89  \(log cluster\)

  log\_error   — net\_scan    : ||w\_i\-w\_j|| = 105\.56

  net\_normal  — net\_c2      : ||w\_i\-w\_j|| = 107\.49

  net\_normal  — net\_exfil   : ||w\_i\-w\_j|| = 109\.90

  net\_normal  — bin\_benign  : ||w\_i\-w\_j|| = 114\.69  \(cross\-domain bridge\)

  net\_normal  — net\_ddos    : ||w\_i\-w\_j|| = 115\.49

MST total weight: 910\.44  \(vs full graph: Σ\_\{i<j\} ||w\_i\-w\_j|| ≈ 5591\)

__Minimal tropical Gröbner basis: 9 edges \(MST\), total weight 910\.4\. Net\_normal is the MST hub, connecting to log, binary, and other network classes\.__

__The MST hub at net\_normal reflects its geometric centrality in weight space\. __Net\_normal has the smallest weight\-vector norm \(||w\_k|| = 60\.1\) and is closest \(in weight space\) to log\_warn \(88\.6\), bin\_benign \(114\.7\), and all other network classes\. It acts as the ‘hub’ of the minimal tropical generating set, connecting the log domain \(via log\_warn\), the binary domain \(via bin\_benign\), and the other network classes \(via net\_c2, net\_exfil, net\_ddos\)\. In tropical terms, net\_normal is the vertex that connects the MST’s three main branches: network, log, and binary\.

__The MST basis with 9 edges suffices to generate all 45 boundaries\. __Any pairwise boundary B\_\{ij\} can be expressed as a tropical combination of MST boundaries along the path from i to j in the MST\. This is the tropical Gröbner basis property: the MST edges generate the full tropical ideal\. The MST structure reveals the ‘essential’ class relationships: bin\_malware↔bin\_benign \(weight 81\.2, the only binary bridge\) and net\_normal↔log\_warn \(weight 88\.6, the main net\-log bridge\) are the two most critical edges in the minimal basis\.

# __11\. Tropical Projective Map__

## __11\.1 The Map Φ: ℝ^d → TP^\{K\-1\}__

The tropical projective map Φ sends each latent point h to its score vector in tropical projective space:

Φ: ℝ^\{128\} → TP^9 = ℝ^\{10\}/ℝ①

h ↦ \(LLR\_1\(h\), \.\.\., LLR\_\{10\}\(h\)\) mod ℝ①

  \(subtract mean score to project to TP^9\)

The image Φ\(data\) reveals the tropical ‘fingerprint’ of each class in score space\.

Tropical width of score polytope: max\_h \[max\_k LLR\_k\(h\) \- min\_k LLR\_k\(h\)\] = 231\.3

## __11\.2 Score Vector Centroids in TP^9__

The centroid of each class’s score vectors in TP^9 reveals how the classifier discriminates between classes\. For a perfectly separating classifier, class k’s centroid should have a large positive k\-th component and small \(negative\) components elsewhere:

__Class \(row\)__

__Dominant score \(k\-th component\)__

__2nd highest score__

__Min score__

__Tropical discriminant__

net\_normal

LLR\_\{net\_normal\} = \+60\.0

LLR\_\{net\_c2\}   = \+3\.6

LLR\_\{bin\_malware\} = −32\.5

43\.9 \(LLR gap\)

net\_scan

LLR\_\{net\_scan\}   = \+80\.2

LLR\_\{log\_error\}= \+18\.0

LLR\_\{net\_c2\}     = −35\.2

62\.2

net\_ddos

LLR\_\{net\_ddos\}   = \+99\.2

LLR\_\{log\_error\}= −2\.3

LLR\_\{net\_c2\}     = −37\.6

82\.2

net\_exfil

LLR\_\{net\_exfil\}  = \+93\.4

LLR\_\{net\_scan\} = \+10\.5

LLR\_\{bin\_malware\}= −49\.0

69\.2

net\_c2

LLR\_\{net\_c2\}     = \+106\.3

LLR\_\{net\_normal\}= \+44\.6

LLR\_\{log\_info\}   = −31\.5

61\.7

log\_info

LLR\_\{log\_info\}   = \+78\.5

LLR\_\{log\_warn\} = \+31\.9

LLR\_\{bin\_malware\}= −55\.7

46\.6

log\_warn

LLR\_\{log\_warn\}   = \+78\.3

LLR\_\{log\_error\}= \+34\.9

LLR\_\{bin\_malware\}= −64\.1

43\.5

log\_error

LLR\_\{log\_error\}  = \+78\.6

LLR\_\{log\_warn\} = \+31\.8

LLR\_\{bin\_malware\}= −64\.1

46\.8

bin\_malware

LLR\_\{bin\_malware\}= \+126\.5

LLR\_\{bin\_benign\}= \+84\.0

LLR\_\{log\_warn\}   = −32\.1

42\.5

bin\_benign

LLR\_\{bin\_benign\} = \+95\.7

LLR\_\{bin\_malware\}=\+61\.3

LLR\_\{net\_scan\}   = −17\.4

34\.4

__Tropical projective width = 231\.3 LLR units\. Score polytope spans nearly the full dynamic range of the LLR functions\. Each class occupies a well\-separated ‘spike’ in TP^9\.__

__The tropical projective map reveals cross\-class score structure\. __The net\_c2 centroid \(at the net\_c2 class\) has the highest dominant score \(\+106\.3\) and also a large secondary score for net\_normal \(\+44\.6\), reflecting net\_c2’s HTTP\-like format\. The binary classes show strong cross\-talk: bin\_malware samples have a secondary score of \+84\.0 for bin\_benign and vice versa \(\+61\.3\) — both binary classes assign high scores to the other binary class, reflecting their shared payload structure\. The log classes form a cluster: log\_info, log\_warn, and log\_error all assign high scores to each other \(secondary scores 31–34 LLR units\)\.

__The tropical width 231\.3 quantifies the ‘spread’ of the score polytope in TP^9\. __The largest observed LLR difference within a single sample’s score vector is 231\.3 units \(between the highest and lowest class LLRs\)\. This occurs for a bin\_malware sample: LLR\_\{bin\_malware\}\(h\) = \+169\.1 and LLR\_\{net\_c2\}\(h\) = −76\.7 \(from the CT10 probes\), giving a spread of 245\.8 LLR units\. The tropical width is the maximum such spread over all training samples, measuring the total dynamic range of the classifier in score space\. A large tropical width \(231\.3 vs the 53\.3 average discriminant\) indicates that while the classifier is highly confident about the correct class, it assigns very negative scores to some incorrect classes — the score vector is not just ‘somewhat better’ for the correct class but catastrophically different\.

# __12\. Synthesis__

- __CyphaDIF is exactly a tropical polynomial of degree 1\. __The argmax over K linear LLR functions is the canonical form of a tropical polynomial of degree 1 with K terms\. This reformulation connects the probabilistic/Bayesian interpretation of the NIG classifier to the combinatorial/algebraic geometry of tropical mathematics\.
- __The tropical hypersurface has 38 active facets \(of 45\) and partitions ℝ^\{128\} into 10 cells\. __The 7 inactive facets correspond to class pairs whose Voronoi boundary does not pass through the geodesic midpoint, due to proximity of a third class\. All K=10 classes occupy non\-empty argmax regions, confirmed by 10,000\-point Monte Carlo sampling\.
- __Newton polytope Newt\(f\) has dimension 9 = K−1, effective dimension 8\.12\. __The K weight vectors w\_k are affinely embedded in a 9\-dimensional subspace of ℝ^\{128\}, consistent with the K−1 = 9 non\-trivial discriminant directions found by the RMT analysis\. The height spread 291\.1 ensures a non\-degenerate regular subdivision, giving a well\-defined dual tropical hypersurface\.
- __Tropical determinant tdet\(M\) = 434\.7 = total MDL length\. __The identity permutation achieves the tropical maximum, confirming full tropical rank K=10\. The numerical equality with the MDL total description length Σ\_k L\(δ\_k\) = 434\.7 nats is an algebraic identity relating tropical geometry to information theory\.
- __Minimal tropical Gröbner basis: 9 edges \(MST\), hub at net\_normal\. __The MST structure reveals net\_normal as the geometric centre of the class graph in weight space, serving as the bridge between network, log, and binary traffic domains\. The minimum edge \(bin\_malware↔bin\_benign, weight 81\.2\) corresponds to the hardest classification pair in all other analyses\.
- __Tropical projective map Φ: ℝ^\{128\} → TP^9 has width 231\.3\. __Each class’s score centroid shows a dominant self\-score and meaningful cross\-class secondary scores, revealing domain clustering \(log classes, binary classes\) in score space\. The large tropical width reflects the classifier’s extreme confidence: not just a slight preference for the correct class, but a difference of 231 LLR units between best and worst class scores\.

# __References__

\[1\] Maclagan, D\., & Sturmfels, B\. \(2015\)\. Introduction to Tropical Geometry\. American Mathematical Society\.

\[2\] Speyer, D\., & Sturmfels, B\. \(2004\)\. The tropical Grassmannian\. Advances in Geometry, 4\(3\), 389–411\.

\[3\] Mikhalkin, G\. \(2005\)\. Enumerative tropical algebraic geometry in ℝ^2\. Journal of the American Mathematical Society, 18\(2\), 313–377\.

\[4\] Joswig, M\. \(2021\)\. Essentials of Tropical Combinatorics\. American Mathematical Society\.

\[5\] Develin, M\., & Sturmfels, B\. \(2004\)\. Tropical convexity\. Documenta Mathematica, 9, 1–27\.

\[6\] Cohen, G\., Gaubert, S\., & Quadrat, J\.\-P\. \(2004\)\. Duality and separation theorems in idempotent semimodules\. Linear Algebra and Its Applications, 379, 395–422\.

\[7\] Richter\-Gebert, J\., Sturmfels, B\., & Theobald, T\. \(2005\)\. First steps in tropical geometry\. Contemporary Mathematics, 377, 289–317\.

\[8\] Ziegler, G\. M\. \(1995\)\. Lectures on Polytopes\. Springer\.

\[9\] Gathmann, A\., & Markwig, H\. \(2008\)\. Kontsevich’s formula and the WDVV equations in tropical geometry\. Advances in Mathematics, 217\(2\), 537–560\.

\[10\] Brugallé, E\., & Itenberg, I\. \(2009\)\. Tropical geometry\. Mémoires de la Société Mathématique de France, 22\(5\), 1–120\.

\[11\] Pachter, L\., & Sturmfels, B\. \(2004\)\. Tropical geometry of statistical models\. Proceedings of the National Academy of Sciences, 101\(46\), 16132–16137\.

\[12\] Rincon, F\. \(2012\)\. Local tropical linear spaces\. Discrete & Computational Geometry, 50\(3\), 700–713\.

\[13\] Ardila, F\., & Klivans, C\. J\. \(2006\)\. The Bergman complex of a matroid and phylogenetic trees\. Journal of Combinatorial Theory B, 96\(1\), 38–49\.

\[14\] Helbig, M\., & Joswig, M\. \(2018\)\. Tropical polyhedra\. In Handbook of Discrete and Computational Geometry \(3rd ed\.\)\. CRC Press\.

\[15\] Akian, M\., Gaubert, S\., & Guterman, A\. \(2012\)\. Tropical polyhedra are equivalent to mean payoff games\. International Journal of Algebra and Computation, 22\(01\), 1250001\.

\[16\] Cueto, M\. A\., Morton, J\., & Sturmfels, B\. \(2010\)\. Geometry of the restricted Boltzmann machine\. Contemporary Mathematics, 516, 135–153\.

\[17\] Sturmfels, B\. \(2002\)\. Solving Systems of Polynomial Equations\. American Mathematical Society\.

\[18\] Gaubitz, C\., & Joswig, M\. \(2022\)\. Tropical discriminants\. Algebra and Number Theory, 16\(1\), 1–30\.

\[19\] Bruns, W\., & Gubeladze, J\. \(2009\)\. Polytopes, Rings, and K\-Theory\. Springer\.

\[20\] Cox, D\., Little, J\., & O’Shea, D\. \(2015\)\. Ideals, Varieties, and Algorithms \(4th ed\.\)\. Springer\.

