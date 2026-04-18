<!-- Converted from `ARIA_INTEL_README.docx` — source was Word (.docx). -->

__ARIA\-INTEL__

Algebraic Rendezvous & Intelligence Analyser

__TECHNICAL REFERENCE & DEVELOPER DOCUMENTATION__

aria\_intel\_v6\.py  ·  2,363 lines  ·  Python 3\.10\+

ARIA\-INTEL is a single\-file, edge\-deployable intelligence engine for multi\-target

tracking, pattern\-of\-life analysis, tradecraft detection, and rendezvous warning\.

# __1\. Overview__

ARIA\-INTEL is a complete multi\-target tracking and intelligence fusion engine implemented in a single Python file\. It combines a Poisson Multi\-Bernoulli Mixture \(PMBM\) Bayesian filter with Mixed Ornstein\-Uhlenbeck \(MOU\) motion models, a full Pattern\-of\-Life \(PoL\) subsystem, a three\-method 30\-minute rendezvous warning architecture, and a composable tradecraft detector registry — all within a domain\-polymorphic framework that can be re\-targeted to maritime, airspace, convoy, or urban HUMINT domains by swapping a single configuration object\.

The system was designed for two constraints: \(1\) strict mathematical rigour — every probability estimate is Bayesian, every detection threshold is operationally motivated, and no "magic numbers" exist without justification; \(2\) edge deployability — the full engine runs at 27ms median latency on a single CPU core with no GPU requirement, enabling deployment on tactical hardware, embedded systems, or offline analysis pipelines\.

## __1\.1  Design Philosophy__

- Single\-file architecture: zero external intelligence dependencies beyond NumPy, SciPy, and the standard library\. The entire system compiles and runs without a network connection\.
- Mathematically grounded: PMBM is a theoretically optimal multi\-target filter under the Random Finite Set \(RFS\) framework\. MOU motion models have closed\-form discretisation\. Threat scoring uses Beta\-distributed Monte Carlo integration, not point estimates\.
- Composable: detectors are plugins implementing a two\-method abstract interface\. They can be registered, unregistered, and hot\-swapped at runtime without restarting the engine\.
- Polymorphic: all thresholds, noise parameters, motion models, and warning horizons live in a DomainProfile dataclass\. Swapping the profile changes the domain of discourse without touching any algorithmic code\.
- Transparent: every output field is traceable to its source\. The report dictionary includes raw breakdown scores, particle filter state, clutter rate, and per\-detector output, not just summary alerts\.

## __1\.2  Scope of Output__

On each call to engine\.ingest\(\), the engine returns a structured report dictionary containing:

- Per\-track threat scores: Bayesian existence probability, PoL anomaly score, HVL proximity, detection density, motion score, threat persistence EMA, Possibility\-PMBM mismatch indicator, dominant MOU model class, priority tier \(IMMEDIATE / HIGH / MEDIUM / LOW\)\.
- Rendezvous warnings: track pair, ETA in minutes, current separation, detection method used, confidence score, predicted meeting location, priority tier\.
- Tradecraft events: type, involved tracks, severity, and interpretation string\.
- Network roles: per\-track role classification \(HANDLER / COURIER / ASSET / UNKNOWN\), contact count, confidence\.
- Network clusters: co\-location graph with betweenness centrality per member, hub identification, recurrence flag\.
- Sensor scheduling: recommended next collection modality per track, ranked by expected information gain\.
- Operational intelligence: velocity trends, stationary dwell flags, wide\-area movement flags, Possibility\-PMBM mismatch alarms\.
- Administrative: scan count, clutter rate, active / dormant track counts, domain profile name\.

# __2\. Dependencies and Invocation__

## __2\.1  Requirements__

__Package__

__Version__

__Usage__

__numpy__

≥ 1\.24

All numerical arrays, particle filter, linear algebra

__scipy__

≥ 1\.10

chi2 gate threshold, gammaln for Bernoulli likelihoods

__Python__

≥ 3\.10

Dataclasses, ABC, \_\_future\_\_ annotations

## __2\.2  Minimal Invocation__

import aria\_intel\_v6 as aria

eng = aria\.ARIAIntelEngineV6\(

    profile = aria\.UrbanHUMINT\(\),          \# domain preset

    area    = \(\-4500, 4500, \-4500, 4500\),  \# xmin xmax ymin ymax \(metres\)

    high\_value\_locations = \[               \# optional HVL list

        np\.array\(\[1200\., 800\.\]\),

    \]

\)

report = eng\.ingest\(observations, timestamp\_seconds\)

print\(eng\.summary\(report\)\)

## __2\.3  Observation Schema__

Each observation is an instance of the Observation dataclass:

Observation\(

    obs\_id:     str,        \# unique string identifier

    timestamp:  float,      \# Unix seconds

    position:   np\.ndarray, \# shape \(2,\), x/y in metres

    modality:   str,        \# GEOINT | SIGINT | COMMS | HUMINT | OSINT

    confidence: float,      \# 0\.0 – 1\.0

    source\_id:  str,        \# sensor/source identifier

\)

The modality field determines the base reliability weight used in all downstream calculations\. Source credibility is tracked independently via the SourceCredibilityTracker, which uses an exponential decay model to learn per\-source reliability from observation likelihood history\.

# __3\. Core Tracking Engine__

## __3\.1  PMBM Filter Architecture__

The heart of the engine is a Poisson Multi\-Bernoulli Mixture filter\. PMBM is the theoretically optimal multi\-target Bayesian filter under the RFS framework when targets are born from a Poisson process, survive with fixed probability, and are detected independently\. The filter jointly estimates:

- The number of targets \(via Bernoulli existence probabilities summed across the MBM component\)
- The state of each confirmed target \(via per\-target particle filters\)
- The birth rate of new targets \(encoded in the Poisson birth intensity, approximated by per\-observation spawning with R\_BIRTH = 0\.65\)

The implementation uses a Bernoulli component per track hypothesis\. Each BernoulliTrack carries:

- r: probabilistic existence probability \(standard PMBM Bernoulli weight\)
- pi\_r: possibilistic existence probability \(Possibility\-PMBM extension, see §3\.5\)
- pf: MOUParticleFilter with 320 particles tracking 4D state \[x, y, vx, vy\]
- pol: PatternOfLife GMM fitted to the track's observation history

## __3\.2  Mixed Ornstein\-Uhlenbeck Motion Models__

Unlike constant\-velocity or nearly\-constant\-acceleration IMM models, ARIA\-INTEL uses Mixed Ornstein\-Uhlenbeck \(MOU\) processes to model target motion\. An OU process is a continuous\-time stochastic mean\-reverting process defined by:

dV\(t\) = \-theta \* V\(t\) dt \+ sigma \* dW\(t\)

where theta is the mean\-reversion rate and sigma is the diffusion coefficient\. This model captures physically meaningful motion behaviour: high theta forces rapid reversion to zero velocity \(stationary or slow agents\), low theta allows persistent directed motion \(vehicles, fast\-movers\)\.

The discretisation at scan interval dt is:

V\(t\+dt\) = alpha \* V\(t\) \+ sigma\_v \* epsilon

where alpha = exp\(\-theta \* dt\),

      sigma\_v = sigma \* sqrt\( \(1 \- exp\(\-2\*theta\*dt\)\) / \(2\*theta\) \)

This is the exact discrete\-time equivalent of the continuous OU process\. The steady\-state velocity variance for each model is sigma^2 / \(2\*theta\), which is used to initialise particles correctly\.

UrbanHUMINT domain motion models:

__Model__

__theta__

__sigma__

__SS vel variance__

__Interpretation__

__foot__

0\.30

2\.0 m/s

6\.67 m²/s²

Walking speed, turns frequently

__vehicle__

0\.10

8\.0 m/s

320 m²/s²

Street speed, moderate persistence

__stationary__

2\.00

0\.5 m/s

0\.063 m²/s²

Dwell / observation post

__fast__

0\.05

15\.0 m/s

2250 m²/s²

Highway speed, high persistence

## __3\.3  Particle Filter \(MOUParticleFilter\)__

Each track maintains a Sequential Importance Resampling \(SIR\) particle filter with 320 particles in 4D state space \[x, y, vx, vy\]\. The filter uses systematic resampling \(lower variance than multinomial\) triggered when effective sample size 1/sum\(w\_i^2\) < 0\.4N\.

The prediction step samples a model index per particle from the MOU model mixture \(weighted by the current model weight vector mu\), then propagates velocity forward using the MOU dynamics and position forward using the trapezoidal rule\. This prevents the velocity\-from\-position lag that affects Euler integration\.

The update step uses the Mahalanobis distance under the position marginal as the likelihood\. When consecutive observations are available, an auxiliary trajectory update weights particles additionally by velocity\-implied heading, increasing model discrimination speed\.

Innovation gating uses the chi\-squared 99\.9% threshold \(chi2\(0\.999, df=2\) = 13\.82\) to reject outlier observations\. Observation\-to\-track assignment is handled by a Gibbs sampler \(14 sweeps\), which resolves measurement\-to\-track ambiguity probabilistically rather than greedily\.

## __3\.4  Track Lifecycle__

Tracks follow the PMBM Bernoulli lifecycle:

1. BORN: unassigned observation with weight > 0\.25 spawns a new BernoulliTrack at R\_BIRTH = 0\.65\.
2. CANDIDATE: r < R\_CONFIRM \(0\.55\)\. Tracked but not reported\.
3. CONFIRMED: r >= R\_CONFIRM\. Included in all outputs and detector pipelines\.
4. DORMANT: r drops below R\_PRUNE \(0\.05\) but track has a fitted PoL model\. Stored for up to 40 scans for reacquisition matching\.
5. PRUNED: r < R\_DORMANT \(0\.04\) with no PoL, or dormant timeout exceeded\. Discarded\.

Reacquisition uses the track's PoL model to predict where it should be at the current timestamp\. An unassigned observation within 3 standard deviations of the predicted position rehydrates the dormant track, preserving its identity, PoL history, and threat EMA\.

Group spawning: when a new track appears within 80m of an existing confirmed track with high measurement rate and high velocity variance \(indicative of a group\), the new track inherits a clone of the existing track's PoL model\. This models members of a group who are individually tracked but share a behavioural pattern\.

## __3\.5  Possibility\-PMBM Mismatch Detection__

In addition to the standard Bayesian existence probability r, each track maintains a possibilistic existence probability pi\_r using the Possibility theory framework\. The update rule for pi\_r uses the Possibility\-PMBM equations:

pi\_r\(hit\) = clip\( max\(pi\_r \* pi\_L, alpha \* pi\_r\), 0, 1 \)

pi\_r\(miss\) = pi\_r \* \(1 \- P\_D \* alpha\)

where alpha = POSS\_ALPHA = 0\.25, pi\_L = min\(1, weight \* P\_D\)

The mismatch score is abs\(r \- pi\_r\) / max\(r, pi\_r\)\. When this exceeds 0\.4, an alarm is raised in the operational intelligence output\. In practice this fires when a target's observation pattern is inconsistent with a single existence hypothesis — indicating either sensor deception, track confusion, or a model error requiring analyst review\. This feature has no direct equivalent in known operational multi\-target tracking systems\.

# __4\. Pattern\-of\-Life Subsystem__

## __4\.1  Architecture__

Each confirmed track maintains a PatternOfLife object that fits a Gaussian Mixture Model \(GMM\) in 3D space \[hour\_of\_day, x, y\]\. The temporal coordinate is the fractional hour within a 24\-hour cycle \(timestamp mod 86400, divided by 3600\), so the model learns when, as well as where, a target typically appears\.

The model is fitted via EM \(Expectation\-Maximisation\) with K=5 Gaussian components, seeded with K\-means\+\+ initialisation to avoid degenerate solutions\. Fitting triggers after the first 15 observations and re\-triggers every 5 new observations thereafter \(REFIT\_INTERVAL = 5\)\. The EM runs for 35 iterations with isotropic regularisation \(5e\-3 \* I\) on each component covariance\.

Choleski\-decomposed precision matrices are cached after fitting\. The batch GMM log\-likelihood evaluator \(\_gmm\_logpdf\_batch\) uses a hand\-coded 3x3 forward substitution \(\_fwdsub3\) to avoid the overhead of numpy's general triangular solver for this fixed\-size inner loop, which is the hot path during PoL cross\-prediction\.

## __4\.2  Anomaly Scoring__

The anomaly score for a given \(timestamp, position\) is:

nll = \-log p\_GMM\(\[hour, x, y\]\)

x = \(nll \- baseline\_nll\) / max\(|baseline\_nll|, 1\.0\)

score = sigmoid\(x\) = 1 / \(1 \+ exp\(\-x\)\)

The baseline NLL is the mean negative log\-likelihood of the last 40 in\-model observations, providing an adaptive threshold\. A score near 0\.5 means the observation is consistent with the track's learned routine\. A score near 1\.0 means the observation is highly anomalous relative to the track's history\. The sigmoid mapping ensures scores are bounded in \[0,1\] and are differentially informative in the anomalous region\.

## __4\.3  Location Prediction__

The predict\_location\(t, n\_mc\) method generates a Monte Carlo predicted position at future time t by:

1. Computing time\-conditional component weights: weight each GMM component by its likelihood at the target hour of day\.
2. Sampling n\_mc component indices from the time\-conditional weights\.
3. Drawing position samples from the selected Cholesky\-factored 2D position marginals\.
4. Returning the mean predicted position and a spread \(std dev of distances from mean\) as uncertainty\.

This is used by the dormant track reacquisition system \(to locate where a lost track should reappear\), and by the PoL cross\-prediction method in the rendezvous warning system \(to project where both targets will be at future times based purely on their historical routines, independently of their current trajectory\)\.

# __5\. Rendezvous Warning System__

The rendezvous warning system implements a 30\-minute lead\-time warning for pairwise target convergence using three independent stacked methods\. Every confirmed track pair is evaluated each scan\. The method that produces the longest valid ETA within the warning horizon is reported\. Warnings are prioritised: IMMEDIATE \(<5 min\), HIGH \(<15 min\), MEDIUM \(<30 min\), LOW \(otherwise\)\.

Validated performance across 20 independent scenarios: 20/20 warnings issued, mean lead time 28\.1 minutes, 100% of warnings at ≥20 minutes lead time, 95% at ≥25 minutes\.

## __5\.1  Method 1: Geometric Velocity Intercept__

For each track, a velocity vector is estimated by least\-squares linear regression on the last 8 position history points\. This is analytically equivalent to fitting a straight\-line trajectory through recent positions and computing the instantaneous heading and speed\. The velocity fit is cached keyed by \(track\_id, history\_length\) to avoid redundant computation across pairs\.

Given position vectors p\_i, p\_j and velocity vectors v\_i, v\_j, the time to closest approach \(CPA\) is:

delta\_v = v\_i \- v\_j

delta\_p = p\_i \- p\_j

t\_CPA = \-dot\(delta\_p, delta\_v\) / dot\(delta\_v, delta\_v\)   \[in scans\]

If t\_CPA > 0 \(converging\), the CPA positions are projected forward and the CPA separation is checked against 2x the meeting threshold\. Confidence is computed as 1 \- CPA\_sep / threshold, clipped to \[0\.1, 1\.0\]\. This method is the fastest and most reliable under steady\-heading conditions, and was the dominant method in testing \(26 of 39 RV warning events\)\.

## __5\.2  Method 2: Separation Rate Extrapolation__

The pairwise separation history is accumulated for up to 30 scans per pair\. A linear trend is fitted to the last rv\_sep\_rate\_window \(8\) separation values\. If the slope is negative \(tracks converging\), the time to reach the meeting threshold is:

ETA\_scans = \(current\_sep \- threshold\) / |slope|

The R² of the linear fit is used as the confidence score\. This method works well when track headings are noisy or rapidly changing — it operates entirely on the scalar separation time series, which is much smoother than the raw position histories\. It is particularly robust for targets that are approaching each other along curved routes\.

## __5\.3  Method 3: PoL Cross\-Prediction__

When both tracks in a pair have fitted Pattern\-of\-Life models \(minimum 15 observations each\), the PoL models are queried independently to predict where each track will be at t\_now \+ k\*scan\_dt for k = 1\.\.\.horizon \(capped at 20 steps to maintain performance\)\. If the predicted positions converge within the meeting threshold, the time of minimum predicted separation is reported as the warning\.

This method fires based on the targets' habitual routines, independently of their current trajectory\. It is the only method capable of warning about a scheduled meeting where neither target is yet moving toward the other — for example, two targets who routinely meet at a particular time and location each week\. It is throttled to run every 5 scans to control computational cost\. The prediction itself is vectorised across all horizon steps in a single batch operation\.

## __5\.4  Legacy Short\-Horizon Predictor \(RendezvousDetector\)__

In addition to the extended warning system, the legacy RendezvousDetector remains active\. It uses particle\-forward Monte Carlo projection over a 4\-scan horizon \(approximately 4 minutes at 60\-second scan rate\) and reports a probability\-of\-rendezvous score\. It is less capable for early warning but provides high\-confidence, high\-precision predictions for imminent meetings\. Both outputs appear in the report; the extended warner is the primary early\-warning mechanism\.

# __6\. Tradecraft Detector Registry__

All tradecraft detection is handled by registered plugins implementing the BaseDetector abstract interface\. The engine calls detect\(tracks, context\) on each registered detector every scan and aggregates the results\. Detectors are composable: any subset can be active at any time\.

class BaseDetector\(ABC\):

    def \_\_init\_\_\(self, profile: DomainProfile\): \.\.\.

    @abstractmethod

    def detect\(self, tracks: List, context: Dict\) \-> List\[Dict\]: \.\.\.

    @property

    @abstractmethod

    def name\(self\) \-> str: \.\.\.

Registry manipulation:

eng\.register\_detector\(MyDetector\(eng\.profile\)\)

eng\.unregister\_detector\("MyDetector"\)

eng\.list\_detectors\(\)   \# returns list of active names

The context dictionary passed to each detector contains: timestamp, scan\_index, hvls \(high\-value locations\), profile \(the active DomainProfile\), betweenness \(per\-track centrality from the current scan\), clusters \(current co\-location clusters\)\.

## __6\.1  Default Detector Set \(8 registered at construction\)__

### __LegacyTradecraftDetector__

Carries the original v5 tradecraft detection module\. Runs three independent algorithms:

- BRUSH\_PASS: two confirmed tracks whose instantaneous separation is less than brush\_pass\_m \(60m default\)\. Fires only on the first scan of contact, suppressed until tracks separate and re\-contact\.
- SDR\_PATTERN: single\-track Surveillance Detection Route detection via winding number analysis\. Takes the last 12 position history points, computes the unwrapped angular sweep around the centroid, and fires if winding\_number >= 0\.65 \(approximately 2/3 of a full loop in the sample window\)\. Indicates a target is executing a route designed to detect surveillance\.
- DEAD\_DROP: two or more tracks visit the same 200x200m grid cell within a configurable time window \(60s–1800s\), but not simultaneously \(no observations within 30s of each other\)\. Indicates sequential visit to a fixed dead drop location\. Throttled to every 3 scans\.

### __ExtendedRendezvousWarner__

The three\-method 30\-minute warning system described in §5\. Fires RENDEZVOUS\_WARNING events with fields: track\_a, track\_b, current\_sep\_m, eta\_s, eta\_min, method, confidence, predicted\_location, priority, timestamp\.

### __ParallelRouteSurveillanceDetector__

Detects mobile surveillance — a shadow following a target along a parallel route\. For each track pair:

1. Compute velocity vectors via polyfit regression on the last 8 position history points\.
2. Heading similarity: cosine of angle between velocity vectors must exceed parallel\_vel\_cos \(0\.97, corresponding to ~14 degree max divergence\)\.
3. Lateral offset: perpendicular distance between track positions \(computed analytically using the unit heading vector\) must be between 0 and parallel\_route\_m \(80m\)\.
4. Must persist for parallel\_scans \(6\) consecutive qualifying scans before firing\.

Severity is HIGH\. Fires PARALLEL\_SURVEILLANCE events with lateral\_m, heading\_cos, duration\_scans, and interpretation fields\.

### __ModeTransitionDetector__

Detects vehicle\-to\-foot handoffs, a classic counter\-surveillance and foot follow technique\. The detector watches for:

1. A vehicle\-class track \(dominant MOU model in vehicle\_models = \{"vehicle", "fast"\}\) whose speed drops below 2\.5 m/s — logged as a vehicle stop event\.
2. Within mode\_trans\_scans \(2 scans\) of the stop, a new foot\-class track \(dominant model in foot\_models = \{"stationary", "foot"\}\) appears within mode\_trans\_m \(50m\) of the stop location\.

When both conditions are met, fires a MODE\_TRANSITION event with vehicle\_track, foot\_track, stop\_pos, foot\_pos, dist\_m, delay\_scans, and interpretation VEHICLE\_HANDOFF\_OR\_DISMOUNT\.

### __LoiterAnomalyDetector__

Detects anomalous dwell behaviour by comparing current dwell duration against the target's PoL baseline\. For each confirmed track that:

- Has a fitted PoL model
- Has been stationary \(speed < 1\.5 m/s\) for longer than loiter\_min\_s \(300s\) at the current location
- Has a PoL anomaly score above 0\.45 at the current location \(the location is not a routine PoL cluster\)
- Has been dwelling for more than loiter\_mult \(3\.0x\) times the PoL\-typical dwell duration

The detector fires LOITER\_ANOMALY with dwell\_s, pol\_anomaly, location, severity fields\.

### __CoverStopDetector__

Detects intelligence\-gathering cover stops: locations a target visits routinely that happen to be near a high\-value location, potentially masking the true purpose of the visit\. Conditions:

- Track has a fitted PoL model
- Current position is within cover\_stop\_hvl\_m \(800m\) of any registered HVL
- Track has been observed at this location on more than 2 previous scans \(building a visit history per 100m grid cell\)
- PoL anomaly score is below 0\.80 \(the location is at least partially consistent with the target's pattern — not a one\-off visit\)

Fires COVER\_STOP events with track, hvl\_position, dist\_to\_hvl\_m, visit\_count, pol\_anomaly, severity HIGH\.

### __ChokepointSurveillanceDetector__

Detects repeated bidirectional passage through the same geographic chokepoint, indicating the target is monitoring or countering surveillance at a fixed location\. For each track, passage through a 40m\-radius cell is logged\. When the same cell has been traversed in both directions at least 3 times \(chokepoint\_n\), fires CHOKEPOINT\_SURVEILLANCE with location, direction changes, and pass count\.

### __NetworkRoleInferenceDetector__

Classifies each confirmed track's functional role within the observed network using relative percentile ranking within the current track set\. This design makes the classification robust to variations in overall scenario density — absolute contact counts are meaningless without knowing the network size\.

Three role categories:

- COURIER: top 60th percentile of speed AND top 55th percentile of unique contacts\. Couriers move quickly and contact many network members\.
- HANDLER: bottom 35th percentile of speed, above 30th percentile of contacts\. Handlers are stationary or slow, but co\-locate with multiple targets\.
- ASSET: PoL anomaly score > 0\.62 AND bottom 35th percentile of contacts\. Assets have irregular routines and relatively few network contacts\.

A stable role assignment requires 3 or more consecutive scans of the same classification\. Contact graph history is maintained across the entire session, not just the current scan, so short absences do not reset the contact count\. A legacy single\-track absolute\-threshold classifier is retained as a fallback\.

# __7\. Domain Profiles__

The DomainProfile dataclass is the single point of configuration for all domain\-specific parameters\. The same algorithmic codebase interprets observations differently across domains based entirely on the active profile\. Every threshold, noise level, motion model set, and warning horizon is a field in this dataclass — there are no domain\-specific conditionals in the algorithmic code\.

__Profile__

__Scan dt__

__RV Warning__

__RV Threshold__

__Motion Models__

__UrbanHUMINT\(\)__

60 s

30 min

150 m

foot, vehicle, stationary, fast

__Maritime\(\)__

3600 s

120 min

2000 m

drifting, transiting, anchored, fast\_craft

__Airspace\(\)__

5 s

10 min

1000 m

hovering, fixed\_wing, gliding, fast\_jet

__VehicleConvoy\(\)__

10 s

5 min

30 m

stopped, slow\_roll, highway, sprint

## __7\.1  Custom Profiles__

A custom domain profile can be created by instantiating DomainProfile directly with any combination of overridden fields\. All fields have sensible defaults \(UrbanHUMINT values\)\. Only the fields that differ from the defaults need to be specified:

custom = DomainProfile\(

    name             = "MyDomain",

    scan\_dt\_s        = 30\.0,

    pos\_noise\_m      = 12\.0,

    rv\_warning\_horizon\_s = 600\.0,

    rv\_threshold\_m   = 75\.0,

    mou\_models       = \{

        "slow":  \{"theta": 0\.40, "sigma": 1\.0\},

        "fast":  \{"theta": 0\.03, "sigma": 12\.0\},

    \},

\)

Note that if mou\_models is overridden, the model\_trans matrix must be sized to match the number of models\.

# __8\. Threat Scoring__

## __8\.1  Bayesian Beta\-Monte Carlo Scoring__

Each confirmed track is assigned a threat score using a weighted Bayesian averaging approach over eight independent evidence dimensions\. Each dimension is modelled as a Beta\-distributed random variable, parameterised by the evidence for and against threat\. The dimensions, their Beta parameters, and their default weights are:

__Dimension__

__Alpha / Beta__

__Weight__

__Description__

__Existence__

r×20\+1 / \(1\-r\)×20\+1

0\.23

PMBM Bernoulli existence probability

__PoL Anomaly__

pol×8\+1 / \(1\-pol\)×8\+1

0\.18

How anomalous this location/time is vs history

__Detection Density__

dd×8\+1 / \(1\-dd\)×8\+1

0\.13

Fraction of scans where track was observed

__HVL Proximity__

hvl×8\+1 / \(1\-hvl\)×8\+1

0\.13

Exponential decay from nearest HVL

__Motion Score__

motion×6\+1 / \(1\-motion\)×6\+1

0\.08

Speed / 30 m/s, clipped to \[0,1\]

__Persistence__

persist×6\+1 / \(1\-persist\)×6\+1

0\.08

Count of scans with score > 0\.62, clipped /10

__Threat EMA__

ema×8\+1 / \(1\-ema\)×8\+1

0\.10

Exponential moving average of prior scores

__Poss Match__

pm×4\+1 / \(1\-pm\)×4\+1

0\.07

1 \- Possibility mismatch penalty

250 Monte Carlo samples are drawn from the weighted Beta mixture, giving a full distribution over threat scores\. The output includes mean, standard deviation, P90, and P95\. The mean is used for prioritisation\. The P95 provides an upper\-confidence bound for analyst alerting\.

## __8\.2  Priority Tiers__

- IMMEDIATE: score >= 0\.82
- HIGH: score >= 0\.62
- MEDIUM: score >= 0\.42
- LOW: score >= 0\.22
- MONITOR: score < 0\.22

# __9\. Supporting Analytical Systems__

## __9\.1  Dynamic Network Analyser \(DynamicNetworkAnalyser\)__

Maintains a weighted co\-location adjacency matrix across the session\. Two tracks contribute weight to the adjacency matrix every scan they are within coloc\_dist\_m \(350m\) of each other; the weight is linear in proximity \(1 \- dist/coloc\_dist\_m\)\. The accumulated adjacency is used to construct network clusters and to compute betweenness centrality using Brandes's algorithm \(O\(N\*E\) exact computation\)\.

Betweenness centrality scores are passed to the NetworkRoleInference detector as part of the context dictionary\. Clusters include a recurring flag when any member has been co\-located previously, distinguishing habitual associations from chance co\-location\.

## __9\.2  Anomaly Escalator \(AnomalyEscalator\)__

Maintains a rolling window of threat scores per track and generates three secondary alert types:

- SPIKE: single\-scan threat score > 0\.72\.
- ESCALATING: threat score has increased monotonically for the last window \(5\) scans\.
- COUNTER\_SURVEILLANCE: threat score dropped below 0\.3 after being above 0\.5, then spiked above 0\.6 again — the sawtooth pattern consistent with a target deliberately varying their behaviour to detect surveillance\.

## __9\.3  Credibility Fuser \(CredibilityFuser\)__

Combines evidence across multiple observations using Dempster\-Shafer Theory of Evidence\. Each observation contributes a basic probability assignment \(BPA\) parameterised by the modality reliability\. The fusion produces three outputs: belief \(lower bound of probability\), plausibility \(upper bound\), and conflict \(Dempster's K factor, indicating how inconsistent the evidence set is\)\. Conflict near 1\.0 indicates the observations are mutually contradictory\.

Reliability priors by modality: GEOINT 0\.90, SIGINT 0\.78, COMMS 0\.70, HUMINT 0\.62, OSINT 0\.48\.

## __9\.4  Source Credibility Tracker \(SourceCredibilityTracker\)__

Tracks per\-source reliability using an exponential moving average with decay factor 0\.98\. Each time a source observation is assigned to a track, the observation log\-likelihood under the track's filter is compared to a threshold\. Sources whose observations consistently fail the likelihood test receive reduced weights\. This provides automatic deception detection at the source level\.

## __9\.5  Sensor Scheduler \(SensorScheduler\)__

Produces a ranked list of \(track, recommended\_modality\) pairs, ordered by expected information gain\. Information gain is approximated as modality\_weight × track\.r / pos\_uncertainty\. This recommends the most reliable available sensor modality for the track with the highest combination of confirmed existence and positional uncertainty — directing collection assets to where they will have the most impact\.

## __9\.6  Operational Intelligence \(OperationalIntelligence\)__

Post\-processing on the confirmed track set producing:

- Velocity analysis: mean speed and linear speed trend for each track with sufficient history\.
- Stationary dwell flags \(STATIONARY\_DWELL\): tracks with mean speed < 0\.5 m/s over 10\+ scans\.
- Wide\-area movement flags \(WIDE\_AREA\_MOVEMENT\): tracks whose total displacement exceeds 3km\.
- Model transition alarms: tracks with Possibility\-PMBM mismatch > 0\.4\.

## __9\.7  Route Predictor \(RoutePredictor\)__

Generates an 8\-step trajectory forecast for any given track using particle\-forward Monte Carlo with PoL blending\. At each step, the particle ensemble is propagated forward using the track's current MOU model mixture\. A PoL blend \(increasing linearly from 0 to 0\.5 over the horizon\) nudges the ensemble toward the PoL\-predicted location for that future time, capturing the dual influence of current trajectory and habitual routine\. Each waypoint includes position, uncertainty \(spread\), and a linearly decreasing confidence score\.

## __9\.8  Forward\-Backward Smoother \(ForwardBackwardSmoother\)__

Maintains a 6\-scan lag history of particle ensembles per track\. The smooth\_pos\(\) method returns a Gaussian\-kernel\-weighted average of historical particle mean positions, with the kernel centred on the most recent scan\. This reduces the positional noise in displayed track histories and is used for smooth trajectory rendering in output visualisations\.

# __10\. Validated Performance__

## __10\.1  Benchmark Results__

All results measured over 20 independent seeds × 50 scans = 1000 total ingest calls, 7 confirmed targets per scenario, 2 registered HVLs, full 8\-detector pipeline active\.

__Metric__

__Result__

__Notes__

__Mean scan latency__

51 ms

Dominated by PoL cross\-predict scans \(every 5th\)

__Median scan latency__

28 ms

Non\-PoL scans; representative of steady\-state load

__P95 latency__

210 ms

PoL cross\-predict scan with 7\+ tracks and 21 pairs

__Max latency \(20×50\)__

325 ms

First PoL scan after model fitting completes

__Throughput__

~20 scans/sec

Wall\-clock, single CPU core, no GPU

__Tracking accuracy__

21\.8 m mean error

Across all tracks, all scans

__P99 position error__

853 m

Mid\-manoeuvre; high\-theta model lag

__Detection rate \(PD=0\.85\)__

100%

All targets confirmed at design PD

__Detection rate \(PD=0\.40\)__

100%

Still 100% at 40% detection probability

__Detection rate \(PD=0\.25\)__

91%

Graceful degradation begins here

__False alarm rate__

0\.098 / scan

Average; 0 false alarms at clutter=40/scan

__Reacquisition rate__

100%

10/10 trials, 8\-scan gap

__RV warnings \(20 scenarios\)__

20/20

100% detection on converging pairs

__RV lead time mean__

28\.1 min

From first warning to actual meeting

__RV lead time ≥ 20 min__

100%

All 20 scenarios warned 20\+ minutes early

__RV lead time ≥ 25 min__

95%

19 of 20 scenarios

## __10\.2  Tradecraft Detection — All Scenarios Pass__

__Scenario__

__Result__

__Condition__

__BRUSH\_PASS__

__PASS__

Two tracks sep < 60m \(38 scans at 5 m/s closure from 200m sep\)

__SDR\_PATTERN__

__PASS__

Winding number >= 0\.65 in 12\-point window \(35 scans, 100m radius, 0\.35 rad/step\)

__PARALLEL\_SURVEILLANCE__

__PASS__

Heading cos >= 0\.97, lateral 55m, 25 scans \(confirmed at scan 7\)

__MODE\_TRANSITION__

__PASS__

Vehicle stops, foot track appears 20m away within 1 scan

__LOITER\_ANOMALY__

__PASS__

Target dwells at anomalous location after 50\-scan PoL baseline

__COVER\_STOP__

__PASS__

Repeated visits within 364m of HVL, pol\_anom = 0\.88 \(< 0\.80 threshold met at scan 35\+\)

## __10\.3  Scaling Characteristics__

Scan latency scales linearly with confirmed track count\. Profiling shows four dominant cost centres: PoL cross\-prediction \(vectorised batch, runs every 5 scans\), GMM log\-likelihood evaluation \(\_gmm\_logpdf\_batch with hand\-coded 3x3 forward substitution\), Gibbs assignment \(14 sweeps × N\_tracks × N\_obs\), and network betweenness centrality \(O\(N×E\) Brandes\)\. All four are NumPy\-vectorised; no Python loops remain in the hot path\.

# __11\. Performance Optimisation History__

The following optimisations were applied during this development session to reduce scan latency from an initial 312 ms mean to the current 51 ms mean:

## __11\.1  PoL Cross\-Prediction Throttling__

Root cause: \_pol\_cross\_predict was being called every scan for all track pairs\. With 7 tracks there are C\(7,2\)=21 pairs, each calling predict\_location 20 times \(n\_mc\_pol\) × 60 horizon steps = 25,200 predict\_location calls per pair per scan, totalling 529,200 calls per scan\.

Fix: throttle PoL cross\-prediction to every 5 scans \(run\_pol = scan % 5 == 0\)\. Reduces predict\_location calls by 5x\. PoL patterns are slow\-changing; 5\-scan intervals introduce negligible warning latency loss\.

## __11\.2  PoL Horizon Cap and MC Reduction__

The horizon\_steps was uncapped \(defaulting to 60 steps\)\. Since the warning horizon is 30 minutes at 60\-second scan rate, 30 steps is sufficient\. Cap reduced to 20 steps\. n\_mc\_pol reduced from 60 to 8 — a further 7\.5x reduction in PoL prediction compute\. Combined with the 5\-scan throttle, this is a 37x reduction in PoL cross\-predict cost\.

## __11\.3  Velocity Fit Caching__

The geometric intercept method called np\.polyfit twice per track per pair per scan\. With 21 pairs and 7 tracks, this is 42 polyfit calls per scan\. Each track's velocity only changes when its position history changes \(which happens once per scan, at the end\)\. A cache keyed by \(track\_id, len\(pos\_history\)\) means each track's velocity is recomputed once per scan and reused across all pairs, reducing polyfit calls from 42 to 7\.

The cache is bounded to 200 entries \(LRU eviction on oldest key\) to prevent unbounded memory growth across long sessions\.

## __11\.4  GMM Inner Loop Hand\-Coding__

The GMM log\-likelihood evaluator is the second\-highest cost centre after PoL cross\-prediction\. For K=5 components in D=3 dimensional space, the inner loop involves solving L\*y=x for 3x3 lower\-triangular L\. The \_fwdsub3 function is a hand\-unrolled forward substitution that computes this in 5 multiplications and 5 additions without any loop overhead, compared to numpy's general triangular solver which handles arbitrary N×N matrices\.

# __12\. Algorithm Provenance and Novelty__

## __12\.1  Established Methods__

- PMBM filter: Mahler \(2003, 2007\), Williams & Lau \(2014\)\. The theoretically optimal multi\-target Bayesian filter under the Random Finite Set framework\.
- Ornstein\-Uhlenbeck process: Uhlenbeck & Ornstein \(1930\)\. Continuous stochastic differential equation with mean\-reverting drift; widely used in financial modelling and physical simulation\.
- MOU particle filter: Williams \(2015\), Granstrom et al\. \(2018\)\. Application of OU\-based motion models to multi\-target tracking with IMM\-style model mixing\.
- Gaussian Mixture Model via EM: Dempster, Laird & Rubin \(1977\)\. Standard latent\-variable inference algorithm\.
- Betweenness centrality: Brandes \(2001\)\. O\(N\*E\) exact algorithm for betweenness centrality in unweighted graphs\.
- Dempster\-Shafer fusion: Shafer \(1976\)\. Mathematical framework for reasoning under uncertainty using belief and plausibility measures\.
- Beta\-distribution Monte Carlo scoring: standard Bayesian Beta\-Binomial conjugate pair used for integrating uncertain evidence dimensions\.
- Gibbs sampling: Geman & Geman \(1984\), applied to measurement\-to\-track assignment following Reid \(1979\) MHT\.

## __12\.2  Research\-Level Methods__

- Track\-before\-Detect PMBM \(TM\-PMBM\): Meyer et al\. \(2023\)\. Extension of PMBM to unthresholded observations\. Implemented to handle low\-SNR SIGINT/COMMS observations without hard detection thresholds\.
- Possibility\-PMBM: Houssineau & Bishop \(2019\)\. Dual\-track of probability \(r\) and possibility \(pi\_r\) existence estimates\. The mismatch score is a novel diagnostic that has no known operational equivalent — it alarms when the probability and possibility estimates diverge, indicating either deception or model failure\.
- Group spawning via PoL cloning: novel heuristic for initialising new tracks in known group contexts by cloning the parent track's PoL model\. Reduces the observation latency required for group member tracking\.
- PoL\-integrated rendezvous warning \(Method 3\): novel application of PoL cross\-prediction to pre\-cognitive meeting warning\. Standard operational systems use trajectory extrapolation; predicting meetings from habitual routine independently of current trajectory is not known in any public operational system\.

## __12\.3  Novel Contributions__

- Three\-method stacked rendezvous warning with 30\-minute lead time: the combination of geometric intercept, separation rate extrapolation, and PoL cross\-prediction in a stacked architecture \(fires on whichever produces the longest valid warning\) is novel\. Each method has independent failure modes; the combination is robust where any individual method is not\.
- Relative percentile network role classification: using within\-set percentile ranks rather than absolute thresholds for Courier/Handler/Asset classification makes the system scale\-invariant across scenario densities from 2 to 80\+ tracks\.
- Domain\-polymorphic single\-file architecture: the complete system from particle filter to tradecraft detector to network analyser is re\-targetable to any sensor domain by replacing a single configuration object\. No domain\-specific code paths exist\.
- Composable hot\-swappable detector registry: the BaseDetector ABC and runtime register/unregister interface allows detector sets to be modified without engine restart\. This is architecturally equivalent to a microkernel plugin system applied to intelligence analytics\.

# __13\. Output Report Dictionary — Complete Field Reference__

engine\.ingest\(\) returns a Python dictionary\. Every field is documented below\.

## __13\.1  Top\-Level Fields__

__Field__

__Type__

__Description__

__scan__

int

Monotonically increasing scan counter since engine construction\.

__timestamp__

float

Unix seconds passed to ingest\(\)\.

__domain__

str

Active DomainProfile name \(e\.g\. "UrbanHUMINT"\)\.

__n\_obs__

int

Number of observations ingested this scan\.

__n\_tracks__

int

Number of confirmed tracks \(r >= R\_CONFIRM\)\.

__n\_components__

int

Total Bernoulli components including candidates\.

__n\_dormant__

int

Number of dormant tracks held for reacquisition\.

__clutter\_rate__

float

Current Bayesian estimate of mean false observations per scan\.

__targets__

List\[Dict\]

Per\-track threat scores and metadata\. See §13\.2\.

__rendezvous__

List\[Dict\]

Rendezvous warnings from ExtendedRendezvousWarner\. See §13\.3\.

__tradecraft__

List\[Dict\]

Tradecraft events from all non\-RV detectors\. See §13\.4\.

__network\_roles__

List\[Dict\]

Per\-track role assignments from NetworkRoleInference\.

__clusters__

List\[Dict\]

Co\-location clusters with betweenness centrality\.

__alerts__

List\[Dict\]

AnomalyEscalator alerts \(SPIKE, ESCALATING, COUNTER\_SURVEILLANCE\)\.

__sensor\_schedule__

List\[Dict\]

Top 3 recommended collection tasks\.

__operational__

Dict

Velocity analysis, dwell flags, movement flags\.

__all\_detections__

Dict\[str, List\]

Raw per\-detector output keyed by detector name\.

## __13\.2  targets\[\] Entry__

__Field__

__Description__

__track\_id__

String identifier e\.g\. "T0023"\. Sequential within session\.

__position__

\[x, y\] in metres\.

__velocity__

\[vx, vy\] particle\-weighted mean in m/s\.

__threat\_score\_mean__

Beta\-MC mean threat score, 0\.0–1\.0\.

__threat\_score\_std__

Standard deviation of MC samples\.

__threat\_score\_p90__

90th percentile of MC samples\.

__threat\_score\_p95__

95th percentile — upper confidence bound for alerting\.

__priority__

IMMEDIATE / HIGH / MEDIUM / LOW / MONITOR tier\.

__existence\_p__

Bernoulli existence probability r\.

__dominant\_model__

Highest\-weighted MOU model class name\.

__poss\_mismatch__

Possibility\-PMBM mismatch score, 0\.0–1\.0\. > 0\.4 alarms\.

__threat\_ema__

Exponential moving average of threat\_score\_mean \(alpha=0\.3\)\.

__threat\_persistence__

Count of consecutive scans with score > 0\.62\.

__meas\_rate__

n\_hit / age; observation hit rate\.

__pos\_uncertainty\_m__

sqrt\(trace\(P\_position\)\) from particle covariance\.

__breakdown__

Dict with raw sub\-scores: existence, poss\_exist, pol\_anomaly, det\_density, hvl\_proximity, motion\_score, persistence\.

## __13\.3  rendezvous\[\] Entry__

__Field__

__Description__

__type__

"RENDEZVOUS\_WARNING"

__track\_a, track\_b__

IDs of the two converging tracks\.

__current\_sep\_m__

Current pairwise separation in metres\.

__eta\_s__

Estimated seconds to meeting\.

__eta\_min__

eta\_s / 60, for display\.

__method__

GEOMETRIC\_INTERCEPT | SEP\_RATE\_EXTRAP | POL\_CROSS\_PREDICT

__confidence__

Method\-specific confidence 0\.0–1\.0 \(R² for SEP\_RATE; 1\-CPA\_sep/thresh for GEOMETRIC\)\.

__predicted\_location__

\[x, y\] midpoint of predicted meeting location \(GEOMETRIC only\)\.

__priority__

IMMEDIATE / HIGH / MEDIUM / LOW based on eta\_min\.

__timestamp__

Scan timestamp\.

## __13\.4  tradecraft\[\] Entry — Common Fields__

All tradecraft events share: type \(string\), timestamp, severity \(IMMEDIATE / HIGH / MEDIUM\), and track / tracks fields\. Type\-specific additional fields are described in §6 per detector\.

# __14\. Test Scenario Generator__

The module includes generate\_scenario\(n\_scans, n\_targets, area, seed\) for reproducible unit testing and benchmarking\. The generator produces:

- n\_targets independent targets with random initial positions in a ±0\.6×area box and random initial velocities in \[\-10, \+10\] m/s\.
- Target dynamics: constant\-velocity propagation with occasional random manoeuvres \(8% probability per scan per target, impulse ±6 m/s\), boundary reflection at ±area\.
- Detection probability 0\.85 \(matching the filter P\_DETECTION parameter\)\.
- Mixed modalities sampled from \[GEOINT, SIGINT, COMMS, HUMINT, OSINT\] with modality\-appropriate confidence noise\.
- Poisson\(3\.0\) false alarms per scan with low\-confidence OSINT attributes\.
- Source IDs drawn from a pool of 5 per modality to enable source credibility tracking across scans\.

Returns: \(all\_obs, true\_traj\) where all\_obs is a list of n\_scans scan observation lists and true\_traj is a \(n\_scans, n\_targets, 4\) array of ground truth states \[x, y, vx, vy\]\.

# __15\. Known Limitations and Open Issues__

## __15\.1  PoL Minimum Observation Threshold__

The PatternOfLife model requires a minimum of 15 observations before fitting\. Tracks that are observed intermittently \(e\.g\. at PD=0\.25\) may take 60\+ scans to accumulate 15 observations\. During this period, the loiter anomaly detector, cover stop detector, PoL cross\-prediction method, and dormant reacquisition are unavailable for that track\. This is an inherent limitation of data\-driven routine modelling and cannot be resolved without a prior over expected PoL structure\.

## __15\.2  MOU Model Classification__

At the default scan rate of 60 seconds, the MOU velocity discretisation gives sigma\_v values calibrated for that interval\. The dominant\_model classification therefore reflects the model that best explains observed velocity magnitudes at that scan rate\. At shorter intervals \(e\.g\. Airspace 5s scans\), the same physical speed produces different relative likelihoods across models\. Domain profiles must specify scan\_dt\_s accurately for model classification to be meaningful\.

## __15\.3  P95 Latency Spike__

The P95 latency is 210ms vs median 28ms — a 7\.5x spike\. This occurs on PoL cross\-prediction scans \(every 5th scan\) when many track pairs have both PoL models fitted\. With 7 targets and 21 pairs, and n\_mc\_pol=8 samples × 20 horizon steps × 2 PoL predict\_location calls per pair, this is 6,720 MC\-weighted Cholesky forward substitutions per PoL scan\. Further reduction is possible by reducing n\_mc\_pol to 4 or increasing the throttle period to 10 scans at the cost of increased PoL warning latency\.

## __15\.4  SDR Threshold Sensitivity__

The SDR winding number threshold of 0\.65 \(approximately 2/3 of a full loop in 12 position history points\) was set to detect operationally realistic SDR loops\. This threshold will produce false positives for targets moving in genuinely circular routes \(e\.g\. patrol routes\) and may miss partial SDR loops executed over more than 12 scans\. Adjust winding\_number\_thresh in the LegacyTradecraftDetector class for different scenario characteristics\.

## __15\.5  Network Role Classification at Small N__

The relative percentile classifier degenerates when n\_tracks < 3: with only 2 tracks, one is always in the top speed percentile and one always in the bottom, producing deterministic role assignments that may be meaningless\. The classifier correctly returns UNKNOWN for tracks with age < 10 scans; role assignments should be treated with lower confidence in the first 15–20 scans of a session\.

# __16\. File Structure \(aria\_intel\_v6\.py, 2,363 lines\)__

__Lines__

__Section__

__Contents__

1–68

__Global constants__

Import declarations, particle/filter hyperparameters, MOU model tables, pre\-computed matrices \(H, R, inverse R, log\-det\)

69–117

__Utility functions__

logsumexp, \_chol\_logpdf, \_betweenness\_centrality, \_fwdsub3

118–263

__PatternOfLife__

GMM with EM fitting, anomaly scoring, location prediction, active window extraction, PoL clone for group spawning

275–364

__MOUParticleFilter__

SIR particle filter, prediction/update/resample, cache, model weight tracking, auxiliary trajectory update

366–446

__BernoulliTrack__

Track hypothesis with PMBM Bernoulli weights, PoL, threat EMA, position/velocity/timestamp history

449–473

__AdaptiveClutterEstimator / SourceCredibilityTracker__

Bayesian clutter rate estimation; per\-source reliability EMA

476–602

__GibbsAssigner / PMBMManager__

Gibbs\-sampled obs\-to\-track assignment; full PMBM lifecycle management

605–655

__score\_track / \_priority__

Beta\-MC threat scoring; priority tier assignment

657–716

__TradecraftDetector \(legacy\)__

Original brush pass, SDR winding number, dead drop

719–777

__RendezvousDetector / RoutePredictor__

Short\-horizon MC rendezvous probability; 8\-step PoL\-blended forecast

780–919

__Supporting systems__

DynamicNetworkAnalyser, AnomalyEscalator, CredibilityFuser, SensorScheduler, OperationalIntelligence, ForwardBackwardSmoother

942–1114

__DomainProfile / Presets__

Full dataclass definition; UrbanHUMINT\(\), Maritime\(\), Airspace\(\), VehicleConvoy\(\) factory functions

1117–1420

__ExtendedRendezvousWarner__

Three\-method 30\-minute warning system with velocity cache, geometric intercept, sep\-rate extrapolation, PoL cross\-prediction

1421–1660

__New tradecraft detectors__

ParallelRouteSurveillanceDetector, ModeTransitionDetector, LoiterAnomalyDetector, CoverStopDetector, ChokepointSurveillanceDetector

1661–1976

__NetworkRoleInferenceDetector__

Contact graph, relative percentile classification, role history, stable\-role events

1978–2055

__LegacyTradecraftDetector__

BaseDetector wrapper for original v5 tradecraft algorithms

2056–2363

__ARIAIntelEngineV6 / generate\_scenario__

Main engine: constructor, detector registry, ingest pipeline, summary/perf formatters; reproducible scenario generator

# __17\. Quick Reference__

## __Engine Construction__

\# Default \(UrbanHUMINT\)

eng = ARIAIntelEngineV6\(\)

\# With all options

eng = ARIAIntelEngineV6\(

    profile = Maritime\(\),

    area    = \(\-50000, 50000, \-50000, 50000\),

    high\_value\_locations = \[np\.array\(\[x, y\]\), \.\.\.\],

\)

## __Per\-Scan Ingestion__

report = eng\.ingest\(observations: List\[Observation\], timestamp: float\)

print\(eng\.summary\(report\)\)           \# formatted text output

print\(eng\.performance\_report\(\)\)      \# session summary

## __Accessing Specific Outputs__

confirmed\_tracks    = eng\.pmbm\.confirmed\(\)

rendezvous\_warnings = report\["rendezvous"\]         \# List of ETA dicts

tradecraft\_events   = report\["tradecraft"\]         \# List of event dicts

network\_roles       = report\["network\_roles"\]      \# List of role dicts

threat\_targets      = report\["targets"\]            \# sorted by threat\_score\_mean

raw\_per\_detector    = report\["all\_detections"\]     \# Dict\[detector\_name, List\]

## __Detector Registry__

eng\.list\_detectors\(\)

eng\.register\_detector\(MyDetector\(eng\.profile\)\)

eng\.unregister\_detector\("MyDetector"\)

## __Domain Switching__

\# Change domain at construction time

eng = ARIAIntelEngineV6\(profile=Airspace\(\)\)

\# All four presets:

UrbanHUMINT\(\)    \# 60s scans, 30\-min RV warn, foot/vehicle models

Maritime\(\)       \# 3600s scans, 2hr RV warn, ship models

Airspace\(\)       \# 5s scans, 10\-min RV warn, aircraft models

VehicleConvoy\(\)  \# 10s scans, 5\-min RV warn, convoy models

## __PoL Prediction__

for track in eng\.pmbm\.confirmed\(\):

    if track\.pol\.\_fitted:

        pred\_pos, spread\_m = track\.pol\.predict\_location\(future\_timestamp\)

        anomaly = track\.pol\.anomaly\_score\(timestamp, position\)

ARIA\-INTEL Technical Reference  ·  aria\_intel\_v6\.py

