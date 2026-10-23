#!/bin/sh
# Status line: "[instance] model dir".
#
# The instance (personal/work/school) comes from CLAUDE_CONFIG_DIR, the same
# variable claude-auto sets; unset means the personal account. Claude Code
# passes session info as JSON on stdin.

set -eu

case ${CLAUDE_CONFIG_DIR:-} in
  "") instance=personal ;;
  *) instance=$(basename "$CLAUDE_CONFIG_DIR"); instance=${instance#.claude-} ;;
esac

input=$(cat)
model=$(printf '%s' "$input" | jq -r '.model.display_name // "claude"')
dir=$(printf '%s' "$input" | jq -r '.workspace.current_dir // .cwd // ""')

printf '\033[2m[%s]\033[0m %s \033[2m%s\033[0m' "$instance" "$model" "$(basename "$dir")"
