<!-- Converted from `game_live_benchmark_README.docx` — source was Word (.docx). -->

__game\_live\_benchmark\.py__

*Cypha HRNA Live Game Benchmark*

Chess   Poker   Go   against real opponents

Technical Reference   February 2026

# __1\. Purpose__

game\_live\_benchmark\.py tests Cypha HRNA in actual game play against real opponents — not as a classifier, but as a player that learns a game and then competes\. This is a fundamentally harder test than the classification benchmark\. In classification, Cypha just needs to identify the correct label for a given position\. Here, Cypha must make sequential decisions across an entire game, and a single bad move can cascade into a lost position\.

The benchmark covers three domains — Chess, Poker, and Go — each chosen for a specific reason\. Chess tests whether Cypha can approximate the decisions of a world\-class engine through pure behavioural cloning, with no lookahead of its own\. Poker tests GTO \(game\-theory optimal\) decision\-making where correct play is determined by equity and pot odds rather than aesthetics\. Go tests strategic position evaluation on a game where local moves have global consequences and the winning heuristic is genuinely subtle\.

Each domain follows the same pipeline: generate training data from a known\-good source, train Cypha on that data, then let Cypha play against a real opponent and report results\.

__Domain__

__Training source__

__Test opponent__

__Scoring__

__Chess__

Stockfish depth\-18 self\-play \(200 games\)

Stockfish depth\-20, skill 20 \(maximum\)

Wins / Draws / Losses, score %

__Poker__

GTO\-optimal actions via Monte Carlo equity \(5,000 hands\)

Rule\-based opponent

Net chips, win rate

__Go__

Greedy bot self\-play, winner credit assignment \(500 games\)

Greedy territory bot

Wins / Draws / Losses by final territory

# __2\. Setup and Requirements__

## __2\.1  Python dependencies__

pip install python\-chess treys numpy

\# python\-chess   chess board representation, move generation, Stockfish interface

\# treys          hand evaluator for poker equity calculation

\# numpy          Go board representation and scoring

If python\-chess is not installed, the Chess domain is silently skipped\. If treys is not installed, the Poker domain is silently skipped\. Go has no external dependencies and always runs\.

## __2\.2  Stockfish__

Chess requires the Stockfish engine binary\. Stockfish is a free, open\-source chess engine and is the strongest chess program in the world\. The benchmark uses it both to generate training data \(self\-play\) and as the test opponent\.

\# Linux / WSL

sudo apt install stockfish

\# macOS

brew install stockfish

\# Windows or custom path

export STOCKFISH\_PATH=/path/to/stockfish

\# or on Windows:

set STOCKFISH\_PATH=C:\\path\\to\\stockfish\.exe

## __2\.3  Cypha__

Cypha\.py must be in the same directory as game\_live\_benchmark\.py\. The benchmark imports CyphaStateful directly\.

\# Directory structure

working\_directory/

    Cypha\.py

    game\_live\_benchmark\.py

\# Run

python game\_live\_benchmark\.py

# __3\. Configuration Reference__

All configuration is at the top of the file\. Edit these constants before running\.

__Constant__

__Default__

__Meaning__

__N\_CHESS\_TRAIN__

200

Number of Stockfish self\-play games to generate training data from\. More games = better training coverage but slower startup\. Each game produces ~50\-150 position pairs depending on game length\.

__N\_CHESS\_TEST__

20

Number of games Cypha plays against Stockfish\. 20 games gives a reasonable statistical picture\. Increase for more confidence\.

__CHESS\_TRAIN\_DEPTH__

18

Stockfish search depth for training game generation\. Deeper = stronger moves = better training signal but much slower generation\.

__CHESS\_TEST\_DEPTH__

20

Stockfish search depth during the test games \(when Stockfish plays Black\)\. This is the opponent strength\.

__CHESS\_SKILL__

20

Stockfish Skill Level 0\-20\. 20 is maximum strength\. Reduce to make the test opponent weaker\.

__CHESS\_NEG\_SAMP__

3

How many non\-optimal moves to label as 'other\_move' per position\. More negatives = sharper discrimination\.

__CHESS\_MAX\_MOVES__

200

Maximum moves per game before declaring a draw\.

__N\_POKER\_TRAIN__

5000

Number of complete hands dealt to generate training data\. Each hand produces ~4 decision points \(one per street\)\.

__N\_POKER\_TEST__

200

Hands Cypha plays against the rule\-based opponent\.

__POKER\_MC\_ITERS__

300

Monte Carlo rollouts per equity calculation during training\. More = more accurate equity but slower training data generation\.

__STARTING\_STACK__

1000

Starting chip stack for each player in the test games\.

__BIG\_BLIND__

10

Big blind size\. Establishes the pot\-odds baseline\.

__N\_GO\_TRAIN__

500

Greedy bot self\-play games for Go training data\.

__N\_GO\_TEST__

30

Games Cypha plays against the greedy bot\.

__GO\_SIZE__

9

Board size\. 9x9 is the default\. This is the standard small\-board format\.

__GO\_KOMI__

6\.5

Komi \(points added to White's score to compensate for Black's first\-move advantage\)\. 6\.5 is standard for 9x9 Chinese rules\.

__STOCKFISH\_PATH__

stockfish

Path to the Stockfish binary\. Default assumes it is on PATH\.

# __4\. How Each Domain Works__

## __4\.1  Chess__

__The task__

Chess is a two\-player perfect\-information game\. The benchmark frames it as a binary classification problem: given a board position and a candidate move, is this the best move available \(label: best\_move\) or not \(label: other\_move\)? Cypha learns to recognise the signatures of strong moves\. During play, it generates a feature string for each legal move and plays whichever one Cypha classifies as best\_move with highest confidence\.

__Training data generation__

Stockfish plays against itself at depth 18 for 200 games\. Before each move, the engine analyses the position and returns the best move from its principal variation\. This move is labelled best\_move\. Three other legal moves chosen at random are labelled other\_move\. This produces roughly 15,000\-25,000 training pairs depending on average game length\.

Each \(board, move\) pair is converted to a feature token string\. The features capture everything a human expert would consider: game phase, material balance, evaluation score, mobility advantage, king safety, pawn structure, and details of the move itself\. The full feature set is:

__phase__

opening / middlegame / endgame\_early / endgame\_late, determined by move number and piece count

__move number__

Full move counter from the game

__pieces__

Total pieces remaining on the board

__mat__

Material difference in centipawns \(pawn=100, knight=320, bishop=330, rook=500, queen=900\)

__eval__

Stockfish evaluation bucket: winning/better/equal/worse/losing

__mob__

White mobility minus Black mobility \(number of legal moves each side has\)

__ks\_w / ks\_b__

King safety: how many enemy pieces are attacking the king

__iso__

Total isolated pawns for both sides

__pass__

White passed pawns \(no enemy pawns blocking or adjacent on adjacent files ahead\)

__piece__

Which piece is being moved \(pawn/knight/bishop/rook/queen/king\)

__to\_region\_r__

Where the piece is going: queenside/center/kingside, and rank number

__cap__

Whether the move captures a piece

__chk__

Whether the move gives check

__cast__

Whether the move is castling

__bonus tokens__

gives\_check, king\_exposed, endgame\_kings, passed\_pawns, mobility\_advantage when applicable

Games start from one of 20 hard\-coded opening sequences \(Ruy Lopez, Sicilian, Queen's Gambit, King's Indian, and others\) to ensure variety in the training positions\.

__How Cypha picks its move during play__

For every legal move on the board, Cypha generates its feature string and calls infer\(\)\. It plays whichever move receives the label best\_move with the highest confidence score\. If no move is classified as best\_move, it falls back to a random legal move\. Cypha uses a quick Stockfish analysis at depth 6 to get the current evaluation score, which it includes in the features — this is a lightweight real\-time evaluation rather than full search\.

__The test opponent__

Stockfish at depth 20, Skill Level 20\. This is the strongest freely available chess engine at near\-maximum strength\. It essentially never makes a mistake\. A win against this opponent is an exceptional result for a system with no explicit lookahead\. Draws are a meaningful achievement\. The benchmark is designed to measure how far pure pattern recognition can get against a search\-based opponent\.

__Scoring__

Win = 1 point, Draw = 0\.5 points, Loss = 0 points\. Score percentage is \(wins \+ 0\.5\*draws\) / games \* 100\. A score above 5% against Stockfish depth\-20 is noteworthy\. The move accuracy probe \(run on a held\-out 15% of training data\) gives a separate measure of how well Cypha learned the labelling task\.

## __4\.2  Poker__

__The task__

Heads\-up no\-limit Texas Hold'em\. Each player starts with 1000 chips\. The game proceeds through four streets: preflop \(no community cards\), flop \(3 cards\), turn \(4 cards\), river \(5 cards\)\. At each street the active player must choose fold, call, or raise\. The benchmark frames this as binary classification: given a game state, is the chosen action the GTO\-optimal action \(best\_action\) or not \(other\_action\)?

__GTO and equity__

GTO stands for Game\-Theory Optimal\. In poker, a GTO strategy is one that cannot be exploited — playing it perfectly means no opponent strategy can win against you in the long run\. The benchmark approximates GTO decisions using real Monte Carlo equity calculation: for a given hand and board, equity is the percentage of runouts where the hero's hand wins at showdown\. This is computed by the treys library, which uses a fast lookup table to evaluate any 5\-card hand\.

The GTO action rule is: raise if equity >= 65%, raise if equity >= 50% and pot odds <= 33%, call if equity >= 38% and pot odds <= 25%, call for drawing hands \(equity >= 28%, pot odds <= 25%, SPR > 4, on flop\), call if equity >= 20% and pot odds <= 15%, fold otherwise\. Pot odds are computed as the bet size divided by total pot after calling\. SPR \(Stack\-to\-Pot Ratio\) is the effective stack divided by the pot\.

__Training data generation__

5,000 complete hands are dealt to showdown\. At each street of each hand, the Monte Carlo equity is computed and the GTO action is determined\. The GTO action is labelled best\_action\. The two non\-optimal actions are labelled other\_action\. This produces roughly 20,000 training pairs\. Each pair includes a rich feature string:

__street__

preflop / flop / turn / river

__pos__

Position: btn \(button\) or bb \(big blind\)

__eq\_bucket__

Equity bucket: strong/ahead/marginal/behind/weak

__equity__

Exact equity percentage from Monte Carlo

__pot__

Current pot size \(capped at 2000 for normalisation\)

__spr__

Stack\-to\-pot ratio

__pot\_odds__

Pot odds percentage for calling the standard bet

__fold\_eq__

Fold equity: how often the opponent needs to fold for a bluff to be profitable

__high / low__

Ranks of the two hole cards

__suited__

Whether the hole cards are the same suit

__connected__

Whether the hole cards are within 2 ranks of each other

__made__

The best made hand on the current board \(preflop, pair, two\_pair, etc\.\)

__stack\_h__

Hero stack size

__board\_cards__

Number of community cards visible

__bonus tokens__

value\_territory, bluff\_territory, short\_stack, connected\_hole, suited\_hole

__How Cypha picks its action during play__

Cypha generates a feature string for each possible action \(fold, call, raise\) and calls infer\(\) on each\. It chooses whichever action is classified as best\_action with highest confidence\. If no action reaches that label, it defaults to call\. Monte Carlo equity is computed at reduced iteration count \(200 vs 300 during training\) to save time during play\.

__The test opponent__

A rule\-based player with fixed thresholds: raise if equity >= 60%, call if equity >= 40%, call if pot odds < 15% and equity >= 25%, otherwise fold\. This opponent is predictable and exploitable — a Cypha model that learns pot odds and position correctly should be able to profit against it over 200 hands\.

__Scoring__

Win rate \(hands won at showdown or by opponent fold\), net chips won or lost over 200 hands, and action accuracy \(how often Cypha chose the GTO\-optimal action on a held\-out probe set\)\. A positive net chip count indicates the strategy is winning\. Win rate above 50% against the rule\-based opponent indicates Cypha is successfully exploiting its predictable tendencies\.

## __4\.3  Go__

__The task__

9x9 Go, Chinese rules with 6\.5 komi for White\. Go is a territory game played on a 9x9 grid\. Players alternately place stones of their colour\. A group of stones with no liberties \(empty adjacent points\) is captured and removed\. The game ends when both players pass consecutively\. The winner is determined by territory \(empty points surrounded by one colour\) plus stones on the board, with White receiving 6\.5 komi points to compensate for Black's first\-move advantage\.

The benchmark uses a pure\-Python Go engine with full rule compliance: stone capture, ko rule \(preventing immediate recapture\), suicide prohibition \(you cannot place a stone that would immediately have no liberties unless it captures\), and superko detection \(preventing repetition of any prior board state\)\.

__The Go engine__

The GoBoard class implements all game logic\. It stores the board as a numpy int8 array \(0=empty, 1=Black, \-1=White\)\. Key methods:

__is\_legal\(r, c, color\)__

Returns True if placing a stone of the given color at \(row, col\) is legal\. Checks bounds, occupancy, ko point, and suicide rule\.

__place\(r, c, color\)__

Places a stone, executes captures, updates ko point and superko history\.

__legal\_moves\(color\)__

Returns all legal \(row, col\) positions for a given colour\.

__score\(\)__

Computes Chinese scoring: flood\-fills empty regions to assign territory, counts stones on board, adds komi\. Returns \(black\_score, white\_score, black\_territory, white\_territory\)\.

__\_liberties\(r, c\)__

BFS flood\-fill to find the group containing \(r,c\) and count its liberties\.

__Training data generation__

500 games are played between two greedy bots\. The greedy bot evaluates each legal move using a simple score: \+10 per opponent stone captured, \+4 for putting an opponent group in atari \(1 liberty\), \+1 per liberty the placed stone would have, minus a distance\-from\-center penalty, plus a small random tiebreak\.

After each game, the winner is determined by final territory count\. All moves played by the winning side are labelled best\_move\. All moves played by the losing side are labelled other\_move\. This is credit assignment by game outcome — a simple but effective signal that Cypha should learn to play like the winner, not the loser\.

For each best\_move in the training data, two random alternative legal moves are added as other\_move examples\. This ensures the training set has contrast: Cypha sees both what the winner played and what the winner could have played but did not\.

Each \(board, move\) pair is converted to a feature token string:

__mv__

Move number in the game

__phase__

opening \(<15 moves\) / middle \(15\-60\) / endgame \(60\-120\) / yose \(120\+\)

__b\_stones / w\_stones / total__

Stone counts for each colour

__score__

Current score bucket: b\_winning/b\_ahead/even/w\_ahead/w\_winning

__b\_terr / w\_terr__

Territory count for each colour at current position

__move\_row / move\_col / region__

Where the move is: corner/edge/center

__own\_libs__

How many liberties the placed stone would have \(capped at 8\)

__captures__

How many opponent stones this move captures

__opp\_atari__

How many adjacent opponent groups this move puts in atari

__caps\_b / caps\_w__

Running capture totals for each player

__color__

Whether Cypha is playing Black or White

__bonus tokens__

capturing\_move, threatening\_capture, safe\_group, in\_danger, center\_play

__How Cypha picks its move during play__

Cypha is tested as Black\. For each move, up to 20 candidate legal moves are sampled \(to limit computation on the full 81\-move board\)\. Each candidate is scored via infer\(\) and Cypha plays the one classified as best\_move with highest confidence\. If none are classified as best\_move, Cypha falls back to the greedy bot heuristic\.

__The test opponent__

The same greedy territory bot used for training game generation\. It is locally strong — it always captures when possible and threatens atari — but it has no global strategic vision and no territory consolidation\. Cypha's win condition is to learn the patterns of global territory control that the greedy bot misses\.

__Scoring__

Win/Draw/Loss by final Chinese scoring \(territory \+ stones \+ komi\)\. Win rate is wins divided by games played\. Each result is reported with the exact margin in points\.

# __5\. The Training Pipeline__

All three domains use the same generic training function after data collection\. The collected \(feature\_string, label\) pairs are shuffled, and 85% are used for training with the remaining 15% reserved for the probe accuracy measurement\.

Training calls cypha\.\_cypha\.train\_step\(feature\_string, label\) for each pair\. This is a single\-pass online training loop — Cypha processes each example once and moves on\. There is no second epoch, no validation\-based early stopping, and no gradient computation\. Each train\_step updates the AnchorMemory store, the HippoCypha episodic memory, the TensorCentroid for the correct class, and runs LVQ2\.1 boundary sharpening\.

\# Training loop \(simplified\)

pairs = collect\_training\_data\(\)

random\.shuffle\(pairs\)

train\_pairs  = pairs\[:int\(len\(pairs\)\*0\.85\)\]

probe\_pairs  = pairs\[int\(len\(pairs\)\*0\.85\):\]

for feature\_string, label in train\_pairs:

    cypha\.\_cypha\.train\_step\(feature\_string, label\)

\# Probe accuracy on held\-out 15%

for feature\_string, label in random\.sample\(probe\_pairs, 2000\):

    predicted\_label, confidence = cypha\.infer\(feature\_string\)

The probe accuracy report shows overall move accuracy, best\_move/best\_action recall \(how often Cypha correctly identifies optimal moves\), and other\_move recall \(how often Cypha correctly rejects non\-optimal moves\)\. A high other\_move recall with slightly lower best\_move recall is normal — there are typically 2\-3 negative examples per positive, making negatives easier to recall\.

__Important__

Each domain uses a completely separate CyphaStateful instance stored in a temporary checkpoint directory\. Chess, Poker, and Go never share weights\. This is essential — the feature vocabularies are completely different and sharing would produce garbage representations\.

# __6\. How Cypha Makes Decisions During Play__

The decision logic is the same for all three games\. For each possible action \(move, action, or stone placement\), Cypha generates the domain\-specific feature string and calls infer\(\)\. The action with the highest confidence of being classified as best\_move or best\_action is chosen\.

\# Pseudocode for all three domains

best\_action = None

best\_confidence = \-1\.0

for candidate in all\_possible\_actions:

    features = domain\_feature\_extractor\(state, candidate\)

    label, confidence = cypha\.infer\(features\)

    if label == 'best\_move' and confidence > best\_confidence:

        best\_confidence = confidence

        best\_action = candidate

if best\_action is None:

    best\_action = fallback\(\)   \# random legal move / greedy bot / call

This approach has a key property: Cypha never explicitly searches the game tree\. It has no minimax, no alpha\-beta, no rollouts\. Every decision is made by pattern\-matching the current state against learned representations of strong play\. The GRIA deliberation engine inside Cypha handles ambiguous cases by running multi\-stage ensemble methods, but none of these simulate future game states — they all operate within the feature space of the current position\.

For chess, this is the defining challenge\. Stockfish wins games by searching 20 moves deep\. Cypha wins games \(if it does\) by recognising the positional signature of a good move without any forward planning\. The question the benchmark answers is: how much of chess skill is pattern recognition versus calculation?

# __7\. Output Format__

The benchmark prints progress during training and testing, then produces a final summary report\. Here is what each section means:

__Training progress__

  Training Cypha\-chess on 18,432 examples\.\.\.

   18,432/18,432  4,211/s

  Training done: 4\.4s  \(0\.24 ms/example\)

Shows training throughput in examples per second and total time\. 0\.24 ms/example is the expected cost for a full Cypha train\_step including AnchorMemory updates and LVQ boundary sharpening\.

__Probe accuracy__

  \[chess\] Move accuracy: 87\.3%  \(best\_recall=84\.1%  other\_recall=90\.5%\)

Overall accuracy on 2,000 held\-out training examples\. best\_recall is how often Cypha correctly identifies the optimal move\. other\_recall is how often Cypha correctly rejects a non\-optimal move\. This reflects training quality, not game strength — a high probe accuracy does not guarantee wins\.

__Chess test progress__

  game  1/20  1\-0  \[W=1 D=0 L=0\]  142s

  game  2/20  0\-1  \[W=1 D=0 L=1\]  289s

  game  3/20  1/2  \[W=1 D=1 L=1\]  401s

Game\-by\-game results\. 1\-0 = White wins \(Cypha wins\), 0\-1 = Black wins \(Stockfish wins\), 1/2 = draw\. Running totals shown\.

__Poker test progress__

   hand  50/200  W=18 D=3 L=29  net=\+124 chips  38s

Running totals every 50 hands\. Net chips is the running profit/loss from Cypha's perspective\.

__Go test progress__

  game  1/30  B\+4\.5  B=42\.5 W=38\.0  \[W=1 D=0 L=0\]  8s

  game  2/30  W\+2\.5  B=37\.0 W=39\.5  \[W=1 D=0 L=1\]  16s

B\+N\.N means Black \(Cypha\) won by N\.N points\. W\+N\.N means White \(greedy bot\) won\. B= and W= are the raw scores including komi\.

__Final summary__

  FINAL RESULTS — ALL GAMES

  CHESS  \(Cypha White vs Stockfish depth 20 skill 20/20\)

     Move accuracy  : 87\.3%

     Games played   : 20

     Wins / Draws / Losses  : 2 / 3 / 15

     Score \(W\+half D\)  : 3\.5 / 20  \(17\.5%\)

     Results  : 0\-1 1\-0 1/2 \.\.\.

  POKER  \(Cypha vs rule\-based opponent, 200 hands\)

     Action accuracy: 91\.2%

     Hands played   : 200

     Wins / Draws / Losses  : 88 / 12 / 100

     Win rate       : 44\.0%

     Net chips      : \+340

  GO  \(Cypha Black vs greedy White, 9x9 Chinese rules\)

     Move accuracy  : 79\.4%

     Games played   : 30

     Wins / Draws / Losses  : 22 / 0 / 8

     Win rate       : 73\.3%

# __8\. Interpreting Results__

__Chess: any wins__

Exceptional\. Stockfish at depth\-20 skill\-20 is close to perfect play\. Any win by a pattern\-matching system with no search tree is a significant result\.

__Chess: draws__

Strong result\. A draw against maximum\-strength Stockfish means Cypha avoided losing material and found a solid position Stockfish could not break through\.

__Chess: score > 10%__

Cypha is finding genuinely strong moves and avoiding obvious blunders\. Most systems without lookahead score under 5% against Stockfish at this level\.

__Poker: positive net chips__

Cypha is making profitable decisions\. The rule\-based opponent is exploitable \(it is too tight: folds equity >= 60% but calls down with less\), and a positive net shows Cypha has identified profitable bet/fold spots\.

__Poker: win rate ~44\-50%__

Expected range\. Poker has high variance per hand\. Win rate alone is less meaningful than net chips over 200 hands\.

__Poker: action accuracy > 85%__

Cypha has learned the GTO logic accurately\. Equity and pot odds are well\-represented in the feature space\.

__Go: win rate > 60%__

Cypha has learned meaningful territory patterns that outperform the greedy heuristic\. The greedy bot is locally strong but strategically blind\.

__Go: win rate > 80%__

Cypha is consistently making globally superior moves\. It has learned to consolidate territory rather than chase local exchanges\.

__Go: move accuracy__

Lower than chess or poker because the credit assignment is noisy — the winner's moves were labelled good regardless of whether individual moves were optimal\. Accuracy in the 70\-85% range is normal and does not reflect game strength directly\.

# __9\. Common Issues__

Stockfish not found: The benchmark will print 'ERROR: Stockfish not found at stockfish' and skip the chess domain\. Install stockfish via apt/brew or set the STOCKFISH\_PATH environment variable\.

python\-chess not installed: The chess domain silently skips\. Run: pip install python\-chess

treys not installed: The poker domain silently skips\. Run: pip install treys

Slow training data generation: Training data generation \(especially chess at depth 18\) can be slow on older hardware\. Chess generates ~200 games at depth 18 — reduce N\_CHESS\_TRAIN or CHESS\_TRAIN\_DEPTH if it is too slow\. Poker MC equity at 300 iterations per decision is the other bottleneck — reduce POKER\_MC\_ITERS to 100 for faster generation with slightly less accurate training labels\.

Chess games very short or all losses: Normal\. Without lookahead, Cypha can fall into tactical traps that Stockfish exploits immediately\. The interesting question is how many draws or wins emerge from the games where Cypha reaches a solid middlegame\.

# __10\. Files and Cleanup__

Each Cypha instance creates a temporary checkpoint directory to persist its weights between training and testing\. These directories are created in the system temporary folder with the prefix cypha\_games\_ and are automatically deleted at the end of the run via shutil\.rmtree\(\)\.

If the benchmark crashes mid\-run, temporary directories may be left behind\. They can be safely deleted:

\# Linux / macOS

rm \-rf /tmp/cypha\_games\_\*

\# Windows

del /s /q %TEMP%\\cypha\_games\_\*

*game\_live\_benchmark\.py   Cypha HRNA   February 2026   All rights reserved*

