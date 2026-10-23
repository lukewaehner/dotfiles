---
name: warrant-analysis
description: "SEC warrant agreement analysis and full term extraction for public SPAC warrants. Trigger when the user asks to analyze warrants, extract warrant terms, evaluate SPAC warrant structures, or asks about a ticker (e.g., KDKRW, BTWNW). Trigger phrases: 'analyze the warrants for [ticker]', 'warrant terms for [ticker]', 'pull the warrant agreement', 'warrant structure analysis', 'what is the strike/redemption/cashless'. Also trigger for tickers ending in W/WS/WT (but confirm with user if it is a warrant ticker vs common stock — many tickers naturally end in W or V), uploaded warrant PDFs, or SEC exhibits (EX-4.1, EX-4.4). Supersedes manual SEC searches — systematic, complete extraction workflow covering exercise, redemption, adjustments, Crescent Term, make-whole, cashless, change of control for public SPAC warrants."
---

# Public SPAC Warrant Analysis — Full Term Extraction from SEC Filings

## Overview

This skill extracts every material term from a **public SPAC warrant agreement** by first building a complete event timeline via web search, then systematically reading the actual SEC filings anchored to those dates.

**Workflow:**
1. **Step 0 — Web Reconnaissance:** Build full event timeline (IPO, deal announcement, deSPAC closing, financings, corporate actions) via web search
2. **Step 1 — Targeted Filing Search:** Use the timeline to pull exactly the right filings from EDGAR
3. **Step 2 — Read Warrant Agreement:** Extract all terms from EX-4.1
4. **Step 3 — Cross-Reference Description of Securities:** Verify terms against proxy/prospectus
5. **Step 4 — Check Adjustments & Crescent Term:** Use financing dates from Step 0 to find trigger evidence
6. **Step 5 — Compile Output:** Produce .docx term sheet
7. **Step 6 — Quality Checks**

**Scope:** Public warrants only. Private placement, working capital, founder, non-redemption, and PIPE warrants are noted for completeness but NOT analyzed in detail. The output notes where private warrant terms differ from public.

---

## Step 0: Web Search Reconnaissance — Build the Full Event Timeline

**ALWAYS DO THIS FIRST.** Before opening any SEC filings, use **web_search** to construct a dated timeline of every key event. This timeline becomes the roadmap for all filing searches.

### 0a. Entity Identification

**Search queries:**
1. `"[TICKER]" SPAC deSPAC merger`
2. `"[TICKER]" "blank check" OR "special purpose acquisition"`
3. `"[TICKER]" former SPAC ticker OR "formerly known as"`

**Extract:**
- SPAC or post-deSPAC?
- If post-deSPAC: original SPAC name, original SPAC ticker
- CIK for both entities if available (current vs. original SPAC — may differ)

**Why:** The Warrant Agreement is filed under the SPAC's original CIK/filings, not the post-deSPAC entity.

### 0b. IPO Date and Terms

**Search queries:**
1. `"[SPAC TICKER]" OR "[SPAC NAME]" IPO date "priced" OR "closed"`
2. `"[SPAC TICKER]" IPO "$10.00" units`
3. `"[SPAC NAME]" "initial public offering" [YEAR range]`

**Extract:**
- **IPO date** → Warrant Agreement (EX-4.1) is in the 8-K filed within days of this date
- **IPO size** (gross proceeds) → Needed for Crescent Term 60% threshold
- **Unit structure** (e.g., 1 share + 1/2 warrant)
- **Underwriter** → Helps predict warrant agreement style (EarlyBird, Cantor, etc.)
- **Overallotment** → Additional warrants issued ~45 days post-IPO

### 0c. Deal Announcement

**Search queries:**
1. `"[SPAC TICKER]" "definitive agreement" OR "business combination agreement" announced`
2. `"[SPAC TICKER]" merger announcement target`

**Extract:**
- **Announcement date** → 8-K (Item 1.01) filed on this date; S-4 follows within weeks
- **Target company** and deal structure
- **Initial valuation / implied share price**

### 0d. deSPAC Closing Date

**Search queries:**
1. `"[TICKER]" OR "[SPAC TICKER]" "business combination" "closed" OR "completed"`
2. `"[TICKER]" deSPAC closing [YEAR]`
3. `"[SPAC NAME]" merger "effective date" OR "closing date"`

**Extract:**
- **Exact closing date** → Closing 8-K (Items 2.01, 3.03) filed within 4 business days
- **Redemption numbers** (shares redeemed, % redeemed, trust remaining)
- **Ticker change date** if applicable

### 0e. Financings at deSPAC (Crescent Term Trigger Search)

**Search queries (cast a wide net):**
1. `"[TICKER]" OR "[SPAC TICKER]" PIPE financing deSPAC`
2. `"[TICKER]" OR "[SPAC TICKER]" "forward purchase agreement" OR FPA`
3. `"[TICKER]" OR "[SPAC TICKER]" backstop OR "non-redemption agreement"`
4. `"[TICKER]" OR "[SPAC TICKER]" convertible note financing [YEAR]`
5. `"[TICKER]" OR "[SPAC TICKER]" "equity line" OR ELOC OR SEPA`
6. `"[TICKER]" warrant adjustment OR "adjusted exercise price"`

**Extract for each financing:**
- Date, type, size ($), price per share, counterparty
- Whether press releases mention "warrant adjustment" (direct Crescent evidence)

**Red flags — Crescent Term almost certainly triggered:**
- Redemptions >80% → trust is small → any financing likely exceeds 60% of equity proceeds
- PIPE/FPA priced at or below $10 with SPAC trading below $10
- Any mention of "adjusted exercise price" or "warrant amendment" in press releases

### 0f. Post-Closing Corporate Actions

**Search queries:**
1. `"[TICKER]" reverse stock split OR stock split`
2. `"[TICKER]" warrant redemption notice OR "called for redemption"`
3. `"[TICKER]" warrant amendment`

**Extract:** Dates and details of any splits, redemption calls, or amendments.

### 0g. Compile Timeline

```
EVENT TIMELINE & FILING ROADMAP — [TICKER]
=============================================
Current Ticker: [TICKER]     |  Current Entity: [NAME]
SPAC Ticker: [TICKER]        |  SPAC Name: [NAME]

[DATE] — SPAC IPO ($XXM, X units at $10, unit = 1 share + 1/X warrant)
         → TARGET FILING: 8-K w/ EX-4.1 (Warrant Agreement) + 424B4/S-1
         Underwriter: [name]

[DATE] — Overallotment exercised (if applicable)
         → TARGET FILING: 8-K

[DATE] — Deal announced with [TARGET]
         → TARGET FILING: 8-K (Item 1.01)

[DATE] — Proxy/S-4 filed
         → TARGET FILING: DEFM14A or S-4/A ("Description of Securities")

[DATE] — deSPAC closed | Redemptions: XX% ($XXM of $XXM trust)
         → TARGET FILING: 8-K (Items 2.01, 3.03, 5.01)

[DATE] — PIPE: $XXM at $XX.XX/share
         → TARGET FILING: 8-K around this date

[DATE] — FPA/Backstop/Other: $XXM at $XX.XX/share
         → TARGET FILING: 8-K around this date

[DATE] — Warrant adjustment notice (if found)
         → TARGET FILING: 8-K w/ EX-99.1

[DATE] — [Any splits, redemption calls, amendments]
         → TARGET FILING: 8-K

CRESCENT TERM PRELIMINARY ASSESSMENT:
  Financings: [list]
  Aggregate proceeds: $XXM
  Trust after redemptions: $XXM
  Financing as % of equity: ~XX%
  Likely triggered: [Yes/No/Unknown]
```

**Share with user before proceeding.** Ask: "Does this look right?"

---

## Step 1: Targeted Filing Search (Guided by Timeline)

### 1a. Resolve Entity in EDGAR

- If post-deSPAC, search EDGAR under BOTH current and original SPAC CIK/ticker
- Use `edgar-filings` with the SPAC ticker to find the original filings

### 1b. Pull Filings by Timeline Date

Every search references a specific date from Step 0:

```
□ Warrant Agreement (EX-4.1)
  → 8-Ks by [SPAC TICKER] within 1 week of [IPO DATE]

□ IPO Prospectus (424B4 or S-1)
  → Filed by [SPAC TICKER] around [IPO DATE]

□ Proxy / Registration ("Description of Securities")
  → DEFM14A or S-4/A around [PROXY DATE]

□ deSPAC Closing 8-K
  → 8-Ks within 1 week of [CLOSING DATE]

□ Financing 8-Ks
  → 8-Ks around [each FINANCING DATE]

□ Warrant Adjustment Notices
  → 8-Ks with EX-99.1 within 30 days of [CLOSING DATE]

□ Post-Closing Corporate Action 8-Ks
  → 8-Ks around [each ACTION DATE]
```

---

## Step 2: Read the Warrant Agreement (EX-4.1)

Read in full using `edgar-filing-text`. Paginate with `offset` and `max_chars` (plan 3-8 reads for 50K-150K chars).

### Extraction Guide

| Section | Extract |
|---------|---------|
| §1 | Warrant Agent |
| §2 | Detachability, fractional rules |
| §3 | **Strike price**, exercise period, cash/cashless mechanics, FMV formula, ownership blocker |
| §4 | **Anti-dilution** (splits, dividends, rights), **Crescent Term (§4.3.2)**, merger treatment, carveouts |
| §6 | **Redemption trigger** (price, trading day window), redemption price, notice period, forced cashless, make-whole table (if present) |
| §7 | Registration obligation, cashless fallback |
| §8-9 | Amendment provisions, governing law |

**Critical extractions:**
- §3.3.1 — All exercise mechanics for public warrants
- §4.3.2 — **Extract the EXACT gate threshold** (do NOT assume $9.20 — it is deal-specific). Record all three conditions and the formula.
- §6 — Full redemption mechanics. If dual redemption ($18 + $10), extract both paths and the make-whole table.

---

## Step 3: Cross-Reference Description of Securities

Find in the proxy/prospectus (DEFM14A or S-4/A) using the **proxy date from Step 0**.

Search with `search_terms`: "Public Warrants", "Description of Warrants"

Verify: strike, redemption trigger, exercise period, warrant count, cashless formula. Flag any discrepancies with the agreement.

---

## Step 4: Check Adjustments & Crescent Term Triggers

### 4a. Post-Closing Amendments

Search 8-Ks after **closing date (from Step 0)** for Item 3.03, Item 5.03, "Warrant Adjustment Notice", "Amendment to Warrant Agreement".

### 4b. Crescent Term Evidence (Using Step 0 Financing Data)

1. **deSPAC closing 8-K:** Search for "Newly Issued Price", "Market Value", "4.3.2", "dilutive issuance", "adjusted exercise price"
2. **8-Ks within 30 days of closing:** Search for "warrant adjustment", "Exhibit 99"
3. **For each financing from Step 0:** Pull the 8-K, extract price/share and proceeds, compare to gate threshold

### 4c. Crescent Term Calculation

```
Gate Threshold (from §4.3.2): $____
Market Value (MV) = 20-day VWAP starting day prior to closing: $____
Newly Issued Price (NIP) = effective price of dilutive issuance: $____
Higher of MV and NIP: $____

Conditions:
  (x) NIP < Gate?  [Y/N]
  (y) Proceeds > X% of equity proceeds?  [Y/N]
  (z) MV < Gate?  [Y/N]
  All met? → [TRIGGERED / NOT TRIGGERED]

Adjusted Strike = 115% × max(MV, NIP) = $____
Adjusted Redemption Trigger = 180% × max(MV, NIP) = $____
```

Cross-check against any filed adjustment notice. Use filing values if discrepancy.

### 4d. Stock Splits / Reverse Splits

If Step 0 found any splits:
- New strike = Old strike × (old shares / new shares)
- New shares per warrant = old × (new shares / old shares)

---

## Step 5: Compile Output (.docx)

Read the docx skill at `/mnt/skills/public/docx/SKILL.md` before creating the document.

### Output Template

```
PUBLIC WARRANT TERM SHEET — [COMPANY NAME] ([TICKER])
================================================================

EVENT TIMELINE
[Reproduce the timeline from Step 0g]

CRESCENT TERM ANALYSIS
  Gate: $XX.XX (§4.3.2)
  MV: $XX.XX | NIP: $XX.XX
  Triggered: [Yes/No]
  Adjusted Strike: $XX.XX | Adjusted Redemption Trigger: $XX.XX

FILING SOURCES
  [Each filing with accession number and date]

WARRANT OVERVIEW
  Warrant Ticker:
  Warrant Agent:
  Agreement Date:
  Public Warrants Outstanding:
  (Other classes noted but not analyzed: Private [count], etc.)

EXERCISE TERMS
  Strike / Exercise Price: [original + adjusted if applicable]
  Exercise Type: Cash (cashless only on redemption or if no registration)
  Cashless Formula: [exact formula, FMV definition]
  Exercise Period: [start → expiration]
  Expiration: [date or duration]
  Ownership Blocker: [if applicable]

REDEMPTION TERMS
  Trigger (Reference Value): [≥$18.00 or adjusted]
    Trading Day Window: [e.g., 20 of 30]
    Reference Value Definition: [section ref]
  Redemption Price: [$0.01]
  Notice Period: [30 days]
  Conditions: [registration, whole not partial]
  Forced Cashless on Redemption: [yes/no, formula]
  $10 Cashless Redemption Path: [if dual-redemption — trigger, price, make-whole table]

ADJUSTMENT PROVISIONS
  Splits/Subdivisions: [section ref]
  Reverse Splits: [section ref]
  Rights Offerings: [section ref]
  Extraordinary Dividends: [threshold, formula, section ref]
  Crescent Term (§4.3.2):
    Gate: $XX.XX
    Conditions: (x) NIP < Gate, (y) proceeds > X%, (z) MV < Gate
    Formula: Strike = 115% × max(MV, NIP); Redemption = 180% × max(MV, NIP)
  Carveouts: [Class B conversion, BC issuances, etc.]

MAKE-WHOLE TABLE (if applicable)
  [Reproduce table or "Not applicable — single redemption structure"]

CHANGE OF CONTROL
  Treatment: [section ref]
  Special provisions:

KEY PRICE LEVELS
  | Level | Price | Source |
  | Adjusted Strike | $X.XX | §3 + §4.3.2 |
  | Original Strike | $X.XX | §3 |
  | Crescent Gate | $X.XX | §4.3.2 |
  | Adjusted Redemption | $X.XX | §6 + §4.3.2 |
  | Original Redemption | $X.XX | §6 |

OTHER PROVISIONS
  No Net Cash Settlement: [yes/no]
  Registration Requirement: [timeline, cashless fallback]
  Amendment Provisions: [holder consent requirements]
  Governing Law: [state]
  Exclusive Forum: [court]

PRIVATE WARRANT DIFFERENCES (summary only)
  [Brief list of how private/sponsor warrants differ: cashless at all times,
   not redeemable under $18 path, transfer-restricted, etc.]

GAPS / FOLLOW-UP
  [Any unknowns or ambiguities]
```

---

## Step 6: Quality Checks

1. **Timeline consistency** — Web dates match EDGAR filing dates?
2. **Strike consistency** — Agreement vs. Description of Securities
3. **Redemption trigger consistency** — Same cross-check
4. **Crescent Term** — Web evidence vs. filing evidence match?
5. **Section references** — All key provisions cited?
6. **Post-closing adjustments** — All splits/amendments reflected?

---

## MCP Tool Usage

Use `tool_search` to load EDGAR tools before starting. Key tools:
- **edgar-filings**: List filings by ticker/CIK, filter by type
- **edgar-filing-index**: List exhibits in a filing
- **edgar-filing-text**: Read filing text (use `offset`/`max_chars` to paginate, `search_terms` to jump)
- **edgar-company-facts**: XBRL facts (share counts)

**Tips:**
- Use `ticker` not `cik` when resolving
- Plan 15,000 chars per read for large docs
- If tool fails, reload via `tool_search` (tunnel URLs rotate)
- Prefer raw text with offset over `summary=true`

---

## Common Patterns

### Warrant Agreement Styles
- **Ares/Reinvent (Type A):** $11.50 strike, $18 single redemption, Crescent Term, no make-whole
- **EarlyBird/Cantor (Type B):** $11.50 strike, dual redemption ($18 + $10 w/ make-whole table)
- **Churchill/CF:** Similar to Type B, Black-Scholes for private warrants

See `/mnt/skills/user/warrant-analysis/references/common_structures.md` for detailed reference including make-whole tables and formula definitions.

### Gotchas
1. **SPAC may have changed CIK at deSPAC** — Step 0 handles this; verify in EDGAR
2. **Warrant Agreement is from SPAC IPO** — look near IPO date, not in S-4
3. **Amendments may be under new CIK** — check both
4. **Crescent Term is retroactive** — applies even if 8-K filed weeks after closing
5. **Make-whole table** only applies to $10 cashless path, not $18 redemption
6. **High redemptions + any financing = Crescent almost always triggered**
7. **Multiple financings compound** — PIPE + FPA + backstop all count toward 60% threshold
8. **Overallotment** — check for 8-K ~45 days post-IPO for additional warrants
