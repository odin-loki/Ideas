# OBSIDIAN-X Body Armour — Simulation Coverage

**No runnable simulation.** Project OBSIDIAN-X is a **hypothetical full-body combat-armour academic study**. The portfolio [`../weapons_simulation.py`](../weapons_simulation.py) does **not** model OBSIDIAN-X ballistic, thermal, power, or cloaking performance.

---

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder. For OBSIDIAN-X, the script **documents scope limits only** — full-body armour, cloaking, and power claims are not modelled; see APES Body Armour (§13) for validated V50/BFD methodology.

```bash
python platform_simulation.py
```

To regenerate the full portfolio results file, still run:

```bash
cd ..
python weapons_simulation.py
```

---

## Why there is no sim

| Claim type | Status |
|---|---|
| 7.62 mm AP V50 / multi-hit | Document-internal design targets — not measured V50 |
| Metamaterial cloaking (visible + thermal + radar) | Not modelled — laboratory narrow-band only in literature |
| Cs-137 / Co-60 nuclear battery at 10 W | Not modelled — published devices are µW–mW class |
| Environmental envelope (−60 °C, 100 m depth, 8 000 m) | Not modelled |

For **simulation-validated** armour panels, see [`../APES Body Armour/SIM_README.md`](../APES%20Body%20Armour/SIM_README.md) (§13).

---






## §23 Lifecycle

Portfolio lifecycle for **`OBSIDIAN-X Body Armour`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | Full-body hypothetical armour — no runnable lifecycle model. |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`OBSIDIAN_X_Specification.md`](OBSIDIAN_X_Specification.md) |
| Research paper | [`OBSIDIAN_X_Research_Paper.md`](OBSIDIAN_X_Research_Paper.md) |
| Torso-only predecessor | [`../OBSIDIAN Body Armour/`](../OBSIDIAN%20Body%20Armour/) |