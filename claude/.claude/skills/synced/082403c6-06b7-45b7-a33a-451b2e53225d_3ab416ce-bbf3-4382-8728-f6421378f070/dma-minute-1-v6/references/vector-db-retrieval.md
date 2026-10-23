# Vector DB retrieval — precedent timeline (P1) and standalone-trajectory positioning (P3)

Two structured pulls against `investment-team-v3`, run with `mcp__MeteoraMCP-AWS__semantic-search`
(load it via `ToolSearch` alongside the other AWS tools if it isn't already available in this
session). Both upgrade research legs this module already runs with `WebSearch` alone — use them
**first**, and fall back to web search only for what they don't cover. Everything below was
empirically probed against the live index, including cross-checks on real deals; several filters
that look correct **fail silently** (return zero, or a wrong-but-plausible result, with no error), so
follow the filters exactly as written rather than improvising a variant.

## P1 — Precedent-timeline pull (feeds §1 of `house-view-and-precedents.md`)

`house-view-and-precedents.md` §1 currently sources 2–3 regulatory-clearance precedents via
`WebSearch` alone. Run this pull first, before that search, to get real day counts and outcome
prose directly instead of assembling them from press coverage.

Use the **`default` namespace mirror**, not the `arbjournal` namespace — only the mirror has
numerically-typed, reliably-filterable deal metadata.

```
semantic-search(
  namespace = "default",
  filter = {"$and": [
    {"document_type": {"$eq": "Merger Arb Analysis"}},
    {"sector": {"$eq": "<GICS sector, e.g. 'Health Care'>"}},
    {"actual_completion_date": {"$ne": ""}}
  ]},
  query = "<deal-shape description matching the gating regulator/review type, e.g. 'FTC second request healthcare staffing merger clearance'>",
  top_k = 8
)
```

Read off `deal_timeline_days` (numeric), `actual_completion_date`, `hsr_outcome` (a prose summary of
the full regulatory history — often a complete answer by itself), `acquirer_ticker`/`primary_ticker`.

**Rules:**

1. **Filter on `sector`, never `industry`.** `industry` is a lossy, sometimes-wrong 25-value tag.
   Confirmed on a real query: filtering by `industry` on a semiconductor deal returned precedents no
   more recent than January 2023 — switching to the matching `sector` value returned the same
   precedents plus every post-2023 second-request precedent in the index, including the single best
   remedy-structure precedent available. The `industry` filter silently deletes the current
   enforcement era.
2. **Never filter on `publication_ts`** — the field is absent on most of this corpus and a
   `$gte`/`$lte` filter on it returns zero, silently. Do era-targeting by reading
   `actual_completion_date`/`publication_date` (strings) after retrieval, not with a numeric filter.
3. **`actual_completion_date {"$ne": ""}` is the closed-deal gate — not `deal_timeline_days {"$gt": 0}`.**
   `deal_timeline_days` is 0 both on terminated deals and on some genuinely closed ones. Gate on the
   completion-date predicate; pull the day count as a value, don't filter on it.
4. **`document_type: "Merger Arb Analysis"` is the canonical isolation handle** for this sub-corpus.
   It is not in the tool's documented `document_type` enum — use it anyway, exactly as written here.
5. **Do not filter on `institution`** — a negative predicate (`$ne`) on it is silently ignored by the
   server.
6. This satisfies, rather than relaxes, §1's existing bar: only keep rows with a real day count and a
   stated outcome, and still do the mandatory analogous/not-analogous reasoning and the procedural-
   friction search per §1's existing instructions — the pull supplies better raw material, not a
   shortcut around the judgment.

If this pull returns nothing analogous after a real attempt with the `sector` filter, say so as a
stated gap naming the filter run, then fall back to `WebSearch` — don't silently skip to web search
without noting the vector pull came up empty.

## P3 — Competitive/standalone-trajectory positioning (feeds §5's Optionality paragraph, and
supplements Step 1's 10-K competitor cross-check)

§5's Optionality paragraph currently sources "the target's standalone business trajectory" from
"press materials, the target's own MD&A language, or recent analyst commentary" ad hoc. Sellside
initiations and notes are a more reliable source for that specific input — recent framing of the
target's trajectory, competitive position, and share/margin direction, from an analyst who covers it.

```
semantic-search(
  namespace = "default",
  filter = {"document_type": {"$in": ["Initiation of Coverage", "Sellside Note"]}},
  query = "<TICKER> <company name> standalone business trajectory competitive position revenue trend",
  top_k = 8
)
```

**Rule 0 — do not add a `ticker`/`sector`/`industry` filter to this pull, ever. Put them in the
query text instead.** This is the single most important rule in this section. A large slice of this
corpus — the bulk-loaded `/Interns/IOC Notes Database/<Sector>` library specifically — has **blank or
flatly wrong** `primary_ticker`/`sector`/`industry` metadata, even though the underlying document
text is fine. Confirmed on two independent real cases:

- **Whirlpool (WHR):** `{"primary_ticker": {"$eq": "WHR"}}` missed a 167-page Stifel initiation
  sitting in `/Interns/IOC Notes Database/Materials` entirely — its `primary_ticker` is `""`.
  Dropping the ticker filter and querying `"Whirlpool WHR major appliance market share"` found it
  immediately, top-ranked.
- **Alzchem (ACT):** `{"sector": {"$eq": "Materials"}}` — which looks correct, since the document
  physically lives in `/Interns/IOC Notes Database/Materials` — returned **zero** relevant hits. The
  document's own `sector` field is mistagged `"Financials"`. Dropping the sector filter, identical
  query, surfaced Alzchem's own initiation as the top hit.

The `document_type` filter above is comparatively reliable and fine to keep. Never add
`primary_ticker`, `sector`, or `industry` — put the ticker and company name directly in the query
text and let the embedding do the work the metadata can't. **Always confirm the returned chunk's
`primary_company` or the chunk text itself actually names the target company** before citing it, since
a name-in-query search can occasionally surface a peer or comp instead.

**Other rules:**

1. This is also the right pull to supplement Step 1's 10-K competitor cross-check when a party's
   Competition-section disclosure is generic or absent (a private acquirer, a target that names no
   one by name) — same query shape, naming the specific product line rather than the bare industry.
2. Exclude the ArbJournal mirror or treat it as desk color, not independent corroboration — the
   `document_type` filter above already excludes `"Merger Arb Analysis"`; if a hit's `folder_path` is
   `/Interns/ArbJournal` anyway, don't cite it as if it were a third-party source.
3. State the note's date and firm. This corpus skews toward whenever a firm last initiated or updated
   coverage — sometimes recent, sometimes 2–3 years old — and §5's read depends on how current the
   trajectory read actually is.
4. If nothing usable comes back, say so as a stated gap naming the query run, and fall back to §5's
   existing "press materials or MD&A language" sourcing rather than silently substituting nothing.

## What this does not cover

Precedent transaction multiples and peer trading comps exist in this index (fairness-opinion
proxies under `document_type: "SEC Filing"`, and comp tables in initiations) but are deliberately
**not** wired into this module. DMA stays completion-risk-only by design — it does not make an
"is this price fair" call, and multiples/valuation belong to the full deal-completion report, not
here.
