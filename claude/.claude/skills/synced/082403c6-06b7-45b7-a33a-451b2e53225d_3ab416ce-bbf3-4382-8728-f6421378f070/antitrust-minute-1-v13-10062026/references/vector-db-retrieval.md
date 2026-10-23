# Vector DB retrieval — precedents (P1), competitive positioning (P3), enforcement posture (P5), regulatory pathway (P6)

Four structured pulls against `investment-team-v3`, all run with the already-loaded
`mcp__MeteoraMCP-AWS__semantic-search` tool. They replace part of what Agents B, D and E would
otherwise do with web search alone — use them **first**, and fall back to web search only for what
they don't cover.

Everything below was empirically probed against the live index, including a dry run on a real deal.
The rules exist because several filters that look correct **fail silently** — they return zero or a
wrong-but-plausible result set with no error, so a guessed filter produces a confidently wrong or
confidently empty memo section. Follow the filters exactly as written; do not improvise a variant.

## P1 — Precedent deals with a real day count and outcome (feeds Section F, and Section E's timeline)

There are two vector stores of ArbJournal's deal files. Use the **`default` namespace mirror**, not
the `arbjournal` namespace, for this pull — only the mirror has numerically-typed, reliably-filterable
metadata.

**Query — run without the completion-date gate.** The filter below deliberately does **not** require
`actual_completion_date != ""`. An earlier version of this pull gated on that field to select "real"
precedents, and the gate is a bug, not a feature: it silently drops every still-open, blocked, or
terminated deal, which is exactly the population that is most diagnostic on a slow-moving regulatory
regime. A deal that has been sitting in front of a regulator for 400+ days with no resolution is *more*
informative about that regulator's real-world friction than a clean closed comp, not less — and a
completion-date gate deletes it from the result set before you ever see it. (This surfaced concretely
on a live run: a state-money-transmitter-gated deal's precedent pull, filtered the old way, missed the
single most relevant comparable in the corpus — a still-open deal on the identical regulatory pathway,
blocked mid-review by a state regulator that had already granted and then suspended its own approval.
That comparable would have changed the base-case read, and the gate is why it wasn't found.)

```
semantic-search(
  namespace = "default",
  filter = {"$and": [
    {"document_type": {"$eq": "Merger Arb Analysis"}},
    {"sector": {"$eq": "<GICS sector, e.g. 'Information Technology'>"}}
  ]},
  query = "<deal-shape description, e.g. 'horizontal semiconductor merger HSR second request divestiture outcome'>",
  top_k = 8
)
```

Read off `deal_timeline_days` (numeric, where present), `actual_completion_date` (where present),
`deal_status` (open / closed / terminated — read this explicitly, don't infer it from whether
`actual_completion_date` is populated), `hsr_outcome` (a prose summary of the full regulatory
history — usually a complete, citable answer on its own), `acquirer_ticker`/`primary_ticker`,
`industry`, and — for still-open deals — any `critical_path` or status-narrative field describing what
is currently pending and why.

**Keep three kinds of rows, not just one.** (1) **Closed deals** with a real day count and a stated
outcome — the existing bar, unchanged. (2) **Open/live deals** with no completion date yet — cite the
days elapsed since signing as of this run (`today - deal_date_announced`), state plainly that the deal
is still pending, and report whatever the `critical_path`/status narrative says is currently holding it
up; an open deal is a precedent for "what friction looks like while it's happening," not for a final
day count, and the memo should frame it that way rather than as a completed comparable. (3)
**Terminated/failed deals** — cite the announce-to-termination day count and the stated reason for the
break; a deal that failed on the same regulatory pathway is a real data point on tail risk and belongs
in the memo, not just closed successes. Label each row's status plainly (`Closed — N days`, `Open —
N+ days and counting, pending [X]`, `Terminated — N days, broke on [X]`) so the reader never mistakes an
open deal's elapsed-days count for a completed timeline.

**Rules, in order of how much damage breaking them does:**

1. **Filter on `sector`, never on `industry`.** This is the load-bearing rule. `industry` is a lossy,
   sometimes-wrong 25-value tag (Spirit Airlines is tagged "Logistics / Supply Chain"). Verified on a
   real query: filtering `industry: "Semiconductors"` returned 5 precedents, newest closed January
   2023 — filtering `sector: "Information Technology"` instead returned 14, including the single best
   remedy-structure precedent in the index (ANSS/SNPS, 548 days, cleared only after divesting to
   Keysight) and every other post-2023 second-request precedent. The `industry` filter silently
   deletes the current enforcement era. Screen for shape/analogy with the semantic query and by
   reading the results, not with the `industry` filter.
2. **Never filter on `publication_ts`.** The field is absent on this corpus; a `$gte`/`$lte` filter
   on it returns zero, silently. There is no working numeric date filter here — do era-targeting by
   reading `actual_completion_date`/`publication_date` (strings) after retrieval.
3. **Do not filter on `actual_completion_date` or `deal_timeline_days` — read them, don't gate on
   them.** `deal_timeline_days` is 0 both on terminated deals and on some genuinely closed ones (the
   source table simply had no Timeline row), and `actual_completion_date` being empty is exactly the
   signal that a deal is still open, not a reason to exclude it (see the note above the query). Gating
   on either field silently deletes open and failed deals from the result set. Use `deal_status` and the
   presence/absence of `actual_completion_date` to *label* each row's status (closed / open / terminated)
   after retrieval — never to filter the query itself.
4. **`document_type: "Merger Arb Analysis"` is the canonical isolation handle** for this sub-corpus
   (equivalently `folder_path: "/Interns/ArbJournal"` — same result set). It is not in the tool's
   documented `document_type` enum; use it anyway, exactly as written here.
5. **Do not filter on `institution`.** A negative predicate on it (`$ne`) is silently ignored by the
   server, and on AlphaSense-bundled documents elsewhere in the index `institution` reflects the
   aggregator, not the actual research firm — it isn't reliable here either.
6. **State the HSR-regime era per row, as the existing precedent rule already requires** — there are
   three eras, not two: routinely granted pre-February-2021 (~73–81% of requests); fully suspended
   February 2021–February 2025 (no grants possible); reinstated since February 2025 but running at a
   low ~29% FY2025 grant rate (per the agencies' own HSR annual report), so a recent grant is real but
   still the exception. A pre-2021 "early termination granted" day count still understates the modern
   floor. Reading `sector` instead of `industry` is what makes recent-era precedents reachable at all;
   still check the date on every row, and verify the current grant-rate trend live rather than
   assuming ~29% is still current.
7. **Optional supplementary pull — competitor-set cross-reference:** add
   `{"secondary_tickers": {"$in": ["<TICKER1>", "<TICKER2>"]}}` to the same filter (in place of the
   sector clause) to find prior deals where either party was named as a competitor. This is a
   low-hit-rate pull — expect mostly noise — but occasionally surfaces the one genuinely load-bearing
   precedent (e.g., the last deal of comparable scale in the same product space that drew a second
   request and didn't survive it). Read the hits; don't cite reflexively.

8. **Mandatory second pass on any sector-gated or dual-gated deal: query the specific regulatory
   *regime*, not the deal's broad sector.** This is not optional and not satisfied by the sector-level
   pull above — a query like "payments M&A" or "fintech merger" is too broad to surface regime-specific
   friction; the query has to name the actual gating mechanism. Keep the same filter (or drop the
   `sector` clause entirely and rely on the query alone, which is often more precise here), change the
   semantic query to the regulator and the specific process — `"Form A Delaware insurance department
   change of control approval timeline"`, `"PRA FCA change in control insurance approval"`, `"OSFI
   Minister of Finance insurance acquisition approval"`, `"FCC 180-day shot clock licence transfer"`,
   `"state money transmitter license change of control approval multi-state"`. This matters because
   ArbJournal deal files frequently embed **their own tables of prior approvals before the same
   regulator** inside a chunk — a table of ten prior Form A reviews with day counts is worth more than
   the deal the chunk nominally belongs to, and a shape-only or sector-only query will not reliably
   surface it. Run both passes (sector-shape and regime-specific); treat the regime-specific pass as
   the primary source for the Approval Clock Build's "observed clock" column, and do not let a
   sector-only pull stand in for it — a broad sector search and a named-regime search routinely surface
   different, non-overlapping precedent sets.
9. **Apply the five-year recency ceiling when reading results back.** Screen on
   `actual_completion_date` after retrieval — there is no working numeric date filter (see rule 2).
   Rows older than five years are admissible for a sector approval only where nothing in-window
   exists for that body, and must be labelled out-of-window.

If this pull returns nothing analogous after a real attempt, say so as a stated negative finding
naming the filter that was run (per the module's existing sourcing discipline) — do not fall back to
an estimate, and do not silently drop to web search without noting the vector pull came up empty.

**A precedent's value to this memo does not require it to have closed.** Report open and terminated
rows alongside closed ones in Section F's precedent table (or Section E's Approval Clock Build sanity
check, whichever the row is more diagnostic for), with the status label from rule 3 above carried into
the table itself — do not quietly drop an open or failed deal to keep the table looking like a clean
set of comparables. A table of five closed deals plus one open, currently-blocked deal on the exact
same pathway is more informative than six closed deals, and should read that way.

## P5 — Standing enforcement-posture editorials (feeds Section A's enforcement-posture row)

ArbJournal maintains running, dated rosters of open regulatory matters as standalone multi-chunk
documents in the **`arbjournal` namespace**, each keyed to its own `deal_id`. These are a direct,
sourced, dated answer to "what is this agency's current posture" — use before falling back to web
search for speeches/press coverage.

```
semantic-search(
  namespace = "arbjournal",
  filter = {"deal_id": {"$eq": "<id from the table below>"}},
  query = "<the specific agency or regime you need, e.g. 'FTC second request pace medium risk'>",
  top_k = 5
)
```

| deal_id | Roster |
|---|---|
| 12254 | Antitrust & Active HSR Second Requests — the primary one for a US DOJ/FTC deal |
| 12248 | Active CFIUS Reviews |
| 14684 | European Antitrust Reviews (EC/CMA prohibition tables) |
| 13870 | UK CMA Update |
| 14094 | New Administration (enforcement-regime transitions) |
| 14664 | FTC Policy (Pharmaceuticals) |
| 13956 | Deal Statistics, including a Failed Deals table |
| 14140 | Positive Retrades |

Pick the roster matching the deal's lead regulator (per Agent D's existing instruction to identify the
lead agency first). These docs run 20–90 chunks and are re-entered/updated over time — **read the
`entry_timestamp` on the returned chunk and state it as the as-of date**, exactly as the module's
existing enforcement-posture rule already requires; do not present a stale entry as current without
flagging it. If the deal's own parties or a close comparator already appear in the roster (common —
these are live trackers of active matters), that is itself a directly on-point finding, not just
posture color.

## P3 — Competitive positioning (feeds Section C's Verbatim Competitor Disclosures and the
overlap narrative)

Named-competitor lists from sellside initiations and notes, drawn straight from the analyst's own
framing of who competes with whom — near-100% hit rate when a company is covered. Use it in two
situations: (a) as the primary source when EDGAR gives nothing to work with — a private target, a PE
portfolio company with no public Competition-section disclosure — before writing the gap as final;
(b) as a corroborating cross-check even when EDGAR does have a Competition section, since a 10-K's
list is often generic ("other electronic trading venues") where a covering analyst names names and
gives product-line detail.

```
semantic-search(
  namespace = "default",
  filter = {"document_type": {"$in": ["Initiation of Coverage", "Sellside Note"]}},
  query = "<company name> competitors competes with <specific product line, not the bare industry>",
  top_k = 5
)
```

**Rules:**

1. **Name the product line in the query, not the industry.** A bare industry-level query returns
   TAM/valuation tables the reranker can't distinguish from a competitor list; naming the specific
   product or business line reliably surfaces the Competition/positioning paragraph instead.
2. **Exclude the ArbJournal mirror or label it as desk-internal.** An unfiltered query on a deal
   already in the ArbJournal file returns the desk's own write-up quoting the target's 10-K — citing
   that as independent corroboration is circular (you'd be citing Meteora quoting the filing Agent B
   already pulled directly). The `document_type` filter above already excludes it (`"Merger Arb
   Analysis"` is not in the `$in` list); if a hit's `folder_path` is `/Interns/ArbJournal` anyway,
   treat it as desk color, not a new source.
3. **State the note's date and firm.** This corpus skews toward whenever a firm last initiated or
   updated coverage — sometimes recent, sometimes 2–3 years old. A competitor *list* rarely goes stale
   fast, but say the date regardless, same discipline as every other sourced fact in this module.
4. **This is a competitor-list source, not a market-share source.** It will not reliably give you
   percentages — that's P1's occasional lottery-ticket hit or the existing web-search gap-fill, not
   this pull. Use P3 only for "who are the named competitors," not for sizing the overlap.
5. **If nothing usable comes back, say so as a stated gap naming the query run** — do not substitute
   a paraphrase of the target's own "we compete with numerous companies" boilerplate as if it were a
   real finding.

## P6 — Chain Bridge Research: regulatory pathway and approval mechanics (feeds Agent E and Section E's Approval Clock Build)

Chain Bridge Research writes **regulatory-pathway analysis** — statutory clocks, control thresholds,
which regulators condition a close, and how approvals sequence — where ArbJournal writes deal files
and running day counts. The two are complementary, not redundant: ArbJournal tells you a deal took
301 days; Chain Bridge tells you the PRA takes 60 working days from acknowledgement and why that
matters. **On a sector-gated deal this is the highest-value pull in the module.** Run it alongside
P1, never instead of it.

```
semantic-search(
  namespace = "default",
  filter = {"folder_path": {"$eq": "/Chain Bridge Research"}},
  query = "<approval body> change of control approval threshold timeline <sector>",
  top_k = 5
)
```

**Rules:**

1. **Query by regulator and mechanism, not by party name.** `"PRA FCA change of control insurance
   approval working days"` returns the mechanics; `"[Target] regulatory approvals"` returns nothing
   useful on a deal days old.
2. **Run one query per critical-path approval body**, not one combined query. A combined query
   returns surface-level coverage of all of them, which is the opposite of what the build needs.
3. **These notes carry real statutory detail and are frequently the only internal source for it** —
   thresholds, working-day counts, interruption mechanics, whether a regime conditions the close or
   merely appears as a covenant. Cite firm, note title and publication date, and check the date: a
   statutory period stated in a 2018 initiation may have been amended since, so treat P6 as the
   anchor for Agent E's live verification rather than as the final word.
4. **Read them for sequencing as well as duration.** Chain Bridge routinely states which approvals
   the parties treated as conditions versus covenants, which is exactly the concurrency question
   Section E.2 has to answer and which no day count will tell you.
5. **If the pull comes up empty, say so as a stated gap naming the filter run**, then fall back to
   Agent E's regulator-guidance and law-firm-white-paper search — do not silently skip.

## What this does not cover

Per-approval day counts from regulator websites (state DOI approval orders, hearing calendars,
supervisory decision registers) are **not** in this index and are Agent E's live-search task, not a
vector pull. Market share / HHI data is **not** reliably sourceable from this index — coverage is uneven and what
exists is frequently stale (multi-year-old figures attributed only to "this report," not a named
provider). Do not retarget the market-structure gap-fill (item 7 in the numbered list above) to this
index; that gap-fill stays a web-search task, exactly as it is today. Precedent transaction multiples
and peer trading comps also exist in this index but are out of scope for this module (they belong to
the full deal-completion report, not the antitrust module) and are not wired in here.
