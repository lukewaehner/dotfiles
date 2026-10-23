# Spread Pressure and Supply — why a deal can trade below its fair spread

Read this file when Section G is being built, and whenever one of the triggers below fires. It answers a
question the clearance analysis cannot: **is the spread wide because of deal risk, or because more people
want to sell than want to buy?** A wide spread caused by forced selling is not a signal about completion
risk, and treating it as one gives the reader the wrong read in both directions.

The module is a set of checks that end in one split of the spread, stated in words. It never produces a
percentage probability and never estimates a figure it cannot source (house rule).

## When to run it

- **Always** a short version (Checks 1, 2 and 4) inside Section G.
- **Full version** when either trigger fires:
  - The buyer's stock is down more than about 5% since announcement. Run Check 6, the buyer-side check.
  - The deal is large, all-cash, and the premium is above about 30%. Run Check 1 and Check 3 with extra care, because that
    combination is the classic setup for index-fund and long-only holders handing shares to arbitrageurs
    faster than arbitrageurs can absorb them.
- When the user pastes a sell-side note explaining a price move, run the full version and test the note's claims
  against Checks 1 to 9.

## Price source order

1. The live pricing tool (`mcp__MeteoraMCP__get-price`).
2. A price the user pasted in this chat (say it is user-supplied, with its time).
3. A price quoted in a desk or broker note in this chat (say whose note and when).
4. If none of the three exists, do not guess. Produce the **price-independent hurdle table** (see
   `entry-price-target-irr.md`: the spread and the day count needed to earn the target IRR at several
   prices) and say in the first line of Section G that no live price was available.

## The nine checks

Each check states a fact, the test it feeds, and a verbal conclusion. A check with no data says "not
disclosed" or "not retrievable", never an estimate.

| # | Check | What to pull | What it tells the reader |
|---|---|---|---|
| 1 | Deal size against liquidity | Equity value; average daily volume (ADV); announcement-day volume as a multiple of ADV; days to turn the float at that volume | Whether the holder base can be absorbed by arbitrage capital without pushing the price down |
| 2 | Float and holder base | Free float; top holders and index funds; whether a large holder is a long-only or an index fund likely to sell to the deal price | Who is forced or likely to sell, and who is sticky |
| 3 | Premium and break price | Premium to the unaffected price; unaffected price adjusted for sector moves since the last unaffected close | How far the stock falls if the deal breaks. A high premium means a big downside leg |
| 4 | Upside against downside | Upside to deal price per share; downside to the adjusted break price per share; downside per $1 of upside (`deal_clock.py downside`) | Whether the risk/reward is acceptable before any probability view |
| 5 | Buyer stock reaction | Buyer move since announcement; deal size against buyer market cap; whether the buyer must raise equity and how that compares with its ADV; pro forma leverage; rating-agency actions; financing document wording: **mandate letter versus commitment letter** | A falling buyer with committed financing is a price problem. A falling buyer with only a mandate letter is a financing problem |
| 6 | Short interest and borrow | Short interest as a share of float (latest filing date); borrow cost if available | Whether shorts are crowding the stock or covering |
| 7 | Sell-side supply | Downgrades to hold at the deal price; analysts moving to "neutral" or dropping coverage | Long-only holders often sell when the rating changes, even if the deal is fine |
| 8 | Tape path, days 1 to 10 | Daily closes and volume against the deal price, as a day-count table | Whether the spread is widening on volume (supply) or on thin volume (drift) |
| 9 | Index events | Index deletion dates, likely index-fund selling, quarter-end rebalancing | Known future selling that can pressure the price on a specific date |

## The output: split the spread into three parts

Use `scripts/deal_clock.py decompose` for the first part.

1. **Time value** = risk-free rate x days to the base-case close / 365. The risk-free rate must be sourced
   (state the source and date). The calculator refuses to run without it.
2. **Technical premium** = extra spread caused by supply: forced sellers, thin liquidity, index selling,
   an over-extended arbitrage community. Judged from Checks 1, 2, 6, 7, 8 and 9.
3. **Risk premium** = extra spread the market is asking for deal-completion risk: regulatory, financing,
   shareholder vote, litigation. Judged from the clearance sections of this memo and Check 5.

The calculator gives the time value in dollars and the residual (technical plus risk). Divide the residual between
technical and risk **in words only**, for example "most of the residual looks technical, because volume was
nine times the average and the sell-side moved to hold, while the regulatory read is unchanged".
Do not invent a split in percentages.

## Verbal calls

Close the module with one line: "Spread is mostly time value / mostly technical / mostly deal risk, and
that points to [wider / tighter] if the supply clears." A reader should be able to act on this without
having to read the checks.

## Single-source flags

If a number that drives a call (ADV, short interest, float, holder percentage) comes from one source, or was
read from a chart, label it "single-source" or "chart-derived" next to the number. A call that rests on one
unverified number should say so.

## Worked example (PTC / Schneider, for calibration only)

Deal $205.00 cash, price $192.50: gross spread $12.50, 6.49%. Base close in 268 days: annualized 8.84%.
With a risk-free rate of 4.00% (an input for illustration only), time value is $5.65 and the residual is
$6.85. Downside to an adjusted break price near $144.06 is $48.44, so each $1 of upside carries $3.88 of
downside. Use real inputs on a live run.
