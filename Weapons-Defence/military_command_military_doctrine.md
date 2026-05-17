# Adaptive Command Military Doctrine

*Operator Specification Sheet*

Document No. TRP-2026-111 | Version 1.0

Prepared for: Australian Department of Defence

Classification: UNCLASSIFIED // FOR OFFICIAL USE ONLY

Date: May 2026

> **The Adaptive Command Military Doctrine is a hypothetical hierarchical infantry command-and-training framework structured across five named tiers — Fire Team (5 personnel) → Squad (25, = 5 Fire Teams) → Platoon (100, = 4 Squads) → Company (1 000, = 10 Platoons) → Battalion (50 000, = 50 Companies) — coupled to a 36-week training pipeline (16 weeks basic infantry + 12 weeks advanced squad operations + 8 weeks specialised role training) under a 40 / 30 / 20 / 10 allocation across individual technical skills / small-unit leadership / specialised roles / cross-training. The doctrine emphasises distributed command authority, universal leadership capability, and rapid succession on casualty. This document is purely doctrinal — `weapons_simulation.py` does NOT model command-and-control, force-on-force outcomes, training pipeline throughput, or unit-cost economics, so no numerical claim in this paper is anchored to the portfolio simulator. The classification banner above is illustrative for portfolio tonal consistency, not a real security marking.**

## Honest framing

- **Doctrinal proposal, not simulated outcome.** This document is a paper concept for command structure and training. No force-on-force wargame, no agent-based simulation, no analytic-model output, and no published peer-reviewed analysis underwrites its effectiveness claims. The simulator that anchors the rest of this portfolio (`weapons_simulation.py`) does not cover command-and-control, training-pipeline throughput, or force-structure economics.
- **Unit-strength numbers are notional and inconsistent with standard NATO usage.** The 50 000-personnel "Battalion" tier is approximately 50–100× the size of a standard NATO infantry battalion (typically 300–1 000 personnel) — in NATO terms, 50 000 is a corps-equivalent (3–5 divisions). The document also opens by describing a "six-tier hierarchical system" but enumerates only five tiers (Fire Team through Battalion). These are document-internal naming choices, not standard ADF / NATO usage, and should be read accordingly. Flag for portfolio follow-up: reconcile the tier-naming with standard ADF doctrine or rename the tiers explicitly.
- **Training-pipeline duration not benchmarked.** The 16 + 12 + 8 = 36-week initial pipeline (plus 6 / 12 / 16 weeks of additional command training for higher tiers) is target-based; it has NOT been benchmarked against current ADF Royal Military College and School of Infantry training-establishment throughput, instructor-cadre availability, or recruit attrition rates.
- **Personnel economics not modelled.** A 50 000-personnel "Battalion" implies sustained recruiting, retention, pay, accommodation, equipment, and ammunition allocations far above current ADF infantry size (~30 000 active across the entire Australian Army). The document does not quantify these costs, nor the implications of the "universal leadership capability" training overhead applied at the full force scale.
- **No mention of joint enablers.** The doctrine is land-force-only and silent on air, maritime, cyber, electronic-warfare, intelligence, logistics, and combat-support enablers. Modern combined-arms operations are not addressable purely by the infantry tier structure described.
- **Single source of truth for numbers.** Where this doctrine intersects fielded ADF or NATO doctrine, those publications are authoritative; this document is a portfolio-internal concept piece only.
- **Classification banner is illustrative.** UNCLASSIFIED // FOUO format and the TRP-2026 numbering are adopted for tonal coherence with the rest of the `Weapons-Defence/` portfolio. No real sponsorship, no real programme office, no adopted doctrine implied.

---

## Command Structure Overview

The doctrine operates on a six-tier hierarchical system designed for maximum flexibility and distributed leadership:

### Tier 1: Fire Team (5 personnel)
- **Unit Size**: 5 soldiers
- **Command**: Team Leader + 4 operators
- **Designation**: Alpha through Echo teams within squads

### Tier 2: Squad (25 personnel) 
- **Unit Size**: 5 Fire Teams (25 soldiers total)
- **Command**: Squad Leader + 5 Team Leaders
- **Designation**: Numbered squads (1st Squad, 2nd Squad, etc.)

### Tier 3: Platoon (100 personnel)
- **Unit Size**: 4 Squads (100 soldiers total)
- **Command**: Platoon Leader + 4 Squad Leaders
- **Designation**: Lettered platoons (Alpha, Bravo, Charlie, Delta)

### Tier 4: Company (1,000 personnel)
- **Unit Size**: 10 Platoons (1,000 soldiers total)
- **Command**: Company Commander + 10 Platoon Leaders
- **Designation**: Numbered companies within battalions

### Tier 5: Battalion (50,000 personnel)
- **Unit Size**: 50 Companies (50,000 soldiers total)
- **Command**: Battalion Commander + 50 Company Commanders
- **Designation**: Numbered battalions within the force structure

## Training Philosophy

### Core Principle: Universal Leadership Capability
Every soldier receives foundational command training to enable effective coordination at the fire team and squad level, creating a resilient command structure that can adapt to casualties and changing tactical situations.

## Infantry Training Regimen

### Phase 1: Basic Infantry Training (16 weeks)
**Weeks 1-8: Individual Skills**
- Marksmanship and weapons proficiency
- Physical conditioning and endurance
- Basic survival and field craft
- Equipment maintenance and logistics
- Communication systems and protocols

**Weeks 9-16: Small Unit Leadership**
- Fire team tactics and coordination
- Basic command principles and decision-making
- Situational awareness and battlefield assessment
- Emergency leadership protocols
- Cross-training on all fire team positions

### Phase 2: Advanced Squad Operations (12 weeks)
**Weeks 1-6: Squad Integration**
- Multi-team coordination exercises
- Squad-level tactical operations
- Resource management and allocation
- Inter-team communication protocols
- Casualty response and command succession

**Weeks 7-12: Leadership Development**
- Tactical decision-making under pressure
- Mission planning and briefing techniques
- Stress inoculation training
- Adaptive leadership scenarios
- Command post operations

### Phase 3: Specialized Role Training (8 weeks)
**Weeks 1-4: Technical Specialization**
- Communications specialists
- Medics and field medicine
- Heavy weapons operators
- Reconnaissance and intelligence
- Logistics and supply coordination

**Weeks 5-8: Cross-Training**
- Exposure to all specialized roles
- Emergency succession protocols
- Multi-role capability development
- Advanced equipment familiarization

## Command Development Track

### Tier 1-2 Leaders (Team/Squad Leaders)
**Selection Criteria:**
- Demonstrated performance in basic training
- Leadership aptitude assessment
- Peer evaluation scores
- Stress response evaluation

**Additional Training (6 weeks):**
- Advanced tactical planning
- Personnel management
- Resource allocation
- Multi-unit coordination
- Mentorship and development skills

### Tier 3-4 Leaders (Platoon/Company Commanders)
**Prerequisites:**
- Minimum 2 years successful squad leadership
- Advanced military education
- Specialized forces experience recommended
- Command assessment completion

**Additional Training (12 weeks):**
- Strategic planning and analysis
- Multi-domain operations
- Advanced communication systems
- Logistics and supply chain management
- Inter-agency coordination

### Tier 5 Leaders (Battalion Commanders)
**Prerequisites:**
- Special forces background required
- All prerequisite training completed
- Minimum 5 years company-level command
- Advanced staff college graduation
- Multi-national exercise participation

**Additional Training (16 weeks):**
- Strategic-level planning
- Joint operations coordination
- Advanced intelligence analysis
- Political-military considerations
- Crisis management and decision-making

## Doctrine Implementation Principles

### Distributed Command Authority
- Each level maintains autonomous decision-making capability
- Upward reporting with downward delegation
- Rapid adaptation to changing battlefield conditions
- Redundant command structures at all levels

### Flexible Training Allocation
- 40% individual technical skills
- 30% small unit leadership and coordination
- 20% specialized role training
- 10% cross-training and adaptability

### Continuous Development
- Regular leadership rotation exercises
- Scenario-based training with leadership casualties
- Multi-level command post exercises
- Inter-unit exchange programs

## Advantages of This Structure

### Resilience
- Multiple layers of trained leadership
- Reduced vulnerability to command disruption
- Rapid reorganization capability
- Maintained effectiveness despite casualties

### Adaptability
- Flexible response to changing mission requirements
- Scalable operations from small to large units
- Cross-trained personnel for multiple roles
- Rapid integration of replacement personnel

### Effectiveness
- Distributed decision-making reduces response time
- Enhanced coordination at all levels
- Improved mission success rates
- Higher personnel retention and morale

## Implementation Considerations

### Resource Requirements
- Extended training periods require significant investment
- Specialized instructor cadre needed
- Advanced training facilities and equipment
- Continuous education and development programs

### Quality Control
- Rigorous selection and assessment processes
- Regular competency evaluations
- Standardized training protocols
- Performance-based advancement criteria

### Integration Challenges
- Coordination with existing military structures
- Standardization across different units
- Maintenance of doctrine consistency
- Adaptation to technological changes

---

## Appendix A — Quantitative Foundations

This appendix gathers standard operational-research constructs used to motivate (not simulate) structural claims embedded in doctrine text: lethality accumulation, supervisory span, throughput learning over the training pipeline, and command-cycle timing.

### A.1 Lanchester linear law — force exchange and ladder concentration

Under **linear** (unit-for-unit aimed fire against fielded shooters) modelling, opposing force attrition scales with surviving enemy shooters:

```
dB/dt = −α · R       (similarly  dR/dt = −β · B  in symmetric formulations)
```

- **B**, **R** — force levels (soldiers firing effectively) over time **t**.
- **α**, **β** — kill effectiveness per adversary shooter per unit time (doctrine-specific; terrain, cover, ISR, lethality aggregated).

Interpretation for this doctrine’s **Fire Team → … → Battalion** numbering ladder (**5 → 25 → 100 → 1 000 → 50 000**): concentrating **25** cooperating shooters at squad scale increases **effective α** versus isolated teams because spotting, arcs, suppression, and cross-fire raise the probability mass on **successful aimed shots** versus the same shooters scattered without mutual support — the Lanchester-linear framework expresses why **whole-unit employment** dominates piecemeal commitment when engagement is reciprocal directed fire rather than asymmetric area fire.

*(This appendix does not quantify α, β — the portfolio simulator deliberately excludes force-on-force command outcomes.)*

### A.2 Span-of-control optimisation — branching tree and supervisory limits

Treat command links as an ideal **uniform tree** height **d** with average outgoing degree **b** (direct reports per leader):

```
N_total ≈ b^d
```

- **b** — branching factor (direct subordinates per leader).
- **d** — command depth (organisational levels from base element to formation apex).
- **N_total** — maximum distinct **bottom-level** positions under one apex if every node is filled.

**Cognitive bound:** operational literature often cites **Miller (1956)** **7 ± 2** **chunks** of immediate information; under combat stress, modern staff practice typically compresses **simultaneous direct supervision** toward **5–9** active subordinate tracks. The doctrine’s **b = 5** fire-team base is consistent with the **low-stress** end of that band; **b ≤ 25** is an **absolute structural ceiling** for formal tree width (not a recommendation for daily supervision load).

**Numeric illustration (notional):** with **b = 5** and **d = 4**, **5⁴ = 625**, i.e., **six hundred twenty-five base slots** reachable from **four** supervisory layers atop a quintuple fan-out — illustrative of mid-scale company-like aggregation mathematics; this document maps **five** teams of five to **twenty-five-person** squads, so hierarchical consistency should be validated against ADF / NATO nomenclature as noted in **Honest framing**.

### A.3 Wright/Crawford unit learning curve — multi-phase throughput

Let **N** denote cumulative homogeneous units processed; per-unit labour or calendar time improves with experience:

```
L(N) = L₁ · N^(−b_w)
```

- **L(N)** — time (or labour cost proxy) required for the **N**th homogeneous unit once the process has stabilised toward steady learning.
- **L₁** — time for the **first** unit (epoch anchor).
- **b_w** — learning exponent; **b_w ≈ 0.152** is the classic **90 % / double production** airframe rule (each doubling drops unit time to **90 %** of prior).

The doctrine’s **36-week** initial pipeline (**16 + 12 + 8 weeks**) can be read as **three phases** each with its own **(L₁, b_w)** pair: individual skills (weeks 1–8), small-unit leadership (weeks 9–16), **then** squad integration (phase 2) and specialisation (phase 3). Transitions reset part of the learning stock (new tasks, new instructors), so aggregate throughput is **not** a single global Wright curve — it is a **concatenation** of segments with **local** exponents.

## IP, Licensing, and Applicability

This document is a **doctrine paper**, not a manufacturable product. There is nothing to licence, manufacture, or procure as a physical system. However, the intellectual contributions of this work are:

| IP asset | Description | Protection approach |
|---|---|---|
| **ACMD command-tier architecture** | The specific 5-tier hierarchy (Fire Team → Squad → Platoon → Company → Battalion) and the corresponding span-of-control ratios (5/5/4/10/50) as a coherent doctrine package | Open publication; doctrine is inherently intended for adoption |
| **36-week phased training pipeline** | The 16+12+8 week allocation with the 40/30/20/10 effort distribution per phase | Open publication |
| **Quantitative OODA / Lanchester doctrine integration** | The explicit mathematical formalisation of mission-command speed advantages in the Lanchester and Boyd frameworks (Appendix A) | Open publication; may be cited academically |

**Applicability.** This doctrine is intended for adoption by ADF units, allied forces, and defence academia without licence or royalty requirement — doctrine serves no purpose if it is not adopted. Any jurisdiction wishing to adapt ACMD for their own force structure may do so freely, with attribution.

**Export controls.** Military doctrine documents are classified by content sensitivity, not by category. This document (UNCLASSIFIED // FOUO-style) carries no DSGL controls. Distribution to partner nations under existing Five-Eyes and bilateral information-sharing frameworks (AUSMIN, AUKUS) is unrestricted at UNCLASSIFIED level.

---

### A.4 Boyd OODA loop timing — five-tier decentralisation

Boyd’s decision cycle decomposes into serial components:

```
T_decision = T_observe + T_orient + T_decide + T_act
```

- **T_observe** — sensor / report intake latency.
- **T_orient** — fusion, threat classification, rules-of-engagement / mission alignment (often dominant under fog).
- **T_decide** — option selection and orders drafting.
- **T_act** — physical execution + feedback.

**Qualitative claim in this doctrine:** delegating **rules-of-engagement‑constrained** choices to **lower tiers** shrinks **T_orient** and **T_decide** for local surprises because data does not traverse the full tree before **acceptable** actions are authorised — **subject to** training, trust, and legal mandate. The document does not assign seconds-level benchmarks; the inequality direction is **hierarchical centralisation ↑ latency** vs **mission command ↓ local latency** when leadership depth is trusted and competent.
