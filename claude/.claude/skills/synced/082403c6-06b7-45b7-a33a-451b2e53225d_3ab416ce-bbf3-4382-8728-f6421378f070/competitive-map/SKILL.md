---
name: competitive-map
description: Build a recursive competitive landscape map from SEC 10-K filings. Use this skill whenever the user asks to map competitors, build a competitive landscape, analyze competition sections across filings, find competitive overlap between companies, or asks "who competes with X" using SEC data. Also trigger when the user mentions competitive analysis from 10-Ks, competitor mapping, or recursive competitor discovery. Works for any pair or set of public companies by extracting named competitors from their 10-K Competition sections and recursively following each competitor's own 10-K disclosures to build a full network graph.
---

# Competitive Landscape Map from 10-K Filings

This skill extracts named competitors from the "Competition" section of companies' 10-K annual reports filed with the SEC, then recursively follows each competitor's own 10-K filings to build a comprehensive competitive overlap map.

## Workflow

### Step 1: Identify the Starting Companies

The user provides one or more ticker symbols (the "seed" companies). Default to 2 companies (a "pair") but support any number of seeds.

### Step 2: For Each Seed Company — Pull the Most Recent 3 10-Ks

Use the EDGAR MCP tools:

```
edgar-filings(ticker=TICKER, form_type="10-K", limit=3)
```

This returns the 3 most recent 10-K filings with accession numbers and document URLs.

### Step 3: For Each 10-K — Find the Competition Section via TOC

Use the `edgar-filing-text` tool with `summary=true` to get the table of contents with subsection offsets:

```
edgar-filing-text(url=DOCUMENT_URL, summary=true)
```

Scan the returned sections and subsections for a title matching "Competition" (case-insensitive, may also appear as "Competitive Environment", "Competitive Landscape", or similar). Record the `start` offset and `chars` size.

**Important edge cases:**
- The Competition section may be a subsection nested inside "Item 1. Business" or inside a broader "GLOSSARY" or "WHERE YOU CAN FIND MORE INFORMATION" section. Always search recursively through all subsections.
- Some filings may not have a standalone Competition section. In that case, try searching in "Item 1A. Risk Factors" for competition-related subsections, or fall back to extracting the full Item 1 Business section and searching for competitor names within it.
- **If `summary=true` fails for a given filing URL, try ONE fallback:** `edgar-filing-text(accession_number=..., ticker=..., summary=true)`. If that also fails, **immediately skip the filing** and move on. Do not retry, do not try alternative approaches, do not use `web_fetch`. Some older or large filings are simply inaccessible via the MCP due to size/parsing limitations — this is a known issue. Log which filing was skipped and continue with the filings that work. Having 2 out of 3 10-Ks is perfectly acceptable.

### Step 4: Extract the Competition Section Text

```
edgar-filing-text(url=DOCUMENT_URL, offset=START, max_chars=CHARS)
```

This returns the raw HTML of the Competition section.

### Step 5: Parse Named Competitors from the Text

Strip HTML tags and extract company names mentioned as competitors. Look for patterns like:
- "companies such as X, Y, and Z"
- "competitors include X"
- "X is/are pursuing..."
- Proper nouns followed by technology/approach descriptions
- Known quantum/tech company names

Build a structured list per filing year:
```
{
  "ticker": "IONQ",
  "fiscal_year": "2025",
  "competitors_named": ["Google", "IBM", "Rigetti Computing", "PsiQuantum", "Xanadu", "Quantinuum", "Alpine Quantum Technologies", "D-Wave", "QuEra"]
}
```

### Step 6: Determine Which Competitors Are Public Companies

For each unique competitor name found across all filings, determine if they are publicly traded. Use the following approach:
- Known mappings: Google → GOOGL, IBM → IBM, Rigetti Computing → RGTI, D-Wave → QBTS, Quantinuum → check if public
- For unknown names, use `web_search` to find their ticker symbol
- Private companies (e.g., PsiQuantum, Xanadu, Alpine Quantum Technologies, QuEra) cannot be recursed into via 10-K — note them as "private" in the map

### Step 7: Recursively Extract Competition Sections for Public Competitors

For each public competitor identified, repeat Steps 2–5 (pull their last 3 10-Ks, find Competition section, extract named competitors).

**Recursion depth:** Default to depth=2 (seed companies → their competitors → competitors' competitors). The user can request deeper recursion but warn that it grows exponentially.

**Cycle detection:** Track all tickers already processed to avoid infinite loops. If Company A names Company B and Company B names Company A, don't re-process A.

### Step 8: Build the Competitive Overlap Map

Produce a structured output showing:

1. **Node list** — Every company encountered, with metadata:
   - Ticker (or "PRIVATE" if not public)
   - Full name
   - Technology approach (if mentioned — e.g., "superconducting", "trapped ion", "photonic", "neutral atom", "quantum annealing")
   - Depth at which discovered (0 = seed, 1 = first-order competitor, 2 = second-order)

2. **Edge list** — Every "names as competitor" relationship:
   - Source ticker → Target company
   - Fiscal year(s) in which the relationship was disclosed
   - Direction (who named whom)

3. **Overlap analysis** — Companies that appear in multiple competitors' filings:
   - Which companies are most frequently named across the network
   - Bidirectional relationships (A names B AND B names A)
   - Companies that appear across all seed companies' filings (common competitors)
   - New competitors that appeared only in recent filings vs. those present across all years
   - Competitors that were dropped from more recent filings

### Step 9: Present Results

Present a **Competitive Landscape Table** as a markdown artifact (.md file). One row per unique competitor, with these columns:

| Column | Description |
|---|---|
| **Competitor** | Company name (ticker if public, "Private" if not) |
| **Named By** | Which seed/network companies list this competitor in their 10-K filings (comma-separated tickers) |
| **Names** | Which seed/network companies this competitor lists in its own 10-K filings (comma-separated tickers; blank if private or no 10-K available) |
| **Description** | One-line summary of what the company does / its competitive angle, drawn from the filing text |

Sort by number of "Named By" entries descending (most-cited competitors first).

## CRITICAL: Always Use MCP Tools — Never Fetch SEC.gov Directly

**Do NOT use `web_fetch` on SEC.gov URLs.** Direct fetches from sec.gov will fail. Always use the EDGAR MCP tools (`edgar-filings`, `edgar-filing-text`, `edgar-filing-index`).

**Skip inaccessible filings fast.** Some older or large filings fail on the MCP due to size/parsing limitations — this is a known issue. The rule is simple:
1. Try `edgar-filing-text(url=..., summary=true)`
2. If that fails, try `edgar-filing-text(accession_number=..., ticker=..., summary=true)`
3. If that also fails, **skip it immediately and move on**. No further retries.

Having 2 out of 3 10-Ks is fine. Having 1 out of 3 is still usable. Note skipped filings in the output.

The only acceptable use of `web_search` is to look up whether a named competitor is publicly traded and find their ticker symbol.

## Error Handling

- If a 10-K filing cannot be accessed after the two MCP attempts above, skip it and note the gap
- If no Competition section is found in a filing's TOC, try broader searches (Item 1, Risk Factors)
- If a competitor cannot be identified as public or private, mark as "UNKNOWN" and note in output
- Some older or smaller company filings may have minimal or no Competition section — note this

## Key MCP Tools Used

- `edgar-filings` — List recent 10-K filings for a ticker
- `edgar-filing-text` with `summary=true` — Get TOC with subsection offsets
- `edgar-filing-text` with `offset` + `max_chars` — Extract specific section text
- `web_search` — Look up ticker symbols for named competitors

## Tips for Better Results

- The Competition section in 10-Ks is typically found as a subsection within Item 1 (Business). It's rarely a top-level section.
- Company names in filings are often formal (e.g., "Rigetti Computing, Inc." not "Rigetti"). Strip legal suffixes for matching.
- Some companies describe competitors generically ("large technology companies") without naming them. Only extract explicitly named entities.
- The same competitor may be named differently across filings (e.g., "Honeywell Quantum Solutions" vs. "Quantinuum" after the spin-off). Resolve aliases.
- For very large companies (Google, IBM, Microsoft), their 10-K Competition sections will cover many business lines. Try to identify the quantum-specific or industry-specific subsection rather than ingesting the entire Competition section.
