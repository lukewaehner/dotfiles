#!/usr/bin/env python3
"""
Pre-send gate for Meteora internal email HTML.

    python3 validate_html.py note.html [--mode standard|enhanced]

Catches the mechanical failures: markup Outlook's Word engine strips or breaks,
off-palette colour, unfilled placeholders, and the structural tells that the
template was rebuilt from memory instead of copied.

It does NOT check the three things that matter most, because it cannot see them:
that the content the user asked for is on top and complete, that the provenance
stamp matches who wrote the body, and that every recipient is inside
meteoracapital.com. Those are on you.

Exit 0 = clean. Exit 1 = errors found; do not send.

It cannot judge whether the writing is any good. That is still on you.
"""

import argparse
import re
import sys

PALETTE = {
    "#0f2942", "#1a1a1a", "#334155", "#475569", "#64748b",
    "#94a3b8", "#c0392b", "#e2e8f0", "#f1f5f9", "#f8fafc",
    "#000000",  # tolerated: Outlook injects it into quoted-chain furniture
}

RAIL_MARKER = "Background &mdash; history and reference, for anyone catching up"
RAIL_MARKER_ALT = "Background — history and reference, for anyone catching up"
RAIL_STYLE = "border-left:3px solid"

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_outlook_safety(html):
    """Markup Outlook desktop strips, ignores, or renders wrong."""
    if re.search(r"<style[\s>]", html, re.I):
        err("<style> block present — Outlook strips it. Inline every rule.")
    if re.search(r'\sclass\s*=\s*["\']', html):
        err("CSS class attribute present — no stylesheet survives. Inline it.")
    if re.search(r"display\s*:\s*(flex|grid)", html, re.I):
        err("flexbox/grid present — Word's engine does not implement it. Use tables.")
    if re.search(r"<(details|summary)[\s>]", html, re.I):
        err(
            "<details>/<summary> present — renders permanently OPEN in Outlook "
            "desktop. Collapsible sections were built, tested and removed; "
            "no technique works there."
        )
    if re.search(r'type\s*=\s*["\']checkbox["\']', html, re.I):
        err(":checked accordion hack present — fails in Outlook for the same reason.")
    if re.search(r"position\s*:\s*(absolute|fixed|sticky)", html, re.I):
        err("CSS positioning present — unsupported in Word's engine.")
    if re.search(r"<script[\s>]", html, re.I):
        err("<script> present — stripped by every mail client.")
    if "@media" in html:
        warn("@media query present — Outlook desktop ignores it. Harmless but inert.")


def check_palette(html):
    # Strip HTML numeric entities first: &#128196; (the 📄 glyph) otherwise reads
    # as the hex colour #128196 and fails a perfectly good note.
    stripped = re.sub(r"&#[0-9]+;", "", html)
    for hexcode in set(re.findall(r"#[0-9a-fA-F]{6}", stripped)):
        if hexcode.lower() not in PALETTE:
            err(f"off-palette colour {hexcode} — see references/style-tokens.md")


def check_wrapper(html):
    if "max-width:640px" not in html.replace(" ", ""):
        err("wrapper missing max-width:640px — the note will run full-bleed.")
    if "font-family:Helvetica,Arial,sans-serif" not in html.replace(" ", ""):
        err("wrapper missing the house font stack.")


def check_placeholders(html):
    left = re.findall(r"\{\{[^}]{0,80}\}\}", html)
    if left:
        sample = ", ".join(left[:3])
        err(f"{len(left)} unfilled placeholder(s) remain: {sample}")


def check_quoted_chain(html):
    if "divRplyFwdMsg" in html or re.search(r"<hr[^>]*tabindex", html, re.I):
        warn(
            "quoted-chain furniture (divRplyFwdMsg / Outlook <hr>) found in the "
            "payload — emit only the NEW block; the client appends the history."
        )


def check_rail(html):
    """Structural tells that the background rail was rebuilt rather than copied.

    Applies to both enhanced categories: SPAC (--mode enhanced) and merger-arb
    (--mode enhanced-railonly) both get a background rail when there's genuinely
    supporting detail to include.
    """
    if RAIL_MARKER in html or RAIL_MARKER_ALT in html:
        if RAIL_STYLE not in html:
            err(
                "background rail heading present but no border-left:3px rail — the "
                "recessed block was flattened. Re-copy references/background-rail.html."
            )
        if "font-size:12px" not in html.replace(" ", ""):
            err("rail is not at font-size:12px — it must sit visually subordinate to the body.")


def check_snapshot(html):
    """Structural tells that the SPAC Snapshot table was rebuilt rather than copied.

    SPAC-only (--mode enhanced). Merger-arb enhanced notes (--mode
    enhanced-railonly) never call this — there is no merger-arb Snapshot table,
    because a target/acquirer pair has no unit structure to group by instrument.
    """
    has_table = "<table" in html
    if not has_table:
        err("enhanced mode but no Snapshot table — copy references/snapshot-table.html")

    if has_table:
        order, pos = [], {}
        for block in ("COMMON", "WARRANTS", "RIGHTS", "UNITS", "DEAL"):
            m = re.search(r"<b>\s*" + block + r"\b", html)
            if m:
                order.append(block)
                pos[block] = m.start()
        for block in ("COMMON", "DEAL"):
            if block not in pos:
                err(f"Snapshot missing the {block} block — the table is grouped by instrument.")
        if "DEAL" in pos and order and order[-1] != "DEAL":
            err("DEAL is not the last block in the Snapshot — instrument order is COMMON→WARRANTS→RIGHTS→UNITS→DEAL.")
        if order and order[0] != "COMMON":
            err("COMMON is not the first block in the Snapshot — instrument order is COMMON→WARRANTS→RIGHTS→UNITS→DEAL.")
        for tell in ("Prices", "Our position", "Unit structure", "CIT"):
            # match the group-row label however it is parenthesised or closed
            if re.search(r"<b>\s*" + tell + r"\b", html):
                err(
                    f'data-type-grouped block "{tell}" — the table is grouped by '
                    "INSTRUMENT, not by data type. It was rebuilt from memory; "
                    "re-copy references/snapshot-table.html."
                )
        if "Stage" not in html:
            warn("Snapshot has no Stage row — it is the last row of the Deal block.")


def check_no_spac_table(html):
    """Merger-arb enhanced notes get no Snapshot table — flag it if one snuck in."""
    if "<table" in html and re.search(r"<b>\s*(COMMON|WARRANTS|RIGHTS|UNITS)\b", html):
        err(
            "enhanced-railonly mode contains an instrument-grouped Snapshot table "
            "— merger-arb names don't get the SPAC Snapshot (no unit structure to "
            "group by). Drop the table, or if this is actually a SPAC name use "
            "--mode enhanced instead."
        )


def check_red_ration(html):
    """Red marks facts needing attention. It only works while it stays rare."""
    spans = re.findall(r'<span style="color:#c0392b[^>]*>(.*?)</span>', html, re.S)
    if len(spans) > 2:
        warn(
            f"{len(spans)} red spans — red marks a fact needing attention, not "
            "emphasis. Above two per note the ration has slipped; re-read them and "
            "cut any that are conclusions rather than facts."
        )


def check_playbook(html):
    if "PLAYBOOK" in html:
        warn(
            "PLAYBOOK line present — this skill drops it by default (Luke, 13:59). "
            "Keep it only if explicitly asked."
        )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument(
        "--mode",
        choices=["standard", "enhanced", "enhanced-railonly"],
        default="standard",
    )
    a = ap.parse_args()

    html = open(a.path, encoding="utf-8").read()

    check_outlook_safety(html)
    check_palette(html)
    check_wrapper(html)
    check_placeholders(html)
    check_quoted_chain(html)
    check_red_ration(html)
    check_playbook(html)

    if a.mode == "enhanced":
        # SPAC name: rail (optional) + required Snapshot table.
        check_rail(html)
        check_snapshot(html)
    elif a.mode == "enhanced-railonly":
        # Merger-arb name: rail (optional), no Snapshot table.
        check_rail(html)
        check_no_spac_table(html)
    else:
        if "<table" in html:
            err("standard mode contains a table — standard mode is the shell alone.")
        if RAIL_MARKER in html or RAIL_MARKER_ALT in html:
            err("standard mode contains the background rail — standard mode is the shell alone.")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\n{len(errors)} error(s) — do not send.")
        return 1
    print(f"OK — {a.mode} mode clean" + (f" ({len(warnings)} warning(s))" if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
