# Ticker identity — matching a broker-report symbol to a pre-clearance symbol

The reconcile engine joins an approval to a trade on an **exact** normalized ticker. Brokers and
employees often write the *same* security two different ways (crypto especially, e.g. an approval for
`BTC` shows up on the statement as `BTC XYZ ABC`), so the engine would miss the match. To fix that,
**you** decide identity with reasonable judgement and record it in an alias map that the engine
applies deterministically.

## How it feeds the engine

While parsing (step 3/4), build `$W/identity_map.json`:

```json
{
  "BTC XYZ ABC": {"canonical": "BTC",  "reason": "same coin, decorated broker symbol"},
  "ETHUSD":      {"canonical": "ETH",  "reason": "crypto pair notation"},
  "BRK.B":       {"canonical": "BRKB", "reason": "same class B share, punctuation variant"}
}
```

Pass it with `--identity-map $W/identity_map.json`. The engine resolves **both** the approval
symbol and the report symbol through this map, so map every variant to **one** canonical form (prefer
the plain ticker the approval used). Always include a short `reason` — the map is part of the audit
trail. The map is used **only** to join an approval to a trade; restricted / SPAC / classification
still run on the reported symbol, so an alias can never hide a prohibited name.

## Scope: CRYPTO + MECHANICAL (locked)

Only two kinds of difference may be auto-joined. Everything else escalates.

### JOIN — crypto symbol variants (same underlying coin)
- Root vs decorated string that carries the root: `BTC` ≈ `BTC XYZ ABC`, `ETH` ≈ `ETH XYZ`.
- ISO / alt codes: `BTC` ≈ `XBT`; pair/quote notation: `BTC` ≈ `BTCUSD` ≈ `BTC-USD` ≈ `BTC/USD` ≈ `BTC USD`.
- Common coins follow the same pattern: `ETH`/`ETHUSD`/`ETH-USD`, `SOL`/`SOLUSD`, `LTC`, `DOGE`, etc.
- Test: is it the **same coin**? If yes → JOIN. (Crypto in a brokerage account is `default` and
  needs an approval — see `exempt-security-types.md`.)

### JOIN — mechanical equity decorations (same issuer, same share class)
- Punctuation only: `BRK.B` ≈ `BRKB` ≈ `BRK/B`; `RDS.A` ≈ `RDSA`.
- Venue / country / feed suffixes: `AAPL` ≈ `AAPL US` ≈ `AAPL.OQ` ≈ `AAPL UW`.
- A CUSIP/ISIN-tagged or exchange-tagged string that plainly carries the ticker for the same line.
- Test: strip the decoration and it's the **identical security** (same issuer AND same class).

### REVIEW — do NOT auto-join under this scope (record in `review_reasons.json` → NEEDS_REVIEW)
- Dual-listings / ADRs: `BABA` vs `9988 HK`, US ADR vs local line — same issuer, *different* line.
- Renamed tickers: `FB` vs `META`, `GOOG` vs `GOOGL` (also different class).
- Anything you cannot confidently call a crypto or mechanical variant.

### SEPARATE — never the same security (let each stand on its own; never map together)
- A derivative vs its underlying: an option or warrant (`NVDA 240119C150`) is not `NVDA`.
- A fund/trust/ETF vs the asset it holds: `GBTC` (Grayscale) ≠ `BTC`; a single-stock ETF ≠ its stock
  (those follow their own classification in `single-stock-etfs.md`).
- **Different share classes are different securities:** `BRK.A` ≠ `BRK.B`, `GOOG` ≠ `GOOGL`. Only
  *punctuation of the same class* is mechanical — never merge two distinct classes.

## Safety rules
- Only add a map entry when you are **confident** it's the same security. When unsure, do **not**
  guess and do **not** map — add the reported symbol to `review_reasons.json` so it becomes
  `NEEDS_REVIEW`.
- Never merge two different assets to force a match — a false join *clears a real violation*.
- Quantity/price may **corroborate** identity when a symbol is ambiguous (step 4), but never widen
  scope on their own: crypto + mechanical only.
