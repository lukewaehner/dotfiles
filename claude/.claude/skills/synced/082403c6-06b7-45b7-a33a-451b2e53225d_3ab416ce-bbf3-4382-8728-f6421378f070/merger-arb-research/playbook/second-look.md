# Second look: questions first reads tend to skip

Load when: running Hour-1, or when Minute-1 has time left after the call is made.

These are the questions that a quick read of the press release, the agreement and the 10-K usually leaves
unasked, and that a good broker note asks the next morning. Use them as prompts for branches the research tree
does not have yet. Keep the questions that apply to this deal, open a branch for each and follow it like any
other; the rest get one line on why they do not apply.

## Approvals

- Have you listed every approval from the target's own footprint, rather than only the ones the press release
  names? Revenue by country, subsidiaries in Exhibit 21, sites by state, licences and permits.
- Did you rule out a foreign regime because "the buyer has no turnover there"? That holds only once the buyer's
  control group is documented. For a new vehicle, name the regimes the target qualifies for on its own and keep
  them on the list as "on present facts, depends on who controls the buyer". FDI regimes never depend on buyer
  turnover.
- When the agreement points to a confidential schedule of approvals, what does the target's footprint say the
  schedule must contain? Apply each regime's threshold to sourced figures (`foreign-approvals.md`,
  `state-healthcare.md`).
- What is the second-longest clock after the one everyone names, and could it overtake it? EC
  pre-notification, a state review, a foreign investment screen and a sector regulator each run on their own
  timetable.
- Does any statutory clock run from the filing date rather than announcement, and what is the latest permitted
  filing date under the agreement?
- How long did this buyer's own past deals take from announcement to close, and with which regulators?
- Is a rule change, a leadership change or a pending policy at a reviewing agency likely to apply to this deal?
- For a foreign buyer or foreign money: does the target hold government contracts, security clearances,
  defense or cloud authorizations, sensitive personal data or critical technology? Does the buyer already hold
  a cleared U.S. subsidiary or an existing mitigation agreement? Does a rival already operate under a
  foreign-ownership arrangement in the same market, which shows what mitigation looks like?

## Competition

- Have you mapped products to customers and tasks for both parties, including the buyer's acquired brands that
  trade under their own names? Two companies that never name each other can still sell competing products to
  the same niche customer.
- Have the parties partnered, licensed, distributed for or invested in each other before?
- What do management say on the calls about who they compete with and where synergies come from? Capacity or
  site consolidation is an admission of overlap.
- Does the efforts clause cap divestitures in a way that shows what the parties expect to give up?
- Is any vertical theory live (an input or interface one party controls that rivals of the other need), or
  access to rivals' confidential information?

## Buyer and money

- Who controls the buyer, end to end? A newly formed vehicle has owners; find them.
- Who are the equity providers, are they part of the buyer group or outside investors, and do any have foreign
  limited partners or holdings that create a filing, an interlock or a national-security question?
- Do the disclosed commitments cover the cash needed at closing? If amounts are not public, back into the
  minimum from the uses (equity price, debt payoff, fees) and the documented rollovers. A holder who consents
  is not a holder who rolls unless a document says so.
- How is the reverse fee backed (parent guarantee, limited guarantee, escrow, nothing)? If the seller demanded
  an escrow or a deposit, what does that imply about the buyer's credit, and what does the escrow secure and
  not secure? What dates do deposit and funding covenants create, and what happens if one is missed?
- What does it cost the buyer to walk, as a ratio of the reverse fee to the company fee and as a share of
  equity value, and can the target force the close?

## Shareholders and litigation

- Is a controller, a large holder or management on both sides of the deal through rollover, continuing roles
  or holder-specific benefits? If officers or a controller roll equity into the buyer and keep roles, write
  "Schedule 13E-3 likely" and put the higher SEC-review odds into the timeline; the proxy confirms it.
- Was approval delivered by written consent at signing, with no disinterested vote? Are there MFW protections?
- Are there special payments to some holders (TRA termination payments, side letters, liquidity for a seller
  that others do not get)?
- Are appraisal rights available, and is there an appraisal-out or a cash-at-closing need that appraisal
  claims could stress?
- Is any suit, books-and-records demand or appraisal petition already filed? Check the docket and the
  "investigation" announcements from plaintiff firms.

## Timing mechanics

- Is the working close built from the agreement's own covenants (filing deadlines, waiting periods, offer
  period or proxy steps, Business Day definition), with every date run through `deal_clock.py`?
- If there is a marketing period: how many consecutive business days, what blackout windows, when does
  required financial information go stale, does an audit date reset it, does it end early when the debt funds?
  Which blackout does the earliest start actually hit?
- Is "not required before X" being misread as a floor? It is a permission; the floor comes from the deadlines.
- Does a tender offer clock or a SEC review change the floor? Is a broker's quoted close date feasible?
- Does guidance sit well past the contractual floor? If so, list the candidate reasons and test each.

## Business and contracts

- Does the target depend on one or two customers, licensors or partners? Read their contracts'
  change-of-control and assignment clauses directly rather than relying on either party's description.
- Do the target's bonds or loans have change-of-control puts or consents, and what does the bond price say about
  completion?
- Does the target report results before the expected close, and how exposed is it to a weak quarter given the
  MAC definition's carve-outs?
- Has the agreement been compared with the buyer's last comparable agreement? A missing carve-out or a different
  fee level is evidence.

## Market

- Is the unaffected date right (leaks, prior bids, rumours) and is the downside adjusted for the sector move since?
- Was there prior interest from other bidders (proxy background later; press and 13D history now)?
- What supply or technical pressure is coming (index deletions, arb crowding, stock-deal hedging, borrow)?
- Was any of the above public before the announcement and in our own library? Check our research first.
