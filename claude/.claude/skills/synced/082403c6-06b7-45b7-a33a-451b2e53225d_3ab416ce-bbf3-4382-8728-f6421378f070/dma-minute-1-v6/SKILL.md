---
name: dma-minute-1-v6
description: "T+0 DMA extraction on freshly filed M&A merger agreements: a Key Terms at a Glance table, Executive Summary, Approvals & Gates, Regulatory & Deal-Protection Architecture, a 14-section extraction, closing risk assessment, and live spread math with an Entry Price to Target IRR block. Pulls the acquirer's parallel 8-K; agreement text controls on fee conflicts; sources precedent timelines via vector-DB; sweeps the earnings call; diffs the last comparable deal; cross-checks bond pricing; Section 11 covers key-commercial-contract change-of-control exposure. Trigger: 'DMA-minute-1', 'dma-minute-1-v6', 'run the DMA', 'quick DMA', 'extract this merger agreement'. Covers cash/stock/mixed/RMT/REIT/private-target deals. Not for SPACs."
---

# DMA Minute-1 — Announcement-Day Merger Agreement Deal-Mechanics Report

**v6's only substantive change from v5: Section 11 of the extraction framework now covers material
commercial-contract change-of-control exposure, not just bond/debt change-of-control provisions.**
The gap this closes was concrete, not hypothetical: a sell-side note on a live position (PSNL/TEM)
did the desk's own job better than this module did — it pulled the target's actual customer-contract
8-K and quoted its change-of-control clause directly, rather than accepting either party's informal
account of what happens to the relationship post-close. A target whose near-term value depends on
one or two key commercial relationships can be contractually exposed to losing (or having to
renegotiate) exactly the relationship the deal thesis depends on, purely because of the change of
control itself — through a clause in the *underlying commercial contract*, which the merger agreement
may only cross-reference rather than restate. Everything else in this skill — Steps 0–2 and 4–9, the
Executive Summary/Approvals & Gates/Architecture-table format, the Entry Price to Target IRR block,
and Sections 1–10 and 12–14 of the extraction framework — carries forward from v5 unchanged.

Produce a T+0 deal-mechanics report on a freshly filed merger agreement: what it says, what it means
for completion risk, and whether the current spread is worth the risk being underwritten. The report
has a locked shape — Executive Summary, Approvals & Gates table, Regulatory & Deal-Protection
Architecture table, a 14-section extraction, a closing risk assessment, and live spread math — and
every run follows it exactly, section for section.

The analytical judgment behind that shape is built to survive contact with the actual documents, not
just look complete on the page. Concretely: read the acquirer's own 8-K, not only the target's, since
each side routinely restates deal terms in its own prose and sometimes states a figure — a Voting
Agreement's aggregate voting power is the recurring example — that never appears verbatim in the
shared exhibits or the target's own filing. Treat a truncation warning from the EDGAR text tool as a
signal to read more, not a signal to stop. Never mark a sub-item "NA — Not found" on the strength of an
exhibit's title alone; read the exhibit's actual body text first. Read the agreement's own Termination
and Expenses articles directly for fee amounts, payer, and trigger, rather than trusting either party's
8-K summary — two independently-drafted 8-Ks agreeing with each other on a number is not corroboration
if they share the same drafting error, and this has happened. Surface both termination fees' percentage
of equity value directly in the Architecture table, not only in the prose section further down, since a
reader who scans only the top-of-report tables — a real reading pattern for a same-day note — should
already see how large each fee is relative to deal size. Read every precedent cited in the completion-
probability discussion for procedural friction, not just its headline outcome, because "cleared without
a second request" and "cleared without a second request but only after a pull-and-refile" describe
different regulatory experiences even though both would otherwise be logged the same way. Treat the
acquirer's own same-day earnings or investor call as a first-class source alongside the press release
and the deck, since management routinely says more live than either party commits to in writing. Where
the acquirer has a recent, readily-identifiable comparable transaction, diff this agreement's material
terms against that prior deal's — a missing carve-out or a different fee percentage relative to the
acquirer's own last deal is real evidence, and the extraction has usually already surfaced everything
needed to make the comparison; it just doesn't make it unless asked. And where the target has public
bonds outstanding, pull a live price as a second, independent market-implied read on completion risk
alongside the equity spread math. Where the target's standalone value depends heavily on a specific
commercial relationship — a single key customer, licensor, or long-term supply partner — go find that
relationship's own governing contract and read its change-of-control clause directly, rather than
trusting either party's informal characterization of what happens to it post-close: whether the
contract requires the counterparty's consent to assign, gives the counterparty a unilateral
termination or license-out right, or simply survives unaffected is a fact with a citation, not a
question either side's spin should be allowed to answer for the reader.

This is a single-shot, no-monitoring module — it does not scan Outlook or Bloomberg IB for broker
research or set up a recurring refresh. Invoke it for the first read on a just-signed agreement.

## Step 0 — Scope the deal

Identify acquirer, target, tickers, and structure from the preamble/recitals or the user's message:
all-cash take-private, all-stock / merger of equals, mixed consideration, Reverse Morris Trust,
REIT-on-REIT, or private-target asset purchase. Deal type determines which framework sections apply and
which pricing legs exist.

## Step 1 — One gather block: pricing, press, document sourcing, and cross-checks

Fire everything in **one** tool-call batch — don't sequence it. The legs:

- **Live pricing** — `mcp__MeteoraMCP__get-price` (non-AWS server) with list syntax `['TGT', 'ACQ']`.
  Skip for private-target deals and say why in the report.
- **Capitalization data** — `mcp__MeteoraMCP__get-company-info` (non-AWS) for share count.
- **Price history** — enough trading history to compute 1-day, 1-week-average, and 1-month-average
  closing prices for the Gross Spread Calculation's premium-math lines. If the pricing tool doesn't
  return history directly, a targeted `WebSearch` for the relevant closing prices is an acceptable
  fallback — cite the basis either way.
- **Volume since announcement** — same pull as price history, one more field: shares traded on the
  announcement day (and each day since, if the report runs later than T+0) against the target's average
  daily volume, for the seasoning/liquidity check in the Gross Spread Calculation block.
- **Target bond pricing, if any exist.** Check whether the target has public bonds outstanding
  (visible from the indenture, a prior credit filing, or a quick `WebSearch`); if so, pull a live or
  recent price via whichever pricing tool is available (e.g. `get-bond-price`). This is one additional
  call, only made when bonds genuinely exist — skip silently (no need to flag the absence) when the
  target has no public debt. See Step 4 for how it's used.
- **Material commercial-contract search, when the target's standalone value depends on one.** Not
  every deal needs this — skip it silently for a diversified target with no single dominant
  relationship. But where the target's value proposition concentrates on a specific customer,
  licensor, or long-term supply partner (visible from the press materials, the target's own recent
  filings, or prior knowledge in this conversation), check whether that relationship's own governing
  contract is a standalone material agreement the target has filed on EDGAR (a master services
  agreement, a long-term supply agreement, a licensing or collaboration agreement) — a quick EDGAR
  full-text or 8-K search on the target's name plus the counterparty's name usually surfaces it when
  one exists. Also check the merger agreement's own Material Contracts representation and disclosure
  schedule index in case it names the same agreement directly. See Step 3, Section 11 for how this
  folds into the extraction.
- **Press context** — `WebSearch` for enterprise value, synergy targets, pro forma leverage, adviser
  identities, and expected close timing.
- **Acquirer's same-day earnings or investor call, if one occurred.** Search once for sell-side
  coverage of that call specifically — `"[Acquirer] earnings call" [target] antitrust OR synergies OR
  termination fee` or equivalent phrasing — separately from the general press-context search above.
  Management routinely addresses things live that neither party's press release states in writing:
  direct confirmation that a known legal or regulatory overhang was priced into the offer, the actual
  composition of a headline synergy figure, or color on deal rationale and structure. Fold anything
  load-bearing into the relevant report section (synergy composition into Section 1/6, overhang
  commentary into the risk assessment) rather than reporting it as a separate block. Skip cleanly, with
  one line saying so, if no such call occurred or no coverage was found.
- **The agreement's table of contents** — if EDGAR-filed, `mcp__MeteoraMCP-AWS__edgar-filing-text` with
  `summary=true` on the Ex-2.1 exhibit (AWS preferred; non-AWS EDGAR twin as fallback).
- **Regulatory precedent** — `WebSearch` for 2-3 prior deals that cleared through the same lead regulator
  as this deal's gating approval, with their actual clearance timelines. This feeds the completion
  probability / working-date read in the Overall Risk Assessment section later — it is not a new report
  section, just a research leg gathered now so Step 6 doesn't have to stop and search mid-write.
- **10-K competitor cross-check** — pull the "Competition" disclosure from (a) the target's most recent
  10-K, (b) the acquirer's most recent 10-K (if it files one), and (c) one adjacent competitor's 10-K if
  the target's disclosure names one. Use `mcp__MeteoraMCP-AWS__edgar-filing-text` with `section='1'` or a
  `summary=true` pass to locate the Competition sub-heading, then pull that subsection only. Note
  explicitly whether the target names the acquirer as a competitor, whether the acquirer's disclosure is
  symmetric or generic, and what a comparable third party's filing says — this asymmetry is a real
  antitrust market-definition signal and belongs inside Section 4 of the extraction, not a separate memo.
  If the disclosures are too generic to yield a signal (privately-held acquirer with no 10-K, a target
  that names no one by name), run the P3 pull in `references/vector-db-retrieval.md` as a
  supplementary source — sellside/IOC coverage often names competitors by product line where a 10-K's
  Competition section is generic or a private acquirer has none — before saying so plainly rather than
  manufacturing a read that isn't in the filing.
- **Acquirer's parallel 8-K.** When the target files an 8-K announcing the merger agreement, also pull
  the *acquirer's* own 8-K on the same transaction — same announcement date, different CIK/ticker — via
  `mcp__MeteoraMCP-AWS__edgar-filings` with `ticker=<ACQUIRER>`, `form_type='8-K'`,
  `filing_date=<announcement date>`, then `edgar-filing-text` on its primary document. Acquirer 8-Ks
  routinely carry an Item 1.01/3.02 narrative description of the same exhibits the target filed — e.g.
  aggregate voting power under a Voting Agreement, financing detail phrasing — that is not restated
  verbatim anywhere in the shared exhibits or the target's own 8-K. Treat this as a standard parallel
  source on every deal with two SEC-reporting parties, not an optional or deal-specific pull — it's one
  more call in the same gather batch, so it costs no sequential time. (Skip only when the acquirer is a
  private company with no 8-K to pull, and say so.)

## Step 2 — Source the full agreement text

### Uploaded PDF
Sequence: `pdfinfo` → `pdftotext -layout` → `grep -n` with quoted section references → `sed -n
'START,ENDp'` for full section bodies.

Hard-won navigation tips:
- Defined terms use Unicode left quotation marks ("). grep with the actual Unicode character —
  straight-quote searches fail silently.
- When grep points near but not exactly to a provision, read ±20–30 adjacent lines before concluding
  it is absent.
- Contiguous section extraction: `awk '/Section 8\.1\./{f=1} f{print} /Section 8\.2\./{if(f)exit}'
  agreement.txt` works reliably.
- Page numbers: map via footer-based detection (short numeric strings after form-feed `\f` splits).
- **A truncation error is a retry signal, not a stop signal.** A token-limit truncation error from
  `edgar-filing-text` (or any large-file read) means the tool couldn't return everything you asked for in
  one call — it does not mean the content isn't there. Halve `max_chars` and re-request from the same
  `offset` until the full section has actually been read, and only then move on. This matters most for
  Article 1 Definitions pulls: it's a long alphabetized list, and a single defined term you need (a
  Confidentiality Agreement date is a recurring example) can sit anywhere in it. Stopping pagination
  early because of a truncation warning is how a term that was one more paginated call away ends up
  marked NA.

### EDGAR-filed agreement
Use `mcp__MeteoraMCP-AWS__edgar-filing-text` with `accession_number` (hyphenated format), `exhibit`,
and `offset`/`max_chars` pagination — page in ≤40,000-char windows by offset once past the TOC pulled in
Step 1. If the exhibit number is unknown, `mcp__MeteoraMCP-AWS__edgar-filing-index` lists every document
in the filing package. If the exhibit resolver fails, fall back to `edgar-filing-index`, copy the
exhibit's document `url`, and pass it via `url=` instead of `exhibit=`.

## Step 3 — Run the 14-section extraction

Read `references/extraction-framework.md` and execute it in full. Non-negotiables throughout:
verbatim-only quotation, Section/Page cites on every extracted fact, bold responsive flag language
where warranted, `NA — Not found in agreement` where genuinely absent, never infer or hallucinate a
figure. Two completeness rules that shape how "NA" gets used:

- **No NA on an exhibit you haven't actually read.** If the EDGAR filing index lists an exhibit
  relevant to a sub-item — a voting/support agreement, a debt commitment letter, and so on — don't mark
  that sub-item NA on the strength of the exhibit's title alone. Read the exhibit's body text first. If a
  figure you need genuinely isn't in the exhibit's own text (a common case: an aggregate percentage tied
  to a share schedule that didn't survive the text extraction, like a Voting Agreement's Exhibit A),
  check the acquirer's parallel 8-K per the Step 1 sourcing leg before falling back to NA — the
  narrative summary there often has exactly the rolled-up figure the raw exhibit doesn't state. If it's
  still genuinely unresolved after both of those checks, say so as an explicit flagged open item ("figure
  not located in the exhibit text or the acquirer's 8-K — confirm against the underlying 13D or forthcoming
  proxy") rather than a bare NA, so the gap is visible to the reader instead of silent.

- **The agreement text controls on termination-fee amount and direction, always.** Section 7
  (Termination Rights & Fees) must be built from a direct read of the agreement's own Termination article
  and its Expenses/Termination Fee section (wherever the deal defines "Termination Fee" and any reverse/
  parent-side fee), not from either party's 8-K Item 1.01 narrative summary. Trace each dollar figure back
  to its own defined-term cross-reference — which section triggers it, which party pays it — before
  writing the number into the report. If the 8-K narrative (either party's, or both) states a different
  amount, a different payer, or a different trigger than the agreement text shows, the agreement is
  controlling; write the correct figures into the report and add an explicit CRITICAL ARBIT NOTE at the
  top of the report identifying the discrepancy, quoting both the agreement's cross-referenced mechanics
  and the conflicting 8-K language. Do not treat agreement between the target's and acquirer's 8-Ks on the
  same (wrong) figure as corroboration — independently-filed 8-Ks routinely share the same drafting error
  or boilerplate, and two matching wrong numbers are still wrong.

Fold the Step 1 10-K competitor cross-check and, where relevant, the jurisdictional-threshold check into
the 4.1/4.3/4.4 sub-items as a short paragraph clearly labeled as press/EDGAR-sourced context — e.g. "10-K
cross-check (press/EDGAR-sourced, not agreement text): ..." — kept visually separate from the verbatim
quoted agreement language above it. Every other section of the 14-section framework follows the
framework file directly.

**On a tender-offer structure, Section 2 (Election Mechanics) flags any minimum-tender-offer-period
that departs from the traditional 20-business-day convention, and cites why.** A one-step-merger
appraisal timeline and a cash tender offer run on genuinely different clocks (a 30-day HSR waiting
period for a one-step merger versus a 15-calendar-day HSR period for a cash tender offer under 16 CFR
803.10 — do not default to 30 days just because that is the more familiar number), and separately, the
minimum tender-offer period itself is not always the traditional 20 business days: an April 2026 SEC
exemptive order allows a 10-business-day minimum for qualifying deals (negotiated, all-cash,
fixed-price, all outstanding shares, no competing bid, structured to close via a DGCL §251(h) back-end
merger). If the agreement's own offer-period section states a period shorter than 20 business days,
quote it verbatim as usual, and add one sentence identifying that this is a deviation from the
standard convention and, if the deal's structure matches the exemptive order's qualifying criteria,
naming that as the likely basis — this is a fact the extraction should surface at the point of
quotation, not something left for a later, separate research pass to reconstruct from the working
close-date math.

**Fold the Step 1 material-commercial-contract search into Section 11's new sub-items (11.5/11.6),
when it applies.** Quote the actual change-of-control/assignment clause verbatim, cited to the
contract's own section, the same discipline as the merger agreement extraction elsewhere in this
report — don't paraphrase it from a press release, an investor note, or either party's informal
account of the relationship. State plainly what the clause requires: consent to assign, a unilateral
termination or license-out right for the counterparty, or nothing (the contract simply survives).
This is a completion-risk / value-continuity fact, not an MAE carve-out and not a bond covenant — keep
it in Section 11, cited to its own contract, not folded into Section 7's MAE discussion or Section
6's termination-fee analysis even though all three bear on downside risk. If the target's value
doesn't concentrate on one relationship, or a search turns up nothing, mark 11.5/11.6 `NA — Not
applicable` and say why in one clause, the same as any other genuinely-absent sub-item.

**Diff against the acquirer's own most recent comparable deal, where one is readily identifiable.** If
the acquirer has signed a prior transaction in the same or a closely adjacent industry within roughly
the last two to three years — the kind of deal a quick search or existing knowledge from this
conversation surfaces without a dedicated research effort — note, in one or two sentences at the point
in the extraction where it's most relevant (typically the MAE carve-out list in Section 7, but also
worth a line on the efforts standard or the termination-fee percentage if either differs materially),
what is different between this agreement and that prior one. This is a comparison against extraction
work already being done, not a new research task: the current agreement's MAE carve-outs, efforts
standard, and fee percentages are all already being pulled verbatim per this section's own
instructions; the only addition is naming, in a sentence, what a reader who knows the acquirer's last
deal would notice is missing or different this time — e.g. "unlike the acquirer's [year] agreement for
[prior target], this MAE definition's tariff/trade-policy carve-out carries no separate 'trade wars'
exclusion" or "the reverse termination fee here is 7.2% of equity value versus 4.1% on the acquirer's
last comparable transaction." Skip cleanly if no clearly comparable prior deal is readily
identifiable — this is not worth a dedicated research effort on its own, only worth doing when the
comparison is cheap because the prior deal is already known or trivially found.

## Step 4 — All math in Python, presented as plain calculation blocks

Run every calculation in a bash heredoc, never show Python source or `print()` calls, present as plain
left-aligned `label: value` blocks:

```
NSA current price:    $40.23  (+30.0% on day)
PSA current price:    $289.80 (-2.7% on day)
Implied offer value:  0.1400 × $289.80 = $40.572
Gross spread:         $40.572 − $40.23 = $0.342 (0.85%)
Reference offer:      $41.68 (based on PSA close of $297.72 on March 13, 2026)
Outside Date:         December 16, 2026 (~9 months)
Annualized gross spread: ~1.1% (assuming Q3/Q4 close)
```

The standard calculation set: gross spread to deal price; annualized return at multiple close-date
scenarios; termination fees as % of equity value; pro forma ownership splits; vote/tender threshold share
counts; timeline items with specific calendar dates and passed/pending status. Additions to the Gross
Spread Calculation block, all inside the existing block, never new sections:

```
1-day premium:        $167.00 / $125.56 − 1 = 33.0%
1-week avg premium:   $167.00 / $XXX.XX − 1 = XX.X%
1-month avg premium:  $167.00 / $XXX.XX − 1 = XX.X%
```

```
Market-implied probability (spot):
  Deal price:              $167.00
  Current price:            $163.00
  Downside reference:       $125.56  (basis stated — e.g. last unaffected close)
  ($163.00 − $125.56) / ($167.00 − $125.56) = 90.3%

Market-implied probability (duration-adjusted):
  Working close date:       [date] ([N] days out, per the precedent read below)
  [same downside reference, discounted for the stated holding period — show the
   discount basis, e.g. cost-of-carry or funding-rate assumption used]
  = XX.X%
```

Always state the downside reference and its basis in the block itself — the number is only as good as
that assumption, and it belongs next to the math, not in separate prose.

```
Volume since announcement:  [N] shares traded on [date] vs. ~[avg daily volume] average
  = [X]% of average daily volume traded / [Y]% of float since signing
  (a spread on a stock that has barely traded since announcement is less seasoned
  and less trustworthy than one that has fully digested the news — say so in the
  verdict when this fraction is low)
```

**Where the target has public bonds (per the Step 1 pull), add a one-line credit cross-check
immediately after the volume/seasoning line:**

```
Credit cross-check: [Target] [coupon]% notes due [year] trading at [price] (vs. [prior price]
  [date/period reference]) — [directionally consistent with / diverging from] the equity spread's
  implied completion odds
```

This is a second, independent market-implied read on completion risk, not a full credit analysis — one
line, one price point (plus whatever recent-move context is cheaply available), and a plain statement of
whether it agrees with or diverges from what the equity spread implies. If the bonds have moved toward
the likely post-close redemption or takeout price, that's corroborating; if they haven't moved or have
moved the other way, say so plainly rather than only reporting the number. Skip this block entirely,
without comment, when the target has no public bonds.

If any Python writes files, pass `encoding='utf-8'`.

Termination-fee percentage-of-equity-value math happens here, same as the rest of this step's
calculations, and also surfaces in the Architecture table (Step 6/Step 7) rather than staying confined
to the Section 6.2/6.3 prose. No separate calculation — the same fee-vs-equity-value math done here just
gets carried into the table cell too.

**Entry Price to Target IRR — required, every run.** Read `references/entry-price-target-irr.md` in
full before this step and apply it exactly: a fresh live-price pull (never a spread reused from
earlier in the conversation), three close-date scenarios (this report's own working close date, and
that date ±30 days — never a fixed generic day-count set), an 8%-default parameterized target IRR,
and the required four-part Read paragraph. This is a sub-block of the Gross Spread Calculation
(Step 7), not a separate section.

## Step 5 — Format the 14-section extraction

For every numbered item in every section of `references/extraction-framework.md`:

```
N.N Sub-item title in title case
Citation line — e.g. "Section 4.3, Page 18", or "Preamble, Page 1" / "Recitals, Page 5" for front matter

"Full verbatim quoted text from the agreement, exactly as written, no paraphrase."

[optional] Plain-language breakdown, bullet list, or aligned calc block unpacking the quote.
```

`NA — Not found in agreement` / `NA — Not applicable` per the Step 3 completeness rules, same inline
flag convention throughout:
- `⚑ CRITICAL ARBIT NOTE:` — a finding that materially changes the risk-arb read
- `⚑ KEY ARBIT NOTE:` — an important but secondary structural point
- `⚑ RISK FLAG:` — something to independently verify or watch

No standalone "structural asymmetries" section, no top-of-report strength/weakness paragraph — flags
live where the underlying provision is discussed and roll up into the closing risk assessment.

## Step 6 — Build the Key Terms table, Executive Summary, Approvals & Gates, and Architecture table

### Key Terms at a Glance table (locked columns: Term | Detail) — sits above the Executive Summary

Before the Executive Summary, build a compact quick-reference table a reader can scan in five seconds
without reading the prose below it — the same job an experienced arb analyst's own Excel snapshot
does. Locked row order, one row each (mark `NA` only where the deal genuinely has no value for that
row, e.g. no ticking fee):

Acquirer / Target | Structure (cash/stock/mixed, one-step merger vs. tender offer) | Headline
consideration (per-share, exact) | Deal value (equity value, and enterprise value if materially
different) | Signing date | Expected close / Outside Date | Termination fees (both, each as $ and %
of equity value, one line each: "Company: $X = Y%" / "Parent: $X = Y%") | Financing (cash-confirmed /
debt-financing-contingent / stock) | Ticking fee (rate and start date, or `NA`) | Key approvals
required (short list: HSR, target vote, sector regulator(s), CFIUS, foreign filings — whichever
actually apply to this deal).

Every figure in this table must already exist elsewhere in the report (the Architecture table, the
Executive Summary, or the extraction) — this table is a front-loaded index into work the rest of the
report is already doing, not a separate calculation, and its figures must match those bodies exactly.

The Executive Summary is a four-part prose block, in this order:

1. One-paragraph deal identification (acquirer, target, headline consideration, deal value, signing
   date, structure).
2. "If the deal closes" paragraph.
3. "If the deal does not close" paragraph(s) — every termination-fee-triggering scenario, who pays
   whom, how much, sole-and-exclusive-remedy status, cited to the specific subsection. One sentence only:
   if the target's standalone business trajectory is discernible from the press materials or recent
   trading history (durably improving, stable, or degrading), say in one clause what that implies for
   where the stock likely trades in a break scenario — this is a downside-sizing input, not a full
   business review, and belongs at the end of this paragraph, not a new one.
4. Closing "so what" sentence naming the single most important structural asymmetry.

Live pricing/spread figures still do not belong here — they live only in the Gross Spread Calculation
block at the close of the report.

### Approvals & Gates table (locked columns: Approval / gate | Risk | Notes)

Same locked six-row order every time (Antitrust/HSR, Foreign merger control, CFIUS/national security,
Sector-specific regulator(s), Target stockholder vote, Acquirer stockholder vote), same risk tags
(`[GREEN — LOW]` / `[GREEN — N/A]` / `[AMBER — MONITOR]` / `[RED — HIGH]`), same condition-vs-covenant
distinction in Notes.

Whichever row is the actual pacing item for the deal gets that said plainly in its own Notes cell — e.g.
"...this is the gating item: HSR/FINRA are expected to clear well inside the Outside Date; CMA Phase 1
prenotification has historically run 4–6 months on comparable deals (see precedent read in the Risk
Assessment section below), which is what the working close estimate is really built around." Do not add a
sentence or paragraph below the table calling this out separately — the table's own Notes column is the
only place this lives. If two gates are genuinely comparable in pacing risk, say that in both rows' Notes
rather than forcing a single answer. On the Target stockholder vote row specifically: if a Voting
Agreement or similar support agreement exists, this Notes cell is where its aggregate committed
voting-power percentage belongs (sourced per Step 1's acquirer-8-K leg if the target's own filings don't
state it) — a locked-up bloc materially changes how much weight this gate should carry, and burying that
figure only in Section 5 lower in the report undersells it here.

### Regulatory & Deal-Protection Architecture table (locked columns: Clause | What it does)

Same locked rows every time: efforts standard; divestiture obligation and its cap construct; sponsor/
portfolio-company carve-out; litigation commitment and its bound; remedy-proffer clock; pull-and-refile
rights; HSR filing deadline; specific performance (financing-conditioned or not); reverse termination
fee; Company/forward termination fee; Outside Date and extension mechanics.

**Inside the two termination-fee rows only:** each fee's "What it does" cell states the dollar amount
**and** that amount as a percentage of total equity value — e.g. "Parent Termination Fee =
$22,540,785.00 = 7.20% of equity value ($313.1mm), payable if [Company] terminates under Section 10.1(g)
[Parent fails to close when required] (Section 11.4(c))." This is the same equity-value-percentage math
already computed in Section 6.2/6.3 and Step 4 above — surface it here too, since a reader scanning only
the top-of-report tables (a real reading pattern for a T+0 note) should not have to reach Section 6 to see
how large each fee actually is relative to deal size. No new row, no new column, no change to any other
row in this table. Both this table's two fee amounts and their payer/trigger attribution must come from
the agreement's own Termination Fee / Expenses section per the Step 3 rule above — never copied from
either party's 8-K narrative without a direct cross-check against the agreement text, since that is
exactly where the two sources have been seen to disagree.

**If the Step 3 same-buyer prior-deal diff surfaced anything for a row in this table** — a different
carve-out, a different fee percentage, a different efforts standard — fold the one-sentence comparison
into that row's "What it does" cell rather than adding a new row or a separate paragraph. The Architecture
table is exactly where a reader benchmarking this deal against the acquirer's last one would look first.

## Step 7 — Assemble in the house format, present in chat

Deliver directly in the chat response — do not write it to a file, and do not call `present_files` /
`SendUserFile` for it, unless the user specifically asks for a file/Word export.

This is the locked report shape, in this exact section order:

```
[TICKER1] / [TICKER2] MERGER AGREEMENT — DMA EXTRACTION REPORT
Merger Agreement dated [DATE] | SEC Filed [DATE] (Accession No. [XXXXXXXXXX-XX-XXXXXX])
Analysis as of [DATE] | Analyst: Meteora Capital

KEY TERMS AT A GLANCE
Term | Detail
[locked row order per Step 6; every figure must match the Architecture table, Executive Summary, and
 extraction below exactly]

EXECUTIVE SUMMARY
[four-part prose block per Step 6]

Approvals & Gates
Approval / gate | Risk | Notes
[locked six-row order; the pacing-item row's Notes cell says so explicitly; the Target stockholder vote
 row's Notes cell states any Voting Agreement's aggregate committed voting-power % if one exists]

Regulatory & Deal-Protection Architecture ([Merger Agreement Ex-X.X, accession XXXXXXXXXX-XX-XXXXXX])
Clause | What it does
[locked rows per Step 6; both termination-fee rows state $ amount AND % of equity value; any
 same-buyer prior-deal diff folds into the relevant row's cell]

1. TRANSACTION OVERVIEW & STRUCTURE
1.1 Precise Parties to the Transaction
1.2 Post-Closing Ownership Structure
1.3 Exact Consideration Structure
1.4 Transaction Format
1.5 Total Equity Value and Enterprise Value

2. ELECTION MECHANICS
[... sections 3 through 14, per the framework file; the 10-K cross-check and jurisdictional-threshold
 check fold into Section 4's sub-items only; the no-bare-NA-on-an-unread-exhibit rule applies
 throughout, most visibly in Section 5 (Shareholder Approval Mechanisms) ...]

OVERALL RISK ASSESSMENT & DEAL COMPLETION PROBABILITY

Summary Matrix
Risk Factor | Assessment | Severity
[one row per material risk dimension that actually applies]

Deal Completion Probability: XX–XX%
[where a precedent read materially informs this range or the working close date referenced in the
 spread calc below, name the 2-3 precedent deals here with one clause each on why they are or aren't
 analogous, AND one clause on any procedural friction that precedent required (pull-and-refile, an
 extended waiting period) rather than just its headline outcome — fold this into the prose immediately
 under the percentage, not a new subheading]

[Optionality — a short paragraph immediately here, before Key Factors. Not "does this close" but
 "is there upside if it doesn't, or only downside": the forward termination fee as a % of equity value
 vs. convention, the target's standalone business trajectory and what it implies for a break-scenario
 downside, and a read on pre-signing process quality (long confi period + unanimous approval + one
 logical buyer reads as a thin or stale market check — say so plainly, it isn't necessarily a red flag,
 it's a fact about how much upside optionality the position actually carries).]

Key Factors Supporting High Probability:
1. [numbered, each tied to a specific provision cited earlier in the report]
2. ...

Key Risks:
- [bulleted, each tied to a specific provision]
- [2-3 specific, mechanism-tied forward-watch items here as additional bullets — e.g. a named
  regulator's approval that could slip, a specific pre-announcement trading pattern worth tracking, a
  go-shop deadline — written as things to watch happen next, not a restatement of risks already covered
  above. These are bullets in the same list, not a separate "watch-list" section.]

GROSS SPREAD CALCULATION (as of [date]):
[TGT] current price:    $XX.XX  (+/-X.X% on day)
[ACQ] current price:    $XX.XX  (+/-X.X% on day)      <- omit for all-cash deals
Implied offer value:    [cash and/or exchange-ratio math] = $XX.XX
Gross spread:            $XX.XX − $XX.XX = $X.XX (X.XX%)
[1-day / 1-week-avg / 1-month-avg premium lines, per Step 4]
[volume-since-announcement / seasoning line, per Step 4]
[credit cross-check line, per Step 4, if the target has public bonds]
Reference offer:         [basis, e.g. announcement-day close or 30-day VWAP premium]
Outside Date:            [date] (~N months from signing)
Annualized gross spread (pre-funding): ~X.X% (assuming [close scenario, precedent-informed per Step
                          4/the Risk Assessment section above])
[Market-implied probability block — spot AND duration-adjusted, per Step 4, with downside
 reference and holding-period basis both stated]

ENTRY PRICE TO TARGET IRR (fresh pull, [timestamp]; target IRR: [X]% [default/per request]):
[Three-scenario table — baseline (this report's own working close date) and baseline ±30 days —
 per references/entry-price-target-irr.md. Required every run, never a fixed generic day-count set.]
[The required four-part Read paragraph, per that same reference file: dollar entry-price range;
 the duration/discount directional relationship; current pricing vs. the target hurdle and what
 that implies about the market's read; a named tail risk or precedent from elsewhere in this same
 report and whether the spread appears to price it in.]

[Closing verdict sentence — one or two sentences stating plainly whether the spread is attractive,
 unattractive, or fair given the working close date, the fee/remedy architecture, and the Optionality
 read described earlier in the report, naming a specific re-entry price/spread level when the analyst
 has a view on where it would become attractive. This is the last line of the report. Say it as
 directly as the house benchmark notes do — do not hedge it into nothing.]
```

Formatting rules:
- Section headers (`N. SECTION TITLE`) are ALL CAPS; sub-item headers (`N.N Title`) are title case.
- The Executive Summary is prose, not bullets.
- Approvals & Gates and Regulatory & Deal-Protection Architecture are tables — always both, always in
  that order, always immediately after the Executive Summary and before Section 1.
- Aligned calc blocks use the plain `label: value` style, not tables — except the Approvals & Gates
  table, the Regulatory & Deal-Protection Architecture table, and the closing Summary Matrix, which ARE
  tables.
- Output clean markdown directly in the chat message.
- No new top-level headers anywhere in the report. If an addition doesn't fit inside one of the existing
  sections/tables/blocks listed above, it doesn't belong in the report — offer it as a Standing follow-on
  instead.

## Step 8 — Optional Call/Color Addendum (not part of the report shape — a separate follow-up)

If the announcement coincides with or precedes an earnings call, deal call, or analyst call whose
transcript becomes available shortly after the initial report is delivered, offer — don't force — a
short, separate follow-up message (not a re-run of the full report) that updates the antitrust
market-definition read and/or the working close date if management's own comments change either one.
Frame it as "Updated Thoughts," not a correction. Do not delay the initial report to wait for a
transcript — the Step 1 earnings-call sweep already covers what's available at gather time; this step
is only for material that surfaces afterward. If the user says this run is one-off/no-addendum, skip
this step and say so in the closing receipt.

## Step 9 — Close it out

The report is a self-contained, point-in-time deliverable, and this module's job ends at delivery.

## Standing follow-ons — offer at the end, don't run unprompted

- Stock-for-stock deals: ratio-spread scenario grid against a range of acquirer prices
- S-4 / joint proxy pull once filed (deals with registered consideration)
- EDGAR exhibit-index pull for supplemental filed documents: debt commitment letters, voting
  agreements, disclosure letter schedule lists
- Word/docx export of the report — Node.js `docx` npm library; validate with
  `/mnt/skills/public/docx/scripts/office/validate.py`; respect OOXML schema ordering
- The Call/Color Addendum (Step 8), if a transcript exists and wasn't run yet
- A deeper antitrust-minute-1 pass if the 10-K cross-check or precedent pull surfaces a real overlap
  concern worth the fuller antitrust module
- A fuller credit-side read (multiple bond tranches, CDS if quoted, ratings-agency commentary) if the
  one-line cross-check in the Gross Spread Calculation block surfaces a genuine divergence from the
  equity-implied read worth investigating further
- Handing the deal to `merger-agreement-extraction`'s monitoring-refresh mode (or
  `deal-research-sweeper`) for a recurring broker-research / EDGAR / spread refresh once the position
  is live and being tracked day to day

## Reference files

- `references/extraction-framework.md` — the locked 14-section analysis framework. Read it in full at
  Step 3 of every extraction.
- `references/house-view-and-precedents.md` — precedent-timeline methodology (including the
  procedural-friction check), the jurisdictional-threshold check, and the reasoning standard for the
  market-implied-probability and verdict lines in the Gross Spread Calculation block. Read it in full
  before Step 4/Step 6 — it is a methodology reference, not an instruction to produce a section by this
  name in the output.
- `references/entry-price-target-irr.md` — the Entry Price to Target IRR methodology: fresh-pricing
  requirement, the baseline/±30-day scenario derivation, the 8%-default parameterized hurdle, and the
  required four-part Read. Read it in full before Step 4. Required every run, inside the Gross Spread
  Calculation block — not a new section.
- `references/vector-db-retrieval.md` — the P1 (precedent-timeline) and P3 (standalone-trajectory /
  competitive-positioning) vector-DB pulls used inside `house-view-and-precedents.md` §1 and §5, and
  as a supplement to the Step 1 10-K competitor cross-check: exact filters, and the empirically-
  confirmed traps (`industry` vs. `sector`, and — critical for P3 — never filtering by ticker/sector/
  industry on the IOC Notes Database corpus, since a large share of it carries blank or flatly wrong
  tags even though the document text is fine). Read it in full before Step 1/`house-view-and-
  precedents.md`.