# Nasdaq Delisting Rules Reference — Structured Equity Context

## Sources
- Low Price Requirement: SEC Release 34-104318 (Dec 10, 2025), operative Jan 19, 2026
- Prior Reverse Split Disqualification: SEC Release 34-102245 (Jan 23, 2025)
- Proposed $5M MVLS Rule: Federal Register 2026-01740 (filed Jan 13, 2026, published Jan 29, 2026)
- Standard bid price/MVLS/MVPHS rules: Nasdaq Listing Rules 5450, 5810

---

## Rule 1: Low Price Requirement — Rule 5810(c)(3)(A)(iii)

**Trigger:** Closing bid price ≤ $0.10 for **10 consecutive business days**

**Consequence:**
- Immediate Staff Delisting Determination
- Immediate trading suspension (stock moves to OTC pending appeal)
- NO compliance period
- NO stay of suspension during Hearings Panel appeal

**Timeline:** 10 business days ≈ 2 calendar weeks

**Key for exploding units:** If the offering craters the stock to ≤$0.10, the clock starts on Day 1 post-close. If warrant explosion creates massive sell pressure driving the stock down, you have ~2 weeks before the stock is suspended. You MUST monetize the position before Day 10.

**How to check:** Look at the post-offering expected price. If (Offering Price × expected dilution factor) ≤ $0.10, this rule is the binding constraint on the trade.

---

## Rule 2: Prior Reverse Split Disqualification — Rule 5810(c)(3)(A)(iv)

**Trigger:** Company executed a reverse stock split in the **prior 12 months** (or cumulative 250:1 in prior 2 years) AND stock falls below $1.00 for 30 consecutive business days.

**Consequence:**
- NO 180-day compliance period on the next bid price deficiency
- Immediate Staff Delisting Determination after 30 business days below $1.00
- Company can appeal to Hearings Panel (which may grant a stay, buying 60-90 days)

**Key for exploding units:** Most of these microcap issuers did a reverse split specifically to regain $1.00 compliance before the offering. The reverse split is typically within the last 12 months. This means if the offering drops the stock back below $1.00 (which it almost always does), there's NO cure period — just 30 business days to delisting determination.

**How to check:**
1. Search the filing for "reverse stock split", "share consolidation", "reverse split"
2. Search EDGAR 6-K filings for the prior 12 months
3. Search web for "[TICKER] reverse stock split"
4. Record: ratio, effective date, 12-month expiry date
5. Calculate: Is expiry date AFTER the expected offering close?

---

## Rule 3: Standard Bid Price Deficiency — Rule 5450(a)(1)

**Trigger:** Closing bid price below $1.00 for 30 consecutive business days

**Consequence (WITHOUT R/S in prior 12 months):**
- 180-day compliance period
- Must close at or above $1.00 for 10 consecutive trading days to cure
- May be eligible for additional 180-day period if meets other listing standards

**Consequence (WITH R/S in prior 12 months):**
- Rule 2 applies instead — NO compliance period

---

## Rule 4: MVLS Deficiency — Rule 5450(b)(2)(A) (Nasdaq Global Market)

**Trigger:** Market Value of Listed Securities below **$50 million** for 30 consecutive business days

**Consequence:**
- 180-day compliance period from notification date
- Must maintain MVLS ≥ $50M for 10 consecutive business days to cure
- If not cured → Staff Delisting Determination → can appeal to Hearings Panel

**Key for exploding units:** Most exploding unit targets are micro/nanocaps with MVLS well below $50M. If there's already a deficiency notice, check the cure deadline. The offering typically makes MVLS worse (more shares at lower prices = lower MVLS).

**Note:** For Nasdaq Capital Market (not Global Market), the MVLS threshold is $35M under Rule 5550(b)(2).

---

## Rule 5: MVPHS Deficiency — Rule 5450(b)(2)(C) (Nasdaq Global Market)

**Trigger:** Market Value of Publicly Held Shares below **$15 million** for 30 consecutive business days

**Consequence:** Same as MVLS — 180-day compliance period, then delisting determination.

**Note:** For Nasdaq Capital Market, the MVPHS threshold is $1M under Rule 5550(a)(2).

---

## Rule 6: Proposed $5M MVLS Rule (PENDING — Not Yet Effective)

**Source:** Nasdaq filed with SEC on Jan 13, 2026; published in Federal Register Jan 29, 2026 (2026-01740)

**Proposed Trigger:** MVLS below **$5 million** for 30 consecutive business days

**Proposed Consequence:**
- Immediate suspension of trading
- Immediate delisting determination
- NO compliance period

**Status:** SEC has 45-day action period from Federal Register publication. Could be effective as early as **March 2026**. Check current status before relying on this.

**Key for exploding units:** Many targets already have MVLS below $5M. If this rule is approved while you're in a position, it could trigger immediate delisting with no warning.

---

## Rule 7: Filing Delinquency — Rule 5250(c)(1)

**Trigger:** Failure to timely file periodic reports (20-F for foreign private issuers, 10-K/10-Q for domestic)

**Consequence:** Deficiency notice, typically 180-day cure period

**Key:** Often a sign of deeper problems (going concern, auditor issues). Check if the company has a history of late filings.

---

## Delisting Process Timeline

Once a Staff Delisting Determination is issued:
1. **Staff Determination** → Company has 15 calendar days to request a Hearings Panel hearing
2. **Hearings Panel** → Hearing scheduled within 30-45 days of request
3. **Panel Decision** → Typically within 30 days of hearing
4. **Total elapsed time from determination to final delisting:** 60-90 days
5. **During appeal:** Stock typically continues to trade UNLESS suspended under Low Price Rule

For Low Price Rule (≤$0.10): Trading is suspended **immediately** — no continued trading during appeal.

---

## How to Model Delisting Risk in the Excel

For each applicable rule, calculate:
1. **Days to trigger:** How many trading days until the threshold is breached (based on post-offering price estimates)
2. **Days to delisting:** Days to trigger + processing time (0 for Low Price, 30 for R/S trap, 180 for standard)
3. **Window to monetize:** Days to delisting minus settlement time (T+1)
4. **Volume needed per day:** Total shares to sell ÷ window days
5. **% of expected daily volume:** Volume needed vs. expected trading volume

If volume needed per day > 10-15% of expected daily volume, the position may be too large to liquidate safely.
