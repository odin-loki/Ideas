# Rockwell 50 to 70 Carbide — HX-70 GradePlex™ + TriboshieldPlus™ + Forge-to-Machine

> **A complete carbide-tooling platform for hard-machining steels from `HRC 40` to `HRC 70` — a regime where conventional WC-Co inserts give up around `HRC 55` and CBN takes over but only on insert geometries CBN can be made into. The platform combines: (1) **HX-70 GradePlex™**, a functionally-graded WC-Co substrate with three radial zones (Zone A `0 – 30 µm` is `92.5 %` WC, `5.5 %` Co, `2.0 %` TaC/NbC at `2050 – 2100 HV30` for the working surface; Zone C is the tougher `13 %` Co core); (2) **TriboshieldPlus™**, a five-layer coating stack (CrN bond, AlCrN thermal barrier, nc-AlTiSiN/a-Si₃N₄ hardness core at `42 – 46 GPa`, 40-bilayer AlCrN/AlTiSiN superlattice at `37.5 nm` per layer, DLC-Si friction layer at `µ < 0.15`); (3) **forge-to-machine**, a near-net-shape forging supply chain that on the H13-breech exemplar drops cost from `AUD $340 – 420` to `AUD $190 – 240` and lead time from `18 – 26` working days to `6 – 9` — a `~40 – 45 %` cost / `~65 – 70 %` lead-time reduction.** End-mill geometries CBN cannot reach become accessible at `HRC 65 – 70` for the first time.

---

## What this folder is

Hard machining — cutting steels at `HRC 50+` — has historically been a forced choice between two bad options: cubic-boron-nitride (CBN) inserts that perform but cost `$$$/insert` and only come in indexable insert geometries that limit the features you can cut, or premium AlTiN-coated WC-Co carbide that wears out fast above `HRC 55`. This folder argues for a third option: a *functionally-graded* WC-Co substrate (HX-70 GradePlex™) that places the hard, fine-grained, low-cobalt material at the cutting edge and the tough, coarser, higher-cobalt material at the core, plus a bespoke five-layer coating (TriboshieldPlus™) engineered to the specific failure modes of hard machining (binder softening at `~700 °C`, WC oxidation to WO₃, diffusive wear into the steel chip), plus a near-net-shape forging supply chain (forge-to-machine) that cuts material removal so machining itself becomes faster and cheaper. The combined platform targets a regime — `HRC 65 – 70` end-mills accessing small features — that simply does not exist in the open commercial market.

The folder is documentation-grade: peer-reviewed citations are heavy (Das, Mahapatra, Xiao, Kim, etc.), the metallurgy is laid out in detail, the manufacturing routing is specified, but author-run machining benchmark appendices are not confirmed in the portions reviewed. Read the gain numbers as **paper-stated projections** unless you locate embedded lab tables.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`HX70_Research_Paper.md`](HX70_Research_Paper.md) | Full research paper. Material physics, three-zone GradePlex composition, sintering protocol, TriboshieldPlus layers, projected machining gains. |
| [`HX70_Sintered_Carbide_Design_Spec.md`](HX70_Sintered_Carbide_Design_Spec.md) | Design specification. |
| [`ForgeMachine_Research_Paper.md`](ForgeMachine_Research_Paper.md) | Forge-to-machine supply-chain analysis. H13-breech exemplar. Cost and lead-time models. |
| [`Forge_to_Machine_Defence_Analysis.md`](Forge_to_Machine_Defence_Analysis.md) | Defence-context analysis. |

---

## 🧠 HX-70 GradePlex™ functionally-graded substrate

Three radial zones, same sintered billet, gradient achieved through controlled in-situ powder layering and HIP densification:

| Zone | Depth | WC | Co | Inhibitors | Hardness | Grain `D₅₀` |
|---|---|---|---|---|---|---|
| **A — Working surface** | `0 – 30 µm` | `92.5 %` | `5.5 %` | `2.0 %` TaC / NbC | **`2050 – 2100 HV30`** | `0.25 – 0.35 µm` |
| **B — Transition** | `30 – 300 µm` | (graded) | (graded ↑) | (graded ↑) | (graded) | (graded) |
| **C — Tough core** | core | balance | **`13 %`** | balance | `~1500 – 1600 HV30` | larger |

### Sintering route

- Vacuum sinter + in-situ HIP
- `100 bar` Ar
- Peak liquid-phase sinter at `1380 °C`
- Carbon control `±0.02 wt %`
- Dew point `≤ −60 °C`

---

## 🛡 TriboshieldPlus™ five-layer coating

| Layer | Material | Thickness | Role |
|---|---|---|---|
| **1 — Bond** | CrN | `0.1 µm` | Adhesion to substrate |
| **2 — Thermal barrier** | AlCrN (70:30 Al:Cr) | `~1.0 µm` | Heat shield |
| **3 — Hardness core** | nc-AlTiSiN / a-Si₃N₄ nanocomposite | `~2.0 µm` | **`42 – 46 GPa` hardness** |
| **4 — Superlattice** | 40 bilayers AlCrN / AlTiSiN | `37.5 nm` per layer | Crack arrest |
| **5 — Friction layer** | DLC-Si | `~0.4 µm` | **`µ < 0.15`** chip-flow surface |

---

## 📊 Projected machining performance (research paper)

| Workpiece hardness | Tool-life gain vs premium AlTiN | Cost vs CBN |
|---|---|---|
| `HRC 55` | **`40 – 55 %` gain** | n/a |
| `HRC 60` | **`85 – 100 %` gain** | n/a |
| **`HRC 65 – 70`** | **First-in-class carbide regime** | **`60 – 70 %` cost reduction** vs CBN |

**Projections**, not in-repo measured wear-test tables.

---

## 🔧 Forge-to-machine supply chain (H13-breech exemplar)

Near-net-shape forging followed by trochoidal hard-milling reduces the volume of metal that has to be removed from the rough billet. On the worked H13-breech (`~3.5 kg` rough → `~1.8 kg` finished):

| Process | Cost (AUD) | Lead time |
|---|---|---|
| Traditional billet machining | `$340 – $420` | `18 – 26` working days |
| **Forge-to-machine** | **`$190 – $240`** | **`6 – 9` working days** |
| **Reduction** | **`~40 – 45 %`** | **`~65 – 70 %`** |

---

## 🚧 Honest caveats

- **HX-70 narrative blends peer-reviewed citations with product-tier architecture** that reads as design-intent.
- **CBN insert geometry limitation arguments are industry-standard**, but **HX-70 as a realised SKU is documentation-only** in this folder.
- **Author-run machining benchmark appendix not confirmed** in the portions reviewed — treat numerical gains as paper-stated projections unless you find embedded lab tables.
- **Sintering tolerances** (carbon `±0.02 wt %`, dew point `≤ −60 °C`) are tight and require very specific furnace control that not every WC-Co operation has.

---

## 🎯 What this displaces

| Standard | Pain point | What this platform offers |
|---|---|---|
| Premium AlTiN-coated carbide | Wears out fast above `HRC 55` | Functionally-graded substrate + 5-layer coating to `HRC 70` |
| CBN inserts | `$$$/insert`, geometry-limited | End-mill geometries accessible at `HRC 65 – 70` |
| Generic WC-Co | One hardness everywhere | Three zones, hard surface + tough core |
| Bar-stock machining | Heavy material removal | Forge-to-machine, `~40 – 45 %` cost cut |

---

## 🔗 Related work in this repo

- [`../Diffusion Welding/`](../Diffusion%20Welding/) — sister manufacturing-process platform (UCDW)
- [`../New Classes of Electrical Components/`](../New%20Classes%20of%20Electrical%20Components/) — adjacent fabrication-science thinking
- [`../Weapons/`](../Weapons/) — defence-tech R&D portfolio (the H13-breech exemplar comes from there)
- [`../UCN Political System/`](../UCN%20Political%20System/) — sovereign-manufacturing doctrine
- [`../Quantum Diamond Wafer/`](../Quantum%20Diamond%20Wafer/) — sister hard-materials work

---

[← Back to main README](../README.md)
