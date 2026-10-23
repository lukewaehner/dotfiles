# Turn-One Gather — the six fixed agent prompts

Launch **all six in a single tool block**. Substitute `{TARGET}`, `{TICKER}`, `{CIK}`, `{ACQUIRER}`,
`{ACCESSION}`, `{DATE}`. Wall clock for the gather is the slowest single agent, not the sum — so the
only thing that matters is that nothing is left out of the block and nothing is read before the block
is sent.

**Shorthand launch (the required form).** Do not re-emit these prompts at launch; a full-prompt
launch block costs a minute-plus of serial emission for nothing. Each agent's launch prompt is:

> Read `{SKILL_DIR}/references/gather-prompts.md`, section "Agent X". Execute it for {TARGET}
> ({TICKER}, CIK {CIK}), acquirer {ACQUIRER}, merger 8-K accession {ACCESSION}, announced {DATE}.
> The closing instructions in that file's header apply to your return. [Agent A only — append:]
> Ex-2.1 offsets from the TOC pull: covenants article at {X}, conditions/termination at {Y},
> definitions article at {Z}.

**Every prompt ends with the same three instructions** (append verbatim):

> Return AT MOST 2,000 words as a labelled field list — not an essay, not a narrative. ALSO write
> that same bounded summary verbatim to `/home/claude/summary-{TICKER}-<yourslug>.md`, with any
> overflow detail in `/home/claude/notes-{TICKER}-<yourslug>.md`. Exceeding the tool-result limit
> forces a disk spill and a recovery read, which costs more than the detail is worth.
>
> Prefix with `VERIFY: ` any fact that is easy to lose in condensation — proper names, individual
> dollar figures, exact share counts, sub-clause cites, single-source estimates. Write what follows
> as a LITERAL substring exactly as it should appear in the final document — a bare token
> (`$107,500,000`, `Simpson Thacher & Bartlett`), never a descriptive sentence.
>
> Preserve the epistemic status of every claim. If something could not be determined, is not
> disclosed, or is your inference, say so in exactly those terms — never render "could not determine
> either way" as "none reported", "not disclosed" as "none", or "consistent with X" as "X". Report
> any figure you could not source as a stated gap; never substitute an estimate. An explicit
> negative finding after search ("no prior enforcement action identified after searching FTC and DOJ
> releases and trade press") is required wherever you searched and found nothing — silence is not a
> finding.

---

## Agent A — Merger agreement: the regulatory architecture

Read Ex-2.1 to 8-K accession {ACCESSION} for {TARGET} ({TICKER}). Use the offsets supplied at launch
and jump by section-heading anchors ("Efforts", "Regulatory", "Termination", "Outside Date",
"Company Termination Fee", "Conditions"); never read the agreement linearly, and never accept
`edgar-filing-text` at its default char limit — fetch ≤40,000-char windows by offset.

Return:

- **The regulatory efforts covenant quoted clause by clause** — the efforts standard ("reasonable
  best efforts" vs. "hell or high water" vs. anything bespoke); whether the divestiture obligation
  runs one way or both; the cap construct in full (unlimited / materiality standard / a
  disclosure-schedule basket — quote the "except as set forth on Section X of the Parent Disclosure
  Schedule" language if present, and state what the cap is measured against); any sponsor or
  portfolio-company carve-out; the litigation commitment and whether it extends through appeal to
  final non-appealable judgment; the **remedy-proffer clock with the calendar date computed**;
  pull-and-refile rights and any cap on them; the **HSR filing deadline with the calendar date
  computed** from the covenant.
- **Interim acquisition standstills, VERBATIM** — any covenant barring either party from acquiring
  or investing in named product/service spaces during pendency. State whether specific spaces are
  named or the language is generic. If specific, list the named spaces exactly: this is the parties'
  own market-definition evidence and it is the highest-value single extract in this agent's brief.
- **Closing conditions** — the complete list, split mutual / buyer / seller, stating explicitly which
  antitrust and foreign regimes *condition the close* and which appear only as covenants.
- **Both termination fees** with exact trigger mechanics, and — stated explicitly — **whether the
  reverse fee is antitrust-specific or a generic breach/financing fee**. Give the amount and, if the
  announced equity or enterprise value is available to you, the fee as a % of it. Include sole-remedy
  and liquidated-damages language, and specific-performance conditionality.
- **Outside date** — the initial date, who may extend, the increment, the maximum date, and the
  condition on extension (typically: only regulatory conditions unsatisfied). Verify in the
  termination article; never assume. State explicitly if there is no extension mechanism.
- **Ticking fee, if any — the four extractions, in this order.** (1) The **trigger date**: the date
  after which consideration begins to accrue. This is the parties' own revealed base case for when
  the named approvals should have landed and is the single most informative timing datum in the
  agreement — better than the press release's prose guidance. (2) **Which approvals trigger it** — a
  fee triggered by specifically named sector approvals is the parties confirming the critical path.
  (3) The **accrual rate** and its compounding/payment convention. (4) The **accrual end date and any
  cap**. Quote the operative clause. If there is no ticking fee, say so — its absence on a long-dated
  deal is itself a finding.
- Go-shop existence and exact end timestamp (one line — it dates a monitorable, nothing more here).
- **Filing deadlines for EVERY approval named in the conditions, not only HSR** — sector-regulator
  applications, foreign change-of-control notifications and any pre-acquisition competition filings
  each typically carry their own covenant deadline (commonly 20–40 business days from signing).
  Compute the calendar date for each; these are the filing-date column of Section E.2's Approval
  Clock Build, and without them the build starts from an assumption instead of a covenant.
- Advisors on both sides, financial and legal, from the notice provisions or the press release. Note
  if a top-tier antitrust firm sits on the acquirer's side — **and note equally whether dedicated
  sector-regulatory counsel appears on both sides while no antitrust specialist does**, which is one
  of the three tells for a sector-gated deal.

## Agent B — Competition sections and geographic revenue (verbatim EDGAR)

For {TARGET} ({TICKER}, CIK {CIK}) — and, **if the acquirer is a strategic (an operating company
that files with the SEC), for the acquirer as well** — pull the latest 10-K and 10-Q. Use
`MeteoraMCP-AWS:extract-10k` first: it returns the Competition section and the segment/geographic
tables directly, verbatim from the filing, which is exactly what is needed. Fall back to
`edgar-filing-text` by offset only for what the extractor misses.

**If the acquirer is a financial sponsor (or hybrid), do not stop at "no acquirer 10-K exists."**
The fund itself has nothing to extract, but that is not the end of this agent's brief — once Agent
C (below) identifies which portfolio company(ies) overlap with {TARGET}, pull whatever EDGAR, S-1,
foreign-registry, or press-sourced competitor and geographic disclosure exists for **those specific
portfolio companies** and run this same extraction against them. Before writing a privately held
portfolio company's disclosure as a stated gap, run the **P3 pull** in `references/vector-db-
retrieval.md` — a sellside/IOC-note search naming the portfolio company's (or {TARGET}'s) actual
competitors, which frequently exists even when no EDGAR filing does. Only after that attempt comes
up empty is it a stated gap ("no public Competition-section or geographic disclosure located for
\[portfolio co.\], and no sellside coverage identified naming its competitors") — it is not a reason
to substitute the sponsor entity as the subject of this section.

Return, per company:

- **The Competition section VERBATIM**, with the form type, filing date and accession. State
  explicitly whether any competitor is named, and if the filing describes competition without naming
  anyone, say that in those words. Do not paraphrase or condense the competitor list — it is
  reproduced or quoted, never summarised.
- **The geographic revenue table reproduced exactly** as filed, for the last two fiscal years, with
  the filing's own regional category labels preserved (standardisation happens later, in the memo;
  the extract stays faithful).
- **Segment descriptions and revenue by segment** for the last two fiscal years, plus any
  customer-type revenue segmentation the filings disclose.
- Product and service line descriptions in enough detail to screen for overlap against the other
  party — the business description, not the financials.
- Any disclosed customer or supplier concentration, and any named supply or distribution agreement
  with the other party (a pre-existing vertical link makes foreclosure concrete rather than
  hypothetical).
- **Both parties' revenue-by-segment and revenue-by-geography tables as filed, for the most recent fiscal year, with the filing's own labels and the note number.** For a 40-F/20-F filer use the AIF and the financial-statement exhibit (extract-10k does not parse 40-F); a filing that does not split U.S. from other North America is reported as filed, never split by you.
- **The mutual-listing check**: state directly whether {TARGET} appears in {ACQUIRER}'s competitor
  list or vice versa, with the citation. If yes, flag it — and then test it rather than treating it as proof. Return the four
  calibration tests for every named pair (management's own words on the party's earnings calls and at
  conferences, quoted with the call date; substitute vs. complement; same customer and purchase
  decision; direction of the naming). A named competitor is a candidate overlap; it becomes a finding
  only when the tests support it (see `references/calibration-principles.md`, principle 1).
- **Corroborate with the P3 pull even when EDGAR disclosure exists.** A 10-K Competition section is
  often generic ("we compete with numerous companies in our industry") where a covering sellside
  analyst names names and product-line detail. Run P3 (`references/vector-db-retrieval.md`) for both
  parties as a supplementary source; where it names a competitor the EDGAR text didn't, add it with
  its own citation rather than folding it silently into the EDGAR-sourced list.
- **The graph-adjacency call — every deal, both parties.** In the same batch as your EDGAR calls, run
  `MeteoraMCP-AWS:entity-neighbors` once per party — the ticker or company name, `hops=1`,
  `rel_types=["CO_MENTIONED_WITH","MENTIONS","IN_INDUSTRY","IN_SECTOR"]`. It reads no filings, so it
  adds no time. Return the adjacent names as **peer-set candidates, explicitly labelled as corpus
  co-occurrence** — they populate the Peer Set table's candidate rows, and they are never reported as
  one company having "named" another.
- **The inbound EDGAR leg — every deal, up to three peer filings.** This runs regardless of what the
  outbound check returned. A party whose Competition section names nobody needs it because there is no
  other evidence; a party with a healthy disclosed list still needs it because a list is not a
  reconciled peer set. Take the **three** most plausible public peers — from the `entity-neighbors`
  result, from either party's own disclosed list, from the sector, or from the market-structure work —
  pull each one's most recent 10-K Competition section, and check whether either party appears in it.
  Three is a hard cap and an early stop is fine; batch all three in one call block rather than walking
  them sequentially. Return, for each hit: the naming company, form type + filing date + accession, and
  **the naming sentence quoted verbatim** — never paraphrased, since the exact language is the evidence.
  Return the misses too, as a count ("screened N peer filings, none names {PARTY}"), because a negative
  result from a search that actually ran is a finding and an unexamined silence is not. Do not follow
  the named competitors into their own competitors — that is a network map, it costs minutes, and it is
  `hour-1`'s job, not this one's.
- **Peer-set assembly data, returned as structured rows rather than prose.** The compose step needs to
  build a Peer Set & Scale table, so hand it the raw material in that shape. For every distinct
  competitor name surfaced by any route above, return: the name as filed, which source(s) named it,
  whether it is public (resolve the ticker — one `WebSearch` per unknown name is acceptable here) or
  private (name the owner if disclosed), and any parent/subsidiary or brand relationship that would
  make two differently-spelled names the same market participant. **Flag explicitly every name that
  appears on more than one party's list** — that cross-list overlap is the strongest shared-market
  evidence public filings produce and it is the item most often lost between gather and compose.

## Agent C — Buyer footprint, portfolio map and antitrust history

Classify and map the buyer side for {ACQUIRER} acquiring {TARGET}.

**If {ACQUIRER} turns out to be a financial sponsor: the deliverable of this entire agent is the
portfolio, not the fund.** Everything below the classification bullet is written with the specific
portfolio company as the grammatical subject — "Precipart manufactures X" and "Precipart's stake is
majority, verified via…", never "{ACQUIRER} manufactures X" or "{ACQUIRER} has no overlap." The fund
name appears only in the classification bullet, the firm-profile bullet (AUM/fund/thesis), and the
fund's own prior antitrust/HSR-filing history — those three are genuinely about the fund; everything
else is about a named holding.

**And enumerate the full portfolio, not just the overlap candidates.** Pull the sponsor's complete
portfolio-page listing (every current holding, not a curated subset) and run every single one through
the overlap classification, including the ones that come back "No." A table with 30 holdings marked
mostly "No overlap — \[different sector\]" and two marked "Overlap — \[line\]" is the auditable,
credible version of this section; a table with only the handful of holdings that seemed relevant from
a web search is not verifiably complete and reads as cherry-picked even when it isn't.

Return:

- The acquisition vehicle's ultimate parent and controlling owner, with **entity-level evidence**
  (vehicle names from the merger agreement, equity-commitment-letter parties, guarantor identity),
  each cited. Then the **buyer classification** — financial sponsor / strategic / hybrid-consortium
  — and the specific evidence that establishes it.
- **If a sponsor (or hybrid): the complete portfolio-company map against the target's business
  lines**, pulled from the sponsor's own portfolio page in full, cross-checked against every current
  holding — not only the ones that look relevant on first read. Enumerate current holdings, majority
  AND minority, plus **past exits** in the target's
  sector — a realized position in the industry is itself evidence of the consolidation pattern.
  Sources in order of reliability: portfolio-company EDGAR filings (13D/G, S-1s naming the sponsor,
  proxy ownership tables), the sponsor's own portfolio page, 13F where applicable, then reputable
  press and PE-database coverage via web search. Mark each holding verified (EDGAR / sponsor
  disclosure) or reported-only (press), note the stake type, and **flag every minority stake
  explicitly** — interlock and partial-ownership theories are live and a dropped minority stake is a
  missed overlap. Also return the sponsor profile: firm, AUM with source and date, current fund, the
  stated investment thesis, and whether the target is a new platform or an add-on to an existing one
  (add-ons in the same market are the highest-scrutiny configuration).
- **The acquirer archetype, for timing rather than overlap** — classify against the archetype table
  in SKILL.md ("Acquirer archetype as a timing input") and return the evidence: has this buyer ever
  been an approved control person of a regulated entity of this type, in this jurisdiction or any
  other? Does it hold a comparable licensed asset today? Is the ownership chain simple or
  multi-tier/offshore? On a sector-gated deal this is a more important return than the portfolio map,
  because a change-of-control review assesses the applicant, not its other holdings.
- **Continuity of control persons** — does any existing controlling shareholder, founder or manager
  roll equity or remain in place post-close? Name them and state whether they are already an approved
  control person of the regulated entities. This is the most underweighted timing mitigant in a
  sector-gated deal and it is frequently disclosed in the announcement press release and nowhere
  else.
- **If a strategic: the acquirer's segments and business lines** with revenue cited, its industry
  position, and its full acquisition history in this sector over the past 5–10 years with dates and
  status. Serial acquisitions of nascent competitors invite killer-acquisition scrutiny.
- **Prior antitrust history for both entities** — FTC / DOJ / EC / CMA reviews, second requests,
  consent decrees, required divestitures, blocked or abandoned deals, and any behavioural remedy
  still in force, **with what was required summarised**. Search agency press releases and trade
  press directly. Return this as an **explicit positive or negative finding**; a buyer operating
  under a live consent decree faces a materially different review than a first-timer, and "nothing
  found" only means something if you say where you looked.
- **History and deal table for both parties** — founding, listing, every acquisition and divestiture with date and price (Deal | Date | Price | Source), marking any row sourced only to an encyclopedia page or trade press. Where sources conflict (for example headquarters), report both and state that the company's latest filing controls.
- **Conduct check for both parties (B.4)**: legal-proceedings sentences quoted verbatim; material weaknesses, revisions vs. restatements, auditor changes with amounts; short-seller reports, class actions, FCC/FTC/SEC/state-AG actions, data breaches — each an explicit positive or negative finding naming where you searched — and for each acquirer-side item, which regulator or approval it bears on.
- Roll-up seriality count: the number of acquisitions the buyer side has made in this sector over
  the past 5–10 years, with the list.

## Agent D — Precedents, market structure, the parties' own materials, prior cooperation & enforcement
posture

Five tasks for the {TARGET} / {ACQUIRER} deal.

**Precedents.** Query the vector database by deal *shape*, never by party name — the deal is days old
and cannot be indexed, so party-name queries return ticker-string collisions that look like hits.
Run the **P1 pull** in `references/vector-db-retrieval.md` first — read that file in full before this
step and apply its filter exactly (`namespace='default'`, `document_type: "Merger Arb Analysis"`,
filtered by GICS **`sector`, never `industry`**, gated on `actual_completion_date != ""`), with
structure-matched semantic queries ("HSR-only all-cash take-private", "sponsor add-on with horizontal
overlap second request", "vertical foreclosure consent decree"). This is a structured lookup, not a
research task — `hsr_outcome` and `deal_timeline_days` on the returned chunks are usually a complete,
citable answer by themselves. Supplement with web search on FTC/DOJ release archives only for
precedents the pull doesn't surface. Return only precedents carrying a **specific announce→close day
count and an actual outcome**; drop anything you cannot source that precisely, and never list a still-
pending deal as a precedent. **For every row, state the HSR-regime era** — there are three: early
termination was routinely granted pre-February-2021 (~73–81% of requests, per the agencies' own HSR
annual reports); fully suspended February 2021–February 2025 (no grants possible in this window,
regardless of the row's day count); and reinstated since February 2025, but running at a low ~29%
FY2025 grant rate — real and citable, but still the exception rather than the norm. A pre-2021 "ET
granted" day count understates the modern floor either way; verify the current grant-rate trend live
rather than assuming ~29% still holds by the time this runs.
**Where state health care regimes are on the perimeter, also tag each row with the state-regime era and give days
from announcement and days from filing.** A deal announced before a state's transaction law took effect did not
face that review, so a comp set that predates the regimes now in scope is a floor on duration, not a central
estimate. Fetch each state's effective date (it is not carried in the skill) and tag the row "before [state]
regime" or "after". See `references/state-healthcare-regimes.md`.
**For every row, also search specifically for procedural friction** — pull-and-refile, withdraw-and-
refile, or an extended waiting period — as its own query, not folded into the outcome search; state
the finding or "none identified after search" for each precedent. A deal that "cleared without a
second request" but needed a pull-and-refile is a different, more cautious data point than a bare
clean clearance, and both matter to the timeline read. Prioritise the acquirer's or sponsor's own
prior acquisitions in this industry, then same-industry deals by any buyer, then same-shape deals in
adjacent industries clearly labelled as adjacent. If the P1 pull returns nothing analogous after a
real attempt with the sector filter, say so as a stated gap naming the filter run, then fall back to
web search — do not silently skip straight to web search without noting the vector pull came up
empty.

**If market-structure data below comes back with a genuine gap** — no citable market-size, share, or
HHI figure for the actual overlap line — run one additional targeted search (vector database plus web)
for the acquirer's or target's closest analogous prior transaction in the same or an adjacent product
line before returning the gap as final. A specialist shop's HHI or share table from that comparable
deal is often the best available proxy. Return it explicitly labelled as a proxy from a named,
different transaction with its own date — never merge it into this deal's own figures.

**Market structure.** Total addressable market size and participant count from a citable industry
source with date; revenue for target, acquirer and the named peer set; any published share or
concentration figures. Label every figure as an estimate with its source and date. Where a figure is
paywalled or simply does not exist publicly, **say so explicitly as a stated gap — never substitute
an estimate.** This is the input that decides whether the memo can quantify shares at all, so the
honesty of the gap statement matters more than its length.

**Return per-peer sizing figures individually, not only as an aggregate market number.** Section C's
Peer Set & Scale table has a per-peer scale column, and the industry's natural denominator — units
sold, revenue, subscribers, GMV — is frequently available per participant in an expert-call transcript
or a sellside note even where no published share table exists. A return that gives only "total market
~X units" forces the compose step to strand the per-participant detail in prose; a return that gives
the per-peer breakdown with each figure's source lets it land in the table where the market-definition
analysis can point at it.

**The parties' own materials.** Fetch the acquirer's IR-site press release and any investor deck
(also filed as 8-K Ex-99.x — furnished deck exhibits under Item 7.01 are where the substance sits,
do not skip them); check the target's IR mirror. Return: the stated strategic rationale; **synergy
figures and precisely how they are framed** — synergies built on capacity rationalisation, plant
consolidation or pricing / go-to-market overlap are admissions of horizontal proximity, so quote the
framing, not just the number; **any self-drawn combined market position, share, rank or "#1/#2 in X"
claim, quoted verbatim with its slide number** — a company mapping its own pro-forma share is among
the strongest overlap evidence available; the stated expected close and the approvals list as the
parties describe it; and any pre-announced divestiture, carve-out or separation commitment, with its
regulatory-condition status stated exactly (a strategic plan is not a remedy commitment).

**Make one attempt at the deck.** Sponsor and take-private deals frequently publish none; record its
absence as a data limitation rather than spending further calls hunting it.

**Search once for how the TARGET's own management names its direct competitors and describes the
acquirer** — the target's most recent earnings-call transcript and conference remarks (a search such as
`"[Target] earnings call" competitor OR "direct competitor" OR partner [acquirer]`). Return the quoted
language with the call or conference date, or state plainly that none was found. A 10-K Competition
section is drafted by counsel to be broad; management's live description of who takes its customers is
often narrower and is the better evidence of real overlap.

**Return the acquirer's full HSR-reviewed deal record for the last ten years** (older only if in the
same product line), each row with overlap type, outcome, and announce→close days, so the memo can show
the outcome mix rather than lean on one precedent.

**If the acquirer holds a same-day or same-week earnings or investor call, search once for sell-side
coverage of that call specifically** — `"[Acquirer] earnings call" [target] antitrust OR synergies OR
overlap` or equivalent phrasing — separately from the deal press release and deck. Management
routinely says more live than either party puts in writing: whether a known conduct-investigation or
antitrust overhang was directly addressed and priced into the offer, the actual composition of any
headline synergy figure (commercial vs. cost, and specifically whether any portion is capacity
rationalisation or plant consolidation — a horizontal-proximity admission the press release may not
contain), or a plain-English description of the overlap in the acquirer's own words. Return this
verbatim where found, attributed to the specific call and the sell-side note covering it; state plainly
if no such call occurred or no coverage was found.

**Prior cooperation / complementary-relationship check.** Search press releases, prior 8-Ks, and
trade press for any joint venture, liquidity-pool or order-flow merger, index-licensing, data-sharing,
or distribution arrangement between {TARGET} and {ACQUIRER} that predates this deal — this is a
different question from whether they name each other as competitors in a 10-K, and the answer can point
the opposite direction (two firms can be disclosed competitors on paper while having jointly operated a
liquidity pool in practice). **If {ACQUIRER} is a financial sponsor, the search target is any
arrangement between {TARGET} and any of {ACQUIRER}'s portfolio companies — the sponsor entity itself is
the unlikely party to a commercial JV or supply deal, so phrase and run the search that way (portfolio
company first, sponsor named only as the umbrella), not as "{ACQUIRER} (or its portfolio companies)."**
Return as an explicit positive or negative finding: name the arrangement, the specific portfolio company
party to it, its date, and its source, or state plainly that none was found after searching press
releases, {TARGET}'s prior 8-Ks, and the relevant portfolio companies' own disclosures.

**Current enforcement posture.** Identify the lead antitrust regulator(s) implicated by this deal
(e.g. US DOJ/FTC, UK CMA, EC) and run the **P5 pull** in `references/vector-db-retrieval.md` first —
ArbJournal maintains standing, dated rosters of every open matter under a given agency (deal_id 12254
for US DOJ/FTC second requests, plus the CFIUS/EC/CMA rosters listed in that file); read the returned
chunk's `entry_timestamp` and cite it as the as-of date. Supplement with web search for the clearest
available additional public signal of that agency's current merger-enforcement posture under its
current leadership — recent public statements or speeches by agency leadership, and/or the observable
pattern of recent clearances versus challenges in comparable matters. Date the finding explicitly (the
posture read is only as good as its as-of date) and flag it as time-sensitive. This is a directional
political/regulatory-climate read, not a case-specific prediction —
say so plainly rather than overstating its precision.

## Agent E — Regulatory pathway: the clock research behind Section E's Approval Clock Build

**Read `{SKILL_DIR}/references/regulatory-clocks.md` in full before starting.** It gives you the
structural mechanics for the common regimes so that your job is verifying specific numbers rather
than discovering that mechanisms exist. Your output is the raw material for Section E.2's Approval
Clock Build, and it is the reason a sector-gated memo can forecast a closing date instead of
extrapolating one.

**Step 1 — enumerate the approval perimeter, entity by entity.** From the target's latest 10-K/20-F
"Regulation" section and its subsidiary list, identify every regulated entity and, for each, the
supervisor whose approval or notification a change of control requires. Be precise about four
distinctions that routinely produce wrong perimeters in both directions:

- **Domiciliary vs. licensed-only.** Approval usually runs to the entity's domiciliary regulator, not
  to every jurisdiction it does business in.
- **Subsidiary vs. branch vs. appointed representative.** Overseas branches commonly require no
  pre-approval — the home-state procedure applies and the branch notifies afterward. Same for
  appointed representatives, where the principal notifies.
- **Approval vs. notification.** Some regimes require prior consent; some require notice without
  unreasonable delay. Only the first sits on the critical path. Say which each is.
- **Captive vs. traditional carrier, for any US-domiciled insurance entity.** Check the state's own
  captive insurance act before defaulting a licensed insurer to the general Form A entry — many states
  carve captives out of the general Insurance Holding Company System Act entirely and run change of
  control through a separate, often unclocked, discretionary-approval rule instead. Read
  `references/regulatory-clocks.md`'s captive entry; if the entity's state isn't built out there, that
  gap is itself exactly the kind of item SKILL.md's "Open questions and the autonomous deep-dive pass"
  is for — flag it rather than silently applying the general regime.
- **Read the full "Regulation" section verbatim, not just the sentence tied to the deal's primary
  sector.** A target's own 10-K routinely names ancillary regulator relationships in the same section
  as the primary-sector language — FINRA broker-dealer membership, an SEC-registered investment
  adviser subsidiary, a named foreign operating footprint (a country, a regulator) — that have nothing
  to do with the deal's headline story but are independently triggered by a change of control. This is
  a primary source that predates the deal by months, so every regulator or registration category it
  names gets enumerated and handed to Step 2 for clocking here, on day one — not left for a broker
  note or a second reading to surface later. See `references/regulatory-clocks.md`'s "Financial-
  services ancillary regimes" entry for the common categories and how to clock each one.

Return the perimeter as a list, and state affirmatively where an entity you might expect to need
approval does **not**.

**Where the perimeter is a state-by-state licensing or change-of-control regime — money transmitter
licenses, state lending licenses, state insurance producer licenses, or any similar multi-state
consent-based regime — enumerate it at the state level, not as an aggregate count.** "Licensed in 46
states" is not an actionable finding for the reader; it tells them nothing about which specific states
could slow or block the deal. Return, for this kind of perimeter:

- **The specific states involved**, named individually — pull the actual list from the entity's own
  licensing disclosure (a 10-K exhibit, a company licensing page, an NMLS registry extract), not a
  restated aggregate figure from a press release or a prior filing that may be stale.
- **The consent type required in each state or state-cluster** — prior written consent, notice-only,
  a deemed-approval-after-N-days mechanism, or no requirement at all for that entity type in that
  state. States vary on this by design; do not assume a uniform national standard.
- **A speed tier per state or state-cluster** — fast / moderate / slow, based on that state regulator's
  observed practical timeline (from the P1/P6 vector pulls per `references/vector-db-retrieval.md`,
  or from precedent deals' own state-by-state disclosures where available). Group states into clusters
  where the evidence supports it rather than forcing a tier call on every single state individually.
- **A named "must-have" list** — the specific states, if any, where precedent or the entity's own
  revenue disclosure suggests a slow or contested approval is more likely (a state whose regulator has
  suspended or delayed a comparable change-of-control approval before, or a state that represents an
  outsized share of the entity's licensed revenue and would materially change the deal's economics if
  excluded). Name them, don't gesture at "certain large states."
- **Whether an NMLS (Nationwide Multistate Licensing System) register lookup was actually performed**
  to verify current license status for the entity in question, or whether the state list is sourced
  only from the entity's own disclosure. State which one happened — a verified NMLS status and a
  restated company disclosure are different confidence levels and the memo should say which is which.

This granularity requirement feeds Section A's regulatory-perimeter check and Section E's Approval
Clock Build directly — see `references/gate-led-structure.md` for how it changes the memo's structure
when this kind of regime turns out to be the gating item.

**Step 1b — threshold-triggered perimeter (state health care transaction laws, certificate of need and similar).**
Some regimes are triggered by revenue, asset or in-state presence thresholds, not by a licence the target holds,
so the target's 10-K "Regulation" section does not list them. When the target provides health care services in
more than one state (pharmacies, infusion or clinic sites, home health), run this step in addition to Step 1.
Read `references/state-healthcare-regimes.md` in full first. Return:

- **A named-state table**: state, regime, notice or approval or review, trigger test, our data (and say where a
  site count is only a proxy), clock from a complete notice, status (Applies / Likely / Probable / Possible —
  verify / Notice only / Not a transaction gate), and the check date of each statute read.
- **The test at the right level.** Test the target, the acquirer's ultimate parent, and any sponsor or affiliates
  the statute counts. Revenue by state is rarely disclosed; if it is not, say so, use location counts as a
  labelled proxy, and say what would replace the proxy.
- **The target's own history.** Search the agencies' public notice pages (Oregon Health Authority, Massachusetts
  Health Policy Commission, California OHCA, and any other state in scope) for the target's and acquirer's earlier
  notices, and read the target's and acquirer's earlier merger proxies for a "State Regulatory Approvals"
  paragraph. Quote it, and say if it only says "certain states".
- **Closing-condition status** for each state separately from statutory status: listed in the agreement or its
  disclosure letter (cite), not listed, or list unfiled. **"List unfiled" may never be the whole answer.** It is
  allowed only beside a derived perimeter and a watch list of agency pages and filings.
- **Floors and tails** from the filing date (`scripts/deal_clock.py adddays`), at the agreement's latest permitted
  filing date and an early date. Run any conditional lead-time rule down and say which fact decides it.
- **The licensure layer** (pharmacy and home infusion change of ownership): the states where the target holds
  licences, tiered fast / moderate / slow from the P1 and P6 pulls and precedent, with the same
  approval-versus-notification distinction as Step 1.

**Step 2 — for each approval body, return the five fields.** Statutory clock; what starts it
(submission vs. acknowledgement vs. determination of completeness); interruption or deficiency
mechanics and who controls them; observed practical range from recent comparable reviews; and the
specific acquirer attributes that lengthen it. Sources, in order: the regulator's own procedural
guidance (filing instructions, completeness checklists, approach documents, transaction
instructions); **law-firm client alerts and white papers on review duration for that regime**, which
are the only public sources that state practical ranges honestly because they are written for clients
who need the real number; standard-setting or supervisory work-stream materials where the acquirer's
archetype triggers them; and the regulator's published hearing calendars and approval orders.

**Step 3 — pull per-approval day counts from precedent reviews.** Where a regulator publishes filing
notices, hearing calendars or approval orders, extract real day counts for two or three recent
comparable applicants. **One well-sourced per-regulator day count is worth more than five
announce-to-close totals**, because it feeds the build directly rather than requiring someone to back
it out. Note the applicant archetype for each — a strategic's Form A and a first-time sponsor's Form
A are different data points and should not be averaged together.

**Step 4 — sequencing.** For each approval, state whether it can run concurrently with the others or
must follow something (another regulator's decision, antitrust clearance, a shareholder vote). Where
a two-step process exists — a supervisor reviewing and recommending, then a minister or board
approving — say so and treat the steps as sequential unless a source says otherwise. **Flag
explicitly which of your sequencing statements are sourced and which are your assumption**, because
sequencing error is the largest single source of error in a constructed timeline.

**Step 5 — the archetype overlay.** Given the acquirer profile Agent C returns, state for each
critical-path body whether this applicant type draws additional scrutiny, what form it takes, and
whether it is typically resolved through negotiated commitments rather than refusal. Where
commitments are the mechanism, say so plainly — negotiating them is calendar, and it is the reason a
first-time regulated-entity owner's review runs long even when nobody objects to the deal.

Run the **P6 Chain Bridge Research pull** in `references/vector-db-retrieval.md` first for each
critical-path body, then supplement with the web sources above. Report the P6 result explicitly,
including when it comes up empty.

**If the deal turns out to be antitrust-gated, your return will be short — that is the correct
outcome, not a failed brief.** Return the perimeter, confirm the sector approvals are
notification-only or ministerial, and say so in one paragraph. What you must not do is guess at
clocks you could not source: an unsourced row stated as unsourced, with the assumption made explicit,
is far more useful than a confident number nobody can check.

---

## Agent F — Standing public record: what was knowable before the announcement

Read `{SKILL_DIR}/references/standing-public-record.md` in full, then execute it for {TARGET} ({TICKER}),
acquirer {ACQUIRER}, announced {DATE}. Agents A to E read the merger agreement and the parties' SEC filings.
Your brief is everything else that was public before {DATE}, worked from that file's fixed checklist and not
from open-ended search.

Return, in this order:

- **Library.** The distinct Drive documents tagged to either party and dated in the 12 months before {DATE}
  (source, type, date), each marked read, sampled (for what) or not read (why), with any finding that bears on
  an approval, a customer overlap or a government exposure quoted in a line.
- **Sector trigger packs.** Name the packs you selected and why. Then one row per check: result, status, source.
- **Rival mirror.** The target's top two or three named competitors: owner and country, whether each holds the
  same authorization or licence, and the structure it uses.
- **Acquirer profile.** The track-record table with day counts from `scripts/deal_clock.py`, the range applied
  to this deal as calendar dates, existing regulated subsidiaries (the company's own words, dated), revenue by
  region, footprint in countries of concern, and any other deal in flight. Check the project for an existing
  `Acquirer Profile - {ACQUIRER}` file first and update it instead of rebuilding.
- **Regulator state.** Per likely reviewing agency: any pending rule or draft guideline (document, date, status),
  and the outcome of the nearest comparable deals in the last 12 months. Write "not found after search" where a
  search for a blocked or abandoned comparable turned up nothing.
- **Prior strategic interest** in the target in the last three years.
- **The coverage ledger**, one row per check, with the three counts.
- **Three to six questions for counsel**, each tied to the finding that raised it.

Do not estimate a revenue share, a clearance level or a contract value. A registry you could not read is
"not searched: [reason]", never a guess. A figure read from a third-party aggregator is flagged
"aggregator, single source".
