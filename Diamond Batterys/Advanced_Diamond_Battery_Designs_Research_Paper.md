<!-- Converted from `Advanced_Diamond_Battery_Designs_Research_Paper.docx` — source was Word (.docx). -->

__ADVANCED HYPOTHETICAL DIAMOND BATTERY DESIGNS__

*Next\-Generation Nuclear Waste\-Powered Diamond Batteries for High Power Applications*

__Technical Research Paper__

Prepared by: Odin | March 2026

__DISCLAIMER__

*This paper presents speculative engineering proposals extrapolated from established nuclear physics and materials science\. All models labelled Series A through D are hypothetical and have not been experimentally validated\. Power output figures represent theoretical upper bounds and are not guaranteed\.*

# Abstract

This paper presents a comprehensive technical framework for a family of advanced hypothetical nuclear diamond battery designs, catalogued across four series \(A–D\), each targeting different power regimes from kilowatt to gigawatt scale\. The proposed architectures build upon the world's first demonstrated carbon\-14 diamond battery <a id="footnote-ref-2"></a>[\[1\]](#footnote-2), developed in December 2024 by the University of Bristol and the UK Atomic Energy Authority \(UKAEA\), and extrapolate established radioisotope power systems science toward utility\-scale applications\. The designs incorporate multi\-isotope hybrid cores, three\-dimensional nanostructured diamond matrices, alpha\-voltaic and thermal\-betavoltaic hybrid conversion, and advanced neutron moderation techniques\. Drawing on peer\-reviewed literature in betavoltaic physics <a id="footnote-ref-4"></a>[\[2\]](#footnote-4)<a id="footnote-ref-6"></a>[\[3\]](#footnote-6), radioisotope thermoelectric generator engineering <a id="footnote-ref-8"></a>[\[4\]](#footnote-8)<a id="footnote-ref-9"></a>[\[5\]](#footnote-9), and diamond semiconductor science <a id="footnote-ref-15"></a>[\[6\]](#footnote-15)<a id="footnote-ref-16"></a>[\[7\]](#footnote-16), this paper critically evaluates theoretical performance limits, identifies the key research breakthroughs required, and proposes a phased 15\-year development roadmap\. A central motivation is the global inventory of over 400,000 metric tonnes of spent nuclear fuel <a id="footnote-ref-11"></a>[\[8\]](#footnote-11), which these designs could transform from a long\-term liability into a distributed clean energy resource\.

# 1\. Introduction

Humanity faces two interlocking challenges in the coming decades: eliminating carbon emissions from the global energy system, and safely disposing of legacy nuclear waste accumulated over 70 years of fission power\. As of 2024, over 400,000 metric tonnes of spent nuclear fuel have accumulated worldwide since the beginning of nuclear electricity generation in 1954 <a id="footnote-ref-11"></a>[\[9\]](#footnote-11), with more than 12,000 metric tonnes added annually <a id="footnote-ref-13"></a>[\[10\]](#footnote-13)\. In the United States alone, approximately 91,000 metric tonnes of spent nuclear fuel sit in interim storage across 80 or more sites, awaiting a permanent geological repository that has yet to materialise <a id="footnote-ref-12"></a>[\[11\]](#footnote-12)\. The cost and political complexity of deep geological disposal makes this waste a multi\-generational liability\.

Diamond batteries offer a conceptually elegant resolution to both challenges simultaneously: encapsulating radioactive decay emitters within synthetic diamond matrices converts isotopic decay energy directly into electricity, while the diamond structure provides near\-perfect physical containment of short\-range radiation\. The principle was articulated by Professor Tom Scott at the University of Bristol in 2016 <a id="footnote-ref-1"></a>[\[12\]](#footnote-1), who described it as turning a long\-term problem of nuclear waste into a long\-term supply of clean energy\. The concept reached experimental realisation in December 2024 when Bristol and UKAEA announced the world's first carbon\-14 diamond battery, capable of powering devices for thousands of years at microwatt levels <a id="footnote-ref-2"></a>[\[13\]](#footnote-2)\.

However, the current generation of diamond batteries operates far below the power densities required for industrial or grid\-scale applications\. The carbon\-14 beta emitter provides a maximum decay energy of only 156 keV <a id="footnote-ref-21"></a>[\[14\]](#footnote-21), and even with a 5,700\-year half\-life, one gram of carbon\-14 in diamond form delivers only 15 joules per day <a id="footnote-ref-1"></a>[\[15\]](#footnote-1)\. Standard betavoltaic atomic batteries achieve efficiencies of 0\.1 to 5%, with high\-efficiency devices reaching 6 to 8% <a id="footnote-ref-7"></a>[\[16\]](#footnote-7)\. For applications beyond ultra\-low\-power sensors, medical implants, and space probes, a fundamental leap in isotope selection, device architecture, and conversion physics is required\.

This paper presents a systematic taxonomy of hypothetical advanced diamond battery designs, grounded in established nuclear engineering and materials science, that project how such devices might be scaled to kilowatt, megawatt, and even gigawatt power levels\. Each design is evaluated against the known physics of candidate radioisotopes, diamond semiconductor behaviour, and thermal conversion engineering\. Where designs exceed current experimental capability, the paper identifies precisely which breakthroughs are required and assesses their plausibility in light of ongoing research\.

# 2\. Background and State of the Art

## 2\.1 Current Diamond Battery Technology

The University of Bristol carbon\-14 diamond battery, realised in collaboration with UKAEA, functions by encapsulating carbon\-14 in a thin beta\-emitting diamond film grown by chemical vapour deposition \(CVD\) at UKAEA's Culham Campus <a id="footnote-ref-3"></a>[\[17\]](#footnote-3)\. The device dimensions are approximately 10 x 10 mm and up to 0\.5 mm thick\. Carbon\-14 was chosen for its short\-range beta emission, which is entirely absorbed within the diamond matrix, preventing external radiation exposure <a id="footnote-ref-21"></a>[\[18\]](#footnote-21)\. The prototype delivers tens of microwatts of continuous power, projected to remain at 50% capacity after 5,730 years <a id="footnote-ref-2"></a>[\[19\]](#footnote-2)\.

Earlier University of Bristol prototypes used nickel\-63 as the radiation source, with diamond non\-electrolytes and semiconductors for energy conversion <a id="footnote-ref-1"></a>[\[20\]](#footnote-1)\. Arkenlight, the spinout company commercialising the technology, reports devices of 10 mm square producing tens of microwatts, and a betalight voltaic product generating up to 35 microwatts already deployed commercially in the nuclear industry <a id="footnote-ref-20"></a>[\[21\]](#footnote-20)\. Concurrently, Chinese startup Betavolt announced in 2024 a nickel\-63 miniature betavoltaic device generating 100 microwatts at 3V with a claimed 50\-year lifetime <a id="footnote-ref-7"></a>[\[22\]](#footnote-7)\.

## 2\.2 Betavoltaic and Alphavoltaic Physics

Betavoltaic devices operate on the same principle as photovoltaic solar cells, substituting beta particles for photons\. Beta particles from a radioisotope source interact with a semiconductor p\-n junction, generating electron\-hole pairs that produce an electrical current <a id="footnote-ref-4"></a>[\[23\]](#footnote-4)\. The key figure of merit is conversion efficiency: the ratio of electrical output power to radioisotope decay power\. Despite significant research, practical betavoltaic devices remain constrained below 4% energy conversion efficiency due to limited beta electron interaction and poor charge transport in conventional absorber materials <a id="footnote-ref-17"></a>[\[24\]](#footnote-17)\. Recent advances in silicon carbide and perovskite architectures have demonstrated record efficiencies above 21% <a id="footnote-ref-17"></a>[\[25\]](#footnote-17), suggesting substantial headroom for improvement\.

Alpha emitters offer far higher energy per decay event than beta emitters, with americium\-241 releasing 5\.5 MeV alpha particles compared to just 156 keV maximum for carbon\-14 beta particles <a id="footnote-ref-5"></a>[\[26\]](#footnote-5)\. Using alpha emitters \(alphavoltaics\) would increase energy output by a factor of approximately 100 for the same device size, weight, and packaging <a id="footnote-ref-11"></a>[\[27\]](#footnote-11)\. However, alpha particles cause more severe radiation damage in semiconductor converters, shortening device lifetime\. Wide\-bandgap semiconductors, particularly diamond, silicon carbide, and gallium nitride, offer the radiation hardness needed to exploit alpha emitters <a id="footnote-ref-5"></a>[\[28\]](#footnote-5)\. Recent work by Wang et al\. demonstrated an americium\-243 radiophotovoltaic battery achieving efficiency 8,000 times higher than conventional alpha source\-scintillator designs by incorporating the radioisotope alongside a terbium transducer within a single crystalline material <a id="footnote-ref-18"></a>[\[29\]](#footnote-18)\.

## 2\.3 Radioisotope Thermoelectric Generators

For power levels above the watt range, radioisotope thermoelectric generators \(RTGs\) represent the established technology\. RTGs convert the heat generated by isotope decay into electricity via the Seebeck effect using thermocouple arrays <a id="footnote-ref-8"></a>[\[30\]](#footnote-8)\. Plutonium\-238, with its 87\.7\-year half\-life and 0\.57 watts per gram power density, has been the standard RTG fuel for NASA space missions <a id="footnote-ref-8"></a>[\[31\]](#footnote-8)\. Strontium\-90, readily extracted from spent nuclear fuel with its 28\.8\-year half\-life, offers a power density of 0\.95 watts per gram for the pure metal, and has historically been deployed in Soviet terrestrial RTGs such as the Beta\-M lighthouse generators producing around 230 watts electrical <a id="footnote-ref-8"></a>[\[32\]](#footnote-8)<a id="footnote-ref-10"></a>[\[33\]](#footnote-10)\. Thermoelectric generators are currently the most reliable conversion option, with efficiencies of 6\.6%, with new developments projected to achieve system efficiencies above 15% <a id="footnote-ref-9"></a>[\[34\]](#footnote-9)\. Crucially, because strontium\-90 and cesium\-137 cannot sustain a nuclear chain reaction under any circumstances, RTGs of arbitrary size and power could theoretically be assembled from them given sufficient material <a id="footnote-ref-8"></a>[\[35\]](#footnote-8)\.

## 2\.4 Diamond as a Semiconductor Material

Synthetic diamond grown by chemical vapour deposition possesses extraordinary properties for semiconductor applications: the highest room\-temperature thermal conductivity of any material, a wide bandgap of 5\.47 eV, exceptional charge carrier mobilities exceeding 3,000 cm² V⁻¹ s⁻¹, and unmatched radiation hardness <a id="footnote-ref-15"></a>[\[36\]](#footnote-15)\. Boron doping creates p\-type diamond semiconductors, while phosphorus doping achieves n\-type behaviour, enabling p\-n junction device architectures <a id="footnote-ref-14"></a>[\[37\]](#footnote-14)\. Boron\-doped diamond can be fabricated via CVD by introducing diborane into the plasma deposition process, with boron concentrations tunable from 10¹⁶ to 10²² cm⁻³ <a id="footnote-ref-16"></a>[\[38\]](#footnote-16)\. The carbon\-14 diamond battery exploits the fact that the beta decay energy of 156 keV is insufficient to break diamond covalent bonds, preserving crystal integrity over the device's entire half\-life <a id="footnote-ref-21"></a>[\[39\]](#footnote-21)\. Nitrogen\-vacancy \(NV\) centre diamonds additionally offer quantum coherence properties relevant to next\-generation quantum\-enhanced conversion architectures <a id="footnote-ref-14"></a>[\[40\]](#footnote-14)\.

# 3\. Series A: Multi\-Isotope Hybrid Diamond Batteries

Series A batteries are designed for kilowatt\-scale applications using dual\-isotope engineered decay systems that combine alpha and beta emitters within a single diamond matrix\. The core innovation is exploiting the complementary properties of alpha emitters for high power density and beta emitters for operational longevity\.

## 3\.1 Model ADB\-H1K: Hybrid Alpha\-Beta Diamond Core \(1\-10 kW\)

The ADB\-H1K design centres on americium\-241 as the primary alpha emitter, paired with carbon\-14 as a long\-life beta baseline\. Americium\-241, with a 432\-year half\-life and 5\.5 MeV alpha decay energy, offers a specific power orders of magnitude higher than carbon\-14's 156 keV maximum beta energy <a id="footnote-ref-5"></a>[\[41\]](#footnote-5)\. Research has shown alphavoltaic devices using americium\-241 and diamond can achieve power densities of 10 mW/cm³, with alpha emitters offering approximately 100x higher energy output than beta emitters of equivalent source mass <a id="footnote-ref-5"></a>[\[42\]](#footnote-5)<a id="footnote-ref-11"></a>[\[43\]](#footnote-11)\. The carbon\-14 secondary layer, with its 5,700\-year half\-life, ensures sustained baseline power as americium\-241 decays over centuries\.

__Parameter__

__Specification__

Target Power Output

1 – 10 kW continuous

Primary Emitter

Americium\-241 \(Am\-241\), alpha, 5\.5 MeV, t½ = 432 yr

Secondary Emitter

Carbon\-14, beta, max 156 keV, t½ = 5,700 yr

Theoretical Power Density

15 – 25 mW/g \(target\)

Target Conversion Efficiency

12 – 18%

Operational Life at 90% Capacity

50\+ years

Containment

Triple\-layer diamond matrix \+ metallic housing

The 3D nanostructured diamond lattice architecture is critical to achieving this performance\. By maximising the surface area available for alpha particle capture and minimising the distance between the radioactive source and the semiconductor junction, self\-absorption losses, which currently limit betavoltaic source efficiency to approximately 15\-17% for standard beta emitters, can be significantly reduced\. Boron\-doped diamond semiconductors are employed throughout for their p\-type conductivity and radiation hardness\. A layered isolation design prevents alpha radiation damage from propagating to the carbon\-14 beta conversion layer\.

This architecture aligns with the scientific consensus that alphavoltaics represent the most promising pathway to high\-power nuclear batteries, with diamond as the converter material of choice due to its radiation tolerance and wide bandgap\. The challenge is managing radiation damage accumulation in the diamond matrix from prolonged alpha bombardment, a problem that cutting\-edge CVD synthesis techniques are progressively addressing <a id="footnote-ref-15"></a>[\[44\]](#footnote-15)\.

## 3\.2 Model ADB\-H100K: Americium\-Tritium Cascade Battery \(100 kW – 1 MW\)

The ADB\-H100K design introduces a cascading decay energy harvesting architecture\. The underlying design philosophy draws on the demonstrated properties of plutonium\-238 oxide RTG fuel, which achieves a reasonable power density of 0\.57 watts per gram <a id="footnote-ref-8"></a>[\[45\]](#footnote-8)\. The cascade approach uses americium\-241 alpha decay to bombard lithium\-6 targets, producing tritium through the reaction ⁷Li\(α,n\)³H \+ ¹He\. The tritium then undergoes beta decay, providing sustained secondary power, while waste heat is recovered via thermoelectric conversion\.

The 500 kg Am\-241/Li\-6 reactor core is enclosed within a 50\-layer synthetic diamond containment system\. Advanced boron\-carbide neutron absorbers manage secondary neutron flux from the Li\-6 reactions, and a passive shutdown mechanism triggers on containment breach\. The modular design allows assembly of units in 10 MW increments, enabling scalable deployment\.

A key safety advantage is that no weapons\-usable material is produced in this cycle\. The proliferation resistance of this architecture is consistent with IAEA non\-proliferation guidelines <a id="footnote-ref-11"></a>[\[46\]](#footnote-11)\. The economics are also theoretically attractive: americium\-241 is a waste product in ageing plutonium stockpiles at sites such as Sellafield in the UK, and the European Space Agency has sponsored research into extracting it for RTG use <a id="footnote-ref-10"></a>[\[47\]](#footnote-10)\.

# 4\. Series B: Thermal\-Enhanced Diamond Batteries

Series B systems address the megawatt power regime by combining radioisotope decay heat with direct betavoltaic conversion in a hybrid architecture\. This approach is grounded in the established RTG engineering of large\-scale strontium\-90 and cesium\-137 systems, enhanced by the addition of a diamond betavoltaic matrix for direct conversion efficiency gains\.

## 4\.1 Model TDB\-1M: Radioisotope Thermal\-Betavoltaic Hybrid \(1\-10 MW\)

The TDB\-1M system distributes energy conversion between a dominant thermal channel \(targeting 70% of output\) and a direct betavoltaic channel \(targeting 30% of output\)\. The thermal channel uses strontium titanate \(SrTiO₃\) ceramic pellets containing strontium\-90\. SrTiO₃ is the standard solid form for Sr\-90 RTG fuel, chosen for its chemical inertness and high melting point <a id="footnote-ref-8"></a>[\[48\]](#footnote-8)\. Strontium\-90 has a power density of 0\.95 watts per gram as the pure metal, and a high fission product yield in uranium\-235 and plutonium\-239 fission makes it available at relatively low cost if extracted from spent nuclear fuel <a id="footnote-ref-8"></a>[\[49\]](#footnote-8)\. A 200 kg central strontium titanate core surrounded by a carbon\-14 embedded diamond betavoltaic matrix forms the conversion architecture\.

__Parameter__

__Specification__

Target Power Output

1 – 10 MW continuous

Primary Fuel

Strontium\-90 \(SrTiO₃ ceramic pellets, 200 kg\)

Secondary Fuel

Cesium\-137, Carbon\-14 diamond matrix

Thermal Conversion

Advanced bismuth telluride thermoelectric arrays

Thermal Transfer

Molten salt heat exchange loops

Target System Efficiency

50 – 65% \(thermal 35\-45% \+ direct 15\-20%\)

Operational Life

30\+ years at 80% capacity

The target combined efficiency of 50\-65% represents a major advance over current RTG efficiency of approximately 6\.6% <a id="footnote-ref-9"></a>[\[50\]](#footnote-9)\. This is achievable in principle through layering advanced thermoelectric materials \(higher ZT Yintl phases, filled skutterudites, and BiTe alloys\) with parallel betavoltaic diamond conversion\. The challenge lies in thermal management: the diamond betavoltaic matrix must be maintained at operating temperature ranges compatible with both semiconductor and thermoelectric function simultaneously\.

Cesium\-137, with a 30\-year half\-life, is one of the most abundant and energetically significant isotopes in spent nuclear fuel\. The UK's high\-level nuclear waste contains nearly 97% of the total radioactivity in less than 3% of the volume <a id="footnote-ref-11"></a>[\[51\]](#footnote-11), with cesium and strontium isotopes among the dominant contributors\. Extracting these for energy generation, as proposed here, would substantially reduce the radiotoxicity and heat load of spent fuel requiring geological disposal\.

## 4\.2 Model TDB\-100M: Utility\-Scale Thermal Diamond Array \(100\+ MW\)

The TDB\-100M scales the hybrid architecture to utility level through an array of 1,000 modular 100 kW thermal\-diamond units with N\+3 redundancy\. The distributed architecture provides multiple fail\-safe advantages: no single module failure can affect global plant output, isotope processing can proceed in a continuous closed\-loop cycle with no plant downtime, and the modular format allows phased construction and incremental commissioning\.

The nuclear waste supply chain for this system is self\-funding in principle: waste owners currently face substantial long\-term storage costs, and would benefit economically from providing isotope feedstock to such a facility\. The global nuclear waste recycling market was valued at $3\.66 billion in 2024 <a id="footnote-ref-13"></a>[\[52\]](#footnote-13)\. Converting high\-level waste isotopes into energy generation could turn a global liability into a global asset, consistent with the "circular economy" framework being developed for the nuclear sector <a id="footnote-ref-21"></a>[\[53\]](#footnote-21)\. The zero\-carbon, zero\-water\-cooling footprint would offer land and resource efficiencies unavailable to any comparable thermal or renewable power source\.

# 5\. Series C: Advanced Neutronics Diamond Batteries

Series C systems push into the tens of megawatt and gigawatt regime by incorporating controlled neutron physics\. These designs move significantly beyond current betavoltaic or RTG paradigms and require breakthroughs in both materials science and nuclear engineering\. They are presented as long\-horizon concepts rather than near\-term engineering proposals\.

## 5\.1 Model NDB\-10M: Moderated Fast Neutron Diamond System \(10\+ MW\)

The NDB\-10M uses curium\-244 spontaneous fission as a neutron source, directed into a subcritical uranium\-235 assembly via an ultra\-pure graphite\-diamond composite moderator\. The neutron flux induces fission events in the subcritical assembly at rates controlled by boron\-10 neutron poison rods, generating a sustained cascade of decay products absorbed by the surrounding diamond matrix\. Tritium production from neutron capture is an additional energy channel\.

The subcritical operation principle is fundamental to the safety case: the system is always maintained below critical mass, requiring the curium\-244 external neutron driver to sustain any reaction\. Curium\-244 is itself a nuclear waste product with an 18\-year half\-life and the highest specific thermal power among commonly proposed RTG isotopes <a id="footnote-ref-9"></a>[\[54\]](#footnote-9)\. Its typical use has been limited to small RTGs due to short lifespan, but its high neutron yield makes it ideal as a driver source in this architecture\. Under any credible accident scenario, removal or failure of the curium driver terminates the reaction passively\.

## 5\.2 Model NDB\-1G: Gigawatt\-Scale Diamond Reactor Array \(1\+ GW\)

The NDB\-1G concept targets baseload utility replacement at gigawatt scale\. It combines 100 modular 10 MW diamond reactor units under AI\-powered predictive control, with molten salt thermal storage providing load\-following capability over a 20\-100% power range\. The fuel matrix uses americium\-242m, which requires approximately 1% of the mass of uranium\-235 or plutonium\-239 to reach criticality, reducing the total fissile inventory required for any given power level\.

This design requires the most significant unproven technology of any series: large\-scale synthetic diamond production, automated robotic isotope handling at scale, and gigawatt\-class nuclear system licensing in a new regulatory category\. It is best understood as a directional research target rather than a near\-term engineering proposal, with a realistic first deployment date of 2040 or later under the most optimistic assumptions\.

# 6\. Series D: Breakthrough Conversion Technologies

Series D designs explore the frontier of conversion physics, incorporating quantum and photonic effects that go beyond classical semiconductor p\-n junction betavoltaics\. These represent the most speculative tier of the taxonomy but are grounded in real physical phenomena with active laboratory investigation\.

## 6\.1 Model QDB\-1K: Quantum\-Enhanced Diamond Battery \(1\-5 kW\)

The QDB\-1K exploits quantum phenomena native to the diamond structure\. Nitrogen\-vacancy \(NV\) centres in diamond act as atomic\-scale quantum sensors with long coherence times at room temperature, and ongoing research is exploring their utility as quantum information interfaces <a id="footnote-ref-14"></a>[\[55\]](#footnote-14)\. In the QDB\-1K design, engineered NV\-centre concentrations serve as quantum efficiency enhancers for electron capture, reducing the energy loss associated with phonon scattering that limits classical betavoltaic efficiency\. Embedded diamond quantum dots provide quantum confinement effects that tune electron capture cross\-sections, while graphene monolayer interfaces provide ballistic electron transport pathways\.

The combination of carbon nanotube 3D electron transport networks with metamaterial electromagnetic structures represents an attempt to engineer the conversion physics at the nanoscale level\. This is an emerging research frontier: the landmark 2024 review of CVD diamond applications explicitly identifies NV\-centre diamonds and quantum computing as among the most promising future directions for the material <a id="footnote-ref-15"></a>[\[56\]](#footnote-15)\. Whether quantum coherence enhancement of betavoltaic conversion is physically achievable at the device scale required here remains an open research question\.

## 6\.2 Model PDB\-10K: Photonic\-Enhanced Diamond System \(10\+ kW\)

The PDB\-10K introduces a radioluminescent photovoltaic intermediate conversion stage\. Scintillator technology that converts high\-energy particles into photons, which are then converted by photovoltaic cells, is an established indirect conversion method <a id="footnote-ref-6"></a>[\[57\]](#footnote-6)\. The innovation here is applying this to a diamond\-based system using quantum dot wavelength tuning, perovskite film photovoltaic conversion, and metamaterial optical concentration\.

Recent research has demonstrated dramatic efficiency improvements in alpha\-decay radioluminescent systems: Wang et al\. \(2025\) achieved power conversion 8,000 times more efficient than conventional separated source\-scintillator designs by incorporating americium\-243 and a terbium\-based transducer within a single crystalline material <a id="footnote-ref-18"></a>[\[58\]](#footnote-18)\. The PDB\-10K design generalises this approach across multiple isotope combinations and wavelength channels\. The use of dual\- and multi\-mode operation \(direct betavoltaic mode combined with radioluminescent photovoltaic mode\) enables dynamic optimisation of conversion pathway based on operating conditions\.

# 7\. Manufacturing and Production Technologies

## 7\.1 Diamond Synthesis

Chemical vapour deposition is the established process for producing high\-purity single\-crystal diamond for semiconductor applications, and CVD methods have been continuously refined since their first description in 1956 <a id="footnote-ref-16"></a>[\[59\]](#footnote-16)\. Plasma\-enhanced CVD at the UKAEA Culham Campus was used to grow the carbon\-14 diamond battery prototype <a id="footnote-ref-3"></a>[\[60\]](#footnote-3)\. Key process parameters include substrate temperature, methane concentration, substrate off\-axis angle, and in the case of boron doping, diborane concentration in the plasma <a id="footnote-ref-16"></a>[\[61\]](#footnote-16)\. Current production rates of 2\-10 micrometres per hour for single\-crystal CVD diamond represent the primary throughput bottleneck for scaling to the device dimensions required by Series A through D batteries\.

Boron\-doped diamond \(BDD\), produced by introducing diborane to the CVD plasma, creates p\-type semiconductor diamond with tuneable conductivity from insulating to highly conductive depending on boron concentration <a id="footnote-ref-14"></a>[\[62\]](#footnote-14)\. High\-pressure high\-temperature \(HPHT\) synthesis offers an alternative route for large\-scale production, with Schottky barrier diamond diode stacks of 200 cells having been fabricated for betavoltaic prototypes achieving 0\.93 microwatts in 5 x 5 x 3\.5 mm³ total volume <a id="footnote-ref-6"></a>[\[63\]](#footnote-6)\. For the Series A\-D battery designs, massively parallel thin\-film deposition reactors analogous to those used in the solar cell industry would be required to achieve production volumes at commercially relevant costs\.

## 7\.2 Isotope Processing

The isotope supply chain for advanced diamond batteries is both the critical enabler and the principal practical challenge\. Carbon\-14 is sourced from radioactive graphite blocks used as neutron moderators in graphite\-moderated reactors\. The UK holds approximately 95,000 tonnes of such graphite blocks <a id="footnote-ref-4"></a>[\[64\]](#footnote-4), and the carbon\-14 is concentrated at the surface of these blocks, making extraction feasible through surface processing\. Strontium\-90 is extracted from spent nuclear fuel by solvent extraction and ion exchange processes demonstrated at scale in the United States since the 1960s, with more than 8 million curies processed at Hanford from 1961 to 1964 <a id="footnote-ref-10"></a>[\[65\]](#footnote-10)\. Americium\-241 is extracted from weapons\-grade plutonium stockpiles undergoing natural decay, with industrial\-scale production projected in the UK in the near future <a id="footnote-ref-10"></a>[\[66\]](#footnote-10)\.

All isotope handling requires highly automated robotic systems capable of operating within shielded hot cells\. Quality assurance protocols must verify isotopic purity at 99\.99%\+ levels to prevent beta\-gamma contamination in alpha\-voltaic conversion layers\. Closed\-loop processing with zero discharge is both technically feasible and a regulatory requirement in all jurisdictions\.

## 7\.3 Economic Projections

__Phase__

__Period__

__Activity__

__Est\. Investment__

Phase 1

2025 – 2030

Research & prototype development

$5B

Phase 2

2030 – 2035

Pilot plant construction & testing

$15B

Phase 3

2035 – 2040

Commercial production scale\-up

$20B

Phase 4

2040\+

Global deployment & grid integration

$10B\+

The target levelised cost of energy for utility\-scale diamond battery arrays is below $0\.02/kWh at full production scale, achieved primarily through near\-zero fuel cost \(isotope waste streams have negative cost\), minimal operational labour through automation, and ultra\-long asset lifetimes exceeding 30 years without fuel replacement\. Capital costs are projected to decline rapidly as CVD diamond synthesis scales, analogous to the cost trajectories observed in solar photovoltaic manufacturing\.

# 8\. Safety and Environmental Assessment

## 8\.1 Radiation Safety

The fundamental radiation safety case for diamond batteries rests on the fact that the diamond matrix provides complete containment of short\-range alpha and beta radiation\. Carbon\-14 emits beta particles with a mean free path of only fractions of a millimetre in solid matter; diamond's density ensures these particles are entirely self\-absorbed within the device <a id="footnote-ref-21"></a>[\[67\]](#footnote-21)\. As Dr Neil Fox of Bristol stated: diamond is the hardest substance known to man, there is literally nothing we could use that could offer more protection <a id="footnote-ref-1"></a>[\[68\]](#footnote-1)\. For alpha emitters in Series A\-D designs, the shorter range of alpha particles \(typically stopped by a sheet of paper in air\) is even more completely contained within the multi\-layered diamond and metallic housing system\.

For Series B thermal systems using strontium\-90, the primary radiological concern is the beta\-gamma emission of the yttrium\-90 daughter product and the bone\-seeking biological behaviour of strontium if released\. Strontium titanate ceramic pellets represent the standard risk\-mitigating fuel form, chosen precisely for their chemical inertness and resistance to dispersal under accident conditions\. The Soviet Beta\-M RTG incident at Lia, Georgia in 2001 demonstrates the consequences of inadequate containment and the importance of multi\-barrier protection\. The designs proposed here incorporate four independent containment barriers: diamond matrix, metallic pressure vessel, reinforced concrete, and underground installation\.

## 8\.2 Nuclear Proliferation

Diamond battery designs using carbon\-14, strontium\-90, cesium\-137, and americium\-241 pose minimal proliferation risk\. None of these isotopes is directly usable in nuclear weapons, and americium\-241 alphavoltaic devices explicitly produce no weapons\-grade materials <a id="footnote-ref-10"></a>[\[69\]](#footnote-10)\. The Series C NDB designs, incorporating uranium\-235 or americium\-242m subcritical assemblies, would require substantially more rigorous IAEA safeguards under Additional Protocol requirements <a id="footnote-ref-11"></a>[\[70\]](#footnote-11)\. Any deployment of Series C or NDB\-1G systems would require comprehensive physical protection measures and material accountability under existing non\-proliferation treaty frameworks\.

## 8\.3 Environmental Benefits

The global inventory of spent nuclear fuel accumulating worldwide represents one of the most concentrated repositories of long\-lived radioactive hazard in human history\. Since the start of nuclear electricity production in 1954 to the end of 2016, some 390,000 tonnes of spent fuel were generated globally <a id="footnote-ref-11"></a>[\[71\]](#footnote-11)\. The diamond battery framework offers a means to extract value from isotopes that would otherwise require hundreds of years of monitored storage, converting them into clean electricity with zero operational carbon emissions, zero water cooling requirements, and a dramatically smaller land footprint than equivalent solar or wind capacity\.

# 9\. Regulatory and Policy Framework

Diamond batteries represent a genuinely new regulatory category: neither a conventional nuclear reactor nor a simple radioisotope device, they combine elements of both\. In the United States, many smoke detectors contain americium\-241 below the NRC exemption limit of 5 microcuries, suggesting that very small diamond battery devices might qualify for exemption <a id="footnote-ref-12"></a>[\[72\]](#footnote-12)\. Scaling to the kilowatt and megawatt devices proposed in Series A and B would require novel licensing frameworks\. The ADVANCE Act of 2024, signed by President Biden, includes provisions for advanced reactor licensing that could potentially accommodate novel betavoltaic and thermal conversion architectures <a id="footnote-ref-12"></a>[\[73\]](#footnote-12)\.

International coordination through the IAEA will be essential for any large\-scale deployment, particularly for material accounting under the Joint Convention on the Safety of Spent Fuel Management and Radioactive Waste Management <a id="footnote-ref-11"></a>[\[74\]](#footnote-11)\. Technology transfer protocols for controlled deployment in developing nations and non\-proliferation verification of Series C NDB designs will require dedicated international treaty instruments beyond existing frameworks\.

Public acceptance remains a critical non\-technical barrier\. Despite the excellent safety record of modern nuclear technology, public perception of radiation risk consistently exceeds actuarial risk in comparative analyses\. The transparency of the diamond battery concept, its visible connection to solving the nuclear waste problem, and its biocompatible applications in medical devices are potential public communication advantages\. The track record of radioisotope\-powered pacemakers from the 1960s through the 1990s provides a precedent for public acceptance of implanted nuclear power sources in life\-critical applications\.

# 10\. Comparative Model Summary

__Model__

__Power__

__Primary Fuel__

__Conversion__

__TRL Target__

ADB\-H1K

1–10 kW

Am\-241 \+ C\-14

Alphavoltaic \+ betavoltaic

2030

ADB\-H100K

100 kW–1 MW

Am\-241 \+ Li\-6 \(tritium cascade\)

Alpha\-cascade \+ thermoelectric

2035

TDB\-1M

1–10 MW

Sr\-90 \+ Cs\-137 \+ C\-14

Thermal \+ betavoltaic hybrid

2035

TDB\-100M

100\+ MW

Sr\-90 / Cs\-137 arrays

Distributed thermal\-diamond

2040

NDB\-10M

10\+ MW

Cm\-244 \(neutron\) \+ U\-235 subcritical

Neutron\-induced betavoltaic cascade

2040

NDB\-1G

1\+ GW

Am\-242m \+ C\-14 \+ tritium

Multi\-stage thermal \+ direct

2045\+

QDB\-1K

1–5 kW

C\-14 / Ni\-63 \+ NV diamond

Quantum\-enhanced betavoltaic

2035

PDB\-10K

10\+ kW

Am\-241 \+ Am\-243 scintillator

Radioluminescent photovoltaic

2035

# 11\. Conclusion

This paper has presented a systematic taxonomy of advanced hypothetical diamond battery designs spanning eight models across four series, from kilowatt alphavoltaic devices to gigawatt reactor arrays\. All designs are grounded in established nuclear physics and materials science, building from the proven carbon\-14 diamond battery demonstrated by the University of Bristol and UKAEA in December 2024 <a id="footnote-ref-2"></a>[\[75\]](#footnote-2), and extrapolating to power regimes that current technology cannot achieve but that the underlying physics does not forbid\.

The path from microwatt demonstration to megawatt utility application requires advances in five critical areas:

1. Advanced isotope engineering: controlled large\-scale production and processing of Am\-241, Sr\-90, and Cs\-137 from nuclear waste streams\.
2. 3D diamond architecture: nanostructured diamond matrices maximising surface area for particle capture and minimising self\-absorption losses\.
3. Hybrid conversion systems: combined thermal and direct conversion technologies achieving system efficiencies well above current RTG baselines\.
4. Automated manufacturing: large\-scale automated CVD diamond synthesis and robotic isotope assembly at production costs compatible with grid\-scale energy\.
5. Advanced safety systems: passive fail\-safe designs with active AI\-powered monitoring validated across all credible accident scenarios\.

The transformative potential is real and scientifically grounded\. The global inventory of over 400,000 metric tonnes of spent nuclear fuel <a id="footnote-ref-11"></a>[\[76\]](#footnote-11), growing at 12,000 tonnes per year <a id="footnote-ref-13"></a>[\[77\]](#footnote-13), represents both the raw material for these systems and the motivation for developing them\. Converting this liability into clean energy would simultaneously address two of the most intractable problems in energy policy\. The 15\-year development timeline from 2025 to 2040 proposed here is aggressive but consistent with historical nuclear technology development trajectories when backed by adequate investment and political will\.

The diamond battery concept is no longer purely theoretical\. The December 2024 prototype is the first proof of principle for a technology that, with sustained research investment and international cooperation, could form the cornerstone of a post\-fossil\-fuel energy system built on the clean transformation of humanity's nuclear legacy\.

# 12\. References

1. Scott, T\.B\. et al\. \(2016\)\. Cabot Institute Annual Lecture: Diamond Battery Concept\. University of Bristol\. Available at: https://www\.bristol\.ac\.uk/cabot/what\-we\-do/diamond\-batteries/
2. University of Bristol & UKAEA \(2024\)\. Scientists and Engineers Produce World's First Carbon\-14 Diamond Battery\. Press Release, 4 December 2024\. Available at: https://www\.bristol\.ac\.uk/news/2024/december/diamond\-battery\-media\-release\.html
3. Fox, N\. & Smith, J\. et al\. \(2024\)\. Carbon\-14 Diamond Battery\. School of Chemistry, University of Bristol\. Available at: https://www\.bristol\.ac\.uk/chemistry/news/2024/carbon\-battery\.html
4. Spencer, M\.G\. & Alam, T\. \(2019\)\. High power direct energy conversion by nuclear batteries\. Applied Physics Reviews, 6\(3\), 031305\. https://doi\.org/10\.1063/1\.5123163
5. Langley, J\.D\.S\., Litz, M\.S\. & Ray, W\.B\. \(2017\)\. Design of Alpha Voltaic Power Source Using Americium\-241 and Diamond with a Power Density of 10 mW/cm³\. Proceedings, Army Research Laboratory\.
6. Thomas, J\. et al\. \(2023\)\. Betavoltaic Nuclear Battery: A Review of Recent Progress and Challenges as an Alternative Energy Source\. Journal of Physical Chemistry C, 127\(16\), 7565–7579\. https://doi\.org/10\.1021/acs\.jpcc\.3c00684
7. Wikipedia \(2025\)\. Atomic Battery\. Available at: https://en\.wikipedia\.org/wiki/Atomic\_battery
8. Wikipedia \(2025\)\. Radioisotope Thermoelectric Generator\. Available at: https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator
9. Wang, X\. et al\. \(2019\)\. Critical design features of thermal\-based radioisotope generators: A review of the power solution for polar regions and space\. Renewable and Sustainable Energy Reviews, 119, 109519\. https://doi\.org/10\.1016/j\.rser\.2019\.109519
10. Ambrosi, R\.M\. et al\. \(2019\)\. Safe radioisotope thermoelectric generators and heat sources for space applications\. Journal of Nuclear Materials, 377\(2\-3\), 506–521\. https://doi\.org/10\.1016/j\.jnucmat\.2008\.03\.030
11. IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. Available at: https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management
12. U\.S\. Congressional Research Service \(2024\)\. Considerations for Reprocessing of Spent Nuclear Fuel\. R48364\. Available at: https://www\.congress\.gov/crs\-product/R48364
13. Market Reports World \(2024\)\. Nuclear Waste Recycling Market 2024–2033\. Available at: https://www\.marketreportsworld\.com/market\-reports/nuclear\-waste\-recycling\-market\-14718618
14. Nebel, C\. \(2020\)\. Nitrogen\-vacancy doped CVD diamond for quantum applications: A review\. Semiconductors and Semimetals, vol\. 103\. https://doi\.org/10\.1016/bs\.semsem\.2020\.03\.001
15. May, P\.W\. et al\. \(2024\)\. Applications of diamond films: a review\. Functional Diamond, 4\(1\), 2410160\. https://doi\.org/10\.1080/26941112\.2024\.2410160
16. Schreck, M\. & Voelkl, R\. \(2011\)\. A review of diamond synthesis by CVD processes\. Diamond and Related Materials, 20\(5\-6\), 620–640\. https://doi\.org/10\.1016/j\.diamond\.2011\.03\.014
17. Jiang, S\. & Liu, X\. \(2025\)\. Beta\-voltaic nuclear batteries: review of recent developments, challenges and future research directions\. Journal of Energy Storage\. https://doi\.org/10\.1016/j\.est\.2025\.014148
18. Wang, Y\. et al\. \(2025\)\. Alpha\-decay radioluminescent nuclear battery with single\-crystal americium\-terbium transducer\. Chemistry World\. Available at: https://www\.chemistryworld\.com/news/the\-race\-to\-commercialise\-nuclear\-powered\-batteries/4020505\.article
19. Clark, S\. & Scott, T\. \(2024\)\. Diamond Battery — World Nuclear News Coverage\. World Nuclear News, 10 December 2024\. Available at: https://world\-nuclear\-news\.org/articles/carbon\-14\-diamond\-battery\-is\-world\-first\-say\-uk\-scientists
20. Boardman, C\. \(2021\)\. Arkenlight: Commercializing Nuclear Diamond Betavoltaic Batteries\. Interview, New Atlas, 5 May 2021\. Available at: https://newatlas\.com/energy/arkenlight\-nuclear\-diamond\-batteries/
21. Ekanem, E\. & Sanni, F\. \(2024\)\. World\-First Carbon\-14 Diamond Battery\. IOM3 Materials World\. Available at: https://www\.iom3\.org/resource/world\-first\-carbon\-14\-diamond\-battery\.html

1. <a id="footnote-2"></a>University of Bristol & UKAEA \(2024\)\. World's First Carbon\-14 Diamond Battery\. Press Release, 4 December 2024\. https://www\.bristol\.ac\.uk/news/2024/december/diamond\-battery\-media\-release\.html [↑](#footnote-ref-2)


2. <a id="footnote-4"></a>Spencer, M\.G\. & Alam, T\. \(2019\)\. High power direct energy conversion by nuclear batteries\. Applied Physics Reviews, 6\(3\), 031305\. https://doi\.org/10\.1063/1\.5123163 [↑](#footnote-ref-4)


3. <a id="footnote-6"></a>Thomas, J\. et al\. \(2023\)\. Betavoltaic Nuclear Battery: A Review of Recent Progress and Challenges as an Alternative Energy Source\. Journal of Physical Chemistry C, 127\(16\), 7565\-7579\. https://doi\.org/10\.1021/acs\.jpcc\.3c00684 [↑](#footnote-ref-6)


4. <a id="footnote-8"></a>Wikipedia: Radioisotope Thermoelectric Generator\. \(2025\)\. https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator [↑](#footnote-ref-8)


5. <a id="footnote-9"></a>Wang, X\. et al\. \(2019\)\. Critical design features of thermal\-based radioisotope generators\. Renewable and Sustainable Energy Reviews, 119, 109519\. https://doi\.org/10\.1016/j\.rser\.2019\.109519 [↑](#footnote-ref-9)


6. <a id="footnote-15"></a>May, P\.W\. et al\. \(2024\)\. Applications of diamond films: a review\. Functional Diamond, 4\(1\), 2410160\. https://doi\.org/10\.1080/26941112\.2024\.2410160 [↑](#footnote-ref-15)


7. <a id="footnote-16"></a>Schreck, M\. & Voelkl, R\. \(2011\)\. A review of diamond synthesis by CVD processes\. Diamond and Related Materials, 20\(5\-6\), 620\-640\. https://doi\.org/10\.1016/j\.diamond\.2011\.03\.014 [↑](#footnote-ref-16)


8. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


9. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


10. <a id="footnote-13"></a>Market Reports World \(2024\)\. Nuclear Waste Recycling Market\. https://www\.marketreportsworld\.com/market\-reports/nuclear\-waste\-recycling\-market\-14718618 [↑](#footnote-ref-13)


11. <a id="footnote-12"></a>U\.S\. Congressional Research Service \(2024\)\. Considerations for Reprocessing of Spent Nuclear Fuel\. https://www\.congress\.gov/crs\-product/R48364 [↑](#footnote-ref-12)


12. <a id="footnote-1"></a>Scott, T\.B\. et al\. \(2016\)\. Cabot Institute Annual Lecture: Diamond Battery Concept\. University of Bristol\. https://www\.bristol\.ac\.uk/cabot/what\-we\-do/diamond\-batteries/ [↑](#footnote-ref-1)


13. <a id="footnote-2"></a>University of Bristol & UKAEA \(2024\)\. World's First Carbon\-14 Diamond Battery\. Press Release, 4 December 2024\. https://www\.bristol\.ac\.uk/news/2024/december/diamond\-battery\-media\-release\.html [↑](#footnote-ref-2)


14. <a id="footnote-21"></a>Ekanem, E\. & Sanni, F\. \(2024\)\. Carbon\-14 Diamond Battery Operation and Applications\. UKAEA / IOM3 Materials World\. https://www\.iom3\.org/resource/world\-first\-carbon\-14\-diamond\-battery\.html [↑](#footnote-ref-21)


15. <a id="footnote-1"></a>Scott, T\.B\. et al\. \(2016\)\. Cabot Institute Annual Lecture: Diamond Battery Concept\. University of Bristol\. https://www\.bristol\.ac\.uk/cabot/what\-we\-do/diamond\-batteries/ [↑](#footnote-ref-1)


16. <a id="footnote-7"></a>Wikipedia: Atomic Battery\. \(2025\)\. https://en\.wikipedia\.org/wiki/Atomic\_battery [↑](#footnote-ref-7)


17. <a id="footnote-3"></a>Fox, N\. & Smith, J\. et al\. \(2024\)\. Carbon\-14 Diamond Battery\. School of Chemistry, University of Bristol\. https://www\.bristol\.ac\.uk/chemistry/news/2024/carbon\-battery\.html [↑](#footnote-ref-3)


18. <a id="footnote-21"></a>Ekanem, E\. & Sanni, F\. \(2024\)\. Carbon\-14 Diamond Battery Operation and Applications\. UKAEA / IOM3 Materials World\. https://www\.iom3\.org/resource/world\-first\-carbon\-14\-diamond\-battery\.html [↑](#footnote-ref-21)


19. <a id="footnote-2"></a>University of Bristol & UKAEA \(2024\)\. World's First Carbon\-14 Diamond Battery\. Press Release, 4 December 2024\. https://www\.bristol\.ac\.uk/news/2024/december/diamond\-battery\-media\-release\.html [↑](#footnote-ref-2)


20. <a id="footnote-1"></a>Scott, T\.B\. et al\. \(2016\)\. Cabot Institute Annual Lecture: Diamond Battery Concept\. University of Bristol\. https://www\.bristol\.ac\.uk/cabot/what\-we\-do/diamond\-batteries/ [↑](#footnote-ref-1)


21. <a id="footnote-20"></a>Boardman, C\. \(2021\)\. Arkenlight: Commercializing Nuclear Diamond Betavoltaic Batteries\. New Atlas, 5 May 2021\. https://newatlas\.com/energy/arkenlight\-nuclear\-diamond\-batteries/ [↑](#footnote-ref-20)


22. <a id="footnote-7"></a>Wikipedia: Atomic Battery\. \(2025\)\. https://en\.wikipedia\.org/wiki/Atomic\_battery [↑](#footnote-ref-7)


23. <a id="footnote-4"></a>Spencer, M\.G\. & Alam, T\. \(2019\)\. High power direct energy conversion by nuclear batteries\. Applied Physics Reviews, 6\(3\), 031305\. https://doi\.org/10\.1063/1\.5123163 [↑](#footnote-ref-4)


24. <a id="footnote-17"></a>Jiang, S\. & Liu, X\. \(2025\)\. Beta\-voltaic nuclear batteries: review of recent developments, challenges and future research directions\. Journal of Energy Storage\. https://doi\.org/10\.1016/j\.est\.2025\.014148 [↑](#footnote-ref-17)


25. <a id="footnote-17"></a>Jiang, S\. & Liu, X\. \(2025\)\. Beta\-voltaic nuclear batteries: review of recent developments, challenges and future research directions\. Journal of Energy Storage\. https://doi\.org/10\.1016/j\.est\.2025\.014148 [↑](#footnote-ref-17)


26. <a id="footnote-5"></a>Langley, J\.D\.S\., Litz, M\.S\. & Ray, W\.B\. \(2017\)\. Design of Alpha Voltaic Power Source Using Americium\-241 and Diamond with a Power Density of 10 mW/cm3\. Semantic Scholar\. [↑](#footnote-ref-5)


27. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


28. <a id="footnote-5"></a>Langley, J\.D\.S\., Litz, M\.S\. & Ray, W\.B\. \(2017\)\. Design of Alpha Voltaic Power Source Using Americium\-241 and Diamond with a Power Density of 10 mW/cm3\. Semantic Scholar\. [↑](#footnote-ref-5)


29. <a id="footnote-18"></a>Wang, Y\. et al\. \(2025\)\. Alpha\-decay radioluminescent nuclear battery using single\-crystal americium\-terbium\. Chemistry World, October 2025\. https://www\.chemistryworld\.com/news/the\-race\-to\-commercialise\-nuclear\-powered\-batteries/4020505\.article [↑](#footnote-ref-18)


30. <a id="footnote-8"></a>Wikipedia: Radioisotope Thermoelectric Generator\. \(2025\)\. https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator [↑](#footnote-ref-8)


31. <a id="footnote-8"></a>Wikipedia: Radioisotope Thermoelectric Generator\. \(2025\)\. https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator [↑](#footnote-ref-8)


32. <a id="footnote-8"></a>Wikipedia: Radioisotope Thermoelectric Generator\. \(2025\)\. https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator [↑](#footnote-ref-8)


33. <a id="footnote-10"></a>Ambrosi, R\.M\. et al\. \(2019\)\. Safe radioisotope thermoelectric generators and heat sources for space applications\. Journal of Nuclear Materials, 377\(2\-3\), 506\-521\. https://doi\.org/10\.1016/j\.jnucmat\.2008\.03\.030 [↑](#footnote-ref-10)


34. <a id="footnote-9"></a>Wang, X\. et al\. \(2019\)\. Critical design features of thermal\-based radioisotope generators\. Renewable and Sustainable Energy Reviews, 119, 109519\. https://doi\.org/10\.1016/j\.rser\.2019\.109519 [↑](#footnote-ref-9)


35. <a id="footnote-8"></a>Wikipedia: Radioisotope Thermoelectric Generator\. \(2025\)\. https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator [↑](#footnote-ref-8)


36. <a id="footnote-15"></a>May, P\.W\. et al\. \(2024\)\. Applications of diamond films: a review\. Functional Diamond, 4\(1\), 2410160\. https://doi\.org/10\.1080/26941112\.2024\.2410160 [↑](#footnote-ref-15)


37. <a id="footnote-14"></a>Nebel, C\. \(2020\)\. Nitrogen\-vacancy doped CVD diamond for quantum applications: A review\. Semiconductors and Semimetals, vol\. 103\. https://doi\.org/10\.1016/bs\.semsem\.2020\.03\.001 [↑](#footnote-ref-14)


38. <a id="footnote-16"></a>Schreck, M\. & Voelkl, R\. \(2011\)\. A review of diamond synthesis by CVD processes\. Diamond and Related Materials, 20\(5\-6\), 620\-640\. https://doi\.org/10\.1016/j\.diamond\.2011\.03\.014 [↑](#footnote-ref-16)


39. <a id="footnote-21"></a>Ekanem, E\. & Sanni, F\. \(2024\)\. Carbon\-14 Diamond Battery Operation and Applications\. UKAEA / IOM3 Materials World\. https://www\.iom3\.org/resource/world\-first\-carbon\-14\-diamond\-battery\.html [↑](#footnote-ref-21)


40. <a id="footnote-14"></a>Nebel, C\. \(2020\)\. Nitrogen\-vacancy doped CVD diamond for quantum applications: A review\. Semiconductors and Semimetals, vol\. 103\. https://doi\.org/10\.1016/bs\.semsem\.2020\.03\.001 [↑](#footnote-ref-14)


41. <a id="footnote-5"></a>Langley, J\.D\.S\., Litz, M\.S\. & Ray, W\.B\. \(2017\)\. Design of Alpha Voltaic Power Source Using Americium\-241 and Diamond with a Power Density of 10 mW/cm3\. Semantic Scholar\. [↑](#footnote-ref-5)


42. <a id="footnote-5"></a>Langley, J\.D\.S\., Litz, M\.S\. & Ray, W\.B\. \(2017\)\. Design of Alpha Voltaic Power Source Using Americium\-241 and Diamond with a Power Density of 10 mW/cm3\. Semantic Scholar\. [↑](#footnote-ref-5)


43. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


44. <a id="footnote-15"></a>May, P\.W\. et al\. \(2024\)\. Applications of diamond films: a review\. Functional Diamond, 4\(1\), 2410160\. https://doi\.org/10\.1080/26941112\.2024\.2410160 [↑](#footnote-ref-15)


45. <a id="footnote-8"></a>Wikipedia: Radioisotope Thermoelectric Generator\. \(2025\)\. https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator [↑](#footnote-ref-8)


46. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


47. <a id="footnote-10"></a>Ambrosi, R\.M\. et al\. \(2019\)\. Safe radioisotope thermoelectric generators and heat sources for space applications\. Journal of Nuclear Materials, 377\(2\-3\), 506\-521\. https://doi\.org/10\.1016/j\.jnucmat\.2008\.03\.030 [↑](#footnote-ref-10)


48. <a id="footnote-8"></a>Wikipedia: Radioisotope Thermoelectric Generator\. \(2025\)\. https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator [↑](#footnote-ref-8)


49. <a id="footnote-8"></a>Wikipedia: Radioisotope Thermoelectric Generator\. \(2025\)\. https://en\.wikipedia\.org/wiki/Radioisotope\_thermoelectric\_generator [↑](#footnote-ref-8)


50. <a id="footnote-9"></a>Wang, X\. et al\. \(2019\)\. Critical design features of thermal\-based radioisotope generators\. Renewable and Sustainable Energy Reviews, 119, 109519\. https://doi\.org/10\.1016/j\.rser\.2019\.109519 [↑](#footnote-ref-9)


51. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


52. <a id="footnote-13"></a>Market Reports World \(2024\)\. Nuclear Waste Recycling Market\. https://www\.marketreportsworld\.com/market\-reports/nuclear\-waste\-recycling\-market\-14718618 [↑](#footnote-ref-13)


53. <a id="footnote-21"></a>Ekanem, E\. & Sanni, F\. \(2024\)\. Carbon\-14 Diamond Battery Operation and Applications\. UKAEA / IOM3 Materials World\. https://www\.iom3\.org/resource/world\-first\-carbon\-14\-diamond\-battery\.html [↑](#footnote-ref-21)


54. <a id="footnote-9"></a>Wang, X\. et al\. \(2019\)\. Critical design features of thermal\-based radioisotope generators\. Renewable and Sustainable Energy Reviews, 119, 109519\. https://doi\.org/10\.1016/j\.rser\.2019\.109519 [↑](#footnote-ref-9)


55. <a id="footnote-14"></a>Nebel, C\. \(2020\)\. Nitrogen\-vacancy doped CVD diamond for quantum applications: A review\. Semiconductors and Semimetals, vol\. 103\. https://doi\.org/10\.1016/bs\.semsem\.2020\.03\.001 [↑](#footnote-ref-14)


56. <a id="footnote-15"></a>May, P\.W\. et al\. \(2024\)\. Applications of diamond films: a review\. Functional Diamond, 4\(1\), 2410160\. https://doi\.org/10\.1080/26941112\.2024\.2410160 [↑](#footnote-ref-15)


57. <a id="footnote-6"></a>Thomas, J\. et al\. \(2023\)\. Betavoltaic Nuclear Battery: A Review of Recent Progress and Challenges as an Alternative Energy Source\. Journal of Physical Chemistry C, 127\(16\), 7565\-7579\. https://doi\.org/10\.1021/acs\.jpcc\.3c00684 [↑](#footnote-ref-6)


58. <a id="footnote-18"></a>Wang, Y\. et al\. \(2025\)\. Alpha\-decay radioluminescent nuclear battery using single\-crystal americium\-terbium\. Chemistry World, October 2025\. https://www\.chemistryworld\.com/news/the\-race\-to\-commercialise\-nuclear\-powered\-batteries/4020505\.article [↑](#footnote-ref-18)


59. <a id="footnote-16"></a>Schreck, M\. & Voelkl, R\. \(2011\)\. A review of diamond synthesis by CVD processes\. Diamond and Related Materials, 20\(5\-6\), 620\-640\. https://doi\.org/10\.1016/j\.diamond\.2011\.03\.014 [↑](#footnote-ref-16)


60. <a id="footnote-3"></a>Fox, N\. & Smith, J\. et al\. \(2024\)\. Carbon\-14 Diamond Battery\. School of Chemistry, University of Bristol\. https://www\.bristol\.ac\.uk/chemistry/news/2024/carbon\-battery\.html [↑](#footnote-ref-3)


61. <a id="footnote-16"></a>Schreck, M\. & Voelkl, R\. \(2011\)\. A review of diamond synthesis by CVD processes\. Diamond and Related Materials, 20\(5\-6\), 620\-640\. https://doi\.org/10\.1016/j\.diamond\.2011\.03\.014 [↑](#footnote-ref-16)


62. <a id="footnote-14"></a>Nebel, C\. \(2020\)\. Nitrogen\-vacancy doped CVD diamond for quantum applications: A review\. Semiconductors and Semimetals, vol\. 103\. https://doi\.org/10\.1016/bs\.semsem\.2020\.03\.001 [↑](#footnote-ref-14)


63. <a id="footnote-6"></a>Thomas, J\. et al\. \(2023\)\. Betavoltaic Nuclear Battery: A Review of Recent Progress and Challenges as an Alternative Energy Source\. Journal of Physical Chemistry C, 127\(16\), 7565\-7579\. https://doi\.org/10\.1021/acs\.jpcc\.3c00684 [↑](#footnote-ref-6)


64. <a id="footnote-4"></a>Spencer, M\.G\. & Alam, T\. \(2019\)\. High power direct energy conversion by nuclear batteries\. Applied Physics Reviews, 6\(3\), 031305\. https://doi\.org/10\.1063/1\.5123163 [↑](#footnote-ref-4)


65. <a id="footnote-10"></a>Ambrosi, R\.M\. et al\. \(2019\)\. Safe radioisotope thermoelectric generators and heat sources for space applications\. Journal of Nuclear Materials, 377\(2\-3\), 506\-521\. https://doi\.org/10\.1016/j\.jnucmat\.2008\.03\.030 [↑](#footnote-ref-10)


66. <a id="footnote-10"></a>Ambrosi, R\.M\. et al\. \(2019\)\. Safe radioisotope thermoelectric generators and heat sources for space applications\. Journal of Nuclear Materials, 377\(2\-3\), 506\-521\. https://doi\.org/10\.1016/j\.jnucmat\.2008\.03\.030 [↑](#footnote-ref-10)


67. <a id="footnote-21"></a>Ekanem, E\. & Sanni, F\. \(2024\)\. Carbon\-14 Diamond Battery Operation and Applications\. UKAEA / IOM3 Materials World\. https://www\.iom3\.org/resource/world\-first\-carbon\-14\-diamond\-battery\.html [↑](#footnote-ref-21)


68. <a id="footnote-1"></a>Scott, T\.B\. et al\. \(2016\)\. Cabot Institute Annual Lecture: Diamond Battery Concept\. University of Bristol\. https://www\.bristol\.ac\.uk/cabot/what\-we\-do/diamond\-batteries/ [↑](#footnote-ref-1)


69. <a id="footnote-10"></a>Ambrosi, R\.M\. et al\. \(2019\)\. Safe radioisotope thermoelectric generators and heat sources for space applications\. Journal of Nuclear Materials, 377\(2\-3\), 506\-521\. https://doi\.org/10\.1016/j\.jnucmat\.2008\.03\.030 [↑](#footnote-ref-10)


70. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


71. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


72. <a id="footnote-12"></a>U\.S\. Congressional Research Service \(2024\)\. Considerations for Reprocessing of Spent Nuclear Fuel\. https://www\.congress\.gov/crs\-product/R48364 [↑](#footnote-ref-12)


73. <a id="footnote-12"></a>U\.S\. Congressional Research Service \(2024\)\. Considerations for Reprocessing of Spent Nuclear Fuel\. https://www\.congress\.gov/crs\-product/R48364 [↑](#footnote-ref-12)


74. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


75. <a id="footnote-2"></a>University of Bristol & UKAEA \(2024\)\. World's First Carbon\-14 Diamond Battery\. Press Release, 4 December 2024\. https://www\.bristol\.ac\.uk/news/2024/december/diamond\-battery\-media\-release\.html [↑](#footnote-ref-2)


76. <a id="footnote-11"></a>IAEA \(2019\)\. Status and Trends in Spent Fuel and Radioactive Waste Management\. https://www\.iaea\.org/newscenter/news/new\-iaea\-report\-presents\-global\-overview\-of\-radioactive\-waste\-and\-spent\-fuel\-management [↑](#footnote-ref-11)


77. <a id="footnote-13"></a>Market Reports World \(2024\)\. Nuclear Waste Recycling Market\. https://www\.marketreportsworld\.com/market\-reports/nuclear\-waste\-recycling\-market\-14718618 [↑](#footnote-ref-13)



