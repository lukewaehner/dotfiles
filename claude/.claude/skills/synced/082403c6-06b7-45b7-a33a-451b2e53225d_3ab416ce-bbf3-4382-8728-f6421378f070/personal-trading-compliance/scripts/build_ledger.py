"""
build_ledger.py — normalize model-extracted pre-clearance requests into a clean approvals ledger.

The pre-clearance emails are read and extracted by Claude (see SKILL.md) into a raw JSON array.
This script does the deterministic part: normalize the side vocabulary, parse dates, coerce
quantities, validate required fields, and flag anything ambiguous as needs_review (never guessed).

Usage:
    python build_ledger.py raw_approvals.json approvals.json

Raw record fields accepted (all optional except noted):
    employee (req), request_date (req), decision (req: Approved/Disapproved/Pending),
    decision_date, clearance_valid_through, ticker (req), cusip, security_name, security_type,
    side (req), quantity, is_ipo_or_pp, source_message_id
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import (normalize_side, parse_date, iso, norm_ticker, load_json, dump_json,
                    OTHER)

_DECISIONS = {"approved": "APPROVED", "disapproved": "DISAPPROVED",
              "denied": "DISAPPROVED", "rejected": "DISAPPROVED", "pending": "PENDING",
              "approve": "APPROVED", "disapprove": "DISAPPROVED", "yes": "APPROVED", "no": "DISAPPROVED"}


def _decision(raw):
    return _DECISIONS.get(str(raw or "").strip().lower(), "PENDING")


def _num(raw):
    if raw is None or raw == "":
        return None
    try:
        return float(str(raw).replace(",", "").replace("$", "").strip())
    except ValueError:
        return None


def normalize_approval(rec: dict, idx: int) -> dict:
    side = normalize_side(rec.get("side") or rec.get("transaction_type"))
    qty = _num(rec.get("quantity") if rec.get("quantity") is not None else rec.get("number_of_shares"))
    decision = _decision(rec.get("decision"))

    review_reasons = []
    if not rec.get("ticker") and not rec.get("cusip"):
        review_reasons.append("no ticker/identifier")
    if side == OTHER:
        review_reasons.append("unrecognized side")
    # Quantity is informational only (limit/market orders won't match exactly), so a missing
    # quantity does NOT force review — the match is ticker + side + date.
    if parse_date(rec.get("request_date")) is None:
        review_reasons.append("no request date")
    if decision == "PENDING":
        review_reasons.append("no clear approve/disapprove decision")

    return {
        "id": rec.get("id") or f"a{idx+1}",
        "employee": rec.get("employee"),
        "request_date": iso(rec.get("request_date")),
        "decision": decision,
        "decision_date": iso(rec.get("decision_date")) or iso(rec.get("request_date")),
        "clearance_valid_through": iso(rec.get("clearance_valid_through")),
        "ticker": norm_ticker(rec.get("ticker")) or None,
        "cusip": (rec.get("cusip") or None),
        "security_name": rec.get("security_name"),
        "security_type": rec.get("security_type"),
        "side": side,
        "quantity": qty,
        "is_ipo_or_pp": bool(rec.get("is_ipo_or_pp")),
        "source_message_id": rec.get("source_message_id"),
        "needs_review": bool(review_reasons),
        "review_reason": "; ".join(review_reasons),
    }


def build(raw_records):
    return [normalize_approval(r, i) for i, r in enumerate(raw_records)]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    raw = load_json(sys.argv[1])
    ledger = build(raw)
    dump_json(ledger, sys.argv[2])
    flagged = sum(1 for a in ledger if a["needs_review"])
    print(f"Wrote {len(ledger)} approvals to {sys.argv[2]} ({flagged} need review).")
