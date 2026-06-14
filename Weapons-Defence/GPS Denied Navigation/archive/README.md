# Archive — legacy navigation simulations

This folder holds **superseded** Monte Carlo scripts and one-off reports from early AGINS validation work. Do not use these for headline numbers or new development.

| File | Status |
|---|---|
| [`nav_sim_soldier.py`](nav_sim_soldier.py) | **Superseded** by [`../agins_sim_package/`](../agins_sim_package/) — soldier MEMS scenarios, GH-SR-IMM filter, and consolidated reporting now live in the package |
| [`nav_sim_soldier_report.md`](nav_sim_soldier_report.md) | **Superseded** output from `nav_sim_soldier.py`; retained for historical comparison only |

## Why archived

The standalone soldier script validated the PDR speed / heading decoupling insight and GH-SR-IMM soldier scenarios in a single monolithic file. The **`agins_sim_package`** refactor splits ship and soldier platforms, shares one filter core with [`../../../Filtering/`](../../../Filtering/), and writes reproducible reports under `agins_sim/outputs/`.

Re-run current validation from the platform root:

```bash
python platform_simulation.py
```

See [`../SIM_README.md`](../SIM_README.md) for the active module map.

[← Platform README](../README.md)
