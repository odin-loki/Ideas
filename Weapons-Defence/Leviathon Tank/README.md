# MT-X Mk.II "Leviathan" — multi-role armoured combat vehicle

> **A simulation-validated 38-tonne amphibious armoured platform combining 140 mm AMET main armament, AlNiCyN-5000 composite armour, PPU-1300 boxer diesel (1,300 hp), hard-kill APS, and troop-carrying capacity for eight dismounts.** Headline design: 65 km/h road speed, 34.2 hp/t, 600 km road range, upper glacis ~779 mm effective RHA with ERA, bustle autoloader at 8 rpm.

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or prototype test data is implied. **Vehicle numbers trace to the standalone `leviathan_sim` package in this folder; main-gun KE cross-checks use the portfolio [`../140mm Tank KE Round/`](../140mm%20Tank%20KE%20Round/) simulator.**

---

## What this folder is

The MT-X Mk.II Leviathan is a **complete platform subfolder**: operator specification, cost analysis, dedicated twelve-module Python simulation suite, and (planned) multi-part research paper. Like BSG-10 Goliath, Leviathan carries its own physics toolchain because tracked-vehicle mobility, amphibious flotation, armour zoning, and APS timelines are outside the Tier-1/Tier-2 cartridge tables in [`../weapons_simulation.py`](../weapons_simulation.py).

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`papers/MT-X_Leviathan_Specification.md`](papers/MT-X_Leviathan_Specification.md) — full technical reference (Parts I–XXII).
3. [`papers/MT-X_Leviathan_Research_Paper.md`](papers/MT-X_Leviathan_Research_Paper.md) — formal design-and-validation narrative (Parts I–XV, convergence in Part XIII).
4. [`papers/MT-X_Leviathan_Cost_Analysis.md`](papers/MT-X_Leviathan_Cost_Analysis.md) — unit and program cost (hybrid bonding).
5. [`SIM_README.md`](SIM_README.md) — how to re-run simulations and interpret dual-track 140 mm penetration.
6. Run [`platform_simulation.py`](platform_simulation.py) — consolidated vehicle performance report.

---

## Source documents

| Document | Format | Role |
|---|---|---|
| [`papers/MT-X_Leviathan_Specification.md`](papers/MT-X_Leviathan_Specification.md) | Technical reference | Hull, armour, powertrain, armament, APS, amphibious, weight, logistics — **start here** |
| [`papers/MT-X_Leviathan_Research_Paper.md`](papers/MT-X_Leviathan_Research_Paper.md) | Academic research paper | Parts I–XV: subsystem design, simulation validation, **Part XIII convergence**, 65 references |
| [`papers/MT-X_Leviathan_Cost_Analysis.md`](papers/MT-X_Leviathan_Cost_Analysis.md) | Cost analysis | Hybrid bonding savings, unit price ~$5.82M–$6.48M |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Module map, headline table, portfolio cross-refs |
| [`platform_simulation.py`](platform_simulation.py) | Local entry script | Runs full `leviathan_sim` suite |
| [`leviathan_sim_package/`](leviathan_sim_package/) | Python package | All vehicle physics modules |

### Simulation modules (`leviathan_sim_package/leviathan_sim/`)

| Module | File | Role |
|---|---|---|
| Mobility | [`mobility/performance.py`](leviathan_sim_package/leviathan_sim/mobility/performance.py) | Speed, range, gradient, ground pressure |
| Armour | [`armour/effective.py`](leviathan_sim_package/leviathan_sim/armour/effective.py) | Effective RHA per zone, ERA |
| Powertrain | [`powertrain/engine.py`](leviathan_sim_package/leviathan_sim/powertrain/engine.py) | PPU-1300 curves and fuel |
| Suspension | [`suspension/ride.py`](leviathan_sim_package/leviathan_sim/suspension/ride.py) | Torsion bars, ride frequency |
| Main gun | [`armament/main_gun.py`](leviathan_sim_package/leviathan_sim/armament/main_gun.py) | Autoloader, dual penetration model |
| Secondary | [`armament/secondary.py`](leviathan_sim_package/leviathan_sim/armament/secondary.py) | Coax + RWS |
| APS | [`aps/engagement.py`](leviathan_sim_package/leviathan_sim/aps/engagement.py) | Engagement envelope |
| Amphibious | [`amphibious/flotation.py`](leviathan_sim_package/leviathan_sim/amphibious/flotation.py) | Buoyancy and swim speed |
| FCS | [`fcs/hit_probability.py`](leviathan_sim_package/leviathan_sim/fcs/hit_probability.py) | First-round hit probability |
| Weight | [`weight/budget.py`](leviathan_sim_package/leviathan_sim/weight/budget.py) | Part XIX budget check |
| Logistics | [`logistics/maintenance.py`](leviathan_sim_package/leviathan_sim/logistics/maintenance.py) | Maintenance and transport |
| Cost | [`cost/unit_cost.py`](leviathan_sim_package/leviathan_sim/cost/unit_cost.py) | Unit/program cost |
| Report | [`reports/generate.py`](leviathan_sim_package/leviathan_sim/reports/generate.py) | Markdown + JSON output |

---

## Headline numbers (simulation-validated)

| Metric | Value |
|---|---|
| Combat mass | **38,000 kg** |
| Engine | **PPU-1300** — 1,300 hp / 4,800 N·m |
| Power-to-weight | **34.2 hp/t** |
| Max road speed | **65 km/h** |
| Ground pressure | **66.9 kPa** |
| Road range (diesel) | **600 km** |
| Main gun | **140 mm L/65** smoothbore, **8 rpm** autoloader |
| Ready + stowed ammo | **34 rounds** |
| Upper glacis (ERA) | **779 mm** eff. RHA |
| Portfolio KE @ 2 km | **326.7 mm** RHA |
| APS two-shot Pk | **0.96** |
| Swim speed | **7 km/h** |
| Unit cost (ex ammo) | **$5.82M** |

See [`SIM_README.md`](SIM_README.md) for methodology, limitations, and the AMET vs portfolio KE discrepancy.

---

## Simulation verification

```bash
python platform_simulation.py
```

Or from the package directory:

```bash
cd leviathan_sim_package
pip install -r leviathan_sim/requirements.txt
python run_all.py
```

Reports: `leviathan_sim_package/leviathan_sim/outputs/leviathan_sim_report.md`

---

## Cross-references

| Related system | Folder |
|---|---|
| 140 mm KE ammunition | [`../140mm Tank KE Round/`](../140mm%20Tank%20KE%20Round/) |
| AlNiCyN armour | [`../AlNiCyN Armour/`](../AlNiCyN%20Armour/) |
| MP-6.8 coax | [`../MP-6.8 Mark II Rifle/`](../MP-6.8%20Mark%20II%20Rifle/) |
| 15.2 mm RWS | [`../MAS-15.2E Anti-Materiel Sniper/`](../MAS-15.2E%20Anti-Materiel%20Sniper/) |
| Rubber tracks | [`../Rubber Tank Tracks/`](../Rubber%20Tank%20Tracks/) |

---

## Honest framing

- **Not a fielded vehicle.** Concept and simulation only.
- **Separate simulator.** Do not expect Leviathan rows in [`../weapons_sim_results.md`](../weapons_sim_results.md) except via linked ammunition subsystems.
- **Weight table gap.** Part XIX line items sum to 31 t; the sim flags the ~7 t discrepancy against the 38 t combat mass claim.
- **Research paper** — [`papers/MT-X_Leviathan_Research_Paper.md`](papers/MT-X_Leviathan_Research_Paper.md) (TRP-2026-MTX-001): twelve technical parts converging in Part XIII with integrated threat matrix and 65 citations.

[← Weapons-Defence](../README.md)
