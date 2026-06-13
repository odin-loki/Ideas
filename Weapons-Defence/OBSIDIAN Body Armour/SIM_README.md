# OBSIDIAN Body Armour — Simulation Coverage

**No runnable simulation.** Project OBSIDIAN (torso-only secret-service suit) is a **hypothetical materials study**. The portfolio [`../weapons_simulation.py`](../weapons_simulation.py) does **not** include an OBSIDIAN ballistic, thermal, or chemical-resistance model.

---

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder. For OBSIDIAN, the script **documents scope limits only** — carbyne/STF suit claims are not modelled; see APES Body Armour (§13) for validated armour numbers.

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
| V50 / multi-hit ballistic performance | Document-internal design targets only |
| Backface deformation (< 10 mm) | Not computed in simulator |
| Carbyne / graphene material properties | Speculative — no engineering-scale supply chain |
| Thermal / CBRN resistance | Not modelled |

For **simulation-validated** body armour in this portfolio, see [`../APES Body Armour/SIM_README.md`](../APES%20Body%20Armour/SIM_README.md) (`weapons_simulation.py` §13).

---






## §23 Lifecycle

Portfolio lifecycle for **`OBSIDIAN Body Armour`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | Hypothetical carbyne / STF suit — no runnable ballistic lifecycle model. |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`OBSIDIAN_Secret_Service_Suit_Specification.md`](OBSIDIAN_Secret_Service_Suit_Specification.md) |
| Research paper | [`OBSIDIAN_Research_Paper.md`](OBSIDIAN_Research_Paper.md) |
| Full-body successor | [`../OBSIDIAN-X Body Armour/`](../OBSIDIAN-X%20Body%20Armour/) |