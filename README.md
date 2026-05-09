# Ideas — Odin Loch's R&D shelf

> **Forty-five folders. Each is a small, self-contained research project written in the register of an internal R&D document — long-form prose, mathematical detail, working code where the topic admits it, and explicit honesty about what is built, what is modelled, and what is speculative.** The shelf spans cryptography (a custom AEAD with receiver-recomputable nonces; an applied protocol suite turning a shared pseudo-random stream into a `48 MB`-saving Bloom-filter coordination primitive on `N = 10⁶`); neural architectures (a parity-validated production stack, a non-attention sequence model with full architecture-search programme, a long-context unified hash-predictive memory reporting `289×` query-latency speedup vs full attention at `100 K` tokens); statistical and mathematical algorithms (a sub-millisecond neural-heuristic scheduler with formal `O(d√T·polylog T)` regret, a deterministic statistical generator claiming `~90 %` of neural perplexity at `O(N)` training cost, an empirical scale-dependent meta-pattern theory of primes); a multi-target tracker that *fixes a known bug* in the standard heavy-tailed JPDA recipe and reports a `51.6 %` mean GOSPA improvement; hardware and materials specifications (a Verilog-orchestrated `1 Hz – 14 GHz` `100 W` noise platform, a Rockwell-65–70 carbide tooling platform with a forge-to-machine supply chain dropping `40–45 %` of cost); physics, quantum, and biomedical work (non-local field theory, NV-centre quantum-diamond programme with explicit barrier accounting, a two-tier neural-quantum-dust biomedical interface that closes a `~6 nW` power budget on FDA-compliant ultrasound at `MI ~ 0.4`); economics, civics, and a smaller creative layer (an energy-resource macroeconomic model that issues currency at `k · TNW` against megajoule-denominated wealth, an eight-paper sovereign-doctrine series, a hemp-anchored cosmeceutical white paper, a botanical-OS bar-operations system). Most folders ship at least one long-form research document; many ship working code; speculative items are *banner-flagged* in their own README. Read it as a portfolio of how-to-think-about-this-problem documents, not a product catalogue.

---

## ⚖️ Licensing

Dual-licensed:

1. **GNU Affero General Public License v3.0+ (AGPL-3.0+)** — free tier for personal use, charity, education, and entities with annual income < AUD 50 000.
2. **Tiered commercial licence** — for commercial use above the free-tier threshold.

See [`modified-license.md`](modified-license.md) for full terms and [`dual-license-setup.md`](dual-license-setup.md) for setup notes.

**Attribution under AGPL-3.0+:**

> "Powered by Ideas, developed by Odin Loch. Licensed under AGPL-3.0+."

Modifications must be shared back under the same dual-licence; research using this software must be open-sourced. Commercial licensees: no requirement to share modifications.

**Commercial enquiries:** odin.loch@outlook.com.au

---

## 🗂 How to navigate

The repository is organised as one folder per topic, browsable in any order. Each folder has its own README that describes what the folder actually contains, lists the source documents, and links related work elsewhere in the repo.

You can read this index six ways:

1. **Selected highlights** ([§ Selected highlights](#-selected-highlights)) — the headline claim from each strongly-evidenced folder, in one place.
2. **Reading paths** ([§ Reading paths](#-reading-paths)) — curated entry sequences for specific interests.
3. **By category** ([§ Categories](#-categories)) — six themed groupings, each with a short essay above the table.
4. **A–Z** ([§ A–Z folder index](#-az-folder-index)) — alphabetical with one-line descriptions.
5. **Navigation aids** ([§ Quick links](#-quick-links)) — repo-level files (audit trail, licence, etc.).
6. **Acronym key** ([§ Acronym key](#-acronym-key)) — every named system in one alphabetised glossary.

---

## ⭐ Selected highlights

A short tour of the strongest individual claims in the shelf, with the folder that backs each one. None of these are throwaway lines: each is the headline number from a long-form research paper inside the named folder.

- **`51.6 %` mean GOSPA improvement** on a four-scenario multi-target benchmark by *fixing a known bug* in the standard heavy-tailed JPDA recipe — peaks at `72.8 %` on one scenario. → [`Filtering/`](Filtering/)
- **`289 ×` query-latency speedup** vs full self-attention at `100 K` tokens (`8.1 ms` vs `2 340 ms`), with `744 ×` memory reduction, by unifying LSH memory and predictive coding under one free-energy functional. → [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/)
- **`~28 ms` median scan latency** for a multi-target tracker fusing PMBM + three rendezvous predictors + eight tradecraft detectors + Dempster–Shafer fusion in one Python module on a single CPU core. → [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/)
- **`p50 0.48 ms`** placement latency at **Jain fairness `1.00`** for a distributed scheduler with formal `O(d√T·polylog T)` regret on its exploration layer. → [`Statistical Scheduler/`](Statistical%20Scheduler/)
- **`~90 %` of state-of-the-art neural perplexity** on long-context tasks at `O(N)` training cost, deterministic, with audit trails. → [`Statistical Generation/`](Statistical%20Generation/)
- **`221` parity tests** keeping a Python research reference and a CMake-built C++ native core *byte-identically* equivalent across 13+ named fixtures. → [`Cypha/`](Cypha/)
- **`48 MB` of message overhead saved** at `N = 10⁶` by replacing 384-bits-per-element Bloom-filter coordination with shared-PRF coordination. → [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/)
- **`AND` is the only nontrivial operation forming a ring with `XOR` over GF(2)** — a uniqueness theorem from an exhaustive computer-verified taxonomy of all 16 binary operations. → [`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/)
- **Five welding regimes from `2-min / 77 %` battlefield repair to `2.3-h / 99 %` aerospace-certifiable bonds** on the same chemistry / electrode set / control logic, at `1 – 2` orders of magnitude lower equipment cost than vacuum diffusion welding. → [`Diffusion Welding/`](Diffusion%20Welding/)
- **`40 – 45 %` cost reduction and `65 – 70 %` lead-time reduction** on a Rockwell-65 carbide insert via a forge-to-machine supply chain, on top of a five-layer coating with `42 – 46 GPa` hardness core. → [`Rockwell 50 to 70 Carbide/`](Rockwell%2050%20to%2070%20Carbide/)
- **`4.92 ×`, `386 ×`, `> 10⁶/s`** measured Python speedups by refactoring Babbage's Difference Engine, the Antikythera Mechanism, and the WWII Torpedo Data Computer into modern algorithms. → [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/)
- **`~6 nW` power budget closes** on FDA-compliant ultrasound (`MI ~ 0.4` vs limit `0.7`) for a two-tier neural-quantum-dust biomedical interface with `~2 – 3 nT/√Hz` magnetometry. → [`Neural Dust/`](Neural%20Dust/)
- **`Total_currency = k · TNW` with `k = 0.85`** — currency issuance pinned to physical-energy-content-of-the-nation rather than monetary aggregates. → [`Economics/`](Economics/)
- **An eight-paper sovereign doctrine** with `≤ 10`-warhead minimal deterrence, `AUD 100M` personal wealth ceiling, every claim referenced. → [`UCN Political System/`](UCN%20Political%20System/)

---

## 🧭 Reading paths

The shelf is large. These curated sequences each build a coherent thread.

### "I do machine learning research"
[`NN Shortcuts/`](NN%20Shortcuts/) (acceleration framework) → [`Cell AI/`](Cell%20AI/) (alternative architecture with honest failure log) → [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) (long-context unification) → [`Statistical Generation/`](Statistical%20Generation/) (deterministic-stats alternative to neural LLMs) → [`Veritas/`](Veritas/) (proof-trace learning) → [`Compression Algorithms/`](Compression%20Algorithms/) (NMP `α ≈ 0.851 ± 0.122` spectral-exponent theory) → [`Cypha/`](Cypha/) (production engineering of an HRNA stack).

### "I do cryptography or distributed systems"
[`Compression Algorithms/`](Compression%20Algorithms/) (Izaac meta-theorem) → [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) (twelve applied protocols) → [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) (receiver-recomputable nonces) → [`RNGS/`](RNGS/) (four-family RNG portfolio) → [`Veritas/`](Veritas/) (verification framework).

### "I do tracking, filtering, or sensor fusion"
[`Filtering/`](Filtering/) (GH-SR-IMM with the GH-JPDA bug fix) → [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) (full PMBM + tradecraft + threat-scoring engine) → [`Statistical Scheduler/`](Statistical%20Scheduler/) (LinTS / PID / CFS sister stack) → [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) (noise-aware classical post-processing).

### "I do hardware or materials engineering"
[`Rockwell 50 to 70 Carbide/`](Rockwell%2050%20to%2070%20Carbide/) (tooling + supply chain) → [`Diffusion Welding/`](Diffusion%20Welding/) (UCDW five regimes) → [`100W Wideband Noise Generator/`](100W%20Wideband%20Noise%20Generator/) (Verilog-as-spec) → [`New Classes of Electrical Components/`](New%20Classes%20of%20Electrical%20Components/) (four-tier device catalogue + simulator) → [`CPU/`](CPU/) (HW-accelerated OS primitives).

### "I do mathematics for its own sake"
[`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/) (uniqueness theorem + permutation polynomials + ANF gate counts) → [`General Math Papers/`](General%20Math%20Papers/) (LCRP meta-principle) → [`3 to 8 Value Boolean Algebra/`](3%20to%208%20Value%20Boolean%20Algebra/) (dimensional emergence) → [`Prime Number Generator/`](Prime%20Number%20Generator/) (scale-dependent meta-pattern theory) → [`Math Question Generator/`](Math%20Question%20Generator/) (curriculum generation at scale).

### "I do physics, quantum, or biomedical"
[`Physics/`](Physics/) (NLFGN-UFT + superluminal recession) → [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) (QDMP + barrier inventory) → [`Diamond Batterys/`](Diamond%20Batterys/) (radioisotope power architectures) → [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) (classical QAOA pipeline) → [`Neural Dust/`](Neural%20Dust/) (NV-centre biomedical interface) → [`GM Enhancements/`](GM%20Enhancements/) (HSA v4.0 protocol).

### "I do policy, economics, or worldbuilding"
[`Economics/`](Economics/) (EREM in megajoules) → [`UCN Political System/`](UCN%20Political%20System/) (eight-paper doctrine series) → [`UCN AIs/`](UCN%20AIs/) (in-universe AI families) → [`Weapons/`](Weapons/) (defence-tech portfolio in operator-document register).

---

## 📚 Categories

### 🤖 Algorithms, learning, and artificial intelligence

The shelf's largest category. Two strands run through it: (1) genuinely-new sequence-modelling architectures that are honest about not yet competing with transformer baselines on perplexity, and (2) classical-statistics algorithms whose advantage is *interpretability* — formal regret bounds, parity-validated native code, explicit uncertainty propagation. Read this category if you want to see how a research programme on alternatives to attention actually progresses (with documented failures, not just successes), or if you want sub-millisecond schedulers and multi-target trackers that you can audit step by step.

| Folder | Description |
|---|---|
| [`Cell AI/`](Cell%20AI/) | A biology-motivated sequence-modelling architecture (CellularAI) — replaces self-attention with reaction-diffusion partition dynamics, online Hebbian plasticity *during the forward pass*, and a 27-experiment architecture-search programme. Best run reports macro-perplexity `246.6` (`966 000 ×` over E0); honest that v1 doesn't approach transformer perplexity on real corpora. |
| [`Cypha/`](Cypha/) | A neural-network inference and training stack (Harmonic Recursive Neural Architecture). Python reference + CMake-built C++ native core + REST server + Qt desktop Studio. **`188` pytest + `33` CTest** parity tests verify Python and native produce *byte-identical* outputs across 13+ named fixtures. |
| [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) | Unified Hash-Predictive Memory — fuses LSH-based memory and hierarchical predictive coding under one free-energy functional. **`289 ×` query-latency speedup** vs full attention at `100 K` tokens (`8.1 ms` vs `2 340 ms`); **`744 ×` memory reduction**. |
| [`Neural Decompiler/`](Neural%20Decompiler/) | Assembly-to-source as conditional sequence modelling. Encoder–decoder Transformer + hierarchical memory + load-balanced mixture-of-experts (binary-focused vs language-focused). Coherent trainable architecture, not a state-of-the-art recovery system. |
| [`NN Shortcuts/`](NN%20Shortcuts/) | A unifying framework for neural-network acceleration. The Streaming Geometry Framework reduces `16` known acceleration techniques to one principle (Incremental Riemannian Estimation); the Algebraic Autopsy decomposes a trained network into tropical + Grassmannian + `11 %` dense `(ℝ, +, ×)` content. |
| [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) | A single-file, edge-deployable multi-target tracker and tactical-intelligence engine (ARIA-INTEL). PMBM random-finite-set tracking + three rendezvous predictors + eight tradecraft detectors + Dempster–Shafer fusion, running at **`~28 ms` median scan latency** on a single CPU core. |
| [`Filtering/`](Filtering/) | A heavy-tailed multi-target tracker (GH-SR-IMM). The distinguishing feature is a **GH-JPDA extension that fixes a known bug** in the standard recipe (use the GH posterior covariance inside a Gaussian association likelihood, *not* the GH likelihood directly): mean **`51.6 %` GOSPA improvement** across four scenarios, peaking at `72.8 %`. |
| [`Statistical Scheduler/`](Statistical%20Scheduler/) | A neural-heuristic distributed task scheduler. CFS-style fair-share scoring + Linear Thompson Sampling exploration in 24-D context + PID-controlled stability override + full statistical monitoring stack. **`p50 0.48 ms`** placement latency, **Jain fairness `1.00`**, formal `O(d√T·polylog T)` regret. |
| [`Statistical Generation/`](Statistical%20Generation/) | The Universal Statistical Generator — a deterministic, interpretable, classical-statistics framework claiming **`~90 %`** of state-of-the-art neural perplexity on long-context tasks at **`O(N)`** training cost. Built on category theory + Lévy triplets + SHA-256 hash compression to `M = 2³²` states. |
| [`VDJ Inspired Algorithm/`](VDJ%20Inspired%20Algorithm/) | Combinatorial pattern recognition derived from V(D)J recombination in the vertebrate immune system. Five primary modules + seven subsystems, all communicating through a typed `Pattern` dataclass. **`~13 ms` at `n = 16, r = 5`** with a `< 1 MB` peak memory footprint. CPU-only. |
| [`Fungal Network Algorithm/`](Fungal%20Network%20Algorithm/) | Pattern recognition through physical network reorganisation, modelled on how fungi search for food without central control. The topology *itself* is the long-term memory; weights and edges are consequences of input history. |
| [`Ashby Optimiser/`](Ashby%20Optimiser/) | Multi-scale homeostatic optimisation — W. Ross Ashby's 1948 homeostat reframed as a black-box optimiser with parallel search units at geometrically-spaced radii. On Rastrigin dim 10 with 500 evals, multi-scale ends at median error **`0.002` vs single-scale `74.7`**. |
| [`UCN AIs/`](UCN%20AIs/) | Speculative AI families in the United Commonwealth Nations worldbuilding setting. Two flagship classes (Any Purpose Network and General Purpose Network), one signal-processing class, and two foundational learning primitives. In-universe technical writing, not built systems. |

### 🔐 Cryptography, verification, and randomness

A category that takes "shared structure as a primitive" seriously. The Izaac thread argues that a *shared deterministic pseudo-random stream* is itself a coordination primitive worth treating as a first-class infrastructure component — and turns it into a `< 2000`-LOC reference implementation of twelve protocols that save measurable bytes-on-wire vs PBFT, HotStuff, and standard Bloom-filter constructions. The ARIA encryption design rejects the AES-GCM / ChaCha20-Poly1305 nonce-management orthodoxy by making nonces structurally non-transmissible. The Veritas thread asks the orthogonal question: what does an ML system that produces *proof traces* alongside loss curves look like? The randomness portfolio takes its quality seriously enough to ship four genuinely different generator families with explicit threat models, not one "default" RNG.

| Folder | Description |
|---|---|
| [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) | A custom authenticated-encryption-with-associated-data scheme (Algebraic Resynchronisation and Integrity Architecture, ARIA) whose nonces are **never transmitted** — receiver re-derives them from the message and a session key, structurally eliminating loss-of-nonce-sync. Three-layer algebraic tower over `GF(2²⁵⁶)` + Meta-DAG RNG entropy pump + dual collision bounds. *Not* the Korean ARIA block cipher. |
| [`Break AES/`](Break%20AES/) | Research scaffolding combining a Transformer student + Llama-teacher knowledge distillation + policy-gradient reinforcement learning with a BLEU-shaped reward — framed as a training stack one might point at AES cryptanalysis. **Not an AES break.** Python skeleton + informal proof-sketch note. |
| [`Compression Algorithms/`](Compression%20Algorithms/) | Canonical home of three frameworks: **Izaac** (shared-PRF coordination → free broadcast channel), **GRIA** (graded reversibility coordinate `α(f) = 1 − H(f(X))/H(X)` with bifurcation at `α = 0.5`, `J ≤ 0.951` upper bound), and **NMP** (Nonlinear Matrix Pruning; `α ≈ 0.851 ± 0.122` measured spectral exponent on neural weight matrices). |
| [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) | Twelve concrete protocols operationalising the Izaac meta-theorem. **Bloom filter coordinated by an Izaac shared seed saves `N × 384` bits of message overhead** — for `N = 10⁶`, that is `48 MB` moved off-wire per coordination round. |
| [`Veritas/`](Veritas/) | A verification-enabled learning architecture in which the artefact produced is not loss curves but proof traces. Every learner emits PAC, mistake-bound, meta-learning, and composition certificates. Worked example: function class `\|H\| = 2^(2⁸) = 2²⁵⁶`, sample bound at `ε = δ = 0.01` is `~1.8 × 10⁶` — proven, not hoped. |
| [`RNGS/`](RNGS/) | Four genuinely different pseudo-random generator families: OTB-LCG (Boolean / transcendental + SHA-256 post-processing), SynerChaos v2 (`~80 cycles/output` on Cortex-M4), Meta-DAG RNG (`≥ 2¹⁵³⁶ × 40320` state-space lower bound), Turbulent Flow (`χ² p = 0.582`, avalanche pass rate `> 0.999`). |

### 📐 Mathematics, algebra, and number theory

This category groups documents that work *inside* mathematics rather than applying it. The Boolean-function dimensional analysis traces how the fraction of "truly `n`-dimensional" (irreducible, non-decomposable) functions rises from `~93.8 %` at `n = 3` to `~99.9 %` at `n = 8` — and what that implies for error-correcting codes and Byzantine N-modular redundancy. The GF(2) sweep proves a non-obvious uniqueness theorem (AND is the *only* nontrivial operation that forms a ring with XOR over GF(2)). The LCRP paper does taxonomy: it documents *when* the `O(n²) → O(n log n)` divide-and-conquer pattern applies and when it doesn't (NP-hard problems, Ω(n) input lower bound, problems with strict super-`O(n log n)` lower bounds).

| Folder | Description |
|---|---|
| [`3 to 8 Value Boolean Algebra/`](3%20to%208%20Value%20Boolean%20Algebra/) | Dimension-by-dimension narrative of the full Boolean function spaces `f : {0,1}ⁿ → {0,1}` for `n = 3 – 8` — exact at small `n` (`256` at `n = 3`, `65 536` at `n = 4`), sampled at large `n` (`2²⁵⁶ ≈ 1.16 × 10⁷⁷` at `n = 8`). Threaded through to error-correcting codes, Byzantine NMR, AES-S-box-style nonlinearity. |
| [`General Math Papers/`](General%20Math%20Papers/) | The Logarithmic Complexity Reduction Principle (LCRP) — a meta-principle, not a theorem, that documents the recurring pattern by which naively `Ω(n²)` problems admit `O(n log n)` algorithms via divide-and-conquer or `O(log n)`-per-element data structures. Master Theorem case analysis as the decision procedure. |
| [`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/) | A seven-paper sweep starting with an exhaustive computer-verified taxonomy of all 16 binary operations on `{0, 1}`. Proves: **AND is the *only* nontrivial operation forming a ring with XOR over GF(2)**. Extends to AES-inverse permutation polynomials (`x⁻¹ = x²⁵⁴` is `1 of 128` permutations on `GF(2⁸)`), gate-count benchmarks (Rule 110: `19 → 6` gates, `68 %` reduction), and Differentiable Logic Gate Networks. |
| [`Math Question Generator/`](Math%20Question%20Generator/) | MegaMathGen — a multi-thousand-line generator for curriculum-grade math problems across the full mathematics-classification taxonomy. SymPy + NumPy + 1000-decimal-place precision arithmetic, `28 GB` memory cap, checkpointing. Paired with a 13-domain landscape survey anchored to MSC2020. |
| [`Prime Number Generator/`](Prime%20Number%20Generator/) | An empirical scale-dependent meta-pattern theory of primes. Local divisibility / 6k±1 effects and global PNT-style gap heuristics make different scale-dependent contributions, crossing over at **`n* ≈ 836` (`s* = log₁₀ n ≈ 2.92`)** under a fitted `α(s) = s^(−0.37)` law. |

### 🔩 Hardware, materials, and process engineering

The hardware category mixes *deliverable* engineering specifications (the carbide tooling platform with measured cost reductions and a forge-to-machine supply chain), *runnable* HDL artefacts (the noise-generator Verilog file is the spec), *historical re-examinations* (Babbage's Difference Engine, the Antikythera Mechanism, and the WWII Torpedo Data Computer refactored into modern Python with measured `4.92 ×`, `386 ×`, and `> 10⁶/s` benchmarks), and *speculative* design conversations (a "future C++", radioisotope diamond batteries scaling from kW to GW). Every folder makes its own register clear.

| Folder | Description |
|---|---|
| [`100W Wideband Noise Generator/`](100W%20Wideband%20Noise%20Generator/) | A single SystemVerilog file orchestrating a Chua-circuit chaotic analogue core, four-band RF power-amplifier chain, 12-bit programmable supply DAC, eight-channel thermal ADC, and hard-protection state machine. Banner targets: **`1 Hz – 14 GHz`** (hardware-dependent), **`100 W`** continuous output, sub-microsecond fault response. |
| [`CPU/`](CPU/) | A heterogeneous many-core CPU design conversation paired with a SystemVerilog sketch of an `os_accelerator` whose inner `hardware_bios` state machine runs `POWER_ON_SELF_TEST → HARDWARE_INIT → MEMORY_TEST → BOOT_SEQUENCE → SYSTEM_INIT → OS_HANDOFF`. **`16` big OOO cores at 4 GHz + `4 096` small cores**, MOESI cache coherence, hardware-accelerated syscalls. Not buildable as written. |
| [`Diamond Batterys/`](Diamond%20Batterys/) | An eight-model taxonomy (Series A – D) of radioisotope diamond batteries from the demonstrated `~kW`-class Bristol/UKAEA C-14 baseline (Dec 2024) up to `GW`-class Cm-244 / Am-242m / U-235 subcritical concepts. Engineering-fiction-grade; explicitly hypothetical at the top of the document. |
| [`Diffusion Welding/`](Diffusion%20Welding/) | Ultra-Compact Diffusion Welding (UCDW) — a five-regime tradespace from **`2-min / 77 %`-strength** battlefield repairs to **`2.3-hour / 99 %`-strength** aerospace-certifiable bonds, on the same chemistry / electrode set / control logic. Equipment cost `$8K – $50K` vs incumbent vacuum diffusion welding's `$500K – $2M`. |
| [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/) | Three historical computing machines refactored into modern Python with measured benchmarks: **Babbage Difference Engine `4.92 ×` speedup**, **Antikythera Fourier reconstruction `386 ×` speedup**, **digital Torpedo Data Computer `> 10⁶ solutions/s` at `±0.015°`**. |
| [`Future C++/`](Future%20C++/) | A long design-conversation transcript exploring what a "modern compiled language with C++ syntax" might look like — borrow-checking from Rust, async/await + green threads, software-transactional memory, richer generics + ADTs + pattern matching. No compiler, no grammar, no benchmarks. |
| [`New Classes of Electrical Components/`](New%20Classes%20of%20Electrical%20Components/) | A four-tier catalogue of `≥ 21` discrete-continuous hybrid passive devices, paired with a five-phase Python simulation programme. Headline simulator claims: **`2.34 × 10⁹` fused solves/s on RTX 3090**, **`526 ×` adjoint-method inverse-design speedup**. |
| [`Rockwell 50 to 70 Carbide/`](Rockwell%2050%20to%2070%20Carbide/) | A complete carbide-tooling platform for hard-machining steels `HRC 40 – 70` — HX-70 GradePlex functionally-graded WC-Co substrate (`2050 – 2100 HV30` working surface), TriboshieldPlus 5-layer coating (`42 – 46 GPa` hardness core, `µ < 0.15`), and a forge-to-machine supply chain that drops `40 – 45 %` of cost and `65 – 70 %` of lead time. |

### 🌌 Physics, quantum systems, and biomedical engineering

A category dominated by *barrier accounting*. The Quantum Diamond Wafer programme pairs an aspirational room-temperature quantum-computing substrate with an explicit **seven-barrier** inventory (coherence leap of `~10⁴ ×`, nm-deterministic NV placement vs `~20 nm` lateral best, no diamond precedent for proposed topological mechanism, etc.) — and a fact-vs-fiction ledger separating real industrial CVD scaling from science fiction. The Neural Dust programme similarly opens by *deleting* unsupported claims from the original specification (no `20 nm` general compute, no thermoelectric bio-power at scale, no entanglement comms) and replacing them with a tight `~6 nW` power budget that *closes*. The Drugs and GM Enhancements folders tier their content explicitly into Verified / Plausible / Speculative.

| Folder | Description |
|---|---|
| [`Physics/`](Physics/) | Two distinct foundations papers. **NLFGN-UFT** (Non-Local Field-Gravity Network Unified Field Theory) — a non-local network-augmented gravity story with explicit advanced + retarded kernels and the structural claim **`v_field ≤ c`** (distinct from "instantaneous Newton" folklore). **Superluminal Recession** — argues that apparent FTL galaxy recession (`v_rec > c` at `z ≈ 1.46`, CMB at `~3.2 c` today) exposes a real interpretational split between rigorous GR-based positions, not a failed ΛCDM fit. |
| [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) | An aspirational CVD-grown Quantum Diamond Metamaterial Processor (QDMP) — paired with a sober companion paper arguing near-term wins live in sensors / hybrid memory / QKD nodes, not room-temperature processors. Targets `T₂ > 100 s` at room temperature (`~10⁴ ×` over `~3 ms` current); seven barriers explicitly enumerated; fact-vs-fiction ledger. |
| [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) | A fully-classical, quantum-shaped graph-optimisation pipeline. Five layers — spectral Laplacian compression → Chebyshev coefficient encoding → small exact (or mean-field) QAOA simulation → noise-norm-weighted shot ranking → spectral lift-back — with verification functions for each. No hardware, no quantum-advantage claim. |
| [`Neural Dust/`](Neural%20Dust/) | Neural Quantum Dust (NQD), a two-tier neural-interface architecture: `150 – 250 nm` NV-nanodiamond quantum sensors + `80 – 150 µm` ultrasound-powered CMOS motes. Closes a **`~6 nW`** power budget on FDA-compliant ultrasound (`MI ~ 0.4` vs limit `0.7`), with `~2 – 3 nT/√Hz` magnetometry. **`15 – 25 year`** programme, every component tagged Verified / Plausible / Speculative. |
| [`GM Enhancements/`](GM%20Enhancements/) | Homo Sapiens Augmentus (HSA) v4.0 — a three-phase **`24 – 34 month`** speculative genetic-modification protocol fusing AAV / LNP / lentiviral delivery, CRISPRa/i + base + prime editing, OSK partial reprogramming, senolytics, and organ-bioprinting. Published with **`~20 – 32 %`** cumulative SAE risk table. **Worldbuilding-purposes-only** banner. |
| [`Drugs/`](Drugs/) | A split-personality folder. *Industrial* pharmaceutics playbooks (Universal Depot framework with PLGA tuning bands, sugar-excipient review, Poloxamer / ISFD recipes) live alongside *speculative* monographs (`COGNIMAX-PRO`, `NeuroBridge-7`, `MetaMax-2034` and other `Meta*` agents). Every speculative compound is banner-flagged. **Not medical, legal, or tactical advice.** |

### 💰 Economics, civics, defence, and creative engineering

The economics and civics work stakes a single position: **wealth, currency, and policy should be denominated in physically-meaningful units, not in self-referential monetary aggregates.** The EREM measures wealth in megajoules; the UCN doctrine series builds a polity around that measurement with hard sovereignty economics, a `≤ 10`-warhead minimal-deterrence posture, an `AUD 100M` personal wealth ceiling, and a closing roadmap that explicitly acknowledges the proposal would need referenda and international consent it does not have. The defence and creative folders apply the same engineering register downward: brochure-credible specification numbers, paired specs / papers, and explicit illustrative-banner labelling on the hypothetical items.

| Folder | Description |
|---|---|
| [`Economics/`](Economics/) | The Energy-Resource Economic Model (EREM) — measures national wealth in **megajoules of Total National Wealth (TNW)** rather than GDP, issues currency at **`Total_currency = k · TNW`** with `k = 0.85` (`15 %` measurement buffer), defines exchange rate as the directly-comparable per-capita TNW ratio. Theoretical / v1.0; asks for empirical validation. |
| [`UCN Political System/`](UCN%20Political%20System/) | The eight-paper United Commonwealth Nations doctrine series — modular Westminster++ governance, hard-sovereignty economics, `≤ 10`-warhead minimal nuclear deterrent, `AUD 100M` personal wealth ceiling, government-manufactured pharma-grade recreational drugs, optional UK – Canada – Australia Crown confederation. Speculative; every claim is referenced. |
| [`Battle Sim/`](Battle%20Sim/) | A survey-and-design note that maps the modern mathematical-modelling landscape for combat — Hughes salvo equations, extended Lanchester, Markov battle-state chains, FATHM linear programming, Dupuy / TNDM combat-power lineage — into one comparative reading map. **Explicitly not an operational simulator.** |
| [`Weapons/`](Weapons/) | A defence-engineering R&D portfolio with paired operator-spec-sheets and TRP-numbered research papers across small-arms (`MP-6.8`, `MAS-15.2E`), heavy weapons (`57mm` autocannon, `140mm` tank round), body armour (APES, AlNiCyN, OBSIDIAN family), CBRN protection (NACS), tactical acoustic cancellation (TACS at `35 – 55 dB` depth), and CL-20 high explosive. Classification banners are stylistic. |
| [`Beauty Products/`](Beauty%20Products/) | A fully-architected cosmeceutical white paper for a hemp-anchored luxury body lotion — `3 : 1` omega-6 : omega-3 hempseed-oil base, Tremella-snow-mushroom humectant (`~500 ×` water-holding capacity), prickly-pear / sea-buckthorn / Centella `0.2 %` asiaticoside active stack, `pH 4.8 – 5.5`, all-natural `3 %` Phase-D preservative system. Fully cited. |
| [`Cocktails/`](Cocktails/) | A bar-operations system treated as a product platform — four native-Australian-botanical bases driving every infusion / syrup / tincture / bitters across four signature series with parallel zero-proof mirrors, two complete bitters fabrication specs, a `2-hour` mushroom stock + `4-hour` fat-wash protocol, and a shift / day / week / month prep workflow. |

---

## 🔤 A–Z folder index

| Folder | One-line description |
|---|---|
| [`100W Wideband Noise Generator/`](100W%20Wideband%20Noise%20Generator/) | Chua-circuit RF noise generator (Verilog) — 1 Hz – 14 GHz, 100 W |
| [`3 to 8 Value Boolean Algebra/`](3%20to%208%20Value%20Boolean%20Algebra/) | Boolean function spaces for n = 3..8 *variables* |
| [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) | Custom AEAD over GF(2²⁵⁶) (NOT the Korean cipher) |
| [`Ashby Optimiser/`](Ashby%20Optimiser/) | Multi-scale homeostatic optimiser (W. Ross Ashby) |
| [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) | ARIA-INTEL — edge-deployable PMBM intelligence engine |
| [`Battle Sim/`](Battle%20Sim/) | Battle simulation design document |
| [`Beauty Products/`](Beauty%20Products/) | Hemp Harmony luxury body lotion — formulation white paper |
| [`Break AES/`](Break%20AES/) | Transformer + RL distillation for AES cryptanalysis |
| [`Cell AI/`](Cell%20AI/) | CellularAI — biologically-inspired non-attention sequence modelling |
| [`Cocktails/`](Cocktails/) | Bar operations as a structured design problem |
| [`Compression Algorithms/`](Compression%20Algorithms/) | Izaac, GRIA, NMP — canonical Izaac home |
| [`CPU/`](CPU/) | SystemVerilog hardware OS-acceleration block |
| [`Cypha/`](Cypha/) | HRNA inference + training + tooling (Python + native C++ + REST + GUI) |
| [`Diamond Batterys/`](Diamond%20Batterys/) | Hypothetical radioisotope diamond batteries (Series A–D) |
| [`Diffusion Welding/`](Diffusion%20Welding/) | UCDW — five-regime electrochemical/thermal/ultrasonic bonding |
| [`docs/`](docs/) | Static-site assets (`index.html`, CSS, generated `site/` mirror) and `EDITORIAL_STYLE.md` |
| [`Drugs/`](Drugs/) | Universal Depot Systems + Nootropics + Schizophrenia Cure (speculative) |
| [`Economics/`](Economics/) | EREM — Energy-Resource Economic Model |
| [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/) | Babbage / Antikythera / TDC algorithm rebuilds |
| [`Filtering/`](Filtering/) | GH-SR-IMM robust multi-target tracking |
| [`Fungal Network Algorithm/`](Fungal%20Network%20Algorithm/) | Bio-inspired self-organising network (topology = memory) |
| [`Future C++/`](Future%20C++/) | Managed-language design conversation |
| [`General Math Papers/`](General%20Math%20Papers/) | LCRP — Logarithmic Complexity Reduction Principle |
| [`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/) | GF(2) ring theorems, operator taxonomy, GRIA spectrum |
| [`GM Enhancements/`](GM%20Enhancements/) | HSA v4.0 enhancement protocol |
| [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) | Applied Izaac protocols (compression, consensus, VRFs) |
| [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) | UHPM — Unified Hash-Predictive Memory |
| [`Math Question Generator/`](Math%20Question%20Generator/) | MegaMathGen + 13-domain mathematics survey |
| [`Neural Decompiler/`](Neural%20Decompiler/) | Assembly → source seq2seq with hierarchical memory + MoE |
| [`Neural Dust/`](Neural%20Dust/) | NQD — Neural Quantum Dust two-tier architecture |
| [`New Classes of Electrical Components/`](New%20Classes%20of%20Electrical%20Components/) | 3-tier hybrid passive-device catalogue + 5-phase simulation |
| [`NN Shortcuts/`](NN%20Shortcuts/) | Efficient neural-network shortcuts |
| [`Physics/`](Physics/) | Non-local gravity + NLFGN UFT + superluminal recession |
| [`Prime Number Generator/`](Prime%20Number%20Generator/) | Scale-dependent meta-pattern theory of primes |
| [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) | QDMP framework + CVD pathways to quantum-grade diamond |
| [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) | Quantum-inspired classical compressed graph processor |
| [`RNGS/`](RNGS/) | Random number generators (incl. Turbulent Flow RNG) |
| [`Rockwell 50 to 70 Carbide/`](Rockwell%2050%20to%2070%20Carbide/) | HX-70 GradePlex™ + TriboshieldPlus™ + forge-to-machine |
| [`Statistical Generation/`](Statistical%20Generation/) | Universal Statistical Generator (category theory + Lévy + IT) |
| [`Statistical Scheduler/`](Statistical%20Scheduler/) | Neural-heuristic distributed task scheduler (LinTS / PID / CFS) |
| [`UCN AIs/`](UCN%20AIs/) | APN / GPN / Signal AI / linear primitives |
| [`UCN Political System/`](UCN%20Political%20System/) | UCN doctrine series + economics + sovereign currency |
| [`VDJ Inspired Algorithm/`](VDJ%20Inspired%20Algorithm/) | Combinatorial pattern recognition + one-shot learning |
| [`Veritas/`](Veritas/) | Formal verification framework |
| [`Weapons/`](Weapons/) | Defence-tech R&D portfolio (UNCLASSIFIED / FOUO style) |

---

## 🔗 Quick links

| File | Role |
|---|---|
| [`AUDIT_README_VS_SOURCE.md`](AUDIT_README_VS_SOURCE.md) | Audit log of README ↔ source-paper discrepancies and the remediation path that produced the current state of this repo |
| [`modified-license.md`](modified-license.md) | Full dual-licence terms (AGPL-3.0+ / commercial) |
| [`dual-license-setup.md`](dual-license-setup.md) | Dual-licence setup notes |
| [`docs/`](docs/) | Static-site assets — `index.html`, shared CSS, generated `site/` mirror, `EDITORIAL_STYLE.md` |

---

## 🔤 Acronym key

Several letter-combinations collide between folders. This index gives each acronym its expansion and the folder that defines it. *Where two folders both use a label, both are listed.*

| Acronym | Expansion | Folder |
|---|---|---|
| **AEAD** | Authenticated Encryption with Associated Data (cryptographic primitive) | [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) |
| **APN** | Any Purpose Network | [`UCN AIs/`](UCN%20AIs/) |
| **ARIA** | Algebraic Resynchronisation and Integrity Architecture (this repository's ARIA — *not* the Korean ARIA block cipher) | [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) |
| **ARIA-INTEL** | Algebraic Rendezvous & Intelligence Analyser | [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) |
| **CFS** | Completely Fair Scheduler (Linux baseline that the scheduler builds on) | [`Statistical Scheduler/`](Statistical%20Scheduler/) |
| **CMUT** | Capacitive Micromachined Ultrasonic Transducer (the wearable patch) | [`Neural Dust/`](Neural%20Dust/) |
| **CVD** | Chemical Vapour Deposition | [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) |
| **EREM** | Energy-Resource Economic Model | [`Economics/`](Economics/) |
| **FATHM** | Force-Allocation-by-Threat Hierarchical-Mathematical (one of the modelled traditions) | [`Battle Sim/`](Battle%20Sim/) |
| **GF(2)** | Galois Field of order 2 (the binary finite field) | [`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/) |
| **GH-JPDA** | Generalised-Hyperbolic Joint Probabilistic Data Association | [`Filtering/`](Filtering/) |
| **GH-SR-IMM** | Generalised-Hyperbolic Square-Root Interacting-Multiple-Model | [`Filtering/`](Filtering/) |
| **GOSPA** | Generalised Optimal Sub-Pattern Assignment (multi-target tracking metric) | [`Filtering/`](Filtering/) |
| **GPN** | General Purpose Network | [`UCN AIs/`](UCN%20AIs/) |
| **GRIA** | Graded Reversibility-Irreversibility Algebra | [`Compression Algorithms/`](Compression%20Algorithms/) |
| **GUP** | Generalised Uncertainty Principle | [`Physics/`](Physics/) |
| **HRNA** | Harmonic Recursive Neural Architecture | [`Cypha/`](Cypha/) |
| **HSA** | Homo Sapiens Augmentus | [`GM Enhancements/`](GM%20Enhancements/) |
| **IMM** | Interacting Multiple Model (Bayesian filter bank) | [`Filtering/`](Filtering/) |
| **IRE** | Incremental Riemannian Estimation | [`NN Shortcuts/`](NN%20Shortcuts/) |
| **ISFD** | In-Situ-Forming Depot (drug-delivery technology) | [`Drugs/`](Drugs/) |
| **LCRP** | Logarithmic Complexity Reduction Principle | [`General Math Papers/`](General%20Math%20Papers/) |
| **LinTS** | Linear Thompson Sampling | [`Statistical Scheduler/`](Statistical%20Scheduler/) |
| **LSH** | Locality-Sensitive Hashing | [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) |
| **MoE** | Mixture-of-Experts | [`Neural Decompiler/`](Neural%20Decompiler/) |
| **NACS** | NEXUS Adaptive Combat System (CBRN protection module) | [`Weapons/`](Weapons/) |
| **NLFGN-UFT** | Non-Local Field-Gravity Network Unified Field Theory | [`Physics/`](Physics/) |
| **NMP** | Nonlinear Matrix Pruning (this repository's NMP — neural compression) | [`Compression Algorithms/`](Compression%20Algorithms/) |
| **NQD** | Neural Quantum Dust | [`Neural Dust/`](Neural%20Dust/) |
| **NV** | Nitrogen-Vacancy (defect centre in diamond) | [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/), [`Neural Dust/`](Neural%20Dust/) |
| **OSK** | Oct4-Sox2-Klf4 (partial reprogramming factors, no c-Myc) | [`GM Enhancements/`](GM%20Enhancements/) |
| **PMBM** | Poisson Multi-Bernoulli Mixture (random finite set tracker) | [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) |
| **PRF** | Pseudo-Random Function (the shared-PRF coordination primitive) | [`Compression Algorithms/`](Compression%20Algorithms/), [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) |
| **QAOA** | Quantum Approximate Optimisation Algorithm | [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) |
| **QDMP** | Quantum Diamond Metamaterial Processor | [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) |
| **QND** | Quantum NanoDiamond (the cellular-scale sensor tier) | [`Neural Dust/`](Neural%20Dust/) |
| **SGF** | Streaming Geometry Framework | [`NN Shortcuts/`](NN%20Shortcuts/) |
| **TACS** | Tactical Acoustic Cancellation System | [`Weapons/`](Weapons/) |
| **TDC** | Torpedo Data Computer (WWII fire-control) | [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/) |
| **TNW** | Total National Wealth (in megajoules) | [`Economics/`](Economics/) |
| **UCDW** | Ultra-Compact Diffusion Welding | [`Diffusion Welding/`](Diffusion%20Welding/) |
| **UCN** | United Commonwealth Nations | [`UCN Political System/`](UCN%20Political%20System/), [`UCN AIs/`](UCN%20AIs/) |
| **UHPM** | Unified Hash-Predictive Memory | [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) |
| **USG** | Universal Statistical Generator | [`Statistical Generation/`](Statistical%20Generation/) |
| **V(D)J** | Variable-Diversity-Joining (vertebrate immune-system gene recombination) | [`VDJ Inspired Algorithm/`](VDJ%20Inspired%20Algorithm/) |
| **Veritas** | Verification-Enabled Reasoning and Integrated Theorem-Acquiring System | [`Veritas/`](Veritas/) |
| **WTA** | Wearable Transducer Array (the external CMUT patch) | [`Neural Dust/`](Neural%20Dust/) |

---

## 🛡 Honest framing

- **A research shelf, not a product catalogue.** Many folders propose systems that have not been built or validated; speculative items carry that label in their own README.
- **Defence framing is a stylistic register.** The Weapons folder, GM Enhancements, ARIA-INTEL, and a handful of others use UNCLASSIFIED / FOUO-style document register. No real classification, sponsorship, or fielded materiel is implied.
- **Speculative pharmacology is not medical advice.** `Drugs/`, `Drugs/Nootropics/`, `Drugs/Schizophrenia Cure/`, `GM Enhancements/`, `Beauty Products/`, and `Weapons/Combat Drug.md` describe theoretical compounds and protocols. Do not synthesise, possess, or administer them.
- **Acronym hygiene matters.** See the [§ Acronym key](#-acronym-key) above; several letter-combinations collide between folders (ARIA, NMP, HSA), so each folder's README spells out which expansion is meant in that context.
- **Numbers are sourced.** Every "headline number" in the [§ Selected highlights](#-selected-highlights) section is taken directly from the corresponding folder's research paper. Per-folder caveats live in those folders' "Honest framing" sections.

---

[← This is the main README]
