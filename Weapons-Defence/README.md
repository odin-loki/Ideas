# Weapons-Defence — defence-tech R&D portfolio

> **A defence-engineering portfolio formatted as the kind of internal R&D documentation a small-team systems-research division would produce.** Every top-level platform has a paired operator specification and a TRP-numbered research paper, across **small-arms** (`MP-4.6M Guardian` pistol, `MP-4.6M Defender` PDW, `MP-6.8 Mark II` rifle, `MAS-15.2E` 15.2 mm anti-materiel sniper, **`BSG-10 Goliath`** 10-gauge bullpup combat shotgun), **heavy weapons** (`57 mm` autocannon, `57 mm` underbarrel grenade, `57 mm` dual-purpose mortar / RPG, `140 mm` electrothermal-chemical tank gun firing a KE round), **body armour** (`APES`, `AlNiCyN` three-tier aluminium, `OBSIDIAN` / `OBSIDIAN-X` hypothetical), **CBRN** (`NACS / NEXUS Adaptive Combat System`), **acoustic cancellation** (`TACS` three-variant family at 35–55 dB depth), **hearing protection** + **command doctrine** + **caseless / cartridgeless ammunition** + **CL-20** energetics + **rubber tank-track pads**, plus the **`HPR-X`** guided high-power rocketry series, the **`TACT-1 Mark II`** full-day SOF ration (with `PODS` high-energy glycerolipid subfolder and **`ASNP`** sports-nutrition powder spec), the **`HEL-CMS/DB`** diamond-battery-powered 280 kW laser air-defence platform, and the **`TAIPAN-1`** guided ballistic interceptor rocket.

> **Every ballistic / velocity / energy / penetration / chamber-pressure number in every spec sheet and every research paper in this folder is derived from a single Python simulator** ([`weapons_simulation.py`](weapons_simulation.py)). The human-readable simulator output lives in [`weapons_sim_results.md`](weapons_sim_results.md) — *that file is the authoritative source*. The parts-commonality matrix across the family lives in [`Common Architecture and Components.md`](Common%20Architecture%20and%20Components.md).

> **Genre note.** Documents adopt a defence-research register (Advanced Defence Systems Research Division, UNCLASSIFIED / FOR OFFICIAL USE ONLY) for tonal coherence. No real classification, no real programme office, and no fielded systems are implied. Several of the v1.0 spec sheets carried optimistic muzzle velocities, magazine capacities, and RHA penetration figures that are now **explicitly retracted** at the top of each rewritten spec; see the per-spec "Corrections from earlier draft" call-outs.

---

## What this folder is

Defence-engineering documentation has a very particular register — paired specification + research-paper documents, TRP designators, comparative tables against fielded incumbents, classification banners, explicit human-factors and safety considerations. Most "speculative weapons" content on the open web is written in fiction-author register and mixes the technical with the operatic. This folder takes the opposite tack: adopt the *defence-engineering documentation register* and produce a consistent multi-platform portfolio inside that register, with every numerical claim **traceable to a single physics simulator and a single common-architecture spec**.

Two pieces of infrastructure make this work:

1. **`weapons_simulation.py`** — a Python physics simulator. **Tier-1** covers internal ballistics (Le Duc / Powley closed-form, calibrated `η = 0.72` for small arms, `0.65` autocannon, `0.55` tank gun), external ballistics (G7/G1 drag tables, ICAO standard atmosphere, point-mass integration), and terminal ballistics (De Marre with `K = 7.80 × 10⁻⁴`, calibrated against M80 / .50 BMG / 14.5 × 114 reference points; Lanz–Odermatt-form long-rod model calibrated against M829-class DU data). Suppressor attenuation uses an adiabatic-expansion **40 dB upper bound**. Recoil is free-recoil energy via momentum conservation. **Tier-2** (added in v2) covers every other numerical claim made anywhere in the portfolio: muzzle-blast SPL + layered hearing-protection stack (foam / double / TACS), wind drift at 10 mph crosswind, bisection-zeroed bullet-drop tables, Hatcher max-effective-range, barrel-life and sustained-fire thermal bounds (calibrated against M4 / M14 / M2HB / GAU-8 / M256), peak recoil force with sprung-stock + muzzle-brake compensation, NATO-60° obliquity penetration, NIJ-style V50 and back-face deformation (calibrated against IIIA-9mm and IV-30-06-AP anchors), Gurney + Mott + Carlton fragmentation lethality, Birkhoff shaped-charge HEAT penetration, Tsiolkovsky-plus-drag rocketry trajectory for the HPR-X series, Kamlet–Jacobs CL-20 / HMX / RDX / TNT detonation pressure and velocity, Nelson–Elliott multi-mic-array TACS cancellation depth, 1-DOF mass-spring-damper tank-track-pad vibration transmission, one-compartment oral PK for the HyperSynergy-X7 stack, Plumb / Holliday-Segar osmolality for the injectable nutrition, and Q10 = 2 Arrhenius lipid-oxidation shelf life for the TACT-1 ration.
2. **`Common Architecture and Components.md`** — the parts-commonality matrix: shared cartridges (the 4.6 × 30 mm Enhanced is one and the same round across the pistol and PDW; the 57 × 347 mm casing is shared across the autocannon and the underbarrel-grenade / mortar variants by tube-internal sleeving), shared action components (one rotating-bolt geometry across the 4.6 family; one S7 tool-steel trigger / sear / extractor recipe across every small-arm), shared barrel-liner alloy (Stellite-21 across `4.6 / 6.8 / 15.2 / 57 / 140`), shared propellant chemistry, shared optic-rail standard (MIL-STD-1913 across the whole portfolio), and shared body-armour materials between APES (military) and APES-L (police).

The result reads like a small-team defence-systems portfolio that has done the unglamorous work of consolidating its parts catalogue.

---

## 📐 Single source of truth — the simulator

| File | Role |
|---|---|
| [`weapons_simulation.py`](weapons_simulation.py) | The simulator. **Tier-1**: internal / external / terminal ballistics, recoil, suppressor attenuation (calibrated against M80 7.62 NATO, M2 .50 BMG AP, 14.5 × 114 B-32 AP, M829-class DU long-rod, and 30 mm GAU-8 data points). **Tier-2**: muzzle SPL + hearing-protection stack, wind drift, zeroed bullet-drop tables, max effective range, barrel life + sustained-fire thermal bound, peak recoil force, obliquity penetration, body-armour V50 + BFD, HE-frag Gurney / Mott / Carlton lethal area, HEAT shaped-charge penetration, HPR-X rocket trajectory, Kamlet–Jacobs detonation chemistry, TACS cancellation depth, track-pad vibration transmission, combat-drug PK, injectable-nutrition osmolality, ration shelf-life. **22 tables in the results file.** |
| [`weapons_sim_results.md`](weapons_sim_results.md) | Human-readable simulator output (22 tables, ~23 kB). Re-generated whenever cartridge geometry, barrel length, armour layup, warhead loadout, rocket stage, drug dose, or formulation changes. **Cite this file in every spec sheet and paper.** |
| [`weapons_sim_results.json`](weapons_sim_results.json) | Machine-readable simulator output (~90 kB), for downstream tooling. |
| [`Common Architecture and Components.md`](Common%20Architecture%20and%20Components.md) | The parts-commonality matrix. Shared cartridges, shared bolt-face geometry, shared trigger packs, shared barrel-liner alloy, shared propellant chemistry, shared optic rail, shared body-armour materials. |

If you change a number in a spec sheet that doesn't trace back to `weapons_sim_results.md`, you have introduced a discrepancy. Re-run the simulator and update the spec instead.

---

## 📑 Source organisation

### Top-level small arms — operator spec + paired research paper

| System | Cartridge | Operator spec | Research paper |
|---|---|---|---|
| **MP-4.6M Guardian Pistol** | 4.6 × 30 mm Enhanced | [`MP-4.6M Pistol.md`](MP-4.6M%20Pistol.md) | [`Research Papers/Paper9_MP46M_Pistol.md`](Research%20Papers/Paper9_MP46M_Pistol.md) |
| **MP-4.6M Defender PDW** | 4.6 × 30 mm Enhanced *(same cartridge as the Guardian)* | [`MP-4.6M Defender PDW.md`](MP-4.6M%20Defender%20PDW.md) | [`Research Papers/Paper8_MP46M_PDW.md`](Research%20Papers/Paper8_MP46M_PDW.md) |
| **MP-6.8 Mark II Rifle** | 6.8 × 51 mm | [`MP-6.8 Advanced Combat Rifle.md`](MP-6.8%20Advanced%20Combat%20Rifle.md) | [`Research Papers/Paper10_MP68_Rifle.md`](Research%20Papers/Paper10_MP68_Rifle.md) |
| **MAS-15.2E Anti-Materiel Sniper** | 15.2 × 115 mm APYT | [`15.2mm Anti-Tank Sniper System.md`](15.2mm%20Anti-Tank%20Sniper%20System.md) | [`Research Papers/Paper1_MAS152E_AntiTank_Sniper.md`](Research%20Papers/Paper1_MAS152E_AntiTank_Sniper.md) |

### Top-level heavy weapons — operator spec + paired research paper

| System | Cartridge | Operator spec | Research paper |
|---|---|---|---|
| **57 mm Autocannon** | 57 × 347 mm | [`57mm Advanced Mechanical Autocannon System.md`](57mm%20Advanced%20Mechanical%20Autocannon%20System.md) | [`Research Papers/Paper2_57mm_Autocannon.md`](Research%20Papers/Paper2_57mm_Autocannon.md) |
| **57 mm Underbarrel Grenade** | 57 mm LV grenade *(same casing geometry as the autocannon, low-velocity reload)* | [`57mm Underbarrel Grenade Round.md`](57mm%20Underbarrel%20Grenade%20Round.md) | [`Research Papers/Paper4_57mm_Underbarrel_Grenade.md`](Research%20Papers/Paper4_57mm_Underbarrel_Grenade.md) |
| **57 mm Mortar / RPG dual-purpose** | 57 mm mortar | [`57mm Enhanced Dual-Purpose System Mortar and RPG.md`](57mm%20Enhanced%20Dual-Purpose%20System%20Mortar%20and%20RPG.md) | [`Research Papers/Paper3_57mm_DualPurpose_System.md`](Research%20Papers/Paper3_57mm_DualPurpose_System.md) |
| **140 mm Tank KE Round** | 140 mm KE | [`140mm Advanced Multi-Effect Tank Round.md`](140mm%20Advanced%20Multi-Effect%20Tank%20Round.md) | [`Research Papers/Paper5_140mm_Tank_Round.md`](Research%20Papers/Paper5_140mm_Tank_Round.md) |

### Protective equipment and systems

| System | Operator spec | Research paper |
|---|---|---|
| **APES Body Armour** *(military)* | [`Advanced Protective Equipment System Specification.md`](Advanced%20Protective%20Equipment%20System%20Specification.md) | [`Research Papers/Paper6_Body_Armor_System.md`](Research%20Papers/Paper6_Body_Armor_System.md) |
| **APES-L Mark I** *(police variant; cross-folder)* | [`../Weapons-Police/APES-L Mark I Police Body Armour.md`](../Weapons-Police/APES-L%20Mark%20I%20Police%20Body%20Armour.md) | [`../Weapons-Police/Research Paper — APES-L Police Body Armour.md`](../Weapons-Police/Research%20Paper%20%E2%80%94%20APES-L%20Police%20Body%20Armour.md) |
| **NACS / NEXUS Adaptive Combat System** | [`NACS TOTAL Camo and Undersuit.md`](NACS%20TOTAL%20Camo%20and%20Undersuit.md) | [`Research Papers/Paper7_NACS_CBRN_System.md`](Research%20Papers/Paper7_NACS_CBRN_System.md) |
| **AlNiCyN three-tier aluminium armour** | [`Aluminium Alloys for Armour.md`](Aluminium%20Alloys%20for%20Armour.md) | [`Research Papers/Paper13_AlNiCyN_Aluminum_Armour.md`](Research%20Papers/Paper13_AlNiCyN_Aluminum_Armour.md) |
| **Hearing protection** | [`military_hearing_protection_systems.md`](military_hearing_protection_systems.md) | [`Research Papers/Paper15_Hearing_Protection.md`](Research%20Papers/Paper15_Hearing_Protection.md) |
| **Military command doctrine** | [`military_command_military_doctrine.md`](military_command_military_doctrine.md) | [`Research Papers/Paper16_Military_Command_Doctrine.md`](Research%20Papers/Paper16_Military_Command_Doctrine.md) |

### Specialised subfolders

| Subfolder | Contents |
|---|---|
| [`Military Noise Cancellation/`](Military%20Noise%20Cancellation/) | **TACS** Tactical Acoustic Cancellation System — three variants (Personal / Mobile / Fixed), 35–55 dB cancellation depth at nodes, < 100 µs latency. [`TACS_Complete_Specification.md`](Military%20Noise%20Cancellation/TACS_Complete_Specification.md), [`Paper11_TACS_System.md`](Military%20Noise%20Cancellation/Paper11_TACS_System.md), [`Paper12_TACS_Energy_Physics.md`](Military%20Noise%20Cancellation/Paper12_TACS_Energy_Physics.md), [`TACS_Energy_Conservation_Analysis.md`](Military%20Noise%20Cancellation/TACS_Energy_Conservation_Analysis.md). |
| [`Rubber Tank Tracks/`](Rubber%20Tank%20Tracks/) | MIL-SPEC track-pad TDP (TRP-2026-014) — HNBR/NBR/NR/Neoprene blend, score 6 679 / 10 000, 15–20 dB noise reduction vs steel. [`Paper14_Military_Track_Pad.md`](Rubber%20Tank%20Tracks/Paper14_Military_Track_Pad.md), [`MIL_SPEC_TRACK_PAD_TDP.md`](Rubber%20Tank%20Tracks/MIL_SPEC_TRACK_PAD_TDP.md), [`EXECUTIVE_SUMMARY.md`](Rubber%20Tank%20Tracks/EXECUTIVE_SUMMARY.md). |
| [`CL-20 High Explosive/`](CL-20%20High%20Explosive/) | Proteinated CL-20 safe-handling explosive paper — [`Proteinated_CL20_Safe_Explosive_Paper.md`](CL-20%20High%20Explosive/Proteinated_CL20_Safe_Explosive_Paper.md), [`CL-20 HE Readme.md`](CL-20%20High%20Explosive/CL-20%20HE%20Readme.md). |
| [`HPR-X Rocketry/`](HPR-X%20Rocketry/) | **HPR-X** guided high-power rocketry series — multi-stage solid-propellant, optional IMU + GPS guidance, civilian-amateur-class through SOF spotter-class. [`README.md`](HPR-X%20Rocketry/README.md), [`HPR-X Series Spec.md`](HPR-X%20Rocketry/HPR-X%20Series%20Spec.md), [`Paper19_HPR-X_Guided_Rocketry.md`](HPR-X%20Rocketry/Paper19_HPR-X_Guided_Rocketry.md). |
| [`TACT-1 Tactical Ration/`](TACT-1%20Tactical%20Ration/) | **TACT-1 Mark II** full-day SOF ration + **ASNP** sports-nutrition powder. [`README.md`](TACT-1%20Tactical%20Ration/README.md), [`TACT-1 Mark II Specification.md`](TACT-1%20Tactical%20Ration/TACT-1%20Mark%20II%20Specification.md), [`TACT-1 Mark II Flavour Catalogue.md`](TACT-1%20Tactical%20Ration/TACT-1%20Mark%20II%20Flavour%20Catalogue.md), [`Paper20_TACT-1_Mk_II_Ration.md`](TACT-1%20Tactical%20Ration/Paper20_TACT-1_Mk_II_Ration.md), [`Advanced Sports Nutrition Powder.md`](TACT-1%20Tactical%20Ration/Advanced%20Sports%20Nutrition%20Powder.md), [`Research Papers/ASNP_Energy_Drink_Research_Paper.md`](Research%20Papers/ASNP_Energy_Drink_Research_Paper.md). Subfolder: [`PODS- Edible High Energy Protein/`](TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/) — synthetic glycerolipid (10.21 kcal/g computed; programmable three-phase release). |
| [`BSG10 Goliath/`](BSG10%20Goliath/) | **BSG-10 Goliath** 10-gauge semi-automatic bullpup combat shotgun — standalone `bsg10_sim` validation (not `weapons_simulation.py`). 45-round drum, ~490 N peak shoulder force, 415 m/s MV. [`README.md`](BSG10%20Goliath/README.md), [`BSG10_Goliath_Full_Specification.md`](BSG10%20Goliath/BSG10_Goliath_Full_Specification.md), [`BSG10_Research_Paper.md`](BSG10%20Goliath/BSG10_Research_Paper.md), [`bsg10_sim_package/`](BSG10%20Goliath/bsg10_sim_package/). |
| [`HEL_CMS_DB Laser AntiAir/`](HEL_CMS_DB%20Laser%20AntiAir/) | **HEL-CMS/DB** High-Energy Laser Counter-Munitions System, Diamond Battery powered — 280–300 kW spectral-beam-combined fiber laser air defence platform. Defeats micro-UAVs (0.2 s dwell), rockets (4.9 s dwell), and cruise missiles (12.3 s dwell) across a 4–7 km engagement envelope. 1 MW(e) Sr-90 thermal-betavoltaic power plant eliminates the generator logistics tail; zero crew; 20-year TCO $71.8M saving $51.8M vs conventional HEL. TDB power source at TRL 2–3. [`README.md`](HEL_CMS_DB%20Laser%20AntiAir/README.md), [`HEL_CMS_DB_Full_Spec.md`](HEL_CMS_DB%20Laser%20AntiAir/HEL_CMS_DB_Full_Spec.md), [`HEL_CMS_DB_Research_Paper.md`](HEL_CMS_DB%20Laser%20AntiAir/HEL_CMS_DB_Research_Paper.md). |
| [`TAIPAN Missile/`](TAIPAN%20Missile/) | **TAIPAN-1** guided ballistic interceptor rocket — 4.87 m, 631 kg wet, RP-1/LOX electric pump-fed (50 kN, Isp 293.1 s, 62 kg dry engine mass). Simulation-verified maximum range **1,618 km** at Mach 13.27 and 367 km apogee; configurable 432–1,618 km by varying nose ballast. Production unit cost **$50k–$80k** (22× cheaper than AMRAAM at 160 km). Entire airframe 3D printed in 14 structural parts. [`README.md`](TAIPAN%20Missile/README.md), [`TAIPAN-1_Technical_Specification_Rev1.0.md`](TAIPAN%20Missile/TAIPAN-1_Technical_Specification_Rev1.0.md), [`TAIPAN-1_Financial_Analysis_Rev1.0.md`](TAIPAN%20Missile/TAIPAN-1_Financial_Analysis_Rev1.0.md), [`TAIPAN-1_Geometry_Reference_Rev1.0.md`](TAIPAN%20Missile/TAIPAN-1_Geometry_Reference_Rev1.0.md), [`taipan1_sim.py`](TAIPAN%20Missile/taipan1_sim.py). |

### Hypothetical / academic-study items

| Item | File |
|---|---|
| **OBSIDIAN body armour (hypothetical)** | [`Research Papers/OBSIDIAN_Research_Paper.md`](Research%20Papers/OBSIDIAN_Research_Paper.md) |
| **OBSIDIAN-X body armour (hypothetical)** | [`Research Papers/OBSIDIAN_X_Research_Paper.md`](Research%20Papers/OBSIDIAN_X_Research_Paper.md), [`Hypothetical Body Armour.md`](Hypothetical%20Body%20Armour.md) |
| **Hypothetical secret-service suit** | [`Hypothetical_secret_service_suit_specs.md`](Hypothetical_secret_service_suit_specs.md) |
| **Combat drug — HyperSynergy-X7** | [`Combat Drug.md`](Combat%20Drug.md), [`Research Papers/Paper18_HyperSynergy_X7_Combat_Drug.md`](Research%20Papers/Paper18_HyperSynergy_X7_Combat_Drug.md) — mirrored to [`../Drugs/Combat Drug.md`](../Drugs/Combat%20Drug.md) |
| **Injectable nutrition** | [`Injectable Food.md`](Injectable%20Food.md), [`Research Papers/Paper17_Injectable_Nutrition.md`](Research%20Papers/Paper17_Injectable_Nutrition.md) — mirrored to [`../Drugs/Injectable Food.md`](../Drugs/Injectable%20Food.md) |
| **ASNP sports-nutrition powder** | [`TACT-1 Tactical Ration/Advanced Sports Nutrition Powder.md`](TACT-1%20Tactical%20Ration/Advanced%20Sports%20Nutrition%20Powder.md), [`Research Papers/ASNP_Energy_Drink_Research_Paper.md`](Research%20Papers/ASNP_Energy_Drink_Research_Paper.md) |
| **Caseless / cartridgeless bullets** | [`Caseless Bullets_README.md`](Caseless%20Bullets_README.md), [`Research Papers/Cartridgeless Bullets_Research_Paper.md`](Research%20Papers/Cartridgeless%20Bullets_Research_Paper.md) |

---

## 🎯 Headline simulator numbers — *single source of truth*

All numbers below come from [`weapons_sim_results.md`](weapons_sim_results.md). Any spec sheet that disagrees with this table is wrong; report it as a bug.

### Small arms

| Weapon | Cartridge | MV | ME | Pₘₐₓ | Free recoil | RHA @ muzzle | Magazine |
|---|---|---|---|---|---|---|---|
| **MP-4.6M Guardian Pistol** | 4.6 × 30 mm | **501 m/s** | **326 J** | 180 MPa (26 107 psi) | 1.5 J (1.1 ft·lb) | 3.8 mm | 20 rd |
| **MP-4.6M Defender PDW** *(same cartridge as the Guardian)* | 4.6 × 30 mm | **501 m/s** | **326 J** | 180 MPa | 0.7 J (0.5 ft·lb) | 3.8 mm | 40 rd |
| **MP-6.8 Mark II Rifle** | 6.8 × 51 mm | **731 m/s** | **2 324 J** | 307 MPa (44 538 psi) | 11.3 J (8.3 ft·lb) | 11.1 mm | 20 rd |
| **MAS-15.2E Anti-Materiel Sniper** | 15.2 × 115 mm APYT | **781 m/s** | **19 505 J** | 258 MPa (37 361 psi) | 255.2 J (188.2 ft·lb) | 48.4 mm | 8 rd, bolt-action |

### Heavy weapons

| Weapon | Cartridge | MV | ME | Pₘₐₓ | Free recoil | RHA @ muzzle |
|---|---|---|---|---|---|---|
| **57 mm Autocannon** | 57 × 347 mm | 948 m/s | 1.08 MJ | 257 MPa | 27.6 kJ | 139.7 mm |
| **57 mm Underbarrel Grenade** | 57 mm LV | 149 m/s | 3.87 kJ | 109 MPa | 579 J | n/a *(HE-frag warhead)* |
| **57 mm Mortar / RPG** | 57 mm mortar | 187 m/s | 24.4 kJ | 111 MPa | 4.97 kJ | n/a *(HE / HEAT warhead)* |
| **140 mm Tank KE Round** | 140 mm KE | **1 698 m/s** | **9.23 MJ** | 198 MPa | 351.7 kJ (recoil-mitigated) | **867 mm @ muzzle, 698 mm @ 500 m, 541 mm @ 1 km, 327 mm @ 2 km** |

### RHA penetration vs range (small arms, mm)

| Cartridge | 100 m | 300 m | 500 m | 800 m | 1 000 m | 1 500 m |
|---|---|---|---|---|---|---|
| 4.6 × 30 mm | 3.1 | 2.2 | 1.8 | 1.5 | 1.3 | 0.9 |
| 6.8 × 51 mm | 10.1 | **8.1** | 6.5 | 4.7 | 3.9 | 3.0 |
| 15.2 × 115 mm | 45.7 | 40.5 | 35.8 | 29.5 | **25.8** | 18.5 |

*(For reference: 5.56 × 45 mm sims at 6.6 mm @ 100 m / 4.8 mm @ 300 m; 7.62 × 51 mm at 8.6 mm @ 100 m / 6.7 mm @ 300 m; 14.5 × 114 mm AP at 34.9 mm @ 100 m / 19.9 mm @ 1 km.)*

### Suppressor attenuation (adiabatic-expansion upper bound, capped at 40 dB)

| Weapon | Chamber vol | Suppressor vol | Baffles | Attenuation |
|---|---|---|---|---|
| MP-4.6M Pistol integral | 1.0 cm³ | 80 cm³ | 6 | 40 dB |
| MP-4.6M Defender PDW | 1.0 cm³ | 180 cm³ | 8 | 40 dB |
| MP-6.8 Mark II Rifle | 3.5 cm³ | 410 cm³ | 7 | 40 dB |
| MAS-15.2E Sniper | 39.0 cm³ | 1 800 cm³ | 10 | 40 dB |

> The 40 dB number is a **modelled upper bound**, not a measured value. Real K-baffle suppressors typically achieve **25 – 35 dB** depending on baffle count, internal volume, and porting. The simulator caps at 40 dB to prevent unrealistic claims.

---

## 🧠 Other headline specs (non-simulator infrastructure)

### NACS / NEXUS Adaptive Combat System (TRP-2026-007)

72 h sealed operations. GORE-Tex CHEMPAK core. **65–92 % IR signature reduction** (overgarment). GHOST rebreather: dual 300 bar cylinders, LiOH scrubbing (`2 LiOH + CO₂ → Li₂CO₃ + H₂O`). Per-unit cost **AUD ~$504** at 50 000-unit volume.

### TACS (Tactical Acoustic Cancellation)

| Variant | Cancellation zone | Depth at nodes | Anti-node | Power | Weight | Latency |
|---|---|---|---|---|---|---|
| **Personal** | 3 – 5 m | 35 – 55 dB | +3 – 6 dB | 35 – 70 W | 5.5 kg | **< 100 µs** |
| **Mobile** | 8 – 15 m | (same) | (same) | 0.8 – 1.8 kW | 245 kg | (same) |
| **Fixed** | 30 – 60 m | (same) | (same) | 3 – 8 kW | 1 800 kg | (same) |

Programme framing: USD 22 M, 36-month timeline; per-unit USD 28 K / 185 K / 850 K. **Acoustic energy is redistributed, not destroyed** — anti-node hazards are explicit in the papers.

### APES Body Armour (TRP-2026-006)

16-layer Kevlar / UHMWPE with graphene interfaces. 7075-T6 honeycomb + B₄C ceramic + Ti-6Al-4V. Non-Newtonian silicone shock-absorber. 20.8 kg full kit. < 3 s emergency doff. PCM thermal at 28 °C, 200 kJ/kg, 25 % body coverage → 4 h thermal budget. **The police APES-L variant in [`../Weapons-Police/`](../Weapons-Police/) shares the B4C tile, ionic-liquid STF chemistry, and aramid panel architecture; the police variant trades the 75 mm helmet ceramic and 25 mm body tile for a single 6.5 kg full-body suit.**

### AlNiCyN Aluminium Armour (TRP-2026-013)

| Tier | Strength | Hardness | RHA equivalent | Cost | TRL |
|---|---|---|---|---|---|
| **AlNiCyN-5000** | 620 MPa | 380 – 420 HB | 1.0 × RHA | USD 11 830 / t | **7 – 8** (near-deployable) |
| **AlNiCyN-7000** | 780 MPa | 550 – 650 HV | (improved) | USD 168 900 / t | 4 – 5 |
| **AlNiCyN-X** | (target) | (target ~2 000 GPa modulus) | (target) | USD 320 000 / kg | 2 – 3 (frontier) |

### Hypothetical OBSIDIAN family

| System | Mass | Strength target | Programme cost | Status |
|---|---|---|---|---|
| **OBSIDIAN** | 11.8 kg | (≥ 4-layer stack) | USD ~40 M / unit | **Hypothetical / For Academic Study** |
| **OBSIDIAN-X** | 18.5 kg | 5 × strength target | **USD 3.1 trillion** programme | **Hypothetical / For Academic Study** |

---

## 🆕 What's new in this revision

1. **Single-source-of-truth simulator.** Every cartridge / muzzle-velocity / muzzle-energy / chamber-pressure / RHA-penetration / free-recoil / suppressor-attenuation number is now derived from `weapons_simulation.py`. The previous v1.0 drafts contained several un-physical numbers (4.6 mm pistol claimed 1 120 m/s, 6.8 mm rifle claimed 1 000 m/s and 4 000 J, 15.2 mm sniper claimed 30 mm RHA at 1 000 m). These are explicitly **retracted at the top of every rewritten spec sheet** under the "Corrections from earlier draft" heading.
2. **`Common Architecture and Components.md`** — new document. Defines shared cartridges, shared bolt-face geometry, shared trigger / sear / extractor recipe, shared barrel-liner alloy, shared propellant chemistry, shared optic-rail standard, shared body-armour materials between APES (military) and APES-L (police). Net spares-SKU reduction across the portfolio: ~62 % vs no-commonality baseline.
3. **Pistol corrections.** The MP-4.6M Guardian pistol spec was the one that most needed simulator backing. It now uses the 4.6 × 30 mm Enhanced cartridge (common with the PDW), the simulator-validated 501 m/s / 326 J / 180 MPa numbers, a single-action semi-only fixed-barrel rotating-bolt short-recoil action, 20-round magazine, 180 mm barrel, and 1.5 J free recoil. The previous 1 120 m/s / 1 752 J / 58 000 psi / 30-round / 900 rpm claims are retracted.
4. **PDW shares parts and cartridges with the pistol.** Same 4.6 × 30 mm Enhanced cartridge, same bolt face, same trigger pack, same magazine well — only the action mass, barrel length, and buffer differ.
5. **6.8 mm rifle magazine corrected** from 50 to 20 rounds (50 was a SAW-spec figure).
6. **15.2 mm sniper action corrected** from semi-automatic gas-piston to bolt-action three-lug rotating bolt (gas-piston primary extraction is marginal at the simulator-validated 258 MPa peak chamber pressure).
7. **Two new platforms (previous revision).** The HPR-X guided rocketry series and the TACT-1 Mark II SOF ration both get full subfolder treatment (operator spec + research paper + README in each).
8. **Police cross-link.** The new [`../Weapons-Police/`](../Weapons-Police/) folder publishes APES-L, a police-doctrine variant of the military APES armour, sharing materials and chemistry but trading the strike-face ceramic and full-tile architecture for a lighter (6.5 kg) full-body suit.
9. **Three new platforms (this revision).**
   - [`HEL_CMS_DB Laser AntiAir/`](HEL_CMS_DB%20Laser%20AntiAir/) — HEL-CMS/DB directed-energy air defence platform (280 kW, diamond battery powered, zero fuel logistics, fully autonomous).
   - [`TAIPAN Missile/`](TAIPAN%20Missile/) — TAIPAN-1 guided ballistic interceptor (1,618 km range, $50–80k production cost, fully 3D-printed 14-part airframe, electric pump-fed RP-1/LOX engine).
   - [`TACT-1 Tactical Ration/PODS- Edible High Energy Protein/`](TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/) — PODS synthetic glycerolipid subfolder added to the TACT-1 ration portfolio (10.21 kcal/g computed energy density, programmable three-phase energy release).
10. **Three new items (this revision).**
   - [`BSG10 Goliath/`](BSG10%20Goliath/) — BSG-10 Goliath 10-gauge bullpup combat shotgun with dedicated `bsg10_sim` package (spec + research paper + folder README).
   - [`TACT-1 Tactical Ration/Advanced Sports Nutrition Powder.md`](TACT-1%20Tactical%20Ration/Advanced%20Sports%20Nutrition%20Powder.md) — ASNP operator spec added as fourth UCN combat-nutrition pillar (paired with existing ASNP research paper).
   - [`../Threat Asessments/`](../Threat%20Asessments/) — Hypothetical threat-intelligence briefs (FSB neurological interference; 2-NT/TNT mixture) with folder README.

---

## 🚧 Honest caveats

- **Classification banners are illustrative, not real.** UNCLASSIFIED / FOUO format adopted for tonal coherence.
- **Simulator numbers are not measured prototype data.** They are the output of `weapons_simulation.py`, which is calibrated against published reference cartridges (M80 7.62 NATO, M2 .50 BMG AP, 14.5 × 114 B-32 AP, M829-class DU long-rod). The simulator is *consistent* and *physics-anchored*, but not a replacement for instrumented testing on a real prototype.
- **The 40 dB suppressor attenuation is a modelled upper bound.** Real prototypes typically achieve 25–35 dB.
- **OBSIDIAN, OBSIDIAN-X, and OBSIDIAN-class hypotheticals are explicitly low-TRL.** Read separately from the simulator-validated small-arms specs.
- **TACS warns of anti-node hazards.** Acoustic energy is redistributed, not destroyed; standing in an anti-node is dangerous.
- **NACS pharmacology stack** (caffeine + modafinil + dextroamphetamine) is contested ethically and legally in real militaries.
- **140 mm KE round penetration is from a long-rod model.** The simulator gives ~867 mm RHA at muzzle / ~541 mm at 1 km. This is in the published-NATO-APFSDS range (M829-class DU) and is a reasonable design-target, but is not a measured prototype performance.
- **Combat drug and injectable nutrition are speculative monographs.** Not medical advice; do not synthesise, possess, or administer.

---

## 🔗 Related work in this repo

- [`Common Architecture and Components.md`](Common%20Architecture%20and%20Components.md) — the parts-commonality matrix for this folder
- [`weapons_simulation.py`](weapons_simulation.py) / [`weapons_sim_results.md`](weapons_sim_results.md) — the simulator and its tabulated output
- [`../Weapons-Police/`](../Weapons-Police/) — APES-L police body armour (same chemistry as APES)
- [`../Rockwell 50 to 70 Carbide/`](../Rockwell%2050%20to%2070%20Carbide/) — sovereign manufacturing (the H13 breech-bolt exemplar; same carbide-tooling supply chain serves these weapons)
- [`../Diffusion Welding/`](../Diffusion%20Welding/) — UCDW field-repair-tier joining process
- [`../Drugs/`](../Drugs/) — pharmacology research (Combat Drug and Injectable Food cross-reference)
- [`../GM Enhancements/`](../GM%20Enhancements/) — HSA enhancement protocol (Super Soldier programme adjacency)
- [`../Diamond Batterys/`](../Diamond%20Batterys/) — sovereign energy that field-deployable systems would draw on
- [`../UCN Political System/`](../UCN%20Political%20System/) — UCN doctrine and `≤ 10`-warhead defence posture
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — ARIA-INTEL battlefield intelligence
- [`../Filtering/`](../Filtering/) — GH-SR-IMM platform-state estimation
- [`../Threat Asessments/`](../Threat%20Asessments/) — Hypothetical threat-assessment monographs (intelligence register)

---

[← Back to main README](../README.md)
