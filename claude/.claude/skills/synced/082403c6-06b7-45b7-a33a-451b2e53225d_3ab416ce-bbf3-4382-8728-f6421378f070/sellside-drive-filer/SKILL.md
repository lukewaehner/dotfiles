---
name: sellside-drive-filer
description: Two-phase daily sell-side research FILER. Phase A (5:00 PM) asks the signed-in user for today's tickers of interest; Phase B (5:30 PM) sweeps the last 24h of sell-side research in Outlook (Email Assistant / Microsoft 365), isolates the notes for those tickers, finds each ticker's folder in Google Drive (creating it if missing), and uploads the research VERBATIM — PDF attachments byte-for-byte, body-only desk notes as the whole email (.eml). Unlike the sell-side digest, it does NOT summarize or route email — it just files the raw research into the right ticker folder. Trigger on "run the sell-side filer", "file the research to Drive", "upload broker notes to Drive", "archive research to the ticker folders", "drop today's research into Drive", or the 5:00/5:30 PM scheduled runs. Always use this skill for filing sell-side research into per-ticker Drive folders — never upload broker research to Drive ad hoc.
---

# Sell-Side Drive Filer (5:00 PM ticker ask + 5:30 PM verbatim filer)

Files sell-side research into a Google Drive organized as one folder per ticker. The daily workflow runs in two phases, as two scheduled tasks (see Scheduling):

- **Phase A — 5:00 PM ticker ask.** Email `ask_recipient` (the signed-in user who owns the scheduled runs) asking which tickers matter today. They reply with tickers.
- **Phase B — 5:30 PM filer.** The sweep-and-file run below. When Phase A got a reply, only the listed tickers are filed; **no reply means every note with an attributable ticker is filed**, so the ask can never cost you a day's research.

Phase B does four things:

1. **Sweep** the signed-in user's inbox for sell-side research received in the last 24 hours.
2. **Attribute** each note to its primary ticker(s) and keep only the notes for the tickers of interest.
3. **Locate** the Drive folder named after that ticker (create it when missing).
4. **Upload verbatim** — every research PDF byte-for-byte, and body-only desk notes as the whole email — into that folder, skipping anything already there.

The whole point is faithful capture: the file that lands in Drive is the *original research*, not a summary of it. A trader opening the `WBD` folder next quarter sees the actual broker PDFs, unaltered. (If you want the analytical summary posted onto the internal email thread instead, that is the separate `sellside-digest` skill — this one only files raw research to Drive.)

Designed to run unattended on a daily schedule, and to be portable: everything binds to the *signed-in user's* mailbox and domain, so the same .skill file works on anyone's Claude once they connect their Microsoft and Google Drive accounts.

---

## Config

Edit these lines to retarget the skill. The invoking prompt can override `test_mode` (see Modes).

| Key | Default | Meaning |
|---|---|---|
| `drive_root_folder_id` | `0AKNhCG89u7IcUk9PVA` | The Shared Drive ("Drive") root that holds the per-ticker folders (`BMNR`, `DUK`, `CLVT`, `SO`, `Crinetics Pharma (CRNX)`, `ATAI (AtaiBeckley)`, …). Folder searches are scoped to it so `CRNX` matches the CRNX ticker folder and not an unrelated folder elsewhere. This is a **Shared Drive root** (id starts `0A…`); the connector writes into it via `parentId` like any folder. Change it only if the ticker folders are relocated. It also holds non-ticker folders (`Sell Side Research`, `Sellside Digest`, `Initiation of Coverage Notes`, etc.) — the ticker-name match in Step 3 ignores those. |
| `internal_domain` | `auto` | Domain that counts as "internal". `auto` = the domain of the signed-in user's own address (from `whoami()` / `get_me`). Only used to gate the Phase A ask recipient; this skill never emails research anywhere. |
| `lookback_hours` | `24` | Sweep window, measured back from run time. |
| `test_mode` | `true` | `true` = no Drive writes at all (no file uploads, no folder creation) — the run reports exactly what it *would* upload and where. Phase A drafts the ask to SELF with a `[TEST]` prefix. Flip to `false` after one verified dry run (or say "live" in the prompt). |
| `create_missing_folders` | `true` | When a ticker of interest has no folder under `drive_root_folder_id`, create one named exactly after the ticker and file into it. `false` = skip that ticker and flag it in the run report instead (strict mode — Drive structure stays exactly as you built it). |
| `body_note_format` | `eml` | How to file a body-only desk note (no PDF attachment) verbatim. `eml` = upload the original message as a `.eml` file (byte-faithful, the true verbatim capture). `pdf` = render the email body to a PDF before upload (more previewable in Drive, but a rendered copy, not byte-verbatim). |
| `fetch_linked_pdfs` | `true` | When a note's substance is behind a portal link that resolves directly to a downloadable PDF the signed-in session can reach, download that PDF and file it verbatim alongside the email. Gated/login/paywall links are ignored — the `.eml` capture still preserves the link. Never authenticate or bypass a wall. |
| `ignore_senders` | (empty) | Addresses/domains never treated as research (e.g. newsletter feeds). |
| `extra_research_senders` | (empty) | Addresses/domains always treated as research candidates even if they don't look like a bank. |
| `flag_unrouted` | `true` | Put the Outlook follow-up flag on research the run couldn't file (no attributable ticker, or — in strict mode — a ticker of interest with no folder), so it doesn't vanish into the chat transcript. |
| `research_folder` | (empty) | Exchange folder that server-side rules move broker research into (see One-time setup). When set, the sweep searches this folder **and** the inbox. Empty = inbox-only sweep. |
| `filename_prefix` | (empty) | Optional string prepended to every uploaded filename (e.g. `Broker - `). Empty = upload under the original filename, unchanged. Use only if you want a house naming convention; it trades a little "verbatim" for consistency. |
| `ask_tickers` | `true` | Two-phase mode: 5:00 PM ask (Phase A) + 5:30 PM scoped run (Phase B, Step 0). `false` = no ask, every run files all attributable tickers (legacy single-run behavior). |
| `ask_recipient` | `SELF` | Who receives the 5:00 PM ask and whose reply scopes the run — the signed-in user who set up the scheduled tasks. Set an explicit address to override; it must be on `internal_domain`. |
| `ask_subject` | `Tickers of interest — sell-side digest {YYYY-MM-DD}` | Subject template for the ask email. Kept identical to the `sellside-digest` skill on purpose (see `share_digest_ask`). Phase B locates today's ask thread by this subject plus the `[SELLSIDE-TICKERS` body marker. |
| `share_digest_ask` | `true` | Reuse the `sellside-digest` skill's 5:00 PM ask thread instead of sending a second one. When `true`, Phase A first looks for today's existing ask (same subject + `[SELLSIDE-TICKERS {date}]` marker); if it already exists, it does NOT send another — so you reply once and both the digest and this filer scope to the same tickers. Only sends its own ask when none exists yet. |

---

## Modes

- **TEST (default):** never pass `confirmed=True` to any send or flag tool, and **make no Google Drive writes** — no `create_file` for uploads, no folder creation. Instead, resolve every folder id (read-only `search_files` is fine) and report, per ticker, exactly which files *would* be uploaded, to which folder id (or "would create folder {TICKER}"). Phase A drafts the ask only (to SELF, `[TEST]` subject prefix), which means a TEST Phase B normally finds no reply and correctly exercises the file-everything fallback. Local temp downloads of PDFs/.eml still happen — that is disk, not a Drive or mailbox write — so the report can show real filenames and sizes.
- **LIVE:** actually upload. Activated when `test_mode` is set to `false` in this file, **or** when the invoking prompt contains the word "live" (e.g. a scheduled task prompt of `Run the sell-side filer (live)`). This lets the owner go live without re-packaging the skill.

Reads are always allowed in both modes — searching for folders and reading email never needs `confirmed` and is never gated. The gate is only on writes (Drive uploads, folder creation, the Phase A send, and flagging).

---

## Scheduling — two weekday tasks (ET)

- **5:00 PM** — prompt `Run the sell-side filer ticker ask (live)` → Phase A only (send the ask, stop). **Skip scheduling this entirely if you also run `sellside-digest`** — with `share_digest_ask: true` the filer reuses the digest's 5:00 PM ask, so scheduling a second ask would just send a duplicate. Let the digest own the ask.
- **5:30 PM** — prompt `Run the sell-side filer (live)` → Phase B (Step 0 onward). Schedule this a few minutes after the digest's own 5:30 PM run so both read the same reply.

"live" in the prompt flips LIVE mode per Modes. An ad-hoc "run the sell-side filer" works at any time: if no ask thread exists for today, Step 0 simply falls back to filing all attributable tickers. When `ask_tickers` is `false`, schedule only the filer task.

---

## Tooling

Mailbox operations go through the **Email Assistant (Microsoft 365) extension** when present. Core set: `whoami`, `search_emails`, `read_email`, `read_thread`, `list_attachments`, `download_attachments`. Enhancements: `download_email_as_eml` (needed for `body_note_format: eml` — this is how a body-only note is captured verbatim), `flag_email` (follow-up flags), plus `draft_email` / `send_email` for the Phase A ask only. Load them via ToolSearch with query `Email Assistant` (or `outlook`).

- If the Email Assistant extension is absent, fall back to equivalent tools on the **Microsoft 365 connector** (ToolSearch `outlook email search`, `download attachments`, etc.). The sweep and attachment download are identical; only tool names change. If `download_email_as_eml` has no connector equivalent, degrade `body_note_format` to `pdf` (render the fetched body) or, failing that, upload the extracted body text as a `.txt` — and say in the run report that the `.eml` capture was unavailable. If neither surface exposes email read for the signed-in user, stop and tell the user which connector to enable — do not improvise.
- **Never send research through any MCP's send-email.** This skill files to Drive; it must not email research anywhere. The only email it ever sends is the Phase A ask, as the signed-in user, to an internal recipient.
- First step of every run: `whoami()` (or `get_me`). If not signed in, stop and print the sign-in instruction. Record the user's address — it defines SELF and (when `internal_domain: auto`) the internal domain.
- On a fresh chat the extension may still be registering: if one ToolSearch returns nothing, say the connector is warming up and ask the user to resend — do not declare it broken.

Google Drive operations use the **Google Drive connector** — load via ToolSearch `google drive`. The tools this skill uses:

- `search_files` — find the ticker folder and dedup-check existing files. Structured query syntax: `title = 'WBD' and mimeType = 'application/vnd.google-apps.folder' and parentId = '{drive_root_folder_id}'`. String values are single-quoted.
- `create_file` — both folder creation and verbatim upload:
  - **Folder:** create it with the Google folder mime type and no content — `create_file(title="{TICKER}", parentId="{drive_root_folder_id}", contentMimeType="application/vnd.google-apps.folder")`. (The connector's bare `mimeType` field is deprecated; pass the folder type via `contentMimeType`. If a given connector build rejects that for a content-less create, retry with `mimeType="application/vnd.google-apps.folder"` — one of the two is what that build expects.) Use the returned folder id as the upload target.
  - **Verbatim PDF upload:** `create_file(title="{original filename}", parentId="{ticker_folder_id}", base64Content="{base64 of the raw bytes}", contentMimeType="application/pdf", disableConversionToGoogleType=true)`. `disableConversionToGoogleType=true` is **load-bearing** — without it Drive converts the PDF into a Google Doc and it is no longer the verbatim file. Always base64-encode the raw bytes into `base64Content` (never `textContent`) for any binary file (PDF, .eml, rendered PDF).
- `get_file_metadata` — only if you need to confirm a returned id.

If the Google Drive connector isn't connected, stop and tell the user to enable it — this skill's entire output is Drive uploads, so there is no graceful degradation for its absence (unlike the email enhancements). Say so plainly rather than filing nowhere.

Link-following (`fetch_linked_pdfs`) uses **`web_fetch`** for direct PDF links, and the **browser tools** (`navigate` + `get_page_text`, load via ToolSearch) only when needed to reach a PDF the signed-in session is already entitled to. These never authenticate or bypass a wall. If neither is available, skip link PDFs and note it — the `.eml`/PDF-attachment capture still stands.

File I/O note (Windows hosts): any temp text you write while handling notes must use `encoding='utf-8'` in Python `open()` calls — Windows defaults to cp1252 and silently corrupts non-ASCII. Binary reads for base64 (PDF, .eml) must open in `'rb'` mode.

---

## One-time setup — server-side pre-filtering (optional)

Not part of the daily run, and only relevant if the Email Assistant extension exposes rule tools (`list_message_rules` / `create_message_rule` / `delete_message_rule`). Trigger when the user says "set up the research rules". Create Exchange inbox rules that move known broker domains into `research_folder` **before** the 5:00 PM run, so the sweep starts from a pre-sorted folder. Preview each rule by calling `create_message_rule(...)` **without** `confirmed`, show the user the When/Then, then repeat with `confirmed=True`. Review existing rules with `list_message_rules()` first to avoid duplicates. Set rules up only interactively — never mid-run on a schedule, never in TEST mode. Rules are a pre-filter, not the classifier: the sweep still classifies by content and still covers the inbox for senders no rule knows about.

---

## Phase A — 5:00 PM ask for tickers of interest

Runs as its own scheduled task ~30 minutes before the filer. Skip entirely when `ask_tickers` is `false`.

1. `whoami()` — resolve SELF; stop if not signed in.
2. **Shared-ask check (when `share_digest_ask` is true).** Search Sent Items and Inbox for today's `ask_subject` / `[SELLSIDE-TICKERS {YYYY-MM-DD}]` marker. If the `sellside-digest` skill (or an earlier filer run) already sent today's ask, **do not send another** — report "ask already sent (shared with digest)" and stop. The reply to that one thread scopes both skills.
3. **Idempotence check:** even with `share_digest_ask` false, search Sent Items (and Drafts in TEST) for today's `ask_subject`. If today's ask already exists, don't send a second one — report "ask already sent" and stop.
4. Otherwise send a **fresh email** (not a reply) to `ask_recipient`:

```
Subject: Tickers of interest — sell-side digest {YYYY-MM-DD}

Reply to this email with today's tickers of interest, separated by spaces or commas
(e.g. "WBD LKSP NVDA"). The 5:30 PM runs will cover only those names.

- Reply "ALL" to file/cover every name.
- No reply by 5:30 PM = all names, as usual.

[SELLSIDE-TICKERS {YYYY-MM-DD}]
```

The marker line is load-bearing: Phase B locates today's ask thread by it, and the sweep uses it to keep the ask email and its replies out of the research classification. Never omit it. Send mechanics follow the house gate: preview without `confirmed`, verify the recipient is on `internal_domain`, then send with identical arguments and `confirmed=True`. (TEST mode: draft only, to SELF, `[TEST]` subject prefix.) Phase A sends exactly one email and does nothing else.

## Step 0 — Read the tickers of interest (Phase B, before anything else)

Skip when `ask_tickers` is `false`. Otherwise:

1. Find today's ask thread: `search_emails(subject="{ask_subject for today}")`, falling back to a body search for `[SELLSIDE-TICKERS {YYYY-MM-DD}]`. Only today's marker counts — yesterday's reply must not scope today's run.
2. `read_thread` and take the **latest human reply** (any message after the ask itself). Parse tickers: split on whitespace/commas/semicolons/newlines, uppercase, strip `$` and punctuation, keep 1–5 letter tokens that look like tickers, ignore filler words. Normalize SPAC class variants to the base common ticker (strip trailing U/W/R/WS) exactly as in Step 2 — a reply of "LKSPU" scopes to LKSP.
3. Outcome (state it in the run report either way):
   - **Tickers parsed → scoped run.** Only notes whose primary ticker(s), after normalization, intersect the list are filed. Everything else — research on other tickers AND no-ticker macro/sector pieces — is **disregarded**: not filed, not flagged, just an `Out of scope` tally in the run report. The Step 1 sweep still covers the entire window at full depth; scoping is applied at attribution (Step 2), never by narrowing the mailbox search — a keyword-narrowed sweep would misattribute forwards and multi-name notes.
   - **Reply is ALL** (or "all tickers" / "everything") → file every attributable ticker.
   - **No thread, no reply, or nothing parseable** → file all attributable tickers, exactly as if `ask_tickers` were off. An ambiguous reply ("the usual", "same as yesterday") is also a file-everything fallback — guessing a scope risks silently dropping research, and filing a few extra folders is cheap and reversible.

A reply that arrives after Phase B has started counts for nothing — the run uses whatever was in the thread when Step 0 executed; don't re-run automatically.

## Step 1 — Sweep the last 24 hours and capture the raw research

Compute `after = now − lookback_hours` as an ISO timestamp. Then:

```
search_emails(after=<ISO>, folder="inbox", max_results=<large>, sort_by="date", order="desc")
```

**No cap on how many emails the run parses — cover the *entire* window.** The invariant is completeness: every message received on/after `after` must be classified. `max_results` is a per-call **page size**, never a ceiling — pass a large value (e.g. 1000, the Graph page maximum) and treat a full-looking page as "there may be more," not "done." Keep fetching until the window is provably exhausted (a page is not the end while it came back full **or** its oldest message is still newer than `after`), using the pagination token when present, otherwise slicing by sender/sub-window. Union all pages and **dedup by message id** before classifying. If you cannot confirm the whole window was covered, say so explicitly in the run report with the count seen and the boundary reached — never quietly stop at a round number. If `research_folder` is set, run the same exhaustive sweep over it too, then classify across both folders.

**Counts as sell-side research (capture it):**
- **Published research** — PDF attachment(s) with rating / price target / estimates / analyst certification / disclosure pages. The email body may be a stub ("please see attached").
- **Desk commentary in the email body** — sales & trading / event-driven / merger-arb / SPAC desk notes: analytical text on a name, often headed "EVENT DRIVEN", "SALES & TRADING", "For Institutional Use Only", with probability trees, spread math, or catalyst timelines. These have no PDF — they are captured via `body_note_format`.
- **Internal forwards OF broker research** (`Fw:` chains where the underlying content is a broker note). Attribute to the original broker/analyst, not the forwarder. In scope if the forward landed inside the window.
- Sender heuristics: bank/broker domains (raymondjames.com, cantor.com, gs.com, jefferies.com, etc.), research distribution addresses, anything in `extra_research_senders`. But content decides — a broker email that is pure logistics is out; an analytical note from an unlisted boutique is in.

**Not research (skip, but list in the run report if borderline):**
- Corporate access / conference invites, roadshow logistics, call scheduling, marketing blasts with no analysis.
- Pure news clippings / press releases without broker analysis.
- Internal-origin analysis that isn't forwarding broker content (the team's own work, not sell-side).
- The skill's own ticker-ask emails and their replies (subject or body contains `[SELLSIDE-TICKERS`), and any `sellside-digest` output (body contains `[SELLSIDE-DIGEST`).
- Anything from `ignore_senders`.

**Collapse duplicate copies.** The same note routinely arrives 2–3 times (direct + team distribution + an internal forward + "confirming receipt" replies). Fingerprint each note as `(broker, note title with Fw:/Re: stripped, publication date)` and file it **once**, keeping the cleanest copy (prefer the original broker email; else the most complete forward). Filing the same PDF three times into one folder helps no one — and the Step 4 dedup guards against it across runs.

**Download the raw artifacts (this is what gets filed).** For each unique in-scope note:
- **PDF attachments →** `download_attachments` to a temp dir, keep the local paths and the **original filenames verbatim**. These are the primary artifacts; they upload byte-for-byte in Step 4.
- **Body-only note →** capture the whole email per `body_note_format`: `eml` uses `download_email_as_eml(message_id, output_dir=<temp>)`; `pdf` renders the email body (HTML→PDF) to a temp file. This is the only durable copy of a desk note that has no attachment, so never skip it.
- **Linked PDF (when `fetch_linked_pdfs`) →** if the note points at a portal "View PDF" / "Access this report" link that resolves directly to a downloadable PDF the signed-in session can reach, fetch it to the temp dir and treat it as another verbatim artifact for that note. A link that hits a login/paywall/consent/JS-shell yields nothing — drop it silently and rely on the `.eml`/attachment capture. Respect `web_fetch`'s content restrictions; a blocked fetch just counts as a discarded link, never an error that aborts the note.

Keep, per note: the local file path(s) of every artifact, the broker, the note title, the publication date, and the delivery form — Step 2 needs the ticker, Step 4 needs the files.

## Step 2 — Attribute to a ticker and scope

For every unique note, determine the **primary ticker(s)** — the name(s) whose investment case the note actually analyzes:

- The subject line is the strongest anchor (`RJF Event Driven: WBD - TGNA Part II ?` → WBD); the body confirms. Counterparties, acquirers, and comps mentioned in passing are *secondary* — they do not earn a folder. A note that materially analyzes two names as investable situations is filed under **both** folders (the same verbatim files go into each).
- Company named without a ticker → resolve the ticker; verify with a quick lookup if unsure rather than guessing (filing into the wrong folder is worse than flagging).
- No attributable single name (macro, sector, strategy pieces) → do not file (there is no ticker folder for it); list it under "no ticker" in the run report and flag it when `flag_unrouted` is on.
- **Ticker normalization:** treat SPAC class variants as their base common ticker (strip trailing U / W / R / WS when it's a unit/warrant/right of the same issuer) — a note on LKSPU files into the LKSP folder. This must match how the folders are named; if the Drive uses the as-published class ticker, keep it as-is and note the convention.

**Scoped runs (Step 0 produced a ticker list):** after attribution, drop every note whose primary ticker(s) don't intersect the list — not filed, not flagged; tally it for the run report's `Out of scope` line. A multi-name note survives if *any* of its primary names is listed, and is filed only under the listed name(s). Secondary mentions never rescue a note.

This skill does **not** summarize. Attribution is the only analysis — it decides which folder each raw file belongs in. The files go up unchanged.

## Step 3 — Find (or create) the ticker's Drive folder

For each ticker with ≥1 in-scope note:

1. **Search** under the configured root:
   ```
   search_files(query="mimeType = 'application/vnd.google-apps.folder' and title = '{TICKER}' and parentId = '{drive_root_folder_id}'")
   ```
   Try the exact `title = '{TICKER}'` match first — most folders are bare tickers (`BMNR`, `DUK`, `CLVT`, `SO`, `GFL`). Many, though, carry the company name in one of two conventions this Drive uses interchangeably: `TICKER (Name)` (e.g. `ATAI (AtaiBeckley)`, `JWACC (JW Aluminum)`) or `Name (TICKER)` (e.g. `Crinetics Pharma (CRNX)`). So when the exact match misses, fall back to `title contains '{TICKER}'` and keep the folder whose title has the ticker as a **standalone token** — bounded by start/end, whitespace, or any of `-_:/(),.` — which correctly lifts `CRNX` out of `Crinetics Pharma (CRNX)` while rejecting the `AI` buried inside `ATAI`. If two folders still plausibly match, prefer the one where the ticker is bare or parenthesized (not a substring of a longer word); if it's genuinely ambiguous, skip and flag rather than filing into both. Getting this right also prevents a false "no match" that would wrongly create a duplicate bare-ticker folder next to an existing `Name (TICKER)` one.
2. **Exactly one match →** use its id as the upload target.
3. **No match →**
   - `create_missing_folders: true` → create the folder with the Google folder mime type (per Tooling: `contentMimeType="application/vnd.google-apps.folder"`, no content), then use the returned id. (TEST mode: don't create; report "would create folder {TICKER}" and treat its uploads as "would upload".)
   - `create_missing_folders: false` → skip the ticker, and flag its notes for follow-up (when `flag_unrouted`), reporting "no folder for {TICKER}".
4. **Multiple matches →** do not guess-and-scatter. Pick the best standalone-token match; if still ambiguous, skip and flag with "ambiguous folder for {TICKER}" so a human resolves it — filing the same research into two rival folders is worse than pausing.

Resolve every folder id with read-only `search_files` even in TEST mode, so the dry-run report shows real destinations.

## Step 4 — Upload verbatim (with dedup)

For each in-scope ticker, upload every artifact of every one of its notes into that ticker's folder. **One folder per ticker; the raw files, unchanged.**

File **directly into the ticker's own folder** — its `parentId` is the folder resolved in Step 3. Do not descend into any research sub-folder the ticker folder may contain (some carry a `Sellside Notes` or `{TICKER} Broker Research` sub-folder, but the naming isn't uniform across tickers, so filing at the ticker-folder level keeps the rule identical for every name). The dedup search below is likewise scoped to that folder.

**Dedup first (idempotent — makes overlapping/re-triggered runs safe).** Before uploading a file, check whether it's already in the folder:
```
search_files(query="title = '{filename}' and parentId = '{ticker_folder_id}'")
```
A title hit means this artifact was already filed on a previous run → skip it and count it as "already filed". Because the 24h window overlaps day-to-day, this check is what stops the same PDF landing twice. If the same folder already holds a *different* file under an identical generic name (e.g. two notes both named `report.pdf`), disambiguate the incoming one by appending ` ({YYYY-MM-DD})` before the extension and note it — this keeps the bytes verbatim while avoiding a false-positive skip or an overwrite.

**Upload each artifact:**
- Read the raw bytes in binary and base64-encode them.
- `create_file(title="{filename_prefix}{original filename}", parentId="{ticker_folder_id}", base64Content="{b64}", contentMimeType="{type}", disableConversionToGoogleType=true)`
  - PDF → `contentMimeType="application/pdf"`.
  - `.eml` → `contentMimeType="message/rfc822"`.
  - rendered body PDF → `application/pdf`.
- `disableConversionToGoogleType=true` on **every** upload so Drive stores the exact file instead of converting it to a Google Doc/Slides. This is the difference between a verbatim archive and a lossy one.
- Preserve the original filename (subject to `filename_prefix`). Do not rename PDFs to something "tidier" — the filename is part of what the desk recognizes.

(TEST mode: skip every `create_file`; for each artifact report `would upload {filename} → {TICKER} folder ({id or "new"})`, plus any it would skip as already-filed.)

**Flag what couldn't be filed (when `flag_unrouted` is true).** After uploading, `flag_email(message_id)` on the kept copy of every research note that got no folder — "no ticker" macro/sector pieces, and (in strict mode) tickers of interest with no/ambiguous folder. The chat report scrolls away; the Outlook flag doesn't. Don't flag non-research skips (invites, logistics) or out-of-scope notes on a scoped run (those were deliberately disregarded per the reply). (TEST mode / connector fallback: report "would flag" instead.)

## Step 5 — Run report

End every run with a compact report in chat (this is what the scheduled-task transcript shows):

```
SELL-SIDE DRIVE FILER — {date} {time} ET — {LIVE|TEST}
Tickers of interest: WBD, LKSP (reply 5:12 PM ET) | ALL (reply) | none — all names (no reply)   [omit line when ask_tickers off]
Swept: {n} messages in window ({inbox|inbox + research_folder}) | research notes: {k} unique ({d} duplicate copies collapsed)
Drive root: "{root folder name}" ({drive_root_folder_id})

TICKER  FILES  FOLDER                          ACTION
WBD     2      WBD (existing)                  uploaded 2 PDFs (0 already filed)
LKSP    1      LKSP (created)                  uploaded 1 .eml (body-only desk note)
NVDA    1      NVDA (existing)                 skipped — 1 PDF already filed today
MSTR    1      — (no folder, strict mode)      not filed — flagged for follow-up

Skipped (no ticker): {broker} "{title}" — macro — flagged for follow-up
Skipped (not research): {sender} "{subject}" — conference invite
Out of scope (not in tickers of interest): {n} notes ({tickers})      [scoped runs only]
Linked PDFs: {n} fetched and filed | {m} gated/discarded              [omit line when fetch_linked_pdfs off or no links seen]
Degraded: {features skipped and why}                                  [omit line when none]
```

Upload nothing when zero in-scope research is found — just report it.

## Failure handling

- **`drive_root_folder_id` unset, still a placeholder, or unreadable** (a `search_files` / `get_file_metadata` on it errors) → stop before any write and say so; a run with no reachable root can't know where to file and must not scatter folders into My Drive. The shipped default (`0AKNhCG89u7IcUk9PVA`) is a Shared Drive, so if the signed-in Google account loses access to that drive this is the error that surfaces.
- **Google Drive connector absent** → stop and say so; this skill's only output is Drive uploads, so there's nothing to degrade to. Do not email the research anywhere as a "fallback".
- **Not signed in to Outlook** → stop; print the sign-in step. Never attempt to send/read through another identity.
- **A tool returns "Session expired"** → call `sign_out()` then `sign_in()`; print the returned device-code URL + code and stop — the browser step needs a human. The next run picks up after sign-in.
- **A PDF won't download or is unreadable** → still upload the file itself if you have the bytes (unreadable to a parser ≠ unusable to the team); if the bytes never arrived, flag the email and report "(attachment undownloadable — see original email)".
- **`download_email_as_eml` unavailable** for a body-only note → degrade `body_note_format` to `pdf`, else upload the extracted body as `{title}.txt` (`contentMimeType="text/plain"`, `disableConversionToGoogleType=true`), and note the degrade.
- **A `create_file` upload errors** (rate limit, transient) → retry once; if it still fails, leave the note unflagged-as-done, report the specific file that didn't upload, and don't mark it filed — so the next run's dedup won't wrongly skip it.
- **A gated/blocked research link** → non-fatal and expected. Discard the link, rely on the `.eml`/attachment capture, tally it on the `Linked PDFs` line. Never authenticate or route around the wall.
- **Phase A failed to send, or Phase B finds no ask thread for today** → file all attributable tickers and say so. The ask is a convenience; never let it block or shrink the run by accident.
