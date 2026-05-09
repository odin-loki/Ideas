# Math Question Generator

> **MegaMathGen — a multi-thousand-line Python program designed to emit an unbounded supply of curriculum-grade mathematics problems across the full mathematics-classification taxonomy, with explicit resource estimation, a `28 GB` memory cap, checkpointing, SymPy / NumPy / 1000-decimal-place precision arithmetic, and progress monitoring via tqdm — paired with a 13-domain landscape survey paper that anchors every domain class to MSC2020 and cites cutting-edge mathematical milestones (geometric Langlands programme's `800+`-page proof in `5` papers, NIST PQC 2024 standardisation, `10 trillion` zeta zeros verified).** Most "math problem generators" are domain-specific exam-builders. This one is built to generate *curricula*, not just questions, and to do so at industrial scale.

---

## What this folder is

There are two kinds of mathematics-problem generators on the open web. The first is the worksheet generator — randomly sample integers, plug into one of a dozen templates, output PDF. The second is the dataset generator for ML training — sample numbers and operations from a fixed schema, emit JSON. Neither is positioned as a *long-running, large-scale, mathematics-curriculum* generator with resource-aware throttling, checkpoint resumption, decimal precision sufficient for serious number-theoretic work, and a domain taxonomy aligned with MSC2020. MegaMathGen is the third option — a tool you point at a hard drive with a few terabytes free, set running for days, and expect to produce gigabytes-to-terabytes of structured mathematics problems across thirteen named domains.

The companion paper (`mathgen research paper.md`) is a 13-domain landscape survey of mathematics in 2024–2026: number theory through to elementary mathematics, with each domain anchored to its MSC2020 classification codes, current frontier work, and the kind of question structure the generator emits. It is broad rather than deep, by its own admission — but unusually current.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`Math-Gen.py`](Math-Gen.py) | **MegaMathGen.** Multi-thousand-line Python generator. Header docstring asserts "unlimited supply" and "gigabytes or terabytes." Memory cap `28 * 1024 = 28 GB` (`memory_limit_mb`). Checkpointing. tqdm progress bars. SymPy + NumPy. `Decimal` precision **`1000`** digits. Extensive domain dictionary opening with number theory and algebra. Resource estimator (`estimate_resources`) with default goals: `10 000` integers, `100 000` integer pairs, `1 000` problems per domain, `1 %` sample (max `1 000`) for time/size estimates, `30 %` overlap heuristic in sizing. |
| [`mathgen research paper.md`](mathgen%20research%20paper.md) | **13-domain landscape survey.** MSC2020-anchored. Number Theory through to Elementary Mathematics. Cites: 2024 geometric Langlands `800+` pages / `5` papers, Breakthrough Prize 2025, NIST PQC 2024, `10 trillion` zeta zeros verified. Reference list `[1]–[48]`. Self-described as "broad rather than deep / literature-entry oriented." |

---

## 🧠 What MegaMathGen does

| Subsystem | Role |
|---|---|
| **Domain taxonomy** | Thirteen MSC2020-anchored domains, opening with number-theory and algebra subtopics |
| **Resource estimator** | Per-domain memory / time / disk projection from a 1 % sample, 30 % overlap heuristic |
| **Checkpointing** | Resume long runs after kill / crash |
| **Precision** | `Decimal` set to `1000` digits — sufficient for serious zeta / prime / Diophantine work |
| **Throttling** | Hard cap at `28 GB` memory; refuses to expand beyond it |
| **Progress** | tqdm bars; live throughput stats |

---

## 🌍 The 13-domain landscape (paper)

The paper organises modern mathematics (2024–2026) into thirteen domains, each anchored to its MSC2020 classification range, current frontier contributors, and key recent results. Examples of cited milestones:

- **Geometric Langlands proof, 2024** — `800+` pages across `5` papers
- **Breakthrough Prize in Mathematics 2025**
- **NIST Post-Quantum Cryptography standardisation, 2024**
- **`10 trillion` zeros of the Riemann zeta function** verified on the critical line (citation `[10]`)
- **FNO neural-operator `~1000×` speedup** for PDEs (cited `[6]`)

The reference list is `48` entries.

---

## 🚧 Honest caveats (paper §)

- **Survey is "broad rather than deep / literature-entry oriented"** — it is a navigation tool, not a research contribution to any of the thirteen domains.
- **Resource estimator outputs are simulations from a 1 % sample**, not measured benchmarks for full runs.
- **Performance claims like "1000× FNO speedup" come from the cited third-party papers**, not from any author benchmark.
- **`Math-Gen.py` line count.** The README shorthand "5200-line" is approximate; the file is in the multi-thousand-line range — pin an exact `wc -l` if you need a number.

---

## 🎯 What this displaces

| Standard | Limitation | What MegaMathGen offers |
|---|---|---|
| Worksheet generator (Khan / Brilliant style) | Domain-narrow, template-based | Thirteen domains, MSC-anchored |
| ML training-set generator | Schema-locked, low precision | `1 000`-digit Decimal, full mathematics taxonomy |
| Hand-written problem sets | Doesn't scale | Gigabyte-to-terabyte runs |
| Generic Python random-math scripts | No checkpointing / resource budgeting | Production-level resource discipline |

---

## 🔗 Related work in this repo

- [`../General Math Papers/`](../General%20Math%20Papers/) — LCRP (Logarithmic Complexity Reduction Principle) — sits in the algorithms domain of the survey
- [`../Prime Number Generator/`](../Prime%20Number%20Generator/) — scale-dependent meta-pattern theory (number-theory domain)
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebra domain
- [`../Statistical Generation/`](../Statistical%20Generation/) — Universal Statistical Generator (probability / statistics domain)
- [`../Veritas/`](../Veritas/) — formal verification (mathematical logic domain)
- [`../Physics/`](../Physics/) — non-local field theory (mathematical physics)

---

[← Back to main README](../README.md)
