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

**`~/.claude` is the source of truth.** School and work pull from it.

**Logins are fully isolated.** This is deliberate and load-bearing — never sync
anything in the "never touch" list below or you will cross-wire accounts.

---

## What's Shared vs. What Isn't

### Symlinked → auto-syncs, edit once in `~/.claude`

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

Edit these in `~/.claude` and all three instances see the change immediately.
No propagation step needed.

### Copied → requires manual propagation

```
settings.json
settings.local.json
```

These are **app-mutable** — Claude Code rewrites them on `/model`, theme
changes, permission prompts, etc. A symlink would let one instance's runtime
writes clobber the others. So they're copies, and adding a hook or statusline
to `~/.claude/settings.json` does **not** reach school or work until you
propagate. See the procedure below.

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

When you add a `statusLine`, hook registration, permission rule, or any other
key to `~/.claude/settings.json`:

```bash
for d in ~/.claude-school ~/.claude-work; do
  cp ~/.claude/settings.json      "$d/settings.json"
  cp ~/.claude/settings.local.json "$d/settings.local.json"
done

# verify all three are identical
md5 ~/.claude/settings.json ~/.claude-school/settings.json ~/.claude-work/settings.json
```

Then **restart the affected sessions.** Claude Code reads `statusLine` and
hook config once at startup — a running session will not pick up the change.

### Before overwriting, back up

`settings.json` accumulates per-instance runtime state. A blind copy discards it:

```bash
ts=$(date +%Y%m%d-%H%M%S)
mkdir -p ~/claude-config-backups/$ts
cp ~/.claude-school/settings.json ~/claude-config-backups/$ts/school-settings.json
cp ~/.claude-work/settings.json   ~/claude-config-backups/$ts/work-settings.json
```

Use a persistent path, not a session scratchpad — scratchpads are session-scoped
and vanish.

---

## Known Side Effects of Unification

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

Note this is only half a solution: `settings.local.json` is *also* on the copy
list, so a propagation run overwrites it too. If you want a per-instance
override to be truly durable, either exclude that file from the loop above or
re-apply the override after each propagation.

---

## Adding a Fourth Instance

```bash
NEW=~/.claude-newinstance
mkdir -p "$NEW"

# symlink the shared surface
for f in hooks agents commands skills plugins rules knowledge get-shit-done \
         gsd-file-manifest.json gsd-install-state.json \
         gsd-migration-journal .gsd-profile; do
  ln -s ~/.claude/"$f" "$NEW/$f"
done

# copy the mutable settings
cp ~/.claude/settings.json ~/.claude/settings.local.json "$NEW/"
```

Then add the alias with `CLAUDE_CONFIG_DIR` pointed at `$NEW`, and log in
separately. Do **not** copy any credential or session file into it.

---

## Troubleshooting

**Statusline not showing** — session predates the config change. Restart it.

**Hook not firing in school/work** — either the hook file isn't under a
symlinked dir, or its registration lives in `settings.json` and hasn't been
propagated. Check both.

**Wrong account in an instance** — something touched `.claude.json`,
`.credentials.json`, or the Keychain. Re-authenticate that instance only.

**Symlink got replaced by a real directory** — Claude Code or an installer
wrote through it. Check with `ls -la ~/.claude-work | grep -E 'hooks|plugins'`;
back up the real dir, delete it, recreate the symlink.
