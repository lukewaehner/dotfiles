# IB box -> Claude Project mapping

This table routes each Instant Bloomberg chat box to a destination Claude Project folder and
gives it a filename slug. Edit it to match the destination Claude's actual project names.

How the skill uses it:
- Match a box by the **stable leading part** of its IB label (titles are truncated on screen,
  e.g. "SAFT (Safety Insur..."). Case-insensitive, ignore trailing "...".
- `slug` -> the filename becomes `<slug>_<YYYY-MM-DD>.md`.
- `project` -> the Claude Project folder the transcript is filed into.
- `capture: no` -> skip this box entirely (utility/admin rooms that aren't deal chats).
- Any box on screen that is NOT in this table is still captured, with slug = a safe
  uppercased version of its label, and filed under the `_unmapped` project for manual routing.

| IB box (leading match) | slug | project | capture |
|---|---|---|---|
| SAFT (Safety Insurance | SAFT | SAFT - Safety Insurance / Mapfre | yes |
| UTZ Brands | UTZ | UTZ Brands | yes |
| PAG Penske | PAG | PAG - Penske | yes |
| Biolife Solutions | BLFS | Biolife Solutions | yes |
| PSNL/TEM Tempus | TEM | PSNL / Tempus | yes |
| LXP - BAM/CPP | LXP | LXP - BAM / CPP | yes |
| ATAI | ATAI | ATAI / Beckley | yes |
| ESI - SOLS | ESI | ESI - SOLS Element | yes |
| TBPH - ZYME | TBPH | TBPH / ZYME | yes |
| AACT Kodiak | AACT | AACT - Kodiak | yes |
| AI LLM Merger Arb | AI_MERGER_ARB | Internal - AI Merger Arb | yes |
| To Do List | - | - | no |
| Deal Notes | - | - | no |
| AI Dev Team | - | - | no |
| Memory Doc Uploads | - | - | no |

## Notes
- Ticker-style slugs (SAFT, UTZ, TEM...) keep filenames greppable and sortable.
- Add a row per new deal room as they appear. Keeping the leading-match text short and
  stable (the part that never truncates) makes matching robust as titles change.
- If you want the whole list captured with no skips, set every `capture` to `yes`.
