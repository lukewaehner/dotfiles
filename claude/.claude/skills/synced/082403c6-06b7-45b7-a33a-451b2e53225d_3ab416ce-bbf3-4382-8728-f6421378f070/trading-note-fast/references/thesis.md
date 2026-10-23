# Distilling the doc-sourced fields (the one judgment step)

Everything here feeds `render_note.py` as plain strings/numbers. Source is the
Executive Summary returned by `read-memory-doc(name, summary_only=true)` — the
SAME single fetch for all four fields. No second call, no EDGAR, no S-1 re-read.

---

## Thesis (3–4 sentences)

### Guardrail (non-negotiable)
The thesis is sourced **EXCLUSIVELY** from the memory-doc Executive Summary.
**Forbidden sources** — never use, even paraphrased: `spac_details.notes`,
`spac_details.recommendation`, `spac_details.s4_amendments`, the header/matrix/
ORDERS data itself, web/EDGAR/first-principles, or prior conversation that
isn't a memory-doc read this session. If the only way to write a substantive
thesis is a forbidden source, render the "no doc" fallback instead — the
absence of a doc IS the signal.

### Three cases
- **Doc exists** → distill 3–4 sentences with the stage framework below.
- **No doc** (`status: not_found`) → `thesis = "No memory doc exists for [TICKER]."`
- **Fetch error** → `thesis = "Memory doc fetch failed — retry or check manually."`

### Pre-deal framework (drop any bullet the doc doesn't speak to)
1. **Sponsor franchise read** — prior-vehicle outcome, PIPE quality (the *names*),
   UW signal, first-timer "no track record" prior.
2. **Structural takeaway** — what unit economics / fee load / sponsor dollars
   *imply* (not "1/2 warrant + 1/10 right").
3. **Mandate / pipeline credibility** — real network in the stated focus vs.
   boilerplate (named advisors, banker movement, specialist hires).
4. **Current Meteora posture** — what we're doing and the exact price/trigger.

### In-deal framework
1. **Closing-probability read** — MCC status, PIPE structure/quality, CoC/debt.
2. **Sponsor-incentive read** — deferred UW math, WCW draws, founder forfeit,
   shell-purchase economics → the playbook they'll actually run.
3. **Process / timeline read** — S-4/F-4 cadence, SEC posture, deadline gap,
   gating items; flag extension/termination risk where load-bearing.
4. **Current Meteora posture** — long for yield-to-vote/close, working W/R at a
   level, FPA, redeem-at-vote, sell-rights-into-pop — exact price AND trigger.

### Distillation rules
- Bullets are signposts, not slots — 3 sentences if the doc speaks to 3.
- Mirror exact thresholds from the doc ("$10.75 × 200K GTC bid", "60c wake-up sell").
- Specificity test: if the sentence could appear in another SPAC's note, it's too generic.
- No verbatim Executive-Summary paragraphs; distill into active voice.
- Mirror the doc's hedging — don't manufacture confidence.
- Tone: Walter-facing colleague who read the doc this morning. Terse, concrete,
  directional. No headings/bullets/bold inside the line.

### Worked examples
**Pre-deal (ALUB):** *Repeat Alussa franchise — ALUS I closed FREYR with a $600M
PIPE from Koch / Glencore / Fidelity blue-chip names, proving real PIPE-raising;
post-close failure was target execution, not sponsor capability. Slorer
(ex-Morgan Stanley energy MD, ex-BTIG energy IB head) joined as CEO to source
through his sell-side network; UW BTIG→Santander signals a move upmarket for PIPE
origination. Long 683K commons ~18c below trust for a yield floor plus 10K
warrants — cheap at 30–35c if the pipeline is real, bleed to zero if sitting on
trust income.*

**In-deal (SIMA):** *Dominari paid $8mm for the shell plus a committed 1.5%
deferred UW fee — too expensive to be speculative, implying a target is lined up.
Sponsor runs a serial extension-postponement playbook (no trust contribution, no
new redemption window) until announcement; base case June–July 2026 before the
7/11/26 hard liq. Long 1,683 commons via $10.75 × 200K GTC for a redemption-yield
floor (~3.7%) plus deal-pop optionality; 200K SIMAW @ ~23c scaling to ~300K via
$0.23 × 100K GTC; don't pay above trust on commons or 26c on warrants, wake-up
sell at 60c.*

### Bad thesis sentences (why)
- "The company is a SPAC with a BCA." (generic)
- "Rights-only structure means dilution-on-close is direct." (restates header)
- "First-time sponsor with generic mandate → banker-shopped." (fails specificity test)
- "Sheet flagged 'Bad deals, Cantor UW'; rec C 10.41." (forbidden `notes`/`recommendation`)

---

## Non-Managing Members (one clause)

Sponsors are usually an LLC with a **managing member** (named principal, control)
plus passive **non-managing members** (accredited backers funding part of the
promote, holding founder shares / PP warrants indirectly, no control). The split
tells us how much promote is the principal's own at-risk capital vs. farmed out.

Extract from the summary (drop what isn't there): managing-member identity; the
non-managing economics — quantified pass-through if the doc carries it (e.g.
`3,398,916 founder shares + 1,246,839 PP warrants`), else the qualitative
disclosure; character (passive promote-funding / strategic / named vs. unnamed).
Mirror the doc — don't upgrade "unnamed" into a stronger signal or invent figures.

Render cases (the value goes inside the quotes the script prints):
- **Doc discloses structure** → the distilled clause, e.g. `Mgr members
  Barcelo/Anderson/Atkins (2-of-3 vote); non-mgr investors ~23.5% of founder
  shares, 0% of PP warrants, no control`.
- **Doc silent** → `""` (empty — "checked, nothing on record").
- **Doc confirms all-principal** → `none — wholly principal-funded`.
- **No doc** → `"" ` with the script already flagging no-doc context is fine; set
  `non_managing_members=""`.

---

## s/f-4 count (in-deal only)

Read the registration-statement count the doc records (base S-4/F-4 = 1, each
amendment +1). Pass as a string the script prints as-is:
- count on record → `"3 (per memory doc)"`
- doc says none filed → `"0 (per memory doc — none filed)"`
- doc has no count → `null` (script renders `s/f-4s: not in doc`)

NEVER reconstruct from EDGAR or `s4_amendments`.

---

## Extension terms

Read deposit economics from the summary (structure/timeline section or a Pillar
entry). Set `ext_per_share_per_month`:
- **Per-share monthly** ("$0.033/sh/mo") → use directly.
- **Flat monthly cap** ("$375,000/month") → `cap / public_shares_outstanding`.
- **Per-period lump** ("$0.10/sh per 3-mo extension") → set
  `ext_per_share_per_month` to the lump and `ext_lump_period_days` to the period
  in days (script uses the cadence variant).
- Doc records none / pre-deal inside first deadline → `0`.
- In-deal or post-anniversary but doc **silent** → `0` AND `ext_silent=true`
  (script prints `Extensions: not in doc — yields may be understated; use
  trading-note-extended to verify`).

Past deposits are already in the sheet CIT — only future deposits are modeled.
Optionally pass `ext_active_since` and `ext_deposits_to_date` for the footer.
Use only what the doc states; never reconstruct from the sheet or first principles.
