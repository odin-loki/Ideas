# Soldier-Portable MEMS Navigation Results

## System
Speed: 5 km/hr walking, 2-hour patrol, MEMS IMU 2°/hr drift

## Key architectural insight: separate speed from heading
PDR ZUPT approach: step-counter gives SPEED (σ≈3%, heading-independent).
Compass gives HEADING (σ=2°, also independent of IMU drift).
Combining them in the filter as separate scalar observations avoids the
heading-drift contamination that corrupts a combined [vn,ve] PDR velocity.

## Results

| Scenario | Filter | Mean (m) | P90 (m) | Max (m) | Hdg° |
|---|---|---|---|---|---|
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
| Mixed (Open→Urban→Open) | GH+PDR+compass | 29.8 | 47.9 | 65.4 | 0.57 |
| Mixed (Open→Urban→Open) | GH compass only | 154.9 | 246.8 | 518.8 | 0.57 |
| Mixed (Open→Urban→Open) | KF+PDR+compass | 48.1 | 63.3 | 82.1 | 0.73 |
| Mixed (Open→Urban→Open) | DR (PDR) | 102.7 | 236.5 | 285.5 | — |
| Mixed (Open→Urban→Open) | DR (raw MEMS) | 336.0 | 597.6 | 672.7 | — |

## Sensor suite (MEMS grade)
| Sensor | Ship (FOG/large) | Soldier (MEMS) |
|---|---|---|
| IMU drift | 0.05°/hr FOG | 2.0°/hr MEMS |
| Star fix | 70-100m | 350m (handheld, stop req.) |
| Pol compass | 0.5°, 0.5% blunder | 2.0°, 6% blunder |
| MagNav | 50-550m | 300m-unusable (urban) |
| PDR SPEED | N/A (ship) | σ≈3% of speed |
| Total power | ~50W | <2W |
| Total mass | ~30kg | <500g |

## vs GPS comparison
| Condition | Military GPS | Ship FOG v2 | Soldier MEMS |
|---|---|---|---|
| Open night (star fixes) | 1-3m | 30m | see results |
| Open day (overcast) | 3-5m | 30m | see results |
| Urban | 5-10m | N/A | see results |
| GPS jammed | 0 (fails) | 30-57m | unaffected |

## Findings
**Best accuracy: open terrain at night with star fixes every 15 min.**
Star fix (350m) + polarised compass (2°) dominate. PDR speed adds small improvement.
IMM model probability shows CA activating at each turn, HI briefly at sharp dynamics.

**Urban is the hard ceiling.** Magnetic disturbance (500+nT, rebar/vehicles) makes
MagNav unusable. Buildings block sky. Only PDR speed + compass remain.
Potential remedies: map-matching (road/building database), visual odometry (camera).

**MEMS vs FOG gap**: 40× worse drift rate but 2 mitigations:
1. PDR speed (heading-independent step count) constrains speed drift
2. Frequent position/heading fixes (every 15 min star, every 8 min MagNav attempt)
The filter gap vs ship (see numbers) is real but bounded — soldier system never jams.

**Silent/passive/unjammable preserved.** The <2W MEMS suite has no detectable RF
emission. No GPS receiver oscillator. Passively reads starlight, sky polarisation,
Earth's magnetic field. Operates inside Faraday cages, underground, underwater.