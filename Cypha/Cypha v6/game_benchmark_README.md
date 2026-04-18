<!-- Converted from `game_benchmark_README.docx` — source was Word (.docx). -->

__game\_benchmark\.py__

*Cypha HRNA Synthetic Game Theory Benchmark*

Chess   Poker   Go   150,000 examples   deep component profiling

Technical Reference   v2   February 2026

# __1\. Purpose__

game\_benchmark\.py is a deep validation and profiling tool for Cypha HRNA\. It generates 150,000 synthetic game theory examples across three domains, trains Cypha on 80% of them, evaluates on the remaining 20%, and produces a detailed breakdown of every component's behaviour — including how often each deliberation method fires, where time is spent, and which classes are hardest to distinguish\.

The benchmark is not testing whether Cypha can play chess, poker, or Go\. It is testing whether Cypha's internal architecture is operating correctly when confronted with high\-complexity, multi\-class classification problems with genuine decision\-boundary ambiguity\. The three game domains were chosen because they provide exactly the right difficulty profile: clear class structure, known\-good feature engineering, and natural class pairs that are genuinely hard to separate\.

The primary verification targets are the deliberation pipeline components\. Vanilla classification with high hippo hit rates is uninteresting — it means the training data is too easy and Cypha never needs to think hard\. The benchmark is explicitly designed to force Cypha into deliberation for 35\-55% of test examples, which is the regime where the full GRIA cascade, Rocchio, PNQ, MCTS, and DMN all activate and can be profiled\.

__Property__

__Value__

__Domains__

chess\_evaluation \(9 classes\), poker\_decision \(8 classes\), go\_strategy \(10 classes\)

__Examples per domain__

50,000 \(600 in \-\-quick mode\)

__Total examples__

150,000

__Train / test split__

80% train, 20% test

__Training epochs__

1 \(hardcoded — single\-pass by design\)

__Boundary examples__

25% of each domain generated at class boundaries

__Feature tokens per example__

~60\-70 tokens

__Feature dimension__

512

__Resonance dimension__

256

__Output__

Per\-domain accuracy, per\-class breakdown, full component profile, JSON report

# __2\. Setup and Usage__

## __2\.1  Requirements__

numpy is the only external dependency\. No chess engine, no poker library, no Go engine — all three game AIs are embedded pure\-Python implementations inside the file itself\.

pip install numpy

\# Cypha\.py must be in the same directory

python game\_benchmark\.py

## __2\.2  Command\-line flags__

__Flag__

__Effect__

__\(no flags\)__

Full benchmark: 50,000 examples per domain, all three domains

__\-\-quick__

Smoke\-test mode: 600 examples per domain, runs in seconds

__\-\-domain chess\_evaluation__

Run only the chess domain

__\-\-domain poker\_decision__

Run only the poker domain

__\-\-domain go\_strategy__

Run only the Go domain

__\-\-verbose__

Print deliberation trace for each inference \(very verbose on 50k examples\)

python game\_benchmark\.py \-\-quick

python game\_benchmark\.py \-\-domain go\_strategy

python game\_benchmark\.py \-\-domain chess\_evaluation \-\-verbose

# __3\. Synthetic Data Generation__

Each domain has an embedded AI class \(ChessAI, PokerAI, GoAI\) that generates realistic feature strings for a given class label\. These are not templates filled with random words — each feature is derived from class\-specific parameter ranges that encode real game logic\. A tactical\_combo position looks different from a fortress\_defense position because the material balance, mobility, king safety, and pawn structure parameters are drawn from ranges that reflect how those positions actually look in real chess games\.

## __3\.1  Boundary examples__

25% of examples in each domain are generated as boundary examples\. For a given class, there is a defined BOUNDARY\_PAIRS map that specifies which other class it is most likely to be confused with\. When generating a boundary example, the feature generator partially blends in the statistical signature of the paired class: it draws some numeric parameters from the boundary class ranges and borrows 1\-3 vocabulary keywords from the boundary class's token set\.

This is what forces deliberation to fire\. A clean tactical\_combo example is easy — it has a high eval score, complex middlegame phase, and characteristic tactical vocabulary\. A boundary example between tactical\_combo and piece\_sacrifice has a negative material balance \(borrowed from piece\_sacrifice\) while retaining the high mobility and eval signal of tactical\_combo\. Cypha's hippo fast\-path will miss these because they do not match stored episodes cleanly, and the deliberation engine must resolve them\.

## __3\.2  Data generation pipeline__

for each class in domain\.classes:

    per\_cls = n // len\(classes\)        \# balanced class distribution

    boundary\_class = BOUNDARY\_PAIRS\[cls\]

    for i in range\(per\_cls\):

        if random\(\) < 0\.25:

            features = ai\.generate\(cls, boundary\_target=boundary\_class\)

        else:

            features = ai\.generate\(cls, boundary\_target=None\)

        pairs\.append\(\(features, cls\)\)

shuffle\(pairs\)

return pairs\[:n\]

# __4\. The Three Embedded Game AIs__

## __4\.1  ChessAI — 9\-class chess position classifier__

ChessAI generates feature strings that represent chess positions at different stages and character types\. It uses piece\-square tables \(PSTs\), pawn structure analysis, and king safety heuristics — the same features used by real chess engines — to produce statistically realistic position descriptions\.

The 9 classes cover the full spectrum of chess position types that require different strategic thinking:

__Class__

__What it represents__

__Key distinguishing features__

__tactical\_combo__

Position where forcing moves or tactics exist

High eval, complex middlegame, tactical flags \(pin, fork, back rank\), high mobility

__positional\_squeeze__

Quiet positional advantage through space/mobility

Moderate eval, high white mobility vs low black mobility, open files low

__endgame\_technique__

Technical endgame with a clear winning method

Late game phase, low mobility, passed pawns, opposition/key square flags

__pawn\_storm__

Aggressive kingside or queenside pawn advance

Opposite castling, open files near king, high pawn storm vocab

__piece\_sacrifice__

Material deficit with compensation \(attack/initiative\)

Negative material balance \(\-400 to \-50\), high eval, material\_deficit flag

__fortress\_defense__

Defending a difficult position by building a fortress

Large material deficit, low mobility for both sides, endgame phase

__zugzwang__

Position where any move worsens the position

Endgame phase, very low mobility both sides, opposition flags

__opening\_theory__

Early game following known theoretical lines

Low move number, opening/early middlegame phase, low eval variance

__endgame\_conversion__

Converting a winning endgame advantage

Material surplus, late game, moderate to low mobility, key square control

__Feature tokens \(~65 per example\)__

Each ChessAI example contains the following token types:

__opening\_X__

Opening system played \(Sicilian, Ruy Lopez, QGD, KID, etc\.\) — 20 openings

__move\_N__

Full move number \(1\-80 depending on game phase\)

__phase\_X__

Game phase \(opening, early\_middlegame, complex\_middlegame, simplified\_middlegame, pawn\_endgame, rook\_endgame, piece\_endgame, minor\_piece\_endgame, queen\_endgame\)

__mat\_\+N__

Material balance in centipawns \(pawn=100, knight=320, bishop=330, rook=500, queen=900\)

__eval\_\+N__

Position evaluation in centipawns from engine\-style assessment

__king\_safety\_w\_N / king\_safety\_b\_N__

King safety score for each side \(attackers near king, 0\-10\)

__pawn\_shield\_w\_N / pawn\_shield\_b\_N__

Pawn shield integrity \(0\-3, pawns protecting the king\)

__open\_file\_near\_king\_w\_N / \.\.\.\_b\_N__

Open files near the king \(enemy rooks can penetrate\)

__mobility\_w\_N / mobility\_b\_N__

Legal move count for each side

__open\_files\_N__

Total open files on the board

__passed\_w\_N / passed\_b\_N__

Passed pawn count for each side

__isolated\_w\_N / isolated\_b\_N__

Isolated pawn count \(pawns with no friendly pawns on adjacent files\)

__doubled\_w\_N / doubled\_b\_N__

Doubled pawn count

__pawn\_islands\_w\_N / pawn\_islands\_b\_N__

Pawn island count \(connected groups of pawns\)

__castled\_w\_X / castled\_b\_X__

Castling status: ks \(kingside\), qs \(queenside\), no \(not castled\)

__pawn structure token__

One of 12 pawn structure types \(IQP, hanging pawns, Carlsbad, etc\.\)

__piece config token__

One of 15 piece configuration types \(bishops of same color, rooks on 7th, etc\.\)

__piece\_activity\_X__

Overall piece activity level: low, med, high

__tempo\_X__

Who has the tempo: w, b, equal

__depth\_N__

Search depth the position was assessed at \(10\-40\)

__tactical flags__

Situational flags: pin\_detected, fork\_threat, back\_rank\_weak, decisive\_advantage, material\_up, opposition\_active, opposite\_castling, etc\.

__class keywords__

8\-12 vocabulary tokens specific to the class \(e\.g\. initiative\_compensation, king\_attack\_compensation for piece\_sacrifice\)

__Boundary pairs__

__Class__

__Boundary partner__

__Why they are hard to separate__

__tactical\_combo__

piece\_sacrifice

Both have high eval and complex middlegame; sacrifice positions often arise from tactics

__piece\_sacrifice__

tactical\_combo

Material deficit vs balanced with similar eval signals

__fortress\_defense__

zugzwang

Both have low mobility and material deficit; differ in whether moves improve or worsen things

__zugzwang__

fortress\_defense

Very low mobility for both sides — the key difference is whether the position is static or dynamic

__pawn\_storm__

positional\_squeeze

Open files and pawn advances appear in both; differ in king safety context

__endgame\_technique__

endgame\_conversion

Both are winning endgames; technique requires specific method, conversion is more straightforward

__endgame\_conversion__

endgame\_technique

Converting material advantage — boundary is how clear\-cut the win is

__positional\_squeeze__

opening\_theory

Both can have similar material balance and low eval; differ in move number and phase

__opening\_theory__

positional\_squeeze

Early middlegame positions where theory ends and positional play begins

## __4\.2  PokerAI — 8\-class poker decision classifier__

PokerAI generates feature strings representing Texas Hold'em decision scenarios\. It uses real GTO \(Game\-Theory Optimal\) concepts: minimum defence frequency \(MDF\), fold equity, nut advantage, implied odds, and stack\-to\-pot ratio\. Equity is approximated using board\-texture\-aware Monte Carlo with Gaussian noise on top of a class\-specific equity hint, producing realistic variance without the computational cost of full card\-level simulation\.

__Class__

__Decision type__

__Typical equity range__

__Key context__

__value\_bet__

Bet for value with a strong hand

62\-95%

Top pair\+, sets, strong draws\. Build pot, commit stack\.

__bluff__

Bet with air/weak hand using fold equity

4\-22%

Nothing hands, backdoor draws\. Credible line, polarized range\.

__check\_call__

Check or call — pot control with medium hand

32\-62%

Middle pairs, draws, showdown value hands\.

__fold__

Fold with no equity or reverse implied odds

3\-22%

Dominated hands, drawing dead, pot committed math fails\.

__pot\_control__

Bet small or check to keep pot manageable

48\-72%

Medium\-strength made hands that can't stand a raise\.

__semi\_bluff__

Bet drawing hand — equity \+ fold equity combined

24\-50%

Flush draws, straight draws, combo draws\. Aggression builds\.

__check\_raise__

Check then raise — trap strong hands or punish c\-bets

35\-80%

Nut draws, sets, top pair on wet boards\. Polar or semi\-bluff XR\.

__donk\_bet__

Lead into the pre\-flop aggressor — non\-standard line

28\-72%

Range blocking, board texture changes, protection leads\.

__Feature tokens \(~65 per example\)__

__street\_X__

flop, turn, or river

__position\_X__

btn, co, hj, mp, ep, bb, sb — table position

__equity\_N__

Hero equity percentage \(Monte Carlo approximation\)

__eq\_bucket\_X__

Equity bucket: strong \(70%\+\), ahead \(55\-70%\), marginal \(40\-55%\), behind \(25\-40%\), weak \(<25%\)

__pot\_odds\_N__

Pot odds percentage for a standard half\-pot bet

__spr\_N__

Stack\-to\-pot ratio \(effective stack / pot\)

__mdf\_N__

Minimum defence frequency — how often hero must call to prevent a pure bluff being profitable

__fold\_equity\_N__

Estimated percentage of time villain folds to a bet

__nut\_advantage\_X__

Whether hero has more nut combinations than villain \(nut\_adv, no\_nut\_adv\)

__implied\_odds\_X__

Implied odds assessment \(good, medium, poor\)

__board\_texture\_X__

Board type from 10 options: dry\_rainbow, wet\_twoflush, paired\_dry, monotone\_flush, connected\_rundown, etc\.

__hand\_X__

Hand description: top\_pair\_top\_kicker, set, flush\_draw, nothing\_airball, etc\. \(20 options\)

__opp\_type\_X__

Opponent type: passive\_fish, aggressive\_reg, tight\_nit, loose\_agg, tricky\_pro, etc\.

__pot\_N__

Current pot size

__bet\_N__

Bet size being considered

__stack\_eff\_N__

Effective stack size

__bd\_fd / bd\_sd__

Backdoor flush draw or straight draw present

__nut\_blocker / nut\_blocker\_pair__

Hero holds a card that blocks the nut hand

__range\_advantage / disadvantage__

Whether hero's range has more strong hands than villain on this board

__class keywords__

8\-10 GTO vocabulary tokens specific to the decision \(e\.g\. thin\_value, clear\_value, overbet\_value for value\_bet\)

__Boundary pairs__

__Class__

__Boundary partner__

__Why they are hard to separate__

__value\_bet__

pot\_control

Both involve betting with a made hand; the line between thin value and pot control is equity threshold

__bluff__

semi\_bluff

Both involve betting weak holdings; semi\-bluffs have equity, pure bluffs do not

__check\_call__

fold

Both involve not betting; differ in whether the hand has any equity or reverse implied odds

__pot\_control__

value\_bet

Medium\-strong hands that could be either depending on board runout and SPR

__semi\_bluff__

check\_call

Drawing hands can be called or semi\-bluffed depending on fold equity and position

__check\_raise__

check\_call

Both start with a check; differ in whether the hand is strong enough to trap

__donk\_bet__

check\_call

Both involve not following standard lines; donk has a specific strategic purpose

__fold__

check\_call

The critical decision: marginal equity hands that may or may not justify continuing

## __4\.3  GoAI — 10\-class Go strategy classifier__

GoAI generates feature strings representing Go board situations on a 9x9 grid\. It uses a real Go board \(numpy int8 array\), BFS liberty counting, flood\-fill territory estimation, and a vectorised Manhattan\-distance influence map\. The feature strings describe the strategic character of the current position — what type of Go problem is most pressing — rather than individual move decisions\.

Go is the hardest of the three domains\. The classes overlap naturally: a life\-and\-death situation can involve ko; a semeai \(capturing race\) is related to life\-and\-death; influence and reduction are strategic complements\. The benchmark reflects this difficulty — Go is expected to have the lowest hippo hit rate and highest deliberation rate of the three domains\.

__Class__

__Strategic situation__

__Key indicators__

__territory\_lead__

Comfortable territory advantage, converting the win

High territory differential, late game phase \(move 100\+\), sealed territory

__fighting__

Active multi\-stone battle in progress

Balanced captures, moderate territory, atari chains, complex fighting vocabulary

__life\_death__

A group must make two eyes or die

Critical min\_liberties \(1\-3\), life\-death vocabulary \(nakade, vital point, false eye\)

__ko__

Ko fight in progress — recapture sequences

High ko\_b and ko\_w counts \(3\-8\), ko\-specific vocabulary, ko master, superko

__endgame__

Dame filling, small endgame moves remain

Very late phase \(move 180\+\), high stone count, counted territory, yose vocabulary

__influence__

Building a large moyo \(sphere of influence\)

High influence scores, low territory, early\-mid game, moyo vocabulary

__reduction__

Approaching or reducing a large moyo

Moderate stone count, reduction sequence vocabulary, probe moves, shoulder hits

__invasion__

Invading deep into enemy territory

Low min\_liberties for invading group, escape vocabulary, two\-stage invasion

__opening__

Fuseki — establishing framework in opening

Low move count \(<15\), star points, approach moves, shimari formations

__semeai__

Capturing race between two groups

Both groups in atari, liberty counting vocabulary, outside vs inside liberties

__Feature tokens \(~60\-70 per example\)__

__move\_N__

Move number in the game \(1\-260\)

__phase\_X__

Game phase: opening \(<30 moves\), early\_middle \(30\-80\), middle \(80\-150\), late \(150\-200\), endgame \(200\+\)

__b\_terr\_N / w\_terr\_N__

Territory estimate for Black and White via flood\-fill

__b\_capt\_N / w\_capt\_N__

Cumulative captures for each colour

__ko\_b\_N / ko\_w\_N__

Number of ko threats held by each side

__lib\_min\_N__

Minimum liberty count across all groups on the board \(1 = atari\)

__lib\_avg\_N__

Average liberty count across all groups

__dens\_N__

Board density \(stones / total intersections as percentage\)

__moyo\_N__

Estimated moyo size \(unclaimed influence territory\)

__seki\_N__

Whether a seki \(mutual life without eyes\) is present

__b\_groups\_N / w\_groups\_N__

Number of separate connected groups for each colour

__b\_stones\_N / w\_stones\_N__

Total stones on the board for each colour

__b\_atari\_N / w\_atari\_N__

Number of groups in atari \(1 liberty\) for each colour

__b\_max\_group\_N / w\_max\_group\_N__

Size of the largest group for each colour

__b\_eyes\_N / w\_eyes\_N__

Estimated eye count for each colour

__corner\_b\_N / corner\_w\_N__

Stones in corner 3x3 regions for each colour

__edge\_b\_N / edge\_w\_N__

Stones on edge rows/columns for each colour

__center\_b\_N / center\_w\_N__

Stones in the center 5x5 region for each colour

__b\_influence\_N / w\_influence\_N__

Manhattan\-distance decay influence score over empty intersections

__ko\_active\_X__

Whether a ko is currently active \(ko\_active or ko\_inactive\)

__cutting\_points\_N__

Number of cutting points in the position

__ladder\_X__

Whether a ladder is present \(ladder\_possible or ladder\_clear\)

__net\_X__

Whether a net \(geta\) is present

__sente\_X__

Who holds sente \(forcing move priority\): sente\_b, sente\_w, sente\_equal

__class keywords__

7\-9 Go vocabulary tokens specific to the strategic situation

__Boundary pairs__

__Class__

__Boundary partner__

__Why they are hard to separate__

__life\_death__

ko

Both involve critical groups with few liberties; ko fights often arise from life\-and\-death

__ko__

life\_death

Ko recapture sequences often occur in bent\-four\-in\-corner life\-death situations

__territory\_lead__

endgame

Late\-game territory lead transitions smoothly into endgame; both have high territory counts

__endgame__

territory\_lead

Endgame dame filling with comfortable lead looks similar to territory consolidation

__fighting__

invasion

Invasions often turn into fights; both have moderate territory and active groups

__invasion__

fighting

A fight that started as an invasion may now be a general battle

__influence__

reduction

These are strategic complements — one side builds moyo, the other reduces it

__reduction__

influence

Reducing a moyo requires entering the influence zone — the positions overlap

__opening__

influence

Early influence\-building looks like fuseki; both have low move counts and high moyo

__semeai__

life\_death

Capturing races often involve groups that are also fighting for life

# __5\. The Profiler__

The benchmark includes a zero\-overhead profiler that wraps every significant Cypha component via monkey\-patching\. No changes are made to Cypha\.py — the wrapping is applied at runtime using Python's functools\.wraps and direct attribute replacement\. Every wrapped function records its call count, total time, and up to 8,000 individual timing samples for percentile calculation\.

## __5\.1  Instrumented components__

__Component__

__Measurement__

__Path__

__trn\.train\_step__

Full training step per example

Train path

__trn\.forward\_train__

Forward pass during training

Train path

__trn\.memory\_store__

AnchorMemory store operation

Train path

__trn\.hippo\_store\_trn__

HippoCypha episodic store

Train path

__trn\.dmn\_run__

DMN consolidation loop

Train path

__inf\.infer__

Full inference call

Inference path

__inf\.encode\_features__

OmegaEncoder feature extraction

Inference path

__inf\.forward\_infer__

Forward pass during inference

Inference path

__inf\.hippo\_fastpath__

HippoCypha fast\-path lookup

Inference path

__inf\.adapter\_lookup__

AnchorMemoryAdapter MP\-filtered lookup

Inference path

__inf\.workspace\_compete__

GlobalWorkspace ignition competition

Inference path

__thought\.note\_uncertainty__

ThoughtProcessor uncertainty tracking

ThoughtProcessor

__thought\.cascade__

ThoughtProcessor hypothesis generation

ThoughtProcessor

__thought\.multi\_scale__

ThoughtProcessor multi\-scale field blend

ThoughtProcessor

__thought\.self\_generate__

ThoughtProcessor trend detection

ThoughtProcessor

__thought\.resonant\_chain__

ThoughtProcessor coherence scoring

ThoughtProcessor

__mem\.memory\_lookup__

Direct AnchorMemory lookup

Memory

__dlib\.deliberate\_iter__

Iterative deliberation \(legacy path\)

Deliberation

__pnq\.pnq\_lookup__

PNQ perturbation\-noise\-query

Deliberation

__mcts\.mcts\_search__

MCTS tree search

Deliberation

__gria\.gria\_cascade__

Full GRIA 3\-stage cascade

Deliberation

## __5\.2  Counters__

__Counter__

__What it counts__

__hippo\_hit__

Inferences resolved by the hippo fast\-path \(immediate return\)

__hippo\_miss__

Inferences that required deliberation \(hippo did not fire\)

__hippo\_hit\_rate__

Derived: hippo\_hit / \(hippo\_hit \+ hippo\_miss\) \* 100%

__gnw\_fired__

GlobalWorkspace ignition successes after hippo miss

__gnw\_miss__

GlobalWorkspace ignition failures \(forced deliberation\)

__gnw\_fire\_rate__

Derived: gnw\_fired / \(gnw\_fired \+ gnw\_miss\) \* 100%

__path\_rocchio__

Inferences where Rocchio contributed to deliberation

__path\_mcts__

Inferences where MCTS ran

__path\_pnq__

Inferences where PNQ ran \(approximated by round count >= 2\)

__dmn\_calls__

Times the DMN consolidation loop was triggered

## __5\.3  Profile report format__

After each domain and at the end of the full run, a profile table is printed with columns: component name, call count, mean latency \(microseconds\), p50, p95, p99, and total time \(milliseconds\)\. The report is grouped into five sections: TRAIN PATH, INFER PATH, THOUGHT PROCESSOR, MEMORY, and DELIBERATION\.

╔══════════════════════════════════════════════════════════════════════════════╗

║  CYPHA PROFILE — POKER\_DECISION \(train\+infer\)                               ║

╠══════════════════════════════════════════════════════════════════════════════╣

║  ─── INFER PATH                                                              ║

║  component                    calls    mean\_us    p50     p95     p99  total\_ms║

║  ─────────────────────────────────────────────────────────────────────────   ║

║  encode\_features              10,000    1,166    1,180   1,200   1,245     11,660 ║

║  hippo\_fastpath               10,000    1,352    1,350   1,479   1,501     13,520 ║

║  infer                         6,780    4,012    3,990   4,323   4,801     27,201 ║

║  ─── COUNTERS                                                                ║

║  hippo\_hit                                                         3,220        ║

║  hippo\_miss                                                        6,780        ║

║  hippo\_hit\_rate                                                    32\.2%        ║

╚══════════════════════════════════════════════════════════════════════════════╝

# __6\. Domain Profile Block__

Before training begins on each domain, the benchmark prints a domain profile block showing the statistical properties of the generated dataset\. This is important for verifying that the data generator produced a balanced, diverse dataset with the right token density\.

  ┌────────────────────────────────────────────────────────────────────┐

  │  DOMAIN PROFILE · CHESS\_EVALUATION                                 │

  ├────────────────────────────────────────────────────────────────────┤

  │  Total examples              50,000                                │

  │  Classes                          9                                │

  │  Gen time                      2\.14s                               │

  │  Examples/sec                23,364                                │

  ├────────────────────────────────────────────────────────────────────┤

  │  Class                      count    pct  avg\_tok                  │

  │  ─────────────────────────────────────────────────────────         │

  │  tactical\_combo              5,556   11\.1%    65\.3                  │

  │  positional\_squeeze          5,556   11\.1%    64\.8                  │

  │  endgame\_technique           5,556   11\.1%    66\.1                  │

  │  \.\.\.                                                               │

  ├────────────────────────────────────────────────────────────────────┤

  │  Token stats  min=58  mean=65\.2  max=74                            │

  │  Vocabulary size              4,821                                │

  │  Top\-5 tokens  material\_balanced\(12441\)  slight\_advantage\(11203\)   │

  └────────────────────────────────────────────────────────────────────┘

The vocabulary size shows how many unique tokens the domain uses\. A richer vocabulary gives Cypha more signal to work with\. The top\-5 tokens reveal which features dominate the corpus — high\-frequency tokens like material\_balanced appear across many classes and contribute less discriminative power than rare class\-specific tokens\.

# __7\. Training and Evaluation Pipeline__

Data is written to a temporary file in the format input|||label with one example per line\. Cypha reads this file using the offset\-indexed training path \(train\_file\_stateful\_offsets\), which builds a byte\-offset index and reads examples by seeking directly to each offset\. This avoids loading the entire dataset into RAM\.

\# Training — single epoch, offset\-indexed file read

cypha\.train\_file\_stateful\_offsets\(tmp\_file, train\_offsets, domain\_name,

                                   epochs=1, verbose=True\)

\# Evaluation — give\_feedback called on every test example

for offset in test\_offsets:

    input\_text, expected = read\_at\_offset\(file, offset\)

    predicted, confidence = cypha\.infer\(input\_text\)

    if predicted == expected:

        correct \+= 1

    \# give\_feedback updates reflexion memory, confusion graph,

    \# cerebellum output model, and Platt calibrator

    cypha\.give\_feedback\(input\_text, predicted, expected,

                         top\_margin, history=None\)

__give\_feedback__

During evaluation, give\_feedback is called with the ground truth label after every inference\. This is deliberate — it activates the reflexion failure memory \(so the same mistake is less likely on the next similar input\), updates the ConfusionGraph with real confusion data, and calibrates the Platt calibrator with real correct/wrong signal\. The evaluation set is not truly held\-out in the machine learning sense — it is a live learning phase\.

## __7\.1  Kappa\(D\) — complexity metric__

For each test example, the benchmark computes kappa\(D\) — the excess kurtosis of the byte\-level differential of the input string\. This measures the statistical complexity of the feature string's byte encoding\. High kappa\(D\) values indicate heavy\-tailed distributions in the byte stream, which corresponds to feature strings with unusual or rare token combinations\. The distribution of kappa\(D\) across test examples gives a measure of how complex the overall test set is\.

Kappa\(D\) is reported as mean, standard deviation, p5 and p95\. A higher mean indicates a more complex test set\. This is primarily a diagnostic metric to verify that the synthetic generator is producing statistically diverse inputs rather than repetitive templates\.

# __8\. Understanding the Output__

## __8\.1  Per\-class accuracy bar chart__

  Per\-class accuracy:

  Class                         Bar            Correct    Acc

  ──────────────────────────────────────────────────────────

  tactical\_combo           ██████████  1,089/1,112  \( 97\.9%\)

  positional\_squeeze       █████████░  1,051/1,111  \( 94\.6%\)

  piece\_sacrifice          ████████░░  1,002/1,112  \( 90\.1%\)

  fortress\_defense         ████████░░    986/1,111  \( 88\.7%\)

  zugzwang                 ████████░░    971/1,111  \( 87\.4%\)

Classes with lower accuracy are the interesting ones — they represent the hardest decision boundaries in the domain\. Piece\_sacrifice and fortress\_defense consistently score lower than tactical\_combo because their feature signatures overlap with other classes\. This is expected and reflects the quality of the boundary generation\.

## __8\.2  Sample errors__

  Sample errors \(first 10\):

    expected=fortress\_defense      got=zugzwang             conf=0\.341

    input: phase\_pawn\_endgame mat\_\-280 eval\_\-40 king\_safety\_w\_6 mobility\_w\_4\.\.\.

    expected=piece\_sacrifice       got=tactical\_combo       conf=0\.412

    input: phase\_complex\_middlegame mat\_\-180 eval\_\+240 king\_safety\_w\_3\.\.\.

Error analysis reveals the natural confusion structure of the domain\. fortress\_defense confused with zugzwang is expected — both have low mobility endgame positions\. The features that distinguish them \(static vs\. worsening position\) are subtle and may require deliberation to resolve correctly\. A low confidence score \(0\.341\) on an error indicates Cypha was uncertain — a higher confidence error indicates the system was wrongly confident\.

## __8\.3  JSON report__

After all domains complete, results are saved to game\_benchmark\_report\_v2\.json in the same directory\. The JSON contains the full per\-domain accuracy, per\-class accuracy, training and evaluation times, number of samples, and all errors\. This file can be used to track accuracy changes across code iterations\.

\{

  "total\_wall\_time\_s": 412\.7,

  "epochs": 1,

  "n\_per\_domain": 50000,

  "domains": \{

    "chess\_evaluation": \{

      "accuracy": 97\.3,

      "n\_train": 40000,

      "n\_test": 10000,

      "per\_class\_acc": \{"tactical\_combo": 97\.9, \.\.\.\},

      "errors": \[\.\.\.\]

    \},

    \.\.\.

  \}

\}

# __9\. Interpreting Results — What to Look For__

__Overall accuracy > 95%__

Cypha has successfully learned the class manifolds for the domain\. The feature engineering and class\-specific parameter ranges are well\-separated in the 512\-dimensional anchor space\.

__Hippo hit rate 30\-60%__

Healthy deliberation regime\. Too high \(>80%\) means the test data is too similar to training data — reduce the boundary example blending ratio or increase class count\. Too low \(<20%\) means Cypha is not forming stable prototypes\.

__Rocchio firing on ~30% of deliberation cases__

Rocchio centroid push is working\. If this is 0%, the deliberation pipeline is not routing through the cascade correctly\.

__PNQ and MCTS firing__

PNQ fires when round count >= 2\. MCTS fires for the hardest boundary cases\. These should both show non\-zero counts after a full 50k run\.

__DMN calls > 0__

The Default Mode Network consolidation loop is triggering\. It fires after a configurable number of training steps\.

__ThoughtProcessor calls = N\_train__

All five ThoughtProcessor methods should be called on every training step\. Zero counts indicate a wiring break\.

__Low accuracy on boundary classes__

Expected\. fortress\_defense, zugzwang, piece\_sacrifice \(chess\); fold, check\_call \(poker\); life\_death, ko, semeai \(Go\) are the natural hard boundaries and will always score lower\.

__Consistent p50 vs p95 for hippo\_fastpath__

If p95 is much higher than p50 \(e\.g\. 1,200 vs 8,000 us\), the memory store has grown unevenly\. Consolidation may not be keeping the store compact\.

# __10\. Files and Cleanup__

Each domain creates a temporary directory with a training data file and checkpoint directory\. These are cleaned up automatically at the end of each domain run via shutil\.rmtree\(\)\. If the benchmark is interrupted \(KeyboardInterrupt is caught and handled cleanly\), the temporary directory is also removed\.

The only persistent output is game\_benchmark\_report\_v2\.json in the script directory\. This file is overwritten on each run\.

\# If interrupted or crashed, clean up manually

rm \-rf /tmp/cypha\_game\_\*

*game\_benchmark\.py   Cypha HRNA   February 2026   All rights reserved*

