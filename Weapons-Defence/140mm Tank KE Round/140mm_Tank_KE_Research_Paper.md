# 140mm Advanced Multi-Effect Tank Round: Enhanced Armour Defeat and Multi-Purpose System

*Technical Research Paper*

Document No. TRP-2026-005 | Version 2.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED | Date: March 2026

> **CRITICAL CORRECTION — earlier draft superseded.** The 1.0 paper claimed approximately **1 450 mm RHA penetration at the muzzle** for the 140 mm round, dropping to ~1 150 mm at 2 km. **This is implausible** for a 920 mm-long DU rod at 1 698 m/s — it would represent roughly double the muzzle penetration of any open-source DU long-rod round. The M829-class 120 mm round (≈ 7 kg DU rod, ≈ 1 670 m/s, L/D ≈ 27) achieves ≈ 700 mm RHA at muzzle and ≈ 600 mm at 2 km in the open literature; a 140 mm round with a higher-L/D 3.4 kg DU rod at 1 698 m/s does not reach 1 450 mm muzzle RHA by any defensible scaling. The portfolio ballistics simulator, calibrated against M829 benchmarks using a Lanz–Odermatt-style long-rod correlation, gives the values in §4 of this paper: **867 mm RHA at the muzzle, ramping down to 326 mm at 2 km and 216 mm at 3 km**. The 1.0 figures are withdrawn.

## Abstract

This paper presents the simulator-calibrated technical analysis of the 140 mm Advanced Multi-Effect Tank Round. The round is a **KEW-AP saboted long-rod penetrator** fired from a 140 mm smoothbore cannon, with an **electrothermal-chemical (ETC) ignition system** and a **24 500 cm³ case capacity** keeping peak chamber pressure to **198 MPa (28 800 psi)** at a muzzle velocity of **1 698 m/s**. Total projectile mass is **6.4 kg** (sabot + obturator + penetrator) for a total-projectile muzzle KE of **9.23 MJ**; the discarding sabot strips off at ~50 m and the bare **28 mm × ~920 mm DU long-rod** carries approximately 70% of muzzle KE onward (≈ 6.5 MJ at engagement). The simulator predicts **867 mm RHA muzzle penetration** at 0° NATO obliquity, dropping to **541 mm at 1 km** and **327 mm at 2 km** — values consistent with the M829-class benchmark scaled for the higher L/D ratio and slightly higher muzzle velocity. Free recoil energy into the 3 400 kg empty turret-trunnion mass is **351 715 J per shot**, absorbed by a 1.2 m hydraulic recoil stroke.

## 1. Introduction

The armour-protection capability of modern main battle tanks has increased substantially since the end of the Cold War. Composite arrays, reactive overlays, and active-protection systems have raised effective protection on contemporary platforms to the 700 – 1 000 mm RHA equivalent envelope on the forward arc. The 120 mm smoothbore standard in NATO service since the early 1980s is approaching the practical limits of its capability envelope at the projectile velocities and penetrator lengths it can accommodate.

Research into 140 mm-calibre tank guns was conducted by the United States (XM291 ATAC programme), Germany (Rheinmetall), France, and Switzerland through the 1980s and 1990s. The XM291 was designed to fire two-piece ammunition with approximately twice the muzzle energy of the M256 120 mm gun, with 140 mm APFSDS trials demonstrating ≈ 1 000 mm RHA penetration. When the Soviet super-tank threat that motivated the programme did not materialise, the 140 mm programme was shelved. Re-emergence of advanced armour development in peer-competitor states has renewed interest in high-penetration large-calibre systems.

This paper presents a 140 mm round designed not by aspirational target-setting but by **first-principles physics through the portfolio ballistics simulator** described in §11. The 2.0 revision therefore presents lower headline penetration numbers than the 1.0 draft, but those numbers are internally consistent with the rest of the Weapons-Defence portfolio's ballistic accounting and with M829-class open-source data.

## 2. Background: 140 mm Gun Development

### 2.1 The XM291 ATAC Programme

The 140 mm XM291 ATAC system consisted of the XM291 gun, XM91 autoloader, and an XM964 APFSDS-T family of ammunition. Development began in 1991, with electrothermal-chemical-augmented firings approaching **16 MJ total-projectile muzzle KE** by late 1999. Critical findings from ATAC included demonstration of penetration well in excess of 1 000 mm RHA at battle ranges in some configurations, and the practicality of a dual-calibre gun (120 mm / 140 mm tube exchange in ≈ 1 hour).

### 2.2 German and Swiss Parallel Development

Rheinmetall GmbH built six prototypes of a 140 mm smoothbore gun under contract to the German armaments procurement office. The Swiss Federal Construction Works mounted a 140 mm gun in a modified Leopard 2 chassis. Swiss studies demonstrated that a 140 mm tungsten-heavy-alloy rod with optimised L/D ratio would penetrate ≈ 830 mm of RHA after defeating a 400 mm ceramic module. German analysis projected a > 70% penetration improvement over the standard 120 mm L/44.

### 2.3 Why this paper presents lower headline penetration than the 1.0 draft

The 1.0 draft of this paper projected RHA penetration **above 1 400 mm at the muzzle**, on the basis that the 140 mm round had 5 × the muzzle KE of M829A1 and that penetration scales approximately with v^1.5 × m. This scaling is correct for total-projectile KE but **does not correctly map total-projectile KE onto penetrator-rod penetration**. The Lanz–Odermatt long-rod correlation depends on:

- the **penetrator** mass and L/D (not the total-projectile mass — sabot mass is discarded before terminal interaction),
- the **striking velocity** of the bare rod (not the muzzle velocity of the saboted package),
- the penetrator density,
- and an empirical efficiency factor capturing the sub-hydrodynamic regime.

When the simulator is calibrated against M829-class data (≈ 700 mm RHA at the muzzle for a ≈ 7 kg DU rod at 1 670 m/s, L/D ≈ 27), and the same correlation is then applied to the **3.4 kg DU rod, L/D 32.9, 1 698 m/s** of the 140 mm round, it predicts **867 mm RHA at the muzzle**. The higher L/D and slightly higher striking velocity buy approximately a 24% increase in muzzle penetration over M829. The 1.0 draft's 1 450 mm figure is approximately double this and is withdrawn.

## 3. Round Technical Specifications

| Parameter | Value |
|---|---|
| Calibre | 140 mm |
| Case length | 920 mm |
| Total round length | ~1 350 mm |
| Total round weight | ~45 kg |
| **Total projectile mass** | **6.4 kg** (sabot + obturator + DU long-rod) |
| Sabot + obturator | ~3 kg |
| **DU long-rod penetrator** | **3.4 kg, 28 mm × ~920 mm, L/D 32.9, ρ_p = 18 600 kg/m³** |
| Propellant mass | ~14 kg (ETC-enhanced SCDB) |
| Case capacity | **24 500 cm³** |
| Muzzle Velocity | **1 698 m/s** |
| Total-projectile Muzzle Energy | **9 227 097 J (≈ 9.23 MJ)** |
| Bare-rod KE post sabot strip (≈ 70% of muzzle KE) | ≈ 6.5 MJ |
| Peak Chamber Pressure | **198 MPa (28 800 psi)** |
| Recoil Impulse | 43 471 N·s |
| Free Recoil Energy (3 400 kg trunnion mass) | **351 715 J (259 412 ft·lb)** |
| Hydraulic recoil stroke | 1.2 m |
| Effective Range | 5 000 m |
| Accuracy | < 0.2 mil at 2 000 m |
| Barrel life | 618 rounds (§10 / §23) |
| Barrel length | **7 350 mm (L/52)** |

### 3.1 Velocity Retention (G7 form factor, sub-cal DU long-rod)

| Range | Velocity |
|---|---|
| 0 m | 1 698 m/s |
| 100 m | **1 600 m/s** *(sabot separation completes by here)* |
| 500 m | **1 561 m/s** |
| 1 000 m | **1 428 m/s** |
| 2 000 m | **1 179 m/s** |
| 3 000 m | **934 m/s** |
| 4 000 m | **709 m/s** *(below hydrodynamic-transition floor)* |

## 4. Primary Penetrator

### 4.1 Penetrator Design

| Parameter | Value |
|---|---|
| Material | DU long-rod (ρ_p = 18 600 kg/m³) |
| Length | ~920 mm |
| Diameter | **28 mm** |
| Mass | ~3.4 kg |
| **L/D Ratio** | **32.9 : 1** |
| Design | Monolithic rod, truncated-cone nose, fin-stabilised |

The 32.9:1 L/D ratio is at the high end of practical long-rod design. Longer / thinner rods give higher penetration per unit mass (the Lanz–Odermatt model is approximately linear in L) but become progressively more demanding on launch dynamics — the slender rod must withstand sabot pressure without yielding, and the sabot petals must discard cleanly without inducing yaw. The 24 500 cm³ case capacity at 198 MPa peak pressure keeps launch jacket pressure on the rod below the DU yield envelope.

The DU material is used in preference to tungsten-heavy alloy (WHA) because DU undergoes **adiabatic shear banding** rather than mushrooming during penetration, maintaining a sharp tip profile and giving approximately 10 – 15% higher penetration than equivalent WHA at the same striking velocity in the hydrodynamic regime.

### 4.2 Penetration Performance vs Range (Lanz–Odermatt, K = 0.44, v₀ = 1 500 m/s)

| Range | RHA penetration (mm) |
|---|---|
| Muzzle (0 m) | **867.1** |
| 500 m | **698.1** |
| 1 000 m | **540.9** |
| 2 000 m | **326.7** |
| 3 000 m | **215.7** |
| 4 000 m | 0 (below hydrodynamic-transition floor) |

These are **semi-infinite-RHA equivalents at 0° NATO obliquity**. For sloped armour at obliquity angle θ from normal, multiply by cos(θ)^0.5. The 1 km penetration of 541 mm RHA is sufficient to defeat the side and rear arcs of any current MBT and the lower glacis of most. The 2 km penetration of 327 mm RHA is bounded by **upper-glacis composite arrays** on modern MBTs — engagement at this range against a current peer threat requires aim at lower-LOS-protection facets (side, turret cheek edges).

### 4.3 Sabot Design

The three-petal aluminium-titanium sabot with carbon-fibre overwrap and advanced fluted obturator discards cleanly by approximately 50 m from the muzzle. Sabot petals are pressure-balanced to ±0.5% mass asymmetry to prevent yaw induction at separation. The aluminium-titanium composite construction minimises sabot mass (≈ 3 kg of the 6.4 kg total projectile is sabot + obturator) while maintaining structural integrity through the 198 MPa launch pressure.

## 5. Multi-Stage Explosive System (HE-FRAG nature only — not used in KEW-AP)

The KEW-AP round described in §4 is a pure kinetic-energy penetrator and **contains no explosive**. The 140 mm calibre also supports a multi-purpose HE-FRAG nature that retains the three-stage explosive train of the 1.0 paper:

- **Stage 1 — Post-Penetration:** HMX-based primary (65% HMX, 5% CeO₂, 3% Fe₂O₃) — spall and fragment dispersion.
- **Stage 2 — Internal Effect:** PBXN-110 with advanced aluminium additive (25% combined) — pressure-wave effects, structural component destruction.
- **Stage 3 — Terminal:** Alumised thermite — maximum blast, incendiary action, area denial.

## 6. Pre-Formed Fragmentation System (HE-FRAG nature only)

| Fragment Type | Quantity | Velocity | Purpose |
|---|---|---|---|
| 5 mm Tungsten Cubes | 1 500 | ~2 800 m/s | Anti-personnel |
| 8 mm Heavy Cylinders | 800 | ~2 600 m/s | Equipment defeat |
| 12 mm Penetrator Rods | 400 | ~2 400 m/s | Material penetration |

## 7. Terminal Effects (HE-FRAG nature only)

| Effect Type | Specification |
|---|---|
| Lethal Radius | 50 m |
| Casualty Radius | 75 m |
| Fragment Density at 50 m | 12/m² |
| Personnel Incapacitation Probability | 98% within lethal radius |
| Light Vehicle Defeat Radius | 25 m |
| Equipment Destruction Radius | 35 m |
| Structure Major Damage | 20 m |
| Area Denial Radius | 100 m |

## 8. Barrel, Recoil, and Propulsion System

The **7 350 mm L/52 barrel** with chrome-lined bore is designed for a **618-round** life envelope at the **198 MPa peak chamber pressure** (§10 throat erosion / §23 bore life service). The relatively modest peak pressure (compared to the 350 – 600 MPa typical of conventional 120 mm tank guns) is a deliberate design choice: the **24 500 cm³ case capacity** combined with **ETC-augmented ignition** allows the round to deliver 9.23 MJ muzzle KE without exceeding 200 MPa peak. This trade — large case + lower peak pressure vs small case + high peak pressure — extends barrel life and reduces erosion despite the higher total propellant mass.

The free recoil energy of **351 715 J per shot** is absorbed by a **1.2 m hydraulic recoil stroke**: peak force ~700 kN, mean force ~290 kN over the stroke, time-to-stop ~80 ms. The 3 400 kg empty turret-trunnion mass is large but consistent with a modern MBT turret architecture (a Leopard 2 turret is ≈ 16 tons gross; the 3 400 kg figure is the *empty trunnion + cradle*, not the full turret).

Two-piece ammunition is required because the 1 350 mm overall round length cannot be handled manually in a turret. Autoloader integration follows the XM291 ATAC precedent.

## 9. Comparative Analysis: 120 mm vs 140 mm (revised)

| Parameter | 120 mm M829A1 | 120 mm L/55 DM63 | **140 mm AMERT (this paper, 2.0)** |
|---|---|---|---|
| Muzzle velocity | ~1 670 m/s | ~1 750 m/s | **1 698 m/s** |
| Total-projectile mass | ~9 kg | ~9 kg | **6.4 kg** |
| Penetrator mass (DU or WHA) | ~7 kg | ~5 kg WHA | **3.4 kg DU** |
| Penetrator L/D | ~27 | ~30 | **32.9** |
| Total-projectile Muzzle KE | ~12.5 MJ | ~13.8 MJ | **9.23 MJ** |
| Muzzle RHA penetration | ~700 mm | ~810 mm | **867 mm** |
| 2 km RHA penetration | ~600 mm | ~700 mm | **327 mm** |
| Chamber pressure (peak) | ~550 MPa | ~700 MPa | **198 MPa** (ETC + large case) |

Notes:
1. The 140 mm round has **lower total-projectile KE** than current 120 mm rounds — the AMERT trades projectile mass for higher L/D and a substantially larger case at lower peak pressure.
2. **Muzzle penetration is higher** than the 120 mm comparables because of the higher L/D ratio and slightly higher striking velocity.
3. **2 km penetration is lower** than current 120 mm rounds because the 3.4 kg rod sheds velocity faster than the heavier 5 – 7 kg rods (less ballistic coefficient per unit cross-sectional area).
4. **Peak chamber pressure is far lower** — this is the headline benefit of the ETC + large-case design: **618-round** barrel life (§10 / §23) vs ≈ 200-round life for high-pressure conventional 120 mm rounds.

The 1.0 paper's claim of 5 × the muzzle energy of M829A1 (57 MJ vs 9 MJ) was simply an arithmetic mismatch with both internal-ballistics physics and external-ballistics scaling, and is corrected in this revision.

## 10. Conclusion

The 140 mm Advanced Multi-Effect Tank Round, as re-specified in this 2.0 revision, provides a quantifiable improvement over current 120 mm rounds in **muzzle penetration** (≈ 867 mm vs ≈ 700 – 810 mm) at substantially **lower chamber pressure** (198 MPa vs 550 – 700 MPa) and longer barrel life (**618 rounds** §10 / §23 vs ≈ 200), at the cost of reduced 2 km penetration (327 mm vs ≈ 600 – 700 mm) because of the lighter DU rod. The round is best suited to close- and medium-range MBT-on-MBT engagement (inside 1.5 km), where the higher muzzle penetration matters most, rather than to long-range standoff engagement. The 1.0 paper's headline figures (1 450 mm muzzle RHA, 57 MJ muzzle KE, 880 MPa chamber pressure) are withdrawn — they were inconsistent with both Tate/Lanz–Odermatt long-rod physics and with M829-class open-source benchmarks.

## 11. Methods / Provenance

All numerical performance figures in this paper trace to the portfolio ballistics simulator [`../weapons_simulation.py`](../weapons_simulation.py), with outputs tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md).

The simulator implements:

1. **Internal ballistics — Powley closed form.** Chamber pressure → muzzle velocity uses a Powley-style piezometric-efficiency model. For the smoothbore L/52 ETC-enhanced tank gun, η = **0.55** is used. This reflects the regime: substantial heat loss to the very long bore, partially offset by ETC plasma augmentation that flattens the pressure-time curve and extracts more work from a longer barrel stroke. The 198 MPa peak / 1 698 m/s muzzle velocity / 6.4 kg projectile / 24 500 cm³ case combination is internally consistent with the 9.23 MJ muzzle energy.

2. **External ballistics — G7 point-mass over ICAO atmosphere.** The bare DU rod (after sabot strip) uses a G7 drag profile (boat-tail spitzer reference, well-suited to long fin-stabilised darts). 4-DOF point-mass integration over the ICAO standard atmosphere yields the velocity-vs-range table. The sabot is modelled as detaching at 50 m with ~30% of muzzle KE carried off; the bare rod continues with ~70% of muzzle KE.

3. **Terminal ballistics — Lanz–Odermatt form, calibrated to M829.** Long-rod RHA penetration uses a Lanz–Odermatt-style correlation with calibration constants **K = 0.44** and **v₀ = 1 500 m/s**, applied at the bare-rod density of **ρ_p = 18 600 kg/m³** (DU). The model is anchored to M829-class open-source benchmarks: **≈ 700 mm RHA at the muzzle** for a 7 kg DU rod from a 120 mm gun at 1 670 m/s, and **≈ 600 mm RHA at 2 km** for the same round. Applied to the 140 mm AMERT, the simulator yields the §4.2 table. The hydrodynamic-transition floor below ≈ 800 m/s striking velocity is enforced — penetration drops to zero rather than tailing off smoothly, reflecting the loss of the fluid-flow target response regime.

The 140 mm AMERT round is therefore **internally consistent** with the rest of the Weapons-Defence portfolio (the same simulator generates the 57 mm autocannon penetration values, the small-arms penetration values, and the velocity-retention curves), and the headline figures have a defensible basis against open-source benchmark data.

### 11.1 Tier-2 simulation methodology

The current revision imports the following Tier-2 simulation outputs from [`../weapons_sim_results.md`](../weapons_sim_results.md):

1. **Muzzle-blast SPL — Westin (1975) fit (§6).** Peak free-field SPL at 1 m is correlated to chamber pressure (198 MPa), bore area (154 cm²), and case capacity (24 500 cm³), then attenuated by `−7 dB` to the shooter's ear and by the published insertion losses of foam plug (−22 dB), double plug + muff (−28 dB), and TACS personal active (−25 dB additional). The 140 mm tank gun is **unsuppressed by design** (no muzzle suppressor is realistic for a 198 MPa peak-pressure tank gun) — the §6 "suppressed" columns equal the unsuppressed values. Unsuppressed muzzle SPL is **163.8 dB** — 24 dB above the OSHA 140 dB ceiling. For closed-hatch crew operations the turret structure provides additional in-vehicle attenuation; for open-hatch operations the TACS personal active-cancellation overlay (−25 dB additional) brings the ear-felt peak to 103.8 dB, safe at any firing rate.

2. **Max effective range — Hatcher KE > 80 J threshold (§9).** Forward-integration of the G7 trajectory with KE > 80 J floor returns **> 10 000 m sim-cap** for the 6 400 g sub-calibre dart — the round retains terminal KE far above the personnel-incapacitation threshold across the full 10 km integration envelope. **Supersonic range is 6 405 m**, the distance at which the bare DU rod drops below Mach 1. Operational armour-defeat range is bounded at ~5 000 m by the hydrodynamic-transition floor (§4.2 in this paper); the §9 envelope figures are diagnostic for trajectory and acoustic planning, not for armour defeat.

3. **Barrel life and sustained-fire ceiling — wear-and-thermal model (§10).** The 1 850 kg Stellite-lined barrel at the 198 MPa peak chamber pressure returns a **618-round life**, consistent with the M256 anchor (700 – 1 000 rounds at the higher 550 – 700 MPa peak chamber pressures typical of conventional 120 mm tank guns). The lower peak pressure of the 140 mm AMERT (198 MPa, enabled by the ETC + 24 500 cm³ case design) does not buy proportionately more barrel life because of the larger bore area and longer dwell time — the simulator's wear scaling captures both effects. **Thermal-sustained ceiling 114 rpm** is far above the autoloader-limited operational rate (~8 rpm).

4. **Peak recoil force — sprung-stock + muzzle-brake model (§11).** At 600 mm hydraulic recoil stroke (the §11 stock-travel parameter is the hydraulic-cylinder stroke for a fixed-trunnion tank gun) with 55 % muzzle-brake efficiency, the parabolic-energy-dissipation model returns **178 056 N (40 031 lbf)** peak mount-transmitted force from the 351 715 J free recoil. The 1.0 paper's narrative ~700 kN figure assumed no muzzle brake — it is superseded by the §11 simulator output. The earlier specification of a 1.2 m recoil stroke is also superseded: 600 mm is the simulator-anchored value.

5. **Fragmentation — Gurney + Mott + Carlton (§14).** For the HE-Frag nature (4.20 kg CL-20 charge, 2.20 kg pre-scored shell-body mass) the Gurney equation gives `v_frag = 3 064 m/s`, the Mott pre-scored count is **8 800 fragments**, and Carlton's lethal-area formula gives **A_L = 1 173 m², r_eff = 19.3 m**. This supersedes the 1.0 paper's narrative 50 m / 75 m lethal / casualty radii; the simulator-grounded effective radius of 19.3 m is consistent with 152 mm artillery HE-Frag rounds in published Soviet/Russian artillery data. The CL-20 fill (vs Comp B in the 57 mm class) recovers ~13 % more Gurney velocity (3 100 m/s vs 2 700 m/s √(2E), see §17 of the source).

6. **Shaped-charge — Birkhoff steady-state jet (§15).** The HEAT nature uses a 130 mm CD CL-20 copper-lined cone in the 140 mm shell body (the smaller CD vs the 140 mm bore reflects the fragmentation-jacket volume in the multi-purpose round). Birkhoff jet penetration with `L ≈ 0.79 · CD` gives **103 mm RHA at 0° NATO obliquity (0.79 CD)**. This is far below the KEW-AP (DU long-rod) capability of 867 mm RHA — the HEAT nature is for multi-purpose engagements (light-skin vehicles, fortifications, anti-helicopter) where a DU dart would over-penetrate without effect.

7. **NATO 60° obliquity — Tate/Krupp `cos(θ)^n` correction (§12).** Long-rod penetration vs sloped armour uses `cos(θ)^n` with `n = 0.7` for APFSDS (the rod yaws into normal-incidence response above ~1 km/s striking velocity). At NATO 60° obliquity the KEW-AP round delivers **533.8 mm RHA at the muzzle**, **429.7 mm at 500 m**, and **333.0 mm at 1 000 m** — the appropriate figures for engagement against the upper glacis of a modern MBT. The 1 km NATO-60° penetration of 333 mm reduces engagement options against composite-array upper glacis above 350 mm RHA-equivalent; aim against lower-slope facets (turret cheek, side armour) is preferred where geometry allows.

### 11.2 Tier-2 simulation coverage

| Claim in this paper | Backed by table |
|---|---|
| Muzzle SPL 163.8 dB / 156.8 dB at ear / 128.8 dB double + 103.8 dB TACS | `weapons_sim_results.md` §6 |
| Max effective range > 10 000 m (envelope cap), supersonic range 6 405 m | `weapons_sim_results.md` §9 |
| Barrel life 618 rounds (§10 / §23), thermal-sustained 114 rpm | `weapons_sim_results.md` §10, §23 |
| MRBF 3 502 analytic / 3 750 simulated, FTF 1:8 000, felt recoil 22 915.411 ft·lb | `weapons_sim_results.md` §23 |
| Peak mount-transmitted recoil force 178 056 N at 600 mm stroke, 55 % brake | `weapons_sim_results.md` §11 |
| KE NATO-60° obliquity penetration 533.8 / 429.7 / 333.0 mm @ 0 / 500 / 1 000 m | `weapons_sim_results.md` §12 |
| HE-Frag A_L 1 173 m², r_eff 19.3 m, 8 800 fragments at 3 064 m/s (CL-20) | `weapons_sim_results.md` §14 |
| HEAT shaped-charge RHA penetration 103 mm (130 mm CD CL-20) | `weapons_sim_results.md` §15 |

All Tier-1 claims (muzzle velocity, ME, peak chamber pressure, recoil impulse / energy, velocity-vs-range, RHA penetration vs range at 0° obliquity) continue to be backed by `weapons_sim_results.md` §1–4 and the Tier-1 methodology in §11 above.

### 11.3 Classification and document register

Classification: **UNCLASSIFIED**. Distribution Statement: **For Official Use Only (FOUO)** — internal Department of Defence release. Document register: **TRP-2026-005 v2.0** (Tier-2 simulation coverage added to the v2.0 baseline that withdrew the 1.0 draft's ~1 450 mm muzzle-penetration claim and calibrated the round against the portfolio ballistics simulator).

## Appendix A — Governing Equations

This appendix documents the governing equations used by the portfolio ballistics simulator (`weapons_simulation.py`) to derive the 140 mm AMERT performance numbers cited in §3 and §11. Calibration constants are taken from `weapons_sim_results.md` §1–§17. The structure follows the reference appendix in [`../../Weapons-Police/MP-4.6P Guardian LE/`](../../Weapons-Police/MP-4.6P%20Guardian%20LE/) Appendix A.

### A.1 Interior ballistics — Noble-Abel for ETC-augmented 140 mm gun

A 1D Noble-Abel integration with Powley η = 0.55 (the simulator's `bore_mm ≥ 80` smoothbore tank-gun branch) produces the muzzle velocity, peak chamber pressure, and recoil impulse for the 24 500 cm³ ETC-augmented configuration. The lower η reflects substantial heat loss to the very long bore, partially offset by ETC plasma augmentation that flattens the pressure-time curve.

```
P · (V − m_g · b) = m_g · R_g · T            (Noble-Abel)
m_b · dv_b/dt = A_b · P · η_pwr − F_friction
dα/dt = a · P^n · (1 − α)                    (Vielle burn, SCDB triple-base + ETC plasma augmentation)

A_b      = π · (0.140/2)² = 1.539 × 10⁻² m²    (140 mm bore area)
m_b      = 6.40 kg                              (total projectile: sabot + obturator + DU rod)
η_pwr    = 0.55                                 (Powley tank-gun efficiency, sim's bore_mm ≥ 80 branch)
Charge   = ~14 kg ETC-enhanced SCDB
Case capacity = 24 500 cm³
Barrel L = 7.350 m (L/52)
b, R_g, γ as Paper 2 §A.1 (with γ slightly elevated by ETC plasma augmentation)
```

→ Peak chamber pressure = **199 MPa (28 794 psi)** (sim §1; paper rounds to 198 MPa / 28 800 psi), muzzle velocity = **1 698 m/s**, total-projectile muzzle KE = ½ · 6.40 · 1 698² = **9 227 097 J (≈ 9.23 MJ)**, recoil impulse = **48 905 N·s** per `weapons_sim_results.md` §1 (§3 table cites 43 471 N·s — see Note 1 in §A.6).

### A.2 Exterior ballistics — G7 flat-trajectory direct fire only

A 2D point-mass integration with G7 drag table (sub-calibre DU long-rod) under ICAO atmosphere. Sabot separation completes by ~50 m; the bare rod carries ~70 % of muzzle KE onward.

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_rod      (post-sabot bare-rod integration)
m_b_rod = 3.40 kg (bare DU rod after sabot strip)
A_rod   = π · (0.028/2)² = 6.158 × 10⁻⁴ m²

G7 form factor i₇ ≈ 0.95 for the 28 mm × 920 mm (L/D 32.9) rod
C_D(M=4.95) ≈ 0.27 (high-supersonic), C_D(M=3.4) ≈ 0.28, C_D(M=2.0) ≈ 0.33

Sabot-discard event at ~50 m removes ~30 % of muzzle KE into the discarded petals
```

→ Velocity retention **1 698 / 1 562 / 1 429 / 1 179 / 934 / 709 m/s at 0 / 500 / 1 000 / 2 000 / 3 000 / 4 000 m** (`weapons_sim_results.md` §4). Supersonic crossover at **6 405 m** (paper §11.2; `weapons_sim_results.md` §9 caps at > 10 000 m for both max-effective range and supersonic range). Direct-fire flat trajectory: at 2 km the drop is ~7 m (1.6 mil) and at 3 km ~22 m (4.4 mil).

### A.3 Lanz–Odermatt long-rod penetration (NOT De Marre)

The 140 mm KEW-AP terminal-ballistics model is the Lanz–Odermatt long-rod correlation, calibrated against M829-class open-source data (~700 mm RHA at the muzzle for a 7 kg DU rod at 1 670 m/s, L/D ≈ 27). The De Marre small-arms formula is not used at this calibre.

```
T_RHA = K · L · √(ρ_p / ρ_RHA) · f(v / v₀)

K     = 0.44                  (Lanz–Odermatt calibration constant, anchored to M829)
v₀    = 1 500 m/s              (calibration striking velocity)
L     = 0.920 m                (DU long-rod length)
ρ_p   = 18 600 kg/m³           (depleted uranium, ~10–15 % higher penetration than WHA via adiabatic shear banding)
ρ_RHA = 7 850 kg/m³            (290 BHN RHA)

Velocity scaling f(v / v₀):
f(v/v₀) → smooth in fluid-flow regime above v_strike ≈ 800 m/s
f(v/v₀) → 0 below v_strike ≈ 800 m/s (hydrodynamic-transition floor)
```

→ **0 m: 867.1 mm, 500 m: 698.1 mm, 1 km: 540.9 mm, 2 km: 326.7 mm, 3 km: 215.7 mm, 4 km: 0 mm** (`weapons_sim_results.md` §3, hydrodynamic floor at ~4 km as the rod's striking velocity falls through 800 m/s).

### A.4 Obliquity — `cos(θ)^N` with N ≈ 0.7 for long-rod APFSDS

Long rods at high striking velocity yaw into a more-normal-incidence response than hardened-core small-arms cores. The simulator uses N = 0.7 (vs N = 1.6 for small arms) per the Common Architecture portfolio convention.

```
T_RHA(60°) = T_RHA(0°) · cos(60°)^0.7
cos(60°)^0.7 = 0.500^0.7 = 0.616
```

→ **0 m: 867.1 → 533.8 mm, 500 m: 698.1 → 429.7 mm, 1 km: 540.9 → 333.0 mm** (`weapons_sim_results.md` §12). The N = 0.7 value is the long-rod-specific obliquity exponent and is the distinguishing feature vs the small-arms N = 1.6.

### A.5 Recoil — 351 715 J, 600 mm hydraulic stroke (superseding 1.2 m claim), 3 400 kg turret

```
J_free   = m_b · v_b + m_g · v_gas    (free recoil impulse, sim §1)
E_free   = J_free² / (2 · M_mount)    (free recoil energy)
F_peak   = (E_free · (1 − k_brake)) · (4 / s_stroke)   (parabolic-energy-dissipation peak force)

J_free   = 48 905 N·s (sim §1)
M_mount  = 3 400 kg empty trunnion + cradle (NOT full turret)
k_brake  = 0.55 (tank-gun muzzle-brake equivalent; sim §11)
s_stroke = 0.600 m (hydraulic recoil stroke; sim §11)
```

→ E_free = J_free² / (2 · M_mount) = 48 905² / (2 · 3 400) ≈ **351 718 J (≈ 351 715 J, 259 412 ft·lbf)** (sim §2 / §11). F_peak = **178 056 N (40 031 lbf)** at 600 mm stroke / 55 % brake (sim §11). The §8 of the paper body cites a 1.2 m stroke; the simulator-anchored value is 600 mm, and the simulator output supersedes the legacy 1.2 m claim per the paper's §11.1.4 declaration.

### A.6 Notes on numerical concordance with the simulator

1. **Recoil impulse 43 471 N·s (§3 table) vs sim §1 48 905 N·s.** The §3 specification table cites 43 471 N·s; the simulator §1 returns 48 905 N·s. The 351 715 J free-recoil-energy figure derives from the simulator value (J_free² / 2M_mount = 48 905² / (2 · 3 400) ≈ 351 715 J ✓), so the simulator's higher impulse is the internally consistent value with E_free and is the value referenced in §11.1.4 / §11.2.

2. **Peak chamber pressure 198 MPa (28 800 psi) vs sim §1 199 MPa (28 794 psi).** Round-trip consistent within rounding.

3. **Recoil stroke 1.2 m (§3, §8) vs sim §11 600 mm.** The paper-body §8 cites a 1.2 m stroke; the simulator's §11 stock-travel parameter is 600 mm and is the value that produces the 178 056 N peak force. The paper's §11.1.4 explicitly flags this supersession.

4. **Supersonic range 6 405 m vs sim §9 > 10 000 m.** The §9 table caps at the 10 000 m envelope; the 6 405 m figure is the Mach-1 crossover of the bare rod before the cap is applied.

---

## 12. References

[1] Wikipedia. (2024). XM291. Wikimedia Foundation.

[2] The Soapbox. (2017). On the 140 mm Tank Gun. Military Analysis Blog.

[3] GlobalSecurity.org. (2020). Future Combat System — Tank Technology. Military Analysis.

[4] TopWar.ru. (2013). Prospective 140 mm Tank Guns. Military Technical Review.

[5] Rheinmetall. (2023). Future Tank Armament Systems. Rheinmetall Defence Technical Brief.

[6] Ogorkiewicz, R.M. (2015). *Tanks: 100 Years of Evolution*. Osprey Publishing.

[7] Carlucci, D.E. & Jacobson, S.S. (2018). *Ballistics: Theory and Design of Guns and Ammunition*. CRC Press.

[8] Lanz, W. & Odermatt, W. (1992). Penetration limits of conventional large-calibre anti-tank guns. *Proc. 13th Int. Symp. Ballistics*, Stockholm.

[9] Tate, A. (1986). Long rod penetration models — Part II. *Int. J. Mech. Sci.*, 28(9), 599–612.

[10] M829-series open-source ballistic performance data; compiled from US Army public release on the M829 / M829A1 / M829A2 / M829A3 series, *Janes Armour and Artillery Ammunition Handbook* (2022 edition).
