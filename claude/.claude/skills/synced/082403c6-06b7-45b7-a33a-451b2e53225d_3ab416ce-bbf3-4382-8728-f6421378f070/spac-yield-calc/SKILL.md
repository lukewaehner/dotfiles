---
name: spac-yield-calc
description: "Calculate annualized SPAC redemption yield (IRR) for any ticker. Trigger when the user asks to 'calculate yield', 'run yield', 'what's the yield on [ticker]', 'annualized return', 'yield to trust', 'yield to redemption', 'IRR on [ticker]', or any request to compute the return profile of a SPAC position trading below trust. Also trigger when user asks 'what's the arb on [ticker]', 'how much discount to trust', 'trust spread', 'how does [ticker] yield compare', or references buying SPACs at a discount and wanting to know the return. Produces a full yield table with multiple scenario timelines sourced from SEC filings, Bloomberg pricing, and internal SPAC data. Supersedes manual yield calculations — systematic, multi-source, skeptical-timeline approach."
---

# SPAC Redemption Yield Calculator

## Overview

This skill calculates the annualized IRR on a SPAC position purchased at market price and redeemed/liquidated at trust value. It produces a multi-scenario yield table covering optimistic-to-pessimistic closing timelines, incorporating trust accrual at the current risk-free rate.

**Core Formula (with trust leakage):**
```
gross_interest = current_CIT × T-bill_rate × days_to_exit / 365
tax_leakage    = gross_interest × tax_rate
wc_leakage     = gross_interest × wc_rate   (capped at wc_annual_cap × days/365 if applicable)
net_accrual    = gross_interest - tax_leakage - wc_leakage
CIT_at_exit    = current_CIT + net_accrual
Annualized IRR = (CIT_at_exit / purchase_price)^(365 / days_to_exit) - 1
```

**Simplified shorthand (retention rate):**
```
retention_rate = 1 - tax_rate - wc_rate
CIT_at_exit = current_CIT + (current_CIT × T-bill_rate × days_to_exit / 365) × retention_rate
```

Where:
- `current_CIT` = cash in trust per share (from spac-details — already reflects all historical withdrawals)
- `T-bill_rate` = current 3-month T-bill yield (from Bloomberg USGG3M Index, divided by 100)
- `purchase_price` = current market price (from Bloomberg get-price)
- `days_to_exit` = calendar days from today to each scenario exit date
- `tax_rate` = estimated tax rate on trust interest income (see Step 0g for extraction)
- `wc_rate` = working capital withdrawal rate as % of interest (see Step 0g for extraction)
- `wc_annual_cap` = annual dollar cap on working capital withdrawals, if any (converted to per-share)

**Why this matters:** SPACs do NOT retain 100% of trust interest. They withdraw cash for (1) federal/state income taxes on interest earned, (2) working capital to fund operating expenses, and (3) occasionally franchise taxes or excise taxes. Ignoring this leakage systematically overstates CIT@EXIT and therefore overstates yield — especially for longer-dated scenarios where cumulative leakage is material. The `current_CIT` from spac-details already reflects all past withdrawals, so only FUTURE leakage between today and exit needs to be modeled.

---

## Step 0: Gather All Inputs (Parallel)

Fire ALL of these tool calls simultaneously. Do not wait for one before starting the next.

### 0a. Internal SPAC Data
```
spac-details(ticker="[TICKER]")
```
**Extract:**
- `cash_in_trust` → CIT per share
- `trust_balance` → total trust $
- `ipo_date` → needed for 24-month liquidation math
- `max_deadline` → hard liquidation deadline
- `est_date` → internal estimated closing date (treat as ONE scenario, not gospel)
- `est_yield` → internal estimated yield (for cross-check only)
- `stage` → predeal vs indeal (changes which scenarios apply)
- `deal_announced` → BCA signing date
- `s4_amendments` → count of S-4/A filings (proxy progress indicator)

### 0b. Bloomberg Pricing
```
get-price(tickers=["[TICKER]"])
```
- Common price → `purchase_price`

Also fetch the risk-free rate:
```
get-price(ticker="USGG3M Index")
```
- Price field / 100 → `T-bill_rate` (this is the =BDP("USGG3M Index","PX_LAST")/100 equivalent)

### 0c. SEC Filings — Determine Timeline

**Registration statements are the single most important input to the timeline.** Miss the S-4 or F-4 and every downstream scenario is wrong. The default `edgar-filings(ticker=[TICKER])` call often misses them for two reasons: (1) a heavily-screened SPAC may have many 13G/A, Form 4, and 425 filings that push the registration statement outside the default `limit=20` window, and (2) **for foreign private issuer (FPI) deals, the registration statement is filed under the PubCo CIK, not the SPAC's CIK** — so the SPAC ticker query returns nothing.

**Mandatory three-pass workflow — do ALL three, do not stop after pass 1:**

**Pass 1 — Broad listing on the SPAC's own CIK:**
```
edgar-filings(ticker="[TICKER]", limit=30)
```
Scan for recent activity, 10-Ks, 10-Qs, DEFM14A, and any obvious registration statement.

**Pass 2 — Targeted registration-statement filter on the SPAC's CIK (ALWAYS run even if pass 1 looked complete):**
```
edgar-filings(ticker="[TICKER]", form_type="S-4", limit=10)
edgar-filings(ticker="[TICKER]", form_type="S-4/A", limit=10)
edgar-filings(ticker="[TICKER]", form_type="F-4", limit=10)
edgar-filings(ticker="[TICKER]", form_type="F-4/A", limit=10)
edgar-filings(ticker="[TICKER]", form_type="DRS", limit=10)
edgar-filings(ticker="[TICKER]", form_type="DRS/A", limit=10)
```

**Pass 3 — PubCo CIK fallback (MANDATORY if the target is a non-US entity, the underwriter/sponsor description mentions "FPI" or "foreign private issuer", or passes 1–2 returned zero registration statements despite the deal being announced >60 days ago):**

FPI deSPACs (Cayman, BVI, UK, Israel, etc. targets) almost always register the deal under a newly-formed PubCo rather than the SPAC. To find the PubCo CIK:
```
web_search: "[TARGET NAME] Limited F-4 SEC EDGAR"
web_search: "[TARGET NAME] [PubCo variant] SEC registration statement"
```
Look for SEC Archives URLs of the form `/data/[CIK]/...` — that number is the PubCo CIK. Then run:
```
edgar-filings(cik="[PUBCO_CIK]", limit=20)
```
The F-4 and DRS will be there. Note: PubCos often have only 2–3 total filings (DRS + F-4 + maybe F-4/A), so a short response with the registration statement at the top is normal.

**Red-flag heuristic — if pass 1 + pass 2 on the SPAC's CIK return no S-4, F-4, or DRS AND deal_announced is >60 days ago, DO NOT CONCLUDE "no registration statement filed." Pass 3 is required.** Incorrectly reporting "no F-4 yet" on a name where one exists under a PubCo CIK causes the skill to invent a 16–20 week "add from today" buffer that does not apply, and systematically overstates days-to-close by 3–6 months.

Once you have a complete filings picture from all three passes, interpret proxy progress:
- **S-4 or F-4 filed publicly?** → Registration statement is live. Earliest realistic close is ~10–16 weeks from initial filing (depends on amendment rounds).
- **S-4/A or F-4/A filed?** → SEC had comments. Each amendment round = 3–6 weeks typical. Count them.
- **DRS only (no public F-4/S-4)?** → Confidential draft on file but not yet public. Target is almost certainly an FPI or EGC using confidential review. Realistic close adds 2–4 months to account for the DRS → public flip → amendments cycle.
- **DEFM14A filed?** → Definitive proxy mailed; vote is typically 10–20 business days after mailing.
- **8-K with Item 2.01?** → Deal already closed; yield calc is moot.
- **No S-4/F-4/DRS after all three passes?** → Pre-proxy. Add minimum 16–20 weeks from today for realistic close.
- **IPO date > 18 months ago?** → SPAC is likely in extension territory. **MANDATORY: run the extension 8-K search in Step 0d.5 before proceeding.** Extension deposits may already be accruing to trust and must be modeled in CIT@EXIT. Do NOT assume the Articles of Association contain the deposit terms — check 8-Ks (Item 1.01, 2.03) filed around the IPO anniversary date.

**⚠ CRITICAL — POST-DEFM14A SUPPLEMENT CHECK:**
Once a DEFM14A is identified, you are NOT done. You MUST scan all filings dated AFTER the DEFM14A for any of the following supplement types that can change the meeting date, redemption deadline, or deal terms:
- **DEFA14A** — Additional definitive proxy soliciting material. Often contains postponement notices, updated meeting dates, or revised deal terms.
- **424B3 / 424B4** — Prospectus supplements to the registration statement. Frequently used to announce meeting postponements, extended redemption deadlines, or updated closing timelines.
- **8-K (post-DEFM14A)** — May disclose adjournments, BCA amendments, extension deposits, or other material changes.

**Always read the most recent DEFA14A and/or 424B3/B4 after the DEFM14A date.** Meeting dates printed in the original DEFM14A are frequently superseded by these supplements. Do NOT assume the DEFM14A meeting date is still current — verify against all subsequent filings. This is a common source of error: the DEFM14A says "March 17" but a 424B3 filed two weeks later pushes it to "March 30."

### 0d. SEC Filing Deep Dive — Extract Hard Dates and Extension Terms

Once you have the filing list (including any PubCo-CIK filings from Pass 3), read the **latest registration statement (S-4, S-4/A, F-4, or F-4/A — whichever applies)** to extract:

1. **Expected closing language**: Use `edgar-filing-text` with `summary=true` to find the Q&A section, then read the "When do you expect the Business Combination to be completed?" answer.
2. **Outside Date / Agreement End Date**: Find the "Termination" section. Extract:
   - First Outside Date
   - Any extension provisions (who can extend, how many times, to what dates)
   - Any auto-extension provisions triggered by counterparty delays (e.g., "+1 day per day financials late past [date]") — these can materially push the effective Outside Date without any party action
   - Final Outside Date (after all extensions)
3. **Meeting date**: Check if a specific date is set (often blank in S-4/F-4, filled in DEFM14A). **Then verify against any post-DEFM14A supplements per Step 0c above.**
4. **Minimum Cash Condition (MCC)**: Relevant for whether deal can close at high redemption.

**Important — for F-4 registrants (FPI deals), the filing is under the PubCo CIK, so pass the PubCo CIK (not the SPAC ticker) when reading the document:**
```
edgar-filing-text(accession_number="[ACCESSION]", cik="[PUBCO_CIK]", summary=true)
```
Passing `ticker=[SPAC_TICKER]` in that case will fail to resolve because the filing's CIK is the PubCo's, not the SPAC's.

5. **Extension deposit terms**: Extract from ALL of the following sources — do NOT stop at the first one that seems empty:
   - **Articles of Association / Amended Articles** section in the S-4 or DEFM14A for any deposit language.
   - **⚠ CRITICAL — EXTENSION 8-Ks (MANDATORY SEPARATE SEARCH):** Extension deposits are frequently NOT in the Articles of Association. They are often structured as standalone promissory notes or contribution agreements disclosed ONLY in 8-Ks filed around the IPO anniversary date. The Articles may just say "the board may extend" with zero mention of deposits — but a separate 8-K filed the same week may disclose a per-share deposit obligation via promissory note. **You MUST run a filtered 8-K search to catch these:**
     ```
     edgar-filings(ticker="[TICKER]", form_type="8-K", filing_date="[IPO_ANNIVERSARY - 2 months]:[TODAY]")
     ```
     Then read each 8-K's Item headers. Look for:
     - **Item 1.01** (Entry into Material Definitive Agreement) — promissory notes, contribution agreements, sponsor deposit commitments
     - **Item 5.03** (Amendments to Articles) — articles amendment approving the extension
     - **Item 2.03** (Creation of Direct Financial Obligation) — often cross-references the promissory note from Item 1.01
     - **Item 8.01** (Other Events) — sometimes used for extension deposit confirmations
     Read the full text of any 8-K that contains Item 1.01 or Item 2.03 around the extension date. The deposit terms (per-share amount, cap, frequency, source) will be in the promissory note or contribution agreement description.
   - Extract:
     - Per-share deposit amount per extension period
     - Any aggregate cap (e.g., "$375,000 per month" caps the per-share amount at high share counts)
     - Frequency (monthly, per 3-month extension, per 6-month extension, etc.)
     - Source of funds (sponsor, promissory note, target contribution)
     - Start date of deposits (first extension date)
     - How many deposits have already been made (count months from first deposit to today)

If no registration statement (S-4, F-4, or DRS) exists yet after all three passes in Step 0c, search the 8-K announcing the BCA (usually the 8-K filed on the `deal_announced` date under the SPAC's CIK) for outside date terms.

### 0e. Web Search — Supplementary Timeline Intel
```
web_search: "[TICKER] SPAC closing timeline [YEAR]"
web_search: "[TARGET NAME] merger vote date"
```
Look for:
- Press releases with updated closing estimates
- Any event deadlines that create hard constraints (e.g., Enhanced Games for APAD)
- Analyst or news coverage with independent timeline estimates

### 0f. User-Provided Dates (if any)

The user may provide additional dates to include as scenarios (e.g., "also run it for July 15"). Always include these in the output table.

### 0g. Trust Leakage — Working Capital Withdrawals and Tax Drain

**This step is MANDATORY.** Trust interest does not accrue dollar-for-dollar to CIT. SPACs routinely withdraw interest for working capital and taxes. Failing to model this overstates CIT@EXIT and inflates yield — the error compounds with time and is most material for longer-dated scenarios (pre-deal SPACs approaching max deadline, extended-timeline in-deal names).

#### What to Extract

From the **IPO prospectus (S-1), 10-K, 10-Q, or S-4 Note 1 ("Organization and Business Operations")**, extract the following trust withdrawal terms:

1. **Working Capital Withdrawal Cap**: Most SPACs allow the sponsor/company to withdraw a portion of interest earned for working capital. Common structures:
   - **Percentage of interest**: e.g., "up to 5% of interest earned annually" (HVII), "up to 10% of interest"
   - **Flat dollar amount**: e.g., "up to $500,000 per year" or "up to $100,000 per month"
   - **No cap on interest withdrawals**: Some SPACs allow unlimited interest withdrawals for working capital (flag this — the SPAC may be draining trust aggressively)
   - **No withdrawals permitted**: Rare but possible — all interest stays in trust until close/liquidation

2. **Tax Withdrawals**: Almost all SPACs allow unlimited withdrawal of interest to pay income taxes. This is typically NOT capped. The key variable is the effective tax rate:
   - **Cayman/Jersey domiciled SPACs**: Often 0% entity-level tax (no income tax on trust interest at the entity level). BUT if the trust is a US grantor trust or interest is US-source, there may still be withholding. Check domicile in spac-details.
   - **Delaware/domestic SPACs**: Subject to federal corporate income tax (~21%) plus state taxes (varies: DE franchise tax is modest, but if the SPAC has nexus in high-tax states, effective rate can be 25%+).
   - **Practical shortcut**: Look at the 10-K income tax note or the trust reconciliation in the 10-Q. Compare beginning-of-period trust balance + interest earned vs. end-of-period trust balance. The difference (minus any extension deposits IN) = total withdrawals. Divide by gross interest to get the historical leakage rate.

3. **Dissolution Expense Reserve**: Some SPACs reserve a small amount of interest for dissolution costs (e.g., "$100,000 of interest to pay dissolution expenses"). This is usually immaterial but should be noted.

4. **Excise Tax (1% buyback tax)**: Since 2023, the federal excise tax on stock buybacks applies to SPAC redemptions. This is assessed on the SPAC entity at year-end based on net redemptions during the year. It reduces total trust but is typically small (~$0.03-$0.10/share depending on redemption volume). Note for completeness but do NOT deduct from CIT@EXIT unless the user specifically asks for post-excise yield.

#### How to Extract (Practical Workflow)

**Primary source**: Read Note 1 of the most recent 10-K or 10-Q (or the HVII financial statements section of the S-4 if no standalone 10-K/10-Q is recent). Search for:
- "permitted withdrawals"
- "working capital requirements"
- "annual limit"
- "interest earned on the funds held in the Trust Account"
- "to pay its taxes"
- "released to the Company"

**Secondary source (for actual historical leakage)**: Read the trust account reconciliation in the 10-K/10-Q. Look for the "Cash Held in Trust Account" note or the trust roll-forward table. Calculate:
```
historical_leakage_rate = (gross_interest_earned - net_trust_increase) / gross_interest_earned
```
This gives you the empirical leakage rate, which is often more accurate than the theoretical cap because (a) some SPACs withdraw less than permitted, and (b) tax rates vary.

#### Default Assumptions (when extraction fails or is ambiguous)

If you cannot extract specific terms, use these conservative defaults:

| Domicile | Tax Rate | WC Rate | Total Leakage | Retention Rate |
|----------|----------|---------|---------------|----------------|
| DE / domestic | 21% | 5% | 26% | 74% |
| KY (Cayman) | 0%* | 5% | 5% | 95% |
| Jersey / BVI | 0%* | 5% | 5% | 95% |

*Cayman/offshore SPACs: The entity itself pays 0% income tax. However, the trust is typically held in US T-bills via a US trustee, so there may be US withholding on interest. In practice, most Cayman SPACs still lose some interest to franchise taxes, state taxes, or other leakage. Use 0% tax as default for Cayman but flag if the 10-K shows material tax payments.

**IMPORTANT**: These are defaults. Always attempt to extract actual terms first. The defaults are fallbacks, not substitutes for reading the filings.

#### Modeling in the Yield Calc

Apply the retention rate to the gross interest accrual:

```python
# After extracting terms:
retention_rate = 1 - tax_rate - wc_rate  # e.g., 1 - 0.21 - 0.05 = 0.74

for scenario_name, exit_date in scenarios.items():
    days = (exit_date - today).days
    gross_interest = current_cit * tbill_rate * days / 365
    net_accrual = gross_interest * retention_rate
    cit_at_exit = current_cit + net_accrual
    ann_irr = (cit_at_exit / purchase_price) ** (365 / days) - 1
```

If the working capital cap is a flat dollar amount rather than a percentage:
```python
wc_annual_cap_per_share = wc_annual_cap_dollars / public_shares_outstanding
wc_leakage = min(gross_interest * wc_pct, wc_annual_cap_per_share * days / 365)
net_accrual = gross_interest - (gross_interest * tax_rate) - wc_leakage
```

---

## Step 1: Build the Scenario Timeline

### Mandatory Scenarios (always include)

Generate scenarios from the data gathered. Every yield table MUST include:

| # | Scenario | Source | Notes |
|---|----------|--------|-------|
| 1 | **Optimistic Close** | Earliest realistic date based on filing progress | See Filing Progress Heuristics below |
| 2 | **Company Estimated Close** | S-4 language / press release | ALWAYS label this clearly as company's own estimate |
| 3 | **Realistic Close** | Skeptical adjustment to company estimate | See Skeptical Timeline Rules below |
| 4 | **First Outside Date** | BCA termination section | Hard contractual date |
| 5 | **Final Outside Date** | After all extensions exercised | Worst-case deal close |
| 6 | **Max Liquidation** | max_deadline from spac-details OR IPO date + 24 months | Yield floor if deal fails entirely |

Plus any user-provided dates as additional rows.

### Filing Progress Heuristics — "Optimistic Close"

Use this to estimate the EARLIEST realistic closing date based on where the proxy process stands today:

| Current Status | Minimum Additional Time to Close |
|---|---|
| No registration statement (neither S-4/F-4 nor DRS) | 16-20 weeks (drafting + SEC review + vote) |
| DRS filed, no public S-4/F-4 yet | 14-18 weeks (confidential review → public flip → vote) |
| S-4 or F-4 filed publicly, no amendments yet | 10-14 weeks (SEC review cycle + amendments + vote) |
| 1 S-4/A or F-4/A filed | 6-10 weeks (possible effectiveness + vote scheduling) |
| 2+ S-4/A or F-4/A filed | 4-8 weeks (likely near effectiveness) |
| DEFM14A filed (proxy mailed) | 2-4 weeks (vote + closing mechanics) |
| DEFM14A filed + meeting postponed (424B3/DEFA14A) | Use NEW meeting date + 1-2 weeks for closing mechanics |
| Vote completed, closing pending | 1-2 weeks |

These are MINIMUMS. Actual timelines frequently exceed these by 2-6 weeks. Treat S-4 (domestic target) and F-4 (foreign private issuer target) as interchangeable for timeline purposes — both follow the same SEC review cycle.

### Skeptical Timeline Rules — "Realistic Close"

**CRITICAL: Company-provided closing estimates are systematically optimistic.** Apply these adjustments:

1. **"Expected to close in Q[X] [YEAR]"** → Use the LAST DAY of that quarter, not the first. Companies say "Q1" when they mean "maybe by end of March if everything goes perfectly."

2. **"Expected to close in H1/H2 [YEAR]"** → Use the last day of that half. H1 = June 30. H2 = December 31.

3. **"Expected to close in [MONTH]"** → Use the last business day of that month.

4. **If the S-4 or F-4 has blank meeting dates** (brackets like "[ ], 2026"), the company does NOT have SEC effectiveness yet. Add at least 6-8 weeks from today regardless of what the cover letter says.

5. **If the S-4/A or F-4/A was just filed** (within last 7 days), assume at least one more round of SEC comments is possible. Add 4-6 weeks from today as floor.

6. **If outside date is within 60 days and no DEFM14A filed**, the deal is at serious risk of needing an extension or amendment. Flag this prominently.

7. **Event deadlines** (e.g., a company's product launch, sports event, regulatory window): If a hard external event creates urgency, the "Realistic" scenario should assume the deal closes AFTER the event unless the proxy is clearly on track to close before it.

### Extension Provisions

Most BCAs allow the outside date to be extended. Common patterns:
- **Unilateral extensions by target**: Enhanced/target can extend 1-3 times in 10-15 day increments
- **Mutual consent extensions**: Both parties must agree
- **Automatic extensions**: Triggered by specific conditions (regulatory approval pending, etc.)
- **Extension fees**: Some require the SPAC to deposit additional funds into trust

ALWAYS include the fully-extended outside date as a scenario, because extensions are exercised more often than not when deals are running late.

---

## Step 2: Calculate the Yield Table

For each scenario date, compute using the **net accrual** (after trust leakage):

```python
from datetime import date

today = date.today()  # Use actual current date

# Trust leakage parameters (extracted in Step 0g)
# Example: HVII = Cayman domicile, 0% tax, 5% WC cap → retention_rate = 0.95
# Example: DE domicile, 21% tax, 5% WC cap → retention_rate = 0.74
retention_rate = 1 - tax_rate - wc_rate

for scenario_name, exit_date in scenarios.items():
    days = (exit_date - today).days

    # Gross trust accrual
    gross_interest = current_cit * tbill_rate * days / 365

    # Net accrual after tax + working capital withdrawals
    net_accrual = gross_interest * retention_rate

    cit_at_exit = current_cit + net_accrual

    # Annualized IRR
    ann_irr = (cit_at_exit / purchase_price) ** (365 / days) - 1
```

**If working capital cap is a flat dollar amount** (not a percentage of interest):
```python
wc_annual_cap_per_share = wc_annual_cap_dollars / public_shares_outstanding
wc_leakage = min(gross_interest * wc_pct, wc_annual_cap_per_share * days / 365)
net_accrual = gross_interest - (gross_interest * tax_rate) - wc_leakage
```

**Edge cases:**
- If `days <= 0`, skip that scenario (date already passed)
- If `days < 7`, show the yield but flag it as "imminent — execution risk on settlement"
- If `purchase_price > current_cit`, the position is ABOVE trust — flag as "negative carry, no arb yield; return is deal-dependent"
- If retention_rate could not be extracted and defaults were used, flag it in the output

---

## Step 3: Produce the Output

### Required Output Format

Present results in this exact structure:

```
═══════════════════════════════════════════════════════════════════════
[TICKER] YIELD ANALYSIS
═══════════════════════════════════════════════════════════════════════

INPUTS:
  Today:                 [DATE]
  Cash in Trust (CIT):   $[X.XXXXXX] per share    (source: spac-details)
  Purchase Price (mkt):  $[X.XX]                   (source: Bloomberg)
  Discount to Trust:     $[X.XXXX] ([X.XX]%)
  3M T-bill Rate:        [X.XXXX]%                 (source: Bloomberg USGG3M)
  Stage:                 [predeal/indeal]
  Target:                [target name or "N/A"]
  IPO Date:              [DATE]
  Max Deadline:          [DATE]
  Min Cash Condition:    [$ amount or "NONE"]

TRUST LEAKAGE ASSUMPTIONS:
  Domicile:              [KY/DE/etc.]
  Tax Rate (on interest):[XX]%    (source: [10-K tax note / default])
  WC Withdrawal Rate:    [XX]%    (source: [S-1 Note 1 / articles / default])
  WC Annual Cap:         [$XX or "uncapped" or "N/A"]
  Retention Rate:        [XX]%    (= 1 - tax_rate - wc_rate)
  Note:                  [any qualifiers, e.g., "Cayman entity, 0% entity tax;
                          WC cap is 5% of interest per S-1 Note 1"]

SEC FILING PROGRESS:
  Registrant:            [SPAC CIK or PubCo CIK — name the entity]
  DRS Filed:             [DATE or "Not filed"]
  S-4 / F-4 Filed:       [DATE + form type, or "Not yet"]
  S-4/A or F-4/A Count:  [N]
  Latest Amendment:      [DATE + form type, or "N/A"]
  DEFM14A Filed:         [DATE or "Not yet"]
  Post-DEFM14A Supps:    [DEFA14A on DATE, 424B3 on DATE, or "None"]
  Meeting Date:          [DATE or "TBD (blank in filing)"]
  BCA 1st Outside Date:  [DATE]
  BCA Final Outside Date:[DATE] (after [N] extensions)
  Extension Deposits:    [$X.XX/share/period or "None identified"]
  PIPE:                  [committed size + structure, or "None" / "Permissive framework only"]
  [Any event deadlines]:  [DATE — description]

═══════════════════════════════════════════════════════════════════════
SCENARIO                          DATE       DAYS  CIT@EXIT  ANN IRR
───────────────────────────────────────────────────────────────────────
  [Optimistic Close (filing)]   MM/DD/YY       XX  $XX.XXXX   X.XX%
  [Company Estimated Close]     MM/DD/YY       XX  $XX.XXXX   X.XX%  ← co est
  [Realistic Close (skeptical)] MM/DD/YY       XX  $XX.XXXX   X.XX%  ← realistic
  [First Outside Date]          MM/DD/YY       XX  $XX.XXXX   X.XX%
  [Final Outside Date]          MM/DD/YY       XX  $XX.XXXX   X.XX%
  [User-Provided Date(s)]       MM/DD/YY       XX  $XX.XXXX   X.XX%
  [Max Liquidation]             MM/DD/YY      XXX  $XX.XXXX   X.XX%  ← yield floor
═══════════════════════════════════════════════════════════════════════

SCENARIO RATIONALE:
  [Scenario 1]:  [1-2 sentence explanation of why this date was chosen]
  [Scenario 2]:  [1-2 sentence explanation]
  ...
```

**IMPORTANT — Always include the DATE column and SCENARIO RATIONALE section.** The date makes each row immediately actionable (the reader can map it to a calendar event or deadline). The rationale section explains the "why" behind each scenario so the reader can calibrate their own view — yield numbers without context are useless.

### Supplementary Data (include when available)

**Internal Cross-Check:**
```
CROSS-CHECK: spac-details est_yield = [X.XX]% (est_date [DATE])
  vs. our calc at same date = [X.XX]%  [MATCH/DELTA: X.XXbps]
```

### Flags and Warnings

Append these flags when conditions are met:

- **⚠ ABOVE TRUST**: Purchase price exceeds CIT. No redemption arb exists. Yield is negative unless deal closes above current price.
- **⚠ PREDEAL**: No announced target. Yield-to-max is the only meaningful scenario. Close-date scenarios are speculative.
- **⚠ PROXY AT RISK**: Outside date is within 60 days and DEFM14A has not been filed. Extension or BCA amendment likely needed.
- **⚠ MEETING DATE BLANK**: S-4/A or F-4/A has been filed but meeting date is still in brackets. SEC has not declared effective yet.
- **⚠ EVENT DEADLINE COMPRESSION**: A hard external event (games, regulatory window, etc.) occurs before the Final Outside Date. Proxy timeline relative to event is the dominant risk.
- **⚠ THIN DISCOUNT**: Discount to trust is under 10bps. Transaction costs may consume the spread.
- **⚠ MEETING DATE SUPERSEDED**: A DEFA14A, 424B3, or 8-K filed after the DEFM14A has changed the meeting date from the original proxy. Always use the most recent date.
- **⚠ EXTENSION DEPOSITS INCREASE CIT**: Sponsor extension deposits are adding to trust. CIT@EXIT for extended scenarios includes these deposits. Show the breakdown (base CIT + T-bill accrual + extension deposits).
- **⚠ NO MCC**: Article VII contains no minimum cash condition. Deal closes at any redemption level. Favorable for arb — no deal-break risk from high redemptions.
- **⚠ MCC AT RISK**: Minimum cash condition of $[X]M exists. At current trust of $[X]M, max redemptions of [X]% would breach MCC unless PIPE/backstop covers the gap. Flag whether PIPE satisfies MCC regardless of redemptions.
- **⚠ TRUST LEAKAGE — DEFAULT ASSUMPTIONS USED**: Could not extract specific tax rate or WC withdrawal terms from filings. Using default retention rate of [X]% based on [domicile] domicile. Actual leakage may differ — verify against next 10-Q trust reconciliation.
- **⚠ HIGH TRUST LEAKAGE**: Retention rate is below 70% (domestic SPAC with high tax + WC drain). Yield is materially lower than gross accrual suggests. For the max liquidation scenario, cumulative leakage reduces CIT@EXIT by ~$[X.XX]/share vs. gross.

---

## Step 4: Pre-Deal vs. In-Deal Differences

### Pre-Deal SPACs (stage = "predeal")

- Only two meaningful scenarios: **Yield-to-Extension** (next extension date) and **Yield-to-Max** (liquidation deadline)
- No outside dates, no filing progress to track
- CIT accrual is the entire return; no deal timeline to estimate
- Label the output section as "PRE-DEAL YIELD (trust accrual only)"

### In-Deal SPACs (stage = "indeal")

- Full scenario table as described above
- Filing progress is the key variable
- Outside dates from BCA are hard constraints

---

## Step 5: Multiple Ticker Batch Mode

If the user provides multiple tickers (e.g., "run yield on APAD, DRDB, BCSS"):

1. Fire all spac-details calls in parallel
2. Batch all tickers into a single get-price call: `get-price(tickers=["APAD", "DRDB", "BCSS"])`
3. The T-bill rate only needs to be fetched once
4. For each ticker, determine if it needs SEC filing analysis (only for in-deal names with meaningful filing activity)
5. Produce a SUMMARY TABLE first (one row per ticker: price, CIT, discount, realistic yield, max yield), then full detail tables below for each

Summary table format:
```
═══════════════════════════════════════════════════════════════
TICKER   PRICE    CIT     DISC   STAGE    REALISTIC   MAX
───────────────────────────────────────────────────────────────
APAD    $10.16  $10.24   0.73%  indeal     7.76%     4.24%
DRDB    $10.XX  $10.XX   X.XX%  indeal     X.XX%     X.XX%
BCSS    $10.XX  $10.XX   X.XX%  predeal      —       X.XX%
═══════════════════════════════════════════════════════════════
```

---

## Reference: Common Gotchas

1. **Trust accrual uses the 3-month T-bill rate**, not the fed funds rate or a money market rate. Trust accounts are invested in T-bills or money market funds backed by T-bills.

2. **CIT from spac-details may be stale by a few days.** For high-precision work, the user can provide a more recent CIT from a 10-Q/10-K trust disclosure. Use the user-provided value if given.

3. **Excise tax on redemptions** (1% federal excise tax on stock buybacks, effective 2023): This can reduce CIT at exit by ~$0.10/share for high-redemption SPACs. Flag but do not deduct unless the user asks for a post-tax yield.

4. **Extension deposits — ACTIVELY EXTRACT AND MODEL**: Many SPACs require the sponsor to deposit additional funds into trust for each extension period (e.g., $0.025-$0.10/share/month, or a lump sum per extension). These deposits INCREASE CIT and materially affect yield for scenarios that extend past the current period.

   **⚠ KEY LESSON (HYAC case study):** Extension deposits are often NOT in the Articles of Association at all. The Articles may grant the board discretion to extend with no mention of deposits. The deposit obligation is frequently structured as a **separate promissory note or contribution agreement** disclosed in an 8-K filed around the IPO anniversary date (Item 1.01 / Item 2.03). If you only search the Articles, you will miss the deposit entirely. Example: HYAC's Articles said "board may extend monthly, up to 12 times" with zero deposit language. A separate 8-K filed July 15, 2025 disclosed a promissory note for $0.025/share/month (capped at $375K) deposited into trust starting July 28, 2025. Searching only the Articles or S-4 termination section would find nothing.

   **Mandatory extraction workflow:**
   - **ALWAYS** run a filtered 8-K search around the IPO anniversary date (±2 months) and read Item 1.01 / 2.03 / 5.03 / 8.01 items. This is the PRIMARY source for extension deposit terms, not the Articles.
   - Also search the S-4/DEFM14A for any cross-references to extension deposits, but do NOT rely on these alone.
   - Look for keywords: "deposit into the Trust Account," "contribution to trust," "per-share deposit," "extension payment," "promissory note," "Contribution," "Extension Amendment."
   - Extract: deposit amount per share per extension period, any aggregate cap, frequency (monthly vs. per-extension), who pays (sponsor, target, third party), and start date.
   
   **Modeling in yield calc:**
   - For scenarios that extend past the current extension period, add the cumulative extension deposits to CIT at exit:
     ```
     cit_at_exit = current_cit + trust_accrual + extension_deposits_per_share × number_of_extensions_in_scenario
     ```
   - If extension deposits are monthly: calculate fractional months between today and the scenario exit date that fall in extension periods.
   - If extension deposits are lump-sum per extension: count how many extension triggers fall within the scenario window.
   - If there is a per-month cap (e.g., $375K/month), compute the effective per-share deposit as: min(stated_per_share, cap / public_shares_outstanding).
   - Display the extension deposit contribution separately in the output (e.g., "CIT@EXIT: $11.67 ($11.53 base + $0.09 accrual + $0.05 ext deposits)").
   - Do NOT wait for the user to mention extension costs — proactively extract them from filings every time.

5. **Settlement timing**: Redemption proceeds typically take 2-5 business days after vote/closing to hit accounts. For very short-dated scenarios (<14 days), add 3-5 days to the holding period.

6. **Trust leakage is real and cumulative — never ignore it.** SPACs withdraw interest from trust for (a) income taxes on trust interest, (b) working capital to fund operating expenses, and (c) occasionally franchise/excise taxes. The CIT from spac-details already bakes in all historical withdrawals, but FUTURE leakage between today and exit must be modeled. For a domestic (DE) SPAC with a 21% tax rate and 5% WC cap, the retention rate is ~74% — meaning for every $1 of gross interest, only $0.74 accrues to trust. Over a 12-month horizon at 4% T-bill rates, that's ~$0.10/share in leakage on a $10 trust. Ignoring it overstates yield by 50-100bps on longer-dated scenarios.

   **⚠ KEY LESSON (HVII case study):** HVII is a Cayman (KY) domiciled SPAC. Cayman entities pay 0% corporate income tax, so the tax leakage component is zero. But the S-1/Note 1 disclosed a 5% annual cap on interest withdrawals for working capital. Retention rate = 95%. For a DE-domiciled SPAC in the same position, retention would be only 74%. The difference: ~6bps on a 3-month scenario but ~40bps on a 12-month scenario. Domicile matters.

   **Quick sanity check**: If the 10-K shows trust growing from $190.0M to $198.4M over 12 months with ~$7.5M in gross interest, but only $8.4M net increase, that implies ~$0 in withdrawals (because $190 + $8.4 = $198.4, and gross interest at ~3.9% on $190M ≈ $7.4M, which means ~$1.0M was withdrawn). Always cross-check the trust roll-forward when available.

7. **Minimum Cash Condition (MCC) and PIPE status belong in the yield output.** Even though they don't directly affect the yield formula, they affect whether the yield is *realizable*. A SPAC with a $100M MCC and no committed PIPE has a binary risk: if redemptions breach the threshold, the deal breaks and you're in a liquidation scenario regardless of the timeline. Always extract MCC from Article VII of the BCA and PIPE status from Section 6.20 (or equivalent). Report both in the INPUTS section. Flag "No MCC" as favorable for the arb, and flag "MCC at risk" if the math is tight.
