<!-- Converted from `README_download.docx` — source was Word (.docx). -->

__download\.py__

Dataset Acquisition & State Management

File 2 of 5  ·  374 lines  ·  Step 1 of the pipeline

For someone reading this for the first time

# __1\. What Is This File?__

download\.py is step one of the pipeline\. It fetches ten publicly available datasets from the internet and saves them to your local directory\. That is the complete scope of what it does — no format conversion, no training, no evaluation\.

You only need to run it once\. After the files are on disk, convert\.py handles the rest\.

python download\.py            \# download all 10 datasets

python download\.py \-\-status   \# check what has been downloaded

python download\.py \-\-retry    \# retry only failed downloads

python download\.py \-\-reset    \# clear state and start fresh

__Where this sits in the pipeline__

download\.py  →  convert\.py  →  benchmark\.py
It produces raw files \(CSV, NPY, ZIP, TAR\.GZ\)\. convert\.py then transforms those into the wire format Cypha reads\.

# __2\. The Ten Datasets__

The ten datasets span three signal domains: text security, URL/phishing classification, and raw signal data \(RF radio and audio\)\. They were chosen to test Cypha's universal encoder across the widest possible range of input types\.

__\#__

__Name__

__Domain__

__Approx size__

__Samples__

__Source__

1

sql\_injection

SQL text

~1\.2 MB

~30k

github: ajinmathew/SQL\-data

2

phishing\_vrbancic

URL features

~18 MB

88k

github: GregaVrbancic/Phishing\-Dataset

3

malware

PE features

~2\.4 MB

~10k

github: mburakergenc/Malware\-Detection

4

network\_intrusion

Net flow

~12 MB

~126k

NSL\-KDD \(defcom17 mirror\)

5

phishing\_emails

Email body

~3\.5 MB

~10k

github: rokibulroni/Phishing\-Email\-Dataset

6

panoradio\_rf

RF signals

~5 GB

~400k

panoradio\-sdr\.de \(HF dataset\)

7

panoradio\_tags

RF labels

<1 MB

—

panoradio\-sdr\.de \(companion CSV\)

8

phiusiil\_phishing

URL features

~8 MB

235k

UCI ML Repository \#967

9

speech\_commands

Audio \(WAV\)

~1\.5 GB

~105k

TensorFlow speech\_commands\_v0\.02

10

esc50

Audio \(WAV\)

~600 MB

2,000

github: karolpiczak/ESC\-50

Total download size is approximately 7–8 GB\. Datasets 6 and 9 \(the RF and speech datasets\) account for most of that\. The small text datasets finish in seconds; the large signal datasets take 10–30 minutes depending on connection speed\.

__Why include RF signals and audio?__

Cypha's universal encoder is designed to classify any 1D signal using the same five mathematical operators\. Including panoradio\_rf \(radio modulation types\) and speech\_commands / esc50 \(audio\) directly tests whether the encoder actually generalises across domains\. A system that only works on text is not universal\.

# __3\. State Machine — Safe to Interrupt__

The most important design property of download\.py is that it is safe to kill at any point and resume without losing progress\. This matters because a 5 GB download over a slow connection might take 20 minutes, and network interruptions happen\.

## __3\.1 The State File__

All progress is tracked in a JSON file called download\_state\.json in the current directory\. It is updated atomically after every completed or failed download\. The schema is:

\{

  "completed": \["sql\_injection", "malware", \.\.\.\],   // list of finished dataset names

  "failed": \{                                         // dict of failed attempts

    "panoradio\_rf": \{

      "error": "Connection timed out",

      "timestamp": "2026\-02\-21 09:15:33"

    \}

  \},

  "in\_progress": "speech\_commands",                  // set at start, cleared on finish

  "downloaded\_files": \{                               // metadata per completed download

    "sql\_injection": \{

      "filename": "sqli\.csv",

      "size\_mb": 1\.23,

      "timestamp": "2026\-02\-21 09:10:05"

    \}

  \}

\}

## __3\.2 State Transitions__

Each dataset follows a simple three\-state lifecycle:

  \(not started\)

       │

       ▼  download function called

  in\_progress  ←─────────────────────────────────────┐

       │                                              │

       ├─ success ──▶  completed  \(skipped on next run\)

       │

       └─ all retries exhausted ──▶  failed

                                         │

                                         └─▶  in\_progress  \(on \-\-retry\)

The in\_progress field is a single string \(not a list\) because downloads are sequential — only one runs at a time\. If the process is killed while in\_progress is set, the next run sees the stale in\_progress entry and re\-downloads that dataset from scratch\.

__Why not resume partially\-downloaded files?__

HTTP partial content \(Range: bytes=X\-\) requires server support and accurate size verification\. For simplicity, download\.py re\-downloads any incomplete file from the start\. Given that the largest file is 5 GB and a partial download takes much less time to verify than to re\-read, this is the correct tradeoff for a tool you run once\.

# __4\. How download\_file\(\) Works__

All ten downloads go through a single download\_file\(url, filename, desc, timeout, max\_retries\) function\. Understanding it helps you diagnose failures\.

## __4\.1 HTTP Request__

The function uses Python's standard library urllib\.request — no third\-party dependencies\. It sets a User\-Agent header mimicking a browser because some servers \(notably the UCI ML Repository\) reject requests without one:

req = urllib\.request\.Request\(url\)

req\.add\_header\("User\-Agent", "Mozilla/5\.0 \(Windows NT 10\.0; Win64; x64\) \.\.\."\)

response = urllib\.request\.urlopen\(req, timeout=timeout\)

## __4\.2 Streaming Download with Progress Bar__

Files are downloaded in 8 KB chunks so memory usage stays constant regardless of file size\. A progress bar is printed to stdout using carriage return \(\\r\) so it overwrites the same line:

while True:

    chunk = response\.read\(8192\)   \# 8 KB at a time

    if not chunk: break

    f\.write\(chunk\)

    downloaded \+= len\(chunk\)

    pct = \(downloaded / total\) \* 100

    bar = "█" \* int\(40 \* downloaded/total\) \+ "░" \* \(40 \- int\(40\*downloaded/total\)\)

    print\(f"  \[\{bar\}\] \{pct:\.1f\}%", end="\\r"\)   \# overwrites same line

This works even when Content\-Length is absent \(some servers omit it\)\. In that case the function reads the entire response into memory before writing, which is fine for all small files in the dataset list\.

## __4\.3 Retry with Exponential Backoff__

If the download fails \(network error, timeout, server error\), it retries up to max\_retries times with exponential backoff plus random jitter:

  wait = 2^attempt \+ Uniform\(0, 2\)   seconds

For three attempts: first retry waits ~2s, second retry waits ~4–6s\. The random jitter prevents multiple simultaneous processes from thundering\-herd a server\.

__Attempt__

__Wait before retry__

__Scenario__

1 \(initial\)

none

First try

2 \(retry 1\)

~2–4 s

Transient network hiccup

3 \(retry 2\)

~4–6 s

Server briefly overloaded

\(give up\)

mark\_failed

Three consecutive failures

## __4\.4 Timeouts__

Two timeout values are used:

- 900 seconds \(15 min\) for most datasets — enough for ~100 MB files on a slow connection\.
- 1800 seconds \(30 min\) for panoradio\_rf \(5 GB\) and speech\_commands \(1\.5 GB\) — explicitly set in their download functions\.

If you are behind a very slow connection and still hitting timeouts, you can manually download the file and place it in the current directory with the expected filename\. The next run will detect it via the size check and skip the download\.

# __5\. Existing File Detection__

Every download function checks whether the file already exists before attempting a download:

if os\.path\.exists\(fn\) and os\.path\.getsize\(fn\) > 1000:

    sz = os\.path\.getsize\(fn\) / \(1024\*1024\)

    print\(f"  Found existing: \{fn\} \(\{sz:\.1f\} MB\)"\)

    mark\_completed\(state, name, fn, sz\)

    return

The size threshold differs by dataset:

- Text datasets \(CSV, ZIP\): threshold is 1,000 bytes — any file over 1 KB is likely valid\.
- Signal datasets \(NPY, TAR\.GZ\): threshold is 1,000,000 bytes \(1 MB\) — guards against partially\-written files from a previous interrupted download\.

This means you can manually place pre\-downloaded files in the directory and download\.py will accept them\. Useful if you are downloading on a different machine and copying over\.

__Note on the panoradio\_rf dataset__

The 5 GB NPY file from panoradio\-sdr\.de is a NumPy float32 array of shape \(N, signal\_length\)\. It is not a CSV — convert\.py handles the format difference by reading it with np\.load\(\) and converting each row to int8 hex\. The companion tags CSV \(panoradio\_tags\) must also be downloaded for the labels\.

# __6\. Dataset Details__

Each dataset is described here with its source, format, labels, and any quirks to be aware of\.

## __6\.1 SQL Injection  \(sql\_injection\)__

CSV with two relevant columns: a query string and a binary label \(0 = safe, 1 = injection\)\. The file uses UTF\-16 encoding with a BOM, which trips up naive CSV readers — convert\.py handles the encoding detection automatically\. About 30,000 samples evenly split between safe queries and injection strings\.

Labels after conversion: safe, sql\_injection\.

## __6\.2 Phishing URLs — Vrbancic  \(phishing\_vrbancic\)__

CSV with 48 engineered URL features \(length ratios, special character counts, domain age, HTTPS flag, etc\.\) plus a binary phishing label\. This is not the raw URL but a pre\-extracted feature vector\. 88,000 samples, moderately imbalanced toward phishing\.

Labels: legitimate, phishing\.

## __6\.3 Malware  \(malware\)__

CSV of Android malware PE features — numeric columns representing file properties, API call counts, and permission flags\. The label column name varies between dataset versions; convert\.py detects it by looking for "label", "class", or "malware" in the column name\.

Labels: benign, malware \(or the raw integer 0/1 which convert\.py maps\)\.

## __6\.4 Network Intrusion — NSL\-KDD  \(network\_intrusion\)__

The classic NSL\-KDD intrusion detection benchmark\. A modified version of KDD Cup 1999 that removes duplicate records\. 41 features per network flow connection: protocol type, service, flag, byte counts, error rates, and more\. The last column is the attack type\.

Labels: normal, anomaly \(convert\.py maps all specific attack types like "neptune", "back", "portsweep" to the single label "anomaly" for binary classification\)\.

## __6\.5 Phishing Emails  \(phishing\_emails\)__

CSV from the SpamAssassin public corpus plus supplemental phishing email bodies\. Contains raw email text\. convert\.py strips HTML tags and truncates to 500 characters before writing to wire format\.

Labels: safe, phishing\.

## __6\.6 Panoradio HF RF  \(panoradio\_rf \+ panoradio\_tags\)__

The largest dataset at ~5 GB\. A NumPy float32 array from the Panoradio SDR project containing HF radio recordings sampled at 12 kHz\. Each row is one signal segment\. The companion tags CSV maps row indices to modulation labels\.

Labels: am, fm, lsb, usb, cw, rtty, and others \(exact set depends on the tag file version\)\.

__Two files required__

panoradio\_rf and panoradio\_tags are two separate downloads that must both complete before convert\.py can process them\. If only one is present, convert\.py will fail with a missing file error\.

## __6\.7 PHIUSIIL Phishing  \(phiusiil\_phishing\)__

235,000 URL samples with 111 engineered features from the UCI Machine Learning Repository\. The dataset is delivered as a ZIP archive\. convert\.py extracts it automatically\. Features include URL length, number of dots, presence of IP address, TLD entropy, and many others\.

Labels: legitimate, phishing\.

## __6\.8 Google Speech Commands  \(speech\_commands\)__

105,000 one\-second WAV files across 35 word classes \("yes", "no", "up", "down", "left", "right", "go", "stop", etc\.\) from the TensorFlow speech\_commands\_v0\.02 dataset\. Delivered as a 1\.5 GB TAR\.GZ archive\. Each WAV is 16 kHz mono PCM\.

Labels: yes, no, up, down, left, right, on, off, go, stop, and 25 others\.

## __6\.9 ESC\-50  \(esc50\)__

2,000 five\-second WAV recordings across 50 environmental sound classes \(dog, rain, chainsaw, helicopter, etc\.\)\. 40 samples per class\. Delivered as a ZIP archive\. Each WAV is 44\.1 kHz stereo PCM; convert\.py converts to mono before encoding\.

Labels: dog, rain, crying\_baby, clock\_tick, helicopter, and 45 others\.

# __7\. Usage Reference__

## __7\.1 Normal run__

cd /your/project/directory

python download\.py

\# Output \(example\):

\#   ====================================================================

\#   COMPLETE DATASET DOWNLOADER \- ALL 10 DATASETS

\#   ====================================================================

\#

\#   ✓ sql\_injection  already downloaded

\#   ✓ malware  already downloaded

\#

\#   ======================================================================

\#     6\. PANORADIO HF RF SIGNALS \(5 GB\)

\#   ======================================================================

\#   Downloading panoradio\_rf \(5 GB, ~10\-20 min\)

\#     URL: http://www\.panoradio\-sdr\.de/\.\.\.

\#     Size: 5120\.0 MB

\#     \[████████████████░░░░░░░░░░░░░░░░░░░░░░░░\] 40\.0% \(2048\.0/5120\.0 MB\)

## __7\.2 Check status__

python download\.py \-\-status

\# Output:

\#   ======================================================================

\#   DOWNLOAD STATUS

\#   ======================================================================

\#

\#   ✅ Completed: 7

\#     ✓ sql\_injection           sqli\.csv              \(1\.2 MB\)

\#     ✓ phishing\_urls\_vrbancic  phishing\_vrbancic\.csv \(17\.8 MB\)

\#     ✓ malware                 malware\.csv           \(2\.4 MB\)

\#     ✓ network\_intrusion       network\_intrusion\.csv \(11\.9 MB\)

\#     ✓ phishing\_emails         phishing\_emails\.csv   \(3\.4 MB\)

\#     ✓ phiusiil\_phishing       phiusiil\_phishing\.zip \(7\.8 MB\)

\#     ✓ esc50                   esc50\.zip             \(598\.1 MB\)

\#

\#   ❌ Failed: 1

\#     ✗ panoradio\_rf  Connection timed out

\#

\#   📊 Success: 7/8 \(87\.5%\)

\#   💾 Downloaded: 643\.6 MB \(0\.63 GB\)

## __7\.3 Retry failed downloads__

python download\.py \-\-retry

\# Only re\-attempts datasets listed in the "failed" dict\.

\# Does not re\-download already\-completed datasets\.

## __7\.4 Reset and start over__

python download\.py \-\-reset

\# Deletes download\_state\.json\.

\# Does NOT delete already\-downloaded files\.

\# The next run will re\-detect them via the size check

\# and mark them completed again without re\-downloading\.

# __8\. Files Produced__

After a successful full run, the following files will be in your current directory:

__Filename__

__Format__

__Size__

__Used by__

sqli\.csv

CSV \(UTF\-16\)

~1\.2 MB

convert\.py → sql\_injection\.txt

phishing\_vrbancic\.csv

CSV

~18 MB

convert\.py → phishing\_vrbancic\.txt

malware\.csv

CSV

~2\.4 MB

convert\.py → malware\.txt

network\_intrusion\.csv

CSV

~12 MB

convert\.py → network\_intrusion\.txt

phishing\_emails\.csv

CSV

~3\.5 MB

convert\.py → phishing\_emails\.txt

dataset\_panoradio\_hf\.npy

NumPy float32

~5 GB

convert\.py → panoradio\_rf\.txt

dataset\_panoradio\_hf\_tags\.csv

CSV

<1 MB

convert\.py → panoradio\_rf\.txt \(labels\)

phiusiil\_phishing\.zip

ZIP → CSV

~8 MB

convert\.py → phiusiil\_phishing\.txt

speech\_commands\.tar\.gz

TAR\.GZ → WAVs

~1\.5 GB

convert\.py → speech\_commands\.txt

esc50\.zip

ZIP → WAVs

~600 MB

convert\.py → esc50\.txt

download\_state\.json

JSON

<1 KB

download\.py internal state

None of these files are read by Cypha\.py directly\. They are all inputs to convert\.py, which transforms them into the wire format \(input|||label per line\) that Cypha reads\.

# __9\. Troubleshooting__

## __9\.1 Connection timeout on panoradio\_rf__

This is the most common failure\. The panoradio\-sdr\.de server is not a high\-bandwidth CDN\. Options:

- Re\-run with \-\-retry and try at a different time of day \(off\-peak hours work better\)\.
- Download the file manually in a browser, save it as dataset\_panoradio\_hf\.npy in the project directory, then run download\.py again — it will detect and skip it\.
- If you do not have the RF dataset, you can still run the benchmark on the other 8 datasets\. benchmark\.py skips any missing \.txt file with a clear error message\.

## __9\.2 UCI ML Repository rejects the request__

The UCI ML Repository \(phiusiil\_phishing\.zip\) occasionally returns 403 Forbidden or redirects to a login page\. This is intermittent\. Solutions:

- Wait and retry\. The repository has rate limits that reset after a few minutes\.
- Download manually from https://archive\.ics\.uci\.edu/dataset/967/ and place the ZIP in the directory\.

## __9\.3 GitHub rate limiting__

GitHub raw content \(used for sql\_injection, phishing\_vrbancic, malware, network\_intrusion, phishing\_emails\) is generally reliable but may occasionally throttle downloads\. The retry logic handles transient 429 errors\. If you are hitting rate limits consistently, wait 60 seconds and re\-run\.

## __9\.4 Disk space__

You need approximately 9–10 GB free for all downloads\. The largest single file is dataset\_panoradio\_hf\.npy at ~5 GB\. After convert\.py runs, the converted \.txt files are a fraction of that size \(the RF dataset compresses significantly in text form\) so you can delete the raw files if space is tight\.

## __9\.5 in\_progress stuck after a crash__

If download\.py is killed during a download, download\_state\.json will have in\_progress set to the dataset name that was downloading\. On the next run this is handled correctly — the in\_progress entry is cleared when the download attempt starts again\. There is no manual intervention required\.

# __10\. Function Reference__

__Function__

__Purpose__

load\_state\(\)

Read download\_state\.json\. Returns empty state dict if file missing or corrupt\.

save\_state\(state\)

Write state dict to download\_state\.json \(pretty\-printed JSON\)\.

mark\_completed\(state, name, fn, sz\)

Add name to completed list, record filename/size/timestamp, clear in\_progress\.

mark\_failed\(state, name, error\)

Add name to failed dict with error string and timestamp, clear in\_progress\.

is\_completed\(state, name\)

Return True if name is in state\["completed"\]\.

show\_status\(state\)

Print formatted status report to stdout\.

download\_file\(url, fn, \.\.\.\)

Streaming download with progress bar, retry, and backoff\. Returns \(success, size\_mb\)\.

download\_sql\_injection\(state\)

Download sqli\.csv\. Skips if size > 1 KB\.

download\_phishing\_urls\_vrbancic\(state\)

Download phishing\_vrbancic\.csv\. Skips if size > 1 KB\.

download\_malware\(state\)

Download malware\.csv\. Skips if size > 1 KB\.

download\_network\_intrusion\(state\)

Download network\_intrusion\.csv\. Skips if size > 1 KB\.

download\_phishing\_emails\(state\)

Download phishing\_emails\.csv\. Skips if size > 1 KB\.

download\_panoradio\_rf\(state\)

Download 5 GB NPY file\. Timeout=1800s\. Skips if size > 1 MB\.

download\_panoradio\_tags\(state\)

Download companion labels CSV\. Skips if size > 1 KB\.

download\_phiusiil\(state\)

Download UCI phishing ZIP\. Skips if size > 1 MB\.

download\_speech\_commands\(state\)

Download 1\.5 GB TAR\.GZ\. Timeout=1800s\. Skips if size > 1 MB\.

download\_esc50\(state\)

Download ESC\-50 ZIP\. Skips if size > 1 MB\.

main\(\)

Entry point\. Parses \-\-status, \-\-reset, \-\-retry flags\. Runs all download functions\.

End of download\.py reference\.  Next: convert\.py

