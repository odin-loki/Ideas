# Hearing Protection — Simulation Coverage

**No standalone simulator.** Muzzle blast and layered hearing-protection numbers are computed inside the portfolio-wide [`../weapons_simulation.py`](../weapons_simulation.py) script and written to [`../weapons_sim_results.md`](../weapons_sim_results.md) **§6**.

APE-1 / HANC-1 product NRR claims (37.8 / 42.6 dB) are **not** independently derived from this simulator — they come from acoustic modelling in the specification.

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio physics engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder. **It also documents scope limits** — APE-1 / HANC-1 NRR claims are spec-internal; portfolio §6 threat-side muzzle SPL and layered protection stacks are extracted per weapon.

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

## What §6 models

### Muzzle peak SPL

Calibration anchors (Stevens / Westin 1975 adapted):

- 5.56 × 45 NATO carbine: ≈ 165 dB muzzle, 158 dB shooter ear
- 7.62 × 51 NATO rifle: ≈ 166 dB muzzle, 159 dB shooter ear
- .50 BMG: ≈ 178 dB muzzle, 170 dB shooter ear
- 120 mm tank gun: ≈ 187 dB muzzle

Shooter-ear column is ~7 dB below muzzle.

### Layered protection columns

| Stack | Attenuation model |
|---|---|
| Foam plug | −22 dB |
| Double plug + muff | −28 dB |
| Double + TACS personal ANC | −28 dB passive + 25 dB active |

Rendered per weapon in §6 table: muzzle (unsup), ear (unsup), muzzle (sup), ear (sup), ear + plug, ear + double, ear + double + TACS.

---

## Key functions in `weapons_simulation.py`

| Function | Role |
|---|---|
| `muzzle_peak_spl_dB()` | Unsuppressed peak SPL from muzzle energy / chamber volume |
| `hearing_protection_layered_dB()` | Net SPL at eardrum behind layered protection stack |
| Tier-2 acoustic block | Builds per-weapon SPL table → `tier2.acoustic` |
| Markdown §6 writer | Renders results table (~line 1947) |

---

## Quick start

```bash
cd ..
python weapons_simulation.py
```

Open `weapons_sim_results.md` → **§6. Muzzle blast & hearing-protection stack (peak SPL, dB)**.

---

## Related portfolio section

- **§18 — TACS Nelson–Elliott cancellation** — personal active-noise-cancellation bound for the wearable 16-element array in [`../Military Noise Cancellation/`](../Military%20Noise%20Cancellation/). See `weapons_sim_results.md` §18.

---






## §23 Lifecycle

Portfolio lifecycle for **`Hearing Protection`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `Hearing Protection` — foam_plug_life_mo=6; electronic_muff_seal_mo=24; earplug_NRR_derated_dB=22 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`Hearing_Protection_Specification.md`](Hearing_Protection_Specification.md) |
| Research paper | [`Hearing_Protection_Research_Paper.md`](Hearing_Protection_Research_Paper.md) |
| Portfolio results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §6 |