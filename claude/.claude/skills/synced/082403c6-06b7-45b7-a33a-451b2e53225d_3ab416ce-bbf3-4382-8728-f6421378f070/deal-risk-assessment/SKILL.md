---
name: deal-risk-assessment
description: "Antitrust and deal-completion risk assessment for announced M&A transactions with any buyer type — PE sponsors, strategics, or hybrid/consortium bidders. Trigger on \"assess deal risk\", \"will the [deal] close\", \"antitrust risk on [deal]\", \"merger arb analysis on [ticker]\", \"completion probability\", any request to judge whether an announced merger or take-private will complete, or a pasted merger press release / agreement / deal 8-K with \"how risky is this\". Classifies buyer type, then produces a phased, EDGAR-cited report (deal terms, buyer footprint, overlap screen, competitive effects, financials, litigation, blind synthesis) plus a strictly separated Tape Check. Sell-side research each run: Outlook + broker notes manually uploaded to the deal folder / Claude Project (replaces AlphaSense), plus Vector Database passes (ArbJournal / Chain Bridge Research institution filters + broad), cited from hit metadata, behind the blind wall. Always use for deal-completion risk — never ad hoc."
---

# M&A Deal Risk Assessment (Buyer-Aware, Blind-Then-Tape)

Produce an institutional deal-completion risk assessment for an announced M&A transaction, with antitrust risk as the centerpiece. The workflow classifies the buyer type early and branches: a private equity sponsor's antitrust exposure lives in its *portfolio companies* and requires a discovery-and-mapping exercise; a strategic acquirer's exposure is visible directly in its own consolidated filings. Hybrids get both.

The report has two strictly separated stages:

1. **Blind fundamental assessment (Phases 1–7).** Do NOT pull the target's current stock price, the deal spread, or any market pricing during these phases. The point of the fundamental work is to form a view *independent* of the market's consensus. If price data leaks in early, the report anchors to the spread and merely rationalizes it — destroying the edge.
2. **Tape Check (Phase 8).** Only after the blind synthesis is fully written, pull live pricing and reconcile the fundamental view against what the market is pricing.

Adopt the perspective of a prospective deal risk analyst evaluating transaction completion probability. Do not provide strategic recommendations to parties in the transaction.

## Anti-hallucination rules (apply in every phase)

These are the discipline that makes the report usable. Violating them produces confident-sounding garbage.

- **Never estimate, calculate, or invent market shares, HHI figures, or probability percentages without explicit source data.** If market size or concentration data is unavailable, state that limitation explicitly instead of estimating. A stated gap is information; a fabricated HHI is a landmine.
- **Cite every fact and figure to a specific source** — EDGAR filing (form type + filing date, accession number where practical), named industry report, government dataset, or news article with outlet and date. This applies to **tables, not just prose: every table names its source in the caption (or a per-row source column)** — a number that lives only in a table with no visible source is unauditable, and the reader shouldn't have to guess whether it came from a 10-K, an analyst estimate, or thin air.
- **Competitor lists and geographic revenue breakdowns must come verbatim from EDGAR filings** (10-K/10-Q Competition sections and segment tables). Do not paraphrase competitor lists — quote or reproduce them and cite the filing.
- **Distinguish sourced facts from analytical opinion.** In the report, opinions are labeled as such ("Assessment:").
- **Closing-probability language is qualitative and precedent-based only.** Ground any probability characterization in named historical precedent transactions (deal, year, outcome). Never emit a bare "85% chance of closing" from intuition.
- **Stage-classify completion sentiment before it enters the completion view.** Analysts writing on announcement day routinely relay sentiment formed during the *pre-announcement rumor window* — "the buy-side is ~50/50 on whether they do a deal," "a deal was largely expected." That is speculation about whether a deal would be *struck*, and it is mooted the moment the agreement is signed; it is NOT a read on whether the *announced* deal will *close*. "Will the deal get done" is ambiguous exactly here — pre-signing it means "will they agree," post-signing it means "will it consummate." So date-stamp each sentiment datum, read what it actually refers to, and carry only post-signing "will the signed deal close" sentiment into the Phase 7 completion assessment or the Tape Check. Pre-announcement deal-happening chatter belongs in the deal-background narrative, never as live completion risk — and a report that leans its "swing factor" on it is resting a live conclusion on a dead question.
- Buyer footprint mappings: verify via EDGAR and issuer/sponsor disclosures; note minority stakes explicitly and flag anything unverifiable as unverified.

## Tools

- **EDGAR**: `MeteoraMCP:edgar-filings`, `edgar-filing-index`, `edgar-filing-text`, `edgar-company-facts`, `edgar-ownership-search` for all filings work. Fall back to web_fetch of sec.gov if MCP tools are unavailable.
- **Web search**: sponsor portfolio pages, PE database coverage, trade press, FTC/DOJ press releases and precedent enforcement actions, short-seller reports.
- **Acquirer / target IR website (deal materials)**: the deal **press release** and **investor presentation ("pitch deck")** are posted to the acquirer's investor-relations site — usually a newsroom / press-release page and an "Events & Presentations" page or a dedicated transaction microsite — often within hours of announcement, and are also filed on EDGAR as 8-K exhibits (press release Ex-99.1; deck furnished Ex-99.1/99.2 under Item 7.01). The target's IR site frequently mirrors them. Fetch with `web_fetch`; if the page is client-rendered and returns an empty shell, switch to the `claude-in-chrome` tools to render it. These are primary sources dated at announcement — read them during Phases 1–7; the blind wall bars only live market pricing, not the disclosed premium or the deck's own figures.
- **Bloomberg (Phase 8 ONLY)**: `MeteoraMCP:get-price`, `get-intraday-bars`, `get-vwap`, `get-company-info`. Do not call these before Phase 8.
- **Sell-side research — two channels, both run every time** (see "Sell-side enrichment" below). These are not ranked or substitutable; each surfaces research the other misses, so run both on every assessment and only drop one when it is genuinely inaccessible (and then say so):
  - **Outlook (Microsoft 365)**: the user's own inbox of broker notes, via the `outlook_email_search` MCP tool + `read_resource` to fetch bodies. Holds the research the user actually receives. See `references/outlook-research-scan.md`.
  - **Uploaded deal-folder research (Claude Project)**: before starting this workflow the user manually downloads the relevant sell-side research and places it in the deal folder / uploads it to the attached Claude Project. This curated set is a primary channel — it replaced the old automated AlphaSense browser step, so treat it with the same weight that step carried: enumerate every research file (Project file list, conversation attachments, any connected deal folder) and read each one in full. Mechanics in "Uploaded research mechanics" below.
- **Vector Database (`MeteoraMCP:semantic-search` on the `investment-team` index)**: the internal research corpus — ArbJournal deal files, broker notes, internal arb research, filings, transcripts. Mandatory passes on every assessment: **named-institution passes** for ArbJournal and Chain Bridge Research (filtered on the institution metadata) and a **broad deal-context pass** (the companies, their market shares, their competitors, precedent transactions in the same sector, and anything else relevant to the deal). Mechanics in "Vector Database passes" below.

## Sell-side enrichment (Outlook + uploaded research + Vector Database)

Sell-side research fills the two gaps EDGAR cannot: analyst **market-structure estimates** and analyst **deal handicapping**. It enters at exactly two points — Phase 4 (market structure) and Phase 7 (deal handicapping) — from sources that all normalize into one attributed set:

1. **Outlook** — the broker notes the user actually receives in their inbox. Mechanics in `references/outlook-research-scan.md`.
2. **Uploaded deal-folder research** — the broker notes the user manually downloaded and placed in the deal folder / attached Claude Project before prompting this workflow. This is the user's own curated breadth layer (it replaced the automated AlphaSense step); its presence is deliberate, so read all of it. Mechanics below.
3. **Vector Database** — the named-institution passes (ArbJournal, Chain Bridge Research) and the broad deal-context pass over the internal corpus. Not strictly "sell-side," but it feeds the same two enrichment points (plus Phase 7 precedents) and follows the same attribution discipline. Mechanics below.

**Run everything on every assessment — Outlook AND the uploaded research AND all Vector Database passes.** They are complementary, not interchangeable: Outlook holds what the user is sent, the deal folder holds what the user deliberately curated for this deal, and the Vector Database holds the firm's accumulated corpus — ArbJournal deal files, Chain Bridge Research merger reports, historical notes, internal arb research — that neither live channel surfaces. Skipping one silently drops research and biases the deal-handicapping, so the only acceptable reason to omit one is that it is genuinely inaccessible this run (Outlook not connected, no research files present in the Project, vector index unreachable) — and when that happens, name the skipped channel in the Section 7 data-limitations list rather than passing over it silently. If the user explicitly restricts the scan to a named channel, honor that and record which channels you were told to skip. Do not treat a clean overlap screen or a "low-risk-looking" deal as license to run fewer channels; the completeness of the sell-side read is exactly what tells you whether that first impression holds.

**The observed failure mode is treating one source as enough** — running the single Outlook MCP call, or skimming two of the uploaded PDFs, and calling the enrichment done. Counter this structurally, not just by intention: kick off all the scans in the same turn (the `outlook_email_search` call, the Project / deal-folder file enumeration, and the `semantic-search` passes) rather than finishing one and only then deciding whether there's room left for the rest. Sequential-by-convenience is how a channel goes from "run this run" to "ran zero times this week."

De-duplicate across channels by firm + date + thesis (the same note often arrives by email AND sits as a PDF in the deal folder AND is chunked in the vector index — collapse to one record, prefer the fuller copy, keep every channel tag), then attribute every surviving item by firm and date at each enrichment point.

### Channel attempt log — required before Phase 4 and before Phase 7

Treat "this channel ran" as something demonstrated, not assumed. Immediately before each enrichment point, produce a five-row table, always in this order, and carry it into the Section 7 data-limitations disclosure verbatim:

| Channel | Action taken | Result |
|---|---|---|
| Outlook | e.g. `outlook_email_search` called with query "..." | e.g. 14 notes found and read in full |
| Uploaded research (Project / deal folder) | e.g. Project file list enumerated; 9 research files identified | e.g. all 9 read in full |
| Vector DB — ArbJournal pass | e.g. `semantic-search` with the ArbJournal institution filter, queries "..." | e.g. 3 deal files harvested (titles, dates) |
| Vector DB — Chain Bridge pass | e.g. `semantic-search` with the Chain Bridge Research institution filter, queries "..." | e.g. 2 merger reports harvested (titles, dates) |
| Vector DB — broad pass | e.g. `semantic-search` ticker/sector queries "..." | e.g. 22 chunks across 11 documents read |

A channel earns a "not available" result only after a concrete action was actually taken and failed — an `outlook_email_search` that errored, a Project file enumeration that returned zero research files (and the user confirmed there are none to upload), a `semantic-search` call that failed or returned nothing on-point. Writing "not available" or "skipped" as a first move, without an action in the middle column, is not a valid log entry — go back and actually attempt the channel before finalizing the table.

### Read thoroughly — do not truncate for speed

The value of the sell-side read is in the specifics — which precedent an analyst cites, the exact review-track call, the one-line remedy thesis — and those live in the body of a note, not its subject or first paragraph. So read the research in full:

- **Outlook**: fetch the FULL body of every subject-line-matching note with `read_resource` (not just the metadata snippet), and page through the entire result set to exhaustion via `nextOffset`/`nextCursor` — do not stop at the first page. Open long forwarded chains all the way down to the original broker note. Reading every matching note end to end is the job; skimming headers is not a substitute.
- **Uploaded research**: enumerate the Project file list completely and read every research document end to end — including sector and peer notes that name neither party, which often carry exactly the market-size and share tables Phase 4 needs. Large PDFs are read in page batches until finished, not sampled.
- **Vector Database**: run each pass with several query angles and page deep enough that results go clearly off-topic before stopping. When a high-relevance document surfaces as a truncated chunk, pull its neighboring chunks rather than quoting from a fragment — do not cite a conclusion from chunk 3 of 21 without reading around it.

Never sample a subset of notes or truncate a note to save time or context. If the volume is genuinely large, keep reading and compress in your notes as you go (firm · date · thesis), but base that compression on having read each note in full. The only acceptable reason to leave research unread is that a channel is inaccessible — which is a stated limitation, not a shortcut. When a run is high-volume, say so in Section 7 and confirm you read the full set rather than a sample.

### The blind wall governs every channel

Sell-side deal notes routinely lead with the spread, price targets, and "deal math" — and the Vector Database is just as contaminated: internal arb research often opens with "the 2–3% spread offers attractive risk/reward," and ArbJournal / Chain Bridge Research coverage of a live deal carries spread views, entry-level framing, and downside estimates. Those are Phase 8 material, not blind fundamental input. While reading during Phases 4–7, extract ONLY the content permitted for the current enrichment point and quarantine everything price-shaped — do not carry a single price target, spread figure, or implied-probability call about the LIVE deal into Sections 1–7. (Historical precedents are different: a *closed* precedent deal's spread history, timeline, and outcome are precedent facts, not live pricing — fully usable in Phase 7.) If an item carries useful spread commentary on the live deal, note that it exists and return to it in the Tape Check, where analyst spread views may be cited alongside the live tape. Hold to this identically no matter which channel an item came from.

### Enrichment point 1 — Phase 4 (market structure)

Across the running channels — Outlook, the uploaded research, and the Vector Database passes (the broad pass plus anything the institution passes surfaced — Chain Bridge Research merger reports routinely quantify shares and HHI) — harvest market-size, market-share, patient-pool, penetration, and competitive-positioning estimates, plus analyst views on barriers to entry and competitive dynamics. This is the legitimate path to quantifying shares/HHI that EDGAR alone rarely permits: a named, dated estimate satisfies the sourcing rule *as an estimate* — present it labeled "analyst estimate" (or "internal research estimate" for vector-sourced internal work), with firm/publication and date, and note dispersion if sources disagree.

### Enrichment point 2 — Phase 7 (deal handicapping)

Across the running channels — Outlook, the uploaded research, and all Vector Database passes (the named-institution passes are at their most valuable here) — gather views on regulatory risk and expected review track (clean / second request), timeline expectations, precedent transactions cited, and remedy speculation. ArbJournal deal files are precedent gold: closed deals in the same sector or with the same regulatory shape, with dated review tracks, announcement-to-close day counts, remedy outcomes, and ArbJournal's own contemporaneous risk categorization. Chain Bridge Research merger reports add named-analyst review-track calls, remedy reads, and timeline projections on live and recent deals. Feed both into the Phase 7 precedent table and Table 9, cited inline from hit metadata. Incorporate live-deal views as attributed views in the completion assessment — but **stage-classify each completion-sentiment line first** (pre-announcement "will a deal happen" vs. post-announcement "will the signed deal close," per the anti-hallucination rules); only post-signing sentiment about closing the announced deal belongs in the completion view. SKIP price targets, spread commentary, and "deal math" on the live deal until Phase 8.

When compiling **Table 9 — Attributed Sell-Side Views on Completion** for Section 7, order the rows by firm priority — see `references/sellside-priority.md` for the fixed High/Medium/Low tier list and its tie-breaking rules — not by date, channel, or the order notes were collected. ArbJournal / Chain Bridge Research items and other non-broker vector-database sources get their own clearly-labeled block, placed after the ranked-firm rows and before unranked firms, attributed from hit metadata ("ArbJournal — [report title], [date]"; "Chain Bridge Research — [analysts], [report title], [date]").

### Uploaded research mechanics (deal folder / Claude Project)

The user curates this channel by hand before prompting the workflow — downloading the relevant broker notes and uploading them to the attached Claude Project (and/or placing them in the deal folder). That workflow has two consequences: the set is deliberate (a file the user bothered to upload is a file they want read — read ALL of it), and an empty set is probably an oversight, not a choice.

1. **Enumerate**: list the attached Claude Project's files, plus any conversation attachments and any connected deal-folder files. Research files are typically named "[YYYYMMDD] [Firm] [Ticker] [Title] [pages].pdf" — but don't rely on names alone; open anything plausibly research.
2. **Read every relevant document in full** — notes on the target, the acquirer, AND sector/peer notes (a tools-sector preview that names neither party often carries exactly the market-share table Phase 4 needs). For a large PDF, read in page batches to the end; never stop at the front section. Targeted project search is a supplement for follow-ups, never a substitute for the full reads.
3. **Extract per note into the shared schema** used by the Outlook channel — firm, analyst, date, channel = "Project upload (file name)", market-structure content, deal view, deferred-to-Phase-8 flag, one verbatim thesis line — see `references/outlook-research-scan.md` Step 3.
4. **De-dup** against Outlook copies of the same note; prefer the fuller copy (usually the uploaded PDF).
5. **If the Project contains no research files, ask the user before proceeding** — under their stated workflow the uploads come first, so absence usually means they forgot, and silently running without the channel produces a report built on a thinner Street read than they intended. Proceed without it only on their say-so, and log it in the attempt table.

### Vector Database passes (`MeteoraMCP:semantic-search`)

Two mandatory passes over the internal corpus (index `investment-team`, default namespace; the `MeteoraMCP-AWS` twin of the tool behaves identically if that server is the one connected). Kick both off in the same turn as the Outlook search and the Project enumeration, as soon as Phase 1 has fixed the parties' names — then return with targeted follow-up queries as Phases 2–4 and 7 surface specific competitor names and candidate precedents.

**Pass A — named institutions (one filtered search set per institution: ArbJournal, then Chain Bridge Research).** Metadata is not uniform across vintages, so each filter covers BOTH author fields, `Institution` and `author_institution`:

```json
{"$or": [{"author_institution": {"$eq": "ArbJournal"}}, {"institution": {"$eq": "ArbJournal"}}]}
```

```json
{"$or": [{"author_institution": {"$in": ["Chain Bridge Research", "ChainBridge"]}}, {"institution": {"$in": ["Chain Bridge Research", "ChainBridge"]}}]}
```

(The verified institution string in the index is "Chain Bridge Research"; the `$in` keeps the shorthand spelling covered too.) **ArbJournal** documents are deal files: terms, conditions, regulatory timelines, antitrust analyses, critical paths, and outcomes. **Chain Bridge Research** documents are event-driven merger reports with named analysts: regulatory-risk analysis with market-share/HHI estimates, review-track and second-request calls, remedy reads, timeline projections, and downside estimates.

Run each filter with several queries: "[target] [acquirer] merger", the target and acquirer names individually, the sector plus "merger"/"acquisition", and structure-matched queries ("second request [sector]", "CFIUS review", "going-private consortium"). Harvest three distinct things: (1) any coverage of THIS deal or these parties; (2) precedent deal files and reports in the same sector or with the same regulatory shape — review track, announcement-to-close day count, remedy outcome, and the publication's contemporaneous risk categorization (→ Phase 7); (3) market-structure estimates — Chain Bridge merger reports routinely quantify shares and HHI (→ Phase 4). Anything price-shaped about the live deal (spread views, entry levels, downside estimates) is quarantined to Phase 8 like every other channel's spread content.

**Pass B — broad deal-context.** No author restriction. Sweep for whatever the corpus holds on: the target and the acquirer as companies (profiles, initiations, transcripts, desk notes); market-size and market-share estimates for the overlapping lines; the competitors named in Phases 2–3; precedent transactions in the same sector; regulatory/enforcement history in the space. Pin company-specific queries with the four-field ticker filter —

```json
{"$or": [{"primary_ticker": {"$eq": "TICK"}}, {"secondary_tickers": {"$eq": "TICK"}}, {"folder_ticker_1": {"$eq": "TICK"}}, {"folder_ticker_2": {"$eq": "TICK"}}]}
```

— and run unfiltered semantic queries alongside, because sector notes and internal research folders (e.g. per-deal "Arb Research" folders) often carry no ticker metadata. Route market-structure material to Phase 4, precedents and handicapping views to Phase 7, and footprint corroboration to Phases 2–3 — corroboration only: EDGAR remains the verbatim source for competitor lists and segment tables.

**Inline citation from hit metadata — mandatory for every vector-sourced claim.** Each `semantic-search` hit returns its citation with it; build the inline cite at the point of use from the metadata fields on the hit: `report_title` (fall back to `source` / `file_name`), `institution` / `author_institution`, `author` / `analyst_names` where present, and `publication_date` (fall back to the folder path + gdrive date when publication metadata is empty). Examples: (ArbJournal — "1Life Healthcare / Amazon Cash Merger – ArbJournal Deal File", 2022-07-21); (Chain Bridge Research — Zsombor Nagy et al., "Altair Engineering (ALTR) / Siemens (SIE GR)", 2024-11-08); (internal research — "Cidara_Merck_Merger_Analysis", /Interns/CDTX/Arb Research, 2025-11-14). Do not cite from memory of the search, do not attribute a chunk's claim to a vaguely-recalled document, and never blend vector-sourced claims with filed data — if a metadata field is empty, cite what the metadata does provide rather than inventing the rest. Multi-chunk documents are cited once per document, not per chunk — and read the neighboring chunks before relying on any single chunk's claim.

### If a channel is unavailable

State which channels ran and which did not, using the Channel Attempt Log above as the source of truth rather than a fresh unsupported claim (Outlook not connected; zero research files in the Project — ask the user first, per the mechanics above; vector index unreachable). Missing channels widen the data-limitation disclosure in Section 7 but do not block the report — proceed with whatever ran, and never fabricate a broker view to fill the gap. If the attempt log shows a channel was never actually attempted, that is not the same thing as "unavailable" — go attempt it before writing the report.


## Workflow

Work through the phases in order. Each phase produces a section of the final report; the report template is in `references/report-template.md` — read it before composing the final output so section order and required tables match exactly.

### Phase 0 — Deal-status pre-check (before any other work)

Confirm the deal is still **pending**. One web search ("[target] [acquirer] merger status") or a scan of the target's most recent 8-Ks answers it. Deals that have already closed, been terminated, or been abandoned invalidate the entire workflow — the blind wall, the tape check, everything. If the deal is not pending, tell the user immediately and ask whether they want a retrospective instead; do not silently run the live-deal workflow on a dead deal. (This check exists because it has been skipped, at the cost of full ingestion passes on closed transactions.)

While here, also capture the live regulatory posture: HSR filing date, any pull-and-refile, Second Request, agency complaint, foreign-regime milestones, S-4 effectiveness, shareholder vote result. These dates anchor Phase 7's timeline scenarios and Phase 8's spread-evolution table.

### Phase 1 — Deal ingestion

Pull the primary deal documents — the **announcement 8-K with its exhibits (press release + investor deck)**, the **merger agreement**, and the **proxy** (DEFM14A / PREM14A / S-4 if stock consideration) — from EDGAR, and pull the **press release and investor deck from the acquirer's IR website** as well (see the dedicated block below; the website copy sometimes posts before the 8-K and the microsite deck can be richer than the furnished PDF). Extract from the agreement and proxy:

- Purchase price and consideration type; premium vs. unaffected price **as disclosed in the proxy or announcement** (do not compute premium from live prices — that would require pulling the tape). If the deal is announced with proration: the cash amount per share, the exchange ratio, the cash/stock proration percentages, and the reference price/VWAP window that set the ratio — Phase 8's blended-consideration calculation needs all four.
- Financing structure: committed debt/equity amounts, financing sources, any financing condition
- Acquirer entity, its ultimate parent, and ownership/equity rollover structure; **insider election/rollover terms** (e.g., a CEO electing all stock, board seats granted at close) — these shift proration capacity to other holders and signal insider conviction
- Termination fees (both directions) with their **exact trigger mechanics** — tail periods, Acquisition Proposal thresholds (50% vs. 20%), whether the reverse fee is antitrust-specific, sole-remedy/liquidated-damages language, interaction with specific performance. A reverse fee well above the conventional 3–4% of EV is itself evidence of negotiated antitrust risk.
- Regulatory efforts covenant strength, read clause by clause: "reasonable best efforts" vs. "hell-or-high-water"; **divestiture-cap-by-schedule constructs** ("except as set forth on Section X of the Parent Disclosure Schedule" — a pre-agreed, confidential remedy basket, materially different from either unlimited or zero commitment); litigation commitments (defend through final non-appealable judgment vs. weaker); **remedy-proffer clocks** (e.g., "proffer no later than N months from HSR filing" — compute the calendar date and carry it into every timeline scenario); pull-and-refile rights and their caps
- **Interim acquisition standstills**: covenants barring either party from acquiring in named product spaces during pendency. Quote them verbatim — the named spaces are the parties' own lawyers' map of the competitively sensitive markets, and the single best market-definition evidence available in Phase 4.
- Outside date and extension mechanics — the initial date, who can extend, increment length, the maximum date, and the condition (typically: only regulatory conditions unsatisfied). Verify in the agreement's termination article; never assume.
- Required approvals: HSR, non-US regimes (EC, UK CMA, China SAMR, etc. — infer from geographic footprint found later, revisit after Phase 3), CFIUS exposure, shareholder vote threshold
- MAC definition and carve-outs
- Dividend/distribution policy during pendency
- Advisors on both sides (financial and legal) — a top-tier antitrust firm on the acquirer's side is a data point

The regulatory efforts covenant and reverse termination fee are the deal's own confession of how much antitrust risk the parties negotiated around — read them closely. Where the merger agreement is a single large exhibit, locate the efforts covenant and termination article by searching for section-heading anchors ("Efforts", "Termination", "Outside Date", "Company Termination Fee") rather than reading linearly.

#### Press release and investor deck (acquirer IR site + 8-K Ex-99.x)

The press release and investor deck are the parties' own framing of the deal, and they carry completion-relevant content the merger agreement never spells out. Both are usually available within hours of announcement — on EDGAR as 8-K exhibits (press release Ex-99.1; deck *furnished* Ex-99.1/99.2 under Item 7.01 — do not skip furnished exhibits, the deck is where the substance sits) and on the acquirer's IR website (newsroom page + an "Events & Presentations" page or a deal microsite), often mirrored on the target's site. Pull both routes. These are dated at announcement, so they live inside the blind wall: read them in Phases 1–7 and use the disclosed premium and the deck's own numbers freely — the wall bars only *live* trading levels, which these documents don't contain.

Extract and route each item to the phase that uses it:

- **Stated strategic rationale** — the parties' theory of the deal. For strategics it doubles as the regulators' read on why the combination matters (→ Section 2 rationale; feeds Phase 4).
- **Synergy targets and their basis** — the cost/revenue synergy figures and, critically, *how* they are framed. Synergies built on capacity rationalization, plant consolidation, or pricing / go-to-market overlap are admissions of horizontal proximity (→ Phase 4 synergy-claim exposure).
- **Self-drawn combined market position** — any slide mapping the pro-forma combined footprint, share, rank, or "#1/#2 in X" positioning. A company mapping its own combined share is unusually strong market-definition and overlap evidence — capture it verbatim with the slide number cited (→ Phase 4).
- **Expected close timing and required approvals** — the announced target close ("expected to close in [period]") and the approvals list ("subject to HSR / regulatory approvals and customary conditions"). Record these as the *parties' stated* timeline, distinct from your independent scenario build (→ Phase 0 posture and Phase 7 timeline scenarios).
- **Financing and pro-forma leverage** — any financing description, committed-facility mention, or pro-forma net-leverage slide, cross-checked against the agreement's financing terms and the filings (→ Phase 5).
- **Pro-forma ownership / governance** — combined ownership split, board composition, named management (→ Section 1 insider/rollover, Section 3 stakeholder analysis).
- **Divestiture or remedy commitments pre-announced** — occasionally the release flags a planned divestiture up front; that is a strong signal the parties already see an overlap problem (→ Phase 4 remedy analysis).

If neither the 8-K exhibits nor the IR site has a deck yet (common in the first hours, and for some financial-sponsor take-privates that issue only a short release), say so and proceed — note it as a data limitation and revisit once furnished.

### Phase 1.5 — Buyer classification

Classify the buyer from evidence, not from the deal's press framing. Determine from the merger agreement's acquirer entity, its ultimate parent, equity commitment letters, and guarantor disclosures:

- **Financial sponsor**: acquisition vehicle ultimately controlled by a PE fund, family office, or other financial buyer with a portfolio of holdings. The competitive entity is the *portfolio*, which must be discovered and mapped.
- **Strategic**: an operating company acquiring in or adjacent to its own business. The competitive entity is the acquirer itself, visible in its consolidated filings.
- **Hybrid / consortium**: PE-backed strategic platforms doing add-ons, sponsor + strategic co-investor consortia, strategics acquiring through financial vehicles. Run BOTH branches, attributing each overlap to the parent that creates it.

State the classification in the report with the evidence supporting it (entity names, commitment letter parties, cited). This is genuinely informative output, not just routing: regulators treat serial sponsor roll-ups and direct horizontal strategic mergers under different lenses.

The classification selects the reference file for Phases 2–3:
- Financial sponsor → read `references/pe-buyer.md`
- Strategic → read `references/strategic-buyer.md`
- Hybrid/consortium → read both; execute both branches

### Phases 2–3 — Buyer competitive footprint and overlap screen (branched)

Execute per the selected reference file. Both branches produce the same two deliverables so downstream phases are buyer-agnostic:

1. **Acquirer Competitive Footprint table** — what the buyer side owns/operates that could overlap with the target (portfolio companies for sponsors; own segments and business lines for strategics; both, attributed, for hybrids), with verification sources.
2. **Overlap Screen table** — each footprint element crossed against the target's product/service lines and geographies, classified as horizontal / vertical / adjacent / potential-competition / none, with evidence citations.

**Gate:** If the screen is clean — no horizontal or vertical overlaps and no concerning acquisition pattern — Phase 4 collapses to a short paragraph stating that and why, with the overlap table as evidence. Do not manufacture depth where none is warranted. If overlaps exist, run Phase 4 in full for each overlapping line.

Also finalize the list of likely regulatory regimes now that geographic footprints are known.

### Phase 4 — Deep competitive effects (conditional on overlaps)

For each flagged overlap:

- **Market definition**: define relevant product and geographic markets; apply the hypothetical monopolist test qualitatively. Quantify shares/HHI ONLY if both revenue and total market size come from citable sources; otherwise state the limitation. Run **sell-side enrichment point 1** here across the running channels — Outlook, the uploaded deal-folder research, and the Vector Database broad pass (see "Sell-side enrichment") — named analyst estimates of market size/share are citable when labeled as estimates with firm/publication and date.
- **Competitor extraction**: reproduce verbatim the Competition-section competitor lists from the target's and each overlapping buyer-side entity's latest 10-K/10-Q (portfolio company filings for sponsors; the acquirer's own filing for strategics), with citations. Cross-reference to identify common competitors. Assess likely responses of third-party competitors.
- **Geographic revenue tables**: extract segment/geographic revenue tables from EDGAR for target and overlapping buyer-side entities, standardize the regional categories, and present a combined-entity comparison table. Flag high-concentration regions and note year-over-year geographic expansion trends.
- **Theories of harm**: work through horizontal overlap, vertical foreclosure, potential competition, conglomerate effects, innovation/dynamic competition, and buyer-power/monopsony — plus the buyer-type-specific angles listed in the selected reference file (e.g., roll-up seriality and cross-portfolio bundling for sponsors; entrenchment and killer-acquisition theories for strategics).
- **Remedy analysis**: qualitatively assess remedy likelihood and identify concrete divestiture candidates (which asset, why it would satisfy the concern) in text or table form.
- **Barriers to entry** in each affected market.

### Phase 5 — Target financial health

A financially shaky target raises financing-failure and MAC risk even when antitrust is clean. From the most recent 10-K/10-Q:

- Capital structure: total debt, key instruments, maturities schedule
- Leverage metrics (Net Debt/EBITDA, interest coverage) — computed only from figures in the filings, with the inputs cited
- Liquidity: cash, revolver availability, near-term maturities
- Covenant compliance, waivers, amendments
- Going-concern language, audit qualifications, distress indicators
- FCF profile: operating cash flow, capex, trend
- Recent financing activity; dividend/buyback sustainability vs. FCF

For strategic buyers paying cash or stock without committed financing, also assess the acquirer's balance-sheet capacity per `references/strategic-buyer.md`.

### Phase 6 — Litigation and fraud screen

For both target and bidder:

- Legal proceedings disclosures from 10-K/10-Q/8-K, with estimated exposure as disclosed
- Regulatory investigations or enforcement actions in filings
- Fraud allegations, restatements, internal investigations
- Web search for short-seller reports or public fraud allegations on either party — cite by publisher and date
- Deal-specific litigation: merger objection suits, fiduciary claims, appraisal actions
- Assessment: could any of this constitute a closing impediment or MAC trigger?

### Phase 7 — Blind synthesis

Compose the full report per `references/report-template.md`, WITHOUT any market pricing data. The synthesis must include:

- A qualitative completion assessment grounded in named precedent transactions — comparable deals matched on BUYER TYPE and overlap profile (PE roll-up precedents for sponsor deals; horizontal strategic merger precedents for strategic deals), their outcomes, timelines, and remedies — cite each precedent. The Vector Database named-institution passes are first-class precedent sources here: closed ArbJournal deal files carry the review track, announcement-to-close day count, and outcome, and Chain Bridge Research merger reports carry contemporaneous regulatory reads on comparable deals — cite each inline from hit metadata (title, institution, analysts, publication date). Build the precedent table to the **Table 8 discipline** in `references/report-template.md`: one deal per row, a specific announce→close day count and outcome per row, comparable precedents only (no non-comparable "contrast" rows), and drop any row whose specifics you can't source (prefer ArbJournal for review track / day count / outcome; the parties' completion 8-Ks/press releases for the dates)
- **Sell-side enrichment point 2** across the running channels — Outlook, the uploaded deal-folder research, and all Vector Database passes (see "Sell-side enrichment"): attributed views on regulatory track, timeline, precedents, and remedies — de-duplicated across channels and extracted with the blind wall intact (no price targets or spread commentary on the live deal until Phase 8)
- Expected timeline scenarios (clean HSR clearance vs. second request vs. litigation) tied to the outside date and covenant strength from Phase 1
- Explicit statement of data limitations encountered

Finish writing this section completely before touching any pricing tool. The blind view is the deliverable; the tape check is the overlay.

### Phase 8 — Tape Check (only after Phase 7 is written)

Now, and only now, pull live pricing:

- Current price, bid/ask, volume, market cap for the target and (if stock/mixed consideration) the acquirer (`get-price`); deal consideration from Phase 1. Derive the share count from market cap ÷ price and cross-check aggregate cash against the announced cash component.
- **Gross spread** = consideration − current price; spread %. **Proration applies only when the deal is announced to be prorated as part of the transaction** (fixed aggregate cash/stock split disclosed in the announcement or merger agreement). When it is, the blended per-share consideration = **(cash proration % × cash per share) + (stock proration % × exchange ratio × acquirer price)** — e.g., a 73% cash / 27% stock proration with $374 cash and a 3.8721 ratio gives 0.73 × 374 + 0.27 × 3.8721 × acquirer price. The cash leg is fixed; the stock leg floats with the acquirer. State both legs, then the blend, and spread the target against the blend. For deals without announced proration (all-cash, fixed per-share cash-and-stock, or election deals with no proration), spread against the stated consideration directly.
- **Proration side-effects** (when the acquirer's price has moved materially since signing): a large acquirer decline raises the real dilution of the fixed-ratio share issuance and the pricing of any debt raise — flag for the financing-risk discussion even where the contract leaves financing risk with the acquirer. Verify against the tape that the target actually trades on the consideration value the election model implies.
- **Spread evolution through milestones (required table)**: pull daily closes since announcement (`get-price` with start/end dates) and tabulate the spread at each Phase-0 milestone (announcement, HSR filing, second request, S-4 effectiveness, vote, today) — for prorated deals, recompute the blended consideration at each date using the same proration formula. Whether the spread widened or kept compressing through adverse-looking milestones (a second request, an agency complaint) is the single most informative datum the tape offers: compression through a second request means the market graded it as process, not peril. Also flag any large unexplained single-day move in either stock (report it; investigating it is optional and a stated limitation if skipped).
- **Annualized return** at the Phase-7 fundamental timeline scenarios (show each scenario with day counts)
- **Downside anchor**: unaffected pre-announcement price pulled from the tape with the date cited (`get-intraday-bars` or historical close). Do not guess the downside — source it and state the date.
- **Market-implied completion probability** = (current − downside) / (consideration − downside), presented explicitly as a function of the stated downside assumption, not as a bare number. For prorated deals, "consideration" here is the blended consideration from the proration formula above. **Stale-anchor sensitivity is mandatory when the market or the acquirer has moved materially since announcement**: the pre-announcement close stops being a valid standalone estimate, and the naive formula then understates implied probability, sometimes wildly (e.g., a naive 65% that becomes ~97% at a sector-marked-down standalone). Present the naive number, name why the anchor is stale, and show the calculation again at at least one explicitly-labeled marked-down illustrative downside. In the regulatory tail, net any antitrust reverse fee (per share) against the gap-down.
- Spread history since announcement if informative beyond the milestone table: is the target trading through the deal price (topping-bid speculation)? Has the deal functioned as downside insurance (target's move vs. acquirer's move over the identical span)?
- Sell-side spread/price-target commentary deferred from Phase 7 may now be cited (firm, date) alongside the live tape
- **Reconciliation paragraph**: does the tape agree with the blind fundamental view? If they diverge, which side has the better argument and why? Divergence is the payoff of the whole exercise — surface it prominently, don't smooth it over.

## Output

**Default deliverable: a `.docx`.** Build the report as a Word document via the docx skill, following the **Document format** section at the top of `references/report-template.md`, then present the file. Section order and required tables still follow `references/report-template.md` exactly; no charts. The governing rule from that Document format section: **skimmable is a formatting property, not a length property** — restructure with a verdict callout, bold lead-in takeaways, and detail-in-tables, but omit nothing. After building, verify completeness mechanically (render to PDF, `pdftotext`, grep for a checklist of facts that only appear in the full analysis — names, exact vote counts, clause cites, single-source estimates) rather than trusting that condensation preserved everything. The blind-then-tape wall holds in the document exactly as in the analysis: Sections 1–7 carry no market pricing; the Tape Check is Section 8.

Deliver in chat as text and tables instead (no document) only when the user explicitly asks for it — e.g., "in chat", "inline", "just show me", "don't make a doc", "text only". The in-chat version is the same content with the same `references/report-template.md` section order and tables; it simply skips the docx build and its verification step.

If any required input is missing (e.g., merger agreement not yet filed, sponsor portfolio opaque), state exactly what is missing and what it prevents, then deliver the rest — in whichever format applies.

**Then write the memory doc — automatically, as the final step of every assessment.** After delivering the report, invoke the `merger-arb-memory` skill without waiting to be asked: **Seed Mode** when the deal has no doc yet (the report distills directly into its seed pillars, blind-view vs. Tape Check labels preserved), **Update Mode** when a doc already exists (append the report as a `diligence` entry and refresh the summary). State in the closing chat receipt which mode ran and the doc name. Skip only when the user said this run is report-only ("just the report", "don't write the doc") — and then say the doc step was skipped. The report is the point-in-time deliverable; the memory doc is where the view lives between assessments, and an assessment that never lands in the doc is knowledge the next session can't read.
