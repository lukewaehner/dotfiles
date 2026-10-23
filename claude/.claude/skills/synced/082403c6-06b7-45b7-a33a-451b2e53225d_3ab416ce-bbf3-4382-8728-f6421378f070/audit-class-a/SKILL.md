---
name: audit-class-a
description: >-
  Reconstruct a SPAC's true Class A ordinary shares outstanding from primary SEC
  filings, to verify 13G/13D ownership percentages and 5% / 9.9% / 10% threshold
  checks. Use whenever the user wants to audit, verify, or rebuild a SPAC's share
  count / shares outstanding / Class A float, questions a 13G denominator, asks
  whether a position crosses 5/9.9/10%, or asks why two share counts disagree
  (Bloomberg EQY_SH_OUT vs the master sheet vs a 13G workpaper). Also triggers on
  "audit class A", "walk the redemptions", "rebuild the cap count from filings".
  Walks the IPO 424B baseline through every extension redemption, founder conversion,
  and going-dark event; outputs a filing-linked timeline table plus a total-vs-float
  reconciliation and threshold flag. Always use this for SPAC share-count / threshold
  verification — don't eyeball it off a stale cover page or a data vendor.
---

# Audit Class A — SPAC share-count reconstruction

## What this does, and why it matters

Rebuild the real number of **Class A ordinary shares outstanding** for a SPAC, event by event, from the filings that actually move it. The point is compliance-grade confidence in a denominator: our 13G/13D percentage, and every 5% / 9.9% / 10% threshold test, is only as good as the share count under it. When a position sits near a filing threshold, a wrong denominator is a missed (or spurious) filing.

Two numbers get quoted for "shares outstanding," and they are usually **both correct** — they just mean different things:

- **Total Class A outstanding** = public shares **plus** any founder/sponsor shares that converted into Class A. This is the correct denominator for a 13G/13D percentage.
- **Public float** = total **minus** the sponsor/founder block. This is what a trader watches.

They differ by exactly the sponsor/founder block. Vendors and internal sheets often store one while a workpaper uses the other, which is why "10.65M vs 2.03M" arguments happen. This skill produces **both**, shows the bridge between them, and ties out to the filings.

Do not trust a single source for the count:
- **Cover pages go stale.** Issuers routinely carry the old registered share count on a 10-K/10-Q cover for weeks after a redemption. A cover dated a month after a big redemption can still show the pre-redemption number.
- **Data vendors blend or lag.** Bloomberg `EQY_SH_OUT` can mix share classes and lags going-dark (delisted/OTC) names badly.
- **The master sheet can be internally inconsistent** — e.g., `common_outstanding` holding the *float* while `pct_9_outstanding` is computed off the *total*.

The filings are the ground truth. Rebuild from them.

## Inputs

- The SPAC — any ticker (common, unit, or warrant) or company name. Everything keys off the **EDGAR CIK**.
- Our position and the sheet's figures from `spac-details`: `common_position`, `common_outstanding`, `pct_9_outstanding`. Pull these first so you can reconcile at the end.

## Workflow

### 1. Anchor on the CIK, never the ticker or name

Tickers migrate and issuers rename mid-life. A SPAC that delists to OTC picks up an "F" ticker (e.g. `IVCB → IVCBF`), and a sponsor handover often comes with a name change (e.g. "Investcorp Europe Acquisition Corp I" → "Invest Acquisition Corporation"). The **CIK is the only stable key**.

- Try `edgar-filings` with the ticker. If it won't resolve (common for delisted/OTC names), find the CIK with `edgar-ownership-search` (full-text the company name — our own 13G on the name will surface the CIK) or from a known 13G workpaper.
- Pull `spac-details` for our position + the sheet numbers.

### 2. Establish the IPO baseline (and confirm the over-allotment)

Read the IPO prospectus (`424B4` / `424B3`) for the offering structure, but **do not take the "as adjusted, assuming no exercise of the over-allotment" capitalization table as your baseline** — the over-allotment is frequently exercised, which changes both the Class A and Class B counts. Confirm the real post-IPO count from the **first 10-K cover page**: "As of [date], there were **X** Class A ordinary shares … and **Y** Class B … issued and outstanding." That **X** is your starting Class A.

### 3. Pull the full filing history — this also generates your links

Call `edgar-filings` with the **CIK**, a wide `filing_date` range (IPO year through today), `limit` 100 (paginate by date if needed). Every row carries a `document_url`. **Capture those URLs** — they become the `Source` links in the output table. Order everything chronologically.

### 4. Walk the extension redemptions — the spine of the reconstruction

Extension votes are where Class A actually moves. For each extension, open the **results 8-K** and read **Item 5.03 / 5.07** and, critically, the **"Redemptions"** paragraph:

> "In connection with the vote … the holders of **N** Class A ordinary shares properly exercised their rights to redeem their shares for cash …"

Subtract **N** from the running Class A balance. These 8-Ks are the load-bearing filings; the redemption number is the signal.

**Skip the noise.** These never move the count and will drown you if you read them: `425` (merger comms — often dozens), other filers' `SC 13D/13G`, `Form 3/4/5`, `NT 10-K/NT 10-Q`, `CORRESP`, `UPLOAD`, `EFFECT`, `CERT`, `8-A`, `DEFA14A` soliciting material. Vik's instinct is right: skip everything until you hit an extension, then micro-manage each redemption filing.

### 5. Catch the five things that break a naive walk

These are the reasons an ad-hoc count is usually wrong. Each has a tell:

1. **Founder Class B → Class A conversion.** Founders often convert their Class B (1:1) into Class A partway through, leaving a single vestigial Class B share. This dumps **millions** of shares into the Class A denominator at once. *Tell:* an annual-report cover that suddenly reads "**X** Class A and **1** Class B," or a conversion 8-K. Add the converted shares to your Class A running balance — they are Class A now and count in the 13G denominator.
2. **Record-date vs post-redemption.** An extension 8-K's *header* states the **record-date** count (pre-redemption); the actual redemption is in the **Redemptions paragraph later in the same filing**. Apply the redemption — never stop at the header number.
3. **Stale cover pages.** Do not trust a 10-K/10-Q cover "issued and outstanding" that post-dates a redemption by only a few weeks. When a cover and a redemption 8-K disagree, the **8-K wins**.
4. **Going dark / delisting.** After a Nasdaq delisting (`25-NSE`), the issuer stops filing `10-Q`/`10-K`. Past that point the **only** truth is in `8-K`s and `DEF 14A / DEF 14C`. A periodic-report-only approach silently freezes at the last 10-Q — you must switch to 8-Ks.
5. **14(c) written-consent extensions.** Once any holder (often us, post-handover) controls >50%, extensions run through a **Section 14(c) information statement** with no shareholder vote. But public holders **still** get redemption rights. "No proxy" ≠ "no redemption" — find the redemption figure in the 8-K.

### 6. Reconcile and flag

- **Total Class A outstanding** = your reconstructed running balance (+1 Class B if it survives).
- **Public float** = total − sponsor/founder block (the converted founder shares + any shares a sponsor/affiliate holds).
- **Our %** = `common_position` ÷ total Class A. Flag against **5% / 9.9% / 10%**. If an affiliate of ours (e.g. the sponsor post-handover) holds more Class A, note the aggregated beneficial-ownership picture separately — that can be a 13D/control position rather than a threshold-monitoring one.
- **Sheet check:** does `common_outstanding` equal your **total** or your **float**? Does `pct_9_outstanding` equal `0.099 × your total`? Call out any staleness (e.g., a recent small redemption the sheet or vendor hasn't picked up).

## Output format

Lead with the **filing-linked timeline table**, then the **reconciliation block**. Reproduce this structure exactly (the `Source` column must contain a markdown link to the specific filing that evidences each row):

---

### [TICKER] — Class A reconstruction (CIK [number])

| Date | Event | Δ Class A | Public float | Sponsor block | Total Class A o/s | Source |
|---|---|---|---|---|---|---|
| 2021-12 | IPO — full over-allotment | +34,500,000 | 34,500,000 | — | 34,500,000 | [424B4](https://www.sec.gov/…) · [10-K](https://www.sec.gov/…) |
| 2023-03-14 | Ext 1 EGM →12/17/23: 15,494,333 redeemed @ $10.43 | −15,494,333 | 19,005,667 | — | 19,005,667 | [8-K](https://www.sec.gov/…) |
| … | … | … | … | … | … | … |

**Reconciliation**

- **Current total Class A:** N (+1 Class B) — [source]
- **Public float:** N
- **Our position:** `common_position` = P% of total → **UNDER / OVER 5% · 9.9% · 10%**
- **Sheet check:** `common_outstanding` = … → equals the *float* / *total* / stale by … ; `pct_9_outstanding` = … → = 9.9% of *total* (✓/✗)
- **Notes:** any affiliate/control aggregation, any figure that is *derived* (bridged between two anchors) rather than read directly — say which.

---

Cite **every redemption to its own 8-K**. If a figure is derived by bridging two verified anchors (e.g. you inferred a redemption from the before/after covers rather than reading its results 8-K), label it as derived so the audit trail is honest.

## Reference

`references/ivcb-worked-example.md` is a full, verified gold-standard run on **IVCB — Invest Acquisition Corporation (fka Investcorp Europe Acquisition Corp I), CIK 1857410** — the hardest case in the book: five extensions, a founder Class B→A conversion, a sponsor handover, a Nasdaq delisting, and the exact `10,650,520` (total) vs `2,025,520` (float) reconciliation. Read it when you want a worked template, a set of real filing URLs to pattern-match against, or when you hit a wrinkle and want to see how it was resolved.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    