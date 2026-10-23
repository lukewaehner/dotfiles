# Antitrust Minute-1 Memo — output template

**No version labels in the deliverable.** Nothing in the delivered memo — its title, section
headers, subsection headers, table rows, or footnotes — should ever contain a module version marker
or similar internal tag, whether inherited from this template's own drafting notes or from the
skill's own name. Any bracketed annotation in this file is an internal authoring note for whoever
edits the skill and is not part of the memo's content. When drafting the memo, read past any such tag
and write the instruction straight. The memo's own title should read simply "Antitrust Minute-1 —
{ACQUIRER} / {TARGET}", with no version suffix.

**Desk read first.** Before Section A, a one-page block: the verdict in plain words; the three separate
reads (first review, duration, challenge or remedy) each rated; the base-case close in days from
announcement; the one regulator to watch; and one line on whether the spread looks mostly time value,
technical or deal risk. It repeats the memo's own conclusions and adds no new analysis. Title it "Desk read".

Six analytical sections plus a required Section G pricing block, in this order.
Chat-native by default; the same structure and tables carry into the `.docx` when one is requested.
Sections C and D are **conditional in depth** — they collapse when the overlap gate finds nothing, but
they never disappear, because "we looked and found nothing" is the finding.

Label every analytical opinion with a leading `Assessment:` so it is never mistaken for a sourced
fact. Every table carries its source in the caption or a per-row source column. RAG polarity:
**green = favourable to completion** (LOW RISK, HIGH probability of clearance), amber = MODERATE /
MONITOR, red = HIGH RISK / adverse. In build JSON a RAG cell is `["LOW RISK", "G"]`.

**Number every subsection: A.1, A.2, B.1, B.2… — not just the six lettered sections.** Any
distinct sub-topic within a section (the matrix vs. the ranked watch-list in A; firm profile vs.
portfolio table vs. regulatory history in B; each theory of harm in D) gets its own number, even in
chat delivery. This is what lets a reader or a follow-up message point at exactly one finding ("check
B.3") instead of "somewhere in section B" — the numbering is a navigation aid, not a length signal,
and a two-sentence subsection is still worth numbering if it's a distinct sub-topic.

**Every table is followed by a paragraph, not just preceded by a caption.** A caption states
what the table is; the paragraph after it says what the table means — which row matters most and
why, what a reader would otherwise have to infer themselves. A table with a source caption and
nothing else is only half-delivered.

**Register: no scaffolding, conclusions first.** Do not narrate the memo's own structure to the reader
("this section will now discuss...", "having established X, we turn to Y", "the following table sets
out..."). A reader does not need to be told what a section is about to do before it does it — the
section heading already says that, and a lead sentence that restates the heading in prose is wasted
space in a document meant to be read in minutes, not skimmed for signposts. Every subsection leads with
its conclusion, then the supporting detail — never the reverse. This mirrors the fact-then-reasoning
discipline SKILL.md already requires for individual findings ("argue to a conclusion — do not report
facts and leave the reader to assemble the verdict"); apply the same front-loading at the subsection
level, not just the sentence level.

**State the memo's own triage decision in plain language, early, as part of the verdict — not as
something the reader has to infer from section lengths or ordering.** Section A's opening (below)
already requires naming the gating regulator in plain language; go one step further and frame it as the
memo's own explicit editorial decision, e.g. "This deal is gated by [the named regime], not by
antitrust — the analysis below is weighted accordingly, with the regulatory pathway carrying most of
this memo's length and the competition analysis compressed to the overlap screen and its evidence." A
reader should never have to notice, several pages in, that the antitrust section was short and infer
from that alone that antitrust wasn't the concern — the memo should have already told them so.

See `references/gate-led-structure.md` for how the classification also governs section ordering, length
budgets, and research depth — the register fixes here are about how each section is *written*; that file
covers how the memo is *shaped*.

---

## A. Antitrust Verdict & Risk Matrix

Open with the verdict in one sentence, then two to three short paragraphs: the deal in a line; the
**threshold framing** (horizontal / vertical / market-extension — this classification is resolved
here, before any concentration discussion, and on a market-extension deal it is the whole analysis);
the **regulatory intensity read** — internally this module classifies every deal antitrust-gated /
sector-gated / dual-gated to decide where the memo's length goes, but **that label itself is never
written into the memo** (see SKILL.md's labelling rule). Instead, name in plain language the one
approval that would set the closing date if it were the only one required, and what regime it sits
in; the gating regulatory items; and what would have to be true for the view to be wrong.

Where a sector regulator — not U.S. antitrust review — is what will actually set the closing date,
say so in the verdict sentence itself, in language that stands on its own: name the regulator(s) or
regime by name (e.g., "state insurance departments and non-US prudential supervisors," "the FCC,"
"the relevant state public utility commission") and state plainly that this, not antitrust review, is
what will govern the timeline. Never use the words "sector-gated," "antitrust-gated," "dual-gated," or
"gate" in this sentence or anywhere else in the delivered memo — an analyst reading the memo has not
read this module's internal instructions and the label will read as unexplained jargon. A reader who
stops after the first line should know both that the competition analysis came back clean and that
the closing date is being set somewhere else — and exactly where.

**Follow the verdict sentence with the memo's own stated triage decision, as its own short sentence or
two** (see the "Register" note above): this deal is being driven by [the named regime], so this memo
weights its length and research depth accordingly — most of what follows is about that regime, and the
competition analysis is compressed because it isn't where the risk is. On an antitrust-gated deal, say
the mirror version plainly: antitrust review is the critical path here, so that is where this memo's
depth goes. This sentence is what lets a reader who only reads Section A already know how to read the
rest of the memo — which sections to slow down for and which to skim — before they get there.

**Antitrust Risk Matrix** — one row per antitrust-relevant factor, RAG-coded:

| Risk factor | Assessment | Rationale (sourced) |
|---|---|---|
| Horizontal overlap | [RAG] | … |
| Vertical / foreclosure | [RAG] | … |
| Potential competition | [RAG] | … |
| Roll-up / serial-acquisition pattern *(sponsor and hybrid buyers)* | [RAG] | … |
| First-review risk *(will it clear the initial HSR review — no Second Request; a pull-and-refile is noted, not penalised as a Second Request)* | [RAG] | … |
| HSR clearance path | [RAG] | … |
| Foreign merger control | [RAG] | … |
| Remedy / divestiture exposure | [RAG] | … |
| Current enforcement posture / political climate *(gating jurisdiction, dated)* | [RAG] | … |
| **Sector-regulator approval — substance** *(will they approve)* | [RAG] | … |
| **Sector-regulator approval — duration** *(how long, and what sets it)* | [RAG] | … |
| **OVERALL ANTITRUST RISK TO COMPLETION** | **[RAG]** | … |
| **OVERALL TIMING RISK TO COMPLETION** | **[RAG]** | … |

Caption: "Directional assessments per Meteora protocol — no fabricated probability percentages or
HHI figures."

**Substance and duration are separate rows on purpose.** A regulator that will certainly approve and
will certainly take nine months to do it is LOW on one and MODERATE-to-HIGH on the other, and
collapsing them into a single "regulatory" row destroys exactly the distinction a merger-arb reader
is trying to price. Likewise the two OVERALL rows: a deal can carry LOW antitrust risk and material
timing risk simultaneously, and that combination is common enough that the matrix should be able to
express it."

**Ranked watch-list, not just one closing line.** Turn the matrix into a short ordered list —
2 to 5 items, each one sentence — ranking what actually moves the completion-risk read, highest first,
with the "why" attached: "1. [factor] — [one clause of reasoning]." This is the synthesis layer a
reader uses without re-reading the matrix; a single unranked "watch this" sentence loses the
prioritization the matrix itself doesn't carry (a table has no way to say factor 1 matters more than
factor 4).

**Other views.** Whenever a sell-side note, desk comment, ArbJournal note, AlphaSense output or IB chat
is present in the run and its clearance or overlap read differs from this memo's verdict *or* supports
it without giving a mechanism, add a short "Other views" block just before the stress-test: one line per
view giving firm/analyst/date (and trust tier where a tier list is available), its read, the mechanism
it relies on (or "no mechanism given"), and whether the memo agrees, disagrees or moves, with the primary
source that decides it. A view with no mechanism is noted but does not carry weight on its own. If no such
view exists, write "No sell-side or desk view located" in one line. See
`references/calibration-principles.md`, principle 5.

**Verdict stress-test.** End Section A with one line: the single sourced fact that most supports the
verdict, the single sourced fact that most cuts against it, and which the memo weighted more and why.
The first-review row, the timing row and the challenge/remedy rows are three separate reads (see
`references/calibration-principles.md`, principle 3): never let a timing concern lift the challenge
rating, and never let a clean challenge rating hide a real timing problem.

## B. Buyer Classification & Competitive Footprint

**B.0 The companies in plain English** — required, opens Section B. Per `references/plain-language-primer.md`:
what each party does and how it makes money; segments; **Revenue by Segment table** and **Revenue by
Geography table** (Segment or Region | Revenue | % of total; bare dollar figures in millions such as
`$164.1`, no "mm", "M" or "millions" anywhere in the table, header or caption; % column adjacent to the
revenue column, one decimal, sums to 100.0%; source form/note/date and link in the caption); history
and past M&A table (Deal | Date | Price or terms | Source, divestitures included).

**B.4 Bad-actor check** — required, closes Section B. Target first, one direct sentence, then support;
then the same check on the acquirer with the regulator each item bears on. See primer.


State the classification — financial sponsor / strategic / hybrid-consortium — with **entity-level
evidence**: the acquisition vehicle, its ultimate parent, equity-commitment-letter parties, guarantor
identity, each cited to the merger agreement or 8-K. Then the buyer's profile: for a sponsor, firm,
AUM with source and date, current fund, stated investment thesis and how the target fits, platform
vs. add-on characterisation; for a strategic, business lines with segment revenue cited, industry
position, and stated strategic rationale.

**Acquirer Competitive Footprint table.**

*Sponsor / hybrid form* — this is the required, explicitly-titled **Portfolio Company Analysis**:

| Portfolio company | Stake (majority / minority / realized) | Sector & product lines | Verified via | Relevance to target |
|---|---|---|---|---|

Minority stakes are flagged, never dropped — interlocks, information sharing and partial-ownership
theories are live. Past exits appear alongside current holdings: a realized position in the target's
industry is itself evidence of the consolidation pattern. Mark each holding verified (EDGAR / sponsor
disclosure) or reported-only (press / PE database).

*Strategic form:*

| Segment / business line | Revenue (cited) | Disclosed competitors in that line (verbatim, cited) | Relevance to target |
|---|---|---|---|

Then, for every buyer type, the **regulatory history finding**: prior FTC / DOJ / EC / CMA reviews,
second requests, consent decrees, required divestitures, blocked or abandoned deals, and any
behavioural remedy still in force — with what was required, summarised. State this as an explicit
positive or negative finding after targeted search of agency releases and trade press. Silence is
not a finding.

**Acquisition history / roll-up read**: the buyer's acquisitions in this sector over the past 5–10
years with dates and status. Regulators increasingly treat serial small acquisitions as cumulative
concentration even where each individually cleared, so a long add-on chain is a risk factor
independent of this deal's standalone overlap.

## C. Overlap Screen, Market Definition & Concentration

**C.0 Antitrust in baby steps** — required, opens Section C: (1) how the market works, (2) where each
party fits, (3) is there an overlap (yes/no, then table), (4) the overlap explained simply and in
detail if present, (5) market shares by jurisdiction with links, or one sentence stating none exist and
what was tried. Followed by the **Jurisdiction table** (Jurisdiction | Filing required? with test and
figures | Overlap there | Market-share data) covering every regime in E.1. No share is ever estimated.


Restate the threshold framing in one line, then:

**Overlap Screen table:**

| Footprint element | Overlap type | Overlapping target line | Geography | Evidence (cited) |
|---|---|---|---|---|

Overlap type is one of: direct horizontal / vertical-upstream / vertical-downstream /
adjacent-complementary / potential future competition / none. Private portfolio companies without
filings are classified from sponsor descriptions and press, cited, and marked lower-confidence.

**Overlap narrative.** Immediately under the table, one prose paragraph walking each row in turn —
"In [line A], {TARGET} is niche and {ACQUIRER} is largely absent; in [line B]...; the one line where
both genuinely participate is [line D]" — so a reader following the paragraph alone already knows where
the real overlap sits before the market-definition subsection formalizes it. This is prose, not another
table.

**Verbatim Competitor Disclosures table:**

| Company | Filing (form + date) | Competitors as listed — VERBATIM |
|---|---|---|

Never paraphrase. State explicitly where a filing names no competitors. Then cross-reference: which
competitors appear on more than one party's list (common competitors are the clearest evidence of a
shared market), and — the single strongest overlap signal in a strategic deal — **whether each party
names the other**. Assess the likely response of significant non-party competitors.

**Inbound Competitor Disclosures table — who names the parties:**

| Naming company (ticker) | Filing (form + date, accession) | Naming language — VERBATIM |
|---|---|---|

The outbound table above answers "who does this party say it competes with," which returns nothing on
a party whose Competition section names no entities. This table answers the other direction, and on
that party it is the only competitor evidence there is. Two or three rows is the useful size — this
corroborates the overlap screen. Quote the naming sentence exactly; the specific language is the
evidence, and a paraphrase cannot be checked.

Where the inbound screen found nothing, drop the table and write the negative finding with its
denominator instead — "screened N peer filings; none names {PARTY} as a competitor" — so the reader
can tell a search that ran and came back empty from a question nobody asked. Where the two directions
disagree, say so in the cross-reference sentence rather than leaving the reader to notice: a party that
names no one while being named by others is a disclosure-posture finding worth a clause of its own, and
it cuts toward the market being real and narrower than that party's own filing implies. Graph-adjacency
output (`entity-neighbors`) never populates *this* table — it is not a disclosure, and presenting
co-occurrence as a naming would overstate the evidence. It belongs in the Peer Set table below, where
it is labelled for what it is.

**Peer Set & Scale table — REQUIRED on every deal:**

| Peer | Ticker / private (owner) | Named by | Names a party? | Scale (cited) | Relevance to overlap line |
|---|---|---|---|---|---|

This is the section's answer to "who else is in this market, how big are they, and which are
tradeable." It is **required on every deal** — including, and especially, deals where both parties
disclosed healthy competitor lists, because that is precisely the case where a reader assumes the
question has been answered and it has not. The two verbatim tables above are raw disclosure. This one
is the reconciliation, and the reconciliation is where the findings are.

Build it by unioning every source the run already touched: the target's disclosed list, the acquirer's
disclosed list, any inbound namers, the `entity-neighbors` adjacency candidates, and the sizing data
Agent D returned from market-structure work. **Sort by how many independent sources name each peer**,
most-corroborated first — a firm both parties name and a third filer confirms is a different-quality
data point from a single unverified mention, and the sort order should make that visible without the
reader doing the counting.

Column rules:

- **Named by** — which sources name this peer: `TGT 10-K`, `ACQ 10-K`, `both`, an inbound filer's name,
  or `corpus adjacency` for an `entity-neighbors` candidate with no filing behind it. Adjacency rows
  are always labelled as such and never described in prose as one company having named another.
- **Names a party?** — does this peer's own filing name the target or the acquirer? Blank for private
  firms and for adjacency-only rows; this column is what connects the peer set back to the inbound
  table.
- **Scale** — the industry's natural denominator (units, revenue, subscribers, GMV), cited to its
  source with a date. A stated gap is fine and normal; an uncited number is not. Estimates from an
  expert call or a sellside note are labelled as estimates with the source named.
- **Relevance to overlap line** — which of Section C's overlap lines, if any, this peer participates
  in. A peer that competes with neither party in the overlapping line still belongs in the table with
  "None — [line]", because a peer set with only the convenient names in it reads as curated.

**Then state the cross-list finding in a sentence, by name.** Which peers appear on more than one
party's list? Common competitors are the clearest evidence of a shared market that public filings
produce, and the memo must name them explicitly rather than placing two tables near each other and
leaving the reader to diff them — that has been this section's most-missed finding. **Resolve
subsidiary and brand relationships before concluding a name is unique to one list**: a parent named on
one list and its operating subsidiary named on the other are the same market participant, and treating
them as two names understates the overlap. If genuinely no name appears on both lists, say that
explicitly too — it is equally informative and cuts the other way on shared-market evidence.

The scale column then feeds the market-definition subsection below directly. Where that subsection
computes or cites a share, it should reference figures already in this table rather than re-deriving
them inline from a prose sentence or an evidence cell.

**Financial-sponsor buyers: this table's second row is the overlapping portfolio company, never
the fund.** A PE fund does not file a 10-K and does not disclose competitors — that is true of every
sponsor on every deal, so stating it ("KKR's 10-K does not name competitors") is not a finding and
does not belong in this table or its surrounding prose. Instead: for whichever portfolio company(ies)
Section B identified as overlapping, pull *their* competitor disclosure — EDGAR if they file, an S-1
or foreign-registry filing if they don't file domestically, or a dated press/trade-press description
if neither exists (mark that row lower-confidence, cited). If a genuinely overlapping portfolio
company has no disclosure of any kind anywhere, say so as a stated gap in one sentence and move on —
do not fill the row with the sponsor entity as a substitute subject.

**Prior Cooperation / Complementary-Relationship check.** A separate, explicit finding from the
naming check above — has there been any prior joint venture, liquidity-pool/order-flow merger,
index-licensing, data-sharing, or distribution arrangement between the two parties, disclosed or
announced before this deal? State as a positive or negative finding, cited:

| Arrangement | Date & source |
|---|---|

or, if none is found, one sentence saying so and where you looked. A finding here can point the
opposite direction from the competitor-naming check (a target's 10-K can name the acquirer as a
competitor even where the same two firms have jointly operated a liquidity pool) — both findings stand
side by side, neither overwrites the other.

**Geographic Revenue Comparison table** — regional categories standardised across companies:

| Region | Target revenue % (cited) | Buyer-side revenue % (cited) | Combined-presence note |
|---|---|---|---|

Extract verbatim from EDGAR segment tables. State the combined entity's position by geography in
text as well as the table, flag high-concentration regions where the overlap exceeds a screening
threshold, note year-over-year expansion trends, and name which regulatory regimes the combined
footprint implicates. Add customer-type segmentation wherever the filings disclose it.

**Financial-sponsor buyers: "Buyer-side revenue %" means the overlapping portfolio company's
geographic revenue, not a consolidated sponsor-level figure — a fund has no revenue by geography of
its own, and noting that is not a finding. Pull the overlapping portfolio company's geographic
disclosure wherever one exists (EDGAR, foreign filing, dated press description of its footprint); if
none exists because the holding is private with no public geographic breakdown, state that as a gap
against the specific holding, and drop this table (or mark it not constructible) only after that
attempt — never construct it around the sponsor entity as a stand-in.

**Market Structure table — the complete attributed data set:**

| Estimate | Value | Source (firm · publication · date) |
|---|---|---|

Every market-size, share and positioning figure gathered appears here, one per row, attribution in
every row, adjacent-market data labelled as such.

**Market definition and concentration.** Define the relevant product and geographic markets and apply
the hypothetical monopolist test qualitatively. Quantify shares and HHI **only** where both a revenue
figure and a total-market figure are citable. Otherwise choose the right statement and make it
precisely:

- *No shared market* → "Concentration analysis is **inapplicable**: the parties do not participate in
  a common relevant market. No HHI is computed." (Not "unavailable" — that implies incompleteness.)
- *Shared market, no citable data* → first, run one targeted search for the acquirer's or target's
  closest analogous prior transaction in the same or an adjacent product line, since a specialist
  research shop's market-share or HHI table from that comparable deal is frequently the best available
  proxy. If a genuine analog exists, cite it explicitly as a proxy from a different transaction — e.g.
  "no citable market-share data exists for [current overlap line]; the closest sourced analog is
  [firm]'s [year] table for [acquirer]'s prior acquisition of [comparable target], putting [acquirer]'s
  share at X% in the same product line — cited as a proxy, not as data on the current transaction." If
  no analog exists either, fall back to: "Market size and share data for [market] could not be sourced;
  concentration is **not quantified** rather than estimated."

**Narrow-vs-broad sensitivity check.** For any line the overlap narrative flagged as genuine
overlap, do not stop at one market definition. State the narrowly-drawn definition (e.g. "electronic-
only execution in this product"), the more broadly-drawn one (e.g. "all execution channels including
voice/bilateral"), which one the analyst believes is economically correct and why (customer type,
protocol, trade size, or channel differences are the usual drivers), and whether the narrow definition —
if a regulator insisted on it — would change the read. Show the comparison; do not land on the broader
definition silently.

Close with barriers to entry in each affected market, and adjacent markets / substitutes.

## D. Competitive Effects & Remedies

**D.0 HSR merger-guidelines table** — required wherever HSR applies. All 11 guidelines plus sub-row 1a
(HHI above 1,800; formerly 2,500), columns Guideline # | Guideline | Analysis | Triggered? (Yes / No /
Maybe), in the exact wording and rules of `references/plain-language-primer.md`. "Triggered" means the
guideline is engaged on the facts, not that the deal will be blocked; row 1 with no share data reads
"No (not measurable)", never a flat "No".


**Theories of harm table:**

| Theory | Assessment | Basis (cited) |
|---|---|---|
| Horizontal / unilateral effects | [RAG] | … |
| Coordinated effects | [RAG] | … |
| Vertical foreclosure (specify direction) | [RAG] | … |
| Potential competition | [RAG] | … |
| Conglomerate / bundling | [RAG] | … |
| Innovation & dynamic competition | [RAG] | … |
| Buyer power / monopsony | [RAG] | … |
| *Buyer-type-specific theories* | [RAG] | … |

Buyer-type-specific rows come from the branch file — sponsor: roll-up seriality, cross-portfolio
bundling and cross-selling, combined data advantage, minority-stake interlocks, vertical alignment
across the portfolio; strategic: entrenchment / killer acquisition, closeness of competition,
synergy-claim exposure.

**Depth without padding: every row that isn't trivially inapplicable gets 1–3 sentences of its
own reasoning, not just a table cell.** "Do not manufacture depth" (below) means don't pad a clean
overlap gate into pages of speculation — it does not mean compress every theory into a bare RAG cell.
The discipline that avoids both failure modes: for each theory in the table, write a short standalone
paragraph stating *why* the assessment is what it is, even when the answer is "not implicated" —
e.g. "Conglomerate concerns require the combined entity to leverage market power in one product to
extract advantage in an adjacent one. [Buyer]'s footprint has no [adjacency type] to [target]'s
product, so no bundling or tying theory is available." A reader should never have to infer the
reasoning behind a RAG cell from the cell alone. Only theories genuinely foreclosed by the threshold
framing (e.g. vertical foreclosure on a pure market-extension deal with no supply relationship at
all) may be dispatched in a single sentence rather than a full paragraph — say which threshold fact
forecloses it.

**Portfolio-context integration** paragraph — platform vs. add-on, customer overlap and
cross-selling potential, data-combination risk, innovation impact from combined R&D. On a strategic
deal, reframe rather than skip: state how the combination sits against the acquirer's existing
franchise (diversifying vs. concentrating) and why that matters to the effects analysis.

**Divestiture Candidates table** (where overlaps exist):

| Asset / business | Concern it addresses | Feasibility note |
|---|---|---|

Include any pre-announced separation or divestiture plan, stating its regulatory-condition status
exactly — a strategic plan announced alongside the deal is not a remedy commitment, and conflating
the two overstates how much the parties have already conceded.

Where the overlap gate came back clean, this section is a short table plus a paragraph saying so and
why, with section C's overlap table as the evidence. Do not manufacture depth.

## E. Regulatory Architecture, Pathway & Timeline

**On a sector-gated deal this is the section the reader came for. Give it the length.**

**E.0 The buyer's own track record (first timeline anchor).** Before any generic precedent, print the
acquirer's deal history from Agent F (`references/standing-public-record.md`, section 4):

| Buyer's deal | Announced | Closed | Days | Approvals known, with dates | Remedy or condition |
|---|---|---|---|---|---|

Then two sentences: the range in days and the calendar dates it implies for this deal (from
`scripts/deal_clock.py`), and how this target differs from those targets. If the buyer has no comparable history,
say so in one line.

**E.0a Guidance-gap test.** State company guidance as a day count from announcement, next to the buyer's own
range and the precedent average. When guidance runs well beyond both, list the candidate reasons, the evidence for
each, and which is best supported:

| Hypothesis for the gap | Evidence | Verdict |
|---|---|---|

Long guidance is the parties telling you something. The memo should say what.

**E.1 Approvals & gates table:**

| Approval / gate | Risk | Notes (condition vs. covenant, cited) |
|---|---|---|
| Shareholder approval | [RAG] | … |
| HSR Act clearance | [RAG] | … |
| Foreign merger control — **one row per regime actually screened, not one combined row** | [RAG] | … |
| CFIUS / FDI regimes | [RAG] | … |
| Sector regulators — **one row per approval body, not one row for the category** | [RAG] | … |

**The foreign merger control row is a reasoned notifiability conclusion, not a label.** Run each
party's own geographic/segment revenue against `references/foreign-merger-thresholds.md`'s six
jurisdictional screens — EU/EUMR, UK CMA, SAMR (China), ACCC (Australia), Canada's Competition Act,
and the Investment Canada Act (a separate foreign-investment review, not a competition filing, and
always stated on its own line rather than folded into the others) — and give one row per regime that
is actually in play, each stating **notifiable / not notifiable / indeterminate — data gap**, the
specific test or threshold that drove the call, and the cited figures. "Foreign merger control may
apply" without naming a regime and a threshold is exactly what this row must not say; an explicit
"screened against EUMR Article 1 and not notifiable — combined worldwide turnover of $X falls short
of the €5bn Test 1 floor" is a complete row even when the answer is negative. Where the deal has no
plausible non-US revenue footprint at all, a single sentence saying so, with the revenue basis cited,
is a sufficient (and still positive) finding — do not manufacture six empty rows for a purely
domestic deal.

Follow the table with the paragraph that says which rows matter. Where the perimeter is wide, state
plainly where the duration actually sits — a deal with a light domestic layer and a heavy offshore
one is a different animal from its precedents even when the total approval count matches.

**E.2 Approval Clock Build** — required on sector-gated and dual-gated deals; short but still present
on antitrust-gated ones. This is the constructed critical path and it is the analytical core of the
section. Build it per `references/regulatory-clocks.md`:

| Approval body | Statutory clock | What starts the clock | Observed clock, ≤5yr precedents (cited) | Acquirer-specific adjustment | Filing date (est./actual) | Approval date (derived) | Critical path? |
|---|---|---|---|---|---|---|---|

Caption the table with its sourcing and follow it with a paragraph that does four things: **names the
critical path**, **names the second-longest chain** (two competing long poles mean a fatter timing
distribution than one clear binding constraint, and that belongs in Section G), **states the
concurrency and sequencing assumptions explicitly as assumptions**, and **states the timing mitigants
tied to the specific approvals they help** — continuity of an already-approved control person,
management rollover, an applicant with prior filings on record.

Under the table add two rows or lines every time an agreement exists: **Guidance against the outside-date
ladder** (`scripts/deal_clock.py ladder`, stating which extension step the company's own close guidance first fits
within, in days from announcement) and **Reverse fee** (the amount, or "no reverse fee"). Count any business-day
period under the agreement's own Business Day definition with `scripts/deal_clock.py bdays`.

Distinguish the statutory clock from what starts it from what it practically takes, in every row. A
row that reports only the statutory number has reported the number least predictive of the outcome.

**E.2a Named-state build and E.2b Earliest-close floors and tails (v13; required when state health care regimes are
on the perimeter).** Format and rules are in `references/state-healthcare-regimes.md`. E.2a is one row per state:

| State | Regime | Notice or approval | Trigger test | Our data (proxy labelled) | Clock (from complete notice) | Status |
|---|---|---|---|---|---|---|

E.2b is:

| Item | Filed [latest permitted date] | Filed [early date] | Versus base close |
|---|---|---|---|

Follow E.2b with one sentence: are the tails timing risks or completion risks, and how many days inside the outside
date does the longest one end. Add a closing-condition line per state (listed / not listed / list unfiled, never
"unfiled" alone) and any conditional state as a labelled conditional row.

**E.3 Regulatory Architecture table** — the merger agreement walked clause by clause, verbatim where
load-bearing:

| Clause | What it does |
|---|---|
| Efforts standard | … |
| Divestiture obligation & cap construct | … |
| Sponsor / portfolio-company carve-out | … |
| Litigation commitment (through appeal?) | … |
| Remedy-proffer clock (calendar date computed) | … |
| Pull-and-refile rights & caps | … |
| HSR filing deadline (calendar date computed) | … |
| Interim acquisition standstills (**verbatim**; named spaces or generic) | … |
| Antitrust reverse termination fee (amount, % of EV vs. the 3–4% convention, antitrust-specific or generic) | … |
| **Ticking fee — rate, trigger date, which approvals trigger it, accrual end and any cap** | … |
| Outside date & every extension mechanism, or the explicit absence of one | … |

**E.4 Timeline scenarios** — fast / base case / slow, each with a day count and an implied close
date, and each named for the *mechanism* that produces it rather than for its speed. The base case is
the Approval Clock Build's derived date plus a closing tail; it is not the midpoint of the parties'
guidance and it is not the mean of the precedent set.

Two required reconciliations follow the scenario table:

- **Decode the stated guidance.** State the guidance window's day-count range from signing and say
  where the constructed base case lands inside it and why. Guidance is negotiated disclosure set
  against the slowest approval's realistic case — a memo that reports the midpoint has ignored the
  information in the window's width.
- **Reconcile against the ticking fee trigger date**, where one exists. That date is the parties' own
  revealed base case for when the named approvals should have landed, and it is a better anchor than
  the press release's prose. Explain any gap between it and the build.

Then a dated **milestone list**: signing, announcement, go-shop expiry, HSR and sector-filing
deadlines, remedy-proffer date, expected hearing dates where a regulator publishes a calendar,
ticking-fee trigger date, outside date and any extension dates.

## F. Precedents, Sources & Limitations

**Precedent Transactions table:**

| Deal | Year | Buyer type | Overlap profile | Approval bodies | **Why analogous (this approval)** | Regulatory outcome | Procedural friction | **Per-approval days (where sourced)** | Announce→close (days) | Remedy | HSR-regime era |
|---|---|---|---|---|---|---|---|---|---|---|---|

One deal per row, never grouped. Every row states a specific day count and the actual outcome. Drop
any row whose specifics cannot be sourced rather than softening it. Comparable precedents only —
matched on **approval body first and acquirer archetype second** where the deal is sector-gated, on
buyer type and overlap profile where it is antitrust-gated. No contrast rows.

**The "Why analogous" cell is not optional and is not "same industry."** Write the specific reason
tied to the approval being predicted — same supervisor, same threshold, same applicant posture — so a
reader can check the claim. A precedent that cannot say which approval it is a precedent *for* is
decoration; drop it.

**Apply the five-year recency ceiling to sector-approval precedents.** Rows outside the window are
admissible only where no in-window precedent exists for that approval body, and carry an explicit
out-of-window label plus one sentence on what has changed since.

**Per-approval day counts outrank total deal timelines** and should be captured wherever a regulator
publishes filing dates, hearing notices or approval orders — they feed the Approval Clock Build
directly instead of requiring the reader to back them out of an announce-to-close number. Every row flags its HSR-regime era —
pre-February-2021 (ET routinely granted, ~73–81% of requests), February 2021–February 2025 (ET fully
suspended, no grants possible), or post-February-2025 (ET reinstated but granted in only ~29% of
FY2025 requests, per the agencies' own HSR annual report) — because a pre-2021 "ET granted" day count
understates today's floor, and a post-reinstatement grant is real but still the exception rather than
the baseline. The **Procedural friction** column states plainly whether the precedent
required a pull-and-refile, an extended waiting period, or any other friction short of a formal second
request — or "none identified" if a specific search for this turned up nothing. "Cleared without a
second request" and "cleared without a second request, but required a pull-and-refile" read as the
same headline outcome and are not the same regulatory experience; this column is what keeps the
clearance handicap honest about which one actually happened.

**Acquirer's full record and outcome mix** — for a repeat acquirer, a compact table of every deal of the
last ten years that went through HSR (older only if in the same product line): Deal | Year | Overlap type
(direct / adjacent / complementary) | Outcome | Announce→close days | Source. Follow it with one sentence
stating the mix and which overlap type drew any Second Request. The worst single precedent is a row here,
not the verdict.

**Clearance handicap** — a short paragraph reading the precedent set onto this deal, directional
only, naming which precedents drive the read and where this deal differs from them. On a sector-gated
deal this paragraph is a **sanity check on Section E.2's constructed date, not the source of it**:
state whether the build and the precedent set agree, and where they disagree say which one governs
and why. Usually the build governs, because the precedent set rarely matches the perimeter exactly —
say that out loud rather than quietly splitting the difference. Separate explicitly which precedents
are being read for **approval-body comparability** and which (if any) only for **buyer posture**.

**Key monitorables** — the dated list of what resolves each open question: HSR filing and waiting-period
expiry, second-request risk window, go-shop expiry, foreign filings, proxy disclosure of the
background-of-the-merger and regulatory covenants, any agency statement.

**Open Questions — Cross-Model Verification.** Present whenever SKILL.md's "Open questions and the
autonomous deep-dive pass" identifies at least one item; on a run with none, say so in one line rather
than omitting the heading silently — a reader should be able to tell "screened, nothing open" apart from
"not screened." This subsection is written for two audiences at once: the deal team reading the memo,
and, unmodified, a different model (ChatGPT, Gemini, Perplexity) with no memory of this conversation. A
numbered list, one question per entry, each entry self-contained:

N. **[The question, phrased so it stands alone]** — [one to two sentences of the minimum deal context
   needed to attempt it: the entity, the jurisdiction, the specific fact pattern]. This run's working
   answer: [the current view, stated plainly, with its confidence — never withheld to make the question
   look "neutral"; a withheld answer just wastes the second model's first pass reconstructing what this
   run already found]. Why it matters: [what it would move if the answer changed — the base-case date,
   the verdict, a specific number in the Approval Clock Build]. Status: **Open** or **Resolved this
   run** — if resolved by the deep-dive pass, state the answer and what would have to be true to change
   it, rather than dropping the entry once it's answered.

**Materiality-ranked, not just listed — and non-material items are cut, not demoted.** Per
`references/open-questions-deep-dive.md`'s Step 4, order surviving entries highest-materiality first
(would move the base-case date or verdict most), and do not include an item that would not move either
one — that item is dropped from this block entirely rather than kept as a low-priority entry. A memo
that lists every flagged item regardless of consequence trains the reader to skim past the whole block.

Keep each entry short enough to paste whole without trimming — the deep-dive follow-up itself is where
the supporting detail belongs, not here. This block is the required input to `hour-1`'s
Perplexity-council reconciliation step (see that skill's retrieval and reconciliation steps) — write it
assuming a downstream reader will paste it verbatim into another model and needs nothing else to attempt
it.

**Coverage ledger (required).** Print Agent F's ledger from `references/standing-public-record.md`, section 7:
one row per check, with result, status (Found / Not found after search) and source, and the counts beneath. No
row may read "Not searched" in a delivered memo; run the check or move it to Open Questions with the reason.

**Questions for counsel.** Three to six plain questions the public record cannot answer, each tied to the finding
that raised it. Omit the block only when the run raised none, and say so.

**Sources** grouped by channel: EDGAR (form, date, accession), company deal materials (press release,
deck with slide numbers), agency releases, industry/trade sources with dates.

**Limitations** — the explicit data gaps, never estimated around; which day-one documents did not yet
exist; the channel attempt log for anything searched and not found (stated as the failed action that
proves unavailability, not as a null finding); and the protocol note: that `Assessment:` marks
opinion, and that no market shares, HHI figures or point clearance-probabilities appear anywhere in
Sections A–F where source data is absent (Section G's IRR/spread math is the sole, by-design
exception, scoped to that section only) — also note here that the Section A enforcement-posture row
is a dated, time-sensitive read, not a durable fact — say as of what date it was assessed and that it
should be re-checked before this memo is reused weeks or months later.

## G. Entry Price to Target IRR

The one section of this memo where live market pricing and a directional pricing view belong — every
other section stays completion-risk-only, exactly as before. Read `references/entry-price-target-irr.md`
in full and apply it exactly.

**Open with one named, desk-legible headline level — before the table, before the fresh-pricing line's
full detail.** One sentence, in the desk's own quick-math vernacular (raw spread = deal price / current
price − 1, doubled for a rough annualized read), naming the specific price level where the trade starts
clearing the target hurdle on this memo's own base-case timeline. See
`references/entry-price-target-irr.md`'s "Lead with one named level" section for the exact convention
and phrasing. This headline sentence does not replace anything that follows — it is a fast-reader's
answer stated first, with the full derivation immediately after.

Then the fresh live gross-spread line (target current price, deal price, spread $ and %, pull
timestamp — never a spread reused from earlier in the conversation), then:

**Entry Price to Target IRR table**, at exactly three scenarios — this memo's own working close date
(from Section E's timeline scenarios / Section F's clearance handicap) and that date ±30 days, never a
fixed generic day-count set:

| Timeline | Spread % needed | Spread $ needed | Implied entry price |
|---|---|---|---|

Target IRR is **8% by default**, parameterized — recompute at a different rate if the user specifies
one, and state plainly which rate was used.

**The Read — required, not optional, immediately under the table**, doing all four in the same
paragraph or a tightly connected pair of sentences: the dollar entry-price range across the three
scenarios; the duration/discount directional relationship stated explicitly; current pricing's
implied annualized return compared against the target hurdle and what that implies about the market's
read; and a named precedent or risk factor from Section D or F, with a plain statement of whether the
current spread appears to price it in. Register: direct and specific — name a level, don't hedge into
an adjective-only conclusion.

**Where the Read concludes the spread is not attractive against the target hurdle, add the mandatory
topping-bid / appraisal-claim paragraph** — see `references/entry-price-target-irr.md`'s "Mandatory
topping-bid / appraisal-claim discussion" section. Brief, labelled, and required even where both
assessments come back weak — the omission is the failure mode, not a weak answer.

**Spread Pressure and Supply paragraph.** After the Read and any topping-bid paragraph, add a short
labelled block built from `references/spread-pressure-supply.md`: the checks that apply (liquidity, float,
break price, upside against downside, buyer stock and financing wording, short interest, sell-side supply,
tape path, index events), a table of the time-value dollars from `scripts/deal_clock.py decompose` against the
residual, and a one-line verbal call: mostly time value, mostly technical, or mostly deal risk. Name any
single-source or chart-derived number. If no live price was available, the first line of this section says so
and the table is the price-independent hurdle table.

Closing line: *"Meteora Capital — Event-Driven Research. Internal investment research; not
investment, legal, or tax advice. Not for distribution."*
