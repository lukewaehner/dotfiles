# Deal Risk Assessment — Report Template

Use this exact section order. Sections marked (conditional) may collapse to a short paragraph when the Phase 3 gate finds no overlaps. Every table listed under a section is required unless its gate condition fails. Label analytical opinion with "Assessment:" so it is never confused with sourced fact.

## Document format (when producing a .docx)

The docx deliverable is a **skimmable, no-omission** version of the same content. Skimmable is a formatting property, not a length property: restructure, never abridge. Structure:

- **Verdict callout box first** (shaded, left accent bar): the completion verdict in one sentence, the compensated-tail summary, and the single most decisive current economic fact. A reader who stops here has the answer.
- **Executive summary**: ~6 bullets, each opening with a bolded label ("The deal:", "Where it stands:", "What to watch:"), each carrying its citations inline.
- **Every section opens with a bold one-line takeaway** before any detail. Prose paragraphs stay short; anything with three or more parallel facts goes into a table.
- **All detail lives in tables** — the ten required tables below plus: a clause-by-clause regulatory-architecture table (Section 1), a milestone/status table (Section 1), and the complete attributed market-data table (Section 4). Dark header rows, zebra striping, bold for the decisive rows, red/green only for outcome words (BLOCKED/CLEARED). **Every table carries its source — in the caption or a per-row source column.** The cite-every-fact discipline is not satisfied by a citation buried in the surrounding prose; a reader auditing a table's numbers should find the source on the table itself rather than hunt the body for it.
- **Two more callout boxes**: the blind view (Section 7) and the tape reconciliation (Section 8).
- **Sources appendix in small type**, grouped by channel (EDGAR / company deal materials / sell-side / web / market data), with accession numbers and the unaffected-window closes. Company deal materials = the press release and investor deck (cite the 8-K exhibit or the IR-site URL, and slide numbers for deck-sourced facts). Under sell-side, tag each attributed note by its source channel — Outlook, uploaded deal-folder research (with the file name), or Vector Database (cited from hit metadata: report title, institution, analysts, publication date) — so provenance is auditable.
- **Integrity note** at the end: what the blind wall did and did not cover in this run, and that "Assessment:" marks opinion.
- Verification: render to PDF, extract text, and grep for a checklist of easily-lost specifics (advisor names, exact vote counts including abstentions, sub-clause cites, every single-source analyst estimate, insider election terms) before delivering. Condensation silently drops facts; the grep catches it.

---

# Deal Risk Assessment: [Acquirer] / [Target] ([TICKER])

*As of [date]. Blind fundamental assessment (Sections 1–7) composed without reference to current market pricing; Tape Check (Section 8) added after.*

## 1. Deal Summary
- Consideration, structure (merger sub mechanics), disclosed premium (with proxy/announcement citation); for election/mixed consideration: cash amount, exchange ratio, proration percentages, and the reference price/VWAP window
- Financing: committed amounts, sources, financing condition (y/n); insider election/rollover terms and board seats
- Termination fees (both directions) with exact trigger mechanics (tail period, Acquisition Proposal threshold, antitrust-specificity, sole-remedy/liquidated-damages language, specific-performance interaction); reverse termination fee as % of EV, benchmarked against the conventional 3–4%
- Regulatory efforts covenant characterization (efforts standard, divestiture-cap-by-schedule constructs, litigation commitment, remedy-proffer clock with the computed calendar date, pull-and-refile rights, interim acquisition standstills quoted verbatim)
- Outside date and extensions (initial date, increments, maximum, condition) — verified in the termination article
- Required approvals list (antitrust regimes, CFIUS, shareholder vote threshold)
- MAC definition highlights and carve-outs
- Dividend policy during pendency
- Advisors, both sides (financial + legal)

**Table 1 — Key Deal Terms** (term | detail | source)
**Regulatory Architecture table** (clause | what it does) — the efforts covenant walked clause by clause, verbatim where load-bearing
**Milestone/Status table** (date | milestone | source) — announcement, HSR filing, pull-and-refile, second request, S-4 effectiveness, vote (exact counts including abstentions), proffer deadline, outside dates; caption carries the analyst-by-analyst close-timing consensus

## 2. Buyer Classification and Competitive Footprint
- Buyer classification (financial sponsor / strategic / hybrid-consortium) with the entity-level evidence supporting it (acquisition vehicle, ultimate parent, equity commitment letter parties — cited)
- Financial sponsor: sponsor background, investment thesis, platform vs. add-on characterization, regulatory history, roll-up pattern
- Strategic: acquirer business overview, strategic rationale as stated, M&A history in sector, regulatory history, synergy claims
- Hybrid: both, with each element attributed to the parent it belongs to

**Table 2 — Acquirer Competitive Footprint**
- Sponsor form: portfolio company | stake (majority/minority) | sector / product lines | verified via (cite) | relevance to target
- Strategic form: segment / business line | revenue (cite) | disclosed competitors (verbatim, cite) | relevance to target
- Hybrid: both forms, attributed

## 3. Overlap Screen
- Method and sources; mutual competitor-listing check for strategic buyers
- Gate outcome: overlaps found or clean screen

**Table 3 — Overlap Screen** (footprint element | overlap type (horizontal/vertical/adjacent/potential/none) | overlapping target line | overlap geography | evidence citation)

## 4. Market Definition and Competitive Effects (conditional)
For each flagged overlap:
- Relevant product and geographic market definition; hypothetical monopolist reasoning
- Shares/HHI ONLY with cited data — filed figures or named sell-side estimates (firm, date) labeled "analyst estimate", with dispersion noted if analysts disagree; otherwise explicit data-limitation statement
- Any **self-drawn combined market position** from the investor deck (pro-forma share, rank, "#1/#2 in X"), quoted verbatim with the slide cited and labeled as the parties' own characterization — strong overlap evidence, not an independent estimate
- Theories of harm assessed: horizontal, vertical, potential competition, conglomerate, innovation, monopsony, plus buyer-type-specific theories (sponsor: roll-up seriality, cross-portfolio bundling, data advantage, minority-stake interlocks; strategic: unilateral effects, coordinated effects, killer acquisition/entrenchment, synergy-claim exposure)
- Barriers to entry
- Remedy likelihood and divestiture candidates

**Market Structure table — the complete attributed data set** (estimate | value | firm · date) — EVERY market-size, share, patient-pool, penetration, and positioning estimate gathered, one row each, attribution in every row; adjacent/non-overlapping-segment data included and labeled as such. This table is the no-omission guarantee for Phase 4: if an estimate was collected, it appears here.
**Table 4 — Verbatim Competitor Disclosures** (company | filing (form, date) | competitors as listed verbatim)
**Table 5 — Geographic Revenue Comparison** (region | target rev % (cite) | buyer-side entity rev % (cite) | combined-presence note)
**Table 6 — Divestiture Candidates** (asset | concern addressed | feasibility note) — only if overlaps exist

## 5. Financial Health
- Target: capital structure, leverage metrics with cited inputs, liquidity, maturities, covenant status, going-concern/distress flags, FCF profile, financing activity
- Strategic buyers without fully committed financing: acquirer balance-sheet capacity vs. consideration
- Assessment: financing/MAC risk contribution

**Table 7 — Capital Structure & Leverage** (item | amount | source filing)

## 6. Litigation and Fraud Screen
- Target and bidder legal proceedings with disclosed exposure (cited)
- Regulatory investigations; fraud/restatement history
- Short-seller reports / public allegations (publisher, date) or explicit "none found"
- Deal-specific litigation (merger objection, appraisal)
- Assessment: closing impediment / MAC relevance

## 7. Completion Assessment (Blind)
- Qualitative completion view grounded in named precedent transactions matched on buyer type and overlap profile

**Table 8 — Precedent Transactions** (deal | year | buyer type | overlap profile | regulatory outcome | timeline | remedy) — **one deal per row; never group multiple deals into one cell** (a cell reading "Deal A; Deal B; Deal C" hides three different outcomes and timelines, and a reader can't act on it). Every row states a **specific announce→close day count or dated range and the actual outcome** — vague timing words ("fast", "months", "clearing at pace") are not acceptable, because the day count and outcome are exactly what the reader came for. **List only genuinely comparable precedents — matched on BUYER TYPE and overlap profile;** do not pad the table with deliberately non-comparable "contrast" deals (a contrast, if it earns its place, is one line of prose in the synthesis, not a precedent row). If a row's specifics can't be sourced, drop it rather than list it vaguely; a still-pending deal has no completion outcome and is not a precedent (mention it in prose if relevant, but keep it out of the outcome table). ArbJournal deal files and Chain Bridge Research merger reports surfaced by the Vector Database are the first-class source for the review track, day count, and outcome — cite them inline from hit metadata (report title, institution, analysts, publication date); fall back to the parties' completion press releases / 8-Ks for the announce and close dates.

- Attributed sell-side views on regulatory track, timeline, and remedies — excluding all price/spread commentary, which belongs in Section 8 — presented in the table below, one row per attributed note
- Timeline scenarios (clean clearance / second request / litigation) vs. outside date

**Table 9 — Attributed Sell-Side Views on Completion** (Bank Name | Analyst Name | Estimated Completion Date | Thoughts on Antitrust Risk | Thoughts on the Merger Agreement) — one row per attributed note gathered across the channels (Outlook / uploaded deal-folder research / Vector Database) at enrichment point 2; use "—" for a column the note doesn't address, and leave Bank/Analyst as "unattributed" only when a source genuinely doesn't expose it. **Every column must carry a defined analytical purpose — do not add a "Miscellaneous" / catch-all column.** A Misc column reads as a junk drawer of unlabeled facts and dilutes the table; a fact worth keeping belongs in one of the defined columns or in the note's `research` write-up, not in a Misc cell. Keep the blind wall: no price targets or spread figures in any cell — those stay deferred to Section 8. **Row order is fixed by firm priority, not by date or channel** — sort High Weighting firms first, then Medium, then Low, then the ArbJournal / Chain Bridge / non-broker vector-database block, then unranked firms by date; see `references/sellside-priority.md` for the exact tier list and same-firm tie-breaking.
- Explicit data limitations encountered in this assessment, including the **Channel Attempt Log** (channel | action taken | result) for Outlook / uploaded research (Project or deal folder) / Vector DB ArbJournal pass / Vector DB Chain Bridge pass / Vector DB broad pass from the SKILL body — every channel needs a demonstrated action, not a bare "unavailable" claim — and any that were genuinely unavailable (not connected, no research files uploaded after checking with the user, vector index unreachable) with the failed action that proved it

## 8. Tape Check (composed strictly after Section 7)
- **Fresh Tape table** (quote item | target | acquirer): bid/ask/mid, market cap, derived share count, aggregate-cash cross-check against the announced cash component
- Current price, deal consideration, gross spread ($ and %). **Proration applies only when the deal is announced to be prorated as part of the transaction**: blended per-share consideration = (cash proration % × cash per share) + (stock proration % × exchange ratio × acquirer price); state the fixed cash leg and floating stock leg separately, then the blend, and spread the target against the blend. For deals without announced proration, spread against the stated consideration directly.
- **Spread Evolution table** (date | milestone | acquirer px | blended | target px | spread $ | spread %) — one row per Phase-0 milestone plus today, recomputing the blended consideration at each date for prorated deals; state explicitly whether the spread widened or compressed through each adverse-looking milestone. Flag large unexplained single-day moves.
- Annualized return under each Section 7 timeline scenario, with day counts
- Downside anchor: unaffected price with date and source
- Market-implied completion probability, stated as a function of the downside assumption; for prorated deals, computed against the blended consideration. **Mandatory stale-anchor sensitivity** when the market/acquirer has moved materially since announcement: present the naive number, name why the anchor is stale, and recompute at at least one labeled marked-down illustrative downside. Net any antitrust reverse fee per share against the gap-down in the regulatory tail.
- Spread behavior beyond the milestone table: trading through deal price (topping speculation); deal-as-downside-insurance comparison (target vs. acquirer move over the identical span); financing/dilution side-effects of a large acquirer move
- Sell-side spread/price-target commentary deferred from Section 7, cited (firm, date)

**Table 10 — Spread Economics** (item | value): gross spread vs. blended consideration, annualized by scenario, downside anchor, naive implied probability, marked-down sensitivity, break compensation per share, stock-leg-vs-cash comparison, downside-insurance comparison

- **Reconciliation:** one paragraph — does the market agree with the blind fundamental view; if not, which side has the better argument and what would resolve the disagreement (upcoming HSR deadline, vote date, filing).

## Sources
Consolidated list: every EDGAR filing (form, date, accession number where practical), report, and article cited above.
