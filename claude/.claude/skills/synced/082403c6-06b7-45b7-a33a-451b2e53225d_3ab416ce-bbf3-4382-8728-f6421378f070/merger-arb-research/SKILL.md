---
name: "merger-arb-research"
description: Research framework for merger-arbitrage trade decisions on public-company M&A. Works out what a deal turns on, sends parallel research agents across public sources, and returns a short layered trade call (buy or not, up to what price, dated cases, ranked risks, precedents, what is unknown), kept in a per-deal living document. Modes - Rumor (pre-announcement), Minute-1 (first read), Hour-1 (deep research), Spread check (why a spread moved), Update (folds new information such as a broker note, desk discussion, filing or passed date into the living document and revises the call). Use whenever the user names an announced or pending merger and asks for minute-1, hour-1, a first read, a rumored deal, a deep dive, antitrust or other regulatory risk, merger agreement terms, closing timeline, spread, downside, or whether to participate, and whenever they pass along new information on a deal already being researched, even if they don't name the skill. Replaces antitrust-minute-1, dma-minute-1 and merger-hour-1.
---

# Merger Arb Research

The reader is a trader deciding whether to put risk on a merger spread. Every piece of work answers one
question: **is the spread paying enough for the risks between today and the close, and what could move it on
the way?**

This skill is a way of reading a deal. It does not list checks to run, because the mechanic that decides one
deal may not exist in the next. The method is the one an experienced analyst uses: read the documents, notice
what is unusual or consequential, work out what it could mean, and follow each lead until it either moves price
or date or plainly does not.

## How to research: read, flag, follow

### 1. Read the documents that set the deal

Read the primary documents in full, giving long ones to an agent: the merger agreement, the announcement and
investor deck, the target's latest 10-K and 10-Q, any support or voting agreements, and the buyer's most recent
comparable merger agreement. In the same wave pull the live price, the unaffected price and the precedent set
(`arbjournal-precedents` and comparable deals on EDGAR). If the deal already has a living document, read it
first and start from its research tree.

### 2. Flag what could matter

While reading, flag any line or fact that does one of three things.

- **It differs from the norm.** Compare it with the buyer's own last comparable agreement (`edgar-redline`
  where possible) and with market practice. Every negotiated departure exists because one side asked for it.
  Ask who asked and what they were protecting against. That answer is often the finding.
- **It touches what the spread depends on.** Whether the deal closes; when it closes; who controls the exit
  (who can walk, what it costs them, and how fast that cost is paid); what the shares are worth if it fails;
  and who outside the two parties can interfere (regulators, holders, courts, customers, lenders).
- **It conflicts with something else.** The deck against the 10-K, guidance against the contractual clock,
  the press release against the agreement, management's list of competitors against the buyer's products.

A flag is cheap. Write it as one line:
*"§X says ... . It could matter because ... . If it does, the effect on price or date is ... . To find out: ... ."*
That line is a branch of the research tree.

The illustrations below come from different kinds of deal. They show how a line becomes a question. They are
not items to check on every deal.
- The target must give notice and wait before it can collect the buyer's break fee. What does the buyer gain
  from the wait? Can it hold the deal open after a block, and until when? Was the step in its last agreement?
- The buyer is excused from any remedy that touches its own products. Which of its products does it expect a
  regulator to look at, and what does the target's 10-K say about competing with them?
- The outside date is longer than in the buyer's last deal, or its extensions are tied to one condition. Which
  review were the parties sizing it for?
- Insiders keep their roles and reinvest equity. A going-private filing becomes likely, and with it a longer
  SEC review.

### 3. Follow each branch

For each branch, decide whether any answer could move the call. If none could, close it in one line with the
reason. If one could, send the branch where the answer lives (`playbook/research-angles.md` lists the kinds of
source), usually as a parallel agent. Each answer that comes back does one of three things:
- **Closes the branch**: it does not matter, with the fact, clause or precedent that shows it.
- **Becomes a risk or an unusual term in the report**: it moves price, date or the exit.
- **Opens new branches**: write the next questions it raises and keep going.

Stop a branch when no plausible answer would change the price you would pay or the date you expect. Stop the
loop when no open branch can.

Record the tree in the living document (section "Research tree"): each branch with its flag, question,
evidence, outcome and child branches. The next session reads it to see what was checked and why.

### 4. Decide and report

Run the price test, set what the price implies against the risks the tree produced, make the call, and say what
is still open.

### Domain notes

The `playbook/` files hold the rules, thresholds and traps for a subject. Open one when a branch reaches that
subject. The files explain how things usually work; the branches decide what to look at. Where a mode file or
playbook file lists checks, treat them as places a branch may lead.

`agreement-reading` (efforts, fees, remedies, material adverse effect, conditions), `timeline-and-dates`,
`competition`, `regulatory-clocks`, `foreign-approvals`, `national-security`, `state-healthcare`,
`financing-and-buyer`, `litigation-and-appraisal`, `spread-and-downside`, `precedents-and-sources`,
`research-angles`. At the end of a deeper review, read `second-look.md` to find branches you have not opened.

### Briefing a research agent

Launch independent agents in one turn. Each brief gives the branch (the flag and the question), why it matters
to the spread, what is already known with sources, two to four places to look plus "anywhere else the evidence
points", the invariants below, and the work folder. Ask for: the answer; Resolved, Bounded or Blocked; the
evidence with citations; confidence; and new branches it opened. If no subagent tool is available, work the
branches yourself and say so in one line at the end of the output.

## Modes

| Mode | When | Time | Read |
|---|---|---|---|
| **Minute-1** | Deal just announced (including pre-market). Ends in a trade call with a buy price and the open branches for Hour-1 | 5-10 min | `modes/minute-1.md` |
| **Hour-1** | After Minute-1. Follows the branches the trade turns on, then confirms, resizes or reverses the call | 30-60 min | `modes/hour-1.md` |
| **Rumor** | Deal reported or expected but not announced. How real it is, likely buyers and terms, slow research done now, a pre-priced call per scenario | 20-40 min | `modes/rumor.md` |
| **Spread check** | The spread on a known deal widened or narrowed. Cause, whether risk changed, buy and exit levels for a short-term trade | 2-5 min | `modes/spread-check.md` |
| **Update** | New information on a deal already researched: a broker note, a desk or internal discussion, a filing, a milestone or a date passing. Logs it, checks it, moves the risks and the call | 2-10 min | `modes/update.md` |

"Minute-1 / first read / worth a look" → Minute-1. "Hour-1 / deep dive / what did we miss / should we
participate" → Hour-1 (run Minute-1 first if none exists). "Spread widened / why did it move" → Spread check.
"Rumored / in talks / exploring a sale" → Rumor. "Here is a note from {broker} / the desk thinks / the proxy is
out / {date} passed" → Update. A broker or desk input is also a source of flags: test each claim against the
agreement, and if it names a term we did not flag, open a branch and say in the report that we had missed it.

## Output

Write the report in the chat, top layer first and depth below a line. Create a file only when the user asks,
then write it from the same text; a request for a format (Word, PDF, a Claude Doc) gets that format. Every line carries a number, a date, a clause or a source; cut any sentence
that does not. The first-read and deeper-review templates in `modes/` follow this order; the Update mode keeps its short
format, with risk changes written as headline lines.

1. **Call**: the action and the buy price or trigger, plus at most three sentences on what the gap pays for and
   what decides it.
2. **Numbers**: one line with the offer, last price and time, gap, annual return to the expected closing date,
   price if the deal fails with its basis, and the chance of failure the market implies.
3. **Risks**: in the format below.
4. **Unusual terms**: in the format below.
5. **Cases**: the table from `deal_clock.py cases` (expected, delayed and deadline dates, and failure), with one
   line on the latest closing date at which the last price still earns 7.5%.
6. **Precedents**: set size, median days to close, where our cases sit, and the one to three closest deals with
   what each teaches. Say so here if the precedent tool failed.
7. **What would change the call**: specific facts, each with the price it implies.
8. **Next events**: dated, each with what it would show.

The call, the numbers and "Risks at a glance" fit on one screen, so a trader who stops there has the decision
and every risk by name. Below the line: the research tree for each deciding branch (flag, evidence, outcome, `View:` lines), then
terms, timeline and sources.

### Writing the risks

The mode templates and the living document template use this format.

Open with **Risks at a glance**, one numbered line per risk, ranked by effect on price or date:

`1. {Who can do what, and what happens to the deal} - {Resolved | Bounded | Blocked} - known by {event, date}`

Then one block per risk, in the same order:

```
**1. {Same headline}** - {status}
- What could happen: {the event, in plain words}
- Why it can happen: {the clause or fact, in plain words} [{source}]
- What it does: {effect on price in dollars, or on the closing date}
- When we will know: {event and date}
- Checked / still open: {what we confirmed; what we have not}
```

- The headline is a sentence with an actor and a consequence, such as "Salesforce can refuse a remedy and
  walk away for $300M". A category such as "regulatory risk" is never a headline.
- Each risk carries one mechanism. When a clause has two consequences (whether a fee is paid, and when), give
  each its own risk or unusual-term line so neither hides inside the other.
- Status: **Resolved** (the documents or facts settle it), **Bounded** (we know the range and the event that
  settles it), **Blocked** (the answer is not public yet; name the document where it will appear).
- Put no probability on a risk. Effects come from `deal_clock.py` or the documents.
- Show at most six risks in the chat. The rest go in the living document.

### Writing the unusual terms

List each term that differs from the norm or from the buyer's last comparable agreement, one line each:

`{Term in plain words} - {how it differs, and from which agreement} - {what it could mean} - {Checked: matters or does not, and why | Open: what settles it}`

Include terms that turned out not to matter, so the reader can see they were examined. If the comparison found
nothing unusual, say which agreement it was compared with.

## The call

- **Minimum return**: 7.5% a year unless the user gives another. The desk also trades short-term widenings
  (Spread check).
- **Probabilities**: the only one in a report is the chance of failure the market price implies, computed from
  the offer, the price and the price if the deal fails. Show it with no return for waiting and after paying
  7.5%, with the date used. With no return for waiting it is (offer - price) / (offer - price if the deal
  fails); the call uses the reading after 7.5%. Put no probability of ours on a closing date, a risk, a topping bid or a suit; the
  facts and which way they point carry the reasoning. Precedent statistics are facts about a set and may be
  quoted.
- **Price test** (`deal_clock.py cases`): give it the last price, one or two lower prices, the price if the
  deal fails and the expected, delayed and deadline dates. It prints the ceiling for each date (the highest
  price that earns 7.5% on a clean close then), the annual return at each price, the implied chance of failure
  after 7.5%, and dollars gained against dollars lost. Show the last price and the trigger price.
- **Making the call**: BUY or BUY UP TO a price when the implied chance of failure after 7.5% is higher than
  the risks support, naming the facts. STARTER, ADD ON a named fact when the price is near that line and one
  fact could settle it. WAIT FOR a price or a fact when the price implies less failure than the risks justify,
  including when it sits above the ceiling for the expected date. PASS when a risk is blocked and large. State
  the implied chance of failure at the trigger price so the reader can disagree.

## Invariants

- **Cite inline**: `[Agmt §8.3(b)]`, `[8-K 10/15/26]`, `[10-K FY25 p.47]`. A number in a table needs a source.
- **Facts flat, judgment marked**: judgment starts with `View:` and says what it rests on.
- **No invented numbers**: no made-up market shares, HHIs or clearance odds.
- **Keep the status of a finding**: "not disclosed", "not found after checking X" and "none" are different.
- **The agreement controls** over summaries. Say so at the top when they disagree. Read before saying "not found".
- **Dates and spreads run in `scripts/deal_clock.py`**. "Within X" is a deadline; "not before X" is a
  permission. Precedent friction builds later cases and moves the expected date only with named evidence.
- **Verify status** (filed or not, pending or settled) at the primary source.
- **Say what was not available**: name any tool or source that failed near the top, and retry before finishing.
- **Public information only**. Stop and flag anything that looks like material non-public information.
- **Plain English for the whole desk**: no internal labels, no filler, no "not X but Y" constructions, no em
  dashes without reason. Define a term of art in a clause the first time it appears and give the full name of
  every filing and regulator on first use. Internal notes are cited as "Meteora master document on CCC, Oct 15"
  and treated as leads. Before sending, apply this table:

  | Instead of | Write |
  |---|---|
  | Break-risk band, b | Not used; the market-implied chance only |
  | Limit | The highest price that earns 7.5% on a clean close on a stated date (ceiling) |
  | Working close / late case | Expected closing date / delayed closing date |
  | Downside | Price if the deal fails |
  | Implied break | The chance of failure the market price implies |
  | Hurdle | Our 7.5% minimum annual return |
  | Annualized | Annual return |
  | Minute-1 / Hour-1 | First read / deeper review |
  | HSR | U.S. antitrust waiting period (Hart-Scott-Rodino) |
  | PREM14A / DEFM14A | Preliminary / definitive proxy statement |
  | 13E-3 | Going-private disclosure filing (Schedule 13E-3) |
  | MAE / MAC | Material adverse effect clause (lets the buyer walk after a major business deterioration) |
  | Reverse fee | Break fee the buyer pays |
  | Specific performance | Court order forcing the buyer to close |
  | Rollover | Insiders reinvesting their shares in the buyer |
  | Marketing period | Window of N business days for the buyer's banks to market the debt |
  | Match right, fiduciary out, go-shop, clear skies, hell-or-high-water | Say what it does in one clause |

## Tools

Load deferred tools in one `ToolSearch` call at the start:

`select:mcp__MeteoraMCP-AWS__edgar-filings,mcp__MeteoraMCP-AWS__edgar-filing-index,mcp__MeteoraMCP-AWS__edgar-filing-text,mcp__MeteoraMCP-AWS__extract-8k,mcp__MeteoraMCP-AWS__extract-10k,mcp__MeteoraMCP-AWS__edgar-ownership-search,mcp__MeteoraMCP-AWS__edgar_company_facts,mcp__MeteoraMCP-AWS__edgar-redline,mcp__MeteoraMCP-AWS__arbjournal-precedents,mcp__MeteoraMCP-AWS__semantic-search,mcp__MeteoraMCP-AWS__docket-search,WebSearch,WebFetch`

Add as needed: `docket-details`, `caselaw-search`, `entity-neighbors`, `graph-search`, `research-search`,
`list-emails`, `read-email`, and the live price tool `mcp__MeteoraMCP__get-price`.
`playbook/precedents-and-sources.md` maps questions to tools.

- `edgar-filing-text`: `summary=true` first, then windows of 40,000 characters or less. If an exhibit lookup
  fails, use the exhibit's direct URL.
- Price: live tool, then a user-pasted price with its time, then a dated public quote. Never guess; with no
  price, print the date by which today's gap earns 7.5% (`deal_clock.py hurdle`).
- Download into `{TARGET}_work/` and check the company name on any agreement before quoting it.
- If an MCP server fails, say which and carry on by other routes.

## Living document

Each deal has one: `merger_arb_deals/{TICKER}/{TICKER}_living_doc.md` under the working folder (or a folder the user names), built from
`assets/living_doc_template.md` at the end of the first mode that runs on the deal. Its risks, unusual terms
and research tree (every branch with flag, question, evidence, outcome and children) use the formats above.

- Read it first in every mode and session on that deal.
- Update it last: the call, numbers, cases, risks, unusual terms, research tree, catalysts, the information log
  (each input, who it came from, what it was checked against, whether it held) and a dated changelog line.
- Keep working files in `{TARGET}_work/`. Send the living document only when the user asks, and say where it
  is.
- A Meteora memory doc is separate and is written only when the user asks.

## Files

- `modes/`: `rumor.md`, `minute-1.md`, `hour-1.md`, `spread-check.md`, `update.md`
- `assets/living_doc_template.md`
- `playbook/`: domain notes listed under "Domain notes"
- `scripts/deal_clock.py`: business days, tender clock, outside-date ladder, spread, minimum-return date,
  carry split, price if the deal fails, implied chance of failure, ceiling and dated cases (`cases`). Run
  `--help`.
