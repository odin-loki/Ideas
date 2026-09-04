# Defence manufacturing analysis: the forge-to-machine revolution

*How near-net-shape forging and advanced hard machining are rewriting the economics of defence manufacturing*

**Defence components are expensive. Not just because of the materials, the tolerances, or the quality assurance chains involved — but because of how inefficiently raw material moves through a traditional production process.**

A forged steel blank for a rifle receiver, a breech block, a vehicle suspension component, or an armour bracket typically follows a path like this: forge the rough shape, anneal it to soften it, send it to machining where it is roughed down in its soft state, send it to heat treatment where it is hardened to service specification, send it back to machining for finish passes, then grinding, then inspection. That is four to six separate process stages, multiple facility transfers, weeks of queue time, and a significant proportion of the original forging ending up as chips on the floor.

*The question worth asking is: what happens to that entire cost structure if you skip the annealing step entirely, deliver the forging in its hardened, near-net-shape condition, and machine it directly to final dimension in one setup?*

**What Near-Net-Shape Forging Actually Means**

Near-net-shape forging is not a new concept, but its combination with capable hard machining is. The idea is to design the forging die such that the blank leaving the forge is already close to final geometry — correct external profile, core features roughed in, minimal excess stock — and to quench and temper the component immediately after forging while the metallurgy is already at temperature. The part arrives at the machining cell already at its service hardness, typically HRC 52–64 for high-performance tool and alloy steels used in defence applications, with perhaps 0.5–2.0 mm of stock on critical surfaces rather than the 5–10 mm of stock on a conventionally over-forged soft blank.

Until recently, this approach was impractical at scale because no carbide tooling could survive production machining at HRC 55+ with acceptable tool life. CBN could, but CBN cannot be run in the small-diameter, complex-geometry end mill formats that defence component features demand. So the industry kept annealing and re-hardening, absorbing the cost because there was no alternative.

Advanced hard machining carbide systems capable of working up to HRC 70 change that calculus entirely.

**Breaking Down the Cost of the Traditional Route**

Consider a representative mid-complexity defence component — a hardened steel breech component for a crew-served weapon system, forged from H13 tool steel, service hardness HRC 52–56, with a finished weight of approximately 1.8 kg and a raw forging weight of roughly 3.5 kg. The traditional production route incurs costs across several distinct buckets.

**Material Waste**

The difference between the 3.5 kg forging and the 1.8 kg finished part is 1.7 kg of H13 steel converted to chips. In a soft pre-machined state that stock removal is done quickly but carelessly — high feeds, aggressive depths, low surface quality — because it all gets re-machined after hardening anyway. This means the pre-machining step adds cost without adding value to the final part. If the forging arrives near-net with 0.5 mm stock rather than 5 mm, the waste drops from 1.7 kg to perhaps 0.3 kg per part. At current H13 pricing of approximately AUD $8–12 per kg in defence-grade bar stock, that is a saving of roughly AUD $11–17 per part in raw material alone, before any process costs are considered.

**Energy and Furnace Time**

An anneal cycle for H13 steel runs at 850–900°C for 2–4 hours followed by controlled cooling over 12–24 hours to prevent cracking. A subsequent hardening and tempering cycle — quench from 1020°C, double temper at 550–600°C — adds another 8–12 hours of furnace time. Each furnace cycle carries energy cost, fixture cost, atmosphere gas cost, and critically, occupancy cost on capital equipment that typically has a queue. In a defence production environment running multiple component types, furnace scheduling is frequently the bottleneck that adds 3–7 days to lead time per batch. Eliminating the anneal cycle removes one full furnace pass. Eliminating the re-harden cycle by delivering the part already at service hardness removes a second. The two combined can remove 5–10 days from the production timeline on a per-batch basis.

**Handling and Transfer Costs**

Each time a component moves — from forge shop to heat treat, heat treat to rough machine, rough machine back to heat treat, heat treat to finish machine — it accrues transport cost, re-inspection cost, potential damage risk, and administrative overhead in the works order system. In a defence supply chain operating under AS9100 or ITAR-adjacent quality frameworks, each transfer point is also a documentation event. Reducing four transfers to one is not a marginal improvement; it compresses the entire quality trail and reduces the probability of non-conformance events that trigger rework loops.

**Tooling Cost**

Soft pre-machining consumes HSS or uncoated carbide at low cost per edge but uses many edges because the stock removal volume is large. Finish machining after hardening consumes premium coated carbide at high cost per edge, but tool life at HRC 52–56 even with current AlTiN coatings is short enough that tool changes are frequent. A capable hard machining system that does all stock removal in one pass — rough to finish — at HRC 52–64 consolidates tooling spend into a single, optimised tool type and eliminates the redundant soft-machining tooling category entirely.

**Quantifying the Combined Effect**

Modelling the full cost differential across these categories for the representative H13 breech component, based on published defence manufacturing cost studies and Australian defence industry benchmarks:

**Cost / Time Element**

**Traditional Route**

**Forge-to-Machine Route**

Raw material waste per part

1.7 kg (~AUD $17)

0.3 kg (~AUD $3)

Furnace cycles required

2 (anneal + harden)

0 (in-line quench at forge)

Furnace time per batch

20 – 36 hours

Eliminated

Process stages

5 – 6 stages

2 stages

Facility transfers

4 transfers

1 transfer

QA documentation events

4 – 6 hold points

1 – 2 hold points

Total processing cost (per part)

AUD $340 – $420

AUD $190 – $240

Lead time (forge to inspection-ready)

18 – 26 working days

6 – 9 working days

Cost reduction

—

~40 – 45%

Lead time reduction

—

~65 – 70%

On a production run of 500 components — a modest quantity for a weapons programme — the cost differential is AUD $50,000–$90,000 and the schedule differential is 9–17 working days. On a programme scale of tens of thousands of components over a contract life, both figures become strategically significant.

**Where the Hard Machining System Becomes the Enabling Technology**

None of the above numbers are achievable without tooling capable of performing reliable, repeatable hard machining from rough to finish in a single setup. The hard machining system must handle three demanding conditions simultaneously.

- Entry cuts into scale and decarburised surface layer at full hardness — typically the most aggressive condition, where thermal shock and abrasion combine. Trochoidal toolpath strategies absorb this by keeping radial engagement low and arc entry smooth, but the tool must survive it.
- Deep cavity features — locking recesses, pin bores, gas escape channels — machined at full HRC with small-diameter tooling where tool deflection and vibration are severe. Negative rake geometries with high flute counts address this by distributing cutting load and stiffening the effective cutting system.
- Tight tolerances to finished dimension without a subsequent grinding step on non-critical surfaces. A hard milling system running at appropriate parameters on a rigid machine (HMC or 5-axis VMC with HSK-A63 spindle, minimum 40 kN spindle bearing preload) can achieve IT7 tolerance and Ra 0.4–0.8 µm surface finish directly from milling — adequate for the majority of defence component functional surfaces.

**Beyond Unit Cost — The Strategic Value of Compressed Lead Time**

In defence procurement, lead time is not just a logistics variable — it is an operational risk variable. The ability to surge production of a component from 50 to 500 units per month in response to an urgent operational requirement is constrained, in a traditional multi-stage process, by furnace capacity, by heat treatment queue, and by the cumulative scheduling complexity of coordinating five process stages across potentially three or four different facilities.

*A forge-to-machine pipeline with single-step hard machining capability is surge-capable in direct proportion to machine tool capacity alone. Adding a machining shift or a second machine centre doubles output. There is no furnace bottleneck to negotiate, no inter-facility transfer to coordinate, no annealing queue to jump.*

The supply chain becomes as agile as the machining floor, and the machining floor is the most flexible element in any metal manufacturing facility. For a defence contractor operating under delivery performance KPIs — or under contractual on-time delivery obligations with liquidated damages provisions — that flexibility has a value that does not appear on any per-part cost calculation but is immediately visible on the programme risk register.

## Conclusion

The combination of near-net-shape forging with direct hard machining capability does not represent an incremental improvement to defence component manufacturing. It represents a structural simplification of the production process — fewer stages, fewer transfers, less material waste, less energy consumption, and a lead time that compresses by two-thirds.

The enabling constraint has always been tooling capability at high hardness. With that constraint removed, the economic case for forge-to-machine as the default production architecture for hardened steel defence components is, on the numbers, compelling.

The question for defence manufacturers is no longer whether this approach is technically feasible. It is whether the production planning, supply chain design, and capital investment decisions are aligned to take advantage of it.

*Defence Manufacturing Analysis  ·  Near-Net-Shape Forging & Hard Machining Economics  ·  Restricted Distribution*
