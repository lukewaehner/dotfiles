---
name: "merger-arb-memory-doc-v1"
description: "Living merger/risk-arbitrage memory docs for M&A deals — risk-arb counterpart of seed-memory (SPACs stay there). Doc per deal: '[Target] - [Acquirer]' if consideration includes public acquirer stock, else '[Target]'. End-of-day capture for the T+0 pipeline (antitrust minute-1, DMA minute-1, hour-1 consolidation) and for a later-stage S-4/Proxy Review module run (merger-arb-s4-proxy[-vN]) whenever one exists in chat. Never hardcodes a version: resolves and cites whichever ran. Requires a current hour-1 consolidation as reconciliation source, re-triggering if stale. Fixed shape: Open Questions (top), hour-1-format Executive Summary, Street map, Position, On the Horizon — no Body; word-for-word section text lives only in entries (headed CURRENT, superseded on update). Seed Mode (no doc) builds from chat; Update Mode supersedes affected entries. Trigger: seed the arb memory, start/update a deal doc, log this to the deal doc, run merger-arb-memory-doc-v1. Always use for arb memory writes."
---

# Merger-Arb Memory — Living Deal Docs for Risk Arbitrage

Stand up and maintain one canonical memory doc per announced M&A deal. The doc is a living
representation of where the deal stands and what we think of it, built specifically off the firm's
T+0 pipeline: the **Antitrust Minute-1 module** and the **DMA Minute-1 module** produce the deep,
section-by-section analytical work earlier in the chat; the **Hour-1 module** consolidates that
work against everything pasted, uploaded, or live-pulled since (broker notes, ArbJournal, Chain
Bridge Research, IB chats, AlphaSense); this skill is what turns that chat-native consolidation
into the deal's permanent, updatable record.

**A fourth, later-stage module feeds this doc too, whenever it exists.** Once an S-4/proxy has
actually been filed — typically weeks after signing, well after the T+0 pipeline above has already
run — the **S-4/Proxy Review module** (`merger-arb-s4-proxy[-vN]`) produces its own analytical work
(Background of the Merger / interested-party diligence, Deal Snapshot, Key Findings, a six-section
skeleton). This skill checks for that output every time it seeds or updates a doc, folds it in when
present, and does not treat its absence as a problem when it isn't expected yet. A deal doc gets
seeded or updated at all sorts of points in a deal's life — sometimes well before any proxy exists,
sometimes long after one has already been reviewed — so this check runs unconditionally, not just
the first time a doc is created. See "When to fold in an S-4/Proxy Review module run" below.

**All four modules are versioned and will keep changing.** At the time this skill was last revised
the installed versions were `antitrust-minute-1-v5`, `dma-minute-1-v5`, `hour-1-v4`, and
`merger-arb-s4-proxy-v4`, but none of that is load-bearing here — the version number is expected to
move forward (v6, v7, …) independently of this skill. Everywhere below, "the Antitrust Minute-1
module," "the DMA Minute-1 module," "the Hour-1 module," and "the S-4/Proxy Review module" refer to
*whichever version actually produced the output in this chat* (or, for the three this skill can
trigger, whichever version is currently installed — the S-4/Proxy Review module is never triggered by
this skill; see below). See "Resolving module versions" below for exactly how to identify and cite
the right one — read it before Phase 0 on every run, since it governs how every other section's
references to these modules should be resolved.

**One document, two parts, one job each — and a real size constraint that shapes how they connect.**
`update-memory-summary` (the top-layer field: Open Questions, Executive Summary, Street map,
Position, On the Horizon) has a confirmed hard ceiling of roughly 30,000 characters across the
entire field — this was empirically verified twice: a direct write rejection in production, and by
measuring a real deal's actual content (a single module's complete original-plus-updated text ran to
~64,000 characters, more than double the ceiling). Two full minute-1 reports' worth of word-for-word
text cannot live inside that field, and this skill does not try to summarize or index that text into
the top layer either — there is no Body section. `update-memory-doc` (entries) has no comparable
ceiling — each entry caps at ~10k characters but splits cleanly via `Part N/M`, with no practical
limit on how many entries exist. **So the complete, current, word-for-word text of each module's
output lives only in entries — but there is exactly ONE live, authoritative entry (or entry group)
per section at any time.** When new information updates a section, a fresh entry carrying the
complete updated section text supersedes the old one; the old entry is never edited or deleted
(append-only), but it stops being the current record. A reader finds the current text for a section
by reading the entry log directly — the most recent entry headed "CURRENT" for that section is
authoritative; anything it names as superseded is history only. See Core Principle 10 for the
full statement — it is the load-bearing design decision in this skill.

**This skill does not re-run antitrust or deal-mechanics analysis, and it does not reconcile chat
history itself.** That reconciliation — is a source's contribution new, does it conflict with the
minute-1 baselines, what does it change — is the Hour-1 module's job, and this skill treats a
current Hour-1 module run as a required input, not an optional enrichment. If one hasn't run yet in
this chat, or the last one predates material new information, this skill runs it before composing
the doc. Running the Hour-1 module twice (once for its own chat deliverable, once implicitly inside
this skill) is wasted work — always check the chat for an existing, current run first.

---

## Resolving module versions

Do this once, early in every run (Phase 0), and keep the result in mind for every later step that
mentions one of these modules.

- **Each module's name follows a fixed base with a version suffix**: `antitrust-minute-1[-vN]`,
  `dma-minute-1[-vN]`, `hour-1[-vN]`, and `merger-arb-s4-proxy[-vN]`. Treat the base name as the
  identity and the suffix as incidental — this skill's instructions never key on a specific `-vN`.
- **To find which version already ran in this chat**, scan the conversation for each module's own
  output (its report header, memo title, "HOUR-1 CONSOLIDATED UPDATE" banner, or — for the S-4/Proxy
  Review module — its What's New / Deal Snapshot / Key Findings front matter) and read off whatever
  version it actually names itself — don't assume it matches this skill's own last-known versions
  above. If more than one version of the same module ran earlier in the same chat (e.g. an analyst
  re-ran a newer antitrust module after an older one, or a PREM14A run was followed by a DEFM14A
  re-run of the S-4/Proxy Review module once the definitive proxy filed), use the most recent one
  and note in the entry that an earlier version's output was superseded.
- **To trigger a module that hasn't run yet** (most often the Hour-1 module, per "When to (re-)run
  the Hour-1 module" below), check the available skills list for the highest-numbered installed
  variant of that base name and invoke that one — never invoke a specific version number written
  into this file, since it will go stale. **The S-4/Proxy Review module is the one exception: this
  skill never triggers it.** It requires an actual filed S-4/proxy as input, which this skill has no
  way to source or confirm exists — check whether one already ran in this chat (see "When to fold in
  an S-4/Proxy Review module run" below), but never invoke it speculatively.
- **Cite the exact version everywhere this doc references one of these modules** — Executive
  Summary provenance and current-record entries alike. "Per hour-1-v6, 8/14" is correct; "per the
  Hour-1 module" alone is not enough once you know the actual version — the generic name is for
  this skill's own instructions, the specific name is for the doc's citations.

---

## Core Principles

1. **One doc per deal, named by the convention.** `[Target Ticker] - [Acquirer Ticker]` (spaces
   around the hyphen, e.g. `BLFS - RGEN`) when the announced consideration includes stock of a
   public acquirer — all-stock, cash-and-stock, or election structures all qualify. `[Target
   Ticker]` alone otherwise — all-cash deals, PE take-privates, private or foreign-unlisted
   acquirers. The naming keys on consideration, not on whether the acquirer happens to be public.
   The user's explicit naming choice always overrides. See "Doc naming" below for edge cases.

2. **The memory doc is the canonical artifact, not the chat output.** The chat output is a
   confirmation receipt. Real work product lives in the doc, where any future session — and any
   sibling skill — reads it via `read-memory-doc`. Do not paste the full current-record text into
   chat unless asked; offer to show it.

3. **Entries are append-only.** Never overwrite or delete an entry. A superseded current-record
   entry stays in the log permanently as history — it is simply no longer the one a reader treats as
   current once a newer entry replaces it. Factual errors that aren't a supersession (a wrong
   citation, a typo) are fixed by appending a `correction`-tagged entry (or a targeted
   `patch-memory-entry` for a true typo-level repair).

4. **The Hour-1 module is the required reconciliation source for the top layer and the
   current-record entries.** Do not independently re-scan the chat for "what changed since the
   minute-1 baselines" — that is exactly what the Hour-1 module's own gather/reconcile steps already
   do (source inventory, tier-ranked reconciliation, delta analysis), and re-deriving it here risks a
   second, silently-diverging answer. Check the chat for a current Hour-1 module run before
   composing; trigger one if absent or stale (see "When to (re-)run the Hour-1 module" below).

5. **The section list is closed and ordered.** Open Questions → Executive Summary → Street
   map (consensus / off-consensus) → Position → On the Horizon. There is no Body section. Read
   `references/summary-template.md` before composing ANY summary, seed or update — it is the single
   source of truth for section order and format, and it is not a suggestion: a doc missing a
   section, or carrying an extra wrapper section not on that list, is a defective write. That
   Executive Summary section always closes with one more line this skill owns directly, appended
   after whichever Hour-1-family module's eight bullets: **Estimated close (Best / Base / Worst)** —
   three dates, nothing else, pulled from the deal's current-record Entry Price to Target IRR
   scenarios. See `references/summary-template.md` for the exact format and sourcing rule; a doc
   missing this line is as defective as a doc missing an entire section.

6. **Durable state at the top; point-in-time data in dated entries — with the current-record
   exception.** The top layer holds facts that stay true until superseded: Open Questions, Street
   map positions, Position. Live tape (spread, prices, implied probability at today's close) goes in
   `misc`-tagged `[tape]` entries with timestamps (see `references/entry-formats.md`), never in the
   top layer. **The one deliberate exception to "durable state lives at the top": the actual
   complete, word-for-word section text is durable state that lives in entries, never in the top
   layer**, per Core Principle 10 — because the top-layer field cannot physically hold it, and this
   skill does not attempt to summarize or index it there either.

7. **The Open Questions register is the doc's conscience, and it sits first.** Every unresolved
   deal question — will a second request issue, does a foreign regime take jurisdiction, is the
   remedy cap real, will the vote clear — gets a numbered OQ with its opened date and source.
   Alongside genuine analytical unknowns, this section also carries **known sourcing gaps** pulled
   straight from the Hour-1 module's Sources Checked / Open Items output (no Chain Bridge coverage
   yet, agreement not filed, earnings-call sweep not run) — these are what tell the next pass where
   to look, which is the whole point of putting this section first. Resolutions are recorded with a
   date, a one-line answer, and the entry that resolved them; resolved OQs move to the Resolved
   list, never deleted.

8. **Consensus is named, dated, and counted — never vibes.** The Street map is built from the
   Hour-1 module's Attributed Views table and Consistency Check, not re-gathered from scratch. State
   the modal view with its count and as-of date. Off-consensus views are first-class content — name
   the dissenter and their thesis in one line. When a firm moves, log the move with both dates.
   Order firms per `references/sellside-priority.md`; ArbJournal / Chain Bridge Research get their
   own labeled block.

9. **Human views are load-bearing and survive every rewrite.** Attributed desk views ("Walter,
   7/22: …"), bear/bull arguments, and why-we-own-it theses are the most valuable content in the doc
   — they capture a position-holder's reasoning at a point in time and cannot be reconstructed from
   filings. Before any top-layer refresh, inventory them; carry every un-mooted one forward with
   attribution and date. Retire a mooted view explicitly (the entry records what was retired and
   why), never silently.

10. **One current, complete, word-for-word record per section — in entries, never duplicated, always
    superseded on update. There is no top-layer Body; the entry log is the only place this content
    lives.**

    This is a deliberate, evidence-driven design, not a compromise of convenience — read the
    "One document, two parts" note above for the numbers that forced it (a single module's complete
    text runs ~64,000 characters; the top-layer field's ceiling is ~30,000). What follows is how to
    execute it correctly:

    - **Seeding a section for the first time**: write its complete, word-for-word text as one or more
      `diligence`-tagged entries (split via `Part N/M` if it exceeds ~10k characters). This entry
      immediately IS the current record — there is no separate "original" to distinguish it from,
      because nothing has superseded it yet.
    - **Updating a section**: when new information (from the Hour-1 module or the supplemental
      filing sweep) changes a section, write a NEW `diligence`-tagged entry (or entry group)
      containing (a) a short headline naming what changed and from what source — the differential,
      for a reader scanning the log — and (b) the complete, current, word-for-word text of the
      section as it now stands, in full, not the old text plus a note. Head the entry explicitly:
      "CURRENT — [module] Section [X], updated [date] — supersedes entry [N]." The prior entry is
      never edited or deleted; it simply stops being the one a reader treats as current.
    - **Never let two entries simultaneously read as "the current text" for the same section.** If a
      section has been updated three times, only the third (newest) entry is ever cited by a later
      update as the baseline to supersede. The first two remain in the log as history, not as
      competing "current" versions — this is the specific failure this design exists to prevent (an
      earlier version of this skill kept a permanently-stale verbatim original alongside a
      separately-maintained "updated" version, and a reader had no single place to look for "what's
      true now").
    - **Tables especially** — the Risk Matrix, Approvals & Gates, Regulatory & Deal-Protection
      Architecture, Overlap Screen, Verbatim Competitor Disclosures, Precedent Transactions, Summary
      Matrix, and any other table the minute-1 reports produced — are reproduced with every row and
      column intact in the current-record entry, updated row-by-row when a delta lands, never
      summarized into prose elsewhere.
    - **Before writing or superseding any current-record entry, run this check:** did this text come
      from copying/carrying forward the actual minute-1 module output as it appears earlier in this
      chat (with the delta folded in at the specific point it applies), or did I just write new
      sentences describing what that output said? If the latter, stop and fix it. A useful test: the
      analyst who ran the original antitrust-minute-1 or dma-minute-1 report should be able to
      recognize every sentence in the current-record entry as their own (or, for an updated section,
      as what their own report would now say given the new information).

11. **Anti-hallucination discipline, inherited from the minute-1 modules.** Cite every fact: filings
    by form + date, notes by firm + date, vector-database items inline from the hit's own metadata,
    prices by timestamp. Completion language is qualitative and precedent-grounded — never emit a
    bare probability percentage from intuition (the one exception, per the minute-1 modules' own
    convention, is the Entry Price to Target IRR block's IRR/spread math, which is a pricing
    calculation, not a fabricated clearance estimate). Do not invent market shares or fill gaps — a
    stated gap is an Open Question.

12. **This doc has no blind wall, but provenance labels survive.** Spread levels, price targets, and
    implied-probability views are recordable here — dated, attributed, in the right place. When
    folding in Antitrust or DMA Minute-1 content that carries its own hedging or epistemic-status
    labels ("not determinable from public sources," "reported-only"), preserve those labels exactly
    through every rewrite — this is the same degradation risk the minute-1 modules guard against in
    their own compression, and it applies here with equal force.

13. **Seed light off whatever exists; update forever.** A thin seed with honest gaps (logged as OQs)
    beats a delayed one — the doc's value compounds with every update, so start it as soon as the
    Hour-1 module has run once. There is no deep-dive substitute skill this module hands off to; the
    depth already lives in the Antitrust and DMA Minute-1 modules, and this skill's job is to keep
    their combined output current, not to re-derive it.

14. **The desk's closing date, and "our view" on closing, is the date on the deal's tear sheet.**
    Wherever this doc says "desk view," "our view," "house view" or "our estimate" about when the
    deal closes (the Street map's "where we differ" line, a broker's date measured against ours, the
    Executive Summary's dates), use the **Est Deal Close Date** on the deal's tear sheet, not a date
    this skill or a minute-1 module worked out on its own. The tear sheet is a spreadsheet in the
    Interns shared drive, usually named `<TICKER> Tearsheet.xlsx` or `<TICKER> Merger Arb Tear
    Sheet.xlsx`; find it with `lookup-drive-file` and read it with the Google Drive connector's
    `read_file_content` (`download-drive-file` cannot read .xlsx files). Two exceptions, and only
    these: the user gives a different date for this run, or the tear sheet is missing, unreadable or
    has no close date. In those cases use the module-derived date and say plainly in the doc which
    one was used and why. When a tear-sheet date exists it takes priority: it is the analyst's date
    after deep research, so show only the tear-sheet date as the desk's view and do not show a
    module-derived date beside it as a competing view. This principle only decides which date is
    called the desk's; it does not change how the Estimated close (Best / Base / Worst) line is built.

---

## Doc naming

Resolve the name BEFORE creating the doc:

- Determine target ticker, acquirer ticker, and consideration type from the minute-1 reports (or
  the press release / 8-K if neither has run yet).
- Consideration includes acquirer stock (all-stock, fixed exchange ratio, cash-and-stock, cash/stock
  election) AND the acquirer is a public company → `[Target Ticker] - [Acquirer Ticker]`, exactly
  that punctuation: `BLFS - RGEN`.
- All-cash, or the acquirer is a PE sponsor / consortium / private or unlisted company →
  `[Target Ticker]`: `BLFS`.
- Edge cases: two-step tender offers follow the same rule on the offer consideration. Foreign
  acquirers use the primary-listing ticker. If a later amendment changes the consideration type,
  keep the original doc name (renaming orphans history) and record the change in a `filing` entry
  and a new current-record entry for the affected deal-terms section.
- Check `list-memory-docs` for BOTH candidate names (and near-variants) before creating, so one deal
  never accumulates two docs. If a duplicate is found, tell the user rather than guessing which to
  keep.

## Tools

- **Memory docs**: `list-memory-docs` (existence check, always first), `create-memory-doc(name,
  author="Claude")` with no seed summary, `update-memory-doc(name, tag, author, body)` to append
  entries — this is where current-record text lives (~10k char body limit — split into "Part N/M"),
  `update-memory-summary` (wholesale top-layer write — the field with the ~30k ceiling; holds only
  Open Questions, Executive Summary, Street map, Position, and On the Horizon — never section text),
  `patch-memory-summary(name, edits=[{old_str, new_str}])` (PREFERRED for targeted edits to the top
  layer), `patch-memory-entry` (typo-level entry repair only), `read-memory-doc(name,
  entries_limit?, summary_only?)`.
- **EDGAR** (`edgar-filings`, `edgar-filing-index`, `edgar-filing-text`): used for this skill's own
  supplemental filing sweep — see "Supplemental filing sweep" below. This is the one piece of
  gather work the Hour-1 module does not do itself.
- **The Hour-1 module (Skill tool)**: the required reconciliation dependency — see "When to
  (re-)run the Hour-1 module" below. Invoke it by whichever installed version resolves per
  "Resolving module versions" above; it is a skill to invoke, not a data source to query directly.
- **Uploaded research / Outlook / web search / Bloomberg pricing**: only as needed to fill a gap the
  Hour-1 module's own sweep didn't cover — this skill leans on its live pulls (ArbJournal, Chain
  Bridge Research, broker emails, live pricing) rather than re-running them.

**A note on the tools' own guidance, and why it doesn't govern the current-record entries.**
`update-memory-summary`'s two-step interface returns a rewrite prompt suggesting "~2 pages of dense
text" — that guidance is aimed at the top-layer field specifically (which holds no section content at
all under this design) and was never a statement about the doc's total capacity. It has no bearing on
entries, which is where the actual complete text belongs.

## When to (re-)run the Hour-1 module

Before composing or refreshing anything, check this conversation for the most recent Hour-1 module
output (whichever version produced it — see "Resolving module versions") and its "As of [date,
time ET]" stamp:

- **No Hour-1 module output anywhere in this chat** → run it now (resolve the installed version per
  "Resolving module versions," then invoke it) before proceeding. There is no fallback path that
  skips this — the Executive Summary format and the current-record entries both depend on its
  output.
- **An Hour-1 module output exists but predates material new information** (a filing, milestone, or
  research item has landed in the chat since its "As of" stamp that isn't reflected in it) → run it
  again. "Material" is a judgment call; when in doubt, re-run — a stale reconciliation silently
  degrades both the Executive Summary and the current-record entries.
- **A current Hour-1 module output already reflects everything relevant** → use it directly, do not
  re-run. Say so in the chat receipt ("reused hour-1-v[N] run from [time]" — name the actual
  version).

## When to fold in an S-4/Proxy Review module run

Unlike the Hour-1 module, this skill never triggers the S-4/Proxy Review module itself — it needs an
actual filed S-4/proxy to run against, and this skill has no path to confirm one exists or to source
it. All this skill does is check whether one already ran in this chat, and fold it in if so.

- **Scan this conversation for an S-4/Proxy Review module output** (its own report header, or the
  What's New / Deal Snapshot / Key Findings front matter the module always produces) every time this
  skill runs — Seed Mode or Update Mode, not just the first time. A doc can be seeded well before any
  proxy exists, and updated long after one has already been reviewed; neither timing is the default
  case, so check unconditionally rather than assuming based on the doc's own age.
- **None found** → this is the ordinary case for most of a deal's life (pre-signing, or signed but
  pre-proxy). Do not treat it as a gap, and do not open an Open Question or a "known sourcing gap"
  line about it — a proxy that isn't expected yet isn't a missing input. (If the DMA Minute-1
  module's own timeline read puts a proxy filing as imminent, that belongs in On the Horizon as a
  next-gating-event note, same as any other expected milestone — not framed as something this skill
  failed to find.)
- **One found, and it isn't reflected in the doc yet** — true by definition in Seed Mode; in Update
  Mode, true when the module's own run postdates the doc's last entry, or when a newer run (e.g. a
  DEFM14A re-run of an earlier PREM14A pass) supersedes what's already logged — → fold it in per
  "Logging S-4/Proxy Review content" below before finishing the doc.
- **One found and already current** → nothing to do; say so in the chat receipt the same way an
  already-current Hour-1 module run is noted as reused rather than re-run.

### Logging S-4/Proxy Review content

The module produces a fixed shape — Deal Snapshot, Key Findings, and a six-section skeleton (with
tables, most notably the Background of the Merger's Interested-Party Characteristics Table) — plus a
capped, two-paragraph What's New section that is transient by the module's own design.

- **Deal Snapshot, Key Findings, and Sections 1–6 are current-record content**, logged exactly like
  an Antitrust or DMA Minute-1 section per Core Principle 10 — complete, word-for-word, tables
  reproduced row-by-row, headed "CURRENT — S-4/Proxy Review, [section name], [seeded/updated]
  [date]," and superseded (never edited in place) if a later run of the module changes them. These
  get their own current-record entries; they do not fold into or overwrite the DMA Minute-1 module's
  existing entries, since the two modules cover different stages of the same deal and both stay
  readable in the log.
- **What's New is not logged as its own current-record section** — it's already a delta summary by
  the module's own design, not durable content. Instead, pull its substance into the `filing`
  differential entry that accompanies the current-record write (per U.4's format): what the proxy
  firmed up or changed (closing timeline, financing, regulatory dates, sale-process read), and which
  current-record entries — the S-4/Proxy Review sections just logged, and any DMA Minute-1 entry
  (Closing Risk, Gross Spread) the same facts also affect — now reflect it.
- **Same supersession discipline as any other section**: if the module reruns (an amendment, a
  DEFM14A after a PREM14A), only the newest run's Sections/Deal Snapshot/Key Findings are ever
  "CURRENT" for this module; the prior run's entries stay in the log as history.

## Supplemental filing sweep

The Hour-1 module's own gather step covers ArbJournal, Chain Bridge Research, broker/sell-side
emails, and live pricing — it does not sweep EDGAR. Before touching any current-record entry, run
one `edgar-filings` check for anything filed since the doc's last entry date (Update Mode) or since
the announcement 8-K (Seed Mode) that the minute-1 baselines and the Hour-1 module's own
reconciliation haven't already captured — an amendment 8-K, a DEFM14A, a 425, a second-request
disclosure. Fold anything found into a fresh current-record entry for the affected section (per Core
Principle 10) and log a short `filing` differential entry alongside it. If nothing new turns up, say
so in the chat receipt rather than silently skipping the check.

## Phase 0 — Mode detection (always first)

1. Resolve module versions per "Resolving module versions" above — this governs every reference
   below.
2. Identify the deal: target, acquirer, tickers, consideration type — from the minute-1 reports if
   they've run, else the press release / 8-K. Resolve the doc name per the naming rule.
3. `list-memory-docs` — look for both candidate names. Doc exists → **Update Mode**. Doc absent →
   **Seed Mode**.
4. Resolve the Hour-1 module dependency per "When to (re-)run the Hour-1 module" above — do this
   before either mode's remaining steps, since both modes consume its output.
5. Check for an S-4/Proxy Review module run per "When to fold in an S-4/Proxy Review module run"
   above — this applies in both modes and regardless of the doc's own age relative to the proxy.

---

## Seed Mode

### S.1 — Confirm inputs

By the time Seed Mode runs, the chat should already contain Antitrust Minute-1 module output, DMA
Minute-1 module output, and a current Hour-1 module consolidation (Phase 0 step 4 ensures the last
one). If the Antitrust or DMA Minute-1 module never ran — the Hour-1 module's own Sources Checked
table will say so — proceed anyway; missing minute-1 legs become Open Questions and "On the
horizon" items rather than blockers, same as the base skill's original seed-light doctrine.

Also check for an S-4/Proxy Review module run (Phase 0 step 5). This is genuinely optional, not a
missing leg to flag: most deals get seeded long before any proxy exists, so its absence here is the
normal case, not a gap. If one is present — a deal doc seeded well after the proxy stage, for
instance — it gets logged in S.3 alongside the minute-1 sections, not treated as a bonus extra.

### S.2 — Supplemental filing sweep

Run the EDGAR sweep described above.

### S.3 — Log the current-record entries

For each section of both modules (Antitrust Sections A–G; DMA's Executive Summary, Approvals &
Gates, Regulatory & Deal-Protection Architecture, deal-mechanics extraction, Closing Risk Assessment,
Gross Spread Calculation), append its complete, word-for-word text — as it currently stands, meaning
with any delta the Hour-1 module or the supplemental sweep (S.2) already surfaced folded directly
into the relevant section's text before it's logged, not written stale-then-patched — as one or more
`diligence`-tagged entries (`Part N/M` if a section exceeds ~10k characters). This is the first
current-record entry for each section; there is nothing to supersede yet.

If an S-4/Proxy Review module run is present (Phase 0 step 5), also log its Deal Snapshot, Key
Findings, and Sections 1–6 as current-record entries the same way, per "Logging S-4/Proxy Review
content" above — these are a fourth, later-stage set of sections alongside the Antitrust/DMA ones,
not a substitute for them.

### S.4 — Create the doc and write the top layer

`create-memory-doc(name="<DOC NAME>", author="Claude")`. If it returns `already_exists`, stop —
Phase 0 should have caught it.

Compose the top layer per `references/summary-template.md`: Open Questions, Executive Summary (the
Hour-1 module's own bullet output, reproduced in its locked format), Street map (from the Hour-1
module's Attributed Views table + Consistency Check), Position (omit if none stated), On the Horizon
(from the Hour-1 module's Open Items). There is no Body section — the top layer never restates or
indexes the section content that S.3 just logged.

Write via `update-memory-summary`. This field should comfortably stay well under its ~30k ceiling,
since it never holds section text or an index of it.

### S.5 — Chat receipt

Doc name, current-record entries logged (module, section, entry numbers), top-layer sections
written, OQs opened, which module versions were used (name them explicitly), Hour-1 module run
reused or freshly triggered, whether an S-4/Proxy Review module run was found and logged (or that
none exists yet, if that's the expected state at this deal stage), and any missing legs.

---

## Update Mode

### U.1 — Read the doc first

`read-memory-doc(name="<DOC NAME>", entries_limit=-1)`. Note the last entry date, which entry is
currently the "CURRENT"-headed record for each section, the open OQs, and the standing desk views
(Core Principle 9 inventory).

### U.2 — Resolve the Hour-1 module dependency

Per "When to (re-)run the Hour-1 module" above, using the doc's last-update timestamp as the
freshness baseline rather than the chat's own prior Hour-1 module stamp — a doc updated after the
last Hour-1 module run but before something new landed still needs a fresh one.

### U.2b — Check for a new S-4/Proxy Review module run

Per "When to fold in an S-4/Proxy Review module run" above, using the doc's last-update timestamp
(not the chat's own prior check, if any) as the freshness baseline. This is the step that catches the
common real-world case this skill is otherwise blind to: a doc seeded before any proxy existed, now
being updated in a chat where an S-4/Proxy Review module run has since happened — its output doesn't
announce itself to Update Mode any other way, so this check has to run every time, not just when the
analyst happens to mention the proxy. Finding nothing here is expected and fine at most deal stages;
it is not itself a delta.

### U.3 — Supplemental filing sweep

Per "Supplemental filing sweep" above, scoped to since the doc's last entry date.

### U.4 — Supersede the affected current-record entries

For every delta the Hour-1 module (U.2), the S-4/Proxy Review check (U.2b), or the supplemental
filing sweep (U.3) surfaced: identify which section it affects, read that section's *currently-cited*
entry (per U.1, not the original minute-1 chat output), and write a new `diligence`-tagged entry
containing the complete, current, word-for-word text of the section given the new information,
headed "CURRENT — [module] Section
[X], updated [date] — supersedes entry [N]." Sections with no delta are not touched — their existing
current-record entry stays authoritative.

Also log a short differential entry (`filing`, `misc [milestone]`, etc., per the mapping table)
alongside the supersession — what changed, from what source, as of when — so a reader scanning the
log gets the headline without opening the full current-record entry.

### U.5 — Rebuild the rest of the top layer

- **Open Questions** — additions and resolutions (see U.6), always reviewed even when the new item
  seems unrelated.
- **Executive Summary** — rebuilt to the Hour-1 module's latest output whenever a new run happened
  in U.2.
- **Street map** — consensus count and as-of date; firm moves flagged explicitly with dates.
- **Position / On the Horizon** — as they change.

There is no Body to repoint — the top layer never referenced the superseded entries by citation, so
nothing there needs updating beyond the sections above.

Prefer `patch-memory-summary` with targeted `old_str → new_str` edits for all of the above; reserve
a full `update-memory-summary` rewrite for wholesale restructures (consideration amended, deal
recut, terminal event). Apply the Core Principle 9 inventory before any rewrite: every standing
human view is carried forward or explicitly retired in the entry.

### U.6 — Open Questions discipline

Every update reviews the register. New unknowns get the next OQ number with date + source (analytic
gaps from the minute-1/Hour-1 reconciliation, plus sourcing gaps from the Hour-1 module's Sources
Checked / Open Items). Resolved OQs move to the Resolved list with date, one-line resolution, and
entry reference. Never renumber, never delete.

### U.7 — Terminal events

Deal closed, terminated, topped, or recut-to-different-buyer: append the `misc`-tagged `[milestone]`
entry, supersede the Executive Summary and the affected current-record entries to reflect the
outcome (legitimate full-rewrite case for those), sweep the OQ register — each open question
resolved or marked moot, with dates — and record the final state. The doc stays as the deal's
permanent record; note in On the Horizon that tracking has ended.

### U.8 — Chat receipt

Which sections were superseded (old entry number → new entry number) and why, which other top-layer
sections changed, OQs opened/resolved, which module versions were used (name them explicitly),
whether the Hour-1 module was reused or re-run, whether an S-4/Proxy Review module run was found and
folded in (or that none exists), and whether the supplemental sweep found anything. Keep it short —
the doc is the deliverable.

---

## Street map rules (consensus / off-consensus)

- The map lives in the top layer in two sections — consensus and off-consensus — with the
  underlying per-note records in `misc`-tagged `[research]` entries. Source it from the Hour-1
  module's Attributed Views table and Consistency Check rather than re-gathering.
- Consensus line: modal view + count + as-of. Below it, one line per firm: firm — analyst —
  latest-note date — track call — timeline — one-line thesis, ordered per
  `references/sellside-priority.md`.
- Off-consensus: every named dissent with its thesis, plus the ArbJournal / Chain Bridge block, plus
  where WE differ from consensus and why.
- Moves are first-class: when a firm's view shifts between Hour-1 module runs, flag it inline with
  both dates.
- De-dup the same note arriving through multiple channels to one record, fullest copy, all channel
  tags.

## Relationship to sibling skills

- **The Antitrust Minute-1 module / the DMA Minute-1 module** — the deep, cited, section-by-section
  analytical work the current-record entries are built from and kept current with. This skill never
  re-runs their analysis; it carries their output forward, word-for-word, superseding the relevant
  entry whenever something changes. Resolve which installed version actually ran per "Resolving
  module versions" above — never assume a specific one.
- **The Hour-1 module** — the required reconciliation dependency (see "When to (re-)run the Hour-1
  module" above). Its own closing note says explicitly that capturing its output into the end-of-day
  record is this skill's job — that hand-off is the normal way this skill gets invoked.
- **The S-4/Proxy Review module (`merger-arb-s4-proxy[-vN]`)** — a later-stage, optional input this
  skill checks for and folds in per "When to fold in an S-4/Proxy Review module run" above, never
  triggers itself. The relationship runs both ways: that module's own baseline-sourcing order checks
  this skill's memory doc as one of its sources when it runs, and this skill in turn logs that
  module's output back into the doc once it exists — each keeps the other current rather than one
  being a dead end for the other's information.
- **`seed-memory`** — SPAC docs only. A SPAC business combination is not a merger-arb deal doc;
  route it there.
- **`merger-agreement-extraction`** — largely superseded by the DMA Minute-1 module in this
  pipeline; if it's still run standalone on a deal, fold its findings into the affected section via a
  new current-record entry, the same as any other delta, and log the differential per U.4.

## References

- `references/summary-template.md` — the closed section list and full top-layer template (no Body
  section), including the locked Hour-1-module Executive Summary format. Read before composing ANY
  summary, seed or update.
- `references/entry-formats.md` — the conceptual entry-tag vocabulary, its mapping onto the tool's
  actual fixed tag set, and per-tag formats — including the current-record `diligence` entry format
  and its supersession header.
- `references/sellside-priority.md` — firm ordering for the Street map.

---

## Appendix: Bundled Files

The files this skill points to (`references/...`, `scripts/...`) are embedded below, verbatim, under their original paths. When the instructions say to read a reference file, read its section here. To run a script, write its block to a file of the same name in the working directory first (e.g. `scripts/buy_write.py`), then run it from there.

### `references/summary-template.md`

````markdown
# Merger-Arb Memory — Top-Layer Template

This file is the single source of truth for the doc's top layer (everything above the entry log).
Both modes read it: Seed Mode composes it fresh; Update Mode patches it while keeping it conformant.
The section order is fixed and closed: **Open Questions → Executive Summary → Street map —
consensus → Street map — off-consensus → Position → On the Horizon.** There is no Body section — do
not add one, a Verdict Block, At-a-glance, Snapshot, TL;DR, or any other wrapper section. Omit
Position gracefully when no position has been stated (never invent one); every other section always
appears, even if one line.

**Durability rule:** the top layer holds facts that stay true until superseded. No live tape
anywhere in it — spread, bid/ask, current prices, and implied probability live only in timestamped
`misc`-tagged `[tape]` entries. (The complete, current-record Entry Price to Target IRR pricing
lives inside the relevant current-record entries per `SKILL.md` Core Principle 10, not in the top
layer.)

**Provenance rule — always name the exact module version, never the generic name.** "The Hour-1
module" and "the Antitrust/DMA Minute-1 modules" (per `SKILL.md`'s "Resolving module versions") are
this skill's own internal shorthand; a reader of the doc should never see that shorthand. Every
section below states, in one line at its head or in its own citations, the specific version that
produced it — "per hour-1-v6, [date/time] ET" for the Executive Summary and Street map.

**There is no Body section — read this before composing anything.** Per `SKILL.md` Core Principle
10, the complete, word-for-word current text of every Antitrust/DMA Minute-1 section lives only in
`diligence` entries — exactly one live current-record entry per section at any time, headed
"CURRENT," always superseded (never duplicated) on update. The top layer never reproduces, summarizes,
or indexes that text — not even as a pointer or a short description. A reader who wants a section's
current content reads the entry log directly. Do not add a section, subsection, or line anywhere in
the top layer whose purpose is to describe or cite what a current-record entry says.

---

## Template

```markdown
## [DOC NAME] — [Acquirer] acquiring [Target]
Announced [date]; [all-cash $X.XX / [ratio] stock / cash+stock mix]; status: [pending — pre-HSR /
HSR waiting / second request / S-4 pending / vote set [date] / closed [date] / terminated [date]]
Last updated: [date, time ET] — [hour-1-vN] run of [date, time ET] [reused / freshly triggered]

### Open Questions

- OQ-1 (opened [date], [source]): [question] — OPEN
- OQ-2 (opened [date], [source]): [question] — RESOLVED [date]: [one-line resolution] (entry [ref])
[Numbering never reused; resolved items keep one line each, never deleted.]

**Known sourcing gaps** (from the current Hour-1 module run's Sources Checked / Open Items, or this
skill's own supplemental filing sweep): [e.g. "no Chain Bridge Research coverage yet"; "merger
agreement not yet filed — deal terms below are PR-only"; "earnings-call sweep not run since
[acquirer]'s last print"]. These are not OQs (they're not questions, they're missing inputs) — kept
in this section because both tell the next pass where to look before it starts.

### Executive Summary

[Reproduce the current Hour-1 module run's locked eight-bullet Executive Summary output verbatim, in
its own fixed order and format — do not re-derive, re-summarize, or re-order it here. Head this
section with the exact version that produced it, e.g. "per hour-1-v6, 8/14 14:20 ET":]

- **Transaction** — ...
- **Lifecycle** — ...
- **Dates** — ...
- **Structure** — ...
- **Financing** — ...
- **Antitrust conclusion** — [verdict]
  – [supporting fact]
  – [supporting fact]
- **MAE/MAC** — ...
- **Street** — ...

[If no installed Hour-1-family module has ever produced this exact shape (shouldn't happen per the
Phase 0 dependency check, but if it does), do not improvise a substitute format — stop and run the
current Hour-1 module first.]

**Estimated close (Best / Base / Worst):** [date] / [date] / [date]

[This one-line addition is this skill's own — layered after the Hour-1 module's eight bullets above,
never mixed into them or used to reinterpret them. It prints ONLY the three dates, nothing else: no
scenario names, no day-counts, no spread/IRR figures, no hedging language. (Any caveat about how
firm the estimate is belongs in Known sourcing gaps or On the Horizon, where the doc already has a
place for that.) Pull the three dates straight from whichever Entry Price to Target IRR entry is
currently CURRENT for this deal — that block already carries a three-scenario date table (typically
Baseline-30 / Baseline / Baseline+30, though a deal may name its scenarios differently): the
earliest/most-optimistic date is Best, the central/primary scenario is Base, the
latest/most-conservative date is Worst. This is a presentation line, not new analysis — never compute
or estimate a date here that doesn't already exist in a current-record entry. Write each date as
"Month DD, YYYY" (e.g. "April 15, 2027") — spelled-out month, no abbreviation, matching how dates
already appear elsewhere in this template — so the line reads the same way regardless of which run
or module produced the underlying scenario dates. If more than one Entry Price to Target IRR block
is current at once (a deal can carry scenarios at more than one target-IRR hurdle — the entry-price
methodology's 8% default is one parameterization, not the only one a desk might run), use the block
run at the desk's default/unspecified hurdle; if every current block states an explicit non-default
target IRR with none marked as the default, use the one the doc's Position or On the Horizon section
already treats as the working scenario, and if that's ambiguous too, say so as a one-line Known
sourcing gap rather than silently picking one. If the deal has no Entry Price to Target IRR entry yet
(very early T+0, or a deal type where that block doesn't apply), write "Estimated close (Best / Base
/ Worst): not yet estimated" rather than omitting the line or inventing dates.]

### Street map — consensus

[modal view + count + as-of, sourced from the current Hour-1 module run's Attributed Views table:
"clean-Phase-1 close in Q4: 5 of 7 attributed firms, as of 8/1"]
- [Firm — Analyst ([date of latest note]): track call · timeline · one-line thesis] (ordered per
  references/sellside-priority.md)
- [next firm …]

### Street map — off-consensus

[named dissents + one-line theses; flag moves inline: "Jefferies: clean → expects second request
(8/14)"]
- [ArbJournal / Chain Bridge block, when coverage exists, cited from hit metadata]
- Where we differ from consensus: [one or two lines, or "we sit with consensus because …"]

### Position

[durable framing only — shares/notional, % of float if known, "as of [date]"; omit the section
entirely if no position stated]

### On the Horizon

- [Next gating event]
- [Remaining data gaps not already captured as Known sourcing gaps above]
- [What the next update should fill]
```

---

## Composition notes

- **Open Questions sits first** because it's the doc's entry point for "what do we still need to go
  find" — a reader picking this doc back up after time away should see the gaps before the verdict,
  not after.
- **Executive Summary belongs to whichever Hour-1 module version produced it, not to this skill.**
  Do not paraphrase it, shorten it further, or reorder its eight elements — any quality issue with
  it belongs to that module's own instructions, not to a rewrite here. If it looks wrong, that's a
  signal to re-run the current Hour-1 module or flag it, not to patch it in place.
- **The Estimated close (Best / Base / Worst) line is the one exception to "don't touch the Executive
  Summary" — because it isn't Hour-1's content, it's this skill's own, appended after Hour-1's eight
  bullets.** Treat it with the same rigor as the closed section list itself: a doc missing this line,
  or one that pads it with anything beyond the three dates, is a defective write, exactly like a doc
  missing a required section. `update-merger-arb-memory-doc-v2` is the one responsible for keeping it
  current after the initial seed — see that skill's own instructions for when it refreshes.
- **No Body, and no substitute for one.** This template holds no index, pointer, or condensed
  description of the Antitrust/DMA Minute-1 section content anywhere. If a future edit is tempted to
  add "just a short summary line" per section, that is a Body by another name — the complete text
  belongs only in the entry log (`SKILL.md` Core Principle 10), and the top layer stays free of it
  entirely, not lightly touching it.
- **Street map** rows compress per-note records; don't duplicate whole notes into the top layer. A
  firm with multiple notes shows its latest view with the date, plus a move flag if it shifted.
- **On the Horizon** is scannable, not exhaustive — the exhaustive gap list is Known sourcing gaps
  under Open Questions; this section is just the next few things to watch for.
- **Never write a bare "hour-1-v4" or "antitrust-minute-1-v5" into these instructions themselves as
  if it were fixed** — those are today's installed versions, not a permanent identity. Every mention
  of a specific version number in this doc's actual *output* is a live citation to what really ran;
  every mention of a module in this skill's *own instructions* should read generically (Hour-1
  module, Antitrust Minute-1 module, DMA Minute-1 module) per `SKILL.md`'s "Resolving module
  versions."
````

### `references/entry-formats.md`

````markdown
# Merger-Arb Memory — Entry Tags and Formats

Every entry is appended via `update-memory-doc(name, tag, author, body)` and is permanent — entries
are the deal's audit trail. But under the current-record design (`SKILL.md` Core Principle 10),
entries carry more than a differential trail: **entries are also where the complete, word-for-word
current text of each Antitrust/DMA Minute-1 section actually lives.** There is exactly one live
current-record entry per section at any time. There is no Body section anywhere in the doc — the
top layer never reproduces, summarizes, or indexes that text. A reader finds a section's current
content by reading the entry log directly; the most recent entry headed "CURRENT" for that section
is authoritative.

This means two different kinds of entry content coexist, and it's important not to blur them:

1. **Current-record entries** (always tagged `diligence`) — the complete, word-for-word text of one
   report section, headed to make unambiguous that it is the live version and what it supersedes.
2. **Everything else** (`filing`, `misc [milestone]`, `misc [research]`, `misc [tape]`, `misc [view]`,
   `correction`, `open-question`, `close-question`, etc.) — differentials: what changed, from what
   source, and which current-record entry now reflects it. These do NOT reproduce report text; they
   name the current-record entry that does, by number.

**Universal rules:**

- Lead line: `[YYYY-MM-DD] — [headline]` (the date is the event/receipt date, not necessarily today).
- Cite every fact: filings as form + filing date (accession number where practical); notes as firm +
  analyst + date; vector-database items inline from the hit's returned metadata; prices with a
  timestamp. Name the exact module version for anything sourced from the Antitrust, DMA, Hour-1, or
  S-4/Proxy Review modules (e.g. "antitrust-minute-1-v5," "hour-1-v6," "merger-arb-s4-proxy-v4") —
  per `SKILL.md`'s "Resolving module versions,"
  never write these tags as fixed version numbers in the *instructions*, but every actual entry
  names the real version that ran.
- If the entry resolves or opens an Open Question, say so by number ("opens OQ-6", "resolves OQ-3")
  — the top-layer register and the entry stream must agree.
- One differential entry per update batch, tagged by dominant type. A second request arriving
  alongside two broker reactions is one `misc [milestone]` entry that includes the reactions (or
  paired with a `misc [research]` entry if the research is substantial) — judgment, not ceremony.
  Current-record entries are separate from this batching: log one current-record entry per section
  that actually changed, alongside (not merged into) the differential entry describing the change.
- **Never let a differential entry drift into reproducing the section text it's describing.** If a
  `misc [milestone]` or `filing` entry is running long because it's carrying the actual new/updated
  language rather than describing the change and citing the current-record entry, stop — that text
  belongs in a `diligence` current-record entry per `SKILL.md` U.4, and the differential entry should
  just point to it.
- **Never let two `diligence` entries simultaneously read as "the current text" for the same
  section.** The newest one says so explicitly in its header ("CURRENT ... — supersedes entry [N]");
  older entries for that section are history only, never deleted (append-only), but never current.

## Tag vocabulary

**The tool (`update-memory-doc`) only accepts a fixed set of tags: `call-notes`, `close-question`,
`correction`, `diligence`, `filing`, `misc`, `open-question`, `trade`. It will reject anything else.**
The conceptual categories below are this skill's own vocabulary for organizing entry *content* — most
map directly onto a tool tag, but several don't have a matching tool tag and must be logged as `misc`
with the conceptual label as a bracketed prefix in the entry body (e.g. `[research] ...`). This isn't
a workaround to route around later — it's the permanent mapping, because the tool's tag set is what it
is. Do not invent or attempt to pass a tag not in the tool's list; it will fail the call.

| Conceptual category | Actual tool tag to use | Use for |
|---|---|---|
| current-record | **`diligence`** (direct match) | The complete, word-for-word current text of one Antitrust Minute-1, DMA Minute-1, or S-4/Proxy Review module section (Deal Snapshot, Key Findings, Sections 1–6 — not the S-4/Proxy Review module's own transient What's New) — seeded fresh (S.3) or superseding a prior current-record entry on update (U.4/U.2b). This is the doc's actual content, not a pointer. |
| `filing` | **`filing`** (direct match) | A new or amended SEC filing distilled: what changed and which current-record entry now reflects it, cited to form + filing date. Not the filing's full text — that lives in the current-record entry it feeds. |
| `milestone` | `misc`, prefixed `[milestone]` | Regulatory / process events: HSR filed, waiting period expired, pull-and-refile, second request, agency complaint or clearance, remedy agreement, S-4 effective, vote result (exact counts), close, termination — what happened and which current-record entries it changed, not a full narrative |
| `research` | `misc`, prefixed `[research]` | Sell-side / ArbJournal / Chain Bridge / vector-database items: attributed per-note records, Street map changes |
| `tape` | `misc`, prefixed `[tape]` | Dated spread observations: prices, consideration value, gross/blended spread, annualized at scenario — always timestamped |
| `view` | `misc`, prefixed `[view]` | Desk views and stance changes: whose view, dated, and why it moved |
| `diligence` (non-current-record) | **`diligence`** (direct match) | Deeper analytical work distilled from a source outside the standard pipeline (e.g. a standalone merger-agreement extraction) that produces a new current-record entry — logged the same way as any other current-record update |
| `consolidation` | `misc`, prefixed `[consolidation]` | An Hour-1 module run folded into the doc (name the exact version): what it reconciled, which current-record entries it superseded, and whether it was reused or freshly triggered |
| `correction` | **`correction`** (direct match) | Fixes to prior entries or top-layer lines — what was wrong, what is right, which entry or top-layer line it corrects. A correction that changes section text itself is logged as a new current-record entry, not as a `correction` entry containing the text. |
| — | **`open-question`** (direct match, use when available) | An entry whose primary purpose is opening one or more new Open Questions — prefer this over folding the OQ into whatever other tag the surrounding content would otherwise get, when the OQ is the main point of the entry |
| — | **`close-question`** (direct match, use when available) | An entry whose primary purpose is resolving one or more Open Questions |
| — | `misc`, prefixed `[call-notes]` if not literal call notes | `call-notes` is a real tool tag but its intended use (notes from an actual call) doesn't map to any category above — use it directly only for genuine call/conversation notes, not as a catch-all |

## Per-tag skeletons

### `diligence` — current-record entry (seeding a section)

This is the doc's actual content for one section. Log one of these per section when seeding
(`SKILL.md` S.3), before the top layer is written.

```
[2026-07-25] — CURRENT — DMA Minute-1, Approvals & Gates, seeded 2026-07-25
Source: dma-minute-1-v5, run 2026-07-25.

[Complete, word-for-word text of the Approvals & Gates section as the DMA Minute-1 module produced
it — every fact, clause, and table row, exactly as written. No summarizing, no compression.]
```

### `diligence` — current-record entry (superseding on update)

Log one of these per section actually affected by new information (`SKILL.md` U.4) — this becomes
the new "CURRENT" entry a reader treats as authoritative for that section.

```
[2026-08-14] — CURRENT — Antitrust Minute-1, Section E (Regulatory architecture, pathway & timeline),
updated 2026-08-14 — supersedes entry 7
Source: hour-1-v6, run 2026-08-14 14:20 ET, reconciling FTC Second Request (8-K filed 2026-08-14).
Differential: clock reset to Second Request compliance; expected-close read pushed from Q4 2026 to
Q1 2027; certification risk flagged as the new gating item.

[Complete, word-for-word current text of Section E as it now stands — the full rewritten section,
not the old text plus a note. Every fact, clause, and table row, exactly as it currently reads.]
```

### `diligence` — current-record entry (S-4/Proxy Review module, seeded into an existing doc)

Log one of these per section (Deal Snapshot, Key Findings, Sections 1–6) whenever the S-4/Proxy
Review module's output turns up in the chat — whether that's at initial seeding or, more commonly,
an Update Mode run well after the doc already exists (`SKILL.md` U.2b). What's New is not logged this
way — its substance goes into the accompanying `filing` entry instead.

```
[2026-09-30] — CURRENT — S-4/Proxy Review, Section 1 (Background of the Merger), seeded 2026-09-30
Source: merger-arb-s4-proxy-v4, run 2026-09-30, reviewing the DEFM14A filed 2026-09-28.

[Complete, word-for-word text of Section 1 as the S-4/Proxy Review module produced it — including the
full Interested-Party Characteristics Table, every row, exactly as written. No summarizing.]
```

### `filing`

```
[2026-07-22] — Merger agreement filed (8-K Ex-2.1, 7/22)
Source: 8-K filed 2026-07-22, Ex-2.1 (accession ...)
Current-record entries affected: DMA Approvals & Gates (entry 12), DMA Regulatory & Deal-Protection
Architecture (entry 13) — termination fees, efforts covenant, and outside date replaced with the
filed agreement's terms (previously PR-only).
Opens OQ-4 (divestiture schedule contents are confidential — remedy cap unknown).
```

### `milestone` (logged via `misc`, prefixed `[milestone]`)

```
[2026-09-02] — FTC issues Second Request
Source: [acquirer] 8-K filed 2026-09-02 / [outlet], 2026-09-02
Current-record entries affected: Antitrust Section A (entry 18), Section E (entry 19) — clock effect
and revised expected-close read incorporated.
Resolves OQ-2 (will the deal clear in the initial waiting period — no).
```

### `research` (logged via `misc`, prefixed `[research]`)

```
[2026-08-14] — Street sweep: 3 new notes (per hour-1-v6 run, 8/14) — Street map updated
- Jefferies — [analyst], 8/14: expects second request; close mid-2027; cites [precedent]. MOVE from
  clean-Phase-1 (7/23 note).
- Evercore — [analyst], 8/12: clean Phase 1, Q4 close; remedy thesis: none needed.
- ArbJournal — [report title], [date]: [view / risk category] (cited from hit metadata).
- Chain Bridge Research — [analysts], [report title], [date]: [view] (cited from hit metadata).
Street map effect: consensus now 4-of-7 clean (was 5-of-7); Jefferies move flagged.
```

### `tape` (logged via `misc`, prefixed `[tape]`)

```
[2026-08-14 15:45 ET] — Spread mark
Target [px] / acquirer [px] (get-price, 15:45 ET); consideration value [x] ([mechanics]); gross
spread $[x] ([x]%).
Annualized at [scenario dates]: ...
Context: [what moved it, if known — else "no attributed driver"].
```

### `view` (logged via `misc`, prefixed `[view]`)

```
[2026-08-15] — Desk view: [holder] on the second request
Walter, 8/15: "[the view, as close to verbatim as practical]"
Basis: [what it rests on]
Executive Summary effect: [what changed and where, if any]
```

### `consolidation` (logged via `misc`, prefixed `[consolidation]`)

```
[2026-08-14] — hour-1-v6 run folded into the doc (run 8/14, 14:20 ET)
Reused / freshly triggered: [which, and why]
Executive Summary: [refreshed / unchanged]
Current-record entries superseded: [section] → entry [N], [section] → entry [N] …
Street map effect: [as above, if applicable]
Supplemental filing sweep: [nothing new / what was found]
```

### `correction`

```
[2026-08-20] — Correction to entry 14 (research, 8/14) and Street map
Wrong: Evercore 8/12 note attributed the remedy thesis to [X].
Right: the note's remedy thesis is [Y] (Evercore, 8/12, p. 4).
Top-layer sections affected: Street map — consensus row corrected. (No current-record entry
affected — this correction doesn't touch report-section text.)
```

Note: the `antitrust-minute-1-v5` and `hour-1-v6` version strings above are illustrative only — they
show the *shape* a real entry takes (name the exact version that ran), not a version this skill
should assume is current. Always substitute whatever version actually produced the content.
````

### `references/sellside-priority.md`

````markdown
# Sell-Side Source Priority (Street Map Ordering)

This tier list sets the firm order for the **Street map — consensus / off-consensus** sections of the merger-arb memory summary (see `references/summary-template.md`), and for any firm-by-firm listing inside `research`-tagged entries. It is the same fixed institutional priority ranking used by the `deal-risk-assessment` skill's Table 9 — not a data-quality judgment; it reflects which desks/analysts the reader wants surfaced first, so order by it every time rather than by date, channel, or alphabetically.

Sort every attributed row into one of the three tiers below, then within a tier, preserve the exact firm order listed (the position number is the sort key). A firm listed with a named analyst matches primarily on the firm; if a surviving note from that firm is attributed to a different analyst than the one named here, it still sorts at that firm's tier position — the named analyst identifies the desk's usual contact, it isn't a filter that excludes other analysts at the same firm.

## High Weighting (sorts first)

1. United First Partners (UFP) — Anna Pavlik
2. FBN — Brian Lombardi
3. UBS — Evren Ergin
4. Market Securities — Jennifer Donaker
5. Cantor — David Connor
6. Raymond James — Paul Shea

## Medium Weighting (sorts after High)

7. Guggenheim — Aaron Glick
8. Elevation Securities
9. Churchill
10. Jones — Cabot Henderson
11. Roth — Mike Lesser
12. Baird — Brian Furbush

## Low Weighting (sorts after Medium)

13. BTIG
14. JP Morgan
15. Goldman Sachs
16. Clear Street

## ArbJournal, Chain Bridge Research, and other non-broker vector-database sources (sorts after Low)

ArbJournal deal files, Chain Bridge Research merger reports, and other non-broker items surfaced by the Vector Database are not broker notes and do not compete for tier positions. Give them their own clearly-labeled block, placed after the Low Weighting rows and before the unranked-firm block, sorted by date (most recent first), attributed from hit metadata ("ArbJournal — [report title], [date]"; "Chain Bridge Research — [analysts], [report title], [date]").

## Unranked firms (sorts last)

Any firm gathered that isn't on this list is unranked — place its rows after the ArbJournal / non-broker block, sorted by date (most recent first). Unranked is a position, not a demotion in substance: keep the underlying research, attribute it fully, and never drop a note just because its firm isn't on this list.

## Multiple notes from the same firm

If more than one attributed note from the same firm survives the enrichment/de-dup pass (e.g., two analysts at UBS, or the same analyst on two dates), keep each as its own row, grouped at that firm's tier position, sorted by date (most recent first) within the group.
````