"""
common.py — shared helpers for the personal-trading compliance pipeline.

Keeps the vocabulary and small utilities in one place so every script normalizes
sides, dates, and statuses identically. Imported by the other scripts.
"""
from __future__ import annotations
import json
import os
import re
from datetime import date, datetime

# ---------------------------------------------------------------------------
# Canonical transaction sides
# ---------------------------------------------------------------------------
BUY, SELL, SHORT, COVER, OTHER = "BUY", "SELL", "SHORT", "COVER", "OTHER"

# Map the many ways brokers/employees phrase a side onto the canonical enum.
_SIDE_MAP = {
    "buy": BUY, "bought": BUY, "b": BUY, "buy to open": BUY, "bto": BUY,
    "purchase": BUY, "purchased": BUY, "long buy": BUY, "buy long": BUY,
    "sell": SELL, "sold": SELL, "s": SELL, "sell to close": SELL, "stc": SELL,
    "sale": SELL, "sell long": SELL, "long sell": SELL,
    "short": SHORT, "sell short": SHORT, "ss": SHORT, "short sell": SHORT,
    "sell to open": SHORT, "sto": SHORT, "short sale": SHORT,
    "cover": COVER, "buy to cover": COVER, "btc": COVER, "cover short": COVER,
    "short cover": COVER, "long cover": COVER, "buy to close": COVER, "btc short": COVER,
}


def normalize_side(raw) -> str:
    """Return a canonical side, or OTHER if it can't be recognized."""
    if raw is None:
        return OTHER
    key = re.sub(r"[^a-z ]", "", str(raw).strip().lower())
    key = re.sub(r"\s+", " ", key).strip()
    return _SIDE_MAP.get(key, OTHER)


def side_compatible(executed: str, approved: str) -> bool:
    """An executed side is covered only by an approval for the SAME side.
    Buying is not covered by a sell approval; covering a short is not a sell, etc."""
    return executed == approved and executed in (BUY, SELL, SHORT, COVER)


# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------
_DATE_FORMATS = [
    "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d-%b-%Y", "%d-%b-%y",
    "%b %d, %Y", "%B %d, %Y", "%m-%d-%Y", "%Y/%m/%d", "%m.%d.%Y",
]


def parse_date(raw):
    """Parse a date from common formats. Returns a datetime.date or None."""
    if raw is None or raw == "":
        return None
    if isinstance(raw, datetime):
        return raw.date()
    if isinstance(raw, date):
        return raw
    s = str(raw).strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    # last resort: ISO prefix like 2026-04-06T...
    try:
        return datetime.fromisoformat(s[:10]).date()
    except ValueError:
        return None


def iso(d) -> str | None:
    if d is None:
        return None
    if isinstance(d, str):
        pd = parse_date(d)
        return pd.isoformat() if pd else None
    return d.isoformat()


# ---------------------------------------------------------------------------
# Reconciliation status constants
# ---------------------------------------------------------------------------
OK = "OK"
UNAPPROVED = "UNAPPROVED"
QTY_OVER_APPROVED = "QTY_OVER_APPROVED"  # retained for compatibility; NOT emitted (see below)
TRADED_WHILE_DISAPPROVED = "TRADED_WHILE_DISAPPROVED"
PROHIBITED_SPAC = "PROHIBITED_SPAC"
PROHIBITED_RESTRICTED = "PROHIBITED_RESTRICTED"
EXEMPT_PRECLEARANCE = "EXEMPT_PRECLEARANCE"
NON_REPORTABLE = "NON_REPORTABLE"
APPROVED_NOT_TRADED = "APPROVED_NOT_TRADED"
NEEDS_REVIEW = "NEEDS_REVIEW"

# Statuses that are an employee-facing exception (drive the notice email).
# NOTE: quantity/price differences are NOT exceptions — employees use limit/market orders, so the
# executed size/price won't equal the pre-clearance request. Matching is ticker + side + date only.
EXCEPTION_STATUSES = {
    UNAPPROVED, TRADED_WHILE_DISAPPROVED,
    PROHIBITED_SPAC, PROHIBITED_RESTRICTED,
}

# Human-readable one-liners for the notice / Excel "Reason" column.
STATUS_LABEL = {
    OK: "Approved and within terms",
    UNAPPROVED: "No matching pre-clearance approval on file",
    QTY_OVER_APPROVED: "Traded more than the approved quantity",
    TRADED_WHILE_DISAPPROVED: "Traded despite a disapproved request",
    PROHIBITED_SPAC: "SPAC — prohibited for employee accounts",
    PROHIBITED_RESTRICTED: "On the firm Restricted List — prohibited",
    EXEMPT_PRECLEARANCE: "Broad ETF/ETN — reportable, no pre-clearance required",
    NON_REPORTABLE: "Not a Reportable Security — out of scope",
    APPROVED_NOT_TRADED: "Approved but no matching trade",
    NEEDS_REVIEW: "Needs human review — do not auto-judge",
}


# ---------------------------------------------------------------------------
# Tiny IO helpers (always UTF-8 so Windows doesn't mangle characters)
# ---------------------------------------------------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(obj, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, default=str)


def norm_ticker(t) -> str:
    return re.sub(r"\s+", "", str(t or "").upper())
