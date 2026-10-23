"""
write_excel.py — write the per-employee compliance workbook and update the master summary.

Per-employee workbook (<Employee>_PersonalTrading.xlsx):
  - Summary       quarter, counts by status, overall result, notice status
  - Approvals     the quarter's ledger + usage (USED/PARTIAL/UNUSED/APPROVED_NOT_TRADED)
  - Transactions  every broker line with Status / Reason / Matched Approval (flagged rows colored)
  - Needs-Review  only the items held for a human (never auto-sent)
  - History       prior quarters appended (re-running a quarter overwrites just that quarter)

Master (_Master_Compliance_Summary.xlsx): one row per employee per quarter for the CCO.

Usage:
  python write_excel.py reconciliation.json --out-dir ./books --master ./books/_Master_Compliance_Summary.xlsx \
      [--notice "auto-sent 2026-07-10" ]
"""
from __future__ import annotations
import sys, os, argparse, re
sys.path.insert(0, os.path.dirname(__file__))
from common import (load_json, EXCEPTION_STATUSES, NEEDS_REVIEW, OK, EXEMPT_PRECLEARANCE,
                    NON_REPORTABLE, APPROVED_NOT_TRADED, STATUS_LABEL)
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

HEAD = Font(bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="1F3864")
FILLS = {
    "exception": PatternFill("solid", fgColor="F4CCCC"),   # red-ish
    "ok": PatternFill("solid", fgColor="D9EAD3"),          # green-ish
    "review": PatternFill("solid", fgColor="FCE5CD"),      # amber
    "muted": PatternFill("solid", fgColor="EFEFEF"),       # gray
}


def _fill_for(status):
    if status in EXCEPTION_STATUSES:
        return FILLS["exception"]
    if status == NEEDS_REVIEW:
        return FILLS["review"]
    if status == OK:
        return FILLS["ok"]
    if status in (EXEMPT_PRECLEARANCE, NON_REPORTABLE, APPROVED_NOT_TRADED):
        return FILLS["muted"]
    return None


def _safe(name):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(name or "employee")).strip("_")


def _sheet(wb, title):
    if title in wb.sheetnames:
        del wb[title]
    return wb.create_sheet(title)


def _header(ws, cols):
    ws.append(cols)
    for c in ws[1]:
        c.font = HEAD
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical="center")


def write_employee_book(recon, out_dir, notice=""):
    os.makedirs(out_dir, exist_ok=True)
    emp = recon.get("employee") or "employee"
    quarter = recon.get("quarter") or ""
    path = os.path.join(out_dir, f"{_safe(emp)}_PersonalTrading.xlsx")
    wb = openpyxl.load_workbook(path) if os.path.exists(path) else openpyxl.Workbook()
    if "Sheet" in wb.sheetnames and wb["Sheet"].max_row == 1 and wb["Sheet"].max_column == 1:
        del wb["Sheet"]

    # --- Summary ---
    s = _sheet(wb, "Summary")
    s.append([f"Personal-Trading Compliance — {emp}"]); s["A1"].font = Font(bold=True, size=14)
    s.append([f"Quarter: {quarter}"])
    result = "EXCEPTIONS" if recon.get("has_exceptions") else ("REVIEW" if recon.get("has_needs_review") else "PASS")
    s.append([f"Result: {result}"]); s["A3"].font = Font(bold=True)
    s.append([f"Notice: {notice or ('held for review' if recon.get('has_needs_review') else 'n/a')}"])
    s.append([f"Auto-send eligible: {recon.get('auto_send_ok')}  |  Low confidence: {recon.get('low_confidence')}"])
    s.append([])
    s.append(["Status", "Count"]);
    for c in s[s.max_row]:
        c.font = HEAD; c.fill = HEAD_FILL
    for status, n in sorted(recon.get("summary", {}).items()):
        s.append([f"{status} — {STATUS_LABEL.get(status, '')}", n])

    # --- Transactions ---
    t = _sheet(wb, "Transactions")
    cols = ["Trade Date", "Ticker", "Security", "Side", "Quantity", "Price", "Broker",
            "Acct", "Status", "Reason", "Matched Approval", "Source"]
    _header(t, cols)
    for r in recon.get("transactions", []):
        t.append([r.get("trade_date"), r.get("ticker"), r.get("security_name"), r.get("side"),
                  r.get("quantity"), r.get("price"), r.get("broker"), r.get("account_last4"),
                  r.get("status"), r.get("reason"), r.get("matched_approval"),
                  f"{r.get('source_file','')}:{r.get('source_row','')}"])
        fill = _fill_for(r.get("status"))
        if fill:
            for c in t[t.max_row]:
                c.fill = fill

    # --- Approvals ---
    a = _sheet(wb, "Approvals")
    _header(a, ["Request Date", "Decision", "Valid Through", "Ticker", "Side", "Qty",
                "IPO/PP", "Usage", "Flag", "Source Msg"])
    for ap in recon.get("approvals", []):
        a.append([ap.get("request_date"), ap.get("decision"), ap.get("clearance_valid_through"),
                  ap.get("ticker"), ap.get("side"), ap.get("quantity"), ap.get("is_ipo_or_pp"),
                  ap.get("usage"), ap.get("status") or "", ap.get("source_message_id")])
        if ap.get("status") in (NEEDS_REVIEW, APPROVED_NOT_TRADED):
            for c in a[a.max_row]:
                c.fill = _fill_for(ap.get("status"))

    # --- Needs-Review ---
    nr = _sheet(wb, "Needs-Review")
    _header(nr, ["Type", "Ticker", "Date", "Side", "Qty", "Reason", "Source"])
    for r in recon.get("transactions", []):
        if r.get("status") == NEEDS_REVIEW:
            nr.append(["transaction", r.get("ticker"), r.get("trade_date"), r.get("side"),
                       r.get("quantity"), r.get("reason"),
                       f"{r.get('source_file','')}:{r.get('source_row','')}"])
    for ap in recon.get("approvals", []):
        if ap.get("status") == NEEDS_REVIEW:
            nr.append(["approval", ap.get("ticker"), ap.get("request_date"), ap.get("side"),
                       ap.get("quantity"), ap.get("review_reason") or "pending/incomplete",
                       ap.get("source_message_id")])

    # --- History (append this quarter; overwrite if re-running the same quarter) ---
    if "History" in wb.sheetnames:
        hist = wb["History"]
        kept = [[c.value for c in row] for row in hist.iter_rows(min_row=2)]
        kept = [row for row in kept if str(row[0]) != str(quarter)]
        del wb["History"]
    else:
        kept = []
    hist = wb.create_sheet("History")
    _header(hist, ["Quarter", "Trade Date", "Ticker", "Side", "Quantity", "Status", "Reason"])
    for row in kept:
        hist.append(row)
    for r in recon.get("transactions", []):
        hist.append([quarter, r.get("trade_date"), r.get("ticker"), r.get("side"),
                     r.get("quantity"), r.get("status"), r.get("reason")])

    # widen a few columns
    for ws in (t, a, nr, hist):
        for col in ws.columns:
            width = min(42, max(10, max((len(str(c.value)) if c.value is not None else 0) for c in col) + 2))
            ws.column_dimensions[col[0].column_letter].width = width

    # order sheets
    wb.move_sheet("Summary", -(wb.sheetnames.index("Summary")))
    wb.save(path)
    return path


def update_master(recon, master_path, notice=""):
    os.makedirs(os.path.dirname(os.path.abspath(master_path)), exist_ok=True)
    cols = ["Employee", "Quarter", "Result", "#Txns", "#Exceptions", "#NeedsReview",
            "Summary", "Notice", "AutoSendOK"]
    if os.path.exists(master_path):
        wb = openpyxl.load_workbook(master_path)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Master"
        _header(ws, cols)

    emp, quarter = recon.get("employee"), recon.get("quarter")
    result = "EXCEPTIONS" if recon.get("has_exceptions") else ("REVIEW" if recon.get("has_needs_review") else "PASS")
    summ = ", ".join(f"{k}:{v}" for k, v in sorted(recon.get("summary", {}).items()))
    newrow = [emp, quarter, result, len(recon.get("transactions", [])),
              len(recon.get("exceptions", [])), len(recon.get("needs_review", [])),
              summ, notice or ("held" if recon.get("has_needs_review") else ""),
              recon.get("auto_send_ok")]
    # upsert by (employee, quarter)
    target = None
    for row in ws.iter_rows(min_row=2):
        if str(row[0].value) == str(emp) and str(row[1].value) == str(quarter):
            target = row[0].row
            break
    if target:
        for j, val in enumerate(newrow, start=1):
            ws.cell(row=target, column=j, value=val)
    else:
        ws.append(newrow)
    wb.save(master_path)
    return master_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("reconciliation")
    ap.add_argument("--out-dir", default="./books")
    ap.add_argument("--master", default=None)
    ap.add_argument("--notice", default="")
    args = ap.parse_args()

    recon = load_json(args.reconciliation)
    book = write_employee_book(recon, args.out_dir, args.notice)
    print(f"Wrote {book}")
    master = args.master or os.path.join(args.out_dir, "_Master_Compliance_Summary.xlsx")
    update_master(recon, master, args.notice)
    print(f"Updated {master}")
