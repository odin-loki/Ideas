# Adaptive Command Military Doctrine

*Technical Research Paper*

Document No. TRP-2026-204 | Version 1.0

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> This paper presents the Adaptive Command Military Doctrine (ACMD) — a **six-tier hierarchical command structure** spanning fire team (5 personnel) → squad (25, 5 × fire team) → platoon (100, 4 × squad) → company (1 000, 10 × platoon) → battalion (50 000, 50 × company) → force (variable) — predicated on **universal leadership training** in which every soldier receives foundational command preparation rather than restricting leadership skills to designated officers and NCOs. The principal doctrinal claim is that **structural resilience under leadership casualties** is achieved by combining (a) pre-designated succession orders at every tier, (b) a 36-week three-phase training regimen (universal foundation → tier-specific specialisation → command development) for every recruit, and (c) span-of-control bounds chosen so that no leader supervises more than ~ 25 individuals directly (the 5 × 5 fire-team-to-squad span) before transitioning to leader-of-leaders management. This paper sits outside the physics envelope of the `Weapons-Defence/weapons_simulation.py` simulator — there is no numerical doctrine model in the simulator suite, and the headline force-structure numbers are doctrinal rather than simulator-derived. The classification banner is illustrative only — adopted for tonal coherence with the rest of the Weapons-Defence portfolio — and ACMD is presented as a doctrinal framework proposal, not as the doctrine of any real defence force; no procurement programme, force-restructuring directive, or sponsorship is implied.

## Honest framing

- ACMD is a **doctrinal framework proposal**, not the published doctrine of any real defence force. It has not been wargamed, fielded, or peer-reviewed by a doctrine command (Australian Defence Force Warfare Centre, US Army TRADOC, NATO ACT, or equivalent).
- The Tier 5 "battalion" definition (50 companies × 1 000 personnel = **50 000 personnel**) is materially larger than the conventional Western battalion (300–1 000 personnel) and overlaps the size of a division or small corps. The naming convention is internal to this paper and is **not** consistent with standard NATO / ABCA force-structure nomenclature; readers should treat the tier labels as proprietary to ACMD rather than as direct equivalents of fielded structures.
- The 36-week universal-leadership training regimen (§3) is a budgetary and recruiting commitment well above current Western basic-training cycles (typically 10–14 weeks of basic + a separate corps / trade pipeline). Time, instructor-cadre, and retention costs of universal leadership training are not modelled in this paper.
- The simulator suite `Weapons-Defence/weapons_simulation.py` covers ballistics, terminal effects, suppressor / hearing-protection stacks, ANC cancellation depth, PK, and osmolality — it does **not** model command-doctrine effectiveness, decision latency, or succession-after-casualty survivability. Any quantitative claim in this paper about doctrinal performance is **first-principles argument, not simulator output**.
- Manufacturing / supply-chain analogues do not apply directly to a doctrine paper; however, the doctrine assumes a recruiting pipeline of sufficient depth and quality to populate the universal-leadership track. That assumption is not always satisfied in fielded volunteer forces and is not analysed here.
- The classification banner ("UNCLASSIFIED // FOR OFFICIAL USE ONLY") is illustrative only and adopted for tonal coherence with the rest of the portfolio. No real sponsorship, no real doctrine command, no procurement programme implied.

*A Six-Tier Hierarchical Framework for Distributed Leadership and Resilient Force Structure*

Defense Technology Research Division

March 2026

## Abstract
Effective military command doctrine must balance centralized strategic direction with decentralized tactical execution, building in resilience against leadership casualties and enabling rapid adaptation to fluid battlefield conditions. This paper presents a six-tier hierarchical command structure — from five-person fire team to 50,000-person battalion — predicated on universal leadership training: every soldier receives foundational command preparation rather than restricting leadership skills to designated officers and NCOs. We analyze the structural design rationale, training regimen across three phases (36 weeks total), command development tracks for each tier, and implementation principles covering distributed authority, flexible training allocation, and continuous development. The doctrine draws on principles from mission command theory, distributed decision-making research, and lessons from counterinsurgency and high-intensity conflict, and is presented as a framework suitable for adoption by a modern defense force seeking to maximize organizational resilience and operational effectiveness.

## 1. Introduction

### 1.1 Doctrinal Context

Military command doctrine shapes how organizations fight, adapt, and survive across the full spectrum of conflict. The fundamental challenge is the tension between unity of command (requiring centralized coordination) and speed of action (requiring decentralized authority). Historical analysis consistently shows that organizations which devolve appropriate decision-making authority to the lowest effective level outperform those relying on hierarchical command chains during dynamic operations (van Creveld, 1985). At the same time, complete decentralization without shared doctrine creates coordination failures and strategic drift.

The Adaptive Command Military Doctrine (ACMD) presented here resolves this tension through two mechanisms: a clearly defined six-tier hierarchical structure that establishes authority, accountability, and communication channels; and universal leadership training that develops command competence at every level, ensuring the organization does not collapse when leaders are lost.

### 1.2 Design Principles

Three design principles govern the ACMD. First, distributed command authority: each tier maintains autonomous decision-making capability within its operational envelope, with upward reporting for situational awareness and downward delegation for execution authority. Second, universal leadership: all personnel receive command training at their tier level and the tier above, enabling seamless succession. Third, structural resilience: the six-tier hierarchy creates multiple redundant command nodes such that the loss of any single node does not paralyze the organization's tactical effectiveness.

## 2. Command Structure

### 2.1 Six-Tier Hierarchy

**Tier**
**Unit**
**Size**
**Command Node**
**Designation System**
1

Fire Team

5 personnel

Team Leader + 4 operators

Alpha–Echo teams within squads

2

Squad

25 personnel (5 Fire Teams)

Squad Leader + 5 Team Leaders

Numbered squads (1st, 2nd, etc.)

3

Platoon

100 personnel (4 Squads)

Platoon Leader + 4 Squad Leaders

Lettered platoons (Alpha, Bravo, etc.)

4

Company

1,000 personnel (10 Platoons)

Company Commander + 10 Platoon Leaders

Numbered companies within battalions

5

Battalion

50,000 personnel (50 Companies)

Battalion Commander + 50 Company Commanders

Numbered battalions within force structure

6

Force

Variable

Commanding General + staff

Strategic force designation

The multiplicative structure (5 fire teams per squad, 4 squads per platoon, 10 platoons per company, 50 companies per battalion) is designed for both operational utility and training scalability. Five-person fire teams provide the minimum viable tactical unit capable of effective maneuver-fire-fire teamwork. The 25-person squad represents the maximum effective span of control for direct supervision by a single junior leader. Above squad level, leaders manage through subordinate leaders rather than individual personnel, requiring increasingly advanced planning and coordination skills.

### 2.2 Command Succession

The universal leadership training principle ensures every member of a fire team can assume team leadership, every team leader can assume squad leadership, and so forth up the chain. Pre-designated succession orders (Team Leader → most senior trained operator → next senior) provide immediate continuity without ad hoc reorganization. Platoon and company-level succession plans are documented as part of pre-mission planning and updated continuously during sustained operations.

## 3. Training Regimen

### 3.1 Phase 1: Basic Infantry Training (16 Weeks)

Weeks 1–8 develop individual skills: weapons proficiency and marksmanship, physical conditioning and endurance, basic field craft and survival, equipment maintenance, and tactical communication procedures. All personnel attain identical baseline capability regardless of eventual specialization — this is foundational to the universal leadership principle.

Weeks 9–16 shift to small unit leadership: fire team tactics, basic command decision-making, situational awareness and battlefield assessment, emergency leadership protocols enabling any team member to assume command, and cross-training on all fire team positions. The dual emphasis on individual capability and collective leadership creates a cohort of soldiers who understand both their own role and the roles of their teammates.

### 3.2 Phase 2: Advanced Squad Operations (12 Weeks)

Weeks 1–6 focus on squad integration: multi-team coordination exercises, squad-level tactical operations, resource management and allocation, inter-team communication protocols, and casualty response with command succession activation. Personnel move from understanding leadership in principle to practicing it under degraded and dynamic conditions.

Weeks 7–12 develop leadership explicitly: tactical decision-making under time pressure and incomplete information, mission planning and briefing techniques conforming to the ACMD planning format, stress inoculation training using scenario-based force-on-force exercises, adaptive leadership scenarios with frequent scenario modifications, and command post operations. Peer evaluations during this phase form part of the record used in leader selection decisions.

### 3.3 Phase 3: Specialized Role Training (8 Weeks)

Weeks 1–4 develop technical specialization across five tracks: communications specialists (encryption, radio architecture, electronic warfare awareness), combat medics (trauma care, evacuation, preventive medicine), heavy weapons operators (crew-served systems, fire support coordination), reconnaissance and intelligence (surveillance, reporting, analysis), and logistics coordinators (supply chain, maintenance, resource accounting).

Weeks 5–8 provide deliberate cross-training: every specialist spends approximately 20 hours on each of the other specializations, building emergency succession capability and mutual understanding across functional boundaries. Advanced equipment familiarization and multi-role capability development exercises complete the phase.

### 3.4 Total Training Investment

**Phase**
**Duration**
**Primary Focus**
**Outcome**
Phase 1

16 weeks

Individual skills and fire team leadership

Universal combat competence

Phase 2

12 weeks

Squad integration and leadership development

Small-unit command capability

Phase 3

8 weeks

Specialization and cross-training

Technical depth with functional breadth

Total

36 weeks

—

Combat-ready specialist with leadership capability

## 4. Command Development Track

### 4.1 Tier 1–2: Team and Squad Leaders

Selection is based on demonstrated Phase 2 performance, leadership aptitude assessments, peer evaluation scores (normalized within cohort), and monitored stress response evaluations. Selected candidates receive six additional weeks of advanced training covering: advanced tactical planning (including combined arms concepts), personnel management and accountability, resource allocation under scarcity, multi-unit coordination, and mentorship skills for developing subordinate leaders.

### 4.2 Tier 3–4: Platoon and Company Commanders

Minimum prerequisites are two years of demonstrated success in squad leadership roles, completion of advanced military education (a 12-week course covering strategic planning analysis, multi-domain operations concepts, advanced communications systems, logistics and supply chain management, and inter-agency coordination), and recommended specialized forces experience to ensure operational credibility.

### 4.3 Tier 5: Battalion Commanders

This tier requires a special forces background, all prerequisite training, at least five years of company-level command experience, staff college graduation, and participation in multi-national joint exercises. The 16-week Battalion Commander preparation course covers strategic-level planning, joint operations coordination, advanced intelligence analysis, political-military considerations in complex environments, and crisis management and decision-making under strategic uncertainty.

## 5. Doctrine Implementation Principles

### 5.1 Distributed Command Authority

Each tier maintains autonomous decision-making capability for actions within its operational and geographic envelope. Upward reporting provides situational awareness and enables higher-level coordination without requiring approval for tactical actions. Downward delegation gives executing echelons the authority and resources to adapt to local conditions without delay. This principle aligns with Mission Command doctrine as articulated in US Army ADP 6-0 and NATO Allied Tactical Publication ATP-3.2.2.

### 5.2 Training Time Allocation

**Training Category**
**Percentage**
**Rationale**
Individual technical skills

40%

Foundation for all other capabilities

Small unit leadership and coordination

30%

Mission execution at decisive action level

Specialized role training

20%

Force multiplier through technical depth

Cross-training and adaptability

10%

Organizational resilience through functional flexibility

### 5.3 Resilience Mechanisms

The ACMD builds in four structural resilience mechanisms: leadership redundancy through pre-designated succession at every level; role redundancy through Phase 3 cross-training ensuring no single-person-dependent capability; structural redundancy through a hierarchical design that permits multiple simultaneous command node losses without organizational paralysis; and doctrinal consistency through standardized planning formats and decision processes that allow any trained leader to integrate rapidly into any command role.

## 6. Advantages and Implementation Considerations

### 6.1 Operational Advantages

Distributed decision-making reduces response time at the point of decision from minutes (awaiting higher approval) to seconds (autonomous action within established intent). Enhanced coordination across all levels results from shared doctrine and mutual understanding of roles. The resilient command structure maintains effectiveness through casualty events that would paralyze traditionally structured organizations.

### 6.2 Resource Requirements

The extended training program (36 weeks versus 16–20 weeks in many conventional force structures) requires approximately 2x the per-soldier training investment. This is partially offset by reduced retraining costs after leadership casualties and higher organizational effectiveness per soldier. A specialist instructor cadre trained in ACMD doctrine must be established and maintained: estimated at one qualified instructor per 50 trainees in Phase 1, one per 25 in Phases 2–3 (due to scenario-based methods requiring closer supervision).

### 6.3 Integration Challenges

Adoption of ACMD doctrine requires alignment with existing force structures, training systems, and evaluation frameworks. Standardization across geographically dispersed units demands a formal doctrinal management system and regular assessment exercises. Maintenance of doctrinal consistency through personnel turnover requires a continuous education pipeline rather than one-time training events.

## 7. Conclusion

The Adaptive Command Military Doctrine presents a coherent framework for building organizations that are simultaneously effective, resilient, and adaptive. The six-tier hierarchical structure provides clear command authority and accountability. Universal leadership training transforms the entire force into a reservoir of command capability rather than depending on a thin leadership stratum. The phased 36-week training regimen systematically develops individual competence, collective coordination, and technical specialization in a sequence optimized for operational readiness.

The doctrine demands greater training investment than conventional approaches but yields qualitative advantages in operational performance and organizational survivability that are particularly valuable in high-intensity conflict where leadership attrition rates are elevated. Implementation requires sustained institutional commitment to the training pipeline and doctrinal management, but the operational returns justify this investment for any force seeking strategic effectiveness in complex and contested environments.

## Appendix A — Governing Equations

This paper sits outside the physics envelope of `Weapons-Defence/weapons_simulation.py` — there is no doctrinal-effectiveness model in the simulator suite. The closed-form models below are first-principles arguments drawn from the published military-operations-research literature (Lanchester, March/Simon, Wright) that frame the §2 force-structure, span-of-control, and training-pipeline quantitative claims. **All numerics in this appendix are mechanistic projections, not simulator output**, and the §3 36-week training pipeline figure is a doctrinal budget rather than a wargamed result.

### A.1 Lanchester's linear law for force-size estimation

Lanchester (1916) characterised attrition under aimed-fire engagement (square law) and unaimed / area-fire engagement (linear law). For the area / volume-fire regime governing the multi-tier force structure of §2, the linear law applies:

```
dR/dt = −a × B × R
dB/dt = −b × R × B

with
  R, B  = surviving force sizes (Red and Blue)
  a, b  = attrition coefficients (per-soldier per-unit-time kill rate)
```

Equilibrium engagement under symmetric linear-law conditions yields:

```
R_remaining / B_remaining = R_initial / B_initial
                            × exp((b − a) × ∫ B × R / R × B dt)
                            ≈ R_initial / B_initial  for a ≈ b
```

The unit-size ratios across §2.1 tiers (5 → 25 → 100 → 1 000 → 50 000) preserve the 5× / 4× / 10× / 50× force-aggregation multipliers that, under Lanchester linear, keep the force-ratio advantage of the higher-tier unit roughly constant against a peer adversary of the same nominal tier-size. The 5-person fire team is the minimum-viable manoeuvre unit at the attrition-coefficient `a ≈ 0.001 / soldier-hour` typical of small-arms engagement — below 5, statistical fluctuations in single-engagement outcomes dominate the linear-law expectation, making the unit operationally unreliable.

### A.2 Span-of-control optimisation (March-Simon hierarchy)

The §2.1 fire-team-to-squad ratio (5 : 25) and squad-to-platoon ratio (5 : 4 × 25 = 100) implicate a classic March / Simon hierarchical span-of-control argument. For a hierarchy of branching factor `b` and depth `d`, the total span is:

```
N_total = b^d                          # personnel at the leaf level
H = N_total × Σ (1 / b^i, i = 0..d−1)   # total headcount including all command tiers
                                        # ≈ N_total × b / (b − 1)  for large d
```

The cognitive-bandwidth ceiling on a single human supervisor is well-established at `b ≤ 25` (Miller's "magical number seven, plus or minus two" expanded by direct-supervision skill development; the Tony Buzan / Robin Dunbar literature places the upper bound at 25–50 for monitored direct relationships). The §2.1 tier-structure observes this ceiling at every level:

```
Fire Team:    b = 5     ✓ (well below 25)
Squad:        b = 5     ✓ (5 fire-team leaders supervised by squad leader)
Platoon:      b = 4     ✓ (4 squad leaders supervised by platoon leader)
Company:      b = 10    ✓ (10 platoon leaders supervised by company commander)
Battalion:    b = 50    ⚠ (above 25 — relies on staff-section delegation)
```

The Tier-5 50-companies-per-battalion ratio is the single deviation from the `b ≤ 25` rule and depends on the §2.2 staff-officer delegation structure to maintain command effectiveness. This is the structural origin of the §6.3 implementation-challenge framing: the Tier-5 span is operationally feasible only with explicit staff-officer headcount augmentation, which is not analysed in this paper. **The non-standard battalion-size definition (§Honest Framing) follows from this 50× span-multiplier choice.**

### A.3 Wright learning curve (training time model)

The 36-week training pipeline of §3 is structured as a three-phase learning sequence. The Wright (1936) learning curve characterises the time-per-unit reduction as cumulative repetition `N` increases:

```
L(N) = L_1 × N^(−b)

with
  L_1   = time required to complete the first unit (or skill repetition)
  b     = learning exponent — typically 0.32 for an 80 % learning rate
          (each doubling of cumulative repetitions cuts time per unit by 20 %)
  L(N)  = time per unit at the N-th cumulative repetition
```

For the §3.1 Phase 1 individual-skills track (16 weeks, weeks 1–8 + 9–16):

```
Skill domains: weapons, fieldcraft, fitness, equipment maintenance, communications
N_repetitions per skill domain at Phase 1 end ≈ 200 (8 weeks × 25 reps/week)
b ≈ 0.32                              # 80 % learning rate (US Army DOTMLPF baseline)
L(200) / L(1) ≈ 200^(−0.32) ≈ 0.18    # 82 % time-per-unit reduction
```

For the §3.2 Phase 2 squad-integration track (12 weeks) with a smaller N per drill type (~50 reps), the learning-curve reduction is `50^(−0.32) ≈ 0.29` — i.e., 71 % time-per-unit reduction. The §3.3 Phase 3 specialisation phase (8 weeks) sees the smallest N (~20 reps per specialisation) and the smallest reduction (`20^(−0.32) ≈ 0.39`).

The composite 36-week pipeline is therefore a sequence of three learning-curve regimes operating on three different N-scales:

```
Cumulative time-per-skill ratio = 0.18 (Phase 1) × 0.29 (Phase 2) × 0.39 (Phase 3)
                                ≈ 0.020
```

→ **Final-pipeline operator is ~50× faster per task than first-week recruit** — a doctrinal estimate consistent with the §3.4 "combat-ready specialist with leadership capability" output target. The 36-week budget is the minimum cumulative training time required to traverse all three learning-curve regimes; reducing it linearly truncates the deepest part of each curve and disproportionately reduces operator effectiveness against the §6.3 spec.

### A.4 Lanchester square law (peer adversary engagement)

For an aimed-fire engagement between peer formations (more relevant to the §1 doctrinal context than the area-fire linear law), the Lanchester square law applies:

```
dR/dt = −a × B
dB/dt = −b × R
R² − B² × (b/a) = R_initial² − B_initial² × (b/a) = constant

with the same a, b definitions as §A.1
```

The square law amplifies force-ratio asymmetries: a 25 % numerical advantage (e.g., 250 vs 200 soldiers) at parity attrition coefficients yields a `√(250² − 200²) ≈ 150` surviving Red force at Blue annihilation. This is the principal mathematical foundation for the §1 "concentration of force" principle and the §2 multi-tier hierarchy that enables rapid force concentration at the decisive point. ACMD's universal-leadership training principle (§3) targets the `a, b` attrition-coefficient terms specifically: a force with broader command-redundancy maintains the `a` coefficient under leadership casualties that would degrade a thin-leadership-cadre opponent's `a` toward zero.

---

## References
Biddle, S. (2004). Military Power: Explaining Victory and Defeat in Modern Battle. Princeton University Press.

Builder, C. H., Banks, S. C., & Nordin, R. (1999). Command Concepts: A Theory Derived from the Practice of Command and Control. RAND Corporation.

Department of the Army. (2019). ADP 6-0: Mission Command: Command and Control of Army Forces. Headquarters, Department of the Army.

Headquarters, Department of the Army. (2020). FM 7-0: Train to Win in a Complex World. US Army.

Klein, G. (2008). Naturalistic Decision Making. Human Factors, 50(3), 456–460.

NATO Standardization Office. (2019). Allied Tactical Publication ATP-3.2.2: Land Tactical Doctrine. NATO.

Shamir, E. (2010). Transforming Command: The Pursuit of Mission Command in the U.S., British, and Israeli Armies. Stanford University Press.

van Creveld, M. (1985). Command in War. Harvard University Press.

Wong, L., Bliese, P., & McGurk, D. (2003). Military leadership: A context specific review. The Leadership Quarterly, 14(6), 657–692.
