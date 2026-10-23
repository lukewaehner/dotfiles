---
name: sec-filing-catchup
description: 'Build and send the daily "SEC Filing Catch Up" digest for Meteora. Sweeps EDGAR DIRECTLY for every ticker in the Meteora SPAC universe (via the spac-details MCP + the edgar-filings MCP), pulls each filing from EDGAR, distills the single most important fact into a one-line "what happened" snapshot for a trader, and emails a crisp HTML table (subject "SEC Filing Catch Up") at end of day with a next-morning re-send. Source is EDGAR itself, NOT the BamSEC email feed — nothing is missed when a BamSEC alert fails to arrive. Trigger when the user asks to "run the SEC filing catch up", "build the filing digest", "what filed today in our universe", "catch up on today''s SEC filings", "send the filing catch up", or when this runs as its daily scheduled task. Always use this skill for the daily catch-up digest — do not assemble it ad hoc. This is a lightweight whole-universe DIGEST; for deep per-8-K analysis with threaded replies and memory-doc updates, use bamsec-filing-handler instead.'
---

# SEC Filing Catch Up

A once-daily digest. Sweep **EDGAR directly** for every ticker in the Meteora
SPAC universe, and for each filing that day give a trader the one fact that
matters — in a single scannable table.

Goal: a 10-second read at the close (repeated next morning) that lists every
universe SEC filing with its hard-number "what happened," sourced straight from
EDGAR so nothing slips through.

**Why EDGAR-direct (not BamSEC email):** the old design read `[BamSEC]` alert
emails. That had two failure modes — a BamSEC email that never arrived, and a
company name that didn't match cleanly. Sweeping EDGAR by the universe's own
tickers removes both: every filing is found at the source, and matching is exact
(ticker → CIK), not fuzzy. BamSEC is fully retired as a source.

This is deliberately **lightweight and breadth-first**. It does not write to
memory docs, thread replies, or do deep analysis — that's `bamsec-filing-handler`'s
job. Keep the two separate.

---

## CONFIG — edit these, nothing else, to retune the skill

```
EOD_SEND_LOCAL     = "18:30"   # end-of-day run, ET (set the EOD cron ~5 min before)
MORNING_SEND_LOCAL = "07:30"   # next-morning re-send, ET (second cron)
TIMEZONE           = "America/New_York"
RECIPIENTS         = []   # Aidas sets this on first run, e.g. ["APuskorius@meteoracapital.com"]
SUBJECT            = "SEC Filing Catch Up"
TEST_MODE          = false      # true -> "[TEST] " subject prefix (dev only; production = false)
INCLUDE_FORM_3_4   = false      # routine insider ownership (Form 3/4) — usually noise
ATTACH_HTML        = false      # never attach — an attachment reads as a download (Aidas)
DELIVERY           = "drive"    # "drive" = PDF link that opens in a tab | "inline" — see Step 5
DRIVE_FOLDER       = ""         # Google Drive folder (id or path) to publish the daily PDF into (when DELIVERY="drive")
```

To change send times, edit the two cron schedules in "Running as scheduled tasks"
below. To go live, set `TEST_MODE = false` and point `RECIPIENTS` at the real reader.

> **Send as the user — never walter.** Use whichever "send as me" email tool is
> connected for the run (e.g. the local Outlook connector `mcp__outlook__send_email`,
> or any other connected Outlook/Exchange/Gmail send tool). **Confirm which send
> tool to use on the first run.** It must send **as the connected user** — in
> production that is **Aidas**, and the digest goes to whoever Aidas lists in
> `RECIPIENTS`. Do NOT use the Meteora `send-email` MCP — that sends as walter@.
> Prefer a tool that supports an HTML body. For the morning bump, **prefer the send
> tool's native scheduled-send/draft**; only fall back to a second cron if it can't.

---

## Workflow

### Step 0 — Establish the target day

Work out which day to digest, in `TIMEZONE`. Two run modes:

- **EOD run** (evening cron): digest **today** up to `EOD_SEND_LOCAL`.
- **Morning run** (next-morning cron): re-digest **the prior business day** — a
  fresh EDGAR sweep of that date, so the email is identical, no stored state.

```bash
python3 - <<PYEOF
import datetime
from zoneinfo import ZoneInfo
TZ="America/New_York"; MODE="eod"   # or "morning"
now=datetime.datetime.now(ZoneInfo(TZ))
if MODE=="morning":
    back = 3 if now.weekday()==0 else 1   # Mon morning digests Friday
    day = now - datetime.timedelta(days=back)
else:
    day = now
print("target_date :", day.strftime("%Y-%m-%d"))
print("date_label  :", day.strftime("%A, %B %-d, %Y"))
print("gen_local   :", now.strftime("%Y-%m-%d %H:%M ET"))
PYEOF
```

Capture `target_date` (the EDGAR date filter) and `date_label` (table header).

### Step 1 — Get the universe

One call: `spac-details` with **no ticker** and
`fields=["spac_ticker","company_name","stage"]` returns every SPAC (~358) with
ticker, name, and stage. This is the sweep set. (Skip any junk rows like
`"#N/A Invalid Security"`.) Keep the `stage` per ticker — the renderer uses it
for the in-deal/pre-deal badge.

### Step 2 — Sweep EDGAR for the day (this is the core change)

For **every** universe ticker, ask EDGAR what it filed on `target_date`. Because
we query by ticker, every hit is by definition in-universe — there is **no
name-matching gate** anymore. Two sourcing paths, in preference order:

**Path A — per-ticker via the Meteora `edgar-filings` MCP (DEFAULT, always works).**
For each ticker:
`edgar-filings(ticker=TICKER, filing_date=target_date, limit=10)`.
It resolves ticker → CIK and returns each filing's `form_type`, `filing_date`,
`accession_number`, and document `url`. Collect them. A ticker with nothing that
day returns `total_filings_returned: 0` — skip silently. Tickers EDGAR can't
resolve (rare renames) → log and skip; they're caught on the next sweep.
- This is the **primary** path because the Meteora MCP is a **live** EDGAR
  channel. Run the calls in parallel batches (~30 at a time) to stay well under
  EDGAR's ~10 req/sec fair-access limit. ~358 calls total, cheap server-side.

**Use the bundled CIK cache first (shipped asset).**
- The skill ships `data/universe_cik_map.json` — a name-verified ticker→CIK map
  for the universe (321/358 resolved; the 36 it couldn't are listed in
  `_meta.unresolved_tickers`). Load it read-only at the start of Step 2 and query
  `edgar-filings(cik=CIK, filing_date=target_date, limit=10)` directly. Querying
  by CIK is exact and immune to the fuzzy-ticker-resolver collisions below; it does
  NOT cut the per-day call count (you still ask each CIK what it filed today), but
  it removes all resolution round-trips/retries and supplies the ready-made CIK set
  Path B needs.
- **Verify on use — the cache is a hint, not gospel.** EDGAR's ticker resolver is
  fuzzy (in testing several tickers silently resolved to the wrong entity — e.g.
  `MTAL`/`GPAC` collided on one CIK), so every cached CIK was name-verified at
  build time. Still confirm the returned filer name matches the expected
  `company_name` from spac-details; on a mismatch, discard the cached CIK, resolve
  live, and prefer the live result.
- **Tickers not in the map** (`_meta.unresolved_tickers` — foreign/OTC F-suffix
  names like ASCBF/SACQF/BLUAF, a few like HUDA, plus any brand-new ticker not yet
  in the file) are resolved live with `edgar-filings(ticker=…)`, name-verified, and
  used for that run. Surface the still-unresolved count in Step 6.
- **Refresh** the map when new SPACs join the universe (re-run the build). The file
  is just `{_meta, map:{TICKER:CIK10}}`; CIKs never change, so it only grows.
- **Dedupe by accession number.** The same filing can surface under two tickers if
  one mis-resolves to another's CIK (`VECA`→`PCSC` in testing). Collapse identical
  `accession_number` to one row, attributed to the filing's subject CIK.

**Path B — daily-index intersect (OPTIONAL fast path, ONLY if verified fresh).**
One fetch of `https://www.sec.gov/Archives/edgar/daily-index/{YYYY}/QTR{n}/form.{YYYYMMDD}.idx`
lists every filing market-wide that day (CIK + form + accession); intersect by the
universe's CIK set (use `data/universe_cik_map.json` — the bundled, name-verified
CIK set). One request instead of 358 — but only when the index is verified fresh.
- **MANDATORY freshness gate (handles the stale-mirror problem):** before trusting
  Path B, confirm the index is actually current. Fetch the directory
  `…/daily-index/{YYYY}/QTR{n}/index.json` and check that `form.{target_date}.idx`
  is listed. If it is **not present** (e.g. the mirror you can reach is frozen to
  an earlier date — this happens in sandboxed/dev environments), **do not** treat
  the day as empty — **fall back to Path A**. Never emit an empty digest just
  because the index file is missing or stale; Path A is the source of truth.

After the sweep, you have a flat list of filings:
`{ticker, company_name, stage, form_type, accession_number, url}`.

**Form scope:** keep all real disclosure forms (8-K, 425, S-4/F-4 ±/A, DEFM14A/
DEF 14A, 424B*, 10-Q, 10-K ±/A, 20-F, 6-K, SC 13D, SC 13G, EFFECT, 15-12B/G,
etc.). SC 13D/G are signal (a new >5% holder — keep them). Form 3/4 insider
ownership is usually noise — include only if `INCLUDE_FORM_3_4 = true`. If one
ticker filed several forms, list each as its own row (or fold trivially-related
ones, e.g. an 8-K + its 425, into one row).

If the whole sweep finds nothing: still send the digest with an empty table
("No SEC filings hit the Meteora SPAC universe today") — absence is a valid,
reassuring signal.

### Step 3 — Pull each filing and write the "what happened" snapshot

The reader is **Aidas, a trader**: he wants the post-event *state of the security*
(cap-structure numbers), the actionable-vs-noise verdict first, anomalies flagged,
and facts not opinions. `references/snapshot-prompt.md` opens with his full
thought process — read it before writing any cell.

For each filing, get the **actual filing text** — never snapshot from the form
type alone.

1. `edgar-filing-text(accession_number=..., ticker=TICKER)`.
   - **8-Ks:** read the SEC-HEADER `ITEM INFORMATION:` lines first — they name the
     event (1.01 deal, 3.02 PIPE, 5.02 director, 5.07 vote, 1.02 termination)
     without parsing the body. For vote/extension 8-Ks, read the Item 5.07 body for
     the **redemption count, $ left in trust, resulting float, and Class-B
     conversion** — Aidas asks for those.
   - **10-Q/10-K:** `summary=true` often returns no sections on SPAC inline-XBRL —
     fall back to a keyword scan for "Trust Account"/"per share" and cross-check
     the `spac-details` trust figure.
   - **SC 13D/G:** pull the holder name, share count, and % from the cover.
2. Distill **one line** (max two) per the snapshot rules: lead with the hard
   number, never restate the form category, flag the unusual. If filing text can't
   be retrieved, include the row with `"filing text unavailable"` rather than
   guessing. Each ticker is independent — never let one filing's facts leak into
   another's snapshot.

### Step 4 — Render the table

```bash
# rows.json keys: date_label, generated_local, source, in_universe (or omit→row count), rows:[...]
echo '{"subject_prefix": ""}' > /tmp/cfg.json   # production: no prefix ([TEST] only if TEST_MODE)
python3 scripts/render_catchup.py /tmp/rows.json /tmp/sec_catchup_<target_date>.html /tmp/cfg.json > /tmp/body.html
```

`rows[]` items: `ticker, company, stage, form, filed, snapshot, url`. Set
`source` to `"EDGAR (direct)"`. Use a **clean** `date_label`
("Weekday, Month D, YYYY") and `generated_local` — no "deep run", no "swept via
EDGAR", no "(test)" descriptors anywhere. The script applies the **hard-coded display order** (`FORM_LADDER` in `render_catchup.py`): 8-K → proxies → S-4/F-4 & S-1/F-1 → offering/effectiveness → 13D/G → 425 → periodic (10-Q/K), in-deal first within each group, and renders the "What happened" column. **Do not reorder rows yourself** — pass them in any order and let the script sort. `/tmp/body.html` is the
email body; the written `.html` is the openable copy — `present_files` it on
manual runs and the first scheduled run.

### Step 5 — Send the digest (as the connected account)

```
<connected send-as-me email tool>(   # e.g. mcp__outlook__send_email; confirm on first run
  to = RECIPIENTS,
  subject = (TEST_MODE ? "[TEST] " : "") + "SEC Filing Catch Up — <date_label>"
            + (MODE=="morning" ? " (morning recap)" : " (EOD)"),
  body = <contents of /tmp/body.html>,   # the full table, INLINE — send VERBATIM, no
                                          # headline/summary/preamble box above it
  body_is_html = true
  # attachments: OMIT by default. The table is already inline; an attached .html
  # reads as a download and is friction (Aidas). Only attach if ATTACH_HTML = true.
)
```

**Delivery — inline body always; never an attachment.** The HTML body carries the
whole table, so the reader never opens or downloads a file. Do **not** attach the
`.html` (Aidas: an attachment is a download = friction).

**`DELIVERY = "drive"` — opens in a browser tab, no download (Aidas's ask).**
He wants to click a link in the email and have the digest open as a page in a new
browser tab. Google Drive does this — **but only for a PDF**, because Drive renders
PDFs inline in its viewer, whereas a raw `.html` on Drive shows "no preview /
download". So:
1. **Render the digest to PDF.** Take the rendered HTML (`/tmp/body.html`) and
   convert it to PDF (the `pdf` skill, or an HTML→PDF converter). Keep the EDGAR
   ticker links — Drive's PDF viewer keeps them clickable.
2. **Upload to Google Drive** with the connected Drive MCP: `create_file` into
   `DRIVE_FOLDER` (file lands in the connected user's own Drive, so the link opens
   for him with no extra sharing). Then `get_file_metadata` to read the file's
   `webViewLink`.
3. **Email it** as before — full table INLINE in the body — with a one-line
   **`Open as page →`** link (`<a target="_blank" href="{webViewLink}">`) at the
   top. Clicking it opens the PDF in a new browser tab; the inline table still lets
   him read at a glance without leaving the email.

Requires the **Google Drive** connector enabled (`create_file`,
`get_file_metadata`). It is connected to the account; if its tools are disabled in
a given run, fall back to inline.

**`DELIVERY = "inline"`:** send the table inline only — no attachment, no
link. The content is fully in the body. (The saved `.html` is still useful for
`present_files` on manual runs.)

**Morning bump — prefer a scheduled draft, fall back to a 2nd task.** First check
whether the connected send tool can schedule delivery (a `send_at`/scheduled-send
param or a draft-with-future-time tool — Aidas's mail tooling may expose this even
though the basic send call may not). If yes, the single EOD run
sends now AND stages the morning copy as a scheduled draft. If no, register the
second cron (below) that re-sweeps the prior business day each morning.

### Step 6 — Report back

```
SEC Filing Catch Up — <date_label>   (source: EDGAR direct, MODE)
Universe swept: N tickers | Filings found: M
Sent: <EOD | morning recap> to RECIPIENTS as <connected account>
Rows:
- [TICKER] FORM — snapshot
- ...
```

---

## Running as scheduled tasks

Always register the **EOD task**. Register the **morning task ONLY as the fallback**
when the connected send tool can't schedule a draft — if it can, the EOD run
stages the morning copy itself.

1. **EOD task** — `cronExpression="25 18 * * 1-5"` (≈5 min before 18:30 ET), MODE eod.
2. **Morning task** — `cronExpression="30 7 * * 1-5"` (07:30 ET), MODE morning.

Cron is LOCAL time. Scheduled runs happen while the app is open; if it was closed
at fire time the task runs on next launch — the morning recap re-sweeps the prior
day, so it's correct whenever it runs.

Each scheduled prompt must be self-contained:

> Run the `sec-filing-catchup` skill end to end. Read its SKILL.md and follow
> Steps 0–6 with MODE="eod" [or "morning"]. Source filings by sweeping EDGAR
> directly across the Meteora SPAC universe (spac-details → edgar-filings per
> ticker for target_date); do NOT read BamSEC email. CONFIG: recipients =
> RECIPIENTS (as set by Aidas), TEST_MODE = false, subject "SEC Filing Catch Up".
> Send via the connected "send as me" email tool with the table as the INLINE HTML
> body (no attachment); DELIVERY="drive" also adds the Drive-PDF "Open as page"
> link. Do not use the Meteora send-email MCP (walter@). Digest only — no memory
> docs, no threaded replies, and no summary/headline box above the table.

## Failure modes & guardrails

- **Stale/blocked raw EDGAR (Path B):** if the daily-index directory doesn't list
  `form.{target_date}.idx` (mirror frozen, or env can't reach a current index),
  FALL BACK to Path A (per-ticker `edgar-filings`, the live channel). Never emit an
  empty digest because an index file was missing.
- **Ticker collision / dedupe:** collapse identical accession numbers to one
  row — a symbol can mis-resolve to another entity's CIK. Prefer CIK queries from
  the cached map.
- **Unresolved-ticker blind spot:** never treat an unresolvable ticker as "no
  filings." Resolve its CIK once, cache it, sweep by CIK thereafter, and report the
  still-unresolved count loudly so the gap is visible.
- **Per-ticker errors:** an `edgar-filings` call that errors or can't resolve a
  ticker is skipped and logged, never fatal — one bad ticker can't sink the run.
- **Rate limit:** keep parallel `edgar-filings` batches modest (~30) to respect
  EDGAR's ~10 req/sec fair-access limit.
- **Snapshot from filing only:** never fill "What happened" from the form type
  alone. Unretrievable text → say so in the cell.
- **No editorial layer:** never prepend a headline, summary, "AI analysis", or any
  prose box above the table. The deliverable is the rendered table only (clean date
  line + table). Send `/tmp/body.html` exactly as the renderer produced it.
- **No recipient = no send:** if `RECIPIENTS` is empty, ask the user — never guess.
- **Wrong sender:** never fall back to the Meteora `send-email` MCP (sends as
  walter@). Send as the connected personal account.
- **Empty day:** send the empty-table digest anyway.
- **Idempotency:** if run twice for the same date you'll send twice; on manual
  re-runs, confirm before re-sending.

## Tools used

| Step | Tool |
|---|---|
| 1 | `Meteora MCP: spac-details` (no ticker → full universe) |
| 2 | `Meteora MCP: edgar-filings` per CIK (Path A, primary); bundled `data/universe_cik_map.json` (name-verified, 321/358); `web_fetch` EDGAR `company_tickers.json` to resolve unresolved tickers; `web_fetch` daily-index `.idx` + `index.json` freshness check (Path B, optional) |
| 3 | `Meteora MCP: edgar-filing-text` |
| 4 | `scripts/render_catchup.py` |
| 5 | Connected "send as me" email tool (e.g. `mcp__outlook__send_email`; INLINE HTML body, no attachment). For `DELIVERY="drive"`: the `pdf` skill (HTML→PDF) + Google Drive MCP `create_file`/`get_file_metadata` to publish the PDF and get its `webViewLink`. |
| setup | `create_scheduled_task` (EOD always; morning only as bump fallback) |

## First-time setup (run once, with the user)

After a successful dry run, register the **EOD task** with `create_scheduled_task`
(`taskId="sec-filing-catchup-eod"`, `cronExpression="25 18 * * 1-5"`, MODE eod).
Add the **morning task** (`taskId="sec-filing-catchup-morning"`,
`cronExpression="30 7 * * 1-5"`, MODE morning) **only** if the send tool can't
schedule a draft. Confirm the cron timezone is the user's local ET, and don't
create tasks the user hasn't approved.

**On the first run, confirm two things with the user before sending:** (a) which
connected "send as me" email tool to use, and (b) the `RECIPIENTS` list. If
`RECIPIENTS` is empty, ask — never guess a recipient or send without one.
