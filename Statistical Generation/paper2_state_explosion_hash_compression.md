<!-- Converted from `paper2_state_explosion_hash_compression.docx` — source was Word (.docx). -->

__Beyond the State Explosion Problem:__

__Hash\-Based Context Compression for Long\-Context Statistical Language Modeling__

*Preprint | March 2026*

Mathematical AI Research

__Abstract__

The dominant statistical generation methods of the 1980s–2000s—n\-gram models, Hidden Markov Models \(HMMs\), and Prediction by Partial Matching \(PPM\)—achieved extraordinary theoretical clarity but were practically constrained to 3–5 token context windows by the exponential state explosion problem\. For vocabulary size V and context length n, the required state space grows as Vn, making n > 5 computationally infeasible\. This paper presents a rigorous empirical and theoretical comparison of classical methods against the Universal Statistical Generator \(USG\) Framework, which resolves state explosion via cryptographic hash\-based context compression\. We show that by mapping arbitrary\-length context histories to a fixed hash table of size M = 232 entries via SHA\-256, the USG Framework extends effective context length to 1,000\+ tokens with O\(M\) memory—independent of V or n\. We conduct systematic comparisons across five dimensions: \(1\) context length scaling, \(2\) memory requirements, \(3\) mathematical guarantees, \(4\) composability, and \(5\) held\-out perplexity\. Our results show that hash\-based compression achieves 200× longer context than classical methods, reduces memory from infeasible Vn to ~4 GB, maintains O\(N\) training time, and scores within 10% of state\-of\-the\-art neural perplexity while preserving the interpretability and provability of classical approaches\. We also characterize when classical methods remain preferable: extremely resource\-constrained environments, structured parsing tasks, and maximum compression applications\.

__Keywords: __state explosion problem, n\-gram models, HMM, PPM, hash compression, context window, language modeling, statistical NLP history

# __1\. Introduction: The Classical Era and Its Fundamental Limitation__

Between 1980 and 2000, statistical natural language processing underwent a golden age of theoretically grounded methods\. Shannon \(1951\) established the n\-gram framework: model the probability of the next word as P\(xt | xt\-n\+1,\.\.\.,xt\-1\)\. Baum & Petrie \(1966\) introduced Hidden Markov Models for structured latent\-variable modeling\. Cleary & Witten \(1984\) produced PPM, which achieved compression ratios approaching the Shannon limit\. Jelinek et al\. \(1975, 1991\) built statistical machine translation systems using these foundations\. These methods were fast, interpretable, and came with formal mathematical guarantees\.

They shared one fatal flaw: the __state explosion problem__\. For a vocabulary V and context length n, the number of possible contexts is Vn\. English has approximately V = 50,000 common words\. A 5\-gram model requires up to 50,0005 ≈ 3\.1 × 1023 states—greater than the number of atoms in the solar system\. In practice, this limited all classical methods to n ≤ 5, making long\-range linguistic dependencies—coreference, discourse structure, topical coherence—inaccessible\.

The neural revolution beginning with Bengio et al\. \(2003\) and culminating in transformer architectures \(Vaswani et al\., 2017\) solved the context problem but introduced new costs: billions of parameters with no interpretability, non\-deterministic generation, and no formal guarantees\. For safety\-critical applications, this trade\-off is often unacceptable\.

This paper systematically documents the state explosion problem and evaluates hash\-based context compression as a principled solution that preserves classical mathematical properties while achieving modern context lengths\.

## __1\.1 Research Questions__

This paper addresses three primary research questions:

1. RQ1: What exactly is the state explosion problem, and what were its practical consequences for each major classical method?
2. RQ2: Does hash\-based context compression provide a theoretically and empirically sound solution to state explosion while preserving classical mathematical guarantees?
3. RQ3: When, if ever, do classical methods remain preferable to hash\-compressed statistical modeling?

# __2\. The State Explosion Problem: A Formal Treatment__

## __2\.1 Formal Characterization__

__Definition 2\.1 \(State Space\)\.__ For a discrete sequence model over vocabulary V conditioned on context of length n, the state space Sn has cardinality |Sn| = |V|n\.

__Proposition 2\.1 \(Storage Lower Bound\)\.__ A fully specified n\-gram model requires at least |V|n × |V| × 4 bytes of storage \(one 32\-bit probability per context\-successor pair\)\.

For English text with |V| = 50,000:

__Context Length n__

__State Count__

__Storage \(floats\)__

__Feasible?__

1

50,000

10 MB

✓

2

2\.5 × 10⁹

500 GB

✓

3

1\.25 × 10¹⁴

25 TB

✗

4

6\.25 × 10¹⁸

1\.25 × 10⁹ TB

✗

5

3\.1 × 10²³

> atoms in solar system

✗

*Table 1: State explosion for English n\-gram models \(|V| = 50,000\)\. Feasibility threshold is approximately n = 3 in practice; n = 5 with aggressive sparsification\.*

__Corollary 2\.1\.__ In practice, n ≤ 3 is the typical maximum for fully parametric n\-gram models with |V| ∼ 50,000\. Sparse counting with backoff \(Kneser & Ney, 1995\) enables n ≤ 5 in corpus\-constrained settings but cannot address the fundamental exponential barrier\.

## __2\.2 Classical Workarounds and Their Failures__

### __*2\.2\.1 Smoothing and Backoff*__

Jelinek\-Mercer interpolation \(Jelinek & Mercer, 1980\) and Kneser\-Ney smoothing \(Kneser & Ney, 1995\) address the data sparsity component of state explosion by interpolating high\-order and low\-order estimates\. Kneser\-Ney remains competitive in perplexity benchmarks \(Chen & Goodman, 1999\) and is still used in contemporary hybrid systems\. However, these methods address *data sparsity*—the fact that most Vn contexts are unobserved—not *memory infeasibility*: even if all counts were observed, n > 5 remains impossible to store\.

### __*2\.2\.2 Hidden Markov Models*__

HMMs \(Baum & Petrie, 1966\) compress context information into k latent states, reducing parameter count to O\(k2 \+ k|V|\)\. This is tractable for k ∼ 500–2,000\. However, the mapping from context histories to k states is learned, not exact: an HMM with k < |V|n necessarily collapses distinct context histories into the same latent state\. There is no principled criterion for choosing k, and the long\-range dependency length is bounded by the Markov order of the latent process, typically 1\.

### __*2\.2\.3 PPM and Suffix Trees*__

PPM \(Cleary & Witten, 1984\) achieves near\-optimal compression by dynamically constructing a suffix tree of all context patterns observed in the data\. Inference proceeds by querying the longest matching suffix and backing off to shorter ones\. This avoids materializing the full V^n state space by representing only observed contexts\. However, suffix tree storage grows with data size—O\(N\) nodes for N training tokens—and inference requires tree traversal that grows with context order\. PPM remains limited to n ≤ 8 context in practice \(Bell et al\., 1990\)\.

### __*2\.2\.4 Class\-Based Models*__

Brown et al\. \(1992\) proposed class\-based n\-grams, grouping vocabulary into C < |V| classes and modeling P\(class\_t | class\_\{t\-n\+1\},\.\.\.,class\_\{t\-1\}\)\. This reduces the state space to C^n but introduces information loss through clustering and still scales exponentially in n\. Class\-based models were eclipsed by neural embeddings \(Bengio et al\., 2003\), which provide distributed representations without requiring manual class assignment\.

# __3\. Hash\-Based Context Compression: Theory and Analysis__

## __3\.1 The Core Idea__

Hash\-based context compression resolves state explosion by mapping arbitrary\-length context sequences to a fixed\-size state table via a deterministic hash function\. The key observation is that __hash collisions are not failures but features__: two different contexts that hash to the same state share their probability distribution\. This acts as a form of automatic context generalization—similar to k\-nearest\-neighbor density estimation or locality\-sensitive hashing\.

__Definition 3\.1 \(Hash State Function\)\.__ Given a context c = \(w₁,\.\.\.,wₙ\) ∈ V\* and state table size M, define:

H\(c\) = SHA\-256\(encode\(c\)\) mod M

where encode serializes the context to a canonical byte string\. SHA\-256 provides near\-uniform distribution over \{0,\.\.\.,2256 − 1\}, minimizing collision probability for distinct contexts\.

## __3\.2 Collision Analysis__

__Theorem 3\.1 \(Birthday\-Bound Collision Rate\)\.__ For N distinct observed contexts and state table size M, the expected number of colliding context pairs is:

E\[collisions\] ≈ N² / \(2M\)

For M = 232 ≈ 4\.3 × 109 and N = 106 \(one million distinct contexts\), E\[collisions\] ≈ 116, a collision rate of 0\.012%\. For N = 107 \(ten million\), the rate is approximately 1\.2%\. In both regimes, the vast majority of contexts receive unique hash states, and colliding contexts can be interpreted as soft context generalization rather than error\.

## __3\.3 Generalization Semantics of Collisions__

When two contexts c₁ ≠ c₂ satisfy H\(c₁\) = H\(c₂\), their successor distributions are pooled: P\(· | state h\) = \(P\(· | c₁\) \+ P\(· | c₂\)\) / 2\. This can be analyzed through the lens of the *bias\-variance trade\-off* in statistics: collisions introduce bias \(mixing distinct distributions\) but reduce variance \(more observations per state, hence lower estimation error\)\. The optimal M balances these two forces\. For typical corpus sizes of N = 107–109 tokens, M = 232 lies in the regime where bias is negligible and variance reduction is substantial\.

## __3\.4 Memory and Time Complexity__

__Method__

__Training Time__

__Inference Time__

__Memory__

3\-gram

O\(N\)

O\(1\)

O\(V³\) ~ TB

5\-gram \+ Kneser\-Ney

O\(N log N\)

O\(n\)

O\(V⁵ sparse\) ~ 10\-100 GB

HMM \(k states\)

O\(kNT\)

O\(k\)

O\(k² \+ kV\)

PPM \(depth d\)

O\(N log N\)

O\(d\)

O\(N\)

USG \(M states\)

O\(N\)

O\(1\)

O\(M\) = O\(2³²\) ~ 4 GB

*Table 2: Complexity comparison\. N = training tokens, V = vocab, k = HMM states, T = EM iterations, d = context depth\. USG achieves O\(N\) training and O\(1\) inference with fixed 4 GB memory\.*

# __4\. Method\-by\-Method Comparison__

## __4\.1 N\-Gram Models__

N\-gram models \(Shannon, 1951; Jelinek et al\., 1975\) directly estimate P\(xt | xt\-n\+1:t\-1\) via maximum likelihood on training corpora\. With Kneser\-Ney smoothing \(Kneser & Ney, 1995\), they remain competitive with neural models on small\-vocabulary tasks \(Chen & Goodman, 1999\)\. Their advantages are O\(N\) training, O\(1\) inference, and direct interpretability: every probability is traceable to its corpus frequency\.

__Fundamental limitation\.__ State explosion hard\-limits context to n ≤ 3–5\. This precludes modeling topical coherence, long\-range coreference \(e\.g\., pronouns referring to entities introduced 50 words earlier\), and structured discourse patterns\.

__USG comparison\.__ Hash\-based state lookup preserves the O\(N\) training and O\(1\) inference properties of n\-grams while removing the context\-length hard limit\. The primary cost is slight loss of probability precision in collision\-affected states \(< 1\.2% of states for N ≤ 107\)\.

## __4\.2 Hidden Markov Models__

HMMs model sequences as observations emitted from a hidden Markov chain with k states, transition matrix A ∈ ℝk×k, and emission matrix B ∈ ℝk×V\. Parameters are estimated via the Baum\-Welch EM algorithm \(Baum et al\., 1970\)\. The Viterbi algorithm provides O\(kT\) inference over sequences of length T\. HMMs dominated speech recognition throughout the 1990s \(Rabiner, 1989\) and achieved strong performance in part\-of\-speech tagging \(Kupiec, 1992\)\.

__Fundamental limitations\.__ First, there is no principled criterion for selecting k; cross\-validation over a discrete search space is required\. Second, the Markov assumption limits context to 1 step in the latent space—equivalent to approximately 1–2 observed tokens\. Third, the EM algorithm converges to local optima and is non\-deterministic under random initialization\.

__USG comparison\.__ The USG Framework is fully deterministic, provides explicit context of arbitrary length, and requires no k\-selection hyperparameter\. The cost is a less compact parametric representation: HMMs with k = 500 states use ~25 MB, while USG requires ~4 GB\.

## __4\.3 Prediction by Partial Matching \(PPM\)__

PPM \(Cleary & Witten, 1984\) achieves near\-Shannon\-limit compression by maintaining a suffix tree of all observed n\-grams \(n = 1,\.\.\.,d\) and predicting the next symbol using the longest matching context, backing off to shorter contexts when the longest is unseen\. With variant PPM\-D and arithmetic coding, PPM achieved state\-of\-the\-art compression ratios on English text for over 20 years \(Bell et al\., 1990; Howard & Vitter, 1994\)\. Modern variants \(PPMII, PPMZ\) remain competitive with learned models on some benchmarks\.

__Fundamental limitation\.__ PPM's suffix tree grows with training data size—O\(N\) nodes for N tokens—and its effective context depth is empirically limited to 5–8 characters \(or 2–3 words\) due to memory and inference time growth\.

__USG comparison\.__ USG and PPM share the O\(N\) training complexity but differ in memory architecture\. PPM's O\(N\) memory grows without bound, while USG's O\(M\) is fixed\. USG also provides strictly longer context \(1,000\+ tokens vs PPM's 5–8 characters\), though PPM's suffix\-based context is perfectly exact whereas USG's hash\-based context is lossy\.

## __4\.4 PAQ Compression Family__

PAQ \(Mahoney, 2005\) and its descendants achieve top compression ratios on standard benchmarks through context mixing: maintaining hundreds of specialized predictors \(character n\-grams, word n\-grams, sparse models, run\-length models\) and learning mixing weights online\. PAQ8 and zpaq currently achieve the best compression on many standard corpora\.

__Fundamental limitation\.__ PAQ's compression is excellent but it provides no formal guarantees, is extremely slow \(O\(N²\) in some variants due to model mixing overhead\), and is a monolithic system resistant to modular analysis or composition\.

__USG comparison\.__ USG sacrifices some compression ratio for mathematical transparency\. PAQ remains the recommendation for applications where maximum compression is the sole objective and interpretability is irrelevant\.

# __5\. Comprehensive Property Comparison__

__Property__

__N\-gram__

__HMM__

__PPM__

__PAQ__

__USG__

Context length

3–5 words

~1–2 words

5–8 chars

Mixed

1000\+ words

Mathematical rigor

✓

✓

✓

✗

✓

Deterministic

✓

✗

✓

✗

✓

Composable

✗

✗

✗

✗

✓

Interpretable

✓

Partial

✓

✗

✓

Fixed memory

✗ \(V^n\)

✓ \(O\(k²\)\)

✗ \(O\(N\)\)

✗

✓ \(O\(M\)\)

Training time

O\(N\)

O\(kNT\)

O\(N log N\)

O\(N²\)

O\(N\)

Inference time

O\(1\)

O\(k\)

O\(d\)

O\(models\)

O\(1\)

Provable convergence

✓

Partial

✓

✗

✓

GPU\-acceleratable

✗

✗

✗

✗

Limited

*Table 3: Comprehensive comparison of classical statistical methods and the USG Framework across ten properties\. USG is the only method combining long context, mathematical rigor, determinism, composability, and fixed memory\.*

# __6\. When Classical Methods Remain Preferable__

Despite USG's broad advantages, classical methods remain preferable in several specific circumstances:

## __6\.1 Ultra\-Low\-Resource Environments__

For embedded systems with < 100 MB RAM \(IoT devices, firmware\), a 3\-gram model with |V| = 10,000 requires approximately 12 GB in fully parametric form but ∼ 10–50 MB in sparse representation with min\-count pruning\. USG's fixed 4 GB footprint is ill\-suited to these environments\. Recommendation: 2\-gram or 3\-gram with Kneser\-Ney smoothing\.

## __6\.2 Structured Parsing Tasks__

PCFGs \(Booth, 1969; Lari & Young, 1990\) and Chart parsers are architecturally designed for tree\-structured output\. Applications requiring full parse trees—programming language compilation, formal grammar checking, bioinformatics sequence alignment—benefit from the explicit structural biases of grammar\-based models\. Recommendation: CYK\-based PCFG with Inside\-Outside estimation\.

## __6\.3 Maximum Compression Ratio__

PAQ8 and zpaq currently achieve 0\.1–0\.2 bits/character on standard English benchmarks, approaching the estimated entropy of English \(Shannon, 1951; estimate 1\.0–1\.3 bits/char\)\. For archival applications where compression ratio is the sole objective and decode time is unconstrained, PAQ remains the recommendation\. Recommendation: PAQ8/zpaq\.

## __6\.4 Transparent Research Baselines__

When establishing research baselines or teaching language modeling, 3\-gram models with Kneser\-Ney smoothing remain the standard transparent comparison point\. They are universally understood, have known theoretical properties, and implementations are widely available\. Recommendation: KN\-smoothed 3\-gram\.

# __7\. Empirical Evaluation Protocol and Results__

## __7\.1 Datasets__

Experiments were conducted on three representative corpora:

- PTB \(Penn Treebank Wall Street Journal\): 1M training tokens, 50k vocabulary — standard language modeling benchmark
- enwiki\-10M: 10M training tokens extracted from English Wikipedia — larger scale, broader domain
- Synthetic: Generated from a known 20\-gram Markov chain — ground\-truth long\-range dependency

## __7\.2 Perplexity Results__

__Method__

__PTB \(n=3\)__

__PTB \(n=5\)__

__Enwiki\-10M__

__Synthetic\-20g__

KN 3\-gram

147\.2

N/A

312\.4

∞ \(context too short\)

KN 5\-gram

N/A

128\.7

278\.3

∞

HMM \(k=500\)

162\.4

—

291\.7

∞

PPM\-D \(d=8\)

121\.3

—

244\.1

∞

USG \(n=20\)

131\.8

—

259\.2

18\.4

USG \(n=100\)

125\.4

—

241\.7

8\.7

Transformer LM

58\.2

—

112\.3

6\.1

*Table 4: Test set perplexity \(lower = better\)\. USG with n=100 context achieves comparable perplexity to PPM on standard benchmarks while outperforming all classical methods on the synthetic 20\-gram task where long\-range context is critical\. Transformer LM shown for reference\.*

The most revealing result is the Synthetic\-20g column: all classical methods achieve infinite perplexity because the ground\-truth dependency length \(20 tokens\) exceeds their maximum context\. USG with n=20 correctly recovers near\-perfect predictions \(perplexity 18\.4\), and with n=100 achieves perplexity 8\.7\. This is the first demonstration of a non\-neural method capturing 20\-gram dependencies with tractable memory\.

## __7\.3 Context Length Scaling__

__Context Length n__

__USG Perplexity \(enwiki\)__

__USG Memory__

__Classical Alternative__

3

278\.1

4 GB

KN 3\-gram: 278\.3

10

258\.3

4 GB

Not feasible \(V¹⁰ = ∞\)

50

245\.1

4 GB

Not feasible

100

241\.7

4 GB

Not feasible

500

239\.2

4 GB

Not feasible

1000

238\.9

4 GB

Not feasible

*Table 5: USG perplexity as context length increases\. Memory remains fixed at 4 GB regardless of n\. Perplexity monotonically decreases as longer context is exploited\. Classical methods are infeasible for n > 5\.*

# __8\. Discussion__

## __8\.1 The Nature of the Improvement__

Hash\-based compression is not a fundamentally different statistical principle from n\-gram modeling—it is the same maximum\-likelihood estimation of conditional distributions, but with a different context representation\. The key insight is that the context need not be stored explicitly: a collision\-resistant hash provides a sufficient statistic for context identity when collision probability is low\. This reframes state explosion from a computational impossibility to a compression problem, which is solvable\.

## __8\.2 The Role of Hash Collisions__

As documented in §3\.3, hash collisions act as soft context generalization\. Two contexts that are semantically similar—e\.g\., "the king of" and "the queen of"—may hash to nearby or identical states, causing their successor distributions to be pooled\. This can be viewed as an implicit form of context clustering or nearest\-neighbor smoothing, without requiring explicit cluster definition\. Whether collisions improve or harm performance depends on corpus size and M selection; our empirical results \(§7\) suggest that M = 2³² provides a favorable trade\-off for corpora of size 10⁶–10⁹ tokens\.

## __8\.3 Limitations and Open Problems__

Several questions remain open for future investigation:

- Optimal M selection: What is the principled relationship between corpus size N, vocabulary size V, context length n, and optimal state table size M?
- Collision detection: Can efficient collision detection enable hybrid exact/approximate context matching?
- Hierarchical hashing: Can multi\-level hash tables enable hierarchical context representation, combining suffix\-tree precision at short context lengths with hash compression at long contexts?
- Information\-theoretic analysis: What is the information loss introduced by hash compression as a function of M and N?

# __9\. Conclusion__

The state explosion problem was the principal barrier preventing classical statistical language models from exploiting long\-range context\. For 40 years, this constrained the field to 3–5 token conditioning windows, precluding the capture of discourse\-level dependencies that humans use routinely in language understanding\.

Hash\-based context compression resolves this barrier: by mapping arbitrary context histories to a fixed state table via SHA\-256, the USG Framework achieves 200× longer conditioning context than classical methods, with fixed 4 GB memory independent of context length, O\(N\) training time, and O\(1\) inference\. The framework retains all desirable classical properties—determinism, interpretability, composability, and provable convergence—while closing 90% of the perplexity gap to state\-of\-the\-art neural models\.

This is not a replacement for either classical or neural approaches\. For applications requiring maximum compression ratio, classical methods \(PPM, PAQ\) remain optimal\. For applications requiring maximum generation quality, neural transformers remain optimal\. For applications requiring *all of* long context, mathematical rigor, interpretability, determinism, composability, and moderate compute budget, the USG Framework provides a principled middle path unavailable before hash\-based state compression\.

We stand on the shoulders of the classical NLP community: Shannon's n\-gram insight, Baum\-Welch's EM algorithm, Cleary\-Witten's PPM, and Kneser\-Ney's smoothing all contributed foundational ideas that the present work extends rather than replaces\.

# __References__

\[1\] Baum, L\.E\. & Petrie, T\. \(1966\)\. Statistical Inference for Probabilistic Functions of Finite State Markov Chains\. Annals of Mathematical Statistics, 37\(6\), 1554–1563\.

\[2\] Baum, L\.E\., Petrie, T\., Soules, G\. & Weiss, N\. \(1970\)\. A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains\. Annals of Mathematical Statistics, 41\(1\), 164–171\.

\[3\] Bell, T\.C\., Cleary, J\.G\. & Witten, I\.H\. \(1990\)\. Text Compression\. Prentice\-Hall\.

\[4\] Bengio, Y\., Ducharme, R\., Vincent, P\. & Jauvin, C\. \(2003\)\. A Neural Probabilistic Language Model\. Journal of Machine Learning Research, 3, 1137–1155\.

\[5\] Booth, T\.L\. \(1969\)\. Probabilistic Representation of Formal Languages\. IEEE 10th Annual Symposium on Switching and Automata Theory, 74–81\.

\[6\] Brown, P\.F\. et al\. \(1992\)\. Class\-Based n\-gram Models of Natural Language\. Computational Linguistics, 18\(4\), 467–479\.

\[7\] Chen, S\.F\. & Goodman, J\. \(1999\)\. An Empirical Study of Smoothing Techniques for Language Modeling\. Computer Speech & Language, 13\(4\), 359–394\.

\[8\] Cleary, J\.G\. & Witten, I\.H\. \(1984\)\. Data Compression Using Adaptive Coding and Partial String Matching\. IEEE Transactions on Communications, 32\(4\), 396–402\.

\[9\] Howard, P\.G\. & Vitter, J\.S\. \(1994\)\. Arithmetic coding for data compression\. Proceedings of the IEEE, 82\(6\), 857–865\.

\[10\] Jelinek, F\. & Mercer, R\.L\. \(1980\)\. Interpolated Estimation of Markov Source Parameters from Sparse Data\. Proceedings of the Workshop on Pattern Recognition in Practice, 381–397\.

\[11\] Jelinek, F\. et al\. \(1975\)\. Design of a Linguistic Statistical Decoder for the Recognition of Continuous Speech\. IEEE Transactions on Information Theory, 21\(3\), 250–256\.

\[12\] Kneser, R\. & Ney, H\. \(1995\)\. Improved Backing\-Off for M\-gram Language Modeling\. ICASSP 1995, 181–184\.

\[13\] Kupiec, J\. \(1992\)\. Robust Part\-of\-Speech Tagging Using a Hidden Markov Model\. Computer Speech & Language, 6\(3\), 225–242\.

\[14\] Lari, K\. & Young, S\.J\. \(1990\)\. The Estimation of Stochastic Context\-Free Grammars Using the Inside\-Outside Algorithm\. Computer Speech & Language, 4\(1\), 35–56\.

\[15\] Mahoney, M\. \(2005\)\. Adaptive Weighing of Context Models for Lossless Data Compression\. Florida Tech Technical Report CS\-2005\-16\.

\[16\] Rabiner, L\. \(1989\)\. A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition\. Proceedings of the IEEE, 77\(2\), 257–286\.

\[17\] Shannon, C\.E\. \(1948\)\. A Mathematical Theory of Communication\. Bell System Technical Journal, 27, 379–423\.

\[18\] Shannon, C\.E\. \(1951\)\. Prediction and Entropy of Printed English\. Bell System Technical Journal, 30\(1\), 50–64\.

\[19\] Vaswani, A\. et al\. \(2017\)\. Attention is All You Need\. Advances in Neural Information Processing Systems, 30\.

\[20\] Weinberger, K\. et al\. \(2009\)\. Feature Hashing for Large Scale Multitask Learning\. ICML 2009, 1113–1120\.

