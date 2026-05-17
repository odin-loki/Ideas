# Modelling AES — neural approaches to AES analysis, both ways round

> **Two complementary papers that come at AES from opposite directions and arrive at the same answer.** [`neural_aes_paper.md`](neural_aes_paper.md) asks *can a neural network recover an AES-128 key from `(plaintext, ciphertext)` pairs?* and constructs a three-barrier infeasibility argument backed by `0.675 %` first-byte test accuracy against a `0.3906 %` random baseline (`+0.28` pp, `z = 1.84`, `p = 0.066` — not significant at `α = 0.05`). [`Break AES with NNs/`](Break%20AES%20with%20NNs/) holds the scaffolding for one such attempted attack — a Transformer-distillation-plus-policy-gradient stack the recovery paper analyses. [`neural_prng_paper.md`](neural_prng_paper.md) asks the dual question *can a neural network generate output statistically indistinguishable from AES?* and reports a partial-convergence result: a GAN reaches `7.983 / 8.0` bits byte entropy and gzip compression ratio `1.0005` (matching AES) but fails chi-squared uniformity at `p ≈ 0`, with the most-tuned WGAN + sequential critic + chi-squared auxiliary configuration ending at `2 / 4` tests passed. The two papers cross-reference each other: the recovery paper predicts that any sufficiently-trained generative model on AES data will collapse toward approximating AES's marginal output distribution rather than learning key structure ("pseudorandom collapse"), and the generator paper measures exactly how close that approximation gets and where it breaks.

> **Genre note.** Research-paper register throughout. The folder pairs a result-bearing pair of papers with an honest record of one experimental scaffolding that motivated the negative side of the analysis. The scaffolding is non-runnable as written; the papers stand on their own.

---

## 📑 What this folder is

A two-direction study of what neural networks can and cannot learn about AES-128:

- **Inverse direction — *can a network recover key material from ciphertext?*** Treated in [`neural_aes_paper.md`](neural_aes_paper.md). Three independent infeasibility arguments — entropy indistinguishability, pseudorandom collapse, and combinatorial state-space infeasibility — backed by five experiments on AES-128. Verdict: **no**, not from `(plaintext, ciphertext)` pairs alone, and the paper is precise about *why* and *how far from chance* the best black-box attack gets.
- **Forward direction — *can a network produce output statistically equivalent to AES?*** Treated in [`neural_prng_paper.md`](neural_prng_paper.md). Three increasingly capable architectures (shallow MLP, deep MLP, GAN — with LSTM as a known-collapse control), plus a WGAN-GP and a final WGAN + sequential critic + chi-squared auxiliary loss configuration. Verdict: **partial**. Entropy and compression match AES; chi-squared uniformity at `n = 96 000` bytes does not.
- **The scaffolding itself.** [`Break AES with NNs/`](Break%20AES%20with%20NNs/) contains the Transformer + RL training stack that was pointed at the recovery problem, plus an informal convergence note and an architecture diagram. The scaffolding is *not* a result — it is the experimental setup whose dead-end the inverse-direction paper formalises.

The two papers cross-reference each other explicitly. [`neural_aes_paper.md`](neural_aes_paper.md) §4.2 ("Pseudorandom Collapse") predicts the failure mode that [`neural_prng_paper.md`](neural_prng_paper.md) §5.2 ("The Distribution-Matching Ceiling") then *measures*. [`neural_prng_paper.md`](neural_prng_paper.md) §1 calls the recovery paper its "companion".

---

## 📑 Source organisation

| File / folder | Role | Status |
|---|---|---|
| [`neural_aes_paper.md`](neural_aes_paper.md) | **Inverse-direction paper.** Neural key recovery against AES-128: theoretical and empirical infeasibility analysis. Three barriers, five experiments, FIPS-vector AES-128. | Result-bearing paper |
| [`neural_prng_paper.md`](neural_prng_paper.md) | **Forward-direction paper.** Learning AES-style pseudorandomness: shallow MLP, deep MLP, LSTM, GAN-BCE, WGAN-GP, and WGAN + sequential critic + chi-squared auxiliary loss. | Result-bearing paper |
| [`Break AES with NNs/`](Break%20AES%20with%20NNs/) | **Recovery-attempt scaffolding.** Transformer student + Llama-teacher distillation + REINFORCE with BLEU reward. Non-runnable as written; included as honest record. | Research scaffolding, not a result |
| [`Break AES with NNs/complete-transformer-rl.py`](Break%20AES%20with%20NNs/complete-transformer-rl.py) | Training scaffolding. `d_model = 512`, `8` heads, `6 + 6` layers, distillation temperature `τ = 2.0`, REINFORCE with `Categorical` sampling, baseline decay `0.99`, entropy bonus `0.01`, gradient clip `1.0`. | Documented bugs — see subfolder README |
| [`Break AES with NNs/math-proof.md`](Break%20AES%20with%20NNs/math-proof.md) | Informal convergence note citing Kushner–Clark, sketching `O(1/ε²)` distillation and `O(1/(1 − γ)³ ε²)` RL sample complexity. Self-described as "not venue-ready". | Informal note |
| [`Break AES with NNs/transformer-architecture.mermaid`](Break%20AES%20with%20NNs/transformer-architecture.mermaid) | Architecture diagram (Mermaid). | Diagram |
| [`Break AES with NNs/Architecture.PNG`](Break%20AES%20with%20NNs/Architecture.PNG) | Architecture diagram (raster). | Diagram |

---

## 🎯 The two questions in one sentence each

**[`neural_aes_paper.md`](neural_aes_paper.md):** *Can a neural network trained on `(plaintext, ciphertext)` pairs recover AES-128 key material?* — **No**, and the paper formalises three independent reasons for it and measures the chance-level performance directly.

**[`neural_prng_paper.md`](neural_prng_paper.md):** *Can a neural network trained on AES-128 output samples generate output statistically indistinguishable from AES, without access to any key or cipher internals?* — **Partially**: entropy and compression match AES; chi-squared uniformity does not, regardless of objective (MSE / BCE / Wasserstein) or training duration tested.

---

## 📊 Key empirical results

### Inverse direction — `neural_aes_paper.md`

**Variable-key first-byte recovery (the correct experimental protocol).** 20 000 training samples / 4 000 test samples, each with an independently sampled random 16-byte key. Three-layer MLP `Linear(32 → 512) → ReLU → LayerNorm → Linear(512 → 512) → ReLU → Linear(512 → 256)`, 20 epochs, Adam `lr = 1e-3`, batch 256.

| Epoch | Train loss (nats) | Test acc | vs random chance |
|---|---|---|---|
| 5 | `5.4368` | `0.4000 %` | `+0.0094` pp |
| 10 | `3.7421` | `0.5250 %` | `+0.1344` pp |
| 15 | `1.4845` | `0.5000 %` | `+0.1094` pp |
| 20 | `0.2696` | `0.4750 %` | `+0.0844` pp |

- Random chance baseline: **`0.3906 %`** (`1 / 256`)
- Best accuracy observed: **`0.6750 %`**
- Gain over chance: **`+0.2844`** pp
- Two-proportion *z*-test on the gain: `z = 1.84`, `p = 0.066` — **not significant** at `α = 0.05`
- Training loss descends to `0.27` nats — below the `ln(256) = 5.5452` nat uniform floor — while test accuracy stays at chance. Signature of pure memorisation with zero generalisation.

**Why the "fixed-key" version is meaningless.** When the key is held constant, every label is identical (`0x2B = 43` for the FIPS test vector). A network learns to predict that constant in `< 5` epochs and reports `100 %` test accuracy. The paper calls this the **naive constant-label trap** and gives it a section of its own (§5.2).

**Entropy and chi-squared on AES-128 output itself.**

| Source | Byte entropy (bits) | Chi-squared p (uniformity) |
|---|---|---|
| Uniform | `8.0000` | — |
| AES-128 ciphertext | `7.9989` | `p = 0.6637` (cannot reject uniform) |
| NN per-prediction entropy | `2.97` (collapsed) | — |

**State-space barrier (Table 2 of the paper).** A 50 %-coverage lookup table for a *single fixed* AES-128 key requires `~ 2^64 ≈ 1.84 × 10^19` samples = **`5.90 × 10^8` TB**, roughly `4.9 ×` total world data storage. The published-results extrapolation `N_samples ≈ 2121 × 2^(0.559·k)` gives `7.58 × 10^24` samples for 128-bit recovery — `2.40 × 10^8` years at `10^9` samples per second.

### Forward direction — `neural_prng_paper.md`

**Headline architecture comparison at convergence (96 000 test bytes):**

| Source | Entropy (bits) | Chi² p | Lag-1 AC | Compression | Tests passed |
|---|---|---|---|---|---|
| AES-128 reference | `7.9977` | `0.5388` | `−0.00008` | `1.0005` | **`4 / 4`** |
| True random | `7.9976` | `0.2428` | `+0.00394` | `1.0005` | `4 / 4` |
| LSTM (MSE) | `0.0000` | `0.0000` | NaN | `0.0013` | `0 / 4` |
| Shallow MLP (MSE, 15 ep) | `6.3430` | `0.0000` | `−0.00042` | `0.8028` | `1 / 4` |
| Deep MLP (MSE, 25 ep) | `7.7612` | `0.0000` | `−0.00586` | `0.9792` | `1 / 4` |
| Deep MLP (converged, 101 ep) | `7.8038` | `0.0000` | `+0.00422` | `0.9839` | `1 / 4` |
| GAN-BCE (25 ep) | **`7.9831`** | `0.0000` | `−0.00541` | **`1.0005`** | **`3 / 4`** |
| GAN-BCE (converged, 120 ep) | `7.9800` | `0.0000` | `−0.02876` | `1.0004` | `2 / 4` |
| WGAN-GP (80 ep) | `7.9844` | `0.0000` | `+0.01322` | `1.0004` | `1 / 4` |
| WGAN + SeqC + χ² aux (110 ep) | `7.9928` | `0.0000` | `+0.00697` | `1.0004` | `2 / 4` |

Test thresholds (NIST SP 800-22 adapted): entropy `≥ 7.99` bits, chi-squared `p > 0.05`, `|r| < 0.01`, compression `≥ 1.0`.

**Four headline findings:**

1. **GAN-BCE at 25 epochs is the high-water mark on tests-passed**, at `3 / 4`. Entropy, autocorrelation, and compression all clear threshold; chi-squared does not.
2. **Chi-squared cannot be unlocked** by any of the objectives tested (MSE, BCE, Wasserstein) or by training to convergence. At `n = 96 000` bytes against `255` degrees of freedom, the minimum-detectable per-bin deviation is `δ_min ≈ √(293 / 96 000) ≈ 0.055`. The trained generators always retain at least this much aggregate non-uniformity.
3. **Inter-output-byte correlation is the proximate cause.** SVD-based weight extraction of the converged GAN gives mean `| inter-byte correlation | = 0.433`, max `0.926`. AES outputs have `~ 0` inter-byte correlation. All 16 output bytes are functions of the same 32 / 128-dimensional seed, so they are algebraically dependent even when marginally uniform.
4. **The LSTM collapses to a constant**, as predicted: optimal MSE on a uniform target is `0.5`, MSE `= Var(Uniform[0,1]) = 1/12 ≈ 0.0833`, and the LSTM converges to exactly that loss (`0.0840` at epoch 15).

**Closed-form weight extraction (§10).** The trained GAN's three weight matrices are full effective rank (`32`, `128`, `16`). After folding BatchNorm and reducing to `(128, 128, 64)` ranks, the result is a **4-layer Gaussian-seed-driven random-projection cascade with independent LeakyReLU(0.2) gating** — 268 128 float32 parameters (`42.5 %` reduction over the full model), 24 653 blocks/sec on a single CPU core, with autocorrelation `−0.000236` (two orders of magnitude better than the full model's `+0.0073`). Chi-squared still fails. **The weights are the algorithm**; the generator does not reduce to a simpler closed form. The paper draws an explicit analogy with AES itself — an irreducible nonlinear mixing function defined by a fixed parameter set.

---

## 🚧 Honest framing

- **Neither paper claims to break AES.** The inverse-direction paper is an *infeasibility* result: it formalises and measures the gap between neural training and key recovery. The forward-direction paper is a *partial-convergence* result: it documents what GAN-class architectures can and cannot match about AES output.
- **`Break AES with NNs/` is scaffolding, not a result.** The Python file is non-runnable as written — undefined data loaders, BLEU called on tensors, `pytest.main([__file__])` at the top of the file. The math note is self-described as informal. The honest version of the subfolder README at [`Break AES with NNs/README.md`](Break%20AES%20with%20NNs/README.md) lays all of this out in a "What's actually here" table.
- **The two papers cite each other and share notation.** "Pseudorandom collapse" is defined in the recovery paper §4.2 and measured in the generator paper §5.2 and §10.4. The 96 000-byte chi-squared barrier in the generator paper is the dual of the 0.3906 % chance baseline in the recovery paper — both are the residual-uniformity floor that neural training is unable to penetrate from each direction.
- **AES remains secure under the standard PRF / IND-CPA model.** Nothing in this folder undermines that assumption; the inverse-direction paper relies on it as a premise, and the forward-direction paper relies on it for the statistical-benchmark properties of AES output. Do not interpret either paper as a cryptanalytic recipe.
- **Side-channel and reduced-round results are out of scope.** The recovery paper §6.1 ("Where Neural Cryptanalysis Does Work") explicitly separates the algebraic black-box regime analysed here from (a) reduced-round toy ciphers (S-AES, S-SPECK), (b) side-channel attacks on physical implementations (ASCAD-style EM-trace neural classifiers), and (c) Gohr-style differential-neural distinguishers on Speck32/64 and Simon. Those regimes are feasible; the regime analysed here is not.
- **Numbers are extracted from the papers, not invented.** Every quantity in this README is taken directly from [`neural_aes_paper.md`](neural_aes_paper.md) or [`neural_prng_paper.md`](neural_prng_paper.md). If the papers update, so should this.

---

## 🔗 Related work in this repo

- [`../ARIA Encryption Algorithm/`](../ARIA%20Encryption%20Algorithm/) — the *build* side of the same problem space: a custom AEAD construction over `GF(2^256)` that does not transmit nonces. Reads as the constructive counterpart to the inverse-direction paper here.
- [`../GF2 Algebra and Applications/`](../GF2%20Algebra%20and%20Applications/) — the proper algebraic underpinnings for finite-field cryptanalysis: ring theorems over `GF(2)`, a polynomial form for the AES inverse (`x⁻¹ = x²⁵⁴` is one of 128 permutations on `GF(2^8)`), and gate-count benchmarks. The algebraic regime that neural training is *not* in.
- [`../Compression Algorithms/`](../Compression%20Algorithms/) — gzip compression as a test of pseudorandomness here directly mirrors the entropy/redundancy framing used in Izaac/GRIA/NMP. The generator paper's compression-ratio metric is exactly the test that an Izaac-style observer would apply.
- [`../Veritas/`](../Veritas/) — the formal verification / PAC-bound machinery that an honest cryptanalysis would need. Both papers here use informal complexity sketches (the generator paper avoids them; the inverse-direction paper sketches them in `Break AES with NNs/math-proof.md` and labels them as not venue-ready).
- [`../RNGS/`](../RNGS/) — the four production-grade random number generators in the repo. The forward-direction paper's WGAN + sequential critic generator is in a strictly different regime: it passes entropy and compression but fails formal chi-squared and is *not* a cryptographic RNG.
- [`../Cypha/`](../Cypha/) — natural-parameter-space classification framework. The "pseudorandom collapse" failure mode is structurally a collapse to the class-conditional prior with no informative offset, which is a Cypha-style way to frame the same observation.

---

## 🧭 How to read this folder

1. Start with [`neural_aes_paper.md`](neural_aes_paper.md) §4 (the three barriers) and §5.3 (the variable-key experiment).
2. Then read [`neural_prng_paper.md`](neural_prng_paper.md) §4 (the architecture-by-architecture results), §5 (why GAN passes entropy and compression but fails chi-squared), and §10 (the weight extraction).
3. Treat [`Break AES with NNs/`](Break%20AES%20with%20NNs/) as a historical record of the scaffolding the recovery paper was written *against* — see its own [`README.md`](Break%20AES%20with%20NNs/README.md) for the honest summary of what the code does and does not do.

---

[← Back to main README](../README.md)
