# Economics — EREM (Energy-Resource Economic Model)

> **EREM reframes national wealth as physics: instead of measuring a nation by GDP (an annual flow accounting for goods produced) or by capital-asset stocks (in dollars whose dollar-denomination is itself the artefact being measured), measure it by **Total National Wealth (TNW) in megajoules** — the actual physical-energy content of natural endowments, manufacturing capacity, food / energy / water security, human / labour capacity, and information / efficiency. Issue currency only when physical wealth grows: `Total_currency = k · TNW` with `k = 0.85` (`15 %` measurement buffer). The exchange rate between two nations is then `(TNW_A / Pop_A) / (TNW_B / Pop_B)` — directly comparable, dimensionally consistent, and immune to monetary inflation.** EREM is explicitly labelled v1.0 / theoretical and asks for empirical validation; what it offers in exchange is a *unit* — the megajoule — that does not depend on what someone in Washington decides about interest rates this morning.

---

## What this folder is

The standard tools for measuring economies are GDP (a flow) and various capital-stock measures denominated in the currency you're trying to evaluate. Both are circular: dollar-denominated wealth measurements presuppose that the dollar is a stable yardstick, which is exactly what is in question when wealth fluctuates against monetary policy decisions. The Inclusive Wealth Index (IWI) tradition tries to fix this by aggregating natural, human, and produced capital, but uses dollar denomination too. EREM proposes a different fix: **take a physical-science yardstick — energy content in megajoules — and recast every wealth component into that unit.** Petroleum reserves are MJ. Wind installed is MJ-per-year. Manufacturing capacity is MJ throughput. Food / energy / water security are MJ-equivalent. Human / labour capacity is MJ. Even information and efficiency — Shannon-information-flux scaled to physical-substrate energy — go into MJ.

The result is a single dimensionally-consistent number for "what is this country worth," with a currency-issuance rule (`Total_currency = 0.85 · TNW`) that makes Cantillon-effect inflation structurally impossible. The exchange-rate formula falls out for free.

The work cites real EROI literature (Murphy & Hall, Brockway et al.) honestly, runs hypothetical worked examples on illustrative national wealth comparisons, and is explicit about being v1.0 — the goal here is to publish the framework so others can validate, not to claim it's been validated.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`EREM_Research_Paper.md`](EREM_Research_Paper.md) | Full research paper. TNW formula, Q-factor, RBCU issuance rule, exchange-rate derivation, trade-entropy worked example. |
| [`EREM_Explained_Paper.md`](EREM_Explained_Paper.md) | Explainer document. Lower-density walkthrough of the same ideas for non-specialist readers. |
| [`Energy_Resource_Economic_Model.md`](Energy_Resource_Economic_Model.md) | Background / model document. |

> **Mirror notice.** Papers `EREM_Research_Paper.md` and `EREM_Explained_Paper.md` are duplicated in [`../UCN Political System/`](../UCN%20Political%20System/) where EREM serves as the political doctrine's economic backbone. **This folder (`Economics/`) is the canonical home of the model itself.**

---

## 🧠 The model

### Total National Wealth

```
TNW = α · NEW + β · MWI + γ · FEW + δ · HLC + ε · IEF       (all in MJ)

α = 0.40   (NEW = Natural Energy Wealth)
β = 0.25   (MWI = Manufacturing & Wealth Infrastructure)
γ = 0.20   (FEW = Food / Energy / Water security)
δ = 0.10   (HLC = Human / Labour Capacity)
ε = 0.05   (IEF = Information / Efficiency Factor)
```

### Q-factor (energy-source quality multiplier)

```
Q = (Energy Density) × (Transportability) × (Controllability) × (Waste Factor)

Q_nuclear        = 1.00     (reference)
Q_petroleum      = 0.75
Q_wind           = 0.65
Q_solar_installed = 0.58
Q_coal           = 0.42
```

### Resource-Backed Currency Units (RBCU)

```
Total_currency = k · TNW       k = 0.85    (15 % measurement buffer)
```

Physical wealth must grow before currency can be issued. There is no equivalent of "the central bank decided to print 2 % more this year."

### Exchange rate

```
Rate(A → B) = (TNW_A / Pop_A) / (TNW_B / Pop_B)
```

Direct, dimensionless, no monetary-policy translation layer.

### Trade valuation with entropy

Worked example: 1 × 10⁹ kg coal at 24 MJ/kg, Q = 0.42, with 8 % entropy loss in transport / refining → **9.26 × 10⁹ MJ-equivalent** delivered to the buyer.

### Worked nations (illustrative)

| Nation | Illustrative TNW | Per-capita | Per-capita rank |
|---|---|---|---|
| A | `4.7 × 10¹⁸ MJ` | `4.0 × 10¹⁰` MJ/person | second |
| B | `2.6 × 10¹⁸ MJ` | `4.4 × 10¹⁰` MJ/person | first |

---

## 📚 Cited literature (literature anchors)

| Source | Claim |
|---|---|
| Murphy & Hall 2010 | EROI ~5:1 minimum societal threshold |
| Brockway et al. 2024 | Useful-stage EROI ~3.5:1 |
| US oil/gas EROI history | ~100:1 → ~18:1 over time |
| Inclusive Wealth Index | 44 of 140 countries with declining per-capita inclusive wealth despite rising GDP |

---

## 🚧 Honest caveats

- **Explicitly theoretical, requires empirical validation.** The papers state this directly.
- **Weighting coefficients (`α, β, γ, δ, ε`) are priors**, not derived. Policy questions on the exact split.
- **Q-factors need national calibration** and dynamic updating (the Q of solar in Australia ≠ the Q of solar in Iceland).
- **No full accounting for knowledge capital or ecosystem services in v1.** Water gets folded into FEW; richer treatment is future work.
- **Political economy of reserve audits and transition is the main practical barrier.** Adopting EREM nationally requires audited physical-resource accounting at a level no major economy currently does.
- **Phased RBCU pathway over decades** in the long research paper. Not a "switch tomorrow" proposal.

---

## 🎯 What this displaces

| Standard | Limitation | What EREM offers |
|---|---|---|
| GDP | Annual flow, currency-circular | Stock-based wealth in SI units |
| Inclusive Wealth Index | Useful but dollar-denominated | Megajoule-denominated, not currency-circular |
| Gold standard | Single-commodity anchor | Multi-component physical anchor |
| Fiat / floating exchange rates | Prone to monetary policy distortions | Direct physical-wealth-per-capita ratio |
| Energy-money proposals (Soddy, Daly) | Conceptual, no operational rule | Concrete TNW formula + `k = 0.85` issuance rule |

---

## 🔗 Related work in this repo

- [`../UCN Political System/`](../UCN%20Political%20System/) — EREM as the economic backbone of UCN doctrine; sovereign digital currency analysis sits there
- [`../Weapons/`](../Weapons/) — defence economics framing (sovereign-manufacturing context)
- [`../Diffusion Welding/`](../Diffusion%20Welding/) — sovereign-manufacturing process work
- [`../Rockwell 50 to 70 Carbide/`](../Rockwell%2050%20to%2070%20Carbide/) — sovereign-manufacturing supply-chain economics
- [`../Diamond Batterys/`](../Diamond%20Batterys/) — energy economics adjacent (NEW component of TNW)
- [`../Statistical Generation/`](../Statistical%20Generation/) — mathematical machinery (Lévy / category theory) potentially applicable

---

[← Back to main README](../README.md)
