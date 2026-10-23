#!/usr/bin/env python3
"""
parse_keywords.py — Parse the sector-watch keywords.md into structured JSON.

Schema produced:
    {
      "sectors": [
        {
          "name": "Autonomous Trucking",
          "tickers": [{"symbol": "AUR", "label": "Aurora Innovation"}, ...],
          "keywords": ["autonomous trucking", '"self-driving freight"', ...],
          "notes": "AUR commercial launch with FedEx is..."
        },
        ...
      ]
    }

Usage:
    parse_keywords.py <keywords.md> [out.json]
    parse_keywords.py keywords.md             # prints to stdout
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path


def parse(md: str) -> dict:
    sectors: list[dict] = []
    current: dict | None = None
    subsection: str | None = None
    notes_lines: list[str] = []

    def flush_notes():
        if current is not None and notes_lines:
            current["notes"] = "\n".join(notes_lines).strip()

    in_fence = False
    for raw in md.splitlines():
        line = raw.rstrip()
        # Track fenced code blocks so we don't parse example sectors inside them
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # Sector heading
        if line.startswith("## ") and not line.startswith("### "):
            flush_notes()
            notes_lines = []
            name = line[3:].strip()
            if (not name
                or name.lower().startswith("rules")
                or name.lower().startswith("how")
                or name.lower().startswith("pausing")):
                current = None
                continue
            paused = False
            if name.startswith("[PAUSED] "):
                paused = True
                name = name[len("[PAUSED] "):]
            current = {"name": name, "paused": paused, "tickers": [], "keywords": [], "notes": ""}
            sectors.append(current)
            subsection = None
            continue
        # Subsection
        if line.startswith("### "):
            flush_notes()
            notes_lines = []
            head = line[4:].strip().lower()
            if "ticker" in head:
                subsection = "tickers"
            elif "keyword" in head:
                subsection = "keywords"
            elif "note" in head:
                subsection = "notes"
            else:
                subsection = None
            continue
        if current is None:
            continue
        # Bullets
        m = re.match(r"^\s*[-*]\s+(.+)$", line)
        if m and subsection in ("tickers", "keywords"):
            content = m.group(1).strip()
            # Drop pure-parenthetical placeholder bullets like:
            #   "(no fixed universe — universe shifts weekly. ...)"
            if content.startswith("(") and content.endswith(")"):
                continue
            if subsection == "tickers":
                # Pattern: "TICKER — Label" or "TICKER - Label" or just "TICKER"
                t = re.match(r"^([A-Z][A-Z0-9.\-]{0,9})\s*(?:[—\-:]\s*(.+))?$", content)
                if t:
                    sym = t.group(1).strip().upper()
                    label = (t.group(2) or "").strip()
                    current["tickers"].append({"symbol": sym, "label": label})
            else:  # keywords
                current["keywords"].append(content)
            continue
        # Notes body (free text under ### Notes)
        if subsection == "notes":
            # Comments inside notes are kept verbatim — they're the user's
            # context for the LLM.
            if line.strip():
                notes_lines.append(line)
            continue

    flush_notes()

    # Drop sectors with neither tickers nor keywords.
    sectors = [s for s in sectors if s["tickers"] or s["keywords"]]
    return {"sectors": sectors}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: parse_keywords.py <keywords.md> [out.json]", file=sys.stderr)
        return 1
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 1
    data = parse(path.read_text(encoding="utf-8"))
    out = json.dumps(data, indent=2, ensure_ascii=False)
    if len(sys.argv) >= 3:
        Path(sys.argv[2]).write_text(out, encoding="utf-8")
        print(f"wrote {sys.argv[2]}", file=sys.stderr)
    else:
        print(out)
    print(f"[parse] {len(data['sectors'])} sectors, "
          f"{sum(len(s['tickers']) for s in data['sectors'])} tickers, "
          f"{sum(len(s['keywords']) for s in data['sectors'])} keywords",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
