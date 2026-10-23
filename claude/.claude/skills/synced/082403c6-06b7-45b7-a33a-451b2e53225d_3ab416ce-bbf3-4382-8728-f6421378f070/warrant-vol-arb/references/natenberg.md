# Natenberg — *Option Volatility and Pricing* (2nd ed.): Internalized Reference

A faithful, chapter-by-chapter distillation of Sheldon Natenberg's *Option Volatility and Pricing: Advanced Trading Strategies and Techniques* (2nd ed., 2015). Built by reading the full text. This is the durable record of that reading — dense by design, organized to be reloaded and applied.

**The book's spine in one breath:** An option is a bet on *speed* (volatility), not just direction. A theoretical pricing model turns a volatility guess into a value; the difference between value and price is your edge. You capture that edge by hedging delta-neutral and dynamically rehedging, which is just betting the same favorable odds many times to smooth out luck. Everything else — the greeks, spreads, synthetics, skew — is machinery for finding edge, sizing it against risk, and surviving the short run long enough for the long-run probabilities to pay off.

---

## Part I — Contracts, Forwards, and the Pricing Idea (Ch 1–5)

### Ch 1 — Financial Contracts
- **Derivatives covered:** forwards, futures, options. In derivative markets you can **sell before you buy** (open short). Opening trade → open position; offsetting trade → closing. **Open interest** = contracts not yet closed; longs must equal shorts.
- **Long/short ambiguity:** distinguish *contract position* (bought/sold the contract) from *market position* (want underlying up/down). A long put is a long contract but a short market position.
- **Settlement — the critical distinction:**
  - **Stock-type settlement:** full immediate payment; profits/losses *unrealized* until you close. (All North American options settle like stock.)
  - **Futures-type settlement (margin + variation):** no upfront payment; daily cash variation flows as price moves. Margin belongs to the trader (earns interest); variation is a real cash credit/debit.
  - **The trap:** in the U.S., futures *options* settle like stock but the underlying *future* settles like a future. A "hedged" position can still have surprise cash-flow/variation needs.
- **Market integrity:** the exchange/clearinghouse becomes counterparty to every trade (buyer to each seller, seller to each buyer). Tiered guarantee: trader → clearing firm → clearinghouse. A U.S. clearinghouse has never failed.

### Ch 2 — Forward Pricing
- **Master relation:** `forward price = cash price + cost of buying now − benefit of buying now`.
- **Physical commodity:** `F = C·(1 + r·t) + (s·t) + (i·t)` (storage s, insurance i). Normal = **contango** (long-dated > short-dated); inverted = **backwardation**, driven by a **convenience yield** (value of having the good *now*).
- **Stock:** `F = [S·(1 + r·t)] − D` (D = dividends to expiry; interest on dividends usually ignored).
- **Bonds/notes:** treat coupons like dividends.
- **FX:** forward uses the ratio of domestic vs. foreign interest accrual on spot. Two rates matter.
- **Options:** value depends on the **forward price** of the underlying. For a futures contract, the forward price *is* the futures price (no extra calc).
- **Arbitrage & implied values:** cash-and-carry locks the mispricing. From `F = S(1+r·t) − D` you can back out the **implied** S, r, or D. Implied values = the market's consensus estimate of the missing input.
- **Dividends:** declared / record / **ex-dividend (ex-date)** / payable dates. Ex-date is what option traders watch (ownership confers the dividend). Stock opens ex-div down by the dividend amount, all else equal.
- **Short sales:** must borrow stock; you receive only the **short rate** rs (< long rate rl). `rl − rs = borrowing cost`. Hard-to-borrow → low/zero rebate → **short squeeze** risk. **Options need no borrowing — always use the long rate for option cash flows.**

### Ch 3 — Contract Specs & Terminology
- **Call** = right to buy; **Put** = right to sell. *All rights to the buyer, all obligations to the seller.* Futures obligate both sides; options give the buyer the choice.
- **Exercise/assignment** settles into: (1) physical underlying, (2) a futures position (immediately margined + variation), or (3) **cash** (index). Cash flow on physical settlement depends only on the **exercise price**, not the underlying price.
- **Exercise style:** **European** = exercise only at expiry; **American** = any time. Geography-independent. Generally: options on futures and on individual stocks → American; index options → European.
- **Premium = intrinsic value + time value (extrinsic).**
  - Call intrinsic = max(0, S − X); Put intrinsic = max(0, X − S). Intrinsic is independent of expiry.
  - Time value (time premium) = the extra paid for the option's protective feature. Zero time value → trading at **parity**. European options can occasionally have *negative* time value (trade below parity).
- **ITM / ATM / OTM:** ITM has positive intrinsic. ATM ≈ exercise nearest underlying; ATM and OTM options are most volatility-sensitive and most actively traded.
- **Automatic exercise** of ITM options at expiry (threshold varies; "do not exercise" notice possible). **Margining** is risk-based for unlimited-risk positions (OCC system; **SPAN** on futures).

### Ch 4 — Expiration P&L
- At expiry an option is worth **exactly intrinsic value**. Four **parity (hockey-stick) graphs**: long/short call, long/short put.
- **Buyers:** limited risk (the premium), unlimited profit. **Sellers:** limited profit (the premium), unlimited risk. Why sell anyway? Because of **probability** — collect enough premium for low-probability risk.
- **Slope:** OTM option slope 0; ITM call slope +1, ITM put slope −1. Long underlying slope +1, short −1 (constant). Build any position's expiration graph by summing slopes across intervals, then anchor one P&L point.
- **P&L graph = parity graph shifted by net debit (down) / credit (up).** Breakeven = where P&L crosses 0.

### Ch 5 — Theoretical Pricing Models
- Options care about **direction *and* speed**. Buying options requires being right on *both* — a hard double bet, which is why most edge comes from volatility, not direction.
- **Expected value** = Σ(outcome × probability). **Theoretical value** = *present value of the expected value* (discount by interest; add dividend-like adjustments). Casino/roulette analogy: pay less than the 95¢ fair value to have the edge — but you must survive the short run to reach the long run.
- **Model-building recipe:** (1) propose terminal prices, (2) assign probabilities such that the market is arbitrage-free → **expected value of the underlying = forward price**, (3) compute the option's expected value, (4) discount to present value per settlement type.
- "At the money" vs **"at the forward"** (exercise = forward price). At-the-forward options are the common benchmark.
- **Black-Scholes (1973):** five core inputs — exercise price, time to expiry, underlying price, interest rate, **volatility**. Variants differ only in forward-price calc and settlement: **Black-Scholes** (stock), **Black** (futures), **Garman-Kohlhagen** (FX, two rates). Volatility is the only **unobservable** input.
- **Riskless hedge:** every option has a theoretically equivalent underlying position (the **hedge ratio / delta**). Do the **opposite with calls** (buy calls → sell underlying) and the **same with puts** (buy puts → buy underlying). An option is a substitute for an underlying position; trade the option when it's cheaper/dearer than its value.
- **GIGO:** a model is a candle in a dark room — invaluable but distorted by the flicker. Garbage in, garbage out; danger rises as size rises.

---

## Part II — Volatility, the Heart of the Book (Ch 6)

### What volatility *is*
- **Volatility = a measure of the speed of the market = a standard deviation (σ).** It is the σ of a normal distribution of percent price changes, annualized.
- **Forward price = the mean** of the distribution; **volatility = the standard deviation.** Together they fully specify a normal distribution.
- **Working definition:** the input is a **one-standard-deviation price change, in %, over one year.** With F = 100, σ = 20% → in one year: ~68.3% chance within 80–120 (±1σ), ~95.4% within 60–140 (±2σ), ~99.7% within 40–160 (±3σ). (≈ 2/3, 19/20, 369/370.)
- For a stock, center the distribution on the **forward**, not spot: 20% of a $108 forward → ±$21.60.

### Scaling for time — the √t rule
- **Volatility is proportional to √t** (unlike interest, which is ∝ t). `σ_period = σ_annual · √t`.
- **256 trading days/year** → √256 = 16. **Daily σ ≈ annual σ / 16.** (e.g., 20% → 1.25%/day on a 100 contract.)
- **52 weeks** → √52 ≈ 7.2. **Weekly σ ≈ annual σ / 7.2.**
- Benchmark: expect a >2σ daily move ~1 in 20 days ≈ once a month.
- Use **settlement-to-settlement** price changes (logarithmic returns) for the calculation.

### Lognormal distributions
- Normal distribution of *prices* is flawed: it permits negative prices. Volatility is a **rate of return** (mix of + and − returns); continuously compounding normally-distributed returns yields a **lognormal distribution of prices** at expiry — bounded by 0 below, open-ended (longer right tail) above.
- Consequence: the **mean sits to the right of the mode/peak**. A symmetric-OTM call (110) is worth **more** than the equally-OTM put (90): the call's upside is unbounded; the put can rise only to the strike. Black-Scholes assumes continuous compounding (a continuous-time model). `$1000·e^0.12 = $1127.50` vs `e^−0.12 = $886.92`.

### Realized vs implied volatility
- **Realized (a.k.a. historical) volatility:** annualized σ of % price changes of the *underlying*. Specify interval (daily/weekly) and window (50-day, 52-week). **Future realized volatility** over the option's life is what truly determines value — and is unknowable, so estimate it (history is the starting point).
- **Implied volatility:** backed *out of an option's market price* — the market's consensus of future realized volatility. Run the model backwards (numerically). Depends on the model and on contemporaneous inputs (stale underlying → wrong implied vol).
- Traders quote options **in vol terms** ("bought the call at 27.5"). "Premium high/low" = implied vol high/low. Comparing two options: lower implied vol is usually the better value.
- **Three vol-change principles** (gold example):
  1. A vol change moves an **ATM** option most **in total points**.
  2. A vol change moves an **OTM** option most **in percent terms**.
  3. A vol change moves a **long-term** option more than a short-term one (higher vega).
  - ITM options are *least* sensitive to vol; deep ITM behaves like the underlying. Hence volume concentrates in ATM/OTM.
- Companion calls/puts (same strike/expiry) have nearly identical implied vols (put-call parity foreshadowed).
- **Weather analogy:** historical vol = climate, forecast = the forecaster, implied = what people on the street are wearing. Decide with a **margin for error** — a 2-point vol error can be ruinous; never run a strategy that only works at *exactly* your vol guess.

---

## Part III — The Greeks (Ch 7, 9) and Dynamic Hedging (Ch 8)

### The risk measures (Ch 7)
Greeks are additive across a position (multiply each by signed contract count, sum). Interest-rate effects on value:
- **Stock calls** rise with rates (higher forward dominates); **stock puts** fall. **Dividends:** up → forward down → calls down, puts up. Carrying **short stock** lowers the effective rate (borrow cost) → willing to sell calls cheaper / buy puts dearer. **Rule: avoid a short stock position when possible** (many traders keep some long stock so they can always sell long).
- **Futures options (futures-type settlement):** insensitive to rates. **(stock-type settlement):** both calls & puts fall slightly as rates rise (small).

**Delta (Δ)** — directional risk; four interpretations:
1. **Rate of change** = slope of the value curve. Call Δ ∈ [0, 100], put Δ ∈ [−100, 0]; underlying Δ = 100 (whole-number convention).
2. **Hedge ratio** = 100 / |Δ| → contracts of underlying per option for a neutral hedge. Delta-neutral = total Δ sums to 0.
3. **Equivalent underlying position** — each 100 deltas ≈ one underlying contract (theoretically; an option is *not* a pure surrogate).
4. **Probability** ≈ chance the option finishes ITM (rough; the true probability is N(d2), slightly less than Δ = N(d1)). ATM ≈ 50; at-the-forward Δ slightly > 50.

**Gamma (Γ)** — curvature; rate of change of delta per 1-point move. **Always positive for long options (calls and puts alike).** Long options → long gamma. New delta = old delta ± gamma (add on up-moves, subtract on down). Better value estimate using average delta: `C + (ΔS)·Δ + ½·(ΔS)²·Γ`. **Gamma = magnitude/speed risk:** +gamma wants big fast moves; −gamma wants the market to sit still.

**Theta (Θ)** — time decay, value lost per day (expressed negative). ATM theta **grows as expiry approaches** (3 mo → −0.03, 3 wk → −0.06, 3 days → −0.16). Positive theta is possible only for a deep-ITM, European, stock-type-settled option with **negative time value** (rising toward intrinsic).

**Vega (κ/ν)** — value change per 1 vol point. **Always positive** for calls and puts. Long-term options have larger vega.

**Rho (ρ)** — value change per 1% rate change. Least important. Sign depends on instrument/settlement (futures-on-futures-settlement → 0; stock calls + / puts −).

**Underlying contract:** Δ = 100; gamma = theta = vega = rho = **0**.

**Interpreting a position (the key couplings):**
- **Gamma and theta are (almost) always opposite in sign and correlated in magnitude.** Movement helps (+gamma) ⟺ time hurts (−theta). You can't have both.
- **Gamma = realized-vol view; vega = implied-vol view.** They usually align but can diverge (underlying gets more volatile while implied vol falls, or vice versa).
- **Breakeven (implied) volatility of a position** ≈ evaluation vol + (total theoretical edge / total vega). This generalizes "implied vol" to whole positions.
- Risk tools *identify* risk; they don't eliminate it. Avoid both ignorance and **"paralysis through analysis."**

### Dynamic Hedging (Ch 8) — how edge is actually captured
- Buy/sell a mispriced option, hedge delta-neutral with the underlying, then **rehedge to delta-neutral at intervals** over the option's life. Each rehedge ends one "bet" and starts another; every bet carries the same favorable odds.
- The adjustments **force you to buy low / sell high** (sell underlying as it rises, buy as it falls). The P&L decomposes into: original hedge, adjustment cash flows, option carry, interest on stock/variation, dividends — *which* components win is random, but the **total ≈ the theoretical edge** if your vol input is right.
- **Replication principle:** the present value of all dynamic-hedging cash flows = the option's theoretical value. Dynamic hedging lets you, in effect, take the other side *at fair value*.
- **Breakeven volatility = the implied volatility at the trade price.** Above it the hedge wins; below it the hedge loses. If implied vol re-rates to your target quickly, you can close early at full profit (implied vol attaches to options, not the underlying).
- **Frictionless-market assumptions** (all violated in reality): free trading, unlimited borrow/lend at one rate, zero transaction costs, no taxes. **Transaction costs** are the real constraint: more frequent rehedging → tighter tracking but higher cost. Adjustments **don't change expected return** — they reduce the variance of outcomes (smooth luck). Retail (high cost) adjusts less and rides more variance; pros adjust often.
- **When to rehedge:** at fixed intervals, or when delta drifts past a set band, or by feel (if you genuinely have it), or not at all (accept the full directional risk, or close instead).

### Risk Measurement II — how the greeks themselves move (Ch 9)
- **Delta vs vol/time:** raise vol *or* time → all deltas move **toward 50**; lower vol or pass time → deltas move **away from 50** (toward 0 or 100). **Time and volatility act alike.** ⇒ no position is *certainly* delta-neutral (delta depends on the unknown future vol; many use the **implied delta**).
- **Gamma, theta, vega are all greatest ATM** — the central principle. ATM options are the traders' tools.
  - ATM **theta and vega are proportional to exercise price**; ATM **gamma is inversely proportional** to exercise price.
  - ATM **gamma rises as expiry nears or vol falls** (delta swings faster); ITM/OTM gamma does the opposite. ⇒ **ATM options near expiry in a low-vol market are the riskiest options to trade** (delta can rocket 0↔100).
  - ATM **theta ∝ √t** → `θ ≈ TV·(1 − √((t−1)/t))`, grows large into expiry. ATM vega is roughly **constant** in vol.
- **Higher-order ("non-traditional") sensitivities:** **vanna** (Δ to vol, = vega to underlying), **charm** (Δ to time / delta-decay), **volga/vomma** (vega to vol), **vega decay / DvegaDtime** (vega to time), **speed** (gamma to underlying), **color** (gamma to time), **zomma** (gamma to vol), **lambda/elasticity** (`Λ = Δ·S/TV`, % leverage — largest for OTM near expiry in low vol).

---

## Part IV — Spreading (Ch 10–13) and Synthetics (Ch 14)

### Why spread (Ch 10)
- A **spread** = opposing positions in related instruments whose values change at different rates. Most successful option traders are **spread traders**: spreading captures theoretical edge while **limiting the effect of short-term bad luck**.
- Casino lesson: spreading bets around the roulette table **keeps the same 5% edge but slashes short-run risk**. There is *no* risk-reward tradeoff in spreading the same edge — only variance reduction. Spreads also widen the **margin for error** on your vol estimate (the whole point — survive being wrong by a few vol points). Types: arbitrage (cash-and-carry), intramarket (calendar), intermarket (crack spread, NOB), ratio.
- **Long premium** = positive gamma (want movement); **short premium** = negative gamma (want quiet).

### Volatility Spreads (Ch 11) — the menu
Each is normally executed **delta-neutral**; classify by gamma/theta and vega:

| Strategy | View | Gamma | Theta | Vega |
|---|---|---|---|---|
| Long straddle / strangle | want movement + rising IV | + | − | + |
| Short straddle / strangle | want quiet + falling IV | − | + | − |
| Long butterfly / condor | want quiet + falling IV | − | + | − |
| Short butterfly / condor | want movement + rising IV | + | − | + |
| Ratio backspread (buy more) | movement / rising IV | + | − | + |
| Ratio frontspread (sell more) | quiet / falling IV | − | + | − |
| **Long calendar** | **quiet underlying BUT rising IV** | − | + | **+** |
| **Short calendar** | **big move OR falling IV** | + | − | **−** |

- **Straddle** = call+put same strike/expiry; **strangle** = different (OTM) strikes. Straddles/strangles have the **largest gamma/vega → riskiest** (whether long or short). A strangle of ITM options = a **guts**.
- **Butterfly** (1×2×1, equal strike spacing, one type) = a strangle/straddle with **limited risk and reward**: value at expiry ∈ [0, strike-width], max at the body. Long butterfly ≈ short straddle but capped → can be done in much larger size. Call and put butterflies (European) are **identical**.
- **Condor** = butterfly with two inside strikes (1×1×1×1). **Ratio spread** = unequal calls/puts, same type/expiry — straddle-like but limited on one side; delta-neutral ratio spreads (more sold) come in for a **credit**. **Christmas tree / ladder** = strangle-like with one side limited.
- **Calendar spread** (time/horizontal): same strike, different expiries. **Long calendar** = buy long-dated, sell short-dated (a debit). Two defining traits: (1) **gains value as time passes** (short-dated ATM decays faster — higher theta near expiry); (2) **gains value as IV rises** (long-dated has higher vega). The **unique signature: −gamma but +vega** — wants the underlying still yet everyone *expecting* a move (e.g., pending news). Big underlying moves **collapse** it (both options lose time value). In **futures**, different months have different underlyings → may need to hedge the calendar with a futures spread.
- **Time butterfly** = buy short-dated calendar / sell long-dated calendar (same strike, three expiries) → behaves like a long calendar (−gamma, +theta, +vega). Note the inversion vs. price butterfly: buying the wings here = a **credit**.
- **Interest/dividends on calendars (stock):** longer-dated forward is more rate/dividend sensitive. Long **call** calendar → **+rho**, **−dividend** risk; long **put** calendar → **−rho**, **+dividend** risk.
- **Diagonal** = calendar with different strikes; if same type & similar delta, acts like a calendar.

### Choosing & adjusting (Ch 11–13)
- **The master rule for picking spreads:** compare your vol estimate to implied vol. **IV low (options cheap) → choose +vega spreads** (long straddle/strangle, short fly/condor, backspreads, long calendars). **IV high (options rich) → choose −vega spreads** (short straddle/strangle, long fly/condor, frontspreads, short calendars). Long calendars when IV is low *and expected to rise*; short calendars when IV is high *and expected to fall*.
- **Adjustment choices:** (1) fixed intervals, (2) at a delta band, (3) by feel, (4) not at all (then pre-decide hold/close conditions). A delta adjustment **in the underlying is risk-neutral** (no gamma/theta/vega change); **in options it changes all the greeks.**

### Bull & Bear Spreads (Ch 12)
- Directional positions via options must still respect volatility. **Naked** calls/puts have little margin for error.
- Bias a ratio spread / butterfly / calendar by shifting the ratio or strikes — but a **−gamma directional spread can invert** (delta flips) on a big/fast move; a +gamma one can invert as vol falls or time passes. Volatility eventually outweighs direction.
- **Vertical spreads (credit/debit spreads)** are the clean directional tool: same type, same expiry, different strikes. **Stay bullish/bearish under all conditions.** Value at expiry ∈ [0, strike-width]. **Buy the lower strike / sell the higher = bullish** (calls *or* puts); reverse = bearish.
- **Selecting the vertical — focus on the ATM option** (most vol-sensitive in total points): **IV low → buy the ATM option** (then sell the OTM to make the spread); **IV high → sell the ATM option** (then buy the ITM). The spread containing the **ITM** option always costs more (it profits in more scenarios; +theta/−gamma); the one with the **OTM** option needs movement (+gamma/−theta). More movement expected → prefer the OTM-containing (cheaper) spread. Wider strikes → more delta and more max P&L.
- Verticals beat outright underlying: **limited risk**, and they can profit even if the market doesn't move your way (volatility dimension).

### Risk Considerations (Ch 13)
- Reward = **theoretical edge**; risk is multi-dimensional (delta/gamma/theta/vega/rho). **Edge alone is meaningless** — scale any edge by doing it bigger. Compare spreads at **equal theoretical edge**, then judge risk.
- **Volga matters at the tails:** a short straddle (volga ≈ 0) loses linearly in rising vol; a ratio spread (−volga) accelerates losses as vol rises; a long butterfly (+volga) decelerates losses and flattens — best tail behavior. So a butterfly can beat a "smaller" short straddle on real risk.
- **Straddles and strangles are the riskiest spreads, long or short** — least margin for error. Prefer structures with better risk characteristics even at slightly lower edge.
- **Sizing by margin for error:** small vol-margin → trade small; large vol-margin → trade larger. Raise the position's breakeven IV by increasing edge (without vega) or cutting vega (without edge).
- **Efficiency** = |gamma/theta| as a quick risk-reward proxy when all options expire together (bigger = better for +gamma; smaller = better for −gamma).
- **Adjustments and ego:** don't keep selling rich / buying cheap options forever — it balloons size and concentrates risk. When risk caps out: **reduce size** (swallow pride) or **adjust in the underlying**. A good spread isn't the one that wins biggest — it's the one that **loses least when things go badly**.
- **Trading style & gamma:** −gamma always adjusts *with* the trend; +gamma always adjusts *against* the trend. Match style (with/against trend) to gamma sign + adjustment frequency. **Liquidity:** the most liquid options are short-term, ATM/slightly-OTM; illiquid/long-dated/deep-ITM widen bid-ask. New traders → liquid markets; pros may prefer illiquid (wider edge) if they trust themselves.

### Synthetics (Ch 14)
- **The six synthetics (same strike & expiry):**
  - synthetic long underlying ≈ long call + short put; synthetic short underlying ≈ short call + long put.
  - synthetic long call ≈ long underlying + long put; synthetic short call ≈ short underlying + short put.
  - synthetic long put ≈ short underlying + long call; synthetic short put ≈ long underlying + short call.
  - Mnemonic: hedge a single option with the underlying and you've synthetically created the **companion** option (opposite type, same strike).
- **|call Δ| + |put Δ| ≈ 100.** Companion call & put have **identical gamma and identical vega** → vol traders make **no distinction between calls and puts** at a strike; flip between them by trading the underlying. (Theta can differ because of carry/cost-of-carry on the underlying or the options.)
- Synthetics explain why call & put **vertical spreads** at the same strikes are equivalent (call spread = debit, put spread = credit; values sum to PV(strike-width)).
- **Iron butterfly** = long strangle + short straddle (centered) = equivalent to a **long** (regular) butterfly but done for a **credit** (selling the iron fly = buying a regular fly). Iron + regular butterfly values sum to PV(strike-width). **Iron condor** analogously. Synthetics also let you re-express Christmas trees etc. into recognizable forms.

---

## Part V — Arbitrage, Early Exercise, Hedging (Ch 15–17)

### Option Arbitrage & Put-Call Parity (Ch 15)
- **Put-call parity:** `C − P = (F − X)/(1 + r·t)` (European). The call−put difference = PV of (forward − strike). Names: combo value, synthetic relationship, conversion market.
  - **Futures option, futures-settled:** `C − P = F − X` (rate = 0, no carry). Exchanges set settlement prices to honor this exactly.
  - **Futures option, stock-settled:** discount by `(1 + r·t)`.
  - **Stock:** compute forward `F = S(1+r·t) − D` first. **Approximation:** `C − P ≈ S − X + X·r·t − D` (call−put ≈ stock − strike + interest on strike − dividends).
- **Conversion** = short call + long put + long underlying (sell the synthetic, buy the real). **Reverse conversion (reversal)** = long call + short put + short underlying. Do a conversion when the **synthetic (combo) is rich**, a reversal when it's **cheap**. Everyone arbing forces C, P, and F back to parity within seconds.
- **Locked futures:** trade synthetic futures via options to get a price beyond the limit (`F = C − P + X`).
- **Implied checks:** if spot ≠ the parity-implied price, solve for the **implied interest rate** or **implied dividend** — the market may be pricing a dividend cut.
- **Arbitrage risks** (conversions/reversals are *low* risk, not *no* risk):
  - **Execution risk** — legging in; prices move before you complete.
  - **Pin risk** — underlying expires *at* the strike; you don't know if your short option is assigned until after expiry → could wake up naked long/short. ATM options *are* exercised (cheaper than trading underlying). Manage by **reducing size into expiry** or crossing conversions vs. reversals "at even money." No pin risk for cash-settled.
  - **Settlement risk** — options stock-settled but futures futures-settled → variation cash flows aren't offset by unrealized option P&L; a synthetic-vs-futures conversion has Δ ≈ `100/(1 + r·t)` (not exactly 100) — you prefer the market to **rise** (earn interest on variation). Bigger with higher rates / longer time.
  - **Interest/dividend risk** (stock): conversion has −rho, +dividend exposure; reversal the opposite.
- **Three-way:** replace the underlying in a conversion/reversal with a deep-ITM option (Δ≈100). **Box** = conversion at one strike + reversal at another → no underlying position; worth PV(strike-width) at expiry; = lending/borrowing (selling a box cheaper = borrowing at a higher rate). Box = a bull call spread + a bear put spread. **Roll** = synthetic long one month + synthetic short another (same strike); value ≈ `X·r·t − D` (carry on strike less dividends); = call calendar minus put calendar. **Time box** / **diagonal roll** = synthetics at different strikes *and* months.
- **Using synthetics to trade better:** there are three ways to buy a straddle (outright, or buy one leg + synthesize the other); pick the cheapest after put-call parity. Likewise the cheapest of call fly / put fly / short iron fly. Edge from synthetics is usually tiny but real over a career.

### Early Exercise of American Options (Ch 16)
- **With no dividends or interest benefit, American = European value.** (True for futures options under futures-type settlement.)
- **Arbitrage boundaries:** an American option **never trades below intrinsic value.** A European option *can* (it's worth the PV-of-intrinsic floor): a European call's lower bound is `max[0, (F−X)/(1+r·t)]`; for stock `≈ S − PV(X) − D` (can be > 0 even when OTM in forward terms). Below the floor → free arbitrage.
- **Value decomposition:**
  - **Call** = intrinsic + **volatility value** + **interest value** − **dividend value**.
  - **Put** = intrinsic + volatility value − interest value + dividend value.
  - Estimate **volatility value ≈ price of the companion OTM option**; **interest value ≈ carry on the strike** (`X·r·t`); **dividend value ≈ total dividend**.
- **When to exercise early:**
  - **Call (stock):** only if dividend value > volatility value + interest value — and only worth doing the **day before the ex-date** (you give up vol+interest value each day; you only gain by capturing the dividend). **No dividend ⇒ never exercise a stock call early.**
  - **Put (stock):** exercise when interest value > volatility value + dividend value — most often *on* the ex-date, but possibly any time. **Blackout:** never exercise within `dividend / (daily interest on strike)` days of a dividend.
  - **Futures option (stock-settled):** exercise when `interest on intrinsic > volatility value`; exercise the day the **companion's theta < the daily interest**.
- **Short stock** lowers the rate → makes **calls more** likely early-exercised, **puts less** (consistent with "avoid short stock").
- **Protective trick:** when you exercise, simultaneously buy the companion OTM option to keep the protective value you'd otherwise surrender. **Selling** an early-exercise candidate beats exercising *if* it trades above intrinsic (rarely, given illiquidity).
- **Pricing American options:** Black-Scholes can't. **Cox-Ross-Rubinstein (binomial, 1979)** — a loop; handles dividends well. **Barone-Adesi-Whaley (quadratic, 1987)** — faster, but treats cash flows as continuous (worse for lump dividends). **Optimal early exercise** ⟺ theoretical value = parity *and* delta = 100. Difference between American & European value grows as the option goes deeper ITM and as vol *falls*.

### Hedging with Options (Ch 17)
- **Protective option** (buy a put for a long, a call for a short) = insurance: capped downside (strike = your deductible) + open upside; cost = the premium. = a synthetic long option. Rate-hedge versions are **caps** (borrower buys rate calls) and **floors** (lender buys rate puts). Most protective options expire worthless — like all insurance; you buy them for protection, not profit.
- **Covered write / overwrite** (sell an option against the underlying) = synthetic short option; credit gives limited downside protection, caps upside. **Buy/write** (buy stock + sell call simultaneously, quoted as one price; CBOE **BXM** index). Sell a call to set a **target sell price**; sell a **cash-secured put** to set a **target buy price** (used in buybacks).
- **Choosing buy vs. sell** = price vs. value (compare IV to expected vol), but **practical protection needs may override theory.**
- **Collar** (long underlying + protective put + covered call) = a **vertical spread** (long collar = bull spread, short = bear) — known protection at low/zero cost ("zero-cost collar"). a.k.a. fence/tunnel/cylinder/split-strike conversion.
- **Complex hedging principle:** **in a high-IV market, buy as few / sell as many options as possible; in a low-IV market, buy as many / sell as few.** Hedge a fraction of directional risk by matching total delta (e.g., −50 deltas of puts to hedge half a long). Restrict unlimited risk to your natural direction.
- **Volatility drag (why hedging helps returns):** higher return *variance* lowers compounded return. Compare arithmetic mean to the **product** of (1+returns); the steadiest manager often wins. **Sharpe ratio** = mean return / σ of returns.
- **Portfolio insurance / option replication:** replicate a protective put you can't buy by **dynamically hedging** (hold a delta = the synthetic call's delta; sell down as delta falls, buy back to expiry). Works only if inputs/assumptions hold — the 1987 crash's **gaps** broke continuous hedging and made the "insurance" far costlier than modeled (and arguably worsened the crash).

---

## Part VI — The Models in Depth (Ch 18–19)

### Black-Scholes (Ch 18)
- The PDE answers: *what option price, with continuous delta-hedging, just breaks even at constant r and σ?* Its terms are the **delta, gamma, theta**, plus the rate term `rS` (spot→forward) and `rC` (expected value→present value), and a vol term scaling the gamma. It mirrors the average-delta estimate `(ΔS)·Δ + ½(ΔS)²·Γ`.
- **Solution:** `C = S·N(d1) − X·e^(−rt)·N(d2)`.
  - **N(d1) = the delta** (average value of stock above the strike).
  - **N(d2) = the true probability** the option finishes ITM (× X = expected payout). **N(d1) > N(d2) always** → delta overstates the ITM probability. ⇒ at-the-forward call Δ slightly > 50, put Δ slightly > −50, so an **at-the-forward straddle is slightly long delta**; it's exactly delta-neutral when the forward sits *below* the strike by `e^[−(r+σ²/2)t]` (further below as time/vol grow).
  - d1, d2 are just the log-moneyness adjusted for the interest drift and the lognormal mean-shift `σ²t/2`, divided by `σ√t`.
  - Extend to other underlyings with a cost-of-carry factor `b`.
- **The 40% rule (must-have approximation):** an exactly **at-the-forward** option's expected value ≈ `0.4 × σ × √t × F` (since the standard normal peak ≈ 0.3989; per 1 vol point on a 100 strike, 1-yr value ≈ 0.399). Theoretical value = discount that. ATM value is **∝ exercise price** and **∝ √t**. Applies to calls and puts (put-call parity). Slightly overstates true BS at high vol/long time (ATM vega declines a touch with vol).
- **Theta** has three parts: vol-value decay (the "**driftless theta**," dominant; same sign for companion call/put), the spot→forward drift, and the PV change. **Max gamma/theta/vega** occur *near* ATM but not exactly: at b=0, max gamma & theta sit *above* the strike, max vega *below*. Raising rates lowers the price of max gamma/vega and raises the price of max theta. (Max gamma ⟺ speed=0; max theta ⟺ charm=0; max vega ⟺ vanna=0.) For stock options, raising rates can make **vega fall** with more time (the option drifts off-the-forward).

### Binomial / Cox-Ross-Rubinstein (Ch 19)
- **Risk-neutral world:** find probability p making you indifferent to buying/selling — expected value = forward. `p = (forward-factor − d)/(u − d)`. Option value = PV of probability-weighted terminal intrinsic values, worked **backwards** node by node.
- **u and d** are chosen recombining and inverse (`u·d = 1`, no drift) and set from vol as a one-σ move per step: `u = e^(σ√(t/n))`, `d = 1/u`. More steps → converges to Black-Scholes (error oscillates, shrinks; 50–100 steps typical; half-step averaging improves accuracy).
- Greeks fall out of the tree (delta, gamma, theta from node values; vega/rho by re-running with bumped inputs). The tree **demonstrates dynamic hedging**: a delta-neutral hedge at theoretical value breaks even each step *after* counting interest on the cash flow.
- **Gamma rent:** volatility trading = **"renting the gamma," the rent = theta.** Over each step, the move needed to break even ≈ **one standard deviation** (= u/d magnitude). +gamma/−theta makes money on movement, loses to time; −gamma/+theta the reverse.
- **American options:** at each node replace the European value with intrinsic if intrinsic is larger, then keep rolling back. This also shifts the delta/gamma. **Dividends** reduce post-dividend node prices (early dividends break recombination → approximate by reducing all later nodes by total dividends). **Pseudoprobabilities:** at very high rates p can exceed 1 / 1−p go negative — the stock's potential move can't offset interest; requires `u > 1 + r·t/n`.

---

## Part VII — Vol Revisited, Position Analysis, Stock Indexes (Ch 20–22)

### Volatility Revisited (Ch 20)
- **Held to expiry, only realized volatility matters; implied volatility matters more the *shorter* you hold.** (A long straddle can lose despite rising IV if time decay outweighs it, or win despite falling IV if the underlying moves.) Price still matters for cash flow/capital, but value = realized vol.
- **Historical vol calc:** use the **sample** standard deviation (÷ n−1) since it estimates the future; data = **log returns**; usually a **zero-mean** assumption (the "deviation from average" feel is wrong to traders — 1%/day forever should not read as 0 vol). 250–260 trading days/year (or all 365 with zeros for closed days when comparing exchanges). Daily returns preferred (more data points). **Extreme-value estimators:** **Parkinson** (high-low) and **Garman-Klass** (open-high-low-close) capture intraday range; weight them with close-to-close when markets aren't continuous.
- **Volatility's character:** **mean-reverting** (gyrates around a long-run mean — e.g., gold ~10–20%, S&P ~15–20%, Bund ~5%) and **serial-correlated** (next period ≈ last period). **Term structure of volatility** (the volatility "cone"): variation is large over short windows, small over long windows → **long-run vol is *easier* to forecast than short-run**, but long-dated options have higher vega so a small long-dated vol error hurts more.
- **Forecasting:** weight recent data more (regressive weighting), but match the **window to the option's life** (serial correlation) — short options → short-term data, long options → long-term/mean. **EWMA** (`λ ≈ 0.94`) weights recent returns more. **GARCH** adds correlation-of-returns + mean-reversion to an EWMA-type base.
- **Implied vol as a predictor:** lags realized vol and is **usually too high** (options tend to be overpriced — an insurance premium, plus hedging/replication costs and model weaknesses). But it can be wildly *too low* before a vol explosion (2008).
- **Term structure of *implied* vol:** short-dated IV is more volatile (mean reversion compresses long-dated IV changes). To assess vega risk across months, scale each month's vega by its **rate of change vs. a primary month** ("whippiness" factor) — a total-vega of 0 can still be net long/short once scaled. Front-month IV often disconnects from the curve. **Seasonal** factors exist (ag summers, natural-gas October/hurricane season).
- **Forward volatility:** since variance ∝ time, `σf²·(t2−t1) = σ2²·t2 − σ1²·t1`. Calendar-spread implied vol and forward vol both act as a **magnifying glass** to spot a mispriced expiration month (e.g., buy the cheap-vol month's calendar, sell the rich). ATM calendar implied vol ≈ spread price / spread vega.

### Position Analysis & Market Making (Ch 21)
- Re-express complex books via **synthetics** into one option type to reveal the structure. But a full picture needs the model **and** scenario analysis: today's greeks are only valid *now* — ask what happens as price moves, vol changes, and time passes.
- **Graphical reads:** −delta graph slopes down-right; +delta up-right. **−gamma = "frown"** (movement hurts), **+gamma = "smile"** (movement helps). Inflection point = where gamma flips sign.
- **The net contract position is essential:** if the market gaps far, all puts act like short underlyings / all calls like long underlyings — what underlying position are you left holding? Big moves happen more than models predict; very-OTM shorts still carry margin (buy them back via **cabinet bids**).
- **Position implied (breakeven) volatility** ≈ eval vol + edge/vega — your vol margin for error. Estimate the price you most want (−gamma position wants to be delta-neutral) via `S − delta/gamma`.
- **Market making:** quote a two-sided market (width & size set by exchange rules; "quote for size" on big orders). Three questions: *what does the market think it's worth, what do I think, what am I carrying?* Profit from the **bid-ask spread** (find the equilibrium price) and from **theoretical mispricing** (dynamic hedge). Manage by **skewing quotes** to acquire risk-reducing trades, watching how risk evolves, and **diversifying** — concentration of risk at one strike/expiry is dangerous even if net greeks are small. Goal: positive edge + intelligently managed risk; ask "what if it moves against me / for me / what can I do now."

### Stock Index Futures & Options (Ch 22)
- **Index types:** price-weighted (Dow — divisor-adjusted), cap-weighted (S&P 500), equal-weighted; **total-return** (DAX) adjusts the divisor for dividends. **% change in index = % change in stock × its weight.** Price-weighted: each 1-pt stock move changes the index by `1/divisor`. Use weights to estimate fair index value when a stock is halted; **VWAP** smooths the closing print.
- **Index futures** are **cash-settled** (delivering the basket is impractical). Fair forward `F = S·[1 + (r − d)·t]` (treat dividends as a negative rate) — but discrete, lumpy dividends make this rough for **short-dated** contracts.
- **Index arbitrage / program trading:** buy/sell futures vs. the basket; **the hedge is delta-based** — hold `(1 + r·t)` units of stock per future (more than 1:1 at high rates/long time; settlement risk because futures cash-settle daily while stock P&L is unrealized). Rate/dividend changes affect profitability (esp. long-dated / narrow indexes). AM vs PM expiration; "**triple witching**." **Structural downward bias** on index futures: most portfolio managers are long stock and hedge by *selling* futures; arbitrageurs can't easily short the basket → persistent selling pressure.
- **Options on index futures** behave like any futures option (exercise → futures position). **Options on a cash index** are **European, cash-settled** (early-exercise nearly killed OEX). Hedge cash-index options with the **futures** that expires with the options; for serial months with no matching future, back out the **implied forward** via put-call parity from a near-ATM call/put.

---

## Part VIII — Where the Model Breaks: Real World, Skews, Vol Contracts (Ch 23–25)

### Models and the Real World (Ch 23)
Six core assumptions of traditional models — each flawed:
1. **Frictionless markets** — false: price limits/locks, short-sale restrictions (inflate puts), no unlimited borrow/lend, different borrow vs. lend rates, taxes, and above all **transaction costs** (which compound with every rehedge).
2. **Constant interest rates** — traders constantly borrow/lend at variable rates; rate risk is minor for short-dated options but real for **deep-ITM long-dated** ones (high rho).
3. **Constant volatility** — false; vol comes in high/low regimes. **Value is path-dependent under dynamic hedging:** the *same* realized vol gives very different straddle outcomes depending on *when* the moves happen. **ATM** options gain most from high vol **near expiry** (gamma peaks late) → worth more than BS in a rising-vol path, less in a falling-vol path; **OTM** options are the reverse (their gamma peaks early). On *average* over many random paths, BS is right (it's probabilistic). **Stochastic-vol** and special interest-rate models exist but add complexity.
4. **Continuous trading (diffusion)** — false; the real world is **jump-diffusion** (gaps at opens and on news). A gap devastates a **short ATM option near expiry** (huge gamma + no chance to adjust); the same gap helps a +gamma position. Gaps are why a traditional model **undervalues** options (implied > historical on average). **Don't sell large numbers of ATM options into expiry.** Conversely, cheap **expiration straddles** can be a +EV bet on a gap (like a mispriced roulette bet — lose often, win big) — often left un-adjusted because deltas are unreliable that close to expiry.
5. **Volatility independent of price** — false. Stock indexes get **more volatile falling** (inverse); commodities **more volatile rising** (direct). ⇒ the **CEV model**; ⇒ a delta-neutral index straddle is really delta-*negative* (you prefer the down-move that brings higher vol).
6. **Lognormal terminal prices** — false. Real return distributions have **more small moves, more big moves (fat tails), fewer intermediate moves** than normal. Described by **skewness** (lopsidedness; left-skew = fatter down-tail) and **kurtosis** (peakedness + tail-fatness; positive/leptokurtic = "fat tails"). Real "black-swan" moves (8+ σ) occur that a normal distribution says are essentially impossible.

### Volatility Skews (Ch 24)
- **Implied vol varies across strikes** — the model is admitting its own inefficiency. The marketplace is *trying* to be efficient given the model's flaws and hedging flows.
- **Three skew shapes** (driven by hedging demand + the vol-price relationship):
  - **Investment skew** ("skew to the downside"): lower strikes carry higher IV. Typical of **stocks/indexes** — investors buy low-strike protective puts and sell high-strike covered calls; markets get more volatile falling.
  - **Demand / commodity skew:** higher strikes carry higher IV (end-users hedge rising prices).
  - **Balanced skew:** roughly symmetric (FX — both sides hedge).
- **Treat the skew as a model input** — fit it (e.g., polynomial `y = a + b·x + c·x²` where **a = ATM vol, b = skewness, c = kurtosis**). Calibrate the x-axis by **moneyness / standard deviations** (`ln(X/S) / (σ√t)`) and the y-axis relative to ATM IV. **Sticky-strike** (fixed vol per strike) is unrealistic; markets use a **floating / sticky-delta** skew that shifts with price and IV. Combine skew (across strikes) with term structure (across expiries) → a **volatility surface**.
- **Skew risk measures:** the skew changes the **delta** (a +vol-shift on a falling underlying lifts OTM put vol → "skewed/adjusted delta"). Many traders use the skew for *values* but a plain model for the *greeks* to stay manageable. Common skew benchmark: **IV(−25Δ put) − IV(+25Δ call)** for skewness; ±5Δ wings for kurtosis.
- **Skew/kurtosis strategies:** trade the slope with a **risk reversal** (buy puts/sell calls or vice versa, hedged delta-neutral, usually chosen **vega-neutral** at the 25Δ wings). Trade curvature with strangles vs. straddles — a vega-neutral **2×1 strangle:straddle = a "dragonfly."** Trade skew/kurtosis *between* expiries with calendarized versions.
- **Implied distribution from butterflies:** the price of the X−ΔX / X / X+ΔX butterfly ÷ total ≈ the market's implied **probability** of finishing at X. Summed over all strikes (infinitesimally narrow) you recover the implied distribution. Stock indexes imply: more chance of small-to-intermediate up-moves and **large down-moves**, less chance of small-to-intermediate down-moves and large up-moves vs. lognormal.

### Volatility Contracts (Ch 25)
- Motivation: dynamic-hedging a vol view is costly and **path-dependent**. Vol contracts let you take a clean vol position; value at expiry rests on a straightforward calc.
- **Realized-volatility / variance contracts (variance swaps):** settle into realized σ over the period (population σ, log returns, zero mean). Quoted in **vol points + notional vega** but usually **settled in variance points** (variance = σ²) because (a) variance is replicable and (b) **variance is additive over time**. Each variance point = `notional vega / (2 × vol price)`. Payoffs escalate with σ² → sellers often want a **cap** (common on single names, rare on indexes). Mostly OTC (counterparty risk).
- **Implied-vol contracts / the VIX:** a constant **30-day implied vol** of S&P 500 (SPX) options (since 2003). **New methodology (Goldman 1999):** price a **strip of OTM options across all strikes weighted 1/X²** → *constant* vol exposure (vega is highest ATM, so weight low strikes more). **No model needed** — just option prices + the risk-free rate (forward via put-call parity). Uses two expirations bracketing 30 days; settlement from special **opening-rotation** trade prices.
- **VIX behavior:** strongly **inversely correlated with the S&P 500** (~−0.74; % move ~5.7× and opposite) → the "**fear index.**" It does **not** reliably predict future realized vol — it reflects **demand for protection** in falling markets. Falling markets *are* moderately more volatile (~−0.39).
- **Trading the VIX (the gotchas):** VIX itself isn't easily traded → use **futures/options**. (1) Futures show a **term structure** (usually **contango**, sometimes backward) and **decay down the curve** in contango as time passes. (2) **Futures move less than the index** (they price expected IV at *their* maturity), converging only at expiry — buyers/sellers are routinely disappointed. (3) **VIX options** carry lower IV than the index's volatility (they're hedged with the *less-volatile futures*) and a distinctive **"half-frown" skew** (low strikes drop off fast, high strikes flatten) reflecting mean-reverting, bounded vol. Spread futures with the term structure: in a curved contango, sell long/buy short if you expect flattening toward backward; reverse for backward→contango.
- **Replication:** a variance position = a **1/X² strip of options, dynamically hedged** to delta-neutral. A *volatility* position can't be perfectly replicated (σ = √variance → non-constant exposure) — hence settlement in variance. VIX replication is hard (strip expiry mismatches, ITM-option conversion, no easily traded SPX underlying).
- **Applications:** speculate on realized (variance swap) or implied (VIX) vol; hedge a gamma book (variance) or vega book (VIX); hedge **equity portfolios** (long VIX offsets falling stocks); hedge **indirect** vol exposure — a market maker long "volume," a manager facing costly rebalancing, or a **covered-call writer** (who is short vol — wants the market still) all hedge by going **long VIX**.

---

## Afterword — A Final Thought
Using a model means making many fallible decisions; you'll be wrong about some inputs, and luck matters short-term. But **in the long run, traders who deeply understand the model — strengths *and* weaknesses — come out ahead.** Have faith in the model, but not **blind** faith: when values defy common sense or conditions move too fast, adjust it or set it aside. **Trading is art and science.** Know what a model can and cannot do, and **make the model your servant, not your master.**

---

## Practical Rules & Heuristics (consolidated)
- **Buying options needs both direction and speed right; selling collects premium for low-probability risk.** Spread to keep edge and cut short-run variance.
- **√t scaling:** daily σ ≈ annual/16; weekly σ ≈ annual/7.2. Expect a >2σ day ~once a month.
- **40% rule:** at-the-forward value ≈ `0.4·σ·√t·F`. ATM value ∝ strike and ∝ √t. ATM vega ≈ constant; ATM theta ∝ √t and spikes into expiry.
- **Gamma, theta, vega are all greatest ATM.** Gamma & theta are opposite-signed and correlated. Gamma = realized-vol view; vega = implied-vol view.
- **Strike-selection rule (verticals & hedges):** IV **low → buy** the ATM option; IV **high → sell** the ATM option.
- **Spread-selection rule:** IV low → **+vega** structures; IV high → **−vega** structures. Long calendars when IV is low & expected to rise; short when high & expected to fall.
- **Hedging-quantity rule:** high-IV market → buy few / sell many options; low-IV → buy many / sell few.
- **Straddles & strangles are the riskiest spreads (long or short).** A good spread loses least when wrong, not most when right. Size to your **margin for error**.
- **|callΔ| + |putΔ| ≈ 100;** companion calls/puts share gamma & vega. Adjust delta in the **underlying** to stay risk-neutral; in **options** to change greeks (and edge).
- **Put-call parity:** `C − P = (F − X)/(1+r·t)`; stock approx `C − P ≈ S − X + X·r·t − D`. American ≥ intrinsic; European can trade below intrinsic.
- **Early exercise:** stock **calls** only the day before ex-date (and only if dividend > vol+interest value); stock **puts** when interest > vol+dividend value. No dividend ⇒ never exercise a stock call early. Avoid short stock.
- **Gamma rent = theta; breakeven move per rehedge ≈ one σ.** Optimal early exercise ⟺ value = parity and Δ = 100.
- **Don't sell big ATM size into expiry** (gap risk); cheap expiration straddles can be +EV.
- **Investment skew** in stocks/indexes (downside vol bid); **demand skew** in commodities (upside bid). Delta-neutral index straddle is really delta-negative.
- **Held to expiry → realized vol is all that matters; implied vol matters more the shorter the hold.** Implied vol is usually a bit too high (insurance).
- **VIX:** ~−0.74 to S&P, a fear gauge not a forecast; futures move less than the index and decay down a contango curve.

## Appendix — Useful Math (formulas)
- **Interest:** simple `P(1+r·t)`; compound `P(1+r/m)^(mt)`; continuous `P·e^(rt)`. Volatility is a **continuously-compounded** rate of return → use `e^x` / `ln`.
- **n-σ price range** around forward F: `F·e^(±n·σ√t)`. **Std devs to a strike:** `ln(X/F)/(σ√t)`.
- **Mean** `µ = Σxᵢ/n`. **Population σ** `√(Σ(xᵢ−µ)²/n)`; **sample σ** `√(Σ(xᵢ−µ)²/(n−1))` (used for forecasting historical vol).
- **Standard normal** `n(x)` has µ=0, σ=1, area 1; peak ≈ 0.3989. **Skewness** from the 3rd moment, **kurtosis** from the 4th (normal kurtosis = 3, usually reported as 0 by subtracting 3).
- **Annualized vol:** `σ = √(Σxᵢ²/(n·t))` with `xᵢ = ln(pₙ/pₙ₋₁)`, t = interval in years (zero-mean, log returns); annualize by dividing by √t (÷√(days-interval/365)). Sample σ > population σ; actual-mean vs zero-mean differ negligibly.

---

*Source: Sheldon Natenberg, "Option Volatility and Pricing: Advanced Trading Strategies and Techniques," 2nd ed. (McGraw-Hill, 2015). This document is an internalized distillation for reference and application, not a substitute for the text.*

