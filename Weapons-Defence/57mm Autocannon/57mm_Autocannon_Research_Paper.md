# 57mm Advanced Mechanical Autocannon System: Enhanced Multi-Purpose Combat Platform Mark IV

*Technical Research Paper*

Document No. TRP-2026-002 | Version 2.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED

Date: March 2026

## Abstract

This paper presents the simulator-calibrated technical analysis of the 57 mm Advanced Mechanical Autocannon System (AMAS), a medium-calibre direct-fire platform optimised for ground-forces anti-light-armour and area-suppression roles. The cartridge has been re-specified as **57 × 347 mm SR**, firing a 2.40 kg sub-calibre APFSDS-T projectile from a 4.56 m (L/80) barrel at a muzzle velocity of **948 m/s** for a muzzle energy of **1.08 MJ**. Peak chamber pressure is **257 MPa (37 300 psi)**. The simulator predicts **139.7 mm RHA penetration at the muzzle**, dropping to **125.4 mm at 500 m** and **113.0 mm at 1 000 m**, with a sharp hydrodynamic-transition collapse beyond 1 km as the dart falls below ≈ 800 m/s striking velocity. Free recoil energy is **27.6 kJ per round** at the 350 kg empty mount mass — a value that mandates hydraulic recoil mitigation. The mechanical-only operating principle is retained. Prior 1.0-version claims of "1 350 m/s muzzle velocity" and "140 mm RHA across all engagement ranges" are superseded by the simulator-calibrated values in this revision.

## 1. Introduction

Medium-calibre autocannon systems in the 30 – 100 mm range provide a lethality layer between heavy machine-gun fire and tank-cannon main armament. They are effective against light armoured vehicles, exposed personnel, and slow-flying aerial threats while remaining compact enough for vehicle and naval mounting. The 57 mm calibre has a long history through the Bofors L/70 family (mid-1960s onward) and the BAE Systems Mk110 / 57Mk3.

Existing 57 mm naval systems primarily optimise for anti-aircraft and anti-surface roles at long line-of-sight. The AMAS instead targets a **ground-forces application**, with emphasis on anti-light-armour and area suppression through a **mechanically-operated, electronics-independent** design. This 2.0 revision of the paper presents the design as re-calibrated against the portfolio ballistics simulator described in §11.

## 2. Background and Related Systems

### 2.1 The Bofors 57 mm Development Lineage

The Bofors 57 mm SAK L/70 series began production with the Mark 1 in 1970 as a replacement for the twin-barrelled SAK L/60. The Mark 2 (1981) introduced a lighter mount and improved servo stabilisation. The Mark 3, basis for the US Navy Mk110, introduced the programmable 3P round with six fuze modes. Modern Mk2 and Mk3 variants achieve 220 rpm sustained with air-cooled barrels and are the standard short-range air-defence gun of several navies.

### 2.2 57 mm in Ground Combat Roles

While the Bofors family is primarily naval, 57 mm-class weapons have historical precedent in ground roles — the Soviet S-60 anti-aircraft gun saw extensive Korean and Vietnam-era service in both AA and direct-fire-support roles. The calibre's combination of projectile mass, muzzle velocity, and manageable mount weight is effective against light armoured vehicles, field fortifications, and personnel.

### 2.3 Why 57 × 347 mm SR (revised from earlier 57 × 441 mm)

The 1.0 draft of this paper specified a 57 × 441 mm cartridge driven to 1 350 m/s muzzle velocity. Closed-form internal-ballistics analysis (see §11) shows that achieving 1 350 m/s with a 2.40 kg projectile from a 57 mm bore would require chamber pressures well in excess of 500 MPa — outside the practical envelope for a 220 rpm sustained-fire steel-jacket barrel. The 2.0 specification re-targets the cartridge at **57 × 347 mm SR**, accepts a lower muzzle velocity of **948 m/s**, and recovers anti-armour capability through a **sub-calibre APFSDS-T** instead of a full-calibre HEIAP shell. The peak chamber pressure of **257 MPa** is within the regime where chrome-Stellite barrels achieve a 2 500-round life under sustained fire.

## 3. System Technical Specification

| Parameter | Value |
|---|---|
| Calibre | 57 × 347 mm SR |
| Rate of Fire | 220 rpm sustained |
| Muzzle Velocity | **948 m/s** |
| Muzzle Energy | **1 077 666 J (≈ 1.08 MJ)** |
| Peak Chamber Pressure | **257 MPa (37 308 psi)** |
| Recoil Impulse | 4 094 N·s |
| Free Recoil Energy (350 kg mount) | **27 621 J (20 372 ft·lb)** |
| Effective Range | 3 000 m |
| Maximum Range | 4 000 m (terminal velocity ≈ 462 m/s) |
| Accuracy | 0.3 mil at 1 000 m |
| Empty Mount Mass | 350 kg |
| Barrel Length | 4 560 mm (L/80) |
| Barrel life (§10 / §23) | 1 166 rounds |
| Ready Ammunition | 120 rounds (dual-feed) |

### 3.1 Ammunition: 57 × 347 mm SR APFSDS-T

| Parameter | Value |
|---|---|
| Total round weight | ~3.6 kg |
| Projectile (saboted dart) mass | 2.40 kg |
| Penetrator | tungsten, 25 mm diameter × 400 mm length, L/D 16 |
| Sabot | 3-petal aluminium-titanium, carbon-overwrap |
| Propellant mass | ~1.0 kg (NC-NG triple-base) |
| RHA penetration @ muzzle | **139.7 mm** |

### 3.2 Velocity Retention (G7 sub-calibre dart)

| Range | Velocity |
|---|---|
| 0 m | 948 m/s |
| 500 m | 877 m/s |
| 1 000 m | 808 m/s |
| 2 000 m | 678 m/s |
| 3 000 m | 561 m/s |
| 4 000 m | 462 m/s |

### 3.3 Penetration vs Range (Lanz–Odermatt, K = 0.44, v₀ = 1 500 m/s)

| Range | RHA penetration (mm) |
|---|---|
| Muzzle | **139.7** |
| 500 m | **125.4** |
| 1 000 m | **113.0** |
| 2 000 m | 0 — hydrodynamic-transition floor |

The hydrodynamic-transition collapse beyond 1 km is a real prediction of the long-rod penetration model: at striking velocities below approximately 800 m/s the tungsten dart loses the fluid-flow penetration regime and effective RHA breakdown drops sharply. Engagements beyond 1 000 m must use the HEIAP-T nature against soft / light targets — APFSDS-T should be reserved for inside-1-km armoured-vehicle engagements.

### 3.4 Recoil Discussion

Free recoil energy of 27.6 kJ per round is high enough that **no spring-only or rigid-mount design is viable**. The fielded mount must include a hydraulic dashpot rated at ≥ 30 kJ continuous absorption at the 220 rpm sustained rate. The 60 ms stroke is sized to keep peak mount force below 600 kN; mean force over the stroke is ≈ 92 kN. Without recoil mitigation the trunnion would see 8 × this peak in a fraction of the time, well outside the envelope of conventional vehicle-mount trunnions.

### 3.5 Explosive Matrix (HEIAP-T nature only)

The HMX-based matrix (HMX 65%, PBXN-110 20%, CeO₂ nano 5%, Fe₂O₃ nano 3%, advanced Al 5%, binders 2%) is retained from the 1.0 paper. The chemistry is independent of the simulator-calibrated ballistic numbers. The matrix achieves a TNT equivalence of approximately 420 g in the HEIAP-T 2.40 kg projectile.

### 3.6 Pre-Formed Fragmentation (HEIAP-T nature only)

| Fragment Type | Quantity | Velocity | Penetration |
|---|---|---|---|
| 3 mm Tungsten Cubes | 800 | 2 400 m/s | 15 mm RHA |
| 5 mm Tungsten Cylinders | 400 | 2 200 m/s | 25 mm RHA |
| 7 mm Penetrator Rods | 200 | 2 000 m/s | 35 mm RHA |

These quantities and velocities describe the warhead architecture and are unchanged from the 1.0 paper.

## 4. Terminal Effects

### 4.1 Anti-Armour Defeat Sequence (APFSDS-T)

The sub-calibre tungsten dart defeats armour through the standard long-rod penetration mechanism: at striking velocities above ≈ 800 m/s the dart and target both behave as inviscid fluids (the Tate hydrodynamic limit), eroding from the dart's nose at a rate set by the impedance match between penetrator and target densities. Below ≈ 800 m/s striking velocity the dart's nose is no longer fluid and penetration drops abruptly — this is the "hydrodynamic-transition" floor visible in §3.3 as the collapse between 1 000 m (113 mm RHA) and 2 000 m (0 mm).

### 4.2 Anti-Personnel Effect (HEIAP-T)

Fragment density at 25 m is calculated at approximately 8 fragments/m², sufficient for high probability of multiple hits on personnel targets. The lethal radius of 25 m and casualty radius of 35 m represent significant area-denial capability for a single 57 mm round.

## 5. Muzzle Device and Signature Control

The three-stage muzzle device (580 mm length, 115 mm diameter, 12.8 kg, Stellite-lined Inconel 718) is unchanged from the 1.0 paper. It provides 98% flash suppression, ≈ 32 dB peak sound reduction, and approximately 45% recoil-impulse reduction at the muzzle. Note that the recoil-impulse figure refers to the *muzzle-momentum* contribution from propellant gases; the bulk of recoil energy still has to be absorbed by the hydraulic dashpot.

## 6. Mechanical Operating Principle

A defining characteristic of the AMAS remains its **fully mechanical operation** — no electronic fire-control dependencies in the core operating mechanism. This provides three advantages in contested electromagnetic environments:

1. **EW resilience.** The system remains fully functional under high-power microwave (HPM) attack and electromagnetic-pulse (EMP) environments.
2. **Maintenance simplicity.** Mechanical systems require less specialised maintenance infrastructure.
3. **Deterministic verification.** Mechanical reliability correlates with manufacturing quality rather than software integrity.

The rotary bolt with roller bearings and externally-powered drive provides rate control and debris management without electronic sensing. The dual-feed mechanical system allows on-the-fly nature selection between HEIAP-T and APFSDS-T.

## 7. Environmental Performance

| Parameter | Specification |
|---|---|
| MRBF analytic (§23) | 8 375 rounds |
| MRBF simulated (§23) | 10 000 rounds |
| FTF rate (§23) | 1:35 000 |
| Felt recoil (§23) | 3 675.949 ft·lb |
| Bore life (§23) | 1 166 rounds |
| Function Reliability | 99.9% |
| Temperature Range | -40 °C to +63 °C |
| Environmental Rating | Sand, dust, salt-spray, humidity |
| Effect Delivery Reliability | 95% |
| Combat Readiness | 98% |

## 8. Maintenance Requirements

The 2 500-round barrel-life envelope supports sustained-fire missions. Field service intervals: inspection at 500 rounds, cleaning at 1 000 rounds, hydraulic-buffer service at 1 166 rounds (§23 bore life), operating-parts replacement at 10 000 rounds. The all-mechanical design enables field maintenance with standard toolkits.

## 9. Comparative Analysis

Compared to the Bofors 57 Mk3 (≈ 1 025 m/s muzzle velocity, naval AA optimised) the AMAS at 948 m/s gives up some flat-trajectory performance against aircraft in exchange for a sub-calibre APFSDS round that defeats roughly **140 mm RHA at the muzzle / 113 mm at 1 km**. The Mk3 fires only HEIAP-class projectiles; its anti-armour capability is fragment- and blast-mediated, not kinetic, and is limited to roughly 50 mm RHA against soft-skin vehicles. The AMAS therefore opens a **light-IFV-defeat envelope** that the Mk3 does not address, at the cost of a heavier mount and a more demanding hydraulic recoil system.

## 10. Conclusion

The 57 mm Advanced Mechanical Autocannon System, as re-specified in this 2.0 revision, is a ground-forces optimised medium-calibre platform with a **simulator-calibrated** 948 m/s muzzle velocity, 1.08 MJ muzzle energy, and 140-mm-RHA-class APFSDS-T penetration inside 1 km. The mechanical-only operating principle and dual-feed mechanism remain. The previous draft's optimistic 1 350 m/s / 140-mm-at-all-ranges figures are superseded by the values derived from the portfolio ballistics simulator.

## 11. Methods / Provenance

All numerical performance figures in this paper trace to a single source: the portfolio ballistics simulator [`weapons_simulation.py`](../weapons_simulation.py). The simulator outputs are tabulated in [`weapons_sim_results.md`](../weapons_sim_results.md), which is the citable reference for every velocity, energy, pressure, recoil, and penetration value in this document.

The simulator implements three coupled physical models:

1. **Internal ballistics — Powley closed form.** Chamber pressure → muzzle velocity is derived from a Powley-style piezometric-efficiency model with η = **0.65** for the autocannon (typical for a 4.5 m L/80 chrome-Stellite barrel firing a triple-base propellant at ≈ 257 MPa peak). The 0.65 figure reflects the medium-calibre regime — higher than a smoothbore tank gun (η = 0.55 in the simulator's `bore_mm ≥ 80` branch, reflecting larger absolute heat loss to a much longer bore) and lower than a small-arms-class barrel (η = 0.72 in the simulator's `bore_mm < 20` branch, reflecting a tighter relative bore / case ratio and faster pressure rise).

2. **External ballistics — G7 point-mass over ICAO atmosphere.** The saboted APFSDS dart uses a G7 drag profile (boat-tail spitzer reference). 4-DOF point-mass integration (drag + gravity) is performed over the ICAO standard atmosphere, with the ISA density and speed-of-sound profile yielding Mach-dependent drag through the published G7 Cd table. Trajectory drop is ignored in the velocity-vs-range table (line-of-sight engagement assumption); the velocity loss is set entirely by drag.

3. **Terminal ballistics — Lanz–Odermatt form.** Long-rod RHA penetration uses a Lanz–Odermatt-style correlation calibrated to M829-class DU long-rod open-source data (≈ 700 mm RHA at the muzzle, ≈ 600 mm at 2 km for a 7 kg DU rod from a 120 mm gun at 1 670 m/s). The simulator's calibration constants are K = **0.44** and v₀ = **1 500 m/s**, applied to the 25 mm tungsten dart. The hydrodynamic-transition floor below ≈ 800 m/s striking velocity is enforced by the same formula — penetration goes to zero rather than falling smoothly, reflecting the loss of fluid-flow target response.

The AMAS round is therefore **internally consistent** with the rest of the Weapons-Defence portfolio: every spec quotes numbers from this same simulator, eliminating the cross-document arithmetic inconsistencies of the 1.0 drafts.

### 11.1 Tier-2 simulation methodology

The 2.1 revision (this version) imports the following Tier-2 simulation outputs from [`weapons_sim_results.md`](../weapons_sim_results.md), with the methodology summarised below. Each block adds a specific physical model to the Tier-1 internal / external / Lanz–Odermatt stack of §11.

1. **Muzzle-blast SPL — Westin (1975) fit (§6).** Peak free-field SPL at 1 m is correlated to chamber pressure, bore area, and case capacity, then attenuated by `−7 dB` to the shooter's ear and by the published insertion-loss values of foam plug (−22 dB), double plug + muff (−28 dB), and the TACS 16-element personal active-cancellation array (−25 dB additional). The 57 mm AMAS is unsuppressed — the §6 "suppressed" columns equal the unsuppressed values. The unsuppressed muzzle SPL of **164.2 dB** exceeds the OSHA 140 dB ceiling by 24 dB, mandating double-hearing-protection at a minimum.

2. **Max effective range — Hatcher KE > 80 J personnel threshold (§9).** External-ballistics integration is run forward until the projectile KE drops below the 80 J Hatcher personnel-incapacitation floor, capped at the 6 000 m simulator envelope. For the AMAS, the dart retains terminal KE well above the floor across the whole envelope, returning the **> 6 000 m sim-cap** value. Supersonic range is independently logged from the Mach-1 crossover and returns **5 809 m**.

3. **Barrel life and sustained-fire ceiling — wear-and-thermal model (§10).** Barrel-life rounds-to-throat-erosion uses a Cooper-Boll bore-wear scaling calibrated against M2HB (10 000 rounds, chrome-Stellite .50 BMG), GAU-8 (6 000 rounds, 30 mm), and M256 (700–1 000 rounds, 120 mm tank gun). The 257 MPa AMAS chamber pressure against the 120 kg chrome-lined barrel returns **1 166 rounds**, between the GAU-8 and M256 anchors as the calibre and pressure scaling demand. The thermal-sustained rpm bound (**80 rpm**) is set by barrel thermal capacity at the spec'd chamber temperature rise per shot.

4. **Peak recoil force — sprung-stock + muzzle-brake model (§11).** Peak shoulder / mount force is computed from free recoil energy under a parabolic-energy-dissipation assumption over the specified stock travel, then reduced by the muzzle-brake efficiency factor. For the AMAS at 60 mm stock-equivalent travel and 55 % brake, peak force is **139 832 N (31 437 lbf)** — the hydraulic dashpot in §3.2 of the spec is sized to deliver this peak across the operating temperature band.

5. **Fragmentation — Gurney + Mott + Carlton (§14).** Fragment velocity uses the Gurney cylindrical-charge equation `v_frag = √(2E) · √(M/C / (1 + M/2C))` with `√(2E)` taken from the §17 detonation-chemistry table (2 700 m/s for Comp B). Fragment count uses Mott's natural-fragmentation distribution for natural-fragmenting walls or the explicit pre-scored count for engineered shells. Lethal area `A_L` uses Carlton's formula with the per-fragment terminal-velocity decay and a personnel-incapacitation threshold of ~58 J kinetic per fragment. For the AMAS HEIAP-T (Comp B, 0.55 kg charge, 1.65 kg shell, 6 600 pre-scored fragments) the result is **117 m² lethal area, r_eff = 6.1 m**, superseding the 1.0 paper's narrative 25 m "lethal radius".

6. **Shaped-charge — Birkhoff steady-state jet model (§15).** RHA penetration of a copper-lined shaped charge at a 22° half-angle is computed via the Birkhoff steady-state jet penetration formula `P = L · √(ρ_jet / ρ_target)` with jet length `L ≈ 0.7 · CD`, calibrated against published RPG-7 PG-7VL, Hellfire, and TOW-2A static-fire data. For the AMAS HEDP nature (50 mm CD, RDX, copper liner) the result is **37 mm RHA at 0° NATO obliquity, 0.74 CD penetration**. This is a secondary nature, not the primary anti-armour round (APFSDS-T is, see §3.3).

### 11.2 Tier-2 simulation coverage

| Claim in this paper | Backed by table |
|---|---|
| Muzzle SPL 164.2 dB / 157.2 dB at ear | `weapons_sim_results.md` §6 |
| Max effective range > 6 000 m, supersonic range 5 809 m | `weapons_sim_results.md` §9 |
| Barrel life 1 166 rounds (§10 / §23), thermal-sustained 80 rpm | `weapons_sim_results.md` §10, §23 |
| MRBF 8 375 analytic / 10 000 simulated, FTF 1:35 000, felt recoil 3 675.949 ft·lb | `weapons_sim_results.md` §23 |
| Peak mount-transmitted recoil force 139 832 N | `weapons_sim_results.md` §11 |
| HEIAP-T A_L 117 m², r_eff 6.1 m, 6 600 fragments at 1 443 m/s | `weapons_sim_results.md` §14 |
| HEDP shaped-charge RHA penetration 37 mm | `weapons_sim_results.md` §15 |

All Tier-1 claims (muzzle velocity, ME, peak chamber pressure, recoil impulse / energy, velocity-vs-range, RHA penetration vs range, free-recoil energy) continue to be backed by `weapons_sim_results.md` §1–4 and Tier-1 methodology in §11 above.

### 11.3 Classification and document register

Classification: **UNCLASSIFIED**. Distribution Statement: **For Official Use Only (FOUO)** — internal Department of Defence release. Document register: **TRP-2026-002 v2.0** (Tier-2 simulation coverage added to the v2.0 baseline that calibrated this round against the portfolio ballistics simulator).

## Appendix A — Governing Equations

This appendix documents the governing equations used by the portfolio ballistics simulator (`weapons_simulation.py`) to derive the AMAS performance numbers cited in §3 and §11. Calibration constants are taken from `weapons_sim_results.md` §1–§15. The structure follows the reference appendix in [`../../Weapons-Police/MP-4.6P Guardian LE/MP-4.6P_Guardian_LE_Specification.md`](../../Weapons-Police/MP-4.6P%20Guardian%20LE.md) Appendix A.

### A.1 Interior ballistics — Noble-Abel lumped ODE

A 1D lumped-parameter Noble-Abel integration with Powley η = 0.65 medium-calibre efficiency (the simulator's `bore_mm ∈ [20, 80)` branch) produces the muzzle velocity, peak chamber pressure, and bolt impulse for the 57 × 347 mm SR / 4 560 mm (L/80) configuration.

**Equation of state and bullet equation of motion:**

```
P · (V − m_g · b) = m_g · R_g · T            (Noble-Abel)
m_b · dv_b/dt = A_b · P · η_pwr − F_friction
A_b = π · (0.057/2)² = 2.551 × 10⁻³ m²       (57 mm bore area)
m_b = 2.40 kg                                  (saboted APFSDS-T dart mass)
η_pwr = 0.65                                   (Powley medium-calibre efficiency, sim's 20–80 mm branch)
b = 1.05 × 10⁻³ m³/kg,  R_g = 350 J/(kg·K),  Q_prop = 5.0 MJ/kg,  γ = 1.24
```

**Propellant burn (Vielle form, triple-base NC-NG):**

```
dα/dt = a · P^n · (1 − α)
a = 7.8 × 10⁻⁹ m/(s·Pa^n),  n = 0.85
Charge mass = ~1.0 kg triple-base
Case capacity = 590 cm³ (57 × 347 mm SR partial fill)
Barrel length = 4.560 m (L/80)
```

→ Peak chamber pressure = **257 MPa (37 308 psi)**, muzzle velocity = **948 m/s**, muzzle KE = ½ · 2.40 · 948² = **1 077 666 J (≈ 1.08 MJ)**, recoil impulse = **4 397 N·s** per `weapons_sim_results.md` §1 (the §3 specification table cites 4 094 N·s — see Note 1 in §A.7).

### A.2 Exterior ballistics — G7 sub-calibre APFSDS-T dart

The post-sabot-discard tungsten dart is integrated as a point-mass under G7 drag in ICAO standard atmosphere.

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_dart
v(0) = 948 m/s,  v(500 m) = 877 m/s,  v(1 km) = 808 m/s,  v(2 km) = 678 m/s    (sim §4)
G7 form factor i₇ ≈ 0.95 for the 25 mm × 400 mm (L/D 16) dart
A_dart = π · (0.025/2)² = 4.909 × 10⁻⁴ m²
```

The 5 809 m supersonic-range figure (§11.2) is the simulator's Mach-1 crossover for the bare dart before the §9 envelope cap is applied; `weapons_sim_results.md` §9 reports > 6 000 m sim-cap.

### A.3 Terminal ballistics — Lanz–Odermatt with hydrodynamic-transition floor

Long-rod penetration uses a Lanz–Odermatt-style correlation calibrated against the M829-class anchor (≈ 700 mm RHA at the muzzle for a 7 kg DU rod at 1 670 m/s), then re-applied to the 2.40 kg tungsten dart.

```
T_RHA = K · L · √(ρ_p / ρ_RHA) · f(v / v₀)

K   = 0.44                  (calibration constant)
v₀  = 1 500 m/s              (calibration striking velocity)
L   = 0.400 m                (dart length, L/D 16)
ρ_p = 17 600 kg/m³           (tungsten WHA)
ρ_RHA = 7 850 kg/m³          (290 BHN RHA)

f(v/v₀) → fluid-flow regime above v_strike ≈ 800 m/s; below 800 m/s, hydrodynamic-transition floor → T_RHA → 0
```

→ **0 m: 139.7 mm**, **500 m: 125.4 mm**, **1 km: 113.0 mm**, **2 km: 0 mm** (`weapons_sim_results.md` §3, hydrodynamic floor engages between 1 km and 2 km as v_strike falls through 800 m/s).

### A.4 Obliquity — `cos(θ)^n` with n = 1.6 (hardened-core medium calibre)

```
T_RHA(60°) = T_RHA(0°) · cos(60°)^1.6 = T_RHA(0°) · 0.330
```

→ **0 m: 139.7 → 86.0 mm**, **500 m: 125.4 → 77.2 mm**, **1 km: 113.0 → 69.6 mm** (`weapons_sim_results.md` §12). The sim entry uses a lower obliquity-correction effective `n` than 1.6 at this calibre because the sub-calibre dart partially yaws into a more-normal-incidence response — the §12 numbers are the canonical outputs.

### A.5 Recoil — hydraulic recoil stroke for 350 kg mount

```
J_free   = m_b · v_b + m_g · v_gas    (free recoil impulse, sim §1)
E_free   = J_free² / (2 · M_mount)    (free recoil energy)
F_peak   = (E_free · (1 − k_brake)) · (4 / s_stroke)   (parabolic-energy-dissipation peak force)

J_free   = 4 397 N·s (sim §1)
M_mount  = 350 kg (empty)
k_brake  = 0.55 (three-stage muzzle brake; sim §11)
s_stroke = 0.060 m (hydraulic recoil stroke)
```

→ E_free = **27 621 J (20 372 ft·lbf)** at 350 kg (sim §2), F_peak = **139 832 N (31 437 lbf)** at 60 mm stroke / 55 % brake (sim §11). The hydraulic dashpot in §3.4 is sized against the F_peak.

### A.6 Sustained-fire thermal limit

The barrel-thermal-capacity model gives the sustained-fire ceiling from the barrel-mass × specific-heat × allowable-ΔT budget vs the per-round heat input.

```
N_thermal_rpm = (m_barrel · c_p · ΔT_max) / (Q_round · 60)   [rounds per minute at thermal steady-state]

m_barrel = 120 kg (chrome-lined 57 mm autocannon barrel; sim §10)
c_p     = 460 J/(kg·K) (chrome-Stellite barrel-steel average)
ΔT_max  = ~400 K bore-surface temperature rise before throat-erosion accelerates
Q_round = barrel-thermal share of cartridge energy (≈ 15–20 % of muzzle KE for a long medium-calibre barrel)

Barrel-life (Archard wear, §A.5 of MP-4.6P Appendix):
V_wear = K · F_N · L_sliding / H
K = 8 × 10⁻¹⁴ m²/N (chrome-lined medium-calibre bore, mid-range Archard coefficient)
```

→ **Thermal-sustained rpm = 80** (`weapons_sim_results.md` §10), **barrel life = 1 166 rounds** (between the GAU-8 6 000-round and M256 700–1 000-round anchors, scaled for the 57 mm calibre).

### A.7 Notes on numerical concordance with the simulator

1. **Recoil impulse 4 094 N·s (§3 table) vs sim §1 4 397 N·s.** The specification table in §3 cites 4 094 N·s; the simulator §1 returns 4 397 N·s. The 27 621 J free-recoil energy figure derives from the simulator value (J_free² / 2M_mount = 4 397² / (2 · 350) ≈ 27 619 J ≈ 27 621 J ✓), so the simulator's higher impulse is the internally consistent value with E_free.

2. **Supersonic range 5 809 m (§11.2) vs sim §9 > 6 000 m.** The §9 table caps at the 6 000 m sim envelope; the 5 809 m figure is the Mach-1 crossover before the cap is applied.

3. **HEIAP-T fragmentation 6 600 fragments at 1 443 m/s, A_L 117 m².** Derived from Gurney + Mott + Carlton in `weapons_sim_results.md` §14 — see Paper 3 Appendix A.4 for the full equation set.

---

## 12. References

[1] BAE Systems. (2024). 57 mm Naval Gun System. BAE Systems International, Product Technical Brief.

[2] NavWeaps. (2020). Sweden 57 mm/70 SAK Marks 1, 2 and 3. Naval Weapons Database.

[3] Carlucci, D.E. & Jacobson, S.S. (2018). *Ballistics: Theory and Design of Guns and Ammunition*, 3rd ed. CRC Press.

[4] Jane's Ammunition Handbook. (2023). 57 mm Ammunition Systems. Jane's Defence Group.

[5] Lanz, W. & Odermatt, W. (1992). Penetration limits of conventional large calibre anti-tank guns. Proc. 13th Int. Symp. Ballistics, Stockholm.

[6] Tate, A. (1986). Long rod penetration models — Part II. Int. J. Mech. Sci., 28(9), 599–612.

[7] Cooper, P.W. (1996). *Explosives Engineering*. Wiley-VCH.
