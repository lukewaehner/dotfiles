---
name: meteora-thesis-impact-test
description: TEST skill — per-ticker thesis-impact monitor over tickers in watchlist.json, independent of the 6 production sector briefs. For each ticker it finds 24-hr pub-date-verified news, READ-ONLY checks the Meteora memory doc for a thesis (cached), READS the 'Internal {TICKER}' Outlook thread for the current thesis and discussion state (cached), and analyzes how the news affects both. ONLY when at least one verified headline exists does it DRAFT a REPLY-ALL into that thread — no news, no draft. Drafts only, reply-all only — NEVER sends, NEVER sets send_at, NEVER creates or updates memory docs. Trigger on 'run the thesis-impact test', 'draft internal updates', 'test the thesis monitor', 'internal thread test', or any variant. Always use this skill for the thesis-impact test — do not run ad hoc. Does not touch the 6 production sector briefs.
---

# Meteora Thesis-Impact Monitor — TEST WORKFLOW

## SOURCE OF TRUTH

This is a STANDALONE TEST skill. It does NOT replace any production sector brief. It tests a new workflow: per-ticker thesis-impact analysis driven by BOTH the Meteora memory doc AND the live internal email chain, delivered as reply-all draft updates into each ticker's internal thread. Output: drafts (reply-all) in the user's Outlook Drafts folder (no auto-send, no scheduled delivery, no Stage 1/2). Created 2026-06-10. Caching layer added 2026-06-10 — memory-doc lookups and Outlook thread lookups are persisted to JSON files alongside this SKILL.md so subsequent runs skip the discovery phase. Updated 2026-06-16: (a) replies are now REPLY-ALL to the full thread participant list, never reply-to-sender-only; (b) the skill now READS the internal thread on every run to extract the current thesis/discussion state and judges news against that live context, not just the static memory doc; (c) a draft is produced ONLY when at least one verified 24-hr headline exists — no news, no draft for that ticker — and the draft body no longer carries a standalone "where the chain stands" section (chain context feeds the thesis-impact note instead).

## CRITICAL RULES (READ FIRST — non-negotiable)

1. **DO NOT CREATE MEMORY DOCS.** If a ticker has no memory doc, write "not tracking via memory doc" and proceed. NEVER call `create-memory-doc`, `update-memory-doc`, or any memory-write tool. (The internal email chain is still read and used for context even when no memory doc exists.)
2. **DO NOT SEND EMAIL.** NEVER call `send_email`. NEVER set `send_at`. Use the draft/preview path only (`reply_all_email` WITHOUT `confirmed=True`). Verify drafts land in the Drafts folder.
3. **REPLY-ALL ONLY.** Always reply to the ENTIRE participant set of the latest thread message (To + Cc, minus the run mailbox itself, plus the original sender). NEVER reply to the sender only. Use `reply_all_email`; if only `reply_email` is available, construct the full recipient list manually so every existing participant is retained.
4. **24-HR HARD CAP** on news (same gate as production briefs).
4b. **NO VERIFIED NEWS = NO DRAFT.** A draft/reply is produced for a ticker ONLY if it has at least one verified 24-hr headline. If zero headlines pass the gate, SKIP that ticker entirely — no draft, no reply — and log the skip in the run summary.
5. **NEVER fabricate URLs or headlines.** Every linked URL is tool-returned; pub date is verified. A headline that appears only inside the internal thread but cannot be independently verified is NOT treated as a found headline (it may still inform context).
6. **NEVER fabricate thesis content.** Thesis comes from the memory doc and/or the internal chain. If neither exists → "not tracking via memory doc" and no chain context.
7. **NEVER fabricate causation.** Ambiguous → "ambiguous — no clear material impact". Honesty over narrative.
8. **DO NOT TOUCH the 6 production sector briefs.**
9. **CACHE WRITES must be valid JSON** and must not lose existing entries — always read-merge-write (never overwrite blindly).

## DATA FILES (in this skill's folder)

Three editable JSON files live alongside this SKILL.md at `C:\Users\rishi\Documents\Claude\Scheduled\meteora-thesis-impact-test\`:

### `watchlist.json` — editable ticker list (user-maintained)
```json
{
  "tickers": ["HDRN", "KDK"],
  "notes": "add or remove tickers here; the skill picks up the list at run time"
}
```
Keep tickers uppercase. The skill reads this on every run. If a ticker is added, it joins discovery on the next run. If removed, drafts for it stop.

### `memory-doc-cache.json` — auto-maintained by the skill
```json
{
  "HDRN": { "has_memory_doc": true,  "doc_name": "HDRN.md", "doc_id": "<pinecone-id>", "last_checked": "2026-06-10T12:15:23Z" },
  "KDK":  { "has_memory_doc": false, "doc_name": null,      "doc_id": null,           "last_checked": "2026-06-10T12:15:23Z" }
}
```
Skip Pinecone discovery for any ticker whose cached `last_checked` is within the last 7 days. Re-discover and update on miss or stale.

### `thread-cache.json` — auto-maintained by the skill
```json
{
  "HDRN": { "conversationId": "AAQk...=", "subject": "Internal HDRN", "last_seen": "2026-06-10T12:15:23Z" },
  "KDK":  { "conversationId": "AAQk...=", "subject": "Internal KDK",  "last_seen": "2026-06-10T12:15:23Z" }
}
```
Skip the `Internal {TICKER}` mailbox search for any ticker with a cached conversationId. Confirm the thread still exists via `read_thread`; on 404 (archived/deleted), invalidate the entry and fall through to discovery. NOTE: the thread is ALWAYS read on each run (Step D) regardless of cache state — the cache only skips the search-by-subject step, not the read.

If any of these files is missing at run-start, treat it as empty (`{}` for caches; `{"tickers": []}` for watchlist) and log a warning. Empty watchlist → ABORT (nothing to do).

## STEP 0 — DATES (same JS as production)

Navigate Chrome to `https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=5d` first, then call `mcp__Claude_in_Chrome__javascript_tool` with:

```javascript
window._dateInfo = (() => {
  const NOW = new Date();
  return JSON.stringify({
    iso_utc: NOW.toISOString(),
    today_short: NOW.toLocaleDateString('en-US', { month:'long', day:'numeric', year:'numeric' }),
    today_human: NOW.toLocaleDateString('en-US', { weekday:'long', year:'numeric', month:'long', day:'numeric' }),
    cutoff_iso: new Date(NOW.getTime() - 24*60*60*1000).toISOString()
  }, null, 2);
})();
"executed";
```

Read via `window._dateInfo`. Cross-verify with bash `date +"%A, %B %-d, %Y"` — MUST equal `today_human`. ABORT on mismatch.

## STEP PRE-A — Load Watchlist + Caches

Use the `Read` tool (preferred) to load the three JSON files. If using PowerShell
instead, always specify encoding explicitly: `Get-Content $path -Encoding UTF8`
or `[System.IO.File]::ReadAllText($path, [Text.Encoding]::UTF8)`. The default on
Windows is cp1252, which silently corrupts non-ASCII characters.

1. Read `watchlist.json`. Parse `tickers` array. ABORT if empty or missing.
2. Read `memory-doc-cache.json`. Parse as object (key = ticker, value = cache entry). Treat missing or invalid JSON as empty `{}`.
3. Read `thread-cache.json`. Same treatment.

Maintain in-memory state for the run:
```
state = {
  tickers: [...from watchlist...],
  mem_cache: {...from memory-doc-cache.json...},
  thread_cache: {...from thread-cache.json...},
  mem_cache_changed: false,
  thread_cache_changed: false,
  now_iso: <today_iso_utc from Step 0>
}
```

## STEP A — Optional context: Bloomberg get-price (skippable)

For each ticker, optionally call Meteora MCP `get-price` (batch call where possible) to capture last regular close + pre-market mid. If it succeeds, the one-line `<TICKER> $X.XX close (M/D), pre-mkt $Y.YY (±N.NN%)` goes into the draft body. SKIP silently on error — informational, not blocking.

## STEP B — Memory doc check per ticker (READ-ONLY, cached)

For EACH ticker in `state.tickers`:

### B.1 — Cache hit (fresh, <7 days)
If `mem_cache[ticker]` exists AND its `last_checked` is within the last 7 days:
- If `has_memory_doc == true`: call Meteora MCP `read-memory-doc` using `doc_name` (or `doc_id`). Extract thesis section. Set `state[ticker].has_memory_doc = true` and `state[ticker].thesis_text = <extracted>`. SKIP Pinecone discovery.
- If `has_memory_doc == false`: SKIP Pinecone discovery entirely. Set `state[ticker].has_memory_doc = false`.

### B.2 — Cache miss or stale (>=7 days, or no entry)
- Call Meteora MCP `list-memory-docs`. Find any doc matching the ticker (`HDRN`, `KDK`, etc. in the name or title).
- If found: call `read-memory-doc`. Extract thesis. Update `mem_cache[ticker] = {has_memory_doc: true, doc_name, doc_id, last_checked: state.now_iso}`. Set `state.mem_cache_changed = true`.
- If not found: update `mem_cache[ticker] = {has_memory_doc: false, doc_name: null, doc_id: null, last_checked: state.now_iso}`. Set `state.mem_cache_changed = true`.
- **NEVER call `create-memory-doc`** under any circumstance.

### B.3 — Audit
At end of Step B, every ticker has `state[ticker].has_memory_doc` set. No Pinecone writes have happened. If any write happened, ABORT — critical violation.

## STEP C — News headlines per ticker (WebSearch + 24-hr pub-date verification)

Google Finance scraping is DROPPED for this skill. Use WebSearch.

For EACH ticker, run 1–2 targeted WebSearch queries:
- `"{TICKER}" news ${TODAY_SHORT}`
- `"{TICKER}" OR "<Company Name from memory doc / chain if available>" after:${YESTERDAY_YYYY_MM_DD}`

Collect ~5–10 candidate URLs. Apply the same paywall/whitelist/unreliable filters as production.

For EACH surviving candidate, navigate Chrome to the URL and extract pub date:

```javascript
window._pubDate = (() => {
  const sel = [
    'meta[property="article:published_time"]',
    'meta[property="og:article:published_time"]',
    'meta[name="parsely-pub-date"]',
    'meta[name="pubdate"]',
    'meta[name="DC.date.issued"]',
    'meta[itemprop="datePublished"]'
  ];
  for (const s of sel) { const el = document.querySelector(s); if (el && el.content) return {source:s, value:el.content}; }
  const t = document.querySelector('time[datetime]');
  if (t) return {source:'time[datetime]', value:t.getAttribute('datetime')};
  const lds = document.querySelectorAll('script[type="application/ld+json"]');
  for (const ld of lds) { try { const j = JSON.parse(ld.textContent); const dp = j.datePublished || (Array.isArray(j) ? j.find(x=>x.datePublished)?.datePublished : null); if (dp) return {source:'ld+json', value:dp}; } catch(e){} }
  return {source:'none', value:null};
})();
JSON.stringify(window._pubDate);
```

GATE: include IFF `hours_since_pub <= 24`. Drop on no machine-readable date. Top 2–3 verified headlines per ticker. Zero pass → SKIP this ticker entirely: NO draft, NO reply. Log the skip in the run summary. (A ticker with no verified news is dropped even if its thread was found.)

## STEP D — Find AND READ the Internal thread per ticker (email-assistant, cached)

This step does TWO things: locate the `Internal {TICKER}` thread, and READ it fully so the run anchors on where the thesis/discussion currently stands. The thread is read on EVERY run.

### D.1 — Locate the thread
- **Cache hit:** if `thread_cache[ticker]` exists, use the cached `conversationId`/`message_id` directly.
- **Cache miss/invalidation:** call `mcp__plugin_email-assistant_email-assistant__search_emails` with subject `Internal {TICKER}`, ~10 results, newest first. Pick the conversation whose subject contains `Internal {TICKER}` (or `RE: Internal {TICKER}`); if multiple, take the most recent activity.
- If NO matching thread found: SKIP this ticker's draft. Log in the run summary. Do NOT cache the absence (so next run retries). Do NOT create a new thread.

### D.2 — Read the thread (MANDATORY every run)
- Call `mcp__plugin_email-assistant_email-assistant__read_thread` on the located message. For long chains use `save_thread_markdown` to capture the full text.
- From the thread, extract **chain context** into `state[ticker].chain_context`:
  - The current working thesis / read as expressed by the team (this may extend or override the memory-doc thesis).
  - The catalysts, risks, and open questions the chain is actively tracking (e.g. upcoming binary events, cap-structure overhangs, licensing milestones, deal status).
  - The most recent team conclusion on prior headlines (so the new draft is consistent with, and builds on, the running discussion rather than repeating it).
  - Capture the latest message's metadata: `last_message_id`, full To + Cc participant list, subject. This drives the reply-all recipient set in Step F.
- On 404 / "not found": DELETE `thread_cache[ticker]`, set `state.thread_cache_changed = true`, and re-run D.1 discovery.

### D.3 — Cache update
- On success, update `thread_cache[ticker] = {conversationId, subject, last_seen: state.now_iso}`. Set `state.thread_cache_changed = true`.

## STEP E — Thesis-impact analysis (per ticker per headline)

Analyze each headline against BOTH the memory-doc thesis (Step B) AND the live chain context (Step D.2). The chain context takes precedence where it is more current than the memory doc.

### If a thesis/chain context exists (memory doc OR chain), for each verified headline:
1. **Headline summary** — 1–2 sentences faithful to the article.
2. **Direction vs thesis** — supports / weakens / invalidates / orthogonal. Cite the named thesis assumption OR the specific catalyst/risk the chain is tracking.
3. **Material impact** — `YES` if it shifts a thesis-critical assumption or a catalyst/risk the chain is actively watching (binary catalyst, deal break, major management change, FDA/regulatory outcome, financing/dilution event, customer win/loss of measurable scale). `NO` if noise / broader beta. `AMBIGUOUS` if genuinely unclear.
4. If `YES` → 1–2 sentence **Thesis Impact** note tied to the named assumption AND to where the chain currently stands.

### Zero verified headlines:
- NO draft is produced for this ticker. Skip it entirely (no reply, no "no-news" note) and record the skip in the run summary. The memory-doc / chain reads were still gathered but are not emailed.

### If `has_memory_doc == false` AND no usable chain context:
- Headline summary only. Thesis-impact note reads `not tracking via memory doc`.

### If `has_memory_doc == false` BUT chain context exists:
- Use the chain context as the thesis basis. Note `not tracking via memory doc — basis is the internal chain's current read` and analyze against that.

## STEP F — Draft REPLY-ALL per ticker (DRAFTS ONLY — no send)

For EACH ticker with a found thread AND at least one verified headline (tickers with zero verified headlines are skipped per Rule 4b — do not draft for them):

1. Compose the reply body from the template below (HTML or plain text per the tool).
2. Save as a REPLY-ALL DRAFT — call `mcp__plugin_email-assistant_email-assistant__reply_all_email` WITHOUT `confirmed=True` (preview/draft only). This retains EVERY participant on the latest thread message (To + Cc) plus the original sender.
   - If `reply_all_email` is unavailable, fall back to `draft_email` with the FULL recipient list reconstructed from Step D.2 metadata (`to` = all To recipients + original sender; `cc` = all Cc recipients), `subject` = `RE: <thread subject>`, threading headers (`In-Reply-To` / `References` = `last_message_id`) if supported. NEVER collapse the recipient list down to the sender alone.
3. VERIFY the draft was created — call `search_emails` against the Drafts folder for the expected subject. If the email tool only previews (does not persist a Drafts item), report that explicitly in the run summary rather than sending. NEVER retry by sending.
4. **NEVER call `send_email`.** **NEVER set `send_at`.** **NEVER set `confirmed=True`.**

### Reply body template

```
{TODAY_HUMAN} — daily thesis-impact monitor (TEST)

Headlines (past 24 hrs, pub-date verified):
• <Title 1> — <Source>, <Nh ago>
  <1–2 sentence summary>
• <Title 2> — <Source>, <Nh ago>
  <1–2 sentence summary>

[Optional Step-A context line if available: {TICKER} $X.XX close (M/D), pre-mkt $Y.YY (±N.NN%)]

Thesis impact:
<one of:
 — Material — <1–2 sentence explanation tied to a named thesis assumption AND the chain's current read>
 — No material impact — the verified headline(s) don't touch a thesis assumption or a catalyst/risk the chain is tracking
 — Ambiguous — <what's unclear and what to watch for>
 — not tracking via memory doc — no Meteora memory doc for this ticker; basis is the internal chain's current read (or: no thesis check performed if no chain context).>

— Draft auto-generated by the thesis-impact test skill. Review before sending.
```

The footer line is REQUIRED.

## STEP G — Cache writeback

After processing all tickers:

1. If `state.mem_cache_changed`:
   - Serialize `state.mem_cache` as pretty-printed JSON (2-space indent, keys sorted alphabetically).
   - Write to `memory-doc-cache.json` via PowerShell `[System.IO.File]::WriteAllText` (UTF-8, no BOM).
   - Re-read and `JSON.parse` to validate. If invalid, restore previous content from a `.bak` backup taken before the write.

2. If `state.thread_cache_changed`:
   - Same procedure for `thread-cache.json`.

3. **Never** write `watchlist.json` — it is user-maintained, not skill-maintained.

## STEP H — Run summary (chat output only)

After cache writeback, output a short summary to chat:
- Per ticker: `{ticker, has_memory_doc, thesis_source: cache_hit | freshly_discovered | none, chain_context_read: yes | no, headlines_verified, thread_found, thread_source: cache_hit | freshly_discovered | none, draft_saved (reply-all) | skipped_no_news, draft_recipient_count, draft_subject_or_id}`.
- Total drafts created.
- Cache deltas: how many memory-doc entries written, how many thread entries written.
- Any anomalies (memory doc found but no recognizable thesis section, thread found but recipient list looks wrong, headline present only in the chain but unverifiable, etc.).

NO email sent. NO scheduled-task fires this skill until the user explicitly registers one.

## LOCKS

- Tickers: loaded from `watchlist.json` (currently HDRN, KDK). Edit the file to add or remove tickers.
- Memory docs: READ ONLY. Never create, never update.
- Internal thread: READ every run; used as live thesis/discussion context. Reply-all draft only.
- Reply mode: REPLY-ALL to the full thread participant list. Never reply-to-sender-only.
- Memory-doc cache: 7-day TTL; refreshed on stale or miss.
- Thread cache: no TTL on the subject-search skip; thread is still READ every run; refreshed only on `read_thread` 404 (lazy invalidation).
- Email: DRAFTS only. Never send. Never set send_at. Never set confirmed=True.
- News window: 24-hr pub-date verified. No verified 24-hr headline for a ticker → no draft for that ticker (the thread is read for context, but nothing is emailed).
- This skill is INDEPENDENT of the 6 production sector briefs.
- Scheduled task: NOT registered by default. Manual invocation only until the user confirms behavior.
