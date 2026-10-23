#!/usr/bin/env python3
"""
verify_freshness.py — HARD 48h cap enforcement for the merger-arb radar.

Ports the date-window filter from sector-watch's run_sector_watch.sh, but
STRICTER: an item with NO verifiable publication date is DROPPED (the
sector-watch shell kept date_ts==0 items; the SKILL prose says drop them, and
this radar follows the prose). No verified timestamp >= cutoff -> DROP. Period.

Input : JSON array of candidate items on stdin (or a file path arg). Each item
        SHOULD carry a date in any of: date, published, publication_date,
        timestamp, snippet (relative phrases like "3 hours ago", "yesterday",
        "2 days ago" are parsed against --now).
Output: JSON {cutoff_utc, now_utc, kept:[...], dropped_stale, dropped_undated,
        kept_count, languages:{...}} to stdout, and a one-line audit to stderr.

Usage:
    cat candidates.json | verify_freshness.py --window-hours 48
    verify_freshness.py candidates.json --window-hours 48 --now 2026-06-15T14:30:00Z
"""
from __future__ import annotations
import argparse, json, re, sys
import datetime as dt

ABS_FORMATS = (
    "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
    "%Y/%m/%d", "%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y", "%d/%m/%Y", "%m/%d/%Y",
)

def parse_abs(v: str):
    v = v.strip()
    cands = [v, v[:19], v[:10]]
    for fmt in ABS_FORMATS:
        for c in cands:
            try:
                return dt.datetime.strptime(c, fmt).replace(tzinfo=dt.timezone.utc)
            except ValueError:
                continue
    return None

def parse_relative(text: str, now: dt.datetime):
    t = text.lower()
    if "just now" in t or "moments ago" in t: return now
    if "yesterday" in t: return now - dt.timedelta(days=1)
    if re.search(r"\btoday\b", t): return now
    m = re.search(r"(\d+)\s*(minute|hour|day|week|month|year)s?\s*ago", t)
    if m:
        n = int(m.group(1)); unit = m.group(2)
        mult = {"minute":1/1440,"hour":1/24,"day":1,"week":7,"month":30,"year":365}[unit]
        return now - dt.timedelta(days=n*mult)
    return None

def item_dt(item, now):
    for key in ("date","published","publication_date","timestamp","datetime"):
        v = item.get(key)
        if v in (None,""): continue
        if isinstance(v,(int,float)):
            return dt.datetime.fromtimestamp(float(v), dt.timezone.utc)
        d = parse_abs(str(v)) or parse_relative(str(v), now)
        if d: return d
    # last resort: scan snippet/title for a relative phrase or absolute date
    blob = " ".join(str(item.get(k,"")) for k in ("snippet","title","description"))
    d = parse_relative(blob, now)
    if d: return d
    m = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", blob)
    if m: return parse_abs(m.group(1))
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile", nargs="?", help="JSON array file (default stdin)")
    ap.add_argument("--window-hours", type=int, default=48)
    ap.add_argument("--now", help="ISO8601 override for 'now' (default: utcnow)")
    args = ap.parse_args()

    now = (dt.datetime.fromisoformat(args.now.replace("Z","+00:00"))
           if args.now else dt.datetime.now(dt.timezone.utc))
    if now.tzinfo is None: now = now.replace(tzinfo=dt.timezone.utc)
    cutoff = now - dt.timedelta(hours=args.window_hours)

    raw = open(args.infile).read() if args.infile else sys.stdin.read()
    items = json.loads(raw) if raw.strip() else []

    kept, stale, undated = [], 0, 0
    langs = {}
    for it in items:
        d = item_dt(it, now)
        if d is None:
            undated += 1; continue
        if d < cutoff:
            stale += 1; continue
        it = dict(it); it["_resolved_date"] = d.isoformat()
        kept.append(it)
        lg = it.get("language") or it.get("lang") or "unknown"
        langs[lg] = langs.get(lg, 0) + 1

    out = {
        "now_utc": now.isoformat(),
        "cutoff_utc": cutoff.isoformat(),
        "window_hours": args.window_hours,
        "kept": kept,
        "kept_count": len(kept),
        "dropped_stale": stale,
        "dropped_undated": undated,
        "languages": langs,
    }
    print(json.dumps(out, indent=2))
    print(f"[verify] cutoff={cutoff.isoformat()} kept={len(kept)} "
          f"dropped_stale={stale} dropped_undated={undated}", file=sys.stderr)

if __name__ == "__main__":
    main()
