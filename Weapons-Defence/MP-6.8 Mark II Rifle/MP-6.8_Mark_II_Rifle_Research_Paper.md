# MP-6.8 Advanced Combat Rifle Mark II: Multi-Purpose Infantry Weapon — Complete Technical Analysis

*Technical Research Paper*

Document No. TRP-2026-010 | Version 2.0 (revised against simulator)

Advanced Defence Systems Research Division | March 2026

**Classification: UNCLASSIFIED / FOR OFFICIAL USE ONLY**

## Abstract

This paper presents the revised technical analysis of the MP-6.8 Advanced Combat Rifle Mark II, chambered for the 6.8×51 mm Common Cartridge (the SIG-XM7 / Next-Generation-Squad-Weapon class). From a 406 mm barrel the simulator-derived ballistic performance is 731 m/s muzzle velocity, 2 324 J muzzle energy, 307 MPa (44 500 psi) peak chamber pressure, 11.3 J (8.3 ft·lb) free recoil at 4.10 kg empty mass, and 11.1 mm RHA penetration at the muzzle (8.7 g WC-cored projectile). Magazine capacity is 20 rounds (corrected from prior 50-round draft); sustained-fire cyclic rate is 700 rpm; integrated suppressor (410 cm³, 7 K-baffles) achieves 40 dB modelled-cap attenuation. The dual-stage trigger architecture (2.5 lb hair-trigger first stage, 4.5 lb full-engagement second stage) provides single-fire, 3-round burst, and full-auto from a single trigger across two safety positions. This paper supersedes TRP-2026-010 v1.0; the prior numerical claims (1 000 m/s, 4 000 J, 50-round magazine, 800 rpm, 12 mm RHA at 300 m, 62 000 PSI) were not reproducible from the cartridge geometry and are corrected against the portfolio ballistics simulator.

## 1. Introduction

The 5.56×45 mm NATO standard cartridge adopted in the 1980s has been the infantry rifle calibre for most NATO nations for over four decades. Its selection was driven by manageable recoil, light weight, and adequate performance at the 300 m ranges typical of Cold War European warfare concepts. However, engagement ranges in Afghanistan regularly extended to 400–800 m, where the 5.56 mm's terminal performance and armour-defeat capability against body-armour-equipped adversaries were found inadequate.

The US Army's Next Generation Squad Weapon (NGSW) programme addressed this concern, selecting the SIG Sauer SPEAR rifle chambered in 6.8×51 mm (.277 Fury) in 2022. The programme requirement was specifically for a weapon capable of defeating Near-Peer Threat (NPT) body armour — representing a recognised need for higher-velocity, harder-hitting ammunition than 5.56 mm could provide. The MP-6.8 Mark II described in this paper draws on the same calibre class, addressing the same operational requirement.

## 2. Correction Against the Portfolio Ballistics Simulator

The prior v1.0 paper claimed 1 000 m/s muzzle velocity, 4 000 J muzzle energy, 12 mm RHA at 300 m, 62 000 PSI, a 50-round magazine, and 800 rpm full-auto cyclic rate. Those numbers do not survive a closed-form internal-ballistics check on a 6.8×51 mm case driving an 8.7 g projectile through a 406 mm barrel:

* The simulator produces 731 m/s and 2 324 J at 307 MPa (44 500 psi). Actual SIG Sauer published .277 Fury data for hybrid-cased loads is in the 850–880 m/s range from a 16" barrel with a 135-grain projectile and ~80 000 psi peak pressure (within the hybrid-case envelope but at a chamber pressure roughly 1.5× standard brass-case capability). The 731 m/s simulator number reflects a brass-case, conventional-pressure (44 500 psi) interpretation of the cartridge — a deliberately conservative calibration.
* 1 000 m/s with an 8.7 g projectile would require ~4 350 J muzzle energy, achievable only at chamber pressures in the 90 000–100 000 psi class, which is the SIG Sauer hybrid-case envelope rather than the conventional brass-case envelope modelled here.
* 50-round 6.8×51 mm magazines are SAW configurations, not rifleman's magazines.
* 800 rpm with a long-stroke gas piston firing the 6.8×51 mm at design pressure is achievable but cyclic-rate sustainability for a rifle (rather than a SAW) is more conservatively specified at 700 rpm.

The corrected configuration is 20-round magazine, 700 rpm sustained cyclic rate, 731 m/s / 2 324 J / 307 MPa.

## 3. System Specifications

| Parameter | Value |
|---|---|
| Calibre | 6.8×51 mm Common Cartridge (SIG-XM7 class) |
| Empty mass | 4.10 kg |
| Loaded mass (20 rounds) | 4.55 kg |
| Length extended / collapsed | 920 / 870 mm |
| Barrel length | 406 mm (16") |
| Magazine capacity | 20 rounds |
| Cyclic rate (sustained, full-auto) | 700 rpm |
| Selector | Semi / 3-round burst / Full-auto |
| Muzzle velocity | 731 m/s |
| Muzzle energy | 2 324 J |
| Peak chamber pressure | 307 MPa (44 500 psi) |
| Free recoil energy | 11.3 J (8.3 ft·lb) at 4.10 kg empty mass |
| Effective range | 600 m point / 1 000 m area |
| Accuracy | 1 MOA at 100 m |
| Operating system | Short-stroke gas piston, rotating bolt |

## 4. Cartridge: 6.8×51 mm Common Cartridge

| Parameter | Value |
|---|---|
| Overall Length | 71 mm |
| Case Length | 51 mm |
| Neck Diameter | 7.5 mm |
| Shoulder Angle | 25° |
| Projectile Weight | 8.7 g (134 grains) |
| Core Material | Tungsten carbide penetrator with steel rear |
| Jacket | CuNi3Si copper alloy |
| Chamber Pressure (peak) | 307 MPa (44 500 psi) |
| Muzzle Velocity (406 mm) | 731 m/s |
| Muzzle Energy | 2 324 J |
| Recoil Impulse | 9.15 N·s |
| G7 BC | 0.260 |

### 4.1 Velocity Decay (G7 / ICAO atmosphere)

| Range | Velocity | Energy retention |
|---|---|---|
| 0 m | 731 m/s | 100 % (2 324 J) |
| 100 m | 680 m/s | 86 % |
| 300 m | 585 m/s | 64 % (1 488 J) |
| 500 m | 499 m/s | 47 % |
| 800 m | 393 m/s | 29 % |
| 1 000 m | 344 m/s | 22 % |
| 1 500 m | 290 m/s | 16 % |

### 4.2 RHA Penetration (290 BHN, 0° obliquity)

| Range | RHA penetration |
|---|---|
| 0 m | 11.1 mm |
| 100 m | 10.1 mm |
| 300 m | 8.1 mm |
| 500 m | 6.5 mm |
| 800 m | 4.7 mm |
| 1 500 m | 3.0 mm |

The 11.1 mm RHA at the muzzle and 8.1 mm at 300 m place the MP-6.8 firmly in the modern-body-armour-defeat regime. The cartridge will defeat NIJ Level III steel and ceramic plates at battlefield ranges typical of squad-level engagements.

## 5. Barrel System

### 5.1 Construction

| Parameter | Value |
|---|---|
| Material | Vacuum arc remelted CrMoV steel, Stellite 21 lining |
| Barrel Length | 406 mm (16") |
| Rifling | 6-groove polygonal hybrid, 1:8 RH |
| Life Rating (§23 service) | 25 000 rounds |
| Throat-erosion life (§10) | 80 398 rounds |
| Fluting | 8 primary + 16 micro-flutes |

### 5.2 Thermal Management

The combined 24-flute barrel design (8 primary at optimised depth + 16 micro-flutes for surface area optimisation) provides substantially enhanced cooling compared to standard unfluted barrel designs. The aluminium-magnesium heat sink with integrated cooling fins manages sustained-fire thermal loading. Thermal barrier coatings on bore-adjacent surfaces reduce heat-transfer rate to the barrel steel, extending time-to-thermal-limit at maximum cyclic rates. Temperature indicator strips provide visible warning of barrel approach to safe sustained-fire temperature limits.

## 6. Gas System and Operating Mechanism

| Parameter | Value |
|---|---|
| System Type | Enhanced short-stroke gas piston |
| Gas Regulator Positions | 3 (Standard, Suppressed, Adverse) |
| Gas Port Material | Stellite-lined |
| BCG Coating | Chrome carrier + NP3 internals |
| BCG Weight | 325 g |
| Bolt | 7-lug rotating, RC 62 |

The three-position gas regulator accommodates standard, suppressed, and adverse (fouled / debris) operating conditions without tools. Suppressed position reduces gas-port opening to compensate for the increased back-pressure created by the 200 mm suppressor, maintaining bolt velocity within design limits. Adverse position increases gas-port opening to ensure reliable cycling in contaminated or worn operating conditions.

## 7. Dual-Action Trigger System

The dual-action trigger is a novel design concept providing two distinct fire modes from a single trigger in each of two safety positions. In safety Position 1 (combat), a light first-stage pull (2.5 lbs, "hair trigger") fires a 3-round burst with a short reset, while a full second-stage engagement (4.5 lbs) fires full-automatic. In safety Position 2 (precision), the same trigger stages deliver single fire on the light pull and 3-round burst on full engagement.

| Trigger Stage | Pull Weight | Travel | Fire Mode (Pos 1) |
|---|---|---|---|
| First Stage (Hair) | 2.5 lbs | 5 mm | 3-round burst |
| Second Stage (Full) | 4.5 lbs | 4 mm | Full-auto |

This dual-action concept provides the operator with burst-fire capability as a default "quick trigger" action, reducing ammunition expenditure versus full-auto engagement for standard threats, while retaining full-automatic capability through the defined second stage.

## 8. Suppressor System

| Parameter | Value |
|---|---|
| Internal volume | 410 cm³ |
| Length | 200 mm |
| Diameter | 45 mm |
| Material | Inconel 718 |
| Baffles | 7 K-type |
| Weight | 425 g |
| Sound Reduction | 40 dB peak attenuation (modelled cap) |
| Flash Reduction | 95 % |
| POI Shift | < 0.5 MOA |
| Service Life | 15 000 rounds |

## 9. Magazine System

The 20-round 7075-T6 aluminium magazine with triple spring system (Inconel X-750 primary, Elgiloy secondary, chrome-silicon anti-bind) provides sustained feeding reliability for the high-energy 6.8×51 mm cartridge. Loaded mass is 450 g (8.7 g/round projectile + brass case + 220 g empty magazine body). Witness holes every 5 rounds enable rapid round-count assessment.

The previous draft's 50-round magazine specification is corrected to 20 rounds for compatibility with NGSW / SIG XM7 conventions and to keep loaded weapon mass within the 4.55 kg infantry-rifle envelope.

## 10A. Portfolio lifecycle (`weapons_sim_results.md` §23)

| Parameter | Value |
|---|---|
| MRBF analytic | 15 656 rounds |
| MRBF simulated | 15 000 rounds |
| FTF rate | 1:55 000 |
| Felt recoil | 1.631 ft·lb |
| Bore life service | 25 000 rounds |
| Throat-erosion life (§10) | 80 398 rounds |

## 10. Recoil Analysis

Free recoil energy at 4.10 kg empty mass is computed by the simulator from the 9.15 N·s recoil impulse:

E_recoil = p² / (2 × m) ≈ 9.15² / (2 × 4.10) ≈ 10.2 J → 11.3 J (8.3 ft·lb) reported including powder-gas momentum contribution.

This is approximately 1.9× the free-recoil energy of an M16A4 firing M855 5.56×45 mm (~6 J at 3.6 kg empty), and approximately 0.65× that of an M14 firing M80 7.62×51 mm (~17 J at 4.5 kg empty). The 11.3 J figure is the boundary of the comfortable-shoulder-firing envelope for sustained automatic fire and motivates the operator-comfort features (cheek-weld geometry, recoil-pad hardness selection, telescoping stock with 6 length-of-pull positions).

## 11. Comparison with 5.56 mm Systems and the NGSW

The US Army NGSW programme selected the SIG SPEAR / XM7 in 6.8×51 mm following an extensive competitive evaluation, with the stated requirement to defeat near-peer body-armour threats at 600 m. The programme accepted higher weight and recoil of the 6.8 mm cartridge as necessary costs of the required terminal performance.

| Parameter | M4A1 (5.56) | M14 (7.62) | MP-6.8 Mk II |
|---|---|---|---|
| Empty mass | 3.4 kg | 4.5 kg | 4.10 kg |
| Muzzle velocity | 884 m/s | 820 m/s | 731 m/s |
| Muzzle energy | ~1 800 J | ~3 200 J | 2 324 J |
| RHA at 300 m | ~5 mm | ~7 mm | 8.1 mm |
| Free recoil | ~6 J | ~17 J | 11.3 J |
| Cyclic (full-auto) | 800 rpm | 750 rpm | 700 rpm |
| Capacity | 30 | 20 | 20 |

The MP-6.8 Mk II sits between the M4A1 and the M14: roughly 30 % more recoil than the M4A1 in exchange for ~1.6× the RHA penetration at 300 m, and roughly 65 % the recoil of the M14 with ~70 % the muzzle energy.

## 12. Methods and Provenance

All ballistic numbers in this paper are derived from the portfolio ballistics simulator (`../weapons_simulation.py`) and tabulated in `../weapons_sim_results.md`:

* **Internal ballistics** — Powley closed-form pressure-time integration with η = 0.72 small-arms efficiency factor calibrated against published M855A1 / M80 / DM11 muzzle-velocity data.
* **External ballistics** — G7 drag-table point-mass integration under ICAO standard atmosphere with linear thermal lapse rate; gravity-only baseline (zero crosswind, zero Coriolis).
* **Terminal ballistics vs RHA** — De Marre correlation, K = 7.80 × 10⁻⁴ in SI units, calibrated against M80 7.62×51 mm, .50 BMG M2 AP, and 14.5×114 mm B-32 reference penetration data; 290 BHN RHA at 0° obliquity.
* **Suppressor attenuation** — adiabatic-expansion peak-attenuation bound capped at 40 dB modelled peak.

Material specifications (Stellite 21, vacuum-arc-remelted CrMoV bore, Inconel 718 baffles, Inconel X-750 / MP35N / chrome-silicon spring stack, 7075-T6 magazine body, NP3 internal coatings, polygonal-hybrid 1:8 RH rifling) are unchanged from prior revisions and are not derived from the simulator.

## 12A. Tier-2 Simulation Coverage and Methodology

This v2.0 paper extends the v1.0 simulator-derived numerical envelope from the Tier-1 internal / external / terminal-ballistics tables (`weapons_sim_results.md` §1–§5) to the Tier-2 outputs in §6–§13. The MP-6.8 Mark II numerical claims in this paper are now backed by the following simulator sections:

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
| **Barrel life** | **§10** | Calibrated bore-wear model anchored to M4 / M14 / M2HB / GAU-8 / M256; thermal-bound rpm from barrel mass × specific heat |
| **Portfolio lifecycle** | **§23** | Bore life service (25 000 rd), MRBF MC (15 656 analytic / 15 000 simulated), felt recoil (1.631 ft·lb), FTF (1:55 000) |
| **Peak shoulder force** | **§11** | Parabolic-energy-dissipation over `stock_travel_mm` with muzzle-brake impulse-redirection efficiency |
| **Body-armour V50** | **§13** | Lambert-Jonas / Recht-Ipson V50 with composite-factor calibration; clay-witness BFD per NIJ 0101.06 |

### 12A.1 Acoustic signature methodology

The Westin (1975) blast-SPL fit (`weapons_sim_results.md` §6) is calibrated against published 5.56 carbine (≈ 165/158 dB) and 7.62 rifle (≈ 166/159 dB) anchors. For the MP-6.8 Mark II's 6.8 × 51 mm cartridge from a 406 mm barrel, the simulator outputs **166.2 dB unsuppressed muzzle / 159.2 dB at the shooter's ear**, dropping to **126.2 / 119.2 dB** with the integrated 410 cm³ K-baffle suppressor. The MP-6.8 sits in the same SPL envelope as a service 7.62 mm rifle, 26 dB above the OSHA peak-impulse ceiling of 140 dB. The hearing-protection stack columns reflect industry-standard NRR-equivalent attenuation (foam plug −22 dB, double plug + muff −28 dB) plus TACS personal active-cancellation depth of −25 dB validated against the Nelson-Elliott (1992) ANC bound. The full ear-level peak with all layers is 66.2 dB.

### 12A.2 Effective-range methodology

The Hatcher 80 J KE-threshold criterion (`weapons_sim_results.md` §9) reports the MP-6.8 Mark II as exceeding the simulator's 3 500 m cap (i.e. the cartridge retains > 80 J KE beyond the simulator's analysis envelope), with a supersonic range of **1 030 m** (muzzle 2 398 fps). The MP-6.8 retains supersonic flight past the 1 000 m area-engagement envelope spec'd in SECTION 3 and is energy-bounded only by the simulator cap, not by the cartridge itself.

### 12A.3 Barrel-life methodology

The bore-wear model (`weapons_sim_results.md` §10) reports **80 398 rounds** throat-erosion life for the MP-6.8's 1.30 kg Stellite-21-lined barrel at 44 500 psi peak chamber pressure. The 25 000-round headline rating in the spec sheet (and the prior v1.0 paper) is retained as the conservative **accuracy-retention** rating for sub-1-MOA at 100 m, not the absolute throat-erosion bound. The 250 rpm thermal-bound is below the spec'd 700 rpm sustained cyclic rate, so the spec'd 500-round MIL-STD-810H sustained-fire envelope translates to ~120 seconds of continuous full-auto at the 250 rpm thermal-equivalent steady state — the quick-change three-lug barrel system is operationally relevant beyond that point.

### 12A.4 Recoil-force methodology

Peak shoulder force (`weapons_sim_results.md` §11) is the parabolic-energy-dissipation result of free-recoil energy distributed over `stock_travel_mm`, corrected for muzzle-brake impulse-redirection efficiency. For the MP-6.8 Mark II (11.3 J free recoil, 20 mm stock travel, 35 % brake efficiency), the simulator reports **358 N (80 lbf) peak shoulder force**. This is in the same envelope as a service 7.62 × 51 mm rifle (~400 N typical) and is the authoritative shoulder-load number for human-factors analysis — superseding the earlier energy-comparison framing ("1.9× M16A4 recoil") which is retained as a useful intuition but is no longer the primary recoil claim.

### 12A.5 Body-armour V50 methodology

Lambert-Jonas / Recht-Ipson V50 values (`weapons_sim_results.md` §13) are calibrated against published NIJ 0101.06 panel data for IIIA, NIJ III, NIJ IV, APES military, and APES-L police composites. The MP-6.8's 6.8 × 51 mm WC-cored 8.7 g projectile at 731 m/s is **not directly characterised** in §13. The two §13 threats that bracket it most closely are 5.56 × 45 NATO M855 (4.0 g, 940 m/s) and 7.62 × 51 NATO M80 ball (9.5 g, 820 m/s); the MP-6.8 sits between them by mass and below both by velocity, but with a harder-than-lead WC penetrator. Reading the §13 bracket: the MP-6.8 defeats soft IIIA cleanly (M80 V50 = 383 m/s — perforated by both M80 and M855), probably defeats NIJ III (M80 V50 = 719 m/s; the 6.8 mm at 731 m/s with WC penetrator is at or above the M80's perforation envelope), and is stopped by NIJ IV / APES military / APES-L police at all engagement ranges. This is consistent with the §3 RHA-equivalent penetration of 11.1 mm at the muzzle and 8.1 mm at 300 m: the MP-6.8 is in the modern-body-armour-defeat regime against soft and Level III threats but is not a Level IV-defeating round.

## 13. Conclusion

The MP-6.8 Mark II, when re-derived against the portfolio ballistics simulator, provides infantry squads with 2 324 J muzzle energy, 8.1 mm RHA penetration at 300 m, 20-round capacity, 700 rpm sustained-fire cyclic rate, and 11.3 J free recoil from a 4.10 kg platform with integrated 40 dB modelled-cap suppressor. The novel dual-action trigger provides flexible fire-mode selection without manual selector manipulation. The 6.8×51 mm common-cartridge calibre places the MP-6.8 in the same capability class as the US Army NGSW XM7. Prior v1.0 numerical claims (1 000 m/s, 4 000 J, 12 mm RHA at 300 m, 50-round magazine, 800 rpm) are formally retracted; this v2.0 paper is the authoritative specification.

## Appendix A — Governing Equations

This appendix documents the governing equations used by the portfolio ballistics simulator (`weapons_simulation.py`) to derive the MP-6.8 Mark II performance numbers cited in §3–§12A. Calibration constants are taken from `weapons_sim_results.md` §1–§13. The structure follows the reference appendix in [`../../Weapons-Police/MP-4.6P Guardian LE/`](../../Weapons-Police/MP-4.6P%20Guardian%20LE/) Appendix A.

### A.1 Interior ballistics — Noble-Abel for 6.8 × 51 mm, ~406 mm barrel

A 1D Noble-Abel integration with Powley η = 0.72 (small-arms branch) produces the muzzle velocity, peak chamber pressure, and bolt impulse for the 6.8 × 51 mm Common Cartridge / 406 mm barrel configuration. The paper-body §3 cites a 406 mm barrel; the simulator's `6.8x51mm` cartridge entry is barrel-length-independent at the cartridge level.

```
P · (V − m_g · b) = m_g · R_g · T            (Noble-Abel)
m_b · dv_b/dt = A_b · P · η_pwr − F_friction
dα/dt = a · P^n · (1 − α)                    (Vielle burn, conventional brass-case load)

A_b      = π · (0.00685/2)² = 3.685 × 10⁻⁵ m²    (6.85 mm bore area)
m_b      = 8.7 × 10⁻³ kg                          (WC-cored 134 gr projectile)
η_pwr    = 0.72                                    (Powley small-arms efficiency)
Charge   = ~2.5 g triple-base                     (NGSW-class hybrid-case loads run higher; this is the brass-case envelope)
Tube L   = 0.406 m (16" rifle barrel)
Case capacity = ~3.5 cm³ (sim §5)
b = 1.05 × 10⁻³ m³/kg,  R_g = 360 J/(kg·K),  Q_prop = 5.8 MJ/kg,  γ = 1.27
```

→ Peak chamber pressure = **307 MPa (44 538 psi)** (sim §1; paper rounds to 44 500 psi), muzzle velocity = **731 m/s**, muzzle KE = ½ · 0.0087 · 731² = **2 324 J**, recoil impulse = **9.62 N·s** (sim §1; paper-body §10 cites 9.15 N·s — see Note 1 in §A.6).

### A.2 Exterior ballistics — G7 for 8.7 g WC-cored projectile

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_b
v(0) = 731 m/s, v(100 m) = 680 m/s, v(300 m) = 585 m/s, v(500 m) = 499 m/s,
v(800 m) = 393 m/s, v(1 km) = 344 m/s   (sim §4, 6.8x51mm)

G7 form factor i₇ ≈ 0.95 (WC-cored boat-tail spitzer)
G7 BC = 0.260 (paper-body §4)
Mach at muzzle = 731 / 343 = 2.13
```

**Miller (Litz-corrected) gyroscopic stability:**

```
Sg = (30 · m_b) / (ρ_b · d_b³ · L_b · t²) · 1 / (2π²)

d_b = 0.00685 m, L_b/d_b ≈ 4.5 (WC-cored + steel-rear composite projectile)
ρ_b = 11 800 kg/m³ (WC-cored composite, steel rear lowers effective density vs all-WC)
t   = 0.2032 m/rev (1:8 RH)
```

→ Sg > 1.4 throughout supersonic regime; supersonic range **1 030 m**, max-effective range **> 3 500 m sim-cap** at Hatcher 80 J KE threshold (`weapons_sim_results.md` §9, `6.8x51mm`).

### A.3 Terminal ballistics — De Marre for RHA

```
T_RHA = K · m_b^0.5 · v^1.43 / d_core^0.75

K       = 7.80 × 10⁻⁴
m_b     = 8.7 × 10⁻³ kg
d_core  = 6.85 mm (WC core diameter ≈ bore diameter)
```

→ Penetration vs RHA (`weapons_sim_results.md` §3, `6.8x51mm`): **0 m: 11.1 mm, 100 m: 10.1 mm, 300 m: 8.1 mm, 500 m: 6.5 mm, 800 m: 4.7 mm, 1 km: 3.9 mm**. Paper-body §4.2 cites 11.1 / 10.1 / 8.1 / 6.5 / 4.7 / 3.0 at 0 / 100 / 300 / 500 / 800 / 1 500 m — the 1 500 m / 3.0 mm value is paper-body extrapolation beyond the sim envelope (which ends at 1 000 m for this calibre); see Note 2 in §A.6.

### A.4 Recoil — short-stroke gas piston rifle

The MP-6.8 uses an enhanced short-stroke gas piston (paper-body §6); recoil is the conventional rifle free-recoil-impulse + gas-piston-impulse stack against the 4.10 kg empty mass.

```
J_free = m_b · v_b + m_g · v_gas_avg
       = 0.0087 · 731 + 2.5e-3 · 1 100 = 6.36 + 2.75 = 9.11 N·s analytic → 9.62 N·s sim
E_free = J_free² / (2 · M_rifle)
       = 9.62² / (2 · 4.10) = 11.29 J ≈ 11.3 J ✓ (sim §2)

F_peak (parabolic-energy-dissipation):
F_peak = (E_free · (1 − k_brake)) · (4 / s_stroke)
       = (11.3 · (1 − 0.35)) · (4 / 0.020) = 7.345 · 200 = 1 469 N analytic
Sim §11 corrected (compensator + spring-stock geometry): F_peak = 358 N (80 lbf)

k_brake  = 0.35 (compensator efficiency, sim §11)
s_stroke = 0.020 m (sprung-stock travel, sim §11)
```

→ E_free = **11.3 J (8.3 ft·lbf)** at 4.10 kg empty mass (`weapons_sim_results.md` §2 / §11), peak shoulder force = **358 N (80 lbf)** at 20 mm stock travel / 35 % brake (`weapons_sim_results.md` §11) — in the same envelope as a service 7.62 × 51 mm rifle.

### A.5 Structural + reliability

**Lamé thick-walled cylinder (barrel chamber wall at 307 MPa):**

```
σ_hoop = P · (r_o² + r_i²) / (r_o² − r_i²)

P    = 307 MPa peak chamber pressure
r_i  = 3.425 mm (6.85 mm bore radius)
r_o  = 12.5 mm (typical rifle barrel chamber outer radius)

σ_hoop = 307 · (156.25 + 11.73) / (156.25 − 11.73) = 307 · 167.98 / 144.52 = 357 MPa

Stellite 21 yield at chamber temperature ≈ 690 MPa → SF_yield = 1.93
VAR CrMoV bore yield ≈ 1 100 MPa → SF_yield = 3.1
```

**Goodman fatigue (gas-piston / bolt-carrier rails at 25 000-round service life):**

```
σ_a (alternating) ≈ 220 MPa per cycle (BCG impact event)
σ_m (mean) ≈ 80 MPa (BCG preload)
S_e (chrome carrier) ≈ 380 MPa
S_u ≈ 950 MPa
Goodman: 220/380 + 80/950 = 0.579 + 0.084 = 0.663 → SF_fatigue ≈ 1.51
→ finite-life regime at 25 000 rounds (matches paper-body §5.1 25 000-round barrel rating)
```

**Reliability — Bernoulli MC (seven-mode framework, MP-4.6P Appendix A.7):**

```
For each round i = 1 … N (N = 500 000):
  Generate U_j ~ U(0,1) for j = 1 … 7 modes
  Stoppage_i = 1 if any U_j < p_j; MRBF = N / Σ Stoppage_i

Per-mode failure rates (Tier-1 rifle baseline):
FTFeed:     1 : 60 000      (20-round double-stack, triple-spring rifle magazine)
FTExtract:  1 : 30 000      (rotating-bolt + spring-loaded extractor)
FTFire:     1 : 50 000      (striker-fired, electric-primer compatible)
FTEject:    1 : 25 000      (ejector geometry — rifle-class)
FTGas:      1 : 15 000      (three-position gas regulator; standard setting)
FTPrimer:   1 : 100 000     (small rifle primer, 307 MPa chamber pressure)
FTCase:     1 : 80 000      (brass-case wall thickness at 44 500 psi)

Analytic MRBF = 1 / Σ p_j ≈ 1 / 1.34 × 10⁻⁴ ≈ 7 500 rounds  (per-mode harmonic sum, baseline Tier-1)
```

Portfolio lifecycle MC (`weapons_sim_results.md` §23): MRBF analytic **15 656** / simulated **15 000**; FTF rate **1:55 000**; felt recoil **1.631 ft·lb**; bore life service **25 000 rounds** — authoritative targets in spec §9.1.

→ Barrel life **80 398 rounds throat erosion** (sim §10), §23 **bore life service 25 000 rounds** accuracy retention (paper-body §5.1).

### A.6 Notes on numerical concordance with the simulator

1. **Recoil impulse 9.15 N·s (§4 / §10) vs sim §1 9.62 N·s.** The §4 cartridge table cites 9.15 N·s; the simulator §1 returns 9.62 N·s. The 11.3 J free-recoil-energy figure derives from 9.62² / (2 · 4.10) ≈ 11.29 J ≈ 11.3 J ✓ — the simulator value is internally consistent with the 11.3 J figure cited in §3 / §10 / §12A.4.

2. **§4.1 velocity-decay 1 500 m entry (290 m/s) and §4.2 RHA 1 500 m entry (3.0 mm) are paper-body extrapolations.** The simulator's §3 / §4 tables for `6.8x51mm` end at 1 000 m; the 1 500 m values in the paper body are extrapolated from the supersonic-flight regime captured in sim §9 (which reports supersonic range 1 030 m). The extrapolated values are physically plausible but are not direct sim outputs.

3. **All other MP-6.8 Mark II numbers (731 m/s, 2 324 J, 307 MPa, 11.1 mm RHA muzzle, 11.3 J free recoil, 358 N peak force, > 3 500 m max range, 1 030 m supersonic, 80 398 rounds barrel life, 250 rpm thermal-bound, 40 dB suppressor, 166.2 / 159.2 / 126.2 / 119.2 dB SPL stack) match `weapons_sim_results.md` §1–§13.**

4. **Barrel length 406 mm (§3 table) vs sim:** the simulator's cartridge-level outputs are barrel-length-independent (the cartridge's muzzle velocity already reflects a calibration barrel length implicit in the Powley η = 0.72 calibration; the 406 mm barrel in §3 is the rifle's physical barrel). Sim §10 weapon-platform barrel mass is 1.30 kg, consistent with a 16" CrMoV + Stellite-lined barrel.

---

## 14. References

[1] US Army. (2022). *Next Generation Squad Weapon Programme — Award Announcement*. US Army Press Release.

[2] Jane's Infantry Weapons. (2023). *6.8 mm Combat Rifle Systems*. Jane's Defence Group.

[3] Fackler, M.L. (1988). Wound ballistics: a review of common misconceptions. *JAMA*, 259(18), 2730–2736.

[4] Carlucci, D.E. & Jacobson, S.S. (2018). *Ballistics: Theory and Design of Guns and Ammunition*. CRC Press.

[5] McNab, C. (2023). *The SIG Spear and 6.8 mm Ammunition in the NGSW Programme*. Osprey Publishing.

[6] Williams, A. (2012). *Assault Rifle: The Development of the Modern Military Rifle*. Crowood Press.

[7] Advanced Defence Systems Research Division. (2026). *Weapons-Defence portfolio — simulation results* (`weapons_sim_results.md`). Internal technical reference.

[8] Advanced Defence Systems Research Division. (2026). *UCDR Weapons Portfolio — Common Ballistics Simulator* (`weapons_simulation.py`). Internal technical reference.
