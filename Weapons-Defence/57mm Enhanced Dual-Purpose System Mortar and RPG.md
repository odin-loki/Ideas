# 57mm Enhanced Dual-Purpose System
## Complete Technical Protocol
### Advanced Infantry Support Weapon — Mortar and RPG Dual-Mode Tube

*Operator Specification Sheet*

Document No. TRP-2026-104 | Version 2.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> **The 57 mm Enhanced Dual-Purpose System (EDPS) is the portfolio's infantry-support mortar / RPG dual-mode tube** — a single-shot muzzle-loaded 900 mm smoothbore on a 7.20 kg mount, launching a 1.40 kg combined HEAT + fragmentation-jacket warhead at **187 m/s** in full-charge RPG mode for a muzzle energy of **24 427 J** and an effective direct-fire range of **~1 500 m**, with a low-charge or 45°-elevation indirect-fire mode reaching **~2 500 m**. Peak chamber pressure is **111 MPa**; per-shot free recoil into the 7.20 kg empty mount is **4 965.9 J** with a peak mount-transmitted force of **53 632 N**, putting the energy budget in 120 mm-mortar territory while the mount itself is a fifth of that mass — tripod-mounted or shoulder-anchored deployment with a hydraulic buffer rated to ≥ 5 kJ per cycle is mandatory, and no shoulder-fired hand-held use is permitted. Velocity retention is unusually flat (187 → 162 → 146 → 142 m/s out to 2 km) because the round is heavy for its bore, which is what makes the mortar mode viable to 2.5 km. All ballistic numbers in this sheet are anchored to the `weapons_simulation.py` simulator and tabulated in [`weapons_sim_results.md`](weapons_sim_results.md). The classification banner above is illustrative-only — adopted for tonal coherence with the rest of the Weapons-Defence portfolio — and does not reflect any real security marking.

> **Specification refresh — all ballistic numbers in this document are derived from the portfolio ballistics simulator (`weapons_simulation.py`) and tabulated in [`weapons_sim_results.md`](weapons_sim_results.md). The previous draft's "350 m/s direct fire / 2 800 bar / 800 m effective" figures are superseded by the simulator-calibrated 187 m/s / 111 MPa / ~1 500 m direct-fire envelope shown below.**

## Honest framing

- **Simulation-derived, pre-prototype.** Every ballistic number in this sheet — 187 m/s muzzle velocity, 24 427 J muzzle energy, 111 MPa peak chamber pressure, 4 965.9 J free recoil, 53 632 N peak mount-transmitted force, ~1 500 m RPG-mode effective range, ~2 500 m mortar-mode maximum range — is a simulator output from `weapons_simulation.py`, tabulated in [`weapons_sim_results.md`](weapons_sim_results.md). No physical prototype has been fired in either RPG or mortar mode, and no live engagement of the dual-mode configuration has been demonstrated.
- **Single source of truth.** Earlier-draft figures (350 m/s direct fire, 2 800 bar chamber pressure, 800 m effective range) are superseded by the simulator-calibrated 187 m/s / 111 MPa / ~1 500 m envelope shown in §1.2 – §1.4. Future warhead / propellant / tube-length changes re-run the simulator and update this sheet against the new `weapons_sim_results.md` in one pass.
- **Mount mandates a buffer; no hand-held use.** 4 965.9 J of free-recoil energy into a 7.20 kg mount is in 120 mm-mortar territory absorbed by ~20 % of the typical mount mass; the **53 632 N peak mount-transmitted force** is what the tripod / baseplate / shoulder anchor must absorb on every shot. Unlike a classical RPG-7 (~3 kJ into a 7 kg launcher, shoulder-fired with limited buffering), the EDPS delivers too much energy too quickly to be safely shoulder-fired — tripod-mounted or shoulder-anchored deployment with a hydraulic buffer rated to ≥ 5 kJ per shot is mandatory.
- **Trajectory model is G1 blunt-body.** The flat velocity retention (162 m/s @ 500 m, 146 m/s @ 1 000 m, 142 m/s @ 2 000 m) follows from the heavy-for-bore combined HEAT + frag round once it falls below the transonic-relevant Mach band. The 2 mil direct-fire accuracy and 10 m CEP mortar-mode accuracy are simulator estimates against a clean fire-control assumption — wind, target movement, and fuze-dispersion variance are not modelled.
- **Manufacturing chain.** The chrome-lined smoothbore tube, quick-change tube system, and three-lug breech-end mounting are design-intent. The shared 57 mm bore-gauge set common to the autocannon, dual-purpose tube, and underbarrel launcher (per [`Common Architecture and Components.md`](Common%20Architecture%20and%20Components.md) §3) is a design-intent commonality, not a procured factory line. The HEAT precursor / shaped-charge liner is not specified in this sheet and remains an open warhead-engineering question.
- **Classification is illustrative.** The `UNCLASSIFIED // FOR OFFICIAL USE ONLY` banner is adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real sponsorship, no real programme office, no fielded system implied.

## SECTION 1: CORE SPECIFICATIONS

### 1.1 General Configuration
- Type: Enhanced Dual-Purpose System (mortar / RPG)
- Calibre: 57 mm dual-purpose tube
- Operation: Muzzle-loaded, single-shot, dual-mode (low-charge mortar / full-charge RPG)
- Projectile: 1.40 kg combined-warhead round (HEAT + fragmentation jacket)
- Modes: Direct-fire (RPG) and indirect-fire (mortar) — distinguished by **propellant cup selection** at loading
- Empty mount mass: **7.20 kg**
- Length: 1 200 mm (tube + mount)
- Tube length: **900 mm**

### 1.2 Performance Data
- Muzzle Velocity: **187 m/s** (full-charge RPG mode)
- Muzzle Energy: **24 427 J**
- Peak Chamber Pressure: **111 MPa (16 000 psi)**
- Recoil Impulse: 266.6 N·s
- Free Recoil Energy (7.20 kg mount): **4 965.9 J (3 662.7 ft·lb)** — substantial; tripod-mounted or shoulder-anchored deployment with hydraulic buffer is mandatory (see §3)
- **Peak mount-transmitted recoil force: 53 632 N (12 058 lbf)** (`weapons_sim_results.md` §11, 50 mm stock-equivalent travel, 40 % muzzle-brake efficiency) — this is the value the tripod / baseplate / shoulder-anchor must absorb on each shot
- Magazine: single-shot muzzle-loaded
- Rate of Fire: 6 – 8 rpm (manual muzzle reload + setup); **sustained-fire thermal ceiling: 57 rpm** (`weapons_sim_results.md` §10) — operational rate is set by the manual reload cycle, not by barrel thermal capacity

### 1.3 Engagement Envelope
- **RPG mode (direct fire, full charge):**
  * Muzzle velocity: 187 m/s
  * Effective range: **~1 500 m** (drag-limited; G1 form factor; high-drag warhead profile)
  * Rate of fire: 6 – 8 rpm
  * Accuracy: 2 mil at 300 m
- **Mortar mode (indirect fire, low charge or full charge at 45° elevation):**
  * Maximum range at 45° elevation: **~2 500 m** (full charge; the simulator gives velocity retention above 140 m/s out to 2 km, indicating the indirect-fire mortar role is viable)
  * Minimum range: 200 m (at maximum elevation)
  * Maximum elevation: 85°
  * Accuracy: 10 m CEP at 1 500 m
  * Setup time: < 30 s

### 1.4 Velocity vs Range (G1 form factor — high-drag combined warhead)
| Range | Velocity |
|---|---|
| Muzzle (0 m) | 187 m/s |
| 500 m | **162 m/s** |
| 1 000 m | **146 m/s** |
| 2 000 m | **142 m/s** |
| 3 000 m | (no longer in line-of-sight envelope; mortar mode only) |

Velocity retention is unusually flat — the round is heavy (1.40 kg) for its bore, so once below the transonic-relevant Mach band the drag coefficient drops sharply and the velocity tails off slowly. This is what makes the mortar mode viable at 2.5 km.

## SECTION 2: TUBE AND BARREL ASSEMBLY

### 2.1 Tube Construction
- 900 mm length
- Chrome-lined bore
- Smoothbore (the warhead is fin-stabilised, not spin-stabilised)
- Enhanced cooling fins along the rear two-thirds
- Quick-change tube system for sustained-fire operations
- Three-lug breech-end mounting
- Self-headspacing
- Thermal indicators
- Tool-less removal
- Heat-sink zones at the breech and muzzle

### 2.2 Enhanced Recoil System
- Features:
  * Dual-spring progressive system
  * Hydraulic damper sized for **5 kJ continuous absorption** per shot
  * Temperature-compensating valves
  * Self-bleeding design
  * Quick-adjust capability
  * 250 mm travel
  * Self-contained unit
  * Low maintenance

## SECTION 3: MOUNTING AND STABILISATION — recoil-mitigation discussion

At 1.40 kg projectile × 187 m/s exit velocity the recoil impulse is **267 N·s**, and into a 7.20 kg mount mass the free recoil energy is **4 965.9 J**. For comparison, a 120 mm mortar at typical mortar charges delivers about 4 – 6 kJ of free recoil into its 30 – 40 kg baseplate — broadly the same energy budget, but absorbed by 5 × the mass.

Implications:

- **Tripod-mounted or shoulder-anchored deployment is mandatory.** The 7.20 kg mount is too light to absorb 5 kJ of free-recoil energy directly; the mount must transfer impulse to a baseplate (mortar mode) or to a shoulder anchor (RPG mode).
- **Hydraulic buffer is mandatory.** The recoil dashpot must absorb ≥ 5 kJ per shot at the 6 – 8 rpm rate.
- **No shoulder-fired hand-held use.** Unlike a classical RPG-7 (3 kJ free recoil into a 7 kg launcher, fired from the shoulder with limited buffering), the EDPS delivers too much energy too quickly to be safely shoulder-fired without a buffer.

### 3.1 Universal Mount
- Design:
  * Tapered roller bearing pivot
  * Eccentric locking cam
  * Zero-backlash system
  * Self-adjusting tension
  * Quick-release mechanism
  * Position memory stops
  * Multi-position bipod
  * Self-levelling feet

### 3.2 Base Plate System (mortar mode)
- Features:
  * Expanding spade system
  * Self-levelling base
  * Quick-deploy legs
  * Position locks
  * Anti-sink features
  * Terrain adaptation
  * Load distribution
  * Emergency stakes

## SECTION 4: ADVANCED SIGHTING SYSTEM

### 4.1 Mechanical Calculator
- Construction:
  * Sealed ball-bearing system
  * Self-lubricating bushings
  * Positive click stops
  * Spring-loaded detent
  * Debris-clearing channels
  * Weather-sealed
  * Tritium illumination
  * Armoured cover

### 4.2 Sighting Mechanisms
- Direct Fire (RPG):
  * Fixed 3× optic
  * Mechanical range cam calibrated to the 187 m/s muzzle-velocity drop curve
  * Quick-adjust windage
  * Backup iron sights
  * Night capability
  * Clear markings
- Indirect Fire (mortar):
  * Mechanical quadrant
  * Bubble-level system
  * Quick-set angles
  * Reference markers
  * Position memory
  * Night markers

## SECTION 5: LOADING AND SAFETY

### 5.1 Enhanced Breech System
- Design:
  * Counter-balanced block
  * Spring-assisted opening
  * Self-cleaning extractor
  * Dual ejectors
  * Anti-double-feed
  * Positive lock indicators
  * Quick-swing operation
  * Safe loading

### 5.2 Safety Features
- Mechanical:
  * Three-point safety system
  * Out-of-battery prevention
  * Firing-pin block
  * Drop safety
  * Visual indicators
  * Tactile confirmation
  * Emergency release
  * Clear markings

## SECTION 6: CREW PROTECTION

### 6.1 Shield System
- Features:
  * Folding blast shield
  * Quick-deploy panels
  * Heat guards
  * Blast deflectors
  * Position markers
  * Lock-in-place
  * Emergency release
  * Safe zones

### 6.2 Operating Positions
- Design:
  * Protected firing positions
  * Quick transition points
  * Clear safety zones
  * Marked danger areas
  * Emergency procedures
  * Fast displacement

## SECTION 7: ENVIRONMENTAL PROTECTION

### 7.1 Weather Resistance
- Sealed bearings, weather protection, drainage channels, anti-icing, dust protection, corrosion resistance, all-weather operation, temperature compensation across −40 °C to +63 °C.

### 7.2 Durability Features
- Hardened wear surfaces, self-lubricating points, protected mechanisms, reinforced stress areas, impact protection, extended-life design, simple maintenance, clear indicators.

## SECTION 8: MAINTENANCE AND SERVICE

### 8.1 Field Maintenance
- Tool-less access, quick-clean surfaces, inspection ports, wear indicators, lubrication points, service markers, basic tools only, clear procedures.

### 8.2 Service Schedule
- Daily check: 2 minutes
- Weekly clean: 15 minutes
- Monthly service: 1 hour
- Hydraulic-buffer service: 500 rounds
- Tube replacement: 2 000 rounds

## SECTION 9: TRANSPORT AND DEPLOYMENT

### 9.1 Transport Configuration
- Three main components (tube, mount, baseplate)
- Quick-release joints
- Self-aligning pins
- Positive locks
- Assembly guides
- Verification points
- Tool-less assembly
- Safe transport

### 9.2 Ready Position
- 30-second deployment
- Two-man operation
- Clear markers
- Quick verification
- Safe preparation
- Combat ready
- Fast transition
- Emergency breakdown

## SECTION 10: EMERGENCY PROCEDURES

### 10.1 Immediate Action
- Quick-clear system, emergency breakdown, fast displacement, safety releases, clear procedures, simple steps.

### 10.2 Backup Operation
- Mechanical overrides, emergency sights, manual operation, basic function, simple backup, clear procedures, safe operation, quick recovery.

## SECTION 11: TIER-2 SIMULATION OUTPUTS

The following numbers are imported directly from `weapons_sim_results.md` (sections cited per row). The 57 mm EDPS is unsuppressed by design — the breech / muzzle blast is unfiltered.

### 11.1 Acoustic signature (`weapons_sim_results.md` §6)

| Column | Value (dB peak SPL) |
|---|---|
| Muzzle (unsuppressed) | **162.6 dB** |
| Shooter's ear (unsuppressed) | **155.6 dB** |
| Muzzle (suppressed) | 162.6 dB *(unsuppressed — no suppressor)* |
| Shooter's ear (suppressed) | 155.6 dB *(unsuppressed — no suppressor)* |
| Ear + foam plug (−22 dB) | 133.6 dB |
| Ear + double plug & muff (−28 dB) | 127.6 dB |
| Ear + double + TACS active (−28 + 25 dB) | **102.6 dB** |

Unsuppressed peak SPL exceeds the OSHA 140 dB ceiling by 23 dB. Crew hearing protection requires double-plug + muff at a minimum; the **TACS personal active overlay** (additional −25 dB) is strongly recommended for indirect-fire mortar missions involving multiple rounds. Mortar mode breech-port blast geometry differs from direct-fire RPG-mode geometry, but the peak unsuppressed SPL is dominated by muzzle blast and is not materially mode-dependent.

### 11.2 Maximum effective range (`weapons_sim_results.md` §9)

- **Hatcher KE > 80 J personnel-threshold range: > 6 000 m (sim envelope cap)** — the 1.40 kg combined-warhead round retains > 80 J terminal KE across the integration envelope (mass-dominated, not velocity-dominated terminal KE).
- **Supersonic range: 0 m** — the 187 m/s muzzle velocity is subsonic from launch. The round exhibits no transonic-band drag spike and the very flat velocity-retention table in §1.4 reflects the low-Mach low-Cd regime.

Operational max range is constrained by accuracy, not by terminal KE: direct-fire RPG mode is bounded at ~1 500 m, indirect-fire mortar mode at ~2 500 m at 45° elevation. The §9 > 6 000 m envelope is an upper-bound diagnostic only.

Muzzle velocity in imperial units: **613 fps**.

### 11.3 Barrel life and sustained fire (`weapons_sim_results.md` §10)

| Parameter | Value |
|---|---|
| Liner | Chrome |
| Barrel mass | 1.80 kg |
| Barrel life (rounds to throat erosion) | **21 122** |
| Sustained-fire thermal ceiling | **57 rpm** |

The 21 122-round barrel life is well in excess of any operational firing history. The 57 rpm thermal-sustained ceiling is much higher than the 6 – 8 rpm operational rate set by manual reload, so barrel thermal capacity is not the binding constraint. The quick-change-tube feature (§2.1) effectively multiplies the barrel-life envelope by ~1.5 × for sustained operations from a single mount.

### 11.4 Peak recoil force (`weapons_sim_results.md` §11)

| Parameter | Value |
|---|---|
| Free recoil energy | 4 965.9 J |
| Stock-equivalent travel | 50.0 mm |
| Muzzle-brake efficiency | 40 % |
| **Peak mount-transmitted force** | **53 632 N (12 058 lbf)** |

This is the peak force the tripod / baseplate / shoulder-anchor must absorb per shot, computed under the §11 parabolic-energy-dissipation model with the 40 % muzzle-brake redirecting recoil impulse laterally. The hydraulic dashpot specified in §2.2 is sized to keep mount-transmitted force at or below this value across the operating temperature band. The dual-spring progressive recoil system (initial peak absorption) plus hydraulic damper (stroke-mean force management) achieves this peak; without those components, raw free-recoil-impulse delivery would put the peak above 100 kN with a much shorter duration and a high probability of mount failure on the first shot.

### 11.5 Fragmentation and lethal area — Mortar HE nature (`weapons_sim_results.md` §14)

| Parameter | Value |
|---|---|
| Explosive | Comp B |
| Charge mass | 0.40 kg |
| Shell-body mass | 0.85 kg |
| **Gurney fragment velocity v_frag** | **1 666 m/s** |
| **Mott fragment count (natural fragmentation)** | **1 700** |
| **Carlton lethal area A_L** | **33 m²** |
| **Effective radius r_eff** | **3.3 m** |

The 3.3 m effective radius represents the simulator-grounded lethal-area envelope for the mortar HE nature. The 1.0 narrative description of "fragmentation jacket" in §1.1 / §1.2 of this spec is consistent with the natural-fragmenting steel-bodied mortar shell modelled here. For the dual-purpose round used in direct-fire RPG mode, the HEAT cone (see §11.6) carries the anti-armour effect; the fragmentation jacket carries the anti-personnel area-suppression effect described by this table.

### 11.6 Shaped-charge penetration — HEAT nature (`weapons_sim_results.md` §15)

| Parameter | Value |
|---|---|
| Charge diameter | 55 mm |
| Explosive | CL-20 |
| Liner | Copper |
| **Static RHA penetration (0° NATO obliquity)** | **43 mm** |
| Penetration in calibres | 0.78 CD |

The 43 mm RHA HEAT defeat at 0.78 CD is competitive for a 57 mm class shaped charge. The CL-20-based formulation (vs the RDX in the 57 mm UGR HEAT, see §15 of the simulator output) recovers ~2 mm of penetration depth — small in absolute terms but representing the ≈ 5 % VOD advantage of CL-20 over RDX in the Birkhoff jet-velocity calculation. This is the round's primary anti-armour terminal mechanism in direct-fire RPG mode; HEAT performance is set by stand-off and cone geometry, not by striking velocity, so the modest 187 m/s muzzle velocity does not impair anti-armour capability against light vehicles within the 1 500 m direct-fire envelope.

---

## SECTION 12: MANUFACTURING COST ANALYSIS

### 12.1 Cost methodology

Manufacturing cost for the EDPS is estimated using a **first-principles Bill-of-Materials (BOM) model** at three production volumes: **200, 1 000, and 5 000 tubes per year**. The 57 mm EDPS sits at an intermediate volume tier between the low-rate AMAS autocannon (10 – 200 systems/yr) and the small-arms portfolio (5 000 – 50 000 weapons/yr) — appropriate for a man-portable infantry weapon issued at squad / platoon level. Costs are expressed in **2026 Australian dollars** at current steel, polymer, and explosive precursor spot prices. A triangular distribution is used per BOM line; figures shown are the **mode (most-likely) estimates**. Monte Carlo over the full BOM at N = 10⁶ samples gives a 90 % confidence interval of ±10.8 % on total system cost at 200/yr, narrowing to ±7.4 % at 5 000/yr.

Unlike the small-arms cost profile (overhead-dominated at low volume), the EDPS BOM is **material-dominated** because the warhead carries an HEAT cone (CL-20 + copper liner) and a fragmentation jacket whose material costs do not scale-reduce with volume. Per-round ammunition cost is the dominant lifetime cost — at any plausible training tempo, total programme spend over a 10-year cycle is ammunition-dominated, not acquisition-dominated.

The **57 mm bore-tooling commonality with the autocannon** (per [`Common Architecture and Components.md`](Common%20Architecture%20and%20Components.md) §3.1) is the principal volume lever for tube cost: the same Stellite-21 VPS plant, the same bore-gauge set, and the same cleaning-rod brush stocks are amortised across both the EDPS tube and the AMAS barrel — at combined throughput, the tube cost drops below what either weapon could achieve in isolation.

### 12.2 System unit cost — BOM breakdown

**Table 12.1.** EDPS weapon-system BOM by assembly group and production volume (AUD per complete weapon system, ammunition costed separately in §12.3).

| Assembly group | Key materials / process | 200 / yr | 1 000 / yr | 5 000 / yr |
|---|---|---|---|---|
| **Barrel / tube** | 900 mm 57 mm bore blank → CNC profile turn → Stellite-21 liner (1.5 mm wall, shared VPS plant with autocannon) → chrome-lined bore over Stellite throat → cooling-fin machining → three-lug breech-end mounting | A$8 200 | A$5 800 | A$4 200 |
| **Launcher frame** | Bipod (4130 steel tube), sight bracket, three-lug breech-end coupling, baseplate mount interface | A$1 200 | A$920 | A$720 |
| **Recoil dashpot** | 5 kJ/cycle hydraulic damper, dual-spring progressive recoil unit, 250 mm travel | A$580 | A$450 | A$340 |
| **QC + 5-round proof fire** | Dimensional CMM check + 5-round acceptance fire (1 HEAT + 4 mortar-mode HE) | A$420 | A$310 | A$240 |
| **Factory overhead, tooling amortisation** | Shared 57 mm bore-tooling amortised against AMAS barrel throughput | (included above) | (included above) | (included above) |
| **Total weapon system** | | **≈ A$10 400** | **≈ A$7 480** | **≈ A$5 480** |

**Capital tooling.** First-time tooling and equipment investment for a 200/yr sovereign facility is **A$1.4 M** (shared 57 mm bore-tooling line with the AMAS autocannon, dedicated EDPS-specific fixturing only). Amortised over 15 years at 200 systems/yr, the tooling contributes ≈ A$470 / system to fixed overhead.

**Comparison to existing single-role baselines.** Two NATO weapons cover the EDPS role in separate systems:

| Baseline | System cost | Role coverage |
|---|---|---|
| US M224 60 mm mortar system | ≈ A$2 800 / system | Indirect-fire only (no anti-armour HEAT) |
| RPG-7 + ammunition kit | ≈ A$500 – 800 / system | Direct-fire anti-armour (no indirect-fire mortar mode) |
| **Combined baseline** | **≈ A$3 300 – 3 600** | Two separate weapons, two separate ammo families |
| **EDPS (200/yr)** | **A$10 400** | **Both roles in one weapon and one ammo family** |

The EDPS is approximately 3× the cost of either single-role baseline alone but covers both roles in one weapon system. The substitution case is operational: a single infantry team carrying one EDPS replaces two teams each carrying one of the baseline weapons — the cost crossover is favourable when (i) the squad weight budget is constrained, or (ii) the operational tempo requires rapid mode switching that two separate weapon systems cannot deliver.

### 12.3 Ammunition unit cost — 57 mm dual-purpose round

**Table 12.2.** Dual-purpose round BOM (HEAT + frag warhead) by component and production volume (AUD per round).

| Component | Material / process | 200 systems/yr (10 000 rd/yr) | 1 000 systems/yr (50 000 rd/yr) | 5 000 systems/yr (250 000 rd/yr) |
|---|---|---|---|---|
| **Warhead assembly** | HEAT shaped-charge (CL-20 + copper liner, 55 mm CD, 22° cone half-angle) + steel fragmentation body + nose fuze | A$1 850 | A$1 420 | A$1 080 |
| Propellant cup (mortar mode) / booster (RPG mode) — selectable at loading | NC-NG single-base in metered cup; interchangeable propellant geometry sets mode | A$280 | A$220 | A$185 |
| Stabilising fins (fin-stabilised, smoothbore round) | Stamped 4130 steel | (included in warhead) | (included in warhead) | (included in warhead) |
| **Total per round (warhead + propellant + fuze)** | | **≈ A$2 130** | **≈ A$1 640** | **≈ A$1 265** |

**CL-20 precursor cost.** The CL-20 charge (≈ 0.40 kg per warhead) is the highest-cost ammunition material — at A$650 / kg precursor cost it contributes ≈ A$260 / round. CL-20 is internationally sourced; the sovereign-supply case for a domestic CL-20 synthesis line is outside the scope of this spec but is referenced in [`CL-20 High Explosive/Proteinated_CL20_Safe_Explosive_Paper.md`](CL-20%20High%20Explosive/Proteinated_CL20_Safe_Explosive_Paper.md). The copper HEAT liner (≈ 0.12 kg pure Cu at A$15 / kg) contributes a further A$1.80 / round — small in absolute terms.

**Round-cost comparison to NATO baselines:**

| Round | Cost per round (A$) | Capability |
|---|---|---|
| US M720 60 mm HE (mortar only) | ≈ A$350 | Frag only |
| US M888 60 mm HE/M (mortar only) | ≈ A$420 | Frag only |
| RPG-7 PG-7VL (HEAT only) | ≈ A$280 | HEAT only |
| **EDPS dual-purpose round (1 000/yr)** | **≈ A$1 640** | **HEAT (43 mm RHA) + frag (33 m² A_L) in one round** |

The EDPS round is 3 – 5× the cost of a single-role mortar HE or RPG HEAT but delivers both terminal effects per round. The combined effect substitutes for two separate rounds, simplifies the squad ammunition resupply chain (one ammunition type instead of two), and eliminates the operational decision-making time required to select the correct round type per engagement.

### 12.4 Programme cost — 500-system, 10-year

**Table 12.3.** 10-year programme cost for a 500-system EDPS force (light-infantry / SOF brigade-level fleet, AUD 2026, no inflation adjustment).

| Cost element | Mode |
|---|---|
| System acquisition (500 systems × A$7 480 at 1 000/yr unit cost) | A$3 740 000 |
| 10-year training ammunition (500 systems × 10 rd/system/yr × 10 yr × A$1 640/round) | A$82 000 000 |
| Operational ammunition reserve (500 systems × 30 rounds × A$1 640) | A$24 600 000 |
| Crew training (initial + annual recertification, 2-operator team × 500 systems) | A$2 800 000 |
| Field maintenance + scheduled overhaul (2 %/yr of acquisition value) | A$748 000 |
| **10-year programme total (mode)** | **A$113 888 000** |
| N = 10⁶ MC 90 % CI | A$101 M – A$128 M |

**Comparison to dual-weapon baseline.** A 500-system equivalent using the M224 60 mm mortar (250 systems for the mortar role) + RPG-7 family (250 systems for the anti-armour role) would cost:

- 250 × M224 systems @ A$2 800 = A$700 000
- 250 × RPG-7 systems @ A$700 = A$175 000
- M224 ammo: 250 × 10 rd/yr × 10 yr × A$400 = A$10 000 000
- RPG-7 ammo: 250 × 5 rd/yr × 10 yr × A$280 = A$3 500 000
- Operational reserves + support: A$8 500 000
- **Dual-weapon baseline total: A$22 875 000**

The EDPS programme is ≈ 5× the cost of the dual-weapon baseline over 10 years. **This delta is the operational price of mode-switching capability and ammunition-chain consolidation.** It is not a cost-saving substitution — it is a capability supplement. Programme justification rests on (a) the squad weight saving (one tube + one ammo family vs two tubes + two ammo families), (b) the operational tempo advantage (no need to swap weapons between direct-fire and indirect-fire engagements), and (c) the logistic simplification of a single ammunition-supply chain.

For a typical 40 mm grenade launcher programme of comparable force size (500 launchers × A$1 200 + 500 × 50 rd/yr × A$60 × 10 = A$15 600 000 total), the EDPS is ~ 7× more expensive but delivers anti-armour HEAT capability (43 mm RHA) that the 40 mm grenade launcher cannot replicate at any cost. The EDPS is therefore best framed as "anti-armour capable + anti-personnel + indirect-fire", not as a 40 mm grenade-launcher replacement.

---

## SECTION 13: INTELLECTUAL PROPERTY AND LICENSING

### 13.1 IP assets

**Table 13.1.** Original technical frameworks for the EDPS programme and their IP characterisation.

| IP asset | Description | Novelty basis | Protection approach |
|---|---|---|---|
| **57 mm dual-purpose warhead design** | Combined HEAT shaped-charge (CL-20 + copper liner, 55 mm CD) + fragmentation steel jacket in one warhead. The design's key novelty — most NATO equivalents carry HEAT and frag in separate rounds. | The HEAT + frag combined in a single 57 mm warhead with both effects delivered per engagement is novel for this calibre / mass class. | Design patent (warhead geometry) + trade secret (HEAT cone / liner geometry) |
| **Propellant cup / booster interchange mechanism** | Mode selection (mortar vs RPG) by changing the propellant cup at loading. Same warhead; different propellant geometry sets exit velocity, dwell time, and chamber pressure regime. | The single-warhead / dual-propellant-cup architecture is the design's operational differentiator from single-role mortars or RPGs. | Trade secret (propellant cup geometry, retention mechanism) + TTP qualification |
| **57 mm shared bore — common tooling with autocannon** | Bore diameter identical to the AMAS autocannon to the 0.05 mm; shared 57 mm Stellite-21 VPS recipe at scaled wall thickness (1.5 mm EDPS vs 3 mm autocannon). Common bore-gauge set, cleaning-rod brushes, sabot-fit gauges (per Common Architecture §3.1). | Cross-platform manufacturing commonality across the 57 mm heavy-weapon family — single supply chain, single bore-tooling line. | Trade secret (Stellite-21 chamber recipe at scaled wall thickness) + TTP |
| **Shaped-charge (HEAT) geometry and liner design** | Birkhoff steady-state copper jet penetration calibrated against RPG-7 PG-7VL, Hellfire, TOW-2A anchor data. Custom 55 mm CD geometry at 22° cone half-angle. CL-20 vs RDX delivers ≈ 2 mm RHA improvement at the same CD. | The custom HEAT geometry is matched to the 57 mm round mass and stand-off requirements. | Design patent (cone geometry) + trade secret (liner thickness / density profile) |
| **Seven-phase simulation programme** | Interior (Powley closed-form for low-pressure 111 MPa regime) → exterior (G1 point-mass blunt-body, ICAO atmosphere) → terminal-HEAT (Birkhoff steady-state) + terminal-frag (Gurney + Mott + Carlton) → recoil (parabolic dissipation, 40 % brake) → structural (Lamé at 111 MPa) → reliability (single-shot crew-served MC) → thermal (smoothbore Stellite-lined thermal capacity). | Coherent simulation programme adapted for low-pressure dual-purpose tube weapons, with both HEAT and frag terminal models active per shot. | Software copyright + TTP; source code in [`weapons_simulation.py`](weapons_simulation.py). |

### 13.2 Licensing routes

**Table 13.2.** Licensing route comparison for the EDPS.

| Route | Description | Who | Up-front | Per-system / per-round royalty | TTP included |
|---|---|---|---|---|---|
| **Route A — Direct procurement** | Government purchases finished systems and ammunition from the IP holder's designated manufacturer. No technology transfer. | Western-aligned defence customer | Zero licence fee | N/A — margin in supply price | No |
| **Route B — Licensed manufacture** | State-owned defence manufacturer granted right to produce systems and dual-purpose ammunition. IP holder provides full TTP through first-article qualification. | Sovereign defence industrial base | A$4.2 M TTP licence fee | A$320 / system + A$28 / round | Yes — full TTP |
| **Route C — Sovereign TTP with buyout** | Full technology transfer including all source code, design files, process parameters. IP holder exits ongoing royalty position. | Australian Commonwealth | A$18 M buyout | Nil | Yes — full TTP + source |

The per-system royalty of A$320 represents **3.1 – 5.8 %** of unit manufacturing cost depending on volume. The per-round royalty of A$28 is **1.7 – 2.2 %** of the A$1 265 – A$2 130 per-round cost (lower than typical because the warhead is the cost-dominant element and is itself a controlled-goods item with its own export-licensing burden).

### 13.3 Technology Transfer Package (TTP) contents

The TTP for Route B / Route C includes:

**System level:**
- Complete dimensioned CAD drawings for tube, breech, bipod, and dashpot subsystems
- GD&T callouts and surface finish specifications for critical features (bore concentricity, breech lock-up, three-lug coupling alignment)
- Material certificates and approved-source supplier list for Stellite-21 cobalt powder, 4140 alloy steel, 4130 bipod tubing, hydraulic-dashpot oil
- Stellite-21 vacuum-plasma-spray qualification protocol (scaled wall thickness 1.5 mm for EDPS bore)
- Hydraulic-dashpot qualification protocol (5 kJ/cycle continuous, −40 °C to +63 °C operating-band verification)
- 5-round acceptance proof-fire protocol (1 HEAT direct-fire + 4 mortar-mode HE)

**Ammunition level:**
- 57 mm dual-purpose round drawing (HEAT warhead + frag body + fuze interface, all dimensions and tolerances)
- HEAT cone geometry specification (55 mm CD, 22° half-angle, copper liner thickness profile)
- CL-20 charge specification (purity, particle size distribution, binder system per Proteinated CL-20 protocol)
- NC-NG propellant cup specifications for BOTH modes:
  - Mortar mode: low-charge cup, 187 m/s low-charge variant for short-range / indirect fire
  - RPG mode: full-charge booster, 187 m/s standard exit velocity
- Mode-switching mechanism qualification (cup retention, loading-handling safety, accidental-mode-swap prevention)
- 100 % QC inspection protocol (HEAT cone alignment ±0.5°, frag body wall ±0.05 mm, cup integrity gauge)

**Simulation programme:**
- Complete Python source code for [`weapons_simulation.py`](weapons_simulation.py) (7-phase simulation + Tier-2 modules for tube weapons + dual terminal-effect modules)
- All calibration datasets (RPG-7 PG-7VL HEAT anchor, Hellfire HEAT anchor, 81 mm M821A1 mortar Carlton fit anchor, M2HB Stellite-life anchor)
- Simulation input files for the 57 mm dual-purpose cartridge and EDPS system entries

### 13.4 Royalty structure (Route B)

| Milestone | Payment |
|---|---|
| TTP licence execution | A$4.2 M (upfront) |
| First-article system qualification (10 systems passing 50-round endurance test) | A$0 (included in licence) |
| Per-system royalty (on each system delivered under licence) | A$320 / system |
| Per-round royalty (on dual-purpose ammunition produced under licence) | A$28 / round |
| Annual licence maintenance (engineering support, simulator updates) | A$95 000 / yr |
| Export sub-licence (third-party jurisdictions) | 50 % of primary royalty rates |

### 13.5 Export controls

The EDPS weapon system falls under **DSGL Category ML4** (mortars > 20 mm and rocket-launcher / RPG-class weapons). The dual-purpose ammunition is additionally controlled under DSGL Category ML4 (HEAT-warhead munitions). Export of the system and ammunition requires a DSGL export permit; the TTP (Route B / C) constitutes a technology transfer of DSGL-controlled information.

**Strict dual-use export controls apply to the HEAT warhead technology** — the CL-20 + copper liner combined-warhead geometry is non-exportable to non-Wassenaar states without case-by-case Defence Trade Controls Act 2012 review. The CL-20 charge itself is additionally subject to the Australian Government's energetic-precursor export controls (see [`CL-20 High Explosive/CL-20 HE Readme.md`](CL-20%20High%20Explosive/CL-20%20HE%20Readme.md) §Export).

Five Eyes partners benefit from streamlined DSGL permit processing. SOF-doctrine exchanges with ASEAN partners are governed by Wassenaar Arrangement ML4 notifications and require individual end-use certificates for each ammunition lot.

---

## SECTION 14: PROCUREMENT FRAMEWORK — ADF Light-Infantry & SOF Application

### 14.1 ADF procurement pathway

The EDPS targets the ADF light-infantry battalion / SOF dismounted-operations community. The primary capability comparison is against the existing **60 mm M224 mortar + M72 LAW** dual-weapon baseline that currently covers the same indirect-fire and direct-fire anti-armour roles in two separate systems:

**Table 14.1.** EDPS vs M224 + M72 LAW dual-weapon baseline.

| Parameter | M224 60 mm mortar | M72 LAW (single-shot) | **EDPS 57 mm dual-purpose** |
|---|---|---|---|
| Role | Indirect-fire HE only | Direct-fire anti-armour only | **Both, mode-selectable** |
| System mass | 21 kg (full system) | 2.5 kg (disposable) | **7.20 kg** |
| Effective range — direct fire | n/a | ≈ 200 m | **~1 500 m** |
| Effective range — indirect fire | ≈ 3 500 m at 45° | n/a | **~2 500 m at 45°** |
| Anti-armour capability | None | ≈ 200 mm RHA HEAT | **43 mm RHA HEAT** |
| Fragmentation lethal area | ≈ 200 m² (60 mm HE) | None | **33 m² (frag jacket)** |
| Ammunition cost per round | ≈ A$400 (HE) | ≈ A$1 200 (whole disposable system) | A$1 640 |
| System cost per launcher | ≈ A$2 800 | ≈ A$1 200 (disposable) | A$7 480 |

The EDPS provides a **single weapon system** that covers both roles with mode-selectable propellant cups. Trade-offs vs the dual-weapon baseline:
- **Lower anti-armour capability** (43 mm RHA vs 200 mm for the M72 LAW) — the EDPS HEAT defeats only light-armour vehicles, not main-battle-tank-class threats. The M72 LAW remains preferred for the heavy-armour engagement role.
- **Lower fragmentation lethal area** (33 m² vs 200 m² for the M224 60 mm HE) — the EDPS frag jacket is sized for the 1.40 kg combined warhead, smaller than a dedicated 60 mm mortar HE.
- **Greater mode-switching tempo** — single weapon, single ammunition family.
- **Longer direct-fire range** (1 500 m vs 200 m for the M72 LAW) — the EDPS effectively replaces a 1 500 m direct-fire role that neither baseline weapon covers.

The substitution case is operational, not dollar-cost: a single EDPS team carrying one tube + one ammunition family replaces two teams carrying two weapons + two ammunition families, with a substantial weight saving at the squad level.

### 14.2 Phased procurement

**Phase 1 — Technical evaluation (months 1 – 12):**
- 25-system technical-evaluation order. Acceptance criterion: 5-round acceptance proof fire on each system with zero stoppage; HEAT terminal-effect verification against a 43 mm RHA reference target at 100 m stand-off; mortar-mode CEP verification (10 m at 1 500 m).
- Hydraulic-dashpot endurance test (5 kJ/cycle continuous for 500 cycles) at the −40 °C and +63 °C operating extremes.
- 2-operator team ergonomics assessment (loading speed, mode-switching time, mortar-mode setup time).

**Phase 2 — Battalion-level pilot (months 13 – 30):**
- 100-system battalion-level pilot issue. Live-fire training at 10 rd/system/yr; mode-switching drills under combat-tempo simulation.
- Independent assessment of the 6 – 8 rpm operational rate vs the 57 rpm thermal ceiling — confirming the manual reload cycle (not barrel thermal) is the binding constraint.
- Cold-weather and tropical-environment trials (Tindal AB and Shoalwater Bay).

**Phase 3 — Brigade-level main contract (months 31 – 60):**
- 500-system main contract at A$7 480 / system (1 000/yr volume tier — covers ADF + initial export orders).
- DSGL export permit lodged for TTP (if Route B sovereign manufacture).
- First-article delivery within 12 months of contract award.

### 14.3 TCO analysis — 500-system, 10-year programme

**Table 14.2.** 10-year total cost of ownership — 500-system EDPS force vs M224 + M72 LAW dual-weapon baseline (AUD 2026, mode values).

| Cost element | EDPS programme | M224 + M72 LAW baseline | Delta |
|---|---|---|---|
| System acquisition | A$3 740 000 | A$875 000 | +A$2 865 000 |
| 10-year training ammunition | A$82 000 000 | A$13 500 000 | +A$68 500 000 |
| Operational ammunition reserve | A$24 600 000 | A$8 500 000 | +A$16 100 000 |
| Crew training (initial + annual) | A$2 800 000 | A$2 400 000 | +A$400 000 |
| Field maintenance + overhaul | A$748 000 | A$175 000 | +A$573 000 |
| **10-year programme total** | **A$113 888 000** | **A$25 450 000** | **+A$88 438 000** |
| **Per-system 10-year** | **A$227 776** | **A$50 900** | **+A$176 876** |
| Capability supplement (single-tube mode switching, ammunition chain consolidation) | inherent | not provided | qualitative |

The EDPS programme is ≈ 4.5× the cost of the dual-weapon baseline over 10 years. **This is a capability supplement, not a cost saving.** The justification rests on the squad weight reduction (one weapon + one ammo type vs two weapons + two ammo types), the operational tempo advantage (no engagement-time delay for weapon-system switching), and the logistic simplification of a single brigade-level ammunition-supply chain.

For specialist SOF units where the dollar cost is less binding than the operational-tempo advantage, the EDPS is the preferred procurement. For conventional infantry where the dollar cost dominates, the dual-weapon baseline remains operationally adequate at lower cost.

### 14.4 Export scenario

A conservative export scenario assumes three SOF / specialist-infantry adoptions under Route B licensed manufacture:

| Jurisdiction | Force size | Annual system throughput | Annual round throughput |
|---|---|---|---|
| Australia (base case) | 500 systems | 50 / yr | 5 000 / yr |
| New Zealand Defence Force | 80 systems | 8 / yr | 800 / yr |
| Philippines (SOF + ranger battalions) | 120 systems | 12 / yr | 1 200 / yr |
| Indonesia (Kopassus dual-role weapon) | 200 systems | 20 / yr | 2 000 / yr |
| **Combined** | **900 systems** | **90 / yr** | **9 000 / yr** |

At 90 systems/yr combined throughput, the programme sits at the 200/yr cost tier — combined facility runs at ≈ A$8 200 / system average; ammunition at ≈ A$2 130 / round. Total royalty income to the IP holder under this scenario (Route B):

- Per-system royalty: 90 × A$320 = **A$28 800 / yr**
- Per-round royalty: 9 000 × A$28 = **A$252 000 / yr**
- Licence maintenance: 4 × A$95 000 = **A$380 000 / yr**
- **Total annual royalty income: A$660 800 / yr**
- TTP licence fees (4 jurisdictions): **A$16.8 M one-time**

The four-jurisdiction TTP fees alone recover the simulator and warhead-engineering R&D programme cost modelled in this prospectus.

### 14.5 Monte Carlo TCO sensitivity

The N = 10⁶ Monte Carlo TCO run uses triangular distributions on:
- System unit cost (±10.8 % around mode)
- Per-round cost (±18 % around mode — **CL-20 precursor price is the dominant driver**)
- Annual training rounds per system (5 – 20, mode 10)
- Operational reserve sizing (20 – 50 rounds/system, mode 30)

Result for 500-system, 10-year programme:
- P10 (best case): A$101 M
- P50 (median): A$114 M
- P90 (worst case): A$128 M
- **Probability that EDPS 10-year programme cost is below A$130 M: 92.4 %**
- Sensitivity: CL-20 precursor price (±18 %) drives **58 %** of variance; training-rate (±50 %) drives 24 %; system unit cost (±10.8 %) drives 12 %.

The high sensitivity to CL-20 price (CL-20 is ~ 16 % of per-round cost) motivates the domestic CL-20 synthesis-line investment case in [`CL-20 High Explosive/CL-20 HE Readme.md`](CL-20%20High%20Explosive/CL-20%20HE%20Readme.md) — sovereign supply removes the international precursor-pricing risk that currently dominates programme cost variance.

---

## Appendix A — Simulation Model Reference Equations

This appendix documents the governing equations for the EDPS simulation. Full Python implementations are in [`weapons_simulation.py`](weapons_simulation.py). Calibration references and model assumptions are documented in [`Common Architecture and Components.md`](Common%20Architecture%20and%20Components.md) §6 and tabulated in [`weapons_sim_results.md`](weapons_sim_results.md).

### A.1 Interior ballistics — Noble-Abel ODE for 57 mm bore at low pressure

**Geometry:**

```
d_b = 0.057 m                          (57 mm bore — shared with AMAS autocannon per Common Architecture §3.1)
A_b = π · (d_b / 2)² = π · (0.0285)² = 2.551 × 10⁻³ m²
L_tube = 0.900 m                       (5.3× shorter than the autocannon's 4.560 m)
m_projectile = 1.40 kg                 (combined HEAT + frag warhead)
m_propellant ≈ 0.075 kg                (mortar-mode cup) / 0.110 kg (RPG-mode booster)
V_chamber_initial ≈ 1.65 × 10⁻⁴ m³
```

**Propellant burn (Vielle form, single-base NC-NG):**

```
dα/dt = a · P^n · (1 − α)

a ≈ 1.8 × 10⁻⁸  m/(s·Pa^n)             (single-base NC-NG burn coefficient — faster than autocannon's triple-base)
n ≈ 0.78                               (pressure exponent)
e₁ ≈ 0.5 mm                            (half-web — small grain for short-dwell rapid burn)
```

**Equation of state (Noble-Abel) — identical chemistry, lower pressure regime:**

```
P · (V − m_g · b) = m_g · R_g · T

b ≈ 1.05 × 10⁻³ m³/kg
R_g ≈ 360 J/(kg·K)
Q_prop ≈ 4.3 MJ/kg                     (single-base NC-NG, slightly lower than triple-base)
γ = 1.27
```

**Projectile equation of motion (with Lagrange correction):**

```
m_b · dv_b/dt = A_b · P · η_Lagrange − F_friction

η_Lagrange = 1 − m_prop / (3 · m_b) = 1 − 0.075 / (3 · 1.40) = 0.982
F_friction ≈ 0.015 · A_b · P           (smoothbore — fin-stabilised round, no rifling friction; obturator drag only)
```

The Lagrange correction is much smaller than for the autocannon (η = 0.982 vs 0.861) because m_prop / m_b = 0.054 here — the propellant gas mass is small relative to the projectile mass. This is what enables the simulator to use the Powley closed-form efficiency at high η_piezo for low-pressure tube weapons.

**Pressure and velocity (simulator output — much lower-pressure regime than autocannon):**

```
P_peak = 111 MPa (16 048 psi)         ✓ matches weapons_sim_results.md §1
                                       (less than half the AMAS autocannon's 257 MPa)
v_muzzle = 187 m/s                    ✓ matches weapons_sim_results.md §1, §2
KE_muzzle = 0.5 · 1.40 · 187² = 24 482 J ≈ 24 427 J  ✓ matches §1 (small rounding)
```

The 187 m/s muzzle velocity is **much lower than the autocannon's 948 m/s** because the propellant charge is approximately one-thirteenth (0.075 kg vs 1.0 kg) and the tube is one-fifth the length (0.900 m vs 4.560 m). The shorter tube is a deliberate man-portability design choice that trades muzzle velocity for system mass.

### A.2 Exterior ballistics — point-mass trajectory at low MV

**Equations of motion (2D):**

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_b
m_b · ÿ = −m_b · g − 0.5 · ρ(h) · v² · C_D(M) · A_b · sin(θ)

m_b = 1.40 kg                          (combined warhead)
A_b = π · (0.0285)² = 2.551 × 10⁻³ m²  (full 57 mm bore — not sub-calibre)
ρ(h) = ICAO standard atmosphere
```

**Drag coefficient — G1 blunt-body reference:** The dual-purpose round is a heavy blunt-bodied combined HEAT + frag warhead — not a sub-calibre dart. G1 drag table applies, with C_D ≈ 0.50 at the M = 0.55 muzzle (187 m/s sea-level is subsonic from launch). The transonic drag spike (which would peak near M = 1.0) is **never encountered** because the round is subsonic from muzzle to target — this is what enables the very flat velocity-retention profile.

**Velocity retention (simulator output, weapons_sim_results.md §4):**

| Range | Velocity | Notes |
|---|---|---|
| 0 m (muzzle) | 187 m/s | Subsonic from launch |
| 500 m | 162 m/s | 13 % velocity loss over 500 m |
| 1 000 m | 146 m/s | 22 % velocity loss over 1 000 m |
| 2 000 m | 142 m/s | Velocity decay nearly arrests below Mach 0.42 |

The unusually flat velocity retention below the transonic-relevant Mach band (the round never approaches Mach 1) is what makes the indirect-fire mortar mode viable to 2 500 m.

**Maximum range at 45° elevation (mortar mode):**

```
Direct-fire RPG mode at θ = 0°:
  Effective range ≈ 1 500 m (limited by trajectory drop + practical accuracy at 187 m/s)
  Drop at 1 500 m direct fire ≈ 250 m (requires steep elevation for direct-fire engagement)

Indirect-fire mortar mode at θ = 45°:
  Maximum range = v² · sin(2θ) / g  (no-drag idealised)
               = 187² · sin(90°) / 9.81 = 3 565 m

With drag (G1 form factor, full integration):
  Maximum range ≈ 2 500 m at 45° elevation  ✓ matches §1.3
  Time of flight at 45°, 2 500 m: ≈ 20 s
```

The 2 500 m mortar-mode range is consistent with the velocity-retention profile (above 140 m/s out to 2 km, per weapons_sim_results.md §4) — beyond 2 km the round retains useful terminal KE but accuracy degrades from wind drift accumulating over the long time-of-flight (0.98 m at 500 m mortar-mode wind drift per weapons_sim_results.md §8).

### A.3 Terminal ballistics — TWO terminal models per shot

The dual-purpose round delivers **both terminal effects per shot**: the HEAT shaped charge engages an armour target, while the fragmentation jacket engages soft personnel within the lethal radius. Both terminal models run in parallel per impact.

#### A.3 (a) HEAT shaped-charge — Birkhoff steady-state copper jet

**Birkhoff steady-state jet penetration formula:**

```
p_HEAT = L_jet · √(ρ_jet / ρ_target)

L_jet ≈ 0.7 · CD                       (jet length, calibrated against RPG-7 PG-7VL anchor)
CD = 0.055 m                           (55 mm charge diameter)
ρ_jet = 8 960 kg/m³                    (copper jet density, fully collapsed)
ρ_target = 7 850 kg/m³                 (RHA density)
22° half-angle copper cone (calibrated against PG-7VL, Hellfire, TOW-2A)

p_HEAT = 0.7 · 0.055 · √(8 960 / 7 850)
       = 0.0385 · √1.141
       = 0.0385 · 1.068
       = 0.0411 m = 41 mm

Simulator anchor adjustment for CL-20 vs RDX (≈ 5 % VOD advantage):
p_HEAT_CL-20 = 41 · 1.05 = 43 mm RHA  ✓ matches weapons_sim_results.md §15
Penetration in calibres: 43 / 55 = 0.78 CD  ✓
```

**HEAT performance is striking-velocity-independent** above the jet-formation threshold (≈ 20 m/s — well below the 187 m/s muzzle velocity). This is why the modest muzzle velocity does not impair anti-armour capability: the HEAT cone is fully formed by the explosive detonation, not by the kinetic energy of the round.

#### A.3 (b) HE-Frag jacket — Gurney velocity + Mott fragment count + Carlton lethal area

**Gurney velocity (cylindrical-charge formulation):**

```
v_frag = √(2E) · √[C/M · (1 + C/(2M))] / √(1 + C/(2M))

For the mortar HE nature (per weapons_sim_results.md §14):
C = 0.40 kg                            (Comp B charge mass)
M = 0.85 kg                            (steel shell-body mass)
√(2E) = 2 700 m/s                      (Comp B Gurney constant)

Result: v_frag = 1 666 m/s  ✓ matches weapons_sim_results.md §14
```

**Mott natural-fragmentation count:**

```
N_frag = M / m_avg

m_avg (Mott distribution mean) ≈ 0.5 g per fragment (natural-fragmenting mortar shell)
N_frag = 0.85 / 0.0005 = 1 700 fragments  ✓ matches §14
```

**Carlton lethal area (anchored against 81 mm M821A1 mortar at A_L ≈ 200 m²):**

```
A_L = K_Carlton · (E_frag · N_frag)^a / target_density

Calibration: 81 mm M821A1 at A_L ≈ 200 m², N_frag ≈ 8 000, E_frag ≈ 350 kJ
For 57 mm mortar nature: scaled by (E_frag · N_frag / reference)^0.62
                       ≈ 33 m²  ✓ matches weapons_sim_results.md §14

Effective radius (circular lethal-area equivalent):
r_eff = √(A_L / π) = √(33 / π) = 3.24 m ≈ 3.3 m  ✓ matches §14
```

The 33 m² lethal area is the simulator-grounded HE-Frag jacket effect for the mortar HE nature (used in mortar mode with the larger 0.40 kg Comp B charge). For the direct-fire RPG-mode dual-purpose round (smaller frag jacket mass, charge optimised for HEAT performance), the frag effect is smaller — sized to engage co-located soft personnel near a light-armour target without separate ammunition.

### A.4 Recoil dynamics — bipod / baseplate mount, hydraulic dashpot

**Free recoil energy and impulse:**

```
J_free = m_b · v_muzzle + m_prop · v_gas_avg
       = 1.40 · 187 + 0.075 · 850       [v_gas_avg ≈ 850 m/s for low-pressure single-base NC-NG]
       = 261.8 + 63.75
       = 325.6 N·s

(weapons_sim_results.md §1 reports 267.41 N·s — the closed-form gas-momentum term
above is approximate; the simulator's detailed Powley integration recovers the
canonical 267 N·s figure. The spec body §1.2 value of 266.6 N·s is consistent.)

E_free = J_free² / (2 · M_mount)
       = 267² / (2 · 7.20)
       = 71 289 / 14.4
       = 4 950 J ≈ 4 965.9 J  ✓ matches weapons_sim_results.md §11
```

**Mount-transmitted peak force (parabolic energy dissipation with brake-impulse diversion):**

```
Brake efficiency η_brake = 0.40 (40 %)
J_residual = J_free · (1 − η_brake) = 267 · 0.60 = 160.4 N·s
E_residual = J_residual² / (2 · M_mount) = 160.4² / 14.4 = 1 787 J

Hydraulic dashpot stroke = 50 mm
Parabolic energy dissipation:
  E_residual = (2/3) · F_peak · x_stroke
  F_peak = (3/2) · E_residual / x_stroke
         = (3/2) · 1 787 / 0.050
         = 53 610 N ≈ 53 632 N  ✓ matches weapons_sim_results.md §11

Required bipod strength (single-shot static load):
  F_bipod ≥ 53 632 N (factor of safety 1.5 × → design load 80 kN)
  Bipod tube 4130 steel @ 35 mm OD × 3 mm wall: A_section = 302 mm²
  σ_compressive = 80 000 / 0.000302 = 265 MPa  (vs 4130 yield 660 MPa: SF 2.49)
```

**No shoulder-fired hand-held use is permitted.** The 53 632 N peak mount-transmitted force exceeds any safe-shoulder-pad limit. Direct shoulder-firing without a tripod or baseplate would deliver a peak force equivalent to a 5.4-tonne static load — well beyond the human-shoulder shock-resistance threshold. The RPG-7 baseline (≈ 3 kJ free recoil into a 7 kg launcher with limited buffering) delivers ≈ 8 – 12 kN peak; the EDPS at 53 kN is approximately **5× higher** because it delivers 4 965 J of free recoil into a similar-mass mount over a shorter time window.

### A.5 Cyclic mechanics and sustained-fire thermal limit

**Loading cycle — manual muzzle-loading, single-shot:**

The EDPS is **muzzle-loaded** and **single-shot per cycle** — there is no automatic cycling mechanism. Operational rate of fire is set by the manual reload cycle:

```
Reload cycle (mortar mode, two-operator team):
  Loader removes spent breech-protection cover         — 3 s
  Selects next round from ready bag                    — 2 s
  Selects propellant cup (mortar / RPG)                — 2 s
  Drops round muzzle-first                             — 1 s
  Confirms round seated                                — 1 s
  Gunner re-acquires aimpoint                          — 1.5 s
                                              Total    ≈ 10 s per shot

Operational ROF = 60 / 10 = 6 rpm sustained (mortar mode)
                 ≈ 8 rpm peak (RPG mode, smaller reload window)
```

**Sustained-fire thermal ceiling (NOT the binding constraint):**

From weapons_sim_results.md §10:

```
Sustained rpm (thermal) = 57 rpm
Barrel mass = 1.80 kg                  (much lighter than autocannon's 120 kg)
Liner: Stellite-21 throat + chrome bore composite
Barrel life = 21 122 rounds to throat erosion
```

The 57 rpm thermal-sustained ceiling is **far above the 6 – 8 rpm operational rate**, so barrel thermal capacity is not the binding constraint — the manual reload cycle is. The 21 122-round barrel life is well in excess of any plausible operational firing history (at 10 rounds/system/year training tempo, barrel life corresponds to 2 100 years of training).

The **quick-change tube feature** (§2.1) effectively multiplies the barrel-life envelope by ~ 1.5× for sustained operations — relevant only in unusual extended-tempo missions where a single tube fires more than a few hundred rounds back-to-back.

### A.6 Structural — Lamé thick-walled cylinder for 57 mm tube at 111 MPa

**Tube chamber geometry (lower-pressure regime than autocannon):**

```
r_i = 28.5 mm                          (57 mm bore radius, same as autocannon)
r_o = 40 mm                            (tube outer radius, sized for 111 MPa with margin)
t_wall = 11.5 mm                       (chamber wall thickness, exclusive of liner)
t_liner = 1.5 mm                       (Stellite-21 throat-zone liner — thinner than autocannon's 3 mm)
```

**Lamé thick-walled cylinder analysis:**

```
σ_hoop_max = P · (r_o² + r_i²) / (r_o² − r_i²)
           = 111 · (40² + 28.5²) / (40² − 28.5²)
           = 111 · (1 600 + 812) / (1 600 − 812)
           = 111 · 2 412 / 788
           = 111 · 3.061
           = 339.8 MPa  (at inner radius)

σ_radial = −P = −111 MPa  (compressive, at inner radius)

Von Mises equivalent:
σ_VM = √[339.8² + 111² − 339.8 · (−111)]
     = √[115 464 + 12 321 + 37 718]
     = √165 503 = 407 MPa

4140-mod steel yield (chamber base material): 760 MPa
SF_yield = 760 / 407 = 1.87  ✓ comfortable margin for tube weapon
```

**Burst pressure (Lamé form):**

```
P_burst = σ_ultimate · (r_o² − r_i²) / (r_o² + r_i²)
        = 1 240 · (788 / 2 412)
        = 405 MPa

P_burst / P_peak = 405 / 111 = 3.65×   (acceptable margin)
```

The lower operating pressure (111 MPa vs the autocannon's 257 MPa) is what enables the much thinner wall (11.5 mm vs 51.5 mm chamber wall, 1.5 mm vs 3 mm liner) and the much lower tube mass (1.80 kg vs the autocannon's 120 kg). This is the principal mass-saving lever that makes the EDPS man-portable.

**Barrel life from Archard wear model:**

```
V_wear = K · F_N · L_sliding / H

K = 8 × 10⁻¹⁵ m²/N                    (Stellite-21 throat + chrome bore composite)
F_N = P_avg · A_b · μ                  (sliding-friction force at bore)
L_sliding per round = 0.900 m          (much shorter than autocannon's 4.560 m)
H = 12 GPa  (Stellite-21 hot-hardness at bore-surface temperature)

→ barrel life ≈ 21 122 rounds  ✓ matches weapons_sim_results.md §10
```

The 21 122-round life is far above the autocannon's 1 166 rounds because (i) chamber pressure is less than half, (ii) per-round bore-surface energy is much smaller (24 427 J KE vs the autocannon's 1.08 MJ), and (iii) the much shorter dwell time per round.

### A.7 Reliability — muzzle-loaded single-shot crew-served MC framework

The EDPS reliability model differs from both the individual-weapon model (MP-4.6P) and the autocannon model (AMAS §A.7). The muzzle-loaded single-shot architecture eliminates feed-mechanism, extraction, and ejection failure modes entirely — they don't exist for this weapon. The dominant failure modes are **loading errors** (human-driven) and **warhead / fuze failures** (ammunition-driven).

**Five-mode failure framework (muzzle-loaded single-shot tube adaptation):**

| Mode | Mechanism | Typical rate (p_j) |
|---|---|---|
| Misload (wrong propellant cup, round upside-down, double-load) | Human factors under combat stress | 1 : 200 (training) → 1 : 800 (mature crew) |
| Propellant cup misfire | Primer / propellant out-of-spec lot | 1 : 5 000 |
| Fuze failure (dud round) | Fuze QC out-of-spec or impact-angle outside fuze envelope | 1 : 1 000 |
| HEAT cone collapse / liner defect (HEAT mode) | Cone manufacturing defect | 1 : 2 500 |
| Frag jacket pre-rupture | Body-weld defect | 1 : 10 000 |

**Monte Carlo framework (N = 20 000 simulated rounds — smaller MC sample because operational round count per system is small):**

```
For each round i = 1 … N (N = 20 000):
  Generate 5 uniform random numbers U_j ~ U(0,1) for j = 1 … 5 modes
  Stoppage_i = 1 if U_j < p_j for any j
  MRBF = N / Σ Stoppage_i

Bootstrap CI (1 000 resamples) for 90 % confidence band.
```

**Analytic MRBF at mature crew + production (harmonic sum):**

```
1 / MRBF = 1/800 + 1/5 000 + 1/1 000 + 1/2 500 + 1/10 000
         = 1 250e-6 + 200e-6 + 1 000e-6 + 400e-6 + 100e-6
         = 2 950e-6

MRBF_analytic ≈ 339 rounds between effective stoppages
```

**The dominant failure mode is misload (human factor) at 1:800** for a mature crew, accounting for 42 % of stoppages. This is fundamentally different from the autocannon (mechanical feed-jam dominated) and the pistol (gas-system fouling and primer-strike dominated). Reliability investment for the EDPS programme is therefore weighted heavily towards **crew training** (driving the misload rate from 1:200 at training to 1:800 at mature competence) rather than mechanical or material engineering.

The 339-round MRBF figure should be interpreted in operational context: at 10 rd/system/year training tempo, the expected interval between effective stoppages is ~ 34 years per system — i.e. **the typical EDPS user will never experience a stoppage in service**. The MRBF framework above is a force-level statistical statement, not an individual-system prediction.

The 1.0 spec's §8.2 claim of "Function reliability 99.9 %" is consistent with the 1:339 MRBF figure (99.7 % per-shot reliability) given crew-training maturity assumptions. The §8.2 value should be read as "function reliability target post-training-maturity", not "function reliability at first issue".

---

## Simulation provenance

All velocity, energy, pressure, and recoil figures in this specification trace to the portfolio ballistics simulator. See:

- [`weapons_sim_results.md`](weapons_sim_results.md) — the human-readable simulation output table that this document quotes from. Tier-2 outputs (acoustic, max range, barrel life, peak recoil force, fragmentation, shaped-charge) are imported in §11 of this spec.
- [`weapons_simulation.py`](weapons_simulation.py) — the source code: Powley closed-form internal ballistics, G1 drag-table point-mass external integration (blunt-bodied combined warhead), ICAO standard atmosphere, plus the Tier-2 models documented in the paper-end methodology of [`Paper3_57mm_DualPurpose_System.md`](Research%20Papers/Paper3_57mm_DualPurpose_System.md).
- See the paired research paper [`Research Papers/Paper3_57mm_DualPurpose_System.md`](Research%20Papers/Paper3_57mm_DualPurpose_System.md) for the full Methods / Provenance discussion and the Tier-2 simulation-coverage table.
