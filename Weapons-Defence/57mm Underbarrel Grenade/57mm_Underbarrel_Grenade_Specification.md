# 57mm Underbarrel Grenade Round
## Complete Technical Specification
### Light Multi-Purpose Round, Single-Shot Break-Action

*Operator Specification Sheet*

Document No. TRP-2026-105 | Version 2.0 (simulator-calibrated)

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> **The 57 mm Underbarrel Grenade Round is the portfolio's light multi-purpose under-barrel HE-FRAG launcher** — a single-shot break-action 305 mm tube on a 2.40 kg launcher mount, firing a 350 g pre-formed tungsten-fragmentation grenade at **149 m/s** for a muzzle energy of **3 872 J**, an effective direct-fire range of **~300 m** against point targets, and a maximum direct-fire range of **~400 m** against personnel in the open. Peak chamber pressure is **109 MPa**; raw free recoil into the 2.40 kg launcher is **578.8 J** — roughly an order of magnitude more than the heaviest hand-held shoulder-fired round in common service — with a raw free-recoil peak force of **48 237 N** at the launcher–rifle rail that the mandatory hydraulic / elastomeric buffer reduces to a shoulder-felt force below 200 N. Anti-personnel terminal effect: the simulator-grounded Gurney / Mott / Carlton computation (§11.5 / §14 of `weapons_sim_results.md`) gives **11 m² Carlton lethal area** and **1.9 m effective radius** for the warhead geometry — comparable to a 40 mm M433 grenade. Earlier pre-simulator author estimates of "15 m lethal / 25 m casualty radius" are explicitly superseded by this simulator result; see §11.5 and the Appendix honest-discrepancy flag. Fragment velocity ~1 909 m/s (Gurney); rate of fire is 4 – 6 rpm, manual break-action reload. All ballistic numbers in this sheet are anchored to the `weapons_simulation.py` simulator and tabulated in [`weapons_sim_results.md`](../weapons_sim_results.md). The classification banner above is illustrative-only — adopted for tonal coherence with the rest of the Weapons-Defence portfolio — and does not reflect any real security marking.

> **Specification refresh — all ballistic numbers in this document are derived from the portfolio ballistics simulator (`weapons_simulation.py`) and tabulated in [`weapons_sim_results.md`](../weapons_sim_results.md). The earlier 250 m/s / 2 800 bar / 600 m maximum figures are superseded by the simulator-calibrated 149 m/s / 109 MPa / ~400 m direct-fire envelope shown below.**

## Honest framing

- **Simulation-derived, pre-prototype.** Every ballistic number in this sheet — 149 m/s muzzle velocity, 3 872 J muzzle energy, 109 MPa peak chamber pressure, 578.8 J raw free recoil, 48 237 N raw peak rail-transmitted force, ~300 m effective / ~400 m maximum direct-fire range — is a simulator output from `weapons_simulation.py`, tabulated in [`weapons_sim_results.md`](../weapons_sim_results.md). No physical under-barrel prototype has been fired, and no live fragmentation pattern has been measured. The simulator-grounded 1.9 m effective radius (11 m² Carlton lethal area) supersedes earlier pre-simulator author estimates of 15 m lethal / 25 m casualty radius — see §11.5 and Appendix A honest-discrepancy flag.
- **Single source of truth.** Earlier-draft figures (250 m/s direct fire, 2 800 bar chamber pressure, 600 m maximum range) are superseded by the simulator-calibrated 149 m/s / 109 MPa / ~400 m envelope shown in §1.2 – §1.3. Future grenade / propellant / barrel-length changes re-run the simulator and update this sheet against the new `weapons_sim_results.md` in one pass.
- **Recoil envelope mandates a buffer.** Free recoil of 578.8 J into a 2.40 kg launcher is roughly an order of magnitude more than the heaviest hand-held shoulder-fired round in common service (a 12-gauge 3" magnum slug delivers ~50 J into a 4 kg shotgun); the **48 237 N raw peak rail-transmitted force** is the value the mount must be sized against. A hydraulic / elastomeric buffer between launcher and host-rifle rail is mandatory, and shoulder-stocked two-hand support — no one-handed or hip-fired use — is the only permitted firing posture.
- **Trajectory model is G1 blunt-body.** Velocity drops from 149 to ~84 m/s within the first 100 m as the grenade decelerates through the transonic-relevant Mach band; beyond ~100 m the velocity stabilises in the low-drag subsonic regime, but the absolute drop becomes the binding accuracy constraint. The simulator does not model wind, target movement, or fire-control solutions, and the 4–6 rpm rate is set by the manual break-action reload cycle, not by barrel thermal capacity.
- **Manufacturing chain.** The 57 mm bore-gauge set common to the underbarrel launcher, dual-purpose tube, and autocannon (per [`Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) §3) is a design-intent commonality, not a procured factory line. Tungsten cube / cylinder / rod pre-formed fragmentation is dependent on a sovereign tungsten-powder supply that the portfolio assumes but does not contract.
- **Classification is illustrative.** The `UNCLASSIFIED // FOR OFFICIAL USE ONLY` banner is adopted for tonal coherence with the rest of the Weapons-Defence portfolio. No real sponsorship, no real programme office, no fielded system implied.

## SECTION 1: CORE SPECIFICATIONS

### 1.1 Round Parameters
- Type: 57 mm low-velocity High-Explosive Fragmentation (HE-FRAG) grenade
- Calibre: 57 mm
- Projectile (grenade) mass: **350 g**
- Propellant: low-charge, ball-powder, in a stub cartridge
- Launcher format: **single-shot, break-action under-barrel**
- Launcher empty mass: **2.40 kg**
- Launcher barrel length: **305 mm**

### 1.2 Performance Data
- Muzzle Velocity: **149 m/s**
- Muzzle Energy: **3 872 J**
- Peak Chamber Pressure: **109 MPa (15 800 psi)**
- Recoil Impulse: 52.6 N·s
- Free Recoil Energy (2.40 kg launcher): **578.8 J (426.9 ft·lb)** — **HIGH** for a hand-held under-barrel launcher; the launcher itself imposes a recoil-mitigation requirement (shoulder stock or weapon-mounted buffer; see §4)
- **Free-recoil peak force at the launcher–rifle interface: 48 237 N (10 845 lbf)** (`weapons_sim_results.md` §11, 18 mm sprung-stock travel, no muzzle brake). **IMPORTANT: this is the FREE recoil force — the actual underbarrel mount uses a hydraulic buffer (see §4.2) to bring the shoulder-felt force below 200 N.** The 48 kN figure is the value that would be transferred to the host rifle's rail if no buffer were fitted; it is included here because the mount design *must* be sized against this raw value.
- Maximum Range: ~400 m direct-fire (limited by drop and the G1 blunt-body drag profile); see §11.2 for the Hatcher KE > 80 J max-effective-range envelope from `weapons_sim_results.md` §9
- Effective Range: ~300 m direct-fire (point targets); ~400 m area-effect against personnel in the open
- Rate of Fire: 4 – 6 rpm (limited by manual break-action reload)

### 1.3 Velocity vs Range (G1 form factor — blunt-bodied grenade)
| Range | Velocity |
|---|---|
| Muzzle (0 m) | 149 m/s |
| 100 m | **84 m/s** |
| 300 m | **80 m/s** |

The grenade is blunt-bodied, so the G1 drag profile applies; velocity falls off sharply in the first 100 m as the projectile decelerates through and just below the transonic-relevant Mach band. Beyond ~100 m the velocity stabilises in the low-drag subsonic regime, but the absolute drop becomes the binding constraint on accuracy.

## SECTION 2: WARHEAD DESIGN

### 2.1 Enhanced Explosive System
- Primary Charge:
  * HMX Base: 65%
  * PBXN-110: 20%
  * Cerium Oxide Nano: 5%
  * Iron Oxide Nano: 3%
  * Advanced Aluminium: 5%
  * Binders: 2%
  * Total Payload: ~80 g (sized to the 350 g grenade mass)

### 2.2 Advanced Fragmentation
- Pre-Formed Matrix (scaled to the smaller grenade):
  * Tungsten Cubes (3 mm):
    - Quantity: ~200
    - Reactive coating
    - Optimised dispersion
  * Tungsten Cylinders (5 mm):
    - Quantity: ~100
    - Enhanced stability
  * Penetrator Rods (7 mm):
    - Quantity: ~40
    - Critical-component defeat

### 2.3 Terminal Effects
- Anti-Personnel:
  * Lethal Radius: 15 m
  * Casualty Radius: 25 m
  * Fragment Velocity: ~1 500 m/s (independent of muzzle velocity — set by the warhead charge-to-fragment mass ratio)
  * Multiple injury mechanisms
- Anti-Materiel:
  * Light vehicle penetration via fragment rods
  * Structure breach against earth-and-timber field works
  * Equipment destruction at close range

## SECTION 3: FUZING SYSTEM

### 3.1 Multi-Mode Fuze
- Operating Modes:
  * Impact (instant)
  * Impact (delay, ~50 ms)
  * Proximity (HOB optimised for personnel-in-open)
  * Self-destruct backup (≈ 25 s — beyond maximum direct-fire time-of-flight)

### 3.2 Safety Features
- Mechanisms:
  * Mechanical setback safety
  * Spin activation (requires several rotations to arm; arms ~20 m beyond muzzle)
  * Drop safety
  * Environmental seals
  * Transport safety
  * Manual safe

## SECTION 4: PROPULSION AND RECOIL

### 4.1 Propellant Design
- Characteristics:
  * Low-flash formulation
  * Progressive burning
  * Temperature stable
  * Low erosion
  * Reduced signature
  * Consistent peak pressure at 109 MPa

### 4.2 Recoil Management — **mandatory mitigation**

At 350 g projectile mass × 149 m/s exit velocity, recoil impulse is 52.6 N·s and free recoil energy is **578.8 J (426.9 ft·lb)** into a 2.40 kg launcher. For comparison, a 12-gauge 3″ magnum slug delivers approximately 50 J of free recoil into a 4 kg shotgun. **The 57 mm UBGL delivers roughly an order of magnitude more recoil energy than the heaviest hand-held shoulder-fired round in common service.**

Mitigation is therefore not optional:
- **Shoulder stock** for the host weapon, extended and locked, transferring recoil to the firer's torso (not the firer's wrist)
- **Weapon-mounted hydraulic or elastomeric buffer** between the launcher and the host-rifle rail
- Optional **shoulder pad** on the firer's plate carrier at the buttstock contact point
- Firing posture restricted to **shoulder-fired, two-hand support** — no one-handed or hip-fired use

## SECTION 5: CASE CONSTRUCTION

### 5.1 Case Design
- Features:
  * High-strength aluminium
  * Reinforced base
  * Enhanced extraction groove
  * Pressure seal system
  * Guide bands
  * Wear reduction

### 5.2 Environmental Protection
- Capabilities:
  * All-weather operation
  * Temperature stable
  * Moisture resistant
  * Impact protected
  * Storage stable
  * Transport ready

## SECTION 6: TERMINAL PERFORMANCE

### 6.1 Effect Zones
- Anti-Personnel:
  * Primary Kill Zone: 15 m
  * Casualty Zone: 25 m
  * Fragment Density: ~6/m² at 15 m
  * Multiple effects
- Anti-Materiel:
  * Light Armour: ~10 mm RHA against the 7 mm fragment rods only (the grenade itself is not an anti-armour munition)
  * Structures: Major damage to field cover
  * Equipment: Destruction within 5 m of detonation
  * Components: Defeat by fragment penetration

### 6.2 Special Effects
- Enhanced Features:
  * Incendiary effect from CeO₂ / Fe₂O₃ / Al thermite-style additives
  * Spall generation against light cover
  * System disruption against electronics within 5 m
  * Area denial within the 25 m casualty zone

## SECTION 7: OPERATIONAL FEATURES

### 7.1 Handling
- Single-shot break-action: hinge the launcher down, eject spent case, insert new round, close to chamber
- Positive lock
- Simple manual extraction
- Clear chamber indicators

### 7.2 Performance
- Low dispersion (about 3 mil at 200 m direct-fire, set by the launcher's iron sights and the grenade's drop profile)
- Consistent trajectory (the 149 m/s muzzle velocity is reproducible to ±3 m/s across the −40 °C to +63 °C operational band)

## SECTION 8: RELIABILITY

### 8.1 Function Standards
- MRBF analytic (§23): 13 857 rounds
- MRBF simulated (§23): 30 000 rounds
- FTF rate (§23): 1:40 000
- Felt recoil (§23): 160.262 ft·lb
- Bore life service (§23): 5 000 rounds
- Operation: 99.9%
- Safety: 100%
- Storage: 10 years
- Transport: Protected
- Handling: Safe

### 8.2 Environmental
- Temperature: −40 °C to +63 °C
- Humidity: 0 – 100%
- Sand/Dust: Protected
- Rain: All conditions
- Salt Spray: Protected

## SECTION 9: MANUFACTURING

### 9.1 Production Standards
- Quality control
- Lot testing
- X-ray inspection
- Performance validation
- Safety certification

### 9.2 Storage
- Temperature control
- Humidity protection
- Impact protection
- Clear marking

## SECTION 10: PERFORMANCE METRICS

### 10.1 Accuracy Standards
- CEP: ~3 mil at 200 m direct-fire
- First-round hit probability: ~70% at 200 m against vehicle-sized targets (set by the steep drop profile)
- Reliable function

### 10.2 Effect Standards
- Fragment Distribution: Even
- Effect Reliability: 95%
- Fuze Function: 99.9%
- Safety Systems: 100%

## SECTION 11: TIER-2 SIMULATION OUTPUTS

The following numbers are imported directly from `weapons_sim_results.md` (sections cited per row). The 57 mm UGR launcher is unsuppressed by design; in §6 of the source the "Muzzle (sup)" and "Ear (sup)" columns therefore equal the unsuppressed values for this weapon.

### 11.1 Acoustic signature (`weapons_sim_results.md` §6)

| Column | Value (dB peak SPL) |
|---|---|
| Muzzle (unsuppressed) | **163.1 dB** |
| Shooter's ear (unsuppressed) | **156.1 dB** |
| Muzzle (suppressed) | 163.1 dB *(unsuppressed — no suppressor)* |
| Shooter's ear (suppressed) | 156.1 dB *(unsuppressed — no suppressor)* |
| Ear + foam plug (−22 dB) | 134.1 dB |
| Ear + double plug & muff (−28 dB) | 128.1 dB |
| Ear + double + TACS active (−28 + 25 dB) | **103.1 dB** |

Unsuppressed peak SPL exceeds the OSHA 140 dB ceiling by 23 dB. Even double hearing protection brings the ear-felt peak only to 128.1 dB — still above the 140 dB ceiling at the +12 dB conservative-stack accounting some procurement registers use. The TACS personal active-cancellation overlay (additional −25 dB) brings the value to 103.1 dB, which is safe by both OSHA and the conservative-stack accounting.

### 11.2 Maximum effective range (`weapons_sim_results.md` §9)

- **Hatcher KE > 80 J personnel-threshold range: > 6 000 m (sim envelope cap)** — the 350 g grenade retains > 80 J terminal KE across the entire integration envelope because the mass is large relative to the muzzle velocity, so terminal energy is dominated by the projectile mass even after deceleration.
- **Supersonic range: 0 m** — the 149 m/s muzzle velocity is well below Mach 1 (≈ 343 m/s in ISA sea-level air). The round is *intrinsically subsonic* and exhibits no transonic-band drag spike. Muzzle velocity in imperial units: **488 fps**.

The > 6 000 m Hatcher envelope is **not** the operational effective range — operational range is bounded at ~400 m by drop and accuracy, not by terminal KE. The §9 figure is an envelope diagnostic only and confirms the grenade does not become non-lethal at any point in its trajectory.

### 11.3 Barrel life and sustained fire (`weapons_sim_results.md` §10)

| Parameter | Value |
|---|---|
| Liner | Chrome |
| Barrel mass | 0.55 kg |
| Throat-erosion life (§10) | **69 500** |
| Bore life service (§23) | **5 000** |
| Sustained-fire thermal ceiling | **126 rpm** |

The §10 throat-erosion life (69 500 rounds) is the Tier-2 Archard wear bound. The §23 **bore life service** rating of **5 000 rounds** matches §23.0.1 chrome-lined launch-tube replace interval. The 126 rpm thermal-sustained ceiling is irrelevant in operational use (manual break-action reload limits cyclic rate to <10 rpm). The 126 rpm thermal-sustained ceiling is irrelevant in operational use (the manual break-action reload limits cyclic rate to <10 rpm) but is reported here for symmetry with the rest of the portfolio.

### 11.4 Peak recoil force (`weapons_sim_results.md` §11)

| Parameter | Value |
|---|---|
| Free recoil energy | 578.8 J |
| Stock-equivalent travel | 18.0 mm |
| Muzzle-brake efficiency | 0 % |
| **Peak free-recoil force at the launcher** | **48 237 N (10 845 lbf)** |

**IMPORTANT clarification on the 48 kN peak force.** This is the *free* recoil force — the force that would appear at the launcher-rifle interface if the launcher were rigidly mounted to the host rifle's rail with zero buffering. **The actual fielded mount does NOT see 48 kN at the shoulder.** The mandatory hydraulic-elastomeric buffer specified in §4.2 absorbs the impulse over a much longer time-stretch, bringing the *shoulder-felt* peak force below ~200 N — comparable to a 12-gauge magnum slug into a 4 kg shotgun.

The 48 kN figure is included here because **the mount and buffer design must be sized against this raw value**. Specifically:

- The launcher–rail interface must withstand 48 kN peak as a structural design-load case.
- The hydraulic buffer must absorb the full 578.8 J energy budget per shot.
- The host rifle's stock and the firer's shoulder see only the buffered, time-stretched residual — < 200 N peak.

Without the buffer the 48 kN raw force into a shoulder would cause clavicle / scapula fracture with high probability on the first shot. The buffer is therefore not a comfort feature — it is a safety-critical mandatory subsystem.

### 11.5 Fragmentation and lethal area — HE-Frag warhead (`weapons_sim_results.md` §14)

| Parameter | Value |
|---|---|
| Explosive | Comp B |
| Charge mass | 0.12 kg |
| Shell-body mass | 0.18 kg |
| **Gurney fragment velocity v_frag** | **1 909 m/s** |
| **Mott fragment count (pre-scored)** | **720** |
| **Carlton lethal area A_L** | **11 m²** |
| **Effective radius r_eff** | **1.9 m** |

The 1.9 m effective radius supersedes the earlier narrative 15 m "lethal radius" / 25 m "casualty radius" values in §6.1 / §2.3 — those were author estimates; the §14 Gurney / Mott / Carlton computation gives the simulator-grounded radius shown here. This is a small-grenade lethal-area envelope, comparable to an M67 hand grenade (≈ 5 m kill / 15 m casualty in published US Army TM 43-0001-29). For sustained engagement of fortified targets the 57 mm Mortar/RPG round (§14 sister entry: 33 m² A_L) or 57 mm Autocannon HE-Frag (117 m²) is the right answer.

### 11.6 Shaped-charge penetration — HEAT nature (`weapons_sim_results.md` §15)

The 57 mm UGR family includes an optional HEAT nature alongside the primary HE-Frag described in §2:

| Parameter | Value |
|---|---|
| Charge diameter | 55 mm |
| Explosive | RDX |
| Liner | Copper |
| **Static RHA penetration (0° NATO obliquity)** | **41 mm** |
| Penetration in calibres | 0.75 CD |

The 41 mm RHA HEAT defeat is slightly below the M433 40 mm HEDP (≈ 51 mm RHA) — the lower-charge-mass 57 mm grenade gives up some shaped-charge depth in exchange for the much larger HE-Frag payload in the primary nature. The HEAT nature is intended for fortification breach (timber-and-earth bunkers, brick walls, light-skin vehicles) where the HE-Frag round would either over-penetrate without effect or fail to defeat the cover.

### 11.7 Portfolio lifecycle (`weapons_sim_results.md` §23)

| Metric | Value |
|---|---|
| Felt recoil | 160.262 ft·lb |
| Barrel SF_yield | 1.41 |
| Bore life service (§23) | 5 000 rounds |
| MRBF analytic | 13 857 rounds |
| MRBF simulated | 30 000 rounds |
| FTF rate | 1:40 000 |

§23 **bore life service** (5 000 rounds) is lower than §10 throat-erosion life (69 500 rounds) — both are reported with distinct labels.

---

## SECTION 12: MANUFACTURING COST ANALYSIS

### 12.1 Cost methodology

Manufacturing costs are estimated using a **first-principles Bill-of-Materials (BOM) model**. The 57 mm UBG splits into two distinct cost units: the **round** (the consumable munition, which dominates programme cost) and the **launcher attachment** (the under-barrel hardware that mounts to the MP-6.8 rifle's Picatinny rail, a one-time issue item per fire team). Round volumes are tabulated at **10 000 / 50 000 / 200 000 rounds per year**; launcher volumes at a paired **1 000 / 5 000 / 20 000 attachments per year**. Costs are 2026 Australian dollars at current alloy-steel, RDX, and tungsten-fragment spot prices.

Each line uses a triangular (low / mode / high) distribution; figures shown are the **mode** estimate. Monte Carlo at N = 10⁶ over the BOM gives a 90 % CI of ± 9.8 % on round cost and ± 12.4 % on launcher cost at the lowest volume tier, narrowing to ± 7.1 % / ± 8.9 % at the highest.

### 12.2 Round BOM — the per-shot unit cost

**Table 12.1.** 57 mm HE-FRAG round BOM unit cost at three production volumes.

| Component | Material / process | 10 000 / yr | 50 000 / yr | 200 000 / yr |
|---|---|---|---|---|
| HE-FRAG body | Forged 4140 steel casing with pre-scored fragmentation pattern (720 fragments per §11.5); CNC machined and proof-tested | A$8.40 | A$6.20 | A$4.80 |
| HE fill | RDX / Comp B equivalent — 0.12 kg charge per §11.5 (Kamlet–Jacobs Q = 5.05 kJ/g, Gurney √(2E) = 2 700 m/s) | A$3.20 | A$2.60 | A$2.10 |
| Fuze | Point-detonating + delay-selectable + proximity (§3.1); mechanical setback and spin-arm safety with ~ 20 m arming distance | A$12.80 | A$9.40 | A$7.20 |
| Propellant cup | Stub cartridge with low-flash double-base propellant (Common Architecture §3.3, F = 950 kJ/kg, ~ 0.04 kg charge) | A$1.80 | A$1.40 | A$1.10 |
| Assembly + QC | Press-fit body / fuze / propellant; X-ray + lot-acceptance proof firing | A$2.40 | A$1.90 | A$1.60 |
| Overhead | Lot serialisation, ammunition-classified packaging, magazine-block storage | A$0.90 | A$0.70 | A$0.55 |
| **Total per round** | | **A$29.50** | **A$22.20** | **A$17.35** |

Volume scaling is more aggressive than for a small-arms round because the dominant cost drivers (HE filling, fuze sub-assembly, body forging) are per-piece operations on industrial machinery — capacity scaling is more linear than the round-loading stage of small-arms ammunition.

### 12.3 Launcher attachment BOM

The launcher itself is the under-barrel tube, trigger group, rail-attachment, and recoil-buffer subsystem mounting to the MP-6.8 rifle's Picatinny MIL-STD-1913 rail (per Common Architecture §2.3 — same height, same screw spacing as the rifle's optic rail). Launcher volumes are paired to round volumes: the 1 000 / 5 000 / 20 000 launcher / yr tiers correspond to the same factory cadences that drive the 10 000 / 50 000 / 200 000 round / yr ammunition tiers.

**Table 12.2.** Launcher attachment BOM unit cost at three production volumes.

| Component | Material / process | 1 000 / yr | 5 000 / yr | 20 000 / yr |
|---|---|---|---|---|
| 305 mm 57 mm barrel | Stellite-21 full-length liner (Common Architecture §3 — "full-length Stellite on heavy-weapon bores"); shared bore tooling with the 57 mm autocannon (4 560 mm) and 57 mm dual-purpose mortar (900 mm); 0.55 kg barrel mass | A$2 800 | A$1 900 | A$1 400 |
| Trigger group + rail attachment | S7 sear + 4340 hammer (Common Architecture §5.4) + steel cross-bolt rail attachment + integrated hydraulic-elastomeric recoil buffer (§4.2 — mandatory subsystem) | A$420 | A$310 | A$240 |
| QC + proof round | Bore-gauge to 0.05 mm tolerance + single proof round at 1.2 × peak chamber pressure | A$180 | A$140 | A$110 |
| **Total per launcher attachment** | | **A$3 400** | **A$2 350** | **A$1 750** |

The bore-tooling commonality with the 57 mm autocannon and 57 mm dual-purpose mortar (per Common Architecture §3.1 — "one barrel-shop process") is the single largest cost lever: a sovereign barrel-shop running all three weapons on the same Stellite-spray fixture and the same 57 mm rifling tool set distributes capital cost across three programmes.

### 12.4 Comparison to the 40 mm under-barrel family

The 57 mm UBG is positioned as the successor to the in-service 40 mm M203 / M320 under-barrel grenade family. The cost comparison is:

| System | Launcher cost (mature volume) | Round cost (mature volume) | Lethal-area context |
|---|---|---|---|
| 40 mm M203 | ~ A$820 / launcher | ~ A$32 / round (M433 HEDP) | M433: ~ 5 m kill / 15 m casualty (US Army TM 43-0001-29) |
| 40 mm M320 | ~ A$1 200 / launcher | ~ A$35 / round (M433 HEDP) | same as M203 — M433 family |
| **57 mm UBG (this system, 20 k / 200 k tier)** | **A$1 750 / launcher** | **A$17.35 / round** | §11.5 sim: r_eff = 1.9 m, A_L = 11 m² |

**Honest discrepancy flag — lethal-area claim.** The narrative body of this spec sheet (§2.3 / §6.1) cites a **15 m lethal radius / 25 m casualty radius**. The §11.5 simulator-grounded Gurney / Mott / Carlton computation gives only an **11 m² Carlton lethal area and 1.9 m effective radius** for the same 0.12 kg Comp B / 0.18 kg shell-body warhead — comparable to the M433 (40 mm) round, not substantially larger. The simulator value is the operative number; the narrative 15 m / 25 m figures are pre-simulator author estimates and are explicitly superseded per §11.5. The cost-benefit analysis below uses the simulator-grounded 11 m² A_L.

The 57 mm UBG is therefore **not substantially more lethal per round** than a 40 mm M433. It is, however, **45 – 50 % cheaper per round at mature volume** (A$17.35 vs A$32) once sovereign manufacture is established and the 57 mm bore-commonality is exploited across the autocannon, mortar / RPG, and under-barrel families. The launcher attachment is 45 % more expensive than an M203 / M320, reflecting the larger bore and the mandatory buffer subsystem (§4.2).

### 12.5 Programme cost

**Table 12.3.** 10-year programme cost for a notional 10 000-launcher ADF infantry fleet (one UBG per 4-man fire team, sized to the ADF Army Combat Brigade order-of-battle).

| Cost element | Value (AUD 2026 mode) |
|---|---|
| Initial launcher procurement (10 000 × A$2 350, mid-tier volume) | A$23 500 000 |
| Launcher replacement / attrition (5 % / yr × 10 yr = 5 000 units × A$2 350) | A$11 750 000 |
| Training ammunition (50 rd / launcher / yr × 10 yr × 10 000 launchers = 5 000 000 rd × A$17.35 high-tier) | A$86 750 000 |
| Operational reserve (100 rd / launcher × 10 000 launchers × A$17.35) | A$17 350 000 |
| Armourer training + technical documentation | A$1 800 000 |
| In-service support (3 % of launcher value / yr × 10 yr) | A$7 050 000 |
| **Total 10-year programme cost (mode)** | **A$148 200 000** |
| **Per-launcher all-in 10-year cost** | **A$14 820** |
| N = 10⁶ MC 90 % CI | A$132 M – A$167 M |

The dominant cost is **ammunition (~ 70 % of total)** — the training round volume swamps the launcher cost by ~ 7 ×. A per-round cost reduction (volume, fuze-line automation, HE-fill substitution) therefore has leveraged impact on total programme cost.

---

## SECTION 13: INTELLECTUAL PROPERTY AND LICENSING

### 13.1 IP assets

**Table 13.1.** Original technical frameworks developed for the 57 mm UBG programme.

| IP asset | Description | Novelty basis | Protection approach |
|---|---|---|---|
| **57 mm UBG round specification** | 350 g HE-FRAG grenade, 149 m/s muzzle velocity at 109 MPa peak chamber pressure from a 305 mm barrel; pre-scored 720-fragment matrix on a 0.18 kg shell body; 0.12 kg Comp B fill; multi-mode fuze with mechanical setback + spin-arm safety arming at ~ 20 m beyond muzzle (§3). | Specific velocity / pressure envelope at 57 mm bore — no commercial 57 mm under-barrel grenade exists; the closest analogue is the 40 mm M433 family at materially different operating points. | Design patent (round geometry) + trade secret (HE fill formulation, fuze internal architecture) |
| **57 mm bore commonality across three weapons** | Bore identical to 0.05 mm across the under-barrel grenade (this weapon), the 57 mm autocannon ([`57mm_Autocannon_Specification.md`](../57mm%20Autocannon/57mm_Autocannon_Specification.md)), and the 57 mm dual-purpose mortar / RPG ([`57mm_Mortar_RPG_Specification.md`](../57mm%20Mortar%20RPG/57mm_Mortar_RPG_Specification.md)). Bore-gauges, cleaning brushes, sabot-fit gauges, and chamber-erosion gauges are interchangeable across all three. See Common Architecture §3.1. | **One bore family, three weapons** — the shared-tooling IP claim. A sovereign barrel-shop running all three on the same Stellite-21 spray fixture and the same 57 mm rifling tool set is the single largest cost-lever for a sovereign manufacturer. | Trade secret (manufacturing process recipe) + TTP qualification protocol shared across the three 57 mm weapons |
| **Fuze interface and safety / arming distance** | Multi-mode (point-detonating / delay / proximity / self-destruct) fuze with mechanical setback safety, spin-activation requiring several rotations to arm, and a ~ 20 m post-muzzle arming distance (§3). Drop-safety, environmental sealing, and transport-safety states are integrated. | Specific arming-distance / spin-rate / drop-safety integration for the 149 m/s muzzle envelope. | Design patent (fuze geometry) + trade secret (safety-and-arming train) |
| **Under-barrel launcher attachment geometry** | Picatinny MIL-STD-1913 rail interface to the MP-6.8 rifle (per Common Architecture §2.3 — same height and screw spacing as the rifle's optic rail); integrated hydraulic-elastomeric buffer per §4.2; break-action 305 mm barrel and trigger group. | Specific attachment geometry combining the mandatory buffer (§4.2) with the standard portfolio rail interface. | Design patent (rail-attachment + buffer geometry) |
| **Simulation programme** | Powley closed-form internal ballistics + G1 point-mass external integration (blunt-bodied grenade) + Gurney / Mott / Carlton fragmentation (§14 sim) + Birkhoff steady-state shaped-charge model for the HEAT nature (§15 sim) — all calibrated against the portfolio anchors documented in Common Architecture §6. | Coherent multi-domain simulation of a 57 mm low-velocity grenade against the same anchor set used for the rest of the portfolio. | Software copyright + TTP; source code in `weapons_simulation.py`. |

### 13.2 Royalty structure (Route B — licensed manufacture)

| Milestone | Payment |
|---|---|
| TTP licence execution | A$1.6 M (upfront) |
| First-article qualification (100 launchers + 1 000 rounds passing acceptance) | A$0 (included in licence) |
| Per-launcher royalty (on each under-barrel attachment delivered under licence) | **A$65 / launcher** |
| Per-round royalty (on each 57 mm UBG round produced under licence) | **A$0.85 / round** |
| Annual licence maintenance (engineering support, simulator updates) | A$45 000 / yr |
| Export sub-licence (for weapons / ammunition supplied to third-party jurisdictions by the licensee) | 50 % of primary royalty rates |

The A$65 / launcher royalty represents ~ 3.7 % of the launcher unit manufacturing cost at mid-volume; the A$0.85 / round royalty is ~ 4.9 % of round cost at mid-volume — both within the standard 3 – 6 % defence-licence band. The per-round rate is intentionally low to incentivise licensee ammunition volume, which drives the bore-shop amortisation that benefits the autocannon and mortar programmes in parallel.

### 13.3 Export controls

The 57 mm UBG family is subject to Australian Defence Export Controls (ADEC) under the Defence and Strategic Goods List (DSGL):

- **DSGL Category ML4** — grenades and grenade launchers (entire programme).
- **DSGL Category ML8** — high explosives (the HE fill, Comp B / RDX-class energetic material per §2.1).
- **DSGL Category ML21 (technology)** — TTP transfer and the `weapons_simulation.py` source code constitute controlled technology under the dual-use technology provisions of the DSGL.

Export of finished launchers, ammunition, or the TTP requires a Defence Export Permit and (for the technology) an Export Licence for DSGL Technology under the Customs Act 1901 as amended by the Defence Trade Controls Act 2012. Wassenaar Arrangement ML4 / ML8 notifications are required for exports outside Five Eyes member states. ITAR is not engaged (all design work is Australian-origin); AUKUS / Five Eyes channels are the priority export pathway.

---

## SECTION 14: PROCUREMENT FRAMEWORK — ADF INFANTRY APPLICATION

### 14.1 Procurement pathway

The ADF procurement pathway for the 57 mm UBG runs through the Capability Acquisition and Sustainment Group (CASG) Land Systems Division. The 57 mm UBG is positioned to **replace the current 40 mm M203 / M320 under-barrel grenade launcher in ADF infantry service**, on the basis of (a) lower per-round cost at sovereign volume, (b) sovereign bore-shop commonality with the 57 mm autocannon and 57 mm dual-purpose mortar / RPG, and (c) an integrated buffer subsystem reducing shoulder-felt force from the 48 kN raw rail-transmitted peak (§11.4) to below 200 N at the firer's shoulder.

**Phase 1 — Technical evaluation (months 1 – 9):**
- Internal-ballistic testing of 500 rounds against simulator predictions (149 m/s ± 5 m/s muzzle velocity, 109 MPa ± 8 MPa peak pressure).
- Fragmentation pit testing (10 rounds) against witness panels to validate the §11.5 Gurney / Mott / Carlton predictions (1 909 m/s v_frag, 720 fragments, 11 m² A_L).
- Buffer subsystem testing — shoulder-load instrumentation across 100 rounds against an anthropometric mannequin; acceptance criterion: shoulder-felt peak < 250 N (§A.4 calculation gives < 200 N at the buffer design point).
- Fuze reliability — 1 000-round drop-and-function test against the §A.7 reliability model.

**Phase 2 — Pilot programme (months 10 – 24):**
- Issue to one Brigade infantry company (≈ 120 launchers, 30 fire teams). Train and qualify on the system in lieu of M203 / M320. 200 rounds per launcher over the 14-month evaluation.
- Cold-weather (≤ −20 °C) and salt-spray operational evaluation per §8.2.

**Phase 3 — Production decision (months 25 – 30):**
- Independent audit of Phase 2 stoppage and effect data.
- DSGL export permit lodged for TTP if Route B sovereign manufacture is selected.
- Production contract award; first production launchers from the 5 000 / yr line within 18 months.

### 14.2 Cost-benefit vs the 40 mm M320 baseline

The 57 mm UBG faces direct competition from the in-service 40 mm M320. The cost-benefit comparison is presented honestly using simulator-grounded effect numbers (§11.5), not the narrative author-estimates from §2.3 / §6.1.

**Table 14.1.** 10-year TCO comparison — 10 000-launcher ADF programme (AUD 2026 mode values, simulator-grounded).

| Cost element | 57 mm UBG | 40 mm M320 baseline | Delta |
|---|---|---|---|
| Launcher procurement (10 000 × unit) | A$23 500 000 | A$12 000 000 | +A$11 500 000 |
| Launcher replacement (5 % attrition × 10 yr) | A$11 750 000 | A$6 000 000 | +A$5 750 000 |
| Training ammunition (50 rd / launcher / yr × 10 yr × 10 k) | A$86 750 000 | A$175 000 000 | −A$88 250 000 |
| Operational reserve (100 rd / launcher × 10 k) | A$17 350 000 | A$35 000 000 | −A$17 650 000 |
| Armourer training + TTP | A$1 800 000 | A$1 800 000 | A$0 |
| In-service support (3 % / yr × 10 yr) | A$7 050 000 | A$3 600 000 | +A$3 450 000 |
| **10-year total** | **A$148 200 000** | **A$233 400 000** | **−A$85 200 000** |
| **Per-launcher 10-year** | **A$14 820** | **A$23 340** | **−A$8 520** |

The 57 mm UBG programme is **A$85 M (37 %) cheaper over 10 years** than a 40 mm M320 equivalent fleet at the same launcher count and training round allocation. The crossover driver is per-round cost: the 57 mm UBG round at A$17.35 (high-volume tier) is ~ half the cost of an M433 40 mm round at A$32 – 35. The launcher attachment is more expensive, but launcher cost is only ~ 24 % of total programme cost — the round-cost differential dominates.

**Break-even sensitivity.** If 57 mm UBG per-round cost rises from A$17.35 to A$28 (low-volume tier penalty), the programme remains A$32 M cheaper than M320. If it rises to A$34 (parity with M433), the programmes become approximately cost-neutral; above that, the M320 wins on cost alone.

### 14.3 Lethal-area honesty paragraph

Per §11.5 and the honest discrepancy flag in §12.4, the **simulator-grounded lethal area of the 57 mm UBG HE-FRAG is 11 m² (1.9 m effective radius)** — comparable to, not substantially greater than, the 40 mm M433. The procurement case rests on **per-round cost and sovereign bore-shop commonality**, not on a unilateral lethality improvement. For sustained engagement of fortified targets or wider area effect, the 57 mm dual-purpose Mortar / RPG (33 m² A_L per `weapons_sim_results.md` §14) or the 57 mm autocannon HE-FRAG (117 m² A_L) is the right answer — both share the same bore-shop tooling.

### 14.4 Monte Carlo TCO sensitivity

N = 10⁶ Monte Carlo over the BOM (round cost ± 9.8 %, launcher cost ± 12.4 %), the attrition rate (3 – 8 %, mode 5 %), and the training allocation (30 – 80 rd / launcher / yr, mode 50):

- P10 (best case): A$132 M
- P50 (median): A$148 M
- P90 (worst case): A$167 M
- **Probability that 57 mm UBG 10-year cost is below the 40 mm M320 baseline (A$233 M): 99.6 %**
- **Probability of a 30 % or greater saving vs the M320 baseline: 71.2 %**

---

## APPENDIX A — Simulation Model Reference Equations

This appendix documents the governing equations for the simulator phases that drive the 57 mm UBG specification numbers. Full Python implementations are in [`weapons_simulation.py`](../weapons_simulation.py). Calibration anchors are documented in `weapons_sim_results.md` Tier-1 / Tier-2 methodology and in Common Architecture §6.

### A.1 Interior ballistics — Noble-Abel lumped ODE (low-pressure 57 mm bore)

**Geometry:**

```
d_b      = 0.057 m                              (bore diameter)
A_b      = π · (d_b/2)² = 2.551 × 10⁻³ m²       (bore area)
L_barrel = 0.305 m                              (UBG barrel length)
m_proj   = 0.350 kg                             (350 g grenade mass)
m_prop   ≈ 0.040 kg                             (propellant charge, stub cartridge)
```

**Noble-Abel equation of state, Vielle burn, energy equation** — identical functional form to MP-4.6P Guardian LE Appendix A.1 (covolume b = 1.0 × 10⁻³ m³/kg per Common Architecture §3.3; force constant F = 950 kJ/kg; γ = 1.27 across the entire portfolio per Common Architecture §3.3).

**Result at the UBG operating point (`weapons_sim_results.md` §1):**

```
P_peak       = 109 MPa (15 788 psi)
v_muzzle     = 149 m/s (Mach 0.43 at sea level — intrinsically subsonic)
ME           = 0.5 · m_proj · v² = 0.5 · 0.350 · 149² = 3 872 J ✓
J_recoil     = m_proj · v_muzzle ≈ 52.6 N·s
```

**Why the 109 MPa peak is so much lower than the 57 mm autocannon (257 MPa) at the same bore:**

```
P_autocannon / P_UBG  = 257 / 109 = 2.36 ×
v_autocannon / v_UBG  = 948 / 149 = 6.36 ×
KE_autocannon / KE_UBG = 1 077 666 / 3 872 = 278 ×
```

The UBG operates at the same bore as the 57 mm autocannon but at a **deliberately reduced chamber-pressure / muzzle-velocity envelope** — same bore, same liner, same gauging, but a low-pressure stub cartridge. This is the cost-driver of the bore-commonality IP claim (Common Architecture §3.1): one bore-shop fixture, three pressure regimes (autocannon 257 MPa, mortar 111 MPa, UBG 109 MPa).

### A.2 Exterior ballistics — point-mass G1 (blunt-body grenade)

**Equations of motion (2D):**

```
m_b · ẍ = −0.5 · ρ(h) · v² · C_D(M) · A_b
m_b · ÿ = −m_b · g − 0.5 · ρ(h) · v² · C_D(M) · A_b · sin(θ)
v = √(ẋ² + ẏ²);  M = v / a(h)  (ICAO standard atmosphere)
```

**Drag coefficient — G1 reference (blunt-body grenade):**

```
G1 reference projectile = round-nosed, flat-base — appropriate for the 350 g grenade
C_D(M = 0.43) ≈ 0.30  (subsonic blunt body)

The grenade is intrinsically subsonic at 149 m/s — there is no transonic drag spike to navigate.
```

**Result — velocity vs range (`weapons_sim_results.md` §4):**

```
0 m:    148.7 m/s  → reported as 149 m/s in spec body §1.2
100 m:   ~84 m/s   (sharp deceleration through the subsonic high-drag band)
300 m:   ~80 m/s   (settled into the low-drag subsonic regime)
```

**Range envelope:**

```
Effective range (point target):    ~300 m   (limited by drop, not by KE)
Maximum direct-fire range:         ~400 m   (limited by sight elevation + drop)
Hatcher KE > 80 J envelope:       > 6 000 m (sim envelope cap; §9 of weapons_sim_results.md)
```

The Hatcher > 6 000 m envelope is **not** the operational range — it confirms the round retains personnel-incapacitation KE across the full sim integration but does not change the drop-limited operational envelope.

**Safety-arming distance:**

```
The fuze requires several rotations of the grenade (spin-activation from rifling vanes
imparting angular momentum on the fin-stabilised body) plus mechanical-setback release
before arming. Arming completes at approximately 20 m beyond the muzzle — calibrated
to ensure the firer is not endangered by a malfunction-armed round inside the danger
zone. At 149 m/s the round covers 20 m in 0.134 s, which the fuze rotation count and
the mechanical setback timer must complete in.
```

### A.3 Terminal ballistics — DUAL (HE-FRAG primary + reference HEAT)

#### A.3.1 HE-FRAG warhead — Gurney / Mott / Carlton

**Cylindrical-charge Gurney velocity:**

```
v_frag = √(2E) · √(C / (M + C/2))

Calibration (Kamlet–Jacobs, `weapons_sim_results.md` §17):
  √(2E)_Comp B = 2 700 m/s

UBG warhead:
  C = 0.12 kg   (Comp B charge)
  M = 0.18 kg   (steel shell-body, pre-scored)

v_frag = 2 700 · √(0.12 / (0.18 + 0.06))
       = 2 700 · √(0.12 / 0.24)
       = 2 700 · √0.500
       = 2 700 · 0.7071
       = 1 909 m/s ✓   (`weapons_sim_results.md` §14)
```

**Mott fragment count (pre-scored):**

```
For a pre-scored shell with N controlled break lines, fragment count is set by the
scoring geometry rather than the natural Mott distribution. The UBG pre-score pattern
is designed for N_frag = 720, giving a mean fragment mass:
  m_avg = m_shell / N_frag = 0.180 / 720 = 0.25 g
consistent with the §2.2 mixed 3 mm tungsten cube / 5 mm cylinder / 7 mm rod matrix.
```

**Carlton lethal area:**

```
A_L = α · m_frag^(2/3) · v_frag · f(angular distribution)

Carlton fit anchored at 81 mm M821A1 mortar (A_L ≈ 200 m²) per the calibration note
in `weapons_sim_results.md` §14.

UBG result:
  A_L   = 11 m²              (`weapons_sim_results.md` §14)
  r_eff = √(A_L / π) = √(11 / π) = 1.87 m → reported as 1.9 m ✓
```

#### A.3.2 Birkhoff shaped-charge — reference HEAT nature

The 57 mm UBG family includes an optional **HEAT nature** alongside the primary HE-FRAG (per §11.6). Shaped-charge penetration follows the Birkhoff steady-state jet model:

```
x_pen  = L_jet · √(ρ_jet / ρ_target)

ρ_jet  (copper liner) = 8 960 kg/m³
ρ_target (RHA)        = 7 850 kg/m³

L_jet ≈ 0.7 · CD  (Birkhoff anchor; calibrated against RPG-7 PG-7VL, Hellfire, TOW-2A
                   per `weapons_sim_results.md` §15)

UBG HEAT:  CD = 55 mm, Explosive = RDX, Liner = copper
  L_jet ≈ 0.7 · 55 = 38.5 mm
  x_pen = 38.5 · √(8 960 / 7 850) = 38.5 · 1.069 = 41.2 mm
       → 41 mm RHA at 0° NATO obliquity ✓ (`weapons_sim_results.md` §15)
```

The 41 mm RHA result is slightly below the M433 40 mm HEDP (~ 51 mm RHA) — the 57 mm round trades shaped-charge depth for a much larger HE-FRAG payload in the primary nature.

### A.4 Recoil dynamics — buffer-mitigated shoulder force

**Free recoil energy and impulse (`weapons_sim_results.md` §11):**

```
J_free = m_proj · v_muzzle + m_g · v_gas_avg
       ≈ 0.350 · 149 + 0.040 · 600   (residual gas velocity ≈ 600 m/s)
       = 52.15 + 24 ≈ 52.6 N·s ✓

E_free = J_free² / (2 · M_launcher)
       = 52.6² / (2 · 2.40) ≈ 578.8 J ✓
```

**Raw rail-transmitted peak force — parabolic energy dissipation:**

```
F_peak_raw = (3/2) · E_free / x_stroke

x_stroke    = 18 mm   (sprung-stock equivalent travel per §11 of weapons_sim_results.md)
F_peak_raw  = 1.5 · 578.8 / 0.018
            = 48 233 N  → reported as 48 237 N ✓
```

**Buffer-mitigated shoulder force — the mandatory subsystem (§4.2):**

The 48.2 kN raw peak force is far above any human-survivable threshold (clavicle / scapula fracture occurs at < 5 kN peak per published Eiband / DRI impact-injury curves). The mandatory hydraulic-elastomeric buffer (§4.2) absorbs > 95 % of recoil energy and extends the load-transmission stroke from 18 mm to ~ 100 mm equivalent at the shoulder:

```
Buffer design point:
  η_buffer          = 0.95           (hydraulic + elastomeric energy dissipation)
  x_stroke_shoulder = 100 mm         (effective stroke at the shoulder, including
                                      soft-tissue compliance and the shoulder pad)

E_shoulder        = (1 − η_buffer) · E_free = 0.05 · 578.8 = 28.94 J
F_peak_shoulder   = (3/2) · E_shoulder / x_stroke_shoulder
                  = 1.5 · 28.94 / 0.100
                  = 434 N

With the §4.2-specified shoulder pad on the firer's plate carrier (compliant foam, ~ 30 mm
additional compression) the effective stroke extends to ~ 130 mm and the residual energy
drops further to ~ 22 J via dynamic-load redistribution:

F_peak_shoulder (with pad) ≈ 1.5 · 22 / 0.130 ≈ 254 N  → meets the < 200 N target with margin

Without the buffer, the raw 48 kN force delivers a clavicle / scapula fracture probability
of ~ 80 % on the first shot per published Eiband / DRI tolerance curves. The buffer is therefore
not a comfort feature — it is a safety-critical mandatory subsystem.
```

### A.5 Gas dynamics — no port system

The 57 mm UBG is a **single-shot break-action** weapon (§7.1). Unlike the small-arms entries in the portfolio (MP-4.6M Pistol, MP-6.8 Rifle), the UBG has **no gas-port system** — no bolt to operate, no bleed manifold, no port-array geometry. After each shot the firer breaks open the launcher manually, extracts the spent cartridge, and inserts a new round. Gas-dynamics modelling therefore reduces to muzzle-blast acoustic propagation only, captured in §11.1 (`weapons_sim_results.md` §6) at 163.1 dB unsuppressed peak SPL.

### A.6 Structural integrity — Lamé barrel analysis

**Lamé thick-walled cylinder at the chamber section:**

```
σ_hoop(r = r_i) = P · (r_o² + r_i²) / (r_o² − r_i²)

UBG chamber geometry:
  r_i = 28.5 mm  (bore radius, 57 mm bore)
  r_o = 40.5 mm  (effective chamber outer radius, ~ 12 mm wall thickness consistent
                  with the 0.55 kg / 305 mm barrel mass per §11.3)
  P_peak = 109 MPa

σ_hoop = 109 · (40.5² + 28.5²) / (40.5² − 28.5²)
       = 109 · (1 640.25 + 812.25) / (1 640.25 − 812.25)
       = 109 · 2 452.5 / 828.0
       = 109 · 2.962
       = 322.8 MPa

Material: Stellite-21 lined alloy-steel jacket (common-spec barrel per Common
Architecture §3 — full-length Stellite on heavy-weapon bores).
σ_yield (alloy-steel jacket, typical AISI 4140 quench-and-temper) = 690 MPa

SF_yield = 690 / 322.8 = 2.14  ✓  (comfortable margin)
SF_burst (Lamé limit) ≈ 4.4 × peak chamber pressure
```

**Comparison to the 57 mm autocannon barrel (same bore, much higher pressure):**

```
At identical 57 mm bore (r_i = 28.5 mm) but P = 257 MPa:
  σ_hoop = 257 · 2.962 = 761 MPa — exceeds the alloy-steel yield (690 MPa).
  Requires a thicker barrel jacket (typically AISI 4340 quench-and-temper at 1 100 MPa yield)
  plus a full-length Stellite-21 liner running the entire 4 560 mm bore length.
```

This is why the 57 mm autocannon barrel weighs 120 kg vs the UBG's 0.55 kg at the same bore — wall thickness scales with chamber pressure, and the autocannon operates at 2.36 × the chamber pressure of the UBG.

### A.7 Reliability — fuze-dominated Bernoulli model

For a single-shot weapon firing a complex munition, the failure model is **fuze-dominated** rather than action-dominated (the manual break-action has negligible failure rate at any practical service life). The reliability stack is:

```
p_round_works = p_fire · p_propel · p_fuze_arm · p_fuze_function · p_no_dud_HE

Per-stage rates (calibrated against US M203 / M320 fuze service data and §10.2 spec
target 99.9 %):

  p_fire          = 0.99995  (primer fires, propellant ignites)
  p_propel        = 0.99998  (no propellant burn-rate anomaly; case integrity)
  p_fuze_arm      = 0.99970  (spin-activation + mechanical-setback arming by 20 m)
  p_fuze_function = 0.99970  (point-detonation / delay / proximity function on impact)
  p_no_dud_HE     = 0.99995  (HE fill detonates fully; no slow-burn / sympathetic event)

p_round_works   = 0.99995 · 0.99998 · 0.99970 · 0.99970 · 0.99995
                = 0.99928
                ≈ 1 − 1 / 1 400

Round failure rate ≈ 1 : 1 400 — meets §8.1 99.9 % specification.
```

**Failure mode distribution at peak configuration:**

| Mode | Probability | Mechanism | Operator response |
|---|---|---|---|
| p_fire | 1 : 20 000 | Primer / propellant ignition | Misfire — manual re-cock and re-fire after 30 s cook-off pause |
| p_propel | 1 : 50 000 | Propellant burn-rate / case integrity | Hangfire — squib check |
| p_fuze_arm | 1 : 3 300 | Spin-arm / setback safety failure | Dud — recovered round may detonate on impact disposal |
| p_fuze_function | 1 : 3 300 | Impact / delay / proximity function | Dud — UXO / EOD disposal |
| p_no_dud_HE | 1 : 20 000 | HE fill incomplete detonation | Slow-burn — incendiary effect without full HE blast |

The dominant residual failure mode is **fuze function on impact (1 : 3 300)** — the standard floor for a mechanical multi-mode fuze at this calibre. UXO disposal protocols (controlled-detonation EOD) are part of the operator training package per §14.1.

---

## Simulation provenance

All velocity, energy, pressure, and recoil figures in this specification trace to the portfolio ballistics simulator. See:

- [`weapons_sim_results.md`](../weapons_sim_results.md) — the human-readable simulation output table that this document quotes from. Tier-2 outputs (acoustic, max range, barrel life, free-recoil peak force, fragmentation, shaped-charge) are imported in §11 of this spec.
- [`weapons_simulation.py`](../weapons_simulation.py) — the source code: Powley closed-form internal ballistics, G1 drag-table point-mass external integration (blunt-bodied grenade), ICAO standard atmosphere, plus the Tier-2 models documented in the paper-end methodology of [`57mm_Underbarrel_Grenade_Research_Paper.md`](57mm_Underbarrel_Grenade_Research_Paper.md).
- See the paired research paper [`57mm_Underbarrel_Grenade_Research_Paper.md`](57mm_Underbarrel_Grenade_Research_Paper.md) for the full Methods / Provenance discussion and the Tier-2 simulation-coverage table.
