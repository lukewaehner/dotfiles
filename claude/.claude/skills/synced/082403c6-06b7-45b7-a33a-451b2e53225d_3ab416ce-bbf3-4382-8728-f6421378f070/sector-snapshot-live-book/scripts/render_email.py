# render_email.py  (Python 3, stdlib only)
# Turns tables.json (from refresh_and_extract.ps1) into a compact, Outlook-safe
# HTML email: three tables with green/red shading + a crisp, data-driven takeaway
# under each, computed straight from the live values. Static styling lives in one
# <style> block; per-cell color uses the bgcolor attribute (works everywhere).
import json, sys, html as _html

CAP = 0.15  # return magnitude that maps to full color intensity
GREEN = (22, 163, 74)
RED = (220, 38, 38)

def _blend(base, a): return tuple(round(255*(1-a) + b*a) for b in base)
def _hex(rgb): return "#%02X%02X%02X" % rgb

def is_num(v): return isinstance(v, (int, float)) and not isinstance(v, bool)

def shade2(v):
    """(bg_hex, is_dark) for a signed fraction, else (None, False)."""
    if not is_num(v): return (None, False)
    a = min(abs(v) / CAP, 1.0) * 0.85
    bg = _hex(_blend(GREEN if v >= 0 else RED, a))
    return (bg, a > 0.5)

def fmt_pct(v, dec=1):
    return f"{v*100:+.{dec}f}%" if is_num(v) else _html.escape("" if v is None else str(v))
def fmt_price(v, dec=2):
    return f"${v:.{dec}f}" if is_num(v) else _html.escape("" if v is None else str(v))
def fmt_tier(v):
    if is_num(v): return str(int(v)) if float(v).is_integer() else f"{v:g}"
    return _html.escape("" if v is None else str(v))
def fmt_text(v):
    if v is None: return ""
    if is_num(v) and float(v).is_integer(): return str(int(v))
    return _html.escape(str(v))

STYLE = (".t{border-collapse:collapse;font:12px Arial,Helvetica,sans-serif;color:#111}"
         ".t td{padding:4px 8px;border:1px solid #d9d9d9;white-space:nowrap;text-align:right}"
         ".t td.h{background:#f0f0f0;font-weight:bold;text-align:center;border:1px solid #cfcfcf}"
         ".t td.l{text-align:left}.t td.c{text-align:center}.t td.w{color:#fff}")

# ---- cell / row / header rendering ----
def render_cell(kind, do_shade, v):
    if kind == "pct1": disp = fmt_pct(v, 1)
    elif kind == "pct2": disp = fmt_pct(v, 2)
    elif kind == "price": disp = fmt_price(v, 2)
    elif kind == "tier": disp = fmt_tier(v)
    else: disp = fmt_text(v)
    classes = []
    if kind == "text": classes.append("l")
    elif kind in ("tier", "ctext"): classes.append("c")
    bgattr = ""
    if do_shade:
        bg, dark = shade2(v)
        if bg:
            bgattr = f' bgcolor="{bg}"'
            if dark: classes.append("w")
    cls = f' class="{" ".join(classes)}"' if classes else ""
    return f"<td{cls}{bgattr}>{disp}</td>"

def render_rows(rows, colspec):
    out = []
    for row in rows:
        if all((c is None or c == "") for c in row): continue
        tds = [render_cell(k, s, (row[i] if i < len(row) else None)) for i, (k, s) in enumerate(colspec)]
        out.append("<tr>" + "".join(tds) + "</tr>")
    return "\n".join(out)

def th(text, colspan=1, rowspan=1, align="center"):
    span = (f' colspan="{colspan}"' if colspan > 1 else "") + (f' rowspan="{rowspan}"' if rowspan > 1 else "")
    cls = "h l" if align == "left" else "h"
    return f'<td class="{cls}"{span}>{_html.escape(text)}</td>'

def table_block(title, what, takeaway, header_html, body_html):
    return (f'<div style="margin:0 0 26px 0;">'
            f'<div style="font:bold 15px Arial,Helvetica,sans-serif;color:#111;margin:0 0 3px;">{_html.escape(title)}</div>'
            f'<div style="font:12px Arial,Helvetica,sans-serif;color:#666;margin:0 0 3px;">{what}</div>'
            f'<div style="font:12px Arial,Helvetica,sans-serif;color:#111;margin:0 0 8px;"><b>Today:</b> {takeaway}</div>'
            f'<table class="t" cellspacing="0" cellpadding="0">{header_html}{body_html}</table></div>')

# ---- takeaway helpers ----
def _pairs(rows, idx): return [(r, r[idx]) for r in rows if idx < len(r) and is_num(r[idx])]
def _best(rows, idx):
    p = _pairs(rows, idx); return max(p, key=lambda x: x[1]) if p else None
def _worst(rows, idx):
    p = _pairs(rows, idx); return min(p, key=lambda x: x[1]) if p else None
def esc(s): return _html.escape(str(s))

def heatmap_takeaway(rows):
    n = len(rows); green = sum(1 for r in rows if is_num(r[1]) and r[1] > 0)
    b, w, yb = _best(rows, 3), _worst(rows, 3), _best(rows, 4)
    if not (b and w and yb): return f"{green}/{n} sectors higher on the day."
    return (f"{green}/{n} sectors green on the day. 1-mo momentum: {esc(b[0][0])} leads ({fmt_pct(b[1])}), "
            f"{esc(w[0][0])} worst ({fmt_pct(w[1])}); YTD leader {esc(yb[0][0])} ({fmt_pct(yb[1])}).")

def scorecard_takeaway(rows):
    n = len(rows); rich, cheap = _best(rows, 1), _worst(rows, 1)
    sgov = sum(1 for r in rows if is_num(r[8]) and r[8] > 0)
    hyg = sum(1 for r in rows if is_num(r[5]) and r[5] > 0)
    if not (rich and cheap): return f"{sgov}/{n} sectors beating trust (SGOV) YTD."
    return (f"Richest to trust: {esc(rich[0][0])} ({fmt_pct(rich[1],2)}); cheapest {esc(cheap[0][0])} ({fmt_pct(cheap[1],2)}). "
            f"{sgov}/{n} sectors beating trust (SGOV) YTD, {hyg}/{n} beating credit (HYG).")

def warrant_takeaway(rows):
    n = len(rows); led = sum(1 for r in rows if is_num(r[9]) and r[9] > 0)
    lead, lag = _best(rows, 10), _worst(rows, 10)
    if not (lead and lag): return f"{led}/{n} warrants outran their sector this week."
    return (f"{led}/{n} warrants outran their sector this week. 1-mo standouts: {esc(lead[0][1])} led its theme "
            f"({fmt_pct(lead[1])}), {esc(lag[0][1])} lagged ({fmt_pct(lag[1])}).")

# ---- table builders ----
def build_heatmap(rows):
    hdr = "<tr>" + th("Sector", align="left") + th("1D") + th("1W") + th("1M") + th("YTD") + th("1Y") + "</tr>"
    cols = [("text", False)] + [("pct1", True)] * 5
    what = "Equal-weight index return per sector. Green = up, red = down — a quick read on where money moved across our themes."
    return table_block("Sector Heatmap — Index Returns", what, heatmap_takeaway(rows), hdr, render_rows(rows, cols))

def build_scorecard(rows):
    r1 = ("<tr>" + th("Sector", rowspan=2, align="left") + th("Current State", colspan=2)
          + th("Performance vs HYG", colspan=3) + th("Performance vs SGOV", colspan=3) + "</tr>")
    r2 = ("<tr>" + th("Avg Prem/(Disc)") + th("Above/Below Trust") + th("1M") + th("6M") + th("YTD")
          + th("1M") + th("6M") + th("YTD") + "</tr>")
    cols = [("text", False), ("pct2", False), ("ctext", False)] + [("pct1", True)] * 6
    what = ("Per-sector book state (avg premium/discount to trust, names above/below) and how the names performed "
            "vs HYG (credit) and SGOV (≈ trust). Green = beating the baseline.")
    return table_block("SPAC Scorecard — State vs. Performance", what, scorecard_takeaway(rows), r1 + r2, render_rows(rows, cols))

def build_warrant(rows):
    r1 = ("<tr>" + th("Common", rowspan=2, align="left") + th("Warrant", rowspan=2, align="left")
          + th("Sector", rowspan=2, align="left") + th("Tier", rowspan=2) + th("Wt VWAP (10d)", rowspan=2)
          + th("Warrant Return", colspan=2) + th("Sector Return", colspan=2) + th("Lead / Lag (W−S)", colspan=2) + "</tr>")
    r2 = "<tr>" + th("1W") + th("1M") + th("1W") + th("1M") + th("1W") + th("1M") + "</tr>"
    cols = [("text", False), ("text", False), ("text", False), ("tier", False), ("price", False)] + [("pct1", True)] * 6
    what = ("Each warrant's return vs its sector's, so Lead/Lag isolates the name-specific move from the theme. "
            "Green = warrant beat its sector; red = trailed.")
    return table_block("Warrant Watch — Theme Participation", what, warrant_takeaway(rows), r1 + r2, render_rows(rows, cols))

# ---- assemble ----
def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "out/tables.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "out/email.html"
    with open(src, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    hm = [r for r in data["heatmap"][4:] if r and r[0]]
    sc = [r for r in data["scorecard"][4:] if r and r[0]]
    ww = [r for r in data["warrant"][4:] if r and r[0]]
    asof = data.get("generated_local", "")
    n = len(hm); green = sum(1 for r in hm if is_num(r[1]) and r[1] > 0)
    yb, yw = _best(hm, 4), _worst(hm, 4)
    overall = f"{green}/{n} sectors green on the day."
    if yb and yw:
        overall += (f" YTD, {esc(yb[0][0])} ({fmt_pct(yb[1])}) leads and {esc(yw[0][0])} ({fmt_pct(yw[1])}) lags.")
    body = build_heatmap(hm) + build_scorecard(sc) + build_warrant(ww)
    doc = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f'<style>{STYLE}</style></head>'
        '<body style="margin:0;padding:0;background:#ffffff;">'
        '<div style="max-width:920px;font:13px Arial,Helvetica,sans-serif;color:#111;padding:6px 2px;">'
        '<div style="font:bold 18px Arial,Helvetica,sans-serif;margin:0 0 2px;">Overall Sector Snapshot &amp; Live Book</div>'
        f'<div style="font:12px Arial,Helvetica,sans-serif;color:#666;margin:0 0 10px;">Live Bloomberg pull &middot; as of {_html.escape(asof)}</div>'
        f'<div style="font:13px Arial,Helvetica,sans-serif;color:#111;margin:0 0 18px;padding:8px 10px;background:#f6f8fa;border:1px solid #e3e7ea;">{overall}</div>'
        f'{body}'
        '<div style="font:11px Arial,Helvetica,sans-serif;color:#999;margin:14px 0 0;border-top:1px solid #eee;padding-top:8px;">'
        'Auto-generated from &ldquo;Sector Indices &mdash; Testing.xlsx&rdquo;. Percentages are Bloomberg change fields '
        '(1W = CHG_PCT_5D). Green = positive / beating baseline, red = negative. Not investment advice.</div>'
        '</div></body></html>')
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    sys.stdout.write(f"WROTE {out} ({len(doc)} chars); sectors={n} warrants={len(ww)}\n")

if __name__ == "__main__":
    main()
