# Unit Valuation Parameters

**Last updated:** 2026-04-17

This file is the authoritative source for all valuation marks used by the `unit-valuation` skill. Update this file (not SKILL.md) when marks change.

---

## Current parameters

### Common stock discount

Common stock in a pre-deal SPAC is economically a cash-equivalent claim on trust at deal redemption or liquidation. Between now and that date, holders demand yield as compensation for carry and deal-failure tail risk. Low-quality sponsor commons empirically trade at this rate below CIT:

**`common_disc_per_month = $0.01`**

- 12-month SPAC → common = CIT − $0.12
- 18-month SPAC → common = CIT − $0.18
- 24-month SPAC → common = CIT − $0.24

Equivalent to ~115–130 bps annualized yield above T-bills after compounding. Fits observed post-split common prices on tier-3 and tier-4 sponsors.

### Right mark

A right converts to a fractional share at deal close. Value is expressed per **1-for-1-equivalent share** and scaled by the unit's right ratio.

**`right_mark_per_1for1 = $0.75`**

- 1/4 right → 0.25 × $0.75 = **$0.188 per unit**
- 1/5 right → 0.20 × $0.75 = **$0.150 per unit**
- 1/8 right → 0.125 × $0.75 = **$0.094 per unit**
- 1/10 right → 0.10 × $0.75 = **$0.075 per unit**
- 1/12 right → 0.083 × $0.75 = **$0.063 per unit**
- 1/15 right → 0.067 × $0.75 = **$0.050 per unit**

Observed market clearing is $1.00–$1.50 per 1-for-1 equivalent (GIXXR, GIWWR, KCHVR, etc). The $0.75 mark is deliberately conservative — fair values produced are therefore floors, not means.

### Warrant mark

Warrants are typically 5-year American calls struck at $11.50 with a $18.00 redemption trigger. In pre-deal SPACs trading at $10, these are OTM with significant time value bounded by the call trigger. Market clears $0.20–$0.35 across tier-3/tier-4 sponsors.

**`warrant_mark_per_full = $0.25`**

- 1/2 warrant → 0.50 × $0.25 = **$0.125 per unit**
- 1/3 warrant → 0.333 × $0.25 = **$0.083 per unit**
- 3/4 warrant → 0.75 × $0.25 = **$0.188 per unit**
- Full warrant (1) → 1.00 × $0.25 = **$0.250 per unit**

### Separation window

Default assumption for unit separation after IPO:

**`separation_window_days = 52`**

Used only as a heuristic. **Verify pre/post-split status via Bloomberg ticker resolution**, not DSI.

---

## Formula summary

```
months_to_liq = (liquidation_deadline - today) / 30.44

common_fair          = cit - months_to_liq * common_disc_per_month
right_value_per_unit = right_ratio * right_mark_per_1for1
warrant_value_per_unit = warrant_ratio * warrant_mark_per_full

fair_unit = common_fair + right_value_per_unit + warrant_value_per_unit
discount_pct = (fair_unit - unit_price) / unit_price * 100
```

---

## Parameter change log

| Date | Parameter | Old | New | Reason |
|---|---|---|---|---|
| 2026-04-17 | `common_disc_per_month` | n/a | $0.01/mo | Initial calibration from realized post-split common prices on low-quality sponsor tier |
| 2026-04-17 | `right_mark_per_1for1` | n/a | $0.75 | Conservative mark — actual clearing is $1.00–$1.50, deliberately below for floor valuation |
| 2026-04-17 | `warrant_mark_per_full` | n/a | $0.25 | Empirical clearing on tier-3/tier-4 pre-deal warrants at $11.50 strike |

---

## Planned framework extensions

The current framework is linear and treats all sponsors alike. Future extensions to consider (in order of priority):

1. **Sponsor quality adjustment.** Tier-4 sponsors have higher liquidation probability and thinner deal quality. Adding a `common_disc_quality_mult` that scales the monthly discount by 1.0× (tier 1-2), 1.25× (tier 3), 1.5× (tier 4) would capture this without breaking the framework.

2. **Right value by deadline proximity.** Rights near the deal vote should be worth more than rights on a brand-new SPAC because deal certainty is higher. A time-to-deadline discount on rights (e.g. 100% of mark within 6 months, 85% at 12 months, 70% at 24 months) would reflect this.

3. **Warrant mark by sponsor track record.** Sponsors with a history of deSPAC'd warrants going to zero should have warrants marked lower. Would require joining against a sponsor-deal-outcome dataset.

4. **Sector adjustment.** Crypto/DAT/AI themed SPACs see warrants spike post-announcement because retail chases the narrative. A sector-linked warrant premium might be warranted but is noisy.

5. **Deal-announced uplift.** Post-announcement, units should jump because rights become more certain and warrants gain deal-specific vol. Currently the framework treats pre-deal uniformly.

Do not implement these without broader calibration work. The current parameters are intentionally coarse to produce conservative floors.

---

## How to update this file

When marks change:

1. Edit the parameter value inline above
2. Update the "Last updated" date at the top
3. Add a row to the change log with old/new/reason
4. Do NOT touch `SKILL.md` or `valuation_formulas.md` unless the workflow itself changes

When adding a new parameter:

1. Add a new section above the "Formula summary"
2. Update the formula summary to show how the new parameter enters the fair calc
3. Document the parameter in the change log
4. Update `SKILL.md` only if the workflow needs to change to incorporate it
