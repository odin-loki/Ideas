# ASNP — Simulation Coverage

**No dedicated ASNP simulator.** Advanced Sports Nutrition Powder formulation numbers are **spec- and literature-derived**, not computed by a standalone script or a dedicated row in [`../../weapons_simulation.py`](../../weapons_simulation.py).

---

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio engine ([`../../weapons_simulation.py`](../../weapons_simulation.py)) via [`../../sim_common.py`](../../sim_common.py) and prints the platform-specific verification slice for this folder. ASNP formulation claims are **scope-limited**; the script anchors nearest portfolio coverage via TACT-1 ration shelf life (§22).

```bash
python platform_simulation.py
```

To regenerate the full portfolio results file, still run:

```bash
cd ../..
python weapons_simulation.py
```

---

## Related portfolio simulation

| Topic | Coverage |
|---|---|
| HBCD low osmolality principle | Shared with TACT-1 Mark II — discussed in parent spec §osmolality |
| TACT-1 shelf life (Q10 Arrhenius) | Portfolio **§22** in [`../../weapons_sim_results.md`](../../weapons_sim_results.md) |
| Injectable osmolality failure mode | Portfolio **§21** — contrast for IV vs oral delivery routes |

ASNP's per-serving osmolality when mixed with 500 mL water is engineered to stay within GI tolerance (see [`ASNP_Specification.md`](ASNP_Specification.md)) — this is a **hand calculation / literature anchor**, not a simulator output.

---

## PODS subfolder (separate sim)

The sibling [`../PODS- Edible High Energy Protein/pods_simulation.py`](../PODS-%20Edible%20High%20Energy%20Protein/pods_simulation.py) models synthetic lipid energy density — adjacent but not ASNP.

---







## §23 Lifecycle

Portfolio lifecycle for **`ASNP Sports Nutrition`** — [`../../weapon_lifecycle.py`](../../weapon_lifecycle.py) / [`../../weapons_sim_results.md`](../../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `ASNP Sports Nutrition` — product_shelf_mo=24; opened_container_days=30 |

| Lifecycle results | [`../../weapons_sim_results.md`](../../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../../weapon_lifecycle.py`](../../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Lifecycle results | [`../../weapons_sim_results.md`](../../weapons_sim_results.md) §23 |
| ASNP specification | [`ASNP_Specification.md`](ASNP_Specification.md) |
| ASNP research paper | [`ASNP_Research_Paper.md`](ASNP_Research_Paper.md) |
| Parent TACT-1 platform | [`../README.md`](../README.md) |