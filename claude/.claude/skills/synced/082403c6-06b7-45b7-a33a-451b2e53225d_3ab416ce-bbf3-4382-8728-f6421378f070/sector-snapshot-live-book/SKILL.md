---
name: sector-snapshot-live-book
description: >-
  Refresh the "Sector Indices" Excel workbook's live Bloomberg values and email
  the Sector Heatmap, SPAC Scorecard, and Warrant Watch tables — each with a
  crisp, data-driven one-line read — to filings@meteoracapital.com as Walter,
  subject "Overall Sector Snapshot & Live Book". Trigger on "run the sector
  snapshot", "send the sector heatmap / scorecard / warrant email", "refresh the
  sector indices book and email it", "sector snapshot email", or on its scheduled
  weekday 8 PM run. The skill opens the workbook in Excel so the Bloomberg BDP
  formulas recalc, waits for the async pulls to settle, extracts the three
  tables, renders a green/red-shaded HTML email, and sends it via the Meteora
  send-email MCP (walter@). Always use this skill for the sector snapshot email —
  do not rebuild the tables or the email ad hoc.
---

# Sector Snapshot & Live Book

A once-a-weekday email. Open the **Sector Indices** workbook in Excel so every
Bloomberg `BDP` cell repulls, then lift the three summary tables into one crisp,
color-shaded HTML email for the desk.

The workbook is Bloomberg-driven: tickers live on the **Directory** tab and fan
out (via `BDP`) to per-sector index sheets, which roll up into three summary
tables. This skill emails those three tables:

- **Sector Heatmap** — equal-weight index return per sector (1D/1W/1M/YTD/1Y).
- **SPAC Scorecard** — per-sector book state (avg premium/discount to trust,
  names above/below) and performance vs HYG (credit) and SGOV (≈ trust).
- **Warrant Watch** — each warrant's return vs its sector's, so Lead/Lag isolates
  the name-specific move from the theme.

Why it must *open* Excel: the values come from `=BDP(...)` (PX_LAST, CHG_PCT_1D/
5D/1M/6M/YTD/1YR, INTERVAL_VWAP). Those only repull when the workbook is open in
Excel with the Bloomberg add-in loaded and the Terminal logged in. Reading the
file cold (openpyxl/pandas) returns yesterday's cached numbers.

---

## CONFIG — edit these, nothing else, to retune the skill

```
WORKBOOK      = "G:\Shared drives\Interns\Sector Indices\Sector Indices - Testing.xlsx"
SKILL_HOME    = "C:\Users\shain\Claude\Scheduled\sector-snapshot-live-book"
RECIPIENT     = "filings@meteoracapital.com"      # production recipient
TEST_RECIPIENT= "chauhan_intern@meteoracapital.com"
SUBJECT       = "Overall Sector Snapshot & Live Book"
SENDER        = walter@ (Meteora send-email MCP — the only sender it supports)
TEST_MODE     = false     # true -> send to TEST_RECIPIENT with "[TEST] " subject prefix
MAX_WAIT_SEC  = 240       # cap on the Bloomberg settle poll (typical settle ~60-90s)
```

To go live: `TEST_MODE = false`, recipient `filings@`. The 8 PM run is registered
as the scheduled task **sector-snapshot-live-book-8pm** (`0 20 * * 1-5`).

---

## Workflow

Three moving parts, all bundled under `SKILL_HOME`:
`scripts\refresh_and_extract.ps1` (Excel + Bloomberg → `out\tables.json`),
`scripts\render_email.py` (`tables.json` → `out\email.html`), then the
Meteora `send-email` MCP.

### Step 1 — Refresh Bloomberg and extract the tables

Launch the PowerShell refresher **detached** so it survives any single
tool-call timeout (the settle poll can run 1–4 minutes), then poll its log:

```powershell
# launch (returns immediately with the worker PID)
Start-Process powershell -WindowStyle Hidden -PassThru -ArgumentList `
  '-NoProfile','-ExecutionPolicy','Bypass','-File',`
  'C:\Users\shain\Claude\Scheduled\sector-snapshot-live-book\scripts\refresh_and_extract.ps1'
```

The script opens the workbook **read-only** (so it never fights a copy already
open, and never saves), forces a full recalc, then polls every 8 s counting
`"#N/A Requesting Data..."` cells until zero (or `MAX_WAIT_SEC`). It writes:

- `out\run.log` — timestamped progress (`t=NNs pending=NN`, then `DONE`).
- `out\tables.json` — the three tables as raw values + `settle_seconds`, `pending_left`.
- `out\status.json` — `{ ok, pending_left, settle_seconds, error }`.

**Wait for completion** by re-reading `out\run.log` every ~20–30 s until it ends
with a `DONE` line (or `out\status.json` exists). Cold start is ~40 s before the
first Bloomberg batch lands; full settle is usually 60–90 s.

Gate on `status.ok`:
- `ok = true` (pending_left 0) → proceed.
- `ok = false` with `pending_left > 0` → Bloomberg didn't fully settle in time.
  Proceed but note "some values may be stale" — OR, if `pending_left` is large
  (say > 50) or every table is blank, the Terminal is likely logged out; abort
  and report rather than send a wall of `#N/A`.
- `error` non-empty → report it; do not send.

### Step 2 — Render the HTML email

```powershell
python "C:\Users\shain\Claude\Scheduled\sector-snapshot-live-book\scripts\render_email.py" `
  "C:\Users\shain\Claude\Scheduled\sector-snapshot-live-book\out\tables.json" `
  "C:\Users\shain\Claude\Scheduled\sector-snapshot-live-book\out\email.html"
```

`render_email.py` (stdlib only) builds an Outlook-safe email: one `<style>`
block + `bgcolor` cells (green = positive / beating baseline, red = negative,
intensity by magnitude), percentages as Bloomberg change fields, VWAP as price,
and — computed straight from the live values — a one-line **Today:** takeaway
under each table plus an overall summary line. It prints
`WROTE <path> (<n> chars); sectors=.. warrants=..`.

### Step 3 — Send as Walter

Read `out\email.html` (UTF-8) and send its full contents as the HTML body via the
Meteora **send-email** MCP (it only sends as walter@):

```
send-email(
  to        = TEST_MODE ? [TEST_RECIPIENT] : [RECIPIENT],
  subject   = (TEST_MODE ? "[TEST] " : "") + "Overall Sector Snapshot & Live Book",
  content_type = "HTML",
  body      = <verbatim contents of out\email.html>
)
```

Send the body **verbatim** — the tables and the crisp reads are already inline.
No preamble, no attachment.

### Step 4 — Report back

One line: settle seconds, sectors/warrants counts, recipient, and the overall
takeaway (e.g. "Sent to filings@ — 9/11 sectors green; Software leads YTD
+39.7%, Nuclear worst −36.2%. Settled in 74 s.").

---

## Running as a scheduled task

Registered as **sector-snapshot-live-book-8pm**, `cronExpression="0 20 * * 1-5"`
(8 PM local, Mon–Fri). Cron is local time. Scheduled runs happen only while the
Claude desktop app is open; if it was closed at 8 PM the run fires on next launch.

Requirements at run time, on THIS machine:
- Excel installed with the **Bloomberg add-in** (`BloombergUI.xla`) enabled.
- **Bloomberg Terminal running and logged in** (BDP needs the live session).
- The `G:` shared drive mounted (Google Drive for Desktop).

## Failure modes & guardrails

- **Terminal logged out / add-in missing:** cells stay `"#N/A Requesting Data..."`
  and never settle → `status.ok=false`, large `pending_left`. Don't email a wall
  of `#N/A`; report that Bloomberg didn't connect and skip the send.
- **Workbook already open by the user:** fine — we open a separate **read-only**
  instance, so there's no lock conflict and nothing is saved back.
- **Tool-call timeout during the wait:** expected. The refresher runs detached;
  always drive it via the `run.log` / `status.json` poll, never by holding one
  long call open.
- **Orphaned headless Excel:** the script Quits Excel in a `finally` block. If a
  run was force-killed mid-way, close stray *window-less* EXCEL.EXE before the
  next run (never kill an Excel that has a visible workbook — that's the user's).
- **Slow first pull:** cold start ~40 s before the first batch resolves; the
  240 s cap covers the full ~60 sector/warrant names comfortably.
- **Never save the workbook** from automation — read-only only.

## Tools used

| Step | Tool |
|---|---|
| 1 | Desktop Commander `start_process` → `scripts\refresh_and_extract.ps1` (Excel COM, read-only, Bloomberg poll) |
| 1 | Desktop Commander `read_file` → poll `out\run.log` / `out\status.json` |
| 2 | Desktop Commander `start_process` → `python scripts\render_email.py` |
| 3 | Desktop Commander `read_file` → `out\email.html`; Meteora **send-email** MCP (walter@) |
| setup | `create_scheduled_task` (`0 20 * * 1-5`) |

## First-time / retarget notes

- The three tables are fixed sheet names: `Sector Heatmap`, `SPAC Scorecard`,
  `Warrant Watch`. If the workbook is renamed or moved, update `WORKBOOK`.
- Data rows begin at row 5 on each sheet (rows 1–4 are title/description/
  group-header/column-header); `render_email.py` slices `[4:]` accordingly.
- To preview without emailing the desk, set `TEST_MODE=true` (goes to
  chauhan_intern@ with a `[TEST]` subject).
