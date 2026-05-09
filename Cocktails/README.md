# Cocktails — bar operations as a structured design problem

> **A complete bar-operations system, treated as a product platform rather than a recipe collection: four native-Australian-botanical "bases" (Coastal / Bush Orchard / Outback Heat / Native Forest) drive every spirit infusion, syrup, tincture, and bitters in the menu, organised into four signature series of three drinks each, with parallel zero-proof mirrors, a shift/day/week/month prep workflow, two complete bitters fabrication specs (a `500 ml` template and an alternative `375 ml` template with `21-day` simplified timeline), an umami / marine / ferment lane that uses `2-hour` mushroom stock and `4-hour` fat-wash protocols, an aus-citrus dehydration system at `57 °C / 12 h`, and a coriander-smash to truffle-avocado to hemp-mushroom to basil-almond to mustard-spice to savory-cream-soda recipe lineup that runs cross-regional fusion through a shared botanical OS.** The unusual move is treating bar operations the way a manufacturing engineer treats a factory floor — base ingredients, intermediate products, finished goods, QC checkpoints, shift rhythms, scaling rules — rather than as artisan free improvisation.

---

## What this folder is

Most cocktail content on the open web is recipe-shaped: take this spirit, mix with these things, garnish thus. Behind a working bar, the documentation that *actually keeps the place running* looks completely different — it specifies infusion timings (Coastal Gin = London dry + Coastal Essence, `48 h`; Bush Vodka, `24 h`; Spiced Rum, `72 h`), batch ratios (Native Orgeat is a `3-day` process, `1 : 1` syrups except Spiced Forest at `2 : 1` Demerara), prep rhythms (taste all syrups daily, weekend "essential prep only"), and platform abstractions (four signature series, each with three drinks, with a non-alcoholic mirror per series, scaled by season). This folder is documentation of *that* kind, applied to a venue conceptually anchored in Australian native botanicals: green ant gin, riberry shochu, native orgeat, blue-tansy/lavender fragrances, mastiha, sandalwood nut butter.

The bitters specifications are unusually engineered: two complete and parallel templates, both with explicit phased infusion (primary days 1 – 10, aromatics 11 – 17, finishing 18+) and `≥ 60 % ABV` spirit + water dilution to land at the right tincture strength. The umami lane is a full sub-platform (mushroom stock, salmon-oil cap `≤ 3 drops/drink`, `24 h` cold dashi with `48 h` use window) that lets the menu cross savoury / marine flavours without ad-hoc experimentation.

---

## 📑 Source documents

### Platform foundations

| File | Role |
|---|---|
| [`menu-structure.md`](menu-structure.md) | Four signature series (Coastal / Bush Tucker / Spice Trail / Forest Floor), three drinks each, seasonal scaling rules, zero-proof mirrors per series. |
| [`base-preparations.md`](base-preparations.md) | Foundational infusion / syrup / tincture preparations with explicit timings: Coastal Gin (`48 h`), Bush Vodka (`24 h`), Spiced Rum (`72 h`), Native Orgeat (`3-day` process), syrups (`1 : 1` default; Spiced Forest `2 : 1` Demerara). |
| [`prep-workflow.md`](prep-workflow.md) | Shift / day / week / month operational rhythms. **QC: taste all syrups daily.** Weekend essential-prep-only. Garnish dehydration `57 °C / 12 h`. |

### Bitters fabrication

| File | Role |
|---|---|
| [`master-bitters.md`](master-bitters.md) | **`500 ml` template.** `400 ml` `≥ 60 % ABV` spirit + `100 ml` water. `50 g` primary bitters / `25 + 25 + 25 g` other tiers. Phased infusion: primary days 1 – 10, aromatics 11 – 17, finishing 18+. |
| [`bitters-system.md`](bitters-system.md) | **`375 ml` alternative template.** `375 ml` spirit, `75 + 25 + 25 g` botanicals, **`21-day` simplified timeline**. |

### Fusion menus + sub-systems

| File | Role |
|---|---|
| [`global-fusion-menu.md`](global-fusion-menu.md) | Cross-regional fusion: argan fat-wash, sandalwood nut butter, green ant gin, mastiha, shochu + riberry. |
| [`accessible-fusion-menu.md`](accessible-fusion-menu.md) | Fusion menu without the rare-ingredient barrier. |
| [`aus-citrus-system.md`](aus-citrus-system.md) | Australian native citrus system: finger lime, desert lime, blood lime, native lemon. Dehydration protocols. |
| [`umami-system.md`](umami-system.md) | Umami / marine / ferment lane. **`2 h` mushroom stock, `4 h` fat-wash, `7-day` mushroom tincture, salmon-oil cap `≤ 3 drops/drink`, `24 h` cold dashi (`48 h` use window).** |

### Recipe exemplars

| File | Recipe |
|---|---|
| [`coriander-smash.md`](coriander-smash.md) | Coriander smash |
| [`hemp-citrus-cocktail.md`](hemp-citrus-cocktail.md) | Hemp + citrus build |
| [`hemp-mushroom-cocktail.md`](hemp-mushroom-cocktail.md) | Hemp + mushroom build |
| [`mustard-spice-cocktail.md`](mustard-spice-cocktail.md) | Mustard + spice profile |
| [`savory-cream-soda.md`](savory-cream-soda.md) | Savoury cream soda (NA-friendly) |
| [`truffle-avocado-cocktail.md`](truffle-avocado-cocktail.md) | Truffle + avocado luxury build |
| [`basil-almond-cocktail.md`](basil-almond-cocktail.md) | Basil + almond build |

---

## 🧠 The platform abstractions

```
4 native-Australian botanical bases  ──→  spirit infusions / syrups / tinctures
                                          (timings: 24 / 48 / 72 h, 3 days)
                                                    │
                                                    ▼
                                      4 signature series × 3 drinks
                                      + zero-proof mirror per series
                                                    │
                                                    ▼
                                      sub-systems:
                                      ├─ aus-citrus dehydration (57 °C, 12 h)
                                      ├─ umami / marine / ferment
                                      └─ bitters fabrication (two templates)
```

---

## 🎯 What is unusual about this

| Standard cocktail folder | What this offers |
|---|---|
| Recipes | Recipes + bases + infusions + bitters fabrication + sub-system specs |
| One template | Two parallel bitters templates (`500 ml`, `375 ml`) |
| Free improvisation | Shift / day / week / month prep rhythm |
| Loose "Australian native" theme | Four explicit botanical bases reused across menu / NA / food cross-utility |
| Menu | Menu + scaling rules + zero-proof mirror per series |

---

## 🚧 Honest caveats

- **No sales / A-B test data.** This is SOP + recipe-design language, not operations research with measured throughput.
- **Feasibility / licensing / allergen / cost** of niche botanicals (green ants, extreme-ABV bitters handling) implies real kitchen-safety and regulatory considerations not negotiated in-text.
- **Some ingredients are seasonal** and the document's "scale by season" rule is a pointer, not a complete plan.

---

## 🔗 Related work in this repo

- [`../Beauty Products/`](../Beauty%20Products/) — sister formulation white-paper work (Hemp Harmony lotion); shared discipline of "named active at named dose with cited mechanism"
- [`../Drugs/`](../Drugs/) — pharmacology framing (caffeine, etc.)
- [`../Statistical Generation/`](../Statistical%20Generation/) — sister information-theoretic frame for product-platform design

---

[← Back to main README](../README.md)
