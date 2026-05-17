# Archive — legacy material from the previous round of the project

This folder preserves three artefacts from the **March 2026** version of the Prime Number Generator project. They are kept for historical traceability — **not** because their conclusions are correct. The current empirical and neural-network studies reach different (and better-supported) conclusions on two specific points; this README documents what was claimed previously, what is now known to be wrong, and what is now known to be right.

## Files

| File | What it is | Status |
|---|---|---|
| `deep_transition_analysis.py` | Original 3-point analysis script that introduced the "meta-pattern" framing for this project. Performed an explicit divisibility / density / gap analysis at scales `s ∈ {2, 5, 7}` and proposed an algorithm that smoothly transitions between sieve-based and density-based generation as `α(s) = s^{−0.37}` decays. | **Partly retired.** Its qualitative structural argument (use `6k±1` + small-prime sieve + scale-adaptive verifier) is preserved by the current generators. Its specific quantitative claims about the power-law form and "critical transitions" are not reproduced by the dense-grid data — see below. |
| `prime_meta_patterns.png` | First-round visualisation of the meta-pattern. | **Superseded.** New plots can be generated from `reports/fit_meta_pattern.md` and `reports/gap_analysis.md`. |
| `transition_mechanics.png` | First-round visualisation of the supposed sieve↔density transition. | **Refuted.** The transitions it depicts at `s = 4.5, 5.89, 8.57` do not exist on the dense-grid data; see Paper 3, §C.2. |

## What the previous round got right

- **The `6k±1` candidate sieve is the right starting point.** All primes greater than 3 lie on this lattice, cutting the candidate stream by `2/3` immediately.
- **Small-prime trial division is the right pre-filter.** It is cheap, sound (rejects only composites), and effective at every scale tested. Confirmed by both the dense-grid M2 measurement (rejection rate ≥ 0.82 over `s ∈ [1, 9]`) and independently by every distilled NN decision tree (Paper 1, §3.3).
- **The primality verifier should be scale-adaptive.** Trial division is the right choice for small `n`; deterministic Miller–Rabin is the right choice for moderate `n`; probabilistic Miller–Rabin is the right choice for very large `n`.
- **Cramér's first-moment heuristic** (gap mean ≈ `ln n`) holds empirically. The newer Paper 3 §B confirms this with `mean / ln n ∈ [0.97, 1.01]` over `s ∈ [1, 8]`.

## What the previous round got wrong

### 1. The functional family of the scale dependence

> **Claimed:** `α(s) = s^{−0.37}` (a power law with fixed exponent), and `β(s) = 1 − 0.487 · s^{−0.37}`.
>
> **Source:** 3-point fit at `s ∈ {2, 5, 7}`.

> **Refuted by:** dense-grid measurements with `40` scale samples × `1000 + 1000` balanced primes / composites per scale (`fit_meta_pattern.py`, see `reports/fit_meta_pattern.md`).
>
> **Replacement:** rational form `f(s) = 1.027 / (1 + 0.030 · s)` for the M2 filter rejection rate (`ΔAIC = +30.78` over the power-law form). For the M1 residue-classifier excess AUC, all three candidate forms (power, exponential, rational) are statistically indistinguishable (`ΔAIC < 1.5`); the rational form `0.404 / (1 + 0.040 · s)` is selected for stability.

### 2. The "critical transitions"

> **Claimed:** Three critical scales where method dominance flips: primary at `s* = 4.5` (`α = β`), secondary at `s = 5.89` (`α = 0.10`), tertiary at `s = 8.57` (`α = 0.01`).
>
> **Source:** algebraically derived from the rejected `s^{−0.37}` power law.

> **Refuted by:** with the rational fit, `f(s)` plateaus at `0.819` at `s = 9.5` and never drops to 50 %, 10 %, or 1 % over the tested range. The supposed "critical transitions" are an artefact of the rejected functional form.
>
> **What `s = 4.5` actually means in the current code:** `prime_generator.py::_PRIMALITY_TEST_SCALE_THRESHOLD = 4.5` is a *computational-cost* threshold — the point where deterministic Miller–Rabin overtakes trial division on commodity 64-bit hardware (since `√(10^{4.5}) ≈ 178` is roughly the modular-exponentiation cost crossover). It has nothing to do with feature-importance dominance.

### 3. "The function will be discovered from NN weights"

> **Claimed (implicit goal):** train a neural network on prime classification, and a closed-form prime-generation rule will emerge from the trained weights.

> **Honest replacement:** No closed-form prime-generation rule exists, and no such rule emerges. What *does* emerge — robustly, at every scale, by both decision-tree and L1-logistic distillation — is the small-prime trial-division sieve on `6k±1` candidates. The neural network rediscovers, but does not extend, the wheel sieve. This is the principal finding of Paper 1.

## Why the legacy code and figures are kept

1. **Traceability.** The current empirical / NN studies are explicit revisions of the previous round; preserving the previous code lets a reader verify exactly what changed and why.
2. **Sanity check.** Re-running `deep_transition_analysis.py` (which is still functional, modulo a hard-coded `/home/claude/` save path that needs editing for local reproduction) on `s ∈ {2, 5, 7}` reproduces the original 3-point fit and explicitly demonstrates how an underdetermined fit can land on a wrong functional family.
3. **The qualitative algorithm structure was right.** It is worth keeping a visible record of *which* parts of the previous round survived dense-grid validation and which did not.

For the current, validated story, see [`../papers/Paper3_Empirical_Baseline.md`](../papers/Paper3_Empirical_Baseline.md) (this round's empirical baseline), [`../papers/Paper1_NN_Discovery.md`](../papers/Paper1_NN_Discovery.md) (NN weight analysis and distillation), and [`../papers/Paper2_Algorithm_Specification.md`](../papers/Paper2_Algorithm_Specification.md) (the operational generator specifications).
