#!/usr/bin/env python3
"""
dedupe_state.py — Manages the sent-link state file for sector-watch dedupe.

State file format:
    {
      "Autonomous Trucking": {
        "2026-05-22": ["https://...", "https://..."],
        "2026-05-21": ["https://..."],
        ...
      },
      "Crypto / Stablecoins": {...},
      ...
    }

Provides three subcommands:
    recent      Print URLs sent for <sector> in the last N days (one per line)
    record      Append today's URLs (from stdin) for <sector> under today's date
    prune       Drop entries older than N days for all sectors

Usage:
    dedupe_state.py recent  "Autonomous Trucking" --days 7
    cat urls.txt | dedupe_state.py record "Autonomous Trucking"
    dedupe_state.py prune --days 7

The state file location is read from config.json's dedupe.state_file. Tilde
gets expanded. Creates the parent directory if missing.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path


def _state_path(config_path: str) -> Path:
    cfg = json.loads(Path(config_path).read_text())
    raw = cfg.get("dedupe", {}).get("state_file", "~/.sector-watch/sent-state.json")
    return Path(os.path.expanduser(raw))


def _load(state_file: Path) -> dict:
    if not state_file.exists():
        return {}
    try:
        return json.loads(state_file.read_text())
    except json.JSONDecodeError:
        return {}


def _save(state_file: Path, state: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2))
    try:
        os.chmod(state_file, 0o600)
    except Exception:
        pass


def cmd_recent(args) -> int:
    state = _load(_state_path(args.config))
    sector_state = state.get(args.sector, {})
    cutoff = (datetime.date.today() - datetime.timedelta(days=args.days)).isoformat()
    urls: set[str] = set()
    for date_str, day_urls in sector_state.items():
        if date_str >= cutoff:
            urls.update(day_urls)
    for u in sorted(urls):
        print(u)
    print(f"[dedupe] {len(urls)} recent URLs for {args.sector!r} (last {args.days} days)",
          file=sys.stderr)
    return 0


def cmd_record(args) -> int:
    urls = [line.strip() for line in sys.stdin if line.strip()]
    if not urls:
        print("[dedupe] no URLs on stdin, nothing to record", file=sys.stderr)
        return 0
    state_file = _state_path(args.config)
    state = _load(state_file)
    sector_state = state.setdefault(args.sector, {})
    today = datetime.date.today().isoformat()
    existing = set(sector_state.get(today, []))
    existing.update(urls)
    sector_state[today] = sorted(existing)
    _save(state_file, state)
    print(f"[dedupe] recorded {len(urls)} URLs for {args.sector!r} on {today}",
          file=sys.stderr)
    return 0


def cmd_prune(args) -> int:
    state_file = _state_path(args.config)
    state = _load(state_file)
    cutoff = (datetime.date.today() - datetime.timedelta(days=args.days)).isoformat()
    pruned = 0
    for sector, by_date in list(state.items()):
        for date_str in list(by_date.keys()):
            if date_str < cutoff:
                pruned += len(by_date.pop(date_str))
        if not by_date:
            del state[sector]
    _save(state_file, state)
    print(f"[dedupe] pruned {pruned} URLs older than {args.days} days", file=sys.stderr)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(Path(__file__).parent.parent / "config.json"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("recent")
    sp.add_argument("sector")
    sp.add_argument("--days", type=int, default=7)
    sp.set_defaults(func=cmd_recent)

    sp = sub.add_parser("record")
    sp.add_argument("sector")
    sp.set_defaults(func=cmd_record)

    sp = sub.add_parser("prune")
    sp.add_argument("--days", type=int, default=7)
    sp.set_defaults(func=cmd_prune)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
