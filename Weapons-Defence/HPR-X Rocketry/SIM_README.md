# HPR-X Rocketry — Simulation Coverage

**Portfolio simulator §16** plus **in-folder Tier-1 RASAero / RK45 trajectory pipeline** documented in the research paper. Two simulation tiers serve different airframe scales.

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio physics engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder — Tier-2 HPR-X V1 / V2 / V3 trajectory rows from portfolio §16.

```bash
python platform_simulation.py
```

To regenerate the full portfolio output, from this folder:

```bash
cd ..
python weapons_simulation.py
```

That writes [`../weapons_sim_results.md`](../weapons_sim_results.md) and [`../weapons_sim_results.md`](../weapons_sim_results.md).

---

## Tier-2 — `weapons_simulation.py` §16

Tsiolkovsky thrust accounting + ICAO atmosphere drag integration for **upscaled HPR-X airframes** (75 mm / 98→75 mm two-stage / 152 mm). Subsonic `C_d ≈ 0.55`, supersonic `0.65`.

| Vehicle | High-angle apogee | 35° max range | Burnout v |
|---|---|---|---|
| HPR-X V1 (75 mm, L1390) | 5 782 m | 6 408 m | 1 093.5 m/s |
| HPR-X V2 (98→75 mm, M+K) | 7 914 m | 7 342 m | 1 477.6 m/s (sustainer) |
| HPR-X V3 (152 mm, N5800) | 2 523 m (35°) | 6 502 m | 1 293.3 m/s |

Source: [`../weapons_sim_results.md`](../weapons_sim_results.md) §16.

### Quick start (Tier-2)

```bash
cd ..
python weapons_simulation.py
```

---

## Tier-1 — hobby airframe RK45 (paper methodology)

The headline hobby-class numbers in [`README.md`](README.md) (3 443 / 3 998 / 5 455 / 7 916 m) come from a **separate** `scipy.integrate.solve_ivp` RK45 pipeline with RASAero-II-derived Cd tables — documented in [`Paper19_HPR-X_Guided_Rocketry.md`](Paper19_HPR-X_Guided_Rocketry.md). This pipeline is **not** a standalone script in the folder; it is described in the paper's methodology section.

| Variant | Single-stage range | Best two-stage |
|---|---|---|
| V1 Sprint (29 mm) | 3 443 m | 5 502 m |
| V2 Transonic (38 mm) | 3 998 m | 7 055 m |
| V3 Supersonic (54 mm) | 5 455 m | 7 916 m |

Tier-1 and Tier-2 cross-check to within ~3 % on un-ballasted reference configurations.

---

## Key functions in `weapons_simulation.py`

| Block | Role |
|---|---|
| Rocket trajectory module (~line 1052) | Stage definitions, ICAO drag, burnout states |
| Tier-2 writer (~line 1741) | V1 / V2 / V3 upscaled runs |
| Markdown §16 writer | Renders apogee, range, burnout table |

---






## §23 Lifecycle

Portfolio lifecycle for **`HPR-X Rocketry`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `HPR-X Rocketry` — motor_case_life_flights=50; nozzle_insert_life_flights=30; avionics_battery_cycles=200 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Folder README | [`README.md`](README.md) |
| Operator spec | [`HPR-X Series Spec.md`](HPR-X%20Series%20Spec.md) |
| Research paper (Tier-1 methodology) | [`Paper19_HPR-X_Guided_Rocketry.md`](Paper19_HPR-X_Guided_Rocketry.md) |
| Portfolio results §16 | [`../weapons_sim_results.md`](../weapons_sim_results.md) §16 |