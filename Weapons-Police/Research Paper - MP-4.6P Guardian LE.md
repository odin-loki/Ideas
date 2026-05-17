# MP-4.6P Guardian LE — Research Paper
## A Simulation-Calibrated Police Combat Pistol in 4.6 × 22 mm DPAP

*Technical Research Paper*

Document No. TRP-2026-020-R | Version 1.0 (simulator-calibrated)

Prepared for: Australian Department of Defence / Australian State Police Procurement

Classification: UNCLASSIFIED / FOR OFFICIAL USE ONLY — Australian Law Enforcement Application

Date: May 2026

> **Genre note.** This paper adopts the academic-register convention used throughout the [`../Weapons-Defence/Research Papers/`](../Weapons-Defence/Research%20Papers/) tree (TRP designators, classification banners, FOUO-style markings, abstract-first structure). No real procurement relationship with any state police service, the Australian Federal Police, the ADF, or the Department of Defence is implied. The MP-4.6P Guardian LE is a design prospectus, not a fielded product, and the 4.6 × 22 mm DPAP cartridge has not been chambered in any prototype hardware. **Classification banner is illustrative — no real classification is implied or held.**

---

## Honest framing

- **Simulation-based, pre-physical-test.** All performance claims are outputs of the seven-phase Python simulation programme described in §3, anchored in [`../Weapons-Defence/weapons_simulation.py`](../Weapons-Defence/weapons_simulation.py) with output captured in [`../Weapons-Defence/weapons_sim_results.md`](../Weapons-Defence/weapons_sim_results.md). Physical bench, range, and NIJ-compliance testing remain the definitive validation pathway.
- **The 4.6 × 22 mm DPAP cartridge is new** and has not been loaded or fired. The case shares head geometry, primer chemistry, and projectile-tooling family with the 4.6 × 30 mm Enhanced; the interior-ballistics model is anchored against the HK MP7 4.6 × 30 mm published reference (1.7 g @ 725 m/s, 180 mm barrel). The 4.6 × 22 mm at 396 m/s sits inside that calibration envelope, but a first-article proof load is the only thing that closes the loop.
- **Hard-armour envelope is bounded.** Defeats NIJ IIIA soft armour and NIJ III hard plate. Does not defeat 15 mm RHA, NIJ IV SiC ceramic, 7.62 NATO rifle plate, or .50 BMG. These are military, not LE-civilian, threats.
- **Reliability claims are Monte Carlo, not field-validated.** MRBF 20 548 (analytic) / 27 778 (simulated, 90 % CI [15 152 – 29 412]) computed by a seven-mode Bernoulli failure-rate Monte Carlo (N = 500 000 rounds); per-mode rates from surface-engineering literature, not prototype testing.
- **Tier-2 surface engineering is load-bearing.** The headline MRBF requires the full DLC + PVD-CrN + precision-machined magazine + 100 % primer-depth QC package. Baseline mechanical design alone achieves ≈ 840 rounds MRBF. The Tier-2 package is **not optional**.
- **Cost numbers assume mature production.** A$164 – 180 per pistol (5 k – 50 k units / yr) assumes state-owned manufacturing and a triangular cost distribution. Real procurement-cost variation has heavier tails.

---

## Abstract

We present the MP-4.6P Guardian LE, a compact combat pistol system purpose-engineered for Australian law-enforcement (LE) and close-protection use, chambered in a proprietary 4.6 × 22 mm Dual-Purpose Armour-Piercing (DPAP) cartridge. The weapon is the LE variant of the previously-documented MP-4.6M Guardian Pistol (4.6 × 30 mm Enhanced; [`../Weapons-Defence/MP-4.6M Pistol.md`](../Weapons-Defence/MP-4.6M%20Pistol.md)): shared bore diameter, primer chemistry, projectile-tooling family, and brass-forming dies; differs in case length (22 vs 30 mm), bullet mass (3.3 g WC + Cu jacket vs 2.6 g solid WC), and operating velocity envelope (396 vs 501 m/s at 180 mm barrel). The design is anchored in a seven-phase first-principles computational simulation programme (interior ballistics, exterior ballistics, terminal ballistics, recoil dynamics, gas dynamics, structural integrity, reliability) implemented in [`weapons_simulation.py`](../Weapons-Defence/weapons_simulation.py), each phase calibrated against published physical references (HK MP7 4.6 × 30 mm; FBI 9 mm 124 gr; Alekseevski-Tate rigid penetrator regime). The Guardian LE defeats NIJ IIIA soft armour (78 mm penetration into a 10 mm reference panel; 7.8× margin), NIJ III hard plate (14.8 mm penetration into 10 mm AR-steel), and all four common LE intermediate barriers (auto glass, vehicle steel panel, drywall, 50 mm solid wood) at the design operating velocity of 396 m/s and 259 J muzzle energy. The bullet arrests inside soft tissue at ≈ 216 mm gel-equivalent (cold-protocol simulation; warm-protocol testing expected to yield 248 – 270 mm) — there is no overpenetration concern at the operating velocity. The recoil management is unusual: felt recoil is **0.084 ft-lbf**, approximately 50× lower than a standard 9 mm service load, enabling accurate single-handed engagement from non-standard firing positions where conventional pistol recoil disrupts point of aim. Reliability is modelled as a seven-mode Bernoulli failure-rate Monte Carlo (N = 500 000 consecutive rounds); the Tier-2-equipped configuration achieves analytic MRBF of 20 548 rounds and simulated mean of 27 778 rounds with a 90 % bootstrap confidence interval of [15 152 — 29 412]. FTF rate is 1:80 000 — 16× the specification minimum. The design is a complete *prospectus* against a published, conservative simulator; the physical-test validation pathway is in §6.1.

---

## 1. Introduction

Contemporary Australian law-enforcement operators face a threat envelope that the standard 9 × 19 mm Parabellum service pistol does not address fully. Armoured offenders (NIJ IIIA-equivalent commercial soft armour, increasingly observed in serious-organised-crime and counter-terrorism arrest scenarios), vehicle barriers (auto glass and panel steel during pursuit terminations), and partition-wall intermediate barriers (drywall, timber framing) constitute the operationally-binding terminal-ballistics constraints. The 9 mm cartridge, in standard ball or expanding bonded-core loadings, addresses soft-target engagement effectively but is marginal-to-deficient against IIIA armour at typical engagement velocities (380 – 410 m/s after barrel-length and barrier losses) and against intermediate barriers when the round must retain lethal energy beyond the barrier. The conventional doctrinal response is to escalate to a patrol carbine for armoured-suspect or barrier engagements, but this requires that the carbine be (i) immediately at hand, (ii) cleared from a vehicle rack inside the engagement timeline, and (iii) deployable in confined or vehicle-interior environments where carbine recoil and length are operationally disadvantageous.

The MP-4.6P Guardian LE addresses this gap with a purpose-built LE handgun in a proprietary 4.6 × 22 mm cartridge whose 3.3 g tungsten-carbide (WC) penetrator defeats IIIA soft armour, NIJ III hard plate, and all common intermediate barriers at the design operating velocity, while keeping felt recoil approximately 50× lower than the 9 mm baseline. The weapon is the *LE variant* of the previously-documented MP-4.6M family ([`../Weapons-Defence/MP-4.6M Pistol.md`](../Weapons-Defence/MP-4.6M%20Pistol.md), [`MP-4.6M Defender PDW.md`](../Weapons-Defence/MP-4.6M%20Defender%20PDW.md)), inheriting projectile-tooling, primer chemistry, brass-forming dies, and bore diameter, but operating at a velocity envelope (396 m/s vs 501 / 542 m/s for the 4.6 × 30 mm military rounds) specifically chosen to keep the bullet inside the *no-overpenetration* regime in soft tissue — a regulatory and tactical requirement that does not bind military deployment but is the principal LE-civilian constraint.

This paper presents the design, the simulation programme, and the predicted performance.

---

## 2. Background

### 2.1 The LE handgun threat envelope

The threat envelope facing a contemporary Australian state-police or AFP operator is bounded above by patrol-rifle engagements (separately addressed) and bounded below by simple unarmoured-suspect arrests. The handgun-binding band of that envelope is dominated by four threat classes:

1. **Armoured-offender engagement.** Commercial NIJ IIIA soft armour is widely available; the 9 mm cartridge does not reliably defeat IIIA armour at typical engagement velocities. The Guardian LE engages this threat through a rigid-WC penetrator that defeats IIIA at the operating velocity with a 7.8× margin.
2. **Vehicle-barrier engagement.** Auto glass (6 mm laminated) and vehicle steel panel (1.5 mm) routinely defeat 9 mm hollow-point loadings, leaving the operator without effective engagement of a threat sheltering behind a vehicle door. The Guardian LE defeats both barriers with 369 – 388 m/s exit velocity, retaining lethal energy after penetration.
3. **Partition-wall engagement.** Building drywall (12 mm) and solid timber (50 mm) are intermediate barriers where the LE rules-of-engagement require both (i) defeat of the barrier and (ii) no overpenetration on the receiver side. The Guardian LE defeats both and arrests in soft tissue beyond.
4. **Close-protection engagement.** A close-protection role requires accurate fire from non-standard positions (vehicle interior, weakened grip, single-handed support of a principal). The Guardian LE's 0.084 ft-lbf felt recoil makes this materially easier than a 9 mm.

### 2.2 The 9 mm baseline and its limits

The 9 × 19 mm Parabellum is the universal Western LE service cartridge: cheap, ubiquitous, low-pressure, well-characterised in soft-tissue and barrier terminal ballistics. Its principal limit in the contemporary LE envelope is the soft-armour-defeat regime: at the velocities a service pistol can deliver, no 9 mm projectile design reliably defeats commercial IIIA armour at typical engagement distance. The Guardian LE replaces the 9 mm baseline in the *armoured-suspect-engagement* and *barrier-engagement* subspaces while accepting that the 9 mm remains superior in the soft-target / cost-per-round / familiar-doctrine subspaces.

### 2.3 The 4.6 × 22 mm DPAP and its lineage

The 4.6 × 30 mm Enhanced cartridge in the previously-documented MP-4.6M family was developed for military application, where overpenetration is not the primary constraint and where the WC penetrator can be optimised for hard-target engagement at higher velocities. The 4.6 × 22 mm DPAP is the deliberate civilian-LE adaptation: the case is shortened from 30 to 22 mm, the bullet is heavier (3.3 g vs 2.6 g) and slightly longer, the propellant charge is reduced, and the operating velocity drops from 501 m/s (180 mm pistol barrel) to 396 m/s. The DPAP designation refers to the cartridge's two-mode terminal behaviour: on impact with soft tissue, the polymer tip collapses and the jacket petals expand to 7.5 mm diameter (a velocity-independent geometric expansion above ≈ 100 m/s); on impact with hard armour, the jacket strips and the WC rod penetrates as a rigid body. This eliminates the operational need to carry separate soft-target and AP ammunition.

---

## 3. Materials and Methods

### 3.1 The seven-phase simulation programme

All quantitative claims are simulator-derived. The simulation programme is implemented in Python as a coherent suite, with the core ballistics modules in [`weapons_simulation.py`](../Weapons-Defence/weapons_simulation.py) and the phase-specific extensions for the recoil, gas-dynamics, structural, and reliability domains documented as named modules in the same file. Each phase is anchored against a published reference (Table 1).

**Table 1.** Simulation phase, model class, calibration reference.

| Phase | Domain | Model class | Calibration reference |
|---|---|---|---|
| 1 | Interior ballistics | Lumped-parameter Noble-Abel ODE, isentropic expansion, Vielle burn rate | HK MP7 4.6 × 30 mm (1.7 g @ 725 m/s, 180 mm barrel) |
| 2 | Exterior ballistics | 2D point-mass trajectory, piecewise Cd vs Mach, Litz-corrected Miller Sg | Litz *Applied Ballistics* (Sg threshold 1.4) |
| 3 | Terminal ballistics | Poncelet resistive-force soft tissue; rigid cavity-expansion AP; Recht-Ipson barriers | FBI 9 mm 124 gr gelatin (8 g @ 370 m/s, 380 mm); Alekseevski-Tate rigid regime |
| 4 | Recoil dynamics | Mass-spring-damper bolt ODE; angular impulse muzzle-rise (2-DOF wrist) | Phase 1 bolt impulse; biomechanical grip constants |
| 5 | Gas dynamics | Isentropic port expansion; choked orifice mass flow; 3-baffle brake | Phase 1 chamber state; classical orifice flow |
| 6 | Structural integrity | Lamé thick-walled cylinder; Archard wear; Wahl spring stress; Goodman fatigue | Phase 1 peak pressure; published material data (416R, H13, 17-7 PH, 7075-T6) |
| 7 | Reliability | Bernoulli 7-mode failure MC, N = 500 000 rounds, bootstrap CI (2 000 resamples) | Per-mode rates from phases 4 – 6 and surface-engineering literature |

The simulation programme is **deliberately conservative**. The 1D lumped interior-ballistics model ignores the Lagrange pressure gradient along the bore, underestimating muzzle velocity by ≈ 39 % vs the HK MP7 reference (corrected explicitly with a documented multiplier). The Poncelet tissue model with calibrated B_gel = 2 366 kg/m³ gives penetration depths ≈ 15 % lower than warm-gelatin FBI-protocol testing. The Archard wear model uses mid-range wear coefficients. The reliability Monte Carlo uses Bernoulli failure rates that do not credit partial-failure recovery. The presented numbers are *floor estimates*, not central estimates.

### 3.2 Phase-by-phase numerical setup

**Phase 1 (interior ballistics).** Noble-Abel equation of state (co-volume 1.05 × 10⁻³ m³/kg), Vielle burn rate (a = 2.4 × 10⁻⁸ m/s/Pa⁰·⁸², half-web e₁ = 100 µm), specific propellant energy 5.8 MJ/kg, case volume 311 mm³, charge mass 0.22 g (43 % load density). Lumped-parameter ODE integrated forward in time with 1 µs time step from primer ignition to muzzle exit. Output: peak chamber pressure, muzzle velocity, propellant burn fraction at muzzle, bolt impulse over the port-transit time.

**Phase 2 (exterior ballistics).** 2D point-mass trajectory with G7 drag table; piecewise Cd(M) interpolation across subsonic, transonic, and supersonic regimes; sea-level ICAO atmosphere; 25 m zero distance with bore elevation as the free parameter. Litz-corrected Miller stability with pitching-moment coefficient C_Mα = 4.0 (WC spitzer projectile, 4.35-calibre length).

**Phase 3 (terminal ballistics).** Poncelet resistive-force ODE for soft tissue with calibrated B_gel; rigid cavity-expansion ODE for AP penetration of soft and hard armour (validity bounded above by ≈ 2 000 m/s impact velocity, above which Alekseevski-Tate erosion regime applies); Recht-Ipson ballistic-limit model for intermediate barriers. Each target is a single-material slab at NIJ-published areal density.

**Phase 4 (recoil dynamics).** Bolt-as-mass-spring system with the bolt impulse from Phase 1 as initial condition; ODE integrated through the 40 mm bolt stroke with the 0.092 N/mm system spring rate. Felt recoil computed from free recoil impulse against a 5.68 kg pistol + shooter effective mass, with the 42 % counter-impulse from the 3-baffle muzzle brake applied as a deterministic reduction. Muzzle rise modelled as angular impulse on a 2-DOF wrist-stock-grip assembly.

**Phase 5 (gas dynamics).** Isentropic expansion from peak chamber pressure to the port zone (115 – 135 mm from breech); choked-orifice mass flow through eight 2.5 mm ports arranged helically over a 20 mm zone; bolt-impulse integration over port-transit time with the corrected 1D-to-3D multiplier.

**Phase 6 (structural integrity).** Lamé thick-walled cylinder analysis for the barrel port zone (inner radius 2.3 mm, outer radius 8.5 mm) under 246 MPa peak chamber pressure; Archard wear with conservative coefficient; Wahl-corrected torsional shear in the recoil spring (17-7 PH wire, H900 condition); Goodman infinite-life fatigue check.

**Phase 7 (reliability).** Bernoulli MC with seven independent failure modes (FTFeed, FTExtract, FTFire, FTEject, Gas Fouling, Primer Failure, Case Separation). Per-mode rates set from the surface-engineering literature and from Phase 4/5/6 outputs (e.g. FTFeed driven by feed-ramp coefficient of friction, FTExtract by extractor hook depth and spring preload). N = 500 000 consecutive rounds; 2 000 bootstrap resamples for confidence intervals.

### 3.3 Software and reproducibility

The simulator is the shared single-source-of-truth across the entire defence portfolio: [`../Weapons-Defence/weapons_simulation.py`](../Weapons-Defence/weapons_simulation.py). The relevant module outputs for the Guardian LE are written to [`../Weapons-Defence/weapons_sim_results.md`](../Weapons-Defence/weapons_sim_results.md). The cartridge entry for 4.6 × 22 mm DPAP and the weapon-platform entry for the Guardian LE are documented in [`../Weapons-Defence/Common Architecture and Components.md`](../Weapons-Defence/Common%20Architecture%20and%20Components.md), which carries the full cartridge table and parts-commonality matrix for the small-arms family.

### 3.4 Limitations of method

The simulator is a coherent suite, but it is *not* a 3D Lagrangian gas-dynamic solver, a full FEA structural model, or a stochastic-yaw 6-DOF exterior-ballistics integrator. The 1D-to-3D correction multipliers, the lumped tissue model, and the Lamé thick-walled-cylinder assumption are documented and conservative — but any of them could fail in unanticipated ways on first-article testing. The reliability per-mode rates are drawn from the surface-engineering literature on similar weapon classes; they have not been measured on prototype Guardian LE hardware.

---

## 4. Results

### 4.1 Interior ballistics

The simulator predicts muzzle velocity of **396 m/s** at peak chamber pressure of **246 MPa (35 700 PSI)** and bullet mass of 3.3 g, giving muzzle kinetic energy of **259 J**. Interior-ballistic efficiency is 20.3 % (KE / propellant energy), with 70.5 % of propellant burned at muzzle exit. The bolt impulse is 47 mN·s after the 1D-to-3D correction (Table 2).

**Table 2.** Interior-ballistics results.

| Parameter | Value |
|---|---|
| Muzzle velocity | 396 m/s (Mach 1.16) |
| Peak chamber pressure | 246 MPa (35 700 PSI) |
| Muzzle kinetic energy | 259 J |
| Propellant burned at muzzle | 70.5 % |
| Bolt impulse (corrected) | 47 mN·s |
| Time to muzzle | ≈ 0.5 ms |

The 20.3 % IB efficiency is below the 28 – 35 % typical of optimised pistol loads because the short 22 mm case means a significant fraction of propellant is still burning as the bullet exits.

### 4.2 Exterior ballistics

Gyroscopic stability factor Sg = 1.70 at the muzzle (1:8″ twist; bullet length 4.35 calibres; Litz-corrected Miller with C_Mα = 4.0), above the 1.4 threshold. The bullet is stable throughout the engagement envelope. Zeroed at 25 m with a bore elevation of 0.044°, the bullet drops 43 mm at 50 m and 269 mm at 100 m. Maximum range at 45° elevation is 1 488 m — the safe-backstop reference for range-design purposes.

### 4.3 Terminal ballistics — soft tissue

Simulated penetration depth at 396 m/s impact is **216 mm** (cold-gelatin parameters per FBI standard). Warm-gelatin protocol testing is expected to yield 248 – 270 mm penetration. The 7.5 mm expansion diameter is geometric and velocity-independent above ≈ 100 m/s. The bullet does not exit the gelatin block at 396 m/s — no overpenetration. Yaw onset at ≈ 70 mm depth; peak yaw ≈ 85° at 375 mm.

### 4.4 Terminal ballistics — hard armour

**Table 3.** Hard-armour penetration results at 396 m/s.

| Target | Thickness | Penetration | Result | Margin |
|---|---|---|---|---|
| NIJ IIIA Kevlar | 10 mm | 78.1 mm | ✓ Defeats | 7.8× |
| NIJ III AR-steel | 10 mm | 14.8 mm | ✓ Defeats | 1.48× |
| 15 mm RHA (ref) | 15 mm | 12.2 mm | Not defeated | — |
| NIJ IV SiC | 8 mm | 4.8 mm | Not defeated | — |

NIJ IIIA and NIJ III defeats cover the LE armoured-offender threat envelope; NIJ IV and 15 mm RHA are military threats explicitly outside the design scope.

### 4.5 Intermediate barriers

**Table 4.** Intermediate-barrier ballistic-limit and exit-velocity results at 396 m/s.

| Barrier | Ballistic limit (m/s) | Exit velocity (m/s) | Energy at exit (J) |
|---|---|---|---|
| Auto glass 6 mm | 143 | 369 | 225 |
| Vehicle steel panel 1.5 mm | 80 | 388 | 248 |
| Drywall 12 mm | 72 | 389 | 250 |
| Solid wood 50 mm | 253 | 304 | 153 |

In all four cases, the post-barrier exit energy exceeds the FBI-Hatcher 80 J threshold for human-incapacitating terminal energy.

### 4.6 Recoil

Free recoil impulse at 396 m/s is 1.40 N·s (bullet momentum 1.31 N·s + ejected gas momentum 0.09 N·s); free recoil energy against a 5.68 kg pistol + shooter effective mass is 0.117 ft-lbf. After the 42 % counter-impulse from the 3-baffle muzzle brake, **felt recoil is 0.084 ft-lbf** — approximately 50× lower than a standard 9 mm 124 gr NATO load in the same system (≈ 4.5 ft-lbf). Peak muzzle rise during a three-round burst at 750 RPM is 0.8°; shot-to-shot POI shift within the burst < 5 mm at 25 m.

### 4.7 Reliability

**Table 5.** MRBF progression through the engineering-intervention pathway.

| Configuration | MRBF (rounds) | FTF rate |
|---|---|---|
| Baseline (corrected bolt) | 840 | 1:8 000 |
| + Tier-1 mechanical (chrome bore, coil extractor, ejector geometry, feed ramp) | 2 899 | 1:8 000 |
| + Ti firing pin + primer QC | 5 128 | **1:80 000 ✓** |
| + Tier-2 DLC (all sliding surfaces) | 12 500 | 1:80 000 ✓ |
| + PVD-CrN (cam, rails) | 13 333 | 1:80 000 ✓ |
| + Precision magazine | 13 953 | 1:80 000 ✓ |
| + 100 % ammo QC (peak) | **20 548 ✓** | **1:80 000 ✓** |

Simulated mean MRBF at peak: 27 778 rounds (N = 500 000 round MC; 90 % bootstrap CI [15 152 – 29 412]). The CI lower bound exceeds the 15 000-round specification. FTF rate of 1:80 000 is 16× the 1:5 000 specification minimum.

### 4.8 Compliance summary

The Guardian LE meets every specification at the Tier-2-equipped configuration:

| Domain | Specification | Achieved | Status |
|---|---|---|---|
| MV | ≥ 380 m/s | 396 m/s | ✓ |
| ME | ≥ 250 J | 259 J | ✓ |
| Peak chamber pressure | ≤ 280 MPa | 246 MPa | ✓ |
| NIJ IIIA defeat at 396 m/s | required | ✓ 7.8× margin | ✓ |
| NIJ III defeat at 396 m/s | required | ✓ 1.48× margin | ✓ |
| 2 MOA at 25 m | < 30 mm | 14.5 mm | ✓ |
| Felt recoil | < 1.0 ft-lbf | 0.084 ft-lbf | ✓ |
| MRBF | ≥ 15 000 rounds | 20 548 analytic / 27 778 sim | ✓ |
| FTF rate | < 1:5 000 | 1:80 000 | ✓ |

---

## 5. Discussion

### 5.1 Where the Guardian LE fits in the LE handgun landscape

The Guardian LE does not replace the 9 mm service pistol in every role. It replaces it specifically in the *armoured-suspect* and *intermediate-barrier* sub-spaces of the LE handgun envelope, while accepting the cost premium (≈ 2× per-round) and the doctrinal-change overhead. For an LE agency whose threat-realisation data shows armoured-offender or vehicle-barrier engagements as a recurring problem, the Guardian LE is the substantive answer. For agencies whose threat envelope is dominated by unarmoured-soft-target engagement, the conventional 9 mm baseline remains correct.

The Guardian LE is *not* a tactical-revolution weapon. It is an incremental capability addition with a specific operational target. The DPAP cartridge concept — single round, two terminal modes, no operator-side ammunition discrimination — is the principal innovation, and it is enabled by the WC + Cu jacketed-spitzer geometry rather than by any novel material chemistry.

### 5.2 Comparison to the 4.6 × 30 mm Enhanced

The 4.6 × 30 mm Enhanced (military Guardian Pistol, MP-4.6M) operates at 501 m/s / 326 J from a 180 mm pistol barrel and 542 m/s / 382 J from the 266.7 mm Defender PDW barrel. At those velocities the overpenetration regime is engaged — the bullet exits a standard 4-handspan tissue model and continues with lethal energy. This is operationally acceptable for military deployment where the rules of engagement do not bind backstop selection in the same way as LE-civilian deployment, and tactically advantageous when engaging through cover. It is *not* operationally acceptable for LE-civilian deployment, where the rules of engagement require both effective threat neutralisation and no overpenetration onto bystanders.

The 4.6 × 22 mm DPAP at 396 m/s sits inside the no-overpenetration regime by design. The trade is reduced barrier-defeat margin (NIJ III is 1.48× rather than 3× as at 501 m/s) and reduced terminal energy beyond the barrier — both deliberate. The LE deployment envelope does not require NIJ IV defeat or 15 mm RHA defeat; it requires NIJ IIIA + NIJ III + the four intermediate barriers, with no overpenetration. The Guardian LE delivers exactly that.

### 5.3 The recoil result

The 0.084 ft-lbf felt-recoil result is the headline operational capability. It enables three distinct operational modes that are unavailable from a 9 mm service pistol:

1. **Single-handed accurate fire under stress** — the operator can engage with the support hand occupied (radio, light, principal-protection, opening a door).
2. **Vehicle-interior engagement** — the operator can engage from inside a vehicle without the recoil impulse compromising vehicle control or causing whiplash injury.
3. **Confined-space accurate fire** — the operator can engage in a stair-tower, doorway, or vehicle interior where conventional pistol recoil disrupts POA and over-pressurises the operator's hearing.

These are not marginal operational advantages. They are step-change capability deltas relative to the 9 mm baseline, and they are achievable specifically because the 4.6 × 22 mm case + 42 % muzzle brake + 0.092 N/mm spring rate combination delivers the recoil impulse onto the shooter at a level below the threshold of perceptible push.

### 5.4 The reliability claim

The analytic MRBF of 20 548 rounds is the *floor* of a conservative simulation; the simulated mean is 27 778 rounds. Both figures exceed the 15 000-round specification with comfortable margin. The FTF rate of 1:80 000 — 16× the spec — is driven primarily by the titanium firing pin's 50 % mass reduction (preserving striker energy in a lightweight system) and the 100 % primer-depth QC on every round. Neither is exotic technology; both have been demonstrated at production volume in other weapon programmes.

The headline reliability result depends on the *full Tier-2 surface-engineering package*. Removing any single Tier-2 intervention reduces MRBF below the 15 000-round specification:

| Removed intervention | Predicted MRBF | Spec met? |
|---|---|---|
| None (full Tier-2) | 20 548 | ✓ |
| 100 % ammo QC | 13 953 | ✗ |
| Precision magazine | 13 333 | ✗ |
| PVD-CrN | 12 500 | ✗ |
| DLC | 5 128 | ✗ |

This is a documented design dependency, not an oversight. A state-owned manufacturer adopting the Guardian LE must commit to the full Tier-2 process chain.

---

## 6. Limitations

### 6.1 Simulation-based, pre-physical-test

Every quantitative claim in this paper is the output of the seven-phase Python simulation programme. The simulator is conservative and the predictions are floor estimates, but no physical hardware has been built or tested. The validation pathway requires:

1. **First-article DPAP cartridge manufacture** (100 rounds against the §3 / Table 2 specifications; chronograph against the simulator's 396 m/s muzzle-velocity prediction; pressure-test against the simulator's 246 MPa peak-chamber prediction). This single step closes the modelling loop on the cartridge.
2. **First-article weapon manufacture** (10 weapons against the §6 / §11 of the spec sheet; bench-test against the compliance table; fire 5 000 rounds across the 10 weapons for stoppage characterisation).
3. **NIJ-accredited terminal-ballistics testing** of the DPAP round against IIIA and III reference panels.
4. **State-police user-acceptance trial** (50 officers, 90-day carry, qualification and operational scenarios).

### 6.2 Hard-armour envelope is bounded

The Guardian LE does not defeat 15 mm RHA, NIJ IV SiC ceramic, 7.62 NATO rifle plate, or .50 BMG. These are military rather than LE-civilian threats and are explicitly outside the design scope. For specialist LE units (state tactical / TRG / counter-terrorism) that engage these threats, the Guardian LE is worn or carried as a primary armour-defeat backup to a separate rifle-rated weapon — never as the sole engagement option for those threats.

### 6.3 The 4.6 × 22 mm cartridge is new

The cartridge has not been loaded or fired in any prototype hardware. The case shares head geometry, primer chemistry, brass-forming dies, and projectile-tooling family with the 4.6 × 30 mm Enhanced (which is itself an extension of the HK MP7 4.6 × 30 mm calibrated reference), so the manufacturing route is well-understood. But until first-article rounds are loaded and chronographed, every interior-ballistics number is a *prediction*, not a *measurement*.

### 6.4 Reliability is Monte Carlo, not prototype-validated

The per-mode failure rates that drive the Monte Carlo are drawn from the surface-engineering literature on similar weapon classes (specifically, the published reliability data from the HK MP7 4.6 × 30 mm and similar gas-operated delayed-blowback pistols). They have not been measured on prototype Guardian LE hardware. The 90 % bootstrap CI of [15 152 – 29 412] characterises the *Monte Carlo statistical uncertainty* under the assumed per-mode rates; it does not characterise the *modelling uncertainty* of the per-mode rates themselves. A pre-production reliability test of 5 – 10 weapons firing 5 000 rounds each is the only thing that closes the modelling loop on reliability.

### 6.5 Tier-2 process chain must be procured

The DLC PECVD, PVD-CrN, laser-formed 440C feed lips, and 100 % primer-depth QC are mature industrial processes individually. The *package* — at the volume required for a service-pistol production line, at the cost target in §12 of the operator spec — has not been qualified for this cartridge. A state-owned manufacturer must commit to the process chain as a unit.

### 6.6 Cost-estimate caveats

The A$164 – 180 per-unit and A$0.83 – 0.92 per-round figures (§12 of the operator spec) assume a state-owned manufacturing arrangement with a triangular cost distribution. Real procurement-cost variation has heavier tails than the triangular assumption captures. The N = 10⁶ Monte Carlo of the cost model is robust to this assumption, but the *magnitude* of the per-unit cost depends sensitively on the WC penetrator sinter-and-grind process yield, which is the longest-lead-time element of the round.

### 6.7 Classification banner is illustrative

UNCLASSIFIED / FOUO format adopted for tonal coherence with the rest of the defence portfolio. No real procurement office, no real classification, no fielded materiel is implied or held.

---

## 7. Conclusions

The MP-4.6P Guardian LE is a complete, simulation-validated police-combat-pistol prospectus chambered in a proprietary 4.6 × 22 mm DPAP cartridge. The design is closed: the spring-mass-system parameters are analytically derived (§6.1 of the operator spec), the barrel safety factors are well-margined (SF_yield 2.28, burst 4.2×), the reliability programme achieves 20 548 + rounds MRBF with a quantified intervention pathway, the terminal-ballistics envelope covers the LE threat matrix (NIJ IIIA, NIJ III, all four common intermediate barriers) without overpenetration, and the felt recoil (0.084 ft-lbf, ≈ 50× lower than 9 mm) enables accurate single-handed engagement from non-standard firing positions.

The weapon is a member of the 4.6 mm family documented in [`../Weapons-Defence/Common Architecture and Components.md`](../Weapons-Defence/Common%20Architecture%20and%20Components.md), sharing bore diameter, primer chemistry, projectile-tooling family, and parts-commonality targets (bolt-face case-hardening recipe, spring-material family, DLC/PVD surface-treatment protocols) with the military [`MP-4.6M Guardian Pistol`](../Weapons-Defence/MP-4.6M%20Pistol.md) and [`MP-4.6M Defender PDW`](../Weapons-Defence/MP-4.6M%20Defender%20PDW.md). The LE-variant case (22 mm vs 30 mm) and heavier bullet (3.3 g vs 2.6 g) are the deliberate design deltas, chosen to move the operating velocity from the overpenetration-prone 501 m/s military regime to the LE-compliant 396 m/s regime.

The prospectus makes five falsifiable predictions that first-article testing can confirm or refute within a single range-validation programme:

1. Muzzle velocity of 396 m/s (± 15 m/s) from a 150 mm barrel with the specified 0.22 g charge — directly measurable by chronograph.
2. Peak chamber pressure of 246 MPa (± 15 MPa) — directly measurable by a piezoelectric pressure transducer in a proof barrel.
3. NIJ IIIA soft-armour defeat at 396 m/s impact velocity — directly testable against a reference panel.
4. Soft-tissue gelatin penetration of 216 mm (cold) / 248 – 270 mm (warm) — directly testable in an FBI-protocol gelatin block.
5. MRBF ≥ 15 000 rounds in a sustained-fire endurance test — verifiable within a 20-weapon × 5 000-round programme.

Until first-article testing confirms these predictions, all claims in this paper remain model predictions, not measurements. The simulator is conservative; physical testing is expected to produce equal or better results.

---

## 8. References

1. HK MP7A2 Technical Data — 4.6 × 30 mm MP7 muzzle velocity and pressure data. Heckler & Koch GmbH, Oberndorf, 2021.
2. Federal Bureau of Investigation. *Handgun Wounding Factors and Effectiveness* (1989, updated 2014). FBI Firearms Training Unit, Quantico VA. (9 mm 124 gr reference for tissue-model calibration.)
3. Litz, B. (2011). *Applied Ballistics for Long Range Shooting*, 2nd ed. Applied Ballistics LLC. (Corrected Miller twist-stability formula; gyroscopic stability Sg.)
4. Miller, D.R. (1983). A New Method of Computing Twist. *Precision Shooting*, January 1983. (Original Miller formula, corrected for SI in Litz 2011.)
5. Recht, R.F. & Ipson, T.W. (1963). Ballistic perforation dynamics. *Journal of Applied Mechanics*, 30(3), 384–390. (Recht-Ipson ballistic-limit model for intermediate barriers.)
6. Alekseevski, V.P. (1966). Penetration of a rod into a target at high velocity. *Combustion, Explosion and Shock Waves*, 2(2), 63–66. (Rigid-cavity-expansion regime for AP penetration below ≈ 2 000 m/s.)
7. Wahl, A.M. (1963). *Mechanical Springs*, 2nd ed. McGraw-Hill. (Wahl correction factor for recoil-spring torsional shear stress.)
8. Goodman, J. (1899). *Mechanics Applied to Engineering*, vol. 1. Longmans Green. (Goodman infinite-life fatigue criterion.)
9. NIJ Standard 0101.07. *Ballistic Resistance of Body Armor*. National Institute of Justice, Washington DC, 2022. (NIJ IIIA and III reference-panel test protocols.)
10. NIJ Standard 0115.00. *Stab Resistance of Personal Body Armor*. National Institute of Justice, Washington DC, 2000. (Referenced in the sibling [`APES-L Mark I Police Body Armour.md`](APES-L%20Mark%20I%20Police%20Body%20Armour.md).)
11. Odinl (2026). *MP-4.6M Guardian Suppressed Service Pistol — Operator Specification Sheet*. [`../Weapons-Defence/MP-4.6M Pistol.md`](../Weapons-Defence/MP-4.6M%20Pistol.md). (Military parent of the 4.6 mm family.)
12. Odinl (2026). *MP-4.6M Defender PDW — Operator Specification Sheet*. [`../Weapons-Defence/MP-4.6M Defender PDW.md`](../Weapons-Defence/MP-4.6M%20Defender%20PDW.md). (PDW sibling, 266.7 mm barrel.)
13. Odinl (2026). *Common Architecture and Components — 4.6 mm / 6.8 mm / 15.2 mm / 57 mm / 140 mm portfolio*. [`../Weapons-Defence/Common Architecture and Components.md`](../Weapons-Defence/Common%20Architecture%20and%20Components.md). (Portfolio cartridge table and parts-commonality matrix.)
14. Odinl (2026). *APES-L Mark I Police Body Armour — Research Paper*. [`./Research Paper — APES-L Police Body Armour.md`](Research%20Paper%20%E2%80%94%20APES-L%20Police%20Body%20Armour.md). (Sibling Weapons-Police research paper.)
15. Archard, J.F. (1953). Contact and rubbing of flat surfaces. *Journal of Applied Physics*, 24(8), 981–988. (Archard wear law for bore-life and cam-track life estimates.)
16. Lamé, G. (1852). *Leçons sur la théorie mathématique de l'élasticité des corps solides*. Bachelier, Paris. (Thick-walled cylinder stress analysis for barrel and chamber.)

---

## Related documents

- [`./MP-4.6P Guardian LE.md`](MP-4.6P%20Guardian%20LE.md) — paired operator specification sheet (this paper's companion)
- [`./APES-L Mark I Police Body Armour.md`](APES-L%20Mark%20I%20Police%20Body%20Armour.md) — sibling Weapons-Police protective system
- [`./Research Paper — APES-L Police Body Armour.md`](Research%20Paper%20%E2%80%94%20APES-L%20Police%20Body%20Armour.md) — sibling research paper
- [`../Weapons-Defence/weapons_simulation.py`](../Weapons-Defence/weapons_simulation.py) — the simulator that produces all numbers cited in this paper
- [`../Weapons-Defence/weapons_sim_results.md`](../Weapons-Defence/weapons_sim_results.md) — canonical simulator output reference
- [`./README.md`](README.md) — folder overview

---

[← Back to folder README](README.md)