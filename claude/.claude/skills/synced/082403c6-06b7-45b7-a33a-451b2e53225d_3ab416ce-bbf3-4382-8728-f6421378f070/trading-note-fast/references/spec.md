# Deterministic spec implemented by scripts/render_note.py

This is the locked Meteora formatting/math spec. The model does NOT execute any
of this by hand — it lives in the script. Read this only to audit or modify the
script.

## Price selection ladder
Default is `mid = (bid+ask)/2`; fall back to `last_trade` when mid is unreliable.

**Common** — fall back to `last_trade` if ANY:
- absolute spread > $0.10, OR relative spread (ask−bid)/mid > 0.5%
- stub: `bid_size ≤ 500` or `ask_size ≤ 500` (numeric only; null size ignored)
- `|mid − last_regular_close| > $0.10` AND `market_status` is pre/after-hours
- payload `_stale_warning`

**Warrant / rights** (relaxed, sub-dollar) — fall back if ANY:
- relative spread > 25%
- stub (≤500 either side)
- `|mid − last_regular_close| > $0.10`

Last resort: sheet price (`common_price` / `warrants_price` / `rights_price`).
Suppress a warrant/right entirely if no price from any source. Bid/Ask are kept
raw for the matrix anchor columns even when the headline uses `last_trade`.

## T-bill
`USGG3M Index` value (mid, else last_trade, else bid) ÷ 100. If unresolved →
0.0366 and footer flags `(DEFAULT — live rate fetch failed)`.

## C-T
`selected_common_price − cash_in_trust`, signed, off the unrounded price.
Display half-up to 2dp with a leading `+`/`-`.

## Unit notation
`U=S` + `W` term + `R` term. `1/n` → `/n`; `1 for 1/n` → `/n`; `1`/`1 for 1` →
no denominator (`+W`); `None`/null/`0` → omit term. Unrecognized → literal `(spec)`.

## Yield (per price × scenario-date cell)
```
days        = (D − today).days                       # drop if ≤ 0
trust_accr  = cit · tbill · days/365
ext         = ext_pm · (days/30.4375)                # or ext_pm·floor(days/period) for lump
cit_exit    = cit + trust_accr + ext
yield       = (cit_exit/price − 1) · 365/days        # simple annualization
```
Format `#.##%`. Gross accrual + future extension deposits only (past deposits
already in CIT). No leakage. `price ≤ 0` or missing CIT → `--`.

## Yield matrix
- Center: `round(vwap_5d, 2)`; if `vwap_5d` is 0/null/<$1 → center on the rounded
  selected common price, column label `Px` (else `VWAP`), and footer notes the
  fallback.
- Columns (fixed order, no sorting): `−3c −2c −1c CENTER +1c +2c +3c Bid Ask`.
  Drop a step column priced ≤ $0; omit Bid or Ask if unavailable.
- Rows: scenario dates EST/6 MON/9 MON/12 MON/MAX in that order, days-to-exit > 0.
  Coincident dates collapse to a slash label (`EST/MAX`) in canonical order.
- Two header rows (labels, then `Price` dollar row), markdown pipes — Bloomberg-
  pasteable. Header annotation line sits above the table as plain text and carries
  `; w/ extensions ($X/sh/mo, per memory doc)` only when `ext_pm > 0`.
- < 2 price columns or no future rows → `Yield matrix unavailable — …`.

## ORDERS
- `WORKING` only; SELL block then BUY block; omit an empty block; omit the whole
  `---`/ORDERS section if no working orders.
- Sort within a block by ticker, then limit price ascending.
- Column widths picked once per render: **equity mode** (Ord/Fill/Rem=5, Avg=6,
  Lmt=5) if any working equity order has limit ≥ $1, else **option mode**
  (4/4/4/5/4). Contract field = 20.
- Row recipe: 6-char label prefix (`SELL: ` / `BUY:  ` / 6 spaces) + contract
  left-justified to 20, then for each column `" | "` + cell (header left-justified,
  data right-justified to width).
- Share counts: equity → k-notation (`25k`, `22.5k`, `<1000` raw); option → raw
  integer contract count.
- Avg = `0.000` (`--` if zero); Lmt = `0.00`. **BUY block omits Avg.**
- Contract name: equity → Bloomberg ticker as-is; option →
  `MM/DD/YYYY Cx` → `Mon D/YY Cx`.

## Suppression
- Invalid ticker (`0`/null/empty/`#N/A`) → drop that instrument from Tickers,
  Positions, AND Prices lines (no `N/A`).
- Valid ticker + zero holding → render `0` in Positions.
- Dom/UW/Bucket/Category: null → `N/A`, never suppress the line.
- `Non-Managing Members:` and `Thesis:` always render (absence is information).

## Footer
- `Yields computed @ Tbill = X.XX% (USGG3M), px = $X.XX` (+ `(last_trade — …)` when
  the common fell back; + `(DEFAULT …)` when the T-bill defaulted).
- `Extensions:` line when `ext_pm > 0` (or the deferral flag when `ext_silent`).
- Per-instrument `last_trade` note for warrant/right fallback.
- VWAP-fallback note, or `VWAP $X vs px $Y — tape moved …` when |VWAP − px| > $0.10.
