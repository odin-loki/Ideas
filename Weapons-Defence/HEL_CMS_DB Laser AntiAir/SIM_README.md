# HEL-CMS/DB — Simulation Coverage

**No runnable simulation in this repo.** HEL-CMS/DB engagement physics (dwell time, irradiance vs range, beam quality, adaptive optics loop bandwidth) are derived **first-principles inside the specification and research paper** — not computed by [`../weapons_simulation.py`](../weapons_simulation.py) or a standalone Python module.

---

## Where the numbers live

| Claim type | Source document |
|---|---|
| Dwell-to-kill vs threat class @ 3–5 km | [`HEL_CMS_DB_Full_Spec.md`](HEL_CMS_DB_Full_Spec.md) Part I — first-principles beam physics |
| Irradiance vs range (421.8 W/cm² @ 500 m → 395.9 @ 5 km) | Same — aperture + atmospheric transmission model |
| 20-year TCO ($71.8 M vs $123.6 M conventional) | Spec Part X + [`HEL_CMS_DB_Research_Paper.md`](HEL_CMS_DB_Research_Paper.md) |
| TDB-1M power output (250 kW(e) × 4 modules) | Spec Part V — TRL 2–3 conceptual; nine orders above Bristol C-14 demo |

---

## Why there is no sim script

The HEL portfolio entry predates integration into `weapons_simulation.py`. The spec explicitly documents closed-form laser heating, atmospheric transmission (Kim model), and saturation-attack timeline analysis inline. A future `hel_cms_sim.py` would need:
- Multi-threat engagement scheduler (6 simultaneous threats scenario)
- AO loop + jitter budget Monte Carlo
- TDB thermal/electrical output vs load duty cycle

None of these are implemented.

---

## Related portfolio simulation

| System | Coverage |
|---|---|
| Diamond battery power source | [`../../../Diamond Batterys/`](../../../Diamond%20Batterys/) — separate TRL documentation |
| Multi-target tracking adjacency | [`../../../Filtering/`](../../../Filtering/) — GH-SR-IMM (sensor fusion context) |

---

## Companion documents

| Document | File |
|---|---|
| Folder README | [`README.md`](README.md) |
| Engineering specification | [`HEL_CMS_DB_Full_Spec.md`](HEL_CMS_DB_Full_Spec.md) |
| Research paper | [`HEL_CMS_DB_Research_Paper.md`](HEL_CMS_DB_Research_Paper.md) |

---

*HEL-CMS/DB simulation coverage — first-principles numbers in spec/paper only. No runnable simulator in this repository.*
