---
name: price-calls
description: Price listed equity call options at user-specified implied volatilities using a CRR binomial tree with borrow cost. Trigger when the user asks to 'price calls', 'price the calls', 'run the calls at [IV]', 'reprice the options', 'what do the calls look like at [vol]', 'model the 7.5s at 50 and 60 vol', or any request to value listed call options across multiple IVs and expiries for a single strike. Also trigger when the user asks for 'IV at bid/ask', 'back out the vol', 'what vol is the market pricing', or wants to compare model prices to market. Works for any ticker with listed options. Requires MCP tools get-price, get-option-chain, and get-option-data.
---

# Price Calls Skill

Price all listed call options at a given strike across every expiry, using a CRR binomial tree with borrow cost. Produces a single table showing model prices at each user-specified IV alongside live market data (bid, ask, last, OI) and the implied vol at bid and ask.

## Inputs

The user provides (or you extract from context):
- **Ticker** — e.g. `KDK`
- **Strike** — e.g. `7.5`
- **IVs** — list of implied volatilities to price at, e.g. `[50, 60]` (in %)
- **Borrow** — annualized borrow cost as continuous dividend yield, e.g. `18` (in %)
- **Risk-free rate** — default `4.25%` unless specified

If the user doesn't provide all inputs, ask. Check memory/conversation history for recent borrow assumptions before asking.

## Step 1: Fetch Live Data via MCP Tools

### 1a. Get spot price

Use the `get-price` tool:

```
Tool: get-price
Parameters:
  ticker: "KDK"        # just the ticker, no suffix
```

Returns JSON with field `price` — this is the live spot. Example:
```json
{
  "ticker": "KDK",
  "price": 7.26,
  "open": 7.51,
  "day_high": 7.61,
  "day_low": 7.21,
  "volume": 173582.0
}
```

Extract `price` as `S` (spot).

### 1b. Get option chain for the strike

Use the `get-option-chain` tool:

```
Tool: get-option-chain
Parameters:
  ticker: "KDK"           # just the ticker, no suffix
  option_type: "call"
  strike_min: 7.5          # exact strike
  strike_max: 7.5          # exact strike
```

Returns JSON with `options` array. Each element contains:
```json
{
  "option_ticker": "KDK US 04/17/26 C7.5 Equity",
  "expiration": "2026-04-17",
  "strike": 7.5,
  "type": "call",
  "px_last": 0.30,
  "px_bid": 0.15,         // can be null
  "px_ask": 0.45,         // can be null
  "volume": 13.0,
  "open_interest": 6,
  "implied_vol": 53.12    // Bloomberg's IV (no borrow adj)
}
```

This gives you every listed expiry at that strike in one call. Extract:
- `expiration` → compute DTE from today
- `px_bid`, `px_ask`, `px_last` → market prices
- `open_interest` → OI
- `implied_vol` → BBG IV (reference only — this is Bloomberg's solve without our borrow)

### 1c. (Optional) Get detailed Greeks from Bloomberg

If the user wants Bloomberg Greeks or more granular data, use `get-option-data`:

```
Tool: get-option-data
Parameters:
  identifiers: [
    "KDK US 04/17/26 C7.5 Equity",
    "KDK US 05/15/26 C7.5 Equity",
    "KDK US 01/21/28 C7.5 Equity"
  ]
```

Use the exact `option_ticker` strings returned by `get-option-chain`. Returns per-contract:
```json
{
  "PX_LAST": 1.55,
  "PX_BID": 1.2,
  "PX_ASK": 1.45,
  "IVOL_LAST": 41.35,
  "OPT_UNDL_PX": 7.28,
  "delta": 0.533,
  "gamma": 0.007,
  "theta": -0.001,
  "vega": 0.036,
  "implied_vol": 41.22,
  "option_ticker": "KDK US 01/21/28 C7.5 Equity"
}
```

This step is optional — only needed if user asks for Bloomberg Greeks or you want to cross-check. The chain call in 1b already has bid/ask/IV.

## Step 2: Price with CRR Binomial Tree

Use a **Cox-Ross-Rubinstein binomial tree** with **1 step per calendar day** (steps = DTE). The borrow enters as the continuous dividend yield `q`.

### Python implementation

```python
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from datetime import date, datetime

def crr_american_call(S, K, T, r, q, sigma, steps):
    """
    CRR binomial tree for American call options.
    
    Parameters:
        S:     spot price
        K:     strike price
        T:     time to expiry in years (DTE / 365)
        r:     risk-free rate (e.g. 0.0425)
        q:     continuous dividend yield / borrow cost (e.g. 0.18)
        sigma: implied volatility (e.g. 0.60)
        steps: number of tree steps (= DTE, 1 step per calendar day)
    
    Returns: American call price
    """
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    p = (np.exp((r - q) * dt) - d) / (u - d)
    disc = np.exp(-r * dt)
    
    # Terminal payoffs
    ST = np.array([S * (u ** (2*j - steps)) for j in range(steps + 1)])
    option = np.maximum(ST - K, 0.0)
    
    # Backward induction with American exercise check
    for i in range(steps - 1, -1, -1):
        Si = np.array([S * (u ** (2*j - i)) for j in range(i + 1)])
        continuation = disc * (p * option[1:i+2] + (1 - p) * option[0:i+1])
        exercise = np.maximum(Si - K, 0.0)
        option = np.maximum(continuation, exercise)
    
    return option[0]


def crr_delta(S, K, T, r, q, sigma, steps, bump=0.01):
    """Central-difference delta from the tree."""
    up = crr_american_call(S + bump, K, T, r, q, sigma, steps)
    dn = crr_american_call(S - bump, K, T, r, q, sigma, steps)
    return (up - dn) / (2 * bump)


def implied_vol_tree(price, S, K, T, r, q, steps):
    """
    Back out the implied vol that makes the CRR tree match a given price.
    Returns None if no solution found.
    """
    try:
        if price <= 0:
            return None
        return brentq(
            lambda sig: crr_american_call(S, K, T, r, q, sig, steps) - price,
            0.01, 5.0, xtol=1e-6
        )
    except:
        return None
```

### Computation loop

For each expiry from the option chain:
1. Compute `DTE` = calendar days from today to expiration
2. Set `T = DTE / 365.0` and `steps = DTE`
3. For each user-specified IV, compute `crr_american_call(S, K, T, r, q, sigma, steps)`
4. Compute delta at each IV via `crr_delta`
5. Back out implied vol at bid: `implied_vol_tree(bid, S, K, T, r, q, steps)` — skip if bid is null
6. Back out implied vol at ask: `implied_vol_tree(ask, S, K, T, r, q, steps)` — skip if ask is null

## Step 3: Output Table

Present results in a markdown table. Format:

```
Ticker: KDK | Spot: $7.26 | Strike: $7.50 | Borrow: 18% | r: 4.25%

| Expiry      | DTE | [IV1] Theo | [IV1] Δ | [IV2] Theo | [IV2] Δ | Bid   | Bid IV | Ask   | Ask IV | Last  | BBG IV | OI   |
|-------------|-----|------------|---------|------------|---------|-------|--------|-------|--------|-------|--------|------|
| Apr 17 '26  |  25 | $0.26      | 0.36    | $0.32      | 0.41    | $0.15 | 35%    | $0.45 | 72%    | $0.30 | 53%    |    6 |
| May 15 '26  |  53 | $0.40      | 0.40    | $0.50      | 0.44    | —     | —      | $0.65 | 68%    | $1.05 | 71%    |  602 |
...
```

Column ordering:
1. Expiry (short date label)
2. DTE
3. For each IV: Theo price and Delta (label column headers as e.g. "50 Theo" / "50 Δ")
4. Market Bid
5. IV at Bid (our model IV solve, with borrow — NOT Bloomberg's)
6. Market Ask
7. IV at Ask (our model IV solve, with borrow)
8. Last
9. BBG IV (Bloomberg's IV, no borrow — reference only)
10. OI

### Formatting rules
- Prices to 2 decimals, dollar sign: `$0.32`
- Delta to 2 decimals, no sign: `0.41`
- IV to whole percent: `72%`
- Null bid/ask → show `—`
- Null IV (couldn't solve) → show `—`
- OI as integer, comma-separated if >999

### Key context to provide the user

After the table, note:
- **"Bid IV" and "Ask IV"** are solved through OUR tree with borrow — they will differ from Bloomberg because BBG does not use our borrow assumption
- If bid IV or ask IV is significantly different from the user's target IVs, flag it
- Call out any expiry where the market is notably wide or where liquidity (OI) is thin
- If there are orders on the blotter (from conversation context), compare limit prices to the model theos

## Edge Cases

- **Very short DTE (<5 days):** Tree still works but values are mostly intrinsic. Note this.
- **Null bid:** Common for illiquid options. Skip IV solve, show `—`.
- **No options at requested strike:** Tell the user and suggest nearby strikes from the chain.
- **Borrow > r:** Expected for hard-to-borrow names. The forward will be below spot. This is correct — note the forward price for context.
- **IV solve fails:** Can happen if price is below intrinsic or above max vol boundary. Show `—`.

## Example Usage

User: "price the 7.5 calls at 50 and 60 vol with 18 borrow"

→ Fetch spot (get-price KDK) → $7.26
→ Fetch chain (get-option-chain KDK, call, strike 7.5) → 5 expiries
→ For each expiry: tree at 50% IV, tree at 60% IV, solve IV at bid, solve IV at ask
→ Output table with all columns
