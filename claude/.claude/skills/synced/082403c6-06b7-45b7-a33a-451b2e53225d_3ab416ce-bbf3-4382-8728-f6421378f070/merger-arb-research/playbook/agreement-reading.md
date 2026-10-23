# Agreement Reading

Load when: a merger agreement (or its 8-K summary) is in hand and you need to extract the terms that move the spread, the close date or the downside, or test whether a term is unusual.

## Why it matters

The agreement fixes what holders receive, what must happen before closing, who can walk and at what cost, and how fast the parties must act. Most spread-moving facts are on its face, but scattered across definitions, the termination article, exhibits and disclosure-schedule references. Read the operative text; summaries in 8-Ks, press releases and broker notes are leads to check against it.

## Sourcing rules before you read

- Read the agreement's Termination and Expenses sections directly for every fee amount, payer and trigger. The agreement controls over any 8-K Item 1.01 summary. Two 8-Ks that agree with each other can share the same drafting error, so matching summaries are no corroboration. If a summary conflicts with the text, use the text and flag the discrepancy at the top of the output.
- Pull the acquirer's own 8-K on the same date as well as the target's. It often restates exhibits in prose and can carry figures the exhibits omit (aggregate voting power under a support agreement is the usual one).
- Read an exhibit's body before writing "not found". A title in the filing index is no evidence of what the exhibit says. If a figure is missing from the exhibit text (a share schedule that did not survive extraction), check the acquirer's 8-K, then the 13D or the forthcoming proxy, and log it as an open item naming where it will appear.
- Treat a truncated tool read as a reason to page further. Long definitions articles hide single terms (confidentiality agreement date, Business Day, Required Amounts) deep in the alphabet.
- Grep defined terms with the curly quotation marks the filing uses; straight-quote searches fail silently. When a search lands near a provision, read 20 to 30 lines either side before concluding it is absent.
- Quote verbatim with section and page. Bracket computed dates next to the clause, e.g. "within 25 Business Days [Nov. 17]", computed on the agreement's own Business Day definition (see timeline-and-dates.md).
- State the equity-value base for every percentage. If a broker or 8-K uses a different base, show both and say which you use.

## Reading for departures

The most useful comparison is the buyer's own last comparable agreement. Read the two side by side, article by
article (`edgar-redline` where both are on EDGAR), and include the termination, fee and remedy articles in full:
who may terminate on which ground, what notice or waiting step comes first, what the other side may do in that
window, and when the fee is paid. Differences inside a clause matter as much as different clauses. For each
difference, ask which side asked for it and what it protects against, and write it as a flag (SKILL.md, "Flag
what could matter"). The baselines at the end of this file stand in for the norm when there is no prior deal.

## Reading map

### Consideration and adjustments
- Effect on capital stock: per-share cash, exchange ratio, mix, CVR, each share class and any nominal-consideration class.
- Election and proration: elections allowed, oversubscription mechanics, election deadline, default treatment of non-electing holders.
- Collars, walk-away prices and price-adjustment formulas for stock deals; ticking fees (trigger date, which approvals trigger it, rate and compounding, accrual end and cap). A ticking-fee trigger date is the parties' own base case for when named approvals should land.
- Equity awards: vested and unvested RSUs, options (cash spread or cancelled), units in Up-C structures, and when each is paid.
- Equity value and EV: compute from the capitalization representation (note its as-of date) times price; reconcile to the press figure.

### Conditions
- List every condition from the conditions article, split mutual, buyer-only, seller-only.
- State which regulatory regimes condition the close and which appear only as filing covenants. Only a condition lets a regulator's silence stop the deal.
- Check whether jurisdictions sit on a confidential schedule and whether the "Competition Laws" or "Antitrust Laws" definition sweeps in foreign direct investment laws.
- Note any dissenting-shares cap, minimum tender condition, majority-of-the-minority condition, financing condition, marketing-period gate or inside date.

### Efforts, burdens and divestiture caps
- Efforts standard: reasonable best efforts, commercially reasonable efforts, or "all actions necessary" / hell-or-high-water.
- Divestiture obligation and its cap: unlimited, materiality standard, dollar or revenue cap, or a pre-agreed basket "except as set forth on Section X of the Parent Disclosure Schedule". A schedule basket means the parties mapped the problem assets before signing.
- Carve-outs for the buyer's affiliates, sponsor funds and portfolio companies; whether remedies are limited to target assets.
- Burdensome Condition definition: quote it, since it is the real ceiling on what the buyer must give up.
- Litigation duty (defend through final non-appealable order or weaker), who controls strategy, remedy-proffer clock (compute the date), pull-and-refile rights, timing agreements.
- Clear skies: bans on buyer or affiliate acquisitions that would delay or impede approval. Named product spaces in an acquisition standstill are the parties' own market definition.
- Filing deadlines for every approval named in the conditions, with computed dates.

### Termination rights and fees
- Every termination trigger, who holds it, and any cure period.
- Company fee and reverse fee: dollar amount, percent of fully diluted equity value and of EV, ratio of reverse to Company fee.
- Triggers by section for each fee. Say whether regulatory failure triggers the reverse fee; if not, the fee prices buyer default only.
- Tail provisions: which terminations start the tail, the look-back requirement (proposal made or publicly known before termination), the tail length and the acquisition-proposal threshold used (often raised to 50%).
- Expense reimbursement, fee reductions for go-shop or excluded parties, enforcement-cost caps, and whether fees are payable more than once.
- Mark spent protections in brackets, e.g. a superior-proposal fee after written consent is delivered: "[spent: approval already delivered]".

### Specific performance and remedy limits
- Is specific performance mutual? Can the Company force closing, force the equity funding, force a deposit?
- Conditions on it: all conditions satisfied, debt funded or will fund at closing, Company confirms readiness. Bold any link to debt availability; it decides whether the reverse fee is the real remedy.
- Election between specific performance and the fee; sole-and-exclusive-remedy clause; carve-outs for fraud and willful breach and the defined term used.
- Damages above the fee: whether the Company can recover lost stockholder premium.

### Deal protection
- No-shop scope and start; go-shop window with exact end timestamp, excluded-party definition and cut-off, reduced fee.
- Fiduciary outs: Superior Proposal (termination right) and Intervening Event (recommendation change only). Note any requirement to hold the vote anyway (force-the-vote).
- Match rights: notice days, re-match days on each amended proposal, whether unlimited.
- Return-or-destroy demands to prior bidders, standstill waivers ("don't ask, don't waive").

### Outside date and extensions
- Initial date and time, who may extend, increments, maximum date, conditions for extension (usually only regulatory conditions open). State plainly when there is no extension.
- Cut-offs tied to it: regulatory concessions owed so as to close N days before it, meeting adjournment limits, failure-to-close rights.

### Voting, support agreements and written consent
- Vote standard (majority outstanding versus votes cast), class votes, acquirer vote for share issuance.
- Support agreements: holders, shares, percent of outstanding and percent of voting power (these differ with high-vote stock), termination on recommendation change.
- Written consent: who delivered it and when; if delivered at signing, the fiduciary out, Company fee and go-shop may be spent. Information-statement mechanics go to timeline-and-dates.md.
- Rollover holders and the receiving entity; whether a target affiliate sits on the buy side. Officers or controlling holders who roll equity into the buyer and keep their roles are normally treated as affiliates engaged in the going-private, so presume a Schedule 13E-3 until the proxy says otherwise. The absence of a 13E-3 reference in the 8-K or legends settles nothing; it is filed with the preliminary proxy or information statement. A 13E-3 raises the odds of SEC review and of disclosure litigation, so it goes on the timeline.

### Interim covenants and dividends
- Target forbearance list and consent standard; permitted dividends and their record dates; dividend coordination in stock deals.
- Parent covenants: cash-maintenance requirements, "Cash Leakage" restrictions, acquisition standstills.

### MAE definition
- Single-prong versus "ability to perform" prong.
- Carve-outs: general economy and markets, industry conditions, geopolitics and trade, tariffs, pandemics, cyber events, changes in law or GAAP, failure to meet projections, announcement and pendency, actions required by the agreement.
- Disproportionate-effect qualifier: which carve-outs it applies to and the comparison group.
- If carve-outs cover industry conditions, cyber and projection misses, the buyer cannot walk on a deteriorating business; the reverse fee becomes the price of walking.

### Appraisal
- Who holds rights (class, meeting or consent), notice and demand clock, cash consideration (no market-out exception), any dissenting-shares cap and who can waive it, Company duties on demands.
- Compute the de minimis thresholds for the statute in force (for Delaware, 1% of the class or $1M at the deal price) and mark statute points "verify".
- Consenting holders usually fall out of the pool. Appraisal does not stop closing; it lowers cash paid at closing and leaves a post-closing claim.

### Financing covenants and cooperation
- Commitment letters described (equity, debt, preferred), conditions, termination of letters, alternative financing obligation.
- No-financing-condition statement; check that it covers every commitment letter.
- Company financing cooperation, Required Financing Information, marketing period (see timeline-and-dates.md), debt payoff letters, Required Amounts definition. Full sufficiency test is in financing-and-buyer.md.

### Closing mechanics
- Closing date: "no later than N Business Days after" conditions, any inside date, any "not required to close before [date]" clause and whether the buyer may waive it.
- Confidentiality agreement date and clean-team terms; if only in a disclosure schedule, cite the schedule and write "date not public".
- Tax treatment (taxable cash, reorganization intent, tax opinion as a condition).

## Beyond the agreement

- Commercial-contract change of control: when the target's value rests on one customer, licensor or supply partner, find that contract (8-K material contracts, the agreement's Material Contracts rep and schedule index) and quote its change-of-control or assignment clause. State whether it requires consent, gives the counterparty a termination or license-out right, or survives untouched. Party statements about the relationship are no substitute.
- Same-buyer diff: see "Reading for departures" above. If no prior deal by the acquirer is readily found, use the closest deal by a comparable buyer and say so.
- Target bonds: if public bonds exist, pull a price and say whether the credit read agrees with the equity spread. Bonds moving toward the takeout or change-of-control price corroborate; no move or the wrong direction diverges.
- Acquirer's same-day call: management often says live what neither release puts in writing (synergy composition, regulatory overhangs priced in).
- 10-K Competition sections of target, acquirer and one named rival: note who names whom; asymmetry is market-definition evidence.

## Coverage before finishing

These are places a first-day read usually needs to have looked; use the list to spot a gap in the tree, not as the order of work. A strong read covers each or marks it "not public" with the document that will disclose it: closing date mechanic and any floor date; each condition including approvals by schedule; Competition Laws definition scope; foreign-person or CFIUS representation (a representation, never a CFIUS determination); consent delivered or vote required; information-statement or proxy filing deadline [computed]; SEC clearance and mailing covenants; HSR filing deadline [computed] and early termination request; other filings; efforts standard, remedy scope and carve-outs; litigation duty; clear skies; outside date and extensions; both fees with percent and base, triggers and spent status; reverse-fee security and deposit dates [computed]; specific performance and its limits; equity and debt commitments and financing condition; cash-maintenance covenant; confidentiality agreement date.

## How to conclude

- Name the single most important structural asymmetry (e.g. remedy limited to the fee, uncapped divestitures on target assets only, no extension).
- Give each non-standard term once, in the "Unusual terms" format (SKILL.md), with the agreement or baseline it departs from and one sentence on what it does to completion, timing, the exit or the price if the deal fails. A term that could move price or date also becomes a risk.
- If nothing is non-standard, say so and name the agreement or baselines it was compared with. List clauses that could not be read (unfiled schedule, omitted exhibit) as "could not be tested".

## Non-standard flag list (baselines)

Baselines are desk conventions from reviewed agreements. Present them as conventions, never as market percentiles. With fewer than five comparables, write "possibly non-standard, thin set".

| Topic | Usual shape | Flag when |
|---|---|---|
| Company fee size | About 2 to 4% of equity value | Above 4%, or below 2% (low fee is optionality-positive for a topping bid) |
| Reverse fee size | Larger than the Company fee, about 2x to 3.5x in reviewed deals; antitrust reverse fee about 3 to 4% of EV | Outside that ratio, large against equity, or absent in a deal with real regulatory risk |
| Reverse fee triggers | Parent breach, failure to close, sometimes regulatory failure | Regulatory failure triggers nothing in a deal with overlap; fee is sole remedy for a financing failure |
| Reverse fee security | Sponsor limited guarantee or equity commitment | Funded into escrow or posted as collateral at or after signing; nothing backs it |
| Buyer liability cap | Reverse fee is the cap; fraud and willful breach carved out | Cap also covers willful breach |
| Company fee triggers | Superior proposal, recommendation change, breach, plus a 9 to 12 month tail | Trigger already spent at signing; tail longer than 12 months or threshold below 50% |
| Go-shop | None in most deals; where present, about 30 to 45 days with a reduced fee for excluded parties | Very short window, no fee reduction, excluded-party cut-off before the window ends |
| Match rights | About 3 to 5 Business Days, shorter on re-match | Unlimited full-length re-matches, or longer than 5 Business Days |
| Fiduciary out | Superior Proposal and Intervening Event until the vote | Ends at signing because approval is already in hand; no Intervening Event out |
| Efforts and remedies | Reasonable best efforts with a divestiture cap or materiality limit | Hell-or-high-water, uncapped, or carve-outs for the buyer's own businesses |
| Clear skies | Ban on acquisitions that would delay clearance | Absent in a sponsor deal with a portfolio, or unusually broad |
| Financing condition | None where financing is committed | A condition exists; no debt commitment and no marketing period in a deal that looks levered |
| Specific performance of equity | Available once conditions are met and debt is funded | Conditioned on matters outside the equity's control, or unconditional enforcement of the equity letter |
| Parent cash covenant | Equity funds at closing; no standing covenant | Parent must hold Required Amounts in cash and avoid leakage |
| Closing floor | Closing two or three Business Days after conditions | A fixed date before which the buyer need not close |
| Stockholder approval | Meeting or tender | Written consent delivered at signing |
| Controller on both sides | Disinterested approval (special committee, majority of the minority) | Controller rolls or funds and consents at signing with neither safeguard |
| Competition-law scope | Named regimes | Jurisdictions only on a confidential schedule; definition includes FDI laws |
| Foreign-person representation | Rare for a domestic sponsor | Parent represents it is not a foreign person or the deal is not a covered transaction |
| Confidentiality agreement | Date in text or proxy Background | Date only in a confidential schedule |
| Rollover | Separate filed agreement | Rollover agreement omitted, share count not stated |
| Damages | Company cannot recover lost premium | Company may recover lost-premium damages |
| Dissenting-shares condition | Absent in most large cash deals | Present, or absent where a visible appraisal block exists |
| Related-party payments | TRA kept or bought out at a disclosed amount | Termination payment to a selling holder outside the consideration, size undisclosed |
| Deposit or funding date | Funding at closing only | A deposit date that no public filing will confirm |
| Outside date | One or more extensions for regulatory delay | No extension |
| Tender offer period | 20 Business Days | Shorter period; check whether it relies on an SEC exemptive order and whether the deal qualifies |
| MAE | Carve-outs with disproportionate-effect qualifier | Single-prong with very broad carve-outs, or no carve-out for a risk the target clearly faces |
| Internal consistency | Covenants match conditions; defined terms defined | A covenant contradicts a condition, a fee cannot trigger under the stated structure, a no-financing-condition sentence omits a commitment letter |

## Common errors

- Reading "no 13E-3 mentioned yet" as "no 13E-3" when management or a controller rolls equity into the buyer.

- Copying a fee, payer or trigger from an 8-K without tracing it to the agreement's defined-term cross-references.
- Marking an item "not found" on an exhibit title, or after a truncated read.
- Quoting a fee percentage without its base, or silently adopting a broker's base.
- Treating a representation (foreign person, no covered transaction) as a regulatory determination.
- Missing that written consent at signing has spent the fiduciary out, the Company fee and any go-shop.
- Reading "reasonable best efforts" as hell-or-high-water, or missing a sponsor-portfolio carve-out that confines remedies to target assets.
- Calling a regime a risk to completion when it appears only as a filing covenant and not as a condition.
- Accepting a party's characterization of a key customer or licensor relationship without reading the contract.
- Folding commercial change-of-control risk into the MAE discussion, where it does not belong.
