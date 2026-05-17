# Conventional vs NN-augmented vs pure-NN prime generation

Each row is the average over `K = 50` random starting points × `M = 5` consecutive primes per start.  Pure-NN threshold τ = 0.5.

`ms/prime` is the wall-clock cost per produced prime; `cand/prime` is the number of 6k±1 candidates examined per produced prime; `accept_rate` is the fraction of candidates that pass the filter.

## Conventional

| scale | ms/prime | cand/prime | accept_rate | bad |
|------:|---------:|-----------:|------------:|----:|
| 3 | 0.006 | 1.88 | 0.532 | 0 |
| 4 | 0.009 | 2.85 | 0.434 | 0 |
| 5 | 0.019 | 4.85 | 0.432 | 0 |
| 6 | 0.020 | 4.56 | 0.456 | 0 |
| 7 | 0.023 | 4.94 | 0.456 | 0 |
| 8 | 0.030 | 5.64 | 0.449 | 0 |

## NN-augmented (NN filter + deterministic verifier)

| scale | ms/prime | cand/prime | accept_rate | bad |
|------:|---------:|-----------:|------------:|----:|
| 3 | 0.367 | 1.88 | 0.794 | 0 |
| 4 | 0.751 | 4.04 | 0.461 | 0 |
| 5 | 1.013 | 5.32 | 0.502 | 0 |
| 6 | 0.986 | 5.20 | 0.563 | 0 |
| 7 | 1.594 | 8.42 | 0.430 | 0 |
| 8 | 1.558 | 7.74 | 0.561 | 0 |

## Pure-NN (NN scoring only, no verifier)

| scale | ms/value | cand/value | primality_recall | skip_rate |
|------:|---------:|-----------:|-----------------:|----------:|
| 3 | 0.235 | 1.22 | 0.6840 | 0.0000 |
| 4 | 0.441 | 2.34 | 0.4040 | 0.2240 |
| 5 | 0.451 | 2.27 | 0.4680 | 0.0200 |
| 6 | 0.347 | 1.71 | 0.3520 | 0.0360 |
| 7 | 0.491 | 2.28 | 0.2600 | 0.1440 |
| 8 | 0.378 | 1.83 | 0.2120 | 0.0960 |

## Speed ratio (NN-augmented / conventional)

| scale | conv ms | NN-aug ms | ratio |
|------:|--------:|---------:|------:|
| 3 | 0.006 | 0.367 | 66.4× |
| 4 | 0.009 | 0.751 | 83.2× |
| 5 | 0.019 | 1.013 | 53.5× |
| 6 | 0.020 | 0.986 | 50.4× |
| 7 | 0.023 | 1.594 | 68.0× |
| 8 | 0.030 | 1.558 | 52.1× |