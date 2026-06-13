# Rubber Tank Tracks — Simulation Coverage

**Portfolio simulator.** Tank-track pad acoustic transmissibility (steel vs HNBR rubber composite) is computed inside [`../weapons_simulation.py`](../weapons_simulation.py) and written to [`../weapons_sim_results.md`](../weapons_sim_results.md) **§19**.

---

## What is modelled

| Output | Method |
|---|---|
| Steel-on-steel transmissibility | Baseline track contact model |
| HNBR composite transmissibility | Rubber pad damping model |
| Net free-field SPL reduction | Difference at drive frequency |

### Headline results (§19)

At **300 Hz drive frequency** (typical track frequency at 30 km/h):

- Steel-on-steel transmissibility: **−22.3 dB**
- HNBR composite transmissibility: **−43.1 dB**
- **Net free-field SPL reduction: 20.8 dB**

Within the published 15–20 dB range for rubber track pads cited in the research paper.

---

## Quick start

```bash
cd ..
python weapons_simulation.py
```

Open `weapons_sim_results.md` and scroll to **§19. Tank-track pad noise reduction**.

---

## Key functions in `weapons_simulation.py`

| Function | Role |
|---|---|
| `track_pad_noise_reduction_dB()` (~line 1293) | Steel vs HNBR transmissibility at drive frequency |
| Tier-2 block (~line 1799) | Populates `tier2.track_pad_noise` |
| Markdown §19 writer | Renders reduction summary |

---

## What is NOT modelled

- Tread-pattern terrain scoring (6 679 / 10 000) — computed in-folder, not in `weapons_simulation.py`
- 25-year lifecycle cost ($282 235 / tank) — separate lifecycle analysis
- Road-damage / diplomatic mobility claims — engineering estimates in executive summary

---

## Companion documents

| Document | File |
|---|---|
| Executive summary | [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) |
| Research paper | [`Paper14_Military_Track_Pad.md`](Paper14_Military_Track_Pad.md) |
| TDP | [`MIL_SPEC_TRACK_PAD_TDP.md`](MIL_SPEC_TRACK_PAD_TDP.md) |
| Portfolio results | [`../weapons_sim_results.md`](../weapons_sim_results.md) §19 |

---

*Track-pad simulation coverage — acoustic transmissibility block only. Not validated against field SPL measurement on operational vehicles.*
