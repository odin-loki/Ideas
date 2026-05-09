# Veritas — verification-enabled learning architecture (Verification-Enabled Reasoning and Integrated Theorem-Acquiring System)

> **VERITAS is a learning architecture in which the artefact produced is not loss curves but proof traces.** Every step of every learner emits PAC, mistake-bound, meta-learning, and composition certificates as it goes — and the system's central composition theorem (Theorem 9) shows that error and confidence add cleanly when a meta-learner sits on top of a base learner: `P(err(m∘h) > ε + ε_m) ≤ δ + δ_m`. Worked example for `n = 8`: the function class has size `|H| = 2^(2⁸) = 2²⁵⁶`, so `ln|H| ≈ 177 000`, and the PAC sample bound at `ε = δ = 0.01` gives `~1.8 × 10⁶` samples — extreme by ML standards, but **proven, not hoped**.

---

## What this folder is

Modern ML verification is a moving target — most of what passes for "verified" is empirical generalisation on a held-out set with a confidence interval over the held-out estimate. Veritas argues for the opposite extreme: every learner inherits a deductive contract on the binary-pattern function class `H = {h : {0,1}ⁿ → {0,1}ⁿ}`, with `|H| = 2^(2ⁿ)`, and the system maintains and composes formal certificates over: PAC sample bounds (Hoeffding), mistake bounds (perceptron-style), exact-identification queries (membership-query learning), and meta-learning bounds (over the class `M = {m : H → H}` of meta-functions).

The work is *deliberately expensive at the full-class level* — a complete PAC bound over `M` is astronomical — because the goal is to expose where you can *and cannot* make formal claims, and to show how to relax to restricted hypothesis classes `H'` where bounds become tractable. The composition theorem is the load-bearing piece: it lets you stack a meta-learner on a base learner and add their failure budgets, rather than multiplying them.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`veritas_research_paper.md`](veritas_research_paper.md) | Main research paper. Defines `B = {0,1}ⁿ`, `H = {h : B → B}`, `\|H\| = 2^(2ⁿ)`, `M = {m : H → H}`. Theorems 1 through 9, including the composition rule. |
| [`veritas-complete-math-proving.md`](veritas-complete-math-proving.md) | Extended proof appendix. |
| [`veritas_core.py`](veritas_core.py) | Core learner machinery. |
| [`veritas_verification.py`](veritas_verification.py) | Verification / certificate emission. |
| [`veritas_distillation.py`](veritas_distillation.py) | Knowledge-distillation track. |
| [`veritas_integration.py`](veritas_integration.py) | Integration with downstream learners. |

---

## 🧠 Theorems

| # | Statement |
|---|---|
| **2** | Single-`h` PAC: `m ≥ (1 / (2ε²)) ln(2/δ)` (Hoeffding). |
| **3** | Uniform PAC over `H`: `m ≥ (1/ε²)(ln\|H\| + ln(1/δ))`. **Worked example `n = 8`: `ln\|H\| ≈ 177 000`, `ε = δ = 0.01` ⇒ `~1.8 × 10⁶` samples.** |
| **4** | Mistake bound: `≤ lg\|H\| = 2ⁿ`. |
| **5** | Membership-query exact identification: `≤ n` queries (basis-query argument). |
| **7** | Meta-mistake ceiling: `lg\|M\| = 2ⁿ · 2^(2ⁿ)` (theoretical, full `M`). |
| **9** | **Composition.** `P(err(m∘h) > ε + ε_m) ≤ δ + δ_m`. *Confidences and errors add.* |

The **runtime proof checklist** ties these together: PAC sample is met → empirical-error slack `√(ln(2/δ)/(2m))` is computed → mistake count `≤ 2ⁿ` is verified → query count `≤ n` is logged → meta-error `≤ 2ε` is checked. The system fails certification if any single line fails.

---

## 🔬 What "verification" means in this folder

Critically, **most of these certificates are vacuously satisfied early in training**. Until enough samples have been seen, the PAC bound is "we have insufficient evidence to make a claim with confidence `δ`," not "the claim is false." The system is honest about this — the verification machinery is a discipline for declaring when you *do* and *do not* have a justified guarantee, not a way to manufacture guarantees at zero cost.

---

## 🚧 Honest caveats

- **Full-class PAC bounds are deliberately expensive.** Practical relief comes from restricting `H` to a tractable subclass `H'` (e.g. monotone functions, low-degree polynomials, decision trees of bounded depth). The framework supports this; the paper discusses it explicitly.
- **Documented prior implementation bug fix:** `ln|H|` must be `2ⁿ ln 2`, **not** `n ln 2`. Earlier code under-estimated the sample requirement by a factor of `2ⁿ / n` — a substantial correction logged transparently in the paper.
- **Theorem 7 / `|M|` is a theoretical ceiling** over the full meta-class. Practical parametric `M` requires VC / Rademacher-style bounds, which the paper points to but does not work out for every parametric family.
- **Computer-assisted proof in this repo is not the same as formal proof in Coq / Lean / Isabelle.** The verification is designed to be *checkable*, not yet *checked* by an external proof assistant.

---

## 🎯 What this displaces

| Standard practice | What it gives | What VERITAS adds |
|---|---|---|
| Held-out test set + 95 % CI | Empirical estimate of generalisation | Deductive PAC bound, mistake bound, query bound |
| "We are 95 % confident" press releases | Vibes | Formal `(ε, δ)` parameters with composition rules |
| Stacking models without analysis | Hope | Theorem 9 budget addition: `(ε + ε_m, δ + δ_m)` |
| Bug-prone hand-calculated bounds | Ad-hoc | Documented bug-fix log: `ln\|H\| = 2ⁿ ln 2`, not `n ln 2` |

---

## 🔗 Related work in this repo

- [`../Long Reasoning and Thinking NN/`](../Long%20Reasoning%20and%20Thinking%20NN/) — UHPM (Unified Hash-Predictive Memory): VERITAS-style certificates would apply
- [`../NN Shortcuts/`](../NN%20Shortcuts/) — Streaming Geometry Framework + Algebraic Autopsy (verification angle)
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — Boolean function structure (VERITAS works over `{0,1}ⁿ → {0,1}ⁿ`)
- [`../3 to 8 Value Boolean Algebra/`](../3%20to%208%20Value%20Boolean%20Algebra/) — sister enumeration of `H` for `n = 3..8`
- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — protocol whose missing EUF-CMA proof would benefit from the VERITAS toolkit

---

[← Back to main README](../README.md)
