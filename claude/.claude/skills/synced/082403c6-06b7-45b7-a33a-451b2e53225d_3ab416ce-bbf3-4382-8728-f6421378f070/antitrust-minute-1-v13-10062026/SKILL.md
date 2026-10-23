---
name: "antitrust-minute-1-v13-10062026"
description: "Announcement-day (T+0) antitrust and regulatory-clearance module for a new M&A deal, and the re-read when new documents land. Produces a gate-led memo (verdict, overlap, competitive effects, regulatory timeline, precedents, Entry Price to Target IRR). v13 covers state health care approvals. The 10/6 revision adds a standing-public-record agent for what was knowable before announcement (target clearances, federal contracts, rival ownership structures, the buyer's own deal track record, pending rules), a coverage ledger, a guidance-gap test and questions for counsel. Also: spread-pressure module, deal-date calculator, CFIUS/FOCI screen with mitigation-instrument sort, delta mode, desk read. Use for antitrust risk, HSR, second request, EC/CMA/SAMR review, CFIUS, FOCI, special security agreements, regulatory timing, outside dates, why a spread is wide, state approvals, or whether analysis changed after new documents. Trigger: 'antitrust-minute-1', 'antitrust risk on [ACQ]/[TGT]', 'will this clear HSR'."
---

# Antitrust Minute-1 (v13) — announcement-day merger-clearance module

Produce a focused clearance read on a deal announced in the last few business days: does this
combination have a competition problem, how big, what would fix it, **and — with equal weight — which
regulator actually determines the closing date, and what does that regulator's process take.**
Seven sections, chat-native, sourced to primary documents — six analytical sections plus a required
Section G pricing block (see "Entry Price to Target IRR" below).

**What v13 changes from v12 (state health care approvals; nothing removed).** On a multi-state health care
target the closing date is usually set by state regulators, and v12 had no entry for them: its clocks covered
insurance, FINRA/RIA and a few federal stubs, and its named-state rule fired only for licensing regimes. v13 adds
(1) a state health care entry in `references/regulatory-clocks.md` and a full reference,
`references/state-healthcare-regimes.md`, with the three layers (transaction-notice laws, licensure and change of
ownership, federal program and accreditation), the perimeter test and the output template; (2) state health
regimes on the "commonly gate" list and two new tells; (3) a threshold-triggered perimeter step in Agent E
(`references/gather-prompts.md`, Step 1b); (4) Section E.2a and E.2b, a named-state build and earliest-close
floors and tails, counted from the filing date; (5) a regime-era tag on state precedents; (6) a rule that "list
unfiled" can never close the question; and (7) a `deal_clock.py adddays` command for the floor and tail arithmetic.
Reason: on OPCH / CD&R-McKesson the state list sat in a confidential Disclosure Letter, the first review stopped
there, and broker notes that tested state statutes against the target's revenue and footprint found what it had
missed (a possible Maine prior-approval review, Oregon and Massachusetts reviews, a California 90-day notice).

**10/6/2026 revision of v13 (the standing public record; nothing removed).** On PTC / Schneider Electric a
broker note the morning after announcement carried five facts our memo lacked, and all five were public before
the deal: the target's Defense Department cloud authorization, the buyer's earlier deals and their timelines, the
buyer's cleared U.S. subsidiary, a pending guideline change at a reviewing agency, and a rival already selling the
same product to the government under a foreign-ownership arrangement. The five gather agents read the agreement and
SEC filings; none was assigned to the rest of the public record. This revision adds (1) a sixth agent, Agent F,
and its reference `references/standing-public-record.md`: our own library first, sector trigger packs, a rival
mirror, an acquirer profile, regulator state and prior strategic interest; (2) a **coverage ledger** in Section F,
so a skipped check never looks like a clean one; (3) the buyer's own track record as the first timeline anchor
(E.0) and a guidance-gap test (E.0a); (4) a target sensitivity profile and a mitigation-instrument sort in the
national-security screen, and a rule that the screen re-runs when the agreement is filed; (5) access to rivals'
confidential information as a standing theory of harm; and (6) questions for counsel. See rules 29 to 33.

**The module's name says antitrust; its job is clearance.** On a large fraction of deals the
competition analysis is correct, complete, and worth two paragraphs, while the thing that decides
whether the deal closes in 150 days or 350 is a sector regulator's change-of-control process that a
generalist read reduces to a table row. A memo that spends its length on theories of harm and its
brevity on the approval build has allocated exactly backwards. The **regulatory intensity
classification** below is what prevents that, and it is resolved before any other analysis.

The judgment inside the six analytical sections is benchmarked against how a genuinely sharp same-day broker
note actually reasons, not just what a checklist would produce mechanically: it walks overlap segment
by segment in prose instead of stopping at a table; it runs an explicit narrow-vs-broad
market-definition comparison rather than landing on one definition silently; it checks whether the
parties have actually behaved as partners (a merged liquidity pool, a joint venture, a licensing deal)
before concluding from a competitor-naming check alone; it reads every cited precedent for procedural
friction, not just its headline outcome date; it treats the acquirer's own earnings-call commentary as
a first-class source, since management often says more on a same-day call than either party's press
release; and where a market-quantification gap shows up, it runs one more targeted search for the
closest analogous prior transaction rather than simply recording the gap. None of that requires a new
section. It requires more from Section C, plus disciplined sourcing habits threaded through Sections A,
D, and F:

1. **Section C carries an overlap narrative** — one prose paragraph, written directly off the Overlap
   Screen table, walking each overlapping (and adjacent) product line in turn and stating plainly
   whether it's genuine head-to-head competition or complementary positioning — before the
   market-definition-and-concentration subsection, not folded into it.
2. **Section C's market-definition subsection carries an explicit narrow-vs-broad sensitivity call**
   for any line with apparent overlap: state both the narrowly-drawn definition and the more
   broadly-drawn one, which one the analyst believes is correct, and why — not just the
   hypothetical-monopolist-test conclusion on its own.
3. **Section C's verbatim-competitor-disclosure and mutual-listing check is corroborated by a
   structured vector-DB pull (P3)** — sellside/IOC coverage naming competitors by product line, which
   is often more specific than a 10-K's Competition section and is frequently the only source
   available at all for a private target or PE portfolio company. See `references/vector-db-
   retrieval.md`.
4. **Section C carries a Prior Cooperation / Complementary-Relationship check** — a short paragraph or
   table alongside that check, surfacing any known joint venture, liquidity-pool merger,
   index-licensing, or distribution agreement between the parties that predates the deal. This is a
   different question than "do they name each other as competitors" — it's "have they actually
   behaved as partners" — and it is frequently the single strongest piece of overlap-mitigating
   evidence available on day one.
5. **Section A's risk matrix carries a current-enforcement-posture row**: antitrust enforcement posture
   / political climate in the gating jurisdiction, sourced and dated like every other row —
   administrations and agency leadership change the real-world odds of a challenge independent of the
   underlying overlap facts, and a T+0 memo that never says so is missing a live input the market is
   already pricing.
6. **Every precedent cited in Section F is read for procedural friction, not just its outcome date.**
   "Cleared without a second request" and "cleared after a pull-and-refile" are both technically
   "no formal second request," but they describe materially different regulatory experiences, and a
   precedent read that only checks the binary outcome misses exactly the texture a sharp reader wants.
   See "Precedents" below.
7. **Agent D's gather brief includes a same-day sweep of the acquirer's own earnings or investor call**,
   not just the merger press release and deck. The single highest-value fact on a live deal — whether
   management has directly addressed a known antitrust or conduct-investigation overhang, priced it into
   the offer, or described the overlap in their own words — routinely surfaces on a same-day call and
   nowhere else. See "What exists on day one" and the Tools section below.
8. **When Section C cannot source market-share or HHI data for the actual overlap line, the vector-
   database and web searches retarget to the acquirer's or target's closest analogous prior transaction**
   before the gap is recorded as final. A professional analyst's market-share table from that
   acquirer's most recent comparable deal is often the best available proxy for a line that has no
   deal-specific data of its own — cited explicitly as a proxy from a different transaction, never
   presented as if it were this deal's own number. See "Precedents" below.
9. **Section G is a required Entry Price to Target IRR pricing block** — a fresh live-price
   pull every run (never reused from earlier in the conversation), three close-date scenarios (this
   memo's own clearance-handicap working close date, and that date ±30 days — never a fixed generic
   day-count set), an 8%-default parameterized target IRR, and a required four-part Read. This is the
   one section in this module where live pricing and a directional pricing view belong. Where a
   ticking fee exists, the block additionally carries a fee-adjusted consideration table. See
   `references/entry-price-target-irr.md`, read in full during the gather window alongside the other
   reference files.
10. **Every deal is classified antitrust-gated / sector-gated / dual-gated in Section A** (where the sector regulator's perimeter cannot be verified at T+0, classify as *conditionally* sector- or dual-gated, say which fact decides it, and run the Approval Clock Build in both cases), and the
    classification routes the rest of the memo — see "Regulatory intensity" below. This is the single
    highest-leverage judgment in the module, because it decides where the memo's length goes. The
    classification itself is internal — Section A states its practical consequence (which regulator
    sets the date, and why) in plain language, never the label. See the labelling rule under "The
    rules that make the output usable" above.
11. **Section E's timeline is a bottom-up build, not a precedent average.** On any sector-gated or
    dual-gated deal, Section E carries an **Approval Clock Build** table — one row per approval body,
    separating the statutory clock from what starts it from what precedents show it actually takes —
    and the base-case close date is derived from the longest chain plus a closing tail. Precedent
    averages become a sanity check on that construction, never a substitute for it. See "Timing is a
    build, not an average" below and `references/regulatory-clocks.md`.
12. **Acquirer archetype is a timing input, and stated guidance and ticking fees are timing
    evidence.** A generalist sponsor making its first acquisition of a licensed entity faces a
    materially different sector review than an incumbent strategic, independent of any overlap; and
    the parties' own close guidance and any ticking-fee trigger date are the most informative timing
    disclosures available on day one. Both are read, not merely reported. See "Acquirer archetype as a
    timing input" and "Timing signals" below.
13. **Any litigation cited as market-definition or overlap evidence carries an affirmative
    disposition check — settled, dismissed, or still pending — never left as "no public disposition
    found" after a single search pass.** A cited case that is actually resolved, and how it resolved,
    changes what it's evidence of: a settlement reached through a license grant or commercial
    accommodation is a data point that market power was checked by ordinary bargaining, not a live
    foreclosure threat, and reporting the case as "unresolved" when it settled understates that. See
    "Litigation cited as market-definition evidence must be status-checked" below.
14. **Section A's regulatory-perimeter check identifies whether each licensed entity is a captive (or
    similar carved-out structure) before applying the general Form A entry to it.** Captives are
    routinely exempted from a state's general Insurance Holding Company System Act by a separate
    captive-insurance chapter, and change of control for one typically runs a single discretionary
    commissioner-approval rule rather than the standard notice-and-hearing machinery — materially
    different timing and process, in either direction, from the default entry. Misapplying the general
    regime to a captive overstates a small entity's timeline; assuming the captive's lighter track
    applies to a traditional carrier understates it. See `references/regulatory-clocks.md`'s captive
    entry.
15. **The run does not end at memo delivery whenever a genuine open question would move the base-case
    date or the verdict.** See "Open questions and the autonomous deep-dive pass" below — screen for
    these before treating a run as finished, then continue straight into the deep dive and its
    cross-model-ready Open Questions block rather than waiting to be asked a second time.
16. **Agent E's perimeter enumeration is never scoped to the deal's primary sector alone.** A target's
    own 10-K "Regulation" section routinely discloses ancillary regulator relationships in the same
    paragraph or two as the primary sector language — FINRA broker-dealer membership, an SEC-registered
    investment adviser subsidiary, a named foreign operating footprint — that have nothing to do with
    the deal's headline sector story but are independently triggered by a change of control, sitting in
    a primary source that predates the deal by months. Read the section in full, not just the sentence
    that matches the assumed sector, and clock every regulator category it names on day one, before
    Section A's antitrust-gated/sector-gated/dual-gated classification is finalized — this is exactly
    the class of finding that should never need a broker note or a second read to surface. See
    `references/regulatory-clocks.md`'s "Financial-services ancillary regimes" entry.
17. **Section C's competitor check runs in both directions, and always ends in a named peer set.**
    "Who does this party name as a competitor" is only half the question, and on a party whose
    Competition section names nobody it returns nothing at all. The other half — "who names this
    party" — comes from third-party filings and is frequently *better* evidence than self-listing.
    But neither direction on its own tells the reader **who the peer set actually is**: two raw,
    unreconciled competitor lists are not a peer universe, and a memo that stops there leaves the
    reader unable to say who else trades in this market or how big any of them are. Section C
    therefore carries a required **Peer Set & Scale table** on every deal — not only where the
    outbound check came up empty. See "The competitor check runs in both directions" below.
18. **The classification doesn't just decide section depth — it decides section order, imposes a hard
    length budget on LOW-scored non-gating topics, and triggers a mandatory second research pass on
    anything MODERATE+ or still open.** Once Section A's classification is resolved, the memo's actual
    read order and space allocation lead with the gating item — on a sector-gated deal that means the
    regulatory pathway and Approval Clock Build, not the overlap screen, get the memo's weight and
    come first in emphasis even where the section lettering stays A→G for house-report continuity. A
    LOW-scored, non-gating topic is capped at roughly 15% of total memo length and does not get its own
    full table. Any item scored MODERATE or higher, or left genuinely unresolved after a first pass,
    gets a second, targeted research pass before delivery — it does not ride on a single pass the way a
    LOW item can. Where the gating item is a state-by-state licensing or change-of-control regime, it
    is named at the state level — specific states, consent type per state or cluster, a speed tier, a
    named must-have list, and whether an NMLS register lookup actually verified status — never
    compressed to an aggregate count. See `references/gate-led-structure.md`, read in full alongside
    `references/memo-template.md` during the gather window.
19. **A precedent pull that only returns closed deals is missing the most diagnostic comparables on a
    slow-moving regime.** The regime-specific ArbJournal pull required on every sector-gated or
    dual-gated deal (see `references/vector-db-retrieval.md`'s P1 rules) explicitly includes open/live
    and terminated deals alongside closed ones, labelled by status — an open deal currently stalled on
    the identical regulatory pathway is frequently more informative about real-world friction than a
    clean closed comp, and excluding it because it hasn't resolved yet is a bug, not a filter.
20. **Section G leads with one named, desk-legible price level before the formal scenario table, and
    closes with a mandatory topping-bid/appraisal-claim discussion whenever the spread doesn't clear
    the target hurdle.** The headline level is stated in the trading desk's own quick-math convention
    (raw spread = deal price/current price − 1, doubled for a rough annualized read) so a fast reader
    gets an actionable number immediately; the full three-scenario table and four-part Read still run
    in full afterward. Where that Read concludes the current spread is unattractive, the memo does not
    stop there — it states, briefly, whether a topping bid or an appraisal-rights claim could still make
    the position interesting, even where both assessments come back weak. See
    `references/entry-price-target-irr.md`.
21. **Open Questions are materiality-ranked, and an item that wouldn't move the date or the verdict is
    cut from the delivered block entirely, not demoted.** Screening for open questions (per
    `references/open-questions-deep-dive.md`) is a two-stage filter: Step 1 decides what's worth
    researching, and a stricter materiality pass afterward decides what's worth delivering — surviving
    Step 1 does not guarantee a place in the final list.
22. **Register: no section-label scaffolding, conclusions before supporting detail, and the memo states
    its own triage decision in plain language as part of the Section A verdict.** Do not narrate what a
    section is about to do ("this section will now discuss..."); every subsection leads with its
    conclusion. Section A's opening states explicitly, in one added sentence, which regime is driving
    this memo's weight and why — a reader should never have to infer the triage from section lengths
    alone. See `references/memo-template.md`'s "Register" note.

23. **The memo is readable by someone who has never worked in the target's industry.** Section B
    opens with the two companies in plain English (what each does, how it makes money, its segments,
    fixed revenue-by-segment and revenue-by-geography tables, history and past deals) and carries a
    bad-actor check on both parties; Section C opens with a five-step "antitrust in baby steps" walk
    and a jurisdiction-by-jurisdiction table covering every regime in E.1; Section D carries the full
    11-guideline HSR merger-guidelines table with a Yes/No/Maybe column. This layer sits *inside* B, C
    and D and never displaces the gating regulator's analysis. Written as a required layer because
    an analytically correct memo still fails a reader who has to assemble the business picture from
    scattered sentences. See `references/plain-language-primer.md`, read in full during the gather
    window.

24. **The verdict is calibrated in both directions, and a listed competitor is a candidate, not a
    finding.** A named rival in a 10-K does not raise the overlap rating until it passes four tests
    (management's own words on earnings calls and at conferences, substitute vs. complement, same
    customers, direction of the naming); one memorable precedent never sets the verdict by itself — the
    acquirer's full record and its outcome mix do; first-review risk, duration risk and challenge/remedy
    risk are rated as three separate reads; the draft verdict is steelmanned one level up and one level
    down before it is locked; any sell-side, desk or AlphaSense view that disagrees is tested against a
    primary source rather than merely logged; and Section A ends with an "Other views" block followed by a one-sentence verdict stress-test.
    These checks run both ways: they must raise a rating on a real overlap as readily as they lower it
    on a paper one. See `references/calibration-principles.md`, read in full during the gather window
    and again before Section A is locked.

25. **Section G carries the Spread Pressure and Supply module.** The clearance read says how risky the
    deal is; it does not say why the price sits where it does. Section G therefore checks deal size against
    liquidity, float and holders, premium and break price, upside against downside, the buyer's stock and
    financing wording, short interest, sell-side supply, the first ten days of tape and index events, then splits
    the spread into time value, technical premium and risk premium, in words only. A buyer move of more than
    about 5% triggers the buyer-side check; a large all-cash deal with a premium above about 30% triggers the
    supply check. When no live price exists, use a user-pasted price, then a desk price, and if none, a
    price-independent hurdle table with that stated in the first line. See `references/spread-pressure-supply.md`.
26. **Dates come from the calculator, not from mental arithmetic.** `scripts/deal_clock.py` counts business
    days using the agreement's own Business Day definition (read the definition and pick the calendars it
    names, for example New York and Paris), builds the outside-date ladder, compares company guidance with that
    ladder, and runs the spread, implied-entry-price, hurdle and spread-split math. Section E states the ladder
    row and says "no reverse fee" when the agreement has none.
27. **A national-security screen runs on any deal with a foreign buyer or a government-facing target.** It reads the
    government-contracts and clearance representation, the efforts clause for a line-of-business ring-fence,
    and the target's government programs and cloud authorizations. Defense revenue share that the target does not
    disclose is written "not disclosed" and never estimated. See `references/national-security-screen.md`.
28. **When new documents land on an existing memo, run delta mode.** Three separate reads (first review,
    duration, challenge or remedy), a what-changed table, a re-based approval clock, a same-deal check on every
    retrieved file, and earlier open questions marked superseded when the agreement answers them. See
    `references/delta-mode.md`.
29. **Agent F reads the public record that existed before the announcement, from a fixed checklist.** Our own
    library first, then the sector trigger packs the target's end markets select, a rival mirror, an acquirer
    profile, regulator state and prior strategic interest. It launches in the same block as Agents A to E, so it
    adds no wall-clock time. The reason is simple: most of what a sharp next-morning broker note contains was
    public the day before, and a memo that lacks it has not been beaten on insight, only on looking. See
    `references/standing-public-record.md`.
30. **Every check is reported, including the ones that found nothing.** Section F prints a coverage ledger with
    one row per check and a status of Found or Not found after search. "Not searched" may appear in an agent's
    return but not in a delivered memo: run the check, or move it to Open Questions with the reason. A screen that
    asks for something and does not require the answer to be reported will be skipped without anyone noticing.
31. **The buyer's own deals are the first timeline anchor, and long guidance gets explained.** Section E opens
    with the acquirer's track record (E.0) applied to this deal as calendar dates, then tests the gap between
    company guidance and that record (E.0a) by listing hypotheses and the evidence for each. Generic comparables
    are the cross-check, not the starting point.
32. **On a foreign buyer of a government-facing target, build the sensitivity profile and sort the instruments.**
    The national-security screen prints the target sensitivity profile, quotes both the instruments the buyer must
    accept and the remedies it may refuse, separates the separation test from the scale test, and says whether the
    scale words are defined. It is re-run in delta mode when the merger agreement is filed, because the clearance
    representation and the burdensome-condition wording are not in a press release.
33. **Access to rivals' confidential information is a standing theory, and unanswerable questions go to
    counsel.** Whenever the target hosts data for the acquirer's competitors, test the data-access theory
    alongside foreclosure (`references/strategic-buyer.md`). Whatever the public record cannot settle (an agency's
    current mood, how a clause would be read) is written as three to six questions for counsel in Section F, not
    guessed at and not dropped.

This is a **module, not a full report.** It deliberately omits financing capacity, MAC analysis,
target solvency, litigation/fraud screening, valuation and the tape — those belong to the full
deal-completion workflow. Its output is written to slot straight into Meteora's house report:

| Memo section | Drops into house report as |
|---|---|
| A. Antitrust verdict & risk matrix | The antitrust row of §1 and the regulatory row of §11 |
| B. Buyer classification & competitive footprint (incl. B.0 plain-English company profiles, B.4 bad-actor check) | §4 Portfolio Company Analysis subsection |
| C. Overlap screen, market definition & concentration (incl. C.0 baby steps, jurisdiction table) | §5 Market Definition & Concentration |
| D. Competitive effects & remedies (incl. D.0 HSR 11-guideline table) | §6 Competitive Effects Analysis |
| E. Regulatory architecture, Approval Clock Build & timeline | §7 Regulatory Pathway & Timeline |
| F. Precedents, sources & limitations | §11 precedent table + §12 sources/limitations |
| G. Entry Price to Target IRR | Tape addendum — this is the one section of this module whose content belongs there, not in §1–§12 |

Adopt the perspective of a **prospective deal risk analyst evaluating completion probability**. Do
not write strategic advice for either party, and do not discuss where the target trades relative to
consideration outside of Section G — that framing belongs to the tape addendum of the full report,
not here. Sections A through F never pull a price and stay completion-risk-only, exactly as before;
the one exception is the required Section G pricing block (see "Entry Price to Target IRR" below),
which is the only place in this module where live pricing, spread math, or an
IRR/entry-price view belongs.

**Argue to a conclusion — do not report facts and leave the reader to assemble the verdict.**
The gather agents return raw field lists on purpose ("not an essay, not a narrative" — see
`gather-prompts.md`); that discipline is for the gather step only. The compose step — turning that
field list into the memo — is a synthesis step, and its job is to do the reasoning the reader would
otherwise have to do themselves. Concretely, every material finding gets three things, not one: the
fact (sourced), the test or reason it matters, and the conclusion connecting them — in that order,
in the same paragraph or table-adjacent sentence, joined with a causal connective ("With no X and no
Y, Z is absent" / "X, therefore Y" / "because A, B does not apply"). A finding that stops at the fact
is half-written. Two contrasts, same underlying move ("no bundling concern," a real pair from this
skill's own drafting history):

- *Weak — fact only, no reasoning:* "Conglomerate / bundling — LOW — No cross-portfolio bundling
  evidence identified."
- *Strong — test stated, fact applied, conclusion drawn:* "Conglomerate concerns require the combined
  entity to leverage market power in one product to extract advantage in an adjacent one. With
  [buyer]'s portfolio entirely outside [target's industry], there is no plausible bundling or
  cross-marketing concern."

**Extend at least one finding per memo into a second-order implication.** Do not stop at "no
overlap was found" where the finding has a further consequence for completion risk, remedy cost, or
competitive-bid dynamics — draw that consequence out explicitly, labelled `Assessment:`. Example: a
buyer whose sole overlap sits in the target's smallest, already-shrinking segment isn't just "low
divestiture exposure" — it means a divestiture remedy would cost the buyer almost nothing, which
removes divestiture friction as a completion risk even in a downside review scenario. That second
sentence — the "which means" — is the part a raw fact list never produces on its own, and it is
usually the single most useful sentence in the section for a reader deciding how much to worry.

**Prefer decisive, evaluative language over procedural hedge-language, on claims that are
actually settled.** "Materially absent," "the dominant factor," "obviates the need for," "has no
foothold here" carry judgment; "stated gap," "reported-only," "could not be confirmed," "flagged as
an open item" are accurate but carry none — and if a memo runs on the second register throughout, the
few places an analyst actually has a view get lost in the noise of the places they don't. Reserve the
procedural register for claims that are genuinely unsettled (see the hedging-fidelity rule above);
use the evaluative register everywhere a sourced fact supports an actual conclusion.

## The rules that make the output usable

These are not stylistic. Each one exists because its violation produces a memo that reads confident
and is wrong in a way the reader cannot detect.

- **Never estimate, calculate or invent market shares, HHI figures, or probability percentages.**
  Quantify shares only when *both* a revenue figure and a total-market figure come from citable
  sources; compute HHI only with sufficient participant data. Where the data does not exist, write
  the limitation. A stated gap is information the reader can act on; a fabricated HHI is a landmine
  that detonates in front of a client.
- **Competitor lists and geographic revenue breakdowns come verbatim from EDGAR** — the Competition
  sections of 10-K/10-Q and the segment/geographic tables. Reproduce or quote them; never paraphrase
  a competitor list, and state explicitly when a filing names no competitors at all.
- **Cite every fact and figure to a specific source** — form type + filing date (accession where
  practical), named industry report with date, agency press release, or news outlet with date. This
  binds **tables as well as prose**: every table names its source in the caption or a per-row source
  column. A number that lives only in a table with no visible source is unauditable, and the reader
  should not have to guess whether it came from a 10-K, an analyst estimate, or thin air.
- **Preserve the epistemic status of every claim through transcription.** "Could not determine
  either way" must not become "none reported"; "not disclosed" must not become "none"; "consistent
  with X" must not become "X". This degrades silently at the moment a hedged finding is compressed
  into a table cell, because cells are short and hedges are long. A real instance: an agent reported
  *"could not find an explicit second-request disclosure either way for any of the four — flagging
  that as an inference"*, and it reached the delivered table as *"No second request reported"* —
  absence of evidence rendered as evidence of absence, in the column the reader leans on hardest.
  When a cell cannot hold the hedge, use the shorter honest form ("not determinable from public
  sources") and put the reasoning in the caption. Every subagent inherits this rule explicitly.
- **Hedge only what is actually uncertain — state settled facts flatly.** The rule above protects
  against *losing* a real hedge in compression; it is not license to hedge everything by default. If a
  fact is directly sourced and settled ("no portfolio company holds a stake in \[sector\]," per a
  reviewed, complete portfolio listing), write it as a flat declarative sentence — "AIP has no
  disclosed portfolio holdings in medical devices" — not "it appears AIP may not currently hold..." A
  memo that hedges settled facts as heavily as unsettled ones trains the reader to discount every
  hedge, including the ones that matter. Reserve qualifying language for claims that are genuinely
  incomplete, inferred, or sourced to a single low-confidence channel.
- **Findings are positive or negative, never inferred silence.** "No prior FTC/DOJ enforcement
  action identified for this sponsor after searching agency releases and trade press" is a finding.
  Saying nothing because you found nothing is not.
- **Directional assessments only, in Sections A–F** — LOW / MODERATE / HIGH with decomposed
  rationale, colour-coded RAG in the matrices (green = favourable to completion, so "LOW RISK" and
  "HIGH probability of clearance" are both **green**). No point probability percentage appears
  anywhere in Sections A–F. (This does not reach Section G's IRR%/spread% math, which is a different
  kind of number — a pricing calculation, not a fabricated clearance-probability estimate — and is
  required there by design.)
- **Separate sourced fact from analytical opinion.** Opinions are prefixed `Assessment:`.
- **Clearance handicapping is precedent-based.** Ground every characterisation in named precedent
  transactions with deal, year, outcome and a real announce→close day count. Never emit an
  intuition-derived "this clears in 90 days".
- **Precedent selection is weighted by product/market/overlap-type comparability first, buyer
  identity second.** The single strongest anchor is the acquirer's own prior deal *in the same
  product market* as the current overlap. "Same acquirer, different industry" (e.g., a fixed-income
  platform deal being handicapped against the same buyer's mortgage-technology or energy-software
  acquisition) is not a substitute for that and must not be labelled "the most probative precedent"
  — it is admissible only as a secondary, clearly-labelled signal about the acquirer's litigation
  posture, negotiating behaviour, or serial-acquisition pattern, never as a timeline or outcome
  anchor for an unrelated overlap. State explicitly, in the clearance-handicap paragraph, which
  precedents are being read for overlap-type comparability and which (if any) are being read only
  for buyer-posture, and why.
- Buyer-side footprint mappings are verified against EDGAR and issuer/sponsor disclosures; minority
  stakes are flagged explicitly, and anything sourced only to press is marked reported-only.
- **A named competitor is not the same finding as an uncooperative one.** The verbatim-competitor
  and mutual-listing check in Section C answers "do the parties describe each other as rivals on
  paper." It does not answer "have they actually behaved as partners." Both questions get answered —
  the second one explicitly, in its own short paragraph, sourced to any prior joint venture,
  liquidity/order-flow-pool merger, index-licensing, distribution, or similar arrangement between the
  parties. Behavioral cooperation evidence outweighs a naming omission and should be weighted that way
  in the Section A verdict. The same logic runs the other way for a naming: a competitor listed in one
  party's 10-K, with no matching language from that party's own management and no rival naming either
  party, is a candidate overlap to be tested, not proof of one. Management's own description of who it
  competes with on an earnings call is at least as probative as counsel-drafted 10-K language, and the
  memo must quote it (see `references/calibration-principles.md`, principle 1).
- **Enforcement posture is a sourced, dated finding like any other — never a background
  assumption.** State the current administration/agency-leadership posture on merger enforcement in
  the deal's gating jurisdiction as its own risk-matrix row, cited to a specific public statement, case
  pattern, or agency release with a date, and note explicitly that the read is time-sensitive and could
  be stale by the time the memo is reused. Do not fold this into the general clearance-handicap
  paragraph where it can't be checked or updated independently.
- **"Antitrust-gated" / "sector-gated" / "dual-gated" — and any derived phrase such as "sector-gate"
  or "the gate is wide" — are internal classification labels for routing this module's own analysis.
  They are never written into the delivered memo, in any section, header, table cell, or caption.**
  The analyst reading the finished memo has not read this skill file, and a label like "sector-gated"
  reads as unexplained internal jargon that raises more questions than it answers. Wherever this
  classification would normally be stated to the reader, say what it *means* in plain,
  self-explanatory language instead: name the actual critical-path regulator(s) or regime by name, and
  state the practical consequence for the closing date. Write "the closing date will be set by state
  insurance regulators and non-US prudential supervisors, not by U.S. antitrust review," never "this
  deal is sector-gated." Use the labels freely in your own reasoning, in the gather-agent prompts, and
  in cross-references to this skill's own sections — just strip them out of anything a reader of the
  finished memo will actually see.

## What exists on day one — and what does not

Half the wasted effort on an announcement-day antitrust read is hunting documents that cannot exist
yet. The document set is knowable in advance; treat the right-hand column as closed.

**Exists:** the merger 8-K and its exhibits (Ex-2.1 merger agreement, Ex-99.1 press release, often a
furnished investor deck under Item 7.01); the target's and acquirer's latest 10-K and 10-Q; both
parties' IR-site press release and deck; the sponsor's portfolio page; agency press releases on prior
enforcement; closed, open, and terminated precedent deals in the ArbJournal corpus (see
`references/vector-db-retrieval.md` — the precedent pull is not limited to closed deals).

**Refresh rule:** if this module is re-run after day one, or the user pastes sell-side, desk, ArbJournal
or AlphaSense commentary into the conversation, treat every view that disagrees with the draft verdict
under `references/calibration-principles.md`, principle 5, before delivering.

**Does not exist — one attempt at most, then record the absence as a limitation:** the preliminary or
definitive proxy (~30 days out), any HSR-filing 8-K or clearance notice, a second request, published
broker research on this deal, and — for most sponsor take-privates — any investor deck at all.

**Structurally impossible, do not attempt:** vector-database queries on the party names. The deal is
days old and cannot be indexed; these return ticker-string collisions that look like hits and are
not. The vector work that *does* pay is filter-first, not name-first — the P1 precedent pull (filtered
by deal shape/sector) and the P5 enforcement-posture roster (filtered by regulator) in Agent D, per
`references/vector-db-retrieval.md`.

## Tools

Load the deferred tools in **one** `ToolSearch` call before the gather block — the set is fixed:

`select:mcp__MeteoraMCP-AWS__edgar-filings,mcp__MeteoraMCP-AWS__edgar-filing-index,mcp__MeteoraMCP-AWS__edgar-filing-text,mcp__MeteoraMCP-AWS__extract-10k,mcp__MeteoraMCP-AWS__extract-8k,mcp__MeteoraMCP-AWS__semantic-search,mcp__MeteoraMCP-AWS__entity-neighbors,mcp__MeteoraMCP__get-price,WebSearch,WebFetch,TaskCreate,TaskUpdate`

Note: `mcp__MeteoraMCP__get-price` is loaded solely for the required Section G pricing
block — see "Entry Price to Target IRR" above and `references/entry-price-target-irr.md`; it has no
legitimate use in Sections A–F.

**Price fallback order (v12).** Live pricing tool first; if it is unavailable or errors, a price the user
pasted in this chat (label it user-supplied, with its time); then a price quoted in a desk or broker note in
the chat (name the note). If none exists, do not guess: build the price-independent hurdle table with
`scripts/deal_clock.py hurdle` and say in the first line of Section G that no live price was available.

**Calculator.** Use `python3 scripts/deal_clock.py --help` for the subcommands (`bdays`, `ladder`, `spread`,
`implied`, `hurdle`, `decompose`, `downside`). Run it instead of computing dates or spreads by hand, and quote
its output. Pass `--json` when you want to reuse the numbers.

- **EDGAR — AWS server first, structured extractors before full text.** `extract-10k` returns the
  Competition section and the segment/geographic tables directly, still verbatim from the filing —
  that is precisely what sections C and D need, in one call instead of paging. `extract-8k` handles
  the announcement 8-K and its press-release/deck exhibits. Reach for raw `edgar-filing-text` only
  for the merger agreement, and there jump by section-heading anchors or offsets — never linearly.
  Fall back to the non-AWS `MeteoraMCP` EDGAR twins only if the AWS server is down.
- **`entity-neighbors` — the inbound competitor leg, one call per party, every run.** It returns the
  knowledge graph's subgraph around a ticker or company name: who sits adjacent to this company across
  the indexed research corpus. This is structural adjacency, not document text, which makes it
  complementary to the P3 vector pull rather than a duplicate of it — P3 asks "what does sellside prose
  say about this product line," `entity-neighbors` asks "who is this company filed next to." It reads
  no filings and pages nothing, so it costs effectively no wall-clock time inside a gather block that is
  already running. See "The competitor check runs in both directions" below.
- **Payload discipline.** `edgar-filing-text` never runs at its 200,000-char default: call
  `summary=true` first for the TOC, then fetch ≤40,000-char windows by offset, or delegate the whole
  document to a subagent (the default for anything agreement-length). Cap `semantic-search` at
  `top_k` 5 with metadata filters.
- **Vector DB — precedents, competitive positioning, enforcement-posture rosters, and regulatory
  pathway analysis (P1/P3/P5/P6):** read `references/vector-db-retrieval.md` in full during the
  gather window, before Agents B, D and E run, and apply its filters exactly. **P6 (Chain Bridge
  Research) is the highest-value pull on a sector-gated deal** — Chain Bridge writes
  regulatory-pathway analysis (statutory clocks, threshold mechanics, approval sequencing) where
  ArbJournal writes deal files and running day counts, and the two are complementary rather than
  redundant. Run both. Also run P1's **mandatory second pass keyed to the specific regulatory regime by
  name**, not just deal shape or sector — a sector-level query is too broad to surface regime-specific
  friction. P1 (`namespace='default'`, `document_type: "Merger Arb Analysis"`, filtered by `sector` —
  never `industry`, which silently drops the current enforcement era) is a structured precedent lookup,
  not a research task: the returned `hsr_outcome` and `deal_timeline_days` fields are usually a
  complete, citable precedent by themselves, and the pull deliberately does **not** gate on
  `actual_completion_date` — open/live and terminated deals are kept and labelled by status rather than
  filtered out, since an open deal stalled on the identical regulatory pathway is often the single most
  diagnostic comparable available (see `references/vector-db-retrieval.md`). P3 (`namespace='default'`,
  `document_type` in `["Initiation of Coverage", "Sellside Note"]`, queried by named product line)
  corroborates Agent B's EDGAR competitor list and is frequently the only source at all for a private
  target or PE portfolio company. P5 (`namespace='arbjournal'`, filtered by `deal_id` to the standing
  roster for the gating agency) answers Section A's enforcement-posture row directly, dated to the
  chunk's `entry_timestamp`. All three run before, and narrow, the web search that used to carry these
  tasks alone.
- **Web search — regulatory pathway primary sources (Agent E, required on sector-gated and
  dual-gated deals).** Precedents tell you what happened; they do not tell you *why* it takes that
  long, and the "why" is what lets a memo forecast instead of extrapolate. For **each critical-path
  approval body**, search: (1) the regulator's own procedural guidance — filing instructions,
  completeness checklists, approach documents, transaction instructions; (2) **law-firm client alerts
  and white papers on review duration** for that regime, which are the only public sources that state
  practical ranges honestly because they are written for clients who need the real number; (3)
  standard-setting or supervisory work-stream materials where the acquirer's archetype triggers them;
  and (4) published hearing calendars and approval orders on the regulator's own site, which serve
  both as precedent day counts now and as the live monitorable later. Return, per body: statutory
  clock, practical range, named source with date, and **the specific factor the source identifies as
  the lengthener** — that last item is the one that makes the build predictive.
- **Web search — antitrust and buyer-side:** sponsor portfolio and PE-database coverage, FTC/DOJ/EC
  press releases and closed enforcement matters, trade press on market structure, industry
  association data — plus three Agent D legs beyond the deal press release itself: any prior joint venture / liquidity-pool /
  licensing / distribution arrangement between the parties; the gating agency's current
  enforcement-posture signal (recent public statements, speeches, or the pattern of recent
  clearances/challenges under the current leadership); and, whenever the acquirer holds a same-day or
  same-week earnings/investor call, a targeted search for sell-side notes covering that call
  specifically — search `"[Acquirer] earnings call" [target] antitrust OR synergies OR overlap` or
  equivalent phrasing. Management routinely says more on a live call than either party's press release
  states in writing — direct confirmation that a known conduct-investigation or antitrust overhang was
  priced into the offer, the actual composition of a headline synergy number (commercial vs. cost,
  and specifically whether any of it is capacity rationalisation or plant consolidation — an admission
  of horizontal proximity the press release itself may not contain), or a plain-English description of
  the overlap in the acquirer's own words. This is one additional targeted search per party, not a general
  earnings-call research expansion — run it once on the acquirer's own call, and once on the
  **target's** most recent earnings call and conference remarks for how its management names its direct
  competitors and describes the acquirer (a 10-K listing is counsel-drafted; a CEO on a call says who
  actually takes customers), and fold anything
  antitrust-relevant into the relevant section (synergy framing into Section D, overlap description
  into Section C, conduct-risk commentary into Section B or A) rather than reporting it separately.
- **No Bloomberg, no other pricing tools, for Sections A–F.** Sections A through F have no legitimate
  use for market pricing and stay completion-risk-only, exactly as before. **Section G is the one
  exception**: it uses `mcp__MeteoraMCP__get-price` (loaded by default — see Tools below) to pull a
  fresh live equity price for the target (and acquirer, if relevant to the offer math), every run.
  Never let a Section G price stand in for, or get treated as informing, the completion-risk read in
  Sections A–F.

## Execution — one gather block, then analysis

**The entire I/O budget is one tool block.** If a run feels slow, the cause is almost always that
the block was split. Reading one agent's return before the last agent is launched has already
serialised the gather and given the parallelism back.

**Pre-launch minimum — three calls in ONE batch:**

1. `edgar-filings` to locate the merger 8-K (skip when the accession is already in the user's prompt,
   as it usually is at T+0);
2. `edgar-filing-index` on that one filing to confirm Ex-2.1 and the exhibit list;
3. `edgar-filing-text(summary=true)` on Ex-2.1 — the TOC, which gives Agent A its offsets for the
   covenants and termination articles.

**Then launch all six gather agents in a single block**, using the shorthand form — each agent
reads its own section of `references/gather-prompts.md` rather than having its prompt re-emitted:

> Read `{SKILL_DIR}/references/gather-prompts.md`, section "Agent X". Execute it for {TARGET}
> ({TICKER}, CIK {CIK}), acquirer {ACQUIRER}, merger 8-K accession {ACCESSION}, announced {DATE}.
> The closing instructions in that file's header apply to your return.

The six: **(A)** merger agreement — the regulatory architecture; **(B)** target and (if strategic)
acquirer periodic filings — Competition sections and geographic/segment tables verbatim, plus the
inbound "who names this party" check; **(C)**
buyer footprint — sponsor portfolio map or acquirer segments, plus prior antitrust history;
**(D)** precedents, market structure, the parties' own deal materials, plus the prior-
cooperation check and the current-enforcement-posture read; **(E)** regulatory pathway — the
per-approval-body clock research that feeds the Approval Clock Build; **(F)** the standing public record — our own library,
sector trigger packs, rival mirror, acquirer profile, regulator state and prior strategic interest, returned
with a coverage ledger (`references/standing-public-record.md`).

**Agent F is required on every run too.** Its checklist is short on a deal with no regulated end market and
that is fine; what matters is that the ledger comes back. Where the target is government-facing or the buyer is
foreign, read `references/national-security-screen.md` while the agents run, since Agent F's defense pack feeds
its sensitivity profile.

**Agent E is required on every run**, because the classification that would tell you it is
unnecessary is itself informed by what Agent E finds. On a deal that turns out to be antitrust-gated
its return will be short and that is fine; on a sector-gated deal it is the most important brief in
the block, and launching it late costs the run its whole advantage.

**While the agents run (~3 minutes), read `references/memo-template.md`, `references/calibration-principles.md`, the buyer branch file,
`references/regulatory-clocks.md`, and — wherever either party has a non-US revenue footprint —
`references/foreign-merger-thresholds.md`.** Do not read them before launch — that is critical-path
time — and do not idle-wait.

## Buyer classification — the branch that decides everything downstream

Classify from evidence, not from press framing. Determine from the merger agreement's acquisition
vehicle, its ultimate parent, the equity commitment letters and the guarantor disclosures:

- **Financial sponsor** — the vehicle is ultimately controlled by a PE fund, family office or other
  financial buyer. The fund competes with nobody directly; the competitive entity is the *portfolio*,
  one layer down, often dozens of holdings, many private, some minority. It must be **discovered**
  before it can be screened. → read `references/pe-buyer.md`.
- **Strategic** — an operating company buying in or adjacent to its own business. The competitive
  entity is the acquirer itself and it files, so no discovery is needed; the work is a rigorous
  two-company comparison. This is often the *higher*-scrutiny case, because two named competitors
  merging is exactly what the agencies are built to catch. → read `references/strategic-buyer.md`.
- **Hybrid / consortium** — PE-backed platforms doing add-ons, sponsor + strategic co-investor
  consortia, strategics buying through financial vehicles. → read both; run both branches and
  attribute each overlap to the parent that creates it.

State the classification in section B with its entity-level evidence, cited. This is substantive
output, not routing: agencies apply different lenses to a serial sponsor roll-up and a direct
horizontal strategic merger, and the classification is the first thing a reader checks.

**The financial-sponsor invariant — this governs every section after classification, not just
Section B.** Once the buyer is classified as a financial sponsor, **the portfolio company is the
subject of every overlap, competitor, geographic, and market-definition sentence and table cell for
the rest of the memo — the fund itself almost never is.** The fund has no product, no Competition
section, no geographic revenue table, and (outside of its own regulatory/HSR-compliance history as a
filer) no antitrust-relevant footprint of its own — noting that a PE fund "doesn't disclose
competitors" or "has no revenue by geography" is not a finding, it is a category error, because a
fund was never going to have either. Concretely:
- Never write "\[SPONSOR\] has no overlap with \[TARGET\]" or "\[SPONSOR\]'s competitors are…" —
  write "no \[SPONSOR\] portfolio company was identified with overlap in \[line\]" or name the
  specific portfolio company.
- Every table in Section C that has a "buyer-side" column (Verbatim Competitor Disclosures,
  Geographic Revenue Comparison) is populated from the **overlapping portfolio company's own**
  filings, press, or foreign-registry disclosures where they exist — never left as a row about the
  sponsor entity. Before writing "no public disclosure," Agent B runs the P3 vector-DB pull
  (`references/vector-db-retrieval.md`) for the portfolio company, since sellside/IOC coverage
  frequently names competitors for firms that never filed a Competition section. If no overlapping
  portfolio company has any public disclosure to pull from **and** the P3 pull comes up empty, say
  that plainly ("\[portfolio co.\] is privately held with no public competitor or geographic
  disclosure located, and no sellside coverage identified naming its competitors") rather than
  substituting a sentence about the fund.
- The one place the sponsor entity *is* the correct subject: firm profile (AUM, fund, thesis), the
  sponsor's own prior antitrust/HSR-compliance history as a filer, and roll-up seriality (the fund is
  the actor doing the rolling up). Everywhere else, if a sentence's subject is the fund's name, stop
  and rewrite it with the portfolio company as the subject.
- **Before delivering the memo**, re-read every sentence containing the sponsor's bare name next to
  the words "overlap," "competitor," "compete," or "revenue by geography" — if the sentence is making
  a substantive claim (not just firm-profile context) rather than routing to a portfolio company, it
  is very likely wrong and needs to be rewritten around the specific holding.

## Regulatory intensity — the second branch, and it decides where the memo's length goes

Buyer type is one branch. **Regulatory intensity is a second, orthogonal one**, resolved in Section A
alongside the horizontal / vertical / market-extension framing and before any concentration
discussion.

The test is not "which approvals are required" — that is a list anyone can copy off a press release.
The test is **"which single approval, if it were the only one required, would still determine the
closing date."** Answer that first, then classify:

| Classification | Meaning | Where the memo's weight goes |
|---|---|---|
| **Antitrust-gated** | HSR / EC / CMA is the critical path; sector approvals are absent, ministerial, or notification-only | Sections C and D run in full; Section E is architecture-heavy (the merger agreement's negotiated antitrust risk allocation). The Approval Clock Build is still required but will be short. |
| **Sector-gated** | A sector regulator is the critical path and antitrust is a 30-day formality | **Sections C and D compress to the overlap gate and its evidence. Section E expands into the full Approval Clock Build. Precedent selection re-anchors on approval body rather than product market.** |
| **Dual-gated** | Both are live | Both run in full, and Section E must state explicitly whether the clocks run **concurrently** or whether the sector regulator waits on antitrust clearance before acting — sequencing is the difference between adding and maxing. |

**Three tells that a deal is sector-gated**, and they are usually visible on the announcement press
release alone:

1. **Both sides retained dedicated sector-regulatory counsel, and no antitrust specialist is named.**
   Advisor lists are the parties' own resource allocation made public. Special insurance counsel on
   both sides with no antitrust firm anywhere on the list is a stronger signal than anything either
   party says in prose.
2. **The approvals sentence names the sector regime and not the antitrust regime.** A release that
   says "required regulatory approvals" and separately names insurance regulators, while never
   mentioning HSR, is telling you which review the parties are worried about.
3. **The stated close window is materially longer than the antitrust waiting period plus proxy time
   can explain.** If HSR plus a proxy is four months and guidance is nine to eleven, something else
   is setting the date. Find it before writing anything else.

Sector regimes that commonly gate: **state insurance departments (Form A change of control)**, **state health
care transaction-notice and review laws and health care licensure (pharmacy, home infusion and home health change
of ownership, certificate of need)**, FCC,
FERC, STB, the Fed / OCC / FDIC, state public utility commissions, foreign prudential supervisors
(PRA/FCA, NBB, CBI, BaFin, OSFI and the Canadian Minister of Finance, BMA, CIMA, MAS, APRA), CFIUS
and foreign-investment screens, and gaming or communications licensing authorities.

Two more tells apply to state health care regimes, and both are visible on the announcement alone:

4. **The approvals sentence says "state regulatory approvals" or "health care regulatory approvals" and the target
   is a multi-state provider** (pharmacies, infusion or clinic sites in many states). Treat this as at least
   *conditionally dual-gated* at T+0 and run `references/state-healthcare-regimes.md`; do not wait for the
   agreement to name the states, because it will probably put them in a confidential disclosure letter.
5. **The agreement carries a filing deadline for health care filings separate from the HSR deadline, or a higher
   efforts standard for health care approvals than for antitrust** (for example "best efforts" against
   "reasonable best efforts"). The parties have told you which review they expect to be slower.

**When the classification comes back sector-gated, state the practical consequence in one line at the
top of Section A and mean it downstream — never the label itself.** Name the regulator or regime that
actually sets the closing date, in plain language a reader who has never seen this skill file can
follow on first read (e.g., "the closing date here will be set by state insurance regulators and
non-US prudential supervisors, not by U.S. antitrust review" — not "this deal is sector-gated"; see
the labelling rule under "The rules that make the output usable"). Do not then write four pages of
theories of harm on a clean overlap gate because those are the sections the module knows how to write.
Compress them honestly — "we looked and found nothing, here is the evidence" is a complete finding —
and spend the recovered length on the approval build, which is what the reader is actually trying to
price.

## Timing is a build, not an average

**The closing date is constructed from the bottom up, one approval body at a time. It is not read off
the middle of a precedent set.** A precedent average blends deals with different regulatory
perimeters, different acquirer types and different filing dates; it can produce a plausible number
while telling the reader nothing about which regulator to watch, what a slip would look like, or what
a favourable surprise would be. Those three things are the analysis. The number alone is not.

**Section E therefore carries an Approval Clock Build table** — required on sector-gated and
dual-gated deals, and still required (though short) on antitrust-gated ones:

| Approval body | Statutory clock | What starts the clock | Observed clock, ≤5yr precedents (cited) | Acquirer-specific adjustment | Filing date (est./actual) | Approval date (derived) | Critical path? |
|---|---|---|---|---|---|---|---|

Four rules make that table honest rather than decorative:

**Distinguish the statutory clock from the clock start, and the clock start from the practical
clock.** Nearly every change-of-control regime pairs a short headline period with a completeness
requirement and a deficiency or interruption mechanism — which makes *completeness*, not the statute,
the elastic variable. A sixty-day statutory Form A period is not a sixty-day review; a supervisor's
92 working days runs from acknowledgement of a complete notification, after a pre-filing engagement
period that is not clocked at all. State all three for every row: what the statute says, what the
regulator must actually receive before it starts counting, and what recent precedents show it takes
in practice. A memo that reports only the statutory number has reported the number least predictive
of the outcome.

**Derive the base case from the longest chain, not the blend.** Build each row as filing date plus
practical review period. The base-case close is the **latest single approval date plus a short
closing-mechanics tail**, not the mean of the precedent set's total deal timelines. Then use the
precedent averages as a **sanity check** — and where the constructed date and the precedent average
disagree, say so plainly, say which one you are trusting, and say why. Usually the build governs,
because the precedent set rarely matches the perimeter exactly.

**Say which approvals run concurrently and which are sequenced, and label those as assumptions.**
Parallel filings add nothing to the critical path; sequenced ones add fully. Insurance
change-of-control filings generally run in parallel across jurisdictions; a lead-state regulator may
wait to see a sister state's disposition; ministerial approvals typically follow the prudential
regulator's recommendation rather than running alongside it; some sector regulators will not act
until antitrust clearance is in hand. Sequencing assumptions are the largest single source of error
in a constructed timeline, and they must appear as stated assumptions rather than disappear into
arithmetic.

**Name the critical path explicitly, and name the second-longest chain too.** The reader's real
question is what to monitor. One flagged regulator is a monitorable; a table of eight without a flag
is homework. Where two approvals are close enough that either could bind, say that — a deal with two
competing long poles has a fatter timing distribution than one with a single clear binding
constraint, and that difference belongs in Section G's Read.

**Add two rows under the table every time an agreement exists.** (1) *Guidance against the outside-date
ladder:* run `scripts/deal_clock.py ladder --signing --announce --initial --months ... --guidance ...` and
state which extension step the company's own close guidance first fits within, in days from announcement.
A guided date that only fits inside the second extension tells the reader the parties already expect to
need an extension. (2) *Reverse fee:* state the amount, or write "no reverse fee" when the agreement has
none, because a buyer with no reverse fee bears no direct cost for walking if a required approval fails.
Count any "business day" period (for example a filing deadline) with `scripts/deal_clock.py bdays` using the
calendars the agreement's own Business Day definition names.

**When state health care regimes are on the perimeter, Section E also carries E.2a and E.2b (v13).** E.2a is the
named-state build: one row per state, ranked by regime and clock rather than by site count, with the regime,
whether it is notice-only, review or prior approval, the trigger test and the data used (a site count is a proxy
and is labelled one), the clock from a complete notice, and a status. E.2b is the earliest-close floors and tails:
for each state, filing date plus the notice lead time (the floor) and filing date plus the comprehensive-review
outer bound (the tail), computed at the agreement's latest permitted filing date and at an early date with
`scripts/deal_clock.py adddays`, each shown against the base close and the outside date, with one sentence saying
whether the tail is a timing risk or a completion risk. Four rules govern both:

1. **Derive the list; never stop at "unfiled".** If the agreement places the states in a confidential disclosure
   letter, log that as a sourcing gap and then build the perimeter from the target's footprint against each
   state's statute, the target's earlier state filings, its earlier merger proxy, and the agencies' public notice
   pages. State the closing-condition status separately from the statutory status (a statute can require a filing
   the agreement does not list).
2. **Test thresholds, not proxies.** Revenue and asset tests at the right level (target, acquirer's ultimate parent,
   sponsor or affiliates where the statute counts them) decide coverage. Location counts only label a proxy.
3. **Count from filing.** Clocks run from a complete filing, not from announcement. An agreement that allows up to
   30 business days to file adds up to six weeks that an announcement-based comparable hides.
4. **Run down conditional lead-time rules.** If a possible regime's lead time would move the earliest close past
   the base case, show the arithmetic as conditional, name the fact that decides it, and add it to the watch list.

Read `references/state-healthcare-regimes.md` for the three layers, the perimeter test, the reference table of
state laws and the worked example. Read `references/regulatory-clocks.md` during the gather window for the per-regime mechanics —
statutory period, clock-start definition, interruption mechanics, observed practical range, and the
specific acquirer attributes that lengthen each one. That file is the encoded domain knowledge that
web search will not reliably reconstruct on a T+0 clock.

## Acquirer archetype as a timing input

On an antitrust-gated deal the buyer's identity matters mainly through its portfolio. **On a
sector-gated deal the buyer's identity is itself the subject of the review** — a Form A or a
change-of-control notice asks who the ultimate controlling persons are, whether they are fit and
proper, what they intend to do with the regulated entity, and how they will capitalise it. The
portfolio is nearly irrelevant to that; the archetype is nearly everything.

| Acquirer archetype | Sector-regulator posture | Directional timing effect |
|---|---|---|
| Incumbent sector strategic, already an approved control person in the jurisdiction | Known applicant, known business model, existing relationship | Fastest |
| Alternative manager with an established regulated platform | Repeat applicant; controlling-person chain already mapped; prior commitments on file | Fast to moderate |
| Generalist private equity, first acquisition of a regulated entity of this type | Full first-time-owner review; commitments negotiated from scratch | Moderate to slow |
| **Sector-specialist investor from an adjacent-but-different sector, first regulated acquisition** | **The applicant must explain to the regulator why an investor of this kind should own this asset. The business plan and capital-maintenance questions ARE the review, not a formality** | **Slow** |
| Foreign, sovereign-linked, or opaque ownership chain | Adds investment-screening and ministerial discretion on top | Slowest |

**Continuity of approved control persons is the most underweighted timing mitigant in a sector-gated
deal.** Where an existing controlling shareholder rolls equity and remains a control person
post-close, the regulator is not approving an unfamiliar ownership chain — it is approving an
addition to one it has already vetted. Likewise, founder and management rollover answers the "who
will actually run this thing" limb of the business-plan review before it is asked. State both in
Section E as timing mitigants **tied to the specific approvals they help**, not as deal-structure
colour in Section B — and be honest that they help most in the jurisdictions where the incumbent
holder is already approved and least in those assessing the new applicant on its own.

**The acquirer's own deals come before any generic comparable.** A buyer that has taken five companies through
the same agencies in six years has shown how long it takes that buyer, with that counsel, in front of those
staff. Agent F returns the track record with day counts; apply the range to this deal as calendar dates in E.0,
then say what is different about this target (size, clearances, hosted data, a regulator the buyer has not faced).
Broker comparables and database averages are the cross-check. On PTC / Schneider the buyer's own five deals ran
119 to 224 days, which bracketed the Street's range better than the industry average did.

## Timing signals — decode them, do not restate them

Two disclosures available on announcement day carry more timing information than anything else, and
both are routinely reported as facts when they should be read as evidence.

**Stated close guidance is negotiated disclosure, not forecast.** It is set by counsel against the
slowest approval's realistic case, and companies do not guide past their own outside date. Decode it:
state the guidance window's day-count range from signing, then say where the constructed critical
path lands inside that range and why. A half-year window opened four and a half months out and
closing ten and a half months out is not guidance for its midpoint — it is the parties telling you
the slow lane is live, because otherwise they would have guided to the earlier half. Where the build
and the guidance disagree, the build governs and the memo says so explicitly.

**When guidance runs well past the buyer's own record, test why (E.0a).** Put the guidance day count beside the
buyer's range and the precedent average. If the gap is large, write the candidate explanations as hypotheses (a
security review of a cleared target, another deal by the same buyer still under review, a foreign filing with a
long pre-notification, plain conservatism), give the evidence for each, and say which is best supported. A long
window with no stated reason is the most informative thing in the press release and should not pass without one.

**A ticking fee is a compensation mechanism the target negotiated, and it reads as price protection
first and risk signal second.** Its presence means both sides concluded that timing extension was
likely enough to be worth pricing, and that the target declined to bear the time-value cost of a
regulatory queue it does not control. It is **not** primarily evidence that the deal is in danger — a
buyer who accepts an accruing purchase price rather than repricing, narrowing the perimeter or
walking is demonstrating conviction, not doubt. Say that plainly rather than reaching for a distress
read.

Three extractions are required, in descending order of value:

1. **The trigger date.** This is the parties' own revealed base case for when the named approvals
   should have landed, and it is a better anchor than any prose guidance in the press release.
   Reconcile the constructed baseline against it and explain any gap.
2. **Which approvals trigger it.** A fee triggered by specifically named sector approvals is the
   parties confirming the critical path for you — carry it straight into the Approval Clock Build's
   critical-path flag as corroboration.
3. **The accrual period's end, and any cap.** A fee that runs indefinitely and one that runs six
   months are different instruments. The end date is where the target's protection stops and the
   outside date becomes the only backstop.

Benchmark the rate against the memo's own hurdle. An accrual rate at or near the target IRR
**substantially neutralises duration risk for the holder inside the accrual window**, which changes
the trade rather than merely colouring it, and it must be carried into Section G's math per
`references/entry-price-target-irr.md` — not left in prose.

## Threshold framing comes before concentration — always

Resolve **horizontal vs. vertical vs. market-extension before any concentration discussion**, and
say so in one line at the top of section C. In a genuine market-extension deal — the ZYME/TBPH
exemplar, an oncology biologics company buying a respiratory small-molecule franchise — there is no
relevant market in which both parties participate, so market-share and HHI computation is not
"unavailable", it is **inapplicable**. Those are different statements and the memo must make the
right one. Writing "HHI could not be calculated" where the honest answer is "there is no shared
market to measure" invites a reader to think the analysis is incomplete when it is complete.

**Overlap gate.** If the screen comes back clean — no horizontal or vertical overlap, no concerning
acquisition pattern — section D collapses to a short theories-of-harm table plus a paragraph
explaining why, with the overlap table as the evidence. Do not manufacture depth where none is
warranted; a two-page section D on a market-extension deal is padding, and padding is how a reader
loses the ability to tell your LOW from your MODERATE. Where overlaps exist, run D in full for every
overlapping line.

**On a sector-gated deal the gate binds harder.** A clean overlap screen there is not an invitation
to demonstrate thoroughness across every theory of harm — it is the finding, and the length it frees
belongs in Section E's Approval Clock Build. Keep sections C and D to the screen, the overlap
narrative, the competitor-disclosure and prior-cooperation checks, and a theories table where each
row gets its reasoning in a sentence or two rather than a paragraph. The discipline to hold to: a
reader should finish section D knowing the competition analysis is complete, and should feel that the
memo got to the regulatory build quickly because that is where the risk lives.

## Narrate the overlap before you define the market

A reader should be able to follow the overlap line by line in plain English before hitting a
concentration or HHI discussion. Immediately under section C's Overlap Screen table, write one prose
paragraph — not a new subsection, not a table — that walks each row the table surfaces and states
plainly whether it reads as genuine head-to-head competition or complementary/adjacent positioning,
e.g. "In [product line A], {TARGET} is a niche participant and {ACQUIRER} is largely absent; in
[product line B], {TARGET} leads and {ACQUIRER} is not a material player; the two are split in
[channel C]; the one line where both parties genuinely participate is [product line D]." This is the
paragraph a reader should be able to stop after and already understand where the real overlap is,
before the market-definition-and-concentration subsection formalizes it.

Where that narrative surfaces a line with real apparent overlap, the market-definition-and-concentration
subsection that follows must run an explicit **narrow-vs-broad sensitivity check** for that line, not
just state one conclusion: name the narrowly-drawn market definition (e.g. "electronic-only execution
in this product"), name the more broadly-drawn one (e.g. "all execution channels including voice/
bilateral"), state which one the analyst believes is the economically correct definition and why
(customer type, protocol, trade size, or channel differences are the usual drivers), and say plainly
whether the narrow definition — if a regulator insisted on it — would change the read. Do not land on
the broad definition silently; show the comparison so the reader can judge the call independently.

**Prior Cooperation / Complementary-Relationship check.** Alongside the existing verbatim-competitor
and mutual-listing check in section C, run one additional, explicit check: has there been any prior
joint venture, liquidity-pool or order-flow merger, index-licensing arrangement, data-sharing deal, or
distribution agreement between the two parties, announced or disclosed before this deal? Search press
releases, prior 8-Ks, and trade press for this specifically — it is a different question from "do they
name each other as competitors" and the two can point in opposite directions (a target's 10-K naming
the acquirer as a competitor does not preclude the same two firms having jointly operated a liquidity
pool). State this as a positive or negative finding, cited, in its own short paragraph or two-row table
(`Arrangement | Date & source`) — not folded into the competitor-listing table, since it answers a
different question and a reader should be able to find it independently.

## The competitor check runs in both directions

The mutual-listing check asks who each party names. That question has a failure mode built into it:
**a Competition section that names nobody returns nothing, and the memo has no way to tell the reader
whether that silence means the market is genuinely undefinable or simply that this issuer's counsel
drafts competitor disclosure in categories rather than names.** Those are very different facts, and the
difference is invisible from the outbound direction alone. A filing that describes "revenue cycle
technology vendors, point solution vendors, and EHR systems providers" without naming a single company
is not evidence of no competition — it is evidence of a drafting choice, and reading it as the former
produces a Section C that looks thin for reasons that have nothing to do with the deal.

The fix is to ask the question the other way: **who names this party.** Run it on the target, and on a
strategic deal the acquirer as well.

**Why the inbound answer is often the better evidence.** A company's own Competition section is
self-serving — there is a live incentive to describe rivals vaguely, and issuers in consolidating
markets frequently do. A rival's filing naming *your* party is a third party's statement against its
own interest, sworn in a document written months before this deal for an unrelated purpose. When the
inbound check produces a verbatim naming, weigh it at least as heavily as a self-listing would have
been weighed, and present it that way rather than as a consolation prize for a failed outbound check.

**How it runs, and why it doesn't cost the module its speed:**

1. **Always, both parties — one `entity-neighbors` call each, inside Agent B's existing batch.** Query
   the ticker (or company name) at `hops=1`, restricted to `rel_types` such as `["CO_MENTIONED_WITH",
   "MENTIONS", "IN_INDUSTRY", "IN_SECTOR"]`. It returns structural adjacency from the indexed corpus
   with no filing reads and no paging, so inside a gather block that is already running it adds no
   serialized time. Its output has a home: it **populates candidate rows in the Peer Set table**,
   tagged in the "Named by" column as corpus-adjacency rather than as a filing disclosure. Keep the
   distinction honest — co-occurrence is not a company naming another company, and an adjacency row is
   never written up as though it were a disclosure — but do not discard it either. A signal with no
   output surface anywhere in the memo is a call that quietly stops being made.
2. **Always — the inbound EDGAR leg, up to three peer filings.** This runs on every deal, not only
   where the outbound check came up empty. A successful outbound check means the memo has competitor
   *text*; it does not mean the memo knows the peer set, and treating the first as proof of the second
   is how a memo ends up with two competitor lists and no answer to "who are this company's peers."
   Take the **three** most plausible public peers (from step 1, from the parties' own disclosed lists,
   from the sector, or from Agent D's market-structure work), pull each one's most recent 10-K
   Competition section, and check whether either party appears. Three is a cap, not a target — stop
   early once the peer picture is settled, and batch all three rather than walking them one at a time.
   Where both parties' own lists are already rich and mutually corroborating, this leg can be short:
   confirm the biggest names and move on.
3. **Never recurse at T+0.** Following each named competitor into *its* competitors builds a network
   map and costs many minutes, most of it spent on names with no bearing on this deal — a diversified
   acquirer's Competition section covers every business line it has, so the map fills with noise unless
   someone spends judgment isolating the relevant slice. That is a real research product and it belongs
   to `hour-1`, which has both the time and the sell-side coverage to do it properly. At T+0 the
   question is narrow — does sourced evidence of a shared market exist — and one hop answers it.

**What reaches the memo — two things, and the second is the one readers ask for.**

First, Section C's Verbatim Competitor Disclosures table gains a short inbound companion (see
`references/memo-template.md`): the naming company, its filing, and the naming language quoted exactly.
That table is narrow evidence for the overlap argument. Extend the cross-reference sentence to cover
both directions and state any asymmetry plainly — "{TARGET}'s own 10-K names no competitors, while
{PEER}'s 10-K names {TARGET} directly" is more informative than either half alone.

Second, and required on every deal, Section C carries a **Peer Set & Scale table** — the consolidated
answer to "who else is in this market, how big are they, and which of them are tradeable." It is built
by reconciling every source the run already touched: the target's own competitor list, the acquirer's
list, any inbound namers, the graph-adjacency candidates, and whatever sizing data Agent D's
market-structure work returned. **Two unreconciled lists sitting in a verbatim table are not a peer
set**, and the difference is not cosmetic — reconciliation is where the findings are:

- **Names appearing on *both* parties' lists are the single clearest evidence of a shared market**, and
  the memo has to say so explicitly rather than leaving the reader to diff two tables by eye. This is
  the most commonly missed finding in the whole section. A real failure mode from this module's own
  history: an acquirer's 10-K named five firms, the target's named three, and three of the largest
  firms in the industry appeared on *both* lists — evidence that went entirely unreported because
  nothing in the memo ever put the two lists side by side. Resolve subsidiary relationships before
  concluding a name is unique to one list (a parent on one list and its operating subsidiary on the
  other is the same participant, and missing that understates the overlap).
- **Resolve each peer to a ticker or to private-with-owner.** A peer set the reader cannot act on is
  half a deliverable, and on a sponsor-adjacent deal the ownership column is what surfaces a portfolio
  overlap Section B might otherwise reach only from the other direction.
- **Carry scale into the table, cited.** Unit volumes, revenue, subscriber counts — whatever the
  industry's natural denominator is. This data routinely gets gathered and then stranded in an evidence
  cell or a prose sentence, where the market-definition subsection has to re-derive it inline. Landing
  it in the table once means Section C's narrow-vs-broad call can point at it instead of rebuilding it.
- Where the run genuinely could not size a peer, leave the cell as a stated gap. The table's value is
  that every populated cell is sourced, not that every cell is full.

**Two honesty limits.** An inbound naming establishes that a third party considers the parties to
compete; it does not by itself establish the relevant market, closeness of competition, or any share
figure, and the narrow-vs-broad sensitivity call still has to be argued on its own evidence. And where
the inbound check also comes back empty, that is now a real finding rather than an untested assumption
— write it as one, naming how many filings were screened ("no filer among the N screened names
{TARGET} as a competitor"). A negative result from a search that actually ran is worth something to the
reader; an unexamined silence is not, and the whole point of this check is to stop reporting the second
as if it were the first.

## Litigation cited as market-definition evidence must be status-checked

Any lawsuit, agency complaint, or arbitration cited in Section C or D as evidence of market power,
foreclosure, or anticompetitive conduct — including one surfaced only as background color on the
target or acquirer's competitive position — gets an explicit, dated disposition check before the memo
is closed out. "No public disposition found" is a valid answer only after a real search for one: query
the docket directly (PACER/CourtListener case number if known), search the case caption plus
"settlement," "dismissed," "consent," or "judgment," and check both parties' subsequent 8-Ks and press
releases for a resolution announcement, since a settlement is often disclosed there before any docket
entry is indexed. A case still shows as "pending" on some aggregators for months after it has actually
resolved — treat a stale aggregator listing as a reason to check further, not as the answer.

State the disposition in the memo itself, next to the citation, not just in a footnote: settled (with
date and, if known, terms), dismissed (with prejudice or without, and why), still pending (with the
docket's most recent entry date, so the reader knows how current the "pending" read is), or — only
after the search above has actually been run — genuinely unresolved/unavailable.

**A settlement is not automatically confirmatory of a foreclosure theory, and is often the opposite.**
A case that resolved through a licensing arrangement, an interoperability commitment, or another
commercial accommodation is evidence that the alleged market-power problem was addressed through
ordinary bargaining between the parties, without regulatory intervention — which cuts against, not
for, a foreclosure or essential-facility theory built on that case. Do not carry a case forward as
open evidence of anticompetitive risk once it is known to have settled; restate what the settlement
actually established and let that inform the read, rather than defaulting to the pre-settlement
framing because that framing was already drafted.

## The merger agreement is the parties' own confession

Section E's core is the regulatory architecture, and it is read clause by clause, not summarised.
Lawyers negotiate antitrust risk in specific places, and each one is evidence about how much risk
they thought they had:

- **Efforts covenant standard** — "reasonable best efforts" vs. "hell or high water", and whether
  the divestiture obligation runs one way or both.
- **Divestiture cap construct** — an unlimited commitment, a materiality standard, or the tell-tale
  **"except as set forth on Section X of the Parent Disclosure Schedule"**: a pre-agreed confidential
  remedy basket, materially different from either extreme, and a sign the parties already mapped the
  problem assets before signing.
- **Litigation commitment** — defend through final non-appealable judgment, or something weaker.
- **Remedy-proffer clock** — "proffer no later than N months from HSR filing". Compute the calendar
  date and carry it into every timeline scenario.
- **Pull-and-refile rights** and their caps; HSR filing deadline computed from the covenant.
- **Antitrust reverse termination fee** — state explicitly whether the reverse fee is
  antitrust-specific or a generic breach/financing fee, and benchmark it as a % of EV against the
  conventional 3–4%. A reverse fee well above that band is itself negotiated evidence of perceived
  antitrust risk, and one well below (or absent) is evidence the parties thought the path was clean.
- **Interim acquisition standstills, quoted verbatim** — covenants barring either party from
  acquiring in named product spaces during pendency. The named spaces are the parties' own lawyers'
  map of the competitively sensitive markets, and they are frequently the single best
  market-definition evidence available on day one. Note whether they name specific spaces or are
  generic.
- **Business Day definition** — read it and note which holiday calendars it names (for example New York and
  Paris). Every filing deadline and "within N business days" period is counted under that definition with
  `scripts/deal_clock.py bdays`, not by weekends alone.
- **Burdensome Condition definition** — quote it. It is the actual ceiling on what the buyer must give up,
  and it is where a line-of-business ring-fence for government or defense work would sit.
- **Government-contracts and security-clearance representation** — see `references/national-security-screen.md`.
- **Which regimes condition the close** — read Article VII and state which antitrust and foreign
  regimes are closing conditions versus which appear only as covenants. The difference decides
  whether a foreign regulator can actually block.

Cross-read this against the parties' own **synergy framing** from the press release and deck.
Synergies built on capacity rationalisation, plant consolidation, or pricing / go-to-market overlap
are admissions of horizontal proximity — quote them and cross-reference into section D. Likewise any
slide mapping the parties' pro-forma combined share, rank or "#1/#2 in X" position: a company
drawing its own combined market map is among the strongest overlap evidence there is. Capture it
verbatim with the slide cited.

## Precedents

The clearance handicap in section F rests on precedent rows, and a row that cannot carry its
specifics is dropped rather than softened. Every row states a specific announce→close day count (or
a dated range) and the actual outcome; vague timing words are not acceptable, a still-pending deal is
not a precedent, and non-comparable "contrast" rows do not belong in the table.

**Every row carries its HSR-regime era — there are now three, not two.** (1) **Pre-February 2021**:
early termination was routinely granted (roughly 73–81% of requests, per the agencies' own HSR annual
reports) — an ET day count from this era reflects a real, common fast-track outcome. (2) **February
2021 – February 2025**: ET was fully suspended; no grants were possible, so any precedent that closed
inside this window necessarily ran the full statutory clock, whatever its day count shows. (3)
**February 2025 – present**: ET was reinstated alongside the FTC's new HSR rules, but is running at a
low grant rate — approximately 29% of requests granted in FY2025 (agencies' HSR annual report, as
tracked by the American Action Forum), well under the pre-2021 range. A recent ET grant is real and
citable, but it is still the exception, not the baseline expectation for a new filing. Flag which era
each row falls in — a pre-2021 ET grant still cannot be used as today's floor, and a post-reinstatement
ET grant should not be read as "ET is back to normal." **Verify live**: the FY2025 grant rate is early
post-reinstatement data and may move as agency practice matures — check the most recent HSR annual
report or a law-firm tracker before assuming ~29% still holds on the deal in front of you.

**Read every precedent for procedural friction, not just its outcome date.** "Cleared on the initial
waiting period, no second request" is the headline outcome; it is not the whole story. Search
specifically — as its own query, alongside the outcome/day-count search, not folded into it — for
whether the precedent required a **pull-and-refile / withdraw-and-refile** (the parties withdrawing
and resubmitting their HSR notification to reset the clock, almost always a signal the reviewing
agency needed more time without issuing a formal second request), an **extended or voluntarily
lengthened waiting period**, or any other procedural friction short of a formal second request. Two
deals that both "cleared without a second request" can have had very different regulatory experiences,
and a precedent read that stops at the binary outcome will systematically overstate how clean the
comparable actually was. State the finding plainly in the precedent row or its accompanying sentence —
"cleared on the initial waiting period, no second request, but required a pull-and-refile before
expiry" is a materially different, more cautious data point than a bare "no second request," and both
the clearance handicap and the timeline scenarios in Section E should reflect whichever is actually
true.

**When a market-quantification gap can't be closed with deal-specific data, retarget the search to the
acquirer's or target's closest analogous prior transaction before recording the gap as final.** If
Section C cannot source a market-share or HHI figure for the actual overlap line after a direct search,
run one more `semantic-search` (namespace `arbjournal`, plus any other available deal-research corpus)
and one more web search — not for this deal's name, but for the acquirer's (or target's) most recent
comparable transaction in the same or an adjacent product line. A specialist research shop's HHI table
from that acquirer's last deal in the same space is frequently the best available proxy for a line that
has no citable data of its own, because it was built by someone doing exactly this kind of
market-definition work on the closest available analog. Use it explicitly as a proxy, cited to its own
transaction and date, never presented as if it were a figure specific to the current deal — e.g. "no
citable market-share data exists for [current overlap line]; the closest sourced analog is [firm]'s
[year] HHI table for [acquirer]'s prior acquisition of [comparable target], which put [acquirer]'s
share in the same product line at X% — cited as a proxy, not as data on the current transaction." This
converts a stated gap into a sourced, appropriately-caveated estimate wherever a genuine analog exists,
and costs at most two additional searches, only run when the direct search has already come back empty.

**Show the acquirer's whole record and its outcome mix, not just its most comparable or most memorable
deal.** For a repeat acquirer, list every deal of the last ten years that went through HSR review (older
only if in the same product line) with overlap type, outcome and day count, then state the mix in one
sentence. A Second Request on a direct-overlap deal is weak evidence about a complementary deal by the
same buyer, and a clean history is weak evidence about a direct overlap; the memo says which case it is.
The one worst precedent is a row in the mix, never the verdict by itself. See
`references/calibration-principles.md`, principle 2.

Prioritise, **on an antitrust-gated deal, product/market/overlap-type comparability first**: (1) the
acquirer's or sponsor's own prior acquisitions in the *same product market* as the current overlap —
usually the single best comparable; (2) same-industry deals by any buyer; (3) same-regulatory-shape
deals in adjacent industries, clearly labelled as adjacent. A same-buyer deal in an unrelated product
market does not outrank a different-buyer deal in the same product market — rank by what was actually
being combined, not by who signed. Where a same-buyer/different-market deal is included, label it
explicitly as a buyer-posture data point, not an overlap comparable. Source from ArbJournal deal
files first (cite from hit metadata — title, institution, publication date), falling back to the
precedents' own completion 8-Ks and press releases for dates.

**On a sector-gated deal, invert the first two keys: rank by approval body first, acquirer archetype
second, product market third.** What is being predicted is a regulator's behaviour toward an
applicant of this type, not a market's structure. A recent change-of-control review by the same
supervisor over a similar applicant is a better precedent than an older deal in the identical product
line before a different regulator — because the review, not the market, is what sets the date.

**Apply a five-year recency ceiling to sector-approval precedents, and say so when you breach it.**
Regime changes make older rows quietly misleading: HSR early termination ran a very different regime
pre-2021 (routinely granted) than 2021–2025 (fully suspended) than today (reinstated since February
2025, but granted in only ~29% of FY2025 requests) — see the three-era framework in the "Precedents"
section above — and supervisors' postures toward particular acquirer archetypes have moved
substantially since 2022 (see `references/regulatory-clocks.md` for the specific overlays). A
pre-2021 precedent can understate both the antitrust floor and the first-time-owner review. Rows
outside the five-year window may be cited only where no in-window precedent exists for that approval
body, and must be labelled out-of-window with one sentence on what has changed since.

**Every row carries a "why analogous" cell tied to the specific approval being predicted** — not
"same industry," which is not a reason. Write something a reader can check: *"same supervisor, same
threshold, same non-domestic applicant posture as this deal."* A precedent that cannot say which
approval it is a precedent *for* is decoration and should be dropped.

**Where disclosable, capture per-approval day counts, not just announce→close.** Filing dates,
hearing notices and approval orders are frequently public on sector-regulator websites even where the
deal file only records the total timeline. One well-sourced per-regulator day count outranks five
total-deal timelines, because it feeds the Approval Clock Build directly instead of requiring the
reader to back it out.

## Plain-language layer — required in every memo

The memo must read cleanly to a smart reader from another field. Apply
`references/plain-language-primer.md`: B.0 (companies in plain English, with the fixed segment and
geography tables — bare dollar figures in millions, no "mm"/"M"/"millions" wording, % of total in the
adjacent column), B.4 (bad-actor check, target first, then acquirer), C.0 (five baby steps plus a
Jurisdiction table for every regime screened in E.1), and D.0 (all 11 HSR guideline rows plus 1a).
Gather implications: Agent B pulls both parties' segment and geography tables as filed (for 40-F/20-F
filers use the annual information form and the financial-statement exhibit, since `extract-10k` does
not parse them); Agent C pulls each party's history and deal table with dates and prices plus the
conduct check; Agent D keeps the sourced-shares-or-stated-gap rule. Where two sources conflict on a
basic fact, the company's own latest filing controls and the conflict is stated once.

## Output

**Default: deliver the memo in chat as text and tables**, following `references/memo-template.md`
exactly for section order and required tables. Read that file during the gather window. Lead with the
verdict — a reader who stops after section A should already have the answer, and the rest should
be the evidence for it.

**Open with a one-page desk read.** Before Section A, give a short block a trader can read in a minute: the
verdict in plain words; the three reads (first review, duration, challenge or remedy) each rated; the
base-case close in days from announcement; the one regulator to watch (on a state-led deal, the states that set the earliest date and the latest tail, and any conditional state); and the one line from Section G on
whether the spread looks mostly time value, technical or deal risk. Then deliver the full memo. The block
adds no new analysis; it is the memo's own conclusions in one place.

**Citations.** Page footers print at the end of a page, so text that appears after the footer for page N is on
page N+1. Cite the agreement's own section number as well as the page, and cite the framework item where one
applies.

**Single-source flags.** Wherever a number that drives a call comes from one source, or was read from a
chart, say "single-source" or "chart-derived" beside it.

**Delta mode.** If a memo already exists in this chat and new material arrived, follow
`references/delta-mode.md` rather than rebuilding the memo.

Two conventions worth holding to. **Skimmable is a formatting property, not a length property**:
restructure with a verdict line, bold lead-in takeaways and detail-in-tables — never abridge the
evidence to make it shorter. And **anything with three or more parallel facts goes in a table**,
with its source in the caption.

**Before delivering, run these four checks on Section C.** Each one exists because its absence has
produced a memo that read as complete and was missing something the reader immediately asked for:

1. **Is the Peer Set & Scale table present?** It is required on every deal. Its absence is not excused
   by both parties having disclosed competitor lists — that condition is the common case, not a reason
   to skip the consolidated view.
2. **Does every peer row carry a source, and a ticker or private-with-owner?** An unsourced or
   unresolved row is not usable.
3. **Did the memo state which names appear on more than one party's list** — by name, in a sentence,
   not implicitly by putting two tables near each other? If no name appears on both lists, say that
   too, since it is equally informative.
4. **Is every sizing figure the run gathered actually in the table** rather than stranded in a prose
   paragraph or an evidence cell? If the market-definition subsection derives a share inline, the
   underlying figures belong in the peer table first and should be referenced from there.

**File naming, one rule:** any saved file is named `[Doc Type] - [PARTY] x [PARTY] ([MM.DD.YYYY])`, for
example `Antitrust Minute-1 - PTC x Schneider (10.05.2026)`.

**On explicit request only** ("make it a doc", "put it in a Word doc", "send me the memo as a
file"), build the Meteora house-format `.docx` with the bundled script rather than hand-writing
document code:

    python3 -m json.tool content.json > /dev/null    # validate first
    python3 scripts/build_report.py content.json "Antitrust Minute-1 - {ACQ} x {TGT} ({MM.DD.YYYY})" --both

The JSON schema is in the script's docstring (cover block, `toc`, static `footer`, RAG cells as
two-element arrays `["LOW RISK","G"]`, `verify[]` checklist). `--both` writes the docx, an HTML twin
and the checklist, and greps every `verify[]` entry against the HTML instantly. Populate `verify[]`
as you author, one fact per entry, written as a **literal substring in the document's own notation**
— bare tokens like `$107,500,000` or `Simpson Thacher & Bartlett`, never a descriptive phrase, since
a paraphrase cannot match and produces a false miss. The filename follows the house deal-document
convention: `[Doc Type] - [PARTY] x [PARTY] ([MM.DD.YYYY])`.

If a required input is missing — merger agreement not yet filed, sponsor portfolio opaque, no
citable market-size source — state exactly what is missing and what it prevents, then deliver the
rest. A memo with three named gaps is more useful than one that papers over them.

## Open questions and the autonomous deep-dive pass

**The T+0 memo is not necessarily the end of the run, and this is not optional polish — read
`references/open-questions-deep-dive.md` in full before treating any run as closed.** In short: screen
the finished memo for items where the answer rests on a general rule or assumption rather than a
primary-source read, and where a wrong answer would move the base-case date or the verdict — a captive
or other carve-out entity not yet built out in `references/regulatory-clocks.md`, a buyer-archetype
question the precedent set can't cleanly answer, a regulator's genuinely open discretionary standard.
Where any exist, **do the primary-source research and send the deep dive as a follow-up immediately, in
the same turn, without waiting to be asked** — never stop at flagging the gap in the T+0 memo and leave
it there. Close every such item with a standalone, cross-model-portable entry per
`references/memo-template.md`'s Open Questions — Cross-Model Verification format; that block is the
required input to `hour-1`'s Perplexity-council reconciliation step. A clean run can close with zero
open questions — say so in one line rather than manufacturing one. **When the merger agreement or a later
filing answers an earlier open question, mark the earlier statement superseded and give the answer with its
citation**; do not leave the old question standing next to the new fact.

## Closing step

The memo itself is a self-contained, point-in-time deliverable — but **the run is not necessarily over
at delivery.** See "Open questions and the autonomous deep-dive pass" immediately above and
`references/open-questions-deep-dive.md`: screen for open questions before treating the run as closed,
and where any exist, continue straight into that pass rather than stopping to ask whether you should.

Where this module was run as one input to a larger deal-completion report, say which house sections
it populates (the mapping table at the top) so the downstream workflow does not redo it.

## Reference files

- `references/calibration-principles.md` — **the v11 calibration layer**: the four-test overlap check
  (management language, substitute vs. complement, same customers, direction of naming), the acquirer's
  full record and outcome mix, the three separate reads (first review / duration / challenge), the
  steelman-both-neighbours step, tested reconciliation of disagreeing sell-side views, sourced-only base
  rates, and the verdict stress-test line. Read in full during the gather window and again before
  Section A is locked.
- `references/open-questions-deep-dive.md` — **the two-phase execution model**: how to screen the
  finished memo for open questions before calling a run done, do the targeted primary-source deep dive
  immediately and without re-prompting, and deliver it as a follow-up with a cross-model-portable
  Open Questions block. Read this once a run is otherwise ready to close out.
- `references/memo-template.md` — the six-section analytical output spec (plus the Section G pricing
  block, added at the end), required tables, house formatting, and the Open Questions — Cross-Model
  Verification format used by the deep-dive pass. Read during the gather window, before composing.
- `references/gather-prompts.md` — the six fixed gather-agent prompts (A to F). Read and launch; do not
  compose agent prompts from scratch.
- `references/pe-buyer.md` — sponsor portfolio discovery, roll-up seriality, sponsor-specific
  theories of harm.
- `references/strategic-buyer.md` — acquirer segment mapping, mutual-competitor-listing check,
  strategic-specific theories of harm.
- `references/entry-price-target-irr.md` — the Section G Entry Price to Target IRR methodology:
  fresh-pricing requirement, the baseline/±30-day scenario derivation, the 8%-default parameterized
  hurdle, the ticking-fee-adjusted consideration table, and the required four-part Read. Read it in
  full during the gather window alongside the other reference files.
- `references/regulatory-clocks.md` — **the encoded per-regime clock mechanics**: statutory period,
  clock-start definition, interruption mechanics, observed practical range, and the acquirer
  attributes that lengthen each review. Insurance (US state Form A, the state captive-insurance
  carve-out regime, and the major non-US prudential supervisors) is built out in full, alongside a
  cross-sector "Financial-services ancillary regimes" entry (FINRA/broker-dealer, RIA/Investment
  Advisers Act, and a foreign-footprint flag) that applies regardless of the deal's primary sector;
  other sectors are stubbed with the load-bearing facts and a pointer to research them live. This is
  the file that makes Section E's Approval Clock Build constructible on a T+0 clock instead of researchable from
  scratch. Read it during the gather window.
- `references/foreign-merger-thresholds.md` — **the jurisdictional threshold screen behind Section
  E.1's "Foreign merger control" row**: the actual notification tests for the EU (EUMR Article 1),
  UK CMA, SAMR (China), ACCC (Australia), Canada's Competition Act, and the Investment Canada Act
  (a separate foreign-investment net-benefit/national-security review, not a competition filing),
  each with the data it needs and a worked EDGAR-based application sequence. This is what turns
  "foreign merger control may apply" into a named test, cited figures, and a notifiable / not
  notifiable / indeterminate conclusion per regime. Read it during the gather window wherever either
  party has a non-US revenue footprint.
- `references/vector-db-retrieval.md` — the P1 (precedent deals — now including open/live and
  terminated deals, labelled by status, not just closed ones), P3 (competitive positioning),
  P5 (enforcement-posture roster) and **P6 (Chain Bridge Research regulatory pathway)** vector-DB
  pulls used by Agents B, D and E: exact filters, the empirically-confirmed traps (`industry` vs.
  `sector`, the `publication_ts`/`deal_timeline_days` silent-failure fields), which deal_id covers
  which regulator, and P1's mandatory regime-specific second pass. Read it in full during the gather
  window, before Agents B, D and E run.
- `references/gate-led-structure.md` — **how the antitrust-gated/sector-gated/dual-gated
  classification reshapes the memo itself**: section-order and emphasis around the gating item, the
  hard ~15%-of-length budget on LOW-scored non-gating topics with no full table, and the mandatory
  second research pass on any MODERATE+ or still-open item, plus a cross-reference to the named-state
  granularity requirement for state-by-state licensing regimes. Read it alongside
  `references/memo-template.md` during the gather window, once the classification is callable.
- `references/state-healthcare-regimes.md` — **v13**: state health care approvals. The three layers (transaction-notice
  and review laws, licensure and change of ownership, federal program and accreditation), the perimeter test
  (thresholds not site counts, right level, target's own history, agency notice pages), the reference table of state
  laws with source tags, floors and tails arithmetic, precedent era and basis, the Section A / E.2a / E.2b output
  template and the OPCH worked example. Read it whenever a deal's approvals include state health regulators.
- `references/spread-pressure-supply.md` — **v12**: the nine checks (liquidity, float, premium and break price,
  upside against downside, buyer stock and financing wording, short interest, sell-side supply, tape path,
  index events), the price fallback order, and the split of the spread into time value, technical premium and
  risk premium. Read during the gather window and apply in Section G.
- `references/delta-mode.md` — **v12**: how to re-read a deal when new documents land (same-deal check, three
  separate reads, what-changed table, re-based clock, superseded questions).
- `references/national-security-screen.md` — the CFIUS / FOCI screen: what to read in the agreement and filings,
  the target sensitivity profile, the mitigation-instrument sort (must accept versus may refuse; separation and
  scale), the buyer side, the re-run rule when the agreement is filed, and the "not disclosed" rule for defense
  revenue share.
- `references/standing-public-record.md` — **10/6 revision**: Agent F's checklist. Our own library first, sector
  trigger packs (defense and government in full, others in short form), rival mirror, acquirer profile, regulator
  state, prior strategic interest, the coverage ledger, questions for counsel, and tool fallbacks. Read it during
  the gather window; Agent F reads it itself.
- `scripts/deal_clock.py` — **v13** calculator: business days, calendar-day add (`adddays`, for state floors and tails),
  outside-date ladder, spread, implied entry price, hurdle, spread decomposition, downside ratio. Standard-library Python.
- `scripts/build_report.py` — Meteora house-format docx builder, used only on explicit request.
- `references/plain-language-primer.md` — **the plain-language layer**: B.0 companies in plain English with the fixed segment and geography tables and history/M&A table, B.4 bad-actor check, C.0 antitrust-in-baby-steps with the jurisdiction table, and D.0 the full 11-guideline HSR table with honesty rules for the Triggered column. Read in full during the gather window.
