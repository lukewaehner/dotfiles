---
name: personal-trading-compliance
description: >
  Quarterly personal-securities attestation check for Meteora Compliance. Cross-references each
  employee's pre-clearance approval emails against the broker report they submit at quarter-end,
  and flags any trade that is unapproved, traded while disapproved, or prohibited (SPACs and firm
  Restricted-List names). Records results in a per-employee Excel database plus a firm-wide master
  summary and, with guardrails, auto-emails employees their exceptions. Use whenever the user wants
  to run the personal-trading check, reconcile personal trades, process an employee's quarterly
  report, review pre-clearance versus a broker report, check the attestation, or find who traded
  without approval, or when a quarter-end attestation or brokerage statement arrives in the
  compliance mailbox. Also handles roster onboarding, employees' household/related accounts, and
  detecting people who file but are not rostered. Always use this skill for the personal-trading
  reconciliation rather than doing it ad hoc.
---

# Personal-Trading Compliance Reconciliation

Compares what each employee was **approved** to trade (pre-clearance emails) against what they
**actually** traded (their quarter-end broker report), and flags the gaps. Grounded in the Meteora
Compliance Manual, Code of Ethics, Personal Securities Transactions.

It scans the shared compliance mailbox — **`Compliance@meteoracapital.com` or
`COO@meteoracapital.com`** — signed in as whoever is running the check (confirm with `whoami`). In
this skill, **"reviewer" means that signed-in person** (CCO or COO). The pre-clearance threads and
the quarter-end reports both land in those mailboxes, so the skill searches the signed-in reviewer's
Outlook on their machine.

## Operating principle — escalate, never guess

This is a compliance control, so a wrong call is worse than a slow one. Whenever parsing,
classification, thread resolution, approval interpretation, restricted-hit identity, or roster
identity is ambiguous or low-confidence, **stop on that item, mark it `NEEDS_REVIEW`, and surface it
to the reviewer** — never invent an approval, guess a security's bucket, or auto-send anything
touching an unresolved item. The scripts already fail this way (unknown becomes `NEEDS_REVIEW`);
keep that discipline in the judgment steps you do by hand.

## Tools

- **Email** — the *Email Assistant (Microsoft 365)* extension, **signed in as whoever is running the
  check (the CCO or COO)**: `whoami`, `search_emails`, `read_thread`, `list_attachments`,
  `download_attachments`, `reply_all_email` / `reply_email` (for the notice). Load via ToolSearch
  (`Email Assistant`) if deferred.
- **Restricted / SPAC** — `rlst-check`, `rlst-read`, and `spac-details` (Meteora MCP). Optionally the
  `edgar` MCP to resolve a ticker to its SEC CIK when verifying a restricted hit.
- **Scripts** — in `scripts/` (Python 3, needs `openpyxl` + `pyyaml`). Run them from the skill
  folder; put per-run working files in a fresh work dir. Below, `$S` = this skill's directory and
  `$W` = a working dir for this run (e.g. `~/pt-compliance/jane-q2/`).

## The classification buckets (what gets flagged)

You can't enumerate every ticker, so **default = requires approval**, and everything else is carved
out. Full detail in `references/exempt-security-types.md` and `references/single-stock-etfs.md`.

- **PROHIBITED (violation on sight):** any SPAC (shares/warrants/rights/units/options) and any
  firm Restricted-List name — becomes `PROHIBITED_SPAC` / `PROHIBITED_RESTRICTED`. Determined live
  with `spac-details` + `rlst-check`, **then identity-verified** (a `rlst-check` hit only counts if
  it's the *same issuer* — see step 4; a loose ticker-substring match is escalated, not flagged).
  A single-stock ETF inherits its underlying's status.
- **PRE-CLEARANCE-EXEMPT:** broad ETFs/ETNs (index/sector/commodity, incl. leveraged/inverse
  *index* funds like TQQQ/SQQQ) — becomes `EXEMPT_PRECLEARANCE`. Listed, never flagged for a
  missing approval.
- **NON-REPORTABLE (ignore):** US-govt, money-market, open-end mutual funds, 529s, non-brokerage
  crypto, UITs; plus DRIP/automatic-plan trades and certified no-control managed accounts.
- **DEFAULT (needs a matching approval):** common stock, options, debt, IPOs/private placements,
  **and single-stock / single-name ETFs** (the test is the *underlying*, not the leverage).

## Workflow (per employee)

Run for one employee ("process Jane's Q2 report") or loop active roster entries for the sweep.
Below, EMPLOYEE = the person's name, QUARTER = e.g. "Q2 2026", BROKER = the custodian name,
BOOKS_DIR = a stable folder for the Excel database.

**0. Sign in.** `whoami()` to confirm which mailbox is active; if not signed in, run the email
extension's sign-in flow. Scan the shared compliance mailbox — **`Compliance@meteoracapital.com` or
`COO@meteoracapital.com`** (whichever the reviewer is signed into) — which receives the pre-clearance
threads and the quarter-end reports.

**1. Resolve the employee.** Read `references/roster.yaml`. Pull their filing addresses,
pre-clearance thread subject(s)/conversation_id, their own `brokers`, their `related_accounts`
(**in-scope** household / beneficial-ownership accounts they must report — spouse, household family,
per Manual §1), `exempt_accounts` (certified no-control last-4s, **out of scope**), and `notify`
flag. Skip `status: departed`. If the person isn't in the roster, do **not** process them — step 1b.

**1b. Roster reconciliation (unrostered filers).** On a sweep, `search_emails` for pre-clearance /
attestation-type mail in the quarter, collect the distinct senders into `filers.json`
(objects with name / address / subject / first_seen), then:
```
python3 $S/scripts/manage_roster.py detect-unrostered --filers $W/filers.json --out $W/unrostered.json
```
Surface any proposals to the reviewer for one-click onboarding (see Roster management). Never
auto-add; never process an unrostered person's trades.

**2. Build the approvals ledger.** `read_thread` on the employee's pre-clearance thread(s). Extract
each pre-clearance **request** and Compliance's **decision** into `$W/raw_approvals.json` — one
object per request with these fields:
```
employee, request_date, decision (Approved/Disapproved/Pending), decision_date,
clearance_valid_through, ticker, cusip, security_name, security_type,
side (Buy/Sell/Short/Cover), quantity, is_ipo_or_pp, source_message_id
```
Read the whole thread in context — a bare "approved" reply only means something next to the request
it answers. If you can't tell whether something was approved, or a field is missing, leave it and
let the normalizer flag it (it becomes `NEEDS_REVIEW`, never a guessed approval).

**An approval is good for the decision day ONLY — not before, not after.** The window is a single
calendar day: the day the CCO approved. It does **not** reach back to trades before that date and
does **not** carry forward to the next day, week, or the rest of the quarter. Example: an approval
granted **12 June** covers trades executed **on 12 June only** — a trade on 11 June or 13 June is
*not* covered by it. Set `decision_date` to that exact approval day. Leave `clearance_valid_through`
**empty/null** unless the CCO *explicitly wrote* a longer window (e.g. "pre-clearance sought through
June 20"); only then set `clearance_valid_through` to that stated end date. Never widen a window by
inference, and never assume an approval spans a range. Then:
```
python3 $S/scripts/build_ledger.py $W/raw_approvals.json $W/approvals.json
```

**3. Locate & parse the broker report(s).** Find the quarter-end attestation email (the report may be
the *Quarterly Transactions* form **or** monthly brokerage statements — the Manual allows statements
in lieu of the form). An employee's submission can include **several accounts**: their own plus each
declared `related_account` (household). `download_attachments`, then per file:
- CSV / XLSX:
```
python3 $S/scripts/parse_report.py $W/report.csv $W/transactions.json \
    --employee "EMPLOYEE" --broker "BROKER" [--account-last4 1234] \
    [--template $S/references/broker-templates/BROKER.json]
```
- PDF / scanned / a layout the parser can't read confidently — **extract it yourself** into the
  same `transactions.json` schema (below), setting `parse_ok` honestly per row and a realistic
  `parse_confidence`. Do not force a shaky parse — low confidence must be visible, not buried.

**Account-holder check (beneficial ownership).** As you parse each report, capture the account
**holder name** printed on it. It must be the EMPLOYEE or one of their declared `related_accounts`
holders. If the holder is someone **not** on this employee's roster entry, do not silently fold it
in — mark those transactions `NEEDS_REVIEW` (reason: "report for undeclared account holder NAME —
confirm beneficial ownership / add to roster") and tell the reviewer. Record the holder + last-4 on
each transaction (use `account_last4`) so the workbook shows whose account each trade came from.

Transaction schema (one object per fill):
```
employee, trade_date, settle_date, ticker, cusip, security_name,
side (BUY/SELL/SHORT/COVER), quantity, price, principal, broker, account_last4,
source_file, source_row, parse_ok (true/false), parse_confidence (0..1)
```
If a report won't parse or is missing, **stop and tell the reviewer** (fail closed).

**4. Restricted / SPAC + classification (with identity verification).** For every distinct ticker in
`transactions.json` (and, for a single-name ETF, its underlying), call `rlst-check` and
`spac-details`. **A `rlst-check` `restricted=true` is NOT trusted on its own** — it matches loosely
and can hit a *different* issuer whose ticker merely contains yours (e.g. querying `NU` / Nu Holdings
returns `INUV` / Inuvo Inc). Confirm identity with the helper:
```
python3 $S/scripts/verify_restricted.py QUERIED_TICKER "Security Name" PRIMARY_TICKER "Matched Company" \
    $S/references/ticker_cik.json
```
It compares exact ticker, then **CIK** (authoritative — seed/refresh `references/ticker_cik.json`
from SEC's company_tickers.json or the edgar MCP), then company name. Then:
- `genuine` → put the ticker in `$W/restricted_map.json` as `{"restricted": true, "reason": "..."}`
  (or `is_spac` for SPACs) so it becomes `PROHIBITED_*`.
- `false_positive` → do **not** restrict it; classify it normally (it's just a stock → `default`).
- `unverified` → add it to `$W/review_reasons.json` as `{TICKER: "rlst hit unconfirmed — ..."}` so
  it becomes `NEEDS_REVIEW` (never silently cleared, never auto-flagged).

Then classify each ticker into `$W/classification.json`:
`spac | restricted | broad_etf | single_stock_etf | non_reportable | default | unknown` (use the two
reference files; `unknown` → `NEEDS_REVIEW`).

**Ticker identity between the approval and the report (build the alias map).** A broker report often
renders the *same* security under a longer or decorated symbol than the pre-clearance email used —
crypto especially (an approval for **`BTC`** can appear on the statement as **`BTC XYZ ABC`**), and
mechanical equity decorations (**`BRK.B`** vs **`BRKB`**, **`AAPL`** vs **`AAPL US`**). The engine
joins on an exact ticker, so **record your identity judgement** in `$W/identity_map.json` and pass it
to `reconcile.py` (step 5). Follow `references/ticker-aliases.md`; the locked scope is **crypto +
mechanical**:
```
{"BTC XYZ ABC": {"canonical": "BTC",  "reason": "same coin, decorated symbol"},
 "BRK.B":       {"canonical": "BRKB", "reason": "same class-B share, punctuation"}}
```
Map every variant to one canonical (the engine resolves **both** the approval and report symbols
through it, only to join an approval to a trade — restricted/SPAC/classification stay on the reported
symbol). **Only** join a same-coin crypto variant or a mechanical equity decoration (same issuer AND
same share class). **Never** merge different assets, different share classes, a derivative with its
underlying, or a fund with the asset it holds (`GBTC` ≠ `BTC`); dual-listings/ADRs and renamed
tickers are out of scope — add those to `review_reasons.json` (→ `NEEDS_REVIEW`), don't map them. If
identity is genuinely ambiguous, you may use matching **quantity/price** as a corroborating
tiebreaker (the one place quantity/price decide anything); still unsure → `NEEDS_REVIEW`, never a
guess.

**5. Reconcile.**
```
python3 $S/scripts/reconcile.py $W/approvals.json $W/transactions.json $W/restricted_map.json \
    $W/classification.json $W/reconciliation.json --employee "EMPLOYEE" --quarter "QUARTER" \
    [--review-reasons $W/review_reasons.json] [--identity-map $W/identity_map.json] \
    [--exempt-last4 1234,5678] [--confidence-threshold 0.85]
```
The engine matches on **ticker + same side + trade date inside the day-only clearance window**.
**Quantity and price are informational only** — limit/market orders won't equal the request; they are
recorded but never flagged. It returns a status per transaction plus `auto_send_ok` (true only when
there are exceptions AND nothing is `NEEDS_REVIEW` AND confidence is fine). Don't re-implement the
matching by hand.

**The flag reason is deterministic and anchored to the trade's own side and date.** For every
unapproved trade the engine writes the reason as `No <SIDE> approval covered <TICKER> on <trade
date>` (e.g. `No SELL approval covered ABC on 2026-06-05.`); a same-day disapproval instead reads
`Traded while disapproved: …`. By design it will **never** name an approval whose day-only window
does not contain the trade date — so a buy approved a week *after* a sell can no longer surface as
"approved to buy, not sell." Treat the engine's `reason` as authoritative and reproduce it
**verbatim** in the notice and the workbook; do not paraphrase it into anything looser.

**6. Write the Excel database.**
```
python3 $S/scripts/write_excel.py $W/reconciliation.json --out-dir BOOKS_DIR \
    --master BOOKS_DIR/_Master_Compliance_Summary.xlsx --notice "STATUS_TEXT"
```
Produces `EMPLOYEE_PersonalTrading.xlsx` (Summary / Transactions / Approvals / Needs-Review /
History) and upserts the master row. Keep BOOKS_DIR stable across quarters so History accrues.

**7. Notify (auto-send, with guardrails).** See below. Then stamp the workbook/master notice status.

**8. Report to the reviewer.** Summarize: result (PASS / EXCEPTIONS / REVIEW), the exception lines,
any `NEEDS_REVIEW` items (incl. unverified restricted hits and undeclared account holders), and any
unrostered filers — with links/paths to the workbooks.

**When you state *why* an item is flagged, think it through against the day-only rule before you
write — and cite it correctly.** A single trade can fail on more than one count (wrong side, wrong
day, no request at all); do not stop at the first thing you notice. Anchor the reason to the trade's
**own side and trade date**, and reproduce the engine's `reason` rather than re-deriving a looser
one. Hard rule: **never name an approval unless its date equals the trade date.** If you are about to
write "approved to buy, not sell" (or similar), check the approval's date first — if it isn't the
trade's date, that approval is irrelevant and must not be cited; the correct statement is simply that
**no approval of that side existed for that date** (e.g. "no sell was approved for 5 June"). An
off-date approval may be mentioned to the reviewer only as context and only if explicitly labeled
"outside the day-only window."

## Auto-send guardrails

Compliance chose **auto-send** for the exception notice, but a false positive off a bad parse must
not email an employee. So:

- **Shadow mode (default for the first live quarter):** set `SHADOW_MODE=true` — do everything,
  including drafting the notice, but **draft only** (do not send). The reviewer confirms the engine
  is right, then sets `SHADOW_MODE=false`.
- **Confidence gate:** only send when `reconciliation.auto_send_ok` is true (exceptions exist, zero
  `NEEDS_REVIEW`, confidence at/above threshold) **and** the employee's roster `notify` is true.
- **Fail closed:** if the report didn't parse, the thread couldn't be resolved, or approvals look
  empty while trades exist — hold and alert the reviewer; never send.
- **Always CC the signed-in reviewer** (the CCO/COO running it) on the notice (oversight + record).
- **Compose** from `assets/notice_template.txt`: fill the quarter, employee, and first name, and one
  exception line per exception (trade date, side, quantity, ticker, security name, and the engine's
  `reason` **verbatim** — do not paraphrase it or add an off-date approval the engine deliberately
  left out). Reply into the employee's existing pre-clearance thread (`reply_email` /
  `reply_all_email`). Preview recipients, then send with `confirmed=True`.

Anything `NEEDS_REVIEW` is **excluded** from the notice and left for the reviewer.

## Roster management

The roster decides who is checked and who gets emailed, so it's compliance-owned but easy to edit:
```
python3 $S/scripts/manage_roster.py list
python3 $S/scripts/manage_roster.py add --name "Jane Doe" --emails "jane@meteoracapital.com,jd@gmail.com" \
        --thread "Jane Doe Personal Trade Pre-Clearance" --broker "Fidelity:1234"
python3 $S/scripts/manage_roster.py update --name "Jane Doe" --add-email "jane2@x.com" --notify true
python3 $S/scripts/manage_roster.py depart --name "Jane Doe"
```
When adding conversationally, gather the fields, confirm with the reviewer, then run `add`. **Also
capture each employee's household/related accounts** (spouse, household family) in the entry's
`related_accounts` — they carry beneficial ownership and must be reported and checked. Lock a thread
by putting its `conversation_id` in `roster.yaml` after confirming it once.

## Modes / triggers

- **Single employee:** "process Jane's Q2 report" — run the workflow for one person.
- **Quarterly sweep:** "run the personal-trading check for Q2" — loop active roster entries, plus
  step 1b unrostered detection. Best run ~30 days after quarter-end (the Manual's filing deadline).
- **Roster edits / onboarding:** "add someone to the roster", "add a spouse/household account",
  "who's filing but not on the roster".

## Notes

- Sides normalize to `BUY / SELL / SHORT / COVER`; an approval only covers the **same** side.
- Clearance is **day-only** unless explicitly extended — valid **only on the exact calendar day the
  CCO approved**, never the day before and never any day after. An approval dated 12 June covers
  trades on 12 June only; 11 June and 13 June are outside it. An unused approval expires that same day
  and cannot cover an earlier trade, a later day, or the rest of the quarter. The only way a window
  spans more than one day is an explicit CCO extension captured in `clearance_valid_through`.
- **Flag reasons are date + side anchored, and cite only in-window approvals.** Every unapproved
  trade reads `No <SIDE> approval covered <TICKER> on <trade date>` (or `Traded while disapproved …`
  for a same-day disapproval). An approval is named in a reason **only** when its day-only window
  contains the trade date; an out-of-window approval — even the same name and side a day or two off —
  is never cited as the cause. This is what prevents the mis-cited "approved to buy, not sell"
  pointing at an approval dated a week from the trade. Reproduce the engine `reason` verbatim.
- **Quantity & price are not matched** (one narrow exception below). Limit/market orders and partial
  fills mean the executed size/price won't equal the request. A valid approval (right ticker, side,
  and day) covers the trade regardless of amount; quantity/price are recorded for reference only.
- **Ticker identity → alias map (crypto + mechanical).** When a report symbol and an approval symbol
  name the same security but aren't byte-identical, record it in `identity_map.json` so the engine
  joins them (step 4 + `references/ticker-aliases.md`). Scope is locked to same-coin crypto variants
  (`BTC` ≈ `BTC XYZ ABC` ≈ `XBT` ≈ `BTCUSD`) and mechanical equity decorations (`BRK.B` ≈ `BRKB`,
  `AAPL` ≈ `AAPL US`) — same issuer and share class only. Different assets, different share classes,
  a derivative vs its underlying, a fund vs the asset it holds (`GBTC` ≠ `BTC`), dual-listings/ADRs
  and renames are never auto-joined → `NEEDS_REVIEW`. Quantity/price may corroborate an ambiguous
  identity but never widen the scope; otherwise they stay informational.
- **Restricted hits are identity-verified.** A `rlst-check` `restricted=true` only counts as a
  violation once `verify_restricted.py` confirms the same issuer (exact ticker → CIK → company
  name). Short tickers (2–3 letters) are the usual false positives; when unconfirmed, escalate.
- **Household/related accounts are in scope.** Employees must report close-relation accounts they
  beneficially own; the skill maps them via `related_accounts`. A report whose holder name isn't the
  employee or a declared relation → `NEEDS_REVIEW` (confirm beneficial ownership), never silently
  processed. `exempt_accounts` (certified no-control) are the opposite — skipped.
- `APPROVED_NOT_TRADED` (approved, never traded) is tracked on the Approvals tab, not a violation.
- New broker layouts: once you've hand-mapped one, save the column map as
  `references/broker-templates/BROKER.json` so it parses deterministically next time.
