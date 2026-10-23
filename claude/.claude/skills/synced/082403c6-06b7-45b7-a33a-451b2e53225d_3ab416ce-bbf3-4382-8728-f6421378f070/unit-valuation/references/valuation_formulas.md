# Unit Valuation Formulas & Edge Cases

Detailed computational reference for the `unit-valuation` skill. Read this when you need precision on edge cases, non-standard unit structures, or multi-unit batch processing.

For current marks, see `valuation_params.md`. Do not hard-code marks here — always read from that file.

---

## Input parsing

### Parsing right/warrant ratios

The `spac-details` MCP tool returns ratios in inconsistent formats. Normalize as follows:

| Raw input | Parse to |
|---|---|
| `"None"`, `None`, `0`, `"0"`, `""` | 0.0 (no right/warrant) |
| `"1"` | 1.0 (full instrument) |
| `"1/2"`, `"1/3"`, `"3/4"` | Evaluate fraction: 0.5, 0.333, 0.75 |
| `"1 for 1/4"`, `"1 for 1/5"` | Strip `"1 for "` prefix, parse fraction |
| Numeric string | Cast to float |

Implementation:

```python
def parse_frac(s):
    if s is None or s in ("None", 0, "0", ""): return 0.0
    s = str(s)
    if "1 for " in s:
        s = s.replace("1 for ", "")
    if "/" in s:
        a, b = s.split("/")
        return float(a) / float(b)
    try:
        return float(s)
    except ValueError:
        return 0.0
```

### Parsing dates

Liquidation deadline and IPO date come as ISO format `YYYY-MM-DD`. Use `date.fromisoformat()`. Reference "today" from the environment, not hard-coded.

### Months to liquidation

Use 30.44 days per month (average Gregorian month):

```python
months_to_liq = (liq_date - today).days / 30.44
```

Do not use 30 days or 365/12 — both introduce bias on long-dated units.

---

## Valuation formulas

### Pre-split unit

```python
common_fair = cit - months_to_liq * common_disc_per_month
right_val   = right_ratio * right_mark_per_1for1
warrant_val = warrant_ratio * warrant_mark_per_full
fair_unit   = common_fair + right_val + warrant_val
discount_pct = (fair_unit - unit_price) / unit_price * 100
```

### Post-split unit (reconciliation)

When the unit is post-split, constituent R and W trade independently. Fair unit should arb to the sum of live component prices:

```python
# live_common_price, live_right_price, live_warrant_price from Bloomberg
fair_unit_live = live_common_price + right_ratio * live_right_price + warrant_ratio * live_warrant_price
```

If the user is evaluating a post-split unit offer, compute both:
- `fair_unit_model` (using the marks)
- `fair_unit_live` (using live component prices)

Flag discrepancies — a large gap between the two indicates a mispriced component (often the right, which is illiquid).

---

## Edge cases

### Missing CIT

If `spac-details` returns `cash_in_trust` as `#N/A` or similar, check:
1. Is this an extending SPAC where sponsor has added trust top-ups? Use the most recent 10-Q or 8-K disclosure instead.
2. Is this a very new IPO not yet indexed? Default to $10.00 until the tracker updates.
3. Is the deal announced and redemption completed? Use the post-redemption trust figure.

### Non-standard unit structures

Some recent SPACs have unusual structures. Handle common variants:

- **Full warrant + fractional right** (AACPU, MYXXU, NOEM): parse both ratios, sum both contributions.
- **Fractional warrant + fractional right** (GTERA: 3/4 W + 1/10 R): parse both, sum.
- **Right with integer numerator > 1** (rare): e.g. "2 for 1/3" = 0.667 share per unit. Adjust parser if encountered.
- **Founder-funded trust premium** (CIT > $10.10 at IPO): use stated CIT, no adjustment.
- **Multiple rights per unit** (very rare): treat each right separately and sum.

### Sponsor-unrated ("bucket ?") SPACs

Brand-new IPOs and some off-beat SPACs don't have a bucket assigned in the tracker. Do NOT default to a bucket — mark as `?` and note in commentary that quality overlay is pending. Consider underwriter as a proxy for quality pending formal assignment:

| Underwriter | Implied tier |
|---|---|
| Goldman, Morgan Stanley, JPM, Citi | 1 |
| Jefferies, BTIG, Barclays | 2 |
| Cantor, Cohen, DBOR, Clearstreet, Santander | 3 |
| Maxim, AGP, Polaris, Kingswood, B Riley, ARC, Roth | 4 |

### Very short deadline (<6 months)

Common discount compresses at short deadlines because the holder is close to cash-out. Formula still produces reasonable output but flag these — they're often extension-risk plays where the sponsor is trying to buy time.

### Very long deadline (>24 months)

The linear $0.01/month model under-prices the discount on 24+ month units (convexity of yield). Flag these in commentary. A possible extension is a convex discount model:

```python
# Not implemented in current framework - documented here for future update
common_disc_convex = 0.01 * months_to_liq * (1 + 0.005 * max(0, months_to_liq - 18))
```

### SPAC with outside extension already funded

If the deadline has been extended and the sponsor paid per-share into trust, use the adjusted CIT. The `spac-details` tool includes the updated trust balance.

---

## Worked examples

### Example 1: AACPU (combo unit)

Inputs from spac-details and Bloomberg (2026-04-17):
- Unit price: $10.06
- CIT: $10.054
- Liquidation: 2027-07-08 (14.7 months)
- Right: "1 for 1/5" → 0.20
- Warrant: "1" → 1.00

Computation:
```
common_fair = 10.054 - 14.7 * 0.01 = 9.907
right_val   = 0.20 * 0.75 = 0.150
warrant_val = 1.00 * 0.25 = 0.250
fair_unit   = 9.907 + 0.150 + 0.250 = 10.307
discount_pct = (10.307 - 10.06) / 10.06 * 100 = 2.46%
```

### Example 2: TRAD/U (right-only)

Inputs:
- Unit price: $10.04
- CIT: $10.041
- Liquidation: 2027-05-27 (13.3 months)
- Right: "1 for 1/4" → 0.25
- Warrant: None → 0

Computation:
```
common_fair = 10.041 - 13.3 * 0.01 = 9.908
right_val   = 0.25 * 0.75 = 0.188
warrant_val = 0 * 0.25 = 0
fair_unit   = 10.096
discount_pct = (10.096 - 10.04) / 10.04 * 100 = 0.56%
```

### Example 3: BEBE/U (warrant-only, past separation window)

Inputs:
- Unit price: $10.00
- CIT: $10.114
- Liquidation: 2027-12-22 (20.2 months)
- Right: None → 0
- Warrant: "1/2" → 0.50
- DSI: 118 (past 52-day window but unit still trades — pre-split confirmed via Bloomberg check that BEBEWS doesn't resolve)

Computation:
```
common_fair = 10.114 - 20.2 * 0.01 = 9.912
right_val   = 0
warrant_val = 0.50 * 0.25 = 0.125
fair_unit   = 10.037
discount_pct = (10.037 - 10.00) / 10.00 * 100 = 0.37%
```

---

## Batch processing

For axe lists or universe screens, run the formula across all candidates in a Python script. Preserve input order for axe presentation but sort by `discount_pct` descending for the ranked table.

Recommended structure:

```python
rows = []
for unit in candidates:
    # pull data, compute fair, store dict
    rows.append({...})

# preserve order for axe display
for r in rows:
    print(...)

# sorted for ranking
rows.sort(key=lambda x: -x['discount_pct'])
for i, r in enumerate(rows, 1):
    print(f"{i}  {...}")
```

---

## Verification checks before presenting results

Before sending a valuation to the user, verify:

1. **Component ratios parsed correctly.** "1 for 1/4" should yield 0.25, not 4.0 or 0.04.
2. **Months calculation uses 30.44.** Off-by-a-month on 24-month deadlines changes fair by $0.01.
3. **Pre/post-split status verified via Bloomberg.** Don't assume based on DSI.
4. **CIT is not `#N/A` or stale.** If it looks off, cross-check against the SPAC's most recent 10-Q.
5. **Position data included.** A screen without position columns is incomplete — pull from spac-details.
6. **Sensitivity noted.** Add commentary on how ±$0.25 right mark or ±$0.10 warrant mark would shift the ranking.

If any verification step fails, flag it in the output rather than silently producing possibly-wrong numbers.
