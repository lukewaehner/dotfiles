---
name: new-deal-ml
description: Fast fact extraction for a merger-arb deal, in two modes. NEW DEAL - given an 8-K / merger-agreement link, an EDGAR accession, or a target ticker, pull the announcement-day fields the deal-close model needs, ready to paste into New Deals.xlsx. MILESTONE UPDATE - when asked for milestones / an update on a deal already in the sheet, pull the milestones that have happened since (and any extended outside date) as the text for the "Milestones so far" column. Extraction only - it does not run the model, write files, update dashboards or compare to brokers.
---

# new-deal-ml: extract the model's inputs, nothing else

## Two modes - pick from the request
| Mode | When | What you return |
|---|---|---|
| **A. New deal** | a new 8-K / merger agreement / ticker | columns 1–20 of `New Deals.xlsx` (announcement-day facts) |
| **B. Milestone update** | "milestones", "update", "what has happened on X", or a deal already in the sheet | column 22 "Milestones so far" (+ column 23 if the outside date was extended) |

If the request is ambiguous, do mode A for a deal announced in the last few days and mode B otherwise, and say which you did.

**Scope (both modes):** read the filings, extract, show the user. Do NOT run Python or the model, do NOT write or edit any project file, do NOT update dashboards, do NOT compare to brokers or send anything. The user pastes the result into `New Deals.xlsx` and runs the forecast themselves (the sheet keeps the day-one forecast and adds a "model now" re-prediction once milestones are entered).

**Rules:** read SEC filings only through the firm's EDGAR tools or sec.gov with User-Agent `MeteoraCapital-Research/1.0`; never put an email address or personal data in any request. Never guess: if something is not in the documents, leave it blank and say why.

---

## Mode A: new deal (announcement-day facts)
Every field is what was public **on announcement day**; later news never goes into columns 1–20.

**Documents:** from the filing folder of the announcement 8-K: Item 1.01 of the 8-K, EX-99.1 (press release), EX-2.1 (merger agreement). If only a ticker is given, take its latest 8-K with Item 1.01. Search the text for the fields rather than reading it all.

| # | Column | Where to find it | Format |
|---|---|---|---|
| 1 | Key | — | `TARGETTICKER-ACQUIRERSHORT`, e.g. `CCC-GTCR` |
| 2 | Target | 8-K | company name |
| 3 | Target ticker | 8-K cover | e.g. `CCC` |
| 4 | Acquirer | 8-K 1.01 | buyer name (sponsor / parent) |
| 5 | Acquirer ticker | — | blank if private |
| 6 | Announced | press-release dateline | `YYYY-MM-DD` (the PR date, not the signing date) |
| 7 | Guidance (verbatim) | PR "expected to close …" | exact words, e.g. `first quarter of 2027`; blank if none |
| 8 | Consideration type | 8-K 1.01 | one of: Cash Merger, Cash Tender, Stock Exchange, Cash & Stock Exchange, Stock Tender |
| 9 | Consideration terms | 8-K 1.01 | e.g. `$7.75 per share in cash` |
| 10 | Conditions | EX-2.1 "Conditions to …" article | comma-separated names from this list: `SH Approval <TICKER>` (plus the acquirer's if it votes), `HSR`, `EC Antitrust`, `China SAMR`, `UK CMA`, `CFIUS`, `Competition Canada`, `Investment Canada`, `<Country> Antitrust`, `Foreign Antitrust` (approvals named only in a non-public schedule), `<Country> Foreign Investment`, `S-4 Review` / `F-4 Review` (stock deals), `Proxy Review` (cash merger with a vote), `Minimum Tender`, `13E-3`, `Information Statement` (written consent), `Federal Reserve` / `OCC` / `FDIC`, `State Insurance DOI`, `FCC`, `FERC`, `State PUC`, `Gaming`, `Health Regulators`, `Court Approval`, `Financing` |
| 11 | Outside date | EX-2.1 termination section ("Outside / End / Termination Date") | INITIAL date, `YYYY-MM-DD` |
| 12 | Outside date auto-extends? | same section | Yes / No |
| 13 | Financing condition? | 8-K / EX-2.1 | Yes / No |
| 14 | Marketing period? | EX-2.1 (search "Marketing Period") | Yes / No |
| 15 | Go-shop? | EX-2.1 (search "Go-Shop", "Window Shop") | Yes / No |
| 16 | Industry | judgement | one of: Airlines, Apparel, Automotive, Banks, Biotech, Cable TV, Casinos, Chemicals, Communication, Construction, Consumer, Containers, Defense, Electrical, Entertainment, Financial, Food, Furnishings, Hardware, Healthcare, Industrial, Insurance, Internet, Lodging, Medical, Mining, Office, Oil, Oilfield, Packaging, Paper, Pharmaceuticals, Pipelines, Publishing, REITs, Radio, Railroads, Recreation, Retail, Semiconductors, Services, Software, Television, Trucking, Utilities, Waste, Wireless, Wireline |
| 17 | Jurisdiction | 8-K cover | state of incorporation, e.g. `DE` |
| 18 | Buyer type | — | Sponsor (PE / infrastructure fund) or Strategic |
| 19 | Deal value ($M) | PR equity value; if only enterprise value is given, shares outstanding (latest 10-Q cover) × offer price | number |
| 20 | Target market cap ($M) | Bloomberg `CUR_MKT_CAP`, last close strictly before announcement | number, or blank if Bloomberg is unavailable (never copy the deal value here) |
| 21 | Add to dashboard? | — | leave for the user (Yes/No) |

**Output, mode A:**
1. A table: column, value, and the source line it came from (filing + section, or a short quote).
2. One tab-separated line with columns 1–20 in order, in a code block, ready to paste into row 3+ of `New Deals.xlsx`.
3. Two or three bullets of timing notes that are not model inputs but matter to the desk (termination fees, extension terms, marketing-period blackout dates, 13E-3, vote timing). Flag any field you left blank or had to judge.

---

## Mode B: milestone update (deal already in the sheet)
**Documents:** what was filed **after** the announcement: 8-Ks (Items 8.01 / 5.07), 425s, DEFM14A / S-4 "Regulatory Approvals" section, SC TO-T/A, press releases, and the FTC early-termination list.

Record only milestones that have **happened**, each with its true date (the event date, not the filing date when they differ). Use exactly these names (they are what the model reads; the Help sheet of New Deals.xlsx lists them too):

| Name | Means |
|---|---|
| `HSR ET` | HSR early termination granted |
| `HSR Expired` | HSR waiting period expired |
| `Second Request Issued` | DOJ / FTC second request (a setback) |
| `EC Clearance`, `China Clearance`, `UK CMA Clearance`, `CFIUS Approval` | named reviews cleared |
| `<Country> Clearance` | other national clearance, e.g. `Mexico Clearance` |
| `Foreign Antitrust Clearance` | unnamed foreign approvals all received |
| `SH Vote` | target shareholder vote held and passed |
| `Effectiveness Date` | S-4 / F-4 declared effective |
| `TO Expired` | tender offer completed |
| `Final Order Granted` | court approval of a scheme / arrangement |
| `Fed Approval`, `FCC Approval`, `FERC Approval`, `State Approval`, `Regulatory Approval` | other regulators |

Not milestones (mention them in the notes instead): an HSR filing, a pull-and-refile, a scheduled vote, a tender extension. An extended outside date goes in column 23, not in the milestones.

| # | Column | Format |
|---|---|---|
| 22 | Milestones so far | `Name YYYY-MM-DD; Name YYYY-MM-DD` — every milestone to date, oldest first (the cell is replaced, not appended) |
| 23 | Latest outside date (if extended) | `YYYY-MM-DD`; blank if never extended |

**Output, mode B:**
1. A table: milestone, date, source (filing + section, or a short quote).
2. The column 22 text (and column 23 if extended) in a code block, ready to paste into the deal's existing row.
3. One or two bullets on what is still pending and anything scheduled (vote date, tender expiry, expected clearances).
