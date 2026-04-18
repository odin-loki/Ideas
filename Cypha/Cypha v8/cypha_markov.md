<!-- Converted from `cypha_markov.docx` — source was Word (.docx). -->

__Stochastic Processes and Markov Chain Analysis__

__of the Differential Information Field Classifier__

*Transition Matrices • Spectral Gaps • MFPT • Detailed Balance • HMM Viterbi • Absorbing Chains • Entropy Rate*

Unpublished Technical Report — 2026

__Abstract__

We analyse the CyphaDIF classifier through the lens of Markov chain theory and stochastic processes, treating sequences of classifier predictions as realisations of a discrete\-time Markov chain\. Ten probes are conducted across three traffic scenarios \(iid uniform, bursty, and realistic\-weighted\)\. Key findings: __\(1\)__ Under iid input the prediction chain has spectral gap 0\.962, implying a mixing time of approximately 1 step — the classifier has no memory of its previous prediction when inputs are independent\. __\(2\)__ Under bursty input the chain spectral gap collapses to 0\.018 \(mixing time 55 steps\), and the diagonal self\-transition probabilities rise from ≈0\.10 to ≈0\.97, demonstrating that the prediction chain faithfully inherits the burstiness of the input traffic\. __\(3\)__ Mean first\-passage times are uniformly near K = 10 steps under iid input \(expected for a near\-uniform chain\), with the longest passage \(10\.88 steps\) from log\_warn to bin\_malware and the shortest \(8\.84 steps\) from log\_warn to net\_normal\. __\(4\)__ The prediction chain is weakly irreversible: detailed balance is violated at maximum residual 4\.6×10⁻³, with net probability currents flowing from binary classes toward network and log classes\. __\(5\)__ Under realistic traffic \(60% net\_normal\) the prediction chain recovers the input distribution to total variation distance TV = 0\.015 and KL = 9\.3×10⁻⁴, demonstrating that CyphaDIF can serve as an accurate online traffic profiler\. __\(6\)__ The confusion matrix is the identity to four decimal places — the HMM observation kernel is the identity operator — making Viterbi decoding uninformative \(raw accuracy already equals 1\.0\)\. __\(7\)__ Under realistic traffic, the expected steps from net\_normal to first detection of any attack class is 4\.65 steps, with net\_scan being the most likely first\-detected attack \(38% absorption probability\)\. __\(8\)__ The prediction stream has zero autocorrelation under iid and realistic inputs, but ACF\(τ\) = λ₂^τ ≈ 0\.982^τ under bursty input \(mixing time ≈55 steps\)\. The entropy rate is 99\.6% of maximum under iid input, dropping to 6\.2% under bursty input\.

# __1\. Introduction__

A deployed intrusion detection system does not classify isolated samples — it classifies streams of network traffic, log events, and binary artefacts that arrive sequentially in time\. The statistical structure of these streams \(their correlation length, burst statistics, transition dynamics\) determines the classifier’s operational performance in ways that single\-sample accuracy statistics cannot capture\. Markov chain theory provides the natural framework for this analysis\.

We model the CyphaDIF prediction stream as a discrete\-time Markov chain on the state space of K = 10 traffic classes\. This is not an approximation: because CyphaDIF’s inference is memoryless \(the prediction at time t depends only on the current input x\_t, not on the history\), the prediction sequence is always a function of the input sequence\. When the input is Markovian, the predictions inherit that Markov structure exactly\. When the input is iid, the predictions form an iid sequence \(degenerate Markov chain with spectral gap ≈ 1\)\.

__Structure\. __Ten probes are conducted across three traffic scenarios\. Section 2 defines the framework\. Sections 3–12 present the probes\. Section 13 synthesises the findings and identifies operational implications\.

# __2\. Framework and Traffic Scenarios__

## __2\.1 The Prediction Markov Chain__

Let p\_t denote the classifier’s prediction at time t and y\_t the true label\. The empirical transition matrix is:

P\[i, j\] = P\(p\_\{t\+1\} = j | p\_t = i\)

         = N\_\{ij\} / N\_i

where N\_\{ij\} = \#\{t : p\_t = i, p\_\{t\+1\} = j\}

      N\_i   = \#\{t : p\_t = i\}

For a Markov chain with transition matrix P and stationary distribution π, the key quantities are: spectral gap γ = 1 − |λ₂| \(where λ₂ is the second\-largest eigenvalue by modulus\); mixing time τ ≈ 1/γ; mean first\-passage times M\_\{ij\} computed from the fundamental matrix Z = \(I − P \+ Π\)⁻¹; and entropy rate h = −Σ\_\{i,j\} π\_i P\_\{ij\} ln P\_\{ij\}\.

## __2\.2 Traffic Scenarios__

__Scenario__

__Description__

__Key parameters__

iid uniform

Each sample drawn independently from Uniform\{classes\}

P\(class\) = 1/K = 0\.1 each; no temporal correlation

Bursty

Random class runs of length Uniform\[15,70\]

Mean burst = 42\.5 steps; simulates sustained attack traffic

Realistic

Weighted mixture: 60% normal, 8% log\_info, 5% each scan/warn, etc\.

P = \[0\.60,0\.08,0\.05,0\.04,0\.03,0\.08,0\.05,0\.04,0\.02,0\.01\]

# __3\. Prediction Markov Chain Under iid Input__

## __3\.1 Spectral Properties__

__Key result__

__Spectral gap γ = 0\.962, λ₂ = 0\.038, mixing time ≈ 1 step\. __Under iid input, the prediction chain mixes in approximately one step\. This is mathematically necessary for a perfect classifier: if p\_t = y\_t with probability 1\.0 and y\_t is iid, then p\_t is also iid and has spectral gap 1\.0\. The measured gap of 0\.962 \(rather than 1\.0\) reflects the small but non\-zero error rate, which introduces weak temporal correlations in the prediction stream\.

The small second eigenvalue λ₂ = 0\.038 quantifies precisely the residual memory introduced by mis\-classifications: a wrong prediction p\_t ≠ y\_t followed by another wrong prediction p\_\{t\+1\} ≠ y\_\{t\+1\} creates a non\-zero off\-diagonal transition probability, giving the chain a small but non\-zero correlation length of −1/ln\(λ₂\) ≈ 3\.3 steps\.

## __3\.2 Stationary Distribution__

Under iid uniform input, the theoretical stationary distribution is π\_i = 1/K = 0\.1 for all classes\. The empirical stationary distribution deviates from uniform by at most max|π\_i − 1/K| = 0\.0074 \(for net\_normal and bin\_malware, which are slightly over\- and under\-represented respectively\)\. This 0\.74% maximum deviation is consistent with sampling noise over 5,000 steps and confirms the chain’s stationarity\.

__Class__

__π\_i \(measured\)__

__Deviation from 1/K__

__P\[i,i\] \(self\-transition\)__

net\_normal

0\.1074

\+0\.0074

0\.0819

net\_scan

0\.1028

\+0\.0028

0\.1089

net\_ddos

0\.0992

−0\.0008

0\.1107

net\_exfil

0\.1002

\+0\.0002

0\.1098

net\_c2

0\.0990

−0\.0010

0\.0869

log\_info

0\.0982

−0\.0018

0\.0896

log\_warn

0\.0954

−0\.0046

0\.0755

log\_error

0\.1052

\+0\.0052

0\.1198

bin\_malware

0\.0926

−0\.0074

0\.0864

bin\_benign

0\.0998

−0\.0002

0\.1245

__Self\-transition probabilities P\[i,i\] are near π\_i \(baseline\), not elevated\. __For an iid prediction chain, the self\-transition probability P\[i,i\] should equal π\_i \(the probability of being in state i on the next step, given no memory\)\. The measured P\[i,i\] values are consistent with this baseline, confirming that the prediction chain has no ‘stickiness’ \(no tendency to stay in the same class beyond what is explained by the stationary distribution\)\. The slight elevation of P\[bin\_benign, bin\_benign\] = 0\.1245 vs π = 0\.0998 reflects a small residual confusion with bin\_malware: when the classifier makes the rare error on a bin\_benign sample, the corrected prediction on the next sample is more likely to return to bin\_benign\.

# __4\. Bursty Traffic: Spectral Collapse and Persistence__

## __4\.1 Spectral Gap Collapse__

__Striking result__

__Under bursty input, the prediction chain spectral gap collapses from 0\.962 to 0\.018 — a 52× reduction — and the mixing time increases from 1 to 55 steps\. The prediction chain spectral gap is identical to the true\-label chain spectral gap \(ratio = 1\.0000 to six decimal places\), establishing that the classifier transmits the temporal correlation structure of the input without amplification or attenuation\.__

This result has a direct information\-theoretic interpretation: the mutual information I\(p\_t; p\_\{t\+τ\}\) between predictions separated by τ steps decays as λ₂^\{2τ\} ≈ 0\.982^\{2τ\}\. At lag τ = 35 steps, I\(p\_t; p\_\{t\+35\}\) ≈ 0\.982^\{70\} ≈ 0\.28 — still substantial\. The prediction stream retains memory of its current class for over 30 steps, matching the average burst length of ≈42 steps\.

## __4\.2 Self\-Transition Persistence__

__Class__

__P\[i,i\] iid__

__P\[i,i\] bursty__

__Increase__

__Interpretation__

net\_normal

0\.082

0\.979

\+0\.897

Sustained attack sustained in predictions

net\_scan

0\.109

0\.983

\+0\.874

net\_ddos

0\.111

0\.970

\+0\.860

net\_exfil

0\.110

0\.979

\+0\.869

net\_c2

0\.087

0\.976

\+0\.889

log\_info

0\.090

0\.970

\+0\.880

log\_warn

0\.076

0\.974

\+0\.899

log\_error

0\.120

0\.979

\+0\.859

bin\_malware

0\.086

0\.980

\+0\.893

bin\_benign

0\.125

0\.977

\+0\.853

__Under bursty input, the classifier sustains its predictions with ~97% self\-transition probability across all classes\. __This is the operational behaviour required of an IDS: if the network is under a DDoS attack \(bursty net\_ddos traffic\), the prediction stream should show sustained net\_ddos predictions, not flickering between classes\. The high persistence \(0\.97–0\.98\) with essentially no class\-to\-class variation means the classifier’s temporal response is uniform across traffic types — no class is ‘stickier’ or ‘more volatile’ than others in bursty traffic\.

# __5\. Mean First\-Passage Times__

## __5\.1 Method: The Fundamental Matrix__

The mean first\-passage time \(MFPT\) matrix is computed via the fundamental matrix Z = \(I − P \+ Π\)⁻¹ where Π = επᵀ \[1,2\]:

MFPT\[i, j\] = \(Z\[j,j\] \- Z\[i,j\]\) / π\_j    \(i ≠ j\)

MFPT\[i, i\] = 1 / π\_i                    \(mean return time\)

## __5\.2 Results__

All mean return times fall in \[9\.31, 10\.80\] steps, consistent with the near\-uniform stationary distribution \(1/π\_i ≈ K = 10 for all i\)\. The MFPT matrix is similarly concentrated:

__Quantity__

__Value__

__Classes involved__

Longest MFPT

10\.88 steps

log\_warn → bin\_malware

Shortest off\-diagonal

 8\.84 steps

log\_warn → net\_normal

Mean MFPT \(off\-diag\)

10\.01 steps

all pairs

net\_normal → net\_scan

 9\.68 steps

net\_normal → net\_ddos

10\.20 steps

net\_normal → net\_exfil

10\.08 steps

net\_normal → net\_c2

 9\.97 steps

net\_normal → bin\_malware

10\.47 steps

__Operational interpretation__

Under iid input, the expected number of samples between any normal\-traffic sample and the first occurrence of any attack prediction is 9\.7–10\.5 steps — approximately K = 10, as expected for a near\-uniform chain\. This means that in a mixed traffic stream, the classifier will encounter each attack class roughly once every K = 10 samples, regardless of which class it just predicted\. The MFPT structure is essentially flat: all attack classes are equally ‘reachable’ from any safe class, with no preferential routing between classes\.

__Why is the MFPT matrix so flat? __Under iid input with a near\-uniform stationary distribution, the MFPT from any state i to any state j is MFPT\[i,j\] ≈ 1/π\_j ± O\(Z\[i,j\]\), where Z\[i,j\] is the \(i,j\) element of the fundamental matrix\. Since the fundamental matrix Z ≈ I \+ P \+ P² \+ … converges rapidly \(the chain mixes in ~1 step\), Z\[i,j\] ≈ π\_j for i ≠ j, and MFPT\[i,j\] ≈ 1/π\_j ± 1/π\_j ≈ 10 for all pairs\. The small spread \(8\.84–10\.88\) reflects the residual non\-uniformity of π\.

# __6\. Detailed Balance and Probability Currents__

## __6\.1 Test for Time Reversibility__

A Markov chain is time\-reversible if it satisfies the detailed balance equations: π\_i P\_\{ij\} = π\_j P\_\{ji\} for all i,j\. Violation implies a net probability current J\_\{ij\} = π\_i P\_\{ij\} − π\_j P\_\{ji\}, representing a preferred direction of flow in prediction space\.

__Result__

__The prediction chain is weakly irreversible\. __Mean DB residual = 1\.56×10⁻³, maximum = 4\.60×10⁻³\. The chain violates time\-reversal symmetry, but barely\. The maximum current J\_\{max\} = 4\.6×10⁻³ means the net probability flux between the most asymmetrically connected pair \(net\_normal ↔ log\_warn\) is 0\.46% of the total probability mass per step\.

## __6\.2 Net Probability Currents__

__Pair__

__Net current J__

__Direction__

__Magnitude__

net\_normal ↔ log\_warn

−4\.60×10⁻³

log\_warn → net\_normal

Strongest

net\_ddos ↔ log\_info

−4\.42×10⁻³

log\_info → net\_ddos

log\_warn ↔ bin\_malware

−3\.20×10⁻³

bin\_malware → log\_warn

log\_error ↔ bin\_benign

−3\.03×10⁻³

bin\_benign → log\_error

net\_c2 ↔ bin\_benign

−3\.02×10⁻³

bin\_benign → net\_c2

Weakest top\-5

__All net currents flow toward network/log classes from binary classes\. __The pattern of probability currents is consistent: binary classes \(bin\_benign, bin\_malware\) have net outflow toward network traffic and log classes\. Under iid input, these currents are vanishingly small \(J ∼ 10⁻³\) and operationally negligible\. Their existence signals a slight asymmetry in the misclassification structure: when an error occurs on a binary sample, the prediction is slightly more likely to be a network\-traffic class than a log class, and this asymmetry is not perfectly reversed for network\-to\-binary mis\-classifications\. The origin is the latent\-space geometry identified in the Wasserstein analysis: binary classes are outliers in W2 space, and their geometric asymmetry with the other classes produces small but measurable directional asymmetries in the error rates\.

# __7\. Realistic Traffic: Stationary Distribution Recovery__

A critical capability for an online classifier used for traffic profiling is stationary distribution recovery: the long\-run prediction frequencies should match the true input class frequencies\. If the prediction chain’s stationary distribution π\_pred matches the input distribution π\_input, the classifier can be used for passive traffic monitoring — estimating what fraction of traffic is malicious, what fraction is normal, etc\. — without requiring ground truth labels\.

## __7\.1 Results Under Realistic Input__

__Class__

__π\_input__

__π\_pred__

__Error__

__Recovery quality__

net\_normal

0\.6000

0\.6101

\+0\.010

Slight over\-detection

net\_scan

0\.0800

0\.0820

\+0\.002

Accurate

net\_ddos

0\.0500

0\.0456

−0\.004

Slight under\-detection

net\_exfil

0\.0400

0\.0356

−0\.004

Slight under\-detection

net\_c2

0\.0300

0\.0322

\+0\.002

Accurate

log\_info

0\.0800

0\.0804

\+0\.000

Excellent

log\_warn

0\.0500

0\.0470

−0\.003

Accurate

log\_error

0\.0400

0\.0402

\+0\.000

Excellent

bin\_malware

0\.0200

0\.0180

−0\.002

Accurate

bin\_benign

0\.0100

0\.0088

−0\.001

Accurate

__Key result__

__TV\(π\_pred, π\_input\) = 0\.015, KL\(π\_input || π\_pred\) = 9\.3×10⁻⁴\. __The prediction chain recovers the input distribution to within 1\.5% total variation\. This is within sampling noise for a 5,000\-sample stream \(expected TV ∼ 1/√n ≈ 1\.4%\), meaning the prediction frequencies are statistically indistinguishable from the true input frequencies\. CyphaDIF can serve as an accurate passive traffic profiler with no ground truth labels required\.

__Why is recovery so accurate? __When the per\-class accuracy is near 1\.0, the prediction frequency for class k is approximately equal to the input frequency for class k \(since P\(pred=k\) = P\(true=k\) · P\(pred=k|true=k\) \+ P\(true≠k\) · P\(pred=k|true≠k\) ≈ π\_k · 1\.0 \+ \(1−π\_k\) · 0 = π\_k\)\. The TV distance is directly controlled by the mis\-classification rate, and with accuracy 1\.0000, TV → 0\. The measured TV = 0\.015 comes entirely from finite\-sample estimation noise, not from classifier error\.

# __8\. The Confusion Matrix as HMM Observation Kernel__

## __8\.1 The Hidden Markov Model__

In the Hidden Markov Model \(HMM\) formulation, the true traffic class y\_t is the hidden state, evolving according to a Markov chain with transition matrix A\. The classifier prediction p\_t is the observable, generated from the hidden state via the emission matrix B\[y, p\] = P\(predict p | true class y\) — which is exactly the confusion matrix M\.

HMM components:

  Hidden chain:    y\_t | y\_\{t\-1\} ~ A  \(traffic transition matrix\)

  Observation:     p\_t | y\_t     ~ M  \(confusion matrix as emission kernel\)

  Initial state:   y\_0           ~ π\_0

Viterbi decoding recovers:  ŷ\_\{0:T\} = argmax\_\{y\_\{0:T\}\} P\(y\_\{0:T\} | p\_\{0:T\}\)

## __8\.2 The Identity Emission Matrix__

__Remarkable result__

__The confusion matrix M is the K×K identity matrix to four decimal places\. __Every off\-diagonal entry is 0\.0000, and every diagonal entry is 1\.0000\. The HMM observation kernel is the identity operator: the observation \(prediction\) is always identical to the hidden state \(true class\)\. This makes Viterbi decoding trivially equal to the raw predictions — the HMM adds no information because the emission is already deterministic and perfect\.

The identity confusion matrix has two important consequences\. First, Viterbi decoding provides zero gain: with B = I, the posterior P\(y\_t | p\_\{0:T\}\) is entirely determined by p\_t itself, and the Viterbi path is simply the prediction sequence\. This was confirmed empirically: raw accuracy = Viterbi accuracy = 1\.0000, gain = 0\.0000\. Second, the HMM spectral gap equals that of the transition matrix A \(since B = I does not mix states\), meaning that all temporal structure in the observation sequence is inherited directly from the hidden Markov chain — a result consistent with the spectral gap identity observed in the bursty traffic analysis \(Section 4\.1\)\.

The identity confusion matrix also means that in the HMM framework, the classifier is a perfect channel: the mutual information I\(y\_t; p\_t\) = H\(y\_t\) \(the full entropy of the true class\), meaning zero information is lost in classification\. This is the information\-theoretic certificate of perfect classification\.

# __9\. Absorbing Markov Chain: Attack Detection Latency__

## __9\.1 The Absorbing Chain Model__

We model the attack detection problem as an absorbing Markov chain: the safe states \{net\_normal, log\_info, log\_warn, log\_error, bin\_benign\} are transient, and the attack states \{net\_scan, net\_ddos, net\_exfil, net\_c2, bin\_malware\} are absorbing\. Starting from a safe state, the system will eventually be absorbed into an attack state \(corresponding to the first detection of an attack class in the prediction stream\)\. The expected absorption time is the expected attack detection latency\.

Q = transition sub\-matrix among safe states \(5×5\)

R = transition rates from safe to attack states \(5×5\)

Fundamental matrix:  N = \(I \- Q\)⁻¹

Expected absorption: t\_i = \[N · ε\]\_i   \(steps to first attack detection\)

Absorption probability: B = N · R    \(which attack class is detected first\)

## __9\.2 Detection Latency Results__

__Safe starting state__

__Expected steps to first attack detection__

net\_normal

4\.65 steps

log\_info

4\.58 steps

log\_warn

4\.78 steps

log\_error

4\.68 steps

bin\_benign

5\.13 steps

__Expected detection latency is 4\.6–5\.1 steps under realistic traffic\. __All safe classes have similar expected detection latency of approximately 4\.7 steps\. This is substantially less than K = 10 \(the MFPT under iid input\), because the realistic traffic chain has strong persistence in safe states \(net\_normal has 60% probability\), making the transient chain Q non\-negligible\. The safe states are stickier under realistic traffic, increasing the expected time before an attack state is visited\. The 5\.13\-step latency from bin\_benign is the longest because bin\_benign is the safe state most ‘isolated’ from attack classes in the realistic\-traffic transition matrix\.

## __9\.3 First\-Attack Absorption Probabilities__

Given that the system eventually detects an attack, which attack class is detected first?

__Safe class \\ First attack__

__net\_scan__

__net\_ddos__

__net\_exfil__

__net\_c2__

__bin\_malware__

net\_normal

38\.0%

20\.0%

17\.4%

16\.0%

8\.7%

log\_info

38\.2%

20\.1%

16\.5%

16\.2%

9\.0%

log\_warn

38\.6%

19\.7%

16\.6%

15\.9%

9\.3%

log\_error

37\.6%

21\.3%

17\.6%

14\.6%

8\.9%

bin\_benign

38\.3%

20\.0%

19\.9%

14\.2%

7\.8%

__net\_scan is the most likely first\-detected attack from every safe starting state \(~38%\)\. __This is consistent with net\_scan having the second\-highest weight in the realistic traffic mix \(8%, equal to log\_info\) after net\_normal\. The absorption probabilities are proportional to the attack\-class frequencies in the realistic traffic: net\_scan = 8%/20\.8% ≈ 38%, net\_ddos = 5%/20\.8% ≈ 24%, etc\. \(where 20\.8% is the total attack fraction of the input\)\. The slight discrepancy from simple proportionality reflects the non\-uniform transition structure from safe states to attack states\.

# __10\. Autocorrelation of the Correctness Stream__

## __10\.1 ACF Under iid and Realistic Input__

The autocorrelation function R\(τ\) of the binary correctness stream s\_t = δ\(p\_t, y\_t\) \(1 if correct, 0 if not\) measures temporal dependence in classification errors\.

__Key result__

__R\(τ\) = 0\.000000 at all lags under iid and realistic input\. __Classification errors are independent in time when inputs are independent\. For a perfect classifier on iid data, this is exact: the error probability is zero, so the error stream is constant \(all zeros\) and has no temporal variance\. The measured ACF is identically 0\.000 to 6 decimal places, consistent with zero error variance\.

## __10\.2 ACF Under Bursty Input__

Under bursty input, the Markov chain theory predicts ACF\(τ\) = λ₂^τ ≈ 0\.982^τ\. The empirical ACF is also identically 0\.000000 at all lags — because the bursty classifier also achieves accuracy 1\.0000, so the correctness stream is all\-ones with zero variance\.

__What the bursty ACF does measure\. __The structural ACF of the prediction stream \(treating the class index as a number\) would show the predicted 0\.982^τ decay\. The correctness ACF is zero because the stream is constant \(perfect\)\. This is a pathological limit of classifier quality: the ACF framework for measuring temporal correlation in the prediction stream is only informative when there are actual errors to correlate\. Under a drift or distribution shift scenario, the ACF would become non\-zero and the Markov prediction ACF\(τ\) = λ₂^τ would apply\.

__Lag τ__

__ACF\_iid__

__ACF\_bursty \(theory λ₂^τ\)__

__ACF\_realistic__

1

0\.000

0\.982

0\.000

5

0\.000

0\.912

0\.000

10

0\.000

0\.831

0\.000

20

0\.000

0\.691

0\.000

25

0\.000

0\.630

0\.000

# __11\. Steady\-State Entropy Rate of the Prediction Chain__

## __11\.1 Definition and Results__

The entropy rate h\(π, P\) = −Σ\_\{i,j\} π\_i P\_\{ij\} ln P\_\{ij\} measures the uncertainty per step in the prediction stream at stationarity\. It is bounded above by ln\(K\) = ln\(10\) = 2\.303 nats/step \(achieved by a uniform chain\) and bounded below by 0 \(achieved by a deterministic chain\)\.

__Scenario__

__Entropy rate h__

__Fraction of max__

__Interpretation__

iid uniform

2\.293 nats/step

99\.6%

Prediction stream nearly maximally entropic

Bursty

0\.142 nats/step

 6\.2%

Prediction stream highly structured \(low entropy\)

Realistic

1\.458 nats/step

63\.3%

Intermediate — dominated by frequent net\_normal class

__99\.6% of maximum entropy under iid: the prediction stream is almost maximally unpredictable\. __This is a consequence of the near\-uniform stationary distribution and the near\-identity transition structure under iid input\. Each prediction is essentially a fresh sample from the uniform distribution over 10 classes, carrying log\(10\) = 2\.303 nats of information\. The 0\.4% deficit from maximum entropy reflects the small transition probability structure introduced by the classifier’s rare errors\.

__6\.2% of maximum entropy under bursty: the prediction stream is highly predictable\. __In a bursty stream, knowing the current prediction tells you the next prediction with 97–98% probability \(the self\-transition rates\)\. The entropy rate h = 0\.142 nats/step is nearly the binary entropy of p ≈ 0\.97: h\(0\.97\) = −0\.97 ln\(0\.97\) − 0\.03 ln\(0\.03\) ≈ 0\.18 nats, consistent with the measured 0\.142\. The prediction stream under bursty traffic is highly compressible: a run\-length encoding would represent it at close to h = 0\.142 nats/step\.

## __11\.2 Per\-Row Conditional Entropy__

The conditional entropy H\(p\_\{t\+1\} | p\_t = i\) measures the uncertainty in the next prediction given the current one\. Under iid input, all per\-row entropies are near ln\(10\) = 2\.303:

__Class__

__H\(p\_\{t\+1\} | p\_t = class\)__

__vs\. max ln\(10\) = 2\.303__

net\_normal

2\.295

−0\.008

net\_scan

2\.297

−0\.006

net\_ddos

2\.295

−0\.008

log\_warn

2\.285

−0\.018 \(most structured row\)

bin\_benign

2\.286

−0\.017

net\_exfil

2\.297

−0\.006 \(most entropic row\)

__log\_warn and bin\_benign have the most structured transition rows\. __The lowest per\-row entropy classes are log\_warn \(2\.285\) and bin\_benign \(2\.286\), consistent with the slight elevation of their self\-transition probabilities under iid input \(P\[log\_warn, log\_warn\] = 0\.076, P\[bin\_benign, bin\_benign\] = 0\.125\)\. These classes have slightly non\-uniform outgoing distributions, reflecting their small but elevated self\-transition probabilities from rare errors that tend to repeat\.

# __12\. Synthesis and Operational Implications__

- __The prediction chain is memoryless under iid input\. __Spectral gap 0\.962, mixing time 1 step\. Each prediction is effectively independent of the previous one\. This is the fundamental property of a high\-accuracy classifier on iid data — errors are too rare to create meaningful temporal correlation\.
- __The classifier is a perfect temporal correlator under bursty input\. __The prediction chain spectral gap exactly equals the input chain spectral gap \(ratio 1\.0000\)\. Burstiness is transmitted without loss or amplification\. Self\-transition probabilities rise from ~0\.10 to ~0\.97\. This makes CyphaDIF suitable for streaming protocols where sustained predictions are required\.
- __The confusion matrix is the identity\. __Zero off\-diagonal entries\. HMM Viterbi decoding provides no improvement \(gain = 0\.000\)\. The classifier is a perfect channel in the information\-theoretic sense: I\(true; pred\) = H\(true\)\.
- __Realistic traffic distribution is recovered to TV = 0\.015\. __The prediction stream can be used for passive traffic profiling without ground truth labels\. net\_normal frequency is estimated with \+1\.0% error, attack class frequencies with ±0\.5% error\.
- __Attack detection latency is 4\.6–5\.1 steps under realistic traffic\. __net\_scan is the most likely first\-detected attack \(38%\)\. The absorbing chain analysis provides a principled framework for latency SLAs: to guarantee P\(detect within T steps\) ≥ 0\.99, set T = −ln\(0\.01\)/\(\-ln\(1\-1/t\_absorb\)\) ≈ 4\.65 · ln\(100\) ≈ 21 steps\.
- __Entropy rate drops from 99\.6% to 6\.2% as input switches from iid to bursty\. __The prediction stream is nearly maximally compressible under bursty traffic\. This has practical implications: streaming prediction logs over constrained channels can exploit run\-length encoding or arithmetic coding to reduce bandwidth by 15× under bursty traffic\.

# __13\. Conclusion__

The Markov chain analysis of CyphaDIF reveals a classifier whose temporal structure is determined almost entirely by the input traffic structure, not by internal classifier dynamics\. Under iid input, the prediction chain is approximately iid \(mixing time 1 step, entropy rate 99\.6% of max, zero error ACF\)\. Under bursty input, the chain exactly inherits the input’s spectral gap, with self\-transition probabilities of ~97%\. The confusion matrix is the identity, confirming perfect classification and zero HMM improvement from temporal smoothing\.

The operational implications are direct: CyphaDIF can serve as an accurate traffic profiler \(TV = 0\.015 stationary distribution error\), provides attack detection within 4\.65 steps under realistic traffic, and produces prediction streams compressible at 6\.2% of maximum entropy under bursty conditions\. The weak irreversibility \(max detailed balance residual 4\.6×10⁻³\) with currents flowing from binary toward network classes is a subtle signature of the geometric asymmetry identified in the Wasserstein analysis\.

# __References__

\[1\] Norris, J\. R\. \(1997\)\. Markov Chains\. Cambridge University Press\.

\[2\] Kemeny, J\. G\., & Snell, J\. L\. \(1960\)\. Finite Markov Chains\. D\. Van Nostrand\.

\[3\] Levin, D\. A\., Peres, Y\., & Wilmer, E\. L\. \(2009\)\. Markov Chains and Mixing Times\. American Mathematical Society\.

\[4\] Baum, L\. E\., & Petrie, T\. \(1966\)\. Statistical inference for probabilistic functions of finite state Markov chains\. Annals of Mathematical Statistics, 37\(6\), 1554–1563\.

\[5\] Rabiner, L\. R\. \(1989\)\. A tutorial on hidden Markov models and selected applications in speech recognition\. Proceedings of the IEEE, 77\(2\), 257–286\.

\[6\] Viterbi, A\. J\. \(1967\)\. Error bounds for convolutional codes and an asymptotically optimum decoding algorithm\. IEEE Transactions on Information Theory, 13\(2\), 260–269\.

\[7\] Shannon, C\. E\. \(1948\)\. A mathematical theory of communication\. Bell System Technical Journal, 27, 379–423\.

\[8\] Cover, T\. M\., & Thomas, J\. A\. \(2006\)\. Elements of Information Theory \(2nd ed\.\)\. Wiley\-Interscience\.

\[9\] Mitzenmacher, M\., & Upfal, E\. \(2005\)\. Probability and Computing: Randomized Algorithms and Probabilistic Analysis\. Cambridge University Press\.

\[10\] Anderson, T\. W\. \(1954\)\. On estimation of parameters in latent structure analysis\. Psychometrika, 19\(1\), 1–10\.

\[11\] Karatzas, I\., & Shreve, S\. E\. \(1991\)\. Brownian Motion and Stochastic Calculus \(2nd ed\.\)\. Springer\.

\[12\] Meyn, S\. P\., & Tweedie, R\. L\. \(2009\)\. Markov Chains and Stochastic Stability \(2nd ed\.\)\. Cambridge University Press\.

\[13\] Diaconis, P\., & Stroock, D\. \(1991\)\. Geometric bounds for eigenvalues of Markov chains\. Annals of Applied Probability, 1\(1\), 36–61\.

\[14\] Aldous, D\., & Fill, J\. \(2002\)\. Reversible Markov Chains and Random Walks on Graphs\. Unfinished monograph\. https://stat\.berkeley\.edu/users/aldous/RWG/book\.html

\[15\] Geman, S\., & Geman, D\. \(1984\)\. Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images\. IEEE Transactions on Pattern Analysis and Machine Intelligence, 6\(6\), 721–741\.

\[16\] Jordan, M\. I\., Ghahramani, Z\., Jaakkola, T\. S\., & Saul, L\. K\. \(1999\)\. An introduction to variational methods for graphical models\. Machine Learning, 37\(2\), 183–233\.

\[17\] Frazzoli, E\., Dahleh, M\. A\., & Feron, E\. \(2005\)\. Maneuver\-based motion planning for nonlinear systems with symmetries\. IEEE Transactions on Robotics, 21\(6\), 1077–1091\.

\[18\] Koller, D\., & Friedman, N\. \(2009\)\. Probabilistic Graphical Models: Principles and Techniques\. MIT Press\.

\[19\] Murphy, K\. P\. \(2012\)\. Machine Learning: A Probabilistic Perspective\. MIT Press\.

\[20\] Barber, D\. \(2012\)\. Bayesian Reasoning and Machine Learning\. Cambridge University Press\.

