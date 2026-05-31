# Ideas ? Odin Loch's R&D shelf

---

## ?? Licensing

Dual-licensed:

1. **GNU Affero General Public License v3.0+ (AGPL-3.0+)** ? free tier for personal use, charity, education, and entities with annual income < AUD 50 000.
2. **Tiered commercial licence** ? for commercial use above the free-tier threshold.

See [`modified-license.md`](modified-license.md) for full terms and [`dual-license-setup.md`](dual-license-setup.md) for setup notes.

**Attribution under AGPL-3.0+:**

> "Powered by Ideas, developed by Odin Loch. Licensed under AGPL-3.0+."

Modifications must be shared back under the same dual-licence; research using this software must be open-sourced. Commercial licensees: no requirement to share modifications.

**Commercial enquiries:** odin.loch@outlook.com.au

---

## ?? How to navigate

The repository is organised as one folder per topic, browsable in any order. Each folder has its own README that describes what the folder actually contains, lists the source documents, and links related work elsewhere in the repo.

You can read this index four ways:

1. **By field** ([? Categories](#-categories)) ? grouped by the field a curious layman would file each project under.
2. **A?Z** ([? A?Z folder index](#-az-folder-index)) ? alphabetical with one-line descriptions.
3. **Navigation aids** ([? Quick links](#-quick-links)) ? repo-level files (audit trail, licence, etc.).
4. **Acronym key** ([? Acronym key](#-acronym-key)) ? every named system in one alphabetised glossary.

---

## ?? Categories

Each section below is the field a curious layman would file these projects under. The descriptions explain what each thing *is* and what it does, in plain-but-not-dumbed-down language.

### ?? Cryptography

| Folder | Description |
|---|---|
| [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) | A custom encryption scheme that doesn?t transmit nonces ? the small unique numbers normally appended to each message to keep encryption fresh. The receiver re-derives the nonce from the message itself plus a shared key, eliminating an entire class of bugs around lost or replayed nonces. Three-layer algebraic construction over a 256-bit binary field. *Not* the Korean ARIA block cipher. |
| [`Modelling AES/`](Modelling%20AES/) | Two complementary neural studies of AES, both negative or limited results. (a) `neural_aes_paper.md` argues that recovering AES-128 key material from plaintext-ciphertext pairs is infeasible for any neural network ? three independent barriers (output entropy indistinguishability, pseudorandom collapse, combinatorial state-space) are quantified, and empirically the model achieves `0.675 %` first-byte accuracy vs the `0.3906 %` random baseline (`p = 0.066`). (b) `neural_prng_paper.md` asks the converse ? can a network learn to *generate* AES-style ciphertext-distribution output? A GAN reaches `7.983` bits byte-entropy and gzip compression `1.0005` (statistically indistinguishable from AES on these two metrics) but fails the chi-squared uniformity test (`p ? 0`). The folder also contains `Break AES with NNs/`, the Transformer + REINFORCE training scaffolding for the attempted key-recovery attack. |
| [`RNGS/`](RNGS/) | Four pseudo-random-number generators built for very different jobs: a general-purpose generator with cryptographic hashing on the output, a fast one for tiny embedded chips (~80 cycles per output on a Cortex-M4), one with a state space larger than 2?5?6, and one based on the chaos of turbulent fluid flow. |
| [`Compression Algorithms/`](Compression%20Algorithms/) | Three frameworks. The headline (**Izaac**) shows that two computers sharing the same pseudo-random stream get a free communication channel ? anything they can independently compute from that stream doesn?t need to be sent over the wire. The other two are an algebra of how irreversible a given function is, and a measured spectral law for pruning weights from neural networks. |
| [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) | Twelve concrete protocols built on the Izaac idea. The clearest example: a Bloom filter coordinated by an Izaac shared seed saves **48 megabytes** of network traffic per coordination round when a million nodes participate, because both sides compute the filter locally instead of transmitting it. |

### ?? Artificial intelligence

| Folder | Description |
|---|---|
| [`Cell AI/`](Cell%20AI/) | A neural-network architecture that replaces self-attention (the engine of GPT-style models) with reaction-diffusion partition dynamics and Hebbian plasticity that updates the weights *during* the forward pass, the way biological neurons do. 27-experiment architecture-search log; honest that v1 doesn?t yet match transformer perplexity on real corpora. |
| [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) | A long-context memory architecture that fuses locality-sensitive hashing (a fast way to find approximate nearest neighbours in high-dimensional space) with hierarchical predictive coding (a brain-inspired prediction-error mechanism), under one shared free-energy functional. **289?? faster than full attention** at 100?000-token contexts, with 744?? memory reduction. |
| [`Neural Decompiler/`](Neural%20Decompiler/) | A neural-network architecture for the problem of turning compiled machine code back into readable source code ? an encoder?decoder Transformer with hierarchical memory plus a load-balanced mixture-of-experts split between binary-pattern experts and language-model experts. Coherent design, not a state-of-the-art recovery system. |
| [`NN Shortcuts/`](NN%20Shortcuts/) | A unifying mathematical framework for sixteen separate neural-network speedup tricks (pruning, distillation, quantisation, low-rank factorisation, etc.). Reduces them all to one underlying principle: **Incremental Riemannian Estimation**. Bonus: an ?algebraic autopsy? that decomposes a trained network into tropical, Grassmannian, and standard-arithmetic content. |
| [`Statistical Generation/`](Statistical%20Generation/) | A language model with **no neural networks in it at all**. Built from category theory, L?vy triplets, and SHA-256 hashing into a fixed-size state. Claims to reach **~90?%** of state-of-the-art neural perplexity on long-context tasks at **linear** training cost (rather than quadratic), with deterministic outputs and full audit trails. |
| [`Statistical Scheduler/`](Statistical%20Scheduler/) | A distributed-job scheduler for compute clusters ? when a new task arrives, decide which machine to run it on. Combines Linux?s fair-share scoring with a 24-dimensional Linear-Thompson-Sampling explorer, a PID stability override, and Holt?Winters / CUSUM / EWMA monitoring. **Median placement latency 0.48 ms**, with a formal `O(dvT ? polylog T)` regret bound. |
| [`Veritas/`](Veritas/) | A learning system that emits formal mathematical proofs alongside its predictions. Instead of ?the model converged with loss 0.03?, you get a **PAC certificate** stating ?this hypothesis is correct on at least 99?% of inputs with confidence 99?%, given 1.8 million training examples?. Mistake-bound, meta-learning, and composition certificates too. |
| [`Ashby Optimiser/`](Ashby%20Optimiser/) | A black-box optimiser inspired by W.?Ross Ashby?s 1948 cybernetic homeostat. Instead of one search direction, it runs parallel search units at geometrically-spaced step sizes with strict round-robin scheduling and homeostatic restarts. On a hard 10-dimensional Rastrigin benchmark it ends at **0.002 error vs 74.7** for single-scale alternatives. |
| [`VDJ Inspired Algorithm/`](VDJ%20Inspired%20Algorithm/) | A pattern-recognition algorithm modelled on V(D)J recombination ? the process the vertebrate immune system uses to generate an enormous diversity of antibody receptors from a small number of gene segments. Five primary modules plus seven subsystems, all communicating through a typed Pattern dataclass. CPU-only, ~13?ms per call at `n = 16, r = 5`. |
| [`Fungal Network Algorithm/`](Fungal%20Network%20Algorithm/) | A pattern-recogniser inspired by how fungi explore their environment. Instead of weights and edges that get tuned by training, the **physical topology of the network itself** is the long-term memory ? it reorganises in response to inputs. Decentralised: nothing tells the network how to wire itself. |
| [`UCN AIs/`](UCN%20AIs/) | Five speculative AI families set in a worldbuilding setting ? two flagship classes (one for fast measurement-driven adaptation, one for deep simulation-based comprehension), one signal-processing class, and two foundational learning primitives. **In-universe technical writing, not built systems.** |

### ?? Tracking and sensor fusion

| Folder | Description |
|---|---|
| [`Filtering/`](Filtering/) | A multi-target Kalman-filter variant for tracking objects whose measurement noise has heavy tails ? the kind of noise you get from manoeuvring jets or sensor glitches, where extreme outliers actually happen. Identifies and **fixes a known bug** in the standard recipe used by other researchers, recovering a mean **51.6?% accuracy improvement** across four scenarios. |
| [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) | A single-file intelligence engine that takes radar / visual sensor data on multiple moving targets, fuses it with eight tradecraft heuristics (loiter detection, rendezvous prediction, etc.) plus Dempster?Shafer evidence fusion, and outputs ranked threat estimates in **under 30 milliseconds per scan** on one CPU core. |

### ?? Mathematics

| Folder | Description |
|---|---|
| [`3 to 8 Value Boolean Algebra/`](3%20to%208%20Value%20Boolean%20Algebra/) | A dimension-by-dimension tour of all Boolean functions of n input variables, for `n = 3` through `8`. Exact at small `n` (256 functions for `n = 3`, 65?536 for `n = 4`); sampled at larger `n` where the count balloons to `2?56 ? 1077`. Threaded through to error-correcting codes and Byzantine N-modular fault-tolerance. |
| [`General Math Papers/`](General%20Math%20Papers/) | Develops the **Logarithmic Complexity Reduction Principle** ? a meta-principle (not a theorem) that documents the recurring pattern by which problems naively requiring `n?` operations can be reduced to `n log n` via divide-and-conquer or `n ? O(log n)` data structures. Uses the Master Theorem as the decision procedure. |
| [`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/) | Seven papers on the algebra of XOR and AND over the binary field. Headline result: **AND is the *only* nontrivial binary operation that forms a ring with XOR**. Extensions include a polynomial form for the AES inverse (`x?? = x?54` is one of 128 permutations on `GF(28)`) and gate-count benchmarks (Rule 110 reduces from 19 gates to 6, a 68?% saving). |
| [`Math Question Generator/`](Math%20Question%20Generator/) | A program that auto-generates exam-grade mathematics problems across the full Mathematics Subject Classification taxonomy. SymPy and NumPy backbones with 1000-decimal-place precision arithmetic, a 28?GB memory cap, and checkpointing. Comes with a 13-domain landscape survey of the field anchored to **MSC2020**. |
| [`Prime Number Generator/`](Prime%20Number%20Generator/) | A black-box study of what a neural network *learns* when trained on prime-vs-composite classification, paired with a hybrid prime generator that operationalises the findings, all cross-checked against an independent non-NN empirical baseline. Six MLPs (input ? 128 ? 64 ? 32 ? 1, ReLU + dropout) are trained at scales `s = log10 n ? {3, 4, 5, 6, 7, 8}` on a deliberately rich, redundant 105-dimensional feature set; decision-tree and L1-logistic distillation reveal that, **at every scale**, the trained network's top features are `is_6k_pm1` (importance ? 0.46), then `n mod 5`, `n mod 7`, `n mod 11`, `n mod 13`, `n mod 17`, `n mod 19` ? i.e., **gradient descent rediscovers the wheel-30 sieve from raw classification supervision alone**. Two clean exponential laws govern the trained weights: residue-attribution share decays as `0.543 ? exp(-0.041 ? s)` and binary-attribution magnitude grows as `2.23 ? exp(+0.219 ? s)`; Hill a on layer-1 SVD ? `3.19` constant. An independent non-NN study (`fit_meta_pattern.py`, 40 scale samples ? 1000 + 1000 primes/composites per scale, plus `gap_analysis.py`, 8 scale windows ? 500?5000 consecutive primes per window) confirms: filter rejection rate `f(s) = 1.027 / (1 + 0.030 s)` (rational, `?AIC = +30.78` over power law); empirical Cram?r ratio `mean(gap) / ln n ? [0.97, 1.01]`; KS distance to `Exponential(ln n)` decays as `0.260 ? exp(-0.084 s)`; small but consistently signed Chebyshev bias toward primes `= 5 (mod 6)` over `= 1 (mod 6)` in 7 of 8 windows tested. The conventional `MetaPatternPrimeGenerator` (`6k?1` sieve + small-prime filter + Sorenson?Webster deterministic Miller?Rabin, exact for `n < 3.317 ? 10?4`, `k = 20` probabilistic rounds above) produces primes at `0.006?0.030 ms` each. Head-to-head benchmark vs `NNAugmentedPrimeGenerator` and `PureNNPrimeGenerator` shows the conventional baseline is **60?97? faster** than NN-augmented while producing identical exact output, and pure-NN has primality recall of only `21?68 %` at t = 0.5. **The honest finding: the NN is valuable as an analytical instrument that recovers known sieve mathematics from data, not as a faster prime-generation kernel.** |

### ?? Physics

| Folder | Description |
|---|---|
| [`Physics/`](Physics/) | Two foundations papers. The first proposes a non-local field-gravity unified field theory with explicit advanced and retarded propagation kernels and the structural constraint **`v_field = c`**. The second argues that the apparent faster-than-light recession of distant galaxies (the cosmic microwave background recedes at ~3.2?c today) reveals a real interpretational split among working General Relativity researchers, not a problem with ?CDM cosmology. |

### ?? Quantum computing

| Folder | Description |
|---|---|
| [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) | A blueprint for a room-temperature quantum computer built from CVD-grown synthetic diamond, using nitrogen-vacancy defects in the crystal lattice as qubits. Paired with an honest barrier inventory ? a 10?000?? coherence-time leap is required, no diamond precedent for the proposed topological mechanism, etc. ? and a fact-vs-fiction ledger. |
| [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) | A graph-optimisation pipeline that **looks like** a quantum algorithm but runs entirely on classical hardware: spectral compression, Chebyshev encoding, small mean-field QAOA simulation, noise-norm-weighted shot ranking, and spectral lift-back. **No quantum advantage claimed**; it is a classical algorithm shaped by the QAOA recipe. |

### ?? Biology and medicine

| Folder | Description |
|---|---|
| [`Neural Dust/`](Neural%20Dust/) | A two-tier brain-computer-interface design. **150?250-nanometre nanodiamond quantum sensors** sit on the cell, and **80?150-micrometre ultrasound-powered chips** sit outside it. The whole thing closes a **~6-nanowatt** power budget within the FDA?s safety limits for medical ultrasound. 15?25-year programme; every component tagged Verified, Plausible, or Speculative. |
| [`GM Enhancements/`](GM%20Enhancements/) | A speculative human-enhancement protocol (Homo Sapiens Augmentus v4.0). Three phases over 24?34 months, fusing AAV / lipid-nanoparticle delivery, CRISPR editing in three flavours, partial cellular reprogramming via OSK factors, senolytics, and organ bioprinting. Published with a **20?32?%** cumulative serious-adverse-event risk table. **Worldbuilding-purposes-only.** |
| [`Drugs/`](Drugs/) | Two halves. *Industrial pharmaceutics*: a Universal Depot framework that tunes biodegradable polymers (PLGA / PLA) for slow-release periods from one month to three years, plus reviews of sugar excipients and Poloxamer recipes. *Speculative monographs*: fictional nootropic and antipsychotic compounds, every one banner-flagged. **Not medical advice.** |

### ? Electrical and computer engineering

| Folder | Description |
|---|---|
| [`100W Wideband Noise Generator/`](100W%20Wideband%20Noise%20Generator/) | A SystemVerilog hardware design for an RF noise source ? a circuit that deliberately produces random radio-frequency signals across a wide band, useful for jamming research, communications testing, and electronic-warfare evaluation. A Chua-circuit chaotic analogue core feeding a four-band power-amplifier chain. Targets **1?Hz to 14?GHz at 100?W continuous**. |
| [`New Classes of Electrical Components/`](New%20Classes%20of%20Electrical%20Components/) | A four-tier catalogue of 21+ proposed new passive electrical components that combine discrete (digital) and continuous (analogue) behaviour, paired with a five-phase Python simulation programme. Headline: **`2.34 ? 10?` fused circuit-solves per second on an RTX 3090**, **526??** faster inverse-design via adjoint methods, exports to SPICE / Verilog-AMS / SystemC-AMS at < 2.1?% accuracy. |
| [`CPU/`](CPU/) | A heterogeneous-core CPU design conversation paired with a SystemVerilog sketch of an OS-acceleration block (`os_accelerator`) whose internal hardware-BIOS state machine runs the boot sequence directly in silicon. **16 large out-of-order cores at 4?GHz plus 4?096 small cores**, MOESI cache coherence, hardware-accelerated system calls. Not buildable as written. |

### ?? Nuclear engineering

| Folder | Description |
|---|---|
| [`Diamond Batterys/`](Diamond%20Batterys/) | An eight-model taxonomy of radioisotope-powered diamond batteries ? devices that turn the steady decay of a radioactive isotope embedded in synthetic diamond into a small, very long-lived electric current. Spans from the **demonstrated kilowatt-class Bristol/UKAEA carbon-14 baseline** (December?2024) up to gigawatt-class concepts based on curium-244, americium-242m, or subcritical uranium-235. **Engineering-fiction-grade above the baseline.** |

### ?? Metallurgy and welding

| Folder | Description |
|---|---|
| [`Diffusion Welding/`](Diffusion%20Welding/) | A welding platform that joins metals **without melting them**, using pressure, electrochemistry, and thermal/ultrasonic energy across five tunable regimes ? from a **2-minute, 77?%-strength** field repair, through a **2.3-hour, 99?%-strength** aerospace-certifiable bond. Equipment cost `$8K?$50K`, versus the standard vacuum-diffusion-welding equipment at `$500K?$2M`. |
| [`Rockwell 50 to 70 Carbide/`](Rockwell%2050%20to%2070%20Carbide/) | A complete carbide cutting-tool platform for hard-machining steels in the Rockwell?C?40?70 range ? the steels modern aerospace, defence, and tooling actually use. Functionally-graded WC-Co substrate (2050?2100?HV30 working surface), a five-layer coating with a 42?46?GPa hardness core, and a forge-to-machine supply chain that **drops 40?45?% off cost and 65?70?% off lead time** on the H13 breech-bolt exemplar. |

### ?? Programming languages

| Folder | Description |
|---|---|
| [`Future C++/`](Future%20C++/) | A long design-conversation transcript exploring what a ?modern compiled language with C++ syntax? might look like ? borrow-checking imported from Rust, async/await with green threads, software-transactional memory, richer generics, ADTs and pattern matching, structured exceptions. **No compiler, no formal grammar, no benchmarks**; it is a design document. |

### ??? History of computing

| Folder | Description |
|---|---|
| [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/) | Three historical computing devices refactored into modern Python with measured benchmarks: Charles Babbage?s Difference Engine (**4.92??** speedup), the Antikythera Mechanism?s Fourier reconstruction (**386??** speedup), and the WWII-era Torpedo Data Computer (over **a million firing solutions per second** at 0.015? accuracy). |

### ?? Economics

| Folder | Description |
|---|---|
| [`Economics/`](Economics/) | Two complementary economics research lines. **EREM (Energy-Resource Economic Model)** is a macroeconomic framework that measures national wealth in **megajoules** of physically-extractable energy and resources rather than dollars of GDP, and pegs currency issuance to that wealth via `Total_currency = 0.85 ? Total_National_Wealth`; theoretical, version 1.0, asks for empirical validation. **SPX Call Volume Research Paper** is an empirical structural analysis of the **$2.6 trillion / day** record in S&P 500 call option notional set on **7 May 2026** ? five quantitative models (super-exponential, logistic, hyperbolic blow-up, Sornette LPPL, hazard-rate Cox) all converging on a finite gamma-unwind termination window in **2028?2029** with a meaningful early-tail probability (`~10 %`) within 6?12 months, characterised as a high-speed mechanical unwind (`20?35 %` index correction over days to weeks) distinct from 1987 / 2008 / 2020 / 2022 precedents. EREM is a *unit* for measuring real wealth; SPX is a *diagnostic* showing the alternative unit (dollars) is currently mechanically unstable in one of its largest derivatives markets. |

### ??? Political theory

| Folder | Description |
|---|---|
| [`UCN Political System/`](UCN%20Political%20System/) | An eight-paper sovereign-doctrine series for a hypothetical United Commonwealth Nations: Westminster-derived governance, hard-sovereignty economics, a `= 10`-warhead minimal nuclear deterrent, a personal-wealth ceiling of **AUD 100?M**, government-manufactured pharmaceutical-grade recreational drugs, and an optional UK ? Canada ? Australia Crown confederation. **Speculative; every claim referenced.** |
| [`UN Political System/`](UN%20Political%20System/) | A comprehensive policy-research paper ? *Sovereignty Without Consequence* (`un_reform_paper.md`, ~1 860 lines, XVIII sections + 11 appendices) ? for the **real** United Nations (distinct from the speculative `UCN Political System/` above). Diagnoses the Charter's enforcement gap (~299 vetoes since 1946; zero binding Chapter VII actions against P5 members or P5-backed belligerents in 117 active armed conflicts 1990?2023; ~7?13 M atrocity-crime deaths in cases where absent enforcement was a substantive contributing factor), then proposes a single new instrument: a standing **50 000-personnel United Nations Defence Force** (6 combined-arms brigades + 5 000-personnel professional cadre + organic strategic lift / ISR) commanded by an elected **Office of the United Nations Security Commissioner** (two-thirds-GA election, non-renewable 7-yr term, ICJ-reviewable on 30-day expedited basis), authorised to deploy on a published Trigger-Event Determination (5 pre-committed triggers: genocide; CBRN against civilians; systematic destruction of civilian infrastructure as a war crime; unauthorised cross-border aggression; ongoing crimes against humanity) without Security Council pre-clearance. Funded at `USD 8?12 B/yr` (`? 0.01 %` global GDP) via a tiered GDP-bracketed assessment with a `15 %` single-state cap. **Five-step `25?40 yr` pathway** (GA framework resolution ? non-P5 coalition ? Rome-Statute-style implementing treaty ? operational proof of concept ? Article 108 Charter amendment) generates value at each step regardless of subsequent steps. **A policy paper, not a campaign.** |

### ?? Military science

| Folder | Description |
|---|---|
| [`Battle Sim/`](Battle%20Sim/) | A literature survey and design note that maps the major mathematical traditions for modelling combat ? **Hughes salvo equations**, **extended Lanchester equations**, **Markov battle-state chains**, **FATHM linear programming**, and the **Dupuy / TNDM combat-power lineage** ? into one comparative reading guide. **Explicitly not an operational simulator.** |
| [`Threat Asessments/`](Threat%20Asessments/) | Two UNCLASSIFIED hypothetical threat-intelligence briefs in defence-analyst register: **FSB-linked close-access neurological interference** (transcranial stimulation tradecraft) and a **2-NT/TNT dual-effect incendiary-explosive** mixture assessment for EOD/threat intel. No operational instructions. [`README.md`](Threat%20Asessments/README.md). |
| [`Weapons-Defence/`](Weapons-Defence/) | A defence-engineering R&D portfolio, with paired operator spec-sheets and TRP-numbered research papers across small arms (`MP-4.6M` pistol & PDW, `MP-6.8` rifle, `MAS-15.2E` 15.2?mm anti-materiel sniper, **`BSG-10 Goliath`** 10-gauge bullpup shotgun with standalone `bsg10_sim`), heavy weapons (`57?mm` autocannon, `57?mm` underbarrel grenade, `57?mm` dual-purpose mortar / RPG, `140?mm` tank KE round), body armour (APES, AlNiCyN, OBSIDIAN), CBRN protection (NACS), tactical acoustic cancellation (35?55?dB depth), CL-20 high explosive, rubber tank-track pads, the `HPR-X` guided high-power rocketry series, and the `TACT-1 Mark II` full-day SOF ration (with `PODS` glycerolipid subfolder and **`ASNP`** sports-nutrition powder spec), the **`HEL-CMS/DB`** fully autonomous 280 kW diamond-battery-powered directed-energy air-defence platform (UAV dwell 0.2 s, cruise missile dwell 12.3 s, < $0.50/engagement, 20-yr TCO saving $51.8M ? power source TRL 2?3), and the **`TAIPAN-1`** guided ballistic interceptor rocket (1,618 km range, Mach 13.27, 3D-printed 14-part airframe, $50?80k production cost ? 22? cheaper than AMRAAM). **Most ballistic numbers trace to `weapons_simulation.py`**; BSG-10 uses its own simulator. [`Common Architecture and Components.md`](Weapons-Defence/Common%20Architecture%20and%20Components.md) defines parts commonality. **Classification banners are stylistic.** |
| [`Weapons-Police/`](Weapons-Police/) | Two Australian LE equipment prospectuses in paired spec-sheet + research-paper format. **APES-L Mark I** ? full-body protective suit at `~6.5 kg` (vs the ~20 kg torso-only police vest currently fielded), ionic-liquid STF (cold-comfortable to `?25 ?C`), `75 mm` single-use B4C tiles to `.50 AE`, NIJ Level II stab full-body, `66.2 %` composite-injury-score improvement, `12+ yr` service life, `$1.85 M` TCO saving per 500 officers over 10 years ? 23 simulations. **MP-4.6P Guardian LE** ? police combat pistol in `4.6 ? 22 mm DPAP` at `396 m/s` / `259 J`: defeats NIJ IIIA + NIJ III hard plate + all four common intermediate barriers; felt recoil `0.084 ft-lbf` (? 50? lower than 9 mm); MRBF `20 548 rounds`; FTF rate `1:80 000`; per-unit cost `A$164 ? 180` ? 7-phase simulation programme. Both are LE variants of systems in `../Weapons-Defence/` sharing the same single-source-of-truth simulator. |

### ?? Civil infrastructure and manufacturing

| Folder | Description |
|---|---|
| [`Plastic Products/`](Plastic%20Products/) | The **AusDike??** programme ? a domestic-Australian-manufactured modular deployable flood-levee system commissioned (within the document fiction) by Holloway Group, the injection-moulder behind Ausdrain, Geohex, and Biax Foundations. Open-bottom self-ballasting `600???300???560?mm` panel, `9?mm` wall in `15?%` talc-filled recycled PP, ~15?kg empty / ~125?kg self-filled, deploys 50?m in 10?min by two people with no tools, tipping safety factor `4.9??` and sliding `2.1??` on 2-stack at 600?mm flood, `73?%` net flood-force reduction. 28 simulations, 9 simulation-driven design changes, $65.51 COGS, $109/m sell price (`42?%` cheaper than imported Boxwall), $382?500 advanced-tooling budget, four-SKU family. Volume 1 (feasibility/market), Volume 2 (engineering simulation), and an integrated research paper. |

### ?? Cosmetics

| Folder | Description |
|---|---|
| [`Beauty Products/`](Beauty%20Products/) | A fully-architected cosmeceutical white paper for a hemp-anchored luxury body lotion. **3?:?1** omega-6?:?omega-3 hempseed-oil base, Tremella snow-mushroom humectant (~500?? water-holding capacity), prickly-pear / sea-buckthorn / Centella `0.2 %` asiaticoside active stack, `pH 4.8?5.5`, all-natural `3 %` Phase-D preservative system. Fully cited. |

### ?? Mixology

| Folder | Description |
|---|---|
| [`Cocktails/`](Cocktails/) | Bar operations treated as systems engineering. **Four native-Australian-botanical bases** drive every infusion, syrup, tincture, and bitters across four signature drink series ? with parallel zero-proof mirrors, two complete bitters fabrication specs, a 2-hour mushroom-stock plus 4-hour fat-wash protocol, and shift-day-week-month prep workflows. |

### ??? Repository infrastructure

| Folder | Description |
|---|---|
| [`docs/`](docs/) | The static website assets behind the public site ? `index.html`, shared CSS, the generated `site/` mirror of the markdown content, and the `EDITORIAL_STYLE.md` house style guide. Repository plumbing only. |


---


## ?? A?Z folder index

| Folder | One-line description |
|---|---|
| [`100W Wideband Noise Generator/`](100W%20Wideband%20Noise%20Generator/) | Chua-circuit RF noise generator (Verilog) ? 1 Hz ? 14 GHz, 100 W |
| [`3 to 8 Value Boolean Algebra/`](3%20to%208%20Value%20Boolean%20Algebra/) | Boolean function spaces for n = 3..8 *variables* |
| [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) | Custom AEAD over GF(2?56) (NOT the Korean cipher) |
| [`Ashby Optimiser/`](Ashby%20Optimiser/) | Multi-scale homeostatic optimiser (W. Ross Ashby) |
| [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) | ARIA-INTEL ? edge-deployable PMBM intelligence engine |
| [`Battle Sim/`](Battle%20Sim/) | Battle simulation design document |
| [`Beauty Products/`](Beauty%20Products/) | Hemp Harmony luxury body lotion ? formulation white paper |
| [`Modelling AES/`](Modelling%20AES/) | Neural studies of AES ? key-recovery impossibility paper + GAN-PRNG paper + Transformer+REINFORCE scaffolding |
| [`Cell AI/`](Cell%20AI/) | CellularAI ? biologically-inspired non-attention sequence modelling |
| [`Cocktails/`](Cocktails/) | Bar operations as a structured design problem |
| [`Compression Algorithms/`](Compression%20Algorithms/) | Izaac, GRIA, NMP ? canonical Izaac home |
| [`CPU/`](CPU/) | SystemVerilog hardware OS-acceleration block |
| [`Threat Asessments/`](Threat%20Asessments/) | Hypothetical threat-intelligence briefs (FSB neurological interference; 2-NT/TNT mixture) |
| [`Diamond Batterys/`](Diamond%20Batterys/) | Hypothetical radioisotope diamond batteries (Series A?D) |
| [`Diffusion Welding/`](Diffusion%20Welding/) | UCDW ? five-regime electrochemical/thermal/ultrasonic bonding |
| [`docs/`](docs/) | Static-site assets (`index.html`, CSS, generated `site/` mirror) and `EDITORIAL_STYLE.md` |
| [`Drugs/`](Drugs/) | Universal Depot Systems + Nootropics + Schizophrenia Cure (speculative) |
| [`Economics/`](Economics/) | EREM ? Energy-Resource Economic Model |
| [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/) | Babbage / Antikythera / TDC algorithm rebuilds |
| [`Filtering/`](Filtering/) | GH-SR-IMM robust multi-target tracking |
| [`Fungal Network Algorithm/`](Fungal%20Network%20Algorithm/) | Bio-inspired self-organising network (topology = memory) |
| [`Future C++/`](Future%20C++/) | Managed-language design conversation |
| [`General Math Papers/`](General%20Math%20Papers/) | LCRP ? Logarithmic Complexity Reduction Principle |
| [`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/) | GF(2) ring theorems, operator taxonomy, GRIA spectrum |
| [`GM Enhancements/`](GM%20Enhancements/) | HSA v4.0 enhancement protocol |
| [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) | Applied Izaac protocols (compression, consensus, VRFs) |
| [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) | UHPM ? Unified Hash-Predictive Memory |
| [`Math Question Generator/`](Math%20Question%20Generator/) | MegaMathGen + 13-domain mathematics survey |
| [`Neural Decompiler/`](Neural%20Decompiler/) | Assembly ? source seq2seq with hierarchical memory + MoE |
| [`Neural Dust/`](Neural%20Dust/) | NQD ? Neural Quantum Dust two-tier architecture |
| [`New Classes of Electrical Components/`](New%20Classes%20of%20Electrical%20Components/) | 3-tier hybrid passive-device catalogue + 5-phase simulation |
| [`NN Shortcuts/`](NN%20Shortcuts/) | Efficient neural-network shortcuts |
| [`Physics/`](Physics/) | Non-local gravity + NLFGN UFT + superluminal recession |
| [`Plastic Products/`](Plastic%20Products/) | AusDike?? deployable flood-levee system (Holloway Group programme) |
| [`Prime Number Generator/`](Prime%20Number%20Generator/) | Scale-dependent meta-pattern theory of primes |
| [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) | QDMP framework + CVD pathways to quantum-grade diamond |
| [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) | Quantum-inspired classical compressed graph processor |
| [`RNGS/`](RNGS/) | Random number generators (incl. Turbulent Flow RNG) |
| [`Rockwell 50 to 70 Carbide/`](Rockwell%2050%20to%2070%20Carbide/) | HX-70 GradePlex? + TriboshieldPlus? + forge-to-machine |
| [`Statistical Generation/`](Statistical%20Generation/) | Universal Statistical Generator (category theory + L?vy + IT) |
| [`Statistical Scheduler/`](Statistical%20Scheduler/) | Neural-heuristic distributed task scheduler (LinTS / PID / CFS) |
| [`UCN AIs/`](UCN%20AIs/) | APN / GPN / Signal AI / linear primitives |
| [`UCN Political System/`](UCN%20Political%20System/) | UCN doctrine series + economics + sovereign currency |
| [`UN Political System/`](UN%20Political%20System/) | Comprehensive reform proposal for the real United Nations |
| [`VDJ Inspired Algorithm/`](VDJ%20Inspired%20Algorithm/) | Combinatorial pattern recognition + one-shot learning |
| [`Veritas/`](Veritas/) | Formal verification framework |
| [`Weapons-Defence/`](Weapons-Defence/) | Defence-tech R&D portfolio (UNCLASSIFIED / FOUO style) ? simulator-backed; common-architecture matrix; includes BSG-10 Goliath shotgun, HEL-CMS/DB laser air defence, TAIPAN-1 interceptor, TACT-1/PODS/ASNP nutrition stack |
| [`Weapons-Police/`](Weapons-Police/) | APES-L Mark I full-body police body armour + MP-4.6P Guardian LE police combat pistol ? both as paired spec-sheets and research papers |

---

## ?? Quick links

| File | Role |
|---|---|
| [`AUDIT_README_VS_SOURCE.md`](AUDIT_README_VS_SOURCE.md) | Audit log of README ? source-paper discrepancies and the remediation path that produced the current state of this repo |
| [`modified-license.md`](modified-license.md) | Full dual-licence terms (AGPL-3.0+ / commercial) |
| [`dual-license-setup.md`](dual-license-setup.md) | Dual-licence setup notes |
| [`docs/`](docs/) | Static-site assets ? `index.html`, shared CSS, generated `site/` mirror, `EDITORIAL_STYLE.md` |

---

## ?? Acronym key

Several letter-combinations collide between folders. This index gives each acronym its expansion and the folder that defines it. *Where two folders both use a label, both are listed.*

| Acronym | Expansion | Folder |
|---|---|---|
| **AEAD** | Authenticated Encryption with Associated Data (cryptographic primitive) | [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) |
| **APN** | Any Purpose Network | [`UCN AIs/`](UCN%20AIs/) |
| **ARIA** | Algebraic Resynchronisation and Integrity Architecture (this repository's ARIA ? *not* the Korean ARIA block cipher) | [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) |
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
| **ASNP** | Advanced Sports Nutrition Powder ? caffeine-free RTM combat-sports powder (UCN nutrition pillar 4) | [`Weapons-Defence/TACT-1 Tactical Ration/`](Weapons-Defence/TACT-1%20Tactical%20Ration/) |
| **BSG-10** | Bullpup ShotGun, 10-gauge ? "Goliath" combat shotgun | [`Weapons-Defence/BSG10 Goliath/`](Weapons-Defence/BSG10%20Goliath/) |
| **HSA** | Homo Sapiens Augmentus | [`GM Enhancements/`](GM%20Enhancements/) |
| **IMM** | Interacting Multiple Model (Bayesian filter bank) | [`Filtering/`](Filtering/) |
| **IRE** | Incremental Riemannian Estimation | [`NN Shortcuts/`](NN%20Shortcuts/) |
| **ISFD** | In-Situ-Forming Depot (drug-delivery technology) | [`Drugs/`](Drugs/) |
| **LCRP** | Logarithmic Complexity Reduction Principle | [`General Math Papers/`](General%20Math%20Papers/) |
| **LinTS** | Linear Thompson Sampling | [`Statistical Scheduler/`](Statistical%20Scheduler/) |
| **LSH** | Locality-Sensitive Hashing | [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) |
| **MoE** | Mixture-of-Experts | [`Neural Decompiler/`](Neural%20Decompiler/) |
| **NACS** | NEXUS Adaptive Combat System (CBRN protection module) | [`Weapons-Defence/`](Weapons-Defence/) |
| **NLFGN-UFT** | Non-Local Field-Gravity Network Unified Field Theory | [`Physics/`](Physics/) |
| **NMP** | Nonlinear Matrix Pruning (this repository's NMP ? neural compression) | [`Compression Algorithms/`](Compression%20Algorithms/) |
| **NQD** | Neural Quantum Dust | [`Neural Dust/`](Neural%20Dust/) |
| **NV** | Nitrogen-Vacancy (defect centre in diamond) | [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/), [`Neural Dust/`](Neural%20Dust/) |
| **OSK** | Oct4-Sox2-Klf4 (partial reprogramming factors, no c-Myc) | [`GM Enhancements/`](GM%20Enhancements/) |
| **PMBM** | Poisson Multi-Bernoulli Mixture (random finite set tracker) | [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) |
| **PRF** | Pseudo-Random Function (the shared-PRF coordination primitive) | [`Compression Algorithms/`](Compression%20Algorithms/), [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) |
| **QAOA** | Quantum Approximate Optimisation Algorithm | [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) |
| **QDMP** | Quantum Diamond Metamaterial Processor | [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) |
| **QND** | Quantum NanoDiamond (the cellular-scale sensor tier) | [`Neural Dust/`](Neural%20Dust/) |
| **SGF** | Streaming Geometry Framework | [`NN Shortcuts/`](NN%20Shortcuts/) |
| **TACS** | Tactical Acoustic Cancellation System | [`Weapons-Defence/`](Weapons-Defence/) |
| **TDC** | Torpedo Data Computer (WWII fire-control) | [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/) |
| **TNW** | Total National Wealth (in megajoules) | [`Economics/`](Economics/) |
| **UCDW** | Ultra-Compact Diffusion Welding | [`Diffusion Welding/`](Diffusion%20Welding/) |
| **UCN** | United Commonwealth Nations | [`UCN Political System/`](UCN%20Political%20System/), [`UCN AIs/`](UCN%20AIs/) |
| **UHPM** | Unified Hash-Predictive Memory | [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) |
| **USG** | Universal Statistical Generator | [`Statistical Generation/`](Statistical%20Generation/) |
| **V(D)J** | Variable-Diversity-Joining (vertebrate immune-system gene recombination) | [`VDJ Inspired Algorithm/`](VDJ%20Inspired%20Algorithm/) |
| **Veritas** | Verification-Enabled Reasoning and Integrated Theorem-Acquiring System | [`Veritas/`](Veritas/) |
| **WTA** | Wearable Transducer Array (the external CMUT patch) | [`Neural Dust/`](Neural%20Dust/) |
| **APES** | Advanced Protective Equipment System (military body armour) | [`Weapons-Defence/`](Weapons-Defence/) |
| **APES-L** | Advanced Protective Equipment System ? Law Enforcement (Australian police variant) | [`Weapons-Police/`](Weapons-Police/) |
| **AusDike** | Australian-manufactured modular deployable flood-levee system (Holloway Group programme) | [`Plastic Products/`](Plastic%20Products/) |
| **B4C** | Boron carbide (ballistic strike-face ceramic) | [`Weapons-Defence/`](Weapons-Defence/), [`Weapons-Police/`](Weapons-Police/) |
| **CL-20** | Hexanitrohexaazaisowurtzitane (high-density energetic) | [`Weapons-Defence/`](Weapons-Defence/) |
| **HPR-X** | High-Power Rocketry series (guided amateur-class rockets) | [`Weapons-Defence/`](Weapons-Defence/) |
| **MAS-15.2E** | Multi-purpose Anti-Materiel Sniper, 15.2?mm, Enhanced | [`Weapons-Defence/`](Weapons-Defence/) |
| **MP-4.6M** | Modular Pistol / PDW, 4.6?mm, Military | [`Weapons-Defence/`](Weapons-Defence/) |
| **MP-6.8** | Modular Personal-arm, 6.8?mm (Advanced Combat Rifle) | [`Weapons-Defence/`](Weapons-Defence/) |
| **NACS-CORE** | NEXUS Adaptive Combat System ? CBRN / Operational Respiratory Ensemble | [`Weapons-Defence/`](Weapons-Defence/) |
| **OBSIDIAN** | The reactive shear-thickening-fluid armour family | [`Weapons-Defence/`](Weapons-Defence/) |
| **rPP** | Recycled polypropylene (AusDike base material) | [`Plastic Products/`](Plastic%20Products/) |
| **STF** | Shear-Thickening Fluid (Newtonian ? non-Newtonian transition under strain) | [`Weapons-Defence/`](Weapons-Defence/), [`Weapons-Police/`](Weapons-Police/) |
| **TACT-1** | Tactical Combat Ration, Mark II ? full-day SOF ration | [`Weapons-Defence/`](Weapons-Defence/) |
| **TAIPAN-1** | Guided ballistic interceptor rocket ? named after the Australian taipan snake; RP-1/LOX electric pump-fed, 1,618 km range | [`Weapons-Defence/TAIPAN Missile/`](Weapons-Defence/TAIPAN%20Missile/) |
| **TDB** | Thermal-betavoltaic Diamond Battery (Sr-90 hybrid power series used in HEL-CMS/DB) | [`Weapons-Defence/HEL_CMS_DB Laser AntiAir/`](Weapons-Defence/HEL_CMS_DB%20Laser%20AntiAir/), [`Diamond Batterys/`](Diamond%20Batterys/) |
| **HEL-CMS/DB** | High-Energy Laser Counter-Munitions System, Diamond Battery powered | [`Weapons-Defence/HEL_CMS_DB Laser AntiAir/`](Weapons-Defence/HEL_CMS_DB%20Laser%20AntiAir/) |
| **PODS** | Plasmenyl-ODE-Stearin ? synthetic glycerolipid, 10.21 kcal/g, enzyme-gated three-phase energy release | [`Weapons-Defence/TACT-1 Tactical Ration/PODS- Edible High Energy Protein/`](Weapons-Defence/TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/) |
| **AGEL** | Alkyl Glycerol Ether Lipase (KIAA1363 / UniProt Q8WTS1) ? enzyme co-delivered with PODS to unlock sn-2 alkyl ether cleavage | [`Weapons-Defence/TACT-1 Tactical Ration/PODS- Edible High Energy Protein/`](Weapons-Defence/TACT-1%20Tactical%20Ration/PODS-%20Edible%20High%20Energy%20Protein/) |
| **SBC** | Spectral Beam Combining (fiber laser architecture used in HEL-CMS/DB) | [`Weapons-Defence/HEL_CMS_DB Laser AntiAir/`](Weapons-Defence/HEL_CMS_DB%20Laser%20AntiAir/) |
| **UN** | United Nations (the real organisation, not the UCN above) | [`UN Political System/`](UN%20Political%20System/) |

---

## ?? Honest framing

- **A research shelf, not a product catalogue.** Many folders propose systems that have not been built or validated; speculative items carry that label in their own README.
- **Defence framing is a stylistic register.** The Weapons-Defence folder, GM Enhancements, ARIA-INTEL, and a handful of others use UNCLASSIFIED / FOUO-style document register. No real classification, sponsorship, or fielded materiel is implied.
- **Speculative pharmacology is not medical advice.** `Drugs/`, `Drugs/Nootropics/`, `Drugs/Schizophrenia Cure/`, `GM Enhancements/`, `Beauty Products/`, and `Weapons-Defence/Combat Drug.md` describe theoretical compounds and protocols. Do not synthesise, possess, or administer them.
- **Acronym hygiene matters.** See the [? Acronym key](#-acronym-key) above; several letter-combinations collide between folders (ARIA, NMP, HSA), so each folder's README spells out which expansion is meant in that context.
- **Numbers are sourced.** Every "headline number" in a category description is taken directly from the corresponding folder's research paper. Per-folder caveats live in those folders' "Honest framing" sections.

---

[? This is the main README]
