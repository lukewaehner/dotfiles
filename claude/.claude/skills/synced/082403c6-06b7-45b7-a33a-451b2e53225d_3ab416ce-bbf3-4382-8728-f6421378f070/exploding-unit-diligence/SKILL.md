---
name: exploding-unit-diligence
description: "Full due diligence on Maxim-style exploding unit deals (F-1, S-1, 424B4) — breakeven modeling, Nasdaq delisting risk, cap structure review, existing instrument reset analysis, and risk matrix. Trigger when the user asks to analyze or do diligence on an exploding unit deal, uploads a 424B4/F-1/S-1 for a structured warrant offering, or asks about delisting risk, reverse split traps, cap table instruments, lock-ups, or deal risks. Trigger phrases: 'do diligence on this deal', 'analyze this exploding unit', 'what are the risks', 'model the breakeven and risks', 'check for delisting risk', 'look at the cap structure', 'build me a full analysis'. Supersedes warrant-f1-analysis for comprehensive requests; use that skill only for quick breakeven-only models."
---

# Exploding Unit Deal — Full Diligence & Risk Analysis

## Overview

This skill produces a **comprehensive Excel workbook** analyzing Maxim-style exploding unit deals (F-1/S-1/424B4 structured warrant offerings with reset provisions and zero exercise price options). The output goes beyond breakeven math to include:

1. **Breakeven Model** — Share explosion math, P&L sensitivity
2. **Cap Structure & Existing Instruments** — Pre-existing warrants, convertibles, and other resetting instruments
3. **Nasdaq Delisting Risk Matrix** — Reverse split disqualification, Low Price Rule, MVLS/MVPHS, cure timelines
4. **Lock-Up & Insider Analysis** — Who's locked up, for how long, what can move
5. **Risk Summary** — Color-coded risk dashboard with severity ratings

---

## Step 1: Gather Deal Terms

### From the Filing (424B4 / F-1 / S-1)

Extract these terms systematically. Read the filing in this order:

**Cover page / Page 1:**
- Offering price per unit
- Total units offered
- Warrant coverage ratio (units : warrants)
- Zero exercise price multiplier
- Reset schedule (which trading days, what percentages)
- Warrant term (years)
- Over-allotment option (shares and/or warrants)
- Total gross proceeds

**Description of Warrants section (typically p.145-165):**
- Exercise price mechanics (confirm = offering price)
- Reset dates and percentages (confirm cover page)
- **FLOOR PRICE** — Critical. Search the full filing for "floor" to find it. This caps how low the reset strike can go.
- Exercise limitation (4.99% / 9.99% blocker)
- Cashless exercise formula
- Anti-dilution provisions (structural only vs. price-based)
- Fundamental transactions provisions

**Capitalization section (typically p.66-68):**
- Shares outstanding pre-offering (Class A and Class B)
- Pro forma shares post-offering
- Any existing warrants, options, convertible instruments listed

**Recent Developments section:**
- Prior offerings and their terms
- Prior warrant exercises and share issuances
- Reverse stock split history — **THIS IS CRITICAL FOR DELISTING ANALYSIS**

**Underwriting section (typically p.154-160):**
- Lock-up agreements (who, how long)
- Company lock-up period
- Over-allotment details

### From the User

After extracting everything from the filing, ask only for what's missing:
- Meteora allocation amount ($)
- Current stock price (if not in filing)
- Assumed exit prices for sensitivity analysis
- Commission rate (default: 30 mills / $0.030 per share)

---

## Step 2: SEC Filing Deep Dive — Risk Research

### 2a. Reverse Split History

**This is the single most important risk factor.** Search for:
- "reverse stock split" / "share consolidation" / "reverse split" in the filing
- Check the Recent Developments section
- Search EDGAR for 6-K filings from the past 12 months mentioning reverse splits
- Search web for "[TICKER] reverse stock split [year]"

**Why it matters:** Under Nasdaq Rule 5810(c)(3)(A)(iv) (SEC Release 34-102245, approved Jan 23, 2025):
- If the company did a reverse split in the **prior 12 months**, OR
- Cumulative 250:1+ reverse splits in the prior **2 years**
- → **NO compliance period** on the next bid price deficiency
- → Stock falls below $1.00 for 30 consecutive business days = immediate Staff Delisting Determination

Record: reverse split ratio, effective date, 12-month expiry date.

### 2b. Current Nasdaq Compliance Status

Search the filing's risk factors and Recent Developments for:
- "Nasdaq" + "deficiency" / "non-compliance" / "listing rule"
- Current deficiency notices (bid price, MVLS, MVPHS, filing delinquency)
- Cure deadlines (180 calendar days from notification date)
- Whether any deficiencies have been cured

**Key Nasdaq rules to assess (read references/nasdaq_rules.md for full details):**

| Rule | Trigger | Consequence | Cure Period |
|------|---------|-------------|-------------|
| Low Price (5810(c)(3)(A)(iii)) | ≤$0.10 for 10 consecutive business days | Immediate delisting + trading suspension | NONE |
| Prior R/S Disqualification (5810(c)(3)(A)(iv)) | R/S in prior 12 months + below $1.00 for 30 days | Immediate delisting determination | NONE |
| Bid Price (5450(a)(1)) | Below $1.00 for 30 consecutive days | Deficiency notice | 180 days (if no R/S trap) |
| MVLS - Global Market (5450(b)(2)(A)) | Below $50M for 30 days | Deficiency notice | 180 days |
| MVPHS - Global Market (5450(b)(2)(C)) | Below $15M for 30 days | Deficiency notice | 180 days |
| Proposed $5M MVLS (pending) | Below $5M for 30 days | Immediate suspension/delisting | NONE (if approved) |

### 2c. Existing Instruments in Cap Structure

Search the filing for ALL of these:
- **Prior warrants** — Look for "Prior Warrants", "February 2026 Offering", "prior offering" in Recent Developments. Check if they have:
  - Price-based anti-dilution (full ratchet or weighted average) — would reset on this new deal
  - Structural anti-dilution only (stock splits/dividends) — would NOT reset on this new deal
  - How many remain outstanding vs. already exercised
- **Convertible notes** — Search for "convertible", "conversion", "note" in financial statement notes
  - Check for floating conversion rates tied to market price
  - Check for anti-dilution provisions
- **ELOCs / SEPAs / Standby facilities** — Search for "equity line", "standby", "purchase agreement"
- **Stock incentive plans** — Search for "incentive plan", "S-8", grants outstanding
- **Legacy warrant shares** — From SPAC/merger transactions

For each instrument found, document: type, quantity outstanding, strike/conversion price, anti-dilution provision type, whether it resets on this deal, and remaining term.

### 2d. Lock-Up Agreements

Extract from the Underwriting section:
- Who is locked up (directors, officers, company)
- Duration from closing (typically 90 days for insiders, 30 days for company)
- What's restricted (sale, transfer, encumbrance, option grants)
- Who can waive (typically the underwriter)
- **Critically: Investors/offering participants are NOT locked up** — they can sell immediately

---

## Step 3: Build the Excel Model

### Required Tabs

Read **references/excel_model_spec.md** for the complete cell-by-cell specification of each tab. The model has 4 tabs:

1. **Breakeven Model** — Deal terms, share explosion math, breakeven calculation, P&L sensitivity
2. **Exit Price Sensitivity** — Full exit price scenario table
3. **Cap Structure & Risk** — Shares outstanding, existing instruments, Nasdaq compliance, delisting timeline, risk matrix
4. **Hypothetical Quick Calc** — Simple scenario tool (from warrant-f1-analysis skill)

### Critical Formulas

**Share Explosion (when floor does NOT bind):**
```
Warrant Shares After Reset 2 = Initial Warrants × (Basis Price / Reset 2 Strike)
Exploded Shares = Warrant Shares After Reset 2 × ZEP Multiplier
Total Shares = Common Shares from Units + Exploded Shares
Breakeven = Gross Proceeds / Total Shares
```

**Share Explosion (when floor DOES bind):**
```
Effective Strike = MAX(Reset 2 Strike, Floor Price)
Warrant Shares After Reset 2 = Initial Warrants × (Basis Price / Effective Strike)
```
The floor binding changes everything — it caps how many shares explode out, raising the breakeven.

**Breakeven discount is always:**
```
Discount = 1 - (Breakeven / Offering Price)
```
For standard 50% reset + 2.0x ZEP, this is always ~80%. If floor binds, it's less.

### Tab 3 Specification: Cap Structure & Risk

This tab has 4 sections:

**Section A: Shares Outstanding**
- Pre-offering Class A / Class B
- New shares from this offering
- Prior warrant shares (exercised and remaining)
- Other instruments (convertible shares, incentive plan)
- Post-offering float (before new warrants)
- Max exploded warrant shares (this deal)
- Over-allotment (if exercised)
- **Fully diluted total**

**Section B: Existing Instruments Risk**
Table with columns: Instrument | Qty Outstanding | Strike/Conversion | Anti-Dilution Type | Resets on This Deal? | Risk Level
- Color code: RED = resets on this deal (price-based anti-dilution), YELLOW = may reset, GREEN = does not reset

**Section C: Nasdaq Delisting Timeline**
Chronological table: Event | Date | Rule | Impact | Days Remaining
- Include: reverse split date, deficiency notices, cure deadlines, offering close, Low Price trigger scenarios, MVLS/MVPHS deadlines, Hearings Panel estimates
- Color code: RED = immediate risk (no cure), ORANGE = near-term deadline, YELLOW = medium-term

**Section D: Risk Summary Matrix**
Table with columns: Risk Factor | Severity (1-5) | Probability | Impact | Mitigation | Notes
Include these risk categories:
1. **Low Price Rule ($0.10)** — 10 business days to delisting, no cure
2. **Reverse Split Trap** — No compliance period if R/S in prior 12 months
3. **MVLS/MVPHS Cure Deadline** — Days remaining to April 1 (or relevant date)
4. **Proposed $5M MVLS Rule** — Pending SEC approval
5. **Existing Instrument Dilution** — Prior warrants/converts that may reset
6. **Lock-Up Expiry** — When insiders can sell
7. **Volume/Liquidity Risk** — Can we monetize the position in time?
8. **Going Concern** — Does the company have a going concern opinion?
9. **HFCAA/PCAOB Risk** — For Chinese issuers
10. **Registration Effectiveness** — Is the F-1/S-1 effective yet?

---

## Step 4: Formatting Standards

Follow all formatting rules from the xlsx skill (read /mnt/skills/public/xlsx/SKILL.md). Additionally:

- **Blue font**: All hardcoded inputs from the filing
- **Black font**: All formulas
- **Red background (light)**: HIGH risk items in risk matrix
- **Orange background**: MEDIUM risk items
- **Green background (light)**: LOW risk / favorable items
- **Yellow background**: Key assumptions needing attention
- Number formats: Share counts `#,##0`, Prices `$#,##0.0000`, Dollars `$#,##0`, Percentages `0.0%`
- After creation: `python /mnt/skills/public/xlsx/scripts/recalc.py <output_file>`

---

## Step 5: Present Results

After building the model, provide a concise narrative summary covering:
1. Breakeven price and discount to offering
2. Top 3 risks with severity
3. Whether any existing instruments reset on this deal
4. Delisting timeline — what's the most binding constraint?
5. Recommended allocation sizing (if enough data)

Do NOT write a long report restating everything in the Excel — the model speaks for itself. Focus on the 2-3 things that could kill the trade.
