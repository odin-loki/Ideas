# Break AES with NNs — research scaffolding for Transformer + RL cryptanalysis of AES

> **A research-scaffolding sketch combining a Transformer student, Llama-teacher knowledge distillation, and policy-gradient reinforcement learning with a BLEU-shaped reward — framed as the training stack one would point at AES key recovery to see what happens.** This folder is *not* an AES break, an attack against AES-128, or a working cryptanalysis tool. It is a Python skeleton plus an informal proof-sketch note exploring whether modern ML training recipes could plausibly approach the problem; the file headers themselves describe the math as informal and the code as research scaffolding.

> **What this folder is NOT.** Not a cryptanalysis result. Not a working tool. Not validated. Not deployable.

---

## 🧭 How this fits the parent folder

This subfolder sits inside [`../`](../) (`Modelling AES/`) and is the *experimental scaffolding* whose dead-end the parent folder's two papers formalise. The companion paper [`neural_aes_paper.md`](neural_aes_paper.md) reads as the post-mortem on attempts of this kind: it identifies three independent barriers (entropy indistinguishability, pseudorandom collapse, combinatorial state-space infeasibility) that defeat black-box neural key recovery against AES-128, and measures the actual chance-level performance (`0.675 %` best test accuracy vs `0.3906 %` random baseline, `+0.28` pp, `p = 0.066`). The sister paper [`../neural_prng_paper.md`](../neural_prng_paper.md) approaches the same problem from the forward direction and measures the partial-convergence ceiling for generating AES-like output. Read this folder *with* both — the parent [`../README.md`](../README.md) is the index.

---

## What this folder is

The proposition is straightforward: take a Transformer architecture (`d_model = 512`, `8` heads, `6 + 6` layers — defaults), distil it from a Llama teacher with KL-temperature `τ = 2.0`, and then fine-tune it with REINFORCE-style policy gradients using BLEU on the output as a reward signal. Whether this produces anything useful when pointed at AES key recovery is the open question; the folder records the scaffolding of one experimental attempt, plus a math note that argues — informally — about Kushner–Clark convergence and `O(1/ε²)` distillation sample complexity.

The files here read as **early-stage research scratch**, not a finished result. The training loop has undefined data loaders. The reward function calls `sentence_bleu` on tensors when BLEU expects token lists or strings. `pytest.main([__file__])` runs at the top of the file before training, which is structurally odd. The proof note acknowledges its own informality.

This is included in the repo as an honest record of an experiment, not as a result claim. [`neural_aes_paper.md`](neural_aes_paper.md) §6.3 ("The Distillation-RL Architecture Specifically") works through the design flaws explicitly — the Llama teacher's semantic token distribution has no relationship to AES key structure, the BLEU reward needs the target plaintext to compute (circular for a real attack), and the encoder's input is uniform noise so adds computational depth without adding information.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`complete-transformer-rl.py`](complete-transformer-rl.py) | Training scaffolding. `MappingLayer`, `nn.Transformer` (`d = 512`, `8` heads, `6 + 6` layers, max-position 5000), `DistillationLoss` (temperature `2.0`, KL × `τ²`), REINFORCE with `Categorical` sampling, baseline decay `0.99`, entropy bonus `0.01`, gradient clip `1.0`. |
| [`math-proof.md`](math-proof.md) | Informal convergence note. Cites Kushner–Clark; sample-complexity sketches `O(1/ε²)` distillation, `O(1/(1 − γ)³ ε²)` RL-style. Self-described as "not venue-ready". |
| [`transformer-architecture.mermaid`](transformer-architecture.mermaid) | Architecture diagram (Mermaid source). |
| [`Architecture.PNG`](Architecture.PNG) | Architecture diagram (raster). |

---

## 🚧 Honest caveats (called out in source)

- **`math-proof.md` explicitly says** the arguments are informal, not venue-ready, and that monotone convergence / smoothness conditions are invoked loosely.
- **`complete-transformer-rl.py` is non-runnable as written**:
  - `main()` calls `distill_step(batch, optimizer)` but `batch` and the data loaders are undefined.
  - `reward_fn` uses `sentence_bleu` on tensors; BLEU expects token lists or strings.
  - `pytest.main([__file__])` runs before training in the same file; structurally odd.
- **No AES-specific cryptanalysis math is present.** No S-box analysis, no key-schedule modelling, no cipher-internals reasoning. AES is referenced as the target by name only.
- **No empirical results in this folder.** No measured key recovery, no key bits leaked, no distinguisher built. The empirical work that *was* done on the recovery question lives one level up in [`neural_aes_paper.md`](neural_aes_paper.md), and arrives at chance-level performance with statistical confirmation.

---

## 🎯 What's actually here

| Claim a reader might assume | Reality |
|---|---|
| AES is broken | No |
| Practical attack on AES-128 / AES-256 | No |
| Reproducible reduction in key-search space | No |
| Working ML cryptanalysis pipeline | No — scaffolding with documented bugs |
| Honest record of an experimental attempt | Yes |
| Useful starting point for someone wanting to actually do this | Possibly — as a *structure*, not a baseline. The parent paper's §6.2 lists what would have to change for any neural approach to be non-trivially above chance. |

---

## 🔗 Related work in this repo

- [`../`](../) — **parent folder.** The two result-bearing papers ([`neural_aes_paper.md`](neural_aes_paper.md) and [`../neural_prng_paper.md`](../neural_prng_paper.md)) plus the unified [`../README.md`](../README.md).
- [`neural_aes_paper.md`](neural_aes_paper.md) — **the companion paper on this scaffolding's regime.** Formalises three barriers (entropy indistinguishability, pseudorandom collapse, combinatorial state-space) and confirms them with five experiments.
- [`../neural_prng_paper.md`](../neural_prng_paper.md) — **the dual question.** Can a neural network generate AES-like output? GAN reaches `7.983` bits entropy and `1.0005` compression but fails chi-squared.
- [`../../ARIA Encryption Algorithm/`](../../ARIA%20Encryption%20Algorithm/) — companion construction (build, not break).
- [`../../Veritas/`](../../Veritas/) — formal verification work, including the bound machinery that an honest cryptanalysis would need.
- [`odin-loki/cellai`](https://github.com/odin-loki/cellai) — alternative neural architecture that does not require attention.
- [`../../GF2 Algebra and Applications/`](../../GF2%20Algebra%20and%20Applications/) — proper algebraic underpinnings for finite-field cryptanalysis.

---

[← Up to `Modelling AES/`](../README.md) · [← Back to main README](../../README.md)
