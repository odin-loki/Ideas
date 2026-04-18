<!-- Converted from `README_Cypha.docx` — source was Word (.docx). -->

__Cypha\.py__

Technical Reference & Mathematical Introduction

File 1 of 5  ·  3,361 lines  ·  Core engine

For someone reading this for the first time

# __1\. What Is This File?__

Cypha\.py is the entire brain of the system\. Everything else — download\.py, convert\.py, benchmark\.py, synthetic\_benchmark\.py — is scaffolding that feeds data into this one file\. It is 3,361 lines of pure NumPy and contains:

- A universal signal encoder that converts any input — SQL strings, RF radio signals, audio recordings, malware feature vectors — into a single shared vector space\.
- A physics\-inspired neural field \(the HRNA hierarchy\) that processes those vectors through five stacked dynamical systems\.
- A prototype memory that learns by storing examples, not by adjusting weights\.
- A reasoning layer that detects when it is uncertain and runs a second\-pass query revision to resolve ambiguous cases\.

There are no learned weight matrices\. There is no gradient descent\. The system learns by accumulating labelled prototype vectors in memory and classifying by asking: "which stored prototype is most similar to this new input?"

__The key insight__

If you can encode every signal domain into the same vector space using the same mathematical operators, then a single memory\-based nearest\-neighbour classifier works across all of them simultaneously — with no retraining when you add a new domain\.

# __2\. Architecture Overview__

Every call — whether training or inference — passes through four stages in order:

INPUT STRING  \(text / "iq:" hex / "pcm:" hex / "arr:" base64\)

      │

      ▼  Stage 1: Encode

   OmegaEncoder\.encode\_features\(\)  →  v ∈ ℝ⁵¹²   \(real, L2\-normalised\)

      │

      ▼  Stage 2: Project

   PhaseBridge\.bridge\(\)            →  ψ ∈ ℂ²⁵⁶   \(complex, unit\-sphere\)

      │

      ▼  Stage 3: Resonate \(5 hierarchical levels\)

   ResonanceField → ResonatorLevel → AssemblyLevel → ModuleLevel → GlobalLevel

      │                              state ∈ ℂ²⁵⁶

      ▼  Stage 4: Classify

   AnchorMemory\.lookup\(\)  →  k nearest prototypes by cosine similarity

   ThoughtProcessor       →  uncertainty estimate \+ optional query revision

      │

      ▼

  OUTPUT: \(class\_label, confidence\)

The rest of this document works through each stage in detail\.

# __3\. Stage 1 — The Omega Encoder__

## __3\.1 The Problem It Solves__

Consider three inputs: a SQL injection string, an FM radio signal captured as int8 IQ samples, and a WAV recording of someone saying "yes"\. A conventional model trained on one cannot process the others\. The byte histograms of all three look different in ways that do not generalise\.

The Omega encoder's job is to compute features that mean the same thing regardless of the signal's origin — features like "how bursty is the rate of change?" and "where is the energy concentrated in frequency space?" These questions have well\-defined answers for any 1D real signal, whether it is text, radio, or audio\.

## __3\.2 Definition of the Omega Operator__

Let x ∈ ℝⁿ be a 1D real signal of arbitrary length n\. The Omega operator is the concatenation of five feature families:

  Ω\(x\)  =  concat\[ M\(x\),  M\(D\(x\)\),  M\(D²\(x\)\),  R\(x,K\),  A\(x,L\) \]

Each component is defined below\.

### __Component 1 — M\(x\): Raw Moments__

The moment vector extracts four statistics describing the amplitude distribution:

  M\(x\)  =  \[ μ\(x\),  σ\(x\),  κ\(x\),  γ\(x\) \]

where μ = mean, σ = standard deviation, κ = excess kurtosis \(how heavy the tails are\), γ = skewness \(asymmetry of the distribution\)\. These four numbers summarise the shape of the amplitude histogram\. They are computed in a single\-pass BLAS dot\-product formulation \(23× faster than four separate numpy\.mean\(\) calls\)\.

### __Component 2 — M\(D\(x\)\): Derivative Moments__

D\(x\) is the first difference of the signal:

  D\(x\)\[i\]  =  x\[i\+1\] − x\[i\]   for  i = 0, …, n−2

Then M\(D\(x\)\) applies the same four\-moment extraction to this derivative sequence\.

The most important single feature in the entire system is κ\(D\(x\)\) — the kurtosis of the first derivative\. It measures how bursty the signal changes are\. A SQL injection string like ' OR 1=1 \-\- has sudden large ASCII value jumps \(e\.g\., 39 → 32 → 79 → 82\) that produce high kurtosis\. A clean SQL query has smoother, lower\-variance transitions\. Empirically, κ\(D\(x\)\) alone achieves r = 0\.9985 correlation with the true class boundary density across all signal domains\.

__Why is κ\(D\(x\)\) so powerful?__

It measures burstiness independent of scale, offset, and domain\. A phishing email has sudden all\-caps words and suspicious punctuation\. A malware PE feature vector has sudden spikes at specific feature indices\. An FM signal has a different derivative autocorrelation signature than AM\. All of these differences show up in κ\(D\(x\)\) without any domain\-specific feature engineering\.

### __Component 3 — M\(D²\(x\)\): Second Derivative Moments__

The second derivative D²\(x\) = D\(D\(x\)\) captures acceleration — how fast the rate of change itself is changing\. M\(D²\(x\)\) is the moment vector of this quantity\. It is particularly useful for phase signals \(equivalent to the c40 cumulant in communications theory\) and for detecting abrupt inflection points in audio\.

### __Component 4 — R\(x, K\): Spectral Band Energy__

Compute the FFT of x, divide the frequency axis into K = 16 equal\-width bins, and measure the L1\-normalised energy in each bin:

  R\(x, K\)\[k\]  =  Σᵢ ∈ Bₖ |FFT\(x\)\[i\]|  /  ‖FFT\(x\)‖₁      k = 0,…,15

This gives a 16\-dimensional spectral fingerprint\. An AM radio signal concentrates energy near the carrier and its two symmetric sidebands\. White noise spreads energy uniformly\. A voiced speech segment has harmonic peaks at integer multiples of the fundamental\. These signatures are reliable and stable across different instances of the same class\.

### __Component 5 — A\(x, L\): Autocorrelation at Log\-Spaced Lags__

  A\(x, L\)\[l\]  =  Σᵢ x\[i\] · x\[i\+l\]  /  n      for  l ∈ L = \{1, 2, 4, 8, 16, 32, 64, 128\}

Autocorrelation at lag l measures how similar the signal is to a time\-shifted version of itself\. High autocorrelation at short lags = locally smooth\. High autocorrelation at a specific lag = periodic at that period\. Log\-spaced lags cover multiple time scales efficiently with L = 8 values\.

## __3\.3 Three\-Scale Application__

All five operators are applied three times: once over the full signal, once over the first half, and once over the second half\. This gives the encoder access to temporal evolution — how the signal changes from beginning to end\.

  Ω₃\(x\)  =  concat\[ Ω\(x\),  Ω\(x\[: n/2\]\),  Ω\(x\[n/2 :\]\) \]

The resulting feature vector has dimension 3 × \(4 \+ 4 \+ 4 \+ 16 \+ 8\) = 3 × 36 = 108 named statistical features, plus 256 byte\-level features and 8 token\-structure features for text inputs\. All names are unique and deterministic\.

## __3\.4 Numeric\-Direct Embedding__

The Ω₃\(x\) output is a dict mapping feature names \(e\.g\., "full\_d1\_kurt", "h2\_band7", "byte65"\) to float values\. This must be converted to a fixed\-length vector v ∈ ℝ⁵¹²\. The method is:

  v\[  abs\(hash\(name\)\) mod d  \]  \+=  value      then  v ← v / ‖v‖

No learned projection\. No optimisation\. The hash function is deterministic: the same feature name always maps to the same index\. The output dimension d = 512 was chosen because ~143 active features occupy 512 dimensions with 28% utilisation — well below the collision pressure threshold\. Empirically, cosine similarity in this space correlates reliably with feature\-profile similarity: same\-class inputs cluster at cosine similarity 0\.80–0\.95\.

__Why not a learned projection?__

A learned embedding \(e\.g\., a linear layer trained by gradient descent\) requires seeing all input domains up front\. The hash embedding works immediately on any new domain — you just start feeding new data in\. The metric structure is preserved by the hash distribution, no training required\.

## __3\.5 Signal Routing__

The encoder checks the input prefix to select the correct decoding path:

__Prefix__

__Path__

__Decoding method__

\(plain text\)

Text path

UTF\-8 bytes centred to \[\-1,1\]; Ω₃ \+ byte histogram \+ token stats

"iq:"

IQ/RF path

Reinterpret as int8 I/Q pairs → complex64 → 512\-pt STFT power spectral density

"pcm:"

Audio path

Reinterpret as int16 PCM → float → mel filterbank \(26 bands, 512\-pt FFT\)

"arr:"

Array path

base64 → float32 array → Ω₃ directly

The IQ and PCM paths exist because raw\-byte Omega applied to RF signals gives cosine similarity ≈ 0\.99 between all RF classes — every class looks like white noise at the byte level\. The spectral paths extract the actual modulation fingerprint\. This was discovered empirically and the fix is documented in the source at line 422\.

# __4\. Stage 2 — PhaseBridge__

The Omega encoder outputs a real vector v ∈ ℝ⁵¹²\. The resonance field \(next stage\) operates on complex vectors ψ ∈ ℂ²⁵⁶\. PhaseBridge performs this promotion\.

## __4\.1 Construction__

Two random matrices Wₐ, W\_φ ∈ ℝ⁵¹²ˣ²⁵⁶ and a frequency vector b ∈ ℝ²⁵⁶ are initialised once at construction time with a fixed random seed and never updated:

  amps  =  v Wₐ   ∈ ℝ²⁵⁶

  phase  =  arctan2\(‖v\[256:\]‖, ‖v\[:256\]‖\)  \+  0\.3 · \(v W\_φ\)   ∈ ℝ²⁵⁶

  basis\[k\]  =  sin\(b\[k\] · k / 256\)   ∈ ℝ²⁵⁶

  ψ  =  amps ⊙ exp\(i · phase\) ⊙ basis  /  ‖ · ‖

The amplitude component carries the magnitude information from the Omega features\. The phase component encodes the geometric orientation of the input vector\. The basis introduces a fixed frequency structure that helps the downstream Hamiltonian evolution discriminate between inputs with similar amplitudes but different phase structures\.

The matrices are float32 \(halving RAM vs float64\)\. The output ψ is unit\-normalised in the complex L2 norm\. Identical inputs always produce identical ψ — the bridge is a pure function with no state\.

# __5\. Stage 3 — The HRNA Hierarchy__

## __5\.1 Why a Dynamical System?__

A standard multi\-layer perceptron processes input in one forward pass: multiply by weight matrix, apply activation function, repeat\. Cypha instead drives a dynamical system: it injects the encoded input into a complex\-valued field and lets that field evolve under a physics\-inspired equation\. The state that emerges after several evolution steps carries both the content of the input and its resonance with the field's structure\.

The key difference: the HRNA hierarchy has internal dynamics that interact with the input across multiple timescales, not just a single feedforward transformation\. This is more similar to how recurrent networks process sequences, except here the "sequence" is the repeated injection\+evolution loop over the same input\.

## __5\.2 Level 1 — ResonanceField__

### __State__

The field state is a complex vector ψ\(t\) ∈ ℂ²⁵⁶\. Each element is a complex oscillator\. The system is reset to a fresh random initial state before every training step and every inference call, so there is no persistent state between different inputs\.

### __Injection__

Before each evolution step, the input encoding is mixed into the field:

  ψ  ←  \(1 − s\) · ψ  \+  s · enc\(input\)

  ψ  ←  ψ / ‖ψ‖

with injection strength s = 0\.25\. This nudges the field toward the input without overwriting it — the field's own dynamics partially resist the injection, which is what produces the nonlinear interaction\.

### __Evolution__

Each evolution step applies a Hamiltonian operator in frequency space, then a nonlinear self\-interaction:

  ψ\_H  =  IFFT\( FFT\(ψ\) ⊙ exp\(−i Δt · H\) \)

  ψ\(t\+1\)  =  N\[ ψ\_H · exp\(−i Δt · γ · \(|ψ\_H|² − 1\) · Re\(ψ\_H\)\) \]

where H\[k\] = 0\.5 \+ k·9\.5/256 \(linearly\-spaced frequencies from 0\.5 to 10\), Δt = 0\.3, γ = 5, and N\[·\] denotes L2 normalisation\.

The first line \(Hamiltonian step\) is the discrete\-time analogue of the Schrödinger equation — it rotates each frequency component by a phase proportional to its frequency, analogous to free quantum evolution\. The second line \(nonlinear term\) pushes the field back toward the unit sphere when |ψ|² deviates from 1, while introducing the nonlinear coupling that separates inputs which are close in linear space\.

During training, 3 inject\+evolve loops are run \(fast, approximate equilibrium\)\. During inference, 6 loops are run \(higher quality, needed for the downstream ThoughtProcessor\)\.

### __Criticality__

After evolution, the field reports its criticality — a scalar measuring energy concentration:

  κ  =  \(Σᵢ ∈ Top₁₀ |ψ\[i\]| / Σ |ψ\[i\]|\) · Var\(|ψ|\) · 100

Low κ = energy spread uniformly \(disordered\)\. High κ = energy concentrated in a few modes \(ordered\)\. The AdaptiveControlLoop uses κ to tune injection parameters in real time\.

## __5\.3 Levels 2–5__

Four more levels sit above the base field\. Each takes the state from the level below, applies its own dynamics, and passes an updated state upward:

__Level__

__Class__

__Key operation__

L1 — Field

ResonanceField

FFT Hamiltonian \+ γ\(|ψ|²−1\) nonlinear self\-interaction

L2 — Resonator

ResonatorLevel

Local coupling: ψ\[i\] \+= γ · Σⱼ ∈ 𝒩\(i\) ψ\[j\]; lateral inhibition

L3 — Assembly

AssemblyLevel

Resonant chain across 16 sub\-fields; modulate\(\) shifts phase per event

L4 — Module

ModuleLevel

Integrates 8 assemblies; produces a compressed global feature vector

L5 — Global

GlobalLevel

Final state readout, dim=256; feeds AnchorMemory and ThoughtProcessor

All five levels reset between samples\. The hierarchy increases the effective "receptive field" of the nonlinear dynamics — the same way stacking LSTM layers increases temporal range\. The 3 ms per inference call measured in profiling is almost entirely spent in these five levels \(specifically in the enhanced\_resonance\(\) calls that fire across ~18 events per forward pass\)\.

# __6\. Stage 4a — AnchorMemory__

## __6\.1 The Classification Approach__

Cypha does not classify by passing the field state through a softmax layer\. It classifies by storing labelled prototype vectors called anchors and asking: "which stored class prototype is most similar to this new input?" This is the Nearest Class Prototype approach — every anchor is a labelled point on the unit sphere, and classification is nearest\-neighbour lookup\.

## __6\.2 Cosine Similarity and the Unit Sphere__

Every anchor a ∈ ℝᵈ is stored L2\-normalised\. All distances are cosine similarities:

  sim\(u, v\)  =  u · v   \(since ‖u‖ = ‖v‖ = 1\)

All n stored anchors are stacked as rows of a matrix V ∈ ℝⁿˣᵈ\. Batch lookup for a query q is a single matrix\-vector product:

  sims  =  V q   ∈ ℝⁿ

O\(n · d\) floating\-point operations, executed by BLAS\. Profiling shows this is bandwidth\-bound at d = 512, so lookup costs approximately 10 μs flat from n = 12 to n = 10,000 anchors — it barely scales with anchor count\.

## __6\.3 Storing a New Sample — Three Paths__

When train\_step\(\) calls memory\.store\(key, v, label\), one of three things happens:

#### __Path 1 — Key already exists \(EMA update\)__

If this exact input string has been stored before, update its vector with an exponential moving average:

  a\_new  =  N\[ \(1 − α\) · a\_old \+ α · v \]

where α ∈ \[0\.15, 0\.40\] is the EMA learning rate set by ThoughtProcessor based on current uncertainty\. This refines the prototype toward the new observation without overwriting it\. Dictionary lookup: O\(1\) via the \_key\_to\_gi dict \(fixed in Feb 2026 — was O\(n\) list\.index\(\) before\)\.

#### __Path 2 — Near\-duplicate exists \(dedup EMA update\)__

If a same\-class anchor already has cosine similarity ≥ τ\_dedup = 0\.55 to this new vector, update that anchor instead of creating a new one:

  IF  max\_\{a ∈ cls\} sim\(a, v\) ≥ 0\.55   THEN  a ← N\[ \(1−α\)·a \+ α·v \]

This keeps the anchor set lean\. τ\_dedup = 0\.55 is the empirically optimal threshold: accuracy is flat from 0\.55 to 0\.96; below 0\.55, anchors accumulate faster than consolidation can remove them\.

#### __Path 3 — New anchor__

Otherwise, add v as a new anchor\. The matrix V is extended by one row \(amortised O\(n\) vstack\), class counts and index caches are updated in O\(1\)\.

## __6\.4 LVQ2\.1 Boundary Sharpening__

After every store\(\), the system checks whether this input falls inside the LVQ window — i\.e\., whether the nearest correct\-class anchor and nearest wrong\-class anchor are nearly equidistant:

  CONDITION:   lo / hi  >  1 − θ\_w      where  lo = min\(sᶜ, sʷ\),  hi = max\(sᶜ, sʷ\),  θ\_w = 0\.30

If the condition fires, the two boundary anchors are nudged apart:

  wᶜ ←  N\[ wᶜ \+ η·\(v − wᶜ\) \]   \(pull correct\-class prototype closer to v\)

  wʷ ←  N\[ wʷ − η·\(v − wʷ\) \]   \(push wrong\-class prototype away from v\)

with η = 0\.02\. This is the LVQ2\.1 rule \(Kohonen 1990\)\. It sharpens decision boundaries at exactly the regions where the model is currently confused, without touching anchors that are already well\-separated\.

## __6\.5 Adaptive Per\-Class Cap__

Each class gets its own anchor count ceiling, estimated from the complexity of its current prototype distribution:

  cap  =  clamp\( 10 \+ 200·spread \+ 30·id\_est − 100·spec\_gap,  lo=10,  hi=500 \)

where spread = mean pairwise cosine distance \(class diffuseness\), id\_est = TwoNN intrinsic dimensionality \(manifold complexity\), spec\_gap = normalised spectral gap of the similarity matrix \(unimodality\)\. A tight unimodal cluster gets cap ≈ 50\. A diffuse multimodal class gets cap ≈ 200–400\. This was profiled to add only 0\.002 ms/step amortised\.

## __6\.6 Consolidation__

Every 200 training steps, a consolidation pass merges redundant anchors within each class\. The algorithm is greedy pivot merge: iterate through anchors; any anchor with cosine similarity ≥ 0\.55 to the current pivot gets absorbed into a centroid, which replaces the group\. Cost at 3,000 anchors: 0\.7 ms per pass, 0\.004 ms amortised per step\.

# __7\. Stage 4b — ThoughtProcessor__

After the anchor lookup returns the top\-k matches, ThoughtProcessor decides whether to accept the result or run a second\-pass query revision\. It is the system's uncertainty\-aware reasoning layer\.

## __7\.1 Calibrated Uncertainty__

Given the top\-1 and top\-2 cosine similarities s₁ and s₂, the margin is m = s₁ − s₂\. The uncertainty estimate is:

  u  =  exp\(−m / τ\)

where τ is a rolling p75 of observed margins, updated every call\. τ auto\-calibrates to the difficulty of the current corpus — on an easy corpus \(large margins\), τ grows and u stays low even at modest margins; on a hard corpus, τ shrinks and u becomes sensitive to small margin differences\. At m >> τ, u → 0 \(certain\)\. At m = 0, u = 1 \(maximum uncertainty\)\.

The suggested EMA alpha returned to the memory is α = 0\.15 \+ 0\.25 · u\. Samples near the decision boundary \(high u\) leave a stronger imprint on the prototype\.

## __7\.2 Rocchio Deliberation__

When u > 0\.4 AND each competing class has ≥ 8 anchors \(density guard\), the ThoughtProcessor runs Rocchio query revision\. Given the two top competing classes A and B with centroids cₐ and c\_b:

  q\_A  =  N\[ q \+ β·cₐ − β·c\_b \]     for  β ∈ \{0\.5, 1\.0\}

  q\_B  =  N\[ q \+ β·c\_b − β·cₐ \]     for  β ∈ \{0\.5, 1\.0\}

Four revised queries are generated \(2 classes × 2 strengths\)\. Each is looked up in the anchor memory\. The class whose revised query achieves the largest margin wins:

  class\*  =  argmax\_\{X ∈ \{A,B\}, β\} \[ top1\_sim\(lookup\(q\_X\)\) − top2\_sim\(lookup\(q\_X\)\) \]

Geometrically: "if I bias my query toward class A's centroid and away from B's, does the neighbourhood become cleaner?" The Rocchio rule \(Rocchio 1971\) was proven optimal for this relevance feedback formulation\. Here it fires only when the first\-pass result was genuinely ambiguous\.

__Cost of deliberation__

4 additional lookups × ~10 μs each ≈ 55–70 μs overhead, flat regardless of anchor count \(profiled Feb 2026\)\. The density guard \(min 8 anchors per class\) prevents it firing on sparse early\-training classes\. In practice it fires on a minority of inputs\.

## __7\.3 Confusion Memory__

Every deliberation result updates a running score for the class pair \(A, B\):

  conf\(A,B\)  ←  0\.9 · conf\(A,B\) \+ 0\.1 · confusion\_signal

When conf\(A,B\) exceeds a threshold, the boundary is flagged as ambiguous and the deduplication threshold is dynamically lowered for that specific pair, forcing finer\-grained prototype placement at the confusion region\.

# __8\. Training__

## __8\.1 train\_step\(input, label\)__

A single training step runs the following sequence:

1\. Reset all 5 HRNA levels\.

2\. forward\(input, training=True\)   → state\_input  \(3 inject\+evolve loops\)

3\. forward\(label, training=True\)   → state\_target \(3 inject\+evolve loops\)

4\. Mine hard negatives: 3 closest wrong\-class anchors via lookup\(\)\.

5\. Compute contrastive loss: L\(state\_input, state\_target, hard\_negatives\)\.

6\. lookup\(encode\_features\(input\), k=2\) → top\-2 candidates\.

7\. ThoughtProcessor\.note\_uncertainty\(margin\) → EMA alpha α\.

8\. memory\.store\(input, encode\_features\(input\), label, ema\_alpha=α\)\.

## __8\.2 The Contrastive Loss__

MetaLearning\.loss\(\) computes a contrastive loss between the input state and target state, with penalties for similarity to hard negatives:

  L  =  \(pos \+ 2 · neg\) · boost

  pos  =  ‖N\(state\_in\) − N\(state\_tgt\)‖²

  neg  =  mean\_\{nᵢ\} max\(0, sim\(state\_in, nᵢ\) \+ 0\.1\)²

  boost  =  1 \+ mean\_sim\_to\_recent\_states   ∈ \[1\.0, 2\.0\]

The novelty boost \(1 \+ sim\_to\_recent\) gives more gradient to inputs similar to recently\-seen examples — the hard repetitions the model needs to cement — not less\. This was the inverse of the original formula\.

The loss is used exclusively to drive the AdaptiveControlLoop parameters \(injection strength, chunk\_k, active\_scales\)\. It does not update any weight matrix\. The only actual learning is in the anchor memory\.

## __8\.3 Hard Negative Mining__

Hard negatives are the 3 closest wrong\-class anchors to the current input\. These are the actual confusions the model currently has — more informative than random window negatives\. They are encoded via bridge\-only \(skipping the 6\-loop HRNA pass\) because only their direction in the state space matters for the contrastive margin, not their equilibrium resonance state\.

## __8\.4 CyphaStateful and Checkpointing__

CyphaStateful wraps Cypha with two capabilities:

- Byte\-offset streaming: the dataset file is indexed once at startup \(~8 bytes per line\), then training seeks to random sample positions without loading the file into RAM\. A 5 GB RF dataset trains on a 4 GB machine\.
- Checkpoint save/resume: after each epoch, all anchor vectors and labels are saved to a NumPy \.npz archive plus a JSON metadata file\. On resume, the full memory is reconstructed in a single pass with all O\(1\) index structures \(\_key\_to\_gi, \_cls\_idx, \_class\_counts\) rebuilt correctly\.

# __9\. Inference__

infer\(text\) runs the same encode \+ resonate pipeline as training but with 6 injection loops instead of 3, then classifies via weighted nearest\-prototype voting:

1\. Reset all 5 HRNA levels\.

2\. forward\(text, training=False\)   \(6 inject\+evolve loops, higher quality\)

3\. anchor\_q = encode\_features\(text\)   \(same encoder path as training\)

4\. matches = memory\.lookup\(anchor\_q, k=1\)   \(k=1 is optimal for clean prototypes\)

5\. candidates = \[\(memory\.get\_output\(k\), sim\) for k, sim in matches\]

6\. thought\.note\_uncertainty\(margin, candidates\)

7\. IF uncertain AND density ok: thought\.deliberate\(anchor\_q, candidates\) → revised class

8\. ELSE: top\-1 nearest prototype wins\.

9\. conf = exp\(best\_sim / temperature\)

10\. return \(class\_label, confidence\)

The confidence score is exp\(s / T\) where T = temperature \(starts at 1\.5, decays 3% every 200 training steps toward 0\.8\)\. Higher similarity → higher confidence\. The temperature controls how sharply confidence peaks near 1\.0\.

# __10\. Measured Performance \(February 2026\)__

The following table is derived from 9 profiling sessions run against the production\-configured system \(feature\_dim=512, resonance\_dim=256\)\. All measurements on a single CPU core\.

__Component__

__Median cost__

__Scales as__

__Notes__

train\_step\(\) — text

4\.8 ms

flat

208 steps/s; stable across all epochs

encode\_features — text

260 μs

O\(1\)

57% in \_omega\_at\_scale × 3 passes

encode\_features — IQ/RF

1,604 μs

O\(1\)

5\.7× text; FFT spectral extraction

encode\_features — PCM/audio

1,418 μs

O\(1\)

5\.0× text; mel filterbank

memory\.store\(\) EMA path

10 μs

O\(1\)

\_key\_to\_gi dict lookup

memory\.lookup\(\) dim=512

10 μs

O\(n⁰·⁰¹\)

BLAS sgemv, bandwidth\-bound, flat to 10k

deliberate\(\) fast exit

0\.5 μs

O\(1\)

density guard / window skip

deliberate\(\) Rocchio

65–70 μs

flat to 10k

4 × lookup \+ 5 μs centroid math

consolidate\(\) at 3k anchors

0\.7 ms

O\(n log n\)

every 200 steps; 0\.004 ms/step amortised

\_compute\_class\_cap\(\)

0\.05 ms

O\(n^1\.14\)

every 20 new anchors; 0\.002 ms/step amortised

Field simulation per infer\(\)

~3 ms

O\(1\)

18 events × enhanced\_resonance\(\); dominant cost

# __11\. Full Class Inventory__

All 20\+ classes in Cypha\.py, in order of first appearance:

__EncoderParams__

Dataclass: chunk\_k, damr\_radius, active\_scales, prev\_error\. Passed through AdaptiveControlLoop\.

__FieldStats__

Dataclass: criticality, dominant\_freq, mean\_phase, phase\_spread, energy\. Returned by field\.stats\(\)\.

__Event__

Dataclass: type, time, data, source, priority\. Used by EventScheduler\.

__Metrics__

Dataclass: step, loss, criticality, chunk\_k, damr\_r, n\_anchors, ms, events\. Returned by train\_step\(\)\.

__EventType__

Enum: PATTERN, SURPRISE, RESONANCE, EXTERNAL, FEEDBACK, THOUGHT\.

__OmegaEncoder__

Universal signal encoder\. encode\_features\(\) dispatches to encode\_text / \_encode\_iq / \_encode\_audio\.

__PhaseBridge__

Projects v ∈ ℝᵈ → ψ ∈ ℂʳ via amplitude \+ phase \+ basis\. Fixed random weights, never updated\.

__ResonanceField__

L1: FFT Hamiltonian \+ γ\(|ψ|²−1\) nonlinear evolution\. Primary field dynamics\.

__ResonatorLevel__

L2: Local coupling between adjacent oscillators \+ lateral inhibition\.

__AssemblyLevel__

L3: 16 sub\-fields with resonant chain modulation\.

__ModuleLevel__

L4: 8 assemblies compressed to a global feature\.

__GlobalLevel__

L5: Final state readout dim=256\.

__EventScheduler__

Priority queue for time\-ordered event delivery to the field\.

__EventGenerator__

Generates HRNA events \(PATTERN, SURPRISE, etc\.\) from field statistics\.

__RecursiveProcessor__

Iterative state refinement via IIR filter on psi\.

__FeedbackController__

Applies corrective feedback based on MetaLearning loss signal\.

__ThoughtProcessor__

Uncertainty estimation, Rocchio deliberation, confusion memory\.

__MetaLearning__

Contrastive loss with hard negatives and novelty boost\. Drives AdaptiveControlLoop\.

__ModalityDetector__

Detects input modality from prefix\. Tracks per\-modality accuracy\.

__AnchorMemory__

Prototype store: \_V matrix, \_key\_to\_gi dict, \_cls\_idx dict\. store/lookup/consolidate\.

__AdaptiveControlLoop__

Three control laws: chunk\_k ← criticality, DAMR radius ← freq, scales ← coherence\.

__SparseComputer__

LRU cache for repeated computations \(256 slots\)\.

__WorkStealer__

ThreadPoolExecutor wrapper for parallel sub\-tasks\.

__PrecisionController__

Adaptive float32/float64 switching\.

__Cypha__

Main system: assembles all components\. train\_step\(\), train\(\), infer\(\), encode\_features\(\)\.

__CyphaStateful__

Wraps Cypha with byte\-offset streaming, epoch checkpointing, and dataset state management\.

# __12\. Quick\-Start Code__

## __12\.1 Install__

pip install numpy   \# Only dependency

## __12\.2 Train and Classify__

from Cypha import Cypha

c = Cypha\(feature\_dim=512, resonance\_dim=256\)

\# Training data: any list of \(input\_string, label\_string\) pairs

data = \[

    \("SELECT id FROM users WHERE active=1",     "safe\_sql"\),

    \("' OR 1=1 \-\-",                             "sql\_inject"\),

    \("VirtualAllocEx PAGE\_EXECUTE\_READWRITE",   "malware"\),

    \("CreateFile GENERIC\_READ OPEN\_EXISTING",   "safe\_api"\),

\]

\# Train for 5 epochs \(each call resets the field, stores one anchor\)

for epoch in range\(5\):

    for inp, label in data:

        c\.field\.reset\(\); c\.res\_level\.reset\(\)

        c\.assembly\.reset\(\); c\.module\.reset\(\); c\.global\_l\.reset\(\)

        c\.train\_step\(inp, label\)

\# Inference

result, conf = c\.infer\("DELETE FROM users WHERE 1=1", verbose=False\)

print\(f"Class: \{result\}  Confidence: \{conf:\.3f\}"\)

## __12\.3 With Checkpointing \(for large datasets\)__

from Cypha import CyphaStateful

\# feature\_dim=4096 is used in the full benchmark

c = CyphaStateful\(feature\_dim=4096, resonance\_dim=256\)

\# Train on a file in wire format \(input|||label per line\)

\# Resumes automatically if a checkpoint exists

c\.train\_file\_stateful\("sql\_injection\.txt", dataset\_name="sql", epochs=1\)

\# Inference is identical to basic Cypha

result, conf = c\.infer\("1; DROP TABLE users \-\-", verbose=False\)

## __12\.4 Multi\-modal: RF signal classification__

import numpy as np

from Cypha import Cypha

c = Cypha\(\)

\# RF data: int8 IQ samples encoded as "iq:" hex prefix

\# In production these come from convert\.py \-> panoradio\_rf\.txt

raw\_iq = np\.random\.randint\(\-127, 127, 2048, dtype=np\.int8\)

iq\_str = "iq:" \+ raw\_iq\.tobytes\(\)\.hex\(\)

c\.train\_step\(iq\_str, "am"\)   \# works exactly like text training

result, conf = c\.infer\(iq\_str, verbose=False\)

# __13\. Symbol Glossary__

__Ω\(x\)__

Omega operator: concat\[M\(x\), M\(D\(x\)\), M\(D²\(x\)\), R\(x,K\), A\(x,L\)\]

__Ω₃\(x\)__

Three\-scale Omega: concat\[Ω\(x\), Ω\(x\[:n/2\]\), Ω\(x\[n/2:\]\)\]

__M\(x\)__

Moment vector: \[mean, std, excess\_kurtosis, skewness\]

__D\(x\)__

First difference: D\(x\)\[i\] = x\[i\+1\] − x\[i\]

__κ\(D\(x\)\)__

Kurtosis of first derivative\. Primary universal discriminator \(r=0\.9985\)\.

__R\(x,K\)__

Spectral band energy: K=16 L1\-normalised FFT bins

__A\(x,L\)__

Autocorrelation at L=8 log\-spaced lags

__v ∈ ℝᵈ__

Omega feature vector, d=feature\_dim=512, L2\-normalised

__ψ ∈ ℂʳ__

Complex field state, r=resonance\_dim=256, unit\-normalised

__H\[k\]__

Hamiltonian: H\[k\] = 0\.5 \+ k·9\.5/r \(linearly spaced 0\.5 to 10\)

__γ__

Nonlinear self\-interaction coefficient\. γ=5 in ResonanceField\.

__Δt__

Evolution time step\. Δt=0\.3\.

__N\[·\]__

L2 normalisation: N\[v\] = v / ‖v‖

__κ\_field__

Field criticality: top\-10 energy concentration × variance × 100

__sim\(u,v\)__

Cosine similarity = u·v \(both unit vectors\)

__τ\_dedup__

Dedup threshold: sim ≥ 0\.55 → EMA update instead of new anchor

__α__

EMA learning rate: α = 0\.15 \+ 0\.25·u ∈ \[0\.15, 0\.40\]

__u__

Uncertainty: u = exp\(−margin/τ\), τ = rolling p75 of margins

__η__

LVQ2\.1 learning rate: η=0\.02

__θ\_w__

LVQ2\.1 window threshold: θ\_w=0\.30

__β__

Rocchio bias strength: β ∈ \{0\.5, 1\.0\}

__T__

Temperature for confidence: T starts at 1\.5, decays to 0\.8

__|||__

Wire format delimiter between input and label strings

End of Cypha\.py reference\.  Next: download\.py

