# Rumor: get ready before the deal is announced

Goal: when a deal is reported but not announced (a press report of talks, a strategic review, a 13D pushing for
a sale, a known bidder circling), work out what the deal would probably look like and do the research now, so
that when it is announced Minute-1 only has to check what differs and the desk can call it in minutes. Run the
research loop in SKILL.md, with the deal's shape as a set of scenarios instead of known terms.

Public information only. If anything in the chat looks like material non-public information (a tip from a
party, an adviser or anyone with a duty of confidence), stop, say so, and suggest compliance; do not research
or trade on it.

## 1. How real is it

- The report: outlet, reporters' record on deals, how specific it is (named buyer, price, timing, advisers),
  and whether it was confirmed, denied, or met with "no comment".
- What the company has said or filed: strategic review, adviser hires, 8-Ks, 13D amendments, poison pill,
  a Schedule 13D group forming, confidentiality agreements disclosed in past proxies.
- Prior attempts: earlier approaches, bids, standstills, failed processes (past proxies' Background sections,
  13D history, press).
- Market reaction: price and volume on the report.

Land it as a short `View:` in words on how ready an announcement looks and roughly when, with the evidence. No percentage.

## 2. Who would buy, and could they

For each plausible buyer (named in reports, past bidders, logical strategics, sponsors active in the sector):
strategic fit, balance sheet and financing capacity, stock currency, its own deal history and how it structures
deals, and anything that would make it a slow or risky buyer (regulatory history, foreign ownership, leverage).

## 3. What the deal would probably look like

Build two to four scenarios. For each: buyer, price range (reported price if any; otherwise premium norms for
the sector and deal type, prior bids, 52-week range, what the buyer can afford), consideration and structure
(cash or stock, tender or one-step, financing), and likely terms, taken from the buyer's own past merger
agreements where they exist (fees as a share of equity value, efforts and divestiture caps, outside date
length, reverse fee). Say which parts are reported and which are inferred.

## 4. Do the slow research now

This is where the time goes. The approvals and their clocks, the overlaps at product level, CFIUS or foreign
investment exposure, state or sector regulators, the buyer's record with those regulators, holder base and
likely vote dynamics, litigation exposure, financing feasibility. Send agents after the questions each
scenario would turn on, exactly as in Hour-1 (`modes/hour-1.md`, section 3). Most of this does not depend on
the final price, so it carries straight into Minute-1.

## 5. Pre-price the call

For each scenario: working close and late case (`deal_clock.py` from the expected covenant structure), downside
(unaffected price now, adjusted as needed), and the highest price that earns 7.5% on a clean close at each date (`deal_clock.py cases`).
Also say what the spread would need to be at announcement to be a BUY, so the desk knows its level the moment
terms print.

If the desk considers owning the target before announcement, show the deal and no-deal outcomes separately
(price if the deal is announced in each scenario, price if talks end). Do not put a probability on the announcement; show the two outcomes and what each is worth.

## 6. Output

```
# {TARGET}: rumor review ({weekday} {date})

**Readiness view.** {Two to three sentences: how ready an announcement looks and roughly when, the most likely
buyer and shape, and the one or two risks that would decide the arb.}

| Scenario | Buyer | Price | Structure | Expected / delayed closing | Highest price that earns 7.5% on a clean close (expected / delayed) |
|---|---|---|---|---|---|

**How we got there.** {Basis for the price ranges, and timing, one line each.}

**What the arb would turn on**
1. **{Question}.** {What we found, state, sources.}

**What we don't know yet**
- {Item} → {what settles it}

**What to watch for**
| Signal | Where | What it would mean |
|---|---|---|

---

## How real is it
## Buyers
## Scenarios and expected terms
## Research on the deciding questions
## Sources
```

## 7. Close out

Give the report in the chat, with no file unless asked, and keep the scenarios, the pre-priced limits and the
research in the deal's living document (SKILL.md, "Living document") so Minute-1 starts from it on announcement. Offer to watch for the signals listed.
