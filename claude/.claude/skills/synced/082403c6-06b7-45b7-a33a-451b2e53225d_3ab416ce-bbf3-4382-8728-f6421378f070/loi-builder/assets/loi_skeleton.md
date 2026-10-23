# LOI Skeleton — Section Assembly Order

The order in which clauses from `references/sponsor_friendly_clauses.md` get assembled. Use BIXI-family inline-heading format (not the IVCB two-column table).

## Section sequence (in order)

```
[Header block — date, confidential marker, target address block, salutation]

[Opening 3 paragraphs from "Header / Preamble"]

Proposed Terms and Conditions of Transaction       (section divider, bold)

1.  Transaction
2.  Board of Directors
3.  US Listing
4.  Timing
5.  Valuation
6.  Lock-Up and Registration Rights
7.  Founder Share Haircut
8.  Public Warrants Treatment
9.  PIPE
10. Minimum Cash Condition
11. LTIP
12. Definitive Agreement
13. Financial Statements and Financial Information

Binding LOI Provisions                              (section divider, bold)

14. Non-Exclusivity with Right of First Negotiation
15. Due Diligence Access
16. Management Availability
17. Choice of Law and Jurisdiction Matters
18. Confidentiality
19. Expenses
20. Trust Account Waiver
21. Term
22. General Provisions

[Signature Page Follows]
[page break]
[Signature blocks: Sponsor first, then "ACCEPTED and AGREED:" Target]
```

## Sections OMITTED (per Meteora spec)

- Shareholder Earnout
- Founder Share Earnout (separate from haircut)
- Termination Fee / break-up fee
- Fiduciary out / Superior Proposal carve-out
- Post-Transaction Capital Structure / Exhibit A
- Foreign-jurisdiction conditions (Australian scheme, FIRB, ATO, court approval, independent expert)
- Convertible note add-on (unless user explicitly requests, then add as section "Convertible Note Financing" between Min Cash Condition and LTIP)
- Employee Equity Plan at 20% (use the 10% LTIP language)

## Formatting conventions

- **Page size:** US Letter (12240 × 15840 DXA), 1-inch margins
- **Default font:** Arial 11pt
- **Title at top:** "[SPONSOR_SHORT] x [TARGET_SHORT] – Letter of Intent" — bold, ~14pt, left-aligned or centered
- **Date line:** below title, regular weight
- **"Confidential" marker:** italic, below date, optional
- **Section headings:** Bold + italic, ~12pt, e.g. ***Transaction***
- **Section dividers** ("Proposed Terms and Conditions of Transaction" and "Binding LOI Provisions"): Bold, ~13pt, centered or with extra space above
- **Defined terms:** Bold on first appearance only (e.g., **Trust Account**, **Definitive Agreement**, **Sponsor**, **Sellers**, **Founder Shares**, **Closing**, **LOI**, **Parties**, **Transaction**, **Share Consideration**, **Transaction Consideration**, **Valuation**, **Mutual Non-Disclosure Agreement**, **Public Stockholders**, **Released Claims**, **Offer Expiration Time**, **Term**, **Related Parties**, **Competing Proposal**, **Right of First Negotiation Period**, **Converted Warrants**, **LTIP**, **PIPE**, **IPO**, **SEC**, **Exchange**, **BCA**)
- **Spacing:** Single line spacing within paragraphs, ~6pt before/after each paragraph
- **Page numbers:** Bottom-center, optional
- **Line breaks:** Use proper Paragraph elements; never `\n` inside a TextRun

## Signature block

```
Very truly yours,

[Blank line]

[SPONSOR_FULL_NAME]                                  (bold)

By: ___________________________
Name: [SPONSOR_SIGNATORY_NAME]

[2 blank lines]


ACCEPTED and AGREED:

[Blank line]

[TARGET_FULL_NAME]                                   (bold)

By: ___________________________
Name: [TARGET_SIGNATORY_NAME]
```
