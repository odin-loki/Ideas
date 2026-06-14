# AGINS — Simulation Report

Generated: 2026-06-13 08:57 UTC

## Executive summary

- **Soldier Open Terrain — Clear Night:** GH+PDR mean 25.9 m, P90 57.3 m
- **Soldier Open Terrain — Daytime Overcast:** GH+PDR mean 47.0 m, P90 65.3 m
- **Soldier Urban Patrol — Sky/Mag Denied:** GH+PDR mean 60.7 m, P90 91.2 m
- **Soldier Mixed (Open->Urban->Open):** GH+PDR mean 29.8 m, P90 47.9 m
- **Ship Maritime — Clear Sky Transit:** GH mean 36.5 m, P90 66.1 m
  - DR (FOG IMU): mean 217.8 m
- **Ship Maritime — 6hr Storm Conditions:** GH mean 56.1 m, P90 95.9 m
  - DR (FOG IMU): mean 217.8 m

## Soldier platform (MEMS)

| Scenario | Filter | Mean (m) | P90 (m) | Max (m) | Hdg° |
|----------|--------|----------|---------|---------|------|
| Open Terrain — Clear Night | GH+PDR+compass | 25.9 | 57.3 | 66.5 | 0.48 |
| Open Terrain — Clear Night | GH compass only | 65.9 | 161.5 | 211.7 | 0.48 |
| Open Terrain — Clear Night | KF+PDR+compass | 59.4 | 108.0 | 118.2 | 0.59 |
| Open Terrain — Clear Night | DR (PDR) | 102.7 | 236.5 | 285.5 | — |
| Open Terrain — Clear Night | DR (raw MEMS) | 336.0 | 597.6 | 672.7 | — |
| Open Terrain — Daytime Overcast | GH+PDR+compass | 47.0 | 65.3 | 76.3 | 0.59 |
| Open Terrain — Daytime Overcast | GH compass only | 143.2 | 238.4 | 259.7 | 0.59 |
| Open Terrain — Daytime Overcast | KF+PDR+compass | 54.5 | 71.8 | 82.5 | 0.75 |
| Open Terrain — Daytime Overcast | DR (PDR) | 102.7 | 236.5 | 285.5 | — |
| Open Terrain — Daytime Overcast | DR (raw MEMS) | 336.0 | 597.6 | 672.7 | — |
| Urban Patrol — Sky/Mag Denied | GH+PDR+compass | 60.7 | 91.2 | 106.5 | 1.04 |
| Urban Patrol — Sky/Mag Denied | GH compass only | 231.2 | 470.2 | 557.3 | 1.01 |
| Urban Patrol — Sky/Mag Denied | KF+PDR+compass | 75.7 | 97.5 | 113.8 | 1.44 |
| Urban Patrol — Sky/Mag Denied | DR (PDR) | 102.8 | 237.1 | 286.0 | — |
| Urban Patrol — Sky/Mag Denied | DR (raw MEMS) | 335.1 | 594.8 | 668.2 | — |
| Mixed (Open->Urban->Open) | GH+PDR+compass | 29.8 | 47.9 | 65.4 | 0.57 |
| Mixed (Open->Urban->Open) | GH compass only | 154.9 | 246.8 | 518.8 | 0.57 |
| Mixed (Open->Urban->Open) | KF+PDR+compass | 48.1 | 63.3 | 82.1 | 0.73 |
| Mixed (Open->Urban->Open) | DR (PDR) | 102.7 | 236.5 | 285.5 | — |
| Mixed (Open->Urban->Open) | DR (raw MEMS) | 336.0 | 597.6 | 672.7 | — |

## Ship platform (FOG)

| Scenario | Filter | Mean (m) | P90 (m) | Max (m) | Hdg° |
|----------|--------|----------|---------|---------|------|
| Maritime — Clear Sky Transit | GH+compass | 36.5 | 66.1 | 91.6 | 0.19 |
| Maritime — Clear Sky Transit | KF+compass | 50.0 | 83.9 | 115.3 | 0.26 |
| Maritime — Clear Sky Transit | DR (FOG IMU) | 217.8 | 374.1 | 411.3 | — |
| Maritime — 6hr Storm Conditions | GH+compass | 56.1 | 95.9 | 122.2 | 0.27 |
| Maritime — 6hr Storm Conditions | KF+compass | 69.8 | 123.1 | 154.8 | 0.32 |
| Maritime — 6hr Storm Conditions | DR (FOG IMU) | 217.8 | 374.1 | 411.3 | — |

## Spec targets (AGINS_full_report.md)

| Platform | Scenario | Target mean | Target P90 |
|----------|----------|-------------|------------|
| Ship | Clear sky | 30 m | 50 m |
| Ship | Storm | 57 m | 91 m |
| Ship | DR only | 206 m | — |
| Soldier | Open night | 26 m | 57 m |
| Soldier | Urban | 61 m | 91 m |

## Full JSON

See `agins_sim_results.json` for machine-readable output.
