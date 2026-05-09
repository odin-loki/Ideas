# Cell AI / CellularAI — biologically-inspired sequence modelling without attention

> **A trainable, non-attention sequence architecture.** CellularAI replaces self-attention with three biologically-motivated principles: a reaction-diffusion cellular partition (CellularPDE), online Hebbian plasticity with a BCM-style sliding threshold (MetaplasticityLayer), and a multi-domain routing layer (MultiModalModel). v2 adds frequency-domain resonance and a crystal-lattice interaction; v3 adds spectral PDE, multiscale partitions, sparse Hebbian, and a guided architecture-search programme (E0–E26).

---

## 🧬 What this folder is

A research codebase: full Python packages for v1, v2, v3, plus a shared `cellai_core/` library, end-to-end training pipelines, an architecture-search programme (`arch_search/`), evaluation harnesses, tests, and a documentation tree under `docs/`. Multiple research papers ship inline.

Earlier README copy claimed a folder structure (`Cell AI v3/`, `Cell AI v2/`, `Thinking CoT/`, `Multi Modal AI/`, `Contracting/`) that **does not exist on disk**. The real layout is below.

---

## 🗂 Actual repository layout

```
Cell AI/
├── README.md
├── setup.py · requirements.txt · .env.example
├── v1/                  cell_ai.py           # CellularAI v1
├── v2/                  cell_ai_v2.py        # CellularAI v2
├── v3/                  cell_ai_v3.py        # CellularAI v3
├── cellai_core/         encoder · memory · multiscale · partition ·
│                        routing · sparse_hebbian · spectral_pde · ...
├── data/
│   ├── config.py
│   └── pipelines/       nlp_pipeline.py · math_pipeline.py · software_pipeline.py
├── arch_search/         run_arch_search*.py · resume scripts · round-4 follow-up
├── scripts/             cli.py · run_full_pipeline.py · run_multimodal.py ·
│                        run_eval.py · profiling · smoke tests
├── tests/
├── tools/
│   └── Math Question Generator/   # bundled MegaMathGen tool
└── docs/
    ├── README.md                       # canonical doc hub
    ├── CELLULARAI_PAPER.md             # main architecture paper
    ├── ARCH_SEARCH_PAPER.md            # E0–E26 search programme
    ├── EVALUATION_REPORT.md
    ├── architecture/   v1 · v2 · v3 · multimodal · parallel · thinking_cot
    ├── math_models/    core · domain · nlp · software · advanced
    └── research/       roadmap · plan · brain comparison · explanations · Q&A
```

---

## 📄 Documentation hub

The canonical navigation file is [`docs/README.md`](docs/README.md). Highlights:

| Document | Subject |
|----------|---------|
| [`docs/CELLULARAI_PAPER.md`](docs/CELLULARAI_PAPER.md) | Main architecture paper — v1 + v2, training & evaluation on ~3 GB multi-domain data |
| [`docs/ARCH_SEARCH_PAPER.md`](docs/ARCH_SEARCH_PAPER.md) | v3 / SpectralPDE / multiscale / sparse Hebbian / guided architecture search rounds E0–E26 |
| [`docs/EVALUATION_REPORT.md`](docs/EVALUATION_REPORT.md) | Held-out evaluation notes |
| [`docs/architecture/v1_architecture.md`](docs/architecture/v1_architecture.md) | Base cellular system |
| [`docs/architecture/v2_intro.md`](docs/architecture/v2_intro.md) · [`v2_vs_v1.md`](docs/architecture/v2_vs_v1.md) · [`v2_math_model.md`](docs/architecture/v2_math_model.md) | Resonance + crystal-lattice extensions |
| [`docs/architecture/v3_architecture.md`](docs/architecture/v3_architecture.md) · [`v3_math_model.md`](docs/architecture/v3_math_model.md) | OICFHS / spectral PDE |
| [`docs/architecture/multimodal_architecture.md`](docs/architecture/multimodal_architecture.md) | Multi-domain routing |
| [`docs/architecture/parallel_model.md`](docs/architecture/parallel_model.md) | Parallel training story |
| [`docs/architecture/thinking_cot_readme.md`](docs/architecture/thinking_cot_readme.md) | Chain-of-thought variant notes |
| [`docs/math_models/`](docs/math_models/) | Domain-specific math models (core, NLP, software, advanced) |
| [`docs/research/`](docs/research/) | Research plan, possibilities, answered questions, brain comparison |

---

## 🧪 Five core architectural pieces (from §3 of the paper)

1. **CellularPDE** — reaction-diffusion partition system. Information propagates between independent state partitions through a learned diffusion operator, replacing token-to-token attention. Inspired by Turing's morphogenesis equations.
2. **MetaplasticityLayer** — Hebbian outer-product update with a BCM-inspired sliding threshold. Enables weight adaptation **during** the forward pass, not only via backprop.
3. **ResonanceSystem** (v2) — frequency-domain enhancement using FFT phase rotation.
4. **CrystalLattice** (v2) — einsum-vectorised lattice fields; mathematically a 3-way Tucker decomposition over the state vector.
5. **MultiModalModel** — soft router that classifies the cellular state and mixes three domain-specialised MLP heads (text / code / math) without duplicating parameters.

v3 introduces **SpectralPDE**, **multiscale partitions**, **sparse Hebbian**, and a guided architecture-search programme over rounds E0–E26 with stream-matched held-out PPL evaluation, continuous-training reruns, and CLI flags `--reeval` / `--train` on `python -m arch_search.run_arch_search_v4`.

---

## ⚙️ Running the code

The CLI lives at `scripts/cli.py`; canonical entry points include `python -m arch_search.run_arch_search_v4` and `scripts/run_full_pipeline.py`. See [`scripts/README.md`](scripts/README.md) for current commands.

Tokeniser: `cl100k_base`. Training data: ~3 GB multi-domain (English text, Python source, mathematics).

---

## 🚧 Honest framing (from the paper's own §1 and §5)

- The paper does **not** claim competitive perplexity with transformers. v1 perplexity on held-out text is ~10 000–250 000 depending on domain — well above GPT-2 baselines.
- Loss curves and gradient norms confirm the architecture **is** trainable; the routing mechanism improves from chance-level to a measurable signal after fine-tuning.
- Gradient analysis identified a **gradient-starvation pathology** at the Hebbian / reaction-diffusion interface; the paper diagnoses and repairs this with a differentiable state-gate projection.
- v3 round **E26** (8k continuous total after E25) does **not** improve warm PPL vs E25 (paper §17.6) — explicitly reported as a negative result.

---

## 🔗 Related work in this repo

- [`Long Reasoning and Thinking NN/`](../Long%20Reasoning%20and%20Thinking%20NN/) — UHPM unified hash-predictive memory; complementary long-context architecture
- [`Cypha/`](../Cypha/) — Harmonic Recursive Neural Architecture (HRNA) full ML stack
- [`NN Shortcuts/`](../NN%20Shortcuts/) — Streaming Geometry Framework + Algebraic Autopsy
- [`Compression Algorithms/`](../Compression%20Algorithms/) — Izaac / GRIA / NMP model-level compression
- [`Neural Decompiler/`](../Neural%20Decompiler/) — Transformer + MoE seq2seq with hierarchical memory
- [`Veritas/`](../Veritas/) — formal verification of learning systems

---

[← Back to main README](../README.md)
