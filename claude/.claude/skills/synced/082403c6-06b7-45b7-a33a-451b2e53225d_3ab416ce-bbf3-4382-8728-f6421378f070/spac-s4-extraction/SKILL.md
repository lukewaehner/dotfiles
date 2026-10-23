---
name: spac-s4-extraction
description: Full S-4 extraction and analysis for SPAC business combination filings. Trigger when the user uploads an S-4 PDF (or references one in context) and asks to 'extract', 'run the S-4', 'do the extraction', 'analyze this S-4', 'pull the terms', 'run the guide on this', 'S-4 review', 'SPAC analysis', or any request to systematically extract SPAC deal terms from a registration statement. Also trigger when the user drops an S-4 PDF without further instructions — the default action is to run the full extraction. Produces a 12-section structured memo covering business fundamentals, deal terms, capitalization, financials, PIPE/financing, capital structure, warrants, risk factors, insider economics, management, audit quality, and valuation. Always use this skill for S-4 extractions — do not attempt ad hoc without it.
---

# SPAC S-4 Extraction Skill

Full structured extraction of SPAC business combination S-4 / proxy statement filings across 12 sections.

---

## Step 1: Extract the PDF

The S-4 is a large PDF. Use `pdftotext` to extract it before analysis:

```bash
pdftotext -layout /mnt/user-data/uploads/<filename>.pdf /home/claude/s4_text.txt
wc -l /home/claude/s4_text.txt
head -300 /home/claude/s4_text.txt
```

If the file is very large (>40,000 lines), use targeted `grep` and `sed` to locate relevant sections rather than reading end to end. Key search terms:

```bash
# Identify SPAC, target, and Pubco names
head -200 /home/claude/s4_text.txt

# Deal economics
grep -n "enterprise value\|equity value\|trust account\|minimum cash\|Available Transaction Cash\|PIPE\|subscription\|consideration" /home/claude/s4_text.txt | head -50

# Capitalization / ownership tables
grep -n "Pro Forma\|ownership.*percent\|redemption.*scenario\|no redemption\|maximum redemption" /home/claude/s4_text.txt | head -30

# Financial statements
grep -n "Balance Sheet\|Statement of Operations\|Cash Flow\|F-[0-9]\|Report of Independent" /home/claude/s4_text.txt | head -40

# Termination / conditions / MCC
grep -n "termination\|outside date\|minimum cash\|Available Transaction Cash\|closing condition" /home/claude/s4_text.txt | head -30

# Warrants
grep -n "warrant.*exercise\|11.50\|redemption.*18\|VWAP.*20.*30\|private.*warrant\|public.*warrant" /home/claude/s4_text.txt | head -30

# Auditors / going concern
grep -n "going concern\|substantial doubt\|Deloitte\|PwC\|KPMG\|EY\|CBIZ\|Marcum\|Withum\|PCAOB\|PFIC\|material weakness" /home/claude/s4_text.txt | head -30

# Lock-ups / promote
grep -n "lock.up\|founder share\|promote\|earnout\|vesting" /home/claude/s4_text.txt | head -30
```

Use `sed -n 'START,ENDp'` to read specific line ranges once you've located relevant sections.

---

## Step 2: Load the Extraction Guide

Read the full 12-section guide before beginning:

```
/mnt/skills/user/spac-s4-extraction/references/s4-guide.md
```

The guide contains exact prompts, sourcing instructions, and output format requirements for each section.

---

## Step 3: Run the Extraction

Work through all 12 sections in order. For each section:

1. **Locate relevant text** using grep/sed on the extracted text file
2. **Extract verbatim language** for key terms (valuation, termination, going concern, etc.)
3. **Present in the required format** — tables for financials, bullet points for deal terms, prose for business model

**Critical output requirements:**
- Financial statements (Sections 4.1–4.3): full tables only, no bullet lists, verbatim line items
- Debt schedule (Section 4.5): structured table from notes only, not balance sheet totals
- Valuation (Section 2.2.2): verbatim language from filing; do not calculate EV unless filing provides the components
- Going concern (Sections 4.6, 8.2.1, 11.3.2): quote "substantial doubt" language directly if present
- Insider economics (Section 9.4): conclude with a clear Yes or No
- If a detail is not disclosed: write **"Not disclosed."** — never infer

**For large filings:** The financial statements are in the "F-pages" (F-1 through F-XX). Use `grep -n "F-[0-9]\|BALANCE SHEET\|STATEMENT OF OPERATIONS\|CASH FLOW"` to locate them, then `sed` to extract the relevant ranges.

---

## Step 4: Output Format

Deliver as a single structured memo with:
- Clear section headers matching the guide (1.1, 1.2 … 12.3.2)
- Deal name / SPAC ticker in the header
- Filing date
- Tables for all financial data
- Concise prose for narrative sections

---

## Common Pitfalls

- **Multiple entities:** Large S-4s often include financials for the SPAC, the target, and Pubco separately. Identify which entity's financials you're presenting for each section. The primary target financials go in Section 4; SPAC financials are supplementary.
- **XRP / crypto / NAV deals:** No traditional revenue model — adapt the business model and projections sections accordingly; note "Not applicable" where appropriate.
- **Going concern on SPAC:** Standard boilerplate for SPACs approaching their deadline. Note it but don't conflate with target company going concern.
- **Adjustment shares / earnout-like features:** XRP-price-indexed or stock-price-indexed share issuances are structurally like earnouts even if not labeled as such — flag them in Section 2.5.
- **PIPE lock-up gap:** Check explicitly whether PIPE/subscription shares are exempt from lock-up restrictions (common; material). Flag in Section 3.4 if present.
- **Fairness opinion conflicts:** Note if fairness opinion provider is also placement agent or has contingent compensation.
