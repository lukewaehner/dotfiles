# Precedent, Threshold & Verdict Methodology

This is a methodology reference, not an output template — nothing here names a new report section.
Everything it produces lands inside a section the locked report shape already has: the
pacing-item note inside the Approvals & Gates table, the 10-K/jurisdictional context inside Section 4,
the precedent-informed probability read and Optionality paragraph inside Overall Risk Assessment, and
the multi-window premium, seasoning, market-implied-probability, and verdict lines inside the closing
Gross Spread Calculation block. It exists because a merger agreement can tell you the efforts standard,
the fee, and the Outside Date — it cannot tell you how long a regulator actually takes, whether the
market already agrees with your read, whether there's any upside if the deal breaks, or what to watch
next. Those gaps are what separated a genuinely great same-day note (and a trusted broker's genuinely
sharp T+1 follow-up on a different deal) from a merely-thorough one in the comparisons this version is
built from.

## 1. Precedent-timeline pull

Goal: turn "the deal guides to 1H 2027" into a specific, defensible working date with a stated
day-count and a stated assumption.

**Sourcing.** Identify 2–3 precedent deals that cleared through the *same lead regulator* named as the
pacing item in the Approvals & Gates table's Notes column (e.g. UK CMA, US FTC/DOJ second request, a
specific sectoral regulator). Run the **P1 pull** in `references/vector-db-retrieval.md` first — read
that file in full before this step and apply its filter exactly (`namespace='default'`,
`document_type: "Merger Arb Analysis"`, filtered by GICS **`sector`, never `industry`**, gated on
`actual_completion_date != ""`). This is a structured lookup, not a research task: the returned
`hsr_outcome` and `deal_timeline_days` fields usually give the precedent's actual clearance timeline
(prenotification-to-Phase-1, Phase-1-to-unconditional-clearance, or HSR-second-request-to-clearance,
as applicable) directly. Use `WebSearch` only to fill in what the pull doesn't cover — this is
public-record regulatory-process information, not something in the agreement.

**Analogous/not-analogous reasoning — mandatory, not optional.** For every precedent cited, state in one
clause why it is or is not a good comparison to the deal at hand: same regulator and same general asset
class is not sufficient on its own — compare competitive-overlap severity, deal size, and whether the
precedent needed a second-phase/in-depth review or cleared at the first stage. A precedent that had
"more serious competitive issues" than the deal being analyzed should be named and explicitly discounted,
not silently used as if it were directly on point. Example register (house benchmark): *"Precedents cited
for [X/Y] and [A/B] don't appear directly analogous given their more serious competitive issues."* A bare
comp name with no reasoning attached does not meet the bar — cut it rather than list it unexamined.

**Producing the working date.** Combine: (a) the precedent-implied timeline for the gating regulator, (b)
the contractual HSR/foreign-filing deadlines already extracted in Section 3/4 of the 14-section report,
and (c) a stated assumption about review depth (e.g. "assuming a targeted Second Request/pull-and-refile
rather than a full in-depth Phase 2"). State the resulting date with its day-count from signing, e.g.
"February 20, 2027 (205 days)" — the day-count is not decoration, it lets the reader immediately judge
whether the estimate is aggressive or conservative relative to the agreement's own Outside Date. This
date and its reasoning belong in the Overall Risk Assessment section's completion-probability prose and
feed the "assuming [close scenario]" clause on the Annualized Gross Spread line — not a separate section.
If a broader review path is plausible, name in one clause what would push the date later, and fold that
into a Key Risks bullet rather than spinning up a new subsection.

**Pre-signing diligence signal.** If the agreement's Confidentiality Agreement date (Section 12.1 of the
14-section extraction) predates signing by several months, note that as weak positive evidence the
parties may have done regulatory-strategy legwork pre-signing — worth a single clause, not a claim of
certainty.

**Procedural friction, not just outcome.** For every precedent cited, search specifically — as its own
query, not folded into the general clearance-timeline search — for whether that deal required a
pull-and-refile / withdraw-and-refile of its regulatory filing, an extended or voluntarily lengthened
waiting period, or any other friction short of a formal second request or Phase 2 review. "Cleared
without a second request" and "cleared without a second request, but only after a pull-and-refile" are
both technically clean outcomes in the binary sense, but they describe different regulatory experiences,
and a precedent read that stops at the headline outcome will understate how much friction the comparable
actually encountered. State the finding in the same clause that names the precedent as analogous or not
— e.g. "[Acquirer]'s [year] acquisition of [prior target] cleared without a second request but required
a pull-and-refile before the initial waiting period expired, suggesting the reviewing agency needed more
time even where it ultimately didn't escalate formally." This belongs in the same precedent-timeline
prose already described above, not a separate subsection, and it should inform how conservative the
resulting working date and its "assuming [review depth]" clause are.

## 2. Jurisdictional-threshold check

For every foreign/supranational competition regime that might plausibly apply beyond the ones already
named as closing conditions (most commonly: EC/EU merger control, but check for any other regime
suggested by the target's disclosed geographic revenue mix), do not just assert "unlikely" — show the
actual number against the actual threshold:

1. Pull the target's (and if relevant, combined pro forma) revenue by geography from the most recent
   10-K or press materials — `mcp__MeteoraMCP-AWS__edgar-filing-text` or `edgar_company_facts`.
2. State the relevant filing threshold for the regime in question (e.g. EU Merger Regulation combined/
   individual turnover thresholds) — a `WebSearch` for the current threshold figures is appropriate here
   since these are public regulatory-process facts, not house data.
3. Show the comparison as a plain calc block: `Revenue outside US/UK: $XXX.XM (below/above [regime]
   threshold of $XXX)`.

If the revenue figure needed for this check genuinely isn't disclosed at the needed granularity, say so
plainly rather than asserting a conclusion without the number behind it — that is itself a fact worth
noting (e.g. "geographic revenue split not broken out at sufficient granularity to test the EC threshold
directly; press-disclosed total non-US/UK revenue of $X is used as a proxy").

## 3. 10-K competitor cross-check (feeds Section 4 of the 14-section extraction)

Already sourced in Step 1 of the main skill file. Use it here to sanity-check headline antitrust
overlap numbers before they get written up. The house benchmark for why this matters: a first pass based
on "Googling market shares" produced a scary 30%+ pro forma headline combined share; actually reading the
target's, acquirer's, and one adjacent competitor's 10-K competition disclosures (asymmetric — target
names acquirer, acquirer doesn't name target, third competitor names both) meaningfully changed the
antitrust read toward "low break risk, narrow targeted overlap." Write up:

- Whether the target's 10-K names the acquirer as a direct competitor (and in what specific
  sub-markets/venues, if named specifically rather than generically).
- Whether the acquirer's 10-K disclosure is symmetric (also names the target) or generic (describes
  competing with "other electronic trading venues" without naming firms) — this asymmetry itself is a
  signal worth stating explicitly, not just noting each fact separately.
- What a comparable third-party competitor's own 10-K says about competing with both parties — if one
  is identifiable from the target's disclosure, this is the cheapest possible cross-check on market
  definition and is worth the extra EDGAR pull every time.

## 4. Market-implied probability and the closing verdict (feed the Gross Spread Calculation block)

Write these the way a trading desk actually talks about a position, in the terse, judgment-forward
register of the two benchmark house notes this version is built from — but they are lines inside the
existing Gross Spread Calculation block, not a new section. Concretely:

- **Two probabilities, stated separately and then reconciled.** The analyst-view probability is the
  Overall Risk Assessment section's existing `Deal Completion Probability: XX–XX%` line, informed by the
  precedent read above. The market-implied probability is a new line inside the Gross Spread Calculation
  block, back-solved from live pricing against a stated downside reference:
  `(current price − downside reference) / (deal price − downside reference)`. State the downside
  reference and its basis (pre-deal unaffected close, or a named analyst downside case if the pre-deal
  anchor has gone stale) every single time — an implied-probability number without its downside
  assumption disclosed is not a usable number.
- **The verdict must be a plain sentence, not a hedge, and it is the last line of the report.** If the
  analyst view and market-implied view roughly agree and the resulting annualized return clears a
  reasonable risk-arb hurdle given the working close date, say the spread looks attractive and why. If it
  doesn't, say that plainly too — the house benchmark's exact register is the model: *"This is not an
  attractive return... we do not think we are being overly cautious at this stage."* A report that stops
  at a completion-probability range without ever answering "is this a good trade" has not done the job
  this version exists to do. This sentence closes the Gross Spread Calculation block — do not give it its
  own heading. **Where the analyst has a view, name a specific re-entry level** — a second broker
  benchmark's exact register is the model here too: *"A $5.50+ spread would be attractive given what we
  know right now."* A number the reader can set an alert on is worth more than an adjective; give one
  whenever the underlying math supports it, and only fall back to adjective-only ("attractive" /
  "unattractive" / "fair") when the position genuinely doesn't support pinning a level.
- **Forward-watch items go into the Key Risks bullet list, named and mechanistic, not generic.** Each
  item should name a specific trigger and why it would move the estimate — a price-bump rumor window tied
  to a specific date/clause, a specific regulator's approval that could slip, a specific plausible
  complainant class or lobbying angle if one genuinely exists for this deal. Do not pad to three items if
  only one or two are plausible; do not write "regulatory risk" as a Key Risks bullet when the report has
  already covered regulatory risk elsewhere in that same list — these bullets are for what to check
  *next*, additional entries in the existing list, not a restatement of what's already there.

## 5. Pre-funding labeling, duration-adjusted probability, seasoning, and Optionality

Four more pieces, benchmarked against a trusted broker's T+1 note on a different deal — all small
additions to blocks that already exist, none of them a new section.

**Pre-funding labeling.** The existing Annualized Gross Spread line is a *gross* number — it says
nothing about the cost of carrying the position. Label it explicitly `(pre-funding)` so the reader isn't
misled into reading it as a net expected return. Do not attempt to compute an actual funding-adjusted
number unless the user has given a borrow/funding rate to apply — the label alone is the honest move
when that input isn't available.

**Duration-adjusted implied probability.** The existing market-implied-probability calc (spot price vs.
a downside reference) is a snapshot; it doesn't account for the fact that a dollar of spread captured
over 60 days is worth more than the same dollar captured over 400 days. Add a second version of the
calc that discounts the downside-reference gap for the actual expected holding period implied by the
working close date from section 1 above — state the discount basis explicitly (a stated funding-rate or
cost-of-carry assumption; if none is available, a simple linear time-scaling is an acceptable, clearly-
labeled approximation). Show both the spot and the duration-adjusted number side by side — never replace
one with the other, since a reader comparing this report across deals needs the spot number to stay
comparable.

**Seasoning / liquidity check.** Pull volume traded since announcement (Step 1) against average daily
volume or float, and state it as a plain calc line in the Gross Spread Calculation block: what fraction
of the stock's typical volume — or its float — has actually traded since the deal was announced. A
spread quoted on a stock that has barely traded since signing (a small fraction of average volume, or of
float) has not been fully tested by the market yet and is a less reliable read than one on a stock that
has traded through a full session or more at real size — say this plainly when the fraction is low, and
let it inform how much weight the verdict puts on the current spread level.

**Optionality.** A different question from completion probability: if the deal breaks, is there any
upside (a topping bid becomes plausible, the standalone business holds its value), or is it pure
downside? Build this from three inputs, each already available elsewhere in the report or cheaply
sourced: (a) the forward/Company termination fee as a % of equity value, benchmarked against the
conventional 2-4% range — a fee at or below the low end of convention offers less deterrence against a
rival bid, which is modestly optionality-positive; (b) the target's standalone business trajectory —
run the **P3 pull** in `references/vector-db-retrieval.md` first (sellside/IOC coverage naming the
target's competitive position and revenue/margin trajectory — more reliable than an ad hoc search,
though it carries one hard rule: never filter that pull by ticker/sector/industry, only by
`document_type`, and put the ticker and company name in the query text instead, since a large slice of
that corpus has broken ticker/sector tagging even when the document text is fine), falling back to the
press materials, the target's own MD&A language, or a direct analyst-commentary search where the pull
comes up empty — a business that has been "melting" or losing share implies the stock is worth less
over time absent the deal, which is optionality-negative (no floor to catch a falling standalone
price); (c) pre-signing process quality — a long confidentiality-
agreement-to-signing gap combined with unanimous board approval and a single logical/strategic best
buyer is evidence the market check may have been thin or the process may have concluded with stale
comparables, which is optionality-negative (a real competitive process would more often surface a rival
bidder). Write this as a short paragraph in the Overall Risk Assessment section, immediately after the
completion-probability prose and before Key Factors — it is a different lens on the same section, not a
new one.
