# Neural Dust — Neural Quantum Dust two-tier neural-interface architecture (NQD)

> **A specific, named architecture — not a metaphor — comprising three layers: **`150–250 nm` fluorescent nanodiamond NV-centre "QND" quantum sensors** at cellular scale (`~10³` per mm³, `~10⁶` for a `10 cm³` cortical target), **`80–150 µm` ultrasound-powered "APEX" CMOS motes** at sub-millimetre scale (`~1 / 0.5–1 mm³`, `~10⁴` for the same target), and an **external CMUT "WTA" wearable patch** as the energy and data uplink — explicitly *correcting* four physics misconceptions in the original Neural Dust vision (no `20 nm` general compute, no thermoelectric bio-power at scale, no entanglement comms, no `+40 %` working-memory enhancement claim) and reframing ambition against demonstrated benchmarks (Utah-array speech BCI, Card et al. NEJM 2024).** The number budget is honest: AlN piezo `k_t² = 0.28` at `10 MHz` resonance gives **`~8 nW` harvested power** at `I₀ = 50 mW/cm²` and `2 cm` brain depth (using `α ≈ 0.5 dB/cm/MHz` attenuation), against a subsystem total `~4–6 nW` continuous average — a tight ledger that *closes*. Magnetometry delivers **`~2–3 nT/√Hz`** sensitivity per QND with isotopically-purified `≥ 99.99 % ¹²C` cores, **`T₂* = 10–100 µs`** bare at 37 °C, and **CPMG `T₂ = 0.5–4.3 ms`** plus **`¹⁴N` nuclear memory `T₂ ~ 0.9–100 ms`**. FDA acoustic safety closes at **MI ~ 0.4** vs limit `0.7` and **TI_B ~ 0.3** vs limit `1.0`. Acoustic backscatter at FSK `Δf = 100 kHz` per mote with TDMA `10 µs` slot scales to **`10⁴` motes per `100 ms` frame** for `~1 kbps/mote × 10⁴ = ~10 Mbps` aggregate. Roadmap is `15–25 years` across phases 0 – 4, `~2027 – 2037+`. Every component is tagged Verified / Plausible / Speculative.

---

## 🧠 What this folder is

A single long-form architecture document describing the NQD system in full: physics, fabrication, deployment, OS-style protocol stack, and clinical roadmap. Every component is tagged with one of three readiness markers: **Verified** (already demonstrated), **Plausible** (physically consistent, not yet demonstrated), or **Speculative** (long-range, valid physics).

---

## 📄 Files

| File | Role |
|------|------|
| [`NQD_Neural_Quantum_Dust_Architecture.md`](NQD_Neural_Quantum_Dust_Architecture.md) | Full architecture paper — Tier 1 QND + Tier 2 APEX + Wearable Transceiver Array (WTA), with mathematics, fabrication specs, deployment protocols, OS model, clinical roadmap, references |

(This is the only paper in the folder. Earlier README copy referenced a generic `research_paper.md` — that file does not exist.)

---

## 🏗 The two-tier architecture

The core insight: no single device can simultaneously satisfy quantum coherence, electronic complexity, ultrasonic power harvesting, and biological minimalism at the same physical scale. NQD therefore separates these into two cooperating device classes plus an external wearable.

| Tier | Device | Scale | Role |
|------|--------|-------|------|
| **Tier 1** | **QND — Quantum Nanodiamond** | 150–250 nm | Quantum sensing, nuclear-spin memory, biomarker detection |
| **Tier 2** | **APEX — Acoustic Processing & Exchange** mote | 80–150 µm | Ultrasonic power harvest, optical readout of nearby QNDs, signal processing, neural stimulation, acoustic backscatter comms |
| **External** | **WTA — Wearable Transceiver Array** | wearable patch | Beamformed ultrasonic power delivery, data aggregation, real-time processing |

Deployment density: ~10³ QND particles per mm³ (quantum magnetometry coverage), ~1 APEX mote per 0.5–1 mm³. A 10 cm³ cortical target volume → ~10⁶ QND + ~10⁴ APEX. QNDs delivered IV with transferrin-receptor BBB transcytosis; APEX motes via stereotactic needle injection.

---

## 🔬 Tier 1 — Quantum Nanodiamond (QND)

Synthetic fluorescent nanodiamond, isotopically purified (≥ 99.99 % ¹²C), with NV centres and a multi-layer surface engineering stack:

1. **Isotopically purified diamond core** (150–200 nm) — 1–5 NV per particle, T₂* 10–100 µs bare, T₂ 0.5–4.3 ms with CPMG-16 at 37 °C, ¹⁴N nuclear spin T₂ 0.9–100 ms.
2. **Hydrogen-terminated surface** (0.5 nm) — negative electron affinity, NV⁻ stabilisation.
3. **Carboxyl / HPG functionalisation** (1–2 nm) — cell-population-specific uptake; mixed surface for primary deployment (HPG + anti-TfR1 + anti-NeuN).
4. **PEG-2000 anti-fouling brush** (2–3 nm) — extends plasma half-life from minutes to hours.

Sensing capabilities (with single-NV / few-NV physics):

| Sensing modality | Sensitivity | Use |
|------------------|-------------|------|
| DC magnetometry (Ramsey) | ~3 nT/√Hz single NV; ~2 nT/√Hz with 3 NVs | Action-potential detection at 5–10 µm proximity |
| Thermometry (zero-field-splitting shift) | ~10 mK/√Hz | Neural-metabolic mapping |
| Electric field (Stark shift) | ~1 mV/µm/√Hz | Extracellular AP amplitude detection |
| Nuclear-spin quantum memory | ¹⁴N register, T₂ 0.9–100 ms at 37 °C | Genuine quantum memory at body temperature |

**Verified anchors:** NV magnetic sensitivity for action-potential detection has been demonstrated in TIRF-ODMR experiments (ACS AMI 2024); intracellular NV thermometry/magnetometry shown in Discover Nano 2025; IV-injectable nanodiamond uptake demonstrated in non-human primates at up to 25 mg/kg with no organ dysfunction (PNAS Nexus 2024).

---

## ⚙️ Tier 2 — APEX mote

80–150 µm aluminium-nitride piezoelectric + 65 nm CMOS hybrid on a parylene-C flexible substrate. Functions:

- **Power harvest** from external ultrasound at sub-µW–nW levels.
- **Optical readout** of surrounding QND fluorescence.
- **Local signal processing** in CMOS.
- **Neural stimulation** when targeted by the WTA.
- **Acoustic backscatter** communication to the WTA.

Targets in the paper include nW-scale harvest, ~0.24 mm³ device volume, retrievable via minimally invasive procedure.

---

## 📡 External — Wearable Transceiver Array (WTA)

Patch-form ultrasonic phased array providing beamformed power delivery, data aggregation, and host-side real-time processing.

---

## 🧪 Five non-negotiable design principles (from §1.1)

1. Minimum footprint per unit of capability.
2. Power autonomy — no batteries, no transcranial wires, no tethers.
3. Quantum-classical hybrid processing — NV register used **only** for tasks where quantum mechanics gives a decisive advantage (nanoscale magnetometry, thermometry, coherent memory).
4. Graceful degradability — spatial redundancy, independent per-node operation.
5. Biological reversibility — Tier 1 QNDs metabolically cleared on a 2–4 week timescale; Tier 2 APEX motes retrievable.

---

## 🚧 Honest framing

The paper itself uses the **Verified / Plausible / Speculative** legend on every component. Several key building blocks (single-AP NV detection in vivo, isotopically purified IV-injectable FNDs, APEX-scale ultrasonic CMOS motes) are individually demonstrated in literature; the integrated NQD system is a design proposal, not a built device.

---

## 🔗 Related work in this repo

- [`../Quantum Diamond Wafer/`](../Quantum%20Diamond%20Wafer/) — QDMP and CVD work share the NV-centre / isotopically-purified-diamond material base
- [`../Diamond Batterys/`](../Diamond%20Batterys/) — same diamond / NV physics applied to power conversion rather than biomedical sensing
- [`odin-loki/cellai`](https://github.com/odin-loki/cellai) — biological-substrate inspiration for distributed neural compute
- [`odin-loki/cypha`](https://github.com/odin-loki/cypha) — signal-processing / ML stack relevant to backend processing of neural sensor data

---

[← Back to main README](../README.md)
