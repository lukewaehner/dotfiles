# Delta mode — re-reading a deal after new documents arrive

Use this when a first memo already exists in the chat and new material lands: the press release, deal slides,
the merger agreement, a sell-side note, a regulator statement. The user's question is then "has the
analysis changed?", not "write the memo again". A delta run reuses the earlier memo and only reports what moved.

## Rules

1. **Same-deal check.** Before using any retrieved file, confirm it names the same acquirer and target as
   the memo. A file for a different buyer on a similar target has been pulled in by mistake before.
2. **Three separate reads, each re-rated.** Rate each of these on its own, unchanged / higher / lower, with the
   reason:
   - First-review risk (does the review get past the initial filing and waiting period?)
   - Duration risk (how long does the longest approval take?)
   - Challenge or remedy risk (does a regulator sue, or demand a divestiture or ring-fence?)
3. **What-changed table.** Columns: item, earlier memo said, now says, source and section, effect on date or
   verdict. Include rows even for "no change" on the items a reader would worry about.
4. **Re-based approval clock.** Rebuild the Approval Clock Build from the new facts (agreement definitions,
   efforts clause, outside dates, guidance). State the new base-case close in days from announcement.
5. **Close inherited open questions.** When the agreement or a filing answers an earlier open question, mark
   the earlier statement "superseded" and give the answer with its citation. Do not leave the old
   question standing alongside the new fact.
6. **Guidance against the outside-date ladder.** Run `scripts/deal_clock.py ladder` with the company's own
   close guidance. State which extension step the guidance first fits within, and say whether a reverse
   termination fee exists. If the agreement has no reverse fee, write "no reverse fee" in the table.
7. **Price-independent hurdle table** (`scripts/deal_clock.py hurdle` at several prices) whenever no live
   price is available.
8. **Cite exactly.** Page footers print at the end of a page, so text appearing after the footer for page
   N sits on page N+1. Cite the page and the agreement section number, and the framework item where one applies.

9. **Re-run the screens the new document can now answer.** When the merger agreement is the new document,
   re-run the national-security screen (`references/national-security-screen.md`) and, on a health care target,
   the state build, against the filed text. Both depend on representations and definitions that a press release
   does not contain. Replace the earlier screen; do not leave a pre-agreement screen standing as current.
10. **Update the coverage ledger.** Any row the first run left as "not found" or moved to Open Questions is tried
    again against the new document (`references/standing-public-record.md`, section 7).

## Output shape

1. One-paragraph answer to "did it change?" with the verdict in plain words.
2. The three-read table.
3. The what-changed table.
4. The re-based clock.
5. Anything still open that would move the date or the verdict (materiality-ranked, as in the main memo).
6. The refreshed national-security screen and coverage ledger, when rules 9 and 10 applied.
