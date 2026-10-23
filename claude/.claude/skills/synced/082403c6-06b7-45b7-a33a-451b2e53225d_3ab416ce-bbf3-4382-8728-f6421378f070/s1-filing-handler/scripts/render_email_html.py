#!/usr/bin/env python3
"""
render_email_html.py — convert the assembled markdown post into clean, email-safe,
inline-styled HTML for the s1-filing-handler.

House style: NEUTRAL and easy to read — no colors, just black text on white, grey
rules, and a light-grey table header. Clear demarcations: PART headings get a solid
underline, Section headings a light underline, horizontal rules between blocks, and
comfortable paragraph/line spacing. Inline styles ONLY (email clients strip <style>
blocks and external CSS).

Usage:  python render_email_html.py <input.md> <output.html>
"""
import sys, re, subprocess

def _markdown():
    try:
        import markdown
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "markdown",
                        "--break-system-packages", "-q"], check=False)
        import markdown
    return markdown

# Inline style per tag — neutral, readable, clear section/paragraph demarcation.
STYLES = {
    "h1": "font-size:19px;font-weight:bold;margin:26px 0 10px;padding-bottom:6px;border-bottom:2px solid #333;",
    "h2": "font-size:16px;font-weight:bold;margin:22px 0 8px;padding-bottom:4px;border-bottom:1px solid #bbb;",
    "h3": "font-size:14px;font-weight:bold;margin:16px 0 6px;",
    "h4": "font-size:13px;font-weight:bold;margin:14px 0 6px;",
    "hr": "border:none;border-top:1px solid #ccc;margin:18px 0;",
    "p":  "margin:0 0 8px;",
    "ul": "margin:0 0 10px;padding-left:22px;",
    "ol": "margin:0 0 10px;padding-left:22px;",
    "li": "margin:3px 0;",
    "table": "border-collapse:collapse;margin:8px 0 14px;font-size:13px;",
    "th": "border:1px solid #bbb;padding:6px 8px;background:#f2f2f2;text-align:left;font-weight:bold;vertical-align:top;",
    "td": "border:1px solid #ccc;padding:6px 8px;text-align:left;vertical-align:top;",
    "blockquote": "margin:6px 0;padding:4px 12px;border-left:3px solid #ccc;",
}

def _inline(html):
    # self-closing <hr /> handled first so it stays valid
    html = re.sub(r"<hr\s*/?>", '<hr style="%s" />' % STYLES["hr"], html)
    for tag, style in STYLES.items():
        if tag == "hr":
            continue
        def repl(m, t=tag, s=style):
            attrs = m.group(1)
            mm = re.search(r'style="([^"]*)"', attrs)
            if mm:  # merge: our base first, existing last (so md alignment overrides)
                merged = s.rstrip(";") + ";" + mm.group(1)
                attrs = attrs[:mm.start()] + 'style="%s"' % merged + attrs[mm.end():]
                return "<%s%s>" % (t, attrs)
            return '<%s%s style="%s">' % (t, attrs, s)
        html = re.sub(r"<%s(?![\w-])((?:\s+[^>]*?)?)>" % tag, repl, html)
    return html

def main():
    if len(sys.argv) < 3:
        print("usage: render_email_html.py <input.md> <output.html>"); sys.exit(1)
    md_text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    html = _markdown().markdown(md_text, extensions=["tables", "sane_lists", "fenced_code", "nl2br"])
    html = _inline(html)
    container = ('<div style="font-family:Calibri,\'Segoe UI\',Arial,sans-serif;'
                 'font-size:14px;line-height:1.5;color:#000;max-width:820px;">' + html + "</div>")
    open(sys.argv[2], "w", encoding="utf-8").write(container)
    print(f"wrote {sys.argv[2]} ({len(container)} chars)")

if __name__ == "__main__":
    main()
