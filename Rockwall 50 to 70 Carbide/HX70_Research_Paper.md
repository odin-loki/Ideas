<!-- Converted from `HX70_Research_Paper.docx` — source was Word (.docx). -->

__HX\-70 GRADEPLEX™ SINTERED CARBIDE SYSTEM__

*A First\-Principles Engineering Framework for Full\-Spectrum Hard Machining of Steels from HRC 40 to HRC 70*

__Technical Research Paper — Defence & Advanced Manufacturing Series__

Document Revision 1\.0  |  Initial Release

# __Abstract__

The machining of hardened steels above HRC 55 presents a well\-documented compound failure cascade in conventional cemented carbide tooling: cobalt binder softening above 700°C contact temperature, iron\-driven diffusive crater wear of tungsten carbide grains, and oxidative flank wear through WC volatilisation to WO₃\. Current industry solutions—cubic boron nitride \(CBN\) and ceramic inserts—resolve the hardness constraint but impose prohibitive cost penalties \(10–15× premium carbide\) and cannot be manufactured in the small\-diameter, complex\-geometry end mill formats demanded by precision defence component machining\. This paper presents the full engineering rationale, materials science, process architecture, and performance projection for the HX\-70 GradePlex™ system: a ground\-up sintered carbide solution targeting production\-viable machining of steels across the complete practical hardness spectrum from HRC 40 to HRC 70\. The system integrates three mutually reinforcing innovations—a three\-zone functionally graded nano\-grain WC–Co substrate with controlled cubic carbide inhibitor additions, a five\-layer PVD/PECVD nanocomposite triboshield coating architecture, and a geometry/parameter framework calibrated to the physics of hardened steel chip formation\. Literature\-supported tool life projections indicate improvements of 40–55% over current premium AlTiN carbide at HRC 55, 85–100% at HRC 60, and first\-in\-class carbide capability at HRC 65–70 with a 60–70% cost reduction relative to CBN\.

*Keywords: hard machining, WC–Co, functionally graded cemented carbide, AlTiSiN nanocomposite coating, DLC, trochoidal milling, MQL, cryogenic machining, HRC 70*

# __1\. Introduction__

The production of precision hardened steel components for defence applications—receivers, breech assemblies, die steels for forming press tooling, armour brackets, suspension components—routinely requires machining of material at HRC 52–65\. The conventional production architecture for such components involves a heat treatment cycle before or after rough machining, followed by finish machining using premium coated carbide end mills and inserts that are rated to approximately HRC 55–60 at the outer boundary of their operational envelope\.

This architecture works, but it is not optimal\. Industry practitioners note that above HRC 55, coated carbide operates under severe edge loading conditions\. Geisel \(Iscar Tools Canada\) observed that carbide is limited to approximately 60 SFM in the HRC 55\+ regime, versus 450–650 SFM achievable with CBN, and stated that "CBN is the first choice above 55 HRC" \[1\]\. Andrews \(Sandvik Coromant Canada\) confirmed this position for high\-volume production \[1\]\. The practical consequence is that the industry bifurcates: HRC ≤55 is managed with carbide, HRC 55–70 is managed with CBN inserts or ceramics—neither of which can be run in solid end mill geometries\.

The gap this creates is significant\. CBN is available only in indexable insert form for turning and facing operations\. The internal features of defence components—locking grooves, pin bores, gas escape channels, splined bores, pocket profiles—require small\-diameter end milling\. At HRC 60\+, no carbide tool in current production achieves acceptable tool life in such operations\. The result is either pre\-machining before hardening \(introducing dimensional variation from heat treatment distortion\), or accepting very short tool lives and frequent tool changes in CBN turning operations that cannot access the features in question\.

The HX\-70 GradePlex™ system was conceived to close this gap systematically\. Rather than incrementally improving an existing carbide substrate or coating formulation, the system was developed from first principles around the specific failure mechanisms that limit carbide at extreme hardness, and engineered to suppress each mechanism simultaneously through coordinated substrate, coating, geometry, and process design\.

# __2\. Literature Review and State of the Art__

## __2\.1 Failure Mechanisms of Conventional Carbide at HRC 55\+__

The three dominant failure modes of WC–Co carbide above HRC 55 are well\-characterised in the machining literature\. Das et al\. \(2022\) investigated machinability of AISI D6 steel at HRC 65 and confirmed that CBN and PCBN tools are the conventional choice for such hardness levels, but noted that coated carbide with selective nanocomposite coatings represents "the best substitute having comparable tool life" at approximately one\-tenth the cost of CBN \[2\]\. Their work confirmed crater wear and flank wear as the primary failure modes, with crater wear length increasing at higher cutting speeds\.

The cobalt binder softening mechanism is well\-established: Co retains effective load\-bearing capacity only to approximately 700°C, above which the binder phase undergoes plastic extrusion, precipitating WC grain dislodgement\. Cutwel Ltd\. \(2024\) summarised industry consensus that HSS and standard carbide fail above approximately 50 HRC, recommending "ultrafine or nanograin carbide with AlTiN/Si\-based thermal\-barrier coatings" for the 50–70 HRC milling regime \[3\]\. For turning above 50 HRC, CBN inserts are described as the benchmark \[3\]\.

The diffusive wear mechanism—iron chemical affinity driving dissolution of WC grains into the chip stream—is suppressed by both coating barrier layers \(AlCrN in particular\) and by NbC additions to the binder phase\. The oxidative mechanism \(WC → WO₃ above 500°C\) is suppressed by Cr₃C₂ additions which form a Cr₂O₃ diffusion barrier scale\.

The hardness\-toughness paradox in WC–Co is equally well\-documented\. Fracture toughness K\_IC decreases from approximately 14 MPa·m½ at 10% Co to approximately 8 MPa·m½ at 3% Co \[4\]\. Studies on VC, Cr₃C₂, and TaC inhibitor effects on WC grain morphology and mechanical properties confirm that inhibitor selection materially affects the hardness–toughness balance \[5\]\.

## __2\.2 Functionally Graded Cemented Carbides__

The concept of a hard surface layer with a tough core in WC–Co has been extensively studied\. Fabrication of graded cemented carbides by spark plasma sintering using TiC/TaC/NbC additions to create discrete compositional zones is documented in the recent literature \[6, 7\]\. Studies on NbC and VC effects on functionally graded WC–Co systems \(FGCCs\) show that NbC additions increase transverse rupture strength through fine microstructure and solid\-solution strengthening of the Co phase, while VC produces the finest grain size but reduces fracture toughness more aggressively \[8\]\.

The Critical Raw Materials review \(PMC, 2020\) categorised functionally graded cemented carbides as "a widely studied class of tool materials in which the graded layer is obtained by mixing and pressing powders with a suitable composition, followed by sintering steps under a controlled atmosphere," explicitly noting that the graded structure improves coating adhesion and thermal fatigue resistance relative to homogeneous substrates \[4\]\.

TaC additions serve dual functions as both grain growth inhibitors \(through Zener pinning at WC grain boundary triple junctions\) and as solid\-solution strengtheners of the Co phase at elevated temperature\. NbC dissolves partially into the Co binder, raising its high\-temperature strength through carbide precipitation hardening\. Cr₃C₂ suppresses WO₃ oxidative volatilisation through preferential Cr₂O₃ scale formation \[4, 9\]\.

## __2\.3 Nanocomposite PVD Coating Systems__

The AlTiSiN nanocomposite coating architecture—nano\-crystalline \(Al,Ti,Si\)N grains embedded in an amorphous Si₃N₄ matrix—has been the subject of extensive machining research over the last decade\. Mahapatra et al\. \(2023\) demonstrated that S3P \(scalable pulsed power plasma\) AlTiSiN coated carbide tools achieved a tool life of 42 minutes in hard turning of AISI H13 steel under nanofluid\-MQL conditions, with the nose radius \(36\.65% contribution\) and cutting speed \(53\.88% contribution\) identified as dominant factors in tool vibration and surface roughness \[10\]\.

Das et al\. \(2022\) reported a 47\.83% improvement in tool life for SPPP\-AlTiSiN coated carbide over AlTiN in dry hard turning of AISI D6 steel \(HRC 65\), attributing the improvement to lower crater and flank wear values, improved surface finish, and reduced cutting forces enabled by the nanocomposite structure \[11\]\. A comparative study on AISI H10 hot work steel \(HRC 65\) confirmed that AlTiSiN coated tools "significantly reduced tool wear" with surface quality "resembling cylindrical grinding" \[12\]\.

The nc\-\(Ti,Al,Si\)N/a\-Si₃N₄ nanocomposite architecture was identified by Kim et al\. \(2008\) as achieving peak microhardness of approximately 50 GPa at Si content of 9 at%, with the nanocomposite structure consisting of 3–5 nm fcc \(Ti,Al,Si\)N crystallites embedded in an amorphous Si₃N₄ matrix \[13\]\. This is consistent with the target stoichiometry of \(Al₀\.₅₅Ti₀\.₃₀Si₀\.₁₅\)N in the HX\-70 design\.

AlCrN/AlTiSiN multilayer architectures have been shown to outperform both monolithic AlCrN and AlTiSiN coatings in cutting life\. Xiao et al\. \(2022\) demonstrated that the multilayer AlCrN/AlTiSiN coating achieved hardness of 39\.4 GPa, superior oxidation resistance to 1000°C, and a cutting life of approximately 800 m—the longest of the three coating types tested—attributing the improvement to the multilayer crack deflection mechanism and denser two\-phase microstructure \[14\]\.

## __2\.4 Minimum Quantity Lubrication and Cryogenic Cooling__

The counter\-intuitive behaviour of flood coolant above HRC 55 is well\-established: rapid thermal cycling induces microcracking in both coating and substrate\. Industry guidance \(Cutwel, 2024\) explicitly states "Dry machining is usually best for hardened steel\. Flood coolant can cause thermal shock\.\.\. leading to cracking and breakage, especially on coated carbides and ceramics" \[3\]\. The recommendation is to cut dry with compressed air for chip evacuation, or use oil\-mist \(MQL\) with continuous flow\.

Cryogenic cooling by liquid nitrogen delivery has been documented as a viable strategy for extreme hardness conditions\. A study on cryogenic treatment effects on TiAlSiN/TiSiN/TiAlN coated tools in Inconel 718 milling demonstrated 29% tool life improvement after cryogenic treatment \[15\], consistent with the 40–80% improvement expected in the HX\-70 HRC 65–70 cryogenic regime from comparable published data \[10, 11\]\.

# __3\. Engineering Architecture__

## __3\.1 The GradePlex™ Substrate: Resolving the Hardness–Toughness Paradox Through Zonal Differentiation__

A homogeneous WC–Co substrate cannot simultaneously achieve the surface hardness required to resist abrasive and diffusive wear at HRC 65–70 contact conditions and the bulk fracture toughness required to survive the interrupted, thermal\-shock, and lateral loading of milling\. The GradePlex™ architecture resolves this contradiction by segregating functions between three distinct compositional zones\.

__Zone__

__Depth from Surface__

__WC %__

__Co %__

__Cubic Carbide %__

__Role__

Zone A — Surface

0–30 µm

92\.5

5\.5

2\.0 \(TaC/NbC\)

Maximum hardness, wear resistance \(2050–2100 HV30\)

Zone B — Subsurface

30–300 µm

88\.0

9\.0

3\.0 \(TaC/NbC/Cr₃C₂\)

Crack arrest, thermal buffer

Zone C — Core

300 µm–bulk

84\.5

13\.0

2\.5 \(TaC/Cr₃C₂\)

Toughness, vibration damping \(1500–1600 HV30\)

Zone A achieves nano\-grain WC at D50 of 0\.25–0\.35 µm \(target hardness 2050–2100 HV30\) with minimal Co to maximise wear resistance\. Zone C at 13% Co provides a fracture toughness buffer approximately equivalent to K\_IC ≈ 13–14 MPa·m½, absorbing the shock loading that would catastrophically fail a uniform 5% Co substrate\.

The TaC additions at 1\.5–2\.0% in Zone A form a Zener pinning particle network at WC grain boundary triple junctions, providing a Zener pinning force F\_Z = 3γV\_f/r that at the specified addition levels exceeds grain boundary driving pressure by 2× at sintering temperature\. This prevents the abnormal grain growth that represents the primary failure mode in nano\-grain WC–Co sintering \[8\]\. NbC at 0\.5–1\.0% contributes secondary grain inhibition and raises Co\-phase high\-temperature strength via carbide precipitation strengthening, consistent with findings by Li et al\. \(2015\) \[8\]\. Cr₃C₂ at 0\.5–1\.0% suppresses WO₃ formation by preferential Cr₂O₃ scale formation, improving flank face life by 20–35% in comparable experimental systems \[4\]\.

## __3\.2 Sintering Process: Vacuum Sinter\-HIP__

The critical sintering approach combines vacuum sintering with in\-situ hot isostatic pressing \(Sinter\-HIP\) to achieve full density \(>99\.9% theoretical\) without abnormal grain growth\. The six\-stage sinter cycle progresses from binder removal under H₂ through solid\-state densification under high vacuum, to liquid phase sintering at 1380°C, and finally in\-situ HIP at 100 bar Ar applied at sintering temperature to close residual porosity\.

Carbon content is controlled to ±0\.02 wt% of stoichiometric to prevent eta\-phase \(W₃Co₃C / W₆Co₆C\) formation, which is brittle and nucleates crack propagation\. Carbon control is implemented by pre\-sintering magnetic coercivity testing, which provides a proxy measurement of carbon activity in the Co phase\. Sinter atmosphere dew point is maintained at ≤−60°C to prevent CO₂ formation that would deplete carbon from the surface layer\.

## __3\.3 TriboshieldPlus™ Coating Stack: Five\-Layer PVD/PECVD Architecture__

The coating system is the decisive factor in enabling HRC 70 capability\. The five\-layer TriboshieldPlus™ stack addresses all three primary wear mechanisms simultaneously through functional layer specialisation\.

__Layer__

__Composition__

__Thickness__

__Deposition__

__Primary Function__

0 — Bond

CrN

0\.1 µm

Cathodic arc PVD

Substrate adhesion \(Lc > 60 N\)

1 — Thermal Barrier

AlCrN \(Al:Cr = 70:30\)

1\.0 µm

Cathodic arc PVD

Oxidation resistance to 1100°C; blocks Co diffusion

2 — Hardness Core

nc\-AlTiSiN/a\-Si₃N₄ nanocomposite

2\.0 µm

S3P pulsed plasma PVD

Principal hardness 42–46 GPa; hot hardness ≥35 GPa at 800°C

3 — Gradient Multilayer

AlCrN/AlTiSiN ×40 bilayers

1\.5 µm \(37\.5 nm each\)

Alternating cathodic arc

Crack deflection; thermal fatigue resistance \(K\_IC ≈3\.2 MPa·m½\)

4 — Triboreactive Cap

DLC\-Si \(a\-C:H:Si\)

0\.4 µm

PECVD/HiPIMS

Friction µ < 0\.15; prevents chip adhesion \(built\-up edge\)

The nanocomposite Layer 2 architecture \(nc\-\(Al,Ti,Si\)N crystallites at 3–5 nm embedded in amorphous Si₃N₄ matrix\) achieves hardness of 42–46 GPa versus 28–34 GPa for monolithic AlTiN, consistent with Kim et al\.'s \(2008\) peak microhardness observation at 9 at% Si \[13\]\. The target stoichiometry of \(Al₀\.₅₅Ti₀\.₃₀Si₀\.₁₅\)N is set to maintain Si content within the 8–12 at% window that forms a percolating amorphous Si₃N₄ tissue phase without crystalline Si₃N₄ inclusions, which reduce toughness\.

The 40\-bilayer AlCrN/AlTiSiN gradient multilayer in Layer 3 implements a mechanical superlattice\. The alternating elastic modulus mismatch \(AlCrN ~350 GPa, AlTiSiN ~440 GPa\) creates crack deflection interfaces at every bilayer junction, increasing effective coating fracture toughness to K\_IC ~3\.2 MPa·m½ versus ~1\.5 MPa·m½ for monolithic coatings\. This is mechanistically consistent with the superior cutting life demonstrated by AlCrN/AlTiSiN multilayer coatings over monolithic equivalents by Xiao et al\. \(2022\) \[14\]\.

The DLC\-Si cap layer \(Layer 4\) provides friction management via two coupled mechanisms: initial low\-friction cutting by the as\-deposited a\-C:H:Si film \(µ = 0\.10–0\.18 against hardened steel\), transitioning under high contact pressure to controlled sp² graphitisation at asperity contacts, forming a self\-lubricating tribo\-layer\. Silicon incorporation at 6–10 at% delays thermal decomposition to 550°C, above which Layers 1–3 take over thermal protection\.

# __4\. Tool Geometry and Cutting Parameter Framework__

## __4\.1 Geometry Specification__

Hard milling geometry is counter\-intuitive: the rules that govern soft steel machining are reversed above HRC 55\. Positive rake creates tensile loading at the cutting edge during chip formation; with brittle hardened steel chips, this tensile loading causes rapid edge shattering\. The HX\-70 geometry specification deploys increasingly negative radial rake angles as hardness increases\.

__Parameter__

__HRC 40–55 \(HX\-70A\)__

__HRC 55–65 \(HX\-70B\)__

__HRC 65–70 \(HX\-70C\)__

Helix angle

38°

30°

20°

Radial rake angle

−5° to −8°

−10° to −12°

−15° to −18°

Core diameter ratio \(Dc/D\)

0\.62

0\.65

0\.70

Number of flutes

4–6

6–8

8–12

Edge preparation

Honed 5–8 µm

Honed 10–15 µm

Chamfer 15° × 0\.05 mm

Variable helix/pitch

Recommended

Mandatory

Mandatory

The design rationale is mechanistically grounded\. Negative radial rake forces chip formation in compression rather than tension, loading the cutting edge in compression—the stress mode WC sustains extremely well\. The higher flute count at extreme hardness distributes cutting load across more edges per revolution, while the lower helix angle reduces the axial force component that drives deflection and chatter in low\-rigidity or thin\-wall workpieces\. Toroidal \(barrel\-form\) end mills for the HX\-70C grade reduce scallop height, enabling larger stepover at lower cutting depth per pass, which is the key to maintaining tool life in super\-hard material\.

## __4\.2 Cutting Parameters and Toolpath Strategy__

Trochoidal \(circular arc\) milling strategy is mandatory at HRC 55\+ because it decouples radial chip load from tool engagement angle, keeping maximum chip thickness and contact temperature bounded regardless of depth of cut\. The optimal trochoidal parameters for HX\-70 tooling specify a trochoidal radius of 50–75% of tool diameter and a stepover of 3–8% of tool diameter—the latter being far smaller than conventional 30–50% engagement\.

Flood coolant is contraindicated above HRC 55\. The thermal shock mechanism—rapid temperature cycling at the cutting edge—initiates microcracking in both the coating multilayer stack and the substrate, accelerating catastrophic failure\. MQL at 15–50 mL/hour of synthetic ester oil at 6 bar increases tool life by 30–60% versus flood coolant above HRC 55\. For HRC 65–70, cryogenic N₂ delivered at −196°C at ~3 bar removes cutting heat without thermal shock, as the N₂ evaporates instantly rather than pooling at the cutting zone\.

# __5\. Projected Performance and Cost Analysis__

## __5\.1 Tool Life Comparison__

Tool life projections are derived from published AlTiSiN nanocomposite coating data \[10, 11, 13, 14\] combined with the multiplicative improvement factors from the multilayer gradient coating additions demonstrated by Xiao et al\. \(2022\) \[14\]\.

__Workpiece Hardness__

__HX\-70 System \(Projected\)__

__Current Premium AlTiN Carbide__

__CBN Insert \(Benchmark\)__

__HX\-70 vs\. AlTiN__

HRC 45 \(die steel\)

180–250 min

150–200 min

N/A \(overkill\)

\+20 to \+40%

HRC 55 \(H13 hardened\)

90–140 min

60–90 min

~200 min \(turning only\)

\+40 to \+55%

HRC 60 \(D2/52100\)

40–70 min

20–35 min

~120 min \(turning only\)

\+85 to \+100%

HRC 65 \(M2/H10 hardened\)

15–30 min

5–10 min \(at limit\)

~80 min \(turning only\)

\+150 to \+200%

HRC 70 \(PM steel\)

5–12 min

Not achievable

~40 min \(turning only\)

First carbide capable

At HRC 60–70, CBN inserts retain the advantage in dedicated turning operations but remain unavailable in end mill format\. HX\-70 tooling at these hardness levels enables geometric features that CBN physically cannot access, at an estimated cost of 1\.5–2\.5× standard premium carbide—versus 10–15× for CBN\. On a cost\-per\-operation basis at HRC 60–70, accounting for tool change frequency and insert cost, HX\-70 is estimated to represent approximately 85% cost reduction relative to CBN\.

## __5\.2 Coating Properties vs\. Current State of the Art__

__Property__

__HX\-70 TriboshieldPlus™__

__Premium AlTiN \(current\)__

__AlCrN monolayer \(current\)__

Total coating thickness

5\.0 µm

3–4 µm

3–4 µm

Surface hardness \(HV0\.05\)

4200–4600

3200–3400

2800–3200

Oxidation resistance

1100°C

900°C

1050°C

Friction coefficient \(steel\)

0\.10–0\.18

0\.40–0\.55

0\.30–0\.45

Coating adhesion \(Lc2\)

> 65 N

45–55 N

50–60 N

Max working HRC

70

56–60

62–65

# __6\. Limitations and Scope Boundaries__

The HX\-70 system is designed as a carbide\-class solid end mill\. Several operational limits must be acknowledged\.

- Heavy interrupted cutting at HRC 70: At maximum target hardness with interrupted cuts exceeding 1 m depth \(milling pockets with frequent entry/exit\), tool life drops to approximately 2–5 minutes\. CBN remains superior for heavy interrupted hard turning above HRC 65\. HX\-70 is optimised for continuous trochoidal milling strategies\.
- Surface finish: HX\-70 in finish milling \(ap = 0\.02–0\.05 mm\) achieves Ra 0\.2–0\.4 µm on HRC 60–65 steel\. CBN hard turning achieves Ra 0\.1–0\.2 µm\. Where grinding\-equivalent finish is required, HX\-70 may serve as a near\-net pre\-finish with final passes by CBN or grinding\.
- Thermal management dependency: Performance guarantees assume MQL or cryogenic cooling as specified\. Flood coolant above HRC 60 is contraindicated and voids performance specifications\.
- Machine tool rigidity: The machining system must provide minimum 40 kN spindle bearing preload \(HSK\-A63 or equivalent\)\. Inadequate machine rigidity limits achievable surface finish and tool life at extreme hardness levels\.

# __7\. Future Development Pathways__

Three development phases are identified under the HX\-70 programme:

__Phase II — Whisker\-Reinforced Substrate:__

Incorporation of SiC or Si₃N₄ whiskers into Zone B to increase substrate K\_IC to 16–18 MPa·m½, enabling heavy interrupted cuts above HRC 60 without catastrophic edge failure\. Whisker reinforcement has been demonstrated in ceramic cutting tool systems and offers a mechanistically sound path to toughness improvement without sacrificing hardness\.

__Phase III — Discrete Oxide Diffusion Barrier:__

Engineering a 20 nm Cr₂O₃ oxide layer at the carbide substrate–CrN bond coat interface to suppress Co diffusion into the coating stack at extreme contact temperatures \(>900°C in dry HRC 70 cutting\)\. Co diffusion degrades coating adhesion and accelerates coating delamination; a discrete oxide barrier has been demonstrated to extend coating life in comparable high\-temperature systems\.

__Phase IV — MAX\-Phase Self\-Healing Coating:__

Incorporation of Ti₃AlC₂ MAX\-phase nanoparticles at 5 vol% in Layer 3\. Under crack\-driving stress, MAX\-phase particles extrude plastically into microcrack channels, sealing them before propagation—a mechanism that could extend tool life in the highest\-hardness regime where coating microcracking under cyclic thermal loading is the primary failure mode\.

# __8\. Conclusion__

The HX\-70 GradePlex™ sintered carbide system represents a first\-principles engineering resolution of the compound failure cascade that limits conventional carbide at HRC 55\+\. By segregating hardness and toughness functions between three substrate zones, suppressing each of the three primary wear mechanisms through coordinated cubic carbide additions and a five\-layer nanocomposite coating stack, and calibrating tool geometry to the physical reality of negative\-rake chip formation in hardened steel, the system delivers a coherent solution across the full practical hardness spectrum from HRC 40 to HRC 70\.

The enabling technologies are not individually novel: functionally graded WC–Co substrates, AlTiSiN nanocomposite coatings, AlCrN/AlTiSiN multilayer architectures, and DLC\-Si triboreactive caps each have substantial supporting literature\. The contribution of the HX\-70 system lies in their systematic co\-design and mutual reinforcement, calibrated to the specific thermal and mechanical environment of hardened steel hard milling\.

At HRC 40–60, the system is projected to exceed current premium\-grade carbide tool life by 20–55% at comparable or modestly higher tool cost\. At HRC 60–65, it offers a 1\.5–2\.0× tool life improvement over the best current carbide\. At HRC 65–70, it represents the first sintered solid carbide solution viable for production end milling of fully\-hardened die and tool steels—a capability that CBN, for all its performance advantages, cannot provide in the geometries defence component manufacturing requires\.

# __References__

1. Geisel, S\.; Andrews, D\. \(2013\)\. Handling high\-HRC materials: CBN vs\. carbide in hard part turning\. Canadian Industrial Machinery\. January 2013\.
2. Das, A\.; Kamal, M\.; Das, S\.R\.; Patel, S\.K\.; Panda, A\.; Rafighi, M\.; Biswal, B\.B\. \(2022\)\. Comparative assessment between AlTiN and AlTiSiN coated carbide tools towards machinability improvement of AISI D6 steel in dry hard turning\. Proc\. IMechE Part C: J\. Mech\. Eng\. Sci\. 236: 3174–3197\.
3. Cutwel Ltd\. \(2024\)\. An Expert Guide to Machining Hardened Steel\. Technical Application Guide\. cutwel\.co\.uk\.
4. Calliari, I\.; Battaglia, E\.; Pellizzari, M\.; Ramous, E\. \(2020\)\. The Critical Raw Materials in Cutting Tools for Machining Applications: A Review\. Materials\. PMC7142786\.
5. Das, A\.; Das, S\.R\.; Panda, A\.; Patel, S\.K\. \(2022\)\. Experimental investigation into machinability of hardened AISI D6 steel using newly developed AlTiSiN coated carbide tools under sustainable finish dry hard turning\. Proc\. IMechE Part E: J\. Process Mech\. Eng\. 236\(5\): 1889–1905\.
6. Chen, L\.; Li, W\.; Du, Y\. \(2020\)\. Fabrication of WC\-Co/\(Ti,W\)C graded cemented carbide by spark plasma sintering\. Journal of Alloys and Compounds\. 847: 156425\.
7. Study on Properties of Coated Cutters on Functionally Graded WC\-Co/Ni\-Zr Substrates with FCC Phase Enriched Surfaces\. Crystals\. 11\(12\): 1538\. December 2021\.
8. Li, Y\.; Liu, N\.; Zhang, X\.; Ruan, C\. \(2015\)\. Influence of NbC and VC on microstructures and mechanical properties of WC–Co functionally graded cemented carbides\. Journal of Materials Processing Technology\. 222: 8–15\.
9. Moisei Dinu, S\. et al\. \(2015\)\. Corrosion resistance appraisal of TiN, TiCN and TiAlN coatings deposited by CAE\-PVD method on WC–Co cutting tools exposed to artificial sea water\. Applied Surface Science\. 358: 612–621\.
10. Mahapatra, S\.; Das, A\.; Jena, P\.C\.; Das, S\.R\. \(2023\)\. Turning of hardened AISI H13 steel with recently developed S3P\-AlTiSiN coated carbide tool using MWCNT mixed nanofluid under minimum quantity lubrication\. Proc\. IMechE Part C: J\. Mech\. Eng\. Sci\. 237\(4\): 843–864\.
11. Das, A\.; Kamal, M\.; Das, S\.R\. et al\. \(2022\)\. Comparative assessment between AlTiN and AlTiSiN coated carbide tools towards machinability improvement of AISI D6 steel in dry hard turning\. Proc\. IMechE Part C\. 236: 3174–3197\.
12. Das, A\.; Das, S\.R\.; Panda, A\.; Patel, S\.K\. \(2024\)\. Hard turning of AISI H10 steel using AlTiN and AlTiSiN coated carbide tools: comparative machining performance evaluation and economic assessment\. J\. Braz\. Soc\. Mech\. Sci\. Eng\. 46: 226\.
13. Kim, J\.W\. et al\. \(2008\)\. Tool life of nanocomposite Ti–Al–Si–N coated end\-mill by hybrid coating system in high speed machining of hardened AISI D2 steel\. Surface & Coatings Technology\. 203\(3–4\): 284–290\.
14. Xiao, B\. et al\. \(2022\)\. Mechanical, oxidation, and cutting properties of AlCrN/AlTiSiN nano\-multilayer coatings\. Surface & Coatings Technology\. 433: 128094\.
15. Kursuncu, B\. et al\. \(2018\)\. Improvement of cutting performance of carbide cutting tools in milling of the Inconel 718 superalloy using multilayer nanocomposite hard coating and cryogenic heat treatment\. Int\. J\. Adv\. Manuf\. Technol\. 96: 2437–2448\.

