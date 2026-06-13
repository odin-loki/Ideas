# MP-4.6P Guardian LE — police combat pistol

> **Simulation-validated 4.6 × 22 mm DPAP law-enforcement pistol:** **396 m/s** / **259 J** / **246 MPa**; defeats NIJ IIIA + NIJ III + four intermediate barriers; felt recoil **0.078 ft·lb**; MRBF **20 548 analytic / ~30 000 simulated** (Tier-2 surface engineering); FTF **1:80 000**. Seven-phase lifecycle sim (§23) matches the military MP-4.6M family toolchain.

---

## Reading order

1. **This README** — navigation and headline numbers.
2. [`MP-4.6P_Guardian_LE_Specification.md`](MP-4.6P_Guardian_LE_Specification.md) — full operator spec (TRP-2026-020).
3. [`MP-4.6P_Guardian_LE_Research_Paper.md`](MP-4.6P_Guardian_LE_Research_Paper.md) — academic paper.
4. [`SIM_README.md`](SIM_README.md) — simulator keys and §23 lifecycle map.
5. Run [`platform_simulation.py`](platform_simulation.py) — PASS/FAIL verification.

---

## Source documents

| Document | Role |
|---|---|
| [`MP-4.6P_Guardian_LE_Specification.md`](MP-4.6P_Guardian_LE_Specification.md) | Operator specification — seven simulation phases, Tier-2 surface engineering, compliance |
| [`MP-4.6P_Guardian_LE_Research_Paper.md`](MP-4.6P_Guardian_LE_Research_Paper.md) | Research paper |
| [`SIM_README.md`](SIM_README.md) | Simulation cross-reference |
| [`platform_simulation.py`](platform_simulation.py) | Local verification (`mp46p_guardian_le`) |
| [`../sim_common.py`](../sim_common.py) | Delegates to [`../../Weapons-Defence/sim_common.py`](../../Weapons-Defence/sim_common.py) |
| [`../../Weapons-Defence/weapons_simulation.py`](../../Weapons-Defence/weapons_simulation.py) | Portfolio + §23 lifecycle engine |
| [`../../Weapons-Defence/weapon_lifecycle.py`](../../Weapons-Defence/weapon_lifecycle.py) | §23 portfolio lifecycle — structural SF, parts-life, reliability MC |

---

## Headline numbers (simulation-validated)

| Metric | Value |
|---|---|
| Cartridge | **4.6 × 22 mm DPAP** (`4.6x22mm`) |
| Muzzle velocity | **396 m/s** |
| Muzzle energy | **259 J** |
| Peak chamber pressure | **246 MPa** |
| Per-unit cost (mature) | **A$164 – 180** |
| Bore life service (§23) | **24,000 rounds** |
| MRBF analytic (§23) | **~20,548 rounds** |
| MRBF simulated (§23) | **~30,000 rounds** |
| Felt recoil (§23) | **~0.078 ft·lb** |
| Spring fatigue SF (§23) | **5.8** |
| Barrel SF_yield (§23) | **2.42** |
| FTF rate (§23) | **1:80,000** |

Source: [`../../Weapons-Defence/weapons_sim_results.md`](../../Weapons-Defence/weapons_sim_results.md) §§1–2, **§23**.

---

## Simulation verification

Portfolio **§23** ([`../../Weapons-Defence/weapon_lifecycle.py`](../../Weapons-Defence/weapon_lifecycle.py)) adds structural integrity, component parts-life, and seven-mode reliability MC on top of Tier-1 ballistics for the 4.6 × 22 mm cartridge.

```bash
python platform_simulation.py
```

| Artifact | Role |
|---|---|
| [`platform_simulation.py`](platform_simulation.py) | Local PASS/FAIL slice |
| [`SIM_README.md`](SIM_README.md) | Table / key map |
| [`../../Weapons-Defence/weapons_sim_results.md`](../../Weapons-Defence/weapons_sim_results.md) | Authoritative output |

Regenerate full portfolio:

```bash
cd ../../Weapons-Defence
python weapons_simulation.py
```

---

## Quick start

```bash
python platform_simulation.py
```

---

## Related work

- [`../../Weapons-Defence/MP-4.6M Guardian Pistol/`](../../Weapons-Defence/MP-4.6M%20Guardian%20Pistol/) — 4.6 × 30 mm military parent (shared §23 lifecycle)
- [`../APES-L Mark I/`](../APES-L%20Mark%20I/) — sibling police body armour
- [`../README.md`](../README.md) — Weapons-Police index

---

[← Back to Weapons-Police README](../README.md)