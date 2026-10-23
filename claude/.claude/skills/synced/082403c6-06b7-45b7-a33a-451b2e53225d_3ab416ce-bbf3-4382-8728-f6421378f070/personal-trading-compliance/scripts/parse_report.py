"""
parse_report.py — normalize a structured broker report (CSV / XLSX) into canonical transactions.

Broker reports vary a lot. This handles the STRUCTURED case (CSV/XLSX) two ways:
  1. A saved per-broker template (JSON column map) — deterministic, preferred once known.
  2. Header auto-detection — best-effort keyword matching when no template exists yet.

For PDFs, scanned statements, or layouts this can't confidently read, DO NOT force it here —
SKILL.md instructs Claude to extract those to the same canonical transactions.json by hand and
run reconcile.py directly. The point is to never silently mis-parse (a wrong parse can wrongly
accuse an employee); low confidence is surfaced, not buried.

Usage:
    python parse_report.py INPUT.csv OUT.json --employee "Jane Doe" --broker "Fidelity" [--template t.json]

A template JSON looks like:
    {"trade_date":"Run Date","ticker":"Symbol","side":"Action","quantity":"Quantity","price":"Price"}
"""
from __future__ import annotations
import sys, os, csv, argparse
sys.path.insert(0, os.path.dirname(__file__))
from common import normalize_side, parse_date, iso, norm_ticker, dump_json, OTHER

# Canonical field -> header keywords (most specific first).
_KEYWORDS = {
    "trade_date": ["trade date", "trade dt", "transaction date", "activity date", "run date", "settlement date", "date"],
    "ticker": ["symbol", "ticker", "sym"],
    "cusip": ["cusip"],
    "security_name": ["description", "security description", "security name", "security", "name"],
    "side": ["action", "transaction type", "buy/sell", "trans code", "activity", "type", "side"],
    "quantity": ["quantity", "number of shares", "shares", "qty", "units"],
    "price": ["execution price", "unit price", "price"],
    "account": ["account number", "account", "acct"],
}


def _load_rows(path):
    """Return (headers, list-of-dict rows) for csv or xlsx."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return [], []
        headers = [str(h).strip() if h is not None else "" for h in rows[0]]
        out = [dict(zip(headers, r)) for r in rows[1:]]
        return headers, out
    # csv
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return (reader.fieldnames or []), list(reader)


def _auto_map(headers):
    """Guess a column map from headers. Returns {canonical: header}."""
    lower = {h.lower().strip(): h for h in headers if h}
    cmap = {}
    used = set()
    for field, kws in _KEYWORDS.items():
        for kw in kws:
            match = next((orig for low, orig in lower.items() if kw in low and orig not in used), None)
            if match:
                cmap[field] = match
                used.add(match)
                break
    return cmap


def _num(raw):
    if raw is None or raw == "":
        return None
    try:
        return float(str(raw).replace(",", "").replace("$", "").replace("(", "-").replace(")", "").strip())
    except ValueError:
        return None


def parse(path, employee, broker, template=None, account_last4=None):
    headers, rows = _load_rows(path)
    cmap = template or _auto_map(headers)
    src = os.path.basename(path)
    txns, parsed_ok = [], 0

    for i, row in enumerate(rows):
        if not any(v not in (None, "") for v in row.values()):
            continue  # blank line
        def g(field):
            col = cmap.get(field)
            return row.get(col) if col else None

        td = parse_date(g("trade_date"))
        ticker = norm_ticker(g("ticker"))
        side = normalize_side(g("side"))
        qty = _num(g("quantity"))
        price = _num(g("price"))
        essentials_ok = bool(td and ticker and side != OTHER and qty is not None)
        if essentials_ok:
            parsed_ok += 1

        txns.append({
            "id": f"t{i+1}",
            "employee": employee,
            "trade_date": iso(td),
            "settle_date": None,
            "ticker": ticker or None,
            "cusip": (g("cusip") or None),
            "security_name": g("security_name"),
            "side": side,
            "quantity": qty,
            "price": price,
            "principal": round(price * qty, 2) if (price is not None and qty is not None) else None,
            "broker": broker,
            "account_last4": account_last4,
            "source_file": src,
            "source_row": i + 2,  # +1 header, +1 to 1-index
            "parse_ok": essentials_ok,
            "parse_confidence": None,  # set at file level below
        })

    confidence = round(parsed_ok / len(txns), 3) if txns else 0.0
    for t in txns:
        t["parse_confidence"] = confidence
    return txns, confidence, cmap


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--employee", required=True)
    ap.add_argument("--broker", default="")
    ap.add_argument("--account-last4", default=None)
    ap.add_argument("--template", default=None, help="JSON column-map file")
    args = ap.parse_args()

    template = None
    if args.template:
        from common import load_json
        template = load_json(args.template)

    txns, conf, cmap = parse(args.input, args.employee, args.broker, template, args.account_last4)
    dump_json(txns, args.output)
    print(f"Parsed {len(txns)} rows from {os.path.basename(args.input)} at confidence {conf}.")
    print(f"Column map used: {cmap}")
    if conf < 0.85:
        print("WARNING: low parse confidence — SKILL.md guardrails say HOLD for review, do not auto-send.")
