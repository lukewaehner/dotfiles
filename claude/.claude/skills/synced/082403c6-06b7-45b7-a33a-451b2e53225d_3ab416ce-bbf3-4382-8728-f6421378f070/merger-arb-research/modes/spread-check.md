# Spread check: the spread moved, why, and is it a trade

Goal: within a few minutes of a spread widening or narrowing, say whether the move carries information about
the deal or is flow, and if it is flow, give levels for a short-term trade: buy into the widening, sell into the
narrowing. The desk also takes these short-term trades on deals it already knows, so speed matters and the
answer can be short.

## 1. Measure the move

Current price and time, the price before the move, the spread then and now, annualized at the working close
(`deal_clock.py spread`), the buyer's stock if consideration includes stock, and the peers' spreads if the desk
tracks them.

## 2. Look for a cause (in this order, stop when one explains the move)

1. Deal news: new filings by either party (8-K, proxy, 13E-3, SC TO, 14D-9), regulator actions (second request,
   Phase 2, CFIUS extension, state notice), court filings, press and wires in the last day.
2. Buyer and financing: buyer stock move, buyer credit or financing news, debt market stress for sponsor deals.
3. Target business: target news, sector news that could reach the MAC carve-outs.
4. Flow and technicals: index deletion or addition dates, a broad widening across arb spreads (deleveraging),
   borrow changes, a large holder selling (Form 4, 13D/A), month-end or quarter-end.
5. Nothing found after checking all of the above: say so, with what was checked.

## 3. Classify and act

- **Information**: the move reflects a real change in risk or timing. Rerun the price test (`deal_clock.py cases`)
  and the dates, and say whether the call changes. Recommend Hour-1 on the new question if it
  is a deciding one.
- **Flow or no cause found**: the risk has not changed. Give the tactical trade:
  - *Buy level*: the trigger price from the price test (`deal_clock.py cases`), where the implied chance of failure after the 7.5% return exceeds what the risks support. Below it, the spread pays for the risk
    without counting on a quick reversal.
  - *Exit level*: the price at which the spread is back to where it traded before the move, or to the level the
    desk would no longer hold for carry (the 7.5% hurdle line), whichever comes first.
  - *Return if it reverts*: dollars and percent from buy to exit, and annualized over a stated holding period.
  - *What would make this wrong*: the event that would turn the widening into information.

## 4. Output

```
# {TARGET}: why the gap moved ({weekday} {date}, {time} ET)

**{INFORMATION | FLOW | NO CAUSE FOUND}.** {One or two sentences: what moved, why, and whether the risk changed.}
Gap to offer {before} → {now} (annual return {before} → {now} to the expected closing date). [price sources and times]

**Trade:** {BUY UP TO $X, EXIT AT $Y ({return}%, {annualized}% over {n} days) | HOLD | CUT | NO TRADE}
**Basis:** chance of failure the market implies {x}% (was {w}%), buy price ${X} where the implied chance after the 7.5% return is {y}% [deal_clock], exit price ${Y} = {basis}
**Checked:** {list of what was checked for a cause, with sources}
**Watch:** {the event that would turn this into information}
```

Answer in the chat, no file unless asked, and update the deal's living document (SKILL.md, "Living document") with the move, its cause and the levels, in the information log and the changelog.
