# RNGS — random number generator zoo

> **Four RNG families across four subfolders.** Each subfolder ships a paper-and-implementation pair (sometimes more): Boolean / Transcendental LCG, Chaotic SynerChaos, DAG / Meta-DAG, and TurbulentFlow. Every generator has its own statistical-quality story — no central thesis is asserted; the folder is genuinely a *zoo* of approaches.

---

## 🎲 What this folder is

A grouping of distinct RNG research projects, each in its own subfolder, plus this index.

---

## 📁 Subfolders

### Boolean / Transcendental LCG

| File | Role |
|---|---|
| [`Boolean RNG/Transcendental_LCG_Theory_Paper.md`](Boolean%20RNG/Transcendental_LCG_Theory_Paper.md) | **The optimised 256-bit transcendental Boolean LCG (OTB-LCG)** — Hull–Dobell maximum-period LCG over $2^{256}$ state, XOR-based Boolean parity functions for parameter generation (eliminates the 22.66 % naive-LCG bias), multi-source hardware entropy harvesting, Von-Neumann bias correction, SHA-256 post-processing. NIST SP 800-22 Rev. 1a passage rates > 99 %. |
| [`Boolean RNG/Transcendental_LCG_Implementation_Paper.md`](Boolean%20RNG/Transcendental_LCG_Implementation_Paper.md) | Implementation companion to the theory paper |
| [`Boolean RNG/optimized_transcendental_lcg_spec.md`](Boolean%20RNG/optimized_transcendental_lcg_spec.md) | Optimised reference specification |
| [`Boolean RNG/transcendental_lcg_python.py`](Boolean%20RNG/transcendental_lcg_python.py) | Python implementation |

### Chaotic / SynerChaos

| File | Role |
|---|---|
| [`Chaotic RNG/synerchaos_research_paper.md`](Chaotic%20RNG/synerchaos_research_paper.md) | SynerChaos research paper |
| [`Chaotic RNG/chaos_readme.md`](Chaotic%20RNG/chaos_readme.md) | Chaos-based RNG overview |
| [`Chaotic RNG/chaos_python.py`](Chaotic%20RNG/chaos_python.py) | Python implementation |
| [`Chaotic RNG/chaos_rng.c`](Chaotic%20RNG/chaos_rng.c) | C implementation |

### DAG / Meta-DAG

| File | Role |
|---|---|
| [`DAG RNG/Meta_DAG_RNG_Research_Paper.md`](DAG%20RNG/Meta_DAG_RNG_Research_Paper.md) | Meta-DAG RNG research paper |
| [`DAG RNG/DAG RNG Intro.md`](DAG%20RNG/DAG%20RNG%20Intro.md) | Conceptual introduction |
| [`DAG RNG/DAG RNG Math Model.md`](DAG%20RNG/DAG%20RNG%20Math%20Model.md) | Mathematical model |
| [`DAG RNG/DAG RNG.py`](DAG%20RNG/DAG%20RNG.py) | Python implementation |

### Turbulent Flow

| File | Role |
|---|---|
| [`Turbulent Flow RNG/`](Turbulent%20Flow%20RNG/) | **TFRNG** — counter-flowing turbulence (two 32-bit streams in opposite rotational directions, XOR-combined), three temporal encodings, three-step Markov memory, MurmurHash3 finaliser. Shannon entropy 3.3219 / log₂10 ≈ 3.3219, χ² p-value 0.582 on 100k samples, avalanche pass rate > 0.999. Pure Python 3.9+, zero dependencies. |
| [`Turbulent Flow RNG/TurbulentFlow_RNG_Research_Paper.md`](Turbulent%20Flow%20RNG/TurbulentFlow_RNG_Research_Paper.md) | Research paper |
| [`Turbulent Flow RNG/turbulentflow_rng.py`](Turbulent%20Flow%20RNG/turbulentflow_rng.py) | Python reference implementation |
| [`Turbulent Flow RNG/README.md`](Turbulent%20Flow%20RNG/README.md) | Detailed in-folder README (algorithm spec, statistical results, comparison table vs. Mersenne Twister / LCG / xorshift128+) |

---

## 📊 Headline comparison

| Generator | Family | Key feature | Empirical highlight |
|---|---|---|---|
| **OTB-LCG** | Boolean LCG, 256-bit state | Boolean parity for parameter generation + Von-Neumann correction + SHA-256 | NIST SP 800-22 > 99 % pass; 22.66 % LCG bias eliminated |
| **SynerChaos** | Chaotic-map RNG | Synergetic chaos (see `synerchaos_research_paper.md`) | C + Python implementations |
| **Meta-DAG** | DAG / hash-graph RNG | Structured dependencies via DAG topology | Math model + intro paper |
| **TurbulentFlow** | Counter-flowing 32-bit streams | XOR of forward / backward rotation chains; MurmurHash3 finaliser | Shannon = 3.3219 / 3.3219, χ² p = 0.582, avalanche > 0.999 |

> Earlier README copy listed all five paper files at the *top level* of `RNGS/`; in fact each paper lives in its named subfolder. Earlier copy also abbreviated the OTB-LCG / SynerChaos / Meta-DAG / TFRNG features into a 4-row "RNG types compared" table that conflated different metrics; the per-paper headline numbers above come straight from the source abstracts.

---

## 🚧 Honest framing

- **None of these are CSPRNGs by themselves.** OTB-LCG advertises NIST SP 800-22 passage and SHA-256 post-processing, but the canonical guidance is still: for cryptographic key material use `secrets` (Python stdlib) or a hardware RNG.
- **TFRNG is decimal-output** (digits 0–9). Do not concatenate digits to form integers in a non-decimal range without re-bias correction.
- **No standardised TestU01 BigCrush results.** The papers report chi-square / Shannon / avalanche; BigCrush is acknowledged as not yet run.

---

## 🔗 Related work in this repo

- [`../Compression Algorithms/`](../Compression%20Algorithms/) — Izaac (deterministic shared randomness as side data)
- [`../Izaac as Side Data/`](../Izaac%20as%20Side%20Data/) — applied Izaac protocols
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic structure relevant to Boolean RNG analysis
- [`../Prime Number Generator/`](../Prime%20Number%20Generator/) — scale-dependent meta-pattern theory
- [`../Cypha/`](../Cypha/) — HRNA inference + training stack (uses RNGs for stochastic components)
- [`../Physics/`](../Physics/) — chaos-theory backdrop for Chaotic / SynerChaos work

---

[← Back to main README](../README.md)
