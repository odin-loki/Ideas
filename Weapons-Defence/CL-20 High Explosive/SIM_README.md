# Proteinated CL-20 — Simulation Coverage

**Dual simulation path:** (1) standalone [`cl20_simulation.py`](cl20_simulation.py) for proteinated impact-sensitivity / hydrogen-bonding stabilisation metrics; (2) portfolio [`../weapons_simulation.py`](../weapons_simulation.py) **§17** for Kamlet–Jacobs detonation chemistry (neat explosive comparison table).

---

## What is modelled

### Portfolio §17 — Kamlet–Jacobs detonation chemistry

| Explosive | ρ (g/cm³) | P_CJ (GPa) | VOD (km/s) | Brisance (TNT=100) |
|---|---|---|---|---|
| **CL-20** | 2.04 | 45.3 | 9.75 | 205.0 |
| HMX | 1.905 | 36.7 | 8.95 | 166.0 |
| RDX | 1.806 | 32.9 | 8.6 | 149.0 |
| TNT | 1.654 | 22.1 | 7.25 | 100.0 |

Proteinated CL-20 numbers (~41 GPa, ~9.4 km/s, brisance ~185) are **explicit extrapolations** documented in the research paper — not separate §17 rows.

### Standalone `cl20_simulation.py`

| Module | Role |
|---|---|
| `QuantumMechanicalCalculator` | DFT-calibrated hydrogen-bond energy |
| `ProteinatedCL20Analyzer` | HBSI, IEDF, PSC stabilisation metrics |
| Impact-sensitivity extrapolation | Spider-Silk config → **15.2 J** (vs 1.5 J neat) — computational, not BAM measured |

---

## Quick start

### Portfolio detonation table (§17)

```bash
cd ..
python weapons_simulation.py
```

Open `weapons_sim_results.md` → **§17. Energetic detonation chemistry**.

### Standalone proteination framework

```bash
cd "CL-20 High Explosive"
python cl20_simulation.py
```

See script header and [`README.md`](README.md) for validated headline table.

---

## Key functions

| Location | Function / block | Role |
|---|---|---|
| `weapons_simulation.py` | Kamlet–Jacobs block (~line 1770) | Neat explosive P_CJ, VOD, Gurney |
| `cl20_simulation.py` | `calculate_hbond_energy()` | Interface stabilisation energy |
| `cl20_simulation.py` | Main analysis runner | Proteinated safety metrics vs neat CL-20 |

---

## Companion documents

| Document | File |
|---|---|
| Folder README | [`README.md`](README.md) |
| Research paper | [`Proteinated_CL20_Safe_Explosive_Paper.md`](Proteinated_CL20_Safe_Explosive_Paper.md) |
| Portfolio results §17 | [`../weapons_sim_results.md`](../weapons_sim_results.md) §17 |

---

*CL-20 simulation coverage — Kamlet–Jacobs + computational proteination model. Not validated against cylinder expansion or BAM fall-hammer measurement.*
