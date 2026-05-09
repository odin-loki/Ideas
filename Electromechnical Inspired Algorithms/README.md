# Electromechnical Inspired Algorithms

> **Three historical computing machines — Babbage's Difference Engine, the Antikythera Mechanism (military reframe), and the WWII Submarine Torpedo Data Computer — refactored into modern numerical algorithms with measured Python benchmarks: Babbage's finite-difference recurrence with cache-friendly in-place loops gets a **`4.92 ×` speedup** on order-2 differences over 2048 points; the Antikythera-prime Fourier reconstruction posts a **`386 ×` speedup** vs naive Python at 5 000 points; and the digital-TDC fire-control solver targets **`> 1 000 000 solutions per second` at `±0.015°` accuracy**.** Three triplets of (paper + companion document + Python implementation) make the case that ancient and obsolete computational machinery still hides modern algorithmic insights — particularly around cache locality (Babbage), prime-based rational approximation (Antikythera), and real-time geometric law-of-sines integration (TDC).

> **Spelling note.** Folder name is `Electromechnical Inspired Algorithms` (one *l*) — preserved as written.

---

## What this folder is

The proposition that mechanical and electromechanical computers contain hidden modern algorithmic insight is not new — Knuth's discussion of the Analytical Engine, Hodges' biography of Turing, and the modern reverse-engineering of the Antikythera Mechanism all touch on it. What this folder adds is *runnable code with measured benchmarks*: each of the three historical machines gets refactored into a modern numerical algorithm, the algorithm is implemented in Python, and the timing is recorded. Babbage's machine becomes a cache-friendly finite-difference loop with documented `~4.92 ×` speedup over the traditional allocation pattern. The Antikythera Mechanism (read here as a "military" device — the reframing is the author's, not the archaeological consensus) becomes an epicyclic Fourier-reconstruction algorithm using prime-numbered gear ratios; the small-prime expansion over `{7, 17, 19, 53, 127, 223}` allows continued-fraction rational approximation at `O(log Q)` cost and yields a `386 ×` speedup at 5 000 points. The Torpedo Data Computer becomes a streaming real-time law-of-sines geometric solver targeting `> 10⁶` solutions/s and `±0.015°` accuracy.

The pitch is "what computational ideas have we lost?" — and the answer, with three case studies, is "more than you'd think."

---

## 📑 Source documents

### Babbage Difference Engine

| File | Role |
|---|---|
| [`paper1_babbage_difference_engine.md`](paper1_babbage_difference_engine.md) | Research paper. Δⁿ formula with binomial coefficients. In-place vs traditional-allocation memory pattern. Order-4 ultimate-loop unrolling `[1, −4, 6, −4, 1]`. |
| [`babbage_difference_engine_algorithm.md`](babbage_difference_engine_algorithm.md) | Companion algorithm doc. |
| [`babbage_python_implementation.py`](babbage_python_implementation.py) | Python implementation. |

### Military Antikythera

| File | Role |
|---|---|
| [`paper2_military_antikythera.md`](paper2_military_antikythera.md) | Research paper. Prime ratios `{7, 17, 19, 53, 127, 223}`. Complex-exponential epicyclic model `z(t) = Σ A_k · exp(i(ω_k t + φ_k))`. Continued-fraction `O(log Q)`. |
| [`complete_military_antikythera_specification.md`](complete_military_antikythera_specification.md) | Complete specification. |
| [`military_antikythera.py`](military_antikythera.py) | Python implementation. Constants: `ANTIKYTHERA_PRIMES = [7, 17, 19, 53, 127, 223, 253, 319]` (note the extra entries vs the paper's classical prime list). |

### Torpedo Data Computer

| File | Role |
|---|---|
| [`paper3_torpedo_data_computer.md`](paper3_torpedo_data_computer.md) | Research paper. Law-of-sines forms: `sin(γ)/V_p = sin(AoB)/V_t`, `sin(δ) = (V_p / V_t) sin(AoB)`. Reach / turn / parallax corrections as `arcsin / arctan` composites. Digital-integrator friction model `0.03 / update`. |
| [`tdc_complete_documentation.md`](tdc_complete_documentation.md) | Complete documentation. |
| [`tdc_python_showcase.py`](tdc_python_showcase.py) | Python implementation. Header asserts: `> 10⁶` solutions/s, `±0.015°` accuracy, `85 %+` solution validity (improved from `24 %`). |

---

## 📊 Reported benchmarks

### Babbage — finite differences

`1 000`-iteration averages, 2 048 points, order 2 differences:

| Implementation | Time | Speedup |
|---|---|---|
| Traditional allocation | `0.0295 ms` | 1 × |
| In-place | `0.0070 ms` | `~4.21 ×` |
| **Ultimate loop-unrolled** | **`0.0060 ms`** | **`~4.92 ×`** |

Pattern: `50 – 80 %` memory reduction across multi-order calculations. Asymptotic class is unchanged (`O(N)` per order); the gains are constant-factor — exactly the kind of cache-locality optimisation modern hardware rewards heavily.

### Antikythera — Fourier reconstruction

| Configuration | Result |
|---|---|
| 5 000 points, naive Python | baseline |
| 5 000 points, prime-Fourier reconstruction | **`386 ×` speedup** |
| Complexity | `O(N · |P|)` for naive Fourier-mode reconstruction |

### Torpedo Data Computer

| Metric | Target |
|---|---|
| Solutions per second | **`> 1 000 000`** |
| Angular accuracy | **`±0.015°`** |
| Gyro envelope | `±180°` (extended from legacy) |
| 24-hour memory budget | `5.3 MB` |
| Solution validity | `85 %+` (improved from `24 %`) |

---

## 🚧 Honest caveats

- **Papers rely heavily on secondary citations** (Wikipedia, Nature summary articles invoked in-text) for the historical machines.
- **"Military Antikythera" is the author's reframing**, not the archaeological consensus on the device's function.
- **Python showcase headers contain marketing-style assertions** (`>10⁶ solutions/s`, `±0.015°`) that should not be conflated with verified naval-qualification testing.
- **`military_antikythera.py` lists `ANTIKYTHERA_PRIMES = [7, 17, 19, 53, 127, 223, 253, 319]`** — `253` and `319` are not prime and appear to be composites added for empirical fit; the paper's classical prime-only list is the cleaner mathematical statement.
- **No independent benchmark logs** are attached in the snippets reviewed.

---

## 🎯 What this displaces

| Standard | What it misses | What this trio offers |
|---|---|---|
| Modern textbook FFT | "FFT is fast, end of story" | Prime-Fourier rational approximation as alternative |
| `numpy.diff` | Allocation overhead at small N | Cache-friendly in-place patterns benchmarked |
| Real-time geometry solvers | Modern frameworks | TDC as streaming integrator with friction-damping model |

---

## 🔗 Related work in this repo

- [`../General Math Papers/`](../General%20Math%20Papers/) — LCRP framework (the Antikythera continued-fraction `O(log Q)` is in this family)
- [`../Statistical Generation/`](../Statistical%20Generation/) — Lévy / category-theory machinery
- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — TDC-style real-time fire-control geometry
- [`../Filtering/`](../Filtering/) — adjacent real-time filtering
- [`../Math Question Generator/`](../Math%20Question%20Generator/) — algorithms domain
- [`../Future C++/`](../Future%20C++/) — language-design adjacent (cache-locality discussion)

---

[← Back to main README](../README.md)
