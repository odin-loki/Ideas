<!-- Converted from `README_convert.docx` — source was Word (.docx). -->

__convert\.py__

Dataset Format Conversion & Wire Format Specification

File 3 of 5  ·  600 lines  ·  Step 2 of the pipeline

For someone reading this for the first time

# __1\. What Is This File?__

convert\.py is step two of the pipeline\. It reads every raw dataset file downloaded by download\.py and transforms it into Cypha wire format — a plain text file where every line is exactly one training sample:

  input\_string  |||  label\_string

That is the only format Cypha\.py reads\. The triple\-pipe delimiter \(|||\) was chosen because it does not appear in any of the input domains: SQL queries, URLs, PE feature vectors, network flows, email text, RF hex strings, and audio hex strings all use different characters but none of them use three consecutive pipe characters\.

__Where this sits in the pipeline__

download\.py  →  convert\.py  →  benchmark\.py
Reads 10 raw files \(CSV, NPY, ZIP, TAR\.GZ\)\. Writes 9 wire\-format \.txt files\. benchmark\.py reads those \.txt files directly\.

python convert\.py            \# convert all datasets

python convert\.py \-\-status   \# check conversion progress

python convert\.py \-\-retry    \# retry any failures

python convert\.py \-\-reset    \# clear state, re\-detect from scratch

# __2\. The Wire Format__

Understanding the wire format is the key to understanding the whole pipeline\. Once you grasp what each line looks like and why, everything else follows\.

## __2\.1 Basic Structure__

Every line in every output file has exactly the same structure:

  INPUT\_STRING  |||  LABEL\_STRING

There is no header row\. There are no quotes\. Every newline is a new sample\. The input string can be arbitrarily long and contain any characters except newline and |||\. The label string is a short identifier with no spaces\.

\# Example lines from sql\_injection\.txt:

SELECT id FROM users WHERE active=1|||safe

' OR 1=1 \-\-|||sql\_injection

SELECT email FROM accounts WHERE user='alice'|||safe

1; DROP TABLE users \-\-|||sql\_injection

\# Example lines from panoradio\_rf\.txt:

iq:1a2b3c4d5e6f\.\.\.8192 bytes of hex\.\.\.|||am

iq:ff01fe02fd03\.\.\.8192 bytes of hex\.\.\.|||fm

\# Example lines from speech\_commands\.txt:

pcm:0000010002000300\.\.\.int16 PCM hex\.\.\.|||yes

pcm:fffefffefffd\.\.\.int16 PCM hex\.\.\.|||no

## __2\.2 The Three Input Types__

The prefix at the start of the input string tells Cypha\.py which encoder path to use:

__Prefix__

__Data type__

__Encoding__

__Cypha encoder path__

\(none\)

Text, URLs, feature vectors

UTF\-8 plain text

encode\_text\(\) — byte seq Ω \+ token stats

"iq:"

RF/radio signal

int8 IQ pairs as lowercase hex

\_encode\_iq\(\) — STFT power spectral density

"pcm:"

Audio signal

int16 PCM samples as lowercase hex

\_encode\_audio\(\) — mel filterbank

__Why hex encoding for signals?__

The wire format is plain text \(UTF\-8\)\. Binary data cannot be stored directly in a UTF\-8 text file\. Lowercase hex is used instead of base64 because it is easier to inspect visually and has no padding concerns\. The overhead is 2 bytes per binary byte, which is acceptable since the files are only read once \(streamed at training time, never loaded into RAM\)\.

## __2\.3 The IQ Prefix — RF Signal Encoding__

RF signals are stored as interleaved int8 I/Q pairs\. Given a complex float32 signal S ∈ ℂⁿ:

  I\[k\]  =  clip\( round\(127 · Re\(S\[k\]\)\), −127, 127 \)  ∈ int8

  Q\[k\]  =  clip\( round\(127 · Im\(S\[k\]\)\), −127, 127 \)  ∈ int8

  wire\[2k\]   = I\[k\]    \(even positions = real component\)

  wire\[2k\+1\] = Q\[k\]    \(odd positions = imaginary component\)

The byte array wire ∈ int8^\{2n\} is then hex\-encoded and written as iq:HEXHEXHEX\.\.\.

When Cypha reads this back, it calls bytes\.fromhex\(text\[3:\]\), reinterprets as int8, splits into even/odd to recover I and Q, forms complex64 = I \+ iQ, and runs a 512\-point short\-time FFT\. This produces the power spectral density that the Omega encoder then processes\.

__Why not store raw float32?__

Float32 hex would be 8 characters per sample vs 2 for int8\. The 4× size increase matters for a 5 GB RF dataset — it would become 20 GB\. The int8 quantisation loses less than 0\.4% of the dynamic range and has no measurable effect on classification accuracy\.

## __2\.4 The PCM Prefix — Audio Encoding__

WAV audio is stored as raw int16 PCM bytes — the same format the WAV file uses internally, with no resampling or channel mixing at this stage\. convert\.py reads WAV frames directly:

with wave\.open\(wav\_path, "rb"\) as wav:

    frames = wav\.readframes\(wav\.getnframes\(\)\)

    audio\_hex = frames\.hex\(\)

f\.write\(f"pcm:\{audio\_hex\}|||\{label\}\\n"\)

When Cypha reads this back, it calls bytes\.fromhex\(text\[4:\]\), reinterprets as int16 little\-endian, normalises to float32 ∈ \[−1, 1\], and passes through a 26\-band mel filterbank with 512\-point FFT windows\. The mel filterbank output feeds into the Omega encoder\.

# __3\. State Machine__

convert\.py uses the same resumable state\-machine design as download\.py\. The state is tracked in convert\_state\.json\.

\{

  "completed": \["sql\_injection", "malware", \.\.\.\],

  "failed": \{

    "panoradio\_rf": \{ "error": "Labels file not found: \.\.\.", "timestamp": "\.\.\." \}

  \},

  "in\_progress": null,

  "converted\_files": \{

    "sql\_injection": \{

      "output\_file": "sql\_injection\.txt",

      "sample\_count": 29442,

      "size\_mb": 1\.87,

      "timestamp": "2026\-02\-21 09:30:12"

    \}

  \}

\}

Conversions are sequential, not parallel\. Only one dataset is in\_progress at a time\. If the process is killed mid\-conversion, the output file may be incomplete — on the next run, the in\_progress entry causes that dataset to be re\-converted from scratch\. The output file is always written completely before mark\_completed\(\) is called\.

# __4\. Converter Details__

Each dataset has a dedicated converter function\. The sections below describe what each one does, what quirks it handles, and what the output looks like\.

## __4\.1  convert\_sql  →  sql\_injection\.txt__

Input: sqli\.csv \(UTF\-16 encoded, ~30k rows, two relevant columns\)\.

### __Encoding quirk__

The file uses UTF\-16 with a byte order mark \(BOM: 0xff 0xfe\)\. Python's default UTF\-8 reader fails on it\. The converter tries three encodings in order — utf\-16, latin\-1, utf\-8 — and uses the first that succeeds\.

### __Column detection__

Rather than hardcoding column names, the converter scans all column names and matches by keyword:

- query\_col: column name contains "query", "sentence", or "text"
- label\_col: column name contains "label", "target", or "class"

### __Label normalisation__

The raw label values vary by dataset version \(some use 0/1 integers, some use "normal"/"benign"\)\. The converter normalises to two canonical labels:

  0 | "0" | "normal" | "benign" | "safe"  →  safe

  anything else  →  sql\_injection

\# Sample output lines:

SELECT \* FROM employees WHERE dept='engineering' LIMIT 10|||safe

' UNION SELECT username, password FROM admin \-\-|||sql\_injection

## __4\.2  convert\_phishing\_urls\_vrbancic  →  phishing\_vrbancic\.txt__

Input: phishing\_vrbancic\.csv \(~88k rows, 48 URL feature columns plus a "phishing" label column\)\.

### __URL vs feature vector__

If a column named exactly "url" exists, the raw URL string is used as the input\. If not \(which is the case for this dataset — it only has engineered features\), the first 20 feature columns are concatenated as "colname:value" pairs:

\# If no URL column:

features = \["NumDots:3", "SubdomainLevel:2", "PathLevel:1", \.\.\.\]

text = " "\.join\(features\)

Labels: phishing if the "phishing" column = 1, else legitimate\.

\# Sample output:

NumDots:3 SubdomainLevel:2 PathLevel:1 UrlLength:52 \.\.\.|||phishing

NumDots:1 SubdomainLevel:0 PathLevel:2 UrlLength:28 \.\.\.|||legitimate

## __4\.3  convert\_malware  →  malware\.txt__

Input: malware\.csv \(~10k rows, PE feature columns plus a label column\)\.

### __Feature serialisation__

Every non\-label column where the value is non\-null and non\-zero is included as "colname:value"\. Zero values are dropped because they add no information and would dominate the token count\. At most 50 features per row are included \(the most informative features appear first in the column ordering\):

\# Sample output:

SizeOfCode:24576 MajorLinkerVersion:14 SizeOfInitializedData:8192 \.\.\.|||benign

SizeOfCode:98304 VirtualAlloc:1 CreateRemoteThread:1 WriteProcessMemory:1 \.\.\.|||malware

## __4\.4  convert\_network  →  network\_intrusion\.txt__

Input: network\_intrusion\.csv \(NSL\-KDD format, no header row, 41 feature columns, last column is label\)\.

### __No header row__

NSL\-KDD uses no column names — pandas assigns numeric column indices 0, 1, 2, …, 41\. The label is always the last column \(index 41\)\. The converter uses the first 20 feature columns\.

### __Integer column name renaming bug__

pandas itertuples\(\) renames integer column names to \_0, \_1, etc\. \(reserved attribute names\)\. The converter avoids this by working directly with the numpy values array \(df\.values\) and using integer indices rather than attribute access:

\# BUG: this breaks when column names are integers

for row in df\.itertuples\(\):

    val = row\.0   \# SyntaxError or AttributeError

\# FIX: use values array directly

arr = df\.values

for row in arr:

    val = row\[feat\_idx\[i\]\]   \# always works

### __Binary label mapping__

All 39 attack types in NSL\-KDD \(neptune, back, portsweep, warezclient, etc\.\) are mapped to a single "anomaly" label for binary classification\. Only "normal" stays as is:

  "normal" in label\_val\.lower\(\)  →  normal

  anything else  →  anomaly

\# Sample output:

f0:0\.00 f1:0\.00 f2:0\.00 f3:215\.00 f4:45076\.00 \.\.\.|||normal

f0:0\.00 f1:0\.00 f2:0\.00 f3:105\.00 f4:146\.00 \.\.\.|||anomaly

## __4\.5  convert\_emails  →  phishing\_emails\.txt__

Input: phishing\_emails\.csv \(SpamAssassin corpus, UTF\-8 or latin\-1, text \+ label columns\)\.

### __Column detection__

- text\_col: column name contains "text", "body", "email", or "message"
- label\_col: column name contains "label", "spam", or "phish"

### __Truncation__

Email bodies are truncated to 500 characters\. The Omega encoder's byte sequence features are dominated by the statistical signature of the first few hundred bytes, so longer inputs add noise rather than signal\. Minimum length is 10 characters — shorter "emails" are dropped\.

  text  =  raw\_email\_body\.strip\(\)\[:500\]

\# Sample output \(truncated for display\):

Dear valued customer, your account has been suspended\. Click here immediately to\.\.\.|||phishing

Hi team, the Q3 report is attached\. Let me know if you have questions\.\.\.|||safe

## __4\.6  convert\_panoradio\_rf  →  panoradio\_rf\.txt__

Input: dataset\_panoradio\_hf\.npy \(5 GB NumPy float32 array\) \+ dataset\_panoradio\_hf\_tags\.csv \(labels\)\.

__Memory\-mapped loading__

The 5 GB NPY file is loaded with np\.load\(path, mmap\_mode="r"\)\. This does not read the file into RAM — it maps the file into virtual address space\. Only the pages actually accessed \(one signal row at a time\) are loaded from disk\. Peak RAM usage during conversion is dominated by the output buffer and pandas, not by the signal data\.

### __Label column detection__

The tags CSV has no standardised column schema\. The converter tries a list of known column names \(label, tag, class, category, modulation, signal\_type, mode, type\) and falls back to the second column if none match\.

### __Signal encoding__

Each row of the NPY array is a complex float32 signal\. The converter scales to int8 range, interleaves I/Q, and hex\-encodes:

signal = data\[i\]                         \# float32 complex row

I = \(signal\.real \* 127\)\.astype\(np\.int8\)  \# scale to \[\-127, 127\]

Q = \(signal\.imag \* 127\)\.astype\(np\.int8\)

iq = np\.empty\(len\(I\) \+ len\(Q\), dtype=np\.int8\)

iq\[0::2\] = I                             \# even indices = I

iq\[1::2\] = Q                             \# odd indices = Q

hex\_str = iq\.tobytes\(\)\.hex\(\)

f\.write\(f"iq:\{hex\_str\}|||\{label\}\\n"\)

Output labels include: am, fm, lsb, usb, cw, rtty, and others depending on the tag file version\. These are the radio modulation modes captured in the HF \(high\-frequency, 3–30 MHz\) band\.

## __4\.7  convert\_phiusiil  →  phiusiil\_phishing\.txt__

Input: phiusiil\_phishing\.zip \(UCI ML Repository, 235k rows, 111 URL feature columns\)\.

### __ZIP extraction__

The ZIP is extracted to \./phiusiil\_extracted/\. The converter then walks the directory tree to find any \.csv file\. This handles nested zip structures where the CSV may be one or two directories deep\.

### __URL vs feature column detection__

Unlike the Vrbancic dataset, PHIUSIIL may contain an actual URL column\. The detector checks:

- Exact column name match: "url", "domain", "address", "link"
- If no exact match, inspect the values of each column — if any sample starts with "http" or "www\.", that column is the URL column\.
- If still no match, raise an error with the available column list\.

Labels: 1 → phishing, 0 → legitimate \(also accepts string variants "phishing"/"legitimate"\)\.

## __4\.8  convert\_speech\_commands  →  speech\_commands\.txt__

Input: speech\_commands\.tar\.gz \(TensorFlow speech commands v0\.02, 35 word directories, ~105k WAV files\)\.

### __Extraction with corruption guard__

The TAR\.GZ is extracted to \./speech\_commands\_extracted/\. The extractor counts subdirectories before and after — if fewer than 30 subdirectories exist, the extraction is deemed incomplete and retried from scratch \(removing the partial extraction first\)\. Speech Commands v0\.02 has 35 word directories plus a background noise directory\.

def count\_subdirs\(d\):

    return sum\(1 for x in os\.listdir\(d\)

               if os\.path\.isdir\(os\.path\.join\(d, x\)\) and not x\.startswith\("\."\)\)

if count\_subdirs\(extract\_dir\) < 30:

    shutil\.rmtree\(extract\_dir\)  \# remove partial

    re\_extract\(\)

### __Background noise exclusion__

The directory \_background\_noise\_ is excluded — it contains long ambient recordings used for data augmentation during neural network training, not labelled word examples\. Including it would create a spurious "background\_noise" class\.

### __WAV reading__

Python's built\-in wave module reads the WAV frames\. No resampling\. The raw int16 bytes are hex\-encoded directly — no normalisation, no channel conversion at this stage\. Cypha's PCM encoder handles the int16 → float conversion internally\.

\# Sample output:

pcm:0000000000000000010000000000000001000000\.\.\.|||yes

pcm:fffffffefffffffdfffffffeffff\.\.\.|||no

## __4\.9  convert\_esc50  →  esc50\.txt__

Input: esc50\.zip \(ESC\-50 environmental sounds, 2000 WAV files, 50 classes × 40 samples each\)\.

### __Metadata\-driven__

Unlike Speech Commands \(where labels come from directory names\), ESC\-50 stores labels in a metadata CSV at ESC\-50\-master/meta/esc50\.csv\. The converter reads the metadata to pair each WAV filename with its category label\. This is more robust than parsing directory structure\.

\# esc50\.csv structure \(first few columns\):

filename,fold,target,category,\.\.\.

1\-100032\-A\-0\.wav,1,0,dog,\.\.\.

1\-100038\-A\-14\.wav,1,14,chirping\_birds,\.\.\.

### __Re\-extraction guard__

If the metadata file cannot be found after extraction, the extractor assumes the ZIP was corrupt or partially extracted and retries\. The metadata path is searched recursively using glob\.glob\("\*\*/meta/esc50\.csv", recursive=True\) to handle any nesting depth\.

# __5\. Output Files__

After a complete run, nine \.txt files are written to the current directory:

__Output file__

__Samples__

__Approx size__

__Input prefix__

__Labels__

sql\_injection\.txt

~29k

~2 MB

none

safe, sql\_injection

phishing\_vrbancic\.txt

~88k

~22 MB

none

legitimate, phishing

malware\.txt

~10k

~3 MB

none

benign, malware

network\_intrusion\.txt

~126k

~15 MB

none

normal, anomaly

phishing\_emails\.txt

~10k

~3 MB

none

safe, phishing

panoradio\_rf\.txt

~400k

~2–4 GB

"iq:"

am, fm, lsb, usb, cw, rtty, \.\.\.

phiusiil\_phishing\.txt

~235k

~60 MB

none

legitimate, phishing

speech\_commands\.txt

~105k

~1\.5 GB

"pcm:"

35 word classes \(yes, no, go, \.\.\.\)

esc50\.txt

2,000

~600 MB

"pcm:"

50 sound classes \(dog, rain, \.\.\.\)

panoradio\_rf\.txt and speech\_commands\.txt are large because each signal is hex\-encoded \(2× the binary size\)\. They are only read once at benchmark time via byte\-offset streaming — they are never loaded into RAM in their entirety\.

# __6\. The convert\_dataset\(\) Orchestrator__

All nine converter functions are invoked through a single orchestrator function:

def convert\_dataset\(state, name, input\_file, output\_file, converter\_func\):

    if is\_completed\(state, name\): return          \# skip already done

    if not os\.path\.exists\(input\_file\):            \# missing raw file

        mark\_failed\(state, name, f"Input not found: \{input\_file\}"\)

        return

    state\["in\_progress"\] = name

    save\_state\(state\)

    try:

        sample\_count = converter\_func\(input\_file, output\_file\)

        if sample\_count == 0: raise ValueError\("No samples converted"\)

        size\_mb = os\.path\.getsize\(output\_file\) / \(1024\*1024\)

        mark\_completed\(state, name, output\_file, sample\_count, size\_mb\)

    except Exception as e:

        mark\_failed\(state, name, f"\{type\(e\)\.\_\_name\_\_\}: \{e\}"\)

        traceback\.print\_exc\(\)

The orchestrator guarantees that:

- A dataset is never marked completed unless its converter returns sample\_count > 0\.
- Any exception \(including import errors, missing dependencies, malformed data\) is caught, logged, and stored in the failed dict without aborting the remaining conversions\.
- KeyboardInterrupt propagates cleanly with a clear resume message\.

# __7\. Function Reference__

__Function__

__Input__

__Purpose__

load\_state\(\)

—

Read convert\_state\.json\. Returns empty state if missing\.

save\_state\(state\)

state dict

Write state to convert\_state\.json\.

mark\_completed\(\.\.\.\)

state, name, output, n, mb

Record successful conversion\.

mark\_failed\(state, name, err\)

state, str, str

Record failure with error message\.

is\_completed\(state, name\)

state, str

True if name in state\["completed"\]\.

show\_status\(state\)

state dict

Print formatted conversion status\.

convert\_sql\(in, out\)

CSV \(UTF\-16\)

SQL injection CSV → wire format\.

convert\_phishing\_urls\_vrbancic\(in, out\)

CSV

Phishing URL features → wire format\.

convert\_malware\(in, out\)

CSV

Malware PE features → wire format\.

convert\_network\(in, out\)

CSV \(no header\)

NSL\-KDD flows → wire format\.

convert\_emails\(in, out\)

CSV

Email bodies → wire format\.

convert\_panoradio\_rf\(in, out\)

NPY \+ CSV

5 GB RF signals → iq: wire format via mmap\.

convert\_phiusiil\(in, out\)

ZIP

PHIUSIIL phishing ZIP → wire format\.

convert\_speech\_commands\(in, out\)

TAR\.GZ

Speech Commands WAVs → pcm: wire format\.

convert\_esc50\(in, out\)

ZIP

ESC\-50 WAVs → pcm: wire format using metadata CSV\.

convert\_dataset\(state, name, in, out, func\)

all

Orchestrator: skip/guard/exception\-wrap any converter\.

main\(\)

—

Entry point\. Parses flags, runs all conversions\.

# __8\. Troubleshooting__

## __8\.1  panoradio\_rf fails with "Labels file not found"__

Both dataset\_panoradio\_hf\.npy and dataset\_panoradio\_hf\_tags\.csv must be present\. The tags file is a separate download \(panoradio\_tags in download\.py\)\. Check that both exist:

ls \-lh dataset\_panoradio\_hf\.npy dataset\_panoradio\_hf\_tags\.csv

## __8\.2  speech\_commands fails with tarfile errors__

If speech\_commands\.tar\.gz is partially downloaded or corrupt, tarfile\.open\(\) will raise an exception\. Delete the TAR file, re\-run download\.py \-\-retry, and then re\-run convert\.py \-\-retry\.

## __8\.3  "No samples converted"__

This means the converter ran without raising an exception but wrote zero valid lines\. Common causes:

- The column detection failed — the auto\-detected query\_col, label\_col, or url\_col is wrong\. Check the printed "Columns:" line and compare with what the converter is looking for\.
- The input file is empty or a partial download\. Check file size with ls \-lh\.
- All rows were skipped due to the minimum length filter \(len\(text\) < 3 or < 10\)\. This can happen if the column mapping picked the wrong column\.

## __8\.4  Slow conversion for panoradio\_rf__

Converting 400k signals at ~5 KB each \(after hex encoding\) takes 15–30 minutes\. The mmap approach ensures it does not run out of RAM, but disk I/O is the bottleneck\. Use an SSD if possible\.

End of convert\.py reference\.  Next: benchmark\.py

