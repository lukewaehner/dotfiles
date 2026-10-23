---
name: merger-arb-radar
description: >
  Daily multilingual SPAC merger-arb news radar for Meteora. Reads the editable
  MERGERARB-WATCHLIST memory doc, and for every in-deal SPAC scans English PLUS
  each target's local-language press for SECOND-ORDER deal-completion and
  left-tail break risk. Verifies live deal status (the internal sheet lags actual
  close/termination by days), classifies every item by risk type / direction /
  severity / latency, dedupes against the prior 7 days, and produces a STRICT
  ranked digest and email. Trigger on "run the merger-arb radar", "merger arb
  news", "scan the arb book", "deal-risk digest", "arb radar", any reference to
  the MERGERARB-WATCHLIST, or a scheduled daily run. The job is information
  gathering, second-order analysis, and reporting - NOT spread/price modeling
  (price is one contextual line only). Always use this skill for the arb news
  radar; do not produce ad-hoc deal-news scans.
---

# Merger-Arb News Radar

A multilingual deal-risk radar for Meteora's in-deal SPAC book. Its entire
purpose is **latency arbitrage on deal-break information**: surface the item that
threatens (or supports) a deal's completion - especially when it breaks in a
foreign-language or local source **before** it reaches the English tape - and
deliver a sharp, second-order read of what it means for the deal.

This is a **reporting and analysis** tool. Do not build spread/yield models.
Price appears as exactly one contextual line per name (level vs. trust).

---

## 0. Scope & golden rules

- **Universe = SPAC business-combination deals only** (in-deal names). Not
  general M&A, not pre-deal SPACs.
- **The value is the second-order read, not the headline.** Every item must
  answer: *what does this imply for deal completion / timeline / a left-tail
  break?* A clipping with no so-what does not belong in the digest.
- **Foreign-language first, geography-driven.** For every name, scan the
  target's AND acquirer's local language(s) in addition to English - the language
  set is derived from where the deal actually touches (HQ, operations, listing,
  and every approval jurisdiction), never a fixed shortlist. The edge is catching
  the local item before it reaches the English tape.
- **Spanish & Portuguese are mandatory for any Latin-American or Iberian nexus.**
  If the target/acquirer has operations, a listing, major revenue, a counterparty,
  or a regulator anywhere in Latin America, Spain, or Portugal, scan Spanish AND
  Brazilian Portuguese - this is the exact lane the tool was built for (the
  founding case was LatAm litigation that hit local press days before English).
- **Verify deal status every run.** The internal spac-details sheet lags
  actual close/termination by days. If the deal has closed or been terminated,
  that is the headline - flag it and recommend removing the name.
- **Absence of news on a high-risk / near-deadline name is itself a signal.**
  Emit an INFO-GAP flag rather than silently dropping the name.
- **Dedupe.** Do not re-report items already logged to a name's memory doc in
  the prior 7 days.
- **READ-ONLY on the ENTIRE Meteora MCP — hard rule, no exceptions.** This skill
  may ONLY read from the Meteora MCP. It must NEVER create, write, append, edit,
  patch, delete, ingest, or otherwise mutate anything on it — not memory docs, not
  the Pinecone index, not any sheet or record. See section 1a for the explicit
  allow/deny tool lists. The watchlist and all per-name docs are user-maintained;
  this tool only reads them. All run state (dedupe, risk maps) lives in a local
  workspace file, never on the Meteora MCP.
- **Never fabricate.** If a source can't be confirmed, say so. No invented
  litigation, regulators, or quotes.

---

## 0a. HARD 2-DAY (48-HOUR) NEWS CAP - RIGID, NON-NEGOTIABLE (READ FIRST)

**Every NEWS / RISK item in the digest must be verifiably dated within the past
48 hours (2 calendar days) of run time. Zero exceptions. Zero "but this is
important" overrides. Zero soft-recency.** (Mirrors the daily sector-watch brief's
hard cap.)

**Step 1 - Compute the cutoff at run start.**
```
NOW_UTC    = current UTC timestamp at start of run
CUTOFF_UTC = NOW_UTC - 48 hours        # ISO 8601, e.g. "2026-06-12T14:30:00Z"
```
Surface CUTOFF_UTC in working notes. Every item must have a publication
timestamp >= CUTOFF_UTC. An item at CUTOFF_UTC - 1 second is stale -> drop. No
fuzz, no rounding.

**Step 2 - Per-item verification (MANDATORY, every item, stop at first PASS/DROP).**
1. Snippet-date check. Accept "4 hours ago", "yesterday", "Jun 13, 2026",
   "2026-06-13", "6/13/2026". Convert to UTC. >= CUTOFF -> PASS; < CUTOFF ->
   DROP (do not even fetch).
2. No date in snippet -> fetch (`mcp__workspace__web_fetch` or Chrome
   `get_page_text`) and look for `<time datetime>`, `article:published_time`,
   `og:published_time`, a `pubdate` attr, or a visible byline date. >= CUTOFF ->
   PASS; older -> DROP.
3. No determinable date -> DROP. URL slug dates (/2026/06/13/) are NOT evidence.
4. Fetch fails (404/blocked/timeout/JS-only) -> DROP.
Quotable: *"No verified timestamp >= CUTOFF -> DROP. Period."*

**Step 3 - Bias queries to recency.** Include explicit dates and
`after:YYYY-MM-DD`; use "today"/"this week"/"yesterday" phrasing; never use
evergreen queries ("outlook 2026", "M&A wave"); never trust SERP order as a
freshness signal.

**Step 4 - Empty state.** If a name has no verified-fresh item, render exactly
`No verified updates in last 48 hrs.` Do NOT pad with stale items for "context."
The empty state IS the message.

**ENFORCEMENT IS PROGRAMMATIC, NOT VIBES.** Every candidate news item MUST pass
through `scripts/verify_freshness.py` (ported + hardened from the sector-watch
scheduled task). Build a JSON array of candidates (each with title, link, source,
snippet, and any date/published/timestamp field, plus a `language` tag) and run:
`cat candidates.json | python3 scripts/verify_freshness.py --window-hours 48`.
Only items in the script's `kept[]` may appear in the email. The script DROPS any
item that is older than cutoff OR has no verifiable date (stricter than the
sector-watch shell, which kept undated items). Use its `dropped_stale` /
`dropped_undated` / `languages` counts directly in the footer audit.

**ABSOLUTE PROHIBITION.** An item that fails verification does NOT appear in the
email in ANY form - not as a citation, not as a link, not as "standing risk,"
"context," or "background," not paraphrased. If you catch yourself writing about a
risk whose only evidence is a stale/undated source, DROP it entirely. (This is the
exact mistake that shipped 2013/2025-dated links in a prior run - never again.)

**THE ONLY CARVE-OUT.** A DEAL-STATUS change (CLOSED / TERMINATED / EXTENDED) and
an upcoming vote/deadline DATE are STRUCTURAL facts taken from filings /
spac-details (NOT from a dated news link), and may be stated regardless of the
cap. A standing risk theme may be mentioned ONLY if at least one supporting item
PASSED verification this run; otherwise it is omitted.

**Step 5 - Footer audit line is REQUIRED** (see section 6).

---

## 1. Inputs & tools

| Need | Tool |
|------|------|
| Active watchlist | read-memory-doc on MERGERARB-WATCHLIST (parse the ACTIVE TICKERS line) |
| Deal context (target, deadline, trust, domicile) | spac-details (ticker lookup) |
| Per-name context (read-only) | read-memory-doc on each ticker (READ ONLY) |
| Price/trust context (1 line) | get-price (mid) + trust from spac-details |
| News scan (EN + local language) | WebSearch (query in each language); escalate to Bright Data search/scrape for deeper local sourcing |
| Dedupe state (7-day) | local JSON state file in the workspace (e.g. radar-state.json). NEVER write memory docs. |
| Delivery | send-email (Meteora MCP) or send-as-me; pilot = dry-run preview, send only on approval |

---

## 1a. Meteora MCP access — ALLOW / DENY (read-only enforcement)

ALLOWED (read-only) — the ONLY Meteora MCP tools this skill may call:
`spac-details`, `get-price`, `get-vwap`, `get-company-info`, `read-memory-doc`,
`list-memory-docs`, `semantic-search`, `list-documents`, `list-indexes`,
`edgar-filings`, `edgar-filing-index`, `edgar-filing-text`, `edgar-company-facts`,
`emsx-blotter` (view only).

FORBIDDEN — NEVER call these (or any other mutating tool), under any circumstance:
`create-memory-doc`, `update-memory-doc`, `update-memory-summary`,
`patch-memory-summary`, `patch-memory-entry`, `delete-memory-entry`,
`delete-memory-doc`, `process-document` (ingest/write), and anything else that
creates, edits, deletes, or ingests. If a step seems to need a write, do it in the
local workspace state file instead — never on the Meteora MCP. Email delivery is
out-of-band via the send-as-me / email-assistant plugin, not via any Meteora write.

If you ever find yourself about to call a forbidden tool: STOP. The correct action
is always to read, compute locally, and report.

## 2. Run procedure (per run)

1. **Load watchlist.** read-memory-doc MERGERARB-WATCHLIST -> parse ACTIVE
   TICKERS. Skip anything under PAUSED.
2. **Per name, load context.** spac-details (target, deadline, trust,
   domicile, price) + read-memory-doc <ticker> (the RISK MAP entry + recent
   entries for dedupe). If no RISK MAP exists, build one (see section 3) before scanning.
3. **Status check (mandatory).** Run an English query for "<target> <SPAC>
   merger closed / terminated / completed / trading <new ticker>". Resolve to one
   of: LIVE / CLOSED / TERMINATED / EXTENDED / UNKNOWN. If CLOSED/TERMINATED ->
   that is the top-line flag in the digest and recommend watchlist removal (do
   NOT write to any memory doc).
4. **Compute the live spread (Bloomberg).** For each name pull the live mid via
   `get-price` and the trust value from `spac-details`; compute
   `spread = mid - trust` in cents and %, labeled premium (mid > trust) or
   discount (mid < trust) to trust. This goes on the name's top line (section 5.1).
5. **Multilingual scan (LIVE names).** Build queries from the RISK MAP: target
   legal + local-language name variants, SPAC name, regulator names, and the
   left-tail watch terms (litigation, antitrust/FDI, financing/PIPE/redemption,
   vote, MAC/business deterioration, competing bid). Run in English AND each
   mapped local language. Lookback obeys the 2-day cap (section 0a). Prefer
   primary sources (regulators, courts, filings) and the RISK MAP local press.
   **Keep a running tally** of (a) the count of distinct sources/pages examined
   and (b) the set of languages queried - both are reported in the footer
   (section 6).
6. **Classify each item** per section 4 (class / direction / severity / latency).
7. **Dedupe** against the last 7 days of the name's memory entries.
8. **Compose** each per-deal block in the STRICT format (section 5).
9. **Rank & assemble** the digest (section 5) and the email (section 6).
10. **Record** dedupe keys for new material items to the local workspace state
    file so the next run dedupes correctly. NEVER write memory docs.
11. **Deliver.** Dry-run preview by default; send email only when approved /
    when run in send mode.

---

## 3. Risk map (built once per name, refreshed as the deal evolves)

Build the risk map IN-RUN from spac-details + web (and read any existing
context via read-memory-doc, read-only). Persist it ONLY to the local workspace
state file if you want reuse - NEVER write it to a memory doc. Required fields:

- **Target legal name** + **local-language name variants** (what the local
  press actually calls it).
- **HQ country** and any second operating country.
- **Scan languages** (English + every local language the deal touches; note
  secondary). Mapping cues: Brazil -> Portuguese; Mexico/Argentina/Chile/Colombia/
  Peru/Spain -> Spanish; France -> French; Germany/Austria/Switzerland -> German;
  Italy -> Italian; Greater China -> Chinese; Japan -> Japanese; Korea -> Korean;
  Thailand -> Thai. A LatAm/Iberia nexus ALWAYS adds Spanish and/or Portuguese.
- **Regulatory / approval jurisdictions** that gate closing (SEC; shareholder
  vote; antitrust - EU/DG-COMP, CMA, SAMR/China, CADE/Brazil, COFECE/Mexico,
  CNDC/Argentina; FDI/strategic-tech - CFIUS, French/Finnish/German screening;
  securities - CVM/Brazil, CNV/Argentina, CNBV/Mexico, CMF/Chile, CNMV/Spain,
  CMVM/Portugal; sector regulators). *The regulatory map is the scan map.*
- **Left-tail watch items** specific to the deal (redemption/PIPE mechanics,
  sovereignty objections, distressed-target solvency, lock-ups, MAC triggers).
- **Sources to scan** - named local press + regulator/court sites + IR/EDGAR.
- **Status at seed** (date + LIVE/CLOSED/etc.).

---

## 4. Classification taxonomy (apply to every item)

**Risk class** (pick one):
REGULATORY (antitrust / FDI / securities) / LITIGATION /
POLITICAL-SOVEREIGNTY / FINANCING (PIPE / convertible / redemption) /
MAC-MAE (target business deterioration, solvency) / SHAREHOLDER-VOTE /
COMPETING-BID / TIMELINE (slippage / extension / deadline) /
DEAL-STATUS (closed / terminated) / INFO-GAP (thin coverage on high-risk
or near-deadline name).

**Direction vs. completion:** THREATENS / SUPPORTS / NEUTRAL.

**Severity:**
- HIGH (red) - could break, halt, or materially re-rate the deal; or deal
  status changed (closed/terminated). Always surfaces to the top.
- MEDIUM (yellow) - timeline or terms risk; watch.
- LOW/INFO (green) - constructive or immaterial; context only.

**Latency flag** (the alpha tell):
- LOCAL-ONLY (globe) - appears in local-language / foreign source, **not yet in
  the English tape**. Boost ranking one tier.
- WIRE - already on English wires.

---

## 5. STRICT report format (locked) - NARRATIVE ANALYST MEMO, MODERN HTML

Reads like a written analyst memo with light modern styling (navy/slate accent
rules, clean type, NO boxes). One narrative entry per name. Severity is computed
internally ONLY - to order entries (most material first) and to choose the Bottom
line - and is NOT displayed (no HIGH/MED/LOW labels, no severity dots).

### 5.1 Per-deal entry

```
Heading (bold, navy): {TICKER} -> {Target legal name}
Sub-line (muted):     {SPAC vehicle name} · {sector}, {country}
Meta (muted mono):    spread {live mid} vs {trust} = {+/-X c} ({+/-X.X%}) {premium|discount}  ·  {deadline <date> | close <window> -> <post-close ticker>}
Paragraph: one FLOWING analytical paragraph (~3-5 sentences) connecting what is
new in the 48h window (or that nothing cleared it) to completion odds, timeline,
and the single biggest left-tail risk, and CLOSING with the recommendation woven
into the prose.
```

Rules:
- Heading is ONLY `{TICKER} -> {Target}` (the company being acquired). Everything
  else - SPAC vehicle, sector/country, spread, deadline - goes on the lines below.
- SPREAD IS MANDATORY on the meta line (live Bloomberg mid vs trust; if unquotable,
  `spread n/a (no quote)` and treat the gap as a flag).
- DO NOT print priority (HIGH/MED/LOW) or a LIVE/status word, and DO NOT use
  severity dots. Order entries by internal severity, most material first.
- The recommendation is woven into the closing sentence - NO standalone Action block.
- Paragraph is analysis with narrative flow, not a restated headline. If nothing
  cleared the 48h window, say so in-sentence.

### 5.2 Digest structure

1. Title + date stamp (weekday, date · SPAC in-deal book · watchlist/set).
2. **Bottom line:** 1-2 sentence paragraph - the single most important takeaway.
3. Entries (section 5.1), most-material first; thin rule between entries.
4. **Coverage at a glance** (footer): "~N sources scanned across L languages over
   the past 48h", then a per-language breakdown (language · approx count · a few
   named outlets).
5. Audit line: window/cutoff · kept/dropped · methodology, AND a DATA-PULLED
   TIMESTAMP (date + ET time the Bloomberg/price data was fetched).

---

## 6. STRICT email format (locked)

- **Format: HTML** (`html=true`), light modern styling, NO boxes:
  - White email body, system sans-serif, line-height ~1.6, max-width ~660px.
  - Title bold ~20px with a 3px navy/slate (#1f3a5f) bottom-border rule under the
    header block.
  - Section micro-labels ("Bottom line", "Coverage at a glance") in small
    uppercase, letter-spaced, navy.
  - Each name: bold navy heading `{TICKER} -> {Target}`; muted sub-line
    (SPAC vehicle · sector, country); muted MONOSPACE meta line (spread ·
    deadline/close -> post-close ticker); then the paragraph. Thin 1px light rule
    between entries. No severity dots, no priority/status labels, no Action block.
  - Footer opens on a 2px navy rule: a "Coverage at a glance" per-language table
    (count + sample outlets), then the muted audit + data-pulled line.
- **Subject:** `[MERGER-ARB RADAR] {Mon DD} - {N} names / 48h cap` (prefix `[TEST]`).
- **Links:** working source link inline where cited; non-English items get a short
  English gloss in parentheses.
- **Footer (REQUIRED), in order:**
  - `Coverage at a glance:` ~N sources across L languages + per-language breakdown
    (language · ~count · sample outlets).
  - `Window: past 48 h · cutoff {CUTOFF_UTC} · {kept_count} kept, {dropped_stale} dropped stale, {dropped_undated} dropped undated.` (numbers come straight from verify_freshness.py)
  - `Data pulled: {Mon DD, YYYY, HH:MM ET}` - timestamp the price/Bloomberg data
    was fetched (from get-price `current_time_et`).
- **Recipients:** only those named by the user / config. Never add unnamed recipients.
- **Send gate:** default DRY-RUN; send only on approval / send mode.

### Worked example (one entry + footer, illustrative)

```
AOGO -> Bangkok Tellink
Arogo Capital Acquisition Corp · mobile virtual network operator, Thailand
spread n/a (no quote, appears OTC) · deadline Jun 29
The tell here isn't a headline, it's the plumbing: Bloomberg can no longer resolve
AOGO and one source now lists it OTC, and with the trust nearly fully redeemed and
no S-4 two weeks from the deadline, this looks likelier to lapse or be forced
through a distressed extension than to close - worth confirming listing status and
any extension/liquidation filing before Jun 29.

--- footer ---
Coverage at a glance: ~50 sources across 5 languages - English ~24 (Investing.com,
StockTitan), Italian ~10 (Il Sole 24 Ore, MilanoFinanza), French ~8 (Boursorama,
Zonebourse), Chinese ~9 (PharmCube, mg21), Thai ~8 (AInvest, GlobeNewswire).
Window: past 48 h · cutoff 2026-06-13 00:00 UTC · 0 kept, 7 dropped as stale.
Data pulled: Jun 15, 2026, 09:28 ET.
```

---

## 7. Editing the universe

The watchlist is the memory doc **MERGERARB-WATCHLIST**. To change coverage,
edit its ACTIVE TICKERS line (or move names to PAUSED). Optionally, the
scheduled run can re-pull spac-details (stage=indeal) each morning so newly
announced deals can be added and closed names auto-drop. Each name needs a RISK
MAP (section 3) before its first scan; build it on the fly if missing.

## 8. Scheduling

Wrap section 2 in a daily scheduled task (~8-9am ET). Pilot: dry-run preview first;
flip to send after approval. Cadence is adjustable via the scheduled task.

## 9. Calibration notes (from pilot, 2026-06)

- Foreign-language scanning validated across FR, FI, SV, DE, IT, ZH.
- Caught two "live" names that had actually CLOSED (Einride->ENRD, VERAXA->VRXA)
  while the internal sheet was stale -> section 2 step 3 is mandatory.
- Caught near-term catalysts (IQM EGM 6/25) and timeline slippage (Everli).
- Flagged a distressed-target left-tail (Aiways) where thin recent news = the
  INFO-GAP signal, not an all-clear.
