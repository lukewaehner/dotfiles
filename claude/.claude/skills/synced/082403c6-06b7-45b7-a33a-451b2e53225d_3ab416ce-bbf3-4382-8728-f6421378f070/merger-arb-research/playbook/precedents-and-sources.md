# Precedents, sources and tools

Load when: you need a precedent timeline, a fact from a filing, the desk's own research, a docket, a
price, or must test a broker note. This is the routing map; use it before improvising a search.

## Why it matters for the spread

The working close date and every risk read rest on sourced facts and real announce-to-close day counts.
Many filters on the internal index fail silently (zero results or plausible wrong results), and many
"open questions" are just pointed at the wrong tool. A wrong route produces a confident, wrong memo.

## Question to tool

| Question | Route |
|---|---|
| What does the agreement say (fees, MAE, covenants, outside date, conditions) | `edgar-filings` for the 8-K, `edgar-filing-index` to confirm Ex-2.1 and exhibits, `edgar-filing-text` with `summary=true`, then windows of 40,000 chars or less by offset; or `exhibit='2.1'` with accession and ticker |
| Press release, deck, announcement 8-K items | `extract-8k`; `edgar-filing-text` with `exhibit='99.1'` |
| Competition section, segment and geographic revenue | `extract-10k`; else `edgar-filing-text` with `section='1'` or the Competition offset from the summary |
| What changed between S-4 and S-4/A, preliminary and definitive proxy | `edgar-redline` (first call without `section_filter` to see sections touched, then drill in) |
| Who owns, who signed support agreements, insider sales, pledges | `edgar-ownership-search` (issuer ticker, form type 13D/13G/4; `enrich=true` for shares and percent) |
| Is a company public, its scale, share count | `edgar-filings`, `edgar_company_facts` |
| Is a suit, demand or appraisal petition pending; did a cited case settle | `docket-search` (party_name, court `delch`, `ded`, `nysd`, `dcd`), `docket-details`, `docket-filings`; RECAP is incomplete, so empty is not clean. Daily firm budget of 125 calls |
| How have courts ruled (MAE, specific performance, appraisal fair value, controller deals) | `caselaw-search` then `caselaw-opinion` |
| How long do deals with this regime take; which precedents had it | `arbjournal-precedents` with `regimes` such as `antitrust:us`, `antitrust:ec`, `fdi:uk`; `since`; `status` closed, active or any. Read `notes[]` before quoting |
| A specific precedent's regulatory history in prose | `semantic-search` P1 pull (below) |
| Has anyone at the desk covered this | `research-search` (Drive, mailbox, memory docs; entity filter), then `semantic-search` per corpus, `graph-search` for relational scoping |
| Broker notes received by email | `list-emails` (search tickers or deal name), `read-email` in full; capture firm and analyst from the signature |
| SPAC-specific position, trust, deadline, deal data | `spac-details` (never for price) |
| Current price | live price tool (below) |
| Foreign filing perimeter | target's revenue by country from the 10-K and Exhibit 21 against each regime's thresholds; the confidential schedule is only the final check |
| Was a fact public before announcement | earliest dated public source; the desk library pull below |

Payload discipline: never run `edgar-filing-text` at its 200,000-char default. Get the TOC first; delegate
agreement-length reads to a subagent. If `summary=true` fails, retry once with accession and ticker, then
skip the filing and say which one is missing. Never fetch SEC.gov URLs directly.

## Internal index routes (`semantic-search`, index investment-team-v3)

Namespaces are disjoint; pick one per query: `default` (Drive: sellside, transcripts, filings, desk
research, plus a mirror of ArbJournal deal files), `arbjournal` (ArbJournal desk notes and rosters),
`emails` (desk threads on the filings and team lists, one thread per document).

P1, precedent deals with day counts:
```
namespace = "default"
filter = {"$and": [{"document_type": {"$eq": "Merger Arb Analysis"}},
                   {"sector": {"$eq": "<GICS sector>"}}]}
query = "<deal shape and regulator, e.g. horizontal software merger HSR second request divestiture>"
top_k = 8
```
Read `deal_timeline_days`, `actual_completion_date`, `deal_status`, `hsr_outcome` (often a complete
citable history), tickers, and any critical-path narrative on open deals.

- Filter on `sector`, never `industry`; the industry tag is lossy and silently drops recent deals.
- Do not filter on `publication_ts` in this sub-corpus (absent; returns zero), on `institution`
  (negative predicates ignored), or on `actual_completion_date` / `deal_timeline_days` (gating deletes
  open and terminated deals; timeline is 0 on some closed deals too). Read them after retrieval.
- `document_type: "Merger Arb Analysis"` isolates the ArbJournal mirror even though it is not in the
  documented enum.
- On any deal gated by a sector or foreign regulator, run a second pass naming the regime and process
  ("Form A insurance change of control approval timeline", "FCC license transfer 180-day shot clock",
  "state money transmitter change of control"). Deal files often embed tables of prior approvals before
  the same regulator, which the sector pass will not surface.
- Optional: replace the sector clause with `{"secondary_tickers": {"$in": [...]}}` to find prior deals
  naming either party as a competitor. Low hit rate; read before citing.

P3, sellside competitor and trajectory views: namespace `default`, filter document_type in
["Initiation of Coverage", "Sellside Note"], ticker and company name and the specific product line in the
query text. Never add ticker, sector or industry filters here: much of the initiation library has blank
or wrong tags. Confirm the chunk names the target. Exclude or label ArbJournal hits as desk color (citing
the desk quoting a 10-K is circular). State firm and date; this is a competitor-list source, not a share
source.

P5, enforcement-posture rosters: namespace `arbjournal`, filter `{"deal_id": {"$eq": <id>}}`, query the
agency and issue. Report the chunk's `entry_timestamp` as the as-of date.

| deal_id | Roster |
|---|---|
| 12254 | Antitrust and active HSR second requests (US) |
| 12248 | Active CFIUS reviews |
| 14684 | European antitrust reviews (EC, CMA) |
| 13870 | UK CMA update |
| 14094 | Enforcement-regime transitions |
| 14664 | FTC policy, pharmaceuticals |
| 13956 | Deal statistics, failed deals table |
| 14140 | Positive retrades |

If the parties or a close comparator already appear on a roster, that is a direct finding.

P6, regulatory pathway mechanics: namespace `default`, filter `{"folder_path": {"$eq": "/Chain Bridge Research"}}`,
one query per approval body naming the regulator and mechanism (thresholds, statutory clock, conditions
versus covenants, sequencing). Highest value on sector-gated deals; check the note date against
statutory amendments.

Deal-specific queries on a newly announced deal return ticker-string collisions; the deal is not indexed
yet. Vectorization of new Drive files lags by hours, so a miss is not absence: search Drive directly for
recent files (for example a council or research folder) and confirm by file contents, never guess between
two candidate folders.

Desk library first: before the web, enumerate what the desk holds on each party from the 12 months
before announcement (`research-search` with entity, or `semantic-search` with the four-field ticker
`$or` over primary_ticker, secondary_tickers, folder_ticker_1, folder_ticker_2, high `top_k`,
`rerank=false`). Initiations and expert calls first. Mark each file read (`read-document`,
`download-drive-file`), sampled (say for what), or not read (with a reason other than time).

## Precedent method

- Rank comparability by what was combined, not who signed. On antitrust-led deals: (1) the acquirer's own
  prior deals in the same product market, (2) same-industry deals by any buyer, (3) same regulatory shape
  in adjacent industries, labeled adjacent. A same-buyer, different-market deal is a buyer-posture data
  point only. On deals led by a sector or foreign regulator, rank by approval body first, acquirer type
  second, product market third.
- Every row needs a real announce-to-close day count (or a dated range), the outcome, its status, and a
  "why analogous" cell naming the approval it predicts. Drop rows that cannot carry this.
- Keep open and terminated deals. Label rows "Closed, N days", "Open, N+ days, pending X", "Terminated,
  N days, broke on X". An open deal stalled on the same pathway is often the most diagnostic comparable.
- Read each precedent for procedural friction as its own search: pull-and-refile, extended waiting
  periods, timing agreements. "No second request but one refile" differs from a clean expiry.
- Tag each US row by HSR era: before Feb 2021 (early termination routinely granted), Feb 2021 to Feb 2025
  (suspended), Feb 2025 onward (reinstated, low grant rate, about 29% in FY2025 [verify current rate]).
  A pre-2021 early-termination count understates today's floor.
- Five-year recency ceiling for sector-approval precedents; older rows only when nothing in-window
  exists, labeled out-of-window with what changed.
- Capture per-regulator day counts where public (filing dates, hearing notices, approval orders); one
  sourced per-regulator count beats several total-deal timelines.
- For a repeat acquirer, list every HSR-reviewed deal of the last ten years with overlap type, outcome
  and days, and state the outcome mix in one sentence. The single worst precedent is one row, never the
  verdict.
- Discount precedents with more serious overlap than this deal, and say so.
- Precedent friction builds scenarios above the contractual floor; it does not move the working date
  without deal-specific evidence. Compute dates with the deal clock calculator, never by hand.

## Standing public record

Use these as places to look when a branch reaches them; each one used reports Found (cited), Not found after
search (name the search), or an open question with the reason.

- Regulator state: for each likely reviewer, pending rules, draft guidelines or consultations (date,
  comment deadline, expected final, not yet in force), and the last 12 months of outcomes on the nearest
  comparables. "Not found after search" checks unsourced claims that an agency "is blocking deals".
  Law-firm client alerts are the fastest source.
- Buyer's own track record: every deal in about six years, announce and close dates, days, approvals
  required and when each landed, remedies. Include subsidiaries and the slow outlier. Note pending deals
  by the same buyer; a live review is the best read on its standing. Then say how this target differs.
- Target's government authorizations and regulated standing: clearances, foreign-ownership mitigation,
  federal cloud authorizations (FedRAMP Marketplace), defense cloud impact level, federal contract dollars
  (USAspending or an aggregator, flagged single-source), named programs, export-control status, whether
  the target hosts customer data. Government revenue share only from filings.
- Sector packs by end market: telecom (FCC licenses, Team Telecom, state commissions), energy (FERC 203,
  state commissions, NRC, CFIUS), financial (Fed, OCC, state insurance), semis (export classes, CHIPS
  conditions, SAMR record), sensitive data (CFIUS, state privacy, EU rules), health care (state notice and
  approval regimes). Always: top disclosed customers and whether any is a government or a buyer rival.
- Rivals' arrangements: for the top two or three competitors, owner and country, whether they hold the
  same authorization, and under what structure. A regulator that already accepts a foreign-owned rival
  under a known structure has shown what it tolerates.
- Prior strategic interest: reported approaches, talks, bids, activist campaigns in three years (who,
  when, price, outcome). Feeds the topping-bid read.
- Close with three to six concrete questions for counsel, each tied to a finding.

## Stress-testing a broker note

A note is a hypothesis to test. Report what it got right, what it left out, what it got wrong, quoting no
more than 40 words of it.

- Date feasibility: run every quoted close, filing or expiry date through the deal clock `tender --check`
  using the agreement's launch and filing covenants and Business Day calendar. Flag weekends and holidays,
  dates earlier than physically possible, and dates feasible only on early filing (a best case). One- or
  two-day gaps between notes usually come from weekends-only versus agreement-calendar counts. Never
  average notes' dates into the working date.
- Outside-date cushion: days between the note's close and each outside date (`ladder`).
- Comparables restarted from this deal's actual filing date, not announcement.
- Remedy cap, burdensome condition and reverse fee read against the agreement; recompute fee
  percentages on our base.
- Regulator calls: each needs a stated reason tested against a primary source; otherwise "unsupported".
- Financing wording: commitment letter versus mandate letter.
- Buyer stock reaction and upside-to-downside ratio (see spread-and-downside.md).
- Market-fact ledger: every claim that a product competes, a competitor exists, a contract was signed,
  a share or revenue figure. Mark verified, unverified or contradicted against a primary source. A
  product page proves "sells it today", a press release proves "signed", only a filing or cited study
  proves share.
- State perimeter claims: was the statute's revenue or asset test applied, or only a site count? Notice
  or approval? Clock counted from filing? A statute test beats any sell-side tier.
- Relayed management statements ("management told us"): log as relayed, firm, date. One desk is a claim,
  two independent desks are corroboration, only a filing or transcript confirms.
- Misses: a claim absent from our work whose earliest public source predates announcement is a method
  miss. Verify it, name the check that should have caught it, and log it.
- Tier lists set ordering and break ties among untested claims only; method beats tier.

## Price fallback order

1. Live price tool (timestamp it; never reuse an earlier spread).
2. A price the user pasted in this chat, labeled user-supplied with its time.
3. A price quoted in a note in the chat, naming the note.
4. None of these: do not guess. Produce the price-independent hurdle output and say so in the first line.

## Common errors

- Gating precedent pulls on completion date and losing open or failed deals.
- Filtering by `industry` or by ticker tags on the initiation library.
- Reading a vector miss on a fresh document as proof it does not exist.
- Citing the desk's own write-up as independent corroboration.
- Precedent rows with "a few months" instead of day counts, or with no era tag.
- Carrying "not yet filed" forward without re-pulling EDGAR.
- Reporting "no second request" where the honest answer is "could not determine either way".
