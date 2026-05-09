# Weapons — defence-tech R&D portfolio

> **A serious defence-engineering portfolio, formatted as the kind of internal R&D documentation a small-team defence-systems research division would produce: every top-level platform has a paired operator-facing specification sheet and a TRP-numbered research paper, organised across small-arms (`MP-6.8` rifle, `MP-4.6M` pistol/PDW, MAS-15.2E `15.2mm` anti-materiel sniper), heavy weapons (`57mm` autocannon / underbarrel grenade / mortar-RPG, `140mm` tank round), body armour (APES, AlNiCyN tiered armour, OBSIDIAN / OBSIDIAN-X), CBRN protection (NACS / NEXUS Adaptive Combat System), tactical acoustic cancellation (TACS), hearing protection, energy nutrition (ASNP), military command doctrine, rubber track pads, CL-20 high explosive, caseless / cartridgeless ammunition, and combat / nutrition pharmacology.** Specification numbers are in the brochure-credible range for genuine defence concepts (`sub-MOA at 800 m`, `1 000 m/s` muzzle velocity, `12 mm RHA at 300 m`, `35 – 55 dB` cancellation depth at TACS nodes, `100 % – 0 false alarms`), with academic hedging on the explicitly-hypothetical items (OBSIDIAN-X labelled "Hypothetical / For Academic Study"). The classification banners are stylistic — UNCLASSIFIED / FOUO format — not real classification, sponsorship, or fielded materiel.

> **Genre note.** Documents adopt a defence-research register (Advanced Defence Systems Research Division, March 2026, UNCLASSIFIED / FOR OFFICIAL USE ONLY) for tonal coherence. No real classification, no real programme office, no fielded systems are implied.

---

## What this folder is

Defence engineering as a documentation discipline has a very particular register: paired specification-and-research-paper documents, TRP (Test and Research Program) designators, comparative tables against fielded incumbents, classification banners, explicit human-factors and safety considerations. Most "speculative weapons" content on the open web is written in fiction-author register and mixes the technical with the operatic. This folder takes the opposite tack — adopt the *defence-engineering documentation register* and produce a consistent multi-platform portfolio inside that register, with all the supporting pieces (NACS-TOTAL signature reduction analysis, AlNiCyN three-tier armour cost model, TACS cancellation-zone physics, rubber-track-pad noise-reduction calculations, ASNP energy-drink pharmacology) one would expect of a real R&D division. The result reads like a small-team defence-systems portfolio.

The cohesion is unusual: every top-level weapon has a *pair* of files (operator spec + research paper), every system has a TRP designator, the AlNiCyN armour cost model uses the same currency convention as the H13-breech forge-to-machine analysis in [`../Rockwell 50 to 70 Carbide/`](../Rockwell%2050%20to%2070%20Carbide/), and the OBSIDIAN-X "Hypothetical" tag is explicit so a reader does not confuse it with the AlNiCyN-5000 tier-1 (`TRL 7-8`) armour.

---

## 📑 Source organisation

### Top-level operator specifications + paired research papers

| System | Operator spec | Research paper |
|---|---|---|
| **MAS-15.2E Anti-Tank Sniper** | [`15.2mm Anti-Tank Sniper System.md`](15.2mm%20Anti-Tank%20Sniper%20System.md) | [`Research Papers/Paper1_MAS152E_AntiTank_Sniper.md`](Research%20Papers/Paper1_MAS152E_AntiTank_Sniper.md) |
| **MP-6.8 Mark II Rifle** | [`MP-6.8 Advanced Combat Rifle.md`](MP-6.8%20Advanced%20Combat%20Rifle.md) | [`Research Papers/Paper10_MP68_Rifle.md`](Research%20Papers/Paper10_MP68_Rifle.md) |
| **MP-4.6M Pistol** | [`MP-4.6M Pistol.md`](MP-4.6M%20Pistol.md) | [`Research Papers/Paper9_MP46M_Pistol.md`](Research%20Papers/Paper9_MP46M_Pistol.md) |
| **MP-4.6M Defender PDW** | [`MP-4.6M Defender PDW.md`](MP-4.6M%20Defender%20PDW.md) | [`Research Papers/Paper8_MP46M_PDW.md`](Research%20Papers/Paper8_MP46M_PDW.md) |
| **57 mm Autocannon** | [`57mm Advanced Mechanical Autocannon System.md`](57mm%20Advanced%20Mechanical%20Autocannon%20System.md) | [`Research Papers/Paper2_57mm_Autocannon.md`](Research%20Papers/Paper2_57mm_Autocannon.md) |
| **57 mm Underbarrel Grenade** | [`57mm Underbarrel Grenade Round.md`](57mm%20Underbarrel%20Grenade%20Round.md) | [`Research Papers/Paper4_57mm_Underbarrel_Grenade.md`](Research%20Papers/Paper4_57mm_Underbarrel_Grenade.md) |
| **57 mm Mortar / RPG dual-purpose** | [`57mm Enhanced Dual-Purpose System Mortar and RPG.md`](57mm%20Enhanced%20Dual-Purpose%20System%20Mortar%20and%20RPG.md) | [`Research Papers/Paper3_57mm_DualPurpose_System.md`](Research%20Papers/Paper3_57mm_DualPurpose_System.md) |
| **140 mm Tank KE Round** | [`140mm Advanced Multi-Effect Tank Round.md`](140mm%20Advanced%20Multi-Effect%20Tank%20Round.md) | [`Research Papers/Paper5_140mm_Tank_Round.md`](Research%20Papers/Paper5_140mm_Tank_Round.md) |
| **APES Body Armour System** | [`Advanced Protective Equipment System Specification.md`](Advanced%20Protective%20Equipment%20System%20Specification.md) | [`Research Papers/Paper6_Body_Armor_System.md`](Research%20Papers/Paper6_Body_Armor_System.md) |
| **NACS / NEXUS Adaptive Combat System** | [`NACS TOTAL Camo and Undersuit.md`](NACS%20TOTAL%20Camo%20and%20Undersuit.md) | [`Research Papers/Paper7_NACS_CBRN_System.md`](Research%20Papers/Paper7_NACS_CBRN_System.md) |
| **AlNiCyN Aluminium Armour** | [`Aluminium Alloys for Armour.md`](Aluminium%20Alloys%20for%20Armour.md) | [`Research Papers/Paper13_AlNiCyN_Aluminum_Armour.md`](Research%20Papers/Paper13_AlNiCyN_Aluminum_Armour.md) |
| **Hearing Protection** | [`military_hearing_protection_systems.md`](military_hearing_protection_systems.md) | [`Research Papers/Paper15_Hearing_Protection.md`](Research%20Papers/Paper15_Hearing_Protection.md) |
| **Military Command Doctrine** | [`military_command_military_doctrine.md`](military_command_military_doctrine.md) | [`Research Papers/Paper16_Military_Command_Doctrine.md`](Research%20Papers/Paper16_Military_Command_Doctrine.md) |

### Hypothetical / academic-study items

| Item | File |
|---|---|
| **OBSIDIAN body armour (hypothetical)** | [`Research Papers/OBSIDIAN_Research_Paper.md`](Research%20Papers/OBSIDIAN_Research_Paper.md) |
| **OBSIDIAN-X body armour (hypothetical)** | [`Research Papers/OBSIDIAN_X_Research_Paper.md`](Research%20Papers/OBSIDIAN_X_Research_Paper.md), [`Hypothetical Body Armour.md`](Hypothetical%20Body%20Armour.md) |
| **Hypothetical secret-service suit** | [`Hypothetical_secret_service_suit_specs.md`](Hypothetical_secret_service_suit_specs.md) |
| **Combat drug — HyperSynergy-X7** | [`Combat Drug.md`](Combat%20Drug.md), [`Research Papers/Paper18_HyperSynergy_X7_Combat_Drug.md`](Research%20Papers/Paper18_HyperSynergy_X7_Combat_Drug.md) — mirrored to [`../Drugs/Combat Drug.md`](../Drugs/Combat%20Drug.md) |
| **Injectable nutrition** | [`Injectable Food.md`](Injectable%20Food.md), [`Research Papers/Paper17_Injectable_Nutrition.md`](Research%20Papers/Paper17_Injectable_Nutrition.md) — mirrored to [`../Drugs/Injectable Food.md`](../Drugs/Injectable%20Food.md) |
| **ASNP energy drink** | [`Research Papers/ASNP_Energy_Drink_Research_Paper.md`](Research%20Papers/ASNP_Energy_Drink_Research_Paper.md) |
| **Caseless / cartridgeless bullets** | [`Caseless Bullets_README.md`](Caseless%20Bullets_README.md), [`Research Papers/Cartridgeless Bullets_Research_Paper.md`](Research%20Papers/Cartridgeless%20Bullets_Research_Paper.md) |

### Specialised subfolders

| Subfolder | Contents |
|---|---|
| [`Military Noise Cancellation/`](Military%20Noise%20Cancellation/) | **TACS** Tactical Acoustic Cancellation System — [`TACS_Complete_Specification.md`](Military%20Noise%20Cancellation/TACS_Complete_Specification.md), [`Paper11_TACS_System.md`](Military%20Noise%20Cancellation/Paper11_TACS_System.md), [`Paper12_TACS_Energy_Physics.md`](Military%20Noise%20Cancellation/Paper12_TACS_Energy_Physics.md), [`TACS_Energy_Conservation_Analysis.md`](Military%20Noise%20Cancellation/TACS_Energy_Conservation_Analysis.md). Three variants (Personal / Mobile / Fixed). |
| [`Rubber Tank Tracks/`](Rubber%20Tank%20Tracks/) | **MIL-SPEC track-pad TDP** (TRP-2026-014) — [`Paper14_Military_Track_Pad.md`](Rubber%20Tank%20Tracks/Paper14_Military_Track_Pad.md), [`MIL_SPEC_TRACK_PAD_TDP.md`](Rubber%20Tank%20Tracks/MIL_SPEC_TRACK_PAD_TDP.md), [`EXECUTIVE_SUMMARY.md`](Rubber%20Tank%20Tracks/EXECUTIVE_SUMMARY.md). HNBR/NBR/NR/Neoprene blend, score `6 679 / 10 000`, **`15 – 20 dB` noise reduction** vs steel. |
| [`CL-20 High Explosive/`](CL-20%20High%20Explosive/) | **Proteinated CL-20 safe-handling explosive paper** — [`Proteinated_CL20_Safe_Explosive_Paper.md`](CL-20%20High%20Explosive/Proteinated_CL20_Safe_Explosive_Paper.md), [`CL-20 HE Readme.md`](CL-20%20High%20Explosive/CL-20%20HE%20Readme.md). |

---

## 🧠 Headline platforms (specification highlights)

### Small arms

**MAS-15.2E Mark III Anti-Tank Sniper** + **15.2 × 115mm APYT cartridge** — `13.2 kg` empty, `1 420 mm` OAL / `720 mm` stowed, `8`-round magazine, **`sub-MOA at 800 m`**, **`30 mm RHA at 1 000 m`**, stock lock at `RC 60` with `0.0005 in` mating tolerance, **`< 30 s` field assembly**. Barrel: chrome-hammer-forged Stellite-21-lined, **`1 500-round` life**.

**MP-6.8 Mark II Combat Rifle** — `6.8 × 51mm`, **`1 000 m/s` muzzle velocity, `4 000 J` energy**, `50`-round magazine, `800 rpm`, **`12 mm RHA at 300 m`**, `62 000 PSI`, **`1 MOA at 100 m`**. Energy multiples vs `5.56` and `7.62` documented in the paper.

### Heavy weapons

**140mm tank KE round** — **`1 950 m/s` muzzle velocity, `57 MJ` energy, `880 MPa` chamber pressure**. Penetrator RHA claims at the high end (`~1 450 mm at 0 m` in-source, stepping down with range) are extreme even for in-universe defence specifications — read as design-target, not measured.

### NACS / NEXUS Adaptive Combat System (TRP-2026-007)

**`72 h` sealed operations.** GORE-Tex CHEMPAK core. **`65 – 92 % IR signature reduction`** (overgarment). GHOST rebreather: dual `300 bar` cylinders, LiOH scrubbing (`2 LiOH + CO₂ → Li₂CO₃ + H₂O`). Cost: **`AUD ~$504` per unit at `50 000`-unit volume**. SEAL gloves / socks / balaclava. Pharmacology stack: caffeine, modafinil, dextroamphetamine.

### TACS (Tactical Acoustic Cancellation)

| Variant | Cancellation zone | Cancellation depth | Anti-node | Power | Weight | Latency |
|---|---|---|---|---|---|---|
| **Personal** | `3 – 5 m` | `35 – 55 dB` at nodes | `+3 – 6 dB` | `35 – 70 W` | `5.5 kg` | **`< 100 µs`** |
| **Mobile** | `8 – 15 m` | (same) | (same) | `0.8 – 1.8 kW` | `245 kg` | (same) |
| **Fixed** | `30 – 60 m` | (same) | (same) | `3 – 8 kW` | `1 800 kg` | (same) |

Programme cost framing: `USD 22 M`, `36`-month timeline; per-unit `USD 28K / 185K / 850K`. The papers stress that **acoustic energy is redistributed, not destroyed** — there are anti-node hazards.

### APES Body Armour (TRP-2026-006)

**16-layer Kevlar / UHMWPE** with graphene interfaces. **`7075-T6` honeycomb + `B₄C` ceramic + `Ti-6Al-4V`**. Non-Newtonian silicone shock-absorber. **`20.8 kg` full kit**. **`< 3 s` emergency doff**. **PCM thermal at `28 °C`, `200 kJ/kg`, `25 %` body coverage → `4 h` thermal budget**.

### AlNiCyN Aluminium Armour (TRP-2026-013)

| Tier | Strength | Hardness | RHA equivalent | Cost | TRL |
|---|---|---|---|---|---|
| **AlNiCyN-5000** | `620 MPa` | `380 – 420 HB` | `1.0 ×` RHA | **`USD 11 830 / t`** | **`7 – 8`** (near-deployable) |
| **AlNiCyN-7000** | `780 MPa` | `550 – 650 HV` | (improved) | `USD 168 900 / t` | `4 – 5` |
| **AlNiCyN-X** | (target) | (target `~2 000 GPa` modulus) | (target) | `USD 320 000 / kg` | `2 – 3` (frontier) |

### Rubber tank-track pad (TRP-2026-014)

HNBR / NBR / NR / Neoprene blend `40 / 30 / 25 / 5 phr`. **`Shore A 72`, `≥ 26 MPa` tensile, `≥ 95 N/mm` tear, `5 s` self-extinguish, `12-min` install.** Score **`6 679 / 10 000`** across terrains. **`25-yr` cost `USD 282 235` per tank, `USD 2.82B` for `10 000` tanks. `15 – 20 dB` noise reduction** vs steel tracks.

### Hypothetical OBSIDIAN family

| System | Mass | Strength target | Programme cost | Status |
|---|---|---|---|---|
| **OBSIDIAN** | `11.8 kg` | (≥ 4-layer stack) | `USD ~40 M / unit` | **Hypothetical / For Academic Study** |
| **OBSIDIAN-X** | `18.5 kg` | `5 ×` strength target | **`USD 3.1 trillion` programme** | **Hypothetical / For Academic Study** |

---

## 📊 Reference-grade benchmarking style

The folder consistently benchmarks against fielded incumbents — Barrett M82 / M107, Snipex Alligator, JSLIST CBRN ensemble, IVAS / Warrior Web, Russian T-90 main armament — and presents specifications side-by-side. **No independent test data from this repository proves any field performance.**

---

## 🚧 Honest caveats (called out in source)

- **Classification banners are illustrative, not real.** UNCLASSIFIED / FOUO format adopted for tonal coherence; no actual security classification or sponsorship is implied or held.
- **OBSIDIAN and OBSIDIAN-X are explicitly hypothetical** with low TRL (`2 – 3` / academic-study). Read separately from AlNiCyN-5000 (`TRL 7 – 8`).
- **TACS warns of anti-node hazards.** Acoustic energy is redistributed, not destroyed; standing in an anti-node is dangerous.
- **NACS pharmacology** (caffeine + modafinil + dextroamphetamine) is contested ethically and legally in real militaries.
- **Many specifications are author-engineered "wouldn't-it-be-nice" targets** rather than measured prototypes.
- **140 mm penetration figures at the high end are extreme even by in-universe defence-spec standards** — design-targets, not validated measurements.

---

## 🔗 Related work in this repo

- [`../Rockwell 50 to 70 Carbide/`](../Rockwell%2050%20to%2070%20Carbide/) — sovereign manufacturing (the H13 breech exemplar)
- [`../Diffusion Welding/`](../Diffusion%20Welding/) — UCDW field-repair-tier joining process
- [`../Drugs/`](../Drugs/) — pharmacology research (Combat Drug and Injectable Food cross-reference)
- [`../GM Enhancements/`](../GM%20Enhancements/) — HSA enhancement protocol (Super Soldier programme adjacency)
- [`../Diamond Batterys/`](../Diamond%20Batterys/) — sovereign energy that field-deployable systems would draw on
- [`../UCN Political System/`](../UCN%20Political%20System/) — UCN doctrine and `≤ 10`-warhead defence posture
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — ARIA-INTEL battlefield intelligence
- [`../Filtering/`](../Filtering/) — GH-SR-IMM platform-state estimation

---

[← Back to main README](../README.md)
