#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Toggle Reduced Motion
# @raycast.mode silent
# @raycast.packageName System
#
# Optional parameters:
# @raycast.icon 🎞️
# @raycast.packageName Viewport Controls
#
# Documentation:
# @raycast.description Toggles reduce motion mode for MacOS
# @raycast.author luke

current=$(defaults read com.apple.universalaccess reduceMotion 2>/dev/null || echo 0)
if [ "$current" = "1" ]; then
  defaults write com.apple.universalaccess reduceMotion -bool false
  osascript -e 'display notification "Reduce Motion: OFF" with title "Raycast"'
else
  defaults write com.apple.universalaccess reduceMotion -bool true
  osascript -e 'display notification "Reduce Motion: ON" with title "Raycast"'
fi
killall Dock
