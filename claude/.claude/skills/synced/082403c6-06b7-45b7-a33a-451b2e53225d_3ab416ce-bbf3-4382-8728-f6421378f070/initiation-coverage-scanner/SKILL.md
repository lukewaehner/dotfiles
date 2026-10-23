---
name: initiation-coverage-scanner
description: >-
  Daily scan of the connected Outlook/M365 mailbox for sell-side equity research INITIATION-OF-COVERAGE notes, then download the full note as a PDF and file it to the Initiation of Coverage Notes shared drive. Trigger on "scan for initiation notes", "run the IC scan", "check for new initiations", "any coverage initiations today", "process the research initiations", or a scheduled daily run. ALSO trigger when the user forwards or references a broker research email that looks like a new initiation (a NEW rating + price target on one company from a desk like JonesTrading) and wants it captured/filed. Handles notes in the email body, a PDF attachment, or behind a View-PDF/portal link (opened via Claude in Chrome). Applies a substance gate so only real long-form initiations are kept, and dedupes via a ledger so nothing is downloaded twice. Download-and-file only — it does NOT read the note in depth or send any email. Always use this skill for initiation notes; not ad hoc.
---

# Initiation of Coverage Scanner

Capture sell-side equity-research **initiation-of-coverage** notes that arrive in the connected
Microsoft 365 / Outlook mailbox, and **file each qualifying note as a PDF into the shared-drive
folder**. The job is meant to run once a day (a scheduled task fires it, typically ~3pm), but it
also runs on demand.

This is a **download-and-file (ingest) job only**. Its whole purpose is to catch genuine new
initiations, pull the complete note, confirm it clears a substance bar, and archive it to the
shared drive under a standard filename — then record it in a ledger so the same note is never
downloaded twice. It does **not** read the note in depth, produce a summary, or send any email.

---

## Configuration (edit these before running)

```
LOOKBACK_HOURS      = 24                # only emails received in the last 24h
MAILBOX_FOLDER      = "Inbox"           # folder to scan
SAVE_DIR            = "G:\Shared drives\Interns\Initiation of Coverage Notes"
LEDGER_FILE         = "[SAVE_DIR]\.ic_ledger.json"   # dedup record, lives beside the notes
TEST_MODE           = true              # true = dry run: still download + save the PDF so a
                                        #   human can inspect it, but DO NOT write the ledger
                                        #   (so a later real run re-processes the note). Flip to
                                        #   false to go live and record saves to the ledger.
```

`SAVE_DIR` is a Google Shared Drive path on the user's machine. The automation can only write
there if that folder is connected/mounted to this environment. If a write to `SAVE_DIR` fails,
stop and tell the user the folder needs to be connected (offer `request_cowork_directory`) - do
**not** silently save somewhere else.

---

## Workflow

### 1. Confirm mailbox access
Call `whoami()` on the Email Assistant (Microsoft 365) extension. If not signed in, run the
sign-in flow (`configure` -> `sign_in` -> `complete_sign_in`) before continuing. All mailbox
reads go through the **Email Assistant** extension - never another connector's email tool.

### 2. Pull the last 24 hours
Compute the ISO date for `now - LOOKBACK_HOURS` and call
`search_emails(after=[iso], folder=MAILBOX_FOLDER, max_results=100, order="asc")`.
Do a broad pull rather than a narrow subject filter - initiation notes do **not** share a
common subject line, so filtering only on "initiation" would miss many. You will classify in
the next step.

Because search granularity is by date (not hour), you may get emails slightly older than 24h.
Check each candidate's actual received timestamp and drop anything older than the cutoff.

### 3. Identify true initiation-of-coverage notes (use judgment, not keyword matching)
Read each email (subject + sender + a `read_email` of the body when the subject is at all
plausible). You are looking for a **sell-side research note that ESTABLISHES NEW coverage on a
single public company**. Positive signals, in rough priority order:

- Explicit language: "initiating coverage", "we initiate", "new initiation", "launching
  coverage", "assuming coverage", "coverage initiated", "IC:".
- A **newly stated rating** (Buy / Outperform / Overweight / Hold / Neutral / Sell /
  Underweight) **plus a price target**, framed as a first view rather than an update.
- Sent from a sell-side research desk / analyst (e.g., JonesTrading and similar). Forwarded
  broker emails count.
- A single named ticker as the subject of the note.

Reject (these are NOT initiations, even if they mention a rating or price target):

- Earnings reactions, quarterly previews/recaps, estimate revisions, price-target changes,
  and **upgrades/downgrades of coverage that already exists**.
- Sector/industry primers, macro notes, thematic pieces with no single-name initiation.
- Sales blasts, trade ideas, morning notes, calendars, conference invites, corporate access.
- Duplicates already in the ledger (see step 4).

When genuinely unsure whether something is a *new* initiation vs. an update, prefer to read
the body: an initiation almost always contains an explicit "we are initiating coverage of
[Company]" sentence and a full company primer. If that sentence is absent, treat it as not an
initiation.

Extract just what you need to dedupe and file each keeper: **Company name, Ticker, Provider
(bank/desk), and the note date**, plus whether the full note is (a) in the body, (b) an
attachment, or (c) behind a link. (You do not need to pull ratings, price targets, or estimates
- there is no summary to produce.)

### 4. Dedupe against the ledger
Read `LEDGER_FILE` (JSON list). Build a dedup key for each candidate:
`normalize(TICKER) + "|" + normalize(PROVIDER)`. Also keep the email's `internetMessageId`.
Skip any candidate whose ticker+provider key OR message-id already appears in the ledger. This
prevents re-downloading on re-runs and when the same note is forwarded multiple times. The
ledger is only appended (never download twice for the same note) - and in `TEST_MODE` you read
it but do not write it.

Use `scripts/note_utils.py` for ledger read/append and key normalization (see "Helper script").

### 5. Capture the COMPLETE note
The email body is often only a teaser. Always get the full note. Decision tree:

- **PDF attachment present** -> `list_attachments(message_id)`, then
  `download_attachments(message_id, output_dir=[workspace tmp])`. That PDF is the note.
- **A "View PDF" / research-portal / broker link is present** (JonesTrading and many desks
  publish this way) -> open it with **Claude in Chrome** and download it — see
  "Downloading a linked note" below. If the page is HTML rather than a PDF, use
  `get_page_text` / `read_page` to pull the complete text and render it to a PDF (see
  "Rendering a PDF"). If the link demands a login you don't have, note the limitation and fall
  back to whatever full text the email body provides.
- **Full note is in the email body, no richer link** -> the body is the note. Save a clean copy
  as PDF (see "Rendering a PDF").
- **Partial in body + link to the full note** -> always prefer the linked full version; use the
  body only as a fallback if the link can't be retrieved.

**Browser prerequisite.** Run this on a Chrome that is on the SAME machine as `SAVE_DIR`
(check `list_connected_browsers`; prefer the browser with `isLocal: true`). If the browser is
on a different computer than the shared drive, downloads land on the wrong machine and you will
not see them. Ideally turn off Chrome's "Ask where to save each file before downloading" so
downloads save silently to the default Downloads folder.

**Downloading a linked note (DOM-first, then click the button as fallback).** The fastest,
most reliable path is a DOM download; only fall back to clicking the viewer's button if that
fails.

1. **Fastest - DOM download.** `navigate` to the PDF/link, then run an in-page fetch and
   trigger a synthetic-anchor download:
   ```js
   const r = await fetch(URL, {credentials:"include"});
   const b = new Blob([await r.arrayBuffer()], {type:"application/pdf"});
   const a = document.createElement("a");
   a.href = URL.createObjectURL(b);
   a.download = "<standard filename>.pdf";
   document.body.appendChild(a); a.click();
   ```
   The file lands in the browser's Downloads folder. Confirm it appears there (by filename)
   within a few seconds.
2. **Fallback - click the Download button with the mouse.** If the file does NOT appear (the
   built-in PDF viewer's restricted context can swallow a synthetic click, or a native Save
   dialog intervened), take a `screenshot`, locate the PDF viewer's **Download** icon at the
   top-right of the viewer toolbar, and **click it** (computer-use mouse). Handle any Save
   dialog, then confirm the file saved.
3. Once saved, move/copy the PDF into `SAVE_DIR` with the standard filename (step 7).

Keep the captured note file in a temporary workspace location for now; it moves to `SAVE_DIR`
only after it passes the substance gate. Text measurement for the gate is handled in the
sandbox by `note_utils.py` (pdftotext) - you do NOT need to extract the note's text through the
browser bridge.

### 6. Substance gate (composite - better than a raw page count)
A real initiation is long-form and analytical. Run `scripts/note_utils.py analyze [note.pdf]`
(or `analyze-text` for body-only notes) to compute the gate. A note **passes** when it is a
genuine new initiation AND is substantive:

1. **Is an initiation** - confirmed in step 3.
2. **Has analytical depth** - contains at least a valuation/price-target rationale section and
   a financials/estimates discussion (look for headings/terms like Valuation, Estimates,
   Financial Model, Forecast, Risks).
3. **Length floor** - **>= ~2,500 words** of substantive content (disclaimers/boilerplate
   excluded) **OR >= 8 pages**. The page backstop is first-class, not just for image-only PDFs:
   text extraction under-counts on many research PDFs, and a genuine long-form initiation runs
   many pages while a flash blast is one or two. The script (`note_utils.py`) already extracts
   with `pdftotext` and trims disclosures only when they appear in the back of the document, so
   an early "important disclosures" nav line or a page-1 watermark can't gut the word count.

Rationale: page count alone is a weak proxy - a dense 6-page initiation beats a 12-page one
padded with disclosures - so the gate pairs it with structure (valuation + estimates/risks) and
the new-initiation classification. Together these catch real research and filter flash blasts,
one-pagers, and marketing. If a note fails the gate, skip it (do not save it); if `TEST_MODE`,
still note in the run log that it was seen and why it was skipped.

### 7. Save the PDF to the shared drive
Filename (exact pattern, sanitized for filesystem - strip characters like `:` `/` `*`):

```
Initiation of Coverage - [Company] ([TICKER]) - [Provider] - [YYYY-MM-DD].pdf
```

Example: `Initiation of Coverage - Everspin Technologies (MRAM) - JonesTrading - 2026-07-10.pdf`

Write/copy the PDF into `SAVE_DIR`. If `SAVE_DIR` is unwritable, stop and ask the user to
connect the folder (see Configuration). In `TEST_MODE` you still save the PDF (so the human can
inspect it) but you flag clearly that it's a dry run and the ledger was not written.

### 8. Update the ledger
On a successful live save, append the record to `LEDGER_FILE`:
`{ticker, provider, company, message_id, saved_pdf, saved_at}`. In `TEST_MODE`, skip this so a
real run later still processes the note.

### 9. Report
Summarize the run to the user: how many emails scanned, how many classified as initiations,
how many passed/failed the gate (with reasons), and which files were saved (with their
`SAVE_DIR` paths). If multiple notes qualified, list each saved file. In `TEST_MODE`, remind
the user that the ledger was not written and to flip `TEST_MODE` off when ready to go live.

---

## Rendering a PDF (when the note is body/HTML, not an attachment)

When the complete note is HTML/text (email body, or an HTML research page pulled via Chrome),
render it to PDF so the shared-drive artifact is consistent. Simplest reliable path: write the
content to a clean HTML file and convert with a headless renderer available in the sandbox
(e.g., `wkhtmltopdf`, `weasyprint`, or Chromium `--headless --print-to-pdf`), or use the `pdf`
skill to produce the PDF. Preserve tables and headings; drop email chrome (signatures,
"Get Outlook for iOS", legal footers) so the saved note is clean.

---

## Helper script

`scripts/note_utils.py` centralizes the deterministic bits so every run behaves the same:

- `analyze [path-to-pdf]` -> prints JSON: `page_count`, `word_count`, detected sections
  (valuation / estimates / risks), and `passes_length` / `passes_structure`.
- `analyze-text [path-to-txt]` -> same, for body-only notes.
- `ledger-check [ledger.json] [ticker] [provider] [message_id]` -> prints `DUPLICATE` or `NEW`.
- `ledger-append [ledger.json] [json-record]` -> appends a record.
- `filename [company] [ticker] [provider] [yyyy-mm-dd]` -> prints the sanitized filename.

Run it in the sandbox against files in the workspace. It only does measurement and
bookkeeping - the judgment call (is this really an initiation?) stays with you.

---

## Reference files

- `scripts/note_utils.py` — deterministic measurement + ledger bookkeeping (see Helper script).

## Failure handling & edge cases

- **Multiple initiations in one day** -> process each independently; one saved PDF per note.
- **Link needs a login you don't have** -> capture whatever full text the email provides, note
  the limitation in the run log, and still apply the gate to what you have (a login-walled note
  that leaves you only a short teaser will usually - correctly - fail the gate).
- **Image-only / scanned PDF** -> use the `pdf` skill's OCR; if word count still can't be
  measured, use the >= 8-page backstop for the gate.
- **`SAVE_DIR` not writable** -> stop, tell the user to connect the shared-drive folder; don't
  reroute the save.
- **Nothing qualifies** -> save nothing; report "scanned N, 0 initiations" so the user knows the
  job ran.
- Keep the whole run non-destructive in `TEST_MODE` until the user has seen a real example and
  is happy: the saved PDF plus the run log are the review artifacts, and the ledger stays
  untouched.
