"""
clearance_window.py — resolve the valid trading window for a pre-clearance approval.

Meteora policy (Compliance Manual §3, Pre-clearance): a clearance is effective ONLY for the
day of the request, UNLESS the CCO explicitly granted a longer window ("Pre-clearance sought
through (date)"). This module makes that rule deterministic and auditable so date matching is
never a judgment call: an unused approval simply expires, and a next-day / good-till-cancelled
fill without a fresh approval falls outside every window.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import parse_date


def resolve_window(approval: dict):
    """Return (start_date, end_date) of the valid trading window, or (None, None) if it
    cannot be determined (missing dates). Only APPROVED requests get a real window.

    - start = decision_date if present, else request_date (the day clearance took effect).
    - end   = clearance_valid_through if the CCO granted it AND it is >= start; else = start
              (day-only). We only honor a multi-day window when the request was APPROVED.
    """
    if str(approval.get("decision", "")).upper() != "APPROVED":
        return (None, None)

    start = parse_date(approval.get("decision_date")) or parse_date(approval.get("request_date"))
    if start is None:
        return (None, None)

    through = parse_date(approval.get("clearance_valid_through"))
    if through is not None and through >= start:
        return (start, through)
    return (start, start)


def trade_in_window(trade_date, approval: dict) -> bool:
    """True if trade_date falls within the approval's valid window (inclusive)."""
    td = parse_date(trade_date)
    if td is None:
        return False
    start, end = resolve_window(approval)
    if start is None:
        return False
    return start <= td <= end


def describe_window(approval: dict) -> str:
    start, end = resolve_window(approval)
    if start is None:
        return "no valid window (not approved / missing date)"
    if start == end:
        return f"valid {start.isoformat()} only (day-only)"
    return f"valid {start.isoformat()} through {end.isoformat()}"


if __name__ == "__main__":
    # Quick manual check.
    demo = {"decision": "APPROVED", "request_date": "2026-04-06", "clearance_valid_through": None}
    print(describe_window(demo), "| 2026-04-06 in window:", trade_in_window("2026-04-06", demo),
          "| 2026-04-07 in window:", trade_in_window("2026-04-07", demo))
