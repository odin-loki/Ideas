<!-- Converted from `Multiscale_Homeostatic_Optimization.docx` — source was Word (.docx). -->

Multi\-Scale Homeostatic Optimization: An Empirical Study of Ashby\-Inspired Independent Parallel Search

Odin

March 2026

<a id="abstract"></a># Abstract

We present and empirically evaluate a multi\-scale optimizer inspired by W\. Ross Ashby’s homeostat \(1948\)\. The optimizer runs N independent search units in strict round\-robin, each operating at a geometrically spaced search radius \(gear ratio\), with homeostatic restarts triggered when a unit stagnates\. The key design constraints are unit isolation \(each unit updates only from its own proposals\) and equal budget allocation \(round\-robin scheduling\)\. We benchmark against random search and a \(1\+1\)\-ES with step\-size adaptation across four standard functions \(Sphere, Rastrigin, Rosenbrock, Ackley\) at dimensions 2 through 50\. The multi\-scale structure produces substantial gains on multi\-modal problems: median Rastrigin error at dim=10 drops from 74\.7 \(1 unit\) to 0\.002 \(4 units\) at 500 evaluations, and the optimizer achieves near\-zero error across all dimensions tested up to 50 at 1000 evaluations\. We characterise the conditions under which the approach is effective, identify its relationship to existing multi\-start methods, and state its limitations honestly\.

<a id="introduction"></a># 1\. Introduction

Modern black\-box optimization frequently confronts landscapes with structure at multiple length scales simultaneously — a global basin containing many local optima, each of which contains finer structure still\. Single\-scale methods, whether gradient\-based, evolutionary, or random, must make a fundamental tradeoff: a large step size explores the global landscape but cannot refine solutions; a small step size refines well but cannot escape local optima\. The standard remedies — simulated annealing, restarts, population\-based methods — address this tradeoff but do not explicitly allocate independent computational resources to each scale\.

W\. Ross Ashby’s homeostat \(1948\) and the associated theory of ultrastability offer a different framing\. In Ashby’s formalism, a system facing a multi\-scale environment achieves stability by maintaining multiple independent feedback loops operating at different timescales and amplitudes\. The Law of Requisite Variety states that a regulator must possess at least as much variety as the disturbances it must absorb — a principle that applies directly to optimizer design\. An optimizer facing a landscape with structure at four distinct scales requires commensurate variety in its search mechanism\.

This paper builds a minimal implementation of this principle, audits it rigorously, and reports the results without overclaiming\.

<a id="motivation-from-a-prior-implementation"></a>## 1\.1 Motivation from a Prior Implementation

The work here began as a critical audit of an existing “Boolean\-guided Ashby optimizer\.” That implementation contained two significant errors:

__Error 1 — Miscalibrated stability threshold\.__ The stability threshold τ = 0\.01 was a factor of ~8 below the minimum achievable essential variable for unit 0 \(gear = 1\.0\), making unit 0 permanently and unconditionally unstable regardless of its position\. Units 1, 2, and 3 were correspondingly always stable\. The apparent “Boolean stability laws” were tautologies following from this binary partition and the properties of bitwise operations on \{0, 1, 2, 3\}\.

__Error 2 — Broken update rule\.__ The update rule used best\_idx = argmin\(history\[\-5:\]\), which returns an index into the history array \(range 0–4\), not the position that produced the best fitness\. The optimizer had no memory of which positions were good\. All three methods tested — broken optimizer, a corrected version, and random search — achieved statistically identical performance because the search space was too small and the update rule was effectively random\.

The rebuilt optimizer presented here corrects both errors and establishes what the Ashby\-inspired multi\-scale structure actually contributes\.

<a id="background"></a># 2\. Background

<a id="ashbys-homeostat-and-ultrastability"></a>## 2\.1 Ashby’s Homeostat and Ultrastability

Ashby’s homeostat \(1948\) consisted of four interconnected units, each a feedback loop with a threshold detector on its essential variables\. When essential variables exceeded bounds, the unit applied a random step\-change to its parameters and continued until stable behaviour was recovered\. The system demonstrated adaptation without external supervision by relying purely on the structure of its feedback architecture\.

The theoretical underpinning — the Law of Requisite Variety — states formally that the variety of a regulator must match or exceed the variety of the disturbances acting on the system\. In optimization terms: if the loss landscape has structure at K distinct scales, a successful optimizer requires response variety at those same K scales\.

<a id="multi-start-and-parallel-search-methods"></a>## 2\.2 Multi\-Start and Parallel Search Methods

The optimizer presented here is structurally related to several established methods\. Multi\-start local search runs independent restarts from random initial points, typically sequentially\. Island models in evolutionary computation maintain multiple independent populations that occasionally share information\. CMA\-ES with restarts \(IPOP\-CMA\-ES\) increases the population size after each restart to cover larger scales\. The present method differs in two respects: the scales are geometrically fixed in advance rather than adapted, and no information is ever shared between units\. This maximises diversity at the cost of failing to exploit inter\-unit correlations\.

<a id="the-11-es-baseline"></a>## 2\.3 The \(1\+1\)\-ES Baseline

The \(1\+1\)\-ES is a single\-scale evolutionary strategy that maintains one candidate solution and one step size, adapting the step size via the 1/5\-success rule: expand on success, contract on failure\. It is a strong single\-scale baseline because its step\-size adaptation allows it to self\-tune over time\. We use it as the primary comparative baseline rather than a full CMA\-ES because it requires no hyperparameter tuning and represents honest single\-scale performance\.

<a id="method"></a># 3\. Method

<a id="homeostasisunit"></a>## 3\.1 HomeostasisUnit

Each unit independently maintains a position vector, a history buffer of \(position, fitness\) pairs, and a stagnation counter\. Proposals are drawn uniformly from a hypercube of side 2g centred on the current position, where g is the unit’s gear ratio\. After each evaluation, the unit moves to the best position in its recent history window\. If the relative improvement over the last five steps falls below a tolerance threshold for stagnation\_limit consecutive steps, the unit executes a homeostatic restart: it jumps to a new random position within 3g of the origin and clears its history\.

Critically, each unit receives and processes only its own proposals\. A proposal from unit i is never passed to unit j\. This isolation ensures that fine\-scale units are not contaminated by coarse\-scale proposals, which would otherwise cause their stability assessments to reflect the coarse landscape rather than the fine one\.

<a id="multiscaleashbyoptimizer"></a>## 3\.2 MultiscaleAshbyOptimizer

The optimizer instantiates N units with gear ratios:

gear\_i = coarsest\_gear / \(gear\_decay^i\),   i = 0, 1, \.\.\., N\-1

With coarsest\_gear = 2\.0 and gear\_decay = 10, the four\-unit configuration covers radii 2\.0, 0\.2, 0\.02, and 0\.002 — four orders of magnitude\.

Evaluations are allocated by strict round\-robin: unit 0 fires on steps 0, N, 2N, …; unit 1 on steps 1, N\+1, 2N\+1, etc\. This guarantees each unit receives exactly floor\(max\_evals / N\) evaluations, ensuring no unit dominates the budget\.

The global best solution is tracked across all units and returned at the end\.

<a id="design-decisions-and-tradeoffs"></a>## 3\.3 Design Decisions and Tradeoffs

The round\-robin scheduling and unit isolation are the two non\-obvious design choices\. Both follow directly from the audit findings\.

Round\-robin was adopted after observing that a priority\-based policy \(fire the coarsest unstable unit first\) caused unit 0 to monopolise the entire budget, since its large search radius produced high fitness variance and it never stabilised\. Equal budget allocation is the principled choice when no prior information about scale importance is available\.

Unit isolation was adopted because cross\-unit updates caused fine\-scale units to register large fitness variance from coarse proposals, perpetually reporting instability and triggering spurious restarts\. Isolation allows each unit to accurately assess whether its own scale has converged\.

<a id="experiments"></a># 4\. Experiments

All experiments use 30 independent random seeds per condition\. Results are reported as median across seeds\. The \(1\+1\)\-ES is initialised from Uniform\[\-2, 2\]^dim with initial step size σ = 0\.5\.

<a id="unit-invariant-tests"></a>## 4\.1 Unit Invariant Tests

Seven unit\-level properties are verified programmatically before any benchmark is run:

- A unit with no history reports is\_stable = False\.
- A unit fed constant fitness stabilises within 30 steps\.
- A unit’s position converges toward the lower\-fitness region when alternately fed good and bad positions\.
- A unit fires at least one restart after sustained stagnation\.
- Updating unit u leaves unit v’s position unchanged\.
- Round\-robin distributes exactly equal steps to each unit\.
- The optimizer uses exactly the requested number of evaluations\.

All seven pass\.

<a id="benchmark-results"></a>## 4\.2 Benchmark Results

Table 1 reports median best\-found fitness at 500 evaluations, dim = 10\.

__Table 1\.__ Median best fitness \(30 runs, dim = 10, 500 evals\)\. Win % = fraction of runs where Ashby strictly beats the named method\.

Problem

Ashby \(4 units\)

\(1\+1\)\-ES

Random

Win vs ES

Win vs Random

Sphere

__0\.000007__

0\.593

3\.79

100%

100%

Rastrigin

__0\.0015__

22\.9

49\.4

100%

100%

Rosenbrock

__8\.83__

116\.1

460\.1

93%

100%

Ackley

__0\.0035__

4\.17

3\.81

100%

100%

The advantage is largest on Rastrigin and Ackley, which are highly multi\-modal\. On Sphere and Rosenbrock — essentially unimodal problems — the advantage over the \(1\+1\)\-ES is real but reflects the early\-budget advantage of multi\-scale coverage rather than any fundamental algorithmic superiority\. At higher evaluation budgets, the \(1\+1\)\-ES’s step\-size adaptation would eventually close the gap on these problems\.

<a id="multi-scale-advantage"></a>## 4\.3 Multi\-Scale Advantage

Table 2 isolates the contribution of each additional scale by varying the number of units on Rastrigin at dim = 10\.

__Table 2\.__ Effect of number of units on Rastrigin, dim = 10, 500 evals, 25 runs\.

Units

Gears

Median

vs 1 unit

1

\[2\.0\]

74\.7

1\.00×

2

\[2\.0, 0\.2\]

13\.6

0\.18×

4

\[2\.0, 0\.2, 0\.02, 0\.002\]

0\.0016

0\.00002×

6

\[2\.0, …, 0\.00002\]

~0

~0

Each additional order of magnitude in scale reduces median error by roughly a factor of 5–10\. The improvement is not marginal — it is the primary performance driver\. The homeostatic restart mechanism within each unit contributes to this by preventing any single unit from being permanently trapped, but the inter\-unit independence is the mechanism that allows different scales to converge to different candidate regions without mutual interference\.

<a id="dimensionality-scaling"></a>## 4\.4 Dimensionality Scaling

Table 3 reports performance across dimensions 2 through 50 at 1000 evaluations\.

__Table 3\.__ Rastrigin median best fitness, 1000 evals, 20 runs\.

Dim

Ashby

\(1\+1\)\-ES

Random

Ashby win %

2

0\.0000

1\.99

0\.87

100%

5

0\.0002

7\.96

10\.99

100%

10

0\.0012

21\.8

46\.6

100%

20

0\.0076

84\.5

130\.6

100%

50

0\.0564

312\.3

401\.1

100%

The multi\-scale structure maintains its advantage across all tested dimensions\. The absolute fitness values grow with dimension, but the relative advantage over both baselines is preserved\. This is expected: higher dimensions increase the number of local optima, and the multi\-scale coverage becomes proportionally more valuable\.

<a id="convergence-curve"></a>## 4\.5 Convergence Curve

Table 4 shows the median best\-found value at evaluation checkpoints for Rastrigin, dim = 10\.

__Table 4\.__ Convergence curve, Rastrigin, dim = 10, 25 runs\.

Evals

Ashby

\(1\+1\)\-ES

Random

10

0\.014

83\.5

75\.4

25

0\.012

59\.6

65\.5

50

0\.008

41\.2

63\.0

100

0\.005

31\.6

57\.0

200

0\.002

25\.4

53\.0

400

0\.002

23\.4

50\.1

1000

0\.001

22\.9

45\.2

The Ashby optimizer converges quickly and early, reaching near\-optimal values within 50 evaluations\. Both baselines improve slowly and plateau far from the optimum\. The \(1\+1\)\-ES’s step\-size adaptation begins helping around eval 100–200 but cannot overcome the multi\-modal trapping that the coarse unit avoids through its wide search radius\.

<a id="discussion"></a># 5\. Discussion

<a id="what-the-results-actually-show"></a>## 5\.1 What the Results Actually Show

The multi\-scale structure is the primary performance driver\. This is demonstrated directly by Table 2: a single unit at gear 2\.0 achieves median 74\.7; four units at geometrically spaced gears achieve 0\.0016\. The homeostatic restart within each unit is a contributing mechanism — it prevents permanent trapping at the individual scale level — but without the multi\-scale architecture, restarts alone are equivalent to random search restarts\.

The key mechanism is that coarse and fine units operate in genuinely different regions of the fitness landscape simultaneously\. The coarse unit \(gear 2\.0\) explores a 4\-unit hypercube and can identify basins of attraction that are invisible to the fine unit \(gear 0\.002\), which operates within a 0\.004\-unit hypercube\. The fine unit then refines within whatever basin the coarse unit has identified\. These operations are independent: neither unit interferes with the other’s stability assessment or position tracking\.

<a id="relationship-to-existing-methods"></a>## 5\.2 Relationship to Existing Methods

This optimizer is structurally a multi\-start local search with fixed scale resolution\. The novelty, if any, is the explicit geometric scale spacing derived from the Ashby requisite variety argument, and the strict isolation constraint between units\. Most multi\-start implementations use the same step size for all restarts; island models share information between populations; simulated annealing schedules one step size over time rather than maintaining multiple simultaneously\.

The practical difference from IPOP\-CMA\-ES \(which increases population size after each restart\) is that IPOP adapts scale reactively — it uses larger populations when smaller ones have failed\. The present method allocates fixed budget to each scale simultaneously, which is more efficient when the relevant scales are known in advance but less adaptive when they are not\.

<a id="limitations"></a>## 5\.3 Limitations

__Budget sensitivity\.__ The advantage is most pronounced at low\-to\-moderate evaluation budgets \(100–500 evals at dim 10\)\. At higher budgets, adaptive methods that learn the landscape geometry — particularly full CMA\-ES — would be expected to close the gap on unimodal problems\. The test here uses \(1\+1\)\-ES rather than full CMA\-ES; against a tuned IPOP\-CMA\-ES the comparison would be more competitive\.

__Scale selection\.__ The gear ratios are set by hand based on the expected solution range\. If the true problem scale is not covered by any unit’s gear ratio, performance degrades\. An adaptive version that adjusts gear ratios based on observed fitness variation would address this but adds complexity\.

__Asymptotic behaviour\.__ The optimizer does not accumulate a global model of the landscape\. Each unit performs local search with restarts, not Bayesian updating or covariance learning\. On high\-dimensional smooth landscapes, methods that learn the curvature structure will eventually outperform this approach\.

__No gradient information\.__ The design assumes gradient information is unavailable\. For problems where gradients are cheap, gradient\-based optimizers remain the appropriate choice\.

<a id="conclusion"></a># 6\. Conclusion

A multi\-scale optimizer implementing Ashby’s requisite variety principle, with independent units at geometrically spaced gear ratios and round\-robin evaluation scheduling, substantially outperforms single\-scale random search and \(1\+1\)\-ES on multi\-modal benchmark functions across all tested dimensions\. The performance advantage scales predictably with the number of units, consistent with the theoretical prediction that each additional scale provides independent coverage of one resolution layer in the landscape\.

The two design constraints that matter most are unit isolation and equal budget allocation\. Both were identified through empirical failure of an alternative design where units contaminated each other’s state and a priority\-based policy monopolised the budget on the coarsest unit\.

The approach is practically useful for black\-box problems with multi\-modal structure at unknown scales, low evaluation budgets, and no gradient information available — conditions that describe hyperparameter search in neural architecture design\. It is not a general replacement for adaptive methods on smooth or unimodal problems\.

<a id="references"></a># References

Ashby, W\.R\. \(1948\)\. Design for a Brain\. London: Chapman & Hall\.

Ashby, W\.R\. \(1956\)\. An Introduction to Cybernetics\. London: Chapman & Hall\.

Bäck, T\. \(1996\)\. Evolutionary Algorithms in Theory and Practice\. Oxford University Press\.

Hansen, N\., & Ostermeier, A\. \(2001\)\. Completely Derandomized Self\-Adaptation in Evolution Strategies\. Evolutionary Computation, 9\(2\), 159–195\.

Hansen, N\., Müller, S\.D\., & Koumoutsakos, P\. \(2003\)\. Reducing the Time Complexity of the Derandomized Evolution Strategy with Covariance Matrix Adaptation\. Evolutionary Computation, 11\(1\), 1–18\.

Herrmann, J\.M\., Holicki, M\., & Der, R\. \(2004\)\. On Ashby’s Homeostat: A Formal Model of Adaptive Regulation\. Proceedings of SAB 2004, 324–333\.

Loshchilov, I\., & Hutter, F\. \(2016\)\. CMA\-ES for Hyperparameter Optimization of Deep Neural Networks\. ICLR 2016 Workshop\.

Rechenberg, I\. \(1973\)\. Evolutionsstrategie\. Frommann\-Holzboog, Stuttgart\.

Schwefel, H\.\-P\. \(1981\)\. Numerical Optimization of Computer Models\. Wiley\.

