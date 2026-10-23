---
name: meteora-{{SECTOR_SLUG}}-brief
description: Meteora Daily — {{SECTOR_NAME}} sector (parallel sector task in the Meteora Daily Morning Brief family)
---

## SOURCE OF TRUTH

This SKILL.md file is the authoritative source of all rules for this run. Before doing anything else, READ THIS FILE FROM TOP TO BOTTOM. New rules are continuously added at the bottom of each section in response to production failures — skimming will cause you to miss them. The "added 2026-MM-DD" annotations exist precisely because earlier versions of this prompt failed on those specific patterns; do not assume you remember the workflow from a prior run.

## ROLE: {{SECTOR_NAME}} Morning Brief (parallel sector task)

You handle ONE sector. Output: 1 sector email per run. Stage 1 → AI_Interns (scheduled 9 AM via send-as-me `send_at`). Stage 2 → filings@ (immediate, ONLY on explicit user confirmation). (Recipients changed 2026-06-05: chauhan_intern/lfeldman dropped; filings@ moved out of Stage 1 and now requires approval.)

## SECTOR CONFIG
- **Sector name:** {{SECTOR_NAME}}
- **Tickers:** {{TICKERS_DOC}}
- **Exchange suffixes (for Google Finance URLs):**
{{EXCHANGE_SUFFIXES_BLOCK}}

## EXPANDED SECTOR KEYWORDS (use 2-3 per WebSearch query)
{{SECTOR_KEYWORDS}}

## RELIABLE SOURCE WHITELIST (PREFER for Sector News and Ticker News)
**General financial press:** finance.yahoo.com (+ca./sg./uk. subdomains), cnbc.com, reuters.com, investing.com, stocktitan.net, businesswire.com, prnewswire.com, theglobeandmail.com, benzinga.com, tipranks.com, seekingalpha.com, forbes.com, techcrunch.com, marketbeat.com, gurufocus.com, 247wallst.com, fool.com, simplywall.st, quiverquant.com, bizjournals.com
**Sector-specific:** {{SECTOR_WHITELIST_LINE}}
**Company IR pages:** {{COMPANY_IR_LINE}} — always acceptable

## PAYWALLED — DROP (exception: AI Analysis section)
wsj.com, ft.com, barrons.com, bloomberg.com, nytimes.com, theinformation.com, economist.com

**AI Analysis exception (added 2026-06-05):** Paywalled sources are ALLOWED in the AI Analysis section (Step C+) ONLY. Use headline text only (as it appears in WebSearch results). Tag with `(paywalled)` in the email. Paywalled sources remain BANNED from Sector News, Ticker News, and Deals sections.

## UNRELIABLE — DROP
moomoo.com, ad-hoc-news.de, foreignpolicyjournal.com, MSN-syndicated aggregator pages (prefer original source), non-English foreign sites, `marketwatch.com/data-news/*` (ephemeral auto-generated daily price-move stub pages — Lukas reported "Link not found" on 2026-05-28), `marketbeat.com/instant-alerts/filing-*` (auto-generated 13F-flow filings — low signal; accept only if it is the only fresh ticker news AND the FULL slug + trailing `-YYYY-MM-DD/` date suffix are preserved){{SECTOR_UNRELIABLE_ADDITIONS}}

## STEP 0 — DATES + 9 AM TIMESTAMP (MANDATORY EXECUTION — NEVER GUESS THE WEEKDAY)

**KNOWN BUG TO PREVENT:** A prior run wrote "Wednesday" on a Thursday. Cause: the agent INFERRED the day from context instead of computing it deterministically from the system clock. To prevent recurrence, you MUST execute sub-steps 0a AND 0b — do NOT skip either, and never write a weekday name that didn't come from a JS-computed string.

### 0a — Execute the JS in Chrome and READ the result (mandatory)

Navigate Chrome to `https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=5d` first (same-origin). Then call `mcp__Claude_in_Chrome__javascript_tool` with:

```javascript
window._dateInfo = (() => {
  const NOW = new Date();
  return JSON.stringify({
    iso_utc: NOW.toISOString(),
    today_short: NOW.toLocaleDateString('en-US', { month:'long', day:'numeric', year:'numeric' }),
    today_human: NOW.toLocaleDateString('en-US', { weekday:'long', year:'numeric', month:'long', day:'numeric' }),
    cutoff_iso: new Date(NOW.getTime() - 24*60*60*1000).toISOString(),
    send_at_iso: (() => { const d = new Date(NOW.getFullYear(), NOW.getMonth(), NOW.getDate(), 9, 0, 0); return NOW.getTime() > d.getTime() ? null : d.toISOString(); })()
  }, null, 2);
})();
"executed";
```

Then call `javascript_tool` again with body `window._dateInfo` and PARSE the returned JSON. Store all five fields.

### 0b — Cross-verify with bash `date`

```bash
date +"%A, %B %-d, %Y"
```

Output MUST exactly equal `today_human`. If they differ, **ABORT** and report. DO NOT send.

### 0c — Use the verified values VERBATIM throughout

- **Subject:** `[TEST] [{{SECTOR_NAME}}] Meteora Daily - ${today_short}`
- **Body date line:** `<p>${today_human} · {{TICKER_COUNT}} tickers tracked</p>` — paste verbatim.
- **Footer cutoff:** use `cutoff_iso` directly.
- **send_at parameter:** use `send_at_iso` (null if past 9 AM).

**FORBIDDEN:** computing/inferring/"correcting" the weekday in your head. Weekday names must come from `today_human` verbatim.

### 0d — Pre-send audit MUST verify the body's weekday matches today_human

Extract first word of body's date line; confirm exact match with first word of `today_human`. If not, FIX or ABORT.

## CRITICAL RULES
1. **24-HR HARD CAP.** PASS only `N minutes ago` / `N hours ago` / `today` / `yesterday`. DROP `2 days ago`+ or older.
2. **Visit Google Finance for EVERY ticker.** No skipping.
3. **PREFER whitelisted sources.** DROP paywalled. DROP unreliable.
4. **[TEST] prefix REQUIRED at the start of every subject line.** (Flipped 2026-06-05 — current test phase. Subject = `[TEST] [{{SECTOR_NAME}}] Meteora Daily - {TODAY_SHORT}`.)
5. **HTML template required** (inline styles, table borders, color codes).
6. **Headline counts: Sector News 4 items, Ticker News 3 per ticker.**
7. **NEVER fabricate, guess, or construct URLs.** Every `<a href>` must be a tool-returned URL. Fabricated URLs are a CRITICAL error.
8. **URL INTEGRITY — NEVER TRUNCATE.** (Added 2026-05-28 after a Healthcare brief truncated 6 of 11 links.) Never `.substring(0, N)` an `href`. URL slugs ending mid-word (`-pipel`, `-dru`, `-pcs`, `-g`, `-be`) are TRUNCATION ARTIFACTS — re-derive the full URL.
9. **WEBSEARCH RESULTS ARE UNDATED — VERIFY EVERY SECTOR ITEM'S PUBLICATION DATE.** (Added 2026-05-29 after a production bug shipped a Network World article from APRIL as "past 24 hrs" Sector News.) WebSearch results have NO reliable publication timestamps. Search-result rank, "fresh-looking" URL slugs, and AI summary phrasing are NOT acceptable date evidence. EVERY sector news item must have its publication date directly verified by opening the URL in Chrome and reading the article's dateline before inclusion. See Step C.3.

## BULLET FORMAT (LOCKED — added 2026-05-29 for cross-sector consistency)

**Every `<li>` in Sector News, Ticker News, and Deals MUST follow this exact contract — no exceptions:**

```html
<li><a href="URL">Title</a> (Source, RELATIVE_TIME)</li>
```

Rules:
- **Title:** verbatim article headline (the link text). No editorial rewriting, no truncation, no trailing punctuation.
- **Source:** short publication name in parens (e.g., `Yahoo Finance`, `CoinDesk`, `Motley Fool`, `Reuters`, `Seeking Alpha`, `MarketBeat`, `GuruFocus`, `Simply Wall St`, `Investing.com`, `TipRanks`, `CoinGape`, `FierceBiotech`, `FreightWaves`). NO URL/domain. Comma after source.
- **Relative time:** the Google Finance `date_hint` compressed to `Nm ago` / `Nh ago` / `Nd ago` / `yesterday` / `today`. Examples: `10 minutes ago` → `10m ago`; `3 hours ago` → `3h ago`; `1 day ago` → `1d ago`; `22 hours ago` → `22h ago`. For Sector News (which uses Step C.3 parsely pub-dates), compute `hours_since_pub` and format the same way (`7h ago`, `19h ago`, etc.).
- **No blurbs.** No "—" + sentence after the parenthesis. No "What to know", no figures, no editorial characterization. The bullet ENDS at the closing `</li>`.
- **No absolute pub dates** like `(pub 2026-05-28)` or `(2026-05-28 18:53Z)`. Always relative.
- **No em-dash separator** between title and source. Use `(Source, time)` parens only.

Anti-patterns (REJECT in Step E audit):
- `<li>Title — Source. USAT market cap hit $140.8M...</li>` — em-dash + blurb
- `<li>Title — CoinDesk (pub 2026-05-28 18:53Z)</li>` — em-dash + absolute time
- `<li>Title — Source (3 hrs ago)</li>` — em-dash present, wrong separator
- `<li><a href="URL">Title</a> (Source)</li>` — relative time missing

This rule SUPERSEDES any conflicting placeholder language in Step D's template comments. Step E.10 audit MUST verify every bullet matches the locked contract or DROP/reformat.

## STEP A — Performance via Bloomberg get-price (PRIMARY); Yahoo is FALLBACK ONLY (rewritten 2026-06-05)

**KNOWN BUG TO PREVENT:** On 2026-06-05 the briefs shipped June 3 closes labeled as latest because Yahoo's chart API serves stale cached daily series pre-market — the prior session's bar can be missing entirely until mid-morning, and the old script silently anchored on whatever bar came last. Bloomberg (internal MCP tool `get-price`, BLPAPI-backed) is now PRIMARY. A stale close must NEVER ship silently.

### A.1 — Batch spot quote (anchor close + pre-market)

Call `get-price` ONCE with `tickers={{TICKERS_JS_ARRAY}}`. For each ticker store:
- `last_regular_close` → the **Close** column value (prior regular-session close, authoritative).
- `mid` (= (bid+ask)/2) → the **Pre-Mkt** column price. Pre-Mkt % = (mid / last_regular_close − 1) × 100, 2 decimals. At an ~8:15 AM run the response's `market_status` should be pre-market; if `mid` is null/absent, or a `_stale_warning` is present, render the Pre-Mkt cell as `—` instead of a bad number.

### A.2 — Historical series for lookbacks

For EACH ticker call `get-price` with `ticker=<T>`, `fields=["PX_LAST"]`, `start_date=<13 months before today, YYYY-MM-DD>`, `end_date=<today, YYYY-MM-DD>`. Parse the returned `history` CSV (`date,PX_LAST` rows). **DROP any row dated today** — that is the in-progress/pre-market session, never a close.

### A.3 — Compute returns

After dropping the today-row, the LAST remaining row is the anchor row. Cross-check: its PX_LAST must equal `last_regular_close` from A.1 within $0.02 (re-fetch once on mismatch; if still mismatched, treat the ticker as STALE per A.4). All returns computed vs `last_regular_close`:
- **1D** = vs the row before the anchor row. **1W** = vs 5 rows back.
- **1M / 6M / 1Y** = vs the last row on/before the same calendar date 1/6/12 months earlier.
- **YTD** = vs the final row of the prior calendar year.
- If a ticker IPO'd more recently than a lookback window, render `—` for unavailable windows.

### A.4 — FRESHNESS GATE (HARD — the fix for the 2026-06-05 stale-close incident)

Compute the **expected last trading day**: the most recent weekday before today (Mon → prior Fri); if that weekday was a US market holiday, step back one more business day. The anchor row's date MUST equal it. If it does not — or A.1/A.2 errored — the ticker is STALE → go to A.5. Use the verified anchor date for the table header "Close (M/D)"; with Bloomberg primary all tickers must share ONE anchor date.

### A.5 — FALLBACK CHAIN (only when Bloomberg errors or fails the gate)

1. Yahoo chart API via Chrome JS: `https://query1.finance.yahoo.com/v8/finance/chart/<T>?interval=1d&range=2y&_=<Date.now() cache-buster>`. Drop bars dated today; apply the SAME A.4 gate to the last remaining bar.
2. If the expected day's bar is missing but `meta.regularMarketTime` falls on the expected day (typical pre-market), use `meta.regularMarketPrice` as the anchor close.
3. Else scrape `https://finance.yahoo.com/quote/<T>/history/` and read the expected day's Close row (volume also available here if needed).
4. If ALL of the above fail: render the most recent close available with an explicit `(stale: M/D)` flag inside the cell and add a footer note naming the ticker. NEVER present a stale close as current — that is the exact failure this rewrite exists to prevent.

## STEP B — Google Finance per ticker (REQUIRED)

For EACH ticker, navigate to `https://www.google.com/finance/quote/<TICKER>:<EXCHANGE>` then scrape:

```javascript
window._scrapeResult = (() => {
  const out = [];
  const links = document.querySelectorAll('a[href*="://"]');
  for (const a of links) {
    const href = a.href;
    if (href.includes('google.com') || href.includes('about.google') || href.includes('/finance/')) continue;
    const txt = (a.innerText || '').trim();
    if (txt.length < 20 || txt.length > 300) continue;
    let p = a;
    for (let i = 0; i < 6 && p; i++) {
      p = p.parentElement;
      if (!p) break;
      const ft = p.innerText || '';
      const dm = ft.match(/(\d+\s*(minute|hour|day|week|month)s?\s+ago|yesterday|today|[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})/i);
      if (dm) { out.push({title: txt.slice(0,200), href, date_hint: dm[0]}); break; }
    }
  }
  return out.slice(0, 15);
})();
window._scrapeResult.length
```

For each ticker:
1. **24-HR CAP filter:** PASS only `N min/hours ago` / `today` / `yesterday`. DROP `2 days ago`+ or older absolute dates.
2. **Paywall filter:** DROP wsj/ft/barrons/bloomberg/nyt/theinformation/economist.
3. **Whitelist preference.**
4. Take **top 3** surviving items.
5. If <3, take what survives. If 0, render `<TICKER>: No news in past 24 hrs.`
6. Dedupe against Sector News.

**JS SCRAPER FALLBACK:** May return `undefined` on `/finance/beta/` variant, OR `[BLOCKED]`. Workaround: assign to `window._scrapeResult` and access via a second JS call. If still failing:
1. Use `get_page_text` for titles/sources/date hints.
2. For EACH article, WebSearch `"<6-8 words of title>" site:<source_domain>` for the URL.
3. Verify the URL's title matches; verify pub date is within 24 hrs.
4. If no match found, DROP — do NOT invent a URL.
5. Title-URL match verification: confirm title AND pub date match.

**URL EXTRACTION DISCIPLINE (MANDATORY):** Before placing URLs in body, dump full hrefs:
```javascript
window._scrapeResult.map((x,i) => i + '|' + x.date_hint + '|FULLHREF=' + x.href).join('\n')
```
Copy from THIS untruncated dump only.

**URL PATTERN BLACKLIST:**
- `marketwatch.com/data-news/*` — drop entirely (stub pages expire).
- `marketbeat.com/instant-alerts/filing-*` — accept ONLY if it is the only fresh ticker news AND the slug ends with `-YYYY-MM-DD/`.

## STEP C — Sector News via WebSearch (3-4 queries) — DATE VERIFICATION MANDATORY

### C.1 — Run the queries

{{WEBSEARCH_QUERIES_BLOCK}}

Collect ~10-15 URLs. Apply paywall/whitelist/unreliable filters to shrink to ~6-8 candidates.

### C.2 — IMPORTANT: WebSearch results have NO trustworthy date

(Added 2026-05-29 after a Network World article from APRIL shipped as "past 24 hrs" Sector News.)

WebSearch returns titles + URLs + an AI summary. **None of these prove pub date.**
- Search-result rank does NOT mean "recent."
- Recent-sounding URL slugs do NOT prove pub date.
- AI-summary phrasing is NOT verified.
- "Last updated" fields in WebSearch metadata are NOT reliable.

### C.3 — MANDATORY: Verify each candidate's pub date in Chrome

For EACH candidate:
1. Navigate Chrome to the URL.
2. Extract pub date:

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

3. Compute `hours_since_pub = (NOW - pub) / 3600000`.
4. **GATE:** include IF AND ONLY IF `hours_since_pub <= 24`. Otherwise drop.
5. If `value === null`, item is disqualified — drop. Do NOT fall back to WebSearch summary claims.
6. Sources that lack machine-readable dates should be dropped without retry.

### C.4 — Build the Sector News block

From verified candidates, pick top 4 by relevance. Record each item's verified pub date — Step E.6 will audit.

### C.5 — Fewer than 4 verified items

Re-run a more targeted WebSearch. Repeat C.3. If still <4, render only verified items with: `<em>Note: only N items passed 24-hr publication-date verification today.</em>` NEVER pad with stale items.

## STEP C+ — AI Analysis: Headline-Performance Synthesis (added 2026-06-05)

After Steps A-C complete (performance data + all headlines collected), synthesize them into a per-ticker "What Moved & Why" analysis. This section ties each ticker's 1D price move to specific headlines.

### C+.1 — Identify movers
Calibrate paragraph length to the size of the 1D move:
- **|1D| >= 2%:** Full paragraph with specific headline/catalyst linked to the move.
- **|1D| 0.5%–2%:** 1–2 sentences.
- **|1D| < 0.5%:** Single sentence ("TICKER was flat, no material news.").
- **Pre-market:** If a ticker shows >= 2% pre-market move with a clear catalyst from a headline, note it.

Order tickers by |1D| descending (biggest movers first).

### C+.2 — Headline sources for synthesis (paywalled ALLOWED here)
Draw from three pools:
1. **Headlines already collected** from Steps B (Google Finance) and C (WebSearch) that passed date verification.
2. **Additional targeted search for big movers** — if a ticker moved >= 2% but no collected headline explains it, run one additional WebSearch with NO domain blocking. Scoped to AI Analysis only.
3. **Paywalled sources** — headlines from wsj.com, ft.com, bloomberg.com, etc. Use headline text only, tag `(paywalled)`.

### C+.3 — Synthesis rules
- **Ground every claim in a specific headline.** Never write "likely due to market conditions" without a linked headline.
- **No hallucinated causation.** If no headline explains a move: "TICKER was down X.X% — no specific catalyst identified in today's news."
- **No jargon padding.** Keep sentences tight.
- **Adaptive length is mandatory.** A 0.3% move does not get the same treatment as a 5% move.

### C+.4 — Honesty policy
If headlines exist but do NOT clearly explain a move, say so. Intellectual honesty > forced narrative.

## STEP D — Compose HTML

**ORDER (canonical, updated 2026-06-05 — Performance on top, AI Analysis second, News below):**
1. `<h2>` sector header
2. Date line
3. **Performance** table
4. **AI Analysis — What Moved & Why** (added 2026-06-05)
5. **Sector News** (past 24 hrs)
6. **Ticker News** (past 24 hrs)
7. **New-ticker flags**
8. **Deals** (past 24 hrs)
9. Footer

This order was made canonical on 2026-06-03 based on the most recently fired live brief (`meteora-consumer-disc-brief`, last run 2026-06-03T12:05:23Z). DO NOT revert to News-on-top — Lukas explicitly redesigned the layout because the performance table is the highest-signal block and should be visible without scrolling.

```html
<!DOCTYPE html><html><body style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif; color:#222; line-height:1.45; font-size:14px; max-width:780px;">
<h2 style="margin:0 0 4px 0;">{{SECTOR_NAME}} — Meteora Daily</h2>
<p style="color:#666; margin:0 0 16px 0; font-size:13px;">{TODAY_HUMAN} · {{TICKER_COUNT}} tickers tracked</p>
<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:16px;">Performance</h3>
<table style="border-collapse:collapse; font-size:13px;">
<thead><tr style="background:#f4f4f4;">
  <th style="border:1px solid #ccc; padding:6px 10px; text-align:left;">Ticker</th>
  <th style="border:1px solid #ccc; padding:6px 10px;">Close ({ANCHOR_M_D})</th>
  <th style="border:1px solid #ccc; padding:6px 10px;">Pre-Mkt</th>
  <th style="border:1px solid #ccc; padding:6px 10px;">1D</th><th style="border:1px solid #ccc; padding:6px 10px;">1W</th><th style="border:1px solid #ccc; padding:6px 10px;">1M</th><th style="border:1px solid #ccc; padding:6px 10px;">6M</th><th style="border:1px solid #ccc; padding:6px 10px;">YTD</th><th style="border:1px solid #ccc; padding:6px 10px;">1Y</th>
</tr></thead>
<tbody><!-- one <tr> per ticker, color positive #080, negative #c00. Pre-Mkt cell format: $X.XX (+N.NN%) or $X.XX (-N.NN%), colored by sign; render — if no pre-market quote --></tbody>
</table>
<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">AI Analysis — What Moved &amp; Why</h3>
<div style="font-size:13px; line-height:1.5; color:#333;">
<!-- One <p> per ticker, ordered by |1D| descending. Format: <p><b>TICKER (±X.X%):</b> Narrative linking 1D move to specific headlines. Tag paywalled with (paywalled). Adaptive length per Step C+.1.</p> -->
</div>
<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">Sector News (past 24 hrs)</h3>
<ul><!-- 4 items in LOCKED BULLET FORMAT: <li><a href="URL">Title</a> (Source, RELATIVE_TIME)</li> --></ul>
<p style="color:#888; font-size:12px;"><em>Filter note: {N_DROPPED} candidate items dropped (stale, paywalled, or unreliable source).</em></p>
<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">Ticker News (past 24 hrs)</h3>
<p style="color:#666; font-size:12px;"><em>Top 3 dated cards per ticker; whitelisted free sources prioritized.</em></p>
<p style="margin:0 0 4px 0;"><b>{TICKER}:</b></p>
<ul style="margin-top:0;"><!-- 3 items in LOCKED BULLET FORMAT --></ul>
<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">New-ticker flags</h3>
<p style="color:#666;">{NEW_TICKER_NOTES_OR_NONE}</p>
<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px; color:#666;">Deals (past 24 hrs)</h3>
<!-- <ul> with deal items in LOCKED BULLET FORMAT, or <p><em>No deal news in past 24 hrs.</em></p> -->
<hr style="margin-top:22px; border:none; border-top:1px solid #ddd;">
<p style="color:#888; font-size:11px;">Window: past 24 hours · cutoff: {CUTOFF_ISO} · scheduled delivery: 9:00 AM ET · sources: whitelisted free publishers (paywalled DROPPED) · perf source: Bloomberg get-price (BLPAPI); Yahoo fallback only</p>
</body></html>
```

## STEP E — Pre-send audit
1. Every news/deal item has `<a href`.
2. **No paywalled domains** anywhere.
3. Table cells have `border:1px solid #ccc`. Colors `#080`/`#c00`.
4. Subject uses TODAY_SHORT and starts with the `[TEST] ` prefix (test phase, flipped 2026-06-05).
5. **URL provenance audit:** every URL must be tool-returned. Constructed/guessed URLs → re-derive via WebSearch or DROP.
6. **Date cross-check (Ticker News):** for `get_page_text` fallbacks, verify WebSearch result date is within 24 hrs.
7. **URL COMPLETENESS CHECK:** slugs ending mid-word (`-g`, `-dru`, `-pcs`, `-pipel`, `-be`) without clean terminators are TRUNCATION ARTIFACTS — re-read raw `href` and replace with FULL URL. If unrecoverable, DROP.
8. **URL PATTERN BLACKLIST CHECK:** drop `marketwatch.com/data-news/...`; for `marketbeat.com/instant-alerts/filing-...` require date suffix `-YYYY-MM-DD/`.
9. **SECTOR NEWS PUB-DATE PROVENANCE AUDIT (MANDATORY, added 2026-05-29):** For EVERY item in the Sector News block, confirm there is a recorded verified pub date from Step C.3 within the past 24 hours, extracted via `meta[property="article:published_time"]`, `<time datetime>`, or JSON-LD `datePublished`. If you cannot point to a specific verified pub date — STOP and re-verify, or DROP. WebSearch rank, recent-looking slugs, and AI summary phrasing are NOT acceptable substitutes. This audit is as important as the Step 0d weekday check.
10. **BULLET FORMAT AUDIT (MANDATORY, added 2026-05-29):** Every `<li>` in Sector News, Ticker News, and Deals MUST match the LOCKED contract `<li><a href="URL">Title</a> (Source, RELATIVE_TIME)</li>`. Reject and reformat any bullet that uses em-dash separators (`Title — Source`), absolute pub dates (`pub 2026-05-28`), trailing prose/blurbs after the parens, or missing a relative-time field.
11. **Footer cutoff sanity check:** confirm footer `cutoff_iso` matches Step 0a output exactly.
12. **ANCHOR FRESHNESS AUDIT (MANDATORY, added 2026-06-05):** For EVERY ticker, the Close anchor date must equal the expected last trading day computed in Step A.4, OR the cell must carry an explicit `(stale: M/D)` flag with a footer note. Spot-check at least one ticker's Close against `last_regular_close` from Step A.1. Confirm Pre-Mkt column cells are either a quote with signed % or `—`.
13. **AI ANALYSIS AUDIT (MANDATORY, added 2026-06-05):** For every claim in the AI Analysis section, verify there is a cited headline link. No unsourced assertions of causation. Paywalled sources must carry the `(paywalled)` tag. 1D return percentages in the AI Analysis must match the Performance table exactly. Pre-market callouts (if any) must match the Pre-Mkt column. If a ticker paragraph says "no catalyst identified," confirm no relevant headline was found in Steps B/C/C+.2. Drop any paragraph that fabricates causation without a linked headline.

## STEP F — Schedule Stage 1 for 9 AM

1. `whoami` returns chauhan_intern (sender mailbox unchanged). If not, ABORT.
2. `draft_email(to=["AI_Interns@meteoracapital.com"], html=true, subject="[TEST] [{{SECTOR_NAME}}] Meteora Daily - ${{TODAY_SHORT}}", body=<HTML>, send_at=SEND_AT_ISO)`.
3. `send_email(..., confirmed=true, send_at=SEND_AT_ISO)`. NOTE: if `send_email` returns "Refusing to send: no prior draft found," the draft expired — re-issue `draft_email` and `send_email` back-to-back.
4. Store body+subject for Stage 2.

## STAGE 2 APPROVAL GATE (CONFIRMATION REQUIRED — changed 2026-06-05)

`AskUserQuestion`: "{{SECTOR_NAME}} brief queued for 9 AM delivery to AI_Interns. Send same email to filings@ now?" Options: `Yes — send to filings@` / `No — hold`.
On Yes: send to `filings@meteoracapital.com` with `send_at=null`. On No: report held.

**Scheduled-run mode:** if running autonomously with no user present, Stage 2 must be HELD by default — NEVER send to filings@ without explicit chat-side approval.

## LOCKS
Stage 1: `["AI_Interns@meteoracapital.com"]`, send_at=SEND_AT_ISO (9:00 AM ET). Stage 2: `["filings@meteoracapital.com"]`, send_at=null, ONLY after explicit user confirmation. Subject `[TEST] [{{SECTOR_NAME}}] Meteora Daily - {{TODAY_SHORT}}` — [TEST] prefix REQUIRED during current test phase. 24-hr cap. Whitelist enforced. Sector-news pub-date verification enforced (Step C.3 + Step E.6). Bullet format enforced (Step E.8). Perf source: Bloomberg get-price primary with HARD freshness gate (Step A.4) + anchor audit (Step E.12). AI Analysis headline-performance synthesis enforced (Step C+ + Step E.13, added 2026-06-05).