---
name: "deal-risk-core"
description: "Fast, single-pass M&A deal-completion risk assessment producing a verdict-bearing report — Risk Matrix, HIGH/MODERATE/LOW ratings, buyer classification, Deal Completion Probability Decomposition — in Meteora's gold-standard 12-section format (e.g. the CBZ/Grant Thornton and ZYME/TBPH reports), targeting ~10 minutes. Trigger on \"run the core deal risk assessment on [TICKER]\", \"quick full report on [deal]\", \"give me the CBZ-format read\", or when deal-risk-assessment's Outlook/Claude-Project sweep and Tape Check would blow a tight time budget. Sourced from EDGAR plus ONE ArbJournal and ONE Chain Bridge Research vector pass — no Outlook, no Project research, no live Tape Check. Sibling to arb-deal-antitrust-initial (extraction-only, never a verdict) and deal-risk-assessment (the complete, slower version). Use this one when the ask is \"that CBZ-style report, fast.\""
---


# M&A Deal Risk — Core Assessment (fast, single-pass, verdict-bearing)

Produce an institutional M&A deal-completion risk assessment — buyer-classified, antitrust-centered,
ending in an explicit HIGH/MODERATE/LOW completion verdict — in roughly 10 minutes and one `.docx`.
This is the skill that reproduces the CBZ/Grant Thornton and ZYME/TBPH "gold standard" report format:
a front-matter parameter table ending in an Overall Completion Assessment, a Section 1 Risk Matrix,
and a Section 11 Deal Completion Probability Decomposition ending in a Composite Completion
Assessment line.

## Where this sits relative to its siblings

- **arb-deal-antitrust-initial** is extraction-only by charter — it never renders a verdict, a Risk
  Matrix, or a completion probability, and explicitly forbids characterizing any term as favorable,
  tight, or unusual. Do not reach for it when the ask is a verdict-bearing report — it structurally
  cannot produce one. Use it only when the ask is genuinely "just the facts, no view."
- **deal-risk-assessment** is the complete version of this same report: it additionally runs an
  Outlook mailbox sweep AND a Claude Project research-file enumeration (each read to exhaustion, not
  sampled) AND two full passes of the ArbJournal/Chain Bridge Research vector index (once for market
  structure, once for precedents) AND a mandatory Phase 8 Tape Check against live Bloomberg pricing,
  with Table 9 sorted by a fixed broker-tier priority list. That thoroughness is the point of the full
  report, and it is also why it routinely runs well past 10 minutes.
- **This skill (deal-risk-core)** keeps the same buyer-classification logic, the same section order,
  the same tables, and the same anti-hallucination discipline as deal-risk-assessment, but sources
  sell-side/precedent content from ONE ArbJournal pass and ONE Chain Bridge Research pass (not two of
  each), skips Outlook and Claude Project entirely, and skips the Tape Check. If, mid-run, the user
  asks for the Outlook sweep, the Project research, or a live spread check, that is a signal to switch
  to deal-risk-assessment rather than bolting those channels onto this skill.

## Anti-hallucination rules (apply in every phase — non-negotiable, unchanged from the full skill)

- **Never estimate, calculate, or invent market shares, HHI figures, or probability percentages
  without explicit source data.** State the limitation instead of estimating.
- **Cite every fact and figure to a specific source** — EDGAR filing (form type + filing date,
  accession number), named report, or news article with outlet and date. Every table names its
  source in the caption or a per-row source column; a number that lives only in a table with no
  visible source is unauditable.
- **Competitor lists and geographic revenue breakdowns must come verbatim from EDGAR filings**
  (10-K/10-Q Competition sections and segment tables). Quote or reproduce them; don't paraphrase.
- **Distinguish sourced facts from analytical opinion.** Label opinions "Assessment:" or "Meteora
  read:" so they're never confused with sourced fact.
- **Closing-probability language is qualitative and precedent-based only.** Ground any completion
  characterization in named historical precedent transactions (deal, year, outcome, day count).
  Never emit a bare percentage from intuition.
- **Stage-classify completion sentiment.** Pre-announcement "will they agree to a deal" chatter is
  not a read on whether the *signed* deal will close — date-stamp sentiment and only carry
  post-signing "will this deal close" views into the completion assessment.
- **Buyer footprint mappings**: verify via EDGAR and sponsor/issuer disclosures; note minority stakes
  explicitly; flag anything unverifiable as unverified rather than dropping it.

## Tools

- **EDGAR**: `edgar-filings`, `edgar-filing-index`, `edgar-filing-text` (`summary=true` for a
  table-of-contents-with-offsets on any large exhibit — this is how the merger agreement's efforts
  covenant and termination article get located without reading the whole document; `section=` to
  pull a 10-K item whole), `edgar-company-facts`, `edgar-ownership-search`. If a full-document pull
  exceeds the token cap, re-request with `summary=true` first, then slice by `offset`/`max_chars`.
- **Acquirer/target IR site**: `web_fetch` for the press release and investor deck (also filed as
  8-K exhibits — press release Ex-99.1, deck furnished Ex-99.1/99.2 under Item 7.01, don't skip
  furnished exhibits). If the page is client-rendered and returns an empty shell, use the
  `claude-in-chrome` tools instead.
- **Web search**: only when the buyer's identity or portfolio isn't resolvable from the filing or
  release within a minute of looking (e.g., a private PE sponsor's own portfolio page).
- **Vector Database** (`semantic-search` on the `investment-team` index, or the equivalent
  Meteora-MCP tool): ONE institution-filtered pass for ArbJournal, ONE for Chain Bridge Research, run
  in the same turn as the EDGAR pulls, not after them. Query with the target/acquirer names, the
  sector, and structure-matched terms ("second request [sector]", "going-private", "roll-up").
  Harvest both market-structure estimates AND precedent deal outcomes from these two passes — do not
  run a second round for each purpose the way the full skill does.
- **Do NOT** call Bloomberg or any live-pricing tool (`get-price`, `get-vwap`, `get-intraday-bars`,
  etc.) — there is no Tape Check in this skill.
- **Do NOT** run an Outlook mailbox search or enumerate a Claude Project's uploaded research files —
  those channels belong to deal-risk-assessment. If the user has uploaded broker notes and clearly
  wants them used, tell them this skill doesn't read that channel and offer to run deal-risk-assessment
  instead, rather than silently absorbing the scope.

## Workflow

Fire independent read streams in the same turn wherever possible — the 8-K package, the merger
agreement's anchored lookups, the target 10-K/10-Q, and the two vector-DB passes are four
independent streams; starting one only after finishing another is the serialization that blows the
time budget.

### Phase 0 — Deal-status pre-check

One web search or a scan of the target's most recent 8-Ks confirms the deal is still pending (not
closed, terminated, or abandoned). Capture whatever regulatory posture is already stated (expected
close quarter, "subject to HSR and customary conditions," shareholder vote required).

### Phase 1 — Deal ingestion

Pull the announcement 8-K with exhibits (press release + deck) and the merger agreement from EDGAR.
Extract:

- Purchase price, consideration type, disclosed premium (with its citation and stated basis — a
  30-day VWAP premium and a close-to-close premium are different numbers; report the one the issuer
  used, labeled as such)
- Financing: committed amounts, sources, financing condition (y/n)
- Acquirer entity, ultimate parent, guarantor
- Termination fees both directions, with trigger mechanics (tail period, go-shop/Excluded-Party
  reduced fee, antitrust-specificity, sole-remedy language)
- Regulatory efforts covenant — quote the operative phrase (e.g. "reasonable best efforts," any
  divestiture-cap-by-schedule carve-out, sponsor/portfolio-company carve-outs)
- Outside date and extension mechanics
- Required approvals (HSR, foreign regimes, CFIUS exposure, shareholder vote threshold)
- MAC/MAE definition highlights and carve-outs
- Advisors, both sides
- Go-shop end date AND the later Excluded-Party tail date if one exists — state both
- Expected closing timeframe as stated by the parties

Use `edgar-filing-text` with `summary=true` on the merger agreement exhibit to find the efforts
covenant, termination article, and outside-date clause by section heading rather than reading
linearly.

### Phase 1.5 — Buyer classification

Classify from the acquisition vehicle, ultimate parent, and equity commitment letter parties — not
from the deal's press framing:

- **Financial sponsor**: acquisition vehicle controlled by a PE fund/family office. The competitive
  entity is the *portfolio*, which must be discovered: enumerate current majority AND minority
  stakes (portfolio company EDGAR filings, the sponsor's own site, press/PE-database coverage where
  EDGAR doesn't reach), historical exits in the target's sector, sponsor regulatory history (prior
  FTC/DOJ/EC reviews, consent decrees), and whether the target is a new platform or an add-on. Assess
  **roll-up seriality** — count sponsor acquisitions in the sector over 5–10 years; a long add-on
  chain is itself a risk factor regardless of this deal's standalone overlap. Flag minority stakes in
  competitors explicitly — common-ownership/interlock theories don't require control.
- **Strategic**: an operating company acquiring in or near its own business. The acquirer's own
  10-K/10-Q substitutes for portfolio mapping: pull its segment structure and revenue, its verbatim
  Competition-section competitor list (check immediately whether the target appears on it or vice
  versa — a named-competitor merger is the strongest overlap signal available), its geographic
  revenue breakdown, its M&A history in the sector, and its own regulatory history.
- **Hybrid**: an operating acquirer funded/controlled by a sponsor (e.g., a PE-backed platform doing
  an add-on), or a sponsor-plus-strategic consortium. Run both branches above, attributing each
  footprint element to the parent that creates it. State explicitly which entity carries the
  competitive footprint and which carries the money — this is itself informative (a Limited Guarantee
  given by the operating entity rather than the sponsor, for instance, is evidence of a sponsor-backed
  strategic acquisition rather than a pure financial take-private).

State the classification with the entity-level evidence supporting it. This is genuinely
load-bearing output, not just routing — regulators treat serial sponsor roll-ups and direct
horizontal strategic mergers under different lenses, and Section 4 of the report leads with this
classification by name (e.g. "Buyer classification: HYBRID").

### Phases 2–3 — Overlap screen

Cross every footprint element (portfolio companies for sponsors; segments/business lines for
strategics; both, attributed, for hybrids) against the target's product/service lines and
geographies. Classify each: direct horizontal / vertical (specify direction) / adjacent-complementary
/ potential future competition / none, with an evidence citation for each. For a strategic buyer,
state explicitly whether each party names the other as a competitor in its own filings — if yes, the
horizontal case is largely made by the parties' own disclosures.

**Gate**: if the screen is clean, Section 6 (Competitive Effects) collapses to a short paragraph
stating that and why, with the overlap table as evidence. Don't manufacture depth where none exists.

### Phase 4 — Market definition and competitive effects (conditional on overlaps)

For each flagged overlap:

- Define the relevant product and geographic market from the target's own 10-K Competition-section
  language (quote it verbatim — a target that says only it competes with "global, national, and
  local firms" is telling you the market is fragmented, and that is itself a finding).
- Quantify shares/HHI ONLY when both a revenue figure and a total-market-size figure are citable
  (a filed number or a named, dated market-research estimate pulled from the ArbJournal/Chain Bridge
  passes or a general web search, labeled "estimate," with dispersion noted if sources disagree).
  Otherwise state the limitation explicitly rather than estimating.
- Capture any **self-drawn combined market position** from the investor deck (pro-forma share, rank,
  "#1/#2 in X") verbatim with the slide cited — a company's own combined-share framing is unusually
  strong overlap evidence.
- Work through the standard theories of harm (horizontal unilateral effects, vertical foreclosure,
  potential competition, conglomerate/cross-selling, innovation/dynamic effects, buyer power) plus
  the buyer-type-specific ones: **roll-up seriality and cross-portfolio bundling/common-ownership
  interlocks** for sponsors; **coordinated effects and killer-acquisition/entrenchment** for
  strategics.
- Note barriers to entry and, qualitatively, remedy likelihood and any concrete divestiture
  candidates.

### Phase 5 — Target financial health

From the most recent 10-K/10-Q: capital structure and key debt instruments with maturities, leverage
metrics computed only from cited filing figures, liquidity (cash, revolver availability), covenant
compliance/waivers, going-concern or audit-qualification language, free-cash-flow profile, and recent
financing activity. For a strategic buyer without fully committed financing, also assess acquirer
balance-sheet capacity against the cash consideration.

### Phase 6 — Litigation and fraud screen

For both target and acquirer: legal-proceedings disclosures from the 10-K/10-Q/8-K with any disclosed
exposure estimate, regulatory investigations or enforcement history, fraud allegations or
restatements, a web search for short-seller reports or public fraud allegations (cite publisher and
date, or state "none identified" as a search-limitation, not a clean-record finding), and any
deal-specific litigation (merger-objection suits, appraisal actions — typically absent until after
the preliminary proxy files). Assess explicitly whether anything here could be a closing impediment or
trip the MAE/MAC test — and if a compliance disclosure was made concurrently with signing, note that
it may fall outside an MAE test that only captures changes *after* signing.

### Phase 7 — Precedent synthesis and completion verdict

Run the ArbJournal and Chain Bridge Research vector passes now if not already fired in Phase 1 (they
should have been — fire them alongside the EDGAR pulls, not after). Build a precedent table: 3–6 rows,
matched on **buyer type and overlap profile**, each with a specific announce→close day count and
outcome (never a vague "months" or "fast") and the sourcing institution/date. Prefer the closest,
most probative precedent explicitly (e.g., the same acquirer's own prior comparable deal) over a
larger set of looser analogs.

Compose the completion verdict — HIGH / MODERATE / LOW, never a bare percentage — as a decomposition
across independent components: antitrust/regulatory clearance, financing availability, no-MAC/target
stability, shareholder approval, and absence of deal-blocking litigation. State the composite
assessment and name the specific items still worth monitoring (a common-ownership overlap left
contractually unaddressed, a marketing-period timing mechanic, an unresolved compliance matter) —
these "MONITOR" items are what separate a considered HIGH from a blank one.

Since there is no Tape Check in this skill, do not compute or imply a market-implied probability, and
do not pull or reference live trading levels anywhere in the report — note in Section 12 that no live
pricing was reviewed, as a stated scope limitation, and point the user to deal-risk-assessment if they
want that reconciliation.

## Report structure — lock this section order exactly

**Front matter** (before Section 1): a parameter table — Transaction | Consideration | Announced |
Target structure | Acquirer structure | Expected close | **Overall completion assessment** (HIGH /
MODERATE / LOW, bolded) — followed by one italic disclaimer line ("Prepared as internal investment
research... not investment, legal, or tax advice... see Section 12") and the report date.

1. **Executive Summary & Deal Completion Risk Matrix** — 2–3 paragraphs of narrative synthesis, then
   a Risk Matrix table: Risk Factor | Assessment (LOW/LOW-MODERATE/MODERATE/HIGH) | Rationale, one
   row per factor (antitrust/HSR, financing certainty, MAE, deal litigation, shareholder approval,
   any common-ownership/structural flag, any mechanical timing risk), ending in an
   **OVERALL COMPLETION PROBABILITY** row. Source line beneath the table.
2. **Deal Structure and Terms** — a Term|Detail table covering everything extracted in Phase 1, then
   an **Advisors** list, then a **Process & governance signals** subsection (board approval
   unanimity, go-shop mechanics, retention/change-in-control programs — these bear on completion,
   not just terms).
3. **Target Financial Analysis** — capital structure & liquidity table, most recent quarter results
   table if released alongside the deal, segment/geographic revenue tables, one "Meteora read" line
   connecting the financial picture to the completion question (e.g., a decelerating business
   explains board acceptance of a premium).
4. **Acquirer Profile & Financing Capacity** — open with **"Buyer classification: [TYPE]."** stated
   plainly, then the entity/platform background, the sponsor's or acquirer's relevant portfolio/
   segment table, and a financing-structure paragraph ending in a labeled **"Structural read
   (Meteora):"** paragraph.
5. **Market Definition & Concentration Analysis** — product/practice-area mapping table, market
   definition paragraph with the verbatim Competition-section quote, a market-size/share table (each
   row sourced, combined-share rows marked "Derived" if arithmetic on cited inputs), and an explicit
   "No HHI is computed" line if data doesn't support one.
6. **Competitive Effects Analysis** — Theory of Harm | Assessment | Basis table, then a
   "Portfolio-context integration" or "Enhanced competitive effects" paragraph, then a remedy-
   likelihood assessment paragraph.
7. **Regulatory Pathway & Timeline** — Approval/gate | Risk | Notes table (HSR, foreign regimes,
   CFIUS, shareholder vote), then an indicative timeline as a dated bullet list from signing through
   the outside date.
8. **Litigation & Fraud Risk Analysis** — Item | Assessment | Detail table covering target material
   litigation, historical litigation, acquirer litigation, restatements/investigations, short-seller
   allegations, deal-specific litigation, and an explicit MAC/fraud-as-closing-impediment assessment
   row.
9. **Valuation & Precedent Analysis** — a Reference|Observation table (equity value, EV, premium,
   any deal characterization quote), then the precedent-transactions table from Phase 7, then an
   **Assessment:** paragraph naming the single closest precedent and why.
10. **Strategic Stakeholder Analysis** — Stakeholder | Position table (board, shareholders,
    activists, target/acquirer management, sponsor, competing bidders).
11. **Deal Completion Probability Decomposition** — Component | Likelihood | Driver table (antitrust,
    financing, no-MAC, shareholder approval, absence of litigation), ending in a
    **COMPOSITE COMPLETION ASSESSMENT** row, then a **Key monitorables** bullet list.
12. **Sources, Citations & Limitations** — a Primary sources list (every EDGAR filing by form/date/
    accession, vector-DB hits by report title/institution/date, any web sources by outlet/date) and a
    Limitations list that explicitly states: no live-market data was reviewed (no Tape Check); no
    Outlook or Claude-Project research channels were run (name that if the user has research they
    expected used); any data gaps encountered (private non-filer entities, unconfirmed ownership
    percentages, market-size figures not independently re-verified this pass).

## Docx build recipe — hard-coded, don't re-derive this each run

- **Do all scratch/intermediate work under `/tmp`, never in the outputs-mounted folder.** Files
  written into the outputs folder cannot be deleted or renamed afterward on this platform — dumping
  chunked build scripts there leaves permanent clutter. Copy only the single finished `.docx` into
  the outputs folder, and only once it's built and verified.
- **Module bridge**: the `docx` npm package is preinstalled at `/tmp/node_modules` in the sandbox but
  is not resolvable from a cwd outside that path. Run every build command with
  `NODE_PATH=/tmp/node_modules` set, e.g. `NODE_PATH=/tmp/node_modules node /tmp/build_main.js`.
- **Chunk the build into part files** if the report is long (it usually is — 12 sections plus tables
  routinely exceeds a single comfortable script). Pattern:
  - `part1.js` — define shared helpers once: `H1`/`H2`/`H3` (heading paragraphs), `P` (body
    paragraph, accepts `{italics, size}` overrides), `bullet`, `label` (bold inline lead-in text
    followed by normal text, for "Assessment:"/"Meteora read:" lines), `cell`/`tableRow`/`makeTable`
    (build a `docx` Table from a header row array + data rows array + column-width array in DXA), and
    `hr` (a thin horizontal rule paragraph for section breaks). Build the front-matter parameter
    table and Section 1 here; export the running `children` array plus all the helpers.
  - `part2.js` through the last part — each `require()`s the prior part, destructures `children` and
    the helpers, appends that part's section(s), and re-exports `children` (plus the helpers, so the
    chain keeps working) — one or two report sections per part file keeps each file a manageable size
    to read back and debug.
  - `main.js` — `require()`s the final part, wraps `children` in a single `Document` with US Letter
    page size override `{width: 12240, height: 15840}` (DXA) and 1080-DXA margins on all four sides,
    a centered footer with `[TICKER] Deal Risk Core - Page ` followed by a `PageNumber.CURRENT`
    field, then `Packer.toBuffer(doc).then(buf => fs.writeFileSync("/tmp/[TICKER]_Deal_Risk_Core_
    [YYYY.MM.DD].docx", buf))`.
- **Verify before presenting** — don't trust that the build succeeded just because the script exited
  cleanly: convert to PDF (`soffice.py --headless --convert-to pdf` on the docx), rasterize a few
  pages (`pdftoppm -jpeg -r 100 file.pdf page`), copy the JPGs into the outputs-mounted folder, and
  `Read` two or three of them (front matter/Risk Matrix, a middle table-heavy section, the final
  Sources page) to confirm tables rendered correctly, no section is empty, and nothing got truncated
  by a part-file wiring mistake.
- **Only then** copy the finished `.docx` from `/tmp` into the outputs-mounted folder — this step is
  final on this platform, so do it last.

## Time budget discipline

- Fire the EDGAR pulls (8-K + exhibits, target 10-K/10-Q, merger-agreement anchored lookups) and the
  two vector-DB passes (ArbJournal, Chain Bridge Research) in the same turn. Serializing "finish the
  filing read, then start the vector search" is exactly what makes the full skill slow — don't
  reproduce it here.
- One vector pass per institution (ArbJournal, Chain Bridge Research), not the full skill's
  double-pass. Pull market-structure content AND precedent content out of that single pass.
- No Outlook search, no Claude Project file enumeration, no Tape Check, no broker-tier Table 9
  sorting — these are exactly what the full deal-risk-assessment skill adds, and exactly what this
  skill exists to skip.
- If a required input is missing (merger agreement not yet filed, sponsor portfolio opaque, no
  10-Q filed yet), state what's missing and what it prevents, then deliver the rest of the report
  rather than stalling on one field.

## Output

A single `.docx` named `[TICKER]_Deal_Risk_Core_[YYYY.MM.DD].docx`, presented to the user as the
final deliverable (e.g. via the file-presentation step available in the current environment).

**Does not write to any memory doc.** Like a flash/preliminary read, this is a point-in-time
deliverable, not the persisted view. If the user wants this run remembered between sessions, tell
them to say so explicitly, or run the full deal-risk-assessment skill, whose synthesis is what feeds
the memory-doc pipeline.

