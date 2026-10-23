# Hour-1: follow the deal

Goal: confirm, resize or reverse the Minute-1 trade call, at what price, and say what to watch. Hour-1 takes the
open branches of the research tree and follows them the way the best analyst on the desk would: from several
kinds of source at once, each answer leading to the next question, until no open branch can move the buy price
or the date. Where the first read holds up, carry it forward in a line.

## 1. Start from what exists

Read the deal's living document (`merger_arb_deals/{TICKER}/{TICKER}_living_doc.md`), its research tree and the
first read in the chat. Re-pull anything marked "not yet filed": the agreement, the buyer's 8-K, a schedule, a
support agreement. Read everything pasted into the chat since: broker notes, desk chat, AlphaSense, emails. Pull
the inbox (`list-emails` / `read-email`) for notes on the ticker if the tool is available. Each new input is a
source of flags (SKILL.md, "Flag what could matter").

If there is no Minute-1, run it first (`modes/minute-1.md`, sections 1-3).

## 2. Re-read for flags the first read missed

The first read is fast and reads for the call. Before following branches, read the agreement once more against
the buyer's last comparable agreement, clause by clause (`edgar-redline` where possible), and against the
baselines in `playbook/agreement-reading.md`. Give the whole agreement to an agent if it is long. Every
difference becomes a flag, including differences inside a clause the first read already summarized: a step,
a notice period, a party who can or cannot act. Then set the open branches in order of how much they could move
the buy price or the date. Usually one to three decide the trade.

Phrase each deciding branch the way a PM would ask it, specific to this deal: "Will CFIUS require mitigation
beyond what Schneider's existing security agreement covers, and how long did its last review take?" A category
("regulatory risk") is not a branch.

## 3. Follow the deciding branches

For each deciding branch:

1. **Split it** into the questions an expert would ask next. The split comes from the facts of this deal: what
   the clause or fact says, why one side wanted it, what would have to be true for it to matter, and where that
   could be confirmed or ruled out.
2. **Pick sources** from at least three kinds in `playbook/research-angles.md` (the parties' filings, a
   regulator's register, precedent deals, the buyer's own history, procurement data, dockets, trade press,
   law-firm commentary). The obvious source is where everyone looks; the edge is usually in the second or third.
3. **Fan out.** One agent per question or cluster of sources, all in one turn, briefed as in SKILL.md
   ("Briefing a research agent").
4. **Follow what comes back.** Each answer closes the branch, becomes a risk or an unusual term, or opens child
   branches. Launch a further wave on child branches that could still move the answer. Stop when another wave
   would not change the buy price or the date, or after three waves.
5. **Land it.** For each deciding branch: the answer, its status, the two or three facts that carry it, and what
   it does to the trigger price and the dates.

If no subagent tool is available, follow the same tree yourself and keep the waves.

Status, written inline:
- **Resolved**: a primary source answers it. Give the answer, the citation and what it changes.
- **Bounded**: no source states it, but the governing test applied to sourced figures narrows it. Show the
  test, the figures and which way it points. Label it as judgment.
- **Blocked**: cannot be known yet. Name the document or event that will settle it and when.

A confidential schedule is never the final answer: derive the likely contents from the target's own filings
(revenue by country, sites by state, licences) and report that as Bounded beside the schedule.

## 4. Look for branches nobody opened

With the time left, read `playbook/second-look.md` as a prompt for branches the tree does not yet have. Open a
branch for each question that applies to this deal and follow it like the others. In the memo, list what this
sweep added and, in one line each, the questions that did not apply and why.

When a sell-side note is in the chat, test its claims and dates against primary sources
(`playbook/precedents-and-sources.md`, broker-note checks). If it raises a term we did not flag, open a branch
and say in the memo that the first read missed it.

## 5. Adversarial pass

Before writing, launch two subagents in one turn with the facts gathered so far (findings with citations, not
the draft):

- **Break case**: argue as hard as the evidence allows that the deal breaks, is repriced or slips past the
  outside date. Name the mechanism, the trigger, the date and the evidence. No invented facts.
- **Tighten case**: argue that the spread is too wide: the close comes earlier, the risks are overstated, or a
  higher bid is plausible. Same rules.

Read both. Anything either side raises that the memo does not answer is either researched or becomes a risk.
Say in the memo which arguments you rejected and why, in one line each.

## 6. Decision memo template

Write for the whole desk (SKILL.md, "Plain English for the whole desk"). Risks and unusual terms follow SKILL.md,
"Writing the risks" and "Writing the unusual terms".

```
# {TARGET} / {BUYER}: deeper review ({weekday} {date})
{Only if something failed: "Not available: {tool or source}, so {what is missing}."}

**Call: BUY / ADD UP TO $X | HOLD STARTER, ADD ON {trigger} | WAIT FOR {event or price} | CUT / PASS.** {At most three sentences: what the spread pays for, where we differ from the market and why, the risk we are underwriting.}
**Changed since the first read:** {one line each, or "no change to the call"}

**Numbers.** Offer {x}; last {price} ({time}); gap {$ and %}; annual return {r}% to {expected date}; price if the deal fails {L} ({basis}, range {a} to {b}); market-implied chance of failure {x}% with no return for waiting.

**Risks at a glance**
1. {Who can do what, and what happens to the deal} - {status} - known by {event, date}

**1. {Same headline}** - {status}
- What could happen:
- Why it can happen: [{source}]
- What it does:
- When we will know:
- Checked / still open:

**Unusual terms**
- {Term} - {how it differs, from which agreement} - {what it could mean} - {Checked: ... | Open: ...}

**Cases** (dated outcomes; no probabilities of ours; arithmetic from `deal_clock.py cases`)
| Case | Date | Annual return at last price | Highest price that earns 7.5% on a clean close | Chance of failure the last price implies after paying 7.5% |
|---|---|---|---|---|
At {trigger price} a clean close on {expected date} earns {r}% and the implied chance of failure after 7.5% is {y}%. The last price earns 7.5% only for a close by {date}.

**Precedents.** {n comparable deals, median and middle half of days to close; where our cases sit; closest deals and what they teach.}

**What would change the call.**
- {Fact} → {action and price}

**Next events**
- {Date}: {event} - {if good} / {if bad}

**Break case and tighten case.** {The strongest version of each in two lines; what we accepted, what we rejected and why.}

---

## Research tree
{One section per deciding branch, in rank order: the flag, the child questions, what each source found, the
waves that followed, with citations; then `View:` lines and what it does to the trigger price and the dates.
Then the closed branches, one line each with the reason they do not matter.}

## Added by the second look
{Branches the sweep opened and where they landed; one line each for questions that did not apply and why.}

## Where we differ from brokers or the desk
{Only real disagreements, each with the primary source that settles it or the reason it stays open.}

## Terms and timeline
{Carried from the first read and corrected. Mark anything changed with the source that changed it.}

## Not yet known
- *Not yet knowable*: {item} → {document or event that settles it, expected when, and what the call does if it goes each way}
- *Checked, could not resolve*: {item} → {what was tried, best bound}

## Sources
```

The call, the numbers and "Risks at a glance" fit on one screen.

## 7. Close out

Give the report in the chat, with no file unless asked, and update the living document: the call, numbers,
cases, risks, unusual terms, research tree, catalysts, open questions, the information log and a changelog line.
Offer one natural follow-up (for example a re-run when the proxy or a regulator filing lands).
