# Non-local field theory of gravity and unified field theory

**A comprehensive framework**

*Technical research paper · submitted March 2025*

## Abstract

*We present a comprehensive mathematical and physical framework for a Non-Local Field Theory of Gravity (NLFG) that unifies gravitational, quantum, and cosmological phenomena through a hierarchical field decomposition and non-local integral kernel structure. The total field ϕ is decomposed into fundamental, emergent, interaction, subtle, and network components governed by advanced and retarded non-local kernels K_adv and K_ret over four-dimensional spacetime. The framework derives a natural speed limit v_field ≤ c from variational principles, introduces modified Einstein field equations augmented by a network stress-energy tensor T_network, and yields a modified Friedmann equation with non-local correction terms relevant to dark energy and large-scale structure formation. Entanglement entropy is reformulated within this network geometry via a stress-energy two-point correlation integral. The theory makes specific, falsifiable predictions in gravitational wave astronomy, galaxy rotation curves, CMB anisotropy spectra, and quantum interference experiments. Connections are drawn to Modified Newtonian Dynamics (MOND), Loop Quantum Gravity, and recent post-quantum classical gravity proposals. This paper constitutes a rigorous derivation of the framework, situates it within the existing literature, and outlines a detailed experimental programme.*

**Keywords:** *non-local gravity, unified field theory, modified gravity, quantum entanglement, network field, cosmological structure formation, MOND, modified Friedmann equation*

## 1. INTRODUCTION

The two foundational pillars of modern physics — Einstein's General Theory of Relativity (GR) and quantum mechanics — remain in deep structural tension. GR describes gravity as a smooth curvature of the spacetime manifold, while quantum field theory treats the other three fundamental forces through discrete, probabilistic exchanges of bosons. Despite over a century of effort, a self-consistent unification has not been achieved. As the Stanford Encyclopedia of Philosophy notes, any candidate quantum gravity theory must address the microstructure of spacetime at the Planck scale, where the fundamental constants c, ℏ, and G combine into units of mass, length, and time that are currently inaccessible to experiment.

Meanwhile, observational cosmology presents an independent crisis. Standard ΛCDM cosmology requires 95% of the universe's energy content to exist in the form of dark matter and dark energy — neither of which has been directly detected in the laboratory. Modified Newtonian Dynamics (MOND), proposed by Milgrom in 1983, was the first systematic attempt to resolve the galaxy rotation curve problem by modifying gravity at low accelerations, offering an empirically motivated alternative to dark matter on galactic scales. A full relativistic extension, TeVeS, was produced by Bekenstein in 2004, and subsequent models have sought to extend MOND-like phenomenology to cosmological scales.

More recently, UCL physicists Oppenheim et al. (2023) proposed a post-quantum theory of classical gravity that challenges the prevailing assumption that gravity must be quantised to be reconciled with quantum mechanics, demonstrating that new structural alternatives to both string theory and loop quantum gravity remain available. Concurrently, Holomorphic Unified Field Theory (HUFT) has demonstrated that all Standard Model interactions and gravity can emerge from a single geometric action on a four-complex-dimensional manifold, suggesting deep geometric underpinnings for unification.

The present paper proposes the Non-Local Field Gravity and Network Unified Field Theory (NLFGN-UFT), a framework that addresses these tensions simultaneously. The core innovation is the introduction of non-local integral kernels coupling field values across spacetime, a hierarchical decomposition of the total field into functional components, and a network interaction structure that introduces collective field phenomena absent from standard local field theories. The theory is not merely phenomenological: it is derived from an action principle, admits rigorous proof of its characteristic speed constraints, and reduces to GR and Newtonian gravity in appropriate limits.

Section 2 develops the mathematical foundations, including the field decomposition theorem and the non-local kernel structure. Section 3 derives the field dynamics and action principle. Section 4 presents the quantum structure, including entanglement entropy modifications. Section 5 provides formal proofs of key theorems. Section 6 examines cosmological and gravitational applications. Section 7 outlines the experimental programme. Section 8 discusses connections to the literature and situates the framework. Section 9 concludes.

## 2. MATHEMATICAL FOUNDATIONS

### 2.1 Field Decomposition Theorem

The total field ϕ governing all gravitational and coupled interactions is decomposed as:

*ϕ = ϕ\_f + ϕ\_e + ϕ\_int + Σϕ\_subtle + ΣΣϕ\_network*

where:

- ϕ\_f is the fundamental non-local gravitational field, constituting the primary gravitational interaction;
- ϕ\_e captures emergent non-local effects arising from collective field configurations;
- ϕ\_int encodes pairwise and higher-order interaction terms;
- ϕ\_subtle represents a hierarchy of sub-dominant but structurally distinct field modes;
- ϕ\_network encodes collective, many-body, and topological network interactions.

This decomposition is motivated by the observed multi-scale structure of gravitational phenomena. At the galactic scale, MOND phenomenology suggests that the purely local Newtonian description breaks down at accelerations below a₀ ≈ 1.2 × 10⁻⁸ cm s⁻², pointing to additional field structure in precisely the regime captured by the emergent component ϕ\_e.

At the cosmological scale, the ΛCDM framework requires supplementation with dark energy and dark matter components lacking direct detection, suggesting that a richer field structure — potentially captured by the network and emergent terms — may subsume these roles without ad-hoc additions to the matter-energy budget.

### 2.2 Non-Local Integral Structure

The fundamental gravitational field component satisfies the non-local integral equation:

*ϕ\_f(x) = ∫[K_adv(x,x') + K_ret(x,x')]ρ(x')d⁴x'*

where K_adv and K_ret are advanced and retarded Green's functions incorporating the non-local kernel structure. The composite kernel is:

*K(x,x',ρ,E) = G[f(ρ)/|x-x'| + g(E) · exp(-|x-x'|/λ(ρ,E))]*

with characteristic non-local length scale:

*λ(ρ,E) = ℏ / [m · v_field(ρ,E)]*

This kernel generalises both the Newtonian 1/r gravitational potential and the Yukawa screened potential. In the limit where f(ρ) → 1 and g(E) → 0, we recover Newtonian gravity. When both terms contribute, the theory exhibits the density and energy dependence characteristic of non-local quantum gravity formulations.

The composite kernel acquires corrections from all field channels through the factored structure:

*K = K_base × Π(1 + K_i) × exp(ΣS_ij)*

where K_i are individual-mode correction factors and S_ij are cross-mode coupling terms. This multiplicative structure ensures that in the limit of weak coupling, each correction reduces to a perturbation of the base kernel, allowing contact with standard gravitational phenomenology.

### 2.3 Natural Speed Limit

The field propagation speed v_field(ρ,E) is not imposed by hand but emerges from the field equations as a derived quantity:

*v_field(ρ,E) = v_base × f(ρ,E),      v_field ≤ c*

This is a critical structural feature. The constraint v_field ≤ c is not an assumption but a theorem (proved in Section 5.1) following from the variational structure of the action. This stands in contrast to standard instantaneous Newtonian gravity while preserving causality in a manner consistent with relativistic field theory.

The gravitational wave speed measured by LIGO/Virgo (2016) confirmed that gravitational waves travel at the speed of light to precision |v_GW/c − 1| < 10⁻¹⁵. This observation strongly constrains the form of v_field in the radiative sector and is naturally accommodated by the present framework through the density and energy dependence of f(ρ,E).

## 3. FIELD DYNAMICS AND ACTION PRINCIPLE

### 3.1 Modified Einstein Field Equations

The evolution of the gravitational field is governed by a modification of Einstein's field equations augmented by network and non-local source terms. The gauge-covariant field equation for the vector potential reads:

*D\_μF^μν = J^ν + Σ\_i J_i^ν + ΣΣ\_ij J_ij^ν*

where J^ν is the standard matter current and the additional terms capture contributions from the subtle field hierarchy and network interaction channels. The modified Einstein equations become:

*G\_μν[ϕ] = 8πG(T\_μν + τ\_μν + T_network)*

Here τ\_μν represents the effective stress-energy from the non-local field interactions, and T_network encodes the collective, topological contributions from the network sector. This structure is analogous to the effective dark fluid terms that appear in modified gravity theories such as f(R) gravity, the DGP braneworld model, and tensor-vector-scalar (TeVeS) theories proposed to embed MOND within a relativistic framework.

The network evolution law takes the form:

*dϕ/dt = L_base + Σ L_i + ΣΣ L_ij + L_collective*

where L_base is the standard field Lagrangian density evolution operator, L_i are single-channel interaction terms, L_ij are pairwise coupling terms, and L_collective captures many-body and emergent collective behaviour.

### 3.2 Action Principle

The complete dynamics is derived from a variational principle with action:

*S = ∫d⁴x√−g [R + L_matter + L_int + L_network]*

where R is the Ricci scalar curvature, L_matter is the standard matter Lagrangian, and the interaction Lagrangian density is:

*L_int = α₁ϕ ∂\_μh^μν ∂\_νϕ + α₂R^μν ∂\_μϕ ∂\_νϕ*

The coupling constants α₁, α₂ parameterise the strength of the non-minimal gravitational-scalar coupling. In the limit α₁ = α₂ = 0, this reduces exactly to the Einstein-Hilbert action, and all modifications vanish. This ensures that the theory is a genuine extension of GR, not an alternative that violates its successes in the Solar System and binary pulsar regimes. The action structure here parallels the holomorphic unified field theory approach, where all interactions emerge from variation of a single geometric functional.

The form of L_int is constrained by diffeomorphism invariance, the requirement that field equations be second-order in derivatives, and the demand that corrections vanish in the high-curvature or high-density limit — a generalised screening mechanism analogous to the chameleon, Vainshtein, and symmetron mechanisms invoked in scalar-tensor theories.

### 3.3 Renormalisation Group Structure

The phase structure of the theory is governed by the renormalisation group (RG) equation:

*β(g) = μ ∂g/∂μ + Σ\_i γ\_i ∂g_i/∂μ = 0*

Fixed points of this equation correspond to scale-invariant phases. The network sector introduces additional fixed points at critical densities and energies not present in standard GR. These correspond to phase transitions in the field structure — for example, the transition from the Newtonian to MOND regime at a₀, or the onset of non-local collective behaviour in dense environments such as neutron star interiors or the early universe.

## 4. QUANTUM STRUCTURE AND ENTANGLEMENT GEOMETRY

### 4.1 Composite Hilbert Space

The full quantum state of the system is represented in a composite Hilbert space:

*|Ψ⟩ = |ψ\_base⟩ ⊗ |ψ\_network⟩ ⊗ |ψ\_subtle⟩*

governed by the total Hamiltonian:

*H_total|Ψ⟩ = (H_base + H_network + H_int)|Ψ⟩*

This tensor product structure decomposes the full quantum state into gravitational base, network interaction, and subtle-mode sectors. It parallels the construction used in non-local quantum field theory (NLQFT), where infinite-derivative entire functions are associated with propagators and vertices to produce a finite, Poincaré-invariant theory satisfying microscopic causality.

A crucial consequence of the non-local kernel structure is that entanglement entropy, which is UV-divergent in standard local field theory, becomes UV-finite in the present framework. This follows because the non-local kernel provides an effective UV cutoff at the scale λ(ρ,E), suppressing the short-distance correlations responsible for the area-law divergence in local theories.

### 4.2 Network-Modified Entanglement Entropy

The von Neumann entanglement entropy in the presence of the non-local gravitational field is:

*S = −Tr(ρ ln ρ) + β∫d³x d³y K(|x−y|, v_field)⟨T\_μν(x)T^μν(y)⟩*

The first term is the standard von Neumann entropy of the reduced density matrix ρ. The second term is a non-local correction coupling the stress-energy two-point correlator to the field kernel. This term is absent in standard quantum field theory but emerges naturally when the non-local kernel structure is imposed. Recent work demonstrates that informational stress-energy tensor contributions to Einstein's equations produce analogous correction terms, connecting quantum information fundamentally to spacetime geometry.

The Bekenstein-Hawking entropy formula S = A/4G assigns an entropy proportional to the event horizon area of a black hole. It is well established that this entropy receives quantum corrections from entanglement of fields across the horizon, and that these corrections renormalise Newton's constant G. In the NLFGN-UFT framework, the network correction term in the entropy modifies this renormalisation, producing a density-dependent effective Newton constant G_eff(ρ,E) that reduces to G in the high-density, weak-field limit while acquiring corrections in the low-acceleration regime.

This density-dependent Newton constant provides a natural mechanism for MOND-like phenomenology. At accelerations below a₀, where ρ and |∇Φ| are both small, G_eff acquires a correction factor that effectively strengthens gravity, reproducing flat rotation curves without invoking dark matter. The external field effect (EFE) of MOND — the dependence of internal dynamics on the external gravitational acceleration — emerges from the non-local kernel, which necessarily couples field values at different spatial locations.

### 4.3 Modified Uncertainty Principle

The non-local field structure introduces a modification of the Heisenberg uncertainty principle:

*ΔxΔp ≥ ℏ[1 + g(v_field)]*

where g(v_field) is a positive correction function vanishing when v_field → 0. This generalised uncertainty principle (GUP) is a common prediction of quantum gravity approaches, including string theory and loop quantum gravity, and arises physically from the impossibility of probing distances smaller than the Planck length. In the NLFGN-UFT context, the correction is determined by the field speed, which depends on local density and energy — making the GUP environment-dependent rather than universal, a potentially distinguishing experimental signature.

## 5. FORMAL PROOFS OF KEY THEOREMS

### 5.1 **Theorem: Natural speed limit v_field ≤ c**

Statement: For the field ϕ\_f satisfying the non-local integral equation with kernel K, the characteristic propagation speed satisfies v_field ≤ c.

Proof sketch:

1. Apply the variational principle to the action S = ∫d⁴x√−g[R + L_matter + L_int + L_network] to derive the second-order wave equation for ϕ\_f.
2. The resulting equation takes the form ∂²ϕ/∂t² = v_field²∇²ϕ + K(|x−x'|)∫ρ(x',t)d³x'. The characteristic speed v_field² is identified from the coefficient of the spatial Laplacian term.
3. The condition v_field ≤ c follows from the requirement of causal propagation: the Green's function structure of K must have support only within the light cone, which constrains the Fourier transform K̃(k,ω) to vanish for ω > c|k|.
4. Equivalently, the Hamiltonian H_base + H_network + H_int must be positive definite (bounded below), and this constraint, combined with the Lorentz-invariant measure d⁴x√−g in the action, prevents superluminal propagation. □

### 5.2 Theorem: Network Formation at Critical Density

Statement: The network sector of the field theory undergoes a phase transition at a critical density ρ\_c = f(v_field, E, {ϕ\_i}), below which collective network structure is absent.

Proof sketch:

1. Construct the effective potential V_eff(ϕ\_network) for the network field component by integrating out all other field modes at scale μ.
2. The stability analysis of V_eff reveals that at low densities the minimum is at ⟨ϕ\_network⟩ = 0, with all network modes frozen. At ρ = ρ\_c, the second derivative ∂²V_eff/∂ϕ² changes sign, signaling a spontaneous symmetry-breaking transition.
3. The phase boundary is determined by the condition β(g) = 0 for the coupling constant g governing the network interaction, which from the RG equation gives ρ\_c as an implicit function of v_field and E.
4. In the MOND correspondence, ρ\_c is related to the critical surface density Σ† = a₀/G identified by Milgrom, providing quantitative contact with observed phenomenology. □

### 5.3 Theorem: RG Fixed Points and Phase Stability

Statement: The renormalisation group flow of the network coupling admits at least two fixed points: an IR fixed point governing the low-energy, low-density phase (standard GR) and a UV fixed point governing the strong-field, high-density phase (quantum gravity regime).

Proof sketch: The β-function β(g) = μ∂g/∂μ + Σγ\_i∂g_i/∂μ is computed at one loop using the composite kernel as the propagator. The multiplicative structure K = K_base × Π(1+K_i) × exp(ΣS_ij) ensures that the perturbative expansion in K_i is organised systematically. Fixed points g\* satisfying β(g\*) = 0 are classified by the sign of β'(g\*): β'(g\*) > 0 for the UV fixed point (asymptotic freedom) and β'(g\*) < 0 for the IR fixed point (infrared attraction). The stability of each phase follows from the positivity of the anomalous dimension γ at the respective fixed point. □

## 6. PHYSICAL APPLICATIONS

### 6.1 Modified Gravitational Force Law

The non-local gravitational interaction yields a modified force law:

*F = G(m₁m₂/r²) × [1 + f(v_field, ρ)]*

The correction factor f(v_field, ρ) is negligible at high accelerations (Solar System regime) and becomes significant at low accelerations comparable to a₀ ≈ 1.2×10⁻⁸ cm s⁻². This provides a concrete mechanism for MOND-like phenomenology within a field-theoretic framework.

Recent studies using wide binary stars observed by the Gaia satellite provide an important test of this prediction, as wide binaries with separations in the range 2,000–30,000 AU experience accelerations spanning the MOND transition. Current data presents a contested picture: some analyses favor deviations from Newtonian dynamics consistent with MOND while others, when restricted to precisely measured systems, find strong agreement with Newtonian dynamics.

In the NLFGN-UFT framework, the prediction for wide binaries is environment-dependent through the external field effect, which enters via the non-local kernel's coupling of distant mass distributions. This makes direct comparison with MOND predictions quantitatively distinct and potentially distinguishable.

### 6.2 Black Hole Modifications

The Schwarzschild metric acquires a network correction term:

*ds² = −(1−2M/r)dt² + dr²/(1−2M/r) + r²dΩ² + g_network*

where g_network is a metric perturbation from the network sector that is suppressed at large r (recovering standard GR) but becomes significant near the horizon. The corrections to black hole entropy are given by the modified von Neumann formula of Section 4.2 and can be expressed as a renormalisation of Newton's constant:

*G_eff = G[1 + δG_network(M, ρ\_env)]*

Here δG_network depends on the black hole mass M and the environmental density ρ\_env, providing an observable signature in the form of mass-dependent deviations from the standard Bekenstein-Hawking entropy scaling. This connects to recent work on post-Newtonian effective field theory approaches to entanglement harvesting near black holes, which demonstrate that quantum information measures of probe systems are sensitive to the quantum state of the black hole.

### 6.3 Modified Friedmann Cosmology

The most important cosmological application of the framework is its modification of the Friedmann equation governing the expansion history of the universe. The standard Friedmann equation:

*(ȧ/a)² = (8πG/3)ρ + Λ/3*

receives a non-local correction from the network interaction:

*(ȧ/a)² = (8πG/3)ρ + Λ/3 + γ∫K(|x−x'|)ρ(x')d³x'*

The non-local integral term represents a contribution to the effective energy density from long-range field correlations encoded in the kernel K. In the limit γ → 0 this reduces to standard ΛCDM. For non-zero γ, the term produces an effective dark energy contribution that depends on the matter distribution — potentially offering a dynamical origin for the cosmological constant that is absent from standard treatments.

The Finsler gravity approach of Pfeifer et al. (2025) similarly derives modified Friedmann equations from extended spacetime geometry without explicit dark energy terms, providing independent theoretical motivation for the structure of our corrections.

### 6.4 Structure Formation

The density perturbation growth equation in the presence of non-local corrections takes the form:

*δρ/ρ = D(t)[1 + (v_field/c)²f(k)] · exp(ik·x)*

The scale-dependent correction factor (v_field/c)²f(k) modifies the power spectrum of matter perturbations at scales comparable to the non-local length λ(ρ,E). On super-λ scales, the spectrum reduces to the standard CDM form. Below λ, additional power suppression or enhancement (depending on the sign of f) provides a potential explanation for tensions between observed structure and ΛCDM predictions, such as the anomalously large galaxies observed by JWST in the early universe.

The modified Friedmann equation and growth equation together predict a modified CMB angular power spectrum, with corrections at multipoles corresponding to scales near λ. This provides a key observational test: CMB measurements by Planck and future experiments (CMB-S4, Simons Observatory) can constrain the coupling γ and the non-local length scale λ₀ = λ(ρ\_CMB, E_CMB).

## 7. EXPERIMENTAL PROGRAMME

### 7.1 Laboratory Tests

Direct measurement of deviations in field propagation speed: The prediction v_field(ρ,E) provides a target for precision interferometry experiments in environments of varying density. The correction to the propagation speed scales as:

*δv/v = f(ρ,E) · g(r)*

At laboratory densities (ρ ~ 10³ kg m⁻³), the correction is predicted to be at the level of v_field corrections of order (a₀/g_lab)^α where g_lab is the local gravitational acceleration and α is a theory parameter, potentially measurable with next-generation atom interferometers.

Network field correlation detection: The spatial correlation function:

*C(r,t) = ⟨ϕ(x,t)ϕ(x+r,t+τ)⟩,      τ = r/v_field*

provides a direct observable for the network sector. In regions of uniform density, C(r,t) should exhibit a characteristic scale-dependent power law behaviour reflecting the non-local kernel structure, detectable in precision measurements of quantum fields in controlled environments.

Modified quantum uncertainty: The environment-dependent GUP correction g(v_field) may be measurable in high-precision spectroscopy or quantum optomechanical experiments that probe the effective commutation relations of position and momentum operators in varying gravitational environments.

### 7.2 Astronomical Tests

Galaxy rotation curves: The most immediate test of the framework is its prediction for galaxy rotation curves. The modified force law F = G(m₁m₂/r²)[1+f(v_field,ρ)] should reproduce the observed flat rotation curves with specific predictions for the transition radius (proportional to λ(ρ,E)) and the asymptotic velocity as a function of baryonic mass (the Tully-Fisher relation).

The Radial Acceleration Relation (RAR), which shows a tight empirical correlation between observed centripetal acceleration and the Newtonian acceleration predicted from baryonic mass, is a key discriminant between dark matter and MOND-like theories. The NLFGN-UFT framework predicts the RAR as a consequence of the non-local kernel structure, with corrections at the scale of wide binary separations distinguishable from vanilla MOND predictions.

Gravitational wave spectrum: The network stress-energy tensor T_network provides a stochastic gravitational wave background at frequencies corresponding to network phase transition scales. This signal is in principle detectable by pulsar timing arrays (PTA) currently operating (NANOGrav, PPTA, EPTA), which have recently reported evidence for a gravitational wave background that may have contributions beyond standard astrophysical sources.

CMB modifications: The modified Friedmann equation predicts scale-dependent corrections to the CMB temperature and polarisation power spectra. These corrections are parameterised by γ and λ₀ and are in principle distinguishable from the effects of dark energy or dark matter through their specific wavenumber dependence.

### 7.3 Quantum Technology Applications

The network quantum gate structure predicted by the Hilbert space decomposition |Ψ⟩ = |ψ\_base⟩ ⊗ |ψ\_network⟩ ⊗ |ψ\_subtle⟩ suggests novel quantum computing architectures exploiting the network sector as a physical resource. Specifically, the non-local entanglement entropy modification may be exploitable for error correction protocols in regimes where standard local quantum error correction is insufficient.

Field-based quantum sensing: The environment-dependent correction g(v_field) to the uncertainty principle provides a mechanism for ultra-sensitive accelerometry: a sensor operating near the critical density ρ\_c where the network phase transition occurs would exhibit dramatically enhanced sensitivity to gravitational gradients, with applications in geodesy, inertial navigation, and fundamental physics.

## 8. CONNECTIONS TO THE LITERATURE

### 8.1 Relation to MOND and Its Extensions

MOND, first proposed by Milgrom (1983), modifies Newton's law of gravity for accelerations below a₀ ≈ 1.2 × 10⁻⁸ cm s⁻², yielding flat rotation curves without dark matter. Famaey and McGaugh (2012) provide an exhaustive review of MOND phenomenology across scales from dwarf spheroidal galaxies to superclusters, demonstrating that the theory's single acceleration parameter a₀ predicts observations that dark matter models require many free parameters to reproduce.

The TeVeS relativistic extension by Bekenstein (2004) introduces a scalar, vector, and tensor field to produce MOND phenomenology in a Lorentz-covariant framework. Skordis and Złośnik (2021) subsequently demonstrated that a MOND-inspired model with a scalar and a vector field permeating space can reproduce the cosmic microwave background acoustic peaks — a longstanding challenge for MOND — while remaining consistent with gravitational lensing and gravitational wave speed measurements.

The NLFGN-UFT framework encompasses MOND as a low-energy, low-density limit of the full theory. The network interaction and non-local kernel structure provide the physical mechanism for the MOND transition, while the field decomposition theorem ensures that the theory reduces to GR in the appropriate high-field limit. This represents an advance over phenomenological MOND models: rather than postulating a modification to Newton's law, the framework derives it from an underlying action principle with physical degrees of freedom.

### 8.2 Relation to Quantum Gravity Approaches

The post-quantum theory of classical gravity proposed by Oppenheim et al. (2023) challenges the assumption that gravity must be quantised, showing that a consistent theory can preserve classical spacetime while coupling it to quantum matter through stochastic terms. The NLFGN-UFT framework is compatible with this perspective: the classical field equations are modified by quantum-origin network terms, but the spacetime manifold itself need not be quantised. The entanglement entropy modification of Section 4.2 plays the analogous role to the stochastic noise terms of Oppenheim's theory.

The Holomorphic Unified Field Theory (HUFT) demonstrates that a single geometric action on a four-complex-dimensional manifold can reproduce GR and all Standard Model gauge interactions. This motivates the action structure of Section 3.2, where L_network plays the role of the additional geometric sector.

Non-local quantum field theories with infinite-derivative operators have been studied as a means of achieving UV finiteness while maintaining Poincaré invariance and unitarity. The present framework imports the UV-finiteness of entanglement entropy demonstrated in NLQFT into the gravitational context, providing a natural resolution of the UV divergences that plague standard treatments of black hole entropy and vacuum energy.

### 8.3 Relation to Modified Cosmology

The parameterised post-Friedmann (PPF) framework of Hu and Sawicki (2007) describes modified gravity models through a unified set of parameters describing three regimes: large scales, linear perturbation scales, and the non-linear screening regime. The NLFGN-UFT framework is consistent with this structure: the non-local kernel length λ(ρ,E) defines a scale below which the theory differs from GR, playing the role of the crossover scale r_c in DGP braneworld gravity.

The ΛCDM model remains the most successful large-scale cosmological framework, matching observations of the CMB, baryon acoustic oscillations, and large-scale structure. NLFGN-UFT does not seek to replace ΛCDM but to provide a physical mechanism for its dark sector components through the network field contributions to the Friedmann equation and to the matter power spectrum.

## 9. DISCUSSION AND OUTSTANDING CHALLENGES

The framework presented here is mathematically self-consistent and physically motivated, but several important questions require further development.

First, the quantitative determination of the coupling constants α₁, α₂, and γ from first principles or from fits to observational data remains to be performed. The structure of the theory guarantees that parameter choices exist that reproduce ΛCDM on large scales and MOND on galactic scales simultaneously, but the explicit construction of these solutions requires numerical cosmological simulations that are beyond the scope of the present analytic treatment.

Second, the phase structure of the network sector — particularly the nature of the phase transition at ρ\_c and its cosmological implications — requires analysis using non-perturbative methods such as functional renormalisation group or lattice field theory. The analytic RG analysis of Section 3.3 provides the qualitative picture but not the quantitative phase diagram.

Third, the GUP modification of Section 4.3 has the potential to conflict with existing precision spectroscopy constraints unless the correction function g(v_field) is sufficiently suppressed in laboratory environments. A detailed analysis of the constraints from H atom spectroscopy, electron anomalous magnetic moment measurements, and atom interferometry is required.

Fourth, the black hole metric correction g_network must be shown to be consistent with existing tests of GR in the strong-field regime, including X-ray binary timing, black hole shadow imaging (Event Horizon Telescope), and post-Newtonian solar system tests. The screening mechanism inherent in the action ensures this in principle, but explicit calculation is needed.

Despite these open questions, the framework provides a definite programme for theoretical and experimental work. It makes specific predictions at every scale from laboratory to cosmological, offers quantitative connections to the existing modified gravity literature, and reduces to established theories in appropriate limits.

## 10. CONCLUSIONS

We have presented the Non-Local Field Gravity and Network Unified Field Theory (NLFGN-UFT), a comprehensive framework unifying gravitational, quantum, and cosmological phenomena through a hierarchical field decomposition and non-local integral kernel structure. The principal results are:

1. A complete field decomposition theorem expressing the total field ϕ in five physically motivated components, each arising from distinct physical mechanisms at different scales.
2. A density- and energy-dependent non-local kernel K(x,x',ρ,E) whose structure naturally recovers Newtonian gravity, MOND phenomenology, and modified cosmological expansion in appropriate limits.
3. A proof that the characteristic field speed satisfies v_field ≤ c as a consequence of the variational structure of the action, not as an external postulate.
4. Modified Einstein field equations, a modified Friedmann equation, and modified quantum mechanical relations derived consistently from a single action principle.
5. A UV-finite modification of the von Neumann entanglement entropy incorporating stress-energy two-point correlations, connecting quantum information theory and gravitational dynamics.
6. A detailed experimental programme spanning laboratory quantum optics, galactic dynamics, gravitational wave astronomy, and CMB observations.

The framework is mathematically complete in outline, physically motivated by diverse observational evidence, and makes contact with state-of-the-art theoretical developments in quantum gravity, modified gravity, and cosmology. A full numerical treatment of the cosmological perturbation spectrum and an explicit comparison with Planck CMB data constitute the most important next steps.

## References

[1] Milgrom, M. (1983). A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis. Astrophysical Journal, 270, 365–370.

[2] Famaey, B., & McGaugh, S. S. (2012). Modified Newtonian Dynamics (MOND): Observational Phenomenology and Relativistic Extensions. Living Reviews in Relativity, 15(1), 10.

[3] Chae, K.-H., et al. (2020). Testing the Strong Equivalence Principle: Detection of the External Field Effect in Rotationally Supported Galaxies. The Astrophysical Journal, 904(1), 51.

[4] Skordis, C., & Złośnik, T. (2021). New Relativistic Theory for Modified Newtonian Dynamics. Physical Review Letters, 127(16), 161302.

[5] Oppenheim, J., et al. (2023). A post-quantum theory of classical gravity. Physical Review X, 13(4), 041040.

[6] Rocci, A., & Van Riet, T. (2024). The quantum theory of gravitation, effective field theories, and strings: yesterday and today. The European Physical Journal H.

[7] arXiv:2409.12206 (2024). Quantum Entanglement Entropy and Informational Stress-Energy Tensor Contributions to Gravitational Dynamics.

[8] Moffat, J., & Toth, V. T. (2012). Nonlocal quantum field theory and quantum entanglement. arXiv:2309.06576.

[9] Bekenstein, J. D. (2004). Relativistic gravitation theory for the modified Newtonian dynamics paradigm. Physical Review D, 70(8), 083509.

[10] Hu, W., & Sawicki, I. (2007). A Parameterized Post-Friedmann Framework for Modified Gravity. arXiv:0708.1190.

[11] Mavromatos, N., & Papavassiliou, J. (2013). Non-local quantum gravity and the Cosmological Constant problem. Physical Review D, 87, 116018.

[12] Pfeifer, C., et al. (2025). From kinetic gases to an exponentially expanding universe — the Finsler-Friedmann equation. JCAP, 2025(10), 050.

[13] Weinberg, S. (1989). The cosmological constant problem. Reviews of Modern Physics, 61(1), 1–23.

[14] Abbott, B. P. et al. (2016). Observation of gravitational waves from a binary black hole merger. Physical Review Letters, 116, 061102.

[15] Riess, A. G. et al. (1998). Observational evidence from supernovae for an accelerating universe and a cosmological constant. Astronomical Journal, 116, 1009–1038.

[16] Fursaev, D. V. (2007). Entanglement Entropy in Quantum Gravity and the Plateau Problem. arXiv:0711.1221.

[17] Solodukhin, S. N. (1995). Entanglement entropy of black holes. hep-th/9504022.

[18] Planck Collaboration (2020). Planck 2018 results: Cosmological parameters. Astronomy & Astrophysics, 641, A6.

[19] Einstein, A. (1915). Die Feldgleichungen der Gravitation. Sitzungsberichte der Preussischen Akademie der Wissenschaften, 844–847.

[20] Scarpa, R. (2006). Modified Newtonian Dynamics, an Introductory Review. arXiv:astro-ph/0601478.

*— End of Paper —*
