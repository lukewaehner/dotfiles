#!/usr/bin/env python3
"""
warrant_arb.py - Warrant volatility-arbitrage engine.

ROLE: VANILLA (no-knockout) borrow-adjusted IV + break-even borrow. For SPAC/de-SPAC warrants that carry
a redemption feature (almost all of them), this OVERSTATES cheapness because it ignores the $18
redemption that truncates the upside tail -- the HEADLINE engine is warrant_knockout_mc.py (knockout-aware).
Use this script as the upper-bound reference, for the break-even-borrow view, or for warrants with
genuinely no redemption feature.

Given a company-issued warrant (a long-dated call), the actual stock-borrow rate,
the realized vol of the stock, and the listed-option ATM implied vol, this:
  - backs out the warrant's BORROW-ADJUSTED implied vol (the only honest read),
  - finds the BREAK-EVEN borrow (where the warrant stops being cheap),
  - reports greeks, a cheap/fair/rich verdict, sizing, and a re-rate P&L table.

Why borrow dominates: a warrant lives for years, so the borrow term e^(-borrow*t)
compounds heavily and is the single biggest driver of its value. Listed options
(days/weeks) are borrow-insensitive. So the warrant's "headline" implied vol from a
terminal (which usually assumes ~0 borrow) is misleading -- re-solve it at the real
stock-loan borrow before comparing to anything.

Usage:
  python warrant_arb.py inputs.json            # prints summary, writes <inputs>.results.json
  python warrant_arb.py inputs.json --borrow 0.05   # override borrow
See inputs.example.json for the schema.

Default model: Black-Scholes with a Merton cost-of-carry term (borrow as a continuous yield). It is the
transparent workhorse and is fine for the borrow-vs-break-even verdict, but it does NOT model the
warrant's redemption/call boundary or share dilution. If those matter (the stock is near the redemption
trigger, or there's a large warrant overhang), switch to a model that does -- e.g. a binomial tree that
imposes the redemption boundary -- per SKILL.md "Choosing the pricing model". This file is short and
meant to be extended or replaced when a better-fitting model is warranted.
"""
import json, sys, math, argparse
from math import log, sqrt, exp, erf

def _N(x): return 0.5*(1+erf(x/sqrt(2)))
def _n(x): return math.exp(-x*x/2)/sqrt(2*math.pi)

def bs_call(S,K,t,sig,r,q):
    """European call with continuous carry; q = borrow (acts like a dividend yield)."""
    if t<=0 or sig<=0: return max(0.0, S*exp(-q*t)-K*exp(-r*t))
    d1=(log(S/K)+(r-q+sig*sig/2)*t)/(sig*sqrt(t)); d2=d1-sig*sqrt(t)
    return S*exp(-q*t)*_N(d1)-K*exp(-r*t)*_N(d2)

def greeks(S,K,t,sig,r,q):
    d1=(log(S/K)+(r-q+sig*sig/2)*t)/(sig*sqrt(t)); d2=d1-sig*sqrt(t)
    delta=exp(-q*t)*_N(d1)
    gamma=exp(-q*t)*_n(d1)/(S*sig*sqrt(t))
    vega=S*exp(-q*t)*_n(d1)*sqrt(t)/100.0   # per 1 vol POINT
    theta=(-(S*exp(-q*t)*_n(d1)*sig)/(2*sqrt(t)) - r*K*exp(-r*t)*_N(d2) + q*S*exp(-q*t)*_N(d1))/365.0
    return dict(delta=delta,gamma=gamma,vega=vega,theta=theta)

def implied_vol(px,S,K,t,r,q,lo=0.02,hi=4.0):
    for _ in range(200):
        m=(lo+hi)/2
        if bs_call(S,K,t,m,r,q)>px: hi=m
        else: lo=m
    return (lo+hi)/2

def breakeven_borrow(px,S,K,t,r,target_iv,lo=0.0,hi=0.8):
    """Borrow at which warrant implied vol == target_iv (monotonic increasing in borrow)."""
    for _ in range(200):
        m=(lo+hi)/2
        if implied_vol(px,S,K,t,r,m) < target_iv: lo=m
        else: hi=m
    return (lo+hi)/2

def run(cfg, borrow_override=None):
    S=cfg["spot"]; px=cfg["warrant_price"]; K=cfg["strike"]
    t=cfg.get("expiry_years") or cfg["expiry_days"]/365.0
    r=cfg.get("rate",0.04); q=cfg["borrow"] if borrow_override is None else borrow_override
    listed=cfg["listed_front_iv"]; rv=cfg.get("realized",{})
    N=cfg.get("size_warrants",10000)
    shares_per=cfg.get("shares_per_warrant",1.0)

    wv=implied_vol(px,S,K,t,r,q)
    g=greeks(S,K,t,wv,r,q)
    be=breakeven_borrow(px,S,K,t,r,listed)

    # comparison set (apples-to-apples uses the longest realized window available)
    long_hv_key=next((k for k in ("HV100","HV60","HV50","HV30","HV10") if k in rv), None)
    long_hv=rv.get(long_hv_key)
    edge_vs_listed=listed-wv
    edge_vs_realized=(long_hv-wv) if long_hv is not None else None

    # verdict
    if wv < listed-0.05 and (long_hv is None or wv < long_hv):
        verdict="CHEAP"
    elif wv > listed+0.03: verdict="RICH"
    else: verdict="FAIR"

    # IV vs borrow grid (chart A)
    grid=[]
    bmax=max(0.20, math.ceil((be+0.04)*100)/100)
    steps=10
    for i in range(steps+1):
        b=bmax*i/steps
        grid.append([round(b,4), round(implied_vol(px,S,K,t,r,b)*100,1)])

    # sizing
    premium=N*px; vega_usd=N*g["vega"]; deltas=N*g["delta"]*shares_per
    hedge_sh=round(deltas); carry_yr=hedge_sh*S*q; theta_usd=N*g["theta"]

    # re-rate P&L (vega-only) toward realized / listed
    targets=sorted(set([round(wv*100)+5, round(wv*100)+10,
                        round(listed*100)] + ([round(long_hv*100)] if long_hv else []) ))
    targets=[x for x in targets if x>wv*100]
    rerate=[]
    for tv in targets:
        pnl=(bs_call(S,K,t,tv/100.0,r,q)-px)*N
        rerate.append(dict(target_iv=tv, pnl=round(pnl), pct=round(pnl/premium*100)))

    return dict(
        inputs=dict(ticker=cfg.get("ticker"), warrant=cfg.get("warrant_ticker"),
                    asof=cfg.get("asof"), spot=S, warrant_price=px, strike=K,
                    expiry_years=round(t,3), rate=r, borrow=q, listed_front_iv=listed, realized=rv),
        warrant_iv=round(wv*100,1),
        greeks={k:round(v,4) for k,v in g.items()},
        breakeven_borrow=round(be*100,1),
        breakeven_cushion=round((be-q)*100,1),
        edge_vs_listed_pts=round(edge_vs_listed*100,1),
        edge_vs_realized_pts=(round(edge_vs_realized*100,1) if edge_vs_realized is not None else None),
        realized_benchmark=long_hv_key,
        verdict=verdict,
        iv_vs_borrow=grid,
        vol_stack=dict(warrant=round(wv*100,1), listed_front=round(listed*100,1),
                       **{k:round(v*100,1) for k,v in rv.items()}),
        sizing=dict(size_warrants=N, premium=round(premium), vega_usd_per_pt=round(vega_usd),
                    hedge_shares=hedge_sh, borrow_carry_per_yr=round(carry_yr),
                    theta_usd_per_day=round(theta_usd,1)),
        rerate_pnl=rerate,
        redemption_trigger=cfg.get("redemption_trigger"),
    )

def fmt(res):
    i=res["inputs"]; L=[]
    L.append(f"=== {i.get('ticker')} / {i.get('warrant')}  warrant vol-arb  ({i.get('asof')}) ===")
    L.append(f"spot {i['spot']}  warrant {i['warrant_price']}  strike {i['strike']}  {i['expiry_years']}y  borrow {i['borrow']*100:.1f}%")
    L.append(f"WARRANT IV (borrow-adj) = {res['warrant_iv']}%   ->   VERDICT: {res['verdict']}")
    if res['edge_vs_realized_pts'] is not None:
        L.append(f"  edge vs listed {i['listed_front_iv']*100:.0f}%: {res['edge_vs_listed_pts']:+g} pts  |  vs realized {res['realized_benchmark']}: {res['edge_vs_realized_pts']:+g} pts")
    else:
        L.append(f"  edge vs listed {i['listed_front_iv']*100:.0f}%: {res['edge_vs_listed_pts']:+g} pts")
    L.append(f"  break-even borrow {res['breakeven_borrow']}% (cushion {res['breakeven_cushion']:+} pts from actual)")
    g=res['greeks']; L.append(f"  greeks: delta {g['delta']:.2f}  vega ${g['vega']:.4f}/pt  gamma {g['gamma']:.4f}  theta ${g['theta']:.5f}/day")
    s=res['sizing']; L.append(f"  per {s['size_warrants']:,} wt: premium ${s['premium']:,} | vega +${s['vega_usd_per_pt']:,}/pt | "
             f"hedge short {s['hedge_shares']:,} sh | carry ${s['borrow_carry_per_yr']:,}/yr")
    L.append("  re-rate P&L: "+" | ".join(f"->{x['target_iv']}%: ${x['pnl']:,} ({x['pct']:+}%)" for x in res['rerate_pnl']))
    return "\n".join(L)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("inputs"); ap.add_argument("--borrow",type=float,default=None)
    ap.add_argument("--out",default=None)
    a=ap.parse_args()
    cfg=json.load(open(a.inputs))
    res=run(cfg,a.borrow)
    print(fmt(res))
    out=a.out or a.inputs.rsplit(".",1)[0]+".results.json"
    json.dump(res,open(out,"w"),indent=2)
    print("\nwrote",out)
