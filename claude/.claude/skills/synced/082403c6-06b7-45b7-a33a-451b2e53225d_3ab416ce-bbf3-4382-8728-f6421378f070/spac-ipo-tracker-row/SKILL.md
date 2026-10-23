---
name: spac-ipo-tracker-row
description: Generate a one-click copy-paste Excel row for Meteora's internal SPAC Unit IPO Tracker. Trigger when the user asks to 'get me the row', 'copy paste for the tracker', 'tracker row', 'IPO tracker row', 'give me the Excel row', 'paste into the tracker', or any request to produce a copy-pasteable row for the internal unit IPO spreadsheet. Also trigger proactively at the END of any S-1 extraction (spac-s1-extraction skill) when the user says 'and get me the copy paste' or 'plus the tracker row'. Do NOT trigger for general Excel/spreadsheet tasks unrelated to the IPO tracker. This skill produces a React artifact with all values pre-filled by Claude — the user just clicks one button to copy and pastes into Excel.
---

# SPAC IPO Tracker Row Copier

## What This Skill Does

Generates a React artifact (.jsx) containing a single pre-filled row for Meteora's internal SPAC Unit IPO Tracker spreadsheet. Claude extracts all relevant fields from the S-1 extraction (or from conversation context) and hardcodes them into the artifact. The user clicks "Copy Row to Clipboard" and pastes into Excel. No form filling — Claude does all the work.

## Column Layout (A–O)

| Col | Label           | Type          | Source / Notes                                                |
|-----|-----------------|---------------|---------------------------------------------------------------|
| A   | Name            | Text          | SPAC ticker (e.g. IPFX)                                      |
| B   | Unit Price      | Number        | Default 10.00 (unit IPO price)                                |
| C   | Pos             | **BLANK**     | User fills manually — always leave empty                      |
| D   | Notes           | Text          | Domicile, warrant/rights coverage shorthand, WC withdrawals   |
| E   | W or R          | Text          | "W", "R", or "N/A"                                           |
| F   | Multiplier      | Number        | Coverage denominator (1/3W → 3, 1/2W → 2, 1/5R → 5)         |
| G   | IPO Date        | Date          | Today's date in M/D/YYYY format                              |
| H   | Max Date        | Excel formula | `=EDATE(G{r},{months})`                                      |
| I   | CIT (IPO DATE)  | Number        | Trust per unit at IPO — 10.00 unless overfunded (10.025, 10.05, etc.) |
| J   | eCIT Today      | Excel formula | See exact formula below                                       |
| K   | Bid Yield       | Number        | Default 0.05 (manual input — user changes in Excel)           |
| L   | Bid             | Excel formula | See exact formula below                                       |
| M   | Imp W           | Excel formula | See exact formula below                                       |
| N   | Imp R           | Excel formula | See exact formula below                                       |
| O   | Max Trust       | Excel formula | See exact formula below                                       |

`$C$4` = T-bill rate (set in the sheet header by the user).
`{r}` = target row number (default 8).

## Exact Formulas

These formulas use INDIRECT R1C1-style and structured table references. The RC offsets are calibrated to the A–O column layout above. Do NOT change the style or offsets.

**H — Max Date:**
```
=EDATE(G{r},{months})
```

**J — eCIT Today:**
```
=[@[CIT (IPO DATE)]]*(1+$C$4)^((TODAY()-INDIRECT("RC[-3]",FALSE))/365)
```
RC[-3] from J = G (IPO Date). Uses the structured reference to CIT (IPO DATE) in column I as the trust base.

**L — Bid:**
```
=INDIRECT("RC[3]",FALSE)/(1+INDIRECT("RC[-1]",FALSE))^((INDIRECT("RC[-4]",FALSE)-TODAY())/365)
```
RC[3] from L = O (Max Trust). RC[-1] from L = K (Bid Yield). RC[-4] from L = H (Max Date).

**M — Implied Warrants:**
```
=IF([@[W or R]]="W",([@[Unit Price]]-[@[Bid ]])*[@Multiplier],"-")
```
Structured table references. Header names must match the user's Excel table. Note the trailing space in `[@[Bid ]]`.

**N — Implied Rights:**
```
=IF(INDIRECT("RC[-8]",FALSE)="R",(INDIRECT("RC[-10]",FALSE)-INDIRECT("RC[-2]",FALSE))*INDIRECT("RC[-7]",FALSE),"-")
```
User-provided formula — copy verbatim. RC offsets are calibrated to the user's actual Excel table layout.

**O — Max Trust:**
```
=[@[CIT (IPO DATE)]]*(1+$C$4)^((INDIRECT("RC[-7]",FALSE)-INDIRECT("RC[-8]",FALSE))/365)
```
RC[-7] from O = H (Max Date). RC[-8] from O = G (IPO Date). Uses the structured reference to CIT (IPO DATE) in column I as the trust base.

## How to Extract Fields from an S-1

Map the S-1 extraction to the DATA block:

- **name**: SPAC common stock ticker (not the unit ticker)
- **price**: Almost always "10.00" — only change if non-standard unit price
- **notes**: Build from these S-1 fields:
  - Domicile (e.g. "Cayman", "Delaware")
  - Warrant/Rights coverage shorthand (e.g. "1/3W", "1/2W", "1/5R", "1/10R")
  - Working capital withdrawal terms (e.g. "$500K/yr WC", "no WC", "$750K/yr WC")
  - Keep it terse — this is a notes cell
- **wOrR**: "W" if warrants, "R" if rights, "N/A" if neither
- **mult**: The denominator of the coverage fraction (1/3W → 3, 1/2W → 2, whole warrant → 1)
- **ipo**: Today's date in M/D/YYYY format
- **months**: SPAC timeline in months (usually 18 or 24; check Section 2 Timeline)
- **citIpo**: Trust per unit at IPO — usually "10" but use "10.025", "10.05", etc. if overfunded (check Section 3 Trust details in the S-1)
- **yield**: Always "0.05" (default; user changes manually in Excel)

## Artifact Template

Generate the artifact as a `.jsx` file saved to `/mnt/user-data/outputs/{ticker}_row.jsx`. Use this exact template — only modify the DATA block and comment at top:

```jsx
import { useState } from "react";

// ===== {TICKER} — {FULL SPAC NAME} =====
const ROW = 8;
const DATA = {
  name: "{ticker}",
  price: "{price}",
  notes: "{notes}",
  wOrR: "{wOrR}",
  mult: "{mult}",
  ipo: "{ipo_date_M/D/YYYY}",
  months: {months},
  citIpo: "{citIpo}",
  yield: "0.05",
};
// ========================================================

const r = ROW;
const cells = [
  { col: "A", label: "Name", val: DATA.name },
  { col: "B", label: "Unit Price", val: DATA.price },
  { col: "C", label: "Pos", val: "", blank: true },
  { col: "D", label: "Notes", val: DATA.notes },
  { col: "E", label: "W or R", val: DATA.wOrR },
  { col: "F", label: "Multiplier", val: DATA.wOrR === "N/A" ? "" : DATA.mult },
  { col: "G", label: "IPO Date", val: DATA.ipo },
  { col: "H", label: "Max Date", val: `=EDATE(G${r},${DATA.months})`, formula: true },
  { col: "I", label: "CIT (IPO DATE)", val: DATA.citIpo },
  { col: "J", label: "eCIT Today", val: `=[@[CIT (IPO DATE)]]*(1+$C$4)^((TODAY()-INDIRECT("RC[-3]",FALSE))/365)`, formula: true },
  { col: "K", label: "Bid Yield", val: DATA.yield },
  { col: "L", label: "Bid", val: `=INDIRECT("RC[3]",FALSE)/(1+INDIRECT("RC[-1]",FALSE))^((INDIRECT("RC[-4]",FALSE)-TODAY())/365)`, formula: true },
  { col: "M", label: "Imp W", val: `=IF([@[W or R]]="W",([@[Unit Price]]-[@[Bid ]])*[@Multiplier],"-")`, formula: true },
  { col: "N", label: "Imp R", val: `=IF(INDIRECT("RC[-8]",FALSE)="R",(INDIRECT("RC[-10]",FALSE)-INDIRECT("RC[-2]",FALSE))*INDIRECT("RC[-7]",FALSE),"-")`, formula: true },
  { col: "O", label: "Max Trust", val: `=[@[CIT (IPO DATE)]]*(1+$C$4)^((INDIRECT("RC[-7]",FALSE)-INDIRECT("RC[-8]",FALSE))/365)`, formula: true },
];

const clipboardText = cells.map(c => c.val).join("\t");

export default function SPACRowCopier() {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try { await navigator.clipboard.writeText(clipboardText); }
    catch { const a = document.createElement("textarea"); a.value = clipboardText; document.body.appendChild(a); a.select(); document.execCommand("copy"); document.body.removeChild(a); }
    setCopied(true); setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ fontFamily: "-apple-system, BlinkMacSystemFont, sans-serif", maxWidth: 820, margin: "0 auto", padding: "16px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 14 }}>
        <div>
          <div style={{ fontSize: 16, fontWeight: 700 }}>{DATA.name}</div>
          <div style={{ fontSize: 10, color: "#999" }}>Row {r} · CIT ${DATA.citIpo} · {DATA.months}mo · {DATA.notes}</div>
        </div>
        <div style={{ fontSize: 11, color: "#888", fontWeight: 600 }}>IPO Tracker Row</div>
      </div>

      <div style={{ overflowX: "auto", border: "1px solid #e0e0e0", borderRadius: 8, marginBottom: 14 }}>
        <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 11, whiteSpace: "nowrap" }}>
          <thead>
            <tr>
              {cells.map(c => (
                <th key={c.col} style={{ padding: "6px 10px", background: c.blank ? "#fff8e1" : "#f5f5f5", borderBottom: "2px solid #ddd", fontWeight: 700, textAlign: "left", color: "#555", fontSize: 10 }}>
                  <span style={{ color: "#bbb" }}>{c.col}</span> {c.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr>
              {cells.map(c => (
                <td key={c.col} style={{
                  padding: "8px 10px", borderBottom: "1px solid #eee",
                  fontFamily: c.formula ? "monospace" : "inherit",
                  fontSize: c.formula ? 10 : 12,
                  color: c.blank ? "#ccc" : c.formula ? "#0066cc" : "#1a1a1a",
                  fontWeight: c.formula ? 400 : 500,
                  fontStyle: c.blank ? "italic" : "normal",
                  background: c.blank ? "#fffde7" : "transparent",
                }}>
                  {c.blank ? "(manual)" : c.val}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>

      <button onClick={copy} style={{
        width: "100%", padding: "14px", border: "none", borderRadius: 8,
        fontSize: 14, fontWeight: 700, cursor: "pointer", transition: "all 0.15s",
        background: copied ? "#16a34a" : "#111", color: "#fff",
      }}>
        {copied ? "✓ Copied — Paste into Row " + r : "Copy Row to Clipboard"}
      </button>
    </div>
  );
}
```

## Instructions

1. Extract the fields from the S-1 extraction or conversation context using the mapping above.
2. Fill in the DATA block in the template. Do not leave any placeholder strings — every field must be a real value.
3. Save the artifact to `/mnt/user-data/outputs/{ticker}_row.jsx`.
4. Present the file with `present_files`.
5. Confirm to the user what was filled in: ticker, domicile, coverage, CIT (IPO DATE) trust base, timeline.

## Edge Cases

- **Rights instead of warrants**: Set wOrR to "R", mult to the rights denominator (e.g. 1/10 right → 10). Imp W returns "-", Imp R calculates.
- **No warrants or rights**: Set wOrR to "N/A", mult to "". Both Imp W and Imp R return "-".
- **Overfunded trust**: If trust is $10.025 per unit at IPO, set citIpo to "10.025". This flows into CIT (IPO DATE), eCIT Today, and Max Trust automatically.
- **Non-standard timeline**: Some SPACs are 18 months. Check the S-1 Section 2 Timeline field.
- **Multiple classes of warrants/rights**: Use the public warrant/right coverage. Note any additional instruments in the Notes field.
