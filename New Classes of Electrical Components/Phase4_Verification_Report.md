<!-- Converted from `Phase4_Verification_Report.docx` — source was Word (.docx). -->

__HYBRID COMPONENT SIMULATION — PHASE 4__

*Independent Verification Report*

February 2026  |  All 5 Application Engines Executed

# __Executive Summary__

All five Phase 4 application engines were executed in a live Python environment\. Physics formulas, benchmark claims, and algorithm correctness were independently verified\. Two critical bugs and two moderate issues were identified\. The core physics models \(shot noise, JKAM kinetics, magnetoelectric tuning\) are grounded in correct literature values\. The main failure modes are parameter scaling errors rather than conceptual mistakes\.

__Item__

__Status__

__Detail__

__App 1 — STDP Neuromorphic__

__BUG__

Neurons never fire\. Synaptic current 16,129× too small \(1e\-9 scaling error\)

__App 2 — In\-Memory Crossbar__

__BUG__

Vmax=1V is 10–100× too high\. E=460 nJ not pJ\. GOPS/W ≈ 0, not 12× A100

__App 3 — RF Adaptive Filter__

__WARN__

L\(Vc\) goes negative above |Vc|>4\.47 V; search uses ±40 V\. 900 MHz fails \(inf\)

__App 4 — Quantum TRNG__

__WARN__

Physics correct\. Von Neumann efficiency 2\.5% not 50%\. NIST Frequency FAILS

__App 5 — Phase\-Change Converter__

__PASS__

Physics correct\. Efficiency 7\.6% is accurate given Rc=100Ω vs RL=10Ω design

# __App 1 — STDP Neuromorphic__

## __Critical Bug: Neurons Never Fire__

The simulation ran 5,000 timesteps and produced zero post\-synaptic spikes\. All synaptic weights remained frozen at initialisation \(w = D×0\.5\)\. The STDP learning rule never executed on\_post\(\), so no LTP or LTD occurred\.

__Root cause — the synaptic current line:__

  I = G\_syn \* 1e\-9 \* spike\_binary

treats spikes as having 1 nanoVolt amplitude\. With G\_syn ≈ 1\.24×10⁻⁴ S, the resulting current is I ≈ 1\.24×10⁻¹³ A \(0\.124 femtoamperes\)\. The LIF neuron requires ≈2 nA to reach threshold — a shortfall of 16,129×\.

__I\_syn \(as coded\)__

1\.24e\-13 A   \(0\.124 fA\)

__I\_threshold \(required\)__

2\.00e\-9 A    \(2\.0 nA\)

__Deficit__

16,129× too small

__Intended scaling__

spike as voltage × G\_syn \(e\.g\. 5 mV × G\_syn\)

__Conductance range__

G\_off = 6\.25e\-5 S → G\_on = 1\.00e\-2 S  \(160× ratio ✓\)

__LTP/LTD asymmetry__

A\+ = 0\.01, A\- = 0\.012 → 20% net depression bias \(correct\)

Fix applied in verification:

  I = G\_syn \* V\_spike \* spike\_binary    \# V\_spike ~ 5 mV

With V\_spike = 5 mV, neurons fired at ~7,280 Hz \(500 ms sim\)\. Weight evolution confirmed — weights drifted toward G\_on as LTP dominated at high firing rates\. At biologically realistic 50 Hz inputs, net depression from A\- > A\+ would stabilise weights as intended\.

# __App 2 — In\-Memory AI Crossbar__

## __Critical Bug: Vmax and Energy Formula__

The code uses Vmax = 1\.0 V with Gmax = 100 µS conductances\. For a 256×256 array, this produces:

__G\_total \(sum all elements\)__

3\.31 S

__Total current at Vmax=1V__

3\.31 A  \(physically absurd for a chip\)

__E\_total \(as coded\)__

460,677 pJ  ≈ 461 nJ

__Power = E/tpulse__

46 W per MVM

__GOPS/W \(as coded\)__

~0  \(far worse than A100\)

__Document claim__

pJ scale, 12× advantage over A100 \(780 GOPS/W\)

To achieve pJ\-scale energy with this conductance profile, Vmax would need to be ~5\.5 mV — unrealistically low\. The fix is Vmax = 100 mV AND Gmax = 1–10 µS, matching published RRAM crossbar literature \(Gao et al\. 2022, IBM PCM arrays\)\. There is also a secondary numpy broadcasting bug in the Inoise formula which was caught and corrected during verification\.

SNR and ENOB results are structurally valid:

__SNR \(corrected formula\)__

57\.3 dB

__ENOB__

9\.2 bits  \(12\-bit theoretical max\)

__2% G\-noise penalty__

3 dB below ideal ADC  ✓

__Noise model__

Correct formulation, wrong input parameters

# __App 3 — RF Adaptive Filter__

## __Warning: Unphysical Inductance at Large Vc__

The magnetoelectric model is L\(Vc\) = Lnom × \(1 − α×Vc²\)\. This goes negative — unphysical — when |Vc| exceeds √\(1/α\) = 4\.47 V\. The binary search spans ±40 V, routinely visiting the unphysical region\.

__L negative above |Vc|__

4\.47 V

__Binary search range__

±40 V  ← must be clamped to ±4\.47 V

__2\.4 GHz \(Vc = −3\.11 V\)__

f = 2\.400 GHz, Q = 38\.9  ✓  \(within physical range\)

__5\.8 GHz \(Vc = −4\.27 V\)__

f = 5\.800 GHz, Q = 16\.1  ✓  \(just within boundary\)

__900 MHz \(Vc = 40 V\)__

f = inf, Q = 0  ✗  \(unphysical — L is negative\)

__Capacitor bank range__

0\.1 pF → 1\.6 pF  \(1\.26 GHz → 5\.03 GHz with Vc=0\)  ✓

__Tuning compute time \(all 3\)__

~1,047 µs wall\-clock \(in hardware: microseconds ✓\)

Fix: clamp the binary search to \(−4\.47, \+4\.47\) V and increase Lnom or decrease α to extend frequency coverage to 900 MHz\. The cap bank alone provides 4× frequency tuning ratio, which is the primary coarse tuning mechanism — the magnetoelectric control is fine tuning only\.

# __App 4 — Quantum TRNG__

## __Warning: Extractor Bias Causes NIST Frequency Failure__

The shot noise physics and H\_min calculation are correct\. The Von Neumann extractor implementation has two issues: \(1\) it extracts only 1 bit per pair \(the MSB of each code\), wasting 90% of available entropy; \(2\) the bias from I\_avg offset causes systematic imbalance in the MSB\.

__sigma \(shot noise\)__

1,790 pA  ✓  \(matches sqrt\(2eIBW\) = 1,789\.97 pA\)

__H\_min__

10\.33 bits  ✓

__H\_shannon__

11\.05 bits  ✓

__sigma/LSB ratio__

512  \(well\-resolved noise — good entropy source ✓\)

__Von Neumann efficiency__

2\.5%  \(theoretical max 50% — 20× below ideal\)

__Throughput at 1 GHz BW__

25 Mbps  \(not 500 Mbps as the note implies\)

__NIST Frequency test__

FAIL  \(p = 0\.0000\)  — bit bias from I\_avg offset

__NIST Runs test__

PASS  \(p = 0\.636\)  ✓

__NIST Block test__

PASS  \(p = 0\.579\)  ✓

Fix: subtract I\_avg before quantisation \(centre the distribution at zero\)\. This removes the DC offset bias before the Von Neumann step\. Alternatively, use a full hash\-based extractor \(SHA\-256 or AES\-CTR DRBG\) which extracts near H\_min bits/sample and eliminates bias\. The entropy source itself is valid — only the extractor needs updating\.

# __App 5 — Phase\-Change Power Converter__

## __Pass: Physics Correct, Efficiency Accurately Predicted__

The GST switch simulation is physically grounded and produces internally consistent results\. Efficiency is flat at 7\.6% across all frequencies — this is correct for the given parameters, not a bug\.

__Efficiency at 10 MHz__

7\.6%

__Efficiency at 50 MHz__

7\.6%

__Efficiency at 100 MHz__

7\.6%

__Efficiency at 500 MHz__

7\.6%

__Theoretical divider ceiling__

RL/\(Rc\+RL\) = 10/\(100\+10\) = 9\.1%

__Switching losses bring it to__

7\.6%  ✓  \(consistent\)

__R\(xi=1, ON\)__

100 Ω  ✓

__R\(xi=0, OFF\)__

1,000,000 Ω  \(10,000× on/off ratio ✓\)

__R\(xi=0\.5, midpoint\)__

10,000 Ω  \(geometric mean of Rc^xi × Ra^\(1\-xi\) ✓\)

__Ea = 2\.3 eV__

Matches GST literature \(2\.1–2\.4 eV range ✓\)

__Thermal tau = Cth × Rth__

1,000 ns — heat cannot dissipate at 500 MHz \(1 ns half\-period\)

__GST vs MOSFET claim \(10fJ vs 100fJ\)__

Consistent with published nanoelectronics data ✓

Design note: Rc = 100 Ω ON\-state resistance against RL = 10 Ω load produces fundamentally low efficiency regardless of switching quality\. For a useful power converter, Rc must be reduced to 1–5 Ω \(competitive with GaN/SiC MOSFETs\), at which point the 10fJ switching energy advantage becomes the key differentiator\. The simulation correctly captures this tradeoff\.

# __Summary — Verification Matrix__

__App__

__Runs__

__Physics__

__Claims__

__NIST/Bench__

__Verdict__

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

2\.4/5\.8G ✓

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

*Conclusion: The Phase 4 framework demonstrates solid conceptual engineering\. All five physical models use correct constitutive equations and literature\-validated parameters\. The two critical bugs are parameter scaling errors \(not physics errors\) — both are single\-line fixes\. The TRNG and RF filter warnings are extractor and search\-bound issues that leave the underlying physics intact\.*

