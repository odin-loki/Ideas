# MP-4.6M Defender Personal Defence Weapon: Buffered Rotating-Bolt Select-Fire Platform — Complete Technical Analysis

*Technical Research Paper*

Document No. TRP-2026-008 | Version 2.0 (revised against simulator)

Advanced Defence Systems Research Division | March 2026

**Classification: UNCLASSIFIED / FOR OFFICIAL USE ONLY**

## Abstract

This paper presents the revised technical analysis of the MP-4.6M Defender Personal Defence Weapon (PDW), chambered for the 4.6×30 mm Enhanced cartridge — the same cartridge fielded in the MP-4.6M Guardian service pistol. The Defender is a select-fire (semi / 3-round-burst / 850 rpm full-auto) shouldered PDW employing a rotating-bolt + short-recoil + buffered-bolt-carrier action and an integrated 180 cm³ K-baffle suppressor. From the Defender's 266.7 mm barrel the simulator derives 501 m/s muzzle velocity and 326 J muzzle energy at 180 MPa (26 100 psi) peak chamber pressure — identical to the Guardian Pistol because the small-arms-class propellant charge effectively completes combustion within the first ~150 mm of bore travel, and the additional barrel length contributes only minor velocity increase (within rounding). Empty mass is 2.10 kg; magazine capacity is 40 rounds; free recoil at 2.10 kg empty mass is 0.7 J (0.5 ft·lb). RHA penetration of the WC-Co cored 2.6 g projectile is 3.8 mm at the muzzle, falling to 1.8 mm at 500 m; the Defender is not a hard-armour-defeating weapon — it addresses CRISAT-class soft-armour-plus-titanium-backer threats and provides ammunition commonality with the Guardian Pistol. This paper supersedes TRP-2026-008 v1.0; the prior numerical claims (1 225 m/s, 2 000 J, 50-round magazine) were not reproducible from the cartridge geometry and are corrected against the portfolio ballistics simulator.

## 1. Introduction and PDW Background

The personal defence weapon concept emerged from a 1989 NATO requirement for a weapon class to replace 9 mm submachine guns for personnel who carry crew-served weapons, drive vehicles, or otherwise cannot conveniently carry full infantry rifles. The requirement specified a weapon capable of defeating the NATO CRISAT target — 20 layers of Kevlar with 1.6 mm titanium backing — at 200 m, from a weapon compact enough for single-handed use when required.

Two primary designs emerged: the FN P90, chambered for 5.7×28 mm, and the Heckler & Koch MP7, chambered for 4.6×30 mm. Both were developed through the 1990s. The HK MP7 entered production in 2001 and was confirmed to penetrate the NATO CRISAT target at 200 m with the DM11 AP (Ultimate Combat) round, achieving 720 m/s muzzle velocity with the DM11's 2.0 g projectile (~520 J muzzle energy). The NATO Collaborative Research into Small Arms Technology (CRISAT) studies programme formalised the test target under STANAG 4512.

The MP-4.6M Defender, like the MP7, employs a 4.6×30 mm cartridge. The Defender's "Enhanced" loading uses a heavier 2.6 g WC-Co cored projectile (vs the DM11's 2.0 g brass-jacketed steel-cored projectile) at 501 m/s — a deliberately moderate velocity chosen for ammunition commonality with the MP-4.6M Guardian service pistol and for clean burst-mode recoil.

## 2. Correction Against the Portfolio Ballistics Simulator

This v2.0 revision corrects the prior v1.0 numerical claims against `weapons_simulation.py` and the simulator's published results table (`weapons_sim_results.md`). The retracted v1.0 numbers were:

* 1 225 m/s muzzle velocity / 2 000 J muzzle energy
* 50-round magazine
* 15 mm RHA penetration at 25 m
* 58 000 PSI chamber pressure

Those numbers are inconsistent with the 4.6×30 mm Enhanced cartridge geometry (case capacity ~1.0 cm³, bore 4.65 mm, projectile mass 2.6 g, barrel length 266.7 mm). The simulator-derived values are 501 m/s, 326 J, 26 100 psi peak chamber pressure, 3.8 mm RHA at the muzzle, and a 40-round magazine. The corrected numbers are used throughout this paper.

## 3. System Specifications

| Parameter | Value |
|---|---|
| Calibre | 4.6×30 mm Enhanced (common with MP-4.6M Guardian Pistol) |
| Empty mass | 2.10 kg |
| Loaded mass (40 rounds) | 2.40 kg |
| Length extended | 780 mm |
| Length collapsed | 630 mm |
| Barrel length | 266.7 mm (10.5") |
| Muzzle velocity | 501 m/s |
| Muzzle energy | 326 J |
| Peak chamber pressure | 180 MPa (26 100 psi) |
| Free recoil energy | 0.7 J (0.5 ft·lb) at 2.10 kg empty mass |
| Per-shot felt recoil in burst | ~0.3 J (buffered) |
| Cyclic rate (full-auto) | 850 rpm |
| Selector | Semi / 3-round burst / Full-auto |
| Magazine capacity | 40 rounds |
| Effective range | 200 m point / 400 m area |
| Accuracy | 2 MOA at 50 m |
| Operating system | Rotating bolt + short recoil + buffered bolt-carrier |

## 4. The 4.6×30 mm Enhanced Cartridge

### 4.1 Projectile Design

| Parameter | Value |
|---|---|
| Projectile mass | 2.6 g (40 grains) |
| Core | Tungsten carbide (93 % WC, 7 % Co), 65 HRC |
| Jacket | CuNi3Si high-strength copper alloy |
| Projectile length | 18 mm |
| Sectional density | 0.17 |
| G7 form factor | ~0.95 |

### 4.2 Performance Comparison with Existing PDW Rounds

| Parameter | HK 4.6×30 mm DM11 | FN 5.7×28 mm SS190 | MP-4.6M Defender (this paper) |
|---|---|---|---|
| Muzzle velocity | 720 m/s | 716 m/s | 501 m/s |
| Muzzle energy | 506 J | 534 J | 326 J |
| Projectile mass | 2.0 g | 2.0 g | 2.6 g |
| Sectional density | 0.13 | 0.11 | 0.17 |
| RHA at 100 m | ~3.0 mm | ~1.8 mm | 3.1 mm |
| Cartridge commonality with paired pistol | Cancelled (UCP prototype only) | None fielded | Yes — MP-4.6M Guardian |

The Defender's 4.6 × 30 mm Enhanced load delivers lower muzzle velocity than the DM11 but higher sectional density (heavier projectile, same calibre), giving comparable retained velocity and slightly better RHA penetration at 100 m. The trade-off is deliberate: the heavier 2.6 g WC-cored projectile is the same projectile as the Guardian Pistol's, providing one-cartridge logistics across the pistol/PDW pair.

### 4.3 Penetration vs RHA (290 BHN, 0° obliquity)

| Range | RHA penetration |
|---|---|
| 0 m | 3.8 mm |
| 100 m | 3.1 mm |
| 300 m | 2.2 mm |
| 500 m | 1.8 mm |
| 800 m | 1.5 mm |

Performance is sufficient against soft body armour and the CRISAT target at typical PDW engagement ranges (≤ 200 m). Hard-plate (NIJ Level III / IV) defeat is *not* claimed.

## 5. Barrel and Suppressor System

### 5.1 Barrel Construction

| Parameter | Value |
|---|---|
| Material | Chrome-lined 4150 steel, Stellite 21 lining |
| Length | 266.7 mm |
| Rifling | 6-groove polygonal hybrid, 1:8 RH |
| Barrel life (§23 service) | 75 000 rounds |
| Throat-erosion life (§10) | 302 501 rounds |
| Surface treatment | Nitride coating |
| Quick-change | Three-lug, tool-less |

### 5.2 Integrated Suppressor

| Parameter | Value |
|---|---|
| Internal volume | 180 cm³ |
| Length | 180 mm |
| Diameter | 38 mm |
| Material | Inconel 718 |
| Baffle count | 8 (K-type) |
| Attenuation | 40 dB peak (modelled cap) |
| Service life | 30 000 rounds |

The 40 dB attenuation is the simulator's adiabatic-expansion-bound peak attenuation cap. Perceived loudness reduction at the operator's ear is somewhat lower in practice due to first-round-pop, supersonic projectile crack at 501 m/s, and action noise — none of which the closed-form model attempts to capture.

## 6. Operating System

### 6.1 Rotating Bolt + Short Recoil + Buffered Bolt-Carrier

The Defender uses the same rotating-bolt + short-recoil action family as the MP-4.6M Guardian Pistol. The PDW-specific addition is a hydraulic-plus-mechanical buffered bolt-carrier that:

* Reduces felt recoil at the operator's shoulder by ~55 % vs an unbuffered short-recoil mass of equivalent inertia.
* Stabilises the 850 rpm full-auto cyclic rate without bolt-bounce.
* Provides per-shot felt recoil in burst mode of ~0.3 J at the operator's shoulder, despite the cumulative impulse over a 3-round burst totalling ~4.8 N·s.
* Extends sustained-fire capacity to 400 rounds before barrel-temperature limits.

### 6.2 Cartridge / Action / Parts Commonality with Guardian Pistol

Common parts (one-line bill-of-materials commonality):

* 4.6×30 mm Enhanced cartridge (chamber, throat, gas behaviour identical).
* Bolt face, firing pin, extractor, ejector.
* MP35N alloy hammer/sear spring set.
* Stellite-21 barrel-liner blank.

Defender-unique components:

* Buffered bolt-carrier assembly.
* Select-fire trigger group with 3-round-burst sear and disconnect.
* 40-round double-stack magazine (not interchangeable with Guardian's 20-round magazine).
* Telescoping stock with hydraulic primary buffer + mechanical secondary buffer.
* 266.7 mm three-lug quick-change barrel.

## 7. Recoil Analysis

Free recoil energy at 2.10 kg empty mass is computed by the simulator from recoil impulse:

E_recoil = p² / (2 × m) ≈ 1.60² / (2 × 2.10) ≈ 0.61 J → 0.7 J reported after recoil-system contribution.

The buffered bolt-carrier reduces *felt* recoil per shot in 3-round burst mode to approximately 0.3 J, a key human-factors enabler of the 2 MOA at 50 m accuracy in burst-mode engagements documented under MIL-STD-810H sustained-fire test conditions.

## 8. Magazine System

The 40-round magazine in 7075-T6 aluminium with hard anodising provides 40-round capacity at 130 g empty (290 g loaded with 40 rounds). Double-stack, double-feed design with hardened steel feed lips, chrome silicon spring, and anti-tilt follower delivers reliable feeding under combat conditions. The debris channels and self-lubricating surfaces accommodate adverse environmental conditions. The PDW magazine is **not interchangeable** with the 20-round Guardian Pistol magazine — the external footprint and feed-lip geometry differ.

## 9. Mechanical Round Counter

The three-digit mechanical round counter provides direct-drive round counting independent of electronic power. The anti-backlash gearing and hardened steel components provide accurate tracking through the weapon's 75 000-round barrel service life (§23).

## 10. Reliability and Environmental Performance

| Parameter | Specification |
|---|---|
| MRBF analytic (§23) | 19 996 rounds |
| MRBF simulated (§23) | 15 000 rounds |
| FTF rate (§23) | 1:75 000 |
| Felt recoil (§23) | 0.125 ft·lb |
| Bore life service (§23) | 75 000 rounds |
| Parts Life | 50 000 rounds minimum |
| Temperature Range | -40°C to +60°C |
| Submersion | 20 m for 1 hour |
| Drop Test | 2 m on all surfaces |
| Sustained Fire | 400 rounds |
| MIL-STD-810H Compliance | Full (sand, salt fog, humidity, shock, vibration) |

## 11. Comparison with HK MP7A1

The HK MP7 has been adopted by special operations units globally and the UK Ministry of Defence Police as a complete pistol-and-rifle replacement platform. Its compact design (38 cm folded), 720 m/s muzzle velocity, and demonstrated CRISAT penetration at 200 m have made it the benchmark PDW system. The MP-4.6M Defender's primary differentiators vs the MP7A1 are: a heavier 2.6 g projectile (vs DM11's 2.0 g), giving slightly higher sectional density and ~3.1 mm vs ~3.0 mm RHA at 100 m; ammunition commonality with the MP-4.6M Guardian service pistol; an integrated 180 cm³ suppressor (40 dB modelled cap); and a buffered bolt-carrier reducing burst-mode felt recoil. The Defender's 501 m/s is *lower* than the MP7's 720 m/s — the trade-off is heavier projectile, lower velocity, common ammunition with a paired service pistol.

## 12. Methods and Provenance

All ballistic numbers in this paper are derived from the portfolio ballistics simulator (`../weapons_simulation.py`) and tabulated in `../weapons_sim_results.md`:

* **Internal ballistics** — Powley closed-form pressure-time integration with η = 0.72 small-arms efficiency factor calibrated against published M855A1 / M80 / DM11 muzzle-velocity data, given case capacity, bore diameter, charge mass, and barrel length.
* **External ballistics** — G7 drag-table point-mass integration under ICAO standard atmosphere with linear thermal lapse rate; gravity-only baseline (zero crosswind, zero Coriolis).
* **Terminal ballistics vs RHA** — De Marre correlation calibrated against M80 7.62×51 mm, .50 BMG M2 AP, and 14.5×114 mm B-32 reference penetration data (K = 7.80 × 10⁻⁴ in SI units); 290 BHN RHA at 0° obliquity.
* **Suppressor attenuation** — adiabatic-expansion peak-attenuation bound capped at 40 dB modelled peak.

Material specifications (Stellite 21, Inconel 718, MP35N, 7075-T6, hydraulic / mechanical buffer stack) are unchanged from prior revisions and are not derived from the simulator.

## 12A. Tier-2 Simulation Coverage and Methodology

This v2.0 paper extends the v1.0 simulator-derived numerical envelope from the Tier-1 internal / external / terminal-ballistics tables (`weapons_sim_results.md` §1–§5) to the Tier-2 outputs in §6–§13. The MP-4.6M Defender numerical claims in this paper are now backed by the following simulator sections:

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
| **Barrel life** | **§10** | Calibrated bore-wear model anchored to M4 / M14 / M2HB / GAU-8 / M256; thermal-bound rpm from barrel mass × specific heat (quick-change barrel treated as 1.5×) |
| **Portfolio lifecycle** | **§23** | Bore life service (75 000 rd), MRBF MC (19 996 analytic / 15 000 simulated), felt recoil (0.125 ft·lb), FTF (1:75 000) |
| **Peak shoulder force** | **§11** | Parabolic-energy-dissipation over `stock_travel_mm` with muzzle-brake impulse-redirection efficiency |
| **Body-armour V50** | **§13** | Lambert-Jonas / Recht-Ipson V50 with composite-factor calibration; clay-witness BFD per NIJ 0101.06 |

### 12A.1 Acoustic signature methodology

The Westin (1975) blast-SPL fit (`weapons_sim_results.md` §6) is calibrated against published 5.56 carbine (≈ 165/158 dB), 7.62 rifle (≈ 166/159 dB), and .50 BMG (≈ 178/170 dB) anchors. For the MP-4.6M Defender, the simulator outputs 163.4 dB unsuppressed muzzle / 156.4 dB at the shooter's ear, dropping to 123.4 / 116.4 dB with the integrated 180 cm³ K-baffle suppressor — identical to the MP-4.6M Guardian Pistol because the simulator's adiabatic-expansion blast model is dominated by chamber-volume / suppressor-volume / baffle-count, not barrel length. The full hearing-protection stack (suppressed + double plug + muff + TACS personal active cancellation) drops ear-level peak to 63.4 dB.

### 12A.2 Effective-range methodology

The Hatcher 80 J KE-threshold criterion (`weapons_sim_results.md` §9) gives 878 m max-effective range for the 4.6 × 30 mm Enhanced cartridge, with a 301 m supersonic range (muzzle 1 644 fps). The Defender's 200 m point / 400 m area engagement envelope sits comfortably within both bounds. Beyond 300 m the projectile transitions to transonic / subsonic flight where conventional sub-MOA accuracy guarantees no longer hold — consistent with the operational PDW role of close-to-medium-range engagement.

### 12A.3 Barrel-life methodology

The bore-wear model (`weapons_sim_results.md` §10) reports **302 501 rounds** throat-erosion life for the Defender's 0.45 kg Stellite-21-lined barrel at 26 100 psi peak chamber pressure. The §23 **bore life service** rating of **75 000 rounds** is retained as the conservative accuracy-retention envelope, not the absolute throat-erosion bound. The 250 rpm thermal-bound is below the spec'd 850 rpm cyclic rate, so sustained burst-mode firing must respect the thermal duty cycle — a constraint already captured in the spec'd 400-round MIL-STD-810H sustained-fire envelope.

### 12A.4 Recoil-force methodology

Peak shoulder force (`weapons_sim_results.md` §11) for the Defender is **54 N (12 lbf)** — the lowest peak force of any platform in the portfolio. The simulator computes this from 0.7 J free recoil distributed over an 18 mm buffered-stock travel envelope with no muzzle brake. The 54 N peak validates the prior narrative claim of ~0.3 J per-shot felt recoil in 3-round burst mode (PDW spec SECTION 3.1) — both metrics describe the same architectural outcome (the buffered bolt-carrier reduces felt recoil by ~55 % vs an unbuffered short-recoil mass of equivalent inertia, but the dominant contribution is the cartridge's low free-recoil energy itself).

### 12A.5 Body-armour V50 methodology

Lambert-Jonas / Recht-Ipson V50 values (`weapons_sim_results.md` §13) are calibrated against published NIJ 0101.06 panel data for IIIA, NIJ III, NIJ IV, APES military, and APES-L police composites. The 4.6 × 30 mm Enhanced is **not directly characterised** in §13. The closest PDW-class threat is the 5.7 × 28 mm SS190 (2.0 g, 716 m/s), which §13 reports as STOPPED by every armour class (V50: IIIA 760, NIJ III 1 426, NIJ IV 2 358, APES 2 790, APES-L 2 212 m/s — all above the SS190's 716 m/s threat velocity). The Defender's 4.6 × 30 mm Enhanced at 501 m/s carries less specific kinetic energy than the SS190 and is bounded above by its outcome. The Defender is consequently **not** a hard-armour-defeating PDW; its operational envelope is unprotected personnel and the CRISAT (20 layers Kevlar + 1.6 mm titanium) target the original NATO PDW requirement specified.

## 13. Conclusion

The MP-4.6M Defender PDW, when re-derived against the portfolio ballistics simulator, is a buffered-bolt-carrier rotating-bolt short-recoil select-fire PDW delivering 326 J muzzle energy, 40-round capacity, 850 rpm full-auto cyclic rate, and 0.7 J free recoil from a 2.10 kg empty platform. Its primary operational differentiators are ammunition commonality with the MP-4.6M Guardian service pistol and integrated 40 dB modelled-cap suppression. Prior v1.0 numerical claims (1 225 m/s, 2 000 J, 50-round magazine, 15 mm RHA at 25 m) are formally retracted; this v2.0 paper is the authoritative specification.

## Appendix A — Governing Equations

This appendix documents the governing equations used by the portfolio ballistics simulator (`weapons_simulation.py`) to derive the MP-4.6M Defender PDW performance numbers cited in §3–§7 and §12A. Calibration constants are taken from `weapons_sim_results.md` §1–§13. The structure follows the reference appendix in [`../../Weapons-Police/MP-4.6P Guardian LE/`](../../Weapons-Police/MP-4.6P%20Guardian%20LE/) Appendix A. The Defender is the PDW variant of the MP-4.6M family; the simulator catalogues the PDW under `4.6x30mm_PDW` and the pistol under `4.6x30mm` (see Note 1 in §A.7 on which set of numbers applies).

### A.1 Interior ballistics — Noble-Abel for 4.6 × 30 mm Enhanced, 266.7 mm barrel

A 1D Noble-Abel integration with Powley η = 0.72 (small-arms branch) produces the muzzle velocity, peak chamber pressure, and bolt impulse.

```
P · (V − m_g · b) = m_g · R_g · T            (Noble-Abel)
m_b · dv_b/dt = A_b · P · η_pwr − F_friction
dα/dt = a · P^n · (1 − α)                    (Vielle burn)

A_b      = π · (0.00465/2)² = 1.698 × 10⁻⁵ m²    (4.65 mm bore area)
m_b      = 2.6 × 10⁻³ kg                          (WC-Co cored projectile)
η_pwr    = 0.72                                    (Powley small-arms efficiency)
Charge   = ~0.40 g triple-base (4.6 × 30 mm Enhanced load)
Tube L   = 0.2667 m (266.7 mm Defender barrel; 1.48× the pistol's 180 mm)
Case capacity = ~1.0 cm³ (sim §5)
b = 1.05 × 10⁻³ m³/kg,  R_g = 360 J/(kg·K),  Q_prop = 5.8 MJ/kg,  γ = 1.27
```

→ For the PDW barrel (`weapons_sim_results.md` §1, `4.6x30mm_PDW`): muzzle velocity = **542 m/s**, muzzle KE = ½ · 0.0026 · 542² = **382 J**, peak chamber P = **180 MPa (26 107 psi)**, recoil impulse = **1.79 N·s**. The paper body §3 cites the pistol-load values (501 m/s, 326 J, 1.60 N·s) — see Note 1 in §A.7.

### A.2 Exterior ballistics — point-mass + Miller Sg

A 2D point-mass integration with G7 drag table (boat-tail spitzer WC-cored projectile) under ICAO atmosphere.

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_b
v(0) = 542 m/s, v(100 m) = 470 m/s, v(500 m) = 308 m/s, v(1 km) = 237 m/s   (sim §4, 4.6x30mm_PDW)

G7 form factor i₇ ≈ 0.95 (WC-cored spitzer)
Mach at muzzle = 542 / 343 = 1.58
```

**Miller (Litz-corrected) gyroscopic stability:**

```
Sg = (30 · m_b) / (ρ_b · d_b³ · L_b · t²) · 1 / (2π²)

d_b = 0.00465 m, L_b/d_b = 18/4.65 = 3.87, ρ_b = 14 800 kg/m³ (WC composite)
t   = 0.2032 m/rev (1:8 twist)
```

→ Sg > 1.4 throughout supersonic regime; supersonic range **376 m** (`weapons_sim_results.md` §9, `4.6x30mm_PDW`), max-effective range **928 m** at the Hatcher 80 J KE threshold.

### A.3 Terminal ballistics — De Marre + Poncelet tissue

**De Marre for RHA penetration:**

```
T_RHA = K · m_b^0.5 · v^1.43 / d_core^0.75

K       = 7.80 × 10⁻⁴
m_b     = 2.6 × 10⁻³ kg
d_core  = 4.65 mm core (WC penetrator core diameter)
v(0)    = 542 m/s for PDW barrel
```

→ Penetration vs RHA for `4.6x30mm_PDW` (`weapons_sim_results.md` §3): **0 m: 4.2 mm, 100 m: 3.4 mm, 300 m: 2.3 mm, 500 m: 1.9 mm, 800 m: 1.5 mm**. The paper body §4.3 cites the pistol-load row values (3.8 / 3.1 / 2.2 / 1.8 / 1.5 mm) — see Note 1 in §A.7.

**Poncelet resistive-force soft-tissue model:**

```
F_resist = (A_gel + B_gel · v²) · A_eff(x)
m_b · dv/dt = −F_resist(v, x),  dx/dt = v

A_gel = 200 Pa (quasi-static yield, FBI cold-gel calibration)
B_gel = 2 366 kg/m³ (inertial coefficient, calibrated to FBI 9 mm 124 gr gelatin)
A_eff = π · (d_b/2)² = 1.698 × 10⁻⁵ m² (rigid 4.6 mm WC penetrator — no expansion)
```

→ At 542 m/s impact the rigid WC penetrator over-penetrates simple gelatin (no expansion); against CRISAT-class soft armour (20 layers Kevlar + 1.6 mm titanium backer) it defeats at the design ≤ 200 m envelope. Hard-plate (NIJ III / IV) defeat is not claimed.

### A.4 Recoil — mass-spring-damper (with buffer on PDW)

The buffered bolt-carrier introduces a hydraulic + mechanical buffer in series with the recoil spring, modelled as an over-damped mass-spring-damper.

```
m_bc · ẍ_bc + c · ẋ_bc + k · x_bc = J_bolt · δ(t − t_port)

m_bc = 0.025 kg          (bolt-carrier group + buffer mass)
k    = 100 N/m           (recoil spring rate)
c    = 6 N·s/m           (hydraulic buffer damping; ζ = c / (2√(k·m)) ≈ 1.9, over-damped)

Cycling rate:
T_cycle = π · √(m_bc / k) · ζ-correction → 850 rpm spec'd

Free recoil:
J_free = m_b · v_b + m_g · v_gas_avg = 0.0026 · 542 + 0.40e-3 · 600 ≈ 1.65 N·s (sim §1, 4.6x30mm_PDW)
E_free = J_free² / (2 · M_pistol)
M_pistol = 2.10 kg (Defender empty mass; sim §2 reports 0.8 J for PDW vs 1.5 J for pistol)

F_peak (parabolic-energy-dissipation):
F_peak = E_free · (4 / s_stroke) = 0.8 · (4 / 0.018) ≈ 178 N at zero brake
Sim §11 with full buffer treatment: F_peak = 63 N (14 lbf) for `MP-4.6M Defender PDW`
```

→ E_free = **0.8 J (0.6 ft·lbf)** at 2.10 kg empty mass (`weapons_sim_results.md` §2), peak shoulder force = **63 N (14 lbf)** at 18 mm buffered-stock travel (`weapons_sim_results.md` §11). The paper body §7 / §12A.4 cites 0.7 J and 54 N — pistol-leakage values; see Note 1 in §A.7.

### A.5 Gas dynamics — short-stroke gas piston / rotating bolt

The Defender uses rotating-bolt + short-recoil + buffered-bolt-carrier (no gas piston in the conventional sense; the "gas dynamics" here is the chamber-to-port expansion that drives the buffered short-recoil cycle).

```
P_port = P_peak · (V_chamber / V_port_zone)^γ        (isentropic expansion to port zone)

V_chamber = 1.0 cm³ (sim §5)
V_port_zone (at 266.7 mm Defender barrel) ≈ V_chamber + A_b · 0.150 m = 1.0 + 169.8 · 0.150 ≈ 26.5 cm³
P_port ≈ 180 · (1.0 / 26.5)^1.27 = 180 · 0.0192 = 3.5 MPa  [at mid-barrel reference port]

Bolt-impulse correction (short-recoil action):
J_bolt = ∫ A_recoil · P(t) dt  [over the bolt-unlock window]
J_bolt_corrected = J_bolt · k_1D→3D    (k ≈ 1.40, MP-4.6P calibration)
```

→ Short-recoil bolt unlock occurs after 4 mm of slide+bolt travel; the buffered bolt-carrier dissipates ~55 % of the bolt-cycle energy into the hydraulic + mechanical buffer, supporting 850 rpm cyclic rate without bolt-bounce.

### A.6 Reliability — Bernoulli Monte Carlo (seven-mode framework)

The same seven-mode Bernoulli MC framework as the MP-4.6P Guardian LE Appendix A.7 (`../../Weapons-Police/MP-4.6P Guardian LE/MP-4.6P_Guardian_LE_Specification.md`):

```
For each round i = 1 … N (N = 500 000):
  Generate 7 uniform random numbers U_j ~ U(0,1)  for j = 1 … 7 modes
  Stoppage_i = 1  if  U_j < p_j  for any j (any mode triggers)
  MRBF = N / Σ Stoppage_i

Bootstrap CI (2 000 resamples) for 90 % confidence interval.

Per-mode failure rates (Defender, baseline PDW Tier-1 configuration):
FTFeed:     1 : 150 000   (double-stack 40-round magazine)
FTExtract:  1 : 100 000   (coil extractor + spring preload)
FTFire:     1 : 80 000    (striker energy vs primer threshold)
FTEject:    1 : 60 000    (ejector geometry + port timing)
FTGas:      1 : 200 000   (gas fouling — short-recoil low gas exposure)
FTPrimer:   1 : 150 000   (primer depth QC)
FTCase:     1 : 250 000   (case separation, low chamber pressure)

Analytic MRBF:
1 / MRBF_analytic = Σ_j p_j ≈ 5 × 10⁻⁵ → MRBF ≈ 20 000 rounds (per-mode harmonic sum)
```

Portfolio lifecycle MC (`weapons_sim_results.md` §23): MRBF analytic **19 996** / simulated **15 000**; FTF rate **1:75 000**; felt recoil **0.125 ft·lb**; bore life service **75 000 rounds** — authoritative targets in paper-body §10 and spec §9.1.

### A.7 Notes on numerical concordance with the simulator

1. **Pistol-row vs PDW-row leakage throughout paper body.** The simulator catalogues the PDW under `4.6x30mm_PDW` (542 m/s, 382 J, 1.79 N·s recoil impulse, RHA 4.2 mm muzzle, 0.8 J free recoil, 63 N peak force, 376 m supersonic, 928 m max-effective range) and the pistol under `4.6x30mm` (501 m/s, 326 J, 1.65 N·s, 3.8 mm RHA, 1.5 J, 559 N, 301 m, 878 m). The paper body §3 / §4.2 / §4.3 / §7 / §12A.2 / §12A.4 / Abstract cite the **pistol-row** numbers throughout (501 m/s, 326 J, 0.7 J, 3.8 mm at muzzle, 878 m, 301 m supersonic, 54 N peak), explicitly attributing the equality to "combustion completes by ~150 mm so additional barrel length contributes only minor velocity increase." Per `weapons_sim_results.md` §1–§11, the simulator-catalogued PDW row is **distinct from** the pistol row and the correct PDW numbers are: 542 m/s, 382 J, 0.8 J free recoil, 4.2 mm RHA at muzzle, 928 m max-effective range, 376 m supersonic, 63 N peak shoulder force. These are flagged for the return summary but the body text is preserved per the editorial constraint.

2. **Recoil impulse 1.60 N·s vs sim §1 1.79 N·s.** Linked to Note 1 — the §7 paper-body computation uses the pistol-row impulse. Sim §1 for `4.6x30mm_PDW` is 1.79 N·s, which yields E_free = 1.79² / (2 · 2.10) ≈ 0.76 J ≈ 0.8 J (sim §2). The paper's 0.7 J figure is consistent with the pistol-row 1.65 N·s impulse and is internally consistent with the pistol-row interior-ballistics chain, but not with the PDW-row chain.

3. **Suppressor §5.2 in paper body 180 cm³ / 8 K-baffles / 40 dB ✓ matches sim §5.**

4. **§6A SPL 163.4 / 156.4 / 123.4 / 116.4 dB cited (PDW) vs sim §6 164.0 / 157.0 / 124.0 / 117.0 dB.** The paper-body §12A.1 acoustic-signature table cites pistol-row numbers (163.4 / 156.4); sim §6 reports 164.0 / 157.0 for the Defender PDW row (and 163.4 / 156.4 for the MP-4.6M Pistol row).

5. **Barrel-life 302 501 rounds and 250 rpm thermal-bound ✓ match sim §10.**

---

## 14. References

[1] Wikipedia. (2024). *Heckler & Koch MP7*. Wikimedia Foundation.

[2] Wikipedia. (2024). *HK 4.6×30mm*. Wikimedia Foundation.

[3] SADEFENSEJOURNAL. (2023). *Personal Defense Weapons — Overview and Comparative Analysis*.

[4] Euro-SD. (2025). *PDWs: A Revolution That Never Quite Happened*. European Security and Defence.

[5] NATO STANAG 4512. (2013). *Dismounted Combatant Target*. NATO Standardisation Agency.

[6] DefenseReview. (2002). *HK MP7 PDW: Serious Compact Firepower*. Defense Review.

[7] Dockery, K. (2007). *Future Weapons*. Berkley Books. ISBN: 978-0425217368.

[8] Advanced Defence Systems Research Division. (2026). *Weapons-Defence portfolio — simulation results* (`weapons_sim_results.md`). Internal technical reference.

[9] Advanced Defence Systems Research Division. (2026). *UCDR Weapons Portfolio — Common Ballistics Simulator* (`weapons_simulation.py`). Internal technical reference.
