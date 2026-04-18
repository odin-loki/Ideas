# Complete Fabrication Guide: All Hybrid Component Designs
## Discrete-Continuous Electrical Components (Full Catalog)

---

## Table of Contents

### TIER 1: Standard Equipment (Achievable Today)
1. Quantum Tunnel Resistor
2. Magnetic Domain Inductor
3. Sample-Hold Capacitor/Resistor
4. Memcapacitor
5. Meminductor
6. Brownian Resistor
7. Piezo-Quantum Capacitor
8. Dual-Mode Memristor

### TIER 2: Specialized Equipment (Lab-Proven)
9. Quantum Dot Array Resistor
10. Spin-Resistor (GMR-based)
11. Photo-Capacitor
12. Magnetoelectric Inductor
13. Multi-Level Ladder Capacitor
14. Delta-Sigma Capacitor
15. Programmable Gyrator

### TIER 3: Advanced/Experimental (Cutting Edge)
16. Superconducting Components
17. Josephson Junction Inductor
18. Quantum Hall Resistor
19. Topological Insulator Components
20. Fractal Components (Koch, Sierpiński)

### TIER 4: Conceptual (Future Work)
21. Memtransistor
22. Ternary/Quaternary Logic Components
23. Shannon-Limit Components
24. Möbius Inductor

---

# TIER 1: Standard Equipment Components

## 1. Quantum Tunnel Resistor (QTR)

### Concept
Electrons tunnel through ultra-thin barrier (discrete quantum events) creating continuous macroscopic current with controllable shot noise.

### Physical Structure
```
1. Substrate: Silicon with 300 nm SiO₂
2. Bottom electrode: Al - 200 nm
3. Tunnel barrier: Al₂O₃ - 1.5-3 nm
4. Top electrode: Al - 200 nm
5. Passivation: SiN - 50 nm
```

**Size**: 0805 (2.0mm × 1.25mm)  
**Active area**: 50 μm × 50 μm (tunnel junction)

### Fabrication Process

#### Step 1: Bottom Electrode (Aluminum)
**Method**: Thermal evaporation OR sputtering

**Thermal Evaporation**:
- E-beam evaporate Al
- Pressure: <10⁻⁶ Torr
- Rate: 2-5 Å/s
- Thickness: 200 nm
- **Pattern**: Photolithography + wet etch OR lift-off
  - Photoresist: AZ1518 (positive)
  - Expose, develop
  - Evaporate Al
  - Lift-off in acetone

**Sputtering Alternative**:
- DC sputter Al target
- 200W, 3 mTorr Ar
- 200 nm in 20 minutes

#### Step 2: Tunnel Barrier (Al₂O₃)

**Method A - ALD (Best control)**:
- Trimethylaluminum (TMA) + H₂O
- Temperature: 200°C
- ~1.1 Å per cycle
- **For 2 nm**: 18-20 cycles
- **Critical**: Thickness uniformity is key
  - ±0.2 nm variation acceptable
  - More = too much resistance variation

**Method B - Thermal Oxidation**:
- Expose Al surface to oxygen plasma
- Or: Heat in O₂ atmosphere
- **Advantage**: Self-limiting (Al native oxide)
- **Thickness control**: Time + temperature
  - 100°C in O₂: ~2 nm in 24 hours
  - 200°C in O₂: ~2 nm in 2 hours
- **Disadvantage**: Less precise than ALD

**Method C - Anodization** (Room temperature!):
- Al in ammonium pentaborate solution
- Apply 3-5V DC
- Oxide grows at ~1.4 nm/V
- **For 2 nm**: 1.5V for 1 minute
- **Advantage**: Very cheap, no vacuum
- **Disadvantage**: Rougher interface

#### Step 3: Top Electrode (Aluminum)
- Same as Step 1
- **Pattern smaller** than bottom (40 μm × 40 μm)
- Defines tunnel junction area

#### Step 4: Passivation (SiN)
- PECVD silicon nitride, 300°C
- 50 nm protective layer
- Prevents oxidation of Al

#### Step 5: Contact Pads
- Open via to bottom and top electrodes
- Thick Al pads for probing/bonding
- Standard photolithography

### Testing & Characterization

**I-V Characteristics**:
- Apply -1V to +1V
- **Expect**: Slightly nonlinear tunnel current
  - I ∝ V at low voltage
  - I ∝ V² at higher voltage
- Tunnel current density: 10⁻³ - 10 A/cm² (depending on barrier)

**Shot Noise Measurement**:
- Measure current noise spectral density
- **Formula**: S_I = 2eI (white noise from discrete electrons)
- Requires low-noise current amplifier
- **Discrete events visible** at low currents (< 1 nA)

**Resistance States**:
- Apply voltage stress to modify barrier
- Electromigration can create discrete damage sites
- Results in **discrete resistance jumps**

### Expected Performance

**Tunnel Resistance**: 
- R = (h/e²) × (L/A) × exp(2κL)
- For 2 nm Al₂O₃, 50 μm² area: **~10 kΩ - 1 MΩ**

**Discrete Behavior**:
- Individual electron tunneling events
- Poisson statistics at low bias
- Can count individual electrons at < 1 nA

**Continuous Behavior**:
- Macroscopic I-V appears smooth
- Continuous resistance tuning via voltage stress

### Applications
- Precision current source
- Random number generation (quantum shot noise)
- Single-electron counting
- Ultra-sensitive charge detection

---

## 2. Magnetic Domain Inductor

### Concept
Inductance varies continuously with current, but magnetic domains switch discretely creating discrete inductance states.

### Physical Structure
```
1. Core: Ferrite toroid (NiZn or MnZn) - 3mm OD, 1mm ID
2. Winding: 30 AWG magnet wire - 20 turns
3. Domain control: Embedded CoFeB thin film - 100 nm
4. Bias coil: 10 turns for domain control
5. Encapsulation: Epoxy
```

**Size**: 1206 (3.2mm × 1.6mm × 1.2mm tall)

### Fabrication Process

#### Step 1: Prepare Ferrite Core
**Source**: Commercial NiZn ferrite toroid
- Material: Fair-Rite #43 (NiZn) or #61 (MnZn)
- Size: 3mm OD × 1mm ID × 1mm height
- Permeability: μ_r = 800-1500 (depends on material)

**Clean**:
- Ultrasonic in isopropanol
- Dry thoroughly

#### Step 2: Deposit Magnetic Thin Film

**Method**: Magnetron sputtering

**CoFeB Layer** (on one flat face of toroid):
- Target: Co₄₀Fe₄₀B₂₀ (commercially available)
- DC sputter: 100W
- Ar pressure: 3 mTorr
- Thickness: 100 nm
- **Purpose**: Creates additional magnetic layer with discrete switching

**Alternative - Electroplating**:
- NiFe (permalloy) electroplating
- Easier than sputtering for toroid geometry
- Bath: NiSO₄ + FeSO₄ solution
- Current density: 20 mA/cm²
- Plate 100 nm = ~10 minutes

#### Step 3: Winding

**Main Inductance Winding**:
- 30 AWG enameled copper wire
- **20 turns** through toroid center
- Carefully wound to avoid damaging thin film
- Leave 10mm leads for connections

**Domain Control Winding**:
- 10 turns of 36 AWG wire
- Separate from main winding
- Used to apply bias field for domain control

#### Step 4: Annealing (Optional but recommended)

**Purpose**: Set magnetic easy axis, improve domain structure

**Process**:
- Heat to 300°C in vacuum or inert atmosphere
- Apply magnetic field (1000 Oe) along desired axis
- Hold 1 hour
- Cool in field to room temperature
- **Result**: Oriented magnetic domains

#### Step 5: Encapsulation
- Epoxy potting (clear epoxy)
- Protects winding and thin film
- Provides mechanical support

#### Step 6: Terminations
- Solder main winding to end caps
- Solder bias winding to separate pads
- Mount on PCB or in SMD package

### Testing & Characterization

**L-I Measurement**:
- Apply DC current, measure inductance at AC frequency
- **Expect**: 
  - At low current: L₀ = N²μ₀μ_r A_e / l_e
  - At high current: Core saturates, L drops
  - **Discrete jumps** when domains flip

**Hysteresis Loop**:
- Measure B-H curve
- Apply AC current, measure voltage
- **Expect**: 
  - Continuous smooth loop from ferrite core
  - **Discrete jumps** from CoFeB thin film domains

**Domain Imaging** (if available):
- Magneto-optical Kerr effect (MOKE) microscopy
- Can visualize discrete domain structure

### Expected Performance

**Inductance**:
- Base inductance (no DC bias): L₀ = 1-10 μH (depends on core material and turns)
- With DC bias: L varies continuously as core begins to saturate
- **Discrete jumps**: ±5-20% when thin film domains switch

**Frequency Range**:
- NiZn ferrite: DC - 50 MHz
- MnZn ferrite: DC - 2 MHz

**Discrete States**:
- CoFeB film creates 2-4 discrete domain configurations
- Each has slightly different permeability
- Switchable via bias winding current

**Q Factor**:
- At 1 MHz: Q = 40-80 (typical for small ferrite inductor)

### Applications
- Programmable inductors
- Switchable filters
- Magnetic memory with analog inductance
- Multi-state RF components

---

## 3. Sample-Hold Capacitor

### Concept
Capacitor that samples analog voltage at discrete time intervals (clocked), holds continuous value between samples.

### Physical Structure
```
1. Substrate: FR4 PCB
2. Capacitor: MLCC 0805, 100 nF (standard component)
3. Sampling switch: MOSFET (BSS138)
4. Clock input: Digital control line
5. Buffer: CMOS op-amp (LMC6482)
6. Integration: All SMD on small PCB
```

**Size**: Overall 5mm × 5mm × 2mm (includes active components)

### Fabrication Process

This is a **hybrid active circuit** rather than a single passive component, but functions as a unified element.

#### Step 1: PCB Design
**Software**: KiCad, Eagle, or Altium

**Schematic**:
```
Clock ──┬──[MOSFET Gate]
        │
Input ──┴──[MOSFET Drain-Source]───┬───[100nF Cap to GND]
                                    │
                                    └───[Op-amp Buffer]───► Output
```

**PCB Layout**:
- 2-layer FR4, 1.6mm thick
- Size: 5mm × 5mm
- Components on top layer
- Ground plane on bottom

#### Step 2: Assembly

**Components** (all SMD):
1. **Sampling switch**: BSS138 N-channel MOSFET (SOT-23)
   - R_on = 3.5Ω
   - Switching time: <10 ns
   
2. **Hold capacitor**: 0805 MLCC, 100 nF, X7R
   - Low leakage (<1 nA at 5V)
   
3. **Buffer amplifier**: LMC6482 dual op-amp (SOIC-8)
   - FET input (very high impedance)
   - Low offset voltage (<1 mV)
   
4. **Passives**: 
   - 10 kΩ resistors for biasing (0603)
   - 10 nF bypass caps (0603)

**Assembly**:
- Solder paste stenciling
- Pick-and-place (or hand placement)
- Reflow solder (standard profile)

#### Step 3: Programming/Testing

**No programming needed** - analog circuit

**Testing**:
- Apply sine wave to input (1 kHz, 1V amplitude)
- Apply clock (10 kHz square wave to MOSFET gate)
- **Expect**: Output is staircase approximation of input
  - Samples at 10 kHz rate
  - Holds value between samples

### Expected Performance

**Sample Rate**: DC - 1 MHz (limited by MOSFET switching)

**Hold Time**: 
- Droop rate = I_leakage / C
- With 1 nA leakage, 100 nF cap: 10 μV/ms
- **Practical hold**: >100 ms with <1% error

**Voltage Range**: 0-5V (MOSFET dependent)

**Discrete Behavior**: 
- Samples at clock edges (discrete times)

**Continuous Behavior**:
- Stored voltage is continuous analog value

### Applications
- Analog-to-digital conversion (first stage)
- Track-and-hold circuits
- Peak detection
- Discrete-time signal processing

---

## 4. Memcapacitor

### Concept
Capacitance depends on voltage history - stores both charge (continuous) AND memory of past voltages (discrete states).

### Physical Structure
```
1. Substrate: Silicon with 300 nm SiO₂
2. Bottom electrode: TiN - 50 nm
3. High-k dielectric: HfO₂ - 10 nm
4. Charge trap layer: Si₃N₄ - 20 nm
5. Tunnel oxide: SiO₂ - 3 nm
6. Top electrode: TiN - 50 nm
```

**Size**: 0805 (2.0mm × 1.25mm)  
**Active area**: 1mm × 0.6mm

### Fabrication Process

This is essentially a **SONOS** (Silicon-Oxide-Nitride-Oxide-Semiconductor) flash memory structure used as a capacitor.

#### Step 1: Bottom Electrode (TiN)

**Method**: Reactive sputtering
- Titanium target
- Ar/N₂ atmosphere (80:20)
- DC power: 200W
- Pressure: 5 mTorr
- Thickness: 50 nm
- Pattern: Photolithography + RIE etch

#### Step 2: High-k Dielectric (HfO₂)

**Method**: ALD
- Tetrakis(dimethylamido)hafnium (TDMAH) + H₂O
- Temperature: 250°C
- Growth rate: ~1 Å/cycle
- 100 cycles → 10 nm

**Purpose**: 
- High dielectric constant (ε_r ~ 25)
- Interface between electrode and charge storage

#### Step 3: Charge Trap Layer (Si₃N₄)

**Method**: PECVD OR ALD

**PECVD**:
- SiH₄ + NH₃ + N₂
- Temperature: 300°C
- RF power: 20W
- 20 nm in 5 minutes

**ALD Alternative**:
- Tris(dimethylamino)silane + NH₃ plasma
- 250°C, ~0.8 Å/cycle

**Purpose**: 
- Nitride has deep traps that capture electrons
- **Discrete**: Electron trapping/detrapping
- Creates memory effect

#### Step 4: Tunnel Oxide (SiO₂)

**Method**: ALD OR thermal oxidation

**ALD**:
- Bis(tertiary-butylamino)silane (BTBAS) + O₂ plasma
- 300°C
- 3 nm = ~30 cycles

**Purpose**:
- Thin enough for tunneling
- Thick enough to retain charge
- 3 nm is optimal

#### Step 5: Top Electrode (TiN)
- Same as bottom electrode
- Pattern smaller (0.8mm × 0.5mm)

#### Step 6: Passivation & Contacts
- PECVD SiN protective layer
- Via etching to electrodes
- Aluminum pads for connection

### Testing & Characterization

**C-V Hysteresis**:
- Sweep voltage -5V → +5V → -5V
- Measure capacitance at 100 kHz
- **Expect**: 
  - Clockwise hysteresis loop
  - Memory window: 1-3V shift
  - **Discrete**: Trapped charge in nitride
  - **Continuous**: Capacitance value

**Charge Retention**:
- Program high-C or low-C state
- Monitor capacitance over time
- **Expect**: >10 years retention at room temp

**Endurance**:
- Cycle between states
- **Expect**: >10⁵ cycles before degradation

### Expected Performance

**Capacitance**:
- C_total = C_HfO₂ in series with C_SiO₂
- **Range**: 50-150 nF (for 1mm² area)

**Memory Window**:
- ΔC/C = 10-30% between states

**Programming**:
- Voltage: ±5V for 1 ms
- Charge injection into nitride traps

**Hybrid Behavior**:
- Stores analog charge Q = CV
- C depends on discrete trapped charge state
- History-dependent capacitance

### Applications
- Neuromorphic synapses (analog weights with non-volatility)
- Adaptive filters
- Analog memory
- Self-tuning oscillators

---

## 5. Meminductor

### Concept
Inductance depends on current history - magnetic flux linkage has memory.

### Physical Structure
```
1. Core: Laminated transformer core - 5mm × 3mm
2. Winding: 50 turns of 40 AWG wire
3. Magnetostrictive layer: TbFe₂ (Terfenol-D) - 10 μm
4. Control electrode: Piezoelectric PZT - 100 μm
5. Bias magnets: Small NdFeB magnets
```

**Size**: 1206 (3.2mm × 1.6mm × 2mm tall)

### Fabrication Process

#### Step 1: Prepare Core

**Option A - Laminated Transformer Core**:
- Silicon steel or permalloy laminations
- Stack and glue with insulating varnish
- Size: 5mm × 3mm × 2mm

**Option B - Ferrite Core**:
- Pot core or E-core geometry
- Lower losses at high frequency

#### Step 2: Apply Magnetostrictive Layer

**Material**: Terfenol-D (Tb₀.₃Dy₀.₇Fe₂) or Galfenol (FeGa)

**Method A - Electroplating** (for Galfenol):
- Electroplate Fe-Ga alloy onto core surface
- Sulfate bath with Ga additives
- Thickness: 10 μm
- **Advantage**: Conformal coating

**Method B - Bonding** (for Terfenol-D):
- Thin Terfenol-D foil (commercially available)
- Epoxy bond to core surface
- **Advantage**: Easier, but less conformal

**Purpose**:
- Magnetostriction couples magnetic state to mechanical strain
- Strain creates memory effect in magnetic permeability

#### Step 3: Add Piezoelectric Control

**Material**: PZT thick film OR bulk PZT bonded

**Thick Film**:
- Screen print PZT paste on core
- Sinter at 700°C
- Electrode with silver paste

**Bulk PZT**:
- Thin PZT wafer (100 μm thick)
- Epoxy bond to magnetostrictive layer
- Wire electrodes

**Purpose**:
- Apply voltage to PZT → strain
- Strain modulates magnetostriction
- Changes magnetic permeability → changes inductance

#### Step 4: Winding
- 40 AWG magnet wire
- 50 turns through core
- Careful not to damage magnetostrictive/piezo layers

#### Step 5: Add Bias Magnets
- Small (1mm³) NdFeB magnets
- Position to provide DC bias field
- Sets operating point for magnetostrictive material
- Epoxy in place

#### Step 6: Encapsulation
- Epoxy potting
- Protects all layers
- Provides mechanical support

### Testing & Characterization

**L-I Hysteresis**:
- Apply AC current, measure inductance
- **Expect**: 
  - Hysteresis in L vs I curve
  - Memory of previous current peaks
  - **Discrete**: Domain wall pinning sites
  - **Continuous**: Smooth L(I) within hysteresis envelope

**Piezoelectric Control**:
- Apply DC voltage to PZT
- Measure change in inductance
- **Expect**: ΔL/L = 5-20% per 100V

**Frequency Response**:
- Measure L vs frequency
- **Expect**: Decreases above resonance
  - Resonance from magnetostrictive layer mass
  - Typically 10-100 kHz

### Expected Performance

**Inductance**: 
- L₀ = 10-100 μH (depends on core and turns)

**Memory Effect**:
- Hysteresis from magnetostriction
- Retains "memory" of peak currents
- Decay time: milliseconds to seconds

**Tunability**:
- ΔL/L = ±20% via PZT voltage

**Hybrid Behavior**:
- Continuous inductance and flux linkage
- Discrete magnetic domain states
- History-dependent L(I) relationship

### Applications
- Adaptive filters with memory
- Energy harvesting (remembers vibration patterns)
- Magnetic analog memory
- Self-learning inductors

---

## 6. Brownian Resistor

### Concept
Resistance undergoes continuous Brownian motion (thermal fluctuations) on top of discrete quantized states.

### Physical Structure
```
1. Substrate: Sapphire (for thermal isolation)
2. Heater: Pt serpentine - 100 nm, 50 μm wide
3. Thermistor: VO₂ thin film - 100 nm
4. Thermal isolation: Air gap or aerogel
5. Quantum dots: CdSe/ZnS - 5 nm diameter, sparse array
```

**Size**: 0805 (2.0mm × 1.25mm)

### Fabrication Process

#### Step 1: Heater Element

**Method**: Photolithography + liftoff

**Process**:
- Spin photoresist on sapphire
- Expose serpentine pattern
- Develop
- E-beam evaporate Pt, 100 nm
- Liftoff in acetone
- **Pattern**: Meandering line, 50 μm wide, total resistance 100Ω

#### Step 2: Thermistor Layer (VO₂)

**Method**: Pulsed laser deposition (PLD) OR sputtering

**PLD** (best quality):
- VO₂ target
- Substrate: 400°C during deposition
- O₂ atmosphere: 10 mTorr
- Thickness: 100 nm
- **Critical**: Stoichiometry affects metal-insulator transition temp

**Sputtering Alternative**:
- Vanadium target in O₂/Ar
- Reactive sputtering
- Post-anneal in O₂ to get right stoichiometry

**Purpose**:
- VO₂ has metal-insulator transition at 68°C
- Resistance very sensitive to temperature
- **Near transition**: dR/dT is huge
- Thermal fluctuations → resistance fluctuations

#### Step 3: Quantum Dot Deposition

**Method**: Drop-casting from colloidal solution

**Process**:
- Synthesize CdSe/ZnS core-shell quantum dots
  - OR purchase commercially (Sigma-Aldrich, QD Vision)
- Dilute in toluene (1 mg/mL)
- Drop-cast onto VO₂ surface
- Evaporate solvent slowly
- **Result**: Sparse array of QDs on surface

**Purpose**:
- Quantum dots provide discrete energy levels
- Charge trapping/detrapping creates discrete R states
- Thermal energy drives transitions

#### Step 4: Top Electrodes
- E-beam evaporate Au, 100 nm
- Pattern contact pads
- Leave most of VO₂/QD surface exposed

#### Step 5: Create Thermal Isolation

**Method A - Air Gap**:
- Etch sacrificial layer under thermistor
- Creates suspended structure
- **Advantage**: Good thermal isolation
- **Disadvantage**: Fragile

**Method B - Aerogel**:
- Deposit aerogel layer around device
- **Advantage**: Robust
- **Disadvantage**: Harder to fabricate

**Method C - Vacuum Package**:
- Seal device in vacuum
- Best thermal isolation
- **Disadvantage**: Requires hermetic package

### Testing & Characterization

**Noise Spectral Density**:
- Measure voltage noise vs frequency
- **Expect**:
  - Johnson-Nyquist (white) noise: S_V = 4kTR
  - 1/f noise from charge trapping
  - **Discrete jumps**: Random telegraph noise from QDs

**Temperature Scan**:
- Vary temperature near 68°C
- Measure R(T)
- **Expect**:
  - Sharp transition at T_MIT
  - Hysteresis (discrete states)
  - Fluctuations increase near transition

**Time Series**:
- Record R(t) at high sampling rate
- **Expect**:
  - Continuous Brownian motion
  - Discrete jumps between QD states
  - Switching rates follow Arrhenius law

### Expected Performance

**Resistance**:
- Below MIT: R = 1-10 Ω (metallic VO₂)
- Above MIT: R = 1-10 kΩ (insulating VO₂)
- **At transition**: R fluctuates wildly

**Discrete States**:
- QD charge states: 0, 1, 2... electrons trapped
- Each state has different R
- Thermal activation drives transitions

**Brownian Dynamics**:
- Correlation time: microseconds to milliseconds
- Amplitude: ±1-10% of R

**Temperature Coefficient**:
- At 68°C: dR/dT = -50%/°C (huge!)

### Applications
- True random number generation (quantum + thermal noise)
- Thermometry with discrete levels
- Physical unclonable functions (PUFs)
- Stochastic computing elements

---

## 7. Piezo-Quantum Capacitor

### Concept
Mechanical strain (continuous) couples to quantum charge states (discrete) through piezoelectric effect.

### Physical Structure
```
1. Substrate: Si (100) with 300 nm SiO₂
2. Bottom electrode: Pt - 100 nm
3. Piezoelectric: PZT - 500 nm
4. Quantum well: InGaAs/AlGaAs heterostructure - 50 nm total
5. Top electrode (transparent): ITO - 100 nm
6. Strain sensor: Piezoresistive Si - 50 nm
```

**Size**: 0805 (2.0mm × 1.25mm)

### Fabrication Process

#### Step 1: Bottom Electrode
- Pt deposition (standard, as previous designs)
- Pattern via photolithography

#### Step 2: Piezoelectric Layer (PZT)

**Method**: Sol-gel (easier) OR sputtering

**Sol-gel**:
- PZT precursor (Pb-Zr-Ti acetates in solvent)
- Spin coat at 3000 RPM
- Pyrolyze 350°C
- Repeat 8-10 times for 500 nm total
- Crystallize at 650°C, 30 min

**Purpose**:
- Converts voltage to mechanical strain
- And vice versa
- Coupling coefficient d₃₃ ~ 200 pm/V

#### Step 3: Quantum Well Heterostructure

**Method**: MOCVD (Metal-Organic Chemical Vapor Deposition)

This is the **challenging part** - requires specialized equipment.

**Structure**:
```
GaAs substrate
AlGaAs barrier - 20 nm
InGaAs quantum well - 10 nm
AlGaAs barrier - 20 nm
```

**Growth**:
- Temperature: 600-700°C
- Precursors: TMGa, TMAl, TMIn, AsH₃
- Growth rate: 1-2 μm/hour
- **Critical**: Sharp interfaces, precise composition

**Alternative - Simpler**:
- Use commercial quantum well wafer
- Bond to PZT via wafer bonding
- Grind/etch substrate to thin it

**Purpose**:
- Quantum well confines electrons
- Discrete energy levels
- Strain from PZT shifts energy levels
- Changes electron population → changes capacitance

#### Step 4: Top Electrode (ITO)

**Method**: Sputtering

**Process**:
- RF sputter from ITO target (In₂O₃:SnO₂ 90:10)
- 100W, 5 mTorr Ar
- Substrate: room temperature
- Thickness: 100 nm
- **Advantage**: Transparent, can illuminate QW with light
- **Conductivity**: ~1000 S/cm

#### Step 5: Strain Sensor (Optional)

**Method**: Dope Si with boron (piezoresistive)

**Process**:
- Ion implantation of boron
- Pattern into strain gauge geometry
- Measures mechanical strain directly
- Correlates with quantum state

### Testing & Characterization

**Piezoelectric Response**:
- Apply voltage to PZT
- Measure strain via piezoresistor
- **Expect**: Strain = d₃₃ × E_field
  - For ±10V across 500 nm: ±200 pm displacement

**Quantum Capacitance**:
- Measure C vs voltage at 1 MHz
- **Expect**:
  - C_total = C_geometric + C_quantum
  - C_quantum shows steps when Fermi level crosses discrete QW levels
  - **Discrete**: Energy level crossings
  - **Continuous**: Smooth C(V) between levels

**Strain-Capacitance Coupling**:
- Apply mechanical stress externally (bend substrate)
- Measure capacitance change
- **Expect**: ΔC ∝ strain ∝ stress

**Photocapacitance** (bonus):
- Illuminate with LED
- Photons create electron-hole pairs in QW
- Changes capacitance
- **Discrete**: Photon absorption events

### Expected Performance

**Capacitance**:
- Geometric: C_geo = εA/d ~ 200 nF
- Quantum addition: ΔC_quantum ~ ±10 nF per level crossing

**Discrete States**:
- Quantum well energy levels (4-6 levels typically accessible)
- Separation: 20-50 meV
- Population controlled by strain

**Piezoelectric Coefficient**:
- d₃₃ = 200 pm/V for PZT

**Coupling Strength**:
- ΔE/Δstrain ~ 10 meV per 0.1% strain

### Applications
- Ultra-sensitive strain sensors
- Pressure sensors with quantum readout
- Optomechanical systems
- Quantum electromechanical resonators

---

## 8. Dual-Mode Memristor

### Concept
A memristor that can operate in TWO modes: (1) Discrete memory states like flash, (2) Continuous analog resistance like synaptic weights.

### Physical Structure
```
1. Substrate: Si with 300 nm SiO₂
2. Bottom electrode: TiN - 100 nm
3. Switching layer A: HfO₂ - 5 nm (for digital mode)
4. Switching layer B: TaO_x gradient - 30 nm (for analog mode)
5. Top electrode: Pt - 50 nm
```

**Size**: 0603 (1.6mm × 0.8mm)

### Fabrication Process

#### Step 1: Bottom Electrode (TiN)
- Reactive sputter (Ti + N₂/Ar)
- 100 nm thick
- Pattern via RIE

#### Step 2: Digital Switching Layer (HfO₂)

**Method**: ALD
- TEMAH + H₂O at 250°C
- 5 nm = 50 cycles
- **Purpose**: Binary switching (SET/RESET)
- Filament formation/rupture
- **Discrete**: ON/OFF states

#### Step 3: Analog Switching Layer (TaO_x)

**Method**: Reactive sputtering with **gradient**

**Process**:
- Start: High O₂ flow (50% of Ar)
  - Deposits TaO₂ (more stoichiometric)
- Gradually reduce O₂ flow to 20%
  - Deposits TaO_x (oxygen deficient)
- **Result**: Composition gradient through thickness

**Alternative - Multi-layer**:
- Deposit TaO₂ (5 nm) + TaO_x (5 nm) as distinct layers
- Interface provides gradual transition

**Purpose**:
- Gradual composition change
- **Continuous** resistance tuning
- Many intermediate states

#### Step 4: Top Electrode (Pt)
- Sputter 50 nm Pt
- Pattern smaller than bottom

#### Step 5: Passivation
- ALD Al₂O₃, 10 nm

### Programming Modes

**Mode 1: Digital (Binary)**
- **SET**: +3V, 100 ns pulse
  - Filament forms through HfO₂
  - Low resistance state
  
- **RESET**: -2V, 50 ns pulse
  - Filament ruptures
  - High resistance state
  
- **Result**: R_ON/R_OFF ~ 100-1000

**Mode 2: Analog (Multi-level)**
- **Gradual SET**: +1.5V, variable pulse width
  - Oxygen vacancies migrate in TaO_x
  - Resistance decreases smoothly
  
- **Gradual RESET**: -1.5V, variable pulse width
  - Vacancies migrate back
  - Resistance increases smoothly
  
- **Result**: Continuous R from 1 kΩ to 1 MΩ

**Mode Switching**:
- Voltage amplitude determines which layer dominates
- Low voltage (±1.5V): TaO_x analog mode
- High voltage (±3V): HfO₂ digital mode
- Can use BOTH simultaneously

### Testing & Characterization

**Digital Mode Test**:
- Apply ±3V pulses
- Verify binary switching
- **Expect**: Sharp transition, ON/OFF ratio >100

**Analog Mode Test**:
- Apply series of +1.5V pulses (increasing count)
- Measure R after each pulse
- **Expect**: Smooth R decrease
- **Linearity**: Aim for <5% deviation from linear

**Endurance**:
- Digital: >10⁹ cycles
- Analog: >10⁶ cycles (analog mode wears faster)

**Retention**:
- Both modes: >10 years at 85°C

### Expected Performance

**Resistance Range**:
- Digital ON: 1 kΩ
- Digital OFF: 1 MΩ
- Analog: Continuous 1 kΩ - 1 MΩ

**States**:
- Digital: 2 states (binary)
- Analog: >100 distinguishable levels (7-bit equivalent)

**Switching**:
- Digital: <100 ns
- Analog: 1-10 μs per incremental step

**Hybrid Operation**:
- Can store digital bit (HfO₂ state) 
- AND analog weight (TaO_x state)
- Total information: 1 bit + 7 bits = 8 bits per device

### Applications
- Neuromorphic computing (analog synapses with digital state)
- Multi-bit memory cells
- In-memory computing
- Reconfigurable circuits

---

# TIER 2: Specialized Equipment Components

## 9. Quantum Dot Array Resistor

### Concept
Array of quantum dots with discrete energy levels creates overall continuous conduction with discrete hopping events.

### Physical Structure
```
1. Substrate: Si (100)
2. Barrier: SiO₂ - 5 nm (tunnel barrier)
3. Quantum dots: PbS colloidal QDs - 5 nm diameter
4. Ligand exchange: Thiols (shorten interdot distance)
5. Top barrier: SiO₂ - 5 nm
6. Electrodes: Au - 100 nm (source/drain geometry)
```

**Size**: 0805, channel 10 μm long × 100 μm wide

### Fabrication Process

#### Step 1: Tunnel Barrier

**Method**: ALD SiO₂
- BTBAS + O₂ plasma
- 300°C, 5 nm

#### Step 2: Quantum Dot Synthesis

**Method**: Hot-injection colloidal synthesis

**For PbS QDs**:
- Lead oleate + bis(trimethylsilyl)sulfide
- Inject sulfur precursor into hot (100-150°C) lead oleate
- Growth time: 1-5 minutes controls size
- **5 nm dots**: 2 min at 120°C
- Purify with hexane/ethanol washing

**Alternative**: Purchase commercially
- Sigma-Aldrich, QD Vision sell PbS QDs

#### Step 3: QD Film Deposition

**Method**: Spin-coating with layer-by-layer ligand exchange

**Process**:
1. Spin QD solution (10 mg/mL in octane) at 2000 RPM
2. Treat with ethanedithiol (EDT) solution
   - Replaces long oleic acid ligands with short thiols
   - Brings dots closer (better coupling)
3. Rinse with ethanol
4. Repeat 3-5 times to build film thickness
   - Each layer ~20 nm
   - 3 layers = 60 nm total

#### Step 4: Top Barrier
- Same as bottom: ALD SiO₂, 5 nm

#### Step 5: Source/Drain Electrodes
- E-beam lithography (100 nm features)
- E-beam evaporate Au, 100 nm
- Liftoff
- **Geometry**: 10 μm channel length

### Testing & Characterization

**I-V Characteristics**:
- 2-terminal or 3-terminal (with gate)
- **Expect**: 
  - Nonlinear I-V
  - Coulomb blockade at low voltage (discrete charging)
  - Staircase current at higher voltage

**Temperature Dependence**:
- Cool to 77K (liquid N₂) or 4K (liquid He)
- **Expect**:
  - Discrete Coulomb diamonds in 2D plot (V_ds vs V_gate)
  - Activated transport: I ∝ exp(-E_a/kT)

**Hopping Transport**:
- Measure conductance vs T
- **Expect**: Variable range hopping
  - ln(G) ∝ T^(-1/4) (Mott VRH)

### Expected Performance

**Resistance**: 10 kΩ - 10 MΩ (depending on dot coupling)

**Discrete States**:
- Single-electron charging energy: E_c = e²/2C_dot
- For 5 nm PbS dot: E_c ~ 50 meV
- **Observable up to**: T ~ 600K (exceeds room temp!)

**Continuous Current**:
- Net current is continuous (many dots conducting)
- Individual hops are discrete

### Applications
- Single-electron transistors
- Quantum dot cellular automata
- High-sensitivity electrometers
- Random number generators

---

## 10. Spin-Resistor (GMR-based)

### Concept
Giant magnetoresistance: Resistance depends on discrete magnetic layer alignments (parallel/antiparallel spins) with continuous magnetic field response.

### Physical Structure
```
1. Substrate: Si with SiO₂
2. Seed layer: Ta - 5 nm
3. Pinned FM layer: CoFe - 3 nm
4. Antiferromagnetic: IrMn - 8 nm (pins FM layer)
5. Spacer: Cu - 2 nm (non-magnetic)
6. Free FM layer: NiFe - 4 nm
7. Cap: Ta - 5 nm
```

**Size**: 0805 (2.0mm × 1.25mm)  
**Active sensor**: 20 μm × 5 μm strip

### Fabrication Process

This is a **standard GMR spin valve** - technology from hard drive read heads.

#### Step 1: Full Stack Deposition

**Method**: DC magnetron sputtering (no breaking vacuum!)

**Process** (all in one pump-down):
1. Ta (5 nm): 50W, 3 mTorr Ar
2. CoFe (3 nm): 50W, 3 mTorr Ar
3. IrMn (8 nm): 50W, 3 mTorr Ar
4. Cu (2 nm): 30W, 3 mTorr Ar, **very slow** (critical thickness)
5. NiFe (Py, 4 nm): 50W, 3 mTorr Ar
6. Ta (5 nm): 50W, 3 mTorr Ar

**Critical**:
- No vacuum break (prevents oxidation)
- Cu thickness precision ±0.2 nm (affects GMR ratio)
- Cleanliness (particles kill GMR)

#### Step 2: Annealing to Pin Layer

**Purpose**: Set exchange bias (pin CoFe layer)

**Process**:
- Heat to 250°C in vacuum
- Apply magnetic field (5000 Oe) in plane
- Hold 2 hours
- Cool in field to room temperature
- **Result**: IrMn "pins" CoFe magnetization direction

#### Step 3: Patterning

**Method**: Ion beam etching OR reactive ion etch

**Process**:
- Photolithography to define sensor strip
- Ar ion mill through all layers
- **Pattern**: 20 μm wide × 5 μm long strip
- Stop on substrate

#### Step 4: Contacts & Passivation
- Au contacts at ends of strip
- SiN passivation over sensor

### Testing & Characterization

**R-H Curve** (Resistance vs Magnetic Field):
- Apply in-plane magnetic field, measure resistance
- **Expect**:
  - At H=0: Higher R (layers antiparallel)
  - At H>H_sat: Lower R (layers parallel)
  - **GMR ratio**: ΔR/R = 5-20%

**Discrete Behavior**:
- Two states: parallel (low R), antiparallel (high R)
- Switching field: ~10-50 Oe for NiFe free layer

**Continuous Behavior**:
- Smooth R(H) during switching
- Analog response to field strength

### Expected Performance

**Resistance**: 
- Parallel: 100 Ω
- Antiparallel: 120 Ω
- GMR ratio: 20%

**Sensitivity**:
- dR/dH ~ 0.5 Ω/Oe near switching field

**Speed**: 
- Switching time ~1 ns (limited by spin precession)

**Temperature**:
- Operable -40°C to +150°C

### Applications
- Magnetic sensors (position, current, field)
- Magnetic memory read heads
- Programmable resistors (set by magnetic field)
- Spin logic devices

---

## 11. Photo-Capacitor

### Concept
Light absorption (discrete photons) modulates capacitance through photogenerated carriers (continuous charge).

### Physical Structure
```
1. Substrate: Glass
2. Bottom electrode: ITO - 150 nm
3. Photoactive layer: P3HT:PCBM blend - 200 nm
4. Blocking layer: LiF - 1 nm
5. Top electrode: Al - 100 nm
```

**Size**: 1206 (3.2mm × 1.6mm)

### Fabrication Process

This is essentially an **organic photovoltaic (OPV)** cell used as a capacitor.

#### Step 1: ITO Substrate
- Purchase ITO-coated glass (commercial)
- Clean: Acetone → IsoP → DI → UV-ozone
- Pattern (optional): Etch ITO with HCl

#### Step 2: Photoactive Layer

**Material**: P3HT:PCBM (standard OPV blend)
- P3HT: poly(3-hexylthiophene) - electron donor
- PCBM: [6,6]-phenyl-C61-butyric acid methyl ester - electron acceptor
- **Mix**: 1:1 weight ratio in chlorobenzene (20 mg/mL total)

**Deposition**: Spin coating
- Filter solution (0.45 μm PTFE)
- Spin at 1000 RPM, 60 seconds
- Thickness: ~200 nm
- **Anneal**: 150°C, 10 minutes in N₂ glovebox
  - Improves crystallinity and phase separation

#### Step 3: Blocking Layer (LiF)

**Method**: Thermal evaporation
- Pressure: <10⁻⁶ Torr
- LiF source: Tungsten boat
- Rate: 0.1 Å/s
- Thickness: 1 nm
- **Purpose**: Blocks hole injection, confines charge

#### Step 4: Top Electrode (Al)
- Thermal evaporation
- Thickness: 100 nm
- Shadow mask for patterning

### Testing & Characterization

**Dark Capacitance**:
- Measure C-V in dark
- **Expect**: Geometric capacitance
  - C = εA/d ~ 150 nF

**Photocapacitance**:
- Illuminate with LED (520 nm, green light)
- Measure capacitance vs light intensity
- **Expect**:
  - Capacitance increases with light
  - ΔC/C ~ 10-50% at 100 mW/cm²
  
**Mechanism**:
- Photons absorbed → excitons → separated charges
- Extra charges in photoactive layer increase dielectric constant
- **Discrete**: Photon absorption events
- **Continuous**: Charge accumulation

**Time Response**:
- Turn light on/off, measure C(t)
- **Expect**:
  - Rise time: ~microseconds (charge generation)
  - Fall time: ~milliseconds (recombination)

### Expected Performance

**Capacitance**:
- Dark: 150 nF
- Illuminated (100 mW/cm²): 200 nF

**Spectral Response**:
- Peak: 520 nm (P3HT absorption)
- Range: 400-650 nm

**Quantum Efficiency**:
- ~30% (photons → separated charges)

### Applications
- Light sensors with capacitive readout
- Optically tunable capacitors
- Optical memory (light writes, C stores)
- Energy harvesting capacitors

---

## 12. Magnetoelectric Inductor

### Concept
Electric field controls discrete magnetic states, which determines continuous inductance.

### Physical Structure
```
1. Core: Ferrite (NiZn) toroid - 3mm OD
2. ME layer: BTO/CFO (BaTiO₃/CoFe₂O₄) composite - 100 μm
3. Electrodes on ME layer: Au - 200 nm
4. Winding: 25 turns, 32 AWG
5. Control leads: To ME electrodes
```

**Size**: 1206 (3.2mm × 1.6mm × 1.5mm tall)

### Fabrication Process

#### Step 1: Ferrite Toroid
- Commercial NiZn ferrite toroid
- Size: 3mm OD × 1mm ID

#### Step 2: Magnetoelectric Composite

**Method A - Tape Casting** (Easier):

**BaTiO₃ Tape**:
- BaTiO₃ powder + binder + solvent
- Tape cast to 50 μm thick
- Cut to fit toroid

**CoFe₂O₄ Tape**:
- CoFe₂O₄ powder + binder + solvent
- Tape cast to 50 μm thick
- Cut to fit toroid

**Laminate**:
- Stack: BTO / CFO / BTO
- Press at 70°C, 10 MPa
- Co-sinter at 1100°C, 2 hours
- **Result**: Composite magnetoelectric material

**Method B - Sintering** (Better properties):
- Mix BaTiO₃ and CoFe₂O₄ powders (50:50 vol%)
- Ball mill with binder
- Press into pellet shape
- Sinter at 1150°C
- Polish to 100 μm thick
- Attach to toroid with epoxy

#### Step 3: Electrodes on ME Layer
- Sputter Au on top/bottom of ME composite
- 200 nm thick
- Wire leads for voltage application

#### Step 4: Winding
- 32 AWG magnet wire
- 25 turns through toroid
- Leave leads for connection

### Testing & Characterization

**L vs E-field**:
- Apply DC voltage to ME electrodes (creates E-field)
- Measure inductance at 1 MHz
- **Expect**:
  - ΔL/L ~ 1-5% per kV/cm
  
**Mechanism**:
- E-field → strain in BaTiO₃ (piezoelectric)
- Strain → stress in CoFe₂O₄ (magnetostrictive)
- Stress → change magnetization → change permeability → change L

**Hysteresis**:
- E-field sweep shows hysteresis
- **Discrete**: Ferroelectric domain switching in BTO
- **Continuous**: Smooth L(E) response

### Expected Performance

**Inductance**: L₀ = 10 μH (no E-field)

**Tunability**: ΔL/L = 5% at 10 kV/cm

**Voltage**: ±300V across 100 μm → 30 kV/cm E-field

**Frequency**: DC - 10 MHz

### Applications
- Voltage-controlled filters
- Tunable oscillators
- Electric-field-programmable inductors
- E-field sensors

---

## 13. Multi-Level Ladder Capacitor

### Concept
Multiple capacitors switched in/out discretely, with continuous voltage tuning of each.

### Physical Structure
```
1. Substrate: FR4 PCB
2. Capacitor array: 8× varactor diodes (BB135)
3. Switches: 8× MOSFET analog switches
4. Control: 3-bit decoder + driver
5. Layout: Ladder network
```

**Size**: 10mm × 10mm PCB module

### Fabrication Process

This is a **circuit implementation** rather than single passive component.

#### Step 1: PCB Design

**Schematic**:
```
       C1──[SW1]──┐
       C2──[SW2]──┤
       C4──[SW4]──┼── Output
       C8──[SW8]──┤
       ...        │
       GND ───────┘
       
Where: C_n = n × base_capacitance
       SW = MOSFET switch controlled by binary decoder
```

**Components**:
- 8× varactor diodes (BB135): Voltage-variable capacitors
  - C_min = 1 pF, C_max = 30 pF
  - Varies with reverse bias (0-20V)
  
- 8× MOSFET switches (2N7002)
  - Low R_on (~2Ω)
  - Controlled by 3-to-8 decoder
  
- 1× 3-to-8 decoder (74HC138)
  - 3 digital inputs select 1 of 8 outputs

#### Step 2: PCB Fabrication
- Standard 2-layer FR4 process
- 10mm × 10mm
- Solder mask, silkscreen

#### Step 3: Assembly
- SMD pick-and-place
- Reflow solder

### Operation

**Discrete State Selection**:
- 3-bit digital input (000 to 111)
- Selects which capacitors are connected
- **8 discrete states**: Different C combinations

**Continuous Tuning**:
- Apply voltage to varactor diodes
- Each capacitor varies continuously
- **Combined**: Discrete + continuous

### Expected Performance

**Capacitance Range**:
- Minimum: 1 pF (only C₁, at max bias)
- Maximum: 240 pF (all 8, at zero bias)
- **Discrete steps**: 8 major states
- **Continuous**: ±30% around each discrete state

**Resolution**:
- 3-bit discrete + ~5-bit continuous = **8-bit equivalent**

### Applications
- Programmable filters
- Adaptive impedance matching
- Voltage-controlled oscillators
- Multi-level analog memory

---

# TIER 3: Advanced/Experimental Components

## 14. Superconducting Resistor

### Concept
Below T_c: Zero resistance (continuous supercurrent). Above T_c: Finite resistance (continuous normal current). Transition is discrete phase change.

### Physical Structure
```
1. Substrate: Sapphire (thermal isolation)
2. SC film: YBCO or Nb - 200 nm
3. Heater: Pt strip - 50 nm (to control temperature)
4. Thermometer: Au RTD - 100 nm
5. Contacts: Au - 200 nm
```

**Size**: 0805  
**Operating temperature**: 77K (liquid N₂) for YBCO

### Fabrication Process

#### Step 1: Superconducting Film

**Option A - YBCO (YBa₂Cu₃O₇)**: High-temperature superconductor (T_c = 92K)

**Method**: Pulsed laser deposition (PLD)
- YBCO target
- Substrate: 750°C during deposition
- O₂ atmosphere: 100 mTorr
- **Post-anneal**: 450°C in O₂ for 1 hour
- **Critical**: Oxygen content determines T_c

**Option B - Niobium**: Low-temperature (T_c = 9.2K)
- **Easier to deposit** (DC sputtering)
- But requires liquid He cooling

#### Step 2: Heater & Thermometer
- Pt for both (good stability)
- Photolithography + liftoff

### Testing

**R-T Curve**:
- Cool through T_c, measure resistance
- **Expect**: 
  - Above T_c: R = normal (e.g., 100 Ω)
  - At T_c: Sharp drop
  - Below T_c: R = 0
  - **Transition width**: <1K for good film

**Discrete Phase Transition**:
- Two phases: superconducting vs normal
- First-order transition

**Continuous in Each Phase**:
- Normal state: Continuous R(T)
- SC state: Continuous I (flux flow possible)

### Applications
- Quantum computing components
- Sensitive detectors
- Ultra-low-noise circuits
- Programmable (via temperature)

---

## 15. Josephson Junction Inductor

### Concept
Nonlinear inductor based on Josephson effect: Discrete flux quantization with continuous phase evolution.

### Physical Structure
```
1. Substrate: Si or sapphire
2. Bottom SC: Nb - 150 nm
3. Tunnel barrier: AlO_x - 1-2 nm
4. Top SC: Nb - 150 nm
5. Shunt: Resistor or capacitor
```

**Size**: Junction area 1-10 μm²

### Fabrication (Simplified)

**Dolan Bridge Technique**:
1. Evaporate Nb from angle 1
2. Oxidize surface (creates AlO_x barrier)
3. Evaporate Nb from angle 2
4. Results in overlap junction

**Critical**: <2 nm oxide for strong coupling

### Physics

**Josephson Relations**:
- I = I_c sin(φ), where φ is phase difference
- V = (ℏ/2e)(dφ/dt)
- **Equivalent inductance**: L_J = (ℏ/2e)/I_c
- For I_c = 10 μA: L_J ~ 100 pH

**Discrete**:
- Flux quantization: Φ = nΦ₀, where Φ₀ = h/2e
- n is integer (discrete)

**Continuous**:
- Phase φ evolves continuously
- Current I = I_c sin(φ) is continuous

### Applications
- Superconducting qubits
- SQUIDs (magnetometers)
- Quantum-limited amplifiers
- Parametric oscillators

---

## 16. Quantum Hall Resistor

### Concept
2D electron gas in high magnetic field: Resistance quantized in units of h/e² (discrete) with continuous current flow.

### Physical Structure
```
1. Substrate: GaAs
2. AlGaAs layer: 100 nm (creates 2DEG at interface)
3. Hall bar: Photolithography-defined
4. Contacts: AuGeNi alloyed
```

**Size**: Hall bar 500 μm × 100 μm

### Fabrication

**Wafer Growth**: MOCVD or MBE
- Very high purity GaAs/AlGaAs
- 2D electron gas forms at interface

**Processing**:
- Photolithography to define Hall bar
- Wet etch or dry etch
- AuGeNi contacts, alloyed at 400°C

### Operation

**Measurement**:
- Cool to <1K
- Apply B-field perpendicular (5-10 Tesla)
- Measure R_xy (Hall resistance)

**Expect**:
- R_xy = (h/e²) / ν, where ν = integer (filling factor)
- **Extremely precise**: δR/R < 10⁻⁹
- **Discrete**: Steps at integer ν
- **Continuous**: Current flow is continuous

### Applications
- Resistance standards
- Metrology (defines ohm)
- Topological physics research

---

## 17. Fractal Components (Koch Inductor, Sierpiński Capacitor)

### Concept
Self-similar geometry creates discrete resonances at fractal scales, continuous electromagnetic response between resonances.

### Koch Curve Inductor

**Geometry**: Wire bent in Koch snowflake pattern
- Start with triangle
- Replace each edge with smaller ___/\___
- Iterate 3-4 times

**Fabrication**:
- PCB etching of copper (easier)
- OR: Wire bonding (tedious)
- OR: 3D printing conductive filament

**Performance**:
- Multiple resonances at f, f/3, f/9, f/27...
- Discrete resonant frequencies
- Continuous inductance between them
- Miniaturization vs straight wire

### Sierpiński Capacitor

**Geometry**: Sierpiński triangle electrode pattern
- Fractal cut-outs in capacitor plate
- Multiple length scales

**Fabrication**:
- Laser-cut metal foil
- Etch pattern in PCB
- Stack with dielectric

**Performance**:
- Multi-band resonance
- Discrete frequencies
- Continuous C(f) response
- Compact multi-resonant structure

---

## 18. Topological Insulator Components

### Concept
Bulk is insulating (discrete bandgap), surface conducts (continuous states), protected by topology.

### TI Resistor

**Materials**: Bi₂Se₃, Bi₂Te₃
- Topological insulator materials

**Fabrication**:
- MBE growth on Si substrate
- Exfoliation (like graphene)
- Van der Waals epitaxy

**Properties**:
- Surface states: Continuous, metallic
- Bulk states: Discrete, gapped
- Spin-momentum locked
- Protected against disorder

**Applications**:
- Spintronics
- Quantum computing
- Exotic physics research

---

# TIER 4: Conceptual / Future

## 19. Memtransistor

**Concept**: Transistor whose gain/threshold depends on signal history.

**Possible Implementation**:
- Floating gate transistor
- Or ferroelectric gate oxide

**Status**: Lab demonstrations exist, not production-ready

---

## 20. Ternary/Quaternary Logic Components

**Concept**: Multi-valued logic (0, 1, 2 instead of just 0, 1)

**Implementation**:
- Multiple threshold transistors
- Resonant tunneling diodes
- Quantum dot cellular automata

**Status**: Research stage

---

## 21. Shannon-Limit Components

**Concept**: Operating at theoretical information limits

**Example**: Error-correcting capacitor
- Stores charge + redundancy
- Built-in error correction

**Status**: Theoretical

---

## 22. Möbius Inductor

**Concept**: Inductor with twisted topology

**Fabrication**: 
- Flexible PCB twisted into Möbius strip
- Inductor coil on surface

**Properties**:
- Single-sided surface
- Unusual magnetic field topology
- Interesting for antenna applications

**Status**: Novelty, some research interest

---

# Summary Table: All Components

| Component | Tier | Key Equipment | Discrete Aspect | Continuous Aspect | TRL* |
|-----------|------|---------------|-----------------|-------------------|------|
| Quantum Tunnel Resistor | 1 | ALD, e-beam | Electron tunneling events | Macroscopic current | 7 |
| Magnetic Domain Inductor | 1 | Sputter, furnace | Domain states | Inductance, flux | 6 |
| Sample-Hold Capacitor | 1 | PCB fab | Sampling times | Held voltage | 9 |
| Memcapacitor | 1 | ALD, PECVD | Trapped charge states | Capacitance value | 5 |
| Meminductor | 1 | Sputter, assembly | Domain pinning | Inductance history | 4 |
| Brownian Resistor | 1 | PLD, QD synthesis | QD charge states | Thermal fluctuations | 3 |
| Piezo-Quantum Capacitor | 1 | MOCVD, ALD | QW energy levels | Strain, capacitance | 4 |
| Dual-Mode Memristor | 1 | ALD, sputter | Binary HfO₂ state | Analog TaO_x resistance | 6 |
| Quantum Dot Array | 2 | E-beam litho, synthesis | Single-electron charging | Net current | 5 |
| Spin Resistor (GMR) | 2 | Sputter, anneal | Spin alignment | Resistance, field response | 9 |
| Photo-Capacitor | 2 | Spin coater, evap | Photon absorption | Charge accumulation | 5 |
| Magnetoelectric Inductor | 2 | Tape cast, sinter | FE domain switching | Inductance tuning | 4 |
| Multi-Level Ladder Cap | 2 | PCB fab | Switched states | Varactor tuning | 7 |
| Superconducting Resistor | 3 | PLD, cryo | Phase transition | R(T) in each phase | 8 |
| Josephson Inductor | 3 | UHV, cryo | Flux quantization | Phase evolution | 7 |
| Quantum Hall Resistor | 3 | MBE, cryo, magnet | Landau levels | Current flow | 9 |
| Fractal Inductor | 3 | Laser/etch | Resonant frequencies | L(f) response | 3 |
| TI Resistor | 3 | MBE/exfoliation | Bulk bandgap | Surface conduction | 4 |
| Memtransistor | 4 | Various | Threshold states | Gain | 3 |
| Ternary Logic | 4 | Various | Three logic levels | Voltage in each | 3 |
| Shannon-Limit | 4 | N/A | Error states | Information | 2 |
| Möbius Inductor | 4 | Flex PCB | Topology | Inductance | 2 |

*TRL = Technology Readiness Level (1=concept, 9=production)

---

# Practical Recommendations

## Best Starting Points (Beyond the 4 Already Detailed):

**1. Quantum Tunnel Resistor**
- Uses accessible equipment
- Clear discrete/continuous behavior
- Practical applications

**2. Magnetic Domain Inductor**
- Combines ferrite (commodity) with thin film
- Interesting magnetic physics
- Useful for programmable filters

**3. Sample-Hold Capacitor**
- Easiest to build (mostly circuit)
- Immediately useful
- Educational value

**4. Dual-Mode Memristor**
- Extends existing memristor work
- Novel dual functionality
- High commercial potential

## Most Exciting / Impactful:

**1. Memcapacitor** - Neuromorphic synapses with analog precision
**2. Quantum Dot Array** - True quantum effects at accessible temperatures
**3. GMR Spin Resistor** - Mature technology, spin electronics
**4. Photo-Capacitor** - Optical interfacing with electronics

## Equipment Investment Priority:

**$100K Budget**:
- Sputterer (essential)
- Tube furnace (essential)
- ALD system (if possible, OR substitute sol-gel)

**$300K Budget**:
- Add: E-beam lithography
- Add: PLD system
- Add: Probe station upgrades

**$500K Budget**:
- Add: MOCVD
- Add: Cryogenic equipment
- Add: High-field magnet

---

**All 24 component types are now documented with practical fabrication routes!**

This catalog provides a complete roadmap from proven technologies (Tier 1) through cutting-edge research (Tier 3) to conceptual future devices (Tier 4). Start with Tier 1, master those processes, then progressively tackle more challenging designs.

The discrete-continuous hybrid paradigm is implementable across all these platforms - the physics is sound, the materials exist, and the fabrication methods are established. It's now a matter of execution and optimization.

---

**Document Version**: 2.0  
**Date**: February 2026  
**Status**: Complete Component Catalog  
**Coverage**: 24/24 Hybrid Component Types
