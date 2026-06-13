# TACS — Simulation Coverage

**Portfolio simulator.** Active acoustic cancellation depth for the Tactical Acoustic Cancellation System (TACS) is computed inside [`../weapons_simulation.py`](../weapons_simulation.py) and written to [`../weapons_sim_results.md`](../weapons_sim_results.md) **§18**.

---

## Local verification script

[`platform_simulation.py`](platform_simulation.py) runs the portfolio engine ([`../weapons_simulation.py`](../weapons_simulation.py)) via [`../sim_common.py`](../sim_common.py) and prints the platform-specific verification slice for this folder (TACS §18 cancellation depth).

```bash
python platform_simulation.py
```

To regenerate the full portfolio results file, still run:

```bash
cd ..
python weapons_simulation.py
```

---

## What is modelled

| Output | Method |
|---|---|
| Per-octave cancellation depth (dB) | Nelson–Elliott (1992) asymmetric-power bound |
| A-weighted broadband average | Weighted sum across 125 Hz – 4 kHz octave bands |
| Variants | Personal (16-element), Mobile (64-element), Fixed (64-element) |

### Headline results (§18)

| Variant | 125 Hz | 250 Hz | 500 Hz | 1 kHz | 2 kHz | 4 kHz | A-weighted avg |
|---|---|---|---|---|---|---|---|
| Personal (3–5 m zone) | 40.0 | 40.0 | 40.0 | 39.1 | 32.1 | 25.1 | **36.3** |
| Mobile (8–15 m zone) | 43.6 | 43.6 | 41.4 | 37.4 | 30.4 | 23.4 | **36.0** |
| Fixed (30–60 m zone) | 43.6 | 41.4 | 37.4 | 33.4 | 26.4 | 19.4 | **32.4** |

---

## Quick start

```bash
cd ..
python weapons_simulation.py
```

Open `weapons_sim_results.md` and scroll to **§18. TACS active acoustic cancellation depth**.

---

## Key functions in `weapons_simulation.py`

| Function | Role |
|---|---|
| `tacs_cancellation_dB()` (~line 1251) | Cancellation depth vs element spacing and frequency |
| Tier-2 block (~line 1779) | Evaluates Personal / Mobile / Fixed variants |
| Hearing-protection integration (~line 680) | `tacs_active` flag adds ~25 dB on passive stack in §ear-damage tables |

---






## §23 Lifecycle

Portfolio lifecycle for **`TACS Military Noise Cancellation`** — [`../weapon_lifecycle.py`](../weapon_lifecycle.py) / [`../weapons_sim_results.md`](../weapons_sim_results.md) §23.

| Item | Detail |
|---|---|
| **§23 Lifecycle** | `TACS Military Noise Cancellation` — wearable_array_service_yr=8; vehicle_array_service_yr=10; battery_cycle_life=500 |

| Lifecycle results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §23 |
| Lifecycle simulator | [`../weapon_lifecycle.py`](../weapon_lifecycle.py) |

## Companion documents

| Document | File |
|---|---|
| Operator specification | [`TACS_Complete_Specification.md`](TACS_Complete_Specification.md) |
| System paper | [`Paper11_TACS_System.md`](Paper11_TACS_System.md) |
| Energy physics paper | [`Paper12_TACS_Energy_Physics.md`](Paper12_TACS_Energy_Physics.md) |
| Portfolio results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §18 |