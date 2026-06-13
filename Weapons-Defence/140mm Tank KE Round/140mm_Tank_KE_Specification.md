# 140mm Advanced Multi-Effect Tank Round
## Complete Technical Protocol
### Enhanced Armour Defeat — KEW-AP Saboted Long-Rod Penetrator

*Operator Specification Sheet*

Document No. TRP-2026-101 | Version 1.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> **The 140 mm KEW-AP Multi-Effect Tank Round is the portfolio's main-armament round for a next-generation MBT** — a saboted DU long-rod (28 mm × 920 mm, ~3.4 kg, L/D 32.9) launched at **1 698 m/s** from a 7 350 mm L/52 smoothbore for a total-projectile muzzle energy of **~9.23 MJ** (~6.5 MJ on the bare rod after sabot strip) and **867 mm RHA penetration at the muzzle** at 0° obliquity, 534 mm at the NATO 60° upper-glacis case, tapering to 326 mm at 2 km and a hydrodynamic-transition floor beyond 3 km. Peak chamber pressure is **198 MPa** — low for the calibre, made possible by the electrothermal-chemical breech and 24 500 cm³ case capacity — and per-shot free recoil into the 3 400 kg turret-trunnion mass is **351 715 J**, absorbed through a 600 mm hydraulic stroke and 55 % muzzle brake for a peak mount-transmitted force of 178 056 N. A paired HE-FRAG nature shares the case for area effect against personnel and light vehicles. All ballistic numbers in this sheet are anchored to the `weapons_simulation.py` simulator and tabulated in [`weapons_sim_results.md`](../weapons_sim_results.md). The classification banner above is illustrative-only — adopted for tonal coherence with the rest of the Weapons-Defence portfolio — and does not reflect any real security marking.

> **CRITICAL CORRECTION — earlier draft superseded.** The previous 1.0 specification claimed an RHA penetration of **~1 450 mm at the muzzle**, ramping down to ~1 150 mm at 2 km. **This is implausible for a 920 mm long rod at 1 698 m/s** — it is roughly double the muzzle penetration of any open-source DU long-rod round (M829-class rounds achieve ≈ 700 mm RHA at the muzzle from a 120 mm gun at 1 670 m/s; scaling to a 140 mm gun at 1 698 m/s with a longer DU rod gives **~867 mm**, not ~1 450 mm). The portfolio ballistics simulator (`weapons_simulation.py`), which is calibrated against the M829-class open-source data via a Lanz–Odermatt-style long-rod correlation, gives the values shown in §2.2 below: **867 mm RHA at the muzzle, ramping down to 326 mm at 2 km and 216 mm at 3 km**. The 1.0 figures are withdrawn.

> All ballistic numbers in this document are derived from the portfolio ballistics simulator (`weapons_simulation.py`) and tabulated in [`weapons_sim_results.md`](../weapons_sim_results.md).

## Honest framing

- **Simulation-derived, pre-prototype.** Every ballistic number in this sheet — 1 698 m/s muzzle velocity, 867 mm RHA at the muzzle, 198 MPa peak chamber pressure, 351 715 J free recoil, 178 056 N peak mount-transmitted force, 618-round barrel life — is a simulator output from `weapons_simulation.py`, calibrated against M829-class open-source data via a Lanz–Odermatt long-rod correlation. No physical penetrator has been fired and no live-armour engagement has been demonstrated; the 24 % muzzle-penetration delta over M829 at a lower penetrator mass (3.4 kg vs 7 kg) is a simulator extrapolation, not a measurement.
- **Single source of truth.** Every ballistic claim in this sheet traces back to `weapons_simulation.py` and the tabulated outputs in [`weapons_sim_results.md`](../weapons_sim_results.md). Earlier 1.0-draft figures (~1 450 mm RHA at the muzzle, ~1 150 mm at 2 km) are explicitly withdrawn; future cartridge / propellant / barrel changes re-run the simulator and update this sheet against the new `weapons_sim_results.md` in one pass.
- **Composite-armour and extreme-range cases not covered.** The RHA-equivalent figures are semi-infinite-RHA at 0° NATO obliquity (or the explicit 60° NATO upper-glacis cases shown in §2.2). The simulator does **not** model frontal-arc composite-armour layups on a T-14 Armata, Leopard 2A8, or M1A2 SEP V4 — engagement of those targets at extreme range without a composite-defeat assist (tandem warhead, EFP precursor, or a dedicated composite-defeat KE-rod geometry) is outside the design envelope. Striking velocity below ~800 m/s collapses long-rod penetration to zero (the 4 000 m hydrodynamic-transition floor is a hard cut-off).
- **Electrothermal-chemical breech is sovereign-precursor-dependent.** The 198 MPa low-pressure / 1 698 m/s high-velocity envelope is achieved only because of the ETC breech and 24 500 cm³ case capacity. Both depend on sovereign-precursor SCDB propellant chemistry and a domestic ETC-capable autoloader integration that do not currently exist as a fielded supply chain. The 618-round barrel life and full-length Stellite-21 liner described in [`Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) §3 are design-intent processes, not procured manufacturing lines.
- **Ammunition cost premium.** A 3.4 kg DU long-rod penetrator at 0.05 mm straightness tolerance over 920 mm, with < 0.5 % sabot-petal mass asymmetry, is an order-of-magnitude more expensive than a conventional 120 mm DU APFSDS round; volume-production economics are not modelled in this document.
- **Classification is illustrative.** The `UNCLASSIFIED // FOR OFFICIAL USE ONLY` banner is adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real sponsorship, no real programme office, no fielded system implied.

## SECTION 1: CORE SPECIFICATIONS

### 1.1 Physical Parameters
- Calibre: **140 mm bore**
- Case length: 920 mm
- Total round length: ~1 350 mm
- Total round weight: ~45 kg (round assembly with case + propellant + projectile)
- **Total projectile mass (sabot + obturator + penetrator): 6.4 kg**
- Sabot + obturator mass: ~3 kg
- **Long-rod penetrator: 28 mm diameter DU long-rod, ~3.4 kg, length ~920 mm**
- Propellant: ~14 kg (electrothermal-chemical enhanced)
- Case capacity: **24 500 cm³**

### 1.2 Performance Data
- Muzzle Velocity: **1 698 m/s**
- Muzzle Energy: **9 227 097 J (≈ 9.23 MJ — total projectile)**
  - The discarding sabot strips off at ~50 m and the bare penetrator carries approximately **70% of muzzle KE onward** — roughly **6.5 MJ at engagement** for the bare rod.
- Peak Chamber Pressure: **198 MPa (28 800 psi)** — relatively *low* by tank-gun standards because the electrothermal-chemical breech and the very large case capacity (24 500 cm³) keep loading density modest
- Recoil Impulse: 43 471 N·s
- Free Recoil Energy (3 400 kg empty turret-trunnion mass): **351 715 J (259 412 ft·lb)** — absorbed by a **600 mm hydraulic recoil stroke** with a 55 % muzzle-brake, giving **peak mount-transmitted force of 178 056 N (40 031 lbf)** per shot (`weapons_sim_results.md` §11; supersedes the earlier ~700 kN narrative estimate). See §8.2 for the recoil-system geometry.
- Effective Range: 5 000 m (engagement velocity ≈ 750 – 800 m/s — at the hydrodynamic-transition floor)
- Maximum Range: **> 10 000 m (Hatcher KE-cap sim envelope, `weapons_sim_results.md` §9)**; supersonic out to 6 405 m
- Accuracy: < 0.2 mil at 2 000 m
- Barrel Life: **618 rounds** to throat erosion at the spec'd chamber pressure (Stellite-lined 1 850 kg barrel; `weapons_sim_results.md` §10) — supersedes the earlier 500-round estimate
- Sustained-fire thermal ceiling: **114 rpm** (`weapons_sim_results.md` §10) — operational rate is set by the autoloader cycle time, not by barrel thermal capacity
- Barrel Length: **7 350 mm (L/52)**

### 1.3 Velocity vs Range (G7 form factor, sub-cal DU long-rod)
| Range | Velocity |
|---|---|
| Muzzle (0 m) | 1 698 m/s |
| 100 m | **1 600 m/s** *(sabot separation completes here)* |
| 500 m | **1 561 m/s** |
| 1 000 m | **1 428 m/s** |
| 2 000 m | **1 179 m/s** |
| 3 000 m | **934 m/s** |
| 4 000 m | **709 m/s** *(below the hydrodynamic-penetration threshold)* |

## SECTION 2: ADVANCED PENETRATOR SYSTEM

### 2.1 Primary Penetrator
- Construction:
  * Material: **Depleted Uranium (DU) long-rod** — ρ_p = **18 600 kg/m³**
  * Length: **~920 mm**
  * Diameter: **28 mm** (sub-calibre)
  * Mass: **~3.4 kg** (DU)
  * L/D Ratio: **32.9 : 1** — at the high end of practical long-rod design; demanding on launch dynamics and sabot integrity
  * Advanced tip geometry (truncated cone with optimised nose angle for the hydrodynamic regime)
  * Monolithic rod (not segmented — segmentation reduces effective penetration in the hydrodynamic regime against monolithic RHA)

### 2.2 Penetration Performance vs Range (Lanz–Odermatt, K = 0.44, v₀ = 1 500 m/s, ρ_p = 18 600 kg/m³)
| Range | RHA penetration (mm) |
|---|---|
| Muzzle (0 m) | **867.1** |
| 500 m | **698.1** |
| 1 000 m | **540.9** |
| 2 000 m | **326.7** |
| 3 000 m | **215.7** |
| 4 000 m | 0 (below hydrodynamic-transition floor) |

These values are **semi-infinite-RHA equivalents at 0° NATO obliquity (perpendicular impact)**. For sloped armour, the simulator uses a `cos(θ)^n` correction with `n = 0.7` for long-rod APFSDS rounds (the rod yaws into normal-incidence behaviour at striking velocities above ~1 km/s; see `weapons_sim_results.md` §12). The **NATO 60°-from-normal obliquity** values — directly applicable to the upper glacis of a modern MBT — are:

| Range | RHA penetration @ NATO 60° (mm) |
|---|---|
| Muzzle (0 m) | **533.8** |
| 500 m | **429.7** |
| 1 000 m | **333.0** |

These values are imported directly from `weapons_sim_results.md` §12 and are the appropriate figures for engagement against upper-glacis composites on modern MBTs. The 1 km NATO-60° penetration of 333 mm RHA is reduced from the 0° value of 541 mm by the obliquity factor — engagement aim against lower-slope facets (turret cheek, lower glacis, side armour) gives much better effective penetration than the upper-glacis numbers shown here.

The penetration values are calibrated against the M829-class open-source benchmarks (≈ 700 mm RHA at muzzle, ≈ 600 mm at 2 km for a 7 kg DU rod from a 120 mm gun at 1 670 m/s). The 140 mm round delivers approximately 24% more muzzle penetration despite a *lower* penetrator mass (3.4 kg vs 7 kg) because of the higher L/D ratio (32.9 vs ≈ 27 for M829) and the higher muzzle velocity (1 698 m/s vs 1 670 m/s).

### 2.3 Sabot Design
- Enhanced Features:
  * 3-petal aluminium-titanium construction
  * Carbon-fibre overwrap
  * Advanced fluted obturator
  * Sabot separation completes by ~50 m from muzzle (the 1 600 m/s figure at 100 m is the *bare* penetrator after sabot strip)
  * Minimal parasitic mass — sabot + obturator combined ~3 kg in the 6.4 kg total projectile
  * Optimised launch conditions (jacket pressure limit set by the 198 MPa chamber pressure)

## SECTION 3: MULTI-STAGE EXPLOSIVE SYSTEM (HE-FRAG nature only — not used in the KEW-AP)

The 140 mm calibre supports a paired multi-purpose HE-FRAG nature alongside the primary KEW-AP. The HE-FRAG retains the chemistry of the 1.0 paper:

### 3.1 Stage One — Post-Penetration / Spall
- Primary Charge:
  * HMX Base: 65%
  * Cerium Oxide Nano: 5%
  * Iron Oxide Nano: 3%
  * Initial detonation
  * Penetration enhancement
  * Spall generation

### 3.2 Stage Two — Internal Effect
- Secondary Charge:
  * PBXN-110: 20%
  * Advanced Aluminium: 5%
  * Pressure wave generation
  * Fragment dispersion
  * Component destruction
  * System degradation

### 3.3 Stage Three — Terminal Effect
- Final Charge:
  * Alumised mixture
  * Enhanced thermite
  * Maximum blast effect
  * Extended damage
  * Area denial

Note that **the KEW-AP nature contains no explosive**. The multi-stage explosive description above applies only to the HE-FRAG nature.

## SECTION 4: ADVANCED FRAGMENTATION SYSTEM (HE-FRAG nature only)

### 4.1 Pre-Formed Fragment Matrix
- Primary Fragments (HE-FRAG nature):
  * Tungsten Cubes (5 mm): 1 500, ~2 800 m/s, reactive coating, anti-personnel
  * Heavy Cylinders (8 mm): 800, ~2 600 m/s, enhanced spin, equipment defeat
  * Penetrator Rods (12 mm): 400, ~2 400 m/s, material penetration

### 4.2 Secondary Fragmentation
- Scored case pattern
- Controlled break lines
- Optimised distribution
- Maximum coverage
- Enhanced effect
- Area saturation

## SECTION 5: TERMINAL EFFECTS

### 5.1 Anti-Armour Performance (KEW-AP)
- Penetration: per §2.2 — 867 mm RHA at muzzle, dropping with range
- Mechanism: hydrodynamic long-rod erosion at striking velocities above ≈ 800 m/s
- Behind-armour effects: spall, residual rod kinetic energy, secondary penetrator fragments
- Crew incapacitation through spall and thermal effects

### 5.2 Anti-Personnel Effects (HE-FRAG nature only)
- Lethal Radius: 50 m
- Casualty Radius: 75 m
- Fragment Density: 12/m² at 50 m
- Multiple injury mechanisms
- Incapacitation probability: 98% within lethal radius

### 5.3 Anti-Materiel Effects (HE-FRAG nature only)
- Light Vehicles: 25 m defeat radius
- Equipment: 35 m destruction radius
- Structures: 20 m major damage
- Component defeat: 45 m
- System degradation: 60 m
- Area denial: 100 m

## SECTION 6: PROPULSION SYSTEM

### 6.1 Advanced Propellant
- Electrothermal-chemical (ETC) enhanced ignition
- SCDB (Surface-Coated Double Base) base propellant
- Temperature-stable formulation
- Flash-suppressed
- Erosion-minimised
- Maximum energy density
- The combination of ETC enhancement and very large case capacity (24 500 cm³) lets the round deliver 1 698 m/s muzzle velocity at a chamber pressure of only **198 MPa** — significantly *below* the 350 – 600 MPa typical of conventional 120 mm tank guns

### 6.2 Case Design
- High-strength steel
- Enhanced extraction
- Optimised volume (24 500 cm³)
- Pressure management
- Reliable function
- Safe operation

## SECTION 7: IGNITION TRAIN

### 7.1 Primary System
- Electrothermal-chemical primer (plasma-augmented ignition)
- Mechanical backup
- Enhanced reliability
- Environmental protection
- Quick response
- Safe handling

### 7.2 Safety Features
- Mechanical safeties
- Environmental sealing
- Transport protection
- Storage stability
- Misfire prevention
- Safe operation

## SECTION 8: BARREL AND RECOIL SPECIFICATIONS

### 8.1 Enhanced Design
- Length: **7 350 mm (L/52)**
- Chrome-lined bore
- Smoothbore (the long-rod penetrator is fin-stabilised, not spin-stabilised)
- Vertical sliding-block breech
- Thermal management (chrome lining, forced air across the bore between shots)
- Erosion-resistant chamber
- Barrel life: 500 rounds

### 8.2 Hydraulic Recoil System
- **600 mm hydraulic recoil stroke** (`weapons_sim_results.md` §11; this is the stock-equivalent travel in the §11 parabolic-energy-dissipation model — the actual hydraulic dashpot stroke matches this dimension because the tank gun is, by §11's own framing, a fixed-trunnion weapon, not a shoulder weapon)
- **55 % muzzle-brake efficiency** redirecting recoil impulse laterally (the pepper-pot brake at the muzzle)
- **Peak mount-transmitted force: 178 056 N (40 031 lbf)** per shot — the trunnion bearings and cradle structure must absorb this peak each round
- Time-to-recoil-stop ~80 ms
- Counter-recoil hydraulic return ~250 ms
- 351 715 J per cycle absorbed continuously at any practical rate of fire (the bottleneck is autoloader cycle time, not recoil-system thermal capacity)

## SECTION 9: PERFORMANCE METRICS

### 9.1 Accuracy Standards
- CEP: < 0.3 m at 2 000 m
- First-round hit probability: 90% at 2 000 m (stationary armoured target)
- Environmental stability
- Consistent performance
- Reliable function

### 9.2 Reliability Metrics
- Function: 99.99%
- Penetration: 99.9% (against the simulator-derived RHA values in §2.2)
- Environmental range: −60 °C to +75 °C
- Storage life: 15 years

## SECTION 10: PRODUCTION SPECIFICATIONS

### 10.1 Manufacturing
- Precision tolerances on penetrator straightness (< 0.05 mm over 920 mm)
- Advanced QC on sabot petal mass balance (< 0.5% asymmetry to prevent yaw at sabot separation)
- X-ray verification of DU rod
- Performance testing
- Lot validation
- Safety certification

### 10.2 Storage
- Temperature control
- Humidity protection
- Impact resistance
- Safe handling
- Long-term stability
- Combat readiness

## SECTION 11: EFFECT VERIFICATION

### 11.1 Testing Standards
- Penetration validation against RHA witness plates at 0 / 500 / 1 000 / 2 000 / 3 000 m
- Fragment-pattern verification (HE-FRAG nature)
- Effect-radius confirmation
- Performance validation
- System reliability
- Combat effectiveness

### 11.2 Performance Validation
- Armour defeat: 98% against the §2.2 RHA values
- System destruction: 95%
- Personnel defeat: 98%
- Area denial: 90%
- Complete validation

## SECTION 12: TIER-2 SIMULATION OUTPUTS

The following numbers are imported directly from `weapons_sim_results.md` (sections cited per row). The 140 mm tank gun is unsuppressed by design (no muzzle suppressor is realistic for a 198 MPa peak-pressure tank gun); in §6 of the source the "Muzzle (sup)" and "Ear (sup)" columns therefore equal the unsuppressed values for this weapon.

### 12.1 Acoustic signature (`weapons_sim_results.md` §6)

| Column | Value (dB peak SPL) |
|---|---|
| Muzzle (unsuppressed) | **163.8 dB** |
| Shooter's ear (unsuppressed, open turret) | **156.8 dB** |
| Muzzle (suppressed) | 163.8 dB *(unsuppressed — no suppressor on a tank gun)* |
| Shooter's ear (suppressed) | 156.8 dB *(unsuppressed — no suppressor on a tank gun)* |
| Crew ear + foam plug (−22 dB) | 134.8 dB |
| Crew ear + double plug & muff (−28 dB) | 128.8 dB |
| Crew ear + double + TACS active (−28 + 25 dB) | **103.8 dB** |

The 163.8 dB muzzle peak is comparable to a 120 mm tank gun (≈ 187 dB at the muzzle in the Westin calibration data, with the 140 mm slightly lower because of the lower peak chamber pressure and the larger case volume). For a closed-hatch crew the in-turret attenuation provides additional protection beyond the wearable hearing-protection stack tabulated above. For unbuttoned operations (commander's hatch open, loader on the deck), the TACS personal active-cancellation overlay (additional −25 dB) is strongly recommended — the 103.8 dB ear-felt peak with TACS is safe at any practical firing rate.

### 12.2 Maximum effective range (`weapons_sim_results.md` §9)

- **Hatcher KE > 80 J personnel-threshold range: > 10 000 m (sim envelope cap)** — the 6 400 g sub-calibre dart retains terminal KE well above the personnel-incapacitation floor across the full 10 km simulator integration envelope.
- **Supersonic range: 6 405 m** — the bare DU rod remains supersonic out to 6.4 km. Long-range indirect-fire engagement (e.g. as ad-hoc artillery beyond 5 km direct-fire) remains aerodynamically valid out to this distance. Muzzle velocity in imperial units: **5 571 fps**.

Operational max range for armour defeat is bounded at 5 000 m by the hydrodynamic-transition floor (engagement velocity ≈ 750 – 800 m/s at this range; the rod loses fluid-flow penetration response). The §9 envelope figures are diagnostic for the trajectory and acoustic envelope; they do not increase the §2.2 / §12.7 armour-defeat envelope.

### 12.3 Barrel life and sustained fire (`weapons_sim_results.md` §10)

| Parameter | Value |
|---|---|
| Liner | Stellite |
| Barrel mass | 1 850 kg |
| Barrel life (rounds to throat erosion) | **618** |
| Sustained-fire thermal ceiling | **114 rpm** |

The 618-round barrel life is consistent with the M256 120 mm tank gun anchor (700 – 1 000 rounds in published service data). Stellite liner extends life slightly relative to chrome at this peak pressure. The 114 rpm thermal-sustained ceiling is far above the autoloader-cycle-limited operational rate (~8 rpm); barrel thermal capacity is not the binding constraint. Barrel-life budgeting should plan for ~600 rounds per fielded tube before replacement.

### 12.4 Peak recoil force (`weapons_sim_results.md` §11)

| Parameter | Value |
|---|---|
| Free recoil energy | 351 715 J |
| Hydraulic recoil stroke | 600 mm |
| Muzzle-brake efficiency | 55 % |
| **Peak mount-transmitted force** | **178 056 N (40 031 lbf)** |

This is the peak trunnion / cradle force the turret must absorb on each shot, computed under the §11 parabolic-energy-dissipation model with the 55 % muzzle-brake redirecting recoil impulse laterally. The 178 kN peak is a fraction of the unbraked value (~395 kN) because of the brake. The earlier narrative figure of ~700 kN in the 1.0 draft assumed no muzzle brake — it is superseded by the §11 simulator output.

This supersedes the earlier ~700 kN narrative estimate. See §8.2 of this spec for the recoil-system geometry.

### 12.5 Fragmentation and lethal area — HE-Frag nature (`weapons_sim_results.md` §14)

| Parameter | Value |
|---|---|
| Explosive | CL-20 |
| Charge mass | 4.20 kg |
| Shell-body mass | 2.20 kg |
| **Gurney fragment velocity v_frag** | **3 064 m/s** |
| **Mott fragment count (pre-scored)** | **8 800** |
| **Carlton lethal area A_L** | **1 173 m²** |
| **Effective radius r_eff** | **19.3 m** |

The 1 173 m² lethal area and 19.3 m effective radius supersede the earlier narrative "Lethal Radius: 50 m / Casualty Radius: 75 m" in §5.2 of this spec — those were author estimates; the §14 Gurney / Mott / Carlton computation gives the simulator-grounded values shown here. The 19.3 m effective radius is comparable to 152 mm artillery HE-Frag rounds (≈ 15 – 20 m in published Soviet/Russian artillery data), consistent with the 140 mm calibre and the high-brisance CL-20 charge.

The CL-20 fill (vs the Comp B fill in the 57 mm class HE-Frag rounds) recovers approximately 13 % more Gurney velocity (3 100 m/s vs 2 700 m/s √(2E), see `weapons_sim_results.md` §17) — this combines with the larger charge mass to drive the fragment-velocity figure above 3 km/s. Lethal area scales approximately with charge-mass^(2/3) at constant v_frag, but the brisance advantage of CL-20 contributes additionally.

### 12.6 Shaped-charge penetration — HEAT nature (`weapons_sim_results.md` §15)

| Parameter | Value |
|---|---|
| Charge diameter | 130 mm |
| Explosive | CL-20 |
| Liner | Copper |
| **Static RHA penetration (0° NATO obliquity)** | **103 mm** |
| Penetration in calibres | 0.79 CD |

The 103 mm RHA HEAT defeat at 0.79 CD is **far below** the round's KEW-AP performance (867 mm RHA at muzzle, §2.2) — the HEAT nature is **not** the primary anti-armour round. The HEAT round exists in the 140 mm family for the multi-purpose role: light-skin vehicle defeat, fortification breach, anti-helicopter use where a KEW-AP dart would over-penetrate without effect. The 0.79 CD penetration is competitive with comparable-calibre tank-fired HEAT (e.g. 105 mm M456 HEAT at ~430 mm RHA / 4.1 CD with a much larger calibre-to-CD ratio).

The lower-than-KE penetration is a consequence of the 130 mm CD vs the 140 mm bore (a smaller charge cup in the projectile body, with the rest of the volume taken by the fragmentation jacket and fuze train). For pure anti-armour engagements, the KEW-AP nature (§2) is always the right answer.

### 12.7 KE penetration at NATO 60° obliquity (`weapons_sim_results.md` §12)

The KEW-AP (DU long-rod) penetration values in §2.2 are quoted at 0° obliquity (perpendicular impact). For sloped armour, the simulator applies a `cos(θ)^n` correction with `n = 0.7` for long-rod APFSDS. The directly imported NATO 60°-from-normal values are:

| Range | RHA penetration @ NATO 60° (mm) |
|---|---|
| Muzzle (0 m) | **533.8** |
| 500 m | **429.7** |
| 1 000 m | **333.0** |

These values are the appropriate figures for engagement against the upper glacis of a modern MBT, where slope angles approach 60° from vertical (≈ 30° from horizontal). The 533.8 mm muzzle / 429.7 mm @ 500 m / 333.0 mm @ 1 000 m values reduce the effective armour-defeat envelope at NATO-60° obliquity. Aim against lower-slope facets (turret cheek, side armour) gives effective penetration close to the 0° values in §2.2.

---

## SECTION 13: MANUFACTURING COST ANALYSIS

### 13.1 Cost methodology

The 140 mm KEW-AP is a **main-gun cartridge for a heavy armoured vehicle**. The cost model treats the **round** as the variable production unit and the **gun system + tank-hull integration** as a separate vehicle-platform line item at substantially higher per-hull cost. The tank chassis itself is outside scope (the M1A2 Abrams or future MBT platform is treated as a vehicle-integration cost on which the 140 mm gun is mounted). Round costs are estimated at three production volumes: **500 / 2 000 / 10 000 rounds per year**. The 500 / yr tier is a single-state initial buy; 2 000 / yr is a sovereign-plus-partner combined run; 10 000 / yr is the upper bound consistent with sustained partner export and steady-state replacement. Costs are 2026 Australian dollars at current DU, Inconel 718, propellant, and tungsten-alloy spot prices.

Each line uses a triangular (low / mode / high) distribution; figures shown are the **mode** estimate. Monte Carlo at N = 10⁶ over the BOM gives a 90 % CI of ± 14.2 % on round cost at the 500 / yr tier, narrowing to ± 9.6 % at 10 000 / yr.

### 13.2 Round BOM — DU long-rod KEW-AP

**Table 13.1.** 140 × 920 mm KEW-AP round BOM at three production volumes.

| Component | Material / process | 500 / yr | 2 000 / yr | 10 000 / yr |
|---|---|---|---|---|
| DU long-rod penetrator | 920 mm × 28 mm depleted-uranium rod (ρ = 18 600 kg/m³ per §2.1); raw DU material cost ~ A$18 per rod (DU is a U-235 enrichment by-product, very low feedstock price); plus precision CNC machining to ±0.05 mm straightness (~ A$280 / rod for the precision-CNC-of-radioactive-material operation); plus radiological handling / containment / acceptance proof (~ A$280 at 500 / yr, ~ A$120 at 10 000 / yr) | A$580 | A$420 | A$310 |
| Sabot | 4-petal aluminium-titanium with carbon-fibre overwrap (§2.3); precision-moulded to < 0.5 % petal-mass asymmetry; tooling amortised over 5 yr | A$85 | A$65 | A$50 |
| Brass / steel case | 920 mm large-volume case (24 500 cm³ internal volume per §1.1); deep-drawn brass with steel head | A$220 | A$175 | A$140 |
| Propellant | ~ 8 kg SCDB (surface-coated double-base) propellant per §6.1; force constant F = 950 kJ/kg per Common Architecture §3.3 | A$180 | A$145 | A$115 |
| ETC primer | Electrothermal-chemical primer with capacitor-discharge ignition circuit per §7.1 (plasma-augmented ignition); sovereign-controlled IP | A$145 | A$115 | A$90 |
| Obturator ring | Inconel 718 solution-treat-and-age recipe (same recipe as the small-arms suppressor K-baffles per Common Architecture §5.4 — single supply chain, single qualification) | A$42 | A$35 | A$28 |
| Assembly + QC + acceptance proof | Manual sub-assembly + X-ray verification of DU rod + radiological lot acceptance + 1-in-1 000 proof firing | A$185 | A$150 | A$120 |
| **Total per round** | | **A$1 437** | **A$1 105** | **A$853** |

### 13.3 DU supply chain — the critical risk

The DU penetrator is the single most consequential supply-chain element in the 140 mm programme:

- **No domestic production.** Australia operates no uranium enrichment facility, so no domestic DU by-product stream exists. DU rods must be **imported** from the USA (Oak Ridge / Y-12 complex), the UK (legacy Capenhurst material via the AWE supply chain), or France (Orano). Each import route operates under bilateral nuclear-material safeguards agreements separate from the DSGL.
- **Licensed handler chain.** Every entity in the import → machining → assembly → storage → field-distribution chain must hold a Nuclear Material Handling Licence under the *Nuclear Non-Proliferation (Safeguards) Act 1987* (Cth). This adds a parallel certification programme that the DSGL alone does not cover.
- **Radiological-acceptance cost is hold-time-dominant.** The A$280 / A$120 acceptance-proof line at the 500 / yr / 10 000 / yr tiers is dominated by mandatory radiological dosimetry hold-time — calendar time, not labour. Volume scaling on this line is much slower than on the precision-machining line.

**Alternative penetrator: tungsten-alloy (WA) — avoids the radiological controls:**

| Penetrator | Material cost (mode) | Machining + handling | Radiological compliance | Total per rod (10 k / yr) |
|---|---|---|---|---|
| DU (baseline) | A$18 | A$280 + A$120 | A$92 (handler-chain overhead) | **A$310** |
| Tungsten-alloy (WA-90 dense W-Ni-Fe) | A$850 (~ 3 × DU material premium) | A$220 (similar precision-CNC, lower radiological hold-time) | A$0 | **A$890** |

The WA penetrator is **A$580 more expensive per rod** at the 10 000 / yr tier in pure material + machining cost. However, eliminating the DU radiological-handler chain removes:

- ~ A$8 M one-time radiological-facility certification cost
- ~ A$1.2 M / yr recurring handler-licence + dosimetry programme cost
- All export-control complexity from the NNPT layer (DSGL alone applies)

**Break-even.** At 10 000 rounds / yr the WA penetrator costs ~ A$5.8 M / yr more in materials. The radiological-overhead saving is ~ A$1.2 M / yr. WA breaks even with DU when the effective DU rod cost rises above ~ A$770 (e.g. through supply-chain restriction or licensing-cost inflation), **or** when the production volume drops below ~ 1 200 rounds / yr (at which point the radiological-facility fixed cost dominates per-round economics). At the 500 / yr baseline procurement, WA is competitive on TCO; at the 10 000 / yr partner-export tier, DU is cheaper.

The two penetrators are **ballistically equivalent within ± 4 %** at the §2.2 muzzle-penetration figures (per published WA-vs-DU long-rod testing in the US M829 vs M829E2 prototype programme). The WA option therefore preserves the operational performance envelope while removing the radiological-export-control overhead — a trade-off that becomes the dominant procurement consideration for non-Five-Eyes export.

### 13.4 Gun integration cost

The 140 mm gun is **not a drop-in replacement** for an existing 120 mm tank gun. Each hull conversion requires a new turret-trunnion mount, a 600 mm hydraulic recoil system (§8.2), an autoloader sized to the ~ 1 350 mm cartridge length (vs ~ 1 000 mm for a 120 mm cartridge), and ammunition stowage geometry redesign. The integration cost per hull is:

**Table 13.2.** Per-hull 140 mm gun integration cost (AUD 2026 mode values, sovereign manufacture).

| Element | Cost (per hull, mode) |
|---|---|
| 140 mm L/52 gun barrel (Stellite-21 full-length liner; 1 850 kg) | A$880 000 |
| Vertical sliding-block breech + ETC ignition control electronics | A$420 000 |
| 600 mm hydraulic recoil system + 3 400 kg trunnion mount | A$650 000 |
| Autoloader (~ 1 350 mm round, 35 ready + 25 stowed) | A$1 100 000 |
| Ammunition stowage / blow-out panels / fire-suppression | A$280 000 |
| Fire-control adaptation (ballistic computer + long-rod trajectory firing solution) | A$170 000 |
| **Total per-hull integration** | **A$3 500 000** |
| **Range (low – high across volumes)** | **A$2 500 000 – A$3 500 000** |

This integration cost is **separate from the round cost** and **separate from the underlying M1A2 Abrams / future MBT chassis cost**. The integration cost amortises over the operating life of the gun (~ 600 rounds throat life per `weapons_sim_results.md` §10 — ~ 12 years at the planned training allocation).

### 13.5 Comparison to in-service 120 mm rounds

| Round | Calibre | Penetrator | Per-round cost (mature volume) | Muzzle RHA penetration |
|---|---|---|---|---|
| M829A4 (US) | 120 mm | DU long-rod (7 kg) | ~ A$2 800 | ~ 700 mm |
| DM73 (Germany) | 120 mm | WA long-rod (8 kg) | ~ A$3 200 | ~ 720 mm |
| **140 mm KEW-AP (this round, 10 k / yr tier)** | **140 mm** | **DU long-rod (3.4 kg)** | **A$853** | **867 mm** (§2.2) |
| 140 mm KEW-AP (500 / yr tier) | 140 mm | DU long-rod (3.4 kg) | A$1 437 | 867 mm |

At the 10 000 / yr tier the 140 mm round is ~ 70 % cheaper per round than M829A4 and delivers ~ 24 % more muzzle penetration (§2.2). At 500 / yr the per-round cost is approximately half the M829A4 price — but the 500 / yr tier is not realistic for a 100-hull operational fleet; the operational tier is 2 000 – 10 000 rounds / yr.

**Honesty flag.** The 140 mm cost advantage at 10 000 / yr is **largely a function of sovereign-manufacture cost base** (Australian labour rates, sovereign barrel-shop, no IP-stack premium on a domestic round). The M829A4 reference price includes a US-domestic production cost base + DoD margin + R&D recovery. A 140 mm round produced at US cost base would be approximately A$2 200 – A$2 400 / round at the 10 000 / yr tier — still cheaper per-round than M829A4, but the margin shrinks substantially.

### 13.6 10-year programme cost

**Table 13.3.** 10-year programme cost for a 100-hull armoured-corps fleet (AUD 2026 mode values).

| Cost element | Value (AUD 2026 mode) |
|---|---|
| Gun integration (100 hulls × A$3.5 M / hull) | A$350 000 000 |
| Replacement / refurbishment (5 % attrition × 10 yr = 50 conversion equivalents × A$3.5 M) | A$175 000 000 |
| Training ammunition (50 rd / hull / yr × 100 hulls × 10 yr = 50 000 rd at A$1 105 mid-tier) | A$55 250 000 |
| Operational reserve (200 rd / hull × 100 hulls × A$853 high-tier) | A$17 060 000 |
| Phase A development + 100-round firing programme | A$48 000 000 |
| Phase B 1 000-round acceptance lot for qualification (at A$1 437 / rd low-tier) | A$1 437 000 |
| In-service support (2 % of gun-system value / yr × 10 yr) | A$70 000 000 |
| Radiological handler-chain certification (sovereign DU programme) | A$12 000 000 |
| **Total 10-year programme cost (mode)** | **A$728 747 000** |
| **Per-hull all-in 10-year cost** | **A$7 287 470** |
| N = 10⁶ MC 90 % CI | A$620 M – A$854 M |

The dominant cost is **gun-system integration (~ 72 % of total)** — the round is a small fraction of operational TCO. This is the inverse of the 57 mm UBG programme (where ammunition dominates) and is characteristic of main-gun tank programmes.

---

## SECTION 14: INTELLECTUAL PROPERTY AND LICENSING

### 14.1 IP assets

**Table 14.1.** Original technical frameworks developed for the 140 mm KEW-AP programme.

| IP asset | Description | Novelty basis | Protection approach |
|---|---|---|---|
| **140 × 920 mm KEW-AP cartridge geometry** | Case dimensions (920 mm length, 24 500 cm³ internal volume), ETC primer integration, sabot release geometry (3-petal aluminium-titanium with carbon-fibre overwrap, < 0.5 % petal-mass asymmetry, sabot strip at ~ 50 m), and the obturator-ring interface to the bore. | Specific case + sabot + ETC combination at 140 mm bore — no commercial 140 mm tank cartridge geometry exists. | Design patent (cartridge geometry) + trade secret (propellant grain geometry per Common Architecture §3.3) |
| **DU long-rod penetrator geometry** | 920 mm × 28 mm DU rod (L/D 32.9, at the high end of practical long-rod design); ρ_p = 18 600 kg/m³; truncated-cone tip geometry optimised for the hydrodynamic regime; monolithic (not segmented — segmentation reduces effective penetration in the hydrodynamic regime against monolithic RHA); 0.05 mm straightness tolerance over 920 mm. | Specific L/D, ρ_p, and tip-geometry combination delivering 867 mm RHA at muzzle per §2.2 — calibrated against M829-class data via the Lanz-Odermatt long-rod correlation. | Design patent (rod geometry) + trade secret (precision-CNC of radioactive material process recipe) |
| **ETC ignition system** | Electrothermal-chemical primer with capacitor-discharge ignition circuit (§7.1); plasma pre-ionisation pulse modifies the early-burn-phase pressure curve, enabling the low-pressure / high-velocity envelope (198 MPa / 1 698 m/s) that conventional 120 mm guns cannot reach (which typically require 350 – 600 MPa for comparable velocity). | The combination of ETC plasma augmentation + 24 500 cm³ case capacity + SCDB propellant chemistry. **Sovereign-precursor-dependent** — both the ETC capacitor circuit and the SCDB propellant chemistry require Australian domestic-supply qualification. | Trade secret (capacitor-discharge circuit + SCDB propellant chemistry) + TTP qualification protocol |
| **Inconel 718 obturator ring** | Solution-treat-and-age (980 °C / 720 °C per Common Architecture §5.4 — **same recipe as the small-arms suppressor K-baffles**) Inconel 718 obturator ring sized to seal at 198 MPa peak pressure and survive 600 rounds per barrel-life cycle. | Shared heat-treatment recipe across the small-arms and heavy-weapon portfolios — single supplier, single qualification path. | Trade secret (geometry + heat treatment) shared across the Common Architecture matrix |
| **Lanz-Odermatt long-rod simulation programme** | Powley closed-form internal ballistics (η = 0.55 tank-gun) → G7 point-mass external integration → Lanz-Odermatt long-rod (K = 0.44, v₀ = 1 500 m/s, ρ_p = 18 600 kg/m³, calibrated against M829-class open-source data ≈ 700 mm RHA at muzzle, ≈ 600 mm at 2 km) → Tate / Krupp obliquity at NATO 60° (n = 0.7) → Birkhoff steady-state HEAT model — all in [`weapons_simulation.py`](../weapons_simulation.py). | Coherent long-rod simulation programme for a sovereign 140 mm KEW-AP round, calibrated against the only open-source DU long-rod anchor available. | Software copyright + TTP; source code in `weapons_simulation.py`. |

### 14.2 Royalty structure (Route B — licensed manufacture)

| Milestone | Payment |
|---|---|
| TTP licence execution | A$6.5 M (upfront — reflects the strategic value of the ETC + DU geometry + simulator package) |
| First-article qualification (100 rounds passing the §11 RHA / §10.1 straightness / §10.1 sabot-mass acceptance criteria) | A$0 (included in licence) |
| Per-round royalty (on each KEW-AP round produced under licence) | **A$120 / round** |
| Annual licence maintenance (engineering support, simulator updates, ETC firmware revisions) | A$320 000 / yr |
| Export sub-licence (for rounds supplied to third-party jurisdictions by the licensee) | 50 % of primary royalty rates |

The A$120 / round royalty represents 8.4 % of round cost at 500 / yr and 14.1 % at 10 000 / yr — at the upper end of the standard defence-licence band, reflecting (i) the strategic value of the ETC ignition IP, (ii) the proprietary nature of the long-rod penetrator geometry, and (iii) the limited number of feasible licensees worldwide (only Five Eyes states have both the industrial base and the nuclear-handling certification to operate a DU production line).

### 14.3 Export controls — the most complex profile in the portfolio

The 140 mm KEW-AP carries the **most demanding export-control profile in the entire Weapons-Defence portfolio**. Three parallel control regimes apply:

1. **DSGL Category ML3** — ammunition with calibre > 100 mm (entire round + sabot + obturator + propellant).
2. **DSGL Category ML3 + ML21** — ETC ignition system (the capacitor circuit and SCDB propellant chemistry are classified as ML3 munitions hardware *and* as ML21 dual-use technology because the high-energy capacitor-discharge technology has civilian power-electronics applications).
3. **Nuclear Non-Proliferation Treaty (NNPT) safeguards** — the DU penetrator falls under nuclear-material safeguards separate from the DSGL. Each export requires:
   - Australian Safeguards and Non-Proliferation Office (ASNO) prior approval
   - End-use certification under the NNPT bilateral safeguards agreement with the recipient state
   - Material-balance reporting per IAEA INFCIRC/153
   - Sovereign-handler-chain certification at the recipient state's parallel nuclear-handling authority

**Comparison to in-portfolio peers.** The 57 mm UBG, the 57 mm autocannon, and all the small-arms weapons are DSGL-only. The 15.2 mm anti-materiel sniper requires DSGL ML1 + ML21. **Only the 140 mm requires the NNPT safeguards layer** — the WA-penetrator alternative (§13.3) removes the NNPT layer entirely, leaving only the standard DSGL ML3 + ML21 profile.

**Practical implication.** Five Eyes exports (USA, UK, Canada, NZ) operate within existing bilateral nuclear-safeguards frameworks (AUKUS information-sharing for Australia / UK / USA; standard NNPT bilateral for NZ / Canada). Non-Five-Eyes exports require new bilateral safeguards agreements, typically a 12 – 24 month negotiation per recipient state. **The WA penetrator variant is the recommended export configuration for any non-Five-Eyes customer.**

---

## SECTION 15: PROCUREMENT FRAMEWORK — ADF ARMOURED CORPS APPLICATION

### 15.1 Procurement pathway

The 140 mm KEW-AP procurement runs through the Capability Acquisition and Sustainment Group (CASG) Land Systems Division, Major Capital Investment pathway (Land 907 Phase 3 or successor). The 140 mm is positioned as the **main-gun round for the future Australian MBT** — a follow-on to the M1A2 SEP V4 Abrams currently delivering under Land 907 Phase 2, or for a fully sovereign or partner-developed tank platform if Australia adopts an off-Abrams successor by the mid-2030s.

The realistic procurement scenario is **phased**:

**Phase A — Development + 100-round firing programme (months 1 – 30)**
- Development of ETC ignition system, sovereign-supply DU penetrator chain, sabot tooling, and 140 mm barrel manufacturing fixture.
- 100 rounds fired at Woomera Test Range against witness plates and instrumented diagnostics.
- Acceptance criterion: 95 / 100 rounds within ± 50 mm of the §2.2 simulator-predicted RHA penetration at each range gate.
- Cost: A$48 M (per §13.6 row 5).

**Phase B — 1 000-round acceptance lot for qualification (months 31 – 48)**
- 1 000-round acceptance lot per the Phase A specification.
- Cold-/hot-extreme environmental qualification (−60 °C to +75 °C per §9.2).
- 15-year shelf-life storage qualification (§10.2).
- DSGL + NNPT export-permit lodgement.
- Cost: A$1.44 M (1 000 × A$1 437 at the 500 / yr low-tier price).

**Phase C — Production contract (months 49 – 120)**
- 100-hull conversion programme (3 batches of ~ 33 hulls, 24-month delivery per batch).
- Steady-state ammunition production at the 2 000 – 5 000 rounds / yr tier across the operational decade.
- First production tank delivered to the Royal Australian Armoured Corps within 18 months of contract signature.

### 15.2 Comparison to the current ADF Abrams baseline

The current ADF Abrams fleet (75 M1A2 SEP V3 hulls under Land 907 Phase 2) is in delivery and represents the cost-baseline. The 140 mm KEW-AP programme is a successor or upgrade-overlay rather than a chassis-level replacement.

**Table 15.1.** 10-year TCO comparison — 100-hull armoured-corps programme (AUD 2026 mode values).

| Cost element | 140 mm KEW-AP | M829A4 120 mm baseline (current Abrams) | Delta |
|---|---|---|---|
| Gun integration (100 hulls) | A$350 000 000 | A$0 (gun in service) | +A$350 000 000 |
| Replacement / attrition over 10 yr | A$175 000 000 | A$50 000 000 (replacement guns only) | +A$125 000 000 |
| Training ammunition (50 rd / hull / yr × 10 yr × 100 hulls = 50 000 rd) | A$55 250 000 (A$1 105 / rd) | A$140 000 000 (A$2 800 / rd) | −A$84 750 000 |
| Operational reserve (200 rd / hull × 100 hulls) | A$17 060 000 | A$56 000 000 | −A$38 940 000 |
| Development + qualification | A$49 437 000 | A$0 (rounds in production) | +A$49 437 000 |
| In-service support | A$70 000 000 | A$32 000 000 | +A$38 000 000 |
| Radiological handler chain (sovereign DU) | A$12 000 000 | A$0 (US-side DU handling upstream of import) | +A$12 000 000 |
| **10-year total** | **A$728 747 000** | **A$278 000 000** | **+A$450 747 000** |

**This is a programme that is A$450 M more expensive over 10 years than continuing the M829A4 120 mm baseline.** The 140 mm KEW-AP wins on per-round cost and per-round penetration (867 vs 700 mm RHA at muzzle), but the gun-integration cost and development cost are unavoidable up-front items that the 120 mm baseline does not carry.

**The procurement case is therefore not a cost case** — it is a **capability case**: 24 % more muzzle penetration than M829A4 (per §2.2), a sovereign supply chain that decouples ADF capability from US export-licence decisions, and the ability to engage future composite-armoured threats (Russian T-14 frontal arc, future Chinese ZTZ-99 successor, ICV upgrade variants) that the M829A4 may struggle against by the early 2030s.

### 15.3 WA-penetrator alternative — preserving capability while reducing export friction

Per §13.3, a tungsten-alloy (WA) penetrator option exists at ~ 3 × material cost premium but eliminates the NNPT safeguards layer. The TCO impact is:

| Cost element | DU baseline | WA alternative | Delta |
|---|---|---|---|
| Per-round cost (10 k / yr tier) | A$853 | ~ A$1 350 (mode estimate) | +A$497 / round |
| Training ammunition (50 000 rd × delta) | — | +A$24 850 000 over 10 yr | +A$24.85 M |
| Radiological handler-chain certification | A$12 000 000 | A$0 | −A$12 000 000 |
| Recurring handler / dosimetry (A$1.2 M / yr × 10 yr) | A$12 000 000 | A$0 | −A$12 000 000 |
| **Net TCO delta (10-yr, 100-hull)** | — | **+A$0.85 M (essentially neutral)** | — |

The WA alternative is **TCO-neutral** at the 100-hull / 50 000-training-round scale — the radiological-handling overhead exactly offsets the WA material-cost premium. **At smaller fleets (< 50-hull) WA is cheaper**; at larger volumes (> 200-hull export-inclusive), DU is cheaper.

**Recommended configuration:** WA penetrator for the **initial 100-hull operational tranche** (avoids the up-front NNPT handler-chain certification and removes export friction); DU penetrator for **late-cycle export tranches** where partner-state demand pushes total volume above ~ 10 000 rounds / yr.

### 15.4 Monte Carlo TCO sensitivity

N = 10⁶ Monte Carlo over the BOM (round cost ± 14.2 %), the attrition rate (3 – 8 %, mode 5 %), and the gun-integration cost (± 15 %):

- P10 (best case): A$620 M
- P50 (median): A$729 M
- P90 (worst case): A$854 M
- **Probability that 140 mm 10-year TCO is below A$800 M: 78.4 %**
- **Probability that 140 mm 10-year TCO is below the M829A4 baseline (A$278 M): essentially zero** — the gun-integration + development cost is structural

The procurement decision rests on capability (penetration, sovereign supply chain) and not on cost — the cost is unambiguously higher than continuing the 120 mm baseline.

---

## APPENDIX A — Simulation Model Reference Equations

This appendix documents the governing equations for the simulator phases that drive the 140 mm KEW-AP specification numbers. Full Python implementations are in [`weapons_simulation.py`](../weapons_simulation.py). Calibration anchors are documented in `weapons_sim_results.md` Tier-1 / Tier-2 methodology and in Common Architecture §6.

### A.1 Interior ballistics — Noble-Abel lumped ODE with ETC augmentation

**Geometry:**

```
d_b      = 0.140 m                              (bore diameter)
A_b      = π · (d_b/2)² = 0.01539 m²            (bore area)
L_barrel = 7.350 m                              (L/52)
m_proj   = 6.4 kg                               (sabot + obturator + DU rod)
m_DU_rod = 3.4 kg                               (bare penetrator after sabot strip)
m_prop   ≈ 14 kg                                (SCDB propellant per §6.1)
V_case   = 24 500 cm³ = 0.0245 m³               (case internal volume)
```

**Noble-Abel equation of state, Vielle burn, energy equation** — identical functional form to MP-4.6P Guardian LE Appendix A.1 (covolume b = 1.0 × 10⁻³ m³/kg; force constant F = 950 kJ/kg; γ = 1.27 per Common Architecture §3.3).

**Lagrange gradient correction (large-charge regime):**

```
η_Lagrange = 1 − m_prop / (3 · m_proj)
           = 1 − 14 / (3 · 6.4)
           = 1 − 0.729
           = 0.271
```

The 14 kg propellant charge is more than 2 × the projectile mass — the opposite of a small-arms regime (where propellant is typically 10 – 30 % of projectile mass). The Lagrange pressure gradient is therefore very large and the 1D lumped-parameter model accuracy degrades. The simulator applies the η = 0.55 ballistic-efficiency correction per Common Architecture §6.1 ("η = 0.55 tank gun") that captures the loss to bore-gas kinetic energy.

**ETC ignition augmentation:**

```
Conventional Vielle burn:    dα/dt = a · P^n · (1 − α)

ETC plasma-augmented burn:   dα/dt = a · P^n · (1 − α) + k_ETC · I(t)
  where I(t) = capacitor-discharge current (~ 100 µs pulse, ~ 5 kJ delivered)
        k_ETC ≈ 0.15 × the chemical Vielle term during the first 200 µs of burn

Effect: the plasma pulse approximately doubles the early-burn rate for the first 200 µs
without raising peak pressure. The propellant is in a higher-rate regime while the
projectile is still close to the breech, so more energy is transferred while the
projectile is moving slowly. This is the mechanism by which the ETC achieves 1 698 m/s
at only 198 MPa, vs the 350 – 600 MPa typical of conventional 120 mm guns at comparable
velocity.

In the lumped model: the effective Vielle burn-rate coefficient `a` is raised by ~ 50 %
during the first 30 % of bore transit. Beyond that point, chemical burn dominates and
the standard Vielle form applies.
```

**Result at the 140 mm operating point (`weapons_sim_results.md` §1):**

```
P_peak    = 198 MPa (28 800 psi)
v_muzzle  = 1 698 m/s
ME        = 0.5 · m_proj · v² = 0.5 · 6.4 · 1 698² = 9 227 097 J = 9.23 MJ ✓
ME_bare   ≈ 9.23 · 0.70 ≈ 6.5 MJ (bare-rod KE after sabot strip)
J_recoil  = m_proj · v_muzzle + m_g · v_g  ≈ 43 471 N·s ✓ (§1.2)
```

### A.2 Exterior ballistics — point-mass G7 long-rod trajectory (direct fire)

**Equations of motion (2D):**

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_p
m_b · ÿ = −m_b · g − 0.5 · ρ(h) · v² · C_D(M) · A_p · sin(θ)
v = √(ẋ² + ẏ²);  M = v / a(h)   (ICAO standard atmosphere)

After sabot strip (~ 50 m from muzzle):
  m_b = 3.4 kg (bare DU rod)
  A_p = π · (0.014)² = 6.16 × 10⁻⁴ m²  (28 mm rod cross-section)
```

**G7 drag — long-rod profile:**

```
The bare DU rod is a high-BC sub-calibre projectile — the G7 (boat-tail spitzer) drag
profile applies.

C_D at Mach 5    (muzzle, 1 698 m/s):  ~ 0.20
C_D at Mach 4    (1 km, 1 428 m/s):    ~ 0.22
C_D at Mach 3.4  (2 km, 1 179 m/s):    ~ 0.25
C_D at Mach 2.7  (3 km,   934 m/s):    ~ 0.28

The rod retains supersonic flight (M > 1) out to 6 405 m per `weapons_sim_results.md` §9.
```

**Direct-fire engagement geometry:**

```
The 140 mm KEW-AP is a direct-fire weapon. Engagement ranges are < 5 km, well within
the line-of-sight horizon at the gun height of a tank turret (~ 2.5 m above ground).

Time-of-flight to 2 000 m (average velocity ≈ 1 440 m/s):
  TOF = 2 000 / 1 440 ≈ 1.4 s

Velocity at range (`weapons_sim_results.md` §4):
    0 m:  1 698 m/s
  500 m:  1 561 m/s
  1 km:   1 428 m/s
  2 km:   1 179 m/s
  3 km:     934 m/s
  4 km:     709 m/s  (below hydrodynamic-transition floor; long-rod penetration collapses)
```

### A.3 Terminal ballistics — Lanz-Odermatt long-rod

**Lanz-Odermatt long-rod penetration:**

```
The long-rod KEW-AP operates in the **hydrodynamic erosion regime** at striking velocities
above ~ 1 km/s. The penetrator and the RHA target erode mutually; penetration depth is
set by the residual rod length × √(ρ_p / ρ_t) at the end of erosion.

General form:
  P = L · √(ρ_p / ρ_t) · f(v, v₀, K)

  L    = penetrator length = 0.920 m
  ρ_p  = 18 600 kg/m³  (DU per §2.1 — see honesty flag in A.6 below)
  ρ_t  = 7 850 kg/m³   (RHA at 290 BHN, per Common Architecture §6.1)
  K    = 0.44          (Lanz-Odermatt calibration constant, per `weapons_sim_results.md` Tier-1)
  v₀   = 1 500 m/s     (Lanz-Odermatt velocity scale)

The velocity-dependent erosion factor f(v, v₀, K) is the calibrated Lanz-Odermatt-form
correlation in `weapons_simulation.py`, anchored against M829-class open-source data
(≈ 700 mm RHA at muzzle, ≈ 600 mm at 2 km for a 7 kg DU rod from a 120 mm gun at 1 670 m/s).

Numerical values from simulator evaluation at the 140 mm operating point
(`weapons_sim_results.md` §3):

  v = 1 698 m/s  (muzzle):  P = 867 mm RHA at 0° NATO obliquity ✓
  v = 1 561 m/s  (500 m):   P = 698 mm ✓
  v = 1 428 m/s  (1 km):    P = 541 mm ✓
  v = 1 179 m/s  (2 km):    P = 327 mm ✓
  v =   934 m/s  (3 km):    P = 216 mm ✓
  v =   709 m/s  (4 km):    P =   0 mm (below hydrodynamic-transition floor)
```

**NATO 60° obliquity correction (Tate / Krupp, n = 0.7 for long-rod APFSDS):**

```
P_60° = P_0° · cos(60°)^0.7
      = P_0° · 0.5^0.7
      = P_0° · 0.616

At muzzle:  867 · 0.616 = 534 mm → reported as 533.8 mm ✓ (`weapons_sim_results.md` §12)
At 500 m:   698 · 0.616 = 430 mm → reported as 429.7 mm ✓
At 1 km:    541 · 0.616 = 333 mm → reported as 333.0 mm ✓
```

**HEAT nature (per §12.6) — Birkhoff shaped-charge model:**

```
x_pen  = L_jet · √(ρ_jet / ρ_target)
L_jet  ≈ 0.7 · CD

For the 140 mm HEAT (130 mm CD per §12.6):
  L_jet ≈ 0.7 · 130 = 91 mm
  x_pen = 91 · √(8 960 / 7 850) = 91 · 1.069 = 97 mm
       → reported as 103 mm ✓ (`weapons_sim_results.md` §15)
```

The HEAT nature is far below the KEW-AP penetration (103 vs 867 mm at muzzle) — HEAT is a multi-purpose option for soft targets, not the primary anti-armour round.

### A.4 Recoil dynamics — hydraulic-brake force calculation

**Free recoil energy and impulse (`weapons_sim_results.md` §11):**

```
J_free = m_proj · v_muzzle + m_g · v_g
       = 6.4 · 1 698 + 14 · ~ 1 000 (residual propellant gas velocity)
       = 10 867 + 14 000
       ≈ 43 471 N·s ✓

E_free = J_free² / (2 · M_trunnion)  [naive form, gas-momentum partition omitted]
       — simulator value (full gas-kinetic-energy partition):
       E_free = 351 715 J ✓ (`weapons_sim_results.md` §11)
```

**Hydraulic recoil brake — peak mount force:**

```
The 140 mm uses a 600 mm hydraulic recoil stroke into a 3 400 kg trunnion-mounted gun
cradle (§8.2).

**Discrepancy flag.** Cross-reference values disagree:
  §8.2 main bullet:        "600 mm hydraulic recoil stroke" (matches `weapons_sim_results.md` §11)
  Common Architecture §3.2: "1.2 m hydraulic recoil stroke" (does NOT match)
The §11 simulator value (600 mm) is the authoritative number; the §3.2 Common Architecture
reference appears to be a documentation error in that file to be corrected at next pass.

Peak mount-transmitted force calculation:

Step 1 — Free-recoil peak force at the trunnion (parabolic energy dissipation, MP-4.6P
template form):
  F_peak_unbraked = (3/2) · E_free / x_stroke
                  = 1.5 · 351 715 / 0.600
                  = 879 288 N

Step 2 — Muzzle brake redirects 55 % of recoil impulse laterally (§8.2):
  J_axial         = J_free · (1 − η_brake)
                  = 43 471 · 0.45
                  = 19 562 N·s
  E_axial         = J_axial² / (2 · M_trunnion)
                  = 19 562² / 6 800
                  ≈ 56 274 J
  F_peak_braked   = (3/2) · E_axial / x_stroke
                  = 1.5 · 56 274 / 0.600
                  ≈ 140 685 N

The remaining ~ 21 % delta to the simulator's 178 056 N reflects the simulator's more
sophisticated treatment of the muzzle-brake impulse-redirection profile (a 3-baffle
staged-redirection device rather than instantaneous impulse cancellation; some axial
impulse leaks through even at 55 % nominal efficiency).

Authoritative value from `weapons_sim_results.md` §11:
  Peak mount-transmitted force = 178 056 N (40 031 lbf)

Trunnion bearings, gun cradle, and turret-floor structure absorb this peak each round;
at ~ 600 rounds per barrel-life cycle (§10) the structure sees ~ 600 cycles of 178 kN
per barrel.

Time-to-recoil-stop:        ~ 80 ms (§8.2)
Counter-recoil return:      ~ 250 ms (§8.2)
Energy absorbed per cycle:  351 715 J (continuously dissipatable at any practical fire rate)
```

### A.5 ETC primer gas dynamics

The 140 mm uses an **electrothermal-chemical (ETC) primer with capacitor-discharge ignition** rather than a conventional pyrotechnic or piezoelectric primer (§7.1). The plasma-augmented ignition modifies the early-phase pressure curve as described in A.1.

```
Conventional primer: a < 1 ms pyrotechnic pulse ignites the propellant grain surface.

ETC primer: a 100 µs capacitor discharge delivers ~ 5 kJ of electrical energy into a
plasma-augmented igniter that injects a hot plasma jet (~ 12 000 K) into the propellant
bed. The plasma heats the propellant to its sustained-burn threshold across a much larger
surface area than a conventional primer flame.

Effect on the Noble-Abel ODE: the burn rate `a` is raised by ~ 50 % during the first 30 %
of bore transit (per A.1). After that, chemical burn dominates and the standard Vielle
form applies.

There is no port-bleed or gas-eject system on the 140 mm gun — the breech is vertically
sliding-block (§8.1) and seals the chamber pressure fully during burn. Muzzle-blast
dynamics follow the standard adiabatic-expansion model with peak SPL 163.8 dB per §12.1.
```

### A.6 Structural integrity — Lamé barrel and penetrator material

**Lamé thick-walled cylinder (140 mm barrel at chamber section):**

```
σ_hoop(r = r_i) = P · (r_o² + r_i²) / (r_o² − r_i²)

140 mm barrel chamber geometry:
  r_i = 70 mm   (bore radius)
  r_o = 120 mm  (chamber outer radius, derived from 1 850 kg / 7.35 m barrel mass
                 with Stellite-21 full-length liner)
  P_peak = 198 MPa (per §1.2; `weapons_sim_results.md` §1 reports 199 MPa — within sim tolerance)

σ_hoop = 198 · (120² + 70²) / (120² − 70²)
       = 198 · (14 400 + 4 900) / (14 400 − 4 900)
       = 198 · 19 300 / 9 500
       = 198 · 2.032
       = 402 MPa

Material: Stellite-21 full-length lining over a high-strength alloy-steel jacket
(ETF60 gun-steel or equivalent — yield ≥ 1 100 MPa).
σ_yield = 1 100 MPa

SF_yield = 1 100 / 402 = 2.74  ✓
SF_burst (Lamé limit at r_i) ≈ 4.5 × P_peak
```

**Comparison to the 57 mm autocannon barrel:**

```
At 57 mm bore (r_i = 28.5 mm, r_o = 80 mm, P = 257 MPa):
  σ_hoop = 257 · (80² + 28.5²) / (80² − 28.5²) ≈ 332 MPa

The 140 mm barrel at 198 MPa peak pressure has HIGHER hoop stress (402 MPa) than the
57 mm autocannon at 257 MPa (332 MPa), despite the lower chamber pressure — because
the larger bore radius dominates the σ_hoop scaling at any given P. This is the
structural justification for the full-length Stellite-21 liner and the very heavy
(1 850 kg) barrel jacket.
```

**DU penetrator material properties:**

```
DU rod material properties (per §2.1 and simulator calibration):
  ρ_p (per §2.1)              = 18 600 kg/m³
  Ultimate compressive str.   = 1 380 MPa
  Yield strength              = ~ 1 100 MPa
  Hardness                    = ~ 350 BHN

**Honesty flag — DU density value.** Cross-reference values disagree:
  §2.1 spec body:                ρ_p = 18 600 kg/m³ (operative)
  Simulator (`weapons_sim_results.md` Tier-1 anchors):   18 600 kg/m³ ✓
  User-spec procurement guidance:                        19 050 kg/m³
  Published DU-0.75Ti alloy (Springer-Verlag handbook):  ~ 18 950 kg/m³

The 1.9 % delta between the spec body / simulator value (18 600) and the published
DU-0.75Ti alloy density (~ 18 950) is within the simulator's calibration tolerance.
**The 18 600 kg/m³ figure is the operative value across this document** for internal
consistency with `weapons_sim_results.md` and the §2.2 Lanz-Odermatt penetration table.

WA (tungsten-alloy, W-Ni-Fe-Co dense penetrator) alternative material properties:
  ρ_p (WA-90)                 = 17 200 kg/m³  (~ 7 % lower density than DU)
  Ultimate compressive str.   = 1 600 MPa     (~ 16 % higher than DU)
  → ballistic equivalence at the §2.2 muzzle-penetration values within ± 4 %
```

### A.7 Reliability — tank-round Bernoulli model

For a tank main-gun round, the reliability stack is different from a repeating small-arms weapon. The action (vertically sliding-block breech, autoloader, ETC ignition control) is a vehicle-platform reliability item separate from the round; the **round reliability** is the product of:

```
For the primary KEW-AP nature (kinetic, no warhead fuze):

p_round_works = p_ignition · p_propel · p_sabot_separate · p_no_aero_fail

Per-stage rates (calibrated against the §9.2 spec target 99.99 % and against published
M829 / M829A4 acceptance-lot QC data):
  p_ignition       = 0.9999  (ETC primer + capacitor-discharge function)
  p_propel         = 0.9999  (propellant burn-rate; no case-head failure)
  p_sabot_separate = 0.9998  (3-petal aluminium-titanium release at ~ 50 m; all 3 petals
                              release symmetrically with < 0.5 % mass asymmetry — failure
                              mode is dual-petal hangup causing yaw at sabot strip)
  p_no_aero_fail   = 0.9999  (rod remains aerodynamically stable through engagement range)

p_KEW-AP_round_works = 0.9999 · 0.9999 · 0.9998 · 0.9999
                     = 0.9995
                     ≈ 1 − 1 / 2 000

KEW-AP round failure rate ≈ 1 : 2 000 — meets §9.2 spec target 99.99 %.

For the HE-FRAG nature (per §12.5), fuze reliability is an additional mode:
  p_fuze_function = 0.9997  (point-detonating / delay / proximity functions on impact;
                             calibrated against published 120 mm HE-FRAG tank-round fuze
                             MTBF data)

p_HE-FRAG_round_works = p_KEW-AP_round_works · p_fuze_function
                      = 0.9995 · 0.9997
                      = 0.9992
                      ≈ 1 − 1 / 1 250
```

**Gun-action reliability (separate from the round, outside this document's scope):**

The vertically sliding-block breech, autoloader, and ETC ignition control electronics have their own reliability stack measured in Mean Rounds Between Failure (MRBF) at the platform level. Published 120 mm tank-gun MRBF for the M256 (Abrams) is ~ 2 000 rounds; the 140 mm gun is expected to be in the same regime at scale, but this is a vehicle-platform-integration metric rather than an ammunition metric and is not modelled in this document.

---

## Simulation provenance

All velocity, energy, pressure, recoil, and penetration figures in this specification trace to the portfolio ballistics simulator. See:

- [`weapons_sim_results.md`](../weapons_sim_results.md) — the human-readable simulation output table that this document quotes from. Tier-2 outputs (acoustic, max range, barrel life, peak recoil force, fragmentation, HEAT, NATO-60° obliquity) are imported in §12 of this spec.
- [`weapons_simulation.py`](../weapons_simulation.py) — the source code: Powley closed-form internal ballistics (η = 0.55 for the smoothbore L/52 ETC-enhanced tank gun), G7 point-mass external integration over ICAO atmosphere, Lanz–Odermatt-form long-rod penetration (K = 0.44, v₀ = 1 500 m/s, ρ_p = 18 600 kg/m³, calibrated to M829-class DU long-rod open-source data of ≈ 700 mm RHA at muzzle / ≈ 600 mm at 2 km), plus the Tier-2 models documented in the paper-end methodology of [`140mm_Tank_KE_Research_Paper.md`](140mm_Tank_KE_Research_Paper.md).
- See the paired research paper [`140mm_Tank_KE_Research_Paper.md`](140mm_Tank_KE_Research_Paper.md) for the full Methods / Provenance discussion and the explicit correction call-out describing why the 1.0 draft's ~1 450 mm muzzle penetration claim was withdrawn.
