# Security Classification Reference

The reconciler needs one `classification` per unique ticker/identifier in a broker report.
Classify each into exactly one bucket below, then pass `{ticker: bucket}` to `reconcile.py`.
When a security cannot be confidently placed, use `unknown` (it becomes `NEEDS_REVIEW`) —
never guess it into an exempt bucket.

Buckets (the value you pass to reconcile):

| bucket | meaning | reconciler effect |
|---|---|---|
| `spac` | A SPAC instrument — common, warrant, right, unit, or option | `PROHIBITED_SPAC` (always) |
| `restricted` | On the firm Restricted List | `PROHIBITED_RESTRICTED` (always) |
| `broad_etf` | Broad-based ETF/ETN (index, sector, multi-name, commodity) — incl. leveraged/inverse **index** funds | `EXEMPT_PRECLEARANCE` (list it, never flag missing approval) |
| `single_stock_etf` | ETF/ETN whose exposure is a **single underlying issuer** (levered or not) | routes to DEFAULT (requires a matching approval) |
| `non_reportable` | Excluded from the definition of Reportable Security (see below) | `NON_REPORTABLE` (ignore) |
| `default` | Everything else: common stock, options, debt, IPOs, private placements | requires a matching approval |
| `unknown` | Cannot be confidently classified | `NEEDS_REVIEW` |

Precedence when more than one could apply: `spac` / `restricted` win over everything
(a single-stock ETF on a restricted/SPAC name is prohibited). Then `non_reportable`, then the
ETF buckets, then `default`.

## Restricted / SPAC (checked live, not from this file)
Do the restricted and SPAC determination with the live tools, not a static list:
- `rlst-check(ticker)` — on the firm Restricted List? (also matches warrants/rights/units)
- `spac-details` / SPAC detection — is this issuer a SPAC?
Warrants, rights, units, and options on a SPAC are all `spac`. A single-stock ETF **inherits**
its underlying's status — if the underlying is restricted or a SPAC, the ETF is too.

## Non-reportable security TYPES — Compliance Manual §2 "Reportable Securities" (p. 14)
The Manual defines "Reportable Securities" as "any Security, except" the list below — so these
types are out of scope. Classify as `non_reportable`. Verbatim from p. 14:
- "Direct obligations of the Government of the United States";
- "Bankers' acceptances, bank certificates of deposit, commercial paper and high-quality
  short-term debt instruments, including repurchase agreements";
- "Shares issued by money market funds";
- "Shares issued by open-end investment companies registered under the Investment Company Act of
  1940, other than investment companies advised or underwritten by Meteora or an affiliate"
  (i.e. ordinary open-end mutual funds, unless Meteora-advised);
- "Interests in 529 college savings plans";
- "Digital Assets and Cryptocurrencies, if not held in a brokerage account"; and
- "Shares issued by unit investment trusts that are invested exclusively in one or more open-end
  investment companies ... none of which are advised or underwritten by Meteora or an affiliate."

Note (same section, p. 14): "ETFs and ETNs are Reportable Securities" but "personal transactions
in ETFs and ETNs do not require pre-clearance from the CCO" — that's why broad ETFs are
`broad_etf` (reportable, no pre-clearance), NOT `non_reportable`.

## Out-of-scope TRANSACTIONS/ACCOUNTS — a different basis: Manual §4c (p. 15-16)
These are not security-type exclusions; they are "Exceptions from Reporting Requirements." An
Employee "is not required to submit":
- "Quarterly reports for any transactions effected pursuant to an Automatic Investment Plan"
  (e.g. a DRIP) — also exempt from pre-clearance under §3 (p. 14); and
- "Any reports with respect to Securities held in accounts over which the Employee had no direct
  or indirect influence or control, such as an account managed by an investment adviser on a
  discretionary basis" — only when the certification is on file (roster `exempt_accounts`).
Operationally these are skipped (treated like `non_reportable`), but cite §4c, not §2, for them.

## Broad ETF vs. single-stock ETF — the decisive test
**The test is the UNDERLYING, not the leverage.**
- Tracks an index / sector / basket / commodity: `broad_etf` (exempt). Leverage or inverse is
  fine: `QQQ`, `SPY`, `XLK`, `TQQQ`, `SQQQ`, `SOXL`, `UVXY` are all `broad_etf`.
- Economic exposure to a **single named company**: `single_stock_etf` (needs approval) — e.g. a
  2x/3x single-name fund, a single-stock income (covered-call) fund, or a single-stock inverse
  fund. See `single-stock-etfs.md` for the curated list + issuer heuristic.
- If you cannot tell how many underlyings a fund has: `unknown`.

## Reportable-but-exempt-from-preclearance
Broad ETFs/ETNs are **Reportable** (they belong in the quarterly report and the Excel) but are
**exempt from pre-clearance** (Manual §2, p. 14). So `broad_etf` becomes `EXEMPT_PRECLEARANCE`:
list it, never flag it as a missing approval. This differs from `non_reportable`, which is
dropped entirely.
