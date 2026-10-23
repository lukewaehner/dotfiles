#!/usr/bin/env python3
"""
build_brief.py - render a 3-page Letter-landscape desk brief (PDF) from warrant_knockout_mc.py's
<inputs>.knockout.json. Pure reportlab.

  python3 build_brief.py inputs.knockout.json --out TICKER_brief.pdf

Page 1: verdict, KPI tiles, model pipeline, inputs/outputs (knockout-adjusted).
Page 2: A implied-vol ladder, B warrant value vs vol (with vs without the knockout), C payoff truncation.
Page 3: trade, execution, risks (redemption-led), verified terms + sources in the footer.

The brief is deliberately plain-English and citation-free in the body; keep options theory out of it.
"""
import json, math, argparse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

INK=HexColor('#14181f');MUT=HexColor('#5b6573');ACC=HexColor('#0b5cab');GOOD=HexColor('#157a4a')
GOODBG=HexColor('#e8f5ee');BAD=HexColor('#b3261e');BADBG=HexColor('#fdecea');AMB=HexColor('#b06a00')
AMBBG=HexColor('#fff6e6');LINE=HexColor('#dde3ea');CHIP=HexColor('#eef3f8');GREY=HexColor('#9aa6b4')
W,H=792,612;M=36;CW=W-2*M

def build(R,out,BC=None):
    i=R["inputs"];s=R["sizing"]
    NP=4 if BC else 3
    tk=i.get("ticker","?");wt=i.get("warrant","?");V=R["verdict"]
    vcol={"CHEAP":GOOD,"RICH":BAD}.get(V,AMB)
    vbg ={"CHEAP":GOODBG,"RICH":BADBG}.get(V,AMBBG)
    vborder={"CHEAP":HexColor('#bfe3cf'),"RICH":HexColor('#f3c5c0')}.get(V,HexColor('#eedcba'))
    lead={"CHEAP":"BUY","RICH":"PASS"}.get(V,"NEUTRAL")
    band="~%d-%d%%"%(R["koiv_delay"],R["koiv_first"])
    rvd=i.get("realized",{}); _rvv=[v for v in rvd.values() if isinstance(v,(int,float))]
    rv_lo=round(100*min(_rvv)) if _rvv else 0; rv_hi=round(100*max(_rvv)) if _rvv else 0
    rvrange="%d-%d%%"%(rv_lo,rv_hi); rbk=R.get("realized_benchmark") or "realized"
    long_hv=round(100*rvd[rbk]) if rbk in rvd else rv_hi
    head={"CHEAP":"Long warrant vol, delta-hedged. After the $%g redemption and the verified %.2fy maturity, the warrant's knockout-adjusted vol %s is below listed (%d%%) and realized - a clean vol edge."%(i["redemption_trigger"],i["t"],band,i["listed"]*100),
          "RICH":"No edge. Once the $%g redemption is priced, knockout-adjusted vol %s is at/above the %d%% listed - pass."%(i["redemption_trigger"],band,i["listed"]*100),
          "FAIR":"Once the $%g knockout and the verified %.2fy maturity are priced, the redemption-adjusted vol %s sits just under the %s realized (~%d%%) and far below short-dated listed (%d%%). The $%g knockout is a soft call worth only a few vol points, so the bigger reason the headline gap to listed isn't real edge is the maturity / term-structure mismatch, not the redemption."%(i["redemption_trigger"],i["t"],band,rbk,long_hv,i["listed"]*100,i["redemption_trigger"])}[V]
    c=canvas.Canvas(out,pagesize=(W,H))
    def T(x,y,t,fn="Helvetica",sz=10,col=INK):c.setFont(fn,sz);c.setFillColor(col);c.drawString(x,y,t)
    def TR(x,y,t,fn="Helvetica",sz=10,col=INK):c.setFont(fn,sz);c.setFillColor(col);c.drawRightString(x,y,t)
    def TC(x,y,t,fn="Helvetica",sz=10,col=INK):c.setFont(fn,sz);c.setFillColor(col);c.drawCentredString(x,y,t)
    def sechead(y,t):T(M,y,t,"Helvetica-Bold",10,ACC);c.setStrokeColor(LINE);c.setLineWidth(1);c.line(M,y-5,W-M,y-5)
    def wrap(x,y,width,segs,size=9.5,leading=12.5):
        sp=c.stringWidth(' ','Helvetica',size);cx=x;cy=y;first=True
        for seg in segs:
            text=seg[0];fn=seg[1];col=seg[2] if len(seg)>2 else INK
            for word in text.split(' '):
                if word=='':continue
                ww=c.stringWidth(word,fn,size)
                if cx+(0 if first else sp)+ww>x+width:cy-=leading;cx=x;first=True
                if not first:cx+=sp
                c.setFont(fn,size);c.setFillColor(col);c.drawString(cx,cy,word);cx+=ww;first=False
        return cy
    def footer(pg):
        c.setStrokeColor(LINE);c.line(M,40,W-M,40)
        T(M,31,"Model: Monte Carlo (daily GBM) at the actual borrow imposing the $%g knockout (%d-of-%d-day trigger + %d-day notice - a soft call: the holder exits or exercises in the ~24-trading-day window and keeps intrinsic, not a $0.01 stub); vanilla cross-checked vs Black-Scholes."%(i["redemption_trigger"],i["trigger_days"][0],i["trigger_days"][1],i["notice_days"]),"Helvetica",7,MUT)
        T(M,21,"Sources: warrant agreement on SEC EDGAR (verified strike / redemption / 5y-post-BC maturity); Bloomberg Terminal DES / HVT / OMON.","Helvetica",7,MUT)
        T(M,11,"Illustrative - verify the live warrant market and loan rate at execution. Internal, not investment advice.","Helvetica",7,MUT)
        TR(W-M,11,"%s / %s Warrant-Arb  -  %d/%d"%(tk,wt,pg,NP),"Helvetica",7,MUT)

    # ---------------- PAGE 1 ----------------
    y=H-36
    T(M,y,"%s / %s - Warrant Volatility Arbitrage"%(tk,wt),"Helvetica-Bold",19);y-=15
    T(M,y,"%s  -  as of %s  -  borrow %.2f%%  -  priced on verified terms (knockout-aware)"%(i.get("company",""),i.get("asof",""),i["borrow"]*100),"Helvetica",9,MUT);y-=24
    c.setFillColor(vbg);c.setStrokeColor(vborder);c.roundRect(M,y-44,CW,46,5,fill=1,stroke=1)
    c.setStrokeColor(vcol);c.setLineWidth(3);c.line(M+2,y-43,M+2,y+1);c.setLineWidth(1)
    wrap(M+16,y-14,CW-30,[(V+" - ","Helvetica-Bold",vcol),(head,"Helvetica",INK)],size=9.5,leading=12.5)
    y-=58
    kpis=[("SPOT","$%.2f"%i["spot"],INK),("%s ASK"%wt,"$%.2f"%i["ask"],INK),("BORROW","%.2f%%"%(i["borrow"]*100),INK),
          ("KO-ADJ IV",band,vcol),("LISTED ATM IV","%d%%"%(i["listed"]*100),INK),("EDGE VS LISTED","~0 to +%.0f pt"%R["edge_listed"],vcol)]
    nn=6;gap=11;tw=(CW-(nn-1)*gap)/nn;th=44
    for k,(l,v,col) in enumerate(kpis):
        x=M+k*(tw+gap);c.setFillColor(white);c.setStrokeColor(LINE);c.roundRect(x,y-th,tw,th,7,fill=1,stroke=1)
        T(x+10,y-15,l,"Helvetica",7,MUT);T(x+10,y-35,v,"Helvetica-Bold",16,col)
    y-=th+14
    sechead(y,"MODEL");y-=14
    boxes=[("Spot %.2f + Borrow %.2f%%"%(i["spot"],i["borrow"]*100),"forward = S e^(r-q)t",CHIP,INK),
           ("Monte Carlo","daily GBM paths",CHIP,INK),
           ("$%g knockout"%i["redemption_trigger"],"soft call, keep intrinsic",CHIP,INK),
           ("Solve vol @ $%.2f"%i["ask"],"ko-adj ~%d%% vs listed %d%%"%(R["koiv_central"],i["listed"]*100),CHIP,INK),
           (V,"",vbg,vcol)]
    bn=5;bgap=24;bw=(CW-(bn-1)*bgap)/bn;bh=46;by=y-bh
    for k,(t1,t2,bg,tc) in enumerate(boxes):
        x=M+k*(bw+bgap);c.setFillColor(bg);c.setStrokeColor(LINE if bg==CHIP else vborder);c.roundRect(x,by,bw,bh,6,fill=1,stroke=1)
        if t2:TC(x+bw/2,by+26,t1,"Helvetica",9,tc);TC(x+bw/2,by+12,t2,"Helvetica",7.3,MUT)
        else:TC(x+bw/2,by+19,t1,"Helvetica-Bold",11,tc)
        if k<bn-1:
            ax=x+bw+3;ay=by+bh/2;c.setStrokeColor(GREY);c.setFillColor(GREY);c.setLineWidth(1.5);c.line(ax,ay,ax+bgap-7,ay)
            p=c.beginPath();p.moveTo(ax+bgap-7,ay);p.lineTo(ax+bgap-13,ay+4);p.lineTo(ax+bgap-13,ay-4);p.close();c.drawPath(p,fill=1,stroke=0);c.setLineWidth(1)
    y=by-22
    colw=(CW-20)/2;lx=M;rx=M+colw+20
    T(lx,y,"INPUTS","Helvetica-Bold",10,ACC);T(rx,y,"OUTPUTS","Helvetica-Bold",10,ACC)
    c.setStrokeColor(LINE);c.line(lx,y-5,lx+colw,y-5);c.line(rx,y-5,rx+colw,y-5)
    rv=i.get("realized",{});rvtxt=" / ".join("%d"%round(v*100) for v in rv.values()) if rv else "-"
    mwtxt="$%g + $%g make-whole"%(i["redemption_trigger"],i["make_whole_trigger"]) if i.get("make_whole_trigger") else "$%g cash, no $10"%i["redemption_trigger"]
    inp=[("Realized vol "+" / ".join(rv.keys()),rvtxt),
         ("Listed ATM implied vol (OMON)","%d%%"%(i["listed"]*100)),
         ("Cost-to-borrow (stock-loan)","%.2f%%"%(i["borrow"]*100)),
         ("Strike / verified life","$%.2f / %.2fy (exp %s)"%(i["strike"],i["t"],i.get("expiry","-"))),
         ("Redemption (from EDGAR)",mwtxt),
         ("Risk-free rate","%.1f%%"%(i["rate"]*100))]
    er=R.get("edge_vs_realized")
    outp=[("Vanilla IV (no knockout)","%.0f%%"%R["vanilla_iv"]),
          ("Knockout-adjusted IV (central)","%d-%d%% (~%d%%)"%(R["koiv_delay"],R["koiv_first"],R["koiv_central"])),
          ("Edge vs listed / %s"%(R.get("realized_benchmark") or "realized"),"~+%.0f / %s pt"%(R["edge_listed"], ("%+g"%er if er is not None else "-"))),
          ("Knockout-fair value @ listed vol","$%.2f vs $%.2f ask"%(R["fair_at_listed"],i["ask"])),
          ("Hedge delta / vega (knockout model)","%.2f / $%.3f per pt"%(R["delta"],R["vega"])),
          ("Per %s wt: premium / hedge"%format(s["N"],","),"$%s / short %s sh"%(format(s["premium"],","),format(s["hedge_sh"],",")))]
    ry=y-18;rh=19
    for k in range(6):
        yy=ry-k*rh
        T(lx+2,yy,inp[k][0],"Helvetica",9.3,INK);TR(lx+colw-2,yy,inp[k][1],"Helvetica",9.3,INK)
        T(rx+2,yy,outp[k][0],"Helvetica",9.3,INK);TR(rx+colw-2,yy,outp[k][1],"Helvetica-Bold" if k==1 else "Helvetica",9.3,vcol if k==1 else INK)
        c.setStrokeColor(LINE);c.line(lx,yy-6,lx+colw,yy-6);c.line(rx,yy-6,rx+colw,yy-6)
    footer(1);c.showPage()

    # ---------------- PAGE 2 ----------------
    y=H-36
    sechead(y,"VISUALIZATIONS - A . Implied-vol ladder: where the warrant's knockout-adjusted vol sits vs the market");y-=16
    ladder=[("Vanilla call, no knockout",R["vanilla_iv"],GREY),
            ("Knockout-adj - issuer delays",R["koiv_delay"],HexColor('#7fae7f')),
            ("Knockout-adj - central estimate",R["koiv_central"],GOOD),
            ("Knockout-adj - redeem at first $%g"%i["redemption_trigger"],R["koiv_first"],HexColor('#7fae7f')),
            ("Listed ATM options",i["listed"]*100,ACC)]
    for key in ("HV100","HV50","HV30","HV10"):
        if key in rv: ladder.append(("Realized "+key,rv[key]*100,GREY))
    caH=150;cax=M;cay=y-caH;barx0=cax+196;barAvail=CW-196-40
    maxv=max(125.0,max(v for _,v,_ in ladder)*1.05);topB=cay+caH-6;rh2=(caH-12)/len(ladder)
    for k,(lab,val,col) in enumerate(ladder):
        yy=topB-k*rh2-8
        TR(barx0-6,yy-3,"%s  %.0f%%"%(lab,val),"Helvetica-Bold" if "central" in lab else "Helvetica",8.2,INK)
        bw2=(val/maxv)*barAvail;c.setFillColor(col);c.rect(barx0,yy-7,bw2,12,fill=1,stroke=0)
        T(barx0+bw2+4,yy-3,"%.0f"%val,"Helvetica-Bold",8,col)
    xl=barx0+(i["listed"]*100/maxv)*barAvail
    c.setStrokeColor(ACC);c.setDash(3,2);c.line(xl,cay+4,xl,topB+2);c.setDash()
    y=cay-16
    cbW=(CW-24)/2;cbH=210;bx=M;bxy=y-cbH
    T(bx,y-2,"B . Warrant value vs vol - with vs without the knockout","Helvetica-Bold",9.5,INK)
    cur=R["curve"];xs=[p[0] for p in cur];unc=[p[1] for p in cur];ko=[p[2] for p in cur]
    xmin,xmax=xs[0],xs[-1];ymax=max(6.0,math.ceil(max(unc)))
    pL=bx+34;pR=bx+cbW-12;pB=bxy+30;pT=bxy+cbH-22
    ax=lambda v:pL+((v-xmin)/(xmax-xmin))*(pR-pL); ay=lambda v:pB+((v-0)/(ymax-0))*(pT-pB)
    c.setStrokeColor(GREY);c.setLineWidth(1);c.line(pL,pB,pR,pB);c.line(pL,pB,pL,pT)
    vt=0
    while vt<=ymax:
        yy=ay(vt)
        if vt>0:c.setStrokeColor(HexColor('#eef1f5'));c.line(pL,yy,pR,yy)
        TR(pL-4,yy-3,"$%d"%vt,"Helvetica",7.5,MUT);vt+=1
    for vv in range(int(xmin),int(xmax)+1,25):TC(ax(vv),pB-12,"%d%%"%vv,"Helvetica",7.5,MUT)
    TC((pL+pR)/2,pB-23,"assumed volatility","Helvetica",8,MUT)
    c.setStrokeColor(BAD);c.setDash(4,2);c.line(pL,ay(i["ask"]),pR,ay(i["ask"]));c.setDash();TR(pR-2,ay(i["ask"])+4,"market $%.2f"%i["ask"],"Helvetica",7.5,BAD)
    def plot(series,col):
        c.setStrokeColor(col);c.setLineWidth(2);p=c.beginPath();p.moveTo(ax(xs[0]),ay(min(series[0],ymax)))
        for j in range(1,len(xs)):p.lineTo(ax(xs[j]),ay(min(series[j],ymax)))
        c.drawPath(p,fill=0,stroke=1);c.setLineWidth(1)
    plot(unc,GREY);plot(ko,GOOD)
    T(ax(xs[1]),ay(min(unc[1],ymax))+4,"no-knockout","Helvetica-Bold",7.5,GREY)
    T(ax(xs[-4]),ay(ko[-4])-10,"knockout ($%g)"%i["redemption_trigger"],"Helvetica-Bold",7.5,GOOD)
    c.setFillColor(GREY);c.circle(ax(R["vanilla_iv"]),ay(i["ask"]),3.5,fill=1,stroke=0);TC(ax(R["vanilla_iv"]),ay(i["ask"])+8,"%.0f%%"%R["vanilla_iv"],"Helvetica-Bold",7.5,GREY)
    c.setFillColor(GOOD);c.circle(ax(R["koiv_first"]),ay(i["ask"]),3.5,fill=1,stroke=0);TC(ax(R["koiv_first"]),ay(i["ask"])+8,"%.0f%%"%R["koiv_first"],"Helvetica-Bold",7.5,GOOD)
    cx=M+cbW+24;cxy=y-cbH
    T(cx,y-2,"C . The $%g knockout - keep intrinsic, forgo remaining time value"%i["redemption_trigger"],"Helvetica-Bold",9.5,INK)
    T(cx,y-12,"Soft call: >= $%g for %d of %d days starts a ~24-trading-day window to exit or exercise (keep intrinsic), else $0.01."%(i["redemption_trigger"],i["trigger_days"][0],i["trigger_days"][1]),"Helvetica",6.6,MUT)
    po=R["payoff"];Sx=[p[0] for p in po];pintr=[p[1] for p in po];plive=[p[2] for p in po]
    qxmax=25;qymax=max(14.0,math.ceil(max(plive)+0.5))
    qL=cx+30;qR=cx+cbW-12;qB=cxy+30;qT=cxy+cbH-22
    qx=lambda v:qL+(v/qxmax)*(qR-qL); qy=lambda v:qB+(v/qymax)*(qT-qB)
    c.setStrokeColor(GREY);c.line(qL,qB,qR,qB);c.line(qL,qB,qL,qT)
    _ys=4 if qymax>14 else 2
    vv=0
    while vv<=qymax+0.001:
        yy=qy(vv)
        if vv>0:c.setStrokeColor(HexColor('#eef1f5'));c.line(qL,yy,qR,yy)
        TR(qL-4,yy-3,"$%d"%int(round(vv)),"Helvetica",7.5,MUT);vv+=_ys
    for vv in range(0,26,5):TC(qx(vv),qB-12,"$%d"%vv,"Helvetica",7.5,MUT)
    TC((qL+qR)/2,qB-23,"stock price","Helvetica",8,MUT)
    c.setStrokeColor(GREY);c.setLineWidth(2);p=c.beginPath();p.moveTo(qx(Sx[0]),qy(min(plive[0],qymax)))
    for j in range(1,len(Sx)):p.lineTo(qx(Sx[j]),qy(min(plive[j],qymax)))
    c.drawPath(p,fill=0,stroke=1)
    c.setStrokeColor(GOOD);c.setLineWidth(2);p=c.beginPath();p.moveTo(qx(Sx[0]),qy(min(pintr[0],qymax)))
    for j in range(1,len(Sx)):p.lineTo(qx(Sx[j]),qy(min(pintr[j],qymax)))
    c.drawPath(p,fill=0,stroke=1);c.setLineWidth(1)
    for xx,lab,cc in [(i["strike"],"strike $%g"%i["strike"],MUT),(i["redemption_trigger"],"knockout $%g"%i["redemption_trigger"],AMB),(i["spot"],"spot",ACC)]:
        c.setStrokeColor(cc);c.setDash(2,2);c.line(qx(xx),qB,qx(xx),qT);c.setDash();TC(qx(xx),qT+4,lab,"Helvetica",7,cc)
    T(qx(20.2),qy(min(plive[-1],qymax))+1,"if never called","Helvetica-Bold",6.8,GREY)
    T(qx(21.4),qy(min(max(Sx[-1]-i["strike"],0),qymax))-7,"intrinsic","Helvetica-Bold",6.8,GOOD)
    T(qx(21.4),qy(min(max(Sx[-1]-i["strike"],0),qymax))-15,"(kept)","Helvetica",6.4,GOOD)
    T(qx(7.5),qy(qymax*0.80),"gap above $%g ="%i["redemption_trigger"],"Helvetica-Bold",6.8,BAD)
    T(qx(7.5),qy(qymax*0.80)-8,"forgone time value","Helvetica",6.6,BAD)
    footer(2);c.showPage()

    # ---------------- OPTIONAL PAGE 3: IMPLIED-BORROW TERM STRUCTURE ----------------
    if BC:
        AMBER=HexColor('#D97706'); STEEL=HexColor('#1D4E89')
        AMBER_L=HexColor('#e2b277'); STEEL_L=HexColor('#9db8d8'); NAVY=HexColor('#0A1628')
        y=H-36
        sechead(y,"IMPLIED-BORROW TERM STRUCTURE - listed-option put-call parity (mid)");y-=13
        T(M,y,"%s  -  as of %s  -  spot $%.2f  -  q from C-P => forward => borrow, ATM bracket, median over trailing %d / %d trading days"%(
            BC.get("ticker") or tk, BC.get("asof",""), BC.get("spot") or 0, BC.get("short_win",10), BC.get("long_win",30)),"Helvetica",8.5,MUT);y-=12
        gx0=M+34; gx1=M+0.70*CW; gy0=118; gy1=y-12
        ymax=BC.get("y_max",100) or 100; xmax=BC.get("x_max_months",60) or 60
        axb=lambda m: gx0+(m/xmax)*(gx1-gx0)
        ayb=lambda q: gy0+(min(q,ymax)/ymax)*(gy1-gy0)
        # gridlines / axes
        yv=0
        while yv<=ymax+0.01:
            yy=ayb(yv)
            if   yv==0:  c.setStrokeColor(NAVY);c.setLineWidth(1.4)
            elif yv==10: c.setStrokeColor(HexColor('#6b7280'));c.setLineWidth(1.2)
            else:        c.setStrokeColor(HexColor('#eef1f5'));c.setLineWidth(0.6)
            c.line(gx0,yy,gx1,yy)
            if yv%10==0: TR(gx0-4,yy-3,"%d%%"%yv,"Helvetica",7.5,MUT)
            yv+=5
        c.setLineWidth(1)
        mv=0
        while mv<=xmax+0.01:
            xx=axb(mv)
            if mv>0: c.setStrokeColor(HexColor('#eef1f5'));c.setLineWidth(0.5);c.line(xx,gy0,xx,gy1)
            TC(xx,gy0-12,"%dm"%mv,"Helvetica",7.5,MUT); mv+=6
        c.setStrokeColor(GREY);c.setLineWidth(1);c.line(gx0,gy0,gx1,gy0);c.line(gx0,gy0,gx0,gy1)
        TC((gx0+gx1)/2,gy0-24,"Months to expiry","Helvetica",8,MUT)
        c.saveState();c.translate(M-3,(gy0+gy1)/2);c.rotate(90);TC(0,0,"Implied borrow q (%)","Helvetica",8,MUT);c.restoreState()
        def hdash(qv,col,lbl):
            if qv is None: return
            yy=ayb(qv);c.setStrokeColor(col);c.setDash(2,3);c.setLineWidth(1);c.line(axb(0.3),yy,gx1,yy);c.setDash()
            TR(gx1-2,yy+3,lbl,"Helvetica",6.5,col)
        hdash(BC.get("avg_long"),AMBER_L,"30d avg %.0f%%"%(BC.get("avg_long") or 0))
        hdash(BC.get("avg_short"),STEEL_L,"10d avg %.0f%%"%(BC.get("avg_short") or 0))
        def poly(curve,col,dash,wdt,mr):
            pts=[(axb(p["months"]),ayb(p["q"])) for p in (curve or []) if p["months"]<=xmax]
            if len(pts)>=2:
                c.setStrokeColor(col);c.setLineWidth(wdt)
                if dash:c.setDash(*dash)
                pth=c.beginPath();pth.moveTo(*pts[0])
                for xy in pts[1:]: pth.lineTo(*xy)
                c.drawPath(pth,fill=0,stroke=1);c.setDash()
            for (xx,yy) in pts:
                c.setFillColor(col);c.circle(xx,yy,mr,fill=1,stroke=0)
                c.setStrokeColor(white);c.setLineWidth(0.8);c.circle(xx,yy,mr,fill=0,stroke=1)
        poly(BC.get("curve_long"), AMBER,None, 2.0,3.1)
        poly(BC.get("curve_short"),STEEL,(5,3),1.6,2.4)
        def star(cx,cy,rO,col):
            pth=c.beginPath()
            for k in range(10):
                ang=-math.pi/2+k*math.pi/5; rr=rO if k%2==0 else rO*0.42
                pt=(cx+rr*math.cos(ang),cy+rr*math.sin(ang))
                (pth.moveTo if k==0 else pth.lineTo)(*pt)
            pth.close();c.setFillColor(col);c.drawPath(pth,fill=1,stroke=0)
        for w in (BC.get("warrants") or []):
            if w["months"]<=xmax:
                xx=axb(w["months"]);yy=ayb(w["q"]);star(xx,yy,5.6,AMBER)
                TC(xx,yy+9,"%s %.0f%%"%(w["label"],w["q"]),"Helvetica-Bold",6.4,HexColor('#8a5a00'))
        # ---- side panel ----
        px=gx1+20; pw=W-M-px; py=gy1
        T(px,py,"READ","Helvetica-Bold",9,ACC);py-=6;c.setStrokeColor(LINE);c.line(px,py,px+pw,py);py-=15
        def leg(yy,col,dash,is_star,txt):
            if is_star: star(px+6,yy+2,5,col)
            else:
                c.setStrokeColor(col);c.setLineWidth(2.2)
                if dash:c.setDash(*dash)
                c.line(px,yy+2,px+13,yy+2);c.setDash()
                c.setFillColor(col);c.circle(px+6.5,yy+2,2.3,fill=1,stroke=0)
            T(px+18,yy,txt,"Helvetica",8,INK)
        leg(py,AMBER,None,False,"30d window (median q by expiry)");py-=15
        leg(py,STEEL,(4,2),False,"10d window (fresher / noisier)");py-=15
        if BC.get("warrants"): leg(py,AMBER,None,True,"warrant-implied borrow");py-=4
        py-=12;T(px,py,"OPTION vs WARRANT BORROW","Helvetica-Bold",7.5,MUT);py-=11
        cl=BC.get("curve_long") or []
        for w in (BC.get("warrants") or []):
            near=min(cl,key=lambda p:abs(p["months"]-w["months"])) if cl else None
            if near:
                rel="RICHER" if w["q"]>near["q"] else "cheaper"
                py=wrap(px,py,pw,[("%s: "%w["label"],"Helvetica-Bold"),
                    ("implies %.1f%% borrow vs ~%.1f%% on the option curve near %.0fm - a %s borrow than options price."%(w["q"],near["q"],w["months"],rel),"Helvetica")],size=7.3,leading=9.3)-6
        py-=3;c.setStrokeColor(LINE);c.line(px,py,px+pw,py);py-=12
        wrap(px,py,pw,[("How to read - ","Helvetica-Bold"),
            ("a downward-sloping curve = a near-dated borrow squeeze that the market expects to ease; 10d under 30d = borrow softening lately. A warrant star well above the option curve says the warrant is pricing a richer borrow than the options - revisit the borrow input before trusting the verdict.","Helvetica")],size=7.3,leading=9.3)
        footer(3);c.showPage()

    # ---------------- LAST PAGE: TRADE / EXECUTION / RISKS ----------------
    y=H-36;sechead(y,"TRADE");y-=14
    c.setFillColor(vbg);c.setStrokeColor(vborder);c.roundRect(M,y-66,CW,66,6,fill=1,stroke=1)
    tl={"CHEAP":"LONG warrant . SHORT stock . delta-neutral","RICH":"PASS - no vol edge once the redemption is priced","FAIR":"FAIR / no clean vol edge - pass, or a small clip only on a specific view"}[V]
    T(M+14,y-19,tl,"Helvetica-Bold",12,INK)
    TR(W-M-14,y-19,"Verdict: %s"%V,"Helvetica-Bold",10,vcol)
    wrap(M+14,y-38,CW-28,[("At $%.2f the warrant prices ~%d%% vol after the knockout, vs ~%s realized (%s ~%d%%) and %d%% listed. Knockout-fair @ listed vol is ~$%.2f. If traded: long warrant / short ~%.2f sh per warrant, delta-neutral."%(i["ask"],R["koiv_central"],rvrange,rbk,long_hv,i["listed"]*100,R["fair_at_listed"],R["delta"]),"Helvetica")],size=9.3,leading=12)
    y-=78
    sechead(y,"EXECUTION & MONITORING");y-=18
    exe=[("When it works - ","you win only if the stock realizes more than ~%d%% vol, or if the company chooses NOT to redeem at $%g (which would re-cheapen the warrant). Absent one of those, there is little vol edge to harvest."%(R["koiv_central"],i["redemption_trigger"])),
         ("Hedge - ","short about %.2f shares per warrant (knockout-model delta, lower than the naive Black-Scholes delta) and re-balance on ~5-7%% stock moves."%R["delta"]),
         ("Size - ","measure by vol: ~$%s of P&L per vol point with $%s premium at risk per %s warrants; thin edge does not justify a large clip."%(format(s["vega_usd"],","),format(s["premium"],","),format(s["N"],","))),
         ("Monitor - ","the borrow weekly (still %.2f%%) and the stock vs the $%g trigger; the redemption is the binding risk, not the borrow."%(i["borrow"]*100,i["redemption_trigger"]))]
    for lab,body in exe:
        c.setFillColor(ACC);c.circle(M+3,y+3,2,fill=1,stroke=0);y=wrap(M+13,y,CW-13,[(lab,"Helvetica-Bold"),(body,"Helvetica")])-13
    y-=4;sechead(y,"RISKS");y-=18
    risks=[("The $%g knockout is a soft call, not a hard price ceiling - "%i["redemption_trigger"],"once the stock holds >= $%g for %d of %d trading days the issuer can redeem for $0.01 after a ~%d-day notice (about a month, ~24 trading days). In that window you SELL the warrant or EXERCISE (cash/cashless) and KEEP the intrinsic - only doing nothing leaves you $0.01. So the redemption forgoes the warrant's remaining TIME VALUE (a few vol points here), not its intrinsic upside; treat it as your hard exit rule, not a $%.2f ceiling."%(i["redemption_trigger"],i["trigger_days"][0],i["trigger_days"][1],i["notice_days"],R["knockout_dollar"])),
           ("Verify the terms - ","strike, redemption and the true 5y-post-BC maturity come from the warrant agreement on EDGAR, not Bloomberg's indicative DES. A wrong maturity feeds straight into the vol solve."),
           ("You are NOT buying cheap vol - ","at ~%d%% the warrant is roughly at the %s realized (~%d%%) and only looks cheap against short-dated listed (%d%%) you cannot sell out to its maturity; a quiet stock loses, and the knockout ends your vol harvest."%(R["koiv_central"],rbk,long_hv,i["listed"]*100)),
           ("Thin instruments - ","the warrant and the listed options are illiquid; build slowly, hedge in the stock, size to what you can exit.")]
    for lab,body in risks:
        c.setFillColor(BAD);c.circle(M+3,y+3,2,fill=1,stroke=0);y=wrap(M+13,y,CW-13,[(lab,"Helvetica-Bold"),(body,"Helvetica")])-13
    footer(NP);c.showPage();c.save()

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("results");ap.add_argument("--out",default=None);ap.add_argument("--borrow-curve",default=None)
    a=ap.parse_args();R=json.load(open(a.results))
    BC=json.load(open(a.borrow_curve)) if a.borrow_curve else None
    out=a.out or a.results.rsplit(".",1)[0]+"_brief.pdf"
    build(R,out,BC);print("wrote",out)
