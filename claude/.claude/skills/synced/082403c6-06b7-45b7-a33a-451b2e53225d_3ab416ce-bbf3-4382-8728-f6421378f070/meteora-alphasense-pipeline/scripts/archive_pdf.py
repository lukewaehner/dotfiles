#!/usr/bin/env python3
"""
archive_pdf.py - deterministic file-wrangling for the AlphaSense pipeline.

Why this exists: every run, after AlphaSense generates a broker-research PDF, the same
error-prone steps repeat - find the file Chrome just dropped in Downloads, move it into
BrokerResearch/<slug>/<YYYY-MM>/, dedupe it, and append an audit row. Doing that ad hoc in
bash each run wastes tokens and invites mistakes (wrong folder, double-download, broken CSV
quoting). This script does it once, correctly, and is idempotent.

AlphaSense names every download exactly:  "YYYYMMDD - Firm - Title - N pages.pdf"

Typical use (one call per downloaded doc, right after the reader's Download finishes):
    python archive_pdf.py --slug nuclear-energy \
        --downloads "C:/Users/rishi/Downloads" \
        --root "C:/Users/rishi/Desktop/Rishi/Projects/Meteora Capital/AlphaSense" \
        --docid SSRFS-00-abc123 --newest

Or archive a specific known filename:
    python archive_pdf.py --slug crypto-stablecoins --file "20260701 - BTIG - X - 8 pages.pdf" ...

Exit codes: 0 = archived (or already present / skipped as dup), 2 = nothing matched.
State/manifest live under <root>/BrokerResearch/ so they persist across runs.
"""
from __future__ import annotations
import argparse, csv, json, os, re, shutil, sys, datetime as dt

AS_NAME = re.compile(r"^(\d{8}) - (.+?) - (.+?) - (\d+) pages\.pdf$", re.I)  # date, firm, title, pages


def load_state(state_path: str) -> dict:
    if os.path.exists(state_path):
        try:
            return json.load(open(state_path))
        except Exception:
            return {}
    return {}


def save_state(state_path: str, state: dict) -> None:
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    json.dump(state, open(state_path, "w"), indent=1, sort_keys=True)


def parse_name(fname: str) -> dict | None:
    m = AS_NAME.match(fname)
    if not m:
        return None
    d, firm, title, pages = m.groups()
    return {"released_date": f"{d[:4]}-{d[4:6]}-{d[6:]}", "firm": firm.strip(),
            "title": title.strip(), "pages": pages, "filename": fname}


def pick_file(downloads: str, explicit: str | None, newest: bool, since_min: int) -> str | None:
    if explicit:
        p = os.path.join(downloads, explicit)
        return explicit if os.path.exists(p) else None
    cands = []
    cutoff = dt.datetime.now().timestamp() - since_min * 60
    for f in os.listdir(downloads):
        if not AS_NAME.match(f):
            continue
        mtime = os.path.getmtime(os.path.join(downloads, f))
        if since_min and mtime < cutoff:
            continue
        cands.append((mtime, f))
    if not cands:
        return None
    cands.sort(reverse=True)                 # newest first
    return cands[0][1] if newest else cands[0][1]


def append_manifest(manifest: str, row: dict) -> None:
    cols = ["pulled_at", "released_date", "firm", "title", "slug", "docid", "filename", "local_path"]
    new = not os.path.exists(manifest)
    os.makedirs(os.path.dirname(manifest), exist_ok=True)
    with open(manifest, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in cols})


def main() -> int:
    ap = argparse.ArgumentParser(description="Archive an AlphaSense-downloaded PDF into the research folder.")
    ap.add_argument("--slug", required=True, help="sector/book slug, e.g. nuclear-energy, spac-universe, macro-rates-credit")
    ap.add_argument("--root", required=True, help="project root (the AlphaSense folder)")
    ap.add_argument("--downloads", required=True, help="Chrome download landing dir")
    ap.add_argument("--file", default=None, help="specific filename to archive (else sweep by pattern)")
    ap.add_argument("--newest", action="store_true", help="when sweeping, take the newest matching PDF")
    ap.add_argument("--since-min", type=int, default=10, help="sweep window in minutes (default 10)")
    ap.add_argument("--docid", default="", help="AlphaSense docid (SSRFS-...) for dedup + audit")
    args = ap.parse_args()

    broker_root = os.path.join(args.root, "BrokerResearch")
    state_path = os.path.join(broker_root, "_state_seen.json")
    manifest = os.path.join(broker_root, "_manifest.csv")
    state = load_state(state_path)

    fname = pick_file(args.downloads, args.file, args.newest, args.since_min)
    if not fname:
        print("NOTHING_MATCHED: no AlphaSense-named PDF found in downloads for the given criteria", file=sys.stderr)
        return 2

    meta = parse_name(fname) or {"filename": fname, "released_date": "", "firm": "", "title": "", "pages": ""}
    key = args.docid or f"{meta['released_date']}|{meta['firm'].upper()}|{meta['title'].upper()}"

    month = (meta["released_date"][:7] or dt.date.today().strftime("%Y-%m"))
    dest_dir = os.path.join(broker_root, args.slug, month)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, fname)

    if key in state or os.path.exists(dest):
        # already archived - clean the duplicate out of Downloads so it doesn't re-sweep
        src = os.path.join(args.downloads, fname)
        if os.path.exists(src) and os.path.exists(dest):
            try: os.remove(src)
            except OSError: pass
        print(f"SKIP_DUP: {fname} already archived under {args.slug}/{month}")
        return 0

    shutil.move(os.path.join(args.downloads, fname), dest)
    state[key] = {"filename": fname, "slug": args.slug, "archived_at": dt.datetime.utcnow().isoformat(timespec="seconds")}
    save_state(state_path, state)
    append_manifest(manifest, {
        "pulled_at": dt.datetime.utcnow().isoformat(timespec="seconds"),
        "released_date": meta["released_date"], "firm": meta["firm"], "title": meta["title"],
        "slug": args.slug, "docid": args.docid, "filename": fname,
        "local_path": os.path.relpath(dest, args.root),
    })
    print(f"ARCHIVED: {fname} -> {args.slug}/{month}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
