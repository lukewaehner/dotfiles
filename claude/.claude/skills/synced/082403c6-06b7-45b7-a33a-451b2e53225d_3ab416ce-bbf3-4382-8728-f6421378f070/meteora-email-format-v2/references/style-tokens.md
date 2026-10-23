# Style tokens — canonical

Derived from `spac-filing-digest/references/email_template.html`. If that file
changes, this one is stale.

## Wrapper

```
font-family:Helvetica,Arial,sans-serif; color:#1a1a1a; max-width:640px; line-height:1.5; font-size:13px
```

`max-width:640px` is load-bearing — it is what keeps the note readable in the
Outlook reading pane and on a phone.

## Type scale

| Element | Spec |
|---|---|
| Provenance stamp | `font-size:10.5px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.09em;margin:0 0 7px` |
| Title | `font-size:16px;font-weight:700;color:#0f2942` |
| Subline | `color:#475569;margin:2px 0 12px` |
| Section heading | `font-weight:700;color:#0f2942;margin:0 0 3px` |
| Body paragraph | `margin:0 0 8px` (inherits 13px) |
| Link | `color:#0f2942;font-weight:700` |
| Action / Calendar label | `<b style="color:#0f2942">` |
| Rail eyebrow | `font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:.07em;margin:0 0 10px` |
| Rail wrapper | `border-left:3px solid #e2e8f0;padding-left:13px;font-size:12px;color:#475569;line-height:1.55` |
| Rail sub-heading | `font-weight:700;color:#64748b;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;margin:0 0 3px` |
| Sources line | `margin:0 0 12px;font-size:10.5px;color:#94a3b8` |
| Table | `border-collapse:collapse;font-size:11.5px;color:#334155` + `width="100%" cellpadding="0" cellspacing="0"` |
| Table group row | `padding:4px 8px;background:#f1f5f9;border:1px solid #e2e8f0` `colspan="2"` |
| Table label cell | `padding:4px 8px;background:#f8fafc;border:1px solid #e2e8f0;width:14%` |
| Table value cell | `padding:4px 8px;border:1px solid #e2e8f0` |
| Footer | `margin:12px 0 0;padding-top:10px;border-top:1px solid #e2e8f0;font-size:11px;color:#94a3b8` |
| Attention span | `color:#c0392b;font-weight:700` |

## Palette — closed set

| Hex | Use |
|---|---|
| `#0f2942` | Titles, headings, link text, bold labels |
| `#1a1a1a` | Body text |
| `#334155` | Table text |
| `#475569` | Subline, rail body |
| `#64748b` | Stamp, rail sub-headings |
| `#94a3b8` | Rail eyebrow, sources, footer |
| `#c0392b` | Attention only — facts that need it, never emphasis |
| `#e2e8f0` | Borders and rules |
| `#f1f5f9` | Table group-row fill |
| `#f8fafc` | Table label-cell fill |

No other colours. `validate_html.py` fails the render on an off-palette hex.

## Why red is rationed

Red marks a fact that needs attention. Use it for decoration and the desk stops
seeing it, which means the one note where it matters reads like every other
note. Provenance is grey for the same reason — it is context, not an alarm.
