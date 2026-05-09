# Asset Tracking Algorithm — ARIA-INTEL

> **ARIA-INTEL = Algebraic Rendezvous & Intelligence Analyser.** A single-file, edge-deployable intelligence engine for multi-target tracking, pattern-of-life analysis, tradecraft detection, and rendezvous warning. Theoretically grounded in the Random-Finite-Set / Poisson-Multi-Bernoulli-Mixture framework; designed for deployment on tactical edge hardware (28 ms median scan latency, single CPU core, no GPU).

---

## 🛰 What this folder is

A research paper, a companion implementation README, and a Python reference implementation for **ARIA-INTEL**, the Algebraic Rendezvous & Intelligence Analyser. The system fuses multi-modal sensor data (GEOINT, SIGINT, COMMS, HUMINT, OSINT) into coherent, actionable intelligence tracks.

The acronym is taken from the title page of `ARIA_INTEL_Research_Paper.md` ("Algebraic Rendezvous & Intelligence Analyser"). Earlier README copy expanded ARIA-INTEL as "Asset Recognition and Identification for INTEL applications" — that gloss is not from the source.

> **Note on the "ARIA" name collision.** This folder's ARIA-INTEL is **not related** to the cryptographic ARIA in `../ARIA Encryption Algorithm/` (which expands to *Algebraic Resynchronisation and Integrity Architecture*). They are independent acronyms that happen to share four letters; cross-references between folders should not imply algorithmic dependency.

---

## 📄 Files

| File | Role |
|------|------|
| [`ARIA_INTEL_Research_Paper.md`](ARIA_INTEL_Research_Paper.md) | Full research paper — theoretical foundations, PMBM filter, MOU motion models, rendezvous warning, tradecraft detector registry, validated performance |
| [`ARIA_INTEL_README.md`](ARIA_INTEL_README.md) | Implementation / usage README |
| [`aria_intel.py`](aria_intel.py) | Python reference implementation (the paper references the v6 file under the name `aria_intel_v6.py` — same engine, ~2 363 lines, Python 3.10+) |

---

## 🏗 Architecture (per §1 of the paper)

ARIA-INTEL operationalises the state-of-the-art within the Random Finite Set framework — specifically the **Poisson Multi-Bernoulli Mixture (PMBM)** filter (Williams 2015; García-Fernández et al. 2018) — and extends it with a suite of intelligence-specific subsystems:

1. **PMBM filter** — theoretically optimal multi-target Bayesian estimator under the RFS framework. Decomposes into a Poisson Point Process over undetected targets and a Multi-Bernoulli Mixture over detected targets.
2. **Mixed Ornstein-Uhlenbeck (MOU) motion models** — continuous-time mean-reverting Gauss-Markov processes (Coraluppi et al.; Williams 2015), bounded position variance suitable for long-horizon intelligence scenarios. Per-domain MOU model bank with an IMM-style particle mixture.
3. **Pattern-of-Life (PoL) modelling** — Gaussian-mixture model of routine behaviour against which deviations are scored.
4. **Three-method 30-minute rendezvous warning architecture** — stacked detection of multi-actor rendezvous events with a ~30-minute lead-time horizon.
5. **Composable tradecraft detector registry** — pluggable detectors for cleanup-route patterns, surveillance detection, dead-drop signatures, etc.
6. **Dempster-Shafer multi-modal evidence fusion** — DST over GEOINT / SIGINT / COMMS / HUMINT / OSINT with modality-calibrated reliability priors.
7. **Possibility-theoretic existence track** — dual Bayesian (r) and possibilistic (π_r) existence estimates; their divergence flags deception or model failure (Houssineau & Bishop 2019).
8. **Domain-polymorphic configuration layer** — single configuration object retargets the engine across HUMINT, maritime, airspace, convoy domains.

---

## 📊 Validated performance (paper §10)

| Metric | Result |
|--------|--------|
| Median scan latency (single CPU core, no GPU) | **28 ms** |
| Rendezvous detection (across 20 independent scenarios) | **100 %** |
| Mean rendezvous lead time | **28.1 minutes** |
| Target confirmation at low detection probability (P_D = 0.40) | **100 %** |
| False alarm rate (at 40 clutter returns/scan) | **0.098 per scan** |

---

## 🧮 Theoretical foundations referenced

- **Random Finite Sets** (Mahler 2003, 2007) — set-valued multi-target state representation.
- **PMBM filter** (Williams 2015; García-Fernández et al. 2018) — conjugate prior for the multi-target Bayes filter; exact closed-form solution to a problem PHD/CPHD only approximate.
- **Ornstein-Uhlenbeck process** (Uhlenbeck & Ornstein 1930) — continuous-time mean-reverting Gauss-Markov.
- **Mixed OU** (Coraluppi et al.; Williams 2015) — drift on both position and velocity.
- **Dempster-Shafer Theory** (Shafer 1976) — multi-modal evidence fusion.
- **Possibility theory** (Zadeh 1978; Dubois & Prade 1988; Houssineau & Bishop 2019) — possibility-PMBM extension.

---

## 🚧 Honest framing

- All benchmark scenarios are **synthetic** with controlled clutter and detection-probability profiles; the paper does not claim live operational deployment results.
- The 28 ms latency is on a single CPU core for the documented test rig; real-world latency depends on sensor cadence and configuration.
- The system is **edge-deployable** by design (no GPU, single-file engine), not a competitor to large fusion-centre architectures.
- The paper is independent research, not a procurement document.

---

## 🔗 Related work in this repo

- [`Filtering/`](../Filtering/) — GH-SR-IMM robust tracking filter; complementary single-target / multi-target framework using IMM with Generalised-Hyperbolic noise instead of PMBM
- [`ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — **independent system** with the same "ARIA" prefix (Algebraic Resynchronisation and Integrity Architecture, an AEAD cipher). Different acronym, different folder, no algorithmic dependency.
- [`Veritas/`](../Veritas/) — formal verification framework, relevant for certifying tracker decisions
- [`RNGS/`](../RNGS/) — random-number generation primitives used in stochastic motion models
- [`Statistical Generation/`](../Statistical%20Generation/) — heavy-tailed and combinatorial statistical generation theory

---

[← Back to main README](../README.md)
