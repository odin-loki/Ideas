# Filtering — GH-SR-IMM

> **Generalised-Hyperbolic Square-Root Interacting-Multiple-Model.** A heavy-tailed-noise multi-target tracker that combines Normal-Inverse-Gaussian / GH measurement noise with conjugate GIG-style scale updates, a three-model IMM (constant-velocity, constant-acceleration with AR(ρ) jerk, H∞ adversarial), square-root cubature Kalman propagation, and a **GH-JPDA** extension that fixes a subtle but consequential bug in the standard recipe — *do not* use the GH likelihood directly inside the JPDA association, use the GH posterior covariance `R_eff` inside a Gaussian association likelihood. With that one fix, GOSPA on a packaged multi-target benchmark drops by **51.6 % on average**, peaking at **72.8 %** on one of the four scenarios.

---

## What this folder is

If you want to track a target whose measurement noise has heavy tails (clutter, glints, occasional outliers) under a manoeuvring motion model, the textbook answer is "use a Student-t Kalman filter or a variational-Bayes Kalman, plug it into JPDA, done." The textbook answer underperforms because:

1. **Heavy tails and manoeuvre handling want different handles.** Conflating them — for example by widening the Student-t degrees-of-freedom every time the target accelerates — degrades both. The right move is to *decouple* the heavy-tail story (per-model GH posterior) from the manoeuvre story (IMM mixing).
2. **Heavy-tailed likelihoods inside JPDA association silently overweight the "all measurements are clutter" hypothesis.** Putting the raw GH likelihood `L = NIG(ν; 0, R)` into the association probability calculation is what the literature does; it's wrong. The fix is to use a Gaussian likelihood with the GH-derived effective covariance `R_eff`, which keeps the heavy-tail robustness in *estimation* but stops the association math from degenerating.

This folder ships the algorithm, the proof in two papers (one full, one short overlap), and a benchmark harness that reproduces the headline numbers in 3–5 minutes on a laptop.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`GH_SR_IMM_Research_Paper.md`](GH_SR_IMM_Research_Paper.md) | Full research paper. Defines the GH measurement model, conjugate scale updates `χ_{k+1} = (1−α)χ_k + α·E[V|ν]`, the IMM transition matrix, square-root CKF predict step, the four named adapters (IW-Q, IW-R, AR-ρ, ACF), and the GH-JPDA fix in §. |
| [`GH_SR_IMM_Paper.md`](GH_SR_IMM_Paper.md) | Shorter overlap paper. |
| [`harcf_benchmark.py`](harcf_benchmark.py) | Reproducible benchmark harness. Single-target run + multi-target run with seeds 42–46, ~3–5 min total runtime. |

---

## 🧠 The mathematics

**Measurement model.** `v_k ~ GH(0, R, χ, ψ)`, `λ = −½` ⇒ NIG. The effective per-step covariance is `R_eff = R / E[1/V | ν]` where `V` is the GIG mixing variable. Online conjugate updates with smoothing rate `α = 0.02` keep `χ` and `ψ` tracking slowly-changing noise statistics.

**IMM bank.**

|  | CV | CA-AR(ρ) | H∞ |
|---|---|---|---|
| Role | constant-velocity baseline | constant-acceleration with first-order autoregressive jerk | adversarial worst-case |

Mode transition `Tr = [[0.95,0.04,0.01],[0.04,0.95,0.01],[0.20,0.20,0.60]]` — the H∞ row is "if you were here last, you're probably going somewhere predictable next." Innovations drive mode-update with the **full NIG log-likelihood**, not a Gaussian approximation.

**Square-root cubature.** The CKF predict step factors covariance via QR on an augmented sigma-point matrix (paper §3.4). This is the "SR" in GH-SR-IMM: numerical stability under the heavy-tailed posteriors that GH produces.

**Adapters.**

- **IW-Q** (process-noise inverse-Wishart) — inliers gated at `MAD 2.5σ`.
- **IW-R** (measurement-noise inverse-Wishart).
- **AR-ρ** — slow online estimate of the jerk autocorrelation for the CA model.
- **ACF monitor** — fault-detection on innovations, threshold `2/√n`.

**GH-JPDA** (the fix). Use `L_GH = N(ν; 0, S_eff)` where `S_eff` is computed from `R_eff`. Critical claim: naive NIG-in-JPDA *hurts* tracking; documented hurt → fix in the paper.

---

## 📊 Reported benchmarks

**Single-target composite score** `S = RMSE + 0.4·|mean(NIS) − 1| + 0.2·std(NIS)`:

| Filter | Composite | Wins / 8 |
|---|---|---|
| **GH-SR-IMM (this work)** | **1.090** | **6** |
| Huang (Student-t robust KF) | 1.760 | — |
| Agamennoni (variational-Bayes KF) | 3.509 | — |

That's **+38 % over Huang, +69 % over Agamennoni** on the same eight scenarios.

**Multi-target GOSPA** (`c = 5, p = 2`) on a 2-target / 2-sensor / `N = 300` setup with `λ_c = 0.05` clutter and seeds 42–46:

| Method | Mean GOSPA | Per-scenario improvement |
|---|---|---|
| Gaussian-JPDA | 4.069 | — |
| **GH-JPDA (this work)** | **1.971** | **51.6 % avg; 48.3 % / 24.9 % / 56.0 % / 72.8 %** |

---

## 🚧 Honest caveats

- **Correlated-Q discussion** — the paper notes that one configuration variant (`1.275`) does not clearly beat Huang's score (`1.252`), so the win is not universal across hyperparameter regimes.
- **Fixed IMM transition matrix** — not learned online, set as in the table above.
- **Multi-target setup assumes known track count and near-truth initialisation**. There is no full track-initiation/termination story in the multi-target benchmark; it tests filtering quality, not data-association recovery from cold start.
- **`harcf_benchmark.py` `SingleTargetTracker` is not the full GH-SR-IMM stack** that the JPDA section uses — the multi-target class uses a simpler SR-CKF + GH per tracker. Methodology splits between "full single-target stack" and "multi-target framework"; treat the GOSPA numbers as evidence that the GH-JPDA *fix* matters, not that the full IMM bank was running per-tracker.

---

## 🎯 What this displaces

| Standard | Limitation | What GH-SR-IMM offers |
|---|---|---|
| Kalman filter + JPDA | Gaussian; collapses on heavy tails | GH-NIG measurement noise, robust to clutter / glints |
| Student-t KF (Huang) | Couples manoeuvre and tail handling | Decoupled: GH per-model + IMM mixing |
| VB-KF (Agamennoni) | Heavy iteration cost; overruns at high noise | Conjugate GIG updates; closed-form |
| GH-likelihood in JPDA | Silently overweights all-clutter hypothesis | `R_eff` inside Gaussian association — empirical 51.6 % GOSPA improvement |

---

## 🔗 Related work in this repo

- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — ARIA-INTEL, full-pipeline tactical-intelligence engine using PMBM rather than IMM as the filtering backbone
- [`../Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator (Lévy / GH machinery is shared mathematical lineage)
- [`../Battle Sim/`](../Battle%20Sim/) — battle modelling that consumes filtered tracks
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — adjacent algebraic structure work

---

[← Back to main README](../README.md)
