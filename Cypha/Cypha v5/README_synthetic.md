<!-- Converted from `README_synthetic.docx` — source was Word (.docx). -->

__synthetic\_benchmark\.py__

Self\-Contained Correctness Test — No Downloads Required

File 5 of 5  ·  784 lines  ·  Run this first

For someone reading this for the first time

# __1\. What Is This File?__

synthetic\_benchmark\.py is a completely self\-contained test of the Cypha system\. It generates its own data, trains on it, and evaluates accuracy — without requiring any downloaded files, any network access, or any dependencies beyond NumPy\.

__Run this first__

If you just cloned the repository, run this before anything else:

    pip install numpy
    python synthetic\_benchmark\.py \-\-quick

If it completes without errors and prints ~80%\+ accuracy across all domains, your installation is working correctly and you can proceed to download\.py → convert\.py → benchmark\.py\.

The file covers all nine domains from the real benchmark:

__Domain__

__Signal type__

__Classes__

__Generator__

sql\_injection

Text

2 \(safe / sql\_injection\)

gen\_sql\_injection\(\)

phishing\_urls

Text

2 \(legitimate / phishing\)

gen\_phishing\_urls\(\)

malware

Text

2 \(benign / malware\)

gen\_malware\(\)

network\_intrusion

Text

2 \(normal / anomaly\)

gen\_network\_intrusion\(\)

phishing\_emails

Text

2 \(safe / phishing\)

gen\_phishing\_emails\(\)

phiusiil\_phishing

Text

2 \(legitimate / phishing\)

gen\_phiusiil\_phishing\(\)

panoradio\_rf

IQ hex

6 \(AM/FM/BPSK/QPSK/USB/CW\)

gen\_panoradio\_rf\(\)

speech\_commands

PCM hex

10 \(yes/no/go/stop/\.\.\.\)

gen\_speech\_commands\(\)

esc50

PCM hex

10 \(dog\_bark/rain/\.\.\.\)

gen\_esc50\(\)

## __1\.1 Two Modes__

python synthetic\_benchmark\.py           \# Full: 500 samples × 9 domains × 3 epochs \(~10 min\)

python synthetic\_benchmark\.py \-\-quick   \# Quick: 50 samples × 9 domains × 1 epoch  \(~2 min\)

python synthetic\_benchmark\.py \-\-verbose \# Show infer\(\) output for every test sample

The \-\-quick mode is suitable for CI/CD pipelines, verifying a code change, or just confirming the system runs\. The full mode produces results comparable to the production benchmark on real data\.

Each domain runs in complete isolation — a fresh CyphaStateful instance per domain, written to a temp directory that is deleted after evaluation\. There is no cross\-domain contamination\.

# __2\. Text Domain Generators__

The six text generators each produce \(input\_string, label\_string\) pairs in the Cypha wire format\. Every generator uses a fixed random seed \(numpy default\_rng\(42\)\) so results are fully reproducible across runs\.

The design principle for all text generators: the two classes must have clearly different Omega signatures, especially κ\(D\(x\)\) — the kurtosis of the first difference of the byte sequence\. This is the primary discriminator used by the Omega encoder, and all generators are explicitly designed to produce distributions that differ on it\.

## __2\.1  gen\_sql\_injection__

Alternates between safe SQL queries built from templates and known SQL injection strings:

\# Safe — smooth byte transitions, low κ\(D\)

SELECT name FROM users WHERE id = 42

UPDATE settings SET theme = 'dark' WHERE uid = 17

\# Injection — sudden ASCII jumps: 39→32→79→82 \(apostrophe→space→O→R\)

' OR 1=1 \-\-

' UNION SELECT username, password FROM admin \-\-

'; EXEC xp\_cmdshell\('dir'\) \-\-

The injection strings contain sudden large ASCII value jumps \(apostrophe=39, space=32, O=79, R=82, 1=49, equals=61\) that produce high kurtosis in the first\-difference sequence\. Safe queries have smoother alphanumeric transitions with lower burstiness\.

Expected κ\(D\): safe ≈ −0\.5 to \+1\.5  |  injection ≈ \+3\.0 to \+8\.0\.

## __2\.2  gen\_phishing\_urls__

Generates real\-looking legitimate URLs vs phishing URLs using common evasion patterns:

\# Legitimate — short, clean domain, HTTPS

https://google\.com/search

https://stackoverflow\.com

\# Phishing — brand name in subdomain, suspicious TLD, IP address, hex

http://google\.com\.login\.7842\.ru/secure

http://192\.168\.47\.193/admin/login

http://secure\-login\.4521\.xyz/account

http://signin\.ebay\.com\.3847\.info/login

Phishing URLs typically have more dots \(subdomains\), longer paths, suspicious TLDs \(\.tk, \.ml, \.xyz, \.ru\), and often contain brand names within subdomain components rather than the primary domain\. These differences are captured by the URL length ratio and special\-character density features in the Omega encoder\.

## __2\.3  gen\_malware__

Generates PE feature strings for benign executables vs malware, based on entropy, API call lists, and obfuscation markers:

\# Benign — low entropy, standard APIs, 3 sections

entropy:4\.21 size:245760 imports:ReadFile WriteFile RegOpenKeyEx CloseHandle sections:3 packed:0

\# Malware — high entropy \(packed/encrypted\), injection APIs, 7 sections

entropy:7\.43 size:18432 imports:VirtualAlloc WriteProcessMemory CreateRemoteThread URLDownloadToFile sections:7 packed:1 suspicious\_strings:1 obfuscated:1

Key discriminators: entropy \(benign: 3\.0–5\.5, malware: 6\.5–8\.0\), packed flag, and API names like VirtualAlloc and CreateRemoteThread which are hallmarks of process injection\.

The Omega encoder treats these as byte sequences, so the byte\-level fingerprint of "entropy:7\.43" vs "entropy:4\.21" contributes to M\(D\(x\)\) via the digit transitions, while the API names produce bigram patterns that distinguish malware from benign\.

## __2\.4  gen\_network\_intrusion__

Generates KDD\-style flow feature strings for normal traffic vs attacks:

\# Normal — standard service, moderate byte counts, SF \(normal\) flag

f0:1\.25 f1:tcp f2:http f3:SF f4:2341 f5:4820 f6:0 f7:0 f8:0 f9:0 f10:0 f11:0 f12:1 f13:0

\# Anomaly \(syn\_flood\) — zero duration, zero dst bytes, S0 flag

f0:0\.00 f1:tcp f2:private f3:S0 f4:47 f5:0 f6:1 f7:1 f8:511 f9:511 f10:1 f11:347 f12:0 f13:1

\# Anomaly \(data\_exfil\) — very large src bytes

f0:0\.21 f1:tcp f2:other f3:S0 f4:387421 f5:14930 f6:1 f7:1 f8:511 f9:511 f10:1 f11:203 f12:0 f13:1

Four attack types are generated: syn\_flood \(zero dst bytes, f5=0, S0 flag\), port\_scan \(short duration, many connections\), data\_exfil \(massive src byte count\), and brute\_force \(many failed connections\)\. All are labelled "anomaly", matching the binary\-classification approach in the real benchmark\.

## __2\.5  gen\_phishing\_emails__

Generates short email body strings for safe business emails vs urgent phishing messages:

\# Safe — neutral tone, reference number, professional language

Hi Sarah, your invoice \#47821 is attached\. Please review and let us know if you have questions\. Best regards, Accounts Team\.

\# Phishing — URGENT ALL\-CAPS, suspicious URL, threat language

URGENT: Your account has been suspended\! Click here immediately to verify your identity and restore access: http://secure\-login\-3847\.tk/verify

The all\-caps URGENT token produces a distinctive ASCII burst pattern — "URGENT" has byte values 85,82,71,69,78,84 \(all uppercase, 65–90 range\) followed by a colon at 58, producing large derivatives in D\(x\)\. Safe emails have gentler case transitions\. The exclamation mark \(33\) and URL at the end also create signature derivative spikes\.

## __2\.6  gen\_phiusiil\_phishing__

A richer URL generation than gen\_phishing\_urls, covering four phishing construction styles:

\# Style 0 — brand name \+ random number \+ suspicious TLD \+ /verify/account path

http://paypal\-secure\-6321\.xyz/verify/account

\# Style 1 — raw IP address with brand name in query string

http://192\.168\.73\.41/admin/login?redirect=paypal

\# Style 2 — long subdomain chain impersonating brand \(subdomain abuse\)

http://secure\.amazon\.com\.login\.update\.verify842\.ml/account/confirm

\# Style 3 — URL shortener with "secure\-login" path

http://bit\.ly/94821/secure\-login

The style variety ensures Cypha must learn a general phishing signature rather than a single pattern\. The Omega encoder sees each URL as a byte sequence, so IP address patterns \(digit\-dot\-digit sequences\), excessive subdomain depth \(many dots\), and suspicious TLD byte patterns all contribute to M\(D\(x\)\)\.

# __3\. RF Signal Generator — gen\_panoradio\_rf__

This is the most mathematically involved generator\. It synthesises six radio modulation types from first principles, ensuring each has a distinct power spectral density \(PSD\) that the Omega encoder can discriminate\.

## __3\.1 Setup__

All modulations use integer sample indices as the time axis — not normalised 0\-to\-1 linspace\. This was a critical fix from an earlier version:

\# WRONG \(old\): carriers at fc=0\.05\-0\.45 all landed near DC bin 0\-2

t = np\.linspace\(0, 1, n\_samples\)

\# CORRECT: integer sample indices → carrier at fc cycles/sample occupies

\# bin floor\(fc \* n\_samples\) in the FFT → well\-separated peaks

t = np\.arange\(n\_samples, dtype=np\.float64\)

With n\_samples=512 and fc in cycles/sample, the carrier occupies FFT bin round\(fc \* 512\)\. Each modulation is assigned a different fc so their PSD peaks fall in different frequency bins\.

## __3\.2 Per\-Modulation Mathematical Design__

### __AM — Amplitude Modulation__

  s\_AM\(t\)  =  \(1 \+ 0\.8·cos\(2π·f\_m·t\)\) · exp\(i·2π·fc·t\)    fc = 0\.08

The message frequency f\_m = 1/50 cycles/sample\. The envelope \(1 \+ 0\.8·msg\) amplitude\-modulates the carrier\. This produces three PSD peaks: carrier at fc, and two sidebands at fc ± f\_m\. The envelope variation creates high amplitude std\.

### __FM — Frequency Modulation__

  φ\(t\)  =  2π·\(fc·t \+ dev·Σᵢ₌₀ᵗ msg\[i\]\)    dev = 0\.04,  fc = 0\.15

  s\_FM\(t\)  =  exp\(i·φ\(t\)\)

The cumulative sum of msg gives the instantaneous phase deviation\. The result is a signal with constant amplitude \(|s\_FM| = 1\) but time\-varying instantaneous frequency\. The PSD is wider than AM \(Carson's rule: bandwidth ≈ 2\(dev \+ f\_m\)·fs\)\. Amplitude std is near zero; instantaneous frequency std is high\.

### __BPSK — Binary Phase Shift Keying__

  chips\[k·sl:\(k\+1\)·sl\]  =  2·bit\_k − 1   ∈ \{−1, \+1\}    sl = 8  samples/symbol

  s\_BPSK\(t\)  =  chips\[t\] · exp\(i·2π·0\.20·t\)

8 samples per symbol \(64 symbols over 512 samples\) means the symbol transitions are slow — the PSD shows narrow sinc\-shaped lobes centred at fc=0\.20 with null bandwidth 2/sl = 0\.25 cycles/sample\. The bits alternate in blocks to guarantee phase transitions\. The phase at each sample is either 0 or π \(cos\(phase\)² ≈ \+1 — the BPSK signature\)\.

### __QPSK — Quadrature Phase Shift Keying__

  s\_QPSK\(t\)  =  \(c\_I·cos\(2π·0\.28·t\) − c\_Q·sin\(2π·0\.28·t\)\) / √2

4 samples per symbol \(128 symbols over 512 samples\) — four times more transitions than BPSK, producing a much wider PSD centred at fc=0\.28\. The four constellation points are at phase angles \{0, π/2, π, 3π/2\}, meaning cos\(2Δφ\) averages to near 0 rather than \+1 as in BPSK\. This distinguishes QPSK from BPSK in the Omega M\(D\(x\)\) features\.

### __USB — Upper Sideband Single Sideband__

True USB SSB is constructed via the analytic signal method to guarantee a one\-sided PSD:

  MSG\_FFT\[n/2 :\] = 0          \(zero negative\-frequency bins\)

  MSG\_FFT\[1:n/2\] \*= 2         \(double positive\-frequency bins — preserve power\)

  s\_a = IFFT\(MSG\_FFT\)          \(complex analytic signal\)

  s\_USB\(t\) = s\_a\(t\) · exp\(i·2π·0\.35·t\)

This places all spectral energy at fc \+ f\_m \(the upper sideband\) with zero energy at fc − f\_m \(the lower sideband is suppressed\)\. The resulting PSD is asymmetric — a distinguishing feature the Omega encoder captures via the asymmetry between frequency band energies\.

### __CW — Continuous Wave__

  s\_CW\(t\)  =  exp\(i·2π·0\.22·t\)

A pure unmodulated carrier\. No envelope variation\. No phase transitions\. The PSD is a near\-perfect delta spike at fc=0\.22\. κ\(D\(x\)\) is near zero \(the derivative of a pure sinusoid has near\-constant amplitude\)\. Amplitude variance is zero\. This is the easiest class to classify\.

## __3\.3 Carrier Phase Randomisation and Noise__

Every generated sample gets a random carrier phase rotation:

  r\_eid·I \+ i·Q  ←  \(I \+ iQ\) · exp\(i·φ\)      φ ~ Uniform\(0, 2π\)

And AWGN is added at 30–40 dB SNR:

  noise\_std  =  10^\{−SNR\_dB / 20\}

The random phase ensures the encoder cannot use absolute phase position — it must rely on the PSD envelope shape and modulation statistics\. This validates that the phase\-invariant features \(amplitude statistics, spectral band energy\) are doing the work\. The 30–40 dB SNR means the noise is detectable but does not obscure the modulation signature\.

## __3\.4 IQ Encoding__

The generated complex signal is converted to int8 hex using the same format as the real panoradio\_rf dataset \(see convert\.py §4\.6\):

  scale  =  max\(|Re|, |Im|\) \+ ε

  I\_i8  =  clip\(Re / scale × 110, −127, 127\)  ∈  int8

  Q\_i8  =  clip\(Im / scale × 110, −127, 127\)  ∈  int8

  wire  =  interleave\(I\_i8, Q\_i8\)  then  \.hex\(\)  →  "iq:HEXHEX\.\.\."

# __4\. Audio Domain Generators__

Both audio generators use the same approach: assign each class a pure sine tone at a specific mel\-filterbank center frequency, ensuring maximum separation in the mel\-feature space\. This is a simplification from realistic speech/sound generation, but it fully exercises the PCM encoder path\.

## __4\.1 The Mel Filterbank and Frequency Assignment Strategy__

The Cypha PCM encoder uses 26 mel\-scale frequency bands over the range 80–4000 Hz at sr=16000 Hz\. The mel scale is:

  mel\(f\)  =  2595 · log₁₀\(1 \+ f / 700\)

Two classes assigned to adjacent mel bands will produce overlapping triangular filter responses \(neighbouring mel filters share boundaries\)\. To avoid this, each class is assigned a frequency at the center of every 2nd or 3rd mel band — giving zero filter overlap between adjacent classes\.

The speech and ESC\-50 generators use different sets of band assignments so there is no frequency collision between the two domains\.

## __4\.2  gen\_speech\_commands — Ten Word Classes__

__Word__

__Frequency \(Hz\)__

__Mel band__

__Notes__

yes

165 Hz

band 1

Sub\-bass

no

293 Hz

band 3

Bass

go

522 Hz

band 6

Low\-mid

stop

803 Hz

band 9

Mid

left

1150 Hz

band 12

Upper\-mid

right

1576 Hz

band 15

Presence

up

2100 Hz

band 18

Brilliance

down

2744 Hz

band 21

High

on

3255 Hz

band 23

Very high

off

3840 Hz

band 25

Near Nyquist

Each word generates a pure sinusoid at the assigned frequency, duration 500 ms at 16000 Hz = 8000 samples\. A tiny amount of white noise \(σ = 0\.005\) is added to prevent exact repetition\. The signal is then quantised to int16 PCM and hex\-encoded:

  sig\(t\)  =  sin\(2π·f₀·t\) \+ 0\.005·ε\(t\)      ε ~ N\(0,1\)

  pcm\[t\]  =  clip\(sig\[t\] · 32767, −32768, 32767\)  ∈  int16

  wire    =  pcm\.tobytes\(\)\.hex\(\)  →  "pcm:HEXHEX\.\.\."

## __4\.3  gen\_esc50 — Ten Environmental Sound Classes__

__Category__

__Frequency \(Hz\)__

__Mel band__

__Notes__

dog\_bark

108 Hz

band 0

Very sub\-bass — distinct from speech range

rain

228 Hz

band 4/5

Low bass

engine

408 Hz

band 7

Low\-mid

clock\_tick

660 Hz

band 10

Mid

thunderstorm

975 Hz

band 13

Upper\-mid

siren

1360 Hz

band 16

Presence

footsteps

1850 Hz

band 19

Brilliance

wind

2450 Hz

band 22

High

helicopter

3060 Hz

band 24

Very high

keyboard\_typing

3980 Hz

band 26

Near Nyquist

ESC\-50 uses duration 1000 ms \(16000 samples\) vs speech's 500 ms to reflect the longer duration of environmental sounds\. The band assignments are offset from speech so the two audio domains do not conflict if ever run in a multi\-domain setting\.

__Why pure tones instead of realistic sound synthesis?__

The goal is not to simulate realistic audio\. It is to verify that the PCM encoder \(mel filterbank → Omega\) correctly discriminates distinct frequency fingerprints\. Pure tones are the worst\-case test: if the encoder cannot distinguish ten tones at different mel\-band frequencies, it cannot classify real audio\. In practice, the real ESC\-50 and speech benchmark accuracy is lower than synthetic because real sounds are complex and variable — the synthetic test sets a correctness floor\.

# __5\. The Benchmark Engine__

All nine domains run through a common benchmark engine in run\_domain\(\)\. This ensures a fair, consistent evaluation methodology across text, RF, and audio domains\.

## __5\.1 Isolation Design__

Each domain gets:

- A fresh CyphaStateful instance \(feature\_dim=4096, resonance\_dim=256\) — no memory of previous domains\.
- A fresh temp directory for the wire\-format \.txt file and the checkpoint directory\.
- The temp directory is deleted with shutil\.rmtree\(\) after evaluation — no disk accumulation\.

tmp\_dir  = tempfile\.mkdtemp\(prefix="cypha\_synth\_"\)

tmp\_file = os\.path\.join\(tmp\_dir, f"\{name\}\.txt"\)

ckpt\_dir = os\.path\.join\(tmp\_dir, "checkpoints"\)

cypha = CyphaStateful\(feature\_dim=4096, resonance\_dim=256,

                      checkpoint\_root=ckpt\_dir\)

\# \.\.\. train and evaluate \.\.\.

shutil\.rmtree\(tmp\_dir, ignore\_errors=True\)   \# clean up

## __5\.2 80/20 Split via Byte\-Offset Index__

The same streaming approach as benchmark\.py — the wire\-format file is indexed to an offset array, then split 80/20 by position:

offsets   = \_build\_offset\_index\(tmp\_file\)

split     = int\(len\(offsets\) \* 0\.8\)

train\_off = offsets\[:split\]

test\_off  = offsets\[split:\]

## __5\.3 Per\-Class Accuracy Breakdown__

Unlike benchmark\.py which only reports overall accuracy, run\_domain\(\) tracks correct and total counts per class and prints a per\-class bar chart:

\# Example output for panoradio\_rf:

  Per\-class:

    AM          ████████░░  40/50  \( 80\.0%\)

    BPSK        ██████████  50/50  \(100\.0%\)

    CW          ██████████  50/50  \(100\.0%\)

    FM          ████████░░  41/50  \( 82\.0%\)

    QPSK        ████████░░  39/50  \( 78\.0%\)

    USB         ████████░░  42/50  \( 84\.0%\)

The bar chart uses ░ \(empty\) and █ \(filled\) at 10% increments\. This immediately shows which classes the model is struggling with\. In the RF domain, AM and QPSK are typically the weakest because their PSDs can partially overlap\.

## __5\.4 Omega Signature Measurement__

run\_domain\(\) computes κ\(D\(x\)\) for up to 100 test samples and reports the mean:

  κ\_D\(s\)  =  excess\_kurtosis\( D\( bytes\(s\) \) \)

This is the same \_kappa\_d\(\) function shown in the synthetic benchmark source\. It measures how bursty the byte\-level derivative is for each input\. The benchmark prints:

  Omega κ\(D\): 4\.83  \(bursty\)     \# high = SQL injections, malware, RF signals

  Omega κ\(D\): 0\.21  \(smooth\)     \# low  = regular email text, URLs

This is a direct readout of how much discriminative signal the Omega operator is likely to find\. High κ\(D\) means there is strong burstiness structure for the encoder to exploit\. Low κ\(D\) means the model must rely more on the spectral and autocorrelation features\.

# __6\. Expected Output__

## __6\.1 \-\-quick Mode \(50 samples, 1 epoch, ~2 min\)__

══════════════════════════════════════════════════════════════════════

  CYPHA HRNA — SYNTHETIC BENCHMARK

  50 examples × 9 domains  |  Omega\-2 encoder  |  Pure numpy

  Mode: QUICK \(50 samples, 1 epoch\)

══════════════════════════════════════════════════════════════════════

  Generating 50 synthetic sql\_injection samples \(text\)\.\.\.

  Generated in 0\.00s

══════════════════════════════════════════════════════════════════════

  DOMAIN: SQL\_INJECTION

══════════════════════════════════════════════════════════════════════

  Total pairs: 50  |  Train: 40  |  Test: 10

  Training \(1 epoch\(s\)\)\.\.\.

  ═══════════════════════════════════════════════

    Epoch 1/1

    Loss:    0\.0421   Meta\-L: 0\.0312

    Anchors: 38 \(0→38, \-0 merged\)  Steps: 40

    \.\.\.

  Training: 0\.2s

  Evaluating 10 test samples\.\.\.

  ─── Results ────────────────────────────────────────

  Accuracy:   90\.0%  \(9/10\)

  Eval time:  0\.1s  \(10 ms/sample\)

  Omega κ\(D\): 3\.42  \(bursty\)

  Per\-class:

    safe           █████████░  4/5   \( 80\.0%\)

    sql\_injection  ██████████  5/5   \(100\.0%\)

## __6\.2 Final Summary__

══════════════════════════════════════════════════════════════════════

  SYNTHETIC BENCHMARK — FINAL SUMMARY

══════════════════════════════════════════════════════════════════════

  Domain                      Accuracy   Samples    κ\(D\)   Classes

  ─────────────────────────────────────────────────────────────────

  ── Cybersecurity \(Text\) ──

  sql\_injection               100\.0%        500    4\.83       2

  phishing\_urls               100\.0%        500    0\.18       2

  malware                     100\.0%        500    0\.24       2

  network\_intrusion            90\.0%        500    0\.31       2

  phishing\_emails             100\.0%        500    0\.14       2

  phiusiil\_phishing            96\.0%        500    0\.19       2

  Category mean               97\.7%

  ── RF Signals ──

  panoradio\_rf                 85\.3%        500    0\.08       6

  Category mean                85\.3%

  ── Audio ──

  speech\_commands              90\.0%        500    0\.01      10

  esc50                        92\.0%        500    0\.01      10

  Category mean                91\.0%

  ─────────────────────────────────────────────────────────────────

  OVERALL                      93\.3%      4,500

  Best:   sql\_injection \(100\.0%\)

  Worst:  panoradio\_rf  \(85\.3%\)

  Total time:   312\.4s

  Encoder:      Omega\-2  \[M\(x\), M\(D\(x\)\), M\(D²\(x\)\), R\(x,K\), A\(x,lags\)\] × 3 scales

  κ\(D\) theory:  linearly encodes string attractor density γ\*/n \(r=0\.9985\)

  Zero external dependencies\. Self\-contained synthetic generation\.

══════════════════════════════════════════════════════════════════════

__What counts as a pass?__

If overall accuracy is above 80% and no domain shows 0% \(which would indicate an encoder routing bug\), the system is working correctly\. RF signals typically show the lowest accuracy in synthetic mode \(85–90%\) because six modulation classes are more difficult to separate than two\. Text domains typically achieve 90–100%\.  Accuracy below 70% on any text domain usually indicates an encoding path problem\.

# __7\. How Synthetic Results Relate to the Real Benchmark__

Synthetic results are systematically higher than real benchmark results\. This is expected and by design\.

__Domain__

__Synthetic \(typical\)__

__Real benchmark \(typical\)__

__Gap and reason__

sql\_injection

95–100%

88–94%

Real injections are more varied in structure and character set

phishing\_urls

95–100%

82–90%

Real URLs use many more patterns and encoding tricks

malware

95–100%

85–92%

Real PE features include more edge cases and obfuscation variants

network\_intrusion

85–95%

75–85%

Real KDD\-99 has correlated features that confuse simple classifiers

phishing\_emails

95–100%

84–90%

Real phishing emails are often subtle; synthetic uses obvious urgency cues

panoradio\_rf

80–90%

78–86%

Real HF radio has multipath fading, adjacent\-channel interference, and noise at variable SNR

speech\_commands

85–95%

68–76%

Real speech has speaker variability, room acoustics, recording artefacts

esc50

88–95%

62–72%

Real environmental sounds are highly variable; synthetic is single pure tones

The gap is largest for audio domains because real speech and environmental sounds have far more within\-class variability than pure sine waves\. The synthetic test exercises the encoder path but cannot replicate the difficulty of acoustic variation\.

# __8\. Function Reference__

__Function__

__Returns__

__Purpose__

gen\_sql\_injection\(n\)

List\[\(str,str\)\]

Safe SQL queries vs injection strings\. n/2 each\.

gen\_phishing\_urls\(n\)

List\[\(str,str\)\]

HTTPS legitimate URLs vs HTTP phishing URLs with 4 evasion styles\.

gen\_malware\(n\)

List\[\(str,str\)\]

Benign PE feature strings \(low entropy\) vs malware \(high entropy, injection APIs\)\.

gen\_network\_intrusion\(n\)

List\[\(str,str\)\]

KDD\-style flow features: normal TCP services vs 4 attack types\.

gen\_phishing\_emails\(n\)

List\[\(str,str\)\]

Business email bodies vs URGENT phishing with URL\.

gen\_phiusiil\_phishing\(n\)

List\[\(str,str\)\]

Rich URL generation with 4 phishing construction styles\.

\_rf\_signal\_hex\(mod, n\)

str

Core RF synthesiser: generates int8 IQ hex for one modulation class\.

gen\_panoradio\_rf\(n\)

List\[\(str,str\)\]

6 RF classes \(AM/FM/BPSK/QPSK/USB/CW\), balanced n/6 each\.

\_fft\_bandpass\(noise, lo, hi, sr\)

ndarray

Ideal FFT\-domain bandpass filter \(used in earlier speech design\)\.

\_speech\_hex\(word, sr, ms\)

str

Pure sine tone for one word class, hex\-encoded int16 PCM\.

gen\_speech\_commands\(n\)

List\[\(str,str\)\]

10 word classes at mel\-band\-spaced frequencies\.

\_env\_sound\_hex\(cat, sr, ms\)

str

Pure sine tone for one environmental sound class, hex\-encoded\.

gen\_esc50\(n\)

List\[\(str,str\)\]

10 sound classes at mel\-band\-spaced frequencies\.

\_kappa\_d\(text\)

float

κ\(D\(bytes\(text\)\)\): burstiness diagnostic for the Omega encoder\.

run\_domain\(name, pairs, epochs, verbose\)

dict

Full train\+eval cycle for one domain\. Temp dir per domain\.

main\(\)

—

Entry point: runs all 9 domains, prints summary, saves JSON report\.

# __9\. Output Report__

synthetic\_benchmark\.py saves a detailed JSON report to synthetic\_benchmark\_report\.json after every run:

\{

  "benchmark":    "synthetic",

  "n\_per\_domain": 500,

  "epochs":       3,

  "timestamp":    "2026\-02\-21 09:00:00",

  "total\_time\_s": 312\.4,

  "overall\_mean": 93\.3,

  "domains": \{

    "sql\_injection": \{

      "domain":        "sql\_injection",

      "n\_samples":     500,

      "n\_train":       400,

      "n\_test":        100,

      "accuracy":      100\.0,

      "correct":       100,

      "epochs":        3,

      "train\_time\_s":  1\.92,

      "eval\_time\_s":   0\.48,

      "omega\_kd\_mean": 4\.83,

      "omega\_kd\_std":  2\.10,

      "n\_classes":     2,

      "classes":       \["safe", "sql\_injection"\],

      "per\_class\_acc": \{ "safe": 100\.0, "sql\_injection": 100\.0 \},

      "errors":        \[\]

    \},

    "panoradio\_rf": \{ \.\.\. \},

    \.\.\.

  \}

\}

This file is overwritten on each run\. Compare runs by saving copies with different names, e\.g\. synthetic\_baseline\.json before making a code change and synthetic\_after\_fix\.json after\.

__End of synthetic\_benchmark\.py reference\.  All 5 files documented\.__

