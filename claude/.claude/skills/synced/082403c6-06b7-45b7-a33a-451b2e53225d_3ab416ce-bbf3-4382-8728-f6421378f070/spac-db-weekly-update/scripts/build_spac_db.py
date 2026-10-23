#!/usr/bin/env python3
"""Rebuild the SPAC Research SQLite database from the two native site exports.

Usage:
  python3 build_spac_db.py --native <all_spacs.csv> --sponsors <sponsors.json> --out <db_path>

- <all_spacs.csv>   = the "All SPACs" CSV export  (spacresearch.com  /symbol?export-all=csv)
- <sponsors.json>   = harvested Sponsors grid     (see scripts/harvest_sponsors.js)
- <db_path>         = destination .sqlite file    (a timestamped backup is kept)

The rebuild is atomic: it builds to a temp file, runs integrity checks, and only then
replaces <db_path>. If checks fail, the existing database is left untouched.
"""
import json, sqlite3, csv, re, os, sys, argparse, datetime, shutil, tempfile

def snake(s):
    s=re.sub(r"\(.*?\)","",str(s)).split(",")[0]
    s=re.sub(r"([a-z0-9])([A-Z])",r"\1_\2",s).lower()
    return re.sub(r"[^a-z0-9]+","_",s).strip("_") or "col"

def to_num(v):
    if v is None: return None
    s=str(v).strip()
    if s in ("","-","N/A","n/a","NA","Not specified","--"): return None
    try: return float(s.replace("$","").replace(",","").replace("%","").replace("x","").strip())
    except: return None

def load_table(cur, table, header, rows):
    cols=[]; seen={}
    for h in header:
        c=snake(h)
        if c in seen: seen[c]+=1; c=f"{c}_{seen[c]}"
        else: seen[c]=0
        cols.append(c)
    is_num=[]
    for j in range(len(cols)):
        vals=[r[j] for r in rows if j<len(r) and str(r[j]).strip() not in ("","-","N/A","Not specified")]
        is_num.append(bool(vals) and sum(1 for v in vals if to_num(v) is not None)/len(vals) >= 0.9)
    cur.execute('CREATE TABLE "%s" (%s)'%(table,",".join('"%s" %s'%(c,"REAL" if is_num[j] else "TEXT") for j,c in enumerate(cols))))
    out=[]
    for r in rows:
        out.append([ (to_num(r[j]) if is_num[j] else (None if (j>=len(r) or r[j] in ("",None)) else str(r[j]))) for j in range(len(cols)) ])
    cur.executemany('INSERT INTO "%s" VALUES (%s)'%(table,",".join("?"*len(cols))), out)
    for h,c in zip(header,cols):
        cur.execute("INSERT INTO column_labels VALUES (?,?,?)",(table,c,h))
    return cols

def build(native, sponsors_json, tmp_db):
    if os.path.exists(tmp_db): os.remove(tmp_db)
    con=sqlite3.connect(tmp_db); cur=con.cursor()
    cur.execute("CREATE TABLE _meta (key TEXT, value TEXT)")
    cur.execute("CREATE TABLE column_labels (table_name TEXT, column_name TEXT, friendly_label TEXT)")

    with open(native,encoding="utf-8",errors="ignore") as f:
        rd=csv.reader(f); header=next(rd); rows=[r for r in rd if any(x.strip() for x in r)]
    load_table(cur,"spacs",header,rows)
    cur.execute("INSERT INTO _meta VALUES ('rows_spacs',?)",(str(len(rows)),))

    sp=json.load(open(sponsors_json))
    hdr={c["field"]:c["header"] for c in sp["colDefs"]}
    load_table(cur,"sponsors",[hdr.get(f,f) for f in sp["fields"]],sp["rows"])
    cur.execute("INSERT INTO _meta VALUES ('rows_sponsors',?)",(str(sp["count"]),))

    for st,vn in {"pre-ipo":"v_pre_ipo","pre-deal":"v_pre_deal","live-deal":"v_live_deal",
                  "closed":"v_closed","liquidated":"v_liquidated","stalled":"v_stalled"}.items():
        cur.execute("CREATE VIEW %s AS SELECT * FROM spacs WHERE status='%s'"%(vn,st))
    cur.execute("""CREATE VIEW v_franchise AS
      SELECT sp.family, sp.officers, sp.type AS sponsor_type, sp.redemptions,
             s.spac, s.spac_ticker AS ticker, s.status, s.newco AS target,
             s.common AS common_price, s.premium, s.trust_cash_remaining, s.trust_value,
             s.deadline, s.banker, s.counsel
      FROM sponsors sp LEFT JOIN spacs s
        ON UPPER(TRIM(s.spac_ticker))=UPPER(TRIM(sp.ticker))""")

    cur.execute("INSERT INTO _meta VALUES ('source','spacresearch.com native exports (All SPACs CSV + Sponsors)')")
    cur.execute("INSERT INTO _meta VALUES ('extracted_at',?)",(datetime.date.today().isoformat(),))
    cur.execute("INSERT INTO _meta VALUES ('built_at',?)",(datetime.datetime.utcnow().isoformat()+"Z",))
    con.commit(); cur.execute("VACUUM"); con.commit(); con.close()

def verify(db):
    con=sqlite3.connect(db); cur=con.cursor()
    ns=cur.execute("SELECT COUNT(*) FROM spacs").fetchone()[0]
    nsp=cur.execute("SELECT COUNT(*) FROM sponsors").fetchone()[0]
    statuses=[r[0] for r in cur.execute("SELECT DISTINCT status FROM spacs")]
    dt=cur.execute("SELECT COUNT(DISTINCT spac_ticker) FROM spacs").fetchone()[0]
    con.close()
    problems=[]
    if ns < 500: problems.append("spacs row count suspiciously low (%d)"%ns)
    if nsp < 300: problems.append("sponsors row count suspiciously low (%d)"%nsp)
    if "live-deal" not in statuses: problems.append("no live-deal rows")
    return {"spacs":ns,"sponsors":nsp,"distinct_tickers":dt,"statuses":statuses,"problems":problems}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--native",required=True)
    ap.add_argument("--sponsors",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    for p in (a.native,a.sponsors):
        if not os.path.exists(p): sys.exit("MISSING INPUT: "+p)
    tmp=tempfile.mktemp(suffix=".sqlite")
    build(a.native,a.sponsors,tmp)
    rep=verify(tmp)
    print("VERIFY:",json.dumps(rep))
    if rep["problems"]:
        os.remove(tmp); sys.exit("ABORT - integrity checks failed; existing DB left untouched.")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)),exist_ok=True)
    if os.path.exists(a.out):
        bak=a.out+"."+datetime.date.today().isoformat()+".bak"
        shutil.copy(a.out,bak); print("backup:",bak)
    shutil.move(tmp,a.out)
    print("OK - database rebuilt at:",a.out)
    print("   spacs=%d  sponsors=%d  tickers=%d"%(rep["spacs"],rep["sponsors"],rep["distinct_tickers"]))

if __name__=="__main__":
    main()
