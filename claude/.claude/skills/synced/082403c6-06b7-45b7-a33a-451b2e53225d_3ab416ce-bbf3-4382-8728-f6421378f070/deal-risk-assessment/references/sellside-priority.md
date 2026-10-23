# Sell-Side Source Priority (Table 9 Ordering)

This tier list sets the row order for **Table 9 — Attributed Sell-Side Views on Completion** in `report-template.md` Section 7. It is a fixed institutional priority ranking, not a data-quality judgment — it reflects which desks/analysts the reader wants surfaced first, so order the table by it every time rather than by date, channel, or alphabetically.

Sort every attributed row into one of the three tiers below, then within a tier, preserve the exact firm order listed (the position number is the sort key). A firm listed with a named analyst matches primarily on the firm; if a surviving note from that firm is attributed to a different analyst than the one named here, it still sorts at that firm's tier position — the named analyst identifies the desk's usual contact, it isn't a filter that excludes other analysts at the same firm.

## High Weighting (sorts first)

1. United First Partners (UFP) — Anna Pavlik
2. FBN — Brian Lombardi
3. UBS — Evren Ergin
4. Market Securities — Jennifer Donaker
5. Cantor — David Connor
6. Raymond James — Paul Shea

## Medium Weighting (sorts after High)

7. Guggenheim — Aaron Glick
8. Elevation Securities
9. Churchill
10. Jones — Cabot Henderson
11. Roth — Mike Lesser
12. Baird — Brian Furbush

## Low Weighting (sorts after Medium)

13. BTIG
14. JP Morgan
15. Goldman Sachs
16. Clear Street

## ArbJournal, Chain Bridge Research, and other non-broker vector-database sources (sorts after Low)

ArbJournal deal files, Chain Bridge Research merger reports, and other non-broker items surfaced by the Vector Database are not broker notes and do not compete for tier positions. Give them their own clearly-labeled block, placed after the Low Weighting rows and before the unranked-firm block, sorted by date (most recent first), attributed from hit metadata ("ArbJournal — [report title], [date]"; "Chain Bridge Research — [analysts], [report title], [date]"). The separate block keeps broker views and journal/internal research visually distinct; the substance is kept in full.

## Unranked firms (sorts last)

Any firm gathered during sell-side enrichment that isn't on this list is unranked — place its rows after the ArbJournal / Chain Bridge / non-broker block, sorted by date (most recent first). Unranked is a position, not a demotion in substance: keep the underlying research, attribute it fully, and never drop a note just because its firm isn't on this list.

## Multiple notes from the same firm

If more than one attributed note from the same firm survives the enrichment/de-dup pass (e.g., two analysts at UBS, or the same analyst on two dates), keep each as its own row, grouped at that firm's tier position, sorted by date (most recent first) within the group.
