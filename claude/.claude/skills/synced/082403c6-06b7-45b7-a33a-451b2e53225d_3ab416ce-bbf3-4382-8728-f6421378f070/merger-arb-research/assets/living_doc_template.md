# {TARGET} / {BUYER}: living deal document

Last updated: {weekday date time ET}. Last mode run: {first read | deeper review | update | spread check | rumor}.
How to use this file: every mode reads it first and updates it last. The research tree (section 5a) shows what has been checked and why, so the next session starts from it. New information (broker note, internal discussion, filing, milestone) goes in section 9 and is reflected in sections 1 to 8 and the changelog (section 10). This is the deal's working record. It is not a memory document.

## 1. Current call
**{BUY UP TO $X | STARTER UP TO $X, ADD ON {fact} | WAIT FOR {fact or price} | PASS}.** {Price and date of the last price.}
- Trigger price: ${X}, where a clean close on {date} earns {r}% a year and the price implies a {y}% chance of failure after paying our 7.5% minimum return. Why that price: {facts}.
- Annual return at the last price if the deal closes on the expected date: {r}%; on the late date: {r2}%.
- What gets us to buy: see section 5.

## 2. The numbers
| Item | Value | Source |
|---|---|---|
{Offer, recent closes, gap to offer, annual return at the last price to each closing date, price if the deal fails with basis, chance of failure the market implies (arithmetic), short interest, holders.}

**What the market is paying for.** {One short paragraph: the closing date or required return or bid chance the last price assumes, found by testing a zero-failure price against our minimum return (`deal_clock.py hurdle`, `limit --breaks 0`).}

## 3. Cases (dated outcomes, no probabilities; arithmetic from `deal_clock.py cases`)
| Case | Date | Payoff | Annual return at last price | Highest price that earns 7.5% on a clean close | Chance of failure the last price implies after paying 7.5% |
|---|---|---|---|---|---|
{Early close, on schedule, short slip, delayed, outside-date squeeze, deal fails. Each late case names the evidence that puts it there.}

**Probabilities.** Only the chance of failure the market implies ({x}% with no return for waiting). We assume no chance of failure and attach none to a case or a risk; the register in section 5 carries the reasoning.

## 4. Dates
| Item | Date | Basis |
|---|---|---|
{Expected closing, delayed closing, tail, hard deadline, company guidance, early path.}

## 5. Risks (ranked by effect on price or date)
**Risks at a glance**
1. {Who can do what, and what happens to the deal} - {Resolved | Bounded | Blocked} - known by {event, date}

**1. {Same headline}** - {status}
- What could happen: {the event, in plain words}
- Why it can happen: {the clause or fact, in plain words} [{source}]
- What it does: {effect on price in dollars, or on the closing date}
- When we will know: {event and date}
- Checked / still open: {what we confirmed; what we have not}

{One block per risk, one mechanism per risk. The living document keeps every risk; the chat shows the top six.}

**Unusual terms**
- {Term in plain words} - {how it differs, and from which agreement} - {what it could mean} - {Checked: matters or does not, and why | Open: what settles it}

**What would change the call.** {Specific facts that would make us add, cut or exit, each with the price it implies.}

## 5a. Research tree
{One entry per branch, nested under the branch that opened it:}
- **{Branch}**: flag {the clause or fact, with source}; question {what we needed to know}; evidence {what we found, with citations}; outcome {risk n | unusual term | closed: why it does not matter | open: what settles it}
  - **{Child branch}**: ...

## 6. Precedents
{ArbJournal pull (`arbjournal-precedents`): set size, median and middle-half days to close, where our base and delayed cases sit. Closest cases table: deal, days to close, why it matters. Write "ArbJournal not available" with the reason if the tool failed, and retry later.}

## 7. Terms
| Term | Detail | Source |
|---|---|---|

## 8. Catalysts and open questions
| Date | Event | Status | If good | If bad |
|---|---|---|---|---|
{Status is Pending, Happened {date}, or Changed.}

**Open research questions.** {Numbered; each says what document or event settles it.}

## 9. Information log (inputs received, newest first)
| Date | Source and type | What it said | Checked against | Verdict | Effect |
|---|---|---|---|---|---|
{Source type: primary filing, company statement, broker note, internal discussion, press report, rumor. Verdict: held, partly held, contradicted, could not check.}

## 10. Changelog (newest first)
- **{weekday date time}.** {What changed in the call, dates, risks or numbers, and why; or "no change to the call".}

## 11. Sources
{Primary documents with dates and accession numbers; other sources with dates.}
