# UCDR Common Architecture & Components
## TRP-2026-022 — UNCLASSIFIED / FOR OFFICIAL USE ONLY

> **A cross-platform component-commonality matrix for the Weapons-Defence portfolio. Every weapon in the small-arms family, the heavy-weapon family, and the body-armour / undersuit family is designed so that as many parts as possible are shared across platforms — to drop the spares burden, simplify training, and let one armourer's bench restore any weapon in the system.** This document defines the common architecture explicitly so that future spec sheets and research papers can reference component lists by name rather than re-specifying them. All ballistic / performance numbers in this folder trace back to [`weapons_sim_results.md`](weapons_sim_results.md) and the simulator in [`weapons_simulation.py`](weapons_simulation.py).

> **Genre note.** UNCLASSIFIED / FOUO-style register; this is in-universe defence-engineering documentation, not real materiel.

---

## 1. Why component commonality matters

A defence-engineering R&D division that designs eight weapons in eight different feed systems with eight different bolt faces and eight different recoil-spring assemblies has built **eight logistic chains**, not one weapons family. The Soviet 7.62 × 39 / AKM ecosystem worked because every variant — rifle, light machine gun, designated marksman, paratroop — shared the same bolt, gas piston, magazine well, and spring rates. NATO's M4 / M249 / M27 family followed the same principle a generation later. This portfolio enforces commonality across **three families** — small-arms, heavy weapons, and personal protective equipment — using a single shared parts catalogue.

---

## 2. Small-arms family — common architecture

### 2.1 Shared cartridge platforms

Two cartridges cover everything from sidearm to designated marksman; a third covers the anti-materiel sniper:

| Cartridge | Bore | Bullet | Muzzle vel. | Muzzle energy | P_max | Weapons that use it |
|---|---|---|---|---|---|---|
| **4.6 × 30 mm Enhanced** | 4.65 mm | 2.6 g WC-Co cored | 501 m/s (pistol) | 326 J | 180 MPa | MP-4.6M Pistol, MP-4.6M Defender PDW |
| **6.8 × 51 mm Common Cartridge** | 6.85 mm | 8.7 g WC-cored | 731 m/s (rifle) | 2 324 J | 307 MPa | MP-6.8 Mark II Rifle (future MP-6.8 LMG) |
| **15.2 × 115 mm APYT** | 15.20 mm | 64 g saboted sub-cal | 781 m/s | 19 505 J | 258 MPa | MAS-15.2E Mark III Sniper |
| **4.6 × 22 mm DPAP** *(LE-only)* | 4.60 mm | 3.3 g WC + Cu jacket | 396 m/s | 259 J | 246 MPa | MP-4.6P Guardian LE Police Pistol (`../Weapons-Police/`) |

The 4.6 × 30 mm is intentionally case-head-compatible with the existing HK-developed 4.6 × 30 mm PDW round so commercial primers and brass-forming dies are available off-the-shelf. The 6.8 × 51 mm Common Cartridge shares case geometry with the SIG-XM7 / XM250 family so the magazine geometry inherits from NATO's adopted Next Generation Squad Weapon ecosystem. The 15.2 × 115 mm APYT is bespoke; its rim and base diameters are sized so the existing 14.5 × 114 mm tooling can be repurposed with one belt-and-pull-stop change. The 4.6 × 22 mm DPAP (police-only) is the LE-variant case — same bore diameter and same projectile family as the 4.6 × 30 mm Enhanced, on a 22 mm shortened case to reduce muzzle velocity to the overpenetration-controlled regime (396 m/s rather than 542 m/s) appropriate for urban LE engagement; common projectile-tooling, primer chemistry, and brass-forming dies are reused between the two cases.

### 2.2 Shared action components — 4.6 mm family (MP-4.6M Pistol & PDW)

The pistol and the PDW share the same cartridge and a deliberate **= 75 % parts commonality** in the action group. Both use a rotating-bolt short-recoil action sized to the 4.6 × 30 mm Enhanced cartridge. The pistol is fixed-barrel, single-action, semi-only; the PDW adds a buffered bolt-carrier for select-fire (semi / 3-round burst / 850 rpm full-auto).

| Component | Material | Pistol | PDW | Notes |
|---|---|---|---|---|
| Bolt face | Carburised low-alloy steel (common-spec target AISI 8620, 60 HRC working face) | shared | shared | Same lug geometry, same firing-pin bore. The AISI 8620 designation is the common-spec target driven from this document; individual spec sheets reference the bolt face as a shared part rather than name the alloy explicitly. |
| Firing pin | Titanium with S7 tool-steel tip, 58–60 HRC | shared | shared | Lightweight to drop lock-time |
| Extractor | S7 tool steel, 56 HRC | shared | shared | Same hook geometry |
| Dual ejectors | Spring-loaded, MP35N alloy | shared | shared | Same spring rate |
| Recoil spring | Chrome-silicon flat-wire | similar | longer free-length on PDW | Same wire diameter, different free length |
| Buffer | Tungsten-filled polymer | absent | present | PDW only |
| Trigger group | S7 sear, hardened 4340 hammer | shared | shared | PDW adds 3-round-burst sear |
| Magazine well geometry | Stamped 4140 | shared (20-rnd) | longer well (40-rnd) | Same lip width, same follower stops |
| Magazine body | 17-7 PH stainless (pistol, 20-rnd) / 7075-T6 anodised aluminium (PDW, 40-rnd) | different — see note | different — see note | The two magazines are intentionally not cross-compatible: the pistol prioritises rigidity in a short deep-draw envelope (stainless); the PDW prioritises mass in a long magazine (aluminium). Both share the same Elgiloy / chrome-silicon spring family and PTFE-lined polymer anti-tilt follower. |
| Sights | Tritium 3-dot, dovetail | shared | shared | RMR cut on optional flat-top variant |

The integrated suppressor on the pistol (80 cm³, 6 baffles, 40 dB attenuation cap) and the side-mounted suppressor on the PDW (180 cm³, 8 baffles, 40 dB cap) share the same Inconel 718 K-baffle stock, the same tool-less end-cap, and the same heat-treatment recipe. The PDW suppressor is one extra baffle pair longer and uses the same Inconel coupon stock.

### 2.3 Shared action components — 6.8 mm family (MP-6.8 Rifle)

The MP-6.8 Mark II uses a short-stroke gas-piston rotating-bolt action sized to the 6.8 × 51 mm Common Cartridge. It is mechanically separate from the 4.6 mm family — the bore is too large to share bolt heads — but it shares the **trigger architecture, optic-rail geometry, and stock-furniture mounting interface** with the PDW. An armourer trained on the PDW lower receiver can transition to the rifle lower receiver inside the same shift.

| Component | Material | Shared with PDW? | Notes |
|---|---|---|---|
| Trigger group | S7 sear, 4340 hammer | yes | Same trigger pack drops into rifle lower |
| Pistol grip | Glass-filled polymer | yes | Same A2-pattern grip |
| Optic rail | Picatinny MIL-STD-1913 on flat-top | yes | Same height, same screw spacing |
| Sling attachment | QD swivel cup | yes | Same socket geometry |
| Magazine release | Ambidextrous polymer paddle | similar | Same paddle, scaled lever ratio |
| Bolt carrier | Hard-chromed 4340 | no — bigger | 6.8 mm bolt won't fit 4.6 mm carrier |
| Gas piston | Inconel 718 short stroke | no — unique | 6.8 mm specific |
| Barrel | Cold-hammer-forged 4140 mod, Stellite-21 throat insert + hard-chrome bore | shared throat-insert + bore-lining recipe | Bore diameter unique |

The barrel uses a **composite lining**, not two competing treatments. The chamber and throat (~ first 40 mm of the bore) carry a Stellite-21 cobalt-base superalloy insert applied by vacuum plasma spray and HIP densified; this is where the worst combined thermal + erosive loading lives. The remainder of the bore is conventionally hard-chromed (~ 20 µm electrolytic Cr). The Stellite-21 throat-insert recipe (1.0 mm wall on small arms, 1.5 mm on the MAS-15.2E, full-length 3 mm on the 57 mm autocannon barrel) is identical across all calibres: cobalt-base superalloy, vacuum plasma-spray applied, post-spray HIP densified, target porosity < 0.5 %. The same barrel-shop fixture runs every calibre. The 57 mm and 140 mm heavy-weapon barrels use full-length Stellite-21 liners (no chrome) because the higher chamber pressures and longer dwell times exceed the duty cycle of electrolytic chrome.

### 2.4 Shared sniper components — MAS-15.2E

The anti-materiel rifle uses a bolt-action with a three-lug rotating bolt face. Its trigger group is mechanically larger than the MP-6.8's but uses the **same S7 / 4340 hardening recipe** and the same set-screw geometry for sear engagement. The forend rail is Picatinny MIL-STD-1913 — same screw spacing as the rifle and PDW. Optics common to every member of the small-arms family include the suite's standard 1–8 × LPVO mount and the 6–24 × precision-optic spec.

---

## 3. Heavy-weapons family — common architecture

Four 57 mm × 347 mm / 57 mm low-velocity / 57 mm dual-purpose / 140 mm KEW-AP weapons sit in this family. Three of the four use the same 57 mm bore — which means **one barrel-blank stock, one shared full-length Stellite-21 lining process, one rifling tool set**. The fourth is the 140 mm tank round, which uses the same Stellite-21 process at greater wall thickness. Unlike the small-arms barrels (Stellite throat + chrome bore composite), all heavy-weapon barrels use full-length Stellite — chamber pressures and dwell times exceed the duty cycle of electrolytic chrome.

### 3.1 Shared 57 mm bore — three weapons, one barrel-shop process

| Weapon | Cartridge | Bore length | Projectile | MV | ME |
|---|---|---|---|---|---|
| 57 mm Autocannon | 57 × 347 mm SR | 4 560 mm / L/80 | 2.40 kg APFSDS-T sub-cal | 948 m/s | 1.08 MJ |
| 57 mm Underbarrel GL | 57 mm LV grenade | 305 mm | 350 g HE-FRAG | 149 m/s | 3 872 J |
| 57 mm Mortar / RPG | 57 mm dual-purpose | 900 mm | 1.40 kg combined-warhead | 187 m/s | 24 427 J |

The **bore diameter is identical** across all three to the 0.05 mm — meaning bore-gauges, cleaning-rod brushes, sabot-fit gauges, and chamber-erosion gauges are interchangeable. The three weapons use different chamber pressures (257 / 109 / 111 MPa peak respectively) so the breech and chamber lining are different on the autocannon vs the low-pressure two — but the bore is the same.

The 57 mm autocannon is the high-pressure / high-velocity APFSDS-launching system; the underbarrel grenade is a low-pressure HE-FRAG hand-held single-shot; the dual-purpose mortar/RPG is a tube-fired round-loaded system that operates in either mortar (low-angle, indirect, ~2 500 m at 45°) or RPG (direct-fire, ~1 500 m) mode by changing the propellant cup.

### 3.2 140 mm tank round — separate but related

The 140 × 920 mm KEW-AP saboted long-rod uses a vertical sliding-block breech with electrothermal-chemical ignition. Per the simulator at 1 698 m/s and 9.23 MJ muzzle energy, it generates 351 715 J of free-recoil energy that is absorbed by a **600 mm hydraulic recoil stroke** into a 3 400 kg turret-trunnion mass. (Note: an earlier draft of this document stated "1.2 m" — this was a documentation error. The 600 mm figure is from `weapons_sim_results.md` §11 and the 140 mm spec body §8.2 and is the authoritative value.) The penetrator is a 920 mm DU long-rod at 28 mm diameter (L/D 33) achieving **867 mm RHA at muzzle and 540 mm at 1 km** — calibrated against M829-class data.

### 3.3 Propellant family

All four heavy-weapon cartridges and all three small-arms cartridges use the same nitrocellulose-based double-base propellant grain (force constant F = 950 kJ/kg, covolume 1.0 cm³/g, ? = 1.27) at different web thicknesses and different surface area-to-volume ratios per cartridge. Single propellant chemistry across the whole portfolio means **one storage standard, one degradation curve, one shelf-life model** — propellant manufactured for the 4.6 mm cartridge is chemically identical to that loaded into the 140 mm tank gun, only the grain geometry is different.

---

## 4. Personal protective equipment family

Three platforms share the NACS CORE undersuit as a base layer: APES (military), APES-L Mark I Police (`Weapons-Police/`), and the hypothetical OBSIDIAN / OBSIDIAN-X academic-study systems. The NACS undersuit ([`NACS CBRN/NACS_Specification.md`](NACS%20CBRN/NACS_Specification.md)) provides:

| Layer | Function | Shared across |
|---|---|---|
| Merino-wool / silver-ion nylon inner | Moisture wicking + antimicrobial | All three platforms |
| GORE CHEMPAK selectively-permeable membrane | 72 h CBRN protection | APES, APES-L (CBRN bonus capability) |
| Sealed YKK waterproof + silicone seal-strip interfaces | Wrist / ankle / neck CBRN seal | APES, APES-L (police variant) |
| Phase-change material (28 °C, 200 kJ/kg) | Thermal buffering | APES military variant only — APES-L omits the NACS PCM because the APES-L 400 g PCM panel makes it redundant per Police Sim 19 |

The IL-STF carrier fluid (ionic-liquid EMIm-BF4, Arrhenius activation energy ≈ 10 kJ/mol vs ≈ 25 kJ/mol for PEG-200) is shared between APES-L Mark I Police and the planned APES Mark II military variant — same chemistry, same temperature window (-25 °C to +45 °C), same 60–65 % v/v SiO2 nanoparticle loading.

The single-use B4C tile geometry (75 mm × 75 mm × 1.9 mm ceramic over 2 mm Al 5052 backing) is shared between APES-L Police and the proposed APES Civilian-Threat configuration. Replacement protocol is identical across both: tool-less, < 30 s per tile, ~75 g per tile.

---

## 5. Common ammunition / accessory accessories

### 5.1 Magazine architecture

| Family | Common magazine geometry | Body material | Capacities offered |
|---|---|---|---|
| 4.6 × 30 mm — Pistol | Single-stack double-feed, deep-draw box | 17-7 PH stainless steel, hard anodised | 20 |
| 4.6 × 30 mm — PDW | Double-stack double-feed, long box | 7075-T6 aluminium, hard anodised | 30 / 40 |
| 4.6 × 22 mm — MP-4.6P Guardian LE (Police) | Double-stack double-feed, short box | 7075-T6 aluminium, hard anodised | 20 |
| 6.8 × 51 mm | Double-stack double-feed (NGSW-pattern) | 7075-T6 aluminium, hard anodised | 10 / 20 / 30 |
| 15.2 × 115 mm | Steel box-magazine, dual stack-single feed | 4140 steel, parkerised | 5 / 8 |
| 57 mm autocannon | Dual-feed externally-powered cassette | Welded 4340 steel | 60 / 120 (ready) |

The common parts across the magazine family are the **Elgiloy / chrome-silicon variable-pitch spring**, the **PTFE-lined polymer anti-tilt follower**, and the **440C stainless laser-formed feed lips** — not the magazine body itself. Body material is selected by capacity-vs-stiffness trade-off (stainless for short deep-draw, aluminium for long mass-critical, steel for heavy-cartridge box). The MP-4.6M Pistol and MP-4.6P Guardian LE are intentionally not magazine-cross-compatible (different cartridge — 4.6 × 30 vs 4.6 × 22 — and different magazine wells).

### 5.2 Suppressor family

All small-arms suppressors use the **Inconel 718 K-baffle** stock with chromium-plated bores, the same tool-less end-cap thread, and the same heat-treatment recipe (solution treat + age, 980 °C / 720 °C). Volumes differ; baffle counts differ; the rest is shared.

| Weapon | Volume | Baffles | Sound reduction (cap) |
|---|---|---|---|
| MP-4.6M Pistol (integral) | 80 cm³ | 6 | 40 dB |
| MP-4.6M Defender PDW | 180 cm³ | 8 | 40 dB |
| MP-6.8 Mark II Rifle | 410 cm³ | 7 | 40 dB |
| MAS-15.2E Sniper | 1 800 cm³ | 10 | 40 dB |

The 40 dB cap is a modelled bound from the adiabatic-expansion calculation in `weapons_simulation.py`. Real prototypes typically achieve 25–35 dB attenuation at the muzzle — the 40 dB number is an upper bound, not a measured value.

### 5.3 Optic mounting interface

Every small arm in the portfolio uses **Picatinny MIL-STD-1913** mounting on the top of the receiver, with identical screw spacing. This means the same red-dot, LPVO, night-vision clip-on, IR aiming laser, or thermal optic can be mounted on any weapon in the family — bench-tested zero on one weapon does not transfer, but the optic is mechanically identical.

### 5.4 Material commonality summary

| Material | Used in | Why |
|---|---|---|
| Stellite-21 | All barrel liners (4.6 / 6.8 / 15.2 / 57 / 140) | Cobalt-base superalloy resists bore erosion; single supply chain |
| S7 tool steel @ 56–60 HRC | All triggers, sears, extractors, firing pins | One heat-treat recipe, one supplier |
| MP35N alloy | All major springs | Non-magnetic, fatigue-tolerant, the same material used in the APES single-use-tile gaskets and the NACS sealed-interface micro-springs |
| Inconel 718 | Suppressor K-baffles, hot-gas paths in autocannon | Solution-treat-and-age recipe shared with the 140 mm tank-gun obturator ring |
| Hardened 4340 | All hammers, rotating-bolt carriers | Single heat-treat recipe (oil-quench, 50–54 HRC) |
| 7075-T6 aluminium | Pistol frame inserts, PDW / Police / 6.8 mm rifle magazine bodies, APES honeycomb backing | One forging alloy, three geometries — magazine bodies (hard-anodised, draw-formed), pistol-frame inserts (machined from billet), and APES honeycomb backing behind the B4C tile array |
| 17-7 PH stainless steel | MP-4.6M Pistol magazine body, all suppressor end caps | Stainless precipitation-hardened alloy for the high-stiffness short-deep-draw application that does not tolerate aluminium yielding |
| 4140 steel | Magazine well stampings, 15.2 mm magazine box, all hammers | Single hot-rolled stock, three machining routes |
| Glass-filled polymer (35 % GF) | Grips, magazine **followers**, magazine release paddles, sub-shell APES carrier | Single resin / glass spec across the portfolio. **Magazine bodies are not GFP** — bodies are 17-7 PH, 7075-T6, or 4140 per section 5.1. |
| Carburised low-alloy steel — common-spec target AISI 8620 (60 HRC working surface) | All bolt faces | Same case-hardening recipe. AISI 8620 is the common-spec target driven from this document. |
| Chrome-silicon flat-wire | All recoil springs | Same wire stock, different free length |

---

## 6. Common simulator — single source of truth

Every numerical claim in every spec sheet and every research paper in this folder is derived from the same Python simulator. The simulator now runs in two tiers covering the full set of physical claims made anywhere in the portfolio.

### 6.1 Tier-1 — core ballistics

- **`weapons_simulation.py`** — Le Duc / Powley closed-form internal ballistics (? = 0.72 small arms, ? = 0.65 autocannon, ? = 0.55 tank gun); G7 / G1 drag-table point-mass external integration over the ICAO standard atmosphere; De Marre RHA-penetration (K = 7.80 × 10?4, calibrated against M80 7.62 NATO @ ≈ 10 mm RHA, M2 .50 BMG AP @ ≈ 20 mm, 14.5 × 114 B-32 @ ≈ 30 mm at 100 m); Lanz–Odermatt-form long-rod model (K = 0.44, v0 = 1 500 m/s, calibrated to M829-class DU long-rod data at ≈ 700 mm RHA @ muzzle and ≈ 600 mm @ 2 km); adiabatic-expansion suppressor attenuation model (40 dB cap); free-recoil energy via momentum conservation.

### 6.2 Tier-2 — comprehensive coverage of every numerical claim

Added in v2 of the simulator to bring **every other numerical assertion** anywhere in this folder under simulator control:

| § | Model | Anchor / calibration |
|---|---|---|
| 6 | Muzzle SPL + layered hearing-protection stack | Westin (1975) SPL fit. Calibrated against 5.56 carbine ≈ 165 dB, 7.62 rifle ≈ 166, .50 BMG ≈ 178, 120 mm M256 ≈ 187. Foam plug -22, double plug+muff -28, double + TACS personal -53. |
| 7 | Zeroed bullet-drop tables from sight-line | Bisection-zeroed point-mass integrator at canonical zero range (100 m service, 500 m sniper). |
| 8 | Wind drift at 10 mph crosswind | Didion / Bagnold form: `drift = v_wind · (t_actual - x/v0)`. |
| 9 | Hatcher max effective range vs personnel | KE threshold = 80 J (FBI / Hatcher convention). |
| 10 | Barrel life + sustained-fire thermal bound | Calibrated against M4 (10 000 rd chrome 5.56), M14 (7 500 rd 7.62), M2HB (10 000 rd Stellite .50), GAU-8 (6 000 rd 30 mm), M256 (700–1 000 rd 120 mm). |
| 11 | Peak recoil force | Parabolic energy dissipation over the stock-travel stroke, with muzzle-brake impulse fraction redirected laterally. |
| 12 | RHA penetration at NATO 60° obliquity | Tate / Krupp `cos(?)^n` with n = 1.6 small arms, n = 0.7 long-rod APFSDS. |
| 13 | Body-armour V50 + back-face deformation | Lambert-Jonas / Recht-Ipson. Calibrated against IIIA + 9 mm ball (≈ 430 m/s), IV + .30-06 M2 AP (≈ 870 m/s). |
| 14 | Fragmentation — Gurney + Mott + Carlton lethal area | Carlton fit anchored at 81 mm M821A1 mortar (A_L ≈ 200 m²). |
| 15 | Shaped-charge (HEAT) RHA penetration | Birkhoff steady-state copper jet, 22° cone half-angle, jet length ≈ 0.7 × CD. Calibrated against RPG-7 PG-7VL, Hellfire, TOW-2A. |
| 16 | HPR-X rocket trajectory | Tsiolkovsky burnout + ICAO-drag point-mass integration with stage separation. |
| 17 | Kamlet–Jacobs detonation chemistry | P_CJ (GPa), VOD (km/s), brisance vs TNT for CL-20 / HMX / RDX / Comp B / TNT / PETN / ANFO. |
| 18 | TACS active acoustic cancellation depth | Nelson-Elliott (1992) multi-mic-array bound, 6 dB/octave high-frequency rolloff above 1 kHz. |
| 19 | Tank-track pad noise transmission | 1-DOF mass-spring-damper transmissibility (steel ?_n 80 Hz, ? 0.02; HNBR ?_n 25 Hz, ? 0.18) at 300 Hz drive frequency. |
| 20 | Combat-drug PK | One-compartment oral-absorption model for caffeine / modafinil / dextroamphetamine. |
| 21 | Injectable-nutrition osmolality | Solute-summed mOsm/kg + Plumb / Holliday-Segar safe-IV bounds (peripheral < 600, central < 1 800). |
| 22 | TACT-1 ration shelf life | Q10 = 2 Arrhenius lipid-oxidation, 36-month baseline @ 25 °C; carnauba coating softens at 82–86 °C. |

### 6.3 The single update path

- **`weapons_sim_results.md`** — the human-readable output across both tiers (22 sections, ~23 KB).
- **`weapons_sim_results.json`** — machine-readable output (~90 KB).

When a future change adjusts cartridge geometry, propellant load, barrel length, armour layup, warhead loadout, rocket stage, drug dose, or formulation, the simulator is re-run and **every spec sheet and paper that cites those numbers is updated against the new `weapons_sim_results.md`** in one pass — there is one source of truth and one update path.

---

## 7. Common training, common armourer, common spares chain

The corollary of component commonality is operational: **one armourer**, trained on the MP-4.6M pistol, can fully field-strip every weapon in the small-arms family within an 8-hour familiarisation block; the rotating-bolt action geometry, trigger-pack drop-in, MIL-STD-1913 rail, suppressor thread, and magazine-well geometry are shared. The same armourer's bench tooling — torque wrenches, headspace gauges, bore-erosion gauges, optic-zero collimator — also covers the MP-6.8 rifle and the MAS-15.2E sniper. The 57 mm bore-gauge set covers all three 57 mm weapons.

The spares chain is similarly compressed. A unit operating the four small arms + the four heavy weapons would, under conventional design practice, carry **eight different bolt heads, eight different spring kits, eight different optic mounts, four different magazine families, and three different suppressor-baffle stocks**. Under the commonality matrix in this document, it carries:

- **3 bolt-head SKUs** (4.6 / 6.8 / 15.2)
- **1 spring stock + 4 free-length cuts**
- **1 optic-rail standard** (MIL-STD-1913)
- **3 magazine families** (4.6 / 6.8 / 15.2)
- **1 suppressor-baffle stock + 4 length variants**
- **1 propellant chemistry + 7 grain geometries**

Net spares-SKU reduction across the portfolio: approximately **62 %** compared to a no-commonality baseline.

---

## 8. Honest caveats

- This commonality matrix is a **design intent**, not a fielded supply chain. No real spares contract exists.
- The 40 dB suppressor attenuation is a modelled adiabatic-expansion upper bound, not a measured value. Real prototypes typically achieve 25–35 dB.
- The 62 % spares-SKU reduction is computed against the design intent above; no procurement office has audited it.
- All ballistic numbers in this folder are simulator-derived. Physical-prototype validation against NATO / NIJ / STANAG test standards remains the definitive answer.
- "Component commonality" is a logistic / engineering virtue, not a guarantee of operational performance — a weapon with shared parts can still fail in the field; the matrix only constrains the spares burden, training overhead, and armourer workload.

---

## 9. Cross-references

- [`weapons_simulation.py`](weapons_simulation.py) — the source-of-truth simulator
- [`weapons_sim_results.md`](weapons_sim_results.md) — the simulator's tabulated output
- Small-arms specs: [`MP-4.6M Guardian Pistol/MP-4.6M_Guardian_Pistol_Specification.md`](MP-4.6M%20Guardian%20Pistol/MP-4.6M_Guardian_Pistol_Specification.md), [`MP-4.6M Defender PDW/MP-4.6M_Defender_PDW_Specification.md`](MP-4.6M%20Defender%20PDW/MP-4.6M_Defender_PDW_Specification.md), [`MP-6.8 Mark II Rifle/MP-6.8_Mark_II_Rifle_Specification.md`](MP-6.8%20Mark%20II%20Rifle/MP-6.8_Mark_II_Rifle_Specification.md), [`MAS-15.2E Anti-Materiel Sniper/MAS-15.2E_Specification.md`](MAS-15.2E%20Anti-Materiel%20Sniper/MAS-15.2E_Specification.md)
- Heavy weapons specs: [`57mm Autocannon/57mm_Autocannon_Specification.md`](57mm%20Autocannon/57mm_Autocannon_Specification.md), [`57mm Underbarrel Grenade/57mm_Underbarrel_Grenade_Specification.md`](57mm%20Underbarrel%20Grenade/57mm_Underbarrel_Grenade_Specification.md), [`57mm Mortar RPG/57mm_Mortar_RPG_Specification.md`](57mm%20Mortar%20RPG/57mm_Mortar_RPG_Specification.md), [`140mm Tank KE Round/140mm_Tank_KE_Specification.md`](140mm%20Tank%20KE%20Round/140mm_Tank_KE_Specification.md)
- Paired research papers in each platform subfolder (see [`README.md`](README.md) index)
- Body-armour cross-link: [`APES Body Armour/APES_Specification.md`](APES%20Body%20Armour/APES_Specification.md) and the police variant at [`../Weapons-Police/APES-L Mark I/APES-L_Specification.md`](../Weapons-Police/APES-L%20Mark%20I%20Police%20Body%20Armour.md)

[? Back to Weapons-Defence README](README.md)