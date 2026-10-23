# Timeline and Dates

Load when: you need a working close date, a closing timeline, any deadline computed from an agreement covenant, a marketing-period read, an outside-date ladder, or a check on a close date someone else quoted.

## Why it matters

Annualized return is spread divided by time, so a close date that is a few weeks wrong mis-prices the trade more than most risk calls. The agreement's covenants fix a contractual floor that can be computed exactly; everything else (SEC review, regulatory friction, marketing-period blackouts) is a scenario above that floor. Brokers routinely quote dates that fall on holidays or that require the parties to file early, so test them before repeating them.

## Core rules

- **Working close date = contractual floor.** Build it from the agreement's own covenants and the statutory minimums, on the agreement's Business Day definition, with `scripts/deal_clock.py`. Never compute dates by hand and never average precedent timelines into it.
- **Precedent friction builds scenarios above the floor.** A pull-and-refile or second request appears as a labelled downside row. Move the working date later only with evidence in hand: an identified horizontal overlap whose precedent needed a refile or second request, a stated agency posture, or a state or foreign clock that runs later. Name the evidence in the same sentence. "Assuming a pull-and-refile" with no evidence is not allowed.
- **"Within X" is a deadline.** The fast path assumes the party acts promptly; the covenant outer limit assumes it uses the full window. Show both.
- **"Not required before X" is a permission to wait.** It sets no floor. The fast path uses the legal minimum instead (e.g. 20 days' notice for a Delaware meeting, mark "verify").
- **"As promptly as reasonably practicable, and in no event more than N days":** fast path = next Business Day; outer limit = day N.
- **Read the Business Day definition first.** Note every holiday calendar it names (New York banks, a foreign capital's banks). A definition that adds a foreign calendar can push a deadline days later than a weekends-only count.
- **Report the house date separately.** If the desk or a tear sheet has a date, show it as "House date" with its gap to the build; do not overwrite the build.
- Output one reusable line: `Working close date: [date] ([N] days from announcement); basis: [agreement section and calendar]; downside: [date] if [event].`

## What to check

| Input | Where it lives |
|---|---|
| Business Day definition and calendars | Definitions article |
| Closing mechanic ("N Business Days after conditions"), inside date, "not required before" clause | Closing section |
| HSR and other filing deadlines | Regulatory efforts covenant |
| Preliminary proxy / information statement / S-4 deadline | Proxy or information-statement covenant |
| SEC review mechanics, mailing deadline | Same covenant ("deemed no review if no notice by day 10") |
| Meeting timing, adjournment limits | Stockholder meeting covenant |
| Tender launch and initial offer period, extension duties | The Offer section |
| Marketing period definition, Required Financing Information, blackouts | Definitions; financing cooperation covenant |
| Outside date, extensions, cut-offs tied to it | Termination article |
| Earnings and fiscal-year dates | Target 10-K/10-Q filing history, earnings calendar |

## One-step merger with a proxy

1. HSR filing date from the covenant (often 10 to 20 Business Days after signing). Waiting period 30 calendar days, expiring 11:59 pm ET, rolled to the next business day if it lands on a weekend or federal holiday.
2. Preliminary proxy (PREM14A) date from the covenant (often 20 to 30 Business Days after signing). Add a Schedule 13E-3 if a target affiliate is on the buy side; it raises the chance of review.
3. SEC review decision: the SEC says within 10 calendar days of the preliminary filing whether it will review. No review: clearance at day 10. Review: model about 30 days from the preliminary filing to clearance and label the date illustrative.
4. Definitive proxy mailing: fast path the next Business Day after clearance; outer limit the covenant's window.
5. Meeting: legal minimum notice after mailing (20 calendar days for a Delaware merger vote; often stated as 20 Business Days in the agreement, which then governs; check which).
6. Closing: the closing mechanic after the last condition (e.g. 2 Business Days), or after the marketing period ends if one applies.

Written-consent deals: preliminary information statement (and 13E-3 if any), the same 10-day SEC review decision, mailing, then at least 20 calendar days after mailing before the action can be taken (Rule 14c-2). Do not estimate SEC review time as a fact; show the no-review case and an illustrative review case.

Stock or mixed deals: S-4 effectiveness replaces proxy clearance and SEC review of an S-4 is more common; add an acquirer vote if share issuance needs one.

## Cash tender offer

1. Launch: the covenant's Business Day count after the agreement date (commonly 10 to 15 Business Days).
2. HSR: filing per covenant; 15 calendar days for a cash tender (16 CFR 803.10), expiring 11:59 pm ET, rolled off weekends and holidays. Do not default to 30.
3. Initial offer period: 20 Business Days under Rule 14e-1, or a shorter period where the agreement relies on an SEC exemptive relief for qualifying all-cash, negotiated, fixed-price offers for all shares closing through a §251(h) back-end merger. Quote the clause and say which basis applies. Offer business days under Rule 14d-1(g)(3) exclude weekends and federal holidays, so Columbus Day and Veterans Day always count as closed.
4. Expiry: the later of the offer expiry and HSR expiry, plus any mandatory extension the agreement requires while conditions remain open.
5. Close: the business day after acceptance; the §251(h) merger follows the same day or the next.
6. Second request on a cash tender: waiting period ends 10 days after substantial compliance (30 for a merger). Never guess the compliance date.

## Marketing periods

A marketing period gives lenders a run of consecutive Business Days with current financial information before the buyer must close. It can add weeks to the floor and is where most hand-built timelines go wrong.

- **Length.** Count the stated consecutive Business Days (commonly 15 to 20; shorter periods exist). The period usually must run once, uninterrupted.
- **Start conditions.** Typically: the buyer holds the Required Financing Information and it is "Compliant"; often the stockholder vote or other conditions must be satisfied (or capable of being satisfied) during the run. Some let the Company give notice of an "Indicated Date" with a short objection window for the buyer.
- **Blackouts.** Read the exact excluded days. Common: a single day around Thanksgiving or July 4 that is not counted; a year-end cut-off (if the period has not ended by about December 18 to 20, it cannot start until early January); a summer cut-off in some agreements. A range of vote dates can then produce the same closing date. Show the date the period would have to start to beat the cut-off, and whether that is feasible.
- **Staleness.** Financial information must be current for an offering. Track the dates when the latest quarter's interims go stale under 144A practice (about 135 days after the quarter end; mark "verify") and when the agreement's own age tests flip (e.g. annual audited statements required once closing falls 60 or more days after fiscal year end; quarterly reviewed statements 45 or more days after quarter end). A period that runs past a staleness date must restart with new statements.
- **Audit-date resets.** After fiscal year end, the new audited statements can become required. If the audit is not ready, the period cannot start or must restart. Put the fiscal-year audit date on the timeline.
- **Restart events.** Information ceasing to be Compliant, an auditor withdrawing an opinion, a restatement, a Company announcement of an intended restatement.
- **Early end.** Most definitions end the period when the debt financing funds, including into escrow. Show this as an alternative close path.
- **Inside date.** Some agreements set a date before which the buyer need not close regardless. Check whether the buyer may waive it.
- **Late-stage relief.** Some definitions stop requiring the vote as a start condition after a stated date, letting the period run before the meeting. Add that row.

## Outside dates

- Initial date, each extension, the conditions for extending (usually only regulatory conditions unsatisfied) and who may extend. State "no extension" when there is none.
- Run `ladder` and say which extension step the company's own close guidance first fits inside. Guidance that only fits in a later extension tells you the parties expect to need it.
- Cut-offs tied to the outside date: concessions owed to allow closing N Business Days before it; adjournment limits; failure-to-close rights.

## Using scripts/deal_clock.py

Always pass `--cal` explicitly; `bdays` defaults to `us,fr`. Supported calendars: `us` (federal holidays, which also close New York banks), `fr`, `none`. For any other foreign calendar the definition names, count by hand against that country's published bank holidays and say so, or extend the script.

| Subcommand | Use |
|---|---|
| `bdays --start D --n N --cal us` | Date N Business Days after D; also prints the weekends-only count |
| `adddays --start D --n N [--base D] [--outside D]` | Calendar-day clocks (HSR, 20-day notice, state and foreign reviews) from the filing date; gap to base close and room inside the outside date |
| `ladder --signing D --announce D --initial D --months 3,6 [--guidance D]` | Outside-date ladder and which step guidance needs |
| `tender --agreement D --cal us --launch-bd N --hsr-bd N --offer-bd N [--hsr-days 30] [--early D] [--second-request-compliance D]` | Earliest close from launch, HSR and offer-period covenants, with deadline, weekends-only, early-filing, one pull-and-refile and (only with a compliance date) second-request cases; `--hsr-days 30` for a one-step merger |
| `tender ... --check D [--check D]` | Test a quoted close date: weekend or holiday, earlier than physically possible, or feasible only if the parties file by a stated day |
| `spread --price P --deal X --asof D --close D` | Gross spread and annualized return for each close date |
| `implied --deal X --irr 0.08 --baseline D --asof D [--shift 30]` | Entry price needed for a target IRR at the baseline and baseline plus or minus the shift |
| `hurdle --price P --deal X --irr R --asof D` | Close date at which today's price earns exactly the target IRR |
| `decompose --price P --deal X --close D --asof D --rf R` | Splits spread into time value and residual risk premium; `--rf` must be a sourced current rate |
| `downside --price P --deal X --unaffected U [--rf R --close D --asof D]` | Dollar upside and downside, downside per $1 of upside, and market-implied break probability with and without carry |

Quote the script's output table. When the agreement-calendar count and the weekends-only count differ, show both: the agreement count is the deadline, the weekends-only count is the early-filing reference that brokers often use.

## Building the timeline

Columns: `Step | Rule (section) | Deadline | Fast path | Covenant outer limit | SEC-review case`. Rows: signing and announcement; each filing and its waiting period; one pull-and-refile downside where relevant; earnings dates that change financial-information tests; preliminary proxy or information statement; SEC review decision; mailing; record date if fixed; meeting; marketing period; **Closing** with day counts from announcement; early-close alternatives (debt into escrow); staleness and audit dates; any date after which a condition stops applying; failure-to-close right; adjournment cut-off; **outside date**.

## How to conclude

State the working close date line, then the main downside timing case and the trap that converts days into weeks (year-end blackout, staleness restart, second request, foreign clock). Compare the floor with precedent timelines for the same lead regulator and say which you trust and why; the build usually governs because precedent perimeters rarely match. For each precedent say in one clause why it is or is not analogous and whether it needed a pull-and-refile, since a clean headline outcome can hide procedural friction.

## Common errors

- Treating "not required before X" as the closing floor.
- Using the 30-day HSR period on a cash tender offer, or 15 days on a merger.
- Counting Business Days on weekends only when the definition names New York or foreign bank holidays; letting `bdays` default to `us,fr` on a US-only definition.
- Computing an offer period on the agreement's calendar instead of the Rule 14d-1(g)(3) federal-holiday calendar.
- Repeating a broker's close date that falls on a holiday or needs a filing before the covenant deadline.
- Adding a default pull-and-refile to the working date when none of the comparables needed one.
- Ignoring a marketing-period year-end blackout, so the floor lands in late December when it cannot.
- Missing a staleness or audit date that forces a restart in the slower paths.
- Stating an SEC review duration as fact rather than as an illustrative scenario.
- Measuring state or foreign review clocks from announcement instead of from the filing date, and forgetting that information requests can toll them.
