# Quantum Diamond Metamaterial Processor (QDMP): a theoretical framework for room-temperature quantum computing via CVD-engineered diamond metamaterials

*Theoretical proposal · Prepared for internal circulation — Advanced Systems Research Group · March 2026*

## Abstract

*We present a theoretical framework for the Quantum Diamond Metamaterial Processor \(QDMP\), a speculative room-temperature quantum computing architecture that combines the mature industrial base of chemical vapor deposition \(CVD\) diamond synthesis with emerging concepts in quantum metamaterials, topological qubit protection, and in-situ defect engineering. The QDMP concept proposes the use of engineered nitrogen-vacancy \(NV\) center arrays embedded in a metamaterial diamond lattice as a scalable, environmentally robust qubit platform. Building on documented advances in CVD production throughput, isotopic purification, and AI-assisted growth optimization, we outline a theoretical roadmap from current NV-center sensing capabilities toward a hypothetical device capable of operating at room temperature with coherence times exceeding 100 seconds. We identify seven fundamental scientific barriers that separate the theoretical proposal from physical realization, assess each against the current literature, and propose targeted research programs to address them. The QDMP framework serves as a structured thought experiment to guide investment in diamond quantum materials research and identify the most critical technological leverage points for room-temperature solid-state quantum computing.*

**Keywords:** *nitrogen-vacancy centers; CVD diamond; quantum metamaterials; topological qubits; room-temperature quantum computing; quantum error correction; Majorana zero modes; isotopic purification; quantum solitons; diamond photonics*

## 1. Introduction

The pursuit of room-temperature quantum computing represents one of the central grand challenges of modern physics and engineering. Current leading platforms—superconducting qubits, trapped ions, and photonic systems—each impose severe environmental constraints that impede scalable deployment. Superconducting qubits, which power IBM and Google's leading processors, require operation near absolute zero \(millikelvin temperatures\), demanding cryogenic infrastructure that consumes kilowatts of power and precludes miniaturization for tactical or embedded applications. Trapped-ion systems require ultra-high vacuum environments and precision laser systems that are inherently fragile. These constraints create a compelling design space for solid-state qubit platforms capable of ambient operation.

The nitrogen-vacancy \(NV\) center in diamond has long been recognized as a singular exception to the general requirement for extreme environmental isolation. \[1\] Unlike competing platforms, the NV center's spin triplet ground state—separated from higher-energy levels by a zero-field splitting of ≈2.87 GHz—permits coherent quantum control at room temperature, and even, under specialized protocols, up to 1000 K. \[3\] This robustness arises from diamond's unique combination of a wide 5.47 eV bandgap, ultralow nuclear spin density \(in isotopically purified ¹²C diamond\), and high Debye temperature, which together suppress the principal decoherence channels that plague other solid-state systems. \[5\]

Despite three decades of NV center research, coherence times in bulk diamond have reached only the millisecond regime under optimized conditions. \[7\] The central thesis of this paper is that reaching the second-to-minute coherence timescales required for fault-tolerant quantum computing will require a conceptual shift: from treating diamond as a passive substrate for isolated NV centers, to engineering the diamond itself as an active metamaterial—a crystallographically structured medium whose macroscopic quantum properties are designed into its atomic geometry during synthesis.

This idea is not entirely speculative in its foundations. The field of quantum metamaterials—defined as artificially engineered nanostructures containing coherent quantum elements that maintain global coherence \[11\]—has demonstrated, in superconducting systems, that engineering the electromagnetic environment of qubits through metamaterial design can dramatically extend effective coherence and enable novel coupling regimes. \[12\] Translating this paradigm to diamond requires solving a different, harder class of problem: engineering quantum structure into a covalently bonded crystal during its atomic assembly, rather than patterning it lithographically. The 2025 landscape of CVD diamond manufacturing—with global capacity exceeding 3,000 reactors, production cycles under five days, and AI-driven growth optimization—provides, for the first time, a manufacturable substrate on which to attempt this translation. \[9\]

In Section 2 we review the physical foundations of NV-center quantum coherence and establish the parameter regime the QDMP architecture must achieve. Section 3 presents the theoretical architecture, including the metamaterial lattice design, proposed topological protection mechanism, and control interface. Section 4 assesses the seven critical scientific barriers against the current literature, with explicit identification of what is established versus what is speculative. Section 5 provides a three-phase research roadmap, and Section 6 outlines estimated performance parameters for a hypothetical QDMP unit under ideal assumptions.

## 2. Physical Foundations of Diamond Quantum Coherence

## 2.1 The Nitrogen-Vacancy Center as a Qubit

The NV center consists of a substitutional nitrogen atom paired with an adjacent lattice vacancy along a \[111\] crystallographic axis, yielding a C₃ᵥ-symmetric defect with a spin-1 \(S=1\) electronic ground state. \[1\] In its negatively charged form \(NV⁻\), the relevant qubit subspace is formed by the ms = 0 and ms = ±1 spin projections of the ³A₂ triplet ground state. Optical pumping with 532 nm laser light initializes the NV spin into ms = 0 with >90% fidelity, exploiting a spin-selective intersystem crossing through a metastable singlet state. \[7\]

The spin Hamiltonian governing qubit dynamics is:

*H = D·Sz² \+ γₑ·B·S \+ Σᵢ Aᵢ·S·Iᵢ  \+  V\_strain*

where D ≈ 2.87 GHz is the zero-field splitting, γₑ is the electron gyromagnetic ratio, B is the external magnetic field, and the hyperfine sum couples the electron spin S to nearby nuclear spins Iᵢ with tensor Aᵢ. The final term Vstrain captures the sensitivity of the NV Hamiltonian to crystal strain, a property with significant implications for metamaterial design.

Coherence in bulk CVD diamond of natural ¹³C abundance is limited by the nuclear spin bath to T₂ ~ μs. Isotopic purification to >99.99% ¹²C removes this dominant noise source, pushing T₂ to ~1 ms and, with dynamical decoupling protocols, to the regime T₂ ≈ 0.5·T₁ ~ 3 ms at room temperature. \[7\] At cryogenic temperatures \(77 K\), T₁ approaches 1 second. \[7\] The theoretical QDMP target of T₂ > 100 seconds therefore requires suppressing decoherence by more than four orders of magnitude beyond the current isotopically-purified room-temperature state of the art. This is the central challenge the metamaterial architecture must address.

## 2.2 Diamond as a Quantum Material Platform

Diamond's exceptional physical properties extend well beyond its usefulness as an NV host. With a thermal conductivity of 22 W/cm·K \(the highest of any known material\), a critical breakdown field of 20 MV/cm, and chemical inertness across a temperature range from cryogenic to above 700°C, \[14\] diamond is an ideal substrate for quantum devices that must function in demanding operational environments. Its optical transparency from deep UV through mid-IR enables both excitation and readout of color centers. Its wide bandgap of 5.47 eV ensures that thermal populations of electronic excited states are negligible at room temperature. \[5\]

Beyond the NV center, diamond hosts an expanding zoo of quantum-optically active color centers. The silicon-vacancy \(SiV⁻\) center offers near-transform-limited optical emission from its zero-phonon line, facilitating photonic quantum network integration. \[13\] The tin-vacancy \(SnV⁻\) center combines high Debye-Waller factor with spin coherence times above 1 K. \[13\] These variants offer a design palette for engineering specific quantum properties into different regions of a composite metamaterial structure—NV centers for long coherence times and magnetic sensitivity, group-IV vacancies for photon emission and network connectivity.

## 2.3 Established Coherence Enhancement Techniques

Several techniques have been validated for extending NV coherence beyond the raw T₂ limit, providing building blocks the QDMP architecture would exploit:

Dynamical Decoupling \(DD\): Periodic microwave π-pulse sequences \(CPMG, XY-8, UDD\) effectively filter low-frequency noise, extending T₂ toward T₁. \[7\] With n = 32 DD pulses, decoherence from the ¹³C bath can be largely refocused.

Strain-Mediated Coherence Protection: Near the surface, the interaction of strain fields with applied magnetic fields can open spin-phonon-confined regimes that substantially increase T₂ for shallow NV centers. \[2\] This mechanism—tunable by crystal engineering—points toward the possibility of structurally programming coherence properties into the lattice itself.

Photonic Integration: Embedding NV centers in photonic crystal nanocavities strongly enhances emission into the zero-phonon line \(ZPL\) via the Purcell effect, enabling efficient spin-photon interfaces for quantum networking. \[5\] Inverse-designed diamond photonic structures have demonstrated cavity coupling sufficient for high-fidelity entanglement operations.

## 3. The QDMP Architecture: Theoretical Design

## 3.1 Core Concept: Quantum Engineering During CVD Growth

The QDMP framework proposes a fundamental departure from the prevailing paradigm of post-synthesis quantum device fabrication. Rather than growing diamond as a bulk material and subsequently implanting defects via ion bombardment—a process that introduces lattice damage and restricts defect density and spatial precision—the QDMP concept calls for engineering quantum properties during the CVD growth process itself.

CVD diamond synthesis proceeds by dissociating a carbon-bearing precursor gas \(typically CH₄ in H₂\) in a plasma, depositing carbon radicals onto a substrate in a layer-by-layer fashion. \[8\] The QDMP concept requires three extensions of this process: \(1\) controlled co-injection of nitrogen precursors at precisely timed intervals to create NV centers at specific depths; \(2\) application of patterned electromagnetic fields during growth to influence vacancy migration and NV complex formation; and \(3\) AI-supervised real-time adjustment of deposition conditions to maintain target lattice parameters during growth.

While each of these elements faces severe technical barriers \(detailed in Section 4\), their conceptual basis in known physics is sound. Ion-induced vacancy formation in diamond is well-characterized; nitrogen incorporation rates in CVD are tunable via precursor partial pressure; and AI-controlled CVD optimization for material quality \(though not quantum property targeting\) is already a feature of advanced manufacturing systems. \[9\]

## 3.2 The Metamaterial Lattice

The defining feature of the QDMP is the metamaterial diamond lattice: a CVD-grown diamond structure containing a three-dimensional periodic array of engineered functional elements, analogous in concept to the unit cell architecture of classical electromagnetic metamaterials but implemented at the atomic scale.

Quantum metamaterials, as defined in the recent literature, are artificially engineered nanostructures containing coherent quantum elements that maintain global coherence—their optical and electronic properties determined by the synergy between electromagnetic field modes and quantum effects in their constituent elements. \[11\] Current realizations of quantum metamaterials involve superconducting circuit arrays, cold atom lattices, and Josephson junction chains. \[12\] The QDMP proposes the first solid-state realization using engineered diamond defects as the quantum meta-atoms.

The proposed lattice unit cell contains: \(a\) a cluster of 3–5 NV centers in a spin-exchange-coupled arrangement, providing redundant qubit encoding; \(b\) an embedded microwave stripline waveguide section for qubit addressing; \(c\) an optical channel aligned to the \[100\] axis for photon-mediated coupling; and \(d\) a phononic bandgap region created by a periodic modulation of local strain to suppress the primary low-frequency phonon decoherence channel.

## 3.3 Topological Protection Mechanism

The QDMP's most ambitious element is its proposed topological protection scheme. Topological quantum computing exploits the non-local encoding of quantum information in the braiding of quasiparticles—Majorana zero modes \(MZMs\)—whose degeneracy is protected by a topological energy gap rather than by environmental isolation alone. \[10\] Microsoft's Majorana 1 processor, unveiled in February 2025, demonstrated for the first time that topological qubits can be realized in a semiconductor-superconductor nanowire hybrid platform, achieving hardware-level error suppression.

The QDMP proposes a diamond-native analogue: engineering strain fields and electromagnetic mode patterns in the metamaterial lattice to create topological phases among the coupled NV cluster spin states. The physical mechanism invoked is analogous to the topological phase transitions studied in condensed matter simulation experiments on superconducting circuits, \[15\] where engineered Hamiltonians with topological invariants can be realized without requiring topological material phases to exist in the unengineered diamond bulk.

We note explicitly that this proposed mechanism has no experimental precedent in diamond and involves several layers of theoretical assumptions that remain unvalidated. Its inclusion is justified as a theoretical target, not a realized capability.

## 3.4 Quantum Soliton Information Carriers

As an alternative or complementary protection mechanism, the QDMP framework proposes encoding logical qubit information in spin-wave solitons—topologically stable, self-reinforcing wave packets in the coupled NV spin lattice. Solitonic quantum states have been proposed as information carriers in one-dimensional spin chains, where the topological winding number of a spin texture provides a discrete conserved quantity immune to smooth perturbations.

In the QDMP lattice, the periodic arrangement of NV clusters creates an effective spin chain along each crystallographic axis. A spin soliton—a domain wall between two topologically distinct NV spin configurations—would propagate through this lattice under microwave drive while preserving its topological quantum number. This mechanism, if realizable, would provide passive error suppression without active error correction overhead.

Solitonic quantum information carriers remain a theoretical proposal in this context. While solitons are well-characterized in classical nonlinear lattices and have been proposed in quantum spin chains, no experimental observation in a solid-state spin system at room temperature has been reported.

## 4. Critical Scientific Barriers and Current Research Status

A rigorous assessment of the QDMP proposal requires explicit identification and quantification of the scientific barriers separating theory from realization. We identify seven barriers of decreasing severity:

## Barrier 1: Coherence Time Extension — Four Orders of Magnitude

The most basic performance requirement for the QDMP—T₂ > 100 s at room temperature—exceeds the best published room-temperature NV coherence time by ~10⁴. While isotopic purification has increased T₂ from ~μs to ~ms, the path from ms to 100 s is not simply a continuation of this trend. It requires eliminating or circumventing multiple independent decoherence channels that become dominant as lower-order noise is suppressed: electric field noise, phonon coupling, surface adsorbates, and charge fluctuations.

Current theoretical work shows that, near clock transitions \(avoided crossings in the NV spin spectrum\), the spin becomes first-order insensitive to magnetic field fluctuations. \[2\] Strain-mediated coherence protection may similarly cancel specific phonon modes. Whether all room-temperature decoherence channels can be simultaneously suppressed remains an open question of fundamental physics.

## Barrier 2: Precise Defect Positioning During CVD Growth

Achieving the metamaterial unit cell geometry requires positioning NV centers with ~1 nm precision in three dimensions during CVD growth—a precision six to seven orders of magnitude beyond current CVD process control. The surface kinetics of CVD deposition are stochastic at the atomic scale, and while parameters such as temperature, pressure, and gas flow ratios can be controlled, they determine ensemble statistics of defect formation, not individual positions.

The field of materials for quantum technologies identifies deterministic spin qubit fabrication as the central overarching challenge for solid-state quantum systems. \[16\] Laser-induced activation currently offers the highest spatial precision for NV creation \(~20 nm\), still well short of the sub-nm requirement for the QDMP lattice. \[16\]

## Barrier 3: Topological Phases in Diamond — Not Yet Demonstrated

No topological phase has been observed in bulk diamond or in NV center spin lattices. The realization of topological phases in superconductor-semiconductor hybrids \(as in the Majorana 1 processor\) required specific material engineering—InAs nanowires proximitized with Al superconducting films—and operates at millikelvin temperatures. \[10\] Translating topological protection to diamond at room temperature requires identifying a mechanism by which the necessary non-Abelian braiding statistics can emerge in a spin system without a superconducting pairing term.

Theoretical proposals exist for synthetic topological phases in quantum spin lattices with engineered coupling terms. Realizing these in diamond would constitute a fundamental discovery in condensed matter physics in its own right.

## Barrier 4: Quantum Metamaterial Coherence in Diamond — Early Stage

The concept of quantum metamaterials—materials whose macroscopic properties are governed by engineered quantum coherence in their constituent elements \[11\]—is well-established in the context of superconducting circuits, where Josephson junction arrays realize tunable quantum media for quantum computing applications. \[12\] However, all current quantum metamaterial realizations are lithographically patterned planar circuits operating at cryogenic temperatures. The extension to three-dimensional crystallographic quantum metamaterials at room temperature is, to our knowledge, without experimental precedent.

## Barrier 5: Real-Time Quantum State Monitoring During CVD

The QDMP manufacturing paradigm requires feedback on quantum properties—spin coherence, entanglement fidelity—during active crystal growth, to allow AI-driven process adjustment. Current in-situ CVD monitoring capabilities are limited to bulk optical properties \(transmission, reflectance\) and gas-phase species concentrations. No technique exists for measuring individual spin coherence times in a growing crystal. Optically detected magnetic resonance \(ODMR\), the standard NV characterization method, \[6\] requires cooling the sample and isolating individual centers—incompatible with active deposition.

## Barrier 6: Scaling — From a Unit Cell to 10¹⁴ Qubits/cm³

Even granting the ability to create a single functional QDMP unit cell, scaling to the proposed 10¹⁴ qubits/cm³ density requires maintaining quantum coherence across a macroscopic lattice of ~10¹⁴ coupled centers. Collective decoherence mechanisms—superradiance, phonon-mediated correlations, charge noise from defect clusters—typically scale unfavorably with system size, and are poorly understood in dense coupled spin systems at room temperature.

## Barrier 7: Classical-Quantum Interface

The interface between topological qubits and conventional electronics remains poorly characterized even in the best-studied superconducting topological systems. For the QDMP, addressing individual qubits within a 10¹⁴/cm³ array via microwave or optical fields requires sub-wavelength spatial selectivity that is not achievable with standard far-field techniques, and would require near-field or plasmonic addressing architectures not yet demonstrated at the required scale or fidelity.

## 5. Three-Phase Research Roadmap

## Phase I: Foundational Coherence Engineering \(Years 1–5\)

Phase I objectives do not require any advances in CVD precision beyond the current state of the art. They instead focus on maximizing coherence in existing high-purity diamond samples through strain engineering, surface passivation, and metamaterial-inspired electromagnetic environment design:

\(a\) Strain-field mapping and engineered coherence protection: Systematic experimental and first-principles study of strain-T₂ correlations in isotopically purified diamonds, building on the theoretical framework in reference \[2\]. Target: identify strain configurations that suppress the dominant room-temperature decoherence channel.

\(b\) NV-center array coherence in 2D: Fabricate ordered 2D NV arrays \(10×10 to 100×100\) via laser-activation with nm-scale positioning and characterize collective coherence properties. Identify signatures of correlated spin dynamics that foreshadow the 3D metamaterial regime.

\(c\) Photonic environment engineering: Embed NV-center arrays in inverse-designed photonic crystal cavities to test whether engineered electromagnetic density of states can suppress phonon-mediated decoherence, as proposed in the quantum metamaterial literature \[12\].

## Phase II: CVD Quantum Engineering \(Years 5–10\)

Phase II attacks Barrier 2 directly, developing techniques for controlled NV positioning during CVD growth:

\(a\) Patterned nitrogen-seeded growth: Develop nitrogen-selective surface chemistry to create preferential NV nucleation sites with 10–20 nm pitch, using templated CVD substrates. This is a materials science challenge, not a fundamental physics barrier.

\(b\) In-situ ensemble coherence monitoring: Develop optical techniques for monitoring NV spin ensemble properties during CVD, providing feedback for process control. Suitable methods may include luminescence lifetime mapping and microwave-assisted growth modulation.

\(c\) Prototype quasi-1D spin chains: Grow quasi-1D NV arrays in diamond nanowires and characterize their collective spin dynamics for signatures of topological spin textures.

## Phase III: Metamaterial Diamond Devices \(Years 10–20\+\)

Phase III represents a convergence of results from Phases I and II into prototype devices:

\(a\) 3D metamaterial unit cell demonstration: Grow and characterize a single-unit-cell quantum metamaterial diamond region with verified quantum coupling between NV clusters.

\(b\) Topological phase search: Systematically probe coupled NV lattices for signatures of non-trivial topological order, guided by theoretical models developed in Phase I.

\(c\) Error-corrected logical qubit demonstration: Demonstrate a single room-temperature logical qubit encoded across multiple physical NV centers with error rate below the fault-tolerance threshold.

## 6. Theoretical Performance Parameters

Under the optimistic assumption that all seven scientific barriers are resolved, we project the following performance parameters for a 1 cm³ QDMP unit. These numbers should be understood as theoretical upper bounds under ideal assumptions, not engineering predictions:

**Parameter**

**Current Best**

**QDMP Target**

Room-temperature T₂

~3 ms \(DD-enhanced\)

>100 s

Qubit density \(per cm³\)

~10⁸ addressable NV

10¹⁴ logical

Native error rate

~10⁻³ \(NV gates\)

10⁻⁶

Operating temperature range

4 K – 700 K \(NV sensing\)

-200°C to \+500°C

Power consumption \(control\)

Watts \(NV experiments\)

~50 mW \(target\)

Thermal conductivity

22 W/cm·K \(diamond\)

22 W/cm·K

Coherence temperature upper limit

~700 K \(standard\)

>1000 K \(target\)

*Table 1. Comparison of current NV-center performance against theoretical QDMP targets. Current values drawn from published literature \[1,2,3,5,7\]. QDMP targets assume resolution of all seven identified scientific barriers.*

## 7. Conclusion

The QDMP framework represents a structured theoretical proposal at the intersection of three maturing fields: CVD diamond manufacturing, \[8\] quantum metamaterials, \[11\] and NV-center quantum technology. \[1\] Its primary scientific value is not as a near-term engineering blueprint, but as a coherent long-range target that organizes an otherwise fragmented research landscape.

The seven barriers identified here are not equivalent in their difficulty. Barrier 1 \(coherence extension\) and Barrier 3 \(topological phases in diamond\) require fundamental physics discoveries of the first rank. Barrier 2 \(CVD positioning precision\) is a hard engineering problem that may yield to incremental progress in surface-chemistry-directed nucleation. Barriers 5, 6, and 7 are primarily engineering challenges whose difficulty depends critically on the physics outcomes of addressing Barriers 1–4.

The proposal's most important practical contribution may be its identification of strain-mediated coherence engineering \[2\] as the most tractable near-term leverage point: this mechanism operates within the physics of existing CVD diamond and requires no new materials breakthroughs, yet points toward coherence enhancement strategies that could, combined with dynamical decoupling, close the gap between the current ~3 ms room-temperature T₂ and the regime—perhaps 1–10 seconds—where fault-tolerant quantum algorithms first become feasible at room temperature.

The QDMP as described—a room-temperature, 10⁶-logical-qubit, century-lifespan device manufacturable in 24 hours at $500 per unit—remains science fiction. But the path leading toward it, even if it terminates well short of that destination, passes through science that is worth doing.

## References
**\[1\]  **Doherty, M.W., Manson, N.B., et al. \(2013\). The nitrogen-vacancy colour centre in diamond. Physics Reports, 528\(1\), 1–45.

**\[2\]  **Häberle, T., et al. \(2025\). A coherence-protection scheme for quantum sensors based on ultra-shallow single nitrogen-vacancy centers in diamond. Nature Communications. https://doi.org/10.1038/s41467-025-64771-7

**\[3\]  **Liu, G.-Q., et al. \(2019\). Coherent quantum control of nitrogen-vacancy center spins near 1000 kelvin. Nature Communications, 10, 1344.

**\[4\]  **Wang, N. & Cai, J. \(2024\). Hybrid quantum sensing in diamond. Frontiers in Physics, 12, 1320108.

**\[5\]  **Gschwendtner, M., et al. \(2025\). Recent progress in hybrid diamond photonics for quantum information processing and sensing. Communications Engineering.

**\[6\]  **Sangtawesin, S., et al. \(2019\). Quantum control for nanoscale spectroscopy with diamond nitrogen-vacancy centers. Frontiers in Physics, 8, 610868.

**\[7\]  **Rondin, L., et al. \(2014\). Magnetometry with nitrogen-vacancy defects in diamond. Reports on Progress in Physics, 77, 056503.

**\[8\]  **Balmer, R.S., et al. \(2009\). Chemical vapour deposition synthetic diamond: materials, technology and applications. Journal of Physics: Condensed Matter, 21\(36\), 364221.

**\[9\]  **Allied Market Research. \(2025\). Lab Grown Diamond Market By Manufacturing Method: Global Opportunity Analysis and Industry Forecast, 2023–2032.

**\[10\]  **Microsoft Station Q / Aghaee, M. et al. \(2025\). Interferometric single-shot parity measurement in an InAs–Al hybrid device. Nature. \[Majorana 1 Processor\]

**\[11\]  **Uriri, S., Ismail, Y., Mafu, M. \(2025\). Quantum metamaterials: Applications in quantum information science. APL Quantum, 2\(2\), 021501.

**\[12\]  **Martínez, J.P., et al. \(2025\). Metamaterials in Superconducting and Cryogenic Quantum Technologies. arXiv preprint arXiv:2506.20047.

**\[13\]  **Orphal-Kobin, L., et al. \(2024\). Coherent Microwave, Optical, and Mechanical Quantum Control of Spin Qubits in Diamond. Advanced Quantum Technologies.

**\[14\]  **Liang, W., et al. \(2024\). A Review of Diamond Materials and Applications in Power Semiconductor Devices. PMC/MDPI Electronics.

**\[15\]  **Xiang, Z.-L., et al. \(2025\). Advancements in superconducting quantum computing. National Science Review.

**\[16\]  **Bhave, S., et al. \(2024\). Materials for Quantum Technologies: a Roadmap for Spin and Topology. Oxford Open Materials Science.
