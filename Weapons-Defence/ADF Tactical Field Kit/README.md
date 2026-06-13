# ADF Tactical Field Kit

> **A next-generation individual field kit for ADF dismounted operators: titanium-alloy tool suite, 32 L MOLLE load-carriage system, inline water filtration, IFAK, navigation/signalling, and integrated nutrition via TACT-1 Mark II + ASNP. Targets < 7 kg kit weight excluding food and water, with TACT-1 delivering 5–14 kg savings over standard IRP for a 72-hour operation.**

> **Genre note.** TRP designator, FOUO banner, and "Advanced Defence Systems Research Division" framing are adopted for tonal coherence with the rest of `Weapons-Defence/`. No real ADF procurement programme or issued equipment is implied.

---

## What this folder is

The **ADF Tactical Field Kit** is an aggregate sustainment-platform specification covering load carriage, water, tools, medical, navigation, hygiene, lighting, and nutrition integration. This folder contains the operator specification only — **no paired research paper exists**. [`platform_simulation.py`](platform_simulation.py) validates integrated nutrition claims via portfolio **§22** (TACT-1 shelf life) and delegates to **`pods_simulation.py --module verify`**.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`ADF_Tactical_Field_Kit_Specification.md`](ADF_Tactical_Field_Kit_Specification.md) — full procurement spec (18 sections).
3. [`SIM_README.md`](SIM_README.md) — aggregate spec scope; §22 + PODS sub-sim links.
4. Run [`platform_simulation.py`](platform_simulation.py) — §22 ration shelf life + PODS verify module.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`ADF_Tactical_Field_Kit_Specification.md`](ADF_Tactical_Field_Kit_Specification.md) | Operator / procurement specification | Complete design, materials, manufacture, weight budget, cost analysis. **Start here.** |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Aggregate scope; §22 ration shelf life + PODS sub-sim links. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | §22 TACT-1 shelf life; invokes `pods_simulation.py --module verify`. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | Lifecycle simulator | §23 service-life and storage intervals. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Portfolio simulator | §22 Arrhenius Q10 ration shelf-life model. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Simulator output | Authoritative §22 shelf-life table. |

**No research paper.** Unlike other platform folders in this reorganisation, ADF Tactical Field Kit has no paired academic paper. All technical content is in the specification above.

---

## 🎯 Headline numbers (specification prose)

| Metric | Value |
|---|---|
| Target field kit weight | **< 7 kg** (excluding food and water) |
| TACT-1 weight saving (72 hr) | **5–14 kg** vs standard IRP |
| Water carry requirement | **≤ 1.5 L** treated (inline filtration) |
| Main pack capacity | **32 L** MOLLE-compatible |
| Empty pack weight | **~2,155 g** |
| Operating temperature | **−20 °C to +65 °C** |
| Load carriage fabric (§23) | **8 yr** |

### Integrated nutrition — simulator §22 (TACT-1 ration shelf life)

Shelf life propagated from the 36-month-at-25 °C baseline using `Q10 = 2` Arrhenius lipid-oxidation model in the portfolio simulator:

| Storage temperature | Use case | Shelf life |
|---|---|---|
| **4 °C** | Cold-chain depot storage | **154.3 months (~ 13 years)** |
| **25 °C** | Lab / climate-controlled magazine (baseline) | **36.0 months (3 years)** |
| **35 °C** | Australian summer ambient / unconditioned warehouse | **18.0 months** |
| **49 °C** | Desert vehicle cabin (sustained + solar gain) | **6.8 months** |
| **60 °C** | Extreme hot-cabin / closed compartment | **3.2 months** |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §22. PODS energy density: [`../TACT-1 Tactical Ration/PODS- Edible High Energy Protein/pods_simulation.py`](../TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/pods_simulation.py) (invoked by `platform_simulation.py`).

---

## 🧩 Nutrition subfolders (integrated components)

| Subfolder | Role |
|---|---|
| [`../TACT-1 Tactical Ration/`](../TACT-1%20Tactical%20Ration/) | TACT-1 Mark II full-day compact ration — 700 g/day, 4,210 kcal |
| [`../TACT-1 Tactical Ration/ASNP Sports Nutrition/ASNP_Specification.md`](../TACT-1%20Tactical%20Ration/ASNP%20Sports%20Nutrition/ASNP_Specification.md) | ASNP combat-sports energy drink powder |
| [`../TACT-1 Tactical Ration/PODS- Edible High Energy Protein/`](../TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/) | PODS high-density lipid nanoparticle (optional energy supplement) |

---

## 🔬 Simulation verification

**Load-carriage mass budget, ergonomics, and component costs are prose targets** in the specification — not portfolio-simulator outputs. The local script validates **integrated nutrition** claims:

- Portfolio **§22** — TACT-1 Mark II ration shelf life vs storage temperature
- **`pods_simulation.py --module verify`** — PODS energy-density chemistry (delegated subprocess)

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | §22 shelf life + PODS verify module |
| [`SIM_README.md`](SIM_README.md) | Aggregate scope; linked subfolder simulations |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | §22 authoritative shelf-life table |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |

To regenerate the **full portfolio** (updates §22):

```bash
cd ..
python weapons_simulation.py
```

Optional JSON summary:

```bash
python platform_simulation.py --json
```

---

## 🚀 Quick start (simulator)

**From this folder** — verify §22 ration shelf life and PODS module:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for nutrition subfolder cross-references.

---

## 🚧 Honest framing

- **Aggregate specification only.** No standalone field-kit simulator; weight and cost numbers are prose engineering targets in the spec.
- **No research paper.** Portfolio reorganisation note: Paper numbering skips a dedicated ADF field-kit paper.
- **Partial nutrition verification.** TACT-1 shelf life uses portfolio §22; PODS uses `pods_simulation.py --module verify`; the field-kit load budget itself is not simulated.

---

## 🔗 Related work in this repo

- [`../TACT-1 Tactical Ration/README.md`](../TACT-1%20Tactical%20Ration/README.md) — oral nutrition pillar
- [`../APES Body Armour/`](../APES%20Body%20Armour/) — ballistic protection (separate load)
- [`../README.md`](../README.md) — Weapons-Defence portfolio index

---

[← Back to Weapons-Defence README](../README.md)