# ASNP — Simulation Coverage

**No dedicated ASNP simulator.** Advanced Sports Nutrition Powder formulation numbers are **spec- and literature-derived**, not computed by a standalone script or a dedicated row in [`../../weapons_simulation.py`](../../weapons_simulation.py).

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

## Companion documents

| Document | File |
|---|---|
| ASNP specification | [`ASNP_Specification.md`](ASNP_Specification.md) |
| ASNP research paper | [`ASNP_Research_Paper.md`](ASNP_Research_Paper.md) |
| Parent TACT-1 platform | [`../README.md`](../README.md) |

---

*ASNP simulation coverage — prose / literature formulation rationale only. No runnable ASNP simulator.*
