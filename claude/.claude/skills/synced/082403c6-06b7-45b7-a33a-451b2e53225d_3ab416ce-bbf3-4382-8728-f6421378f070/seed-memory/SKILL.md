---
name: seed-memory
description: "Orchestrator for Meteora SPAC memory docs. Seed Mode (new doc): pre-deal builds a 3-pillar doc (S-1 extraction, trading note, sponsor bios); in-deal builds a 6-pillar doc (adds S-4 extraction, deal review, and a Target Dossier — company history, funding rounds, comps, lineage, valuation) and composes a DEAL-FOCUSED summary per references/in-deal-summary.md. Update Mode (existing doc, stage unchanged): refreshes the summary to current guidance; never overwrites entries. Deal Transition Mode (pre-deal doc whose SPAC just announced a BCA): appends in-deal pillars 4-6 and REBUILDS the summary to the deal-focused template — target/deal/valuation as the lede, sponsor cut to PIPE-raising only. Trigger on seeding, updating, or transitioning a doc: 'seed/build memory for X', 'update/refresh summary on X', 'X announced a deal', 'X/[target] BCA', 'transition X to in-deal'. Also when a SPAC is referenced with no doc, an S-1/S-4/BCA is pasted, or 'deal announced'. Always use this skill; never ad hoc."
---

# Seed Memory — End-to-End SPAC Doc Initialization

Stand up a Meteora memory doc from scratch for a SPAC, OR refresh an existing doc's executive summary to current guidance. This skill orchestrates the firm's diligence sub-skills (3 for pre-deal: `spac-s1-extraction`, `trading-note-extended`, `spac-bios`; 5 for in-deal, additionally including `spac-s4-extraction` and `spac-deal-review`) and writes their outputs into a properly structured memory doc via `MeteoraMCP-AWS:create-memory-doc`, `MeteoraMCP-AWS:update-memory-doc`, `MeteoraMCP-AWS:update-memory-summary`, and `MeteoraMCP-AWS:patch-memory-summary`. After the doc is written (Seed Mode) or the summary is updated (Update Mode), the executive summary is also emailed as nicely-formatted HTML to `filings@meteoracapital.com` so the team has a snapshot alongside the canonical doc — see Step 4.6 / Step U.7.

Every name worth covering gets the same first-pass treatment, so subsequent diligence builds on a consistent foundation. The skill exists because seeding a new doc by hand routinely loses one of the three pillars (structure, tape, or team), and inconsistent seeding compounds across the universe.

---

## Core Principles

1. **One doc, three pillars, one summary.** Every seeded doc is built from the same three sub-skill outputs (S-1 extraction, trading note, team bios) and a unified executive summary that synthesizes across them. Do not seed a doc with only one or two pillars — partial seeds lose comparability across the universe.

2. **The memory doc is the canonical artifact, not the chat output.** The chat output is a confirmation receipt. Real work product lives in the doc. `MeteoraMCP-AWS:read-memory-doc` is what every subsequent skill (`trading-note-extended`, `spac-deal-review`, `spac-headlines`, `spac-ai-agent`) reads. Seeding the doc properly is what makes those skills useful downstream.

3. **EDGAR is a first-class S-1 source, not a fallback.** When the user has not uploaded a PDF, `MeteoraMCP-AWS:edgar-filings` + `MeteoraMCP-AWS:edgar-filing-text` (or `MeteoraMCP-AWS:edgar-filing-index` for exhibit URLs) IS the primary path. Do not ask the user to upload a PDF if EDGAR has the filing — pull it directly. Asking the user to do work the tool can do is wrong.

4. **Pre-effective SPACs require graceful degradation.** A new IPO often does not yet trade on Bloomberg, has no EMSX activity, and is not in `MeteoraMCP-AWS:spac-details`. The trading-note step degrades to a "structural extraction only" output rather than failing. The doc still gets seeded with everything available.

5. **Do not silently skip a pillar.** If a pillar can't run (no S-1 found on EDGAR, no team bios possible because the S-1 has no biographies, etc.), explicitly note the gap in the executive summary's "On the horizon" section so future work knows what to fill in.

6. **The executive summary is a synthesis, not a paste — but team and sponsor track record warrant fulsome treatment.** Do not concatenate the three sub-skill outputs into the summary. The summary is a content-driven distilled view of: structure (from S-1), tape + yield (from trading note), team (from bios), and sponsor/franchise track record (from bios + web search), with a trade view at the end. There is no fixed word ceiling. Structure / tape / yield sections are dense and short — those details live in the Pillar 1 and Pillar 2 entries and only need 1-2 lines each in the summary. Team bios and sponsor track record sections, however, must be substantive and stand alone — multi-sentence per principal, named-vehicle-with-outcome per prior SPAC. A summary that runs 1,000-1,500 words because the franchise has five named principals and four prior SPAC vehicles is correct; one that runs 600 words because team and franchise were compressed to one-liners is wrong.

7. **One Bloomberg call, batched.** When pulling the live tape, batch all tickers (common, warrant, rights, USGG3M Index) into a single `get-price` call. Sequential single-ticker calls are wrong.

8. **Always use `MeteoraMCP-AWS:list-memory-docs` first** to confirm whether the doc exists. The skill operates in three modes (disambiguated in Phase 0 by doc existence + stage):
   - **Seed Mode** (doc does not exist, OR exists only as an unseeded auto-created stub — see the Phase 0 stub check) — runs the full pillar workflow against fresh data and writes a new doc with new entries + new summary. Stage-aware: 3 pillars + pre-deal summary for pre-deal; 6 pillars + deal-focused summary (`references/in-deal-summary.md`) for in-deal.
   - **Update Mode** (doc exists, is actually seeded per the stub check, and stage matches the doc's shape) — re-runs the diligence sweep ONLY to bring the existing summary into compliance with current guidance (post-deSPAC quality calibration, full director enumeration including IPO-original IDs, exhaustive franchise enumeration via officer-bio tenure lists, removal of tape-characterization phrases, etc.), graded against the template matching the doc's stage. Update Mode does NOT overwrite existing pillar entries; it rewrites the executive summary using `MeteoraMCP-AWS:patch-memory-summary` (preferred — targeted exact-match substitutions) for partial edits, falling back to `MeteoraMCP-AWS:update-memory-summary` only for genuine full rewrites. If gaps are found in the existing pillar entries, Update Mode appends a `correction`-tagged entry documenting them. The skill enters Update Mode automatically when the doc exists and stage is unchanged; do NOT direct the user to `MeteoraMCP-AWS:update-memory-doc` and do NOT refuse to proceed.
   - **Deal Transition Mode** (doc exists, was seeded pre-deal, and the SPAC has just announced a BCA) — appends the in-deal pillars (4 `spac-s4-extraction`, 5 `spac-deal-review`, 6 Target Dossier) as NEW entries, leaves pre-deal Pillars 1–3 untouched, and REBUILDS the executive summary wholesale to the deal-focused template (`references/in-deal-summary.md`) via `MeteoraMCP-AWS:update-memory-summary`, re-centering on the target and collapsing sponsor coverage to PIPE-raising track record (CP20). See Phase D.

9. **Sheet bucket is ground truth for tier; Claude does not propose revisions.** The `bucket` field from `MeteoraMCP-AWS:spac-details` (1, 1.5, 2, 2.5, 3 — lower is higher quality) is the firm's canonical quality ranking and is quoted verbatim in the executive summary's one-line view. The sheet bucket reflects the team's accumulated judgment across underwriter, sponsor, structure, and prior outcomes — Claude's pillar pass does not re-rank it, silently or via a “suggested revision” flag. Bucket changes are desk decisions made in conversation: the doc records a revision ONLY when a transcript / email / desk note captured in the doc explicitly directs one, recorded as `Bucket revision per desk ([name], [date]): [old] → [new]` with attribution per CP21. Findings that bear on quality — a billionaire principal the sheet didn't capture, a prior public-co bankruptcy on the team, an anchor the sheet doesn't reflect — are stated factually in their own sections and left for the desk to weigh. Stating the fact is Claude's job; moving the bucket is not.

10. **The executive summary must stand alone.** Downstream skills (`trading-note-extended` thesis pulls, `spac-deal-review`, `spac-headlines`, `spac-ai-agent`) read each doc's summary in isolation — they do not pull peer docs to fill in context. This means the summary cannot substitute `"same officer as [peer ticker]"`, `"identical to [peer franchise]"`, or `"see [peer doc] for details"` in place of actual content. Even when the SPAC is the n-th vehicle in a franchise (a sister Cantor / Churchill / Ajax / Pono SPAC with the same officer slate), the summary must restate the substantive biographical, sponsor-track-record, and aggregate-metric content in full. Cross-references to peer docs are valuable as supplements (`"see [peer ticker] for paired-position thinking"`) but never as substitutes for primary content. The single highest-impact failure mode of this skill is producing a summary so referential it ceases to be useful when read alone — guard against this aggressively.

11. **The executive summary is evergreen — no point-in-time data and NO trading characterization, even as a brief phrase.** Live prices, yields, spreads, volumes, today's-mid-position-MV, yield-to-est-date-as-of-today, "trades at +1c premium today" — anything that goes stale within days — does not belong in the summary. Tape data lives in timestamped Pillar 2 entries which carry the "as of" context. The summary describes durable facts: structure, team, track record, thesis. **No trading characterization is permitted anywhere in the summary, even as a phrase.** Forbidden constructions include: `"trades at/near trust on thin volume,"` `"trades at a discount with active arb-desk participation,"` `"premium to trust on illiquidity, not signal,"` and any other liquidity / premium / discount / volume framing. (This tightens prior guidance which had allowed brief tape phrases in the one-line view; that carve-out is rescinded.) The summary template has NO Tape section AND the One-line view has no trading-characterization element — if Claude finds itself writing either, it is doing the wrong thing. Position section gives durable share count and % of public float; current dollar mark is omitted (or at minimum carries an "as of [date]" caveat that signals it's stale by default). The test: a summary written today should still be ~95% accurate when re-read in 6 months barring a deal announcement or extension event. Tape data fails that test in 6 days; even structural phrasings like "illiquid" / "thin liquidity" inappropriately drift toward tape framing and should be replaced with durable structural language ("smaller deal size", "naked-common float of ~22M") that survives the 6-month re-read.

    **CP 11 sub-rule (a) — The tape-data prohibition is content-based, not label-based.** The prohibition extends to any subsection that stores tape data, regardless of its parent label or position in the summary. A "Verdict Block" with a `TAPE:` row, an "At-a-glance" snapshot, a quick-view header table, a "Status" line, a "Cover" bullet, or any other nested wrapper that stores bid/ask, current float counts, current trust-per-share, redemption percentages, current dollar marks on positions, two-sided-market framing, current yields, or any other point-in-time data is STILL a Tape section — it is just nested under a different label. The wrapper can claim to be "structural synthesis" and can even be prefaced by an explicit CP 11 reference ("durable structural synthesis — live tape lives in Pillar 2 entries per CP 11"); if the body still contains tape data, it violates CP 11. The wrapper label is window-dressing; the content is what is prohibited. Test: if the content would go stale within days, it does not belong in the summary, no matter what wrapper section it sits in. Sub-sections containing entirely durable content (SPONSOR / TARGET / STRUCTURE / TRADE rows of a Verdict Block) do not by themselves trigger this sub-rule — the violation is specifically the tape-bearing row (typically a TAPE: row or similar) within the wrapper, which must be excised.

    **CP 11 sub-rule (b) — The canonical section list is closed.** For PRE-DEAL docs the allowed sections are exactly: One-line view, Structure, Risk Factors / Atypical Features, Sponsor team, Sponsor track record, Relationships & Coverage, Filing track, Position, Trade view, On the horizon. For IN-DEAL docs the closed list is different and larger — it is defined in `references/in-deal-summary.md` Part 2 (One-line view, Deal terms, Target overview, Company history, Funding history, Comparable companies, Related companies / lineage, Valuation, Pro forma capitalization, Target management, Sponsor — PIPE-raising track record, Relationships & Coverage, Structure, Risk Factors / Atypical Features, Filing track, Position, Trade view, On the horizon). Use the pre-deal list for pre-deal docs and the in-deal list for in-deal docs; do not mix them. Adding extra subsections — Verdict Block, At-a-glance, Snapshot, Quick view, Status, Cover row, Header bullet, "TL;DR", "Executive bullets at top", "Warrant cohort" / "SPAC cohort" comparison blocks, or any analog — bloats the summary, duplicates content from the canonical sections, and creates the structural pressure to compress into tape-style framing that produced sub-rule (a)'s nested TAPE: row in the first place. Brief structural compressions belong in the One-line view, which already exists for that purpose; longer durable content belongs in the named canonical sections. Do not seed extras; do not preserve them when found in existing docs. In Update Mode, encountered extra subsections must be patched out wholesale via `MeteoraMCP-AWS:patch-memory-summary` (empty `new_str` for the entire wrapper, including its preamble line and every row inside) — do NOT try to "rescue" them by editing values or relabeling rows. The structural element itself is the problem, not the specific data in it.

12. **The Risk Factors / Atypical Features section captures deal-specific, material, differentiating findings.** Class B Consent Right, sole-UW = sponsor affiliate, sponsor-controlled board pre-BC, founder shares = 20% promote, sponsor-friendly governance — these are universal SPAC features and do NOT belong here. Number of S-1 amendments, registration cycle length, liquidity profile, and other position-management considerations are not findings unless tied to a substantive material change (auditor change, mandate scrub, right-economics richening, founder-share split changes, per-share overfund added or removed, extension cadence step-up). A finding is something that differentiates THIS deal from the SPAC norm or from the immediately-prior franchise sibling, in a way that affects thesis, sizing, or exit logistics. If Claude can't articulate the differentiation in a single clause ending in "...unlike [peer / SPAC norm]", the item does not belong here. The section earns its name; pad-content findings dilute the real ones.

    **CP 12 — section name rationale.** This section was previously named "Bombs" — that label is rescinded for two reasons. First, "Bombs" is editorial color (see CP 18) and implies binary catastrophe when many genuine findings are not catastrophic, just atypical. Second, the section scope is broader than risk: it captures both (a) genuine risks (sponsor track record problems, going-concern restatement footnotes, terminated prior PIPEs) AND (b) atypical features that are structurally differentiating but may be neutral or even positive (e.g., right-ratio richening from 1/10 → 1/4 is a *favorable* atypical feature that absolutely belongs in this section per CP 13). "Risk Factors / Atypical Features" is accurate, neutral, and captures both polarities. Use it as the section header. Singular noun within the section is "finding" (each finding is either a risk factor or an atypical feature, depending on polarity). When Update Mode encounters an existing doc with a "Bombs" header, patch the header to "Risk Factors / Atypical Features" — see Step U.2 item #5.

    **CP 12 sub-rule (a) — Going concern and other standard-feature framings are not findings.** Going-concern opinions are universal for blank-check shells (every SPAC auditor issues one as the redemption-deadline approaches) and are standard for pre-revenue or sub-scale operating-company targets. Listing "both sides going concern" as a section headline pads the section without saying anything. If the underlying disclosure contains a genuinely uncommon element — a multi-section audit restatement footnote, a specific derivative-classification dispute, an SAB 99 materiality call, a 16-section restatement covering SAFEs/convertibles/balance-sheet/cash-flows — reframe the finding around the uncommon element and treat the going-concern itself as a routine factual disclosure. Same logic applies to other standard SPAC-life features: routine NT 10-Q filings near deadlines, deferred-fee waivers (the norm, not the exception), founder lockups with $12 early release, standard 1% backstop terms — none are findings unless the specifics deviate meaningfully from the SPAC norm.

    **CP 12 sub-rule (b) — Thematic-precedent reach dilutes the structural point.** If the sponsor's prior franchise outcomes already produce a sponsor-pattern finding (e.g., "2-of-2 prior consummations resulted in post-deSPAC failure"), do NOT add a separate "and the prior failure was also in [sector / theme]" finding. Theme-matching between prior failed deSPAC and current target is rarely the operative signal — sponsor execution capability is. Stacking a thematic-precedent finding on top of a sponsor-pattern finding double-counts the same underlying concern (sponsor cannot execute) while creating false specificity (it implies the theme is the problem when the structural diagnosis is sponsor capability). Use the precedent for one frame at a time — either sponsor pattern OR thematic pattern, whichever is the operative signal — not both.

13. **Comparative diligence against the immediately-prior franchise sibling is mandatory.** When a SPAC is part of a franchise (Cantor, Churchill, Ajax, Pono, Replay, Forest Road, etc.), every structural feature must be cross-referenced against the immediately-prior franchise vehicle and any other recent siblings. Things added relative to the prior sibling, things dropped (e.g., `"prior franchise vehicles had a $0.15 per-share overfund at redemption; this one does not"`), terms enhanced (right-ratio richening from 1/10 to 1/4), terms degraded (founder share count increased per dollar of trust), trust-per-share differences, extension cadence changes, OA exercise differences — all of these are top-of-page diligence findings and routinely belong in the Risk Factors / Atypical Features section. The high-impact failure mode this principle exists to prevent: missing that the new deal silently *removed* a sweetener that prior deals had (e.g., overfund kicker dropped) — this is the most actionable comparative finding in franchise SPAC diligence and is also the easiest to miss because the omission isn't called out in the S-1.

14. **Franchise vehicle enumeration must be exhaustive — own vehicles AND adjacent precedents.** When seeding a franchise SPAC, enumerate every vehicle in the franchise's history: pre-IPO shells with registered S-1s but not yet priced, in-flight IPO'd siblings (CEP I/II/III/IV/V/+, CFFE I/II/III/+, Churchill VI/VII/+, etc.), in-deal vehicles, completed deSPACs (with PubCo names + dates + outcomes), liquidated vehicles. Use EDGAR CIK family search — franchise CIKs are usually clustered numerically — combined with the franchise's IR archive and news archive. Beyond own-sponsored vehicles, also capture franchise-adjacent precedents: deSPAC transactions where the sponsor served as PIPE provider, FPA provider, anchor investor, or deSPAC underwriter without sponsoring the SPAC itself (e.g., Securitize for Cantor). These adjacent precedents demonstrate vertical capability and pipeline depth and routinely matter more than own-sponsor track record for assessing PIPE-raise track record. Do not list only the vehicles that came up in conversation — sweep the universe systematically before composing the summary. `"CEP II / CEP III not confirmed"` is NOT an acceptable data gap deferred to "On the horizon" — resolve it before writing. Do not assert aggregate cadence numbers (`"2 vehicles in last 10 weeks"`) that aren't directly verifiable from the enumerated vehicle list — hallucinated cadence is a known failure mode.

    **CP 14 sub-rule — Pending vehicles do NOT enter hit-rate denominators.** Aggregate franchise metrics (consummation hit rate, post-deSPAC quality counts) are computed against vehicles with terminal outcomes only — closed deSPACs, liquidated SPACs, terminated BCAs followed by liquidation. The SPAC currently being analyzed is by definition pending and does not enter its own franchise denominator. Standard phrasing: "X of Y prior vehicles with terminal outcomes consummated (excluding pending [TICKER])." Counting the pending vehicle as a "0-of-2" or "2-of-3" against itself is a logic error that appears repeatedly across summary, verdict block, and bucket-revision sections — sweep for it explicitly. Same rule for in-flight BCAs that haven't yet closed or terminated: count them only after the terminal outcome lands.

15. **The threshold-of-concern for ownership concentration is 9.9%, not 5%.** The 5% Schedule 13G filing threshold is administrative and is not a thesis-level concern — Meteora files 13Gs as a matter of course. The threshold that affects investment behavior — affiliate status, 13D triggering events, voting limitations, redemption restrictions, side-pocket implications — is 9.9%. Do not flag 5% positions as compliance "action items" or as findings in the Risk Factors / Atypical Features section. Only flag concentration concerns when approaching or exceeding 9.9% of public float. Below 9.9%, position-size context belongs in the Position section as a durable factual observation (`"~5% of public float"`) without a compliance flag. Below ~1% of public float, even the position-size framing should be dropped — at that scale, concentration is not a topic. State the share count cleanly and move on; lines like "No 9.9% concentration concern" on a sub-1% position add noise without information.

16. **Post-deSPAC outcomes are graded per the OUTCOMES-RUBRIC memory doc — read it before grading anything; it supersedes any rubric text embedded in any skill file.** The canonical, desk-editable rubric lives in the `OUTCOMES-RUBRIC` memory doc (`MeteoraMCP-AWS:read-memory-doc(name="OUTCOMES-RUBRIC")`). Reading it is a mandatory pre-step wherever a prior-SPAC outcome is graded (Phase 3, Phase 4 assembly, Update Mode gap item 3, any franchise aggregate). These grades measure a SPONSOR'S TRACK RECORD — (a) bringing something public the market sustainably valued, and (b) pulling real capital into the deal to close it — not pure point-in-time deSPAC tape, and never IPO-investor expectations. The rubric's load-bearing rules, restated so intent survives paraphrase:

    - **Factor 1 — tape band, read peak AND current, take the BETTER.** Bands vs the $10 trust reference: **Strong** = sustained above $10; **Good** = sustained $7–$10; **Mediocre** = $4–$7; **Poor** = below $4 but still a viable, listed going concern; **Failed** = structural failure ONLY (bankrupt, delisted for non-compliance, liquidated, receivership). A sub-$1 price by itself is Poor, never Failed. “Sustained” ≈ a level held ~3+ months (or a 3-month median/VWAP at the band line), excluding the first 1–2 weeks of trading and transient/meme spikes. Grading on the current price alone is the misapplication this rule exists to prevent — a sustained higher band gave arb holders a realizable exit and demonstrated real market demand; equally, an above-trust CURRENT price is itself the definitive read regardless of the path that led there.
    - **Successes get graded, not narrated.** When the peak-and-current read lands Good or Strong, the outcome is a SUCCESS: state the grade, the sustained band, and the current price as a present-state fact — then stop. Do NOT attach drawdown color, “brutal stretch” narration, or counts-against-the-sponsor framing to an interim decline: a multi-year drawdown between a sustained high and today is an operating-company / macro story that a redeem-at-trust holder was never exposed to, and it is not the sponsor's grade. (Worked case: NextNav — PIPE raised, closed through heavy redemptions, current price above trust → an obvious success; one factual line, no color.)
    - **Factor 2 — capital-formation overlay: a qualifying closing raise LIFTS the tape band; the lift is a qualitative judgment, not a dollar threshold.** There is NO hard $100M (or any other) bright line. A qualifying closing PIPE / committed financing (real, committed, identifiable institutional capital that funded the close — PIPE, forward purchase, non-redemption book, sponsor-affiliated committed equity) lifts the band one tier at minimum, and two tiers on a viable name when the recorded qualitative context marks the raise as franchise-defining. Weigh, and state in the grade line: **era of close** (post-2021 SPAC-winter closing PIPEs were rarities — any winter-era raise is an outsized capability signal), **redemption backdrop** (assembling a book against 90%+ redemptions is the harder feat), **anchor quality** (named institutional capital), **size relative to the deal**, and **sponsor→newco board continuation** (principals taking PubCo board seats = conviction and alignment; count it from the merger proxy / newco roster). A winter-era closing raise assembled against heavy redemptions on a still-viable name presumptively earns the two-tier lift. (Worked case: SPWR/Complete Solaria — ~$80M assembled against ~99% redemptions in the 2023 winter → Poor tape lifted two tiers → **Good**.)
    - **Caps preserved:** structural Failed caps at Poor no matter the raise; only sustained >$10 tape earns Strong — the overlay never manufactures Strong. The overlay only lifts, never drags: a small or absent raise is neutral, never a penalty (and pre-deal, absence is never a mark at all — CP24). “Success” for franchise hit-rate / aggregate-quality purposes = Strong or Good.
    - **Always pull the post-close sustained high AND the live Bloomberg price** on every prior consummated deSPAC ticker before grading — never grade from training-data priors — and state both factors explicitly in the grade line, e.g.: “Good — Poor sustained tape ($1–3, viable), lifted two tiers by the ~$80M winter-era closing book assembled against ~99% redemptions.”

    **CP 16 sub-rule (a) — Do NOT use trust-value-as-anchor framing for deSPAC outcomes.** The construction "PubCo acquired for $10M = 96% destruction of original $250M trust" is wrong on first principles. SPAC trust capital is redeemable at $10 (plus interest) by definition; no public shareholder is exposed to the deSPAC outcome with their trust dollar. The trust does not "sit in" the operating company at risk — it goes either to redeeming shareholders or to the post-close balance sheet, but the redemption right is the floor for any non-electing holder. Comparing post-close market cap to original IPO trust size manufactures a destruction figure that misrepresents what was actually at risk. Describe the post-deSPAC outcome directly: current PubCo price tier, market cap, whether bankrupt / delisted / penny / Pink Sheets / forced reverse splits. The rubric labels in this principle already capture the severity gradient — let them do the work.

    **CP 16 sub-rule (b) — Do NOT use ad-hoc editorial grades.** "Catastrophic", "complete failure", "near-total value destruction", "wipeout", "annihilation" are not grading labels in this rubric. The canonical labels are strong / good / mediocre / poor / failed; use them verbatim. Editorial color in grade lines ("Quality: catastrophic") creates inconsistency across docs and substitutes rhetoric for the structured assessment. If the outcome is bankruptcy or sub-$1 trading, the rubric label is "failed" — that already carries the severity. Reserve the rubric labels for quality lines and let any additional facts (price tier, delisting, mkt cap) stand on their own.

17. **Standing redemption protocol is implicit; do NOT restate it for positions Meteora does not hold.** For trust-arb names, the standing protocol is redeem at trust unless an explicit reason exists not to — every reader of these docs knows this. The summary does not need to state "Common AVOID/SELL/REDEEM" or "Post-deSPAC [PubCo] common: AVOID" as a recommendation when Meteora's position in that leg is zero. The Position section documents zero common (or zero rights, or zero warrants — whichever legs are absent); that suffices. Issuing a SELL/AVOID rec on a leg Meteora doesn't own implies a position-management action that doesn't exist. Apply this rule consistently across the One-line view, Verdict block, Trade view, and any "Post-deSPAC" recommendations: if the leg is unheld, the summary describes it factually (structure, dilution, post-close outlook) without issuing a rec. Same logic for any combination of legs — naked-warrant positions don't carry common-leg recs; naked-common positions don't carry warrant-leg recs.

18. **Avoid editorial color and punchy rhetorical framings.** Phrases like "the pattern of X IS the pattern", "death spiral", "doom loop", "near-total value destruction", "catastrophic", "no way to put lipstick on this", "a 0-of-anything record", "the franchise is the problem" substitute style for substance and date the document — they read as commentary, not analysis. State facts cleanly: prior-vehicle outcomes by ticker with current price tier; aggregate metric (X-of-Y); rubric grade. Tape characterizations ("thin two-sided market", "near-zero volume", "single-share OTC bids") edge toward the prohibition in CP 11 — replace with structural framing ("two-sided market", "microscopic public float", "OTC Pink stub"). This extends the Tips-section color-cut rule that previously applied to bios so that it also governs the Risk Factors / Atypical Features section, one-line views, and trade views. The CP 12 section rename ("Bombs" → "Risk Factors / Atypical Features") is an application of this principle to a section header — section names should describe scope, not strike a tone. Test: if a sentence can be deleted without losing fact-content, delete it. Test 2: if a phrase functions as drum-roll or rhetorical underscore rather than information, cut it.

19. **Plain language for sell-side and sponsor-press jargon — define on first use.** This extends Core Principle 11's parenthetical-definition rule from structural terms (Crescent Term, ZEP, OA exercise) to operational and market-microstructure terms that read clearly to a SPAC desk but opaquely to anyone else reading the doc cold. Examples of jargon that should be expanded or replaced:
    - "terminated on redemption volume" → "redemptions at the extension or BCA vote left trust capital below the deal's minimum-cash threshold; the SPAC terminated the BCA and liquidated"
    - "bumped on tape" → "first reported by [outlet] before the official 8-K"
    - "going effective" / "went effective" → "the SEC declared the S-4 (or other registration) effective"
    - "crossed for redemption" → "redeemed at the redemption deadline"
    - "got plugged" / "got bagged" → state the actual fact (filled at $X, redemption hit at $Y)
    - "stuck on tape" → "did not trade today" or "no two-sided market today"

    The summary must be readable cold by a Meteora analyst who has never traded SPACs before. If a phrase would require translation, translate it in-line.

20. **In-deal docs re-center on the deal — the target is the lede, sponsor coverage collapses to PIPE-raising track record.** A pre-deal summary leads with the sponsor because the deal does not yet exist; deal-sourcing AND PIPE-raising track record both matter. The moment a BCA is announced, the deal exists and deal-sourcing capability is spent history. The summary pivots to the **target and the deal**: what the company is, its history since inception, its private funding rounds, its comparable companies, its spin-out/parent lineage, the valuation the deal implies, and the full deal terms. Sponsor coverage shrinks to the only forward-looking sponsor question left — *can they raise / have they raised the capital to close at the minimum-cash threshold?* — i.e. PIPE / committed-financing track record graded per CP16, plus a one-line board-composition note. Drop the full director-by-director slate and deal-sourcing narrative from the in-deal summary (they remain in the Pillar 3 entry). Management diligence in-deal means the **target's operating team**, bio'd with the depth pre-deal bios gave sponsor principals. This focus shift is mandatory and identical for BOTH paths that produce an in-deal doc — Seed Mode at in-deal stage (from scratch) and Deal Transition Mode (existing pre-deal doc, BCA just announced) — and is templated once in `references/in-deal-summary.md`, which both paths read and follow verbatim. All other Core Principles (evergreen/no-tape CP11, color-cut CP18, plain-language CP19, standing-protocol CP17, concentration CP15, bucket-verbatim CP9, prior-deSPAC grading CP16) continue to govern unchanged.

21. **Human-authored theses, desk views, and argumentation are load-bearing — no summary rewrite may drop them.** Summaries get rebuilt (Deal Transition Step D.6, Update Mode full rewrites, in-deal re-seeds); human judgment does not regenerate. A desk view recorded in the doc — an attributed argument ("Elroy = hardware OEM vs Merlin = software autonomy; hardware may command MORE public-market value — Vik"), a bear/bull case sourced from the street, a pair-trade or relative-value framing against another name, a why-we-own-it thesis, a dissent between desk members — is the single most valuable content in the doc, worth more than any Claude-generated synthesis, because it captures a position-holder's reasoning at a point in time and cannot be reconstructed from filings. Losing it in a rewrite is the worst failure this skill can produce — strictly worse than a formatting violation or a stale comp. Before ANY summary rewrite, in any mode:

    **(a) Inventory first.** Sweep the existing summary AND all entries for human-generated content: entries whose author is not Claude; attributed views inside any entry body ("Vik:", "Walter:", "Alex:", "per the desk", "framing (NAME)", named Twitter/street sources); thesis lines; trade-view argumentation; pair-trade and relative-value cross-reads; open desk debates; and relationship / coverage intel (named bankers and brokers, sponsor contact email domains, "same sponsor as [ticker]" cross-reads, in-flight introductions) — the raw material for the Relationships & Coverage section (CP23), which is almost entirely human-sourced and therefore especially prone to being lost in a rewrite. Write the inventory down as a checklist before composing.

    **(b) Carry forward, with attribution.** Every distinct human view that has not been mooted by events must appear in the rebuilt summary — attributed and dated where the source is attributed ("desk view (Vik, 6/26): ...") — in the appropriate canonical section: Trade view for position theses and desk debates; Comparable companies for relative-value cross-reads; Risk Factors / Atypical Features for human-flagged concerns; Relationships & Coverage (CP23) for banker/broker/sponsor-contact intel, sponsor cross-name linkages, and introduction status. Compression is fine; deletion is not. If a human view references tape ("Merlin trades at a discount"), do NOT drop it under CP11 — restate the argument durably (a relative-value claim: "MRLN screens cheaper than the implied Elroy valuation — the desk's bear cross-read") so the reasoning survives even as the tape reference is generalized.

    **(c) Retire explicitly, never silently.** If an event has genuinely mooted a human view (deal terminated, the debated instrument redeemed), the rewrite may move it out of the summary — but the transition / correction entry MUST record which human views were carried forward (and to which section) and which were retired (and why). Silent disappearance is the exact failure mode this principle exists to prevent; the ledger makes every drop deliberate and reviewable. The ledger protects HUMAN content only — Claude-generated framings that prove wrong are simply patched out: no “retired”, “superseded”, or “previously stated” residue in the summary or in chat deliverables, and no ceremony around the old framing. The correction entry is the sole record of what changed; the summary reads as if the error never existed.

    **(d) Precedence.** Where a Claude-synthesized framing and a human desk view disagree, the human view leads and the synthesis is presented alongside as context — never the reverse. CP18's color-cut targets Claude-generated rhetorical filler and biographical anecdote; it is NOT license to cut human argumentation. CP11's evergreen rule governs how a human view is phrased, not whether it appears.

22. **F-4/S-4 discovery is multi-registrant - never conclude "no S-4/F-4 filed" (or mark the target's financials, history, or ownership as a data gap) from a SPAC-CIK-only search.** The registration statement that carries the target's audited financials, MD&A, business description, funding history, and beneficial-ownership table is frequently NOT filed under the SPAC's own CIK. Foreign-private-issuer and offshore de-SPACs (Cayman / BVI / PRC / most Asia-Pacific targets, and many domestic ones) route the deal through a NEW listing holdco (the pro forma PubCo) or a merger sub, and file the F-4 (or S-4) under THAT entity's separate EDGAR CIK. A lookup that resolves EDGAR only by the SPAC ticker or SPAC CIK will find nothing and wrongly report "no F-4 / DATA GAP" while a full registration statement - with every section the Target Dossier needs - sits under the holdco's CIK. This is the single most damaging silent-failure mode in the in-deal build: it converts an available, extractable filing into a fabricated "unavailable" and poisons Target overview, Company history, Funding history, Valuation, and Target management with false data-gap language. It is exactly how a real Meteora doc came to assert "NO F-4 filed" for a deal whose F-4 was on file under the target's listing holdco. Before Phase 1B / Phase T / Phase D may record that no registration exists, run the **3-pass discovery protocol**:

    **Pass 1 - SPAC registrant.** `MeteoraMCP-AWS:edgar-filings(cik=<SPAC CIK>)` for `S-4`, `S-4/A`, `F-4`, `F-4/A`, `424B3`. Use the CIK, not the ticker: `edgar-filings(ticker=...)` routinely fails to resolve for delisted / OTC SPACs, which is itself a reason a SPAC-only check comes back empty.

    **Pass 2 - the new listing holdco / PubCo / merger-sub registrant (the pass that catches the FPI case).** Read the BCA 8-K to get the name of the pro forma PubCo and any merger sub (e.g. "Leading Partners Limited," "<Target> Holdings Limited," "<Ticker> Purchaser Inc."). Resolve that entity's CIK via EDGAR full-text / company search - `https://efts.sec.gov/LATEST/search-index?q="<holdco name>"&forms=F-4,S-4` or the browse endpoint `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=<name>&type=F-4` - then `MeteoraMCP-AWS:edgar-filings(cik=<that CIK>)`. This is where offshore / FPI F-4s live, and it is the pass that was missing when the failure above occurred.

    **Pass 3 - the target's own registrant.** If the target was ever an SEC filer (prior registrant, withdrawn S-1, Reg A, formerly public), search its CIK too.

    Only after ALL THREE passes come back empty may the doc state "no S-4/F-4 filed" - and it must name the registrants / CIKs searched so the negative is auditable. When a registration IS found under a holdco / merger-sub CIK, extract it in full (Pillar 4) and build the Target Dossier from it; do NOT leave "DATA GAP" language in the summary. The Filing-track line's "3-pass: SPAC CIK + PubCo CIK" note in the in-deal template is the record that this was done.

23. **The summary carries a Relationships & Coverage section — who covers the name, who reps whom, who we know, and which introductions are in flight.** SPAC arb is a relationship business: which bank ran the IPO, which advisor reps the target, which sell-side desk covers *us* on the name, which named banker to call, what a sponsor's contact email domain is, and which other SPACs share a sponsor are all load-bearing facts a desk trades on — and they were, until now, homeless in the summary, so they lived only in Bloomberg IB (Instant Bloomberg) chat scrollback and got lost. This section is where that intelligence lands so it is durable and searchable alongside the canonical doc. It is a first-class section of BOTH the pre-deal and in-deal summaries (added to both closed section lists — see CP11 sub-rule (b)).

    **What it holds:**
    - **Deal / sell-side coverage:** the bank(s) that ran the SPAC IPO; the target-side financial advisor / who reps the target (in-deal); the PIPE placement agent (in-deal); and which sell-side desks cover Meteora on the name (StoneX, Cantor, Clear Street, BTIG, Jefferies, etc.). Underwriters come from the S-1; target advisor and placement agent from the BCA 8-K / S-4 "Background of the Business Combination."
    - **Named contacts:** person — role/affiliation — email domain where known (e.g. `"Janet — sell-side coverage on EURK & COLA"`, `"sponsor contacts at @macrodm.com"`, `"Steph — DBC Asia banker"`). Name the individual and their firm; contact intel is the point of the section.
    - **Sponsor / cross-name linkage:** other SPACs that share this sponsor, or share a sponsor-adjacent contact set — e.g. `"shares sponsor with FVN; both reached at @macrodm.com"`. These linkages let one relationship serve several names and are exactly the "same guys as [ticker]" cross-reads desks make verbally and then forget.
    - **Introduction / relationship status (dated):** in-flight introductions, who is making them, and any access constraints (e.g. `"DBC intro in progress — Phil → Steph (DBC Asia banker); banker Asia-based so contact routed accordingly (7/10)"`).

    **CP23 sub-rule (a) — attribution and preservation follow CP21.** This content is almost always human-authored — it comes from desk IB exchanges, morning chats, and analyst legwork, not from filings. It is therefore load-bearing human content under CP21: attribute desk-sourced intel with name + date (`"(Henry, 7/10)"`), carry it forward on every rewrite, and never drop a live relationship fact silently — a retired contact (banker left the desk, intro abandoned) is logged in the correction/transition entry, not deleted without a trace. Losing a captured relationship in a rewrite is a CP21 failure.

    **CP23 sub-rule (b) — durable facts are evergreen; workflow items carry a date; NO tape (CP11 still governs).** Coverage identity, banker names, email domains, and sponsor linkages are durable and evergreen — they survive the 6-month re-read. In-progress introductions and access constraints are genuine relationship *state*, not durable facts, so they carry an explicit date and are understood as point-in-time relationship-workflow notes (the same treatment CP21 gives dated desk views) — this is the ONE controlled exception to the evergreen default, and it exists because "who is talking to whom right now" is precisely what the desk wanted captured. What this section may NEVER hold is **tape**: no bid/ask, yields, spreads, volumes, premium/discount, or current dollar marks — those remain prohibited here exactly as everywhere else in the summary (CP11) and live only in timestamped Pillar 2 entries. Coverage ≠ posture: "BTIG runs the SPAC and reps the target" is coverage (belongs here); "our offer sits at 10.90" is posture/tape (does NOT belong here — Pillar 2).

    **CP23 sub-rule (c) — omit gracefully, never pad.** If no relationship or coverage intel exists beyond the underwriter list, the section is a single line naming the underwriter(s) and, in-deal, the target advisor — that is enough. Do not invent contacts, do not speculate about who covers the name, and do not manufacture linkages. An honest one-liner beats a padded section.

24. **PIPE facts are track record, not prophecy — and a pre-deal SPAC without a committed PIPE never gets negative language for it.** Essentially no pre-deal SPAC has a committed PIPE; absence is the universal baseline, so it is never a differentiating mark — not in the One-line view, not in peer tables (no “None — [X] advisory only” cells), not as an “only name with no real-capital backer” contrast, not in Risk Factors / Atypical Features. Symmetrically, make no claims about a sponsor's PIPE-raising ABILITY in either direction: no speculative very-high/high/moderate/low ratings, and never a claim that a sponsor “has no PIPE-raise ability” or “cannot raise.” Speak only to the demonstrated RECORD — named closing raises with deal, size, date, redemption backdrop, and anchors (adjacent-precedent roles count: PIPE / FPA / anchor / UW on third-party deals) — plus factual distribution-network context (e.g., an advisory franchise's institutional Rolodex) recorded alongside the record, not in place of it. Where no prior raise exists, write `no prior closing PIPE on record` as a neutral fact and stop. In Update Mode, sweep existing docs for violations and patch them out (Step U.2 item 21).

25. **Structural figures cite the latest operative registration filing — and a figure the doc itself flags as uncertain may never be repeated.** The operative source for every structural figure — trust per share / CIT and any overfund, unit composition and right ratio, extension cadence and deposit amounts, OA size, founder shares / promote, at-risk capital, offering size, deadlines — is the LATEST operative filing: the 424B4 once the IPO has priced, else the most recent S-1/A or F-1/A. Never the original S-1, never the sheet, never the doc's own prior text. Mid-registration amendments routinely move exactly these figures (a $10.00 trust becoming $10.05 overfunded, a right ratio richening) — that is why the filing track is a findings source (CP13) — so re-citing a pre-amendment figure is a factual error, not a rounding nit. Duties: (a) any pass that writes or re-states a structural figure (Seed, Update, or Transition) verifies it FIRST against the operative filing's cover page / offering table — one targeted `MeteoraMCP-AWS:edgar-filing-text` pull; the sheet (`spac-details`) and the existing summary are cross-checks, never citation sources. (b) If the doc's open questions or On-the-horizon flag a figure discrepancy, resolving it from EDGAR is MANDATORY before any write that touches or repeats that figure — repeating a disputed figure while its own open-question flag stands is the exact failure this principle exists to prevent (worked case: TVIV — the summary cited $10.00/share trust while the doc's own open questions noted the latest S-1/A showed $10.05). (c) Every corrected figure is logged in the correction entry with the filing cited (form + date or accession number).

---

## Workflow Overview

The skill operates in three modes, chosen automatically in Phase 0 from whether the doc exists and whether the SPAC's stage matches the doc's shape:

**Seed Mode** (doc does not exist) runs the phases below in order. Sub-skill / pillar count is stage-aware: **3 pillars for pre-deal** (`spac-s1-extraction`, `trading-note-extended`, `spac-bios`); **6 pillars for in-deal**, adding `spac-s4-extraction` (Phase 1B, when an S-4/F-4 has been filed), `spac-deal-review` (Phase 3B), and the **Target Dossier** (Phase T — company-since-inception history, funding rounds, comps, spin-out/parent lineage, valuation inputs; methodology in `references/in-deal-summary.md` Part 1). The phase numbering labels the conditional in-deal additions Phase 1B, Phase 3B, and Phase T so they slot in without renumbering the core pillars. **In-deal seeds compose the deal-focused summary** per `references/in-deal-summary.md` Part 2 at Step 4.5 — NOT the pre-deal template.

- **Phase 0 — Pre-flight checks.** Detect mode (Seed vs Update) and stage (pre-deal vs in-deal); identify whether S-1 PDF is attached or whether to pull from EDGAR; pull our internal book via `MeteoraMCP-AWS:spac-details` (includes `stage`); pull our live trading posture via `emsx-blotter`; run a web search for top-of-mind sponsor / deal context; run the EDGAR CIK family sweep for franchise enumeration. These lookups happen in parallel and feed every downstream pillar.
- **Phase 1 — S-1 Extraction (Pillar 1).** Either run `spac-s1-extraction` on the attached PDF or run the EDGAR-direct alternative. Cross-reference key fields (founder share count, OA exercise, CIT, IPO date, deadlines) against the MeteoraMCP-AWS:spac-details payload from Phase 0. Output is the structural skeleton of the SPAC.
- **Phase 1B — S-4/F-4 Extraction (Pillar 4 — in-deal only).** Run `spac-s4-extraction` if Phase 0 detected `stage="indeal"` AND an S-4 / F-4 has been filed - established via the **CP22 3-pass discovery protocol** (SPAC CIK + the new listing holdco / merger-sub CIK + the target CIK), NOT a SPAC-CIK-only check, since FPI / offshore deals file the F-4 under the PubCo / merger-sub registrant. Output is the structural skeleton of the DEAL (consideration, redemption rights, PIPE, lockups, exchange ratio, target operating financials). If all three CP22 discovery passes confirm no S-4 / F-4 yet (BCA announced, registration pending), defer Phase 1B with a note in the doc and proceed to Phase 2.
- **Phase 2 — Trading Note + Tape (Pillar 2).** Run `trading-note-extended` if the SPAC trades on Bloomberg; otherwise run the pre-effective alternative. Reconcile the MeteoraMCP-AWS:spac-details price columns against live Bloomberg. Append the EMSX blotter snapshot — working orders, recent fills, GTC sells/buys, route status — directly into the Pillar 2 entry so the doc captures both the tape AND our posture against the tape.
- **Phase 3 — Team Bios (Pillar 3).** Run `spac-bios` from the S-1 disclosures + supplemental web search (sponsor net-worth, prior SPAC outcomes, recent press, board-position changes). MANDATORY: enumerate the full board roster (S-1 management table + every Item 5.02 8-K) and mine the CFO/CEO bios for the prior-SPAC tenure list (primary source for legacy franchise enumeration with named outcomes).
- **Phase 3B — Deal Review (Pillar 5 — in-deal only).** Run `spac-deal-review` if Phase 0 detected `stage="indeal"`. The deal review applies Meteora's skeptical framework (tape first, sponsor second, structure third, narrative last) and produces a structured view on the announced deal. Phase 3B can run on BCA materials alone — it does NOT require an S-4 filing. Phase 3B feeds the executive summary's Risk Factors / Atypical Features and trade-view sections with deal-specific findings.
- **Phase T — Target Dossier (Pillar 6 — in-deal only).** Build the target-research dossier per `references/in-deal-summary.md` Part 1: company history since inception (filings + web), past private funding rounds (amounts / dates / post-money / named investors), comparable public companies with vertical-appropriate multiples, spin-out / carve-out / parent lineage and affiliated entities, and the inputs for a basic valuation (implied deal EV + multiples vs. comps vs. last private round). Read that file in full before running this phase. Output is the Pillar 6 entry and the raw material for the in-deal summary's Target overview, Company history, Funding history, Comparable companies, Related companies / lineage, and Valuation sections. Sources EDGAR via `MeteoraMCP-AWS` and live comp multiples via Bloomberg (`MeteoraMCP:get-price` / `get-company-info`).
- **Phase 4 — Doc Assembly.** Write each pillar's output as a tagged entry to the memory doc (3 entries for pre-deal seeds; up to 6 for in-deal seeds), then compose and write the executive summary — the pre-deal template (Step 4.5) for pre-deal seeds, or the deal-focused template (`references/in-deal-summary.md` Part 2) for in-deal seeds — synthesizing across all pillars + the MeteoraMCP-AWS:spac-details / EMSX / web-search cross-checks. Apply the post-deSPAC outcome rubric (Core Principle 16 — read the OUTCOMES-RUBRIC memory doc first; grade peak-and-current with the capital-formation overlay) using fresh Bloomberg prices on every consummated prior-SPAC deSPAC ticker before grading.

Run pillars sequentially in Seed Mode — Pillar 1 produces data Pillars 1B / 2 / 3 reference; Pillar 3 routinely uses information from Pillar 1 (founder share splits, sponsor entity structure); Pillar 5 (deal review) and Pillar 6 (target dossier) routinely use information from Pillars 1, 1B, 2, and 3. Parallelizing within a stage loses cross-pillar signal.

**Update Mode** (doc exists, seeded, stage matches doc shape) runs Phase 0 then jumps to Phase U:

- **Phase 0 — Pre-flight check (lighter).** Confirm the doc exists and that stage matches the doc's shape (no pending transition); route to Update Mode. Apply the gap-checklist with the template matching the doc's stage — pre-deal docs against the pre-deal template, in-deal docs against `references/in-deal-summary.md`.
- **Phase U — Update Mode Workflow.** Read the existing doc, run a gap-checklist against current guidance (director enumeration, franchise enumeration, post-deSPAC quality grading, tape-data leakage AND tape-characterization phrases, Risk Factors / Atypical Features section, concentration framing, color-cut, cross-reference substitutes), pull only the fresh data needed to close gaps, compose targeted edits as `(old_str, new_str)` pairs, and apply them via `MeteoraMCP-AWS:patch-memory-summary` (preferred over `MeteoraMCP-AWS:update-memory-summary` for partial edits — see Step U.5 tool-selection rule). Append a `correction`-tagged entry if pillar entries had factual gaps. Update Mode never overwrites existing pillar entries.

**Deal Transition Mode** (doc exists, was seeded pre-deal, and the SPAC has just announced a BCA) runs Phase 0 then jumps to Phase D:

- **Phase 0 — Pre-flight check.** Confirm the doc exists AND is pre-deal-shaped AND the SPAC is now in-deal; route to Deal Transition Mode.
- **Phase D — Deal Transition Workflow.** Append the in-deal pillars (Pillar 4 `spac-s4-extraction` if an S-4/F-4 is filed; Pillar 5 `spac-deal-review` on BCA materials; Pillar 6 Target Dossier) as NEW entries — existing pre-deal Pillars 1–3 are preserved untouched (append-only) — then REBUILD the executive summary wholesale from the pre-deal template to the deal-focused template (`references/in-deal-summary.md` Part 2) via `MeteoraMCP-AWS:update-memory-summary`, append a `transition`-tagged entry recording the stage change, and email the rebuilt summary. The content shift is total (CP20), so this is a full rewrite, not a patch.

---

## Phase 0 — Pre-Flight Checks

Before doing anything else, run these checks. Steps 3–5 below should be issued in parallel as a single batch — they are independent lookups and feed every downstream pillar. Step 7 (franchise sweep) is also parallelizable with steps 3–5 once the sponsor entity is known from the ticker.

1. **Check whether the doc already exists** — call `MeteoraMCP-AWS:list-memory-docs` and look for the ticker.
   - If the doc does NOT exist → enter **Seed Mode** (continue with the standard Phases 1–4 below). Seed Mode is itself stage-aware: if Step 3 below detects `stage="indeal"`, the seed runs the in-deal pillar set (1–6) and composes the deal-focused summary per `references/in-deal-summary.md` — see Phase overview and Step 4.5.
   - **Existence ≠ seeded — run the stub check FIRST.** Filing pipelines auto-create docs whenever they append an entry (`MeteoraMCP-AWS:update-memory-doc` auto-creates on first write), leaving lightweight stubs that were never actually seeded. Tell-tales: no Pillar 1/2/3 diligence entries (only filing-digest / misc / headline entries); a summary lacking the canonical sections (no Sponsor team, Sponsor track record, Structure, Risk Factors / Atypical Features); self-flags like “lightweight seed”, “auto-created”, “flesh out structure/sponsor pillars on next dedicated pass”. A stub routes to **Seed Mode**, NOT Update Mode: run the full pillar workflow, append the pillar entries to the EXISTING doc (do not call `create-memory-doc`; existing entries are preserved as history; the CP21 human-content inventory over those entries is still mandatory), and compose the full summary via `update-memory-summary`. Running Update Mode on a stub produces cosmetic patches on a skeleton — the doc looks “processed” while carrying none of the three pillars. (Worked case: YICC — auto-created by the 7/9/26 unit-separation 8-K digest, self-flagged “lightweight seed”, then mistakenly given targeted Update passes instead of a seed. Surface every stub explicitly to the user/orchestrator; never silently cosmetic-patch one.)
   - If the doc DOES exist AND passes the stub check → it is one of two modes; disambiguate by stage before proceeding:
     - **Pull the current stage** from `MeteoraMCP-AWS:spac-details(ticker="<TICKER>")` (the `stage` field) and check EDGAR for a recent BCA 8-K (`MeteoraMCP-AWS:edgar-filings`). Also read the existing doc's shape via `MeteoraMCP-AWS:read-memory-doc(name="<TICKER>", summary_only=true)` — a pre-deal doc's summary leads with Sponsor team / Sponsor track record and has no Deal terms / Target overview sections.
     - **If the SPAC is now in-deal (BCA announced) AND the existing doc is still pre-deal-shaped** (no in-deal pillars; summary is sponsor-led with no Deal terms / Valuation sections) → enter **Deal Transition Mode** (jump to "Phase D — Deal Transition Workflow"). The doc must be re-centered on the deal, not merely refreshed. Do NOT route this to Update Mode — a targeted summary patch cannot perform the pre-deal→in-deal focus shift (CP20); the summary is rebuilt wholesale and the in-deal pillars (4–6) are appended.
     - **Otherwise** (doc and stage agree — pre-deal doc + pre-deal SPAC, or already-in-deal doc + in-deal SPAC) → enter **Update Mode** (jump to "Phase U — Update Mode Workflow"). The intent is "refresh the existing summary to current guidance," applied with the template matching the doc's stage. Do NOT stop, do NOT redirect the user to `MeteoraMCP-AWS:update-memory-doc`, and do NOT overwrite existing entries.

2. **Identify the S-1 source**. Ask:
   - Is there an S-1 PDF attached in this conversation? (Check `/mnt/user-data/uploads/`.) If yes → Phase 1 PDF path.
   - If not → Phase 1 EDGAR path (do not prompt the user for a PDF; pull from EDGAR).

3. **Pull our internal book** via `MeteoraMCP-AWS:spac-details(ticker="<TICKER>")`:
   - Capture: position sizes (common, warrants, rights, units), common_outstanding, cash_in_trust, deadlines (est_date, six/nine/twelve_month_date, max_date), bucket, category, underwriter, IPO date, IPO proceeds, internal "notes" and "recommendation" columns, unit composition (warrants_in_unit, rights_in_unit, rights_adjustment).
   - If the SPAC is in the sheet with non-null trust/structure → Phase 2 standard path (Bloomberg-traded).
   - If the SPAC is not in the sheet OR is pre-effective → Phase 2 pre-effective path.
   - Treat the sheet's `notes` and `recommendation` as flags worth verifying, not authoritative — they are often stale. The same applies to the sheet's structural figures (cash_in_trust, unit composition, deadlines): cross-checks against the operative filing, never the citation source (CP25).

4. **Pull our live trading posture** via `MeteoraMCP:emsx-blotter(tickers=["<COMMON>", "<WARRANT>", "<RIGHTS>", "<UNIT>"])`. Use a batched `tickers` array, not sequential single-ticker calls.
   - Surface: working orders (BUY/SELL, side, amount, limit_price, GTC vs DAY, broker, account, route status), filled amounts and avg fill price, idle balance.
   - Compare working order limit prices against the live Bloomberg quote (Phase 2) — orders sitting far from market may be stale and worth flagging to the user.
   - If the EMSX returns no orders, that itself is information — record "no live working orders" rather than skipping silently.

5. **Run a web search** for sponsor / deal / mandate context. Issue `web_search` queries such as:
   - `"<SPAC full name>" SPAC merger` — catches deal rumors, BCA announcements, recent press
   - `"<SPAC full name>" IPO` — catches Renaissance Capital / IPO Edge / Bloomberg coverage of the IPO
   - `"<Chairman name>" net worth` or `"<Chairman name>" Forbes` — confirms billionaire status if relevant
   - `"<Sponsor entity>" SPAC track record` — surfaces prior-SPAC outcomes (e.g. BowX → WeWork bankruptcy)
   - For pre-deal names with quiet 8-K activity, also try `"<SPAC ticker>" target` or `"<SPAC name>" rumored` — sometimes deal-track press leads the filings.
   - If web search returns nothing useful, that's also information — record it. Do not invent deal speculation.

6. **Confirm the ticker is correct**. If the user gave you a ticker that doesn't resolve in `MeteoraMCP-AWS:spac-details` AND doesn't return EDGAR filings AND doesn't appear in web search, surface the ambiguity to the user before continuing. Many SPACs have a separate registration ticker (e.g. "CRA") vs. the Bloomberg/internal ticker (e.g. "CRAQ") — note both and confirm which Bloomberg ticker resolves via `get-price`.

7. **Franchise enumeration sweep** (REQUIRED for any SPAC sponsored by a known franchise: Cantor / Cantor Equity Partners, Churchill, Ajax, Pono, Replay, Forest Road, Compass, Tishman Speyer, Aldel, Replay, etc.). This step exists to enforce Core Principle 14 — exhaustive franchise vehicle enumeration — and to enable Core Principle 13 — comparative diligence against the immediately-prior sibling. Do all of:
   - **EDGAR CIK family sweep**: pull EDGAR filings for adjacent CIKs in the same numeric neighborhood as the target SPAC's CIK (franchise CIKs are typically clustered numerically — e.g., CEPF CIK = 2034267, CEPV CIK = 2034266 are consecutive). Identify every CIK with a sponsor-entity name matching the franchise pattern (e.g., "Cantor Equity Partners", "Cantor EP Holdings"). Pull the most recent S-1 / 8-K / 10-K filing for each to confirm whether each is pre-IPO shell, in-flight IPO'd, in-deal, completed deSPAC, or liquidated.
   - **Franchise IR archive web search**: `"<Franchise name>" SPAC 2025`, `"<Franchise name>" SPAC IPO`, `"<Franchise name>" deSPAC`, `"<Sponsor parent>" PIPE 2025`, `"<Sponsor parent>" anchor investor` — catches own-sponsored vehicles AND franchise-adjacent precedents (sponsor as PIPE / FPA / anchor / UW on third-party deSPACs).
   - **Pull the immediately-prior franchise sibling's memory doc** (or its S-1 if no doc exists): `MeteoraMCP-AWS:read-memory-doc(name="<PRIOR_SIBLING_TICKER>")`. Capture: per-share trust, per-share at-redemption overfund (if any), right ratio, founder share count per dollar of trust, extension cadence, OA size and exercise terms, mandate language, sponsor structure (single-sponsor vs syndicated at-risk capital), at-risk capital syndication terms.
   - The output of this sweep feeds directly into the Risk Factors / Atypical Features section (comparative deltas vs prior sibling) and the sponsor track record section (full enumeration). If this sweep is skipped, both sections will be incomplete — that's the failure mode to avoid.

---

## Phase 1 — S-1 Extraction (Pillar 1)

The goal is the same regardless of source: a 9-section structural extraction of the SPAC's IPO terms.

### Path A — PDF attached

Run the firm's `spac-s1-extraction` skill. That skill does `pdftotext -layout` extraction from the uploaded PDF and produces:
- Part 1: 9-section structured extraction (Overview, Offering, Trust, PP/Promote/Anchor, Sponsor/Admin Fees, Underwriter, Lockup, Target, Sponsor Team).
- Part 2: Investment summary with risk-factor / atypical-feature findings, sponsor info, mgmt table.

The output is what gets logged as the first entry in the doc.

### Path B — No PDF attached, pull from EDGAR

This is the alternative we've explicitly added. Workflow:

1. **Find the most recent S-1 filing** via `MeteoraMCP-AWS:edgar-filings(ticker="<TICKER>", form_type="S-1", limit=20)` and `MeteoraMCP-AWS:edgar-filings(ticker="<TICKER>", form_type="S-1/A", limit=20)`. If neither returns results, also try `form_type="DRS"` and `form_type="DRS/A"` (confidential submissions if the company has gone effective).

2. **Identify the operative filing**. The most recent S-1/A supersedes the original S-1. Compare against any prior amendments to track structural changes (right ratio, offering size, mandate, auditor) — those mid-registration changes are themselves diligence findings.

3. **Pull the full text** via `MeteoraMCP-AWS:edgar-filing-text` with the filing URL. Use `summary: True` for initial orientation if the filing is large; then targeted fetches with `offset` + `max_chars` for specific sections. Typical SPAC S-1 sections live at:
   - Cover page / pricing table → first 5,000 chars
   - Risk Factors → 10,000-25,000 chars
   - Use of Proceeds + Capitalization → 25,000-35,000 chars
   - Sponsor Information / Management → 35,000-55,000 chars
   - Underwriting → 75,000-90,000 chars
   - Description of Securities → 90,000-110,000 chars
   - Certain Relationships / Related Party → 110,000-130,000 chars

4. **Pull the exhibits** if the body references them. `MeteoraMCP-AWS:edgar-filing-index(accession_number=...)` returns the document inventory; key exhibits for a SPAC S-1 are:
   - EX-1.1 (Underwriting Agreement)
   - EX-3.1 / EX-3.2 (Articles)
   - EX-10.x (Sponsor Letter Agreement, Trust Agreement, PP Subscription Agreement, Registration Rights, Admin Services Agreement)
   - EX-99.x (Consent letters from auditors / IDs)

5. **Apply the same 9-section structure** as `spac-s1-extraction` would produce. The output should be indistinguishable in shape from a PDF-sourced extraction. The only difference is that EDGAR-direct extraction lets you cite exact accession numbers and URL references, which is actually a small upgrade over PDF-sourced.

6. **Compare to prior amendments** if any exist. Capture the filing track:
   - DRS confidential submission date(s)
   - Original S-1 file date + offering size + right ratio
   - Each S-1/A amendment with date and material changes
   - Any auditor change (look for 8-K Item 4.01 or filing-track auditor disclosures)
   - Any mandate change (compare cover-page mandate language across amendments)

This filing-track comparison is one of the most valuable diligence outputs. A name that has gone DRS → S-1 → S-1/A No. 1 → No. 2 → No. 3 over 7 months with right-economics richening + mandate scrub + auditor change is telling you something the PDF-only path doesn't surface.

### Pillar 1 output

Whichever path was used, the entry that gets written to the doc is the **9-section structured extraction + investment summary**. Tag: `diligence`.

---

## Phase 2 — Trading Note + Tape (Pillar 2)

### Path A — Bloomberg-traded SPAC

Run the firm's `trading-note-extended` skill. That skill produces:
- Live Bloomberg prices (common, warrant, rights, USGG3M)
- VWAP-centered yield matrix (±1c/±2c/±3c plus bid/ask)
- Extension deposit modeling from EDGAR 8-Ks
- EDGAR-verified S-4/F-4 count (in-deal only)
- Thesis line (will be empty for a freshly-seeded doc — that's expected; the doc won't have a summary yet)

In addition to the trading-note-extended output, the Pillar 2 entry for a seed MUST include:

**(a) Sheet-vs-Bloomberg price reconciliation.** Compare every price column in the MeteoraMCP-AWS:spac-details payload (common_price, warrants_price, rights_price, unit price if present, vwap_5d) against the live Bloomberg mid. If any sheet price disagrees with Bloomberg by more than 5%, call it out explicitly — note the sheet value, the Bloomberg value, the percentage delta, and the corrected position-value math. This is a real data-integrity finding that should go in the entry, not be silently swallowed.

**(b) Live EMSX blotter snapshot from Phase 0.** Embed the working orders + recent fills directly into the entry: side, ticker, amount, limit_price, working/filled/idle, broker, route status, GTC vs DAY, last update timestamp. Reconcile order limit prices against live Bloomberg — orders sitting far from market warrant a comment ("$0.25 working sell vs $0.21 ask = above market, deliberate" or "$10.31 working sell vs $10.25 ask = above market, position housekeeping" or "stale order, worth raising with trader").

**(c) Recent filing track since IPO.** Pull the last 8 EDGAR filings and summarize what's there and — equally important — what's missing. Long stretches of 8-K silence (no extension activity, no auditor change, no sponsor structure update) are themselves diligence findings. So is a heavy 13G filer cluster (institutional SPAC-arb accumulation).

### Path B — Pre-effective / Bloomberg-unresolvable

If `get-price` returns nothing for the ticker (pre-IPO, not yet effective), produce a structural-only output instead:

```
=== TAPE (PRE-EFFECTIVE) ===
TICKER: <TICKER>
Status: Pre-effective; no Bloomberg ticker resolution; no EMSX activity.
Filing track: <pull from Phase 1 — DRS/S-1/S-1/A dates + sizes + right ratios>
Trust per share (target): $<from S-1>
Extension cadence (target): $<per share> / $<total per month> for up to <N> extensions
Sponsor offshore structure: <BVI/Cayman/etc.>
UW: <name + tier>
PIPE/anchor: <none disclosed / $X named>
Auditor: <current>; prior auditor changed <date> if applicable
Counsel: <SPAC US / target / UW>
```

Note explicitly that the tape will be re-checked when the IPO prices and the sheet entry is created. Tag: `filing`.

### Pillar 2 output

The trading note (Path A) or the pre-effective structural snapshot (Path B). Tag: `filing` for either path.

---

## Phase 3 — Team Bios (Pillar 3)

Run the firm's `spac-bios` skill. That skill produces:
- Long-bullet executive summary per principal (exits / fund AUM / billionaire status / PIPE-raise track record / loaded adjacencies / career one-liner)
- Per-person 9-section deep dive
- Network map across the team
- Red flag register
- Open questions

Specific to this seed-memory orchestration:
- Pull the principals list from the Phase 1 extraction. Do not re-extract from the S-1 — Phase 1 already did that.
- **Mandatory: enumerate the FULL board roster, not just the most-recently-appointed ID.** Pull from BOTH (a) the S-1 management section "Officers, Directors and Director Nominees" table, AND (b) every subsequent 8-K Item 5.02 director-appointment / officer-change filing in EDGAR. The S-1 lists original IPO-effective IDs (typically 2–3 named "Director Nominees" who take their seats at trading commencement); 8-Ks add or replace IDs over time. Naming only the latest 8-K appointment (or only IDs the user mentioned) and missing the IPO-original IDs is the single most common Pillar 3 failure mode and routinely gets caught only on user feedback. Concretely: for any SPAC, the management table is in the S-1 management section under "Officers, Directors and Director Nominees" with names, ages, and titles; the bios that follow give role tenure, prior-SPAC seats, employment history, and education. For 8-Ks, filter `MeteoraMCP-AWS:edgar-filings` with `form_type="8-K"` and read each one whose description includes director appointment / officer change / Item 5.02. Bio every director, including footnote-only "Director Nominees" — they ARE directors as of trading commencement. The ONLY acceptable reason to skip a named director is if subsequent 8-Ks confirm they resigned before trading; in that case, note both the appointment and the resignation in a brief one-line footnote rather than omitting them.
- **Mandatory: mine the CFO and CEO bios in the S-1 management section as the PRIMARY source for legacy franchise enumeration.** When a SPAC officer has prior-SPAC tenure (very common for franchise sponsors — e.g., Cantor's Jane Novak, Churchill's Glenn Hutchins, Pono's various), their S-1 bio enumerates each prior SPAC with named tenure dates AND named outcomes inline: `"served as Chief Financial Officer of CFAC III from July 2021 until consummation of its initial business combination with AEye in August 2021, as Chief Financial Officer of CFAC V from July 2021 until consummation of its business combination with Satellogic in January 2022"` — every clause is a primary-source legacy-vehicle datapoint with target name + close date or liquidation date. EDGAR CIK family sweep finds the entities; the officer-bio tenure list reveals the OUTCOMES. Read the CFO bio carefully and capture every prior-SPAC tenure clause. Failing to mine this list is how 4 of 7 legacy CFAC vehicles (AEye, Satellogic, Rumble, CFAC VII liquidation) get missed in a Cantor seed despite the data being in the document Phase 1 already pulled.
- Use any Phase 1-discovered context (mandate scrub, auditor change, mid-registration right richening) to inform §9 synthesis.
- If a sub-component requires Bloomberg historical (e.g., a CEO's prior public-co tenure performance), use `MeteoraMCP:get-price` with the relevant ticker and date range. This is in-scope for Pillar 3.
- **Always pull current Bloomberg prices on every consummated prior-SPAC deSPAC ticker** before assigning a quality grade. Read the OUTCOMES-RUBRIC memory doc and grade per Core Principle 16 — the BETTER of highest sustained band and current price, plus the qualitative capital-formation overlay. Do not grade from training-data priors — `Rumble` may be a "good" outcome at $8 today even if it deSPAC'd at $10; `AEye` may be "poor" at $2 even if it had a $1B valuation at deSPAC. Batch the price calls into a single `get-price(tickers=[...])` invocation across all the franchise's consummated deSPAC tickers.
- **Always supplement S-1 bios with web search.** S-1 disclosures are minimum-required and frequently understate (or whitewash) prior-SPAC outcomes, contested public-co tenures, or wealth/network color. For each named principal, run web search for: `"<full name>" Forbes`, `"<full name>" net worth`, `"<full name>" CEO <prior company>`, `"<full name>" SPAC`, plus any specific prior-SPAC ticker that surfaced in the S-1. This is what makes the difference between a doc that says "Mr. X founded TIBCO" and one that says "Mr. X founded TIBCO, sold to Vista for $4.3B in 2014, owns the Sacramento Kings, and rolled the BowX → WeWork SPAC that bankrupted in 2024." The latter is what the memory doc should look like.

### Pillar 3 output

The full spac-bios output. Tag: `diligence`.

---

## Phase 4 — Doc Assembly

This is where the three pillars become a doc.

### Step 4.1 — Create the doc

Call `MeteoraMCP-AWS:create-memory-doc(name="<TICKER>", author="Claude")` with NO seed summary. The summary will be written at the end of this phase via `MeteoraMCP-AWS:update-memory-summary`.

If the call returns `already_exists`, stop — Phase 0 should have caught this, but treat it as a fail-safe.

### Step 4.2 — Write Pillar 1 entry

`MeteoraMCP-AWS:update-memory-doc` with:
- `name`: ticker
- `tag`: `diligence`
- `author`: Claude
- `body`: the full Phase 1 output (9-section extraction + investment summary). If the body exceeds ~10k chars (the tool limit), split into "Part 1 of 2 — sections 1-5" and "Part 2 of 2 — sections 6-9 + summary" entries.

### Step 4.3 — Write Pillar 2 entry

`MeteoraMCP-AWS:update-memory-doc` with:
- `tag`: `filing`
- `body`: the full Phase 2 output (trading note OR pre-effective structural snapshot).

### Step 4.4 — Write Pillar 3 entry

`MeteoraMCP-AWS:update-memory-doc` with:
- `tag`: `diligence`
- `body`: the full Phase 3 output. Will almost always exceed 10k chars; split into multi-part entries: "Team deep dive — Part 1/N — Executive Summary + aggregate", "Part 2/N — [Person 1] + [Person 2]", etc.

### Steps 4.4b–4.4d — Write the in-deal pillar entries (in-deal seeds only)

Run these ONLY when Phase 0 detected `stage="indeal"`. Skip entirely for pre-deal seeds.

- **Step 4.4b — Write Pillar 4 entry (S-4/F-4 extraction).** `MeteoraMCP-AWS:update-memory-doc` with `tag: filing`, `body`: the full Phase 1B `spac-s4-extraction` output. Split if >10k chars. If the CP22 3-pass discovery (SPAC CIK + holdco / merger-sub CIK + target CIK) confirms no S-4/F-4 is filed yet, skip this entry and note the deferral in the Pillar 6 / summary "On the horizon."
- **Step 4.4c — Write Pillar 5 entry (deal review).** `MeteoraMCP-AWS:update-memory-doc` with `tag: diligence`, `body`: the full Phase 3B `spac-deal-review` output.
- **Step 4.4d — Write Pillar 6 entry (Target Dossier).** `MeteoraMCP-AWS:update-memory-doc` with `tag: diligence`, `body`: the full Phase T Target Dossier (company history since inception, funding rounds, comps, lineage, valuation inputs — per `references/in-deal-summary.md` Part 1). Split into "Target Dossier — Part 1/N — Company history + funding", "Part 2/N — Comps + lineage + valuation" if >10k chars.

### Step 4.5 — Compose and write the Executive Summary

This is the synthesis step. The summary is the single document a reader needs to fully understand the name.

**Branch on stage first:**
- **Pre-deal seed** → compose from the three pillars using the pre-deal template in THIS step (below).
- **In-deal seed** → STOP and read `references/in-deal-summary.md` in full, then compose the deal-focused summary per its Part 2 template, synthesizing across all six pillars. Do NOT use the pre-deal template below for in-deal docs — the focus shift in CP20 is mandatory (target is the lede; sponsor collapses to PIPE-raising track record). After composing, write it via `MeteoraMCP-AWS:update-memory-summary` (two-step interface; skip the prompt-fetch step) exactly as the pre-deal path does at the end of this step, then proceed to Step 4.6 (email) unchanged.

The remainder of this step is the PRE-DEAL template. Compose it from all three pillars' findings using this structure.

**The pre-deal section list below is closed.** The allowed subsections are exactly the ones enumerated in the template — One-line view, Structure, Risk Factors / Atypical Features, Sponsor team, Sponsor track record, Relationships & Coverage, Filing track, Position, Trade view, On the horizon. (The in-deal closed list is different and lives in `references/in-deal-summary.md` Part 2.) Do NOT add a Verdict Block, At-a-glance, Snapshot, Quick view, Status, Cover row, Header bullet, "TL;DR", Warrant/SPAC cohort comparison block, or any other extra subsection on top of these — extras bloat the summary, duplicate content, and create structural pressure to compress into tape-style framing. Brief structural compressions belong in the One-line view, which exists for that purpose. See Core Principle 11 sub-rule (b).

```markdown
## Executive Summary

**[TICKER] — [Full SPAC Name] ([Exchange]; [Domicile — e.g. Cayman Islands exempted, BVI, Delaware]; CIK [10-digit CIK from EDGAR — e.g. 0002034266]; [pre-IPO / post-IPO]; S-1/A No. <N> filed <date>; [effective / not yet effective])**

**One-line view:** Bucket [<sheet bucket from MeteoraMCP-AWS:spac-details, verbatim — e.g. 1.5>] — [tier-N UW], [anchor status if any], [domain fit assessment]. [Pre-deal / post-deal] [trade view in one phrase]. NOTE: NO trading characterization here, even as a brief phrase. Forbidden: `"trades at/near trust on thin volume,"` `"trades at a discount,"` `"premium to trust on illiquidity,"` or any liquidity/premium/discount/volume framing. The One-line view captures durable structure + thesis only. See Core Principle 11. Per CP24, the absence of a committed PIPE is the pre-deal norm — it never appears here (or anywhere in the doc) as a negative.

**Structure:** *(every figure below verified at write time against the latest operative registration filing — 424B4 if priced, else the newest S-1/A / F-1/A — per CP25)*
- Offering: [units × $price = $size]; unit = [composition]; [OA size + days].
- Trust: $[total] / $[per unit] ([overfund — e.g., "$0.20/share, OR explicitly "no per-share overfund at redemption, unlike prior franchise sibling [TICKER] which had $0.15/share" if the comparative finding holds]). [Trustee/bank].
- Timeline: [base months] + [extensions] @ [$ per month] = [max months]. [Public vote / no public vote on extensions].
- At-risk capital: [Sponsor private placement: units × $ = $]. [Whether the at-risk capital is wholly sponsor-funded OR syndicated to non-managing members; if syndicated, named co-investors / family offices / anchor LPs and aggregate $ they put in + key terms (liquidation preference vs founder shares, side-letter rights, lock-ups, forfeiture). Wholly sponsor-funded is the default; syndication is material structural detail that affects sponsor incentive alignment and target-search behavior.]
- Promote: [shares] (~[%] post-IPO). [Single-class / Class A/B] structure.
- Lockup: [terms].

**Risk Factors / Atypical Features ([N]):**

Each finding must be deal-specific, material, and differentiating — see Core Principle 12. Universal SPAC features (Class B Consent Right, sole-UW = sponsor affiliate, sponsor-controlled board pre-BC, 20% promote) are NOT findings. Filing-mechanic observations (number of S-1 amendments, registration cycle length) are NOT findings unless tied to a substantive material change. Liquidity profile is NOT a structural finding — it's a position-management consideration noted in the Trade view if relevant. The section earns its name; pad-content findings dilute the real ones. Findings can be either **risk factors** (genuine negatives — sponsor track record problems, restatement footnotes, terminated prior PIPEs) or **atypical features** (structural deviations from the SPAC norm that may be neutral or positive — right-ratio richening from 1/10 → 1/4, an added per-share overfund, a richer-than-typical extension cadence, etc.). Both polarities belong here; the section name reflects that scope.

The richest source of findings in franchise SPACs is comparative diligence against the immediately-prior franchise sibling — see Core Principle 13. Specifically check for:
- Per-share overfund / at-redemption kicker added or removed vs prior siblings (e.g., `"no $0.15 per-share at-redemption overfund, unlike CFFE I/II/III which had it"` — high-impact actionable finding routinely missed because the omission isn't called out in the S-1).
- Right-economics richening or degradation (1/10 → 1/4, etc.).
- Founder share count per dollar of trust (a tighter or looser sponsor economic).
- Extension cadence step-ups or step-downs ($/share/month).
- OA size or terms.
- Mandate scrubs across amendments.
- Auditor changes.
- Sponsor structure changes (single-sponsor vs syndicated at-risk capital, GP-led vs strategic-sponsor).

Finding-writing rule: if Claude can't articulate the differentiation in a single clause ending in "...unlike [SPAC norm or prior franchise sibling]", the item does not belong here.

1. [Top finding — written in the form: `"X — [implication for thesis/sizing/exit], unlike [SPAC norm or prior franchise sibling]"`]
2. ...
[List up to 8 most significant findings across all three pillars. Quality over quantity — 3 real findings beats 6 padded ones.]

**Sponsor team (substantive bios — restate in full, do not cross-reference peer docs):**

For each principal — CEO, CFO, AND every named director (independent and otherwise) AND every co-sponsor — produce a multi-sentence bullet covering all of the elements below. The director slate must be COMPLETE: pull from the S-1/F-1 management section AND every subsequent 8-K Item 5.02 director-appointment filing. Naming only the most-recent ID appointment (or only the IDs that came up in the user's prompt) is wrong — the full board roster is durable structural context. Even when this SPAC is the n-th vehicle in a franchise with the same officer slate as a sister doc, restate the bio in full here. "Same officer as [peer ticker]" is wrong — downstream skills read each doc in isolation.

Per-principal elements (every bullet must touch all that apply):
- **Role + tenure**: title at the SPAC, when they joined the sponsor org, age/career stage if relevant.
- **Most-prominent prior achievements**: named exits with deal size + acquirer + year; public-co tenures with ticker + dates + Bloomberg-confirmed performance signal (drawdown, rally, bankruptcy); fund AUM if a GP; named prior-SPAC outcomes including liquidations and bankruptcies.
- **Network / franchise context**: family relationships, board overlaps with co-principals, prior-SPAC director-rotation pattern if a "house ID," sponsor-affiliated public-co board seats (BGC, Newmark, Ajax-tier conglomerate boards, etc.).
- **PIPE-raise track record**: named prior closing raises — deal, size, date, redemption backdrop, named anchors — including adjacent-precedent roles (PIPE / FPA / anchor / UW on third-party deals). When none exists: `no prior closing PIPE on record`, a neutral fact, not a caution. Never a speculative very-high/high/moderate/low capability rating and never a claim of absent ability (CP24).
- **Red flag if any**: one concrete flag from the bios output (litigation, contested tenure, undisclosed adjacency, political exposure, etc.). If clean, say so.

Format: one bullet per principal, multi-sentence prose. A 5-person team is 5 substantial bullets, not 5 one-liners. Aim for ~3-6 sentences per principal — more for a vice-lede CEO with a billionaire-scale network or a contested public-co tenure, less for a clean-record audit-chair ID.

Cut color and irrelevant biographical detail — see Tips section. Anecdotes (9/11, family origin stories, foundational-trauma narratives), career color beyond what's structurally relevant, and historical events even when cinematically compelling do not belong in the summary. Keep what bears on the PIPE-raise track record, deal-sourcing capability, exit track record, public-co tenure performance, network depth, and conflicts. The Pillar 3 entry can carry color; the summary should not.

[Worked example shape — Brandon G. Lutnick on a Cantor vehicle:]
- **Brandon G. Lutnick (Chairman & CEO):** Joined Cantor Fitzgerald April 2022; promoted to Chairman & CEO of Cantor February 2025 at age ~28, the moment his father Howard Lutnick became U.S. Secretary of Commerce in the Trump administration. Personal exit/operating track record is thin (early-career), but inherits one of the deepest financial-services networks in the U.S. — Cantor parent + BGC Group (NASDAQ:BGC) + Newmark Group (NASDAQ:NMRK), all family-controlled. Father Howard led Cantor 1992-Feb 2025 (33 years) and built it from a single trading partnership into a financial-services and real-estate conglomerate; Howard's network is the firm's network. PIPE-raise track record: very high for digital assets / financial services / real-estate-services targets (Twenty One Capital BTC-treasury deSPAC Dec 2025 demonstrates capability in crypto vertical specifically); moderate for healthcare. Red flag: Cabinet-level political exposure via Howard creates conflict-of-interest optics on any cross-border or trade-policy-sensitive target — Cantor has publicly stated Howard divested operational control upon assuming the Cabinet role, but the optics linger.

**Sponsor track record (named vehicles, named outcomes — do not cross-reference peer docs):**

For SPAC sponsors with any prior vehicles, list each prior SPAC vehicle by name with the elements below. This applies to franchise sponsors (Cantor, Churchill, Ajax, Pono, Replay, Forest Road, etc.) and also to one-off sponsors with a single prior SPAC. Skip this section ONLY if the principals have no prior SPAC history at all.

Enumeration must be EXHAUSTIVE — see Core Principle 14. Sweep EDGAR CIK family search (franchise CIKs are usually clustered numerically), the franchise's IR archive, and news archive. List every vehicle in the franchise's history: pre-IPO shells with registered S-1s but not yet priced, in-flight IPO'd siblings (CEP I/II/III/IV/V/+, CFFE I/II/III/+, Churchill VI/VII/+, etc.), in-deal vehicles, completed deSPACs (with PubCo names + dates + outcomes), liquidated vehicles. Listing only the vehicles that came up in conversation is a known failure mode. `"CEP II / CEP III not confirmed"` is NOT an acceptable data gap deferred to "On the horizon" — resolve it before writing.

Beyond own-sponsored vehicles, also list franchise-adjacent precedents: deSPAC transactions where the sponsor served as PIPE provider, FPA provider, anchor investor, or deSPAC underwriter without sponsoring the SPAC itself (e.g., Securitize for Cantor). These adjacent precedents demonstrate vertical capability and pipeline depth and routinely matter more than own-sponsor track record for assessing PIPE-raise track record — they are not optional.

Per-prior-vehicle elements:
- **Vehicle name + IPO or board-formation date**
- **Outcome**: deSPAC consummated → name of PubCo + close date + post-deSPAC performance signal (price action, bankruptcy, delisting); OR liquidated → date + return-to-trust signal; OR active → current status.
- **Quality grade**: canonical label only — strong / good / mediocre / poor / failed — graded per CP16 / the OUTCOMES-RUBRIC memory doc on peak-and-current tape plus capital formation, with both factors stated in the grade line.
- **Role (for adjacent precedents only)**: PIPE / FPA / anchor / UW / strategic equity.

Then aggregate franchise metrics — every line gets a hard value or an explicit "n/a verified". Numbers asserted MUST be directly verifiable from the enumerated vehicle list above; do not assert cadence numbers like `"2 vehicles in last 10 weeks"` without computing them from the list. Hallucinated cadence numbers are a known failure mode — see Core Principle 14.
- **Consummation hit rate**: [N consummated / M total prior vehicles] = [%]. Computed from enumerated list — show the math.
- **Quality of consummated deals**: one sentence — "1 strong (Twenty One Capital BTC treasury), 1 mediocre (XBP), 1 poor (View)".
- **Forbes-listed billionaires affiliated with the sponsor**: count + names + source (e.g., "Howard Lutnick — controlling Cantor + BGC + Newmark wealth, Forbes-billionaire scale").
- **Institutional-backer / anchor / PIPE relationship depth**: named institutional relationships demonstrated on prior deals (e.g., `"$X PIPE backstop on Twenty One Capital led by [LP]; named anchors on prior franchise deals: [list]; FPA counterparties: [list]"`). This is the metric that bears on PIPE-raise track record — parent revenue is NOT a substitute. Skip parent revenue unless it is the only available signal; the question we care about is who shows up to fund the next deal, not how much top-line the parent does.
- **Public-co board exposure of principals outside the SPAC**: count + key seats (e.g., "BGC director slate, Newmark director slate").
- **Recent SPAC IPO cadence**: how many SPACs the franchise has IPO'd in last 12 months and at what aggregate trust size — verify the count against the enumerated vehicle list before asserting.
- **PIPE-raise track record**: named raises with sizes, dates, redemption backdrop, and anchors (a named PIPE / FPA / backstop on a prior deal counts; pure assertion of “deep network” does not — distribution-network context is recorded alongside the record, not in place of it). State `no prior closing PIPE on record` neutrally when that is the fact; no speculative capability ratings (CP24).

[Worked example shape — Cantor Equity Partners franchise:]
Prior own-sponsored vehicles:
- **CF Finance Acquisition Corp. II** (board-formed late 2020) → **View, Inc.** consummated March 2021 (smart-glass company); post-deSPAC outcome poor — meaningful drawdown post-close. Quality: poor.
- **CF Acquisition Corp. IV** (board-formed Dec 2020) → **liquidated December 2023** — failed to find a target during the SPAC bust window; capital returned to shareholders. Quality: failed.
- **CF Acquisition Corp. VIII** (board-formed March 2021) → **XBP Global / XBP Europe** consummated November 2023 (document-management business in Europe); post-deSPAC outcome in the $4–$7 band. Quality: mediocre.
- **Cantor Equity Partners, Inc. (CEP I)** (board-formed Aug 2024) → **Twenty One Capital, Inc.** consummated December 2025 (Bitcoin treasury vehicle); the franchise's most recent and most relevant reference deal — confirms ability to deploy in the digital-assets vertical quickly. Quality: strong.
- [+ all other CEP / CFFE / CF Acquisition vehicles surfaced via EDGAR CIK family sweep — pre-IPO shells, in-flight, etc.]

Adjacent precedents (sponsor as PIPE / FPA / anchor / UW, not as sponsor):
- **Securitize** (deSPAC, [date], [PubCo / Class A ticker]) — Cantor as [role; e.g., PIPE provider / deSPAC underwriter]. Demonstrates digital-assets vertical capability beyond Twenty One Capital.
- [+ other adjacent precedents surfaced via news / IR archive sweep]

Aggregate:
- Consummation hit rate: [N consummated / M total enumerated] = [%]. (Compute from enumerated list above.)
- Quality of consummated deals: [enumerate by quality grade].
- Forbes-listed billionaires affiliated: [count + names + source].
- Institutional-backer / anchor / PIPE relationship depth: [named PIPE backstops on prior deals; named anchors; FPA counterparties]. Do not substitute "Cantor parent revenue is multi-billion" — that's not the metric we care about.
- Public-co board exposure of principals: [BGC director slate, Newmark director slate, plus active SPAC vehicles].
- Recent SPAC IPO cadence: [computed from enumerated vehicle list — e.g., "3 vehicles IPO'd in 2025: CEPF 8/2025 $400M + CEPV 11/2025 $220M + CEPS [date] [size]; aggregate $X trust raised"]. Verify against enumerated list before asserting.
- PIPE-raise track record: [named raises by vertical — deal, size, date, redemption backdrop, anchors].

**Relationships & Coverage:**

Per Core Principle 23. Capture coverage and contact intelligence that a desk trades on; keep durable facts evergreen, date any in-flight workflow items, and hold NO tape (coverage ≠ posture). Omit gracefully — if nothing beyond the underwriter is known, this is a single line. Attribute desk-sourced intel with name + date (CP21).
- Deal / sell-side coverage: [bank(s) that ran the IPO; sell-side desks that cover Meteora on the name — StoneX / Cantor / Clear Street / BTIG / Jefferies / etc., if known].
- Named contacts: [person — role/affiliation — email domain if known; e.g. "Janet — sell-side coverage on the name (reconnect pending)"].
- Sponsor / cross-name linkage: [other SPACs sharing this sponsor or a sponsor-adjacent contact set; e.g. "shares sponsor with [TICKER]; both reached at @[domain]"].
- Introduction / relationship status (dated): [in-flight intros, who is making them, access constraints; e.g. "intro in progress — [person] → [person] ([firm]); (M/D)"].

**Filing track:**
- [DRS/S-1/S-1/A timeline with sizes + right ratios at each step]
- Mandate scrub (if any): [original mandate] → [current mandate]
- Auditor change (if any): [prior] → [current], [date]

**Position:**
- Common: [share count] shares. ~[%] of [public float / total Class A outstanding].
- Rights: [count if applicable]. Warrants: [count if applicable].
- Concentration framing: report `"~X% of public float"` as durable factual context. Compliance flag ONLY if approaching or exceeding 9.9% of public float — see Core Principle 15. Below 9.9%, do NOT flag the 5% Schedule 13G threshold as an action item; it's administrative.
- Position dollar mark is omitted from the summary — current MV goes stale; it lives in the timestamped Pillar 2 entry.

(NOTE: There is no Tape section in the summary. Tape data — bid/ask, yields, spreads, volumes, current MV — goes stale within days and lives in the timestamped Pillar 2 entry. See Core Principle 11.)

**Trade view:** [thesis-derived posture, NOT tape-driven and NOT a reflexive HOLD — derive the posture from the thesis + structure + rubric read. Below-trust common on a name the desk wants is an accumulate framing with a size objective; a rubric-successful franchise argues for building, not parking. Posture only for legs held or targeted (CP17); durable phrasing that survives a 6-month re-read. e.g.: `"ACCUMULATE common below trust toward [size objective] — trust-arb with [franchise] optionality; warrants: no adds above [level] absent a deal; pair-trade context vs sister vehicle [TICKER]."` Do NOT write `"premium of +1c will compress on..."` or any other tape-dependent claim.]

**On the horizon:**
- [Next gating event — IPO pricing, S-4 filing, vote, deadline. Define any internal jargon parenthetically — e.g., `"18-month soft deadline (the date by which the sponsor expects to consummate; extensions available to push to the hard 24-month deadline)"` — see Tips section.]
- [Any data gaps from this seed — e.g. `"Pillar 2 will be re-run when IPO prices"`. NOTE: missing franchise-vehicle enumeration is NOT an acceptable data gap; resolve before writing per Core Principle 14.]
- [Open questions to monitor — pull from Pillar 3 open questions list]
- [Compliance flag ONLY if approaching 9.9% — see Core Principle 15. Do NOT flag 5% Schedule 13G threshold; that's administrative.]
- [Bucket revision ONLY if the desk explicitly directed one in a transcript / email captured in the doc — record as `Bucket revision per desk ([name], [date]): [old] → [new]` (CP9/CP21). Claude does not propose bucket revisions; omit this bullet otherwise.]
```

Then call `MeteoraMCP-AWS:update-memory-summary` twice:
1. First call: `name="<TICKER>"` with no `new_summary` — returns the prompt for rewriting (which we ignore since we're seeding, not rewriting).
2. Second call: `name="<TICKER>"`, `new_summary=<the composed summary above>`. This writes the summary to the doc.

**Bucket sourcing rules for the One-line view:**
- Pull `bucket` from `MeteoraMCP-AWS:spac-details(ticker=<TICKER>)` and quote it verbatim in the one-line view ("Bucket 1.5", not "B/B+ tier" or any letter equivalent).
- Pre-effective SPACs not yet in the sheet have no bucket — write "Bucket [pre-sheet — not yet ranked]".
- Claude never proposes a bucket revision (CP9). The doc records one only when a desk transcript / email captured in the doc explicitly directs it, attributed and dated per CP21. Findings that bear on quality are stated factually in their own sections and left for the desk to weigh.
- Never alter the sheet bucket cited in the body of the summary. Downstream skills (`trading-note-extended`, `spac-deal-review`, `spac-ai-agent`) read the one-line view and need the sheet value there for consistency across the universe.

### Step 4.6 — Email the executive summary to the filings distribution list

After the summary has been written to the doc via `MeteoraMCP-AWS:update-memory-summary` in Step 4.5, email a nicely formatted HTML copy to `filings@meteoracapital.com` so the team has a snapshot alongside the canonical doc.

Call `MeteoraMCP-AWS:send-email` with:
- `to`: `["filings@meteoracapital.com"]`
- `subject`: `[<TICKER>] Memory doc seeded — <Full SPAC Name>` (e.g. `[CEPV] Memory doc seeded — Cantor Equity Partners V`)
- `content_type`: `"HTML"`
- `body`: the executive summary rendered as HTML — see formatting rules below.

**Markdown → HTML conversion rules.** The executive summary lives in the doc as markdown; the email body is rendered HTML. Apply these substitutions when composing the email body:

- The opening identifier line `**[TICKER] — [Full SPAC Name] (...)**` → `<h2 style="margin:0 0 16px 0; font-size:18px;">[TICKER] — [Full SPAC Name]</h2>` with the parenthetical metadata in a `<p style="color:#666; font-size:12px; margin:0 0 20px 0;">` immediately below.
- Section headers `**One-line view:**`, `**Structure:**`, `**Risk Factors / Atypical Features ([N]):**`, `**Sponsor team:**`, `**Sponsor track record (aggregate):**`, `**Relationships & Coverage:**`, `**Filing track:**`, `**Position:**`, `**Trade view:**`, `**On the horizon:**` → `<h3 style="margin:20px 0 8px 0; font-size:14px; color:#0a0a0a;">Section name</h3>`.
- Inline `**bold**` → `<strong>...</strong>`.
- Markdown bullet lists (`- ...`) → `<ul style="margin:4px 0 12px 20px; padding:0;"><li style="margin:4px 0;">...</li></ul>`. Preserve nesting.
- Plain paragraphs → `<p style="margin:8px 0;">...</p>`.
- Em-dashes, en-dashes, smart quotes, and parenthetical definitions preserved verbatim.
- Wrap the entire body in a single outer `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif; font-size:14px; line-height:1.55; color:#1a1a1a; max-width:820px;">...</div>` so it renders cleanly in Outlook web/desktop and Gmail.
- At the top of the body, immediately inside the outer `<div>`, prepend a small provenance header:

  ```html
  <p style="color:#888; font-size:11px; margin:0 0 16px 0; border-bottom:1px solid #eee; padding-bottom:8px;">
    Memory doc seeded for <strong>[TICKER]</strong> on [today's date — YYYY-MM-DD]. Source of truth is the memory doc; this email is an evergreen snapshot of the executive summary at seed time.
  </p>
  ```

**Content scope:** the email contains the executive summary ONLY. Do NOT include Pillar 1 / Pillar 2 / Pillar 3 entries in the email body — those live in the doc and are too long for an email. Do NOT include any tape data, live yields, or other point-in-time information beyond what is already in the evergreen summary (Core Principle 11 still governs).

**Pre-effective SPACs:** the email goes out even when the SPAC is pre-effective and Pillar 2 is the structural-only fallback. The summary still has substantive structure/team/sponsor content — that's what gets emailed.

**Failure handling:** if `MeteoraMCP-AWS:send-email` returns an error (transient Microsoft Graph issue, auth glitch, recipient validation), do NOT block on it — the doc has already been written and is the canonical artifact. Capture the error message and surface it in the Step 4.7 chat confirmation as `Email send to filings@: FAILED — <error>; please retry manually.` Do not silently swallow the failure.

### Step 4.7 — Confirm completion

Reply in chat with a short confirmation:
- Doc name + author + creation timestamp
- Number of entries written (should be 3-7 depending on splits)
- Length of executive summary
- Whether the filings@ email send succeeded (or the error if it failed)
- Any data gaps flagged
- One-line "Next steps for the user" (e.g. "Watch for IPO pricing 8-K to re-run Pillar 2 with live tape")

Do not paste the entire doc back into chat — the work is in the doc itself. The chat receipt is just confirmation.

---

## Phase U — Update Mode Workflow

Update Mode is invoked from Phase 0 when the doc already exists AND is actually seeded (a stub fails the Phase 0 check and routes to Seed Mode instead — existence ≠ seeded). The user's intent in invoking seed-memory on an existing doc is "refresh the executive summary to current guidance" — for example, after a Core Principle change (post-deSPAC quality rubric calibration, evergreen-summary ban on tape data, exhaustive franchise enumeration), or after the user spot-checks the existing summary and finds gaps. This is a first-class workflow; do not refuse, do not punt to `MeteoraMCP-AWS:update-memory-doc`.

The defining constraint of Update Mode is: **only the executive summary is rewritten, never the existing pillar entries.** Pillar entries are append-only history. If gaps are found in pillar entries (missing IPO directors, missing legacy vehicles, mis-graded outcomes), document the gaps via a NEW `correction`-tagged entry — do not edit prior entries.

### Step U.1 — Read the existing doc fully

Call `MeteoraMCP-AWS:read-memory-doc(name="<TICKER>", entries_limit=-1)` to pull the full doc — existing summary plus all entries. Read both carefully. The summary tells you what was previously asserted; the entries tell you what raw data was captured. Gaps in the summary are often reflected in gaps in the entries (e.g., if Pillar 1 listed only 1 of 3 IPO directors, the summary will too).

### Step U.2 — Run the gap-checklist against current guidance

Compare the existing summary against EVERY current Core Principle. The most common gap categories:

1. **Director enumeration (Core Principle on full board roster, Phase 3 mandatory step)** — Does the summary's Sponsor team section enumerate every director named in the S-1 management table AND every Item 5.02 8-K appointment since IPO? Pull `MeteoraMCP-AWS:edgar-filings(cik=<CIK>, form_type="8-K", limit=20)` and the S-1 management section to verify. IPO-original "Director Nominees" who took their seats at trading commencement are routinely missed if Pillar 3 only captured the most recent 8-K appointment.

2. **Franchise enumeration (Core Principle 14, plus Phase 3 officer-bio-tenure-list mandatory step)** — Does the summary enumerate every prior SPAC vehicle from the franchise? Re-mine the S-1 CFO and CEO bios for the prior-SPAC tenure list (every "served as CFO of [X] from [date] until consummation of its initial business combination with [Target] in [date]" clause is a vehicle). Cross-reference against the EDGAR CIK family sweep. Listing only vehicles that came up in conversation, or only the most-recent CEP-generation siblings while skipping legacy CFFE / CFAC names, is a known failure mode.

3. **Post-deSPAC outcome grading (Core Principle 16 / OUTCOMES-RUBRIC)** — Read the `OUTCOMES-RUBRIC` memory doc FIRST, then re-grade every prior consummated deSPAC on the peak-AND-current rule (the BETTER of the highest sustained band and the current price; pull live prices via batched `get-price(tickers=[...])`) plus the qualitative capital-formation overlay (winter-era / heavy-redemption / anchored closing raises weigh heavily; no dollar bright line). Sweep for the three legacy mis-grade patterns: (a) grades set on the current price alone that ignore a sustained higher band — or an above-trust current print that itself reads Strong; (b) viable low-price names graded “Failed” (Failed is structural only — bankrupt / delisted / liquidated); (c) rubric-successful outcomes (Good/Strong) still carrying drawdown narration or counts-against-the-sponsor color — compress to the grade + one factual present-state line. Re-grading against the current rubric is the highest-impact correction in any Update Mode pass.

4. **Tape-data leakage AND tape-characterization phrases (Core Principle 11, including sub-rules a + b)** — Does the summary contain any point-in-time data: bid/ask, today's volume, current yields, dollar mark on position, "trades at +1c premium today"? Equally important: does the summary contain ANY trading characterization, even as a brief phrase? Forbidden phrasings include: `"trades at/near trust on thin volume"`, `"trades at a discount with arb-desk participation"`, `"premium to trust on illiquidity, not signal"`, "thin liquidity", "extremely thin liquidity", "illiquid", "illiquidity", and any other liquidity / premium / discount / volume framing — all must be removed. Replace with durable structural language ("smaller deal size", "naked-common float of ~22M", "$220M trust") that survives the 6-month re-read. All tape data and tape characterization belong exclusively in timestamped Pillar 2 entries. Run a literal grep / mental scan for the words "trades", "premium", "discount", "liquid", "illiquid", "liquidity", "thin", "thick", "volume" in the summary; any hit outside structural context (e.g., "trust" / "trade view" / "trades at $X" inside a deSPAC quality grade) is a candidate for removal. **Additionally check for nested tape-data wrappers and extra subsections per CP 11 sub-rules (a) and (b):** does the summary contain a "Verdict Block", "At-a-glance", "Snapshot", "Quick view", "Status", "Cover row", "TL;DR", "Executive bullets at top", "Warrant cohort" / "SPAC cohort" comparison blocks, or any other subsection beyond the canonical section list (One-line view, Structure, Risk Factors / Atypical Features, Sponsor team, Sponsor track record, Filing track, Position, Trade view, On the horizon)? Inside any such wrapper, is there a `TAPE:` row, a "Current state" row, or any other row that stores bid/ask, current float, trust-per-share, redemption percentages, two-sided-market framing, or other tape data? Both the nested tape-bearing rows AND the entire extra-wrapper subsection (preamble line + all rows) must be patched out wholesale — empty `new_str` covering the whole wrapper. Do NOT try to "rescue" the wrapper by editing the TAPE: row to be more "structural" or by relabeling it; the structural element itself is the problem. Run a literal grep for "Verdict Block", "At-a-glance", "Snapshot", "TAPE:", "cohort" in the summary; any hit is a candidate for removal.

5. **Risk Factors / Atypical Features section (Core Principle 12, plus the section rename)** — Are the listed findings deal-specific, material, AND differentiating ("...unlike SPAC norm or prior franchise sibling")? Universal SPAC features (Class B Consent Right, sole-UW = sponsor affiliate, 20% promote) and tape-dependent observations (negative T-bill carry, illiquidity) are NOT findings. Position-management considerations are NOT findings. **Additionally check for the legacy section header "Bombs":** the section was renamed per CP 12 because "Bombs" is editorial color (CP 18-adjacent) and misleadingly narrow — the section captures both genuine risks AND atypical features that may be neutral or positive (e.g., right-ratio richening). When the existing summary has a `**Bombs ([N]):**` header, patch it to `**Risk Factors / Atypical Features ([N]):**` and sweep surrounding prose for `bomb` / `bombs` references (e.g., "Each bomb must be deal-specific" → "Each finding must be deal-specific"; "Bomb-writing rule" → "Finding-writing rule"; "Top bomb" → "Top finding"). Singular noun within the section is "finding"; preserve the polarity by labeling each finding as a risk factor or an atypical feature in prose where it would clarify (e.g., "richer-than-typical right-ratio (atypical feature, favorable)").

6. **Concentration framing (Core Principle 15)** — Is the 5% Schedule 13G threshold flagged as a compliance action item? It should not be — only 9.9% is the threshold that affects investment behavior.

7. **Color-cut (Tips section)** — Does the summary contain anecdotes (9/11, family origin stories, foundational-trauma narratives) that don't bear on the PIPE-raise track record, deal-sourcing, exit track record, public-co tenure performance, network depth, or known conflicts? Cut.

8. **Cross-references masquerading as content (Core Principle 10)** — Does the Sponsor team section say "same officer as [peer ticker]" or "see [peer doc] for details" instead of restating the bio? The summary must stand alone; cross-references are supplemental, never substitutes.

9. **Stale framing after deadline / event resolution** — Does the existing summary still describe events as pending, contingent, or speculative when they have since resolved? Sweep mentally for every date string ("6/14/26", "outside date"), every conditional clause ("if/then", "contingent on", "in the event"), and every speculative modifier ("would/could/pending/may"). Common patterns: (a) "Contingency for the case where Y" written when Y has already happened or been mooted by a new filing; (b) "Realistic close window now: late May" when the deadline has passed and a new extension has been filed; (c) deadline references in One-line view, Risk Factors / Atypical Features, Deal Terms, Trade View, and On the Horizon all needing to update together — partial propagation leaves the doc internally inconsistent; (d) On-the-horizon bullets that describe events that have since occurred. Verify against fresh EDGAR filings (extension proxies, S-4/A amendments, 8-Ks, BCA amendments) for any name where any deadline-or-event-pending language exists, then re-grep the whole summary to ensure every reference propagates.

10. **Pending vehicles counted in franchise denominators (Core Principle 14 sub-rule)** — Does the summary express franchise hit rate as "X-of-Y" with the current SPAC itself in the denominator (e.g., "0-of-2 prior franchise quality" when ATEK is one of the 2)? Sweep aggregate-metric lines, bucket-revision lines, and Verdict block SPONSOR rows. Pending vehicles do not enter their own franchise denominators.

11. **Trust-value-as-anchor framing for deSPAC outcomes (Core Principle 16 sub-rule a)** — Does the summary describe a prior deSPAC's outcome as "$X mkt cap = Y% destruction of original $N trust"? Trust capital was redeemable; the destruction figure manufactured from trust size misrepresents what was at risk. Reframe around direct outcome facts (current price tier, mkt cap, bankrupt/delisted/penny status).

12. **Standing-protocol restatement for positions Meteora does not hold (Core Principle 17)** — Does the summary issue a SELL/AVOID/REDEEM rec on a leg (common, rights, warrants) where the Position section reports zero exposure? Sweep One-line view, Verdict block REC row, Trade view, Post-deSPAC bullets. If unheld, describe factually without issuing a rec.

13. **Standard-feature findings and thematic-precedent reach (Core Principle 12 sub-rules)** — Are any findings simply restating universal SPAC features (going concern on the shell, deferred-fee waiver outstanding, founder lockup with $12 release, NT 10-Q filings near deadlines)? Reframe around uncommon specifics or drop. Is there a "and the prior failure was also in [theme]" finding sitting next to a sponsor-pattern finding? Pick one frame; drop the double-counted one.

14. **Editorial color in summary prose (Core Principle 18)** — Does the summary contain rhetorical-underscore phrases ("the pattern of X IS the pattern", "death spiral", "doom loop", "near-total value destruction", "no way to put lipstick on this", "catastrophic" as a grade-line label, "wipeout")? Cut and replace with clean factual statement. Test: deletion without information loss = delete.

15. **Sell-side and sponsor-press jargon undefined (Core Principle 19)** — Does the summary use opaque trade-desk shorthand without expansion ("terminated on redemption volume", "bumped on tape", "going effective", "crossed for redemption", "stuck on tape", "got plugged")? Define inline or rewrite in plain language. Readable cold is the standard.

16. **Concentration framing on sub-1% positions (Core Principle 15 sub-rule)** — Does the Position section include "No 9.9% concentration concern" or similar compliance-framing on a sub-1%-of-float position? At that scale, concentration is not a topic. Drop the framing; state share count cleanly.

17. **In-deal docs: grade against the in-deal template, not the pre-deal one (CP20).** If the doc is already in-deal (it has Deal terms / Valuation sections), run the gap-checklist against `references/in-deal-summary.md` Part 2: is the sponsor section correctly collapsed to PIPE-raising track record only (not a full director slate)? Is the target the lede? Are the comps and valuation current versus the latest S-4/A (multiples drift; re-pull live comp multiples via Bloomberg)? Do the deal terms reflect the most recent amendment? Are funding history and lineage present? Missing target sections, a stale comp set, or a sponsor section that still reads pre-deal are in-deal gaps to close. (NOTE: a pre-deal doc whose SPAC has newly announced a BCA is NOT an Update-Mode case — it routes to Deal Transition Mode per Phase 0. This item is only for docs already in-deal.)

18. **Human thesis or desk color dropped by a prior rewrite (CP21)** — Compare the current summary against the doc's human-generated content: entries authored by someone other than Claude, and attributed views inside entry bodies ("Vik:", "Walter:", "per the desk", "framing (NAME)", named street sources). If a prior rewrite dropped a desk view that is still live — a thesis, a pair-trade framing, a relative-value cross-read, an open debate — restore it to the appropriate section with attribution, durably phrased per CP21(b). This is the highest-priority gap category in this checklist: restoring lost human argumentation outranks every formatting, grading, and enumeration fix above.

19. **Missing or under-populated Relationships & Coverage section (CP23)** — Does the summary have a **Relationships & Coverage** section? Docs seeded before CP23 was added will not have one at all — in that case the Update-Mode pass MUST add it (it is now part of both closed section lists, CP11 sub-rule (b)). To populate it, mine three sources for coverage/contact intelligence: (a) the doc's own entries and existing summary — the S-1 underwriter(s), and any banker/broker/sponsor-contact intel already captured in Pillar entries or attributed desk notes; (b) the BCA 8-K / S-4 "Background of the Business Combination" for the target-side advisor and PIPE placement agent (in-deal docs); and, most importantly, (c) any relationship intel in the CURRENT conversation — Bloomberg IB (Instant Bloomberg) chat scrollback, morning-call notes, or broker exchanges the user has pasted, which is exactly the homeless intelligence this section exists to capture (named bankers, sponsor email domains, "same sponsor as [ticker]" cross-reads, in-flight introductions). Fold every such fact into the section, attributed with name + date where it came from a desk exchange (CP21 / CP23 sub-rule (a)). Keep durable facts evergreen; date in-flight workflow items; hold NO tape — "BTIG runs the SPAC and reps the target" is coverage and belongs here, "our offer sits at 10.90" is posture and belongs in Pillar 2 (CP23 sub-rule (b)). If genuinely nothing beyond the underwriter is known, a single honest line is the correct populated state — do not pad (CP23 sub-rule (c)). Because relationship intel is human-sourced, the same content is part of the CP21 inventory (item 18) — sweep the entries for it whenever you rebuild.

20. **Cohort comparison blocks (CP11 sub-rule b)** — Does the summary (or any entry) contain a “warrant cohort” / “SPAC cohort” section, table, or framing? These are artifacts of batch seeding sessions where several docs were built in one conversation — the “cohort” is just whichever names happened to share the chat, so the comparison carries no analytical meaning. Patch them out wholesale (summary via `patch-memory-summary`; entries via `patch-memory-entry`) and log the removal in the correction entry. Grep for “cohort”.

21. **Pre-deal no-PIPE negatives and PIPE-ability claims (CP24)** — Does the doc treat the absence of a committed PIPE on a pre-deal name as a negative (“no committed PIPE/anchor” as a caution, “None — [X] advisory only” peer-table cells, “only name with no real-capital backer”), or make claims about PIPE-raising ABILITY in either direction (very-high/high/moderate/low ratings, “no PIPE-raise ability”)? Replace with the factual PIPE-raise track record — named raises with size / date / redemption backdrop / anchors, or `no prior closing PIPE on record` stated neutrally. Also patch legacy in-deal section headers “Sponsor — PIPE-raising track record” → “Sponsor — PIPE-raising track record”.

22. **Unsolicited bucket-revision flags (CP9)** — Does the summary carry a “Suggested bucket revision” (or any Claude-proposed bucket change) that no desk transcript / email captured in the doc explicitly directed? Remove it — the sheet bucket stands alone; bucket changes are desk decisions. Where the desk HAS directed a change in a captured exchange, keep it, attributed and dated per CP21.

23. **Structural-figure verification against the latest operative filing (CP25)** — Pull the latest operative registration filing (`edgar-filings`: 424B4 if priced, else newest S-1/A / F-1/A; use the CIK when the ticker doesn't resolve) and read its cover page / offering table (`edgar-filing-text`, first ~5-8k chars). Reconcile EVERY structural figure the summary cites — trust per share / CIT + overfund, unit composition, right ratio, extension cadence and deposits, OA, founder shares / promote, at-risk capital, offering size, deadlines — and patch any stale figure. THEN sweep the summary's open questions / On-the-horizon for unresolved figure discrepancies and resolve them from the filing — never leave the flag standing next to the stale figure, and never repeat the disputed figure unresolved. Log every old→new with the filing cited (form + date). This item runs in EVERY Update Mode pass: a pass that patches around a wrong trust figure propagates it.

For each identified gap, note specifically: (a) what the existing summary said, (b) what the current guidance requires, (c) what fresh data is needed to fill the gap.

### Step U.3 — Pull only the fresh data needed for identified gaps

Update Mode is targeted, not exhaustive. Do not re-run the full Phase 1–3 pillars. Pull only the specific data needed to close the gaps from Step U.2. Typical Update-Mode data pulls:

- `MeteoraMCP-AWS:edgar-filings(cik=<CIK>, form_type="8-K", limit=20)` to enumerate post-IPO director-appointment / officer-change filings.
- `MeteoraMCP-AWS:edgar-filing-text` on the S-1/A to re-read the management section and CFO/CEO bios for missed director names and missed prior-SPAC tenure clauses.
- EDGAR CIK family sweep (adjacent CIKs to the SPAC's CIK) to locate sister-vehicle SPACs the existing summary may have missed.
- `MeteoraMCP:get-price(tickers=[...])` batched across every consummated prior-SPAC deSPAC ticker to apply the post-deSPAC quality rubric.
- `MeteoraMCP-AWS:spac-details(ticker=<sister TICKER>)` for any newly-discovered sister vehicles (PIPE size, deal status, current trust).
- `MeteoraMCP-AWS:edgar-filings` + `MeteoraMCP-AWS:edgar-filing-text` on the LATEST operative registration filing (424B4 if priced, else newest S-1/A / F-1/A) — cover page / offering table — to verify every structural figure before the summary re-states it (CP25 / gap item 23). Standard in every Update Mode pass, not optional.
- Web search ONLY if the gap involves a specific principal's outside biography (Forbes ranking, prior public-co tenure performance, contested narrative).

Run these in parallel where possible. Do NOT re-run trading-note-extended, EMSX blotter pulls, or full S-1 extraction — those produce Pillar 2 / Pillar 1 content that already exists in the doc and would be discarded anyway since Update Mode does not modify entries.

### Step U.4 — Compose the new summary

Compose the new executive summary using the same template as Phase 4.5, applying ALL current Core Principles. The new summary should be:

- **Comprehensive** — every gap from Step U.2 is filled.
- **Stand-alone** — no cross-references to peer docs as substitutes for content (Core Principle 10).
- **Evergreen** — no tape data, no current dollar mark on position, no point-in-time yields (Core Principle 11).
- **Honestly graded** — post-deSPAC outcomes graded per the OUTCOMES-RUBRIC memory doc (peak-and-current tape band + qualitative capital-formation overlay; Core Principle 16) using fresh Bloomberg prices.
- **Exhaustively enumerated** — full director slate, full franchise vehicle list (legacy + own-sponsored + adjacent precedents).
- **Thesis-preserving** — the CP21 inventory (existing summary + entries) is satisfied: every live human-authored view appears in the new summary with attribution; none lost relative to what the doc held before this pass.

Length will typically grow — adding missed directors and missed franchise vehicles routinely takes a previously-1,500-word summary to 2,000+ words. That is correct per Tips section: "A summary that runs 1,000-1,500 words because the franchise has five named principals and four prior SPAC vehicles is correct." For franchises with many vehicles (Cantor at ~12, Churchill at ~10), 2,000-2,500 words is appropriate.

### Step U.5 — Write the new summary to the doc

**Tool selection rule.** Two tools are available for writing the updated summary; prefer the right one for the situation:

- **`MeteoraMCP-AWS:patch-memory-summary(name, edits=[{old_str, new_str}, ...])`** — PREFERRED for targeted edits. Apply one or more `old_str → new_str` substitutions to the existing summary. Each `old_str` must match the current summary exactly and uniquely; use empty `new_str` to delete a phrase. Edits apply sequentially — if any edit fails (string not found, ambiguous match), the entire patch is aborted and nothing is saved. Use this whenever fewer than roughly half the sections are changing — fixing a CIK, removing a banned tape-characterization phrase, updating a CFO's bio, refreshing one prior-SPAC's quality grade, correcting a sponsor track-record line. Patch is faster, less token-expensive, lower-risk, and produces a cleaner audit trail than a full rewrite.
- **`MeteoraMCP-AWS:update-memory-summary(name, new_summary)`** — RESERVED for genuine full rewrites. Use only when (a) the summary is being seeded from scratch (Seed Mode Phase 4), (b) the gap-checklist surfaces wholesale issues (most sections need to change), or (c) the existing summary is broken / truncated / corrupt and must be restored from a known-good text. Do not reach for `MeteoraMCP-AWS:update-memory-summary` when 1–3 targeted patches would do the job; full rewrites have more failure modes and routinely introduce drift in sections that weren't supposed to change. Full rewrites additionally REQUIRE the CP21 human-content inventory pass before composing — wholesale rewrites are precisely where human theses have historically been lost.

**Update Mode default flow.** For most Update Mode passes — closing 1–4 specific gap categories — compose the targeted edits as `(old_str, new_str)` pairs and call `MeteoraMCP-AWS:patch-memory-summary` once with all of them. Read the current summary fresh via `MeteoraMCP-AWS:read-memory-doc(summary_only=true)` immediately before composing the patches so each `old_str` is verified against the live text, not against context that may be stale. If a patch fails, re-read the summary (the live text may differ slightly — whitespace, em-dashes vs hyphens, smart quotes), correct the `old_str`, and retry. The two-step prompt-fetch step of `MeteoraMCP-AWS:update-memory-summary` is unnecessary in Update Mode — the gap-checklist in Step U.2 IS the rewriting prompt.

**Pillar entry corrections use `MeteoraMCP-AWS:patch-memory-entry`.** The same exact-match rule applies; entries are referenced by 1-based index. Use `MeteoraMCP-AWS:read-memory-doc(entries_limit=-1)` first to see entries with their indices.

### Step U.6 — Append a correction-tagged entry documenting the gaps fixed

If Step U.2 identified gaps in the existing pillar entries (missing IPO directors, missing franchise vehicles, mis-graded outcomes), append a `correction`-tagged entry via `MeteoraMCP-AWS:update-memory-doc(name=<TICKER>, tag="correction", author="Claude", body=<correction_body>)`.

The correction body should briefly enumerate:
- What was missing or mis-graded in the original pillar entries.
- The corrected data (full director slate, full franchise enumeration, re-graded post-deSPAC outcomes).
- A note that the executive summary has been updated to reflect the corrections; the original pillar entries remain as historical record.

This keeps the entry record honest. Future readers seeing the summary cite a director the original Pillar 3 entry doesn't bio will find the correction entry that explains the discrepancy.

If Step U.2 identified gaps ONLY in the summary (e.g., color cut, tape-data removed, findings reframed, "Bombs" header renamed to "Risk Factors / Atypical Features") and the underlying pillar entries had the correct data, no correction entry is needed — the summary is the only thing that needed updating.

### Step U.7 — Email the updated executive summary to the filings distribution list

After the summary has been updated in the doc via `MeteoraMCP-AWS:patch-memory-summary` (or `MeteoraMCP-AWS:update-memory-summary` in the full-rewrite case) in Step U.5, email the freshly-updated summary to `filings@meteoracapital.com`.

**Read the live post-update summary first.** Call `MeteoraMCP-AWS:read-memory-doc(name="<TICKER>", summary_only=true)` to fetch the canonical post-patch text. Do NOT compose the email body from your in-context patch plan — patches may have applied in a slightly different order than composed, and the canonical content is what's actually in the doc after writes settle. This step is mandatory.

Call `MeteoraMCP-AWS:send-email` with:
- `to`: `["filings@meteoracapital.com"]`
- `subject`: `[<TICKER>] Memory doc summary updated — <Full SPAC Name>`
- `content_type`: `"HTML"`
- `body`: the freshly-fetched executive summary rendered as HTML — apply the SAME markdown-to-HTML conversion rules as Seed Mode Step 4.6.

The provenance header at the top of the body differs from Seed Mode to reflect that this is an update, not a fresh seed:

```html
<p style="color:#888; font-size:11px; margin:0 0 16px 0; border-bottom:1px solid #eee; padding-bottom:8px;">
  Memory doc summary updated for <strong>[TICKER]</strong> on [today's date — YYYY-MM-DD]. Gaps closed in this update: [one-line list from Step U.2 — e.g. "added 2 missing IPO directors; expanded legacy CFAC franchise track record from 4 to 7 vehicles; re-graded 3 deSPACs per current SPAC-arb quality rubric; removed banned tape-characterization phrases"]. Source of truth is the memory doc; this email is an evergreen snapshot of the post-update executive summary.
</p>
```

**Content scope, formatting, and failure handling rules are identical to Seed Mode Step 4.6** — summary only (no pillar entries), HTML body wrapped in the outer styling `<div>`, MeteoraMCP-AWS:send-email failures surfaced in the Step U.8 chat confirmation rather than blocked on.

### Step U.8 — Confirm completion

Reply in chat with a short confirmation:
- Doc name + ticker + Update Mode confirmation
- New summary length (vs prior length, e.g. "21,845 chars vs prior 15,710")
- List of gap categories closed (e.g. "added 2 missing IPO directors, expanded legacy CFAC track record from 4 to 7 vehicles, re-graded 3 deSPACs from mediocre/poor → good per current rubric")
- Whether a correction entry was appended (and what it covers)
- Whether the filings@ email send succeeded (or the error if it failed)

Do not paste the new summary into chat — it lives in the doc.

---

## Phase D — Deal Transition Workflow

Deal Transition Mode is invoked from Phase 0 when the doc already exists, was seeded pre-deal (Pillars 1–3 only; sponsor-led summary with no Deal terms / Valuation sections), and the SPAC has since announced a BCA (now `stage="indeal"`). This is NOT a guidance refresh — it is a re-centering of the document onto the deal per CP20. The pre-deal summary's organizing question (can this sponsor source and close a deal?) is now spent; the document must answer the in-deal questions (what is the target, what is it worth, what are the terms?).

**The two paths produce identical in-deal output.** Phase D and an in-deal Seed compose the SAME deal-focused summary from the SAME template (`references/in-deal-summary.md`) and run the SAME target research (Phase T). The only difference is mechanical: a Seed builds the doc from scratch (all six pillars fresh); a Transition appends the in-deal pillars to an existing pre-deal doc. Read `references/in-deal-summary.md` in full before composing.

**Defining constraints:**
- **Existing pre-deal pillar entries (1–3) are preserved untouched** — append-only, exactly as in Update Mode. The pre-deal S-1 extraction, trading note, and sponsor bios remain valid history.
- **The in-deal pillars (4–6) are appended as NEW entries.**
- **The executive summary is rebuilt wholesale**, not patched. The focus shift from sponsor-led to deal-led changes nearly every section, so this is the one case where `MeteoraMCP-AWS:update-memory-summary` (full replace) is correct over `patch-memory-summary` — see Step D.6.
- **Human-authored theses and desk color carry forward (CP21).** "Rebuilt wholesale" refers to the summary's STRUCTURE, not its human content. Step D.1's read doubles as the CP21 inventory pass; Step D.6 places every live human view in the rebuilt summary; Step D.7's transition entry logs the carried-forward/retired ledger.

### Step D.1 — Read the existing doc fully
`MeteoraMCP-AWS:read-memory-doc(name="<TICKER>", entries_limit=-1)`. Confirm it is pre-deal-shaped (Pillars 1–3, sponsor-led summary). Capture the structural facts already extracted (trust, deadlines, unit composition, sponsor principals, franchise enumeration) — they carry forward into the in-deal summary's condensed Structure and Sponsor — PIPE-raising sections without re-extraction.

While reading, build the **CP21 human-content inventory**: a written checklist of every attributed desk view, thesis line, pair-trade/relative-value framing, and human-authored argument found in the existing summary and entries (entries with author ≠ Claude, and attributed views inside any entry body). This inventory is a mandatory input to Step D.6 — the rebuilt summary is graded against it item by item.

### Step D.2 — Pull the deal context
- `MeteoraMCP-AWS:spac-details(ticker="<TICKER>")` — confirm `stage="indeal"`, capture pro forma ticker if present, current position.
- `MeteoraMCP-AWS:edgar-filings(cik=<SPAC CIK>)` — locate the BCA 8-K, the investor deck (Ex 99.1/99.2), and any S-4/F-4 - applying the **CP22 3-pass discovery** (after the SPAC CIK, resolve the new listing holdco / merger-sub CIK named in the BCA and search THAT registrant, since offshore / FPI F-4s are filed there, not under the SPAC; then the target CIK). Do not conclude "no S-4/F-4" from the SPAC CIK alone. Also pull the target's CIK if it has its own EDGAR history.
- Web search for the deal announcement, the target, and the target's funding history (per `references/in-deal-summary.md` Part 1.2/1.3 query lists).
- `MeteoraMCP:get-price` / `get-company-info` (Bloomberg, non-AWS — AWS lacks these) for live comp multiples.

### Step D.3 — Run Pillar 4 (S-4/F-4 extraction), if filed
If an S-4/F-4 is filed (confirmed via the CP22 3-pass discovery - SPAC CIK + holdco / merger-sub CIK + target CIK), run `spac-s4-extraction` and append the output as a `filing`-tagged entry (per Step 4.4b). If all three CP22 passes confirm no S-4/F-4 yet, skip and note the deferral in the summary's "On the horizon"; Pillars 5 and 6 can still run on BCA materials.

### Step D.4 — Run Pillar 5 (deal review)
Run `spac-deal-review` on the BCA materials (deck + 8-K + S-4 if present) and append as a `diligence`-tagged entry (per Step 4.4c).

### Step D.5 — Run Pillar 6 (Target Dossier)
Build the Target Dossier per `references/in-deal-summary.md` Part 1 — company history since inception, funding rounds, comps, spin-out/parent lineage, valuation inputs — and append as a `diligence`-tagged entry (per Step 4.4d).

### Step D.6 — Rebuild the executive summary wholesale to the deal-focused template
Compose the new summary per `references/in-deal-summary.md` Part 2, synthesizing pre-deal Pillars 1–3 (now condensed into Structure + Sponsor — PIPE-raising) with in-deal Pillars 4–6 (now the lede). Apply CP20 (target is the lede; sponsor collapses to PIPE-raising) and every other Core Principle. Write via `MeteoraMCP-AWS:update-memory-summary` (full replace — this is a genuine wholesale rewrite, not a partial edit, so `patch-memory-summary` does NOT apply here). Use the two-step interface; the in-deal template + the existing pre-deal content together ARE the rewriting prompt, so the prompt-fetch step is informational only.

**CP21 verification (blocking).** Before writing, place every live item from the D.1 human-content inventory into the draft — attributed and durably phrased — in its appropriate section (position theses and desk debates → Trade view; relative-value cross-reads → Comparable companies; human-flagged concerns → Risk Factors / Atypical Features). After composing, re-check the draft against the inventory item by item; a missing live human view is a blocking error to fix before the write, not a nit to note. Mooted views are retired per CP21(c) via the Step D.7 ledger.

### Step D.7 — Append a transition-tagged entry
`MeteoraMCP-AWS:update-memory-doc(name="<TICKER>", tag="transition", author="Claude", body=<transition_body>)` recording: the BCA announcement (target, date, headline terms), that the doc transitioned pre-deal → in-deal on [today's date], which in-deal pillars were appended (4/5/6, noting any deferral), that the executive summary was rebuilt to the deal-focused template, and the **CP21 ledger** — every human view from the D.1 inventory listed as either carried forward (naming the summary section it landed in) or retired (with the mooting event). This keeps the entry record honest — a future reader sees exactly when and why the doc's focus changed.

### Step D.8 — Email the rebuilt summary to the filings distribution list
Read the live post-rebuild summary via `MeteoraMCP-AWS:read-memory-doc(name="<TICKER>", summary_only=true)`, then `MeteoraMCP-AWS:send-email` to `["filings@meteoracapital.com"]` with subject `[<TICKER>] Memory doc transitioned to in-deal — <Full SPAC Name> / <Target>` and `content_type: "HTML"`. Apply the same markdown→HTML conversion rules as Step 4.6, with a provenance header noting the pre-deal→in-deal transition and the target name. Content scope, formatting, and failure handling are identical to Step 4.6.

### Step D.9 — Confirm completion
Reply in chat with: doc name + ticker + Deal Transition confirmation; the target name and headline deal terms; which in-deal pillars were appended (and any deferral, e.g. "Pillar 4 deferred — no S-4 yet"); new summary length vs prior; that a `transition` entry was appended; and whether the filings@ email succeeded. Do not paste the summary into chat — it lives in the doc.

---

## Output Format Conventions

- **The doc is the deliverable**, not the chat. Do not paste the synthesized executive summary into chat as the response — write it to the doc and confirm.
- **Entries are append-only.** Never use `MeteoraMCP-AWS:update-memory-doc` to overwrite. If something needs to be corrected, append a `correction`-tagged entry.
- **Tag entries correctly**: Pillar 1 → `diligence`; Pillar 2 → `filing`; Pillar 3 → `diligence`. The `filing` tag is reserved for filing track / structural disclosures so future searches by tag are useful.
- **Author = Claude** for all entries written by this skill (so the user can distinguish between human-authored and skill-authored entries downstream).
- **Use markdown** in entries — they render in the doc as markdown.
- **Do not seed the executive summary on doc creation** — leave the seed empty and write it via `MeteoraMCP-AWS:update-memory-summary` at Step 4.5. This keeps the summary composition in one place.

---

## Tips for Better Results

**Run pillars sequentially, not in parallel.** Pillar 1 produces information (sponsor entities, principal names, founder share splits) that Pillars 2 and 3 reference. Pillar 3's network map needs the sponsor entity disclosures from Pillar 1. Trying to parallelize loses cross-pillar signal.

**For pre-effective SPACs, the One-line view's trade-view phrase reads `"Pre-effective; not yet trading — Pillar 2 will be re-run when IPO prices."`** This is correct and expected. The summary still has no Tape section AND no trading-characterization element — see Core Principle 11.

**For the EDGAR-direct path (Phase 1 Path B), use `summary: True` on the first `MeteoraMCP-AWS:edgar-filing-text` call** to get an orientation pass. Then run targeted offset-based fetches for the specific 9 sections. Skipping the orientation pass and going straight to offset fetches routinely misses sections because S-1 page lengths vary.

**The mid-registration filing-track comparison is high-signal.** Look for: right-economics richening (e.g., 1/10th → 1/4 right is a 2.5x richer dilution), offering-size changes, geography mandate scrubs ("China including Hong Kong and Macau" → "industry-agnostic"), auditor changes, sponsor structure changes, ID slate changes. All of these go into the executive summary's "Filing track" section.

**Pillar 3's `spac-bios` skill always pulls Bloomberg historical for any public-co operating tenure of any team member.** This routinely surfaces the single highest-impact diligence signal (a CEO's prior public-co tenure that produced a -67% drawdown + 5x post-departure rally, etc.). Do not skip this.

**Large entries get split.** `MeteoraMCP-AWS:update-memory-doc` has a ~10k char body limit. Pillar 3's spac-bios output for a 5-person team will be 30-50k chars and needs to be split into 3-5 entries. Use clear "Part N/M" headers on each split entry so future readers can reconstruct the sequence.

**The "On the horizon" section in the summary is forward-looking.** Pull the next 1-3 gating events (IPO pricing, S-4 filing, extension deposit, vote date, hard liquidation deadline) from Pillars 1 and 2, and the top 3-5 open questions from Pillar 3. This is what the user will scan first when they re-open the doc 3 months later.

**Calibrate length per section, not as a global ceiling.** The summary has no fixed word target. Structure / filing-track / position sections should stay tight (1-2 lines per element) — those details live in the Pillar 1 and Pillar 2 entries and don't need to be restated at length in the summary. Team bios and sponsor track record are the opposite: they must be substantive, named, and stand alone, even when the SPAC is a sister to a peer doc with the same officer slate. The single most common failure mode of a seeded summary is compressing team and franchise content into one-liners or "same as [peer ticker]" cross-references — guard against this aggressively. A summary that runs 1,000-1,500 words because the franchise has five named principals and four prior SPAC vehicles is doing the right thing.

**Cut color and irrelevant biographical detail.** The summary is read for thesis-relevant signal, not narrative interest. Anecdotes (9/11 retellings, family origin stories, foundational-trauma narratives), career color beyond what's structurally relevant, and historical events even when cinematically compelling routinely sneak into bios written from S-1 disclosure language. Test each clause: does this affect the PIPE-raise track record, deal-sourcing, exit track record, public-co tenure performance, network depth, or a known conflict? If no — cut it. The Pillar 3 entry can carry color; the summary cannot. Concretely, a sentence like "Howard Lutnick's network is the firm's network" earns its place because it directly drives the PIPE-raise track record assessment; "survived the 9/11 attack which killed 658 of Cantor's 960 staff" does not earn its place in the summary even though it is true and historically significant.

**No internal Meteora jargon without parenthetical definition.** Internal terms — `"soft mark,"` `"trust floor,"` `"redemption kicker,"` `"Crescent Term,"` `"naked common,"` `"house ID,"` `"exploding unit,"` `"BHAV-style trade,"` etc. — should be defined parenthetically the first time they appear in the summary, OR replaced with plainer language. The summary is read by team members rotating in and by downstream skills with no priors; clarity is cheap and ambiguity costs. Concrete example: instead of `"18-month soft mark (May 2027)"` write `"18-month soft deadline (May 2027) — the date by which the sponsor expects to consummate; extensions available to push to the hard 24-month deadline."`

**Comparative franchise diligence is the highest-leverage step in seeding a franchise SPAC.** When seeding a Cantor / Churchill / Ajax / Pono / Replay / Forest Road vehicle, before composing the summary, pull the immediately-prior franchise sibling's memory doc (or its S-1 if no doc exists) and run a side-by-side on: per-share overfund at redemption (added or removed?), right-economics, founder share count per dollar of trust, extension cadence ($/share/month), OA size and exercise terms, mandate language, sponsor structure (single-sponsor vs syndicated at-risk capital). Things SILENTLY DROPPED from the new deal vs prior siblings are routinely the most actionable findings (Risk Factors / Atypical Features section) and are the easiest to miss because the omission isn't called out anywhere in the S-1. See Core Principle 13.

**EDGAR CIK family sweep is the canonical method for franchise enumeration.** Franchise CIKs are usually clustered numerically — e.g., CEPF CIK = 2034267, CEPV CIK = 2034266 (consecutive). To enumerate the full franchise universe, search EDGAR for adjacent CIKs in the same numeric neighborhood, look for matching sponsor-entity names, and cross-reference against the franchise's IR archive and recent SPAC IPO news. This sweep should happen in Phase 0 alongside the standard pre-flight checks. Listing only the vehicles that came up in the user's prompt or the standard `MeteoraMCP-AWS:spac-details` lookup is wrong — see Core Principle 14. The high-impact failure mode this prevents: missing an in-flight or recently-IPO'd sibling that wasn't on the user's radar but that materially affects franchise cadence and PIPE-capability narrative.

**Adjacent precedents (sponsor as PIPE/FPA/anchor/UW, not as sponsor) belong in the franchise track record.** A sponsor's role as PIPE provider, FPA counterparty, anchor investor, or deSPAC underwriter on third-party SPACs is durable evidence of vertical capability and pipeline depth — often more relevant for assessing PIPE-raise track record on a target-vertical-specific basis than the sponsor's own SPAC track record. For Cantor, Securitize is an obvious adjacent precedent. The franchise IR archive and news archive (search `"<Sponsor name>" PIPE`, `"<Sponsor name>" FPA`, `"<Sponsor name>" anchor`, `"<Sponsor name>" deSPAC`) routinely surface these. Skipping adjacent precedents is the failure mode this principle exists to prevent.

**Position concentration framing: 9.9%, not 5%.** When writing the Position section, report `"~X% of public float"` as durable factual context. Compliance "action items" appear ONLY when approaching or exceeding 9.9% — affiliate status / 13D triggering / voting limitations / redemption restrictions are the thresholds Meteora actually behaves around. The 5% Schedule 13G threshold is administrative; do not flag it as a finding in the Risk Factors / Atypical Features section or as an "On the horizon" action item. See Core Principle 15.

**Post-deSPAC outcome grading: read the OUTCOMES-RUBRIC memory doc first, then grade peak-and-current with the capital-formation overlay.** The desk-editable rubric doc supersedes any grading text in this or any other skill file — pull it via `MeteoraMCP-AWS:read-memory-doc(name="OUTCOMES-RUBRIC")` before grading, and never grade from training-data priors. The two rules that catch most mis-grades: (1) the tape band is the BETTER of the highest sustained band and the current price — a name above trust today is a success no matter how ugly the path (state the grade; skip the drawdown story), and a name that sustained $7–$10 for three months is Good even if it prints $3.83 today; Failed is structural only (bankrupt / delisted / liquidated — a viable sub-$1 name is Poor). (2) A qualifying closing raise lifts the band — one tier at minimum, two when the qualitative context makes it franchise-defining (post-2021 winter era, 90%+ redemption backdrop, named anchors, size vs the deal, sponsor board continuation) — with no dollar bright line. Worked case: SPWR/Complete Solaria (~$80M against ~99% redemptions, 2023 winter) = Poor tape lifted two tiers → Good. Mis-grading successes down — or narrating their drawdowns — understates real franchise capability and produces a misleading thesis.

**Officer bios in the S-1 management section are the primary source for legacy franchise enumeration — read them carefully.** When the SPAC's CFO or CEO has prior-SPAC tenure, their S-1 bio enumerates each prior vehicle inline with named tenure dates and named outcomes (target name + close date, or liquidation date). For example: `"served as Chief Financial Officer of CFAC III from July 2021 until consummation of its initial business combination with AEye in August 2021"` — that single clause is a primary-source datapoint capturing entity, role, dates, AND outcome. EDGAR CIK family sweep finds the entities; the officer-bio tenure list reveals what happened to each. Mining this list is mandatory in Phase 3 (and in any Update Mode gap-checklist for franchise enumeration). The high-impact failure mode this exists to prevent: missing 4 of 7 legacy CFAC vehicles (AEye, Satellogic, Rumble, CFAC VII liquidation) in a Cantor seed despite the data sitting in the document Phase 1 already pulled.

**Director enumeration is mandatory and must capture every name in the S-1 management table plus every Item 5.02 8-K appointment since IPO.** Pulling only the most-recently-appointed ID and missing the IPO-original "Director Nominees" who took their seats at trading commencement is the single most common Pillar 3 / summary failure mode. The S-1 management section has a table titled "Officers, Directors and Director Nominees" naming every original director with age and title; bios follow with role tenure, prior-SPAC seats, prior employment, and education. Footnote-only "Director Nominees" ARE directors as of trading commencement — bio them. After the S-1, every Item 5.02 8-K either adds, replaces, or resigns a director — sweep `MeteoraMCP-AWS:edgar-filings(cik=<CIK>, form_type="8-K", limit=20)` and read each one. The cumulative roster — original IPO directors plus net additions/removals from 8-Ks — IS the current board, and every member must appear in the summary's Sponsor team section.

---

## Reference: MeteoraMCP Doc Tools

- `MeteoraMCP-AWS:list-memory-docs` — confirm doc does not already exist (Phase 0)
- `MeteoraMCP-AWS:create-memory-doc(name, author, summary?)` — create the file (Phase 4.1; pass no summary)
- `MeteoraMCP-AWS:update-memory-doc(name, tag, author, body)` — append entry (Phase 4.2-4.4 in Seed Mode; Step U.6 in Update Mode for correction entries)
- `MeteoraMCP-AWS:update-memory-summary(name, new_summary?)` — wholesale set/replace summary. RESERVED for from-scratch seeds (Phase 4.5) and full rewrites only. Two-step interface; for seeding skip the prompt-fetch step.
- `MeteoraMCP-AWS:patch-memory-summary(name, edits=[{old_str, new_str}, ...])` — **PREFERRED for targeted summary edits in Update Mode (Step U.5).** Apply exact-match `old_str → new_str` substitutions; empty `new_str` deletes. All edits apply atomically — if any fails, nothing saves. Use this whenever fewer than roughly half the sections are changing. Lower token cost, lower drift risk, cleaner audit trail than a full rewrite.
- `MeteoraMCP-AWS:patch-memory-entry(name, entry_index, edits=[{old_str, new_str}, ...])` — same as MeteoraMCP-AWS:patch-memory-summary but for a specific pillar entry by 1-based index. Use to correct a Pillar 1 / 2 / 3 entry without deleting and re-adding it. Read the doc first via `MeteoraMCP-AWS:read-memory-doc(entries_limit=-1)` to confirm the index.
- `MeteoraMCP-AWS:read-memory-doc(name, entries_limit?, summary_only?)` — for confirming doc state, fetching the live summary text before composing patches, or surveying entries before patching one.
- `MeteoraMCP-AWS:delete-memory-doc(name)` / `MeteoraMCP-AWS:delete-memory-entry(name, entry_index)` — emergency-only; surface to user before using
- `MeteoraMCP-AWS:send-email(to, subject, body, content_type)` — used in Step 4.6 (Seed Mode) and Step U.7 (Update Mode) to deliver the executive summary as HTML to `filings@meteoracapital.com`. Sender is fixed to walter@meteoracapital.com. The summary email is part of the seed/update workflow, not optional.

**Tool-selection rule of thumb for summary edits:** if you can express the change as 1–4 substring substitutions, use `MeteoraMCP-AWS:patch-memory-summary`. If you can't (the existing text is corrupt, the structure is wholesale changing, or the summary is being seeded from scratch), use `MeteoraMCP-AWS:update-memory-summary`. Default to patch.

---

## Reference: Sub-Skills Orchestrated

- `spac-s1-extraction` — Phase 1 Path A (PDF attached). Output goes into Pillar 1 entry.
- `trading-note-extended` — Phase 2 Path A (Bloomberg-traded). Output goes into Pillar 2 entry.
- `spac-bios` — Phase 3. Output goes into Pillar 3 entries (likely split).
- `spac-s4-extraction` — Phase 1B (in-deal, S-4/F-4 filed). Output goes into Pillar 4 entry.
- `spac-deal-review` — Phase 3B (in-deal). Output goes into Pillar 5 entry.

The EDGAR-direct alternatives in Phase 1 Path B and the pre-effective alternative in Phase 2 Path B are inline workflows, not separate skills — they live in this skill so the orchestration is self-contained. The **Target Dossier** (Phase T / Pillar 6) is likewise an inline workflow, with its methodology in the bundled reference file below rather than a separate skill.

## Reference: Bundled Files

- `references/in-deal-summary.md` — the canonical in-deal deliverable: Part 1 is the Target Dossier research methodology (Pillar 6 — company history since inception, funding rounds, comps, spin-out/parent lineage, valuation inputs); Part 2 is the deal-focused executive summary template (the closed in-deal section list). **Read this file in full** before composing any in-deal summary, whether via an in-deal Seed (Step 4.5) or a Deal Transition (Step D.6). It is the single source of truth shared by both paths — if the in-deal deliverable needs to change, change it there, not inline.

## Reference: Server Routing (MeteoraMCP-AWS vs MeteoraMCP)

Prefer **`MeteoraMCP-AWS`** for every tool both servers expose: memory-doc CRUD (`create-memory-doc`, `update-memory-doc`, `read-memory-doc`, `list-memory-docs`, `patch-memory-summary`, `patch-memory-entry`, `update-memory-summary`), all EDGAR tools, `spac-details`, `send-email`, and Pinecone / `semantic-search`. Fall back to the non-AWS **`MeteoraMCP`** ONLY for tools AWS does not have: Bloomberg (`get-price`, `get-vwap`, `get-company-info`, `get-bond-chain`/`get-bond-price`, `get-option-chain`/`get-option-data`) and `emsx-blotter`. The Bloomberg/EMSX references in Phases 0, 2, T, and D are deliberately non-AWS for this reason.

---

## What This Skill Replaces

This skill replaces:
- **Ad-hoc memory doc seeding** ("let me just create the doc and paste in what I have"), partial seeds (only running one of the three pillars and never circling back), and inconsistent first-pass quality across the SPAC universe. The framework is the entire point — every doc gets the same three-pillar foundation, so subsequent diligence (`trading-note-extended` thesis blocks, `spac-deal-review` pulls, `spac-headlines` lookups) all build on a consistent base.
- **Ad-hoc summary updates** ("the summary on [TICKER] needs to be updated for new guidance, just rewrite it" with no checklist applied). Update Mode is targeted, mode-aware, and applies the full Core Principles checklist + post-deSPAC quality rubric every time. Doing summary updates without the checklist routinely misses the same categories the original seed missed (full director slate, exhaustive franchise enumeration, properly-graded post-deSPAC outcomes).
- **Ad-hoc deal write-ups when a BCA drops on a name we already track** ("the deal got announced, let me just rewrite the summary"). Deal Transition Mode enforces the full pre-deal→in-deal re-centering (CP20): it appends the in-deal pillars (S-4 extraction, deal review, Target Dossier), runs the target research (history since inception, funding rounds, comps, lineage, valuation), and rebuilds the summary to the deal-focused template — rather than bolting a deal paragraph onto a sponsor-led pre-deal summary. The in-deal deliverable is identical whether the name was first seeded pre-deal then transitioned, or seeded fresh while already in-deal.

Always use this skill to seed a new memory doc, update an existing summary to current guidance, OR transition a pre-deal doc to in-deal when a BCA is announced — do not do any of these ad hoc. Consistent first-pass quality across the universe, consistent re-grading when guidance evolves, and a consistent deal-focused deliverable when deals are announced are what make the rest of the doc system work.
