# Battle Sim — modern mathematical battle modelling, a literature survey

> **A survey-and-design note that maps the modern mathematical-modelling landscape for combat — Hughes salvo equations, extended Lanchester equations for irregular warfare, Markov battle-state chains, FATHM linear programming, the Dupuy/TNDM combat-power lineage — into one comparative framework.** The folder is *explicitly not* an operational simulator; it is a structured reading map intended as the prerequisite groundwork for one. The note is unusually honest about its own epistemics: it asks readers to verify each cited model against primary sources before relying on any of its numbers.

---

## What this folder is

The literature on quantitative combat modelling is fragmented across half a dozen traditions that rarely cite each other: naval salvo equations (Wayne Hughes, 1995), Lanchester-style attrition with later extensions for guerrilla and recruitment dynamics, Markov chain models of engagement state ({Initial → Contact → Engagement → Resolution}), linear programs like FATHM that solve theatre-level allocations, and the Dupuy / TNDM combat-power tradition that bakes in 60+ environmental variables and the OLI metric. Each tradition has different inputs, different invariants, and different valid use-cases. This folder presents them side-by-side with the equations, then closes with a taxonomy of computational speed / convergence / scalability for each, and an honest "verify before using" warning about its own claims.

It is the right read for anyone trying to *choose between* modelling approaches before writing a simulator — and the wrong read for anyone wanting code that runs.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`Battle Sim.md`](Battle%20Sim.md) | The substantive survey-and-design note. Hughes salvo recursion, irregular warfare ODEs with recruitment / defection terms, Markov state machines, FATHM LP framing, Dupuy/TNDM lineage, comparative table, closing Hughes quote on the role of variables in battle. |

---

## 🧠 Modelling traditions surveyed

| Tradition | Key formula | What it models | What it can't |
|---|---|---|---|
| **Hughes salvo (1995)** | `A(t+1) = A(t) − β·B(t) / (defensive_factor_A)` and symmetric for `B` | Naval missile-vs-defensive-system salvos | Sustained ground engagement |
| **Extended Lanchester** | Coupled ODEs with recruitment, defection, attrition rates | Irregular warfare, insurgency dynamics | Tactical decisions |
| **Markov battle states** | `π = πP` over `{Initial, Contact, Engagement, Resolution}`; `10–20` iterations to convergence by eigenvalue argument | Engagement progression | Spatial / kinematic detail |
| **FATHM** | LP `minimise Σ losses s.t. constraints`; doc claims sub-3-minute full-theatre solve (unsourced in note) | Theatre-level allocation | Stochastic effects |
| **Dupuy / TNDM** | Combat Power formula with `60+` environmental variables; OLI (Operational Lethality Index) | Historical-validation-style assessment | Cyber, EW, multi-domain |

---

## 📊 Comparative table (qualitative, paper §)

The note's own comparison table groups each tradition by **computational speed / convergence behaviour / scalability tier**. Concrete numerical claims (e.g. FATHM "sub-3-minute," WWII-validation status, iteration counts) are **documentary survey assertions** that the file *itself* asks you to verify against primary sources before relying on.

---

## 🚧 Honest caveats (explicit in the note)

- **This is a reading map, not an operational manual.** The opening paragraph states this directly.
- **Verify cited numbers and parameters against primary sources.** Asked of the reader by the author.
- **No code, no harness, no benchmark.** This is documentation; if you want runtime, you build it.
- **Future-work scope** lists cyber, multi-domain, AI, and quantum extensions — by listing them as not-yet-covered, the note signals the boundary of v1.

---

## 🎯 Who this is for

| Reader | Value |
|---|---|
| Researcher choosing a modelling tradition | Side-by-side equations + comparison table saves weeks |
| Simulator engineer | Decision tree before writing code |
| Operations analyst | Quick taxonomy of named methods |
| Anyone wanting a running simulator | Wrong folder — see academic packages or commercial tools |

---

## 🔗 Related work in this repo

- [`../Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — ARIA-INTEL would feed track inputs into any simulator built from this folder
- [`../Filtering/`](../Filtering/) — GH-SR-IMM provides robust per-platform state estimation
- [`../Weapons-Defence/`](../Weapons-Defence/) — defence-tech R&D portfolio that any combat model would parameterise
- [`../UCN Political System/`](../UCN%20Political%20System/) — strategic doctrine that frames the engagements

---

[← Back to main README](../README.md)
