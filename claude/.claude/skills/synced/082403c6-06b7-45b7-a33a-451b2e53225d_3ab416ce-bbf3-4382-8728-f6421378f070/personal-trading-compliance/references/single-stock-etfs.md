# Single-Stock ETFs — require approval (NOT exempt)

Single-stock / single-name ETFs give leveraged, inverse, or income exposure to **one** company,
so they carry the same conflict/front-running risk as trading the underlying and require
pre-clearance like any single stock (classify as `single_stock_etf`). Broad-index funds — even
leveraged/inverse ones like TQQQ/SQQQ/SOXL — are exempt (`broad_etf`).

This list is a **starter, not exhaustive** — new ones launch constantly. Use it for fast exact
matches, but also apply the heuristic below, and when unsure classify `unknown` (→ `NEEDS_REVIEW`)
rather than assuming exempt.

## Heuristic (use when a ticker isn't listed)
A fund is `single_stock_etf` if ANY of these is true:
- Its name contains a single company name + a leverage/inverse/income wrapper, e.g.
  "Direxion Daily **TSLA** Bull 2X", "GraniteShares 2x Long **NVDA**", "YieldMax **AAPL** Option
  Income", "T-Rex 2X Long **MSTR**", "Tradr 2X Short **NVDA**".
- Its holdings/exposure resolve to **one** issuer (swaps/options on a single name).
- It's issued by a known single-stock line: **Direxion Daily (single-name Bull/Bear)**,
  **GraniteShares 2x Long/Short**, **T-Rex 2X**, **Defiance Daily Target 2X**, **Tradr (AXS)**,
  **YieldMax** (single-name option-income), **Leverage Shares**, **Kurv**, **Roundhill (single name)**.

If the name references an **index/basket/sector** (Nasdaq-100, S&P 500, Semiconductors, Russell,
"Innovation", VIX, gold), it's `broad_etf` no matter the leverage.

## Curated tickers (single-name → require approval)
```
# TSLA
TSLL TSLS TSLT TSLZ TSLQ TSLR TSLY TSLG TSDD
# NVDA
NVDL NVDU NVDX NVDD NVDQ NVDS NVDY NVYY
# AAPL
AAPU AAPD APLY AAPB
# MSFT
MSFU MSFD MSFY MSFL MSFO
# AMZN
AMZU AMZD AMZY AMZZ
# GOOGL / GOOG
GGLL GGLS GOOY
# META
METU METD FBL FBY
# MSTR (MicroStrategy)
MSTU MSTX MSTZ MSTY SMST
# COIN (Coinbase)
CONL CONI CONY CONU
# AMD
AMDL AMDS AMDY AMUU AMDG
# PLTR (Palantir)
PLTU PLTD PTIR PLTG PLTY
# NFLX
NFXL NFXS NFLY
# Other common single-name funds
SMCX SMCL SMCZ        # Super Micro
MUU MUD               # Micron
MARO MARZ             # (single-name where applicable)
BRKU                  # Berkshire 2x
JPMO                  # JPMorgan income
XOMO                  # Exxon income
PYPY                  # PayPal income
SQY                   # Block income
MRNY                  # Moderna income
ABNY                  # Airbnb income
DISO                  # Disney short income
BABX                  # Alibaba 2x
UBER-linked, HOOD-linked, etc. — verify by holdings
```

Note: income/covered-call single-name funds (the YieldMax "-Y" family: TSLY, NVDY, APLY, MSFY,
AMZY, GOOY, FBY, CONY, MSTY, JPMO, XOMO, PYPY, MRNY, ABNY, DISO, AMDY, PLTY …) are single-name
exposure and therefore require approval, even though they are marketed as "income."
