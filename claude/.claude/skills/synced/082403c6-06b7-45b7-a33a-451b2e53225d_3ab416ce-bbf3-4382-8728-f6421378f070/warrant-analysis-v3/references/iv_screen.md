# IV Screen Methodology (Step 4.5 detail)

Read this file before running any part of the IV Screen. It covers five things: the zero-borrow
Black-Scholes inversion, the ex-redemption comp filter, the comp table build, the listed-options
logic ported from `warrant-arb-analysis`, and the Pre-Close Scenario Mode used when the subject ticker
itself is still inside an open redemption window.

---

## 1. Warrant IV Solve — Black-Scholes, Zero Borrow

The warrant is treated as a European call. Solve for the implied volatility σ that reproduces the
observed warrant price via standard Black-Scholes, with **zero cost-to-borrow and zero dividend yield**
(q = 0). This is a deliberate simplification relative to a full knockout-aware model (see the note at
the end of this section) — it is a screening number, not an execution-grade price.

**Inputs:**
- `W` — current warrant price (live)
- `S` — current common stock price (live)
- `K` — strike price (from the warrant agreement — use the Crescent-adjusted strike if triggered)
- `T` — time to expiry in years. For SPAC/deSPAC warrants this is almost always 5 years from the
  business-combination closing date, not the IPO date — confirm from Step 0/2.
- `r` — risk-free rate. Use the current ~3-month T-bill yield if obtainable from a price/rate tool;
  otherwise a reasonable current short-rate proxy is fine. Rate is a minor input relative to S, K, T.
- `q = 0` (no borrow, no dividend) — this is the "zero borrow" convention for this skill.

**Method:** bisection or Newton-Raphson on σ against the Black-Scholes call price
`C(S, K, T, r, q, σ) = W`, converging to within a cent of the observed warrant price. Don't rely on a
single-shot approximation formula — iterate to convergence, since the whole IV Screen downstream reads
on this number.

**Run it twice per warrant:**
1. **Spot IV** — S = current common price.
2. **Floor-Scenario IV** — S = the PIPE illustrative floor price from Step 3.6, if one exists (including
   a reset-triggered floor found in the full anti-dilution article, not just a headline fixed price).
   This answers: if the stock traded down to the level the PIPE's own conversion economics reference,
   does the warrant's current price still look cheap, or does the apparent cheapness depend entirely on
   the stock staying near current levels?

**Present spot and floor together, in the same table, as their own rows — never spot in the table and
the floor described afterward in prose.** Use dedicated rows: `Spot IV` then, immediately below it,
`Floor IV` (with `Floor price` above both, if you want the dollar level shown too). This has been flagged
twice now as a recurring failure mode: a run will correctly compute the floor IV number, then write it as
a sentence below the table ("Floor-scenario IV: ~53%...") instead of a row, because only the subject
column has a value and the comp columns would just say "n/a." Resist that — a row where every comp cell
reads "n/a" is still the right structure, because the whole point is letting the reader scan Spot IV then
Floor IV vertically, stacked directly against every comp's Spot IV in the same table. Moving it to prose
defeats the comparison it exists to enable.

**Edge case — warrant price below the zero-vol floor.** Occasionally the market price sits below what
even a 0% BS solve would produce (the "zero-vol floor," i.e., the present value of the strike/intrinsic
path at zero volatility). When this happens, Spot IV is not "very low" — it's mathematically undefined,
and that's a meaningful finding, not an error to paper over. Report it as `UNDEFINED — market price below
zero-vol floor (floor = $X.XX)` rather than forcing a number, and treat it as a flag worth investigating
(thin debut-day liquidity, wide spreads, unsettled borrow) rather than silently discarding the observation.

**Report both with the explicit caveat:** "Zero-borrow BS IV — a screening estimate, not a trade-ready
price. It ignores actual stock-loan cost and the SPAC/deSPAC redemption knockout. If actual borrow is
materially positive, or the desk is sizing a real position, price it properly with `warrant-vol-arb`
(knockout-aware Monte Carlo, real borrow) before trading off this number."

---

## 2. Ex-Redemption Filter — Which Names Belong in the Comp Set

**The rule is about the put right, not the deal-closed flag.** A live, pre-close SPAC's common stock
trades near trust NAV because holders can still redeem for cash — that embedded put floors the stock
and mechanically suppresses realized vol, and any warrant IV solved against that suppressed stock price
and vol will look deceptively low. A post-close deSPAC obviously has no such put. But a **pre-close SPAC
whose redemption window has already run its course — e.g., the extension or merger vote's redemption
deadline has passed and the redemption results are filed — has also lost the put**, even though the
business combination hasn't formally closed yet. Its common is genuinely trading on equity risk from
that point forward, so it belongs in the comp set.

**How to confirm a candidate is ex-redemption (whether or not it has since closed):**
- Search EDGAR for the 8-K reporting the shareholder vote / redemption results (typically Item 5.07,
  sometimes paired with Item 8.01) — this discloses the redemption deadline and the shares/amount
  redeemed. Once that date has passed, the redemption right on the remaining, non-redeemed shares is
  gone until (if ever) a new extension vote is called.
- If a later extension vote has been announced or is pending, treat the name as **live again** (a new
  redemption window reopens the put) until that window also closes.
- If genuinely unclear from EDGAR alone, a quick web search for "[TICKER] redemption deadline" or
  "[TICKER] special meeting results" usually resolves it fast.

**Exclude:** any SPAC currently inside an open redemption window (upcoming extension vote, upcoming
merger vote not yet held, or a redemption offer currently outstanding).

**Include:** post-close deSPACs, and pre-close SPACs confirmed ex-redemption per the above.

This same test applies to the **subject ticker** being analyzed, not just the comps. If the subject
warrant's underlying is itself still inside an open redemption window, say so plainly in the report —
the Spot IV / Floor IV numbers for that name carry the same distortion and shouldn't be presented as a
clean read.

---

## 3. Comp Table Build

1. **Assemble candidates in two passes, in this order — don't stop after the first if it comes up
   thin:**
   - **Pass 1 — closed deSPACs** in the same sector/vintage. Pull tickers from `spac-details` if
     available, or ask the user for a starting list.
   - **Pass 2 — pre-close SPACs confirmed ex-redemption** (Section 2) in the same sector. These are
     equally valid comps and are frequently the *only* names available for a recently-voted deal in a
     niche sector (e.g. energy/nuclear/fusion), where a handful of names is the whole universe. Always
     run this pass before concluding "no comps" — a thin Pass 1 result is a reason to run Pass 2, not a
     reason to stop.
   - If both passes are thin within the exact sector, widen to an adjacent sector before giving up
     entirely, and say explicitly that the comps are cross-sector. For a narrow-tech name (e.g. fusion),
     the right adjacent set is usually other high-binary-catalyst, pre-revenue, capital-intensive
     hard-tech deSPACs — quantum computing, advanced nuclear, space, deep-tech/climate-tech — not just
     the literal same subsector. Name the broadened category explicitly rather than silently drifting
     into unrelated names.
   - **If `spac-details` errors out or is otherwise unavailable, don't stall the search on it.** Reload
     via `tool_search` once; if it still fails, fall back to `web_search` (e.g. "[sector] SPAC warrant
     list 2025 2026", "[sector] deSPAC closed business combination") and EDGAR full-text search for
     candidate tickers instead. Note the tool failure explicitly in Gaps/Follow-Up rather than quietly
     working around it — a fallback that isn't disclosed looks like a clean data pull when it wasn't one.
   - **Show your exclusions, not just your inclusions.** For every candidate seriously considered and
     rejected (still pre-vote, wrong instrument, delisted, etc.), name it and say why — this is what
     makes a thin comp set defensible instead of merely asserted, and it's the difference between "I
     looked and there are genuinely only 2" and "I stopped after 2."
   - **A generic sector search misses names — use the target's own filings as a peer list, not just
     web search phrasing.** The single best source for "who are the real comps" is the target company's
     own S-4/proxy business description or "Competition" section — it names its actual technology/market
     peers directly, and a de-SPAC'd peer named there is a far stronger comp than one found by guessing
     search terms. Pull that section before finalizing Pass 1, cross-reference every named peer against
     EDGAR/web for deSPAC status, and don't treat a sector search as complete until this cross-check is
     done. Run at least 2-3 differently-worded searches as well (e.g. don't stop at "[sector] SPAC
     warrant" — also try "[sector] deSPAC closed 2025 2026", named-competitor searches, and searches on
     the sponsor's other deals) before concluding a pass is exhausted.
   - **A comp set that's thinner than a prior run on the same ticker is a signal to look harder, not
     a different answer.** If this ticker has been analyzed before and a name was found as a comp
     previously, don't silently drop it this run without a specific reason (e.g., it's no longer
     ex-redemption, or its warrant delisted) — an inconsistent comp set between runs usually means the
     search wasn't exhaustive, not that the universe changed.
2. Filter every candidate through Section 2 above. Drop anything still inside an open redemption window
   — don't include with a caveat, exclude outright, since the distortion isn't a minor footnote.
3. **Filter for scale similarity using pro forma equity value, not the SPAC's own market cap.** A
   pre-close SPAC's market cap just reflects trust NAV (~$200-300M for a typical deal) regardless of
   whether the target is a $250M or $3B business — it tells you nothing about the actual company's scale
   or vol profile. Use the **pro forma equity value of the combined company at the deal's own reference
   price**, as disclosed in the BCA/press release/investor deck (commonly stated directly as "implied pro
   forma equity value of approximately $X," or backed out from pro forma shares outstanding × the deal's
   $10.00-equivalent reference price). This is the number that actually describes what's being compared,
   both for the subject and for every comp — including comps that are themselves still pre-close (use
   their deal-implied pro forma value too, not their shell's trust-based market cap). For comps that have
   already closed and are trading, the live market cap is a fine cross-check once available since it now
   reflects the real business, but the pro forma-at-deal figure is still the more consistent anchor across
   a mixed pre-close/post-close comp set. Pull this for each candidate and show it in the table — don't
   just assert fit, let the reader see it.
4. Per surviving comp, pull: underlying price, warrant price, strike, time-to-expiry, and pro forma
   equity value (plus current market cap if already trading post-close).
   **Compute realized vol of the underlying ONLY over the window from that name's own ex-redemption (or
   close) date forward** — never a window that spans back across its own redemption-window-closed date,
   since the earlier period is mechanically put-suppressed and not a real vol reading, not merely a less
   relevant one. Use whatever lookbacks fit inside that window (30/90/180/252-day where available); if
   the ex-redemption history is only days old, say so and treat the comp's HV as not yet usable rather
   than reporting a precise-looking but meaningless annualized number. Solve warrant IV per Section 1
   (spot only for comps; floor-scenario is subject-ticker-specific and optional for comps if a PIPE floor
   is known).
5. Build the table, with spot and floor as columns, not a spot table plus a separate floor bullet:

```
Ticker | Redemption Type | Pro Forma Equity Value (deal) | Underlying HV (post-ex-redemption window only) | Strike | Moneyness | TTE | Spot Price | Spot IV | Floor Price | Floor IV | vs. HV
```

6. Note redemption structure (single $18 vs. dual $18/$10 make-whole) per comp — don't compare IVs
   across structurally different redemption types without flagging the difference, since the knockout
   shape affects the "true" richness of the quoted price even though this skill's solve doesn't model it
   directly.
7. If fewer than 3 names survive both filters, say so and treat the comp read as directional only — but
   only after confirming both Pass 1 and Pass 2 were actually run.

---

## 4. Listed Options IV (adapted from `warrant-arb-analysis`)

Only run this if the underlying has a listed options market (`get-option-chain` returns strikes/expiries).
Skip and state "no listed options" otherwise.

**a. Liquidity screen.** Pull the chain (calls and puts). A full unfiltered chain on a name with many
expiries/strikes can exceed the tool's output size and come back truncated or unparseable — if that
happens, don't give up on the section, narrow the request instead: pull the nearest 2-3 expiries first,
or filter to strikes within roughly 30-50% of spot, then widen only if you need more. Per expiry, compute
total OI, best-strike OI, ATM bid-ask spread. Classify LIQUID (OI ≥ 1,000, ATM spread ≤ 15% of mid), THIN
(OI 200–999 or spread 15–40%), or ILLIQUID (below that). If a narrowed pull still can't be parsed, report
what you did get plus "full chain exceeded tool output limits — partial read only" rather than dropping
the section silently.

**b. IV term structure.** For each LIQUID/THIN expiry, pull ATM call and put IV. Build:

```
Expiry | DTE | ATM Strike | ATM Call IV | ATM Put IV | P/C Skew
```

Add the warrant's own Spot IV (Section 1) as an anchor row labeled `WARRANT (zero-borrow BS)`.

**c. Read the shape.** Contango (IV rises with DTE) = normal, weak signal that front-end vol is rich vs.
the warrant. Flat = moderate. Backwardation (front-end IV > warrant IV) = the classic warrant-arb
environment — front-end vol looks rich relative to the long-dated warrant.

**d. Skew.** Compare ATM call vs. put IV at the nearest liquid expiry — positive skew (puts > calls)
reads as the market pricing downside/distribution risk; negative skew reads as call demand/squeeze risk.

This section feeds the final verdict (Step 5) but does not replace it — a rich front-end vs. cheap
warrant is supportive evidence, not the whole answer once overhang and PIPE-floor risk are layered in.

---

## 5. Pre-Close Scenario Mode — Assumed-Price IV Grid (Subject Still Inside an Open Redemption Window)

**When this replaces the ordinary Spot IV read.** Section 1's Spot IV needs a common-stock price that's
actually free to move on equity risk. A SPAC still inside an open redemption window doesn't have one —
the redemption put pins the common near trust value, so plugging that price into Black-Scholes as `S`
doesn't tell you anything about the warrant's optionality against the business the SPAC is actually
trying to buy. The warrant's own market price, by contrast, is **not** trust-anchored — warrants have no
claim on the trust and no redemption right, so the warrant price already reflects the market's live view
on deal probability and (whatever the market thinks) eventual post-close value. That asymmetry is the
whole basis for this mode: hold the warrant's actual traded price fixed, and instead of solving IV at one
uninformative spot level, solve it across a small grid of assumed common prices — so the reader sees "if
the stock ends up worth $X once the redemption right is gone, today's warrant price implies Y% vol at
that level," across a spread, not a single misleading point.

**Trigger.** Subject ticker's SPAC has not closed AND is confirmed still inside an open redemption window
per Section 2 (redemption status = Live-redeemable, not ex-redemption). Ex-redemption pre-close names and
closed deSPACs still get an ordinary Section 1 Spot IV — this mode is only for the subject, and only
while its own put right is live. It never applies to comps; Section 2 already excludes still-live names
from the comp set entirely, so there is nothing to reconcile there.

**Step 1 — Establish the floor.** The floor is the per-share amount a holder could get today by
redeeming — the hard lower bound for any assumed price, because a common share cannot rationally be
modeled below its own instant cash-out value while the right exists. Source, in priority order:
1. The per-share redemption price stated in the most recent extension/redemption 8-K (Item 5.07/8.01) —
   this is the actual number a shareholder would receive, and the most authoritative figure available.
2. `spac-details` (trust value / NAV-per-share field), if available and working.
3. Most recent 10-Q: trust account balance ÷ shares subject to possible redemption.

Cite whichever source you used and its as-of date. Trust value accretes upward from interest and can
jump at extension deposits, so an IPO-era "$10.00" is very often stale on a seasoned SPAC. **Treat $10.00
as a first guess to verify, never as a given** — the whole point of this step is knowing the real current
floor, not assuming the IPO price still applies.

**If `spac-details` returns more than one field that should reconcile to the same trust-per-share
figure** (e.g., a direct per-share field vs. trust balance ÷ shares outstanding computed from other
fields in the same response) **and they don't match, don't silently pick one.** Cross-check both against
the most recent 10-Q and flag the discrepancy explicitly in the output rather than presenting a single
number as clean when the source data itself disagreed.

**Step 2 — Build the assumed-price grid, checking every level against the floor before including it:**
- **Floor** — the computed value itself, labeled as such. (This is also, not coincidentally, close to
  where the live common already trades — that's the definition of trust-anchored. Including it makes the
  grid's baseline explicit rather than implied.)
- **$10.00 flat** — the standard illustrative starting point, but only if it is at or above the floor. On
  a seasoned SPAC the floor itself may already sit above $10.00 (accreted interest) — if so, **drop the
  $10.00 row and say explicitly why** ("$10.00 is below the current trust floor of $10.XX and is not a
  valid scenario") rather than quietly including a sub-floor number anyway.
- **Floor × 1.15, Floor × 1.5, Floor × 2, Floor × 3** — illustrative re-rating multiples, rounded to the
  nearest cent (standard equity-price convention). Scaling off the floor rather than fixed dollar levels
  keeps the grid sensible across trusts of very different sizes and very different implied target
  valuations. The tighter 1.15× level is there deliberately: the wider multiples routinely solve to
  UNDEFINED (see below) on a fresh, modestly-priced pre-close warrant, and keeping one closer-in level
  materially improves the odds that at least one upper-grid row resolves to an actual number rather than
  the grid being floor-and-comp-median only.
- **Comp median post-close price**, if any ex-redemption/closed comps are identifiable — ties the top of
  the grid to something empirically observed rather than purely arbitrary multiples, and name which comps
  it's drawn from. If the full Section 3 comp-table build is already being run as part of the same report,
  reuse those results here rather than duplicating the search. If it isn't (e.g., a standalone scenario
  run), a lighter same-sector pull — three or more names confirmed genuinely ex-redemption or closed,
  live-priced — is an acceptable stand-in for this one row; just label it explicitly as a light-touch pull
  rather than presenting it as the full comp-table protocol.
- **Any additional level the user asks for** — run it, but check it against the floor first exactly like
  the defaults; if a requested level is sub-floor, say so and don't compute a number for it.

**Step 3 — Solve.** For each assumed price `S` in the grid, hold the warrant's actual observed live price
`W` fixed and solve σ per Section 1's method (bisection/Newton-Raphson to convergence). Present every
level as its own table row — the same discipline as Spot IV/Floor IV elsewhere in this skill: never
collapse this into a prose paragraph once it's computed.

**Setting T when the deal hasn't closed.** Section 1's T assumes 5 years from a firm business-combination
closing date — a still-live subject, by definition, doesn't have one yet. Source an expected closing date
from the deal's own disclosed timeline (press release, F-4/S-4 timeline language, most recent Rule 425
communication — e.g., "expected to close in the second half of 2026"), take the midpoint if only a range
is given, and **disclose it explicitly as a labeled assumption, not a fact**. Run a quick sensitivity
check across the disclosed range (early/mid/late of the guided window) and report whether it moves the
read meaningfully — usually it shifts IV by no more than a point or two, but say so rather than presenting
a single T as if it were confirmed.

**Which price to hold fixed.** Use the warrant's last regular-session close/mid by default — thin
after-hours prints on these names often carry wide spreads that don't represent a real tradeable level.
If an intraday or after-hours print is used instead, disclose it and sanity-check it against the regular
close; a brief sensitivity comparison (regular close vs. the alternate print) is good practice when they
diverge by more than a trivial amount.

```
PRE-CLOSE SCENARIO IV — [TICKER] (redemption window still open; live common ≈ trust value, not a usable spot proxy)
  Assumed common price | Basis                                                  | Implied IV (at live warrant price $X.XX, T=X.XXy)
  $X.XX                 | Floor / current trust value (as of [date], [source])   | ~XX%
  $10.00                | Flat IPO reference (or "SKIPPED — below floor of $X.XX")| ~XX% / —
  $X.XX                 | Comp median post-close ([tickers])                    | ~XX%
  $X.XX                 | Floor × 1.15, illustrative                            | ~XX%
  $X.XX                 | Floor × 1.5, illustrative                              | ~XX%
  $X.XX                 | Floor × 2, illustrative                               | ~XX%
  $X.XX                 | Floor × 3, illustrative                               | ~XX%
  Assumed BC closing date used for T: [date] (source: [press release / F-4 timeline language], labeled
    as an assumption, not confirmed) — sensitivity across [range] moved IV by [X points].
```

**UNDEFINED rows are a common outcome in this grid, not a rare edge case — say so plainly.** Because the
warrant's actual traded price is held fixed while the assumed price rises, the zero-vol floor at each
assumed level rises with it; on a warrant that's meaningfully out-of-the-money with several years of
runway, it's entirely normal for the wider multiples (×1.5/×2/×3, sometimes even ×1.15) to come back
`UNDEFINED — market price below zero-vol floor ($X.XX)`. That is itself a finding, not a broken table —
it means today's warrant price embeds little probability weight on that much re-rating, holding
volatility as the only free parameter. State it that way explicitly (see the worked example logic in
Section 1) rather than leaving a row of blanks that reads as an error.

**Mandatory caveat, every time this table appears:** "These are hypothetical re-rating scenarios, not
price predictions — actual post-close price depends on deal terms, redemptions, and market reception,
none of which are settled until closing. This grid reads 'what does the warrant's current price imply
about vol if the stock ends up worth $X,' not 'where will the stock trade.'"

**Floor guardrail — non-negotiable.** Never present an assumed price below the computed floor, whether it
came from the defaults above or from a user request. If a candidate level would fall below it, drop it
(defaults) or decline and say why (user request) rather than solving a number for an economically
unreachable price. This includes the $10.00 default itself — it is not exempt just because it's the
conventional example level.
