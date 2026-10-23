---
name: sector-watch
description: Meteora's daily sector watch — SPAC / event-arbitrage focused. Every weekday this skill iterates through every ACTIVE sector in keywords.md and sends ONE email per sector (N active sectors = N emails per weekday). Paused sectors (heading prefixed [PAUSED]) are skipped. For each sector: runs bdata search news for sector keywords AND for sector+deal-keyword combinations over the past 48 hours (HARD CAP, no exceptions), dedupes URLs against the past 7 days, pulls 1D/1W/1M/6M/YTD/1Y Yahoo Finance perf per ticker via Chrome, composes News headlines + perf table + AI Analysis (headline-performance synthesis) + per-ticker briefs + ticker flags + Deals (in that order — NO narrative paragraph), sends via send-as-me. Subject format: [Sector] Meteora Daily - Date (with [TEST] prefix in test_mode). Trigger on 'run the sector watch', 'send today's sector emails'. Always use this skill for the daily workflow. Dry-run preview is default; sending needs approval.
---

# Sector Watch (Meteora — Daily, Single-Sector)

Meteora's daily sector brief. **One email per weekday, one sector per email.**
The skill rotates through the sectors listed in `keywords.md` on a Mon-Fri
cycle (with N sectors, the full rotation completes every N weekdays).
Weekends are skipped by default.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  sector-watch (THIS skill)                                          │
│                                                                     │
│  pick today's sector (Mon-Fri rotation via pick_sector.py)          │
│   → run bdata search --type news for that sector's keywords         │
│   → scrape top article bodies                                       │
│   → pull 1D/1W/1M/6M/YTD/1Y Yahoo Finance perf for each ticker          │
│   → flag newly-mentioned tickers not in the universe                │
│   → compose News + perf + AI Analysis + briefs + flags + Deals      │
│   → call send-as-me's draft_email → preview → send_email            │
└─────────────────────────────────────────────────────────────────────┘
              │                                  │
              ▼                                  ▼
     ┌────────────────────┐         ┌──────────────────────┐
     │ brightdata-plugin  │         │ send-as-me plugin    │
     │ (bdata search,     │         │ (configure, sign_in, │
     │  bdata scrape)     │         │  draft_email,        │
     │                    │         │  send_email)         │
     └────────────────────┘         └──────────────────────┘
```

## Required prerequisites

1. **brightdata-plugin** installed and `bdata login` complete.
2. **send-as-me plugin** installed and `configure(email='...')` + `sign_in`
   complete. While `config.test_mode = true`, configure as
   `chauhan_intern@meteoracapital.com`.

The skill aborts cleanly with a clear error if either prerequisite is missing
at run time.

## Files in this skill

```
sector-watch/
├── SKILL.md                          ← you are here
├── keywords.md                       ← user-editable sector → tickers + keywords doc
├── config.json                       ← committed, non-secret settings (rotation, sender, recipient, etc)
├── config.local.example.json         ← template for secrets (rename to .local.json and edit)
└── scripts/
    ├── parse_keywords.py             ← keywords.md → structured JSON
    ├── pick_sector.py                ← compute today's sector from day-of-week
    ├── yahoo_perf.js                 ← Yahoo Finance perf snippet (paste into Chrome javascript_tool)
    └── run_sector_watch.sh           ← orchestrator (pick → news → scrape → perf → merge)
```

## How the daily rotation works

Each weekday runs ONE sector, advancing through `keywords.md` in order:

```
anchor_date = 2026-05-18 (Mon)  ← from config.json

Mon May 18  → sectors[0]   (first sector in keywords.md)
Tue May 19  → sectors[1]
Wed May 20  → sectors[2]
Thu May 21  → sectors[3]
Fri May 22  → sectors[4]
Mon May 25  → sectors[5]   ← if 6 sectors, this is the 6th
Tue May 26  → sectors[0]   ← cycle wraps
... and so on
```

To change which sector runs on which day, **reorder the `## ` headings in
`keywords.md`**. Add a new sector → it joins the rotation in its position.
Add a sector at position N+1 with N existing sectors → rotation extends to
N+1 weekdays and phase-shifts naturally.

Weekend behavior is controlled by `config.schedule.fallback_behavior`:
- `"skip"` (default) → no-op, "no sector scheduled today"
- `"run_next"` → run next Monday's sector
- `"last_weekday"` → re-run most recent Friday's sector

> **Test mode (current default).** `config.json` ships with `test_mode: true`,
> `sender.expected_email` and `recipient.to` both set to
> `chauhan_intern@meteoracapital.com`. Sends are self-loops, subject is
> prefixed `[TEST] `. To graduate to production: flip `test_mode` to `false`,
> update `sender.expected_email` and `recipient.to` in config.json, run
> `configure(email='<new sender>')` on send-as-me.

## HARD 48-HOUR CAP — RIGID, NON-NEGOTIABLE (READ FIRST)

**Every item in the News list AND every item in the Deals list MUST be
verifiably dated within the past 48 hours of run time. Zero exceptions.
Zero "but this is important" overrides. Zero soft-recency assumptions.**

This is the most-violated rule in the skill's history and the user has
explicitly flagged it twice as a critical failure. **If you find yourself
even considering including an item without a verified timestamp, STOP and
DROP IT.**

### Step 1 — Compute the cutoff explicitly at run start

Before searching for ANY news, compute and write down the cutoff:

```
NOW_UTC    = current UTC timestamp at start of this run
CUTOFF_UTC = NOW_UTC − 48 hours        # ISO 8601, e.g. "2026-05-24T14:30:00Z"
```

Surface CUTOFF_UTC in your working notes. Every item you consider for the
email must have a publication timestamp **≥ CUTOFF_UTC**. Items at
`CUTOFF_UTC − 1 second` are stale and dropped. No fuzz, no rounding.

### Step 2 — Per-item verification (MANDATORY, every item, no exceptions)

For EVERY candidate news/deal item — before it enters any draft of the
email body — execute this verification chain in order. Stop at the first
PASS or DROP.

1. **Snippet-date check.** Read the WebSearch / bdata search snippet for an
   explicit date. Accepted formats: `"4 hours ago"`, `"yesterday"`,
   `"May 25, 2026"`, `"2026-05-25"`, `"5/25/2026"`. Convert to a UTC
   timestamp. If `timestamp ≥ CUTOFF_UTC` → **PASS** (keep). If
   `timestamp < CUTOFF_UTC` → **DROP** (do not even fetch the article).

2. **If no date in snippet, fetch the article.** Use
   `mcp__workspace__web_fetch <url>` (or Chrome `get_page_text`) and search
   the rendered HTML for any of: a `<time datetime="...">` element, a
   `<meta property="article:published_time">` tag, an `og:published_time`
   meta, a `pubdate` attribute, or a visible byline date (e.g.
   `"Published: May 25, 2026"`). Convert to UTC. If
   `timestamp ≥ CUTOFF_UTC` → **PASS**. If older → **DROP**.

3. **If the article fetch returns NO determinable date** (no `<time>` tag,
   no meta, no visible byline date) → **DROP**. Do not guess. Do not assume
   "the URL has /2026/05/25/ in it so probably May 25" — URL slugs are not
   sufficient evidence. **DROP**.

4. **If the fetch itself fails** (404, blocked, timeout, JS-only) → **DROP**.
   Don't fall back to the snippet text alone. **DROP**.

**Quotable summary, paste into your draft when in doubt:** *"No verified
timestamp ≥ CUTOFF → DROP. Period."*

### Step 3 — Bias search queries toward recency

To minimize verification failures downstream, bias EVERY search query for
this skill toward the past 48 hours at query construction time:

- ✅ **Include the actual date in the query**: `"<sector> news May 25 2026"`,
  `"<sector> news May 26 2026"` (use yesterday's and today's dates).
- ✅ **Use recency-coded phrasing**: `"<sector> news today"`,
  `"<company> announced this week"`, `"<sector> deal yesterday"`.
- ✅ **Use WebSearch's date filter when available** — `WebSearch` accepts
  `after:YYYY-MM-DD` syntax in the query. Use `after:CUTOFF_DATE` to
  pre-filter at search time.
- ❌ **Never** use evergreen-flavored queries: `"<sector> M&A wave"`,
  `"<sector> trends"`, `"<sector> outlook 2026"`. These pull months-old
  articles that waste your verification budget.
- ❌ **Never** trust the SERP order as a freshness signal. SERPs rank by
  relevance, not date.

### Step 4 — Hard floor on the email body

After verification:

- If the verified-fresh news array is non-empty → render the headlines in
  the News section.
- If the verified-fresh news array is **empty** → render exactly:
  `No major updates in the last 48 hrs.` This is the ONLY acceptable
  empty-state response. Do NOT pad with stale items "for context." Do NOT
  add older items in a "background" callout. **The empty state IS the
  message.**

Same rule for Deals: empty → `No deal news in past 48 hrs.` and that's it.

### Step 5 — Audit line in the email footer (REQUIRED)

Every email MUST include this footer line confirming the cap was applied:

```
Window: past 48 hours · cutoff: <CUTOFF_UTC ISO> · N news kept, K dropped as stale · M deals kept, L dropped as stale
```

The `K` and `L` numbers are non-zero in almost every real run — that's the
point of the verification gate. A run that reports `K=0, L=0` against a
WebSearch that returned ≥5 results is suspicious — re-verify.

### Why this rule is rigid

Two prior failure modes the user has explicitly called out:

1. **May 22 automation test**: included articles dated May 4, May 7, May 12,
   May 13 — when the run was on May 22. That's 9-18 days stale, treated as
   "fresh" by the agent because the dates weren't checked. Critical failure.
2. **May 26 morning test**: agent included items from "earlier in May"
   when the cutoff was May 24. Soft-recency creep. Critical failure.

The user has said this needs to be a "hard hard cap." That means: if you
ever find yourself writing the sentence "this item is older than 48 hours
but I'm including it because..." — **STOP. DROP IT. Either ship the
sparse email, or don't ship.** Stale items rot the entire signal value of
the brief.

There is no narrative paragraph in this skill (retired May 26, 2026) and
therefore NO escape valve for older context. The headlines are the brief.
(Note: the AI Analysis section added 2026-06-05 is NOT a narrative paragraph — it is a structured, per-ticker synthesis that ties specific headlines to 1D price moves. It does not reintroduce freeform narrative.)


## AI Analysis — Headline-Performance Synthesis (added 2026-06-05)

After collecting news headlines (Step 4) and ticker performance (Yahoo perf), synthesize them into a short "AI Analysis — What Moved & Why" block in the email. This section ties each ticker's 1D price move to specific headlines collected during the news-gathering phase, giving the reader an instant explanation of why each name moved.

### Paywalled sources — ALLOWED for AI Analysis only

Paywalled sources (wsj.com, ft.com, barrons.com, bloomberg.com, nytimes.com, theinformation.com, economist.com) are **allowed** in the AI Analysis section. Rules:
- Use **headline text only** (as it appears in search results). Do not quote paywalled article body text.
- Tag every paywalled citation with `(paywalled)` in the email HTML.
- Paywalled sources remain **banned** from the News headlines, per-ticker briefs, and Deals sections.

### Identify movers — adaptive depth by |1D| magnitude

For each ticker in the sector, calibrate paragraph length to the size of the move:
- **|1D| >= 2%**: Full paragraph with specific headline/catalyst linked to the move.
- **|1D| 0.5%–2%**: 1–2 sentences.
- **|1D| < 0.5%**: Single sentence ("XYZ was flat, no material news.").
- **Pre-market**: If a ticker has a >= 2% pre-market move with a clear catalyst from a headline, note it.

Order tickers by |1D| descending (biggest movers first).

### Headline sources for synthesis

Draw from three pools:
1. **Headlines already collected** — the news items from bdata search / WebSearch that passed the 48-hour verification gate.
2. **Additional targeted search for big movers** — if a ticker moved >= 2% but no collected headline explains it, run one additional `WebSearch("<TICKER> news today <DATE>")` with no domain blocking. This extra search is scoped to AI Analysis only; results do not flow into the News or Deals sections.
3. **Paywalled sources** — headlines from wsj.com, ft.com, bloomberg.com, etc. that appear in search results. Use headline text only, tag `(paywalled)`.

### Synthesis rules

- **Ground every claim in a specific headline.** Never write "likely due to market conditions" or similar vague causation without a linked headline.
- **No hallucinated causation.** If no headline explains a move, say so: "TICKER was down X.X% — no specific catalyst identified in today's news."
- **No jargon padding.** Keep sentences tight. If there's not much to say, don't force a paragraph.
- **Adaptive length is mandatory.** A 0.3% move does not get the same treatment as a 5% move.
- **1D% in AI Analysis must match the perf table.** If the perf table says -2.1%, the AI Analysis paragraph must say -2.1%, not -2.0% or "about 2%".

### HTML placement in the email

Insert the AI Analysis block **after the performance table** and **before the per-ticker briefs**. Use this HTML structure:

```html
<h3 style="border-bottom:1px solid #ddd; padding-bottom:4px; margin-top:18px;">AI Analysis — What Moved &amp; Why</h3>
<div style="font-size:13px; line-height:1.5; color:#333;">
<!-- One <p> per ticker, ordered by |1D| descending -->
<p><strong>TICKER</strong> was down X.X% — [explanation grounded in headline]. <a href="URL">Source</a></p>
<p><strong>TICKER2</strong> was up X.X% — [explanation]. <a href="URL">Source</a> <span style="color:#888;">(paywalled)</span></p>
</div>
```

### Audit check for AI Analysis

Before sending, verify:
- Every `<p>` in the AI Analysis block cites at least one headline with a working link.
- Every paywalled citation is tagged `(paywalled)`.
- Every 1D% figure matches the perf table exactly.
- Pre-market context (if included) is consistent with the perf table anchor.
- No paragraph fabricates causation without a linked headline.

## Setup gate (run first)

```bash
if ! command -v bdata >/dev/null 2>&1; then
    echo "bdata CLI not installed — install brightdata-plugin first, then: bdata login"
    exit 1
elif ! bdata zones >/dev/null 2>&1; then
    echo "bdata not authenticated — run: bdata login"
    exit 1
fi
```

send-as-me readiness is checked lazily at send time (see "Sending" below).

## Data source fallback chain

The pipeline has TWO data sources (news + ticker performance). Each has a primary path and ordered fallbacks. Use whichever works in this session — log which path was used in the preview so the user knows.

### News (per sector, past 7 days)

1. **`bdata search --type news`** (primary) — Bright Data CLI on the user's machine. The runner script (`scripts/run_sector_watch.sh`) defaults to this. Requires the brightdata-plugin to be installed and `bdata login` to have been completed.
2. **`WebSearch`** (fallback) — Anthropic's built-in web search tool. Use when `bdata` is unavailable (sandbox without the CLI, MCP disconnected, etc.) or returns errors. Call it once per keyword phrase. Tradeoffs: fewer results per call, no `--type news` filter, but works from any Claude session.
3. **`mcp__Claude_in_Chrome__navigate` + `get_page_text`** (final fallback) — drive a real browser to fetch news index pages (e.g., Google News search results, source-specific feeds). Use when both above fail or when a specific JS-rendered news site is needed. Slowest path; reserve for when news really matters and the other paths failed.

### Article bodies (top 3 items per sector)

1. **`bdata scrape <url> -f markdown`** (primary).
2. **`mcp__workspace__web_fetch <url>`** (fallback) — fetches static HTML; works for most news sites that aren't fully client-rendered.
3. **`mcp__Claude_in_Chrome__navigate` + `get_page_text`** (final) — for JS-heavy sites that web_fetch can't render.

If all three fail for a given URL, **the item must still pass the Step 2 timestamp verification above**. If the date can't be confirmed without the body, DROP IT — do not include the headline alone with an unverifiable date.

### Ticker performance (1D / 1W / 1M / 6M / YTD / 1Y)

**HARD RULE 1 — web sources only. NEVER use `mcp__37e4df80-...__get-price` (Meteora's Bloomberg MCP) for this skill.** Portability requirement — the skill must work for any user, not just those with Meteora's internal data access.

**HARD RULE 2 — NEVER use yfinance, the Python `yfinance` library, or any pip-installed market-data package.** Validated May 26, 2026: PyPI is blocked at the Cowork sandbox proxy and yfinance cannot be installed; sandbox bash also cannot reach `query1.finance.yahoo.com` directly (proxy returns 403). The Chrome path below is the ONLY documented price source.

**The one and only path: Claude-in-Chrome `javascript_tool` → Yahoo chart JSON endpoint.** Validated end-to-end on May 26, 2026 across Autonomous Trucking, Crypto/Stablecoins, and Healthcare sectors with cross-checks against Yahoo's `range=5d` published values.

**Recipe (all tickers in a single batch):**

```
1. mcp__Claude_in_Chrome__list_connected_browsers       — find an available browser
2. mcp__Claude_in_Chrome__select_browser(deviceId)      — pick it
3. mcp__Claude_in_Chrome__tabs_context_mcp(createIfEmpty=true)
4. Paste the full contents of scripts/yahoo_perf.js into
   mcp__Claude_in_Chrome__javascript_tool, with the tickers array
   interpolated at the top. The script:
     a. fetch()s https://query1.finance.yahoo.com/v8/finance/chart/<T>?interval=1d&range=2y
        for each ticker (runs inside the browser, so it bypasses sandbox
        proxy restrictions).
     b. Parses the JSON, computes 1D/1W/1M/6M/YTD/1Y per the canonical math.
     c. Assigns the JSON-stringified result to window._perfResult.
5. Poll window._perfResult with a follow-up javascript_tool call until
   defined; parse it.
6. (Optional sanity-check, recommended for every run) re-fetch with
   range=5d and verify that closes[-2]/closes[-3]-1 matches the 1D you
   just computed for each ticker. If they don't match, your indexing is
   off.
```

The script is small (~70 lines of JS) and lives at `scripts/yahoo_perf.js`. The browser is the runtime — no Python, no Node, no pip.

**Range: ALWAYS use `range=2y`, not `range=1y`.** Validated May 26: `range=1y` returns ~251 closes starting just *after* the calendar-1Y-ago date, so the calendar-anchored 1Y lookback fails and falls back to "earliest available," producing a `*` partial-window flag for every ticker. `range=2y` returns ~500 closes, the 1Y lookback resolves exactly to `anchor_date − 1 calendar year`, and asterisks disappear except for tickers with genuinely <1Y of trading history (recent IPOs).

**Anchor: `closes[-1]` (the most recent close Yahoo reports — same value shown in the quote-page header).** This is the Yahoo-aligned anchor, reverse-engineered May 26, 2026 (PM): SBUX 1D/6M/1Y all replicated their published pills EXACTLY (-1.64% / +16.98% / +20.17%) only with this anchor. Behavior across session states:
- **After close**: `closes[-1]` = today's settled close (stable, matches Yahoo's "At close" header).
- **Pre-market**: `closes[-1]` = prior trading day's close (stable, matches the Yahoo header pre-open).
- **Mid-session**: `closes[-1]` = live intraday quote (moves with the tape; perf will shift through the day but will always match what Yahoo shows AT THAT MOMENT).

For a morning briefing sent 6-9 AM ET (pre-market), `closes[-1]` is the prior trading day's close — stable and Yahoo-aligned.

**Series: RAW `close` array, NOT `adjclose`.** Yahoo's published pills are PRICE return (raw close-to-close), not total return. Using `adjclose` introduces a ~2-3% upward drift for typical dividend payers (SBUX example: adjclose 1Y gave +26.03% vs raw close +20.17% — the 2.4% dividend yield × 1Y compounded explains most of the gap). The Yahoo chart line itself is plotted on raw close, so the pills are internally consistent.

**Math (CANONICAL — Yahoo quote-page-aligned, validated May 26, 2026 PM):**

```
anchor_idx  = closes.length - 1          # today's close (or live intraday)
anchor      = closes[anchor_idx]
anchor_ts   = timestamps[anchor_idx]     # Unix seconds (RAW close, not adjclose)

# 1D / 1W — trading-day-based. No calendar ambiguity for short windows.
1D  = anchor / closes[anchor_idx - 1] - 1     # vs prior trading day
1W  = anchor / closes[anchor_idx - 5] - 1     # vs 5 trading days back

# 1M / 6M / 1Y — calendar-based: most-recent close on OR BEFORE
# (anchor_date - N calendar months/years). Walk backward from
# (anchor_idx - 1) until timestamps[i] <= target_ts.
#
# CRITICAL — target MUST be set to end-of-UTC-day (setUTCHours(23,59,59))
# before comparison. Without this, the DST shift between May (EDT, UTC-4)
# and Nov (EST, UTC-5) puts the target one hour BEFORE the recorded Nov
# close timestamp, causing on-or-before to skip the correct target day.
# Symptom: SBUX 6M reported +18.05% instead of Yahoo's +16.98% (denominator
# was Nov 25 close instead of Nov 26).
1M  = anchor / lookback_calendar(months=1)  - 1
6M  = anchor / lookback_calendar(months=6)  - 1
1Y  = anchor / lookback_calendar(years=1)   - 1

# YTD — Dec 31 PRIOR-YEAR close (NOT Jan 2 of current year).
# Walk backward from (anchor_idx-1) until you hit a timestamp whose
# UTC year equals current_year - 1; that's the Dec 31 close.
YTD = anchor / dec31_prior_year_close - 1
```

**Validation gate (every run):** compute SBUX (or any liquid name with stable Yahoo coverage) and visually compare 1D / 6M / YTD / 1Y against the Yahoo quote page (`finance.yahoo.com/quote/<TICKER>/`). If any pill differs by more than 0.1pp, the math has drifted — debug before sending the email.

**Cross-check protocol** (run once per sector before drafting the email): re-fetch each ticker via Chrome with `range=5d` and verify your computed 1D equals `closes[-2] / closes[-3] - 1` from the 5d data. If they don't match, your indexing is wrong. Validated May 26: all 14 ticker 1Ds matched their 5d-range references exactly across three sector tests.

**Symbol normalization (auto-applied by the script):** Yahoo's canonical form for class shares is dash, not dot. The script auto-converts `BRK.B → BRK-B`, `BF.B → BF-B`, `RDS.A → RDS-A`, etc. Either form is fine in `keywords.md`.

**Edge cases the hardened script handles (validated May 26, 2026 — 18/18 stress-test pass):**

| Edge case | Behavior |
|---|---|
| Mega-cap with splits (NVDA) | adjclose-aware, splits transparent |
| Recent IPO <1Y (CRCL, KDK) | computes full table; `1Y_partial: true` |
| Class-share dot variant (BRK.B, BF.B) | auto-normalized to dash form |
| Index symbol (^GSPC, ^IXIC) | URL-encoded caret, works clean |
| ETF (SPY, IBIT) | identical handling to equities |
| Foreign ADR (ASML, BABA) | identical handling, USD-denominated |
| Crypto pair (BTC-USD) | 731 closes (weekend trading included) |
| Bad symbol / typo (ZZZZZZZ, TSLAA) | clean `ok: false, error: "HTTP 404"` |
| Yahoo returns 200 + `chart.error` | detected, surfaced as `ok: false` |
| Transient 5xx / network failure | single retry with 1s backoff |
| Fewer than 2 valid closes | falls back to `regularMarketPrice`, marks `ok: 'partial'` |

### NO n/a-SPAM EMAIL RULE — failure handling for perf

**An email filled with `n/a` rows looks bad and erodes trust.** When the perf JSON has any ticker with `ok: false` or `ok: 'partial'`, follow this escalation:

1. **First, double-check the symbol.** Look in `keywords.md` for the ticker as the user wrote it. If it has a dot (`BRK.B`), the script already normalized — that's not the issue. If it's a typo (e.g. `TSLAA` instead of `TSLA`), surface the error to the user in chat and ask which symbol they meant. **DO NOT send an email with `n/a` for a fixable typo.**

2. **Second, retry the fetch.** A single transient failure can fail the first call. Re-run the script for just the failing tickers after a 5–10 second pause. The script itself does one in-built retry on 5xx; this is a second-level retry from the agent layer.

3. **Third, if it STILL fails**, decide based on failure count:
   - **1 ticker failed, ≥4 succeeded** → drop the failing ticker entirely. Add a footnote below the perf table: `* <ticker> excluded: Yahoo data unavailable today.` The table has NO `n/a` row.
   - **2+ tickers failed** → STOP. Surface to the user. Likely a Yahoo outage or symbol-mapping issue affecting the whole sector. Don't ship a half-broken email; resolve symbols or skip the sector for the day.
   - **Entire sector failed** → don't send the email. Report to user, wait for guidance.

4. **`ok: 'partial'` (brand-new IPO, <2 closes)** → exclude the ticker from the perf table; mention it in the New-ticker flags section as a recent listing not yet ready for perf tracking.

5. **`1Y_partial: true` (ticker has <1Y history but >50 closes)** → this is NORMAL for recent IPOs (CRCL, KDK). Render the FULL perf table with `+X.X%*` in the 1Y cell and a single footnote: `* 1Y window uses earliest available close (<date>) — ticker has <1 year of trading history.` This is NOT an "n/a-spam" case.

**Principle:** an email with NO perf table is better than an email with a perf table full of `n/a`. If perf data isn't trustworthy across the sector, render a single line: `Performance data unavailable today — Yahoo chart endpoint failed for <N> of <M> tickers. Will retry on next run.` and proceed with News + Deals only. Never blast a table of dashes — it makes the brief look unmaintained.

### Forbidden price sources for this skill

- `mcp__37e4df80-c7f5-4e0e-b4c4-c93e0ee1e885__get-price` (Meteora Bloomberg MCP) — Meteora-internal, not portable.
- yfinance / any pip-installed market-data package — PyPI blocked at sandbox proxy (validated May 26, 2026).
- urllib / requests / curl from sandbox bash to `query1.finance.yahoo.com` — proxy returns 403 (validated May 26).
- `mcp__workspace__web_fetch` for the chart endpoint — provenance issues, returns cached/stale data.
- `WebSearch` (Google SERP price widget) for perf — single coarse % change, unreliable timeframes.
- Any paid market data API that not every recipient of this skill would have access to.

The Chrome→Yahoo path is the only one that survives portability + sandbox-proxy + freshness checks.

### Which path the runner uses

The runner script (`scripts/run_sector_watch.sh`) hardcodes the primary path (bdata + Yahoo) because those are designed for hands-off scheduled runs on the user's laptop. **Fallback paths are for ad-hoc dry-runs invoked from a chat session** where the script may not be runnable. In an ad-hoc dry-run:

- Don't try to invoke the script; gather the data via the fallback tools directly.
- Compose the same email body the script would have produced.
- Tell the user which fallback path you used and why.

When `bdata` IS available on the calling machine, always prefer it over the fallback chain — the bdata results are more comprehensive (news vertical, full bodies, structured) and don't burn LLM context on parsing snippets.

## How to add, remove, or pause a sector

This is the most common change you'll make. The keywords.md file IS the
single source of truth — edit it and the next run picks up the change.
**The skill does NOT need to be reinstalled** when keywords.md changes.

**To add a sector** (e.g., "Defense Technology"):
1. Open `skills/sector-watch/keywords.md`.
2. Insert a new `## Defense Technology` heading anywhere.
3. Populate `### Keywords` at minimum. `### Tickers` and `### Notes`
   optional but recommended.
4. Save. The rotation extends by one weekday automatically.

**To pause a sector** (keep in file but skip rotation): prefix the heading
with `[PAUSED] ` — e.g. `## [PAUSED] SPAC IPOs & New Filings`. The parser
flags it; `pick_sector.py` skips it; the rotation contracts to active
sectors only. To unpause, remove the prefix. This is the right choice when
you want to temporarily suspend a sector without losing its keywords,
tickers, or notes.

**To remove a sector permanently**: delete the `## ` heading and its content.
Save. The rotation contracts.

**To reorder**: move the `## ` heading earlier or later in the file. The
position in the file = position in the Mon-Fri cycle (skipping paused
sectors).

**Current state** (as of last edit):
- Active rotation: Autonomous Trucking, Crypto / Stablecoins, Software,
  Healthcare, Consumer Discretionary (5 sectors, full cycle in one week).
- Paused: SPAC IPOs & New Filings, SPAC Deals & Business Combinations,
  Structured Equity & Micro-cap Financings, Regulatory & Market Structure
  (4 sectors). Unpause by removing the `[PAUSED] ` prefix in keywords.md.

If the user asks Claude to add/remove/pause a sector via chat, Claude can
edit keywords.md directly — show the diff first, confirm with the user,
then save. Don't auto-add tickers from auto-discovery flags without
confirming.

**Picking which sector to run** — for a generic "run the sector watch"
request, iterate through ALL active sectors (the default, per the new
daily-all-sectors mode). For ad-hoc requests scoped to a specific sector,
pass `--sector "Sector Name"` to the runner to scope to just that one.

## Pick your path

| Situation | Action |
|---|---|
| User said "run the sector watch" / "test the sector watch" — generic | run pipeline for today's scheduled sector; dry-run preview |
| User said "send today's sector watch" | run pipeline → preview → ask "send?" → on yes, send |
| User named a specific sector ("run sector watch for autonomous trucking") | pass `--sector "Autonomous Trucking"` to the runner; dry-run preview |
| User asks for a specific past date ("run yesterday's sector watch") | pass `--date YYYY-MM-DD`; pipeline picks that day's sector |
| Today is a weekend and user said "run today's" | tell the user no sector is scheduled today; offer to run the next weekday's or pick a specific one |
| User wants to edit keywords/universe | open `keywords.md`, edit, re-run |
| User wants to schedule daily | first complete one successful preview → send cycle; only then offer `create_scheduled_task` (Mon-Fri 6am ET is the default) |

## Action

### 1. List active sectors, then run the pipeline ONCE PER SECTOR

The daily workflow iterates: every weekday morning, fetch the active sector
list, then for each sector run the pipeline → compose → send. This produces
N emails per weekday (one per active sector). With the current keywords.md
that's 5 emails on Mon-Fri.

First, list the active sectors:

```bash
SKILL_DIR="<absolute path to this skill's directory>"
ACTIVE_SECTORS=$(python3 "$SKILL_DIR/scripts/pick_sector.py" \
    "$SKILL_DIR/keywords.md" "$SKILL_DIR/config.json" --list-active)
echo "$ACTIVE_SECTORS"
# Prints one sector name per line, e.g.:
#   Autonomous Trucking
#   Crypto / Stablecoins
#   Software
#   Healthcare
#   Consumer Discretionary
```

Then **for each sector, invoke the runner with --sector**:

```bash
SKILL_DIR="<absolute path to this skill's directory>"
OUT=$(mktemp /tmp/sector_watch_XXXX.json)

bash "$SKILL_DIR/scripts/run_sector_watch.sh" \
    "$SKILL_DIR/keywords.md" \
    "$SKILL_DIR/config.json" \
    "$OUT" \
    [--sector "Sector Name"] \
    [--date YYYY-MM-DD] \
    [--per-keyword 5] \
    [--country us]
```

Flags (all optional):

- `--sector "Name"` — explicit sector override (skip rotation lookup).
- `--date YYYY-MM-DD` — override today (useful for re-running missed days).
- `--per-keyword N` — top N news hits per keyword (default 5).
- `--country xx` — Bright Data country code (default us).

The script produces ONE JSON like:

```json
{
  "date": "2026-05-22",
  "generated_iso": "2026-05-22T20:15:00Z",
  "sector": {
    "name": "Structured Equity & Micro-cap Financings",
    "notes": "Universe is wide and changes weekly...",
    "tickers": [
      {"symbol": "XYZ", "label": "...", "perf": {"price": 4.21, "ok": true, "perf": {"1D": 0.021, "1W": 0.084, "1M": 0.123, "6M": 0.34, "