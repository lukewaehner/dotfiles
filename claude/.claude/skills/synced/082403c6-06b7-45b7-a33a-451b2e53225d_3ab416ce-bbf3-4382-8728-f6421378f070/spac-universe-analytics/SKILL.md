---
name: spac-universe-analytics
description: >-
  Use whenever a question spans the whole SPAC market, not one deal or Meteora's own book — counting, ranking, or averaging across all SPACs ever filed. Covers: counting SPACs by status (Completed/Withdrawn/Liquidated/Abandoned); ranking sponsors, directors, underwriters, or auditors by how many SPACs they're tied to; trending trust size, IPO proceeds, or IPO pop by exchange, industry, domicile, or year; or querying "the SPAC universe"/"universe database". Often phrased casually — "who are the top underwriters," "which auditor shows up the most," "breakdown by industry for an IC memo," "who's done the most deals over the years," "has trust size changed over time." Trigger whenever answering needs many SPACs at once, not one. NOT one SPAC's own terms/merger/trading; NOT current desk positions (spac-details); NOT the local SQLite refresh (spac-db-weekly-update). If unsure, run it by name: spac-universe-analytics.
---

# SPAC Universe Analytics

This skill turns a plain-English analytical question into a SQL query against
Meteora's SPAC universe database, and returns the answer in one fixed,
predictable shape — so a trader, an analyst, and someone building a deck all
get output they can trust and reuse without having to double-check the
plumbing every time.

The database is reached through two MCP tools: `universe-schema` (describes
the table) and `universe-query` (runs a read-only SELECT against it). Nothing
here is optional plumbing — each step below exists because skipping it
produced a wrong answer at least once already.

## Why schema-first, every single time

Never hardcode a column list in this skill. The source spreadsheet gets new
fields added to it over time (this is exactly how the `sponsor` and
`directors` columns showed up between two sessions), and a skill that
memorized yesterday's schema would silently miss them or guess wrong names.

Call `universe-schema` at the start of every invocation, before writing any
SQL. It returns each column's snake_case name, its original spreadsheet
header, its type, and — for low-cardinality columns — the exact set of values
present. Use that live output to build your query, not anything remembered
from a previous run or written below. (The columns mentioned in examples
throughout this file — `spac_status`, `domicile`, `directors`, `sponsor`,
`left_lead_uw` — are illustrative of what existed as of this writing, not a
contract.)

**Looking ahead to more tables.** Today there is one table, `universe_rows`.
If a second table is added later for cross-table joins, don't assume the
single-table world still holds — check what `universe-schema` (or whatever
its successor reports) describes, and look for `cik` as the join key: it's
already a clean, populated identifier on every row, and the natural anchor
for joining a SPAC's universe record to another table about the same entity.

## Step 1: Translate the question

Before writing SQL, pin down:

- **Dimension** — what's being ranked or grouped (a sponsor, a director, an
  underwriter, a domicile, an industry...)
- **Metric** — count of SPACs, sum/average of some numeric column, etc.
- **Scope** — all statuses, or only `Completed` / a specific `spac_status`?
  ("closed deals" means `spac_status = 'Completed'`; a bare "how many SPACs"
  usually means every status unless the user says otherwise.)
- **Time axis** — does the user want this broken out by year? If so, which
  date column is the right one — `ipo_date` for "when did this SPAC come to
  market", `closing_or_liquidation_date` for "when did this deal close",
  `announced_date` for "when was the deal announced". Pick the one that
  matches what's actually being asked, and say which one you used.
- **Filters** — any explicit constraints (a specific exchange, industry, date
  range).

**Match the row filter to whether the described event actually happened, not
just to whether a field is populated.** This is a real trap: a SPAC can have
a lead underwriter, a domicile, or a sponsor recorded in the data long before
it ever IPOs — and it can carry that same value forever if it's later
Withdrawn or Abandoned without ever pricing. So "which underwriters have led
the most IPOs" is not the same query as "which underwriters appear in the
`left_lead_uw` column" — the first requires the IPO to have actually
happened (a non-null `ipo_date`, in addition to a non-null `left_lead_uw`),
the second doesn't. Read the verb in the question — "led IPOs", "closed
deals", "raised in trust at IPO" — and ask what has to be true of a row for
that verb to apply to it, separately from which column holds the value you're
counting. Getting this wrong doesn't throw an error; it just quietly inflates
every count with deals that never happened.

## Step 2: Classify the target column — multi-value or single-value

This is the step that saved this skill from producing a nonsense ranking, and
it applies to every future field the same way.

Some text columns hold exactly one entity per row (e.g. a one-off SPAC
sponsor LLC, or a single lead underwriter) — grouping by these gives a real
ranking. Others hold a comma-separated list of multiple entities per row
(e.g. a board of several directors) — grouping by the raw string in SQL just
buckets by the whole string, which is meaningless; the list has to be split
in code first, and *then* counted.

Before ranking by any free-text column, sample a handful of real values with
a quick `SELECT column, othercontext FROM universe_rows WHERE column IS NOT
NULL LIMIT 15` and look at them:

- If `universe-schema` already lists a fixed `values` array for the column
  (like domicile or stock exchange), it's categorical and single-value —
  group by it directly.
- If the sampled values are single free-text strings with no repeats across
  different SPACs, treat it as single-value and say so — don't force a
  ranking out of it. Concretely: `sponsor` turned out to be a one-off,
  SPAC-specific LLC name — 708 of 711 sponsor/year combinations came back
  with exactly one closed deal, which isn't a ranking, it's just a list.
  Report that plainly instead of dressing it up as a leaderboard.
- If the sampled values are comma-separated multi-word tokens (several full
  names in one cell), it's multi-value — pull the raw rows (don't try to
  `GROUP BY` the raw string), split each cell on commas in Python, and count
  the individual entities. This is what makes `directors` a real ranking
  (top director sits on 16 SPACs), where `sponsor` isn't.

State which way you classified the column and why, in one line, as part of
the output — "treated `directors` as multi-value because sample rows contain
comma-separated full names" — so the reader can sanity-check your judgment
rather than trust it blindly.

**When single-value isn't the end of the story.** Sometimes a column being
single-value at the raw-string level (one sponsor LLC per SPAC) still leaves
a real, more useful question underneath it — "who are the repeat sponsors"
is a legitimate thing to want to know even though the literal `sponsor`
field never repeats. If the question is clearly asking about repeat
entities rather than repeat exact strings, it's worth a second pass: group
raw values that plausibly name the same underlying sponsor by their shared
distinctive brand word (e.g. "Gores Holdings II", "Gores Metropoulos", and
"Gores Sponsor VI" all share "Gores"), excluding generic first words that
would cause false merges (e.g. "Global", "New", "First", "American") since
those aren't brand identifiers. Always show the literal, raw-field answer
first — don't replace it — and label the normalized view clearly as a
heuristic with two named blind spots: it won't catch a sponsor that
rebranded entirely between vehicles, and a shared generic word can still
slip through and merge two unrelated sponsors. This extra pass is optional
and judgment-based — reach for it when a flat "not rankable" would leave the
real question unanswered, not as a default step for every single-value
column.

## Step 3: Run the query

Write the SQL against `universe_rows` using the exact snake_case names
`universe-schema` returned. `universe-query` defaults to a 200-row limit
(max 2000) — raise `limit` when you need the full result set for an
aggregate or a multi-value column that you're about to parse in Python.

If the result comes back too large for the tool's inline output, it gets
saved to a file on disk instead of an error you should retry around — that's
the expected large-result path, not a failure. Read that file directly with
Python via Bash (`json.load`) and process it there; don't try to page through
it with the Read tool in chunks, and don't eyeball or silently truncate it.
Every row that came back should be accounted for in the final CSV, even if
only the top 15–20 make it into the chat table.

## Step 4: Build the standard output bundle

Every invocation of this skill ends with the same five things, in this
order. Don't skip or reorder them — the whole point of wrapping this in a
skill is that the shape of the answer doesn't depend on who asked or how.

**1. Headline.** One plain-English sentence that answers the question
directly, before any table or chart. If you classified a column as
single-value/not-rankable in Step 2, say that here instead of presenting a
fake ranking.

**2. Table.** A markdown table inline in the chat, top 15–20 rows by
default (mention in your reply that the attached file has the rest). Never
paste a raw dump of hundreds or thousands of rows into the chat.

**3. Chart.** Default to a static PNG — it's the fastest to produce and
drops cleanly into an email or deck. Only build an interactive HTML/SVG
chart (following the `dataviz` skill's palette and mark guidance) if the
user explicitly asks for something interactive.

  Use `scripts/build_chart.py` to render it rather than writing chart code
  from scratch each time — it already handles both shapes this skill needs:

  ```
  # A straight ranking (one bar per category, sorted descending):
  python scripts/build_chart.py --input result.csv \
    --category-col director --value-col total_spacs \
    --shape ranking --top-n 15 \
    --title "Directors by number of SPACs" --output chart.png

  # A breakdown by year/period (one small-multiple panel per period,
  # top-N categories within each):
  python scripts/build_chart.py --input result.csv \
    --category-col director --value-col spacs_that_year --period-col ipo_year \
    --shape by_period --top-n 5 --max-periods 8 \
    --title "Top directors by SPACs, by IPO year" --output chart.png
  ```

  Pick `ranking` for a plain leaderboard question and `by_period` whenever
  the user asked "by year" or "over time". `--max-periods` keeps the panel
  count sane by defaulting to the most recent periods — say so if you had to
  drop older ones. Deliver the PNG with `SendUserFile`.

**4. Full data file.** Attach the complete result set as a CSV (or an .xlsx
if the user wants something pivotable in Excel) via `SendUserFile` — nothing
should be missing from this just because the chat table and chart are
top-N only.

**5. Caveats line.** Whenever the query touched a column with a
data-quality quirk — a single-value column that isn't really rankable, dates
missing for some rows and therefore excluded from a by-year cut, or the risk
that naive string-matching on names conflates two different real people or
entities who happen to share an identical string — say so plainly in one or
two sentences. Silence here is how a wrong ranking looks authoritative.

## Worked examples, for calibration

**"Rank directors by number of SPACs, overall and by year"** — `universe-schema`
→ found `directors` as a free-text column → sampled it and saw comma-separated
full names → classified multi-value → pulled all 1,875 rows with a non-null
`directors` value → split on commas in Python (6,245 unique directors, 1,173
with 2+ SPACs) → built an overall ranking (Randall Bort led with 16) and a
by-`ipo_date`-year breakdown (332 rows excluded from the by-year cut for
missing an IPO date) → delivered a headline, a top-15 table, a PNG bar chart,
a full CSV, and a caveat about the excluded rows and about naive
name-matching being unable to tell two different "Robert Smith"s apart.

**"Which underwriters have led the most SPAC IPOs"** — the row filter has to
match the verb: a SPAC with a `left_lead_uw` value but no `ipo_date` was
never actually taken public, so it doesn't count as an IPO "led". Scoping to
`left_lead_uw IS NOT NULL AND ipo_date IS NOT NULL` gives Cantor Fitzgerald
169 IPOs led — the earlier, wrong version of this query counted every row
with a `left_lead_uw` value regardless of whether the IPO happened, which
inflated the same count to 195. Same discipline applies to "closed deals"
(requires `spac_status = 'Completed'`, not just a `sponsor` value) and any
other question phrased around an event rather than a raw field.
