#!/usr/bin/env python3
"""
render_catchup.py - deterministic HTML builder for the "SEC Filing Catch Up" digest.

Why a script and not free-form model output: the table layout, the email-safe
inline CSS, and the send-time math must be identical every run. The model's job
is to produce GOOD snapshots; this script renders them the same way every time
so the email never drifts.

Input  : a JSON file (argv[1]) - schema below.
Output : writes a standalone .html file (argv[2]) AND prints the same HTML to
         stdout. The printed HTML is what you paste verbatim into the send-email
         `body` (content_type="HTML"). One canonical HTML powers both the saved
         file and the email body, so they can never disagree.
Config : optional argv[3] JSON {"subject_prefix": "[TEST] "}.

Input JSON schema:
{
  "date_label": "Monday, June 29, 2026",
  "generated_local": "2026-06-29 18:25 ET",
  "scanned": 41, "in_universe": 6, "dropped": 35,
  "rows": [
    {"ticker":"CCIX","company":"Churchill Capital Corp IX","stage":"predeal",
     "form":"8-K","filed":"2026-06-29",
     "snapshot":"Item 5.07 - extension vote passed; new deadline 12/31/26, $0.03/sh monthly deposit.",
     "url":"https://www.sec.gov/Archives/edgar/data/..."}
  ]
}
"""

import sys, json, html



# Aidas's display order: 8-K, then proxies, then S-4/F-4 & S-1/F-1 (+ offering/
# effectiveness), then 13D/G, then 425, then periodic (10-Q/K), then everything else.
# Combo-aware: a row labelled "8-K / 425" ranks as 8-K (the most senior form wins).
FORM_LADDER = [
    (0, ["8-K"]),                                   # current reports (8-K, 8-K/A)
    (1, ["14A"]),                                   # proxies: DEF/PRE/DEFR/DEFM/DEFA 14A
    (2, ["S-4", "F-4", "S-1", "F-1"]),              # merger / IPO registration statements
    (3, ["424B", "EFFECT", "8-A12B", "CERT"]),      # offering / went-effective / listing
    (4, ["13D", "13G"]),                            # beneficial-ownership
    (5, ["425"]),                                   # merger communications
    (6, ["10-Q", "10-K", "20-F", "6-K", "NT 10"]),  # periodic reports
]

def _form_rank(form):
    up = (form or "").upper()
    for rank, keys in FORM_LADDER:
        if any(k in up for k in keys):
            return rank
    return 7  # anything else sorts last

def _esc(s):
    return html.escape(str(s if s is not None else "")).strip()


def build_html(data, subject_prefix=""):
    rows = sorted(data.get("rows", []), key=lambda r: (
        _form_rank(r.get("form", "")),
        0 if r.get("stage") == "indeal" else 1,
        r.get("ticker", ""),
    ))

    date_label = _esc(data.get("date_label", ""))
    scanned = data.get("scanned", "?")
    in_universe = data.get("in_universe", len(rows))
    dropped = data.get("dropped", "?")
    gen = _esc(data.get("generated_local", ""))
    source = _esc(data.get("source", "EDGAR (direct)"))

    th = ('padding:7px 10px;text-align:left;font-size:11px;font-weight:600;'
          'text-transform:uppercase;letter-spacing:.04em;color:#5b6470;'
          'border-bottom:2px solid #d4d9e0;white-space:nowrap;')
    td = 'padding:8px 10px;font-size:13px;color:#1f2430;border-bottom:1px solid #edf0f4;vertical-align:top;'

    body_rows = []
    for r in rows:
        stage = r.get("stage", "")
        tag = ('<span style="display:inline-block;font-size:9px;font-weight:700;'
               'padding:1px 5px;border-radius:3px;margin-left:6px;vertical-align:middle;'
               + ('background:#fde8c8;color:#8a5a00;">IN-DEAL</span>' if stage == "indeal"
                  else 'background:#e3ecf7;color:#3a5b86;">PRE-DEAL</span>'))
        ticker = _esc(r.get("ticker"))
        url = (r.get("url") or "").strip()
        ticker_cell = (f'<a href="{_esc(url)}" style="color:#1a4d8f;text-decoration:none;font-weight:700;">{ticker}</a>'
                       if url else f'<span style="font-weight:700;">{ticker}</span>')
        body_rows.append(
            '<tr>'
            f'<td style="{td}white-space:nowrap;">{ticker_cell}{tag}</td>'
            f'<td style="{td}color:#5b6470;">{_esc(r.get("company"))}</td>'
            f'<td style="{td}white-space:nowrap;font-weight:600;">{_esc(r.get("form"))}</td>'
            f'<td style="{td}white-space:nowrap;color:#5b6470;">{_esc(r.get("filed"))}</td>'
            f'<td style="{td}">{_esc(r.get("snapshot"))}</td>'
            '</tr>'
        )

    if not body_rows:
        body_rows = [f'<tr><td style="{td}" colspan="5"><em>No SEC filings hit the '
                     'Meteora SPAC universe today.</em></td></tr>']

    table = (
        '<table role="presentation" style="border-collapse:collapse;width:100%;'
        'max-width:860px;font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;">'
        '<thead><tr>'
        f'<th style="{th}">Ticker</th><th style="{th}">Company</th>'
        f'<th style="{th}">Form</th><th style="{th}">Filed</th>'
        f'<th style="{th}">What happened</th>'
        '</tr></thead><tbody>' + "".join(body_rows) + '</tbody></table>'
    )

    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"></head>'
        '<body style="margin:0;padding:18px;background:#ffffff;'
        'font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#1f2430;">'
        f'<div style="font-size:18px;font-weight:700;margin-bottom:2px;">{subject_prefix}SEC Filing Catch Up</div>'
        f'<div style="font-size:13px;color:#5b6470;margin-bottom:14px;">{date_label}</div>'
        + table +
        '<div style="font-size:11px;color:#8a929d;margin-top:14px;line-height:1.5;">'
        f'{in_universe} filings across the Meteora SPAC universe &middot; source: {source}. '
        f'Snapshots pulled from the EDGAR filing text. Generated {gen}.</div>'
        '</body></html>'
    )


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: render_catchup.py <input.json> <output.html> [config.json]")
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    prefix = ""
    if len(sys.argv) > 3:
        with open(sys.argv[3], encoding="utf-8") as f:
            prefix = json.load(f).get("subject_prefix", "")
    out_html = build_html(data, subject_prefix=prefix)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(out_html)
    sys.stdout.write(out_html)


if __name__ == "__main__":
    main()
