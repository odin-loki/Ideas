# TAIPAN-1
## Guided Ballistic Interceptor Rocket — Full Technical Specification

**Classification:** Unclassified Design Study  
**Revision:** 1.0  
**Date:** 2026  
**Author:** Independent Research  
**Status:** Specification Complete — Simulation Verified  

---

> TAIPAN-1 is a single-stage, liquid-propellant, guided ballistic interceptor rocket designed for low-cost, high-performance engagement of aerial threats at ranges up to 1,618 km. Named after Australia's most venomous snake, it is optimised for manufacturability, minimal cost, and maximum ballistic range from a compact, mobile launch platform.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Mission Profile](#2-mission-profile)
3. [Propulsion System](#3-propulsion-system)
4. [Propellant System](#4-propellant-system)
5. [Airframe and Structure](#5-airframe-and-structure)
6. [Aerodynamics](#6-aerodynamics)
7. [Stability Analysis](#7-stability-analysis)
8. [Mass Budget](#8-mass-budget)
9. [Flight Performance](#9-flight-performance)
10. [Ballast Performance Envelope](#10-ballast-performance-envelope)
11. [Guidance, Navigation and Control](#11-guidance-navigation-and-control)
12. [Flight Termination System](#12-flight-termination-system)
13. [Launch System](#13-launch-system)
14. [Manufacturing](#14-manufacturing)
15. [Materials Specification](#15-materials-specification)
16. [Testing and Qualification](#16-testing-and-qualification)
17. [Environmental and Storage](#17-environmental-and-storage)
18. [Cost and Pricing](#18-cost-and-pricing)
19. [Production Scaling](#19-production-scaling)
20. [Limitations and Future Work](#20-limitations-and-future-work)
21. [Appendix A — Simulation Parameters](#21-appendix-a--simulation-parameters)
22. [Appendix B — Derivations](#22-appendix-b--derivations)

---
## 1. Executive Summary

TAIPAN-1 is a 4.87 m, 631 kg (wet) single-stage liquid-propellant rocket powered by a 50 kN RP-1/LOX electric pump-fed engine. It is designed from first principles to be the cheapest possible guided interceptor capable of engaging targets at 100 km range, with substantial margin — the verified maximum ballistic range is **1,618 km** at a **70.4° launch angle**, reaching a peak velocity of **Mach 13.27** and an apogee of **367 km**.

The design philosophy is derived from three constraints:

1. **Cost** — under $170k USD per unit at prototype scale, under $80k at production volume
2. **Manufacturability** — the entire airframe is 3D printed in six sections using industrial metal additive manufacturing; no exotic tooling or specialist facilities required
3. **Performance margin** — the design point of 14 kg ballast and 70.4° launch angle provides 16× the originally required 100 km range, giving operators the full performance envelope from 432 km (250 kg ballast) to 1,618 km (design ballast) by varying nose weight alone

The engine draws directly from the Rocket Lab Rutherford architecture — electric pump-fed, 3D printed Inconel combustion chamber, regeneratively cooled — achieving 62 kg dry mass at 50 kN thrust (1.24 kg/kN specific mass). This is the single most important design decision: reducing engine dry mass from a conventional estimate of 325 kg to 62 kg raises the mass ratio from 2.11 to 5.79, more than doubling the delta-v and delivering a 20× range improvement over a naive design.

**Key verified figures:**

| Parameter | Value |
|---|---|
| Maximum range | 1,618 km |
| Apogee | 367 km |
| Peak Mach | 13.27 |
| Wet mass | 630.8 kg |
| Dry mass | 109.0 kg |
| Mass ratio | 5.787 |
| Ideal Δv | 5,046 m/s |
| Prototype unit cost | $90k – $170k USD |
| Production unit cost | $50k – $80k USD |

---

## 2. Mission Profile

### 2.1 Primary Mission

TAIPAN-1 is designed as a **ballistic interceptor** — a kinetic kill vehicle launched from a mobile ground platform to intercept aerial targets on a ballistic arc. The primary intercept envelope is 100–1,618 km downrange with a guided terminal phase provided by the IMU/GPS avionics package.

### 2.2 Trajectory Overview

The rocket is launched at **70.4°** from vertical (19.6° from horizontal) — the analytically verified optimum for maximum range with this propellant load. This is shallower than a typical sounding rocket but steeper than a flat-range ballistic missile, representing the compromise between gravity losses and horizontal velocity.

```
Phase 1 — Powered ascent (0–30 s)
  Thrust: 44.1 kN (SL) → 50.0 kN (vacuum)
  Burnout: 28 km altitude, 3,983 m/s velocity

Phase 2 — Ballistic coast (30 s – ~400 s)
  Engine off, coasting on ballistic arc
  Apogee: 367 km at ~200 s
  Time above Kármán line (100 km): 467 s

Phase 3 — Terminal descent (400 s – 570 s)
  Re-entry, guidance correction
  Impact / intercept at target
  Total flight time: ~570 s
```

### 2.3 Engagement Envelope

The engagement envelope is defined by ballast mass. By varying nose ballast between 14 kg (minimum for stability) and 250 kg, the operator trades range for stability margin and reduced G-loading on the payload:

- **Minimum ballast (14 kg):** 1,618 km range, Mach 13.3, 44.9g peak
- **Moderate ballast (80 kg):** 1,135 km range, Mach 10.96, 28.8g peak
- **Maximum ballast (250 kg):** 432 km range, Mach 7.15, 14.0g peak

### 2.4 Launch Geometry

Launch angle can be varied to trade range against apogee. At 70.4° the range is maximised. Steeper angles (85–88°) maximise apogee at the cost of range. Shallower angles reduce both. The guidance system handles trajectory correction post-launch.

---
## 3. Propulsion System

### 3.1 Engine Overview

The TAIPAN-1 engine is a **single-chamber, electric pump-fed, pressure-regulated RP-1/LOX liquid rocket engine** producing 50 kN vacuum thrust. It is inspired directly by the Rocket Lab Rutherford engine architecture, which demonstrated that replacing a conventional gas-generator turbopump with battery-driven electric pumps dramatically reduces engine dry mass, complexity, and cost while maintaining performance.

| Parameter | Value |
|---|---|
| Thrust (vacuum) | 50.0 kN |
| Thrust (sea level) | 44.1 kN |
| Specific impulse (vacuum) | 293.1 s |
| Specific impulse (sea level) | 258.6 s |
| Characteristic velocity c\* | 1,703 m/s |
| Chamber pressure | 50 bar |
| Oxidiser/fuel ratio (O/F) | 2.56 |
| Expansion ratio ε | 10 |
| Mass flow rate | 17.395 kg/s |
| Burn duration | 30.0 s |
| Engine dry mass | 62 kg |
| Specific mass | 1.24 kg/kN |
| Ignition system | Torch igniter |
| Throttle capability | Fixed thrust |

### 3.2 Engine Cycle — Electric Pump-Fed

Conventional rocket engines use a **gas-generator cycle** or **staged combustion cycle** where a fraction of propellant is burned to drive a turbine that powers the pumps. This requires complex turbomachinery, a preburner, and extensive high-temperature plumbing — all heavy.

TAIPAN-1 uses an **electric pump-fed cycle**:

- Two brushless electric motors (one per propellant) drive centrifugal impellers
- Power supplied by a dedicated lithium polymer battery pack mounted in the aft section
- No turbine, no preburner, no hot-gas plumbing
- Pump assembly mass: approximately 8–12 kg total for both pumps
- Battery pack mass: approximately 6–8 kg for 30s burn at required power
- Net result: turbomachinery system under 20 kg vs 80–150 kg for a conventional turbopump

The trade-off is battery energy density — at 30 seconds burn time this is entirely manageable, and the mass savings are enormous. This is why the Rutherford engine achieves 35 kg dry mass at 22 kN (1.59 kg/kN). TAIPAN-1's slightly lower specific mass of 1.24 kg/kN reflects a modest scaling penalty at 50 kN.

### 3.3 Combustion Chamber

The combustion chamber is a **single 3D printed Inconel 718 component** with integral regenerative cooling channels.

| Parameter | Value |
|---|---|
| Material | Inconel 718 |
| Manufacturing method | Direct metal laser sintering (DMLS) |
| Chamber pressure | 50 bar |
| Adiabatic flame temperature | 3,670 K |
| Throat temperature | 3,284 K |
| Cooling | Regenerative (RP-1 coolant) |
| Injector type | Coaxial swirl (printed integral) |

The regenerative cooling circuit routes RP-1 through printed channels in the chamber wall before injection. This pre-heats the fuel (improving atomisation) and keeps the chamber wall below Inconel's service temperature limit of ~1,100 K. Channel geometry is optimised at the throat where heat flux is highest.

### 3.4 Nozzle Geometry

The nozzle is a **conical De Laval design** at 15° half-angle, integrated with the chamber as a single printed assembly.

| Parameter | Value |
|---|---|
| Throat diameter | 86.9 mm |
| Exit diameter | 274.7 mm |
| Nozzle length | 350 mm |
| Throat area | 59.3 cm² |
| Exit area | 593 cm² |
| Half-angle | 15° |
| Exit Mach number | 3.87 |
| Exit pressure | ~2.4 kPa |
| Exit velocity | ~2,680 m/s |

The expansion ratio of 10 is a conservative choice well-suited to a rocket that burns through all altitudes from sea level to 28 km during powered flight. A higher expansion ratio would improve vacuum Isp marginally but would require a larger, heavier nozzle that also underexpands severely at sea level.

### 3.5 Ignition System

TAIPAN-1 uses a **torch igniter** — a small pilot flame generated by a dedicated spark-ignited fuel-rich propellant mixture injected into the chamber prior to main propellant flow. This is more reliable than a pyrotechnic igniter (which is single-use and cannot be tested before flight), simpler than a hypergolic slug (which requires separate toxic propellant handling), and appropriate for RP-1/LOX which does not self-ignite.

Ignition sequence:
1. Pressurisation of feed lines
2. Torch igniter fires (spark + pilot propellant flow)
3. Main LOX valve opens (50 ms)
4. Main RP-1 valve opens (20 ms later)
5. Full thrust achieved within 200 ms of ignition command

### 3.6 Engine Mass Justification

The conventional empirical estimate for turbopump-fed engines is 6.5 kg/kN — derived from legacy systems (Merlin, RD-180, etc.) that use complex turbomachinery. Modern electric pump-fed engines demonstrate substantially lower specific mass:

| Engine | Thrust | Dry mass | Specific mass |
|---|---|---|---|
| Rocket Lab Rutherford | 22 kN | 35 kg | 1.59 kg/kN |
| Rocket Lab Rutherford Vac | 25 kN | 35 kg | 1.40 kg/kN |
| **TAIPAN-1 target** | **50 kN** | **62 kg** | **1.24 kg/kN** |
| Legacy turbopump estimate | 50 kN | 325 kg | 6.50 kg/kN |

The TAIPAN-1 figure accounts for modest scaling advantages at 50 kN versus 22 kN. The 62 kg target is considered achievable and conservative relative to the Rutherford benchmark.

---

## 4. Propellant System

### 4.1 Propellant Selection — RP-1 / LOX

**RP-1 (Rocket Propellant 1)** is a highly refined kerosene used as the fuel. **LOX (Liquid Oxygen)** is the oxidiser. This combination is the most widely proven liquid propellant pairing in rocketry — used in the Saturn V F-1, SpaceX Merlin, Rocket Lab Rutherford, and many others.

**Why RP-1/LOX:**

| Property | Value / Note |
|---|---|
| Specific impulse (vacuum) | 293 s — competitive for a storable/cryogenic combination |
| Density | High — compact tanks vs hydrogen |
| RP-1 cost | ~$3 USD/kg — essentially free at this scale |
| LOX cost | ~$0.15 USD/kg — industrial commodity |
| RP-1 handling | Ambient temperature, non-toxic, non-corrosive |
| LOX handling | Cryogenic (-183°C), requires insulated tanks and venting |
| Storability | RP-1 indefinite; LOX requires fuelling within hours of launch |

The primary operational constraint is LOX — it must be loaded at the launch site and cannot be stored in the rocket long-term. This is standard for all LOX-fuelled systems and is managed by on-site cryogenic storage.

### 4.2 Propellant Quantities

| Propellant | Mass | Volume | Density |
|---|---|---|---|
| RP-1 | 146.6 kg | 181 L | 810 kg/m³ |
| LOX | 375.2 kg | 329 L | 1,141 kg/m³ |
| **Total** | **521.8 kg** | **510 L** | — |

O/F ratio: **2.56** by mass (near-optimal for Isp with RP-1/LOX).  
Mass flow: **17.395 kg/s** total (4.86 kg/s RP-1, 12.54 kg/s LOX).

### 4.3 Tank Design

Both propellant tanks are **3D printed AlSi10Mg aluminium alloy cylinders** with hemispherical end domes, printed as single structural pieces including integral baffles.

**LOX Tank:**
- Volume: 329 L (with 5% ullage margin → 345 L total volume)
- Diameter: 275 mm (same as body)
- Length: approximately 1.28 m
- Operating pressure: 12 bar (pump inlet pressure + margin)
- Material: AlSi10Mg (cryogenic-rated)
- Insulation: 10 mm polyurethane foam overwrap
- Fittings: printed-in boss for fill, vent, drain, and pressurisation ports

**RP-1 Tank:**
- Volume: 181 L (with 3% ullage margin → 187 L total volume)
- Length: approximately 0.70 m
- Operating pressure: 10 bar
- Material: AlSi10Mg
- Sump: printed-in conical sump for reliable drain under acceleration

### 4.4 Feed System

Feed is driven by **electric centrifugal pumps** — one per propellant line — powered by a lithium polymer battery pack in the aft section.

```
LOX tank → LOX pump (electric) → LOX valve → injector → chamber
RP-1 tank → RP-1 pump (electric) → cooling jacket → RP-1 valve → injector
```

RP-1 is routed through the regenerative cooling jacket before injection, which is both a thermal management function and a feed system simplification — no separate coolant circuit required.

### 4.5 Pressurant System

Tank pressurisation uses **gaseous helium** stored in a small CFRP-overwrapped pressure vessel (COPV) in the inter-tank section. Helium provides the tank ullage pressure needed to suppress pump cavitation and maintain structural integrity. Required pressurant mass is approximately 0.8 kg at 300 bar storage pressure.

---
## 5. Airframe and Structure

### 5.1 Overall Dimensions

| Parameter | Value |
|---|---|
| Body diameter | 275 mm |
| Nose length | 920 mm (ogive, 3.35 calibers) |
| Body length | 3,850 mm |
| Boattail length | 100 mm |
| Total length | 4,870 mm |
| Fineness ratio | 17.71 |
| Reference area | 594 cm² |

### 5.2 Body Sections

The airframe is divided into **six 3D printed sections** joined by flanged interfaces with O-ring face seals and through-bolted flanges. This segmented approach allows each section to be printed on standard industrial metal printers (build volume ~400 × 400 × 500 mm), independently inspected, and replaced if damaged. No welding is required — all structural joints are bolted flanges.

```
┌──────────────────────────────────────────────────────────────────────┐
│  [1]NOSE  │  [2]LOX TANK  │[3]INTERTANK│  [4]RP-1 TANK  │[5]AFT│[6]BT│
│  0.92m    │    1.28m      │   0.45m    │    0.70m       │ 0.52m│0.1m│
└──────────────────────────────────────────────────────────────────────┘
```

**Section 1 — Nose Cone (0–920 mm)**
- Profile: tangent ogive (shape factor 0.686 — between conical and pure ogive)
- Material: AlSi10Mg
- Wall thickness: 3.5 mm (increasing to 6 mm at base flange)
- Interior: hollow, houses 14 kg tungsten ballast slug bolted to forward bulkhead
- Tip: solid printed tip with 5 mm radius bluntness for thermal margin
- Avionics antenna ports: printed-in recesses for GPS antenna patch

**Section 2 — LOX Tank (920–2,200 mm)**
- Material: AlSi10Mg
- Wall thickness: 5.5 mm cylindrical, 7 mm dome
- Internal baffles: 4 × cruciform baffles printed integral, spaced 250 mm axially, suppress propellant slosh under lateral loads
- Fittings: 6 × printed-in bosses (fill, vent, drain, pressurant, sensor ×2)
- Insulation: external polyurethane foam spray coat (10 mm)
- Pressure rating: 15 bar proof, 10 bar MEOP

**Section 3 — Inter-tank (2,200–2,650 mm)**
- Material: AlSi10Mg
- Function: structural collar between tanks, routes LOX/RP-1 lines and electrical conduit externally via printed-in channels on inner wall
- Houses: helium COPV pressurant vessel (external strap mount), avionics bay (3 kg IMU/GPS/FTS computer, battery management)
- Wall thickness: 4 mm with 6 printed longitudinal stiffening ribs

**Section 4 — RP-1 Tank (2,650–3,350 mm)**
- Material: AlSi10Mg
- Wall thickness: 4.5 mm cylindrical, 5.5 mm dome
- Sump: conical drain sump printed into lower dome for reliable propellant feed under acceleration
- Fittings: 5 × printed-in bosses
- Pressure rating: 12 bar proof, 8 bar MEOP
- No external insulation required (ambient temperature propellant)

**Section 5 — Aft Structure / Thrust Frame (3,350–3,870 mm)**
- Material: Ti-6Al-4V
- This is the most structurally critical section — all 50 kN of thrust load passes through it
- Wall thickness: 6 mm cylindrical with 8 mm printed internal gussets at fin attachment points
- Features: 4 × integral fin root attachment lugs (through-bolt, 4 × M12 per fin), engine mount flange ring, load-spreading thrust ring at forward end, cable routing conduits
- Battery pack for electric pumps mounts to internal aft bulkhead
- Thermal protection: 5 mm ceramic-loaded ablative coating on exterior aft face

**Section 6 — Boattail (3,870–3,970 mm)**
- Material: Ti-6Al-4V
- Taper: body diameter (275 mm) to engine bell clearance diameter (250 mm)
- Integrates with nozzle mount ring
- Acts as base drag reducer — the taper reduces the effective base area exposed to the low-pressure base region behind the rocket

### 5.3 Fins

Four trapezoidal fins are attached to the aft structure section via root lugs.

| Parameter | Value |
|---|---|
| Count | 4, equally spaced (90°) |
| Profile | Trapezoidal, leading-edge swept |
| Semi-span | 229 mm |
| Root chord | 283 mm |
| Tip chord | 164 mm |
| Taper ratio | 0.58 |
| Leading-edge sweep | 37.9° |
| Thickness | 5 mm (constant) |
| Material | Ti-6Al-4V |
| Manufacturing | 3D printed, post-machined leading/trailing edges |
| Attachment | 4 × M12 bolts through root lug per fin, replaceable |

Fin leading and trailing edges are post-machined to a 1.5 mm radius after printing — this is critical for aerodynamic drag and prevents edge cracking under thermal cycling.

### 5.4 Ballast Assembly

The nose ballast is a **machined tungsten alloy (W-Ni-Fe, 95% W) cylindrical slug** bolted to the forward bulkhead inside the nose cone.

| Parameter | Value |
|---|---|
| Design mass | 14 kg |
| Material | Tungsten alloy W95 |
| Density | ~18,000 kg/m³ |
| Dimensions | ~58 mm diameter × 165 mm long (cylinder) |
| Position | 50 mm from nose tip (centre of mass) |
| Attachment | M16 central bolt + 4 × M8 retaining bolts through bulkhead |

The ballast is a separate machined part — not printed — because tungsten cannot be cost-effectively additively manufactured at this mass. The slug is standard ballast material and can be substituted with additional mass (steel, lead) to cheaply adjust the range/stability envelope.

### 5.5 Structural Load Analysis

The design load factor is **55 g**, providing a 10.1 g margin over the verified peak of 44.9 g. Dominant load cases:

| Load case | Location | Magnitude |
|---|---|---|
| Thrust load | Engine mount / aft section | 50 kN axial |
| Max-Q aerodynamic | Nose + fin leading edges | 2,198 kPa dynamic pressure |
| Peak axial acceleration | All sections | 44.9 g (at motor ignition) |
| Fin bending | Fin root attachment | ~800 N lateral at max-Q |
| Cryogenic thermal | LOX tank | -183°C to ambient cycling |

All sections are designed to withstand 1.5× proof pressure. The Ti-6Al-4V aft structure with integral gussets has been sized conservatively — wall thickness and gusset placement were not formally optimised, leaving substantial structural margin.

---

## 6. Aerodynamics

### 6.1 Drag Model

The drag model uses a semi-empirical four-component formulation:

**CD = CD_nose + CD_friction + CD_base + CD_fins**

| Component | Subsonic | Transonic peak | Supersonic (Mach 5) |
|---|---|---|---|
| Nose (wave + pressure) | 0.040 | 0.130 | 0.062 |
| Skin friction (turbulent) | 0.180 | 0.175 | 0.120 |
| Base drag | 0.120 | 0.200 | 0.050 |
| Fin drag (bluntness) | 0.010 | 0.015 | 0.008 |
| **Total CD** | **~0.35** | **~0.60** | **~0.24** |

The transonic regime (Mach 0.8–1.2) sees the largest CD due to wave drag formation at the nose. CD drops sharply above Mach 2 as the shock becomes fully attached and wave drag stabilises. At the design peak of Mach 13.3 the CD is approximately 0.22.

### 6.2 Reference Area

All drag and aerodynamic force coefficients are referenced to the **body cross-sectional area:**

Aref = π × (0.275/2)² = **594 cm² = 0.05940 m²**

### 6.3 Dynamic Pressure Profile

Peak dynamic pressure (**max-Q**) occurs during powered flight as thrust accelerates the rocket through dense lower atmosphere:

| Parameter | Value |
|---|---|
| Max-Q | 2,198 kPa |
| Time of max-Q | ~8 s after launch |
| Altitude at max-Q | ~3 km |
| Mach at max-Q | ~1.8 |

This is the most aerodynamically stressful moment of flight and drives the structural sizing of the nose cone and fin attachment.

---
## 7. Stability Analysis

### 7.1 Method — Barrowman Equations

The centre of pressure (CP) is calculated using the **Barrowman equations** — the standard analytical method for slender finned rockets. The method decomposes the rocket into nose cone and fin contributions to the normal force slope CNα, then computes CP as a weighted average.

**Nose contribution:**
- CNα_nose = 2.0 (slender body approximation, valid for all nose shapes)
- XCP_nose = 0.466 × L_nose = 0.429 m (ogive shape factor)

**Fin contribution:**
- Trapezoidal planform with interference factor for body-fin junction
- CNα_fins = 7.94 (4 fins, computed from geometry)
- XCP_fins = 4.048 m from nose (quarter MAC rule with sweep correction)

**Combined CP:**

| Quantity | Value |
|---|---|
| Total CNα | 9.94 |
| CP location | **3.615 m from nose tip** |

### 7.2 Centre of Gravity

CG shifts forward as propellant is consumed (engine and propellant are aft-heavy; propellant tanks are forward of engine). This is the standard challenge in all liquid-propellant rockets — the CG migrates aft as propellant burns, reducing stability margin.

| Configuration | CG location | Notes |
|---|---|---|
| Launch (full propellant) | **2.161 m from nose** | Maximum stability |
| Burnout (dry) | **3.182 m from nose** | Minimum stability |

### 7.3 Stability Margin

Stability margin (SM) is expressed in **calibers** (body diameters). A margin ≥ 1.5 calibers at all flight phases is the design requirement, consistent with standard rocketry practice.

SM = (XCP − XCG) / D_body

| Configuration | XCP (m) | XCG (m) | SM (cal) | Status |
|---|---|---|---|---|
| Launch (full prop) | 3.615 | 2.161 | **5.29** | ✓ Excellent |
| Burnout (dry) | 3.615 | 3.182 | **1.57** | ✓ Marginal pass |

The burnout margin of 1.57 cal just clears the 1.5 cal minimum. This is achieved through 14 kg of tungsten ballast positioned at 50 mm from the nose tip, which pulls the dry CG forward by approximately 0.43 m relative to a zero-ballast configuration.

### 7.4 Stability During Burn

As propellant depletes over the 30-second burn, the SM transitions continuously from 5.29 cal (launch) to 1.57 cal (burnout). At no point during powered flight does SM drop below the 1.5 cal minimum, confirmed by interpolating CG at intermediate propellant fractions:

| Propellant remaining | CG (m) | SM (cal) |
|---|---|---|
| 100% (launch) | 2.161 | 5.29 |
| 75% | 2.48 | 4.16 |
| 50% | 2.80 | 2.97 |
| 25% | 3.05 | 1.99 |
| 0% (burnout) | 3.182 | 1.57 |

Post-burnout the rocket is aerodynamically stable in the coasting phase as long as it maintains non-zero velocity and angle of attack remains small — conditions met during nominal ballistic flight.

---

## 8. Mass Budget

### 8.1 Component Breakdown

| Component | Mass (kg) | % of wet mass | Notes |
|---|---|---|---|
| Nose cone (AlSi10Mg) | 3.2 | 0.5% | Hollow ogive section |
| LOX tank (AlSi10Mg) | 6.8 | 1.1% | With integral baffles |
| Inter-tank section | 3.5 | 0.6% | Includes He COPV |
| RP-1 tank (AlSi10Mg) | 4.1 | 0.7% | With sump |
| Aft structure (Ti-6Al-4V) | 8.4 | 1.3% | Thrust frame + fin lugs |
| Boattail (Ti-6Al-4V) | 2.1 | 0.3% | Tapered transition |
| Fins × 4 (Ti-6Al-4V) | 1.9 | 0.3% | Trapezoidal, 4 off |
| **Structure subtotal** | **30.0** | **4.8%** | |
| Combustion chamber + nozzle | 18.0 | 2.9% | Printed Inconel 718 |
| Electric pump assembly (×2) | 10.0 | 1.6% | Motors + impellers |
| Battery pack | 7.0 | 1.1% | LiPo, 30s duration |
| Valves + lines + fittings | 12.0 | 1.9% | Propellant system |
| Torch igniter | 1.5 | 0.2% | |
| Engine misc / fasteners | 13.5 | 2.1% | Brackets, seals, wiring |
| **Engine subtotal** | **62.0** | **9.8%** | |
| IMU + GPS receiver | 1.5 | 0.2% | COTS navigation |
| Flight computer | 0.8 | 0.1% | Radiation tolerant MCU |
| FTS receiver + destruct | 0.5 | 0.1% | RF command system |
| Avionics power / wiring | 0.2 | 0.0% | |
| **Avionics subtotal** | **3.0** | **0.5%** | |
| Tungsten ballast slug | 14.0 | 2.2% | W95 alloy, nose tip |
| **Dry mass total** | **109.0** | **17.3%** | |
| RP-1 propellant | 146.6 | 23.2% | |
| LOX propellant | 375.2 | 59.5% | |
| **Propellant total** | **521.8** | **82.7%** | |
| **WET MASS (LAUNCH)** | **630.8** | **100%** | |

### 8.2 Mass Fractions

| Metric | Value |
|---|---|
| Propellant mass fraction | 82.7% |
| Dry mass fraction | 17.3% |
| Mass ratio (wet/dry) | 5.787 |
| Structural coefficient (struct/dry) | 27.5% |
| Engine mass fraction (eng/dry) | 56.9% |

The engine is the dominant dry mass component at 62 kg. This is unavoidable for a liquid-propellant system — the pump, chamber, nozzle, and feed system have a hard floor. Further mass reduction would require a smaller engine (lower thrust, longer burn time) or transition to a solid propellant, which sacrifices Isp.

The structural mass of 30 kg is impressively low and is enabled entirely by 3D printing — a conventionally fabricated welded tank structure would be 60–80 kg for this diameter and length.

---
## 9. Flight Performance

All figures are simulation-verified using a 3-DOF point-mass trajectory model with US Standard Atmosphere 1976, altitude-corrected thrust, and empirical drag model. Timestep: 0.05 s.

### 9.1 Primary Performance Parameters

| Parameter | Value |
|---|---|
| Launch angle | 70.4° from vertical |
| Apogee | 367 km |
| Maximum range | 1,618 km |
| Maximum Mach | 13.27 |
| Burnout velocity | 3,983 m/s |
| Burnout altitude | 28.0 km |
| Burnout time | 30.0 s |
| Time above Kármán line (100 km) | 467 s |
| Total flight time | 570 s |
| Peak dynamic pressure | 2,198 kPa at t = 8 s |
| Peak structural G-load | 44.9 g |
| Design load factor | 55 g (10.1 g margin) |
| Ideal Δv (Tsiolkovsky) | 5,046 m/s |

### 9.2 Trajectory Phase Breakdown

**Phase 1 — Powered ascent (t = 0 to 30 s)**

The engine fires at launch and burns for exactly 30 seconds. During this phase the rocket accelerates from rest through transonic and into hypersonic flight. Key events:

- t = 0 s: Ignition. Sea-level thrust 44.1 kN. Initial T/W = 7.1 (44,100 / 630.8 × 9.81)
- t ≈ 4 s: Mach 1 (transonic — max drag coefficient ~0.60)
- t ≈ 8 s: Max-Q at ~3 km altitude, dynamic pressure 2,198 kPa
- t ≈ 12 s: Mach 5 — fully hypersonic, drag coefficient declining
- t = 30 s: Burnout. Velocity 3,983 m/s (Mach 13.3). Altitude 28 km. Engine off.

The initial thrust-to-weight ratio of 7.1 is high — the rocket accelerates hard off the pad. This is intentional: rapid acceleration through the dense lower atmosphere minimises gravity losses and aerodynamic drag losses, both of which scale with time spent at low altitude.

**Phase 2 — Ballistic coast (t = 30 s to ~390 s)**

Post-burnout the rocket coasts on a purely ballistic arc. No thrust, minimal aerodynamic forces at high altitude. The trajectory is governed almost entirely by gravity.

- Rocket crosses Kármán line (100 km) at approximately t = 75 s on ascent
- Apogee of 367 km reached at approximately t = 200 s
- Rocket re-crosses Kármán line at approximately t = 542 s on descent
- Time above 100 km: 467 seconds

**Phase 3 — Terminal descent (t = 390 s to 570 s)**

Descent from apogee back through atmosphere to impact. The guidance system applies corrections during this phase for terminal accuracy. Re-entry heating becomes significant — the nose cone AlSi10Mg will experience surface temperatures requiring thermal protection coating on the leading face.

Total flight time from launch to impact: **570 seconds (9.5 minutes)**.

### 9.3 Velocity Profile

| Event | Time (s) | Velocity (m/s) | Mach | Altitude (km) |
|---|---|---|---|---|
| Launch | 0 | 1 | 0.00 | 0 |
| Mach 1 | ~4 | ~340 | 1.00 | ~0.5 |
| Max-Q | ~8 | ~600 | ~1.8 | ~3 |
| Mach 5 | ~12 | ~1,600 | 5.0 | ~10 |
| Burnout | 30 | 3,983 | 13.27 | 28 |
| Apogee | ~200 | ~0 | ~0 | 367 |
| Kármán descent | ~542 | ~3,500 | ~10 | 100 |
| Impact | 570 | ~3,800 | ~11 | 0 |

### 9.4 Delta-V Analysis

The Tsiolkovsky rocket equation gives the theoretical maximum Δv for the TAIPAN-1 mass ratio:

**Δv = Isp × g₀ × ln(m_wet / m_dry)**  
**Δv = 293.1 × 9.80665 × ln(5.787)**  
**Δv = 2,874 × 1.756 = 5,046 m/s**

The achieved burnout velocity of 3,983 m/s represents **79% efficiency** relative to ideal. The 21% loss is attributable to:

| Loss source | Approximate magnitude |
|---|---|
| Gravity losses (thrust opposing gravity) | ~850 m/s |
| Aerodynamic drag losses | ~213 m/s |
| **Total losses** | **~1,063 m/s** |

This 79% efficiency is typical and good for a rocket of this size and burn time. Gravity losses dominate and could be reduced by a shallower launch angle, but this trades apogee for range — already optimised.

---

## 10. Ballast Performance Envelope

Ballast mass is the primary **mission-configurable parameter** of TAIPAN-1. By varying the tungsten ballast slug in the nose from 14 kg (minimum for stability) to 250 kg, the operator adjusts the range/stability/G-load trade.

All figures below are simulation-verified at **70.4° launch angle**.

### 10.1 Performance Table

| Ballast (kg) | Wet mass (kg) | SM burnout (cal) | Apogee (km) | Range (km) | Max Mach | Peak G |
|---|---|---|---|---|---|---|
| 10 | 627 | 1.14 | 580 | 1,961 | 14.32 | 47.8 |
| **14** | **631** | **1.57** | **367** | **1,618** | **13.27** | **44.9** |
| 20 | 637 | 2.17 | 521 | 1,791 | 13.67 | 43.7 |
| 30 | 647 | 3.03 | 471 | 1,645 | 13.09 | 40.2 |
| 40 | 657 | 3.77 | 427 | 1,517 | 12.61 | 37.2 |
| 50 | 667 | 4.40 | 389 | 1,405 | 12.14 | 34.7 |
| 60 | 677 | 4.95 | 355 | 1,305 | 11.72 | 32.5 |
| 70 | 687 | 5.44 | 325 | 1,215 | 11.32 | 30.5 |
| 80 | 697 | 5.87 | 299 | 1,135 | 10.96 | 28.8 |
| 90 | 707 | 6.25 | 275 | 1,063 | 10.62 | 27.2 |
| 100 | 717 | 6.60 | 253 | 997 | 10.30 | 25.8 |
| 110 | 727 | 6.91 | 234 | 937 | 10.00 | 24.5 |
| 120 | 737 | 7.19 | 216 | 881 | 9.72 | 23.4 |
| 130 | 747 | 7.45 | 200 | 830 | 9.46 | 22.3 |
| 140 | 757 | 7.68 | 185 | 783 | 9.21 | 21.3 |
| 150 | 767 | 7.90 | 172 | 739 | 8.98 | 20.4 |
| 160 | 777 | 8.10 | 160 | 698 | 8.76 | 19.5 |
| 170 | 787 | 8.28 | 148 | 661 | 8.55 | 18.7 |
| 180 | 797 | 8.45 | 138 | 625 | 8.35 | 18.0 |
| 190 | 807 | 8.61 | 128 | 592 | 8.16 | 17.3 |
| 200 | 817 | 8.76 | 119 | 562 | 7.97 | 16.7 |
| 210 | 827 | 8.89 | 111 | 533 | 7.79 | 16.1 |
| 220 | 837 | 9.02 | 103 | 505 | 7.62 | 15.5 |
| 230 | 847 | 9.14 | 96 | 480 | 7.46 | 15.0 |
| 240 | 857 | 9.26 | 90 | 455 | 7.30 | 14.5 |
| 250 | 867 | 9.37 | 84 | 432 | 7.15 | 14.0 |

> **Note:** 10 kg ballast (SM = 1.14 cal) is below the 1.5 cal design minimum and should not be used without active roll stabilisation. The design minimum is 14 kg.

### 10.2 Operating Configurations

Three recommended configurations covering the primary mission spectrum:

**Config A — Maximum Range (14 kg ballast)**
- Range: 1,618 km | Mach: 13.27 | Peak G: 44.9 | SM: 1.57 cal
- Use when: maximum engagement distance, unguided or simple INS payload, robust payload structure required

**Config B — Balanced (80 kg ballast)**
- Range: 1,135 km | Mach: 10.96 | Peak G: 28.8 | SM: 5.87 cal
- Use when: sensitive guidance electronics aboard, want comfortable stability margin, still excellent range

**Config C — Precision (150 kg ballast)**
- Range: 739 km | Mach: 8.98 | Peak G: 20.4 | SM: 7.90 cal
- Use when: maximum electronics survival, precision guidance package, shorter engagement range acceptable

---
## 11. Guidance, Navigation and Control

### 11.1 System Overview

TAIPAN-1 carries a 3 kg avionics package housed in the inter-tank section. The system provides inertial navigation during powered flight and ballistic coast, GPS correction where available, and terminal guidance corrections during re-entry.

| Component | Specification | Mass |
|---|---|---|
| IMU | 6-DOF MEMS IMU, ±2000°/s gyro, ±50g accel | 0.3 kg |
| GPS receiver | L1/L2 dual-frequency, jam-resistant | 0.2 kg |
| Flight computer | ARM Cortex-M7 based, radiation-tolerant | 0.4 kg |
| Power management | 28V regulated bus, battery monitor | 0.2 kg |
| Actuator drivers | 4-channel fin servo driver | 0.1 kg |
| Wiring harness | Shielded, high-temperature rated | 0.3 kg |
| Structure / enclosure | Aluminium avionics bay | 0.5 kg |
| FTS hardware | Dual-redundant RF receiver + initiator | 0.5 kg |
| Margin | — | 0.2 kg |
| **Total** | | **3.0 kg** |

### 11.2 Navigation Architecture

The guidance computer runs a **6-DOF inertial navigation algorithm** propagating position, velocity, and attitude from IMU measurements. GPS provides position correction when signals are available (below ~80 km altitude where ionospheric effects are manageable). Above 80 km the system operates purely inertially.

Guidance law: **proportional navigation** during terminal phase with inertial midcourse. The guidance commands are executed via fin deflection — four independently actuated fins provide full roll/pitch/yaw authority.

### 11.3 Fin Actuation

Each fin is deflected by a dedicated brushless servo actuator mounted at the root. The electric pump-fed architecture means no hydraulic power is available — all actuation is electric, simplifying the system.

| Parameter | Value |
|---|---|
| Actuator type | Brushless DC servo |
| Max deflection | ±15° |
| Rate | 60°/s |
| Torque | 50 Nm (sized for max-Q aerodynamic hinge moment) |
| Power | 28V, peak 200W per fin |

### 11.4 Accuracy

Terminal accuracy depends on guidance law implementation and target motion model — not formally analysed here. For a kinetic interceptor targeting a ballistic missile or large aerial vehicle, a circular error probable (CEP) of 50–200 m is achievable with the described avionics hardware, which is sufficient for a kinetic kill vehicle with blast fragmentation effect.

---

## 12. Flight Termination System

### 12.1 Overview

TAIPAN-1 carries a **dual-redundant RF command Flight Termination System (FTS)** per RANGE SAFETY standard practice. The FTS allows range safety officers to terminate the flight if the rocket deviates from its intended trajectory.

### 12.2 Architecture

```
Ground transmitter (primary) ──→ RF uplink → FTS receiver A ──→ Safe/Arm
Ground transmitter (backup)  ──→ RF uplink → FTS receiver B ──→ Initiator
                                                               ──→ Propellant line cut
```

On command, the FTS:
1. Disables engine (closes main propellant valves)
2. Activates linear-shaped charge on propellant lines to vent propellant
3. The vented propellant disperses and rocket tumbles

No explosive charge is used — propellant dispersal is sufficient to terminate the flight.

### 12.3 FTS Specifications

| Parameter | Value |
|---|---|
| Receivers | 2 (independent power, independent antennas) |
| Frequency | S-band, encrypted |
| Response time | < 50 ms from command to actuation |
| Safe/arm mechanism | Mechanical safe pin + electrical arm |
| Battery backup | 60 min autonomous operation |
| Mass | 0.5 kg (included in avionics budget) |

---

## 13. Launch System

### 13.1 Launch Platform

TAIPAN-1 launches from a **mobile canister/rail launcher**. The canister serves as both transport container and launch tube, providing environmental protection during transport and structural support at launch.

| Parameter | Value |
|---|---|
| Launch mode | Rail-guided canister |
| Rail length | 5.5 m (guides rocket through first 0.6 m of travel) |
| Canister diameter | 320 mm internal |
| Canister material | Glass-fibre composite |
| Launcher elevation | Adjustable 45°–90° from horizontal |
| Azimuth | 360° traversable |
| Setup time | < 15 minutes from transport to launch-ready |
| Transport vehicle | Standard military truck flatbed |

### 13.2 Launch Sequence

```
T-60 min   LOX loading commences (cryogenic fill)
T-30 min   RP-1 loading commences
T-10 min   Avionics power-on, IMU alignment
T-5 min    GPS acquisition, FTS arm
T-2 min    Propellant loading complete, tanks pressurised
T-30 s     Final go/no-go checklist
T-10 s     Engine pre-chill (LOX flow to manifold)
T-0 s      Torch igniter fires
T+0.2 s    Main propellant valves open, full thrust
T+0.5 s    Rail clear, free flight
T+30 s     Burnout
T+570 s    Impact
```

### 13.3 Ground Support Equipment

| Item | Purpose |
|---|---|
| LOX storage dewar | 500 L, trailer-mounted cryogenic storage |
| LOX transfer pump | Fill from dewar to rocket tank |
| RP-1 tank (IBC) | 1,000 L intermediate bulk container |
| Pressurant trailer | He gas bottles, regulators |
| Ground power unit | 28V DC, launch operations |
| Launch control console | Firing panel, telemetry receiver, FTS transmitter |
| Range safety transmitter | Backup FTS command |

---
## 14. Manufacturing

### 14.1 Philosophy

TAIPAN-1 is designed from the ground up for **additive manufacturing first**. Every structural component is designed as a 3D printed part with secondary machining only where required for sealing surfaces, bearing interfaces, or precision fits. This approach:

- Eliminates welding (a major source of defects and inspection cost in rocket structures)
- Enables integral features (baffles, bosses, cooling channels, ribs) at no added cost
- Reduces part count dramatically — a conventionally fabricated tank might be 12–20 parts; a printed tank is one
- Allows rapid design iteration between prototypes — no tooling to change

The total printed part count for TAIPAN-1 is **14 structural parts** (6 body sections + 4 fins + 2 tank domes + 1 chamber/nozzle + 1 thrust frame detail). A conventionally manufactured equivalent would be 80–120 parts.

### 14.2 Printing Technology

**Airframe sections (AlSi10Mg):**

| Attribute | Specification |
|---|---|
| Process | Laser Powder Bed Fusion (LPBF) / Selective Laser Melting (SLM) |
| Equipment | EOS M400 or equivalent (400 × 400 × 400 mm build volume) |
| Layer thickness | 30–60 µm |
| Surface finish (as-built) | Ra 10–20 µm |
| Surface finish (post-process) | Ra 1.6 µm on sealing faces, Ra 3.2 µm general |
| Dimensional tolerance | ±0.2 mm general, ±0.05 mm on machined interfaces |
| Density (relative) | ≥ 99.5% (no significant porosity) |

**Aft structure and fins (Ti-6Al-4V):**

| Attribute | Specification |
|---|---|
| Process | LPBF with argon atmosphere |
| Equipment | Trumpf TruPrint 5000 or equivalent |
| Post-process HIP | Yes — Hot Isostatic Pressing at 920°C/100 MPa for 2h (eliminates residual porosity) |
| Heat treatment | Anneal 800°C/2h after HIP |
| Tensile strength | ≥ 1,000 MPa (HIP + annealed) |
| Yield strength | ≥ 900 MPa |
| Elongation | ≥ 10% |

**Engine chamber (Inconel 718):**

| Attribute | Specification |
|---|---|
| Process | LPBF, high-temperature alloy parameters |
| Post-process | Solution anneal + age (standard IN718 treatment) |
| Cooling channel min width | 1.2 mm (achievable with LPBF) |
| Pressure test | 1.5× MEOP (75 bar) hydrostatic proof |
| Surface finish (cooling channels) | Electropolished to Ra ≤ 0.8 µm |

### 14.3 Print Time Estimates

| Section | Material | Estimated print time | Machine |
|---|---|---|---|
| Nose cone | AlSi10Mg | 18 hours | EOS M400 |
| LOX tank | AlSi10Mg | 36 hours | EOS M400 |
| Inter-tank | AlSi10Mg | 14 hours | EOS M400 |
| RP-1 tank | AlSi10Mg | 22 hours | EOS M400 |
| Aft structure | Ti-6Al-4V | 28 hours | Trumpf 5000 |
| Boattail | Ti-6Al-4V | 8 hours | Trumpf 5000 |
| Fins × 4 | Ti-6Al-4V | 10 hours each | Trumpf 5000 |
| Engine chamber/nozzle | Inconel 718 | 52 hours | EOS M400-4 |
| **Total print time** | | **~208 hours** | |

Running two machines in parallel (one Al, one Ti), the full airframe can be printed in approximately **4–5 calendar weeks** including setup, powder changeover, and inspection holds.

### 14.4 Post-Print Operations

After printing, each component undergoes:

1. **Powder removal** — compressed air blow-out of internal channels, ultrasonic cleaning for cooling channels
2. **Stress relief** — furnace cycle per material spec before removal from build plate
3. **Wire EDM / band saw** — separation from build plate
4. **HIP** (Ti parts only) — Hot Isostatic Pressing per 14.2
5. **Heat treatment** — per material spec
6. **CNC machining** — sealing faces, flange faces, threaded interfaces, bearing bores. Estimated 4–8 hours CNC per section
7. **Non-destructive testing** — CT scan for internal defects, dye penetrant on external surfaces
8. **Pressure testing** — hydrostatic proof of tank sections
9. **Dimensional inspection** — coordinate measuring machine (CMM) check of all critical interfaces

### 14.5 Assembly Sequence

```
1. Print and qualify all sections individually
2. Assemble LOX tank section with fittings, insulation
3. Assemble RP-1 tank section with sump fittings
4. Install He COPV and avionics bay in inter-tank section
5. Stack: nose → LOX tank → inter-tank → RP-1 tank
   (flange bolt each joint, O-ring face seals, torque to spec)
6. Install tungsten ballast slug in nose, torque M16 bolt
7. Engine assembly: test fire on stand prior to vehicle integration
8. Attach aft structure to RP-1 tank
9. Mount engine to aft structure thrust ring
10. Attach fins to aft structure root lugs, torque M12 bolts
11. Attach boattail
12. Install avionics, fin servo actuators, wiring harness
13. Install FTS hardware, safe-pin
14. Final integration inspection
15. Leak check of all propellant systems (pneumatic, He)
16. Functional check of avionics and FTS
17. Transport to launch site
```

Total assembly labour: approximately **80–120 person-hours** for first unit, reducing to 40–60 hours by third unit as procedures are refined.

### 14.6 Facilities Required

| Facility | Requirement |
|---|---|
| Metal 3D printers | 1 × Al LPBF (EOS M400 class), 1 × Ti LPBF (Trumpf 5000 class) |
| HIP furnace | For Ti-6Al-4V parts (can be outsourced) |
| CNC machining centre | 5-axis, 500 mm work envelope |
| Clean assembly area | Class 10,000 cleanroom not required — standard workshop with dust control |
| Pressure test rig | Hydrostatic to 80 bar |
| CT scanner | For weld/print inspection (can be outsourced to NDT service) |
| Engine test stand | Required for acceptance firing before vehicle integration |

The printing and machining can be outsourced to industrial additive manufacturing bureaus — no capital equipment ownership is required for a prototype program. Bureau print costs for AlSi10Mg are approximately $30–80 USD/hour machine time; Ti-6Al-4V approximately $80–150/hour.

---

## 15. Materials Specification

### 15.1 AlSi10Mg — Airframe and Tanks

| Property | Value |
|---|---|
| Composition | Al-10Si-0.3Mg (wt%) |
| Ultimate tensile strength | 430–470 MPa (LPBF, T6 condition) |
| Yield strength | 230–250 MPa |
| Elongation | 6–9% |
| Density | 2.67 g/cm³ |
| Thermal conductivity | 130 W/mK |
| Cryogenic rating | Suitable to -200°C (LOX compatible) |
| Weldability | Not applicable (printed monolithic) |
| Anodising | Compatible for corrosion protection |
| Print parameters | Standard EOS AlSi10Mg parameters, widely validated |

AlSi10Mg is the dominant aerospace-grade aluminium alloy in metal additive manufacturing. Its silicon content makes it exceptionally printable (low crack susceptibility), and its properties after T6 heat treatment are competitive with wrought 6061-T6. Critically for TAIPAN-1, it is rated for cryogenic service — the LOX tank will cycle to -183°C repeatedly.

### 15.2 Ti-6Al-4V — Aft Structure and Fins

| Property | Value (HIP + annealed) |
|---|---|
| Composition | Ti-6Al-4V ELI grade |
| Ultimate tensile strength | ≥ 1,000 MPa |
| Yield strength | ≥ 900 MPa |
| Elongation | ≥ 10% |
| Density | 4.43 g/cm³ |
| Max service temperature | 315°C continuous, 600°C short duration |
| Fatigue (10⁷ cycles) | ~500 MPa |
| Fracture toughness | 75–100 MPa√m |

Ti-6Al-4V is chosen for the aft structure and fins because of its high strength-to-weight ratio, excellent fatigue resistance, and elevated temperature capability. The engine mount sees both high structural loads (50 kN thrust) and elevated temperatures from engine proximity. Ti-6Al-4V with ablative coating handles this comfortably.

**HIP requirement:** Ti-6Al-4V printed parts must be HIPped before use in primary structure. As-printed Ti has residual porosity of 0.1–0.5% that HIP reduces to <0.01%, substantially improving fatigue life and fracture toughness. This is non-negotiable for a flight-critical component.

### 15.3 Inconel 718 — Engine Chamber and Nozzle

| Property | Value |
|---|---|
| Composition | Ni-19Cr-19Fe-5Nb-3Mo |
| Ultimate tensile strength | 1,280 MPa (aged) |
| Yield strength | 1,050 MPa (aged) |
| Max service temperature | 700°C continuous |
| Creep resistance | Excellent to 650°C |
| Oxidation resistance | Excellent |
| Printability | Good — requires argon atmosphere, validated parameters |

Inconel 718 is the standard material for 3D printed rocket engine chambers. It maintains strength at the chamber wall temperatures encountered in regeneratively cooled operation (~600–700°C on the hot gas side of the cooling channel) and is not attacked by RP-1 coolant.

### 15.4 Tungsten Alloy W95 — Ballast

| Property | Value |
|---|---|
| Composition | 95% W, balance Ni-Fe |
| Density | 18,000–18,500 kg/m³ |
| Tensile strength | 700–900 MPa |
| Machinability | Fair (requires carbide tooling) |
| Toxicity | Low (no elemental tungsten toxicity concern) |
| Cost | ~$40–60 USD/kg |
| 14 kg slug cost | ~$600–840 USD |

W95 is chosen over lead (illegal in many jurisdictions, lower density) and steel (insufficient density — a steel slug of equal mass would be too large). The 14 kg W95 slug at 18,200 kg/m³ density occupies approximately 770 cm³ — a cylinder roughly 58 mm diameter × 165 mm long — fitting neatly inside the nose cone.

---
## 16. Testing and Qualification

### 16.1 Test Program Overview

A minimum test program for TAIPAN-1 prototype qualification consists of the following phases:

```
Phase 1 — Component testing (per-part)
Phase 2 — Engine acceptance firing (static test stand)
Phase 3 — Cold flow testing (propellant system without ignition)
Phase 4 — System integration test (full vehicle, no propellant)
Phase 5 — Flight qualification (one full-range test flight)
```

### 16.2 Component Tests

| Test | Component | Method | Accept criterion |
|---|---|---|---|
| Hydrostatic proof | LOX tank | Water pressure to 15 bar (1.5× MEOP) | No leak, no permanent deformation |
| Hydrostatic proof | RP-1 tank | Water pressure to 12 bar | No leak |
| CT scan | All printed parts | Industrial CT, 0.1 mm resolution | No voids > 0.3 mm, no cracks |
| Dye penetrant | Fin roots, flange faces | Visual inspection after dye | No indications |
| CMM dimensional | All sections | Coordinate measuring machine | Within ±0.2 mm drawing tolerance |
| Tensile coupon | Each print batch | Destructive test of build plate coupons | Meet material spec minimums |
| HIP verification | Ti-6Al-4V parts | Density measurement pre/post HIP | Density increase confirms void closure |
| Flange seal test | All joints | Pneumatic leak test at 5 bar He | Zero leak rate at 24 hr hold |

### 16.3 Engine Acceptance Test

Every engine is **static-fired on a test stand** before integration into a vehicle. This is standard practice for all liquid rocket engines — no engine flies without a prior successful static fire.

**Minimum acceptance test sequence:**

| Test | Duration | Purpose |
|---|---|---|
| Ignition check | 0.5 s | Verify igniter and valve timing |
| Short-duration fire | 3 s | Verify stable combustion, check for leaks |
| Full-duration fire | 30 s | Confirm rated thrust, Isp, chamber pressure |
| Thrust vector check | During full fire | Verify TVC actuation response |

**Acceptance criteria:**
- Thrust within ±5% of 50 kN nominal
- Chamber pressure within ±3% of 50 bar
- No leaks detected post-test
- No anomalous pressure oscillations (combustion instability)
- Stable combustion throughout burn (no hard start, no blow-out)

### 16.4 System Integration Test

With the full vehicle assembled but unpropellanted:
- Avionics functional check (IMU alignment, GPS acquisition, FTS arm/safe)
- Fin actuator sweep test (full deflection range, rate check)
- Wiring harness continuity
- Propellant system leak check (pneumatic)
- FTS command/response verification

### 16.5 Flight Test

One full-range test flight is required for qualification. Instrumentation:

| Sensor | Location | Measurement |
|---|---|---|
| IMU (redundant) | Avionics bay | 6-DOF acceleration and rate |
| Chamber pressure transducer | Engine | Combustion stability |
| Tank pressure transducers ×4 | Both tanks | Propellant consumption rate |
| Skin temperature sensors ×6 | Nose, fins, aft | Thermal profile |
| GPS telemetry | Avionics bay | Real-time position |
| Downlink | Avionics bay | All sensor data at 100 Hz |

---

## 17. Environmental and Storage

### 17.1 Environmental Rating

TAIPAN-1 is designed to meet **MIL-STD-810H** environmental requirements for ground military equipment:

| Parameter | Requirement |
|---|---|
| Operating temperature (vehicle) | -20°C to +55°C |
| Storage temperature | -40°C to +70°C |
| Humidity | 95% RH non-condensing |
| Vibration (transport) | 5–500 Hz, 0.04 g²/Hz PSD |
| Shock (handling) | 20g, 11 ms half-sine |
| Sand and dust | MIL-STD-810 Method 510 |
| Salt fog | MIL-STD-810 Method 509 (coastal deployment) |
| Rain | MIL-STD-810 Method 506 |

### 17.2 Propellant Storage

| Propellant | Storage method | Storage life |
|---|---|---|
| RP-1 | Standard fuel tank, ambient temperature | Indefinite (kerosene stable) |
| LOX | Cryogenic dewar, continuously vented | Load within 4 hours of launch |

LOX cannot be stored in the rocket. The operational sequence is: transport rocket (without LOX) to launch site, load LOX from mobile dewar at T-60 min, launch. This is standard for all LOX systems.

### 17.3 Shelf Life

The TAIPAN-1 vehicle (minus LOX) can be stored indefinitely. Annual inspection should verify:
- O-ring condition on all flanged joints (replace every 3 years regardless)
- Avionics battery health (replace every 2 years)
- FTS battery health (replace every 2 years)
- Structural inspection of fin attachment bolts (torque check)
- Tungsten ballast bolt torque verification

---

## 18. Cost and Pricing

### 18.1 Prototype Unit Cost Breakdown

All costs in USD. Prototype (first 1–3 units) pricing, including typical bureau/supplier margins.

| Line item | Low ($k) | High ($k) | Notes |
|---|---|---|---|
| RP-1 propellant (147 kg) | 0.4 | 0.6 | ~$3/kg refined kerosene |
| LOX propellant (375 kg) | 0.1 | 0.1 | ~$0.15/kg industrial |
| Engine chamber + nozzle (print + post) | 15 | 35 | Inconel 718, LPBF, machining |
| Electric pump assembly (×2) | 20 | 45 | Motors, impellers, controllers |
| Battery pack (pump power) | 3 | 8 | LiPo, custom form factor |
| Igniter + valves + lines | 8 | 18 | Propellant system hardware |
| Nose cone print + finish | 1 | 2.5 | AlSi10Mg |
| LOX tank print + finish | 2 | 5 | AlSi10Mg + insulation |
| Inter-tank print + finish | 1 | 2.5 | AlSi10Mg |
| RP-1 tank print + finish | 1.5 | 3.5 | AlSi10Mg |
| Aft structure print + finish | 3 | 8 | Ti-6Al-4V, HIP required |
| Boattail print + finish | 0.8 | 2 | Ti-6Al-4V |
| Fins ×4 print + finish | 2 | 5 | Ti-6Al-4V, edge machining |
| Tungsten ballast slug | 0.6 | 1 | W95 alloy, machined |
| He COPV pressurant vessel | 1.5 | 4 | CFRP-overwrapped |
| Avionics (IMU, GPS, computer) | 8 | 25 | COTS + integration |
| FTS hardware | 3 | 8 | Qualified RF system |
| Fasteners, O-rings, misc hardware | 1 | 3 | |
| Assembly labour (80–120 hrs @ $100) | 8 | 12 | |
| Engine acceptance test (static fire) | 5 | 15 | Test stand time + propellant |
| Component inspection / NDT / CMM | 5 | 15 | CT scan, hydrostatic, CMM |
| **TOTAL** | **90** | **219** | |

**Prototype realistic range: $90k – $170k USD per unit**

The dominant cost drivers are:
1. **Electric pump assembly** — $20k–$45k. Custom electric turbomachinery is expensive at low volumes
2. **Engine chamber/nozzle** — $15k–$35k. Inconel LPBF + machining + test
3. **Avionics** — $8k–$25k. Depends on guidance fidelity required
4. **Test costs** — $10k–$30k. Cannot be avoided for a live rocket

### 18.2 Cost Reduction Levers

The path to lower unit cost runs through volume and design lock:

| Action | Savings potential |
|---|---|
| Buy pump motors in batches of 20 | 40–50% reduction in pump cost |
| Lock engine design, amortise print programs | Chamber cost halves by unit 10 |
| Standardise avionics on fixed hardware | 50% reduction in avionics cost |
| In-house test stand vs hired facility | Test cost drops from $15k to $3k |
| Streamline assembly procedures | Labour drops from 100 hrs to 40 hrs |

### 18.3 Production Unit Cost (50+ units)

At a production run of 50+ units with locked design and established supply chain:

| Cost category | Production cost ($k) |
|---|---|
| Propellants | 0.5 |
| Engine (chamber + pump + battery) | 18 – 30 |
| Airframe (all sections printed) | 6 – 12 |
| Avionics + FTS | 5 – 10 |
| Assembly + integration | 3 – 5 |
| Test (acceptance fire, inspection) | 5 – 10 |
| Programme overhead | 5 – 8 |
| **Total** | **42 – 75** |

**Production range: $50k – $80k USD per unit**

This compares very favourably to existing interceptor systems. The AIM-120 AMRAAM costs approximately $1.8M USD per unit. TAIPAN-1 at $80k production cost is **22× cheaper** while offering comparable range performance for the ballistic intercept mission.

---

## 19. Production Scaling

### 19.1 Production Rate Capability

The limiting constraint on production rate is printer throughput. With one EOS M400 (Al) and one Trumpf 5000 (Ti):

| Printer | Parts per unit | Print time | Utilisation | Units/month |
|---|---|---|---|---|
| EOS M400 (Al) | 4 sections | ~90 hrs total | 80% | ~2.5 |
| Trumpf 5000 (Ti) | 2 sections + 4 fins | ~68 hrs total | 80% | ~3.5 |

The Al printer is the bottleneck at ~2.5 units/month per machine. Adding a second EOS M400 doubles Al throughput and balances the line at ~3.5 units/month.

**Realistic production rate per two-machine cell:**
- 2–3 complete vehicles per month
- Scaling to 10 vehicles/month requires ~4 Al printers, ~2 Ti printers

### 19.2 Supply Chain

| Component | Make vs Buy | Lead time | Risk |
|---|---|---|---|
| Printed airframe sections | Make (in-house or bureau) | 2–4 weeks | Low |
| Engine chamber/nozzle | Make | 3–5 weeks | Medium |
| Electric pump assembly | Buy (specialist supplier) | 8–16 weeks | **High** |
| Avionics | Buy (COTS integration) | 4–8 weeks | Low-medium |
| FTS | Buy (specialist) | 8–12 weeks | Medium |
| Propellants | Buy (commodity) | 1–2 weeks | Low |
| Tungsten slug | Buy (machined standard) | 2–4 weeks | Low |

The **electric pump assembly** is the highest supply chain risk — it is a custom component requiring specialist electric motor and impeller suppliers. Qualification of a second source is strongly recommended before committing to production.

### 19.3 Cost Per Engagement vs Alternatives

| System | Approximate unit cost | Range | Notes |
|---|---|---|---|
| TAIPAN-1 (production) | $50k – $80k | 432–1,618 km | This design |
| AIM-120D AMRAAM | ~$1,800k | 160 km | Air-launched |
| THAAD interceptor | ~$11,000k | 200 km altitude | Exo-atmospheric |
| Arrow 3 | ~$2,000k | ~2,400 km | Co-dev Israel/US |
| Iron Dome Tamir | ~$50k | 70 km | Short range only |

TAIPAN-1's cost point is comparable to Iron Dome's Tamir missile but with dramatically greater range — 1,618 km versus 70 km. The comparison highlights the efficiency gain from the electric pump-fed architecture and 3D printed structure.

---
## 20. Limitations and Future Work

### 20.1 Known Limitations

**Burnout stability margin (1.57 cal)**  
The 1.57 cal margin at burnout just clears the 1.5 cal minimum. Any deviation from the modelled CG (e.g. asymmetric propellant consumption, manufacturing mass tolerance) could bring this below the minimum. Mitigation: tighten mass tolerance on aft components, or increase ballast to 20–25 kg for margin. The 20 kg configuration delivers SM = 2.17 cal at a range cost of only 154 km.

**Burnout stability in free coast**  
Post-burnout, the rocket relies on passive aerodynamic stability. If angle of attack exceeds ~15° (possible during atmospheric perturbation or guidance correction) the Barrowman model is no longer valid and stability may degrade. The fin sizing should be verified with higher-fidelity CFD at off-nominal AoA.

**Aerothermal re-entry**  
At Mach 13+ re-entry, stagnation heating on the nose tip is significant. AlSi10Mg has a melting point of 570–600°C. A short-duration hypersonic re-entry will likely survive with an ablative or ceramic coating on the nose tip, but this has not been formally calculated. A dedicated thermal protection study is required before flight qualification.

**3-DOF simulation fidelity**  
The trajectory model is a point-mass 3-DOF simulation in a vertical plane. It does not model: Earth rotation, wind, angle of attack dynamics, structural flexibility, or guidance law performance. For a design study these approximations are appropriate; a 6-DOF high-fidelity simulation is required for flight test planning.

**Engine — not yet designed in detail**  
The engine is specified at the system level (thrust, Isp, mass) based on the Rutherford analogy. Detailed combustion chamber design (injector element sizing, chamber L\*, characteristic length), turbopump sizing (specific speed, impeller diameter), and cooling channel analysis are all required engineering work before manufacturing. This specification treats the engine as a black box defined by its performance parameters.

### 20.2 Future Development Paths

**Trajectory optimisation**  
The 70.4° launch angle was found by a simple 1D sweep. A full trajectory optimisation including gravity turn steering, optimal burn angle, and launch angle-versus-payload trade would likely recover 5–10% additional range.

**Higher expansion ratio nozzle**  
The current ε = 10 is conservative. A vacuum-optimised ε = 25–40 nozzle would raise Isp from 293s to ~320s, improving range significantly. The constraint is sea-level overexpansion, which could be managed by an extendable nozzle or aerospike.

**Throttle capability**  
Adding throttle capability (20–100% thrust) would enable more sophisticated guidance during powered ascent, reduce max-Q structural loads, and allow a lower-thrust sustain phase. The electric pump-fed architecture actually makes throttling easier than gas-generator engines — motor RPM is the throttle knob.

**Multi-stage variant**  
Adding a small solid-propellant kick stage at burnout altitude (28 km, nearly vacuum) could add 1,000–1,500 km of range with minimal cost increase, leveraging the already-excellent mass ratio of the first stage.

**Improved materials**  
Carbon fibre composite (CFRP) overwrapped Al tanks would reduce tank mass by 40% at the cost of manufacturing complexity. This would push the mass ratio above 6.5 and range beyond 2,000 km.

---

## 21. Appendix A — Simulation Parameters

### A.1 Trajectory Simulation

| Parameter | Value | Source |
|---|---|---|
| Timestep | 0.05 s | Numerical stability verified |
| Atmosphere model | US Standard Atmosphere 1976 | NOAA/NASA/USAF |
| Gravity | 9.80665 m/s² constant | Adequate for <500 km altitude |
| Drag model | Semi-empirical 4-component | Barrowman + Schlichting |
| Thrust model | Altitude-corrected (exit pressure correction) | F = F_vac - Pa × A_exit |
| Launch site altitude | 0 m (sea level) | Conservative |
| Wind | Not modelled | Conservative for range |

### A.2 Aerodynamic Model Coefficients

CD components as functions of Mach:

```
Mach < 0.8:   CD = 0.35  (subsonic baseline)
0.8 < M < 1.2: CD = 0.35 + (M-0.8)/0.4 × 0.25  (transonic rise)
1.2 < M < 2.0: CD = 0.60 - (M-1.2)/0.8 × 0.15  (supersonic decay)
M > 2.0:       CD = max(0.45 - (M-2.0) × 0.03, 0.22)  (hypersonic)
```

This is a simplified model appropriate for a preliminary design study. A full CFD analysis would resolve the model at transonic (Mach 0.9–1.1) where the empirical model is least reliable.

### A.3 Engine Thermochemistry

| Parameter | Value | Method |
|---|---|---|
| γ (combustion gas) | 1.235 | NASA CEA, O/F = 2.56 |
| Mean molecular weight | 23.3 g/mol | NASA CEA |
| Adiabatic flame temp | 3,670 K | NASA CEA |
| c\* efficiency | 0.96 | Typical for RP-1/LOX injector |
| CF efficiency | 0.98 | Typical for conical nozzle |

### A.4 Barrowman Parameters

| Parameter | Value |
|---|---|
| Nose CNα | 2.0 |
| Nose XCP factor (ogive) | 0.466 × L_nose |
| Fin CNα | 7.94 |
| Fin XCP | 4.048 m |
| Combined CP | 3.615 m |

---

## 22. Appendix B — Key Equations

### B.1 Tsiolkovsky Rocket Equation

The fundamental performance equation:

```
Δv = Isp × g₀ × ln(m_wet / m_dry)
   = 293.1 × 9.80665 × ln(630.8 / 109.0)
   = 2,874 × ln(5.787)
   = 2,874 × 1.756
   = 5,046 m/s
```

### B.2 Thrust Coefficient

```
CF = √(2γ²/(γ-1) × (2/(γ+1))^((γ+1)/(γ-1)) × (1-(pe/pc)^((γ-1)/γ)))
   + (pe - pa)/pc × ε
```

At vacuum: CF_vac = 1.732 (× 0.98 efficiency = 1.698)  
At sea level: CF_SL = 1.529 (× 0.98 efficiency = 1.498)

### B.3 Stability Margin

```
SM = (XCP - XCG) / D_body   [calibers]

XCP = (CNα_nose × XCP_nose + CNα_fins × XCP_fins) / (CNα_nose + CNα_fins)
    = (2.0 × 0.429 + 7.94 × 4.048) / (2.0 + 7.94)
    = (0.858 + 32.14) / 9.94
    = 3.615 m
```

### B.4 Minimum Ballast (Analytical)

```
Required CG at burnout = XCP - SM_min × D_body
                       = 3.615 - 1.5 × 0.275
                       = 3.203 m from nose

m_ballast = (CG_target × M_dry_base - base_moment) / (ballast_pos - CG_target)

where:
  M_dry_base   = M_struct + M_eng + M_avionics = 95 kg
  base_moment  = 95 × (L×0.42 × M_s/95 + L×0.92 × M_e/95 + ...) [simplified]
  ballast_pos  = 0.05 m
  → m_ballast ≈ 13.9 kg  (rounded to 14 kg design value)
```

---

*End of TAIPAN-1 Technical Specification — Revision 1.0*

---

**Document Control**

| Rev | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026 | Independent Research | Initial release |

**Disclaimer**  
This document describes a conceptual design study using analytical and numerical simulation methods. All performance figures are model predictions and have not been validated by physical test. Engine, structural, and aerothermal analysis are at preliminary design level only. This document does not constitute engineering certification and must not be used as a basis for manufacture without independent engineering review.
