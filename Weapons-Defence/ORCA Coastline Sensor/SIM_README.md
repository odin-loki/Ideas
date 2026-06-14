# ORCA — simulation guide

**Dedicated platform simulation** via the local [`orca_sim_package/`](orca_sim_package/) suite. ORCA models DC corrosion-field detection range, propeller DEMON classification range, 54-node array coverage geometry, and Tier 1 economics from the dipole physics in [`papers/ORCA_System_Specification.md`](papers/ORCA_System_Specification.md) Appendix A.

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the full `orca_sim` package and prints headline numbers. Use this from the platform folder root:

```bash
python platform_simulation.py
python platform_simulation.py --json
```

Full suite (same engine, more verbose):

```bash
cd orca_sim_package
pip install -r orca_sim/requirements.txt
python run_all.py
```

Outputs land in [`orca_sim_package/orca_sim/outputs/`](orca_sim_package/orca_sim/outputs/):

| File | Role |
|---|---|
| `orca_sim_report.md` | Human-readable consolidated report |
| `orca_sim_results.json` | Machine-readable full results |

---

## Requirements

```bash
pip install numpy scipy matplotlib
```

Python 3.9+ required. Matplotlib is optional (coverage-map plots only).

---

## Simulation modules

| Module | Path | Models |
|---|---|---|
| **Corrosion field** | `physics/corrosion.py` | Lateral dipole field E(r) = M / (4πσ(r²+Δz²)^(3/2)); baseline voltage V = E × D |
| **Propeller field** | `physics/propeller.py` | Quasi-static oscillating dipole with skin depth δ(f); harmonic roll-off 1/k^1.5 |
| **Detection range** | `detection/range.py` | 10 dB SNR threshold solver; matched-filter noise V_noise = √2·σ_e·√BW/√N |
| **Matched filter** | `processing/matched_filter.py` | 3-pair star geometry, √N coherent gain, bearing estimation |
| **DEMON** | `processing/demon.py` | Cyclostationary 300 s integration, blade-rate fingerprint |
| **Array coverage** | `array/coverage.py` | Node spacing = 2×r_detect; ceil(3000/57)+1 = 54 nodes |
| **Economics** | `economics/tier1.py` | Acquisition rollup ($775,676), annual ops ($298,797), P-8A comparison |
| **Report** | `reports/generate.py` | Markdown + JSON export *(invoked by `run_all.py`)* |

All parameters live in [`orca_sim_package/orca_sim/config.py`](orca_sim_package/orca_sim/config.py).

---

## Cross-portfolio references

| Subsystem | Portfolio folder | Sim role |
|---|---|---|
| GH-SR-IMM filter | [`../../Filtering/`](../../Filtering/) | Shore-station track correlator (Kalman on multi-node events) |
| ARIA-INTEL | [`../../Asset Tracking Algorithm/`](../../Asset%20Tracking%20Algorithm/) | Maritime domain-awareness adjacency |
| Leviathan (coastal defence platform) | [`../Leviathon Tank/`](../Leviathon%20Tank/) | Amphibious AFV that would operate in ORCA-cued areas |
| P-8A cueing doctrine | [`papers/ORCA_System_Specification.md`](papers/ORCA_System_Specification.md) §10.6 | ORCA detects at 28 km; P-8A diverts for acoustic ID |

### Physics — dual documentation track

The specification Appendix A documents the closed-form dipole model used for headline ranges. The **`orca_sim` package** re-implements that model for reproducibility and sensitivity sweeps (dipole moment, electrode noise, integration time). Cite **this package** for simulation-verified numbers; cite the **specification** for node architecture, BOM, and deployment doctrine.

---

## Headline numbers (default run)

| Metric | Value |
|---|---|
| **Submarine — UEP (Type-039)** | **28.49 km** @ 10 dB SNR |
| **Surface vessel — UEP (6,000 A·m)** | **45.22 km** @ 10 dB SNR |
| **Submarine — propeller (DEMON)** | **0.88 km** (classification only) |
| Node spacing (100% coverage) | **57 km** |
| Tier 1 node count | **54** |
| Coastline length | **3,000 km** |
| Electrode baseline | **200 m**, 3 independent pairs |
| Electrode noise (DC) | **1 nV/√Hz** |
| Integration (DC / DEMON) | **60 s** / **300 s** |
| Tier 1 acquisition | **$775,676** |
| Annual operating cost | **$299k/year** (rounded) |
| vs P-8A acquisition | **0.019%** |
| Per-node cost (production 500+) | **~$4,160** |

---

## Known model limitations

1. **Homogeneous half-space** — No bathymetric refraction, sediment conductivity layering, or continental-shelf geometry effects.
2. **Fixed dipole moments** — Type-039 M = 1,500 A·m and surface vessel M = 6,000 A·m are catalogue values; cathodic-protection state and hull condition not swept.
3. **No biofouling degradation** — Electrode noise floor assumed stable; fouling would raise noise and shrink range.
4. **No oceanographic MHD background** — Tidal MHD fields are modelled as common-mode rejected; extreme events not simulated.
5. **Propeller skin depth only** — ELFE range capped by δ ≈ 67 m at 14 Hz; DEMON extends classification marginally beyond raw field detectability.
6. **Economics are Tier 1 only** — Tier 2 corridor nodes and export pricing not in default `run_all.py` output.
7. **No field trial calibration** — All ranges are model-derived; Phase 2 ocean trials in spec roadmap are not yet reflected in sim outputs.

Re-run after editing `config.py` and update [`papers/ORCA_System_Specification.md`](papers/ORCA_System_Specification.md) Appendix A to match.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)
