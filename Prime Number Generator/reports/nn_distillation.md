# Knowledge distillation: NN → tree, NN → sparse logistic

For each scale we trained a depth-8 decision tree and an L1-regularised logistic regression to mimic the trained MLP, using the NN's own predictions as the teacher target. Tables below show how faithfully each surrogate reproduces the NN, and which input features the surrogate ends up using.

## Fidelity summary

| scale | NN acc | NN AUC | tree → NN | tree AUC | tree leaves | logit → NN | logit AUC | logit nz coefs |
|------:|------:|------:|--------:|--------:|------------:|---------:|--------:|--------------:|
| 3 | 0.7850 | 0.8341 | 0.8350 | 0.9256 | 14 | 0.8900 | 0.8559 | 43 |
| 4 | 0.7333 | 0.8301 | 0.7683 | 0.9155 | 15 | 0.8217 | 0.8487 | 44 |
| 5 | 0.7333 | 0.8308 | 0.7700 | 0.9213 | 14 | 0.8083 | 0.8422 | 45 |
| 6 | 0.7550 | 0.8355 | 0.8000 | 0.8971 | 14 | 0.8333 | 0.8433 | 42 |
| 7 | 0.7433 | 0.8317 | 0.7917 | 0.8880 | 13 | 0.8117 | 0.8344 | 45 |
| 8 | 0.7367 | 0.8098 | 0.7733 | 0.8930 | 13 | 0.8067 | 0.8221 | 49 |

## Decision-tree top features by scale

### scale s = 3

| feature | group | importance |
|:--------|:------|----------:|
| `is_6k_pm1` | sieve | 0.4789 |
| `res_5` | residue | 0.2175 |
| `res_7` | residue | 0.1351 |
| `res_11` | residue | 0.0489 |
| `res_13` | residue | 0.0390 |
| `res_17` | residue | 0.0389 |
| `res_29` | residue | 0.0187 |
| `res_19` | residue | 0.0166 |
| `mod30` | wheel | 0.0048 |
| `res_101` | residue | 0.0012 |

### scale s = 4

| feature | group | importance |
|:--------|:------|----------:|
| `is_6k_pm1` | sieve | 0.4224 |
| `res_5` | residue | 0.1811 |
| `res_7` | residue | 0.1536 |
| `res_13` | residue | 0.0671 |
| `res_11` | residue | 0.0575 |
| `res_17` | residue | 0.0532 |
| `res_23` | residue | 0.0344 |
| `res_19` | residue | 0.0269 |
| `res_83` | residue | 0.0018 |
| `res_107` | residue | 0.0013 |

### scale s = 5

| feature | group | importance |
|:--------|:------|----------:|
| `is_6k_pm1` | sieve | 0.4277 |
| `res_5` | residue | 0.1992 |
| `res_7` | residue | 0.1155 |
| `res_11` | residue | 0.0736 |
| `res_13` | residue | 0.0662 |
| `res_19` | residue | 0.0505 |
| `res_17` | residue | 0.0338 |
| `res_23` | residue | 0.0304 |
| `res_71` | residue | 0.0020 |
| `res_61` | residue | 0.0006 |

### scale s = 6

| feature | group | importance |
|:--------|:------|----------:|
| `is_6k_pm1` | sieve | 0.4625 |
| `res_5` | residue | 0.2227 |
| `res_7` | residue | 0.1143 |
| `res_13` | residue | 0.0704 |
| `res_11` | residue | 0.0526 |
| `res_19` | residue | 0.0285 |
| `res_23` | residue | 0.0259 |
| `res_17` | residue | 0.0218 |
| `mod30` | wheel | 0.0009 |
| `log2_n` | scale | 0.0003 |

### scale s = 7

| feature | group | importance |
|:--------|:------|----------:|
| `is_6k_pm1` | sieve | 0.4614 |
| `res_5` | residue | 0.2039 |
| `res_7` | residue | 0.1437 |
| `res_13` | residue | 0.0545 |
| `res_11` | residue | 0.0506 |
| `res_19` | residue | 0.0353 |
| `res_29` | residue | 0.0249 |
| `res_43` | residue | 0.0240 |
| `res_83` | residue | 0.0010 |
| `log2_n` | scale | 0.0004 |

### scale s = 8

| feature | group | importance |
|:--------|:------|----------:|
| `is_6k_pm1` | sieve | 0.4670 |
| `res_5` | residue | 0.1947 |
| `res_7` | residue | 0.1341 |
| `res_13` | residue | 0.0528 |
| `res_17` | residue | 0.0484 |
| `res_11` | residue | 0.0449 |
| `res_19` | residue | 0.0332 |
| `res_37` | residue | 0.0204 |
| `res_43` | residue | 0.0038 |
| `res_53` | residue | 0.0005 |

## L1-logistic top features by scale

### scale s = 3

| feature | group | coefficient |
|:--------|:------|-----------:|
| `is_6k_pm1` | sieve | +3.1362 |
| `res_5` | residue | +1.5459 |
| `res_7` | residue | +0.6399 |
| `mod30` | wheel | -0.6366 |
| `last_digit` | digits | -0.4482 |
| `res_17` | residue | +0.3754 |
| `res_11` | residue | +0.3257 |
| `mod6` | wheel | +0.2896 |
| `res_13` | residue | +0.2837 |
| `res_37` | residue | +0.2072 |

### scale s = 4

| feature | group | coefficient |
|:--------|:------|-----------:|
| `is_6k_pm1` | sieve | +2.7313 |
| `res_5` | residue | +1.2264 |
| `mod30` | wheel | -0.6975 |
| `res_7` | residue | +0.4680 |
| `last_digit` | digits | -0.3547 |
| `res_11` | residue | +0.2563 |
| `mod6` | wheel | +0.2286 |
| `res_13` | residue | +0.2076 |
| `res_53` | residue | +0.2069 |
| `res_19` | residue | +0.2028 |

### scale s = 5

| feature | group | coefficient |
|:--------|:------|-----------:|
| `is_6k_pm1` | sieve | +2.6825 |
| `res_5` | residue | +1.3040 |
| `mod30` | wheel | -0.6268 |
| `res_7` | residue | +0.5091 |
| `last_digit` | digits | -0.3665 |
| `res_19` | residue | +0.2534 |
| `res_11` | residue | +0.2426 |
| `res_13` | residue | +0.2172 |
| `res_3` | residue | +0.1986 |
| `res_53` | residue | +0.1490 |

### scale s = 6

| feature | group | coefficient |
|:--------|:------|-----------:|
| `is_6k_pm1` | sieve | +2.8625 |
| `res_5` | residue | +1.3698 |
| `mod30` | wheel | -0.6575 |
| `res_7` | residue | +0.5489 |
| `res_13` | residue | +0.3576 |
| `last_digit` | digits | -0.3391 |
| `res_11` | residue | +0.2999 |
| `mod6` | wheel | +0.2234 |
| `res_41` | residue | +0.2006 |
| `res_17` | residue | +0.1826 |

### scale s = 7

| feature | group | coefficient |
|:--------|:------|-----------:|
| `is_6k_pm1` | sieve | +2.6767 |
| `res_5` | residue | +1.2883 |
| `mod30` | wheel | -0.5344 |
| `res_7` | residue | +0.5204 |
| `last_digit` | digits | -0.4088 |
| `res_11` | residue | +0.2875 |
| `mod6` | wheel | +0.1767 |
| `res_13` | residue | +0.1657 |
| `res_19` | residue | +0.1329 |
| `res_83` | residue | +0.1275 |

### scale s = 8

| feature | group | coefficient |
|:--------|:------|-----------:|
| `is_6k_pm1` | sieve | +2.5067 |
| `res_5` | residue | +1.1709 |
| `mod30` | wheel | -0.6364 |
| `res_7` | residue | +0.4758 |
| `last_digit` | digits | -0.2716 |
| `res_11` | residue | +0.2322 |
| `res_13` | residue | +0.1967 |
| `res_3` | residue | +0.1806 |
| `res_17` | residue | +0.1632 |
| `res_19` | residue | +0.1381 |
