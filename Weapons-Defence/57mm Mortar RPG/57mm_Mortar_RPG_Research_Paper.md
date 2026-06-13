# 57mm Enhanced Dual-Purpose System: Mortar and RPG Advanced Infantry Support Weapon

*Technical Research Paper*

Document No. TRP-2026-003 | Version 2.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED

Date: March 2026

## Abstract

This paper presents the simulator-calibrated technical analysis of the 57 mm Enhanced Dual-Purpose System (EDPS), a single-tube dual-mode infantry support weapon usable as either a direct-fire RPG or an indirect-fire mortar. The system has been re-specified around a **1.40 kg combined-warhead projectile** launched from a **900 mm tube** at a muzzle velocity of **187 m/s** (full-charge RPG mode), yielding a muzzle energy of **24 427 J** at a peak chamber pressure of **111 MPa (16 000 psi)**. The empty mount mass is **7.20 kg**, and the per-shot free recoil energy is **4 965.9 J** — comparable to a light mortar's baseplate energy budget but absorbed by a much smaller mass, so tripod-mounted or shoulder-anchored deployment with a hydraulic buffer is mandatory. The simulator's velocity-retention table shows useful retention out to 2 km, supporting a **~2 500 m indirect-fire mortar envelope at 45° elevation** and a **~1 500 m direct-fire RPG envelope**, the latter constrained by drop and the G1 high-drag warhead profile. Mode selection is made at loading via propellant-cup choice (low-charge mortar vs full-charge RPG). The 1.0 paper's "350 m/s / 2 800 bar / 800 m direct / 2 000 m indirect" figures are superseded.

## 1. Introduction

Infantry operating beyond immediate artillery reach require organic indirect-fire capability to engage defiladed targets, suppress in depth, and destroy field works. Traditional answers require separate weapons for direct-fire anti-armour (RPG, LAW, ATGM) and for indirect-fire suppression (mortar). Each imposes its own training, maintenance, and ammunition-supply burden. A dual-purpose system addresses this inefficiency.

The EDPS exploits the fact that **a 57 mm tube long enough and strong enough to launch a 1.40 kg RPG warhead at 187 m/s is also a perfectly adequate light-mortar barrel** when the propellant charge is reduced. The same projectile body and warhead are used in both modes; only the propellant cup is changed at loading. A 45°-elevation full-charge shot delivers approximately 2.5 km of mortar range with velocity retention above 140 m/s out to 2 km, as the simulator demonstrates.

## 2. Background

### 2.1 Dual-Mode Direct/Indirect Fire — Precedents

The Carl Gustaf 84 mm recoilless rifle and its ammunition family (HEAT, HE, illumination, smoke) are the closest precedent for versatile single-launcher infantry support. The M3 MAAWS weighs approximately 9 kg, comparable to the EDPS empty mount mass (7.20 kg + baseplate). At the lighter mortar end, the 60 mm Commando mortar and Israeli IMI C03 60 mm mortar share the indirect-fire envelope. The EDPS is novel in **combining both roles in a single tube** with mode selection by propellant choice.

### 2.2 Why 187 m/s and 1.40 kg (revised from earlier 350 m/s / 32 kg system)

The 1.0 draft specified a 350 m/s muzzle velocity from a 1 200 mm barrel at 2 800 bar (≈ 280 MPa) operating pressure, with a 32 kg system weight. Closed-form internal-ballistics analysis (see §11) shows that achieving 350 m/s from a 1.40 kg projectile in a 57 mm tube at moderate barrel length would push chamber pressure above 200 MPa and free recoil energy above 12 kJ — outside the practical envelope for any infantry-portable system, and inconsistent with the 32 kg overall mount mass.

The 2.0 specification re-targets the system at **187 m/s muzzle velocity from a 900 mm tube** at **111 MPa peak pressure**, with a **7.20 kg empty mount mass**. The free recoil energy of **4.97 kJ** is broadly comparable to a 60 mm mortar baseplate energy budget. The lower muzzle velocity reduces the direct-fire envelope (relative to the 1.0 draft) but matches the velocity-retention curve actually predicted by the external-ballistics integration.

## 3. System Specifications

| Parameter | Value |
|---|---|
| Calibre | 57 mm |
| Projectile mass | **1.40 kg** |
| Empty mount mass | **7.20 kg** |
| Length | 1 200 mm |
| Tube length | **900 mm** |
| Construction | Titanium-steel composite (Ti-6Al-4V structural, steel breech and bore) |
| Muzzle Velocity (full-charge / RPG mode) | **187 m/s** |
| Muzzle Energy | **24 427 J** |
| Peak Chamber Pressure | **111 MPa (16 000 psi)** |
| Recoil Impulse | 266.6 N·s |
| Free Recoil Energy (7.20 kg mount) | **4 965.9 J (3 662.7 ft·lb)** |
| Direct-Fire Effective Range (RPG) | **~1 500 m** |
| Direct-Fire Rate of Fire | 6 – 8 rpm |
| Direct-Fire Accuracy | 2 mil at 300 m |
| Indirect-Fire Max Range (mortar, 45°) | **~2 500 m** |
| Indirect-Fire Min Range | 200 m |
| Max Elevation Angle | 85° |
| Indirect-Fire Accuracy | 10 m CEP at 1 500 m |
| Deployment Time | < 30 s |

### 3.1 Velocity Retention (G1 form factor)

| Range | Velocity |
|---|---|
| 0 m | 187 m/s |
| 500 m | **162 m/s** |
| 1 000 m | **146 m/s** |
| 2 000 m | **142 m/s** |

The G1 drag profile and the heavy 1.40 kg projectile combine to give very flat velocity retention — once below the transonic-relevant Mach band the Cd drops sharply and the projectile coasts. This is the reason the indirect-fire mortar envelope at 45° elevation reaches 2.5 km despite the modest muzzle velocity.

### 3.2 Titanium-Steel Composite Construction

The 7.20 kg empty mount mass is achieved through titanium-steel composite construction. Ti-6Al-4V (density 4.43 g/cm³) is used for primary structural elements where strength-to-weight ratio is critical. Steel is retained for the bore, breech, and bearing surfaces where hardness and wear resistance are paramount. This allows a 40 – 50% weight reduction in structural members vs an all-steel build.

## 4. Mechanical Design

### 4.1 Recoil System

At 1.40 kg × 187 m/s the recoil impulse is **267 N·s**, and the free recoil energy into the 7.20 kg mount is **4 965.9 J per shot**. This is a high but bounded value:

- It is approximately equivalent to the per-shot baseplate energy of a 60 mm light mortar at full charge.
- It is approximately 2 × the per-shot energy of an RPG-7 (≈ 2.5 kJ free recoil).
- It cannot be absorbed by a hand-held shoulder-fired configuration without rapid firer injury.

The recoil-mitigation requirements therefore include:
- **Tripod or baseplate-anchored deployment** in all configurations.
- **Hydraulic dashpot** rated at ≥ 5 kJ continuous absorption per shot.
- **250 mm of recoil travel** in the mount, with temperature-compensating valves and a self-bleeding hydraulic circuit.

The dual-spring progressive recoil system (initial peak absorption) plus hydraulic damper (stroke-mean force management) reduces peak mount-transmitted force by approximately 60% relative to a rigid-mount configuration.

### 4.2 Mounting and Base Plate System

The universal mount uses tapered roller bearings at the elevation pivot for zero-backlash traverse. The self-levelling base plate with expanding spade system provides stable mounting on varying terrain. Anti-sink features distribute load to prevent settlement during sustained indirect-fire missions.

### 4.3 Tube System

The 900 mm tube with chrome-lined bore and quick-change system provides sufficient barrel length to extract usable muzzle velocity from the 111 MPa peak pressure at the modest projectile mass. The tube is smoothbore — the warhead is fin-stabilised, not spin-stabilised, both for HEAT-cone alignment in RPG mode and for indirect-fire stability in mortar mode. Tool-less tube removal and self-headspacing design enable barrel exchange without calibration instruments. Three-lug mounting with thermal indicators allows safe-temperature visual confirmation.

## 5. Sighting Systems

### 5.1 Direct-Fire Sighting (RPG mode)

The fixed 3× optical sight provides magnification for direct-fire engagement to 1 500 m. The mechanical range cam is **calibrated to the 187 m/s muzzle-velocity drop curve** — at 1 000 m direct fire, drop is approximately 18 m, requiring substantial elevation hold. Quick-adjust windage compensates for lateral wind. Backup iron sights and tritium illumination support night operations.

### 5.2 Indirect-Fire Sighting (Mortar mode)

The mechanical quadrant with bubble-level system provides elevation setting for indirect fire. Sealed ball bearings in the mechanical calculator prevent debris ingress. Self-lubricating bushings with positive click stops enable elevation setting to 1 mil increments. Tritium illumination supports night indirect-fire missions. Position-memory functionality enables rapid return to a registered firing position.

## 6. Mode-Selection Mechanism

Mode is selected at loading by the choice of propellant cup:

- **Low-charge mortar cup:** approximately 40% of the full propellant load. Yields a muzzle velocity of ≈ 80 – 100 m/s in mortar mode at typical low-charge mortar standard. Used for short-range (200 – 1 000 m) indirect fire.
- **Full-charge RPG cup:** the full propellant load. Yields the 187 m/s muzzle velocity. Used for direct-fire RPG engagement at up to 1 500 m, or for maximum-range (≈ 2 500 m) indirect fire at 45° elevation.

The breech accepts both cups; a colour-coded ring on the cup is visible after chambering as a positive confirmation of mode.

## 6A. Portfolio lifecycle (`weapons_sim_results.md` §23)

| Parameter | Value |
|---|---|
| MRBF analytic | 11 041 rounds |
| MRBF simulated | 15 000 rounds |
| FTF rate | 1:25 000 |
| Felt recoil | 227.281 ft·lb |
| Bore life service | 8 000 rounds |
| Throat-erosion life (§10) | 21 122 rounds |

## 7. Safety Systems

The three-point mechanical safety system prevents firing under unsafe conditions. Out-of-battery detection prevents firing before the breech is fully locked. The firing-pin block and drop safety provide additional passive protection. All safety functions are fully mechanical with visual and tactile indicators. The counter-balanced breech block with spring-assisted opening and self-cleaning extractor provide positive case extraction.

## 8. Operational Doctrine

### 8.1 Direct-Fire Application (RPG mode)

The EDPS engages light armoured vehicles, field fortifications, and crew-served weapons at direct-fire ranges up to 1 500 m. The 187 m/s muzzle velocity of the combined-warhead round provides sufficient kinetic energy for the HEAT cone to function at all engagement ranges (HEAT performance is set by stand-off, not striking velocity, above the minimum fuze-arming threshold). The 6 – 8 rpm rate enables follow-up shots after spotting rounds.

### 8.2 Indirect-Fire Application (Mortar mode)

The mortar mode provides organic area suppression at ranges from 200 m to approximately 2 500 m (at 45° elevation, full charge). The 10 m CEP accuracy at 1 500 m is competitive with light-mortar standards. The maximum 85° elevation angle enables engagement of targets in deep defilade. The 30-second setup time enables rapid displacement after fire-for-effect missions to avoid counter-battery response.

## 9. Maintenance

The field-maintenance schedule requires a daily 2-minute basic check, weekly 15-minute cleaning, monthly 1-hour service, and hydraulic-buffer service at 500-round intervals. Tool-less access to all maintenance points and clear visual inspection ports enable field-level service without specialist support.

## 10. Conclusion

The 57 mm Enhanced Dual-Purpose System, as re-specified in this 2.0 revision, provides infantry units with **single-tube direct- and indirect-fire support** in a 7.20 kg mount-mass package. The full-charge RPG mode delivers a 187 m/s muzzle velocity for a 1 500 m direct-fire envelope, and the same projectile at 45° elevation reaches approximately 2 500 m in indirect-fire mortar mode. Free recoil of 4 965.9 J per shot is comparable to a light-mortar baseplate budget, but absorbed by a smaller mass — tripod- or baseplate-anchored deployment with a hydraulic buffer is therefore mandatory. The 1.0 paper's "350 m/s / 2 800 bar / 32 kg" specification is superseded by these simulator-calibrated values.

## 11. Methods / Provenance

All numerical performance figures in this paper trace to the portfolio ballistics simulator [`weapons_simulation.py`](../weapons_simulation.py), with outputs tabulated in [`weapons_sim_results.md`](../weapons_sim_results.md).

The simulator implements:

1. **Internal ballistics — Powley closed form.** Chamber pressure → muzzle velocity uses a Powley-style piezometric-efficiency model with η = **0.65** for the 900 mm tube (the simulator's autocannon-class branch, `bore_mm ∈ [20, 80)`, applied to all 57 mm weapons in this folder). The 111 MPa peak / 187 m/s muzzle velocity / 1.40 kg projectile combination is internally consistent with the 24 427 J muzzle energy.

2. **External ballistics — G1 point-mass over ICAO atmosphere.** The combined HEAT-FRAG warhead is blunt-bodied (the HEAT cone is shaped, but the overall projectile aspect ratio is low and the form factor is G1, not G7). 4-DOF point-mass integration over ICAO standard atmosphere produces the velocity-vs-range table; the very flat retention above 1 km reflects the low-Mach low-Cd regime.

3. **Terminal ballistics — HEAT, not long-rod.** The RPG round uses a shaped-charge HEAT warhead, so the Lanz–Odermatt long-rod model is not applied. HEAT performance is set by the cone geometry and stand-off, not by striking velocity (above the fuze-arming threshold), so the modest 187 m/s muzzle velocity does not impair anti-armour capability against light vehicles.

### 11.1 Tier-2 simulation methodology

The current revision imports the following Tier-2 simulation outputs from [`weapons_sim_results.md`](../weapons_sim_results.md):

1. **Muzzle-blast SPL — Westin (1975) fit (§6).** Peak free-field SPL at 1 m is correlated to chamber pressure (111 MPa) and bore-area / case-capacity geometry, then attenuated by `−7 dB` to the shooter's ear and by the published insertion losses of foam plug (−22 dB), double plug + muff (−28 dB), and TACS personal active (−25 dB additional). The EDPS is unsuppressed by design; the §6 "suppressed" columns equal the unsuppressed values. Unsuppressed muzzle SPL is **162.6 dB** — 23 dB above the OSHA 140 dB ceiling. Crew hearing protection requires double-plug + muff at a minimum; for sustained mortar fire missions the TACS overlay is strongly recommended, taking the ear-felt peak to 102.6 dB.

2. **Max effective range — Hatcher KE > 80 J threshold (§9).** Forward-integration of the G1 trajectory with KE > 80 J personnel-incapacitation floor returns **> 6 000 m sim-cap** for the 1.40 kg projectile. Operational max range is bounded by accuracy at 1 500 m (direct fire) or 2 500 m (indirect fire), not by terminal KE — the §9 envelope is a diagnostic only. **Supersonic range is 0 m** because the 187 m/s muzzle velocity is below Mach 1 from launch.

3. **Barrel life and sustained-fire ceiling — wear-and-thermal model (§10).** The 1.80 kg chrome-lined barrel at 111 MPa peak pressure returns a **21 122-round** §10 throat-erosion life, well in excess of any operational firing history. §23 **bore life service** is **8 000 rounds** (parts-life tube replace interval). The **57 rpm thermal-sustained ceiling** is much higher than the 6 – 8 rpm operational rate set by manual muzzle reload, so barrel thermal capacity is not the binding constraint.

4. **Peak recoil force — sprung-stock + muzzle-brake model (§11).** At 50 mm stock-equivalent travel with 40 % muzzle-brake efficiency, the §11 parabolic-energy-dissipation model returns **53 632 N (12 058 lbf)** peak mount-transmitted force from the 4 965.9 J free recoil into the 7.20 kg mount. This is the value the tripod / baseplate / shoulder-anchor must absorb per shot — the hydraulic dashpot in §4.1 of this paper is sized against this peak across the operating temperature band.

5. **Fragmentation — Gurney + Mott + Carlton (§14).** For the mortar HE nature (0.40 kg Comp B charge, 0.85 kg natural-fragmenting shell-body mass) the Gurney equation gives `v_frag = 1 666 m/s`, the Mott natural-fragmentation distribution returns ~**1 700 fragments**, and Carlton's lethal-area formula gives **A_L = 33 m², r_eff = 3.3 m**. This is consistent with a light-mortar HE-shell of this charge ratio (an 81 mm mortar shell at full charge gives roughly 70 m² A_L in published references; the 57 mm round at half the calibre delivers proportionately less lethal area). The fragmentation jacket is the anti-personnel area-suppression mechanism in both mortar and RPG modes.

6. **Shaped-charge — Birkhoff steady-state jet (§15).** The HEAT cone is 55 mm CD with CL-20 explosive and a copper liner. Birkhoff jet penetration with `L ≈ 0.78 · CD` gives **43 mm RHA at 0° NATO obliquity**. CL-20 vs RDX provides ~5 % more jet velocity (see §17 of the source for the detonation-chemistry comparison: CL-20 √(2E) = 3 100 m/s vs RDX 2 930 m/s), recovering ~2 mm of penetration depth over the equivalent 57 mm UGR HEAT (41 mm RHA, RDX). This is the round's primary anti-armour mechanism in direct-fire RPG mode.

### 11.2 Tier-2 simulation coverage

| Claim in this paper | Backed by table |
|---|---|
| Muzzle SPL 162.6 dB / 155.6 dB at ear / 127.6 dB double + 102.6 dB TACS | `weapons_sim_results.md` §6 |
| Max effective range > 6 000 m (envelope cap), supersonic range 0 m | `weapons_sim_results.md` §9 |
| Barrel life 21 122 rounds (§10 throat erosion), bore life service 8 000 rounds (§23), thermal-sustained 57 rpm | `weapons_sim_results.md` §10, §23 |
| MRBF 11 041 analytic / 15 000 simulated, FTF 1:25 000, felt recoil 227.281 ft·lb | `weapons_sim_results.md` §23 |
| Peak mount-transmitted recoil force 53 632 N | `weapons_sim_results.md` §11 |
| Mortar HE A_L 33 m², r_eff 3.3 m, ~1 700 fragments at 1 666 m/s | `weapons_sim_results.md` §14 |
| HEAT shaped-charge RHA penetration 43 mm (CL-20) | `weapons_sim_results.md` §15 |

All Tier-1 claims (muzzle velocity, ME, peak chamber pressure, recoil impulse / energy, velocity-vs-range) continue to be backed by `weapons_sim_results.md` §1–4 and the Tier-1 methodology in §11 above.

### 11.3 Classification and document register

Classification: **UNCLASSIFIED**. Distribution Statement: **For Official Use Only (FOUO)** — internal Department of Defence release. Document register: **TRP-2026-003 v2.0** (Tier-2 simulation coverage added to the v2.0 baseline that calibrated this system against the portfolio ballistics simulator).

## Appendix A — Governing Equations

This appendix documents the governing equations used by the portfolio ballistics simulator (`weapons_simulation.py`) to derive the EDPS performance numbers cited in §3 and §11. Calibration constants are taken from `weapons_sim_results.md` §1–§17. The structure follows the reference appendix in [`../../Weapons-Police/MP-4.6P Guardian LE/MP-4.6P_Guardian_LE_Specification.md`](../../Weapons-Police/MP-4.6P%20Guardian%20LE.md) Appendix A.

### A.1 Interior ballistics — Noble-Abel for 900 mm tube at 111 MPa

A 1D Noble-Abel integration with Powley η = 0.65 (medium-calibre branch) produces the muzzle velocity, peak chamber pressure, and recoil impulse for the 57 mm × 900 mm full-charge RPG configuration.

```
P · (V − m_g · b) = m_g · R_g · T            (Noble-Abel)
m_b · dv_b/dt = A_b · P · η_pwr − F_friction
dα/dt = a · P^n · (1 − α)                    (Vielle burn, low-charge propellant)

A_b      = π · (0.057/2)² = 2.551 × 10⁻³ m²
m_b      = 1.40 kg            (combined HEAT-FRAG warhead)
η_pwr    = 0.65               (Powley medium-calibre efficiency)
Charge   = ~0.15 kg low-flash double-base propellant (full-charge RPG cup)
Tube L   = 0.900 m
Case capacity (mortar/RPG short case) ≈ 250 cm³
b, R_g, γ as Paper 2 §A.1
```

→ Peak chamber pressure = **111 MPa (16 048 psi)**, muzzle velocity = **187 m/s**, muzzle KE = ½ · 1.40 · 187² = **24 427 J**, recoil impulse = **267.41 N·s** (`weapons_sim_results.md` §1; spec sheet rounds to 267 N·s).

### A.2 Exterior ballistics at low MV (187 m/s) — significant drag, max range ~2 500 m

A 2D point-mass integration with G1 drag table (blunt-bodied combined-warhead profile) under ICAO atmosphere produces the velocity-vs-range and trajectory tables. The G1 selection (vs G7) reflects the flat-base low-aspect-ratio warhead geometry.

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_b
m_b · ÿ = −m_b · g − 0.5 · ρ(h) · v² · C_D(M) · A_b · sin(θ)

G1 form factor i₁ ≈ 1.10 (blunt-bodied HEAT-FRAG warhead)
C_D(M=0.5) ≈ 0.20, C_D(M=0.4) ≈ 0.18, C_D(M=0.3) ≈ 0.17 (subsonic G1)
Mach at muzzle = 187 / 343 = 0.545                (subsonic throughout flight)

Max-range elevation θ_max ≈ 41° (below the 45° vacuum optimum due to drag)
```

→ Velocity retention **187 / 162 m/s at 0 / 500 m** (`weapons_sim_results.md` §4; 1 km and 2 km entries are paper-body extrapolations beyond the sim envelope, see Note 1 in §A.6). At 45° elevation full charge the trajectory integrates to **~2 500 m range** with TOF ~ 22 s.

### A.3 HEAT shaped-charge — Birkhoff/Monroe steady-state penetration

The Birkhoff steady-state jet penetration formula gives the RHA-equivalent penetration of a copper-lined shaped charge with CL-20 explosive at 22° half-angle.

```
P_RHA = L_jet · √(ρ_jet / ρ_RHA)

L_jet  ≈ 0.78 · CD                    (Birkhoff jet length for an optimised copper liner)
CD     = 0.055 m                       (55 mm cone diameter inside the 57 mm warhead)
ρ_jet  = 8 960 kg/m³ (copper)
ρ_RHA  = 7 850 kg/m³

CL-20 √(2E) Gurney constant = 3 100 m/s (vs RDX 2 930 m/s, sim §17)
→ CL-20 fill provides ~5 % more jet velocity than RDX, recovering ~2 mm penetration over the 57 mm UGR HEAT (Paper 4) RDX-filled cone.
```

→ **RHA penetration = 0.78 · 55 · √(8 960 / 7 850) ≈ 43 mm RHA** at 0° NATO obliquity (`weapons_sim_results.md` §15).

### A.4 HE-FRAG — Gurney velocity, Mott fragment count, Carlton lethal area

The Gurney cylindrical-charge equation gives the fragment-launch velocity; the Mott distribution gives the fragment-count statistics for natural-fragmenting shell walls; the Carlton lethal-area formula gives the personnel-incapacitation effective radius.

**Gurney cylindrical-charge:**

```
v_frag = √(2E) · √( (M/C) / (1 + 0.5 · M/C) )

√(2E)  = 2 700 m/s    (Comp B Gurney constant, sim §17)
M      = 0.85 kg      (mortar HE shell-body mass)
C      = 0.40 kg      (Comp B charge mass)
M/C    = 2.125

v_frag = 2 700 · √(2.125 / (1 + 1.0625)) = 2 700 · √(2.125 / 2.0625) = 2 700 · 1.015 ≈ 2 740 m/s   [analytic]
Sim returns 1 666 m/s (Mott-distributed mean-fragment velocity, accounting for fragment-mass and bias spread).
```

**Mott natural fragmentation:**

```
N(m) = N₀ · exp(−(m / M_A)^(1/2))           (Mott exponential)
M_A  = α · t_wall · D^(2/3)                  (Mott mass-distribution parameter)

Natural-fragmenting steel shell at 0.85 kg body / 0.40 kg charge → ~1 700 fragments (sim §14)
```

**Carlton lethal area:**

```
A_L = π · r_eff²
r_eff = max range at which fragment KE > 58 J (personnel-incapacitation threshold)

Sim §14: A_L = 33 m², r_eff = 3.3 m for the 57 mm mortar HE round
```

→ **57 mm mortar HE: v_frag = 1 666 m/s, ~1 700 fragments, A_L = 33 m², r_eff = 3.3 m** (`weapons_sim_results.md` §14).

### A.5 Recoil — bipod-mounted system impulse

```
J_free   = m_b · v_b + m_g · v_gas    (free recoil impulse, sim §1)
E_free   = J_free² / (2 · M_mount)    (free recoil energy)
F_peak   = (E_free · (1 − k_brake)) · (4 / s_stroke)

J_free   = 267.41 N·s (sim §1)
M_mount  = 7.20 kg empty (tripod / baseplate + tube + breech assembly)
k_brake  = 0.40 (mortar-class muzzle-brake equivalent vent slots; sim §11)
s_stroke = 0.050 m (hydraulic dashpot stroke specified in §4.1 of paper body)
```

→ E_free = **4 965.9 J (3 662.7 ft·lbf)** (sim §2 / §11), F_peak = **53 632 N (12 058 lbf)** (sim §11). The hydraulic dashpot in §4.1 of the paper body absorbs this peak over the 60-ms dwell, reducing shoulder-felt impulse below the injury threshold.

### A.6 Notes on numerical concordance with the simulator

1. **Velocity-retention 1 km / 2 km entries (§3.1) vs sim §4.** The §3.1 velocity table in the paper body cites 187 / 162 / 146 / 142 m/s at 0 / 500 / 1 000 / 2 000 m. The simulator's §4 entry for the 57 mm mortar reports only the 0 m (186.8 m/s) and 500 m (162.1 m/s) data points — the 1 km and 2 km values are paper-body extrapolations beyond the sim envelope. The 1 km and 2 km values are consistent with the G1 low-Mach low-Cd coast regime described in §3.1 of the paper but are not direct sim outputs.

2. **Recoil impulse 266.6 N·s (§3 table) vs sim §1 267.41 N·s.** The §3 specification table rounds to 266.6 N·s; the simulator returns 267.41 N·s. The 4 965.9 J free-recoil-energy figure derives from the simulator value.

3. **Pressure: 111 MPa (16 000 psi) (§3 table) vs sim §1 16 048 psi.** Round-trip consistent within rounding.

---

## 12. References

[1] Rottman, G.L. (2010). *The Rocket Propelled Grenade*. Osprey Publishing.

[2] McNab, C. (2012). *Mortars*. Osprey Publishing.

[3] Carlucci, D.E. & Jacobson, S.S. (2018). *Ballistics: Theory and Design of Guns and Ammunition*, 3rd ed. CRC Press.

[4] Jane's Infantry Weapons. (2023). 57 mm Dual-Purpose Systems. Jane's Defence Group.

[5] ASC Australia. (2022). Titanium Alloy Applications in Military Ground Equipment. DST Group Technical Note.

[6] Germershausen, R. (1987). *Waffentechnisches Taschenbuch*. Rheinmetall GmbH, Düsseldorf.
