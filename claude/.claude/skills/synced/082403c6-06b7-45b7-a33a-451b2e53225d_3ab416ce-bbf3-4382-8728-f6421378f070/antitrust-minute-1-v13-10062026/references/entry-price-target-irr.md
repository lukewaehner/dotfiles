# Entry Price to Target IRR — methodology

This block runs every time this skill produces a memo — it is a required component of Section G
(Entry Price to Target IRR), not optional polish. It answers a pricing question this module
previously scoped out entirely ("This module never pulls a price" / "no market pricing by design" —
both superseded specifically and only for this block; every other scoping boundary in this skill is
unchanged). Skip cleanly, with one line saying so, only for private-target deals. Where no live equity
price is obtainable, use the price fallback described below instead of skipping.

## Lead with one named level, in the desk's own vernacular, before the table

**Section G opens with a single, concrete, named price level — not the table.** The formal
three-scenario table and the four-part Read (below) still run in full, in order, immediately after —
this is not a substitute for the rigor, it is a headline placed in front of it. The reason: a reader
scanning this memo at speed does mental math the way a trading desk actually does it, not the way a
spreadsheet does it, and a section that makes them wait for a table before getting an actionable number
has buried the lede. Live feedback on an earlier version of this module made exactly this point —
a section that led with methodology before a level "wasn't read" by a desk reader working off a phone at
7:45am, independent of the quality of the analysis underneath it.

**The convention:**

```
spread% ≈ (deal price / current price) − 1
rough annualized read ≈ spread% × 2   [a fast desk-side proxy for "double the raw spread," not a
                                        substitute for the formal ×365/days annualization below —
                                        it approximates the common case where the working timeline
                                        is roughly six months; state the actual day count alongside
                                        it so the approximation is checkable]
```

State it as one sentence, in front of everything else in Section G: **"At today's [$X.XX] print
against a [$Y.YY] deal price, that's a [Z]% raw spread — call it [Z×2]% annualized on the desk's
quick math. [TGT] at [$W.WW] or better is where this starts clearing an [target]% hurdle on the
memo's own base-case timeline."** Name the specific price level the desk would actually want to see
before the trade clears the formal hurdle — this is the same number the baseline row of the table
below will produce, stated first, in the register a reader can act on immediately, before the table
walks through how it was derived. Do not let this headline sentence substitute for the table or the
Read that follow — it is a fast-reader's summary of where they land, not a replacement for showing the
work.

**When the print is far from the hurdle level** (for example a stale or pre-announcement price sitting
well below the level that clears the hurdle): the headline sentence's "at $W or better" wording and the
Read's "$A–$B below the current mid" wording both assume the print is above the hurdle price. Reverse
them honestly — say the print is already below the level that clears the hurdle, that the raw spread
therefore likely reflects a stale or pre-announcement price, and give the hurdle prices as the level the
tape should settle toward. Do not force the template sentence.

## v12 additions: calculator, price fallback, and the spread split

- **Use the calculator.** `scripts/deal_clock.py spread`, `implied`, `hurdle`, `decompose` and `downside` produce every
  number in this block, in the house format (spread % needed = IRR x days / 365; spread $ = deal price x spread %;
  implied entry = deal price / (1 + spread %)). Quote its output. The table still shows day counts only.
- **Price fallback.** Live tool, then a user-pasted price, then a desk price from a note in the chat. If none exists,
  produce the **price-independent hurdle table** (spread and day count needed to earn the target IRR at several
  prices, from `deal_clock.py hurdle`) and say in the first line of Section G that no live price was available.
- **Spread split.** After the Read, add one short paragraph from `references/spread-pressure-supply.md`: time value,
  technical premium and risk premium, in words, with the buyer-side check when the buyer is down more than about 5%.

## Always a fresh calculation

**Pull a live spot price for this block specifically, every run — never reuse a spread computed
earlier in this conversation, even if this exact deal was priced minutes ago.** State the pull's
timestamp next to the current gross spread line. This is a hard requirement: a stale spread produces
a stale implied entry price, and the whole point of this block is that it's checkable against the
market at the moment the memo is read.

## Three scenarios, derived from this memo's own constructed timeline — never a fixed generic range

Run the calculation at exactly three close-date scenarios:

- **Baseline** — this memo's own working close-date estimate from **Section E.2's Approval Clock
  Build** (the longest approval chain plus a closing tail), as reconciled in Section E.4 and
  sanity-checked against Section F's clearance handicap. On a sector-gated deal the build governs;
  do not substitute the precedent average or the midpoint of the parties' guidance. Use the base-case
  scenario as baseline unless the memo's own prose names a different scenario as its central
  estimate.
- **Baseline − 30 days**
- **Baseline + 30 days**

Do not substitute an arbitrary or previously-used date range (e.g. a fixed 140/160/180-day set) — the
three dates must be derived from this specific deal's own working close-date estimate each time, so
they move with the analysis instead of staying static across different deals or re-runs of the same
deal as the working estimate itself shifts.

**State the Baseline as an explicit calendar date wherever it is named in prose** (e.g. "Nov. 30,
2026"), never as a vague relative description ("late November", "early Q4", "toward year-end").
This calendar-date requirement is for prose only — the Entry Price to Target IRR table's Timeline
column (below) shows day counts alone (e.g. "Baseline − 30 (82 days)") and never carries a calendar
date.

## Target IRR: 8% default, always parameterized

The default annualized-IRR hurdle is **8%**. This is a default, not a fixed constant — if the user
specifies a different target rate, recompute at that rate instead and say so. State plainly, every
time this block runs, which hurdle rate was used ("target IRR: 8% (default)" or "target IRR: X% (per
request)").

## The math

```
Current gross spread (fresh pull, [timestamp]):
  [TGT] current price:  $XX.XX
  Deal price:            $XX.XX
  Gross spread:           $X.XX (X.XX%)

Annualized IRR at each scenario (spread% × 365/days):
  Baseline − 30 ([N] days):  X.X%
  Baseline ([N] days):       X.X%
  Baseline + 30 ([N] days):  X.X%

Entry price / spread needed for [target]% IRR:
  Spread % needed = [target]% × (days / 365)
  Implied entry price = deal price / (1 + spread% needed)
  Spread $ needed = deal price − implied entry price   [derive it this way so the table's columns tie]
```

Present as a table:

| Timeline | Spread % needed | Spread $ needed | Implied entry price |
|---|---|---|---|
| Baseline − 30 ([N] days) | | | |
| Baseline ([N] days) | | | |
| Baseline + 30 ([N] days) | | | |

## Ticking fees — a required second table where one exists

Where the merger agreement provides for a ticking fee (consideration accruing after a stated trigger
date, typically where named regulatory approvals remain outstanding), the fixed-consideration table
above **systematically understates the return in exactly the scenario the fee was negotiated to
address** — the slow one. Fix that with a second table rather than a sentence.

Compute the **effective consideration** at each of the three scenario dates:

```
Effective consideration at close date D:
  accrual_days   = max(0, D - trigger_date)   [capped at any stated accrual end date]
  effective_px   = deal_price x (1 + accrual_rate x accrual_days / 365)
                   [use the agreement's own convention if it compounds or pays differently]
```

| Timeline | Accrual days | Effective consideration | Spread % needed | Spread $ needed | Implied entry price |
|---|---|---|---|---|---|

Then state the comparison plainly: **an accrual rate at or near the target hurdle substantially
neutralises duration risk inside the accrual window**, because the consideration grows at roughly the
rate the holder is discounting at. That is a different trade from a fixed-price deal with the same
nominal spread, and the Read must say so rather than leaving the reader to notice it.

Three honesty rules. **Where the trigger date is not yet disclosed** — common at T+0 before Ex-2.1
files — say so, run the fixed-consideration table alone, and flag the fee's trigger date as the
highest-value missing input rather than assuming one. **Where the accrual has an end date**, show
where protection stops: past that point the holder is exposed to duration again with only the outside
date as backstop, and if a scenario falls beyond it, say which one. **Do not treat the fee as
certain** — it accrues only on its stated trigger, which is usually specific named approvals rather
than delay generally.

## The Read — required, not optional, in this exact shape

Every run of this block ends with a "Read" paragraph. A Read that only restates the table in prose
does not satisfy this requirement — it must do all of the following, in order, in the same
paragraph or a tightly connected pair of sentences (item 5 applies only where a ticking fee exists):

1. **State the dollar entry-price range** across the three scenarios in one clause (e.g. "to
   underwrite an X% IRR you'd need [TGT] to trade roughly $A–$B below the current $C mid").
2. **State the directional relationship explicitly** — longer duration needs a wider dollar discount
   for the same annualized return (or the reverse, if the slope runs the other way for a
   deal-specific reason — say so and why).
3. **Compare current live pricing's implied annualized return against the target hurdle**, and say
   what that comparison suggests about the market's implicit read on this deal's clearance odds.
4. **Name a specific precedent or risk factor from Section D, E or F of this same memo** (a named
   theory of harm, a named precedent transaction, the enforcement-posture row, or — on a sector-gated
   deal — **the named critical-path regulator from Section E.2's Approval Clock Build**) and state
   plainly whether the current spread appears to price it in or not. On a sector-gated deal the
   critical-path regulator is usually the right thing to name, because it is the actual risk being
   compensated; naming a LOW-rated theory of harm there tells the reader nothing.
5. **Where a ticking fee exists, state its effect on the trade in one clause** — whether it offsets
   the duration risk the table just quantified, and where its protection stops.

Register: direct and specific, the way a trading desk actually talks about a position — name a level,
don't hedge into an adjective-only conclusion. This is the only place in this module where directional,
evaluative pricing language about the trade itself belongs; every other section keeps to the
completion-risk framing described in "Adopt the perspective of a prospective deal risk analyst" at the
top of this skill.

## Mandatory topping-bid / appraisal-claim discussion whenever the read concludes the spread is not attractive

**Whenever this block's own analysis — the Read's third element, comparing live pricing's implied
annualized return against the target hurdle — concludes that the current spread does not clear the
target IRR, or is otherwise not attractive on the memo's own math, add one short paragraph naming the
two standard ways a deal in that position could still become interesting despite the unattractive
spread.** Do not omit this because the assessment of either path is weak — a weak assessment stated
plainly is the required output; silence on the question is not. A reader evaluating an unattractive
spread is always implicitly asking "so why would anyone hold this," and the memo should answer instead
of leaving the reader to wonder whether the question was considered.

Assess both, briefly:

1. **A topping or competing bid.** Is there any disclosed or plausible basis for a higher offer —
   a named strategic or financial party with a disclosed prior interest, a go-shop provision still
   open, public reporting of other bidders during the process, or a standalone value case (sum-of-the-
   parts, precedent multiples) that makes the current price look light relative to what a full auction
   might produce? Where none of this exists, say so plainly ("no disclosed competing interest and no
   go-shop currently open — a topping bid would have to originate from a party with no public footprint
   in the process to date, which is a weak basis for the trade") rather than reaching for a generic
   "M&A happens" hedge.
2. **An appraisal-rights claim by dissenting shareholders.** Relevant on any statutory merger where
   dissenters' rights are available (state it explicitly where the deal structure involves a going-
   private or controller-affiliated transaction subject to an enhanced fairness or majority-of-the-
   minority framework, since those structures draw appraisal petitions more often than an arm's-length
   strategic deal). State briefly whether the deal's specific facts — a depressed or controller-
   influenced sale process, a valuation gap versus recent trading or precedent multiples, the presence
   or absence of a special committee and its independence — make an appraisal claim a plausible source
   of incremental value for a holder, or whether the process facts cut against one (a fulsome special-
   committee process, a market check, analyst fairness support). This is a completion-risk-adjacent,
   not a legal-advice, assessment — state it as a sourced, dated `Assessment:`, not as a prediction of
   litigation outcome.

Label this paragraph clearly (e.g. "Why this could still work despite the spread") so a reader scanning
for it can find it without re-reading the whole Read paragraph, and keep it to a few sentences per path
— this is a completeness check, not a new sub-analysis with its own sourcing burden beyond what the
rest of the memo has already gathered.
