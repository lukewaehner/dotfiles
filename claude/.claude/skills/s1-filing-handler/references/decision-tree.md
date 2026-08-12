# Decision tree, edge cases & scan-window logic

This is the detail behind Steps 1, 4, 5, 7, 8 and 9 of `SKILL.md`. Read it when you
need the exact rule for a case you're unsure about.

## Classifying the filing

The SPACInsider tag is always bracketed. Check `[S-1/A]` **before** `[S-1]` — `S-1` is a
substring of `S-1/A`, so testing `[S-1]` first would mislabel every amendment as an initial.
`scripts/parse_alert.py --parse` does this for you; the rule is:

- `[S-1/A]` present  -> `S-1/A` (amendment)
- else `[S-1]` present -> `S-1` (initial)
- neither -> not our alert (skip). Lookalikes like `[S-1MEF]` do **not** match `[S-1]`
  (there's no `]` right after `S-1`), which is intentional.

**SPAC name comes from the subject**, never the body. The body also names the *deSPAC
target* (e.g. "Factorial Energy, Inc.") — do not confuse the target with the SPAC.

## IPO vs deSPAC registration (the scope gate)

SPACInsider's `[S-1]` stream carries two very different things:

1. **A new SPAC IPO S-1** — blank-check company raising a trust. This is what
   `spac-s1-extraction` is built for. **In scope.**
2. **An "Initial DeSPAC Registration Statement"** — a post-deal registration tied to a
   business combination (carries a "DeSPAC Company Name:" target). Structurally nothing
   like an IPO S-1; running the IPO extraction on it yields "Not disclosed" everywhere.
   **Out of scope — skip** with a one-line note.

`parse_alert.py` sets `subtype: "despac"` when the body says "deSPAC" / "Initial DeSPAC
Registration Statement" or carries a "DeSPAC Company Name:" line, and `in_scope: false`.
The attached Cartesian Growth III / Factorial Energy example is a deSPAC registration and
must be skipped.

## Resolving the ticker

Order of preference:

1. Cover page of the S-1 on EDGAR (`edgar-filing-index` -> primary doc) — the offering
   usually lists Unit / Share / Warrant / Right symbols. `spac-s1-extraction`'s Section 1
   also enumerates these, so for a new IPO you get the ticker as a by-product of the body.
2. `spac-details(ticker)` to confirm the SPAC is in Meteora's universe and to disambiguate
   a reused ticker (match on CIK).

Use the **base common ticker** in the subject — strip a trailing `U` (unit), `W`/`WS`
(warrant), `R`/`RT` (right). Example: `CGCCU` -> `CGCC`.

**Canonical subject = `Internal <TICKER>`** (bare common ticker, no brackets, no name — matches
Luke's `spac-filing-digest`, so both skills share one chain per name). If no ticker has been
assigned yet (very common pre-IPO), open `Internal <SPAC Name>` as a placeholder and rename it
to `Internal <TICKER>` via `reply_all_rename_thread` once an amendment reveals the ticker
(createReplyAll keeps the conversation intact). Never invent a ticker.

## Detecting an existing internal thread (full ticker × folder matrix)

Mirror Luke's `spac-filing-digest` discovery so both skills converge on one chain per name.

**Build the identifier set:** common ticker + warrant + rights + the **unit** in BOTH forms
`<COMMON>U` and `<COMMON>/U` (the unit is the most-missed — names are often first tracked at IPO
under the unit), plus the bare **SPAC name** (for a chain opened pre-ticker as `Internal <Name>`).

**Search every identifier × every folder:** `search_emails(subject="Internal X", folder=F)` for
`F` in **SentItems, Inbox, Archive**. A teammate-opened thread lives in Inbox, not Sent. Never
substitute one broad `subject="Internal"` scan (capped, drops threads).

Matching rules:

- **Exact token match.** `Internal VII` ≠ `Internal VIIA`; the common must not swallow the
  unit/warrant/rights variant or vice-versa. Treat `RE:`/`Fw:` and trailing text as the same
  thread (`Internal IPFXU`, `RE: Internal IPFXU`, `Internal IPFXU: tail` are one thread).
- **Never collapse roman numerals / ordinals** — "…III" must not match "…II".
- **Clean threads only.** A usable chain has no no-reply/alert address (e.g.
  `tech@spacinsider.com`) as a participant. Gather all clean hits across every identifier and
  folder, then reply onto the **single most recent** message; `read_thread` it to confirm the
  recipients are clean before sending.
- Only open a **new** chain after the full matrix returns zero clean hits — name it with the
  **common** ticker (`Internal <TICKER>`), or `Internal <SPAC Name>` if no ticker yet.
- **Note on scanning the colleague's own inbox:** a chain nobody in this mailbox is on won't be
  found (duplicate risk). Searching Inbox + Archive (not just Sent) mitigates it; flag any
  new-chain creation as "no prior thread found." For full coverage, point the skill at the
  shared `Filings@` mailbox via delegated access.

## The 2×2 routing (with the two edges)

| # | Filing | Thread exists? | Action | Body |
|---|---|---|---|---|
| 1 | S-1 (IPO) | no | Open a **new** thread `Internal <TICKER>` (or `Internal <SPAC Name>` if no ticker yet) to `Filings@` | `spac-s1-extraction` output, verbatim |
| 2 | S-1/A | yes | **Reply-all** on the existing thread; **rename the subject to `Internal <TICKER>` if the ticker is now known** (via `reply_all_rename_thread`, keeps threading) | material-change summary (see `s1a-redline.md`) |
| 3 | S-1 (IPO) | yes (edge) | Dedup usually catches a re-file. If genuinely new, **reply-all** with the extraction — don't open a duplicate thread | extraction output |
| 4 | S-1/A | no | **Extract the S-1/A itself** — it *is* the current terms; ignore the superseded S-1. Run the full `spac-s1-extraction` on this S-1/A -> new `Internal <TICKER>` chain. **No redline** (no prior post to diff) | full `spac-s1-extraction` on the S-1/A |

Rationale for the edges:
- **#3** protects against duplicate alerts and manual re-runs creating a second thread.
- **#4** (Aidas, updated): a no-chain S-1/A is **not** a redline. The amendment *is* the current
  terms, so run the full `spac-s1-extraction` on the **S-1/A itself** and open the chain — we do not
  chase the superseded original S-1. A redline only makes sense once the chain already holds a
  prior extraction (case #2): a **new** S-1/A vs the previous S-1/S-1-A, impactful changes only.

**Batch ordering:** if an S-1 and its S-1/A both land in the same window (rare), process in
filing-time order so the S-1 opens the thread (case 1) and the S-1/A then replies to it
(case 2) rather than being treated as an orphan amendment (case 4).

## Scan window (Step 1) — full logic

Two nominal runs, both `America/New_York` (DST-aware), both weekdays:

- **09:00 run** scans **06:00–09:00** today.
- **17:30 run** scans **09:00–17:30** today.

Rules:
- Filings do not arrive after 17:30, so the afternoon window is capped at 17:30 and the
  morning window is capped at 09:00. The handler never scans past those caps, even on a late
  manual re-run — `parse_alert.py --window` enforces the caps.
- **Which window** is chosen by the clock: a run before noon ET -> morning window; a run at
  or after noon -> afternoon window. A manual re-run after 17:30 therefore correctly picks
  the afternoon window (09:00–17:30), not "09:00–now".
- **Failed run recovery:** the two windows are contiguous at 09:00, so nothing falls between
  them. If the *morning* run fails and is re-run in the afternoon, force it with
  `--session morning` so it still pulls 06:00–09:00 (otherwise the clock would pick
  afternoon). If the *afternoon* run fails, just re-run it — the clock picks afternoon.
- The connector's `search_emails` only takes a start bound (`after`); always filter results
  client-side to `receivedDateTime <= cutoff` so a late-window run doesn't sweep in the next
  window's mail.
