# Filtering — GH-SR-IMM robust multi-target tracking

> **Generalised Hyperbolic Interacting-Multiple-Model filter with Square-Root Cubature Kalman propagation, plus a GH-JPDA multi-target extension.** A robust adaptive Bayesian tracking filter that simultaneously handles non-Gaussian (heavy-tailed) measurement noise, unknown / time-varying target dynamics, and numerically stable covariance propagation. Reference Python implementation included.

---

## 📡 What this folder is

A research paper, a shorter conference-style writeup, and a benchmark implementation. The deliverable is a generic robust tracking filter, not a domain-specific radar or sonar system — but the paper motivates the design by referring to non-Gaussian measurement noise in radar clutter, multipath in urban GNSS / inertial navigation, and impulsive returns in acoustic sensors.

The acronym **GH-SR-IMM** expands as:

- **GH** — Generalised Hyperbolic distribution (NIG subfamily, after Barndorff-Nielsen)
- **SR** — Square-Root (Cholesky-form Cubature Kalman propagation)
- **IMM** — Interacting Multiple Model

Earlier README copy expanded this as "Gated Hamiltonian Sequential Recursive" — that gloss does not appear in any source document and has been corrected.

Attribution: **O. Halvorsen · Independent Defense Research, Sydney · Technical Report TR-2026-GH-SR-IMM · March 2026**.

---

## 📄 Files

| File | Role |
|------|------|
| [`GH_SR_IMM_Research_Paper.md`](GH_SR_IMM_Research_Paper.md) | Full research paper — derivation, theorems, eight-scenario single-target benchmark + four-scenario multi-target benchmark, references |
| [`GH_SR_IMM_Paper.md`](GH_SR_IMM_Paper.md) | Shorter / conference-style version |
| [`harcf_benchmark.py`](harcf_benchmark.py) | Python reference implementation + reproducible benchmark harness |

---

## 🎯 What the filter does

1. **Non-Gaussian measurement noise** — places a Normal-Inverse Gaussian (NIG) distribution over measurement noise. Two NIG shape parameters (χ, ψ) are adapted **per model, per timestep** using exact conjugate Generalised Inverse Gaussian (GIG) posterior updates — heavy-tail handling without approximation.
2. **Unknown / time-varying dynamics** — three competing models compete via a standard IMM mixer: **CV** (constant velocity), **CA** (constant acceleration with correlated noise), **HI** (H-infinity robust). Model probabilities are updated using the **full NIG likelihood**.
3. **Numerical stability** — covariance matrices are propagated in **Cholesky square-root form** throughout (SR-CKF, third-degree spherical-radial cubature rule, QR-decomposition predict step), guaranteeing positive definiteness at every step.

### GH-JPDA multi-target extension

A naive substitution of NIG likelihoods into standard JPDA performs **worse** than Gaussian-JPDA, because NIG marginals are heavier-tailed and outliers receive higher association weight. The paper's contribution: use the GH posterior to **inflate the effective measurement noise** for outlier-like measurements, making the association Gaussian small and correctly suppressing their association probability.

---

## 📊 Benchmark headline numbers (from the abstract)

| Metric | Result |
|--------|--------|
| Single-target benchmark composite score (lower is better) | **GH-SR-IMM 1.09** vs Student-t KF (Huang 2017) **1.76** vs Variational Bayes KF (Agamennoni 2012) **3.51** |
| Improvement over Student-t KF | **38 %** |
| Improvement over VB KF | **69 %** |
| Multi-target GOSPA reduction (GH-JPDA vs Gaussian-JPDA) | **51.6 %** lower mean GOSPA across four geometric scenarios with clutter |

Single-target benchmark covers eight scenarios: Gaussian, heavy-tail, Lévy, manoeuvring, correlated, mixed-regime, bimodal, jerk dynamics. Multi-target benchmark covers four geometric scenarios with clutter.

---

## 🧪 Contributions (from §1 of the paper)

1. Principled fusion of exact conjugate **GIG posterior updates** with the IMM framework — per-model adaptive non-Gaussian noise characterisation without approximation.
2. **Square-Root CKF** propagation integrated into the IMM mixer-predictor cycle — guaranteed numerical positive definiteness under extreme outlier conditions.
3. Multi-target **GH-JPDA** extension — correct application of the GH posterior to data association, achieving 51.6 % GOSPA reduction.
4. Open-source benchmark + Python reference implementation.

---

## 🚧 Honest framing

- The filter is designed and benchmarked on **synthetic scenarios**; the paper does not claim live radar / sonar / GNSS tracking results.
- Performance numbers are relative to the specific competing filters (Student-t KF, VB KF, Gaussian-JPDA) on the published benchmark suite — they do not constitute a head-to-head against fielded military trackers.
- Three-model IMM is a deliberate tractability choice; deeper variable-structure IMM, LSTM-IMM, etc. are out of scope.

---

## 🔗 Related work in this repo

- [`Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — ARIA-INTEL uses PMBM (a different Bayesian multi-target framework) plus IMM-style model mixture; complementary tracking system
- [`ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — Algebraic Resynchronisation and Integrity Architecture (cryptographic ARIA, unrelated acronym to ARIA-INTEL)
- [`RNGS/`](../RNGS/) — random-number generation primitives used in stochastic motion models
- [`100W Wideband Noise Generator/`](../100W%20Wideband%20Noise%20Generator/) — high-power wideband noise source; the natural adversary for any robust tracking filter

---

[← Back to main README](../README.md)
