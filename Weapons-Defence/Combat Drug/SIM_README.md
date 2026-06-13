# Combat Drug — Simulation Coverage

**Portfolio simulator only.** Pharmacokinetic reference numbers for the HyperSynergy-X7 combat-drug stack are computed inside [`../weapons_simulation.py`](../weapons_simulation.py) and written to [`../weapons_sim_results.md`](../weapons_sim_results.md) **§20**.

**Important scope limit:** §20 models **one-compartment oral PK** for FDA-approved fielded stimulants (caffeine, modafinil, dextroamphetamine) at a standardised 80 kg subject. It does **not** simulate the six novel HSX7 depot compounds (MetaMax-2034, MetaFlow-47, etc.) — those have no published human PK to calibrate against.

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio physics engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder. **It also documents scope limits** — HSX7 depot PK is not simulated; §20 reference-stimulant oral PK is extracted.

```bash
python platform_simulation.py
```

To regenerate the full portfolio output, from this folder:

```bash
cd ..
python weapons_simulation.py
```

That writes [`../weapons_sim_results.md`](../weapons_sim_results.md) and [`../weapons_sim_results.json`](../weapons_sim_results.json).

---

## What is modelled

| Output | Method |
|---|---|
| C_max, t_max, t½, AUC | One-compartment oral absorption, first-order elimination |
| Reference drugs | Caffeine 200 mg, modafinil 200 mg, dextroamphetamine 10 mg PO |
| HSX7 proxy stack | Half-dose caffeine 100 mg + modafinil 100 mg (oral benchmark only) |

### Headline results (§20)

| Drug | Dose | t_max | C_max | t½ | AUC |
|---|---|---|---|---|---|
| Caffeine 200 mg PO | 200 mg | 0.8 h | 4 069.5 ng/mL | 5.0 h | 32 652 ng·h/mL |
| Modafinil 200 mg PO | 200 mg | 2.24 h | 2 113.1 ng/mL | 14.0 h | 47 496 ng·h/mL |
| Dextroamphetamine 10 mg PO | 10 mg | 2.26 h | 21.4 ng/mL | 10.0 h | 359 ng·h/mL |
| HSX7 proxy — caffeine 100 mg | 100 mg | 0.8 h | 2 034.7 ng/mL | 5.0 h | 16 326 ng·h/mL |
| HSX7 proxy — modafinil 100 mg | 100 mg | 2.24 h | 1 056.5 ng/mL | 14.0 h | 23 748 ng·h/mL |

---

## Quick start

```bash
cd ..
python weapons_simulation.py
```

Open `weapons_sim_results.md` and scroll to **§20. Combat-drug one-compartment PK**.

---

## Key functions in `weapons_simulation.py`

| Function / block | Role |
|---|---|
| Combat-drug PK block (~line 1310) | One-compartment oral absorption models |
| Tier-2 writer (~line 1801) | Populates `tier2.combat_drug_pk` |
| Markdown §20 writer | Renders results table |

---







## §23 Lifecycle

Portfolio lifecycle for **`Combat Drug`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `Combat Drug` — depot_shelf_cold_chain_mo=36; room_temp_hold_hr=72; autoinjector_shelf_mo=24 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Operator specification | [`Combat_Drug_Specification.md`](Combat_Drug_Specification.md) |
| Research paper | [`Combat_Drug_Research_Paper.md`](Combat_Drug_Research_Paper.md) |
| Portfolio results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §20 |