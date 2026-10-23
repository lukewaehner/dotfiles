#!/usr/bin/env python3
"""
warrant_knockout_mc.py - redemption-knockout-aware warrant vol-arb engine (the HEADLINE for SPAC warrants).

A SPAC warrant is a long-dated call subject to a soft call / KNOCKOUT: once the stock holds >= a trigger
(usually $18) for 20 of 30 trading days, the issuer can redeem for $0.01 after a ~30-day notice -- but in
that window the holder SELLS the warrant or EXERCISES (cash/cashless) and KEEPS the intrinsic; only doing
nothing yields $0.01. So the redemption does NOT remove the intrinsic upside -- it forces early conversion
and forgoes the warrant's remaining TIME VALUE. Plain Black-Scholes ignores the forced conversion and so
overstates the warrant, but for a deep-OTM name the haircut is just that time-value give-up (often only a
few vol points, since intrinsic is preserved). This engine prices the actual knockout (the residual call
the holder keeps at the trigger, not a $0.01 stub) and re-solves the redemption-adjusted ("knockout-adjusted")
implied vol.

Method: Monte-Carlo, daily GBM, antithetic, risk-neutral drift (r - borrow). On each path, the issuer
redeems on the first day the 20-of-30-day >= trigger condition is met; during the 30-day notice the holder
keeps a short residual call (valued closed-form at the trigger day), so they capture ~intrinsic-plus-a-bit,
not zero. Implied vol is read off a price-vs-vol grid (common random numbers -> smooth & monotonic), so no
slow nested bisection. Two issuer behaviours bracket the answer: redeem at first eligibility (aggressive ->
highest implied vol) and a delayed/registration-gap proxy (lenient -> lower). The midpoint is central.

Also reports the VANILLA no-knockout IV (closed-form BS + Merton carry) as the upper bound on cheapness -- the
gap to the knockout-adjusted number is how much of the apparent "edge" is really just the un-priced knockout.

Usage:
  python3 warrant_knockout_mc.py inputs.json                 # prints summary, writes <inputs>.knockout.json
  python3 warrant_knockout_mc.py inputs.json --paths 8000    # fewer MC paths (faster, noisier)
  python3 warrant_knockout_mc.py inputs.json --borrow 0.05   # what-if a different borrow
See references/inputs_schema.md for the input fields (verified strike/maturity/redemption from EDGAR).
"""
import json, sys, math, argparse
import numpy as np
from math import log, sqrt, exp, erf

def _N(x): return 0.5*(1.0+erf(x/math.sqrt(2.0)))
def Nvec(x): return 0.5*(1.0+np.vectorize(math.erf)(x/math.sqrt(2.0)))

def bs_call(S,K,t,sig,r,q):
    S=np.asarray(S,float)
    if t<=0 or sig<=0: return np.maximum(0.0, S*math.exp(-q*t)-K*math.exp(-r*t))
    d1=(np.log(S/K)+(r-q+sig*sig/2)*t)/(sig*math.sqrt(t)); d2=d1-sig*math.sqrt(t)
    return S*math.exp(-q*t)*Nvec(d1)-K*math.exp(-r*t)*Nvec(d2)
def bs_call_s(S,K,t,sig,r,q):  # scalar
    if t<=0 or sig<=0: return max(0.0, S*math.exp(-q*t)-K*math.exp(-r*t))
    d1=(log(S/K)+(r-q+sig*sig/2)*t)/(sig*sqrt(t)); d2=d1-sig*sqrt(t)
    return S*exp(-q*t)*_N(d1)-K*exp(-r*t)*_N(d2)
def bs_delta(S,K,t,sig,r,q):
    d1=(log(S/K)+(r-q+sig*sig/2)*t)/(sig*sqrt(t)); return exp(-q*t)*_N(d1)

def run(cfg, paths=14000, borrow_override=None, seed=7):
    S0=cfg["spot"]; PX=cfg["warrant_price"]; K=cfg["strike"]
    T=cfg.get("expiry_years") or cfg["expiry_days"]/365.0
    r=cfg.get("rate",0.04); q=cfg["borrow"] if borrow_override is None else borrow_override
    listed=cfg["listed_front_iv"]; rv=cfg.get("realized",{})
    trig=cfg.get("redemption_trigger",18.0); mw=cfg.get("make_whole_trigger")
    tdays=cfg.get("trigger_days",[20,30]); notice_days=cfg.get("notice_days",30)
    delay_level=cfg.get("delay_trigger_proxy", trig+4.0)
    N=cfg.get("size_warrants",10000); shares_per=cfg.get("shares_per_warrant",1.0)
    nwin, mwin = int(tdays[0]), int(tdays[1])
    NOTICE=notice_days/365.0
    NDAYS=int(round(252*T)); dt=1.0/252.0
    rng=np.random.default_rng(seed)
    Zb=rng.standard_normal((paths,NDAYS)); Z=np.concatenate([Zb,-Zb],axis=0)
    discT=math.exp(-r*T)

    def knockout_price(sig, level, S0_=None):
        S0_=S0 if S0_ is None else S0_
        drift=(r-q-0.5*sig*sig)*dt; vol=sig*math.sqrt(dt)
        S=S0_*np.exp(np.cumsum(drift+vol*Z,axis=1)); n=S.shape[0]
        ind=(S>=level).astype(np.int16); cs=np.cumsum(ind,axis=1)
        roll=cs.copy(); roll[:,mwin:]=cs[:,mwin:]-cs[:,:-mwin]
        hit=roll>=nwin; has=hit.any(axis=1); first=np.where(has,hit.argmax(axis=1),-1)
        val=np.empty(n); nt=~has
        val[nt]=np.maximum(S[nt,-1]-K,0.0)*discT
        if has.any():
            d=first[has]; Sd=S[has,d]
            val[has]=bs_call(Sd,K,NOTICE,sig,r,q)*np.exp(-r*(d.astype(float)*dt))
        return float(np.mean(val))

    def vanilla_iv(lo=0.03,hi=3.0):
        for _ in range(70):
            m=(lo+hi)/2
            if bs_call_s(S0,K,T,m,r,q)>PX: hi=m
            else: lo=m
        return (lo+hi)/2

    def interp_iv(grid_prices, grid_vols):
        for i in range(len(grid_vols)-1):
            a,b=grid_prices[i],grid_prices[i+1]
            if (a-PX)*(b-PX)<=0 and b!=a:
                return grid_vols[i]+(PX-a)*(grid_vols[i+1]-grid_vols[i])/(b-a)
        return None

    vols=[round(0.50+0.1*i,2) for i in range(11)]   # 0.50 .. 1.50
    ko_first=[knockout_price(s,trig) for s in vols]
    ko_delay=[knockout_price(s,delay_level) for s in vols]
    unc=[bs_call_s(S0,K,T,s,r,q) for s in vols]

    van=vanilla_iv()
    iv_first=interp_iv(ko_first,vols); iv_delay=interp_iv(ko_delay,vols)
    # fall back to bound if the market price is off the grid
    if iv_first is None: iv_first=vols[-1] if ko_first[-1]<PX else vols[0]
    if iv_delay is None: iv_delay=vols[-1] if ko_delay[-1]<PX else vols[0]
    central=(iv_first+iv_delay)/2.0

    # greeks on the knockout model at the central vol (finite difference)
    cv=central; dS=0.02*S0
    delta=(knockout_price(cv,trig,S0+dS)-knockout_price(cv,trig,S0-dS))/(2*dS)
    vega =(knockout_price(cv+0.005,trig)-knockout_price(cv-0.005,trig))/1.0   # per 1 vol point
    fair_listed=knockout_price(listed,trig)

    # comparison set
    long_hv_key=next((k for k in ("HV100","HV60","HV50","HV30","HV10") if k in rv),None)
    long_hv=rv.get(long_hv_key)
    # break-even borrow on the VANILLA model (closed form) -- a reference; the knockout, not borrow, usually binds
    def van_iv_at(qq):
        lo,hi=0.03,3.0
        for _ in range(60):
            m=(lo+hi)/2
            d1=(log(S0/K)+(r-qq+m*m/2)*T)/(m*sqrt(T)); d2=d1-m*sqrt(T)
            px=S0*exp(-qq*T)*_N(d1)-K*exp(-r*T)*_N(d2)
            if px>PX: hi=m
            else: lo=m
        return (lo+hi)/2
    blo,bhi=0.0,0.6
    for _ in range(60):
        bm=(blo+bhi)/2
        if van_iv_at(bm)<listed: blo=bm
        else: bhi=bm
    be_van=(blo+bhi)/2

    # verdict on the CONSERVATIVE (aggressive-redemption) end of the band
    floor=min(listed, long_hv) if long_hv is not None else listed
    if iv_first < floor-0.05: verdict="CHEAP"
    elif iv_delay > listed+0.03: verdict="RICH"
    else: verdict="FAIR"

    curve=[[int(vols[i]*100), round(unc[i],3), round(ko_first[i],3)] for i in range(len(vols))]
    knockout_dollar=trig-K
    # payoff series for the brief: [stock, intrinsic kept at knockout, live value if never called]
    payoff=[[round(s,1), round(max(s-K,0.0),2), round(bs_call_s(max(s,0.01),K,T,central,r,q),2)] for s in np.arange(0,25.5,0.5)]

    premium=N*PX; vega_usd=N*vega; hedge_sh=round(N*delta*shares_per); carry=round(hedge_sh*S0*q)
    return dict(
        inputs=dict(ticker=cfg.get("ticker"),warrant=cfg.get("warrant_ticker"),company=cfg.get("company"),
                    asof=cfg.get("asof"),spot=S0,ask=PX,strike=K,t=round(T,3),
                    expiry=cfg.get("expiry"),borrow=q,rate=r,listed=listed,realized=rv,
                    redemption_trigger=trig,make_whole_trigger=mw,trigger_days=tdays,notice_days=notice_days),
        vanilla_iv=round(van*100,1),
        koiv_first=round(iv_first*100,1), koiv_delay=round(iv_delay*100,1), koiv_central=round(central*100),
        knockout_dollar=knockout_dollar, fair_at_listed=round(fair_listed,2),
        delta=round(float(delta),3), vega=round(float(vega),4),
        edge_listed=round((listed-iv_first)*100,1), edge_listed_delay=round((listed-iv_delay)*100,1),
        edge_vs_realized=(round((long_hv-central)*100,1) if long_hv is not None else None),
        realized_benchmark=long_hv_key, breakeven_borrow_vanilla=round(be_van*100,1),
        verdict=verdict, curve=curve, payoff=payoff,
        sizing=dict(N=N,premium=round(premium),vega_usd=round(vega_usd),hedge_sh=hedge_sh,carry=carry),
    )

def fmt(R):
    i=R["inputs"]; L=[]
    L.append("=== %s / %s  warrant vol-arb (KNOCKOUT-AWARE)  (%s) ==="%(i.get("ticker"),i.get("warrant"),i.get("asof")))
    L.append("spot %.2f  warrant %.2f  strike %.2f  %.2fy (exp %s)  borrow %.2f%%  redeem $%g"%(
        i["spot"],i["ask"],i["strike"],i["t"],i.get("expiry"),i["borrow"]*100,i["redemption_trigger"]))
    L.append("VANILLA IV (no knockout) = %.0f%%   |   KNOCKOUT-ADJUSTED IV = %.0f-%.0f%% (central ~%d%%)   ->   VERDICT: %s"%(
        R["vanilla_iv"],R["koiv_delay"],R["koiv_first"],R["koiv_central"],R["verdict"]))
    rb=R["realized_benchmark"]; er=R["edge_vs_realized"]
    L.append("  edge vs listed %.0f%%: ~0 to +%.0f pts  |  central vs %s: %s"%(
        i["listed"]*100,R["edge_listed"], rb, ("%+g pts"%er if er is not None else "n/a")))
    L.append("  knockout-fair value @ listed %.0f%% vol: $%.2f vs $%.2f ask  |  vanilla break-even borrow %.1f%% (ref)"%(
        i["listed"]*100,R["fair_at_listed"],i["ask"],R["breakeven_borrow_vanilla"]))
    s=R["sizing"]
    L.append("  knockout-model greeks: delta %.2f  vega $%.4f/pt   |   per %s wt: premium $%s | hedge short %s sh | carry $%s/yr"%(
        R["delta"],R["vega"],format(s["N"],","),format(s["premium"],","),format(s["hedge_sh"],","),format(s["carry"],",")))
    if i.get("make_whole_trigger"):
        L.append("  NOTE: $%g make-whole redemption present -- ~value-preserving (hands holders ~BS-fair cashless), so the $%g cash redemption is the binding knockout modeled here."%(i["make_whole_trigger"],i["redemption_trigger"]))
    return "\n".join(L)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("inputs"); ap.add_argument("--paths",type=int,default=14000)
    ap.add_argument("--borrow",type=float,default=None); ap.add_argument("--out",default=None)
    a=ap.parse_args()
    cfg=json.load(open(a.inputs))
    R=run(cfg,paths=a.paths,borrow_override=a.borrow)
    print(fmt(R))
    out=a.out or a.inputs.rsplit(".",1)[0]+".knockout.json"
    json.dump(R,open(out,"w"),indent=2); print("\nwrote",out)
