#!/usr/bin/env python3
"""
parse_alert.py — deterministic helpers for the s1-filing-handler skill.

Two jobs, kept in one file so the skill only has to remember one path:

1) --window : compute the scan window for THIS run (morning vs afternoon), in
   America/New_York, with hard caps at 09:00 (morning) and 17:30 (afternoon).
2) --parse / --eml : classify a SPACInsider alert — filing type (S-1 vs S-1/A),
   SPAC name, EDGAR CIK + accession (decoding Outlook SafeLinks), and whether it
   is a genuine IPO S-1 or a deSPAC/business-combination registration (skip).

Everything prints JSON to stdout so the skill can read the fields back verbatim
instead of eyeballing an email.

Examples
--------
    python parse_alert.py --window
    python parse_alert.py --window --session morning
    python parse_alert.py --window --now 2026-06-30T19:05:00
    python parse_alert.py --parse --subject "Fw: [S-1] Foo Corp" --body-file body.txt
    python parse_alert.py --eml "Fw_ [S-1] Cartesian Growth Corporation III.eml"
"""
import argparse
import base64
import json
import re
import sys
from datetime import datetime, time, timedelta

try:
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover - fallback if tzdata missing
    ET = None

# ---- Filing window ---------------------------------------------------------

MORNING = (time(6, 0), time(9, 0))     # 06:00–09:00 ET
AFTERNOON = (time(9, 0), time(17, 30))  # 09:00–17:30 ET
# A run at/before this hour is treated as the morning run; after it, afternoon.
MORNING_CUTOFF_HOUR = 12


def _now_et(now_iso=None):
    if now_iso:
        dt = datetime.fromisoformat(now_iso)
        if dt.tzinfo is None and ET is not None:
            dt = dt.replace(tzinfo=ET)
        return dt
    if ET is not None:
        return datetime.now(ET)
    return datetime.now()


def session_window(now_iso=None, session=None):
    """Return the [start, end] scan window for this run.

    session may be forced to 'morning' or 'afternoon'; otherwise it is chosen by
    the clock (before noon ET -> morning, else afternoon). Ends are hard caps:
    the morning window never runs past 09:00 and nothing ever scans past 17:30.
    """
    now = _now_et(now_iso)
    if session not in ("morning", "afternoon"):
        session = "morning" if now.hour < MORNING_CUTOFF_HOUR else "afternoon"
    start_t, end_t = MORNING if session == "morning" else AFTERNOON
    day = now.date()
    start = datetime.combine(day, start_t, tzinfo=now.tzinfo)
    end = datetime.combine(day, end_t, tzinfo=now.tzinfo)
    return {
        "session": session,
        "date": day.isoformat(),
        "start_iso": start.isoformat(),
        "end_iso": end.isoformat(),
        # convenience: what to pass to search_emails(after=...) and the cutoff to
        # filter receivedDateTime against.
        "after": start.isoformat(),
        "cutoff": end.isoformat(),
        "now": now.isoformat(),
    }

# ---- Alert parsing ---------------------------------------------------------

_PREFIX_RE = re.compile(r"^(?:\s*(?:re|fw|fwd)\s*:\s*)+", re.IGNORECASE)


def classify_subject(subject):
    """S-1/A (checked first — it contains 'S-1' as a substring) vs S-1 vs None.

    Only the bracketed SPACInsider tags count, so '[S-1MEF]' or a stray 'S-1'
    inside a company name does not misfire.
    """
    s = subject or ""
    if re.search(r"\[\s*S-1/A\s*\]", s, re.IGNORECASE):
        return "S-1/A"
    if re.search(r"\[\s*S-1\s*\]", s, re.IGNORECASE):
        return "S-1"
    return None


def clean_spac_name(subject):
    """SPAC name = subject minus forward/reply prefixes and the [S-1]/[S-1/A] tag."""
    s = subject or ""
    prev = None
    while prev != s:  # strip possibly-stacked 'Fw: Re:' prefixes
        prev = s
        s = _PREFIX_RE.sub("", s).strip()
    s = re.sub(r"\[\s*S-1(?:/A)?\s*\]", "", s, flags=re.IGNORECASE).strip()
    return re.sub(r"\s{2,}", " ", s).strip(" -–:")


def _unwrap_safelinks(url):
    """Return the real target of an Outlook SafeLinks URL, else the url itself."""
    from urllib.parse import urlparse, parse_qs, unquote
    try:
        p = urlparse(url)
        if "safelinks.protection.outlook.com" in p.netloc:
            q = parse_qs(p.query)
            if "url" in q and q["url"]:
                return unquote(q["url"][0])
    except Exception:
        pass
    return url


def extract_edgar(body):
    """Find the EDGAR index link (through SafeLinks) and return CIK + accession."""
    text = body or ""
    urls = re.findall(r"https?://[^\s<>\"\]]+", text)
    resolved = [_unwrap_safelinks(u) for u in urls]
    cik = accession = index_url = None
    for u in resolved:
        if "sec.gov/Archives/edgar/data/" not in u:
            continue
        m_cik = re.search(r"/data/(\d+)/", u)
        m_dash = re.search(r"\d{10}-\d{2}-\d{6}", u)  # dashed accession
        acc = None
        if m_dash:
            acc = m_dash.group(0)
        else:
            m_folder = re.search(r"/data/\d+/(\d{18})", u)  # no-dash folder
            if m_folder:
                d = m_folder.group(1)
                acc = f"{d[:10]}-{d[10:12]}-{d[12:]}"
        if m_cik and cik is None:
            cik = int(m_cik.group(1))
        if acc and accession is None:
            accession = acc
        if cik and accession:
            index_url = u
            break
    return {"cik": cik, "accession": accession, "index_url": index_url}

def detect_subtype(body):
    """ipo vs despac. SPACInsider tags deSPAC registrations explicitly, and they
    carry a target ('DeSPAC Company Name:'); those are out of scope for the IPO
    extraction path."""
    text = (body or "")
    low = text.lower()
    despac_target = None
    m = re.search(r"deSPAC Company Name:\s*(.+)", text, re.IGNORECASE)
    if m:
        despac_target = m.group(1).strip().splitlines()[0].strip()
    is_despac = ("despac" in low) or bool(m) or ("business combination" in low and "registration statement" in low)
    return {"subtype": "despac" if is_despac else "ipo", "despac_target": despac_target}


def parse_email(subject, body):
    out = {
        "filing_type": classify_subject(subject),
        "spac_name": clean_spac_name(subject),
    }
    out.update(extract_edgar(body))
    out.update(detect_subtype(body))
    out["in_scope"] = (out["filing_type"] in ("S-1", "S-1/A")) and (out["subtype"] == "ipo")
    return out

# ---- .eml convenience (for testing / saved messages) -----------------------

def read_eml(path):
    import email
    from email import policy
    with open(path, "rb") as fh:
        msg = email.message_from_binary_file(fh, policy=policy.default)
    subject = msg.get("subject", "")
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    body += part.get_content()
                except Exception:
                    payload = part.get_payload(decode=True) or b""
                    body += payload.decode("utf-8", "replace")
        if not body:
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    payload = part.get_payload(decode=True) or b""
                    body += payload.decode("utf-8", "replace")
    else:
        payload = msg.get_payload(decode=True) or b""
        body = payload.decode("utf-8", "replace")
    return subject, body

# ---- CLI -------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--window", action="store_true", help="compute this run's scan window")
    ap.add_argument("--session", choices=["morning", "afternoon"], help="force the session")
    ap.add_argument("--now", help="ISO datetime to treat as 'now' (testing)")
    ap.add_argument("--parse", action="store_true", help="parse an alert")
    ap.add_argument("--subject", help="alert subject line")
    ap.add_argument("--body-file", help="path to a file containing the alert body text")
    ap.add_argument("--eml", help="path to a .eml file (implies --parse)")
    args = ap.parse_args()

    if args.window:
        print(json.dumps(session_window(args.now, args.session), indent=2))
        return

    if args.eml:
        subject, body = read_eml(args.eml)
        print(json.dumps(parse_email(subject, body), indent=2))
        return

    if args.parse:
        subject = args.subject or ""
        body = ""
        if args.body_file:
            with open(args.body_file, "r", encoding="utf-8", errors="replace") as fh:
                body = fh.read()
        print(json.dumps(parse_email(subject, body), indent=2))
        return

    ap.print_help()


if __name__ == "__main__":
    main()
