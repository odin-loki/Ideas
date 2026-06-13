# MT-X Mk.II Leviathan — simulation guide

**Dedicated platform simulation** via the local [`leviathan_sim_package/`](leviathan_sim_package/) suite. Unlike cartridge-level weapons in the parent portfolio, the Leviathan is a full vehicle — mobility, armour, powertrain, suspension, armament, APS, amphibious performance, fire control, weight budget, logistics, and unit cost are modelled in separate modules that converge in a consolidated report.

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the full `leviathan_sim` package and prints headline numbers. Use this from the tank folder root:

```bash
python platform_simulation.py
python platform_simulation.py --json
python platform_simulation.py --portfolio-check
```

Full suite (same engine, more verbose):

```bash
cd leviathan_sim_package
pip install -r leviathan_sim/requirements.txt
python run_all.py
```

Outputs land in [`leviathan_sim_package/leviathan_sim/outputs/`](leviathan_sim_package/leviathan_sim/outputs/):

| File | Role |
|---|---|
| `leviathan_sim_report.md` | Human-readable consolidated report |
| `leviathan_sim_results.json` | Machine-readable full results |

---

## Requirements

```bash
pip install numpy
```

Python 3.9+ required. No SciPy dependency for the default vehicle model.

---

## Simulation modules

| Module | Path | Models |
|---|---|---|
| **Mobility** | `mobility/performance.py` | Power-to-weight, ground pressure, grade speeds, road range |
| **Armour** | `armour/effective.py` | Oblique effective RHA, ERA credits, zone mass estimates |
| **Powertrain** | `powertrain/engine.py` | PPU-1300 torque curve, fuel consumption load points |
| **Suspension** | `suspension/ride.py` | Torsion-bar natural frequency, wheel travel |
| **Main armament** | `armament/main_gun.py` | 140 mm AMET autoloader, dual penetration tracks |
| **Secondary** | `armament/secondary.py` | MP-6.8 coax, 15.2 mm RWS |
| **APS** | `aps/engagement.py` | Detection envelope, reaction timeline, salvo Pk |
| **Amphibious** | `amphibious/flotation.py` | Buoyancy margin, swim power, fording |
| **FCS** | `fcs/hit_probability.py` | CEP-based first-round hit probability |
| **Weight** | `weight/budget.py` | Part XIX budget reconciliation |
| **Logistics** | `logistics/maintenance.py` | Crew, intervals, transport footprint |
| **Cost** | `cost/unit_cost.py` | Unit and program cost (central case) |
| **Report** | `reports/generate.py` | Markdown + JSON export |

All parameters live in [`leviathan_sim/config.py`](leviathan_sim_package/leviathan_sim/config.py).

---

## Cross-portfolio references

| Subsystem | Portfolio folder | Sim role |
|---|---|---|
| Main gun KE | [`../140mm Tank KE Round/`](../140mm%20Tank%20KE%20Round/) | **Portfolio-validated** penetration (867 mm @ 0 m, 327 mm @ 2 km) |
| Armour material | [`../AlNiCyN Armour/`](../AlNiCyN%20Armour/) | 1:1 RHA equivalent assumption |
| Coax | [`../MP-6.8 Mark II Rifle/`](../MP-6.8%20Mark%20II%20Rifle/) | Secondary armament spec |
| RWS | [`../MAS-15.2E Anti-Materiel Sniper/`](../MAS-15.2E%20Anti-Materiel%20Sniper/) | 15.2 mm remote weapon |
| Tracks | [`../Rubber Tank Tracks/`](../Rubber%20Tank%20Tracks/) | Running gear / ground pressure context |

### 140 mm penetration — dual track

The specification claims **AMET** performance (~1,950 m/s, ~1,450 mm @ 0 m, ~1,150 mm @ 2 km). The portfolio [`140mm Tank KE Round`](../140mm%20Tank%20KE%20Round/) simulator (corrected KEW-AP) reports **1,698 m/s**, **867 mm @ 0 m**, **327 mm @ 2 km**. The Leviathan sim reports **both** and flags the ~3.5× discrepancy at 2 km. Use **portfolio numbers** for cross-weapon comparisons; treat AMET claims as specification targets pending separate validation.

---

## Headline numbers (default run)

| Metric | Value |
|---|---|
| Combat mass | **38,000 kg** |
| Power-to-weight | **34.2 hp/t** |
| Max road speed | **65 km/h** |
| Ground pressure | **66.9 kPa** |
| Road range (diesel) | **600 km** (spec-calibrated) |
| Upper glacis (with ERA) | **779 mm** eff. RHA |
| Turret front (with ERA) | **1,073 mm** eff. RHA |
| Main gun ROF | **8 rpm** (7.5 s cycle) |
| Stowed main-gun rounds | **34** (22 bustle + 12 hull) |
| Portfolio KE @ 2 km | **326.7 mm** RHA |
| Spec AMET @ 2 km | **1,150 mm** RHA (unvalidated vs portfolio) |
| APS two-shot Pk | **0.96** |
| Swim speed | **7 km/h** |
| Buoyancy margin | **+10.5%** |
| Unit cost (ex ammo) | **$5.82M** |
| Weight budget (Part XIX sum) | **31,000 kg** → **−7,000 kg gap** vs 38 t claim |

---

## Known model limitations

1. **Weight budget** — Part XIX line items sum to 31 t, not 38 t; sim documents the gap rather than inventing filler mass.
2. **ERA** — Areal thickness credits, not full jet-interaction physics.
3. **APS** — Single inbound ATGM; no saturation or multi-spectral jamming model.
4. **Amphibious** — Displacement estimate; not CFD.
5. **Range** — Road range anchored to spec (600 km); not a full fuel-burn integration.
6. **AMET** — Spec penetration track is not reconciled with portfolio KEW-AP.

Re-run after editing `config.py` and update [`papers/MT-X_Leviathan_Specification.md`](papers/MT-X_Leviathan_Specification.md) and [`papers/MT-X_Leviathan_Research_Paper.md`](papers/MT-X_Leviathan_Research_Paper.md) to match.

---

[← Platform README](README.md) · [← Weapons-Defence](../README.md)
