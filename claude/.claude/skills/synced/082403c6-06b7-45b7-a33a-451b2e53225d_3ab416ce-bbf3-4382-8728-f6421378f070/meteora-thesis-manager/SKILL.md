---
name: meteora-thesis-manager
description: "Edit the news-monitor's data files by chatting — companion to meteora-thesis-monitor. The meat is a FLAT ticker list in watchlist.json (ticker maps to its internal Outlook thread subject plus a memory-doc flag — no sectors, no groups); this skill maintains it conversationally. INSTALL auto-detects the user's home and seeds the shared folder (under %USERPROFILE% Documents/Claude/Scheduled/meteora-thesis-shared) — never hardcodes a username. ADD TICKERS is interactive: asks which tickers, scans Outlook for internal threads (email-assistant), checks Meteora memory docs, shows what it found to confirm, then instantly updates watchlist.json. LIST shows the watchlist; REMOVE drops a ticker; EDIT makes any other change (fix a subject, etc.). Trigger on 'set up the monitor', 'add tickers', 'add a ticker', 'scan internal threads', 'list tickers', 'remove ticker', 'edit watchlist'. Reads/writes only the shared folder; reads Outlook and memory-doc list read-only; never sends email."
---

## SOURCE OF TRUTH
Companion editor for meteora-thesis-monitor. It owns the data files (the meat); it does NOT scan news or post analysis (that is the monitor). The watchlist is a FLAT ticker list — no sectors, no groups, no per-sector skills, no cloning. Created 2026-06-17. Reads/writes ONLY the shared folder; reads Outlook (email-assistant) plus the memory-doc list (Meteora MCP, read-only). Never sends email.

## PORTABLE SHARED FOLDER (auto-detect; never hardcode a username)
SHARED = %USERPROFILE%\Documents\Claude\Scheduled\meteora-thesis-shared\. Resolve %USERPROFILE% at runtime. All file ops use this resolved path.

## watchlist.json SHAPE (the one file that matters)
A flat map: tickers.{TICKER}.subject (internal Outlook thread subject, or null) and tickers.{TICKER}.memory_doc (true/false). Tickers sharing one thread point at the same subject. Always READ-MERGE-WRITE (never clobber existing tickers); validate JSON after write; keep a .bak and restore on parse failure.

## MODE SELECT (from the trigger; announce it)
- INSTALL — "set up", "install", or SHARED/watchlist.json missing.
- ADD TICKERS — "add ticker(s)", "scan internal threads".
- LIST — "list tickers".
- REMOVE — "remove ticker".
- EDIT — any other chat edit (change a subject, fix memory_doc). Make the edit, read-merge-write, confirm.
If ambiguous, ASK.

## MODE: INSTALL
1. Resolve SHARED. If it exists with watchlist.json, report "already set up" then LIST.
2. Else create SHARED and copy the bundled seed files: watchlist.json (illustrative or empty), posted-headlines.json, thread-cache.json, reply-template.html, README.txt.
3. Validate JSON (read back + parse). 4. Confirm email-assistant is signed in (whoami) so the add-tickers scan works. 5. Tell the user to save the meteora-thesis-monitor skill and run "add tickers".

## MODE: ADD TICKERS (interactive)
### Step 1 — Which tickers
AskUserQuestion: "Which tickers to add?" (multiSelect plus an "Other" free-text). UPPERCASE; dedupe against existing watchlist.
### Step 2 — Scan now?
AskUserQuestion: Yes (scan Outlook plus memory docs) / Not now (add bare with subject null, scan later).
### Step 3 — Scan (if Yes), parallel where possible
- Internal thread — use the CANONICAL ticker x folder matrix (same as Luke's spac-filing-digest / s1-filing-handler; do NOT shortcut): build the identifier set = common + warrant + rights (from Meteora MCP spac-details) PLUS the unit in BOTH forms {TICKER}U and {TICKER}/U (the unit is the most-missed). For each identifier X, search_emails(subject="Internal X", folder=F) for F in SentItems, Inbox, Archive. Exact-token match ("Internal FVN" != "Internal FVNN"; roman numerals never collapse). Among all CLEAN hits (no no-reply/alert participant) take the SINGLE MOST RECENT; capture its subject + message_id. Never rely on one broad subject="Internal" scan or Sent-only.
- Memory doc: Meteora MCP list-memory-docs ONCE (covers all); match each ticker by name (read-only).
### Step 4 — Confirm
Per-ticker summary: ticker, thread subject found (or none), memory doc found (or none). AskUserQuestion (multiSelect) to confirm the threads are the RIGHT ones. An unconfirmed thread is still addable but with subject null.
### Step 5 — Write
For each confirmed ticker: set tickers.{TICKER} = { subject: confirmed subject or null, memory_doc: true/false }. If a thread was found, also seed thread-cache[subject] = {conversationId, last_message_id, last_seen_iso: now}. Read-merge-write plus validate plus .bak.
### Step 6 — Confirm
Report exactly what was written (ticker, subject found?, memory doc?). The next monitor run includes them; a ticker with subject null is skipped by the monitor until a subject is set.

## MODE: LIST
Print a table: ticker, thread subject (or none), memory doc (or none). No writes.

## MODE: REMOVE
AskUserQuestion which ticker(s) to remove. Delete from watchlist; read-merge-write; confirm. Leave posted-headlines.json history intact (harmless).

## SAFETY / LOCKS
- Reads/writes ONLY the resolved SHARED folder; reads Outlook plus the memory-doc list (read-only). No email send. No memory-doc creation. No sectors, no groups, no per-sector skills, no cloning, no daily brief.
- Auto-detect home; never hardcode a username. All writes: read-merge-write plus validate plus .bak restore.
- Add-anyway: a ticker with no confirmed thread is still added (subject null); the monitor covers it once a subject is set.
