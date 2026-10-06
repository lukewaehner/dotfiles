#!/usr/bin/env bash
# macOS notification + sound when a Claude Code agent finishes or needs me.
# Wired as a Stop and Notification hook in claude/.claude/settings.template.json,
# next to the workmux set-window-status calls that drive the D/Q tab markers.
# Fires even when the window is focused, since I may have walked away from it.
#
# Reads the hook payload on stdin; titles the notification with the worktree
# directory name so parallel agents can be told apart.

set -uo pipefail

payload=$(cat)
event=$(jq -r '.hook_event_name // empty' <<< "$payload")
project=$(basename "$(jq -r '.cwd // empty' <<< "$payload")")

case "$event" in
  Stop)
    message="Done"
    sound="Glass"
    ;;
  Notification)
    message=$(jq -r '.message // "Waiting for input"' <<< "$payload")
    sound="Ping"
    ;;
  *)
    echo "agent-notify: unexpected hook event '${event}'" >&2
    exit 1
    ;;
esac

# Text goes in through argv, not interpolated into the script, so quotes in a
# prompt message can't break (or inject into) the AppleScript.
osascript \
  -e 'on run argv' \
  -e 'display notification (item 2 of argv) with title (item 1 of argv) sound name (item 3 of argv)' \
  -e 'end run' \
  "Claude · ${project:-agent}" "$message" "$sound"
