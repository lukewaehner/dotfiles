#!/usr/bin/env python3
"""deal_clock.py - deterministic date and spread arithmetic for merger-arb memos.

Why this exists: in the PTC / Schneider run the same hand arithmetic was redone in ad hoc
Python several times (business-day deadlines, outside-date ladder, annualized spread, implied
entry price), and a broker note landed three days off on the HSR deadline because the agreement's
"Business Day" definition also excluded Paris bank holidays. Run this script instead of doing the
math inline, and quote its output.

Subcommands (all print plain text; add --json for machine-readable output):

  bdays   --start 2026-10-04 --n 25 --cal us,fr
          Date that is N business days after START. --cal picks the holiday calendars to skip:
          us (US federal / New York bank holidays), fr (France public holidays), none. Weekends
          are always skipped. Read the agreement's "Business Day" definition first and pick the
          calendars it names.

  ladder  --signing 2026-10-04 --announce 2026-10-05 --initial 2027-04-04 --months 3,6,9
          Outside-date ladder: each extension date as an offset from the initial end date, with
          days from signing and from announcement. Optional --guidance 2027-09-30 adds a row
          that shows which extension the company's own closing guidance needs.

  spread  --price 192.50 --deal 205 --close 2027-06-30 --asof 2026-10-05 [--close ... repeat]
          Gross spread in dollars and percent, and annualized return (spread% x 365/days) for
          each close date.

  implied --deal 205 --irr 0.08 --baseline 2027-06-30 --asof 2026-10-05 [--shift 30]
          Entry-price table for baseline -30 / baseline / baseline +30 days (or +/- --shift):
          spread % needed = irr x days/365; spread $ = deal x spread%; entry = deal/(1+spread%).
          The table shows day counts only, per the house IRR format.

  hurdle  --price 192.50 --deal 205 --irr 0.08 --asof 2026-10-05
          The close date at which the current price earns exactly the target IRR.

  decompose --price 192.50 --deal 205 --close 2027-06-30 --asof 2026-10-05 --rf 0.04
          Splits the gross spread into time value (risk-free rate x days/365 x price) and the
          residual (technical supply premium + deal-risk premium). --rf must come from a sourced
          current rate; the script refuses to guess one.

  downside --price 192.50 --deal 205 --unaffected 144.06
          Dollar upside, dollar downside to the unaffected (or peer-adjusted) price, and the ratio.

  adddays --start 2026-11-18 --n 180 [--base 2027-04-30] [--outside 2027-10-05]
          Date that is N calendar days after START (a state notice or review clock counted from the
          FILING date, not announcement). With --base it prints the gap to the base-case close;
          with --outside it prints the days left inside the outside date. Run it once per state
          clock, at the latest permitted filing date and at an early date. Statutory clocks usually
          run from a complete notice and can be tolled by information requests: say so in the table.

Dates are ISO (YYYY-MM-DD). The script uses only the standard library.
"""
import argparse
import json
import sys
from datetime import date, timedelta


# ----------------------------------------------------------------------------- calendars
def _easter(year):
    """Western Easter Sunday (anonymous Gregorian algorithm)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def _nth_weekday(year, month, weekday, n):
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(year, month, weekday):
    d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def _observed(d):
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def us_holidays(year):
    """US federal holidays, which also close New York banks. Observed-date rule applied."""
    h = {
        _observed(date(year, 1, 1)),
        _nth_weekday(year, 1, 0, 3),   # MLK
        _nth_weekday(year, 2, 0, 3),   # Presidents
        _last_weekday(year, 5, 0),     # Memorial
        _observed(date(year, 6, 19)),  # Juneteenth
        _observed(date(year, 7, 4)),
        _nth_weekday(year, 9, 0, 1),   # Labor
        _nth_weekday(year, 10, 0, 2),  # Columbus / Indigenous Peoples
        _observed(date(year, 11, 11)), # Veterans
        _nth_weekday(year, 11, 3, 4),  # Thanksgiving
        _observed(date(year, 12, 25)),
    }
    return h


def fr_holidays(year):
    """French public holidays (fixed and Easter-based). No observed-date shifting in France."""
    e = _easter(year)
    return {
        date(year, 1, 1),
        e + timedelta(days=1),   # Easter Monday
        date(year, 5, 1),
        date(year, 5, 8),
        e + timedelta(days=39),  # Ascension
        e + timedelta(days=50),  # Whit Monday
        date(year, 7, 14),
        date(year, 8, 15),
        date(year, 11, 1),
        date(year, 11, 11),
        date(year, 12, 25),
    }


def holiday_set(cals, years):
    out = set()
    for c in cals:
        c = c.strip().lower()
        if c in ("", "none"):
            continue
        for y in years:
            if c == "us":
                out |= us_holidays(y)
            elif c == "fr":
                out |= fr_holidays(y)
            else:
                raise SystemExit(f"unknown calendar '{c}' (use us, fr or none)")
    return out


def add_business_days(start, n, cals):
    hol = holiday_set(cals, range(start.year, start.year + 3))
    d, count = start, 0
    while count < n:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in hol:
            count += 1
    return d


def add_months(d, months):
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    # clamp the day to the month length
    for day in (d.day, 30, 29, 28):
        try:
            return date(y, m, day)
        except ValueError:
            continue
    raise ValueError("bad date")


def iso(s):
    try:
        y, m, d = (int(x) for x in s.split("-"))
        return date(y, m, d)
    except Exception:
        raise argparse.ArgumentTypeError(f"bad date '{s}', use YYYY-MM-DD")


def days(a, b):
    return (b - a).days


def emit(args, text_lines, data):
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2, default=str))
    else:
        print("\n".join(text_lines))


# ----------------------------------------------------------------------------- commands
def cmd_bdays(a):
    cals = a.cal.split(",")
    end = add_business_days(a.start, a.n, cals)
    plain = add_business_days(a.start, a.n, ["none"])
    lines = [
        f"{a.n} business days after {a.start} (skipping weekends and calendars: {a.cal}) = {end} ({end:%A})",
        f"For reference, weekends-only count = {plain}",
    ]
    emit(a, lines, {"start": a.start, "n": a.n, "calendars": cals, "date": end, "weekends_only": plain})


def cmd_ladder(a):
    months = [int(m) for m in a.months.split(",")]
    rows = [("Initial end date", a.initial)] + [
        (f"Extension +{m} months", add_months(a.initial, m)) for m in months
    ]
    lines = ["Outside-date ladder (each extension is measured from the initial end date)",
             f"{'Step':<24}{'Date':<14}{'Days from signing':>18}{'Days from announce':>20}"]
    data = []
    for label, d in rows:
        lines.append(f"{label:<24}{d!s:<14}{days(a.signing, d):>18}{days(a.announce, d):>20}")
        data.append({"step": label, "date": d, "days_from_signing": days(a.signing, d),
                     "days_from_announce": days(a.announce, d)})
    if a.guidance:
        need = next((lbl for lbl, d in rows if d >= a.guidance), "beyond the last extension")
        lines.append(f"Company guidance {a.guidance} ({days(a.announce, a.guidance)} days from announce) "
                     f"first fits within: {need}")
        data.append({"guidance": a.guidance, "first_fits_within": need,
                     "days_from_announce": days(a.announce, a.guidance)})
    emit(a, lines, data)


def cmd_spread(a):
    gross = a.deal - a.price
    pct = a.deal / a.price - 1
    lines = [f"Price {a.price:.2f}  Deal {a.deal:.2f}  Gross spread ${gross:.2f} ({pct*100:.2f}%)",
             f"{'Close date':<14}{'Days':>6}{'Annualized %':>14}"]
    data = {"gross_dollars": gross, "gross_pct": pct, "scenarios": []}
    for c in a.close:
        n = days(a.asof, c)
        ann = pct * 365 / n
        lines.append(f"{c!s:<14}{n:>6}{ann*100:>14.2f}")
        data["scenarios"].append({"close": c, "days": n, "annualized_pct": ann})
    emit(a, lines, data)


def cmd_implied(a):
    shift = timedelta(days=a.shift)
    cases = [("Baseline - %d" % a.shift, a.baseline - shift), ("Baseline", a.baseline),
             ("Baseline + %d" % a.shift, a.baseline + shift)]
    lines = [f"Target IRR: {a.irr*100:.1f}%  Deal price {a.deal:.2f}",
             f"{'Timeline':<28}{'Spread % needed':>17}{'Spread $ needed':>17}{'Implied entry':>15}"]
    data = []
    for label, d in cases:
        n = days(a.asof, d)
        sp = a.irr * n / 365
        sd = a.deal * sp
        entry = a.deal / (1 + sp)
        lines.append(f"{label + ' (' + str(n) + ' days)':<28}{sp*100:>16.2f}%{sd:>17.2f}{entry:>15.2f}")
        data.append({"timeline": label, "days": n, "spread_pct": sp, "spread_dollars": sd,
                     "implied_entry": entry, "date": d})
    lines.append("House format: show day counts only in the memo table, no calendar dates.")
    emit(a, lines, data)


def cmd_hurdle(a):
    pct = a.deal / a.price - 1
    n = round(pct / a.irr * 365)
    d = a.asof + timedelta(days=n)
    lines = [f"At price {a.price:.2f} the gross spread is {pct*100:.2f}%.",
             f"It earns exactly {a.irr*100:.1f}% annualized if the deal closes in {n} days = {d}."]
    emit(a, lines, {"gross_pct": pct, "days": n, "date": d, "irr": a.irr})


def cmd_decompose(a):
    n = days(a.asof, a.close)
    gross = a.deal - a.price
    time_value = a.price * a.rf * n / 365
    resid = gross - time_value
    lines = [f"Gross spread ${gross:.2f} over {n} days (risk-free input {a.rf*100:.2f}%, must be sourced)",
             f"  Time value at the risk-free rate: ${time_value:.2f} ({time_value/a.price*100:.2f}% of price)",
             f"  Residual (supply/technical premium + deal-risk premium): ${resid:.2f} "
             f"({resid/a.price*100:.2f}% of price)",
             "Split the residual between technical and risk in words only; do not invent a percentage."]
    emit(a, lines, {"gross": gross, "days": n, "time_value": time_value, "residual": resid, "rf": a.rf})


def cmd_downside(a):
    up = a.deal - a.price
    down = a.price - a.unaffected
    ratio = down / up if up else float("inf")
    lines = [f"Upside to deal: ${up:.2f}   Downside to {a.unaffected:.2f}: ${down:.2f}   "
             f"Downside per $1 of upside: {ratio:.2f}",
             "Reference only: adjust the unaffected price for sector moves since the last close "
             "before using it as a break price."]
    emit(a, lines, {"upside": up, "downside": down, "ratio": ratio})


def cmd_adddays(a):
    end = a.start + timedelta(days=a.n)
    lines = [f"{a.n} calendar days after {a.start} = {end} ({end:%A})"]
    data = {"start": a.start, "n": a.n, "date": end}
    if a.base:
        d = (end - a.base).days
        lines.append(f"Versus base close {a.base}: {d:+d} days ({'later' if d > 0 else 'earlier' if d < 0 else 'same day'})")
        data["vs_base_days"] = d
    if a.outside:
        d = (a.outside - end).days
        lines.append(f"Days inside outside date {a.outside}: {d}")
        data["inside_outside_days"] = d
    emit(a, lines, data)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("bdays"); s.add_argument("--start", type=iso, required=True)
    s.add_argument("--n", type=int, required=True); s.add_argument("--cal", default="us,fr")
    s.set_defaults(fn=cmd_bdays)

    s = sub.add_parser("ladder"); s.add_argument("--signing", type=iso, required=True)
    s.add_argument("--announce", type=iso, required=True); s.add_argument("--initial", type=iso, required=True)
    s.add_argument("--months", default="3,6,9"); s.add_argument("--guidance", type=iso)
    s.set_defaults(fn=cmd_ladder)

    s = sub.add_parser("spread"); s.add_argument("--price", type=float, required=True)
    s.add_argument("--deal", type=float, required=True); s.add_argument("--asof", type=iso, required=True)
    s.add_argument("--close", type=iso, action="append", required=True); s.set_defaults(fn=cmd_spread)

    s = sub.add_parser("implied"); s.add_argument("--deal", type=float, required=True)
    s.add_argument("--irr", type=float, default=0.08); s.add_argument("--baseline", type=iso, required=True)
    s.add_argument("--asof", type=iso, required=True); s.add_argument("--shift", type=int, default=30)
    s.set_defaults(fn=cmd_implied)

    s = sub.add_parser("hurdle"); s.add_argument("--price", type=float, required=True)
    s.add_argument("--deal", type=float, required=True); s.add_argument("--irr", type=float, default=0.08)
    s.add_argument("--asof", type=iso, required=True); s.set_defaults(fn=cmd_hurdle)

    s = sub.add_parser("decompose"); s.add_argument("--price", type=float, required=True)
    s.add_argument("--deal", type=float, required=True); s.add_argument("--close", type=iso, required=True)
    s.add_argument("--asof", type=iso, required=True); s.add_argument("--rf", type=float, required=True)
    s.set_defaults(fn=cmd_decompose)

    s = sub.add_parser("downside"); s.add_argument("--price", type=float, required=True)
    s.add_argument("--deal", type=float, required=True); s.add_argument("--unaffected", type=float, required=True)
    s.set_defaults(fn=cmd_downside)

    s = sub.add_parser("adddays"); s.add_argument("--start", type=iso, required=True)
    s.add_argument("--n", type=int, required=True); s.add_argument("--base", type=iso)
    s.add_argument("--outside", type=iso); s.set_defaults(fn=cmd_adddays)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
