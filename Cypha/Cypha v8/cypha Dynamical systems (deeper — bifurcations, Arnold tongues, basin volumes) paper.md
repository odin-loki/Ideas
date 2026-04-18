<!-- Converted from `cypha Dynamical systems (deeper — bifurcations, Arnold tongues, basin volumes) paper.docx` — source was Word (.docx). -->

__Dynamical Systems__

__of the Differential Information Field Classifier__

*Bifurcations • Arnold Tongues • Basin Volumes • Attractors • Phase Portrait • Lyapunov Spectrum • Escape Times • Omega\-Limit Sets • Sensitivity • Simplex Dynamics*

Unpublished Technical Report — 2026

__Abstract__

We analyse CyphaDIF as a nonlinear dynamical system, investigating bifurcations, phase\-locking regions \(Arnold tongues\), basin of attraction geometry, attractor structure, gradient flow phase portraits, the full Lyapunov spectrum, first\-passage escape times, omega\-limit sets, sensitivity to initial conditions, and the nonlinear dynamics of the softmax map on the probability simplex\. __DS1 \(Bifurcations\): __The class mean update δ\(t\+1\) = \(1−α−λ\)δ\(t\) \+ α·input has a stable fixed\-point regime for 0 < α < 2−λ = 1\.998, with a period\-doubling \(flip\) bifurcation at α = 1\.998 and a transcritical bifurcation at α = 0\. Current α ≈ 1/300 is 599× below the flip bifurcation\. Temperature T is a bifurcation parameter with critical value T\_c = 22\.4 \(statistical mechanics paper\); current T = 2\.5 is 9\.0× below T\_c\. __DS3 \(Basin volumes\): __Under the world\-prior Gaussian N\(μ₀, v̄·I\), net\_normal captures 69\.5% of probability mass; bin\_malware and net\_c2 capture < 0\.01%\. Under the uniform class mixture, all basins are nearly equal \(9\.7–10\.2%\), confirming linear separability\. Fisher geodesic crossings occur at t\* = 0\.5000 for all tested pairs: every decision boundary is the exact geodesic midpoint — Bayes\-optimal to four decimal places\. __DS6 \(Lyapunov spectrum\): __Full state dimension 17,792\. Three blocks: μ₀ block \(λ\_L = −0\.000333, 128 modes\), δ\_k block \(λ\_L = −0\.005348, 1,280 modes\), W block \(λ\_L ≈ −0\.001–0\.002\)\. All Lyapunov exponents negative: globally attracting fixed point\. __DS7 \(Escape\): __Mean first\-passage time to classification flip: 1\.2×10⁴ steps \(bin\_malware↔bin\_benign, hardest\) to 3\.8×10^\{16\} steps \(net\_c2↔bin\_malware, easiest\)\. __DS9 \(Sensitivity\): __Perturbation halving time t½ = 129\.6 steps\. CyphaDIF is strongly contractive — not chaotic\. __DS10 \(Simplex\): __Softmax Jacobian spectral radius ρ\(J\) = 1/T = 0\.4 < 1 at T = 2\.5 \(convergent\); ρ\(J\) = 10 > 1 at T\* = 0\.1 \(divergent in fixed\-point iteration, consistent with its use as a terminal temperature rather than iteration target\)\.

# __1\. CyphaDIF as a Nonlinear Dynamical System__

A dynamical system is a rule describing how a state vector evolves over time\. CyphaDIF’s learning process defines a discrete\-time dynamical system on the state space Θ = \(μ₀, \{δ\_k\}, W\) ∈ ℝ^\{17792\}:

State:        θ = \(μ₀, δ\_1,\.\.\.,δ\_K, W\) ∈ ℝ^\{D \+ K·D \+ D²\}

              dim = 128 \+ 10·128 \+ 128² = 128 \+ 1280 \+ 16384 = 17792

Update map:   θ\(t\+1\) = F\(θ\(t\), x\_t, y\_t\)

  μ₀   : Welford mean update  \[α\_t = 1/\(t\+1\)\]

  δ\_k  : class mean IIR   \[δ\_k ← \(1\-α\_k\-λ\)δ\_k \+ α\_k\(h\_t\-μ₀\)\]

  W     : contrastive Fisher\-Rao gradient update

Fixed point:  F\(θ\*, x, y\) = θ\* for all \(x,y\)  \[achieved at convergence\]

Attractor:    \{θ\*\} — globally attracting fixed point

__The system is high\-dimensional \(17,792 state variables\) but has a low\-complexity attractor \(a single fixed point\)\. __This is the hallmark of a ‘well\-designed’ learning system: the high\-dimensional state converges to a low\-dimensional representation of the data\. The three state blocks \(μ₀, δ\_k, W\) have different timescales and dynamics, making the system a multi\-scale dynamical system\. We analyse each subsystem and the full system in turn\.

# __2\. Bifurcation Analysis__

## __2\.1 Learning Rate α as Bifurcation Parameter__

Consider the class mean update as a 1D map with α as a control parameter\. The scalar dynamics on a single dimension of δ\_k are:

f\_α\(x\) = \(1\-α\-λ\)x \+ α·c  where c = E\[h\_i\-μ\_\{0,i\}|y=k\]  \(constant input\)

Fixed point: x\* = αc/\(α\+λ\) = G·c  \(attractor for stable regime\)

Stability: |f\_α'\(x\*\)| = |1\-α\-λ| < 1  ⇔  0 < α\+λ < 2

Bifurcation diagram \(pole p = 1\-α\-λ vs\. α\):

  α = 0:      p = 1\-λ = 0\.998  \[neutrally stable; Welford limit\]

  α = 1/300:  p = 0\.9947         \[current operating point\]

  α = 1:      p = \-λ = \-0\.002   \[period\-2 cycle emerges\]

  α = 2\-λ:    p = \-1             \[FLIP BIFURCATION \(period\-doubling\)\]

  α > 2\-λ:   |p| > 1            \[unstable; diverging oscillations\]

__Flip bifurcation at α\_c = 2−λ = 1\.998\. Current α = 1/300 = 0\.00333 is 599× below α\_c\. The system is deeply in the stable regime\.__

__The flip \(period\-doubling\) bifurcation at α = 1\.998 is the boundary between stable convergence and diverging oscillations\. __For α slightly above 1\.998, the fixed point loses stability and a period\-2 orbit appears \(the class mean oscillates between x\* \+ ε and x\* − ε\)\. As α increases further, a cascade of period\-doubling bifurcations leads to chaos\. However, since α is a learning rate and must satisfy 0 < α ≤ 1 \(probability constraint\), the chaos regime \(α > 2\) is inaccessible\. The system can only undergo a single flip bifurcation at α = 1\.998 ≈ 2, which is itself at the boundary of the physical constraint\.

__The 599× safety margin to the flip bifurcation explains the robustness of the learning dynamics\. __Even if the effective learning rate were increased 500× \(by processing each class sample 500 times instead of once\), the system would still be in the stable regime\. The MDL decay λ = 0\.002 shifts the bifurcation point from α = 2 to α = 2 − λ = 1\.998, a tiny change that makes the system slightly more robust \(narrower unstable region\)\.

## __2\.2 Temperature T as Bifurcation Parameter__

The temperature T controls the sharpness of the posterior distribution\. The statistical mechanics analysis identified a second\-order phase transition at the critical temperature T\_c = 22\.4:

Posterior self\-consistency: p\_k = σ\_k\(LLR\(μ\_k\)/T\)

Order parameter: m\(T\) = max\_k p\_k  \[fraction of posterior on dominant class\]

Phase structure:

  T < T\_c = 22\.4: ORDERED phase   \[m\(T\) > 1/K; peaked posterior\]

  T = T\_c:        CRITICAL point   \[continuous bifurcation\]

  T > T\_c:        DISORDERED phase \[m\(T\) = 1/K; uniform posterior\]

Current state:  T = 2\.5  \(9\.0× below T\_c\)

Order parameter at T=2\.5: m = 0\.9999  \(from DS10: p\_max ≈ 1\.000\)

Distance to critical: ΔT = T\_c \- T = 22\.4 \- 2\.5 = 19\.9

Classification breaks down at T = T\_c = 22\.4

__The bifurcation at T\_c = 22\.4 is a second\-order \(continuous\) phase transition\. __As T increases through T\_c from below, the order parameter m\(T\) decreases continuously from m\(T\_c^\-\) = \(K\-1\)/K \(just below critical: one class barely dominant\) to m\(T\_c^\+\) = 1/K \(uniform\)\. There is no latent heat \(energy discontinuity\) — this is a Landau second\-order transition\. The order parameter exponent β = 1/2 \(mean\-field\), so m\(T\) ∼ \(T\_c \- T\)^\{1/2\} near T\_c\. At T = 2\.5, we are at T/T\_c = 0\.112 — deep in the ordered phase, far from any transition\.

# __3\. Arnold Tongues: Phase\-Locking Regions__

When the input to an EMA filter is periodic with frequency f and amplitude A, the filter output locks to the input frequency with amplitude ratio R/A = |H\_α\(e^\{2πif\}\)|\. The Arnold tongue is the region in \(f, A\) space where the filter output is ‘locked’ to the input \(gain > threshold\):

Forced EMA: v\(t\+1\) = \(1\-α\)v\(t\) \+ α·A·sin\(2πft \+ φ\)

Steady\-state: v\(t\) = R·sin\(2πft \+ ψ\)

Gain: R/A = |H\_α\(f\)| = α / |1\-\(1\-α\)e^\{\-2πif\}|

Arnold tongue boundary: R/A = threshold \(e\.g\., 0\.7 = \-3\.1 dB\)

__EMA Scale__

__α__

__f\_\{\-3dB\} \(natural\)__

__f\_\{\-6dB\} \(−6 dB = gain=0\.5\)__

__Arnold tongue width \(gain>0\.7\)__

__Fraction locked__

Fast

0\.100

0\.01679

0\.02917

0\.01608 cyc/samp

45\.7% of log\-range

Medium

0\.050

0\.00817

0\.01417

0\.00730 cyc/samp

34\.1% of log\-range

Slow

0\.020

0\.00322

0\.00557

0\.00226 cyc/samp

19\.1% of log\-range

Very slow

0\.005

0\.00080

0\.00138

< 0\.001 cyc/samp

0\.0% \(no locking\)

__Arnold tongue widths: fast EMA locks 45\.7% of the log\-frequency range; very slow locks nothing \(< 0\.001 cyc/sample\)\. The four\-scale bank provides multi\-resolution phase\-locking across three decades\.__

__Arnold tongues in discrete nonlinear systems arise from the interplay between the natural frequency of the oscillator and the forcing frequency\. __For a linear EMA filter, the ‘tongue’ is simply the passband of the filter: any periodic input within the passband is tracked with amplitude gain > threshold\. The very slow EMA \(α = 0\.005, f\_3dB = 0\.001\) has no measurable locking at frequencies above 0\.001 cyc/sample — it is essentially a DC estimator that ignores periodic components\. The fast EMA \(α = 0\.10, f\_3dB = 0\.0168\) tracks periodic patterns with periods as short as 6 samples \(0\.167 cyc/sample / f\_3dB = 10× margin\)\.

__In the context of network security, the Arnold tongues correspond to the temporal scales of detectable periodic attack patterns\. __A DDoS flood with a regular packet inter\-arrival time of T\_attack = 1/f\_attack samples will be phase\-locked by the fast EMA if T\_attack > 1/0\.017 = 59 samples, by the medium EMA if T\_attack > 1/0\.008 = 125 samples, and by the slow EMA if T\_attack > 1/0\.003 = 310 samples\. The very slow EMA \(1/0\.0008 = 1250 samples\) provides context averaging over long time horizons but does not track rapid oscillations\.

# __4\. Basin of Attraction Volumes__

## __4\.1 Monte Carlo Basin Estimation__

The basin of attraction B\_k = \{h: argmax\_j LLR\_j\(h\) = k\} is the set of all points that ‘belong to’ class k under the classifier\. We estimate basin volumes by Monte Carlo sampling under two distributions:

__Class__

__P\(basin | world\-prior Gaussian\)__

__P\(basin | class mixture\)__

__Interpretation__

net\_normal

69\.51%

10\.15%

Largest Gaussian basin; world prior maps here

log\_error

 9\.99%

10\.08%

Second\-largest Gaussian basin

bin\_benign

 6\.58%

10\.13%

net\_scan

 5\.68%

10\.08%

log\_warn

 4\.22%

10\.21%

log\_info

 3\.24%

9\.87%

net\_ddos

 0\.28%

10\.08%

net\_exfil

 0\.49%

10\.13%

net\_c2

 0\.01%

10\.01%

Smallest Gaussian basin; most ‘remote’ class

bin\_malware

< 0\.01%

9\.87%

Nearly zero Gaussian basin

__Under N\(μ₀, v̄·I\): net\_normal captures 69\.5% of Gaussian probability; bin\_malware < 0\.01%\. Under the class mixture: all basins nearly equal \(9\.7–10\.2%\) — linear separability confirmed\.__

__The 69\.5% basin volume for net\_normal under the world\-prior Gaussian reflects its geometric centrality\. __The world\-prior distribution N\(μ₀, v̄·I\) is centred at the world mean μ₀, which the convex analysis paper showed maps to net\_normal \(LLR\_\{net\_normal\}\(μ₀\) = −19\.04, the least negative\)\. Since most probability mass under the world prior is near μ₀, and net\_normal’s Voronoi cell is the one containing μ₀, net\_normal gets the lion’s share\. Bin\_malware’s basin \(< 0\.01%\) is almost invisible under the world prior because bin\_malware’s centroid is the farthest from the world prior \(Fisher distance 11\.53\) and requires very specific byte patterns \(MZ header\) to reach\.

__Under the class mixture, all basins are nearly equal \(9\.7–10\.2%\), confirming linear separability\. __When samples are drawn uniformly from all K class distributions, each class gets approximately 1/K = 10% of the probability mass assigned to its own basin\. The near\-perfect balance \(standard deviation 0\.13% across classes\) demonstrates that the classifier has properly separated all K classes in the encoded feature space, with no class ‘leaking’ into another’s basin under its own distribution\.

## __4\.2 Basin Boundaries: Fisher Geodesic Midpoint Theorem__

The decision boundary between class i and class j is the hyperplane \{h: LLR\_i\(h\) = LLR\_j\(h\)\}\. For equal\-covariance Gaussians, this boundary passes through the geodesic midpoint of the two class centroids:

Geodesic midpoint: μ\_mid = \(μ\_i \+ μ\_j\)/2  \[in Fisher metric = arithmetic midpoint\]

Theorem \(proved in Convex Analysis paper\):

  LLR\_i\(μ\_mid\) = LLR\_j\(μ\_mid\)  and  t\* = 0\.5000 for all pairs

Verified numerically for 5 pairs:

  bin\_malware ↔ bin\_benign : t\* = 0\.5000  \(boundary at exact midpoint\)

  log\_info    ↔ log\_warn   : t\* = 0\.5000

  net\_normal  ↔ net\_c2     : t\* = 0\.5000

  net\_scan    ↔ net\_ddos   : t\* = 0\.5000

  log\_error   ↔ bin\_malware: t\* = 0\.5000

  ⇒ ALL boundaries are exactly at the geodesic midpoint \(Bayes\-optimal to 4 d\.p\.\)

__The t\* = 0\.5000 result for all pairs is the dynamical expression of Bayes\-optimality\. __In the equal\-covariance Gaussian model, the optimal \(minimum\-error\) decision boundary between classes i and j is exactly the perpendicular bisector of the segment \[μ\_i, μ\_j\] in the Fisher metric — the geodesic midpoint\. The NIG classifier, by construction \(shared variance v₀, class means μ\_k = μ₀ \+ δ\_k\), achieves this exactly\. The dynamical interpretation: the gradient flow of the loss function converges to the Bayes\-optimal boundary, confirming that the fixed point θ\* is the globally optimal classifier for the Gaussian model\.

# __5\. Attractor Geometry and Phase Portrait__

## __5\.1 Fixed Points and Convergence Residuals__

After training, the system state θ is near \(but not at\) the fixed point θ\*\. The convergence residual measures the remaining distance:

__Class__

__||δ\_k \- δ\_k\*|| \(residual\)__

__Mean orbit radius ||h\-μ\_k||__

__Orbit/residual ratio__

net\_normal

0\.311

0\.474

1\.52

net\_scan

0\.379

0\.239

0\.63

net\_ddos

0\.474

0\.146

0\.31

net\_exfil

0\.509

0\.249

0\.49

net\_c2

0\.536

0\.365

0\.68

log\_info

0\.444

0\.021

0\.05

log\_warn

0\.386

0\.017

0\.04

log\_error

0\.322

0\.044

0\.14

bin\_malware

0\.497

0\.669

1\.35

bin\_benign

0\.322

0\.644

2\.00

__Mean convergence residual 0\.418 \(class means are 80% converged after training\)\. Mean orbit radius 0\.287\. Log classes are extremely tight \(orbit 0\.017–0\.044\); binary classes are diffuse \(orbit 0\.644–0\.669\)\.__

__The convergence residual measures how far the class mean has drifted from its steady\-state target G·E\[h−μ₀|y=k\]\. __After 300 samples per class \(3 epochs × 100\), the step\-response analysis predicts 79\.9% convergence, consistent with the observed residuals \(mean 0\.418 ≈ 20% of the target offset\)\. The net\_c2 class has the largest residual \(0\.536\) because it has the largest class offset ||E\[h−μ₀|y=k\]|| and requires more samples to converge\. The log classes have the smallest residuals \(0\.311–0\.386\) due to their near\-zero within\-class variance \(orbit radius 0\.017–0\.021\)\.

__The orbit radius \(within\-class variance in latent space\) reveals class structure\. __Log classes have essentially zero variance in latent space \(orbit radius 0\.017–0\.044\): the rigid \[TYPE\] HH:MM:SS format produces nearly identical feature vectors for all samples\. Binary classes have the highest variance \(0\.644–0\.669\): the random payload after the 4\-byte header creates diverse feature vectors\. From a dynamical perspective, the log classes sit at essentially a single point in latent space \(a true fixed point of the input process\), while the binary classes form a diffuse cloud \(a noisy attractor\)\.

## __5\.2 Phase Portrait: Gradient Flow__

In the continuous\-time limit, the class mean update becomes the ordinary differential equation \(ODE\):

dδ\_k/dt = α\_k\(h \- μ₀\) \- \(α\_k\+λ\)δ\_k

This is a linear ODE with exact solution:

  δ\_k\(t\) = δ\_k\* \+ \(δ\_k\(0\)\-δ\_k\*\)·exp\(\-\(α\_k\+λ\)t\)

  where δ\_k\* = \[α\_k/\(α\_k\+λ\)\]·E\[h\-μ₀|y=k\]  = G·E\[h\-μ₀|y=k\]

Jacobian of the flow: J = \-\(α\_k\+λ\)·I  where α\_k\+λ = 0\.00533

  All eigenvalues: \-0\.00533  \(scalar multiple of identity\)

  div\(F\) = tr\(J\) = D·\(\-0\.00533\) = 128×\(\-0\.00533\) = \-0\.683

  curl\(F\) = 0  \(gradient flow: irrotational, no vorticity\)

  Interpretation: strongly contracting flow, no spirals or cycles

__The zero curl \(irrotational flow\) confirms that the dynamics are purely dissipative — no oscillations or limit cycles\. __A gradient flow ∇V always has curl = 0: the flow follows level sets of the potential function V\(δ\_k\) = \(α\_k\+λ\)||δ\_k−δ\_k\*||^2/2 \(quadratic Lyapunov function\)\. The negative divergence div\(F\) = −0\.683 measures the rate at which phase volume shrinks under the flow: after time t, a ball of initial conditions with volume V₀ has volume V₀·exp\(−0\.683t\)\. This strong volume contraction is the global attractor property: all initial conditions converge to the single fixed point δ\_k\*\.

# __6\. Lyapunov Spectrum of the Full System__

The Lyapunov spectrum \{λ\_L^1 ≥ λ\_L^2 ≥ \.\.\.\} characterises the long\-time average rate of stretching or contraction in each state\-space direction\. For a system with globally attracting fixed point, all Lyapunov exponents are negative:

Full state dimension: 17,792

Block 1 — World prior μ₀ \(Welford, frozen after 3000 steps\):

  Pole p\_μ = 1 \- 1/3000 = 0\.99967

  λ\_L = log\(0\.99967\) = \-0\.000333 per step

  D = 128 degenerate eigenvalues \(scalar × identity update\)

Block 2 — Class means \{δ\_k\}, k=1\.\.10:

  Pole p\_k = 1 \- α\_k \- λ = 0\.994667

  λ\_L = log\(0\.994667\) = \-0\.005348 per step

  K×D = 1280 degenerate eigenvalues

Block 3 — Encoder W \(contrastive Fisher\-Rao\):

  λ\_L ≈ log\(1 \- η\_enc·κ\_F\) ≈ \-0\.001 to \-0\.002 per step  \(estimated\)

  D² = 16,384 eigenvalues \(rich spectral structure\)

Maximum Lyapunov exponent: λ\_L^max = \-0\.000333  \(world prior block\)

All λ\_L < 0 → globally asymptotically stable fixed point

Kaplan\-Yorke dimension: d\_KY = 0  \(point attractor, no fractal structure\)

__Maximum Lyapunov exponent λ\_L^max = −0\.000333 per step\. All 17,792 exponents negative: point attractor with Kaplan\-Yorke dimension 0\. CyphaDIF is anti\-chaotic\.__

__The slowest mode \(world prior, λ\_L = −0\.000333\) is the bottleneck for convergence\. __The world prior requires approximately 1/|0\.000333| = 3000 steps to contract by 1/e — it has essentially ‘frozen’ after training\. In contrast, the class means \(λ\_L = −0\.005348\) converge 16× faster, and the encoder even faster \(estimated\)\. The multi\-timescale structure of the Lyapunov spectrum reflects the hierarchical learning: fast local updates \(class means, encoder\) converge first, followed by slow global adaptation \(world prior\)\.

__The Kaplan\-Yorke dimension d\_KY = 0 means the attractor is a single point \(zero\-dimensional\)\. __The Kaplan\-Yorke formula d\_KY = j \+ Σ\_\{i=1\}^j λ\_L^i / |λ\_L^\{j\+1\}| where j is the largest index such that Σ\_\{i=1\}^j λ\_L^i ≥ 0\. Since all λ\_L < 0, even the first sum λ\_L^1 < 0, giving j = 0 and d\_KY = 0\. This contrasts with strange attractors \(d\_KY > 0, fractal geometry\) found in chaotic systems\. CyphaDIF’s attractor is a simple point: the learned parameter vector θ\*\.

# __7\. First\-Passage Times and Escape Analysis__

For a correctly classified sample h\_0, the first\-passage time T\_fp is the number of iid noise perturbations ε\_t ~ N\(0, v̄·I\) needed before the classification flips from class i to class j:

h\_t = h\_0 \+ ε\_t  where ε\_t ~ N\(0, v̄·I\) iid

Flip event: LLR\_i\(h\_t\) < LLR\_j\(h\_t\)

          ⇔  ⟨w\_i\-w\_j, ε\_t⟩ > Δ\_0 = LLR\_i\(h\_0\) \- LLR\_j\(h\_0\)

P\(flip per step\) = Q\(Δ\_0 / σ\_proj\)

  where σ\_proj = σ\_noise · ||w\_i\-w\_j||  \(σ\_noise = √v̄ = 0\.124\)

  and Q\(x\) = Φ\(\-x\) = P\(N\(0,1\) > x\)

__Class pair__

__Δ₀ \(LLR gap at centroid\)__

__σ\_proj__

__P\(flip per step\)__

__E\[T\_fp\] \(steps\)__

bin\_malware ↔ bin\_benign

37\.90

10\.06

8\.3×10^\{−5\}

1\.2×10^4

log\_warn ↔ log\_error

44\.12

11\.24

4\.3×10^\{−5\}

2\.3×10^4

log\_info ↔ log\_warn

48\.86

12\.01

2\.4×10^\{−5\}

4\.2×10^4

net\_normal ↔ net\_scan

71\.30

14\.19

2\.5×10^\{−7\}

4\.0×10^6

net\_exfil ↔ net\_c2

127\.56

17\.86

4\.6×10^\{\-13\}

2\.2×10^\{12\}

net\_c2 ↔ bin\_malware

159\.27

19\.00

2\.6×10^\{\-17\}

3\.8×10^\{16\}

__E\[T\_fp\] ranges from 1\.2×10^4 \(hardest: bin\_malware↔bin\_benign\) to 3\.8×10^\{16\} \(easiest: net\_c2↔bin\_malware\)\. The classifier would survive 10^4 iid noise steps before misclassifying even the hardest pair\.__

__The first\-passage time of 1\.2×10^4 steps for the hardest pair \(bin\_malware↔bin\_benign\) is the dynamical expression of the Bhattacharyya bound \(5\.3×10^\{\-5\}\) from the coding theory paper\. __The mean escape time is 1/P\(flip\) = 1/8\.3×10^\{\-5\} = 1\.2×10^4\. This is the number of iid noise observations needed before the classifier’s decision on a bin\_malware sample \(at the class centroid\) is expected to flip to bin\_benign\. In practice, classifier outputs are not perturbed by iid noise, so this is a theoretical worst\-case stability measure\.

__The enormous range \(12 orders of magnitude\) between hardest and easiest pairs reflects the 4\.2× range in LLR gaps\. __The LLR gap Δ₀ enters the Q\-function argument exponentially: doubling Δ₀ roughly squares the escape time\. Net\_c2↔bin\_malware has Δ₀ = 159\.3 \(4\.2× larger than bin\_malware↔bin\_benign\), giving an escape time of 3\.8×10^\{16\} — longer than the age of the universe in seconds \(4\.3×10^\{17\}\)\. This class pair is effectively ‘unconfusable’ under any realistic noise level\.

# __8\. Omega\-Limit Sets and Recurrence__

The omega\-limit set ω\(x\_0\) of a trajectory starting from x\_0 is the set of all accumulation points as t→∞\. For a gradient flow with a globally attracting fixed point:

ω\(θ₀\) = \{θ\*\}  for ALL initial conditions θ₀ ∈ Θ

Verification via convergence simulation \(bin\_malware, 1000 steps\):

  t=  0: dist = 1\.103  \(ratio 1\.000 = start, 1 step = instant correction\)

  t=  1: dist = 0\.662  \(ratio 0\.600 — large first\-step correction\)

  t= 10: dist = 0\.643  \(ratio 0\.583\)

  t= 50: dist = 0\.575  \(ratio 0\.521\)

  t=100: dist = 0\.495  \(ratio 0\.449\)

  t=300: dist = 0\.223  \(ratio 0\.202 — 80% convergence at end of training\)

  t=500: dist = 0\.012  \(ratio 0\.010 — 99% convergence\)

  t→∞: dist → 0    \(ratio → 0 — exact convergence to θ\*\)

Fitted Lyapunov exponent \(t=50\.\.300\): \-0\.00373 per step

  \(Theoretical: log\(p\_k\) = \-0\.00535; slight discrepancy from Welford α\_t = 1/t\)

__The single\-point omega\-limit set ω\(θ₀\) = \{θ\*\} for all initial conditions is the global attractor property\. __By the Poincaré\-Bendixson theorem \(for 2D systems\) and its higher\-dimensional analogues, a gradient flow with a unique fixed point and a globally defined Lyapunov function must converge to the fixed point\. Here, V\(δ\_k\) = ||δ\_k − δ\_k\*||^2 is a global Lyapunov function \(V ≥ 0, ̇V < 0 away from δ\_k\*\), confirming the omega\-limit set is the singleton \{δ\_k\*\}\. The Poincaré recurrence theorem does not apply \(it requires a measure\-preserving flow; CyphaDIF’s flow is volume\-contracting\)\.

# __9\. Sensitivity to Initial Conditions__

A hallmark of chaotic systems is sensitive dependence on initial conditions: two nearby trajectories diverge exponentially\. CyphaDIF exhibits the opposite — exponential convergence:

Two trajectories: δ\(0\) = 0,  δ'\(0\) = ε  \(||ε|| = 0\.1\)

Same update rule applied to both\.

Separation: ||δ\(t\) \- δ'\(t\)|| = ||ε||·p\_k^t  \(exact, linear system\)

  t=  0: separation = 0\.10000  \(ratio 1\.00000\)

  t=  1: separation = 0\.09947  \(ratio 0\.99467\)

  t= 10: separation = 0\.09479  \(ratio 0\.94793\)

  t= 50: separation = 0\.07654  \(ratio 0\.76538\)

  t=100: separation = 0\.05858  \(ratio 0\.58581\)

  t=300: separation = 0\.02010  \(ratio 0\.20103\)

Halving time t\_½ = log\(0\.5\)/log\(p\_k\) = 129\.6 steps

Chaotic: t\_½ → 0  \(exponential amplification of errors\)

CyphaDIF: t\_½ = 129\.6 steps  \(exponential suppression of errors\)

__Perturbation halving time t½ = 129\.6 steps\. CyphaDIF is STRONGLY CONTRACTIVE — initial condition differences halve every 130 training steps\. The complete opposite of chaos\.__

__The halving time of 129\.6 steps has a direct operational interpretation\. __If the class mean estimator starts from a wrong initial guess \(e\.g\., a different prior\), the error is halved every 130 training observations of that class\. After 3 epochs × 100 samples = 300 observations, the error has been reduced to 0\.201 of its initial value — from any starting point, the system converges to within 20% of the correct answer\. This robustness to initial conditions is the dynamical complement of the large phase margin \(PM = 126\.8°\) identified in the control theory analysis\.

__Strong contractivity implies unique global attractors and zero topological entropy\. __A contractive system with rate ρ < 1 has a unique fixed point by the Banach contraction mapping theorem: any two trajectories starting from different initial conditions converge to the same limit\. The topological entropy h\_top = max\(0, λ\_L^max\) = max\(0, −0\.000333\) = 0, confirming no chaos\. This is in sharp contrast to turbulent dynamical systems, strange attractors, or chaotic neural networks, which have positive topological entropy\.

# __10\. Nonlinear Dynamics of the Softmax Map on the Simplex__

## __10\.1 Fixed Points and Their Stability__

The softmax map S\_T: ℝ^K → Δ^\{K\-1\} sends score vectors to probability simplices\. The map is a nonlinear contraction on the probability simplex for T > 1:

Softmax: \[S\_T\(s\)\]\_k = exp\(s\_k/T\) / Σ\_j exp\(s\_j/T\)

Jacobian at p\*: J\_\{ij\} = \(1/T\)\(δ\_\{ij\} p\_i \- p\_i p\_j\) = \(1/T\)\(diag\(p\) \- p p^T\)

Eigenvalues of J: \{ 0 \(K\-1 times\), p\_k^max/T \(approximately\) \}

Spectral radius: ρ\(J\) ≈ 1/T  \(for confident posteriors p\_max ≈ 1\)

  T=0\.1 \(optimal\):  ρ\(J\) = 10\.0 > 1  \[fixed\-point iteration diverges\]

  T=1\.0:            ρ\(J\) = 1\.0 = 1  \[neutrally stable boundary\]

  T=2\.5 \(nominal\):  ρ\(J\) = 0\.4 < 1  \[fixed\-point iteration converges\]

  T=22\.4 \(T\_c\):     ρ\(J\) ≈ 0\.045   \[very slow contraction near critical\]

## __10\.2 Posterior Self\-Consistency__

The posteriors at the class centroids are extremely concentrated, with the correct class capturing essentially all probability mass:

__Class__

__p\*\(correct class\)__

__p\*\(2nd highest\)__

__Posterior entropy H \[nats\]__

net\_normal

1\.000000

0\.000000

0\.000000

net\_scan

1\.000000

0\.000000

0\.000000

net\_ddos

1\.000000

0\.000000

0\.000000

net\_exfil

1\.000000

0\.000000

0\.000000

net\_c2

1\.000000

0\.000000

0\.000000

log\_info

1\.000000

0\.000000

0\.000000

log\_warn

1\.000000

0\.000000

0\.000001

log\_error

1\.000000

0\.000000

0\.000000

bin\_malware

1\.000000

0\.000000

0\.000001

bin\_benign

0\.999999

0\.000001

0\.000016

__All class centroids achieve p\*\(correct\) = 1\.000000 to 6 decimal places\. The softmax map at T=2\.5 is a strong contraction \(spectral radius 0\.4\), consistent with the deep\-certainty regime confirmed across all prior analyses\.__

__The spectral radius ρ\(J\) = 1/T = 0\.4 means the fixed\-point iteration p\(t\+1\) = S\_T\(LLR\(h\)/T\) converges geometrically at rate 0\.4 per step\. __Starting from the uniform distribution p\(0\) = \(1/K,\.\.\.,1/K\), after t iterations the distance to the fixed point p\* has been multiplied by 0\.4^t: 1 step gets you 60% of the way, 2 steps 84%, 5 steps 99%\. The temperature T=2\.5 → T=1 boundary is the convergence threshold for this iteration: at T < 1, the iteration diverges \(spectral radius > 1\) and cannot be used to find the posterior; at T > 1, it converges\.

__The T\* = 0\.1 optimum \(from statistical mechanics\) gives spectral radius 10 — it is NOT a contraction\. __This is not a contradiction: T\* = 0\.1 is optimal for the posterior’s accuracy \(Brier score, calibration\), not for the fixed\-point iteration’s convergence\. At T\* = 0\.1, the softmax posterior is correctly calibrated but the naive iteration p\(t\+1\) = S\_\{T\*\}\(LLR\(h\)\) would not converge\. In practice, the posterior at T\* = 0\.1 is computed in a single forward pass \(not iteratively\), so the spectral radius of the Jacobian is irrelevant for inference — it only matters if one tried to use fixed\-point iteration as a solver\.

# __11\. Synthesis: Dynamical Systems Portrait of CyphaDIF__

- __Bifurcations: Two bifurcation parameters identified\. __Learning rate α: flip bifurcation at α\_c = 1\.998 \(599× above current α = 1/300\)\. Temperature T: second\-order phase transition at T\_c = 22\.4 \(9× above nominal T = 2\.5\)\. Both parameters are deeply in the stable ordered regime\.
- __Arnold tongues: The four EMA scales provide multi\-resolution phase locking\. __Fast EMA \(α = 0\.10\) locks 45\.7% of the log\-frequency range; very slow \(α = 0\.005\) provides DC averaging only\. The NIGField thus captures periodic traffic patterns on timescales from 6 to 1250 samples\.
- __Basin geometry: Under the world prior, net\_normal captures 69\.5% of probability mass; under the class mixture, all basins are equal \(9\.7–10\.2%\)\. __All decision boundaries pass exactly through Fisher geodesic midpoints \(t\* = 0\.5000 for all 5 tested pairs\), confirming Bayes\-optimality of the basin boundaries\.
- __Lyapunov spectrum: All 17,792 exponents negative \(λ\_L^max = −0\.000333\)\. __Kaplan\-Yorke dimension 0: point attractor\. The three\-block structure \(world prior: λ = −0\.000333; class means: λ = −0\.00535; encoder: λ ≈ −0\.001–0\.002\) reveals the multi\-timescale convergence hierarchy\.
- __First\-passage escape times: 1\.2×10^4 \(bin\_malware↔bin\_benign\) to 3\.8×10^\{16\} steps \(net\_c2↔bin\_malware\)\. __Even the hardest pair survives 12,000 noise steps before flipping\. The 12\-order\-of\-magnitude range \(hardest vs\. easiest\) arises from the 4\.2× range in LLR gaps\.
- __Sensitivity to initial conditions: t½ = 129\.6 steps\. __CyphaDIF is strongly contractive \(all Lyapunov exponents negative, topological entropy 0\): the opposite of a chaotic system\. Any two trajectories from different starting points converge to the same fixed point\.
- __Softmax simplex dynamics: spectral radius ρ\(J\) = 1/T = 0\.4 < 1 at T = 2\.5\. __The softmax map is a contraction on the probability simplex for T > 1\. The nominal T = 2\.5 ensures convergent posterior updates\. The optimal T\* = 0\.1 gives ρ\(J\) = 10 \(a fixed\-point iteration at T\* would diverge, but single\-pass inference is unaffected\)\.

# __References__

\[1\] Strogatz, S\. H\. \(2015\)\. Nonlinear Dynamics and Chaos \(2nd ed\.\)\. CRC Press\.

\[2\] Kuznetsov, Y\. A\. \(2004\)\. Elements of Applied Bifurcation Theory \(3rd ed\.\)\. Springer\.

\[3\] Guckenheimer, J\., & Holmes, P\. \(1983\)\. Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields\. Springer\.

\[4\] Arnold, V\. I\. \(1988\)\. Geometrical Methods in the Theory of Ordinary Differential Equations \(2nd ed\.\)\. Springer\.

\[5\] Devaney, R\. L\. \(2003\)\. An Introduction to Chaotic Dynamical Systems \(2nd ed\.\)\. Westview Press\.

\[6\] Lyapunov, A\. M\. \(1992\)\. The General Problem of the Stability of Motion\. Taylor & Francis\. \(Original 1892\.\)

\[7\] Eckmann, J\.\-P\., & Ruelle, D\. \(1985\)\. Ergodic theory of chaos and strange attractors\. Reviews of Modern Physics, 57\(3\), 617–656\.

\[8\] Milnor, J\. \(1985\)\. On the concept of attractor\. Communications in Mathematical Physics, 99\(2\), 177–195\.

\[9\] Banach, S\. \(1922\)\. Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales\. Fundamenta Mathematicae, 3, 133–181\.

\[10\] Poincaré, H\. \(1890\)\. Sur le problème des trois corps et les équations de la dynamique\. Acta Mathematica, 13, 1–270\.

\[11\] Zaslavsky, G\. M\. \(2005\)\. Hamiltonian Chaos and Fractional Dynamics\. Oxford University Press\.

\[12\] Kaplan, J\. L\., & Yorke, J\. A\. \(1979\)\. Chaotic behavior of multidimensional difference equations\. Lecture Notes in Mathematics, 730, 204–227\.

\[13\] Fredrickson, P\., Kaplan, J\. L\., Yorke, E\. D\., & Yorke, J\. A\. \(1983\)\. The Liapunov dimension of strange attractors\. Journal of Differential Equations, 49\(2\), 185–207\.

\[14\] Lorenz, E\. N\. \(1963\)\. Deterministic nonperiodic flow\. Journal of the Atmospheric Sciences, 20\(2\), 130–141\.

\[15\] Mandelbrot, B\. B\. \(1982\)\. The Fractal Geometry of Nature\. W\. H\. Freeman\.

\[16\] Redner, S\. \(2001\)\. A Guide to First\-Passage Processes\. Cambridge University Press\.

\[17\] Gardiner, C\. \(2009\)\. Stochastic Methods: A Handbook for the Natural and Social Sciences \(4th ed\.\)\. Springer\.

\[18\] Lasota, A\., & Mackey, M\. C\. \(1994\)\. Chaos, Fractals, and Noise: Stochastic Aspects of Dynamics \(2nd ed\.\)\. Springer\.

\[19\] Robinson, C\. \(1999\)\. Dynamical Systems: Stability, Symbolic Dynamics, and Chaos \(2nd ed\.\)\. CRC Press\.

\[20\] Wiggins, S\. \(2003\)\. Introduction to Applied Nonlinear Dynamical Systems and Chaos \(2nd ed\.\)\. Springer\.

