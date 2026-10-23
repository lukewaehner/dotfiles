# Entry Price to Target IRR — methodology (v5 addition)

This block runs every time this skill produces a Gross Spread Calculation — it is a required
sub-block of that section, not optional polish. It answers a different question than the existing
Annualized Gross Spread line: not "what does today's price imply," but "what price would this need
to trade at to clear a target return." Skip cleanly, with one line saying so, only for private-target
deals or where no live equity price is obtainable.

## Always a fresh calculation

**Pull a live spot price for this block specifically, every run — never reuse a spread computed
earlier in this conversation, even if this exact deal was priced minutes ago.** State the pull's
timestamp next to the current gross spread line. This is a hard requirement: a stale spread produces
a stale implied entry price, and the whole point of this block is that it's checkable against the
market at the moment the report is read.

## Three scenarios, derived from this report's own working close date — never a fixed generic range

Run the calculation at exactly three close-date scenarios:

- **Baseline** — this report's own precedent-informed working close-date estimate (the date named in
  the Overall Risk Assessment / Deal Completion Probability prose, built per
  `house-view-and-precedents.md`'s precedent-timeline-pull methodology).
- **Baseline − 30 days**
- **Baseline + 30 days**

Do not substitute an arbitrary or previously-used date range (e.g. a fixed 140/160/180-day set) —
the three dates must be derived from this specific deal's own working close-date estimate each time,
so they move with the analysis instead of staying static across different deals or re-runs of the
same deal as the working estimate itself shifts.

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

Annualized IRR at each scenario (existing convention — spread% × 365/days):
  Baseline − 30 ([N] days):  X.X%
  Baseline ([N] days):       X.X%
  Baseline + 30 ([N] days):  X.X%

Entry price / spread needed for [target]% IRR:
  Spread % needed = [target]% × (days / 365)
  Spread $ needed = deal price × spread% needed
  Implied entry price = deal price / (1 + spread% needed)
```

Present as a table:

| Timeline | Spread % needed | Spread $ needed | Implied entry price |
|---|---|---|---|
| Baseline − 30 ([N] days) | | | |
| Baseline ([N] days) | | | |
| Baseline + 30 ([N] days) | | | |

## The Read — required, not optional, in this exact shape

Every run of this block ends with a "Read" paragraph. A Read that only restates the table in prose
does not satisfy this requirement — it must do all four of the following, in order, in the same
paragraph or a tightly connected pair of sentences:

1. **State the dollar entry-price range** across the three scenarios in one clause (e.g. "to
   underwrite an X% IRR you'd need [TGT] to trade roughly $A–$B below the current $C mid").
2. **State the directional relationship explicitly** — longer duration needs a wider dollar discount
   for the same annualized return (or the reverse, if the slope runs the other way for a
   deal-specific reason — say so and why).
3. **Compare current live pricing's implied annualized return against the target hurdle**, and say
   what that comparison suggests about the market's implicit read (e.g. pricing for a clean/fast
   precedent scenario; pricing in real completion risk; sitting between the two).
4. **Name a specific tail risk or precedent from elsewhere in this same report** (a named comparable
   deal from the precedent set, a named regulatory scenario, a named open item) and state plainly
   whether the current spread appears to price it in or not.

Register: direct and specific, the way a trading desk actually talks about a position — name a level,
don't hedge into an adjective-only conclusion. This paragraph sits immediately after the table and
before (or as part of) the Gross Spread Calculation block's closing verdict sentence — it does not get
its own new top-level section.
