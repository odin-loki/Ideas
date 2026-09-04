# The Energy-Resource Economic Model (EREM)

*A thermodynamically consistent framework for national wealth assessment, resource-backed currency design, and biophysical economic measurement*

Version 1.0 — January 2026

**Status:** Theoretical framework — requires empirical validation

*Keywords: biophysical economics, energy quality, national wealth, EROI, resource-backed currency, thermoeconomics, entropy, TNW*

## Abstract

The Energy-Resource Economic Model (EREM) proposes a physics-grounded framework for measuring national wealth and anchoring monetary systems to verifiable physical quantities. Unlike conventional GDP-based accounting, which aggregates financial transaction flows, EREM defines Total National Wealth (TNW) as a dimensionally consistent sum of energy reserves, material resources, food production capacity, human labour capacity, and infrastructure efficiency — all expressed in SI-compatible energy units (megajoules). By anchoring currency issuance to TNW via a conservative backing ratio, EREM offers a monetary mechanism that cannot expand through financial engineering alone, instead constraining money supply growth to rates permitted by physical resource discovery, efficiency improvement, or renewable capacity addition.

This paper presents the theoretical underpinnings of EREM within the intellectual tradition of biophysical economics, situating the framework alongside seminal contributions from Georgescu-Roegen (1971), Soddy (1926), Odum (1971, 1996), Hall and Klitgaard (2018), and the broader Energy Return on Investment (EROI) literature. The mathematical formalism is developed in full, including Energy Quality Factors (Q-factors), National Energy Wealth (NEW), Material Wealth Index (MWI), Food Energy Wealth (FEW), Human Labour Capacity (HLC), Infrastructure Efficiency Factor (IEF), the Resource-Backed Currency Unit (RBCU), and international exchange rate mechanics. Dimensional consistency proofs, numerical examples, and a critical comparison with fiat currency systems are provided. Limitations, open research questions, and a phased implementation pathway are discussed.

## 1. Introduction

Modern macroeconomics measures national wealth primarily through Gross Domestic Product (GDP) — the aggregate monetary value of final goods and services produced within a country in a given period. While GDP has served as a practical proxy for economic activity since its formalization by Simon Kuznets in the 1930s, a long-standing and increasingly prominent critique argues that it fundamentally misrepresents real wealth. GDP conflates income with wealth, treats resource depletion as neutral, rewards environmental destruction when it generates cleanup costs, and can expand indefinitely through financial engineering without any corresponding increase in physical productive capacity [60].

These shortcomings are not merely theoretical. The Inclusive Wealth Index (IWI), developed under the United Nations Environment Programme, tracks the combined stock of produced, human, and natural capital across 140 countries. Critically, the IWI reveals that 44 of these countries experienced declining per-capita inclusive wealth even as their GDP per capita rose — indicating that measured "growth" masked the drawdown of real productive foundations [55]. The Dasgupta Review (2021) similarly concluded that overreliance on GDP leads policy-makers to substitute income for wealth, systematically undervaluing the natural capital upon which all economic activity ultimately depends [58].

The intellectual lineage of physics-based economic critique extends to Frederick Soddy, the Nobel Prize-winning radiochemist who, in Wealth, Virtual Wealth and Debt (1926), drew a precise distinction between real wealth — physical goods, productive machinery, energy resources — and virtual wealth, the mathematical abstractions of money and debt. Soddy observed that real wealth obeys the Second Law of Thermodynamics: it decays, corrodes, and is consumed. Debt, by contrast, compounds at interest according to purely mathematical rules, with no thermodynamic upper bound [22][23]. This fundamental asymmetry, Soddy argued, ensures that financial obligations will eventually outpace the physical wealth they claim to represent — a prediction that has been borne out repeatedly in successive financial crises.

Nicholas Georgescu-Roegen formalised these intuitions in his 1971 magnum opus, The Entropy Law and the Economic Process. Georgescu-Roegen demonstrated that the conventional economic representation of production as a reversible, mechanical process violates the Second Law of Thermodynamics [31][36]. The economy does not recycle matter and energy in a closed loop; it irreversibly transforms low-entropy resources (concentrated fossil fuels, mineral ores, fertile soils) into high-entropy waste. Economic scarcity is therefore not a function of price signals alone, but of the irreversible physical reality of entropy [31]. Howard T. Odum extended this analysis through his development of emergy accounting — the total solar energy required, directly and indirectly, to produce a good or service — providing a unified metric for comparing energy flows across qualitatively different systems [41][43][44].

More recently, the field of biophysical economics, represented most prominently by Charles Hall, Robert Costanza, and their collaborators, has developed EROI (Energy Return on Investment) as a practical metric capturing the energy profit of energy production systems. EROI data consistently show that the net energy delivered by fossil fuels to society has declined significantly over recent decades — from EROI ratios of 100:1 for early US oil and gas (circa 1919) to approximately 18:1 by the mid-2000s — with direct consequences for economic productivity [14][20]. As Hall, Lambert and Balogh (2014) demonstrated, declining EROI means an increasing fraction of gross economic output must be diverted to sustaining energy production itself, compressing the discretionary surplus available for other economic activity [20].

The Energy-Resource Economic Model (EREM) proposed in this paper draws on all of these intellectual traditions. It is not, however, merely a restatement of prior work. EREM makes specific technical contributions: (1) a formal weighted composite wealth index (TNW) expressed in SI energy units and proven dimensionally consistent; (2) an explicit Energy Quality Factor (Q-factor) framework that captures not just energy content but energy density, transportability, controllability, and waste profile in a single scalar; (3) a currency design mechanism (RBCU) anchored to TNW with a defined conservative backing ratio; and (4) a trade exchange rate formula derived from per-capita TNW differentials, incorporating thermodynamic entropy losses from shipping. Together, these components constitute an implementable, testable framework that positions physics as the foundation of economic measurement — not its critic.

## 2. Intellectual and Historical Context

## 2.1 The Physiocrats and the Origins of Physical Economics

The roots of energy-grounded economic thinking precede modern thermodynamics. The Physiocrats of 18th-century France — Quesnay, Mirabeau, and Turgot — argued that real wealth derived exclusively from the productivity of the land, the original solar energy transformer [5]. Their tableau économique was the first systematic attempt to trace the circular flow of value through a productive economy anchored in physical production. While the Physiocrats lacked the vocabulary of thermodynamics, their insistence that agriculture (the conversion of solar energy via soil and water into food and fibre) was the uniquely productive sector anticipates modern biophysical analysis with remarkable precision.

Sergei Podolinsky, a Ukrainian scientist writing in the early 1880s, attempted a more explicit reconciliation of thermodynamics with economic theory. Podolinsky modelled agricultural labour productivity as a function of the energy inputs subsidising human effort, and argued that the ultimate limits to economic growth lay not in political economy but in physical and ecological laws [2]. His work foreshadowed three core concepts later central to EROI analysis: energy flow analysis to characterise food production efficiency; labour productivity as a function of energy subsidy; and the concept of net energy surplus as the driver of civilisational complexity [2].

## 2.2 Frederick Soddy: Thermodynamic Critique of Money

Frederick Soddy's contributions to biophysical economics are historically underappreciated relative to his stature in chemistry and nuclear physics. In Wealth, Virtual Wealth and Debt (1926) and subsequent works, Soddy laid out a systematic critique of fractional reserve banking grounded in thermodynamic realities [22][23][29]. His central argument was precise: real wealth obeys thermodynamic laws — it cannot grow at compound interest rates because physical systems are subject to entropy and decay. Debt, however, is a purely mathematical construct with no thermodynamic upper bound. The compound growth of debt therefore inevitably outstrips the growth of real wealth, generating recurring financial instability [22].

Soddy advocated for a monetary system in which currency issuance was constrained by physical productive capacity, echoing the RBCU mechanism proposed in EREM. He argued that "real wealth was derived from the use of energy to transform materials into physical goods and services" [22] — a claim that is essentially the conceptual core of the TNW formula. His proposals were largely ignored by mainstream economists of his era but were later adopted into ecological economics by Herman Daly, Robert Costanza, and others [2][3].

## 2.3 Georgescu-Roegen and the Entropy Law

Nicholas Georgescu-Roegen's The Entropy Law and the Economic Process (1971) is the foundational text of entropy economics [31][33][36]. Georgescu-Roegen's central argument was that neoclassical production theory — in which capital and labour can be substituted freely, and production processes are mechanically reversible — is physically impossible. The Second Law of Thermodynamics mandates irreversibility: low-entropy resources (ordered, concentrated, available energy) are degraded into high-entropy waste in every productive process. This degradation cannot be undone within a finite energy budget [31].

Georgescu-Roegen introduced the concept of "low entropy" as the source of genuine economic scarcity, in contrast to the neoclassical view of scarcity as arising from relative price dynamics alone. His bioeconomic programme proposed treating the economy as a thermodynamic system in which matter-energy flows, not just monetary flows, determine the scope of productive possibility [36]. While some of Georgescu-Roegen's specific claims (notably regarding matter recycling limits) remain contested, his fundamental insight that economic processes are irreversible thermodynamic transformations is now widely accepted in ecological economics [3].

## 2.4 H.T. Odum and Emergy Analysis

Howard T. Odum developed an elegant solution to the problem of comparing qualitatively different energy forms: emergy (embodied energy), defined as the total solar energy required, directly and indirectly, to produce a good or service, measured in solar emjoules [41][43]. Odum's energy systems language — a symbolic notation for diagramming energy flows, feedback loops, and hierarchical transformations in both ecological and economic systems — provided a computational framework capable of integrating market and non-market goods within a single energy accounting system [41][42].

Odum's concept of transformity (the emergy per unit energy of a product, indicating its position in the energy quality hierarchy) directly anticipates EREM's Q-factor framework. Like Q-factors, transformities capture qualitative differences between energy forms: a joule of highly concentrated nuclear energy has a vastly different role in the economic system than a joule of diffuse solar insolation [43][44]. Odum recognised, as EREM does, that energy quality — not merely energy quantity — determines productive capacity. His Maximum Empower Principle further argued that self-organising systems evolve toward configurations that maximise useful energy transformation over time [41][46].

## 2.5 EROI and Biophysical Economics

Energy Return on Investment (EROI) — the ratio of energy delivered to society to energy expended in obtaining it — was developed principally by Charles Hall and collaborators as a practical, quantifiable extension of biophysical economics [14][16][20]. EROI data provide empirical grounding for the otherwise abstract claim that net energy drives economic surplus. Hall, Lambert and Balogh (2014) demonstrated that EROI values for conventional fossil fuels have declined substantially over the past century, and that this decline has directly compressible consequences for societal discretionary output [20].

The EROI literature also establishes minimum EROI thresholds for societal function. Murphy and Hall (2010) concluded that a societal EROI of approximately 5:1 (by their extended methodology) represents the minimum sustainability threshold, while EROI of 12–13:1 is required to support a technologically advanced society with cultural and artistic production [16]. More recent work using useful-stage EROI estimates (incorporating final-to-useful conversion efficiencies) finds that the effective EROI of fossil fuels at point of use is approximately 3.5:1 — substantially lower than standard EROI metrics suggest [17]. These findings strengthen the case for EREM's IEF (Infrastructure Efficiency Factor), which explicitly rewards improvements in energy conversion efficiency.

## 3. The EREM Framework: Formal Specification

## 3.1 Base Units

EREM is built on three SI-derived base units:

- Energy Wealth Unit (EWU): 1 EWU = 1 MJ (megajoule). The joule is the SI unit of energy (1 J = 1 kg·m²·s⁻²); the megajoule (1 MJ = 10⁶ J) is the practical unit for national-scale energy accounting.
- Material Wealth Unit (MWU): 1 MWU = 1 kg of element or compound at standard purity. Material masses are converted to energy-equivalent units via elemental energy densities.
- Labour Capacity Unit (LCU): 1 LCU = 1 human-hour of productive work capacity, anchored at 2.5 MJ of food-energy equivalent (the approximate metabolic energy budget for sustained human labour).

The choice to denominate all wealth components in energy units is not merely convenient: it is physically motivated. All physical work — the movement of matter, the transformation of materials, the maintenance of biological systems — requires energy as the enabling substrate. By expressing all components in joules, EREM achieves dimensional homogeneity and ensures that the TNW formula is not a dimensional abuse but a genuine physical statement.

## 3.2 Energy Quality Factors (Q-Factors)

Not all energy is economically equivalent. A joule of nuclear-grade heat at the point of generation has profoundly different economic implications than a joule of diffuse solar insolation on an overcast day. The EREM Energy Quality Factor (Q) captures this distinction:

Q = (Energy Density) × (Transportability) × (Controllability) × (Waste Factor)

Each sub-factor is dimensionless and bounded [0, 1]. Nuclear energy serves as the reference standard (Q_nuclear = 1.00) against which all other energy forms are calibrated. The derivation of Q-factors for the primary energy sources is summarised in Table 1 below.

| Energy type | Q-factor | Energy density (J/kg) | Transportability | Controllability | Waste factor |
|-------------|----------|--------------------------|------------------|-----------------|--------------|
| Nuclear (U-235) | 1.00 | 8.2 × 10¹³ | 0.95 (compact, stable) | 0.98 (precise load-following) | 0.92 (long-term storage issues) |
| Petroleum | 0.75 | 4.6 × 10⁷ | 0.98 (portable liquid) | 0.90 | 0.60 (CO₂, refining losses) |
| Hydroelectric | 0.82 | Variable (gravitational) | 0.90 (grid transmittable) | 0.95 (load-following) | 1.00 (clean) |
| Natural gas | 0.68 | 5.5 × 10⁷ | 0.90 (pipeline / LNG) | 0.95 (fast response) | 0.65 (CO₂) |
| Wind | 0.65 | Variable (wind speed) | 0.85 (grid transmittable) | 0.35 (intermittent) | 1.00 (clean) |
| Solar (installed) | 0.58 | 150–200 W/m² avg. | 0.85 (point-of-use gen.) | 0.30 (intermittent) | 1.00 (clean) |
| Coal | 0.42 | 2.4 × 10⁷ | 0.85 (bulk handling) | 0.70 (slow response) | 0.45 (CO₂, particulates) |

*Table 1. EREM Energy Quality Factors by fuel type. Nuclear energy is the reference standard (Q = 1.00).*

Q-factor weighting is conceptually consistent with Odum's transformity framework [43]: just as transformity captures the energy quality hierarchy by reference to solar input, EREM's Q-factors capture the economic utility hierarchy of energy carriers relative to the most controllable, dense, and low-waste reference standard (nuclear). Both approaches recognise that the capacity to do economic work depends not just on energy quantity but on the quality, density, and accessibility of that energy.

## 3.3 National Energy Wealth (NEW)

The National Energy Wealth (NEW) formula aggregates contributions from finite fossil reserves and renewable energy infrastructure:

NEW = Σᵢ(R_i × Q_i × E_i) + Σⱼ(C_j × CF_j × L_j × Q_j × 8760)

Where:

  R_i   = Proven reserves of fuel type i (kg)

  Q_i   = Quality factor for fuel type i

  E_i   = Specific energy content (J/kg)

  C_j   = Installed renewable capacity (W)

  CF_j  = Capacity factor for renewable j (dimensionless, 0–1)

  L_j   = Expected operational lifespan (years)

  Q_j   = Quality factor for renewable j

  8760  = Hours per year

In expanded form, using reference energy densities (coal: 24 MJ/kg; natural gas: 55 MJ/kg; petroleum: 46 MJ/kg; uranium-235: 8.2×10⁷ MJ/kg):

E_reserves = Σ(R_coal × 0.42 × 24 MJ/kg)

           \+ Σ(R_gas × 0.68 × 55 MJ/kg)

           \+ Σ(R_petrol × 0.75 × 46 MJ/kg)

           \+ Σ(R_uranium × 1.00 × 8.2×10⁷ MJ/kg)

E_renewable = Solar_W × 0.58 × 0.25 × 8760 h/yr × 25 yr

            \+ Wind_W  × 0.65 × 0.35 × 8760 h/yr × 20 yr

            \+ Hydro_W × 0.82 × 0.50 × 8760 h/yr × 50 yr

The renewable component integrates expected lifetime output, reflecting the capitalised energy value of installed infrastructure over its service life. This treatment is analogous to the NPV (net present value) logic of conventional investment accounting, but expressed in physical rather than monetary terms, and free of the distortions introduced by discount rates.

## 3.4 Material Wealth Index (MWI)

The Material Wealth Index (MWI) captures the physical stock of critical materials, weighted by their economic versatility and accessibility:

MWI = Σₖ(M_k × V_k × A_k)

Where:

  M_k = Mass of material k in proven reserves (kg)

  V_k = Versatility factor (number of critical industrial applications)

  A_k = Accessibility factor (extraction difficulty, 0–1)

Materials are categorised into three tiers by scarcity and economic leverage, with multiplicative scarcity premiums applied: Tier 1 structural metals (iron, aluminium, copper; V-factors 7–9, A-factors 0.7–0.9, multiplier ×1.0); Tier 2 rare earth elements and battery metals (neodymium V=15, lithium V=12, cobalt V=10; A-factors 0.3–0.6, multiplier ×3.0); and Tier 3 platinum group metals (platinum V=18, palladium V=16; A-factors 0.1–0.3, multiplier ×10.0). A circular economy correction factor (Recycling_rate × Stock × 0.5) is applied to reflect the partial wealth value of recyclable secondary stocks.

The V-factors encode a form of economic network centrality: materials that enable the greatest number of industrial applications have the highest versatility scores. This is conceptually consistent with the resource criticality literature, which identifies materials as "critical" when they are both economically important and supply-constrained [e.g., rare earth elements designated critical by the EU and the US Department of Energy].

## 3.5 Food Energy Wealth (FEW)

Food production capacity is the energetic foundation of human labour power. FEW converts agricultural land productivity into energy units:

FEW = (Arable_area_m² × Yield_J/m²/yr × Soil_Q)

    \+ Storage_reserves_J

  FEW_grains  = Area × 2.5×10⁶ J/m²/yr × Soil_Q

  FEW_protein = Area × 1.8×10⁶ J/m²/yr × Soil_Q

  FEW_fats    = Area × 3.5×10⁶ J/m²/yr × Soil_Q

Total FEW = (FEW_grains + FEW_protein + FEW_fats)

          × Water_availability (0–1)

          × Climate_stability (0.7–1.0)

## 3.6 Human Labour Capacity (HLC)

Human Labour Capacity converts demography and nutritional status into an energy flow:

HLC = Population × Working_age\_% × Health_factor × (FEW / Population_needs)

  Population_needs = Pop × 2500 kcal/day × 365 × 4184 J/kcal

                   ≈ Pop × 3.83×10⁹ J/person/year

  Working_age\_%   = (Age 15–65 cohort) / Total population

  Health_factor   = 0.6–1.0 (function of nutrition + healthcare quality)

This formulation explicitly links labour productivity to nutritional security — a connection empirically well-established in development economics but routinely ignored in GDP accounting. A population that is malnourished or energy-deficient will have a reduced HLC regardless of nominal wage levels, a reality that conventional monetary metrics systemically obscure.

## 3.7 Infrastructure Efficiency Factor (IEF)

The IEF rewards technological advancement and operational efficiency:

IEF = (Actual_GDP_energy_equiv / Theoretical_minimum_energy)

    × (Grid_eff × Transport_eff × Industrial_eff)^(1/3)

Theoretical minimum energy = Carnot limits + material transformation minima

The IEF captures a critical dimension of economic development: the ability to extract more useful work from a given energy input. A nation with a highly efficient grid, advanced manufacturing, and low-waste transport can deliver substantially more economic output per unit energy than a structurally inefficient peer. By including IEF in the TNW formula — albeit with a relatively modest weight (ε = 0.05) — EREM creates a genuine incentive for efficiency investment that is absent from commodity-backed currency systems but essential to a forward-looking wealth framework.

## 3.8 Total National Wealth (TNW)

The master formula aggregates all components into a single dimensionally consistent index:

TNW = (α × NEW) + (β × MWI) + (γ × FEW) + (δ × HLC) + (ε × IEF)

  α = 0.40  (energy weight)

  β = 0.25  (materials weight)

  γ = 0.20  (food weight)

  δ = 0.10  (labour weight)

  ε = 0.05  (efficiency weight)

All components normalised to MJ-equivalent.

Σ(α, β, γ, δ, ε) = 1.00

The weighting coefficients (α, β, γ, δ, ε) are the primary empirically open parameters of the EREM framework. The proposed values above represent an informed theoretical prior: energy is assigned the largest weight (0.40) because it is the universal enabling input for all physical work; materials (0.25) are the physical substrate of technology and infrastructure; food (0.20) directly constrains the size and productivity of the human population; labour (0.10) encodes the organisational capacity to deploy resources; and efficiency (0.05) provides a forward-looking innovation premium. Optimal weights are a primary open research question for empirical validation (Section 7).

## 3.9 Dimensional Consistency Proof

A fundamental requirement of any physical framework is dimensional homogeneity. The EREM TNW formula satisfies this requirement:

[TNW] = [Energy] = MJ = kg·m²·s⁻²

NEW:  [kg] × [dimless] × [J/kg]           = [J]  ✓

MWI:  [kg] × [dimless] × [dimless]                

      → converted to [J] via standard energy                        

        equivalents per material                   ✓

FEW:  [m²] × [J/m²/yr] × [yr]             = [J]  ✓

HLC:  [persons] × [J/person/yr] × [yr]    = [J]  ✓

IEF:  [dimless] × [J]                     = [J]  ✓

All components reduce to energy units.

System is dimensionally consistent. □

Additionally, a global conservation principle holds: in a closed planetary system, the sum of TNW across all nations equals the sum of physical resources on and within Earth (modulo renewable energy flows from the Sun). Wealth cannot be created by financial engineering; it can only be transferred between nations via trade or increased via resource discovery, efficiency improvement, or renewable infrastructure deployment. This conservation property eliminates the possibility of collectively illusory wealth expansion — a failure mode endemic to fiat monetary systems.

## 4. The Resource-Backed Currency Unit (RBCU)

## 4.1 Currency Issuance Formula

The Resource-Backed Currency Unit (RBCU) anchors monetary supply to physical TNW:

Total_currency_issuance = k × TNW

  k = 0.85 (conservative backing ratio)

1 RBCU = (TNW / Total_currency) MJ-equivalent

Maximum currency expansion rate = (dTNW/dt) / TNW

The backing ratio k = 0.85 serves as a physical reserve margin, analogous to a fractional reserve ratio but operating in the opposite direction: rather than multiplying money above its physical backing, RBCU issuance is set below TNW to provide a buffer against measurement uncertainty and short-term resource fluctuations. This conservatism is intentional: the expected uncertainty in large-scale geophysical estimates (proven reserves, renewable capacity assessments) warrants a 15% margin.

## 4.2 Inflation and Deflation Mechanics

Under RBCU mechanics, currency expansion is only permitted when one or more of the following physical conditions are satisfied:

- New reserves are discovered and verified (increases R_i in the NEW formula)
- Renewable energy infrastructure is installed (increases C_j in NEW)
- Infrastructure efficiency improves (increases IEF)
- Population growth is matched by proportional food production increase (increases HLC without decreasing FEW per capita)

Conversely, automatic deflation occurs when:

- Resources are depleted faster than discovery or recycling replenishes them
- Infrastructure degrades (grid efficiency falls, transport systems deteriorate)
- Food production declines relative to population requirements

This automatic deflation mechanism is one of EREM's most significant departures from fiat systems. In a fiat regime, resource depletion is an externality that does not appear in the money supply — a nation can exhaust its oil reserves and continue issuing currency as if the wealth were intact. Under RBCU, the depletion immediately reduces TNW, contracts the permissible currency supply, and gently deflates the currency — making stored savings more valuable and incentivising conservation. This is not a design curiosity; it is the fundamental alignment mechanism between economic incentives and physical reality that fiat systems structurally lack.

## 4.3 Interest Rates Under EREM

In a resource-backed system, interest rates cannot be set arbitrarily by central bank policy; they must reflect real resource dynamics:

Interest_rate = Resource_depletion_rate + Risk_premium + Time_preference

  Resource_depletion_rate = Annual_extraction / Total_reserves

  Risk_premium = Default_probability × (1 – Collateral_coverage)

  Time_preference = 0.01–0.03

Maximum sustainable interest = Discovery_rate + Efficiency_gains_rate

This formulation ties the cost of capital directly to the rate of physical resource drawdown. If a nation is consuming its oil reserves at 5% per year, base interest rates cannot sustainably be set below 5%, as lenders must at minimum recover the real wealth destruction implicit in resource extraction. Soddy's fundamental critique — that compound interest is "physically impossible" in a finite resource system because it implies indefinite exponential growth — is operationalised here as an explicit upper bound on the maximum sustainable interest rate [22][29].

## 5. International Trade and Exchange Rates

## 5.1 Exchange Rate Formula

Exchange rates between nations under EREM are determined by per-capita TNW differentials:

Exchange_rate(A/B) = (TNW_A / Pop_A) / (TNW_B / Pop_B)

  = Per-capita wealth of Nation A / Per-capita wealth of Nation B

This formulation eliminates currency manipulation as a trade instrument. Exchange rates reflect genuine productive capacity differences; a nation cannot devalue its way to competitiveness by printing money. The physical reality of TNW is invariant to monetary policy decisions — only actual physical productivity changes move the exchange rate.

## 5.2 Trade Valuation with Entropy Loss

Physical trade involves real thermodynamic costs: transporting matter and energy requires energy, and that energy is irreversibly lost (in the thermodynamic sense) in the process. EREM captures this explicitly:

Trade_value = Mass × Energy_density × Q_factor × (1 – entropy_loss)

Example: 1 million tonnes of coal (A exports to B):

  Mass          = 1×10⁹ kg

  Energy density = 24 MJ/kg

  Q_coal        = 0.42

  Entropy loss  = 0.08 (8% transport energy cost)

  Trade_value = 1×10⁹ × 24 × 0.42 × 0.92

              = 9.26×10⁹ MJ-equivalent = 9.26×10⁹ RBCU_A

The entropy loss factor (here 0.08) encodes the real energy cost of shipping, expressed as a fraction of the energy content being traded. This ensures that long-distance resource trade is accurately costed, and that the thermodynamic penalty of globalised supply chains — routinely invisible in conventional trade accounting — appears explicitly in the balance of payments.

## 5.3 Worked National Example

The following numerical example illustrates EREM applied to two hypothetical nations:

| Parameter | Nation A (Resource-Rich) | Nation B (Efficient, Tech-Advanced) |
| --- | --- | --- |
| NEW (energy reserves) | 5.0 × 10¹⁸ MJ | 2.0 × 10¹⁸ MJ |
| MWI (material wealth) | 2.0 × 10¹⁵ kg-eq | 1.5 × 10¹⁵ kg-eq |
| FEW (food production) | 3.0 × 10¹⁷ MJ/yr | 2.0 × 10¹⁷ MJ/yr |
| HLC (labour capacity) | 1.0 × 10¹⁷ MJ/yr | 5.0 × 10¹⁶ MJ/yr |
| IEF (efficiency factor) | 0.35 | 0.75 |
| Population | 100 million | 50 million |
| TNW (calculated) | ≈ 4.7 × 10¹⁸ MJ | ≈ 2.6 × 10¹⁸ MJ |
| Currency issued (k=0.85) | 4.0 × 10¹⁸ RBCU | 2.2 × 10¹⁸ RBCU |
| Per-capita wealth | 4.0 × 10¹⁰ RBCU/person | 4.4 × 10¹⁰ RBCU/person |
| Exchange rate | 1.000 RBCU_A | 1.100 RBCU_A per RBCU_B |

## 6. Comparison to Existing Economic Frameworks

## 6.1 EREM vs. Fiat Currency Systems

| Dimension | Fiat (Current System) | EREM (Resource-Backed) |
| --- | --- | --- |
| Currency backing | Government debt, confidence | Physical TNW (energy + materials + food + labour + efficiency) |
| Inflation mechanism | Central bank policy (discretionary) | Physical resource depletion (automatic, objective) |
| Wealth measurement | GDP (financial transaction flow) | TNW (productive capacity stock, in MJ) |
| Asset bubbles | Structurally possible (price disconnects from cost) | Structurally impossible (asset value capped at energy cost) |
| Interest rate setting | Committee discretion (subjective) | Resource depletion + risk (physics-derived) |
| Resource depletion | Externalised (invisible to money supply) | Automatic currency contraction (immediate and visible) |
| Trade exchange rates | Market / policy determined | Per-capita TNW ratio (non-manipulable) |
| Efficiency rewards | Partial (reflected in productivity and profits) | Direct TNW increase (IEF component) |
| Wealth creation mechanism | Financial engineering, debt expansion | Physical discovery, efficiency, infrastructure, renewables |
| Dimensional consistency | Not applicable (monetary units) | Dimensionally proven (all units reduce to joules) |

## 6.2 EREM vs. the Gold Standard

EREM shares with the gold standard the property that currency issuance cannot be expanded indefinitely through financial engineering. However, gold backing has a critical deficiency: gold is a single, inert commodity with limited industrial leverage (V_gold is relatively low compared to platinum group metals or rare earths). A gold standard does not reward energy efficiency, renewable investment, or agricultural productivity — all of which generate real wealth under EREM but are invisible to a gold-backed system. Moreover, gold production itself has a relatively low Q-factor utility relative to its mining energy cost, making it a poor anchor for a physically motivated wealth framework.

EREM supersedes the gold standard by anchoring currency to the full spectrum of national productive capacity — the entire thermodynamic engine of the economy, not merely the inventory of a single metal. It also incorporates renewable energy, which the gold standard structurally cannot, making EREM inherently future-compatible in a way that gold-backed systems are not.

## 6.3 EREM vs. the Inclusive Wealth Index (IWI)

The UN's Inclusive Wealth Index (IWI) [55][52] is conceptually the closest existing framework to EREM. Both measure national wealth as a stock rather than a flow, and both incorporate natural capital alongside produced and human capital. The IWI demonstrates exactly the failure mode EREM is designed to address: 44 of 140 countries analysed showed declining inclusive wealth despite rising GDP per capita, confirming that monetary flow metrics systematically misrepresent wealth dynamics [55].

However, EREM and IWI differ in three important respects. First, IWI still expresses wealth in monetary (US dollar) terms, retaining the measurement instabilities inherent in money as a ruler. EREM uses SI energy units, which are invariant and physically grounded. Second, IWI does not directly anchor a currency system — it is an analytical indicator, not a monetary constitution. EREM is explicitly designed as both a wealth measurement system and a currency backing mechanism. Third, EREM introduces the IEF component, which explicitly captures energy conversion efficiency as a source of wealth — a feature absent from IWI's framework.

## 7. Limitations, Critiques, and Open Research Questions

EREM is a theoretical framework at v1.0, and its authors do not claim it is ready for immediate implementation. The following limitations and open questions represent the primary research agenda for empirical validation and refinement.

## 7.1 Weighting Coefficient Calibration

The coefficients (α=0.40, β=0.25, γ=0.20, δ=0.10, ε=0.05) are theoretically motivated priors, not empirically validated optima. Different economic structures may warrant different weightings: a small island nation with minimal mineral resources but exceptional human capital and renewable energy may argue for lower β and higher δ or ε. Calibration of optimal weighting across diverse national economies is a major research programme requiring cross-country empirical data on the correlations between TNW components and measured human wellbeing outcomes.

## 7.2 Q-Factor Measurement and Dynamics

The Q-factors presented in Section 3.2 incorporate qualitative assessments (controllability, waste factor) that require empirical validation at the national level. Q-factors are also dynamic: as battery storage technology improves, the controllability penalty for solar and wind decreases, raising their Q-factors over time. A rigorous dynamic Q-factor model — incorporating technology learning curves, storage costs, and grid integration penalties — is needed for accurate forward projections of renewable energy's contribution to TNW.

## 7.3 Knowledge Capital and Intangibles

EREM's TNW formula does not currently incorporate knowledge capital — patents, scientific capacity, institutional quality, or software. This is a deliberate conservative choice: knowledge is extremely difficult to quantify in energy-equivalent terms without arbitrary conversion factors. The IEF component partially captures knowledge capital via its efficiency multiplier (more knowledge typically produces more efficient systems), but this is an indirect and incomplete representation. Future EREM extensions should explore whether knowledge capital can be quantified in emergy-equivalent terms, following Odum's information emergy framework [42].

## 7.4 Ecosystem Services

EREM does not explicitly account for ecosystem services — carbon sequestration, water purification, biodiversity, soil regeneration — beyond their indirect effect on Soil_Q and Water_availability in the FEW formula. The Dasgupta Review (2021) and the natural capital accounting literature argue strongly that ecosystem services represent a significant fraction of genuine national wealth, particularly for developing nations with large intact natural systems. A comprehensive EREM v2.0 should incorporate an Ecosystem Services Wealth (ESW) component.

## 7.5 Political Economy of Implementation

The most significant practical barrier to EREM implementation is political, not technical. Sovereign monetary authorities have powerful incentives to retain discretionary control over money supply expansion. The transition from a fiat system to an RBCU system would require: (a) politically independent reserve audit institutions capable of verifying resource stocks; (b) international agreement on measurement standards and Q-factor conventions; and (c) a transitional mechanism allowing the fiat and RBCU systems to coexist during the verification period. Section 9 sketches a phased transition pathway.

## 8. Future Extensions

The EREM framework is extensible in multiple directions:

- Space resources: Asteroid mining and lunar extraction will eventually constitute legitimate components of planetary material wealth. EREM's MWI formula extends naturally to off-world reserves once extraction becomes operationally feasible.
- Fusion energy: Commercial fusion power will introduce an energy source with Q-factors potentially exceeding current nuclear fission, with substantially reduced waste. EREM's Q-factor framework accommodates fusion via the same dimensional machinery.
- Negative emissions: As carbon dioxide removal (CDR) technologies scale, EREM could incorporate a negative-emissions credit that reflects the real energy value of restored atmospheric low-entropy.
- Quantum computing efficiency: As quantum computing reduces the energy cost of computational work, IEF gains from quantum-enabled industrial optimisation should be formally quantifiable.
- Water as explicit wealth component: Freshwater is a critical but currently under-represented resource in EREM. A Water Wealth Component (WWC) incorporating aquifer volumes, river flow rates, and desalination capacity should be developed for EREM v2.0.
- Dynamic Q-factor evolution: Machine learning methods applied to energy production data could enable continuous Q-factor updating as technology evolves, replacing static parameter estimates with adaptive real-time values.

## 9. Implementation Pathway

A phased transition from fiat to RBCU systems is proposed, recognising both the technical requirements and the political economy of implementation:

| Phase | Description | Duration | Key Milestones |
| --- | --- | --- | --- |
| Phase 1: Data Infrastructure | Establish independent national resource audit institutions. Define standardised Q-factor measurement protocols. Develop quarterly reserve reporting and renewable capacity registries. | Years 1–5 | First TNW estimates published; international measurement standards agreed. |
| Phase 2: Parallel Currency | Issue RBCU alongside existing fiat currency. RBCU non-mandatory; used initially in commodity and energy trade. Market-determined fiat/RBCU exchange rate established. | Years 5–15 | RBCU accepted in 30%+ of commodity trade; exchange rate stable. |
| Phase 3: Gradual Transition | Increase mandatory RBCU usage in government transactions, tax collection, and bond issuance. Reserve backing gradually increased as verification confidence grows. | Years 15–25 | TNW verification coverage exceeds 80% of national wealth; RBCU fiat parity achieved. |
| Phase 4: Full Conversion | RBCU becomes primary currency. Fiat currency retired over a scheduled period. Central bank mandate redefined from inflation targeting to TNW stewardship. | Years 25+ | Full RBCU monetary constitution in force. |

## 10. Conclusion

The Energy-Resource Economic Model (EREM) proposes that economics, properly understood, is a branch of physics: the study of how societies transform low-entropy energy and matter into human wellbeing, subject to the laws of thermodynamics. The central deficiency of contemporary economic measurement — GDP and fiat monetary systems — is that it operates entirely in the monetary domain, using money as a ruler whose length changes over time, and thereby systematically misrepresents the physical reality of national productive capacity.

EREM addresses this deficiency by constructing a dimensionally consistent, physically grounded composite wealth index (TNW) expressed in SI energy units, and anchoring currency issuance to TNW via a conservative backing ratio. The resulting RBCU monetary system cannot be expanded through financial engineering; it cannot generate bubbles by decoupling asset prices from physical cost; it cannot externalise resource depletion; and it cannot misrepresent efficiency improvements as neutral. Every mechanism in the system is aligned with physical reality.

The framework stands on a century of intellectual work: Soddy's thermodynamic critique of debt-based money [22][23], Georgescu-Roegen's entropy economics [31][36], Odum's emergy hierarchy [41][43][44], Hall's EROI analysis [14][16][20], and the Inclusive Wealth literature [55][52]. EREM does not discard this heritage — it synthesises it into a single, implementable, testable system.

The framework requires substantial empirical validation, particularly in the calibration of weighting coefficients, the dynamic modelling of Q-factors, and the measurement methodology for material versatility and accessibility. These are tractable research problems. What is not tractable — what is a matter of physical law rather than estimation — is the fundamental principle that animates EREM:

*"You cannot eat GDP. You cannot power a city with confidence. Real wealth is energy, matter, and the knowledge to transform them efficiently."*

## References

**[1]** Georgescu-Roegen, N. (1971). The Entropy Law and the Economic Process. Harvard University Press, Cambridge, MA.

**[2]** Cleveland, C.J. (1987). Biophysical economics: historical perspective and current research trends. Ecological Modelling 38(1–2), 47–73.

**[3]** Melgar-Melgar, R.E. & Hall, C.A.S. (2020). Why ecological economics needs to return to its roots: the biophysical foundation of socio-economic systems. Ecological Economics 169, 106567.

**[4]** Hall, C.A.S. & Klitgaard, K. (2018). Energy and the Wealth of Nations: An Introduction to Biophysical Economics (2nd ed.). Springer.

**[5]** Yan, J., Feng, L., Steblyanskaya, A., Kleiner, G., & Rybachuk, M. (2019). Biophysical economics as a new economic paradigm. International Journal of Public Administration, 42(15–16), 1395–1407.

**[6]** Perkins, R., & Neumayer, E. (2020). Putting the biophysical (back) in economics: a taxonomic review of modeling the earth-bound economy. Biophysical Economics and Sustainability 5(1).

**[7]** Goldman, D. (2023). Exergy theory of value: towards a comprehensive understanding of economic value creation. SSRN Working Paper 4562648.

**[8]** Kennedy, C. (2021). The intersection of biophysical economics and political economy. Ecological Economics 191, 107231.

**[9]** Kuzemko, C., Bradshaw, M., Bridge, G., et al. (2020). Covid-19 and the politics of sustainable energy transitions. Energy Research & Social Science 68, 101685.

**[14]** Hall, C.A.S., Lambert, J.G., & Balogh, S.B. (2014). EROI of different fuels and the implications for society. Energy Policy, 64, 141–152.

**[16]** Murphy, D.J. & Hall, C.A.S. (2010). Year in review — EROI or energy return on (energy) invested. Annals of the New York Academy of Sciences 1185, 102–118.

**[17]** Brockway, P.E. et al. (2024). Estimation of useful-stage energy returns on investment for fossil fuels with implications for renewable energy. Nature Energy.

**[20]** Hall, C.A.S., Lambert, J.G., & Balogh, S.B. (2014). EROI of different fuels and the implications for society. Energy Policy 64, 141–152. (Full paper.)

**[22]** Soddy, F. (1926). Wealth, Virtual Wealth and Debt: The Solution of the Economic Paradox. George Allen & Unwin, London.

**[23]** Soddy, F. (1934). The Role of Money. George Routledge & Sons, London.

**[29]** Fix, B. (2020). Frederick Soddy's debt dynamics. Economics from the Top Down (blog). https://economicsfromthetopdown.com/2020/09/12/frederick-soddys-debt-dynamics/

**[30]** Natural Economics Workshop. (2025). Frederick Soddy versus the world. Substack. https://naturaleconomicsworkshop.substack.com

**[31]** Georgescu-Roegen, N. (1971). The Entropy Law and the Economic Process. Harvard University Press. [Second reference for entropy law arguments.]

**[36]** Cuscó, P. (2023). The law of entropy and the economic process. Review, Escola Tècnica Superior d'Arquitectura del Vallès.

**[41]** Brown, M.T. (2003). Prof. Howard T. Odum. Energy 28(4), 293–301.

**[42]** Brown, M.T. (2023). Evaluating information with emergy: how did Howard T. Odum incorporate human information into emergy accounting? Discover Environment.

**[43]** Brown, M.T. & Ulgiati, S. (2004). Energy quality, emergy, and transformity: H.T. Odum's contributions to quantifying and understanding systems. Ecological Modelling 178, 201–213.

**[44]** Odum, H.T. (1996). Environmental Accounting: Emergy and Decision Making. Wiley, New York.

**[46]** Brown, M.T. (2025). Biosphere dynamic empower: Howard T. Odum's contributions to open systems thermodynamics. Ecological Modelling 505, 110820.

**[51]** van Zanten, H.H.E. et al. (2024). Beyond GDP: a review and conceptual framework for measuring sustainable and inclusive wellbeing. The Lancet Planetary Health 8(9), e719–e733.

**[52]** Agarwal, N. & Saha, M. (2024). Sustainable matrix beyond GDP: investment for inclusive growth. Humanities and Social Sciences Communications 11, 217.

**[55]** Managi, S. & Kumar, P. (2018). Inclusive Wealth Report 2018. Cambridge University Press / UNEP.

**[58]** Dasgupta, P. (2021). The Economics of Biodiversity: The Dasgupta Review. HM Treasury, London.

*— END OF PAPER —*
