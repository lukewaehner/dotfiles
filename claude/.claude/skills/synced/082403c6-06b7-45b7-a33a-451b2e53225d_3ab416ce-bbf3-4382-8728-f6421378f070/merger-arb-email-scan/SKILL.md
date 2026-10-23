---
name: "merger-arb-email-scan"
description: "Scan Filings@ for forwarded broker merger-arb notes (UBS, TD, Jefferies, RJF, Oscar Gruss, Elevation, CTFN, any broker), check where we stand on each deal (EMSX blotter, deal memory doc, live spread), and post a short desk analysis of what the new note actually says and means as a reply-all on that ticker's existing Internal chain, rendered in the meteora-email-format-v2 house HTML format. Use for 'run the merger arb email scan' and its recurring runs."
---

# Merger Arb Email Scan

Finds merger-arb broker notes forwarded to Filings@meteoracapital.com, splits each note by deal, and for every deal with an EXISTING "Internal {TICKER}" chain posts ONE analytical update per run: where we stand (book, our view, tape), what the new note says, and what it changes. The broker text goes at the bottom as the source, not as the post. It never creates a new chain. Built to run unattended, so a run that finds nothing must end in a few tool calls.

No visible tags in posts. Dedup lives in the MASCANDEDUPE memory doc (Step 5).

Every post is sent as HTML in the **meteora-email-format-v2** house format, using the same layout as its SPAC notes: body, then background rail with the Snapshot table (Step 6b). This skill adopts that format on purpose, as the user's standing instruction, so the "invoked explicitly" rule in meteora-email-format-v2 is satisfied by this skill. Plain-text posts are no longer allowed.

A local Python job (`ma-scan`, launchd every 5 minutes on Lukas's Mac) used to post UBS notes verbatim with a visible `[MA-SCAN ...]` tag. That job must either be paused or changed to read and write the MASCANDEDUPE ledger with the same fingerprint, or it will double-post next to this skill. Until then, Step 5 also treats a legacy tag in the thread as "already posted".

## Config

| Key | Value |
|---|---|
| `lookback_minutes` | 65 for the hourly run; 20 if looping every 5 min |
| `filings_address` | Filings@meteoracapital.com |
| `internal_domain` | meteoracapital.com |
| `ledger_doc` | MASCANDEDUPE (memory doc) |
| `test_prefix` | "Shivom testing" |
| `test_prefix_dates` | 2026-10-07 (America/New_York). On these dates line 1 of every post is the test prefix; on other dates it is omitted. |

## Tools

- **Detection and reading:** MeteoraMCP-AWS `list-emails` and `read-email`. They return exact `receivedDateTime` and the full HTML body. Do not use the Email Assistant's `read_email` for source text (it truncates).
- **Where we stand:**
  - `emsx-blotter(tickers=[...])` (MeteoraMCP): live working orders for the target and acquirer. Call it once per run with every deal ticker. For today's executions, also call with `order_status="FILLED"`. The blotter shows orders, not positions; never state a position size it does not show.
  - `list-memory-docs` (once per run; the result is large, so save it and grep for names) and `read-memory-doc(name, entries_limit=3)` (MeteoraMCP-AWS). Deal docs are named `{TARGET}` or `{TARGET}-{ACQUIRER}` (e.g. OPCH, ROKU-FOXA, SYNA-ON). Ignore `COVENANT-*`, `*DEDUPE`, SPAC theme docs.
  - `merger-arb-list` (MeteoraMCP-AWS): deal terms (cash, exchange ratio, expected close) for the spread.
  - `get-price(tickers=[target, acquirer])` (MeteoraMCP): live bid/ask/mid. Quote mid and say which session.
- **Format:** the `meteora-email-format-v2` skill. Load it with the Skill tool once per run, before the first post (skip this on a run with nothing to post). Its files are `references/shell.html` (the template) and `scripts/validate_html.py` (the pre-send gate). Find them with `find / -path '*meteora-email-format-v2/references/shell.html' 2>/dev/null | head -1`. If the skill or either file can't be found, post nothing this run, write no ledger lines, and log `format unavailable`. The next run retries.
- **Posting:** Email Assistant (Microsoft 365) on the user's computer: `whoami`, `search_emails`, `read_thread`, `read_email`, `reply_all_email` (with `html=True`). Posts go out as whoever is signed in. Never send through MeteoraMCP `send-email` or any other sender.
- **Step 0:** Email Assistant `whoami()`. The signed-in user must be on `internal_domain`. If not signed in, stop and report.

## Step 1: Detect

1. `list-emails(search="recipients:filings@meteoracapital.com", top=50)`. Keep messages whose `receivedDateTime` is within `lookback_minutes`. If the oldest kept message is still inside the window, page further; if the cursor errors, run a second search `recipients:filings@meteoracapital.com AND subject:FW` to cover the gap. If none, print `MA-SCAN {time ET}: nothing new` and end.
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
4. **What is new:** compare each source against the memory doc (summary + last entries) and the last few posts on the chain. Classify each fact as NEW, CONFIRMS (already known), or CONTRADICTS our view.

If every fact for the ticker is CONFIRMS with no new number, date, or view (e.g. "meeting is today" when the doc already has the date), do not post. Log `no-news` in the ledger and in the run log.

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
4. **Verify delivery.** Find the sent item with `search_emails(folder="SentItems", subject=<chain subject>, max_results=5)`. Read the newest one with `read_email` and check that its recipients match the preview. A `sent` status alone does not prove delivery. If the recipients come up short, log `delivery-check FAILED: {TICKER}` so a person can resend. Do not auto-resend, because the ledger already says posted.

## Step 8: Log

End with one compact line set, not emailed anywhere:

```
MA-SCAN {YYYY-MM-DD HH:MM ET}: sources {n}
posted: OPCH -> "Re: Internal OPCH Option Care" (RJF), ROKU -> "INTERNAL ROKU INTERNAL FOXA" (ELEV, UBS, OG), ...
no-news: ...
skipped (no chain): ...
skipped (dup): ...
format-fail / delivery-check FAILED / no recipients: ...   (omit if none)
dropped: "{subject}" ({reason}), ...
ledger: ok | FAILED read (thread check only)
format: meteora-email-format-v2 enhanced (SPAC-style) | unavailable
```

## Rules

- Never create new chains, and never send a new message to Filings@.
- Never reply on a chain with an external recipient.
- Never edit broker text in the SOURCE block; never invent positions, terms, or prices.
- No visible dedup tags in posts; the ledger is the record.
- Every post is meteora-email-format-v2 HTML in the SPAC-style enhanced layout (shell → rail → Snapshot) that passed `validate_html.py --mode enhanced`. Never fall back to plain text.
- Never change the fingerprint or ledger format without changing the ma-scan script the same way.
- If a tool errors, retry once, then skip that item and log it. If the blotter, memory doc, or price call fails, still post with that line marked "unavailable".
