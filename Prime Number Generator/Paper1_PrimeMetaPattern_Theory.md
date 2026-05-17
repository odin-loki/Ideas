# A scale-dependent meta-pattern in prime number generation: empirical discovery of a power law transition between local and global generative methods

*Preliminary research manuscript · 2025*

> ## ⚠️ Erratum and 31-sample re-fit (2026)
>
> This paper, as originally drafted, has three problems that an external review and a 31-scale-sample re-run (`fit_meta_pattern.py`, `fit_meta_pattern.md`) confirmed are real. The original text is preserved unchanged below for the historical record; this section overrides any conflicting claim in the body.
>
> **1. Functional-form inconsistency.** §2.2 reports the empirical fit in *exponential* form,
>
> > `f_L(s) = 0.258 · exp(−0.373·s)`,    `f_G(s) = 1 − 0.487 · exp(−0.371·s)`,
>
> and then jumps to the *power-law* form `α(s) = s^(−0.37)`, `β(s) = 1 − 0.487·s^(−0.37)` in the same section, asserting they are the same. They are not: at `s = 2` the exponential gives `0.258 · exp(−0.746) ≈ 0.122`, while the power law gives `2^(−0.37) ≈ 0.774`, a factor of ~6 disagreement. The numerical values reported in Tables 1 and 2 of the paper (`α = 77.4 %` at `s = 2`, etc.) match the *power law*; the algorithm code in `prime_generator.py` also used the *power law*; but the only fit equation actually written down in §2.2 is the *exponential*. This was a transcription error.
>
> **2. The exponent `−0.37` does not reproduce on more scale samples.** The original fit was performed on three scale points (`s = 2, 5, 7`); with only three points one cannot distinguish a power law from an exponential. Re-fitting with 31 evenly-spaced scale samples (`s = 1.0, 1.25, …, 8.5, 9.0`), 600 + 600 balanced primes/composites per scale, and three independent measurements (`fit_meta_pattern.md`):
>
> | Curve | Form | Fit | AIC | Verdict |
> |---|---|---|---:|---|
> | M1 residue-classifier excess AUC | power law | `0.391 · s^(−0.104)` | `−80.19` | best by `0.9` |
> |                                  | exponential | `0.382 · exp(−0.026·s)` | `−79.28` | indistinguishable |
> | M2 small-prime filter rejection rate | rational | `1.050 / (1 + 0.034·s)` | `−158.10` | **best** |
> |                                       | exponential | `1.040 · exp(−0.029·s)` | `−156.19` | close |
> |                                       | power law | `1.057 · s^(−0.111)` | `−138.72` | **rejected, ΔAIC = +19.4** |
>
> No curve produces an exponent near `−0.37`. M1's measured exponent is `~ −0.10`. M2 is best fit by a rational form (a *plateau*, not a power law) and the exponential beats the power law by `ΔAIC = +17.5`.
>
> **3. The "critical transition at `n* ≈ 836`" (`s* ≈ 2.92`) is an artefact.** It was derived analytically from `1.487 · s^(−0.37) = 1`, i.e. by substituting the (incorrect) exponent and the (incorrect) coefficient `0.487` into a constraint on the algebraic crossing of `α` and `β`. With the corrected M2 fit, `f_M2(s) = 1.050 / (1 + 0.034·s)` is monotonically and slowly declining and **does not cross any specific threshold** in the tested range — at `s = 9` it is still `0.81`. There is no scale-dependent crossover for the algorithm to exploit. The right algorithmic switch — from `O(√n)` trial-division primality to `O(k log³ n)` Miller–Rabin — is set by computational cost, not by feature importance, and lives at `s ≈ 4.5` (`n ≈ 31 623`).
>
> **What this means for the body of this paper.**
>
> - §2.2 (the fit equation), §2.3 (the critical-transition derivation), §3.3 ("the power law meta-pattern"), §3.4 ("the critical transition"), and §4 (the renormalisation-group analogy with `γ = −0.37` as a "universal critical exponent") are all built on the bad three-point fit. They should be read as the original conjecture, **not** as confirmed by this work.
> - §5 (the connection to neural-network weight-matrix spectral exponents reportedly in the `0.35 – 0.45` range, including HRNA's `α ≈ 0.85` and Martin–Mahoney's `~0.37`) was a numerical-coincidence argument. With the actual measured exponent for M1 being `~ −0.10`, **the coincidence is not present**, and this section should be regarded as withdrawn.
> - §3.5 (deterministic vs stochastic information contribution) and the empirical scale-by-scale measurements in §3.1, §3.2 (filter effectiveness, density accuracy) survive — those numbers were measured directly, not derived from the bad fit.
> - The companion algorithm paper (Paper 2) and the algorithm code carry their own erratum block; both have been corrected.
>
> **What survives as the genuine empirical finding.** The local divisibility filter is useful at every scale tested up to `n = 10⁹`, and its useful-work rate decays slowly (best fit a *plateau*, not a power law). The PNT-density approximation becomes very accurate above `s ≈ 4` (relative error `< 0.05`). Hybrid sieve-plus-Miller–Rabin generation is the right operational choice; the original paper's specific *power-law* and *critical-transition* claims about how to weight that hybrid are not supported by the corrected data.
>
> **Appropriate framing.** As corrected, this is empirical, computationally-driven mathematics — appropriate venue is Experimental Mathematics (Taylor & Francis) or Integers, not Annals of Mathematics. The work has no bearing on the Riemann Hypothesis or the Clay Millennium Prize, contrary to any framing in earlier drafts.
>
> The original text follows below for the historical record.

---

## Abstract

We report the empirical discovery of a continuous power law transition governing the optimal generative structure of prime numbers as a function of scale. Through systematic analysis of prime gap distributions, divisibility filter effectiveness, and density prediction accuracy across eight orders of magnitude \(10¹ to 10⁸\), we identify a scale parameter s = log₁₀\(n\) and a weight function:

**α\(s\) = s^\(-0.37\)**

which interpolates between local divisibility-based generation \(dominant for small n\) and global density-based generation \(dominant for large n\). The transition between these two generative regimes occurs smoothly near n\* ≈ 836 \(s\* ≈ 2.92\), which we term the critical transition point. We find this power law is empirically analogous to the running of coupling constants in the Renormalization Group \(RG\) framework from quantum field theory — wherein microscopic \(local\) interactions yield to macroscopic \(statistical/thermodynamic\) behavior as the observation scale increases. This meta-pattern implies that no single closed-form prime generator can be globally optimal; instead, the prime-generating algorithm is best understood as a trajectory through function space parameterized by scale. We derive a working algorithm from this continuous transition and validate it across tested scales. The critical exponent -0.37 matches power law exponents observed in the singular value spectra of neural network weight matrices, suggesting a deep structural connection between prime distributions and learned representations in high-dimensional systems.

**Keywords:** *prime number distribution, scale invariance, power law, renormalization group, meta-pattern, prime gap statistics, prime generation algorithm, phase transition, number theory*

## 1. Introduction

The distribution of prime numbers represents one of the most extensively studied problems in all of mathematics. Since the work of Gauss and Legendre in the late 18th century, it has been known that primes thin out at a rate approximately described by 1/ln\(n\), a result formalized in the Prime Number Theorem \(PNT\) and proved independently by Hadamard and de la Vallée Poussin in 1896 \[1, 2\]. The PNT gives us the global asymptotic density of primes, but the local structure — the precise spacing between consecutive primes, and the rules governing which integers are prime candidates — has proven far harder to characterize.

Two complementary frameworks have traditionally been used to reason about primes. The first is the local, divisibility-based framework: any prime p > 3 must satisfy p ≡ ±1 \(mod 6\) by virtue of the 6k±1 structure arising from elimination of multiples of 2 and 3. More generally, sieve methods \(Eratosthenes, Atkin, Sundaram\) progressively eliminate composite candidates through local divisibility rules. The second is the global, statistical framework: under the Cramér probabilistic model \[3\], gaps between consecutive primes are approximately exponentially distributed with mean ln\(n\), consistent with the heuristic that each integer near n is prime independently with probability 1/ln\(n\). This model, while known to be imperfect — Maier \[4\] demonstrated it fails in short intervals — captures the macro-statistical behavior of prime gaps with remarkable accuracy at large scales.

The central question motivating this work is: how do these two frameworks — the local and the global — relate to one another as a function of scale? We hypothesize, and empirically confirm, that there exists a smooth, power-law governed transition between these two modes of prime generation, analogous to the renormalization group \(RG\) flow in physics where microscopic coupling constants "run" with energy scale \[5\].

Our empirical analysis proceeds as follows. We characterize prime distributions at three representative scales \(n ∼ 10², n ∼ 10⁵, n ∼ 10⁷\) through comprehensive statistical analysis of: \(a\) divisibility filter effectiveness as a function of scale, \(b\) density prediction accuracy of the PNT approximation, \(c\) prime gap distribution fit to exponential models, and \(d\) feature importance weights derived from a binary classification formulation of primality. From these measurements, we extract a power law exponent α = -0.37 governing the decay of local \(divisibility\) importance with increasing scale, and derive the complementary global weight function. We term the resulting framework the "prime meta-pattern" and the transition function the "scale-dependent generative trajectory."

## 1.1 Connections to Prior Work

Our work builds on several strands of prior research. Cohen \[6\] and colleagues recently established that prime gaps are asymptotically characterized by moments matching those of an exponential distribution with mean ln\(n\), providing formal statistical grounding for the global framework. Cramér's original 1936 conjecture \[3\] — that maximal prime gaps are O\(\(ln pⁿ\)²\) — and Granville's subsequent refinements \[7\] provide the theoretical backbone of density-based prime models. In the local framework, the 6k±1 structure is classical, and the efficiency of sieve methods is well-characterized \[8\].

The renormalization group analogy is novel to our knowledge. While there exist connections between the Riemann zeta function and spectral theory in physics \(see Montgomery's pair correlation conjecture and the connection to GUE statistics\), we are unaware of prior work explicitly modeling the local-to-global generative transition in primes as an RG flow. The normal form theory of RG flows \[9\] provides a natural mathematical framework for our empirical observations about universality classes of prime generative methods.

Separately, the power law exponent α = -0.37 we observe matches exponents found in the singular value spectra of weight matrices in trained neural networks \[10\], raising the speculative but intriguing possibility that both phenomena reflect a common underlying principle of information organization across scales.

## 2. Empirical Methodology

We analyzed prime distributions across three primary scale regimes, selecting contiguous windows of 10,000 primes centered at representative values. Scales were chosen to span three orders of magnitude in n, from n ∼ 10² to n ∼ 10⁷, ensuring coverage of the anticipated transition region near n ≈ 836.

## 2.1 Feature Extraction

For each scale, we extracted two classes of feature:

**Local \(divisibility\) features: **fraction of integers passing the 6k±1 filter, filter effectiveness \(composite rejection rate\), and residue class uniformity across mod-6 classes.

**Global \(density/statistical\) features: **observed prime density vs. PNT prediction \(1/ln n\), mean gap vs. expected gap ln\(n\), gap distribution chi-squared deviation from exponential, and gap variance-to-mean ratio.

Feature importance was quantified by treating primality as a binary classification task and measuring the mutual information contribution of each feature class. This approach follows the methodology of Koukoulopoulos \[11\] in treating prime distribution as a probabilistic object.

## 2.2 Scale Parameterization

We parameterize scale as s = log₁₀\(n\), so that the three primary scales correspond to s ≈ 2, 5, and 7. The transition region near n ≈ 836 corresponds to s\* ≈ 2.92. We fit power law curves to the measured feature importances:

**Local importance: f\_L\(s\) = 0.258 · exp\(-0.373 · s\)**

**Global importance: f\_G\(s\) = 1 - 0.487 · exp\(-0.371 · s\)**

The exponents -0.373 and -0.371 are indistinguishable within measurement uncertainty, and we report their common value as -0.37 throughout. This yields the canonical weight function:

**α\(s\) = s^\(-0.37\)   \[local/divisibility weight\]**

**β\(s\) = 1 - 0.487 · s^\(-0.37\)   \[global/density weight\]**

## 2.3 Critical Transition Identification

The critical transition point s\* is defined as the scale at which α\(s\*\) = β\(s\*\), i.e., local and global importance are equal. Solving analytically:

**s^\(-0.37\) = 1 - 0.487 · s^\(-0.37\)**

## 1.487 · s^\(-0.37\) = 1

**s\* = 1.487^\(1/0.37\) ≈ 2.92   =>   n\* = 10^2.92 ≈ 836**

This value is empirically confirmed by direct testing: primes below 836 are most efficiently generated via local \(sieve-based\) methods, while primes above 836 are better generated via density-based approaches. The transition is smooth — no discontinuity or sharp crossover is observed.

## 3. Results

## 3.1 Scale-Dependent Divisibility Filter Effectiveness

A key empirical finding is that divisibility filter effectiveness \(the fraction of composite candidates rejected by the 6k±1 filter plus small-prime trial division\) increases monotonically with scale, contradicting a naive expectation that larger primes would be harder to pre-filter. Table 1 summarizes the observed effectiveness:

**Scale \(n\)**

**s = log₁₀\(n\)**

**Filter Effectiveness**

**Dominant Method**

**Density Accuracy**

~10²

2.0

10.7%

LOCAL \(α = 77.4%\)

103.2%

~10⁵

5.0

33.1%

TRANSITIONING \(α = 55.1%\)

99.5%

~10⁷

7.0

51.4%

GLOBAL \(α = 48.7%\)

100.2%

*Table 1. Scale-dependent properties of prime generation. Filter effectiveness and density accuracy measured over 10,000 consecutive primes per scale.*

The counterintuitive increase in divisibility filter effectiveness with scale can be explained as follows: at large n, the density of primes among 6k±1 candidates is lower, meaning a larger fraction of candidates are composite and thus filterable by small-prime divisibility checks. However, and crucially, the overall importance of divisibility checking to the generation algorithm decreases as the power law α\(s\) = s^\(-0.37\), because the marginal contribution of additional trial division becomes negligible compared to density-guided candidate selection.

## 3.2 Density Prediction Accuracy

The PNT prediction density = 1/ln\(n\) achieves near-perfect accuracy at all scales tested. At s = 2 \(n ∼ 100\), the ratio of actual to expected density is 1.032 \(3.2% overcount\), converging to 0.995 at s = 5 and 1.002 at s = 7. This convergence is consistent with the PNT asymptotic result \[π\(x\) ∼ x/ln\(x\)\] and demonstrates that the global framework becomes highly reliable at moderate scales.

The gap distribution shows similarly strong convergence. At all three scales, the chi-squared statistic comparing observed gap distributions to exponential\(mean = ln\(n\)\) is large and negative \(indicating strong divergence from a pure exponential in absolute terms\) but stable in relative terms — the fraction of gaps within one standard deviation of expectation remains approximately constant. This is consistent with Cohen's \[6\] finding that prime gap moments are asymptotically exponential despite discrete deviations.

## 3.3 The Power Law Meta-Pattern

Fitting power laws to the measured feature importances across scales yields the key result of this paper. The local feature importance decays as a power law in s:

**f\_L\(s\) ∝ s^\(-0.37\)**

while the global feature importance grows complementarily as:

**f\_G\(s\) = 1 - 0.487 · s^\(-0.37\)**

These fits are shown in the figures accompanying this paper. The power law exponent -0.37 is robust across different operationalizations of "local importance": whether measured as mutual information, filter effectiveness relative to total candidates, or classifier feature importance from a logistic regression formulation.

Crucially, this power law implies that the generative structure of primes is not fixed — it is a function of scale. There is no single feature \(neither local divisibility nor global density\) that dominates across all scales. Instead, the optimal strategy smoothly transitions from one to the other, governed by the universal exponent -0.37.

## 3.4 The Critical Transition and Its Neighborhood

In the neighborhood of n\* ≈ 836, the α and β weights are nearly equal, producing a genuinely hybrid generative regime. Table 2 traces the transition through the primes in this neighborhood:

**Prime n**

**α \(local\)**

**β \(global\)**

**Dominant Method**

787

0.675

0.671

LOCAL

797

0.674

0.672

LOCAL

809

0.674

0.672

LOCAL

829

0.673

0.672

LOCAL

839

0.672

0.673

GLOBAL  ← transition

853

0.672

0.673

GLOBAL

877

0.671

0.673

GLOBAL

911

0.669

0.674

GLOBAL

*Table 2. Weight values near the critical transition point n\* ≈ 836. The transition is smooth — weights change by less than 0.001 per step.*

The smoothness of this transition is one of the most important findings of this work. There is no sharp discontinuity, no sudden change in prime distribution statistics, at n\*. The crossover is a gradual re-weighting of generative methods, consistent with a genuine continuous phase transition rather than a first-order jump.

## 3.5 Deterministic vs. Stochastic Components

An additional empirical measurement concerns the decomposition of prime generation into deterministic \(structural\) and stochastic \(random\) components. We find that across all scales, the deterministic component — comprising the 6k±1 structural constraint and exact primality verification — accounts for approximately 96-98% of the generative process \(by information contribution\), with the stochastic component \(gap sampling from exponential distribution\) accounting for only 2-4%.

This finding has practical significance: it implies that a largely deterministic prime generator, relying on the 6k±1 structure for candidate selection and Miller-Rabin verification for primality testing, retains nearly all information content of the full generation process. The stochastic component provides only marginal improvement in candidate selection efficiency at large scales.

## 4. The Renormalization Group Analogy

The pattern we have described — a smooth transition between microscopic \(local\) and macroscopic \(global\) behavior, governed by a power law exponent — is structurally identical to the Renormalization Group \(RG\) flow as formulated in quantum field theory and statistical mechanics \[5, 12, 13\].

In the RG framework, physical systems are analyzed by systematically "coarse-graining" — integrating out short-range degrees of freedom and examining how effective couplings change with observation scale. The key results are:

1. Coupling constants "run" with scale according to the β-function equations of the theory.
2. Fixed points of the RG flow correspond to scale-invariant theories, where the system looks the same at all scales.
3. The approach to a fixed point is governed by critical exponents, which are universal \(independent of microscopic details\) within a universality class.

The correspondence with our prime meta-pattern is precise:

**RG Concept**

**Prime Meta-Pattern Analog**

Observation scale \(energy/length\)

s = log₁₀\(n\)  \(prime scale\)

Running coupling constant α\(E\)

α\(s\) = s^\(-0.37\)  \(local weight\)

UV fixed point \(high energy\)

s → 0: pure local/sieve behavior

IR fixed point \(low energy\)

s → ∞: pure global/density behavior

Critical exponent γ

γ = -0.37 \(measured\)

Phase transition scale

s\* ≈ 2.92, n\* ≈ 836

Universality class

Power law decay class

*Table 3. Structural correspondence between RG flow and the prime meta-pattern.*

In QED, the electric fine structure constant α\_QED runs from approximately 1/137 at low energies to approximately 1/128 at 200 GeV, a running governed by the logarithm of the energy scale \[14\]. Our prime coupling α\(s\) runs from near-unity at small s to near-zero as s → ∞, with the power law replacing the logarithmic running of gauge couplings. The analogy is not exact — prime numbers are not a quantum field theory — but the structural parallel is striking and suggestive.

The most compelling aspect of the analogy is the smooth transition at s\* ≈ 2.92. In RG language, this is a critical point: a value of s at which neither generative method dominates, and the system exhibits "critical slowing down" in the sense that small changes in the algorithm produce maximal uncertainty in outcome. This is analogous to the diverging susceptibility at a thermodynamic critical point \[15\].

We conjecture that the exponent -0.37 is a universal critical exponent in the number-theoretic sense: that it characterizes not just the 6k±1 / PNT transition specifically, but a broader class of transitions between local \(residue-class based\) and global \(density-based\) generative methods for prime-like sequences. Verifying this conjecture would require application of the same analysis to related sequences \(Gaussian primes, prime k-tuples, primes in arithmetic progressions\).

## 4.1 Non-Existence of a Closed-Form Prime Formula

The RG analogy provides a new perspective on the longstanding question of why no simple closed-form formula for primes exists. Our analysis implies that such a formula cannot exist for a deep reason: the optimal generative structure of primes is not a fixed object but a scale-dependent trajectory. A closed-form formula would necessarily pick a single point in the space of generative methods; but the prime meta-pattern tells us that the correct method varies continuously with scale.

More precisely: the prime-generating function is best understood not as a map from integers to primes, but as a point on a trajectory through function space:

**F\(n\) = α\(s\) · F\_local\(n\) \+ β\(s\) · F\_global\(n\),  s = log₁₀\(n\)**

where F\_local and F\_global are themselves well-defined \(divisibility sieve and PNT-based density sampler, respectively\). The prime trajectory is the parameterization of this family of functions by scale. This is structurally analogous to an RG trajectory through theory space, where no single fixed-point theory can capture the behavior at all scales.

## 5. Connection to Neural Network Weight Matrix Spectra

A remarkable coincidence — or possibly a deep connection — arises from the power law exponent α = -0.37 itself. In the analysis of trained neural network weight matrices, singular value spectra have been reported to follow power law distributions with exponents in the range 0.35-0.45 for well-trained networks \[16\]. Odin's earlier work in the HRNA \(Harmonic Recursive Neural Architecture\) framework identifies a power law exponent α ≈ 0.85 for HRNA weight matrices, compared to α ≈ 0.37 in prime gap research.

While the precise relationship between these exponents is not yet understood, we suggest the following speculative interpretation. The singular value spectrum of a weight matrix W ∈ ℝ^\{m×n\} encodes the complexity structure of the function it represents: flat spectra \(all singular values equal\) correspond to pure white noise, while heavy-tailed spectra \(power law decay\) correspond to structured, compressible information. The exponent -0.37 may represent a universal "information compression rate" at which structured objects \(primes, trained weights\) store scale-dependent information in a hierarchy of decreasing importance.

This interpretation is consistent with the GRIA \(Graded Reversible-Irreversible Algebra\) framework, in which compression and cryptography are unified through the concept of scale-dependent information content. Primes, as the elementary multiplicative building blocks of integers, exhibit the same hierarchical information structure as the "important" \(large singular value\) directions in a neural network weight matrix.

We emphasize that this connection is speculative and requires further investigation. However, the numerical coincidence of the exponents — -0.37 in prime gap analysis, -0.37 in neural network spectral analysis — is strong enough to warrant dedicated study.

## 6. Discussion

## 6.1 Implications for Number Theory

Our empirical findings suggest several concrete conjectures for number-theoretic investigation:

1. The exponent -0.37 is universal within the class of local-to-global transitions in prime distribution, independent of the specific local filter used \(6k±1 vs. 30k\+\{1,7,11,...\} etc.\).
2. The critical transition point n\* ≈ 836 has structural significance: it is the scale at which the PNT local error and the sieve efficiency exactly balance.
3. The smooth transition at s\* is related to the behavior of prime gaps near the secondary transition points identified at s = 4.50 \(n ≈ 3×10⁴\) and s = 5.89 \(n ≈ 8×10⁵\), which may represent higher-order RG fixed points.

## 6.2 Limitations

Several limitations of the current analysis should be acknowledged. First, the exponent -0.37 is derived empirically from a limited number of scale samples \(s = 2, 5, 7\); a more rigorous determination would sample more densely across scales and employ maximum likelihood fitting rather than least-squares power law regression. Second, the claim that the transition is "smooth" at n\* ≈ 836 is based on finite-difference observation of α and β values at nearby primes; a formal continuity proof would require analytic tools. Third, the RG analogy, while structurally compelling, remains a heuristic: we have not identified a formal RG group acting on prime distributions, nor a corresponding β-function in the field-theoretic sense.

## 6.3 Future Directions

The meta-pattern discovery opens several promising research directions:

- Formal derivation of the exponent -0.37 from first principles \(Riemann hypothesis conditional or unconditional\).
- Extension to Gaussian primes, prime k-tuples, and primes in arithmetic progressions to test universality.
- Investigation of higher-order transition points \(s = 4.50, 5.89, 8.57\) as potential higher-order RG fixed points.
- Formal proof of the non-existence of a universal prime formula via RG non-commutativity arguments.
- Investigation of the -0.37 exponent in neural network spectra as a possible deep connection to prime information structure.

## 7. Conclusion

We have reported the empirical discovery of a power law meta-pattern governing prime number generation across scales. The central result is:

**α\(s\) = s^\(-0.37\),  s = log₁₀\(n\)**

which characterizes the fraction of prime-generative information contributed by local divisibility rules as a function of scale. The complementary global \(density-based\) weight β\(s\) = 1 - 0.487 · s^\(-0.37\) increases monotonically with scale, reflecting the growing accuracy of the Prime Number Theorem approximation.

The transition between local and global dominance occurs smoothly near the critical point n\* ≈ 836 \(s\* ≈ 2.92\). This smooth transition is structurally analogous to the running of coupling constants in the Renormalization Group framework, providing a new conceptual bridge between number theory and theoretical physics.

Our findings imply that primes do not have "one pattern" but a scale-dependent trajectory of patterns, and that the optimal prime-generating algorithm must adapt its method as a function of the scale of the target prime. A working algorithm implementing this continuous transition is derived and tested in the companion paper to this manuscript.

The discovered exponent -0.37 appears in both prime gap analysis and neural network weight matrix spectra, suggesting a potentially universal role in the power law organization of scale-dependent information in structured mathematical and learned systems.

# Acknowledgments

This research arose from exploratory computational investigation of prime distributions across scales. The empirical findings presented here are preliminary and should be treated as hypotheses for future rigorous mathematical investigation.

## References
**\[1\]  **Hadamard, J. \(1896\). Sur la distribution des zéros de la fonction ζ\(s\) et ses conséquences arithmétiques. Bulletin de la Société Mathématique de France, 24, 199–220.

**\[2\]  **de la Vallée Poussin, C.J. \(1896\). Recherches analytiques sur la théorie des nombres premiers. Annales de la Société scientifique de Bruxelles, 20, 183–256.

**\[3\]  **Cramér, H. \(1936\). On the order of magnitude of the difference between consecutive prime numbers. Acta Arithmetica, 2\(1\), 23–46.

**\[4\]  **Maier, H. \(1985\). Primes in short intervals. Michigan Mathematical Journal, 32\(2\), 221–225.

**\[5\]  **Wilson, K.G. \(1971\). Renormalization group and critical phenomena I. Physical Review B, 4\(9\), 3174–3183.

**\[6\]  **Cohen, J.E. \(2024\). Gaps Between Consecutive Primes and the Exponential Distribution. Experimental Mathematics, 33\(4\), 1–28.

**\[7\]  **Granville, A. \(1995\). Harald Cramér and the distribution of prime numbers. Scandinavian Actuarial Journal, 1995\(1\), 12–28.

**\[8\]  **Riesel, H. \(1994\). Prime Numbers and Computer Methods for Factorization \(2nd ed.\). Birkhäuser, Boston.

**\[9\]  **Sethna, J.P., Tchistiakov, I.M., et al. \(2019\). Normal Form for Renormalization Groups. Physical Review X, 9\(2\), 021014.

**\[10\]  **Martin, C.H., Mahoney, M.W. \(2021\). Implicit self-regularization in deep neural networks: evidence from random matrix theory and implications for learning. Journal of Machine Learning Research, 22\(165\), 1–73.

**\[11\]  **Koukoulopoulos, D. \(2019\). The Distribution of Prime Numbers. American Mathematical Society.

**\[12\]  **Kadanoff, L.P. \(1966\). Scaling laws for Ising models near T\_c. Physics, 2\(6\), 263–272.

**\[13\]  **Fisher, M.E., Wilson, K.G. \(1972\). Critical exponents in 3.99 dimensions. Physical Review Letters, 28\(4\), 240–243.

**\[14\]  **Peskin, M.E., Schroeder, D.V. \(1995\). An Introduction to Quantum Field Theory. Addison-Wesley, Reading MA.

**\[15\]  **Stanley, H.E. \(1971\). Introduction to Phase Transitions and Critical Phenomena. Oxford University Press.

**\[16\]  **Mahoney, M.W., Martin, C.H. \(2019\). Traditional and Heavy-Tailed Self Regularization in Neural Network Models. Proceedings of the 36th International Conference on Machine Learning, ICML 2019, PMLR 97:4284–4293.

**\[17\]  **Hardy, G.H., Wright, E.M. \(2008\). An Introduction to the Theory of Numbers \(6th ed.\). Oxford University Press.

**\[18\]  **Maynard, J. \(2022\). Counting primes. Fields Medal Lecture. Proceedings of the International Congress of Mathematicians.
