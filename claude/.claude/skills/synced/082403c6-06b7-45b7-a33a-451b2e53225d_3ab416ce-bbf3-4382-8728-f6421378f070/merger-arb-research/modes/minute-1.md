# Minute-1: the first call

Goal: within 5-10 minutes of the announcement, often pre-market, give the desk a call it can trade on: buy or
not, up to what price, why, and what is still unknown. Run the read, flag, follow method in SKILL.md on a
short clock. A call made on what can be known now, with its assumptions named, beats a slow complete answer;
Hour-1 follows the branches left open.

## 1. Orient and launch the first wave (first 1-2 minutes)

If a living document exists for this target (`merger_arb_deals/{TICKER}/{TICKER}_living_doc.md`, for example from
a Rumor run), start from it: compare the announced terms with the scenario that was pre-priced, take its research
tree as known, and spend the agents on what differs.

From the press release and 8-K: target, buyer and who controls it, consideration, structure (one-step merger,
tender, scheme), signing date, stated conditions, guided timing, and whether the merger agreement (Ex-2.1) is on
EDGAR yet (it often lands a day later). As soon as you have that, launch in one turn:

- **Terms agent**: reads the agreement in full (or the PR and 8-K if it is not filed) and returns two things.
  First, the facts the call needs: conditions, covenant deadlines and Business Day definition, outside date,
  both fees with their triggers and payment mechanics, remedies, financing, votes and consents, rollover.
  Second, the flags: every clause that departs from the buyer's last comparable agreement or from the
  baselines in `playbook/agreement-reading.md`, every clause that changes who can walk, when or at what cost,
  and every clause that conflicts with the press release. Each flag comes back as a one-line branch
  (SKILL.md, "Flag what could matter").
- **Market agent**: last price with time (pre-market quote if that is all there is), unaffected price and date
  (check the tape for a run-up before it), peer or index move since, holder base, prior bids, short interest,
  target bonds.
- **Precedent agent**: `arbjournal-precedents` (regimes such as `antitrust:us`, `since` about three years back)
  plus the closest comparable deals on EDGAR, including the buyer's own recent deals: days from announcement to
  close with median and middle half, the cases that ran long and why, any that failed or were repriced. If
  ArbJournal is unavailable, say so at the top of the report and use EDGAR alone.
- **One to three agents on the branches the announcement already shows.** The scope usually reveals them: a
  foreign buyer of a government contractor, a new vehicle with undisclosed equity, a multi-state health care
  target, an obvious horizontal overlap, a controller on both sides. Brief each on its branch with two or three
  angles from `playbook/research-angles.md`.

Use only information dated up to now. Broker notes in the chat or inbox are inputs; check anything they carry
against a primary source before it reaches the top of the output.

## 2. Build the first tree (while the agents run)

Write the branches you can already see, then add the terms agent's flags as they arrive. For each, decide in a
line whether any answer could move the call. Close the ones that cannot, with the reason. Rank the rest by how
much they could move the buy price or the date. If an open branch looks decisive and nothing covers it, launch
an agent on it now. Compute the expected and delayed closing dates with `scripts/deal_clock.py` as soon as the
covenant terms arrive.

## 3. Price and call

Price if the deal fails: the unaffected price adjusted for the peer or index move, with a range and its basis
(`playbook/spread-and-downside.md`). Then the price test and the call as in SKILL.md ("The call"): list the dated
cases (early, expected, delayed, deadline; each delayed case tied to evidence) and run `deal_clock.py cases` with
the last price and one or two lower trigger prices. If the call depends on something not yet checked or not yet
knowable, the call line says so. With no print yet, give the ceilings and returns instead of a spread. If the
agreement is not filed, name the terms the call takes from the press release.

## 4. Output template

Write for the whole desk (SKILL.md, "Plain English for the whole desk") and run the substitution table over the
finished text. Risks and unusual terms follow SKILL.md, "Writing the risks" and "Writing the unusual terms".

```
# {TARGET} / {BUYER}: first read ({weekday} {date})
{Only if something failed: "Not available: {tool or source}, so {what is missing}."}

**Call: BUY UP TO $X | STARTER UP TO $X, ADD ON {fact} | WAIT FOR {fact or price} | PASS.** {At most three sentences: what the gap pays per year, what the price implies against the risks below, and what would change the call.}

**Numbers.** Offer {x}; last {price} ({time}); gap {$ and %}; annual return {r}% to {expected date}; price if the deal fails {L} ({basis}, range {a} to {b}); market-implied chance of failure {x}% with no return for waiting.

**Risks at a glance**
1. {Who can do what, and what happens to the deal} - {Resolved | Bounded | Blocked} - known by {event, date}
2. ...

**1. {Same headline}** - {status}
- What could happen:
- Why it can happen: [{source}]
- What it does:
- When we will know:
- Checked / still open:

{One block per risk, same order, at most six.}

**Unusual terms**
- {Term in plain words} - {how it differs, and from which agreement} - {what it could mean} - {Checked: ... | Open: ...}

**Cases** (dated outcomes; no probabilities of ours; arithmetic from `deal_clock.py cases`)
| Case | Date | Annual return at last price | Highest price that earns 7.5% on a clean close | Chance of failure the last price implies after paying 7.5% |
|---|---|---|---|---|
{Early, expected, delayed, deadline, deal fails. Each delayed case names its evidence. A negative implied chance is written "none: price is above the ceiling". The failing case shows the price if the deal fails and the loss.}
At {trigger price} a clean close on {expected date} earns {r}% and the implied chance of failure after 7.5% is {y}%. The last price earns 7.5% only for a close by {date}.

**Precedents.** {n comparable deals, median days to close, middle half; where our cases sit. Closest: deal, days, what it teaches.}

**What would change the call.**
- {Fact} → {action and price}

**Next events**
- {Date}: {event} - {what it would show}

---

## Research tree
{Each branch: the flag, the question, what the agents found with citations, outcome (risk, unusual term, closed with reason, or open), child branches, `View:` lines.}

## Terms
| Term | Detail | Source |
{Price and consideration, structure, conditions, efforts standard, both fees with % of equity value and EV and
payment mechanics, remedies, financing, no-shop and match rights, outside date, votes and support agreements,
rollover. Omit rows that are boilerplate for this deal.}

## Timeline
| Step | Deadline or earliest date | Outer limit | Basis |

## Not yet known
- *Not yet checked*: {item} → {where to look}
- *Not yet knowable*: {item} → {what settles it, expected when}
- *Assumed for this call*: {assumption}; if wrong, {effect on the call}

## Sources
{Primary documents used, with dates and accession numbers where practical.}
```

The call, the numbers and "Risks at a glance" fit on one screen. Every number has its basis next to it. The open
branches and "Not yet known" are the deeper review's work list, so make each one specific enough to act on.

## 5. Close out

Give the report in the chat; no file unless asked. Create the deal's living document from
`assets/living_doc_template.md`, including the research tree, and say where it is in one line. Offer the deeper
review in one line unless the call is PASS, and say that new information from brokers or the desk can be passed
in at any time (Update mode).
