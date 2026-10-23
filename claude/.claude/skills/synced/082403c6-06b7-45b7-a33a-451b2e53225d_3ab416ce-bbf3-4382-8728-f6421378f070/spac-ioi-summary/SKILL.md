---
name: spac-ioi-summary
description: 'Produce a tight, IOI-ready evaluation of a brand-new SPAC IPO: unit pricing matrix (offer-price, auto-extension-window first-redemption deadline, 5% ± 0.6% yield grid, overfunded CIT when applicable) + IPO Terms (5 bullets including trust overfunding and excess working capital outside trust), Key Bombs (3 bullets: WC WDLs, prior liquidations, other deviations), Management Team (3 bullets). Trust overfunding (CIT > $10.00) and excess WC outside trust are first-class signals and must be flagged prominently. Trigger on "IOI summary", "run IOI", "IOI eval", "pre-IOI summary", "should we IOI [TICKER]", "IOI on [TICKER]", "give me the IOI", "IOI write-up", or any request for a tight evaluation supporting an IOI decision on a new SPAC IPO. Also trigger proactively after spac-s1-extraction and spac-bios when the user asks for a "summary" or "IOI". Always use this skill for IOI evaluation summaries — the format is locked, reproduce exactly, produce ONLY this output (no preamble, no postamble).'
---

# SPAC IOI Summary — Pre-IOI Evaluation Output

## Overview

This skill produces a compressed, scannable evaluation of a brand-new SPAC IPO designed to support an IOI decision. It combines four blocks:

1. **Unit pricing matrix** (pre-IPO offer price, auto-extension first-redemption deadline, CIT reflects any overfunding)
2. **IPO Terms** (5 bullets: structure, trust + overfunding callout, **excess WC outside trust**, promote/fees, PP)
3. **Key Bombs** (3 bullets: WC WDLs, prior liquidations on team, other deviations)
4. **Management Team** (3 bullets: officers compressed, named ID, remaining IDs)

The format is **LOCKED**. Do not add introductory prose, outro, or extra sections. Output is exactly the four blocks below and nothing else.

This skill expects that S-1 extraction (`spac-s1-extraction`) and team diligence (`spac-bios`) have been run earlier in the conversation. If they haven't, run them first OR pull the equivalent facts from EDGAR / Bloomberg / the uploaded S-1 PDF before producing the IOI output. **Do not produce an IOI summary from S-1 reading alone — the team-diligence layer (prior liquidations, undisclosed network bridges, engineered credentials) is the most consequential input.**

## Required inputs

| Input | Source |
|---|---|
| Ticker | User |
| Unit price | Always **$10.00** (offer price). The point of IOI evaluation is to assess the deal at offer. Do NOT pull a live quote. |
| IPO date | Assumed **today** (current date in system context). Do NOT use a projected post-S-1 date. |
| Max date | **End of the auto-extension window from S-1 Section 2 Timeline.** This is the first guaranteed shareholder redemption opportunity. Compute as: base term + any auto extensions that do NOT trigger a redemption opportunity (BCA-triggered auto, deposit-based auto). Vote-based extensions are NOT included because they always trigger a redemption right at each vote. **Do NOT default to 24mo — pull the actual auto-window length from the S-1 every time.** Do NOT use the 36mo soft cap. Common values: 12mo flat, 12+3=15mo (BCA-auto), 18mo flat, 18+6=24mo (deposit-auto), 24mo flat. AGP-led / Cayman / smaller-cap SPACs frequently use 12+3=15mo — defaulting to 24mo overstates the redemption horizon and understates the implied yield (overpays for the unit). |
| CIT at IPO | **Pull from S-1 every time.** $10.00 is the standard floor; overfunded trusts run $10.025, $10.05, $10.10, $10.15. When CIT > $10.00, this is overfunding (typically funded by a slice of PP proceeds or anchor commitment) — must be flagged prominently in the matrix header AND used in the MaxTrust calc. Overfunding raises the redemption floor and IRR; understating CIT understates the yield. |
| T-Bill | Pull `USGG3M Index` PX_LAST via `MeteoraMCP:get-price`. Fall back to 3.67% if unavailable. |
| Structure ratio | "1/2W" → N=2; "1/3W" → N=3; "1/10R" → N=10. From S-1. |
| Sponsor / management facts | From S-1 extraction earlier in conversation |
| Team SPAC track record | From team diligence earlier in conversation (always include prior liquidations explicitly) |
| Excess WC outside trust | From S-1 Section 5. Aggregate cash available to fund the search outside the trust: (i) IPO proceeds not deposited into trust, (ii) PP proceeds in excess of any trust overfunding deposit, (iii) sponsor working capital loan / promissory note capacity. More excess WC correlates with higher probability of a successful outcome (sponsor can absorb failed deal cycles without mid-search capital raise). Must be highlighted in IPO Terms; light WC must be flagged in Other bombs. |

## Yield matrix computation

Default: base yield 5.0%, step 0.2%, 7 rows (4.4%, 4.6%, 4.8%, 5.0%, 5.2%, 5.4%, 5.6%).

```
MaxTrust = CIT × (1 + r_Tbill)^((MaxDate − IPODate)/365)
ImpliedCommonBid = MaxTrust / (1 + y_target)^((MaxDate − Today)/365)
ImpliedFullW = (UnitPrice − ImpliedCommonBid) × N
```

For pre-IPO IOI (IPO = today, MaxDate = today + N months), both date differences equal the same N-month interval. Compute T = N/12 (years) and use:
```
MaxTrust = $10.00 × (1 + r_Tbill)^T
ImpliedCommonBid = MaxTrust / (1 + y)^T
ImpliedFullW = ($10.00 − ImpliedCommonBid) × N_coverage
```

**N is pulled from the S-1 every time — never hardcoded to 24.** Common N values: 12, 15 (12+3 BCA-auto), 18, 24 (18+6 deposit-auto or flat 24). For OTAIU-style 12+3 BCA-auto, T = 1.25 years and the yield horizon is materially shorter than 24mo.

Always show **4 decimals** on prices. Bold the 5.0% row in the matrix.

## Locked output format

Reproduce this template exactly. All caps placeholders are filled in; everything else is verbatim.

```
**[TICKER]** — Unit $10.00 (offer, pre-IPO), IPO M/D/YY (assumed today), [STRUCTURE_RATIO], Max date M/D/YY ([N]mo), **CIT $XX.XXXX** [if > $10.00: append "**(OVERFUNDED +$0.0XX/share)**"], T-Bill X.XX%

| Yield | Implied Common | Implied [W or R] |
|------:|---------------:|-----------------:|
| 4.4%  | $X.XXXX        | $X.XXXX          |
| 4.6%  | $X.XXXX        | $X.XXXX          |
| 4.8%  | $X.XXXX        | $X.XXXX          |
| **5.0%** | **$X.XXXX**     | **$X.XXXX**      |
| 5.2%  | $X.XXXX        | $X.XXXX          |
| 5.4%  | $X.XXXX        | $X.XXXX          |
| 5.6%  | $X.XXXX        | $X.XXXX          |

MaxTrust at deadline: $X.XXXX

At 5% target yield, you're paying ~$0.XX per whole [warrant/right] by buying the unit at $10.00.

---

**IPO Terms**
- **Structure:** $XXXM / XXM units @ $10 / [UNIT_COMPOSITION] / [UNIT_TICKER] / [EXCHANGE] / [DOMICILE] / [N]mo to redemption ([EXTENSION_TYPE: e.g., 12mo + 3mo BCA-auto, 18mo + 6mo deposit-auto, 24mo flat with vote-based only]) / [UW_NAME] [sole bookrunner / co-managers] / 15% OA.
- **Trust:** $XX.XX/share full trust [if > $10.00: append " — **OVERFUNDED +$0.0XX/share = $X.XM above the $10.00 floor, funded by [SOURCE: e.g., $0.025/unit slice of PP proceeds]**"], [TRUSTEE] trustee, [TRUST_INVESTMENT]. 15% redemption cap.
- **Excess WC:** $X.XM aggregate outside trust — $X.XM from PP excess / $X.XM from IPO retention / $X.XM sponsor loan facility ([CONVERSION_MECHANIC if any, e.g., "convertible to PPW @ $1.00 at IBC"]). [Qualitative read: **deep / adequate / light, likely needs mid-search raise**]. [If light: note the implication — sponsor likely to raise external capital mid-search, compromising deal terms.]
- **Promote/fees:** XX% promote ($0.00X basis). UW X.X% (X.X% upfront / X.X% deferred, [DEFERRED_MECHANIC]). $XXK/mo admin. [BCMA_STATUS].
- **PP:** $XM PPW @ $X.XX — $XM sponsor / $XM underwriters; [PPW_FUNDING_MECHANIC].

**Key Bombs**
- **WC WDLs — [CLEAN or NON-STANDARD detail].** [PERMITTED_WITHDRAWAL_LANGUAGE]. [EXTENSION_MECHANICS].
- **Liquidation on team:** [Any team member's prior liquidation OR "None on team record"]. Team SPAC record: [N successes with current trading levels] + [N liquidations].
- **Other:** Numbered list — (1) ... (2) ... (3) ... (4) ... — covering: undisclosed network bridges (especially Audit Chair conflicts), absence of anchor/FPA/PIPE, sponsor structure flags, engineered credentials, just-in-time board appointments, off-thesis sector inclusions, **light excess WC outside trust (flag if sponsor likely needs mid-search raise)**.

**Management Team**
- **Officers:** **[EXEC_CHAIR/SPONSOR_MGR_NAME]** ([role]) — [career one-liner]. [Exit count + Forbes status]. [Most relevant prior credential]. [Concurrent SPAC roles if any]. **[CEO_NAME]** (CEO) — [career one-liner]. [Most relevant tenure + Bloomberg-confirmed performance]. [Current role]. **[CFO_NAME]** (CFO) — [career one-liner]. [Engineered credential flag if applicable].
- **[FIRST_NAMED_ID] (ID):** [Background one-liner] — [Prior SPAC roles + outcomes]. [Committee role]. [Network value descriptor].
- **[REMAINING_IDS_COMBINED]:** **[ID_2]** ([committee role]) — [tenure with quantified performance]. [Network bridge flag if applicable]. **[ID_3]** — [career one-liner]. [Prior SPAC outcomes including any liquidations].
```

## Style rules

- **Single output, no preamble, no postamble.** No "Here's the IOI summary…" intro. No "Let me know if you want…" outro. Just the four blocks.
- **Use em-dash separators** (—) within bullets, not multiple commas.
- **Bold lead-in fragments** so each bullet is scannable.
- **Compressed sentences.** Drop articles where possible. Use SPAC-arb shorthand (UW, PPW, IBC, deSPAC, OA, BCMA, MCC, FPA, GDG, PP).
- **Always include the 5% one-line context** below the matrix: "At 5% target yield, you're paying ~$0.XX per whole warrant by buying the unit at $10.00." (Substitute "right" if rights deal.)
- **Always mark WC WDLs explicitly** as "CLEAN" or specify the non-standard feature. The CLEAN finding is the answer the reader is looking for; do not bury it.
- **Always quantify post-deSPAC performance** for any team member's prior deSPAC (e.g., "BULL -27% post-deal").
- **Always flag undisclosed network bridges** in Other bombs if surfaced in the team diligence — these are the highest-impact diligence flags.
- **Always note Forbes status** for the Exec Chair / sponsor manager when relevant ("not on Forbes" if applicable).
- **Always render as markdown** with bullet lists and bold; the matrix is a markdown table with right-aligned numeric columns.
- **Trust overfunding (CIT > $10.00) must be flagged aggressively.** Append "**(OVERFUNDED +$0.0XX/share)**" in bold to the matrix-header CIT field, AND repeat the callout in the Trust IPO-Terms bullet with the aggregate dollar excess and the funding source quoted explicitly. Never bury overfunding in a phrase like "$10.025 trust" — it must read as a structural feature, not a typo.
- **Excess WC outside trust is a first-class bullet, not a footnote.** Always populate the dedicated "Excess WC:" bullet with the aggregate dollar figure, the component breakdown (PP excess / IPO retention / sponsor loan capacity), the conversion mechanic on the sponsor loan, and a qualitative read (deep / adequate / light). If light, flag the mid-search-raise risk in Other bombs as well.

## Edge cases

- **Auto-extension window shorter than 24mo (e.g., 12mo base + 3mo BCA-triggered auto = 15mo)**: The end of the auto window IS the first shareholder redemption opportunity, because beyond the auto window any further extension is vote-based and triggers a redemption right. Use the 15mo (or whatever the actual auto window is) as Max Date — **do NOT default to 24mo**. This is the common pattern for AGP-led / Cayman / smaller-cap SPACs and any deal where the sponsor has a tight base term plus a BCA-announcement auto-bump. Defaulting to 24mo on a 15mo SPAC will overstate Max Trust by ~3% and understate implied right cost by ~50% at the 5% line — the unit will look much cheaper than it actually is. Always pull the timeline from S-1 Section 2 before computing.
- **Rights deal** (e.g., 1/10R): replace "Implied W" column with "Implied R", change multiplier N to the right ratio denominator, change the one-line context to "per right". Update the structure note in the matrix header.
- **Combo unit (1W + 1/4R, etc.)**: the multiplier collapses to N=1 since W and R can't be separated. Show "Implied W+R" combined cost. Flag in matrix header.
- **Unit has no embedded W/R (clean common-only)**: drop the "Implied W" column entirely. Note in the one-line context that there is no embedded optionality.
- **No anchor / FPA / PIPE indication**: explicitly mention in Other bombs. This is the operative test for institutional capital-raise capability.
- **Tier-1 sponsor or anchor present**: soften the "first-time sponsor" framing if applicable. Do not manufacture bombs that aren't there.
- **Multiple IDs with prior liquidations**: call all of them out in the Liquidation bullet.
- **Team has zero prior SPAC experience**: note in the Liquidation bullet ("Team SPAC record: zero prior SPAC roles on team").
- **Stated sectors include digital assets / crypto treasuries with no team domain expertise**: flag in Other bombs as DAT optionality.
- **Just-in-time credentials** (board appointments within 30 days of S-1 filing): flag in Other bombs as credential burnishing.
- **CIT > $10.00 (overfunded trust — $10.025, $10.05, $10.10, $10.15)**: Use the overfunded value in the MaxTrust calc, and flag aggressively in BOTH the matrix header (append "**(OVERFUNDED +$0.0XX/share)**" to CIT) AND the Trust IPO-Terms bullet (state per-share excess, aggregate dollars above $10.00, and the funding source — typically a $0.0XX/unit slice of PP proceeds, or an anchor top-up). Overfunding directly raises the redemption floor and IRR; understating CIT understates the yield. This is not a footnote — it is a structurally positive feature of the deal and must be the first thing the reader notices after the ticker.
- **Light excess WC outside trust**: When aggregate WC outside trust (PP excess + IPO retention + sponsor loan capacity) is materially below peer norms, flag in the Excess WC bullet with the qualitative tag "**light, likely needs mid-search raise**" AND add a numbered item to Other bombs framing the mid-search-raise risk and the typical consequence (compromised deal terms when sponsors raise on the fly).

## Worked example (KEYY — Keystone Acquisition Corp., S-1 filed 5/4/26)

**KEYY** — Unit $10.00 (offer, pre-IPO), IPO 5/5/26 (assumed today), 1/2W, Max date 5/5/28 (24mo), CIT $10.00, T-Bill 3.68%

| Yield | Implied Common | Implied W |
|------:|---------------:|----------:|
| 4.4%  | $9.8632        | $0.2737   |
| 4.6%  | $9.8255        | $0.3491   |
| 4.8%  | $9.7880        | $0.4239   |
| **5.0%** | **$9.7508** | **$0.4985** |
| 5.2%  | $9.7138        | $0.5725   |
| 5.4%  | $9.6770        | $0.6461   |
| 5.6%  | $9.6403        | $0.7193   |

MaxTrust at deadline: $10.7503

At 5% target yield, you're paying ~$0.50 per whole warrant by buying the unit at $10.00.

---

**IPO Terms**
- **Structure:** $250M / 25M units @ $10 / 1 share + ½ warrant / KEYYU / Nasdaq GM / Cayman / 24mo to redemption (vote-based extensions only) / Cohen & Co. **sole bookrunner** / 15% OA.
- **Trust:** $10.00/share full trust, Efficiency Inc. trustee, T-bills ≤185d / 2a-7 MMF / demand deposit. 15% redemption cap.
- **Excess WC:** $2.8M aggregate outside trust — $2.0M from PP proceeds in excess of UW PPW funding / $0.3M from IPO retention after offering expenses / $1.5M sponsor loan facility (convertible to PPW @ $1.00 at IBC). **Adequate** — sufficient for ~1.5 deal cycles before a sponsor top-up would be required; no anchor or FPA backstop to cushion a failed first attempt.
- **Promote/fees:** 25% promote ($0.003 basis). UW 6.0% (2.0% upfront / 4.0% deferred, deferred paid only on remaining trust post-redemption). $20K/mo admin. No BCMA.
- **PP:** $7M PPW @ $1.00 — $4.5M sponsor / $2.5M underwriters; UW PPW funded by recycled $0.10/unit upfront fee (zero net UW cash).

**Key Bombs**
- **WC WDLs — CLEAN.** Taxes (ex-Excise) + $100K liquidation only. No annual interest cap, no rollover, no auto/deposit extensions.
- **Liquidation on team:** **Payne (ID) was director of HCAR — $330M Dec 2020 IPO, liquidated Dec 22, 2022 at $10.11.** Team SPAC record: 1 success (SKGR→BULL, Chin/Boehner/Payne; BULL **-27%** post-deal) + 1 liquidation.
- **Other:** (1) **Paul Cho (Audit Chair) was direct co-employee of Chin (CEO) at SK hynix N.A. 2016-2019 — undisclosed in S-1; compromises conflict-screening for any SK-group IBC** (the realistic target). (2) No anchor / no FPA / no PIPE on $250M trust. (3) First-time sponsor; 36% of sponsor economics held by undisclosed passive members. (4) Park appointed to IPCX board April 24 — 10 days before this S-1 (credential burnishing).

**Management Team**
- **Officers:** **Park** (Exec Chair, sponsor mgr) — KPMG Seoul → Nexgen Singapore IB → indep. consultant. Zero principal exits, no fund, not on Forbes. USAR East Asia ops 2021-Dec 2025 (USAR +174% post-deSPAC, ops role only). Concurrent IPCX audit cmte. **Chin** (CEO) — SK group lifer: SK telecom Americas → SK hynix President GDG 2017-21 (hynix +186% during tenure) → SKGR CEO → BULL deSPAC. Now Co-CEO of Solidigm Inc. (SK hynix AI Co. spinout, formed Jan 2026). **Cho** (CFO) — Korean attorney/S&P/SK hynix America VP CorpDev → CEO of AgaMatrix ($20M-purchase-price i-SENS sub — engineered credential).
- **Boehner (ID):** 53rd House Speaker, Squire Patton Boggs policy advisor, Titan Mining director. SKGR director (BULL deSPAC). Comp Cmte chair. Policy/CFIUS access; not a check-writer.
- **Paul Cho & Payne (IDs):** **Paul Cho** (Audit Chair) — UCTT GC since Oct 2019 (+485% during tenure, AI/semi tailwind), prior SK hynix N.A. GC 2014-2019 (the undisclosed Chin overlap). First public board. **Payne** — multi-board healthcare-services CEO. SKGR director (BULL deSPAC) AND **HCAR director (liquidated Dec 2022)**.

## What this skill replaces

This replaces the ad-hoc "should we IOI" question with a locked-format synthesis. It assumes the underlying S-1 extraction and team diligence work has been done. The skill is a synthesis layer, not a research layer — the depth of the underlying diligence (especially Bloomberg-confirmed team performance and undisclosed network bridges) determines the quality of the output.

Always use this skill for IOI evaluation summaries. Do not produce ad-hoc IOI write-ups in a different format — consistency across deals is the point.
