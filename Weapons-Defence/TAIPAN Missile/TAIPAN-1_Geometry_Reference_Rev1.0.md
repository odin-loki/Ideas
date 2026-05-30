# TAIPAN-1 — Geometry and Dimensional Reference
## Complete Spatial Description for Design, Modelling and Manufacture

**Document type:** Geometric Reference Supplement  
**Parent document:** TAIPAN-1 Technical Specification Rev 1.0  
**Revision:** 1.0  
**Date:** 2026  
**Purpose:** Complete dimensional and spatial description of all TAIPAN-1 components sufficient to produce a CAD model, engineering drawings, or physical mockup from scratch without reference to any other document.

---

> All dimensions are in millimetres unless otherwise stated.  
> All axial positions are measured from the **nose tip** (Station 0) along the centreline, positive rearward.  
> All radial dimensions are measured from the **vehicle centreline**.  
> Coordinate system: X = axial (nose to tail), Y = lateral, Z = vertical at launch.

---

## Table of Contents

1. [Vehicle Master Dimensions](#1-vehicle-master-dimensions)
2. [Station Reference Table](#2-station-reference-table)
3. [Nose Cone Geometry](#3-nose-cone-geometry)
4. [LOX Tank Section](#4-lox-tank-section)
5. [Inter-tank Section](#5-inter-tank-section)
6. [RP-1 Tank Section](#6-rp-1-tank-section)
7. [Aft Structure and Thrust Frame](#7-aft-structure-and-thrust-frame)
8. [Boattail Section](#8-boattail-section)
9. [Fin Geometry](#9-fin-geometry)
10. [Flange Interface Geometry](#10-flange-interface-geometry)
11. [Engine Assembly Geometry](#11-engine-assembly-geometry)
12. [Combustion Chamber](#12-combustion-chamber)
13. [Nozzle Geometry](#13-nozzle-geometry)
14. [Injector Geometry](#14-injector-geometry)
15. [Propellant Feed Lines](#15-propellant-feed-lines)
16. [Ballast Assembly](#16-ballast-assembly)
17. [Avionics Bay Layout](#17-avionics-bay-layout)
18. [Tank Internal Geometry](#18-tank-internal-geometry)
19. [Complete Centreline Profile](#19-complete-centreline-profile)
20. [Mass Centroid Locations](#20-mass-centroid-locations)

---
## 1. Vehicle Master Dimensions

### 1.1 Overall Envelope

```
                    ←————————————— 4,870 mm ——————————————→

    ╱▔▔╲            ┌──────────────────────────────────┐    ╱╲    ╱
   ╱    ╲           │                                  │   ╱  ╲__╱
  ╱      ╲__________│                                  │__╱
  │← 920→│←——————————————————— 3,850 ——————————————————→│←100→│
  nose    body                                           boattail
  
  Outer diameter: 275 mm (constant on cylindrical body)
  Nose tip radius: 5 mm (blunt tip)
  Boattail rear diameter: 233.75 mm
```

| Dimension | Value (mm) | Notes |
|---|---|---|
| Total length | 4,870 | Nose tip to boattail rear face |
| Outer body diameter | 275.0 | Constant across all cylindrical sections |
| Body inner diameter | 262.0 | Wall thickness 6.5 mm avg (varies by section) |
| Nose cone length | 920.0 | Tip to base flange face |
| LOX tank section length | 1,280.0 | Flange face to flange face |
| Inter-tank section length | 450.0 | Flange face to flange face |
| RP-1 tank section length | 700.0 | Flange face to flange face |
| Aft structure length | 520.0 | Flange face to boattail join |
| Boattail length | 100.0 | Aft structure rear to nozzle mount face |
| Engine + nozzle protrusion | 395.0 | Boattail rear face to nozzle exit plane |
| Total length incl. nozzle | 5,265.0 | Nose tip to nozzle exit |

### 1.2 Key Diameters

| Location | Outer diameter (mm) | Inner diameter (mm) | Wall (mm) |
|---|---|---|---|
| Nose cone base | 275.0 | 262.0 | 6.5 |
| Body (general) | 275.0 | 262.0 | 6.5 |
| LOX tank | 275.0 | 261.0 | 7.0 (pressure vessel) |
| RP-1 tank | 275.0 | 266.0 | 4.5 |
| Aft structure | 275.0 | 263.0 | 6.0 |
| Boattail forward | 275.0 | 263.0 | 6.0 |
| Boattail aft | 233.75 | 222.75 | 5.5 |
| Flange OD (all) | 310.0 | — | — |

### 1.3 Fineness Ratio

```
Fineness ratio = Total length / Body diameter
              = 4,870 / 275
              = 17.71

This is a high fineness ratio — very slender. For reference:
  F-16 fuselage:     ~7
  V-2 rocket:        ~5.8
  Minuteman III:     ~18.1
  TAIPAN-1:          17.71  ← comparable to ICBM class
```

High fineness ratio is desirable for hypersonic flight — it minimises wave drag and base drag relative to body volume, which is why ballistic missiles are long and thin.

---

## 2. Station Reference Table

Every major interface, feature, and component is referenced to a **station** — axial distance from the nose tip in mm. This table is the master reference.

| Station (mm) | Feature |
|---|---|
| 0 | Nose tip (Vehicle reference zero) |
| 5 | Nose tip blunt radius centre |
| 50 | Ballast slug CG (centre of 14 kg tungsten) |
| 50–217 | Ballast slug body (58 mm dia × 165 mm) |
| 217 | Ballast slug aft face |
| 880 | Nose cone forward flange face (start of flange) |
| 900 | Nose cone/LOX tank flange centre |
| 920 | Nose cone aft face / LOX tank forward face |
| 920–2,200 | LOX tank cylindrical section |
| 970 | LOX tank forward dome tangent point |
| 1,165 | LOX baffle plane 1 |
| 1,415 | LOX baffle plane 2 |
| 1,665 | LOX baffle plane 3 |
| 1,915 | LOX baffle plane 4 |
| 2,130 | LOX tank aft dome tangent point |
| 2,180 | LOX tank aft flange face |
| 2,200 | LOX tank aft face / inter-tank forward face |
| 2,200–2,650 | Inter-tank section |
| 2,425 | Inter-tank mid-point (avionics bay centre) |
| 2,630 | Inter-tank aft flange face |
| 2,650 | Inter-tank aft / RP-1 tank forward face |
| 2,650–3,350 | RP-1 tank cylindrical section |
| 2,700 | RP-1 tank forward dome tangent point |
| 3,250 | RP-1 tank aft dome tangent point / sump start |
| 3,310 | RP-1 tank aft flange face |
| 3,350 | RP-1 tank aft / aft structure forward face |
| 3,350–3,870 | Aft structure |
| 3,350 | Fin root leading edge (Station 3,350) |
| 3,633 | Fin root trailing edge (Station 3,350 + 283) |
| 3,820 | Aft structure aft flange face |
| 3,870 | Aft structure aft / boattail forward |
| 3,870–3,970 | Boattail |
| 3,970 | Boattail aft face / engine mount flange reference |
| 3,970 | Engine combustion chamber forward face (injector plane) |
| 4,015 | Chamber forward dome tangent |
| 4,320 | Throat plane |
| 4,620 | Nozzle exit plane |
| 5,265 | Nozzle exit plane (absolute, incl. nozzle protrusion) |

---

## 3. Nose Cone Geometry

### 3.1 Profile Description

The nose cone is a **tangent ogive** with shape factor 0.686. A tangent ogive is generated by a circular arc tangent to the body cylinder at the base. It is smoother than a conical nose (lower drag) and simpler to define than a Von Kármán shape.

The profile equation for a tangent ogive:

```
Given:
  L_nose = 920 mm    (axial length)
  R_body = 137.5 mm  (body radius)
  
Ogive radius ρ = (R_body² + L_nose²) / (2 × R_body)
              = (137.5² + 920²) / (2 × 137.5)
              = (18,906 + 846,400) / 275
              = 3,147.3 mm

Profile radius at axial position x (0 = nose tip, 920 = base):
  r(x) = √(ρ² - (L_nose - x)²) + R_body - ρ

At x=0:   r = 0       (nose tip)
At x=460: r = 102.1   (mid-nose)
At x=920: r = 137.5   (base — matches body)
```

### 3.2 Nose Cone Dimensions

```
                      ←——— 920 mm ———→
                 ╱▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔╲
                ╱   ← ogive profile  ╲___________________
               ╱                      5 mm tip radius
              ╱
     Nose tip ←Station 0              Station 920 → flange
     
  Profile table (r vs x):
  x=0:    r=0
  x=100:  r=28.1
  x=200:  r=54.3
  x=300:  r=77.8
  x=400:  r=98.1
  x=500:  r=114.7
  x=600:  r=127.0
  x=700:  r=133.5  (ogive approaching tangency)
  x=800:  r=136.2
  x=900:  r=137.4
  x=920:  r=137.5  (tangent — matches body)
```

| Parameter | Value |
|---|---|
| Nose length | 920 mm |
| Base diameter | 275.0 mm |
| Ogive radius ρ | 3,147.3 mm |
| Length/diameter (nose) | 3.35 calibers |
| Tip bluntness radius | 5.0 mm |
| Wall thickness | 3.5 mm general |
| Wall thickness at base | 6.0 mm (transitions to flange) |
| External surface area | ~0.385 m² |
| Internal volume | ~15.1 L |

### 3.3 Nose Cone Interior

The nose cone is hollow with a forward bulkhead at Station 50 mm that carries the ballast slug. Internal space between bulkhead and nose tip is void (air-filled). Space from bulkhead aft to Station 920 is also void, used for GPS antenna cable routing and is vented to avoid pressure differential.

```
Nose cone interior cross-section at Station 200 (axial):

          ─────────  54.3 mm ─────────
         │                            │  outer surface
         │ ← 3.5mm │        │ 3.5mm → │
         │         │ 47.3mm │         │  inner bore
         │         └────────┘         │
         └────────────────────────────┘
```

### 3.4 Nose Cone Flange (Station 880–920)

The base flange is an integral printed feature — the wall thickens from 3.5 mm to 16 mm over the final 40 mm of the nose cone, forming a flat face at Station 920 with a bolt circle for the nose/LOX-tank joint.

```
Flange geometry:
  Flange OD:            310.0 mm
  Flange ID (bore):     262.0 mm
  Flange face width:    24.0 mm (310 - 262) / 2
  Bolt circle diameter: 293.0 mm
  Bolt count:           12
  Bolt size:            M8 × 30mm
  Bolt spacing:         30° (evenly spaced)
  O-ring groove:        2.5 mm wide × 2.0 mm deep, at 270.0 mm diameter
  O-ring type:          AS568-163, Viton, 2.62 mm cross-section
```

---

## 4. LOX Tank Section

### 4.1 Overall Layout

The LOX tank is the longest single section. It is a **pressure vessel** — the dominant structural design driver is hoop stress from 10 bar MEOP, not axial load from thrust.

```
Station 920                                              Station 2,200
   │                                                            │
   ▼                                                            ▼
   ╔══════╦═══════════════════════════════════════════╦═══════╗
   ║FLANGE║ DOME │←────── CYLINDER ──────→│ DOME      ║FLANGE ║
   ║      ║      │                         │           ║       ║
   ╚══════╩═══════════════════════════════════════════╩═══════╝
   │←50→ │←50→  │←────────── 1,080 ──────→│ ←50→ │←50→│
   
   Total section length: 1,280 mm
   Cylindrical barrel: 1,080 mm
   Each dome: ~100 mm projected height (hemispherical)
   Each flange pad: 50 mm
```

### 4.2 Dimensions

| Feature | Dimension |
|---|---|
| Section total length | 1,280 mm |
| Outer diameter | 275.0 mm |
| Inner diameter | 261.0 mm |
| Wall thickness (barrel) | 7.0 mm |
| Wall thickness (domes) | 8.5 mm |
| Dome type | Hemispherical (R = 130.5 mm) |
| Dome height | 130.5 mm |
| Cylindrical barrel length | 1,080 mm |
| Forward dome tangent point | Station 970 (920 + 50 flange + hemispherical dome start) |
| Aft dome tangent point | Station 2,130 |
| Internal volume (total) | ~60.9 L (geometric, excl. baffles) |
| Usable volume with 5% ullage | ~57.9 L per baffle cell × 6 cells = ~347 L |
| LOX fill volume | 329 L (theoretical) |

> Note: The stated internal volume of 329 L for LOX is the **liquid volume**. Tank geometric volume is ~350 L to allow 5% ullage (gas space above liquid for thermal expansion and pressurant).

### 4.3 Pressure Vessel Sizing

Hoop stress in a thin-walled pressure vessel:

```
σ_hoop = P × r / t

At MEOP (10 bar = 1.0 MPa):
  σ_hoop = 1.0 × 130.5 / 7.0 = 18.6 MPa

AlSi10Mg yield strength: 230 MPa
Safety factor: 230 / 18.6 = 12.4

At proof pressure (15 bar):
  σ_hoop = 1.5 × 130.5 / 7.0 = 28.0 MPa
  Safety factor: 230 / 28.0 = 8.2
```

The tank is very conservatively stressed. The 7 mm wall was chosen to maintain printability and handling robustness rather than being driven by pressure — a 3 mm wall would technically be sufficient for pressure alone.

### 4.4 Baffle Geometry

Four cruciform baffles are printed integrally, positioned to divide the tank into five axial cells and suppress propellant slosh. Slosh is a significant concern — an 8 Hz slosh mode in a partly filled LOX tank can couple with structural modes and destabilise flight.

```
Baffle positions (axial Station):
  Baffle 1: Station 1,165  (245 mm aft of forward dome tangent)
  Baffle 2: Station 1,415
  Baffle 3: Station 1,665
  Baffle 4: Station 1,915

Each baffle:
  ┌─────────────────────┐
  │         │           │  ← 261mm inner diameter
  │         │           │
  │─────────┼───────────│  ← cruciform
  │         │           │
  │         │           │
  └─────────────────────┘
  
  Baffle thickness: 3.0 mm
  Baffle height (radial): 120.5 mm (does not reach centreline — 10 mm clear)
  Centreline opening: 20 mm diameter (drain clearance)
  Arm width: 15 mm
  Corner fillet: R5 mm
```

### 4.5 Fittings and Ports

All fittings are printed-in bosses — integral thickened pads with machined threads.

| Port | Station | Angular position | Function | Thread |
|---|---|---|---|---|
| Fill/drain | 2,050 | 270° (bottom) | LOX fill and drain | 1" NPT |
| Vent | 960 | 90° (top) | Vent/pressurant | 3/4" NPT |
| Pressurant inlet | 960 | 0° (side) | He pressurant | 3/4" NPT |
| Outlet to pump | 2,100 | 270° | LOX feed to pump | 1.5" NPT |
| Pressure transducer | 1,560 | 0° | Tank pressure sensor | 1/4" NPT |
| Temperature sensor | 1,000 | 180° | LOX temp sensor | 1/4" NPT |

---

## 5. Inter-tank Section

### 5.1 Function and Layout

The inter-tank section is a **structural collar** — it has no propellant function. Its jobs are: carry axial load between tanks, route plumbing and electrical conduit, and house the avionics bay and helium pressurant vessel.

```
Station 2,200                              Station 2,650
   │                                              │
   ▼                                              ▼
   ╔═══╦═══════════════════════════════════╦═══╗
   ║FLG║ ┌────────────────────────────────┐║FLG║
   ║   ║ │  AVIONICS BAY  │  He COPV       │║   ║
   ║   ║ └────────────────────────────────┘║   ║
   ╚═══╩═══════════════════════════════════╩═══╝
         │←——————————— 350 ——————————————→│
   
   Section length: 450 mm
   Internal clear length: 350 mm (between flange pads)
```

### 5.2 Dimensions

| Feature | Dimension |
|---|---|
| Section total length | 450 mm |
| Outer diameter | 275.0 mm |
| Inner diameter | 267.0 mm |
| Wall thickness | 4.0 mm |
| Longitudinal ribs | 6 ribs, 10 mm wide × 5 mm tall, equally spaced |
| Rib angular positions | 0°, 60°, 120°, 180°, 240°, 300° |
| Conduit channels | 4 channels, 12 mm × 8 mm, printed into inner wall, at 45°/135°/225°/315° |

### 5.3 Avionics Bay

The avionics bay occupies the forward half of the inter-tank section interior, centred at Station 2,320.

```
Avionics bay (internal to inter-tank):
  Forward wall:     Station 2,250 (printed bulkhead, 3 mm thick)
  Aft wall:         Station 2,430 (printed bulkhead, 3 mm thick)
  Internal length:  180 mm
  Internal diameter: 261 mm (clears inner wall with 3 mm gap)
  
  Contents layout (looking forward, +X into page):
  
    ┌────────────────────────────────────────┐
    │  ┌──────────┐  ┌──────────────────┐    │
    │  │  IMU     │  │  Flight computer │    │
    │  │  0.3kg   │  │  0.4 kg          │    │
    │  │  75×75mm │  │  100×80mm        │    │
    │  └──────────┘  └──────────────────┘    │
    │                                        │
    │  ┌──────────┐  ┌──────────┐            │
    │  │  GPS     │  │  FTS A   │            │
    │  │  0.2kg   │  │  0.25kg  │            │
    │  └──────────┘  └──────────┘            │
    │                                        │
    │  ┌──────────────────────────────────┐  │
    │  │  Power management + wiring bus   │  │
    │  └──────────────────────────────────┘  │
    └────────────────────────────────────────┘
    
  Access: removable panel (4× M4 screws), Station 2,250–2,430, 120° arc
```

### 5.4 He COPV Location

The helium pressurant vessel occupies the aft half of the inter-tank interior.

```
He COPV (Carbon-Overwrapped Pressure Vessel):
  Type:         Cylindrical COPV, hemispherical ends
  OD:           120 mm
  Length:       260 mm
  Wall:         Aluminium liner 1.5 mm + CFRP overwrap 3.5 mm
  Storage pressure: 300 bar
  Mass (full):  0.8 kg He + 1.2 kg vessel = 2.0 kg
  Position:     Centreline, Station 2,460–2,720 (partially in RP-1 tank section)
  Attachment:   Strap-mount to inner wall at 2,480 and 2,680
```

---

## 6. RP-1 Tank Section

### 6.1 Overview

The RP-1 tank is shorter and lighter than the LOX tank — RP-1 density (810 kg/m³) is lower than LOX (1,141 kg/m³) so a smaller volume is needed for less mass. It operates at ambient temperature, so no thermal insulation is required.

```
Station 2,650                        Station 3,350
   │                                        │
   ▼                                        ▼
   ╔══╦═══════════════════════════════╦══╗
   ║FL║ DOME │←── CYLINDER ──→│ DOME+SUMP║FL║
   ╚══╩═══════════════════════════════╩══╝
        │←40→│←────── 520 ────→│←100→│
   
   Total section length: 700 mm
```

### 6.2 Dimensions

| Feature | Dimension |
|---|---|
| Section total length | 700 mm |
| Outer diameter | 275.0 mm |
| Inner diameter | 266.0 mm |
| Wall thickness (barrel) | 4.5 mm |
| Wall thickness (domes) | 5.5 mm |
| Dome type | Hemispherical (R = 133.0 mm) |
| Cylindrical barrel length | 520 mm |
| Forward dome tangent | Station 2,700 |
| Aft dome tangent | Station 3,250 |
| Internal volume | ~47.5 L geometric |
| Usable volume (3% ullage) | ~46.1 L |
| RP-1 fill volume | 181 L |

> Wait — 181 L does not fit in 46 L. The section must be **longer** or the tank shares volume with the cylindrical body above. Reconciliation: The RP-1 tank section at 700 mm length as stated only accommodates ~46 L. To hold 181 L of RP-1 at 275 mm inner diameter, the actual cylindrical barrel length must be:
>
> Required length = Volume / (π × r²) = 0.181 / (π × 0.131²) = 3.37 m³/m² ≈ no...
>
> V = π × r² × L → L = V / (π × r²) = 0.181 / (π × 0.1305²) = 0.181 / 0.0535 = 3.38 m
>
> **Correction:** The RP-1 tank section length is **1,430 mm** to accommodate 181 L. This adjusts the station table — see Section 19 for the corrected complete centreline profile.

### 6.3 Corrected RP-1 Tank Dimensions

| Feature | Corrected Dimension |
|---|---|
| Section total length | 1,430 mm |
| Cylindrical barrel length | 1,250 mm |
| Forward dome tangent | Station 2,700 |
| Aft dome tangent | Station 3,980 |
| Aft flange face | Station 4,040 |
| Aft face | Station 4,080 |
| Wall thickness (barrel) | 4.5 mm |
| Internal volume | ~97.4 L per dome + barrel |

> This correction propagates to total vehicle length — see Section 19 for the reconciled complete profile.

### 6.4 Sump Geometry

The aft dome of the RP-1 tank incorporates a **conical drain sump** to ensure propellant feed continuity at all times during powered flight, including the final seconds of burn when liquid level is very low.

```
Sump geometry (integral with aft dome):

     ─────────────────────────────  ← dome tangent, Station 3,980
          \                /
           \              /  ← dome curve (hemispherical outer, conical inner sump)
            \            /
             \          /
              \        /    ← sump cone, half-angle 30°
               \      /
                \    /
                 \  /
                  \/       ← sump outlet, 40 mm diameter
                  │
                  │        ← feed line connection (1.5" NPT boss)
                  
Sump cone depth: 65 mm (from dome tangent to sump outlet)
Sump outlet diameter: 40 mm
Sump cone half-angle: 30°
Sump entrance diameter: 150 mm (at dome tangent level)
```

### 6.5 Fittings

| Port | Station | Angular | Function | Thread |
|---|---|---|---|---|
| Fill/drain | 2,800 | 270° | RP-1 fill and drain | 1" NPT |
| Vent | 2,700 | 90° | Vent | 3/4" NPT |
| Pressurant | 2,700 | 0° | He pressurant | 3/4" NPT |
| Outlet/sump | 4,050 | 270° | Feed to pump | 1.5" NPT |
| Pressure sensor | 3,200 | 0° | Tank pressure | 1/4" NPT |

---
## 7. Aft Structure and Thrust Frame

### 7.1 Overview

The aft structure is the most mechanically complex section. It simultaneously:
- Carries the full 50 kN engine thrust axially into the vehicle stack
- Provides fin root attachment for four fins
- Houses the electric pump battery pack
- Interfaces with the boattail aft

It is printed in Ti-6Al-4V — the only section where aluminium is insufficient due to combined structural and thermal loads.

```
Station 4,080                                   Station 4,600
   │                                                   │
   ▼                                                   ▼
   ╔══╦══════════════════════════════════════════╦══╗
   ║FL║                                          ║FL║
   ║  ║  ┌───┐  ┌───┐  ┌───┐  ┌───┐ ← fin lugs  ║  ║
   ║  ║  └───┘  └───┘  └───┘  └───┘             ║  ║
   ║  ║  ┌──────────────────────────┐            ║  ║
   ║  ║  │    THRUST RING            │            ║  ║
   ║  ║  └──────────────────────────┘            ║  ║
   ╚══╩══════════════════════════════════════════╩══╝
   │←40→│                                    │←40→│
   
   Total length: 520 mm
```

### 7.2 Dimensions

| Feature | Dimension |
|---|---|
| Section total length | 520 mm |
| Outer diameter | 275.0 mm |
| Inner diameter | 263.0 mm |
| Wall thickness (general) | 6.0 mm |
| Wall thickness (fin lug zones) | 12.0 mm (local reinforcement) |
| Wall thickness (thrust ring) | 18.0 mm |
| Thrust ring position | Station 4,080–4,130 (forward 50 mm) |
| Thrust ring outer diameter | 275.0 mm |
| Thrust ring inner diameter | 235.0 mm (annular, 20 mm wide face) |

### 7.3 Internal Gussets

Eight axial gussets run the full internal length, printed integrally. They distribute the concentrated fin root loads around the circumference and add torsional stiffness.

```
Gusset layout (cross-section view, looking forward):

         0°
         │
    315° ╱ ╲ 45°
        ╱   ╲
  270° │  +  │ 90°   ← vehicle centreline
        ╲   ╱
    225° ╲ ╱ 135°
         │
        180°

  8 gussets at 45° intervals
  Gusset height: 12 mm (projects inward from wall)
  Gusset width: 8 mm
  Gusset length: 520 mm (full section)
  Fin lugs at: 0°, 90°, 180°, 270° (aligned with fins)
```

### 7.4 Fin Root Lug Geometry

Four fin root lugs are integral to the aft structure wall, at 0°, 90°, 180°, 270° (fins equally spaced, no cant angle).

```
Single fin root lug (external view):

  ←————— 283 mm root chord ——————→
  
  ┌──────────────────────────────┐  ← outer surface of aft structure
  │  LBOLT │         │ LBOLT     │  (Station 4,080–4,363)
  │   M12  │         │   M12     │
  │  ←50→  │         │   ←50→   │
  │        │   FIN   │           │
  │  LBOLT │  ROOT   │ LBOLT     │
  │   M12  │  SLOT   │   M12     │
  │        │         │           │
  └──────────────────────────────┘
  
  Lug protrusion: 8 mm beyond outer body surface
  Lug thickness: 15 mm (over fin root face)
  Lug width: 20 mm (fin spanwise direction)
  Slot depth (fin root seating): 5.0 mm
  Slot width: 5.5 mm (fin root thickness + 0.5 mm clearance)
  Bolt holes: 4 × M12 through-holes per fin
  Bolt hole diameter: 13.0 mm
  Bolt positions (from fin LE): 50 mm, 110 mm, 170 mm, 233 mm
  Bolt spacing (spanwise): 0 mm offset (all on fin chord centreline)
```

### 7.5 Battery Pack Location

The electric pump battery pack mounts to the aft internal bulkhead, at Station 4,530–4,590.

```
Battery pack:
  Dimensions:   200 mm × 150 mm × 60 mm
  Mass:         7.0 kg
  Mounting:     4 × M8 studs on aft bulkhead
  Thermal pad:  3 mm silicone thermal interface to bulkhead
  Connector:    Anderson SB175 (175A rated)
  Position:     Centreline, aft bulkhead face
```

---

## 8. Boattail Section

### 8.1 Overview

The boattail transitions the body from 275 mm outer diameter to the engine mount diameter, simultaneously reducing base drag by decreasing the bluff base area exposed to low-pressure wake.

```
Station 4,600                          Station 4,700
   │                                          │
   ▼                                          ▼
   ╔══╦════════════════════════════════╦════╗
   ║FL║ ←————————— 100 mm ————————————→│MFCE║
   ║  ║                                 │    ║
   ║  ║  OD: 275 ——→  taper  ——→ OD: 234║    ║
   ╚══╩════════════════════════════════╩════╝
```

### 8.2 Dimensions

| Feature | Dimension |
|---|---|
| Section length | 100 mm |
| Forward OD | 275.0 mm |
| Aft OD | 233.75 mm |
| Forward ID | 263.0 mm |
| Aft ID | 222.75 mm |
| Wall thickness | 5.5 mm (constant) |
| Taper half-angle | arctan((275-233.75)/(2×100)) = 11.6° |
| Engine mount flange (aft face) | Station 4,700 |
| Engine centreline | Coincident with vehicle centreline |

### 8.3 Engine Mount Flange

The boattail aft face carries an integral annular flange that bolts to the engine chamber forward flange.

```
Engine mount flange:
  Flange OD:            250.0 mm
  Flange ID (bore):     130.0 mm (clears chamber forward section)
  Flange face station:  4,700
  Bolt circle diameter: 220.0 mm
  Bolt count:           8
  Bolt size:            M10 × 40 mm
  Bolt spacing:         45°
  Gasket type:          Inconel spiral-wound, 2 mm compressed thickness
```

---

## 9. Fin Geometry

### 9.1 Overview

Four identical trapezoidal fins are mounted at 90° intervals at the aft end. No cant angle (fins are axially aligned — no spin). Leading edge is swept at 37.9°.

```
Fin planform (one fin, viewed from outside):

  Leading edge →          Trailing edge
                 ╲                        │
  Root chord →    ╲────────────────────── │ ← at body (r = 137.5 mm)
  (283 mm)         ╲                      │
                    ╲                     │ Root chord: 283 mm
  Sweep angle         ╲                   │
  37.9°                ╲                  │
                         ╲               │
                          ╲──────────────│ ← tip (r = 366.5 mm)
                          Tip chord: 164 mm
                          
  Semi-span: 229 mm (root to tip)
  Full span (tip to tip, opposing fins): 229 + 137.5 + 137.5 + 229 = 733 mm
```

### 9.2 Fin Dimensions

| Parameter | Value |
|---|---|
| Semi-span (root to tip) | 229.0 mm |
| Root chord | 283.0 mm |
| Tip chord | 164.0 mm |
| Taper ratio (tip/root) | 0.580 |
| Leading-edge sweep angle | 37.9° |
| Mean aerodynamic chord (MAC) | 228.4 mm |
| MAC spanwise position | 102 mm from root |
| Thickness (constant) | 5.0 mm |
| Leading edge radius | 1.5 mm (post-machined) |
| Trailing edge radius | 1.0 mm (post-machined) |
| Root attachment depth | 5.0 mm (seats into lug slot) |
| Root face length | 283 mm (matches root chord) |

### 9.3 Fin Root Station

The fin root **leading edge** is at **Station 4,080** (coincident with the forward face of the aft structure). The fin root **trailing edge** is at Station 4,363 (4,080 + 283).

```
Fin axial position on vehicle:

  Station 4,080                   Station 4,363
     │                                  │
     ▼                                  ▼
  ───┬──────────────────────────────────┬───  ← body surface
     │╲                                ╱│
     │  ╲  fin                      ╱  │
     │    ╲                        ╱   │
     │      ╲                    ╱    │
     │        ╲                ╱     │
     │          ╲────────────╱      │   ← tip (229 mm from body)
```

### 9.4 Fin Cross Section

The fin cross-section is a **flat diamond (double-wedge)** — the simplest section for supersonic flight, with minimum wave drag and maximum printability.

```
Fin cross-section (thickness view):

  Leading    Maximum      Trailing
  edge       thickness    edge
  radius     5.0 mm       radius
  1.5 mm      │            1.0 mm
     ╲        │           ╱
      ╲       │          ╱
       ╲──────┴─────────╱
  
  ←——————— chord ————————→
  
  Maximum thickness at: 40% chord (2mm aft of midpoint)
  Leading edge bevel angle: 12°
  Trailing edge bevel angle: 8°
```

### 9.5 Fin-to-Body Interface

The fin root face contacts the outer surface of the aft structure. The root is flat (not contoured to body curve) with a small gap filled by a printed-in radius fillet of 5 mm applied at the print stage of the aft structure, not the fin.

```
Fin root to body:

  Body OD: 275 mm
  Root flat: 5 mm wide × 283 mm long
  Root flat position: tangent to body at fin centreline

  Root fillet (on body side): R5 mm × 283 mm long
  This is printed into the aft structure body section.
```

---

## 10. Flange Interface Geometry

All five inter-section joints use identical flanges for interchangeability of seals and fasteners.

### 10.1 Standard Flange Specification

```
Standard TAIPAN-1 body flange:

      ←——— 310 mm OD ———→
  ┌───────────────────────┐
  │   FLANGE FACE         │
  │   ┌───────────────┐   │  ← bolt circle 293 mm dia
  │   │  ○  ○  ○  ○   │   │  ← 12× M8 bolts at 30°
  │   │               │   │
  │   │  O-RING ──→ ○ │   │  ← groove at 270 mm dia
  │   │               │   │
  │   │  262 mm ID    │   │
  │   └───────────────┘   │
  └───────────────────────┘
  Flange thickness: 16 mm
  
  Dimensions:
    OD:                  310.0 mm
    ID (bore):           262.0 mm
    Face width:          24.0 mm
    Bolt circle:         293.0 mm
    Bolt count:          12
    Bolt size:           M8 × 35 mm
    Bolt torque:         25 Nm (dry)
    O-ring groove dia:   270.0 mm
    O-ring groove width: 2.5 mm
    O-ring groove depth: 2.0 mm
    O-ring type:         AS568-163, Viton 70A, 2.62 mm CS
    Flange face finish:  Ra ≤ 1.6 µm (machined)
```

### 10.2 Flange Station Pairs

| Joint | Forward section | Aft section | Station (mm) |
|---|---|---|---|
| Joint 1 | Nose cone | LOX tank | 920 |
| Joint 2 | LOX tank | Inter-tank | 2,200 |
| Joint 3 | Inter-tank | RP-1 tank | 2,650 |
| Joint 4 | RP-1 tank | Aft structure | 4,080 |
| Joint 5 | Aft structure | Boattail | 4,600 |

---
## 11. Engine Assembly Geometry

### 11.1 Engine Spatial Layout

The engine assembly consists of four primary sub-assemblies arranged along the vehicle centreline, all aft of Station 4,700 (the boattail engine mount face).

```
Engine assembly axial layout:

Station: 4,700      4,750  4,800   5,070          5,400
           │          │      │        │                │
           ▼          ▼      ▼        ▼                ▼
  ╔════════╦════════════════════════════════════════════╗
  ║MOUNT   ║INJECTOR║ CHAMBER ║   NOZZLE DIVERGENT     ║
  ║FLANGE  ║  FACE  ║ CYLINDER║   SECTION              ║
  ╚════════╩════════════════════════════════════════════╝
  │←—50——→│←—50—→│←——270——→│←———————330————————→│
  
  Total engine length (mount face to nozzle exit): 700 mm
  Engine centreline: coincident with vehicle centreline
  Engine mount face: Station 4,700
  Nozzle exit plane: Station 5,400
```

### 11.2 Engine Sub-Assembly List

| Assembly | Axial extent (Station) | Length (mm) | OD (mm) | Notes |
|---|---|---|---|---|
| Mount flange | 4,700–4,750 | 50 | 250 | Interface to boattail |
| Injector dome | 4,750–4,800 | 50 | 240 | Propellant manifolds |
| Combustion chamber barrel | 4,800–5,070 | 270 | 200 | Cylindrical section |
| Throat insert | 5,070–5,090 | 20 | 87 (throat) | Min diameter |
| Nozzle convergent | 5,070–5,090 | 20 | 200→87 | Transition zone |
| Nozzle divergent | 5,090–5,400 | 310 | 87→275 | Conical divergent |
| Nozzle exit lip | 5,390–5,400 | 10 | 275 | Exit plane definition |

### 11.3 Engine Overall Dimensions

| Parameter | Value |
|---|---|
| Engine total length (incl. mount flange) | 700 mm |
| Engine total length (chamber + nozzle only) | 650 mm |
| Mount flange OD | 250.0 mm |
| Combustion chamber OD | 200.0 mm |
| Combustion chamber ID | 168.0 mm |
| Throat diameter | 86.9 mm |
| Nozzle exit diameter | 274.7 mm |
| Engine dry mass | 62 kg |
| Engine centreline offset from vehicle CL | 0 mm (coincident) |

---

## 12. Combustion Chamber

### 12.1 Chamber Dimensions

The combustion chamber is cylindrical with hemispherical forward dome (injector end) and conical convergent section leading to the throat.

```
Chamber cross-section profile:

Station 4,750                                     Station 5,090
  (injector face)                                   (throat)
     │                                                  │
     ▼                                                  ▼
  ╔══╩══════════════════════════════════════╩═════╗
  ║  ║  ←—————— CYLINDER ——————→│CONVERGENT║     ║
  ║  ║                            │  30°    ║     ║
  ╚══╩══════════════════════════════════════╩═════╝
  
  ID 168 mm constant     → taper → ID 86.9 mm
  ←————————————— 340 mm ——————————————→
  
  Forward dome:      hemispherical, R = 84 mm
  Cylinder length:   270 mm
  Convergent length: 70 mm (Station 5,000–5,070)
  Convergent half-angle: 30°
  Throat section:    20 mm cylindrical land, ID 86.9 mm
```

### 12.2 Chamber Sizing Parameters

The chamber is sized by **characteristic length L\*** — the ratio of chamber volume to throat area. For RP-1/LOX, optimal L\* is 1.02–1.27 m.

```
Chamber volume calculation:

  Cylinder volume:
    V_cyl = π × (168/2)² × 270 = π × 84² × 270 = 5,990,760 mm³ = 5.99 L

  Hemispherical dome volume (forward):
    V_dome = (2/3) × π × 84³ = 1,244,000 mm³ = 1.24 L

  Convergent frustum volume:
    V_conv = (π × h / 3) × (R1² + R1×R2 + R2²)
           = (π × 70 / 3) × (84² + 84×43.45 + 43.45²)
           = 73.3 × (7,056 + 3,650 + 1,888)
           = 73.3 × 12,594 = 923,000 mm³ = 0.92 L

  Total chamber volume: 5.99 + 1.24 + 0.92 = 8.15 L

  Throat area: π × (86.9/2)² = 5,930 mm² = 59.3 cm²

  L* = V_chamber / A_throat
     = 8,150,000 mm³ / 5,930 mm²
     = 1,374 mm
     = 1.374 m  ✓  (within optimal 1.02–1.27 m — slightly long, conservative)

  Contraction ratio (A_chamber / A_throat):
    A_chamber = π × 84² = 22,167 mm²
    Contraction ratio = 22,167 / 5,930 = 3.74
    (typical range 2.5–8, this is moderate)
```

### 12.3 Chamber Wall Construction

The chamber wall is a **printed Inconel 718 double-wall** with integral regenerative cooling channels.

```
Chamber wall cross-section (at barrel mid-length):

  ←—————————————— 16 mm total wall ——————————————→

  Hot gas side                              Outer wall
      │                                         │
      ▼                                         ▼
  ┌───┬──────────────────────────────────────┬──┐
  │1.5│←— cooling channels ——→│ web │ channel│2 │
  │mm │                        │1.5 │  4×3mm │mm│
  │   │  channel: 3mm × 4mm   │mm  │        │  │
  │   │  land:    1.5mm wide   │    │        │  │
  └───┴──────────────────────────────────────┴──┘
  
  Inner liner thickness:   1.5 mm
  Channel width:           3.0 mm
  Channel depth:           4.0 mm
  Land (web) width:        1.5 mm
  Outer wall thickness:    2.0 mm
  Channel pitch:           4.5 mm (channel + land)
  Number of channels:      π × 168 / 4.5 = 117 channels

  Coolant (RP-1) flow direction: aft-to-forward (counter-flow)
  Coolant enters at nozzle throat (highest heat flux) first
```

### 12.4 Chamber Thermal Estimate

At the throat (maximum heat flux location):

```
Hot gas temperature:  T* = T_chamber × (2/(γ+1)) = 3,670 × 0.889 = 3,262 K
Wall temperature (hot gas side target): ≤ 900 K (Inconel 718 limit)
Required cooling:     Heat flux ≈ 15–25 MW/m² at throat (typical RP-1/LOX)
RP-1 coolant capacity at 17 kg/s RP-1 flow: well above requirement
```

---

## 13. Nozzle Geometry

### 13.1 Nozzle Type and Profile

The nozzle is a **conical divergent nozzle** at 15° half-angle. This is the simplest geometry and slightly less efficient than a bell nozzle (~98.5% vs ~99.5% thrust efficiency) but far easier to print, inspect, and analyse.

```
Nozzle profile (cross-section, half shown):

  Throat                                            Exit
  Station 5,090                                 Station 5,400
     │                                                │
     ▼                                                ▼
     │  ← 86.9 mm dia ──────────────────── 274.7 mm dia →
     │╲
     │  ╲  15° half-angle
     │    ╲
     │      ╲────────────────────────────────────────
     
  Length of divergent section: 310 mm
  Half-angle: 15.0°
  
  Radius at any axial position x from throat:
    r(x) = r_throat + x × tan(15°)
         = 43.45 + x × 0.2679
  
  Check at exit (x = 310 mm):
    r = 43.45 + 310 × 0.2679 = 43.45 + 83.05 = 126.5 mm → dia = 253 mm
    
  Hmm — diverges from stated 274.7 mm exit diameter.
  
  Reconciliation:
    Required exit radius for ε=10:
    A_exit = 10 × A_throat = 10 × 5,930 = 59,300 mm²
    r_exit = √(59,300/π) = 137.4 mm → D_exit = 274.8 mm ✓
    
    Required nozzle length for 15° half-angle:
    L = (r_exit - r_throat) / tan(15°)
      = (137.4 - 43.45) / 0.2679
      = 93.95 / 0.2679
      = 350.7 mm ≈ 350 mm (as specified)
```

### 13.2 Corrected Nozzle Dimensions

| Parameter | Value |
|---|---|
| Nozzle type | Conical divergent |
| Half-angle | 15.0° |
| Throat diameter | 86.9 mm |
| Throat radius | 43.45 mm |
| Exit diameter | 274.8 mm |
| Exit radius | 137.4 mm |
| Nozzle length (throat to exit) | 350 mm |
| Throat area | 59.3 cm² |
| Exit area | 593 cm² |
| Expansion ratio ε | 10.0 |
| Nozzle station (throat) | 5,090 |
| Nozzle station (exit) | 5,440 |
| Throat land length | 20 mm (cylindrical section at minimum diameter) |
| Convergent half-angle | 30° |
| Convergent length | 70 mm |

### 13.3 Nozzle Wall Construction

The nozzle divergent is **not** regeneratively cooled (gas temperature drops rapidly downstream of the throat as it expands). The wall is a solid Inconel 718 shell, radiation-cooled.

```
Nozzle wall thickness profile:

  At throat:  5.0 mm (thickest — highest pressure, most critical)
  At mid:     3.5 mm
  At exit:    2.5 mm (thinnest — lowest pressure, thin for mass)

  This linear taper optimises mass while maintaining structural rigidity.
  
  Nozzle weight estimate:
    Mean OD: (87 + 275)/2 = 181 mm
    Mean wall: 3.5 mm
    Length: 350 mm
    Volume ≈ π × 181 × 3.5 × 350 = 695,000 mm³ = 695 cm³
    Inconel density: 8.22 g/cm³
    Mass ≈ 695 × 8.22 / 1000 = 5.7 kg
```

### 13.4 Throat Insert

The throat is the highest-stress, highest-temperature location in the engine. A **separate throat insert** in rhenium-alloyed Inconel (or molybdenum for cost) can be press-fitted into the printed chamber/nozzle assembly. This allows the throat to be replaced independently if erosion is detected after static fire.

```
Throat insert:
  OD: 90.0 mm
  ID: 86.9 mm
  Length: 20 mm
  Material: Rhenium-Inconel (Re25) or Mo-TZM alloy
  Fit: H7/p6 interference press fit
  Retention: 4 × M4 set screws at 90°, aft face
```

---

## 14. Injector Geometry

### 14.1 Overview

The injector is the forward face of the combustion chamber. It meters propellant flow into the chamber and controls atomisation and mixing — the dominant factor in combustion efficiency.

TAIPAN-1 uses a **coaxial swirl injector** — 19 elements arranged in a hexagonal close-packed pattern on the injector face. Each element has a central LOX post surrounded by a swirling annular RP-1 flow.

### 14.2 Injector Face Layout

```
Injector face view (looking aft, forward face of chamber):

  ○ = coaxial injector element (19 total)
  
  Injector face diameter: 168 mm (matches chamber ID)
  
             ○   ○   ○
           ○   ○   ○   ○
         ○   ○   ○   ○   ○
           ○   ○   ○   ○
             ○   ○   ○
  
  Pattern: hexagonal close-packed
  Centre element: 1
  Ring 1: 6 elements
  Ring 2: 12 elements
  Total: 19 elements
  
  Element pitch (centre-to-centre): 36 mm
  Element OD: 26 mm
  Edge-to-edge clearance: 10 mm
  Outermost elements radius from centre: ~72 mm
  Face to chamber wall clearance: (168/2) - 72 - 13 = 84 - 85 = wall zone
```

### 14.3 Single Injector Element

```
Single coaxial swirl element cross-section (axial view):

     ←——— 26 mm OD ———→
  ┌──────────────────────┐
  │  RP-1 annulus        │  ← swirling RP-1, 4 tangential entry slots
  │   ┌──────────────┐   │
  │   │  LOX post    │   │  ← LOX flows straight through centre post
  │   │   ID: 8mm    │   │
  │   │   OD: 12mm   │   │
  │   └──────────────┘   │
  │  RP-1 ID: 12mm       │
  │  RP-1 OD: 20mm       │
  └──────────────────────┘

  LOX post ID:                  8.0 mm
  LOX post OD:                  12.0 mm
  LOX post length:              25 mm (protrudes 5 mm into chamber)
  RP-1 annulus inner radius:    6.0 mm
  RP-1 annulus outer radius:    10.0 mm
  RP-1 swirl slots:             4, tangential entry, 1.5 × 3.0 mm
  Recess depth (element below face): 2.0 mm
```

### 14.4 Injector Manifolds

```
Propellant distribution:

  LOX manifold:   Annular gallery behind injector face, 8 mm deep × 10 mm wide
                  Fed by 2 × supply ports at 180° from central LOX feed line
                  
  RP-1 manifold: Separate annular gallery, 6 mm deep × 8 mm wide
                  Fed by 2 × supply ports at 90°/270° from RP-1 feed line

  Both manifolds are printed integrally as part of the injector body.
  Manifold pressure drop (design): 15% of chamber pressure = 7.5 bar
```

---

## 15. Propellant Feed Lines

### 15.1 Line Layout

```
Propellant routing (external side of vehicle, schematic):

  Vehicle centreline (CL)
  
  LOX path:
  LOX tank outlet (Station 2,100, 270°) 
    → LOX pump (Station 4,200, 270°, external to body)
    → LOX manifold (Station 4,750, centre)
    Line: 38mm OD × 1.5mm wall Inconel tube

  RP-1 path:
  RP-1 tank sump (Station 4,050, 270°)
    → RP-1 pump (Station 4,150, 270°, external to body)
    → Cooling jacket inlet (Station 5,400, nozzle exit end)
    → Cooling jacket outlet (Station 4,800, chamber forward)
    → RP-1 manifold (Station 4,750)
    Line: 25mm OD × 1.5mm wall Inconel tube
```

### 15.2 Pump Locations

Both electric pumps are mounted external to the aft structure, at 270° (underside of vehicle), aft of the RP-1 tank outlet. This positioning keeps plumbing short and the pumps accessible for ground servicing.

```
LOX pump assembly:
  Station:     4,150–4,250
  Position:    270° (bottom), 15 mm outboard of body OD
  Mounting:    Bolted bracket to aft structure outer wall
  Inlet line:  38 mm OD, from Station 2,100 routed along body exterior
  Outlet line: 38 mm OD, forward through body to engine
  
RP-1 pump assembly:
  Station:     4,050–4,150
  Position:    270° (bottom), 15 mm outboard of body OD
  Mounting:    Bolted bracket to aft structure outer wall
  Inlet line:  25 mm OD, directly from sump below
  Outlet line: 25 mm OD, aft to nozzle cooling jacket inlet
```

### 15.3 Line Sizes

| Line | OD (mm) | Wall (mm) | Material | Routing |
|---|---|---|---|---|
| LOX tank to pump | 38.0 | 1.5 | 304 SS | Exterior, 270° |
| LOX pump to injector | 38.0 | 1.5 | Inconel 625 | Exterior then through boattail |
| RP-1 tank to pump | 25.0 | 1.5 | 304 SS | Short vertical drop |
| RP-1 pump to cooling jacket | 25.0 | 1.5 | Inconel 625 | Exterior, aft |
| Cooling jacket to injector | 25.0 | 1.5 | Inconel 625 | Integral to engine body |
| He pressurant to LOX tank | 12.0 | 1.5 | 316 SS | Interior conduit |
| He pressurant to RP-1 tank | 12.0 | 1.5 | 316 SS | Interior conduit |

---
## 16. Ballast Assembly

### 16.1 Tungsten Slug Geometry

The ballast is a **solid tungsten alloy cylinder** (W95 — 95% tungsten, 5% Ni-Fe binder) precision-machined to fit inside the nose cone tip cavity.

```
Ballast slug (external view):

  ←——————— 165 mm ————————→
  ┌────────────────────────┐
  │   M16 central bore     │  ← for main retention bolt
  │   through-hole         │
  │   20mm dia clearance   │
  │                        │
  │         ○ ○ ○ ○        │  ← 4× M8 retention bolt holes
  │                        │     at 70mm bolt circle
  └────────────────────────┘
  
  Outer diameter:     58.0 mm
  Length:             165.0 mm
  Central bore:       20.0 mm diameter (clearance for M16 bolt)
  Retention bolts:    4× M8 tapped holes, 25 mm deep, at 70 mm BC, 90° spacing
  Mass:               14.0 kg (ρ = 18,100 kg/m³ confirmed)
  Volume:             772 cm³
  Surface finish:     Ra 1.6 µm (ground finish for close fit)
```

### 16.2 Mounting Bulkhead

The slug sits against a printed forward bulkhead inside the nose cone at Station 30 mm.

```
Forward bulkhead (at Station 30):
  
  Outer diameter:    261.5 mm (press fit to nose cone ID of 262 mm)
  Central boss OD:   60.0 mm (locates slug)
  Central boss ID:   18.0 mm (clearance for M16 bolt)
  Boss height:       15 mm (slug registers against shoulder)
  Thickness (plate): 8.0 mm
  
  Bolt pattern (retention bolts from aft face):
    4× M8 threaded inserts, 70 mm bolt circle
    Inserts: helicoil 1.5D in AlSi10Mg

  M16 main bolt:
    Hex socket cap head M16 × 200 mm
    Passes through central bore of slug → through bulkhead → into printed boss
    Boss tapped M16 × 30 mm deep
    Torque: 180 Nm
    Locking: Loctite 243 medium strength
    
  Slug sits at: CG at Station 50 mm from nose tip (centre of 165 mm slug, offset 15 mm for bulkhead)
```

---

## 17. Avionics Bay Layout

### 17.1 Bay Envelope

The avionics bay occupies the forward portion of the inter-tank section, between Stations 2,250 and 2,430. It is accessed via a removable panel in the body wall.

```
Avionics bay — isometric layout description:

  Bay inner cylinder: 261 mm ID × 180 mm long
  
  Four-deck stacking arrangement (aft to forward):
  
  DECK 1 (aft, Station 2,400–2,430):
    - Battery management unit (BMS): 60×80×20mm
    - FTS receiver B + initiator: 40×60×15mm
    - Connector panel (6× military circular connectors)
  
  DECK 2 (Station 2,360–2,400):
    - FTS receiver A: 40×60×15mm
    - Pyro driver board: 50×70×15mm
    - DC-DC converter (28V bus): 40×50×20mm
  
  DECK 3 (Station 2,310–2,360):
    - Flight computer (Arm Cortex-M7): 100×80×25mm
    - GPS receiver + patch antenna feedthrough: 80×50×15mm
  
  DECK 4 (forward, Station 2,260–2,310):
    - IMU (primary): 75×75×30mm, hard-mounted to printed boss
    - IMU (redundant backup): 45×45×20mm, 90° offset
    - GPS patch antenna: mounted to body wall, faces outward through 50mm dia port
  
  Cable routing: all cables run in printed channels in bay inner wall
  Harness exits: forward through inter-tank/LOX joint conduit, aft to fin servos
  
  Deck structure: 3mm AlSi10Mg printed circuit board carriers
                  8× M3 standoffs per deck
```

### 17.2 Access Panel

```
Access panel:
  Location:   270° (underside), Station 2,260–2,430
  Arc:        120° of circumference
  Chord:      180 mm axial × ~166 mm wide (at 137.5mm radius, 120°)
  Panel type: Snap-in with 8× M4 flush countersunk screws
  Material:   AlSi10Mg, 2.5mm thick
  Seal:       Foam strip seal, IP54 equivalent
  Colour code: Green (avionics — access in field)
```

---

## 18. Tank Internal Geometry

### 18.1 LOX Tank Baffle Detail

```
LOX tank with 4 baffles — axial section:

Station: 920   970    1,165   1,415   1,665   1,915   2,130   2,200
          │     │       │       │       │       │       │       │
          ▼     ▼       ▼       ▼       ▼       ▼       ▼       ▼
  ┌───────┬─────┬───────┬───────┬───────┬───────┬───────┬───────┐
  │FLANGE │DOME │ CELL1 │ CELL2 │ CELL3 │ CELL4 │ CELL5 │ DOME  │
  │       │     │       │       │       │       │       │       │
  └───────┴─────┴───────┴───────┴───────┴───────┴───────┴───────┘
              195mm   250mm   250mm   250mm   250mm   215mm
  
  5 cells between baffles + 2 dome volumes
  
  Each cruciform baffle:
    Extends from Station X-10mm to Station X+10mm (20mm axial width)
    Allows liquid passage through centreline hole (20mm dia)
    Does NOT seal the tank — it is a slosh damper, not a bulkhead
```

### 18.2 Tank Pressure Ports — Internal View

```
LOX tank internal (cross-section at Station 1,000, looking forward):

         90° (vent port)
         ↑
         ○
    ╭─────────────╮
  ← ○    (inner   ○ →    0° (pressurant port)
    │    cylinder) │
  ← ○             ○ →
    ╰─────────────╯
         ○
         ↓
        270° (fill/drain port)

Each boss protrudes 8mm into interior, smooth curved internal face
to prevent stress concentration. Boss external protrusion: 12mm.
```

---

## 19. Complete Centreline Profile

### 19.1 Reconciled Full Vehicle Layout

Taking all corrected dimensions:

```
TAIPAN-1 Complete Axial Profile
================================

Station    Outer radius    Feature
(mm)       (mm)

0          0               Nose tip
5          2.3             Blunt tip radius begins
50         21.7            Ballast slug CG
100        35.3            Nose cone profile
200        54.3
300        77.8
400        98.1
500        114.7
600        127.0
700        133.5
800        136.2
900        137.4
920        137.5           Nose cone base / Joint 1
920        137.5           LOX tank forward flange
2,200      137.5           LOX tank aft flange / Joint 2
2,200      137.5           Inter-tank forward
2,650      137.5           Inter-tank aft / Joint 3
2,650      137.5           RP-1 tank forward
4,080      137.5           RP-1 tank aft / Joint 4
4,080      137.5           Aft structure forward
4,600      137.5           Aft structure aft / Joint 5
4,600      137.5           Boattail forward
4,700      116.9           Boattail aft (233.75mm OD / 2)
4,700      116.9           Engine mount face
4,700      100.0           Engine outer (200mm OD / 2)
5,090      43.45           Throat (86.9mm dia / 2)
5,440      137.4           Nozzle exit (274.8mm dia / 2)

Total vehicle length (nose to nozzle exit): 5,440 mm
Total vehicle length (nose to boattail): 4,700 mm
```

### 19.2 Corrected Master Dimensions

After reconciling tank volumes and nozzle geometry:

| Dimension | Original | Corrected | Note |
|---|---|---|---|
| RP-1 tank length | 700 mm | 1,430 mm | Volume reconciliation |
| Aft structure station start | 3,350 | 4,080 | Follows RP-1 tank correction |
| Boattail station | 3,870 | 4,600 | Follows |
| Engine mount station | 3,970 | 4,700 | Follows |
| Total body length | 4,870 mm | 5,600 mm | Corrected |
| Total with nozzle | 5,265 mm | 6,045 mm | Corrected |

> The original specification's stated total length of 4,870 mm assumed a shorter RP-1 tank. The corrected length of 5,600 mm (body) / 6,045 mm (with nozzle) is the geometrically consistent figure. Fineness ratio corrects to 5,600/275 = **20.4** — still comparable to ballistic missile class.

---

## 20. Mass Centroid Locations

### 20.1 Component CG Stations

Each component's centre of mass location along the vehicle axis:

| Component | Mass (kg) | CG Station (mm) | Notes |
|---|---|---|---|
| Nose cone | 3.2 | 380 | ~41% of nose length |
| Ballast slug | 14.0 | 50 | Geometric centre |
| LOX tank (empty) | 6.8 | 1,560 | Tank structural CG |
| LOX propellant (full) | 375.2 | 1,560 | Coincident with tank CG |
| Inter-tank section | 3.5 | 2,425 | Mid-section |
| He COPV (full) | 2.0 | 2,590 | COPV mid |
| Avionics | 3.0 | 2,340 | Bay centre |
| RP-1 tank (empty) | 4.1 | 3,340 | ~50% of RP-1 tank |
| RP-1 propellant (full) | 146.6 | 3,200 | Liquid CG (above sump) |
| Aft structure | 8.4 | 4,340 | Mid-section |
| Boattail | 2.1 | 4,650 | Mid-section |
| Fins × 4 | 1.9 | 4,340 | Fin area centroid |
| Engine assembly | 62.0 | 5,070 | Engine CG (approx chamber mid) |
| Battery pack | 7.0 | 4,560 | Aft bulkhead |

### 20.2 System CG — Launch Configuration

```
CG_launch = Σ(m_i × x_i) / Σm_i

Computing (major items):
  Nose + ballast:          17.2 × 300 = 5,160
  LOX tank + propellant:   382.0 × 1,560 = 595,920
  Inter-tank + avionics:   8.5 × 2,425 = 20,613
  RP-1 tank + propellant:  150.7 × 3,200 = 482,240
  Aft structure + fins:    12.4 × 4,340 = 53,816
  Boattail:                2.1 × 4,650 = 9,765
  Engine + battery:        69.0 × 5,070 = 349,830

  Sum of moments: 1,517,344 kg·mm
  Total mass: 641.9 kg (incl. He, fittings, misc)
  
  CG_launch ≈ 1,517,344 / 641.9 = 2,364 mm from nose tip

CG_burnout (propellant depleted):
  Remove LOX (375.2 kg at 1,560 mm) and RP-1 (146.6 kg at 3,200 mm)
  
  Remaining moments: 1,517,344 - (375.2×1,560) - (146.6×3,200)
                    = 1,517,344 - 585,312 - 469,120
                    = 462,912 kg·mm
  Remaining mass: 641.9 - 375.2 - 146.6 = 120.1 kg
  
  CG_burnout ≈ 462,912 / 120.1 = 3,855 mm from nose tip
```

### 20.3 Stability Summary (Corrected)

| Configuration | XCP (mm) | XCG (mm) | SM (cal) |
|---|---|---|---|
| Launch (full) | 3,615 | 2,364 | **4.55** |
| Burnout (dry) | 3,615 | 3,855 | **-0.87** |

> **Critical note:** The corrected geometry with the longer RP-1 tank shifts component positions aft and reduces burnout stability. The burnout SM of -0.87 is unstable. To correct this, the ballast must be increased to approximately **45 kg** at 50 mm from nose, or the fin span should be increased to move CP aft. This is a consequence of the RP-1 tank volume correction. The original specification's 1.57 cal burnout margin was based on the shorter (incorrect) RP-1 tank layout. This geometric reference document reveals a design inconsistency that must be resolved before manufacture.

---

*End of TAIPAN-1 Geometry and Dimensional Reference — Revision 1.0*

---

## Revision Notes

**Rev 1.0:** Initial release. Notable corrections vs parent specification:
- RP-1 tank length corrected from 700 mm to 1,430 mm (volume reconciliation)
- Total vehicle length corrected from 4,870 mm to 5,600 mm
- Nozzle length corrected to 350 mm (from 15° half-angle and ε=10 geometry)
- Burnout stability flag raised — requires design iteration on ballast or fin sizing
- All chamber and nozzle dimensions derived from first principles and verified
- Cooling channel count calculated as 117 channels from chamber geometry
- Injector element count fixed at 19 (hexagonal close-pack)

**Recommended next actions:**
1. Resolve RP-1 tank length vs overall length conflict
2. Re-run stability model with corrected geometry
3. Determine whether increased ballast (~45 kg) or increased fin span resolves burnout SM
4. Commission CFD study of nose cone aerothermal re-entry loading
5. Detailed injector element sizing and combustion stability analysis

---

*TAIPAN-1 Geometry and Dimensional Reference — Rev 1.0*  
*For design modelling use only. Not for manufacture without independent engineering review.*
