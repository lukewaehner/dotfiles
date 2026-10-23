#!/usr/bin/env python3
"""
render_note.py  -  Trading Note (Fast) deterministic renderer.

Takes ONE json bundle (raw Meteora MCP payloads + the few model-distilled
strings) and prints the COMPLETE note: header block, unit notation, prices,
C-T, thesis, ORDERS, the VWAP-centered yield matrix, and the footer.

ALL arithmetic and ALL fixed-width / markdown formatting happen here so the
model never has to compute a yield or count a padding space. The model's only
job is to fetch the payloads and distill the thesis / non-managing / s-4 /
extension fields, then run this script and print its stdout verbatim.

Usage:
    python3 render_note.py input.json
    cat input.json | python3 render_note.py

Input JSON schema (see references/input_schema.md for the full spec):
{
  "ticker": "IPCX",
  "today": "2026-06-26",                 # optional; defaults to system date (ET)
  "thesis": "....",                       # model-distilled, 3-4 sentences
  "non_managing_members": "....",         # model-distilled; "" if doc silent
  "sf4_count": "2 (per memory doc)",      # in-deal only; null/"" otherwise
  "ext_per_share_per_month": 0,           # 0 if doc records none
  "ext_active_since": null,               # "mm/dd/yyyy" or null
  "ext_deposits_to_date": null,           # int or null
  "ext_lump_period_days": null,           # int -> lump-sum cadence variant
  "ext_silent": false,                    # true => in-deal/post-anniv but doc silent
  "spac_details": { ... },                # raw spac-details payload
  "prices":  { ... },                     # raw get-price payload (has .results)
  "orders":  { ... }                      # raw emsx-blotter payload (has .orders)
}
"""

import sys, json, math
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP

# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #

def rhu(x, places=2):
    """round half-up (Decimal) -> float; None-safe."""
    if x is None:
        return None
    q = Decimal(10) ** -places
    return float(Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP))

def money(x, places=2):
    if x is None:
        return None
    return f"${rhu(x, places):,.{places}f}"

def signed_money(x):
    if x is None:
        return "N/A"
    v = rhu(x, 2)
    sign = "-" if v < 0 else "+"
    return f"{sign}${abs(v):,.2f}"

def commas(x):
    try:
        return f"{int(round(float(x))):,}"
    except (TypeError, ValueError):
        return "N/A"

def is_invalid_ticker(t):
    if t is None:
        return True
    s = str(t).strip()
    if s == "" or s == "0" or s.lower() == "none" or s.lower() == "null":
        return True
    if s.startswith("#N/A") or s.upper().startswith("#N/A"):
        return True
    return False

def parse_date(s):
    if not s:
        return None
    s = str(s)
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s[:10], fmt).date()
        except ValueError:
            continue
    return None

def fmt_date(d):
    return d.strftime("%m/%d/%Y") if d else "N/A"

def norm_tkr(t):
    """strip Bloomberg suffixes/exchange codes for matching."""
    if t is None:
        return ""
    s = str(t).upper().strip()
    for suf in (" US EQUITY", " UQ EQUITY", " UN EQUITY", " UW EQUITY",
                " UR EQUITY", " EQUITY", " INDEX", " CURNCY"):
        if s.endswith(suf):
            s = s[: -len(suf)]
            break
    return s.replace(" ", "")

def fmt_k(v):
    """share-count k-notation for equity orders."""
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "--"
    if abs(v) < 1000:
        return str(int(round(v)))
    s = f"{v/1000:.1f}".rstrip("0").rstrip(".")
    return f"{s}k"

# --------------------------------------------------------------------------- #
# price selection
# --------------------------------------------------------------------------- #

def get_price_row(prices, *candidates):
    """match a get-price result to one of several candidate tickers."""
    results = prices.get("results", []) if isinstance(prices, dict) else []
    wanted = {norm_tkr(c) for c in candidates if not is_invalid_ticker(c)}
    if not wanted:
        return None
    for r in results:
        if norm_tkr(r.get("ticker")) in wanted:
            return r
    return None

def _num(x):
    try:
        if x is None:
            return None
        return float(x)
    except (TypeError, ValueError):
        return None

def select_common(row, market_status, sheet_price):
    """common selection ladder. returns (price, method, reason, bid, ask)."""
    if row is None:
        return (sheet_price, "sheet", "no live quote", None, None)
    bid, ask, mid = _num(row.get("bid")), _num(row.get("ask")), _num(row.get("mid"))
    last = _num(row.get("last_trade"))
    close = _num(row.get("last_regular_close"))
    bs, asz = _num(row.get("bid_size")), _num(row.get("ask_size"))
    if mid is None and bid is not None and ask is not None:
        mid = (bid + ask) / 2.0
    off_hours = str(market_status).lower() in ("pre_market", "after_hours", "pre-market", "after-hours")

    reasons = []
    if bid is not None and ask is not None:
        spread = ask - bid
        if spread > 0.10:
            reasons.append("wide spread")
        if mid and mid > 0 and (spread / mid) > 0.005:
            reasons.append("wide spread")
    if (bs is not None and bs <= 500) or (asz is not None and asz <= 500):
        reasons.append("stub size")
    if mid is not None and close is not None and abs(mid - close) > 0.10 and off_hours:
        reasons.append("mid drifted from close")
    if row.get("_stale_warning"):
        reasons.append("stale ref")

    if mid is not None and not reasons:
        return (mid, "mid", None, bid, ask)
    if last is not None:
        reason = reasons[0] if reasons else "mid unreliable"
        return (last, "last_trade", reason, bid, ask)
    if mid is not None:
        return (mid, "mid", None, bid, ask)
    if sheet_price is not None:
        return (sheet_price, "sheet", "no live quote", bid, ask)
    return (None, None, "no price", bid, ask)

def select_wr(row, sheet_price):
    """warrant / rights ladder (relaxed sub-dollar thresholds)."""
    if row is None:
        return (sheet_price, "sheet") if sheet_price is not None else (None, None)
    bid, ask, mid = _num(row.get("bid")), _num(row.get("ask")), _num(row.get("mid"))
    last = _num(row.get("last_trade"))
    close = _num(row.get("last_regular_close"))
    bs, asz = _num(row.get("bid_size")), _num(row.get("ask_size"))
    if mid is None and bid is not None and ask is not None:
        mid = (bid + ask) / 2.0

    bad = False
    if bid is not None and ask is not None and mid and mid > 0:
        if (ask - bid) / mid > 0.25:
            bad = True
    if (bs is not None and bs <= 500) or (asz is not None and asz <= 500):
        bad = True
    if mid is not None and close is not None and abs(mid - close) > 0.10:
        bad = True

    if mid is not None and not bad:
        return (mid, "mid")
    if last is not None:
        return (last, "last_trade")
    if mid is not None:
        return (mid, "mid")
    if sheet_price is not None:
        return (sheet_price, "sheet")
    return (None, None)

# --------------------------------------------------------------------------- #
# unit notation
# --------------------------------------------------------------------------- #

def _unit_term(letter, spec):
    if spec is None:
        return None
    s = str(spec).strip().lower()
    if s in ("none", "null", "", "0"):
        return None
    if s in ("1", "1/1", "1 for 1"):
        return f"+{letter}"
    if s.startswith("1/") and s[2:].isdigit():
        return f"+{letter}/{s[2:]}"
    if s.startswith("1 for 1/"):
        d = s.split("1 for 1/")[-1].strip()
        if d.isdigit():
            return f"+{letter}/{d}"
    # fallback: render literally
    return f"+{letter}({spec})"

def unit_notation(sd):
    w = _unit_term("W", sd.get("warrants_in_unit"))
    r = _unit_term("R", sd.get("rights_in_unit"))
    out = "U=S"
    if w:
        out += w
    if r:
        out += r
    return out

# --------------------------------------------------------------------------- #
# yield math
# --------------------------------------------------------------------------- #

def yield_cell(price, cit, tbill, today, D, ext_pm, ext_period_days):
    if price is None or price <= 0 or cit is None or D is None:
        return None
    days = (D - today).days
    if days <= 0:
        return None
    trust_accrual = cit * tbill * days / 365.0
    if ext_period_days:
        ext = ext_pm * math.floor(days / ext_period_days)
    else:
        ext = ext_pm * (days / 30.4375)
    cit_exit = cit + trust_accrual + ext
    total_ret = cit_exit / price - 1.0
    return total_ret * 365.0 / days

def scenario_rows(sd, today):
    """ordered, days>0 filtered, coincident-date deduped scenario list."""
    spec = [("EST", "est_date"), ("6 MON", "six_month_date"),
            ("9 MON", "nine_month_date"), ("12 MON", "twelve_month_date"),
            ("MAX", "max_date")]
    raw = []
    for label, key in spec:
        d = parse_date(sd.get(key))
        if d and (d - today).days > 0:
            raw.append((label, d))
    # dedup coincident dates -> slash-joined label, canonical order preserved
    by_date = {}
    order = []
    for label, d in raw:
        if d not in by_date:
            by_date[d] = []
            order.append(d)
        by_date[d].append(label)
    rows = []
    for d in order:
        rows.append(("/".join(by_date[d]), d))
    return rows

# --------------------------------------------------------------------------- #
# ORDERS block
# --------------------------------------------------------------------------- #

_MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def contract_name(order):
    """equity -> bloomberg ticker as-is; option -> compact 'Oct 16/26 C9'."""
    t = str(order.get("ticker", "")).strip()
    if str(order.get("yellow_key", "")).lower() == "equity":
        return t
    # option: reformat 'SYM US 10/16/2026 C9' -> 'Oct 16/26 C9'
    import re
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})\s+([CP][\d.]+)", t)
    if m:
        mm, dd, yyyy, cp = m.groups()
        try:
            return f"{_MONTHS[int(mm)]} {int(dd)}/{yyyy[2:]} {cp}"
        except (ValueError, IndexError):
            return t
    return t

def fmt_orders(orders_payload):
    orders = orders_payload.get("orders", []) if isinstance(orders_payload, dict) else []
    working = [o for o in orders if str(o.get("status", "")).upper() == "WORKING"]
    if not working:
        return ""

    equity_mode = any(
        str(o.get("yellow_key", "")).lower() == "equity" and _num(o.get("limit_price")) and _num(o.get("limit_price")) >= 1.0
        for o in working
    )
    if equity_mode:
        W = {"Ord": 5, "Fill": 5, "Rem": 5, "Avg": 6, "Lmt": 5}
    else:
        W = {"Ord": 4, "Fill": 4, "Rem": 4, "Avg": 5, "Lmt": 4}
    CW = 20  # contract width

    def share(v):
        return fmt_k(v) if equity_mode else (str(int(round(_num(v)))) if _num(v) is not None else "--")

    def is_opt(o):
        return str(o.get("yellow_key", "")).lower() != "equity"

    def cell_share(o, v):
        return str(int(round(_num(v)))) if is_opt(o) and _num(v) is not None else share(v)

    def row(prefix, contract, cells, header=False):
        line = prefix + f"{contract:<{CW}}"
        for label, val, w in cells:
            line += " | "
            line += f"{val:<{w}}" if header else f"{val:>{w}}"
        return line.rstrip() if header else line

    def block(side):
        os_ = [o for o in working if str(o.get("side", "")).upper() == side]
        if not os_:
            return []
        os_.sort(key=lambda o: (str(o.get("ticker", "")), _num(o.get("limit_price")) or 0))
        cols = ["Ord", "Fill", "Rem", "Avg", "Lmt"] if side == "SELL" else ["Ord", "Fill", "Rem", "Lmt"]
        prefix = "SELL: " if side == "SELL" else "BUY:  "
        lines = [row(prefix, "Contract", [(c, c, W[c]) for c in cols], header=True)]
        for o in os_:
            avg = _num(o.get("avg_price"))
            avg_s = f"{avg:.3f}" if (avg and avg > 0) else "--"
            lmt = _num(o.get("limit_price"))
            lmt_s = f"{lmt:.2f}" if lmt is not None else "--"
            valmap = {
                "Ord": cell_share(o, o.get("amount")),
                "Fill": cell_share(o, o.get("filled")),
                "Rem": cell_share(o, o.get("remain_balance")),
                "Avg": avg_s,
                "Lmt": lmt_s,
            }
            lines.append(row("      ", contract_name(o), [(c, valmap[c], W[c]) for c in cols]))
        return lines

    out = ["---", "ORDERS"]
    out += block("SELL")
    out += block("BUY")
    return "\n".join(out)

# --------------------------------------------------------------------------- #
# assemble
# --------------------------------------------------------------------------- #

def build(inp):
    sd = inp["spac_details"]
    prices = inp.get("prices", {}) or {}
    orders = inp.get("orders", {}) or {}
    stage = sd.get("stage", "predeal")
    today = parse_date(inp.get("today")) or date.today()
    market_status = prices.get("market_status")

    ticker = sd.get("spac_ticker") or inp.get("ticker")
    w_tkr = sd.get("warrant_ticker")
    r_tkr = sd.get("rights_ticker")
    u_tkr = sd.get("unit_ticker")
    w_valid = not is_invalid_ticker(w_tkr)
    r_valid = not is_invalid_ticker(r_tkr)
    u_valid = not is_invalid_ticker(u_tkr)

    # ---- prices ----
    c_row = get_price_row(prices, ticker)
    common_px, c_method, c_reason, c_bid, c_ask = select_common(
        c_row, market_status, _num(sd.get("common_price")))

    w_px = w_method = None
    if w_valid:
        w_row = get_price_row(prices, w_tkr, f"{w_tkr}/WS", f"{w_tkr} US Equity")
        w_px, w_method = select_wr(w_row, _num(sd.get("warrants_price")))

    r_px = r_method = None
    if r_valid:
        r_row = get_price_row(prices, r_tkr)
        r_px, r_method = select_wr(r_row, _num(sd.get("rights_price")))

    # ---- tbill ----
    tb_row = get_price_row(prices, "USGG3M Index", "USGG3M")
    tbill_default = False
    if tb_row is not None:
        tb = _num(tb_row.get("mid")) or _num(tb_row.get("last_trade")) or _num(tb_row.get("bid"))
        tbill = (tb / 100.0) if tb is not None else 0.0366
        if tb is None:
            tbill_default = True
    else:
        tbill, tbill_default = 0.0366, True

    cit = _num(sd.get("cash_in_trust"))
    ct = (common_px - cit) if (common_px is not None and cit is not None) else None

    ext_pm = _num(inp.get("ext_per_share_per_month")) or 0.0
    ext_period_days = inp.get("ext_lump_period_days")
    ext_silent = bool(inp.get("ext_silent"))

    # ---- header block lines ----
    L = []
    L.append("IN DEAL" if stage == "indeal" else "PRE DEAL")

    # tickers line
    tline = [f"{{{ticker} US Equity}}"]
    if w_valid:
        tline.append(f"{{{w_tkr} US Equity}}")
    if r_valid:
        tline.append(f"{{{r_tkr} US Equity}}")
    L.append(" ".join(tline))

    # positions
    pos = [f"C Position: {commas(sd.get('common_position'))}"]
    if stage != "indeal" and u_valid:
        pos.append(f"U Position: {commas(sd.get('units_position'))}")
    if w_valid:
        pos.append(f"W Position: {commas(sd.get('warrants_position'))}")
    if r_valid:
        pos.append(f"R Position: {commas(sd.get('rights_position'))}")
    L.append("; ".join(pos))

    # unit notation
    L.append(f"Unit: {unit_notation(sd)}")

    # prices line
    pl = []
    if common_px is not None:
        pl.append(f"[{ticker}]: {money(common_px)}")
    if w_valid and w_px is not None:
        pl.append(f"[{w_tkr}]: {money(w_px)}")
    if r_valid and r_px is not None:
        pl.append(f"[{r_tkr}]: {money(r_px)}")
    if pl:
        L.append(", ".join(pl))

    # dom / uw / bucket / category (+ s-4 in-deal)
    def na(v):
        return "N/A" if (v is None or str(v).strip() in ("", "0", "None", "null")) else v
    dom_label = "Dom" if stage == "indeal" else "Domicile"
    bucket = sd.get("bucket")
    bucket_s = "N/A" if bucket is None else (str(int(bucket)) if float(bucket) == int(bucket) else str(bucket))
    dline = f"{dom_label}: {na(sd.get('domicile'))}; UW: {na(sd.get('underwriter'))}; Bucket: {bucket_s}; Category: {na(sd.get('category'))}"
    if stage == "indeal":
        sf4 = inp.get("sf4_count")
        dline += f"; s/f-4s: {sf4 if sf4 else 'not in doc'}"
    L.append(dline)

    # trust balance (in-deal) + CIT / C-T
    if stage == "indeal" and _num(sd.get("trust_balance")) is not None:
        L.append(f"Trust balance: {money(sd.get('trust_balance'))}mm")
    L.append(f"CIT: {money(cit)}; C-T: {signed_money(ct)}")

    # common o/s + 9.9%
    L.append(f"Common O/S: {commas(sd.get('common_outstanding'))}; 9.9%: {commas(sd.get('pct_9_outstanding'))}")

    if stage == "indeal":
        tgt = sd.get("target")
        if tgt:
            tgt = str(tgt).replace("Announced: ", "").strip()
            L.append(f"In deal with: {tgt}")
        # PIPE rollout line
        pipe = sd.get("pipe_size")
        if pipe is None:
            pipe_s = "N/A"
        elif _num(pipe) == 0:
            pipe_s = "None disclosed"
        else:
            p = _num(pipe)
            if p == int(p):
                pipe_s = f"${int(p)}mm"
            elif p < 1:
                pipe_s = f"${p:.2f}mm"
            else:
                pipe_s = f"${p:.1f}mm".replace(".0mm", "mm")
        L.append(f"PIPE: {pipe_s} (per spac-insider)")
        if sd.get("deal_announced"):
            L.append(f"Announced: {fmt_date(parse_date(sd.get('deal_announced')))}")
        L.append(f"Deadline: {fmt_date(parse_date(sd.get('deadline')))}; Outside Date: {fmt_date(parse_date(sd.get('outside_date')))}")
        L.append(f"IPO Date: {fmt_date(parse_date(sd.get('ipo_date')))}")
    else:
        ipo_line = f"IPO Date: {fmt_date(parse_date(sd.get('ipo_date')))}"
        if _num(sd.get("ipo_proceeds")) is not None:
            ipo_line += f"; IPO proceeds: {money(sd.get('ipo_proceeds'))}mm;"
        L.append(ipo_line)
        L.append(f"Liquidation Deadline: {fmt_date(parse_date(sd.get('liquidation_deadline')))}")

    # non-managing + thesis
    nmm = inp.get("non_managing_members", "")
    if nmm is None:
        nmm = ""
    L.append(f'Non-Managing Members: "{nmm}"')
    L.append(f"Thesis: {inp.get('thesis', '').strip()}")

    # orders
    ob = fmt_orders(orders)
    if ob:
        L.append(ob)

    note_block = "```\n" + "\n".join(L) + "\n```"

    # ---- yield matrix ----
    matrix = build_matrix(sd, today, cit, tbill, common_px, c_bid, c_ask,
                          ext_pm, ext_period_days)

    # ---- footer ----
    foot = []
    px_note = ""
    if c_method == "last_trade":
        sp = f"{c_bid:.2f}" if c_bid is not None else "--"
        sa = f"{c_ask:.2f}" if c_ask is not None else "--"
        px_note = f" (last_trade — mid unreliable: spread ${sp} x ${sa}, {c_reason})"
    tbill_note = " (DEFAULT — live rate fetch failed)" if tbill_default else " (USGG3M)"
    foot.append(f"Yields computed @ Tbill = {tbill*100:.2f}%{tbill_note}, px = {money(common_px)}{px_note}")

    if ext_pm and ext_pm > 0:
        if ext_period_days:
            foot.append(f"Extensions: {money(ext_pm)}/sh per {ext_period_days//30 or ext_period_days}-mo period (per memory doc)")
        else:
            line = f"Extensions: {money(ext_pm)}/sh/mo (per memory doc)"
            if inp.get("ext_active_since"):
                line += f", active since {inp['ext_active_since']}"
            if inp.get("ext_deposits_to_date") is not None:
                line += f", {inp['ext_deposits_to_date']} deposits to date"
            foot.append(line)
    elif ext_silent:
        foot.append("Extensions: not in doc — yields may be understated; use trading-note-extended to verify")

    if w_method == "last_trade" and w_valid:
        foot.append(f"[{w_tkr}] px = {money(w_px)} (last_trade — mid unreliable)")
    if r_method == "last_trade" and r_valid:
        foot.append(f"[{r_tkr}] px = {money(r_px)} (last_trade — mid unreliable)")

    vwap = _num(sd.get("vwap_5d"))
    if not vwap or vwap < 1:
        foot.append("Matrix centered on selected price — no valid 5d VWAP")
    elif common_px is not None and abs(vwap - common_px) > 0.10:
        foot.append(f"VWAP {money(vwap)} vs px {money(common_px)} — tape moved since 5d window; bid/ask cols anchor actionable levels")

    footer_block = "```\n" + "\n".join(foot) + "\n```"

    return note_block + "\n\n" + matrix + "\n\n" + footer_block

def build_matrix(sd, today, cit, tbill, common_px, c_bid, c_ask, ext_pm, ext_period_days):
    vwap = _num(sd.get("vwap_5d"))
    centered_on_vwap = bool(vwap and vwap >= 1)
    center = rhu(vwap, 2) if centered_on_vwap else rhu(common_px, 2)
    center_label = "VWAP" if centered_on_vwap else "Px"
    if center is None:
        return "Yield matrix unavailable — insufficient price data"

    # columns: -3c..+3c, then Bid, Ask
    steps = [("−3c", center - 0.03), ("−2c", center - 0.02), ("−1c", center - 0.01),
             (center_label, center), ("+1c", center + 0.01),
             ("+2c", center + 0.02), ("+3c", center + 0.03)]
    cols = [(lbl, rhu(p, 2)) for lbl, p in steps if p > 0]
    if c_bid is not None:
        cols.append(("Bid", rhu(c_bid, 2)))
    if c_ask is not None:
        cols.append(("Ask", rhu(c_ask, 2)))
    if len(cols) < 2:
        return "Yield matrix unavailable — insufficient price data"

    rows = scenario_rows(sd, today)
    if not rows:
        return "Yield matrix unavailable — no future scenario dates"

    # header annotation
    ann = f"YIELD MATRIX — centered on {center_label} = {money(center)}"
    if not centered_on_vwap:
        ann += " (no valid 5d VWAP)"
    ann += f", Bid = {money(c_bid) if c_bid is not None else '--'}, Ask = {money(c_ask) if c_ask is not None else '--'}"
    if ext_pm and ext_pm > 0:
        ann += f"; w/ extensions ({money(ext_pm)}/sh/mo, per memory doc)"

    # table
    head = "| Yield | " + " | ".join(lbl for lbl, _ in cols) + " |"
    sep = "|" + "---|" * (len(cols) + 1)
    price_row = "| Price | " + " | ".join(money(p) for _, p in cols) + " |"
    body = [head, sep, price_row]
    for label, D in rows:
        cells = []
        for _, p in cols:
            y = yield_cell(p, cit, tbill, today, D, ext_pm, ext_period_days)
            cells.append(f"{y*100:.2f}%" if y is not None else "--")
        body.append(f"| {label} ({fmt_date(D)}) | " + " | ".join(cells) + " |")

    return ann + "\n\n" + "\n".join(body)

# --------------------------------------------------------------------------- #

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            inp = json.load(f)
    else:
        inp = json.load(sys.stdin)
    sys.stdout.write(build(inp) + "\n")

if __name__ == "__main__":
    main()
