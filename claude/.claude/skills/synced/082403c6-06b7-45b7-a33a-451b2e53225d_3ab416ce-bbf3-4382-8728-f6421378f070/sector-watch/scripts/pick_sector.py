#!/usr/bin/env python3
"""
pick_sector.py — Given today's date + keywords.md + config.json, return the
sector name to run today.

Logic:
  - Parse keywords.md → ordered list of sector names.
  - Read config.json for anchor_date, weekdays_only, fallback_behavior.
  - Compute "weekday index" = number of weekdays (Mon-Fri) elapsed since
    anchor_date, inclusive of today if today is a weekday.
  - sector_index = (weekday_index % N) where N = len(sectors).
  - If today is a weekend and weekdays_only=true:
      fallback_behavior 'skip'         → exit 2 with a clear message
      fallback_behavior 'run_next'     → use next Monday's sector
      fallback_behavior 'last_weekday' → use most recent Fri's sector

Usage:
    pick_sector.py <keywords.md> <config.json> [--date YYYY-MM-DD]
    pick_sector.py <keywords.md> <config.json> --sector "Autonomous Trucking"
        (explicit override; still validates the name exists)

Prints the chosen sector name to stdout, or exits non-zero with explanation.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Reuse the parser from sibling script
sys.path.insert(0, str(Path(__file__).parent))
from parse_keywords import parse  # type: ignore


def weekdays_between(start: date, end: date) -> int:
    """Count weekdays (Mon-Fri) from start (inclusive) to end (inclusive)."""
    if end < start:
        return -weekdays_between(end, start)
    days = (end - start).days + 1
    full_weeks, rem = divmod(days, 7)
    count = full_weeks * 5
    # Count weekdays in the remaining partial week
    start_dow = start.weekday()  # Mon=0 .. Sun=6
    for i in range(rem):
        if (start_dow + i) % 7 < 5:
            count += 1
    return count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords", help="Path to keywords.md")
    ap.add_argument("config", help="Path to config.json")
    ap.add_argument("--date", help="Override today's date (YYYY-MM-DD)")
    ap.add_argument("--sector", help="Explicit sector name (skip rotation calculation)")
    ap.add_argument("--list-active", action="store_true",
                    help="Print all active (non-paused) sectors, one per line, then exit. "
                         "Used by the daily-all-sectors workflow to iterate.")
    args = ap.parse_args()

    # Parse sectors — skip paused
    md = Path(args.keywords).read_text(encoding="utf-8")
    parsed = parse(md)["sectors"]
    paused = [s["name"] for s in parsed if s.get("paused")]
    sectors = [s["name"] for s in parsed if not s.get("paused")]
    if paused:
        print(f"[pick] paused (skipped): {paused}", file=sys.stderr)
    if not sectors:
        print("no active sectors in keywords.md (all paused?)", file=sys.stderr)
        return 1

    # --list-active: print every active sector and exit (no rotation lookup needed)
    if args.list_active:
        for name in sectors:
            print(name)
        print(f"[pick] {len(sectors)} active sectors listed", file=sys.stderr)
        return 0

    # Explicit sector override (paused sectors can be requested explicitly)
    if args.sector:
        all_names = [s["name"] for s in parsed]
        match = next((n for n in all_names if n.lower() == args.sector.lower()), None)
        if not match:
            print(f"unknown sector: {args.sector!r}", file=sys.stderr)
            print(f"valid: {all_names}", file=sys.stderr)
            return 1
        if match in paused:
            print(f"[pick] warning: sector {match!r} is PAUSED; using anyway (explicit override)",
                  file=sys.stderr)
        print(match)
        return 0

    # Read config
    cfg = json.loads(Path(args.config).read_text())
    sched = cfg.get("schedule", {})
    weekdays_only = sched.get("weekdays_only", True)
    anchor = datetime.strptime(sched.get("anchor_date", "2026-05-18"), "%Y-%m-%d").date()
    fallback = sched.get("fallback_behavior", "skip")

    # Today
    today = (datetime.strptime(args.date, "%Y-%m-%d").date()
             if args.date else date.today())
    is_weekend = today.weekday() >= 5  # Sat=5, Sun=6

    if is_weekend and weekdays_only:
        if fallback == "skip":
            print(f"today ({today}) is a weekend; weekdays_only=true; nothing to run",
                  file=sys.stderr)
            return 2
        elif fallback == "run_next":
            # Advance to next Monday
            days_to_monday = (7 - today.weekday()) % 7
            target = today + timedelta(days=days_to_monday)
        elif fallback == "last_weekday":
            # Back up to most recent Friday
            days_back = today.weekday() - 4  # Sat=1, Sun=2
            target = today - timedelta(days=days_back)
        else:
            print(f"unknown fallback_behavior: {fallback!r}", file=sys.stderr)
            return 1
    else:
        target = today

    # Compute weekday index relative to anchor
    wd = weekdays_between(anchor, target) - 1  # 0-indexed
    if wd < 0:
        print(f"target date {target} is before anchor {anchor}", file=sys.stderr)
        return 1

    sector_idx = wd % len(sectors)
    chosen = sectors[sector_idx]
    print(chosen)

    # Diagnostic info to stderr
    print(f"[pick] date={target} weekday_index={wd} sector_index={sector_idx}/{len(sectors)} → {chosen!r}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
