#!/usr/bin/env python3
"""
note_utils.py - deterministic helpers for the initiation-coverage-scanner skill.

Subcommands:
  analyze       <note.pdf>                          measure a PDF note (pages/words/sections/gate)
  analyze-text  <note.txt>                           measure a plain-text / body note
  ledger-check  <ledger.json> <ticker> <provider> <message_id>   -> DUPLICATE | NEW
  ledger-append <ledger.json> <json-record>          append a processed-note record
  filename      <company> <ticker> <provider> <yyyy-mm-dd>       -> sanitized filename

The gate is intentionally simple and transparent. The model still makes the judgment
call about whether the email is a genuine *new* initiation; this script only measures
length + structure so every run applies the same substance bar.
"""
import sys, json, re, os

WORD_FLOOR = 2500          # substantive-content word floor
PAGE_BACKSTOP = 8          # used only when word count can't be measured
# Boilerplate/disclaimer markers - text after these is excluded from the word count
BOILERPLATE_MARKERS = [
    "important disclosures", "analyst certification", "regulation analyst certification",
    "reg ac", "disclosure appendix", "required disclosures",
    "distribution of ratings", "important disclosures required by",
]
SECTION_TERMS = {
    "valuation": ["valuation", "price target", "target price", "dcf", "sum-of-the-parts",
                  "sum of the parts", "ev/", "p/e", "multiple"],
    "estimates": ["estimates", "financial model", "forecast", "income statement",
                  "revenue", "eps", "ebitda", "projections", "our model"],
    "risks":     ["risks", "risk factors", "key risks", "downside", "bear case"],
}


def _read_pdf_text(path):
    """Extract text + page count. pdftotext (poppler) is the PRIMARY extractor: it is
    far more reliable than pypdf on sell-side research PDFs (embedded fonts, columns),
    where pypdf frequently under-extracts and would wrongly fail the length gate.
    pypdf is only a fallback if poppler is unavailable."""
    text, pages = "", 0
    import subprocess
    try:
        text = subprocess.check_output(["pdftotext", "-q", path, "-"], text=True)
    except Exception:
        text = ""
    try:
        out = subprocess.check_output(["pdfinfo", path], text=True)
        m = re.search(r"Pages:\s+(\d+)", out)
        pages = int(m.group(1)) if m else 0
    except Exception:
        pages = 0
    if len(text.split()) < 50:  # poppler missing or extracted almost nothing -> try pypdf
        try:
            from pypdf import PdfReader
            r = PdfReader(path)
            if not pages:
                pages = len(r.pages)
            t2 = "\n".join((p.extract_text() or "") for p in r.pages)
            if len(t2.split()) > len(text.split()):
                text = t2
        except Exception:
            pass
    return text, pages


def _strip_boilerplate(text):
    low = text.lower()
    n = len(text)
    cut = n
    # Only treat a disclosures marker as the start of the legal tail if it appears past
    # the halfway point. Earlier occurrences are page headers/watermarks (e.g. the
    # "important disclosures" nav line or a "this report is intended for" watermark) and
    # must not truncate the substantive body.
    for mk in BOILERPLATE_MARKERS:
        i = low.find(mk)
        if i != -1 and i > n * 0.5:
            cut = min(cut, i)
    return text[:cut]


def _measure(text, pages):
    body = _strip_boilerplate(text)
    words = len(re.findall(r"\b\w+\b", body))
    low = body.lower()
    sections = {name: any(t in low for t in terms) for name, terms in SECTION_TERMS.items()}
    # Pass on EITHER a healthy word count OR the page backstop. Text extraction can
    # under-count on some research PDFs, so page count is a first-class substance signal.
    passes_length = words >= WORD_FLOOR or pages >= PAGE_BACKSTOP
    # structure = has a valuation rationale AND (estimates OR risks) discussion
    passes_structure = sections["valuation"] and (sections["estimates"] or sections["risks"])
    return {
        "page_count": pages,
        "word_count": words,
        "sections": sections,
        "passes_length": passes_length,
        "passes_structure": passes_structure,
        "gate": "PASS" if (passes_length and passes_structure) else "FAIL",
        "word_floor": WORD_FLOOR,
        "page_backstop": PAGE_BACKSTOP,
    }


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def sanitize(s):
    return re.sub(r'[\\/:*?"<>|]', "", (s or "").strip())


def load_ledger(path):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return []
    return []


def cmd_analyze(path):
    text, pages = _read_pdf_text(path)
    print(json.dumps(_measure(text, pages), indent=2))


def cmd_analyze_text(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    print(json.dumps(_measure(text, 0), indent=2))


def cmd_ledger_check(ledger, ticker, provider, msgid):
    entries = load_ledger(ledger)
    key = norm(ticker) + "|" + norm(provider)
    for e in entries:
        if norm(e.get("ticker")) + "|" + norm(e.get("provider")) == key:
            print("DUPLICATE"); return
        if msgid and e.get("message_id") == msgid:
            print("DUPLICATE"); return
    print("NEW")


def cmd_ledger_append(ledger, record_json):
    entries = load_ledger(ledger)
    rec = json.loads(record_json)
    entries.append(rec)
    os.makedirs(os.path.dirname(os.path.abspath(ledger)), exist_ok=True)
    with open(ledger, "w") as f:
        json.dump(entries, f, indent=2)
    print("APPENDED")


def cmd_filename(company, ticker, provider, date):
    name = f"Initiation of Coverage - {sanitize(company)} ({sanitize(ticker)}) - {sanitize(provider)} - {date}.pdf"
    print(name)


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    c = a[0]
    try:
        if c == "analyze":            cmd_analyze(a[1])
        elif c == "analyze-text":     cmd_analyze_text(a[1])
        elif c == "ledger-check":     cmd_ledger_check(a[1], a[2], a[3], a[4] if len(a) > 4 else "")
        elif c == "ledger-append":    cmd_ledger_append(a[1], a[2])
        elif c == "filename":         cmd_filename(a[1], a[2], a[3], a[4])
        else:
            print(f"unknown subcommand: {c}"); print(__doc__); sys.exit(1)
    except IndexError:
        print(f"missing args for '{c}'"); print(__doc__); sys.exit(1)


if __name__ == "__main__":
    main()
