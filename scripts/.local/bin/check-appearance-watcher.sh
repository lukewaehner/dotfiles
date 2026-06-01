#!/usr/bin/env bash
# Watchdog for com.user.appearance-watcher launchd agent.
# Sends a macOS notification and attempts a restart if the agent is down.
# Intended to be called from crontab every few minutes.

LABEL="com.user.appearance-watcher"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

notify() {
  osascript -e "display notification \"$1\" with title \"Dotfiles\" subtitle \"Appearance Watcher\" sound name \"Basso\"" 2>/dev/null
}

line=$(launchctl list 2>/dev/null | grep "$LABEL")

if [[ -z "$line" ]]; then
  notify "Service not loaded — attempting reload"
  launchctl load "$PLIST" 2>/dev/null
  exit 1
fi

pid=$(awk '{print $1}' <<< "$line")
exit_code=$(awk '{print $2}' <<< "$line")

if [[ "$pid" == "-" ]]; then
  notify "Watcher crashed (exit $exit_code) — restarting"
  launchctl unload "$PLIST" 2>/dev/null
  launchctl load "$PLIST" 2>/dev/null
  exit 1
fi
