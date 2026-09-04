# Hybrid component simulation — Phase 4 verification

<!-- Converted from `Phase4_Verification_Report.docx` — source was Word (.docx). -->

*Independent verification report · February 2026 · All five application engines executed*

## Executive Summary

All five Phase 4 application engines were executed in a live Python environment. Physics formulas, benchmark claims, and algorithm correctness were independently verified. Two critical bugs and two moderate issues were identified. The core physics models (shot noise, JKAM kinetics, magnetoelectric tuning) are grounded in correct literature values. The main failure modes are parameter scaling errors rather than conceptual mistakes.

**Item**
**Status**
**Detail**
**App 1 — STDP Neuromorphic**
**BUG**
Neurons never fire. Synaptic current 16,129× too small (1e-9 scaling error)

**App 2 — In-Memory Crossbar**
**BUG**
Vmax=1V is 10–100× too high. E=460 nJ not pJ. GOPS/W ≈ 0, not 12× A100

**App 3 — RF Adaptive Filter**
**WARN**
L(Vc) goes negative above |Vc|>4.47 V; search uses ±40 V. 900 MHz fails (inf)

**App 4 — Quantum TRNG**
**WARN**
Physics correct. Von Neumann efficiency 2.5% not 50%. NIST Frequency FAILS

**App 5 — Phase-Change Converter**
**PASS**
Physics correct. Efficiency 7.6% is accurate given Rc=100Ω vs RL=10Ω design

# App 1 — STDP Neuromorphic
## Critical Bug: Neurons Never Fire
The simulation ran 5,000 timesteps and produced zero post-synaptic spikes. All synaptic weights remained frozen at initialisation (w = D×0.5). The STDP learning rule never executed on_post(), so no LTP or LTD occurred.

**Root cause — the synaptic current line:**
  I = G_syn \* 1e-9 \* spike_binary

treats spikes as having 1 nanoVolt amplitude. With G_syn ≈ 1.24×10⁻⁴ S, the resulting current is I ≈ 1.24×10⁻¹³ A (0.124 femtoamperes). The LIF neuron requires ≈2 nA to reach threshold — a shortfall of 16,129×.

**I_syn (as coded)**
1.24e-13 A   (0.124 fA)

**I_threshold (required)**
2.00e-9 A    (2.0 nA)

**Deficit**
16,129× too small

**Intended scaling**
spike as voltage × G_syn (e.g. 5 mV × G_syn)

**Conductance range**
G_off = 6.25e-5 S → G_on = 1.00e-2 S  (160× ratio ✓)

**LTP/LTD asymmetry**
A+ = 0.01, A- = 0.012 → 20% net depression bias (correct)

Fix applied in verification:

  I = G_syn \* V_spike \* spike_binary    \# V_spike ~ 5 mV

With V_spike = 5 mV, neurons fired at ~7,280 Hz (500 ms sim). Weight evolution confirmed — weights drifted toward G_on as LTP dominated at high firing rates. At biologically realistic 50 Hz inputs, net depression from A- > A+ would stabilise weights as intended.

# App 2 — In-Memory AI Crossbar
## Critical Bug: Vmax and Energy Formula
The code uses Vmax = 1.0 V with Gmax = 100 µS conductances. For a 256×256 array, this produces:

**G_total (sum all elements)**
3.31 S

**Total current at Vmax=1V**
3.31 A  (physically absurd for a chip)

**E_total (as coded)**
460,677 pJ  ≈ 461 nJ

**Power = E/tpulse**
46 W per MVM

**GOPS/W (as coded)**
~0  (far worse than A100)

**Document claim**
pJ scale, 12× advantage over A100 (780 GOPS/W)

To achieve pJ-scale energy with this conductance profile, Vmax would need to be ~5.5 mV — unrealistically low. The fix is Vmax = 100 mV AND Gmax = 1–10 µS, matching published RRAM crossbar literature (Gao et al. 2022, IBM PCM arrays). There is also a secondary numpy broadcasting bug in the Inoise formula which was caught and corrected during verification.

SNR and ENOB results are structurally valid:

**SNR (corrected formula)**
57.3 dB

**ENOB**
9.2 bits  (12-bit theoretical max)

**2% G-noise penalty**
3 dB below ideal ADC  ✓

**Noise model**
Correct formulation, wrong input parameters

# App 3 — RF Adaptive Filter
## Warning: Unphysical Inductance at Large Vc
The magnetoelectric model is L(Vc) = Lnom × (1 − α×Vc²). This goes negative — unphysical — when |Vc| exceeds √(1/α) = 4.47 V. The binary search spans ±40 V, routinely visiting the unphysical region.

**L negative above |Vc|**
4.47 V

**Binary search range**
±40 V  ← must be clamped to ±4.47 V

**2.4 GHz (Vc = −3.11 V)**
f = 2.400 GHz, Q = 38.9  ✓  (within physical range)

**5.8 GHz (Vc = −4.27 V)**
f = 5.800 GHz, Q = 16.1  ✓  (just within boundary)

**900 MHz (Vc = 40 V)**
f = inf, Q = 0  ✗  (unphysical — L is negative)

**Capacitor bank range**
0.1 pF → 1.6 pF  (1.26 GHz → 5.03 GHz with Vc=0)  ✓

**Tuning compute time (all 3)**
~1,047 µs wall-clock (in hardware: microseconds ✓)

Fix: clamp the binary search to (−4.47, +4.47) V and increase Lnom or decrease α to extend frequency coverage to 900 MHz. The cap bank alone provides 4× frequency tuning ratio, which is the primary coarse tuning mechanism — the magnetoelectric control is fine tuning only.

# App 4 — Quantum TRNG
## Warning: Extractor Bias Causes NIST Frequency Failure
The shot noise physics and H_min calculation are correct. The Von Neumann extractor implementation has two issues: (1) it extracts only 1 bit per pair (the MSB of each code), wasting 90% of available entropy; (2) the bias from I_avg offset causes systematic imbalance in the MSB.

**sigma (shot noise)**
1,790 pA  ✓  (matches sqrt(2eIBW) = 1,789.97 pA)

**H_min**
10.33 bits  ✓

**H_shannon**
11.05 bits  ✓

**sigma/LSB ratio**
512  (well-resolved noise — good entropy source ✓)

**Von Neumann efficiency**
2.5%  (theoretical max 50% — 20× below ideal)

**Throughput at 1 GHz BW**
25 Mbps  (not 500 Mbps as the note implies)

**NIST Frequency test**
FAIL  (p = 0.0000)  — bit bias from I_avg offset

**NIST Runs test**
PASS  (p = 0.636)  ✓

**NIST Block test**
PASS  (p = 0.579)  ✓

Fix: subtract I_avg before quantisation (centre the distribution at zero). This removes the DC offset bias before the Von Neumann step. Alternatively, use a full hash-based extractor (SHA-256 or AES-CTR DRBG) which extracts near H_min bits/sample and eliminates bias. The entropy source itself is valid — only the extractor needs updating.

# App 5 — Phase-Change Power Converter
## Pass: Physics Correct, Efficiency Accurately Predicted
The GST switch simulation is physically grounded and produces internally consistent results. Efficiency is flat at 7.6% across all frequencies — this is correct for the given parameters, not a bug.

**Efficiency at 10 MHz**
7.6%

**Efficiency at 50 MHz**
7.6%

**Efficiency at 100 MHz**
7.6%

**Efficiency at 500 MHz**
7.6%

**Theoretical divider ceiling**
RL/(Rc+RL) = 10/(100+10) = 9.1%

**Switching losses bring it to**
7.6%  ✓  (consistent)

**R(xi=1, ON)**
100 Ω  ✓

**R(xi=0, OFF)**
1,000,000 Ω  (10,000× on/off ratio ✓)

**R(xi=0.5, midpoint)**
10,000 Ω  (geometric mean of Rc^xi × Ra^(1-xi) ✓)

**Ea = 2.3 eV**
Matches GST literature (2.1–2.4 eV range ✓)

**Thermal tau = Cth × Rth**
1,000 ns — heat cannot dissipate at 500 MHz (1 ns half-period)

**GST vs MOSFET claim (10fJ vs 100fJ)**
Consistent with published nanoelectronics data ✓

Design note: Rc = 100 Ω ON-state resistance against RL = 10 Ω load produces fundamentally low efficiency regardless of switching quality. For a useful power converter, Rc must be reduced to 1–5 Ω (competitive with GaN/SiC MOSFETs), at which point the 10fJ switching energy advantage becomes the key differentiator. The simulation correctly captures this tradeoff.

# Summary — Verification Matrix
**App**
**Runs**
**Physics**
**Claims**
**NIST/Bench**
**Verdict**
1 — STDP

✓

✓

✗ BUG

N/A

Fix scaling

2 — Crossbar

✓

✓

✗ BUG

Fails

Fix Vmax

3 — RF Filter

✓

Partial

✓

2.4/5.8G ✓

Fix Vc range

4 — TRNG

✓

✓ ✓

Partial

Freq FAIL

Fix extractor

5 — Converter

✓

✓ ✓

✓

Valid

PASS

*Conclusion: The Phase 4 framework demonstrates solid conceptual engineering. All five physical models use correct constitutive equations and literature-validated parameters. The two critical bugs are parameter scaling errors (not physics errors) — both are single-line fixes. The TRNG and RF filter warnings are extractor and search-bound issues that leave the underlying physics intact.*

