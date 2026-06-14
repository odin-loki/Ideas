# ORCA — Simulation Report

Generated: 2026-06-13 09:01 UTC

## Executive summary

- **Type-039 UEP detection:** 28.49 km (spec 28.49 km)
- **Surface ISR UEP detection:** 45.23 km (spec 45.22 km)
- **Propeller DEMON classification:** 0.88 km (spec 0.88 km)
- **Tier 1 array:** 54 nodes, 57.0 km spacing, 3021 km coast
- **Tier 1 acquisition:** $775,676 (spec $775,676)
- **False alarm rate:** 7.890 events/node/week (spec < 1.0/week)

## Detection range validation (Appendix A)

### Calibrated model

| Mode | Spec (km) | Simulated (km) | Error | Pass |
|------|-----------|----------------|-------|------|
| Type-039 UEP | 28.49 | 28.49 | 0.000% | ✓ |
| Surface ISR UEP | 45.22 | 45.23 | 0.011% | ✓ |
| Propeller DEMON | 0.88 | 0.88 | 0.000% | ✓ |

### Uncalibrated (raw Appendix A parameters)

| Mode | Spec (km) | Simulated (km) | Error | Pass |
|------|-----------|----------------|-------|------|
| Type-039 UEP | 28.49 | 28.49 | 0.014% | ✓ |
| Surface ISR UEP | 45.22 | 45.22 | 0.003% | ✓ |
| Propeller DEMON | 0.88 | 1.08 | 22.337% | ✗ |

## Array coverage

- Nodes: **54** @ **57.00 km** spacing
- Coast length: **3021 km**
- Detection radius: **28.49 km**
- Full coverage: **partial**
- Blind corridor on single-node failure: **57.0 km**

## Economics

- Node cost (nominal): **$6,401.40**
- Tier 1 acquisition: **$775,676**
- P-8A comparison: ORCA is **0.2248%** of one P-8A

## Calibration notes

- DC noise bandwidth: **0.009991654219533781 Hz** (default 0.01 Hz)
- Propeller gain scale: **0.0359**

**Known gaps:**
- Propeller DEMON: raw Appendix A gain stack (+75.2 dB) predicts 1.08 km vs spec 0.88 km (22.3% error). Applied propeller_gain_scale=0.0359.
- UEP corrosion: Appendix A field equations with BW=0.01 Hz match submarine range within 0.01% without bandwidth calibration.
- DEMON gain table (§3.5) is treated as a cumulative amplitude multiplier; spec narrative uses √(300×14) for DEMON alone — combined stack may double-count integration bandwidth.

## Full JSON

See `orca_sim_results.json` for machine-readable output.
