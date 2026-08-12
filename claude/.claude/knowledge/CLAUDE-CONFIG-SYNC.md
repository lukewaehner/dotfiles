# Claude Code Multi-Instance Config

Context and maintenance procedure for the three-instance Claude Code setup.
Place in `scripts/` or `hooks/`. Read this before editing any Claude config.

---

## The Setup

Three Claude Code instances run from separate config directories, invoked by alias:

| Instance | Config dir | Login |
|---|---|---|
| personal | `~/.claude` | personal |
| school | `~/.claude-school` | Northeastern |
| work | `~/.claude-work` | Meteora |

**`~/Repos/dotfiles` is the source of truth**, via stow. `~/.claude` is no
longer a real directory tree — its shared entries are symlinks into
`dotfiles/claude/.claude/`, and school and work symlink to `~/.claude`. Edits
land in the repo and are versioned.

Restow after adding anything new to the package:

```bash
cd ~/Repos/dotfiles && stow --restow claude
```

**Logins are fully isolated.** This is deliberate and load-bearing — never sync
anything in the "never touch" list below or you will cross-wire accounts.

---

## What's Shared vs. What Isn't

### Stowed from the repo → auto-syncs, versioned

```
hooks/
agents/
commands/
skills/
plugins/
rules/
knowledge/
get-shit-done/
gsd-file-manifest.json
gsd-install-state.json
gsd-migration-journal
.gsd-profile
```

Plus `~/.agents/` — a sibling of `~/.claude`, stowed from
`dotfiles/claude/.agents/`. It holds the 27 installed agent skills that
`~/.claude/skills/` symlinks into. It has to stay a sibling: those inner links
are relative (`../../.agents/skills/X`), so the two directories must keep the
same parent or every skill breaks. See Troubleshooting.

Edit any of these in the repo and all three instances see it immediately.
No propagation step needed.

### Merged from a template → run the sync script

```
settings.json
settings.local.json
```

These are **app-mutable** — Claude Code rewrites them on `/model`, theme
changes, and permission prompts. A symlink would let one instance's runtime
writes clobber the others, so stow can't manage them.

Instead, the shared keys live in a tracked template,
`dotfiles/claude/.claude/settings.template.json`, and a script merges them into
each instance while leaving per-instance keys alone:

```bash
sync-claude-settings.sh           # report drift, change nothing
sync-claude-settings.sh --apply   # back up, then merge
```

Shared (in the template, propagated): `hooks`, `statusLine`, `enabledPlugins`,
`tui`, `skipDangerousModePermissionPrompt`.

Per-instance (never overwritten): `model`, `theme`, `effortLevel`,
`permissions`.

That split is the whole point. The old procedure was a blind `cp`, which is
what destroyed per-instance state during the 2026-07-23 unification — see
Known Side Effects below. A merge can't.

### Never touch — isolation depends on it

```
.claude.json
.credentials.json
projects/
sessions/
history.jsonl
```

Plus the macOS Keychain entries. Copying or symlinking any of these merges
logins and session state across instances.

---

## Propagating a New Setting

When you add a `statusLine`, hook registration, or any other shared key:

1. Edit `dotfiles/claude/.claude/settings.template.json`.
2. `sync-claude-settings.sh` — review the reported drift.
3. `sync-claude-settings.sh --apply` — backs up each instance to
   `~/claude-config-backups/<timestamp>/` before writing.
4. **Restart the affected sessions.** Claude Code reads `statusLine` and hook
   config once at startup; a running session will not pick up the change.

The script is safe to run any time — with no flag it only reports, exits 1 on
drift, and touches nothing. It refuses to write to an instance whose
`settings.json` is unparseable rather than overwriting it, and exits non-zero
if it finishes with any instance left unrepaired.

If you add a fourth instance, no edit is needed:

```bash
CLAUDE_INSTANCES="$HOME/.claude $HOME/.claude-new" sync-claude-settings.sh
```

### Adding a key that should NOT propagate

Keep it out of the template. Anything absent from the template is invisible to
the sync and survives untouched — that's how `model`, `theme`, `effortLevel`,
and `permissions` stay per-instance.

---

## Known Side Effects of Unification

Historical — the `cp`-based procedure that caused this was replaced by the
merge-based sync script on 2026-08-12. Kept because it documents what
per-instance keys exist and why they're excluded from the template.

A full copy from `~/.claude` overwrites per-instance runtime preferences. Observed
losses from the 2026-07-23 unification:

**school** — lost `permissions.defaultMode`, lost `effortLevel: xhigh`,
model reverted opus → sonnet, theme auto → dark-ansi

**work** — lost `effortLevel: high`, model reverted (Fable) → sonnet,
theme auto → dark-ansi

Model and theme are trivially reset in-session. Permission mode and effort level
are worth pinning.

### Pinning per-instance overrides

`settings.local.json` is layered over `settings.json` and survives the `/model`
and theme writes that mutate the base file. Put instance-specific keys there:

```jsonc
// ~/.claude-school/settings.local.json
{
  "permissions": { "defaultMode": "auto" }
}
```

> ⚠️ **Verify this key.** The original note for this came through garbled —
> confirm the exact shape against Claude Code's current settings schema before
> relying on it.

This is no longer only half a solution. The sync script merges rather than
copies, so any key absent from the template survives a propagation run — a
per-instance override is durable wherever you put it.

---

## Adding a Fourth Instance

```bash
NEW=~/.claude-newinstance
mkdir -p "$NEW"

# symlink the shared surface (point at ~/.claude, which stow owns)
for f in hooks agents commands skills plugins rules knowledge get-shit-done \
         gsd-file-manifest.json gsd-install-state.json \
         gsd-migration-journal .gsd-profile; do
  ln -s ~/.claude/"$f" "$NEW/$f"
done

# seed settings.json from the template, then set per-instance keys in-session
cp ~/Repos/dotfiles/claude/.claude/settings.template.json "$NEW/settings.json"
CLAUDE_INSTANCES="$NEW" sync-claude-settings.sh
```

Then add the alias with `CLAUDE_CONFIG_DIR` pointed at `$NEW`, and log in
separately. Do **not** copy any credential or session file into it.

Add `$NEW` to `INSTANCES` in the sync script so it's covered by future runs.

---

## Troubleshooting

**Statusline not showing** — session predates the config change. Restart it.

**Hook not firing in school/work** — either the hook file isn't under a
symlinked dir, or its registration lives in `settings.json` and hasn't been
propagated. Run `sync-claude-settings.sh` to check the second case.

**Personal skills missing from the skill list** — the installer writes
`~/.agents/skills/X` and links `~/.claude/skills/X` at it *relatively*
(`../../.agents/skills/X`), so the link only resolves while `.agents` and
`.claude` share a parent. Moving either one breaks all of them silently — the
skills just stop appearing, with no error. This is what the 2026-08-12 stow
migration did, and why `.agents` is stowed alongside `.claude` rather than left
in `$HOME`. To check:

```bash
find ~/.claude/skills -maxdepth 1 -type l ! -exec test -e {} \; -print
```

Empty output is healthy. Anything listed is a dead skill.

**Wrong account in an instance** — something touched `.claude.json`,
`.credentials.json`, or the Keychain. Re-authenticate that instance only.

**Symlink got replaced by a real directory** — Claude Code or an installer
wrote through it. Check with `ls -la ~/.claude-work | grep -E 'hooks|plugins'`;
back up the real dir, delete it, recreate the symlink.
