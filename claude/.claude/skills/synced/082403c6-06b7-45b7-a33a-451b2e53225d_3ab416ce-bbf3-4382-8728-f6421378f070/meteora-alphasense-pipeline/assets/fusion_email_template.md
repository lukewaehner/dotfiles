# Email template - "Desk memo" HTML (Broker Research only)

The daily run sends **ONE consolidated Broker Research HTML email** containing a **section per sector** (each sector = one Desk-memo card under its own header), with a **single shared footer/legend** at the very bottom (not repeated per section). Include a section **only** for sectors with material new broker research — omit any sector whose synthesis reports no material new broker research, and omit the individual-ticker SPAC watchlist when it has only an off-theme match / no synthesis. (News emails are retired — news is out of scope.) Send as **HTML** (Email Assistant `draft_email`
/ `send_email` with `html=True`) using the Desk-memo templates below. They are **Outlook-safe**: table
layout + inline styles only - no flexbox, no CSS variables, no external/`<style>` CSS, no dark-mode vars.
Keep the palette and structure; swap only the content placeholders (`{{...}}`).

## Locked subject-line template (keep consistent)
`AlphaSense AM - Broker Research - <Mon D>` — ONE consolidated email; each sector is a headed section inside it (TEST prefix `[TEST] `).
e.g. `AlphaSense AM - Broker Research - Jul 15`, with sections: Crypto / Stablecoins, Software / Cyber / Networking, Healthcare / Pharma, ... (empty sectors omitted).

## Cardinal rule: RELAY only - no analysis, no calls/opinions
This is an ingestion tool. Each email carries **AlphaSense's own broker synthesis** (the Agent "Weekdays Update" report) plus the ingestion tally - nothing else. Do **not** cross-reference
against Meteora's memory docs, positions, internal threads, or the VDR; do **not** add a thesis, a
verdict ("confirms / supportive / cheap / high-probability / buy-sell"), or any Meteora-specific
commentary. The report-summary sentences are the *report's* content as AlphaSense stated it - never a
Claude call. If a scope had no material new broker research, say so plainly (that is what the agent
synthesis itself says) and move on.

## Footer legend (fixed - reproduce verbatim in the templates below)
- **flagged** = new docs the alert surfaced in the past 24h (incl. off-scope noise).
- **in-scope** = broker-research docs whose primary ticker/coverage maps to a name in `ingestion_scope.json`, PLUS any Expert-Insight (`EC-`) transcript the alert surfaced (the
  download filter).
- **downloaded** = in-scope broker-research + expert-insight docs saved to the DB.
- **expert insights** = expert-network call transcripts (`EC-` docids) the alert surfaced — wanted primary research, downloaded & archived, never skipped.
- **Archive parent folder:** `C:\Users\rishi\Desktop\Rishi\Projects\Meteora Capital\AlphaSense\BrokerResearch\`
  (files land in `<sector-slug>\<YYYY-MM>\`).
The Broker Research footer carries the full legend + archive path.

## Palette (fixed hexes - warm-gray + one blue accent; do not swap for CSS vars)
ink `#2C2C2A` | body `#2C2C2A` | muted `#888780` | label `#5F5E5A` | hairline `#E9E7E0` |
footer bg `#F7F5EE` | accent rule `#185FA5` | mono = `Consolas,'Courier New',monospace` | sans =
`Arial,Helvetica,sans-serif`.

## BROKER RESEARCH email - HTML (Desk memo)
Placeholders: `{{SCOPE}}` `{{DATE}}` `{{FLAGGED}}` `{{INSCOPE}}` `{{DOWNLOADED}}` `{{REPORTS}}`
`{{LEDGER}}` `{{TESTLINE}}` (TEST mode -> `TEST (self only)`; live -> `Investment Team`).
Each report row is a **2-3 sentence summary of what the report actually said** (NOT a one-line headline),
~40-75 words, taken in substance from the AlphaSense Agent synthesis or the downloaded PDF: sentence 1 =
the report's central thesis; sentence 2 = the issuance / deal implication (offer size, valuation, terms,
cornerstone, IPO-window stats, etc.); optional sentence 3 = a rating/PT change or the report's own
second-order read. Source of the summary: for Agent / GenSearch broker scopes use that firm's **Central
Thesis** + **Implication for Issuance and Dynamics** (+ any **Rating / Target Change**); for a downloaded
deal-terms PDF use the deal terms + the report's own **Conclusion**. RELAY only - the sentences are the
*report's* content, never a Claude call/opinion. Lead with the firm in bold and a short italic topic tag:
`<div style="font-size:13px;line-height:1.6;color:#2C2C2A;padding-bottom:7px;"><b>Firm</b> (analyst) &mdash; <i>topic.</i> Thesis sentence. Issuance/deal-implication sentence with sizes/terms; any rating or PT change.</div>`
Worked example (real, from the 2026-07-02 Macro SPAC / IPO scope):
`<div style="font-size:13px;line-height:1.6;color:#2C2C2A;padding-bottom:7px;"><b>DZT Research</b> (Ke Yan, CFA) &mdash; <i>Guangdong Dtech A+H, deal-terms.</i> PCB drilling-tools maker pricing at HKD 380/sh (~$617M, 12.63M shares; sponsors CITIC/HSBC) with a $254M cornerstone = 41.2% of base. The implied 56% A-H premium sits above the report's own ~30% fair-value view and the ~47% PCB-peer average, and DZT concludes it would participate and expects a positive debut.</div>`
`{{LEDGER}}` = `downloaded: ...<br>expert insights: ...<br>skipped: ...` (plain filenames / short reasons; no commentary; list downloaded broker-research PDFs and expert-insight transcripts, and put only patent/news/off-scope items under skipped).

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;margin:0;padding:0;"><tr><td align="center" style="padding:0;">
<table role="presentation" width="640" cellpadding="0" cellspacing="0" style="width:640px;max-width:640px;font-family:Arial,Helvetica,sans-serif;color:#2C2C2A;">
<tr><td style="height:3px;background:#185FA5;font-size:0;line-height:0;">&nbsp;</td></tr>
<tr><td style="padding:16px 20px 10px 20px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td style="vertical-align:top;"><div style="font-size:11px;color:#888780;">AlphaSense AM &middot; Broker research</div><div style="font-size:17px;font-weight:bold;color:#2C2C2A;padding-top:3px;">{{SCOPE}}</div></td>
<td align="right" style="vertical-align:top;font-family:Consolas,'Courier New',monospace;font-size:12px;color:#888780;white-space:nowrap;">{{DATE}}</td>
</tr></table></td></tr>
<tr><td style="padding:9px 20px;border-top:1px solid #E9E7E0;font-family:Consolas,'Courier New',monospace;font-size:12px;color:#5F5E5A;">{{FLAGGED}} flagged &middot; {{INSCOPE}} in-scope &middot; {{DOWNLOADED}} downloaded to DB</td></tr>
<tr><td style="padding:12px 20px;border-top:1px solid #E9E7E0;"><div style="font-size:12px;font-weight:bold;color:#5F5E5A;padding-bottom:6px;">Broker reports (AlphaSense synthesis)</div>{{REPORTS}}</td></tr>
<tr><td style="padding:12px 20px;border-top:1px solid #E9E7E0;"><div style="font-size:12px;font-weight:bold;color:#5F5E5A;padding-bottom:6px;">Download ledger</div><div style="font-size:12px;line-height:1.6;color:#6f6f6a;font-family:Consolas,'Courier New',mono