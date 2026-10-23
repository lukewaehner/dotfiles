---
name: meteora-thesis-intraday
description: "Lean, CROSS-SECTOR INTRADAY sweep for the thesis-impact architecture (pairs with the per-sector morning briefs). Runs every ~45 min. 60-MINUTE HARD CAP on news. Scans every ticker that has an internal Outlook thread in the shared registry (all sectors, including unassigned), and on a new, non-duplicate headline analyzes thesis impact against the memory doc (Meteora MCP, read-only) + the internal chain (email-assistant) and drafts a reply into that thread. No brief, no perf table, no AI-analysis section — deliberately tiny and fast. Shares registry + dedup state with the morning skill so no story repeats across runs. TEST MODE never sends — drafts only, sends only to the signed-in user (SELF), [TEST] subject prefix. Live sector skills untouched. Trigger on 'run the thesis intraday', 'intraday thesis sweep', 'nuclear intraday sweep', or a 45-min scheduled run."
---

## SOURCE OF TRUTH
Authoritative spec — read top to bottom. STANDALONE TEST skill, the INTRADAY pipeline of the thesis-impact architecture. Pairs with `meteora-nuclear-thesis-morning` and shares one state folder. Does NOT modify the live nuclear brief or any of the 6 production sector skills. Created 2026-06-16. Window = **60 minutes, hard**. Deliberately lean: no perf, no AI analysis, no HTML brief. While testing, NOTHING is sent; every recipient forced to SELF (the signed-in user).

## TEST MODE (HARD — active)
`TEST_MODE = true`. **SELF = the address returned by `email-assistant whoami` (the signed-in user running this skill). ALL test-mode email goes ONLY to SELF — i.e., you only ever email yourself while testing. Resolve SELF at runtime; never hardcode an address.** All email goes through the `email-assistant` plugin ONLY (never send-as-me). 1) Sending IS allowed, but the ONLY permitted recipient is `SELF` — never real thread participants. 2) Never set `send_at`. 3) `[TEST]` in any subject. 4) Internal reply → `email-assistant reply_email` on the latest thread message *authored by SELF* (routes to SELF, threaded); if the latest is from anyone else, `email-assistant send_email` a new `RE: <subject>` to SELF. 5) PROD switch (real participants + `reply_all_email`) is INERT while TEST_MODE.

## SHARED STATE (same files the morning skill uses)
Folder (PORTABLE — never hardcode a username): `%USERPROFILE%\Documents\Claude\Scheduled\meteora-thesis-shared\`. Resolve `%USERPROFILE%` at runtime (PowerShell `$env:USERPROFILE`, or detect the home dir — do NOT assume any specific username). If the folder is missing, run the `meteora-thesis-manager` install routine first (or create it and seed empty JSONs).
- `registry.json > threads`: ticker → internal-thread `subject`. **This is the intraday universe** (only these tickers are scanned). User-maintained; never overwrite.
- `posted-headlines.json`: shared dedup ledger. Read at start; read-merge-write at end (7-day prune). A URL here is never re-analyzed/re-posted — this is what stops the morning run and the sweeps from double-posting.
- `thread-cache.json` / `memory-doc-cache.json`: lazy caches.

## UNIVERSE (CROSS-SECTOR — this is the single intraday sweep for ALL sectors)
Universe = **every** ticker in `registry.threads` that has a non-null `subject`, **regardless of `sector`** (nuclear-energy, autonomous-trucking, …, or `sector:null`). This sweep is sector-agnostic: it is the ONLY coverage for tickers whose `sector` is null/unassigned (no morning brief exists for them), and it ALSO re-checks sector-tagged tickers intraday. Intraday acts only on tickers with an internal thread (nowhere to post otherwise); a registry ticker with `subject:null` is skipped until a subject is set. (Legacy name says 'nuclear' but the sweep covers the whole registry.) Exchange for Google Finance: HDRN→NASDAQ (extend as registry grows; default NASDAQ, OKLO/SMR→NYSE if added).

## SPEED PLAYBOOK (this skill must stay tiny)
1. **Gate hard, gate early:** if a ticker has no new in-window headline, STOP for it — no memory-doc read, no thread read, no draft. Most sweeps end here in seconds.
2. **Live-listing discovery first** (not WebSearch): same-day PRs hit Google Finance / StockTitan / BusinessWire listings before WebSearch indexes them. Discover there, then open the article only to read the pub date.
3. **Batch Chrome** with `browser_batch`; one pass for discovery + pub-date check.
4. **Dedup before analysis:** drop anything already in `posted-headlines.json` BEFORE any thread/memory read.
5. **Lazy + cached** thread/memory reads; cap `read_thread` to latest ~3 msgs.
Accuracy anchors kept: deterministic date (Step 0), Chrome pub-date verification (Step 2), 60-min hard cap.

## STEP 0 — DATES + 1-HR CUTOFF (deterministic)
Navigate Chrome to `https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=5d`, then `javascript_tool`:
```javascript
window._dateInfo=(()=>{const NOW=new Date();return JSON.stringify({iso_utc:NOW.toISOString(),today_human:NOW.toLocaleDateString('en-US',{weekday:'long',year:'numeric',month:'long',day:'numeric'}),cutoff_1h:new Date(NOW.getTime()-60*60*1000).toISOString()},null,2);})();"executed";
```
Read back `window._dateInfo`. Cross-verify bash `date` weekday == `today_human`; mismatch → ABORT. CAP = `cutoff_1h` (anything older than 60 minutes is dropped — no exceptions).

## STEP 1 — Load shared state
Read `registry.json` (universe) and `posted-headlines.json` (dedup). Empty registry → nothing to do, stop. Build the in-memory dedup set from `posted`.

## STEP 2 — Per-ticker news scan (narrow universe, 60-min cap)
For EACH universe ticker (batch Chrome ops):
1. Discover candidates from Google Finance (`https://www.google.com/finance/quote/<T>:<EXCH>`) and the StockTitan listing (`https://www.stocktitan.net/news/<T>/`). Apply paywall/whitelist/unreliable filters.
2. For each surviving candidate, open the article and read pub date:
```javascript
window._pubDate=(()=>{const sel=['meta[property="article:published_time"]','meta[property="og:article:published_time"]','meta[name="parsely-pub-date"]','meta[name="pubdate"]','meta[name="DC.date.issued"]','meta[itemprop="datePublished"]'];for(const s of sel){const el=document.querySelector(s);if(el&&el.content)return{source:s,value:el.content};}const t=document.querySelector('time[datetime]');if(t)return{source:'time[datetime]',value:t.getAttribute('datetime')};const lds=document.querySelectorAll('script[type="application/ld+json"]');for(const ld of lds){try{const j=JSON.parse(ld.textContent);const dp=j.datePublished||(Array.isArray(j)?j.find(x=>x.datePublished)?.datePublished:null);if(dp)return{source:'ld+json',value:dp};}catch(e){}}return{source:'none',value:null};})();JSON.stringify(window._pubDate);
```
3. GATE: keep IFF `minutes_since_pub <= 60`. `value===null` → drop (no fallback).
4. Drop anything already in the dedup set. If nothing fresh+new for this ticker → STOP for it (no further reads).

## STEP 3 — THESIS-IMPACT ANALYZER (only for tickers with a fresh, new headline)
T.1 Context (lazy, cached): memory doc via Meteora MCP `read-memory-doc` (summary_only) — `list-memory-docs` match on cache miss; never create/update. Internal chain via email-assistant: resolve `registry.threads[T].subject`→conversationId (thread-cache else `search_emails subject=<subject>` newest-first); `read_thread` latest ~3 msgs for current thesis/discussion + last conclusion; cache conversationId + last_message_id. Neither exists → skip.
T.2 Per headline, vs BOTH memory-doc thesis AND live chain (chain wins where more current): summary (1-2 sentences) · direction (supports/weakens/invalidates/orthogonal, name the assumption or tracked catalyst/risk) · material YES/NO/AMBIGUOUS · if YES, note tied to assumption + chain read.

## THESIS IMPACT BLOCK (LOCKED FORMAT — identical to the morning brief, for consistency)
Decluttered: bold verdict header + 4-item bullet list, per ticker.
```html
<p style="margin:8px 0 2px 0;"><b>{TICKER} — {MATERIAL | NO MATERIAL IMPACT | AMBIGUOUS}</b></p>
<ul style="margin-top:0; padding-left:18px;">
  <li><b>Headline:</b> {1 sentence, faithful} (<a href="{URL}">{Source}</a>, {Nm} ago).</li>
  <li><b>Read-through:</b> {what the news actually is / how to read it}.</li>
  <li><b>Thesis:</b> {direction vs the named assumption or the chain's tracked catalyst/risk; whether the read changes}.</li>
  <li><b>Basis:</b> {memory doc {DOC} | internal chain | both | "not tracking via memory doc — internal chain only"}.</li>
</ul>
```

## STEP R — Internal-thread reply draft
HTML body (SAME locked Thesis Impact block as the morning brief — reply == brief format):
```html
<div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:13px;line-height:1.5;color:#333;">
<p style="margin:0 0 6px 0;"><b>{TODAY_HUMAN} — thesis-impact monitor (INTRADAY, TEST)</b></p>
{THESIS IMPACT BLOCK for this ticker — locked format}
<p style="color:#888;font-style:italic;font-size:11px;margin-top:10px;">— Auto-generated by the nuclear thesis-impact (intraday) test skill. Review before sending.</p>
</div>
```
TEST MODE routing (email-assistant ONLY): preview with `reply_email` (confirmed=false) on the latest thread message authored by SELF, `html=true` → confirm recipient is exactly SELF → resend `confirmed=true`. If the latest message is NOT from SELF, `send_email` (draft→confirmed) a new `RE: <thread subject>` to `[SELF]`. Never `send_at`. Then record each posted URL in `posted-headlines.json` (read-merge-write, 7-day prune).
PROD (inert): `reply_all_email` on `last_message_id`, `confirmed=true`.

## STEP E — Audit
1) Every headline pub date verified <=60 min. 2) No item already in `posted-headlines.json`; new URLs recorded. 3) Every thesis claim cites the headline + names assumption/chain read; no fabricated causation. 4) **TEST-MODE (CRITICAL):** email-assistant ONLY (no send-as-me); no `send_at`; every recipient is exactly SELF (the signed-in user); no real participants anywhere → else STOP. 5) URLs complete + tool-returned (no truncation/fabrication).

## STEP H — Run summary (chat)
Per-ticker `{ticker, headlines_in_60min, deduped_new, analyzed, material, draft_made|skipped_no_news}`; dedup delta; confirmation nothing was sent and all drafts went only to SELF. If the whole sweep found nothing new, say so in one line.

## SCHEDULING (set up ONE recurring cross-sector task)
Runs every ~45 minutes during market hours and covers ALL sectors' internal threads. Ask Claude to create a scheduled task:
- Prompt: `Run the thesis intraday sweep (meteora-thesis-intraday).`
- Cron: e.g. `*/45 13-21 * * 1-5` (UTC ≈ 9:00–17:00 ET) — adjust to your market-hours window.
ONE task covers every sector (do not create per-sector intraday tasks). While `TEST_MODE` is on it emails only SELF.

## LOCKS
- INTRADAY pipeline; pairs with `meteora-nuclear-thesis-morning` via the shared state folder. Live sector skills UNTOUCHED.
- TEST_MODE on: email-assistant ONLY; sends allowed but recipient forced to SELF (signed-in user); no send_at. Reply uses the LOCKED Thesis Impact block (bulleted, identical to the morning brief).
- Window 60 minutes HARD. Universe = registry threads tickers only. No duplicate stories (shared dedup).
- Thesis = memory doc (read-only) + internal chain; lazy+gated+cached. Speed Playbook enforced. Pub-date verification kept.
- No scheduled task registered by default. Manual runs only until the user flips PROD.
