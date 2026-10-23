#!/usr/bin/env bash
# run_sector_watch.sh — Meteora daily single-sector pipeline.
#
# 1. Determine today's sector via pick_sector.py (or --sector override)
# 2. Run two news-search passes for that sector's keywords:
#      a. General news (sector keywords, past --window-hours)
#      b. Deal-focused news (sector hint × universal deal keywords, past --window-hours)
# 3. Filter out URLs already sent for this sector in the past dedupe.lookback_days
# 4. Scrape article bodies for the top items
# 5. Pull 1D/1W/1M/6M/YTD/1Y Yahoo perf for every ticker in the sector universe
# 6. Auto-discover new tickers mentioned in the news
# 7. Write one JSON the SKILL.md uses to compose the email
#
# Usage:
#   run_sector_watch.sh <keywords.md> <config.json> <out.json> [--sector NAME] [--date YYYY-MM-DD] [--per-keyword 5] [--country us] [--window-hours 48]
set -euo pipefail

KEYWORDS_FILE=""
CONFIG_FILE=""
OUT_FILE=""
PER_KEYWORD=5
COUNTRY="us"
SECTOR_OVERRIDE=""
DATE_OVERRIDE=""
WINDOW_HOURS=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --sector)        SECTOR_OVERRIDE="$2"; shift 2 ;;
        --date)          DATE_OVERRIDE="$2"; shift 2 ;;
        --per-keyword)   PER_KEYWORD="$2"; shift 2 ;;
        --country)       COUNTRY="$2"; shift 2 ;;
        --window-hours)  WINDOW_HOURS="$2"; shift 2 ;;
        -h|--help)       sed -n '2,20p' "$0"; exit 0 ;;
        -*) echo "unknown flag: $1" >&2; exit 1 ;;
        *)
            if   [[ -z "$KEYWORDS_FILE" ]]; then KEYWORDS_FILE="$1"
            elif [[ -z "$CONFIG_FILE"  ]]; then CONFIG_FILE="$1"
            elif [[ -z "$OUT_FILE"     ]]; then OUT_FILE="$1"
            else echo "extra arg: $1" >&2; exit 1
            fi
            shift ;;
    esac
done

[[ -n "$KEYWORDS_FILE" && -n "$CONFIG_FILE" && -n "$OUT_FILE" ]] || {
    echo "usage: run_sector_watch.sh <keywords.md> <config.json> <out.json> [flags]" >&2
    exit 1
}
[[ -r "$KEYWORDS_FILE" ]] || { echo "cannot read $KEYWORDS_FILE" >&2; exit 3; }
[[ -r "$CONFIG_FILE"  ]] || { echo "cannot read $CONFIG_FILE" >&2; exit 3; }

SKILL_DIR="$(cd "$(dirname "$(realpath "$0")")/.." && pwd)"
PARSE="$SKILL_DIR/scripts/parse_keywords.py"
PICK="$SKILL_DIR/scripts/pick_sector.py"
DEDUPE="$SKILL_DIR/scripts/dedupe_state.py"
# NOTE: yahoo_perf.py has been retired (yfinance + sandbox-proxy issues).
# Perf is pulled via scripts/yahoo_perf.js → Chrome javascript_tool by the
# calling agent AFTER this script returns. This script emits an empty perf
# placeholder and the agent fills it in.
for s in "$PARSE" "$PICK" "$DEDUPE"; do
    [[ -x "$s" ]] || { echo "missing helper: $s" >&2; exit 3; }
done

# Read window_hours from config if not on CLI
if [[ -z "$WINDOW_HOURS" ]]; then
    WINDOW_HOURS=$(python3 -c "import json;print(json.load(open('$CONFIG_FILE')).get('news',{}).get('window_hours',48))")
fi

# --- CLI gate ---------------------------------------------------------------
if ! command -v bdata >/dev/null 2>&1; then
    echo "bdata CLI not installed — see bright-data-best-practices/references/cli-setup.md" >&2
    exit 2
fi
if ! bdata zones >/dev/null 2>&1; then
    echo "bdata not authenticated — run: bdata login" >&2
    exit 2
fi

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# --- 1. Pick today's sector --------------------------------------------------
PICK_ARGS=("$KEYWORDS_FILE" "$CONFIG_FILE")
[[ -n "$SECTOR_OVERRIDE" ]] && PICK_ARGS+=(--sector "$SECTOR_OVERRIDE")
[[ -n "$DATE_OVERRIDE"   ]] && PICK_ARGS+=(--date "$DATE_OVERRIDE")

if ! TODAYS_SECTOR=$(python3 "$PICK" "${PICK_ARGS[@]}" 2>/tmp/pick.err); then
    PICK_RC=$?
    cat /tmp/pick.err >&2
    if [[ $PICK_RC -eq 2 ]]; then
        echo "{\"skipped\":true,\"reason\":\"weekend\",\"sector\":null}" > "$OUT_FILE"
        echo "$OUT_FILE"
        exit 0
    fi
    exit $PICK_RC
fi
cat /tmp/pick.err >&2 || true
echo "[run] today's sector: $TODAYS_SECTOR (window: ${WINDOW_HOURS}h)" >&2

# --- 2. Parse keywords.md, filter to today's sector -------------------------
python3 "$PARSE" "$KEYWORDS_FILE" "$WORK/parsed_all.json" >/dev/null
python3 - "$WORK/parsed_all.json" "$TODAYS_SECTOR" "$WORK/parsed.json" <<'PY'
import json, sys
src, sector_name, out = sys.argv[1:4]
data = json.load(open(src))
match = [s for s in data["sectors"] if s["name"] == sector_name]
if not match:
    print(f"sector '{sector_name}' not in parsed keywords.md", file=sys.stderr)
    sys.exit(1)
json.dump({"sectors": match}, open(out, "w"), indent=2, ensure_ascii=False)
PY
SECTOR_NAME=$(python3 -c "import json;print(json.load(open('$WORK/parsed.json'))['sectors'][0]['name'])")

# --- 3. Load dedupe state (URLs sent for this sector in the past 7 days) ----
LOOKBACK_DAYS=$(python3 -c "import json;print(json.load(open('$CONFIG_FILE')).get('dedupe',{}).get('lookback_days',7))")
python3 "$DEDUPE" --config "$CONFIG_FILE" recent "$SECTOR_NAME" --days "$LOOKBACK_DAYS" > "$WORK/recent_urls.txt" 2>/dev/null || true
RECENT_COUNT=$(wc -l < "$WORK/recent_urls.txt" | tr -d ' ')
echo "[run] dedupe: $RECENT_COUNT URLs already sent for this sector in past ${LOOKBACK_DAYS}d" >&2

# --- 4. General + Deal news searches ----------------------------------------
NEWS_DIR="$WORK/news"; mkdir -p "$NEWS_DIR"
python3 - "$WORK/parsed.json" "$CONFIG_FILE" "$WORK/recent_urls.txt" "$NEWS_DIR" "$PER_KEYWORD" "$COUNTRY" "$WINDOW_HOURS" <<'PY'
import json, subprocess, sys, time
from pathlib import Path

parsed_path, config_path, recent_path, news_dir, per_kw, country, window_hours = sys.argv[1:8]
per_kw = int(per_kw)
window_hours = int(window_hours)
window_secs = window_hours * 3600
sector = json.load(open(parsed_path))["sectors"][0]
cfg = json.load(open(config_path))
deal_keywords = cfg.get("news", {}).get("deal_keywords", [])
recent_urls = set(line.strip() for line in open(recent_path) if line.strip())

now_ts = time.time()

def parse_date(item):
    # Try common Bright Data date fields. Returns epoch seconds or 0 if unparseable.
    for key in ("date", "published", "publication_date", "timestamp"):
        v = item.get(key)
        if not v: continue
        if isinstance(v, (int, float)): return float(v)
        # Try a few string formats
        try:
            import datetime as dt
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return dt.datetime.strptime(v[:len(fmt) if "T" not in fmt else 19], fmt).replace(tzinfo=dt.timezone.utc).timestamp()
                except ValueError:
                    pass
        except Exception:
            pass
    return 0.0

def search_news(query, query_type="general"):
    try:
        r = subprocess.run(
            ["bdata", "search", query, "--type", "news", "--country", country, "--json"],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode != 0:
            print(f"[{query_type}] FAIL: {query!r}: {r.stderr[:120]}", file=sys.stderr)
            return []
        payload = json.loads(r.stdout)
        return payload.get("news") or payload.get("organic") or payload.get("results") or []
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"[{query_type}] FAIL: {query!r}: {type(e).__name__}", file=sys.stderr)
        return []

def to_item(raw, keyword, source_pass):
    return {
        "keyword": keyword,
        "source_pass": source_pass,
        "title":   (raw.get("title") or "").strip(),
        "link":    (raw.get("link") or raw.get("url") or "").strip(),
        "source":  (raw.get("source") or raw.get("displayed_link") or "").strip(),
        "snippet": (raw.get("description") or raw.get("snippet") or "").strip(),
        "date":    raw.get("date") or raw.get("published") or "",
        "date_ts": parse_date(raw),
    }

general_results = []
for kw in sector["keywords"]:
    raws = search_news(kw, "general")
    for r in raws[:per_kw]:
        general_results.append(to_item(r, kw, "general"))
    print(f"[news/general] {kw}: {len(raws)} hits", file=sys.stderr)

# Deal-focused search: combine the sector's first keyword (or sector name)
# with each deal keyword. Limit to top 3 deal keywords to control runtime.
sector_hint = sector["keywords"][0] if sector["keywords"] else sector["name"]
deal_results = []
for dk in deal_keywords[:5]:
    q = f"{sector_hint} {dk}"
    raws = search_news(q, "deal")
    for r in raws[:3]:
        deal_results.append(to_item(r, dk, "deal"))
    print(f"[news/deal]    {dk}: {len(raws)} hits", file=sys.stderr)

# Filter: window (drop items older than now - window_secs); dedupe (drop URLs
# already sent in past 7 days); dedupe across passes (deal > general if URL
# appears in both — flag it as a deal).
def filter_and_dedupe(items, already_seen):
    out = []
    seen = set(already_seen)
    for it in items:
        if not it["link"] or it["link"] in seen:
            continue
        if it["date_ts"] > 0 and (now_ts - it["date_ts"]) > window_secs:
            continue  # too old
        seen.add(it["link"])
        out.append(it)
    return out, seen

# Deals get priority — process them first so they don't get dedupe-eaten by
# general news with the same URL.
deal_filtered, seen = filter_and_dedupe(deal_results, recent_urls)
general_filtered, _ = filter_and_dedupe(general_results, seen)

Path(f"{news_dir}/general.json").write_text(json.dumps(general_filtered, indent=2))
Path(f"{news_dir}/deals.json").write_text(json.dumps(deal_filtered, indent=2))
print(f"[news] FINAL: general={len(general_filtered)} · deals={len(deal_filtered)} "
      f"(after window={window_hours}h and dedupe against {len(recent_urls)} recent)",
      file=sys.stderr)
PY

# --- 5. Yahoo perf placeholder (FETCHED LATER BY AGENT VIA CHROME) ----------
# Per the May 26, 2026 skill revision: yahoo_perf.py (yfinance-based) has been
# retired because (a) PyPI is blocked at the Cowork sandbox proxy and yfinance
# cannot be installed, and (b) sandbox bash cannot reach query1.finance.yahoo.com
# directly (403). The calling agent pulls perf via scripts/yahoo_perf.js routed
# through mcp__Claude_in_Chrome__javascript_tool AFTER this script returns.
# We emit a placeholder with the ticker list; the agent populates perf values.
TICKERS=$(python3 -c "
import json
sector = json.load(open('$WORK/parsed.json'))['sectors'][0]
print(','.join(t['symbol'] for t in sector['tickers']))
")
python3 -c "
import json
tickers = '$TICKERS'.split(',') if '$TICKERS' else []
placeholder = {t: {'ok': False, 'reason': 'pending — agent must run yahoo_perf.js via Chrome'} for t in tickers}
json.dump(placeholder, open('$WORK/perf.json', 'w'))
"
echo "[run] perf placeholder emitted for ${TICKERS:-(no tickers)} — agent fills via Chrome+yahoo_perf.js" >&2

# --- 6. Scrape top news bodies (for narrative synthesis) --------------------
BODIES_DIR="$WORK/bodies"; mkdir -p "$BODIES_DIR"
python3 - "$NEWS_DIR/general.json" "$NEWS_DIR/deals.json" "$BODIES_DIR/bodies.json" <<'PY'
import json, subprocess, sys
from pathlib import Path

gen_p, deal_p, out_p = sys.argv[1:4]
items = json.load(open(gen_p)) + json.load(open(deal_p))
seen = set()
bodies = []
for it in items[:6]:  # top items overall
    link = it["link"]
    if not link or link in seen: continue
    seen.add(link)
    try:
        r = subprocess.run(
            ["bdata", "scrape", link, "-f", "markdown"],
            capture_output=True, text=True, timeout=45,
        )
        if r.returncode == 0 and r.stdout.strip():
            body = r.stdout[:8000]
            bodies.append({"link": link, "title": it["title"], "body": body})
            print(f"[body] scraped: {it['title'][:60]}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print(f"[body] TIMEOUT: {link[:60]}", file=sys.stderr)
Path(out_p).write_text(json.dumps(bodies, indent=2))
PY

# --- 7. Auto-discover tickers in news + bodies ------------------------------
python3 - "$WORK/parsed.json" "$NEWS_DIR/general.json" "$NEWS_DIR/deals.json" "$BODIES_DIR/bodies.json" "$WORK/discovered.json" <<'PY'
import json, re, sys
from collections import Counter
from pathlib import Path

parsed_path, gen_p, deal_p, bodies_p, out_p = sys.argv[1:6]
sector = json.load(open(parsed_path))["sectors"][0]
universe = {t["symbol"].upper() for t in sector["tickers"]}
TICK_RE = re.compile(r"(?:\$|\(NASDAQ:\s*|\(NYSE:\s*|\(AMEX:\s*|\b(?:NASDAQ|NYSE|AMEX):\s*)([A-Z]{2,5})\b")
STOPWORDS = {"CEO","CFO","CTO","COO","AI","ML","API","USA","USD","EUR","GBP","GDP","EPS","IPO","SPAC","ETF","SEC","FDA","FAA","DOJ","FBI","NYSE","NASDAQ","AMEX","PIPE","ESG","LLM","SaaS","B2B","B2C","DTC"}

counter, refs = Counter(), {}
for path in (gen_p, deal_p):
    for it in json.load(open(path)):
        blob = f"{it.get('title','')}\n{it.get('snippet','')}"
        for m in TICK_RE.finditer(blob):
            sym = m.group(1)
            if sym in STOPWORDS or sym in universe: continue
            counter[sym] += 1
            refs.setdefault(sym, []).append(it.get("link",""))
for b in json.load(open(bodies_p)):
    for m in TICK_RE.finditer(b.get("body","")):
        sym = m.group(1)
        if sym in STOPWORDS or sym in universe: continue
        counter[sym] += 1

suggestions = [{"symbol": sym, "mention_count": cnt, "links": refs.get(sym,[])[:3]}
               for sym, cnt in counter.most_common(10) if cnt >= 2]
Path(out_p).write_text(json.dumps(suggestions, indent=2))
print(f"[discover] {len(suggestions)} new ticker suggestions", file=sys.stderr)
PY

# --- 8. Merge into final JSON output ----------------------------------------
python3 - "$WORK" "$OUT_FILE" "$SECTOR_NAME" "${DATE_OVERRIDE:-}" "$WINDOW_HOURS" <<'PY'
import json, sys, datetime
from pathlib import Path

work, out_file, sector_name, date_override, window_hours = sys.argv[1:6]
parsed = json.load(open(f"{work}/parsed.json"))["sectors"][0]
perf = json.load(open(f"{work}/perf.json"))
discovered = json.load(open(f"{work}/discovered.json"))
general = json.load(open(f"{work}/news/general.json"))
deals = json.load(open(f"{work}/news/deals.json"))
bodies = json.load(open(f"{work}/bodies/bodies.json"))

body_by_link = {b["link"]: b["body"] for b in bodies}
for 