#!/usr/bin/env bash
#
# Propagate shared Claude Code settings to every instance.
#
# settings.json is app-mutable — Claude Code rewrites it on /model, theme
# changes, and permission prompts — so it can't be symlinked like the rest of
# the config without one instance's runtime writes clobbering the others. It's
# the one part of the setup stow can't manage.
#
# So: the shared keys live in a tracked template, and this script merges them
# into each instance without touching per-instance keys. That's the difference
# from a plain `cp`, which silently reset model, theme, and effortLevel on
# every run.
#
#   sync-claude-settings.sh           report drift, change nothing (exit 1 if drift)
#   sync-claude-settings.sh --apply   back up, then merge the template in
#
# Never reads or writes .claude.json, .credentials.json, history.jsonl,
# projects/, or sessions/ — login isolation between instances depends on those
# staying untouched.

set -euo pipefail

DOTFILES="${DOTFILES:-$HOME/Repos/dotfiles}"
TEMPLATE="${CLAUDE_SETTINGS_TEMPLATE:-$DOTFILES/claude/.claude/settings.template.json}"
BACKUP_ROOT="${CLAUDE_BACKUP_ROOT:-$HOME/claude-config-backups}"

# Space-separated override, so a fourth instance needs no edit here — and so
# this is testable against fixtures instead of the live config.
if [[ -n "${CLAUDE_INSTANCES:-}" ]]; then
  read -ra INSTANCES <<< "$CLAUDE_INSTANCES"
else
  INSTANCES=("$HOME/.claude" "$HOME/.claude-school" "$HOME/.claude-work")
fi

APPLY=false
[[ "${1:-}" == "--apply" ]] && APPLY=true

command -v jq >/dev/null || { echo "error: jq not found" >&2; exit 2; }
[[ -f "$TEMPLATE" ]] || { echo "error: template not found: $TEMPLATE" >&2; exit 2; }
jq -e . "$TEMPLATE" >/dev/null || { echo "error: template is not valid JSON" >&2; exit 2; }

# The instance projected down to just the template's top-level keys. Anything
# else the instance holds is per-instance state and is deliberately invisible
# to this comparison.
shared_view() {
  jq -S --slurpfile t "$TEMPLATE" \
    'with_entries(select(.key | IN($t[0] | keys[])))' "$1"
}

drift=0       # shared keys differ from the template
unresolved=0  # --apply cannot fix this one; never report success over it
for dir in "${INSTANCES[@]}"; do
  name="$(basename "$dir")"
  settings="$dir/settings.json"

  [[ -d "$dir" ]]      || { echo "skip     $name (no such instance)"; continue; }
  [[ -f "$settings" ]] || { echo "MISSING  $name has no settings.json"; drift=1; unresolved=1; continue; }

  if ! jq -e . "$settings" >/dev/null 2>&1; then
    echo "INVALID  $name settings.json is not valid JSON — not touching it"
    drift=1
    unresolved=1
    continue
  fi

  if diff -q <(shared_view "$settings") <(jq -S . "$TEMPLATE") >/dev/null; then
    echo "ok       $name"
    continue
  fi

  drift=1
  echo "DRIFT    $name"
  diff <(shared_view "$settings") <(jq -S . "$TEMPLATE") \
    | sed 's/^/           /' || true

  if $APPLY; then
    stamp="$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$BACKUP_ROOT/$stamp"
    cp "$settings" "$BACKUP_ROOT/$stamp/$name-settings.json"

    # Template wins on shared keys; every other key the instance holds
    # survives untouched. Write to a temp file so a jq failure can't leave a
    # truncated settings.json behind.
    tmp="$(mktemp)"
    jq -S --slurpfile t "$TEMPLATE" '. * $t[0]' "$settings" > "$tmp"
    jq -e . "$tmp" >/dev/null || { echo "error: merge produced invalid JSON" >&2; rm -f "$tmp"; exit 3; }
    mv "$tmp" "$settings"

    echo "           applied (backup: $BACKUP_ROOT/$stamp/$name-settings.json)"
  fi
done

if $APPLY; then
  echo
  if (( unresolved )); then
    echo "Finished with unrepaired instances above — fix those by hand."
    exit 1
  fi
  echo "Restart affected sessions — hooks and statusLine are read once at startup."
  exit 0
fi

if (( drift )); then
  echo
  echo "Run with --apply to merge the template in."
  exit 1
fi
