# 100W Wideband Noise Generator

> **A single SystemVerilog file (`complete_noise_generator`) that orchestrates a Chua-circuit chaotic analogue core, a four-band RF power-amplifier chain, a 12-bit programmable supply DAC, an eight-channel thermal ADC, and a hard-protection state machine — into one digitally-supervised wideband noise platform with banner targets of `1 Hz – 14 GHz` (hardware-dependent) and `100 W` continuous output.** The pitch is unusual: the Verilog file *is* the specification. Most "noise generator" papers ship a research write-up that gestures at HDL; this folder ships the HDL with the supervisory architecture (chaos parameter DACs, band-mapped PA staging, SMPS setpoints, LCD UI, fault taxonomy) all in one source — a foundation for a high-power EW/test-source-class build with sub-microsecond fault response.

---

## What this folder is

Wideband noise generators are a niche corner of RF instrumentation that doesn't have many "complete" reference designs in the open. The commercial high-power test sources are closed, the chaos-circuit literature is fragmented across analogue-circuits papers, and the "100 W" tier is rare enough that most amateur builds top out at a watt or two on a benchtop. This folder is one author's attempt to put a digital supervision architecture under the whole stack: a Chua chaotic oscillator (op-amp core, switched `L/C/R` banks, piecewise-linear nonlinearity segment select, `chaos_dac` injection) handles the analogue noise generation, a four-band PA chain handles power amplification, a 12-bit DAC sets supply voltages, an eight-channel ADC monitors thermals, and an LCD-driven user interface plus an SCR crowbar plus arc-detect plus VSWR-trip safety subsystem keeps the whole thing alive. The novelty is that all of this lives in *one Verilog file* you can read top-to-bottom in an afternoon.

The output performance — phase noise, SFDR, flatness across the band — is fundamentally limited by the analogue-electronics build, which is *outside* this file. The Verilog targets the *control intent*; the realised performance is hardware-dependent. The folder is honest about that.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`100w_Wideband_Noise_Generator.v`](100w_Wideband_Noise_Generator.v) | The complete design. Module `complete_noise_generator`. Header targets: `1 Hz – 14 GHz`, `100 W`, FPGA-agnostic (Xilinx / Intel / Lattice noted). |

> **Folder note.** No standalone `.md` research paper accompanies the Verilog. The HDL header is primary; this README is the prose layer.

---

## 🧠 Subsystems (in the source)

| Subsystem | What it does |
|---|---|
| **Chua chaotic oscillator** | Op-amp core with switched L/C/R banks, piecewise-linear nonlinearity segment select via `chaos_dac` injection. Source of the wideband noise. |
| **`ps_voltage` DAC** | 12-bit programmable supply DAC controlling rail voltage. |
| **RF PA chain** | Four-band staging from `freq_pot`: **DC – 500 MHz**, **500 MHz – 2 GHz**, **2 – 6 GHz**, **6 – 14 GHz**. |
| **Eight-channel thermal ADC** | Multi-point thermal monitoring. |
| **Protection subsystem** | `MAX_TEMP = 85 °C` hard trip, `77 °C` warning, `VSWR 3:1` reference, **SCR crowbar**, **arc_detect**, **fast_shutdown** in **sub-microsecond** budget. Fault taxonomy: `FAULT_VSWR`, `FAULT_ARC`, `FAULT_TEMP`, etc. |
| **Startup sequencer** | Cycle-counted: `T_AUX_SETTLE = 256`, `T_BIAS = 512`, `T_PS_SETTLE = 768`, `T_DRV_SETTLE = 1 024` clock cycles. |
| **LCD UI** | Operator-facing controls + status. |

---

## 📊 Banner targets (header, hardware-dependent)

| Parameter | Target |
|---|---|
| Frequency range | **`1 Hz – 14 GHz`** |
| Output power | **`100 W`** continuous |
| Bands | DC – 500 MHz, 500 MHz – 2 GHz, 2 – 6 GHz, 6 – 14 GHz |
| Fast-shutdown latency | **sub-microsecond** |
| Thermal trip | `85 °C` |
| VSWR trip | `3:1` |
| FPGA family | Xilinx / Intel / Lattice |

---

## 🚧 Honest caveats

- **No measured RF performance data** in this folder. The frequency / power / phase-noise figures are *controller intent*; realised performance depends on the analogue build (PCB layout, PA selection, filtering, shielding).
- **No standalone research paper.** The Verilog header is primary.
- **No EMC / regulatory analysis.** A 100 W wideband emitter at GHz frequencies has serious regulatory implications that are not addressed here.
- **Not a deployment guide.** This is a design-intent document, not a build-and-deploy manual.

---

## 🎯 What this displaces

| Standard | Limitation | What this design offers |
|---|---|---|
| Commercial closed-source noise sources | $$$, opaque | Open Verilog supervision architecture |
| Bench-top chaos-circuit kits | < 1 W, narrow band | 100 W banner target, four-band staging |
| Software-defined radio noise generation | Limited bandwidth, low power | Analogue chaos with full-band PA chain |
| Ad-hoc safety circuits | Bolt-on after the fact | Fault taxonomy + SCR crowbar + arc-detect built into the supervisor from the start |

---

## 🔗 Related work in this repo

- [`../CPU/`](../CPU/) — sister single-file HDL design culture
- [`../New Classes of Electrical Components/`](../New%20Classes%20of%20Electrical%20Components/) — hybrid passive components that could feed this PA chain
- [`../RNGS/Chaotic RNG/`](../RNGS/Chaotic%20RNG/) — SynerChaos chaotic-PRNG sister work
- [`../Physics/`](../Physics/) — chaos-theory backdrop
- [`../Weapons/`](../Weapons/) — defence-tech R&D portfolio (EW context)

---

[← Back to main README](../README.md)
