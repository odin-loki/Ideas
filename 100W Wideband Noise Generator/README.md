# 100W Wideband Noise Generator — Chua-circuit RF noise generator with FPGA supervision

> **A single Verilog module.** Chua chaotic-circuit RF noise generation with full digital supervision, controllable from 1 Hz to 14 GHz (hardware dependent) at up to 100 W continuous output. The Verilog source is itself the canonical specification — the README only describes what is in the file.

---

## ⚡ What this folder is

A single Verilog file (`100w_Wideband_Noise_Generator.v`) implementing the digital control surface for a high-power wideband chaotic noise generator. The module supervises a Chua-circuit op-amp core, the variable reactive components that tune chaos parameters, the buffer stages, the RF driver and power-amplifier chain, output filtering, the dual SMPS rails, and a full safety/protection architecture.

This folder contains **no formal research paper** — the design is captured in the Verilog header and module comments, plus the structural code itself. Performance figures previously listed in the README ("100 MHz–2 GHz", "−100 dBc/Hz phase noise", "≥ 10 MHz bandwidth") were not anchored in the source and have been removed.

---

## 📄 File

| File | Role |
|------|------|
| [`100w_Wideband_Noise_Generator.v`](100w_Wideband_Noise_Generator.v) | Top-level Verilog module — Chua chaotic core, RF chain, supervisor logic, safety architecture |

---

## 📋 Spec from the source header (verbatim)

| Parameter | Value |
|-----------|-------|
| Chaos source | Chua circuit (op-amp core) |
| Frequency range | 1 Hz – 14 GHz (hardware dependent) |
| Maximum RF output | 100 W continuous |
| Supply control | 12-bit DAC (`ps_voltage`) |
| FPGA target | Any device with sufficient I/O (Xilinx / Intel / Lattice) |
| Clock | Configurable (minimum frequency determined by §6 of the source) |

Quantitative performance (phase noise, in-band flatness, exact spurious-free dynamic range) depends on the specific analogue front-end built around this controller and is **not** specified by the digital module alone.

---

## 🛠 What the Verilog module actually controls

Roughly grouped from the I/O list at the top of the source:

- **Chua core op-amp** — biases (12-bit DACs), programmable gain selection.
- **Chua reactive components** — switched inductor tuning word, capacitor bank, resistor bank (sets Chua-diode slope).
- **Chua buffers** — input / output buffer biases, gain selection for flat PSD compensation.
- **Chaos control** — external chaos-parameter injection DAC, piecewise-linear nonlinearity segment select.
- **RF chain — driver** — bias, gain, enable.
- **RF chain — power amplifier** — Class-AB quiescent bias, drive level, sub-band switch matrix select, enable.
- **Output conditioning** — digital step attenuator, output filter bank, automatic impedance-matching network.
- **Power supplies — primary** — main SMPS enable, SCR crowbar trigger, voltage and current set-points.
- **Power supplies — secondary / bias** — additional rails for buffers, drivers, reference DACs.
- **Protection / monitoring** — overvoltage and arc detection (crowbar), interlocks, thermal sensing array (referenced in body), VSWR and EMC handling.

---

## 🧭 Where this fits in the repo

This is essentially a **defence / EW-relevant** wideband interference and test source: a controllable high-power noise emitter with a wide operating band, suitable for receiver-saturation tests, COMINT / SIGINT susceptibility analysis, white-noise crypto testing, and (with appropriate licensing and propagation-safety controls) jamming research. It is presented as a **design** at the digital-supervision layer — the analogue components, RF amplifier topology, power thermals, and regulatory licensing are not specified here.

---

## 🚧 Honest framing

- The Verilog module is the **only artefact** — there is no companion research paper, mathematical specification, or measurement report in this folder.
- The 100 W / 1 Hz – 14 GHz banner numbers come from the source header comment and are explicitly tagged "hardware dependent" — they describe the controller's intent, not measured RF performance of any specific build.
- High-power wideband emitters are subject to spectrum licensing and EMC regulations; the source is not a deployment guide.

---

## 🔗 Related work in this repo

- [`RNGS/`](../RNGS/) — chaotic RNG (`Chaotic RNG/`) shares Chua-circuit / nonlinear-dynamics ancestry; turbulent-flow and DAG RNG also use chaos analogues
- [`ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — Meta-DAG RNG depends on a high-quality entropy source of this kind for keystream synchronisation
- [`Break AES/`](../Break%20AES/) — cryptanalysis context (signal-side and side-channel)
- [`Filtering/`](../Filtering/) — adaptive filtering / robust tracking is the natural countermeasure to high-power noise emitters

---

[← Back to main README](../README.md)
