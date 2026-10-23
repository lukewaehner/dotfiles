# Financing and Buyer

Load when: any consideration is cash, the buyer is a sponsor or newly formed vehicle, a named investor gives an equity commitment, a reverse fee is backed by a guarantee or escrow, or the buyer is a strategic paying in stock.

## Why it matters

A buyer that cannot or will not fund turns the deal into a fee claim. Who controls the buyer decides the HSR filing party, whose holdings count for overlap, and whether foreign or minority investors raise national-security or interlock questions. Whether disclosed sources cover the cash needed, how the reverse fee is backed, and what the buyer pays to walk set the real downside on a financing break.

## What to check

### Control chain
- Build a table: `Entity | Role | What it holds or controls | Control test | Source`. Rows: Parent, merger subs, principals or founders, the equity investor, every named co-investor, rollover holders and their post-closing stakes, lenders.
- Apply the HSR control test (16 CFR 801.1(b); confirm current text): 50% or more of voting securities or the contractual right to designate 50% or more of directors; for non-corporate entities, 50% of profits or of assets on dissolution. Never infer control from the size of a cheque.
- Filing party: if one holder passes, it is the ultimate parent entity and its controlled holdings are the buyer's footprint. If none passes, the buyer is its own ultimate parent. If undeterminable, write "not public", run both outcomes, and list the question (who designates Parent's directors, who holds 50% of profits).
- A newly formed vehicle led by operators with outside capital is neither a sponsor nor a strategic. Label it "operator-led vehicle with outside equity" so you never write "the sponsor has no overlap" about a fund that is not the sponsor.

### Sponsor portfolio overlap screen
- Enumerate the full current portfolio, majority and minority, from portfolio-company EDGAR filings, the sponsor's site, 13F, then press. Mark each verified or press-only. Keep minority stakes; agencies reach them through interlock and information-flow theories.
- Classify each holding against the target's lines and geographies: horizontal, vertical (state direction), adjacent, potential competition, none. Make the portfolio company the subject of every overlap sentence, never the fund.
- Count the sponsor's acquisitions in the sector over 5 to 10 years; serial add-ons are cumulative-concentration risk. Note platform versus add-on: an add-on into the same market is the highest-scrutiny sponsor configuration.
- Search the sponsor's regulatory history (second requests, consent decrees, abandoned deals) and state the result either way.
- Screen a co-investor's or equity provider's portfolio only if the control chain puts it inside the footprint or it has board seats, consent or information rights. A passive LP outside the footprint gets no horizontal screen; say why.
- Interlocks: Clayton Act §8 director overlaps with target competitors; holders with stakes in target competitors and post-closing information access.
- Sector-gated deals (insurance, banking, utilities): the regulator reviews the applicant, so check whether the sponsor has been an approved control person before, how many tiers and borders the ownership chain crosses, where acquisition leverage sits, affiliated arrangements, and capital plans. Expect negotiated commitments, which take calendar time. Continuity of an already-approved controlling holder is the strongest timing mitigant.

### Equity provider research
- Record exact legal name and cite, commitment document (date, amount or "not public", limited guarantee, third-party beneficiary status, funding conditions, expiry, assignment or syndication rights and whether the named investor is released).
- Entity resolution: search the exact name on EDGAR (entity search, Form D index). Deal vehicles often have no filing. Report the closest registered entity by name and general partner, labelled "closest registered entity, not confirmed as the same". List same-name, different-people entities as unrelated. Never merge entities on name similarity.
- Look-through routes, in order, recording which found nothing:
  1. The deal's own filings: Schedule 13E-3 (filing persons; source and amount of funds), proxy or information statement (financing, insiders' interests, Background), 8-Ks.
  2. Form D: issuer, year formed, general partner, promoters, total sold, number of investors, first sale. It does not name LPs.
  3. Form ADV Part 1 Schedule D §7.B.(1): per-fund gross assets, beneficial owner count, non-US ownership share, owner types. Most direct public source for foreign LPs. New vehicles may not be itemized; record the flagship funds.
  4. 13F-HR: listed US equity positions at quarter end; a target position shows an existing stake, absence proves nothing else.
  5. 13D/13G and Forms 3, 4, 5 for stakes in the target.
  6. Vendor fund screens (size, vintage, uncalled capital); cross-check vehicle size against Form D.
  7. Public pension and endowment commitment schedules: name LPs in a fund series (never their share of this deal).
  8. Firm site, press and portfolio-company filings; internal deal databases.
- Prior commitments: search for the firm with "equity commitment letter" and "take-private", EDGAR full text across 8-K, DEFM14A, SC 13E3 and SC TO-T, and internal deal files. Table: `Date | Target | Role | Amount | Outcome | Source`. Keep private-round investments separate from public-company equity commitment letters.
- Tag every fact with its source. Aggregator figures are leads only; tag them "unverified" or leave them out.

### Foreign LP and national-security signals
- Table: `Vehicle or holder | Foreign signal | Evidence | Source`. Signals: offshore feeder or parallel fund, non-US general partner, non-US share on Form ADV, sovereign or state-linked LPs on pension schedules, foreign owners named in documents.
- Read the agreement's foreign-person representation and any fund clause. Report what it says; it is no CFIUS determination. Foreign LPs in a fund matter mainly when they have control or access rights (31 CFR 800.307).
- Test the target: does it hold sensitive personal data on more than one million US individuals or critical technology? A yes makes non-controlling foreign access rights relevant; a no ends the point.

### Sources and uses
Every number carries a tag: [S] sourced with cite, [D] derived from [S] only, [E] estimate with its assumption named in the row. A mixed row takes the weakest tag. Never carry an [E] figure into a summary without its tag. Work the arithmetic in code.

Uses:
- Each paid share class and Up-C unit times the deal price, from the capitalization representation (note its date). Nominal classes at about zero.
- Awards: RSUs at deal price (show full amount as an upper bound if vested awards pay through payroll after closing or unvested awards convert to deferred cash), options at spread or zero if cancelled.
- Fully diluted equity value; reconcile to every other base in use.
- Debt payoff: principal at last balance sheet date [S], amortization to the working close [D], estimated principal at close [E], accrued interest [E], prepayment premium (sensitivity per 1% of principal unless the credit agreement was read), revolver draw. Take bond redemption or change-of-control put prices from the indenture.
- Fees and expenses: "not disclosed" unless sourced. List exclusions under the table.

Rollover check, holder by holder (every consent or support signatory, every holder named in rollover definitions, every 5% holder): `Holder | Stake | Value at deal price | Documented as rolling? | Source`. Use "Yes, size known / not stated", "No, not documented", or "Unknown, exhibit omitted". A holder that consents or signs a support agreement has not thereby agreed to roll. Write "[Holder] is not documented as rolling" for each, and show an "if they roll anyway" column. If a rollover's size is unstated, use 100% as a labelled upper bound.

Sources: equity commitment (amount or "not public"), debt commitments (or "none", stated), Parent and Merger Sub cash including any escrowed fee deposit (part of the plug, not on top), documented rollovers, target cash only if the funding representation counts it, other documented sources. Quote the funding-sufficiency representation and the Required Amounts definition and check what they must cover (consideration, debt payoff, premiums, fees).

Back into the unknown when commitments are not public: `Plug = total cash uses − rollover value − other documented sources`, in three scenarios (no one rolls; base case with documented rollovers only; all large holders roll), each with and without the RSU upper bound. If the agreement requires commitment plus Parent cash to cover Required Amounts, the base-case plug is the implied floor [E]. Compare it with outside evidence (Form D of the closest vehicle, fund size and uncalled capital, press reports of a raise, flagged as secondary). Name the filing that will disclose the amount and its expected date.

### Debt commitment quality
- Lenders, facility types and amounts; conditions limited to the merger conditions plus customary certain-funds items (SunGard-style limited reps, no due-diligence or market-out conditions).
- Flex terms if disclosed, commitment expiry versus the outside date, alternative financing obligation, whether ratings or leverage tests sit in the conditions.
- Whether the no-financing-condition statement and specific-performance clause cover every letter (equity, preferred, debt). An omitted letter is a drafting gap to flag.
- Marketing period and its interaction with funding (see timeline-and-dates.md).
- Pro forma leverage at the deal terms, with inputs cited, when the buyer's credit matters.

### Reverse fee: the ten facts
1. Amount and percent of fully diluted equity value, of EV and of cash needed from Parent, base stated each time.
2. Ratio to the Company fee, in dollars and percentage points.
3. Triggers: Parent breach, failure to close, failed deposit, financing failure, regulatory failure. State plainly whether regulatory failure triggers nothing.
4. Backing: guarantee, equity commitment, escrow or deposit, parent credit, nothing.
5. Recourse beyond the backing; the sole-remedy clause and its carve-outs with the defined willful-breach term.
6. Specific performance: closing, equity funding, deposit, and the limiters ("to the extent set forth in the Equity Commitment Letter", debt funded, all conditions met).
7. Escrow terms: amount, agent, account, deadline, interest, fees, release routes (to the Company on a fee-payable termination, to the paying agent as consideration at closing, back to Parent otherwise) and their Business Day counts.
8. Consequence of a missed deposit: termination right, cure, deemed breach, fee trigger. If silent, say so.
9. Interaction with the commitment letter: termination on fee payment, assignment or syndication, release of the named investor, third-party beneficiary rights.
10. Damages above the fee: lost-premium damages on willful breach, caps.

### Backing ladder (strongest to weakest collectability)
1. Investment-grade parent balance sheet, no financing condition.
2. Limited guarantee from a sponsor fund with disclosed capital.
3. Equity commitment plus limited guarantee from a newly formed vehicle.
4. Equity commitment alone, Company as third-party beneficiary.
5. Funded escrow or deposit with no guarantee beyond it.
6. Nothing.

An escrow secures collection of the fee up to the escrowed amount. It does not secure the closing; if the buyer refuses, the remedy is still the fee unless specific performance reaches the funding. It does show the vehicle held at least that cash by the deposit date; size it as escrow divided by cash needed from Parent. List the reasons the seller may have wanted it (shell buyer credit, investor unwilling to guarantee, commitment not directly enforceable, a specific concern about the equity source) as hypotheses, and say who asked is not public until the Background section is filed.

### Tripwire dates
For each deposit, funding, notice or filing covenant: `Date (computed with deal_clock.py bdays) | Event | Consequence if missed (quote) | Who can see it | Where it appears`. A timely deposit usually produces no filing; a termination produces an 8-K. Mark "no public confirmation expected" where true.

### Walk cost
Fee in dollars, per fully diluted share (state the count), percent of equity and EV, ratio to the Company fee. Where the fee is the sole remedy, the buyer's cost of not closing is the fee. If the MAE carve-outs cover industry conditions, cyber events and projection misses, the buyer cannot walk on a weak business and the fee is the price of the option to walk; name the next filing that will show the business. Arithmetic only, no forecast of buyer behaviour.

### Strategic buyer specifics
- The acquirer is the competitive entity: segments and revenue, Competition section verbatim, mutual-listing check, geographic revenue, M&A history, regulatory history, existing supply or customer links. Synergies framed as capacity cuts or pricing overlap read as admissions of horizontal proximity.
- Stock consideration: exchange ratio, collar and walk rights, acquirer vote (share issuance above 20% under exchange rules), S-4 effectiveness, dividend coordination, and the acquirer's own MAE and interim covenants. The spread depends on the acquirer's price; compute it at a live acquirer quote.
- Balance sheet: cash on hand, existing revolver capacity, bridge facilities and takeout plan, pro forma leverage and rating-agency commentary, any ratings condition.
- Market-extension deals: say the concentration analysis is inapplicable because the parties share no relevant market, and address any nominal touchpoint explicitly.

## How to conclude

- Filing party and footprint on present facts, whether the footprint adds overlap, and the foreign-ownership read, each with the document that will resolve unknowns.
- Sufficiency line, one of three: covered on the documents (state the margin); not confirmable (implied floor $X [E], outside evidence does or does not reach it); shortfall indicated (state the gap). Repeat the exclusions so the floor reads as a minimum.
- Equity provider assessment: facts first, then one labelled sentence. Say a provider "can" or "cannot" fund only when both the need and the capacity are sourced.
- Place the reverse fee on the backing ladder, state what any escrow does and does not secure, give walk-cost lines and tripwire dates.

## Reference data

- Company fee: about 2 to 4% of equity value (desk convention).
- Antitrust reverse fee: about 3 to 4% of EV (desk convention; use only when the fee is antitrust-specific). A fee well above suggests the parties saw real antitrust risk; absent or low suggests they saw a clean path.
- Reverse fee typically larger than the Company fee; reviewed deals ran about 2x to 3.5x.
- Sponsor deals with committed financing normally carry no financing condition and back the reverse fee with a limited guarantee. Escrowing the fee at signing is unusual.
- With fewer than five comparables, call the set thin and avoid "high" or "low".

## Common errors

- Writing "amount not public" and stopping, when the Required Amounts and rollover terms allow a floor.
- Assuming a consenting or large holder rolls.
- Counting the escrowed fee deposit on top of Parent cash instead of inside the plug.
- Treating the closest registered vehicle as the confirmed commitment party.
- Screening a passive LP's portfolio for overlap, or naming the fund instead of the portfolio company as the competitor.
- Dropping minority portfolio stakes.
- Reading a foreign-person representation as a CFIUS clearance, or concluding foreign control from an offshore feeder alone.
- Quoting fee percentages without a base, or comparing percentages computed on different bases.
- Assuming a missed deposit gives the Company a termination right when the agreement is silent.
- Taking aggregator AUM figures as fact.
