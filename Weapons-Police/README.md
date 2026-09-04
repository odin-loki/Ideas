# Weapons-Police — law-enforcement equipment R&D

> **Two Australian law-enforcement equipment prospectuses, each in a dedicated platform subfolder** with hub `README.md`, operator specification, research paper, `SIM_README.md`, and `platform_simulation.py` calling the shared [`../Weapons-Defence/sim_common.py`](../Weapons-Defence/sim_common.py) runner (portfolio physics + **§23 lifecycle**). **APES-L Mark I** — 6.5 kg full-body armour, 23 spec simulations, §13 V50 cross-check, **§23 panel service 10 yr**. **MP-4.6P Guardian LE** — 4.6 × 22 mm DPAP @ 396 m/s / 259 J, seven-phase lifecycle sim with parts-life and MRBF MC.

> **Genre note.** Defence-research register (TRP designators, FOUO banners). No real procurement office or fielded materiel implied.

---

## Folder convention

Each platform lives in its own subfolder:

| Platform | Folder | `platform_simulation.py` ID |
|---|---|---|
| **MP-4.6P Guardian LE** | [`MP-4.6P Guardian LE/`](MP-4.6P%20Guardian%20LE/) | `mp46p_guardian_le` |
| **APES-L Mark I** | [`APES-L Mark I/`](APES-L%20Mark%20I/) | `apes_l_body_armour` |

Root retains [`sim_common.py`](sim_common.py) (thin delegate to Weapons-Defence) and this index.

---

## Single source of truth

| File | Role |
|---|---|
| [`../Weapons-Defence/weapons_simulation.py`](../Weapons-Defence/weapons_simulation.py) | Portfolio Tier-1/Tier-2 physics |
| [`../Weapons-Defence/weapon_lifecycle.py`](../Weapons-Defence/weapon_lifecycle.py) | **§23** portfolio lifecycle — unique config per platform |
| [`../Weapons-Defence/weapons_sim_results.md`](../Weapons-Defence/weapons_sim_results.md) | Authoritative tabulated output (§§1–23) |
| [`../Weapons-Defence/Common Architecture and Components.md`](../Weapons-Defence/Common%20Architecture%20and%20Components.md) | Cartridge table includes **4.6 × 22 mm DPAP** |

---

## Headline numbers

### MP-4.6P Guardian LE (§23 lifecycle)

| Metric | Value |
|---|---|
| MV / ME / P_max | **396 m/s** / **259 J** / **246 MPa** |
| Bore life service (§23) | **24,000 rounds** |
| Felt recoil (§23) | **0.078 ft·lb** |
| MRBF analytic (§23) | **~20,548 rounds** |
| MRBF simulated (§23) | **~30,000 rounds** |
| FTF rate (§23) | **1:80,000** |
| Barrel SF_yield (§23) | **2.42** |

### APES-L Mark I (§23 lifecycle)

| Metric | Value |
|---|---|
| Mass | **6.5 kg** vs 20.25 kg incumbent |
| Panel service life (§23) | **10 yr** |
| Ceramic tile replacement (§23) | **4 yr** |
| Soft panel refresh (§23) | **6 yr** |
| Injury-score improvement | **66.2 %** |
| 10-year TCO saving | **+$1.85 M / 500 officers** |

---

## Per-platform verification

From each platform folder:

```bash
python platform_simulation.py
```

Regenerate full portfolio:

```bash
cd ../Weapons-Defence
python weapons_simulation.py
```

Regenerate lifecycle docs after config edits:

```bash
cd ../Weapons-Defence
python update_lifecycle_docs.py
```

---

## Related work

- [`../Weapons-Defence/`](../Weapons-Defence/) — military parent portfolio (MP-4.6M Guardian / Defender share §23 lifecycle)
- [`../Weapons-Defence/APES Body Armour/`](../Weapons-Defence/APES%20Body%20Armour/) — military APES
- [`../README.md`](../README.md) — repository index

---

[← Back to main README](../README.md)
