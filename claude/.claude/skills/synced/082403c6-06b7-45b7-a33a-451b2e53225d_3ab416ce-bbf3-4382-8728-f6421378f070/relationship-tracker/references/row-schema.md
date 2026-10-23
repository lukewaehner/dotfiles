# Tracker row schema

`build_tracker.py` consumes a JSON list of rows (or `{"rows":[...],"asOf":"YYYY-MM-DD"}`).
Fields per row:

| field           | type            | notes |
|-----------------|-----------------|-------|
| `id`            | string          | stable key; derive from ticker/name so user edits persist across rebuilds. Auto-generated if omitted. |
| `display`       | string (req)    | SPAC name or group shown in the SPAC column. |
| `ticker`        | string          | primary SPAC ticker, e.g. "LOKV". |
| `matchKey`      | string          | ticker used to match the live SPAC universe (alias if the common ticker differs, e.g. "ISRL"→"ISRLF"). Defaults to `ticker`. |
| `type`          | enum            | `Sponsor` / `Bank/Broker` / `Target`. |
| `contacts`      | string          | "Name (Firm) / Name (Firm)". |
| `lastContacted` | "YYYY-MM-DD"    | most recent deal email sent or received. |
| `statusOverride`| string|null     | set `"Liquidating"` or `"Closed/Done"` to override live status; else null. |
| `nextStep`      | string          | concrete action. |
| `followUp`      | "YYYY-MM-DD"|null| when to resurface; drives the "Follow up now" flag when due. |
| `notes`         | string          | summary + any borderline-classification note; use " ;; " between dated entries. |

Live deal status (In-Deal / Pre-Deal / target / deadline / bucket) is filled at
runtime by the artifact via `spac-details` keyed on `matchKey` — you do not bake it
into the row.
