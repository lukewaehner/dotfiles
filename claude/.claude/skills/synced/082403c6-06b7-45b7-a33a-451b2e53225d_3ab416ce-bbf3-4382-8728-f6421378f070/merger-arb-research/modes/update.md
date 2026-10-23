# Update: fold new information into the deal

Goal: when something new arrives on a deal we are already researching (a broker note, a point from a desk or
internal discussion, a filing, a date passing, a price move), put it in the deal's living document, check it,
move the risks and the call if they should move, and tell the user in a few lines what changed. The user should
never have to repeat context: the living document is how the next session knows what was discussed and where we
stand. Time budget 2 to 10 minutes; a big filing such as the preliminary proxy deserves a full read.

## 1. Read the living document

Open `merger_arb_deals/{TICKER}/{TICKER}_living_doc.md` (SKILL.md, "Living document"). Note the current call,
the cases table, the risks, the unusual terms, the research tree and when it was last updated. If there is no living document, say so, run
the mode that fits (Minute-1 for an announced deal, Rumor for a rumored one) and build it, then apply the new
information.

## 2. Classify each input

Record who it came from, when, and how much weight it can carry, from strongest to weakest: a primary filing or
the agreement; a company statement or call; a broker or sell-side note; a desk or internal discussion; a press
report; a rumor. For an internal discussion, record who said it and the reasoning, because the desk's reasoning
is information too, whether or not the facts in it check out. Split a long input into separate claims; each
claim gets its own row in the information log.

## 3. Check

- Split the input into claims and treat each as a flag (SKILL.md, "Flag what could matter"). If it names a term,
  clause or fact that is not in the research tree, open a branch for it, follow it, and say in the report that
  we had missed it.
- A claim of fact is tested against the primary source (the agreement, the filing, the regulator's register;
  broker-note checks are in `playbook/precedents-and-sources.md`). A claim that cannot be tested stays in the log
  as unverified and does not move the call.
- Pull EDGAR again for anything filed since the living document was last updated: the proxy, 8-Ks, ownership
  filings, going-private disclosure, the antitrust notices. A filing may be the thing the user is referring to.
- If the input disagrees with our view, test the claim the disagreement rests on and record both sides. Say in
  the report whether our view moved and why.

## 4. Move what should move

Go through the living document and ask what this input touches:

- **Risks**: change a risk's status (Blocked, Bounded, Resolved), its trigger or its effect, or add a risk in
  the format from SKILL.md, "Writing the risks". A clause with a second consequence gets its own entry.
- **Unusual terms and research tree**: add any term the input surfaced, and record the branch it opened and
  where it landed.
- **Price test and cases**: re-run `deal_clock.py cases` with the new last price and the trigger prices. Add,
  move or drop dated cases when a fact changes a date. A new date goes through `deal_clock.py`. No probability
  of ours goes on a case, a risk or the deal; the market-implied chance of failure is recomputed.
- **Catalysts**: mark an event Happened with its date and what it showed; add the dates it created.
- **Open questions**: close the ones it answers; add the ones it raises, each with what settles it.

### Milestones and what to read in them

| Event | Read | Looking for |
|---|---|---|
| Preliminary proxy | Background of the Merger; financing; interests of directors and officers; regulatory approvals; opinion of the financial adviser; any going-private filing | Number of bidders and who dropped, confidentiality and standstill terms, debt and equity amounts, preferred investors, rollover size, whether insiders are filing persons, foreign filings, meeting date |
| Definitive proxy | Differences from the preliminary; meeting date; adviser recommendations | Timing against the debt-marketing window and the Q3 and audit dates |
| Quarterly results | Results against guidance; any statement on the deal; risk factors | Material adverse effect carve-outs, customer or financing news |
| Antitrust filing or expiry | Press release, regulator notices, early termination list | Second request, withdrawal and refiling |
| Bond or loan launch | Offering terms, ratings, pricing, escrow | Funding certainty, window timing |
| Vote | Results and any adjournment | Margin, adjournment, new bidders |
| Complaint or injunction motion | Docket entry, hearing date | Whether closing can be blocked; schedule |
| Price move without news | Run Spread check (`modes/spread-check.md`) | Cause |

## 5. Decide

State the call before and after. If it changed, say which fact changed it and what price it implies. If it did
not change, say so and why the new information was already inside the numbers.

## 6. Report in the chat, then write the document

Reply with these lines and nothing more unless the news is large:

```
**Update: {TARGET} ({weekday} {date} {time})**
**Came in:** {source, type, how reliable} - {the claim in one line}
**Checked:** {each claim: against what, and whether it held}
**Moved:**
- {Risk headline}: {old status} → {new status}, {why}
- {New risk or unusual term, if any, with "missed in earlier read" where true}
- {Cases, dates and numbers that changed; or "nothing"}
**Call:** {before} → {after} {and the price}
**Watch next:** {the next dated event and what it would show}
```

Then update the living document: the information log (one row per claim), the risks, unusual terms and research tree as needed, and a
dated changelog line. No file goes to the user unless they ask.
