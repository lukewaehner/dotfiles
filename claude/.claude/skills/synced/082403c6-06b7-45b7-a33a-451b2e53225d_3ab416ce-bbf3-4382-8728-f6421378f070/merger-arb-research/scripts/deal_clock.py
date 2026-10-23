#!/usr/bin/env python3
"""deal_clock.py - deterministic date and spread arithmetic for merger-arb memos.

Why this exists: hand date arithmetic in memos drifts (business-day deadlines that ignore a
foreign holiday calendar named in the agreement's "Business Day" definition, close dates that land
on a Sunday, annualized spreads on the wrong day count). Run this script instead of doing the math
inline, and quote its output.

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

  hurdle  --price 192.50 --deal 205 --irr 0.08 --asof 2026-10-05
          The close date at which the current price earns exactly the target IRR.

  decompose --price 192.50 --deal 205 --close 2027-06-30 --asof 2026-10-05 --rf 0.04
          Splits the gross spread into time value (risk-free rate x days/365 x price) and the
          residual (technical supply premium + deal-risk premium). --rf must come from a sourced
          current rate; the script refuses to guess one.

  downside --price 192.50 --deal 205 --unaffected 144.06
          Dollar upside, dollar downside to the unaffected (or peer-adjusted) price, and the ratio.

  limit   (sensitivity only, needs a failure chance supplied by the user; not part of the default report) --deal 7.75 --downside 5.40 --asof 2026-10-15 --close 2027-01-25 [--late 2027-04-06]
          [--hurdle 0.075] [--breaks 0.03,0.07,0.15,0.30] [--price 7.40]
          Limit price for each break-risk band: the expected value ((1-b) x deal + b x downside)
          discounted at the hurdle to the close date. Shows the working and late cases and, with
          --price, the market-implied break probability for comparison.

  cases   --asof 2026-10-17 --deal 7.75 --price 7.61[,7.55,7.50] --downside 6.00 [--hurdle 0.075]
          --case "On schedule|2027-01-25" --case "Delayed|2027-03-19" --case "Deadline|2027-04-10"
          Dated cases with no probabilities of our own. For each closing date: days, the highest price
          that still earns the minimum return on a clean close (ceiling), and for each price tested the
          annual return if the deal closes then and the chance of failure the price implies after paying
          the minimum return for waiting (negative means the price is above the ceiling). Also prints the
          dollars gained and lost and the latest closing date at which the last price earns the minimum.

  adddays --start 2026-11-18 --n 180 [--base 2027-04-30] [--outside 2027-10-05]
          Date that is N calendar days after START (a state notice or review clock counted from the
          FILING date, not announcement). With --base it prints the gap to the base-case close;
          with --outside it prints the days left inside the outside date. Run it once per state
          clock, at the latest permitted filing date and at an early date. Statutory clocks usually
          run from a complete notice and can be tolled by information requests: say so in the table.

  tender  --agreement 2026-10-08 --cal us [--launch-bd 15] [--hsr-bd 15] [--offer-bd 10] [--hsr-days 15]
          [--refile-gap-bd 1] [--early 2026-10-22] [--check 2026-11-13 --check 2026-11-15]
          [--second-request-compliance 2027-02-01] [--announce 2026-10-08]
          Cash-tender-offer clock. Builds the earliest close from the agreement's own covenants:
            launch and HSR filing deadlines = N business days after the agreement date, counted on the
            calendar the agreement's Business Day definition names (--cal), then
            HSR expiry = filing + 15 calendar days (30 for a one-step merger), rolled forward off a
            weekend or federal holiday, expiring at 11:59 pm ET;
            initial offer expiry = --offer-bd business days after launch (SEC Rule 14d-1(g)(3): every day
            except Saturday, Sunday and federal holidays, so US holidays always apply here);
            earliest close = the business day AFTER the later of the two expiries.
          Prints, in one table: the deadline case on the agreement's calendar, the same deadline on a
          weekends-only count (shown whenever the two counts differ, because brokers use both), an
          optional early-filing case (--early), a one-pull-and-refile case for each (the parties withdraw
          on the last day and refile --refile-gap-bd business days later; the new 15 days run from the
          refile), and, only if a compliance date is supplied, a second-request case (10 days after
          substantial compliance for a cash tender, 30 for a merger; the script never guesses the
          compliance date). --check tests a date someone else quoted: weekend or holiday, earlier than
          physically possible, or feasible only if the parties file by a stated date.

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
    width = a.deal - a.unaffected
    p_break = up / width if width else float("nan")
    lines = [f"Upside to deal: ${up:.2f}   Downside to {a.unaffected:.2f}: ${down:.2f}   "
             f"Downside per $1 of upside: {ratio:.2f}",
             f"Market-implied break probability (no carry): {p_break:.1%}  = (deal - price) / (deal - downside)"]
    data = {"upside": up, "downside": down, "ratio": ratio, "implied_break_no_carry": p_break}
    if a.rf is not None and a.close and a.asof:
        t = days(a.asof, a.close) / 365.0
        fwd = a.price * (1 + a.rf * t)
        p2 = (a.deal - fwd) / width if width else float("nan")
        lines.append(f"Market-implied break probability with carry at rf {a.rf:.2%} to {a.close}: {p2:.1%}  "
                     f"= (deal - price x (1 + rf x t)) / (deal - downside)")
        data["implied_break_with_carry"] = p2
    lines.append("The downside is an estimate: state its basis (unaffected price, peer- or index-adjusted, multiple). "
                 "Run it at the low and high end of the downside range.")
    emit(a, lines, data)


def cmd_limit(a):
    def lim(close, b):
        t = days(a.asof, close) / 365.0
        ev = (1 - b) * a.deal + b * a.downside
        return ev / (1 + a.hurdle * t), ev, t
    lines = [f"Limit price = expected value / (1 + hurdle x t);  expected value = (1 - b) x deal + b x downside",
             f"Deal {a.deal:.2f}  Downside {a.downside:.2f}  Hurdle {a.hurdle:.1%} annualized  As of {a.asof}"]
    data = {"rows": []}
    lines.append(f"{'Break risk b':>13} {'Close':>11} {'Days':>5} {'Exp. value':>11} {'Limit':>8}")
    for b in a.breaks:
        for close, tag in [(a.close, "working"), (a.late, "late")]:
            if close is None:
                continue
            L, ev, t = lim(close, b)
            lines.append(f"{b:>13.0%} {str(close):>11} {days(a.asof, close):>5} {ev:>11.2f} {L:>8.2f}  ({tag})")
            data["rows"].append({"break": b, "close": close, "case": tag, "ev": ev, "limit": L})
    if a.price is not None:
        width = a.deal - a.downside
        p0 = (a.deal - a.price) / width if width else float("nan")
        lines.append(f"At the current price {a.price:.2f} the market-implied break probability (no carry) is {p0:.1%}.")
        data["implied_break_no_carry"] = p0
    lines.append("b is the analyst's break-risk band (upper edge), stated as a view with its reasons. "
                 "Use the late-case row when the working close is uncertain.")
    emit(a, lines, data)


def cmd_cases(a):
    """Dated cases, no probabilities of our own. Prints returns, a clean-close ceiling and the market-implied chance of failure."""
    prices = a.price
    last = prices[0]
    rows = []
    for raw in a.case:
        parts = [x.strip() for x in raw.split("|")]
        if len(parts) != 2:
            sys.exit(f"--case needs label|date, got: {raw}")
        label, when = parts
        close = iso(when)
        n = days(a.asof, close)
        if n <= 0:
            sys.exit(f"Case '{label}' is dated on or before the as-of date.")
        t = n / 365.0
        width = a.deal - a.downside
        row = {"label": label, "date": close, "days": n, "ceiling": a.deal / (1 + a.hurdle * t), "by_price": []}
        for p_ in prices:
            ann = (a.deal / p_ - 1) / t
            implied_after = 1 - (p_ * (1 + a.hurdle * t) - a.downside) / width
            row["by_price"].append({"price": p_, "ann_if_closes": ann, "implied_failure_after_hurdle": implied_after})
        rows.append(row)
    width = a.deal - a.downside
    lines = [f"Dated cases as of {a.asof}; deal {a.deal:.2f}, price if the deal fails {a.downside:.2f}, minimum return {a.hurdle:.1%} a year "
             f"(simple interest, days/365). No probabilities of our own are used; the only probabilities are market-implied.",
             f"Dollars gained if it closes / lost if it fails, per share: " + ", ".join(
                 f"at {p_:.2f}: {a.deal - p_:.2f} / {p_ - a.downside:.2f} (needs {(p_ - a.downside) / width:.1%} completion to break even with no carry)" for p_ in prices),
             "A negative implied chance of failure means the price is above what even a clean close pays at the minimum return.",
             f"{'Case':<30}{'Date':>12}{'Days':>6}{'Clean-close ceiling':>21}" +
             "".join(f"{'@' + format(p_, '.2f') + ' return':>14}{'@' + format(p_, '.2f') + ' implied fail':>20}" for p_ in prices)]
    for r in rows:
        lines.append(f"{r['label'][:29]:<30}{str(r['date']):>12}{r['days']:>6}{r['ceiling']:>21.2f}" +
                     "".join(f"{x['ann_if_closes']:>14.1%}{x['implied_failure_after_hurdle']:>20.1%}" for x in r["by_price"]))
    t0 = (a.deal / last - 1) / a.hurdle
    zero_date = a.asof + timedelta(days=int(t0 * 365))
    lines.append(f"The price {last:.2f} earns {a.hurdle:.1%} on a clean close only if the deal closes by {zero_date}.")
    for p_ in prices:
        lines.append(f"Market-implied chance of failure at {p_:.2f} with no return for waiting: {(a.deal - p_) / width:.1%}.")
    data = {"cases": rows, "clean_close_date_at_last_price": zero_date}
    emit(a, lines, data)


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


# ----------------------------------------------------------------------------- tender clock
def is_bd(d, hol):
    return d.weekday() < 5 and d not in hol


def roll_forward(d, hol):
    """Move d to the next business day if it falls on a weekend or holiday (HSR rule for an expiry date)."""
    while not is_bd(d, hol):
        d += timedelta(days=1)
    return d


def next_bd(d, hol):
    d += timedelta(days=1)
    return roll_forward(d, hol)


def bd_after(d, n, hol):
    c = 0
    while c < n:
        d += timedelta(days=1)
        if is_bd(d, hol):
            c += 1
    return d


def tender_case(label, launch, filed, a, us_hol):
    """One row: launch and HSR filing dates in, earliest close out. HSR roll and SEC offer count use US holidays."""
    hsr_exp = roll_forward(filed + timedelta(days=a.hsr_days), us_hol)
    offer_exp = bd_after(launch, a.offer_bd, us_hol)
    binding = "HSR" if hsr_exp >= offer_exp else "offer period"
    close = next_bd(max(hsr_exp, offer_exp), us_hol)
    return {"case": label, "launch": launch, "hsr_filed": filed, "hsr_expiry": hsr_exp,
            "offer_expiry": offer_exp, "binding": binding, "earliest_close": close,
            "offer_must_be_extended": offer_exp < hsr_exp}


def refile_case(base, a, us_hol):
    """Parties pull on the last day of the first waiting period and refile; the clock restarts from the refile."""
    pull = base["hsr_expiry"]
    refiled = bd_after(pull, a.refile_gap_bd, us_hol) if a.refile_gap_bd else pull
    row = tender_case(base["case"] + " + 1 refile", base["launch"], refiled, a, us_hol)
    row["pulled_on"] = pull
    return row


def cmd_tender(a):
    cals = a.cal.split(",")
    us_hol = holiday_set(["us"], range(a.agreement.year, a.agreement.year + 3))
    ann = a.announce or a.agreement
    launch_dl = add_business_days(a.agreement, a.launch_bd, cals)
    file_dl = add_business_days(a.agreement, a.hsr_bd, cals)
    launch_wk = add_business_days(a.agreement, a.launch_bd, ["none"])
    file_wk = add_business_days(a.agreement, a.hsr_bd, ["none"])

    rows = [tender_case(f"Deadline ({a.cal} calendar)", launch_dl, file_dl, a, us_hol)]
    if (launch_wk, file_wk) != (launch_dl, file_dl):
        rows.append(tender_case("Deadline (weekends-only count)", launch_wk, file_wk, a, us_hol))
    if a.early:
        rows.append(tender_case("Early filing (input)", a.early, a.early, a, us_hol))
    base_rows = list(rows)
    for r in base_rows:
        rows.append(refile_case(r, a, us_hol))
    if a.second_request_compliance:
        wait = 10 if a.hsr_days == 15 else 30
        sr_exp = roll_forward(a.second_request_compliance + timedelta(days=wait), us_hol)
        sr_close = next_bd(sr_exp, us_hol)
        rows.append({"case": f"Second request (+{wait}d after compliance)",
                     "launch": None, "hsr_filed": None, "hsr_expiry": sr_exp, "offer_expiry": None,
                     "binding": "HSR", "earliest_close": sr_close, "offer_must_be_extended": True})

    lines = [f"Tender clock - agreement {a.agreement}, Business Day calendar '{a.cal}', announce {ann}",
             f"Covenants: launch within {a.launch_bd} BD = {launch_dl} ({launch_dl:%a}); "
             f"HSR within {a.hsr_bd} BD = {file_dl} ({file_dl:%a}); initial offer {a.offer_bd} BD; "
             f"HSR period {a.hsr_days} days",
             f"{'Case':<44}{'Launch':<12}{'HSR filed':<12}{'HSR expiry':<17}{'Offer expiry':<17}"
             f"{'Earliest close':<18}{'Days':>5}"]
    for r in rows:
        def f(d):
            return f"{d} {d:%a}"[:16] if d else "-"
        lines.append(f"{r['case']:<44}{str(r['launch'] or '-'):<12}{str(r['hsr_filed'] or '-'):<12}"
                     f"{f(r['hsr_expiry']):<17}{f(r['offer_expiry']):<17}"
                     f"{f(r['earliest_close']):<18}{days(ann, r['earliest_close']):>5}")
        r["days_from_announce"] = days(ann, r["earliest_close"])
    lines.append("HSR expires at 11:59 pm ET; a Saturday, Sunday or holiday expiry rolls to the next business day; "
                 "close = next business day after the later of HSR expiry and offer expiry.")
    if any(r["offer_must_be_extended"] for r in rows[:len(base_rows)]):
        lines.append("Offer expiry falls before HSR expiry in at least one case: the offer must be extended once; "
                     "confirm the agreement's mandatory-extension clause.")
    if not a.second_request_compliance:
        lines.append("Second request: no date computed. Supply --second-request-compliance with a sourced "
                     "substantial-compliance date; the script will not guess one.")
    lines.append("Refile rows assume the parties pull on the last day of the first period. They are a downside "
                 "scenario unless the cited precedents needed one.")

    checks = []
    for t in (a.check or []):
        verdict = ""
        if t.weekday() >= 5 or t in us_hol:
            verdict = "cannot be a closing date (weekend or holiday)"
        else:
            # latest filing date (business days, launch same day) that still closes on or before t
            latest = None
            d = a.agreement
            while d <= file_dl:
                if is_bd(d, us_hol):
                    r = tender_case("x", d, d, a, us_hol)
                    if r["earliest_close"] <= t:
                        latest = d
                d += timedelta(days=1)
            if latest is None:
                first = tender_case("x", a.agreement, a.agreement, a, us_hol)["earliest_close"]
                verdict = f"not physically possible (earliest conceivable close if filed on signing is {first})"
            elif latest >= file_dl:
                verdict = "feasible even if the parties use the full covenant period"
            else:
                verdict = (f"feasible only if HSR is filed and the offer launched on or before {latest} "
                           f"(covenant deadline {file_dl})")
        lines.append(f"Check {t} ({t:%A}): {verdict}")
        checks.append({"date": t, "weekday": f"{t:%A}", "verdict": verdict})
    emit(a, lines, {"agreement": a.agreement, "calendar": cals, "launch_deadline": launch_dl,
                    "hsr_deadline": file_dl, "rows": rows, "checks": checks})


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
    s.add_argument("--rf", type=float); s.add_argument("--close", type=iso); s.add_argument("--asof", type=iso)
    s.set_defaults(fn=cmd_downside)

    s = sub.add_parser("limit"); s.add_argument("--deal", type=float, required=True)
    s.add_argument("--downside", type=float, required=True); s.add_argument("--asof", type=iso, required=True)
    s.add_argument("--close", type=iso, required=True); s.add_argument("--late", type=iso)
    s.add_argument("--hurdle", type=float, default=0.075)
    s.add_argument("--breaks", type=lambda x: [float(v) for v in x.split(",")], default=[0.03, 0.07, 0.15, 0.30])
    s.add_argument("--price", type=float); s.set_defaults(fn=cmd_limit)

    s = sub.add_parser("cases"); s.add_argument("--asof", type=iso, required=True)
    s.add_argument("--deal", type=float, required=True)
    s.add_argument("--price", type=lambda x: [float(v) for v in x.split(",")], required=True,
                   help="last price, optionally followed by other prices to test: 7.61,7.55,7.50")
    s.add_argument("--downside", type=float, required=True); s.add_argument("--hurdle", type=float, default=0.075)
    s.add_argument("--case", action="append", required=True, help="label|date")
    s.set_defaults(fn=cmd_cases)

    s = sub.add_parser("adddays"); s.add_argument("--start", type=iso, required=True)
    s.add_argument("--n", type=int, required=True); s.add_argument("--base", type=iso)
    s.add_argument("--outside", type=iso); s.set_defaults(fn=cmd_adddays)

    s = sub.add_parser("tender"); s.add_argument("--agreement", type=iso, required=True)
    s.add_argument("--cal", default="us"); s.add_argument("--launch-bd", dest="launch_bd", type=int, default=15)
    s.add_argument("--hsr-bd", dest="hsr_bd", type=int, default=15)
    s.add_argument("--offer-bd", dest="offer_bd", type=int, default=10)
    s.add_argument("--hsr-days", dest="hsr_days", type=int, default=15)
    s.add_argument("--refile-gap-bd", dest="refile_gap_bd", type=int, default=1)
    s.add_argument("--early", type=iso); s.add_argument("--announce", type=iso)
    s.add_argument("--check", type=iso, action="append")
    s.add_argument("--second-request-compliance", dest="second_request_compliance", type=iso)
    s.set_defaults(fn=cmd_tender)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
