---
name: warrant-arb-analysis
description: >
  Full fundamental pre-trade analysis for Meteora's Warrant Arbitrage strategy — long warrants vs. short calls / long puts / delta-hedged structure. Trigger when the user asks to 'run a warrant arb analysis', 'do a warrant arb write-up', 'analyze [TICKER] for a warrant arb', 'is [TICKER] a good warrant arb candidate', 'pull the arb analysis on [TICKER]', or any request to evaluate a company for a long-warrant / short-vol trade. Also trigger when the user mentions a warrant ticker (e.g. PSQHW, KDKRW) alongside options or vol and asks for background analysis. Output is a single structured email-ready memo covering company profile, financials, cap stack, warrant terms, vol profile, dilution risk, catalysts, sentiment, and trade setup summary. Always use this skill for warrant arb pre-trade diligence — do not do this analysis ad hoc.
---

# Warrant Arb Fundamental Analysis — Pre-Trade Memo

## Overview

Produces a single **email-ready memo** on a potential warrant arb candidate. The memo is structured to be copy-pasted directly into an email — no spreadsheets, no attachments, clean prose and compact tables.

**The trade this supports:** Long warrants + short front-end calls (or long puts, or delta-hedged) — long back-end vol, short front-end vol. The memo surfaces data and flags risks; it does **not** make a hard buy/sell recommendation.

**Tools used across this skill:**
- `get-price`, `get-company-info`, `get-option-chain`, `get-option-data`, `get-vwap` — Bloomberg
- `get-bond-chain`, `get-bond-price` — Bloomberg bonds
- `edgar-filings`, `edgar-filing-text`, `edgar-filing-index`, `edgar-company-facts`, `edgar-ownership-search` — SEC EDGAR
- `web_search`, `web_fetch` — PR history, news, sentiment, short interest

**Always call `tool_search` before using EDGAR and Bloomberg tools** — tunnel URLs rotate.

---

## Workflow

```
Step 0 — Entity Recon         (web_search)
Step 1 — Company Profile      (web_search + get-company-info)
Step 2 — Financial Highlights (get-company-info + edgar-company-facts + get-price)
Step 3 — Cap Stack & Overhang (EDGAR + Bloomberg bonds + web_search)
Step 4 — Warrant Terms        (EDGAR + get-price)
Step 5 — Volatility Profile   (get-option-chain + get-option-data)
Step 6 — Dilution Risk Rating (compute from Steps 2–3)
Step 7 — Business Quality     (web_search + EDGAR)
Step 8 — Catalyst & PR        (web_search — trailing 12mo PRs + forward calendar)
Step 9 — Sentiment & Positioning (web_search for short interest, insider flow)
Step 10 — Trade Setup Summary  (synthesize all steps)
Step 11 — Format & Deliver     (assemble email memo)
```

Work through every step in order. Do not skip steps. Show the user a brief status note before each step.

---

## Step 0: Entity Recon

Before anything else, resolve the full entity picture.

**Searches:**
1. `[TICKER] company description business`
2. `[TICKER] warrant ticker deSPAC SPAC`
3. `[TICKER] [WARRANT TICKER] warrant outstanding`

**Extract:**
- Full company name, common ticker, warrant ticker (e.g. PSQHW)
- Is this a deSPAC or a native public company with warrants?
- If deSPAC: original SPAC name, closing date, redemption %
- CIK for EDGAR (try both current entity and original SPAC if deSPAC)

Confirm entity before proceeding.

---

## Step 1: Company Profile

**Goal:** 2–4 sentence plain-English description of what the business does, what stage it's at, and any notable strategic pivots underway.

**Sources:**
- `get-company-info` (Bloomberg fundamental description)
- `web_search`: `[TICKER] business model investor presentation 2024 2025`
- Latest 10-K or 10-Q "Business" section via EDGAR if Bloomberg is sparse

**Write as:** A tight business-school-style paragraph. No fluff. Flag if the company is pre-revenue, burning cash, or mid-pivot — those are relevant to how long your warrants need to survive.

---

## Step 2: Financial Highlights

Pull each metric below. Flag any that are unavailable.

**Bloomberg (`get-company-info`):** Market cap, EV, cash & equivalents, total debt, LTM revenue, shares outstanding.

**EDGAR (`edgar-company-facts`):** Cross-check shares outstanding, verify cash/debt from latest 10-Q balance sheet.

**Compute yourself:**
- **Net Cash** = Cash − Total Debt
- **Net Cash Per Share** = Net Cash / Diluted Shares
- **Current Ratio** = Current Assets / Current Liabilities (from 10-Q)
- **Quarterly Burn Rate** = (Operating Cash Outflow last Q or LTM / 4). Use EDGAR cash flow statement.
- **Cash Runway (months)** = (Cash / Quarterly Burn) × 3. Flag if < 12 months.
- **Revenue Growth YoY** = (LTM Rev − Prior Year Rev) / Prior Year Rev

**Format for memo:**

```
Market Cap:          $XXM
Enterprise Value:    $XXM
Cash:                $XXM
Total Debt:          $XXM
Net Cash:            $XXM  ($X.XX/share)
LTM Revenue:         $XXM  (XX% YoY)
Quarterly Burn:      $XXM/quarter
Cash Runway:         ~XX months  ⚠️ [flag if <12mo]
Current Ratio:       X.XX
Diluted Shares O/S:  XXM
```

---

## Step 3: Cap Stack & Overhang

Map every instrument that can create dilution. This is the most important section for the arb — dilution events are your enemy on the long warrant leg.

### 3a. Warrants

**EDGAR + web_search:**
- Public warrants outstanding and ticker
- Private / sponsor warrants outstanding
- Strike price and expiration date (pull from warrant agreement EX-4.1 if needed — reference the `warrant-analysis` skill for deep dives)
- Redemption call trigger price (e.g. $18.00 / 20-of-30 trading days)
- Are they registered?
- Cashless exercise provision — summarize

### 3b. Convertible Notes

**Bloomberg (`get-bond-chain`, `get-bond-price`) + EDGAR:**
For each convert:
- Principal outstanding, conversion price, maturity date
- Shares issuable on full conversion
- Any reset / ratchet provisions (toxic flag)
- Lock-up expiration if recently issued

**Toxic convertible flag:** If conversion price resets downward on any trigger, mark **⚠️ TOXIC** and describe the reset mechanics.

### 3c. ATM / ELOC / SEPA

**EDGAR (S-3, 424B forms) + web_search:**
- Is there an active shelf? How much capacity remains?
- ATM program: size, amount drawn to date, remaining capacity
- ELOC / SEPA: counterparty, total commitment, shares issued to date, remaining
- Rate of utilization over last 6 months

**⚠️ SEPA / ELOC Floor Mechanics — Check This Every Time:**

Variable-price equity lines (especially YA II / Yorkville structures) often contain a **minimum conversion floor price** (commonly $1.00). This is not a standard anti-dilution provision — it is a **structural death spiral risk**:

- If the stock drops toward the floor, the number of shares issued per dollar drawn grows explosively
- Example: A $1M draw at $5.00/share = 200K new shares. The same draw at $1.10/share (just above $1.00 floor) = 909K new shares — a 4.5x increase in dilution from a 78% stock decline
- This dynamic accelerates selling pressure as the stock drops, which is exactly when the warrant position is most stressed

**How to identify it:** Search the SEPA/convertible note agreement (EDGAR exhibit, typically EX-10.1 or EX-4.1 on the 8-K announcing the SEPA) for language like: "floor price", "minimum price", "subject to a floor of $X.XX", or "the lower of X% of VWAP and $X.XX."

**Flag:** If any floor ≤ $2.00, mark **⚠️ TOXIC FLOOR — SEPA/ELOC** with the floor price and estimated share issuance at various stock price scenarios. This must be called out in the Trade Setup Summary risks.

### 3d. Lock-Up Expiration Calendar

**EDGAR (S-1, registration statements, lockup agreements) + web_search:**

List all known upcoming lock-up expirations by date:
```
[DATE] — Insider / Founder shares (XXM shares, ~XX% of float)
[DATE] — PIPE investors (XXM shares)
[DATE] — Convertible note conversion eligibility (if 12m lockup)
```
These are known selling pressure dates — flag any within 90 days.

### 3e. Dilution Summary Table

```
Instrument              | Shares (M) | % of O/S | Notes
------------------------|------------|----------|------
Public Warrants         |            |          | Strike $X.XX, exp [DATE]
Private Warrants        |            |          |
Conv. Note A            |            |          | Conv. @ $X.XX
Conv. Note B            |            |          |
ATM Remaining           |            |          | ~$XXM capacity
ELOC/SEPA Remaining     |            |          |
Shelf Remaining         |            |          |
TOTAL POTENTIAL DILUTION|            |          |
```

---

## Step 4: Warrant Terms

Extract the key economic terms of the **public warrants**. This drives the long leg of the trade.

**⚠️ MANDATORY: Confirm warrant counts from EDGAR before completing this section.** Do not use estimated or Bloomberg-reported counts — they are frequently stale or incomplete for deSPACs. Pull the warrant counts directly:

1. **For deSPACs:** Use `edgar-filings` on the original SPAC ticker/CIK, find the 8-K filed within days of the IPO date, read EX-4.1 (Warrant Agreement) for public warrant count, and the closing 8-K (Items 2.01, 3.03) for final outstanding counts after redemptions.
2. **For native public companies:** Check the most recent 10-Q notes to financial statements for "Warrant" disclosure, or search EDGAR full text for "warrants outstanding."
3. If counts remain unclear after EDGAR search, note explicitly: "⚠️ Warrant count unconfirmed — EDGAR EX-4.1 review required before sizing."

Use the `warrant-analysis` skill for full term extraction if deep mechanics are needed.

**Sources:** Bloomberg (`get-price` on warrant ticker) + EDGAR EX-4.1.

**Fetch live warrant price:** `get-price` on [WARRANT TICKER]

**Compute — Basic Metrics:**
- **Intrinsic Value** = max(0, Common Price − Strike)
- **Time Value / Premium** = Warrant Price − Intrinsic Value
- **Implied Leverage** = Common Price / Warrant Price
- **Breakeven at Expiry** = Strike + Warrant Price
- **Moneyness** = Common Price / Strike (e.g. 0.60 = 40% OTM)

**Compute — Warrant Implied Volatility (CRITICAL for the arb):**

The warrant is economically equivalent to a long-dated European call option. Back out its implied volatility using Black-Scholes inversion so it can be directly compared to listed options IV.

Inputs needed:
- **W** = current warrant price (from `get-price`)
- **S** = current common stock price
- **K** = warrant strike price
- **T** = time to expiry in years (months remaining / 12)
- **r** = risk-free rate (use 4.25% unless current Fed Funds rate differs materially)
- **q** = dividend yield (0% for most micro/small caps — verify)

**Method — Black-Scholes Inversion (iterative bisection):**

Since we cannot run code, use the following approximation approach:

1. **Starting estimate:** For an OTM call, IV ≈ W / (S × √(T/6.28)) × (K/S)^0.4 — this gives a rough starting point within ~15% of true IV.

2. **Refine via listed option comparison:** Find the listed call option on the chain with the most similar moneyness (S/K ratio) and closest DTE to the warrant's expiry. Use that option's Bloomberg IV as a proxy anchor, then adjust:
   - If warrant is cheaper per unit of time value than the comparable option → warrant IV is lower
   - If warrant is more expensive → warrant IV is higher
   - Directional adjustment: ±5-15 vol pts per 20% difference in time value

3. **Cross-check with ATM approximation:** For an option roughly ATM, σ ≈ (W / S) × √(2π / T). For OTM warrants, multiply by an OTM adjustment factor of (S/K)^0.5.

4. **Report the estimate with honest uncertainty:** "Warrant IV estimated at ~XX% (±5-10 pts; back-of-envelope BSM inversion — not a precise model price)."

**Why this matters:** The core warrant arb thesis is that front-end listed options trade at materially higher IV than the back-end warrant IV. If this differential is narrow (< 20 pts), the trade has weak theoretical support. If it is wide (> 40 pts), the arb signal is strong. The warrant IV estimate is the denominator of this calculation.

**Format for memo:**

```
Warrant Ticker:           [TICKER]W
Strike Price:             $X.XX
Expiration:               [DATE] (~XX months remaining)
Moneyness:                X.XX (XX% OTM / ITM)
Redemption Call Trigger:  $XX.XX / 20-of-30 trading days
Cashless Exercise:        [Yes/No — brief mechanics]
Registered:               [Yes/No]
Current Warrant Price:    $X.XX
Common Price:             $X.XX
Intrinsic Value:          $X.XX
Time Value:               $X.XX  (XX% of warrant price)
Implied Leverage:         X.Xx
Breakeven at Expiry:      $X.XX  (requires +XX% move in common)
Warrant IV (est.):        ~XX%   (±5-10 pts; BSM back-of-envelope)
Risk-Free Rate Used:      X.XX%
Comparable Listed Option: [TICKER] [Expiry] [Strike] C @ XX% IV — [DTE] DTE, [moneyness] moneyness

Key Risk: [1 sentence on biggest warrant-specific risk]
```

---

## Step 5: Volatility & Options Profile

This section answers two questions the traders need before putting on a trade:
1. **Are the options liquid enough to execute the short leg?**
2. **Are front-end options trading at a higher IV than the warrant (the arb signal)?**

Both must be confirmed. If either fails, flag the trade as not yet actionable.

**Tools:** `get-option-chain` (full chain, both calls and puts), `get-option-data` (specific contract details).

---

### 5a. Full Chain Liquidity Screen

Pull the **entire** option chain: `get-option-chain` with no strike or expiry filter, `option_type: "call"`. Then repeat for `option_type: "put"`.

For every expiration found, build a liquidity table:

```
Expiry       | DTE | Total OI | Best Call OI | Best Put OI | ATM Spread % | Verdict
-------------|-----|----------|--------------|-------------|--------------|--------
[Expiry 1]   |  XX |    XXX   |     XXX      |     XXX     |    XX%       | LIQUID / THIN / ILLIQUID
[Expiry 2]   |  XX |    XXX   |     XXX      |     XXX     |    XX%       | ...
```

**Liquidity definitions (apply per expiry):**
- **LIQUID:** Total OI ≥ 1,000 across all strikes AND ATM bid-ask spread ≤ 15% of mid
- **THIN:** Total OI 200–999 OR ATM spread 15–40% of mid — usable but expect slippage
- **ILLIQUID:** Total OI < 200 OR ATM spread > 40% of mid — delta hedge only

**For each LIQUID or THIN expiry, identify the single best short-leg candidate:** the individual strike with the highest OI, a reasonable bid (> $0.05), and spread < 30% of mid. This becomes a candidate for the short leg. Rank candidates across all expirations.

---

### 5b. IV Term Structure — Full Build

For each LIQUID/THIN expiry, pull the **ATM call** IV (use the strike closest to current stock price). Use `get-option-data` or read directly from `get-option-chain` results.

Build the full IV term structure table:

```
Expiry       | DTE | ATM Strike | ATM Call IV | ATM Put IV | P/C Skew  | Best Liquid Strike | Best Strike IV | Best Strike OI
-------------|-----|------------|-------------|------------|-----------|-------------------|----------------|---------------
[Expiry 1]   |  XX |   $X.XX    |    XX%      |    XX%     | +/-XX pts | $X.XX C           |    XX%         |   XXXX
[Expiry 2]   |  XX |   $X.XX    |    XX%      |    XX%     | +/-XX pts | $X.XX C           |    XX%         |   XXXX
[Expiry 3]   |  XX |   $X.XX    |    XX%      |    XX%     | +/-XX pts | $X.XX C           |    XX%         |   XXXX
WARRANT      | XXX |   $X.XX    |   ~XX%      |    N/A     |    N/A    | N/A               |    ~XX%        |   ~XXXK
(est. BSM)
```

The final row is the warrant IV estimate from Step 4. This is the anchor for the arb differential calculation.

**Reading the term structure:**
- **Normal (contango):** IV rises with DTE — front-end options cheaper than back-end. Weak arb environment.
- **Flat:** IV roughly equal across expirations. Moderate arb potential — warrant must be materially cheaper than listed options.
- **Inverted (backwardation):** Front-end IV > back-end IV — this is the ideal arb environment. Short elevated front-end vol, own cheap back-end vol via warrants.
- **Extremely inverted:** Front near-term IV > 100% while warrant IV < 50% — strong signal.

---

### 5c. Arb Signal Scoring — The Key Output

This is the number the traders need. Compute and display explicitly:

```
ARB SIGNAL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Warrant IV (estimated):           ~XX%  (back-end vol — what you're BUYING)
Best Short Leg IV:                 XX%  ([Expiry] [Strike] C — what you're SELLING)
IV Differential:                  +XX pts  ([Signal strength: STRONG / MODERATE / WEAK])
IV Ratio (short/warrant):         X.Xx  (e.g. 2.5x means front IV is 2.5x warrant IV)

All Expirations vs. Warrant IV:
  [Expiry 1] ATM IV:  XX%  →  +XX pts over warrant IV
  [Expiry 2] ATM IV:  XX%  →  +XX pts over warrant IV
  [Expiry 3] ATM IV:  XX%  →  +XX pts over warrant IV

Arb Signal: [STRONG / MODERATE / WEAK / NO SIGNAL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Signal strength definitions:**
- **STRONG:** IV differential ≥ 40 pts AND IV ratio ≥ 2.0x AND at least one LIQUID expiry
- **MODERATE:** IV differential 20–39 pts OR IV ratio 1.5–1.99x — worth monitoring, not yet compelling
- **WEAK:** IV differential < 20 pts OR IV ratio < 1.5x — front-end vol not sufficiently elevated
- **NO SIGNAL:** IV differential negative or warrant IV exceeds all listed options IV — do not put on the trade

**Important caveat to always include:** "Warrant IV is a back-of-envelope BSM estimate (±5-10 pts). The differential direction and order of magnitude are reliable; the precise number is not. Confirm with a proper options model before sizing."

---

### 5d. Short Leg Candidates — Ranked

Rank the top 3 executable short leg candidates by desirability. For each, note why it ranks where it does.

```
RANK | Contract          | IV    | OI    | Spread | IV Diff vs Warrant | Verdict
-----|-------------------|-------|-------|--------|-------------------|--------
  1  | [Exp] $XX.XX C    | XX%   | XXXX  |  XX%   |      +XX pts      | BEST — highest OI, tight spread
  2  | [Exp] $XX.XX C    | XX%   | XXXX  |  XX%   |      +XX pts      | GOOD — wider but more premium
  3  | [Exp] $XX.XX C    | XX%   | XXXX  |  XX%   |      +XX pts      | FALLBACK — thin but usable
     | DELTA HEDGE       | N/A   | N/A   | N/A    |       N/A         | If all options illiquid
```

**Selection criteria in priority order:**
1. OI ≥ 500 (minimum viable liquidity for entry/exit)
2. Bid-ask spread ≤ 25% of mid (execution cost)
3. IV differential vs. warrant ≥ 30 pts (arb cushion)
4. Strike selection: prefer OTM calls (higher IV, lower delta = less directional risk on the short leg)
5. DTE: prefer 45–90 days (sweet spot of theta decay vs. roll cost)

---

### 5e. Put/Call Skew — Sentiment Read

For the nearest LIQUID expiry, compare ATM call IV to ATM put IV:

```
ATM Call IV ([Expiry]):  XX%
ATM Put IV  ([Expiry]):  XX%
Skew (put - call):      +/-XX pts
→ Interpretation: [bullish / bearish / neutral]
```

- **Put IV > Call IV (positive skew):** Market hedging downside. Common is under distribution pressure. Supports short call / long put structure.
- **Call IV > Put IV (negative skew):** Retail call buying / squeeze risk. Short call leg has squeeze exposure — size down or prefer delta hedge.
- **Flat (< 5 pt skew):** No strong directional lean from options market.

---

### 5f. Options Data Quality Flag

Before leaving this section, note any data quality issues that affect execution:

```
Options Data Quality:
  Bloomberg IV data available:    [Yes / Partial / No]
  Expirations with live bids:     [X of Y found on chain]
  Stale/zero-bid contracts noted: [List any strikes with null bid prices]
  Warrant IV confidence:          [High / Medium / Low] — [1 sentence reason]
```

If Bloomberg IV is unavailable for key contracts (null `implied_vol` field), note the bid/ask mid and flag that IV was not directly available from Bloomberg — the mid price is reported instead.

---

## Step 6: Dilution Risk Rating

Reverse-engineer the DilutionTracker-style rating from Steps 2–3 using these definitions:

**Offering Ability**
- High: Active shelf with > $20M remaining OR pending S-1
- Medium: $1M–$20M shelf remaining
- Low: < $1M shelf capacity or no active shelf

**Overhead Supply (Total Potential Dilution excl. shelf)**
Compute: (Warrants + Converts + ATM/ELOC remaining) / Current Shares O/S
- High: > 50% dilution
- Medium: 20–50%
- Low: < 20%

**Historical Dilution Profile**
Check share count change over past 3 years via `edgar-company-facts`.
- High: > 100% O/S increase
- Medium: 30–100%
- Low: < 30%

**Imminent Cash Need** (from Step 2 cash runway)
- High: < 6 months runway
- Medium: 6–24 months
- Low: > 24 months or cash flow positive

**Overall Risk** = modal score across the four.

**Format:**
```
Overall Risk:      [High / Medium / Low]
Offering Ability:  [High / Medium / Low] — $XXM shelf remaining
Overhead Supply:   [High / Medium / Low] — XX% potential dilution
Historical:        [High / Medium / Low] — XX% O/S growth 3yr
Cash Need:         [High / Medium / Low] — ~XX months runway
```

---

## Step 7: Business Quality Flag

Not a full deep dive — just a quick three-point flag that tells us whether the business can survive long enough for the warrants to matter.

**Score each 🟢 / 🟡 / 🔴:**

1. **Is the business real?** Paying customers, real revenue, operating product. Search recent earnings, 10-Q.
2. **Path to profitability / sustainability?** Narrowing losses, gross margin trend, any FCF positive quarters. Check EDGAR cash flow and income statement.
3. **Management credibility?** Any recent insider buying (Form 4s via `edgar-ownership-search`), tenure, relevant experience. Search SEC + web.

**Format:**
```
Business Reality:        🟢/🟡/🔴 — [1 sentence]
Profitability Path:      🟢/🟡/🔴 — [1 sentence]
Management Credibility:  🟢/🟡/🔴 — [1 sentence]
```

**Survival Risk:** If 2 or more 🔴, flag: ⚠️ HIGH SURVIVAL RISK — warrants could expire worthless if company deteriorates.

---

## Step 8: Catalyst Analysis & PR Calendar

### 8a. Trailing 12-Month PR Summary

**Search:** `[COMPANY NAME] press release news 2024 2025 site:prnewswire.com OR site:businesswire.com OR site:globenewswire.com`

Also: `web_search "[TICKER] news announcements"` and scan 2–3 pages.

For each PR in trailing 12 months, note: **Date — Headline — 1-sentence summary.**

List them chronologically, then write a **3–4 sentence synthesis:** What kinds of news does this company generate? What's the PR narrative / investor story? How frequent are releases? What's likely coming next?

### 8b. Forward Catalyst Calendar

Pull or estimate the following known/likely events:

```
[DATE or ~DATE]  Earnings — Q[X] 2025 results
[DATE or ~DATE]  Earnings — Q[X] 2025 results
[DATE]           Lock-up expiration — [instrument]
[DATE]           Warrant expiration
[DATE or ~DATE]  Shelf registration renewal (if applicable)
[~DATE]          Expected PR type based on cadence (e.g. "product launch PRs ~monthly")
```

**For earnings dates:** `web_search "[TICKER] earnings date Q3 2025"` or check EDGAR for 8-K Item 2.02 pattern.

**Earnings = key vol event.** Note how many earnings remain before warrant expiry — each is a vol catalyst you can trade around on the short leg.

---

## Step 9: Sentiment & Market Positioning

### 9a. Short Interest

**Search:** `[TICKER] short interest short float days to cover`
Sources to check: Finviz, Ortex, iborrowdesk, Fintel, MarketBeat short interest pages.

Extract:
- Short % of float
- Days to cover
- Borrow rate / availability (easy, hard to borrow, HTB)
- Short interest trend (increasing / decreasing)

**⚠️ Data Gap — New deSPACs (< 12 months public):**
Standard short interest data providers often have incomplete or missing data for companies that have been public less than 12 months. This is expected, not a search failure. If hard numbers are unavailable, use these **proxy signals** instead and note the gap explicitly in the memo:

| Proxy Signal | What It Tells You |
|---|---|
| Company filed naked short complaint or hired counsel against short sellers | Management perceives active short pressure; borrow is likely HTB |
| 424B3 / prospectus supplements filed rapidly post-listing | SEPA shares hitting market = technical selling pressure, not traditional short interest |
| Daily volume as % of float > 20% on down days | Elevated short volume likely; float is tiny relative to trading activity |
| Bid-ask spread on borrow (iborrowdesk) > 50% annualized | Stock is HTB; short squeeze potential elevated |
| Stock fell > 30% within 3 months of listing | Typical deSPAC PIPE/redemption arbitrage selling; not the same as fundamental shorting |

For new deSPACs, always note: **"Standard short interest data unavailable — stock < 12 months public. [List any proxy signals found above.]"**

**Flag:** If short > 20% of float AND days to cover > 5, note **⚠️ SQUEEZE RISK**. For new deSPACs with proxy signals present, note **⚠️ SQUEEZE RISK (PROXY — data limited)**.

### 9b. Options Market Positioning (from Step 5)

Summarize: Is options OI skewed puts or calls? Any unusual call buying? This bleeds into warrant demand.

### 9c. Insider & Institutional Activity

**EDGAR `edgar-ownership-search`:** Recent Form 4 filings — are insiders buying or selling?

**Web search:** `[TICKER] 13F institutional holders 2025` — any known funds adding or exiting?

### 9d. Retail Sentiment

**Search:** `[TICKER] stocktwits reddit wallstreetbets`

Note: follower counts, recent post volume/tone, any viral moments. Flag if retail is heavily in calls (adds to squeeze risk on the short leg) or if sentiment is universally bearish (supports long warrant entry).

**Format:**
```
Short Float:      XX%
Days to Cover:    X.X
Borrow:           Easy / Hard / HTB  (~XX% annualized)
Short Trend:      Increasing / Decreasing / Flat
Insider Activity: [Brief — buying/selling/neutral, most recent Form 4]
Institutional:    [Brief — known holders, trend]
Retail Sentiment: [Brief — platform, tone, any notable activity]
Squeeze Risk:     Low / Medium / High
```

---

## Step 10: Trade Setup Summary

Synthesize everything into the actual trade structure recommendation. This is **not** a buy/sell call — it's a structured risk/reward summary for discussion.

```
PROPOSED STRUCTURE
  Long:  [WARRANT TICKER] @ ~$X.XX
  Short: [Front-month calls at $X.XX strike, ~XX DTE] OR [Long puts] OR [Delta hedge via common]
  Ratio: TBD — pending Greeks

TRADE THESIS (2–3 sentences)
  [Why the IV differential / vol structure supports this trade given the specific company setup]

KEY ENTRY CONDITIONS
  □ Warrant price at or below $X.XX (time value threshold)
  □ Front-end IV above XX% (short leg adequately priced)
  □ No lock-up expiration within 30 days of entry
  □ [Any company-specific trigger]

RISKS TO MONITOR
  ⚠️ [Top 3 risks, ranked — e.g. dilution event, warrant redemption call, options illiquidity]

WARRANT EXPIRY HORIZON
  XX months — [sufficient / tight] given current business trajectory

EXIT CRITERIA
  □ IV differential compresses to < XX pts
  □ Warrant approaches redemption call trigger ($XX.XX)
  □ Dilution event materially changes cap stack
  □ Business quality deteriorates (cash runway < 6 months)
```

---

## Step 11: Format & Deliver

Assemble the full memo in this order, formatted for email. Use compact tables where specified, plain prose elsewhere. No spreadsheet-style formatting — it needs to read cleanly in an email client.

```
═══════════════════════════════════════════════════════
WARRANT ARB MEMO — [COMPANY NAME] ([TICKER] / [WARRANTW])
[DATE]
═══════════════════════════════════════════════════════

COMPANY PROFILE
[Step 1 output]

FINANCIAL HIGHLIGHTS
[Step 2 table]

CAP STACK & OVERHANG
[Step 3 — prose intro + dilution table + lock-up calendar]

WARRANT TERMS
[Step 4 table + key risk note]

VOLATILITY & OPTIONS PROFILE
[Step 5 — IV term structure table + commentary + trade leg recommendation]

DILUTION RISK RATING
[Step 6 table]

BUSINESS QUALITY
[Step 7 three-point flag]

CATALYST & PR CALENDAR
[Step 8a PR list + synthesis + 8b forward calendar]

SENTIMENT & POSITIONING
[Step 9 table + brief commentary]

TRADE SETUP SUMMARY
[Step 10 full block]

DATA SOURCES
Bloomberg | SEC EDGAR | Web Search | [DATE pulled]
═══════════════════════════════════════════════════════
```

**Final check before delivering:**
- [ ] All prices are live (pulled today, not cached)
- [ ] Warrant expiry date confirmed from EDGAR
- [ ] Lock-up dates confirmed from EDGAR
- [ ] Any ⚠️ flags called out explicitly in Trade Setup Summary
- [ ] Email memo is self-contained — recipient needs no prior context

---

## Notes & Edge Cases

**No listed options:** If the company has no options market, note this explicitly. The short leg becomes a common stock delta hedge only — flag as **reduced arb efficiency**.

**Warrant very near expiry (< 6 months):** Flag prominently. The time value thesis is compressed. Warrant analysis is still valid but urgency is higher.

**Deeply ITM warrants:** If warrant is deep in the money (common >> strike), intrinsic value dominates. The vol arb thesis is weaker — closer to a straight equity trade.

**deSPAC with Crescent Term triggered:** If Step 0 identifies a Crescent-adjusted strike, use the ADJUSTED strike throughout. Reference the `warrant-analysis` skill for full Crescent mechanics.

**Missing data:** If Bloomberg tools return no data (e.g. company too small), fall back to EDGAR XBRL via `edgar-company-facts` for financials, and note the gap.

**SEPA with toxic floor + pre-revenue company:** This combination (zero revenue + YA II / variable-price SEPA with $1 floor) is the single most dangerous cap stack pattern for the long warrant leg. The floor creates a reflexive loop — stock drops → more shares issued per draw → more supply → stock drops further → warrants approach zero. If this pattern is present, flag it as the #1 risk in the Trade Setup Summary and recommend sizing the position conservatively until revenue inflects.
