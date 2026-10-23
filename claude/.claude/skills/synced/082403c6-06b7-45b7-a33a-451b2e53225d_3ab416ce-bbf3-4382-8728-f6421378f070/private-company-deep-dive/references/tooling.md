# Research Tooling Reference — MCP Tool Sequencing Protocol

## GOVERNING PRINCIPLE

MCP tools provide structured, high-fidelity data that web search cannot replicate. Pinecone semantic search surfaces proprietary VDR materials; EDGAR provides the authoritative SEC filing record. External web search is always the last resort. Any finding from web search that contradicts Pinecone VDR or EDGAR filings must be flagged `[CONFLICTING DATA]` with both sources cited and a note on which is more likely to be authoritative.

---

## MANDATORY TOOL SEQUENCE

Execute in this order. Deviation is only permitted on connectivity failure — document the failure and substitute the next available tool.

```
Step 1:  pinecone-stats           → confirm index connectivity and document volume
Step 2:  list-documents           → enumerate available VDR materials
Step 3:  semantic-search          → filtered queries across 4 categories
Step 4:  read-document            → full retrieval of highest-relevance documents
Step 5:  edgar-ownership-search   → executive-level and company-level ownership filings
Step 6:  edgar-filings            → company and executive SEC filing history
Step 7:  edgar-filing-index       → enumerate exhibits within relevant filings
Step 8:  edgar-filing-text        → full text extraction of material sections
Step 9:  edgar-company-facts      → structured XBRL financial data for prior employers
Step 10: web search / external    → only after all MCP tools exhausted
```

---

## TOOL SET 1 — PINECONE SEMANTIC SEARCH MCP

The Pinecone vector database contains Meteora's proprietary VDR document library — pitch decks, financial models, management presentations, due diligence materials, and prior research reports. Always the first research call made.

### `pinecone-stats` — Verify Index Connectivity

Run as the first Pinecone call to confirm the index is live and assess content volume.

- If the index returns zero vectors or an error: do NOT proceed to filtered search. Escalate the connectivity issue and fall back to Google Drive search immediately. Document the failure.
- Use document count to calibrate expectations:
  - 1,000+ vectors for a target company → rich VDR, expect substantive findings
  - Fewer than 50 vectors → limited proprietary material; treat as a diligence flag

### `list-documents` — Enumerate Available Documents

Run before executing semantic queries to identify what documents are present. Prevents blind searching.

- Filter or sort by document name to identify management-related materials. Look for filenames containing: `team`, `management`, `bio`, `org`, `board`, `governance`, `cap table`, `executive`
- Cross-reference the document list against the expected VDR folder structure for the target company
- **Gaps in expected document types are themselves a finding**: no audited financials, no cap table, no management bios → document as a diligence observation

### `semantic-search` — Execute Targeted Queries

Primary retrieval tool. Apply the standard metadata filter to constrain results to the target company before falling back to unfiltered search.

**Standard metadata filter pattern:**
```json
{
  "$or": [
    {"primary_company": {"$eq": "[Company Name]"}},
    {"primary_ticker": {"$eq": "[TICKER]"}},
    {"folder_ticker_1": {"$eq": "[TICKER]"}}
  ]
}
```

**Execute all queries below in sequence, applying the metadata filter to each:**

#### Category A — Management & Governance
```
"executive team biography background experience"
"CEO founder history prior companies"
"board of directors independent members governance"
"management compensation equity ownership alignment"
"organizational structure reporting lines"
"key person risk departure succession"
```

#### Category B — Financial Quality & Capital Structure
```
"revenue ARR bookings recognized deferred"
"gross margin unit economics CAC payback"
"funding round cap table liquidation preference"
"convertible note SAFE warrant coverage anti-dilution"
"burn rate runway cash position bridge"
"audit PCAOB going concern financial statements"
```

#### Category C — Risk & Red Flags
```
"litigation dispute legal proceedings lawsuit"
"regulatory compliance sanctions export control"
"customer concentration revenue dependency"
"related party transaction conflict of interest"
"employee departure turnover culture"
```

#### Category D — SPAC / IPO Readiness
```
"SPAC readiness IPO timeline public company"
"PCAOB audit auditor financial restatement"
"registration statement S-1 SEC filing"
"lock-up agreement insider shares founder equity"
```

**Fallback protocol:**
- If filtered search returns fewer than 3 results for any category → re-run those queries without the metadata filter as an unfiltered semantic search across the full index
- Document which queries returned null results under filtered search — limited proprietary materials in the VDR is itself a diligence flag
- Document both the filtered attempt and the unfiltered fallback in the Research Tool Log

### `read-document` — Full Document Retrieval

When `semantic-search` or `list-documents` returns a highly relevant document, use `read-document` to retrieve the full content rather than relying on the truncated snippet.

**Always use for documents that appear to contain:**
- Executive bios or management team profiles
- Board materials or governance documents
- Cap table details or equity schedules
- Audited financial statements
- Investor presentations with management section

Cross-reference full document content against external sources — discrepancies between internal VDR materials and external press releases are a significant finding.

---

## TOOL SET 2 — SEC EDGAR MCP

The EDGAR MCP provides direct programmatic access to SEC filings. Use to surface any regulatory footprint the target company or its executives have left in the public record — as counterparties, reporting persons, registrants, or named individuals.

### `edgar-ownership-search` — Ownership Filings (SC 13D, SC 13G, Forms 3/4/5)

Run this first among EDGAR tools — it is the highest-signal tool for the Management Deep Dive.

**Search by individual executive name:**
- Identifies all entities through which the individual holds reportable positions
- Frequently reveals undisclosed affiliated entities, family office vehicles, or cross-investments with counterparties
- Run for every named C-suite executive and board member

**Search by company name:**
- Identifies all reporting owners (13D/13G filers)
- Reveals who has taken a significant position and whether activist, strategic, or related-party investors are present

**SPAC-specific use:**
- Form 4 and Form 3 filings reveal insider transaction timing
- Executives selling immediately after lock-up expiry = negative signal
- Executives buying in the open market post-merger = positive signal
- Flag discrepancies between ownership in registration statements and subsequent Form 4 filings — timing gaps can indicate undisclosed transfers

### `edgar-filings` — List Filings by Ticker or CIK

Use for any company with a public market presence or named as a counterparty in a SPAC transaction.

- Input: company ticker or CIK number
- Output: chronological list of filing types and accession numbers

**Primary use:** Confirm whether the target company has ever filed with the SEC directly (S-1, S-4, 8-K, 10-K, proxy statement) or appears as a named entity in a counterparty filing.

**For Management Deep Dive:** Run this search against the names of key executives — individuals with financial services backgrounds, SPAC involvement, or prior public company affiliations will frequently appear as reporting persons or named parties.

**Flag as unexpected for a private company:**
- S-1 withdrawal (indicates failed prior IPO attempt)
- 8-K disclosure by a SPAC counterparty referencing the target
- Prior proxy statement disclosures of the executive as a named party in a dispute

### `edgar-filing-index` — Enumerate Documents Within a Filing

Once a relevant filing is identified via `edgar-filings`, use this tool to pull the complete document index for that accession number. Reveals all exhibits, amendments, and supplemental materials.

**High-value exhibits to identify:**
| Exhibit | Contents |
|---------|---------|
| Exhibit 10.1 | Material contracts |
| Exhibit 21 | Subsidiary list |
| Exhibit 99.1 | Investor presentations |
| Proxy Statement | Executive compensation, beneficial ownership, independent director disclosures |
| S-4 / Registration Statement | Management bios, risk factors, related-party transactions, financials |

### `edgar-filing-text` — Extract Full Text of Filing or Exhibit

Primary tool for extracting substantive content from any filing identified via `edgar-filing-index`.

**Always extract these sections for any S-1, S-4, 10-K, or proxy statement touching the target company or its executives:**

| Section | What to Look For |
|---------|-----------------|
| **Legal Proceedings** | Disclosed litigation, regulatory actions, arbitration — both company-level and individual-level |
| **Management** | Official bios, employment history, board committee memberships |
| **Executive Compensation** | Cash vs. equity mix; sign-on payments; severance arrangements |
| **Certain Relationships and Related Party Transactions** | Undisclosed conflicts, loans to executives, related-party contracts |
| **Risk Factors** | Most candid language available — surfaces customer concentration, regulatory uncertainty, going-concern conditions that marketing materials omit |
| **Security Ownership** | Beneficial ownership table — cross-reference against `edgar-ownership-search` results |

**Amendment comparison technique:**
- Pull Risk Factors from Amendment No. 1 and compare to Amendment No. 3 of the same S-1
- Language that was softened, added, or removed under counsel pressure reveals what the company was required to disclose
- Changes to the Legal Proceedings section across amendments are particularly significant

### `edgar-company-facts` — Structured XBRL Financial Data

Use to extract structured financial facts for:
1. Any public company being used as a valuation comparable
2. Any prior public company employer of a key executive

**For Management Deep Dive use:**
- Verify the financial performance of prior companies where executives held leadership roles
- Did the company grow revenue, maintain margins, and generate shareholder value during their tenure, or did it deteriorate?
- Cross-reference reported financials against the executive's claimed achievements in press releases and LinkedIn bios
- **Discrepancies between claimed outcomes and filed financials are a significant red flag** — flag as `[CONFLICTING DATA]`

---

## RESEARCH TOOL LOG TEMPLATE

Complete this table as tools are executed. Include in the final output.

| Step | Tool | Input / Query | Result Summary | Null Finding? |
|------|------|--------------|----------------|---------------|
| 1 | pinecone-stats | — | [vectors found / error] | Y/N |
| 2 | list-documents | — | [documents enumerated] | Y/N |
| 3a | semantic-search (filtered) | Category A queries | [hits / no hits per query] | Y/N |
| 3b | semantic-search (filtered) | Category B queries | [hits / no hits per query] | Y/N |
| 3c | semantic-search (filtered) | Category C queries | [hits / no hits per query] | Y/N |
| 3d | semantic-search (filtered) | Category D queries | [hits / no hits per query] | Y/N |
| 3e | semantic-search (unfiltered fallback) | [queries that returned null] | [hits / no hits] | Y/N |
| 4 | read-document | [document IDs] | [content summary] | Y/N |
| 5 | edgar-ownership-search | [exec names / company name] | [filings found] | Y/N |
| 6 | edgar-filings | [ticker / CIK / exec names] | [filing types found] | Y/N |
| 7 | edgar-filing-index | [accession numbers] | [exhibits identified] | Y/N |
| 8 | edgar-filing-text | [exhibit / section] | [material findings] | Y/N |
| 9 | edgar-company-facts | [prior employer tickers] | [financial data extracted] | Y/N |
| 10 | web search | [queries] | [findings] | Y/N |

**Null findings are valid outputs.** A clean search result is not a clean bill of health. Document every database searched and every query that returned no results — a null result is not the same as no risk.

---

## CONFLICT RESOLUTION PROTOCOL

When findings from different sources conflict, apply the following priority hierarchy:

1. **Audited financial statements** (via `edgar-filing-text` or `edgar-company-facts`) — highest authority for financial claims
2. **SEC filings** (proxy statements, S-1/S-4 legal proceedings sections) — highest authority for disclosed legal matters and ownership
3. **Pinecone VDR materials** — high authority for internal company representations; flag if contradicted by SEC filings
4. **Press releases and company-issued materials** — treat as company-asserted; flag `[UNVERIFIED]` unless corroborated
5. **Web search / trade press** — corroborating or contradicting context; lowest authority for factual claims

Never silently resolve a conflict. Always document the discrepancy, cite both sources, and note which is more likely authoritative and why.
