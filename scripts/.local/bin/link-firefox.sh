#!/usr/bin/env bash
#
# Link the tracked Firefox chrome config into the active Firefox profile.
#
# firefox/ is not a stow package. Stow mirrors a package's tree into $HOME,
# but the profile directory it would need to write into is named randomly
# (e.g. m8zz0fwi.default-release), so there is no fixed path to mirror. This
# script reads the default profile out of profiles.ini and symlinks into it.
#
#   link-firefox.sh           link into the default profile
#   link-firefox.sh --dry-run show what would change, touch nothing
#
# Idempotent: re-running relinks cleanly. Anything real (not already our
# symlink) sitting at a target path is moved aside, never deleted.
#
# Firefox reads userChrome.css and user.js only at startup -- restart it
# after running this.

set -euo pipefail

DOTFILES="${DOTFILES:-$HOME/Repos/dotfiles}"
SRC="$DOTFILES/firefox"
FF_ROOT="${FIREFOX_ROOT:-$HOME/Library/Application Support/Firefox}"

dry_run=false
[[ "${1:-}" == "--dry-run" ]] && dry_run=true

log()  { printf '  %s\n' "$*"; }
die()  { printf 'error: %s\n' "$*" >&2; exit 1; }

[[ -d "$SRC/chrome" ]] || die "not found: $SRC/chrome"
[[ -f "$SRC/user.js" ]] || die "not found: $SRC/user.js"
[[ -f "$SRC/chrome/onebar/onebar.css" ]] ||
  die "onebar submodule is empty -- run: git -C '$DOTFILES' submodule update --init"

ini="$FF_ROOT/profiles.ini"
[[ -f "$ini" ]] || die "no profiles.ini at $ini"

# profiles.ini lists every profile; the [Install*] section names the default.
rel=$(awk -F= '/^\[Install/ { in_install = 1; next }
                /^\[/       { in_install = 0 }
                in_install && /^Default=/ { print $2; exit }' "$ini")
[[ -n "$rel" ]] || die "no Default= under any [Install...] section in $ini"

profile="$FF_ROOT/$rel"
[[ -d "$profile" ]] || die "profile directory not found: $profile"

echo "profile: $profile"

link() {
  local src="$1" dest="$2"

  if [[ -L "$dest" && "$(readlink "$dest")" == "$src" ]]; then
    log "ok        $(basename "$dest") -> already linked"
    return 0
  fi

  if [[ -L "$dest" ]]; then
    $dry_run && { log "relink    $(basename "$dest") (points elsewhere)"; return 0; }
    rm "$dest"
  elif [[ -e "$dest" ]]; then
    # Real file or directory -- preserve it instead of clobbering.
    local aside="$dest.pre-link.$(date +%Y%m%d-%H%M%S)"
    $dry_run && { log "move+link $(basename "$dest") (real file -> $(basename "$aside"))"; return 0; }
    mv "$dest" "$aside"
    log "moved     $(basename "$dest") -> $(basename "$aside")"
  else
    $dry_run && { log "link      $(basename "$dest")"; return 0; }
  fi

  ln -s "$src" "$dest"
  log "linked    $(basename "$dest")"
}

link "$SRC/chrome"   "$profile/chrome"
link "$SRC/user.js"  "$profile/user.js"

$dry_run && { echo "(dry run -- nothing changed)"; exit 0; }
echo "done -- restart Firefox to pick up the changes"
