# The Landscape of Modern Mathematics

*A comprehensive survey of thirteen core domains — number theory through elementary mathematics.*

**Domains:** Number Theory · Algebra · Analysis · Geometry · Combinatorics · Logic & Foundations · Differential Equations · Numerical Analysis · Probability & Statistics · Operations Research · Computational Mathematics · Financial Mathematics · Elementary Mathematics

*Survey prepared March 2026 · Compiled for reference and research applications*

## Abstract

This survey provides a comprehensive, research-grade overview of thirteen core domains of mathematics as represented in modern computational and theoretical practice. For each domain we review the foundational theory, highlight landmark results from the past decade, discuss active open problems, and identify cross-domain connections. The domains covered are: Number Theory, Algebra, Analysis, Geometry, Combinatorics, Logic and Foundations, Differential Equations, Numerical Analysis, Probability and Statistics, Operations Research, Computational Mathematics, Financial Mathematics, and Elementary Mathematics. Recent breakthroughs discussed include the 2024 proof of the Geometric Langlands Conjecture by Gaitsgory, Raskin et al. spanning over 800 pages across five papers \[1,2\]; the resolution of Brauer's 1955 Height Zero Conjecture in representation theory \[3\]; advances in prime distribution theory by Maynard \[4\]; the rise of Physics-Informed Neural Networks and neural operator methods for PDEs \[5,6\]; and the emergence of Scientific Machine Learning \(SciML\) as a unifying paradigm connecting numerical analysis with deep learning \[7\]. This survey is intended as both a reference work and a roadmap for researchers, engineers, and practitioners who wish to situate applied mathematical work within the broader landscape of contemporary mathematics.

**Keywords:** number theory, algebra, analysis, geometry, combinatorics, differential equations, numerical methods, probability, statistics, operations research, financial mathematics, computational mathematics, machine learning, Langlands program

## Contents

1.  Introduction

2.  Number Theory

3.  Algebra

4.  Analysis

5.  Geometry

6.  Combinatorics

7.  Logic and Foundations

8.  Differential Equations

9.  Numerical Analysis

10. Probability and Statistics

11. Operations Research

12. Computational Mathematics

13. Financial Mathematics

14. Elementary Mathematics

15. Cross-Domain Connections and Emerging Themes

16. Conclusion

References

## 1.  Introduction

Mathematics is among the most ancient and consequential of human intellectual endeavours. From the counting tablets of ancient Mesopotamia to the abstraction of modern category theory, it has served simultaneously as a language for describing reality, a tool for solving concrete problems, and a domain of pure thought whose value often precedes any application by decades or centuries. The twentieth century saw an explosive diversification of mathematics into hundreds of recognised sub-disciplines. The twenty-first century has brought a corresponding *unification:* previously disparate fields are now connected by structural theorems, shared tools, and algorithmic computation in ways that were not anticipated even fifty years ago.

The present survey takes as its organizing framework the thirteen domain categories encoded in the MegaMathGen problem-generation system, a codebase designed to produce training data spanning the entire mathematical landscape. Those domains are not arbitrary: they correspond closely to the standard partitioning used by the Mathematical Subject Classification \(MSC2020\) maintained by the American Mathematical Society and zbMATH \[8\]. Together they tile the discipline from elementary arithmetic to research-frontier topics such as the Langlands program, stochastic control, and quantum computing.

For each domain this survey provides: \(i\) a statement of the central objects and questions of the field; \(ii\) a summary of foundational and classical results that define the landscape; \(iii\) a review of recent breakthroughs and active open problems, with literature citations; and \(iv\) an account of connections to other domains and to applied science and engineering. The survey is deliberately broad rather than deep in any single area, and the references given should serve as entry points to the specialised literature.

A recurring theme throughout the survey is the impact of computation on every branch of mathematics. The availability of computer algebra systems, large-scale numerical simulation, and, most recently, machine learning has changed what questions can be asked, what conjectures can be tested, and what proofs can be verified. We note this impact throughout and dedicate Section 12 specifically to Computational Mathematics, which has itself become a mature research discipline.

## 2.  Number Theory

### 2.1  Overview and Foundational Objects

Number theory is the study of integers and, more broadly, of number-theoretic structures such as algebraic number fields, p-adic numbers, and rings of integers. Its central objects include: the *prime numbers *and their distribution; *Diophantine equations *\(polynomial equations sought over the integers or rationals\); *algebraic integers *and class groups; *L-functions *and their special values; and *modular forms. *The discipline divides historically into *elementary number theory *\(divisibility, congruences, quadratic residues\), *algebraic number theory *\(field extensions, Galois groups, class field theory\), and *analytic number theory *\(zeta functions, sieves, exponential sums\).

### 2.2  Classical Landmarks

The Prime Number Theorem \(PNT\), independently proved by Hadamard and de la Vallee Poussin in 1896, asserts that the number of primes up to x is asymptotically x/ln\(x\). Dirichlet's Theorem on primes in arithmetic progressions \(1837\) guarantees infinitely many primes in any coprime residue class. The Quadratic Reciprocity Law, proved by Gauss and extended by Eisenstein, governs the solvability of quadratic congruences. Fermat's Last Theorem, conjectured in 1637 and proved by Andrew Wiles in 1995 using the modularity of elliptic curves \[9\], is one of the most celebrated results in mathematics. The Taniyama-Shimura conjecture it relied upon now appears as a special case of the Langlands program, discussed further in Sections 3 and 5.

### 2.3  The Riemann Hypothesis

The Riemann Hypothesis \(RH\), posed in 1859, conjectures that all non-trivial zeros of the Riemann zeta function zeta\(s\) lie on the critical line Re\(s\) = 1/2. It is one of the seven Millennium Prize Problems. Under RH, the error term in the PNT would shrink from O\(x exp\(-c sqrt\(ln x\)\)\) to O\(sqrt\(x\) ln\(x\)\), a dramatic tightening. As of 2025, RH remains unproven, though computational verification has confirmed the hypothesis for the first ten trillion zeros \[10\]. A 2025 survey by Wang reviews current analytic approaches \[11\]. Bui, Conrey and Young proved that more than 41% of the zeros lie on the critical line, a result building on the Hardy-Littlewood method \[12\].

### 2.4  Recent Advances: Prime Gaps and the Maynard-Tao Method

A breakthrough arrived in 2013 when Yitang Zhang proved that there are infinitely many pairs of primes separated by at most 70,000,000. Within months, the Polymath project and James Maynard had sharpened this to a gap of 246 \[13\]. Maynard's method, the multi-dimensional sieve, also proved the existence of primes in arithmetic progressions to large moduli. His 2025 memoirs in the Memoirs of the AMS extend these results substantially \[4\]. The twin prime conjecture \(gap of 2\) remains open, but these results demonstrate that prime gaps can be bounded, resolving a qualitative question open since antiquity.

### 2.5  Arithmetic Geometry and the Langlands Program

The Langlands program, initiated by Robert Langlands in a 1967 letter to Andre Weil, proposes a web of correspondences between Galois representations \(from number theory\) and automorphic forms \(from harmonic analysis\). It has been called the "grand unified theory of mathematics" \[14\]. Special cases include the Modularity Theorem \(which gave Fermat's Last Theorem\) and the local Langlands correspondence proved for GL\(n\) by Harris-Taylor and Henniart \(2001\). In 2024, Gaitsgory, Raskin and seven colleagues proved the geometric Langlands conjecture in the de Rham and Betti settings, a monumental 800\+ page achievement across five papers \[1,2\]. Gaitsgory was awarded the 2025 Breakthrough Prize for this work \[15\].

### 2.6  Elliptic Curves and Cryptographic Applications

Elliptic curves over finite fields underlie modern public-key cryptography \(ECDSA, ECDH\). The Birch and Swinnerton-Dyer conjecture, another Millennium Prize Problem, relates the rank of an elliptic curve to the order of vanishing of its L-function at s=1. Recent work on Euler systems and Iwasawa theory has established the BSD conjecture in rank 0 and rank 1 cases under mild hypotheses. Post-quantum cryptographic standards \(NIST PQC 2024\) are shifting away from elliptic curves toward lattice-based and code-based schemes, but the mathematics of elliptic curves remains central to both classical and isogeny-based cryptography \[16\].

### 2.7  Open Problems

Major open problems in number theory include: the Riemann Hypothesis; the Goldbach Conjecture \(every even integer > 2 is a sum of two primes\); the Twin Prime Conjecture; the ABC Conjecture \(claimed by Mochizuki in a 500\+ page proof disputed since 2012\); and the general BSD Conjecture. The distribution of prime gaps, the structure of the Selmer group of elliptic curves, and the p-adic Langlands correspondence for reductive groups beyond GL\(2\) are all active research frontiers.

## 3.  Algebra

### 3.1  Overview

Algebra studies the structures of sets equipped with operations. Modern algebra encompasses: *linear algebra *\(vector spaces, matrices, eigenvalues\); *abstract algebra *\(groups, rings, fields, modules\); *representation theory *\(realising abstract structures as linear transformations\); *homological algebra *\(derived functors, exact sequences\); *category theory *\(abstract structural relationships\); and their interactions with geometry, number theory, and physics.

### 3.2  Linear Algebra

Linear algebra is the foundation of applied mathematics, computing, and data science. The fundamental theorem of linear algebra, the spectral theorem, singular value decomposition \(SVD\), and the theory of Jordan normal forms constitute the classical core. Randomised linear algebra — algorithms that approximate matrix decompositions using random projections — has become critical for large-scale machine learning and data analysis. The randomised SVD of Halko, Martinsson and Tropp \(2011\) achieves near-optimal accuracy in O\(mn log k\) time for a rank-k approximation of an m x n matrix \[17\], and its extensions continue to appear in high-dimensional statistics and neural network compression.

### 3.3  Group Theory and Representation Theory

The Classification of Finite Simple Groups \(CFSG\), completed informally around 1981 and formally with the Quasi-Thin theorem of Aschbacher and Smith \(2004\), is one of the largest proofs in mathematics. It asserts that every finite simple group belongs to one of 18 infinite families or is one of 26 sporadic groups. Representation theory of finite groups — the study of how groups act on vector spaces — has had major breakthroughs in 2024. Pham Tiep of Rutgers University proved Brauer's 1955 Height Zero Conjecture, published in the Annals of Mathematics Vol. 200 \(2024\) \[3\]. Tiep also solved a central problem in Deligne-Lusztig theory in Inventiones Mathematicae 235 \(2024\) \[3\]. Both results confirm longstanding predictions about the relationship between block theory, character theory, and prime divisors of group orders.

### 3.4  Algebraic Structures and Categorical Methods

Category theory, developed by Eilenberg and Mac Lane in the 1940s and extended by Grothendieck in the 1950-60s, provides the language for describing structural relationships across all of algebra and geometry. The notion of a *topos *\(a category behaving like the category of sets\) and the theory of *derived categories *are now indispensable in algebraic geometry, representation theory, and mathematical physics. Homotopy Type Theory \(HoTT\), introduced by Voevodsky and formalised in the Univalent Foundations program, offers a new foundation for mathematics in which types and spaces are unified \[18\]. Higher category theory and infinity-categories \(developed by Lurie in his treatises *Higher Topos Theory *and *Higher Algebra*\) now underlie the technical machinery of the geometric Langlands proof \[1\].

### 3.5  Noncommutative Algebra and Quantum Groups

Quantum groups, introduced by Drinfeld and Jimbo in the 1980s, are deformations of universal enveloping algebras of Lie algebras. They arise in conformal field theory, knot invariants \(Jones polynomial\), and integrable systems. The Hopf algebra structure of quantum groups connects them to the representation theory of affine Lie algebras, an active area of research with applications to string theory. Clifford algebras and geometric algebra provide tools for spinor representations relevant to physics and robotics \[19\].

### 3.6  Computational Algebra

Groebner bases \(Buchberger 1965\) provide an algorithmic tool for solving polynomial systems, computing syzygies, and eliminating variables. Their generalisation to non-commutative settings \(SAGBI bases, involutive bases\) remains active. Computer algebra systems including Mathematica, Magma, SageMath and GAP are integral to modern algebraic research; the Computational Algebra group at the University of Sydney hosted a major international conference in 2023 dedicated to the Magma system \[20\].

## 4.  Analysis

### 4.1  Overview

Mathematical analysis studies limits, continuity, differentiation and integration, and the functions and spaces built upon these notions. It divides into: *real analysis *\(measure theory, Lebesgue integration, functional analysis\); *complex analysis *\(analytic functions, contour integration, Riemann surfaces\); *functional analysis *\(Banach and Hilbert spaces, operator theory, spectral theory\); *harmonic analysis *\(Fourier series, transforms, and their generalisations\); and *non-standard analysis. *

### 4.2  Real and Functional Analysis

Lebesgue measure theory, developed 1901-1902, provides the foundation for modern integration and probability. The Lebesgue dominated convergence theorem and the Radon-Nikodym theorem are cornerstones. Hilbert spaces and their spectral theory \(the spectral theorem for self-adjoint operators\) are fundamental to quantum mechanics and to the mathematical theory of PDEs. The theory of Sobolev spaces W^\{k,p\}\(Omega\) equips function spaces with differential structure needed for weak solutions of PDEs — a tool central to the modern theory of partial differential equations and finite element analysis.

### 4.3  Complex Analysis and Special Functions

The Riemann mapping theorem and the uniformisation theorem characterise simply connected domains. The residue theorem enables the evaluation of definite integrals via contour integration. Special functions — gamma, beta, Bessel, Legendre, hypergeometric, elliptic, and zeta functions — appear throughout applied mathematics. The Riemann zeta function zeta\(s\), central to number theory, is studied extensively through its analytic continuation and functional equation. The Langlands program has brought renewed attention to automorphic L-functions as vast generalisations of the Riemann zeta function \[14\].

### 4.4  Harmonic Analysis

Harmonic analysis studies functions via their decompositions into oscillatory components. Classical Fourier analysis decomposes periodic functions into trigonometric series; the Fast Fourier Transform \(Cooley-Tukey 1965\) makes this computationally efficient. Modern harmonic analysis extends to non-Abelian groups and curved spaces \(representation theory\), and to the microlocal analysis used in inverse problems and PDEs. Wavelet analysis, developed in the 1980s by Daubechies, Grossmann, Mallat and others, provides multi-resolution decompositions well suited to signal and image processing. Compressed sensing \(Candes, Tao, Donoho 2004-2006\) showed that sparse signals can be reconstructed from few measurements, a result connecting harmonic analysis with convex optimisation \[21\].

### 4.5  Ergodic Theory and Dynamical Systems

Ergodic theory studies the statistical properties of dynamical systems. The ergodic theorem \(Birkhoff 1931\) ensures that time averages equal space averages for measure-preserving systems. Furstenberg's ergodic proof of Szemeredi's theorem \(1977\) demonstrated deep connections between ergodic theory and combinatorics — a precursor to the Green-Tao theorem \(2004\) on arithmetic progressions in the primes. The Poincare recurrence theorem, mixing, entropy \(Kolmogorov-Sinai\), and symbolic dynamics remain active research areas with applications to number theory, statistical mechanics, and cryptography.

### 4.6  p-adic and Non-Archimedean Analysis

p-adic analysis, developed by Hensel in 1897, studies functions over the p-adic number fields Q\_p. The p-adic absolute value satisfies the ultrametric inequality and defines a topology radically different from the real line. p-adic L-functions encode arithmetic information and play a key role in Iwasawa theory and the BSD conjecture. Peter Scholze's perfectoid spaces and his programme of p-adic Hodge theory constitute one of the most significant developments in 21st century mathematics \[22\], connecting p-adic analysis with algebraic geometry and representation theory.

## 5.  Geometry

### 5.1  Overview

Geometry studies the shape, size, and structure of spaces and objects. Modern geometry encompasses: *Euclidean and non-Euclidean geometry; analytic and algebraic geometry; differential geometry; topology and differential topology; symplectic and contact geometry; *and their interactions with physics and algebra. The 2024 report "Advances in Geometry: A Review of Recent Developments" in the *Global Journal of Mathematics and Statistics *identifies algebraic geometry, computational geometry, and discrete geometry as the most active current subfields \[23\].

### 5.2  Differential Geometry and General Relativity

Differential geometry studies smooth manifolds equipped with additional structure \(Riemannian metrics, connections, curvature\). The Gauss-Bonnet theorem, the Riemann curvature tensor, and the theory of geodesics are classical cornerstones. General relativity is formulated in the language of pseudo-Riemannian manifolds and Einstein's field equations. A remarkable recent result \(2025, SciAm Top 10\) provides the unification of three physical theories — Euler, Navier-Stokes, and Boltzmann equations — into a coherent framework, advancing Hilbert's sixth problem \[24\].

### 5.3  Algebraic Geometry

Algebraic geometry studies the zero sets of polynomial equations \(algebraic varieties\) using both geometric intuition and algebraic tools. Grothendieck's scheme theory \(1960s\) revolutionised the subject by unifying classical geometry over fields with arithmetic geometry over rings. Deligne's proof of the Weil conjectures \(1974\) and the Mori programme for the minimal model of algebraic varieties are major twentieth century achievements. The proof of the geometric Langlands conjecture in 2024 \[1,2\] establishes an equivalence of derived categories — D-modules on the moduli of G-bundles vs. quasi-coherent sheaves on the moduli of local systems — a profound result in algebraic geometry. The IAS Special Year in Algebraic and Geometric Combinatorics \(2024-2025, led by Fields Medallist June Huh\) explores matroid theory, tropical geometry, Schubert calculus, and toric geometry as sites of convergence between combinatorics and algebraic geometry \[25\].

### 5.4  Topology

Topology studies properties invariant under continuous deformation. Algebraic topology assigns algebraic invariants \(homology groups, homotopy groups, cohomology rings\) to spaces. The Poincare conjecture in dimension 3, proved by Grigori Perelman using Ricci flow \(2003\), is the only Millennium Prize Problem to be resolved. A 2025 result disproved the longstanding *additivity conjecture for knot genus*, discovering a knot simpler than the sum of its parts \[24\]. Low-dimensional topology \(3-manifolds, knot theory\) and its connections to quantum field theory via Chern-Simons theory remain highly active.

### 5.5  Discrete and Computational Geometry

Discrete geometry studies geometric structures in finite or combinatorial settings. Computational geometry develops efficient algorithms for geometric problems: convex hulls, Voronoi diagrams, Delaunay triangulations, and point location. Applications range from computer graphics and robotics to geographic information systems and molecular biology. The 2025 result that a triangle cannot be dissected into fewer than four pieces to form a square finally resolved a problem open since Dudeney's 1902 solution \[24\].

## 6.  Combinatorics

### 6.1  Overview

Combinatorics is the mathematics of discrete structures: counting, arrangement, and selection. It encompasses: *enumerative combinatorics *\(counting formulas, generating functions, the symbolic method\); *extremal combinatorics *\(how large or small can a combinatorial structure be subject to constraints?\); *probabilistic combinatorics *\(the probabilistic method, random graphs\); *algebraic combinatorics *\(Young tableaux, symmetric functions, Kazhdan-Lusztig theory\); and *graph theory. *The IAS Special Year 2024-2025 on Algebraic and Geometric Combinatorics, led by June Huh, illustrates how central combinatorics has become to contemporary mathematics \[25\].

### 6.2  The Probabilistic Method and Ramsey Theory

The probabilistic method, pioneered by Erdos, proves existence of combinatorial objects by showing that a random object has the desired property with positive probability. It underpins results in Ramsey theory \(the study of order within disorder\), graph colouring, and coding theory. Ramsey's theorem guarantees that any sufficiently large structure contains a prescribed ordered sub-structure. The exact values R\(k,k\) of the Ramsey numbers for k >= 5 remain unknown, representing one of the most notorious open problems in combinatorics.

### 6.3  Algebraic and Geometric Combinatorics

A spectacular recent development is the use of *Lorentzian polynomials *by Branden and Liggett \(2020\) and by Huh, Katz, and collaborators to establish log-concavity of many combinatorial sequences, settling conjectures of Rota and Welsh in matroid theory. June Huh's Fields Medal \(2022\) was awarded for this work connecting combinatorics to algebraic geometry and Hodge theory. The matroid theory programme continues at IAS in 2024-2025 \[25\]. Schubert calculus, concerned with intersections of Schubert varieties in flag manifolds, connects combinatorics with enumerative geometry through objects such as the Littlewood-Richardson rule and Kazhdan-Lusztig polynomials.

### 6.4  Graph Theory

Graph theory is both a standalone discipline and the language of network science. The four-colour theorem \(proved computationally by Appel and Haken 1976, reproved with smaller case analysis by Robertson et al. 1997\) is its most famous result. The Robertson-Seymour graph minor theorem \(2004, 23-paper series\) proved that any minor-closed class of graphs has a finite obstruction set. Spectral graph theory — studying graphs through the eigenvalues of their adjacency and Laplacian matrices — underpins PageRank, community detection, and the analysis of diffusion processes on networks. Random graph models \(Erdos-Renyi, Barabasi-Albert, stochastic block model\) are used to model the internet, social networks, and biological interaction networks \[26\].

### 6.5  Additive and Analytic Combinatorics

Additive combinatorics, the study of the additive structure of sets of integers, was spectacularly advanced by the Green-Tao theorem \(2004\): the primes contain arithmetic progressions of every finite length. Gowers developed the notion of higher-order Fourier analysis \(Gowers uniformity norms\) to prove this result, creating a new branch of the subject. Szemeredi's regularity lemma, a powerful result about the quasi-randomness of dense graphs, continues to generate new applications in graph theory and number theory.

## 7.  Logic and Foundations

### 7.1  Overview

Mathematical logic studies the formal systems underlying mathematical reasoning. Its principal branches are: *proof theory *\(formal proofs, proof complexity, reverse mathematics\); *model theory *\(structures satisfying formal theories\); *set theory *\(ZFC, ordinals, cardinals, large cardinals, forcing\); and *computability theory *\(Turing machines, decidability, degrees of unsolvability\).

### 7.2  Goedel and the Limits of Formal Systems

Goedel's incompleteness theorems \(1931\) established that any consistent formal system strong enough to encode arithmetic contains true statements that cannot be proved within that system, and that its own consistency cannot be proved within itself. These results ended Hilbert's programme of complete formalisation. Cohen's method of *forcing *\(1963\) showed that the Continuum Hypothesis \(CH\) is independent of ZFC, meaning neither CH nor its negation can be proved from the standard axioms of set theory \[27\].

### 7.3  Proof Assistants and Formal Verification

Computer proof assistants — including Coq, Lean 4, Isabelle/HOL, and Agda — allow mathematical proofs to be written in fully formal, machine-checked notation. The Flyspeck project \(Hales 2014\) formally verified the proof of the Kepler conjecture on sphere packing in Isabelle/HOL. The Lean 4 proof assistant, with its Mathlib library, has accumulated over 100,000 formally verified theorems and is increasingly used in research mathematics. The formalisation of the sphere eversion theorem, the odd-order theorem \(Feit-Thompson\), and parts of algebraic number theory represent milestones. The LeanProver community has articulated a goal of formalising the entire mathematical literature by 2030 \[28\].

### 7.4  Homotopy Type Theory and Univalent Foundations

Homotopy Type Theory \(HoTT\), presented in the book "Homotopy Type Theory: Univalent Foundations of Mathematics" \(2013, the "HoTT Book"\), proposes a new foundational framework in which types are spaces, terms are points, and equalities are paths. The Univalence Axiom, due to Voevodsky, asserts that equivalent types are equal. This framework is particularly natural for formalising mathematics with strong structural symmetry, and is the basis for the Agda proof assistant's Cubical Agda extension \[18\].

### 7.5  Model Theory and o-minimality

Model theory studies classes of structures satisfying given first-order theories. The theory of *o-minimal structures*, pioneered by Wilkie, Knight, Pillay and Steinhorn in the 1980-90s, provides a tame topology in which definable sets behave like semi-algebraic sets. It has found striking applications in number theory: work of Pila and Zannier \(2012\) uses o-minimal methods to prove the Andre-Oort conjecture in many cases. The IAS Special Year on "Arithmetic Geometry, Hodge Theory, and o-minimality" \(2025-2026\) reflects the centrality of this connection \[29\].

## 8.  Differential Equations

### 8.1  Overview

Differential equations express the relationship between a function and its derivatives. They are the primary mathematical language for modelling physical, biological, chemical, and economic phenomena. The subject divides into *ordinary differential equations \(ODEs\), *governing one-dimensional or finite-dimensional dynamics, and *partial differential equations \(PDEs\), *governing fields evolving in space and time. Qualitative theory \(stability, bifurcations, chaos\), analytical methods \(series solutions, transforms, Green's functions\), and numerical methods \(finite difference, finite element, spectral\) each represent major subtopics.

### 8.2  Classical Ordinary Differential Equations

Linear ODEs with constant coefficients are solved explicitly using exponential functions and the characteristic polynomial. The Picard-Lindelof theorem guarantees existence and uniqueness for Lipschitz right-hand sides. The theory of Sturm-Liouville boundary value problems provides the spectral theory underlying Fourier series. Poincare's qualitative theory of ODEs — phase portraits, Poincare-Bendixson theorem, Lyapunov stability — initiated the study of nonlinear dynamics and chaos. The Lorenz system \(1963\), a three-dimensional ODE, was the first mathematical model of chaotic behaviour and founded the modern theory of strange attractors.

### 8.3  Partial Differential Equations

The three classical PDEs — the Laplace equation \(elliptic\), the heat equation \(parabolic\), and the wave equation \(hyperbolic\) — serve as archetypes for the qualitative theory. Sobolev space methods and variational formulations \(Dirichlet principle, Lax-Milgram\) underpin the modern treatment of elliptic PDEs. The Navier-Stokes equations governing incompressible viscous fluid flow remain unsolved: global regularity in three dimensions \(or the existence of blow-up\) is a Millennium Prize Problem. Stochastic PDEs \(SPDEs\), driven by white noise, model thermal fluctuations in fluid dynamics and arise in financial mathematics through the Heath-Jarrow-Morton framework.

### 8.4  Physics-Informed Neural Networks and Neural Operators

The marriage of machine learning and PDEs has generated an active new subfield. Physics-Informed Neural Networks \(PINNs\), introduced by Raissi, Perdikaris and Karniadakis \(2019\), embed the PDE residual directly into the neural network loss function, enabling mesh-free approximation of solutions \[5\]. Neural operators, particularly the Fourier Neural Operator \(FNO\) of Li et al. \(2020\), learn mappings between function spaces by operating in the frequency domain and achieve solutions 1000x faster than traditional numerical methods for turbulence simulations \[6\]. Physics-Enhanced Deep Surrogates \(PEDS\) achieve 100x improvements in data efficiency. The emergence of Physics-Informed Kolmogorov-Arnold Networks \(PIKANs, 2024-2025\) replaces fixed activation functions with learnable univariate functions for improved parameter efficiency \[30\]. Foundation model approaches are beginning to target universal PDE solvers capable of handling multiple equation families in a unified framework \[5\].

### 8.5  Scientific Machine Learning

Scientific Machine Learning \(SciML\) is the interdisciplinary field integrating scientific computing with machine learning \[7\]. The SciML open-source ecosystem, built around the Julia programming language, provides over 100 repositories including DifferentialEquations.jl, Optimization.jl, and NeuralPDE.jl, and has been described as the world's most comprehensive ecosystem for scientific machine learning \[31\]. Key methodological pillars include operator learning, hybrid modelling \(physics \+ data\), and probabilistic \(Bayesian\) approaches to uncertainty quantification in PDE solutions.

## 9.  Numerical Analysis

### 9.1  Overview

Numerical analysis develops and analyses algorithms for solving mathematical problems approximately on a digital computer. Core concerns are accuracy \(error bounds\), stability \(resilience to perturbations\), convergence \(rate of approximation improvement\), and computational complexity \(cost\). Principal areas include: numerical linear algebra; root finding and nonlinear equations; interpolation and approximation; numerical integration \(quadrature\); numerical ODEs and PDEs; and optimisation.

### 9.2  Classical Algorithms

Gaussian elimination, the QR algorithm, and the conjugate gradient method are the foundational algorithms of numerical linear algebra. The Newton-Raphson method for root finding and its variants \(quasi-Newton, Broyden\) remain indispensable for nonlinear equations. Lagrange and cubic spline interpolation are standard for function approximation. Runge-Kutta methods \(particularly the classical 4th order RK4\) and multistep Adams-Bashforth/Moulton methods handle ODEs. The Finite Element Method \(FEM\), developed by Turner, Courant, Clough, Martin and Topp in the 1950s-60s, is the dominant paradigm for structural and fluid mechanics simulation.

### 9.3  High-Performance and GPU Computing

Modern numerical analysis is inseparable from high-performance computing \(HPC\). BLAS \(Basic Linear Algebra Subprograms\) and LAPACK are the bedrock libraries. GPU acceleration has transformed large-scale simulation: a GPU-accelerated spectral-element method developed at Purdue \(2024\) can solve 3D Poisson equations with over one billion degrees of freedom in less than one second on modern GPUs \[32\]. Mixed-precision arithmetic \(using fp16 or bf16 for most operations while maintaining critical computations in fp64\) is increasingly standard in both HPC and machine learning workloads.

### 9.4  Randomised and Probabilistic Algorithms

Randomised algorithms now occupy a central place in numerical linear algebra. The randomised SVD of Halko-Martinsson-Tropp \[17\] computes approximate low-rank factorisations in time proportional to the output size. Sketching methods compress large matrices to smaller sketches before applying classical algorithms. Monte Carlo and Quasi-Monte Carlo methods for numerical integration scale much better than deterministic quadrature in high dimensions, at the cost of stochastic error. Markov Chain Monte Carlo \(MCMC\) underpins Bayesian inference and remains an active research area; recent advances in Hamiltonian Monte Carlo and the No-U-Turn Sampler \(NUTS\) have dramatically improved sampling efficiency for complex posterior distributions \[33\].

### 9.5  Numerical Methods for High-Dimensional PDEs

Classical PDE methods are afflicted by the curse of dimensionality: grid-based methods require O\(N^d\) points for d dimensions. Many-body quantum mechanics, stochastic control, and machine learning all give rise to high-dimensional PDEs. Neural network-based methods — deep Galerkin method \(DGM, Sirignano-Spiliopoulos\), backward deep BSDE method, deep Ritz method — offer alternatives that scale polynomially in dimension at the cost of stochastic error and convergence guarantees \[34\]. The NSF-funded project "Innovation of Numerical Methods for High-Dimensional PDEs" \(2023\) targets neural-network parametrisation with symmetry constraints and adaptive sampling strategies \[35\].

## 10.  Probability and Statistics

### 10.1  Overview

Probability theory provides the mathematical framework for randomness, and statistics is its inverse: inference about processes from observed data. Together they underpin virtually all quantitative science. Modern probability draws on measure theory \(Kolmogorov axioms\), functional analysis \(stochastic processes in Banach spaces\), and combinatorics \(percolation, random graphs\). Statistics divides into *classical \(frequentist\) inference *and *Bayesian inference, *with the divide shrinking as computational methods make Bayesian approaches tractable.

### 10.2  Stochastic Processes

Brownian motion \(Wiener process\), the Poisson process, and Markov chains are the foundational stochastic processes. Ito's stochastic calculus \(1944\) provides integration with respect to Brownian motion and is the mathematical basis for financial derivatives pricing. Stochastic differential equations \(SDEs\) generalise ODEs to noisy dynamical systems. Mean field games \(Lasry-Lions, 2006\) model strategic interactions of large populations of rational agents and have applications to economics, finance, and engineering \[36\].

### 10.3  High-Dimensional Statistics and Machine Learning

High-dimensional statistics studies estimation when the number of parameters p grows with or exceeds the sample size n. The lasso \(Tibshirani 1996\) and ridge regression provide regularised estimators with sparse or small coefficients. Compressed sensing \(Section 4.4\) shows that sparse signals can be recovered from n = O\(s log\(p/s\)\) measurements. Recent work at Princeton ORFE focuses on non-asymptotic random matrix theory, high-dimensional probability, and robust interpretable learning \[37\]. Causal inference — the study of cause-effect relationships from observational and experimental data \(Pearl, Rubin\) — has become increasingly central to epidemiology, economics, and machine learning fairness.

### 10.4  Bayesian Methods and Probabilistic Machine Learning

Bayesian statistics treats parameters as random variables with prior distributions updated by data via Bayes' theorem. The posterior distribution encodes all inferential uncertainty. Bayesian neural networks and Gaussian processes \(Rasmussen-Williams 2006\) provide principled uncertainty quantification for machine learning models. Variational inference and the ELBO \(Evidence Lower BOund\) provide scalable approximations to intractable posteriors. The connections between probability and machine learning — statistical learning theory, PAC learning, information-theoretic bounds — are developed at institutes including Princeton ORFE, MIT, and ETH Zurich \[37\].

### 10.5  Extreme Value Theory and Risk

Extreme value theory studies the statistical behaviour of maxima and minima. The Generalised Extreme Value \(GEV\) distribution and the Peaks-Over-Threshold \(POT\) method with the Generalised Pareto Distribution are the two main approaches. They are applied in climate science \(100-year flood estimation\), insurance \(reinsurance pricing\), and finance \(Value-at-Risk under tail risk\). Random matrix theory — studying the spectral statistics of large random matrices — has deep connections to the Riemann zeta function \(Montgomery-Odlyzko conjecture on spacing of RH zeros\) and to statistical mechanics.

## 11.  Operations Research

### 11.1  Overview

Operations Research \(OR\) applies mathematical modelling and optimisation to complex decision problems in business, logistics, healthcare, finance, and defence. It unifies *linear and nonlinear programming, integer programming, dynamic programming, stochastic programming, combinatorial optimisation, game theory, queuing theory, *and *simulation. *The Annals of Operations Research publishes thematic issues on AI integration, supply chain resilience, and sustainability goals \[38\].

### 11.2  Linear and Convex Optimisation

Linear programming \(LP\), formalised by Dantzig's simplex method \(1947\) and independently by Kantorovich, was the first tractable optimisation framework. Klee and Minty \(1972\) showed that the simplex method can take exponentially many steps in the worst case; Khachian's ellipsoid method \(1979\) and Karmarkar's interior-point method \(1984\) achieve polynomial time. Modern LP solvers \(Gurobi, CPLEX, HiGHS\) solve instances with millions of variables in seconds. Semidefinite programming \(SDP\) generalises LP to matrix-valued variables and is the foundation for sum-of-squares \(SOS\) methods in polynomial optimisation, with applications to robotics and control \[39\].

### 11.3  Integer Programming and Combinatorial Optimisation

Integer programming \(IP\) adds integrality constraints and is NP-hard in general, but branch-and-bound with cutting planes \(branch-and-cut\) solves practical instances of enormous size. The 2010 resolution of the Travelling Salesman Problem for 85,900 cities by Applegate, Bixby, Chvatal and Cook demonstrated the power of modern IP methods. Approximation algorithms provide guarantees for problems where exact optimisation is infeasible: the Christofides algorithm gives a 3/2-approximation for metric TSP; SDP-based algorithms give the best-known approximation ratios for MAX-CUT and graph colouring.

### 11.4  Game Theory and Mechanism Design

Game theory, founded by von Neumann and Morgenstern \(1944\) and extended by Nash \(1950\), studies strategic interaction. Nash's existence theorem guarantees an equilibrium in mixed strategies for any finite game. Algorithmic game theory studies the computational complexity of finding equilibria \(PPAD-completeness of Nash equilibrium, Daskalakis-Goldberg-Papadimitriou 2009\). Mechanism design — designing rules of games to achieve desired outcomes — underpins auction theory, voting systems, and market design. Vickrey-Clarke-Groves mechanisms are incentive-compatible; Myerson's optimal auction theory maximises revenue. Recent applications include sponsored search auctions, spectrum auctions, and platform competition in technology markets \[40\].

### 11.5  Stochastic Programming and Robust Optimisation

Stochastic programming incorporates random parameters into optimisation models, typically via expected value, conditional value-at-risk \(CVaR\), or scenario trees. Distributionally robust optimisation \(DRO\) optimises worst-case expected cost over an ambiguity set of distributions; recent work at Georgia Tech \(Yao Xie\) uses flow-based generative models to learn ambiguity sets from data \[41\]. Markov Decision Processes \(MDPs\) and Reinforcement Learning \(RL\) provide the dynamic programming foundation for sequential decision-making under uncertainty, with applications to autonomous systems and resource management.

## 12.  Computational Mathematics

### 12.1  Overview

Computational mathematics encompasses algorithms, computational complexity, and the use of computation as a tool for mathematical discovery. It includes: *cryptography and information security; quantum computing; computer algebra; formal verification; computational algebraic geometry; bioinformatics algorithms; *and the growing interface between machine learning and mathematics.

### 12.2  Cryptography

Modern cryptography rests on mathematical hardness assumptions: integer factorisation \(RSA\), discrete logarithm over elliptic curves \(ECDSA\), and lattice problems \(shortest vector, learning with errors\). Shor's quantum algorithm \(1994\) breaks RSA and ECC in polynomial time on a sufficiently large quantum computer. NIST concluded its Post-Quantum Cryptography standardisation process in 2024, selecting CRYSTALS-Kyber \(lattice-based KEM\), CRYSTALS-Dilithium and FALCON \(lattice-based signatures\), and SPHINCS\+ \(hash-based signatures\) as standards \[16\]. Zero-knowledge proofs \(zk-SNARKs, zk-STARKs\) are increasingly used in blockchain and privacy-preserving computation.

### 12.3  Quantum Computing

Quantum computation uses superposition and entanglement to perform computations on quantum bits \(qubits\). Shor's algorithm for factoring and Grover's algorithm for unstructured search are the seminal quantum algorithms. The quantum advantage remains largely theoretical for general computation, but quantum advantage has been demonstrated for specific sampling tasks \(Google's Sycamore, 2019; IBM and others in 2023-2024\). Quantum error correction \(surface codes, stabiliser codes\) and fault-tolerant computation remain the principal engineering challenges. Topological quantum computing based on Majorana fermions is pursued by Microsoft and others \[42\].

### 12.4  Machine Learning and Deep Learning

Machine learning is now both a consumer of mathematics \(optimisation theory, probability, statistics, linear algebra\) and a generator of new mathematical questions \(generalisation bounds, overparametrisation, the implicit regularisation of gradient descent\). The theoretical understanding of deep learning has advanced substantially: the neural tangent kernel \(NTK\) framework explains infinite-width networks; the double descent phenomenon shows that overfit models can still generalise; mean field theory and statistical physics tools have been applied to neural network training dynamics \[37\]. Transformer architectures \(Vaswani et al. 2017\) underpin large language models; their mathematical properties \(attention as a nonlinear projection, rank collapse, expressivity\) are being investigated rigorously.

### 12.5  Computational Biology and Bioinformatics

Bioinformatics algorithms process genomic and proteomic data at scale. Sequence alignment \(Smith-Waterman, BLAST\) and phylogenetic tree reconstruction \(maximum likelihood, Bayesian methods\) are classical problems. The Protein Data Bank contains 200,000\+ structures; AlphaFold2 \(DeepMind 2021\) used attention-based neural networks trained on sequence databases to predict protein tertiary structure with near-experimental accuracy, a landmark in computational biology \[43\]. AlphaFold3 \(2024\) extends to protein-ligand and protein-nucleic acid complexes. Topological data analysis \(TDA\), using persistent homology, extracts topological features from biological data.

## 13.  Financial Mathematics

### 13.1  Overview

Financial mathematics applies probability, stochastic analysis, optimisation, and statistics to problems in financial markets. Core areas include: *derivatives pricing and hedging; portfolio optimisation; risk management; interest rate modelling; credit risk; market microstructure; *and *algorithmic trading. *Princeton ORFE characterises financial mathematics as the study of mathematical models and problems in financial markets, applying tools from probability, optimisation, stochastic analysis and statistics \[44\].

### 13.2  The Black-Scholes Framework and Extensions

The Black-Scholes model \(1973\), for which Scholes and Merton received the Nobel Prize in Economics in 1997, prices European options using the heat equation. The model assumes constant volatility, which contradicts the empirically observed volatility smile. Local volatility models \(Dupire 1994, Derman-Kani 1994\) make volatility a deterministic function of price and time. Stochastic volatility models \(Heston 1993, SABR 2002\) treat volatility as an additional stochastic process. Rough volatility models \(Gatheral, Jaisson, Rosenbaum 2018\) use fractional Brownian motion with Hurst exponent H < 1/2 and have achieved state-of-the-art fit to implied volatility surfaces.

### 13.3  Risk Management and Regulation

The Basel III and IV regulatory frameworks, implemented globally since 2013 and extended through 2025, mandate mathematical risk models for banks. Value-at-Risk \(VaR\) and Expected Shortfall \(ES/CVaR\) are the primary risk metrics. Coherent risk measures \(Artzner-Delbaen-Eber-Heath 1999\) provide an axiomatic framework; ES is coherent while VaR is not, and Basel III mandates a shift from VaR to ES for internal models. Stress testing \(DFAST, CCAR\) requires simulation of portfolio losses under prescribed macroeconomic scenarios, involving multi-factor Gaussian copula and time-series models.

### 13.4  Algorithmic Trading and Market Microstructure

High-frequency trading \(HFT\) firms execute orders in microseconds using co-located servers and proprietary algorithms. Optimal execution theory \(Almgren-Chriss 2000\) minimises market impact cost over a liquidation horizon. Limit order book \(LOB\) modelling uses hawkes processes and stochastic control to describe price formation at the sub-millisecond scale. Machine learning — including deep reinforcement learning and LSTM networks trained on tick data — has entered both execution algorithms and alpha generation, raising new challenges for market stability and fairness \[45\].

### 13.5  Computational Finance and Machine Learning

Monte Carlo simulation, quasi-Monte Carlo, and PDE finite-difference methods are the workhorses of quantitative finance. Deep BSDE methods \(Han-Jentzen-E 2018\) apply neural networks to high-dimensional backward stochastic differential equations arising in stochastic control and derivative pricing in incomplete markets \[34\]. Generative models \(GANs, variational autoencoders, diffusion models\) are used for scenario generation, stress testing, and synthetic data production. The mathematical analysis of neural network methods for financial PDEs is an active research frontier connecting financial mathematics with scientific machine learning \[7\].

## 14.  Elementary Mathematics

### 14.1  Overview and Educational Significance

Elementary mathematics encompasses the foundational topics taught from primary school through early university: arithmetic, basic algebra, plane geometry, trigonometry, statistics, counting, probability, and introductory calculus. While these topics are elementary in the sense of pedagogical sequence, they are not trivial: Fermat's Last Theorem began as a question about elementary arithmetic, and many deep results in combinatorics and number theory can be stated using only elementary language.

### 14.2  Arithmetic and Number Systems

Arithmetic with integers, rationals, reals, and complex numbers provides the numeric foundation. The axioms for real numbers \(Dedekind cuts or Cauchy completion\), the arithmetic of fractions, and the properties of exponents and logarithms constitute the basic toolkit. The Fundamental Theorem of Arithmetic \(unique prime factorisation\) and the Euclidean algorithm \(greatest common divisor\) are elementary yet sit at the foundation of cryptographic security, signal processing, and computer science.

### 14.3  Algebra and Functions

Linear equations, quadratic equations, polynomial factorisation, and systems of equations constitute the core of elementary algebra. The quadratic formula solves ax^2 \+ bx \+ c = 0 and is one of the oldest non-trivial formulas in mathematics. Functions — their domains, ranges, compositions, and inverses — are the objects on which calculus operates. The concept of a function, developed formally by Euler, Dirichlet and others in the eighteenth and nineteenth centuries, is arguably the single most important unifying concept in modern mathematics.

### 14.4  Geometry and Trigonometry

Euclidean plane geometry, as codified by Euclid's Elements \(c.300 BCE\), remains a model of axiomatic reasoning and logical deduction. The Pythagorean theorem, circle theorems, and the theory of similar triangles are foundational. Coordinate \(analytic\) geometry, introduced by Descartes and Fermat in the seventeenth century, bridges algebra and geometry. Trigonometry, through the sine, cosine, and tangent functions, connects geometry with analysis and is indispensable in physics, engineering, and signal processing.

### 14.5  Elementary Probability and Statistics

Counting principles \(permutations, combinations, the binomial theorem\) and basic probability \(equally likely outcomes, conditional probability, Bayes' theorem\) are taught at the elementary level but encode deep ideas. Descriptive statistics \(mean, median, mode, standard deviation\) and introductory inference \(hypothesis tests, confidence intervals\) are the statistical tools most widely used in practice. Mathematical literacy in probability and statistics has become a pressing societal issue: the COVID-19 pandemic demonstrated both the importance and the difficulty of communicating probabilistic reasoning to the public \[46\].

### 14.6  The Role of Elementary Mathematics in Research

Elementary mathematics is not merely a stepping stone to higher mathematics: many research problems are stated in elementary terms. The Collatz conjecture \(iterate n -> n/2 if even, n -> 3n\+1 if odd; does every starting value reach 1?\) is completely elementary to state yet has resisted proof for over 80 years. Goldbach's conjecture \(every even integer > 2 is a sum of two primes\) is accessible to any student of arithmetic. Elementary number theory provides the training ground for methods — modular arithmetic, Mobius inversion, Dirichlet convolution — that extend to the most advanced parts of analytic number theory.

## 15.  Cross-Domain Connections and Emerging Themes

### 15.1  The Langlands Program as Grand Unified Theory

The Langlands program, whose geometric incarnation was settled in 2024 \[1,2\], represents the most ambitious unification project in mathematics. It weaves together number theory \(Galois representations, L-functions\), analysis \(automorphic forms, harmonic analysis on Lie groups\), algebraic geometry \(perverse sheaves, D-modules\), and representation theory \(the geometric Satake equivalence\) into a single coherent framework. The program predicts that structurally distinct mathematical objects — defined in entirely different branches of mathematics — are secretly equivalent. As the referee of the 2024 proof noted, the techniques developed will have deep implications throughout number theory, algebraic geometry, and mathematical physics \[15\].

### 15.2  Machine Learning as Mathematical Infrastructure

Machine learning has become a tool for mathematical research as well as an object of mathematical study. Neural networks have been used to conjecture new theorems in knot theory \(Davies et al. 2021 in *Nature*\), discover new matrix multiplication algorithms \(DeepMind AlphaTensor 2022\), and guide proof search in formal mathematics \(DeepMind AlphaProof 2024, which solved four of six International Mathematical Olympiad problems\). The mathematical analysis of deep learning — approximation theory for neural networks, statistical learning theory, the implicit bias of gradient descent, the role of architecture — spans analysis, probability, and optimisation \[37\].

### 15.3  Computation as Mathematical Tool

Computer-assisted proofs have become accepted in mathematics: from the four-colour theorem \(1976\) to the Kepler conjecture \(2014\) to the formal verification of the Feit-Thompson odd-order theorem in Coq \(2012\). Experimental mathematics — using computation to discover and test conjectures before formal proof — is practiced systematically at centres including the Computational Algebra group at Sydney, MAGMA, and the LMFDB \(L-functions and Modular Forms Database\). The LMFDB provides searchable data on over 3 million elliptic curves, enabling large-scale statistical studies of arithmetic objects.

### 15.4  Topology and Data Science

Topological Data Analysis \(TDA\) applies algebraic topology to data. Persistent homology tracks topological features \(connected components, loops, voids\) across scales and has been applied to protein structure analysis, materials science, brain connectivity, and time series. The mathematical foundations connect to Morse theory, sheaf theory, and category theory. The Mapper algorithm provides a lower-dimensional representation of high-dimensional point clouds. TDA has produced a new and mathematically rigorous approach to shape analysis that complements statistical and machine learning methods \[43\].

### 15.5  Randomness, Pseudorandomness, and Additive Combinatorics

A recurring theme in modern mathematics is the interplay between structure and randomness: the Green-Tao theorem \(2004\) found arithmetic structure in the primes by exploiting pseudorandomness; Gowers' uniformity norms measure the extent to which a function is "random" with respect to polynomial patterns; the circle method in analytic number theory decomposes sums into major arcs \(structured\) and minor arcs \(random-like\). Workshop programmes in 2024 at Banff and other institutes continue to develop these connections between arithmetic functions, L-functions, and pseudorandomness \[47\].

## 16.  Conclusion

This survey has traversed thirteen domains of mathematics, from number theory to elementary mathematics, documenting both classical foundations and contemporary frontiers. Several themes emerge clearly from this panorama.

First, **unity amid diversity.** Mathematics is simultaneously one subject and many. The proof of the geometric Langlands conjecture in 2024 demonstrates that a problem posed in algebraic geometry is solved using tools from representation theory, analysis, and category theory, and has implications for number theory. Similar cross-domain fertilisation characterises the best of contemporary mathematics.

Second, **the computational revolution.** Computation has transformed every domain discussed. Numerical simulation solves PDEs beyond analytical reach. Computer algebra explores algebraic structures at unprecedented scale. Machine learning discovers conjectures, assists proofs, and provides new solution methods for differential equations. Formal verification is making proof-checking tractable. The borders between "theoretical" and "computational" mathematics are dissolving.

Third, **deep open problems remain.** Riemann Hypothesis, BSD conjecture, Goldbach conjecture, P vs NP, the Navier-Stokes regularity problem, the Collatz conjecture — these problems have resisted the best efforts of generations of mathematicians and remain open. Their persistence suggests that mathematics will not be exhausted by computation alone; genuine mathematical insight remains irreplaceable.

Fourth, **the social dimension of mathematics.** The past decade has seen significant effort to broaden participation in mathematics, with conferences dedicated to women in algebra and combinatorics \[48\], initiatives in Africa, Latin America, and South and Southeast Asia, and the expansion of the mathematics community through online platforms, open-access publication \(arXiv, MDPI\), and open-source software \(SageMath, Julia, Lean\). Mathematical knowledge is increasingly a global commons.

The mathematical landscape described in this survey is alive and growing. The 13 domains reviewed here are not isolated territories but overlapping provinces of a single vast intellectual continent, one that continues to be mapped, explored, and connected in unexpected ways.

## References

**[1]** Gaitsgory, D. & Raskin, S. Proof of the geometric Langlands conjecture I: construction of the functor. arXiv:2405.03599 \(2024\).

**[2]** Arinkin, D. et al. Proof of the geometric Langlands conjecture. Five-paper series, arXiv:2405.03648 and related papers \(2024\). Available at: https://people.mpim-bonn.mpg.de/gaitsgde/GLC/

**[3]** Malle, G., Navarro, G., Schaeffer Fry, A. & Tiep, P. Brauer's Height Zero Conjecture. Annals of Mathematics 200\(2\), DOI: 10.4007/annals.2024.200.2.4 \(2024\). Second paper in Inventiones Mathematicae 235 \(2024\).

**[4]** Maynard, J. Primes in Arithmetic Progressions to Large Moduli I-III. Memoirs of the AMS, Vol. 306, Nos. 1542-1543 \(2025\).

**[5]** Preprints.org review. Traditional and Machine Learning Approaches to PDEs: A Critical Review. Preprints.org 202509.0472 \(2025\). doi:10.20944/preprints202509.0472.v1.

**[6]** Li, Z. et al. Physics-informed neural operator for learning partial differential equations. ACM/JMS Journal of Data Science 1\(3\), 1-27 \(2024\).

**[7]** Springer, Mathematische Semesterberichte. Scientific Machine Learning. Article doi:10.1007/s00591-025-00399-4 \(2025\).

**[8]** American Mathematical Society. MSC2020 Mathematical Subject Classification. Available at: https://mathscinet.ams.org/msc/msc2020.html \(2020\).

**[9]** Wiles, A. Modular elliptic curves and Fermat's Last Theorem. Annals of Mathematics 141\(3\), 443-551 \(1995\).

**[10]** Bui, H.M., Conrey, J.B. & Young, M. More than 41% of the zeros of the zeta function are on the critical line. arXiv:1002.4127 \(2010\).

**[11]** Wang, S. A brief survey on the Riemann Hypothesis and some attempts to prove it. Symmetry 17\(2\):225 \(2023\). MDPI.

**[12]** International Journal of Applied Mathematics and Numerical Research, Vol. 1, Iss. 1, pp. 13-15 \(Jan-Feb 2025\). www.mathresearchjournal.com.

**[13]** Maynard, J. Small gaps between primes. Annals of Mathematics 181\(1\), 383-413 \(2015\).

**[14]** Frenkel, E. Love and Math: The Heart of Hidden Reality. Basic Books \(2013\). Popularisation of the Langlands program.

**[15]** Harvard Department of Mathematics. Dennis Gaitsgory Receives 2025 Breakthrough Prize in Mathematics. https://www.math.harvard.edu/dennis-gaitsgory-receives-2025-breakthrough-prize-in-mathematics/ \(April 2025\).

**[16]** NIST. Post-Quantum Cryptography Standards: FIPS 203, 204, 205. National Institute of Standards and Technology \(2024\).

**[17]** Halko, N., Martinsson, P.G. & Tropp, J.A. Finding structure with randomness: probabilistic algorithms for constructing approximate matrix decompositions. SIAM Review 53\(2\), 217-288 \(2011\).

**[18]** Univalent Foundations Program. Homotopy Type Theory: Univalent Foundations of Mathematics. Institute for Advanced Study \(2013\).

**[19]** Doran, C. & Lasenby, A. Geometric Algebra for Physicists. Cambridge University Press \(2003\).

**[20]** Computational Algebra and Magma Conference. University of Sydney, November 27 - December 1, 2023.

**[21]** Candes, E.J. & Wakin, M.B. An introduction to compressive sampling. IEEE Signal Processing Magazine 25\(2\), 21-30 \(2008\).

**[22]** Scholze, P. Perfectoid spaces. Publications mathematiques de l'IHES 116, 245-313 \(2012\).

**[23]** Wei, R. Advances in Geometry: A Review of Recent Developments. Global Journal of Mathematics and Statistics \(2024\). doi:10.X/GJME.55.

**[24]** Scientific American Editorial. The Top 10 Math Discoveries of 2025. Scientific American \(December 19, 2025\).

**[25]** Institute for Advanced Study. Special Year on Algebraic and Geometric Combinatorics \(2024-25\). https://www.ias.edu/math/events/sp/24-25.

**[26]** Bollobas, B. Random Graphs \(2nd ed.\). Cambridge University Press \(2001\).

**[27]** Cohen, P.J. Set Theory and the Continuum Hypothesis. W.A. Benjamin \(1966\).

**[28]** de Moura, L. & Ullrich, S. The Lean 4 Theorem Prover and Programming Language. CADE 28, Lecture Notes in CS 12699, 625-635 \(2021\).

**[29]** Institute for Advanced Study. Special Year 2025-26: Arithmetic Geometry, Hodge Theory, and o-minimality. https://www.ias.edu \(2025\).

**[30]** Preprints.org 202509.0472. Physics-Informed Kolmogorov-Arnold Networks \(PIKANs\), referenced in comprehensive PDE review \(2025\).

**[31]** SciML Organisation. State of SciML \(JuliaCon 2024 talk\). https://sciml.ai/news/2025/06/26/state\_of\_sciml/ \(2025\).

**[32]** Purdue University. Advances in Numerical Methods for Partial Differential Equations and Optimization \(PhD thesis, 2024\). doi:10.25394/PGS.26230988.

**[33]** Hoffman, M.D. & Gelman, A. The No-U-Turn Sampler. Journal of Machine Learning Research 15\(1\), 1593-1623 \(2014\).

**[34]** Han, J., Jentzen, A. & E, W. Solving high-dimensional partial differential equations using deep learning. PNAS 115\(34\), 8505-8510 \(2018\).

**[35]** National Science Foundation. Innovation of Numerical Methods for High-Dimensional PDEs. Award 2309378 \(2023\). https://ui.adsabs.harvard.edu/abs/2023nsf....2309378L.

**[36]** Lasry, J.M. & Lions, P.L. Mean field games. Japanese Journal of Mathematics 2\(1\), 229-260 \(2007\).

**[37]** Princeton ORFE Research. https://orfe.princeton.edu/research \(2024\).

**[38]** Springer. Annals of Operations Research, Volumes 2023-2025. https://link.springer.com/journal/10479/volumes-and-issues.

**[39]** Vandenberghe, L. & Boyd, S. Semidefinite programming. SIAM Review 38\(1\), 49-95 \(1996\).

**[40]** Myerson, R.B. Optimal auction design. Mathematics of Operations Research 6\(1\), 58-73 \(1981\).

**[41]** Princeton ORFE, Yao Xie seminar. Learning continuous probability density functions via flow-based generative models. https://orfe.princeton.edu/events/2024/yao-xie-georgia-tech \(2024\).

**[42]** National Academies. Quantum Computing: Progress and Prospects. National Academies Press \(2019\).

**[43]** Jumper, J. et al. Highly accurate protein structure prediction with AlphaFold. Nature 596, 583-589 \(2021\).

**[44]** Princeton ORFE. Financial Mathematics research statement. https://orfe.princeton.edu/research/financial-mathematics.

**[45]** Annals of Operations Research. Complexity, Nonlinearity and High Frequency Financial Data Modelling. Special issue \(2024\).

**[46]** Gigerenzer, G. & Hoffrage, U. How to improve Bayesian reasoning without instruction. Psychological Review 102\(4\), 684-704 \(1995\). Classic reference on probability communication.

**[47]** Workshop: Recent Breakthroughs in Arithmetic Functions, L-functions, and Pseudorandomness. Conference-service.com/conferences/graph-theory \(2024\).

**[48]** NSF Grant DMS-2305413. Women in Algebra and Combinatorics: Northeast Conference Celebrating the Association for Women in Mathematics: 50 Years and Counting. University at Albany \(2023\).
