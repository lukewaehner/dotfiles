# Gold-standard worked example — IVCB (CIK 1857410)

**Invest Acquisition Corporation** (f.k.a. **Investcorp Europe Acquisition Corp I**). Cayman Islands, **domestic filer** (10-K/10-Q/8-K, not 20-F/6-K). IPO 12/15/2021, current business-combination deadline **12/17/2027**.

This is the hardest case in the book and exercises every trap: five extensions, a founder Class B→A conversion, a sponsor handover to a Meteora affiliate, a Nasdaq delisting to OTC, two ticker/name changes, and two "conflicting" vendor share counts that are both correct. Use it as a template and a sanity check for the workflow.

Identifier drift (why you must key on CIK):
- Nasdaq: `IVCB` / `IVCBU` / `IVCBW` → OTC: `IVCBF` / `IVCUF` / `IVCWF`
- Name: "Investcorp Europe Acquisition Corp I" → "Invest Acquisition Corporation" (approved 12/12/2025)
- CIK **1857410** never changes.

## Verified timeline

| Date | Event | Δ Class A | Public float | Sponsor block (conv. founder) | Total Class A o/s | Source |
|---|---|---|---|---|---|---|
| 2021-12 | IPO — full over-allotment (34.5M units); 8,625,000 Class B founder | +34,500,000 | 34,500,000 | — | 34,500,000 | [424B4](https://www.sec.gov/Archives/edgar/data/1857410/000119312521359613/d171893d424b4.htm) · [FY21 10-K](https://www.sec.gov/Archives/edgar/data/1857410/000119312522093813/d282218d10k.htm) |
| 2023-03-14 | Ext 1 EGM → 12/17/23; **15,494,333** redeemed @ $10.43 ($161.6M) | −15,494,333 | 19,005,667 | — | 19,005,667 | [8-K](https://www.sec.gov/Archives/edgar/data/1857410/000119312523074128/d460637d8k.htm) |
| 2023-12-05 | Ext 2 EGM → 6/17/24; **7,460,372** redeemed @ $10.9972 ($82.0M) | −7,460,372 | 11,545,295 | — | 11,545,295 | [results 8-K](https://www.sec.gov/Archives/edgar/data/1857410/000119312523290774/d621625d8k.htm) · [prelim 8-K](https://www.sec.gov/Archives/edgar/data/1857410/000119312523288017/d545431d8k.htm) |
| ~2024-Q1 | **Founder Class B→A conversion**: 8,624,999 Class B → Class A (1 Class B left) | +8,624,999 | 11,545,295 | 8,624,999 | 20,170,294 | [FY23 10-K cover](https://www.sec.gov/Archives/edgar/data/1857410/000119312524093395/d172732d10k.htm) |
| 2024-05-21 | Ext 3 EGM → 12/17/24; **2,159,610** redeemed @ $11.31 ($24.4M) | −2,159,610 | 9,385,685 | 8,624,999 | 18,010,684 | [8-K](https://www.sec.gov/Archives/edgar/data/1857410/000119312524144892/d665136d8k.htm) |
| 2024-12-17 | Ext 4 EGM → 12/17/25; **7,360,165** redeemed | −7,360,165 | 2,025,520 | 8,624,999 | **10,650,519** | [results 8-K](https://www.sec.gov/Archives/edgar/data/1857410/000119312524284326/d922688d8k.htm) |
| 2024-12-23 | **Sponsor Handover**: Samara Special Opportunities (Vik Mittal, sole director) buys 6,037,499 Class A + 1 Class B + 11.69M PP warrants for $1; Vik → CEO/CFO/Chair. Nasdaq delist notice → OTC | 0 | 2,025,520 | 8,624,999 | 10,650,519 | [Purchase Agr. 8-K](https://www.sec.gov/Archives/edgar/data/1857410/000119312524279197/d650538d8k.htm) · [handover 8-K](https://www.sec.gov/Archives/edgar/data/1857410/000119312524284326/d922688d8k.htm) |
| 2025-05-22 | Form 25-NSE — Nasdaq delisting effective (already trading OTC) | 0 | 2,025,520 | 8,624,999 | 10,650,519 | [25-NSE](https://www.sec.gov/Archives/edgar/data/1857410/000135445725000445/xslF25X02/primary_doc.xml) |
| 2025-12-12 | Ext 5 EGM → **12/17/27**, name → "Invest Acquisition Corp"; **18,226** redeemed (deadline 12/10/25) | −18,226 | 2,007,294 | 8,624,999 | **10,632,293** | [DEF 14C](https://www.sec.gov/Archives/edgar/data/1857410/000182912625009436/investcorpeuropeacq_def14c.htm) · [8-K](https://www.sec.gov/Archives/edgar/data/1857410/000182912625010061/investacqcorp_8k.htm) |
| 2026-01-14 | Auditor change (Marcum) — **no share impact** | 0 | 2,007,294 | 8,624,999 | 10,632,293 | [8-K](https://www.sec.gov/Archives/edgar/data/1857410/000182912626001937/investcorpalacq_8k.htm) |
| 2026-02-17 | Schedule 13D filed — **no share impact** | 0 | 2,007,294 | 8,624,999 | 10,632,293 | [SC 13D](https://www.sec.gov/Archives/edgar/data/1857410/000190510626000058/xslSCHEDULE_13D_X01/primary_doc.xml) |

**Current (as of 2026-07): 10,632,293 Class A + 1 Class B = 10,632,294 total ordinary.**

## The reconciliation (the whole point)

The two "conflicting" numbers are both right and differ by **exactly 8,625,000** (the founder/sponsor block):

- **10,650,520** = Bloomberg `EQY_SH_OUT` / Brandon's 3/31/26 13G workpaper = **total** ordinary shares (10,650,519 Class A + 1 Class B) at the **post-Ext-4** state. Confirmed verbatim by the Dec-2025 8-K: *"As of November 23, 2025 … 10,650,520 ordinary shares … consisting of 10,650,519 Class A ordinary shares and one Class B ordinary share."*
- **2,025,520** = master-sheet `common_outstanding` = **public float only** (total minus the 8,624,999 converted founder shares).
- Both are **stale by 18,226** — the Dec-2025 redemption. Corrected: **10,632,293 total**, **2,007,294 float**.

**Threshold math (correct denominator = total Class A):**
- Fund `common_position` 2,000,000 ÷ 10,632,293 = **18.8%** (ties to the 13G's 18.78% off 10,650,520). **OVER 10%.**
- Sheet `pct_9_outstanding` = 1,054,401 = 9.9% × 10,650,519 → correctly uses the **total**, but is stale (current 9.9% = 1,052,597). The sheet is internally inconsistent: threshold off *total*, `common_outstanding` shows the *float*.
- Meteora aggregate (fund 2,000,000 + Samara/affiliate 6,037,499) ÷ 10,632,293 ≈ **~76%** — a **13D control position**, matching the handover 8-K's "~75.6%" statement. IVCB is a control name, not a 9.9%-line name.

## Trap sightings in this name (for pattern-matching)

- **Stale cover:** the FY2022 10-K cover ([link](https://www.sec.gov/Archives/edgar/data/1857410/000119312523112915/d483124d10k.htm)) states **34,500,000 Class A as of 4/24/2023** — a *month after* 15,494,333 were redeemed (3/14/23). The cover is wrong; the Ext-1 8-K is right.
- **Founder conversion:** FY2023 cover reads "20,170,294 Class A and **1** Class B" — that single Class B is the tell that 8,624,999 founder shares converted into the Class A denominator.
- **Record-date vs post-redemption:** the Dec-2025 8-K header says 10,650,519 Class A (record date 11/23/25); the Redemptions paragraph in the same filing removes 18,226 → true 10,632,293.
- **Going dark:** last periodic report is the Q3-2024 10-Q (filed 11/25/24, [link](https://www.sec.gov/Archives/edgar/data/1857410/000119312524264506/d793831d10q.htm)). After the delisting there are none — Ext 4 and Ext 5 exist only as 8-Ks / DEF 14C.
- **14(c) consent:** Ext 5 (Dec 2025) ran via a Section 14(c) information statement (Meteora controls ~99% of the vote) yet still triggered 18,226 of public redemptions.

## Which filings carried the signal (trim guide)

Read: the **extension results 8-Ks** (Item 5.03/5.07 → "Redemptions") — one number each; the **first 10-K cover** (over-allotment baseline); **annual-report covers** (to catch the founder conversion); the **handover 8-K** (control change). Everything else here — the many 425s, other filers' 13G/D, Form 4s, NT/CORRESP/UPLOAD/EFFECT/CERT/8-A, DEFA14A — was noise for the share count.
