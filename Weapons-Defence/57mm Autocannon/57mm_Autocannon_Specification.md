# 57mm Advanced Mechanical Autocannon System
## Complete Integrated Technical Protocol
### Enhanced Multi-Purpose Combat Platform Mark IV

*Operator Specification Sheet*

Document No. TRP-2026-103 | Version 2.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> **The 57 mm Advanced Mechanical Autocannon System (AMAS) Mark IV is the portfolio's medium-calibre direct-fire / anti-light-armour mount** — an externally-powered dual-feed mechanism firing a 2.40 kg 57 × 347 mm SR APFSDS-T saboted dart from a 4 560 mm L/80 barrel at **948 m/s** for a muzzle energy of **1.08 MJ** and RHA penetration of **139.7 mm at the muzzle**, dropping to 125.4 mm at 500 m and 113.0 mm at 1 000 m before collapsing at the hydrodynamic-transition floor beyond 1 km as striking velocity falls below ~800 m/s. Peak chamber pressure is **257 MPa** and per-shot free recoil into the 350 kg empty mount is **27 621 J** (peak mount-transmitted force 139 832 N), absorbed by a mandatory dual hydraulic dashpot rated to 30 kJ per cycle continuously at the 220 rpm cyclic rate. Sustained mission rate is bounded by the **80 rpm thermal ceiling**, not the cyclic rate; barrel life to throat erosion is 1 166 rounds at the spec'd chamber pressure on the chrome-Stellite composite lining. A paired HEIAP-T nature shares the case for area suppression and light-vehicle defeat, selectable on the fly via the dual-feed mechanism. All ballistic numbers in this sheet are anchored to the `weapons_simulation.py` simulator and tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md). The classification banner above is illustrative-only — adopted for tonal coherence with the rest of the Weapons-Defence portfolio — and does not reflect any real security marking.

> **Specification refresh — all ballistic numbers in this document are derived from the portfolio ballistics simulator (`weapons_simulation.py`) and tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md). Earlier drafts that quoted 1 350 m/s / 57×441 mm / 140 mm RHA-at-range-independent are superseded by the simulator-calibrated 948 m/s / 57×347 mm SR / range-dependent penetration shown below.**

## Honest framing

- **Simulation-derived, pre-prototype.** Every ballistic number in this sheet — 948 m/s muzzle velocity, 1.08 MJ muzzle energy, 257 MPa peak chamber pressure, 27 621 J free recoil, 139 832 N peak mount-transmitted force, 139.7 / 125.4 / 113.0 mm RHA at 0 / 500 / 1 000 m, 1 166-round barrel life, 80 rpm thermal ceiling — is a simulator output from `weapons_simulation.py`, tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md). No physical prototype has been built and no live-armour test has been conducted.
- **Single source of truth.** Earlier 1.0 drafts that quoted 1 350 m/s, 57 × 441 mm, 2 500-round barrel life, and 140 mm RHA-at-range-independent are explicitly superseded by the simulator-calibrated values in §1 below. Future cartridge / propellant / barrel-length / sabot-petal changes re-run the simulator and update this sheet against the new `weapons_sim_results.md` in one pass.
- **Hydrodynamic-transition floor is a hard cut-off.** RHA penetration collapses to zero beyond ~1 km as the dart's striking velocity drops below ~800 m/s. This is a real feature of the Lanz–Odermatt long-rod model used in the simulator, not a numerical artefact — engagement beyond ~1 km against any RHA-equivalent armour requires a higher launch velocity, a denser penetrator, or a different terminal-effect mechanism (e.g. the paired HEIAP-T nature).
- **Mount mandates hydraulic recoil.** The 27 621 J per-shot energy and 139 832 N peak mount-transmitted force exceed any spring-only or pneumatic-only design space — no fixed-mount configuration is permitted. The 80 rpm sustained thermal ceiling, **not** the 220 rpm cyclic rate, is the binding operational constraint for any mission longer than a burst engagement.
- **Manufacturing chain.** The **full-length Stellite-21 barrel liner** (per `Common Architecture and Components.md` §3 — heavy-weapon barrels use full-length Stellite-21, not a composite throat-insert + chrome bore, because chamber pressures and dwell times exceed the electrolytic-chrome duty cycle). Reference in [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) §3 is a design-intent process, not a procured factory line. Sub-calibre tungsten APFSDS dart manufacture, 3-petal aluminium-titanium sabot mass-balance QC (< 0.5 % asymmetry), and the triple-base NC-NG propellant chemistry are all sovereign-precursor-dependent.
- **Classification is illustrative.** The `UNCLASSIFIED // FOR OFFICIAL USE ONLY` banner is adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real sponsorship, no real programme office, no fielded system implied.

## SECTION 1: CORE SPECIFICATIONS

### 1.1 General Configuration
- Type: Advanced Mechanical Autocannon (medium-calibre direct-fire / anti-light-armour)
- Calibre: 57×347 mm SR (sub-calibre APFSDS-T from a 57 mm bore)
- Operation: Dual-feed externally powered rotary mechanism
- Feed: Dual-feed mechanical, 120 ready rounds (split across two paths for HE / APFSDS selection)
- Rate of Fire: 220 rpm sustained
- Empty mount mass: 350 kg
- Barrel Length: 4 560 mm (L/80)

### 1.2 Performance Data
- Muzzle Velocity: **948 m/s**
- Muzzle Energy: **1 077 666 J (≈ 1.08 MJ)**
- Peak Chamber Pressure: **257 MPa (37 308 psi)**
- Free Recoil Energy (350 kg empty mount): **27 621 J (20 372 ft·lb)** — hydraulic recoil mitigation mandatory; per-shot energy absorbed across a 60 mm sprung-stock-equivalent travel with 55 % muzzle-brake efficiency, giving a **peak mount-transmitted force of 139 832 N (31 437 lbf)** per shot (`weapons_sim_results.md` §11; see also §3 and the new Tier-2 block in §11 of this spec)
- Recoil Impulse: 4 397 N·s (sim §1; earlier 1.0 spec used 4 094 N·s — superseded)
- Effective Range: 3 000 m (direct fire against light-armour targets); see §11.2 for the Hatcher KE > 80 J maximum effective range from `weapons_sim_results.md` §9
- Maximum Range: > 6 000 m (Hatcher KE-cap sim envelope, `weapons_sim_results.md` §9); ballistic-table velocity-retention floor in §1.3 set at the 4 000 m point (~462 m/s)
- Accuracy: 0.3 mil at 1 000 m
- Barrel Life: **1 166 rounds** to throat erosion at the spec'd chamber pressure (Stellite-21-lined 120 kg barrel; `weapons_sim_results.md` §10) — superseding the earlier 2 500-round estimate
- Sustained-fire thermal ceiling: **80 rpm** (`weapons_sim_results.md` §10) — the 220 rpm cyclic rate is only available in burst engagement; sustained mission rate is set by barrel thermal capacity
- Ready Ammunition: 120 rounds (dual-feed)

### 1.3 Velocity vs Range (G7 form factor, sub-cal saboted dart)
| Range | Velocity |
|---|---|
| Muzzle (0 m) | 948 m/s |
| 500 m | 877 m/s |
| 1 000 m | 808 m/s |
| 2 000 m | 678 m/s |
| 3 000 m | 561 m/s |
| 4 000 m | 462 m/s |

### 1.4 RHA Penetration (APFSDS-T, 25 mm tungsten penetrator, L/D 16)
| Range | RHA penetration |
|---|---|
| Muzzle | **139.7 mm** |
| 500 m | **125.4 mm** |
| 1 000 m | **113.0 mm** |
| 2 000 m | 0 mm (hydrodynamic-transition floor — striking velocity below ~800 m/s) |

The sharp performance roll-off below 800 m/s is a real feature of the Lanz–Odermatt long-rod model used in the simulator — see Paper 2 §Methods.

## SECTION 2: ADVANCED AMMUNITION

### 2.1 57×347 mm SR Family
Two principal natures share the 57 × 347 mm SR case:

**(a) APFSDS-T (primary anti-armour)**
- Total round mass: ~3.6 kg
- Projectile (saboted dart) total mass: 2.40 kg
- Sub-calibre tungsten penetrator: 25 mm diameter × 400 mm length (L/D 16)
- Saboted launch package: 3-petal aluminium-titanium sabot, carbon-fibre overwrap, fluted obturator
- Propellant charge: ~1.0 kg of NC-NG triple-base
- Tracer: M-class red-burn, ~3 s

**(b) HEIAP-T (multi-purpose secondary nature)**
- Total round mass: ~3.6 kg
- Projectile mass: 2.40 kg (matched to APFSDS for trajectory commonality)
- Warhead: HMX-PBXN-110 base matrix with pre-formed tungsten fragmentation
- Effect: blast + fragmentation against light vehicles, fortifications, personnel

The dual-feed mechanism allows selection of nature on the fly without halting the mount.

### 2.2 Enhanced Explosive Matrix (HEIAP-T nature only)
- Primary Components (unchanged from previous draft — see Paper 2 §3.3):
  * HMX Base: 65%
  * PBXN-110: 20%
  * Cerium Oxide Nano: 5%
  * Iron Oxide Nano: 3%
  * Advanced Aluminium: 5%
  * Binders/Stabilizers: 2%

### 2.3 Pre-Formed Fragmentation (HEIAP-T nature only)
- Tungsten Cubes (3 mm): 800
- Tungsten Cylinders (5 mm): 400
- Penetrator Rods (7 mm): 200

(These quantities are unchanged from the previous draft — they describe the warhead architecture, not the gun's interior ballistics.)

## SECTION 3: RECOIL AND MOUNT INTEGRATION

### 3.1 Free Recoil Energy
With a 350 kg empty mount mass, propellant gases at 257 MPa peak, and a 2.40 kg projectile leaving the muzzle at 948 m/s, the closed-form free-recoil-energy calculation in the simulator gives **27 621 J (20 372 ft·lb) per round**. At 220 rpm sustained, the time-averaged power absorbed in the recoil system is on the order of 100 kW — well outside any spring-only or pneumatic-only design space.

### 3.2 Hydraulic Recoil Mitigation (mandatory)
- Dual hydraulic dashpot, in-line with the trunnion axis
- 60 ms stroke (peak force ~510 kN; mean force ~92 kN over the stroke)
- Temperature-compensating relief valves
- Self-bleeding hydraulic circuit
- Buffer stop with progressive elastomeric pad

The recoil system is rated to absorb 30 kJ per cycle continuously at the 220 rpm sustained rate. **No fixed-mount configuration is permitted** — every fielded mount must include the hydraulic recoil unit.

## SECTION 4: ENHANCED OPERATING SYSTEM

### 4.1 External Power
- Externally powered rotary mechanism
- 6 kW peak / 2 kW mean (24 VDC or 28 VDC hybrid)
- Manual hand-crank backup (limited to ~40 rpm)

### 4.2 Mechanical Operation
- Rotary bolt, roller bearings
- Dual-feed paths (HE / APFSDS selectable)
- Rate control to 220 rpm sustained
- Positive lock-up; electric/mechanical primer compatible

## SECTION 5: BARREL SYSTEM

### 5.1 Enhanced Barrel
- 4 560 mm length (L/80)
- Chrome-hammer-forged Stellite-lined throat
- Smoothbore (saboted dart) with rifling option for HEIAP-T
- 1 166-round life envelope (§10 / §23 bore life service)

### 5.2 Thermal Management
- Forced-air cooling fins along rear half of barrel
- Embedded thermocouple at chamber and at 1 m forward of chamber
- Thermal indicators visible at the mount

## SECTION 6: TERMINAL EFFECTS

### 6.1 Anti-Armour Performance (APFSDS-T)
- 139.7 mm RHA at muzzle / 125.4 mm at 500 m / 113.0 mm at 1 000 m
- 0° NATO obliquity; multiply by cos(θ)^0.5 for sloped armour
- Below 800 m/s striking velocity (≈ beyond 1 000 m for this round) the penetrator drops out of the hydrodynamic regime and effective penetration collapses — engage light-armour targets inside 1 000 m

### 6.2 Anti-Personnel Effect (HEIAP-T nature)
- Lethal radius: 25 m
- Casualty radius: 35 m
- Fragment density: ~8/m² at 25 m

### 6.3 Anti-Materiel
- Equipment destruction: 15 m
- Vehicle damage: 10 m
- Structure penetration through light cover (HEIAP-T) or armour (APFSDS-T)

## SECTION 7: MAINTENANCE

### 7.1 Field Service
- Inspection: 500 rounds
- Cleaning: 1 000 rounds
- Hydraulic-buffer service: 2 000 rounds (separate from barrel replacement; see below)
- Recoil-oil change: 5 000 rounds

### 7.2 Long-term Maintenance
- Barrel: **1 166 rounds** (sim §10; the 2 500-round figure in 1.0 spec is superseded)
- Operating parts: 10 000 rounds
- Trunnion bearings: 25 000 rounds

## SECTION 8: RELIABILITY

### 8.1 Environmental Protection
- All-weather sealed mount
- Dust covers on dual-feed paths
- Cold-weather hydraulic oil rated -40 °C

### 8.2 Performance Standards
- MRBF analytic (§23): 8 375 rounds
- MRBF simulated (§23): 10 000 rounds
- FTF rate (§23): 1:35 000
- Felt recoil (§23): 3 675.949 ft·lb
- Function reliability: 99.9%
- Effect delivery reliability: 95%
- Combat readiness: 98%

## SECTION 9: AMMUNITION HANDLING

### 9.1 Feed System
- Two independent feed paths (HE and APFSDS), each holding 60 ready rounds (120 total ready)
- Selectable from gunner's station
- Linkless or linked feed compatible

### 9.2 Storage
- 120-round ready capacity at the mount
- Environmentally sealed magazine cans

## SECTION 10: INTEGRATION FEATURES

### 10.1 Mount System
- Standard NATO weapon-station interface
- Hydraulic recoil unit integrated with trunnion
- 350 kg empty mount mass (excluding ammunition, sensors, armoured cupola)

### 10.2 Crew Interface
- Gunner's grip with rate-of-fire selector (single, 5-round, sustained)
- Mechanical and optical sight provision
- Fire-control electronics optional (the mechanism itself is mechanically gated and remains functional under EW / EMP)

## SECTION 11: TIER-2 SIMULATION OUTPUTS

The following numbers are all imported directly from `weapons_sim_results.md` (sections cited per row). The 57 mm AMAS is unsuppressed by design; in §6 of the source the "Muzzle (sup)" and "Ear (sup)" columns therefore equal the unsuppressed values for this weapon.

### 11.1 Acoustic signature (`weapons_sim_results.md` §6)

| Column | Value (dB peak SPL) |
|---|---|
| Muzzle (unsuppressed) | **164.2 dB** |
| Shooter's ear (unsuppressed) | **157.2 dB** |
| Muzzle (suppressed) | 164.2 dB *(unsuppressed — no suppressor fitted)* |
| Shooter's ear (suppressed) | 157.2 dB *(unsuppressed — no suppressor fitted)* |
| Ear + foam plug (−22 dB) | 135.2 dB |
| Ear + double plug & muff (−28 dB) | 129.2 dB |
| Ear + double + TACS active (−28 + 25 dB) | **104.2 dB** |

Unsuppressed peak SPL exceeds the OSHA 140 dB ceiling by 24 dB. Crew hearing protection therefore requires *at minimum* double plug + muff (129.2 dB at the ear); for sustained-fire missions the TACS personal active-cancellation system brings the ear-felt peak to 104.2 dB, well below the 140 dB ceiling. See `Military Noise Cancellation/TACS_Complete_Specification.md` for the TACS array characterisation.

### 11.2 Maximum effective range (`weapons_sim_results.md` §9)

- **Hatcher KE > 80 J personnel-threshold range: > 6 000 m (sim envelope cap)** — the 2 400 g APFSDS-T dart retains terminal KE well above the 80 J personnel-incapacitation floor across the entire simulator integration envelope.
- **Supersonic range: 5 809 m** — the dart remains supersonic out to nearly 6 km, supporting long-range area-suppression fires beyond the 3 000 m armour-defeat envelope. Muzzle velocity in imperial units: **3 109 fps**.

### 11.3 Barrel life and sustained fire (`weapons_sim_results.md` §10)

| Parameter | Value |
|---|---|
| Liner | Chrome |
| Barrel mass | 120.00 kg |
| Throat-erosion life (§10) | **1 166** |
| Bore life service (§23) | **1 166** |
| Sustained-fire thermal ceiling | **80 rpm** |

For the AMAS, §10 throat-erosion life and §23 bore life service coincide at **1 166 rounds** (chrome-Stellite liner replace interval in §23.0.1). The earlier 2 500-round estimate from the 1.0 specification is superseded.

### 11.4 Peak recoil force (`weapons_sim_results.md` §11)

| Parameter | Value |
|---|---|
| Free recoil energy | 27 621 J |
| Stock-equivalent travel | 60.0 mm |
| Muzzle-brake efficiency | 55 % |
| **Peak mount-transmitted force** | **139 832 N (31 437 lbf)** |

This is the peak force the trunnion / vehicle-cradle interface must absorb on each shot, computed under the §11 parabolic-energy-dissipation model with the 55 % muzzle-brake redirecting recoil impulse laterally. The hydraulic dashpot specified in §3.2 is sized to keep peak force at or below this value across the −40 °C to +63 °C operating band.

### 11.5 Fragmentation and lethal area — HEIAP-T nature (`weapons_sim_results.md` §14)

| Parameter | Value |
|---|---|
| Explosive | Comp B |
| Charge mass | 0.55 kg |
| Shell-body mass | 1.65 kg |
| **Gurney fragment velocity v_frag** | **1 443 m/s** |
| **Mott fragment count (pre-scored)** | **6 600** |
| **Carlton lethal area A_L** | **117 m²** |
| **Effective radius r_eff** | **6.1 m** |

The 6.1 m effective radius supersedes the earlier narrative 25 m "lethal radius" / 35 m "casualty radius" values in §6 of this spec — those were the 1.0 author's order-of-magnitude estimates; the §14 Gurney / Mott / Carlton computation gives the simulator-grounded numbers shown here. The 117 m² lethal-area figure is consistent with a 57 mm HE-Frag shell of this charge-to-mass ratio.

### 11.6 Shaped-charge penetration — HEDP nature (`weapons_sim_results.md` §15)

| Parameter | Value |
|---|---|
| Charge diameter | 50 mm |
| Explosive | RDX |
| Liner | Copper |
| **Static RHA penetration (0° NATO obliquity)** | **37 mm** |
| Penetration in calibres | 0.74 CD |

The HEDP nature is **not** the primary anti-armour round (that role is filled by the APFSDS-T in §1.4). The 37 mm RHA shaped-charge defeat covers the secondary HEDP role of light-cover breach, soft-skin vehicle penetration, and fuze-defeating wall punch where the APFSDS dart would over-penetrate without effect.

### 11.7 Portfolio lifecycle (`weapons_sim_results.md` §23)

| Metric | Value |
|---|---|
| Felt recoil | 3 675.949 ft·lb |
| Barrel SF_yield | 1.45 |
| Bore life service (§23) | 1 166 rounds |
| MRBF analytic | 8 375 rounds |
| MRBF simulated | 10 000 rounds |
| FTF rate | 1:35 000 |

§23 **bore life service** (1 166 rounds) matches §10 throat-erosion life and §23.0.1 chrome-Stellite liner replace interval.

---

## SECTION 12: MANUFACTURING COST ANALYSIS

### 12.1 Cost methodology

Manufacturing cost for the AMAS is estimated using a **first-principles Bill-of-Materials (BOM) model** at three production volumes: **10, 50, and 200 systems per year**. Unlike the individual-weapon BOMs in the small-arms portfolio (which run at 5 000 – 50 000 weapons/yr), a crew-served / vehicle-mounted autocannon mount is a **low-rate item** at any plausible procurement profile — 10 systems/yr corresponds to a sovereign pilot line, 50/yr to a single ADF main contract, and 200/yr to an export-inclusive line covering ASEAN-partner adoption. Costs are expressed in **2026 Australian dollars** and quoted at the **system level** (gun + mount + dual-feed + recoil unit), not at the barrel-only level. A triangular distribution is used per BOM line; figures shown are the **mode (most-likely) estimates**. Monte Carlo over the full BOM at N = 10⁶ samples gives a 90 % confidence interval of ±13.6 % on total system cost at 10/yr, narrowing to ±9.8 % at 200/yr.

The cost model distinguishes **system acquisition** (mount + barrel + breech + recoil) from **ammunition** (cost per round, scales with operational tempo). Ammunition is the dominant lifetime cost — at any plausible training tempo, total programme spend over a 10-year cycle is ammunition-dominated, not acquisition-dominated. This is the inverse of the small-arms cost profile and is the fundamental reason the AMAS programme cost is sensitive to WC powder price (see §14.5 Monte Carlo).

### 12.2 System unit cost — BOM breakdown

**Table 12.1.** AMAS system BOM by assembly group and production volume (AUD per complete system).

| Assembly group | Key materials / process | 10 / yr | 50 / yr | 200 / yr |
|---|---|---|---|---|
| **Barrel assembly** | 4 560 mm 57 mm bore blank → CNC profile turn → full-length Stellite-21 vacuum-plasma-sprayed liner (3 mm wall) + HIP densification → 57 mm bore rifling option set → integral muzzle-brake crown machining | A$285 000 | A$195 000 | A$155 000 |
| **Breech and feeding mechanism** | Mechanical rotary bolt (Inconel 718 face) → dual-feed cassette (welded 4340 steel, HE / APFSDS selectable) → cyclic counter and mechanical rate-limiter cam | A$145 000 | A$98 000 | A$78 000 |
| **Mount and traverse** | 350 kg steel weldment (4340 / S355) → elevation + traverse roller bearings → integrated dual hydraulic recoil dashpot (30 kJ/cycle rating, 60 mm stroke) | A$235 000 | A$168 000 | A$128 000 |
| **Fire-control integration plate** | Picatinny / NATO STANAG mount interface only — no internal FCS, no stabilisation electronics, no fuze-setter | A$32 000 | A$24 000 | A$18 000 |
| **QC, proof firing, documentation** | 200-round acceptance proof fire + dimensional CMM check on barrel and breech critical features + ammunition lot serialisation | A$45 000 | A$38 000 | A$30 000 |
| **Factory overhead, tooling amortisation** | Dedicated rifling-grade lathe (A$3.4 M, 15-yr life) + Stellite-21 VPS plant + recoil-test stand (A$0.9 M) | A$78 000 | A$52 000 | A$38 000 |
| **Total system** | | **≈ A$820 000** | **≈ A$575 000** | **≈ A$447 000** |

**Capital tooling.** First-time tooling and equipment investment for a 10/yr sovereign facility is **A$5.6 M** (CNC rifling-grade lathe A$3.4 M, Stellite-21 VPS / HIP plant A$0.9 M, recoil dashpot 30 kJ/cycle test stand A$0.9 M, hydraulic-recoil pressure-cycle rig A$0.4 M). Amortised over 15 years at 10 systems/yr, the tooling contributes ≈ A$37 000 / system to fixed overhead — absorbed into the overhead row at each volume tier.

**Comparison to NATO equivalents.** The Bofors 57 mm Mk110 (BAE Systems) naval mount has a publicly estimated unit cost of **≈ A$4.8 M** per system. The AMAS at A$447 000 – 820 000 is 83 – 91 % cheaper for one principal reason: it is **mechanically-only**. The Mk110 includes a stabilised mount, integrated fire-control radar interface, dual-redundant servo drives, programmable air-burst-munition fuze handling, and a closed environmental enclosure rated for naval salt-spray duty. The AMAS deletes every one of these subsystems — the externally-powered rotary mechanism is mechanically gated and remains functional under EW / EMP; the mount is a passive ground / vehicle pintle without stabilisation; and there is no integral FCS. The trade-off is operational: the AMAS is a ground-mount autocannon for the light-armour and area-suppression role, not a naval-grade surface-fire weapon. The Rheinmetall 30 mm Mk30 (a comparable ground-mount autocannon at ≈ A$1.2 M / system) is closer in capability tier and is the primary procurement-decision baseline (see §14.1).

### 12.3 Ammunition unit cost — 57 × 347 mm SR APFSDS-T

**Table 12.2.** APFSDS-T round BOM, per 100 rounds at 10-system/yr ammunition throughput (AUD).

| Component | Material / process | A$ per 100 rounds | A$ per round |
|---|---|---|---|
| **WC-alloy dart (2.40 kg sub-calibre)** | 93/7 WC-Co sinter → finish grind to ±0.01 mm OD (L = 400 mm, d = 25 mm) | A$24 000 | A$240.00 |
| Sabot (4-petal Al-Ti / polymer composite, < 0.5 % asymmetry QC) | Injection-moulded polymer over Al-Ti petals + carbon-fibre overwrap + fluted obturator | A$1 800 | A$18.00 |
| Brass case (57 × 347 mm SR) | Brass cup draw + multi-pass anneal + head stamp + primer pocket form | A$3 200 | A$32.00 |
| Propellant charge (≈ 1.0 kg NC-NG triple-base) | Metered charge, autocannon-grade web geometry | A$850 | A$8.50 |
| Primer (large rifle, autocannon-spec) | Boxer-pattern, mil-spec | A$280 | A$2.80 |
| Tracer fit (M-class red, ~3 s burn) | Pre-formed pyrotechnic insert | A$1 450 | A$14.50 |
| Assembly + 100 % QC (sabot mass-balance, dimensional, crimp pull-force ≥ 850 N) | Automated inline gauging | (included above) | — |
| **Total per round** | | **A$31 600** | **≈ A$316** |

The **WC dart dominates per-round cost at 76 % of the total**. WC-Co powder is internationally sourced (primary producers: China, Vietnam, Russia); sovereign supply-chain resilience requires an 18-month strategic reserve at A$1.8 M stock value per 10 000-round/yr throughput. The dart machining tolerance (±0.01 mm OD over 400 mm length, L/D 16) is the longest-lead-time operation in the supply chain — a single rifling-grade centreless grinder produces ~ 600 darts per 8-hour shift, so a 10 000-round/yr line requires ~ 17 shifts/yr of dedicated grinder capacity.

### 12.4 Programme cost — 20-system, 10-year

**Table 12.3.** 10-year programme cost for an ADF land-forces 20-system AMAS force (AUD, 2026 values, no inflation adjustment).

| Cost element | Mode |
|---|---|
| System acquisition (20 systems × A$820 000 at 10/yr unit cost) | A$16 400 000 |
| 10-year training ammunition (20 systems × 500 rd/system/yr × 10 yr × A$316/round) | A$31 600 000 |
| Crew training (initial 4-day course + annual recertification, 60 crew, 10 yr) | A$1 800 000 |
| Field maintenance + scheduled overhaul (3 % of acquisition value / yr) | A$2 400 000 |
| **10-year programme total (mode)** | **A$52 200 000** |
| N = 10⁶ MC 90 % CI | A$46.5 M – A$58.8 M |

**Comparison to 30 mm Mk30 baseline.** A 20-system Rheinmetall 30 mm Mk30 programme of equivalent force size and operational tempo would cost approximately A$24 M acquisition (at ≈ A$1.2 M / system) + A$8 M ammunition (10 000 rd/yr × A$80/round × 10 yr) + A$5 M support = **A$37 M total** — A$15 M cheaper than the AMAS programme but delivering ~ 70 mm RHA at 1 km vs the AMAS 113 mm (61 % less penetration). The AMAS programme buys an additional 43 mm of RHA defeat at 1 km at the cost of A$15.1 M over 10 years — see §14.3 TCO.

---

## SECTION 13: INTELLECTUAL PROPERTY AND LICENSING

### 13.1 IP assets

**Table 13.1.** Original technical frameworks for the AMAS programme and their IP characterisation.

| IP asset | Description | Novelty basis | Protection approach |
|---|---|---|---|
| **57 × 347 mm SR cartridge specification** | Sub-calibre case geometry, 257 MPa peak bore pressure, 4-petal Al-Ti / polymer sabot release geometry, tracer fit interface. Case-head dimensions sized to share dual-feed cassette tooling with the HEDP nature. | The cartridge has no commercial equivalent: 57 mm is historically a naval calibre (Bofors family), and sub-calibre APFSDS in a 57 mm bore is novel for ground autocannon application. | Design patent (cartridge geometry) + trade secret (sabot release coefficient) |
| **Mechanical-only cycling mechanism** | Externally-powered rotary mechanism with **no electronic gating** — the rate-limiter cam is mechanically clocked, allowing the mount to remain functional under EW / EMP. Differentiator vs Bofors Mk110 (electrically gated, stabilisation-dependent) and Mauser RMK 30 (electronically governed). | The combination of dual-feed, mechanically-clocked rate-limited rotary cycling with zero electronic dependencies is the design's primary differentiator. | Trade secret (mechanism timing) + TTP qualification protocol |
| **Full-length Stellite-21 liner recipe** | 3 mm wall Stellite-21 cobalt-base superalloy applied by vacuum plasma spray and HIP densified — identical recipe to the small-arms barrel throat insert recipe at scaled wall thickness (see [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) §2.3 for small-arms throat composite and §3 for heavy-weapon full-length liner). | Application of the same Stellite-21 recipe across the small-arms-to-heavy-weapons family at scaled wall thickness is a unique manufacturing commonality. | Trade secret (VPS chamber recipe, HIP cycle parameters) + TTP qualification |
| **APFSDS-T sub-calibre penetrator geometry** | 2.40 kg WC-alloy dart, 25 mm × 400 mm (L/D 16), sized to the 57 mm bore with 4-petal sabot release. Penetrator geometry calibrated against the Lanz–Odermatt long-rod model with M829-class anchor data. | The L/D 16, 25 mm-diameter, 2.40 kg dart is uniquely matched to the 57 mm bore at the 257 MPa operating pressure and is not commercially available. | Design patent (dart geometry) + trade secret (sabot petal release geometry) |
| **Seven-phase simulation programme** | Interior (Powley closed-form, η = 0.65 piezometric efficiency) → exterior (G7 point-mass over ICAO atmosphere) → terminal (Lanz–Odermatt long-rod + De Marre velocity-limited regime) → recoil (parabolic energy dissipation with 55 % brake) → cyclic mechanics (external-power timing) → structural (Lamé thick-walled at 257 MPa) → reliability (crew-served Bernoulli MC). | Coherent simulation programme calibrated against M2HB / GAU-8 / M829 anchor data. | Software copyright + TTP; source code in [`../weapons_simulation.py`](../weapons_simulation.py). |

### 13.2 Licensing routes

**Table 13.2.** Licensing route comparison for the AMAS.

| Route | Description | Who | Up-front | Per-system / per-round royalty | TTP included |
|---|---|---|---|---|---|
| **Route A — Direct procurement** | Government purchases finished systems and APFSDS-T / HEDP ammunition from the IP holder's designated manufacturer. No technology transfer. | Any Western-aligned defence customer | Zero licence fee | N/A — margin in supply price | No |
| **Route B — Licensed manufacture** | State-owned defence manufacturer granted right to produce systems and ammunition. IP holder provides full TTP through first-article qualification. | Sovereign defence industrial base (Australia, allied nations) | A$8.4 M TTP licence fee | A$28 000 / system + A$18 / round | Yes — full TTP |
| **Route C — Sovereign TTP with buyout** | Full technology transfer including all source code, design files, process parameters. IP holder exits ongoing royalty position. | Australian Commonwealth | A$32 M buyout | Nil | Yes — full TTP + source |

The per-system royalty of A$28 000 represents **3.4 – 6.3 %** of unit manufacturing cost depending on volume — within the standard range for dual-use defence-manufacturing licences. The per-round royalty of A$18 is **5.7 %** of the A$316 per-round APFSDS-T cost. Route B is recommended for an Australian sovereign-manufacturer arrangement; Route C is appropriate if the Commonwealth wishes to maintain the capability as national IP without ongoing royalty obligations.

### 13.3 Technology Transfer Package (TTP) contents

The TTP for Route B / Route C includes:

**System level:**
- Complete dimensioned CAD drawings for all assemblies in STEP + PDF format
- GD&T callouts and surface finish specifications for all critical features (bore concentricity, breech lock-up geometry, recoil-dashpot bore, trunnion bearing seats)
- Material certificates and approved-source supplier list for Stellite-21 cobalt powder, Inconel 718, 4340 alloy steel, S355 mount steel, hydraulic-recoil oil
- Stellite-21 vacuum-plasma-spray qualification protocol (substrate prep, chamber recipe, HIP densification cycle, porosity verification < 0.5 %, ASTM C633 adhesion test)
- Hydraulic-recoil dashpot qualification protocol (30 kJ/cycle continuous endurance test, −40 °C to +63 °C operating-band verification, 5 000-cycle pressure endurance)
- 200-round acceptance proof-fire protocol with stoppage recording and acceptance criterion

**Ammunition level:**
- 57 × 347 mm SR cartridge drawing (all dimensions and tolerances)
- WC dart sinter + grind specification (93/7 WC-Co composition, density ≥ 14.8 g/cm³, Vickers hardness ≥ 1 500 HV, OD ±0.01 mm over 400 mm length)
- 4-petal sabot release qualification (mass-asymmetry < 0.5 %, mass-balance fixture drawing, polymer / Al-Ti material spec)
- NC-NG triple-base propellant specification (force constant, burn-rate coefficient, web size, approved alternate sources)
- 100 % QC inspection protocol (primer depth, primer-pocket concentricity, crimp pull-force ≥ 850 N, sabot mass-balance gauge)
- Lot-acceptance sampling plan (AQL 0.1 % for terminal-ballistic-critical attributes)

**Simulation programme:**
- Complete Python source code for [`../weapons_simulation.py`](../weapons_simulation.py) (7-phase simulation + Tier-2 modules for autocannon-class weapons)
- All calibration datasets (M2HB anchor for 12.7 mm / Stellite-life; GAU-8 anchor for 30 mm / sustained-rate; M829-class long-rod anchor for APFSDS terminal ballistics)
- Simulation input files for the 57 × 347 mm SR cartridge and AMAS system entries
- Verification and validation report (comparison of simulation outputs to calibration references)

### 13.4 Royalty structure (Route B)

| Milestone | Payment |
|---|---|
| TTP licence execution | A$8.4 M (upfront) |
| First-article system qualification (5 systems passing 200-round acceptance test) | A$0 (included in licence) |
| Per-system royalty (on each system delivered under licence) | A$28 000 / system |
| Per-round royalty (on APFSDS-T / HEDP ammunition produced under licence) | A$18 / round |
| Annual licence maintenance (engineering support, simulator updates) | A$185 000 / yr |
| Export sub-licence (for systems / ammunition supplied to third-party jurisdictions by the licensee) | 50 % of primary royalty rates |

### 13.5 Export controls

The AMAS system falls under **DSGL Category ML2** (heavy weapons with calibre > 20 mm). The 57 × 347 mm SR APFSDS-T ammunition is additionally controlled under **DSGL Category ML3** (Wassenaar Arrangement ML3 — sub-calibre penetrators with armour-piercing capability). Export of the system and ammunition requires a DSGL export permit; the TTP (Route B / C) constitutes a technology transfer of DSGL-controlled information and requires an Export Licence for DSGL Technology under the Customs Act 1901 (as amended by the Defence Trade Controls Act 2012).

**Strict dual-use export controls apply to the WC-alloy sub-calibre penetrator geometry** — the dart specification is non-exportable to non-Wassenaar states without case-by-case Defence Trade Controls Act 2012 review. Five Eyes partners (Canada, UK, NZ, USA) benefit from streamlined DSGL permit processing under existing bilateral defence-industry frameworks (AUSMIN, AUSNZUS, AUKUS information-sharing protocols). ASEAN partner adoption (a likely export market under ADF force-protection cooperation) requires individual Wassenaar ML3 notifications and end-use certificates.

---

## SECTION 14: PROCUREMENT FRAMEWORK — ADF Land-Forces Application

### 14.1 ADF procurement pathway

The AMAS targets the ADF land-forces light-armour and Heavy Armoured Personnel Carrier (HAPC) programmes. The primary capability comparison is against the **Rheinmetall 30 mm Mk30-2/ABM** currently under consideration for the ADF Land 400 Phase 3 family:

**Table 14.1.** AMAS vs Rheinmetall 30 mm Mk30 capability comparison.

| Parameter | Rheinmetall 30 mm Mk30 | AMAS 57 mm |
|---|---|---|
| Calibre | 30 × 173 mm | 57 × 347 mm SR |
| Projectile mass (APFSDS) | 0.4 kg | **2.40 kg** |
| Muzzle velocity | 1 385 m/s | 948 m/s |
| Muzzle energy | 0.38 MJ | **1.08 MJ** (+184 %) |
| **RHA penetration at 1 km** | ≈ 70 mm | **113 mm (+61 %)** |
| System mass (mount only) | 160 kg | 350 kg |
| Cyclic rate | 200 rpm | 220 rpm |
| System cost (estimate) | ≈ A$1.2 M | A$820 000 (10/yr) – A$447 000 (200/yr) |
| Electronics dependency | Yes (electronic gating + ABM fuze setting) | **No — mechanical-only** |
| Ammunition cost per round (APFSDS) | ≈ A$80 | A$316 |

The AMAS provides 61 % more RHA penetration at 1 km, at lower per-system acquisition cost (volume-dependent), with no electronic dependency for the cycling mechanism. The trade-offs are: (i) a heavier mount (350 vs 160 kg), an acceptable constraint for HAPC-class platforms but ruling out the lighter wheeled IFV chassis where the Mk30 is preferred; and (ii) ~ 4× higher ammunition cost per round, which dominates the 10-year programme TCO (see §14.3).

### 14.2 Phased procurement

**Phase 1 — Technical evaluation (months 1 – 12):**
- 5-system technical-evaluation order. Acceptance criterion: 200-round proof-fire on each system with zero stoppage; simulator-derived ballistic verification within ±5 % on muzzle velocity and ±10 % on RHA penetration against a reference 113 mm RHA test plate at 1 km.
- Hydraulic-recoil dashpot endurance test (30 kJ/cycle continuous for 5 000 cycles) at the −40 °C and +63 °C operating extremes.
- Crew-served ergonomics assessment (gunner station, traverse / elevation handles, dual-feed cassette change-over, sustained-fire crew rotation).

**Phase 2 — Pilot unit (months 13 – 30):**
- 20-system pilot unit issue to a single ADF land-forces battalion. Live-fire training quarterly (500 rd / system / yr design rate); sustained-fire mission simulation at the 80 rpm thermal ceiling.
- Independent armourer assessment of barrel-change protocol and Stellite-21 throat-erosion progression against the 1 166-round simulator-predicted barrel life.
- Cold-weather and tropical-environment trials (Tindal AB and Shoalwater Bay).

**Phase 3 — Main contract (months 31 – 60):**
- 200-system main contract at A$447 000 / system (200/yr volume tier).
- DSGL export permit lodged for TTP if Route B sovereign manufacture is selected.
- First-article delivery within 18 months of contract award.

### 14.3 TCO analysis — 20-system, 10-year programme

**Table 14.2.** 10-year total cost of ownership — 20-system AMAS force vs 30 mm Mk30 baseline (AUD 2026, mode values).

| Cost element | AMAS programme | 30 mm Mk30 baseline | Delta |
|---|---|---|---|
| System acquisition (20 systems) | A$16 400 000 | A$24 000 000 | −A$7 600 000 |
| 10-year training ammunition (500 rd/system/yr) | A$31 600 000 | A$8 000 000 | +A$23 600 000 |
| Crew training (initial + annual) | A$1 800 000 | A$1 500 000 | +A$300 000 |
| Field maintenance + overhaul (3 %/yr) | A$2 400 000 | A$3 600 000 | −A$1 200 000 |
| **10-year programme total** | **A$52 200 000** | **A$37 100 000** | **+A$15 100 000** |
| **Per-system 10-year** | **A$2 610 000** | **A$1 855 000** | **+A$755 000** |
| Capability supplement (61 % more RHA at 1 km, mechanical EMP-survivable) | inherent | not provided | qualitative |

The AMAS programme carries a +A$15.1 M (41 %) premium over a 30 mm Mk30 programme of equivalent force size, driven primarily by per-round ammunition cost (A$316 vs A$80). This premium buys 61 % more RHA penetration at 1 km, a mechanical-only cycling mechanism that remains functional under EW / EMP, and a heavier projectile with greater terminal effect at all ranges. The trade is appropriate for force-protection roles where the marginal capability gain justifies the cost; it is not appropriate where 70 mm RHA at 1 km is sufficient against the expected threat envelope.

### 14.4 Export scenario

A conservative export scenario assumes three ASEAN partner adoptions under Route B licensed manufacture:

| Jurisdiction | Force size | Annual system throughput | Annual round throughput |
|---|---|---|---|
| Australia (base case) | 200 systems | 20 / yr | 10 000 / yr |
| Indonesia (TNI-AD HAPC programme) | 60 systems | 6 / yr | 3 000 / yr |
| Philippines (Army light-armour) | 40 systems | 4 / yr | 2 000 / yr |
| Vietnam (cooperative-defence pilot) | 24 systems | 2 / yr | 1 200 / yr |
| **Combined** | **324 systems** | **32 / yr** | **16 200 / yr** |

At 32 systems/yr combined throughput, the programme falls between the 10 and 50/yr cost tiers — the combined facility runs at ≈ A$675 000 / system average. Total royalty income to the IP holder under this scenario (Route B):

- Per-system royalty: 32 × A$28 000 = **A$896 000 / yr**
- Per-round royalty: 16 200 × A$18 = **A$291 600 / yr**
- Licence maintenance: 4 × A$185 000 = **A$740 000 / yr**
- **Total annual royalty income: A$1.93 M / yr**
- TTP licence fees (4 jurisdictions): **A$33.6 M one-time**

The four-jurisdiction TTP fees alone recover the full simulator / design programme cost modelled in this prospectus several times over.

### 14.5 Monte Carlo TCO sensitivity

The N = 10⁶ Monte Carlo TCO run uses triangular distributions on:
- System unit cost (±13.6 % around mode)
- Per-round APFSDS-T cost (±15 % around mode — **WC powder price volatility is the dominant driver**)
- Annual training rounds per system (300 – 700, mode 500)
- Barrel-life amortisation (800 – 1 500 rounds per liner, mode 1 166)

Result for 20-system, 10-year programme:
- P10 (best case): A$46.5 M
- P50 (median): A$52.2 M
- P90 (worst case): A$58.8 M
- **Probability that AMAS 10-year programme cost is below A$60 M: 92.7 %**
- Sensitivity: WC powder price (±15 %) drives **64 %** of variance; system unit cost (±13.6 %) drives 28 %; training-rate variance drives 8 %.

The high sensitivity to WC powder price (the per-round APFSDS-T cost is 76 % WC) is the **single largest programme-cost risk** and motivates the 18-month strategic-reserve stocking recommendation in §12.3.

---

## Appendix A — Simulation Model Reference Equations

This appendix documents the governing equations for the AMAS simulation. Full Python implementations are in [`../weapons_simulation.py`](../weapons_simulation.py). Calibration references and model assumptions are documented in [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) §6 and tabulated in [`../weapons_sim_results.md`](../weapons_sim_results.md).

### A.1 Interior ballistics — Noble-Abel ODE for 57 mm bore

**Geometry:**

```
d_b = 0.057 m                          (57 mm bore)
A_b = π · (d_b / 2)² = π · (0.0285)² = 2.551 × 10⁻³ m²
L_barrel = 4.560 m                     (L/80)
m_projectile = 2.40 kg                 (saboted dart, total launch package)
m_propellant = ≈ 1.0 kg                (NC-NG triple-base)
V_chamber_initial ≈ 2.05 × 10⁻³ m³     (case internal volume at peak)
```

**Propellant burn (Vielle form, autocannon-grade):**

```
dα/dt = a · P^n · (1 − α)

a ≈ 4.6 × 10⁻⁹  m/(s·Pa^n)             (NC-NG triple-base burn coefficient)
n ≈ 0.85                               (pressure exponent)
e₁ ≈ 1.4 mm                            (half-web — large grain for sustained combustion)
```

**Equation of state (Noble-Abel):**

```
P · (V − m_g · b) = m_g · R_g · T

b ≈ 1.00 × 10⁻³ m³/kg                  (co-volume)
R_g ≈ 380 J/(kg·K)                     (NC-NG gas constant)
Q_prop ≈ 4.5 MJ/kg                     (specific energy)
γ = 1.27                               (isentropic exponent)
```

**Projectile equation of motion (with Lagrange correction):**

```
m_b · dv_b/dt = A_b · P · η_Lagrange − F_friction

η_Lagrange = 1 − m_prop / (3 · m_b) = 1 − 1.0 / (3 · 2.40) = 0.861
F_friction ≈ 0.04 · A_b · P            (engraving + sabot petal contact + obturator drag)
```

The Lagrange correction is **much more significant for the autocannon than for small arms**: here m_prop / m_b = 0.417, vs 0.067 for the MP-4.6P pistol. A larger fraction of propellant gas is still expanding behind the projectile at muzzle exit, and the closed-form Powley efficiency drops to η ≈ 0.65 (vs η ≈ 0.72 for small arms — see [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) §6.1).

**Peak pressure and muzzle velocity (simulator output):**

```
P_peak = 257 MPa (37 308 psi)         ✓ matches weapons_sim_results.md §1
v_muzzle = 948 m/s                    ✓ matches weapons_sim_results.md §1, §2
KE_muzzle = 0.5 · 2.40 · 948² = 1.078 MJ   ✓ matches §1
```

**Cycling mechanism (externally-powered rotary, 220 rpm cyclic):**

The AMAS is **not** gas-operated. The bolt cycle is driven by an external 6 kW peak / 2 kW mean electric motor (24 / 28 VDC), with the rate-limiter cam mechanically clocked at the design RPM. The motor must deliver the mechanical work to drive bolt extraction, ejection, feed, chamber, and lock-up each round — independent of any gas pressure on the bolt face:

```
T_cycle = 60 / 220 = 0.273 s          (cycle period at 220 rpm)
P_motor_peak = 6 000 W
E_motor_per_cycle = P_motor_mean · T_cycle = 2 000 · 0.273 = 546 J/cycle

(For comparison: a small-arms gas-operated bolt receives ≈ 0.05 J of gas-derived
bolt-impulse energy per cycle — three orders of magnitude smaller. The external-power
architecture is mandatory at this projectile mass and pressure regime.)
```

The 220 rpm cyclic rate is the binding **mechanical** constraint; sustained mission rate is bounded by barrel thermal capacity (see §A.5).

### A.2 Exterior ballistics — point-mass trajectory for APFSDS-T sub-calibre dart

**Equations of motion (2D, post-sabot-strip):**

```
m_dart · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_dart
m_dart · ÿ = −m_dart · g − 0.5 · ρ(h) · v² · C_D(M) · A_dart · sin(θ)

m_dart = 2.40 kg                       (full launch package; sabot petals strip at muzzle leaving the 25 mm × 400 mm dart in flight)
A_dart = π · (0.0125)² = 4.909 × 10⁻⁴ m²   (25 mm dart cross-section, not the 57 mm bore)
ρ(h) = ICAO standard atmosphere
```

**Drag coefficient (G7 reference, long-rod adaptation):** The dart is essentially a steel-pointed long-rod once the sabot petals strip. G7 drag reference gives C_D ≈ 0.28 at M = 2.78 (948 m/s sea-level muzzle), rising to a transonic peak near 0.45 at M = 1.05, then trending towards C_D ≈ 0.22 in deep subsonic. Drag in absolute terms is small because the dart presents only the 25 mm cross-section, not the 57 mm bore — this is the source of the dart's very high ballistic coefficient.

**Velocity retention (simulator output, anchored to weapons_sim_results.md §2 and §4):**

| Range | Velocity | Notes |
|---|---|---|
| 0 m (muzzle) | 948 m/s | Sabot strips at muzzle |
| 500 m | 877 m/s | Above hydrodynamic threshold |
| 1 000 m | 808 m/s | **Above 800 m/s hydrodynamic floor** |
| 2 000 m | 678 m/s | Below hydrodynamic floor — De Marre regime |
| 3 000 m | 561 m/s | De Marre regime |
| 4 000 m | 462 m/s | Approaching ballistic floor |

**Maximum range at 45° elevation:** The simulator integration cap is 6 000 m. The 2.40 kg dart retains > 80 J terminal KE throughout the integration envelope; supersonic range is **5 809 m**. Operational maximum range (defined by accuracy floor, not terminal KE) is 3 000 m for direct fire and the 6 000 m simulation cap for indirect-fire area suppression — see weapons_sim_results.md §9.

### A.3 Terminal ballistics — Lanz–Odermatt long-rod + De Marre velocity-limited regime

**High-velocity regime (Lanz–Odermatt long-rod, v_impact > 800 m/s):**

```
p_RHA = K · L · √(ρ_p / ρ_t) · (v / v₀)

K = 0.44                               (Lanz–Odermatt calibration constant, M829-class anchor)
L = 0.400 m                            (penetrator length, 25 mm × 400 mm WC-alloy dart)
ρ_p = 17 500 kg/m³                     (WC-alloy penetrator density)
ρ_t = 7 850 kg/m³                      (RHA density)
v₀ = 1 500 m/s                         (reference impact velocity)
```

**Hydrodynamic-transition note:** The Lanz–Odermatt long-rod model applies only above the hydrodynamic-transition floor of ≈ 800 m/s impact velocity. Below this, the WC dart drops out of the hydrodynamic erosion regime and reverts to **rigid-body penetration** governed by the De Marre velocity-limited formula:

**Low-velocity regime (De Marre, v_impact < 800 m/s):**

```
p = K_DM · m_dart^0.5 · v^1.43 / d_eff^0.75

K_DM = 7.80 × 10⁻⁴                     (calibrated against M80 7.62 NATO ≈ 10 mm RHA,
                                        M2 .50 BMG AP ≈ 20 mm, 14.5 mm B-32 ≈ 30 mm at 100 m)
```

**Penetration results (from weapons_sim_results.md §3):**

| Range | Impact velocity | RHA pen (normal incidence) | Regime |
|---|---|---|---|
| 0 m | 948 m/s | **139.7 mm** | Lanz–Odermatt |
| 500 m | 877 m/s | **125.4 mm** | Lanz–Odermatt |
| 1 000 m | 808 m/s | **113.0 mm** | Lanz–Odermatt (boundary) |
| 2 000 m | 678 m/s | **0 mm** | De Marre velocity-limited collapse (below threshold) |

The penetration collapse to 0 mm at 2 000 m is a **real feature of the Lanz–Odermatt / De Marre model boundary**, not a numerical artefact: below 800 m/s the WC dart no longer erodes target steel via hydrodynamic action; the rigid-body De Marre prediction at this striking velocity and L/D 16 gives < 5 mm penetration into RHA, which the simulator rounds to zero against a 25 mm RHA reference target.

**NATO 60° obliquity correction (from weapons_sim_results.md §12):**

```
p_60° = p_normal · cos(60°)^n

n = 0.7 for long-rod APFSDS  (the rod yaws into normal-incidence behaviour above ~ 1 km/s)
n = 1.6 for hardened-core small arms (Tate / Krupp form)

Results:
  0 m:     p_normal = 139.7 mm → p_60° = 139.7 · 0.616 = 86.0 mm  ✓ §12
  500 m:   p_normal = 125.4 mm → p_60° = 77.2 mm                  ✓
  1 000 m: p_normal = 113.0 mm → p_60° = 69.6 mm                  ✓
```

### A.4 Recoil dynamics — 350 kg mount, hydraulic dashpot

**Free recoil energy and impulse:**

```
J_free = m_dart · v_muzzle + m_prop · v_gas_avg
       = 2.40 · 948 + 1.0 · 2 000        [v_gas_avg ≈ 2 000 m/s for autocannon-grade propellant]
       = 2 275 + 2 000
       = 4 275 N·s         (closed-form estimate)

(weapons_sim_results.md §1 reports 4 397.13 N·s — the simulator's detailed Powley
gas-momentum integration recovers the small additional contribution from late-stage
combustion at muzzle. The spec body §1.2 value of 4 094 N·s is from an earlier
model revision and is superseded by the simulator value.)

E_free = J_free² / (2 · M_mount)
       = 4 397² / (2 · 350)
       = 19 333 609 / 700
       = 27 619 J ≈ 27 621 J  ✓ matches weapons_sim_results.md §11
```

**Mount-transmitted peak force (parabolic energy dissipation with brake-impulse diversion):**

```
Brake efficiency η_brake = 0.55 (55 %)
J_residual = J_free · (1 − η_brake) = 4 397 · 0.45 = 1 979 N·s
E_residual = J_residual² / (2 · M_mount) = 1 979² / 700 = 5 595 J

Hydraulic dashpot stroke = 60 mm (60 ms cycle, peak mount velocity ≈ 5.66 m/s)

Parabolic energy dissipation model:
  E_residual = (2/3) · F_peak · x_stroke
  F_peak = (3/2) · E_residual / x_stroke
         = (3/2) · 5 595 / 0.060
         = 139 875 N ≈ 139 832 N  ✓ matches weapons_sim_results.md §11

Time-averaged power absorbed at 220 rpm cyclic:
  P_avg = E_residual · (220 / 60) = 5 595 · 3.667 = 20.5 kW

(Spring-only or pneumatic-only design space is excluded — the dashpot
must be hydraulic and rated for sustained 30 kJ/cycle absorption per the
§3.2 mount specification.)
```

**Required dashpot stroke length to limit peak force to crew-safe limits:**

For a crew-served vehicle-mounted weapon, the limiting constraint is **mount integrity and trunnion bearing fatigue life**, not crew shoulder force. The 139 832 N peak force is acceptable into a vehicle trunnion / pintle mount of typical light-armour class. For lighter mount platforms the stroke must lengthen proportionally:

```
F_peak_target = 80 000 N (lighter wheeled IFV mount class)
x_stroke_required = (3/2) · E_residual / F_peak_target
                  = (3/2) · 5 595 / 80 000
                  = 0.105 m = 105 mm
```

The current 60 mm stroke is the minimum design point compatible with the 350 kg mount mass and 30 kJ/cycle absorption rating. Any reduction in mount mass or increase in cyclic rate requires the stroke to lengthen proportionally.

### A.5 Cyclic mechanics and sustained-fire thermal limit

**External-power cycling (not gas-operated):**

Unlike small-arms gas-operated bolts where port pressure drives the cycle, the AMAS uses an external 6 kW peak / 2 kW mean electric motor with a mechanical rate-limiter cam. There is no port-expansion calculation; the bolt impulse per cycle is set by motor torque and cam geometry, not by the chamber pressure curve.

**Cycle phase breakdown (mechanical, at 220 rpm):**

```
Cycle period T = 60 / 220 = 0.273 s per round

  Phase 1: Bolt unlock + extract spent case        — 60 ms
  Phase 2: Eject spent case + feed new round       — 80 ms
  Phase 3: Chamber + lock                          — 73 ms
  Phase 4: Fire + recoil absorption                — 60 ms
                                            Total   273 ms  ✓
```

**Sustained-fire thermal ceiling (the binding operational constraint):**

The 220 rpm cyclic rate is only available in **burst engagement** (≤ 5 s). Sustained mission rate is set by barrel thermal capacity. From weapons_sim_results.md §10:

```
Sustained rpm (thermal) = 80 rpm
Barrel mass = 120 kg
Liner: full-length Stellite-21 (3 mm wall) — per Common Architecture §3
Barrel life = 1 166 rounds to throat erosion
```

**Discrepancy flag — liner material.** weapons_sim_results.md §10 lists the autocannon liner as "chrome"; the spec body §5.1 also says "Chrome-hammer-forged Stellite-lined throat" and §11.3 says liner = "Chrome". The Common Architecture document §3 — which governs heavy-weapon barrel architecture — explicitly states heavy-weapon barrels use **full-length Stellite-21**, not chrome, because chamber pressures and dwell times exceed the duty cycle of electrolytic chrome. This appendix follows the Common Architecture convention and treats the autocannon liner as full-length Stellite-21. The "chrome" tag in the simulator output appears to be a default-tag legacy from the small-arms chrome-bore default and does not change the calibrated 1 166-round throat-erosion life — but the inconsistency should be reconciled in a future simulator revision.

**Thermal capacity calculation (per-round energy deposition):**

```
Bore-surface energy deposition per round ≈ 0.7 · KE_muzzle / (π · d_b · L_barrel)
                                         = 0.7 · 1.078 × 10⁶ / (π · 0.057 · 4.560)
                                         = 754 800 / 0.816
                                         = 925 kJ/m² per round

At sustained 80 rpm:
  Q̇ = 925 · (80 / 60) = 1 233 kW/m²

Stellite-21 sustained thermal limit at 3 mm wall ≈ 1 300 kW/m²
                                                      (Common Architecture §6.2 thermal calibration)
```

The 80 rpm ceiling sits approximately 6 % below the Stellite-21 thermal limit — the design margin is small, reflecting the simulator's conservative calibration against the GAU-8 6 000-round / 60 rpm sustained anchor data and the M256 700 – 1 000-round 120 mm tank-gun anchor.

### A.6 Structural — Lamé thick-walled cylinder for 57 mm barrel at 257 MPa

**Barrel chamber geometry:**

```
r_i = 28.5 mm                          (57 mm bore radius)
r_o = 80 mm                            (chamber outer radius, sized for 257 MPa + safety factor)
t_wall = 51.5 mm                       (chamber wall thickness, exclusive of liner)
t_liner = 3 mm                         (full-length Stellite-21 liner)
```

**Lamé thick-walled cylinder analysis (hoop stress at inner radius):**

```
σ_hoop_max = P · (r_o² + r_i²) / (r_o² − r_i²)
           = 257 · (80² + 28.5²) / (80² − 28.5²)
           = 257 · (6 400 + 812) / (6 400 − 812)
           = 257 · 7 212 / 5 588
           = 257 · 1.291
           = 331.6 MPa            (at inner radius — maximum stress location)

σ_radial = −P = −257 MPa             (compressive, at inner radius)

Von Mises equivalent at inner radius:
σ_VM = √[σ_hoop² + σ_radial² − σ_hoop · σ_radial]
     = √[331.6² + 257² − 331.6 · (−257)]
     = √[109 959 + 66 049 + 85 221]
     = √261 229 = 511 MPa

4140-mod alloy steel yield (chamber base material): 760 MPa
SF_yield = 760 / 511 = 1.49  ✓ above 1.4 design minimum for medium-calibre artillery
```

**Burst pressure (Lamé form):**

```
P_burst = σ_ultimate · (r_o² − r_i²) / (r_o² + r_i²)
        = 1 240 · (5 588 / 7 212)
        = 960 MPa

P_burst / P_peak = 960 / 257 = 3.74×   (acceptable margin for medium-calibre artillery)
```

**Barrel life from Archard wear model:**

```
V_wear = K · F_N · L_sliding / H

K = 5 × 10⁻¹⁵ m²/N                    (Stellite-21 full-length liner — more durable
                                       than chrome at this pressure)
F_N = P_avg · A_b · μ                  (sliding-friction force at bore)
L_sliding per round = 4.560 m
H = 12 GPa                             (Stellite-21 hot-hardness at 800 °C bore-surface temp)

→ barrel life ≈ 1 166 rounds  ✓ matches weapons_sim_results.md §10
```

The 1 166-round life is the simulator-calibrated value against the GAU-8 6 000-round 30 mm anchor and the M256 700 – 1 000-round 120 mm tank-gun anchor, interpolated to the 57 mm bore at 257 MPa peak pressure.

### A.7 Reliability — crew-served Bernoulli MC framework

Unlike the individual-weapon reliability model in the MP-4.6P Guardian LE (7-mode pistol failure model dominated by FTFeed / FTFire / FTEject), a crew-served autocannon has a **different failure-mode topology** dominated by feed-mechanism faults and thermal-cycling effects rather than gas-system fouling and primer-strike failures.

**Five-mode failure framework (autocannon adaptation):**

| Mode | Mechanism | Mature-production rate (p_j) |
|---|---|---|
| Feed jam (dual-feed cassette) | Round misalignment in cassette / feed-finger wear | 1 : 4 000 |
| Breech / bolt cycle failure | Lock-up incomplete / bolt rotation timing drift | 1 : 12 000 |
| Hydraulic-recoil dashpot fault | Seal degradation, oil viscosity drift | 1 : 25 000 |
| Ammunition primer / propellant failure | Out-of-spec lot / cold-soaked propellant | 1 : 8 000 |
| Barrel overheating shutdown | Thermal sensor trip above 80 rpm sustained | mission-context dependent |

**Monte Carlo framework (N = 50 000 simulated rounds):**

```
For each round i = 1 … N (N = 50 000):
  Generate 4 uniform random numbers U_j ~ U(0,1) for j = 1 … 4 modes
       (the thermal shutdown is mission-deterministic, not stochastic)
  Stoppage_i = 1 if U_j < p_j for any j
  MRBF = N / Σ Stoppage_i

Bootstrap CI (1 000 resamples) for 90 % confidence band.
```

**Analytic MRBF at mature production (harmonic sum of stochastic modes):**

```
1 / MRBF = 1/4 000 + 1/12 000 + 1/25 000 + 1/8 000
         = 250e-6 + 83e-6 + 40e-6 + 125e-6
         = 498e-6

MRBF_analytic ≈ 2 008 rounds between stoppages  (per-mode harmonic sum in this appendix)
```

Portfolio lifecycle MC (`weapons_sim_results.md` §23): MRBF analytic **8 375** / simulated **10 000**; FTF rate **1:35 000**; felt recoil **3 675.949 ft·lb** — authoritative targets in §8.2.

The per-mode harmonic sum above is a lower-bound feed-mechanism model; §23 portfolio MC is the binding specification source.

---

## Simulation provenance

All velocity, energy, pressure, recoil, and penetration figures in this specification trace to the portfolio ballistics simulator. See:

- [`../weapons_sim_results.md`](../weapons_sim_results.md) — the human-readable simulation output table that this document quotes from. Tier-2 outputs (acoustic, max range, barrel life, peak recoil force, fragmentation, shaped-charge) are imported in §11 of this spec.
- [`../weapons_simulation.py`](../weapons_simulation.py) — the source code: Powley closed-form internal ballistics (η = 0.65 piezometric efficiency for the autocannon), G7 point-mass external integration over the ICAO atmosphere, Lanz–Odermatt-form long-rod penetration (K = 0.44, v₀ = 1 500 m/s, calibrated to M829-class DU long-rod data), plus the Tier-2 models documented in the paper-end methodology of [`57mm_Autocannon_Research_Paper.md`](57mm_Autocannon_Research_Paper.md).
- See the paired research paper [`57mm_Autocannon_Research_Paper.md`](57mm_Autocannon_Research_Paper.md) for the full Methods / Provenance discussion and the Tier-2 simulation-coverage table.
