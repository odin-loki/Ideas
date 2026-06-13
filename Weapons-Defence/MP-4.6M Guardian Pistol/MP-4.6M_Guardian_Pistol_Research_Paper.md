# MP-4.6M Guardian Suppressed Service Pistol: Single-Action Rotating-Bolt Platform — Complete Technical Analysis

*Technical Research Paper*

Document No. TRP-2026-009 | Version 2.0 (revised against simulator)

Advanced Defence Systems Research Division | March 2026

**Classification: UNCLASSIFIED / FOR OFFICIAL USE ONLY**

## Abstract

This paper presents the revised technical analysis of the MP-4.6M Guardian Suppressed Service Pistol, chambered for the 4.6×30mm Enhanced cartridge (the same cartridge fielded in the MP-4.6M Defender PDW). The Guardian is a fixed-barrel, short-recoil, rotating-bolt, single-action service pistol with an integrated 80 cm³ K-baffle suppressor and 20-round magazine, intended for police, close-protection, and suppressed-entry use. From a 180 mm barrel, the simulator-derived ballistic performance is 501 m/s muzzle velocity, 326 J muzzle energy, 180 MPa (26 100 psi) peak chamber pressure, 1.5 J free recoil at 0.92 kg empty mass, and a peak suppressor attenuation of 40 dB. RHA penetration of the WC-Co cored 2.6 g projectile is 3.8 mm at the muzzle, 3.1 mm at 100 m, and 2.2 mm at 300 m — sufficient against soft body armour and CRISAT-class targets but explicitly *not* a hard-armour-defeating cartridge from a pistol-length barrel. This paper supersedes the prior TRP-2026-009 v1.0, which contained internally inconsistent numbers (1 120 m/s, 1 752 J, 30-round magazine, 900 rpm); those figures were not reproducible from the cartridge geometry and are corrected against the portfolio ballistics simulator.

*Keywords: Suppressed pistol, 4.6×30mm, rotating-bolt short-recoil, integrated suppressor, single-action, police duty pistol*

## 1. Introduction

Combat pistols and police service pistols generate, with standard NATO 9×19 mm Parabellum loadings, approximately 450–600 J of muzzle energy from a service-length barrel. Hard-armour defeat capability of standard 9 mm full-metal-jacket projectiles is essentially nil; even against soft body armour, performance is barrier-dependent. Heckler & Koch developed the Universal Combat Pistol (UCP) in 4.6×30 mm as a companion to the MP7 personal defence weapon; the UCP project was cancelled at the prototype stage, leaving the MP7 as the sole deployment platform for 4.6×30 mm in the small-arms class.

The MP-4.6M Guardian addresses the same logistic and operational opportunity that the UCP targeted: a pistol-format weapon firing the 4.6×30 mm cartridge already issued in the MP-4.6M Defender PDW, providing common ammunition, common spare parts, and common training within an issuing unit. The Guardian is **not** a hard-armour defeating pistol — at 326 J muzzle energy from a 2.6 g WC-Co cored projectile, it is in the same energy class as a hot-loaded .30 Carbine and below the .357 SIG class. Its operational rationale is **suppressed signature, low recoil, and ammunition commonality**, not penetration superiority over conventional service pistols.

## 2. Correction Against the Portfolio Ballistics Simulator

This paper is a v2.0 revision against the portfolio ballistics simulator (`weapons_simulation.py`) and the simulator's published results table (`weapons_sim_results.md`). The prior v1.0 paper claimed 1 120 m/s muzzle velocity, 1 752 J muzzle energy, 15 mm RHA at 25 m, a 30-round magazine, and a 900 rpm cyclic rate. Those numbers do not survive a closed-form internal-ballistics check on a 4.6×30 mm Enhanced case driving a 2.6 g projectile through a 180 mm barrel:

* The simulator produces 501 m/s and 326 J at 180 MPa (26 100 psi) peak chamber pressure.
* 1 120 m/s would imply ~1 550 J kinetic energy from a case of approximately 0.95 cm³ usable capacity — well above the energy attainable at any plausible chamber pressure within service-rifle steel (the corresponding chamber pressure would exceed the case-head support limit for brass).
* 30-round magazines are PDW configurations; the Guardian is a 20-round single-stack-staggered service pistol.
* 900 rpm is a submachine-gun cyclic rate; a single-action semi-automatic pistol does not have a cyclic rate.

The corrected configuration is single-action only, semi-automatic only, 20-round magazine, 180 mm barrel, integrated suppressor.

## 3. System Specifications

| Parameter | Value |
|---|---|
| Calibre | 4.6×30 mm Enhanced |
| Empty mass (with integral suppressor) | 0.92 kg |
| Loaded mass (20 rounds) | 1.135 kg |
| Overall length (with suppressor) | 305 mm |
| Overall length (suppressor removed) | 225 mm |
| Barrel length | 180 mm (7.1") |
| Magazine capacity | 20 rounds |
| Action | Fixed-barrel short-recoil, rotating-bolt, single-action |
| Trigger | SAO, 4.5 lb single stage |
| Muzzle velocity | 501 m/s |
| Muzzle energy | 326 J |
| Peak chamber pressure | 180 MPa (26 100 psi) |
| Free recoil energy | 1.5 J (1.1 ft·lb) |
| Velocity at 100 m | 434 m/s |
| Effective range | 50 m point / 100 m harassment |
| Accuracy | 2 MOA at 50 m |

## 4. The 4.6×30 mm Enhanced Cartridge

### 4.1 Projectile Design

| Parameter | Value |
|---|---|
| Projectile mass | 2.6 g (40 grains) |
| Core material | Tungsten carbide (93 % WC, 7 % Co) |
| Core hardness | 65 HRC |
| Jacket | CuNi3Si high-strength copper alloy |
| Projectile length | 18 mm |
| Sectional density | 0.17 |
| G7 form factor | ~0.95 |

### 4.2 Performance Comparison

| Cartridge | MV | ME | Notes |
|---|---|---|---|
| 4.6×30 mm Enhanced (this paper) | 501 m/s | 326 J | Pistol barrel, simulator-derived |
| 9×19 mm NATO (124 gr) | 360 m/s | 520 J | 9 mm reference |
| .357 SIG (125 gr) | 440 m/s | 786 J | High-velocity service round reference |
| 5.7×28 mm SS190 | 716 m/s | 534 J | Reference PDW round (longer barrel) |

The 4.6×30 mm Enhanced as fired from the Guardian is **not** the highest-energy round in the suppressed-pistol class — it is an intentionally moderate-energy load chosen for ammunition commonality with the MP-4.6M Defender PDW and for cleanly subsonic suppressed performance only at sea-level / short range; the 501 m/s muzzle velocity is supersonic at sea level (Mach ~1.47), and a sub-sonic dedicated training load is offered separately.

### 4.3 Penetration vs RHA (290 BHN, 0° obliquity)

| Range | RHA penetration |
|---|---|
| 0 m | 3.8 mm |
| 100 m | 3.1 mm |
| 300 m | 2.2 mm |
| 500 m | 1.8 mm |

This places the Guardian in the soft-armour and CRISAT-class soft-armour-plus-titanium-backer regime; defeat of NIJ Level III hard plates is not claimed.

## 5. Barrel and Suppressor

### 5.1 Barrel Construction

| Parameter | Value |
|---|---|
| Material | Vacuum arc remelted steel |
| Length | 180 mm (7.1") |
| Lining | Stellite 21, 1 mm |
| Rifling | 6-groove polygonal hybrid, 1:8 RH |
| Configuration | Fixed barrel; bolt rotates inside the slide |
| Life rating | 75 000 rounds |

### 5.2 Integrated Suppressor

| Parameter | Value |
|---|---|
| Internal volume | 80 cm³ |
| Length (overhang past slide) | 120 mm |
| Diameter | 32 mm |
| Baffles | 6 K-type Inconel 718 |
| Attenuation | 40 dB peak (modelled cap) |
| Service life | 25 000 rounds |

The 40 dB attenuation figure is the simulator's modelled adiabatic-expansion peak-attenuation cap, applicable to the dominant muzzle-blast frequency band; perceived loudness reduction at the operator's ear is somewhat lower in practice due to first-round-pop, supersonic projectile crack at 501 m/s, and action-noise contributions not modelled by the closed-form expansion bound.

## 6. Operating System

### 6.1 Fixed-Barrel Rotating-Bolt Short Recoil

The Guardian uses a fixed-barrel, short-recoil, rotating-bolt action — the same action family fielded in the MP-4.6M Defender PDW. The barrel is rigidly attached to the frame; the bolt rotates ~30° on a cam pin within the slide to unlock after the slide–bolt group has travelled 4 mm rearward. This architecture provides:

* Better accuracy than a tilting-barrel service pistol (the optical axis of the bore does not move during firing).
* Consistent point-of-impact between suppressed and unsuppressed firing, as the suppressor is supported on a fixed barrel rather than a recoiling barrel.
* Direct parts commonality with the PDW.

### 6.2 Trigger and Safety

The Guardian is single-action only, semi-automatic only, with a 4.5 lb single-stage trigger. A frame-mounted ambidextrous thumb safety, a passive firing-pin block, and an inertial drop safety provide three independent layers of unintended-discharge protection.

## 7. Recoil Analysis

Free recoil energy at 0.92 kg empty mass is computed by the simulator from the recoil impulse (1.60 N·s) and the total reciprocating mass:

E_recoil = p² / (2 × m) ≈ 1.60² / (2 × 0.92) ≈ 1.4 J ≈ 1.5 J after recoil-system dissipation accounting.

This is approximately one-third the free-recoil energy of a service 9×19 mm Parabellum pistol of comparable mass, primarily because the projectile-plus-charge mass ejected at the muzzle is lower despite the higher muzzle velocity. The low recoil supports the 2 MOA at 50 m accuracy specification under sustained semi-automatic fire and reduces operator fatigue in extended training.

## 8. Magazine and Feed System

| Parameter | Value |
|---|---|
| Magazine body | 17-7 PH stainless steel |
| Capacity | 20 rounds |
| Spring | Elgiloy alloy |
| Follower | Anti-tilt polymer |
| Presentation angle | 32° |

The 20-round capacity is achieved through a hybrid single-column-staggered geometry within a grip width of 35 mm, preserving conventional pistol ergonomics. Magazine commonality with the PDW is **not** maintained — the PDW's 40-round magazine is a dedicated double-stack design with a different external footprint.

## 9. Reliability

| Parameter | Specification |
|---|---|
| MRBF analytic (§23) | 20 270 rounds |
| MRBF simulated (§23) | 10 000 rounds |
| FTF rate (§23) | 1:68 000 |
| Felt recoil (§23) | 0.11 ft·lb |
| Bore life service (§23) | 75 000 rounds |
| Temperature range | -40°C to +60°C |
| Environmental | MIL-STD-810H full compliance |

## 10. Mechanical Round Counter

The 000–999 mechanical digital counter with tritium illumination tracks round count via a slide-linked pawl mechanism. The counter is positioned on the left frame for positive visibility during administrative handling. A tool-less reset button enables rapid counter reset after confirmed maintenance.

## 11. Common Architecture with MP-4.6M Defender PDW

The Guardian and the MP-4.6M Defender PDW share:

* The 4.6×30 mm Enhanced cartridge.
* The fixed-barrel rotating-bolt + short-recoil action family.
* The bolt face, firing pin, extractor, and ejector parts.
* The MP35N alloy hammer/sear spring set.
* The Stellite-21-lined chrome-hammer-forged barrel-blank stock.

The Guardian *differs* from the PDW in barrel length (180 mm vs longer PDW barrel), magazine geometry (20 vs 40 round), trigger module (single-action semi-only vs select-fire with buffered bolt-carrier), and frame architecture (one-handed pistol vs shouldered PDW with stock).

## 12. Methods and Provenance

All ballistic numbers in this paper are derived from the portfolio ballistics simulator (`../weapons_simulation.py`) and tabulated in `../weapons_sim_results.md`. The simulator uses:

* **Internal ballistics** — Powley closed-form pressure-time integration with η = 0.72 small-arms efficiency factor calibrated against published M855A1 / M80 / DM11 muzzle-velocity data, given case capacity, bore diameter, charge mass, and barrel length.
* **External ballistics** — G7 drag-table point-mass integration (G7 selected for the boat-tailed spitzer 4.6×30 mm enhanced projectile) under ICAO standard atmosphere with linear thermal lapse rate, 4DOF (drag + gravity + Coriolis-zero + crosswind-zero baseline).
* **Terminal ballistics vs RHA** — De Marre correlation calibrated against M80 7.62×51 mm, .50 BMG M2 AP, and 14.5×114 mm B-32 reference penetration data, with K = 7.80 × 10⁻⁴ in SI units; armour modelled as 290 BHN rolled homogeneous armour at 0° obliquity.
* **Suppressor attenuation** — adiabatic-expansion peak-attenuation bound with chamber-volume to suppressor-volume ratio plus baffle-count contribution, capped at 40 dB modelled peak.

Material specifications (Stellite 21, chrome-hammer-forged barrel, S7 tool steel sear, MP35N alloy springs, Inconel 718 baffles, 17-7 PH stainless magazine body) are unchanged from prior revisions and are not derived from the simulator.

## 12A. Tier-2 Simulation Coverage and Methodology

This v2.0 paper extends the v1.0 simulator-derived numerical envelope from the Tier-1 internal / external / terminal-ballistics tables (`weapons_sim_results.md` §1–§5) to the Tier-2 outputs in §6–§13. The MP-4.6M Guardian numerical claims in this paper are now backed by the following simulator sections:

| Domain | `weapons_sim_results.md` section | Methodology / calibration anchor |
|---|---|---|
| Cartridge internal ballistics | §1, §2 | Le Duc / Powley closed-form; η = 0.72 small-arms efficiency |
| External ballistics velocity | §4 | G7 point-mass under ICAO standard atmosphere |
| RHA penetration (0° normal) | §3 | De Marre, K = 7.80 × 10⁻⁴, 290 BHN RHA |
| Suppressor attenuation | §5 | Adiabatic-expansion peak-attenuation bound, 40 dB cap |
| **Acoustic signature** | **§6** | Westin (1975) muzzle-blast SPL fit, calibrated against 5.56 / 7.62 / .50 BMG anchors; layered hearing-protection stack (foam −22 dB, double −28 dB, +TACS −25 dB) |
| **Zeroed bullet drop** | **§7** | Bisection-zero integration, scope-height-over-bore 4 cm, canonical 100 m zero |
| **Wind drift** | **§8** | Didion / Bagnold full-value crosswind correction, 4.47 m/s (10 mph) |
| **Hatcher max-effective range** | **§9** | KE > 80 J personnel-incapacitation threshold + supersonic-range cutoff |
| **Barrel life** | **§10** | Calibrated bore-wear model anchored to M4 (10 000 rd 5.56 chrome-lined), M14 (7 500 rd 7.62), M2HB (10 000 rd .50 Stellite); thermal-bound rpm from barrel mass × specific heat |
| **Portfolio lifecycle** | **§23** | Structural SF, parts-life bore service (75 000 rd), MRBF MC (20 270 analytic / 10 000 simulated), felt recoil (0.11 ft·lb), FTF (1:68 000) |
| **Peak shoulder force** | **§11** | Parabolic-energy-dissipation over `stock_travel_mm` with muzzle-brake impulse-redirection efficiency |
| **Body-armour V50** | **§13** | Lambert-Jonas / Recht-Ipson V50 with composite-factor calibration; clay-witness BFD per NIJ 0101.06 |

### 12A.1 Acoustic signature methodology

The Westin (1975) blast-SPL fit (`weapons_sim_results.md` §6) is calibrated against published 5.56 carbine (≈ 165/158 dB muzzle/ear), 7.62 rifle (≈ 166/159 dB), and .50 BMG (≈ 178/170 dB) anchors. For the MP-4.6M Guardian, the simulator outputs 163.4 dB unsuppressed muzzle / 156.4 dB at the shooter's ear, dropping to 123.4 / 116.4 dB with the integrated 80 cm³ K-baffle suppressor. The hearing-protection stack columns reflect industry-standard NRR-equivalent attenuation (foam plug −22 dB, double plug + muff −28 dB) plus the TACS personal-variant active-cancellation depth of −25 dB validated against the Nelson-Elliott (1992) ANC bound (`weapons_sim_results.md` §18). The full ear-level peak with all layers is 63.4 dB.

### 12A.2 Effective-range methodology

The Hatcher 80 J KE-threshold criterion (`weapons_sim_results.md` §9) provides the maximum personnel-incapacitation range for the cartridge / barrel-length combination; the supersonic range is the cross-over point of the G7-integrated trajectory through Mach 1.0 in ICAO atmosphere. For the MP-4.6M Guardian's 4.6 × 30 mm Enhanced load (501 m/s, 2.6 g WC-cored), the simulator reports an 878 m KE > 80 J range and a 301 m supersonic range; the cartridge becomes transonic / subsonic before reaching its KE-threshold range, so the operational envelope is bounded by transonic-destabilisation accuracy degradation, not energy decay.

### 12A.3 Barrel-life methodology

The bore-wear model (`weapons_sim_results.md` §10) computes rounds-to-throat-erosion from chamber pressure, projectile mass, propellant mass, and liner-material wear coefficient, calibrated against the M4 / M14 / M2HB / GAU-8 / M256 anchors. For the Guardian's 0.30 kg Stellite-21-lined barrel at 26 100 psi, the simulator reports **302 501 rounds** throat-erosion life (§10). The §23 **bore life service** rating of **75 000 rounds** is retained as the conservative accuracy-retention envelope (sub-2-MOA at 50 m), not the absolute throat-erosion bound.

### 12A.4 Recoil-force methodology

Peak shoulder force (`weapons_sim_results.md` §11) is the parabolic-energy-dissipation result of free-recoil energy distributed over `stock_travel_mm`, corrected for muzzle-brake impulse-redirection efficiency. For the Guardian (1.5 J free recoil, 4 mm grip-cycle envelope, 0 % brake), the simulator reports 559 N peak shoulder force — comparable to a 9 mm Parabellum service pistol, consistent with the cartridge's modest recoil impulse and the rotating-bolt locked-breech architecture.

### 12A.5 Body-armour V50 methodology

Lambert-Jonas / Recht-Ipson V50 ballistic-limit values (`weapons_sim_results.md` §13) are calibrated against published NIJ 0101.06 panel data for soft IIIA, NIJ III, NIJ IV, and the APES military / police composites. The 4.6 × 30 mm Enhanced is **not directly characterised** in §13; the closest catalogued PDW-class threat is the 5.7 × 28 mm SS190 (2.0 g, 716 m/s), which §13 reports as STOPPED by every armour class. The Guardian's 4.6 × 30 mm at 501 m/s carries less specific kinetic energy than the SS190 and is bounded above by the SS190's outcome — every armour class in the simulator's catalogue stops the Guardian's projectile.

## 13. Conclusion

The MP-4.6M Guardian, when re-derived against the portfolio ballistics simulator, is a low-recoil, suppressed, rotating-bolt single-action service pistol delivering 326 J of muzzle energy from a 2.6 g WC-Co cored projectile at 501 m/s, with a 20-round magazine and integrated 40 dB suppressor. Its operational rationale is suppressed signature, low recoil, ammunition commonality with the MP-4.6M Defender PDW, and CRISAT-class soft-armour defeat — *not* hard-armour penetration. Prior numerical claims (1 120 m/s, 1 752 J, 15 mm RHA, 30-round magazine, 900 rpm) are formally retracted; this v2.0 paper is the authoritative specification.

## Appendix A — Governing Equations

This appendix documents the governing equations used by the portfolio ballistics simulator (`weapons_simulation.py`) to derive the MP-4.6M Guardian Pistol performance numbers cited in §3–§7 and §12A. Calibration constants are taken from `weapons_sim_results.md` §1–§13. The structure follows the reference appendix in [`../../Weapons-Police/MP-4.6P Guardian LE/MP-4.6P_Guardian_LE_Specification.md`](../../Weapons-Police/MP-4.6P%20Guardian%20LE.md) Appendix A; the Guardian Pistol is the military parent (4.6 × 30 mm Enhanced) of the Guardian LE (4.6 × 22 mm DPAP), and the equations follow the same seven-phase structure.

### A.1 Interior ballistics — Noble-Abel for 4.6 × 30 mm, 180 mm barrel

A 1D Noble-Abel integration with Powley η = 0.72 (small-arms branch) produces the muzzle velocity, peak chamber pressure, and bolt impulse for the Guardian pistol's 180 mm barrel.

```
P · (V − m_g · b) = m_g · R_g · T            (Noble-Abel)
m_b · dv_b/dt = A_b · P · η_pwr − F_friction
dα/dt = a · P^n · (1 − α)                    (Vielle burn)

A_b      = π · (0.00465/2)² = 1.698 × 10⁻⁵ m²    (4.65 mm bore area)
m_b      = 2.6 × 10⁻³ kg                          (WC-Co cored projectile)
η_pwr    = 0.72                                    (Powley small-arms efficiency)
Charge   = ~0.40 g triple-base
Tube L   = 0.180 m (180 mm Guardian barrel)
Case capacity = ~1.0 cm³ (sim §5)
b, R_g, γ as Paper 8 §A.1
```

→ Peak chamber pressure = **180 MPa (26 107 psi)** (sim §1; paper rounds to 26 100 psi), muzzle velocity = **501 m/s**, muzzle KE = ½ · 0.0026 · 501² = **326 J**, recoil impulse = **1.65 N·s** (sim §1; paper-body §7 cites 1.60 N·s — see Note 1 in §A.7).

### A.2 Exterior ballistics — point-mass + Miller Sg

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_b
v(0) = 501 m/s, v(100 m) = 434 m/s, v(300 m) = 338 m/s, v(500 m) = 299 m/s,
v(800 m) = 256 m/s, v(1 km) = 231 m/s   (sim §4, 4.6x30mm)

G7 form factor i₇ ≈ 0.95 (WC-cored spitzer)
Mach at muzzle = 501 / 343 = 1.46
```

**Miller (Litz-corrected) gyroscopic stability:**

```
Sg = (30 · m_b) / (ρ_b · d_b³ · L_b · t²) · 1 / (2π²)

d_b = 0.00465 m, L_b/d_b = 18/4.65 = 3.87, ρ_b = 14 800 kg/m³
t   = 0.2032 m/rev (1:8 twist, from §5.1)
```

→ Sg > 1.4 throughout supersonic regime; supersonic range **301 m**, max-effective range **878 m** at Hatcher 80 J KE threshold (`weapons_sim_results.md` §9, `4.6x30mm`).

### A.3 Terminal ballistics — De Marre + Poncelet tissue

**De Marre for RHA penetration:**

```
T_RHA = K · m_b^0.5 · v^1.43 / d_core^0.75

K       = 7.80 × 10⁻⁴
m_b     = 2.6 × 10⁻³ kg
d_core  = 4.65 mm
v(0)    = 501 m/s
```

→ Penetration vs RHA: **0 m: 3.8 mm, 100 m: 3.1 mm, 300 m: 2.2 mm, 500 m: 1.8 mm, 800 m: 1.5 mm, 1 km: 1.3 mm** (`weapons_sim_results.md` §3, `4.6x30mm`). All paper-body §4.3 values match.

**Poncelet resistive-force soft-tissue model:**

```
F_resist = (A_gel + B_gel · v²) · A_eff(x)
m_b · dv/dt = −F_resist(v, x),  dx/dt = v

A_gel = 200 Pa,  B_gel = 2 366 kg/m³ (FBI cold-gelatin calibration)
A_eff = π · (d_b/2)² = 1.698 × 10⁻⁵ m² (rigid WC penetrator)
```

→ Rigid 2.6 g WC penetrator at 501 m/s carries significant overpenetration risk in soft tissue (the explicit motivation for the lower-velocity 4.6 × 22 mm DPAP cartridge of the MP-4.6P Guardian LE LE-variant; see [`../../Weapons-Police/MP-4.6P_Guardian_LE_Research_Paper.md`](../../Weapons-Police/Research%20Paper%20-%20MP-4.6P%20Guardian%20LE.md) §5.2).

### A.4 Recoil — mass-spring-damper (pistol, no buffer)

The Guardian pistol is rotating-bolt + short-recoil **without** the PDW's buffered bolt-carrier; the recoil-spring + slide group is the only stage.

```
m_slide · ẍ_slide + c · ẋ_slide + k · x_slide = J_bolt · δ(t − t_unlock)

m_slide = 0.350 kg          (slide + bolt group)
k       = 92.4 N/m          (spring rate, comparable to MP-4.6P system spring; see Guardian LE Appendix A.4)
c       = ~0.18 N·s/m       (estimated polymer guide-rod damping)

Free recoil:
J_free = m_b · v_b + m_g · v_gas_avg = 0.0026 · 501 + 0.40e-3 · 600 ≈ 1.55 N·s analytic → 1.65 N·s sim
E_free = J_free² / (2 · M_pistol) = 1.65² / (2 · 0.92) ≈ 1.48 J ≈ 1.5 J ✓ (sim §2)

F_peak (parabolic-energy-dissipation):
F_peak = E_free · (4 / s_stroke) = 1.5 · (4 / 0.004) = 1 500 N analytic
Sim §11 corrected: F_peak = 559 N (126 lbf) at 4 mm grip-cycle, 0 % brake
```

→ E_free = **1.5 J (1.1 ft·lbf)** at 0.92 kg empty mass (`weapons_sim_results.md` §2), peak shoulder force = **559 N (126 lbf)** (`weapons_sim_results.md` §11) — comparable to a 9 mm Parabellum service pistol.

### A.5 Gas dynamics — port expansion + 6-baffle integral suppressor

```
P_port = P_peak · (V_chamber / V_port_zone)^γ        (isentropic expansion)

V_chamber = 1.0 cm³ (sim §5)
V_port (at 180 mm barrel) = V_chamber + A_b · 0.150 m ≈ 1.0 + 16.98 · 0.150 / 10⁶ × 10⁶
                          = 1.0 + 2.547 = 3.55 cm³ — or in m³: 3.55 × 10⁻⁶ m³

Integral suppressor (80 cm³, 6 K-baffles):
Attenuation_max ≈ 10 · log₁₀(V_suppressor / V_chamber) + N_baffles · k_baffle
               = 10 · log₁₀(80 / 1.0) + 6 · 4 = 19 + 24 = 43 dB analytic
               → capped at 40 dB modelled cap (sim §5)
```

→ Suppressor attenuation **40 dB peak** (`weapons_sim_results.md` §5, `MP-4.6M Pistol integral`); SPL with suppressor = **123.4 dB muzzle / 116.4 dB at ear** (sim §6).

### A.6 Structural — Lamé + Wahl + Goodman

**Lamé thick-walled cylinder (barrel chamber wall):**

```
σ_hoop = P · (r_o² + r_i²) / (r_o² − r_i²)

P    = 180 MPa peak chamber pressure
r_i  = 2.325 mm (4.65 mm bore)
r_o  = 10.5 mm (typical pistol barrel outer diameter at chamber)

σ_hoop = 180 · (110.25 + 5.41) / (110.25 − 5.41) = 180 · 115.66 / 104.84 = 198.6 MPa

Stellite 21 yield at chamber temperature ≈ 690 MPa → SF_yield = 3.5
```

**Wahl-corrected recoil-spring stress:**

```
τ = K_w · 8 · F · D / (π · d³)

K_w  = (4C − 1)/(4C − 4) + 0.615/C            (Wahl correction)
C    = D / d = 11 (spring index for compact pistol spring)
K_w  = (43)/(40) + 0.0559 = 1.131

F_max = k · x_max = 92.4 · 0.040 = 3.70 N
τ_max = 1.131 · 8 · 3.70 · 0.011 / (π · 0.001³) ≈ 117 MPa
S_e (17-7 PH H900 shear endurance) = 428 MPa → fatigue SF ≈ 3.7
```

**Goodman infinite-life fatigue (slide / barrel cycles):**

```
σ_a / S_e + σ_m / S_u ≤ 1 / SF_fatigue

For the slide guide rails at 75 000-round service life:
σ_a (alternating, per cycle) ≈ 80 MPa
σ_m (mean, slide-spring preload) ≈ 40 MPa
S_e (4140 alloy steel) ≈ 350 MPa
S_u ≈ 850 MPa
→ Goodman: 80/350 + 40/850 = 0.229 + 0.047 = 0.276 → SF_fatigue ≈ 3.6, infinite-life
```

### A.7 Reliability — Bernoulli MC

The seven-mode Bernoulli framework (Guardian LE Appendix A.7) applied to the Guardian pistol's per-mode rates:

```
Per-mode failure rates (Guardian pistol, baseline single-action service-pistol configuration):
FTFeed:     1 : 80 000    (single-column-staggered 20-round, slightly tighter feed envelope than PDW)
FTExtract:  1 : 60 000
FTFire:     1 : 50 000    (single-action striker; less margin than buffered PDW)
FTEject:    1 : 40 000
FTGas:      1 : 200 000   (low gas exposure in short-recoil pistol)
FTPrimer:   1 : 100 000
FTCase:     1 : 250 000

Analytic MRBF = 1 / Σ p_j ≈ 1 / 6.5 × 10⁻⁵ ≈ 15 000 rounds (per-mode harmonic sum)
FTF rate ≈ 1 / 50 000 (per-mode FTFire rate in this appendix)
```

Portfolio lifecycle MC (`weapons_sim_results.md` §23): MRBF analytic **20 270** / simulated **10 000**; FTF rate **1:68 000**; felt recoil **0.11 ft·lb** — authoritative targets in paper-body §9 and spec §11.2. §23 portfolio MC supersedes the per-mode harmonic sum for specification claims.

### A.8 Notes on numerical concordance with the simulator

1. **Recoil impulse 1.60 N·s (§7) vs sim §1 1.65 N·s.** Minor discrepancy; the §7 analytic computation cites 1.60 N·s, while `weapons_sim_results.md` §1 returns 1.65 N·s. The 1.5 J free-recoil-energy figure derives from 1.65² / (2 · 0.92) = 1.48 J ≈ 1.5 J ✓, so the simulator value is the internally consistent one.

2. **All other Guardian Pistol numbers (501 m/s, 326 J, 180 MPa, 3.8 mm RHA, 1.5 J free recoil, 559 N peak force, 878 m max range, 301 m supersonic, 302 501 rounds barrel life, 250 rpm thermal-bound, 40 dB suppressor) match `weapons_sim_results.md` §1–§13.** The Guardian Pistol is the most directly-traceable platform in the portfolio.

3. **Section §6A SPL 163.4 / 156.4 / 123.4 / 116.4 / 94.4 / 88.4 / 63.4 dB ✓ matches sim §6 `MP-4.6M Pistol` row.**

---

## 14. References

[1] Ezell, E.C. (1988). *Handguns of the World*. Stackpole Books.

[2] Wikipedia. (2024). *HK 4.6×30mm cartridge*. Wikimedia Foundation.

[3] Hutchcroft, I. (2009). Rotating-bolt short-recoil service pistols. *Small Arms Review*, 12(9).

[4] Jane's Infantry Weapons. (2023). *Suppressed Service Pistol Systems*. Jane's Defence Group.

[5] Cutshaw, C.Q. (2011). *Tactical Small Arms of the 21st Century*. Gun Digest Books.

[6] Advanced Defence Systems Research Division. (2026). *Weapons-Defence portfolio — simulation results* (`weapons_sim_results.md`). Internal technical reference.

[7] Advanced Defence Systems Research Division. (2026). *UCDR Weapons Portfolio — Common Ballistics Simulator* (`weapons_simulation.py`). Internal technical reference.
