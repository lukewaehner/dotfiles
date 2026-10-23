#!/usr/bin/env python3
"""
Condense a raw Meteora meeting transcript into high-signal dialogue.

Why: the daily transcripts are auto-generated (Zoom/Teams), ~250-300KB, and mostly
timestamps and one-word backchannel ("Yeah.", "Mm-hmm."). Feeding the raw file wastes
context and makes the model miss things on long transcripts. This collapses it to
speaker-attributed substance so the extraction step can read the whole day at high signal.

Usage:
    python condense_transcript.py RAW_IN.txt CONDENSED_OUT.txt

It:
  - drops VTT-style timestamp lines (HH:MM:SS --> HH:MM:SS)
  - joins each speaker's consecutive lines into one block
  - strips Meteora name-tag suffixes ("| Meteora Capital", "I Meteora Capital")
  - removes pure backchannel / filler blocks (unless they carry a number or a TICKER)

Keep the raw file too — this is a lossy convenience view for reading, not the source of record.
"""
import re
import sys
import os

TS = re.compile(r'^\d{1,2}:\d{2}:\d{2}\s*-->')
SPK = re.compile(r'^(.+?):\s*(.*)$')
BACKCHANNEL = {
    "yeah", "okay", "ok", "mm-hmm", "mmhm", "right", "sure", "yep", "got it",
    "exactly", "correct", "thank you", "thanks", "yes", "no", "uh-huh", "mm",
    "hmm", "cool", "of course", "i agree", "agreed", "true", "gotcha",
    "for sure", "totally", "yeah yeah", "right right", "mm hmm", "uh huh",
}
# Known speakers help avoid treating "First Choice Healthcare:" style false matches as speakers.
KNOWN = (
    "Vik Mittal", "Aidas Puskorius", "Luke Gries", "Alex Piskunov", "Larry Feldman",
    "Steve Schneider", "Shivom Joshi", "Elena Zheng", "Nathaniel Cespedes", "Arsh Jain",
    "Jack Davis", "Aditya Sagar", "Henry", "Rishi", "Kevin", "Joe", "Meteora Capital",
)
TAGS = (" I Meteora Capital", " | Meteora Capital", " Meteora Capital")


def condense(src_path: str) -> list[str]:
    text = open(src_path, encoding="utf-8", errors="replace").read().split("\n")
    blocks: list[tuple[str, str]] = []
    cur_spk = None
    cur_txt: list[str] = []

    def flush():
        nonlocal cur_spk, cur_txt
        if cur_spk and cur_txt:
            blocks.append((cur_spk, " ".join(cur_txt).strip()))
        cur_spk, cur_txt = None, []

    for ln in text:
        if TS.match(ln) or not ln.strip():
            continue
        m = SPK.match(ln)
        if m and any(m.group(1).startswith(k) for k in KNOWN):
            s = m.group(1)
            for t in TAGS:
                s = s.replace(t, "")
            s = s.strip()
            body = m.group(2).strip()
            if s == cur_spk:
                if body:
                    cur_txt.append(body)
            else:
                flush()
                cur_spk, cur_txt = s, ([body] if body else [])
        else:
            # continuation line for the current speaker (wrapped text)
            if cur_spk is not None:
                cur_txt.append(ln.strip())
    flush()

    out = []
    for s, t in blocks:
        norm = t.lower().strip().rstrip(".").strip()
        if norm in BACKCHANNEL:
            continue
        # keep short lines only if they carry a number or a TICKER-like token (signal)
        if len(t) < 18 and not re.search(r"\d", t) and not re.search(r"\b[A-Z]{2,6}\b", t):
            continue
        out.append(f"{s}: {t}")
    return out


def main():
    if len(sys.argv) < 3:
        print("usage: python condense_transcript.py RAW_IN.txt CONDENSED_OUT.txt", file=sys.stderr)
        sys.exit(2)
    src, dst = sys.argv[1], sys.argv[2]
    lines = condense(src)
    open(dst, "w", encoding="utf-8").write("\n".join(lines))
    kb = round(os.path.getsize(dst) / 1024, 1)
    words = sum(len(x.split()) for x in lines)
    print(f"condensed {os.path.basename(src)} -> {os.path.basename(dst)}: "
          f"{len(lines)} blocks, {kb}KB, ~{words} words")


if __name__ == "__main__":
    main()
