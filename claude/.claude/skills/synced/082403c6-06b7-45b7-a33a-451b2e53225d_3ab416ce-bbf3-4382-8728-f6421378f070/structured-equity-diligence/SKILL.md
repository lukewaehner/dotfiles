---
name: structured-equity-diligence
description: >
  Full institutional due diligence on small/micro-cap public companies being evaluated as candidates
  for Meteora-style structured equity financings — convertible notes, SEPAs, equity units with
  warrants, or hybrid draw facilities. Trigger this skill whenever the user asks to "do diligence
  on", "review", "analyze", or "evaluate" a public company ticker for a potential structured
  investment, or asks whether a company is suitable for a SEPA, convertible note, equity line,
  or similar instrument. Also trigger when the user pastes a company name or ticker alongside
  phrases like "what do you think", "is this a good candidate", "run the diligence", or "look
  into this one". Always use this skill for structured equity investment evaluation — do not
  attempt this ad hoc.
---

# Structured Equity Investment — Full Due Diligence

This skill produces a comprehensive institutional due diligence review of a small/micro-cap
public company as a candidate for a Meteora-style structured equity financing. The output covers
business fundamentals, full SEC filing sweep, capitalization table, complete financing history
(including actual deal terms from exhibits), Nasdaq compliance and delisting risk, management
background, red flags, and a structured financing suitability assessment with recommended
instrument options.

---

## The Four Binding Constraints — Check These First

Before going deep, establish these four facts immediately. They govern every structuring decision:

1. **Derivative liability / equity floor**: Does the company have a Nasdaq minimum stockholders'
   equity requirement? ($2.5M for Capital Market.) Any variable-rate instrument (floating
   conversion, resettable warrants) is likely classified as a derivative liability under ASC 815,
   marked to market at signing across the FULL committed facility — not tranche by tranche. This
   mark hits equity on day one. Quantify the likely mark vs. the equity cushion before recommending
   any instrument.

2. **Nasdaq compliance status and Panel Monitor**: Is the company under any deficiency notice,
   cure period, or Mandatory Panel Monitor? A Panel Monitor means ANY new deficiency bypasses the
   standard 180-day cure and goes straight to Hearings Panel. Identify the exact expiry date.

3. **Reverse split history and bid-price cure eligibility**: Has the company done a reverse split
   in the prior 12 months? If yes, under Rule 5810(c)(3)(A)(iv), a new bid-price deficiency
   triggers immediate delisting proceedings with NO cure period. Identify the exact anniversary
   date that restores eligibility.

4. **Daily dollar volume / monetization ceiling**: At 20% daily capture of ADTV (average daily
   trading value in dollars), how many trading days does it take to exit a $1M position? This is
   a hard constraint, not a soft one. Model it explicitly.

---

## Step 1: EDGAR Full Filing Sweep

Go to `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=[TICKER]` and retrieve
ALL filings. Do not rely on summaries — open the actual documents.

### 1a. Annual and Quarterly Reports (10-K, 10-Q)
Pull the most recent 10-K and all 10-Qs from the past 24 months. Extract:
- Revenue, gross profit, operating loss, net loss (quarterly and annual)
- Cash and cash equivalents (each period end)
- Stockholders' equity (each period end — track the trend toward or away from the $2.5M floor)
- Burn rate: cash used in operations per quarter
- Runway calculation: cash ÷ quarterly burn
- Going concern language — exact wording from auditor and management
- Auditor name and any auditor changes
- Authorized vs. issued shares (common and preferred)
- Full warrant table: quantity, exercise price, expiry, anti-dilution provisions
- Full convertible instrument table: principal, conversion price mechanics, maturity
- All equity plan shares: options, RSUs, ESPP
- Revenue breakdown: product vs. royalty vs. services vs. grants
- R&D vs. SG&A breakdown (flag if SG&A >> R&D for a science company)
- Related party transactions section — read carefully
- Legal proceedings section — read every item
- ATM facility details: agent name, amount allocated, amount remaining, baby shelf status

### 1b. Registration Statements (S-1, S-3, 424B filings)
Pull EVERY registration statement and prospectus. For each:
- Filing date, type, amount registered
- Current status: effective, withdrawn, expired
- Lead placement agent / underwriter
- Offering structure: units, shares, pre-funded warrants, common warrants
- **Open the actual prospectus exhibit** — do not rely on summaries
- Extract from the Description of Warrants / Securities section:
  - Exercise price mechanics (fixed vs. variable)
  - Reset provisions: exact reset dates, reset percentages, reset formula
  - **Floor price** — search the full document for "floor" — this is critical
  - Anti-dilution provisions: structural only (splits/dividends) vs. price-based (full ratchet,
    weighted average) — price-based = resets on any new deal at lower price
  - Cashless exercise formula
  - Blocker provisions (4.99% / 9.99%)
  - Fundamental transaction provisions
- For 424B4 filings specifically: extract share explosion math if reset warrants are present
  (Maxim-style exploding unit structures)

### 1c. 8-K Filings — Last 24 Months
Read every 8-K. Flag and summarize any that disclose:
- Nasdaq deficiency notices (any type)
- Reverse stock splits (ratio, effective date — CRITICAL for 12-month lookback)
- Hearing Panel decisions or Panel Monitor impositions
- Officer/director appointments or departures (note whether "disagreements" are cited)
- Material financings, warrant exercises, share issuances
- Litigation filings or settlements
- Asset sales, partnerships, license agreements
- Going concern disclosures

### 1d. Form 4 (Insider Trading)
Pull all Form 4 filings from the past 12 months. For each:
- Who filed (name, title)
- Transaction type: open market buy, open market sale, RSU grant, option exercise
- Shares and price
- Net insider buying vs. selling over the period
- Flag any large open-market sales by insiders — especially around announcements

### 1e. Proxy Statement (DEF 14A)
Pull the most recent proxy. Extract:
- Board composition and independence
- Executive compensation (base salary, bonus, equity grants)
- Related party transaction disclosures
- Any shareholder votes on reverse splits, authorized share increases, or equity plan expansions

---

## Step 2: Broad Internet and News Search

Run web searches on the company name, ticker (current AND historical), and key executives:

### 2a. Company-Level Searches
- `[company name] OR [ticker] reverse split` — find all historical splits with dates and ratios
- `[company name] OR [ticker] Nasdaq deficiency notice`
- `[company name] OR [ticker] lawsuit litigation SEC investigation`
- `[company name] OR [ticker] short seller report`
- `[company name] OR [ticker] placement agent offering`
- `[ticker] split history site:splithistory.com` — verify complete split history
- `[company name] name change history` — flag shell-like multiple identity changes
- `[ticker] SEC EDGAR filings` — cross-check filing completeness

### 2b. Management and Principal Background Checks
For EACH named executive and director (CEO, CFO, Chairman, all board members):
- `[full name] lawsuit litigation fraud SEC`
- `[full name] stock promoter convicted`
- `[full name] FINRA BrokerCheck` — if they have a broker/dealer background
- `[full name] [company name] insider trading`
- `[full name] other companies` — what else have they run? Any failures or scandals?
- Search for connections between entity shareholders (LLC names, trust names) and any known
  bad actors — particularly in reverse merger situations where pre-IPO shareholders are entities
  rather than named individuals
- Check if the company went public via reverse merger with a shell — if yes, research the shell's
  prior owners and any SEC comment letters on the S-1/registration

---

## Step 3: Capitalization Table — Build From Primary Sources

Do NOT rely on data aggregators. Build the cap table from SEC filings directly.

| Instrument | Quantity | Strike / Conversion | Anti-dilution Type | Expiry | Resets on New Deal? |
|---|---|---|---|---|---|
| Common shares outstanding | | N/A | N/A | N/A | N/A |
| Authorized but unissued | | N/A | N/A | N/A | N/A |
| Common warrants | | $X.XX | Structural / Price-based | MM/YY | Yes / No |
| Pre-funded warrants | | $0.001 | Structural | Until exercised | No |
| Convertible notes | | Variable/Fixed | [specify] | MM/YY | [analyze] |
| Stock options (vested) | | $X.XX | N/A | MM/YY | No |
| RSUs (unvested) | | N/A | N/A | MM/YY | No |
| ESPP | | [price formula] | N/A | N/A | No |
| ATM facility | | Market | N/A | Per agreement | No |

**Key question for each instrument:** Does it have price-based anti-dilution (full ratchet or
weighted average)? If yes, a new structured deal at a lower price will reprice it — creating
additional dilution and potentially triggering its own derivative liability cascade.

---

## Step 4: Complete Financing History — Every Deal

Reconstruct the full capital raise timeline. For each transaction:
- Date
- Structure (PIPE, registered direct, best efforts public, ATM, convertible note, SEPA, etc.)
- Gross proceeds
- Lead placement agent / underwriter (flag repeat agents — especially Maxim, HCW, Roth, Aegis,
  JonesTrading — these often signal repeat dilutive issuers)
- Key terms: offering price, warrant coverage, warrant strike, reset provisions, OID, conversion
  mechanics
- **Open the actual exhibit (purchase agreement, warrant agreement, note agreement)** — do not
  rely on the 8-K summary. Search EDGAR for EX-10.1, EX-4.1, EX-4.4 filed with each 8-K
- Flag any instruments with: floating conversion rates, full ratchet anti-dilution, death spiral
  features, most favored nation clauses, or investor blocking rights

**Cumulative dilution analysis:** Track shares outstanding from the earliest available filing to
today. Compute total dilution and identify which financings drove the largest share count increases.

### 4b. Share Count Evolution Table
Build a quarter-by-quarter table of shares outstanding from the 10-K/10-Q filings:

| Period End | Shares Outstanding | Change from Prior | % Dilution | Key Event |
|---|---|---|---|---|
| Dec 31, 20XX | X,XXX,XXX | — | — | Baseline |
| Mar 31, 20XX | X,XXX,XXX | +X,XXX,XXX | +XX% | [offering/conversion] |

This table is one of the most powerful visual tools for showing serial dilution velocity. If the
company has tripled its share count in 12 months, that tells you more than any single metric.

### 4c. Financing Trajectory Pattern Analysis
After reconstructing the full timeline, analyze the PATTERN across all raises:
- **Are deal sizes declining?** (e.g., IPO was $16M, most recent raise is $1.5M)
- **Are offering prices declining?** (e.g., IPO at $5.00, most recent at $1.285)
- **Are terms getting more dilutive?** (increasing warrant coverage, lower strikes, wider
  discounts, OIDs appearing)
- **Is the placement agent changing?** (companies that rotate agents often do so because
  prior agents will no longer market their deals)
- **Is the frequency of raises accelerating?** (3+ raises in 12 months = desperate)

This trajectory tells you where the company sits in its life cycle and what leverage it has (or
doesn't have) to negotiate terms with Meteora. A company on its 8th raise at declining prices
has essentially no negotiating leverage.

### 4d. Resale Registration Status — Check EVERY Outstanding S-3 / S-1
For EVERY registration statement filed in the past 18 months:
- **Has it been declared effective by the SEC?** Search for an EFFECT notice on EDGAR for that
  CIK. Also check whether the prospectus language says "information in this prospectus is not
  complete and may be changed" (= NOT effective, still in review).
- **If effective:** When did it go effective? Are selling stockholders actively selling?
- **If NOT effective:** How long has it been pending? (>60 days = unusual, may signal SEC
  comment letters or issuer problems.) This creates a **trapped investor problem** — PIPE
  participants who cannot exit because the resale registration hasn't gone effective. Once it
  does go effective, expect concentrated selling pressure.
- **Rule 144 fallback:** If the S-3 is stuck, when does the 6-month Rule 144 holding period
  expire for the most recent PIPE? Is the company current on SEC filings (required for Rule
  144(c) availability for non-affiliates)?

This is a frequently overlooked but critical risk factor for structured note investors. If prior
PIPE investors are sitting on unrealized losses with no registration to sell through, the
effective date of that S-3 will trigger a wave of selling that compounds with any selling from
your own conversion shares.

---

## Step 4e: Contractual Financing Restrictions from Prior Deals

**This step is frequently missed and can be a hard deal-killer.** Every PIPE, registered direct,
and best-efforts offering SPA contains post-closing covenants that restrict the company's ability
to raise additional capital. These restrictions are not disclosed in 10-Ks or press releases —
they live exclusively in the SPA exhibits filed with the 8-K. If Meteora proceeds without reading
them, it may structure and execute a deal that the company is contractually prohibited from doing,
exposing the company to injunctive relief from prior investors.

**For EVERY financing in the past 18 months, open the SPA exhibit (usually EX-10.1) filed with
the closing 8-K and search for the following provisions:**

### VRT (Variable Rate Transaction) Prohibition
The most dangerous covenant for Meteora. Search the SPA for "Variable Rate Transaction,"
"variable rate," or "VRT." Extract:

- **Duration:** Typically 1 year from closing date. Calculate the exact expiry date.
- **Scope of definition:** Does the VRT definition capture: (a) floating conversion / exercise
  prices tied to VWAP or trading price? (b) reset provisions triggered by future events or stock
  price levels? (c) equity lines of credit? (d) ATM facilities (sometimes carved out)?
- **Carve-outs:** Common exclusions include: ATM with the same placement agent as sales agent;
  Exempt Issuances (options/RSUs to employees, shares for acquisitions, etc.). Read these
  carefully — they narrow the restriction but do not eliminate it.
- **Remedy:** Most SPAs grant purchasers the right to seek **injunctive relief** (not just
  damages) against the company for VRT violations. This means a prior investor can obtain a
  court order stopping Meteora's deal from closing. Flag this explicitly.
- **Meteora instruments affected:** SEPAs, ELOCs, any convert with floating price or reset
  warrants, and variable-discount notes are ALL Variable Rate Transactions by definition.
  Fixed-price registered directs or PIPEs are typically not.

**If a VRT prohibition is active and unexpired: Meteora's core instruments are contractually
barred. This is a Hard Pass trigger regardless of all other factors.**

### Lock-Up on Additional Equity Issuances (Short-Term Blackout)
Separate from the VRT prohibition, most SPAs also include a hard short-term blackout on any
equity issuance. Search for "Subsequent Equity Sales" or "Lock-Up" or "Equity Sales":

- **Duration:** Typically 30–90 days from closing (separate from and shorter than the VRT period)
- **Scope:** Covers ALL share issuances and registration statement amendments, not just VRTs
- **Carve-outs:** S-8 for employee plans, amendments that don't increase offering size, ATM
  supplements with the same agent

### Debt Incurrence Restrictions
Search for "Indebtedness," "Additional Debt," "debt," or "negative covenant" provisions:

- Is the company prohibited from incurring additional debt (secured or unsecured) above a
  threshold without prior consent of existing note/debenture holders?
- Does an existing note agreement (e.g., JGB-style senior secured debenture) contain an
  **affirmative covenant requiring restricted cash** pledged to existing holders? If yes, any
  new secured instrument would require a subordination agreement or intercreditor arrangement.
- Does any existing instrument contain a **most favored nation clause** requiring the company
  to offer existing holders the same terms as any new investor? If yes, Meteora's economics
  would automatically be shared with (and potentially undercut by) prior investors.

### Capital Changes Restriction
Search for "Capital Changes," "reverse split," or "reclassification":

- Some SPAs prohibit reverse splits for 3–6 months from closing without purchaser consent,
  except splits required to maintain Nasdaq listing. If active, this limits the company's
  ability to cure a bid-price deficiency — which is relevant to Meteora's delisting risk model.

### Anti-Dilution Triggers from Prior Warrants
Already covered in Step 3, but cross-reference here: does any outstanding warrant series have
**price-based anti-dilution** (full ratchet or weighted average)? If yes, any Meteora deal at
a lower price than the prior offering price **automatically resets those warrants**, inflating
shares outstanding, diluting Meteora's position at conversion, and potentially triggering
additional derivative liability marks. Model the reset explicitly.

### How to Find These Documents Efficiently

1. For each financing in the past 18 months, find the closing 8-K on EDGAR
2. Use `edgar-filing-index` to list all exhibits
3. Look for **EX-10.1** (typically the SPA), **EX-4.1 / EX-4.2** (warrant agreements),
   **EX-4.4** (note agreement if a convertible)
4. In the SPA, navigate directly to **Article IV (Other Agreements)** or **Section 4.11**
   (the most common location for Subsequent Equity Sales / VRT provisions)
5. Search the full text for: "Variable Rate," "variable rate transaction," "Subsequent Equity
   Sales," "Indebtedness," "Most Favored Nation," "Capital Changes"

### Contractual Restriction Summary Table

Build this table for each financing in the past 18 months and include it in the output:

| Financing | Closing Date | VRT Prohibition? | VRT Expiry | Short Blackout? | Blackout Expiry | Debt Restriction? | MFN? | Injunctive Relief? |
|---|---|---|---|---|---|---|---|---|
| [Sept 2025 RD] | Sept 16, 2025 | Yes (§4.11(b)) | Sept 16, 2026 | Yes (30 days) | Oct 16, 2025 | Yes (use of proceeds) | No | Yes |
| [Prior PIPE] | [date] | [Yes/No] | [date/N/A] | [Yes/No] | [date/N/A] | [Yes/No] | [Yes/No] | [Yes/No] |

If the VRT expiry is more than 6 months away, or if a debt incurrence restriction blocks a
convertible note structure, note these as hard constraints in the Section 2 (Four Binding
Constraints) summary at the top of the output — not buried in Step 4.

---

## Step 5: Nasdaq Compliance and Delisting Risk

### 5a. Reverse Split History — The Most Critical Single Data Point
Compile EVERY reverse split: ratio, effective date, pre/post share counts.
- Has the company done a reverse split in the **trailing 12 months**? → No cure period on next
  bid-price deficiency (Rule 5810(c)(3)(A)(iv))
- Has the company done **cumulative 250:1 or more** in the trailing **2 years**? → Same result
- Calculate the exact anniversary date(s) that restore cure eligibility
- Calculate the cumulative ratio across all historical splits

### 5b. Current Compliance Status
For each Nasdaq listing rule, determine current status:

| Rule | Standard | Current Level | Status | Cure Deadline |
|---|---|---|---|---|
| Bid Price (5450(a)(1) / 5550(a)(2)) | ≥ $1.00 | $X.XX | Compliant / Deficient | MM/DD/YY |
| Stockholders' Equity (5550(b)(1)) | ≥ $2.5M | $XM | Compliant / Deficient | MM/DD/YY |
| MVLS (5550(b)(2)) | ≥ $35M | $XM | Compliant / Deficient | MM/DD/YY |
| Min. Bid / Low Price (5810(c)(3)(A)(iii)) | ≥ $0.10 | $X.XX | Compliant / At risk | N/A |
| Proposed $5M MVLS (pending SEC) | ≥ $5M | $XM | Would comply / At risk | TBD |

### 5c. Panel Monitor
If the company has been through a Hearings Panel:
- What were the deficiencies?
- What was the Panel's decision?
- Is a Mandatory Panel Monitor in effect? If yes, exact expiry date.
- During the monitor period: ANY new deficiency → automatic Hearings Panel escalation, no cure

### 5d. Equity Floor Stress Test
Project stockholders' equity forward 2–4 quarters using current burn rate (no Lilly / no
milestone assumptions — conservative):

| Quarter | Projected Equity | Cushion to $2.5M Floor | Risk Level |
|---|---|---|---|
| Current | $XM | $XM | Green/Yellow/Red |
| +1Q | $XM | $XM | Green/Yellow/Red |
| +2Q | $XM | $XM | Green/Yellow/Red |
| +3Q | $XM | $XM | Green/Yellow/Red |

### 5e. Stockholder Approval and Exchange Cap Risk (Nasdaq Rule 5635(d))
Any convertible instrument that could result in issuance of > 19.99% of pre-transaction shares
outstanding requires stockholder approval under Nasdaq Rule 5635(d). Analyze:

- **Does the proposed instrument breach the 19.99% cap on full conversion?** Calculate the
  maximum shares issuable at the floor price and compare to pre-transaction shares outstanding.
- **Is there a stockholder approval deadline in the deal documents?** If yes, what are the
  liquidated damages for failure to obtain approval by that date?
- **Quorum risk:** Can the company actually obtain a quorum? Check the most recent proxy / annual
  meeting results. If the company had to adjourn meetings for lack of quorum (as TNON did — twice
  in 2025), this is a significant structural risk. Low retail engagement = hard to get votes.
- **Who controls the vote?** Calculate insider + institutional ownership as a % of outstanding.
  If the largest shareholders collectively control >50%, approval is likely. If the shareholder
  base is highly fragmented retail, quorum is the real risk.
- **What happens if approval is NOT obtained?** Typical consequences:
  - Liquidated damages (cash payment company may not be able to afford)
  - Conversions capped at 19.99% of pre-transaction shares — remaining principal must be repaid
    in cash (which the company almost certainly doesn't have)
  - Event of Default under the note
  - This creates a structural trap: the company can't convert enough to retire the debt, can't
    pay cash, and defaults — the worst outcome for everyone.

---

## Step 6: Derivative Liability Quantification

For any proposed variable-rate instrument, estimate the day-one derivative liability:

**Key inputs:**
- Stock price (current)
- Implied volatility (pull from the company's own Black-Scholes disclosures in 10-Q notes, or
  use historical vol from options if listed)
- Conversion discount (% below VWAP)
- Floor price
- Term (months)
- Full committed facility size (NOT per-tranche — the liability is recognized at signing)

**Rough framework (adjust for actual vol):**
At ~100% implied vol, a variable-conversion note typically carries a derivative liability of
30–45% of face value on day one. At ~113% vol (VIVS's actual disclosed vol), this rises to
~35–50% of face value.

| Facility Size | Approx. Derivative Liability (35–50% of face) | Day-1 Equity Hit | Post-Signing Equity | Cushion to $2.5M |
|---|---|---|---|---|
| $500K | $175–250K | $(250K) | Current equity - $250K | [calculate] |
| $1.0M | $350–500K | $(500K) | Current equity - $500K | [calculate] |
| $1.5M | $525–750K | $(750K) | Current equity - $750K | [calculate] |
| $2.5M | $875K–$1.25M | $(1.25M) | Current equity - $1.25M | [calculate] |
| $3.5M | $1.2–$1.75M | $(1.75M) | Current equity - $1.75M | [calculate] |

**Rule:** If post-signing equity (after derivative mark) falls below $3.0M, flag as HIGH RISK
relative to the $2.5M floor — one quarter of losses could trigger a deficiency.

**Critical note on tranching:** A committed multi-tranche facility creates the FULL derivative
liability at signing, not at each funding date. Separate standalone note agreements executed
independently at each funding date are the correct structural workaround if liability management
is a priority.

---

## Step 7: Red Flag Inventory

Score each of the following. Mark: ✅ Clean | ⚠️ Watch | 🔴 Serious

**Financial / Operational:**
- [ ] Going concern opinion from auditor
- [ ] Accumulated deficit > 10x market cap
- [ ] Revenue < $1M TTM with no near-term revenue path
- [ ] SG&A materially exceeds R&D for a science/tech company
- [ ] Cash runway < 2 quarters (conservative, no milestone assumptions)
- [ ] Auditor change in past 24 months

**Capital Structure / Financing:**
- [ ] More than 2 reverse splits in company history
- [ ] Reverse split within trailing 12 months (bid-price cure disqualification)
- [ ] Repeat dilutive offerings (3+ capital raises in 24 months)
- [ ] Prior instruments with price-based anti-dilution (ratchet / reset)
- [ ] ATM facility consistently used as primary survival mechanism
- [ ] Baby shelf capacity exhausted or near-exhausted
- [ ] Pending withdrawn S-1 (signals failed financing attempt)

**Compliance / Listing:**
- [ ] Active Nasdaq deficiency (any type)
- [ ] Mandatory Panel Monitor in effect
- [ ] Stockholders' equity < $4M (thin cushion for derivative instruments)
- [ ] Market cap < $5M (proposed new Nasdaq minimum risk)
- [ ] Stock price < $2.00 (limited cushion above $1.00 bid-price minimum)

**Legal / Governance:**
- [ ] Active litigation (as plaintiff or defendant — read the actual complaint if possible)
- [ ] SEC investigation or comment letters unresolved
- [ ] Related party transactions with management-affiliated entities
- [ ] Entity (LLC/trust) shareholders in reverse merger with undisclosed beneficial owners
- [ ] Management or director connections to prior failed/fraudulent companies
- [ ] Multiple name/ticker changes (3+ identities = flag)
- [ ] Convicted or sanctioned individuals in management or shareholder history

**Management:**
- [ ] CEO/CFO turnover in past 24 months
- [ ] Director resignations citing disagreements
- [ ] Insider selling (open market) while company fundraises
- [ ] Executive compensation excessive relative to company size
- [ ] Related party consulting/services agreements with management affiliates

**Structural / Deal-Specific:**
- [ ] **Active VRT prohibition from prior SPA** — Meteora's core instruments (SEPA, ELOC,
  variable convert) are contractually barred; check expiry date (Step 4e)
- [ ] **Short-term equity issuance blackout still running** from prior offering (Step 4e)
- [ ] **Debt incurrence restriction** in existing note agreement blocks new secured or
  unsecured financing without consent of existing holders (Step 4e)
- [ ] **Most Favored Nation clause** in prior instrument — new Meteora deal terms automatically
  offered to existing holder, undermining deal economics (Step 4e)
- [ ] **Injunctive relief remedy** available to prior investors for covenant violations —
  court order could stop deal at closing (Step 4e)
- [ ] Prior warrant price-based anti-dilution: any new deal at lower price auto-resets warrants
- [ ] Death spiral or escalating discount conversion mechanics (see Step 7b below)
- [ ] Stockholder approval required with history of quorum failures
- [ ] Exchange cap (19.99%) limits conversion before stockholder approval
- [ ] Recent acquisitions paid in shares with contingent consideration (cash the company may lack)
- [ ] Goodwill from acquisitions > 15% of total assets (impairment risk under financial stress)
- [ ] Trapped PIPE investors — prior PIPE resale S-3 not yet effective, holders sitting on losses
- [ ] Syndicated convertible deal (multiple note holders = uncoordinated selling pressure)

### 7b. Death Spiral / Escalating Discount Structure Analysis
If the proposed or existing instrument features any of the following, flag it as a potential
death spiral structure and model the feedback loop explicitly:

- **Escalating conversion discounts** (e.g., 25% discount at closing → 40% at maturity →
  60% if unpaid 30 days post-maturity). This creates a perverse incentive: if the company can't
  repay, the discount widens, incentivizing the note holder to short the stock and convert at
  ever-deeper discounts, pushing the stock lower, which widens the effective discount further.
- **OID + deep discount combination** (e.g., 20% OID plus 25%+ conversion discount). The
  investor's cost basis is already 20% below face value; add a 25% conversion discount and
  the effective acquisition price for shares is ~40% below market at inception.
- **No floor price or floor price below delisting threshold.** If the floor is set at $0.10
  (or 20% of $1.00 minimum bid), the instrument effectively permits conversion at prices
  inconsistent with continued Nasdaq listing.
- **Mandatory Default Amount > 100% of principal.** A 150% mandatory default amount combined
  with a company that can't pay cash = forced conversion at distressed prices.

**Model the dilution cascade:**
At the current stock price, calculate shares issued per $1M of principal converted at each
discount tier:

| Scenario | Conversion Price | Shares per $1M | % Dilution to Current Base |
|---|---|---|---|
| 25% discount | $X.XX | X,XXX,XXX | XX% |
| 40% discount | $X.XX | X,XXX,XXX | XX% |
| 60% discount | $X.XX | X,XXX,XXX | XX% |

This table makes the exponential dilution impact viscerally clear and is essential for both
internal investment committee discussion and for framing Meteora's alternative to the company.

### 7c. Acquisition-Related Dilution and Contingent Liabilities
For any acquisition completed in the past 24 months:
- **Shares issued as purchase consideration:** How many shares were issued, and at what implied
  price? Were any shares subject to lock-up or pledge-back arrangements?
- **Contingent consideration / earn-outs:** What are the triggers (revenue milestones, product
  approvals)? Will they be settled in cash or shares? If cash, does the company have the cash?
  If shares, model the additional dilution.
- **Goodwill and intangible assets:** What percentage of total assets is goodwill? For a company
  under financial stress, goodwill impairment is likely and will further erode stockholders'
  equity — accelerating the path toward Nasdaq equity deficiency.
- **Integration costs:** Are there ongoing integration expenses (new hires, earn-out salaries,
  facility consolidation) that increase the burn rate above the pre-acquisition baseline?

---

## Step 8: Structured Financing Suitability Assessment

### Monetization Analysis
- ADTV (30-day average daily trading volume in dollars)
- At 20% daily capture: daily monetization capacity = ADTV × 20%
- Days to exit $500K position: $500K ÷ daily capacity
- Days to exit $1M position: $1M ÷ daily capacity
- Days to exit $2M position: $2M ÷ daily capacity
- Flag any position where exit takes > 90 trading days as HIGH monetization risk

### Instrument Selection Framework

**Option 1 — Equity Unit (Shares + Warrants):**
- Use when: derivative liability is a hard constraint, or equity cushion is thin
- Warrants: structural anti-dilution only = equity-classified, no derivative mark
- Warrants: price-based reset = liability-classified, derivative mark applies
- Economics: locked in via offering discount and warrant upside only
- Registration: S-1 (not shelf if baby shelf constrained)
- Best for: companies where Nasdaq/equity risk is elevated and simpler documentation is preferred

**Option 2 — Convertible Note, Tranched:**
- Use when: better economics needed and company can absorb derivative mark
- OID: 5–10% per tranche
- Conversion: trailing VWAP minus 10–15% discount, with floor at $1.00
- Warrants: 75–100% coverage, same formula as conversion price
- Tranches: at S-1 effectiveness, +60 days, +120 days — each conditional on equity ≥ $3.0M
- CRITICAL: Use separate standalone note agreements per tranche if derivative liability is a
  concern — do not use a master committed facility with multiple draw rights
- Equity gate: hard covenant requiring minimum stockholders' equity at each funding date

**Option 3 — SEPA + Convertible Draw Facility + Commitment Shares:**
- Use when: Meteora wants maximum optionality and a volume catalyst is expected
- Commitment shares: 2–3% of facility size, registered on S-1, paid at signing
- SEPA draws: at Meteora's discretion, priced at VWAP minus 8–10%
- Convertible facility: same terms as Option 2 alongside the SEPA
- WARNING: SEPA is effectively inert at < $100K/day ADTV — model the draw timeline explicitly
- Same derivative liability issue on the convertible component applies

### Sizing Constraints Checklist
Before recommending a deal size, verify all of the following:
- [ ] **No active VRT prohibition from prior SPA** (Step 4e) — if present and unexpired, STOP
- [ ] **No active short-term equity issuance blackout** (Step 4e)
- [ ] **No debt incurrence restriction** blocking the proposed instrument type (Step 4e)
- [ ] **No MFN clause** that would share Meteora's economics with prior investor (Step 4e)
- [ ] Post-signing equity (after derivative mark) ≥ $3.0M
- [ ] Panel Monitor status — if active, derivative instruments are extremely high risk
- [ ] Reverse split 12-month anniversary has passed (bid-price cure available)
- [ ] Baby shelf capacity (if using shelf) or S-1 path confirmed
- [ ] Existing instrument anti-dilution: will any prior warrants/converts reprice on this deal?
- [ ] HCW / tail fee / placement agent litigation: accrued liability included in equity calculation
- [ ] Authorized share headroom sufficient for full conversion + warrant exercise

---

## Step 9: Deal Document Review (When Provided)

When the user provides actual deal documents (SPA, note agreement, warrant agreement, term
sheet), review them systematically. Extract and organize:

### 9a. Key Economic Terms Table
Build a summary table of ALL material terms:
- Structure type (OID note, convertible, SEPA, etc.)
- Principal amount, purchase price, OID percentage
- Maturity date and interest rate
- Conversion price formula (exact mechanics, not summary)
- Floor price (if any) — compare to Nasdaq $1.00 minimum bid
- Discount escalation schedule (if applicable — map out each step with dates)
- Beneficial ownership limitation (4.99% / 9.99%)
- Exchange cap (Nasdaq 5635(d) — 19.99% issuance limitation)
- Stockholder approval deadline and liquidated damages for failure
- Share reservation requirements (200% of conversion shares = common)

### 9b. Event of Default Provisions
List every Event of Default with its cure period. Flag the ones most likely to be triggered
given the company's current financial condition. Common high-risk defaults:
- Payment default (company lacks cash)
- Trading suspension > X days (delisting risk)
- Failure to deliver conversion shares within deadline
- Failure to obtain stockholder approval by deadline
- Breach of Nasdaq minimum listing standards
- Going concern qualification from auditor

### 9c. Negative Covenants and Restrictions
- Variable rate transaction prohibition (duration)
- Additional indebtedness restrictions
- Affiliate transaction restrictions
- Dividend and distribution restrictions
- Use of proceeds limitations
- Public information failure penalties (Rule 144(c) compliance)

### 9d. Comparison to Market
If the user has provided or described a competing / existing term sheet, build a side-by-side
comparison highlighting where Meteora's proposed terms are superior:

| Term | Existing/Competing Structure | Meteora Proposal |
|---|---|---|
| OID | XX% | XX% |
| Conversion Discount | XX% | XX% |
| Facility Size | $XM | $XM |
| Counterparty Structure | Syndicated / Bilateral | Bilateral |
| Company Control | [describe] | [describe] |
| Equity Draw Option | None / Available | Available at XX% |

---

## Step 10: Management Diligence Questions

Generate a prioritized list of questions to ask company management, organized by what matters
most for underwriting the deal. These should be specific, not generic — informed by the actual
financial data and risks identified in the analysis.

### Priority 1: Survival to Maturity
- Current cash balance (not last reported quarter-end)
- Monthly burn rate including any post-acquisition integration costs
- Whether additional financing is contemplated before maturity
- Whether auditor has flagged going concern for the current fiscal year

### Priority 2: Nasdaq Compliance
- Whether any deficiency notices have been received (bid price, market cap, equity)
- Whether a reverse split is being contemplated and if board/shareholder authorization exists
- Current status of any pending compliance plans

### Priority 3: Stockholder Approval (if applicable)
- Confidence in obtaining quorum and approval by deadline
- Identity of largest shareholders and their expected support
- Ability to pay liquidated damages in cash if approval is not obtained

### Priority 4: Revenue Trajectory and Business Fundamentals
- Current run-rate procedure volumes and revenue pipeline
- Breakdown of revenue by product line (if multiple)
- Competitive dynamics and reimbursement landscape
- Status of any pending FDA clearances or clinical milestones

### Priority 5: Capital Structure and Competing Claims
- Full warrant count across all series with current exercise prices
- Current conversion terms on any outstanding preferred stock (have they been reset?)
- Status of any contingent consideration from acquisitions
- Any off-balance-sheet obligations or guarantees

### Priority 6: Registration and Insider Activity
- Status of any pending registration statements (effective? SEC comments?)
- Whether insiders are currently buying in the open market
- Any lock-up agreements expiring in the near term

---

## Step 11: Output Format

Deliver the findings in the following sequence:

1. **Executive Summary** — 3–4 sentences. Overall verdict (suitable / conditionally suitable /
   not suitable), single most important risk, and recommended instrument if applicable.

2. **The Four Binding Constraints** — quantified (equity cushion, Panel Monitor dates, reverse
   split dates, ADTV monetization math).

3. **Business Overview** — what it does, revenue, burn, cash runway, key catalysts (with
   conservative timing assumptions — do not rely on management guidance without scrutiny).

4. **Complete SEC Filing Review** — summarized findings from every filing category.

5. **Capitalization Table** — full table from primary sources.

6. **Financing History** — every deal with actual terms from exhibits. Include the financing
   trajectory pattern analysis (deal sizes, prices, terms declining over time). Include the
   share count evolution table showing dilution velocity.

7. **Contractual Financing Restrictions** — table of all active/recent restrictions from prior
   SPAs: VRT prohibitions (with expiry dates), equity blackouts, debt incurrence covenants,
   MFN clauses, and injunctive relief rights. Flag any that block Meteora's proposed instrument.

8. **Resale Registration Status** — status of every outstanding S-3/S-1, whether effective,
   trapped PIPE investor analysis.

9. **Nasdaq Compliance** — complete split history, compliance table, equity stress test,
   stockholder approval / exchange cap risk assessment.

10. **Red Flag Inventory** — scored with ✅ / ⚠️ / 🔴. Include death spiral analysis and
    acquisition-related risks.

11. **Management Background** — findings from principal searches.

12. **Deal Document Review** — if documents provided, key terms table, Events of Default,
    negative covenants, and comparison to Meteora's proposed terms.

13. **Illustrative Dilution Math** — worked examples at each discount tier showing shares
    issued per $1M converted and percentage dilution to current share base.

14. **Management Questions** — prioritized list of questions for company management call.

15. **Three Financing Options** — presented neutrally from the company's perspective (not
    Meteora's economics). Highlight instrument features, derivative liability implications, and
    registration path for each. Include a comparison table vs. the existing proposed structure
    if one exists.

16. **Overall Risk Rating** — HIGH / MEDIUM / LOW with one-paragraph justification.

---

## Conservative Assumptions — Always Apply These

- **Never rely on management milestone guidance** without independent verification. Assume
  milestones arrive 6–9 months later than guided.
- **Never count contingent payments** (milestones, earn-outs, escrow releases) in the runway
  calculation unless already received.
- **Assume worst-case registration path** — new S-1 (not shelf) unless shelf availability is
  confirmed and baby shelf headroom is explicitly calculated.
- **Daily volume is a hard constraint**, not a soft one. Model the monetization timeline at
  20% ADTV capture. Do not assume volume spikes from catalysts in the base case.
- **Derivative liability is recognized at signing** across the full committed facility — not
  tranche by tranche. Use separate note agreements if tranche-by-tranche liability recognition
  is needed.
- **All prior warrant/convert anti-dilution provisions must be verified from the actual
  exhibit** — do not rely on 8-K summaries or prospectus cover pages.
- **Syndicated deals create uncoordinated selling pressure.** When multiple investors hold
  the same discount-to-VWAP conversion right, each has an incentive to convert and sell as
  fast as possible before other holders do the same. This "mad dash" dynamic depresses the
  stock far more than a bilateral deal with a single counterparty. Always flag syndicated
  structures as a risk factor, and frame Meteora's bilateral alternative when presenting
  options.
- **Stockholder approval is never guaranteed.** Even when the shareholder base appears
  supportive, quorum risk is real for micro-cap companies with fragmented retail ownership.
  Check the company's track record of obtaining quorum at prior annual meetings.
- **Trapped PIPE investors sell aggressively.** When a prior PIPE's resale registration goes
  effective and the stock is below the PIPE offering price, expect concentrated selling pressure
  as trapped investors exit at a loss. Time this event against Meteora's own conversion window.
- **Always read the prior SPA exhibit before structuring.** VRT prohibitions, equity blackouts,
  and debt incurrence covenants are never disclosed in the 10-K or press releases — they exist
  only in the EX-10.1 attached to the closing 8-K. A deal is not structurally viable until these
  covenants have been read from the actual document and confirmed not to block Meteora's
  instrument. Prior purchasers with injunctive relief rights can stop a Meteora closing in court.
