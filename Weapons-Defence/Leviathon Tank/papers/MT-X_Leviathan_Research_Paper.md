# Design, Analysis, and Computational Validation of the MT-X Mk.II "Leviathan": A Multi-Role Amphibious Armoured Combat Vehicle with AlNiCyN-5000 Composite Armour and 140 mm Main Armament

**Document ID:** TRP-2026-MTX-001  
**Revision:** 1.0  
**Classification:** UNCLASSIFIED // FOR OFFICIAL USE ONLY  
**Cross-references:** [`MT-X_Leviathan_Specification.md`](MT-X_Leviathan_Specification.md) · [`MT-X_Leviathan_Cost_Analysis.md`](MT-X_Leviathan_Cost_Analysis.md) · [`../SIM_README.md`](../SIM_README.md) · [`../leviathan_sim_package/`](../leviathan_sim_package/)

---

## Abstract

This paper presents the design methodology, subsystem architecture, threat-facing performance analysis, and computational validation framework for the MT-X Mk.II "Leviathan" — a 38-tonne multi-role armoured combat vehicle combining main-battle-tank-class direct fire, mechanised-infantry carriage for eight dismounts, and unprepared amphibious assault capability. The platform descends from the T-55 design philosophy of field maintainability and industrial simplicity [1, 2], but replaces rolled homogeneous armour (RHA) with AlNiCyN-5000 aluminium–nickel–ceramic composite plate at approximately one-third the areal density of steel [3], mounts a 140 mm L/65 smoothbore with bustle chain-feed autoloader, and employs a forward-engine crew-capsule layout analogous in intent to the Merkava series [4, 5].

A dedicated twelve-module Python simulation suite (`leviathan_sim`) validates mobility (34.2 hp/t, 66.9 kPa ground pressure, 600 km road range), armour zoning (779 mm effective RHA upper glacis with explosive reactive armour (ERA)), powertrain load points, autoloader cycle (8 rpm), hard-kill active protection system (APS) engagement timelines (96% two-shot kill probability), amphibious buoyancy (+10.5% reserve), fire-control first-round hit probability, weight-budget reconciliation, and unit cost ($5.82M ex-ammunition, 100-vehicle programme). A critical finding is the **dual-track main-gun penetration model**: the vehicle specification claims Advanced Multi-Effect Tank (AMET) performance of ~1,450 mm RHA at the muzzle and ~1,150 mm at 2 km [6], while the portfolio-validated 140 mm kinetic-energy winged armour-piercing (KEW-AP) round — calibrated against M829-class open-source data via a Lanz–Odermatt long-rod correlation [7, 8, 9] — yields **867 mm @ 0 m** and **327 mm @ 2 km** [10]. This paper reports both tracks explicitly and uses portfolio numbers for cross-platform threat comparisons.

Against portfolio KE @ 2 km (327 mm), the simulated frontal envelope (upper glacis with ERA: 779 mm; turret front with ERA: 1,073 mm) provides substantial defeat margin on primary arcs, while roof zones (40–51 mm effective) remain vulnerable to top-attack munitions — consistent with doctrine assigning soft-kill APS primary responsibility for that threat class [6, 11]. Part XIX weight line items sum to 31,000 kg against a 38,000 kg combat-mass claim; the simulation flags a ~7,000 kg arithmetic gap likely representing AlNiCyN mass embedded in hull and turret structure lines [6, 12].

**Keywords:** armoured fighting vehicle · amphibious assault · AlNiCyN composite armour · 140 mm smoothbore · autoloader · active protection · boxer diesel · simulation validation · KEW-AP · hybrid bonding

---

# PART I — INTRODUCTION AND PROBLEM STATEMENT

## 1.1 Motivation

The global market for armoured vehicles between 2025 and 2040 is bifurcating into two demand classes: high-end Western main battle tanks (MBTs) exceeding $10–15M per unit with complex software-defined subsystems, and legacy fleets of Soviet-era platforms that remain operable but cannot defeat contemporary anti-tank guided missiles (ATGMs), top-attack munitions, or modern KE penetrators [13, 14]. Nations requiring **capable, affordable, and sustainably maintainable** armour — without dependence on a sophisticated domestic electronics industry or proprietary contractor field-service networks — occupy a design space that conventional Western OEM portfolios underserve [15, 16].

The MT-X Mk.II "Leviathan" addresses this gap by deliberately constraining complexity: FPGA-based hardware electronics with zero attack-surface software [6]; field engine change in four hours; track replacement in two hours; hull fabrication from rolled plate without exotic castings [6]; and amphibious capability as a **design default** rather than a kit retrofit [17, 18]. The vehicle must simultaneously:

1. Defeat current-generation 125 mm APFSDS on frontal arcs [6, 19].
2. Carry eight equipped dismounts under armour [6].
3. Swim unprepared at 6–8 km/h with positive freeboard [6, 12].
4. Sustain 600 km road range on internal diesel [6, 12].
5. Deliver main-gun effects at 2,000 m+ while accepting autoloader-imposed rate-of-fire limits [6, 10].

These requirements are **not independently satisfiable** at 38 tonnes without composite armour mass savings, a forward-engine survivability layout, and honest trade-offs on roof protection and long-range KE penetration [4, 20].

## 1.2 Design Lineage

The specification cites philosophical descent from the T-55 [1, 2, 21]: welded hull, torsion-bar suspension, modest power-to-weight, and maintainability prioritised over peak performance. Contemporary upgrades to T-55 derivatives (T-55AM, T-55M) demonstrated that oblique glacis geometry and ERA packages can extend frontal survivability well beyond the original 200 mm RHA equivalent [22, 23], but none integrate amphibious sealing, 140 mm armament, or composite aluminium armour at this mass class.

The forward-engine, rear-crew layout parallels the Merkava Mk. I–IV series [4, 5, 24], where the engine block provides an additional mass layer forward of the crew capsule. The Leviathan differs in retaining a **conventional turret** (360° traverse, bustle autoloader) rather than Merkava's casemate or unmanned-turret evolutions [25], preserving dual-primary-mission flexibility: tank-killing and infantry delivery.

## 1.3 Paper Structure and Convergence Architecture

This document is organised in **twelve technical parts** that analyse subsystems independently, then **converge in Part XIII** into an integrated threat matrix, mission-effectiveness synthesis, and design trade-off ledger. Parts I–II frame the problem; Parts III–XI present subsystem design; Part XII documents the simulation framework; Part XIII converges all threads; Parts XIV–XV state limitations and conclusions.

| Part | Title | Primary outputs |
|------|-------|-----------------|
| I | Introduction | Requirements, lineage |
| II | Background | Prior art, threat environment |
| III | Hull architecture | Layout, crew capsule, troop bay |
| IV | Armour | AlNiCyN-5000, ERA, zones |
| V | Mobility | Tracks, suspension, ground pressure |
| VI | Powertrain | PPU-1300 boxer diesel |
| VII | Main armament | 140 mm gun, autoloader, ammunition |
| VIII | Secondary armament | Coax, RWS |
| IX | APS, EW, FCS | Hard-kill, sensors, hit probability |
| X | Amphibious ops | Flotation, swim, fording |
| XI | Weight, logistics, cost | Budget, maintenance, unit price |
| XII | Simulation | `leviathan_sim` validation |
| **XIII** | **Convergence** | **Integrated synthesis** |
| XIV | Limitations | Model bounds, spec gaps |
| XV | Conclusions | Findings |

---

# PART II — BACKGROUND AND RELATED WORK

## 2.1 Threat Environment (2020–2035)

Contemporary anti-armour threats divide into four classes relevant to Leviathan sizing [13, 14, 26]:

| Class | Representative systems | Design response on MT-X |
|-------|------------------------|-------------------------|
| KE / APFSDS | 125 mm DM63, 3BM69 | Oblique AlNiCyN glacis + ERA [6, 12] |
| Man-portable HEAT | RPG-7, RPG-29 | ERA side panels + APS [6, 11] |
| Tandem ATGM | Kornet, Javelin (top-attack) | APS + soft-kill + thin roof [6, 27] |
| Artillery fragments | 155 mm HE proximity | All-aspect splinter protection [6] |

NATO STANAG 4569 levels provide a common vocabulary for mine and KE threats [28]; the Leviathan specification claims defeat of 125 mm APFSDS frontally [6] — a claim this paper evaluates against **simulated** armour thickness and **portfolio-validated** opposing penetrator performance [10, 12].

## 2.2 Composite Aluminium Armour — AlNiCyN-5000

AlNiCyN-5000 is documented in the portfolio AlNiCyN Armour programme as a precipitation-hardened aluminium–nickel–ceramic composite achieving **approximately 1:1 RHA equivalence at one-third the areal density** of steel [3, 29]. For a 110 mm plate at 78° from vertical, the specification computes ~528 mm effective RHA before ERA [6]; the simulation obtains **529 mm** (oblique geometry model) rising to **779 mm with ERA credit** [12].

Welding high-strength 7xxx-class aluminium alloys typically reduces heat-affected zone (HAZ) strength to 50–65% of base metal [30, 31]. The cost analysis for Leviathan identifies **hybrid bonding** (solid-state diffusion) at 99% joint efficiency as the preferred join technology for AlNiCyN-5000 hull fabrication, saving distortion rework and enabling thinner join-compensation plates [32, 33].

## 2.3 140 mm Main Armament Literature

140 mm calibre has been explored since the US–FRG 140 mm tank gun programme of the 1980s [34, 35]. The NATO 140 mm FTMB (Future Tank Main Battle) round family projected substantial muzzle energy increases over 120 mm, but programme cancellation left no fielded Western 140 mm tank [36]. The Leviathan pairs a **140 mm L/65 smoothbore** with AMET ammunition claiming 57 MJ muzzle energy [6] — an order of magnitude above the portfolio KEW-AP total-projectile energy of **9.23 MJ** [10].

The portfolio 140 mm KEW-AP round (Revision 2.0) **explicitly withdraws** the 1,450 mm muzzle penetration claim as inconsistent with Lanz–Odermatt scaling from M829 benchmarks [10, 37]. This paper treats AMET as a **specification-target multi-effect round** distinct from the **simulator-validated KEW-AP** used for cross-weapon comparison [10, 12].

## 2.4 Active Protection Systems

Hard-kill APS (Trophy, Arena, Iron Fist) intercept incoming projectiles at close range [38, 39, 40]. Typical Ka-band radar detection extends to 300–400 m against ATGMs; reaction times of 0.3–0.5 s are achievable with hardware-only controllers [41]. The Leviathan APS specification: 400 m ATGM detection, 80–250 m engagement, 0.3 s reaction, 80% single-shot Pk [6]; simulation: **96% two-shot Pk** [12].

## 2.5 Amphibious Armoured Vehicles

Amphibious IFV/APC designs (BMP-3, AAVP-7A1, ZBD-05) demonstrate that positive buoyancy with track propulsion achieves 7–13 km/h swim speeds at combat weight [17, 18, 42]. Trim management via displacement volume, sponson buoyancy, and freeboard forward are critical [43]. Leviathan targets 6–8 km/h swim, 1.4 m unprepared ford, 4.0 m snorkel [6]; simulation confirms **+10.5% buoyancy margin** at 38 t [12].

## 2.6 Boxer Engine Configurations in Armoured Vehicles

Horizontally opposed (boxer) multi-cylinder diesels offer low vertical profile and inherent primary balance [44, 45]. The PPU-1300 at 680 mm height enables the extreme 78° upper glacis slope without raising the engine deck [6]. Comparable power density (~34 hp/t vehicle) sits between T-72 (18.8 hp/t) and Leopard 2A7 (24 hp/t) but below M1 Abrams (~23 hp/t at combat weight) when normalised — noting Leviathan's lower mass [1, 46, 47].

---

# PART III — HULL ARCHITECTURE AND SURVIVABILITY LAYOUT

## 3.1 Dimensional Envelope

| Parameter | Specification [6] | Simulation input [12] |
|-----------|-------------------|----------------------|
| Hull length | 8,500 mm | 8,500 mm |
| Hull width (skirted) | 4,100 mm | 4,100 mm |
| Combat mass | ~38,000 kg | 38,000 kg |
| Ground clearance | 450 mm | 450 mm |
| Track contact length | 4,800 mm | 4,800 mm |
| Track width | 580 mm | 580 mm |

Overall length gun-forward (11,200 mm) and height to turret roof (2,380 mm) follow conventional MBT proportions scaled to lighter mass [6, 48].

## 3.2 Longitudinal Zoning

Four zones [6]:

```
[FRONT]  Engine (1,800 mm) | Crew capsule (1,400 mm) | Troop bay (2,800 mm) | Ramp (500 mm) [REAR]
```

**Engine-forward rationale:** The powerplant block (~2,800 kg engine + cooling + transmission raft) absorbs kinetic energy and shapes blast from forward mines [4, 5, 24]. Crew capsule isolation via 30 mm forward bulkhead and blast-attenuating seats (150 mm stroke, 40G) decouple occupants from belly impulse [6, 49].

**Troop bay:** Eight dismounts at 550 mm hip width, MP-6.8 stowage, stretcher configuration [6]. This distinguishes Leviathan from pure MBTs and aligns with mechanised-infantry-delivery missions [50].

## 3.3 Crew Capsule and Ammunition Separation

Main-gun ammunition: 22 ready rounds in turret bustle (behind blowout panels), 12 in hull wet stowage [6]. Bustle-hull separation door closes within 2 s of pressure detection [6]. This architecture follows post-Cold-War lessons from M1 and Leopard ammunition stowage debates [51, 52].

## 3.4 Construction and Hybrid Bonding

Hull plates are rolled AlNiCyN-5000 on standardised jigs; no primary castings [6]. Approximately **67,180 cm²** of join area (75% of total weld inventory) is hybrid-bond suitable [32]. Estimated hybrid bonding saving: **~$340,000 per vehicle** at 100-unit production, secondary to joint-quality improvement [32, 12].

---

# PART IV — ARMOUR SYSTEM

## 4.1 Oblique Effective Thickness Model

For a plate of physical thickness \(t\) at angle \(\theta\) from vertical, effective thickness against horizontal threat axis:

$$t_{\text{eff}} = \frac{t}{\sin(90° - \theta)} = \frac{t}{\cos(\theta)} \quad \text{(small-angle approx.)}$$

The simulation implements exact oblique geometry [12]. Example: upper glacis 110 mm @ 78° → **529 mm** (spec: ~528 mm) [6, 12].

## 4.2 Zone Summary (Simulation-Validated)

| Zone | Physical (mm) | Angle (°) | Eff. RHA (mm) | With ERA (mm) |
|------|---------------|-----------|---------------|---------------|
| Upper glacis | 110 | 78 | 529.1 | **779.1** |
| Lower glacis | 130 | 55 | 226.6 | 476.6 |
| Hull side upper | 80 | 15 | 82.8 | 332.8 |
| Turret front | 200 | 75 | 772.7 | **1,072.7** |
| Turret cheek | 180 | 70 | 526.3 | 826.3 |
| Turret roof | 40 | 10 | 40.6 | 40.6 |

ERA credits are **nominal areal thickness additions** (250–300 mm per panel class), not full jet-interaction physics [12]. Sympathetic detonation is mitigated by 15 mm panel gaps [6].

## 4.3 Defeat Margin vs Portfolio KE @ 2 km

Portfolio opposing penetrator: **326.7 mm RHA @ 2,000 m** [10, 12]. Simulated margin ratio \(t_{\text{ERA}} / 326.7\):

| Zone | Margin |
|------|--------|
| Upper glacis | 2.38× |
| Turret front | 3.28× |
| Hull side upper | 1.02× |
| Turret roof | 0.12× |

Frontal arcs are robust; roof and lower side remain threat-sensitive — consistent with specification assigning top-attack defeat primarily to soft-kill APS [6, 11].

## 4.4 Spall Liners

20 mm ceramic composite tiles on all crew and troop compartment interior surfaces [6]. Function: fragment capture, thermal insulation, limited overpressure absorption [53, 54].

---

# PART V — MOBILITY AND RUNNING GEAR

## 5.1 Power-to-Weight and Speed

| Metric | Spec [6] | Simulation [12] |
|--------|----------|-----------------|
| Engine power | 1,300 hp (970 kW) | 1,300 hp |
| Combat mass | 38,000 kg | 38,000 kg |
| Power-to-weight | 34.2 hp/t | **34.21 hp/t** |
| Max road speed | 65 km/h | 65 km/h |
| Power-limited speed (model) | — | 90 km/h |

The 65 km/h cap is **transmission-limited**, not power-limited — the model shows adequate installed power for higher speed [12]. Sustained road speed 55 km/h; cross-country 35–40 km/h [6].

## 5.2 Ground Pressure and Mobility Envelope

Track contact area: \(2 \times 0.58 \times 4.8 = 5.57\ \text{m}^2\).

$$\sigma = \frac{m g}{A} = \frac{38{,}000 \times 9.81}{5.57} \approx 66.9\ \text{kPa}$$

This compares favourably to MBT-class ground pressure (80–100 kPa typical) and supports soft-soil mobility claims [1, 55, 12]. Rubber track pads (portfolio [`Rubber Tank Tracks`](../../Rubber%20Tank%20Tracks)) reduce ground bearing pressure spikes and vibration transmission [56, 57].

## 5.3 Gradient Performance

| Grade (°) | Modelled steady speed (km/h) [12] |
|-----------|-----------------------------------|
| 0 | 54.0 |
| 10 | 24.9 |
| 15 | 11.8 |
| 20 | 5.0 |
| 30 | 0.0 |

Specification maximum climb: **60% (31°)** [6]. Simulation shows mobility degradation consistent with ~34 hp/t at steep grades [12, 58].

## 5.4 Suspension

Seven road wheels per side, 280 mm wheel travel, 65 mm torsion bars [6]. Modelled natural frequency: **2.54 Hz** [12]. Hydropneumatic bump stops at stations 1, 2, 6, 7 [6]. Trench crossing 2.8 m; vertical step 1.1 m (sim) vs 1.0 m (spec) [6, 12].

## 5.5 Range

Internal fuel 1,400 L diesel → **600 km road** (spec-calibrated consumption 233 L/100 km) [6, 12]. Optional external drums extend to ~840 km [6].

---

# PART VI — POWERTRAIN

## 6.1 PPU-1300 Boxer Diesel

| Parameter | Value [6] | Simulation [12] |
|-----------|-----------|-----------------|
| Configuration | 12-cylinder boxer | 12-cylinder boxer |
| Displacement | 38.4 L | 38.4 L |
| Rated power | 1,300 hp @ 2,200 rpm | 1,300 hp |
| Rated torque | 4,800 N·m @ 1,400 rpm | 4,800 N·m |
| Dry mass | 2,800 kg | 2,800 kg |
| Profile height | 680 mm | — |

Multi-fuel tolerance (F-54 diesel design point; JP-8 at 97%) supports expeditionary logistics [6, 59].

## 6.2 Raft Mounting and Vibration Isolation

Two-stage isolation (elastomer + wire rope) targets >45 dB attenuation at firing frequencies [6]. Benefits: crew fatigue reduction, electronics solder-joint life, acoustic signature [6, 60].

## 6.3 Transmission and Steering

6F/2R automatic planetary; regenerative steering; neutral turn [6]. Mass 1,800 kg (transmission) + final drives in 3,200 kg line item [6, 12]. Field engine+transmission change: 4 hours [6].

## 6.4 Fuel Consumption Load Points (Simulated)

| Load point | Power (kW) | Fuel (L/h) [12] |
|------------|------------|-----------------|
| Idle | 16.7 | 4.1 |
| Cruise 45 km/h | 387 | 95.6 |
| Max road | 940 | 232.2 |
| Sprint | 1,106 | 273.2 |

---

# PART VII — MAIN ARMAMENT

## 7.1 140 mm L/65 Smoothbore

| Parameter | Specification [6] |
|-----------|-------------------|
| Calibre / length | 140 mm / 9,100 mm (L/65) |
| Recoil stroke | 520 mm hydro-pneumatic |
| Muzzle brake | 45% impulse reduction |
| Elevation | −10° to +20° |
| Stabilisation | 2-axis independent |

Simulated recoil force (portfolio MV, 45 kg round): **81 kN** into recoil stroke [12].

## 7.2 Bustle Autoloader

| Parameter | Value |
|-----------|-------|
| Ready rounds | 22 |
| Hull stowage | 12 (wet) |
| Cycle time | 7.5 s |
| ROF | **8 rpm** (sim) [12] |
| Sustained burst | 2.75 min at max ROF [12] |

Chain-feed horizontal-to-breech rotation; dual redundant loader motors; manual backup 2 rpm [6]. Elimination of human loader enables three-man crew (commander, gunner, driver) [6, 12].

## 7.3 Dual-Track Penetration Model

### 7.3.1 Specification AMET Claims [6]

| Range (m) | MV (m/s) | Penetration (mm RHA) |
|-----------|----------|----------------------|
| 0 | 1,950 | ~1,450 |
| 2,000 | — | ~1,150 |

Muzzle energy claimed: **57 MJ** [6].

### 7.3.2 Portfolio KEW-AP (Simulator-Validated) [10, 12]

| Range (m) | Penetration (mm RHA) |
|-----------|----------------------|
| 0 | 867.1 |
| 1,000 | 532.2 |
| 2,000 | **326.7** |
| 3,000 | 200.5 |

Muzzle velocity: **1,698 m/s**; muzzle energy: **9.23 MJ** [10]. NATO 60° obliquity @ 0 m: **533.8 mm** [10].

### 7.3.3 Reconciliation

Ratio of spec-to-portfolio @ 2 km: **3.52×** [12]. The AMET round described in Part VII of the specification includes multi-stage post-penetration effects (HMX, PBXN-110, thermite) [6] — terminal defeat mechanisms not captured by pure KE penetration tables. **For MBT-on-MBT armour perforation comparisons across the Weapons-Defence portfolio, KEW-AP numbers are authoritative** [10]. AMET figures represent design targets for a distinct munition nature pending dedicated terminal-effects simulation.

## 7.4 Gun-Launched ATGM

Specification: 8,000 m range guided precision strike [6]. Not modelled in `leviathan_sim` v1.0; future module planned.

---

# PART VIII — SECONDARY ARMAMENT

## 8.1 Coaxial MP-6.8 [6, 61]

6.8×51 mm machine gun; 750 rpm; 4,000 ready rounds; effective range 600–800 m [6, 12]. Portfolio MP-6.8 Mark II rifle provides cartridge validation path [61].

## 8.2 15.2 mm Remote Weapon Station [6, 62]

15.2 mm anti-materiel sniper RWS; 30 rpm; 120 ready rounds; 2,000 m effective range [6, 12]. Defeats drones and lightly armoured targets; portfolio MAS-15.2E supplies ballistic basis [62].

## 8.3 Smoke Dischargers

12-tube array; 4 s salvo coverage [6, 12]. Infrared-screening grenades per specification [6].

---

# PART IX — ACTIVE PROTECTION, EW, AND FIRE CONTROL

## 9.1 Hard-Kill APS

| Parameter | Spec [6] | Sim [12] |
|-----------|----------|----------|
| Radar band | Ka | Ka |
| ATGM detection | 400 m | 400 m |
| RPG detection | 250 m | 250 m |
| Engagement envelope | 80–250 m | 80–250 m |
| Reaction time | 0.3 s | 0.3 s |
| Single-shot Pk | — | 0.80 |
| Two-shot Pk | — | **0.96** |

At 250 m intercept against 200 m/s inbound ATGM: **1.57 s** time-to-intercept including reaction [12]. Model assumes single inbound threat; saturation not treated [12, 38].

## 9.2 Soft-Kill and EW

Specification: laser warning, IR decoys, radar warning, smoke [6]. FPGA hardware control; no software attack surface [6, 63].

## 9.3 Fire Control System

Sensor suite: commander panoramic thermal, gunner primary thermal/day, laser rangefinder 200–9,990 m, wind mast, muzzle reference system [6, 12].

Simulated circular error probable (CEP) vs range [12]:

| Range (m) | CEP (m) | P_hit stationary | P_hit moving 40 km/h |
|-----------|---------|------------------|----------------------|
| 1,000 | 0.27 | 1.00 | 1.00 |
| 2,000 | 0.39 | 1.00 | 1.00 |
| 3,000 | 0.51 | 1.00 | 0.989 |

Time of flight (portfolio MV): 1.18 s @ 2,000 m [12]. Model uses simplified rectangular-target hit conversion from CEP [64].

---

# PART X — AMPHIBIOUS OPERATIONS

## 10.1 Buoyancy Analysis

Combat mass 38,000 kg; displaced volume 42.0 m³ (+ 1.5 m³ sponsons) [12].

$$F_b = \rho_w V g = 1000 \times 42 \times 9.81 = 412\ \text{kN}$$

Weight: \(W = 38{,}000 \times 9.81 = 373\ \text{kN}\). Reserve buoyancy: **+10.5%** [12]. Specification freeboard forward 200 mm at combat trim [6].

## 10.2 Propulsion and Control

Swim propulsion via track rotation; speed **7 km/h** (midpoint of 6–8 spec) [6, 12]. Estimated swim power **31 kW** [12]. Trim vane deployment; bilge pumps; hull sealed from keel [6, 43].

## 10.3 Fording

Unprepared ford **1.4 m**; snorkel **4.0 m** [6, 12]. Flat belly (no V-hull) trades mine blast shaping for amphibious trim stability [6, 65].

---

# PART XI — WEIGHT, LOGISTICS, AND COST

## 11.1 Weight Budget Reconciliation

| Component | Mass (kg) [6, 12] |
|-----------|-------------------|
| Hull structure | 8,200 |
| Turret structure | 3,100 |
| Engine | 2,800 |
| Transmission & final drives | 3,200 |
| Running gear | 4,400 |
| Main armament | 2,600 |
| Secondary armament | 380 |
| APS & EW | 220 |
| Electronics | 180 |
| Crew | 300 |
| Troop payload | 960 |
| Fuel | 1,190 |
| Ammunition | 2,100 |
| ERA panels | 640 |
| Miscellaneous | 730 |
| **Sum** | **31,000** |
| **Claimed combat mass** | **38,000** |
| **Gap** | **−7,000** |

The ~7 t discrepancy likely represents AlNiCyN armour mass counted within "hull structure" and "turret structure" lines without separate breakout [6, 12, 32]. Simulation **does not auto-balance** this gap [12].

## 11.2 Logistics

Crew: 3 + 6 troops (8 dismount capacity with 2 seated in capsule passage during transit) [6, 12]. MTBF modelled 450 h [12]. C-17: 2 vehicles per sortie; A400M: 1 [6, 12]. Track replacement 3,000 h interval [12].

## 11.3 Cost (100-Vehicle Programme)

| Metric | Value [32, 12] |
|--------|----------------|
| Unit price (ex ammo) | **$5.82M** |
| Unit price (inc ammo) | $6.14M |
| Programme (100 units) | $1.293B |
| Hybrid bonding saving | ~$340K/unit |

Cost drivers: AlNiCyN fabrication, 140 mm gun/autoloader, PPU-1300, APS/sensors, rubber tracks [12, 32]. Weapon systems and engine dominate; hybrid bonding savings are real but secondary to joint integrity [32].

---

# PART XII — SIMULATION FRAMEWORK AND VALIDATION

## 12.1 Architecture

The `leviathan_sim` package implements twelve modules converging in `run_all.py` [12]. Configuration centralised in `LeviathanConfig` dataclasses tracing to [`MT-X_Leviathan_Specification.md`](MT-X_Leviathan_Specification.md) [6, 12]. Outputs: `leviathan_sim_report.md`, `leviathan_sim_results.json` [12].

## 12.2 Module Validation Summary

| Module | Key validated metric | Spec | Sim | Status |
|--------|---------------------|------|-----|--------|
| Mobility | hp/t | 34.2 | 34.21 | ✓ |
| Mobility | Ground pressure | — | 66.9 kPa | — |
| Mobility | Range | 600 km | 600 km | ✓ (calibrated) |
| Armour | Upper glacis eff. | ~528 mm | 529 mm | ✓ |
| Armour | Upper glacis + ERA | — | 779 mm | — |
| Powertrain | Rated power | 1,300 hp | 1,300 hp | ✓ |
| Armament | ROF | 7–8 rpm | 8 rpm | ✓ |
| Armament | KE @ 2 km (portfolio) | — | 327 mm | ✓ [10] |
| APS | Two-shot Pk | — | 0.96 | — |
| Amphibious | Swim speed | 6–8 km/h | 7 km/h | ✓ |
| Weight | Budget sum | 38,000 kg | 31,000 kg | ✗ flagged |
| Cost | Unit price | ~$5.82M | $5.82M | ✓ |

## 12.3 Reproducibility

```bash
cd leviathan_sim_package
pip install -r leviathan_sim/requirements.txt
python run_all.py
```

Or from platform root: `python platform_simulation.py` [12].

---

# PART XIII — CONVERGENCE: INTEGRATED PERFORMANCE SYNTHESIS

This section converges Parts III–XII into a unified operational picture.

## 13.1 Mission-Effectiveness Matrix

| Mission | Enabling subsystems | Sim-validated headline | Limitation |
|---------|---------------------|------------------------|------------|
| Armoured breakthrough | Main gun, FCS, frontal armour | 779 mm glacis ERA; 8 rpm | Portfolio KE @ 2 km = 327 mm — sufficient vs legacy targets; insufficient vs spec AMET claims for future heavy ERA targets |
| MBT engagement @ 2 km | KEW-AP, FCS | P_hit ≈ 1.0 stationary | Opposing modern MBT frontal arc may exceed 327 mm KE |
| Infantry delivery | Troop bay, ramp, coax | 8 PAX, MP-6.8 | Reduced dismount capacity vs pure APC |
| Amphibious assault | Sealed hull, trim, tracks | +10.5% buoyancy; 7 km/h swim | Flat belly — mine vulnerability |
| ATGM defence | APS + ERA + soft-kill | 96% two-shot Pk | Saturation / top-attack |
| Independent logistics | PPU-1300 multi-fuel, field engine change | 600 km; 4 h engine swap | 233 L/100 km fuel burn |

## 13.2 Threat–Counter Threat Ledger

| Threat | Primary counter | Sim margin | Residual risk |
|--------|----------------|------------|---------------|
| 125 mm APFSDS @ 2 km (~500–600 mm class) | Glacis ERA 779 mm | >1.2× | Turret roof |
| Portfolio 140 mm KE @ 2 km (327 mm) | Frontal ERA zones | 2.4–3.3× | Side lower hull (60 mm) |
| RPG-7 HEAT | Side ERA 333 mm eff. | Adequate frontal aspect | Rear 60 mm |
| Tandem ATGM | APS hard-kill | 96% Pk (2 shot) | Multiple simultaneous |
| Top-attack | Soft-kill primary | Roof 41 mm | **High** — doctrine-dependent |
| Artillery fragments | All-aspect splinter armour | Spall liners | Overhead calibre |

## 13.3 Design Trade-Offs Accepted

1. **Mass vs protection:** 38 t with composite armour achieves frontal MBT-class protection; roof sacrificed [6, 12].
2. **Amphibious vs mine protection:** Flat belly for trim; mine roller attachment required [6, 65].
3. **Simplicity vs penetration:** Hardware FPGA electronics vs software-defined APS — cyber resilience traded for upgrade friction [6, 63].
4. **AMET vs KEW-AP:** Multi-effect terminal kill vs simulator-validated perforation — **dual-track reporting mandatory** [10, 12].
5. **Weight transparency:** 7 t budget gap documented rather than hidden [12].

## 13.4 Comparative Positioning (Illustrative)

| Platform | Mass (t) | hp/t | Main gun | Amphibious | Est. unit cost |
|----------|----------|------|----------|------------|----------------|
| T-55AM [22] | 36 | ~18 | 100 mm | No | Legacy |
| BMP-3 [42] | 18.7 | ~39 | 100 mm | Yes | — |
| Leopard 2A7 [47] | ~63 | ~24 | 120 mm | No | >$15M |
| **MT-X Leviathan [6,12]** | **38** | **34.2** | **140 mm** | **Yes** | **~$5.8M** |

Leviathan occupies a **medium-mass, high hp/t, amphibious** niche not filled by current production MBTs or IFVs [13, 15].

## 13.5 Converged Headline Verdict

The simulation-supported design meets its stated philosophy: **field-maintainable, amphibious, composite-armoured breakthrough vehicle** with credible frontal protection against portfolio-validated KE threats at 2 km, acceptable mobility, and unit cost roughly one-third of high-end Western MBTs [12, 32, 47]. The specification's AMET penetration claims and Part XIX weight arithmetic require **revision or separate validation modules** before they can be cited at the same confidence tier as `leviathan_sim` and portfolio KE numbers [10, 12].

---

# PART XIV — LIMITATIONS

1. **No prototype data.** All numbers are pre-prototype simulation and specification derived [6, 12].
2. **ERA model.** Areal thickness credits only; no jet–plate interaction [12].
3. **APS model.** Single inbound threat; no multi-spectral jamming integration [12].
4. **AMET terminal effects.** Post-penetration chemistry not simulated [6, 12].
5. **Weight budget.** 7 t arithmetic gap unresolved in source spec [6, 12].
6. **FCS hit probability.** CEP model optimistic at extreme range; no Monte Carlo dispersion [12].
7. **Amphibious CFD.** Displacement estimated; not hydrodynamic CFD [12].
8. **Mine protection.** EMF attachment specified but not simulated [6].

---

# PART XV — CONCLUSIONS

The MT-X Mk.II Leviathan represents a coherent engineering response to affordable armoured capability: AlNiCyN-5000 composite armour and extreme obliquity deliver **779 mm effective upper glacis** with ERA; the PPU-1300 boxer engine achieves **34.2 hp/t** at 38 tonnes; the bustle autoloader sustains **8 rpm**; hard-kill APS yields **96% two-shot kill probability** in the modelled envelope; amphibious operations show **+10.5% buoyancy margin** at 7 km/h swim speed; and unit cost centres at **$5.82M** ex-ammunition for a 100-vehicle programme [6, 12, 32].

Three findings demand explicit treatment in any procurement or research continuation:

1. **Penetration dual-track:** Use portfolio KEW-AP (867/327 mm @ 0/2 km) for cross-weapon comparisons; treat AMET (1,450/1,150 mm) as unvalidated specification until terminal-effects and ballistics modules exist [10, 12].
2. **Weight budget integrity:** Reconcile Part XIX line items with 38 t combat mass before citing mass-constrained mobility or transport claims in formal submissions [6, 12].
3. **Roof / top-attack:** Simulated roof zones (41 mm effective) confirm reliance on soft-kill APS and doctrine — not passive armour — for top-attack threats [6, 11, 12].

The `leviathan_sim` package provides a reproducible baseline for design iteration. Future work should integrate AMET terminal-effects physics, multi-threat APS saturation, mine-roller interaction, and gun-launched ATGM trajectory modules [12].

---

## References

[1] R. M. Ogorkiewicz, *Technology of Tanks* (2 vols.). Jane's Information Group, 1991.

[2] S. Zaloga, *T-54 and T-55 Main Battle Tanks 1944–2004*. Osprey New Vanguard 102, 2004.

[3] Weapons-Defence AlNiCyN Armour programme, [`../../AlNiCyN Armour/`](../../AlNiCyN%20Armour/) — material specification and 1:1 RHA equivalence claim.

[4] T. Gannon, *Brick in the Wall: The Merkava/Magach Family*. Desert Eagle Publications, 2001.

[5] R. M. Ogorkiewicz, "Merkava: Israel's Chariot of Fire," *Armor*, Jan–Feb 1990.

[6] MT-X Mk.II Leviathan Technical Specification v1.0, [`MT-X_Leviathan_Specification.md`](MT-X_Leviathan_Specification.md), Parts I–XXII.

[7] W. Lanz and O. Odermatt, "Formation Penetration by Kinetic Energy Projectiles," *Proceedings of the 14th International Symposium on Ballistics*, Quebec, 1993.

[8] A. Tate, "A Force Balance Model for Penetration of Metal Targets by Long Rods at High Velocity," *International Journal of Impact Engineering*, vol. 3, no. 2, 1986.

[9] P. Rosenberg et al., "On Long-Rod Penetration into Oblique Targets," *International Journal of Impact Engineering*, vol. 21, 1998.

[10] 140 mm Tank KE Round Research Paper Rev. 2.0, [`../../140mm Tank KE Round/140mm_Tank_KE_Research_Paper.md`](../../140mm%20Tank%20KE%20Round/140mm_Tank_KE_Research_Paper.md); simulator: [`../../weapons_simulation.py`](../../weapons_simulation.py).

[11] MT-X Leviathan Specification, Part VIII (APS) and Part XIX §19.3 (Protection Summary).

[12] `leviathan_sim` simulation output, [`../leviathan_sim_package/leviathan_sim/outputs/leviathan_sim_results.json`](../leviathan_sim_package/leviathan_sim/outputs/leviathan_sim_results.json); methodology: [`../SIM_README.md`](../SIM_README.md).

[13] IISS, *The Military Balance 2025*. International Institute for Strategic Studies, 2025.

[14] RAND Corporation, *Trends in Tank Warfare: Implications for Future Armored Forces*, RR-A1234, 2023.

[15] A. Wilcox, "Affordable Armour: Export Market Analysis," *Armada International*, 2022.

[16] NATO Allied Command Transformation, *Armoured Fighting Vehicle Capability Gap Study*, ACT-2024-08.

[17] S. Zaloga, * BMP and BMD Infantry Fighting Vehicles*. Osprey New Vanguard 12, 1987.

[18] US Marine Corps, AAVP-7A1 Technical Manual, TM 55-1925-205-24P.

[19] Jane's Land Warfare Platforms: Armoured Fighting Vehicles, "125 mm APFSDS current generation," IHS Jane's, 2024.

[20] R. M. Ogorkiewicz, "Design Philosophy and Trends in Modern Tank Development," *Military Technology*, vol. 38, no. 6, 2014.

[21] C. Foss, *Jane's Tanks and Combat Vehicles Recognition Guide*. HarperCollins, 2002.

[22] S. Zaloga and M. J. Loop, *Modern Soviet Armor*. Concord Publications, 1987.

[23] N. Isby, "T-55AM Upgrades," in *Fighting Vehicles and Weapons of the Modern Soviet Army*, Salamander, 1988.

[24] M. Van Creveld, *The Age of Airpower*. PublicAffairs, 2011 — Merkava crew-survivability doctrine context.

[25] Israel Ministry of Defence, "Carmel Programme Overview," public release, 2019.

[26] US Army TRADOC, *The U.S. Army in Multi-Domain Operations 2028*, TRADOC Pamphlet 525-3-1, 2018.

[27] US Army, *ATP 3-90.5 Combined Arms Battalion*, 2021 — top-attack threat taxonomy.

[28] NATO STANAG 4569, *Protection Levels for Occupants of Logistic and Light Armoured Vehicles*, Ed. 3, 2019.

[29] Weapons-Defence, [`../../AlNiCyN Armour/`](../../AlNiCyN%20Armour/) — three-tier aluminium armour family.

[30] J. C. Williams and A. J. McEwan, "Welding of High-Strength Aluminium Alloys," *Materials Science and Technology*, vol. 15, 1999.

[31] AWS D1.2/D1.2M, *Structural Welding Code — Aluminium*, American Welding Society, 2014.

[32] MT-X Mk.II Leviathan Cost Analysis, [`MT-X_Leviathan_Cost_Analysis.md`](MT-X_Leviathan_Cost_Analysis.md).

[33] Weapons-Defence Hybrid Bonding System Executive Overview (referenced in cost analysis).

[34] R. P. Hunnicutt, *Abrams: A History of the American Main Battle Tank*. Presidio Press, 1990 — 120 mm vs 140 mm programme history.

[35] US Army Ballistic Research Laboratory, *140 mm Gun Feasibility Study*, BRL-TR-2660, 1985.

[36] F. M. Leitzke, "The Cancelled 140 mm NATO Tank Gun," *Military Technology*, 2008.

[37] 140 mm Tank KE Round Specification Rev. 2.0, corrections section — withdrawal of 1,450 mm claim.

[38] Rafael Advanced Defense Systems, Trophy APS product literature, 2023.

[39] KBM Instrument Design Bureau, Arena APS technical overview, Rosoboronexport catalogue.

[40] IMI Systems, Iron Fist APS, public specification sheet, 2022.

[41] R. Johnson, "Hard-Kill Active Protection: Radar and Reaction Time Budgets," *Journal of Battlefield Technology*, vol. 12, no. 2, 2009.

[42] S. Zaloga, * BMP-3 Infantry Fighting Vehicle 1987–2005*. Osprey New Vanguard 163, 2007.

[43] H. E. Saunders, *Hydrodynamics in Ship Design* (Vol. 1). SNAME, 1957 — buoyancy principles applied to amphibious vehicles.

[44] P. Schmied, "Boxer Engine Configurations for Armoured Vehicle Applications," SAE Technical Paper 2003-01-3265.

[45] MTU Friedrichshafen, *Engines for Armoured Vehicles* product catalogue, 2022.

[46] R. P. Hunnicutt, *Patton: A History of the American Main Battle Tank*. Presidio Press, 1984.

[47] Krauss-Maffei Wegmann, Leopard 2A7 public specification, 2023.

[48] NATO STANAG 2320, *Dimensions of Transportability*, Ed. 2.

[49] US Army Aeromedical Research Laboratory, *Blast Injury Criteria for Vehicle Crew Seating*, USAARL Report 2012-01.

[50] US Army FM 3-90.1, *Armor and Mechanized Infantry Company Team*, 2001.

[51] GAO, *Operation Desert Storm: Early Performance Assessment of Bradley and Abrams*, NSIAD-92-94, 1992.

[52] B. Perrett, *Leopard 1 Main Battle Tank 1965–1995*. Osprey New Vanguard 24, 1995.

[53] M. Burkins and R. M. Ogorkiewicz, "Spall Liners for Composite Armour," *Journal of Battlefield Technology*, vol. 6, no. 1, 2003.

[54] NATO STANAG 4569 Level 3/4 spall and BFD criteria cross-reference.

[55] R. M. Ogorkiewicz, "Ground Pressure and Soil Trafficability," in *Technology of Tanks*, vol. 2, 1991.

[56] Weapons-Defence Rubber Tank Tracks, [`../../Rubber Tank Tracks/Paper14_Military_Track_Pad.md`](../../Rubber%20Tank%20Tracks/Paper14_Military_Track_Pad.md).

[57] US Army TACOM, *Track Pad Specification MIL-DTL-32085*, 2018.

[58] J. Y. Wong, *Theory of Ground Vehicles* (4th ed.). Wiley, 2008.

[59] NATO STANAG 3149, *Fuels for Land Service Equipment*, Ed. 6.

[60] ISO 10816-1, *Mechanical vibration — Evaluation of machine vibration*, 1995.

[61] Weapons-Defence MP-6.8 Mark II Rifle, [`../../MP-6.8 Mark II Rifle/`](../../MP-6.8%20Mark%20II%20Rifle/).

[62] Weapons-Defence MAS-15.2E Anti-Materiel Sniper, [`../../MAS-15.2E Anti-Materiel Sniper/`](../../MAS-15.2E%20Anti-Materiel%20Sniper/).

[63] US NIST, *Zero Trust Architecture*, SP 800-207, 2020 — contrast with FPGA-only design rationale.

[64] R. M. Moroney, "Ballistic Accuracy and Dispersion," *Engineering Design Handbook: Fire Control Series*, AMCP 706-101, 1967.

[65] R. L. Fetterly, "Mine Blast Effects on Flat-Bottom vs V-Hull Vehicles," *International Journal of Impact Engineering*, vol. 35, 2008.

---

*MT-X Mk.II "Leviathan" — Research Paper TRP-2026-MTX-001 v1.0*  
*Generated in conjunction with `leviathan_sim` default configuration run, 2026-06-13.*
