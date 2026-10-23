---
name: fpa-document-editing
description: "Draft, adapt, and redline Forward Purchase Agreement / FSPA (Funded Standby Purchase Agreement) documents for Meteora Capital's SPAC transactions. Trigger when the user asks to 'draft an FPA', 'redline the FSPA', 'update the FPA for [ticker]', 'adapt [base FPA] for [new deal]', or 'create a forward purchase confirmation for [ticker]'. Also trigger when the user uploads one or two .docx files alongside a SPAC ticker and asks to compare, adapt, or update them. Produces a tracked-change .docx redline sourced from public SEC filings (IPO prospectus, 8-K/BCA, F-4/S-4, Articles of Association)."
---

# FPA / FSPA Document Editing — SPAC Forward Purchase Agreement Adaptation

## Overview

This skill adapts an existing Meteora FPA/FSPA template (the **base document**) into a redlined draft for a new SPAC transaction. The output is a `.docx` file with all changes shown in **tracked-change redline format** (green insertions, red strikethrough deletions), suitable for direct negotiation use.

**Primary workflow:** Receive base `.docx` (prior executed or draft FPA) → gather all deal-specific data from public SEC filings → apply tracked-change edits programmatically using lxml → pack and deliver redlined `.docx`.

**This skill requires the docx skill.** Read `/mnt/skills/public/docx/SKILL.md` before starting any file work.

---

## Step 0: Understand What Changed — Diff the Base Against the Prior Version

Before touching the new deal, if the user provides TWO documents (e.g., "I used FLFV as the base, updated to HSPT"), **diff them first** to understand all prior edits:

```bash
cd /home/claude
pandoc --track-changes=all "base.docx" -o base.md
pandoc --track-changes=all "updated.docx" -o updated.md
diff base.md updated.md > full_diff.txt
```

Read the full diff systematically. Categorize every change into:
- **Party/header changes** (names, dates, addresses, contacts)
- **Merger structure changes** (step merger, entities, jurisdiction)
- **Economic term changes** (floor price, max shares, fees, settlement adj)
- **Structural changes** (removed PIPE, removed additional shares, new provisions)
- **Legal/boilerplate additions** (new no-reliance clauses, characterization paragraphs)

This diff becomes your master checklist for the new deal.

---

## Step 1: Gather VACH/SPAC Data from SEC EDGAR

**Always source from primary filings. Never guess party details, addresses, article numbers, or signatory names.**

### 1a. EDGAR Filing Sequence to Pull

Use `edgar-filings` with the SPAC's CIK to find:

| Filing | What to Get |
|--------|-------------|
| **IPO 8-K** (filed day of IPO close) | Articles of Association exhibit (EX-3.2 or EX-3.1) — this is the **executed** version |
| **IPO 424B4** | SPAC address, phone, unit structure, AoA overview |
| **BCA 8-K** (deal announcement) | BCA exhibit (EX-2.1) — merger structure, notice addresses, signatories, BCA date |
| **F-4/A or 424B3** (definitive proxy) | Target details, deal terms, PubCo name, warrant details |
| **10-K** | SPAC address confirmation, redemption limitation description |

### 1b. Critical Data Points to Extract

**From the BCA EX-2.1 (most important):**
- Merger structure description in the body (Initial Merger + Acquisition Merger parties, sequence)
- Merger Sub name, jurisdiction
- PubCo name, jurisdiction
- Notice addresses for SPAC and Company (Section 12.4 or similar)
- Signatory names and titles on the signature page
- BCA date (from the 8-K header)

**From the AoA EX-3.2:**
- Full text of the Business Combination article (typically Article 53 for Cayman SPACs)
- The **bulldog clause** sub-article number — the one that restricts redemption to 15% per group. This is NOT always the same article number across SPACs. Read it, don't assume.
- AoA effective date (shown at the top of the exhibit)

**From the 424B4:**
- SPAC registered address and phone number
- Contact name at SPAC

**Confirmed data points for VACH (Voyager Acquisition Corp., CIK 2006815):**
```
SPAC:           Voyager Acquisition Corp., Cayman Islands exempted company ("VACH")
Ticker:         VACH (shares), VACHU (units), VACHW (warrants) — Nasdaq
Address:        131 Concord Street, Brooklyn, NY 11201
Phone:          (347) 720-2907
Contact:        Adeel Rouf, President and CEO
Email:          adeel@voyageracq.com
VACH Counsel:   Winston & Strawn LLP, 800 Capitol Street Suite 2400,
                Houston TX 77002; Michael J. Blankenship; mblankenship@winston.com
AoA:            Amended and Restated Memorandum and Articles of Association,
                effective May 31, 2024 (Cayman File #: 405665)
Bulldog clause: Article 53.5 (15% redemption cap per group)
BCA date:       April 22, 2025
Merger Sub:     Veraxa Cayman Merger Sub (Cayman Islands exempted company)
PubCo:          Veraxa Biotech Holding AG (Swiss public limited company)
Target:         Veraxa Biotech AG, Talacker 35, 8001 Zurich, Switzerland
                Attn: Oliver Baumann; oliver.baumann@xlifesciences.ch
Target CEO:     Christoph Antz (BCA signatory — ALWAYS confirm from BCA sig page,
                not from proxy/F-4 board descriptions)
Target Counsel: Duane Morris LLP, 901 New York Avenue N.W. Suite 700 East,
                Washington DC 20001; Andrew Tucker; ATucker@duanemorris.com
Proxy (424B3):  Filed February 19, 2026
```

---

## Step 2: The Bulldog Clause — Always Verify, Never Assume

The FSPA contains two references to the bulldog clause:
1. In the **Excess Shares** definition: `"as defined in Article [X.X] of the Amended and Restated Memorandum and Articles of Association, dated [DATE]"`
2. In the **Counterparty representations**: `"The Counterparty shall waive any violation of its 'bulldog clause,' as set forth in Article [X.X] of the Articles of Association"`

**The article number varies by SPAC.** HSPT used Article 48.5. VACH uses Article 53.5. Pull the AoA and find the sub-article that contains the 15% redemption cap language — do not copy the prior number.

The correct provision reads something like: *"no such Member acting together with any Affiliate...may exercise this redemption right with respect to more than 15 per cent of the Public Shares in the aggregate without the prior consent of the Company."*

---

## Step 3: Understand the FSPA Document Structure

A Meteora FSPA is structured as a **table-based confirmation** with defined terms in a two-column table (term | definition) followed by prose provisions. Key sections in order:

1. **Header block** — Date, To (Counterparty + Target), Address, From (Meteora entities), Re, Purpose
2. **Terms table** — All economic and structural definitions:
   - Effective Date, Settlement Date, Valuation Date
   - Floor Price / VWAP Trigger Event
   - VWAP Price (Bloomberg screen reference)
   - Shares definition (Counterparty identity)
   - Number of Shares, Maximum Number of Shares, Purchased Amount
   - Recycled Shares, Prepayment Amount, Prepayment Shortfall
   - Prepayment Shortfall Consideration, Shortfall Sales
   - OET (Optional Early Termination)
   - Settlement Amount, Settlement Amount Adjustment
   - Reset Price
   - Excess Shares (bulldog clause reference)
   - Reimbursement of Legal Fees
   - Share Registration
3. **Other Provisions** — Representations, covenants, indemnification, governing law
4. **Notices** — Meteora, Counterparty (+ counsel), Target (+ counsel)
5. **Signature blocks** — Meteora entities, Counterparty, Target
6. **Schedule A** — Pricing Date Notice form

---

## Step 4: Apply Redlines — Technical Implementation

### 4a. Setup

```bash
# Unpack the base docx
python /mnt/skills/public/docx/scripts/office/unpack.py base.docx unpacked/

# Install lxml (required — do NOT use string replacement on XML files)
pip install lxml --break-system-packages -q
```

### 4b. CRITICAL: Use lxml Tree Manipulation, Not String Replacement

**This is the most important technical lesson from this exercise.** String replacement on `document.xml` produces structurally invalid OOXML because `<w:del>` and `<w:ins>` elements must be **siblings of `<w:r>` at the paragraph level**, never children of `<w:r>`. Every OOXML schema validator will reject `del`/`ins` nested inside `w:r`.

**Always use lxml to:**
1. Find the `w:r` run containing the text to change
2. Remove that run from its parent
3. Insert `[before-run]`, `[w:del]`, `[w:ins]`, `[after-run]` as siblings at the same parent level

**Core replace function:**

```python
from lxml import etree
import copy

W  = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
TS = '2026-03-23T00:00:00Z'  # use actual date
AUT = 'Claude'

def w(t): return f'{{{W}}}{t}'

_nid = [1000]
def nid(): _nid[0]+=1; return str(_nid[0])

def replace_in_run(run, old_text, new_text):
    """
    Replace first occurrence of old_text in run's w:t with del+ins siblings.
    new_text='' for pure deletion (no ins element created).
    Returns True if replacement was made.
    """
    t_el = run.find(w('t'))
    if t_el is None or t_el.text is None: return False
    if old_text not in t_el.text: return False
    
    text   = t_el.text
    idx    = text.find(old_text)
    parent = run.getparent()
    pos    = list(parent).index(run)
    rpr    = run.find(w('rPr'))
    before, after = text[:idx], text[idx+len(old_text):]
    
    parent.remove(run)
    ip = pos
    def push(el): nonlocal ip; parent.insert(ip, el); ip += 1
    
    if before:
        rb = copy.deepcopy(run); rb.find(w('t')).text = before
        rb.find(w('t')).set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        push(rb)
    
    # Deletion
    de = etree.Element(w('del'))
    de.set(w('id'),nid()); de.set(w('author'),AUT); de.set(w('date'),TS)
    dr = etree.SubElement(de,w('r'))
    if rpr is not None: dr.append(copy.deepcopy(rpr))
    dt = etree.SubElement(dr,w('delText')); dt.text = old_text
    dt.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    push(de)
    
    # Insertion (skip if pure deletion)
    if new_text:
        ie = etree.Element(w('ins'))
        ie.set(w('id'),nid()); ie.set(w('author'),AUT); ie.set(w('date'),TS)
        ir = etree.SubElement(ie,w('r'))
        if rpr is not None: ir.append(copy.deepcopy(rpr))
        it = etree.SubElement(ir,w('t')); it.text = new_text
        it.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        push(ie)
    
    if after:
        ra = copy.deepcopy(run); ra.find(w('t')).text = after
        ra.find(w('t')).set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        push(ra)
    
    return True

def replace_all(root, old_text, new_text, limit=None):
    """Apply replace_in_run across all runs. Use root.iter(w('r')) NOT xpath."""
    count = 0
    for run in root.iter(w('r')):         # NOTE: iter(), not xpath — see below
        if limit and count >= limit: break
        if replace_in_run(run, old_text, new_text): count += 1
    return count
```

### 4c. CRITICAL: Use `root.iter(w('r'))`, Not `root.xpath('.//w:r', ...)`

`root.xpath('.//w:r', namespaces={'w': W})` sometimes **misses runs** in table cells due to namespace binding differences between elements created by lxml vs. those parsed from the file. `root.iter(w('r'))` is reliable and finds every `w:r` element regardless of where it is in the tree.

### 4d. Runs with Multiple w:t Elements (`lastRenderedPageBreak`)

Some runs contain **two `w:t` elements** split by a `<w:lastRenderedPageBreak/>` element. `run.find(w('t'))` only returns the first `w:t`. If a text replacement fails despite the text appearing in the paragraph, check whether the target text is in the **second** `w:t` element:

```python
# Don't just use run.find(w('t')) — check all w:t elements in the run
t_elements = run.findall(w('t'))
for t_el in t_elements:
    if t_el.text and 'target text' in t_el.text:
        # modify t_el directly, then insert del/ins AFTER the run
        t_el.text = text[:idx]  # truncate to before-text
        # insert del, ins, after-run at parent.insert(pos+1, ...)
```

### 4e. Deleting an Entire Table Row (Tracked Delete)

To mark an entire `<w:tr>` (table row) as deleted without physically removing it:

```python
for tbl in root.iter(w('tbl')):
    for tr in tbl.iter(w('tr')):
        row_text = ''.join(t.text or '' for t in tr.iter(w('t')))
        if 'TARGET ROW LABEL:' in row_text:
            for run in list(tr.iter(w('r'))):
                t_el = run.find(w('t'))
                if t_el is None or not t_el.text: continue
                parent = run.getparent(); pos = list(parent).index(run)
                rpr    = run.find(w('rPr'))
                parent.remove(run)
                de = etree.Element(w('del'))
                de.set(w('id'),nid()); de.set(w('author'),AUT); de.set(w('date'),TS)
                dr = etree.SubElement(de,w('r'))
                if rpr is not None: dr.append(copy.deepcopy(rpr))
                dt = etree.SubElement(dr,w('delText')); dt.text = t_el.text
                dt.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
                parent.insert(pos, de)
            break
```

### 4f. Inserting New Paragraphs (Tracked Insertion)

To add new content (e.g., a counsel block in the notices section) as tracked insertions, create new `w:p` elements wrapping the text in `w:ins`:

```python
def make_ins_para(line_text, sz='20'):
    p_el  = etree.Element(w('p'))
    ppr   = etree.SubElement(p_el, w('pPr'))
    jc    = etree.SubElement(ppr, w('jc')); jc.set(w('val'),'both')
    ins_el = etree.Element(w('ins'))
    ins_el.set(w('id'),nid()); ins_el.set(w('author'),AUT); ins_el.set(w('date'),TS)
    r     = etree.SubElement(ins_el, w('r'))
    rpr   = etree.SubElement(r, w('rPr'))
    etree.SubElement(rpr,w('sz')).set(w('val'),sz)
    etree.SubElement(rpr,w('szCs')).set(w('val'),sz)
    t     = etree.SubElement(r, w('t')); t.text = line_text
    t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    p_el.append(ins_el)
    return p_el

# Insert after target paragraph
target_para = ...  # find the w:p you want to insert after
parent_body = target_para.getparent()
insert_idx  = list(parent_body).index(target_para) + 1
for i, line in enumerate(new_lines):
    parent_body.insert(insert_idx + i, make_ins_para(line))
```

### 4g. Restoring Placeholders (Undo a Tracked Change)

When you want to revert a prior tracked change back to a placeholder (e.g., restore `[Law Firm]` where Winston was previously inserted):

```python
def restore_to_placeholder(root, ins_text, restore_text):
    """Find a w:ins element whose text = ins_text, remove it and its paired w:del,
    insert a plain w:r with restore_text."""
    for ins_el in root.xpath('.//w:ins', namespaces={'w': W}):
        full = ''.join(t.text or '' for t in ins_el.xpath('.//w:t', namespaces={'w': W}))
        if full != ins_text: continue
        parent   = ins_el.getparent()
        children = list(parent)
        pos      = children.index(ins_el)
        # Find paired del (immediately before or after)
        del_el = None; del_pos = None
        for offset in [-1, 1]:
            idx = pos + offset
            if 0 <= idx < len(children) and children[idx].tag == w('del'):
                del_el = children[idx]; del_pos = idx; break
        inner = ins_el.xpath('.//w:r', namespaces={'w': W})
        rpr = inner[0].find(w('rPr')) if inner else None
        # Build plain run
        plain = etree.Element(w('r'))
        if rpr is not None: plain.append(copy.deepcopy(rpr))
        t = etree.SubElement(plain, w('t')); t.text = restore_text
        remove_pos = pos
        parent.remove(ins_el)
        if del_el is not None:
            parent.remove(del_el)
            remove_pos = min(pos, del_pos)
        parent.insert(remove_pos, plain)
        return True
    return False
```

**NOTE:** Bullet placeholder characters appear as literal `\u2022` (U+2022) in lxml text — NOT as `&#x2022;` entities. Always use the actual Unicode character when searching for `[•]` placeholders.

### 4h. Validate Structure After Every Batch

After each batch of replacements, run this check before saving:

```python
violations = 0
for run in root.iter(w('r')):
    for child in run:
        ctag = child.tag.split('}')[1] if '}' in child.tag else ''
        if ctag in ('del','ins'): violations += 1
if violations:
    print(f"WARNING: {violations} del/ins nested inside w:r — fix before packing")
```

### 4i. Pack the Docx — Bypass pack.py for Binary Files

`pack.py` tries to condense all `.xml` files and will fail on binary custom XML files (e.g., `customXml/item2.xml`). Use `zipfile` directly instead:

```python
import zipfile, os

SOURCE_DIR = 'unpacked/'
OUTPUT     = 'output.docx'
ORIGINAL   = 'base.docx'  # fallback for files not in unpacked dir

# Read original for any files not modified
original_files = {}
with zipfile.ZipFile(ORIGINAL, 'r') as z:
    for name in z.namelist():
        original_files[name] = z.read(name)

with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    written = set()
    # Write all files from unpacked directory
    for root_dir, dirs, files in os.walk(SOURCE_DIR):
        for fname in files:
            fpath   = os.path.join(root_dir, fname)
            arcname = os.path.relpath(fpath, SOURCE_DIR).replace(os.sep, '/')
            zout.writestr(arcname, open(fpath,'rb').read())
            written.add(arcname)
    # Write any original files not in unpacked dir (fonts, media, etc.)
    for arcname, data in original_files.items():
        if arcname not in written:
            zout.writestr(arcname, data)
```

### 4j. Verification Pattern — Use Recursive del-Skip

The naive `'term' in full_text` check will incorrectly report terms as "live" when they're only inside `<w:del>` blocks. Always use a recursive function that skips entire `del` subtrees:

```python
def collect_live(elem):
    """Recursively collect text, skipping w:del subtrees entirely."""
    texts = []
    tag = elem.tag.split('}')[1] if '}' in elem.tag else ''
    if tag == 'del': return texts          # skip entire del subtree
    if tag == 't' and elem.text: texts.append(elem.text)
    for child in elem: texts.extend(collect_live(child))
    return texts

live_text = '\n'.join(collect_live(root))
# Now check:
assert 'HSPT' not in live_text            # old ticker absent
assert 'VACH' in live_text                # new ticker present
```

---

## Step 5: Standard Replacement Checklist for SPAC FPA Adaptation

Work through these in order. Each should be a `replace_all(root, old, new)` call.

### Header Block
- [ ] Date: prior date → `[•], 2026`
- [ ] Counterparty name (full legal name + jurisdiction)
- [ ] Target name (full legal name + jurisdiction)
- [ ] Counterparty ticker
- [ ] Counterparty address (and in Pricing Date Notice)
- [ ] Counterparty phone (Pricing Date Notice)

### Merger Structure (body text)
- [ ] "SPAC will merge with and into [old Merger Sub]" → new Merger Sub name
- [ ] Old Merger Sub name and definition token
- [ ] Old HoldCo/SL Science entity name and definition token
- [ ] "Following the [First / Initial] Merger, [old entity] will merge with and into [old Target]" → new structure
- [ ] "with [old Target] being the surviving entity" → new surviving entity language
- [ ] "[SPAC] will change its corporate name to" → update
- [ ] PubCo name (in bracket placeholder or standalone)
- [ ] BCA date
- [ ] BCA parties list (remove old entities, insert new ones)

### Terms Table
- [ ] Bloomberg screen: `OLD <Equity> AQR SEC"` → `NEW <Equity> AQR SEC"`
- [ ] Shares definition: old company name and ticker
- [ ] Bulldog clause article number and AoA date (both occurrences)
- [ ] Maximum Number of Shares (if changed)
- [ ] Floor price / VWAP Trigger Event dollar amount (if changed), or delete row entirely
- [ ] Settlement Amount Adjustment multiplier (if changed)
- [ ] Legal fees cap (if changed)
- [ ] Reset Price: remove weekly reset if applicable; keep dilutive offering clause
- [ ] Valuation Date condition (ii): update SEPA/ELOC/note reference to current deal

### Notices
- [ ] Counterparty firm name (in "Notice to Counterparty" header)
- [ ] Counterparty address lines (all instances)
- [ ] Counterparty attention/email
- [ ] Meteora counsel block: insert or leave as `[Law Firm]` / `[•]` placeholders per instruction
- [ ] Target address (all lines)
- [ ] Target attention/email
- [ ] Target counsel firm, address, attention, email
- [ ] Delete Robinson & Cole or other prior SPAC's carry-over counsel if present
- [ ] Pricing Date Notice: counterparty name, address, phone

### Signature Blocks
- [ ] SPAC/Counterparty entity name (bold heading)
- [ ] Signatory name and title — **ALWAYS confirm from BCA signature page**
- [ ] Target entity name (bold heading)
- [ ] Target signatory name and title — **ALWAYS confirm from BCA signature page** (may differ from proxy/F-4 management bios)
- [ ] Year in "Date: [•], 202X"

### 424B3 / Lock-Up Reference
- [ ] Proxy date placeholder → actual filing date of the 424B3

---

## Step 6: Common Mistakes and How to Avoid Them

### Mistake 1: String replacement on XML → structural violations
**What happened:** First implementation used Python `str.replace()` on the raw XML file. This embeds `<w:del>` elements inside `<w:r>` tags, which is an OOXML schema violation. Took 3+ attempts and a complete restart to fix.
**Fix:** Always use lxml from the start. The `replace_in_run()` function above is the only safe approach.

### Mistake 2: Using xpath instead of iter for run traversal
**What happened:** `root.xpath('.//w:r', namespaces={'w': W})` missed certain runs in table cells. The `replace_all()` function returned 0 matches even when the text was clearly present.
**Fix:** Always use `root.iter(w('r'))`. It finds every `w:r` regardless of namespace binding.

### Mistake 3: Runs with two w:t elements (lastRenderedPageBreak)
**What happened:** The legal fees `$50,000` text was in a run containing two `w:t` elements split by a `<w:lastRenderedPageBreak/>`. `run.find(w('t'))` only finds the first `w:t`, missing the target text in the second.
**Fix:** Before declaring a text "not found," check all `w:t` elements in the run: `for t_el in run.findall(w('t'))`. If the target text is in the second `w:t`, modify that element and insert the del/ins block after the run.

### Mistake 4: Assuming bulldog clause article number
**What happened:** Used Article 48.5 (HSPT's number) in the first version. VACH uses Article 53.5 with a completely different numbering scheme.
**Fix:** Pull the AoA from EDGAR (EX-3.2 from the S-1 or IPO 8-K), find the provision that contains the 15% language, and read its article number. Never copy from a prior deal.

### Mistake 5: Wrong target signatory
**What happened:** Used Oliver Baumann (Chairman of the Board) as the Veraxa signatory because he appears throughout the proxy as the Company Shareholder Representative. The actual CEO/signatory on the BCA is Christoph Antz.
**Fix:** Pull the BCA EX-2.1 and go to the signature page. Read the actual name and title. The signatory is whoever signed the BCA, not necessarily whoever is mentioned most in the proxy.

### Mistake 6: Bullet placeholder encoding
**What happened:** `restore_to_placeholder()` couldn't find `Attention: [•]` / `Email: [•]` when searching with `'[&#x2022;]'`. The XML file stores this as literal `\u2022` after pandoc/lxml processing.
**Fix:** Always use the actual Unicode character in Python strings: `'Attention: [\u2022]'` not the XML entity.

### Mistake 7: pack.py failing on binary customXml files
**What happened:** `pack.py` tries to `utf-8` decode every `.xml` file including `customXml/item2.xml`, which is a binary data store. This throws `UnicodeDecodeError`.
**Fix:** All XML validations passed — the error was only in pack.py's condense step. Use `zipfile` directly to assemble the docx, falling back to the original for any files not in the unpacked directory.

### Mistake 8: Text spread across multiple runs for multi-token phrases
**What happened:** Long phrases like `"HSPT, SL Science, Merger Sub I, Merger Sub II and Target"` are split across multiple `w:r` elements. A single `replace_all()` can't find the full phrase because no single run contains the whole string.
**Fix:** For multi-run phrases, break them into per-run replacements. After replacing the first token (e.g., `HSPT` → `VACH`), replace the remainder (e.g., `", SL Science, Merger Sub I, Merger Sub II"` → `" and Veraxa Biotech AG"`) as a separate step. Or use a "collect paragraph text then replace in-paragraph" approach.

### Mistake 9: Verification using simple string search misses del-block context
**What happened:** `'$10.00.' in live_text` returned `True` even after the period was correctly deleted, because `$10.00.` appeared in the **Dilutive Offering Reset** definition (unrelated sentence). Also, the naive `join(all_text)` approach includes `delText` elements.
**Fix:** Use the `collect_live()` recursive function that skips entire `del` subtrees. Check for specific phrases in context (e.g., `'$10.00; provided'`) rather than bare substrings.

---

## Step 7: Deal-Specific Economic Terms Worksheet

Confirm these with Walter before drafting. Leave as `[•]` in the document if not yet determined.

| Term | HSPT Value | VACH Value | Notes |
|------|-----------|-----------|-------|
| Maximum Number of Shares | 3,000,000 | 4,000,000 | |
| Floor Price / VWAP Trigger | $2.00 | Removed entirely | Delete full table row |
| Settlement Amount Adjustment | $0.75 | $0.50 | Multiplier per share |
| Legal Fees Cap | $50,000 | $30,000 | Attorney fees reimbursement |
| Valuation Date (ii) reference | SEPA/convertible note | ELOC with Lincoln Park Capital, LLC | Remove brackets |
| Reset Price — weekly reset | Present | Removed | Keep dilutive offering clause |
| Prepayment Shortfall fee | 2.50% | TBD | |
| OET minimum | 50,000 shares | 50,000 shares | |
| Meteora entities | MCP + MSTO + MSC | TBD | Leave bracketed until confirmed |

---

## Step 8: Output Quality Checklist

Before delivering the file, verify:

- [ ] Zero structure violations (`del`/`ins` inside `w:r`) — run the violations check
- [ ] All old party names absent from live text
- [ ] All new party names present in live text
- [ ] Article 53.5 (not 48.5) cited in both bulldog clause locations
- [ ] BCA date April 22, 2025
- [ ] AoA date May 31, 2024
- [ ] Signatory for Counterparty: Adeel Rouf, President and Chief Executive Officer
- [ ] Signatory for Target: Christoph Antz, Chief Executive Officer
- [ ] Tracked deletion count and insertion count are roughly equal (pure deletions increase del count)
- [ ] ZIP integrity passes (`testzip()` returns None)
- [ ] Paragraph count unchanged (pack.py or lxml verification)

---

## Appendix: VACH Article 53 Redemption Mechanics Summary

Article 53 governs Business Combination mechanics and contains all redemption provisions. Relevant sub-articles for FSPA purposes:

| Article | Content | FSPA Relevance |
|---------|---------|---------------|
| 53.1 | Supremacy clause — Article 53 overrides all others | Background |
| 53.2 | Pre-closing: submit to shareholders or conduct tender offer | Background |
| 53.4 | Net tangible assets ≥ $5,000,001 condition | Background |
| **53.5** | **15% bulldog clause — redemption cap per group** | **CITE IN FSPA** |
| 53.6 | No withdrawal of redemption notice | Background |
| 53.7 | Liquidation: 24-month deadline from IPO (Aug 12, 2026) | Background |
| 53.8 | Amendment → redemption right triggered | Background |
| 53.9 | Trust Account access only via redemption/tender/liquidation | Background |
| 53.10 | No new share issuances pre-close entitling Trust access | Background |
| 53.11 | 80% FMV test; no blank-check target | Background |

Only Article 53.5 is cited in the FSPA. The "waiver of bulldog clause" language covers Meteora's position in the context of the redemption limitation.
