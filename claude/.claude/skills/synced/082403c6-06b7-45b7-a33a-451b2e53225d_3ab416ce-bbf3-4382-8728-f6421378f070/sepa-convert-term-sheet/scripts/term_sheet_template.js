/**
 * Meteora Capital – Term Sheet Generator
 * ----------------------------------------
 * Generates a professional .docx term sheet for SEPA + Convertible Pre-Paid
 * Advance transactions. Customize the DEAL PARAMETERS section below, then run:
 *
 *   node term_sheet_template.js
 *
 * Outputs: ./output/[TICKER]_Term_Sheet_Meteora.docx
 *
 * Dependencies: npm install -g docx
 *               place meteora_logo.png in same directory as this script
 */

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
  PageBreak, UnderlineType, LevelFormat, ImageRun
} = require('docx');
const fs = require('fs');
const path = require('path');

// ═══════════════════════════════════════════════════════════════════════════════
// DEAL PARAMETERS — customize these for each transaction
// ═══════════════════════════════════════════════════════════════════════════════

const COMPANY_NAME   = "Company Name, Inc.";       // full legal name
const TICKER         = "TICK";                     // Nasdaq/NYSE ticker
const DATE           = "April 1, 2026";            // term sheet date

// ── Pre-Paid Advance (Convertible Note) ──────────────────────────────────────
// To calculate: PRINCIPAL = FUNDED / (1 - OID_DECIMAL)
// e.g. $4M funded @ 10% OID → $4,000,000 / 0.90 = $4,444,444 principal
const FUNDED_AMT     = "$4,000,000";               // cash Meteora wires
const PRINCIPAL_AMT  = "$4,444,444";               // face value of the note
const OID_PCT        = "10%";                      // original issue discount
const OID_DIVISOR    = "90%";                      // 1 - OID_DECIMAL (for prose)

// ── SEPA ─────────────────────────────────────────────────────────────────────
const SEPA_MAX       = "$100,000,000";             // max commitment
const COMMIT_PERIOD  = "36 months";                // facility duration

// ── Pricing ──────────────────────────────────────────────────────────────────
const CO_DISC        = "97%";                      // company-initiated advance: % of VWAP on notice date
const INV_DISC       = "94%";                      // investor-initiated advance: % of lowest 5-day VWAP
const VAR_DISC       = "94%";                      // variable conversion price (match investor-initiated)
const FIXED_CONV     = "$1.43";                    // fixed conversion price
const FLOOR_PCT      = "20%";                      // floor as % of fixed price
const FLOOR_PRICE    = "$0.286";                   // floor price = FIXED_CONV × FLOOR_PCT

// ── Fees ─────────────────────────────────────────────────────────────────────
const COMMIT_FEE_PCT = "1%";                       // % of SEPA commitment
const COMMIT_FEE_AMT = "$1,000,000";               // = SEPA_MAX × COMMIT_FEE_PCT
const DILIGENCE_FEES = "$45,000";                  // legal/diligence fee cap

// ═══════════════════════════════════════════════════════════════════════════════
// FORMATTING CONSTANTS — do not change unless rebranding
// ═══════════════════════════════════════════════════════════════════════════════

const SECTION_FILL = "DDDDDD";   // gray section header background
const FONT         = "Times New Roman";
const FONT_SIZE    = 20;         // 10pt (docx uses half-points)

const LW = 2000;                 // label column width (DXA)
const CW = 7360;                 // content column width (DXA)
const TW = LW + CW;             // total table width = 9360 DXA (6.5")

// ═══════════════════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

const border    = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders   = { top: border, bottom: border, left: border, right: border };
const noBorder  = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// Text run helpers
const T  = s => new TextRun({ text: s, font: FONT, size: FONT_SIZE });
const B  = s => new TextRun({ text: s, bold: true, font: FONT, size: FONT_SIZE });
const IT = s => new TextRun({ text: s, italics: true, font: FONT, size: FONT_SIZE });
const BU = s => new TextRun({ text: s, bold: true, underline: { type: UnderlineType.SINGLE }, font: FONT, size: FONT_SIZE });

// Paragraph helpers
const pp = (runs, opts = {}) =>
  new Paragraph({ children: Array.isArray(runs) ? runs : [runs], spacing: { before: 40, after: 40 }, ...opts });
const sp = () => new Paragraph({ children: [], spacing: { before: 60, after: 60 } });

// Table cell helpers
const cell = (w, children) => new TableCell({
  borders,
  width: { size: w, type: WidthType.DXA },
  margins: { top: 80, bottom: 80, left: 100, right: 100 },
  verticalAlign: VerticalAlign.TOP,
  children: Array.isArray(children) ? children : [children],
});

// Standard two-column term row: [label (gray)] | [content (white)]
function row(label, content) {
  const labelCell = new TableCell({
    borders,
    width: { size: LW, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    verticalAlign: VerticalAlign.TOP,
    shading: { fill: "F5F5F5", type: ShadingType.CLEAR },
    children: Array.isArray(label) ? label : [pp([B(label)])],
  });
  const contentCell = new TableCell({
    borders,
    width: { size: CW, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    verticalAlign: VerticalAlign.TOP,
    children: Array.isArray(content) ? content : [pp([T(content)])],
  });
  return new TableRow({ children: [labelCell, contentCell] });
}

// Full-width gray section header row
function sectionHeader(text) {
  return new TableRow({ children: [
    new TableCell({
      borders, columnSpan: 2,
      width: { size: TW, type: WidthType.DXA },
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      shading: { fill: SECTION_FILL, type: ShadingType.CLEAR },
      children: [pp([B(text)])],
    })
  ]});
}

// Logo header table — title left, logo upper right
let logoData = null;
const logoPath = path.join(__dirname, 'meteora_logo.png');
try { logoData = fs.readFileSync(logoPath); } catch(e) {
  console.warn('Warning: meteora_logo.png not found. Header will render without logo.');
}

function logoHeaderTable(titleLines) {
  const nb = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const nb4 = { top: nb, bottom: nb, left: nb, right: nb };

  const titleChildren = titleLines.map((line, i) =>
    new Paragraph({
      children: [new TextRun({ text: line, bold: true, font: FONT, size: i === 0 ? 26 : 22 })],
      spacing: { before: 0, after: 40 },
    })
  );

  const logoCell = logoData
    ? new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new ImageRun({ data: logoData, transformation: { width: 120, height: 120 }, type: "png" })],
        spacing: { before: 0, after: 0 },
      })
    : new Paragraph({ children: [] });

  return new Table({
    width: { size: TW, type: WidthType.DXA },
    columnWidths: [6800, 2560],
    borders: { top: nb, bottom: nb, left: nb, right: nb, insideH: nb, insideV: nb },
    rows: [new TableRow({ children: [
      new TableCell({
        borders: nb4, width: { size: 6800, type: WidthType.DXA },
        margins: { top: 0, bottom: 0, left: 0, right: 0 },
        verticalAlign: VerticalAlign.CENTER,
        children: titleChildren,
      }),
      new TableCell({
        borders: nb4, width: { size: 2560, type: WidthType.DXA },
        margins: { top: 0, bottom: 0, left: 0, right: 0 },
        verticalAlign: VerticalAlign.CENTER,
        children: [logoCell],
      }),
    ]})]
  });
}

// ═══════════════════════════════════════════════════════════════════════════════
// STANDARD METEORA PREAMBLE (only company name changes)
// ═══════════════════════════════════════════════════════════════════════════════

const preambleText =
  `This term sheet (the "Term Sheet") dated as of ${DATE} is intended for discussion purposes only and does not ` +
  `represent or constitute an offer, undertaking or commitment on the part of Meteora Capital LLC or any of its ` +
  `affiliates ("Meteora", "Investor" or "Investors") to arrange or provide financing to ${COMPANY_NAME} (the "Company") ` +
  `or any of its affiliates or any other person. Except for this preamble, the epilogue at the end of the Term Sheet ` +
  `captioned "Confidentiality and Exclusivity" and the sections captioned "ROFR" and "Governing Law", all terms set out ` +
  `herein are non-binding and any obligation or commitment of Meteora or any of its affiliates is subject to the completion ` +
  `of due diligence, investment committee and other internal approvals and the execution and delivery of definitive ` +
  `transaction documentation (the "Definitive Documentation"), in each case as may be satisfactory to Meteora at its sole ` +
  `discretion. Nothing herein shall be construed to compel Meteora to commit to purchase securities of the Company or ` +
  `secure financing on behalf of the Company by third parties, ensure that Meteora executes agreements with the Company, ` +
  `or guarantee the obligations of Meteora under any definitive documentation by and among the Company and itself.`;

// ═══════════════════════════════════════════════════════════════════════════════
// TERM TABLE ROWS
// ═══════════════════════════════════════════════════════════════════════════════

const termRows = [

  // Parties
  row("Issuer",   `${COMPANY_NAME} (Nasdaq: ${TICKER}) (the "Company")`),
  row("Investor", `Meteora Capital LLC and/or its affiliated funds and managed accounts (the "Investor" or "Meteora")`),
  row("Currency", `US Dollars ("USD" or "$")`),
  row("Date",     DATE),

  // ── I. TRANSACTION OVERVIEW ────────────────────────────────────────────────
  sectionHeader("I.  TRANSACTION OVERVIEW"),

  row("Transaction\nSummary", [
    pp([T(`This Term Sheet contemplates an integrated financing package consisting of two components:`)]),
    pp([B(`(1) Standby Equity Purchase Agreement ("SEPA"): `), T(`A committed facility of up to ${SEPA_MAX} over ${COMMIT_PERIOD}, under which the Company may draw Advances in the form of equity (share issuances) or convertible promissory notes ("Convertible Notes"), depending on prevailing trading volume at the time of each Advance.`)]),
    pp([B(`(2) Upfront Pre-Paid Advance: `), T(`An initial funded advance of ${FUNDED_AMT} at closing (${PRINCIPAL_AMT} principal at ${OID_PCT} OID), structured as a Convertible Note and counting toward the SEPA Commitment Amount.`)]),
  ]),

  // ── II. SEPA ───────────────────────────────────────────────────────────────
  sectionHeader("II.  STANDBY EQUITY PURCHASE AGREEMENT (SEPA)"),

  row("Maximum\nCommitment",
    `Up to ${SEPA_MAX} in aggregate (the "Commitment Amount"), available to the Company over the Commitment Period, inclusive of all amounts drawn under any Convertible Notes issued pursuant hereto.`),

  row("Commitment\nPeriod",
    `${COMMIT_PERIOD} from the effective date of the definitive SEPA agreement (the "Commitment Period").`),

  row("Advance Structure\n(Equity vs. Debt)", [
    pp([T(`Upon receipt of an Advance notice from the Company, Meteora shall fund each Advance as follows:`)]),
    pp([BU("Equity Advance: "), T(`Where the prevailing ADTV supports settlement in shares, the Advance will be funded in exchange for newly issued shares of Common Stock at the Purchase Price (as defined below). Equity Advances shall be sized so that the shares issuable do not exceed the Daily Volume Limitation.`)]),
    pp([BU("Debt Advance (Convertible Note): "), T(`Where prevailing ADTV is insufficient to support full equity settlement, or where the parties mutually agree, all or a portion of an Advance will be funded as a Convertible Note on the terms set forth in Section III. Each Convertible Note issued as a Debt Advance reduces the remaining Commitment Amount dollar-for-dollar.`)]),
    pp([BU("Concurrent SEPA Availability: "), T(`For the avoidance of doubt, the SEPA facility shall remain available and fully operational during any period in which one or more Convertible Notes remain outstanding. Meteora may submit Advance notices and receive shares of Common Stock pursuant to the SEPA concurrently with any outstanding Convertible Note balance, without restriction.`)]),
  ]),

  row("Commitment Fee",
    `${COMMIT_FEE_PCT} of the Commitment Amount (${COMMIT_FEE_AMT}), payable to Meteora at closing. The Commitment Fee may be paid in cash (netted from the Initial Advance proceeds) or, at the Company's election, in shares of Common Stock priced at the closing date market price.`),

  row("Purchase Price\n(Equity Advances)", [
    pp([BU("Company-Initiated Advances: "), T(`${CO_DISC} of the daily VWAP of the Common Stock on the date of the Advance notice.`)]),
    pp([BU("Investor-Initiated Advances: "), T(`${INV_DISC} of the lowest daily VWAP of the Common Stock over the 5 consecutive trading days immediately preceding the date of the Investor Advance notice.`)]),
  ]),

  row("Volume Thresholds\n& Limitations", [
    pp([BU("Daily Volume Limitation: "), T(`No single Advance shall result in the issuance of shares exceeding 30% of the average daily trading volume ("ADTV") of the Common Stock calculated over the 10 trading days preceding the Advance notice.`)]),
    pp([BU("Automatic Reduction: "), T(`If shares issuable under an Advance would exceed the Daily Volume Limitation on any single trading day within the pricing period, the Advance shall automatically be reduced to conform to such threshold. Any unfunded portion may be re-submitted as a subsequent Advance or, at Meteora's election, funded as a Convertible Note Advance.`)]),
  ]),

  row("Constraints on\nCompany Notices",
    `The Company may not submit an Advance notice if: (i) the resulting share issuance would exceed 30% of ADTV; (ii) the Company is in possession of material non-public information; (iii) no effective registration statement covers the resale of the applicable shares; or (iv) the Company is in breach of any representation, warranty, or covenant under the definitive agreements.`),

  row("Registration\nRights",
    `The Company shall file a registration statement (on Form S-1 or S-3, as applicable) covering the resale of all shares issuable under the SEPA and upon conversion of any Convertible Notes within 30 calendar days of execution of the definitive agreements, and shall use commercially reasonable efforts to cause such registration statement to become effective as promptly as practicable.`),

  row("Right of First\nRefusal (ROFR)",
    `Meteora shall have a right of first refusal to participate in up to 50% of any subsequent debt, equity, or equity-linked financing completed by the Company during the Commitment Period, on terms no less favorable than those offered to any third-party investor. This provision is binding on the parties.`),

  // ── III. CONVERTIBLE NOTES ─────────────────────────────────────────────────
  sectionHeader("III.  CONVERTIBLE PRE-PAID ADVANCE / CONVERTIBLE NOTES"),

  row("Initial Upfront\nAdvance", [
    pp([T(`Meteora shall fund ${FUNDED_AMT} at closing (the "Initial Advance"), in exchange for a Convertible Note with a principal amount of ${PRINCIPAL_AMT} (reflecting ${OID_PCT} original issue discount). The Initial Advance reduces the remaining Commitment Amount by ${FUNDED_AMT}.`)]),
  ]),

  row("Principal &\nPurchase Price", [
    pp([T(`Each Convertible Note shall be issued at a ${OID_PCT} original issue discount. The funded amount (i.e., the purchase price paid by Meteora) shall be ${OID_DIVISOR} of the face principal amount of the Note.`)]),
    pp([T(`Initial Advance: ${FUNDED_AMT} funded / ${PRINCIPAL_AMT} principal.`)]),
    pp([T(`Subsequent Debt Advances: funded amount \u00f7 (1 \u2212 ${OID_PCT}) = principal amount, calculated at the time of each Advance.`)]),
  ]),

  row("Maturity",
    `12 months from the date of issuance of each Convertible Note, unless earlier converted, redeemed, or accelerated (the "Maturity Date").`),

  row("Interest Rate",
    `0% per annum. No interest shall accrue or be payable on any Convertible Note issued under this facility.`),

  row("Conversion Price", [
    pp([T(`Each Convertible Note shall be convertible into shares of Common Stock at Meteora's election at the lower of:`)]),
    pp([BU("Fixed Conversion Price: "), T(`${FIXED_CONV} per share (the "Fixed Price"); and`)]),
    pp([BU("Variable Conversion Price: "), T(`${VAR_DISC} of the lowest daily VWAP of the Common Stock over the 5 consecutive trading days immediately preceding the applicable Conversion Notice date (the "Variable Price"). The Variable Conversion Price is consistent with the Investor-Initiated Advance purchase price under the SEPA.`)]),
    pp([T(`The "Conversion Price" shall be the lower of (i) the Fixed Price and (ii) the Variable Price, subject in each case to the Floor Price below.`)]),
  ]),

  row("Floor Price", [
    pp([T(`The Conversion Price shall not be less than ${FLOOR_PCT} of the Fixed Price (i.e., ${FLOOR_PRICE} per share) (the "Floor Price").`)]),
    pp([T(`If the Variable Price falls below the Floor Price on any Conversion Notice date, conversion shall occur at the Floor Price. Any downward adjustment to the Floor Price shall require mutual written agreement and, if required, shareholder approval in compliance with applicable Nasdaq Listing Rules.`)]),
  ]),

  row("Conversion\nMechanics", [
    pp([T(`Meteora may convert all or any portion of the outstanding principal of any Convertible Note at any time from and after the issuance date by delivery of a written Conversion Notice to the Company.`)]),
    pp([T(`Shares shall be delivered within 2 trading days of receipt of a Conversion Notice (the "Share Delivery Deadline"). Failure to deliver shares by such deadline shall give rise to standard cash penalties and buy-in rights as set forth in the definitive note agreement.`)]),
  ]),

  row("Optional\nRedemption",
    `The Company may prepay any Convertible Note, in whole or in part, upon 5 business days' prior written notice to Meteora, at a redemption price equal to 110% of the principal amount being redeemed. Meteora may convert any portion subject to a redemption notice prior to the effective date of such redemption.`),

  row("Beneficial\nOwnership Cap",
    `Meteora shall not convert any Convertible Note to the extent that, after giving effect to such conversion, Meteora and its affiliates would beneficially own more than 9.99% of the then-outstanding shares of Common Stock.`),

  row("Covenants", [
    pp([BU("No Short Sales: "), T(`Meteora shall not engage in short sales of the Common Stock during any period in which a Convertible Note remains outstanding, except as expressly permitted under a separate written agreement.`)]),
    pp([BU("Most Favored Nation: "), T(`If the Company enters into any subsequent convertible debt or equity-linked financing on terms more favorable to the counterparty than those set forth herein (including a lower floor price or greater discount), Meteora shall have the right to elect those more favorable terms.`)]),
    pp([BU("Use of Proceeds: "), T(`Proceeds shall be used for general working capital and corporate purposes. The Company shall not apply any proceeds to repurchase equity, pay dividends, or repay affiliate indebtedness without Meteora's prior written consent.`)]),
  ]),

  // ── IV. GENERAL TERMS ──────────────────────────────────────────────────────
  sectionHeader("IV.  GENERAL TERMS"),

  row("Variable Rate\nTransaction\nProhibition", [
    pp([T(`From the date of execution of definitive agreements until the later of (i) the date on which no Convertible Notes remain outstanding and (ii) the expiration of the Commitment Period (the "Restricted Period"), the Company shall not, without the prior written consent of Meteora, directly or indirectly issue, enter into, or agree to issue or enter into any Variable Rate Transaction.`)]),
    pp([T(`"Variable Rate Transaction" means any transaction in which the Company issues or sells (or agrees to issue or sell) any debt or equity security (a) at a conversion, exercise, or exchange price that is based upon and/or varies with the trading price of or quotations for the Common Stock at any time after the initial issuance of such security; (b) with a conversion, exercise, or exchange price subject to being reset at some future date or upon the occurrence of specified or contingent events; or (c) pursuant to any equity line of credit, "at-the-market" offering, or similar facility — in each case, other than pursuant to the SEPA and Convertible Notes issued thereunder.`)]),
    pp([T(`Carve-outs: (i) issuances pursuant to this SEPA or any Convertible Note hereunder; (ii) employee/director equity incentive plan issuances; (iii) securities issued in connection with a bona fide merger, acquisition, or Board-approved strategic partnership.`)]),
    pp([T(`Meteora shall be entitled to seek injunctive relief to enforce this provision, in addition to any right to collect damages, without the requirement to post a bond or other security.`)]),
  ]),

  row("Representations\n& Warranties",
    `Customary representations and warranties for a transaction of this nature, including: due organization and authority, valid issuance of securities, no material adverse change, SEC reporting compliance, and accuracy of public disclosures.`),

  row("Diligence &\nLegal Fees",
    `The Company shall reimburse Meteora for its reasonable and documented legal, diligence, and transaction costs, not to exceed ${DILIGENCE_FEES} in the aggregate, payable at closing.`),

  row("Governing Law",
    `State of New York. Disputes shall be resolved by binding arbitration in New York County, New York, pursuant to the rules of the American Arbitration Association. This provision is binding on the parties.`),

  row("Definitive\nDocumentation",
    `This Term Sheet is subject to the negotiation, execution, and delivery of mutually acceptable definitive agreements, including without limitation: a Standby Equity Purchase Agreement, a Form of Convertible Promissory Note, a Registration Rights Agreement, and such other transaction documents as are customary for a transaction of this nature.`),
];

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIDENTIALITY & EXCLUSIVITY (binding — do not change without legal review)
// ═══════════════════════════════════════════════════════════════════════════════

const confExcl =
  `This Term Sheet and its contents are strictly confidential. The Company shall not disclose the existence or terms ` +
  `of this Term Sheet to any third party (other than its legal counsel and financial advisors on a need-to-know, ` +
  `confidential basis) without Meteora's prior written consent. For a period of 30 days from the date hereof ` +
  `(or until execution of definitive agreements, if earlier), the Company agrees not to solicit, initiate, encourage, ` +
  `or engage in discussions with any third party regarding a financing transaction that would be competitive with the ` +
  `transaction described herein. The parties agree that this Confidentiality and Exclusivity paragraph shall be legally ` +
  `binding on both parties notwithstanding the non-binding nature of the remainder of this Term Sheet.`;

// ═══════════════════════════════════════════════════════════════════════════════
// SIGNATURE BLOCK HELPER
// ═══════════════════════════════════════════════════════════════════════════════

function sigBlock(entity, name, title) {
  return [
    pp([B(entity)], { spacing: { before: 0, after: 120 } }),
    pp([T("By: ___________________________________")]),
    pp([T(`Name: ${name}`)]),
    pp([T(`Title:  ${title}`)]),
    pp([T("Date:   _________________________________")]),
  ];
}

// ═══════════════════════════════════════════════════════════════════════════════
// DOCUMENT ASSEMBLY
// ═══════════════════════════════════════════════════════════════════════════════

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 360, hanging: 360 } } }
      }]
    }]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },            // US Letter
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },  // 0.75" margins
      }
    },
    children: [

      // ── Page 1: Terms ──────────────────────────────────────────────────────
      logoHeaderTable([
        "METEORA CAPITAL, LLC",
        `Term Sheet \u2014 ${COMPANY_NAME} (${TICKER})`,
        DATE,
      ]),
      sp(),

      new Paragraph({
        children: [new TextRun({ text: preambleText, italics: true, font: FONT, size: 18 })],
        spacing: { before: 0, after: 160 },
      }),

      new Paragraph({
        children: [new TextRun({ text: "TERMS OF THE OFFERING", bold: true, font: FONT, size: 20 })],
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 120 },
      }),

      new Table({
        width: { size: TW, type: WidthType.DXA },
        columnWidths: [LW, CW],
        rows: termRows,
      }),

      sp(),
      new Paragraph({
        children: [
          new TextRun({ text: "Confidentiality and Exclusivity.  ", bold: true, font: FONT, size: 20 }),
          new TextRun({ text: confExcl, italics: true, font: FONT, size: 18 }),
        ],
        spacing: { before: 60, after: 60 },
      }),

      // ── Page 2: Signatures ─────────────────────────────────────────────────
      new Paragraph({ children: [new PageBreak()], spacing: { before: 0, after: 0 } }),

      logoHeaderTable([
        "METEORA CAPITAL, LLC",
        `Signature Page to Term Sheet \u2014 ${COMPANY_NAME} (${TICKER})`,
        DATE,
      ]),
      sp(),

      new Paragraph({
        children: [new TextRun({
          text: `IN WITNESS WHEREOF, the parties have indicated their agreement to the terms of this Term Sheet by signing ` +
                `below. This Term Sheet is non-binding in all respects except with respect to the Confidentiality and ` +
                `Exclusivity, ROFR, and Governing Law provisions set forth above.`,
          italics: true, font: FONT, size: 18,
        })],
        spacing: { before: 0, after: 200 },
      }),

      new Table({
        width: { size: TW, type: WidthType.DXA },
        columnWidths: [4600, 4760],
        rows: [new TableRow({
          children: [
            new TableCell({
              borders: noBorders, width: { size: 4600, type: WidthType.DXA },
              margins: { top: 0, bottom: 0, left: 0, right: 200 },
              children: sigBlock("METEORA CAPITAL, LLC", "Vik Mittal", "Managing Member"),
            }),
            new TableCell({
              borders: noBorders, width: { size: 4760, type: WidthType.DXA },
              margins: { top: 0, bottom: 0, left: 200, right: 0 },
              children: sigBlock(COMPANY_NAME.toUpperCase(), "", ""),
            }),
          ]
        })]
      }),

      sp(), sp(),
      new Paragraph({
        children: [new TextRun({
          text: `This Term Sheet does not constitute an offer to sell or a solicitation of an offer to buy any security. ` +
                `Any offering will be made only pursuant to definitive documentation and in compliance with applicable securities laws.`,
          italics: true, font: FONT, size: 16,
        })],
        alignment: AlignmentType.CENTER,
        spacing: { before: 80, after: 0 },
      }),

    ]
  }]
});

// ═══════════════════════════════════════════════════════════════════════════════
// OUTPUT
// ═══════════════════════════════════════════════════════════════════════════════

const outDir = path.join(__dirname, 'output');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);
const outPath = path.join(outDir, `${TICKER}_Term_Sheet_Meteora.docx`);

Packer.toBuffer(doc)
  .then(buf => {
    fs.writeFileSync(outPath, buf);
    console.log(`\n✓ Term sheet generated: ${outPath}`);
    console.log(`  ${COMPANY_NAME} (${TICKER}) | ${DATE}`);
    console.log(`  SEPA: ${SEPA_MAX} | Initial Advance: ${FUNDED_AMT} funded / ${PRINCIPAL_AMT} principal | OID: ${OID_PCT}`);
  })
  .catch(err => { console.error('Error generating term sheet:', err); process.exit(1); });
