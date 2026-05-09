# Asset Tracking Algorithm — ARIA-INTEL

> **ARIA-INTEL = Algebraic Rendezvous & Intelligence Analyser.** A single-file, edge-deployable multi-target tracking and tactical-intelligence engine that fuses Poisson Multi-Bernoulli Mixture (PMBM) random-finite-set tracking, Mixed Ornstein–Uhlenbeck (MOU) motion, spatio-temporal pattern-of-life GMMs, three independent rendezvous-prediction methods stacked in parallel, eight tradecraft detectors, Dempster–Shafer multimodal fusion, and Beta–Monte-Carlo threat scoring — into one Python module designed to run at **~28 ms median scan latency on a single CPU core, no GPU**, on tactical edge hardware.

---

## What this folder is

Most "multi-target trackers" are research code that does one thing — usually a Kalman filter or a basic JPDA over a fixed motion model — and stops at "track ID + position estimate." ARIA-INTEL is intended to be the **whole intelligence pipeline** that downstream operators actually need from a tracker: it doesn't just tell you *where the target is*, it tells you *what the target is doing*, *whether two targets are about to meet*, *whether the target's behaviour matches a known tradecraft pattern*, and *how confident you should be about all of that* — all wrapped in a single config-file abstraction (`DomainProfile`) so the same engine retunes itself for urban HUMINT, maritime, airspace, or vehicle-convoy domains without code changes.

The pitch is: one engine, one config, full pipeline, edge-deployable. The implementation file in this folder is the reference. The accompanying research paper documents the mathematics; the README inside the folder gives a faster operator-facing tour.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`ARIA_INTEL_Research_Paper.md`](ARIA_INTEL_Research_Paper.md) | Full research paper. Defines PMBM update equations, MOU discrete-time formulae (`α = exp(−θ·dt)`, σ_v formula and Urban-MOU table), the three-method rendezvous stack, possibility-theory dual existence (PMBM r vs π_r), the eight Beta-distribution threat dimensions, the topological winding-number SDR, and validation tables on a synthetic scenario generator. |
| [`ARIA_INTEL_README.md`](ARIA_INTEL_README.md) | Operator-style overview (faster onboarding than the research paper). |
| [`aria_intel.py`](aria_intel.py) | Reference Python implementation. Single-file engine. |

> **Naming note.** The research paper and README cite `aria_intel_v6.py`; the file actually present is `aria_intel.py`. They describe the same engine; the version-suffix is internal-bookkeeping language.

---

## 🧠 Subsystems (named in the paper)

| Subsystem | What it does |
|---|---|
| **PMBM tracker** | Random-finite-set multi-target tracker with Poisson-Multi-Bernoulli-Mixture posteriors. Parameters: `R_BIRTH = 0.65`, `P_S = 0.97` (paper) / `P_SURVIVAL = 0.995` (code), `P_DETECTION = 0.85`, `R_CONFIRM = 0.55`, `R_PRUNE = 0.05`, `320` particles, `14` Gibbs sweeps for hypothesis sampling. |
| **MOU motion model** | Mixed Ornstein–Uhlenbeck motion with discrete-time update `α = exp(−θ·dt)`. Per-class (θ, σ) tables for foot, vehicle, stationary, fast platforms (Urban MOU table). Replaces the standard "constant-velocity Gaussian" assumption with a mean-reverting process tuned per behaviour class. |
| **Pattern-of-Life GMM** | `K = 5` Gaussian-mixture pattern-of-life model fitted via EM after `15` observations and refit every `5` observations thereafter. Chi-squared gate `χ²(0.999, df = 2)` for outlier rejection. |
| **Stacked rendezvous warner** | Three methods run in parallel and vote: (1) **Geometric Velocity Intercept** (closest-point-of-approach time over the last `8` track points; the paper reports correctly catching `26 of 39` rendezvous events on this method alone in the synthetic test), (2) **Separation-Rate Extrapolation** for non-intercepting closing geometries, (3) **PoL Cross-Prediction** (throttled every `5` scans, horizon cap `20`) to catch rendezvous that the kinematics alone wouldn't predict because both targets are heading to a known shared waypoint. |
| **Possibility-Bayesian dual existence** | Maintains both Bayesian `r` and possibility-theory `π_r` track-existence scores, alarms on `|r − π_r| / max(r, π_r) > 0.4`. Diagnostic intended to flag "this track is well-supported by data but its support pattern is anomalous" — a class of failure mode that single-existence trackers cannot detect. `POSS_ALPHA = 0.25` in code. |
| **Tradecraft detector pack** | Eight detectors (six explicitly tabled as PASS in the paper) for spotting professionally-evasive movement: surveillance-detection runs, role-rotations across networks, etc. |
| **SDR winding number** | Topological surveillance-detection-run detector. Paper acknowledges this can false-positive on circular patrols. |
| **Threat scorer** | Beta-distributed score across `8` dimensions, `250`-sample Monte Carlo, tier thresholds `0.82 / 0.62 / 0.42 / 0.22` for HIGH / ELEVATED / MODERATE / LOW. |
| **Dempster–Shafer fusion** | Multimodal evidence combination across heterogeneous sensors. |

---

## 📊 Reported benchmarks (synthetic `generate_scenario`, paper §)

| Metric | Value |
|---|---|
| Median scan latency | **28 ms** (paper) / **27 ms** (README — internal inconsistency) |
| Mean scan latency | 51 ms |
| P95 scan latency | 210 ms |
| Max scan latency | 325 ms |
| Throughput | ~20 scans/s on one CPU core |
| Mean position error | 21.8 m |
| P99 position error | 853 m |
| Rendezvous warning recall | **100 % (20/20 scenarios)** |
| Mean rendezvous lead time | 28.1 min; 100 % ≥ 20 min; 95 % ≥ 25 min |
| Detection at low P_D | **100 % at P_D = 0.40, 91 % at P_D = 0.25** |
| False-alarm rate | 0.098 / scan; **0 false alarms at clutter density 40/scan** in one tabled cell |
| Reacquisition over an 8-scan gap | 100 % (10/10) |

These are author-reported, single-author, on a synthetic scenario generator. They are not third-party validations.

---

## 🎯 Domain profiles

The same code retunes for very different sensing regimes via a `DomainProfile` preset:

| Profile | Scan period | RV horizon | Spatial gate |
|---|---|---|---|
| Urban HUMINT | 60 s | 30 min | 150 m |
| Maritime | 3 600 s | 120 min | 2 000 m |
| Airspace | 5 s | 10 min | 1 000 m |
| Vehicle Convoy | 10 s | 5 min | 30 m |

---

## 🚧 Honest caveats (called out in the paper §12)

- **PoL needs `15` observations to fit**, so very-low-P_D targets defeat the PoL-driven detectors and the PoL cross-prediction rendezvous arm until enough data accumulates.
- **P95 latency spikes on PoL-cross-predict scans** — the `28 ms` median is not the worst case; aim for `~325 ms` budget.
- **SDR winding-number `> 0.65`** can false-positive on legitimate circular patrols.
- **Network-role tradecraft detectors are weak for `n_tracks < 3`** — no network exists to analyse.
- The possibility/Bayesian existence-mismatch diagnostic is described as having "**no known equivalent in deployed multi-target tracking systems**" — read this as positioning, not as an external endorsement.
- File-naming inconsistency between paper-cited `aria_intel_v6.py` and the on-disk `aria_intel.py`.
- 27 ms vs 28 ms median latency varies between paper and README — single-author inconsistency.

---

## 🌐 What this displaces

| Role | Standard tool | What ARIA-INTEL adds |
|---|---|---|
| Multi-target tracker | JPDA, GM-PHD, basic PMBM | Whole-pipeline output (kinematics → behaviour → rendezvous → tradecraft → threat) |
| Pattern-of-life | Hand-rolled per-deployment GMM | Self-fitting, refitting PoL with chi-squared gating built in |
| Rendezvous prediction | Usually absent | Three methods stacked; documented `100 %` recall with 28 min mean lead time on its own scenario suite |
| Threat scoring | Rule-based ROE matrix | Beta-MC with calibrated tier thresholds |

---

## 🔗 Related work in this repo

- [`../Filtering/`](../Filtering/) — GH-SR-IMM heavy-tailed multi-target tracking (complementary; ARIA-INTEL uses a different filter family but shares the IMM idea)
- [`../Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator that underpins the Beta-MC threat machinery's distributional reasoning
- [`../Battle Sim/`](../Battle%20Sim/) — adjacent: tactical reasoning over the tracks ARIA-INTEL would deliver
- [`../Weapons/`](../Weapons/) — defence-tech R&D portfolio that consumes intelligence products of this kind

---

[← Back to main README](../README.md)
