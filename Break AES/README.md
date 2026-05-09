# Break AES — research scaffolding for Transformer + reinforcement-learning cryptanalysis of the Advanced Encryption Standard

> **A research-scaffolding sketch combining a Transformer student, Llama-teacher knowledge distillation, and policy-gradient reinforcement learning with a BLEU-shaped reward — framed as a training stack one might point at AES cryptanalysis and see what happens.** This folder is *not* an AES break, an attack against AES-128, or a working cryptanalysis tool. It is a Python skeleton plus an informal proof-sketch note exploring whether modern ML training recipes could plausibly approach the problem; the file headers themselves describe the math as informal and the code as research scaffolding.

> **What this folder is NOT.** Not a cryptanalysis result. Not a working tool. Not validated. Not deployable.

---

## What this folder is

The proposition is straightforward: take a Transformer architecture (`d_model = 512`, `8` heads, `6+6` layers — defaults), distil it from a Llama teacher with KL-temperature `τ = 2.0`, and then fine-tune it with REINFORCE-style policy gradients using BLEU on the output as a reward signal. Whether this produces anything useful when pointed at AES key recovery is the open question; the folder records the scaffolding of one experimental attempt, plus a math note that argues — informally — about Kushner–Clark convergence and `O(1/ε²)` distillation sample complexity.

The files here read as **early-stage research scratch**, not a finished result. The training loop has undefined data loaders. The reward function calls `sentence_bleu` on tensors when BLEU expects token lists or strings. `pytest.main([__file__])` runs at the top of the file before training, which is structurally odd. The proof note acknowledges its own informality.

This is included in the repo as an honest record of an experiment, not a result claim.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`complete-transformer-rl.py`](complete-transformer-rl.py) | Training scaffolding. `MappingLayer`, `nn.Transformer` (d=512, 8 heads, 6+6 layers, max-position 5000), `DistillationLoss` (temperature 2.0, KL × τ²), REINFORCE with `Categorical` sampling, baseline decay 0.99, entropy bonus 0.01, gradient clip 1.0. |
| [`math-proof.md`](math-proof.md) | Informal convergence note. Cites Kushner–Clark; sample-complexity sketches `O(1/ε²)` distillation, `O(1/(1−γ)³ε²)` RL-style. Self-described as "not venue-ready." |
| [`transformer-architecture.mermaid`](transformer-architecture.mermaid) | Architecture diagram. |

---

## 🚧 Honest caveats (called out in source)

- **`math-proof.md` explicitly says** the arguments are informal, not venue-ready, and that monotone convergence / smoothness conditions are invoked loosely.
- **`complete-transformer-rl.py` is non-runnable as written**:
  - `main()` calls `distill_step(batch, optimizer)` but `batch` and the data loaders are undefined.
  - `reward_fn` uses `sentence_bleu` on tensors; BLEU expects token lists or strings.
  - `pytest.main([__file__])` runs before training in the same file; structurally odd.
- **No AES-specific cryptanalysis math is present.** No S-box analysis, no key-schedule modelling, no cipher-internals reasoning. AES is referenced as the target by name only.
- **No empirical results.** No measured key recovery, no key bits leaked, no distinguisher built.

---

## 🎯 What's actually here

| Claim a reader might assume | Reality |
|---|---|
| AES is broken | No |
| Practical attack on AES-128 / AES-256 | No |
| Reproducible reduction in key-search space | No |
| Working ML cryptanalysis pipeline | No — scaffolding with documented bugs |
| Honest record of an experimental attempt | Yes |
| Useful starting point for someone wanting to actually do this | Possibly — as a structure, not a baseline |

---

## 🔗 Related work in this repo

- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — companion construction (build, not break)
- [`../Veritas/`](../Veritas/) — formal verification work, including the bound machinery that an honest cryptanalysis would need
- [`../Cell AI/`](../Cell%20AI/) — alternative neural architecture (CellularAI) that does not require attention
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — proper algebraic underpinnings for finite-field cryptanalysis

---

[← Back to main README](../README.md)
