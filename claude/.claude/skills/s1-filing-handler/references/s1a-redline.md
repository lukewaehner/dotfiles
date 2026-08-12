# S-1/A amendment: redline against the prior filing

This backs Step 9 **case 2 only** — an S-1/A **when the chain already holds a prior extraction**.
A no-chain S-1/A is **not** redlined; it gets the full `spac-s1-extraction` run on the S-1/A itself
(Step 9 row 4 / Step 10). When you *do* redline, surface **only the relevant, impactful
changes** — the team already has the prior extraction in the thread.

## 1. Locate the immediately-prior filing

The baseline is the filing right before this amendment, not always the original S-1:

- S-1/A (#1) -> baseline is the original **S-1**
- S-1/A (#2) -> baseline is **S-1/A (#1)**
- S-1/A (#n) -> baseline is **S-1/A (#n-1)**

How: `edgar-filings(cik=<CIK>, form_type="S-1", limit=10)` and again for `form_type="S-1/A"`
(or a combined query if supported). Sort by filing date/accession. The baseline is the most
recent S-1-family filing with a date strictly before this amendment's. Capture its accession.

**No-chain S-1/A is NOT a redline.** If an S-1/A arrives and no `Internal <TICKER>` chain exists,
do **not** redline and do **not** pull the old S-1 — run the full `spac-s1-extraction` on the
**S-1/A itself** and open the chain (SKILL.md Step 9 row 4 / Step 10). You only redline once the
chain already holds a prior extraction: a **new** S-1/A vs the immediately-prior S-1/S-1-A.

## 2. Run the redline

Call the Meteora MCP `edgar-redline` with the prior accession as the base and this
amendment as the revision. (When you load the tool, confirm its exact parameter names/order
from the schema — pass the older filing as the "from"/base and the newer as the "to"/revision.)

If `edgar-redline` returns something usable, distill it. If the diff is enormous or the tool
errors on a large document, fall back to a **section-by-section** comparison using `extract-s1`:
call `extract-s1(cik=<CIK>, filing_date=<prior-date>, fields=[...])` for the baseline and
`extract-s1(cik=<CIK>, filing_date=<this-date>, fields=[...])` for the amendment — this returns
5–15K tokens of targeted section text per filing instead of the full 4M-char document. Use
`fields=["trust_account_terms","warrant_terms","business_combination_deadline","use_of_proceeds","cap_table","management","principal_stockholders"]`
to cover all the redline priority buckets. Compare only those (see the checklist below) rather
than dumping a raw diff. Only fall back to `edgar-filing-text` for sections `extract-s1` can't
locate (it will flag those in `fields_not_found`).

## 3. Extract the verbatim changes (no interpretation)

Pull the **actual changed text and numbers** from the `edgar-redline` output and quote them
`old -> new` (no paraphrase, no "what this means" read — the desk wants the raw deltas). But
**filter to the changes that actually matter**: report only the **relevant, impactful** changes —
the ones that move the investment case (the buckets below). Drop cosmetic diffs (cover dates,
amendment counters, pagination/TOC, typo/case, EX-23 consents) **and** immaterial substantive
tweaks that don't affect the desk's read (re-worded boilerplate risk factor, a moved sentence, a
trivially-restated mechanic). Impactful changes only, quoted verbatim.

Bucket the changes in **this priority order** (the desk's confirmed focus):

1. **Trust, redemption & deadline** — per-share trust / overfunding, trust-interest withdrawal
   terms, 15% redemption cap, redemption price, months-to-close, extension mechanics.
2. **Sponsor economics & dilution** — promote %, founder-share counts, anti-dilution / Crescent
   ($9.20-type) term, forfeiture; PIPE / anchor / private-placement size, participants, terms.
3. **Offering & security structure** — units offered, over-allotment, unit price, warrant/right
   ratio & strike, unit-split timing.
4. **Underwriter, risk & people** — underwriter & fees (upfront / deferred / PP purchase), new or
   removed risk factors, management / board / director changes, auditor change.
5. **Other** — any other **impactful** change that doesn't fit the buckets above.

Omit a bucket entirely if nothing in it changed — do **not** write "no change" lines.

## 4. Reply body format (verbatim, no fluff)

Lead with what it's redlined against, then the changes bucketed in the priority order above. Each
line is the document's own words/numbers, `"<old>" -> "<new>"`. **No** commentary, no "bomb", no
desk read, no "no material change" reassurance lines.

```
S-1/A — <TICKER> <SPAC Name> — amendment #<n>
Redlined vs: <prior form + accession + date>   |   This filing: <accession + date>

Trust / Redemption / Deadline:
- <field>: "<old>" -> "<new>"

Sponsor economics / Dilution:
- <field>: <old> -> <new>

Offering / Structure:
- <field>: <old> -> <new>

Underwriter / Risk / People:
- <field>: <old> -> <new>

Other:
- <field>: <old> -> <new>

Source: EDGAR <this accession> <url>
```

Omit any bucket with no changes (don't pad). If the whole amendment is cosmetic, one line only:
`No substantive changes — <what it was, e.g. adds Exhibit 23.1 auditor consent>.` Quote real
numbers verbatim; never approximate or interpret.

## 5. Ticker / subject: rename the thread when the amendment reveals a ticker

The canonical subject is `Internal <TICKER>` (bare common ticker, no brackets/name — Luke's
`spac-filing-digest` house format). A chain is often opened `Internal <SPAC Name>` at the initial
S-1 because no ticker
existed yet; when a later S-1/A assigns the ticker, **rename the thread on the reply**.

Mechanism: use **`reply_all_rename_thread(message_id, body, new_subject, html=True, confirmed=True)`** (Graph createReplyAll -> set new_subject -> send). It
creates the reply *inside the existing conversation*, so setting a new `subject` renames the
thread **without breaking threading** — the `conversationId` is preserved. Pass
`new_subject="Internal <TICKER>"`.

- Thread subject already equals canonical -> reply-all, subject unchanged.
- Thread subject differs (was `Internal <SPAC Name>`, name-only, or you're replying on a stray
  `Re: [S-1/A] Name` alert chain) -> reply-all with `subject=<canonical>` to normalize it.
- Still no ticker -> keep `Internal <SPAC Name>`.
- Add a one-line note at the top of the reply body ("Ticker now assigned: **CGCC** — thread
  renamed to `Internal CGCC`.") and record the corrected title in the state
  file's `titles` map so later runs recognize the thread.

If `reply_all_rename_thread` is unavailable in some environment, fall back to a plain
`reply_all_email` (subject stays `Re: <original>`), surface the ticker in the body, and flag the
rename as pending in the run summary.
