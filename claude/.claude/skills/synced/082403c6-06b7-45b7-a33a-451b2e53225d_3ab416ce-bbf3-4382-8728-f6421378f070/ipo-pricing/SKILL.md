---
name: ipo-pricing
description: Back out the implied price of a SPAC unit's warrant or right from a target common-stock yield. Trigger when the user asks to 'price the IPO', 'price the unit', 'what's the warrant worth at X% yield', 'IPO pricing for [TICKER]', 'is the warrant reasonable at X yield', 'implied warrant cost', 'implied right cost', 'what's the unit imply', or any request to evaluate whether a SPAC unit's embedded warrant/right is fairly priced given a target yield on the common. Also trigger proactively whenever the user pastes a unit ticker alongside questions about whether the warrant or right is cheap, fair, or expensive given current trading levels. Produces a 7-row yield matrix (default 5% ± 0.6% in 0.2% steps) showing implied common bid and implied full warrant/right cost at each yield level. Always use this skill for unit-pricing questions — do not produce ad-hoc warrant/right valuations from a yield target.
---

# IPO Pricing — Implied Warrant/Right Cost from Common Yield

## What this skill does

Given a SPAC unit, this skill answers: **"if the common is to trade at X% yield to redemption, what does the embedded warrant or right have to cost?"**

It produces a yield matrix (default 5.0% ± 0.6% in 0.2% steps, 7 rows) showing the implied common bid and the implied full warrant/right cost at each yield level. The user can override the base yield and/or the step size.

This is a **breakeven / residual** calculation — not a from-first-principles warrant valuation. The number it gives you is the cost at which the warrant/right is "free" given the target yield. Compare that implied cost to your view of fair warrant/right value to decide whether the unit is cheap, fair, or expensive.

## The math (three steps)

**Step 1 — project trust to the deadline:**
```
MaxTrust = CIT_at_IPO × (1 + r_Tbill)^((MaxDate − IPODate) / 365)
```

**Step 2 — discount back to today at the target yield:**
```
ImpliedCommonBid = MaxTrust / (1 + y_target)^((MaxDate − Today) / 365)
```

**Step 3 — residual × ratio denominator:**
```
ImpliedFullWR = (UnitPrice − ImpliedCommonBid) × N
```

Where `N` is the denominator of the warrant/right ratio. For "1/3W", N = 3. For "1/10R", N = 10. The structure note (e.g. "Cayman, 1/3W") gives you N directly.

## Required inputs

| Input | Source | Notes |
|---|---|---|
| Unit ticker OR manual params | User | Try ticker first; fall back to manual if nothing pulls |
| Unit Price | Bloomberg `get-price` (live) — fall back to user-stated price or offer price only if no live quote | **ALWAYS pull the live unit price from `get-price` first if the unit trades.** Do NOT default to $10.00. Only use $10.00 (or another offer price) when the unit has not yet broken / is pre-IPO, or when the user explicitly states a different price they want priced. |
| IPO Date | EDGAR S-1/424B4 or user | When the SPAC IPO'd (or expects to IPO) |
| Max Date duration | Structure note + sponsor extensions | 18mo for typical 1/2W deals; 24mo for rights deals or longer-duration warrants |
| CIT at IPO | S-1 / 424B4 | Almost always $10.00 or $10.05 — read it from the prospectus |
| T-Bill Yield | Bloomberg `USGG3M Index` PX_LAST | The trust earns this; matters for trust accrual |
| W or R | Structure note | Determines which row of the output is populated |
| Multiplier (N) | Structure note "1/N W" or "1/N R" | The denominator of the fraction |

## Workflow

### Step 1 — Get the inputs

**CRITICAL — UNIT PRICE RULE:** The unit price input must come from the live tape whenever the unit trades. Do NOT default to $10.00 just because it's a SPAC unit. The whole point of the matrix is to evaluate where the unit is *actually* trading vs. yield, so a hardcoded $10.00 when the unit prints $9.97 or $10.05 silently corrupts the implied W/R column. Always call `get-price` first. Use $10.00 (or another offer price) only when (a) the unit has not yet broken (pre-IPO or day-of-IPO before first print), or (b) the user explicitly says "price it at $X" — in which case use their stated price and note it.

**If the user gives a ticker:**
1. Call `get-price` for the unit and use the live mid (or bid/ask) as the unit price. If the unit has not yet broken, fall back to the offer price ($10.00 typical) and flag that you're using the offer price because no live quote exists. If the user explicitly stated a price, use theirs and note it.
2. Call `get-price` on `USGG3M Index` for the current 3M T-bill yield. If unavailable, default to 3.67%.
3. For an existing SPAC, look up IPO date and structure from `spac-details` MCP tool. For a brand-new IPO not yet in the sheet, ask the user or pull from the S-1.
4. Confirm CIT at IPO ($10.00 vs $10.05) — for newer deals this is often $10.05.

**If the user provides params manually:**
Take what they give and confirm any missing pieces (especially CIT, structure ratio, max date duration). If they give a ticker but specify a unit price ("price IACQU at $10"), use their stated price — don't override with the live print.

### Step 2 — Compute MaxDate

If the user gave a duration in months, MaxDate = IPODate + that many months. Otherwise infer from structure: 1/2W or 1/3W deals are usually 18 months; rights deals and 1/10W+ deals are usually 24 months. Always ask if you're guessing — the duration is a major driver.

### Step 3 — Build the yield matrix

Default: base yield 5.0%, step 0.2%, 7 rows from −0.6% to +0.6% (4.4%, 4.6%, 4.8%, 5.0%, 5.2%, 5.4%, 5.6%).

If the user specifies a different base or step, use theirs.

For each yield level, compute ImpliedCommonBid and ImpliedFullWR (or implied full Right) using the formulas above.

### Step 4 — Output the table

Use this format (markdown, rendered inline in the response):

```
**[TICKER]** — Unit $X.XX, IPO MM/DD/YY, [structure], Max date MM/DD/YY ([N] mo), CIT $X.XX, T-Bill X.XX%

| Yield | Implied Common | Implied [W or R] |
|------:|---------------:|-----------------:|
| 4.4%  | $X.XXXX        | $X.XXXX          |
| 4.6%  | $X.XXXX        | $X.XXXX          |
| 4.8%  | $X.XXXX        | $X.XXXX          |
| 5.0%  | $X.XXXX        | $X.XXXX          |
| 5.2%  | $X.XXXX        | $X.XXXX          |
| 5.4%  | $X.XXXX        | $X.XXXX          |
| 5.6%  | $X.XXXX        | $X.XXXX          |

MaxTrust at deadline: $X.XXXX
```

Bold the base yield row (5.0% or whatever the user picked). Show 4 decimal places on prices — the implied W/R values for narrow-ratio deals (1/10W, 1/15R) are very small and 2 decimals lose resolution.

### Step 5 — One sentence of context

After the table, add ONE short interpretive sentence — not analysis, just a framing reminder. Example: *"At 5% target yield, you'd be paying $0.35 per whole warrant by buying the unit; compare to your fair-value view on a 1/2W with 18mo duration on this sponsor."* No comp set, no trade rec — just the framing.

## Worked example

User: "Price out KBRO at 5%"

KBRO inputs: Unit $10.00, IPO 4/28/26, structure "Cayman, 1/2W, 18mo" (W, multiplier=2), CIT $10.00, T-Bill 3.67%, MaxDate 10/28/27.

```
**KBRO** — Unit $10.00, IPO 4/28/26, 1/2W (18mo), Max date 10/28/27, CIT $10.00, T-Bill 3.67%

| Yield | Implied Common | Implied W |
|------:|---------------:|----------:|
| 4.4%  | $9.8940        | $0.2119   |
| 4.6%  | $9.8656        | $0.2688   |
| 4.8%  | $9.8373        | $0.3254   |
| **5.0%** | **$9.8091**     | **$0.3818**  |
| 5.2%  | $9.7811        | $0.4378   |
| 5.4%  | $9.7532        | $0.4936   |
| 5.6%  | $9.7254        | $0.5492   |

MaxTrust at deadline: $10.5560
```

At 5% target yield, you'd be paying $0.38 per whole warrant by buying the unit at $10.00.

## Edge cases

**No warrant or right (N/A unit):** Some IPOs are clean common-only units. In that case there's no residual to back out — show only the implied common bid column with a note that the unit has no embedded W/R. The implied common bid should equal MaxTrust discounted at the target yield, and the unit price minus that bid is just the dealer markup, not an implied W/R.

**Unit-only structures (1W + 1/4R combos):** When the unit contains both a warrant AND a right, the multiplier collapses to 1 because you can't separate them. Flag this and show the implied "combined extra" cost rather than an implied W or R individually.

**Pre-IPO or pre-break (deal not priced / unit not yet trading):** Only in this case should you use the offer price ($10.00 typical). Use the prospective IPO date (or "today"), and the structure from the S-1/F-1. This is the same calc — just with prospective inputs. Always flag that you're using the offer price because there is no live quote yet.

**Sponsor extensions:** The model assumes the max date is the **longest possible** deadline (full extensions exercised). This is the conservative yield-to-trust assumption and matches how the broader Meteora yield models work. Don't shorten the duration unless the user explicitly asks for a no-extension scenario.

**WC leakage:** The model does NOT subtract working capital withdrawals from MaxTrust. This is consistent with the source IPO_tracker layout — leakage is a separate adjustment the user makes mentally based on the structure note. Don't try to bake it in unless the user asks.

## What NOT to do

- Don't try to value the warrant/right from first principles (Black-Scholes, binomial). That's `price-calls` / `warrant-arb-analysis` territory. This skill produces breakevens, not theoretical fair values.
- **Don't default the unit price to $10.00 when the unit trades.** Always pull the live mid from `get-price` first. $10.00 is only the right input for pre-IPO / pre-break units or when the user explicitly states it. A stale or assumed unit price silently corrupts the implied W/R column — this is the single most common way to produce a wrong matrix.
- Don't add a comp set unless asked. The user explicitly scoped this to the yield matrix only.
- Don't try to back out the yield from a market warrant price (the inverse direction). User explicitly scoped that out.
- Don't guess at the structure or max date — ask if you don't know. The multiplier and duration are the two biggest drivers; getting them wrong makes the whole table wrong.
- Don't round to 2 decimals on the implied W/R column. For narrow-ratio deals these can be <$0.10 and 2-decimal rounding hides material differences. Always use 4 decimals on price columns.
