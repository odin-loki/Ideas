# Neural decompilation with hierarchical memory and mixture-of-experts

## Abstract

We describe a practical encoder–decoder architecture for *neural decompilation*: learning a mapping from a low-level token sequence (e.g. disassembled instructions) to a high-level source-like token sequence. The model combines (1) a **hierarchical memory module** that conditions representations on learnable memory slots via multi-head attention, (2) a standard **Transformer** encoder and decoder, and (3) a **mixture-of-experts (MoE)** layer partitioned into binary-focused and language-focused expert families, with an auxiliary load-balancing objective. A reference implementation ships with a synthetic corpus for integration testing. This note situates the design among related work and outlines evaluation protocols suitable for future empirical studies.

## 1. Introduction

Decompilation recovers readable structure from executables. Classical pipelines (disassembly, control-flow recovery, type reconstruction, pretty-printing) are brittle across compilers, optimizations, and obfuscation. *Neural* approaches treat decompilation as conditional sequence modeling: the model observes a linearized low-level program and generates a high-level program. This aligns with neural machine translation but differs in vocabulary structure (registers, immediates, memory operands) and long-range semantics (calling conventions, data structures).

This work does not claim state-of-the-art recovery on full binaries; it specifies a **coherent trainable architecture** and a **reproducible training loop** so that researchers can swap corpora, losses, and analysis passes without rewriting ad hoc prototypes.

## 2. Related work

- **Neural machine translation** (Bahdanau et al.; Vaswani et al.) provides the encoder–decoder and attention baseline.
- **Mixture-of-experts** (Shazeer et al.; Fedus et al., Switch Transformers) motivates sparse or dense routing to specialize sub-networks—here, loosely grouped as “binary” vs “language” experts to mirror distinct inductive biases.
- **Neural decompilation and assembly-to-code** (various workshop and security-venue papers) often use RNNs or Transformers on assembly text; our stack is closest to Transformer seq2seq with additional structural priors (memory + MoE).
- **Program analysis** (control flow, types) can be integrated as auxiliary tasks or as features; the present codebase reserves `task_weights` in configuration for such extensions.

## 3. Method

### 3.1 Notation

Let \(x = (x_1,\ldots,x_{T_x})\) be source token indices (assembly-like) and \(y = (y_1,\ldots,y_{T_y})\) target indices (high-level). Teacher forcing uses decoder input \((y_1,\ldots,y_{T_y-1})\) to predict \((y_2,\ldots,y_{T_y})\).

### 3.2 Hierarchical memory

Each level applies **compressed representations** and **multi-head attention** from sequence queries to a bank of learnable memory slots \(M \in \mathbb{R}^{K \times d}\). Gated fusion combines compressed states with context vectors; multiple levels stack and are fused by a linear projection. This implements a *differentiable* analogue of “remembered” program context without committing to a full external memory database.

### 3.3 Transformer encoder and decoder

The encoder is a stack of `TransformerEncoderLayer` blocks (pre-norm, GELU). The decoder is causal self-attention plus cross-attention to encoder outputs. Positions use learned embeddings capped at `max_sequence_length`.

### 3.4 Mixture-of-experts

Let \(h \in \mathbb{R}^{d}\) be a hidden vector. A router produces logits \(z \in \mathbb{R}^{E}\), probabilities \(p = \mathrm{softmax}(z)\), and expert outputs \(o_e = \mathrm{FFN}_e(h)\). The MoE output is \(\sum_{e=1}^{E} p_e , o_e\) (dense mixture in the reference code for clarity and small \(E\)).

**Load balancing:** with batch-averaged importance \(\bar{p} = \frac{1}{BT}\sum_{b,t} p_{b,t}\), we add \(\lambda \lVert \bar{p} - u \rVert^2\) where \(u\) is uniform over experts. This discourages router collapse.

### 3.5 Objective

Primary loss is **token cross-entropy** with label smoothing on non-padding positions. Total loss:

\[
\mathcal{L} = \mathcal{L}_{\mathrm{CE}} + \lambda_{\mathrm{moe}} \mathcal{L}_{\mathrm{aux}}.
\]

## 4. Experiments (protocol)

The bundled **synthetic** dataset only validates pipelines (forward pass, shapes, loss decrease). Serious benchmarks should include:

1. **Lifted assembly** paired with source from compiler-generated datasets (same compilation flags recorded).
2. **Metrics:** exact match, BLEU against reference C, and graph-level metrics (CFG edit distance) where tooling exists.
3. **Ablations:** remove MoE; replace hierarchical memory with a single cross-attention pass; vary expert count \(E\).

Report variance across random seeds and compiler optimization levels.

## 5. Limitations

- **Scale:** Real binaries imply long sequences and large vocabularies; training requires data filtering, chunking at function boundaries, and possibly hierarchical models beyond this prototype.
- **Correctness:** Neural outputs should be type-checked and tested; the model does not guarantee semantics-preserving translation.
- **MoE routing:** Dense mixtures cost \(O(E)\) per token; production systems may switch to top-\(k\) sparse kernels.

## 6. Conclusion

We presented a modular neural decompiler design—hierarchical memory, Transformer seq2seq, and family-structured MoE with load balancing—and provided an open implementation suitable for extension to real assembly–source corpora. Future work should emphasize *semantic* evaluation (tests, symbolic execution) alongside string-based metrics.

## References (illustrative)

- Vaswani et al., “Attention Is All You Need,” NeurIPS 2017.
- Shazeer et al., “Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer,” ICLR 2017.
- Fedus et al., “Switch Transformers: Scaling to Trillion Parameter Models,” JMLR 2022.
