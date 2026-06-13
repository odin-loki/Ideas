# TAIPAN-1 — Guided Ballistic Interceptor Rocket

> **A single-stage, liquid-propellant, guided ballistic interceptor rocket designed for minimum cost and maximum range from a compact mobile launch platform.** Named after Australia's most venomous snake. 4.87 m long, 631 kg wet mass, RP-1/LOX electric pump-fed engine — simulation-verified maximum range **1,618 km** at Mach 13.27. Production unit cost **$50k–$80k USD**, compared to $1.8M for an AMRAAM at 160 km range.

---

## What this folder is

TAIPAN-1 is a from-first-principles interceptor rocket design whose defining principle is cost. Three constraints shaped every decision:

1. **Cost under $80k at volume** — achieved by an electric pump-fed engine (eliminating the gas-generator turbopump that accounts for most of the cost of conventional liquid rocket engines) and a fully 3D-printed airframe in 14 structural parts.
2. **Manufacturability** — the entire airframe prints on standard industrial metal AM machines (EOS M400, Trumpf TruPrint 5000). No welding, no exotic tooling.
3. **Performance margin** — the 14 kg ballast design point delivers 1,618 km range, 16× the originally required 100 km, giving a configurable engagement envelope from 432 km (250 kg ballast) to 1,618 km by varying nose weight alone.

The engine architecture is the single most important design decision. Replacing a conventional gas-generator turbopump (325 kg dry mass at 50 kN) with a Rocket Lab Rutherford-inspired electric pump-fed design (62 kg dry mass) raises the mass ratio from 2.11 to 5.79, more than doubling Δv and delivering a 20× range improvement over a naive design.

---

## 📑 Source documents

| Document | Role |
|---|---|
| [`TAIPAN-1_Technical_Specification_Rev1.0.md`](TAIPAN-1_Technical_Specification_Rev1.0.md) | Full engineering specification — 22 sections covering propulsion, propellant system, airframe, aerodynamics, stability analysis, mass budget, flight performance, ballast performance envelope, GNC, FTS, launch system, manufacturing, materials, testing, cost, and production scaling. All performance figures simulation-verified. |
| [`TAIPAN-1_Financial_Analysis_Rev1.0.md`](TAIPAN-1_Financial_Analysis_Rev1.0.md) | Complete financial analysis — bottom-up component cost model, hardware unit cost (prototype and production), development program cost, testing infrastructure, fully-loaded unit cost, 20-year TCO, production scaling economics, competitive cost comparison, break-even analysis, and procurement strategy. |
| [`TAIPAN-1_Geometry_Reference_Rev1.0.md`](TAIPAN-1_Geometry_Reference_Rev1.0.md) | Complete geometric and dimensional reference — all station positions, section dimensions, nose cone profile, tank geometry, fin planform, flange interfaces, and ballast assembly, sufficient to produce a CAD model from scratch. |
| [`TAIPAN-1_Research_Paper.md`](TAIPAN-1_Research_Paper.md) | Research paper (synthesis) | Short validation narrative synthesising spec + `taipan1_sim.py` results. |
| [`SIM_README.md`](SIM_README.md) | Simulation suite documentation — covers all eight analysis modes, class architecture, physics models (Barrowman CP, semi-empirical drag, US Standard Atmosphere 1976, Tsiolkovsky), Bayesian GP optimiser, and library API. |
| [`taipan1_sim.py`](taipan1_sim.py) | Python simulation toolkit. Atmosphere model, engine thermochemistry, Barrowman aerodynamics, mass model, 3-DOF trajectory integrator, Bayesian optimiser. `python taipan1_sim.py --sim verify` runs the full verification dashboard. |
| [`taipan1_verification.png`](taipan1_verification.png) | Verification dashboard plot — trajectory, ballast sweep, stability margin vs propellant fraction, drag curve, and engine performance at design point. |

---

## 🎯 Headline numbers (simulation-verified)

### Performance

| Parameter | Value |
|---|---|
| Maximum range (14 kg ballast) | **1,618 km** |
| Apogee | **367 km** (above Kármán line for 467 s) |
| Peak Mach | **13.27** |
| Burnout velocity | 3,983 m/s |
| Burnout altitude | 28 km |
| Total flight time | 570 s (9.5 minutes) |
| Wet mass | 630.8 kg |
| Dry mass | 109.0 kg |
| Mass ratio | 5.787 |
| Ideal Δv (Tsiolkovsky) | 5,046 m/s |
| Achieved burnout velocity efficiency | 79% (21% lost to gravity + drag) |

### Ballast performance envelope

| Ballast | Range | Max Mach | Peak G | SM at burnout |
|---|---|---|---|---|
| 14 kg (design) | 1,618 km | 13.27 | 44.9 g | 1.57 cal |
| 80 kg (balanced) | 1,135 km | 10.96 | 28.8 g | 5.87 cal |
| 150 kg (precision) | 739 km | 8.98 | 20.4 g | 7.90 cal |
| 250 kg (maximum) | 432 km | 7.15 | 14.0 g | 9.37 cal |

### Cost comparison

| System | Unit cost | Range | Cost ratio |
|---|---|---|---|
| **TAIPAN-1 (production, 50+ units)** | **$50k–$80k** | **432–1,618 km** | **1× baseline** |
| Iron Dome Tamir | ~$50k | 70 km | ~1× cost, 23× less range |
| AIM-120D AMRAAM | ~$1.8M | 160 km | **22–37× more expensive** |
| THAAD interceptor | ~$11M | 200 km altitude | **137–220× more expensive** |
| Arrow 3 | ~$2M | ~2,400 km | **25–40× more expensive** |

### Engine

| Parameter | Value |
|---|---|
| Cycle | Electric pump-fed (Rutherford-inspired) |
| Propellants | RP-1 / LOX |
| Thrust (vacuum) | 50.0 kN |
| Specific impulse (vacuum) | 293.1 s |
| Chamber pressure | 50 bar |
| Burn duration | 30.0 s |
| Engine dry mass | **62 kg** (vs 325 kg for conventional turbopump at this thrust) |
| Combustion chamber | 3D printed Inconel 718, regeneratively cooled |

---

## 🏗️ Design philosophy

The 3D-printed airframe produces 14 structural parts from a conventionally fabricated design that would be 80–120 parts. Total print time approximately 208 hours on two parallel machines (one AlSi10Mg, one Ti-6Al-4V). Assembly labour ~80–120 person-hours for the first unit.

**Materials:**
- **AlSi10Mg** — nose cone, LOX tank, inter-tank, RP-1 tank. Cryogenic-rated to −200°C, good as-printed properties.
- **Ti-6Al-4V** (HIPped) — aft structure, boattail, fins. ≥ 1,000 MPa UTS after HIP + anneal; handles 50 kN thrust load and aerodynamic heating near the engine.
- **Inconel 718** — combustion chamber and nozzle. Maintains strength at 600–700°C chamber wall temperatures.
- **Tungsten alloy W95** — 14 kg nose ballast slug. 18,000 kg/m³ density allows a compact 58 × 165 mm cylinder to provide the forward CG offset needed for burnout stability.

**Stability:** Launch SM 5.29 cal → burnout SM 1.57 cal. The 14 kg tungsten ballast is sized analytically to just clear the 1.5 cal minimum at burnout. Increasing to 20 kg gives 2.17 cal burnout SM with only 154 km range penalty.

---

## 📐 Three recommended configurations

| Config | Ballast | Range | Use case |
|---|---|---|---|
| **A — Maximum Range** | 14 kg | 1,618 km | Maximum engagement distance; robust payload structure required |
| **B — Balanced** | 80 kg | 1,135 km | Sensitive electronics; comfortable stability margin |
| **C — Precision** | 150 kg | 739 km | Maximum electronics survival; precision terminal guidance |

---

## 🚧 Honest caveats

- **3-DOF simulation only.** The trajectory model is a point-mass 3-DOF simulation in a vertical plane. No Earth rotation, no wind, no angle-of-attack dynamics, no structural flexibility. A 6-DOF high-fidelity simulation is required for flight test planning.
- **Engine is specified at system level, not designed in detail.** Injector element sizing, cooling channel analysis, and turbopump sizing are all future engineering work. The specification treats the engine as a black box defined by its performance parameters (Isp, thrust, dry mass), benchmarked against the Rutherford architecture.
- **Burnout SM is marginal at 1.57 cal.** Any manufacturing mass tolerance deviation in the aft section could bring this below 1.5 cal. The 20 kg ballast configuration (SM = 2.17 cal) is recommended unless maximum range is operationally required.
- **Aerothermal re-entry is unanalysed.** At Mach 13+ the nose cone AlSi10Mg (melt point ~580°C) requires a thermal protection study and ablative or ceramic coating before any flight qualification attempt.
- **This is a conceptual design study.** All performance figures are model predictions, not measured prototype data. The document explicitly does not constitute engineering certification.

---

## 🔗 Related work in this repo

- [`../../../Diamond Batterys/`](../../../Diamond%20Batterys/) — power source for the HPR-X rocketry series and longer-range propulsion adjacency
- [`../../HPR-X Rocketry/`](../HPR-X%20Rocketry/) — the HPR-X guided high-power rocketry series within the same portfolio (smaller, solid-propellant)
- [`../../weapons_simulation.py`](../weapons_simulation.py) — portfolio common simulator (Tsiolkovsky + drag trajectory modelling also covered there for HPR-X)
- [`../../../Filtering/`](../../../Filtering/) — GH-SR-IMM multi-target tracking (applicable to terminal guidance sensor fusion)
- [`../../../Asset Tracking Algorithm/`](../../../Asset%20Tracking%20Algorithm/) — ARIA-INTEL battlefield intelligence (intercept targeting adjacency)

---

[← Back to Weapons-Defence README](../README.md)
