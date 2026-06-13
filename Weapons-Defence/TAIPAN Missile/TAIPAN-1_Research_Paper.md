# TAIPAN-1 — Design Validation Research Paper

**Classification:** Unclassified design study  
**Revision:** 1.0  
**Date:** 2026  
**Status:** Synthesis of simulation-verified technical specification  

---

## Abstract

TAIPAN-1 is a single-stage, liquid-propellant guided ballistic interceptor rocket optimised for minimum unit cost and maximum range from a compact mobile launch platform. This paper synthesises the simulation-verified performance claims from the TAIPAN-1 engineering documentation suite — technical specification Rev 1.0, geometry reference, and financial analysis — as validated by the standalone `taipan1_sim.py` trajectory toolkit. At the design point (14 kg tungsten nose ballast, 70.4° launch angle, 50 kN RP-1/LOX electric pump-fed engine), the 3-DOF point-mass model predicts **1 618 km maximum range**, **Mach 13.27 peak velocity**, and **367 km apogee** from a 630.8 kg wet / 109.0 kg dry vehicle (mass ratio 5.787). Production unit cost is projected at **$50k–$80k USD** at 50+ units — 22–37× below AIM-120D AMRAAM at comparable mission utility. All performance figures are model predictions; no instrumented flight test data exists.

---

## 1. Introduction

Conventional guided interceptors (AMRAAM, Tamir, THAAD) trade cost against range through turbopump-heavy propulsion and conventionally fabricated airframes. TAIPAN-1 inverts this trade by adopting Rocket Lab Rutherford-inspired electric pump-fed propulsion (62 kg dry engine vs ~325 kg conventional at 50 kN) and a 14-part 3D-printed airframe, raising mass ratio from 2.11 to 5.79 and more than doubling achievable Δv.

## 2. Simulation framework

Validation uses `taipan1_sim.py`:
- **Atmosphere:** US Standard Atmosphere 1976 (0–86 km)
- **Propulsion:** RP-1/LOX thermochemistry (γ = 1.235, O/F = 2.56), altitude-corrected thrust
- **Aerodynamics:** Barrowman CP + semi-empirical four-component drag (subsonic/transonic/supersonic)
- **Trajectory:** 3-DOF point-mass gravity turn, explicit Euler dt = 0.05 s
- **Stability:** Barrowman SM in calibers; design burnout SM = **1.57 cal** (marginal vs 1.5 cal minimum)

See [`SIM_README.md`](SIM_README.md) for full module map and CLI usage.

## 3. Verified performance summary

| Parameter | Value | Source |
|---|---|---|
| Maximum range | 1 618 km | `taipan1_sim.py --sim verify` |
| Apogee | 367 km | Same |
| Peak Mach | 13.27 | Same |
| Wet / dry mass | 630.8 / 109.0 kg | Mass model |
| Mass ratio | 5.787 | Tsiolkovsky |
| Ideal Δv | 5 046 m/s | Engine model |
| Burnout velocity efficiency | 79 % | Trajectory (21 % gravity + drag loss) |

### Ballast envelope

| Ballast (kg) | Range (km) | Max Mach | SM @ burnout |
|---|---|---|---|
| 14 (design) | 1 618 | 13.27 | 1.57 cal |
| 80 | 1 135 | 10.96 | 5.87 cal |
| 150 | 739 | 8.98 | 7.90 cal |
| 250 | 432 | 7.15 | 9.37 cal |

## 4. Cost validation cross-check

Financial analysis (Rev 1.0) bottom-up BOM supports prototype $90k–$170k and production $50k–$80k at 50+ units, consistent with 3D-printed airframe labour (~80–120 h first unit) and electric-pump engine cost structure benchmarked against Rutherford.

## 5. Limitations

- **3-DOF only** — no AoA dynamics, Earth rotation, wind, or structural flexibility
- **Burnout SM marginal** — manufacturing tolerance on aft mass could drop below 1.5 cal; 20 kg ballast recommended unless max range required
- **Aerothermal re-entry unanalysed** — Mach 13+ nose heating requires TPS study before flight qualification
- **Engine black-box** — injector sizing, cooling channels, pump detail design are future work

## 6. Conclusions

Simulation validates TAIPAN-1 as a credible low-cost long-range interceptor concept at the systems-modelling level. Flight test, 6-DOF verification, and engine detail design remain open. The design point delivers 16× the originally required 100 km range, providing a configurable engagement envelope by nose ballast alone.

---

## References (companion documents)

| Document | File |
|---|---|
| Technical specification | [`TAIPAN-1_Technical_Specification_Rev1.0.md`](TAIPAN-1_Technical_Specification_Rev1.0.md) |
| Geometry reference | [`TAIPAN-1_Geometry_Reference_Rev1.0.md`](TAIPAN-1_Geometry_Reference_Rev1.0.md) |
| Financial analysis | [`TAIPAN-1_Financial_Analysis_Rev1.0.md`](TAIPAN-1_Financial_Analysis_Rev1.0.md) |
| Simulation suite | [`SIM_README.md`](SIM_README.md), [`taipan1_sim.py`](taipan1_sim.py) |

---

*TAIPAN-1 research synthesis — for design study use only. Not engineering certification.*
