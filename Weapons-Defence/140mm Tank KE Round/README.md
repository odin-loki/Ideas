# 140 mm KEW-AP Multi-Effect Tank Round

> **A simulation-validated saboted DU long-rod (28 mm × 920 mm) launched at 1 698 m/s for 9.23 MJ muzzle energy, 867 mm RHA at the muzzle, and 198 MPa peak chamber pressure from a 7 350 mm L/52 ETC smoothbore.** Headline gun: 3 400 kg trunnion mass, 351.7 kJ free recoil through 600 mm hydraulic stroke (178 056 N peak force), 618-round barrel life.

> **Genre note.** Commercial Sensitive / defence-technology register for tonal coherence. No real procurement or live-armour test data implied. **Numbers trace to [`../weapons_simulation.py`](../weapons_simulation.py) — cartridge key `140mm_KE`, weapon key `140 mm Tank Gun`.**

---

## What this folder is

The 140 mm KEW-AP round is a **complete platform subfolder**: operator specification, academic research paper, and **Tier-C portfolio simulation**. The round is the portfolio's main-armament KE solution for a next-generation MBT, with a paired HE-FRAG nature sharing the case.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`140mm_Tank_KE_Specification.md`](140mm_Tank_KE_Specification.md) — product and engineering spec (TRP-2026-101).
3. [`140mm_Tank_KE_Research_Paper.md`](140mm_Tank_KE_Research_Paper.md) — formal design-and-validation narrative (includes 1.0 penetration correction).
4. [`SIM_README.md`](SIM_README.md) — portfolio sim guide.
5. Run [`platform_simulation.py`](platform_simulation.py) — PASS/FAIL claim verification against the portfolio sim.

---

## 📑 Source documents

| Document | Format | Role |
|---|---|---|
| [`140mm_Tank_KE_Specification.md`](140mm_Tank_KE_Specification.md) | Operator / product specification | Cartridge, sabot, ETC breech, recoil, multi-effect warheads, Tier-2 imports. |
| [`140mm_Tank_KE_Research_Paper.md`](140mm_Tank_KE_Research_Paper.md) | Academic research paper | Lanz–Odermatt calibration vs M829, obliquity, limitations. |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Keys, CLI, result sections. |
| [`platform_simulation.py`](platform_simulation.py) | Local verification script | Runs portfolio engine; prints PASS/FAIL checks for this platform's spec claims. |
| [`../sim_common.py`](../sim_common.py) | Shared sim runner | Loads `weapons_simulation.py` and formats per-platform verification output. |
| [`../weapons_simulation.py`](../weapons_simulation.py) | Simulator source | Cartridge `140mm_KE`, weapon `140 mm Tank Gun`. |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative output | Cite for every ballistic claim. |

---

## 🎯 Headline numbers (simulation-validated)

All values below come from [`../weapons_sim_results.md`](../weapons_sim_results.md) §§1–3, 11–12, 14–15, 17, **§23**.

| Metric | Value |
|---|---|
| Cartridge | **140 mm KE** (`140mm_KE`) |
| Muzzle velocity | **1 698 m/s** (5 571 fps) |
| Muzzle energy | **9.23 MJ** (9 227 097 J) |
| Peak chamber pressure | **198–199 MPa** (~28 794 psi) |
| RHA @ 0° (0 / 500 / 1 000 / 2 000 m) | **867 / 698 / 541 / 327 mm** |
| RHA @ NATO 60° (0 / 500 / 1 000 m) | **534 / 430 / 333 mm** |
| Trunnion mass | **3 400 kg** |
| Free recoil | **351 715 J** (259 412 ft·lb) |
| Peak mount force | **178 056 N** (40 031 lbf) |
| Barrel life | **618 rounds** |
| HE-Frag lethal area (CL-20) | **1 173 m²** (r_eff 19.3 m) |
| HEAT penetration | **103 mm RHA** |
| Bore life service (§23) | **700 rounds** |
| MRBF analytic (§23) | **~3,502 rounds** |
| MRBF simulated (§23) | **~3,750 rounds** |
| Felt recoil (§23) | **~22914.359 ft·lb** |
| Spring fatigue SF (§23) | **2.6** |
| Barrel SF_yield (§23) | **2.23** |
| FTF rate (§23) | **1:8,000** |

---

## 🔬 Simulation verification

All headline numbers in this README trace to [`../weapons_sim_results.md`](../weapons_sim_results.md), produced by [`../weapons_simulation.py`](../weapons_simulation.py) and [`../weapon_lifecycle.py`](../weapon_lifecycle.py) (§23). Use the local verification script to confirm spec claims without regenerating the full portfolio:

```bash
python platform_simulation.py
```

The script prints **PASS/FAIL** checks for each claim in the specification and research paper.

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Local PASS/FAIL verification slice for this platform |
| [`SIM_README.md`](SIM_README.md) | Cartridge/weapon keys, table cross-references, methodology |
| [`../weapons_sim_results.md`](../weapons_sim_results.md) | Authoritative tabulated output — cite in every spec edit |
| [`../sim_common.py`](../sim_common.py) | Shared runner invoked by `platform_simulation.py` |
| [`../weapon_lifecycle.py`](../weapon_lifecycle.py) | §23 lifecycle — structural SF, parts-life, reliability MC |

To regenerate the **full portfolio** after editing shared parameters:

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

**From this folder** — verify platform claims:

```bash
python platform_simulation.py
```

**Regenerate full portfolio** (after shared parameter edits):

```bash
cd ..
python weapons_simulation.py
```

See [`SIM_README.md`](SIM_README.md) for cartridge key `140mm_KE`, weapon key `140 mm Tank Gun`, and result-table map.

---

## 🚧 Honest framing

- **Not a fielded round.** Simulation calibrated to M829-class open-source anchors — not instrumented live fire.
- **1.0 draft withdrawn.** Earlier ~1 450 mm muzzle RHA claim is explicitly retracted; simulator gives **867 mm**.
- **ETC + SCDB dependency.** The 198 MPa / 1 698 m/s envelope requires electrothermal-chemical breech and sovereign propellant chemistry not modelled as a fielded supply chain.

---

## 🔗 Related work in this repo

- [`../57mm Autocannon/`](../57mm%20Autocannon/) — medium-calibre 57 mm family (shared Stellite liner recipe)
- [`../CL-20 High Explosive/`](../CL-20%20High%20Explosive/) — HE-FRAG fill chemistry (§17 Kamlet–Jacobs)
- [`../Rubber Tank Tracks/`](../Rubber%20Tank%20Tracks/) — mobility subsystem context
- [`../Common Architecture and Components.md`](../Common%20Architecture%20and%20Components.md) — heavy-weapon barrel §3

---

[← Back to Weapons-Defence README](../README.md)