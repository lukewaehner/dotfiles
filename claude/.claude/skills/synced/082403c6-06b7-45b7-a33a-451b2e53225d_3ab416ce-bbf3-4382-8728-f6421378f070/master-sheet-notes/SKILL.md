---
name: master-sheet-notes
description: >
  Generate a short, copy-pasteable Notes column entry for the Meteora SPAC master tracker spreadsheet. Trigger whenever the user asks to "update notes", "create a note for the sheet", "master sheet note", "notes column", "copy-paste note for [ticker]", "tracker note", or any request to produce a concise notes string for a SPAC position. Also trigger proactively at the end of any in-depth SPAC analysis session when the user references updating the spreadsheet or master sheet. Produces a single dense text string covering unit structure, PIPE terms, S-4/F-4 status, common stock price range and MoM, plus warrant/right price range since deal/IPO with prior month close and MoM change.
---

# Master Sheet Notes

Generates a single copy-pasteable Notes column entry for the Meteora SPAC tracker. The output is a tightly packed, plain-text string — no bullet points, no headers, no markdown formatting inside the note itself (so it pastes cleanly into Excel).

---

## Workflow

Run all tool calls in parallel where possible.

### Step 1 — Pull core data (parallel)

1. **`spac-details`** (by ticker) → get: `deal_announced`, `rights_adjustment`, `warrant_ticker`, `rights_ticker`, `stage`, `max_deadline`, `ipo_date`
2. **`get-price` (historical, common)** → SPAC common ticker, `start_date = ipo_date (or deal_announced if in-deal)`, `end_date = today`, `fields = ["PX_LAST"]` — full common price range
3. **`get-price` (historical, common)** → SPAC common ticker, `start_date = first day of prior month`, `end_date = last day of prior month`, `fields = ["PX_LAST"]` — prior month-end close for common
4. **`get-price` (spot, common)** → current price of the SPAC common ticker
5. **`get-price` (historical, W/R)** → warrant or rights ticker, `start_date = ipo_date (or deal_announced if in-deal)`, `end_date = today`, `fields = ["PX_LAST"]` — full W/R price range
6. **`get-price` (historical, W/R)** → same W/R ticker, `start_date = first day of prior month`, `end_date = last day of prior month`, `fields = ["PX_LAST"]` — prior month-end close for W/R
7. **`get-price` (spot, W/R)** → current price of the warrant/right ticker
8. **`edgar-filings`** → SPAC ticker, form_type `8-K`, limit 5, `include_exhibits: true` — to find the BCA announcement 8-K with PIPE terms
9. **`edgar-filings`** → SPAC ticker, all form types, limit 20 — to check for any S-4, F-4, or DRS filing

Use `tickers` batch mode where possible to reduce the number of calls (e.g., batch the two spot prices into one call).

### Step 2 — Check for confidential F-4 under PubCo CIK

If no public S-4/F-4 found under SPAC ticker:
- Note that for Cayman/Jersey PubCo structures, the F-4 files under the PubCo's CIK, not the SPAC's. A confidential DRS is invisible on EDGAR.
- If the PubCo is a foreign private issuer (Cayman, Cayman Islands exempted company, etc.), state: "no public filing; confidential DRS cannot be ruled out (FPI eligible)"
- If there IS a public S-4/F-4, state the form type, filing date, and amendment count

### Step 3 — Parse PIPE terms from the BCA 8-K

From the BCA announcement 8-K text, extract:
- Total PIPE size at announcement
- Any subsequent upsizing (with date)
- Pre-funded amount (if any, and whether funded at signing or later)
- PIPE structure: equity vs. preferred; if preferred: dividend rate, conversion price, any floor/reset, put/call terms
- Whether MCC exists and if PIPE satisfies it

If PIPE detail is unavailable from the 8-K text alone, note what is known and flag for further review.

### Step 4 — Derive unit structure line

From `spac-details`:
- If `warrant_ticker` is populated and `rights_adjustment` = 0: **U = S + W/[fraction]** (check IPO prospectus for warrant fraction; default assume 1/4 if unknown)
- If `rights_ticker` is populated and `warrant_ticker` = 0: **U = S + R(1/[rights_adjustment denominator])** — e.g., rights_adjustment = 0.1 → R(1/10)
- If both: note both
- If neither: "no warrants/rights"

### Step 5 — Calculate price statistics

Compute stats for **both** common and warrant/right tickers separately:

**Common stock:**
- **Range since IPO (or deal)**: `min(PX_LAST)` → `max(PX_LAST)` (format to 2 decimal places)
- **Prior month close**: last available PX_LAST in the prior month
- **Current price**: spot price
- **MoM change**: `(current - prior_month_close) / prior_month_close` as % — state "up X%" or "dn X%" or "flat"

**Warrants/Rights** (if they exist):
- **Range since IPO (or deal)**: `min(PX_LAST)` → `max(PX_LAST)` (format to 2 decimal places)
- **Prior month close**: last available PX_LAST in the prior month
- **Current price**: spot price
- **MoM change**: `(current - prior_month_close) / prior_month_close` as % — state "up X%" or "dn X%"

---

## Output Format

Produce a single text string. No line breaks inside the note. Use `|` as section separator, semicolons within sections. Keep abbreviations tight.

```
**[SPAC COMMON TICKER]** (as of [M/D/YY]) | U = S + [structure]. [Deal/pre-deal context]. [PIPE terms if in-deal]. [F-4/S-4 status if in-deal]. [Sponsor/mgmt color if notable]. Common range since IPO/deal ([date]): $[low]–$[high]; [Prior month abbrev] close $[px] → [today] $[px] ([MoM]). W range since IPO/deal: $[low]–$[high]; [Prior month abbrev] close $[px] → [today] $[px] ([MoM]).
```

The note always leads with the **common stock ticker** (e.g., RTAC, IPCA), not the warrant or rights ticker. Both common and W/R price sections are included — common first, then warrants/rights.

### Format rules
- Dollar amounts: use M suffix (e.g., $83.5M), round to 1 decimal
- Dates: use M/D/YY format (e.g., 3/19/26) or Mon-YY for month references (e.g., Feb close)
- Percentages: round to nearest whole number (e.g., "dn 3% MoM")
- "No MCC" or "MCC: $[X]M" (state whether PIPE satisfies it)
- For F-4 status, use one of:
  - "no public filing; confidential DRS cannot be ruled out (FPI eligible)"
  - "F-4 filed [date], [N] amendments" 
  - "S-4 filed [date], [N] amendments"
  - "F-4 public [date]; [amendment count] amds"
- Keep the whole note under ~600 characters for clean Excel paste (longer than before because it now includes both common and W/R ranges)

---

## Example Outputs

**In-deal with rights (no warrants):**
```
**IPCA** (as of 3/19/26) | U = S + R(1/10), no warrants. PIPE: $83.5M total (upsized 3/19/26 from $63.5M at signing); >$35M pre-funded into target pre-close. Series A Pref: 10%/12% PIK div, $12.00 cvt px, $5.00 floor (6-mo VWAP reset), 5-yr put, 150%→100% call schedule. No MCC. F-4/S-4: no public filing; confidential DRS cannot be ruled out (FPI eligible). Common range since deal (8/25/25): $10.18–$10.85; Feb close $10.42 → 3/19/26 $10.38 (flat MoM). R range since deal: $0.28–$0.49; Feb close $0.35 → 3/19/26 $0.34 (dn ~3% MoM, despite +21% pop today off $0.28 low yesterday).
```

**Pre-deal with warrants:**
```
**RTAC** (as of 4/7/26) | U = S + W/2, no rights. Pre-deal, no BCA. $210M IPO 5/15/25; Clear Street. KY domicile; deadline 11/16/27. Trust $10.37. Sponsor: Swider (CEO, 50% econ) + Nunes (Chairman, 50% econ); same team as DWAC/DJT. Focus: crypto/blockchain, data security, dual-use tech. No S-4/F-4 filed. Common range since IPO: $10.28–$12.50; Mar close $10.28 → 4/7 $10.29 (flat MoM). W range since IPO: $0.46–$2.54; Mar close $0.46 → 4/7 $0.60 (up 30% MoM).
```

---

## Key Edge Cases

- **Pre-deal SPACs (no BCA yet)**: Output unit structure and price stats only; omit PIPE and F-4 sections. State "pre-deal, no BCA."
- **No warrants or rights**: Note "no warrants/rights; commons only."
- **PIPE in commons (not preferred)**: Describe as "PIPE: $[X]M equity at $10.00/share" or as described in the 8-K
- **Multiple PIPE tranches**: List each tranche with size and close timing (e.g., "Tranche 1: $X at signing; Tranche 2: $Y at close")
- **MCC that PIPE satisfies regardless of redemptions**: Note "MCC satisfied by PIPE regardless of redemptions"
- **Rights/warrants never traded**: Note "no secondary market data available" for the price range

---

## Tools Required

- `spac-details` (MeteoraMCP)
- `get-price` (MeteoraMCP, historical mode)
- `edgar-filings` (MeteoraMCP)
- `edgar-filing-text` (MeteoraMCP, if PIPE terms need deeper extraction from 8-K exhibit)
