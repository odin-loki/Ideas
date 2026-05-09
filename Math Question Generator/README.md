# Math Question Generator — `MegaMathGen` + a 13-domain survey

> **Two complementary deliverables.** A 5 200-line Python generator (`Math-Gen.py` / "MegaMathGen") that produces an unlimited supply of mathematical problems across the full mathematical landscape, paired with a research-grade survey of those thirteen domains intended as the *reference map* the generator targets.

---

## 🎓 What this folder is

A research paper plus a working generator. The paper is a domain map; the generator implements problem synthesis across that map.

| File | Role |
|---|---|
| [`mathgen research paper.md`](mathgen%20research%20paper.md) | **The Landscape of Modern Mathematics** — comprehensive survey of 13 core domains (Number Theory · Algebra · Analysis · Geometry · Combinatorics · Logic & Foundations · Differential Equations · Numerical Analysis · Probability & Statistics · Operations Research · Computational Mathematics · Financial Mathematics · Elementary Mathematics). Cites recent landmarks (2024 Geometric Langlands proof; Brauer height-zero; Maynard's prime-gap work; PINNs / neural operators; SciML). |
| [`Math-Gen.py`](Math-Gen.py) | **MegaMathGen** — a continuous problem generator built on `sympy` + `numpy`. Memory-managed (stays under ~28 GB RAM), disk + time estimates before generation, checkpointing to recover from leaks / crashes, and `tqdm` progress tracking. Designed to run open-ended and produce gigabyte-to-terabyte corpora. |

---

## 🧮 What MegaMathGen actually generates

Per the script's own header, its scope is: **complete statistical coverage of all possible numbers and problems**, across the thirteen survey domains. It uses `sympy` for symbolic generation (`solve`, `Eq`, `simplify`, `expand`, `factor`, `limit`, `diff`, `integrate`, matrix work) plus `numpy` for numerical sampling, with `Fraction`/`Decimal` to keep exact rationals where appropriate.

The implementation is one file, large (~5 200 lines), and self-contained — no external corpus is required. Rerunning produces a fresh dataset.

> Earlier README copy listed properties ("Single Solution", "Verifiable", "Educational", "Scalable", "Difficulty-Ranked") as if they were established design principles. The script is more pragmatic than that: it is an *enumeration / synthesis* engine first, not a curated assessment platform. Treat the paper as the map and `Math-Gen.py` as the generator that traverses it.

---

## 🚧 Honest framing

- The survey paper is a long synthesis with citations; it does not propose new mathematics, it is intended to anchor the generator's coverage.
- The generator runs open-ended; quality / pedagogical value of individual problems is not formally controlled — they are mathematically valid by construction (because they are generated symbolically), but the *interestingness* gradient is left to downstream filtering.
- `Math-Gen.py` requires `sympy`, `numpy`, and `tqdm`. There is no `requirements.txt` in this folder.

---

## 🔗 Related work in this repo

- [`../General Math Papers/`](../General%20Math%20Papers/) — Logarithmic Complexity Reduction Principle, the lone math paper that didn't fit elsewhere
- [`../Statistical Generation/`](../Statistical%20Generation/) — generative theory (category-theoretic + Lévy-process framework)
- [`../3 to 8 Value Boolean Algebra/`](../3%20to%208%20Value%20Boolean%20Algebra/) — Boolean function spaces $f:\\{0,1\\}^n\\to\\{0,1\\}$ for $n=3..8$
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — algebraic backbone
- [`../Veritas/`](../Veritas/) — formal verification (relevant for verifying generator outputs)

---

[← Back to main README](../README.md)
