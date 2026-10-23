# SPAC Research Database — Schema Reference

**Source:** spacresearch.com native exports (All SPACs CSV + Sponsors)  
**Extracted:** 2026-07-15  •  **Built:** 2026-07-15T19:02:18.163951Z

Two base tables — **`spacs`** (one row per SPAC, all lifecycle stages) and **`sponsors`** (one row per sponsor vehicle, grouped into families) — plus helper views. Join on ticker: `spacs.spac_ticker = sponsors.ticker`.

## Tables

### `spacs`  (1815 rows)

| column | type | description |
|---|---|---|
| `spac` | TEXT | SPAC |
| `status` | TEXT | Status |
| `spac_ticker` | TEXT | SPAC Ticker |
| `warrant_ticker` | TEXT | Warrant Ticker |
| `newco` | TEXT | Newco |
| `newco_ticker` | TEXT | Newco Ticker |
| `filed` | TEXT | Filed |
| `ipo` | TEXT | IPO |
| `tenor` | TEXT | Tenor (months) — months |
| `unit_specs` | TEXT | Unit Specs |
| `warrant_specs` | TEXT | Warrant Specs |
| `right_specs` | TEXT | Right Specs |
| `trust_value` | REAL | Trust Value, $ — USD per share |
| `coverage` | REAL | Coverage, % — warrant coverage, % |
| `ipo_sector` | TEXT | IPO Sector |
| `ipo_geography` | TEXT | IPO Geography |
| `ipo_proceeds` | REAL | IPO Proceeds ($M) — USD millions |
| `announced` | TEXT | Announced |
| `deadline` | TEXT | Deadline |
| `closed` | TEXT | Closed |
| `ev` | REAL | EV ($M) — USD millions |
| `tev_ipo` | REAL | TEV/IPO |
| `merger_sector` | TEXT | Merger Sector |
| `merger_geography` | TEXT | Merger Geography |
| `redeemed` | REAL | Redeemed — % redeemed at merger |
| `common` | REAL | Common, $ — USD/share |
| `unit` | REAL | Unit, $ — USD/share |
| `warrant` | REAL | Warrant, $ — USD/share |
| `newco_common` | REAL | Newco Common |
| `newco_warrant` | REAL | Newco Warrant |
| `newco_warrant_ticker` | TEXT | Newco Warrant Ticker |
| `banker` | TEXT | Banker |
| `counsel` | TEXT | Counsel |
| `ipo_sector_focus` | TEXT | IPO Sector Focus |
| `premium` | REAL | Premium (premium=positive; discount=negative) — % vs trust (positive=premium, negative=discount) |
| `liquidating_trust_value` | REAL | Liquidating Trust Value |
| `return_at_liquidation` | REAL | Return at Liquidation — % |
| `structure` | TEXT | Structure |
| `min_cash` | REAL | Min Cash ($M) — USD millions |
| `pipe_fpa` | REAL | PIPE+FPA ($M) — USD millions |
| `trust_cash_remaining` | REAL | Trust Cash Remaining ($M) — USD millions (total) |

### `sponsors`  (1181 rows)

| column | type | description |
|---|---|---|
| `family` | TEXT | Family |
| `name` | TEXT | name |
| `spac` | TEXT | SPAC |
| `root_symbol` | TEXT | rootSymbol |
| `ticker` | TEXT | Ticker |
| `officers` | TEXT | Officers |
| `type` | TEXT | Type |
| `status` | TEXT | Status |
| `target` | TEXT | Target |
| `market_cap` | TEXT | Market Cap — USD millions |
| `sector` | TEXT | Sector |
| `geography` | TEXT | Geography |
| `common` | TEXT | Common — USD/share |
| `common_change` | TEXT | commonChange |
| `oldcommon_price` | TEXT | oldcommonPrice |
| `common_stock_split` | TEXT | commonStockSplit |
| `warrant` | TEXT | Warrant — USD/share |
| `warrants_change` | TEXT | warrantsChange |
| `redemptions` | TEXT | Redemptions — % redeemed |

## Views

- `v_closed`
- `v_franchise`
- `v_liquidated`
- `v_live_deal`
- `v_pre_deal`
- `v_pre_ipo`
- `v_stalled`

- `v_live_deal`, `v_pre_ipo`, `v_pre_deal`, `v_closed`, `v_liquidated`, `v_stalled` — `spacs` filtered by `status`.
- `v_franchise` — `sponsors` LEFT JOIN `spacs` on ticker: family, officers, redemptions + live market data.

## Notes & gotchas
- **Dates** (`filed`,`ipo`,`announced`,`deadline`,`closed`) are the site's `M/D/YYYY` strings.
- **`trust_value`** is per-share (~$10–11); **`trust_cash_remaining`** is total $M. Use `trust_value` for discount/premium math.
- **`premium`** already equals price-vs-trust (the Franchise Book "vs Trust" column).
- **`status`**: pre-ipo, pre-deal, live-deal, closed, liquidated, stalled (stalled = broken/terminated).
- Some `sponsors` rows have no matching `spacs` row (delisted/older) → NULLs on the joined side.
