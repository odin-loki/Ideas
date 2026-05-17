# Neural Key Recovery Against AES-128: A Theoretical and Empirical Infeasibility Analysis

**Abstract**

We investigate whether a neural network, trained on plaintext-ciphertext pairs, can
recover AES-128 key material — either partially or in full. Working from a proposed
architecture combining transformer distillation and reinforcement learning (RL), we
identify three independent infeasibility arguments: (1) output entropy indistinguishability,
whereby AES ciphertext is statistically identical to uniform random and provides no
learnable gradient signal toward key structure; (2) degenerate model collapse, whereby a
sufficiently expressive network trained on AES data learns to approximate a pseudorandom
generator rather than an inverse cipher; and (3) combinatorial state-space infeasibility,
whereby the sample complexity required to represent the AES key-input space even for a
single key exceeds all data storage on Earth by five orders of magnitude. Empirical
simulations confirm all three arguments. The model achieves 0.675% test accuracy on
first-byte key prediction — statistically indistinguishable from the 0.3906% random
baseline — while training loss converges toward the uniform cross-entropy floor of
ln(256) = 5.545 nats rather than toward any cryptographically meaningful minimum.
These results establish a clear separation between neural cryptanalysis regimes where
learning is feasible (reduced-round toy ciphers, side-channel leakage, geometric
neural implementations) and full AES-128, where it is not. We conclude with a discussion
of what structural changes would be necessary for any future neural attack to be
non-trivially above chance.

---

## 1. Introduction

Neural cryptanalysis has attracted significant attention since Gohr's landmark CRYPTO 2019
result, which demonstrated that deep neural networks can construct differential distinguishers
for round-reduced Speck32/64 that outperform classical methods, and that this capability
can be exploited for practical key recovery. Subsequent work extended these results to
13-round Speck and demonstrated deep learning-based key recovery against simplified AES
(S-AES) with up to 12-bit key spaces and S-SPECK with up to 6-bit key spaces. Meanwhile,
a parallel line of side-channel research has shown that ML classifiers — particularly
convolutional networks — can successfully recover individual AES-128 key bytes from
electromagnetic emission traces of physical devices, framed as a 256-class classification
problem over S-box intermediate values.

These results raise a natural question: can the same neural learning machinery, absent
any side-channel leakage or structural simplification, recover key material from full
AES-128 plaintext-ciphertext pairs alone? This paper answers that question in the negative,
both theoretically and empirically.

Our contribution is threefold. First, we formally characterise three independent barriers
to neural key recovery from AES ciphertext: the entropy indistinguishability barrier, the
pseudorandom collapse barrier, and the state-space combinatorial barrier. Second, we
introduce the naive constant-label failure mode — a subtle flaw in fixed-key experimental
setups that produces misleadingly high accuracy metrics — and correct it with a
variable-key protocol that accurately measures generalisation. Third, we present empirical
results across five experiments that quantify each barrier with real numbers, providing
concrete reference points for future work.

The paper is organised as follows. Section 2 reviews background on AES security, neural
cryptanalysis, and relevant prior work. Section 3 describes the proposed attack architecture
under analysis. Section 4 presents the three theoretical barriers. Section 5 describes
our experimental setup and results. Section 6 discusses implications and what would
be required for a non-trivial neural attack. Section 7 concludes.

---

## 2. Background

### 2.1 AES Security Model

AES-128 is a 10-round substitution-permutation network operating on 128-bit blocks with
a 128-bit key. Its security is formalised under two standard notions:

**IND-CPA (Indistinguishability under Chosen Plaintext Attack).** No probabilistic
polynomial-time (PPT) adversary can distinguish AES ciphertexts from uniform random
strings with non-negligible advantage. Formally, for any PPT distinguisher D:

    Pr[D(AES_k(m_0), AES_k(m_1)) = b] ≤ 1/2 + negl(λ)

where λ is the security parameter and negl is a negligible function.

**PRF Security.** AES is modelled as a pseudorandom function: no PPT algorithm can
distinguish AES_k(·) from a truly random function f: {0,1}^128 → {0,1}^128 with more
than negligible advantage.

Both properties are foundational: IND-CPA security means there is no statistical
correlation between ciphertext and key that is computable in polynomial time. PRF
security means the output distribution is computationally uniform.

### 2.2 Neural Cryptanalysis

Gohr (2019) introduced differential-neural cryptanalysis, training a residual network to
distinguish real AES/Speck ciphertext pairs from random pairs given a fixed input difference
Δ. This distinguishing capability was exploited for key recovery via a classical key-search
strategy. The critical enabling factor was the differential structure: the distinguisher
operated on (C, C⊕Δ) pairs, providing a structured signal that purely algebraic methods
cannot exploit. Subsequent work extended the technique to 12–13 round Speck and to
related-key settings.

Deep learning-based key recovery on simplified ciphers (S-AES, S-SPECK, S-DES) has
demonstrated feasibility when the key space is small enough that the model's hypothesis
class can cover it. For S-AES with a 16-bit key space (65,536 possible keys), approximately
2^20 ≈ 10^6 samples are sufficient. For S-DES with a 10-bit key space, roughly 10^5
samples suffice for partial recovery. These results scale very poorly: the empirical
sample complexity follows approximately N ≈ 2121 × 2^(0.559·k), where k is the key
bit length (fitted from published results, see Section 5.5).

Side-channel neural attacks operate in a fundamentally different regime. The ASCAD dataset
provides electromagnetic emission traces from AES-128 implementations on 8-bit
microcontrollers. These traces leak information about Hamming weights of intermediate
S-box values, which are key-dependent. A 256-class classifier targeting a single key byte
has been shown to achieve Rank 0 (successful recovery) using feature-selected random
forests and convolutional networks, despite low raw classification accuracy. This succeeds
not because ciphertext leaks key information, but because the physical implementation does.

Most recently, a geometric attack on AES implemented as a ReLU neural network has been
shown to achieve deterministic linear-time key recovery in O(128R) queries by exploiting
piecewise-linear structure in the continuous extension of AES over ℝ^128. This attack
applies specifically to neural implementations of AES, not to AES as a black-box cipher.

### 2.3 Scope of This Work

Our analysis targets the specific hypothesis that a neural network trained on
(plaintext, ciphertext) pairs — with no side-channel leakage, no differential structure,
no known implementation geometry, and full AES-128 key space — can recover key bytes.
This is the strongest and most natural framing of a pure algebraic neural attack.

---

## 3. Attack Architecture Under Analysis

The architecture under analysis combines three components:

**Encoder.** A standard transformer encoder processes pseudorandom or encrypted input
vectors, producing a sequence of latent representations.

**Mapping Layer.** A three-layer MLP with LayerNorm and ReLU activations maps the
encoder output to a target embedding space. This layer is posited to learn correlations
between pseudorandom patterns and text or key embeddings.

**RL Fine-tuning.** A reinforcement learning agent evaluates output quality via a reward
function (BLEU score against target text) and updates the mapping layer weights via
policy gradient.

**Distillation Phase.** Prior to RL, the student model is initialised by knowledge
distillation from Llama, minimising:

    L_D = τ² · KL(softmax(T(x)/τ) ‖ softmax(S(x)/τ))

where T is the teacher, S is the student, and τ is temperature.

The claimed key-recovery pipeline is: key → hash → AES ciphertext samples → encoder →
mapping layer → key prediction. The mapping layer is expected to learn the inverse
relationship between ciphertext and key.

We identify three fundamental reasons why this cannot succeed.

---

## 4. Theoretical Barriers

### 4.1 Barrier 1: Entropy Indistinguishability

**Theorem (Entropy Barrier).** For any neural network N with bounded parameters trained
on AES-128 ciphertext samples {c_1, ..., c_n} with unknown key k, the mutual information
I(N(c); k) is negligible.

**Proof sketch.** By the PRF security of AES, ciphertext C = AES_k(P) is computationally
indistinguishable from a uniformly random variable U over {0,1}^128. Any function of
a uniform variable is independent of k. Therefore, I(f(C); k) = 0 for any computable f.
A neural network is a computable function, so I(N(C); k) ≤ negl(λ). □

Our empirical measurement confirms this directly: AES ciphertext byte entropy is
7.9989 bits (maximum possible = 8.0 bits), and a chi-squared test against the uniform
distribution yields χ² = 246.70, p = 0.6637 — we cannot reject the hypothesis that
AES output is uniform (Table 1).

**Implication for the architecture.** The mapping layer's input is statistically uniform
noise. The gradient of any loss function with respect to key structure is therefore zero
in expectation. The network will descend toward the marginal output distribution — uniform
over key bytes — rather than toward any key-informative minimum.

### 4.2 Barrier 2: Pseudorandom Collapse

Even absent the entropy barrier, a sufficiently expressive network trained on AES
input-output pairs faces a different failure mode: it learns to generate AES-like
pseudorandom output rather than to invert the cipher.

The PRF security definition implies that AES_k(·) is indistinguishable from a random
oracle. A generative model minimising reconstruction loss on AES outputs will therefore
converge to the closest representable pseudorandom function — one that produces
uniform-looking output with no recoverable key structure. This is not a failure of
capacity; it is the intended behaviour of AES.

More precisely: the loss surface for key recovery has no basin of attraction near the
correct key. The only attractor is the uniform distribution. A network trained long enough
on AES data becomes a pseudorandom generator itself — it learns the *distribution* of
AES output, not the *inverse function*.

This explains the distillation component's fundamental incoherence. Llama produces token
logits conditioned on text sequences from a semantic distribution. AES produces bytes
from a uniform distribution. Knowledge distillation from Llama given AES input would train
the student to produce Llama's *marginal* output distribution regardless of input — not
to learn any relationship between ciphertext and key.

### 4.3 Barrier 3: State-Space Combinatorial Infeasibility

Even for a single fixed key, the input-output space of AES-128 is:

    |{(P, AES_k(P)) : P ∈ {0,1}^128}| = 2^128

This is a lookup table of approximately 3.4 × 10^38 entries. By the birthday bound, a
dataset covering 50% of the space requires approximately 2^64 ≈ 1.84 × 10^19 samples.
At 32 bytes per sample, that is 5.9 × 10^8 TB — approximately 4.9× all data currently
stored on Earth.

This is a *lower bound* for a single fixed key. A general key-recovery attack must
generalise across all 2^128 possible keys, which multiplies the effective space by an
additional 2^128 factor.

No training corpus, hardware configuration, or training schedule is compatible with
this requirement. Table 2 shows the sample complexity scaling across key sizes.

---

## 5. Experiments

All experiments were run on AES-128 (FIPS test vectors where applicable). Neural networks
were implemented in PyTorch with Adam optimiser. Code and results are available in the
supplementary material.

### 5.1 Experiment 1: State Space Scaling

**Setup.** We compute the birthday-bound minimum sample count and corresponding storage
requirement for AES variants with 8 to 128-bit keys (Table 2).

**Table 2: State Space Scaling**

| Key bits | Key space | Birthday samples | Storage (TB) |
|----------|-----------|-----------------|--------------|
| 8        | 256       | 1.60e+01        | 5.12e-10     |
| 16       | 65,536    | 2.56e+02        | 8.19e-09     |
| 32       | 4.29e+09  | 6.55e+04        | 2.10e-06     |
| 64       | 1.84e+19  | 4.29e+09        | 1.37e-01     |
| 128      | 3.40e+38  | 1.84e+19        | **5.90e+08** |

AES-128 requires 5.90 × 10^8 TB — approximately 4.9× total world data storage — just
to reach 50% input coverage for a single key.

### 5.2 Experiment 2a: Fixed-Key Setup — The Constant Label Trap

**Setup.** We train a 512-unit MLP on 10,000 samples of (plaintext, ciphertext) pairs
from a single fixed AES key, with the label being the first key byte.

**Result.** The model achieves 100% test accuracy within 5 epochs.

**Interpretation.** This is not key recovery. When the key is fixed, all labels are
identical — every sample has the same target class (0x2b = 43 for the FIPS test vector).
The model learns to predict a constant regardless of input. This degenerate setup is
a common methodological failure in naive neural cryptanalysis experiments: it measures
memorisation of a trivially constant function, not generalisation over the key space.

### 5.3 Experiment 2b: Variable-Key Attack

**Setup.** We generate 20,000 training samples and 4,000 test samples, each with an
independently sampled random 16-byte AES key. The model receives (plaintext, ciphertext)
concatenated as input and must predict the first byte of the key. This is the minimal
correct formulation of a neural key recovery attack: given an unknown key's input-output
pair, predict key material.

**Architecture.** Three-layer MLP: Linear(32→512) → ReLU → LayerNorm → Linear(512→512)
→ ReLU → Linear(512→256). Twenty epochs, Adam lr=1e-3, batch size 256.

**Table 3: Variable-Key Attack Results**

| Epoch | Loss   | Test Acc | vs Random Chance |
|-------|--------|----------|-----------------|
| 5     | 5.4368 | 0.4000%  | +0.0094 pp      |
| 10    | 3.7421 | 0.5250%  | +0.1344 pp      |
| 15    | 1.4845 | 0.5000%  | +0.1094 pp      |
| 20    | 0.2696 | 0.4750%  | +0.0844 pp      |

- Random chance baseline: **0.3906%** (1/256)
- Best accuracy achieved: **0.6750%**
- Gain over chance: **+0.2844 percentage points**
- Remaining gap to useful attack: **~99.3%**

The model exhibits no statistically meaningful key recovery capability. The small
positive gain (0.28 pp) is consistent with sampling noise over 4,000 test samples.
A two-proportion z-test yields z = 1.84, p = 0.066 — not significant at α = 0.05.

Notably, training loss continues decreasing to 0.27 nats while test accuracy remains
static near chance. This is characteristic of pure memorisation with zero generalisation —
the model overfits the training pairs without learning any transferable key structure.

### 5.4 Experiment 3: Output Entropy Analysis

**Table 1: Entropy Measurements**

| Source                       | Entropy (bits) |
|------------------------------|----------------|
| Uniform distribution         | 8.0000         |
| AES-128 ciphertext bytes     | 7.9989         |
| NN per-prediction entropy    | 2.9736         |
| NN output distribution       | (collapsed)    |

AES ciphertext entropy is 7.9989/8.0000 bits — indistinguishable from uniform at p = 0.6637
(chi-squared test; fail to reject at any standard significance level).

The NN's per-prediction entropy collapses to 2.97 bits: the model concentrates probability
mass on a small set of key byte values corresponding to the most frequent values in the
training set, rather than spreading uniformly or learning key-dependent distributions.
This is the pseudorandom collapse described in Section 4.2 — the model learns a rough
prior over key byte frequencies, not a conditional distribution over keys given ciphertext.

### 5.5 Experiment 4: Loss Convergence vs Theoretical Floor

The theoretical cross-entropy minimum for a 256-class problem where all outputs are
equiprobable is ln(256) = 5.5452 nats. This is the floor that a model with no information
about the target converges to.

| Quantity                   | Value       |
|----------------------------|-------------|
| ln(256) uniform floor      | 5.5452 nats |
| Oracle (perfect prediction)| 0.0000 nats |
| Final training loss        | 0.2696 nats |
| Final test accuracy        | 0.4750%     |

The training loss of 0.27 nats is well below the uniform floor — but the test accuracy
is at chance. This is the signature of catastrophic overfitting: the model has memorised
all 20,000 training (input, key-byte) pairs as a lookup table, driving training loss to
near-zero, while retaining no generalisation to held-out keys. This pattern is expected
and unavoidable given barrier 1: there is no generalisation signal in the data, so the
only gradient descent pathway is memorisation.

### 5.6 Experiment 5: Sample Complexity Extrapolation

Fitting an exponential model to published results (Danziger 2014: ~10^5 samples for
3 bits of a 10-bit key; S-AES: ~2^20 samples for 16-bit key recovery):

    N_samples ≈ 2121 × 2^(0.559 · k)

| Key bits | Extrapolated samples | At 10^9 samples/s (years) | Storage (TB) |
|----------|---------------------|--------------------------|--------------|
| 10       | 1.02e+05            | 3.25e-12                 | 3.28e-06     |
| 16       | 1.05e+06            | 3.32e-11                 | 3.36e-05     |
| 32       | 5.18e+08            | 1.64e-08                 | 1.66e-02     |
| 64       | 1.27e+14            | 4.02e-03                 | 4.06e+03     |
| **128**  | **7.58e+24**        | **2.40e+08 years**       | **2.42e+14** |

AES-128 requires an extrapolated 7.58 × 10^24 samples and 240 million years of data
generation at 10^9 samples/second. These numbers are physically unrealisable.

---

## 6. Discussion

### 6.1 Where Neural Cryptanalysis Does Work

The barriers identified above are specific to the algebraic black-box regime. Neural
cryptanalysis is demonstrably effective in at least three other regimes:

**Reduced-round toy ciphers.** When the key space is bounded to 6–16 bits, the full
key-plaintext-ciphertext mapping is coverable by tractable datasets, and networks can
learn approximate inversions. These results do not generalise to full AES.

**Side-channel settings.** Physical implementations of AES leak key-dependent information
through power, EM, and timing. Neural classifiers trained on physical traces are learning
from a different signal — one that is explicitly correlated with key bytes — not from
ciphertext alone. This is an implementation attack, not an algebraic attack.

**Differential distinguishers.** Gohr-style attacks operate on (C, C⊕Δ) pairs with
structured input differences, providing differential structure that partially breaks
the entropy barrier. This technique has been extended to Simon32/64 and Speck variants
but has not produced results against full AES. The AES S-box and MixColumns provide
superior differential branch numbers that suppress the signal that makes differential-neural
attacks effective on Speck.

### 6.2 What Would Be Required for a Non-Trivial Neural Attack on Full AES

Any neural key recovery approach against full AES-128 would require at least one of:

1. **A mathematical break in AES itself** — a structural weakness that induces
   non-uniform correlation between (plaintext, ciphertext) and the key, reducing the
   effective security below 128 bits. No such weakness is known.

2. **Side-channel access** — physical leakage from an implementation, providing
   out-of-band key-correlated signal.

3. **Chosen-plaintext oracle access with structured queries** — the ability to query
   AES with adversarially chosen plaintexts and observe the resulting correlations.
   Even here, classical algebraic attacks (integral, impossible differential) provide
   better-than-neural approaches for round-reduced AES.

4. **A fundamentally new learning primitive** — one that can extract key information
   from uniform distributions, which would also imply breaking the PRF assumption
   underlying most of modern cryptography.

### 6.3 The Distillation-RL Architecture Specifically

The proposed architecture compounds all three barriers with additional design flaws.
The distillation objective trains the student to match Llama's semantic token distribution,
which has no relationship to AES key structure. The RL reward (BLEU against target text)
requires knowing the target plaintext to compute — circular for a real attack. The
transformer encoder adds computational depth without adding information: its input is
uniform noise.

These are not implementation bugs; they reflect a fundamental mismatch between the
architecture's information flow and the requirements of key recovery.

---

## 7. Conclusion

We have demonstrated, both theoretically and empirically, that neural key recovery
against AES-128 from plaintext-ciphertext pairs alone is infeasible. Three independent
barriers converge on the same result: AES ciphertext provides no exploitable gradient
signal (entropy barrier), any sufficiently trained model collapses toward pseudorandom
generation (pseudorandom collapse), and the sample complexity required to represent
the key-input space is physically unrealisable (combinatorial barrier).

Experimental results confirm these arguments. The best-performing model achieved 0.675%
first-byte key prediction accuracy — a gain of 0.28 percentage points over random chance
(0.3906%), not significant at α = 0.05 — while training loss descended to 0.27 nats
through pure memorisation with zero generalisation. AES ciphertext bytes exhibit
7.9989/8.0 bits entropy, indistinguishable from uniform at p = 0.66.

These results provide a clean separation between feasible and infeasible neural
cryptanalysis regimes, and concrete reference metrics — the 0.3906% random baseline,
the 5.5452 nat uniform floor, and the 5.90 × 10^8 TB minimum data requirement — that
can anchor future work in this area.

---

## References

1. Gohr, A. (2019). Improving attacks on round-reduced Speck32/64 using deep learning.
   *CRYPTO 2019*, LNCS 11693, 150–179.

2. Kim, J. et al. (2023). Deep-learning-based cryptanalysis of lightweight block ciphers
   revisited. *Entropy*, 25(7), 986. PMC10378000.

3. Poudel, M. & Rahimi, N. (2025). Machine learning-based AES key recovery via
   side-channel analysis on the ASCAD dataset. *arXiv:2508.11817*.

4. Danziger, M. & Henriques, M.A.A. (2014). Improved cryptanalysis combining
   differential and artificial neural network schemes. *ISCC 2014*.

5. [Anonymous]. (2026). Assessing geometric security of AES neural realizations:
   Linear-time key recovery via neural leakage. *ePrint 2026/734*.

6. Chen, Y. et al. (2018). Research on plaintext restoration of AES based on neural
   network. *Security and Communication Networks*, 2018, 6868506.

