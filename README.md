# Ideas — Odin Loch's R&D shelf

> **Forty-five folders of research, design specs, and speculative work, written like internal R&D documents.** Cryptography, neural architectures, materials science, physics, economics, defence-tech, and a smaller fiction layer (cocktails, beauty, worldbuilding). Most folders ship at least one long-form research document; many ship working code; speculative items are flagged in their own README.

---

## ⚖️ Licensing

Dual-licensed:

1. **GNU Affero General Public License v3.0+ (AGPL-3.0+)** — free tier for personal use, charity, education, and entities with annual income < AUD 50 000.
2. **Tiered commercial licence** — for commercial use above the free-tier threshold.

See [`modified-license.md`](modified-license.md) for full terms and [`dual-license-setup.md`](dual-license-setup.md) for setup notes.

**Attribution under AGPL-3.0+:**

> "Powered by Ideas, developed by Odin Loch. Licensed under AGPL-3.0+. www.odinloch.com.au"

Modifications must be shared back under the same dual-licence; research using this software must be open-sourced. Commercial licensees: no requirement to share modifications.

**Commercial enquiries:** odin.loch@outlook.com.au

---

## 🗂 How to navigate

The repository is organised as one folder per topic, browsable in any order. Each folder has its own README that describes what the folder actually contains, lists the source documents, and links related work elsewhere in the repo.

You can read this index three ways:

1. **By category** ([§ Categories](#-categories)) — six themed groupings.
2. **A–Z** ([§ A–Z folder index](#-az-folder-index)) — alphabetical with one-line descriptions.
3. **Navigation aids** ([§ Quick links](#-quick-links)) — repo-level files (audit trail, licence, etc.).

---

## 📚 Categories

### 🤖 Algorithms, learning, and AI

| Folder | Description |
|---|---|
| [`Cell AI/`](Cell%20AI/) | CellularAI — biologically-inspired non-attention sequence modelling (CellularPDE, Hebbian plasticity, MultiModalModel; v1/v2/v3) |
| [`Cypha/`](Cypha/) | HRNA inference, training, and tooling (Python core + parity-validated native C++ + REST + Studio GUI) |
| [`Long Reasoning and Thinking NN/`](Long%20Reasoning%20and%20Thinking%20NN/) | UHPM = Unified Hash-Predictive Memory — long-context LSH + predictive coding under one free-energy functional |
| [`Neural Decompiler/`](Neural%20Decompiler/) | Assembly → source seq2seq with hierarchical memory and Mixture-of-Experts |
| [`NN Shortcuts/`](NN%20Shortcuts/) | Efficient neural-network shortcuts |
| [`Asset Tracking Algorithm/`](Asset%20Tracking%20Algorithm/) | ARIA-INTEL = Algebraic Rendezvous & Intelligence Analyser — edge-deployable PMBM filter, 28 ms scan latency |
| [`Filtering/`](Filtering/) | GH-SR-IMM — Generalised Hyperbolic Square-Root Interacting-Multiple-Model robust multi-target tracker; GH-JPDA extension |
| [`Statistical Scheduler/`](Statistical%20Scheduler/) | Neural-heuristic distributed task scheduler (LinTS / PID / CFS) |
| [`Statistical Generation/`](Statistical%20Generation/) | Universal Statistical Generator — category theory + Lévy triplets + information-theoretic filtration |
| [`VDJ Inspired Algorithm/`](VDJ%20Inspired%20Algorithm/) | Combinatorial pattern recognition + one-shot learning (5 modules + 7 subsystems; 13 ms at n=16, r=5) |
| [`Fungal Network Algorithm/`](Fungal%20Network%20Algorithm/) | Pattern recognition by physical network reorganisation (no central control) |
| [`Ashby Optimiser/`](Ashby%20Optimiser/) | Multi-scale homeostatic optimiser (W. Ross Ashby's 1948 homeostat reframed) |
| [`UCN AIs/`](UCN%20AIs/) | APN, GPN, Signal AI, linear-congruent / linear-gradient-descent primitives (UCN universe) |

### 🔐 Cryptography and verification

| Folder | Description |
|---|---|
| [`ARIA Encryption Algorithm/`](ARIA%20Encryption%20Algorithm/) | Custom AEAD over GF(2²⁵⁶) — *not* the Korean ARIA block cipher; the local ARIA = Algebraic Resynchronisation and Integrity Architecture |
| [`Break AES/`](Break%20AES/) | Transformer + RL distillation for AES cryptanalysis research |
| [`Compression Algorithms/`](Compression%20Algorithms/) | Izaac, GRIA (Graded Reversible-Irreversible Algebra), NMP (Nonlinear Manifold Projection) — canonical home of the Izaac framework |
| [`Izaac as Side Data/`](Izaac%20as%20Side%20Data/) | Applied Izaac protocols — shared deterministic randomness as side information |
| [`Veritas/`](Veritas/) | Verification-Enabled Reasoning and Integrated Theorem-Acquiring System |
| [`RNGS/`](RNGS/) | Random number generators including Turbulent Flow RNG |

### 📐 Mathematics and logic

| Folder | Description |
|---|---|
| [`3 to 8 Value Boolean Algebra/`](3%20to%208%20Value%20Boolean%20Algebra/) | Boolean function spaces $f:\\{0,1\\}^n\\to\\{0,1\\}$ for $n=3..8$ — dimensional emergence, bent functions, QEC, Byzantine NMR |
| [`General Math Papers/`](General%20Math%20Papers/) | LCRP — Logarithmic Complexity Reduction Principle |
| [`GF2 Algebra and Applications/`](GF2%20Algebra%20and%20Applications/) | GF(2) Ring Uniqueness Theorem, 16-operator taxonomy, GRIA Spectrum Theorem |
| [`Math Question Generator/`](Math%20Question%20Generator/) | MegaMathGen — sympy-based continuous problem generator; 13-domain landscape survey |
| [`Prime Number Generator/`](Prime%20Number%20Generator/) | Scale-dependent meta-pattern theory; power law $\alpha(s) = s^{-0.37}$; critical transition |

### 🔩 Hardware, materials, and process science

| Folder | Description |
|---|---|
| [`100W Wideband Noise Generator/`](100W%20Wideband%20Noise%20Generator/) | Chua-circuit RF noise generator under FPGA supervision; 1 Hz – 14 GHz, 100 W |
| [`CPU/`](CPU/) | SystemVerilog hardware OS-acceleration block (`os_accelerator` + inner `hardware_bios`) |
| [`Diamond Batterys/`](Diamond%20Batterys/) | Hypothetical radioisotope diamond batteries (Series A–D; C-14, Am-241, Pu-238, Sr-90) — speculative |
| [`Diffusion Welding/`](Diffusion%20Welding/) | UCDW — Ultra-Compact Diffusion Welding; 5 regimes from 2-min field repair (77 %) to 99 % aerospace-certified |
| [`Electromechnical Inspired Algorithms/`](Electromechnical%20Inspired%20Algorithms/) | Babbage Difference Engine, Antikythera ("military"), Torpedo Data Computer — three triplets (paper + companion doc + Python) |
| [`Future C++/`](Future%20C++/) | Design conversation: managed compiled language with C++ syntax, Rust-style ownership, async + green threads |
| [`New Classes of Electrical Components/`](New%20Classes%20of%20Electrical%20Components/) | 3-tier hybrid passive-device catalogue + 5-phase simulation programme |
| [`Rockwell 50 to 70 Carbide/`](Rockwell%2050%20to%2070%20Carbide/) | HX-70 GradePlex™ sintered carbide for hard machining (HRC 40 – 70) + TriboshieldPlus™ coating + forge-to-machine |

### 🌌 Physics, quantum, and biomedical

| Folder | Description |
|---|---|
| [`Physics/`](Physics/) | Non-local field theory; NLFGN UFT; superluminal-recession cosmology |
| [`Quantum Diamond Wafer/`](Quantum%20Diamond%20Wafer/) | QDMP — Quantum Diamond Metamaterial Processor; CVD-diamond pathways for sensing and computing |
| [`Quantum Graph Optimisation/`](Quantum%20Graph%20Optimisation/) | Quantum-inspired classical pipeline: spectral compression → Chebyshev → classical QAOA simulation → noise-side-data ranking → spectral lift-back |
| [`Neural Dust/`](Neural%20Dust/) | NQD — Neural Quantum Dust two-tier architecture (QND / APEX / WTA) |
| [`GM Enhancements/`](GM%20Enhancements/) | HSA v4.0 — Homo Sapiens Augmentus; three-phase 24–34 month enhancement protocol |
| [`Drugs/`](Drugs/) | Universal Depot Systems framework + Nootropics + speculative schizophrenia therapeutics — speculative, not medical advice |

### 💰 Economics, civics, defence, and creative

| Folder | Description |
|---|---|
| [`Economics/`](Economics/) | EREM — Energy-Resource Economic Model (canonical) |
| [`UCN Political System/`](UCN%20Political%20System/) | UCN doctrine series: 8 numbered papers + economics + sovereign digital currency + constitutional-architecture analysis |
| [`Battle Sim/`](Battle%20Sim/) | Battle simulation design |
| [`Weapons/`](Weapons/) | Defence-tech R&D portfolio: small-arms, anti-materiel platforms, body armour, NACS, TACS, OBSIDIAN-X, AlNiCyN armour (UNCLASSIFIED / FOUO style) |
| [`Beauty Products/`](Beauty%20Products/) | Hemp Harmony luxury body lotion (formulation white paper) |
| [`Cocktails/`](Cocktails/) | Bar operations as a structured design problem (menus, prep workflows, mixology systems) |

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

## 🛡 Honest framing

- **A research shelf, not a product catalogue.** Many folders propose systems that have not been built or validated; speculative items carry that label in their own README.
- **Defence framing is a stylistic register.** The Weapons folder, GM Enhancements, ARIA-INTEL, and a handful of others use UNCLASSIFIED / FOUO-style document register. No real classification, sponsorship, or fielded materiel is implied.
- **Speculative pharmacology is not medical advice.** `Drugs/`, `Drugs/Nootropics/`, `Drugs/Schizophrenia Cure/`, `GM Enhancements/`, `Beauty Products/`, and `Weapons/Combat Drug.md` describe theoretical compounds and protocols. Do not synthesise, possess, or administer them.
- **Acronym hygiene matters.** Several letter-combinations collide between folders (ARIA, NMP, HSA, etc.). Each folder's README spells out which expansion is meant in that context.

---

[← This is the main README]
