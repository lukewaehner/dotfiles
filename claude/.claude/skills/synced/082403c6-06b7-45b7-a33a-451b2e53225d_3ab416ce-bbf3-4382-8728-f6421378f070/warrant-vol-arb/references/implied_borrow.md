# Implied-borrow term structure (listed-option put-call parity)

A market-based read on the stock borrow at **every tenor**, for when the underlying has **listed options**.
Borrow is the swing input in the warrant verdict, so when the option market exists you can lay an
independent borrow read against (a) the single desk-quoted rate you priced with and (b) the warrant's own
implied borrow. This builds the **"Implied Borrow by Tenor"** panel in the desk brief (the optional extra
page: 30d amber solid + markers, 10d steel-blue dashed, warrant-implied borrow as stars).

## When to use

- The underlying has a listed options market (OMON returns a chain). **Skip it when there are none** — most
  micro-cap de-SPACs return OMON "security not supported" (OPTX/OPTXW was one); then the brief is the
  normal 3 pages and the single desk-quoted borrow stands alone.
- Always optional. The verdict does not require it, but it is the strongest corroboration of the borrow
  that drives the whole knockout-adjusted-vol call.

## Method — put-call parity at mid, ATM bracket, median

Per ATM-bracket observation — a (quote-date, expiry, strike) with call & put bid+ask and **that day's
spot**:

    C_mid = (c_bid + c_ask) / 2        P_mid = (p_bid + p_ask) / 2
    T     = (expiry − quote_date) / 365
    fwd   = (C_mid − P_mid) + K·e^(−rT)     # PCP:  C − P = S·e^(−qT) − K·e^(−rT)  ⇒  S·e^(−qT) = fwd
    q     = −ln(fwd / spot) / T             # implied borrow (continuous), per observation

Pool observations over two trailing windows ending at as-of — **10 and 30 trading days** (10d fresher /
noisier, 30d smoother). Per option expiry the implied borrow is the **median q** of the valid ATM-bracket
observations in the window; the two median term-structures are the curves. Their mean across expiries is a
transparent "avg" reference line (not a tenor-weighted index).

This is a **borrow** read off the forward, not a vol read — do not substitute the listed IV.

Notes:
- **Spot is the quote-date spot**, not the as-of spot — the stock moves across the window, and each
  observation's q uses its own day's spot.
- **ATM bracket** = the ~2 strikes nearest that day's spot, per expiry.
- Keep every observation with a **positive forward**; the per-expiry median is robust to the wide-market
  outliers that single quotes throw off.

## The pull (local Bloomberg terminal)

For the trailing ~30 sessions, for each listed expiry, pull the ~2 ATM strikes' **call & put bid/ask** and
the **day's spot**. OMON gives today's chain; use the option-monitor history (or a dated OMON pull) for the
prior sessions. Assemble into `obs.json`. The `warrants` points are the borrow you want to mark at the
warrant's (long) tenor — the desk-quoted/used borrow and/or a warrant-implied borrow — drawn as stars for
the cross-check.

## obs.json schema

```json
{
  "ticker": "KDK", "warrant_ticker": "KDKRW",
  "asof": "2026-06-25",
  "spot": 5.14,                 // as-of spot (header only)
  "rate": 0.043,                // ~risk-free short rate (USGG3M)
  "obs": [
    {"date": "2026-06-25", "exp": "2026-07-17", "K": 5.0,
     "c_bid": 0.45, "c_ask": 0.70, "p_bid": 0.30, "p_ask": 0.55, "spot": 5.14}
    // ... one row per (quote-date, expiry, ATM strike); spot = THAT day's spot
  ],
  "warrants": [                 // optional borrow markers at the warrant tenor (stars)
    {"label": "KDKRW", "exp": "2030-09-25", "q": 14.27}
  ]
}
```

## Run

```bash
python3 scripts/implied_borrow.py obs.json                 # writes obs.borrow_curve.json, prints the curve
python3 scripts/implied_borrow.py obs.json --windows 10,30 # trailing trading-day windows (default 10,30)
python3 scripts/build_brief.py inputs.knockout.json --borrow-curve obs.borrow_curve.json --out TICKER_brief.pdf
```

The brief auto-adds the term-structure page only when `--borrow-curve` is supplied; otherwise it stays the
standard 3 pages.

## Reading it

- **Downward-sloping (inverted) curve** = a near-dated borrow squeeze the market expects to ease; a flat or
  upward curve = a stable or tightening borrow.
- **10d under 30d** = borrow softening recently (the fresh window is cheaper than the smoothed one); 10d
  above 30d = tightening.
- **Warrant star vs the option curve at that tenor is the headline cross-check.** A star well above the
  option curve means the warrant is pricing a *richer* borrow than the options — and your
  knockout-adjusted vol leans entirely on that borrow, so confirm the rate before trusting the verdict.
  (The option curve usually stops years short of the warrant, so the star is read against the curve's
  long end / its extrapolation, not a same-tenor option.)
```
