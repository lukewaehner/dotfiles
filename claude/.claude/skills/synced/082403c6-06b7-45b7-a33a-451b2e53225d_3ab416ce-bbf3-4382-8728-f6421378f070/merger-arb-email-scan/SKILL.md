---
name: "merger-arb-email-scan"
description: "Scan Filings@ for forwarded broker merger-arb notes (UBS, TD, Jefferies, RJF, Oscar Gruss, Elevation, CTFN, any broker), check them against the deal memory doc so only material news gets posted, check where we stand (EMSX blotter, memory doc, live spread), and post a short desk analysis as a reply-all on that ticker's existing Internal chain in meteora-email-format-v2 HTML. Keeps each deal's memory doc current (seed with merger-arb-memory-doc-v1 if missing, else update-merger-arb-memory-doc-v3-10202026). Every run also checks for Daily Blotter Notes (several a day, including Midday) and the Internal Transcript; each note is handled on its own the first time it is seen, and posts a per-deal recap (what we traded, or what the desk call said, and what changed since the last post) on each merger-arb Internal chain. Nothing is posted for a note until that note has been sent to Filings@. Runs 6:30 AM-7:30 PM ET on weekdays. Use for 'run the merger arb email scan' and its recurring runs."
---

# Merger Arb Email Scan

Every run does three jobs, in this order:

1. **Broker-note scan (Steps 1-7).** Finds merger-arb broker notes forwarded to Filings@meteoracapital.com, splits each note by deal, checks every fact against the deal's memory doc, and for every deal with an EXISTING "Internal {TICKER}" chain and something material to say, posts ONE analytical update: where we stand (book, our view, tape), what the new note says, and what it changes. The broker text goes at the bottom as the source, not as the post.
2. **Memory-doc upkeep (Step 8).** For every ticker that got a post this run, brings its memory doc up to date with what is on the chain: seeds it with `merger-arb-memory-doc-v1` if it does not exist, otherwise updates it with `update-merger-arb-memory-doc-v3-10202026`.
3. **Blotter and transcript recaps (Step 9). Most important job; never skip the check.** Every run looks for Daily Blotter Notes and the Internal Transcript sent to Filings@. Each note is its own trigger: the first time a run sees a note, it posts a per-deal recap from that note alone on each merger-arb deal's Internal chain, saying what changed since the last post on that chain, then updates the memory doc. Blotter notes do not wait for the transcript and the transcript does not wait for the blotter. No note sent, no recap.

It never creates a new chain. Built to run unattended, so a run that finds nothing new and has no end-of-day work must end in a few tool calls.

No visible tags in posts. Dedup lives in the MASCANDEDUPE memory doc (Step 5).

Every post is sent as HTML in the **meteora-email-format-v2** house format, using the same layout as its SPAC notes: body, then background rail with the Snapshot table (Step 6b). This skill adopts that format on purpose, as the user's standing instruction, so the "invoked explicitly" rule in meteora-email-format-v2 is satisfied by this skill. Plain-text posts are no longer allowed.

A local Python job (`ma-scan`, launchd every 5 minutes on Lukas's Mac) used to post UBS notes verbatim with a visible `[MA-SCAN ...]` tag. That job must either be paused or changed to read and write the MASCANDEDUPE ledger with the same fingerprint, or it will double-post next to this skill. Until then, Step 5 also treats a legacy tag in the thread as "already posted".

## Config

| Key | Value |
|---|---|
| `run_window` | 06:30-19:30 America/New_York, Monday-Friday. Allow a 5-minute tolerance on each edge (a 06:29 or 19:31 start counts as inside). Outside the window, print `MA-SCAN {time ET}: outside run window` and stop. |
| `lookback_minutes` | 65 for the hourly run; 20 if looping every 5 min. On the first run of the day (the first run at or after 06:25 ET), look back to 19:30 ET on the previous business day instead, so notes that arrived overnight are covered. |
| `filings_address` | Filings@meteoracapital.com |
| `internal_domain` | meteoracapital.com |
| `sender` | lukas@meteoracapital.com. Every post goes out from this account and no other (Step 0). |
| `ledger_doc` | MASCANDEDUPE (memory doc), for broker-note posts. Format shared with the ma-scan script; do not change it. |
| `eod_ledger_doc` | MASCANEOD (memory doc), for blotter and transcript recaps and memory-doc runs. Used only by this skill (Step 9). |
| `blotter_subject` | `Daily Blotter Note` (sent by an internal address to Filings@, e.g. "Daily Blotter Note — 11.10.2026", "Daily Blotter Note — 11.10.2026 (Midday)"). There can be several in a day (Midday, end of day, re-sends). Every one is a separate source (Step 9). |
| `transcript_subject` | `Internal Transcript` (internal sender to Filings@; the subject is often a reused chain like "RE: Internal Transcript: 9/17 PM", so identify the day from the body heading "Meteora End-of-Day Summary — {Month D, YYYY}" / "Internal Transcript: {M/D} PM", not from the subject). |
| `test_prefix` | "Shivom testing" |
| `test_prefix_dates` | 2026-10-07 (America/New_York). On these dates line 1 of every post is the test prefix; on other dates it is omitted. |

## Tools

- **Detection and reading:** MeteoraMCP-AWS `list-emails` and `read-email`. They return exact `receivedDateTime` and the full HTML body. Do not use the Email Assistant's `read_email` for source text (it truncates).
- **Where we stand:**
  - `emsx-blotter(tickers=[...])` (MeteoraMCP): live working orders for the target and acquirer. Call it once per run with every deal ticker. For today's executions, also call with `order_status="FILLED"`. The blotter shows orders, not positions; never state a position size it does not show.
  - `list-memory-docs` (once per run; the result is large, so save it and grep for names) and `read-memory-doc(name, entries_limit=3)` (MeteoraMCP-AWS). Deal docs are named `{TARGET}` or `{TARGET}-{ACQUIRER}` (e.g. OPCH, ROKU-FOXA, SYNA-ON). Ignore `COVENANT-*`, `*DEDUPE`, SPAC theme docs.
  - `merger-arb-list` (MeteoraMCP-AWS): deal terms (cash, exchange ratio, expected close) for the spread.
  - `get-price(tickers=[target, acquirer])` (MeteoraMCP): live bid/ask/mid. Quote mid and say which session.
- **Memory-doc upkeep (Step 8):** the `merger-arb-memory-doc-v1` skill (seed a doc that does not exist) and the `update-merger-arb-memory-doc-v3-10202026` skill (update a doc that exists). Load each with the Skill tool when Step 8 needs it, never before. If a skill can't be loaded, log `mem-skill unavailable: {name}` and carry on; the posts still go out.
- **Format:** the `meteora-email-format-v2` skill. Load it with the Skill tool once per run, before the first post (skip this on a run with nothing to post). Its files are `references/shell.html` (the template) and `scripts/validate_html.py` (the pre-send gate). Find them with `find / -path '*meteora-email-format-v2/references/shell.html' 2>/dev/null | head -1`. If the skill or either file can't be found, post nothing this run, write no ledger lines, and log `format unavailable`. The next run retries.
- **Posting:** Email Assistant (Microsoft 365) on the user's computer: `whoami`, `search_emails`, `read_thread`, `read_email`, `reply_all_email` (with `html=True`). The Email Assistant sends as whoever is signed in, and that must be `sender` (lukas@meteoracapital.com). Never send through MeteoraMCP `send-email` or any other sender.
- **Step 0a (window):** check the current time in America/New_York against `run_window`. Outside it, print `MA-SCAN {time ET}: outside run window` and stop without any other tool call.
- **Step 0:** Email Assistant `whoami()`. The signed-in account must be `sender` (lukas@meteoracapital.com, case-insensitive). If nobody is signed in, or anyone else is (e.g. Shivom_intern@meteoracapital.com), post nothing this run and write no ledger lines. You may still run Steps 1-6 and 9.1-9.3 so the log shows what would have posted (Step 8 never runs without a post), but end with `sender mismatch: signed in as {whoami result}` and stop. Never call `sign_out`, `sign_in` or `configure` on an unattended run: switching accounts needs Lukas to finish a browser sign-in. The next run retries.

## Step 1: Detect

1. `list-emails(search="recipients:filings@meteoracapital.com", top=50)`. Keep messages whose `receivedDateTime` is within `lookback_minutes`. If the oldest kept message is still inside the window, page further; if the cursor errors, run a second search `recipients:filings@meteoracapital.com AND subject:FW` to cover the gap. If none survive Steps 1-3, skip straight to Step 9 (the end-of-day check runs on every run, even when there are no broker notes). Only when Step 9 also has nothing to do, print `MA-SCAN {time ET}: nothing new` and end.
2. Subject filter (no body read). Drop if the subject contains, case-insensitively: `Internal `, `CA EVENTS`, `JEF Access`, `Jefferies Host`, `Group Call`, `Fireside`, `Dinner`, `Roadshow`, `REGISTER`, `Hosted Meetings`, `Conference`, `Webinar`, `[S-1`, `[F-1`, `S-1/A`, `Video`, `Allocations`, `[MA-SCAN`, `UBS Call on`, `SPAC News Roundup`, `Daily Digest`, `LevFin`, `US HY Data`, `Free To Trade`, `Technical Take`, `WHAT TRADERS ARE WATCHING`, `Morning Call:`.
3. Keep only messages forwarded by someone on `internal_domain` that quote an external original (`From:` with a non-meteoracapital.com address). Any external broker or news service counts (ubs.com, td.com, raymondjames.com, oscargruss.com, elevationsecurities.com, arbjournal.com, pressrisk.io/CTFN, utdfirst.com, cantor.com, jonestrading.com, ...).
4. If a broker sends a "(correction)" of a note in the window, use the correction and log the original as `superseded`.

## Step 2: Read and classify

- `read-email(message_id)` for each survivor. If the result is saved to a file, parse it with python: drop style/script, turn `<br>`, `</p>`, `</div>`, `</tr>`, `</li>` into newlines, `html.unescape`, collapse whitespace.
- Keep only merger-arb content: spreads, proration, tenders, HSR, second requests, antitrust, CFIUS, state or foreign approvals, votes, timing, terms, topping bids, financing, deal litigation. Drop invites, single-name research, macro, credit, SPAC IPOs, spin-offs with no deal.

## Step 3: Split by deal

- File each item under the TARGET ticker (UNF-CTAS, ROKU-FOX, "PTC-SU FP" → target first). A post-close instrument of a deal files under the deal's target chain (SKYD warrants → WBD).
- A deal's section is every line about it: one-liners, calendar rows, dedicated sections, roundup blocks.
- Keep the exact broker text for each section (it becomes the Source block). Strip legal disclaimers, contact blocks, unsubscribe footers.

Reference universe: `merger-arb-list`. A ticker missing from it is still eligible; the gate is whether its Internal chain exists.

## Step 4: Find the existing chain

- `search_emails(subject="Internal {TICKER}", folder="Inbox", max_results=25)`; if nothing qualifies, repeat with `folder="SentItems"`.
- A hit qualifies only if its subject, after any Re:/RE:/Fw: prefixes, contains `Internal {TICKER}` case-insensitively with the ticker followed by a space, `(`, `:`, `/`, `-` or end of subject. "Internal BOW" must not match "INTERNAL BOWN"; "Internal D" must not match "Internal DV".
- Use the newest qualifying message. No qualifying chain: skip and log `no chain: {TICKER}`. Never create a new email or chain.

## Step 5: Dedup (ledger, no visible tag)

Fingerprint per source, computed in Bash exactly like this (shared with the ma-scan script):

```python
import hashlib, re
from datetime import datetime
from zoneinfo import ZoneInfo
def fingerprint(subject, sender, received_iso):
    s = re.sub(r"^\s*((re|fw|fwd)\s*:\s*)+", "", subject or "", flags=re.I)
    s = re.sub(r"\s+", " ", s).strip().lower()
    d = datetime.fromisoformat(received_iso.replace("Z", "+00:00")).astimezone(ZoneInfo("America/New_York")).date().isoformat()
    return hashlib.sha1(f"{s}|{sender.lower()}|{d}".encode()).hexdigest()[:10]
```

`subject` is the Filings@ message subject, `sender` the forwarder's address, `received_iso` its `receivedDateTime`.

- Read the ledger once per run: `read-memory-doc("MASCANDEDUPE", summary_only=true)`. If it returns `not_found`, create it with `create-memory-doc` and the summary below. If the read errors or the `POSTED` heading is missing, treat it as a FAILED read, not an empty ledger: fall back to the thread check only and log it.
- A (fingerprint, ticker) pair is already posted if the ledger has a line starting `{fingerprint} | {TICKER} |`, or (legacy) `read_thread` on the chain contains `[MA-SCAN src={fingerprint} tkr={TICKER}]`. Skip those sources for that ticker.
- If every source for a ticker is already posted, skip the ticker (`dup`).

Ledger seed summary:

```
Dedupe ledger for merger-arb-email-scan and the ma-scan script. NOT a research doc.
One line per (source, ticker) posted: <fingerprint> | <TICKER> | <chain subject, prefixes stripped> | <YYYY-MM-DD HH:MM ET> | <posted|no-news>
Prune lines older than 30 days on the first run of each ET day.

### POSTED
```

Write side: immediately after each successful send (and after each `no-news` decision in Step 6), add one line per fingerprint covered with `patch-memory-summary`, replacing `### POSTED` with `### POSTED\n{new lines}`. Log right after the send, never batched at the end of the run, so a crash cannot cause a re-post.

## Step 6: Where we stand, then analysis

For each ticker that still has unposted sources, gather context BEFORE writing:

1. **Book:** blotter rows for the target and acquirer (side, quantity, filled, working, limit or MKT, TIF, date). If none: "No working orders on the blotter." Never guess position size.
2. **Our view:** the deal memory doc. Pull the as-of date, terms, our close date and its basis, the gating approvals, risk ratings, Street views on file, and the open questions. If there is no doc, say "No memory doc on file".
3. **Tape:** `get-price` for target and acquirer. With the terms from the memory doc or `merger-arb-list`, compute deal value, gross spread ($ and %), and annualized return to our close date (show the date used). For stock or mixed deals, value the stock leg at the acquirer mid. If any input is missing, say which and skip the number; never invent terms or prices.
4. **What is new: check the memory doc every time, then judge what matters.** This check is mandatory for every ticker, every source, every run. Read the deal doc (`read-memory-doc(name, entries_limit=5)`: summary, open-question register, the most recent entries) AND the last 3-5 posts on the Internal chain (`read_thread`, read fresh right before drafting, every time, because a blotter recap or a person's reply may have landed since the last run). Then list each fact in the source and classify it:
   - **NEW**: not in the doc or on the chain.
   - **CONFIRMS**: already in the doc or on the chain (same fact, same date, same number).
   - **CONTRADICTS**: differs from our view (a different close date, risk call, term, or count).

   Then rate each NEW or CONTRADICTS fact as **MATERIAL** or **NOISE**. Be strict; the desk reads these on a phone between trades.

   | MATERIAL (worth a post) | NOISE (never worth a post on its own) |
   |---|---|
   | A regulatory step changes status: HSR filed/cleared/pulled-and-refiled, second request, foreign or FDI clearance or Phase 2, CFIUS, state or sector regulator action or hearing date | A second outlet restating a filing or event already posted on the chain or logged in the doc |
   | A new or changed date: expected close, vote, outside date, hearing, decision deadline, marketing-period start | "On track", "we await closing", "nice customary timeline" and other tone with no new fact |
   | Terms change: price, ratio, CVR, collar, financing, a price cut or bump, extension of the DMA | Day counts ("Day 96"), deal recaps, structure descriptions we already have |
   | A topping bid, activist, go-shop result, or deal-break signal | A broker's own view that merely agrees with ours and adds no date, number, or reason |
   | Litigation: filed, injunction motion, ruling, settlement | Calendar rows repeating a date already in the doc |
   | A priority-tier broker's view that differs from ours, or gives the first dated view since a milestone | Single-name fundamentals, credit, or macro mixed into the note |
   | Something that answers or reopens an open question (OQ-n) in the doc | Teasers with no facts beyond the headline (e.g. a paywalled "click for full article") unless the headline itself is a material fact |

   Worked example (DV, 11/10/2026): ArbJournal said DV's Q4 2026 guidance is "great news", the deal is "at Day 96", and it is "solidly on track". The Q4 guidance was already posted on the chain on 11/9 and agrees with the doc's 11/27 base. Everything is CONFIRMS or NOISE, so: no post, `no-news`.

If the ticker has no MATERIAL fact, do not post. Log `no-news` in the ledger and in the run log, with a 5-10 word reason (e.g. `no-news: DV (restates 11/9 Q4 guidance; tone only)`). When it is a close call, post; say in the takeaway line what is new and keep the post short.

If the source is MATERIAL but its only content is a PDF attachment (empty body), read it with `get-email-attachment`, take the text from the PDF, and use that text as the verbatim Source block. If the attachment can't be read, log `attachment-only: {subject}` instead of dropping it silently.

Otherwise draft the post content. Desk tone, short sentences, numbers over adjectives, under ~250 words above the Source block. This outline sets the content and order only; Step 6b turns it into house HTML.

```
Shivom testing                                   <- only on test_prefix_dates
{TICKER}/{ACQ}: {one-line takeaway, e.g. "RJF sees no 2nd Request; keeps 3/31/27 close, matches ours"}

WHERE WE STAND
- Book: {blotter summary or "No working orders on the blotter"}
- Our view ({memory doc name}, as of {date}): {close date + basis; gating item; risk rating}
- Tape ({session} {HH:MM ET}): {TGT} {mid} / {ACQ} {mid} -> deal value {x}, spread {$} ({%}), {annualized %} to {close date}

WHAT THE NOTES SAY
- {Broker}: {2-3 lines in plain language with the specific facts, dates, numbers}
- {Broker 2}: ...

WHAT IT MEANS
- New vs known: {what is actually new; what just repeats what we have}
- Changed since the last post ({who/what, time}): {what differs from the latest post on the chain, e.g. a moved close date or new fills; or "no change"}
- Timing / probability / terms: {effect on our close date, risk read, or spread; say if it moves an open question (OQ-n) and how}
- Book: {how it bears on the working orders, as an observation, e.g. "supports the working 1,000 ROKU sell"; never place, change or recommend specific orders}
- Watch: {next dated catalyst}

SOURCE
{Broker} ({analysts}) | "{original subject without FW:}" | {original sent time ET} | fwd by {forwarder}
{verbatim broker section}
(repeat per source)
```

Analysis rules:
- Every claim in WHERE WE STAND and WHAT IT MEANS must come from the blotter, the memory doc, get-price, or the notes themselves. Name the source when it matters ("per the OPCH doc", "per RJF"). No outside knowledge, no speculation dressed as fact.
- Say plainly when a broker disagrees with our view (different close date, different risk call) and by how much.
- WHAT THE NOTES SAY paraphrases; the SOURCE block keeps the exact text (never edit broker words there).
- One post per ticker per run, covering all of that ticker's new sources.
- WHAT IT MEANS covers only the MATERIAL facts. If a source also carries NOISE, leave it out of the analysis (it stays in the verbatim Source block).

## Step 6b: Render in meteora-email-format-v2 (SPAC-style enhanced layout)

Every post uses the same layout as a SPAC note in meteora-email-format-v2's **Enhanced** mode: the body on top, then the **background rail**, with the **Snapshot table** inside the rail where the SPAC template puts it. Validate with `--mode enhanced`.

**This deliberately overrides one line in meteora-email-format-v2.** That skill says merger-arb names get no Snapshot table. On the user's instruction (Lukas, 2026-10-16), this skill's posts use one anyway, adapted as described in section 3. The override applies only to this skill's posts. Everything else in that skill still applies: copy each file fresh, inline styles only, closed palette, red rationed, footer, stamp, and internal recipients only.

Read `references/shell.html`, `references/background-rail.html` and `references/snapshot-table.html` **fresh, right before you render each post**. Copy their markup, styles and structure from those reads. Never rebuild them from memory.

### 1. Shell (top of the note): what's new goes here

| Shell slot | Content |
|---|---|
| Test prefix (only on `test_prefix_dates`) | Insert `<div style="font-weight:700;color:#0f2942;margin:0 0 4px">Shivom testing</div>` as the first element inside the wrapper, above the stamp. On other dates, leave it out. |
| Provenance stamp | **Keep** `Cowork generated`. Claude writes the analysis. |
| Title | `{TARGET} / {ACQUIRER}`, or just `{TARGET}` if the acquirer is private or undisclosed |
| Subline | `Broker note scan · {broker short names} · {YYYY-MM-DD}` |
| First body paragraph | The one-line takeaway, with no heading above it |
| Sections | `What the notes say`, then `What it means`. Each one is a section-heading div followed by `<ul style="margin:0 0 8px;padding-left:18px">` with one `<li style="margin:0 0 3px">` per bullet in the Step 6 draft. The `Book` observation stays as a bullet under `What it means`. The draft's `Where we stand` content moves into the rail and the Snapshot. |
| Source link `<p>` | Use it when a source carries a deal or article URL (e.g. the ArbJournal dealDetail link or the CTFN article link), one `<p>` per link. Otherwise delete it. |
| Action line | **Delete it.** This skill never decides or recommends trades. |
| Calendar line | The `Watch` item(s), as one short sentence per dated catalyst. Delete the line if nothing is dated. |

### 2. Background rail: context and the broker text

Copy `background-rail.html`. Keep its divider, its eyebrow (exactly `Background &mdash; history and reference, for anyone catching up`), and the recessed `border-left:3px` block at 12px. Use these sub-headings, at the rail's sub-heading spec, in this order:

- **Where we stand.** 2–4 sentences: our view from the memory doc (as-of date, our close date and its basis, the gating item, the risk rating), plus the date and gist of the last post on the chain. If there is no doc, say "No memory doc on file."
- **Key open items / questions.** Open questions from the memory doc (OQ-n) that these notes touch. Mark any the notes answered as resolved; never delete one silently. If none apply: `<p style="margin:0 0 12px">None touched by these notes.</p>`
- **Thesis &amp; material update.** First `<p>`: our standing view. Second `<p>`: whether the notes confirm, advance or contradict it, using the NEW / CONFIRMS / CONTRADICTS classification from Step 6.
- **Source — broker text, verbatim.** Replaces the rail's "Market &amp; web context" block, because the scan runs no web pass. For each source, write a `<p style="margin:0 0 4px;font-size:10.5px;color:#94a3b8">` with the header line `{Broker} ({analysts}) · "{original subject}" · {sent ET} · fwd by {forwarder}`. Below it, put the verbatim broker section in a `<p style="margin:0 0 12px">`, HTML-escaped with `html.escape`. Turn line breaks into `<br>`, and keep list items as `<ul style="margin:0 0 12px;padding-left:18px">`/`<li style="margin:0 0 3px">` when the source has lists. Do not change any broker words.
- **Snapshot table.** Put it last inside the rail, where the template's "SNAPSHOT TABLE GOES HERE" comment sits, the same as on a SPAC note (section 3).

### 3. Snapshot table: merger-arb version

Copy `snapshot-table.html`'s wrapper, `Snapshot (as of {HH:MM ET}, {session})` heading, `<table>` attributes, and its group-row, label-cell and value-cell styles exactly. Keep the instrument-first grouping, with COMMON first and DEAL last. The SPAC-only rows (vs trust, CIT, Yield to trust, Float) and the WARRANTS, RIGHTS and UNITS blocks are dropped. Exception: if the deal has a CVR or another listed instrument, add it as its own block between the COMMON blocks and DEAL.

| Block (group row) | Label rows → content |
|---|---|
| `<b>COMMON ({TARGET}) — target</b>` | **Price:** `{mid} mid (bid {bid} / ask {ask}); last {last}` from get-price. **Position:** blotter rows for the target (side, qty, filled/working, limit or MKT, TIF), or `No working orders on the blotter`. |
| `<b>COMMON ({ACQUIRER}) — acquirer</b>` | Only when the acquirer is listed. Same Price and Position rows. If it is private, collapse to the single group row `<b>COMMON</b> — acquirer private ({name})`. |
| `<b>DEAL</b>` | **Terms:** consideration per share (cash / exchange ratio / mixed), per the memory doc or merger-arb-list. **Spread:** deal value {x} · gross {$} ({%}) · **{annualized %} to {close date}** (name the date used); for stock legs, use the acquirer mid. **Progress:** where each approval stands (HSR / second request, foreign antitrust and FDI, CFIUS, state or sector regulators, shareholder vote, financing, litigation). **Key dates:** in order: filings/approvals → vote → expected close → outside date. **Bold** any date that is a trigger or condition (outside date, termination right, ticking fee start), and say so if it has passed. **Stage:** `{stage, e.g. Announced / HSR filed / Second request / Vote passed / Pending close} · our close {date} ({basis}) · risk {rating} · per {memory doc name}`. |

Any input that's missing gets `n/a — {why}` (e.g. `n/a — Bloomberg cannot resolve this ticker`, `not retrieved this run`). Never leave a cell blank, and never invent a number. If the memory doc and merger-arb-list disagree on terms or close date, print both and name the conflict.

### 4. Footer, red and validation

- Footer: `Internal Meteora note — for internal discussion only; not investment advice. Sourced from {brokers}; EMSX blotter, {memory doc name}, Bloomberg.` Delete the EDGAR accession clause.
- Red (`<span style="color:#c0392b;font-weight:700">`) is only for a fact where a broker contradicts our view, or for a passed or imminent trigger date. Use at most two per post.
- Inline styles only, and only colours on the palette. Emit the new block only. Never touch the quoted chain.
- **Validate:** write the HTML to the scratchpad as `ma-{TICKER}.html` and run `python3 {validator path} ma-{TICKER}.html --mode enhanced`. Any ERROR means: fix it and re-validate once. If it still fails, do not send, write no ledger line, and log `format-fail: {TICKER} ({first error})`. The next run will retry it. WARN lines are fine.
- **Check the three things the validator can't see:** what's new (the takeaway and analysis) sits on top and is complete; the stamp is present; every recipient is internal (Step 7).

## Step 7: Post

meteora-email-format-v2 pre-authorizes merger-arb notes to send without a human confirm, so this step never waits for the user. The preview → `confirmed=True` sequence below is only the Email Assistant tool's own two-step.

1. Call `reply_all_email(message_id, body=<validated HTML>, html=True)` without `confirmed` to preview it. Read the recipient list in the preview:
   - If any recipient is outside `internal_domain`, do not send. Log it.
   - If the list is empty, or contains only the signed-in user (a self-loop on a chain where the signed-in user sent the newest message), preview again against the newest message on the chain that someone else sent, found with `read_thread`. If no message on the chain gives real recipients, skip the ticker and log `no recipients: {TICKER}`.
2. Call it again with identical arguments plus `confirmed=True`. The preview store holds only the most recent preview, so go preview → confirm one post at a time, never in a batch.
3. Write the ledger lines right away (Step 5). Use status `posted`; the ledger format is unchanged.
4. **Verify delivery.** Find the sent item with `search_emails(folder="SentItems", subject=<chain subject>, max_results=5)`. Read the newest one with `read_email` and check that it is from `sender` (lukas@meteoracapital.com) and that its recipients match the preview. A `sent` status alone does not prove delivery. If the recipients come up short, log `delivery-check FAILED: {TICKER}` so a person can resend. Do not auto-resend, because the ledger already says posted.

## Step 8: Memory-doc upkeep (after every post)

Runs for every ticker that got a post this run, from Step 7 (broker note) or Step 9 (blotter or transcript recap). It never runs for `no-news`, `dup` or `no chain` tickers. It runs AFTER the post is sent and its ledger line written, so a slow or failed memory run can never block or undo a post.

1. **Find the doc.** Grep the saved `list-memory-docs` result for `{TARGET}`, `{TARGET}-{ACQUIRER}` and `{TARGET} - {ACQUIRER}` (case-insensitive). Ignore `COVENANT-*`, `*DEDUPE`, `MASCAN*` and SPAC docs.
2. **Doc exists → update it.** Load `update-merger-arb-memory-doc-v3-10202026` with the Skill tool and run it on that doc with args:
   `{doc name}: run completely and write it. Unattended scheduled run from merger-arb-email-scan; no one is watching, so this trigger is the confirmation. New information: the post just sent on "{chain subject}" ({broker-note scan | blotter recap | transcript recap}, {date}) and the sources quoted in it. Read the chain with read_thread for anything posted since the doc's last update and fold it in.`
   That skill's Core Principle 10 accepts a "run completely / write it" trigger as confirmation, so it writes without stopping. Still print its digest and Change Note in this run's output so the write can be audited.
3. **No doc → seed one.** Load `merger-arb-memory-doc-v1` and run it in Seed Mode. The material is the whole Internal chain (`save_thread_markdown`, or `read_thread` if that's unavailable) plus the sources in the post just sent. Name the doc by that skill's rule (`{Target}`, or `{Target} - {Acquirer}` when the consideration includes public acquirer stock).
   - **Hour-1 dependency.** v1 requires a current Hour-1 module run. If an `hour-1*` skill is installed, let v1 run it as it says. If none is installed, Lukas's instruction (2026-11-10) overrides v1's no-fallback rule for these runs only: seed from the chain as the reconciliation source, and state in the doc's provenance line `Seeded from the Internal {TICKER} chain by merger-arb-email-scan; no Hour-1 run (module not installed)`. Never invent what an Hour-1 run would have said.
4. **One memory run per ticker per run.** If a ticker got more than one post in the same run (a broker-note post and a recap, or two recaps), do one combined update after both posts.
5. **Cap and queue.** Do at most 4 memory runs per scheduled run (they are long: research, email sweep, verification). Write every further ticker to MASCANEOD as `MEM-PENDING | {date} | {TICKER} | {doc name or "seed"} | {chain subject}`. At the start of Step 8 on each run, clear pending items first (oldest first, inside the same cap of 4) before new ones.
6. **Record it.** After each memory run, add `MEM | {YYYY-MM-DD HH:MM ET} | {TICKER} | {doc name} | seeded|updated|failed: {reason}` to MASCANEOD, and remove that ticker's `MEM-PENDING` line if there was one.
7. **Never send email from a memory run.** The memory skills may read mail (their email sweep) but this skill's posts are the only email that goes out. If either memory skill asks to send or reply to anything, don't.

## Step 9: Blotter and transcript recaps (check on EVERY run; most important step)

Through the day, an internal sender (usually walter@meteoracapital.com) emails Filings@ two kinds of Cowork-generated notes:
- **Daily Blotter Note — {MM.DD.YYYY}**: fills over 5,000 shares, by name, with price, last, position and yields. **There can be several in one day**: a `(Midday)` note, the end-of-day note, and sometimes a re-send or correction. Each one is a separate source.
- **Internal Transcript**: the summary of the all-hands Zoom call, sent on a reused subject like "RE: Internal Transcript: 9/17 PM", so identify it from the body heading, not the subject. The PM version ("Meteora End-of-Day Summary — {date}" / "Internal Transcript: {M/D} PM") usually lands around 7 PM ET; a morning version ("Meteora Morning Summary — {date}" / "Internal Transcript: {M/D} AM") can also arrive. Each one is a separate note. Skip anything marked `*TEST*`.

**The trigger is the note itself.** A recap goes out only after a blotter note or transcript has actually been sent to Filings@, and only from what that note says. Nothing is posted on a schedule, ahead of a note, or in anticipation of one. Every note is handled on its own, the first time a run sees it:
- each blotter note → a **blotter recap** per deal (what we traded);
- the transcript → a **transcript recap** per deal (what the desk said).

Blotter notes never wait for the transcript, the transcript never waits for a blotter note, and a later blotter note never waits for an earlier one. If three blotter notes and a transcript arrive in a day, that is up to four separate recaps per deal, each posted when its note is first seen, and each saying what changed since the previous post on that chain.

### 9.1 Detect (every run, even with no broker notes)

1. Read MASCANEOD once (`read-memory-doc("MASCANEOD", summary_only=true)`; create it with the seed summary below if `not_found`).
2. Search with `list-emails(search=..., top=10)` using unquoted or body-phrase queries; a quoted `subject:"..."` restriction does not work reliably (tested 11/10: it returned unrelated "INTERNAL" chains). Use:
   - blotter: `"Daily Blotter Note"`
   - transcript: `"End-of-Day Summary"` and `"Morning Summary"`
   Then keep only messages to Filings@ from internal senders whose subject contains `Daily Blotter Note` or `Internal Transcript` and is not marked `*TEST*`. If the list tool fails, fall back to the Email Assistant `search_emails(subject="Daily Blotter Note")` / `search_emails(subject="Internal Transcript")` with `after` = yesterday, and read the bodies with MeteoraMCP `read-email`.
3. Keep every note received since 19:30 ET on the previous business day. That covers today's notes plus any that landed after last night's final run.
4. Compute each kept note's fingerprint with the Step 5 function (Filings@ subject, sender, `receivedDateTime`). A note is **new** if MASCANEOD has no `NOTE | {fingerprint} |` line. Skip notes that are not new.
5. Identify each new note's trading day D (blotter: the date in the subject or body heading; transcript: the body heading date) and its type (`blotter-midday`, `blotter` or `transcript`). Process new notes oldest first, so each "what changed" comparison runs in time order.
6. If there are no new notes, log `notes: none new` and go to Step 10.

### 9.2 Read and extract (per note)

1. `read-email` the note (full HTML; never the Email Assistant's truncating `read_email`). The result is usually too big for the context (the 11/9 transcript was 1.17M characters because it quotes every earlier transcript on the reused chain), so let it save to a file and work on the file with python: parse to text as in Step 2, then **cut at the first quoted header** (a line `From: ...` followed by `Sent: ...`). Only the text above it is this note. Keep the HTML too; a blotter note's per-name blocks split cleanly on its bold name headers (e.g. "AACI {AACI US Equity} — Bought 125,000 @ $10.11").
2. Build the **merger-arb universe** once per run: every target and acquirer ticker in `merger-arb-list`, plus any ticker with a `posted` line in MASCANDEDUPE in the last 30 days. Map each acquirer to its target. SPAC names (trust value, yield to deadline, pre-deal common) are out of scope, even when they trade.
3. For each name in the universe, collect from this note only:
   - **Blotter note:** the name's block(s): side, quantity, price, last, and position as the note states it. The note lists only fills over 5,000 shares, so also call `emsx-blotter(tickers=[universe], order_status="FILLED")` once per run and keep D's fills for these names up to the note's time stamp. Call `emsx-blotter(tickers=[universe])` once for working orders.
   - **Transcript:** every bullet or line that mentions the ticker, the target or acquirer company name (e.g. Brighthouse → BHF, Western Union → IMXI), or an alias from the memory doc. Keep speakers and time stamps exactly as written. Look in every part: the ticker sections (Part 1), calendar rows (Part 0.5), items to confirm (Part 5) and open action items (Part 7, keep the owner). Merger-arb names are often bundled into one bullet (e.g. "OPCH / GFL / CTFN / DV / BHF / IMXI ... — MERGER ARB & CREDIT", then "OPCH: ... GFL: ... DV: ..."); split those at each `TICKER:` and file each piece under its own ticker. Ignore the transcript's own blotter table (Part 2) and fill-only lines with "no further commentary": fills are reported by the blotter recap, so they never make a name in play for a transcript recap.
4. A name is **in play** for this note if:
   - blotter note: it has at least one fill in the note (or in EMSX for D that its chain has not been told about yet);
   - transcript: the transcript has substance on it (a fact, view, number, decision or action item). A name that only appears in a list is `mention-only`; log it and move on.

### 9.3 Read the chain, compare, then write (per note, per in-play name)

1. Find the chain (Step 4). No chain: log `notes no chain: {TICKER}`. Never create one.
2. Dedup: skip if MASCANEOD has `RECAP | {note fingerprint} | {TICKER} |`.
3. **Read the Internal chain every time, right before writing.** Use `read_thread` on the newest message, or `save_thread_markdown` if the thread is long. Find the most recent post on the chain of any kind: an earlier blotter recap today, a transcript recap, a broker-note scan, or a person's reply. Note what it said about fills, position, close date, view and open questions.
4. Gather Step 6 items 1-3 (book, our view from the memory doc, tape). Then compare this note against both the chain and the memory doc:
   - **Changed since the last post.** Say exactly what changed and since when. For example: "Since the Midday blotter recap (12:47 PM): bought another 25,000 at 13.56; position 40,000 → 65,000 (per Daily Blotter Note)"; "Desk now sees close by 11/20, vs 11/27 in this morning's scan post"; "Walter's 2:10 PM reply flagged a working 10k sell; it is now filled". If nothing changed for this name since the last post (for example, the end-of-day blotter repeats the Midday fills exactly), do not post. Log `no change: {TICKER} ({note type})` and write the RECAP line with status `no-change`.
   - **Against the memory doc.** Compare trades with the doc's Position section: added, trimmed, opened or closed, and by how much. Compare the discussion with the doc's view and open questions (NEW / CONFIRMS / CONTRADICTS, and MATERIAL vs NOISE per Step 6.4). If the blotter note gives a position, quote it and name the source ("per the Daily Blotter Note"). Never state a position size that no source shows.
5. Draft with the same tone and limits as Step 6 (under ~250 words above the Source block). Blotter recap:

```
Shivom testing                                   <- only on test_prefix_dates
{TICKER}/{ACQ}: {one-line takeaway, e.g. "Added 25k at 13.56 since midday; position now 65k"}

WHAT WE DID ({Midday | End-of-day} blotter, {D})
- Fills: {side qty @ avg px, per the Daily Blotter Note / EMSX}
- Working: {orders still on, or "No working orders on the blotter"}
- Position: {per the Daily Blotter Note; or "not stated in this note"}

WHAT CHANGED
- Since the last post ({who/what, time}): {exact change; for the first post on the chain today, "first update today"}
- Vs the memory doc: {change vs the Position section on file}

WHAT IT MEANS
- {effect on the trade's return, view, timing or OQ-n, as an observation only}
- Watch: {next dated catalyst}

SOURCE
Daily Blotter Note — {D}{ (Midday)} | {sender} | {sent ET}
{verbatim block(s) for this name}
```

   A transcript recap has the same shape, with three differences: `WHAT THE DESK SAID` ({Speaker, time}: plain-language paraphrase) replaces `WHAT WE DID`; `WHAT CHANGED` compares the desk's view with the last post and the memory doc; and the Source header is `Internal Transcript ({M/D} PM) | {sender} | {sent ET}`, above the verbatim lines.

6. **Render** per Step 6b, with these changes:
   - Subline: `{Midday blotter | End-of-day blotter | Desk call} recap · {D}`.
   - Body sections as drafted above, with `What changed` as its own section right after the first one.
   - The rail's Source block is titled `Source — {blotter | transcript} excerpt, verbatim`.
   - Footer: `Sourced from the {Daily Blotter Note | Internal Transcript} for {D}; EMSX blotter, {memory doc name}, Bloomberg.`

   Validate the same way.
7. **Post** per Step 7, except that the ledger line goes to MASCANEOD: `RECAP | {note fingerprint} | {TICKER} | {chain subject} | {YYYY-MM-DD HH:MM ET} | posted`. Then run Step 8 for the ticker, passing the note's fills or transcript lines and the "what changed" bullets as the new information.
8. **Close out the note.** When every in-play name for the note is posted, unchanged, or logged (`no chain`, `format-fail`, `no recipients`), write `NOTE | {fingerprint} | {D} | {blotter-midday|blotter|transcript} | {YYYY-MM-DD HH:MM ET} | posted {n}`.
   - If a run dies midway, the per-ticker RECAP lines stop re-posts and the next run finishes the rest.
   - A re-sent or corrected note has a new fingerprint and is processed like any other. Its WHAT CHANGED section says what differs from the earlier note.

MASCANEOD seed summary:

```
Ledger for merger-arb-email-scan blotter/transcript recaps and memory-doc runs. NOT a research doc.
NOTE | <note fingerprint> | <trading day YYYY-MM-DD> | <blotter-midday|blotter|transcript> | <YYYY-MM-DD HH:MM ET> | posted <n>
RECAP | <note fingerprint> | <TICKER> | <chain subject> | <YYYY-MM-DD HH:MM ET> | <posted|no-change>
MEM | <YYYY-MM-DD HH:MM ET> | <TICKER> | <doc name> | <seeded|updated|failed: reason>
MEM-PENDING | <YYYY-MM-DD> | <TICKER> | <doc name or seed> | <chain subject>
Prune lines older than 30 days on the first run of each ET day (never prune MEM-PENDING).

### LOG
```

Write lines with `patch-memory-summary`, replacing `### LOG` with `### LOG\n{new line}`, right after each event. Never batch them.

## Step 10: Log

End with one compact line set, not emailed anywhere:

```
MA-SCAN {YYYY-MM-DD HH:MM ET}: sources {n}
posted: OPCH -> "Re: Internal OPCH Option Care" (RJF), ROKU -> "INTERNAL ROKU INTERNAL FOXA" (ELEV, UBS, OG), ...
no-news: DV (restates 11/9 Q4 guidance; tone only), ...
skipped (no chain): ...
skipped (dup): ...
format-fail / delivery-check FAILED / no recipients / sender mismatch / attachment-only: ...   (omit if none)
dropped: "{subject}" ({reason}), ...
notes: {type} {D} {HH:MM} -> posted: DV, LNTH ... | no change: ... | mention-only: ... | no chain: ...   (one line per new note; or "none new")
memory docs: updated DV; seeded IMXI; pending: ...; failed: ...
ledger: ok | FAILED read (thread check only)
format: meteora-email-format-v2 enhanced (SPAC-style) | unavailable
```

## Rules

- Run only inside `run_window` (06:30-19:30 ET, weekdays).
- Check for blotter notes and the transcript on every run (Step 9), whether or not there are broker notes. Each note is handled separately, the first time it is seen; a recap goes out only after its note has been sent to Filings@.
- Read the Internal chain right before every post (scan or recap) and say what changed since the last post on it.
- Check the memory doc before every post, and post only MATERIAL news (Step 6.4).
- Never create new chains, and never send a new message to Filings@. End-of-day recaps go on existing Internal chains only.
- Never reply on a chain with an external recipient.
- Never edit broker, blotter or transcript text in the SOURCE block; never invent positions, terms, or prices.
- Memory-doc runs (Step 8) write memory docs only; they never send email.
- No visible dedup tags in posts; the ledger is the record.
- Every post is meteora-email-format-v2 HTML in the SPAC-style enhanced layout (shell → rail → Snapshot) that passed `validate_html.py --mode enhanced`. Never fall back to plain text.
- Never change the fingerprint or ledger format without changing the ma-scan script the same way.
- If a tool errors, retry once, then skip that item and log it. If the blotter, memory doc, or price call fails, still post with that line marked "unavailable".
