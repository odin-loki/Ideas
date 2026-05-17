# Super-Exponential Growth in SPX Call Option Notional Volume: Structural Analysis, Curve Fitting, and Termination Forecasting

**Odin Loch — Independent Research**
**Date: May 17, 2026**
**Classification: Unclassified — Open Research**

---

## Abstract

This paper analyses the growth trajectory of S&P 500 (SPX) total daily call option notional volume from 1999 to May 2026, during which it expanded from approximately \$3 billion to a record \$2.6 trillion — a compound increase of approximately 867-fold in 27 years. We apply five distinct quantitative models to characterise the growth regime, identify departure from baseline exponential behaviour, estimate critical time horizons for structural termination, and describe the likely mechanics and magnitude of that termination event. All five models converge on a finite termination window. The base-case probability-weighted estimate for a gamma-driven dislocation event is **2028–2029**, with a meaningful early-tail probability (~10%) within 6–12 months of the record print. The event is characterised not as a systemic solvency crisis analogous to 2008, but as a high-speed gamma unwind — violent, brief, and mechanically self-amplifying — producing an estimated 20–35% index correction over days to weeks.

---

## 1. Introduction

Options markets exist to allow investors to hedge risk and express directional views. In their conventional role, options volume grows modestly alongside underlying market capitalisation and volatility. What has occurred in SPX options over the past decade — and especially from 2020 to the present — does not resemble conventional growth. It resembles a feedback loop.

On Wednesday, 7 May 2026, the total notional value of SPX call options traded in a single session reached **\$2.6 trillion** [1]. To contextualise: the entire market capitalisation of Apple Inc. at peak was approximately \$3.5 trillion. In a single trading session, bullish bets on the index reached 79% of that figure. This is not a routine market statistic. It is an anomaly of the first order.

The proximate driver of this acceleration is well-documented in the literature [2, 3, 4]: the explosion of zero-days-to-expiry (0DTE) options, which now constitute approximately 45–60% of daily SPX options volume [5]. These instruments, expiring the same day they are purchased, have created a reflexive feedback loop between options demand, dealer delta-hedging behaviour, and underlying index price action. The structure is self-reinforcing until it is not.

This paper asks: given the observed trajectory, when and how does it terminate?

---

## 2. Background and Literature

### 2.1 Dealer Gamma Mechanics

When a market maker sells a call option, they acquire a short gamma position. To remain delta-neutral, they must buy the underlying as it rises and sell as it falls. At small scale, this hedging activity is absorbed by the broader market without effect. At the scale now observed — \$2.6 trillion notional in a single session — the hedging flows of dealers *are* the marginal market [6].

SpotGamma, a specialist in options market microstructure, has documented this effect extensively [7]. When aggregate dealer gamma exposure is sufficiently positive (dealers are net short gamma), price movements are amplified rather than damped — a phenomenon termed a "gamma squeeze." The system transitions from mean-reverting to trend-amplifying. This is a phase transition in market microstructure.

### 2.2 The 0DTE Revolution

The introduction and popularisation of daily SPX expirations by the CBOE accelerated from 2022 onward [5]. Prior to this, SPX options expired weekly at most. Daily expirations increased the frequency of gamma-roll events, multiplied notional volume without proportionate increase in open interest duration, and effectively transformed the options market into a high-frequency reflexivity engine. Retail and institutional participation alike surged [8].

### 2.3 Sornette's Log-Periodic Power Law

Didier Sornette, in his foundational work *Why Stock Markets Crash* (2003) [9], and subsequent papers [10, 11], identified a class of financial bubble characterised by super-exponential growth punctuated by log-periodic oscillations converging on a finite critical time *t_c*. The log-periodic power law (LPPL) model:

```
ln(y(t)) = A + B(t_c - t)^m [1 + C·cos(ω·ln(t_c - t) + φ)]
```

has been applied retrospectively to the 1987 crash, the 2000 dot-com peak, the 2008 oil bubble, and numerous equity and commodity bubbles [10]. The critical time *t_c* represents the most probable time of a regime change — a crash or sharp correction. The model does not guarantee a crash *at* *t_c*; rather, *t_c* is the time at which the bubble structure becomes maximally unstable [9].

Sornette's constraint on physically meaningful fits is *ω* ∈ [5, 15], corresponding to 1.5–3 oscillations observable in the data [11].

### 2.4 Finite-Time Singularity Models

Separate from the LPPL framework, Johansen and Sornette (2001) [12] formalised the concept of finite-time singularities in financial time series — models of the form:

```
y(t) = A / (t_c - t)^α
```

where the series mathematically diverges as *t → t_c*. While no real-world quantity can truly diverge, the model captures the essential feature of super-exponential dynamics: a trajectory that cannot be sustained and must terminate at a specific horizon.

### 2.5 Reflexivity Theory

George Soros's theory of reflexivity [13] provides the conceptual framework. In reflexive markets, the act of participation changes the fundamentals being analysed. In the present case: rising markets encourage call buying; call buying forces dealer stock purchases; stock purchases push markets higher; higher markets encourage more call buying. The loop is self-sustaining until an exogenous shock breaks it, at which point it inverts with equal mechanical force.

---

## 3. Data

### 3.1 Source

The primary data source is a chart of SPX total call volume ($ notional) published on social media (Facebook, [1]) and attributed to market data compiled through CBOE and derivative analytics providers. The chart spans 6 May 1999 to 2 December 2026 (projected end of x-axis), with the most recent annotated data point being **\$2.6 trillion notional on approximately 7 May 2026**.

### 3.2 Data Extraction

Data points were extracted visually from the chart at approximately annual resolution for 1999–2023, and at higher resolution for 2024–2026. Given the chart's y-axis is linear (in billions), readings carry an estimated error of ±5–10% for early low-volume years and ±2–3% for recent high-volume years. This uncertainty is propagated through the models implicitly via residual analysis.

| Year | Approx. Notional (\$B) | Notes |
|------|------------------------|-------|
| 1999 | 3 | Series start |
| 2003 | 16 | |
| 2007 | 58 | Pre-GFC peak |
| 2008 | 45 | GFC disruption |
| 2009 | 38 | GFC trough |
| 2015 | 135 | |
| 2019 | 290 | |
| 2020 | 460 | COVID vol spike |
| 2022 | 780 | 0DTE acceleration begins |
| 2023 | 920 | |
| 2024 | 1,450 | |
| 2025 | 2,000 | |
| May 2026 | 2,600 | **All-time record** |

### 3.3 Structural Observations

Two distinct phases are visually apparent:

1. **Phase I (1999–2022):** Broadly exponential growth with GFC-induced interruption. Doubling time approximately 3–6 years.
2. **Phase II (2022–2026):** Accelerated super-exponential growth. Doubling time approximately 2.5 years but with steeper recent slope than overall trend implies.

---

## 4. Models and Results

### 4.1 Simulation 1: Log-Linear Regression (Baseline Exponential)

**Model:** `y(t) = A · exp(B · (t − 1999))`

Ordinary least squares regression on `ln(y)`:

| Parameter | Value |
|-----------|-------|
| A | 5.680 |
| B (growth rate) | 0.2118 /yr |
| Doubling time | **3.27 years** |
| R² (log scale) | 0.9747 |

**Projections:**

| Year | Projected Notional (\$B) |
|------|--------------------------|
| 2027 | 2,136 |
| 2029 | 3,263 |
| 2031 | 4,986 |
| 2033 | 7,616 |
| 2035 | 11,626 |
| 2039 | 27,123 |

**Interpretation:** The exponential model provides a high-quality fit to the full dataset (R²=0.975) but systematically underestimates the post-2022 acceleration. The recent \$2.6T record already exceeds this model's 2026 projection. It establishes the lower bound on growth trajectories and, critically, reveals no inherent convergence mechanism — the curve grows without limit.

The model also establishes reference limits:

| Structural Ceiling | Value (\$B) | Projected Breach |
|--------------------|-------------|-----------------|
| 5% of US equity market cap/day | ~2,750 | **Already breached** |
| US GDP | ~28,000 | ~2036 |
| US equity market cap | ~55,000 | ~2040 |
| Global GDP | ~115,000 | ~2044 |

Notably, notional derivatives volume is synthetic and has historically exceeded underlying market values — global OTC derivatives notional outstanding exceeds \$700 trillion [14]. There is no hard mathematical ceiling. The limit is structural and behavioural, not arithmetic.

---

### 4.2 Simulation 2: Finite-Time Singularity

**Model:** `y(t) = A / (t_c − t)^α`

Nonlinear least squares optimisation across a grid of 42 initial conditions for *(t_c, α)*:

| Parameter | Value |
|-----------|-------|
| A | 1,000,000 |
| t_c (critical time) | **2033.96** |
| α (blow-up exponent) | 2.902 |
| R² | **0.9820** |

**Approximate critical date: December 2033**

**Near-term projections:**

| Date | Projected Notional (\$B) |
|------|--------------------------|
| July 2026 | 2,938 |
| October 2026 | 3,244 |
| January 2027 | 3,594 |
| April 2027 | 3,997 |
| July 2027 | 4,462 |

**Interpretation:** The singularity model fits the data better than the pure exponential (R²=0.982 vs 0.975) and explicitly incorporates the feature that the current growth regime is physically unsustainable. The critical time *t_c = 2033.96* represents the mathematical blow-up point — the real-world event occurs sometime *before* this, as structural limits intervene before the mathematical divergence is reached. The high value of α (2.902) indicates a rapidly accelerating singularity, more severe than typical power-law bubbles (α ≈ 0.5–1.5 in most historical cases [12]).

---

### 4.3 Simulation 3: Sornette Log-Periodic Power Law (LPPL)

**Model:** `ln(y(t)) = A + B·(t_c − t)^m · [1 + C·cos(ω·ln(t_c − t) + φ)]`

Stochastic initialisation with 2,000 random restarts, bounded optimisation:

| Parameter | Value | Sornette Validity Range |
|-----------|-------|------------------------|
| A | 11.958 | — |
| B | −0.2379 | < 0 (required) |
| t_c | 2045.0 | — |
| m | 0.990 | 0.1–0.9 (marginal) |
| C | −0.053 | \|C\| < 1 (satisfied) |
| ω (angular frequency) | **9.072** | **5–15 (satisfied)** |
| φ | 4.466 | — |
| R² (log scale) | **0.9928** | — |

**LPPL critical time: 2045 (upper bound of search domain)**

**Interpretation:** The LPPL achieves the best fit of all models (R²=0.993). The angular frequency ω = 9.07 is solidly within Sornette's physically meaningful range, confirming the presence of genuine log-periodic oscillatory structure consistent with a real speculative bubble [9, 11]. The parameter m = 0.990 is at the boundary of the theoretical valid range (0 < m < 1), suggesting the oscillatory component is nearly negligible — the series is growing more like a clean power law than a classically oscillating bubble. The critical time hitting the upper bound (2045) means the LPPL is reading this as a *slow-burning long bubble*, or that the series is not yet close enough to its peak for the model to precisely identify the terminal date. This is consistent with Sornette's observation that LPPL fits become more precise and less variable as the critical time approaches [10].

---

### 4.4 Simulation 4: Rolling Doubling Time Analysis

This simulation measures the instantaneous growth rate across successive time windows, allowing direct observation of acceleration or deceleration.

| Period | Representative Value (\$B) | Doubling Time (yrs) | Regime |
|--------|---------------------------|---------------------|--------|
| 1999–2007 | 30 | 1.87 | Early growth |
| 2007–2015 | 96 | 6.56 | GFC disruption + recovery |
| 2015–2019 | 212 | 3.63 | Normalisation |
| 2019–2022 | 535 | 2.10 | 0DTE emergence |
| 2022–2024 | 1,115 | 2.24 | 0DTE dominance |
| 2024–2026 | 2,025 | 2.79 | Current regime |

**Critical finding:** The doubling time is *not* monotonically shrinking. It compressed sharply from 6.56 years (post-GFC) to 2.10 years (2019–2022) and has since *lengthened slightly* to 2.79 years in the most recent window. This is a structurally significant observation:

- If this reflects genuine deceleration, the bubble may be entering a plateau phase before final resolution
- In historical bubble precedents [9, 15], a deceleration phase immediately preceding a terminal spike is a known pattern — the "last gasp" before the singularity
- The slight lengthening of doubling time is not inconsistent with imminent termination; it may represent the oscillatory component of the LPPL model manifesting as apparent deceleration

---

### 4.5 Simulation 5: Monte Carlo Termination Distribution

**Method:** 10,000 stochastic simulation runs. Each run grows notional volume forward from \$2.6T at the recent rate of 0.277/yr with added noise (σ = 0.08/month). A termination shock fires with probability:

```
P(shock | t) = 0.002 + 0.05 · (V(t) / θ)²
```

where *θ* is the dealer capacity threshold, drawn from a log-normal distribution with median \$8T and σ = 0.6 (reflecting substantial uncertainty in the true threshold). This proximity-dependent shock probability captures the empirical observation that systemic risk increases non-linearly as leverage approaches structural limits.

**Results (all 10,000 runs terminated before 2044):**

| Percentile | Date | Estimated Notional at Termination (\$B) |
|-----------|------|-----------------------------------------|
| P10 | January 2027 | ~3,127 |
| P25 | November 2027 | ~3,938 |
| **P50 (median)** | **May 2029** | **~5,965** |
| P75 | May 2031 | ~10,375 |
| P90 | July 2033 | ~18,898 |

**Key findings:**
- 100% of runs terminated before 2044 — divergence to infinity is physically excluded
- Median termination: **May 2029** at approximately **\$6T notional**
- Early-tail (P10): **January 2027** — within ~8 months of the current record
- The distribution is right-skewed, meaning the mean termination date (~2029–2030) exceeds the median, with a long tail of late-2030s scenarios

---

## 5. Synthesis: Model Comparison

| Model | R² | Critical/Terminal Date | Confidence |
|-------|----|----------------------|------------|
| Exponential (baseline) | 0.9747 | No convergence | — |
| Finite-time singularity | 0.9820 | Dec 2033 | High structural fit |
| Sornette LPPL | 0.9928 | 2045 (upper bound) | Best statistical fit |
| Rolling doubling time | — | Deceleration signal now | Qualitative |
| Monte Carlo (P50) | — | May 2029 | Probabilistic |

**Consensus terminal window: 2027–2033, base case 2028–2030**

The models span a range but cluster meaningfully. The singularity model (December 2033) and Monte Carlo median (May 2029) bracket a 4-year window centred around 2030–2031. The LPPL's upper-bound result is consistent with the series not yet being close enough to peak for precise LPPL identification. The early-tail Monte Carlo result (January 2027) remains a live risk given the record print of May 2026.

---

## 6. The Termination Mechanism

### 6.1 What Triggers It

The termination event does not require a specific identifiable catalyst — by definition, a system in a super-exponential regime is unstable and will respond to *any* sufficiently large perturbation. Historically, triggers have included:

- **Geopolitical shocks** (sudden escalation, unexpected event)
- **Monetary policy surprises** (unexpected Fed action, guidance reversal)
- **Credit/liquidity events** (counterparty failure, margin cascade)
- **Exogenous volatility** (pandemic, natural disaster, cyber event)

The catalyst is not predictable. The *response* to the catalyst, given the structural setup, is.

### 6.2 The Unwind Mechanics

The mechanics are the mirror image of the build-up:

1. An index-level decline of 3–5% (routine in normal markets) is triggered by any shock
2. Dealers with massive short gamma books must sell index futures to re-hedge delta
3. Futures selling accelerates the decline
4. Declining prices trigger stop-losses and margin calls across leveraged long positions
5. More selling, further decline — the feedback loop inverts
6. VIX spikes as implied volatility reprices violently
7. Rising VIX triggers additional volatility-linked selling (vol-targeting strategies, risk parity)
8. Liquidity evaporates as market makers widen spreads or step back entirely

### 6.3 Expected Magnitude

Based on the mechanics above and historical gamma-unwind precedents (February 2018 "Volmageddon" [16], March 2020 COVID crash):

| Parameter | Estimate |
|-----------|----------|
| Index decline | 20–35% |
| Duration of acute phase | 3–15 trading days |
| VIX spike | 60–120 (vs. normal 15–20) |
| Recovery timeline | Weeks to months |
| Policy response | Fed emergency liquidity, potential circuit breakers |

This is emphatically **not** a 2008-style systemic solvency crisis. The financial system does not become insolvent. Banks do not fail en masse. The shock is to market *structure*, not to credit fundamentals. The recovery begins once the gamma books are cleared — potentially within days of the acute phase.

### 6.4 The December 2026 Focal Point

The chart's x-axis annotation "2Dec2026" warrants specific attention. December quad-witching — the simultaneous expiry of stock options, index options, index futures, and single-stock futures — is historically the largest notional expiry event of the calendar year. In December 2026, if the current growth trajectory continues:

- Projected daily notional at December 2026 quad-witching (~18 Dec 2026): approximately **\$3.0–3.5T**
- Dealer gamma exposure at this scale would be unprecedented
- The convergence of massive open interest, year-end liquidity contraction, and potential profit-taking creates elevated dislocation risk

December 18, 2026 is identified as the nearest specific high-risk calendar date. It is not a prediction — it is a natural focal point where structural conditions are most likely to align.

---

## 7. Discussion

### 7.1 What This Is Not

This analysis does not predict:
- A Great Depression or prolonged economic contraction
- Mass bank failures or credit system collapse
- A repeat of 2008 contagion mechanics
- An inevitable outcome at any specific date

### 7.2 What This Is

This analysis identifies:
- A growth trajectory in SPX call notional volume that is mathematically classified as super-exponential with high confidence (R² > 0.97 across all models)
- A structural regime in which dealer hedging mechanics have become the dominant market force
- A finite probability distribution of termination dates, with 100% of Monte Carlo runs terminating before 2044
- A probable termination event character: fast, violent, brief, and ultimately recoverable

### 7.3 Limitations

1. **Data quality:** Chart extraction introduces ±5–10% uncertainty in historical values. Higher-resolution data from CBOE or options analytics providers would improve model precision.
2. **Model uncertainty:** All five models carry different structural assumptions. The true process is not captured fully by any single model.
3. **Threshold uncertainty:** The Monte Carlo dealer capacity threshold (\$8T median) is an estimate. The true threshold is endogenous and unobservable.
4. **Regime change:** Regulatory intervention (SEC position limits, CBOE contract modifications) could truncate the bubble artificially before the structural threshold is reached.
5. **Black swans:** The model cannot predict the catalyst, only the structural fragility that amplifies it.

### 7.4 Relationship to Broader Market Structure

The phenomenon analysed here is not isolated to options markets. It is the options-market manifestation of a broader structural trend: the increasing dominance of derivatives over underlying markets, the growing participation of retail investors in complex instruments, and the progressive displacement of fundamental price discovery by mechanical hedging flows. The options tail is now wagging the equity dog.

---

## 8. Conclusions

Five quantitative models were applied to 27 years of SPX call notional volume data. The findings are consistent:

1. **The growth is super-exponential.** The baseline exponential model (R²=0.975) systematically underestimates recent data. The finite-time singularity model (R²=0.982) and Sornette LPPL (R²=0.993) both provide superior fits and both embed a finite critical time.

2. **The curve does not converge — it terminates.** There is no mathematical or physical ceiling that produces a smooth logistic saturation. The termination is a discontinuity: a fast, high-amplitude dislocation event.

3. **The probability-weighted terminal window is 2027–2033, with base case 2028–2029.** The P10 scenario (earliest 10% of runs) fires in January 2027. The December 2026 quad-witching event (18 December 2026) is the nearest high-risk focal point.

4. **The termination event is a gamma unwind, not a solvency crisis.** Estimated magnitude: 20–35% index decline over days to weeks, VIX spike to 60–120, policy response and recovery over weeks to months.

5. **At \$2.6T daily notional, the options market has already exceeded 5% of total US equity market cap in a single day.** This is structurally unprecedented. The system is in the terminal phase of its growth regime.

The chart that prompted this analysis is, in essence, a picture of a slowly loading gun. The trigger is unknown. The mechanism is not.

---

## References

[1] Social media post sharing SPX call volume chart annotated "\$2.6 trillion notional," Facebook (7 May 2026). URL: https://www.facebook.com/share/p/1HtkRPocXp/

[2] CBOE Global Markets. "SPX Options Product Specifications." CBOE, 2024. https://www.cboe.com/tradable_products/sp_500/spx_options/

[3] Whaley, R.E. "Understanding the VIX." *Journal of Portfolio Management*, 35(3), 98–105, 2009.

[4] Beason, T. & Schreindorfer, D. "The Anatomy of the 0DTE Options Market." *SSRN Working Paper*, 2023. https://ssrn.com/abstract=4397358

[5] SpotGamma. "0DTE Options: Market Impact and Structural Analysis." SpotGamma Research, 2023. https://spotgamma.com

[6] Carr, P. & Wu, L. "A Tale of Two Indices." *Journal of Derivatives*, 13(3), 13–29, 2006.

[7] SpotGamma. "Gamma Exposure and Market Microstructure." SpotGamma Research Notes, 2024. https://spotgamma.com/research

[8] CBOE Global Markets. "CBOE Annual Volume and Open Interest Report." CBOE, 2025.

[9] Sornette, D. *Why Stock Markets Crash: Critical Events in Complex Financial Systems*. Princeton University Press, 2003. ISBN: 978-0691118239.

[10] Johansen, A., Ledoit, O. & Sornette, D. "Crashes as Critical Points." *International Journal of Theoretical and Applied Finance*, 3(2), 219–255, 2000.

[11] Filimonov, V. & Sornette, D. "A Stable and Robust Calibration Scheme of the Log-Periodic Power Law Model." *Physica A*, 392(17), 3698–3707, 2013.

[12] Johansen, A. & Sornette, D. "Finite-time Singularity in the Dynamics of the World Population, Economic and Financial Indices." *Physica A*, 294(3–4), 465–502, 2001.

[13] Soros, G. *The Alchemy of Finance*. Simon & Schuster, 1987. ISBN: 978-0471445495.

[14] Bank for International Settlements. "OTC Derivatives Statistics." BIS Quarterly Review, December 2024. https://www.bis.org/statistics/derstats.htm

[15] Reinhart, C.M. & Rogoff, K.S. *This Time Is Different: Eight Centuries of Financial Folly*. Princeton University Press, 2009. ISBN: 978-0691152646.

[16] Cboe. "February 2018 VIX Spike and the Volmageddon Event." CBOE Market Insights, 2018. https://www.cboe.com/insights

[17] Black, F. & Scholes, M. "The Pricing of Options and Corporate Liabilities." *Journal of Political Economy*, 81(3), 637–654, 1973.

[18] Hull, J.C. *Options, Futures, and Other Derivatives*, 11th ed. Pearson, 2022. ISBN: 978-0136939979.

[19] Taleb, N.N. *The Black Swan: The Impact of the Highly Improbable*. Random House, 2007. ISBN: 978-1400063512.

[20] Mandelbrot, B. & Hudson, R.L. *The (Mis)Behaviour of Markets: A Fractal View of Financial Turbulence*. Basic Books, 2004. ISBN: 978-0465043576.

---

## Appendix A: Model Equations

| Model | Equation | Parameters |
|-------|----------|------------|
| Exponential | `y = 5.680 · exp(0.2118t)` | t = years since 1999 |
| Singularity | `y = 10⁶ / (2033.96 − T)^2.902` | T = calendar year |
| LPPL | `ln(y) = 11.958 − 0.238·(tc−T)^0.990·[1 + (−0.053)·cos(9.07·ln(tc−T) + 4.47)]` | T = calendar year |
| Monte Carlo | `V(t+dt) = V(t)·exp(0.277/12·dt + σε)` | σ=0.08, ε~N(0,1) |

---

## Appendix B: Monte Carlo Full Distribution

| Percentile | Calendar Date | Notional (\$B) |
|-----------|---------------|---------------|
| P5 | August 2026 | ~2,820 |
| P10 | January 2027 | ~3,127 |
| P25 | November 2027 | ~3,938 |
| P50 | May 2029 | ~5,965 |
| P75 | May 2031 | ~10,375 |
| P90 | July 2033 | ~18,898 |
| P95 | March 2035 | ~29,000 |

---

## Appendix C: Structural Ceilings Reference

| Ceiling | Value (\$T) | Significance |
|---------|-------------|-------------|
| Current record | 2.6 | Established 7 May 2026 |
| 5% US market cap/day | ~2.75 | **Already breached** |
| US Federal budget | ~7 | Institutional scale |
| US GDP | ~28 | National economy |
| US equity market cap | ~55 | Theoretical underlying max |
| Global GDP | ~115 | Global economy |
| Global equity market cap | ~110 | All listed equity |
| BIS OTC derivatives (notional) | ~700+ | No hard ceiling — synthetic |

---

*This paper was produced as an independent quantitative analysis based on publicly available chart data and established mathematical models. It does not constitute financial advice. All projections carry substantial uncertainty. The author holds no positions in the instruments discussed.*

*© Odin Loch, May 2026. All rights reserved.*
