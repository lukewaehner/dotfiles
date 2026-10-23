---
name: warrant-vol-arb
description: Decide whether a company-issued warrant (SPAC/de-SPAC or any listed warrant, tickers usually ending W/WS/WT) is CHEAP, FAIR, or RICH as a volatility instrument, and if cheap size a delta-hedged long-warrant/short-stock trade. Use whenever the user asks to analyze, value, or screen a warrant, asks if a warrant is cheap or expensive, mentions warrant arb, wants a warrant desk brief, or pastes a warrant ticker. Pulls live tape only from the Bloomberg Terminal (DES/HVT/OMON; no market-data MCP), then verifies the strike, redemption mechanics, and true 5y-post-merger maturity from the warrant agreement on SEC EDGAR, read in the user's local Claude-in-Chrome browser (engage it first; web-fetch is a last resort). For SPAC warrants the $18 redemption is a soft-call knockout, not a hard price ceiling, so the headline is a redemption-aware Monte-Carlo, not Black-Scholes. With listed options it adds an implied-borrow term-structure panel (PCP by tenor). Always use this skill for warrant cheap/rich questions.

---

# Warrant Volatility Arbitrage

Decide whether a long-dated, company-issued warrant is **cheap, fair, or rich** as a volatility
instrument, and if cheap, size a delta-hedged **long-warrant / short-stock** trade. This works for
**any warrant on any underlying**, and is tuned for the **SPAC / de-SPAC warrants** that dominate the
desk's flow — the whole workflow is parameterized by what you pull from Bloomberg AND verify from the
warrant's actual SEC filing.

> **Start here — load the framework first.** Before anything else, read `references/natenberg.md`. It
> is your internalized background on options and volatility — the greeks, implied vs realized vol,
> forwards / cost-of-carry, dynamic hedging, mean reversion and the term structure of vol, skew, and the
> pricing models. Everything here — the pricing, the cheap/fair/rich call, the sizing, and especially
> the explanations — assumes that grounding, so read it up front.

## Two ideas make this work

A warrant is a **long-dated call** (often 3–5 years). Two features dominate its value, and a terminal's
headline implied vol ignores both:

**1. Cost-to-borrow.** Borrow enters the forward as `F = S·e^(r − borrow)·t` and **compounds over the
whole life of the warrant**, so it is the single biggest driver of a long-dated warrant's value (short
listed options are borrow-insensitive). Bloomberg's OVME implied vol usually assumes ~0 borrow and looks
deceptively cheap. **Re-solve the warrant's implied vol at the REAL stock-loan borrow** before comparing
it to anything. Get the actual rate from the stock-loan desk — do not infer it from listed-option
put-call parity (put-skew demand contaminates it).

**2. The redemption — an $18 *knockout*, not a hard price ceiling.** Almost every SPAC warrant lets the issuer
**redeem all warrants for $0.01 once the stock holds ≥ $18 for 20 of 30 trading days** — but read the
mechanic carefully, because it is a **soft call, not a $6.50 ceiling.** The trigger starts a **~30-day
redemption notice (about a month, ≈24 trading days)** in which the holder **sells the warrant in the
market, or exercises it (cash or cashless) to keep the intrinsic at the then-price.** Only a holder who
sleeps through the window is actually liquidated at $0.01. So what the knockout takes from you is the
warrant's **remaining multi-year time value** — you are forced to convert early — **not the intrinsic
upside** (if it is called at $25 you keep ~$13.50, not $6.50). Some agreements also carry a **$10.00
make-whole redemption**. Plain Black-Scholes still overstates the warrant because it ignores this forced
early conversion, but the haircut is only that **time-value give-up**: for a deep-OTM name it is often
just a **few vol points** (the intrinsic is preserved), **not** a tail-removing ceiling — so do not over-credit
it. The **headline number is the redemption-adjusted ("knockout-adjusted") implied vol from the Monte-Carlo
engine**, which values a called warrant as the residual call you actually keep (intrinsic-plus-a-little),
not a $0.01 stub; vanilla BS is reported only as an upper-bound reference.

There is also a **break-even borrow** — the rate at which the warrant's (knockout-adjusted) vol equals the
listed front-month vol. Below it the warrant is cheap; above it there is no edge.

## Trust the tape, verify the terms

Bloomberg gives you the live tape (prices, realized vol, listed IV). But **Bloomberg's warrant
*contract terms* — strike, expiration, redemption trigger — are frequently INDICATIVE and wrong.** On the
DES screen Bloomberg literally prints "EXPIRATION DATE & EXERCISE PRICE INDICATIVE ONLY." A common, costly
error: Bloomberg keys the expiry off the IPO/issue date, but a SPAC warrant actually expires **5 years
after the business-combination close**, which can be a year or more later than Bloomberg shows. A wrong
maturity feeds straight into the vol solve.

**So every run verifies the contract terms against the warrant agreement on SEC EDGAR, by driving
edgar.sec.gov in the user's LOCAL Claude-in-Chrome browser** (see `references/edgar_terms.md`). This is mandatory, not optional —
the verdict pivots on the strike, the redemption mechanics, and the true maturity, and these come from
the filing, not the terminal.

## Data sources — drive the Bloomberg Terminal and SEC EDGAR yourself (no data MCP)

This is a **"drive the apps" workflow by design, and it deliberately uses no market-data MCP.** The tape
is pulled by **taking control of the Bloomberg Terminal** (computer-use / Citrix); the contract terms are
read by **driving SEC EDGAR in the user's LOCAL Claude-in-Chrome browser**. The desk wants this analysis sourced and shown from the
live Terminal and the actual filing on screen — the OMON surface, the HVT term structure, and the
warrant-agreement language *seen and auditable in their native context*, not fetched as bare numbers.

- **The Bloomberg Terminal is the ONLY source for tape** (DES / HVT / OMON / spot — every price and vol).
  Do **not** use a quote / market-data MCP (e.g. `get-price`, `get-option-chain`, `get-option-data`,
  `get-vwap`, `get-company-info`, `spac-details`), **not even as a cross-check or a fallback.** If Citrix
  is genuinely unavailable, stop and tell the user — a number whose provenance you can't show on the
  Terminal does not belong in the brief. The Terminal's own SEAR build often routes a free-typed
  `TICKER Equity FUNCTION` into search; load the security first, then run the function (see
  `references/bloomberg_pulls.md`).
- **SEC EDGAR in the user's LOCAL Claude-in-Chrome browser is the source for every contract term.** Engage that browser first — call `mcp__Claude_in_Chrome__list_connected_browsers`, then `select_browser` to connect to and select the user's local Chrome (the one running the Claude extension), and confirm it is connected; if none is connected, stop and ask the user to open it (never a sandboxed/headless browser). Open the warrant agreement in that browser
  so it is seen on screen. Do **not** use an EDGAR data MCP (`edgar-filings`, `edgar-filing-text`, …) to
  read filings.
- **The warrant agreement is long — don't let that push you back onto an MCP.** A full agreement
  (~130k+ characters) overflows the browser's single read-page limit. The fix is **not** a data MCP; it is
  to **read it section-by-section in the local browser with `find`** — and only as an explicit LAST RESORT fetch the EDGAR document with the approved
  web-fetch tool, save it into the deal folder, and grep the operative sections. That gives a permanent,
  citable copy and keeps the EDGAR-MCP out of the loop. Full mechanics — including the in-browser
  targeted-read alternative — are in `references/edgar_terms.md`.

## Workflow

0. **Load the framework.** Read `references/natenberg.md`.
1. **Identify the warrant.** The user gives a warrant ticker (or a company — find its warrant; the
   warrant usually shares the root + `W`/`WS`/`WT`).
2. **Pull live tape from the Bloomberg Terminal** by taking control of the laptop — warrant DES, underlying
   HVT (realized vol), OMON (listed IV), spot. Read prices/vols here, but treat strike/expiry/redemption
   as **indicative only**. See `references/bloomberg_pulls.md`. The Terminal is the **only** source for
   tape — there is no data-MCP fallback (see *Data sources* above).
3. **Verify the contract terms on SEC EDGAR in the user's LOCAL Claude-in-Chrome browser** (`references/edgar_terms.md`) —
   **mandatory**. First engage the local Chrome (`list_connected_browsers` / `select_browser`; if none is
   connected, stop and ask the user to open it — never a sandboxed browser), then read the agreement
   section-by-section in-browser with `find` per `references/edgar_terms.md`, using the sandboxed web-fetch
   only as a last resort and never a data MCP.
   Confirm from the warrant agreement: the **strike**, the **redemption mechanics** ($18
   cash redemption? $10 make-whole? the 20-of-30-day trigger, 30-day notice, cashless terms, any
   anti-dilution adjustment to the $18 level), and the **true expiration** (almost always *5 years after
   the BC close* — find the BC close date and compute it; do not use Bloomberg's date).
4. **Get the cost-to-borrow** from the user / stock-loan desk. This and the verified terms are the
   make-or-break inputs.
5. **Assemble the inputs JSON** (schema in `references/inputs_schema.md`), including the verified
   redemption terms and maturity.
6. **Price it.**
   - **SPAC / de-SPAC warrant (has a redemption feature) → knockout-aware Monte-Carlo is the headline.**
     Run `python3 scripts/warrant_knockout_mc.py inputs.json`. It reports the **knockout-adjusted implied vol**
     (and a band reflecting how aggressively the issuer redeems), the **vanilla no-knockout IV** as an
     upper-bound reference, the edges vs listed/realized, greeks, sizing, and the chart series. It writes
     `inputs.knockout.json`.
   - **Warrant with genuinely no redemption feature →** the vanilla engine is sufficient: run
     `python3 scripts/warrant_arb.py inputs.json` (Black-Scholes + Merton carry, break-even borrow).
   - Either way you can also run `warrant_arb.py` for the borrow-vs-break-even view; just don't quote its
     vanilla IV as the headline when a knockout exists.
7. **Interpret** the CHEAP / FAIR / RICH verdict (below).
8. **Build the desk brief:** `python3 scripts/build_brief.py inputs.knockout.json --out <TICKER>_brief.pdf`
   → a Letter-landscape PDF (verdict + inputs/outputs, the vol ladder + value-vs-vol + knockout
   charts, and trade/execution/risks). Present it.
9. **(If the underlying has listed options) Add the implied-borrow term structure.** Borrow is the swing
   input, so when an options market exists, corroborate it from put-call parity: pull the trailing ~30
   sessions of ATM-bracket option mids (plus each day's spot) from the local terminal, run
   `python3 scripts/implied_borrow.py obs.json`, then pass `--borrow-curve obs.borrow_curve.json` to
   `build_brief.py` — it adds a page laying the option-implied borrow term structure (10d & 30d) against
   the warrant-implied borrow (the rate you priced with, marked as a star). Skip for names with no listed
   options (e.g. most micro-cap de-SPACs, where OMON is not supported). See `references/implied_borrow.md`.

## The pricing model — knockout-aware by default for SPAC warrants

The bundled `warrant_knockout_mc.py` prices the warrant with a **Monte-Carlo** (daily GBM, antithetic) under
the risk-neutral drift `r − borrow`, imposing the **actual redemption rule**: the issuer redeems once the
stock satisfies the 20-of-30-day ≥ trigger condition; during the 30-day notice the holder keeps a short
residual call (valued closed-form), so they capture roughly intrinsic-plus-a-little, not zero — this is the **soft-call** reality (within the ~30-day/≈24-trading-day notice the holder exits or exercises and keeps intrinsic; only doing nothing yields $0.01), so the engine is **not** a hard $6.50-style ceiling. It solves
the **knockout-adjusted implied vol** that reproduces the market warrant price, and reports a **band** between
an aggressive-issuer case (redeem at first eligibility — highest implied vol) and a lenient case (issuer
delays / registration gap — lower implied vol). The midpoint is the central estimate.

It also reports the **vanilla no-knockout IV** (closed-form Black-Scholes + Merton carry) as the **upper bound
on cheapness** — useful to show how much of the apparent edge is really just the un-priced knockout.

You are **not locked to this model.** Use whatever values the specific warrant best:
- **$10 make-whole present** → set `make_whole_trigger` in the inputs; the engine adds the second,
  lower trigger. The make-whole is designed to hand holders ~Black-Scholes-fair value, so it is less
  punitive than the $18 knockout but can force conversion earlier.
- **Early-exercise / dilution / jumps** → a CRR tree, Longstaff-Schwartz LSMC, a PDE, or a jump-diffusion
  are all fair game; build it if it values *this* warrant more faithfully. Keep the **knockout-adjusted vol vs
  break-even / listed / realized** comparison front and center — that's the edge — and sanity-check
  against the vanilla bound and the 40%-rule.

## Getting the data

**Bloomberg Terminal (live tape — the only source for prices/vols).** Drive it in Citrix; pull warrant
DES, underlying HVT, OMON, spot. Full screen-reading guide in `references/bloomberg_pulls.md`. Remember:
prices and vols here are good; **terms are indicative — verify on EDGAR.** Drive the Terminal yourself;
there is **no quote-MCP fallback** — if Citrix is down, say so rather than sourcing tape elsewhere.

**SEC EDGAR in the user's LOCAL Claude-in-Chrome browser (authoritative terms — mandatory).** Engage that browser first (`list_connected_browsers` / `select_browser`; if none is connected, stop and ask the user to open Chrome with the Claude extension — never a sandboxed browser), then drive edgar.sec.gov in it
to read the warrant agreement and confirm strike, redemption mechanics, and the true 5-years-post-BC
maturity. Step-by-step in `references/edgar_terms.md`. Because a full warrant agreement overflows the
browser's read-page limit, **read it section-by-section in the local browser with targeted `find` jumps**; only as an explicit LAST RESORT pull it with the approved web-fetch (save into
the deal folder → grep the sections) — **never via an
EDGAR data MCP.** Keep the saved copy as the deal's record for any name in the book.

**Cost-to-borrow** comes from the user / stock-loan desk — the terminal's securities-finance field is
usually not entitled, and option-implied borrow is contaminated by put skew. If they quote a **rebate**,
the borrow fee ≈ benchmark short rate (read it off the Terminal — e.g. OMON's pricing rate or `USGG3M`)
**minus** the rebate.

## Interpreting the verdict (knockout-adjusted)

Compare the **knockout-adjusted** warrant vol to listed front-month IV and realized HVs:

- **CHEAP** — knockout-adjusted vol is several points below both listed and realized, with comfortable borrow
  cushion. Recommend the long-warrant / short-stock trade and present the brief.
- **FAIR** — knockout-adjusted vol sits inside the realized/listed range; thin or no edge. Say so; suggest
  small size or passing. **This is the common outcome for SPAC warrants once the $18 knockout and the true
  maturity are priced** — and catching it is the point.
- **RICH** — knockout-adjusted vol is above listed; no edge, pass.

Always state the break-even borrow and the cushion, and be explicit about how much of any apparent edge
is the un-priced redemption — the vanilla-vs-knockout-adjusted gap, which for a *soft call* is usually only a few vol points, so don't over-credit it; the bigger reason a headline "edge vs listed" is fake is normally the maturity/term-structure mismatch (a multi-year warrant compared against short-dated listed vol you can't sell out that far).

## The trade (when CHEAP)

Long the warrant, short `delta` shares per warrant (use the **knockout-model delta**, which is lower than the
naive BS delta) to stay direction-neutral. You own multi-year vol cheaply; you win if the stock realizes
more vol than the knockout-adjusted implied, harvested by re-hedging, and/or if the warrant re-rates toward
realized. **Risks the engine/brief surface:** the **$18 knockout** — once the stock holds ≥$18 for 20 of 30 trading
days you have a ~30-day (≈24-trading-day) notice to **exit or exercise**, and a position left unmanaged
past it is redeemed at **$0.01**; it is your hard exit rule, and what you give up at that point is the
warrant's remaining time value, not its intrinsic. Also: borrow drifting toward break-even, and that the
warrant is only "cheap" if the stock keeps moving.

## Explaining the analysis (teach mode)

The user will often ask you to explain the model, an input, the verdict, the trade, the break-even, the
knockout, or a concept. Treat this as first-class. Ground it in `references/natenberg.md` — connect the
**specific number on the screen** to the **general principle** (e.g., "over ~4 years a 15% borrow
compounds to roughly a 30% haircut to the forward, which is why borrow dominates a long-dated warrant";
or "the $18 redemption is a *soft call*, not a hard price ceiling: the holder keeps intrinsic by exercising or
selling inside the ~24-trading-day notice, so it only forgoes the warrant's *remaining time value* — for a
deep-OTM name often just a few vol points, which is why the redemption is rarely the main reason a warrant
isn't cheap; the maturity/term-structure gap to short-dated listed vol usually is"). Name the concept, give the intuition, separate what you measured
from what you assumed, and flag noisy inputs. Keep the framework in your reasoning and explanations but
**out of the client-facing brief** — the brief stays plain-English and citation-free; the theory lives
here.

## Notes

- **Ticker-agnostic by construction.** Nothing is hardcoded — strike, life, redemption, vols, borrow all
  come from the pull + filing.
- **Verify before you price.** Bloomberg terms are indicative; the warrant agreement is authoritative.
  The two most common Bloomberg errors are a too-short maturity (IPO-keyed instead of 5-years-post-BC)
  and a missing/!generic redemption level.
- **The $18 redemption is a *knockout* (soft call), not a hard price ceiling.** ≥$18 for 20 of 30 trading days starts
  a ~30-day (≈24-trading-day) notice; the holder exits or exercises to keep intrinsic, else $0.01. It forgoes
  the warrant's remaining time value (usually only a few vol points), and it is the position's hard exit
  trigger — it is **not** a $6.50 ceiling. Never describe or chart it as a hard price ceiling.
- Rate is the least important input — a sensible ~risk-free is fine. Borrow and the verified terms are
  what move the verdict.
- Verify the live warrant market and loan rate at execution before sending anything to the desk.
- `scripts/inputs.example.json` is a worked example you can copy and edit.
