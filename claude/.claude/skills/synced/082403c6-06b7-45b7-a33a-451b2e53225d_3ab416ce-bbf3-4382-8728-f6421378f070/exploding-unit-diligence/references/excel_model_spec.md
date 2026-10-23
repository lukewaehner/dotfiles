# Excel Model Specification — Exploding Unit Diligence

## Workbook Structure

The model has 4 tabs. All formulas use Excel cell references — NEVER hardcode calculated values.

---

## Tab 1: "Breakeven Model"

### Section 1: Deal Terms (Rows 5-22)

Headers in Row 5: B="DEAL TERMS (424B4)" | C="Value" | D="Source" | E="Notes"
Header style: White font, dark blue fill (2F5496)

| Row | B (Label) | C (Value) | D (Source) | E (Notes) |
|-----|-----------|-----------|------------|-----------|
| 6 | Offering Price per Unit | [hardcoded, blue] | "424B4 p.X" | "= Basis Price" |
| 7 | Total Units Offered | [hardcoded, blue] | "424B4 p.X" | "Firm commitment" |
| 8 | Over-Allotment Units (shares) | [hardcoded, blue] | "424B4 p.X" | "45-day option" |
| 9 | Over-Allotment Warrants | [hardcoded, blue] | "424B4 p.X" | "$0.001 per warrant" |
| 10 | Gross Proceeds (base) | =C6*C7 | "" | formula |
| 11 | Gross Proceeds (w/ full OA) | =C10+(C8*[OA share price])+(C9*0.001) | "" | formula |
| 12 | (blank) | | | |
| 13 | Warrant Strike (Initial) | =C6 | "" | "= Basis Price (100%)" |
| 14 | Reset 1: Day N (70%) | =C6*0.7 | "" | "70% × Basis Price" |
| 15 | Reset 2: Day N (50%) | =C6*0.5 | "" | "50% × Basis Price" |
| 16 | Floor Price | [hardcoded, blue] | "424B4 p.X" | "Hard floor on resets" |
| 17 | Floor Binding? | =IF(C16>C15,"YES - Floor binds","NO - Floor does NOT bind") | "" | logic check |
| 18 | Effective Reset 2 Strike | =MAX(C15,C16) | "" | "MAX(Reset 2, Floor)" |
| 19 | (blank) | | | |
| 20 | Zero Exercise Price Multiplier | [hardcoded, blue] | "424B4 p.X" | typically 2.0 |
| 21 | Warrant Term | [hardcoded text, blue] | "424B4 p.X" | "3 years" etc |
| 22 | Warrant Coverage | [hardcoded text, blue] | "424B4 p.X" | "1:1" etc |

Formatting notes:
- Hardcoded inputs: blue font (0000FF), light cyan fill (DAEEF3)
- Formulas: black font, light gray fill (F2F2F2)
- Number formats: prices = `$#,##0.0000`, share counts = `#,##0`, dollars = `$#,##0`

### Section 2: Share Explosion Math (Rows 24-37)

Headers in Row 24: B="SHARE EXPLOSION MATH" | C="Shares" | D="Formula" | E="Notes"

| Row | B (Label) | C (Formula) | D (Description) |
|-----|-----------|-------------|-----------------|
| 25 | Common Shares from Units | =C7 | "= Total Units" |
| 26 | Warrants Issued (initial) | =C7 | "= Total Units" |
| 27 | (blank) | | |
| 28 | Warrant Shares After Reset 2 | =C26*C6/C18 | "Warrants × (Basis/Effective Strike)" |
| 29 | Exploded Shares (ZEP 2.0x) | =C28*C20 | "Reset shares × multiplier" |
| 30 | (blank) | | |
| 31 | **TOTAL SHARES RECEIVED** | =C25+C29 | "Common + Exploded" |
| 32 | (blank) | | |
| 33 | If Over-Allotment Exercised: | (label only) | |
| 34 | OA Common Shares | =C8 | |
| 35 | OA Warrants → Exploded | =C9*C6/C18*C20 | "OA warrants fully exploded" |
| 36 | **TOTAL w/ Full OA** | =C31+C34+C35 | |

TOTAL rows: yellow result fill (FFF2CC)

### Section 3: Breakeven Analysis (Rows 39-52)

Headers in Row 39: B="BREAKEVEN ANALYSIS" | C="Value"

| Row | B (Label) | C (Formula) | Format |
|-----|-----------|-------------|--------|
| 40 | Total Capital Deployed | =C10 | $#,##0 |
| 41 | Total Shares Received (base) | =C31 | #,##0 |
| 42 | (blank) | | |
| 43 | **BREAKEVEN PRICE PER SHARE** | =C40/C41 | $#,##0.0000 |
| 44 | Discount to Offering Price | =1-(C43/C6) | 0.0% |
| 45 | Margin of Safety (vs Offering Px) | =1-(C43/C6) | 0.0% |
| 46 | (blank) | | |
| 47 | With Full Over-Allotment: | (label) | |
| 48 | Capital Deployed (w/ OA) | =C11 | $#,##0 |
| 49 | Shares Received (w/ OA) | =C36 | #,##0 |
| 50 | Breakeven (w/ OA) | =C48/C49 | $#,##0.0000 |
| 51 | (blank) | | |
| 52 | 424B4 Stated Exploded Shares | [hardcoded, blue] | #,##0 — cross-check |

BREAKEVEN row: green fill (E2EFDA) — this is the key output.

**Cross-check:** The 424B4 cover page states total exploded warrant shares. Compare C29 to C52. They MUST match. If they don't, there's an error in the floor price or reset structure.

---

## Tab 2: "Exit Price Sensitivity"

### P&L Sensitivity Table

Row 2: Title "P&L SENSITIVITY — Exit Price Scenarios (Base Deal, No OA)"
Row 4 Headers: B="Exit Price" | C="Gross Proceeds" | D="Net P&L" | E="Return %" | F="vs Offering"

For each exit price scenario (rows 5+):
- B: [hardcoded exit price, blue] — use range from $0.01 to offering price + upside
- C: `=B{r}*'Breakeven Model'!C31`
- D: `=C{r}-'Breakeven Model'!C10`
- E: `=D{r}/'Breakeven Model'!C10`
- F: `=B{r}/[offering price]-1`

**Recommended exit prices to always include:**
- $0.01, $0.02, $0.03, $0.04, $0.05 (sub-penny range)
- $0.06, $0.08, $0.10 (around typical floors and Low Price Rule threshold)
- $0.15, $0.20, $0.25, $0.30 (mid-range recovery)
- Offering price (shows the 4x-5x upside if stock doesn't move)
- $0.40, $0.50 (upside scenarios)

Adjust range based on the specific deal's offering price.

---

## Tab 3: "Cap Structure & Risk"

This is the most important tab for risk assessment. It has 4 sections.

### Section A: Shares Outstanding (Rows 4-15)

Headers: B="SHARES OUTSTANDING" | C="Shares" | D="Source"

| Row | B (Label) | C (Value/Formula) | D (Source) |
|-----|-----------|-------------------|------------|
| 5 | Pre-Offering Class A | [hardcoded, blue] | "424B4 p.XX" |
| 6 | Class B Outstanding | [hardcoded, blue] | "424B4 p.XX" |
| 7 | New Shares from This Offering | [hardcoded, blue] | "424B4 p.1" |
| 8 | Prior Warrant Shares (exercised) | [hardcoded, blue] | "424B4 p.XX" |
| 9 | Prior Warrants (remaining, unexercised) | [hardcoded, blue] | "424B4 p.XX" |
| 10 | (blank) | | |
| 11 | Post-Offering Float (before new warrants) | =SUM(C5,C7,C8) | formula |
| 12 | + Max Exploded Warrant Shares (this deal) | ='Breakeven Model'!C29 | cross-sheet |
| 13 | + Over-Allotment (if exercised) | ='Breakeven Model'!C34+'Breakeven Model'!C35 | cross-sheet |
| 14 | (blank) | | |
| 15 | **FULLY DILUTED TOTAL** | =C11+C6+C9+C12+C13+[other instruments] | yellow fill |

Adjust the fully diluted formula to include all instruments found in the cap table.

### Section B: Existing Instruments (Rows 17-30+)

Headers: B="EXISTING INSTRUMENTS" | C="Qty Outstanding" | D="Strike / Conversion" | E="Anti-Dilution Type" | F="Resets on This Deal?" | G="Risk Level"

For each instrument found in the filing, add a row:

```
Example rows:
Prior Warrants (Feb 2026) | 370,440 | $1.58 (post-reset) | Structural only | NO | LOW
Convertible Note (XYZ) | $2,000,000 | Floating (80% VWAP) | Full ratchet | YES | HIGH
S-8 Incentive Plan | 500,000 authorized | N/A | None | NO | LOW
Legacy Warrant Shares | 0 (fully exercised) | N/A | N/A | N/A | NONE
```

Color coding for Risk Level:
- **HIGH (RED fill FCE4EC)**: Instrument WILL reset/ratchet on this deal — creates additional dilution
- **MEDIUM (ORANGE fill FFF3E0)**: Instrument MAY reset depending on conditions
- **LOW (GREEN fill E8F5E9)**: Instrument does NOT reset, minimal risk
- **NONE (no fill)**: Fully exercised or expired

**Anti-dilution types to look for:**
- "Structural only" = adjusts for splits/dividends only → does NOT reset on new offerings
- "Weighted average" = adjusts for below-market issuances → DOES reset, but dilution is moderated
- "Full ratchet" = strike resets to lowest price in any new issuance → DOES reset, maximum dilution
- "Floating conversion" = conversion price tied to market VWAP → DOES reset continuously

### Section C: Nasdaq Delisting Timeline (Rows 33-48+)

Headers: B="NASDAQ DELISTING TIMELINE" | C="Date / Status" | D="Rule / Impact"

Chronological table of events and deadlines. Example:

```
16:1 Reverse Split Effective | 12/26/2025 | Triggers R/S disqualification thru 12/26/2026
Bid Price Deficiency Cured | 1/12/2026 | Regained $1.00 for 10 days
MVLS Deficiency Notice ($50M) | 10/3/2025 | 180-day cure → April 1, 2026
MVPHS Deficiency Notice ($15M) | 10/3/2025 | 180-day cure → April 1, 2026
This Offering Closes | ~2/27/2026 | XX M new shares + warrants
(blank)
IF STOCK ≤ $0.10 for 10 days: | ~Day 14 post-close | Rule 5810(c)(3)(A)(iii) — IMMEDIATE delisting
IF STOCK < $1.00 for 30 days: | NO cure period | Rule 5810(c)(3)(A)(iv) — Prior R/S trap
MVLS/MVPHS Cure Deadline | April 1, 2026 | XX days from offering close
Hearings Panel (if appealed) | ~June/July 2026 | 60-90 days post-determination
$5M MVLS Rule (if approved) | ~March 2026 | Immediate delisting, no cure (PENDING)
```

"IF STOCK" warning rows: light red fill (FCE4EC)

### Section D: Risk Summary Matrix (Rows 50-65+)

Headers: B="RISK FACTOR" | C="Severity (1-5)" | D="Probability" | E="Impact if Triggered" | F="Time Horizon" | G="Notes"

Standard risk factors to always assess:

| # | Risk Factor | How to Assess Severity |
|---|-------------|----------------------|
| 1 | Low Price Rule ($0.10) | 5 if post-offering price likely ≤$0.15; 3 if $0.15-0.30; 1 if >$0.30 |
| 2 | Reverse Split Trap | 5 if R/S in prior 12 months and stock already <$1; 1 if no R/S |
| 3 | MVLS/MVPHS Deadline | 5 if <30 days to deadline; 3 if 30-90 days; 1 if >90 days or N/A |
| 4 | Proposed $5M MVLS Rule | 4 if MVLS already <$5M; 2 if $5-10M; 1 if >$10M |
| 5 | Existing Instrument Resets | 5 if full ratchet converts exist; 3 if weighted avg; 1 if structural only |
| 6 | Lock-Up Expiry Pressure | 3 if insiders have large blocks; 1 if minimal insider float |
| 7 | Volume / Liquidity Risk | 5 if <100K avg daily volume; 3 if 100K-500K; 1 if >1M |
| 8 | Going Concern | 4 if going concern opinion exists; 1 if clean audit |
| 9 | HFCAA / PCAOB Risk | 3 if Chinese issuer with offshore auditor; 1 if US-based |
| 10 | Registration Effectiveness | 4 if not yet effective; 1 if already effective |

Severity color coding:
- 5: Dark red fill (D32F2F), white font
- 4: Red fill (E57373), white font
- 3: Orange fill (FFB74D)
- 2: Yellow fill (FFF176)
- 1: Green fill (81C784)

---

## Tab 4: "Hypothetical Quick Calc"

Simplified scenario tool (same as warrant-f1-analysis skill Tab 2):

```
G3: "Investment"          H3: ='Breakeven Model'!C10
G4: "Unit Price"          H4: ='Breakeven Model'!C6
G5: "Warrant Strike"      H5: =I5*H4     I5: 1 [blue, multiplier]
G6: "Cashless Multiplier" H6: ='Breakeven Model'!C20
G7: "Reset Price"         H7: =I7*H4     I7: 0.5 [blue, floor %]

G9:  "Shares"             H9:  =H3/H4
G10: "Warrant Shares"     H10: =((H9*H5)/H7)*H6

G12: "Common Exit"        H12: =(1+I12)*H9*H4     I12: -0.7 [blue, assumed loss %]
G13: "Warrant Exit"       H13: =((1+I13)*H4)*H10  I13: -0.93 [blue, assumed loss %]
G14: "PnL ($)"            H14: =H12+H13-H3
G15: "PnL (%)"            H15: =H14/H3

G17: "Break Even"         H17: =H3/(H9+H10)
```

---

## Cross-Sheet References

Tab 2 references Tab 1 for total shares and capital deployed.
Tab 3 references Tab 1 for exploded warrant shares and over-allotment.
Tab 4 references Tab 1 for investment, unit price, and multiplier.

Always use format: `='Tab Name'!CellRef`

---

## Post-Build Checklist

1. Run `python /mnt/skills/public/xlsx/scripts/recalc.py <file>` and fix any errors
2. Verify Tab 1 exploded shares = 424B4 stated total (cross-check row)
3. Verify breakeven discount is ~80% for standard 50%/2.0x deals (or calculate expected if floor binds)
4. Verify all existing instruments in Tab 3 Section B are accounted for
5. Verify all Nasdaq deadlines in Tab 3 Section C use correct dates from filings
6. Verify risk severity ratings in Tab 3 Section D are defensible
