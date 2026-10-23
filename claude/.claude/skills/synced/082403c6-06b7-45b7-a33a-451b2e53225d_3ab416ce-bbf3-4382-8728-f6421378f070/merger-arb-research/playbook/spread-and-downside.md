# Spread, downside and market-implied odds

Load when: you need the current spread, an annualized return, a break price, what the market is
implying about completion, why the spread is wider or tighter than the risk read suggests, or a buy level.

## Why it matters

The spread pays for time, for supply pressure, and for completion risk. A wide spread from forced selling
says little about deal risk, and a tight spread on an unseasoned tape may not be tested yet. The verdict
needs the upside, the downside, the timeline and an honest split of what the residual spread is paying
for. Run arithmetic through the deal clock calculator (`spread`, `implied`, `hurdle`, `decompose`,
`downside`, `adddays`) and quote its output.

## Inputs to fix first

- Price: live tool, then user-pasted (labeled, timed), then a note's quoted price (named). Never guess;
  with no price, give the hurdle in price-independent form (spread and days needed at several prices).
- Offer value: cash; or exchange ratio times live buyer price plus cash for stock deals; apply any collar.
  Treat a CVR separately (below).
- Dates: floor (contractual earliest close from the agreement's covenants and Business Day calendar),
  base (working close date), downside (refile, second request, or slow regulator scenario, with the
  evidence that triggers it). State each as a calendar date and days from today.
- Dividends: add target dividends expected before close, subtract buyer dividends the short pays on a
  stock deal.
- Risk-free rate: sourced, with source and date (for example the T-bill yield matching the holding
  period). The decomposition refuses to run without it.

## Spread and return

```
Gross spread $   = offer value - price
Gross spread %   = offer value / price - 1
Annualized       = spread % x 365 / days to close        (simple, pre-funding)
```
Show it at floor, base and downside dates. Label the annualized figure pre-funding; do not net out a
funding or borrow rate unless one is given.

Quick desk read: spread % roughly doubled approximates annualized on a six-month deal; always show the
actual day count beside it.

Hurdle line (one line, replaces any entry-price table): the close date at which today's price earns the
target IRR (`hurdle`), and the entry price that clears it on the base date:
```
Spread % needed  = IRR x days / 365
Entry price      = offer / (1 + spread % needed)
```
Desk hurdle 7.5% annualized unless the user gives another; say which was used.

Ticking fees: compute effective consideration at each date, offer x (1 + rate x accrual days / 365) from
the trigger date, capped at any accrual end, using the agreement's convention. An accrual rate near the
hurdle largely neutralizes duration risk inside the window; say where protection stops. If the trigger
date is not yet public, say so and run the fixed case.

## Premium and unaffected price

- Premium to the last unaffected close, and to 1-week and 1-month average closes (or VWAP), with the
  unaffected date stated. Check for leaks or rumor run-ups before the "unaffected" date and step back if
  needed.
- Also note the premium to the 52-week high and to the analyst target range when they frame the break
  case.

## Downside price

Estimate the break price with its basis and a range, never a single unexplained number.

- Unaffected price: last clean close before announcement or leak.
- Peer or index adjusted: unaffected price x (1 + peer basket or sector index move since the unaffected
  date). Name the basket.
- Multiple-based: unaffected EV/EBITDA or P/E applied to current estimates, reflecting any guidance cut
  or standalone deterioration since signing.
- Adjust for known damage or support: a reverse fee payable to the target on a regulatory break (per
  share, after tax if material), a business "melting" without the deal, new bidders or activist interest.
- When the unaffected price is stale (long pending deals), prefer the peer-adjusted or multiple-based
  number, or a sourced analyst downside, and say why.

Upside to downside: `downside` gives dollar upside, dollar downside and downside per $1 of upside.

## Market-implied probability

Ignoring carry:
```
Implied break probability      = (offer - price) / (offer - downside)
Implied completion probability = (price - downside) / (offer - downside)
```
Carry-adjusted, holding to the base date at the risk-free rate r over t years:
```
Implied completion = (price x (1 + r x t) - downside) / (offer - downside)
```
Show both, with the downside basis and the date and rate used. The carry-adjusted completion figure is
higher because part of the spread is time value. Run it at the downside price range to show sensitivity.
These are arithmetic on market prices; they are the only probability numbers allowed, and they never
substitute for the analyst's risk read. Set the two side by side and reconcile.

## From view to limit price

The trade call needs a price. Put the deal in a break-risk band (Low 3%, Moderate 7%, Elevated 15%, High 30%;
criteria in `modes/minute-1.md`), then run `deal_clock.py limit --deal D --downside L --asof T --close C
[--late C2] [--hurdle H] [--price P]`. The desk hurdle is 7.5% annualized. The limit is the expected value ((1 - b) x deal + b x downside)
discounted at the hurdle to the close date. Compare it with the price and print the market-implied break
probability beside the band. The downside moves the limit as much as the band does, so run the low end of the
downside range too.

## Splitting the spread

`decompose` gives time value = price x r x days / 365 and a residual. Divide the residual between
technical premium (supply) and risk premium (completion risk) in words only, citing the checks below,
for example "most of the residual looks technical: volume ran far above average, two downgrades to hold
at the deal price, and the regulatory read is unchanged". Never invent a percentage split.

Close with one line: spread is mostly time value, mostly technical, or mostly deal risk, and that points
wider or tighter if supply clears.

## Supply and technical checks

Run 1, 2 and 4 always; all of them when the buyer is down more than about 5% since announcement, the deal
is large, all-cash with a premium above about 30%, or a note explains a price move.

1. Size against liquidity: equity value, ADV, announcement-day volume as a multiple of ADV, days to turn
   the float. Large deals can exceed arbitrage capital.
2. Float and holder base: index funds and long-only holders likely to sell to arbs, sticky holders, and
   how crowded the arb community already is (13F and 13G filers known for arb, other live deals competing
   for the same capital).
3. Seasoning: share of ADV and of float traded since announcement. A spread on a thinly traded tape is
   less reliable; say so in the verdict.
4. Upside against downside, before any probability view.
5. Buyer stock: move since announcement, deal size against buyer market cap, equity raise against buyer
   ADV, pro forma leverage, rating actions, and commitment letter versus mandate letter. A falling buyer
   with committed financing is a price problem; with only a mandate, a financing problem.
6. Short interest as a share of float (with filing date) and borrow cost; hard-to-borrow buyer stock
   makes stock-deal spreads stay wide.
7. Sell-side supply: downgrades to hold at the deal price or dropped coverage push long-only selling.
8. Tape path days 1 to 10: widening on volume means supply; on thin volume, drift.
9. Index events: deletion dates and rebalances create dated selling; inclusion of the buyer in a stock
   deal can create buying.

Flag any driving number as single-source or chart-derived when it is.

## Stock deals, collars and CVRs

- Fixed exchange ratio: hedge by shorting ratio x buyer shares per target share; spread = ratio x buyer
  price - target price. Buyer borrow cost and dividends are part of carry. Heavy arb shorting can
  pressure the buyer around announcement and in the run-up to close.
- Fixed value with a collar: inside the collar the ratio floats and the hedge changes with price;
  outside it the deal behaves as fixed ratio. Model value at the collar edges and note the averaging
  period; hedge flows concentrate in it.
- Mixed consideration: value each leg, note proration and elections.
- CVRs: value separately by milestone, date, probability from sourced evidence, and discount; say
  whether they trade. Many arbs assign little value; show the spread with and without.

## Optionality if the deal breaks or is topped

- Topping bid: named prior interested parties, an open go-shop, reported other bidders, a light price
  against standalone value or precedent multiples, and a target termination fee at or below the low end
  of the 2 to 4% convention (less deterrence). Check matching rights and any voting or support agreements
  that lock up approval. Where none exists, say plainly that a topping bid has no visible basis.
- Process quality: a long gap between confidentiality agreement and signing, unanimous approval and one
  logical buyer can mean a thin market check; state it as a fact about optionality.
- Standalone trajectory: share loss or guidance cuts lower the break price over time.
- Appraisal: on cash statutory mergers, especially controller or going-private deals, appraisal can add
  value for some holders (see litigation-and-appraisal.md). State as `Assessment:`.
When the spread does not clear the hurdle, always say whether either path makes the position interesting.

## Second read from credit

If the target has public bonds, pull a price. Bonds moving toward the change-of-control put or
redemption price corroborate the equity read; bonds that have not moved, or moved away, diverge. One
line. Take put and redemption terms from the indenture.

## What tends to move spreads around events

Tighten: HSR expiry or early termination, foreign clearances, filed definitive proxy and set meeting
date, vote or written consent delivered, financing syndicated or bonds priced, marketing period started,
regulatory approvals ahead of guidance, a topping bid or rumor, index-deletion selling done.

Widen: second request, pull-and-refile, Phase 2 or in-depth review, a new regulator or state added to the
perimeter, agency speeches or suits on similar deals, buyer stock drop or downgrade, financing market
stress, target guidance cut or MAE chatter, litigation with an injunction motion, outside-date approach
without extension rights, large holders exiting, quarter-end or index selling.

## How to conclude

Last line: is the spread attractive, unattractive or fair at the base date given the downside and the
risk read, and at what level it becomes attractive ("attractive at $X or wider"). Name the specific risk
the spread does or does not appear to price (a named regulator, precedent or open item). Put forward-watch
items in risk bullets as specific triggers with dates.

## Common errors

- Reusing an earlier spread instead of a fresh, timestamped price.
- An implied probability without its downside basis and date.
- Using a stale unaffected price on a long pending deal with no peer adjustment.
- Calling a supply-driven widening a risk repricing, or the reverse, without the checks.
- Presenting annualized gross as a net expected return.
- Averaging broker close dates instead of using the built working date.
- Ignoring buyer dividends, borrow cost or collar mechanics on stock deals.
- Splitting the residual into invented percentages.
