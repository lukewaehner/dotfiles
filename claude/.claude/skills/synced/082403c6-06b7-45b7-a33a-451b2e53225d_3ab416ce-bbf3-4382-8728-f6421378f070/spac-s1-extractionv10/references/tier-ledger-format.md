# Tier Ledger — shared record of sponsor tier grades
One row per vehicle graded, so tiers stay comparable across names instead of being re-derived per run.

| Field | Content |
|---|---|
| `ticker` | SPAC ticker |
| `graded` | date |
| `tier` | 1–5, half-tiers allowed |
| `pedigree` / `structure` / `prior_outcomes` / `capital_access` / `deal_flow_edge` | axis grades 1–5 |
| `vertical_fit_modifier` | 0.0 / +0.25 / +0.5 |
| `structure_math` | `SE = r + 0.15w = x; SE grade g; runway m adj a; UW tier adj u; structure = final` |
| `composite_math` | `0.30·ped + 0.30·str + 0.20·prior + 0.15·cap + 0.05·flow = base; +mod = tier` |
| `deciding_axes` | the two axes that decided the tier |
| `archetype_comp` | the tier-1 franchise matched on archetype |
| `poor_mans_of` | the payoff line |
| `anchor` | yes / no / undetermined, with what was swept |
| `cost_per_share` | managing vs non-managing |
| `ledger_labels` | verbatim FRANCHISE-OUTCOMES-LEDGER labels the Axis-3 grade rests on |
| `superstar_flag` | no, or `yes — person, % of sponsor economics` (reported, never scored) |
| `sponsor_changed_since_ipo` | no, or `yes — acquirer, date` |
| `tier_confidence` | high / medium / low |
| `untagged_figures` | any figure that could not be source-tagged |

**Read before grading.** Where a name shares principals with an existing row, read that row first. Where a franchise's prior-vehicle outcomes are already recorded, cite them rather than re-deriving — sponsor teams recycle across sibling vehicles, and independent re-derivation is how sibling docs come to disagree about identical facts.
