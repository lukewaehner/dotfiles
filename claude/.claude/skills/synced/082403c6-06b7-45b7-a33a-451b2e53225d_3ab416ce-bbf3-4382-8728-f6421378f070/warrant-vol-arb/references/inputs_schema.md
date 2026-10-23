# inputs.json schema

Tape (`spot`, `warrant_price`, `listed_front_iv`, `realized`) comes from the **Bloomberg pull**; the
contract terms (`strike`, `expiry_*`, `redemption_trigger`, `make_whole_trigger`, `trigger_days`,
`notice_days`) come from the **verified warrant agreement on SEC EDGAR** (see `edgar_terms.md`) — do NOT
take strike/expiry/redemption from Bloomberg's indicative DES. `borrow` comes from the stock-loan desk.
Percentages are **decimals** (95% → 0.95).

```json
{
  "ticker": "IMSR",              // underlying ticker
  "warrant_ticker": "IMSRW",     // warrant ticker
  "company": "Terrestrial Energy Inc",
  "asof": "2026-06-23",

  "spot": 7.645,                 // underlying last/mid (Bloomberg)
  "warrant_price": 3.65,         // warrant ask (cost to buy) — or mid (Bloomberg)
  "strike": 11.50,               // VERIFIED exercise price (EDGAR warrant agreement)
  "expiry_years": 4.35,          // VERIFIED life = (BC close + 5y) − asof. OR use "expiry_days"
  "expiry": "28-Oct-2030",       // human-readable verified expiry (for the brief)
  "shares_per_warrant": 1.0,

  "rate": 0.04,                  // ~risk-free; least important input
  "borrow": 0.0094,              // ACTUAL stock-loan cost-to-borrow — make-or-break

  "listed_front_iv": 1.17,       // near-the-money front-month call IVM from OMON
  "realized": { "HV10": 0.894, "HV30": 1.144, "HV50": 1.181, "HV100": 1.010 },

  "redemption_trigger": 18.0,    // VERIFIED $18 cash-redemption level (EDGAR)
  "trigger_days": [20, 30],      // Reference-Value mechanic: N of M trading days >= trigger
  "notice_days": 30,             // redemption notice period (days)
  "make_whole_trigger": null,    // set to e.g. 10.0 only if the agreement HAS a $10 make-whole redemption
  "delay_trigger_proxy": 22.0,   // lenient-issuer bound: stock level the issuer effectively waits for
  "size_warrants": 50000         // sizing clip for the brief
}
```

Required: `spot`, `warrant_price`, `strike`, `expiry_years` (or `expiry_days`), `borrow`,
`listed_front_iv`, `redemption_trigger`. The rest have sensible defaults
(`trigger_days=[20,30]`, `notice_days=30`, `make_whole_trigger=null`, `delay_trigger_proxy=trigger+4`).

## Run

```bash
# Knockout-aware engine = HEADLINE for SPAC warrants (writes <inputs>.knockout.json)
python3 scripts/warrant_knockout_mc.py inputs.json
python3 scripts/warrant_knockout_mc.py inputs.json --paths 8000     # faster/noisier
python3 scripts/warrant_knockout_mc.py inputs.json --borrow 0.05    # what-if borrow

# Vanilla BS bound + break-even borrow (no knockout) — reference, or for warrants with no redemption
python3 scripts/warrant_arb.py inputs.json

# 3-page desk brief from the knockout-aware results
python3 scripts/build_brief.py inputs.knockout.json --out TICKER_brief.pdf
```

The knockout-aware `knockout.json` carries everything the brief needs: `vanilla_iv`, `koiv_first` /
`koiv_delay` / `koiv_central`, edges, `fair_at_listed`, knockout-model `delta`/`vega`, the price-vs-vol
`curve`, the `payoff` truncation series, `verdict`, and `sizing`.
