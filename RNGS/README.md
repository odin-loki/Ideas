# RNGS — Random Number Generators (a four-family portfolio)

> **Four genuinely different families of pseudo-random number generators in four subfolders, each with its own threat model, performance profile, and statistical evidence — selected so a downstream user can pick the right tool for the job rather than reach for a default.** OTB-LCG (Boolean / transcendental LCG, hardened with SHA-256 post-processing) targets near-cryptographic quality on a 256-bit state. SynerChaos v2 is a 739-bit embedded chaotic+LFSR composite optimised for `~80 cycles/output` on Cortex-M4. Meta-DAG RNG is a transcendentally-seeded 8-node DAG with a `≥ 2¹⁵³⁶ × 40320` state-space lower bound and `≥ 63.9 bits` per 64-bit-output min-entropy under stated normality hypotheses. TurbulentFlow is a decimal-digit (ℤ₁₀) generator with `Shannon entropy 3.3219` (≈ `log₂ 10`), `χ² p = 0.582`, and `avalanche pass rate > 0.999` on 100 000 samples — explicitly framed as a non-cryptographic aesthetic generator, not a CSPRNG.

---

## What this folder is

"Use a CSPRNG" is the answer for cryptography, "use Mersenne Twister" is the default for simulation, and beyond that most projects either roll their own broken PRNG or import three different libraries depending on what they're doing. This folder is an opinionated portfolio: four RNG families, each with a research paper, a reference implementation, and an honest threat-model statement. The goal is to make the threat-model boundaries between them legible — which generator to use for cryptographic key material, which for simulation, which for embedded chaos, which for UI dice rolls — rather than asking users to read four separate cryptography papers to figure that out.

---

## 📁 Subfolder portfolio

### Boolean / Transcendental LCG — near-cryptographic, 256-bit state

| File | Role |
|---|---|
| [`Boolean RNG/Transcendental_LCG_Theory_Paper.md`](Boolean%20RNG/Transcendental_LCG_Theory_Paper.md) | **OTB-LCG (Optimised Transcendental Boolean LCG)** — Hull–Dobell maximum-period LCG over `2²⁵⁶` state, XOR-based Boolean parity functions for parameter generation (eliminates the `22.66 %` naive-LCG bias documented for the standard recipe), multi-source hardware entropy harvesting, Von-Neumann bias correction, SHA-256 post-processing. |
| [`Boolean RNG/Transcendental_LCG_Implementation_Paper.md`](Boolean%20RNG/Transcendental_LCG_Implementation_Paper.md) | Implementation companion. |
| [`Boolean RNG/optimized_transcendental_lcg_spec.md`](Boolean%20RNG/optimized_transcendental_lcg_spec.md) | Reference specification. |
| [`Boolean RNG/transcendental_lcg_python.py`](Boolean%20RNG/transcendental_lcg_python.py) | Python implementation. |

**Headline:** **NIST SP 800-22 Rev. 1a passage rates > 99 %**. Eliminates the 22.66 % parameter-selection bias of naive LCG. Reseed every `2²⁰` cycles. Shannon-normalised entropy gate `0.70` default, pool `8192 B`. Distinction between Shannon and min-entropy explicitly handled in seed screening.

### Chaotic / SynerChaos v2 — embedded, 739-bit composite

| File | Role |
|---|---|
| [`Chaotic RNG/synerchaos_research_paper.md`](Chaotic%20RNG/synerchaos_research_paper.md) | Research paper. |
| [`Chaotic RNG/chaos_readme.md`](Chaotic%20RNG/chaos_readme.md) | Conceptual overview. |
| [`Chaotic RNG/chaos_python.py`](Chaotic%20RNG/chaos_python.py) | Python implementation. |
| [`Chaotic RNG/chaos_rng.c`](Chaotic%20RNG/chaos_rng.c) | C implementation (embedded targets). |

**Headline:** `~80 cycles per output on Cortex-M4`. **739-bit total state.** LFSR polynomial `x³² + x²² + x² + x + 1`, mask `0x80200003`. **98 % reduction in sequence correlation** (`500/999 → < 10/999` in stated test). Bucket-test χ² **< 20** vs critical `24.99` at `df = 15`.

### DAG / Meta-DAG RNG — transcendental seed structure

| File | Role |
|---|---|
| [`DAG RNG/Meta_DAG_RNG_Research_Paper.md`](DAG%20RNG/Meta_DAG_RNG_Research_Paper.md) | Research paper. |
| [`DAG RNG/DAG RNG Intro.md`](DAG%20RNG/DAG%20RNG%20Intro.md) | Conceptual introduction. |
| [`DAG RNG/DAG RNG Math Model.md`](DAG%20RNG/DAG%20RNG%20Math%20Model.md) | Mathematical model. |
| [`DAG RNG/DAG RNG.py`](DAG%20RNG/DAG%20RNG.py) | Python implementation. |

**Headline:** **8-node DAG**, transcendental-derived 64-bit seeds (π, e, √2, φ, ζ(3), γ, Catalan's constant, Glaisher–Kinkelin). Cross-mix to `(i+3)` and `(i+5)`, `meta_state` mix step, four rounds → one 64-bit output. **State-space lower bound `≥ 2¹⁵³⁶ × 40 320`. Period lower bound `≥ 2⁶⁴`.** **Min-entropy `≥ 63.9 bits` per 64-bit output under stated normality hypotheses.**

> The same architecture appears in [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) as a keyed entropy pump for AEAD; here it is a standalone PRNG.

### Turbulent Flow — decimal aesthetic

| File | Role |
|---|---|
| [`Turbulent Flow RNG/`](Turbulent%20Flow%20RNG/) | Subfolder with detailed README. |
| [`Turbulent Flow RNG/TurbulentFlow_RNG_Research_Paper.md`](Turbulent%20Flow%20RNG/TurbulentFlow_RNG_Research_Paper.md) | Research paper. |
| [`Turbulent Flow RNG/turbulentflow_rng.py`](Turbulent%20Flow%20RNG/turbulentflow_rng.py) | Python reference. |
| [`Turbulent Flow RNG/README.md`](Turbulent%20Flow%20RNG/README.md) | Detailed in-folder README. |

**Headline:** Two 32-bit streams in counter-rotational directions, XOR-combined. Three temporal encodings, three-step Markov memory, MurmurHash3 finaliser. **Output is decimal digits (ℤ₁₀), not binary.** Stats on 100 000 samples: **Shannon entropy `3.3219 bits` (≈ `log₂ 10`), χ² p-value `0.582`, max transition probability `0.1076`, avalanche pass rate `> 0.999`.** Pure Python 3.9+, zero dependencies.

---

## 📊 Side-by-side comparison

| Family | State / period | Stats highlight | Threat model | When to use |
|---|---|---|---|---|
| **OTB-LCG** | 256-bit Hull–Dobell + SHA-256 | NIST SP 800-22 > 99 % pass | **Near-cryptographic** (with SHA-256 stage) | Key material *if no CSPRNG available* |
| **SynerChaos v2** | 739-bit composite | `~80 cycles / output Cortex-M4`; 98 % correlation reduction | **Non-crypto, embedded** | Sensors, telemetry, embedded chaos |
| **Meta-DAG RNG** | `≥ 2¹⁵³⁶ × 40 320` state, `≥ 63.9 bits` min-entropy / output | Transcendental seeds, period `≥ 2⁶⁴` | **Statistical / strong PRNG** under normality hypotheses | High-quality simulation; entropy pump for keyed schemes |
| **TurbulentFlow** | Counter-rotating 32-bit streams | Shannon `3.3219`, χ² `p = 0.582`, avalanche `> 0.999` | **Non-cryptographic, decimal-output** | UI dice, lottery digits, decimal sequences |

---

## 🚧 Honest caveats (per family)

- **None of these is a standardised CSPRNG by themselves.** OTB-LCG advertises NIST SP 800-22 passage and SHA-256 post-processing, but the canonical guidance is still "for cryptographic key material, use `secrets` (Python stdlib) or a hardware RNG." The Boolean doc states this explicitly.
- **SynerChaos v2** explicitly says: statistical tests ≠ cryptographic proof; finite-precision chaos has known pitfalls; the FastMix mixer is not AES-grade.
- **Meta-DAG RNG** relies on **empirical normality assumptions** for its min-entropy bound; period beyond `2⁶⁴` is "expected" but not closed-form proven.
- **TurbulentFlow** is explicitly **non-next-bit-secure**, time-seeded by default, and outputs decimal digits — do *not* concatenate digits to form integers in non-decimal ranges without rebias correction.
- **No standardised TestU01 BigCrush results** are reported. The papers report `χ²` / Shannon / avalanche; BigCrush is acknowledged as not yet run.

---

## 🎯 Which to use when

| Need | Use this | Don't use |
|---|---|---|
| Cryptographic key material | `secrets` / hardware RNG | Any of these alone |
| Embedded simulation, low cycles | SynerChaos v2 | Mersenne Twister (state too large) |
| High-quality scientific simulation | Meta-DAG RNG | Linear PRNGs |
| Decimal sequences (UI, lottery) | TurbulentFlow | Anything binary |
| Need NIST passage + size budget | OTB-LCG | Naive LCG |

---

## 🔗 Related work in this repo

- [`../Compression Algorithms/`](../Compression%20Algorithms/) — Izaac uses σ streams that need a CSPRNG underneath
- [`../Izaac as Side Data/`](../Izaac%20as%20Side%20Data/) — applied protocols
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — finite-field structure relevant to Boolean RNG analysis
- [`../Prime Number Generator/`](../Prime%20Number%20Generator/) — scale-dependent meta-pattern theory; related randomness questions
- [`../Cypha/`](../Cypha/) — HRNA inference + training stack (uses RNGs for stochastic components)
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — Meta-DAG RNG used as keyed entropy pump for AEAD
- [`../Physics/`](../Physics/) — chaos-theory backdrop for the Chaotic / SynerChaos work

---

[← Back to main README](../README.md)
