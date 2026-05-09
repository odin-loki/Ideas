# Ideas — Odin Loch's R&D shelf

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

You can read this index four ways:

1. **By scientific subfield** ([§ Categories](#-categories)) — one section per scientific subfield, fine-grained.
2. **A–Z** ([§ A–Z folder index](#-az-folder-index)) — alphabetical with one-line descriptions.
3. **Navigation aids** ([§ Quick links](#-quick-links)) — repo-level files (audit trail, licence, etc.).
4. **Acronym key** ([§ Acronym key](#-acronym-key)) — every named system in one alphabetised glossary.

---

## 📚 Categories

Each section below is a single scientific subfield. Folders are grouped strictly by methodology, not by superficial topic similarity. Where two folders share a subfield (e.g. multi-target tracking, or shared-PRF coordination), they appear together; otherwise each folder gets its own section. Categories are ordered roughly from most-established science to most-speculative / creative.

**Quick navigation** (43 categories):

1. [An encryption algorithm](#-an-encryption-algorithm)
2. [Cracking AES with AI (a training stack, not a break)](#-cracking-aes-with-ai-a-training-stack-not-a-break)
3. [Random number generators](#-random-number-generators)
4. [Saving bandwidth with shared random streams](#-saving-bandwidth-with-shared-random-streams)
5. [Machine learning that proves what it learned](#-machine-learning-that-proves-what-it-learned)
6. [Tracking many moving targets at once](#-tracking-many-moving-targets-at-once)
7. [Sub-millisecond computer-job scheduling](#-sub-millisecond-computer-job-scheduling)
8. [Giving neural networks long memories](#-giving-neural-networks-long-memories)
9. [A neural network without attention](#-a-neural-network-without-attention)
10. [A production-grade neural network stack](#-a-production-grade-neural-network-stack)
11. [Making neural networks run faster](#-making-neural-networks-run-faster)
12. [Turning machine code back into source code](#-turning-machine-code-back-into-source-code)
13. [A language model without neural networks](#-a-language-model-without-neural-networks)
14. [Optimisation inspired by 1948 cybernetics](#-optimisation-inspired-by-1948-cybernetics)
15. [Pattern recognition modelled on the immune system](#-pattern-recognition-modelled-on-the-immune-system)
16. [Algorithms that grow like fungus](#-algorithms-that-grow-like-fungus)
17. [AI families for an imagined future nation](#-ai-families-for-an-imagined-future-nation)
18. [All the Boolean functions, dimension by dimension](#-all-the-boolean-functions-dimension-by-dimension)
19. [The algebra of XOR and AND](#-the-algebra-of-xor-and-and)
20. [When slow problems have fast algorithms](#-when-slow-problems-have-fast-algorithms)
21. [Auto-generating maths-curriculum questions](#-auto-generating-maths-curriculum-questions)
22. [Finding patterns in prime numbers](#-finding-patterns-in-prime-numbers)
23. [Foundational physics and cosmology](#-foundational-physics-and-cosmology)
24. [A quantum computer made from diamond](#-a-quantum-computer-made-from-diamond)
25. [Quantum-style graph optimisation, on a normal computer](#-quantum-style-graph-optimisation-on-a-normal-computer)
26. [Brain interfaces from ultrasound-powered nanodiamonds](#-brain-interfaces-from-ultrasound-powered-nanodiamonds)
27. [A speculative human-enhancement protocol](#-a-speculative-human-enhancement-protocol)
28. [Drug formulation and slow-release recipes](#-drug-formulation-and-slow-release-recipes)
29. [A 100-watt wideband RF noise generator](#-a-100-watt-wideband-rf-noise-generator)
30. [Designing a new kind of CPU](#-designing-a-new-kind-of-cpu)
31. [Diamond batteries powered by nuclear waste](#-diamond-batteries-powered-by-nuclear-waste)
32. [Welding metal in a backpack-sized box](#-welding-metal-in-a-backpack-sized-box)
33. [Cutting tools for very hard steel](#-cutting-tools-for-very-hard-steel)
34. [New kinds of resistors, capacitors, and inductors](#-new-kinds-of-resistors-capacitors-and-inductors)
35. [Old mechanical computers, redone in modern code](#-old-mechanical-computers-redone-in-modern-code)
36. [Sketching what comes after C++](#-sketching-what-comes-after-c)
37. [Currency backed by joules, not gold](#-currency-backed-by-joules-not-gold)
38. [Designing a new political system from scratch](#-designing-a-new-political-system-from-scratch)
39. [How militaries mathematically model battles](#-how-militaries-mathematically-model-battles)
40. [Defence-tech research and spec sheets](#-defence-tech-research-and-spec-sheets)
41. [A luxury hempseed body lotion, fully formulated](#-a-luxury-hempseed-body-lotion-fully-formulated)
42. [Running a cocktail bar like an engineering project](#-running-a-cocktail-bar-like-an-engineering-project)
43. [Repository infrastructure (site assets and styling)](#-repository-infrastructure-site-assets-and-styling)

---


### 🔐 An encryption algorithm

| Folder | Description |
|---|---|
| [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) | A custom AEAD scheme (Algebraic Resynchronisation and Integrity Architecture) whose nonces are **never transmitted** — receiver re-derives them from the message and a session key, structurally eliminating loss-of-nonce-sync. Three-layer algebraic tower over `GF(2²⁵⁶)` + Meta-DAG RNG entropy pump + dual collision bounds. *Not* the Korean ARIA block cipher. |

### 🔓 Cracking AES with AI (a training stack, not a break)

| Folder | Description |
|---|---|
| [`Break AES/`](Break%20AES/) | Research scaffolding combining a Transformer student + Llama-teacher knowledge distillation + policy-gradient reinforcement learning with a BLEU-shaped reward — framed as a training stack one might point at AES cryptanalysis. **Not an AES break.** Python skeleton + informal proof-sketch note. |

### 🎲 Random number generators

| Folder | Description |
|---|---|
| [`RNGS/`](RNGS/) | Four genuinely different generator families with explicit threat models: OTB-LCG (Boolean / transcendental + SHA-256 post-processing), SynerChaos v2 (`~80 cycles/output` on Cortex-M4), Meta-DAG RNG (`≥ 2¹⁵³⁶ × 40320` state-space lower bound), Turbulent Flow (`χ² p = 0.582`, avalanche pass rate `> 0.999`). |

### 📦 Saving bandwidth with shared random streams

| Folder | Description |
|---|---|
| [`Compression Algorithms/`](Compression%20Algorithms/) | Canonical home of three frameworks: **Izaac** (shared-PRF coordination → free broadcast channel meta-theorem), **GRIA** (graded reversibility coordinate `α(f) = 1 − H(f(X))/H(X)` with bifurcation at `α = 0.5`, `J ≤ 0.951` upper bound), and **NMP** (Nonlinear Matrix Pruning; `α ≈ 0.851 ± 0.122` measured spectral exponent). |
| [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) | Twelve concrete protocols operationalising the Izaac meta-theorem. **Bloom filter coordinated by an Izaac shared seed saves `N × 384` bits of message overhead** — for `N = 10⁶`, that is `48 MB` moved off-wire per coordination round. |

### ✅ Machine learning that proves what it learned

| Folder | Description |
|---|---|
| [`Veritas/`](Veritas/) | A learning architecture in which the artefact produced is not loss curves but proof traces. Every learner emits PAC, mistake-bound, meta-learning, and composition certificates. Worked example: function class `\|H\| = 2^(2⁸) = 2²⁵⁶`, sample bound at `ε = δ = 0.01` is `~1.8 × 10⁶` — proven, not hoped. |

### 🎯 Tracking many moving targets at once

| Folder | Description |
|---|---|
| [`Filtering/`](Filtering/) | A heavy-tailed multi-target tracker (Generalised-Hyperbolic Square-Root Interacting-Multiple-Model). The distinguishing contribution is a **GH-JPDA extension that fixes a known bug** in the standard recipe (use the GH posterior covariance inside a Gaussian association likelihood, *not* the GH likelihood directly): mean **`51.6 %` GOSPA improvement** across four scenarios, peaking at `72.8 %`. |
| [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) | A single-file, edge-deployable multi-target tracker and tactical-intelligence engine (ARIA-INTEL). PMBM random-finite-set tracking + three rendezvous predictors + eight tradecraft detectors + Dempster–Shafer fusion, running at **`~28 ms` median scan latency** on a single CPU core. |

### ⏱ Sub-millisecond computer-job scheduling

| Folder | Description |
|---|---|
| [`Statistical Scheduler/`](Statistical%20Scheduler/) | A neural-heuristic distributed task scheduler. CFS-style fair-share scoring + Linear Thompson Sampling exploration in 24-D context + PID-controlled stability override + Holt–Winters / CUSUM / EWMA monitoring. **`p50 0.48 ms`** placement latency, **Jain fairness `1.00`**, formal `O(d√T·polylog T)` regret. |

### 🧠 Giving neural networks long memories

| Folder | Description |
|---|---|
| [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) | Unified Hash-Predictive Memory — fuses LSH memory and hierarchical predictive coding under one free-energy functional. **`289 ×` query-latency speedup** vs full attention at `100 K` tokens (`8.1 ms` vs `2 340 ms`); **`744 ×` memory reduction**. |

### 🧬 A neural network without attention

| Folder | Description |
|---|---|
| [`Cell AI/`](Cell%20AI/) | A biology-motivated sequence-modelling architecture (CellularAI). Replaces self-attention with reaction-diffusion partition dynamics, online Hebbian plasticity *during the forward pass*, and a 27-experiment architecture-search programme (E0 – E26). Honest that v1 doesn't approach transformer perplexity on real corpora. |

### 🔧 A production-grade neural network stack

| Folder | Description |
|---|---|
| [`Cypha/`](Cypha/) | A neural-network inference and training stack (Harmonic Recursive Neural Architecture). Python reference + CMake-built C++ native core + REST server + Qt desktop Studio. **`188` pytest + `33` CTest** parity tests verify Python and native produce *byte-identical* outputs across 13+ named fixtures. |

### ⚡ Making neural networks run faster

| Folder | Description |
|---|---|
| [`NN Shortcuts/`](NN%20Shortcuts/) | A unifying framework. The Streaming Geometry Framework reduces 16 canonical NN acceleration techniques to one principle (Incremental Riemannian Estimation); the Algebraic Autopsy decomposes a trained network into tropical + Grassmannian + `11 %` dense `(ℝ, +, ×)` content. |

### 🔁 Turning machine code back into source code

| Folder | Description |
|---|---|
| [`Neural Decompiler/`](Neural%20Decompiler/) | Assembly-to-source as conditional sequence modelling. Encoder–decoder Transformer + hierarchical memory + load-balanced mixture-of-experts (binary-focused vs language-focused). Coherent trainable architecture, not a state-of-the-art recovery system. |

### 📊 A language model without neural networks

| Folder | Description |
|---|---|
| [`Statistical Generation/`](Statistical%20Generation/) | The Universal Statistical Generator — a deterministic, interpretable, classical-statistics framework claiming **`~90 %`** of state-of-the-art neural perplexity on long-context tasks at **`O(N)`** training cost. Built on category theory + Lévy triplets + SHA-256 hash compression to `M = 2³²` states. |

### 🌀 Optimisation inspired by 1948 cybernetics

| Folder | Description |
|---|---|
| [`Ashby Optimiser/`](Ashby%20Optimiser/) | W. Ross Ashby's 1948 homeostat reframed as a black-box optimiser. Parallel search units at geometrically-spaced radii, strict round-robin scheduling, homeostatic restarts on stagnation. On Rastrigin dim 10 with 500 evals: multi-scale **`0.002`** vs single-scale **`74.7`**. |

### 🦠 Pattern recognition modelled on the immune system

| Folder | Description |
|---|---|
| [`VDJ Inspired Algorithm/`](VDJ%20Inspired%20Algorithm/) | Combinatorial pattern recognition derived from V(D)J recombination in the vertebrate immune system. Five primary modules + seven subsystems through a typed `Pattern` dataclass. **`~13 ms` at `n = 16, r = 5`** with a `< 1 MB` peak memory footprint. CPU-only. |

### 🍄 Algorithms that grow like fungus

| Folder | Description |
|---|---|
| [`Fungal Network Algorithm/`](Fungal%20Network%20Algorithm/) | Pattern recognition through physical network reorganisation, modelled on how fungi search for food without central control. The topology *itself* is the long-term memory; weights and edges are consequences of input history. Decentralised, emergent. |

### 👾 AI families for an imagined future nation

| Folder | Description |
|---|---|
| [`UCN AIs/`](UCN%20AIs/) | Two flagship classes — Any Purpose Network (measurement-based, fast adaptation) and General Purpose Network (simulation-based, deep comprehension); one signal-processing class (Universal Resonance Learning System); and two foundational learning primitives. In-universe technical writing, not built systems. |

### 📐 All the Boolean functions, dimension by dimension

| Folder | Description |
|---|---|
| [`3 to 8 Value Boolean Algebra/`](3%20to%208%20Value%20Boolean%20Algebra/) | Dimension-by-dimension narrative of the full Boolean function spaces `f : {0,1}ⁿ → {0,1}` for `n = 3 – 8` — exact at small `n` (`256` at `n = 3`, `65 536` at `n = 4`), sampled at large `n` (`2²⁵⁶ ≈ 1.16 × 10⁷⁷` at `n = 8`). Threaded through to error-correcting codes, Byzantine NMR, AES-S-box-style nonlinearity. |

### 🔢 The algebra of XOR and AND

| Folder | Description |
|---|---|
| [`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/) | A seven-paper sweep starting with an exhaustive computer-verified taxonomy of all 16 binary operations on `{0, 1}`. Proves: **AND is the *only* nontrivial operation forming a ring with XOR over GF(2)**. AES-inverse permutation polynomial (`x⁻¹ = x²⁵⁴` is `1 of 128` permutations on `GF(2⁸)`). Gate-count benchmarks (Rule 110: `19 → 6` gates, `68 %` reduction). Differentiable Logic Gate Networks. |

### ⏳ When slow problems have fast algorithms

| Folder | Description |
|---|---|
| [`General Math Papers/`](General%20Math%20Papers/) | The Logarithmic Complexity Reduction Principle (LCRP) — a meta-principle, not a theorem, that documents the recurring pattern by which naively `Ω(n²)` problems admit `O(n log n)` algorithms via divide-and-conquer or `O(log n)`-per-element data structures. Master Theorem case analysis as the decision procedure. |

### ✏️ Auto-generating maths-curriculum questions

| Folder | Description |
|---|---|
| [`Math Question Generator/`](Math%20Question%20Generator/) | MegaMathGen — a multi-thousand-line generator for curriculum-grade math problems across the full mathematics-classification taxonomy. SymPy + NumPy + 1000-decimal-place precision arithmetic, `28 GB` memory cap, checkpointing. Paired with a 13-domain landscape survey anchored to MSC2020. |

### 🔷 Finding patterns in prime numbers

| Folder | Description |
|---|---|
| [`Prime Number Generator/`](Prime%20Number%20Generator/) | An empirical scale-dependent meta-pattern theory of primes. Local divisibility / 6k±1 effects and global PNT-style gap heuristics make different scale-dependent contributions, crossing over at **`n* ≈ 836`** (`s* = log₁₀ n ≈ 2.92`) under a fitted `α(s) = s^(−0.37)` law. Hybrid Miller–Rabin (`k = 20`, error `≤ 9 × 10⁻¹³`). |

### 🌌 Foundational physics and cosmology

| Folder | Description |
|---|---|
| [`Physics/`](Physics/) | Two distinct papers. **NLFGN-UFT** (Non-Local Field-Gravity Network Unified Field Theory) — non-local network-augmented gravity with explicit advanced + retarded kernels and the structural claim **`v_field ≤ c`**. **Superluminal Recession** — argues that apparent FTL galaxy recession (`v_rec > c` at `z ≈ 1.46`, CMB at `~3.2 c` today) exposes a real interpretational split between rigorous GR-based positions, not a failed ΛCDM fit. |

### 💎 A quantum computer made from diamond

| Folder | Description |
|---|---|
| [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) | An aspirational CVD-grown Quantum Diamond Metamaterial Processor (QDMP) — paired with a sober companion paper arguing near-term wins live in sensors / hybrid memory / QKD nodes, not room-temperature processors. Targets `T₂ > 100 s` at room temperature (`~10⁴ ×` over `~3 ms` current); seven barriers explicitly enumerated; fact-vs-fiction ledger. |

### ⚛️ Quantum-style graph optimisation, on a normal computer

| Folder | Description |
|---|---|
| [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) | A fully-classical, quantum-shaped graph-optimisation pipeline. Five layers — spectral Laplacian compression → Chebyshev coefficient encoding → small exact (or mean-field) QAOA simulation → noise-norm-weighted shot ranking → spectral lift-back — with verification functions for each. No hardware, no quantum-advantage claim. |

### 🧪 Brain interfaces from ultrasound-powered nanodiamonds

| Folder | Description |
|---|---|
| [`Neural Dust/`](Neural%20Dust/) | Neural Quantum Dust (NQD), a two-tier neural-interface architecture: `150 – 250 nm` NV-nanodiamond quantum sensors + `80 – 150 µm` ultrasound-powered CMOS motes. Closes a **`~6 nW`** power budget on FDA-compliant ultrasound (`MI ~ 0.4` vs limit `0.7`), with `~2 – 3 nT/√Hz` magnetometry. **`15 – 25 year`** programme, every component tagged Verified / Plausible / Speculative. |

### 💉 A speculative human-enhancement protocol

| Folder | Description |
|---|---|
| [`GM Enhancements/`](GM%20Enhancements/) | Homo Sapiens Augmentus (HSA) v4.0 — a three-phase **`24 – 34 month`** speculative protocol fusing AAV / LNP / lentiviral delivery, CRISPRa/i + base + prime editing, OSK partial reprogramming, senolytics, and organ-bioprinting. Published with **`~20 – 32 %`** cumulative SAE risk table. **Worldbuilding-purposes-only** banner. |

### 💊 Drug formulation and slow-release recipes

| Folder | Description |
|---|---|
| [`Drugs/`](Drugs/) | A split folder. *Industrial* pharmaceutics playbooks (Universal Depot framework with PLGA tuning bands `50:50 10–25 kDa` for `1–3 month` release through to `PLA 100–300 kDa` for `12–36 month`, sugar-excipient review, Poloxamer / ISFD recipes) live alongside *speculative* monographs (`COGNIMAX-PRO`, `NeuroBridge-7`, `MetaMax-2034`). Every speculative compound is banner-flagged. **Not medical advice.** |

### 📻 A 100-watt wideband RF noise generator

| Folder | Description |
|---|---|
| [`100W Wideband Noise Generator/`](100W%20Wideband%20Noise%20Generator/) | A single SystemVerilog file orchestrating a Chua-circuit chaotic analogue core, four-band RF power-amplifier chain, 12-bit programmable supply DAC, eight-channel thermal ADC, and hard-protection state machine. Banner targets: **`1 Hz – 14 GHz`** (hardware-dependent), **`100 W`** continuous output, sub-microsecond fault response. |

### 🖥️ Designing a new kind of CPU

| Folder | Description |
|---|---|
| [`CPU/`](CPU/) | A heterogeneous many-core CPU design conversation paired with a SystemVerilog sketch of an `os_accelerator` whose inner `hardware_bios` state machine runs `POWER_ON_SELF_TEST → HARDWARE_INIT → MEMORY_TEST → BOOT_SEQUENCE → SYSTEM_INIT → OS_HANDOFF`. **`16` big OOO cores at 4 GHz + `4 096` small cores**, MOESI cache coherence, hardware-accelerated syscalls. Not buildable as written. |

### ☢️ Diamond batteries powered by nuclear waste

| Folder | Description |
|---|---|
| [`Diamond Batterys/`](Diamond%20Batterys/) | An eight-model taxonomy (Series A – D) of radioisotope diamond batteries from the demonstrated `~kW`-class Bristol/UKAEA C-14 baseline (Dec 2024) up to `GW`-class Cm-244 / Am-242m / U-235 subcritical concepts. Engineering-fiction-grade; explicitly hypothetical. |

### 🔥 Welding metal in a backpack-sized box

| Folder | Description |
|---|---|
| [`Diffusion Welding/`](Diffusion%20Welding/) | Ultra-Compact Diffusion Welding (UCDW) — a five-regime tradespace from **`2-min / 77 %`-strength** battlefield repairs to **`2.3-hour / 99 %`-strength** aerospace-certifiable bonds, on the same chemistry / electrode set / control logic. Equipment cost `$8K – $50K` vs incumbent vacuum diffusion welding's `$500K – $2M`. |

### ⚙️ Cutting tools for very hard steel

| Folder | Description |
|---|---|
| [`Rockwell 50 to 70 Carbide/`](Rockwell%2050%20to%2070%20Carbide/) | A complete carbide-tooling platform for hard-machining steels `HRC 40 – 70` — HX-70 GradePlex functionally-graded WC-Co substrate (`2050 – 2100 HV30` working surface), TriboshieldPlus 5-layer coating (`42 – 46 GPa` hardness core, `µ < 0.15`), and a forge-to-machine supply chain that drops `40 – 45 %` of cost and `65 – 70 %` of lead time on the H13-breech exemplar. |

### 🔌 New kinds of resistors, capacitors, and inductors

| Folder | Description |
|---|---|
| [`New Classes of Electrical Components/`](New%20Classes%20of%20Electrical%20Components/) | A four-tier catalogue of `≥ 21` discrete-continuous hybrid passive devices, paired with a five-phase Python simulation programme. Headline simulator claims: **`2.34 × 10⁹` fused solves/s on RTX 3090**, **`526 ×` adjoint-method inverse-design speedup**, SPICE / Verilog-AMS / SystemC-AMS export at `< 2.1 %` accuracy. |

### 🕰️ Old mechanical computers, redone in modern code

| Folder | Description |
|---|---|
| [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/) | Three historical computing machines refactored into modern Python with measured benchmarks: **Babbage Difference Engine `4.92 ×` speedup**, **Antikythera Fourier reconstruction `386 ×` speedup**, **digital Torpedo Data Computer `> 10⁶ solutions/s` at `±0.015°`**. |

### 💻 Sketching what comes after C++

| Folder | Description |
|---|---|
| [`Future C++/`](Future%20C++/) | A long design-conversation transcript exploring what a "modern compiled language with C++ syntax" might look like — borrow-checking from Rust, async/await + green threads, software-transactional memory, richer generics + ADTs + pattern matching. No compiler, no grammar, no benchmarks. |

### ⚖️ Currency backed by joules, not gold

| Folder | Description |
|---|---|
| [`Economics/`](Economics/) | The Energy-Resource Economic Model (EREM) — measures national wealth in **megajoules of Total National Wealth (TNW)** rather than GDP, issues currency at **`Total_currency = k · TNW`** with `k = 0.85` (`15 %` measurement buffer), defines exchange rate as the directly-comparable per-capita TNW ratio. Theoretical / v1.0; asks for empirical validation. |

### 🏛️ Designing a new political system from scratch

| Folder | Description |
|---|---|
| [`UCN Political System/`](UCN%20Political%20System/) | The eight-paper United Commonwealth Nations doctrine series — modular Westminster++ governance, hard-sovereignty economics, `≤ 10`-warhead minimal nuclear deterrent, `AUD 100M` personal wealth ceiling, government-manufactured pharma-grade recreational drugs, optional UK – Canada – Australia Crown confederation. Speculative; every claim is referenced. |

### ⚔️ How militaries mathematically model battles

| Folder | Description |
|---|---|
| [`Battle Sim/`](Battle%20Sim/) | A survey-and-design note that maps the modern mathematical-modelling landscape for combat — Hughes salvo equations, extended Lanchester, Markov battle-state chains, FATHM linear programming, Dupuy / TNDM combat-power lineage — into one comparative reading map. **Explicitly not an operational simulator.** |

### 🛡️ Defence-tech research and spec sheets

| Folder | Description |
|---|---|
| [`Weapons/`](Weapons/) | A defence-engineering R&D portfolio with paired operator-spec-sheets and TRP-numbered research papers across small-arms (`MP-6.8`, `MAS-15.2E`), heavy weapons (`57mm` autocannon, `140mm` tank round), body armour (APES, AlNiCyN, OBSIDIAN family), CBRN protection (NACS), tactical acoustic cancellation (TACS at `35 – 55 dB` depth), and CL-20 high explosive. Classification banners are stylistic. |

### 💄 A luxury hempseed body lotion, fully formulated

| Folder | Description |
|---|---|
| [`Beauty Products/`](Beauty%20Products/) | A fully-architected cosmeceutical white paper for a hemp-anchored luxury body lotion — `3 : 1` omega-6 : omega-3 hempseed-oil base, Tremella-snow-mushroom humectant (`~500 ×` water-holding capacity), prickly-pear / sea-buckthorn / Centella `0.2 %` asiaticoside active stack, `pH 4.8 – 5.5`, all-natural `3 %` Phase-D preservative system. Fully cited. |

### 🍸 Running a cocktail bar like an engineering project

| Folder | Description |
|---|---|
| [`Cocktails/`](Cocktails/) | A bar-operations system treated as a product platform — four native-Australian-botanical bases driving every infusion / syrup / tincture / bitters across four signature series with parallel zero-proof mirrors, two complete bitters fabrication specs, a `2-hour` mushroom stock + `4-hour` fat-wash protocol, and a shift / day / week / month prep workflow. |

### 🛠️ Repository infrastructure (site assets and styling)

| Folder | Description |
|---|---|
| [`docs/`](docs/) | Static-site assets for the public site: `index.html`, shared CSS, generated `site/` mirror, and the `EDITORIAL_STYLE.md` house style guide. Repository plumbing only. |

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
- **Numbers are sourced.** Every "headline number" in a category description is taken directly from the corresponding folder's research paper. Per-folder caveats live in those folders' "Honest framing" sections.

---

[← This is the main README]
