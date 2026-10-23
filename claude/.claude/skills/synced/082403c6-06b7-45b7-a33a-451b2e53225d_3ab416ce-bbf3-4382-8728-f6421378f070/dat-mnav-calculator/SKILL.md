---
name: dat-mnav-calculator
description: >
  Institutional-grade mNAV (market-value Net Asset Value) calculation for Digital Asset Treasury
  (DAT) companies — public equities holding cryptocurrency (BTC, ETH, SOL, BNB, or other tokens)
  as their primary treasury asset. Trigger this skill whenever the user asks to calculate, check,
  update, or analyze the mNAV, NAV discount/premium, ETH-per-share, BTC-per-share, hedge ratio,
  or ETHA/IBIT short ratio for any DAT company. Also trigger when the user says "what's the
  discount", "is this trading cheap to NAV", "update my mNAV model", "compute the hedge ratio",
  "how much ETHA do I short", or references mNAV in any context. Use this skill for MSTR, SBET,
  BMNR, BTBT, BTCS, DFDV, BNC, EMPD, SQNS, or any other DAT company. Do not attempt mNAV
  calculations ad hoc — always use this skill.
---

# DAT mNAV Calculator

## Purpose

Calculate filing-accurate mNAV multiples, EV bridges, per-share crypto exposure, and ETF hedge
ratios for Digital Asset Treasury companies. The output identifies relative value: long DAT
companies at a discount to NAV, with ETF shorts (ETHA, IBIT) or DAT peer shorts to hedge out
crypto direction and isolate the spread.

---

## DATA DATING STANDARDS — MANDATORY

Every data point in every mNAV output must carry an explicit as-of date and source citation.
No exceptions. Format:

  [Value]  (as of [DATE] | Source: [TOOL or FILING], [specific reference])

Every output must open with this header:

  ================================================
  [TICKER] mNAV SNAPSHOT
  Calculated:    [date and time of this calculation]
  Price data:    [Bloomberg timestamp for all prices]
  Holdings data: [as-of date of crypto holdings — filing date]
  Shares data:   [as-of date of share count — filing date]
  Filing basis:  [most recent 10-K or 10-Q used]
  STALE FLAGS:   [any data points exceeding staleness thresholds, or "None"]
  ================================================

Staleness thresholds — flag and note if exceeded:

  Crypto holdings, ATM-funded accumulator   >2 weeks old    re-run edgar-filings for newer 8-K
  Crypto holdings, active trader (BRR)      ANY AGE         always run Step 4.5 reconciliation
  Crypto holdings, stable accumulator       >1 quarter old  check for newer 10-Q or PR
  Share count, active ATM issuer            >2 weeks old    active issuers dilute continuously
  Share count, active buyback program       >2 weeks old    shares shrink via repurchases
  Cash / debt / preferred                   >1 quarter old  re-run balance sheet pull
  Crypto or stock prices                    >prior EOD      repull via Bloomberg get-price

---

## MCP TOOL USAGE

### Bloomberg MeteoraMCP: get-price

Used for all live price data — crypto, equities, and ETFs. All three asset classes
are pulled directly via this single tool using the correct Bloomberg identifier format.

CRYPTO TICKERS — verified resolving Bloomberg identifiers (as of March 2026):

  Asset             Bloomberg Ticker       Notes
  --------          ----------------       -----
  Bitcoin (BTC)     XBTUSD Curncy          Primary DAT reserve asset
  Ethereum (ETH)    XETUSD Curncy          Primary DAT reserve asset
  Solana (SOL)      XSOUSD Curncy          Primary DAT reserve asset
  XRP               XRPUSD Curncy
  Litecoin (LTC)    LTCUSD Curncy
  Bitcoin Cash      BCHUSD Curncy
  Stellar (XLM)     XLMUSD Curncy
  Dogecoin (DOGE)   XDGUSD Curncy
  Cardano (ADA)     XADUSD Curncy
  Avalanche (AVAX)  XAVUSD Curncy
  Polkadot (DOT)    XDOUSD Curncy
  Polygon (MATIC)   XMAUSD Curncy
  Cosmos (ATOM)     XATUSD Curncy
  Chainlink (LINK)  XLIUSD Curncy
  Uniswap (UNI)     XUNUSD Curncy
  Tether (USDT)     XDTUSD Curncy

  BNB               DOES NOT RESOLVE via Bloomberg — use CoinMarketCap manually
                    Label source explicitly: "CoinMarketCap as of [date/time]"

EQUITY TICKERS — standard Bloomberg format:

  "SBET US Equity"    "BMNR US Equity"    "MSTR US Equity"
  "BRR US Equity"     "BTBT US Equity"    "DFDV US Equity"
  "BTCS US Equity"    "EMPD US Equity"    "BNC US Equity"

ETF TICKERS — for hedge ratio sizing only, not crypto price discovery:

  "ETHA US Equity"    iShares Ethereum Trust (ETH hedge)
  "IBIT US Equity"    iShares Bitcoin Trust (BTC hedge)

Batch pull example — pull everything needed for one mNAV calculation in a single call:

  get-price(tickers=["XETUSD Curncy", "SBET US Equity", "ETHA US Equity"])

Always record the Bloomberg timestamp returned with each price. This is the "as of"
datetime for that data point in the output. Do not substitute the system clock.

If a ticker fails to resolve, note this explicitly in the output and state the
fallback source used with its timestamp.

---

### Bloomberg MeteoraMCP: get-company-info

Used to pull current shares outstanding, float, and market cap directly from Bloomberg.
This is a fast cross-check against filing-based share counts — useful for catching
recent ATM issuances between filing dates.

  get-company-info(ticker="SBET")

Returns: shares outstanding, float, market cap, sector, exchange.

Important: Bloomberg share counts for recently restructured or de-SPACed tickers can
be unreliable. Always confirm against the most recent EDGAR filing. Use this tool
as a supplement, not as the primary source for share count.

---

### MeteoraMCP EDGAR: edgar-filings

Lists available SEC filings for a company. Always run this first to identify the
most recent 10-K, 10-Q, and any 8-Ks filed after the last quarterly.

  edgar-filings(ticker="SBET", form_type="10-K")
  edgar-filings(ticker="SBET", form_type="8-K")

Parameters:
  ticker      SBET, MSTR, BMNR, BRR, BTBT, DFDV, BNC, EMPD, BTCS
  form_type   10-K, 10-Q, 8-K, DEF 14A, DEFM14A

Foreign filer exceptions:
  SQNS (Sequans)    files 20-F and 6-K, not 10-K
  BTBT (Bit Digital) files 20-F, not 10-K

Key 8-K triggers to check for (filed after the most recent 10-K):
  Item 8.01 Other Events        crypto holdings update — most common for ATM accumulators
  Item 3.02 Unregistered Sales  new share issuances under ATM or warrant exercises
  Item 2.01 Acq/Disposition     crypto purchases via put assignment or direct purchase (BRR)
  Item 1.01 Material Agreements new debt, ATM, or derivative contracts
  Item 7.01 Regulation FD       press releases — share buyback announcements, NAV updates

Always check: is there an 8-K filed after the 10-K? If yes, it likely contains
a more recent crypto holdings figure than the 10-K balance sheet.

---

### MeteoraMCP EDGAR: edgar-filing-index

Lists all documents and exhibits within a specific filing package.
Use to locate the correct exhibit before reading text.

  edgar-filing-index(accession_number="[from edgar-filings output]")

Look for:
  EX-99.1       press release inside an 8-K (holdings updates, ATM pricing)
  Primary 10-K  contains balance sheet and notes to financials
  DEF 14A       proxy — exec comp, RSU/option tables, warrant details

---

### MeteoraMCP EDGAR: edgar-filing-text

Reads full or partial text from a specific filing document.
Use grep-style numeric search — search for the known dollar or token quantity,
not keywords, to locate the right section quickly.

  edgar-filing-text(url="[from edgar-filing-index]", offset=0, max_chars=5000)

Navigation strategy for 10-Ks:

  Cover page share count        offset 0–5,000
  Balance sheet                 offset 80,000–200,000
  Notes to financials           offset 1,500,000–2,500,000
  Crypto holdings section       search for known quantity (e.g. "868,699") to pinpoint offset

---

### Standard Tool Call Sequence for a Full mNAV Calculation

  1. get-price(tickers=["XETUSD Curncy", "SBET US Equity", "ETHA US Equity"])
     → crypto price, stock price, ETF NAV — all with Bloomberg timestamps

  2. edgar-filings(ticker="SBET", form_type="8-K")
     → check for any 8-K filed after the most recent 10-K (updated holdings?)

  3. edgar-filings(ticker="SBET", form_type="10-K")
     → confirm the most recent annual filing date and accession number

  4. edgar-filing-index([10-K accession number])
     → locate primary financial statements document

  5. edgar-filing-text([doc URL], offset=0, max_chars=3000)
     → cover page: shares outstanding as-of date

  6. edgar-filing-text([doc URL], offset=100000, max_chars=10000)
     → balance sheet: cash, debt, preferred stock

  7. edgar-filing-text([doc URL], offset=1500000, max_chars=15000)
     → notes to financials: RSU tables, warrant terms, preferred liquidation values

  8. edgar-filing-text → Subsequent Events note (usually last note in financials)
     → post-balance-sheet transactions: note repurchases, share buybacks, crypto buys/sales,
       collateral disclosures, new debt. CRITICAL for Step 4.5 reconciliation.

  9. Read ALL post-10K 8-Ks identified in step 2 — especially Item 2.01 (crypto
     acquisitions/dispositions) and Item 7.01 (press releases with holdings/NAV data)

  10. edgar-filings(ticker="[TICKER]", form_type="DEFM14A") or form_type="DEF 14A"
      → proxy statement: merger consideration, exec comp, RSU/option tables, EIP terms,
        earnout triggers, employment agreements, equity plan amendments
      CRITICAL for de-SPACs and any company with a pending merger. Skip only if the
      company has no recent proxy and no pending M&A.

  11. From proxy/DEFM14A, extract:
      - Total merger consideration (base + earnout shares)
      - Employment agreements (base salary, signing bonus, RSU grants)
      - EIP pool size, evergreen %, amendment proposals
      - Sponsor/seller earnout triggers and auto-vest dates
      Build the Step 3.5 dilution waterfall from these inputs.

  12. From 10-K Income Statement or Cash Flow Statement, extract:
      - Total G&A expense (cash portion — subtract SBC)
      - Revenue (if any)
      - Compute annualized cash operating burn for Step 4.7

---

## Core mNAV Concepts

### Simple mNAV (P/NAV)

  mNAV = Market Cap / (Crypto Holdings x Crypto Price)

Use as a quick screen. Below 1.0x = market values the stock at a discount to its crypto.

### EV-based mNAV (preferred for rigor)

  EV = Market Cap + Total Debt + Preferred Stock Liquidation Value - Adjusted Cash
  Adjusted Cash = Unrestricted Cash - 1yr Operating Cash Burn Reserve
  EV mNAV = EV / (Crypto Holdings x Crypto Price)

Always use EV-based mNAV when a company has material debt or preferred stock.
The simple P/NAV overstates the common equity's crypto claim by ignoring senior claims
and the operating cost of maintaining the DAT strategy.

### NAV per Common Share

  Adjusted NAV = Crypto NAV - Debt - Preferred Liq. Value + Adjusted Cash
  NAV/share = Adjusted NAV / Shares at relevant dilution tier

Always present NAV/share at the 12-month-forward dilution tier as the primary
investable figure. The pre-dilution NAV/share is a reference point, not a target.

---

## Step-by-Step Calculation Procedure

### Step 1: Crypto Price

Pull directly from Bloomberg using the verified tickers above.
Record the Bloomberg timestamp verbatim — this is the price as-of datetime in output.

### Step 2: Crypto Holdings

Source hierarchy (use the most recent available):
  1. 8-K press release filed after the most recent 10-K (use edgar-filings to check)
  2. Most recent 10-K balance sheet
  3. Most recent 10-Q balance sheet

For ETH companies: distinguish native ETH, LsETH (liquid staked — at PCR redemption value,
subject to ~9-day exit queue), WeETH (wrapped ETH — at conversion rate), and USDC/stablecoin.

For ATM-funded accumulators (SBET, BMNR): holdings change weekly. Always check for a
post-10-K 8-K before relying on the 10-K figure. Flag if no 8-K within 2 weeks.

Never use company website dashboards as primary source — they often include pre-funded
warrants in their share denominator, structurally overstating reported mNAV.

CRITICAL — active crypto traders vs. passive accumulators:
  Some DAT companies actively BUY AND SELL crypto (e.g. BRR). Do NOT assume holdings
  only go up between filing dates. When large post-YE cash outflows (note repurchases,
  share buybacks, operating expenses) exceed available unrestricted cash, the company
  almost certainly sold crypto to fund those outflows. See Step 4.5 for reconciliation.
  The balance-sheet crypto figure is a STARTING POINT, not a current figure — you must
  adjust it for subsequent sales and purchases identified in post-YE 8-Ks, subsequent
  events disclosures, and the cash flow reconciliation.

### Step 3: Share Count

Source hierarchy:
  1. Most recent 8-K if filed after the last quarterly (ATM issuances disclosed here)
  2. Most recent 10-K or 10-Q cover page (shares outstanding as-of filing date)
  3. Bloomberg get-company-info — cross-check only; unreliable for de-SPACed tickers

Basic shares: common shares issued and outstanding. Use for the mNAV denominator.

Fully diluted shares: add to basic —
  Pre-funded warrants     treat as economically equivalent to shares (exercisable for $0.001)
                          include even though not on the cover page "shares outstanding"
  Unvested RSUs           include gross (before tax withholding) if vesting is near-term
  In-the-money warrants   apply treasury stock method
  Convertible notes       only if conversion is in-the-money (stock > conversion price)
  Equity plan reserve     EXCLUDE — unissued and uncommitted

Key distinction: company mNAV dashboards often include pre-funded warrants in their
"basic" count, inflating the denominator and making mNAV appear higher (less discount)
than the filing-based calculation. Always flag this discrepancy.

### Step 3.5: Full Dilution Waterfall (MANDATORY)

Every mNAV snapshot must present BOTH a pre-dilution mNAV (current basic shares) and a
dilution waterfall that catalogs every source of future share issuance with its trigger,
probability, and timeline. The output must show mNAV at multiple dilution scenarios.

Why this matters: A DAT company trading at 0.65x mNAV on basic shares can be 0.80x+ on
a forward diluted basis once you layer in imminent merger shares, RSU vesting, EIP
evergreen, and warrant exercises. The "discount" that looks investable on a headline
basis can be structurally illusory once dilution is properly modeled.

#### Source Documents for Dilution

Pull ALL of the following — do not rely solely on the 10-K:

  10-K Note: Stockholders Equity   warrants (public, private, placement agent), share counts
  10-K Note: Share-Based Comp      RSU grants, vesting schedules, performance milestones
  10-K Note: Recapitalization      de-SPAC share composition (founder, PIPE, public, sponsor)
  10-K Note: Subsequent Events     post-balance-sheet share issuances, merger consideration
  DEF 14A / DEFM14A               equity plan terms (pool size, evergreen), merger share count,
                                   executive comp (RSU tables, signing bonuses, bonus stock)
  8-Ks (Item 5.07)                shareholder vote results confirming dilutive proposals
  Sponsor/Seller Earnout Agreements  earnout shares, triggers, auto-vest provisions

For de-SPACed companies: always pull the proxy or DEFM14A in addition to the 10-K.
The proxy contains the complete merger consideration breakdown, earnout terms, and
employment agreements that drive incremental dilution post-close.

#### CRITICAL — Issued-and-Outstanding vs. Truly Incremental (VERIFY EVERY LINE)

This is the single most common error in DAT dilution analysis. Before adding ANY
dilution source to the waterfall, you MUST determine whether those shares are:

  (A) ALREADY ISSUED AND OUTSTANDING — shares that exist today, are on the cover
      page "shares outstanding" figure, vote at shareholder meetings, and participate
      in per-share economics. They may be transfer-restricted (locked up, subject to
      earnout vesting, not freely tradeable) but they ARE counted in basic shares.
      These are NOT incremental dilution — they are already in your denominator.

  (B) TRULY UNISSUED — shares that do not yet exist and will only come into being
      upon a future event (warrant exercise, option exercise, RSU settlement,
      convertible note conversion, merger closing, new ATM issuance, EIP grant).
      These ARE incremental dilution.

The distinction matters enormously. A de-SPAC with 82M basic shares may have 8.3M
sponsor shares and 9.5M seller earnout shares that are transfer-restricted. Adding
those 17.8M as "dilution" when they are ALREADY in the 82M double-counts them and
inflates the diluted share count by ~22%. This makes the fully diluted mNAV appear
far more expensive than reality.

VERIFICATION PROCEDURE — run for every line item in the dilution waterfall:

  1. Find the shares in the 10-K Note 4 (Recapitalization) share table or balance
     sheet equity section. The table that reconciles "shares available immediately
     after the Business Combination" is the definitive source for de-SPACs.

  2. Check: are these shares included in the total "shares issued" or "shares
     outstanding" figure on the balance sheet / cover page?
       If YES → they are Category (A). Do NOT add them to diluted count.
       If NO → they are Category (B). They ARE incremental dilution.

  3. For de-SPAC companies specifically, the following are almost always Category (A)
     — issued at close and ALREADY in the outstanding count:

       Sponsor/founder shares        issued at close in exchange for Class B shares
       Seller earnout shares          issued at close to the merger target's owners
       Private placement shares       issued to sponsor at IPO
       Representative shares          issued to underwriter
       PIPE conversion shares         issued at close upon preferred → common conversion

     These shares are subject to lock-ups or earnout restrictions on TRANSFER, but
     they are ISSUED and OUTSTANDING. The lock-up/earnout does not affect whether
     they are in the share count — it only affects when they can be SOLD. The unlock
     date creates a selling pressure event, not a dilution event.

  4. The following are almost always Category (B) — truly incremental:

       Public and private warrants     exercisable for new shares upon payment of strike
       Convertible note shares         created only upon conversion (if in the money)
       RSUs (unvested)                 settled in newly issued shares upon vesting
       EIP authorized pool             new shares issued upon future grant + vesting
       Merger consideration (unclosed) shares to be issued when a voted merger closes
       ATM shares                      new shares sold into the market under an ATM program
       Evergreen shares                automatic annual increase in authorized pool

  5. EDGE CASE — Earnout shares with auto-vest: Sponsor and seller earnout shares
     that auto-vest at the 2-year anniversary are Category (A) for share count
     purposes (already outstanding) but create a Category (A) SELLING PRESSURE event
     at the auto-vest date. Do not model them as incremental dilution. Do flag the
     auto-vest date as a potential overhang catalyst in qualitative notes.

If you cannot definitively determine whether a dilution source is Category (A) or
(B), FLAG IT and present both scenarios (with and without). Never silently assume.

#### EIP Pool vs. Individual RSU Grants — Avoid the Double-Count

The Equity Incentive Plan (EIP) pool and individual RSU grants draw from the SAME
authorization. They are not additive. The pool IS the RSU grants plus ungranted
remainder. You must choose ONE of these approaches:

  APPROACH 1 (Preferred — bottom-up by grant):
    List each individual RSU grant with its specific trigger, vesting schedule, and
    probability. Sum the individual grants. Then add only the REMAINING ungranted
    pool as separate "future grants" overhang.

    Example:
      Pomp performance RSUs:    8,000,000   (from EIP, at $15–$50 triggers)
      Cormier time-based RSUs:  1,650,000   (from EIP, 4yr vest)
      Park time-based RSUs:     1,600,000   (from EIP, 4yr vest)
      Remaining ungranted pool:   296,660   (= 8,516,660 initial pool - 8,220,000 granted)
      EIP amendment (if approved): 12,000,000 (incremental authorization)
      Annual evergreen:           ~4,160,000/yr (5% of prior YE shares)

  APPROACH 2 (Aggregate — simpler but less precise):
    Use the full EIP authorized pool as a single line item. Do NOT also list
    individual RSU grants separately. This avoids the double-count but loses
    visibility into which grants are likely to vest vs. remain theoretical.

  NEVER do both — listing individual RSU grants AND the full EIP pool simultaneously
  double-counts every RSU that was granted from the pool.

Also verify: do post-merger employment agreement RSU grants (e.g. CTO grant at close)
come from the existing EIP pool, or from a new authorization (amendment)? If the
existing pool is nearly exhausted (>80% granted), new grants almost certainly require
the amendment shares. Check the proxy Proposal 3 / EIP amendment for the additional
share count.

#### Convertible Notes — Use CURRENT Outstanding, Not Original Face

Convertible notes may have been partially repurchased, redeemed, or converted since
issuance. Always verify the CURRENT outstanding principal before computing potential
dilution shares:

  1. Check 10-K Note: Debt for the balance sheet carrying value and face amount
  2. Check Subsequent Events for post-balance-sheet repurchases
  3. Check post-10-K 8-Ks for additional repurchase transactions
  4. Compute: Dilution shares = Current face / Conversion price
     NOT: Original face / Conversion price

  Example: BRR issued $235M convertible notes, but repurchased $135.4M in Feb 2026.
  Current outstanding = $99.6M. Conversion at $13.00 = 7,659,240 shares (not 18.1M).

#### Dilution Waterfall Structure

Build the waterfall in order of certainty, from nearest-term to most remote:

  TIER 1 — IMMINENT (within 60 days, near-certain)
    Approved but unclosed mergers (stock consideration already voted on)
    RSUs with service-only vesting where service period is complete or near-complete
    ATM shares already issued but not yet in the latest filing

  TIER 2 — PROBABLE (within 12 months, high likelihood)
    EIP annual evergreen (automatic on Jan 1 each year — 5% of prior YE shares typical)
    Time-based RSU grants where vesting is ongoing (e.g. 4-year annual cliff)
    Employment agreement equity grants (e.g. Noor $4M RSU grant at close)
    Merger earnout shares where trigger is achievable (stock > target price)

  TIER 3 — CONTINGENT (requires specific conditions, uncertain timing)
    Performance RSUs with market-price milestones well above current stock
    Sponsor/seller earnout shares with auto-vest at period end (treat as certain at
    the auto-vest date even if share price triggers are unlikely)
    Warrants (public and private) — deeply OTM but with long expiration
    Convertible note conversion — only if conversion price is within striking distance

  TIER 4 — THEORETICAL MAXIMUM (everything in the money simultaneously)
    Full exercise of all warrants + full conversion of all converts + all RSU milestones
    hit + all earnout triggers achieved. Use for stress testing only.

For each dilution source, record:
  Source           [filing, note, section]
  Shares           [exact count or formula]
  Category         [A = already outstanding / B = truly incremental]  ← MANDATORY
  Trigger          [price target, service period, automatic date, board discretion]
  Probability      [near-certain / high / moderate / low / near-zero at current price]
  Timeline         [imminent / 12mo / 2yr+ / at expiration date]
  Verification     [cite the specific filing line that confirms A vs B classification]

Only Category (B) items increase the diluted share count. Category (A) items are
listed for completeness (selling pressure, overhang analysis) but DO NOT add to shares.

#### Key De-SPAC Dilution Traps

De-SPACed companies (BRR, others) carry multiple share classes that look like dilution
but are actually already outstanding. The critical discipline is to check EVERY item
against the 10-K Note 4 recapitalization table before classifying it.

ALREADY OUTSTANDING (Category A — do NOT add as dilution):

  Founder/sponsor shares      issued at close in exchange for Class B shares; subject to
                              earnout lock-ups but ALREADY in shares outstanding count.
                              The earnout vesting date is a SELLING PRESSURE event, not
                              a dilution event. Flag the date, but do not double-count.
  Seller earnout shares       issued at close to the original company's founders; locked
                              under transfer restrictions + price/BTC VWAP triggers. Auto-
                              vest at earnout period end (typically 2 years). Already in
                              shares outstanding. Same logic: selling pressure, not dilution.
  Representative shares       underwriter shares from SPAC IPO; small, already issued.
  Private placement shares    sponsor's co-invest at IPO; already issued.
  PIPE conversion shares      if preferred units converted to common at close, those common
                              shares are already issued and outstanding.

TRULY INCREMENTAL (Category B — add as dilution):

  Public & private warrants   exercisable for NEW shares; $11.50 strike typical. Only
                              dilutive if exercised. Apply treasury stock method if ITM.
  Pending merger shares       shares to be issued when an APPROVED but UNCLOSED merger
                              closes. These do not yet exist. (e.g. Silvia 9M base shares)
  RSUs (unvested)             will be settled in newly issued shares upon vesting. Use the
                              bottom-up grant approach, not the EIP pool aggregate.
  Convertible note shares     created only if conversion is triggered. Use current face.
  EIP ungranted pool +        truly incremental authorization that hasn't been issued yet.
  amendment + evergreen

COMMON ERROR: Adding sponsor earnout shares (8.3M) and seller earnout shares (9.5M)
on top of a basic count that already includes them. This overstates dilution by ~20%+.
The 10-K recapitalization table is the authoritative source — if those shares are in
the "shares issued immediately following the Business Combination" total, they are
Category (A) and must not be added again.

#### Dilution Scenario Table

Present mNAV at each scenario in the output:

  Scenario                         Shares          NAV/share    mNAV     Discount
  Pre-dilution (basic today)       [X]M            $[X]         [X]x     [X]%
  + Tier 1 (imminent)              [X]M            $[X]         [X]x     [X]%
  + Tier 1+2 (12-month forward)    [X]M            $[X]         [X]x     [X]%
  Full dilution (theoretical max)  [X]M            $[X]         [X]x     [X]%

The difference between pre-dilution and 12-month-forward mNAV is the "dilution drag."
If dilution drag exceeds ~10pp of mNAV, flag it — the headline discount is misleading.

### Step 4: Debt, Preferred, Cash

From the most recent balance sheet (10-K or 10-Q):

Debt: convertible notes at face/principal, term loans, DeFi borrowings (e.g. Aave for BTCS)

Preferred stock: use liquidation preference (face value), NOT market price
  MSTR has four series: STRK (8%), STRF (10%), STRC (variable), STRD (10%)
  Each series: $1,000 liquidation preference x shares outstanding per series
  All four must be deducted from BTC NAV before arriving at common equity's claim

Cash: cash and equivalents plus USDC/stablecoins; exclude restricted cash

### Step 4.5: Post-Balance-Sheet Cash Flow Reconciliation (MANDATORY)

This step catches crypto sales between the balance sheet date and today. Skip it only
if the most recent filing is <2 weeks old AND no material 8-Ks have been filed since.

Procedure:
  1. Read 10-K/10-Q Subsequent Events note — lists post-YE transactions (note repurchases,
     share buybacks, crypto acquisitions, debt issuances, etc.)
  2. Read ALL 8-Ks filed after the balance sheet date — look for Item 2.01 (acquisitions/
     dispositions), Item 8.01 (other events), Item 1.01 (material agreements)
  3. Build a post-balance-sheet cash flow waterfall:

     Starting unrestricted cash (from balance sheet)
     - Convertible note repurchases (cash paid, from 8-K or subsequent events)
     - Share repurchases (from 8-K or subsequent events)
     - Crypto purchases (from 8-K, include put option assignments)
     - Operating cash burn (estimate from last period's CF statement if material)
     + Cash from crypto sales (SOLVE FOR THIS if waterfall goes negative)
     + New debt issuances
     + ATM equity issuances
     = Estimated current unrestricted cash

  4. If the waterfall shows a NEGATIVE implied cash balance without crypto sales, then
     crypto WAS SOLD to fund the gap. Estimate the amount sold:
       BTC sold ≈ (cash shortfall) / (avg BTC price during the period)
     Use Bloomberg historical prices for the relevant date range.

  5. Cross-check against collateral disclosures: if the company has collateralized debt
     (e.g. BRR's convertible notes), subsequent events or 8-Ks often disclose the
     collateral composition (e.g. "3,000 BTC and $26.7M cash as of [date]"). This is a
     HARD CONSTRAINT on minimum holdings at that date — but total holdings may be higher
     if some BTC is unencumbered.

  6. Adjusted crypto holdings = Balance sheet holdings - Estimated sales + Post-YE purchases

  If the reconciliation is uncertain (e.g., insufficient disclosure to determine sales),
  FLAG THIS PROMINENTLY in the output and present a range:
    Low estimate: collateral-disclosed BTC + confirmed post-collateral-date purchases
    High estimate: balance sheet BTC + confirmed purchases (assumes no sales)

### Step 4.7: Operating Cash Burn Deduction (MANDATORY)

Cash on the balance sheet is NOT fully available to common equity holders — a portion
will be consumed by the operating business and the cost of running the DAT strategy.
Deducting this burn is essential for honest NAV computation.

Why this matters: A company showing $70M cash and $100M debt appears to have $30M net
debt. But if the business burns $20M/year in cash and generates negligible revenue,
one year of operations alone erodes the cash position to $50M — and the effective
net debt jumps to $50M. Ignoring this overstates NAV by the full PV of future burn.

#### Extracting Operating Cash Burn

Source the annual cash operating burn rate from:

  1. Cash Flow Statement → Operating Activities (most reliable)
     Use the "cash used in operating activities" line, but strip out non-cash items
     that are already added back (SBC, digital asset FV changes, depreciation).
     The key figure is: G&A (cash) + operating losses, net of any real revenue.

  2. Income Statement → Operating Expenses
     If the CF statement is from a stub period (de-SPACs), annualize:
       Annualized burn = (Total cash G&A / months in period) × 12
     Subtract stock-based compensation (non-cash) from total G&A to get cash G&A.
     Revenue offsets burn only if recurring and at-scale — most DATs have <$1M revenue.

  3. Post-filing incremental costs
     If a merger has been approved or employment agreements signed since the last
     filing, ADD the incremental comp costs:
       New executive base salary + bonus target + one-time signing bonus (if year 1)
       Acquired company's G&A run rate (from proxy/DEFM14A MD&A section)

#### Cash Burn Deduction Methodology

Deduct a 1-year forward operating cash burn reserve from unrestricted cash before
computing NAV to common. This represents the minimum cash that will be consumed by
operations and cannot be returned to shareholders through crypto holdings.

  Adjusted Cash = Unrestricted Cash - (1-Year Forward Cash Burn)

If Adjusted Cash goes negative, the deficit effectively becomes additional senior
claims against the crypto treasury — it means the company will need to either sell
crypto or raise equity to fund operations. This is a critical red flag: the operating
business is actively destroying crypto NAV.

  Adjusted NAV = Crypto NAV + Adjusted Cash - Debt - Preferred Liq. Value

If the company has material revenue that covers a meaningful portion of operating
costs, reduce the burn estimate accordingly. But be skeptical of "revenue" from
related-party transactions, one-time events, or pre-revenue product launches.

#### Presentation

Show the operating burn deduction explicitly in the capital structure section:

  CAPITAL STRUCTURE (with operating burn deduction)
    Debt:                    -$[X]M
    Preferred (liq. value):  -$[X]M
    Cash (unrestricted):     +$[X]M
    - 1yr operating burn:    -$[X]M    (Source: annualized from [filing period])
    = Adjusted cash:         +$[X]M
    NET NAV TO COMMON:        $[X]M

#### Sensitivity Note

The 1-year burn reserve is a baseline. For companies with high burn rates, low
revenue visibility, and large comp packages (e.g. BRR post-Silvia), the actual drag
may be higher. Present a range if the run-rate is uncertain:

  Conservative (burn × 1.0yr):  NAV/share = $[X]
  Extended (burn × 1.5yr):      NAV/share = $[X]

### Step 5: Compute mNAV

The mNAV must now be computed at MULTIPLE dilution scenarios using the burn-adjusted NAV.
Present all scenarios — the pre-dilution figure alone is insufficient.

Simple (headline only — use for quick screening, NOT for investment decisions):
  mNAV = (Stock Price x Basic Shares) / (Crypto Holdings x Crypto Price)

Adjusted EV-based (primary figure):
  Adjusted Cash = Unrestricted Cash - 1yr Operating Burn Reserve
  EV = (Stock Price x Basic Shares) + Debt + Preferred Liq. Value - Adjusted Cash
  EV mNAV = EV / (Adjusted Crypto Holdings x Crypto Price)

NAV per share (at each dilution tier):
  Adjusted NAV = Crypto NAV - Debt - Preferred Liq. Value + Adjusted Cash
  For each scenario:
    NAV/share = Adjusted NAV / Shares at that dilution tier
    mNAV = Stock Price / NAV/share
    Discount = (Stock Price / NAV/share) - 1

Dilution drag:
  Dilution drag = Pre-dilution NAV/share - 12mo-forward NAV/share
  If dilution drag > 10% of pre-dilution NAV/share, flag as material

Always present the 12-month-forward figure as the "investable mNAV" — this is the
discount that will actually accrue to shareholders given known dilution ahead.

---

## ETF Hedge Ratio Calculation

### Objective

Full delta hedge neutralizes all crypto price direction. P&L becomes purely a function of
mNAV convergence — not whether ETH or BTC goes up or down. This is the correct objective
for a pure discount-convergence trade.

### ETH Treasury Companies — Hedge with ETHA short

Step 1: ETH per DAT share
  ETH/share = Total ETH Holdings / Basic Shares Outstanding

Step 2: ETH per ETHA share (live from Bloomberg)
  ETHA_NAV = get-price("ETHA US Equity") → NAV field
  ETH/ETHA = ETHA_NAV / ETH_Spot

  Note: use live NAV, not the static prospectus ratio. ETHA's 0.25%/yr sponsor fee causes
  the ETH/ETHA ratio to drift down over time. Always recompute at entry and rebalance.

Step 3: Hedge ratio
  ETHA shares to short per 1 DAT share = ETH/DAT_share / ETH/ETHA_share

Example (SBET):
  ETH/share = 868,699 / 197,158,808 = 0.004406
  ETH/ETHA = $15.45 NAV / $2,098 ETH = 0.007364
  Hedge ratio = 0.004406 / 0.007364 = 0.598 ETHA per SBET
  Per 100K SBET long: short 59,800 ETHA

### BTC Treasury Companies — Hedge with IBIT short

  BTC/share = Total BTC Holdings / Basic Shares Outstanding
  BTC/IBIT = get-price("IBIT US Equity")[NAV] / get-price("XBTUSD Curncy")
  IBIT shares to short = BTC/share / BTC/IBIT

### Hedge Philosophy

  100% hedge    full delta neutralization; P&L = pure mNAV compression
                use when thesis is purely mean reversion of the discount

  50-65% hedge  preserves some crypto upside; use when a covered call buy-write
                is layered on top (the short call already caps upside — adding a
                full ETF short on top eliminates the double-trigger scenario)

  Never >100%   turns a long-discount trade into a net short crypto position

### Peer Hedge Alternative

Shorting a peer DAT instead of the ETF neutralizes both crypto price risk and
sector-level DAT sentiment simultaneously. Remaining P&L = purely idiosyncratic
discount compression.

  Example: Long SBET (~0.69x mNAV) / Short BMNR (~1.0x mNAV)
  Captures the ~31pp mNAV spread between two structurally similar ETH treasury companies
  Requires confirming the short leg has no near-term catalysts to widen the spread

---

## Company-Specific Notes

### SBET (Sharplink, Inc.) — ETH Treasury
  Crypto:        ETH — pull XETUSD Curncy
  ETF hedge:     ETHA US Equity
  Staking:       third-party validators (vs. BMNR's proprietary MAVAN infra)
  Options:       listed June 18, 2025; check chain before any buy-write sizing
  Dilution note: Consensys pre-funded warrants (~11.9M) are economically equivalent
                 to shares and must be in diluted count; company website includes these
                 in "basic", overstating their reported mNAV vs. filing-based calc

### BMNR (Bitmine Immersion Technologies) — ETH Treasury
  Crypto:        ETH — pull XETUSD Curncy
  ETF hedge:     ETHA US Equity
  Note:          ATM-funded accumulator — holdings move weekly, always check latest 8-K
                 MAVAN proprietary staking network is legitimate reason for premium
                 vs. SBET which delegates to third parties

### MSTR (Strategy Inc.) — BTC Treasury
  Crypto:        BTC — pull XBTUSD Curncy
  ETF hedge:     IBIT US Equity
  Capital stack: four preferred series (STRK, STRF, STRC, STRD) — all must be deducted
                 at liquidation preference before computing common equity's BTC claim
                 Omitting preferred massively overstates common NAV
  Note:          active ATM issuer — share count grows weekly; always check most recent 8-K

### BTCS — ETH Treasury (Hybrid)
  Crypto:        ETH — pull XETUSD Curncy
  Note:          uses Aave DeFi borrowing; add Aave debt to EV bridge or P/NAV is wrong
                 has real operating revenue (Builder+, NodeOps) — strip out for clean crypto NAV

### DFDV — SOL Treasury
  Crypto:        SOL — pull XSOUSD Curncy
  ETF hedge:     no liquid SOL ETF with short availability; use crypto futures or peer short

### BNC — BNB Treasury
  Crypto:        BNB — Bloomberg does NOT resolve; use CoinMarketCap manually
                 label source: "CoinMarketCap as of [date/time]"
  Note:          June $2.50 call only executable options contract as of last check

### BRR (ProCap Financial, Inc.) — BTC Treasury
  Crypto:        BTC — pull XBTUSD Curncy
  ETF hedge:     IBIT US Equity
  De-SPAC:       closed Dec 5, 2025 via CCCM merger. Inception June 17, 2025 — very
                 short operating history. Bloomberg share count may lag filings.
  ACTIVE TRADER: BRR actively buys AND sells BTC. Unlike pure accumulators (SBET, BMNR),
                 BRR executes large round-trip trades. Do NOT assume 10-K BTC holdings
                 are a floor — run the Step 4.5 cash flow reconciliation EVERY TIME.
  Put strategy:  BRR sells BTC put options to acquire BTC at target prices. When puts are
                 assigned, the company files Item 2.01 8-Ks disclosing the acquisition.
                 But it does NOT file 8-Ks for BTC sales — sales must be inferred from
                 the cash flow reconciliation.
  Convertible:   0.00% Convertible Senior Secured Notes due 2028. $235M original face.
                 $99.6M remaining after Feb 2026 repurchase. Conversion rate: 76.9 shares
                 per $1,000 = $13.00 conversion price. Deeply OTM at current stock levels.
                 Notes are collateralized by BTC (at 50% value) and cash (at 100% value).
                 Collateral disclosures in 8-Ks/subsequent events provide a HARD FLOOR
                 on BTC holdings at the disclosure date.
  Warrants:      public warrants (BRRWW), $11.50 strike. Deeply OTM.
  Share buyback: active open-market repurchase program while stock trades below NAV.
                 Check subsequent events and 8-Ks for updated share count after buybacks.

---

## mNAV Entry Framework

Entry thresholds:
  0.70x    watch list — track but do not initiate
  0.60-0.65x   entry zone — initiate position
  0.55x or below   add zone

Three-component structure at entry:
  1. Long stock at target mNAV price
  2. Sell covered call (20-30% OTM, 30-45 DTE) — generates immediate premium income
     that reduces effective cost basis regardless of convergence timing
  3. Short ETF hedge at 100% delta (pure convergence) or 50-65% (if buy-write caps
     upside and double-trigger scenario should be preserved)

P&L profile at full hedge (ETH direction fully neutralized):
  Entry at 0.65x, exit at 1.0x   +54% return on spread alone
  Entry at 0.60x, exit at 1.0x   +67% return on spread alone
  Plus call premium collected at entry adds further to effective return

---

## Output Format

  ================================================
  [TICKER] mNAV SNAPSHOT
  Calculated:    [date and time]
  Price data:    [Bloomberg timestamp]
  Holdings data: [filing as-of date]
  Shares data:   [filing as-of date]
  Filing basis:  [e.g. 10-K FY2025 filed Mar 9 2026]
  STALE FLAGS:   [list or "None"]
  ================================================

  SHARE COUNT (Pre-Dilution)
    Basic shares:           [X]M   (as of [date] | Source: [10-K/8-K cover page])
    + Pre-funded warrants:  [X]M   (as of [date] | Source: [filing, note X])
    Adjusted basic:         [X]M

  DILUTION WATERFALL
    Source                        Shares     Cat.  Trigger                     Probability
    -----                         ------     ----  -------                     -----------
    [Sponsor earnout shares]      [X]M       A     [already outstanding, locked] N/A — in basic
    [Seller earnout shares]       [X]M       A     [already outstanding, locked] N/A — in basic
    [Pending merger shares]       +[X]M      B     [approved, pending close]   Near-certain
    [EIP evergreen 2026]          +[X]M      B     [automatic Jan 1]           Certain
    [Time-based RSUs]             +[X]M      B     [4yr vest from grant]       High
    [Performance RSUs]            +[X]M      B     [stock ≥ $X for 5 days]    [Low/Near-zero]
    [Public warrants]             +[X]M      B     [$X strike, exp date]       [Near-zero]
    [Private warrants]            +[X]M      B     [$X strike]                 [Near-zero]
    [Convertible notes]           +[X]M      B     [$X conv. price, current face] [Near-zero]
    [Merger earnout]              +[X]M      B     [VWAP ≥ $X]                [Low/Moderate]

    Cat. A = already in basic shares (selling pressure only, NOT incremental dilution)
    Cat. B = truly incremental (adds to diluted share count)

  CRYPTO HOLDINGS
    [Token] held:           [X]    (as of [date] | Source: [filing, pg/section])
    x Crypto price:         $[X]   (as of [date/time] | Source: Bloomberg, [ticker])
    = Crypto NAV:           $[X]M

  CAPITAL STRUCTURE (with operating burn deduction)
    Debt:                  -$[X]M  (as of [date] | Source: Balance sheet)
    Preferred (liq. value):-$[X]M  (as of [date] | Source: [Note X])
    Cash (unrestricted):   +$[X]M  (as of [date] | Source: [filing/PR/reconciliation])
    - 1yr operating burn:  -$[X]M  (Source: annualized from [period], [filing])
    = Adjusted cash:       +$[X]M

  NAV TO COMMON (Adjusted)
    Crypto NAV:             $[X]M
    + Adjusted cash:        $[X]M
    - Debt:                -$[X]M
    - Preferred:           -$[X]M
    = Net NAV to Common:    $[X]M

  mNAV BY DILUTION SCENARIO
    Scenario                         Shares    NAV/shr   mNAV    Discount
    Pre-dilution (basic today)       [X]M      $[X]      [X]x    [X]%
    + Tier 1 (imminent)              [X]M      $[X]      [X]x    [X]%
    + Tier 1+2 (12-month forward)    [X]M      $[X]      [X]x    [X]%
    Full dilution (theoretical max)  [X]M      $[X]      [X]x    [X]%
    Dilution drag (basic → 12mo):    [X]pp

  HEDGE RATIO (use 12-month-forward share count for sizing)
    [Token]/share (stock):  [X]    ([holdings] / [12mo-forward shares])
    [Token]/share (ETF):    [X]    (ETF NAV $[X] / [Token] $[X] | Bloomberg [date])
    Hedge ratio:            [X] [ETF] per [stock] share
    Per 100K shares long:   short [X] [ETF] (~$[X]M notional)

  ENTRY LEVELS (at current [Token] price of $[X], 12mo-forward basis)
    0.65x entry:            $[X]
    0.60x entry:            $[X]
    0.55x entry:            $[X]

  Formula: entry_px = mNAV_target x (Adjusted NAV / 12mo_forward_shares)

