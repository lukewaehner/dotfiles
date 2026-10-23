#!/usr/bin/env python3
"""
implied_borrow.py - implied stock-borrow TERM STRUCTURE from listed-option put-call parity (mid).

WHY THIS EXISTS. Borrow is the single biggest driver of a long-dated warrant's value, and the whole
warrant-vol-arb verdict pivots on it. When the underlying has LISTED OPTIONS, the option market gives an
independent, market-based read on the borrow at every tenor - which you can lay against the single
desk-quoted rate and against the warrant's own implied borrow. This builds that read.

METHOD (put-call parity at mid, ATM bracket, median). For each ATM-bracket option observation
(quote date, expiry, strike, call & put bid+ask, and THAT day's spot):

    C_mid = (c_bid + c_ask)/2          P_mid = (p_bid + p_ask)/2
    T     = (expiry - quote_date) / 365
    fwd   = (C_mid - P_mid) + K * exp(-r*T)     # PCP:  C - P = S*e^{-qT} - K*e^{-rT}  =>  S*e^{-qT} = fwd
    q     = -ln(fwd / spot) / T                 # implied borrow (continuous), per observation

Observations are pooled over two trailing windows ending at as-of - 10 and 30 TRADING days (10d fresher /
noisier, 30d smoother). Per option expiry the implied borrow is the MEDIAN q of the valid ATM-bracket
observations in the window. The two median term-structures are the curves the brief plots (30d amber solid,
10d steel-blue dashed). Their mean across expiries is reported as a transparent "avg" reference line.
Optional company-warrant points are carried as stars at their (long) tenor for the option-vs-warrant
borrow cross-check.

USAGE
  python3 implied_borrow.py obs.json                 # prints summary, writes <obs>.borrow_curve.json
  python3 implied_borrow.py obs.json --out curve.json
  python3 implied_borrow.py obs.json --windows 10,30 # trading-day window lengths (default 10,30)
Then feed the curve into the desk brief:
  python3 build_brief.py inputs.knockout.json --borrow-curve <obs>.borrow_curve.json --out TICKER_brief.pdf

See references/implied_borrow.md for the obs.json schema and the Bloomberg pull.
"""
import json, argparse, math, statistics, datetime as dt

def _date(s): return dt.date.fromisoformat(s)

def busday_count(d0, d1):
    """Trading (Mon-Fri) days between two ISO date strings, sign-agnostic, holidays ignored."""
    a, b = _date(d0), _date(d1)
    if b < a: a, b = b, a
    days = (b - a).days
    full_weeks, rem = divmod(days, 7)
    n = full_weeks * 5
    wd = a.weekday()                      # 0=Mon .. 6=Sun
    for i in range(rem):
        if (wd + i) % 7 < 5: n += 1
    return n

def months_to(asof, exp): return (_date(exp) - _date(asof)).days / 30.44

def obs_q(o, r):
    """Per-observation implied borrow via put-call parity at mid. None if not solvable."""
    try:
        cm = (o["c_bid"] + o["c_ask"]) / 2.0
        pm = (o["p_bid"] + o["p_ask"]) / 2.0
        S  = o["spot"]; K = o["K"]
        T  = (_date(o["exp"]) - _date(o["date"])).days / 365.0
    except (KeyError, TypeError):
        return None
    if T <= 0 or not S or S <= 0: return None
    fwd = (cm - pm) + K * math.exp(-r * T)
    if fwd <= 0: return None              # forward must be positive to imply a borrow
    q = -math.log(fwd / S) / T * 100.0
    return dict(date=o["date"], exp=o["exp"], K=K, c_mid=round(cm, 4), p_mid=round(pm, 4),
                fwd=round(fwd, 4), q=round(q, 4))

def curve_for(rows, asof):
    """rows: obs_q dicts in one window -> per-expiry median q, sorted by months-to-expiry."""
    by = {}
    for rr in rows: by.setdefault(rr["exp"], []).append(rr["q"])
    pts = [dict(exp=e, months=round(months_to(asof, e), 2),
                q=round(statistics.median(qs), 4), n=len(qs))
           for e, qs in by.items()]
    pts.sort(key=lambda p: p["months"])
    avg = round(statistics.mean([p["q"] for p in pts]), 4) if pts else None
    return pts, avg

def run(cfg, windows=(10, 30)):
    r = cfg.get("rate", 0.043); asof = cfg["asof"]; spot = cfg.get("spot")
    allq = [q for q in (obs_q(o, r) for o in cfg.get("obs", [])) if q]
    wins = {}
    for nd in sorted(windows):
        rows = [q for q in allq if busday_count(q["date"], asof) <= nd]
        pts, avg = curve_for(rows, asof)
        wins[nd] = dict(curve=pts, avg=avg, n=len(rows))
    short, long_ = min(windows), max(windows)
    warr = [dict(label=w["label"], months=round(months_to(asof, w["exp"]), 2), q=round(w["q"], 3))
            for w in cfg.get("warrants", []) if w.get("exp") and w.get("q") is not None]
    qs_all = ([p["q"] for w in wins.values() for p in w["curve"]] + [w["q"] for w in warr]) or [10]
    ms_all = ([p["months"] for w in wins.values() for p in w["curve"]] + [w["months"] for w in warr]) or [6]
    y_max = math.ceil(max(10, max(qs_all)) / 10) * 10 + 10
    x_max = math.ceil(max(6, max(ms_all)) / 6) * 6 + 6
    return dict(
        ticker=cfg.get("ticker"), warrant=cfg.get("warrant_ticker"), asof=asof, spot=spot, rate=r,
        short_win=short, long_win=long_,
        curve_long=wins[long_]["curve"],  avg_long=wins[long_]["avg"],  n_long=wins[long_]["n"],
        curve_short=wins[short]["curve"], avg_short=wins[short]["avg"], n_short=wins[short]["n"],
        warrants=warr, y_max=y_max, x_max_months=round(x_max, 1),
    )

def fmt(R):
    L = [f"=== {R.get('ticker')} implied borrow term structure (PCP @ mid)  asof {R['asof']}  spot {R.get('spot')} ==="]
    L.append(f"{R['long_win']}d window: avg {R['avg_long']}%  ({R['n_long']} obs)   |   "
             f"{R['short_win']}d window: avg {R['avg_short']}%  ({R['n_short']} obs)")
    L.append(f"{'expiry':>12} {'months':>7} {str(R['long_win'])+'d q%':>9} {str(R['short_win'])+'d q%':>9}")
    sc = {p["exp"]: p["q"] for p in R["curve_short"]}
    for p in R["curve_long"]:
        L.append(f"{p['exp']:>12} {p['months']:>7.2f} {p['q']:>9.2f} {sc.get(p['exp'],float('nan')):>9.2f}")
    for w in R["warrants"]:
        L.append(f"  warrant {w['label']}: {w['q']:.2f}% @ {w['months']:.1f}m (star)")
    return "\n".join(L)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("obs"); ap.add_argument("--out", default=None)
    ap.add_argument("--windows", default="10,30")
    a = ap.parse_args()
    cfg = json.load(open(a.obs))
    wins = tuple(int(x) for x in a.windows.split(","))
    R = run(cfg, windows=wins)
    print(fmt(R))
    out = a.out or a.obs.rsplit(".", 1)[0] + ".borrow_curve.json"
    json.dump(R, open(out, "w"), indent=2)
    print("\nwrote", out)
