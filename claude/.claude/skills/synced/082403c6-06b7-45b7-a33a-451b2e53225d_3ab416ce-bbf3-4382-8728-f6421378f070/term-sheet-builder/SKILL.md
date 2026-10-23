---
name: term-sheet-builder
description: "Draft and generate professional term sheets (.docx) for Meteora Capital's structured equity financing transactions. Use this skill whenever the user asks to create, draft, build, or generate a term sheet for any of the following: Forward Purchase Agreements (FPAs), Standby Equity Purchase Agreements (SEPAs), Equity Lines of Credit (ELOCs), Convertible Pre-Paid Advances, convertible notes, or any combination of these structures. Also trigger when the user mentions deSPAC financing term sheets, SPAC trust recycling proposals, structured equity proposals, or asks to prepare a financing proposal for a company. Trigger on phrases like 'draft a term sheet', 'build a term sheet', 'create a SEPA term sheet', 'FPA term sheet', 'ELOC proposal', 'convertible term sheet', or any mention of generating Meteora financing documentation for a specific company or deal."
---

# Term Sheet Builder for ELOCs, Converts, and FPAs

## Overview

This skill generates professional term sheets (Word .docx files) for Meteora Capital's structured equity transactions. It covers three core deal structures:

1. **Forward Purchase Agreements (FPAs)** — Meteora purchases SPAC shares from open market or redeeming shareholders, holds through deSPAC, and settles at maturity
2. **Standby Equity Purchase Agreements (SEPAs / ELOCs)** — Equity line of credit facility where the company can draw down capital by issuing shares to Meteora at a discount to market
3. **Convertible Pre-Paid Advances** — Convertible promissory notes that convert at a variable conversion price, typically bundled with a SEPA

Term sheets may include one structure alone, or combine multiple (e.g., FSPA + SEPA + Converts).

## When to Use This Skill

Use this skill whenever the user asks to:
- Draft, create, or build a term sheet for a SEPA, ELOC, FPA, forward purchase agreement, convertible note, or pre-paid advance
- Modify an existing Meteora term sheet template
- Generate a term sheet for a deSPAC deal, SPAC transaction, or small/micro-cap financing
- Create a financing proposal for a company

## Prerequisites

```bash
npm install -g docx
```

Also requires the docx validation script at `/mnt/skills/public/docx/scripts/office/validate.py`.

## Step 1: Gather Deal Parameters

Before generating, collect all required parameters from the user. Ask for anything not provided.

### Header / Entity Information
| Parameter | Description | Example |
|-----------|-------------|---------|
| `dealType` | "despac" or "direct" | "despac" |
| `spacName` | SPAC entity name (deSPAC only) | "Relativity Acquisition Corp." |
| `targetName` | Target / NewCo name | "Instinct Brothers" |
| `companyName` | The legal counterparty (= spacName if deSPAC, = targetName if direct) | "Relativity Acquisition Corp." |
| `ticker` | SPAC or company ticker (for FSPA references) | "RLTY" |
| `termSheetDate` | Date of the term sheet | "February 6, 2026" |

### Structure Selection
Ask which structures to include. At least one is required:

| Structure | Include? | Notes |
|-----------|----------|-------|
| **FSPA** (Forward Share Purchase Agreement) | Yes/No | Typically for deSPAC deals |
| **SEPA** (Standby Equity Purchase Agreement) | Yes/No | The equity line facility |
| **Convertible Pre-Paid Advances** | Yes/No | Usually bundled with SEPA |

### FSPA Parameters (if included)
| Parameter | Default | Description |
|-----------|---------|-------------|
| `fspaAmount` | — | Max dollar value of recycled shares (e.g., $75,000,000) |
| `fspaMaturity` | 3 months post-close or S-1 effectiveness | Maturity date description |
| `settlementAdjustment` | $0.75 | Per-share deduction from VWAP during valuation period |
| `shareCommitmentFee` | 75,000 shares | Netted from recycled shares |
| `referencePrice` | $10.00 | Reference price per share |
| `valuationMultiple` | 10x | Volume multiple for valuation period |

### SEPA Parameters (if included)
| Parameter | Default | Description |
|-----------|---------|-------------|
| `sepaMaxCommitment` | — | Maximum commitment amount (e.g., $150,000,000) |
| `sepaCommitmentPeriod` | 36 months | Duration of the facility |
| `commitmentFeePercent` | 1% | Percentage of max commitment |
| `commitmentFeeCap` | $500,000 | Dollar cap on commitment fee |
| `purchasePriceDiscount` | 97% | Company-initiated notice purchase price as % of market price |

### Convertible Pre-Paid Advance Parameters (if included)
| Parameter | Default | Description |
|-----------|---------|-------------|
| `initialTranche` | — | Cash amount at closing (e.g., $500,000 or $1,000,000) |
| `conversionDiscount` | 95% | % of lowest 5-day VWAP for conversion price |

### Optional Terms
| Parameter | Default | Description |
|-----------|---------|-------------|
| `includeROFR` | true | Include Right of First Refusal section |
| `rofrPercent` | 50% | ROFR participation percentage |
| `volumeThreshold` | 30% | Daily volume limitation (almost never changes) |
| `constraintThreshold` | 30% | Company-initiated notice constraint (almost never changes) |
| `diligenceFees` | $45,000 | Legal fee cap |
| `governingLaw` | "State of New York" | Governing law |

## Step 2: Generate the Document

Read the template script at `scripts/term_sheet_template.js` for the base document structure. Then customize it with the user's parameters.

### Key Formatting Rules
- **Font**: Times New Roman throughout
- **Title**: Left-aligned, bold, 11pt
- **Table layout**: Two columns — left column (labels, no shading, bold) and right column (content)
- **Table borders**: Thin black single borders
- **Page size**: US Letter (12240 x 15840 DXA) with 0.75" margins (1080 DXA)
- **Preamble**: Italicized, 9pt

### Document Structure

The document follows this order:
1. **Header** — "Meteora Capital – [SPAC] x [Target]" (deSPAC) or "Meteora Capital – [Company]" (direct)
2. **Preamble** — Standard legal disclaimer (replace company name only)
3. **"Terms of the Offering" heading**
4. **Term table** — Each structure gets its rows, in this order:
   - Meteora Lead Investor Commitment (summary of what's included)
   - FSPA rows (if applicable): Transaction Description, Maturity Date/Tenor, FSPA Acceleration Provisions, Maturity Settlement, Share Commitment Fee, Cash Commitment Fee, Interest Rate, Reference Price, Covenants
   - SEPA row
   - Commitment Fee row
   - Purchase Price row (Company-Initiated and Investor-Initiated subsections)
   - Convertible Pre-Paid Advances row
   - Constraints on Company-Initiated Notices row
   - Volume Thresholds row (Daily Volume Limitation and Automatic Reduction subsections)
   - ROFR row (if included)
   - Diligence and Legal Fees row
   - Governing Law row
5. **Confidentiality and Exclusivity** paragraph
6. **Signature page** — Always includes Meteora/Vik. For deSPAC: SPAC signature block + Target signature block. For direct: just the company signature block.

### Critical Variable Fields Summary

These are the fields that change deal-to-deal and MUST be customized:

| What Changes | Where in Doc |
|-------------|--------------|
| Entity names | Header, preamble, signature blocks |
| Ticker | FSPA transaction description |
| Dollar amounts | FSPA amount, SEPA max commitment, initial tranche, commitment fee cap |
| FSPA settlement adjustment | Maturity Settlement section ($X.XX per share) |
| Share commitment fee | Share Commitment Fee row |
| Reference price | Reference Price row |
| SEPA purchase price % | Purchase Price section (e.g., 97%) |
| Conversion discount % | Convertible Pre-Paid Advances section (e.g., 92%, 95%) |
| Commitment fee % and cap | Commitment Fee row |
| ROFR inclusion and % | ROFR row (or omit entirely) |

### What Almost Never Changes
- Volume thresholds (30%)
- Constraint thresholds (30%)
- Covenants (no shorting, 9.9% blocker, lock-ups)
- Diligence fee cap ($45,000)
- Governing law (New York)
- Confidentiality/Exclusivity language
- Preamble legal language (except entity name)
- Valuation period (10x volume)

## Step 3: Validate and Deliver

After generating the .docx:

```bash
python /mnt/skills/public/docx/scripts/office/validate.py output.docx
```

Copy to `/mnt/user-data/outputs/` and present to the user via `present_files`.

## Template Reference

The base template script is at `scripts/term_sheet_template.js`. This contains the full document generation code using the `docx` npm package. When building a term sheet:

1. Copy the template to `/home/claude/`
2. Modify the variables at the top of the script based on deal parameters
3. Add or remove table rows based on which structures are included
4. Run with `node` to generate the .docx

See the template script for the complete implementation including all table rows, formatting, and signature blocks.
