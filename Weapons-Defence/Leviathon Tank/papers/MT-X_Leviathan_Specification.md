# MT-X Mk.II — "LEVIATHAN"
## Heavy Breakthrough & Amphibious Assault Vehicle
### Complete Technical Specification — Reference Document v1.0

---

> *"If a rural mechanic can't fix it, redesign it."*
> *"If it can't swim, rethink it."*
> *"If it needs software, harden it."*

---

## PART I: DESIGN PHILOSOPHY & OVERVIEW

### 1.1 Concept

The MT-X Mk.II "Leviathan" is a multi-role armoured combat vehicle combining the firepower of a main battle tank, the troop-carrying capacity of an armoured personnel carrier, and the amphibious assault capability of a landing vehicle. It descends philosophically from the T-55 — simple, reliable, field-maintainable — but integrates contemporary materials science, electronics architecture, and weapons technology to produce a platform that competes with and defeats vehicles costing three to four times as much.

The vehicle is designed for nations requiring a capable, affordable, and sustainably maintainable armoured platform that does not depend on a sophisticated industrial base for ongoing support. Every system is designed to be understandable, repairable, and upgradeable in a forward operating environment.

### 1.2 Mission Profiles

| Priority | Mission |
|---|---|
| Primary | Armoured breakthrough and direct fire support |
| Primary | Amphibious beach assault and river crossing |
| Primary | Mechanised infantry delivery under armour |
| Secondary | Convoy escort and urban operations |
| Secondary | Reconnaissance in force |
| Future | Recovery, engineering, command variants (mount points only) |

### 1.3 Design Pillars

- **Simplicity of manufacture** — Standard weld geometry, no exotic casting requirements, common bolt patterns throughout
- **Field maintainability** — Engine change in 4 hours, track replacement in 2 hours, all electronics hot-swappable by module
- **All-hardware electronics** — Zero software architecture, full FPGA-based systems, immune to cyber attack
- **Amphibious by default** — Not an afterthought. Hull sealed from the keel up.
- **Weapons integration** — Three-tier weapons stack covering every threat from infantry to MBT at ranges from 0 to 8,000m
- **Crew survivability** — Crew capsule in hull, engine-forward, blowout panels, isolated from ammo

---

## PART II: HULL ARCHITECTURE

### 2.1 Overall Dimensions

| Parameter | Measurement |
|---|---|
| Hull length (without gun) | 8,500mm |
| Overall length (gun forward) | 11,200mm |
| Hull width (without skirts) | 3,600mm |
| Hull width (with skirts) | 4,100mm |
| Hull height (to turret ring) | 1,700mm |
| Overall height (to turret roof) | 2,380mm |
| Ground clearance | 450mm |
| Track width | 580mm |
| Track contact length | 4,800mm |
| Combat weight | ~38,000kg |

### 2.2 Hull Layout — Forward Engine Configuration

The hull is divided into four longitudinal zones from front to rear:

```
[FRONT]
|  Zone 1  |  Zone 2  |     Zone 3      |  Zone 4  |
| ENGINE   |  CREW    |  TROOP BAY      |   REAR   |
| BLOCK    |  CAPSULE |  (8 PAX)        |   RAMP   |
| 1,800mm  |  1,400mm |    2,800mm      |   500mm  |
[REAR]
```

The engine occupies the full frontal hull width and height, acting as a primary armour layer for the crew capsule immediately behind it.

### 2.3 Hull Geometry & Angles — Complete Specification

All angles are measured from vertical unless stated otherwise.

#### 2.3.1 Front Hull — Engine Deck Zone

| Surface | Angle from Vertical | Physical Thickness | Effective RHA |
|---|---|---|---|
| Upper glacis plate | 78° (12° from horiz.) | 110mm AlNiCyN-5000 | ~528mm |
| Lower glacis plate | 55° (35° from horiz.) | 130mm AlNiCyN-5000 | ~227mm |
| Engine deck top | 5° rearward slope | 60mm AlNiCyN-5000 | — |
| Glacis-to-deck transition | Chamfered radius 80mm | — | — |

The upper glacis at 78° from vertical is the primary ballistic surface. At this angle, a physical plate of 110mm presents an effective thickness of approximately 528mm to a direct frontal shot, exceeding the penetration capability of most current-generation APFSDS rounds before ERA is factored in.

The lower glacis transitions sharply at the hull belly join. The join is a full-penetration butt weld, reinforced with a 40mm internal backing strip. No external fasteners on the glacis face — all joins are internal or flush.

#### 2.3.2 Hull Sides

| Surface | Angle from Vertical | Physical Thickness | Notes |
|---|---|---|---|
| Upper hull side (above track) | 15° outward splay | 80mm AlNiCyN-5000 | ERA panel zone |
| Lower hull side (track zone) | 0° (vertical) | 60mm AlNiCyN-5000 | Protected by skirts |
| Side skirt panels | 15° outward splay | 25mm AlNiCyN-5000 | Bolt-on, quick release |
| Hull-to-deck side join | 45° chamfer | Full weld | Internal fillet weld |

The 15° outward splay on the upper hull side increases effective thickness from 80mm to approximately 83mm while simultaneously deflecting shaped charge jets downward and outward. This geometry also sheds mud and debris naturally.

Side skirts are attached via standardised 12mm bolts on 200mm centres. Any panel removes in under 3 minutes with a standard socket set. Replacement panels are interchangeable across all hull positions.

#### 2.3.3 Hull Rear

| Surface | Angle from Vertical | Physical Thickness | Notes |
|---|---|---|---|
| Upper rear plate | 35° | 60mm AlNiCyN-5000 | Above ramp opening |
| Lower rear plate / ramp | 0° (vertical, when closed) | 60mm AlNiCyN-5000 | Hinged ramp door |
| Rear plate-to-deck join | 25° chamfer | Full weld | |

The rear plate is intentionally the thinnest armoured face. The operational doctrine assumes the rear is never presented to direct fire. The ramp door is armoured to equivalent standard when closed and sealed.

#### 2.3.4 Hull Roof & Belly

| Surface | Angle | Physical Thickness | Notes |
|---|---|---|---|
| Crew capsule roof | 10° forward slope | 50mm AlNiCyN-5000 | Spall liner below |
| Troop bay roof | 8° forward slope | 40mm AlNiCyN-5000 | Spall liner below |
| Engine deck | 5° rearward slope | 60mm AlNiCyN-5000 | Access panels |
| Hull belly (all zones) | Flat | 30mm AlNiCyN-5000 | Sealed for amphibious ops |

The hull belly is flat. Mine protection is provided by the bolt-on EMF/mechanical mine clearing attachment rather than a V-hull, which would compromise amphibious trim. The belly plate is a single continuous sheet along each zone, welded to the lower hull sides with full-penetration welds and internal backing strips.

### 2.4 Hull Construction Method

All primary hull plates are **rolled AlNiCyN-5000** cut to profile and assembled on a standardised jig. Weld joints are designed for single-pass where possible and never require exotic filler materials.

**Join types by location:**

| Join | Type | Notes |
|---|---|---|
| Glacis-to-belly | Full penetration butt weld | Backing strip internal |
| Glacis-to-sides | Full penetration corner weld | External fillet, 12mm radius |
| Side-to-roof | Lap weld + fillet | 15mm fillet, both sides |
| Belly-to-rear | Full penetration butt weld | Backing strip internal |
| All ERA mount points | Threaded insert, cast-in | M20 bolts, 300mm pattern |
| All equipment mount points | Flanged hardpoint, welded | Standard 150×150mm plate |

No casting is required for any primary structural component. The entire hull can be fabricated with a CNC plasma cutter, standard rolling mill, and MIG/TIG welding equipment available at most industrial facilities.

### 2.5 Crew Capsule

The crew capsule is a self-contained armoured cell within the hull, located immediately behind the engine block, separated from both the engine bay (forward) and troop compartment (rearward) by armoured bulkheads.

**Capsule dimensions:**
- Length: 1,400mm
- Width: 2,200mm (full hull interior width)
- Height: 1,500mm (seated operation)

**Crew positions:**
- **Driver** — forward-left, reclined seat, periscope block forward
- **Commander** — centre-right, raised position, access to RWS controls and BMS display
- **Gunner** — centre-left, primary FCS display and main gun controls

All three crew members are seated on **blast-attenuating seats** — energy-absorbing strokes of 150mm, rated to 40G peak impulse. Seats are fixed to the capsule floor structure, not the hull belly, isolating occupants from belly-transmitted impulse loads.

**Capsule entry/exit:**
- Dedicated roof hatch per crew position — independent operation
- All hatches open forward (counterbalanced) to provide frontal cover when dismounted
- Emergency blow-off bolts on all hatches — single lever activation

**Bulkheads:**
- Forward bulkhead (engine bay separation): 30mm AlNiCyN-5000 + fire suppression systems on engine side
- Rear bulkhead (troop bay separation): 25mm AlNiCyN-5000 + acoustic damping layer

### 2.6 Troop Compartment

Located between the crew capsule and the rear ramp. Configured to carry 8 fully equipped troops in combat configuration.

**Compartment dimensions:**
- Length: 2,800mm
- Width: 2,200mm
- Height: 1,600mm (standing clearance for seated troops)

**Seating:**
- 4 seats per side, fold-down bench configuration
- Seats fold flat against the hull walls when not in use (cargo/casualty configuration)
- Each seat: energy-absorbing, 40G rated, 5-point quick-release harness
- Minimum hip-to-hip width per seat: 550mm

**Rifle stowage:**
- 8× MP-6.8 weapon racks, one per seat position
- Positive locking — weapons cannot shift during amphibious ops or rough terrain
- Racks positioned muzzle-up, butt-down, accessible from seated position

**Emergency exits:**
- Primary: rear ramp
- Secondary: roof hatch (1,000×600mm, above centreline of troop bay)
- Tertiary: crew capsule passage through rear bulkhead door (750×550mm)

**Casualty / medevac configuration:**
- All seats fold flat in under 60 seconds
- Two standard NATO stretchers fit in full-length configuration
- Tie-down points at 400mm intervals along both walls

### 2.7 Rear Ramp & Door System

The rear ramp is the primary troop entry and exit point and a critical structural component of the rear hull.

**Ramp specifications:**
- Width: 2,000mm (full clearance for 2-abreast exit)
- Height (opening): 1,600mm
- Plate thickness: 60mm AlNiCyN-5000 (equivalent to rear hull plate)
- Angle when open: rests at 20° below horizontal (acts as exit ramp)
- Operation: hydraulic primary, manual secondary (hand pump)
- Opening time (hydraulic): 8 seconds
- Opening time (manual): 25 seconds
- Sealing: perimeter rubber gasket, compressed by ramp closure, rated to 4m water depth
- Hinge: triple heavy-duty piano hinge, full-width, rated to 3,000kg door weight
- In amphibious configuration: ramp sealed and locked by four over-centre clamps

---

## PART III: ARMOUR PACKAGE

### 3.1 AlNiCyN-5000 Base Armour

The primary structural armour material throughout the vehicle is **AlNiCyN-5000** — a production-ready (TRL 7-8) aluminium-based armour alloy providing rolled homogeneous armour (RHA) equivalent ballistic performance at 61% lower density than steel.

**Material properties:**

| Property | Value |
|---|---|
| Density | 3.05 g/cm³ (vs steel 7.85 g/cm³) |
| Yield Strength | 620 MPa |
| Tensile Strength | 720 MPa |
| Hardness | 380–420 HB |
| Fracture Toughness | 28 MPa√m |
| RHA Equivalency | 1:1 (25mm = 25mm RHA) |
| Spall resistance | Superior to steel (ductile failure mode) |
| Multi-hit capability | Excellent — crack arrest mechanisms |
| Operating temperature | −60°C to +120°C |
| Cost | ~$12,000/metric tonne at scale |

The weight saving achieved by substituting AlNiCyN-5000 for conventional RHA steel is approximately 9–12 tonnes at equivalent protection levels. This saving is partially reinvested into increased plate thickness (Option C — approximately 35% greater than baseline RHA spec) and partially absorbed by the heavier 140mm armament package and bustle autoloader.

### 3.2 Armour Thickness & Effective Protection — Complete Breakdown

#### 3.2.1 Frontal Arc (0° to ±30° azimuth)

| Zone | Physical Thickness | Plate Angle | Effective RHA | + ERA |
|---|---|---|---|---|
| Upper glacis | 110mm | 78° from vertical | ~528mm | +250mm HEAT |
| Lower glacis | 130mm | 55° from vertical | ~227mm | +250mm HEAT |
| Turret front primary face | 200mm | 75° from vertical | ~772mm | +300mm HEAT |
| Turret front secondary face | 180mm | 70° from vertical | ~526mm | +300mm HEAT |
| Gun mantlet (integrated) | 160mm | 65° from vertical | ~379mm | N/A |
| Driver's visor block | 120mm | 0° (vertical) | 120mm | +ERA |

The upper glacis represents the strongest single armoured surface on the vehicle. At 78° from vertical, a round striking the upper glacis must penetrate through an effective thickness of approximately 528mm of AlNiCyN-5000 before reaching internal structure. With ERA panels fitted, the HEAT-equivalent protection approaches 778mm — defeating all current man-portable anti-tank weapons and the majority of helicopter-launched ATGMs.

#### 3.2.2 Side Arc (±30° to ±150° azimuth)

| Zone | Physical Thickness | Plate Angle | Effective RHA | Notes |
|---|---|---|---|---|
| Upper hull side | 80mm | 15° from vertical | ~83mm | + ERA panels |
| Lower hull side | 60mm | 0° (vertical) | 60mm | Protected by skirts |
| Side skirts | 25mm | 15° from vertical | ~26mm | Spaced armour effect |
| Turret side primary | 120mm | 40° from vertical | ~157mm | + ERA |
| Turret side secondary | 100mm | 35° from vertical | ~122mm | + ERA |

Side protection is enhanced primarily through ERA panels on the hull and turret sides. The spaced skirt arrangement provides a stand-off distance of approximately 350mm, ensuring shaped charge jets detonate and dissipate before reaching the primary hull plate.

#### 3.2.3 Rear Arc (±150° to ±180° azimuth)

| Zone | Physical Thickness | Notes |
|---|---|---|
| Upper rear hull | 60mm at 35° | ~74mm effective |
| Lower rear hull / ramp | 60mm at 0° | 60mm effective |
| Turret rear | 60mm at 25° | ~66mm effective |

Rear armour is minimum viable — sufficient against small arms, shell fragments, and blast, not designed for direct APFSDS engagement. Operational doctrine does not expose the rear to direct fire.

#### 3.2.4 Top Attack Protection

| Zone | Physical Thickness | Notes |
|---|---|---|
| Turret roof | 40mm | Top-attack munition consideration |
| Crew capsule roof | 50mm | + spall liner |
| Troop bay roof | 40mm | + spall liner |
| Engine deck | 60mm | Ventilation grilles steel-mesh protected |

Top-attack protection is augmented by the soft-kill EW suite, which provides warning and jamming capability against top-attack missile seekers.

### 3.3 Modular ERA Panel System

Explosive Reactive Armour panels are fitted as standard to all frontal and side surfaces. They are entirely bolt-on — no welding, no specialist tooling, no permanent modification to the base armour.

**ERA panel specifications:**

| Parameter | Value |
|---|---|
| Panel dimensions | 400×400mm (standard) |
| Panel thickness | 60mm |
| Mounting | 4× M20 bolts per panel, standardised 300mm pattern |
| Replacement time | 20 minutes per panel with 2 personnel |
| HEAT defeat | +250–300mm equivalent |
| Fragmentation effect | Minimal — reactive layer contained |
| Temperature rating | −45°C to +75°C |

ERA panels on all frontal surfaces are arranged with a 15mm gap between adjacent panels to prevent sympathetic detonation. The bolt pattern is identical across all positions on the vehicle — any panel fits any mounting point. No left/right/top/bottom orientation — fully interchangeable.

**ERA coverage zones:**
- Upper and lower glacis: full coverage, 6 panels
- Turret front primary and secondary faces: full coverage, 8 panels
- Hull sides above track line: full coverage, 10 panels per side
- Turret sides: partial coverage (non-interference with RWS traverse), 4 panels per side

### 3.4 Spall Liners

All interior surfaces of the crew capsule and troop compartment are lined with **ceramic composite spall liner tiles**, 20mm thick, bonded to the inner hull surface with fire-rated adhesive and mechanically retained by aluminium retaining strips.

The spall liner serves three functions:
1. Catches and absorbs spall and fragments from a penetrating hit
2. Provides thermal insulation — reduces crew compartment temperature significantly
3. Provides limited blast overpressure absorption

Liner tiles are 300×300mm for ease of replacement. Any tile can be removed and replaced in under 5 minutes without removing adjacent tiles.

---

## PART IV: POWERTRAIN

### 4.1 Boxer Engine — MT-X PowerPlant Unit (PPU-1300)

The MT-X is powered by a purpose-designed **12-cylinder horizontally-opposed (boxer) multi-fuel diesel engine** designated PPU-1300.

**Horizontally opposed configuration:**
In a boxer engine, cylinder banks are arranged on opposite sides of the crankshaft, with pistons moving horizontally inward and outward. Each bank's piston movement is directly opposed and counterbalanced by the opposite bank, producing near-complete primary mechanical vibration cancellation at the crankshaft level. This is the engine architecture's fundamental advantage — the mechanical balance is inherent, not achieved through counterweights or balance shafts.

**PPU-1300 specifications:**

| Parameter | Value |
|---|---|
| Configuration | 12-cylinder horizontally opposed, 4-stroke |
| Displacement | 38.4 litres |
| Bore × Stroke | 145mm × 154mm |
| Power output | 1,300hp (970 kW) at 2,200 rpm |
| Torque | 4,800 Nm at 1,400 rpm |
| Power-to-weight (vehicle) | 34.2 hp/tonne |
| Specific power | 33.8 hp/litre |
| Dry weight | 2,800kg |
| Dimensions (L×W×H) | 1,900×1,600×680mm |
| Profile height | 680mm — significantly lower than V-configuration |
| Cooling | Liquid-cooled, cross-flow radiator system |
| Lubrication | Dry sump, external reservoir |
| Starter | Dual — electric primary, compressed air backup |

The 680mm height profile of the boxer layout is a critical advantage in the forward engine configuration — it allows the upper glacis to maintain its extreme slope angle without requiring a tall frontal hull profile. A V12 of equivalent power would typically stand 1,100–1,300mm tall.

### 4.2 Multi-Fuel Capability

The PPU-1300 is designed to operate on any hydrocarbon fuel in the diesel/distillate family without modification, adjustment, or additive:

| Fuel | Performance Retention |
|---|---|
| NATO F-54 (diesel) | 100% (design point) |
| NATO F-34 / JP-8 (jet fuel) | 97% |
| Commercial road diesel | 100% |
| Biodiesel (B20–B100) | 92–100% |
| Synthetic diesel (GTL/BTL) | 98% |
| Heating oil (emergency) | 88% |

Multi-fuel operation is achieved through:
- Wide-tolerance fuel injection system with self-adjusting injection timing
- Cetane-independent ignition management (hardware FPGA-controlled)
- Flexible fuel pump tolerant of varying viscosity
- No fuel-specific software maps — all calibration is hardware-set

In field conditions, the PPU-1300 can draw from any available petroleum source. The fuel system can be purged and switched between fuel types without engine shutdown by operating the cross-connect valve sequence.

### 4.3 Submarine-Style Raft Mounting System

The entire powertrain — engine, transmission, and final drive units — is mounted on an isolated **floating raft**, derived directly from the vibration isolation principles used in submarine machinery spaces.

**Raft construction:**

The powertrain sits on a welded steel subframe (the "raft") which is itself isolated from the hull structure by a two-stage isolation system:

**Stage 1 — Primary isolators (Engine-to-Raft):**
- 24× conical elastomeric mounts, arranged in two rows of 12
- Each mount rated to 2,000kg static load
- Natural frequency: 8–12 Hz
- Attenuation: >25 dB above 50 Hz
- Mount material: Nitrile rubber with steel end plates
- Replacement: individual mounts, no raft removal required

**Stage 2 — Secondary isolators (Raft-to-Hull):**
- 16× wire rope isolators, arranged at structural corners and midpoints
- Natural frequency: 4–6 Hz
- Attenuation: >35 dB above 80 Hz
- Combined with Stage 1: >45 dB total attenuation at firing frequencies

**Flexible connections:**
All connections crossing the raft-hull isolation boundary — fuel lines, oil lines, coolant hoses, electrical conduits, control linkages — are fitted with flexible sections of sufficient length to accommodate raft movement of ±20mm in all axes. No rigid connection bridges the isolation gap.

**Measured benefits:**
- Crew capsule vibration: reduced to <0.3 m/s² RMS at combat speed (tarmac)
- Acoustic hull radiation: reduced by approximately 40 dB vs rigid-mounted equivalent
- Electronics service life: estimated 2–3× improvement (vibration is primary failure mode for solder joints and optical systems)
- Crew fatigue: substantially reduced — 8-hour operations feasible without performance degradation

### 4.4 Transmission

| Parameter | Value |
|---|---|
| Type | Automatic planetary, 6 forward + 2 reverse |
| Steering | Regenerative — differential steer, neutral turn capable |
| Shift control | Electronic selector (FPGA-controlled hardware) |
| Max road speed | 65 km/h |
| Max reverse speed | 35 km/h |
| Neutral turn | Yes — pivot on spot |
| Transmission weight | 1,800kg |
| Oil cooling | Dedicated cooler, thermostatically controlled |
| Change time (field) | Concurrent with engine change — 4 hours combined |

### 4.5 Final Drives & Sprockets

- **Final drives:** 2× planetary reduction units, ratio 5.8:1
- **Drive sprockets:** Front-drive (consistent with Merkava layout), 13-tooth, 650mm pitch diameter
- **Sprocket material:** Hardened steel, induction-hardened tooth faces
- **Sprocket change:** Bolted hub, 16× M24 bolts — field replaceable

### 4.6 Fuel System

| Parameter | Value |
|---|---|
| Internal fuel capacity | 1,400 litres |
| Fuel tank location | Hull sides and floor — armoured integral tanks |
| Operational range | 600km (diesel, road) / 520km (JP-8) |
| External drum tanks | 2× 200L drums, quick-connect rear mount points |
| Total range with drums | ~840km |
| Fuel pump | Twin electric, cross-connected, either serves either tank group |
| Fill points | Left and right hull rear, standardised NATO coupling |
| Self-sealing capability | Tank walls are self-sealing against small-arms penetration |

### 4.7 Cooling System

The boxer layout creates a low-profile engine bay requiring a purpose-designed cooling arrangement:

- **Radiator:** Two side-mounted radiators, one per cylinder bank, exhausting through armoured louvred grilles in the upper hull sides
- **Cooling airflow:** Driven by two variable-speed fans, thermostatically controlled, FPGA-managed
- **Grille armour:** Each louvre is 15mm AlNiCyN-5000, angled at 45° to provide cooling airflow while preventing projectile entry
- **Combat temperature range:** Full power operation at ambient −40°C to +55°C
- **Transmission cooling:** Separate oil-to-water heat exchanger, shared coolant loop

### 4.8 Engine Change Procedure

Target: 4 hours with a crew of 4, basic tools.

The engine bay roof consists of three bolted access panels, total 12× M30 bolts. Removal exposes the complete powertrain from above. The raft assembly is lifted as a single unit on standard recovery vehicle hooks — no disassembly of the raft is required for a routine engine change. All fluid connections are quick-release. Electrical connections are multi-pin MIL-SPEC connectors, colour-coded and keyed.

---

## PART V: SUSPENSION & RUNNING GEAR

### 5.1 Torsion Bar Suspension

The MT-X uses a **longitudinal torsion bar** suspension system — the same fundamental design proven on the T-54/55 series, updated with modern materials and geometry.

**System overview:**
Each road wheel is connected to a trailing arm, which is anchored to a torsion bar running transversely across the hull floor. When the road wheel rises over an obstacle, the trailing arm twists the torsion bar, storing energy elastically and then releasing it — providing the suspension stroke.

**Torsion bar specifications:**

| Parameter | Value |
|---|---|
| Material | 55CrSi spring steel, shot-peened |
| Bar diameter | 65mm |
| Bar length | 2,000mm (full hull width) |
| Maximum deflection | ±28° |
| Road wheel travel | ±280mm (total 560mm stroke) |
| Number of bars | 14 (7 per side) |

**Hydraulic bump stops:**
Each suspension station has a hydraulic bump stop at full compression, preventing metal-to-metal contact and adding progressive damping at the end of stroke. These are self-contained units, bolt-in replaceable in under 20 minutes per station.

**Hydraulic shock absorbers:**
Stations 1, 2 (front), and 6, 7 (rear) have hydraulic rotary dampers — the stations that see the greatest dynamic loads. Stations 3, 4, 5 (mid) are undamped torsion bar only, reducing weight and complexity at lower-stress stations.

### 5.2 Road Wheels

| Parameter | Value |
|---|---|
| Number per side | 7 |
| Diameter | 750mm |
| Width | 190mm |
| Construction | Steel rim, solid rubber tyre bonded |
| Hub | Tapered roller bearings, sealed-for-life |
| Spacing | 680mm centre-to-centre (stations 1–6), 760mm (6–7) |
| Return rollers | 4 per side, 300mm diameter |

Road wheels are dual-tyre configuration (two rubber-tyred discs per hub) — distributes load and maintains mobility if one tyre is damaged.

### 5.3 Drive Sprocket & Idler

- **Drive sprocket:** Front, 13-tooth, 650mm pitch diameter, hardened steel
- **Idler wheel:** Rear, 680mm diameter, adjustable tensioner
- **Track tensioning:** Hydraulic adjuster, operable from driver's position — no external tools required for routine tensioning

### 5.4 Track System

| Parameter | Value |
|---|---|
| Type | Single-pin steel link with rubber pad |
| Track width | 580mm |
| Track pitch | 164mm |
| Links per track | 92 |
| Pad material | Replaceable rubber (road) / bare steel (off-road) |
| Ground pressure | 0.77 kg/cm² (combat load) |
| Track pin material | Hardened steel, 40mm diameter |
| Track weight (per side) | ~1,800kg |
| Change time | 2 hours with crew of 4 |
| Track life | ~5,000km before reconditioning |

Rubber track pads are bolted to each link — 2× M16 bolts per pad. Individual pads replace in under 5 minutes. Bare steel contact links are available for soft ground, mud, and amphibious operations where rubber provides no advantage.

**Track tension indicator:** A simple mechanical gauge on the rear idler adjuster — green/amber/red indicator visible from outside the vehicle. No tools needed to check tension.

---

## PART VI: TURRET

### 6.1 Turret Configuration

The MT-X Mk.II uses an **unmanned remote turret**, operated entirely from the crew capsule in the hull below. No crew are seated in the turret at any time. This provides:

- Crew completely separated from turret penetrations
- Turret can be smaller — no crew ergonomic requirements
- If the turret is destroyed, the crew survive and can potentially withdraw
- Lower overall vehicle height — no crew requirement for head clearance in turret

### 6.2 Turret Geometry & Angles

The turret is a welded AlNiCyN-5000 structure with a **faceted multi-angle front** designed simultaneously for ballistic protection and radar cross section reduction.

#### 6.2.1 Turret Front — Faceted Array

The turret front is not a single surface but a **three-plane faceted array**. No two adjacent faces are parallel. No face is perpendicular to the horizontal. Every surface is angled to deflect both kinetic rounds and radar returns.

| Face | Angle from Vertical | Angle in Azimuth | Physical Thickness | Effective RHA |
|---|---|---|---|---|
| Primary centre face | 75° | 0° (direct front) | 200mm | ~772mm |
| Secondary left cheek | 70° | 25° outward | 180mm | ~526mm |
| Secondary right cheek | 70° | 25° outward | 180mm | ~526mm |
| Transition chamfer (left) | 65° | 12° outward | 150mm | ~355mm |
| Transition chamfer (right) | 65° | 12° outward | 150mm | ~355mm |
| Gun aperture surround | 60° | 0° | 160mm | ~320mm |

The faceted array means there is no single large flat surface to produce a strong radar return. Each face reflects energy in a different direction. The combined frontal protection envelope exceeds 500mm RHA equivalent across the full ±30° frontal arc.

#### 6.2.2 Turret Sides

| Surface | Angle from Vertical | Physical Thickness | Notes |
|---|---|---|---|
| Forward side panel | 45° outward | 120mm | + ERA panels |
| Mid side panel | 35° outward | 120mm | + ERA panels |
| Rear side panel | 25° outward | 100mm | |
| Side-to-roof transition | 55° | 80mm | Continuous sweep, no sharp edge |

The outward splay of the turret sides increases effective thickness and deflects rounds away from the hull roof. The continuous transition from side to roof eliminates the sharp edge that creates a horizontal radar reflector on conventional turrets.

#### 6.2.3 Turret Rear & Roof

| Surface | Angle from Vertical | Physical Thickness | Notes |
|---|---|---|---|
| Rear turret face | 25° | 60mm | Blowout panel zone above |
| Turret roof forward | 10° forward slope | 40mm | Camera/sensor array |
| Turret roof rear (bustle) | 5° rearward slope | 25mm — BLOWOUT | Intentionally weak |
| Bustle blowout panels | 0° (horizontal) | 8mm mild steel | Vent path |

The bustle occupies the turret rear above the blowout zone. The roof panels above the ready ammunition are deliberately thin mild steel — designed to vent upward under the pressure of an ammunition cook-off event, directing the explosion away from the crew capsule below.

#### 6.2.4 Turret Ring

- **Diameter:** 2,200mm internal
- **Material:** Hardened steel ring, 80mm face width
- **Bearing:** Full-circle ball bearing race, sealed
- **Drive:** Electric traverse motor, FPGA-controlled
- **Traverse rate:** 0–45°/second, variable
- **Traverse:** 360° continuous
- **Elevation arc:** −10° to +20° (main gun)
- **Turret ring seal:** Labyrinth seal + rubber wiper — NBC and waterproof rated

### 6.3 Bustle Autoloader

The 140mm AMET round at 45kg total weight and 1,350mm length exceeds the capability of a carousel autoloader. The MT-X uses a **bustle-mounted chain-feed autoloader**.

| Parameter | Value |
|---|---|
| Ready rounds | 22 (bustle magazine) |
| Secondary stowage | 12 rounds (hull — wet stowage) |
| Total ammunition | 34 rounds |
| Loading time | 7.5 seconds (ready round to loaded) |
| Rate of fire | ~7–8 rounds per minute (sustained) |
| Loading system | Chain-feed conveyor, round lifted from horizontal to breech axis |
| Round orientation | Horizontal in magazine, rotated to breech angle during feed |
| Manual backup | Semi-manual loading capability — 2 rpm |
| Loader motor | Redundant dual-motor — either motor drives the system |

**Wet secondary stowage:**
The 12 hull-stowed rounds sit in individual cells filled with water-based fire suppressant gel. If a round is struck by a penetrating fragment, the gel absorbs thermal energy and dramatically reduces the probability of cook-off. Each cell is individually sealed. Rounds are transferred from hull stowage to the bustle by the crew commander using the transfer mechanism during a lull in firing.

**Blowout separation:**
A sliding armoured door separates the bustle ready magazine from the rest of the turret interior when rounds are not being cycled. The door closes automatically within 2 seconds of any magazine pressure event detection.

---

## PART VII: MAIN ARMAMENT

### 7.1 140mm Smoothbore Gun

The primary armament is a **140mm calibre smoothbore cannon**, matched to the 140mm Advanced Multi-Effect Tank Round (AMET).

| Parameter | Value |
|---|---|
| Calibre | 140mm |
| Barrel length | 9,100mm (L/65) |
| Barrel material | Electro-slag remelted steel |
| Bore lining | Chrome, 0.15mm, full length |
| Rifling | None (smoothbore) |
| Muzzle brake | Yes — multi-baffle, 45% recoil force reduction |
| Bore evacuator | Yes — positioned at 60% from breech |
| Thermal sleeve | Full length, composite-fibreglass, reduces thermal bow |
| Breech type | Vertical sliding wedge, semi-automatic |
| Recoil system | Hydro-pneumatic, 520mm stroke |
| Barrel life | 500 rounds (AMET) |
| Barrel change time | 4 hours (field, 4 personnel) |
| Elevation arc | −10° to +20° |
| Stabilisation | Full 2-axis, independent of vehicle pitch/roll |

### 7.2 140mm AMET Round Integration

The 140mm Advanced Multi-Effect Tank Round is the primary munition. Key performance parameters as integrated into this weapon system:

| Parameter | Value |
|---|---|
| Calibre | 140mm |
| Round weight | 45kg |
| Muzzle velocity | 1,950 m/s |
| Muzzle energy | 57 MJ |
| Effective range | 5,000m |
| Maximum range | 8,000m |
| RHA penetration (0m) | ~1,450mm |
| RHA penetration (2,000m) | ~1,150mm |
| Accuracy | <0.2 mil at 2,000m |
| Anti-personnel lethal radius | 50m |
| Anti-personnel casualty radius | 75m |
| Anti-vehicle defeat radius | 25m (light vehicles) |
| Propellant | SCDB (Surface Coated Double Base) |
| Primer | Electric primary / mechanical backup |
| Storage life | 15 years |
| Temperature range | −60°C to +75°C |

**Multi-stage warhead effects:**
1. **Penetrator:** Tungsten-DU alloy matrix, 950mm long, 40mm diameter, L/D 23.75:1. Achieves initial perforation of the target armour.
2. **Stage 1 post-penetration charge:** HMX-based, initiates immediately post-penetration. Generates spall and initial internal overpressure.
3. **Stage 2 internal effect:** PBXN-110 based, pressure wave and fragment dispersion. Destroys internal systems.
4. **Stage 3 terminal:** Aluminium-thermite mixture, extended burn and blast. Area denial and complete internal defeat.

**Pre-formed fragment matrix:**
- 1,500× tungsten cubes (5mm), 2,800 m/s
- 800× heavy cylinders (8mm), 2,600 m/s
- 400× penetrator rods (12mm), 2,400 m/s

### 7.3 Gun-Launched ATGM Capability

The 140mm smoothbore is compatible with gun-launched anti-tank guided missiles fired through the main barrel. This provides a standoff engagement capability beyond the AMET's kinetic range:

- Effective range: up to 8,000m (guided)
- Used against targets beyond APFSDS effective range
- Missile is stored in the bustle alongside AMET rounds (4 missiles in dedicated cells)
- Loading procedure identical to AMET round

---

## PART VIII: SECONDARY ARMAMENT

### 8.1 Coaxial Machine Gun — 6.8×51mm

A belt-fed coaxial machine gun chambered in **6.8×51mm Advanced Combat Round**, mounted to the left of the main gun and slaved to the gunner's FCS.

| Parameter | Value |
|---|---|
| Calibre | 6.8×51mm |
| Muzzle velocity | 1,000 m/s |
| Muzzle energy | 4,000 J |
| Effective range | 600m (point) / 800m (area) |
| Rate of fire | 750–800 rpm |
| Belt capacity | 1,000 rounds ready |
| Reserve ammunition | 3,000 rounds (hull stowage) |
| RHA penetration | 12mm at 300m |
| Barrel | Quick-change, Stellite-lined |
| Barrel change | Tool-less, under 30 seconds |
| Stabilisation | Slaved to main gun 2-axis stabilisation |

The 6.8×51mm calibre gives the coaxial gun genuine anti-materiel capability — it will defeat light armoured vehicles, APCs, and technical vehicles at combat ranges without requiring the main gun. Shared ammunition supply with the 8 embarked troops' MP-6.8 rifles provides a logistics simplification.

**6.8×51mm Round — Key Ballistic Data:**
- Projectile weight: 8.0g (123.5 grains)
- Core: Tungsten carbide penetrator with steel rear
- Jacket: Enhanced copper alloy (CuNi3Si)
- Boat tail: 9°
- BC (G1): 0.515
- Chamber pressure: 62,000 PSI
- Energy retention at 300m: 75%

### 8.2 Commander's Remote Weapon Station — 15.2×115mm APYT

The commander's weapon is a **stabilised remote weapon station (RWS)** chambered in **15.2×115mm APYT**, mounted on the turret roof and operable independently of the main gun.

| Parameter | Value |
|---|---|
| Calibre | 15.2×115mm APYT |
| Action | Semi-automatic |
| RHA penetration | 30mm at 1,000m |
| Accuracy | Sub-MOA at 800m |
| Magazine capacity | 8 rounds (quick-change) |
| Reserve ammunition | 96 rounds (turret stowage) |
| Traverse | 360° independent of turret |
| Elevation | −10° to +60° |
| Stabilisation | Full 2-axis, independent |
| Thermal sight | Yes — integrated with APS threat tracking |
| Slew rate | 0–90°/second |
| RWS weight | ~180kg |

**Dual role — APS Hard Kill:**
The 15.2mm RWS serves simultaneously as the commander's precision anti-materiel weapon and the vehicle's hard-kill Active Protection System. The APS threat radar cues the RWS to incoming missile bearings, and the weapon engages the incoming threat with precision semi-automatic fire before impact. The semi-automatic, high-velocity nature of the 15.2×115mm round makes it effective against the approach speed of most ATGMs.

**Threat engagement envelope:**
- Incoming threat detection range: 400m
- Engagement initiation: 250m
- Minimum engagement range: 80m (geometry dependent)
- Estimated single-shot kill probability on ATGM: >80%

---

## PART IX: ACTIVE PROTECTION SYSTEM

### 9.1 Hard-Kill Layer — 15.2mm RWS Integration

As described above, the commander's 15.2mm RWS is the hard-kill element. The APS threat radar is a dedicated **Ka-band pulse-Doppler radar array**, four panels covering 360° azimuth, mounted on the turret roof corners.

| Parameter | Value |
|---|---|
| Radar type | Ka-band pulse-Doppler |
| Coverage | 360° azimuth, −10° to +70° elevation |
| Detection range | 400m (ATGM), 250m (RPG) |
| Track update rate | 50 Hz |
| False alarm rate | <0.01/hour (FPGA-processed) |
| Reaction time (detect to engage) | <0.3 seconds |
| Simultaneous track capacity | 4 threats |

**FPGA processing:**
All threat detection, tracking, and weapon cueing is performed in dedicated FPGA hardware. There is no software processing loop — the hardware state machine processes radar returns and outputs fire control data with nanosecond-class latency, not the millisecond-class latency of a software system.

### 9.2 Soft-Kill Layer — Electronic Warfare Suite

The soft-kill system operates independently and simultaneously with the hard-kill layer. It degrades, deceives, and defeats threats before they reach engagement range.

**EW suite components:**

| System | Function | Coverage |
|---|---|---|
| Laser warning receiver | Detects laser designators and rangefinders | 360° |
| Radar warning receiver | Detects active radar threats | 360° |
| Missile approach warning | IR-based approach detection | Hemisphere |
| Active IR jammer | Jam IR-guided missile seekers | ±90° azimuth |
| Laser dazzler | Blind or degrade optical guidance systems | ±60° forward |
| Active radar jammer | Disrupt radar-guided threats | 360° |
| Smoke grenade launchers | Multi-spectral obscurant | 12× launchers, 360° |

**Multi-spectral smoke:**
The smoke system dispenses grenades producing obscurant effective in the visual, near-IR, thermal-IR, and millimetre-wave radar bands simultaneously. A vehicle can be rendered effectively invisible across all common guidance spectra within 4 seconds of launch.

**Coordinated response:**
The soft-kill and hard-kill systems share the same threat data bus (hardware). When a laser warning fires, the smoke launches automatically and simultaneously the RWS slews to the threat bearing. When a missile approach is detected, the IR jammer activates, radar jammer activates, smoke launches, and the RWS slews — all simultaneously, all within 0.3 seconds, all without crew input.

---

## PART X: FIRE CONTROL SYSTEM

### 10.1 System Architecture

The fire control system is entirely FPGA-based hardware — no software, no operating system. All ballistic computation, sensor fusion, and display generation is implemented as digital logic in field-programmable gate arrays.

### 10.2 Commander's Sight

| Parameter | Value |
|---|---|
| Type | Panoramic, independent stabilised |
| Thermal channel | 3rd generation cooled MWIR |
| Day channel | HD colour CCD |
| Magnification | ×2 to ×12 continuous zoom |
| Field of view | 4° to 24° (thermal) |
| Stabilisation | 2-axis, independent of vehicle and turret |
| Traverse | 360° continuous |
| Hunter-killer | Yes — commander designates, gunner engages |
| Laser rangefinder | Nd:YAG, eye-safe, 150m–10,000m |
| Display | 800×600 high-brightness OLED, helmet-mountable feed |

### 10.3 Gunner's Sight

| Parameter | Value |
|---|---|
| Type | Fixed forward, 2-axis stabilised |
| Thermal channel | 3rd generation cooled MWIR |
| Day channel | HD colour CCD |
| Magnification | ×3 to ×18 continuous zoom |
| Field of view | 2.5° to 18° |
| Stabilisation | 2-axis, coupled to gun |
| Laser rangefinder | Nd:YAG, 100m–10,000m, range gate capable |
| Display | Dual 1024×768 OLED eyepiece + large format crew display |

### 10.4 Ballistic Computer

The ballistic computer is implemented entirely in FPGA logic — a dedicated ballistics FPGA module in the electronics bay.

**Sensor inputs (all hardware, direct connection):**
- Laser rangefinder range
- Crosswind sensor (ultrasonic anemometer)
- Barrel wear sensor (electromagnetic — measures bore diameter)
- Ammunition temperature sensor
- Vehicle cant sensor (inclinometer, 2-axis)
- Turret/gun angular position encoders
- Target angular rate (derived from tracker FPGA)

**Outputs:**
- Aim point correction (azimuth and elevation offsets)
- Fire control display overlay
- Autoloader trigger signal
- Gun firing signal

**First-round hit probability:** >92% at 2,000m against a stationary target, >80% against a moving target, on the move.

### 10.5 Driver's Vision System

| System | Description |
|---|---|
| Forward periscopes | 3× SAGEM-type fixed periscopes, covering 180° forward |
| Day camera | Wide-angle forward camera, display in capsule |
| Thermal camera | Forward-looking thermal, for night and smoke driving |
| Rear camera | Wide-angle rear coverage — reversing and ramp monitoring |
| Driver's display | 300mm diagonal colour display, tiltable |

The driver has no need to open a hatch under any operational condition. All driving can be performed with full situational awareness from the sealed crew capsule.

---

## PART XI: ELECTRONICS ARCHITECTURE

### 11.1 Design Philosophy — Zero Software

The MT-X Mk.II contains **no software of any kind**. There is no operating system, no firmware, no programmable microcontroller code, no binary executable. Every electronic function in the vehicle is implemented as fixed digital logic in **Field-Programmable Gate Arrays (FPGAs)** or discrete hardware.

This architecture provides:

| Property | Software System | MT-X Hardware System |
|---|---|---|
| Attack surface | Large (remote exploit, code injection) | **Zero (no attack pathway)** |
| EMP resilience | Moderate | **High (FPGAs harden well)** |
| Boot time | 30–120 seconds | **<1 second (logic active on power)** |
| Latency | Milliseconds | **Nanoseconds** |
| Failure modes | Crash, hang, corrupt state | **Hardware fault — predictable, contained** |
| Update method | Software patch (remote risk) | **Physical module swap (requires access)** |
| Reliability | MTBF limited by OS | **MTBF limited by silicon lifetime** |

### 11.2 FPGA Module Architecture

The vehicle electronics are divided into **functional hardware modules**, each a self-contained FPGA-based unit performing one defined role.

| Module | Function | Update frequency |
|---|---|---|
| FCS-1 | Ballistic computation | Rare |
| FCS-2 | Thermal/optical display processing | Rare |
| FCS-3 | Stabilisation control (gun & turret) | Rare |
| APS-1 | Radar threat detection & tracking | Occasional |
| APS-2 | EW/jamming control | Occasional |
| BMS-1 | Battlefield picture processing | Regular |
| BMS-2 | Communications encode/decode | Regular |
| BMS-3 | IFF & transponder logic | Regular |
| ENG-1 | Engine management | Rare |
| ENG-2 | Transmission & drive control | Rare |
| NAV-1 | GPS/INS navigation | Occasional |
| PWR-1 | Power distribution management | Rare |
| DRONE-1 | Drone command & telemetry | Regular |
| NBC-1 | NBC sensor processing & air management | Rare |

### 11.3 Hot-Pluggable Module System

Every module is **hot-pluggable** — it can be removed and replaced while the vehicle is powered without affecting other systems.

**Module connector:**
- 120-pin MIL-SPEC connector, gold-plated
- Physically keyed — each module type has a unique key position, cannot be inserted in wrong slot
- Positive locking — quarter-turn collar locks module in place
- Blind-mate capable — can be inserted without visual alignment

**Module housing:**
- Aluminium alloy, 200×150×40mm standard size
- Labelled in large print: function, revision number, date of manufacture
- Sealed to IP67 — module can be field-swapped in rain
- Integral ESD protection — no damage from handling in dry conditions

**Module self-test:**
On insertion, each module performs a 0.8-second hardware self-test. A green LED on the module face indicates pass. Red indicates fault — pull and replace. Test is entirely internal to the module — no external test equipment required.

**Update/upgrade process:**
"Updating" any system means physically delivering a new module to the vehicle and swapping it in. There is no remote update path. No network connection required. No technician laptop. New module in — old module out — vehicle capability updated. The only way to change the logic of any MT-X system is to be physically present at the vehicle.

### 11.4 Power Architecture

| Parameter | Value |
|---|---|
| Main bus voltage | 28V DC (MIL-STD-1275) |
| Secondary bus | 270V DC (high-power consumers) |
| Main generator | Engine-driven, 30 kW continuous |
| Emergency generator | Dedicated boxer-driven 10 kW unit |
| Battery backup | 4× lithium-iron-phosphate, 24V/100Ah each |
| Battery runtime (essential systems) | 4 hours |
| Power distribution | Solid-state distribution units (no fuses — FPGA-controlled trip) |
| Wiring standard | MIL-W-22759, shielded throughout |

**No software in power management:** The power distribution FPGA (PWR-1) monitors bus voltages and currents in hardware, trips circuits in hardware, and logs fault states to non-volatile hardware registers. A technician reads fault history by looking at the physical register display on the module face — no laptop, no software.

---

## PART XII: BATTLEFIELD MANAGEMENT SYSTEM

### 12.1 Overview

The BMS provides a full networked tactical picture — every MT-X in a formation shares position, heading, status, and target data in real time with every other vehicle and with command elements.

### 12.2 Tactical Display

Each crew member (commander, gunner, driver) has a dedicated display showing:
- Vehicle's own position on digital map (GPS + INS fused)
- All friendly units in formation (Blue Force Tracking)
- Known enemy positions (updated from BMS-1 module)
- Active threat alerts from APS (bearing and type)
- Drone video feed (switchable)
- Ammunition state
- Vehicle health summary (engine temp, fuel, track tension)

Displays are FPGA-generated — the display processing hardware reads sensor data and generates the display image directly in hardware. No graphics processor, no rendering software.

### 12.3 Communications Suite

| System | Specification |
|---|---|
| Primary voice/data | Frequency-hopping VHF/UHF, FPGA-controlled |
| Frequency hopping rate | 300 hops/second (hardware-implemented) |
| Encryption | Hardware AES-256 — dedicated crypto FPGA |
| Datalink | Tactical data broadcast, 1 Mbps, 10km range |
| Antenna | 4× conformal low-profile (flush-mounted) |
| Inter-vehicle latency | <50ms position/status update |
| Jamming resistance | FHSS + DSSS combined (hardware) |
| Backup | HF long-range radio, BMS-2 module |
| Naval coordination | UHF maritime band, built into BMS-2 |

**No software radio:** All frequency synthesis, modulation, demodulation, and protocol handling is implemented in FPGA hardware. The radio cannot be reprogrammed remotely. Frequency plans are loaded by physically swapping the BMS-2 module.

### 12.4 Navigation

| System | Specification |
|---|---|
| GPS | Dual-frequency, military P(Y) code |
| Inertial Navigation | Ring laser gyro, 3-axis |
| Fused accuracy | <5m CEP continuous, <20m GPS-denied |
| Heading accuracy | <0.5 milliradians |
| Velocity accuracy | <0.1 m/s |
| Update rate | 100 Hz |

The INS maintains position through GPS-denied environments (tunnels, urban canyons, EW jamming) by dead reckoning from the ring laser gyro. The hardware fusion of GPS and INS provides continuous accurate position.

### 12.5 IFF — Identification Friend or Foe

- **System:** Hardware transponder/interrogator
- **Mode:** NATO STANAG 4193 compatible
- **Response time:** <1ms (hardware)
- **Code update:** Physical module swap — codes cannot be intercepted from outside the vehicle
- **Integration:** IFF returns displayed as overlays on BMS tactical picture

---

## PART XIII: NBC & AIR SYSTEMS

### 13.1 Overpressure System

The NBC protection system maintains the crew capsule and troop compartment at a positive pressure relative to the external atmosphere, preventing ingress of contaminated air.

| Parameter | Value |
|---|---|
| Overpressure maintained | +5 mbar above external |
| Filter type | Combined HEPA + activated carbon + ASZM-TEDA |
| Flow rate | 360 litres/minute (crew capsule + troop bay combined) |
| Particle filtration | >99.97% at 0.3 micron |
| Chemical agent filtration | HD, GB, VX, CK, AC (all NATO Schedule 1) |
| Biological agent filtration | >99.9999% at 1 micron |
| Filter life | 200 hours in contaminated environment |
| Filter change time | 8 minutes (external access) |

### 13.2 Air Scrubbing — Troop Compartment

The troop compartment has a **dedicated recirculating air scrubber** for extended sealed operations:

- CO₂ scrubber (lithium hydroxide canister) — absorbs expired CO₂
- CO sensor — alarm and auto-vent if engine bay leak detected
- Humidity control — dehumidifier cycle
- Temperature management — electric heating/cooling for troop bay independent of engine heat
- Full recirculation possible for up to 6 hours without external air draw

At 8 troops plus 3 crew, the closed-cycle scrubber system provides 6 hours of sealed operations — sufficient for a beach assault, inland penetration, and troop delivery without unsealing the hull.

### 13.3 CBRN Sensor Suite

- **Chemical detector:** Ion mobility spectrometry, continuous monitoring
- **Biological detector:** Particle counter + assay (30-minute confirmation)
- **Radiological detector:** Geiger-Müller array, dose rate and accumulated dose
- **All sensors:** Feed directly to NBC-1 FPGA module, display on crew BMS
- **Alarm:** Automatic alarm + overpressure increase on chemical or radiological detect

---

## PART XIV: DRONE SYSTEM

### 14.1 Launch System

A **pop-up canister launcher** is mounted on the turret rear, containing 4 canister tubes arranged in a 2×2 array. The canister array hinges rearward and upward from the turret roof when activated, elevating to 45° for drone launch. The array returns flush to the turret roof when not in use.

| Parameter | Value |
|---|---|
| Canister capacity | 4 tubes standard |
| Tube diameter | 120mm (configurable for different drone types) |
| Launch method | Pneumatic ejection, 6-bar |
| Elevation for launch | 45° (folding mount) |
| Stow position | Flush with turret roof |
| Control | DRONE-1 FPGA module, commander's station |

### 14.2 Reconnaissance Drone Configuration (Standard)

Each canister carries one folding-wing reconnaissance drone:

| Parameter | Value |
|---|---|
| Type | Fixed-wing, tube-launched, folding |
| Wing span (deployed) | 800mm |
| Weight | 1.2kg |
| Endurance | 40 minutes |
| Range | 15km from vehicle |
| Payload | Dual thermal/day gimballed camera |
| Datalink | Hardware-encrypted, 5km reliable |
| Speed | 80–120 km/h |
| Recovery | Expendable (belly land) or net recovery on rear hull deck |

Video feed from all active drones is simultaneously displayed on the commander's BMS display and broadcast across the formation BMS network — every vehicle in the formation can see what the drone sees.

### 14.3 Loitering Munition Configuration (Optional Mission Fit)

Canisters can be loaded with **loitering munitions** in place of or alongside reconnaissance drones:

| Parameter | Value |
|---|---|
| Type | Tube-launched loitering munition |
| Warhead | 2.5kg shaped charge |
| Endurance | 30 minutes |
| Guidance | Thermal seeker, hardware-processed |
| Operator | Commander designates from drone video feed |
| Terminal dive angle | 70–90° (top attack profile) |
| Abort capability | Yes — until terminal phase commit |

The loitering munition requires no software — terminal seeker processing is in a dedicated guidance FPGA within the munition itself.

---

## PART XV: AMPHIBIOUS SYSTEMS

### 15.1 Hull Sealing — Standard

The hull is sealed from the keel up as a baseline design requirement. Amphibious capability is not an add-on — it is an inherent property of the hull.

| Seal location | Type | Depth rating |
|---|---|---|
| All hull plate joins | Full-penetration weld | Not applicable |
| Turret ring | Labyrinth + rubber wiper | 4m |
| Crew hatch seals | Compressed rubber, cam-lock | 4m |
| Rear ramp | Perimeter rubber gasket, over-centre clamps | 4m |
| Troop hatch | Compressed rubber | 4m |
| Gun mantlet | Rubber boot + inner seal ring | 2m |
| Coaxial gun aperture | Spring-loaded rubber plug (auto) | 2m |
| Engine air intake | Automated shutoff valve | Activates on water entry |
| Engine exhaust | Submerged exhaust manifold + non-return valve | 4m |
| All electrical penetrations | Epoxy-sealed MIL-SPEC | 4m |

**Bilge pumps:** 2× electric centrifugal pumps, 200 litres/minute each. Manual backup pump in crew capsule. Either pump can handle normal leakage independently; both operating together can cope with significant water ingress.

### 15.2 Standard Flotation — Calm Water

In calm to slight sea conditions (Sea State 1–2, waves up to 0.5m), the MT-X swims without additional equipment.

**Trim vane:** A folding trim vane deploys from the front hull lower edge, deflecting the bow wave and preventing the vehicle nosing under. Deploys in 20 seconds, hydraulic, operable from the driver's station.

**Water propulsion:** Track propulsion in water. The tracks rotating against the water provide a thrust of approximately 15 kN, achieving **6–8 km/h** swimming speed. Steering in water is by differential track speed — same as land steering.

**Freeboard:** At combat weight (~38,000kg) with trim vane deployed, the hull maintains approximately 200mm of freeboard forward, 350mm aft.

### 15.3 Moderate Sea State Package — Sea State 3 (up to 1.25m waves)

A bolt-on stability package extends operational capability to moderate sea conditions:

**Inflatable sponsons:**
- 2× inflatable rubber/nylon sponsons, one per hull side
- Stow flat against hull sides when deflated (add ~40mm to hull width)
- Inflate in under 3 minutes from built-in CO₂/compressed air system
- Each sponson: 3,200×600×400mm when inflated
- Buoyancy added: ~770 litres per side (1,540 litres total — ~1,540kg additional buoyancy)
- Sponson attachment: 12× M16 quick-release pins per side — 15-minute fit/remove
- Deflate and repack time: 20 minutes

**Ballast redistribution blocks:**
- 4× bolt-on steel ballast blocks, 150kg each
- Mount on hull lower sides at waterline level
- Lower centre of gravity by approximately 80mm
- Improve roll stability in beam seas
- Bolt-on, M30 bolts, 10-minute fit per block

**Wave deflector extension:**
- Extends the trim vane horizontally, increasing effective bow wave deflection
- Prevents shipping water over the glacis in head seas
- Fits to trim vane in 5 minutes

**Combined effect of full moderate sea package:**
- Maximum recommended sea state: SS3 (significant wave height 1.25m)
- Roll stability: vessel stable to ±25° continuous, ±35° transient
- Capsize resistance: significantly improved
- Speed reduction in SS3: approximately 2 km/h (4–6 km/h in waves)

### 15.4 Deep Fording — Snorkel

For crossing water obstacles below 4m depth on firm bottom:

- **Snorkel:** Rigid 4m aluminium tube, 300mm diameter, stores on rear hull
- **Fit time:** 15 minutes, 2 personnel
- **Depth capability:** Up to 4m (hull fully submerged)
- **Speed:** 3–5 km/h (track propulsion on bed if depth permits)
- **Vision:** Periscope block for driver, cameras sealed and active
- **Preparation time before entry:** 30 minutes (full sealing and snorkel fit)

### 15.5 Naval Coordination

For amphibious assault operations in coordination with naval vessels:

- **Transponder:** AIS-compatible hardware transponder (BMS-2 module) — landing craft and naval vessels track each MT-X
- **Launch capability:** From LCU, LCAC, LSD well deck — ramp deployment
- **Sea launch depth:** Deployable from 2m water depth off landing craft ramp
- **Formation swimming:** BMS provides GPS position of all swimming vehicles on commander's display
- **Shore approach:** Trim vane stays deployed until tracks ground; vehicle drives directly up beach gradient

---

## PART XVI: MINE CLEARING ATTACHMENT

### 16.1 Overview

The mine clearing attachment is a **bolt-on front assembly** that mounts to standardised hard points on the lower front hull. It does not modify the vehicle permanently and requires no tools beyond a standard socket set.

**Attachment time:** 25 minutes, crew of 4
**Removal time:** 15 minutes, crew of 4
**Storage:** On dedicated logistics vehicle or trailer

### 16.2 Mechanical Flail/Roller System

**Mine roller (primary):**
- 3× roller drums, each 600mm wide, 400mm diameter, total coverage 1,800mm (full vehicle width + 100mm each side)
- Drum material: Hardened steel, 20mm wall
- Drum mounting: Free-rolling on 100mm shaft
- Pressure applied: Vehicle weight transferred through roller arms (~8 tonnes per roller)
- Effective against: Pressure-fuzed anti-tank mines

**Mine flail (secondary — swappable with roller):**
- Powered flail drum, 2,200mm wide
- Drive: PTO from main engine via flexible shaft
- Chain length: 400mm hardened steel chains, 72 per drum
- Rotation: 240 rpm
- Ground penetration: 120mm
- Effective against: All buried mines regardless of fuse type
- Coverage: Full vehicle width + 200mm each side

The roller and flail heads are interchangeable on the same mounting frame — swap in under 20 minutes.

### 16.3 EMF Mine Sweep System

The electromagnetic sweep system generates a pulsed magnetic field ahead of the vehicle, triggering magnetically-fuzed mines at a safe distance:

| Parameter | Value |
|---|---|
| System type | Pulsed electromagnetic coil array |
| Coil arrangement | 3× horizontal coils, total width 2,000mm |
| Peak field strength | 800 A/m at ground level |
| Pulse rate | 20 Hz |
| Safe trigger distance | 3–5m ahead of coil |
| Power draw | 12 kW from main bus |
| Effective against | Magnetic influence mines, magnetic component of combination-fuzed mines |
| Weight | 280kg |

The EMF system and mechanical system operate simultaneously. On a typical minefield:
- EMF system triggers magnetically-fuzed mines 3–5m ahead of the rollers
- Rollers then physically detonate any remaining pressure mines
- Flail (if fitted) breaks up any mines missed by rollers

---

## PART XVII: RADAR SIGNATURE REDUCTION

### 17.1 Geometry Contribution

The primary radar cross section reduction comes from the hull and turret geometry:

**Key principles applied:**

1. **No vertical flat faces:** Every external surface is angled. Vertical flat plates are perfect retroreflectors — they return radar energy directly to the emitter. The MT-X has none.

2. **No 90° dihedral angles:** Corners formed by two surfaces meeting at 90° create a retroreflector. All hull-to-deck and side-to-roof joins are chamfered or radiused.

3. **Faceted turret front:** The multi-plane turret face scatters radar energy in different directions rather than concentrating it back to a single source.

4. **Recessed apertures:** Gun barrel, optics, sensor heads are all either recessed or contoured to minimise the dihedral formed between the barrel/sensor and the hull surface.

**RCS reduction estimate vs conventional tank:** 60–75% reduction in frontal radar cross section compared to a conventional design with vertical sides and flat faces.

### 17.2 RAM Coating

All external surfaces are coated with a **Radar Absorbent Material (RAM)** coating applied over the AlNiCyN-5000 base:

| Parameter | Value |
|---|---|
| Type | Carbon-loaded rubber matrix with ferrite layer |
| Thickness | 3–5mm |
| Coverage | All external surfaces except track and running gear |
| Absorption bandwidth | 8–18 GHz (X and Ku band — most fire control radar frequencies) |
| Weight added | ~180kg (whole vehicle) |
| Application | Spray-applied — field reapplication possible |
| Durability | 3 years before reapplication in normal operational conditions |

### 17.3 Antenna & Sensor Management

All antennas are **conformal low-profile** designs flush-mounted to the hull and turret surfaces:
- No whip antennas (major RCS contributors)
- No protruding sensor heads
- Optics are recessed behind flush covers when not in use
- All cables and conduits internal — nothing external

---

## PART XVIII: VARIANT FUTURE-PROOFING

### 18.1 Hull Hard Points

The following mounting interfaces are built into the hull structure at time of manufacture, whether used or not:

| Location | Hard Point Spec | Intended Use |
|---|---|---|
| Lower front hull (2×) | 600mm flanged plate, 8× M30 bolts | Mine clearing attachment |
| Rear hull upper (2×) | 400mm flanged plate, 6× M24 bolts | Recovery tow bar / crane mount |
| Rear hull lower (2×) | 300mm flanged plate, 4× M24 bolts | Dozer blade / CEV attachment |
| Roof centreline (4×) | 250mm flanged plate, 4× M20 bolts | Mission equipment (drone, APS expansion) |
| Hull sides mid (4× per side) | 200mm flanged plate, 4× M20 bolts | ERA expansion / appliqué armour |

Each hard point has a **power tap (28V DC, 100A)** and a **data tap (MIL-STD-1553 hardware bus)** immediately adjacent, capped when not in use.

### 18.2 Future Variant Roadmap *(Not in current scope — mount points only)*

| Variant | Description | Key Change |
|---|---|---|
| MT-X ARV | Armoured Recovery Vehicle | Crane and winch replacing turret |
| MT-X CEV | Combat Engineering Vehicle | Dozer blade, mine roller, breaching charge launcher |
| MT-X CMD | Command Vehicle | Expanded BMS, communication mast, extra crew stations |
| MT-X CASEVAC | Medical Evacuation | Troop bay reconfigured for 4 stretchers + medic station |
| MT-X ADA | Air Defence | Turret replaced with dual 35mm cannon / SAM launcher |

All variants share the identical hull, engine, running gear, and supply chain. Training, spare parts, and maintenance procedures are 80–90% common across variants.

---

## PART XIX: PERFORMANCE SPECIFICATIONS

### 19.1 Mobility

| Parameter | Value |
|---|---|
| Maximum road speed | 65 km/h |
| Sustained road speed | 55 km/h |
| Cross-country speed | 35–40 km/h |
| Maximum reverse speed | 35 km/h |
| Neutral turn | Yes (pivot in place) |
| Gradient (climb) | 60% (31°) |
| Side slope | 40% (22°) |
| Vertical obstacle | 1.0m |
| Trench crossing | 2.8m |
| Fording depth (unprepared) | 1.4m |
| Fording depth (snorkel) | 4.0m |
| Swimming speed | 6–8 km/h |
| Range (road, diesel) | 600km |
| Range (road, JP-8) | 520km |
| Range with external drums | ~840km |

### 19.2 Weapons Performance Summary

| Weapon | Range | Effect |
|---|---|---|
| 140mm AMET (APFSDS) | 5,000m effective | ~1,150mm RHA at 2,000m |
| 140mm ATGM | 8,000m | Guided precision strike |
| 15.2mm APYT (RWS) | 800m–1,000m | 30mm RHA at 1,000m |
| 6.8×51mm Coax | 600–800m | 12mm RHA at 300m |

### 19.3 Protection Summary

| Threat | Protection |
|---|---|
| 125mm APFSDS (current gen) | Defeated frontally |
| Man-portable HEAT (RPG-7 class) | Defeated frontally and laterally (ERA) |
| ATGM (tandem warhead) | Soft-kill + hard-kill + ERA |
| Artillery fragments | Defeated all aspects |
| Small arms (up to 14.5mm AP) | Defeated all aspects |
| Top-attack munitions | Soft-kill primary, 40mm roof secondary |
| Mine (anti-track) | Mine clearing attachment |
| NBC agents | Overpressure + filtration + sealed hull |
| Cyber attack | Zero attack surface (no software) |
| EMP | FPGA hardware — high resilience |

### 19.4 Weight Budget

| Component | Weight (kg) |
|---|---|
| Hull structure (AlNiCyN-5000) | 8,200 |
| Turret structure | 3,100 |
| Engine (PPU-1300) | 2,800 |
| Transmission & final drives | 3,200 |
| Running gear (suspension, wheels, tracks) | 4,400 |
| Main armament (gun + autoloader) | 2,600 |
| Secondary armament (coax + RWS) | 380 |
| APS & EW suite | 220 |
| Electronics (all modules) | 180 |
| Crew (3 × 100kg equipped) | 300 |
| Troop payload (8 × 120kg equipped) | 960 |
| Fuel (1,400L) | 1,190 |
| Ammunition (34 main, coax, 15.2mm) | 2,100 |
| ERA panels | 640 |
| Miscellaneous (fluids, tools, stores) | 730 |
| **TOTAL COMBAT WEIGHT** | **~38,000kg** |

---

## PART XX: LOGISTICS & MAINTENANCE

### 20.1 Maintenance Philosophy

Every system on the MT-X is designed to be diagnosed and repaired by a qualified vehicle mechanic with a standard tool roll, without specialist equipment, in a field environment.

**No black boxes.** Every module has a visible fault indicator. Every fluid level has a mechanical sight glass. Every wear indicator is visible without disassembly.

### 20.2 Key Maintenance Intervals

| Task | Interval | Time Required | Personnel |
|---|---|---|---|
| Track tension check | Daily | 5 minutes | 1 |
| Fluid levels check | Daily | 10 minutes | 1 |
| Track pad inspection | 500km | 30 minutes | 2 |
| Full running gear inspection | 1,000km | 2 hours | 2 |
| Engine oil change | 250 hours | 45 minutes | 2 |
| Transmission oil change | 500 hours | 60 minutes | 2 |
| Torsion bar inspection | 5,000km | 4 hours | 2 |
| ERA panel replacement | As required | 20 min/panel | 2 |
| Electronics module check | 500 hours | 15 minutes | 1 |
| RAM coating reapplication | 3 years | 8 hours | 4 |

### 20.3 Critical Replacement Times

| Task | Time | Personnel | Tools |
|---|---|---|---|
| Engine change | 4 hours | 4 | Standard socket set + engine hoist |
| Transmission change | 5 hours | 4 | Standard socket set + engine hoist |
| Track replacement (one side) | 2 hours | 4 | Track tool set |
| Electronics module swap | 2 minutes | 1 | None |
| ERA panel replacement | 20 minutes | 2 | M20 socket |
| Barrel change | 4 hours | 4 | Barrel change fixture |
| Road wheel replacement | 30 minutes | 2 | Standard socket set |
| Shock absorber replacement | 45 minutes | 2 | Standard socket set |

### 20.4 Ammunition Resupply

| Ammunition | Storage | Resupply method |
|---|---|---|
| 140mm AMET | 34 rounds onboard | Rear loader vehicle, ramp access |
| 6.8×51mm | 4,000 rounds onboard | Standard ammunition box, crew hatch |
| 15.2×115mm | 104 rounds onboard | 8-round magazine through turret hatch |
| Drone canisters | 4 onboard | Direct canister swap, turret roof |
| Smoke grenades | 12 onboard | Individual tube loading, exterior |

---

## PART XXI: COMPLETE SPECIFICATIONS SUMMARY

```
MT-X Mk.II "LEVIATHAN"
Heavy Breakthrough & Amphibious Assault Vehicle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIMENSIONS
  Hull length:                  8,500mm
  Overall length (gun fwd):     11,200mm
  Hull width (without skirts):  3,600mm
  Hull width (with skirts):     4,100mm
  Hull height (to turret ring): 1,700mm
  Overall height (turret top):  2,380mm
  Ground clearance:             450mm
  Combat weight:                ~38,000kg

CREW & CAPACITY
  Crew:                         3 (commander, gunner, driver)
  Embarked troops:              8
  Crew location:                Armoured hull capsule
  Troop location:               Rear hull compartment

MOBILITY
  Max road speed:               65 km/h
  Max reverse speed:            35 km/h
  Cross-country speed:          35–40 km/h
  Power-to-weight:              34.2 hp/tonne
  Range (diesel):               600km
  Range (JP-8):                 520km
  Range (+ external drums):     ~840km
  Swimming speed:               6–8 km/h
  Gradient:                     60% (31°)
  Trench crossing:              2.8m
  Fording (unprepared):         1.4m
  Fording (snorkel):            4.0m

ENGINE
  Type:                         12-cyl horizontally-opposed (boxer)
  Designation:                  PPU-1300
  Power:                        1,300hp at 2,200rpm
  Torque:                       4,800Nm at 1,400rpm
  Fuels:                        Diesel, JP-8, civilian, biodiesel
  Mounting:                     Submarine raft isolation
  Location:                     Front hull (Merkava layout)

ARMOUR
  Primary material:             AlNiCyN-5000
  Upper glacis:                 110mm / 78° / ~528mm eff. RHA
  Turret front:                 200mm / 75° / ~772mm eff. RHA
  ERA fitted:                   +250–300mm vs HEAT
  Blowout panels:               Turret bustle roof
  Spall liners:                 Crew capsule & troop bay

MAIN ARMAMENT
  Calibre:                      140mm smoothbore
  Round:                        AMET (45kg, 57 MJ)
  Muzzle velocity:              1,950 m/s
  Penetration @ 2,000m:         ~1,150mm RHA
  Effective range:              5,000m
  Ready rounds:                 22 (bustle) + 12 (hull wet)
  Autoloader type:              Bustle chain-feed
  Rate of fire:                 7–8 rpm

SECONDARY ARMAMENT
  Coaxial:                      6.8×51mm belt-fed, 1,000 ready
  Commander's RWS:              15.2×115mm APYT, 104 rounds
  RWS dual role:                APS hard-kill + anti-materiel

ACTIVE PROTECTION
  Hard-kill:                    15.2mm RWS (APS mode)
  Soft-kill:                    Full EW/jamming suite
  Radar:                        Ka-band pulse-Doppler, 360°
  Multi-spectral smoke:         12× launchers, 360°

ELECTRONICS
  Architecture:                 All-FPGA hardware, zero software
  Update method:                Physical hot-plug module swap
  Cyber attack surface:         Zero
  EMP resilience:               High

AMPHIBIOUS
  Standard operation:           Sea State 1–2 (unprepared)
  With stability package:       Sea State 3 (sponsons + ballast)
  Deep fording:                 4m (snorkel)
  Hull seal rating:             4m static depth

MINE CLEARING
  Mechanical:                   Roller or flail (interchangeable)
  Electromagnetic:              Pulsed EMF, 800 A/m, 20 Hz
  Fit time:                     25 minutes

DRONES
  Capacity:                     4 canisters (recon or loitering munition)
  Recon endurance:              40 minutes
  Loitering munition warhead:   2.5kg shaped charge

NBC
  System:                       Overpressure + scrubber
  Filtration:                   HEPA + activated carbon + ASZM-TEDA
  Sealed endurance:             6 hours (crew + 8 troops)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## PART XXII: REFERENCE DOCUMENTS

The following source specifications were used in the development of this vehicle's weapons and materials systems:

| Document | System | Key Contribution |
|---|---|---|
| `140mm_Advanced_Multi-Effect_Tank_Round.md` | Main armament | Round specs, penetration data, multi-stage warhead, barrel specification |
| `Aluminium_Alloys_for_Armour.md` | Armour package | AlNiCyN-5000 material properties, manufacturing, ballistic performance, weight comparison |
| `MP-6_8_Advanced_Combat_Rifle.md` | Coaxial MG | 6.8×51mm round ballistic data, coaxial integration specs, troop weapon standard |
| `15_2mm_Anti-Tank_Sniper_System.md` | Commander's RWS | 15.2×115mm APYT round, RWS specification, APS integration basis |

---

*MT-X Mk.II "Leviathan" — Technical Reference v1.0*
*Document covers: Hull, Armour, Powertrain, Suspension, Turret, Armament, APS, FCS, Electronics, BMS, NBC, Drones, Amphibious, Mine Clearing, Radar Signature, Variants, Performance, Logistics.*

