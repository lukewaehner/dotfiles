---
name: warrant-analysis-v3
description: "SEC warrant agreement analysis, full term extraction, and a cheap/fair/rich implied-vol screen for public SPAC and deSPAC warrants. Trigger when the user asks to analyze warrants, extract warrant terms, evaluate SPAC warrant structures, screen a warrant for underpriced optionality, or asks about a ticker (e.g., KDKRW, BTWNW). Trigger phrases: analyze the warrants for [ticker], warrant terms for [ticker], pull the warrant agreement, is this warrant cheap, IV screen on [ticker], screen the warrant vs comps. Also trigger for tickers ending in W/WS/WT (confirm it is a warrant, not common stock), uploaded warrant PDFs, or SEC exhibits (EX-4.1, EX-4.4). One workflow: exercise/redemption/adjustment terms, lock-up and PIPE overhang, plus a zero-borrow Black-Scholes IV screen against historical vol, an ex-redemption comp set, and listed options. For a borrow-sensitive, knockout-aware execution price when sizing a trade, hand off to warrant-vol-arb. Pre-close names get an assumed-price IV grid, not a spot read."
---

# Public SPAC Warrant Analysis — Terms + IV Screen

## Overview

This skill does two things for a **public SPAC or deSPAC warrant**: (1) extracts every material term
from the warrant agreement and related filings, the same full extraction as before, and (2) screens
whether the warrant's current price embeds cheap, fair, or rich optionality — using a zero-borrow
Black-Scholes IV solve, historical vol, an ex-redemption comp universe, listed options (if any), and the
company's own overhang picture (lock-ups, PIPE structure) as context for whether "cheap on IV" actually
means cheap.

**Why the overhang and PIPE sections matter for the IV read, not just as background:** a warrant can
solve to a low implied vol at today's stock price and still be a bad long if the float is about to be
flooded by an unlocked PIPE or founder block — the realized path the warrant needs to pay off on is
exactly what that selling pressure works against. Likewise, a convertible PIPE's floor conversion price
is a structurally meaningful reference for where the stock could trade under stress, so the IV solve is
run at that level too, not just at the current tape. Treat these as inputs to the vol judgment, not a
separate section someone can skip.

**For a SPAC that hasn't closed and is still inside an open redemption window**, the subject's own live
common price is trust-anchored and isn't a usable Black-Scholes input on its own. Step 4.5 switches into
a **Pre-Close Scenario Mode** instead of a single spot read: it holds the warrant's actual traded price
fixed and solves implied vol across a grid of assumed common prices — starting from the current
redemption floor (never below it), not a flat assumed $10.00 — so the reader gets a spread of "if the
stock ends up worth $X" readings instead of one distorted number.

**Workflow:**
1. **Step 0 — Web Reconnaissance:** Build the full event timeline via web search
2. **Step 1 — Targeted Filing Search:** Pull exactly the right filings from EDGAR
3. **Step 2 — Read Warrant Agreement:** Extract all terms from EX-4.1
4. **Step 3 — Cross-Reference Description of Securities:** Verify terms against proxy/prospectus
5. **Step 3.5 — Lock-Up & Overhang Map** *(near-close/recently-closed deSPACs)*
6. **Step 3.6 — PIPE Structure & Illustrative Floor**
7. **Step 4 — Check Adjustments & Crescent Term**
8. **Step 4.5 — IV Screen:** zero-borrow BS solve, ex-redemption comps, listed options, and a Pre-Close
   Scenario Mode (assumed-price grid) when the subject is still inside an open redemption window
9. **Step 5 — Compile Output:** Produce .docx term sheet + IV screen + verdict
10. **Step 6 — Quality Checks**

Private placement, working capital, founder, non-redemption, and PIPE warrants stay out of the detailed
extraction scope (public warrants are the subject), but the PIPE's own economics are now first-class
inputs to the IV screen via Step 3.6 — that is a different thing from extracting the PIPE warrant's
own terms, which this skill still does not do in depth.

---

## Step 0: Web Search Reconnaissance — Build the Full Event Timeline

**ALWAYS DO THIS FIRST.** Before opening any filing in full, use **web_search** to construct a dated
timeline of every key event. This timeline is the roadmap for the rest of the skill.

**What web search is for vs. what EDGAR is for.** Web search is most reliable for *entity resolution*
(ticker → CIK → original SPAC name, target, financings, corporate actions) and least reliable for *exact
dates*. Treat web-derived dates as approximate pointers only. Once you have the CIK (Step 1), EDGAR's
own chronological filing list is the **authoritative** source for every date — anchor the final timeline
to filing dates, not web dates.

### 0a. Entity Identification
1. `"[TICKER]" SPAC deSPAC merger`
2. `"[TICKER]" "blank check" OR "special purpose acquisition"`
3. `"[TICKER]" former SPAC ticker OR "formerly known as"`

Extract: SPAC or post-deSPAC? Original SPAC name/ticker if post-deSPAC. CIK for both entities if they differ.

### 0b. IPO Date and Terms
1. `"[SPAC TICKER]" OR "[SPAC NAME]" IPO date "priced" OR "closed"`
2. `"[SPAC TICKER]" IPO "$10.00" units`
3. `"[SPAC NAME]" "initial public offering" [YEAR range]`

Extract: IPO date, IPO size, unit structure, underwriter, overallotment.

### 0c. Deal Announcement
1. `"[SPAC TICKER]" "definitive agreement" OR "business combination agreement" announced`
2. `"[SPAC TICKER]" merger announcement target`

Extract: announcement date, target, initial valuation.

### 0d. Redemption / Vote Status *(new — feeds the ex-redemption test used later)*
1. `"[TICKER]" special meeting redemption results`
2. `"[TICKER]" extension vote redemption deadline`
3. `"[TICKER]" OR "[SPAC TICKER]" "business combination" "closed" OR "completed"`

Extract: has a redemption window already closed (extension vote or merger vote), even if the deal
itself hasn't closed? Closing date and redemption %, if closed. This status is used again in Step 4.5.

### 0e. Financings at deSPAC (Crescent Term Trigger Search)
1. `"[TICKER]" OR "[SPAC TICKER]" PIPE financing deSPAC`
2. `"[TICKER]" OR "[SPAC TICKER]" "forward purchase agreement" OR FPA`
3. `"[TICKER]" OR "[SPAC TICKER]" backstop OR "non-redemption agreement"`
4. `"[TICKER]" OR "[SPAC TICKER]" convertible note financing [YEAR]`
5. `"[TICKER]" OR "[SPAC TICKER]" "equity line" OR ELOC OR SEPA`
6. `"[TICKER]" warrant adjustment OR "adjusted exercise price"`

Extract per financing: date, type, size, price/share, counterparty. Note any press mention of "warrant
adjustment" (direct Crescent evidence).

**Red flags — Crescent Term almost certainly triggered:** redemptions >80% of trust; PIPE/FPA priced at
or below $10 with SPAC trading below $10; any "adjusted exercise price" language in press releases.

### 0f. Post-Closing Corporate Actions & Lock-Ups
1. `"[TICKER]" reverse stock split OR stock split`
2. `"[TICKER]" warrant redemption notice OR "called for redemption"`
3. `"[TICKER]" warrant amendment`
4. `"[TICKER]" warrant exchange offer OR warrant tender offer`
5. `"[TICKER]" "exchange agreement" warrants OR "offer to exchange" warrants`
6. `"[TICKER]" lock-up expiration OR "lock-up period" PIPE OR sponsor`

Extract: dates/details of splits, redemption calls, amendments, warrant exchange/tender offers, and any
lock-up expiration dates already public. A warrant exchange or tender offer can convert or extinguish
the public warrant entirely — if one has occurred or is pending, flag it prominently in the final output,
because the instrument the user is asking about may no longer exist on the original terms.

### 0g. Compile Timeline

```
EVENT TIMELINE & FILING ROADMAP — [TICKER]
=============================================
Current Ticker: [TICKER]     |  Current Entity: [NAME]
SPAC Ticker: [TICKER]        |  SPAC Name: [NAME]

[DATE] — SPAC IPO ($XXM, X units at $10, unit = 1 share + 1/X warrant)
         → TARGET FILING: 8-K w/ EX-4.1 (Warrant Agreement) + 424B4/S-1
[DATE] — Overallotment exercised (if applicable)         → TARGET FILING: 8-K
[DATE] — Deal announced with [TARGET]                    → TARGET FILING: 8-K (Item 1.01)
[DATE] — Proxy/S-4 filed                                  → TARGET FILING: DEFM14A or S-4/A
[DATE] — Redemption window closed (vote/extension)        → TARGET FILING: 8-K (Item 5.07)
[DATE] — deSPAC closed | Redemptions: XX%                 → TARGET FILING: 8-K (Items 2.01, 3.03, 5.01)
[DATE] — PIPE: $XXM at $XX.XX/share                       → TARGET FILING: 8-K
[DATE] — FPA/Backstop/Other: $XXM at $XX.XX/share         → TARGET FILING: 8-K
[DATE] — Warrant adjustment notice (if found)             → TARGET FILING: 8-K w/ EX-99.1
[DATE] — [Splits, redemption calls, amendments, lock-up expirations]

REDEMPTION STATUS: [Live — window open / Ex-redemption, not yet closed / Closed]
CRESCENT TERM PRELIMINARY ASSESSMENT: [as before]
```

**Show the timeline to the user, then decide whether to pause.** If everything resolved cleanly, show it
inline and proceed. Pause and ask "Does this look right?" only when there's genuine ambiguity worth a
human check: dual/uncertain CIK, conflicting dates, an unconfirmed target, or a likely-triggered Crescent
Term where a wrong assumption would flip the headline numbers.

---

## Step 1: Targeted Filing Search

Same as before — resolve the entity in EDGAR (both CIKs if post-deSPAC), then pull each filing by the
timeline date: Warrant Agreement (EX-4.1) near IPO date, IPO prospectus, proxy/registration, redemption
vote 8-K, deSPAC closing 8-K, financing 8-Ks, warrant adjustment notices, post-closing action 8-Ks.

---

## Step 2: Read the Warrant Agreement (EX-4.1)

Read in full using `edgar-filing-text`. Paginate with `offset`/`max_chars` (plan 3-8 reads for 50K-150K chars).

| Section | Extract |
|---------|---------|
| §1 | Warrant Agent |
| §2 | Detachability, fractional rules |
| §3 | **Strike price**, exercise period, cash/cashless mechanics, FMV formula, ownership blocker |
| §4 | **Anti-dilution**, **Crescent Term (§4.3.2)**, merger treatment, carveouts |
| §6 | **Redemption trigger**, redemption price, notice period, forced cashless, make-whole table |
| §7 | Registration obligation, cashless fallback |
| §8-9 | Amendment provisions, governing law |

**Critical extractions:**
- §3.3.1 — exercise mechanics for public warrants
- §4.3.2 — the exact gate threshold (deal-specific, don't assume $9.20) and the exact proceeds
  percentage in condition (y) (usually 60% but verify)
- §6 — full redemption mechanics; if dual redemption, both paths and the make-whole table

**Make-whole table — extract, never template.** Transcribe cell-by-cell from this specific filing and
cite the accession number. `references/common_structures.md` is illustrative structure only — never copy
its numbers into an output. If you can't fully read the table, say "make-whole table present — not
extracted; see [accession] §[x]" rather than reproducing approximate values.

---

## Step 3: Cross-Reference Description of Securities

Find in the proxy/prospectus (DEFM14A or S-4/A) using the proxy date from Step 0. Search
`search_terms`: "Public Warrants", "Description of Warrants". Verify strike, redemption trigger,
exercise period, warrant count, cashless formula against the agreement; flag discrepancies.

---

## Step 3.5: Lock-Up & Overhang Map

Run this step when Step 0 shows a deSPAC close within roughly the last or next 180 days — this is when
overhang timing actually matters to a warrant holder. For a long-seasoned post-close name or a pre-deal
SPAC with no close in sight, skip it and say so.

**Sources:** BCA, Sponsor Support Agreement, PIPE Subscription Agreements, and the S-4/proxy "Lock-Up"
section — all on EDGAR. Lock-up terms are commonly scattered across all three; don't stop at the proxy
summary.

**Build:**
```
Holder                | Shares (M) | % of post-close O/S | Lock-up length | Early-release trigger | Expiration
-----------------------|------------|----------------------|-----------------|------------------------|------------
Founder/Sponsor        |            |                      |                 |                        |
PIPE investors         |            |                      |                 |                        |
FPA/Backstop holders    |            |                      |                 |                        |
Other >5% holders      |            |                      |                 |                        |
```

**Flag explicitly, in plain language, at the top of this section (not buried in the table):**
- If the **PIPE has no lock-up** — common, and the single biggest silent overhang risk on a warrant long.
- If a founder early-release trigger price sits **below the warrant's breakeven** — that's the case
  where the overhang unlocks right as the warrant would otherwise start working.

---

## Step 3.6: PIPE Structure & Illustrative Floor

**Classify the PIPE:** common stock at a fixed price, vs. convertible (note or preferred) with a floor
or reset mechanic. Source: PIPE Subscription Agreement / certificate of designations, EDGAR EX-10.x.

**A "fixed" headline conversion price is not the whole story — this is the most common silent miss in
this step.** Convertible PIPEs frequently carry a separate anti-dilution/reset article (e.g., a
"Certificate of Designations §29.8" style provision) that only activates on a future test date — a
VWAP-reset a set number of months after closing, a periodic ratchet, or a dilutive-issuance reset. A
headline price that looks fixed today can still resolve to a hard floor later. **Always read the full
anti-dilution/reset article, not just the conversion-price clause**, and if a reset mechanic exists,
extract: the trigger/test date, the reference VWAP window, and the resulting floor price (e.g., "resets
to the greater of the trailing 20-day VWAP or $X.XX, tested on [date]"). Treat this exactly like any
other floor for Step 4.5 — it's a structural reference level, not a prediction, but skipping it because
the headline price looked fixed is a real error, not a minor omission.

**If convertible with a floor (headline or reset-triggered):** extract the floor conversion price. Frame
it correctly — **this is not a price prediction.** It's a structural reference level: the price at which
the PIPE investor's own conversion economics change, which makes it a useful stress-test level for the IV
solve in Step 4.5. Say this caveat explicitly wherever the floor number appears in the output, and note
the test date if the floor is reset-triggered rather than immediate.

**If no floor / straight common PIPE:** say so — but only after confirming there's no reset article
buried later in the document; there is no illustrative floor to carry into Step 4.5, and the IV screen
runs at spot only.

---

## Step 4: Check Adjustments & Crescent Term Triggers

### 4a. Post-Closing Amendments
Search 8-Ks after the closing date for Item 3.03, Item 5.03, "Warrant Adjustment Notice", "Amendment to
Warrant Agreement", and any warrant exchange/tender offer ("offer to exchange", Schedule TO,
exchange-agreement S-4). A closed or pending exchange/tender changes the headline answer — surface it at
the top of the output.

### 4b. Crescent Term Evidence
1. deSPAC closing 8-K: "Newly Issued Price", "Market Value", "4.3.2", "dilutive issuance", "adjusted exercise price"
2. 8-Ks within 30 days of closing: "warrant adjustment", "Exhibit 99"
3. Per financing from Step 0: pull the 8-K, extract price/share and proceeds, compare to gate threshold

### 4c. Crescent Term Calculation
```
Gate Threshold (§4.3.2): $____
Market Value (MV) = 20-day VWAP starting day prior to closing: $____
Newly Issued Price (NIP): $____
Conditions: (x) NIP < Gate? (y) Proceeds > [verified %] of equity proceeds? (z) MV < Gate?
All met? → [TRIGGERED / NOT TRIGGERED]
Adjusted Strike = 115% × max(MV, NIP)
Adjusted Redemption Trigger = 180% × max(MV, NIP)
```
Cross-check against any filed adjustment notice; use filing values if there's a discrepancy.

### 4d. Stock Splits / Reverse Splits
New strike = Old strike × (old shares / new shares). New shares/warrant = old × (new shares / old shares).

---

## Step 4.5: IV Screen

**Don't run this step ahead of Steps 2 and 3.6 for the subject ticker.** The IV solve needs the subject's
own strike (Crescent-adjusted if triggered) and PIPE floor as inputs — those come from actually reading
the warrant agreement and PIPE documents, not from memory or a prior run. If time pressure or a narrow
request tempts you to jump straight to comps, confirm the subject's own strike and floor are established
first (even a quick pass), or flag explicitly in the output that they weren't re-verified this run and
the subject-side numbers are carried from a prior pass rather than freshly confirmed.

**Read `references/iv_screen.md` in full before running this step** — it has the exact method for the
zero-borrow Black-Scholes solve, the ex-redemption comp filter, the comp table build, and the listed
options logic. Summary of what this step produces:

1. **Warrant IV Solve** — zero-borrow BS inversion at (a) the current spot price and (b) the PIPE floor
   from Step 3.6, if one exists. Two numbers: Spot IV and Floor-Scenario IV. Report both the price level
   and the solved IV side by side (spot price + spot IV, floor price + floor IV) — the floor is not a
   footnote appended after the numbers, it belongs in the same table as the spot read.
2. **Comp Universe** — historical vol and warrant IV for a set of comparable SPAC/deSPAC warrants,
   **restricted to names that have lost the redemption put** (post-close, or pre-close but confirmed
   ex-redemption — see the reference file for exactly how to confirm this). Never include a live,
   still-redeemable SPAC as a comp, and apply the same ex-redemption check to the **subject ticker**
   itself before presenting its IV as a clean read.
   **Search proactively for both kinds of eligible comp — don't stop at closed deSPACs.** If a full
   search of closed deSPACs in the sector comes up thin, that is not the end of the search: pre-close
   SPACs whose redemption window has already closed are equally valid comps (see
   `references/iv_screen.md` §2) and are often the only names available for a recently-voted deal in a
   niche sector. Only report "no comps found" after checking both categories. Also cross-check the
   target's own S-4/proxy "Competition" section for named peers — that's a stronger source than generic
   sector search terms and is the most common reason an obvious comp gets missed (see
   `references/iv_screen.md` §3 for the full protocol).
   **Also filter for scale similarity using pro forma equity value, not the SPAC's own market cap.** The
   SPAC shell's market cap just reflects trust NAV and says nothing about the target's actual scale — use
   the pro forma equity value implied by the deal itself (from the BCA/press release/investor deck) for
   both the subject and every comp, and note it in the table so the reader can judge fit.
3. **Listed Options IV** (if the underlying trades options) — full chain liquidity screen, IV term
   structure with the warrant's own Spot IV as the anchor row, and a read on contango/backwardation.
4. **Pre-Close Scenario Mode** — triggers automatically when the subject ticker is confirmed still
   inside an open redemption window (Section 2's ex-redemption test, applied to the subject itself, not
   just to comps). Instead of a single trust-anchored, uninformative Spot IV, solve IV across a grid of
   assumed common prices anchored to a computed redemption floor — never a flat assumed $10.00 without
   verifying it against the actual current floor first. See `references/iv_screen.md` §5 for the exact
   method, the floor-sourcing priority (latest extension 8-K > `spac-details` > 10-Q trust balance), the
   default grid (floor, $10.00-if-valid, floor×1.5/2/3, comp median), and the non-negotiable rule that no
   assumed price — default or user-requested — may sit below that floor.
5. **Synthesis** — carried into Step 5's verdict, not decided in isolation here.

---

## Step 5: Compile Output (.docx)

Read the docx skill at `/mnt/skills/public/docx/SKILL.md` before creating the document.

**Keep it dense — and that applies double to the Bottom Line paragraph specifically.** This is a
desk-read document, not an exhaustive filing memo. The most common way this report bloats is cramming
every caveat (Crescent ambiguity, floor-IV context, lock-up timing, comp fit) into one giant Bottom Line
paragraph — a wall of text is exactly as unreadable as ten separate sections, just compressed into one
place. **Hard target: 4-5 short sentences, under ~120 words, for Bottom Line.** State only: what the
warrant is (strike/redemption/expiration in one clause), the verdict and headline number (spot IV vs.
comp read), and the ONE caveat that most qualifies it. Every other caveat — Crescent test status, floor
IV, lock-up overlap — already has its own table below; reference it in half a sentence ("see Crescent
Term below" / "floor IV sits inside the comp range, see IV Screen") rather than re-deriving the reasoning
in prose. If you catch yourself writing a second "however" clause or a third qualifying dependent clause
in Bottom Line, stop and move that point to its proper table instead.

Outside of Bottom Line, favor tables and short bullets over prose everywhere, and don't restate a number
in a paragraph if it's already in a table above. Target something a PM can read start-to-finish in under
two minutes; a report that takes five is too long regardless of how much diligence sits behind it.

**If Pre-Close Scenario Mode is active** (subject still inside an open redemption window), the verdict
can't be a single "screens Nx cheap at today's spot" line, because today's spot isn't a usable price.
State it as a range instead — e.g., "screens cheap across the tested re-rating range above $X" or "only
screens cheap once the stock is assumed above $X, fair-to-rich below it" — and point to the scenario
table rather than re-deriving each level's read in prose.

**Lead with the verdict, not the last section.** The whole point of the IV Screen is to answer "is this
cheap" — that answer belongs in the first line the reader sees, not buried after ten sections of term
extraction. There is no separate "Verdict" section at the end of this template; the verdict IS the
headline and the Bottom Line, stated once, up front.

### Output Template

```
PUBLIC WARRANT TERM SHEET + IV SCREEN — [COMPANY NAME] ([TICKER])
Verdict: [Screens Cheap / Fairly Priced / Screens Rich] — [Underpriced/Fair/Overpriced] Optionality ([High/Moderate/Low] Confidence)
================================================================

BOTTOM LINE
[4-5 short sentences, under ~120 words. What it is (strike/redemption/expiration, one clause) + the
 verdict number (spot IV vs. comp read) + the single biggest caveat, in half a sentence with a pointer to
 its table ("see Crescent Term below" / "see IV Screen — floor IV sits inside the comp range"). This
 paragraph replaces what would otherwise be a separate late "verdict" section — say it once, briefly,
 here, and let the tables below carry the supporting detail instead of repeating it in prose.]

⚠ CORPORATE-ACTION ALERT (only if applicable)
[Warrant exchange, tender offer, redemption call, reverse split, or amendment. Omit if none apply.]

KEY LEVELS & REDEMPTION STATUS
  Strike / Redemption trigger / Crescent gate: $X.XX / $X.XX / $X.XX
  Spot mid (underlying / warrant), timestamped: $X.XX / $X.XX
  Redemption status (subject ticker): [Live-redeemable / Ex-redemption / Closed] — [confirms IV screen is
    reliable, or if still live-redeemable, points to the Pre-Close Scenario grid in IV SCREEN below rather
    than just flagging the distortion]

EVENT TIMELINE (condensed to one line per event — dates + filing type only, save color for Bottom Line)
  [Step 0g]

WARRANT TERMS SUMMARY (collapse Exercise/Redemption/Adjustment/Change-of-Control into one compact table)
  Item | Detail
  Structure | unit ratio, warrant count, agent
  Exercise window | start, expiration (flag non-standard length), cash/cashless mechanics
  Redemption | trigger, price, window, make-whole Y/N (if Y, transcribed table cited separately)
  Crescent-equivalent | gate, conditions, adjusted strike/trigger if triggered
  Private warrant differences | "verified against [accession]" or "generic — not verified"

OVERHANG, PIPE & FLOOR (merge Step 3.5 + 3.6 into one section)
  Holder | Instrument | Lock-up length | Expiration
  [rows — state "N/A, not near a close" if Step 3.5 skipped]
  PIPE type, price, headline conversion/floor terms, and — critically — any reset/VWAP-reset provision
  found in the full anti-dilution article (trigger date + mechanic), with the "not a prediction" caveat.
  State "no floor found, including on a full reset-article read" if genuinely none exists.

CRESCENT TERM — [TRIGGERED / NOT TRIGGERED / PENDING] (one compact table, not a multi-line derivation)
  Test | Result

IV SCREEN
  Metric                     | Subject ([TICKER])   | [Comp 1] | [Comp 2] | [Comp N]
  Redemption status           | [status]              | ex-redemption | ex-redemption | ...
  Pro forma equity value (deal) | $XXXM               | $XXXM    | $XXXM    | ...
  Spot price (underlying/warrant) | $X.XX / $X.XX     | $X.XX / $X.XX | ... | ...
  Spot IV (zero-borrow BS)    | ~XX% (or "UNDEFINED — mkt price below zero-vol floor" if the warrant
    trades below the price a 0% BS solve would produce; state the floor $ level when this happens) | ~XX% | ~XX% | ...
  Floor price (PIPE reset/illustrative floor, if one exists) | $X.XX | n/a | n/a | n/a
  Floor IV (solved at that floor price)                       | ~XX% | n/a | n/a | n/a
  Historical vol (ex-redemption window only) | [see note below] | XX% ann. | XX% ann. | ...

  **Floor IV is its own row, directly under Spot IV, ALWAYS — never a sentence written below the
  table.** Even though only the subject usually has a known floor (comps get "n/a"), a mostly-empty
  row is still a row: the whole point is that a reader can look straight down the Spot IV row, then
  straight down the Floor IV row immediately below it, and see both against every comp's Spot IV in
  the same glance. Moving Floor IV into prose ("Floor-scenario IV: ~53%...") defeats that and has
  been flagged as a repeat issue — don't do it, even if it feels like a stretch to make a single-value
  row look natural next to comp columns that all say "n/a."

  Note on historical vol: compute and show ONLY the realized-vol window measured from the date each name
    went ex-redemption (or closed) forward — never include or display a pre-redemption "quiet period"
    figure, even as color, since it's mechanically suppressed by the put right, not just less relevant.
    If the subject's own post-put history is only a few days old, say so explicitly and mark it noise
    rather than presenting a clean-looking annualized number.

  **If the subject ticker is still inside an open redemption window:** its Spot IV / Floor IV cells above
    read "see Pre-Close Scenario below" instead of a number (comps are unaffected — they're ex-redemption
    by construction, so their Spot IV stands as normal). Immediately below the IV SCREEN table, add:

  PRE-CLOSE SCENARIO IV — [TICKER] (redemption window still open; live common ≈ trust value, not a usable spot proxy)
    Assumed common price | Basis                                                  | Implied IV (at live warrant price $X.XX, T=X.XXy)
    $X.XX                 | Floor / current trust value (as of [date], [source])   | ~XX%
    $10.00                | Flat IPO reference (or "SKIPPED — below floor of $X.XX")| ~XX% / —
    $X.XX                 | Comp median post-close ([tickers], if any survived the filter) | ~XX%
    $X.XX                 | Floor × 1.15, illustrative                            | ~XX%
    $X.XX                 | Floor × 1.5, illustrative                              | ~XX%
    $X.XX                 | Floor × 2, illustrative                               | ~XX%
    $X.XX                 | Floor × 3, illustrative                               | ~XX%
    Assumed BC closing date used for T: [date, source, labeled as an assumption] — note if wider/narrower
      than one row came back UNDEFINED (expected on OTM pre-close names, not a bug — see iv_screen.md §5).
    Floor source: [latest extension/redemption 8-K per-share price, or spac-details, or 10-Q trust
      balance ÷ shares subject to redemption — cite whichever was used and its as-of date].
    Caveat: hypothetical re-rating scenarios, not price predictions — see `references/iv_screen.md` §5.
  Comp set: state how many names were considered and how many survived the ex-redemption + pro forma
    equity value filter (flag thin if < 3), and name which category each came from (closed deSPAC vs.
    ex-redemption pre-close).
  Fair value at comp-range vol: [if useful, back out what the warrant would be worth at the low/high of
    the comp IV range, to make the "screens Nx cheap/rich" claim concrete — this prose is fine for the
    dollar-value translation, it's the Floor IV number itself that must live in the table above, not here]
  Listed options (if applicable): Expiry | DTE | ATM Strike | ATM Call IV | ATM Put IV | P/C Skew, with
    the warrant's own Spot IV as an anchor row. State "no listed options" if none.
  Caveat: "Zero-borrow BS IV is a screening estimate, not an execution price — ignores real borrow and
    the redemption knockout. For trade sizing, run warrant-vol-arb."

────────────────────────────────────────────────────────────
PASTE-READY SUMMARY
  ticker= | warrant_ticker= | strike= | strike_adjusted= | redemption_trigger= | redemption_price= |
  window= | expiration= | crescent_present=Y/N | crescent_triggered=Y/N | dual_redemption=Y/N |
  make_whole=Y/N | agent= | governing_law= | agreement_accession= | pipe_lockup=Y/N | pipe_floor= |
  spot_iv= | floor_iv= | comp_median_iv= | comp_count= | redemption_status= | redemption_window_open=Y/N |
  trust_floor= | scenario_ivs= | verdict=

GAPS / FOLLOW-UP (short bullets only)
  [Unknowns/ambiguities. Tag each: (sourced §) vs (estimated) vs (market) vs (stale — confirm current).]

FILING SOURCES (compact list: accession + one-line label, no separate long section elsewhere)
  [Each filing with accession number]
```

---

## Step 6: Quality Checks

1. Timeline anchored to EDGAR filing dates, not web dates?
2. Strike/redemption trigger consistent between agreement and Description of Securities?
3. Crescent Term: gate AND proceeds-% both verified from text, not assumed?
4. Make-whole table transcribed cell-by-cell with accession cite, or explicitly marked "not extracted"? Reference-file numbers not copied?
5. Corporate actions (exchange/tender/redemption call/split/amendment) surfaced at the top if present?
6. Private-warrant section labeled "verified" or "generic — not verified"? No "customarily" stated as a finding?
7. **Lock-up/overhang sourced from the actual agreements (BCA, Sponsor Support, Subscription Agreements), not assumed generic?**
8. **PIPE floor verified from the filing, not estimated?**
9. **Warrant IV solve converged to the observed price (not a one-shot approximation)?**
10. **Comp set every member confirmed ex-redemption (post-close or vote/window closed), none still inside an open redemption window? Subject ticker's own redemption status checked and stated?**
11. **Comp search actually checked BOTH closed deSPACs AND pre-close ex-redemption SPACs before concluding "no comps," cross-referenced the target's own named competitors from its S-4/proxy, and filtered on pro forma equity value (not the SPAC's own trust-based market cap)? Each comp's pro forma equity value shown?**
12. **Comp set has ≥3 names, or explicitly flagged as thin/directional-only?**
13. **Listed-options section run, or explicitly marked N/A with reason?**
14. **Historical vol shown for the subject and every comp measured ONLY from their respective ex-redemption/close dates forward — no pre-redemption "quiet period" figure presented anywhere, even as context? Short post-put windows flagged as noise rather than presented as a clean number?**
15. **PIPE section checked the full anti-dilution/reset article, not just the headline conversion price, before concluding "no floor"?**
16. **Verdict stated once, up front (title line + Bottom Line) — no separate, redundant verdict section buried near the end?**
17. **Output dense — tables/short bullets over prose, no restated numbers, readable in under two minutes?**
18. Market references (any live prices shown) sourced and timestamped, or the block omitted?
19. Provenance flags present for stale/IPO-era figures?
20. **Subject ticker's own strike (Crescent-adjusted if applicable) and PIPE floor actually confirmed this run before the IV solve ran — not carried in from memory or a prior pass without saying so?**
21. **Any tool failure (`spac-details` error, oversized option chain, etc.) disclosed in Gaps/Follow-Up along with what fallback was used, rather than silently worked around?**
22. **Bottom Line is 4-5 sentences / under ~120 words — not a wall of text carrying every caveat that already lives in a table below?**
23. **Floor IV appears as its own row in the IV Screen table (directly under Spot IV), not as a sentence written below the table — even when every comp cell in that row just reads "n/a"?**
24. **If the subject ticker is still inside an open redemption window, did the report run the Pre-Close Scenario grid (not just caveat the spot number), compute a real floor from a cited source (latest extension 8-K, `spac-details`, or 10-Q trust balance — not an assumed $10.00), and confirm every assumed price shown — including the $10.00 row itself — is at or above that floor?**
25. **In the Pre-Close Scenario grid, is the BC-closing-date assumption behind T disclosed explicitly (source + labeled as an assumption), and are any UNDEFINED rows presented as an expected finding (not left looking like a broken table)?**

---

## MCP Tool Usage

Load via `tool_search` before starting. Key tools:
- **edgar-filings / edgar-filing-index / edgar-filing-text / edgar-company-facts / edgar-ownership-search** — SEC EDGAR (filings, exhibits, full text, XBRL, Form 4s for lock-up-adjacent insider activity)
- **get-price / get-vwap / get-intraday-bars** — live and historical prices for the IV solve, historical vol, and comp pulls
- **get-option-chain / get-option-data** — listed options chain and IV, when the underlying has one
- **spac-details** — SPAC universe lookup, useful for building the comp candidate list

**Tips:**
- Use `ticker` not `cik` when resolving entities.
- Plan 15,000 chars per EDGAR read for large docs.
- If a tool fails, reload via `tool_search` (tunnel URLs rotate).
- Prefer raw text with offset over `summary=true` for filings.
- **`spac-details` can error out server-side** (seen failing on a missing dependency). Reload via
  `tool_search` once; if it still fails, don't let the comp search stall on it — fall back to
  `web_search` + EDGAR full-text search for candidate tickers, and say explicitly in Gaps/Follow-Up that
  the fallback was used.
- **`get-option-chain` can exceed its own output limit on a name with many strikes/expiries** and come
  back truncated. Narrow the request (nearest 2-3 expiries, or strikes within ~30-50% of spot) rather
  than abandoning the listed-options section; report a partial read explicitly if even that overflows.
- **For the Pre-Close Scenario Mode's floor, prefer the per-share redemption price stated in the latest
  extension/redemption 8-K over back-calculating from the balance sheet** — it's the actual, already-
  disclosed number a holder would receive, and the most authoritative of the three sources in
  `references/iv_screen.md` §5.

---

## Common Patterns

### Warrant Agreement Styles
- **Ares/Reinvent (Type A):** $11.50 strike, $18 single redemption, Crescent Term, no make-whole
- **EarlyBird/Cantor (Type B):** $11.50 strike, dual redemption ($18 + $10 w/ make-whole table)
- **Churchill/CF:** Similar to Type B, Black-Scholes for private warrants

See `references/common_structures.md` for make-whole tables and formula definitions, and
`references/iv_screen.md` for the full IV Screen methodology.

### Gotchas
1. SPAC may have changed CIK at deSPAC — Step 0 handles this; verify in EDGAR.
2. Warrant Agreement is from SPAC IPO — look near IPO date, not in the S-4.
3. Amendments may be under the new CIK — check both.
4. Crescent Term is retroactive — applies even if the 8-K is filed weeks after closing.
5. Make-whole table only applies to the $10 cashless path, not the $18 redemption.
6. High redemptions + any financing = Crescent almost always triggered.
7. Multiple financings compound — PIPE + FPA + backstop all count toward the 60% threshold.
8. Overallotment — check for an 8-K ~45 days post-IPO for additional warrants.
9. **PIPE floor is a structural reference, never state it as an expected price.**
10. **Zero-borrow IV is a screening upper bound on cheapness, not a trade-ready price — real borrow narrows the edge. Point to `warrant-vol-arb` if the desk is actually sizing.**
11. **Live SPAC common trades with an embedded put (trust redemption right) until its redemption window closes — realized vol and any warrant IV solved off it will look deceptively low. Never use a still-redeemable name as a comp, and caveat the subject ticker's own IV screen if it's still inside an open redemption window. A pre-close SPAC whose window has already closed is fine to use — the closed-deal flag is not the right test, the put right is.**
12. Lock-up terms are often scattered across the BCA, Sponsor Support Agreement, and separate Subscription Agreements — check all three, don't stop at the S-4 summary.
13. **A thin comp set is usually a search-effort problem, not a data-availability one.** If the first pass at closed deSPACs in-sector turns up nothing, that's the point to broaden — pull in pre-close ex-redemption names and check adjacent sectors — before writing "no comps found." A near-miss sector (e.g. energy/nuclear for a fusion name) is a legitimate comp source even if not an exact match.
14. **Don't mix comps of very different scale, and don't use the SPAC's own market cap to judge scale.** A pre-close SPAC's market cap just reflects trust NAV — a $230M-trust shell can be merging with a $250M target or a $3B one, and trust size tells you nothing about which. Use the deal's own pro forma equity value (from the BCA/press release/deck) for both the subject and every comp, and show it so the reader can judge fit themselves.
15. **A "fixed" PIPE conversion price can still hide a floor.** Read the full anti-dilution/reset article of the convertible instrument, not just the clause stating the initial conversion price — VWAP-reset and periodic-reset provisions are common and often the single most important number in the whole report if the stock is trading anywhere near the reset test level.
16. **Historical vol computed across a redemption-put boundary is invalid, not just noisy.** Never blend or present a pre-redemption vol figure alongside a post-put one — the two are not measuring the same thing. If the post-put sample is too short to be meaningful, say so plainly instead of quietly presenting a number that looks precise but isn't.
17. **The verdict goes at the top, once.** Don't write a full synthesis paragraph twice (once disguised as "Bottom Line," again as a separate "Verdict" section later) — that's exactly the kind of redundancy that makes these reports too long to be useful at a desk.
18. **A missed obvious comp is usually a search-breadth problem, not a "there are no more" problem.** The target's own S-4/proxy "Competition" section names its real peers directly — cross-check every comp candidate list against it before finalizing, since generic sector search terms alone reliably miss names that the target's own filing would have surfaced immediately.
19. **A still-live SPAC's own IV screen needs the Pre-Close Scenario grid, not just a caveat.** The subject's live common price is trust-anchored the same way a comp's would be (Gotcha #11) — but for the subject ticker itself, the fix isn't to exclude it, it's to hold the warrant's real traded price fixed and solve IV across a grid of assumed common prices anchored to the actual current redemption floor. Never default to a flat $10.00 without checking it against that floor first — trust value accretes above $10.00 over time, and on a seasoned SPAC $10.00 itself can already be a sub-floor, invalid scenario.
20. **In the Pre-Close Scenario grid, most of the upper rows coming back UNDEFINED is normal, not a bug.** A live test (BBCQW, July 2026) confirmed this: the wider re-rating multiples (×1.5/×2/×3) landed UNDEFINED on a genuinely typical fresh, modestly-priced pre-close warrant, because the zero-vol floor rises with the assumed price while the actual warrant price stays fixed. Present that as a finding (little probability weight priced on that much re-rating), not a broken table — and keep the tighter ×1.15 level in the grid specifically because it's more likely to resolve to a real number when the wider ones don't. Also from that same test: the BC-closing-date assumption behind T needs to be sourced and disclosed explicitly (deal timeline guidance, not a guess), and the fixed warrant/common price should default to the last regular-session close rather than a thin after-hours print.
