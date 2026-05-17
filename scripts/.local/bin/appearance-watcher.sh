#!/usr/bin/env bash
# Watches macOS appearance and calls theme-switch.sh on changes.
# Run as a launchd agent — see ~/Library/LaunchAgents/com.user.appearance-watcher.plist

PREV=""

while true; do
  DARK=$(osascript -e 'tell application "System Events" to get dark mode of appearance preferences' 2>/dev/null)
  if [[ "$DARK" == "true" ]]; then
    CURRENT="Dark"
  else
    CURRENT="Light"
  fi
  if [[ "$CURRENT" != "$PREV" ]]; then
    PREV="$CURRENT"
    if [[ "$CURRENT" == "Dark" ]]; then
      "$HOME/.local/bin/theme-switch.sh" dark
    else
      "$HOME/.local/bin/theme-switch.sh" light
    fi
  fi
  sleep 1
done
