---
name: unit-valuation
description: Institutional SPAC unit valuation framework. Compute fair value for pre-split and post-split SPAC units using sum-of-parts (deadline-adjusted common + rights + warrants), screen the pre-deal universe for undervalued units, evaluate broker axe lists against fair value, and flag combo-unit opportunities. Trigger when the user asks to 'value these units', 'fair value [ticker] unit', 'is [unit ticker] cheap', 'screen for undervalued units', 'evaluate this axe', 'best value units', 'units trading below fair', 'should we buy [UU ticker]', or any request to assess unit offers or rank the universe by embedded optionality. Also trigger proactively when broker axe lists or new IPO pricings arrive with unit tickers, or when the user asks about the 'BHAV-style' early-split trade. Always use this skill for unit valuation — do not produce ad-hoc fair values.
---

# SPAC Unit Valuation Skill

Compute institutional fair value for any SPAC unit — pre-split or post-split — using a sum-of-parts framework. Rank the universe, evaluate axe lists, and flag trade opportunities.

## Core framework

A SPAC unit is a stapled instrument: common stock + fractional warrant(s) and/or fractional right(s). At separation (typically 52 days post-IPO) each component trades independently. Fair value of the unit today is the sum of what each component will be worth when unstapled.

**Fair unit = Common value + Right value + Warrant value**

The three component values are each calculated with its own parameterized model. All parameters are centralized in `references/valuation_params.md` so that the framework can be updated in one place as marks evolve.

## Workflow

### Step 1: Identify the unit(s) to value

Accept any of:
- A single ticker ("value VACI unit")
- A list of broker axe offers ("evaluate this axe list")
- A universe query ("screen all pre-deal units")
- A subset filter ("only 1/4 right units", "only combo units")

### Step 2: Load current valuation parameters

Read `references/valuation_params.md` for the current marks. Always re-read this file fresh — it is the single source of truth for marks and may have been updated. Do NOT hard-code marks from prior conversations.

Current parameters (authoritative file is `references/valuation_params.md`):
- Common discount per month to liquidation deadline
- Right mark per 1-for-1 share equivalent
- Warrant mark per full warrant
- Separation window assumption (days post-IPO)

### Step 3: Pull unit data

For each ticker, call `MeteoraMCP:spac-details` to get:
- `unit_ticker`, `cash_in_trust`, `liquidation_deadline`, `ipo_date`
- `warrants_in_unit` (e.g. "1/2", "1/3", "1", "None")
- `rights_in_unit` (e.g. "1 for 1/4", "1 for 1/5", "None")
- Position data: `units_position`, `common_position`, `warrants_position`, `rights_position`
- Underwriter, bucket, sponsor quality tags

For live unit price, call `MeteoraMCP:get-price` with the unit ticker. Note unit tickers can be `{TKR}U`, `{TKR}/U`, or occasionally non-standard — retry with both formats if the first resolves with an error.

### Step 4: Verify pre-split vs post-split status

Pre-split = constituent W and R tickers do NOT trade independently on Bloomberg. The fair-value framework applies differently:
- **Pre-split**: unit still stapled, fair = sum of parts
- **Post-split**: unit may still trade but common/R/W also trade separately; fair should reconcile across all three (unit should arb to sum of live prices of components)

To verify status, call `MeteoraMCP:get-price` on the warrant ticker and right ticker (from spac-details). If either resolves with a live price and volume, the unit has split. If both fail to resolve or have zero volume, unit is pre-split.

The separation window is typically 52 days post-IPO, but sponsors can delay the 8-K filing. Do not assume DSI > 52 means split — verify on Bloomberg.

### Step 5: Compute fair value

Apply the formulas below for each component, sum, compare to live unit price.

See `references/valuation_formulas.md` for complete computational detail including edge cases (missing CIT, non-standard unit structures, sponsor-funded trust top-ups).

**Quick summary:**

```
common_fair = CIT - (months_to_liquidation * common_disc_per_month)
right_value_per_unit = right_ratio * right_mark_per_1for1
warrant_value_per_unit = warrant_ratio * warrant_mark_per_full
fair_unit = common_fair + right_value_per_unit + warrant_value_per_unit
discount_pct = (fair_unit - unit_price) / unit_price * 100
```

Ratios: "1/4 right" → 0.25, "1/5 right" → 0.20, "1 for 1/4" → 0.25, "1/2 warrant" → 0.50, "full warrant" or "1" → 1.00.

### Step 6: Rank and present

Always present results as a ranked table. Required columns (left to right):

1. `#` — rank by discount % descending
2. `Ticker` — unit ticker
3. `Offer` / `Unit Px` — live price or broker offer
4. `Size` — broker size if applicable
5. `UW` — underwriter (5 chars max)
6. `B` — bucket (quality tier)
7. `R` — right ratio as fraction or `—`
8. `W` — warrant ratio as fraction or `—`
9. `Mos` — months to liquidation
10. `Fair` — computed fair value
11. `Disc%` — signed percentage (positive = cheap to fair)
12. `U Pos` — current unit position from spac-details (or `—`)
13. `C Pos` — current common position (or `—`)

Use monospace formatting so columns align. For axe lists, list offers in order they were provided, then output the ranked table separately.

### Step 7: Commentary

After the table, always provide:

**Top picks** — top 2–3 names with the richest discount, with position context (new adds vs. existing exposure)
**Pass list** — names at or inside fair, no trade
**Combo unit flag** — if any units have BOTH W and R stacked, call them out separately (these are usually the biggest dislocations)
**Sensitivity note** — how the ranking changes if right mark moves ±$0.25 or warrant mark moves ±$0.10
**Sponsor risk flag** — if any top picks are from weak sponsors (ARC, Maxim, Polaris, Kingswood, DBOR), note the quality overlay

## When to use which view

- **Single unit value check** — minimal output, just the fair value calc with component breakdown. Use when user asks "what's VACI worth" or similar.
- **Axe list evaluation** — ranked table with position columns. Use when user pastes broker offers.
- **Universe screen** — larger ranked table across all pre-split units, plus stratification by structure (1/4R, 1/5R, 1/2W, combo). Use for systematic screens.
- **Trade construction** — narrative with specific sizing recommendations. Use when user is building a book around the framework.

## Output format — single unit check

For single-ticker requests, use a breakdown format:

```
{TICKER}U @ ${unit_px}
CIT: ${cit}, Liq: {liq_date} ({mos:.1f} months out)
Structure: {r_str} R + {w_str} W  ({pre-split | post-split})

Common fair:     ${cit} - ({mos} × ${common_disc}) = ${common_fair}
Right value:     {r_frac} × ${right_mark} = ${r_val}
Warrant value:   {w_frac} × ${warrant_mark} = ${w_val}
─────────────────
Fair unit:       ${fair}
Offered/Live:    ${unit_px}
Discount:        {sign}{disc_pct}%

Position: {u_pos} units, {c_pos} common
```

## Output format — axe list

Present as markdown table with all columns listed in Step 6. Follow with commentary from Step 7.

## Output format — universe screen

Stratify by structure type. Produce separate sub-tables for:
- Combo units (W + R both)
- Right-only units (1/4 R, 1/5 R, 1/8 R, 1/10 R)
- Warrant-only units (1/2 W, 1/3 W, full W)

Within each stratum, rank by discount %. Top-line commentary should compare the stratified winners.

## Integration notes

- **Conservative marks by design.** The default parameters are set to the low end of observed trading ranges. Fair values produced are therefore floors, not targets. A unit trading at fair is still likely cheap to model mean.
- **Separation status is empirical.** Always verify via Bloomberg ticker resolution, not DSI-based heuristics.
- **Position context matters.** A 2% discount on a name where we're already at target size is different from 2% on a zero-position name. Always pull positions.
- **Sponsor quality overlay.** The framework does not directly model sponsor quality. Deals from tier-4 sponsors (ARC, Maxim, Polaris, Kingswood) should be stress-tested with a higher common discount ($0.015–$0.02/month) before sizing up.

## Updating the framework

The parameters and detailed formulas live in `references/valuation_params.md` and `references/valuation_formulas.md` so they can be updated independently of the skill workflow. When the user says "update the marks" or "the warrant mark should be $X now":

1. Open `references/valuation_params.md`
2. Update the relevant parameter inline
3. Update the "Last updated" date and add a line to the change log
4. Do NOT modify SKILL.md unless the workflow itself is changing

The framework itself (common + right + warrant sum-of-parts) can be extended — e.g., adding a sponsor-quality adjustment, a sector adjustment, or a deal-announcement premium — by creating additional reference files and documenting the new term in the fair value formula.

## What this skill does NOT do

- Does not value in-deal SPACs (different framework — use in-deal spread analysis)
- Does not price individual warrants on their own (use `warrant-arb-analysis` skill)
- Does not compute SPAC yield to deadline (use `spac-yield-calc` skill)
- Does not fetch S-1 terms for new IPOs not yet in the tracker (use `spac-s1-extraction` skill first, then this skill)
- Does not make bucket assignments for unrated SPACs — flag these as "bucket ?" and note the gap
