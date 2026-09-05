# MT-X Mk.II Leviathan — Simulation Report

Generated: 2026-09-05 00:14 UTC

## Executive summary

- **Combat mass:** 38,000.0 kg (budget delta -7000.0 kg)
- **Power-to-weight:** 34.21 hp/t
- **Max road speed:** 65.0 km/h (modelled power limit 90.0 km/h)
- **Ground pressure:** 66.9 kPa
- **Upper glacis (ERA):** 779.1 mm eff. RHA
- **Main gun ROF:** 8.0 rpm (34 rounds stowed)
- **Portfolio KE @ 2 km:** 326.7 mm RHA
- **Unit cost (ex ammo):** $5.82M

## Mobility

- **power_to_weight_hp_t:** 34.21
- **ground_pressure_kpa:** 66.9
- **track_contact_area_m2:** 5.57
- **max_road_speed_kmh:** 65.0
- **power_limited_speed_kmh:** 90.0
- **power_at_spec_vmax_kw:** 148.0
- **installed_power_kw:** 969.0
- **grade_speed_kmh:**
  - **0:** 54.0
  - **5:** 54.0
  - **10:** 24.9
  - **15:** 11.8
  - **20:** 5.0
  - **25:** 0.8
  - **30:** 0.0
- **max_surmountable_grade_deg:** 31
- **trench_crossing_m:** 2.8
- **vertical_step_m:** 1.1
- **fuel_capacity_L:** 1400.0
- **modelled_range_km:** 600.0
- **spec_range_km:** 600
- **fuel_consumption_L_per_100km:** 233.3
- **turning_radius_m:** 8.5

## Armour (headline zones)

| Zone | Physical (mm) | Eff. RHA | With ERA |
|------|---------------|----------|----------|
| upper_glacis | 110 | 529.1 | 779.1 |
| lower_glacis | 130 | 226.6 | 476.6 |
| hull_side_upper | 80 | 82.8 | 332.8 |
| hull_side_lower | 60 | 60.0 | 60.0 |
| turret_front_primary | 200 | 772.7 | 1072.7 |
| turret_front_cheek | 180 | 526.3 | 826.3 |
| turret_roof | 40 | 40.6 | 40.6 |
| hull_roof_crew | 50 | 50.8 | 50.8 |

## Main armament

- **ROF:** 8.0 rpm
- **Recoil force:** 81.0 kN

**Portfolio KE penetration (mm RHA):**

- 0 m: 867.1
- 500 m: 679.3
- 1000 m: 532.2
- 1500 m: 417.0
- 2000 m: 326.7
- 2500 m: 256.0
- 3000 m: 200.5

> Specification AMET claims (1950 m/s, 1450 mm @ 0 m) exceed portfolio-validated KEW-AP (1698 m/s, 867 mm @ 0 m). Sim reports both; use portfolio for cross-weapon comparisons.


## APS

- **radar_band:** Ka
- **detection_atgm_m:** 400.0
- **detection_rpg_m:** 250.0
- **engage_envelope_m:** [80.0, 250.0]
- **reaction_time_s:** 0.3
- **single_shot_pk:** 0.8
- **two_shot_pk:** 0.96
- **engagement_timeline:** (10 entries)
- **notes:** Model assumes head-on ATGM at 200 m/s; no multi-target saturation.

## Amphibious

- **combat_mass_kg:** 38000.0
- **displacement_m3:** 42.0
- **displacement_with_sponsons_m3:** 43.5
- **buoyancy_margin_percent:** 10.5
- **floats_without_preparation:** True
- **sponson_buoyancy_kg:** 3080.0
- **swim_speed_kmh:** 7.0
- **swim_power_kw:** 31.0
- **unprepared_ford_m:** 1.4
- **snorkel_depth_m:** 4.0
- **freeboard_forward_mm:** 200.0
- **notes:** Swim propulsion via track rotation; 6–8 km/h per specification. Reserve buoyancy must stay positive with full fuel and ammo.

## Weight budget

| Component | kg |
|-----------|-----|
| hull_structure | 8,200 |
| turret_structure | 3,100 |
| engine | 2,800 |
| transmission_final_drives | 3,200 |
| running_gear | 4,400 |
| main_armament | 2,600 |
| secondary_armament | 380 |
| aps_ew | 220 |
| electronics | 180 |
| crew | 300 |
| troop_payload | 960 |
| fuel | 1,190 |
| ammunition | 2,100 |
| era_panels | 640 |
| miscellaneous | 730 |
| **Total** | **31,000** |
| Spec target | 38,000.0 |

## Cost

- **unit_price_ex_ammo_MUSD:** 5.82
- **unit_price_inc_ammo_MUSD:** 6.14
- **program_100_vehicles_BUSD:** 1.293
- **hybrid_bonding_saving_per_vehicle_USD:** 340000
- **cost_drivers:** ['AlNiCyN-5000 armour fabrication (hybrid bonding)', '140mm AMET and autoloader', 'PPU-1300 boxer engine', 'APS and sensor suite', 'rubber track running gear']
- **notes:** Central case from MT-X_Leviathan_Cost_Analysis.md; 100-unit production run.

## Full JSON

See `leviathan_sim_results.json` for machine-readable output.
