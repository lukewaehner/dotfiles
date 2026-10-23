# Common SPAC Warrant Structures Reference

## Standard SPAC Warrant Agreement Variants

### Type A: Ares / Reinvent Style (Single Redemption)

**Characteristics:**
- Strike: $11.50
- Single redemption path at $18.00 trigger
- Crescent Term (§4.3.2) for dilutive issuance adjustment — gate threshold is deal-specific (NOT always $9.20)
- NO make-whole table
- NO $10.00 cashless redemption
- NO Black-Scholes reference for public warrants

**Crescent Term Formula (§4.3.2):**

The Crescent Term has TWO distinct components:

1. **Gate Threshold** (deal-specific, e.g., $9.20 in AACT/KDK): This is an activation condition only. ALL three conditions must be met for the adjustment to fire:
   - (x) Additional shares issued at effective price < Gate Threshold ("Newly Issued Price" or NIP)
   - (y) Aggregate gross proceeds from such issuances > 60% of total equity proceeds (net of redemptions)
   - (z) 20-trading-day VWAP starting day prior to closing ("Market Value" or MV) < Gate Threshold

2. **Adjustment Formula** (keys off ACTUAL dilution levels, NOT the gate):
   - New Exercise Price = 115% × max(Market Value, Newly Issued Price)
   - New Redemption Trigger = 180% × max(Market Value, Newly Issued Price)

**Critical distinction:** The gate threshold determines WHETHER the adjustment fires. The Market Value and Newly Issued Price determine HOW MUCH the adjustment is. For example, in KDK: gate was $9.20, MV was $8.07, NIP was lower → adjustment keyed off $8.07 (the higher of MV and NIP), producing strike of $9.28 and redemption trigger of $14.53.

**Examples:** AACT/KDK, Reinvent Technology Partners Z

---

### Type B: EarlyBird / Cantor Style (Dual Redemption + Make-Whole)

**Characteristics:**
- Strike: $11.50
- TWO redemption paths:
  1. Standard: $18.00 trigger, $0.01 redemption price (same as Type A)
  2. Cashless at $10.00: $10.00 trigger, $0.10 redemption price, with make-whole table
- Make-whole table governs cashless exercise shares upon $10 redemption
- May include Black-Scholes reference for certain warrant classes

**$10.00 Cashless Redemption (§6.2 typically):**
- Trigger: Reference Value ≥ $10.00 for 20/30 trading days
- Redemption price: $0.10 per warrant
- Company MUST allow cashless exercise on redemption
- Number of shares received determined by make-whole table below
- Private warrants: also redeemable under this path (unlike $18 path)

**Standard Make-Whole Table:**
Shares of common stock per warrant upon cashless exercise, based on Fair Market Value and time remaining:

| FMV \ Months | 60 | 57 | 54 | 51 | 48 | 45 | 42 | 39 | 36 | 33 | 30 | 27 | 24 | 21 | 18 | 15 | 12 | 9 | 6 | 3 | 0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $10.00 | 0.261 | 0.252 | 0.243 | 0.233 | 0.224 | 0.214 | 0.204 | 0.194 | 0.184 | 0.174 | 0.163 | 0.152 | 0.141 | 0.129 | 0.118 | 0.106 | 0.094 | 0.082 | 0.069 | 0.056 | 0.042 |
| $11.00 | 0.281 | 0.272 | 0.263 | 0.253 | 0.244 | 0.234 | 0.224 | 0.214 | 0.204 | 0.193 | 0.183 | 0.172 | 0.161 | 0.149 | 0.137 | 0.125 | 0.113 | 0.100 | 0.087 | 0.073 | 0.058 |
| $12.00 | 0.297 | 0.289 | 0.280 | 0.271 | 0.261 | 0.252 | 0.242 | 0.232 | 0.222 | 0.211 | 0.200 | 0.190 | 0.179 | 0.167 | 0.155 | 0.142 | 0.130 | 0.117 | 0.104 | 0.089 | 0.074 |
| $13.00 | 0.311 | 0.303 | 0.294 | 0.285 | 0.276 | 0.267 | 0.257 | 0.247 | 0.237 | 0.226 | 0.216 | 0.205 | 0.194 | 0.183 | 0.170 | 0.158 | 0.145 | 0.132 | 0.118 | 0.104 | 0.088 |
| $14.00 | 0.323 | 0.315 | 0.307 | 0.298 | 0.289 | 0.280 | 0.270 | 0.261 | 0.250 | 0.240 | 0.230 | 0.219 | 0.208 | 0.197 | 0.185 | 0.172 | 0.159 | 0.146 | 0.132 | 0.117 | 0.102 |
| $15.00 | 0.333 | 0.326 | 0.317 | 0.309 | 0.300 | 0.291 | 0.282 | 0.272 | 0.262 | 0.252 | 0.241 | 0.231 | 0.220 | 0.209 | 0.197 | 0.184 | 0.172 | 0.158 | 0.144 | 0.130 | 0.115 |
| $16.00 | 0.342 | 0.335 | 0.327 | 0.318 | 0.310 | 0.301 | 0.292 | 0.282 | 0.272 | 0.262 | 0.252 | 0.242 | 0.231 | 0.220 | 0.208 | 0.196 | 0.183 | 0.170 | 0.156 | 0.142 | 0.127 |
| $17.00 | 0.350 | 0.343 | 0.335 | 0.327 | 0.318 | 0.310 | 0.301 | 0.291 | 0.282 | 0.272 | 0.262 | 0.251 | 0.241 | 0.230 | 0.219 | 0.207 | 0.194 | 0.181 | 0.167 | 0.153 | 0.139 |
| $18.00 | 0.357 | 0.350 | 0.342 | 0.334 | 0.326 | 0.318 | 0.309 | 0.300 | 0.290 | 0.281 | 0.271 | 0.261 | 0.250 | 0.240 | 0.229 | 0.217 | 0.205 | 0.192 | 0.179 | 0.164 | 0.150 |

*Note: Exact values vary by deal. Always verify against the actual filing. The above is representative of the Churchill Capital / CF Acquisition / Replay style.*

**Fair Market Value Definition (for make-whole):**
Average of closing prices for 10 trading days ending on third trading day prior to redemption notice date.

**Months to Expiration:**
Calendar months from redemption notice date to warrant expiration date.

**Interpolation:**
If exact FMV or months not in table, linearly interpolate between adjacent values.

**Examples:** Churchill Capital Corp IV (CCIV/LCID), CF Acquisition Corp VIII, GS Acquisition Holdings Corp 2

---

### Type C: Structured / Non-Standard

Some warrants deviate significantly. Watch for:
- **Penny warrants** ($0.01 exercise price) — common in PIPE structures
- **Reset warrants** — exercise price resets periodically based on market price (like exploding unit deals)
- **Knockout warrants** — expire worthless if stock price hits a barrier
- **Revenue warrants** — exercisability tied to revenue milestones
- **Earn-out warrants** — vest upon achievement of price/performance targets

---

## Key Definitions Reference

### Reference Value (Redemption)
The closing price of common stock for any 20 trading days within a 30-consecutive-trading-day period ending on the third trading day prior to the date on which notice of redemption is sent. This is the price that must equal or exceed the redemption trigger.

### Fair Market Value (Cashless Exercise)
For cashless exercise purposes: the average of the last reported sale prices of common stock for the 10 trading days ending on the third trading day prior to the date on which notice of exercise (or notice of redemption, if forced cashless) is sent.

### Market Value (Crescent Term)
The volume-weighted average price of common stock during the 20-trading-day period starting on the trading day prior to the day on which the Business Combination closes. Used to calculate adjusted strike and redemption trigger.

### Newly Issued Price (Crescent Term)
The effective issue price or effective conversion price at which additional shares of common stock or equity-linked securities are issued in connection with the Business Combination. If no consideration is received, the NIP equals $0.

---

## Cashless Exercise Formulas

### Standard Cashless (Public Warrants — triggered by redemption or no-registration)
```
Shares = (Warrant Shares × (FMV − Exercise Price)) / FMV
```
Where FMV = 10-day average closing price ending 3 days before the notice date.

### Make-Whole Cashless ($10 Redemption Path)
```
Shares = Table Value (based on FMV and months to expiration)
```
Where Table Value is looked up from the make-whole table, with linear interpolation.

### Private Placement / Sponsor Cashless (available at any time)
```
Shares = (Warrant Shares × (FMV − Exercise Price)) / FMV
```
Same formula as public, but FMV measured as of exercise notice date (not redemption notice date).

---

## Section Number Cross-Reference

Different warrant agents use slightly different section numbering. Here's a rough mapping:

| Topic | Continental STT | Computershare | AST |
|-------|----------------|---------------|-----|
| Exercise Price | §3.1 | §3.1 | §3(a) |
| Duration/Period | §3.2 | §3.2 | §3(b) |
| Exercise Mechanics | §3.3 | §3.3 | §3(c)-(e) |
| Adjustments — Splits | §4.1 | §4.1 | §4(a) |
| Adjustments — Reverse | §4.2 | §4.2 | §4(b) |
| Adjustments — Dilutive | §4.3.2 | §4.3(b) | §4(c) |
| Merger/Reorg | §4.4 | §4.4 | §4(d) |
| Redemption | §6.1 | §6.1 | §6(a) |
| Reference Value | §6.2 | §6.2 | §6(b) |
| Registration | §7.4 | §7.4 | §7 |
| Amendments | §9.8 | §9.8 | §9(h) |
| Governing Law | §9.3 | §9.2 | §9(c) |

*These are approximate. Always verify against the actual document.*
