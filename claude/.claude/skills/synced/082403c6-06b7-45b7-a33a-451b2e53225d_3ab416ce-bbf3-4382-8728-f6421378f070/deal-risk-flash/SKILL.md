---
name: deal-risk-flash
description: >
  Fast, sub-10-minute preliminary read on a just-announced M&A deal — deal terms from the
  8-K/press release/deck, four anchored merger-agreement lookups (efforts covenant, outside date,
  marketing period, approvals), a preliminary overlap screen from the target's 10-K Competition
  section and revenue mix, precedents from the ArbJournal/Chain Bridge Research vector index, and
  a lean-in/watch/pass call — in the same section order as deal-risk-assessment, so the full run
  later fills in the same document. Trigger on "flash read on [ticker/deal]", "quick take on this
  deal", "just announced, what's the risk", "give me something in five minutes", "preliminary
  read", "first look at this", or any pasted 8-K/merger press release where speed matters more
  than completeness. Also trigger proactively the moment a merger 8-K or deal press release lands
  and nothing has been produced yet. This is the fast triage tier that runs FIRST on every new
  deal; deal-risk-assessment is the complete follow-up, run separately.
---

# Deal Risk Flash — sub-10-minute preliminary read

Deal-risk-assessment is thorough because it has to be: it walks a merger agreement clause by
clause, maps a buyer's full competitive footprint, pulls verbatim competitor lists out of every
overlapping entity's 10-K, defines markets, and runs an exhaustive, un-sampled sweep of three
sell-side channels twice. That rigor is the point of the full report, and it is also why it
cannot land in five minutes.

Flash exists for the narrower job: the desk needs to decide, within minutes of a deal hitting the
tape, whether this is something to lean into, watch, or ignore. It gets there by being ruthless
about *which* work pays off in the first five minutes, not by doing every kind of work badly.

**What Flash does do**, all of it fired in one parallel burst:

1. The documents that exist and matter at T+0 — the 8-K, the press release, the deck.
2. **Four anchored lookups into the merger agreement** — the efforts/divestiture covenant, the
   outside date, the marketing period, and the required-approvals list. Not a clause walk: four
   targeted section reads. These four punch far above their cost, because the efforts covenant is
   the parties' own confession of how much antitrust risk they negotiated around, and the desk
   will ask about it within the first ten minutes.
3. **A preliminary overlap screen off the target's own 10-K** — the Competition section verbatim
   plus the segment and geographic revenue mix. Reading one section of one filing is roughly a
   minute and converts "overlap plausible, unverified" from a shrug into an evidenced flag.
4. An instant vector-database precedent scan in place of the sell-side sweep. ArbJournal and Chain
   Bridge Research are already ingested and structured — querying them is seconds, not the minutes
   it takes to page an Outlook mailbox.

**What Flash still does not do**, and must say so plainly: full buyer footprint mapping, buyer-side
competitor extraction, market definition or any share/HHI work, target financial health, the
litigation and fraud screen, the full sell-side sweep, and the tape. Every one of these is
something deal-risk-assessment still does properly, later. Flash's job is to be honest about what
it skipped, not to pretend it did the full job faster.

**Flash stays inside the blind wall.** No live price, spread, or market data enters this report —
same discipline as deal-risk-assessment Phases 1-7, for the same reason: a fundamental read that
starts from the spread just rationalizes the spread. If the desk wants a price check, that is a
separate, explicit ask — Flash does not fetch it, mention it, or imply one is coming. Note the
disclosed premium from the release freely; that is a filed figure, not the tape.

**Flash does not write to the memory doc.** A five-minute read is not the view that should persist
between sessions. Only deal-risk-assessment's full synthesis earns a memory-doc entry (via the
seed-memory / merger-arb-memory skills). If the user wants this deal remembered, tell them to run
the full assessment.

**Flash does not launch the full assessment automatically.** It is a standalone read. Close by
noting that deal-risk-assessment exists as the complete follow-up, and let the user decide when to
run it — don't kick it off in the background.

## Tools

- **EDGAR**: `MeteoraMCP:edgar-filings`, `edgar-filing-index`, `edgar-filing-text`,
  `edgar-company-facts`. Fallback: `web_fetch` of sec.gov if the MCP is unavailable.
  Two arguments make Phase 1 fast enough to be worth doing — learn them: `summary=true` returns a
  table of contents with sub-headings and character offsets (this is how you find the efforts
  covenant in a 600KB exhibit without reading it), and `section='1'` extracts a 10-K item whole.
- **Acquirer/target IR site**: `web_fetch` for the press release and investor deck; if the page is
  client-rendered and returns an empty shell, switch to the `claude-in-chrome` tools to render it.
- **Vector Database** (`MeteoraMCP:semantic-search` on the `investment-team` index): the same
  ArbJournal and Chain Bridge Research institution-filtered passes the full skill uses in Phase 7,
  run here as a primary research step rather than the last one.
- **Web search**: only if the buyer's identity or portfolio isn't resolvable from the filing or
  press release in under a minute of looking.
- Do **not** call Bloomberg or any live-pricing tool. There is no Tape Check in Flash.

## Phase 0 — Pending check (30 seconds)

One search or a glance at the 8-K confirms the deal is freshly announced and not already closed,
terminated, or rumor-stage. While here, grab whatever regulatory posture is already stated
(expected close quarter, "subject to HSR and customary closing conditions," shareholder vote
required) — usually a line in the press release, not something that needs digging.

## Phase 1 — Parallel ingestion (the speed lever)

This phase decides whether Flash lands in under ten minutes or in thirty. **Fire every call below in the
same turn.** Four independent read streams go out together — the 8-K package, the EX-2.1 anchored
lookups, the target's 10-K, and the vector queries. Finishing the filing read before starting the
vector search is exactly the serialization that makes the full skill slow; don't reproduce it
here. If a later stream needs something an earlier one produced, take the second round trip — one
extra hop is cheap, four sequential reads are not.

### Stream A — 8-K, press release, deck

Extract only what a call needs:

- Parties, consideration (cash/stock/mixed), deal value, disclosed premium
- Acquirer entity name and, if visible in one line, its ultimate parent and guarantor
- Termination fees both directions, including any reduced go-shop/Excluded-Party fee
- Stated expected close timing and the approvals list
- Strategic rationale and synergy framing in the parties' own words
- Any self-drawn combined-market-position slide (strong, fast overlap evidence — capture it
  verbatim with the slide number)
- Financing description (committed amounts, sources, whether financing is a condition)
- Pre-announced divestitures or planned separations — when the release already says a segment will
  be carved out post-close, that shapes what a remedy conversation would even look like

Two things reliably hide in plain sight in the release, and both have burned this read before:

- **Which premium the issuer chose to quote.** A premium to a 30-day VWAP rather than to the
  unaffected close is a deliberate framing choice. Note the basis explicitly, and if both the VWAP
  premium and a close-to-close premium are available, note the gap — a wide gap means the stock
  moved hard into the announcement, which is worth understanding before anyone underwrites the
  downside. Report the metric the issuer used, labeled as such; never silently upgrade it to "the
  premium."
- **When the go-shop actually ends.** The headline date is rarely the real one: most agreements let
  the target keep negotiating with any party that bid during the window ("Excluded Parties") for a
  further 10-15 days, usually at the reduced termination fee. The realistic topping deadline is
  that later date. State both.

### Stream B — merger agreement, four anchored lookups (EX-2.1)

Call `edgar-filing-text` with `summary=true` on the merger agreement exhibit to get the heading
map, then read only the sections you need by offset. Four items, nothing more:

1. **Efforts / regulatory covenant** — the efforts standard ("reasonable best efforts" vs.
   "hell-or-high-water"), whether divestiture is required, and whether that obligation is capped
   by materiality or by a disclosure schedule. Quote the operative phrase; don't paraphrase it.
2. **Outside date** (and extension mechanics if stated in the same clause).
3. **Marketing period** length — it sets the floor on time-to-close even when everything clears.
4. **Required approvals** as the agreement lists them, which is often broader than the closing
   conditions: separate out what is a *condition to closing* from what is merely a *covenant to
   file* (state premerger notifications, foreign investment or competition filings). Conflating
   the two overstates or understates the regulatory surface, and the desk will notice.

If the agreement isn't filed yet — common in the first hour — say so and move on. Do not let this
stream block the others.

### Stream C — target 10-K: competition and revenue mix

The cheapest real competitive evidence available at T+0, and the thing an unaided read most often
misses. Pull the target's latest 10-K and take three things:

- The **Competition section verbatim** (`summary=true` locates it; it usually sits inside Item 1).
  Reproduce the competitor list as written and cite the filing — do not paraphrase it. A target
  that names specific rivals hands you the overlap analysis; a target that says only that it
  competes with "global, national and local firms" is telling you the market is fragmented, which
  is itself a finding and should be quoted as such.
- **Segment revenue mix** — which lines carry the revenue, in dollars and percent. This is what
  makes a planned carve-out legible (a segment being separated post-close is 15% of revenue or
  50%, and that changes the read).
- **Geographic revenue mix** — a target with 99% domestic revenue has a very different foreign-
  filing surface than one with a third of revenue in the EU.

Then one line on the buyer's own business from the release, its 10-K if it is a public filer, or
`edgar-company-facts`. Where the buyer is private (common for sponsor and partnership acquirers),
say so — that asymmetry is why this screen stays preliminary.

### Stream D — vector database precedents

Run the same institution-filtered pattern the full skill uses in Phase 7, as a first step rather
than a last one:

- ArbJournal filter and Chain Bridge Research filter, queried with the target and acquirer names,
  the sector, and the buyer-type-matched structure ("bank merger," "going-private," "second
  request [sector]") — harvest review track, announcement-to-close day count, outcome, and
  contemporaneous risk categorization.
- One broad, unfiltered pass on the parties and the sector.
- Cite every hit from its metadata (institution, title, author where present, date). Speed is not
  a license to cite from memory of a search result.

If several differently-framed queries return the same small cluster of unrelated documents, that
is a **coverage gap in the index**, not proof that no precedent exists. Report it that way — it is
useful signal for whoever maintains the corpus, and it stops a thin precedent table from being
read as a considered finding.

## Phase 2 — Buyer classification and preliminary overlap screen

Classify the buyer from what Phase 1 surfaced — acquirer entity, ultimate parent, guarantor, and
how the release describes it:

- **Financial sponsor**: acquisition vehicle tied to a PE fund or family office. Note the sponsor;
  if the release or deck names portfolio companies in the same space, take that as your overlap
  signal rather than building the full portfolio map the way the full skill does.
- **Strategic**: an operating company acquiring in or near its own business.
- **Hybrid / consortium**: an operating acquirer funded or controlled by a sponsor, or a
  sponsor-plus-strategic consortium. Increasingly the common case — note both angles, and say
  which entity carries the competitive footprint and which carries the money.

State the classification with a confidence flag — **confirmed** (clear from entity, guarantor, or
commitment-letter language) or **likely, unconfirmed** (inferred). Don't burn budget forcing
certainty.

**Then build the preliminary overlap screen** from Stream C, one row per identifiable target line:
the target business line, its revenue share, whether the buyer plausibly operates in that line,
the evidence, and a horizontal / vertical / adjacent / no-signal classification. Grade it:

- **Overlap evidenced, unverified** — the target's own Competition section, the deck's market-
  positioning language, or a named portfolio-company match puts the parties in the same line.
  Quote the evidence.
- **Overlap plausible, unverified** — same sector or SIC code, but nothing more specific found.
- **No overlap signal found, but not screened** — none of the above surfaced.

Never render any of these as **clean**. Flash has not defined a market, sized a share, or read the
buyer's own competitor list; only deal-risk-assessment's full screen earns that word. The value of
grading honestly is that "evidenced, unverified" and "no signal, not screened" send the desk to
genuinely different next steps, and collapsing them into one hedge destroys that.

## Phase 3 — Precedent synthesis

Build a short precedent table from the Stream D hits — 3 to 5 rows, buyer-type and sector matched
where possible, each naming the deal, the sourcing institution and date, the review track, the
announcement-to-close day count, and the outcome. Same job as Table 8 in the full report, from one
fast pass rather than a targeted search built on a completed overlap analysis — so present these
as indicative comparables, not the vetted precedent set.

If the index returns nothing on-point, say so plainly rather than stretching a loosely-related deal
to fill the table. A precedent table padded with structurally-unlike deals is worse than an empty
one, because it looks like work was done.

## Phase 4 — Assemble the Flash Read

Compose to `references/flash-report-template.md` — read it before writing. It mirrors
deal-risk-assessment's section names and order so the two reads are the same document at different
resolutions: a Flash Read on Monday and a full assessment on Thursday should slot together, with
the deferred sections filling in rather than the whole thing being rewritten in a new shape.

Two rules govern what goes in it. Every fact must trace to something pulled in Phases 0-3 — where
a field wasn't found, write "not yet known" rather than inferring it to make the template look
complete. And the deferred sections stay visible as stubs rather than being deleted: a reader
needs to see what has *not* been looked at, and a section silently missing reads as a section with
nothing to report.

## Output

Deliver the Flash Read in chat, then save the same content as a short `.docx` (read the `docx`
skill for mechanics; keep it to the template — no cover page, no appendix beyond sources). Present
the file. The whole value of Flash is that it is short: if the document is running past two pages,
the analysis has drifted into the full assessment's territory.

Do not invoke `seed-memory`, `merger-arb-memory`, or any memory-doc tool from this skill.
