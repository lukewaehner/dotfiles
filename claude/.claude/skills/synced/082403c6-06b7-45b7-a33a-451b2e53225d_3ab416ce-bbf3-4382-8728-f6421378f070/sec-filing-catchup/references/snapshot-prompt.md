# Who this digest is for — read this first

The reader is **Aidas, a trader**. Everything below is downstream of how he
thinks. Internalize his intent and you'll write good snapshots even for events
the rules don't name; pattern-match the examples without it and you'll miss.

1. **The post-event STATE of the security, not a description of the event.** When
   he asks "how many redeemed? float now? was Class B converted?" he's asking what
   the cap structure looks like *after*. A trader prices off shares outstanding,
   cash-per-share, trust left, dilution. The filing (vote, NRA, deposit) is only
   the trigger — carry the math through to the number it leaves behind.
2. **Signal vs. noise, verdict first.** He scans ~20 rows for the 2 that are
   actionable. Declare each cell's class up front — real event (terms, money,
   dates) vs. skippable (a promo 425). The triage word goes first.
3. **He hunts anomalies.** The off-pattern situation (S-4 effective yet amended
   with no vote date, a target swap, an out-of-cycle trust move) is where
   mispricing and risk live. Surface it loudly (`Unusual: …`).
4. **Report, don't editorialize.** Give the fact and the number; *he* decides what
   it means. No "this is significant," no implied trade. State it as fact.
5. **Accuracy is non-negotiable, and absence must be explicit.** Never assert what
   the filing doesn't say — a confident wrong fact ("no target yet" when there is
   one) is worse than an omission. And when a field he expects on this event type
   isn't in the filing, **say so** ("no redemption results stated") rather than
   leaving it silently blank: a blank is ambiguous — he can't tell whether you
   missed it or the filing omitted it, and those imply opposite trades.

Through-line: **decision-ready, trader-grade facts — the cap-structure numbers and
catalyst dates that move or time the position, classified actionable-vs-noise up
front, anomalies flagged, stated as fact.** When in doubt: "what would Aidas need
to answer a question about this position cold?" — put that in the cell.

---

# How to write the "What happened" cell

One line (two at most, ~12–28 words), pulled from the **actual EDGAR filing
text** — never from the form label alone. Rules:

- **Lead with the hard number / name / date**, not the verb. NRA share counts,
  redemptions + $ out of trust, trust $/sh, PIPE size, valuation, deposit terms,
  vote/record dates, over-allotment — the figure is the first thing in the cell.
- **Never restate the form category.** "director/officer change", "other event",
  "quarterly report", "entered an agreement" carry zero info beyond the Form
  column. Replace the category with the specifics inside it.
- **Banned as standalone filler** (only OK if immediately followed by specifics):
  *routine, various, certain matters, an agreement, other event, update, change.*
- **Preserve the filing's calibration** — "expected to close in Q4" stays
  "expected", not "will".
- **State absence explicitly.** If a field he expects for this event type isn't in
  the filing after you've read the right section, say so in the cell (`no redemption
  results stated`, `trust/sh not disclosed`, `vote date not set`) — an expected
  field left blank is ambiguous. If the text can't be retrieved at all, `filing
  text unavailable`. Never invent, never silently omit an expected field.

The test: if the same sentence could sit on another company's row, it's too
generic.
- Bad:  `Item 1.01 — entered a material definitive agreement.`
- Good: `NRA on 4,256,015 Class A sh; Sponsor assigns 425,602 founder sh post-close (of 500K pool). Target: BIG3 HoldCo.`
- Bad:  `Quarterly report filed.`
- Good: `10-Q — trust $10.42/sh (vs $10.38 Q/Q); ~$1.1M cash outside trust; going-concern flagged.`

---

# Lead fact by form type

- **8-K** — read the SEC-HEADER `ITEM INFORMATION:` lines for the Item number(s),
  then pull the body specifics:
  - **5.07 vote / extension** — the FULL stats: votes for/against, shares
    **redeemed** (count + $/sh), **$ left in trust**, resulting **shares
    outstanding/float**, **whether Class B converted** (state it), and the new
    deadline. A headline ("extended one year") without these numbers is incomplete.
    **Redemption results are a REQUIRED field** on any vote/extension: give the
    count (and $ out of trust), or — if the filing doesn't disclose them — state
    **"no redemption results stated."** Never omit silently.
  - **1.01 / 2.01** — deal signed/closed: target, equity value, structure; NRA
    share counts; PIPE size.
  - **1.02** — termination: which agreement/counterparty, effective date, trust
    consequence.
  - **3.02** — unregistered/PIPE sale: size + price.
  - **5.02** — director/officer change: WHO left / WHO appointed, by name + role.
  - **8.01** — the ACTUAL event (Nasdaq deficiency/cure, trust extension deposit $
    + new deadline, press-release content) — never "other event."
- **Extension proxies (DEF 14A/PRE 14A) and extension 8-Ks** — state the **sponsor
  contribution** to trust tied to the extension ($/sh or $/month, cap). Do **NOT**
  assert "no target yet" — many extending SPACs already have a signed target; only
  state target status if the filing confirms it.
- **Proxies (DEFM14A/DEF 14A/PRE 14A/DEFR14A)** — meeting date, what's being voted
  on, redemption deadline.
- **S-4 / F-4 / S-1 / F-1 (and /A)** — registration status + the headline term
  (valuation, PIPE) **and the shareholder vote (meeting) date + record date** when
  set (Aidas asks for these specifically); if not set, say "vote date not set."
- **IPO offering / effectiveness (424B*, EFFECT, 8-A12B, CERT)** — the **trust
  funded** ($ total and $/sh) and the **over-allotment** (size + whether
  exercised). Not just "IPO priced." e.g. `$200M in trust, $10.00/sh, +3M over-allotment`.
- **SC 13D / 13G (and /A)** — holder name, stake **%** + share count, passive
  (13G) vs activist (13D). A new >5% holder is signal:
  `NEW >5% holder: Feis Equities 5.08% (1.23M sh), passive`. (Form 3/4 insider
  ownership is usually dropped — see `INCLUDE_FORM_3_4`.)
- **425** — say **"Promo"** FIRST when it's a LinkedIn post / TV hit / press blast
  with no new terms, then the target. Lead with a real term only if the 425
  actually carries one (newly signed BCA, PIPE, valuation) — then still note it
  came via a promo filing.
- **10-Q / 10-K (and /A)** — trust **$/sh** (and Q/Q delta), cash outside trust,
  runway / going-concern flag.
- **Anything else** — one neutral line: the form + its single most material disclosure.

**Flag the unusual.** Atypical fact patterns open the cell with `Unusual:` and
state what's strange in one clause.

Numbers discipline: exact thresholds beat adjectives (`$0.025/sh monthly, capped
at $375K`, not "small monthly deposit"). Use the filing's figures verbatim; don't
back-compute beyond what's stated.

---

# Worked examples

- **Vote 8-K (GRAF):** `Extension vote passed (21.1M for); deadline →9/27/26 (board may extend monthly to 12/27/26). 14,590,367 Class A redeemed @ ~$10.86 (~$91.3M left in trust); 14,159,633 sh out after (14,159,632 A + 1 B, no B conversion). NRA locked 4,256,015 sh for 425,602 founder sh. Target: BIG3 HoldCo.`
- **Termination 13D/A (MBAV):** `Unusual: ReserveOne BCA terminated, S-4 withdrawn — deal dead; sponsor sold 4,279,279 founder sh at $3.33 ($14.25M).`
- **IPO (YICC):** `Final 424B4 — $200M: 20M units @ $10 (1/3 warrant @ $11.50) + 3M over-allotment; targets Latin America.`

---

# Operational notes (from live testing)

- **8-K fast path:** the SEC-HEADER `ITEM INFORMATION:` lines name the event
  without parsing the body — read them first. The body specifics (vote stats,
  counterparties, deposit $) sit deeper (~12k–20k chars in, past the
  cover/securities tables), so page to there for the numbers.
- **10-Q / 10-K trust figure:** `summary=true` often returns NO sections on SPAC
  inline-XBRL filings — fall back to a keyword scan for "Trust Account" / "per
  share" / "subject to possible redemption", and cross-check the `spac-details`
  trust figure; if they disagree by >1¢, prefer the filing and flag it.
- **EFFECT notices:** an EFFECT filing means a registration statement (S-4/F-4 or
  S-1/F-1) was declared effective by the SEC — often no standalone document to
  read; snapshot it from the event ("S-1 declared effective; IPO cleared to
  price" / "S-4 effective; merger vote/closing can proceed").

---

> **Row ORDER is not decided here.** The renderer (`scripts/render_catchup.py`,
> `FORM_LADDER`) hard-codes the display order: 8-K → proxies → S-4/F-4 & S-1/F-1 →
> offering/effectiveness → 13D/G → 425 → periodic (10-Q/K), in-deal first within
> each group. Pass rows in any order; do not sort them yourself.
