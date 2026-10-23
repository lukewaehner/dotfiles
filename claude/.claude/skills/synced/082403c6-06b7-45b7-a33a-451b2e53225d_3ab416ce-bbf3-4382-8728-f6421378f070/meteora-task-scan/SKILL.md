---
name: meteora-task-scan
description: Weekday 9am/1pm/4pm email scan: Vik/Luke/Aidas PLUS any email mentioning Rishi/AI-interns as doing the work; surfaces NEW tasks + UPDATES and AUTO-UPDATES THE LIVE BOARD every run; reads & writes board-state.json (the live board) + regenerates tasks.json, writes scan-proposals.json + digest; reconciles the user's manual edits (manual edits win).
---

You are the email-scan engine behind Rishi's "Meteora Task Board". Each run you (1) read the LIVE board, (2) scan email, (3) merge NEW action items + UPDATES into the board honoring any manual edits the user made, and (4) write the updated board back so the artifact is always live — then print a ranked digest. This is a read-only EMAIL job — do NOT send, reply to, draft, or forward any email; just read and summarize. (Reading and WRITING the local board/output files described below is the whole point of this job and is expected.)

## ENCODING SAFETY RULES (learned 2026-06-29 — apply everywhere in this skill)

Windows defaults to **cp1252** for all file I/O unless you say otherwise. Reading or writing any file without explicit UTF-8 encoding silently corrupts non-ASCII characters (`·`, `→`, `✨`, etc.) into mojibake (`Â·`, `â†'`, `ðŸ'`). This corruption is invisible at write time and only appears when the artifact renders — often runs later.

**PowerShell reads — ALWAYS add `-Encoding UTF8`:**
```powershell
# CORRECT
Get-Content 'file.json' -Raw -Encoding UTF8

# WRONG — defaults to cp1252, silently corrupts non-ASCII
Get-Content 'file.json' -Raw
```

**Python file I/O — ALWAYS pass `encoding='utf-8'`:**
```python
# CORRECT
open(path, 'r', encoding='utf-8')
open(path, 'w', encoding='utf-8')

# WRONG — inherits OS code page (cp1252 on Windows)
open(path, 'r')
open(path, 'w')
```

**JavaScript string literals in migrate() patches — use `\uXXXX` escapes for non-ASCII:**
```javascript
// CORRECT — pure ASCII, survives any encoding pipeline
tN.who = 'Vik · Aidas · Luke';   // · = U+00B7
tN.next = 'Review → ship';             // → = U+2192

// RISKY — literal chars can be re-encoded when the patch file is written
tN.who = 'Vik · Aidas · Luke';
```
This matters especially for `who` fields (which use `·` separators) and any string that is assembled in Python/PowerShell and then injected into the HTML.

CONTEXT
- The user is Rishi Chauhan, who operates as `chauhan_intern@meteoracapital.com` and is part of the `AI_Interns` distro. He leads the AI/research tooling buildout at Meteora Capital.
- EMAIL TOOLING — CRITICAL: Use ONLY the "Email Assistant — Microsoft 365" connector (extension). Call its tools EXPLICITLY by their fully-qualified names and do NOT default to any other connected email/Graph/Outlook server:
  • mcp__Email_Assistant__Microsoft_365___search_emails  (args: sender, subject, after, folder, max_results, flagged_only)
  • mcp__Email_Assistant__Microsoft_365___read_thread  (args: message_id)
  • mcp__Email_Assistant__Microsoft_365___download_email_as_eml  (use when a thread has visuals/images/embedded tables or hyperlinks to extract — the .eml exposes the full HTML body, every href, and image attachments)
  • mcp__Email_Assistant__Microsoft_365___save_thread_markdown  (use for very long chains)
  If another email connector appears, ignore it. If the Email Assistant connector is offline, wait briefly and retry once; if still offline, say so and stop. (Confirm with mcp__Email_Assistant__Microsoft_365___whoami if unsure it is active.)

STEP 1 — LOAD & RECONCILE THE LIVE BOARD (do NOT hardcode it)
- The LIVE board state is the FULL task objects the Task Board artifact reads and writes: C:\Users\rishi\Desktop\Rishi\Projects\Meteora Capital\board-state.json (Desktop Commander read_file). The artifact writes this file on every manual edit, so it ALWAYS reflects the user's latest manual changes (status drags, edited fields, dismissed/added tasks). READ IT FIRST.
  • Shape: `{updated, source, lastScanAt, dismissed:[normalized-titles], tasks:[{id,ref,title,status,pri,eff,cl,thread,who,due,onList,whatIs,done,next,start,phase,phases,timeline,ai,notes}]}`.
  • `phases` = array of `{name,done}` over the 5 phases [Scoping, Development, Testing, Documentation, Done]; `timeline` = array of `[dateLabel, text]`; `notes` = array of `{ts,who,text}`.
- **FAST READ (CRITICAL — learned 2026-06-29)**: board-state.json is ~75KB. Use a SINGLE Desktop Commander start_process call with PowerShell to read the ENTIRE file at once rather than chunked reads:
  `powershell -command "Get-Content 'C:\Users\rishi\Desktop\Rishi\Projects\Meteora Capital\board-state.json' -Raw -Encoding UTF8 | Out-String"`
  **`-Encoding UTF8` is mandatory** — omitting it causes PowerShell to read as Windows-1252 (cp1252), silently corrupting every non-ASCII character (`·`, `→`, `✨`, etc.) into mojibake (`Â·`, `â†'`). This was the root cause of the garbled task board incident (2026-06-29).
  If the output is truncated by the process monitor, use `-First 1200` (or more) lines — read enough to see ALL tasks. Never read in 500-line chunks if the file has >500 lines, as that misses later tasks and causes wrong gap detection.
- Fallback order if board-state.json is missing/unreadable: read tasks.json (slim `{updated, tasks:[{id,ref,title,status,pri,eff,cl,thread}]}`) and treat it as the board (hydrate minimal objects); if that is also missing, note it and proceed with NEW-task detection only. NEVER hardcode a task list.
- board-state.json is the SOURCE OF TRUTH for what already exists AND for the user's manual edits. Use it to (a) never duplicate a task, (b) match UPDATES by id / normalized title / thread, and (c) RESPECT manual edits per STEP 5.

STEP 2 — SCAN EMAIL (TWO PASSES, then merge & dedupe) — all via the Email Assistant — Microsoft 365 connector
Window: after = today minus 1 day (ISO). Folders to cover (EXCLUDE Sent Items, Deleted Items, Junk Email, Drafts, Outbox, Conversation History): Inbox, Archive, Communication, Auto SEC Filings Update, Memory Doc Seeds, Memory Doc Update, Merger Arb Events, DAR Reports, Meteora Daily, SPAC Top Movers Email.

PASS A — by sender: for each folder, call mcp__Email_Assistant__Microsoft_365___search_emails with sender = Vik (vik@meteoracapital.com), then Luke (lgries@meteoracapital.com), then Aidas (APuskorius@meteoracapital.com).

PASS B — by mention (ANY sender, SUBJECT *and* BODY): ALSO capture any email — regardless of who sent it — that indicates Rishi or the AI interns are to do or discuss the work. CRITICAL: the mention is frequently in the BODY, not the subject (a thread titled "Internal TDAC" or "Bixi cslm3" can still say "@Rishi Chauhan ..." in the body). So do NOT rely on the `subject` filter alone. Run it BOTH ways and union the results:
  (i) Cheap pass — run mcp__Email_Assistant__Microsoft_365___search_emails (no sender) with the `subject` filter for "Rishi", "Chauhan", "AI interns", "interns".
  (ii) Body pass (PRIMARY, do this every run) — pull the most recent ~20 threads per folder (no subject filter) and READ each one's subject AND body, keeping any whose subject OR body contains: "Rishi", "Chauhan", "chauhan_intern", "AI interns", "AI_Interns", "@Rishi", "Arsh", or any phrasing that assigns/implies Rishi or the interns own or discuss the work — e.g. "Rishi will / to / is working on", "have/ask/loop in/sit with/work with/discussed with Rishi", "for the interns", "intern team to", "let's get Rishi", "Rishi can you", "@Rishi <verb>". Treat this body scan as the main detector, the subject filter as a supplement. Do NOT restrict Pass B to the three senders, and do NOT assume the subject reflects whether Rishi is involved — check the body.

PASS C — RISHI'S OWN SELF-NOTES (CRITICAL — added 2026-06-23): Rishi logs progress by REPLYING TO HIMSELF on these chains (From `chauhan_intern@meteoracapital.com` → To `chauhan_intern@meteoracapital.com`, often beginning "Note for self ..."). Pass A misses these (he is not Vik/Luke/Aidas) and Pass B's subject filter misses them (the thread subject usually has no "Rishi"/"Chauhan" token), so they are invisible unless you look for them explicitly. EVERY run: call mcp__Email_Assistant__Microsoft_365___search_emails with sender = `chauhan_intern@meteoracapital.com` across BOTH the normal folders AND `SentItems` (self-notes land in Sent and Inbox; this is the ONE case where you DO read Sent Items). The TRIGGER IS STRUCTURAL, NOT THE WORDING: keep EVERY message that is self-addressed — From `chauhan_intern@` AND To includes `chauhan_intern@` — regardless of what it says. Do NOT require the phrase "Note for self". Rishi logs these with whatever prefix he likes — "Note for self", "Note", "Note for task", "Note to self", "note re <ticker>", "todo", "update", "reminder", "fyi self", or no prefix at all — and any of them (or none) counts. If it's a self-addressed email, READ it and treat its content as a progress log. These are Rishi's OWN words = the STRONGEST progress signal (per STEP 3.5): map each to its existing task by normalized subject / thread and emit an UPDATE (status advance, `done`, `next`, new people/dates). They are almost always UPDATES to an existing task; only create a NEW task if the self-note describes work that isn't tracked yet. Example handled this way: the DataTracks thread — a self-note "Followed up with jack. Will reconnect tomorrow (23rd June)" advanced #11 to In progress.

PASS D — RISHI'S OWN OUTBOUND ON TRACKED THREADS (CRITICAL — added 2026-06-24 after the AP2 / HY / Mercator misses): Rishi's MOST IMPORTANT progress reports are NOT self-notes — they are his REGULAR outbound replies on existing tracked threads, often with an attached deliverable, a "Quick update" header, or a scoping question to a teammate. These do not match Pass A (he's not Vik/Luke/Aidas), do not match Pass B's subject filter (thread subjects like "AP2 — Re: [BamSEC] TDAC filed a new Form 425" or "Internal. Fw: Mercator SPAC Risk Capital Docs" contain no "Rishi" token), and do not match Pass C (they have other To: recipients, not self-addressed). Without Pass D they are completely invisible — and you will miss skill ships, deliverable handoffs, and scope-overlap calls.
  EVERY run, in addition to Pass C: call mcp__Email_Assistant__Microsoft_365___search_emails with sender = `chauhan_intern@meteoracapital.com` in `SentItems` over the window (use max_results >= 100). For every result, normalize the subject (strip Re:/Fw:/Fwd:) and check whether the normalized subject matches an existing `tasks[].thread` on the board (substring match EITHER direction; thread subjects often only contain a fragment of the email subject, e.g. board thread "AP2 / Translational Development 425" vs email subject "AP2 — Re: [BamSEC] Translational Development Acquisition Corp. filed a new Form 425" — both directions count). If it matches OR the message has attachments OR the body contains any of: "I've built", "I built", "I've shipped", "I shipped", "I've made", "I made", "attached", "Quick update", "Sharing an artifact", "Sharing another skill", "sharing a skill", "ready to swap", "I'll reach out", "Will reach out", "Note to self", "Note for self", or any "@<name>" scoping question ("would this be different from", "is this duplicative", "does this overlap", "different from the X we've been working on") — MANDATORY READ the full thread. These are deliverable ships, action commitments, or scope checks and are the strongest possible task-progress signals; missing one means the board says Pending when the work is already shipped.
  Pass D is NOT capped at 12 threads — read every match. The 12-thread cap below applies only to Pass A/B reads.

Merge Pass A + Pass B + Pass C + Pass D, dedupe threads by normalized subject (strip leading Re:/Fw:/Fwd:). READ ORDER (mandatory minimums, do not skip): (1) ALL Pass D matches (Rishi-outbound on tracked threads or with attachments / ship/scope keywords) — uncapped; (2) ALL Pass C self-notes — uncapped; (3) UP TO 12 most recent additional Pass A + Pass B threads. If Pass C + Pass D together already exceed 12, that's fine — read them anyway. When a thread carries a Rishi self-note OR a Rishi outbound to a tracked thread, ALWAYS include it among the threads you read.

NEVER ASSUME A THREAD IS "ALREADY CAPTURED" BECAUSE ITS PARENT TASK EXISTS ON THE BOARD. The board records what was true at the LAST scan; the whole point of this run is to find what changed since then. Rishi may have shipped a deliverable, asked a scope question, or committed to a next-day action on a thread whose parent task is already #N on the board — and that's exactly the case Pass D catches. The cost of reading one extra thread is small; the cost of missing a deliverable ship (per the 2026-06-24 AP2 miss: Rishi shipped the news-monitor skill on the AP2 chain and the scanner read only the subject) is the board lying to the user for days.

STEP 3 — CLASSIFY each relevant thread against the loaded board (STEP 1):
- NEW TASK — a clear, previously-untracked action for Rishi / the AI interns (build, fix, research, deliverable, scheduled review, explicit @mention, or someone stating Rishi/AI-interns will handle it). Must NOT match an existing task.
- UPDATE TO EXISTING TASK — maps to an existing task AND carries a material change: new instruction/scope, new info/decision, status change (started/blocked/done/deferred), new deadline, new person to involve, or feedback to fold in. Reference it by its id.
- IGNORE — FYIs, thanks/acknowledgements, social, market commentary, automated feeds, and anything where the work clearly belongs to someone else and Rishi/AI-interns are NOT named or implied as doing/discussing it.
For each UPDATE give exact field edits using these keys where relevant: status (Pending/Active/In progress/Blocked/Waiting on others/Completed/Cancelled), priority, effort, next, due, who, whatIs, done, and a one-line brainstorm note to append. Quote the short evidence line. For mention-based items, the evidence quote MUST contain the phrase showing Rishi/AI-interns involvement.

STEP 3.5 — INFER PHASE & PROGRESS FROM THREAD CONTEXT (AUTO-UPDATE)
When a thread maps to an existing task, do NOT just append the new instruction — read the LATEST state of the conversation and update the task's PHASE and details to match where the work actually stands. Rishi's own messages (from chauhan_intern@meteoracapital.com) and the AI_Interns replies are the STRONGEST signal — weight them above anyone else's, and prefer Rishi's MOST RECENT message in the thread.
- Map language → status (only move a task FORWARD, never backward, unless an explicit blocker/termination appears):
  • Assignment with no Rishi/intern reply yet → leave Pending.
  • "will look into / will research / noted, will add to plans / taking a stab / starting on" → Active (owned & started).
  • "I set up / I built / I made / repackaged / I identified / root cause is / prototyped / tested / sharing findings / here's the result / I did X" → In progress (substantive work done) — capture WHAT was done in `done` and `note`.
  • "waiting on / blocked on / need X from Y first" → Blocked or Waiting on others (name the dependency in `next`).
  • "done / shipped / live / works / resolved / closed out" → Completed.
- DELIVERABLE SHIP (added 2026-06-24): the strongest possible UPDATE signal. Rishi outbound on a tracked thread with an attachment AND/OR phrases like "I've built / shipped / made", "attached the X here", "Quick update — I've X", "Sharing an artifact / a skill / a file I built", "ready to swap", "Attaching a general template" = a DELIVERABLE was shipped to the team. REWRITE `done` to describe the shipped artifact in concrete terms (what it does, who it's for, cadence/scope/scale numbers, where it was attached). REWRITE `next` to capture every follow-up Rishi himself named in the same email (look for "A few things I'll need to" / "Next steps —" / "Open items:" / numbered lists). Advance the phase forward at least one step. If status was Pending/Active, move to In progress (or Completed if Rishi explicitly says shipped + done). Append a dated timeline + note. Never just "append a note" on a ship message — the `done` field MUST reflect the new reality.
- SCOPING QUESTION TO A TEAMMATE (added 2026-06-24): Rishi outbound on a tracked thread asking a colleague a scope/overlap/duplication question — e.g. "@Luke would this be different from the redline tool we've been working on?", "is this duplicative of what we're doing with X?", "does this overlap with Y?". CAPTURE THE QUESTION VERBATIM in a `note`. UPDATE `next` to "Awaiting <name>'s answer on <question>." If the question implies an in-flight workstream that isn't on the board, FLAG it under "⚠️ NEEDS YOUR CALL" in the digest — the user may want to add that workstream as its own task.
- Extract concrete progress from Rishi's replies into `done` (what is finished/started) and his stated follow-up into `next`. Pull any new people, deadlines, decisions, or technical context (even from others' replies) into `who`/`due`/`note`.
- The evidence quote for a phase change should be Rishi's own words wherever possible (e.g. "Will look into this linked lists method...").
- If the thread shows Rishi already acted on a task the board still lists as Pending, that IS a material change — emit the UPDATE even if no new instruction was given.

STEP 4 — MERGE INTO THE LIVE BOARD, THEN WRITE ALL OUTPUTS
Work on the in-memory board you loaded in STEP 1. Apply your STEP 3 classifications to it under the STEP 5 reconciliation rules:
- NEW TASK → append with `id = (max existing id)+1`, `ref = "#"+id`. Build a full object compatible with the artifact: status Pending (or Active/In progress if the thread shows it already started), pri/eff/cl from your classification, who, due "from email scan", thread, onList "New (email)", whatIs=summary, done "—", next=start=suggestedStart, phase "Scoping", phases = the 5-phase template with none done (or [0] done if started), timeline [[today, evidence]], ai=summary, notes []. SKIP if its normalized title/thread already matches an existing task OR appears in board-state.json `dismissed`.
- UPDATE → apply the exact field edits to the matched task (keys map to board fields: priority→pri, effort→eff, cluster→cl; status/who/due/next/whatIs/done/phase as-is). APPEND a dated timeline entry. Timeline entry format: [dateLabel, text] where text is plain evidence with NO prefix (write "Vik: refine the GRAF note" not "From scan: Vik: ..."). Always guard with `if(!tN.timeline.some(e=>e[1]===text)) tN.timeline.push([date, text])` to prevent duplicates on re-runs. Advance `phases`/`phase` only forward.
- BRAINSTORM / NOTES IS USER-MANUAL ONLY (added 2026-06-24): the `notes` array on every task powers the user-facing "BRAINSTORM / NOTES" widget — it's their personal notepad. The scan MUST NEVER write to `notes`. Do not append `{who:"AI", ...}` notes. Do not append any AI-authored note under any other `who` value either. All scan-derived context belongs in `timeline` (dated, machine-readable changelog) and the structured fields `done`, `next`, `whatIs`, `who`, `due`. The user owns `notes` end-to-end. The same rule applies to the migrate() patches: never `push` to `t.notes`. The only legitimate touch to `notes` in migrate() is a one-time cleanup to delete previously-written `who:"AI"` entries (already inserted 2026-06-24).

Then WRITE these files (Desktop Commander write_file), in order, to C:\Users\rishi\Desktop\Rishi\Projects\Meteora Capital\:
  A) board-state.bak.json — a verbatim copy of the board you LOADED in STEP 1 (recovery point), BEFORE applying changes. Copy with: `powershell -command "Copy-Item '<src>' '<dst>' -Force"`
  B) board-state.json — the merged FULL board: `{updated:"<ISO now>", source:"scan", lastScanAt:"<ISO now>", dismissed:<carry forward unchanged>, tasks:[...full objects...]}`. THIS IS THE LIVE BOARD — the artifact loads it on open, so the board updates every run with no manual step. Write the WHOLE object for every task; preserve every rich field you did not change (whatIs, done, phases, timeline, notes, ai, start, onList, …). Never write a trimmed task.
  C) tasks.json — regenerate the slim lookup FROM the merged board: `{updated:"<date>", tasks:[{id,ref,title,status,pri,eff,cl,thread}]}`. Keeps backward-compat and the export path in sync.
  D) scan-proposals.json — audit/handoff of THIS run only. CRITICAL FORMAT (learned 2026-06-29): `changes` MUST be an OBJECT of `{field: newValue}` pairs — NEVER a string. `applyProposals()` in the artifact calls `Object.entries(u.changes)` which on a plain string returns character-index pairs like `["0","n"]` and corrupts task objects. Required shape:
  ```json
  {
    "generatedAt": "<ISO timestamp>",
    "newTasks": [
      {
        "title": "...",
        "priority": "P1|P2|P3|Track",
        "effort": "Quick|Medium|Long|Med",
        "cluster": "A|B|C|D|S",
        "who": "...",
        "thread": "...",
        "suggestedStart": "...",
        "summary": "...",
        "evidence": "..."
      }
    ],
    "updates": [
      {
        "id": 2,
        "changes": { "status": "In progress", "next": "..." },
        "note": "",
        "evidence": "..."
      }
    ]
  }
  ```
  Overwrite each run; empty arrays if nothing.

STEP 4.6 — PUSH THE DELTA INTO THE LIVE ARTIFACT (REQUIRED EVERY RUN — this is what actually updates what the user sees)
CRITICAL REALITY CHECK (learned 2026-06-23): the Task Board artifact does NOT load board-state.json on open. It renders from its own browser localStorage and only mutates it two ways: (1) its on-load `migrate(t)` function, which runs idempotent patches against the localStorage tasks every load, and (2) an in-page `autoImportScan()` that tries to read scan-proposals.json via the connector — but that in-sandbox connector read does NOT fire reliably, so DO NOT depend on it. `board-state.json` is OUTBOUND only (the artifact WRITES it via persistState; on load it reads only the `dismissed` ledger from it). Therefore writing the JSON files in STEP 4 is necessary for the scan's own bookkeeping but is NOT sufficient to update the board the user looks at. You MUST also inject the delta into the artifact's `migrate()` function. Do this every run:

- Artifact file: C:\Users\rishi\Documents\Claude\Artifacts\meteora-task-board\index.html
- **HOW TO EDIT THE FILE (learned 2026-06-29 — Desktop Commander edit_block is unreliable for multi-line JS; use Python):**
  1. Write a Python script to `C:\Users\rishi\AppData\Local\Temp\patch_artifact.py` using Desktop Commander write_file
  2. The script: `open(html_path, 'r', encoding='utf-8')` to read, `content.replace(old_marker, new_marker+patch)`, `open(html_path, 'w', encoding='utf-8')` to write back. **Both open() calls MUST have `encoding='utf-8'`** — the artifact HTML contains non-ASCII characters (·, →, etc. in the SEED data); opening without UTF-8 corrupts them. Handle both `\n` and `\r\n` line endings.
  3. **Non-ASCII in JS string literals — use `\uXXXX` escapes**: any non-ASCII character assembled in Python and injected into the JS source (e.g. `who` field values containing `·`) must be written as `·` (etc.) rather than the literal character. Python string → HTML file → browser is a lossy pipeline for non-ASCII literals; `\uXXXX` escapes are pure ASCII and survive it intact.
  4. Run it: `mcp__Desktop_Commander__start_process` → `python "C:\Users\rishi\AppData\Local\Temp\patch_artifact.py"`
  5. Verify the patch landed: `Select-String -Path '<html>' -Pattern '<your new comment>'`
  DO NOT use PowerShell heredocs for multi-line strings containing JS — heredoc handling fails with embedded quotes and special chars. DO NOT use `edit_block` for long JS patches — it uses fuzzy search that may match the wrong location.

- Find the END of the `migrate(t)` function (it ends with `  }catch(e){}` then `  return t;` then `}` — the same block that already contains the #3 and #19 patches). Insert your new patches immediately BEFORE `  return t;`.
- For each NEW task: guard with `if(!t.some(x=>x.id===N)){ t.push({ ...full object... }); }` using the SAME id N you assigned in board-state.json, and `phases:ph([])` (or `ph([0])` if started). This makes it idempotent — it adds once and never duplicates.
- For each UPDATE / status change (incl. user-confirmed completions & cancellations): guard so it only fires once and FORWARD-ONLY, e.g. `const tN=t.find(x=>x.id===N); if(tN && tN.status!=='Completed'){ tN.status='Completed'; tN.phase='Done'; tN.phases=ph([0,1,2,3,4]); tN.done=...; tN.next='—'; tN.timeline.push([...]); }`. Mirror exactly the field edits you wrote to board-state.json. Never `push` to `tN.notes` — that's the user-manual brainstorm pad. Never re-open a manual terminal state (respect STEP 5); never re-add a title in the `dismissed` ledger (just leave it out of migrate — do not push it).
- Use `ph(...)`, `CL`, and the existing helpers already defined in the file. Keep every inserted statement valid JS on its own lines.
- UNIQUE VARIABLE NAMES — CRITICAL (learned 2026-06-24): `migrate(t)` is one function body, so every `const` (and `let`) inside it shares the same block scope, including across prior date-stamped patches. Re-using a name another patch already declared is a SyntaxError and the WHOLE PAGE renders blank (no tasks at all, no console message from the user's side) until it's fixed. Before inserting your block: (a) grep the file for every `const t<digits><suffix>=` and every `const n<digits><suffix>=` / `const tl<digits>=` already in `migrate()`; (b) pick suffixes that are unused — bump to the next letter (`t21b` already exists → use `t21c`, then `t21d`, etc.); do the same for inner notes (`n21a/n21b/n21c` → `n21d/...` if those collide); (c) `var` declarations (as opposed to `const`) are function-scoped and do NOT collide by name — prefer `var` for all migrate() variables to avoid this class of bug entirely; (d) AFTER editing, MANDATORY syntax check (see below).
- **MANDATORY SYNTAX CHECK (learned 2026-06-29 — NEVER skip this):** Before re-registering:
  ```powershell
  # Extract the main script and check with Node
  # -Encoding UTF8 is MANDATORY — omitting it corrupts non-ASCII chars in the JS
  $html = Get-Content 'C:\Users\rishi\Documents\Claude\Artifacts\meteora-task-board\index.html' -Raw -Encoding UTF8
  $js = [regex]::Match($html, '(?s)<script(?! type=)[^>]*>(.*?)</script>').Groups[1].Value
  $js | Out-File 'C:\Users\rishi\AppData\Local\Temp\artifact_script.js' -Encoding UTF8
  ```
  Then: `node -e "const fs=require('fs'),vm=require('vm');try{vm.compileFunction(fs.readFileSync('C:\\Users\\rishi\\AppData\\Local\\Temp\\artifact_script.js','utf8'),[]);console.log('SYNTAX OK');}catch(e){console.log('ERROR:',e.message);}"`
  If it says ERROR — fix the variable name collision or syntax issue and re-check. DO NOT proceed to update_artifact until you see "SYNTAX OK".
- THEN re-register the artifact so the host serves the new file: mcp__cowork__update_artifact requires html_path INSIDE the session workspace, so first copy the edited file:
  `powershell -command "Copy-Item 'C:\Users\rishi\Documents\Claude\Artifacts\meteora-task-board\index.html' '<session-outputs>\index.html' -Force"`
  Then call mcp__cowork__update_artifact with id "meteora-task-board", html_path=<that outputs copy>, and a one-line update_summary.
- **POST-REGISTER VERIFICATION (learned 2026-06-29)**: After update_artifact, tell the user "Board updated — please click Reload in the artifact header. If tasks don't appear, click Reset (restores SEED + migrate patch)." This surfaces any silent failures immediately instead of leaving a blank board undetected.
- IDEMPOTENT: because every patch is guarded (id-not-present for adds, status-not-already-Completed for completions, deduped note pushes), re-running the scan re-applies cleanly — applying twice == applying once. If there is no delta this run, skip the artifact edit.

STEP 5 — RECONCILIATION RULES (manual edits ALWAYS win)
The board you loaded may contain changes the user made since the last run. Honor them:
- FORWARD-ONLY status: only advance a task (Pending → Active → In progress → Completed) per the STEP 3.5 ladder. NEVER move a task backward.
- MANUAL TERMINAL STATES STICK: if the user set a task to Completed or Cancelled, do NOT reopen it. If new email clearly reactivates it, do NOT silently revert — leave it and FLAG it in the digest under "⚠️ NEEDS YOUR CALL".
- MANUAL FIELD EDITS STICK: if the user changed priority, effort, title, who, due, status, etc., keep their value. Only fill fields that are empty/placeholder ("—"), or append to notes/timeline. Never overwrite a user-entered value with a scan guess.
- NO RESURRECTION: never re-add a task whose normalized title is in `dismissed`, and never recreate a task the user removed.
- DEDUPE: match existing tasks by id first, then normalized title (strip Re:/Fw:/Fwd:), then thread. One task per real piece of work.
- IDEMPOTENT: re-running on the same emails must not create duplicates or churn fields — applying twice == applying once.

STEP 6 — PRINT THE DIGEST (the board is ALREADY updated — this is the readout)
   1. One-line header: scan time, # new tasks, # updates, # flagged.
   2. "🔴 FOCUS NOW": single most urgent item (new or updated; if nothing new, the most urgent existing board item — clear SPAC-reliability + email-plumbing gates first, then push AP2).
   3. "🆕 NEW TASKS": #id Title — evidence — priority/effort/cluster (A=research engine,B=email tooling,D=ops,S=standalone) — who — first step.
   4. "✏️ TASK UPDATES": #id (title) — what changed — exact field edits — evidence.
   5. "⚠️ NEEDS YOUR CALL": any conflict where email contradicts a manual terminal state (only if any).
   6. If nothing changed: "No new action items or updates — board is current ✅".

Keep it tight and scannable. Use ONLY the Email Assistant — Microsoft 365 connector for email; read-only on email; never send anything. Writing the board/output files is expected.

POSTMORTEM — KNOWN FAILURE MODES (each one was a real miss; this section exists so the scanner stops making them)
1) 2026-06-24 AP2 DELIVERABLE-SHIP MISS. Rishi shipped the news-monitor skill as an attachment on the AP2 chain (350+ tickers, ~45 min cadence, posts to each ticker's chain, pulls book position from MCP). The scanner read the subject of the AP2 thread but did NOT open it because the parent task #1 was already on the board. Result: `done` on #1 still said "skill BUILT" when the truth was "skill BUILT and SHIPPED publicly on the chain with these three named follow-ups." Root cause: no Pass D for Rishi-outbound on tracked threads. Fix: Pass D above + the DELIVERABLE SHIP rule in STEP 3.5. Self-check every run: did you read every SentItems thread whose normalized subject matches an existing board `thread`? If no, you skipped Pass D.
2) 2026-06-24 HY RESEARCH SELF-NOTE MISS. Rishi self-noted "Will reach out Larry today regarding this and other sell side research" on the DB HY thread. The scanner's regex for self-notes had a body-format dependency and missed the message. Root cause: format-coupled detection instead of structural. Fix: Pass C already says the trigger is STRUCTURAL (From = Rishi AND To includes Rishi), so the SentItems search alone should surface this. Always read every self-addressed result from the SentItems search regardless of body shape. Do NOT use regex to filter the self-note bodies before reading them — read first, classify after.
3) 2026-06-24 MERCATOR SCOPING-QUESTION MISS. Rishi asked Luke on-thread "would this be different from the redline tool we've been working on?" — a scope-overlap question that implies an in-flight workstream not currently on the board. The scanner read the thread (because Vik was sender on Pass A) but classified Rishi's reply as a minor "still scoping" note instead of a material UPDATE that should change `next` and flag a NEEDS YOUR CALL. Fix: SCOPING QUESTION rule in STEP 3.5 above.
4) 2026-06-24 BRAINSTORM CONTAMINATION. The earlier version of this skill instructed the scan to "APPEND (never overwrite) a deduped AI note `{ts:today,who:"AI",text:<brainstorm note>}`" on every UPDATE. The board's `notes` array is rendered as the user-facing BRAINSTORM / NOTES widget — it's their personal notepad. Stuffing AI-generated context into it polluted the pad with scan output and crowded out the user's own thoughts. Root cause: confused two concerns — machine-readable changelog (correct home: `timeline`) vs. user-manual brainstorm pad (correct home: `notes`, owned by the user only). Fix: ban writing to `notes` in both the JSON merge (STEP 4) and the artifact migrate patches (STEP 4.6). All scan-derived context goes into `timeline` and the structured fields (`done`, `next`, `whatIs`, `who`, `due`). One-time migrate cleanup removed every existing `who:"AI"` note from localStorage so the BRAINSTORM widget shows only the user's own entries going forward.
5) 2026-06-29 SLOW RUN — MULTIPLE FAILED EDIT ATTEMPTS. The artifact HTML edit took 4 failed attempts (edit_block without loading schema → PowerShell heredoc with quote conflicts → Python inline in bash heredoc → finally Python written to temp file). Root causes: (a) edit_block needs ToolSearch to load schema first; (b) PowerShell heredoc can't handle embedded JS quote characters; (c) Python can't be used inline in bash heredocs with complex strings. Fix: ALWAYS write Python edits to a temp file via Desktop Commander write_file, then run `python <tempfile>`. Documented in STEP 4.6 "HOW TO EDIT THE FILE" above.
6) 2026-06-29 BOARD READ TOO SLOW. board-state.json was read in 500-line chunks, requiring 3+ separate process calls and missing tasks #18+ on the first read. Fix: use `Get-Content ... -Raw -Encoding UTF8` in a single call, or use `-First 1500` to get the whole file. Documented in STEP 1 "FAST READ".
7) 2026-06-29 SCAN-PROPOSALS FORMAT BUG → BLANK BOARD. scan-proposals.json was written with `changes: "string"` (human-readable description) instead of `changes: {"field": "value"}` (machine-readable object). The artifact's `applyProposals()` calls `Object.entries(u.changes)` — on a string this returns character-index pairs like `["0","n"]` and sets garbage numeric properties on every task object, potentially breaking the card renderer. Fix: always write `changes` as an object of field-value pairs. If a field didn't change, omit it (or use `changes: {}`). Format documented in STEP 4 scan-proposals.json spec above.
8) 2026-06-29 NO POST-REGISTER VERIFICATION. After calling update_artifact, the board was left blank without a clear "please Reload" instruction. Fix: always end the run with the verification instruction in STEP 4.6. If user reports blank board after Reload, tell them to click Reset (which re-runs SEED + migrate()).
9) 2026-06-29 ENCODING CORRUPTION — GARBLED WHO FIELDS (Â·, â†'). Root cause: multiple encoding failures compounding across the pipeline: (a) PowerShell `Get-Content` without `-Encoding UTF8` reads UTF-8 files as cp1252, corrupting non-ASCII chars on read; (b) Python `open()` without `encoding='utf-8'` does the same on write; (c) non-ASCII literals (`·`, `→`) in JS string literals embedded in HTML via Python string injection got re-encoded at each step, turning `·` (U+00B7) into `Â·` (U+00C2 U+00B7) then `Ã‚·` (double-garbled). The corruption propagated into localStorage and persisted across sessions. Fix: (a) `-Encoding UTF8` on ALL PowerShell `Get-Content` calls — see STEP 1 and STEP 4.6 syntax-check block; (b) `encoding='utf-8'` on ALL Python `open()` calls — see STEP 4.6 HOW TO EDIT; (c) `\uXXXX` escapes for any non-ASCII char assembled in Python and injected into JS source — see STEP 4.6 non-ASCII guidance. A localStorage guard (`Â·` indexOf check) was also added to the artifact's startup code to auto-clear any lingering garbled data on first load.

SELF-CHECK BEFORE WRITING THE DIGEST:
- For every existing tracked task whose `thread` field appears in the SentItems search results for the window, confirm you actually called `read_thread` on that thread this run. If you didn't, do it before finalizing. The 12-thread cap NEVER applies to a thread Rishi sent to in the window.
- For every UPDATE you're about to write to board-state.json and to the migrate patch: confirm you are NOT touching the `notes` array. If you are, move that text into `timeline` (dated) and into the appropriate structured field (`done` for what's finished, `next` for what's pending, `whatIs` for scope).
- MANDATORY: confirm syntax check passed ("SYNTAX OK" from Node) before calling update_artifact.
- MANDATORY: confirm scan-proposals.json `changes` fields are objects, not strings.
- MANDATORY: confirm all PowerShell file reads use `-Encoding UTF8` and all Python file opens use `encoding='utf-8'`.
- MANDATORY: confirm any non-ASCII characters in migrate() JS string literals are written as `\uXXXX` escapes, not literal chars.
