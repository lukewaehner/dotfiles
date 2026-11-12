---
name: "update-merger-arb-memory-doc-v3-10202026"
description: "Standing day-2+ updater for a merger-arb deal's memory doc. v3 (10/20/2026) researches every open question on every run (not only when no analyst input exists), gives each a second pass, and leaves open only questions waiting on a dated event or not public; rebuilds the register as two tables (waiting on a dated event / answered); and fills Position from the tear sheet, the desk-call transcript and the EMSX blotter, with return on cost and buy-write returns. Also handles ad hoc new info (filing, broker note, IB chat, price move, email), runs a per-ticker email sweep, verifies claims against primary sources, shows a digest and Change Note before writing, then supersedes entries and rebuilds the top layer. Trigger: update-merger-arb-memory-doc-v3-10202026, update the memory doc, what changed since last update, change note, resolve the open questions, log this to the deal doc. Requires an existing doc; not for seeding."
---

# Update Merger-Arb Memory Doc — Standing Day-2+ Updater (Phase 4/5 and beyond)

**What v3 changes from v2 (10/20/2026; desk-approved after the BRZE / CRM call; nothing else removed).** See
`references/v3-changes.md`. In short:
1. **Research every open question on every run.** The v2 "fallback gated on absence" is removed: every open OQ gets a
   research attempt each run (`references/answer-or-escalate.md`). Analyst-supplied research is still verified first and
   not duplicated; the run adds the cheapest primary-source check and researches whatever the analyst did not cover. New
   questions get a second pass in the same run. After a v3 run an OQ stays open only as **Waiting on a dated event** (event
   and date named) or **Not public** (document named). This overrides Core Principle 3 and Phase A step 5 below wherever
   they say the self-directed pass does not run.
2. **The register is two tables** in the doc summary: "Waiting on a dated event" and "Answered" (with type: Answered /
   Judgment / Immaterial). Numbers are never reused or renumbered.
3. **Position comes from the desk's records**: tear sheet, desk-call transcript or notes, and the EMSX blotter; with
   return on cost and, when the desk sells calls, buy-write returns (`scripts/buy_write.py`). Never "no position on file"
   without checking all three.
4. **On the Horizon's "next update should cover" items are attempted**, not just carried.
5. **Precedent tables** reproduced in entries follow `references/precedent-table-format.md`.

**v2's only substantive change from v1: Core Principle 5 (verify before accepting) now has two
additional claim-type checks, drawn directly from a sell-side desk note (FBN, Brian Lombardi, on
PSNL/TEM) that did this skill's own verification job better than this skill did.** The note (1)
checked whether a counterparty who would be obligated to disclose a claimed change to a material
relationship had actually filed that disclosure, and treated the absence as evidence against the
claim rather than a shrug; and (2) read a company's own informal statement (a press quote, an IR
email) closely enough to notice what it didn't say, not just what it did. Both are general-purpose
verification techniques, not deal-specific — see the two new bullets under Core Principle 5 below.
Everything else — Core Principles 1–12, and the "When NOT to use"/sibling-skill sections — carries
forward from v1 unchanged. The phases carry forward too, with one scoping fix rather than any new
machinery: **the Executive Summary is refreshed on any run whose verified findings materially change
the deal's read, not only on a verdict move** (Phase B step 7, Phase C, Phase D step 6). Its
structure and wording are otherwise preserved exactly — only the affected bullets move, and a run
with nothing material leaves the summary untouched.

**v2.1 change (on top of v2): every run now ends with a Change Note delivered in chat** — a short, plain-language
account of everything that changed since the last run of this skill (or since `merger-arb-memory-doc-v1`
seeded the doc, if this is the first update), listed by source, where each source is *analyzed* rather than
merely listed, followed by a thesis scoreboard saying which parts of our view moved. It comes from the
desk's own use of this skill: the doc is the permanent record, but the person running the desk needs a
fast answer to "did our thesis move, and which source moved it?" without reading the entry log. See Core
Principle 14, Phase C and `references/change-note-format.md`. Nothing else in v2 changes.

The desk's ongoing ritual for a live merger-arb deal, from day 2 through close or termination: once
`merger-arb-memory-doc-v1` has seeded the doc off the T+0 pipeline, this skill is what keeps it
current for the rest of the deal's life. It runs in one of two modes, both landing in the same doc
via the same mechanics:

- **Open-Questions deep dive (Phase 4/5)** — the doc's Open Questions get handed to AlphaSense,
  Perplexity, and this chat's own research capability; this skill synthesizes what comes back,
  verifies it, and resolves what can be resolved.
- **Ad hoc new information (any day after day 2, on an ongoing basis)** — the analyst drops in
  whatever's landed since the last update — a filing, a broker note, an IB chat message, a price
  move, something heard on a call — whether or not it answers a standing Open Question. This is not
  a special case or an edge case of the OQ loop; it is the more common way this skill actually gets
  invoked once a deal is a few days old, since new information rarely arrives pre-sorted against the
  OQ register.
- **Self-directed research fallback** — if the analyst calls this skill and neither AlphaSense nor
  Perplexity deep-dive output (nor any other OQ-directed research) has been pasted into the chat
  since the doc's last update, this skill does not sit idle waiting for that input. It runs the
  research itself, against the doc's own open questions, using whatever tools this session has
  (EDGAR, web search, the ArbJournal/Chain Bridge vector databases, live pulls) and answers each open
  question to the best of its ability from what it can independently find and verify. **This mode is
  gated strictly on absence of input**: the moment this run's gather step (Phase A) finds any
  OQ-directed research already sitting in the chat, this fallback does not run — the analyst's own
  research input always takes priority, and this skill synthesizes and verifies that input rather
  than duplicating or second-guessing it with its own parallel research pass. The two are mutually
  exclusive within a single OQ: never both for the same question in the same run.

This skill owns that whole ongoing loop. It does not seed a new doc (that's
`merger-arb-memory-doc-v1`'s Seed Mode) and it does not re-run the T+0 pipeline (antitrust-minute-1 /
dma-minute-1 / hour-1) — it consumes whatever the doc already holds and folds in whatever's new,
whenever it arrives, for as long as the deal stays open.

**This skill is a sibling of `merger-arb-memory-doc-v1`, not a replacement.** It reuses that skill's
doc shape (Open Questions → Executive Summary → Street map → Position → On the Horizon, no Body
section), its current-record-entry design (Core Principle 10 — exactly one live `diligence` entry
per section, headed CURRENT, always superseded, never duplicated), and its tag vocabulary. Read
`merger-arb-memory-doc-v1`'s `SKILL.md` and its three reference files
(`references/summary-template.md`, `references/entry-formats.md`, `references/sellside-priority.md`; all three are embedded in the Appendix of `merger-arb-memory-doc-v1`'s SKILL.md)
before the first write of any run — this skill's instructions below assume that vocabulary and do not
repeat it in full. `sellside-priority.md` is the same fixed tier list `hour-1-v4` uses (see that
skill's "How this applies inside Hour-1 specifically" section for the same mechanic in a live
consolidation) — this skill uses it not just for Street map ordering but as a conflict-resolution
rule among secondary sources (Core Principle 6 below).

**The one behavior this skill adds on top of that shared design: don't trust a research pass just
because it came back confident.** AlphaSense and Perplexity outputs are secondary syntheses — they
can fabricate citations, misattribute a note to the wrong analyst, or state a "consensus" that
doesn't hold up. Every claim that resolves an Open Question gets checked against whichever source is
actually authoritative for that kind of claim (the filing itself for anything about deal terms or
disclosure language, a live price pull for anything about the tape, the vector databases' own hit
metadata for anything attributed to ArbJournal/Chain Bridge) before it's accepted into the doc.
Where no primary-source check is possible, the answer is still recorded — but the confidence label
says so plainly, and the doc's own hedging conventions (Core Principle 12) are preserved.

---

## Core Principles

1. **Read the doc's Open Questions register before reading anything else.** `read-memory-doc(name,
   entries_limit=-1)` first, always, on every invocation regardless of which mode this run turns out
   to be. Note each open OQ's number, opened date, and source, and the standing desk views (Core
   Principle 9 of the sibling skill) so they survive the refresh. This read also tells you the doc's
   last-updated timestamp — the baseline for "what's new since."

2. **Gather everything that's landed since that timestamp, not just what the user explicitly hands
   you.** This includes both input shapes described above, and a single run often mixes both:
   - Open-Questions-directed research: AlphaSense deep-dive output, Perplexity deep-dive output, or
     this chat's own research run against specific OQs (distinct from the Phase-1 AlphaSense pull the
     T+0 pipeline already folded in).
   - Anything else new: a filing mentioned or attached, a new broker/sell-side note, a Bloomberg IB
     chat message, a price move worth marking, a rumor, a desk view, or anything else the analyst
     pastes in or describes — with no requirement that it maps to an existing OQ. New information is
     new information; this skill does not wait for it to be phrased as an answer to a numbered
     question before treating it as worth logging.
   - If the chat only contains one of AlphaSense/Perplexity for the OQ-directed path, proceed with
     what's there — do not block waiting for the other, but say so plainly in the digest and the chat
     receipt (a synthesis built from one secondary source instead of two carries a lower ceiling on
     confidence for any claim that source alone supports).

3. **(v3: superseded — see the v3 block at the top. Every open OQ is researched every run; the split below now only decides whether a question gets a full self-directed pass or a verify-plus-cheapest-check pass.)** **The self-directed research fallback is gated strictly on absence, checked per OQ, not per run.**
   After the gather step, sort the doc's open OQs into two groups: those with any OQ-directed research
   pasted into the chat since the last update (even partial, even just one source) go through the
   ordinary verify-a-secondary-claim path (Core Principle 5 below); those with *no* research pasted
   for them at all are candidates for self-directed research. Do not run self-directed research on an
   OQ the analyst already fed research for, even thin research — verify what's there first, and only
   treat it as unanswered if the analyst's own input turns out not to actually address the question.
   If every open OQ has some research already pasted, this run has nothing for the fallback to do and
   it does not activate. Say plainly in the digest which OQs (if any) were answered via self-directed
   research versus analyst-supplied research, so the distinction is never silently blurred.

4. **Self-directed research uses the same tools this skill already has, run directly against the
   open question rather than against someone else's claim about it.** EDGAR (`edgar-filings`,
   `edgar-filing-index`, `edgar-filing-text`, `edgar-ownership-search`) for anything a filing would
   settle; web search for news, precedent, and anything not in a filing; the ArbJournal/Chain Bridge
   vector databases for deal-specific research coverage; live price pulls for anything about the
   tape. Work each open OQ the way an analyst doing the research themselves would — read the actual
   filing section, don't stop at the first search result, and follow an entity or precedent back to
   its own primary documentation before citing it. This is the same rigor Core Principle 5 (below)
   applies to checking a secondary source's claim, just applied from the start instead of as a check
   on someone else's work. Resolve to the same four-way scale (Resolved / Partially resolved /
   Directionally resolved / Still open per Phase B) — self-directed research closes plenty of
   questions only partially or directionally, and the confidence label says so exactly like it would
   for analyst-supplied research. Do not manufacture false precision because no secondary source's
   claim is present to hedge against — an unanswerable question stays Still open.

5. **Verify before accepting — the whole point of this skill, for analyst-supplied research.** For
   each OQ an analyst-supplied research pass claims to resolve, ask: what would actually settle this,
   and can I check it directly?
   - A claim about a filing's exact language (a rep, a carve-out, a defined term, a section's scope)
     → pull the filing text directly (`edgar-filing-text` / `edgar-filing-index`) and quote the
     controlling language yourself. Do not accept a secondary source's paraphrase or quote without
     checking it against the primary text when the filing is available.
   - A claim about a named entity, deal, or precedent ("X is the same X as in deal Y") → verify the
     identity independently (EDGAR full-text search, the entity's own filings) rather than accepting
     an unlinked assertion.
   - A claim sourced to "ArbJournal" or "Chain Bridge Research" specifically → the vector database's
     own hit metadata is the primary source here; re-pull it rather than trusting a secondary source's
     paraphrase of what those databases supposedly say.
   - A claim about current pricing, spread, or a specific dated fact only a live pull can settle →
     pull it fresh, don't reuse a number a research pass quoted from earlier in the day.
   - A claim with no available primary-source check (a forward-looking industry view, an unconfirmed
     trade rumor, a note the desk doesn't have access to) → record it as unverified, exactly as
     unverified, and say what would close the gap (a specific filing, note, or search) rather than
     silently treating repetition across two secondary sources as verification. Two AI research
     tools agreeing is corroboration, not confirmation — say which one it is.
   - **A company's informal statement (a press quote, an IR reply, a call remark) implies a change
     to a previously-disclosed material relationship or arrangement** (e.g., a role, a partnership,
     a contractual position the company or a counterparty had earlier disclosed) → check whether the
     party who would be obligated to disclose that change formally (an 8-K, a proxy amendment, a
     material-contract filing) has actually filed it. Don't stop at "no filing found, so this is
     unverified" — a disclosure that should exist by now and doesn't is itself evidence against the
     claim, and the digest should say so plainly rather than filing it as a neutral non-finding.
     Distinguish this from a claim that's merely too new to have a filing yet (state the normal lag
     for that filing type) versus one where the expected window has already passed.
   - **A claim's only source is an informal or verbal company statement** (a press quote, an IR
     email, a conference remark — as opposed to a filing, a transcript excerpt with full context, or
     a definitive announcement) → read its literal wording for what it does not say, not only for
     what it does. Note the statement's exact phrasing, where it sits in its source (a headline
     defense vs. a buried aside, and what claim it's positioned next to), and whether that precise
     wording actually supports the inference being drawn from it or only sounds like it does on a
     quick read. Quote the operative phrase itself in the verification note rather than paraphrasing
     it — a paraphrase is exactly where this kind of overreading creeps in.
   - **Optional, more judgment-laden — not a required step every run:** a company's or a named
     principal's own documented disclosure history (prior restatements, quiet-period violations,
     late or corrected filings) can inform how much credence an otherwise-unconfirmed company claim
     deserves. Use it only when it's clearly on point to the claim at hand; this is a softer,
     more subjective factor than the checks above, so don't treat it as a mandatory box to check
     or let it substitute for an available primary-source check.
   - When AlphaSense and Perplexity (or either of them and this chat's own check) disagree, say so
     explicitly rather than picking one silently — the disagreement itself is often the more
     important finding.

6. **Sell-side priority (`references/sellside-priority.md`) breaks conflicts among secondary
   sources — it never overrides a verified primary source.** When two claims bearing on the same Open
   Question disagree and at least one is attributed to a firm/analyst on the priority list, resolve as
   follows, and only in this order:
   - **A primary-source check settles it first, whenever one is available and actually performed.**
     If Core Principle 5's verify-before-accept step pulled the filing text, the live price, or the
     vector-DB hit metadata and it contradicts a priority-list firm's note, the primary-source finding
     controls — full stop. Sell-side priority is not a substitute for verification and does not get
     invoked to override a claim this skill can check directly itself. Note the sellside-priority.md
     reference file says this explicitly: it is "not a data-quality judgment," and tier "decides ORDER
     and WEIGHT, never inclusion" — this skill extends it one step further, to conflict resolution
     among secondary sources specifically, but does not stretch it into a substitute for primary-source
     verification.
   - **Priority-list source vs. non-priority secondary source, with no primary-source check available
     or applicable** (a house view, a forward-looking read, a claim only a broker would have) → the
     priority-list source's information is the desk's working answer for that OQ. State the resolution
     plainly as coming from sell-side priority, not from independent verification — see the Phase C
     Source column.
   - **Two priority-list sources conflicting with each other** → the higher tier position (lower
     number on the list) wins — e.g., UFP (#1) over Guggenheim (#7), Guggenheim (#7) over BTIG (#13).
     Still log both sides by name; a priority-resolved conflict is auditable, not a silent pick.
   - **Two non-priority (unranked) sources conflicting, or a priority-list source conflicting with an
     unattributed AlphaSense/Perplexity synthesis that carries no firm name** → sell-side priority has
     nothing to say here; fall back to the ordinary Core Principle 5 disagreement handling (state both
     sides, don't pick one silently).
   - This applies to Open-Questions resolution (Phase B/C) and to any current-record supersession this
     run's synthesis drives — not to the Street map's firm ordering, which already uses this same list
     per the sibling skill and is unaffected by this principle.

7. **A multi-pass or multi-model synthesis some research tool reports (a "council," a panel of
   models, an aggregated verdict) is itself a claim, not a verified fact.** Check its citations the
   same way as any other claim before it can move a house verdict. A fabricated or unverifiable
   citation inside an otherwise-useful synthesis does not disqualify the synthesis's other, checkable
   claims — but it does mean the citation-dependent claim gets flagged, not quietly waved through.

8. **Verdict revisions are rare and consequential — apply them everywhere at once, not
   incrementally.** If the research (analyst-supplied or self-directed) changes the house call on
   completion risk (a antitrust-minute-1 risk-tier verdict, a DMA closing-risk read, or the doc's own
   Executive Summary conclusion), that revision must land consistently in the same run: the affected
   current-record entry (per the sibling skill's Core Principle 10 supersession), the Executive Summary, and the Street
   map/Position framing wherever it references the old verdict. State the reasoning plainly — what
   independent reads support the new call and what the old call rested on — so the revision is
   auditable, not just asserted.

9. **A correction to this doc's own prior work is logged as a correction, not silently folded into
   new research.** If verification surfaces that an earlier entry in this doc (or an earlier
   antitrust-minute-1/dma-minute-1/hour-1 run it captured) got something wrong — misattributed a
   note, missed a carve-out, mis-transcribed a quote — say so explicitly: what was wrong, what's
   right now, and which entry it corrects, per the sibling skill's `correction` tag. This is
   different from an OQ resolving because new information arrived; don't blur the two.

10. **Always show the digest before writing anything.** Every run ends its research phase with the
   digest described in Phase C presented in chat, and an explicit question: write it to the doc now,
   or hold here first? Do not call any memory-doc write tool until the user confirms — unless the
   user's own trigger for this run already said to run completely / write it / update the doc (in
   which case treat that as the confirmation and proceed, but still show the digest as part of the
   same turn so the write is auditable against it).

11. **New Open Questions surface during verification — capture them, don't let them fall out.** A
    deep-dive (analyst-supplied or self-directed) answering OQ-3 may turn up a genuinely new gap (a
    claim that needs a dedicated follow-up, a document nobody's pulled yet). These get logged as new
    OQs in the same run, not left as a loose thread in the chat transcript.

12. **Run a supplemental email sweep every invocation — a direct, lightweight, single-ticker safety
    net, not a vague "check the inbox" instruction.** An earlier version of this principle said only
    to check Outlook/Bloomberg IB sources for anything landed since the doc's last update; that's too
    loose to reliably catch a same-day note, and a same-day note slipping past exactly that kind of
    loose check was an observed failure, not a hypothetical one — a combined multi-term search (deal
    name plus both tickers) under-ranked a genuinely new same-day mention that a plain single-ticker
    search then surfaced immediately. Run the sweep properly, every time, per the discipline below —
    this happens on every invocation regardless of which mode the run turns out to be (OQ deep-dive,
    ad hoc update, or self-directed research), and it does not depend on `merger-arb-memory-doc-v1`'s
    Hour-1 dependency or anything else this skill doesn't itself control:
    - **Search per ticker, separately** — `list-emails(search="<TICKER1>")`, and, if the acquirer is
      public, `list-emails(search="<TICKER2>")` as a second call. **Never combine tickers or the deal
      name into one multi-term query** (never `search="<TICKER1> <TICKER2> <Deal Name>"`). A
      single-ticker query is deliberately broader and noisier than a combined one — that's the point;
      the skim step below is what keeps the noise from becoming wasted read effort.
    - **Scope to since the doc's last-updated timestamp** (from Phase A step 1) — the same window
      this skill already uses for gathering everything else.
    - **Do not rely on the mailbox's read/unread flags** to decide what's already covered — a note
      can be marked read by anyone with mailbox access without ever having been logged to the doc,
      and an unread flag proves nothing about relevance on its own.
    - **Skim subject lines and senders first, read selectively.** A single-ticker search surfaces
      calendar mentions, unrelated coverage that happens to share a string, and genuine substance side
      by side. Spend a full `read-email` only on what looks like actual deal-specific content — a note
      that only places the ticker in an active-names or calendar list, with no deal-specific
      substance, doesn't need a full read or a log entry.
    - **Route anything found into the ordinary Phase A step 3 bucket sort**, the same as any other
      gathered item: answers an open OQ, is new information with no OQ attached, or raises a question
      the doc doesn't have yet. It then goes through the same Phase B verification and Phase D
      logging as everything else — captured with firm/analyst attribution for the Street map per
      `references/sellside-priority.md` — never a separate ad hoc logging path of its own.
    - **If nothing new turns up, say so in the chat receipt** (Phase D step 7) rather than leaving the
      check unmentioned — a silent clean check and a skipped check should never look the same to a
      reader.

13. **The Estimated close (Best / Base / Worst) line is refreshed every run it needs to be, independent
    of the Executive Summary materiality test.** `merger-arb-memory-doc-v1`'s template appends one line
    to the Executive Summary — three dates only, nothing else — sourced from the deal's current-record
    Entry Price to Target IRR scenarios: earliest/most-optimistic date is Best, central/primary
    scenario is Base, latest/most-conservative date is Worst (restated here so this check is
    self-contained; see that skill's `references/summary-template.md` for the exact line format, the
    date-string convention, and what to do when more than one current-record IRR block exists). Phase B
    step 7's materiality bar ("would a reader be misled") governs the other eight bullets; it was never
    meant to govern this one, because it isn't a judgment call — the line either matches what the
    current-record entry now says or it doesn't. Whenever this run produces a fresh Entry Price to
    Target IRR pull (true on essentially any run that touches pricing, since that block requires a
    fresh price every time) or any other finding that moves the deal's estimated-close timeline — a
    precedent-timeline pull, a regulatory delay or acceleration, a new vote date or filing deadline, a
    deal amendment — compare the three dates the current-record entry now carries against what the
    top-layer line currently shows. **"Moved" means any of the three dates differs at all, by even a
    day — there is no minimum-delta threshold.** This is deliberate, not an oversight: unlike Phase B
    step 7's judgment call on materiality, this line is a pure presentation of the current-record data,
    so it either matches that data or it's stale, with nothing in between to exercise judgment about.
    If they've moved, refresh the line via `patch-memory-summary` in the same Phase D write, even on a
    run where nothing else in the Executive Summary rises to Phase B step 7's bar. Skipping this because
    "nothing material happened" conflates two different checks: the eight bullets ask whether a reader
    would be misled, this line only asks whether it still matches the source of truth.

14. **Every run delivers a Change Note in chat — everything that changed since the last run, listed by
    source, with each source analyzed.** The window runs from the doc's last-updated timestamp (the last
    write by `merger-arb-memory-doc-v1` or by an earlier run of this skill) to now. The digest in Phase C
    exists so the user can approve a write; the Change Note exists so the user can see, at speed, whether
    the thesis moved and which source moved it. Read `references/change-note-format.md` before composing
    it. The rules:
    - **Cover every source type that landed in the window:** Bloomberg IB chat messages and anything the
      analyst typed in; pasted or emailed broker/sell-side notes (name the firm, the analyst, the time,
      and the tier from `merger-arb-memory-doc-v1`'s `references/sellside-priority.md`); every item the
      email sweep found (Core Principle 12), including mailbox items that turned out to have nothing new
      (named together in one "checked, nothing new" line, so a clean check never looks like a skipped
      one); filings (form, date, accession number); ArbJournal and Chain Bridge hits; AlphaSense and
      Perplexity output; price marks; desk views; **and this run's own analysis.** Own work counts as
      sources too: each calculation, primary-source verification pull, precedent comparison, document
      read, or self-directed research item gets its own row that names the method and what it was run
      against. The desk wants to see what Claude did, not only what other people said.
    - **Analyze every source; do not just list it.** Each source row has four parts: (1) *What it said*
      (attributed, one sentence; quote the operative phrase when the wording matters); (2) *Our analysis*
      (what we checked it against, what it adds beyond what the doc already held, what it conflicts with,
      and how far to trust it: primary-verified, secondary, or unverified); (3) *Effect on thesis*, using
      exactly one of Confirms / Adds / Modifies / Negates / Immaterial; (4) *Logged as* (the entry type,
      or "not logged" with the reason). A row that only restates the source has failed this rule.
    - **A verified primary source outranks tier.** When the filing contradicts a priority-list firm, or
      confirms a low-tier one, say so in the analysis cell (Core Principle 6). Tier orders the rows and
      breaks ties between secondary sources; it never replaces the check.
    - **Then the thesis scoreboard.** The thesis means the Executive Summary's bullets (above all the
      antitrust / gating-regulator conclusion and the timing), the Estimated close line, the Street map
      consensus and where we sit against it, and any standing desk view. One line per element: *Before →
      After* or *Unchanged*, with the source(s) that drove it. Elements the run left alone are still
      listed, so the reader can see they were tested.
    - **Close with a net line of one to three sentences:** what is material, what is not, and, when the
      thesis is unchanged, what would have changed it. Do not invent materiality to make a run look busy.
    - **Write it the way the desk reads: plain, short, self-explanatory.** Spell out a term or acronym the
      first time it appears (for example, EBITA means earnings before interest, taxes and amortization;
      a "match right" means the buyer gets a set number of hours to raise its bid before the target can
      switch deals). Keep each table cell to one or two sentences. Fold minor items into the one "checked,
      nothing new" line. Numbers come only from a tool or a cited source; never estimate one.
    - **Show it once.** It replaces the "New information" table in Phase C (it contains that table's
      content and more), and the Phase D receipt then points to it instead of repeating it.

15. **The desk's closing date, and "our view" on closing, is the date on the deal's tear sheet.**
    Read the tear sheet on every run, because it can change between runs. Wherever the doc, the
    digest or the Change Note says "desk view," "our view," "house view" or "our estimate" about when
    the deal closes (the thesis scoreboard's timing row, the Street map's "where we differ" line,
    a broker's date measured against ours), use the **Est Deal Close Date** on the deal's tear sheet,
    not a date this skill or a minute-1 module worked out on its own. The tear sheet is a spreadsheet
    in the Interns shared drive, usually named `<TICKER> Tearsheet.xlsx` or `<TICKER> Merger Arb Tear
    Sheet.xlsx`; find it with `lookup-drive-file` and read it with the Google Drive connector's
    `read_file_content` (`download-drive-file` cannot read .xlsx files). Two exceptions, and only
    these: the user gives a different date for this run, or the tear sheet is missing, unreadable or
    has no close date. In those cases use the module-derived date and say plainly in the digest and
    the doc which one was used and why. When a tear-sheet date exists it takes priority: it is the
    analyst's date after deep research, so show only the tear-sheet date as the desk's view and do
    not show a module-derived date beside it as a competing view. If the doc's Estimated close line
    no longer agrees with the tear sheet, tell the user in chat. This principle only decides which
    date is called the desk's; it does not change how the Estimated close (Best / Base / Worst) line
    is built.

---

## Phase A — Read and gather

1. Resolve the doc name and confirm it exists: `list-memory-docs`, then `read-memory-doc(name,
   entries_limit=-1)`. If no doc exists for this deal, stop and say so — direct the user to
   `merger-arb-memory-doc-v1`'s Seed Mode first. This skill only ever runs in Update Mode.
2. From the read, build the working agenda: every open OQ (number, question, opened date/source),
   the current-record entry currently CURRENT for each section, the standing desk views, and the
   doc's last-updated timestamp.
   Write down the window start (that timestamp) now; the Change Note (Core Principle 14) reports against
   it. As each source is read in the steps below, keep a running source list (firm/analyst/time, or
   filing/accession, or own-analysis method) so the note is built as the run goes, not reconstructed at
   the end.
3. Gather everything in this chat since that timestamp per Core Principle 2 above — both
   OQ-directed research and any other new item. Sort each gathered item into one of three buckets;
   an item can land in more than one if it both answers an OQ and carries other new content:
   - **Answers or partially answers an existing OQ** — map it to the OQ(s) it speaks to yourself,
     don't require the user to have pre-sorted it.
   - **New information with no existing OQ to attach to** — a filing, note, price mark, or desk view
     that updates the doc's record of the deal without closing a numbered question. Still goes
     through Phase B's verification discipline; it just doesn't produce an OQ resolution row.
   - **Raises a question the doc doesn't have yet** — goes straight to "new OQ" handling (Core
     Principle 11) rather than being forced into an artificial resolution.
4. **Supplemental email sweep per Core Principle 12** — run it now, per ticker, scoped to the
   timestamp from step 2, regardless of what step 3 already found in the chat itself (the two are
   independent sources: chat content vs. mailbox content). Sort anything found into the same
   three-bucket split as step 3 rather than treating it as a separate pass, and note in the digest
   whether the sweep found anything or came up clean.
5. **(v3) Read the desk's own records** — tear sheet, desk-call transcript or notes since the last update, and the EMSX
   blotter (`emsx-blotter`) — for the Position section (`references/v3-changes.md` §3).
6. **(v3) Research every open OQ** per `references/answer-or-escalate.md`: full pass where no analyst research exists,
   verify-plus-cheapest-check where it does; second pass on new questions. The split below still labels which path each
   OQ took.
7. **Determine the self-directed research fallback set (Core Principles 3–4).** Cross the doc's open
   OQs against what steps 3–4 actually found: any open OQ with zero analyst-supplied research
   addressing it anywhere in the chat or the email sweep since the last update goes onto the
   self-directed research list for Phase B. Any open OQ with even partial analyst-supplied research
   addressing it does not — it's worked through the ordinary verify-a-secondary-claim path instead.
   State this split plainly at the start of Phase B's output (even if the self-directed list is
   empty, or if it's every open OQ) so it's never ambiguous which path produced which answer.

## Phase B — Verify and synthesize

For every item on the agenda, regardless of which bucket it landed in:

1. Pull together what every gathered source says about it.
2. For analyst-supplied items, run the verification check appropriate to the claim type (Core
   Principle 5). For self-directed items (Core Principle 4), the research itself IS the primary-source
   pull — there's no separate claim to check, since this skill went straight to the source. Either
   way, do the primary-source work yourself — don't ask the user to do it, and don't skip it because a
   secondary source (or the analyst's own paraphrase of something they read or heard) sounded
   confident.
3. For items answering an OQ, resolve to one of: **Resolved** (verified directly, or resolved beyond
   reasonable doubt by convergent, checkable sources), **Partially resolved** (part of the question is
   settled, part isn't — say exactly which part), **Directionally resolved** (the weight of evidence
   points one way but no source closes it definitively), or **Still open** (nothing new that actually
   settles it, even if research was attempted). Never mark an OQ Resolved on the strength of an
   unverified secondary-source claim alone — a sell-side priority tie-break (Core Principle 6) is an
   exception only when the disagreement it resolves is itself among secondary sources; label that
   resolution "Resolved via sell-side priority," never plain "Resolved," so a later reader can tell it
   apart from a primary-source verification.
4. For new information with no OQ attached, characterize what it changes: which current-record
   section it updates, whether it's simply additive (a new data point, logged without disturbing
   existing conclusions) or actually changes a prior read.
5. Note whether this item touches a verdict (Core Principle 8) or corrects prior doc content (Core
   Principle 9).
6. Note any new OQ this item surfaces (Core Principle 11).

Then, once every item has been worked:

7. **Test the Executive Summary for materiality.** Re-read the summary as it currently stands in the
   doc, bullet by bullet, against everything this run verified — taken together, since two
   individually-additive findings can jointly make a bullet wrong. For each bullet ask: *would a
   reader who read only this summary now be misled, or be missing a fact that drives the deal call?*
   A yes means that bullet is rewritten this run rather than left for a later one — the summary is
   the part of the doc anyone re-reads at speed, so a stale summary sitting on top of a current entry
   stack is the failure worth guarding against. Materiality is about the deal call, not novelty: a
   verdict move, a changed or corrected headline term, a regulatory or vote event, a spread or
   close-date move that breaks the summary's framing, an OQ the summary itself flags as unresolved
   getting resolved, or a correction to something the summary asserts. A note that agrees with the
   existing read, or a price mark inside the range already described, is additive — log the entry and
   leave the summary alone. Only verified findings move a bullet; an unverified claim stays in its
   entry until something confirms it. Most runs will not move the summary, and that is the correct
   outcome, not a skipped step.

8. **Draft the Change Note rows** (Core Principle 14) from the work above: one row per source with the
   four parts, own-analysis rows included, then the thesis scoreboard and the net line. Decide each
   "Effect on thesis" label against the Executive Summary as it stands in the doc, not against memory of
   the chat.

## Phase C — Present the digest (always, before any write)

Present in chat, not yet written to the doc. Use both parts that apply — a run built entirely from
ad hoc new information with no OQ-directed research in it still gets a digest, just without an OQ
table:

**Open-Questions answer key**, when this run addressed any — always include the Source column so
analyst-supplied and self-directed answers are never blurred together:

```
| # | Question | Answer | Confidence | Source |
|---|---|---|---|---|
| OQ-N | [question as it reads in the doc] | [resolution, stated plainly, with what was checked and how] | [High — verified directly at the source / Confirmed gap remains — no source closes it / Directionally resolved, not fully closed / Unresolved] | [Analyst-supplied (AlphaSense/Perplexity/etc., verified) / Self-directed (this skill's own research, no analyst input present) / Sell-side priority (firm, tier N — no primary-source check available or applicable)] |
```

**The Change Note** (Core Principle 14; format and a worked example in `references/change-note-format.md`).
This replaces the old "New information" table. Always present it, including on a run that has no OQ-directed
research, and including when the user chose to hold the write. Shape:

```
**Change note — [DOC NAME], [window start] to [now] (since [last v1 seed / last v2 run])**

| Source (tier) | What it said | Our analysis | Effect | Logged as |
|---|---|---|---|---|
| [firm, analyst, time / filing, accession / own analysis: method] | [one sentence] | [checked against what; what it adds; what it conflicts with; trust level] | [Confirms / Adds / Modifies / Negates / Immaterial] | [entry type or "not logged: reason"] |

Checked, nothing new: [named list of mailbox items, notes or filings read with nothing to add]

**Thesis scoreboard**
| Thesis element | Before | After | Driven by |
|---|---|---|---|
| [gating-regulator conclusion / timing and base close / remedy and fee protections / financing / Street consensus / standing desk view / Estimated close] | [as the doc stands] | [new, or "Unchanged"] | [source(s)] |

**Net:** [one to three sentences: what is material, what is not, what would have changed it]
```

Follow the Change Note with:
- **The Executive Summary result, every run** (Phase B step 7) — either the bullets this run changes,
  shown as current text → proposed text with the finding that drove each, so the exact wording is
  approved before it's written; or one line saying the summary is unchanged and why. A summary left
  alone because nothing was material and one left alone because the check never ran should not look
  the same to a later reader.
- **The Estimated close (Best / Base / Worst) line, every run** (Core Principle 13) — old dates → new
  dates if this run's Entry Price to Target IRR pull or any other timeline-relevant finding moved
  them, or one line saying the line is unchanged because the current-record dates didn't move. This
  check is independent of the Executive Summary result above — the eight bullets can be unchanged
  while the close-date line still moves (a fresh price pull alone can shift the IRR scenario dates
  without touching the deal-terms bullets), and vice versa.

And, as applicable:
- Any verdict revision this run implies, stated plainly with the reasoning (Core Principle 8).
- Any correction to the doc's own prior content (Core Principle 9), stated plainly.
- New Open Questions surfaced, not yet in the doc.
- Which sources disagreed, if any, and how the disagreement was resolved or left open — including any
  case where the resolution came from sell-side priority (Core Principle 6) rather than a
  primary-source check: name both sides, name the priority tier that decided it, and say so plainly
  rather than presenting it as an independently verified answer.

Close with: **"Want me to write this into the memory doc now, or hold it here in chat first?"** — or,
if the user's trigger already authorized the write, proceed straight to Phase D in the same turn.

## Phase D — Write (only after confirmation)

Apply `merger-arb-memory-doc-v1` Update Mode mechanics exactly, using this run's synthesis as the
delta source in place of (or alongside) a Hour-1 module run:

1. **Supersede affected current-record entries.** For every section a verified finding actually
   changes (a corrected quote, a resolved carve-out question, a corrected attribution), read the
   currently-CURRENT entry, write a new `diligence` entry with the complete, current, word-for-word
   text of the section as it now stands, headed `CURRENT — [section], updated [date] — supersedes
   entry [N]`, per the sibling skill's Core Principle 10 and `references/entry-formats.md`.
2. **Log the synthesis itself as one or more entries** — a `close-question`-tagged entry (or entries)
   covering the OQs resolved this run, with the verification basis for each (what was checked, at
   what source); a `correction`-tagged entry for anything fixing this doc's own prior error; a
   `misc [research]` entry for the raw AlphaSense/Perplexity content (or supplemental-email-sweep
   find) folded in, if it carries standalone value beyond what the resolution entries already
   capture. Don't let a differential entry drift into reproducing section text that belongs in a
   current-record entry instead (per `entry-formats.md`'s universal rules) — and don't let a
   fabricated or unverifiable citation from a research pass get carried into the doc as if it were
   confirmed; log it as a flagged, unverified item instead, explicitly named as such, so a later
   reader knows not to build on it. For an OQ resolved via sell-side priority (Core Principle 6), the
   `close-question` entry's verification basis names the mechanism explicitly — "Resolved via
   sell-side priority: [firm], tier [N], over [other source/firm] — no primary-source check
   available/applicable" — so a later reader (or a later run of this skill, or of `hour-1-v4`) can
   see it was a priority tie-break, not an independent verification, and can supersede it if a
   primary-source check later becomes possible.
3. **Log ad hoc new information that doesn't resolve an OQ using the ordinary tag mapping** in
   `merger-arb-memory-doc-v1`'s `references/entry-formats.md` — a new filing as `filing`, a
   regulatory/process event as `misc [milestone]`, a broker/sell-side note or ArbJournal/Chain Bridge
   item (including anything the supplemental email sweep turned up) as `misc [research]`, a price
   mark as `misc [tape]`, a desk view as `misc [view]`. This is the same tag vocabulary the sibling
   skill uses for its own Update Mode differentials — this skill doesn't invent a separate logging
   path for information that happens to arrive outside the OQ-deep-dive loop, or through the email
   sweep rather than the chat. If the item is purely additive (updates the record, doesn't change a
   conclusion), the differential entry alone is enough; if it changes a section's current read, still
   write the current-record supersession per step 1 above.
4. **Open Questions register (v3: written as the two tables in `references/v3-changes.md` §2 — Waiting on a dated event, then Answered).** Move each resolved/partially-resolved/directionally-resolved OQ per
   Phase B's classification to the Resolved list with date, one-line resolution, confidence, and
   entry reference — genuinely unresolved OQs stay open, unchanged. Add new OQs surfaced this run
   with the next sequential number, opened date, and source. Never renumber, never delete.
5. **Verdict revision, if any.** Apply it to the current-record entry it originates in (step 1), the
   Executive Summary, and the Street map/Position framing in the same pass — per Core Principle 8,
   do this consistently rather than in one place and not another.
6. **Rebuild the top layer** via `patch-memory-summary` (preferred, targeted edits) or
   `update-memory-summary` (only for a wholesale restructure, e.g. a verdict revision that touches
   most of the summary at once). Touch each part on its own gate, not as one bundled edit:
   - **Open Questions** — per step 4 above.
   - **Executive Summary** — write exactly the bullets Phase B step 7 found material and Phase C
     showed, and nothing else; every other bullet, and the summary's existing structure and wording,
     stay exactly as they stand (this skill still does not re-run Hour-1 or re-derive its bullets from
     scratch); a run with nothing material leaves the summary untouched.
   - **Estimated close (Best / Base / Worst) line** — its own gate, per Core Principle 13: refresh it
     whenever the underlying current-record dates moved, regardless of whether the eight bullets above
     did. A run can (and often will) touch this line while leaving the Executive Summary bullets
     untouched, or vice versa — write each independently rather than treating one as triggering the
     other.
   - **Street map** — firm moves, new consensus count if it changed.
   - **Position / On the Horizon** — (v3) Position rebuilt from the tear sheet, desk-call notes and EMSX blotter every run; On the Horizon's "next update should cover" list trimmed to items still needing an event or input.
7. **Chat receipt.** What was resolved (OQ numbers, confidence, and whether analyst-supplied or
   self-directed), what new information was logged and how, what was corrected, whether a verdict
   moved and why, new OQs opened, which current-record entries were superseded (old entry number →
   new), which sources were used this run (name them — "AlphaSense deep-dive pasted [time]",
   "Perplexity deep-dive pasted [time]", "direct EDGAR verification this run", "broker note pasted
   [time]", "self-directed research — no analyst input present for OQ-N/OQ-M"), whether the
   supplemental email sweep (Core Principle 12) found anything or came up clean, and whether the
   Executive Summary moved — which bullets and on what finding, or "unchanged: [one-line reason]".
   Keep it short — the doc is the deliverable, same as the sibling skill's own convention. **Do not
   repeat the Change Note here**: point to it, and add only what the note could not know before the write
   (the final entry numbers and the top-layer lines patched). If the user held the write, say that the
   note stands as presented and nothing was written.

---

## When NOT to use this skill

- **No existing doc for the deal** → `merger-arb-memory-doc-v1` Seed Mode first.
- **Consolidating same-day T+0 pipeline output (antitrust/DMA/hour-1) into the doc for the first
  time** → that's `merger-arb-memory-doc-v1` Seed Mode, not this skill.
- **A live intraday Hour-1-style consolidation is what's actually needed** — the analyst wants a
  full reconciled chat deliverable right now, with a fresh Attributed Views table and Consistency
  Check across everything pasted today, the way the T+0 pipeline produces one — run the
  currently-installed Hour-1 module directly first, then this skill (or `merger-arb-memory-doc-v1`
  Update Mode) to capture it. This skill does not reproduce the Hour-1 module's own gather/reconcile
  machinery. That said, this is a narrow exception, not the general rule: **routine new information
  arriving on any day after day 2 — a note, a filing, a price mark, something the analyst heard —
  goes straight through this skill.** It is the standing updater for the doc's remaining life, not
  limited to Open-Questions-directed research.

## Relationship to sibling skills

- **`merger-arb-memory-doc-v1`** — owns doc creation (Seed Mode) and the doc's shape, tag vocabulary,
  and current-record-entry mechanics that this skill reuses in full. This skill is effectively its
  standing Update-Mode successor from day 2 onward — covering both Open-Question resolution and
  ordinary ad hoc new information — rather than a narrow OQ-only specialization; read its `SKILL.md`
  and all three reference files before the first write of any run.
- **The Hour-1 module (`hour-1-v4`)** — the T+0-day intraday consolidation path; this skill does not
  trigger it and does not duplicate its full gather/reconcile machinery. If a run turns up that a
  live, fully reconciled Hour-1-style deliverable is actually what's needed right now, say so and hand
  off rather than improvising a substitute reconciliation here — but this is the exception; ordinary
  new information on any later day runs through this skill directly. The two skills also share
  `references/sellside-priority.md` as the same fixed tier list: `hour-1-v4` uses it to order the
  Attributed Views table and to pick which side of a conflict a same-day consolidation leads with;
  this skill uses the same list the same way for the doc's Street map ordering (via the sibling
  skill), and additionally as the Core Principle 6 conflict-resolution rule for Open Questions —
  matching how `hour-1-v4`'s own "How this applies inside Hour-1 specifically" section already treats
  tier as deciding which side of a conflict gets the house default read, not as license to omit the
  losing side. This skill's own supplemental email sweep (Core Principle 12) is independent of the
  Hour-1 module entirely — it runs every invocation regardless of whether Hour-1 has run recently, is
  reused, or isn't in the picture at all this far into a deal's life.
- **The Antitrust Minute-1 / DMA Minute-1 modules** — this skill never re-runs their analysis; a
  verified finding that changes their conclusions is folded in as a current-record supersession
  (Phase D step 1), the same mechanism the sibling skill uses.

## Reference files (v3)

- `references/v3-changes.md` — **(v3, 10/20/2026)** research on every open question every run, the two-table register,
  Position from the tear sheet, desk-call notes and EMSX blotter, and the BRZE worked example. Read in full at Phase A.
- `references/answer-or-escalate.md` — **(v3, shared with Antitrust Minute-1 v18, DMA Minute-1 v11, Hour-1 v14)** the four
  end states and the research ladder.
- `references/precedent-table-format.md` — **(v3, shared)** the precedent columns and order for any precedent table
  written into an entry.
- `references/change-note-format.md` — the Change Note format (v2.1), unchanged.
- `scripts/buy_write.py` and `scripts/test_buy_write.py` — buy-write returns for the Position section; expect PASS.

---

## Appendix: Bundled Files

The files this skill points to (`references/...`, `scripts/...`) are embedded below, verbatim, under their original paths. When the instructions say to read a reference file, read its section here. To run a script, write its block to a file of the same name in the working directory first (e.g. `scripts/buy_write.py`), then run it from there.

### `references/v3-changes.md`

````markdown
# Memory updater v3 changes (10/20/2026)

Source: the BRZE / CRM desk call of 10/20/2026 and the debrief the desk approved the same day. The BRZE doc
ended day one with 18 open questions; about half could have been closed with one lookup each, and the
Position section said fills were "unconfirmed" while the desk had bought ~50,000 shares on the 8:01 call.

## 1. Research every open question on every run

v2 ran its own research only on questions with no analyst input (the "fallback", gated on absence). v3 drops
the gate: **every open OQ gets a research attempt on every run**, using the tool ladder in
`answer-or-escalate.md` (filings, web, our library, expert-call transcripts, live prices, the desk's own
inputs).
- Where an analyst pasted research on an OQ, still verify it (Core Principle 5) **and** run the cheapest
  primary-source check yourself; do not repeat a full research pass the analyst already did.
- Where nothing was pasted, run the full attempt (this is what v2 called the fallback).
- Questions that surface while answering get one more pass in the same run.
- An OQ may stay in the register only as **Waiting on a dated event** (name the event and expected date) or
  **Not public** (name the confidential document). "OPEN" with no event is not allowed after a v3 run.
- Answers that rest on judgment are recorded as "Answered as judgment", with the evidence and what would
  change it, and a "re-test when" note if a later event could overturn it.

Show the research pass in the digest as a table before writing:
| OQ | Tried this run | Result | New state |
|---|---|---|---|

## 2. The register as two tables

The doc summary's Open Questions section becomes:

**Waiting on a dated event** (the only questions left open)
| # | Question | Working answer | What answers it | Expected date |
|---|---|---|---|---|

**Answered** (kept for the record; move to a `resolved` entry after 30 days)
| # | Question | Answer | Type (Answered / Judgment / Immaterial) | Source / basis |
|---|---|---|---|---|

OQ numbers are never reused or renumbered (Core Principle: never renumber, never delete). Mark questions
answered this run "🆕" only in the chat digest, not in the doc. "Known sourcing gaps" stays under the tables;
remove items closed this run and date the rest.

## 3. Position from the desk's own records

Before writing the Position section, read:
1. the tear sheet (working orders, desk close date and its basis);
2. any desk-call transcript or notes since the last update (chat or Drive);
3. the EMSX blotter (`emsx-blotter`, Meteora MCP) for fills in the target and its options.
Write: size (shares, ~% of fund if stated), average cost, target size, working orders and fills, and the
source of each. Add the return on our cost to the desk date and to our modelled date, and, when the desk is
selling calls, the current buy-write returns (`buy_write.py` from DMA Minute-1 v11, or the same math by
hand: (strike − (stock − call bid)) ÷ (stock − call bid), annualized). If the blotter and the call disagree,
show both and say which is newer. Never write "no position on file" without checking all three.

## 4. On the Horizon: the "next update should cover" list is tried, not just listed

Each item on the previous run's "next update should cover" list is attempted this run. Remove the ones
done; keep only items that need an event or input that does not exist yet, each with what it needs.

## Worked example

"Full Mock - Merger-Arb Memory Update v3 - CRM x BRZE (10.20.2026)" in the Antitrust project docs: Part 1 is
the in-chat Change Note, research-pass table and thesis scoreboard; Part 2 is the full rebuilt summary. The
🆕 / ✏️ markers there show the v3 changes; they do not appear in the doc.
````

### `references/answer-or-escalate.md`

````markdown
# Answer-or-Escalate — how every open question ends (shared by Antitrust Minute-1 v18, DMA Minute-1 v11, Merger Hour-1 v14, memory updater v3)

## Why this exists

On BRZE / CRM (10/20/2026) the desk had to ask about 20 questions live that the first pass could have
answered: when the buyer's fiscal year ends, whether there is China exposure, how big the named competitors
are, where Gartner and Forrester place them, whether there is a deal call, which options are listed. The
memory doc ended the day with 18 open questions; about half could have been closed with one lookup each.
Vik's rule: "Our skills shouldn't be leaving open questions at this point." A question the run never tried
to answer is not analysis. It is a to-do list handed back to the reader.

## The four end states

Every question a run raises, inherits or is handed ends in exactly one of these:

| State | When it is allowed | What the row must carry |
|---|---|---|
| **Answered** | A source closes it | The answer and the source (filing and date, page, URL, price pull time) |
| **Answered as judgment** | No source closes it, but the evidence supports a view | The best answer an industry practitioner would give, the word "judgment", and the evidence weighed. Say what would change it |
| **Waiting on a dated event** | The answer is not public yet and a known event will make it public (HSR expiry, proxy, Second Request 8-K, agency clearance, foreign register) | The event and its expected date, counted with the deal clock |
| **Not public** | The document that answers it is confidential by design (Disclosure Letter schedules, standstill terms, banker fee before the proxy) | The document that would answer it |

"Open", "TBD", "unclear" and "to be confirmed" are not end states. If a row would say one of those, the run
has not finished with that question.

## The loop

1. **Collect** every question: ones this run raises, ones inherited from an earlier module or the memory
   doc, and every Verdict Stress Test row (a stress test is a question; it must end in an answer, not in a
   description of what the adverse evidence would be).
2. **Try each one** with the tools the session has, cheapest first: the filings already pulled; EDGAR
   full text; the parties' websites; web search; our Drive library (ArbJournal, Chain Bridge, sell-side,
   AlphaSense / Tegus expert calls); live prices and option chains; the desk's own inputs (tear sheet,
   desk-call transcript, EMSX blotter).
3. **Second pass.** Answering a question often raises a new one. Give each new question one more pass in
   the same run (two levels deep). After that, anything still unanswered must be in the "Waiting on a dated
   event" or "Not public" state.
4. **Write the two output tables** (below). Nothing else in the report lists questions.

## The Minute-1 / Hour-1 split (speed rule)

Minute-1 skills (Antitrust Minute-1, DMA Minute-1) are meant to be fast. They answer a question on the spot
only if it takes one lookup or reuses data already pulled (a fiscal-year end, an Ex-21 country check, a date
calculation, a price pull). Anything that needs a deep dive (competitor sizing, analyst-report placements,
expert calls, website sweeps, a 12-month enforcement review, a country-by-country threshold screen) is
**handed to Hour-1** with a one-line plan of what to pull. A handed-off row is not an open question: it has an
owner and a plan.

Merger Hour-1 takes every handed-off row and runs the full loop on it. The memory updater runs the loop on
every open row of the doc's register on every run, not only when an analyst asks.

## Output tables

**Minute-1 (Antitrust, DMA):**

**Answered in this pass**
| Question | Answer | Type (Answered / Judgment) | Source / basis |
|---|---|---|---|

**Waiting on a dated event**
| Question | What answers it | Expected date |
|---|---|---|

**Handed to Hour-1 (with what to pull)**
| Question | Why it is a deep dive | What Hour-1 should pull |
|---|---|---|

**Not public** (only when a row qualifies)
| Item | Document that would answer it |
|---|---|

**Hour-1 and the memory updater:** "Closed this run" and "Waiting on a dated event" (plus "Not public" when
needed). There is no hand-off table: these modules are where questions get closed.

Target on a typical deal: the "Waiting on a dated event" table has 4 to 6 rows, all tied to filings or
agency actions with dates.

## Cross-model portability

When a question survives to "Waiting" or "Not public" and the skill's older instructions ask for a
cross-model (Perplexity / ChatGPT / Gemini) entry, keep that entry self-contained (entity, jurisdiction,
fact pattern, our working answer, why it matters). The two tables above replace the old numbered
"Open Questions" list as the visible output; the portable wording can sit in the row's first cell.
````

### `references/precedent-table-format.md`

````markdown
# Precedent table format (shared; replaces the old "Year" and "HSR-regime era" columns)

## Why it changed

Vik asked on 10/20/2026 what the "Era" column meant and whether it was the president. It was not: it meant
whether HSR **early termination** was available ("ET era" before February 2021, "ET suspended" February 2021
to February 2025, "ET reinstated" after). The label was never explained, so it read as noise. The desk also
reads precedents by administration ("Slack was a different administration"), and wants the newest deals
first.

## Required columns, in this order

| Deal | Announced | Closed / ended | Days | President during review | Early termination available? | …the skill's own columns (buyer type, overlap, agencies, why analogous, outcome, procedural friction, remedy, comparability) |
|---|---|---|---|---|---|---|

- **Announced** and **Closed / ended**: full dates (M/D/YYYY). For an abandoned or blocked deal write the end
  date and "(abandoned)" or "(blocked)".
- **Days**: announce to close or end, calendar days. If a sector or foreign clock is the point, add a
  per-approval day count in the skill's own column; do not overwrite Days.
- **President during review**: the U.S. president in office from announcement to close. If the review
  crossed an inauguration, show both in order of office: "Trump / Biden" (started under Trump),
  "Biden / Trump" (started under Biden). Inaugurations: Obama 1/20/2009 and 1/20/2013; Trump 1/20/2017;
  Biden 1/20/2021; Trump 1/20/2025. For a non-U.S.-only review, still show the U.S. president (it is a
  time stamp) and name the relevant foreign regulator in the agencies column.
- **Early termination available?**: whether the FTC/DOJ could grant early end of the 30-day HSR wait during
  the waiting period. Yes before 2/4/2021; No from 2/4/2021 (suspended) to 2/10/2025; Yes from 2/10/2025
  (reinstated with the new HSR form, but granted in only ~29% of FY2025 requests per the agencies' HSR
  annual report, so it is the exception). Whether it was actually granted goes in the procedural-friction
  column ("early termination about 8/26/2025").

## Order

**Newest first** by announcement date. The buyer's own deals are not pulled to the top; the comparability
column says which rows set the base case.

## Caption line under the table

One italic line: *"Early termination available?" = whether the agencies were granting early end of the
30-day HSR wait at the time (suspended February 2021 to February 2025).* Keep it on every table; it is the
answer to the question the desk asked.

## Worked example (BRZE / CRM, 10/20/2026)

| Deal | Announced | Closed / ended | Days | President during review | Early termination available? | Outcome | Procedural friction |
|---|---|---|---|---|---|---|---|
| Salesforce / Informatica | 5/27/2025 | 11/18/2025 | 175 | Trump | Yes | Cleared | Likely refile; early termination about 8/26/2025 |
| IBM / HashiCorp | 4/24/2024 | 2/27/2025 | 309 | Biden / Trump | No | Cleared, no conditions | Refile; Second Request 7/12/2024 |
| Cisco / Splunk | 9/21/2023 | 3/18/2024 | 179 | Biden | No | Cleared | None found |
| Adobe / Figma | 9/15/2022 | 12/18/2023 (abandoned) | 459 | Biden | No | Abandoned | DOJ Second Request; EC and CMA in-depth |
| Salesforce / Slack | 12/1/2020 | 7/21/2021 | 232 | Trump / Biden | No | Cleared, no remedy | Pull-and-refile; Second Request 2/16/2021 |
| Salesforce / Tableau | 6/10/2019 | 8/1/2019 | 52 | Trump | Yes | Cleared (CMA after close) | CMA hold-separate after closing |
| Twilio / SendGrid | 10/15/2018 | 2/1/2019 | 109 | Trump | Yes | Cleared | Early termination about 11/19/2018 |
| Adobe / Marketo | 9/20/2018 | 10/31/2018 | 41 | Trump | Yes | Cleared | Not determined |
| Salesforce / ExactTarget | 6/4/2013 | 7/12/2013 | 38 | Obama | Yes | Cleared | None found |

Slack: filed 12/14/2020 under Trump, Second Request and clearance under Biden. That is why the column shows
both.

Note on Slack's "Early termination available?": the waiting period ran into February 2021, when ET was
suspended; the column shows the state during the waiting period that mattered (No).
````

### `references/change-note-format.md`

````markdown
# Change Note — format, rules and a worked example

The Change Note is the chat deliverable every run of this skill produces (Core Principle 14). It answers
one question for the person running the desk: **"since the last update, did our thesis move, and which
source moved it?"** The memory doc stays the permanent record; the note is the fast read.

## Window

From the doc's last-updated timestamp (the last write by `merger-arb-memory-doc-v1` seed mode or by an
earlier run of this skill) to now. Name both ends in the header, and say what the baseline run was.

## What counts as a source (every one gets a row, or a place in "checked, nothing new")

| Source type | How to name it |
|---|---|
| Bloomberg IB chat / anything typed by the analyst | "IB chat, [who], [time]" |
| Broker or sell-side note, pasted or emailed | "[Firm], [analyst], [time]; tier [High/Medium/Low/unranked]" (tiers: `merger-arb-memory-doc-v1/references/sellside-priority.md`); say if it is desk commentary rather than research |
| Mailbox sweep item (Core Principle 12) | same as above; items with nothing new go in the "checked, nothing new" line, by name |
| Filing | "[Form], filed [date], accession [no.]" |
| ArbJournal / Chain Bridge | "ArbJournal, [alert time]"; metadata from the hit |
| AlphaSense / Perplexity | "[Tool], [time]"; secondary until checked |
| Price mark / tape | "[Source], [timestamp]" |
| Desk view | "[Who], [date]" |
| **This run's own analysis** | "Own analysis: [method]", e.g. "Own analysis: read agreement §5.2(e) to test the match-right claim", "Own analysis: date math on outside dates", "Own analysis: read the deal slides for overlap language", "Own analysis: self-directed research on OQ-9" |

## The four parts of a source row

1. **What it said.** Attributed, one sentence. Quote the operative phrase when the wording matters.
2. **Our analysis.** What we checked it against; what it adds that the doc did not already hold; what it
   conflicts with; how far to trust it (primary-verified, secondary, or unverified, and what would close
   the gap). This is the part that makes it analysis. A cell that only restates the source is a defect.
3. **Effect on thesis.** Exactly one of: **Confirms** (agrees with a current view), **Adds** (new fact, no
   conclusion changes), **Modifies** (changes a number, date, or the strength of a view), **Negates**
   (contradicts a current view), **Immaterial** (nothing for the deal call).
4. **Logged as.** The entry type (`misc [research]`, `filing`, `correction`, `open-question`, a CURRENT
   `diligence` supersession) or "not logged: [reason]".

Order rows: primary sources and own analysis that verify claims first, then notes by tier (High, Medium,
Low, unranked), then non-broker sources. A verified primary source outranks tier: when a filing contradicts
a priority-list firm, or backs up a low-tier note, say so in the analysis cell.

## Thesis scoreboard

One row per element, including elements the run left alone (so the reader can see they were tested):
gating-regulator conclusion; timing and base close; remedy and fee protections; financing; spread driver
(only if the doc has a view); Street consensus and where we sit against it; any standing desk view; the
Estimated close line.

## Net line

One to three sentences: what is material, what is not; if nothing moved, what would have changed it.

## Style

Plain and short. Spell out a term the first time (EBITA, match right, FOCI, SSA). One or two sentences per
cell. Numbers only from a tool or a cited source. No bullets inside table cells.

---

## Worked example (PTC / Schneider, window 10/5/2026 4:45 PM ET to 5:30 PM ET, baseline: the merger-hour-1-v9 consolidation run)

**Change note — PTC, 10/5/2026 4:45 PM to 5:30 PM ET (since the hour-1-v9 consolidation)**

| Source (tier) | What it said | Our analysis | Effect | Logged as |
|---|---|---|---|---|
| Own analysis: read agreement §5.2(e) (match right) | n/a | Initial notice is 120 hours; any material change to a Superior Offer needs a new notice and a 72-hour period. The buyer can match again each time. Our doc said "five-day match right". | Modifies | `correction` entry |
| Own analysis: read Ex-99.1 (press release) | "21x" multiple; closing "by Q3 2027"; Schneider Q3 revenue release moved to 10/16/2026 | The 21x is EV/Adj. EBITA (enterprise value over earnings before interest, taxes and amortization, less stock pay), not EBITDA. Primary source. | Modifies | `correction`; `misc [research]` |
| Own analysis: read agreement §6, §3.7 and the equity-raise authority to test "Schneider holders may not back it" | n/a | No Schneider shareholder vote is a closing condition; financing is not a condition; the equity raise runs under existing authority. Buyer-side stock risk, not a closing risk. | Adds | `open-question` (OQ-12) |
| Own analysis: read deal slides for overlap language | n/a | Slides 4 and 15 call PTC "complementary" and name no overlap. This is the buyer's own framing, so it is advocacy, not a finding. | Adds | `open-question` status update (OQ-3) |
| JPMorgan, N. Jhamb, 4:31 PM (Low) | Upgrade to Neutral, PT $205; close "first half of 2027"; overlap "relatively limited"; Schneider holders "surprised" | H1 2027 conflicts with the filing ("by Q3 2027"), so the filing controls and we do not adopt it. The overlap view matches our competition read but is unsourced. | Negates (timing); Confirms (overlap) | `misc [research]` |
| Cantor, D. Connor, 2:35 PM (High, desk commentary) | Working close 4/1/2027 | Anchored to the first outside date and one comp, not to CFIUS review time. A placeholder, not a regulatory read. Its Altair day count (157) is 147 by date math. | Modifies | `misc [research]` |
| UBS desk, E. Ergin, 2:16 PM (High, desk commentary) | 9.7% annualized at $192.85 to 5/31/2027; "unlimited match rights" | Spread math uses the desk's price, not a live pull. The match-right claim is right in substance (see first row). | Confirms | `misc [research]` |
| ArbJournal, 11:50 AM | Call replay: Q3 2027 reiterated; sentiment "highly skeptical" | Terms agree with the filing. The skepticism is about Schneider's stock and two deals at once, which feeds OQ-12. | Adds | `misc [research]` |

Checked, nothing new: UFP daily (titles only); Oscar Gruss PDF (attachment not opened, so flagged as unread, not as clean).

**Thesis scoreboard**

| Thesis element | Before | After | Driven by |
|---|---|---|---|
| Gating regulator | CFIUS leads, SAMR is the swing | Unchanged | UBS desk, agreement read |
| Timing / base close | 6/30/2027 | Unchanged; Cantor earlier, JPM H1 2027 rejected | Ex-99.1, Cantor, JPM |
| Remedy and fee protections | As filed | Match right corrected to 120h + 72h resets | Agreement §5.2(e) |
| Street consensus | 3 of 4 dated firms, May to July 2027 | 3 of 5; Cantor earlier, Elevation later | Cantor |
| Estimated close line | May 31 / June 30 / July 30, 2027 | Unchanged | No IRR scenario date moved |

**Net:** Thesis unchanged. What is material is the correction (21x is EBITA; the match right renews) and the finding that Schneider shareholder pushback is not a closing risk. A different gating regulator or a CFIUS timeline from the proxy would have moved it.
````

### `scripts/buy_write.py`

````python
#!/usr/bin/env python3
"""Buy-write and covered-call returns for a merger-arb position (standard library only).

Shipped with dma-minute-1-v11-10202026 and merger-hour-1-v14-10202026.

A buy-write = buy the stock and sell a call against it at the same time.
  net debit          = stock price - call bid
  value at expiry    = strike when the strike is at or below today's price (stock pinned near the offer);
                       today's price when the strike is above it (no early close assumed)
  return to expiry   = (strike - net debit) / net debit
  annualized         = return * 365 / days to expiry
An outright call sale against an existing long earns the call bid only; its "return" is shown as
bid / stock price for scale.

Usage:
  python3 buy_write.py --asof 2026-10-20 --stock 45.395 --offer 47.50 \
      --leg 2026-11-20:45:0.60 --leg 2026-12-18:45:1.05 --leg 2027-01-15:45:0.80 --leg 2027-02-19:45:1.00 \
      [--target-irr 0.08]

Each --leg is EXPIRY:STRIKE:CALL_BID. Output is a markdown table plus a one-line "best leg" read.
The assumption that the stock finishes at or above the strike is stated in the output; if the
strike is above the offer price, the leg is flagged because the upside is capped by the deal.
"""
import argparse
import datetime as dt


def parse_leg(s):
    exp, strike, bid = s.split(":")
    return dt.date.fromisoformat(exp), float(strike), float(bid)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof", required=True)
    ap.add_argument("--stock", type=float, required=True)
    ap.add_argument("--offer", type=float, required=True)
    ap.add_argument("--leg", action="append", required=True)
    ap.add_argument("--target-irr", type=float, default=0.08)
    a = ap.parse_args(argv)
    asof = dt.date.fromisoformat(a.asof)
    rows = []
    for leg in a.leg:
        exp, k, bid = parse_leg(leg)
        days = (exp - asof).days
        if days <= 0:
            continue
        debit = a.stock - bid
        # Strike at or below today's price: assume called away at the strike (deal pending, stock pinned).
        # Strike above today's price: assume the stock is unchanged at expiry (no deal close before expiry assumed).
        payoff = min(k, a.offer, a.stock) if k > a.stock else k
        ret = (payoff - debit) / debit
        ann = ret * 365 / days
        flag = ""
        if k > a.offer:
            flag = "strike above offer: upside capped at offer"
        elif a.stock < k:
            flag = "strike above today's price: return assumes stock unchanged (call premium only)"
        rows.append((exp, k, bid, debit, ret, ann, days, flag))
    print(f"Buy-write returns (as of {asof}, stock ${a.stock:.3f}, offer ${a.offer:.2f}; in-the-money strikes assume the stock stays at or above the strike; out-of-the-money strikes assume the stock is unchanged)\n")
    print("| Expiry | Strike | Call bid | Net debit | Days | Return to expiry | Annualized | vs target | Note |")
    print("|---|---|---|---|---|---|---|---|---|")
    for exp, k, bid, debit, ret, ann, days, flag in rows:
        vs = "above" if ann >= a.target_irr else "below"
        print(f"| {exp:%a %m/%d/%Y} | ${k:.2f} | ${bid:.2f} | ${debit:.3f} | {days} | {ret*100:.2f}% | {ann*100:.1f}% | {vs} {a.target_irr*100:.0f}% | {flag} |")
    if rows:
        best = max(rows, key=lambda r: r[5])
        print(f"\nBest leg: {best[0]:%b %Y} ${best[1]:.2f} buy-write at {best[5]*100:.1f}% annualized "
              f"({best[4]*100:.2f}% to {best[0]:%m/%d/%Y}); it pays whenever the deal closes, as long as the stock is at or above ${best[1]:.2f} at expiry.")
    return rows


if __name__ == "__main__":
    main()
````

### `scripts/test_buy_write.py`

````python
#!/usr/bin/env python3
"""Regression test for buy_write.py on the BRZE 10/20/2026 15:47 chain. Expect PASS."""
import io, contextlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buy_write
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rows = buy_write.main(["--asof", "2026-10-20", "--stock", "45.395", "--offer", "47.50",
                           "--leg", "2026-11-20:45:0.60", "--leg", "2026-12-18:45:1.05",
                           "--leg", "2027-01-15:45:0.80", "--leg", "2027-02-19:45:1.00"])
ann = [round(r[5] * 100, 1) for r in rows]
assert ann == [5.4, 9.1, 3.8, 4.1], ann
assert "Best leg: Dec 2026 $45.00" in buf.getvalue()
print("PASS")
````