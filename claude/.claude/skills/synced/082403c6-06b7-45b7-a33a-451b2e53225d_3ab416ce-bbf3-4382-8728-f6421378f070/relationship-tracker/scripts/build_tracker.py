#!/usr/bin/env python3
"""Inject scanned relationship rows into the tracker template.

Usage:  python build_tracker.py rows.json out.html [--template path] [--asof YYYY-MM-DD]

rows.json may be either a bare list of row objects, or {"rows": [...], "asOf": "..."}.
Each row: see references/row-schema.md. Only `display` is strictly required.
"""
import json, sys, os, argparse, datetime, re

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('rows'); ap.add_argument('out')
    ap.add_argument('--template', default=os.path.join(os.path.dirname(__file__),'..','assets','tracker_template.html'))
    ap.add_argument('--asof', default=datetime.date.today().isoformat())
    a=ap.parse_args()
    # Always use UTF-8 for all file I/O — Windows default (cp1252) silently corrupts
    # non-ASCII characters (·, →, etc.) into mojibake sequences like Â·, â†'.
    data=json.load(open(a.rows, encoding='utf-8'))
    rows = data['rows'] if isinstance(data,dict) and 'rows' in data else data
    asof = (data.get('asOf') if isinstance(data,dict) else None) or a.asof
    norm=[]
    for i,r in enumerate(rows):
        disp=(r.get('display') or r.get('ticker') or 'UNTAGGED')
        rid=r.get('id') or re.sub(r'[^A-Za-z0-9]+','_', str(r.get('ticker') or disp)).strip('_') or ('row_%d'%i)
        norm.append({
            'id':rid,
            'display':disp,
            'ticker':r.get('ticker',''),
            'matchKey':r.get('matchKey') or r.get('ticker') or '',
            'type':r.get('type','Sponsor'),
            'contacts':r.get('contacts',''),
            'lastContacted':r.get('lastContacted'),
            'daysSince':r.get('daysSince'),
            'statusOverride':r.get('statusOverride'),
            'nextStep':r.get('nextStep',''),
            'followUp':r.get('followUp'),
            'notes':r.get('notes',''),
        })
    seed={'asOf':asof,'count':len(norm),'rows':norm}
    tmpl=open(a.template, encoding='utf-8').read()
    out=tmpl.replace('__SEED_JSON__', json.dumps(seed, separators=(',',':')))
    open(a.out,'w', encoding='utf-8').write(out)
    print('wrote %s with %d rows (asOf %s)'%(a.out,len(norm),asof))

if __name__=='__main__':
    main()
