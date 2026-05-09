# 3 to 8 Value Boolean Algebra — dimensional emergence in Boolean function spaces

> **n = 3 to n = 8 *variables*, not 3-to-8 truth values.** A systematic dimension-by-dimension characterisation of Boolean function spaces $f:\{0,1\}^n\to\{0,1\}$, cataloguing linear / balanced / self-dual / threshold / bent / irreducible function counts, and mapping the structural results to cryptographic primitive design, the Steane $[\![7,1,3]\!]$ quantum code, and Byzantine-fault-tolerant n-modular redundancy.

---

## 🧮 What this folder is

Boolean function research — concretely, the space of $f:\{0,1\}^n\to\{0,1\}$ as $n$ grows from 3 to 8. The total count is $2^{2^n}$, which goes from 256 (n = 3, fully enumerable in microseconds) through 65 536 (n = 4, fully enumerable) into the sampling regime for $n\ge 5$.

The folder name "3 to 8 Value" is somewhat misleading — earlier README copy interpreted this as multi-valued or fractional truth values ({0, 0.5, 1}, Belnap-style four-valued logic, etc.). The actual flagship paper studies **binary-valued** Boolean functions of **3 to 8 variables**. The README is now grounded in that source.

---

## 📄 Files

| File | Role |
|------|------|
| [`boolean_research_paper.md`](boolean_research_paper.md) | Flagship paper — *Dimensional emergence and structural complexity in Boolean algebras of three to eight variables* |
| [`three_var_boolean_analysis.md`](three_var_boolean_analysis.md) | Companion analysis at $n=3$ |
| [`four_var_boolean_universe.md`](four_var_boolean_universe.md) | Companion at $n=4$ |
| [`five_var_boolean_frontier.md`](five_var_boolean_frontier.md) | Companion at $n=5$ — full enumeration ends here; $n\ge 5$ moves to sampling |
| [`six_var_boolean_transcendence.md`](six_var_boolean_transcendence.md) | Companion at $n=6$ |
| [`seven_var_perfect_democracy.md`](seven_var_perfect_democracy.md) | Companion at $n=7$ |
| [`eight_var_digital_perfection.md`](eight_var_digital_perfection.md) | Companion at $n=8$ |

---

## 🔑 Headline result — dimensional emergence

The fraction of **genuinely n-dimensional (irreducible)** functions — those that cannot be written as a composition of lower-dimensional functions — rises monotonically with $n$:

| $n$ | Total $2^{2^n}$ | Linear / affine $2^{n+1}$ | Irreducible fraction |
|-----|-----------------|----------------------------|-----------------------|
| 3 | 256 | 16 | ~25 % |
| 4 | 65 536 | 32 | rising |
| 5 | $\sim 4\times 10^9$ | 64 | rising |
| 6 | $\sim 1.8\times 10^{19}$ | 128 | high |
| 7 | $\sim 3.4\times 10^{38}$ | 256 | very high |
| 8 | $\sim 1.2\times 10^{77}$ | 512 | **~99.9 %** |

By $n=8$, almost every function is genuinely 8-dimensional and resists low-dimensional decomposition. The paper frames this as **dimensional emergence** — a complexity threshold beyond which the structural landscape becomes effectively irreducible.

---

## 🧰 Function families catalogued

For each $n$ the paper tracks six structural quantities (paper §1):

1. **Total function count** $2^{2^n}$
2. **Linear functions** (affine maps over $\mathrm{GF}(2)$) — exact count $2^{n+1}$
3. **Balanced functions** (Hamming weight $2^{n-1}$) — critical for crypto and quantum superposition
4. **Self-dual functions** (invariant under complementation)
5. **Threshold / majority functions** $T_k^n$ — output 1 iff at least $k$ of $n$ inputs are 1
6. **Genuinely n-dimensional (irreducible) functions**

### Bent functions (maximally nonlinear)

A function is **bent** iff all Walsh-Hadamard coefficients satisfy $|\hat H f(a)| = 2^{n/2}$ — equivalent to all derivatives $D_a f$ being balanced for $a\ne 0$. Achievable only for **even $n$**. Maximum nonlinearity is $2^{n-1} - 2^{n/2-1}$. Bent functions are not themselves balanced, so they cannot serve directly as cipher combiners — but they underpin AES-style S-box construction, Kerdock codes, and difference sets. Exact bent-function counts are known only up to $n=8$.

---

## 🎯 Three application domains (paper §3–§5)

1. **Cryptographic primitives** — bent functions, balanced near-bent constructions, AES-style S-box design, linear / differential cryptanalysis resistance.
2. **Quantum error correction** — the **Steane $[\![7,1,3]\!]$ code** as a concrete CSS construction; mapping of parity / linearity structure of Boolean functions to stabiliser codes.
3. **Byzantine-fault-tolerant n-modular redundancy** — threshold and majority functions as the kernel of NMR voting and Byzantine agreement protocols.

The paper provides a scaling table from $n=2$ through $n=8$ tying each domain's parameters to dimensional structure.

---

## 🔬 Method

- **Exact enumeration** for $n\le 4$ (256 and 65 536 functions, respectively).
- **Statistically sound sampling** for $n=5$ through $n=8$, where complete enumeration is computationally infeasible.
- Walsh-Hadamard transform machinery for nonlinearity / bent characterisation.
- Composition / projection tests for irreducibility.

---

## 🚧 Honest framing

- For $n\ge 5$ the irreducibility fractions are **statistical estimates** from sampling, not exact counts.
- Exact bent-function counts are known only up to $n=8$; beyond that, the paper does not extrapolate.
- The mapping to applications (S-boxes, Steane code, NMR voting) is explanatory rather than constructive — the paper does not propose new ciphers or QEC codes.

---

## 🔗 Related work in this repo

- [`GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — seven-paper series on $\mathrm{GF}(2)$ algebra; Boolean functions as the study object, taxonomy of binary operators, GF(2) Ring Uniqueness Theorem
- [`General Math Papers/`](../General%20Math%20Papers/) — LCRP / complexity-reduction principle (Walsh-Hadamard transform sits in the FFT class of reductions)
- [`Veritas/`](../Veritas/) — formal verification (Boolean structure underpins much of propositional logic / SAT)
- [`Break AES/`](../Break%20AES/) — cryptanalysis context for the bent-function / S-box discussion
- [`Compression Algorithms/`](../Compression%20Algorithms/) — algebraic compression theory (GRIA grade interacts with Boolean operator taxonomy)

---

[← Back to main README](../README.md)
