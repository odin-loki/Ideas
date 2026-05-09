# Neural Decompiler — assembly to source code via sequence-to-sequence learning with hierarchical memory and mixture-of-experts

> **Binary → high-level source, reframed as conditional sequence modelling: a practical encoder–decoder Transformer for *neural decompilation* — the classical compiler-pipeline problem of recovering readable structure (disassembly, control-flow recovery, type reconstruction, pretty-printing) from executables — equipped with a hierarchical memory module of learnable slots `M ∈ ℝ^(K×d)` accessed by multi-head attention with gated fusion, a load-balanced mixture-of-experts (auxiliary loss `λ‖p̄ − u‖²`) split into binary-focused and language-focused families, and a pre-norm GELU encoder/decoder stack with learned position embeddings.** The framing is honest: this is a coherent trainable architecture and reference training loop, not a state-of-the-art recovery system on full binaries — the bundled synthetic corpus only validates the pipeline (forward pass, shape checks, loss decrease), and serious benchmarking would require lifted-assembly + source datasets with recorded compiler flags. Earlier README copy described the folder as decompiling "trained PyTorch models" — that is **not** the subject; the subject is the program-understanding problem.

---

## 🔧 What this folder is

A research note (`RESEARCH.md`) plus a runnable PyTorch package (`neural_decompiler/`) implementing the architecture: hierarchical memory module, Transformer encoder/decoder, mixture-of-experts layer, training loop, inference harness, dataset, and synthetic corpus for pipeline validation.

Earlier README copy described this folder as decompiling "trained PyTorch models" — that is **not** the subject. Per `RESEARCH.md` §1, the task is the classical compiler-pipeline problem of recovering readable structure from executables (disassembly, control-flow recovery, type reconstruction, pretty-printing) reframed as conditional sequence modelling.

---

## 📄 Files

| File / package | Role |
|----------------|------|
| [`RESEARCH.md`](RESEARCH.md) | Research note — task, architecture, training objective, evaluation protocol, limitations, references |
| [`Architecture.txt`](Architecture.txt) | Block-diagram / sketch of the network |
| [`Neural Decompiler.py`](Neural%20Decompiler.py) | Top-level entry script |
| [`requirements.txt`](requirements.txt) | Dependencies |
| `neural_decompiler/` | Implementation package |
| ↳ `model.py` | Transformer encoder/decoder + hierarchical memory + MoE |
| ↳ `train.py` | Training loop with auxiliary load-balancing loss |
| ↳ `infer.py` | Inference / decoding |
| ↳ `dataset.py` | Synthetic-corpus dataset abstraction |
| ↳ `memory.py` | Hierarchical memory module (learnable memory slots + multi-head attention + gated fusion) |
| ↳ `experts.py` | Mixture-of-experts layer |
| `archive/Neural_Decompiler_design_sketch.py.txt` | Earlier design sketch, kept for provenance |

---

## 🏗 Architecture (per `RESEARCH.md` §3)

1. **Hierarchical memory module** — at each level, compressed representations attend to a bank of learnable memory slots $M \in \mathbb{R}^{K\times d}$ via multi-head attention; gated fusion combines compressed states with the resulting context vectors; multiple levels stack and are fused linearly. Acts as a differentiable analogue of "remembered" program context.
2. **Transformer encoder** — pre-norm GELU `TransformerEncoderLayer` stack. Learned position embeddings capped at `max_sequence_length`.
3. **Transformer decoder** — causal self-attention plus cross-attention to encoder outputs.
4. **Mixture-of-experts (MoE)** — router produces logits $z\in\mathbb{R}^E$; probabilities $p=\mathrm{softmax}(z)$; expert outputs $o_e = \mathrm{FFN}_e(h)$; output is the dense mixture $\sum_{e=1}^E p_e\,o_e$. Experts are loosely partitioned into **binary-focused** and **language-focused** families.
5. **Load balancing** — auxiliary loss $\lambda \lVert\bar p - u\rVert^2$ where $\bar p$ is batch-averaged importance and $u$ is uniform over experts; discourages router collapse.

---

## 🎯 Objective

Primary loss is token cross-entropy with label smoothing on non-padding positions. Total loss:

$$\mathcal L = \mathcal L_{\mathrm{CE}} + \lambda_{\mathrm{moe}}\,\mathcal L_{\mathrm{aux}}.$$

---

## 📊 Evaluation protocol (proposed, not yet run on real binaries)

The bundled synthetic corpus only validates the pipeline (forward pass, shape checks, loss decrease). Serious benchmarks would use:

1. **Lifted assembly** paired with source from compiler-generated datasets, with compilation flags recorded.
2. Metrics: exact match, BLEU against reference C, and graph-level metrics (CFG edit distance) where tooling exists.
3. Ablations: remove MoE; replace hierarchical memory with a single cross-attention pass; vary expert count $E$.

---

## 🚧 Honest framing (from `RESEARCH.md` §5)

- This is a **coherent trainable architecture** plus a reference training loop, not a state-of-the-art recovery system on full binaries.
- Real binaries imply long sequences and large vocabularies; production deployment would require chunking at function boundaries and possibly hierarchical models beyond this prototype.
- Neural outputs should be type-checked and tested; the model does **not** guarantee semantics-preserving translation.
- Dense MoE mixtures cost $O(E)$ per token; production systems may switch to top-$k$ sparse kernels.

---

## 🔗 Related work in this repo

- [`Cell AI/`](../Cell%20AI/) — alternative non-attention sequence backbone with multi-domain MoE-style routing
- [`Long Reasoning and Thinking NN/`](../Long%20Reasoning%20and%20Thinking%20NN/) — UHPM long-context memory architecture
- [`NN Shortcuts/`](../NN%20Shortcuts/) — Streaming Geometry Framework efficiency techniques
- [`Cypha/`](../Cypha/) — Harmonic Recursive Neural Architecture; full ML stack
- [`Compression Algorithms/`](../Compression%20Algorithms/) — model-level compression theory (NMP, GRIA, Izaac)

---

[← Back to main README](../README.md)
