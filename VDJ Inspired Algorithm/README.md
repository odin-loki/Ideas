# VDJ Inspired Algorithm — immune-system-inspired combinatorial pattern recognition for embedded / defence (V-D-J recombination)

> **A general-purpose combinatorial pattern-recognition and one-shot-learning framework whose mathematical structure is borrowed wholesale from V(D)J recombination in the vertebrate adaptive immune system: combinatorial assembly from a finite segment library (humans use ~`40 V × 23 D × 6 J` segments to address `> 10¹³` antibody specificities), geometric `1/2^k` weighting that *mathematically justifies* capping combination depth at `r = 6` (beyond which marginal information gain drops below `1.6 %`), RAG1/RAG2-inspired pattern-driven state transitions giving genuine one-shot learning with no retraining cycle, and five primary modules plus seven supporting subsystems all communicating exclusively through a typed `Pattern` dataclass — no module holds a reference to another, so modules can be replaced, parallelised, or adversarially probed individually.** Instrumented end-to-end performance: **`13.0 ms ± 4.4 ms` at `n = 16, r = 5`** with a **`< 1 MB`** (`997 KB`) peak memory footprint, CPU-only, NumPy 2.4.2 / Python 3.12 — designed for defence, embedded, and real-time applications where data scarcity, interpretability, and resource constraints preclude large-scale statistical learning. The framework explicitly does *not* model immunology — it uses VDJ recombination as a *mathematical philosophy*, not a biological simulation.

---

## 🧬 What this folder is

A research paper plus its reference Python implementation. The paper is the canonical specification of the framework, including the modular decomposition, mathematical foundations, and an empirical performance profile.

| File | Role |
|---|---|
| [`VDJ_Research_Paper.md`](VDJ_Research_Paper.md) | Primary paper — VDJ biology, mathematical abstractions, system architecture, module mathematics, empirical profile, related-work survey, limitations. |
| [`VDJ_Inspired_Algorithm.py`](VDJ_Inspired_Algorithm.py) | NumPy-only Python reference implementation. |

---

## 🧠 What the framework actually does

VDJ recombination in jawed vertebrates assembles antibody receptors from a **finite library** (~40 V × 23 D × 6 J segments in humans) plus junctional diversity, generating a theoretical repertoire $> 10^{13}$ specificities. The VDJ-Inspired Algorithm extracts four mathematical principles from this and realises them in software:

1. **Combinatorial assembly from a finite segment library** — patterns are typed compositions of segments, not free-form vectors.
2. **Geometric progression weighting** — $1/2^k$ scaling provides mathematical justification for capping the combination depth at $r=6$, beyond which marginal information gain falls below 1.6 %.
3. **Pattern-driven state transitions** — RAG1/RAG2-inspired one-shot activation; once a pattern is observed, it is immediately available for matching with no retraining cycle.
4. **Single-example generalisation** — one-shot learning is the design target, not an emergent property.

### Five primary modules

| Module | Role |
|---|---|
| `OneShotLearner` | Ingest and immediately make a pattern matchable |
| `PatternRecognizer` | Match new input against the segment library |
| `CombinatorialGenerator` | Generate typed combinations under the $1/2^k$ weighting |
| `MetaPatternProcessor` | Higher-order pattern composition |
| `SpaceExplorer` | Topological / spatial fingerprinting and exploration |

Plus seven supporting subsystems, all communicating through the typed `Pattern` dataclass. **No module holds a reference to another** — modules can be replaced, parallelised, or adversarially probed individually.

### Empirical profile (from the paper, instrumented run)

| Setting | Result |
|---|---|
| $n=16$, $r=5$, full pipeline | 13.0 ms, $\sigma$ = 4.4 ms |
| Peak memory at $n=16$, $r=5$ | 997 KB |
| Topological + spatial-exploration cost at $n=64$ | < 2.5 ms (effectively free) |
| Hardware | CPU-only, NumPy 2.4.2, Python 3.12 |

---

## 🚧 Honest framing

- **The algorithm does not model immunology.** It uses VDJ recombination as a *mathematical philosophy* — combinatorial generation under geometric weighting, typed interface contracts, one-shot learning, minimal state — and applies that to the general pattern-recognition problem. Earlier README copy described the system as "search / optimisation" / "clonal expansion / somatic hypermutation / affinity maturation" — those biological steps are *not* what this framework implements.
- Designed for **defence, embedded, and real-time** applications where data scarcity, interpretability, and resource constraints preclude large-scale statistical learning.
- The geometric depth-cap argument (cap at $r=6$ once marginal information gain $< 1.6$ %) is a *mathematical* result from the $1/2^k$ weighting, not a tuning hack.

---

## 🔗 Related work in this repo

- [`../Cell AI/`](../Cell%20AI/) — biologically-inspired sequence modelling without attention
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — Izaac / NMP / GRIA frameworks; the typed-segment-library principle echoes the codec view of NMP
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic structure relevant to typed pattern composition
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — ARIA-INTEL: another single-file edge-deployable analysis engine
- [`../Filtering/`](../Filtering/) — GH-SR-IMM heavy-tailed Bayesian filter
- [`../Long Reasoning and Thinking NN/`](../Long%20Reasoning%20and%20Thinking%20NN/) — UHPM long-context architecture

---

[← Back to main README](../README.md)
