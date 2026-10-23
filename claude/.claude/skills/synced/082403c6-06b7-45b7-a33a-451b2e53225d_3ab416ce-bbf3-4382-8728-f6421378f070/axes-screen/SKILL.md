---
name: axes-screen
description: Cross-reference an external axe list, headline blast, or broker chat transcript against Meteora's live EMSX book and surface every price point within 5 cents of our working orders. Trigger whenever the user pastes a multi-ticker axe/headline blast (from StoneX, Brandon Brenner, Clear Street, Cantor, Jefferies, or any broker) and asks to "compare against the blotter", "cross-reference our book", "screen the axes", "find alignment", "where are we close", or any variant. ALSO trigger proactively whenever the user pastes a block of broker axes, morning headlines, unit bids, or sell-side axe lists — the default action is to run this screen. Produces a single Bloomberg-pasteable table showing cross-side alignment (actionable trades) and tight same-side overlap (competing with the broker). Always use this skill for axe-vs-book comparisons — do not produce ad-hoc comparisons.
---

# Axes Screen

Single-pass cross-reference of external broker axes against the Meteora live EMSX book. **Table first, commentary after (optional, only if it adds value).** Output pastes into Bloomberg/Excel without reformatting.

## When to run

User pastes a block of broker axes/headlines (bids, offers, trade prints, unit bids/offers) — typically 10–50 tickers — and wants to know which of their lines we can trade against and which we're stacked behind.

Typical triggers:
- "Compare with EMSX blotter"
- "Cross-reference against our book"
- "Screen these axes"
- "Find alignment / where are we close"
- Paste of a broker chat transcript or axe sheet with no explicit instruction — default to running this screen

## The core principle

The user is looking at a 10–50 line broker message and wants one answer: **what can I trade?** Render the table immediately. No preamble. No parsed-list dump. No "Top calls" summary above the table. The table itself is the product.

## Workflow

### Step 1: Parse the axe list silently

Extract every ticker + side + price + size from the input. Do not write the parsed list to the user. The input format varies by broker:

- **StoneX (Brandon Brenner)** — timestamped one-liners: `09:32:04 LOKV can sell 250k @ 10.45` or `09:51:25 ETHM 10.75 bid 100k`
- **Unit bids/offers** — grouped blocks: `AACPU 10.04 bid 100k`
- **Headline blasts** — mixed trade prints and axes

**Important parsing notes:**
- "X bid Y" = broker will PAY X → broker BUYING → we need to SELL to hit
- "X at Y" or "can sell Y @ X" = broker OFFERING → we need to BUY to lift
- "traded" / `Xx'd` is informational (prior print) — include with Side `TRD`
- Pre-split SPAC units (`AACPU`, `LEGO/U`) are distinct tickers from the common — don't collapse
- **SPAC shorthand — disambiguate via tape, not assumption.** A bare decimal like `.93x.96` or `9.96` or `.56` drops the leading handle. Do NOT assume commons are always a $9 handle — SPAC commons trade anywhere from ~$9.50 to ~$12+ depending on trust value and deal status. The leading digit is implied by the current market.
  - For commons, if the snip itself shows enough context (an earlier line on the same ticker quoting `9.96` in full, a market quoted as `9.93x9.96`, etc.) use that.
  - If context is ambiguous, call `get-price(ticker=...)` on every shorthand-quoted ticker to anchor the handle before writing the row. Cheaper to do one batched `get-price(tickers=[...])` upfront than to misread `.96` as `9.96` when it's actually `10.96`.
  - For warrants/rights/sub-$1 quotes, `.56` unambiguously means 0.56 (leading digit is zero).
- When a market is shown (`.93x.96 , 100k up`), treat it as two lines: BID + OFR at the resolved prices, both at the shown size

### Step 2: Resolve shorthand handles and pull the blotter

**2a — Resolve any shorthand prices.** If any axe line uses dropped-handle shorthand (e.g., `.96`, `.93x.96`) and the handle isn't unambiguous from the snip itself, make a single batched `get-price(tickers=[...])` call with every ambiguous ticker. Use the mid or last trade to anchor the leading digit. Do this before classifying — misresolving a handle makes every downstream gap wrong.

**2b — Pull the blotter in one call.** For each axe line, include in a single batched `emsx-blotter(tickers=[...])` call:
- The exact ticker as written
- If the axe is for a unit, also include the common base (strip trailing `U` or `/U`)

Warrants/rights on the same base are caught automatically by substring match. **Do NOT loop. Do NOT pull the full blotter.**

### Step 3: Classify each broker line against our orders

For each axe line, scan **same-ticker** orders in the response and classify within 5c:

**Cross-side (actionable)** — broker wants one way, we're working the other:
- Broker BIDS X → we SELL at price ≤ X + 0.05
- Broker OFFERS X → we BUY at price ≥ X − 0.05

**Same-side (competing/informational)** — we're on the same side near their level:
- Broker BIDS X → we also BUY within 5c
- Broker OFFERS X → we also SELL within 5c

**Different-leg axes are dropped.** If the broker axes the warrant and we only have common (or vice versa), omit the line entirely — it's noise. Cap-stack relationships belong in `unit-valuation` or dedicated warrant work, not here.

### Step 4: Render the table — nothing before it

The first thing the user sees is the table. No header, no "here's the screen," no top-calls bullets. Just the table.

| Ticker | Broker Side | Broker Px | Broker Sz | Our Side | Our Px | Our Working | Gap | Category | Note |

Column rules:
- **Ticker** — the broker's ticker, as written
- **Broker Side** — `BID` / `OFR` / `TRD`
- **Broker Px** — the broker's level (e.g., `10.04`)
- **Broker Sz** — shortened (`100k`, `25k`, `1M`)
- **Our Side** — `SELL` / `BUY`
- **Our Px** — our limit price
- **Our Working** — working size only (not idle parent balance). Shorthand (`10k`, `5.7k`)
- **Gap** — cents, signed from our perspective. Cross-side: positive cents we'd concede to trade (`+2c`). Same-side: `=` if exact level, `+Xc above` / `−Xc below` showing our price relative to broker.
- **Category** — `ACTIONABLE` (cross-side ≤ 5c), `WIDE` (>5c but meaningful, include only if requested or if position is significant), `SAME-SIDE`
- **Note** — 5–10 words. Flag `size match`, `our axe bigger`, `competing at level`, `internal conflict` (we're on both sides), `working 1c through us`

Sort order:
1. `ACTIONABLE` first, tightest gap at top
2. `SAME-SIDE` next, tightest gap at top
3. `WIDE` at the bottom (only if included)

Formatting:
- Plain markdown table. No code fences around it.
- If no Meteora order is within 5c on same-ticker, **omit the axe line entirely**.
- If nothing is actionable and nothing is same-side within 5c, the table is empty — say so in one line and stop.

### Step 5: Optional commentary below the table

Only add commentary if there is something non-obvious worth flagging — e.g., "Griffin is offering BBCQ 2c through our ask on 5x our size; we're about to be stranded." Keep to 2–4 lines max, bullet format. **Skip entirely if the table speaks for itself.** Never repeat what's already in the table.

## Example: end-to-end

**Input:**
```
09:55:00 CCIX 10.73 bid 200k
09:56:58 AACB can sell 25-50k @ 10.39
10:08:28 HCAC 9.95 bid 50k
```

**Output (nothing precedes the table):**

| Ticker | Broker Side | Broker Px | Broker Sz | Our Side | Our Px | Our Working | Gap | Category | Note |
|---|---|---|---|---|---|---|---|---|---|
| HCAC | BID | 9.95 | 50k | SELL | 9.96 | 30.7k | +1c | ACTIONABLE | 69k idle behind |
| CCIX | BID | 10.73 | 200k | SELL | 10.78 | 5.7k | +5c | ACTIONABLE | 24.9k remain |

HCAC is the call — 1c concession on full size and we clear 30.7k working.

(AACB has no working order within 5c → omitted. No different-leg rows.)

## Judgment calls

### What counts as "within 5 cents"?

- Commons $9–$11: strict 5c window
- Warrants/rights <$1: 5c window still, but if percentage gap is huge (e.g., $0.15 vs $0.20 = 33%), flag in Note as `WIDE%`
- Units ($10–$10.50): 5c window

### Internal conflicts

If we have both a BUY and SELL on the same ticker and both are near the broker's level, show both rows and note `internal conflict` on each. Common with positions worked across sub-books.

### When nothing is actionable

One line: "No alignment within 5c." Stop. Don't pad with leg translations or wide rows just to have content.

## Non-negotiables

- **Table first.** Nothing above it. No parsed-list echo, no "Top calls" callouts.
- **One table.** Same-side rows go at the bottom of the same table.
- **Same-ticker matches only.** Drop different-leg rows (broker on common, we on warrant, or vice versa).
- **Batched blotter call.** One `emsx-blotter(tickers=[...])`. Never loop.
- **Working size, not total.** The "Our Working" column shows live on exchange, not idle parent balance.
- **Omit dead lines.** No Meteora order within 5c on the same ticker → skip the row entirely.
- **Commentary is optional.** Skip if the table speaks for itself.
