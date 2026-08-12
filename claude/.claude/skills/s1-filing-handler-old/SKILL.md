---
name: s1-filing-handler-old
description: >
  S-1 and S-1/A filing extractor and redliner for Meteora's SPAC research.
  Given a filing with CIK, accession number, and filing type, extracts the full
  S-1 structure (all sections + SPAC-specific fields) using the extract-s1 MCP tool,
  or redlines an S-1/A amendment against its prior filing to surface only the changes.
  Use this skill whenever the user says "extract this S-1", "analyze this S-1/A",
  "redline the amendment", "pull S-1 fields", or provides an S-1 accession number.
---

# S-1 Filing Handler

Extracts and analyzes S-1 and S-1/A filings from SEC EDGAR using structured field extraction
and amendment redlining.

**Goal.** Given an S-1 filing, extract all standardized and SPAC-specific fields with minimal
token overhead. For amendments (S-1/A), surface only the impactful changes vs. the prior filing.

This skill uses the `extract-s1` MCP tool for efficient section extraction and `edgar-redline`
for amendment analysis.

---

## Extraction Workflow

### Step 1 — Identify the filing
From the user's input, extract: `cik` (or ticker), `accession` number, and `filing_type` (S-1 vs S-1/A).
If the user provides a URL or SafeLink, decode it to the raw sec.gov link.

### Step 2 — Determine fields to extract
**For S-1 (IPO):** Extract all fields via `extract-s1`.
- Default fields: use_of_proceeds, cap_table, dilution, management, principal_stockholders
- Standard fields: risk_factors
- SPAC fields (if applicable): trust_account_terms, warrant_terms, rights_terms, 
  business_combination_deadline, offering_summary, founder_shares, private_placement, 
  admin_agreement, underwriting, lock_up

**For S-1/A (Amendment):** Extract the key changed sections.
Call `edgar-redline` to surface the impactful changes only, then extract only those sections
via `extract-s1` for detailed context.

### Step 3 — Call extract-s1
```
extract-s1(
  cik=<CIK>,
  filing_date=<YYYY-MM-DD>,
  fields=["trust_account_terms","warrant_terms","business_combination_deadline","management",
          "principal_stockholders","use_of_proceeds","cap_table","dilution"]
)
```

Returns JSON with each field containing the extracted section text. For SPAC IPOs, include
SPAC-specific fields. Omit `filing_date` to get the most recent S-1 or S-1/A.

### Step 4 — For amendments (S-1/A), redline vs prior filing
Call `edgar-redline` with the current accession and prior filing accession.
Returns a summary of substantive changes. Extract only the changed sections from both filings
for side-by-side comparison.

### Step 5 — Format and display results

**For new S-1:** Display the full extraction under a one-line header with ticker, filing type, date, CIK, and accession.

**For S-1/A:** Display only the changed sections with side-by-side before/after comparison.

Display is formatted for copy/paste into email:
- Clean section headers
- Field values organized by category  
- SPAC-specific fields clearly marked
- For amendments: changes highlighted
- No auto-sending — user controls distribution

---

## Tools

- **`extract-s1(cik, filing_date, fields)`** — Meteora MCP tool. Extracts named sections
  from S-1/S-1/A with no LLM processing. Fast, deterministic, low token overhead.
- **`edgar-redline(accession_current, accession_prior)`** — Meteora MCP tool. Generates
  a summary of changes between two filing versions.
- **`edgar-filing-index(accession)`** — SEC EDGAR index. Lists all documents in the filing.
- **`edgar-filing-text(accession, doc_seq)`** — Raw filing text for fallback analysis.
- **`spac-details(ticker, cik)`** — SPAC-specific metadata (tickers, dates, parties).

---

## Notes

- **No dedup, no state.** This skill is stateless — extract on each invocation.
- **SPAC-specific fields.** Include trust_account_terms, warrant_terms, founder_shares,
  etc. only for SPAC IPOs, not for traditional S-1s.
- **Ticker resolution.** Use the base common ticker (strip trailing U/W/R/RT/WS).
  Confirm with `spac-details` if needed.
- **Amendments.** For S-1/A, always compare against the immediately prior version,
  not the original S-1, to catch iterative changes.
