---
name: dar-comparison
description: "Compare two Dollars at Risk (DAR) reports and produce a professional .docx analysis. Trigger when the user uploads two DAR reports, asks to compare DAR across dates, requests a DAR change analysis, or mentions 'DAR comparison', 'what changed in DAR', 'compare the DAR reports', 'DAR delta', or 'DAR period-over-period'. Also trigger when the user pastes or uploads documents containing DAR tables with security types (Common, Warrants, Rights), bucket breakdowns, avg vs trust, avg warrant cost, avg rights cost, and concentration tables. Works for any fund sub-book (MSTO, full book, etc.). Supersedes ad-hoc DAR analysis — systematic extraction, comparison, and docx report generation."
---

# DAR Comparison Report — Period-over-Period Analysis

## Overview

This skill compares two Dollars at Risk (DAR) reports and produces a professional .docx comparison report with tables and narrative analysis. The reports come from Meteora Capital's SPAC event-driven portfolio and contain standardized sections.

**Output:** A formatted Word document (.docx) with comparison tables, mover analysis, and narrative commentary.

---

## Critical Domain Knowledge

These rules encode how DAR works in SPAC portfolios. Violating them produces incorrect analysis.

### 1. Wider discounts DECREASE DAR (but represent negative P&L)

- "Avg vs Trust" measures how far below trust value the common shares were purchased
- A more negative avg vs trust (e.g., -$0.04 → -$0.10) means shares were bought at a wider discount
- **Wider discounts REDUCE dollars at risk** because there is less capital exposed per share
- **However, wider discounts represent NEGATIVE P&L** — prices moved against the position
- Always frame this correctly: "adverse price movement drove negative P&L but mechanically reduced DAR"
- NEVER say wider discounts "increase DAR" or are "unfavorable for DAR"

### 2. Lower warrant/rights costs DECREASE DAR (but represent negative P&L)

- If avg warrant cost falls (e.g., $0.32 → $0.30), that means warrant prices declined — a loss
- Lower prices mean less capital at risk per unit, so DAR decreases
- Same logic applies to rights: lower avg rights cost = loss on position but lower DAR

### 3. Top-10 lists are NOT exhaustive position lists

- DAR reports show the top 10 names by DAR in each category
- **If a name drops out of the top 10, do NOT assume the position was exited**
- It may have shrunk below the #10 cutoff but still exist in the book
- For names that left the top 10: report "fell out of the top 10" and note prior DAR as "(was $XK)"
- For names that entered the top 10: report "entered the top 10" and note current DAR
- **Do NOT show $0 for the unknown period** — instead show `<$X` where X is the #10 entry's DAR on that date (the upper bound of what the position could be)
- **Do NOT compute dollar changes for names only in one top-10 list** — you don't have both data points
- Only compute exact $ and % changes for names appearing in BOTH periods' top 10

### 4. Confirm report scope before comparing

- Reports may be for different sub-books (MSTO, full book, etc.) or different funds
- Always check the report header/title for the fund or sub-book label
- An MSTO report and a full-book report are NOT comparable apples-to-apples
- Ask the user to clarify if scope is ambiguous

---

## Step 1: Parse Both DAR Reports

Extract the following data from each report. The reports are typically pasted as text or uploaded as files.

### Data to Extract

For each report, extract:

**Header info:**
- Date
- Fund / sub-book name (e.g., MSTO, Full Book)

**DAR by Security Type (top-level):**
- Pre-Deal: Common, Warrants, Rights, Total
- In-Deal: Common, Warrants, Rights, Total
- TOTAL: Common, Warrants, Rights, Total

**Pre-Deal DAR by Bucket:** Buckets 1-5 and "-", by Common/Warrants/Rights

**In-Deal DAR by Bucket:** Buckets 1-5 and "-", by Common/Warrants/Rights

**Average Cost Tables (ALL row only is sufficient for comparison):**
- Pre-Deal Avg vs Trust: Shares, Avg
- In-Deal Avg vs Trust: Shares, Avg
- Pre-Deal Avg Warrant Cost: Shares, Avg
- In-Deal Avg Warrant Cost: Shares, Avg
- Pre-Deal Avg Rights Cost: Shares, Avg
- In-Deal Avg Rights Cost: Shares, Avg

**Concentration / Top 10 Tables (all 6 categories):**
- Pre-Deal Common: Rank, Ticker, DAR, %
- Pre-Deal Warrants: Rank, Ticker, DAR, %
- Pre-Deal Rights: Rank, Ticker, DAR, %
- In-Deal Common: Rank, Ticker, DAR, %
- In-Deal Warrants: Rank, Ticker, DAR, %
- In-Deal Rights: Rank, Ticker, DAR, %

Also extract the concentration summary rows (Top 1, Top 3, Top 5, Top 10, Top 20) for each category.

---

## Step 2: Build Comparison Tables

### 2a. DAR Summary Table

Compare total DAR, by security type, by pre-deal/in-deal, with $ change and % change columns.

Headers: `Category | [Date 1] | [Date 2] | Change ($) | Change (%)`

Rows:
- Total DAR
- Common (indented)
- Warrants (indented)
- Rights (indented)
- Pre-Deal Total
- PD Common, PD Warrants, PD Rights (indented)
- In-Deal Total
- ID Common, ID Warrants, ID Rights (indented)

### 2b. Average Costs & Share Counts Table

Headers: `Metric | [Date 1] | [Date 2] | Change`

Rows for each of the 6 avg cost categories: show both the avg cost and the share count.

### 2c. Top-10 Mover Tables (one per category, 6 total)

For each of the 6 concentration categories (PD Common, PD Warrants, PD Rights, ID Common, ID Warrants, ID Rights):

Headers: `Ticker | [Date 1] DAR | [Date 2] DAR | Change ($) | Change (%)`

**Row construction logic (CRITICAL):**

```
For each category:
  d1_map = {ticker: dar} from Date 1 top 10
  d2_map = {ticker: dar} from Date 2 top 10
  floor_d1 = DAR of the #10 entry on Date 1
  floor_d2 = DAR of the #10 entry on Date 2

  // Names in BOTH top 10s — exact delta known
  For ticker in d1_map AND d2_map:
    Show: ticker, d1_dar, d2_dar, (d2_dar - d1_dar), pct_change

  // Names only in Date 1 top 10 — fell out
  For ticker in d1_map but NOT d2_map:
    Show: ticker, d1_dar, "<$floor_d2", "", "Left Top 10"

  // Names only in Date 2 top 10 — entered
  For ticker in d2_map but NOT d1_map:
    Show: ticker, "<$floor_d1", d2_dar, "", "New Top 10"
```

**Never show $0 for the unknown period. Never compute a delta for these rows.**

---

## Step 3: Write Narrative Analysis

The narrative should cover these sections. Use the numbered structure below.

### Section 1: Executive Summary
- Total DAR change ($ and %)
- Which security types drove the change
- Two-force framework: (1) price movement drove negative/positive P&L while mechanically reducing/increasing DAR, (2) position changes (trimming, accumulation, rotation) independently changed DAR
- Highlight the most dramatic category moves

### Section 2: Overall DAR by Security Type
- Accompany with the DAR Summary comparison table
- Note shifts in composition (% of total by security type)
- Note pre-deal vs in-deal split changes

### Section 3: Price vs. Position Size Attribution
- Accompany with the Average Costs & Share Counts table
- For each security type, analyze:
  - Did share counts change? (position sizing)
  - Did average costs change? (price movement)
  - Which factor drove the DAR change?
- Remember: wider discounts and lower costs = negative P&L but lower DAR
- Provide a summary paragraph at the end attributing the overall DAR change to price vs position

### Section 4: Top DAR Movers by Name
- One sub-section per category (6 total), each with its mover table
- For names in both top 10s: cite exact $ and % changes
- For names that fell out: say "(was $XK)" — do NOT cite a dollar change
- For names that entered: say "entered the top 10 at $XK"
- Note any deal-related context if apparent (e.g., a name moving from pre-deal to in-deal suggests a deal announcement)

### Section 5: Concentration & Composition
- Compare top 1, 3, 5, 10, 20 concentration percentages across periods
- Note whether the book became more or less concentrated and in which categories
- Identify drivers of concentration changes

### Section 6: Key Takeaways
- 3-4 bullet-style paragraphs summarizing the most important findings
- Lead with the headline DAR change
- Separate position-driven vs price-driven effects
- Note risk profile shifts (composition, concentration)

---

## Step 4: Generate the .docx Report

Read the docx skill (`/mnt/skills/public/docx/SKILL.md`) and follow its instructions for document creation using `docx-js`.

### Document Formatting

- **Font:** Arial throughout
- **Page size:** US Letter (12240 x 15840 DXA), 1080 DXA margins
- **Header:** Right-aligned, "DAR Comparison | [Fund] | [Date1] vs [Date2]", italic, gray
- **Footer:** Centered page numbers
- **Heading 1:** 36pt bold, color #1F3864
- **Heading 2:** 26pt bold, color #1F3864
- **Body text:** 20 (10pt)
- **Table headers:** White text on #1F3864 background, bold
- **Table body:** Alternating rows with #F2F2F2 shading, 17 (8.5pt)
- **Negative values:** Show in parentheses `($X)` and color #CC0000 (red)
- **Column alignment:** First column left-aligned (bold), all other columns right-aligned
- **Cell margins:** top/bottom 60, left/right 100
- **Borders:** Light gray (#CCCCCC), single, size 1
- **Always use WidthType.DXA** (never PERCENTAGE — breaks in Google Docs)
- **Always use ShadingType.CLEAR** (never SOLID)

### Number Formatting

- Dollar amounts: `$1,234,567` (no decimals), negatives as `($1,234,567)`
- Percentages: `+12.3%` or `-12.3%` (always show sign)
- Share counts: `1,234,567` (comma-separated)
- Avg costs: `$0.32` (2 decimal places)

### Page Breaks

Insert page breaks before Section 4 (Top Movers) and before the second half of mover tables if needed to avoid awkward breaks.

---

## Checklist Before Finalizing

- [ ] Confirmed both reports are from the same fund/sub-book (or noted the difference)
- [ ] Dates are correctly labeled in all table headers and narrative
- [ ] No "$0" shown for names that simply fell out of or entered the top 10
- [ ] Dollar changes only computed for names present in BOTH top-10 lists
- [ ] Wider discounts described as negative P&L but DAR-reducing (never "DAR-increasing")
- [ ] Lower warrant/rights costs described as negative P&L but DAR-reducing
- [ ] No assumption that a name was "exited" just because it left the top 10
- [ ] Narrative uses "fell out of the top 10" and "(was $XK)" for disappeared names
- [ ] Red (#CC0000) formatting applied to negative values in tables
- [ ] Document validated with `python scripts/office/validate.py`
