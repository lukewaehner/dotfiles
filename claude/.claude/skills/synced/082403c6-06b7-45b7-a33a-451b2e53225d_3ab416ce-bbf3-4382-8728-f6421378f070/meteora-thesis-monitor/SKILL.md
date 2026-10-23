---
name: meteora-thesis-monitor
description: "General, FILE-DRIVEN intraday news monitor for internal research threads (not a daily brief, not sector-specific). Reads a FLAT ticker list from watchlist.json (ticker -> internal Outlook thread subject + memory-doc flag) and, on a fresh material headline, drafts a thesis-impact update into that ticker's internal chain. Default SCAN_SET = internal-thread tickers; toggle to all. The STEP 2 news scan FANS OUT across parallel read-only sub-agents in buckets for speed; analyzer, drafting and dedup writes stay centralized. On a material hit it reads the internal thread + Meteora memory doc (read-only) AND pulls a LIVE position snapshot from spac-details so the email shows where we stand. 60-MINUTE HARD CAP, cross-run dedup, pub-date verified. TEST MODE drafts only to the signed-in user (SELF), [TEST] prefix. Edit the list via the meteora-thesis-manager skill. Trigger on 'run the news monitor', 'thesis sweep', 'scan news', 'scan a ticker', or a scheduled run."
---

## SOURCE OF TRUTH
A GENERIC engine. It contains NO ticker list of its own — the tickers live in watchlist.json (the meat), as a FLAT list (no sectors, no groups). Scope = intraday news to internal-chain thesis update ONLY. No daily/morning brief, no performance table, no AI-analysis section. Created 2026-06-17.

## TEST MODE (HARD — active)
TEST_MODE = true. SELF = the address from email-assistant whoami (the signed-in user). ALL email goes ONLY to SELF — you only ever email yourself while testing. Resolve SELF at runtime; never hardcode an address. Email goes through the email-assistant plugin ONLY. Never set send_at. Put [TEST] in any subject. Internal reply uses reply_email on the latest thread message authored by SELF (routes to SELF, stays threaded); if the latest message is from anyone else, use send_email for a new "RE: {thread subject}" to SELF. The PROD switch (real participants plus reply_all_email) is documented but INERT while TEST_MODE.

## METEORA MCP USAGE (read-only, lazy, material-hits only)
This skill calls Meteora MCP only AFTER a ticker clears the fresh-headline gate AND is judged material:
- read-memory-doc (summary_only) — baseline thesis, when memory_doc is true.
- spac-details (by ticker) — LIVE position snapshot (common / warrants / rights / units) + trust/CIT + liquidation deadline, AND the warrant/rights tickers used to build the thread-discovery identifier set.
Never create or update memory docs. Never place trades. No get-price/EMSX/EDGAR calls in this skill.

## DATA FILES — the meat (PORTABLE path, auto-detect; never hardcode a username)
Folder: %USERPROFILE%\Documents\Claude\Scheduled\meteora-thesis-shared\ (resolve %USERPROFILE% at runtime). If missing, tell the user to run the meteora-thesis-manager install. Files:
- watchlist.json — THE source of truth. FLAT shape: tickers.{TICKER}.subject (internal Outlook thread subject, or null) and tickers.{TICKER}.memory_doc (true/false). No groups, no sectors. This is the only file that defines what gets scanned. Tickers sharing one thread (e.g. HUN and OLN) point at the same subject.
- posted-headlines.json — dedup ledger (url to {ticker, first_seen_iso}); read at start, read-merge-write at end, 7-day prune.
- thread-cache.json — subject to {conversationId, last_message_id, last_seen_iso}; lazy.
- reply-template.html — the HTML body of the internal-thread reply, with brace placeholders. Read it at send time and fill placeholders; do not hardcode the HTML here.

## TICKER SELECT (decide from the trigger)
- SCAN_SET config (set at the top of the run): default = "threads" — ONLY tickers whose subject is NOT null (the names we can actually post into; today that is the small set). Flip SCAN_SET = "all" to scan every ticker in watchlist.json (future broad mode — scans all tickers, but still drafts ONLY where a thread exists).
- If the user named a single ticker (e.g. "scan HDRN") OR a scheduled prompt specifies one, load ONLY that ticker (overrides SCAN_SET).
- Otherwise load the SCAN_SET set. In "threads" mode, null-subject tickers are NOT scanned (nothing to post into). In "all" mode, a null-subject ticker may be scanned but is reported as skipped_no_thread if it has news.
Announce SCAN_SET and which tickers you are sweeping.

## SPEED PLAYBOOK (stay tiny)
1. Gate hard, gate early: no fresh in-window headline means STOP for that ticker (no thread read, no memory read, no spac-details, no draft). Most sweeps end here in seconds.
2. Live-listing discovery first (Google Finance / StockTitan / BusinessWire), not WebSearch — same-day PRs appear there before WebSearch indexes them; then open the article only to read the pub date.
3. Batch Chrome with browser_batch.
4. Dedup BEFORE analysis: drop anything already in posted-headlines.json before any thread, memory, or spac-details read.
5. Lazy plus cached thread/memory reads; cap read_thread to the latest 3 messages.
6. Fan the scan out (STEP 1.5) so many tickers are checked in parallel; keep the heavy analyzer/draft/dedup in one place.

## STEP 0 — DATE plus 60-MIN CUTOFF (deterministic)
Navigate Chrome to the Yahoo finance chart endpoint for AAPL (interval 1d, range 5d), then run javascript_tool:
```javascript
window._dateInfo=(()=>{const NOW=new Date();return JSON.stringify({iso_utc:NOW.toISOString(),today_human:NOW.toLocaleDateString('en-US',{weekday:'long',year:'numeric',month:'long',day:'numeric'}),cutoff_1h:new Date(NOW.getTime()-60*60*1000).toISOString()},null,2);})();"executed";
```
Read back window._dateInfo; cross-verify bash date weekday equals today_human; mismatch means ABORT. CAP = cutoff_1h (older than 60 minutes is dropped — no exceptions).

## STEP 1 — Load watchlist (plus optional single-ticker filter) plus dedup
Read watchlist.json; build the ticker set per TICKER SELECT (each entry carries its subject and memory_doc flag). Read posted-headlines.json to build the dedup set. Empty set means nothing to do, stop.

## STEP 1.5 — PARALLEL FAN-OUT (scanner sub-agents)
The STEP 2 news scan is the bottleneck, so fan it out; the analyzer, drafting and dedup writes stay centralized in THIS run (the orchestrator).
- Split the loaded ticker set into BUCKETS of about 30 tickers each (BUCKET_SIZE = 30; raise it if runs feel slow, lower it if scanners time out). One bucket = one sub-agent.
- Spawn all buckets CONCURRENTLY: issue every Agent call in a SINGLE message (subagent_type general-purpose). Give each scanner: its bucket (ticker + company name + subject), the orchestrator's cutoff_1h, and the current dedup URL set (read-only).
- Each scanner is READ-ONLY: it runs STEP 2 ONLY for its bucket (reuse the passed cutoff_1h; do not recompute the date) and returns a COMPACT JSON list of fresh, in-window, NON-duplicate hits: [{ticker, headline_sentence, url, source, pub_iso, minutes_ago}]. Nothing else.
- Scanners DO NOT read threads, read memory docs, call spac-details, draft, send, or write any file. That keeps guardrails, drafting and ALL dedup-ledger writes in ONE place (the orchestrator) and prevents two agents double-posting a shared-thread story (e.g. HUN/OLN).
- If a single ticker was named, OR the set is tiny (about 30 or fewer), skip fan-out and scan inline.
- Orchestrator merges every scanner's hits, re-dedups the merged list, then runs STEP 3 onward only on the (usually few) hits.

## STEP 2 — Per-ticker news scan (60-min cap)
For EACH ticker (batch Chrome ops). Use the ticker symbol plus its company name as the relevance terms.
1. Discover candidates: Google Finance quote page for the ticker (infer exchange; default NASDAQ) and the StockTitan news listing for the ticker. Apply paywall/unreliable filters.
2. For each surviving candidate, open it and read the pub date:
```javascript
window._pubDate=(()=>{const sel=['meta[property="article:published_time"]','meta[property="og:article:published_time"]','meta[name="parsely-pub-date"]','meta[name="pubdate"]','meta[name="DC.date.issued"]','meta[itemprop="datePublished"]'];for(const s of sel){const el=document.querySelector(s);if(el&&el.content)return JSON.stringify({source:s,value:el.content});}const t=document.querySelector('time[datetime]');if(t)return JSON.stringify({source:'time',value:t.getAttribute('datetime')});const lds=document.querySelectorAll('script[type="application/ld+json"]');for(const ld of lds){try{const j=JSON.parse(ld.textContent);const dp=j.datePublished||(Array.isArray(j)?j.find(x=>x.datePublished)?.datePublished:null);if(dp)return JSON.stringify({source:'ld',value:dp});}catch(e){}}return JSON.stringify({source:'none',value:null});})();
```
3. GATE: keep IF AND ONLY IF minutes_since_pub is 60 or less; a null value means drop (no fallback).
4. Drop anything already in the dedup set. Nothing fresh and new means STOP for this ticker.

## THREAD DISCOVERY (canonical — matches spac-filing-digest / s1-filing-handler)
Find the ONE canonical internal chain for a ticker with the SAME mandatory matrix Luke's spac-filing-digest and the s1-filing-handler use — do NOT shortcut to the stored subject or a single broad scan:
1. Identifier set: from spac-details take common (spac_ticker), warrant_ticker, rights_ticker (skip any absent or 0); ADD the unit ticker in BOTH forms {COMMON}U and {COMMON}/U (spac-details does NOT carry the unit; it is the most-missed). Also include the stored watchlist subject token if present.
2. Search every identifier X across every folder: search_emails(subject="Internal X", folder=F) for F in SentItems, then Inbox, then Archive. A teammate-opened thread lives in Inbox, not Sent. NEVER substitute one broad subject="Internal" scan (it is capped and silently drops threads).
3. Exact-token match: "Internal FVN" must not match "Internal FVNN"; the common must not swallow the unit/warrant/rights variant; NEVER collapse roman numerals (III is not II). Treat RE:/Fw: prefixes and any trailing text as the SAME thread.
4. Winner: among all CLEAN hits (participants are the desk / Filings@ with NO no-reply or alert address such as notifications@bamsec.com or tech@spacinsider.com), take the SINGLE MOST RECENT message across all identifiers and folders; read_thread it to confirm the recipients are clean; cache subject -> conversationId / last_message_id.
5. Conclude "no thread" ONLY after the full matrix returns zero clean hits.

## STEP 3 — THESIS-IMPACT ANALYZER (only for tickers with a fresh, new headline)
T.1 ESTABLISH CURRENT STATE FIRST — context before conclusions (lazy, cached, but ORDERED):
  (a) PULL spac-details ONCE (read-only, by ticker). It yields BOTH (i) our LIVE position — common / warrants / rights / units, plus trust/CIT and liquidation deadline — and (ii) the identifier set (common / warrant / rights tickers) for thread discovery.
  (b) FIND THE INTERNAL THREAD via the canonical matrix in THREAD DISCOVERY above — do NOT just trust the stored subject. read_thread the winning chain's latest ~3 messages and extract where we are now: the LATEST running thesis / most recent update / last team conclusion. THE THREAD IS THE MOST CURRENT SOURCE OF TRUTH AND OVERRIDES THE MEMORY DOC wherever they differ — assume the memory doc may be stale.
  (c) IF memory_doc is true, also call read-memory-doc (summary_only) for the BASELINE thesis (read-only; never create or update) — backdrop only, not the current word.
  (d) POSITION SNAPSHOT = the live figures from the spac-details payload in (a) (authoritative "where we stand"; overrides any doc/chain figure). If spac-details returned not_found, fall back to the position stated in the memory doc or thread; if neither, "no position on file".
  Synthesize a one-line "current state" = the running thesis as it stands TODAY (thread-latest first; memory doc as backdrop), with our live position attached. No clean thread found AND no memory doc means skip the ticker (in SCAN_SET=all a material name with neither may open a new canonical chain — see STEP R).
T.2 ONLY THEN analyze the new headline AGAINST that established current state (never in isolation): summary (1-2 sentences); direction vs the current running thesis (supports / weakens / invalidates / orthogonal, naming the assumption or tracked catalyst/risk); material YES / NO / AMBIGUOUS; if YES, a note tied to that assumption. Then produce a THESIS UPDATE and COMPARE IT EXPLICITLY AGAINST THE THREAD'S LATEST RUNNING THESIS (not the memory doc): if the headline changes that running thesis, state the concrete one-line change; if the memory doc disagrees with the thread, defer to the thread and flag the memory doc as possibly stale. If not material, "no change to thesis". The THESIS UPDATE describes ONLY how the news affects our thesis — it is NOT a trade or position recommendation. NEVER suggest buying, selling, adding, trimming, chasing, hedging, or sizing, and never tell the team what to do with the position. Analyze the news and its thesis impact; the decision is the team's.

## STEP 3.5 — MATERIAL GATE (we are NOT forced to send)
Only tickers with material = YES proceed to STEP 4 and STEP R. For material = NO or AMBIGUOUS: do NOT build a block, do NOT draft, do NOT send any email — record the ticker as analyzed_not_material in the summary. WE NEVER SEND AN EMAIL JUST BECAUSE THERE WAS A HEADLINE; only a genuine material change to the running thesis warrants a draft. Still record EVERY analyzed URL (material or not) in posted-headlines.json so it is not re-processed next run. If NO ticker is material this run, send nothing and say so in one line. Pull spac-details only for the material tickers — never for the whole watchlist.

## STEP 4 — Build the reply (from reply-template.html) — material tickers only
Read reply-template.html from the shared folder. Structure per ticker = clear TITLE, quick HEADLINE, quick SUMMARY, THESIS IMPACT. Fill brace placeholders: TODAY_HUMAN; and per material ticker (repeat the per-ticker block once each): TICKER, VERDICT (always MATERIAL here), HEADLINE_SENTENCE, URL, SOURCE, AGO (e.g. "12m ago"), SUMMARY (1-2 sentence quick summary of the news); and under THESIS IMPACT: DIRECTION_NOTE (supports/weakens/invalidates/orthogonal vs the running thesis, naming the assumption/catalyst; judged against the thread first, memory doc as backdrop), POSITION_EXPOSURE (the LIVE spac-details snapshot — e.g. "Common 839,998 | Warrants 174,288 | Rights 0 | Units 0; trust/CIT $10.12; deadline 2028-04-07"; omit zero legs cleanly; if spac-details not_found use the doc/chain figure or "no position on file"), THESIS_UPDATE (concrete change to the running thesis vs the thread's latest read; if the memory doc looks stale, say so; describe the thesis impact ONLY — NO trade/position recommendation, no buy/sell/add/trim/chase/hedge/size language), BASIS ("memory doc {DOC}", "internal chain", "both", or "not tracking via memory doc — internal chain only"; append "+ live spac-details" when the position came from spac-details). Do not invent HTML beyond the template.

## STEP R — Send the internal-thread reply (per MATERIAL ticker only)
TEST MODE routing (email-assistant ONLY): reply_email with confirmed=false on the latest thread message authored by SELF, html=true, body = the filled template; confirm the recipient is exactly SELF; then resend with confirmed=true. If the latest message is NOT from SELF, use send_email (draft then confirmed) for a new "RE: {thread subject}" to the SELF address. Never set send_at. Record each posted URL in posted-headlines.json (read-merge-write, 7-day prune).
NEW-CHAIN FALLBACK (matches the handlers): if THREAD DISCOVERY returned zero clean threads for a material ticker (only possible in SCAN_SET=all), open the canonical chain with send_email (draft then confirmed), subject EXACTLY "Internal {COMMON}" (the word Internal, a space, the bare common ticker) — in TEST_MODE addressed only to SELF with the [TEST] prefix; in PROD to Filings@meteoracapital.com. Never open a new chain until the full matrix has run.
PROD (inert): reply_all_email on last_message_id with confirmed=true.

## STEP E — Audit
1) Every headline pub date verified at 60 minutes or less. 2) Nothing already in posted-headlines.json; all analyzed URLs recorded. 3) Every thesis claim cites the headline and names the assumption/chain read; no fabricated causation. 4) MATERIAL GATE honored: an email exists ONLY for material=YES tickers; non-material tickers produced NO email. 5) Position line came from a real spac-details call (or an explicit fallback) — never invented. 6) TEST-MODE (CRITICAL): email-assistant ONLY; no send_at; every recipient is exactly SELF; no real participants — else STOP. 7) URLs complete and tool-returned. 8) NO trade/position recommendation anywhere in the draft — news-vs-thesis impact only; the position line is a factual snapshot.

## STEP H — Run summary (chat)
SCAN_SET and tickers swept; per ticker: ticker, headlines_in_60min, deduped_new, analyzed, material, and one of draft_made / analyzed_not_material / skipped_no_news / skipped_no_thread; dedup delta; confirmation nothing was sent beyond SELF and nothing was sent for non-material tickers. If the whole sweep found nothing material, say so in one line.

## SCHEDULING (set up ONE recurring task)
Ask Claude to create a scheduled task: prompt "Run the thesis news monitor.", cron like */45 13-21 * * 1-5 (UTC, roughly market hours). ONE task covers the whole watchlist. While TEST_MODE is on, scheduled runs email only SELF.

## LOCKS
- GENERIC engine; the flat ticker list lives in watchlist.json (edit via the manager skill). No sectors, no groups, no per-sector skills.
- Default SCAN_SET = threads (internal-thread tickers only). Flip to "all" for the full universe (broad scan; still drafts only where a thread exists).
- STEP 2 scan FANS OUT across parallel read-only sub-agents in ~30-ticker buckets; the analyzer, drafting and ALL dedup writes stay centralized in the orchestrator. Scanners never read threads/docs, never call spac-details, never draft, never write files.
- THREAD DISCOVERY is the canonical ticker x folder matrix (common + warrant + rights + unit {COMMON}U and {COMMON}/U, across SentItems/Inbox/Archive), exact-token match (roman numerals never collapse), newest CLEAN thread wins (no no-reply/alert participant). Same method as spac-filing-digest / s1-filing-handler; never shortcut to the stored subject or one broad "Internal" scan. Open a new chain (Internal {COMMON}) only after the matrix returns zero clean hits.
- Scope = intraday news to internal-chain update only. No daily brief, no perf, no AI-analysis.
- ONLY MATERIAL updates are sent. We are NEVER forced to send — a fresh headline alone is not enough; non-material/ambiguous tickers produce no email.
- ANALYZE-ONLY, NEVER ADVISE. The skill ONLY analyzes the news and classifies its material/immaterial impact on our EXISTING thesis. It NEVER recommends a position action — no buy/sell/add/trim/chase/hedge/size language anywhere. The decision is the team's; the skill just surfaces the news, the thesis impact, and a factual position snapshot.
- The internal THREAD is the most-current thesis and OVERRIDES the memory doc; assume the memory doc may be stale and compare the thesis update against the thread's latest running thesis.
- Every reply carries a LIVE position snapshot from spac-details (common/warrants/rights/units + trust + deadline), pulled read-only and ONLY for material tickers; fall back to doc/chain or "no position on file" if not_found. Never place trades.
- TEST_MODE: email-assistant ONLY; recipient forced to SELF; no send_at; [TEST] prefix. PROD switch documented and inert.
- 60-minute HARD cap. Cross-run dedup (records all analyzed URLs). Lazy plus gated reads. Pub-date verification kept. Reply HTML lives in reply-template.html.
- No scheduled task registered by default.
