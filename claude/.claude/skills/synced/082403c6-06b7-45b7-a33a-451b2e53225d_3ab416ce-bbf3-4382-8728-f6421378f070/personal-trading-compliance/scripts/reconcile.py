"""
reconcile.py — classify every broker transaction and match it against the approvals ledger.

This is the deterministic core. All the JUDGMENT (reading emails, classifying odd securities,
SPAC/restricted lookups, restricted-identity verification) happens upstream in Claude/MCP and
arrives here as plain JSON, so the actual pass/fail logic is auditable and repeatable.

MATCHING RULE: employees place limit / market orders, so the executed quantity and price will NOT
equal the pre-clearance request. Quantity and price are INFORMATIONAL — never a violation. A DEFAULT
transaction is approved when there is an APPROVED request for the same ticker and same side whose
day-only clearance window contains the trade date.

REASON RULE (why a trade is flagged): the flag reason is anchored to the trade's OWN side and date
("No SELL approval covered ABC on 2026-06-05."). An approval may be named in a reason ONLY IF its
day-only window contains the trade date; an out-of-window approval (even same ticker/side, even a
wrong-side approval a few days off) neither covers nor explains the trade and is never cited. This
is what stops a mis-cited reason like "approved to Buy, but traded Sell" pointing at an approval
dated a week away from the trade.

Inputs (JSON):
  approvals.json       normalized ledger (build_ledger.py)
  transactions.json    normalized transactions (parse_report.py or hand-extracted)
  restricted_map.json  {TICKER: {"restricted":bool,"is_spac":bool,"reason":str}}  (VERIFIED rlst-check/spac-details)
  classification.json  {TICKER: "spac|restricted|broad_etf|single_stock_etf|non_reportable|default|unknown"}
Optional:
  --review-reasons FILE  {TICKER: "why this must go to a human"} — forces NEEDS_REVIEW with that
                         exact reason (used e.g. for an rlst hit we could not confirm by CIK/name).
  --identity-map FILE    {SYMBOL: {"canonical": SYM, "reason": ...}} — AI-judged ticker identity so
                         a decorated broker symbol joins its approval (e.g. "BTC XYZ ABC" -> BTC,
                         "BRK.B" -> BRKB). Resolved on BOTH the approval and the report symbol, so
                         map every variant to one canonical. Applied ONLY to the approval<->trade
                         join; restricted / SPAC / classification lookups stay on the REPORTED symbol
                         so an alias can never mask a prohibited hit.

Usage:
  python reconcile.py approvals.json transactions.json restricted_map.json classification.json \
      reconciliation.json --employee "Rishi Chauhan" --quarter "Q2 2026" \
      [--review-reasons review_reasons.json] [--exempt-last4 9999] [--confidence-threshold 0.85]
"""
from __future__ import annotations
import sys, os, argparse
sys.path.insert(0, os.path.dirname(__file__))
from common import (norm_ticker, side_compatible, load_json, dump_json, OTHER, parse_date, iso,
                    OK, UNAPPROVED, TRADED_WHILE_DISAPPROVED, PROHIBITED_SPAC, PROHIBITED_RESTRICTED,
                    EXEMPT_PRECLEARANCE, NON_REPORTABLE, APPROVED_NOT_TRADED, NEEDS_REVIEW,
                    EXCEPTION_STATUSES, STATUS_LABEL)
from clearance_window import trade_in_window, resolve_window

_BUCKET_TO_STATUS = {
    "spac": PROHIBITED_SPAC,
    "restricted": PROHIBITED_RESTRICTED,
    "non_reportable": NON_REPORTABLE,
    "broad_etf": EXEMPT_PRECLEARANCE,
}
_DEFAULT_BUCKETS = {"single_stock_etf", "default"}


def _decision_day(appr):
    """The single calendar day a decision applies to: decision_date, else request_date.

    Clearance/disapproval is day-only, so a decision only speaks to ONE date. Used to test
    whether a disapproval actually lands on the trade date."""
    return parse_date(appr.get("decision_date")) or parse_date(appr.get("request_date"))


def _bucket_for(tx, restricted_map, classification, exempt_last4, review_reasons):
    """Return (terminal_status_or_None, note). If None, the tx needs approval matching."""
    tkr = norm_ticker(tx.get("ticker"))
    # 1. Certified no-control / discretionary account -> out of scope entirely (Manual §4c).
    if tx.get("account_last4") and str(tx["account_last4"]) in exempt_last4:
        return NON_REPORTABLE, "certified exempt account (no control)"
    # 2. Can't trust the row -> review, never judge.
    if not tx.get("parse_ok", True):
        return NEEDS_REVIEW, "row did not parse cleanly"
    if not tkr:
        return NEEDS_REVIEW, "no ticker/identifier"
    # 3. Explicit human-review override (e.g. an rlst hit we could not confirm was the same issuer).
    if tkr in review_reasons:
        return NEEDS_REVIEW, review_reasons[tkr]
    # 4. Live restricted / SPAC check (VERIFIED upstream) overrides the classification bucket.
    rm = restricted_map.get(tkr, {})
    if rm.get("is_spac"):
        return PROHIBITED_SPAC, rm.get("reason") or "SPAC instrument"
    if rm.get("restricted"):
        return PROHIBITED_RESTRICTED, rm.get("reason") or "on firm Restricted List"
    # 5. Classification bucket.
    bucket = (classification.get(tkr) or "unknown").lower()
    if bucket in _BUCKET_TO_STATUS:
        return _BUCKET_TO_STATUS[bucket], f"classified {bucket}"
    if bucket in _DEFAULT_BUCKETS:
        return None, bucket  # needs matching
    return NEEDS_REVIEW, f"unclassified security ({bucket})"


def reconcile(approvals, transactions, restricted_map, classification,
              employee=None, quarter=None, exempt_last4=None, confidence_threshold=0.85,
              review_reasons=None, identity_map=None):
    exempt_last4 = set(str(x) for x in (exempt_last4 or []))
    review_reasons = {norm_ticker(k): v for k, v in (review_reasons or {}).items()}
    restricted_map = {norm_ticker(k): v for k, v in restricted_map.items()}
    classification = {norm_ticker(k): v for k, v in classification.items()}
    # Ticker-identity (alias) map — AI judgement, applied ONLY to join an approval to a trade.
    # {symbol -> {"canonical": SYM, "reason": ...}}, resolved on BOTH approval and report symbols.
    # Restricted / SPAC / classification lookups deliberately stay on the REPORTED symbol (in
    # _bucket_for) so an alias can never mask a prohibited hit.
    identity_map = {norm_ticker(k): v for k, v in (identity_map or {}).items()}

    def resolve(t):
        """Canonicalize a symbol for JOIN purposes only (map hit -> canonical, else itself)."""
        entry = identity_map.get(norm_ticker(t))
        if entry and entry.get("canonical"):
            return norm_ticker(entry["canonical"])
        return norm_ticker(t)

    appr_state = []
    for a in approvals:
        usable = (str(a.get("decision", "")).upper() == "APPROVED"
                  and not a.get("needs_review")
                  and resolve_window(a)[0] is not None)
        appr_state.append({"appr": a, "usable": usable, "touched": False})

    def same_security(tx_key):
        """Approvals whose identity-resolved ticker equals this trade's resolved key."""
        return [s for s in appr_state if resolve(s["appr"].get("ticker")) == tx_key]

    results = []
    for tx in sorted(transactions, key=lambda t: (parse_date(t.get("trade_date")) or parse_date("2999-12-31"))):
        terminal, note = _bucket_for(tx, restricted_map, classification, exempt_last4, review_reasons)
        if terminal is not None:
            results.append({**tx, "status": terminal, "reason": note or STATUS_LABEL[terminal],
                            "matched_approval": None})
            continue

        tkr, side = norm_ticker(tx.get("ticker")), tx.get("side")
        if side == OTHER or side is None:
            results.append({**tx, "status": NEEDS_REVIEW, "reason": "unrecognized side",
                            "matched_approval": None})
            continue

        trade_date = tx.get("trade_date")
        td_iso = iso(trade_date) or (trade_date or "an unstated date")
        st = same_security(resolve(tkr))

        # A trade is APPROVED only by a same-side approval whose DAY-ONLY window contains the
        # trade date. Quantity/price stay informational (see module header / MATCHING RULE).
        matches = [s for s in st if s["usable"] and side_compatible(side, s["appr"].get("side"))
                   and trade_in_window(trade_date, s["appr"])]
        if matches:
            s = matches[0]
            s["touched"] = True
            results.append({**tx, "status": OK,
                            "reason": f"Approved: {side} {tkr} was cleared for {td_iso} "
                                      f"(quantity & price not required).",
                            "matched_approval": s["appr"]["id"]})
            continue

        # -- No valid approval. Build the reason DETERMINISTICALLY and anchor it to THIS trade's
        # own side and date. The single rule that fixes mis-cited reasons:
        #   An approval may drive/appear in the reason ONLY IF its day-only window contains the
        #   trade date. An approval on any OTHER day -- even the same ticker and side, and even a
        #   wrong-side approval nearby -- is out of window, so it neither covers nor explains this
        #   trade and is therefore NOT named here. This prevents "approved to Buy, but traded Sell"
        #   from citing an approval dated a week away from the trade.
        #
        # The one case that earns its own (more serious) status is a request for THIS ticker and
        # THIS side that the CCO DISAPPROVED *on the trade date itself* -- told to stand down and
        # traded anyway. A disapproval on any other day is not "traded while disapproved"; it is
        # just an unapproved trade for this date (the default reason below).
        trade_d = parse_date(trade_date)
        disapproved_today = [
            s for s in st
            if str(s["appr"].get("decision", "")).upper() == "DISAPPROVED"
            and side_compatible(side, s["appr"].get("side"))
            and trade_d is not None and _decision_day(s["appr"]) == trade_d
        ]
        if disapproved_today:
            results.append({**tx, "status": TRADED_WHILE_DISAPPROVED,
                            "reason": f"Traded while disapproved: the request to {side} {tkr} on "
                                      f"{td_iso} was disapproved that day.",
                            "matched_approval": disapproved_today[0]["appr"]["id"]})
            continue

        # Default: no same-side clearance was in force for this ticker on this exact trade date.
        # Date + side anchored, uniform for every unmatched trade (right-side/wrong-day,
        # wrong-side/same-day, wrong-side/wrong-day, or nothing on file all land here).
        results.append({**tx, "status": UNAPPROVED,
                        "reason": f"No {side} approval covered {tkr} on {td_iso}.",
                        "matched_approval": None})

    approvals_out = []
    for s in appr_state:
        a = dict(s["appr"])
        dec = str(a.get("decision", "")).upper()
        if a.get("needs_review"):
            a["usage"], a["status"] = "NEEDS_REVIEW", NEEDS_REVIEW
        elif dec == "PENDING":
            a["usage"], a["status"] = "PENDING", NEEDS_REVIEW
        elif dec == "APPROVED" and not s["touched"]:
            a["usage"], a["status"] = "UNUSED", APPROVED_NOT_TRADED
        elif dec == "APPROVED":
            a["usage"], a["status"] = "USED", None
        else:
            a["usage"], a["status"] = "DISAPPROVED", None
        approvals_out.append(a)

    summary = {}
    for r in results:
        summary[r["status"]] = summary.get(r["status"], 0) + 1

    exceptions = [r for r in results if r["status"] in EXCEPTION_STATUSES]
    low_conf = any((t.get("parse_confidence") is not None and t["parse_confidence"] < confidence_threshold)
                   for t in transactions)
    needs_review = ([r for r in results if r["status"] == NEEDS_REVIEW]
                    + [a for a in approvals_out if a.get("status") == NEEDS_REVIEW])

    return {
        "employee": employee, "quarter": quarter,
        "transactions": results, "approvals": approvals_out,
        "summary": summary, "exceptions": exceptions, "needs_review": needs_review,
        "has_exceptions": bool(exceptions), "has_needs_review": bool(needs_review),
        "low_confidence": low_conf,
        "auto_send_ok": bool(exceptions) and not needs_review and not low_conf,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("approvals"); ap.add_argument("transactions")
    ap.add_argument("restricted_map"); ap.add_argument("classification")
    ap.add_argument("output")
    ap.add_argument("--employee", default=None); ap.add_argument("--quarter", default=None)
    ap.add_argument("--exempt-last4", default="")
    ap.add_argument("--review-reasons", default=None)
    ap.add_argument("--identity-map", default=None)
    ap.add_argument("--confidence-threshold", type=float, default=0.85)
    args = ap.parse_args()

    out = reconcile(
        load_json(args.approvals), load_json(args.transactions),
        load_json(args.restricted_map), load_json(args.classification),
        employee=args.employee, quarter=args.quarter,
        exempt_last4=[x for x in args.exempt_last4.split(",") if x],
        confidence_threshold=args.confidence_threshold,
        review_reasons=load_json(args.review_reasons) if args.review_reasons else None,
        identity_map=load_json(args.identity_map) if args.identity_map else None,
    )
    dump_json(out, args.output)
    print(f"{args.employee or ''} {args.quarter or ''}: {out['summary']}")
    print(f"exceptions={len(out['exceptions'])} needs_review={len(out['needs_review'])} "
          f"low_confidence={out['low_confidence']} -> auto_send_ok={out['auto_send_ok']}")
