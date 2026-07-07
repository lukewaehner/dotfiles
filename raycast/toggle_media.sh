#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Toggle Media
# @raycast.mode silent
#
# Optional parameters:
# @raycast.icon ⏯️
# @raycast.packageName Media Controls
#
# Documentation:
# @raycast.description Toggles play/pause for whatever media is currently active
# @raycast.author luke

/opt/homebrew/bin/nowplaying-cli togglePlayPause
