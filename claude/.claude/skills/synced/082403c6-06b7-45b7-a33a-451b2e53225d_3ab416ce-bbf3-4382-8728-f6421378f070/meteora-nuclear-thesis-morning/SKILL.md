---
name: meteora-nuclear-thesis-morning
description: "TEST copy of the Nuclear Energy MORNING brief, modified for the thesis-impact architecture. 24-hr window. Runs the normal nuclear sector brief (Bloomberg perf, sector + ticker news, AI analysis) AND adds an inline Thesis Impact section for tickers that have a thesis, then drafts a reply into each thesis ticker's internal Outlook thread. Reads internal threads via the email-assistant plugin and memory-doc theses via the Meteora MCP (read-only). Shares registry + dedup state with the intraday skill so no story repeats. Optimised for speed (parallel calls, batched Chrome, lazy gated reads) without loosening the date/freshness/pub-date accuracy gates. TEST MODE never sends — drafts only, sends only to the signed-in user (SELF), [TEST] subject prefix. Live sector skills untouched. Trigger on 'run the nuclear thesis morning', 'nuclear morning brief test', 'morning thesis brief'."
---

## SOURCE OF TRUTH
Authoritative spec for this run — read top to bottom. STANDALONE TEST COPY of `meteora-nuclear-energy-brief`, modified for the thesis-impact architecture (MORNING pipeline). Does NOT replace or modify the live nuclear brief or any of the 6 production sector skills. Created 2026-06-16. Window = 24 hours. Pairs with `meteora-thesis-intraday`; both share one state folder. While testing, NOTHING is sent and every recipient is forced to SELF.

## TEST MODE (HARD — active)
`TEST_MODE = true`. **SELF = the address returned by `email-assistant whoami` (the signed-in user running this skill). ALL test-mode email goes ONLY to SELF — i.e., you only ever email yourself while testing. Resolve SELF at runtime; never hardcode an address.** All email goes through the `email-assistant` plugin ONLY (do NOT use send-as-me). 1) Sending IS allowed, but the ONLY permitted recipient is `SELF` — never a real Stage-1 list, never real thread participants. 2) Never set `send_at`. 3) `[TEST]` subject prefix on the brief. 4) Brief → `email-assistant send_email` to SELF. 5) Internal reply → `email-assistant reply_email` on the latest thread message *authored by SELF* (routes to SELF, stays threaded); if the latest message is from anyone else, instead `email-assistant send_email` a new `RE: <subject>` to SELF. 6) PROD switch (real recipients + `reply_all_email`) is documented but INERT while TEST_MODE.

## SHARED STATE (single source of truth, both skills)
Folder (PORTABLE — never hardcode a username): `%USERPROFILE%\Documents\Claude\Scheduled\meteora-thesis-shared\`. Resolve `%USERPROFILE%` at runtime (PowerShell `$env:USERPROFILE`, or detect the home dir — do NOT assume any specific username). If the folder is missing, run the `meteora-thesis-manager` install routine first (or create it and seed empty JSONs).
- `registry.json > threads`: ticker → internal-thread `subject` (user-maintained; never overwrite).
- `posted-headlines.json`: dedup ledger (URL → {ticker, first_seen, mode}); read at start, read-merge-write at end, 7-day prune. A URL here is never re-analyzed/re-posted.
- `thread-cache.json` / `memory-doc-cache.json`: lazy caches to skip rediscovery.

## SECTOR CONFIG  <!-- SECTOR-SPECIFIC SWAP BLOCK: when the manager clones this skill for a new sector, swap ONLY these sector fields + the EXPANDED KEYWORDS, the sector/IR whitelist lines, the Step T.0 sector slug, the Step C.1 WebSearch queries, and the subject-line sector name. Everything else (TEST MODE, gates, locked format, dedup, shared state) stays VERBATIM. -->
- Sector: Nuclear Energy. Tickers: IMSR, OKLO, SMR, NNE, LTBR, ASPI, HDRN.
- Exchange (Google Finance): NASDAQ → IMSR, NNE, LTBR, ASPI, HDRN · NYSE → OKLO, SMR.
- **This brief's sector slug = `nuclear-energy`.** A registry ticker counts for THIS brief only if its `sector == "nuclear-energy"` (or it is in the hardcoded nuclear universe above). Registry tickers tagged another sector — or `sector: null` (unassigned) — are IGNORED here; they are handled by their own sector brief and/or the cross-sector intraday sweep.
- Thesis tickers (for this brief) = (hardcoded nuclear universe) UNION (registry tickers where `sector=="nuclear-energy"`), further requiring an internal thread AND/OR a memory doc.

## SPEED PLAYBOOK (do this — it is why this copy is faster; never trade away accuracy)
1. **Parallelize independent tool calls in ONE message:** the 7 `get-price` history calls (Step A.2) together; the 4 WebSearch queries (Step C.1) together.
2. **Batch Chrome with `browser_batch`:** group per-ticker Google Finance navigate+scrape (Step B) and the sector pub-date verifications (Step C.3) rather than one call each.
3. **Verify-once / dedupe-early:** before pub-date-verifying a sector candidate, drop it if it is already a verified ticker headline OR already in `posted-headlines.json`. Never verify the same URL twice.
4. **Gate thesis work:** Step T memory-doc + thread reads fire ONLY for a thesis ticker that has a fresh, in-window, non-duplicate headline. Quiet thesis tickers → one line, no reads.
5. **Cap thread reads** to the latest ~3 messages (or `save_thread_markdown`); never pull whole chains into context.
6. **One scan only:** Step T reuses headlines already gathered+verified in Steps B/C — never a second scan.
Accuracy anchors that STAY (do not skip): Step 0 deterministic dates, Step A.4 Bloomberg freshness gate, Step C.3 Chrome pub-date verification.

## STEP 0 — DATES (deterministic; never guess weekday)
0a) Navigate Chrome to `https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=5d`, then `javascript_tool`:
```javascript
window._dateInfo = (() => { const NOW=new Date(); return JSON.stringify({
  iso_utc:NOW.toISOString(),
  today_short:NOW.toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric'}),
  today_human:NOW.toLocaleDateString('en-US',{weekday:'long',year:'numeric',month:'long',day:'numeric'}),
  cutoff_24h:new Date(NOW.getTime()-24*60*60*1000).toISOString(),
  send_at_iso:(()=>{const d=new Date(NOW.getFullYear(),NOW.getMonth(),NOW.getDate(),9,0,0);return NOW.getTime()>d.getTime()?null:d.toISOString();})()
},null,2); })(); "executed";
```
Read back `window._dateInfo`, parse. 0b) Cross-verify bash `date +"%A, %B %-d, %Y"` == `today_human`; mismatch → ABORT. 0c) Subject `[TEST] [Nuclear Energy] Meteora Daily - ${today_short}`; body weekday verbatim from `today_human`.

## STEP A — Performance via Bloomberg get-price (PRIMARY; Yahoo fallback)
A.1 ONE batch `get-price` `tickers=[IMSR,OKLO,SMR,NNE,LTBR,ASPI,HDRN]`: per ticker `last_regular_close`→Close, `mid`→Pre-Mkt, %=(mid/close-1)*100; null/`_stale_warning`→`—`.
A.2 Lookbacks: issue all 7 per-ticker history calls **in a single message** (`fields=["PX_LAST"]`, start=13mo back, end=today). Drop today's row.
A.3 Returns vs `last_regular_close`: 1D prev row, 1W 5 rows back, 1M/6M/1Y last row on/before that date, YTD final row prior year.
A.4 FRESHNESS GATE (hard): anchor row date == expected last trading day (prior weekday; step back over US holidays). Else STALE → A.5. One shared anchor date.
A.5 Fallback: Yahoo chart API via Chrome (cache-buster) → `meta.regularMarketPrice` if expected bar missing pre-market → scrape `/quote/<T>/history/` → else render close with `(stale: M/D)` + footer note. Never show a stale close as current.

## STEP B — Google Finance ticker news (full universe; batch the navigations)
Group with `browser_batch`. For EACH ticker navigate `https://www.google.com/finance/quote/<T>:<EXCH>` then scrape (assign `window._scrapeResult`, read via a follow-up JS call):
```javascript
window._scrapeResult=(()=>{const out=[];for(const a of document.querySelectorAll('a[href*="://"]')){const href=a.href;if(href.includes('google.com')||href.includes('about.google')||href.includes('/finance/'))continue;const txt=(a.innerText||'').trim();if(txt.length<20||txt.length>300)continue;let p=a;for(let i=0;i<6&&p;i++){p=p.parentElement;if(!p)break;const dm=(p.innerText||'').match(/(\d+\s*(minute|hour|day|week|month)s?\s+ago|yesterday|today|[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})/i);if(dm){out.push({title:txt.slice(0,200),href,date_hint:dm[0]});break;}}}return out.slice(0,15);})();window._scrapeResult.length
```
Filter per ticker: 24-hr cap → paywall → whitelist preference → top 3 → dedupe vs Sector News AND vs `posted-headlines.json`. 0 survive → `<T>: No news in past 24 hrs.` Dump full hrefs untruncated before use. Fallback: `get_page_text` → WebSearch `"<6-8 words>" site:<domain>` → verify title+pub date → else DROP.

## STEP C — Sector News via WebSearch — pub-date verification mandatory
C.1 Run these 4 queries **in one message** (collect ~10-15 → filter to ~6-8):
- `nuclear energy OR "small modular reactor" news ${today_short}`
- `Oklo OR NuScale OR "Nano Nuclear" OR Lightbridge OR "ASP Isotopes" OR "Hadron Energy" news ${today_short}`
- `SMR OR nuclear NRC license OR contract OR deal ${yesterday_yyyy_mm_dd}`
- `nuclear power data center agreement ${today_short}`
C.2 WebSearch dates are NOT trustworthy. C.3 Verify each surviving candidate in Chrome (batch with `browser_batch`): open URL, read pub date:
```javascript
window._pubDate=(()=>{const sel=['meta[property="article:published_time"]','meta[property="og:article:published_time"]','meta[name="parsely-pub-date"]','meta[name="pubdate"]','meta[name="DC.date.issued"]','meta[itemprop="datePublished"]'];for(const s of sel){const el=document.querySelector(s);if(el&&el.content)return{source:s,value:el.content};}const t=document.querySelector('time[datetime]');if(t)return{source:'time[datetime]',value:t.getAttribute('datetime')};const lds=document.querySelectorAll('script[type="application/ld+json"]');for(const ld of lds){try{const j=JSON.parse(ld.textContent);const dp=j.datePublished||(Array.isArray(j)?j.find(x=>x.datePublished)?.datePublished:null);if(dp)return{source:'ld+json',value:dp};}catch(e){}}return{source:'none',value:null};})();JSON.stringify(window._pubDate);
```
GATE: include IFF `hours_since_pub<=24`; `value===null`→drop. Dedupe vs `posted-headlines.json`. C.4 Top 4 by relevance. C.5 If <4: targeted re-search; never pad with stale.

## STEP C+ — AI Analysis (headline-performance synthesis)
After perf, before Thesis Impact. Cover all tickers; depth ∝ |1D| (>=2% full paragraph w/ cited catalyst; 0.5-2% 1-2 sentences; <0.5% one sentence). Paywalled headlines allowed here (headline text only, tag `(paywalled)`, no Chrome check). Ground every causal claim in a cited headline; else "no single-headline catalyst identified". Pre-market callout if |pre-mkt|>=2% with a clear catalyst.

## STEP T.0 — Determine the thesis set (HARD — run for ALL universe tickers)
First build THIS brief's universe = (hardcoded nuclear tickers) UNION (registry tickers whose `sector=="nuclear-energy"`). Registry tickers with another sector or `sector:null` are EXCLUDED from the nuclear brief. Then for every universe ticker set `has_thesis = (ticker in registry.threads with sector nuclear-energy) OR has_memory_doc`. Resolve `has_memory_doc` from `memory-doc-cache.json` (fresh <7d); on any miss/stale, call Meteora MCP `list-memory-docs` ONCE and match all universe tickers in a single pass, then update the cache. This defines which tickers Step T analyzes and which appear in the brief's Thesis Impact section. NEVER skip — a memory-doc ticker (sector nuclear-energy) with no internal thread still requires inline thesis coverage.

## STEP T — THESIS-IMPACT ANALYZER (the new core; gated + lazy)
Run ONLY for thesis tickers (from Step T.0) with >=1 fresh, in-window, non-duplicate headline (reuse Steps B/C — no new scan).
T.1 Context (lazy, cached): Memory doc via Meteora MCP `read-memory-doc` (summary_only) if cache says present/fresh, else `list-memory-docs` match + cache (never create/update). Internal chain via email-assistant: resolve `registry.threads[T].subject`→conversationId (thread-cache else `search_emails subject=<subject>` newest-first), `read_thread` latest ~3 msgs for current thesis/discussion + last team conclusion; cache. Neither exists → skip ticker.
T.2 Per headline, vs BOTH memory-doc thesis AND live chain (chain wins where more current): (1) summary 1-2 sentences; (2) direction supports/weakens/invalidates/orthogonal, naming the assumption or tracked catalyst/risk; (3) material YES/NO/AMBIGUOUS; (4) if YES, note tied to the assumption + chain read.
T.3 Output `{ticker, headline(s), summary, direction, material, note}` → feeds the brief inline (Step D) AND the internal reply (Step R).

## THESIS IMPACT BLOCK (LOCKED FORMAT — used IDENTICALLY by the brief Step D and the reply Step R)
Both the brief's Thesis Impact section and the internal-thread reply use this exact per-ticker HTML so the two are visually consistent. Decluttered: a bold verdict header + a 4-item bullet list.
```html
<p style="margin:8px 0 2px 0;"><b>{TICKER} — {MATERIAL | NO MATERIAL IMPACT | AMBIGUOUS}</b></p>
<ul style="margin-top:0; padding-left:18px;">
  <li><b>Headline:</b> {1 sentence, faithful} (<a href="{URL}">{Source}</a>, {Nh|Nm} ago).</li>
  <li><b>Read-through:</b> {what the news actually is / how to read it}.</li>
  <li><b>Thesis:</b> {direction vs the named assumption or the chain's tracked catalyst/risk; whether the read changes}.</li>
  <li><b>Basis:</b> {memory doc {DOC} | internal chain | both | "not tracking via memory doc — internal chain only"}.</li>
</ul>
```
Thesis ticker with NO in-window headline (brief only): `<p style="margin:8px 0;"><b>{TICKER}:</b> no verified news in window; chain read unchanged.</p>`

## STEP D — Compose HTML brief (SELF-CONTAINED TEMPLATE — do NOT depend on any other skill)
Section order: (1) header (2) date line (3) Performance (4) AI Analysis (5) Thesis Impact (6) Sector News (7) Ticker News (8) New-ticker flags (9) Deals (10) footer. Styles LOCKED: inline only; table borders `1px solid #ccc`; positive `#080`, negative `#c00`; max-width 780px. News/Deal bullets LOCKED: `<li><a href="URL">Title</a> (Source, RELATIVE_TIME)</li>` — no em-dash, no absolute dates, no blurbs. Build the body from THIS exact embedded skeleton (fill placeholders; one `<tr>` per ticker; one Thesis Impact block per Step-T.0 thesis ticker). `{SECTOR_NAME}`/`{N}` come from SECTOR CONFIG; `{PREMKT_OR_LAST}` = "Pre-Mkt" at an ~8:15 AM scheduled run (mid vs prior close) or "Last" during a regular session.
```html
<!DOCTYPE html><html><body style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif; color:#222; line-height:1.45; font-size:14px; max-width:780px;">
<h2 style="margin:0 0 4px 0;">{SECTOR_NAME} — Meteora Daily</h2>
<p style="color:#666; margin:0 0 16px 0; font-size:13px;">{TODAY_HUMAN} · {N} tickers tracked</p>

<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:16px;">Performance</h3>
<table style="border-collapse:collapse; font-size:13px;">
<thead><tr style="background:#f4f4f4;">
<th style="border:1px solid #ccc; padding:6px 10px; text-align:left;">Ticker</th>
<th style="border:1px solid #ccc; padding:6px 10px;">Close ({ANCHOR_MD})</th>
<th style="border:1px solid #ccc; padding:6px 10px;">{PREMKT_OR_LAST}</th>
<th style="border:1px solid #ccc; padding:6px 10px;">1D</th><th style="border:1px solid #ccc; padding:6px 10px;">1W</th><th style="border:1px solid #ccc; padding:6px 10px;">1M</th><th style="border:1px solid #ccc; padding:6px 10px;">6M</th><th style="border:1px solid #ccc; padding:6px 10px;">YTD</th><th style="border:1px solid #ccc; padding:6px 10px;">1Y</th>
</tr></thead>
<tbody>
<!-- ONE row per ticker. Pre-Mkt/Last cell = "$X.XX (±N.NN%)" colored by sign, or "—" if no quote. Each % cell colored #080 (>=0) / #c00 (<0). -->
<tr>
  <td style="border:1px solid #ccc; padding:6px 10px;"><b>{TICKER}</b> <span style="color:#888;">{NAME}</span></td>
  <td style="border:1px solid #ccc; padding:6px 10px;">${CLOSE}</td>
  <td style="border:1px solid #ccc; padding:6px 10px; color:{SIGN};">${LAST} ({CHG}%)</td>
  <td style="border:1px solid #ccc; padding:6px 10px; color:{SIGN1D};">{1D}</td>
  <td style="border:1px solid #ccc; padding:6px 10px; color:{SIGN1W};">{1W}</td>
  <td style="border:1px solid #ccc; padding:6px 10px; color:{SIGN1M};">{1M}</td>
  <td style="border:1px solid #ccc; padding:6px 10px; color:{SIGN6M};">{6M}</td>
  <td style="border:1px solid #ccc; padding:6px 10px; color:{SIGNYTD};">{YTD}</td>
  <td style="border:1px solid #ccc; padding:6px 10px; color:{SIGN1Y};">{1Y}</td>
</tr>
</tbody>
</table>
<p style="color:#888; font-size:12px;">1D/1W/1M/6M/YTD/1Y are close-to-close vs the {ANCHOR_MD} anchor; "{PREMKT_OR_LAST}" is the {pre-market mid | live intraday quote}. Perf source: Bloomberg get-price.</p>

<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">AI Analysis — What Moved &amp; Why</h3>
<div style="font-size:13px; line-height:1.5; color:#333;">
<!-- one <p> per ticker, biggest |1D| first: <p><b>TICKER (±X.X%):</b> narrative tied to a cited <a href="URL">headline</a>; tag (paywalled) where applicable; adaptive length per Step C+. -->
</div>

<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">Thesis Impact</h3>
<div style="font-size:13px; line-height:1.5; color:#333;">
<!-- one LOCKED THESIS IMPACT BLOCK (defined above) per Step-T.0 thesis ticker (thread AND/OR memory-doc). Non-thesis tickers omitted. Thesis ticker with no in-window headline -> the one-line "no verified news in window; chain read unchanged." variant. -->
</div>

<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">Sector News (past 24 hrs)</h3>
<ul><!-- up to 4 verified items in LOCKED bullet format --></ul>
<p style="color:#888; font-size:12px;"><em>{FILTER_NOTE — e.g. only N items passed 24-hr pub-date verification; dropped stale/paywalled/unreliable}</em></p>

<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">Ticker News (past 24 hrs)</h3>
<p style="margin:0 0 4px 0;"><b>{TICKER}:</b></p>
<ul style="margin-top:0;"><!-- up to 3 verified items (LOCKED bullet format); or single line "{TICKER}: No news in past 24 hrs." --></ul>

<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">New-ticker flags</h3>
<p style="color:#666;">{NEW_TICKER_NOTES_OR_NONE}</p>

<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px; color:#666;">Deals (past 24 hrs)</h3>
<!-- <ul> of LOCKED-format deal items, OR <p><em>No deal news in past 24 hrs.</em></p> -->

<hr style="margin-top:22px; border:none; border-top:1px solid #ddd;">
<p style="color:#888; font-size:11px;">[TEST] Window: past 24 hours · cutoff {CUTOFF_ISO} · perf: Bloomberg get-price · thesis impact: Meteora memory docs + internal chains · TEST MODE: email-assistant, SELF only.</p>
</body></html>
```

## STEP R — Internal-thread reply draft (per thesis ticker THAT HAS A THREAD)
Only thesis tickers present in `registry.threads` get a reply draft. Memory-doc-only thesis tickers are covered inline in the brief (Step D) and produce NO reply (no thread exists).
HTML body (uses the SAME locked Thesis Impact block as the brief, so reply == brief format):
```html
<div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:13px;line-height:1.5;color:#333;">
<p style="margin:0 0 6px 0;"><b>{TODAY_HUMAN} — thesis-impact monitor (MORNING, TEST)</b></p>
{THESIS IMPACT BLOCK for this ticker — locked format}
<p style="color:#888;font-style:italic;font-size:11px;margin-top:10px;">— Auto-generated by the nuclear thesis-impact (morning) test skill. Review before sending.</p>
</div>
```
TEST MODE routing (email-assistant ONLY): preview with `reply_email` (confirmed=false) on the latest thread message authored by SELF, `html=true` → confirm recipient is exactly SELF → resend with `confirmed=true`. If the latest message is NOT from SELF, use `send_email` (draft→confirmed) a new `RE: <thread subject>` to `[SELF]` instead. Never `send_at`. Record each posted URL in `posted-headlines.json`.
PROD (inert): `reply_all_email` on `last_message_id`, `confirmed=true` → full participants.

## STEP E — Pre-send audit
1) Every news item has a complete tool-returned `<a href>`. 2) No paywalled outside AI-Analysis. 3) Perf cells bordered/colored, Pre-Mkt present or `—`, anchor freshness ok or `(stale: M/D)`. 4) Subject starts `[TEST] `. 5) WINDOW: every item's verified pub date <=24h. 6) DEDUP: nothing already in `posted-headlines.json`; new URLs recorded. 7) THESIS: every claim cites a headline + names assumption/chain read; no fabricated causation; "not tracking via memory doc" used correctly. 8) **TEST-MODE (CRITICAL):** email-assistant ONLY (no send-as-me); no `send_at`; every recipient is exactly SELF (the signed-in user); no real participants / AI_Interns / filings@. Any other recipient → STOP. 9) Bullet format matches locked contract.

## STEP F — Deliver (TEST MODE)
1) `email-assistant whoami` returns a valid signed-in mailbox (= SELF) else ABORT. 2) Brief: `email-assistant draft_email` then `send_email` (confirmed=true) with identical fields — `to=[SELF]`, `html=true`, subject `[TEST] [Nuclear Energy] Meteora Daily - ${today_short}`, body=<HTML>. NO `send_at`. 3) Internal updates per Step R (email-assistant). 4) Write run summary. PROD (inert): brief `send_email` to the real Stage-1 list with `send_at`; internal `reply_all_email confirmed=true`.

## STEP H — Run summary (chat)
Per-ticker `{ticker, has_thesis(doc/chain/none), headlines_in_window, deduped_new, analyzed, material, draft_made|skipped_no_news}`; dedup delta; anomalies; explicit confirmation nothing was sent and all drafts went only to SELF.

## SCHEDULING (this is meant to run automatically — set up a recurring task)
This brief should fire every weekday morning. Ask Claude to create a scheduled task:
- Prompt: `Run the Nuclear Energy thesis morning brief (meteora-nuclear-thesis-morning).`
- Cron: `15 8 * * 1-5` (≈9 AM ET delivery, matching the production sector briefs).
Confirm email-assistant + Meteora MCP are connected before the first scheduled run. While `TEST_MODE` is on, scheduled runs email only SELF; flip the PROD switch when ready for real recipients. (Each sector gets its OWN morning task; the intraday sweep is one shared cross-sector task — see its skill.)

## LOCKS
- Test copy of `meteora-nuclear-energy-brief`; live sector skills UNTOUCHED. Pairs with intraday skill via shared state folder.
- TEST_MODE on: email-assistant ONLY; sends allowed but recipient forced to SELF (signed-in user); [TEST] prefix; no send_at. Brief and reply share the LOCKED Thesis Impact block (bulleted, identical format).
- Window 24h. No duplicate stories (shared dedup). Thesis = memory doc (read-only) AND/OR internal chain; thesis set resolved for ALL universe tickers (Step T.0, HARD); lazy+gated+cached. Memory-doc-only tickers get inline brief coverage; thread tickers also get a reply.
- Speed Playbook enforced (parallel calls, browser_batch, verify-once, gated reads). Accuracy anchors kept: Step 0 dates, A.4 freshness gate, C.3 pub-date verification. Bullet format locked.
- No scheduled task registered by default. Manual runs only until the user flips PROD.
