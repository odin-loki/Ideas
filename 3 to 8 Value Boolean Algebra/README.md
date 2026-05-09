# 3 to 8 Value Boolean Algebra

> **A dimension-by-dimension narrative of the full Boolean function spaces `f : {0,1}ⁿ → {0,1}` for `n = 3, 4, 5, 6, 7, 8` — exact at small `n`, sampled at large `n`, anchored to formal Walsh–Hadamard / bent-function machinery and threaded through to applications in error-correcting codes (Steane), Byzantine N-modular redundancy, AES-S-box-style nonlinearity, and quantum control.** The space sizes are `2^(2ⁿ)`, which is `256` at `n = 3`, `65 536` at `n = 4` (the last fully-enumerable case for typical hardware), `4.3 × 10⁹` at `n = 5`, `1.8 × 10¹⁹` at `n = 6`, `~3.4 × 10³⁸` at `n = 7`, and `2²⁵⁶ ≈ 1.16 × 10⁷⁷` at `n = 8` — and the headline thread is that the fraction of "**truly `n`-dimensional**" (irreducible, non-decomposable) functions rises from `~93.8 %` at `n = 3` to `~99.9 %` at `n = 8`.

> **Key vocabulary clarification.** "3 to 8 value" here means **3 to 8 input variables**, not 3-valued vs 8-valued logic. The codomain is always `{0, 1}`. The "value" is `n` in `{0, 1}ⁿ → {0, 1}`.

---

## What this folder is

Most introductions to Boolean algebra stop at `n = 2` or `n = 3`, hand-wave at `n = 4`, and then jump straight to "of course the space gets enormous." This folder takes the opposite approach: walk through each dimension from `n = 3` to `n = 8`, lay out the exact combinatorial structure where you can (small `n`), use disciplined sampling where you can't (large `n`), and at every step tie the structure back to the same vocabulary — Hamming weight distributions, threshold/majority functions, linear/affine subspaces, balanced functions, self-dual functions, bent functions, and the irreducibility / "truly `n`-dimensional" fraction. The result is a unified narrative for the entire low-`n` regime that engineers and theoreticians actually use.

The applications layer maps each level to real artefacts: `n = 3` to triple-modular redundancy and the Hamming `[7,4]` parity codes; `n = 4` to nibble-level error correction and AES-S-box building blocks; `n = 5` and beyond to Reed–Muller codes, bent-function nonlinearity, quantum error correction (the Steane `[[7,1,3]]` code at `n = 7`), and Byzantine consensus thresholds.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`three_var_boolean_analysis.md`](three_var_boolean_analysis.md) | `n = 3`. All `256` functions enumerated. Hamming weights `C(8, k)`. `16` linear / `2^(n+1) = 16` affine. `70` balanced. `~93.8 %` "truly 3D." Named exemplars: **F232 = MAJORITY (at-least-2-of-3)**, **F150 = 3-XOR**. |
| [`four_var_boolean_universe.md`](four_var_boolean_universe.md) | `n = 4`. **Full enumeration of all `65 536` functions.** Binomial on `C(16, k)`. Examples: `AND4 = F32768`, `OR4 = F65534`, `PARITY4 = F27030`, `MAJORITY4 = F59520`. `32` linear, `12 870` balanced, `256` self-dual, `~59 000 (~90 %)` "truly 4D," `~10 %` 2 × 2 decomposable. |
| [`five_var_boolean_frontier.md`](five_var_boolean_frontier.md) | `n = 5`. `4.3 × 10⁹` total. `64` linear (exact). `~6.06 × 10⁸` (`14.12 %`) balanced (extrapolated from sample). `~6.06 × 10⁵` bent (estimated). `~95 %` "truly 5D." Memory budget for full storage: `~137 GB`, days–weeks of compute. Sample size used: `20 000`. |
| [`six_var_boolean_transcendence.md`](six_var_boolean_transcendence.md) | `n = 6`. `1.8 × 10¹⁹` total. **`5 000`-function sample**. `128` linear (exact). Extrapolated `~6.748 × 10¹⁸` balanced. `~98 %` truly 6D. `2.3 EB` storage if you tried. Named: **HYPERMAJORITY6 (≥ 4-of-6)**. |
| [`seven_var_perfect_democracy.md`](seven_var_perfect_democracy.md) | `n = 7`. `~3.4 × 10³⁸` total. `2 000`-function sample. `256` linear (exact). `~99.5 %` truly 7D. **Steane `[[7,1,3]]` code, 7-XOR, democratic threshold functions** anchored here. |
| [`eight_var_digital_perfection.md`](eight_var_digital_perfection.md) | `n = 8`. `2²⁵⁶ ≈ 1.16 × 10⁷⁷` total. `512` linear (`2⁹`). `1 000`-function sample. **`BYTE_PERFECT = 70/256 = 27.3 %`** (functions returning true on exactly half of inputs at byte boundary). `~99.9 %` truly 8D. |
| [`boolean_research_paper.md`](boolean_research_paper.md) | Formal backbone. **Walsh–Hadamard transform**, **bent function maximum nonlinearity `2^(n−1) − 2^(n/2−1)` (even `n`)**, **irreducibility definition**, bridges to Steane code and Byzantine / threshold kernels. Explicitly uses sampling for `n ≥ 5`. |

---

## 🧠 The headline numbers

| `n` | Total functions `2^(2ⁿ)` | Linear | Balanced | "Truly `n`-D" |
|---|---|---|---|---|
| 3 | 256 | 16 | 70 | ~93.8 % |
| 4 | 65 536 | 32 | 12 870 | ~90 % |
| 5 | 4.3 × 10⁹ | 64 | ~14.1 % | ~95 % |
| 6 | 1.8 × 10¹⁹ | 128 | ~37 %† | ~98 % |
| 7 | 3.4 × 10³⁸ | 256 | ~50 %† | ~99.5 % |
| 8 | 1.16 × 10⁷⁷ | 512 (`2⁹`) | ~50 %† | **~99.9 %** |

† extrapolations from samples — the per-file sources are explicit about which numbers are exact and which are estimated.

The "truly `n`-D" curve is the load-bearing claim: as `n` grows, the fraction of functions that are decomposable into smaller-arity pieces *vanishes*. This is the combinatorial reason why high-`n` Boolean function design genuinely *needs* the high-`n` machinery — there is no shortcut through smaller subspaces for the overwhelming majority of functions.

---

## 🚧 Honest caveats

- **Internal tension across files.** `three_var_boolean_analysis.md` calls `n = 4` a "computational challenge"; `four_var_boolean_universe.md` then asserts a complete `65 536` enumeration. `five_var_boolean_frontier.md` simultaneously claims to be the "last practical complete analysis" and uses sampling. Treat scale claims as a mix of rhetorical and exact + sampled.
- **`boolean_research_paper.md` is explicit** that all `n ≥ 5` results use sampling rather than enumeration where enumeration is infeasible.
- **Heavy applications-forward language.** Quantum, AES, and space-mission framings are interpretation, not always derived line-by-line from in-paper proofs.
- **Sample sizes (20 000 / 5 000 / 2 000 / 1 000 for n = 5..8) are author-chosen.** Confidence intervals on the extrapolated counts are not computed in-text.

---

## 🎯 Why this is useful

| Audience | Use |
|---|---|
| Cryptographer | Bent-function lookup at relevant `n`; AES-S-box-class structures at `n = 4` |
| Quantum-EC researcher | Steane `[[7,1,3]]` motivation; CSS-code function classes |
| Distributed-systems engineer | Threshold / majority / Byzantine kernels with tight counts |
| Formal-methods researcher | Companion to [`../Veritas/`](../Veritas/) PAC bounds: this is the `H` for `n = 3..8` |
| ML interpretability | Decomposable vs irreducible functions ⇔ which features can be factorised |

---

## 🔗 Related work in this repo

- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — exhaustive 16-binary-op taxonomy, GF(2) ring uniqueness, GRIA Spectrum Theorem
- [`../Veritas/`](../Veritas/) — PAC sample bounds over exactly this `H`; the `n = 8` case has `\|H\| = 2²⁵⁶`
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — Izaac and GRIA share Boolean / GF(2) lineage
- [`../RNGS/Boolean RNG/`](../RNGS/Boolean%20RNG/) — Boolean LCG analysis benefits from this structure
- [`../UCN AIs/`](../UCN%20AIs/) — Boolean primitives for UCN-universe AI

---

[← Back to main README](../README.md)
