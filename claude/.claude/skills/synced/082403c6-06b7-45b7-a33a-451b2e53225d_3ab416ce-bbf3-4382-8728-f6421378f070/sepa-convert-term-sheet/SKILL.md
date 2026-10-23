---
name: sepa-convert-term-sheet
description: "Draft and generate professional term sheets (.docx) for Meteora Capital's structured equity financing transactions. Use this skill whenever the user asks to create, draft, build, or generate a term sheet for any of the following: Forward Purchase Agreements (FPAs), Standby Equity Purchase Agreements (SEPAs), Equity Lines of Credit (ELOCs), Convertible Pre-Paid Advances, convertible notes, or any combination of these structures. Also trigger when the user mentions deSPAC financing term sheets, SPAC trust recycling proposals, structured equity proposals, or asks to prepare a financing proposal for a company. Trigger on phrases like 'draft a term sheet', 'build a term sheet', 'create a SEPA term sheet', 'FPA term sheet', 'ELOC proposal', 'convertible term sheet', or any mention of generating Meteora financing documentation for a specific company or deal."
---

# Term Sheet Builder — SEPA + Convertible Pre-Paid Advance

## Overview

Generates a professional two-page `.docx` term sheet for Meteora Capital's SEPA + Convertible Pre-Paid Advance transactions. The output covers:

1. **Terms page** — preamble + four-section term table + Confidentiality/Exclusivity
2. **Signature page** — execution blocks for Meteora and the Company

Both pages carry the Meteora Capital logo in the upper-right corner.

---

## Quick Start

### Step 1 — Collect deal parameters

Ask for any missing parameters before generating. The minimum required set:

| Parameter | Example |
|-----------|---------|
| Company legal name | "Beamr Imaging Ltd." |
| Ticker | "BMR" |
| Date | "April 1, 2026" |
| SEPA max commitment | "$100,000,000" |
| SEPA term | "36 months" |
| Initial advance (funded) | "$4,000,000" |
| OID % | "10%" → principal = funded ÷ (1 − OID) |
| Company-initiated advance price | "97% of VWAP on notice date" |
| Investor-initiated advance price | "94% of lowest 5-day VWAP" |
| Variable conversion price | "94% of lowest 5-day VWAP" (usually = investor-initiated) |
| Fixed conversion price | "$1.43" |
| Floor price % | "20% of fixed price" |
| Commitment fee | "1% of commitment = $1,000,000" |
| Diligence fee cap | "$45,000" (default — rarely changes) |

### Step 2 — Run the template

```bash
# 1. Copy template to working directory
cp /mnt/skills/user/term-sheet-builder/scripts/term_sheet_template.js /home/claude/
cp /path/to/meteora_logo.png /home/claude/    # must be named meteora_logo.png

# 2. Edit parameters at the top of the script (DEAL PARAMETERS section)

# 3. Generate
cd /home/claude && node term_sheet_template.js

# 4. Validate
python3 /mnt/skills/public/docx/scripts/office/validate.py /home/claude/output/TICK_Term_Sheet_Meteora.docx

# 5. Deliver
cp /home/claude/output/TICK_Term_Sheet_Meteora.docx /mnt/user-data/outputs/
```

---

## Document Formatting Standards

These are Meteora's house standards — do not change without explicit instruction.

| Element | Spec |
|---------|------|
| Font | Times New Roman throughout |
| Body size | 10pt (size: 20 in docx half-points) |
| Preamble size | 9pt (size: 18) |
| Disclaimer size | 8pt (size: 16) |
| Page size | US Letter (12240 × 15840 DXA) |
| Margins | 0.75" all sides (1080 DXA) |
| Table width | 9360 DXA (full content width) |
| Label column | 2000 DXA, light gray fill (F5F5F5) |
| Content column | 7360 DXA, white |
| Cell borders | Single, 0.5pt, black (000000) |
| Section headers | Full-width, gray fill (DDDDDD), bold |
| Logo | 120x120px, upper-right both pages |
| Logo file | meteora_logo.png (square, black on white) |

---

## Document Structure

### Section I — Transaction Overview
- Parties (Issuer, Investor, Currency, Date)
- Transaction Summary (SEPA + Pre-Paid Advance narrative)

### Section II — SEPA
- Maximum Commitment
- Commitment Period
- Advance Structure (Equity vs. Debt + Concurrent SEPA Availability)
- Commitment Fee
- Purchase Price (Company-Initiated / Investor-Initiated)
- Volume Thresholds & Limitations (30% ADTV)
- Constraints on Company Notices
- Registration Rights
- Right of First Refusal (ROFR) — binding provision

### Section III — Convertible Pre-Paid Advance / Convertible Notes
- Initial Upfront Advance
- Principal & Purchase Price (OID mechanics)
- Maturity (12 months per note)
- Interest Rate (0%)
- Conversion Price (Fixed / Variable / Floor)
- Floor Price
- Conversion Mechanics
- Optional Redemption (110% prepayment)
- Beneficial Ownership Cap (9.99%)
- Covenants (No Short Sales / MFN / Use of Proceeds)

### Section IV — General Terms
- Variable Rate Transaction Prohibition — binding, with injunctive relief
- Representations & Warranties
- Diligence & Legal Fees
- Governing Law — binding provision
- Definitive Documentation

### Epilogue
- Confidentiality and Exclusivity — binding provision

### Signature Page
- Meteora: Vik Mittal, Managing Member
- Company: blank execution block

---

## Key Pricing Mechanics

### OID Calculation
```
Principal = Funded Amount / (1 - OID%)
Example:  $4,000,000 / (1 - 0.10) = $4,444,444
```

### Advance Pricing Convention
| Direction | Price Basis |
|-----------|-------------|
| Company-initiated | % of VWAP on the date of notice (single day) |
| Investor-initiated | % of lowest VWAP over prior 5 trading days |

### Variable Conversion Price
- Always matches the Investor-Initiated advance price (same discount, same 5-day lookback)
- Note this alignment explicitly in the term sheet

### Floor Price
```
Floor = Fixed Conversion Price x Floor%
Example: $1.43 x 20% = $0.286
```

---

## Frequently Adjusted Terms

| Term | Variable in script |
|------|-------------------|
| Company name / ticker / date | COMPANY_NAME, TICKER, DATE |
| Funded amount + OID + principal | FUNDED_AMT, OID_PCT, PRINCIPAL_AMT |
| SEPA size and term | SEPA_MAX, COMMIT_PERIOD |
| Company-initiated advance price | CO_DISC |
| Investor-initiated advance price | INV_DISC |
| Variable conversion price | VAR_DISC (usually = INV_DISC) |
| Fixed conversion price | FIXED_CONV |
| Floor price % and dollar | FLOOR_PCT, FLOOR_PRICE |
| Commitment fee % and amount | COMMIT_FEE_PCT, COMMIT_FEE_AMT |

## Rarely Changed Terms
- Volume thresholds (30% ADTV)
- Maturity (12 months per note)
- Interest rate (0%)
- Optional redemption premium (110%)
- Beneficial ownership cap (9.99%)
- ROFR participation (50%)
- Diligence fee cap ($45,000)
- Governing law (New York / AAA arbitration)
- Preamble language (only company name changes)
- Confidentiality/Exclusivity language
- VRT carve-outs (SEPA/notes, employee plans, M&A)

---

## Logo Handling

The logo must be named `meteora_logo.png` and placed in the same directory as the script before running.

Use the square black-on-white Meteora Capital logo (400x400px). If the logo file is missing, the script generates cleanly without it and prints a warning.

Do NOT use the wide banner version (Meteora_Header.png) — it has a black artifact bar in the top-right that renders incorrectly in Word.

---

## Validation

Always run after generating:

```bash
python3 /mnt/skills/public/docx/scripts/office/validate.py output.docx
```

Expected: ~110 paragraphs, All validations PASSED.

---

## Template Script

The full working template is at `scripts/term_sheet_template.js`. It is self-contained — edit the DEAL PARAMETERS block at the top and run with `node`. No other files needed except the logo.
