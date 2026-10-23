# input.json schema for scripts/render_note.py

One bundle per ticker. Raw MCP payloads pass through untouched.

| Field | Type | Source | Notes |
|---|---|---|---|
| `ticker` | str | you | base common ticker (fallback if `spac_details.spac_ticker` missing) |
| `today` | str | you | `YYYY-MM-DD`, ET. Optional — defaults to system date. **Pass it** for reproducibility. |
| `thesis` | str | doc | distilled 3–4 sentences, or a fallback string (see thesis.md) |
| `non_managing_members` | str | doc | clause inside the quotes; `""` if silent; `none — wholly principal-funded` if confirmed |
| `sf4_count` | str / null | doc | in-deal only, e.g. `"2 (per memory doc)"`; `null` → prints `not in doc`; ignored pre-deal |
| `ext_per_share_per_month` | number | doc | `$/sh/mo`; `0` if none |
| `ext_active_since` | str / null | doc | `mm/dd/yyyy` for footer; optional |
| `ext_deposits_to_date` | int / null | doc | footer; optional |
| `ext_lump_period_days` | int / null | doc | set for per-period lump-sum cadence; else `null` |
| `ext_silent` | bool | you | `true` only when in-deal/post-anniversary AND doc silent on extensions |
| `spac_details` | obj | `spac-details` | raw payload |
| `prices` | obj | `get-price` | raw payload; must include `results[]` and `market_status` |
| `orders` | obj | `emsx-blotter` | raw payload; must include `orders[]` (nested `routes` ignored) |

## Payload fields the script reads

**spac_details:** `stage, spac_ticker, warrant_ticker, rights_ticker, unit_ticker,
domicile, underwriter, bucket, category, cash_in_trust, trust_balance,
common_outstanding, pct_9_outstanding, common_position, warrants_position,
rights_position, units_position, common_price, warrants_price, rights_price,
warrants_in_unit, rights_in_unit, vwap_5d, ipo_date, deal_announced, target,
deadline, outside_date, liquidation_deadline, ipo_proceeds, pipe_size,
est_date, six_month_date, nine_month_date, twelve_month_date, max_date`.

**prices:** top-level `market_status`; each `results[]` row: `ticker, bid, ask,
mid, bid_size, ask_size, last_trade, last_regular_close, _stale_warning`.

**orders:** each `orders[]`: `ticker, yellow_key, side, status, amount, filled,
remain_balance, avg_price, limit_price`.

## Run
```bash
python3 scripts/render_note.py input.json     # or pipe via stdin
```
Print stdout verbatim. Batch: one bundle per ticker (the shared `get-price`
payload may be reused across bundles); separate notes with a blank line and `---`.
