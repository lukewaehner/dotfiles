# Recalibrate `email-voice` to a new person

Run this once per person who installs the skill. It rewrites the voice fingerprint, the register table, the `Calibrated for:` line in `SKILL.md`, and the examples in `references/examples.md` so the skill writes like **them** — then repackages the skill as a `.skill` file for re-upload.

Trigger phrases: "recalibrate the email-voice skill to me", "learn my email voice", "retarget this to me", "set up email-voice for me".

The single most important rule: **learn from the thread, not just the sent text.** A sent message on its own tells you *what* they wrote; the incoming message they were replying to tells you *why* they wrote it that way — how formal the other party was, what was being asked, what register the moment called for. Always pair each reply with the message it answered.

## Prerequisites

- The **Email Assistant (Microsoft 365)** tools must be available and signed in **as the person being calibrated**. Call `whoami` first. If the signed-in account isn't theirs, stop and ask them to sign in with their own account before continuing — otherwise you will learn the wrong person's voice.
- Capture their name, title, and standard signature for the sign-off lines.

## Step-by-step

### 1. Confirm identity
`whoami` → confirm the account is the person to calibrate. Note their display name and signature block.

### 2. Pull the Sent box (last ~3 months)
`search_emails(folder="SentItems", after="YYYY-MM-DD", max_results=100)` with `after` set ~90 days back. If the box is busy, page back further by lowering `after` and pulling again. Aim to *see* 60–100 sent items before filtering.

### 3. Filter to genuinely human-authored replies
Keep only messages where the person actually wrote prose. **Drop:**
- Automated / templated sends from a shared mailbox: daily briefs, P&L blasts, `[TEST]` sends, BamSEC or other filing alerts.
- Calendar system mail: `Accepted:` / `Declined:` / `Tentative:`.
- E-signature and other service notifications (Adobe Sign, DocuSign, etc.).
- Pure forwards with no added words, and notes-to-self.

What's left — real replies and outbound asks — is the corpus.

### 4. Read threads for context (the key step)
Choose ~10–15 messages that span the registers, and for each call `read_thread(message_id)` to capture **the incoming message + their reply together**. Make sure the sample covers:
- internal quick replies (to a manager / peer),
- at least one longer idea or proposal email,
- an external counterparty email (banker / vendor / client) if any exist,
- a scheduling / HR / logistics note,
- a nudge / follow-up bump.

If a register is genuinely absent from their mail, note it and model that register on the closest formal/informal neighbor rather than inventing samples.

### 5. Extract the fingerprint
From the corpus, pull out — with one or two **verbatim** anchors each:
- **Greetings** (e.g. `Hi [Name],`, `Hey [Name]`, `[Name] –`, none) and when each is used.
- **Openers** — the first move (acknowledge? dive in? thank?).
- **Opinion handling** — do they hedge (`I think`, `I believe`, `maybe`) or assert flatly? With or without a follow-on proposal?
- **Recurring tics** — reassurance phrases, favorite connectors, stock closers.
- **Sign-offs** — by register; note when they use none.
- **Signature block** — capture their exact Outlook signature from the foot of their sent mail, verbatim. The Graph connector does not auto-apply it, so the skill has to carry it.
- **Punctuation & rhythm** — dash style, exclamation-point frequency, sentence-length mix, lists vs prose, any structured-email scaffolding.
- **Diction** — formality band, jargon, any second-language business-English register, words they reach for.
- **Length calibration** — how long a yes/no, an ack, a proposal each run.

### 6. Rewrite the skill in place
- `SKILL.md`: update the `Calibrated for:` line (name, role, date); replace **The voice fingerprint** section and the **Register shifts** table with the new person's habits and anchors; adjust **Anti-patterns** to their actual failure-modes (the generic-email tells they specifically avoid); and swap the **Signature block** for theirs.
- `references/examples.md`: replace every example with new anonymized incoming→reply pairs drawn from their threads, grouped by register, each with a one-line "why in-voice" note.
Keep the file structure, headings, and the `description` triggers identical — only the *content* of the voice changes.

### 7. Anonymize (default on)
Unless the owner says the skill will stay strictly internal and asks for verbatim, scrub before saving:
- External counterparty / client / vendor names → `[Counterparty]`, `[Vendor]`, `[Client]`.
- Tickers, deal names, $ figures, share counts → `[TICKER]`, `[Deal]`, `~N`.
- Personal data (passport, immigration, addresses, phone, comp) → generalize ("a document", "an appointment").
- Greeting names → neutral placeholders (`David`, `Sam`, `Jordan`, `Team`).
**Preserve the person's wording and structure exactly** — the phrasing is the calibration value; only the facts get masked.

### 8. Repackage and deliver
Zip the updated folder as a `.skill` file (the directory name stays `email-voice`) and present it for re-upload:
```bash
cd <parent-of-email-voice>
python - <<'PY'
import zipfile, os
root, name = ".", "email-voice"
out = f"{name}.skill"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, _, fs in os.walk(name):
        for f in fs:
            if f.endswith((".pyc",)) or "__pycache__" in dp:
                continue
            p = os.path.join(dp, f)
            z.write(p, p)
print("Wrote", out, os.path.getsize(out), "bytes")
PY
```
Then tell them: the installed copy is read-only, so they upload this `.skill` file to override the prior version, and the skill now writes in their voice.

## Quality bar

- Anchors must be **verbatim** from their mail — paraphrased "anchors" defeat the purpose.
- Every register row in the table should be backed by at least one real example; don't assert a habit you didn't observe.
- If the sample is thin (new mailbox, <20 real replies), say so and offer to re-run later once there's more to learn from. A small, honest profile beats a confident invented one.
