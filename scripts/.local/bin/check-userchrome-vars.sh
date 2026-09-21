#!/usr/bin/env bash
#
# Report CSS custom properties that userChrome.css (and the vendored
# onebar) reference but the installed Firefox no longer defines.
#
# Firefox renames these tokens without notice, and the failure is silent:
# a var() that resolves to nothing makes the whole declaration invalid at
# computed-value time, so the property falls back to its initial value
# instead of erroring. Three tokens had already gone stale before anyone
# noticed (--urlbar-min-height, --tab-block-margin, and friends).
#
# Also flags `display: -moz-box`, which Firefox removed entirely — any
# remaining use is dead.
#
#   check-userchrome-vars.sh [chrome-dir]
#
# Defaults to the tracked config. Exits 1 only for stale tokens in files
# we own, so it can gate a commit or run after a Firefox update. Drift in
# vendored onebar/ is reported but does not fail: upstream lags Firefox
# and we are not going to patch its copy.

set -euo pipefail

DOTFILES="${DOTFILES:-$HOME/Repos/dotfiles}"
chrome="${1:-$DOTFILES/firefox/chrome}"
res="${FIREFOX_RESOURCES:-/Applications/Firefox.app/Contents/Resources}"

die() { printf 'error: %s\n' "$*" >&2; exit 2; }

[[ -d "$chrome" ]] || die "chrome dir not found: $chrome"
[[ -d "$res" ]]    || die "Firefox resources not found: $res"

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

# Firefox splits its CSS across two archives depending on the build.
unzip -qo "$res/browser/omni.ja" '*.css' -d "$work/ff" 2>/dev/null || true
unzip -qo "$res/omni.ja"         '*.css' -d "$work/ff" 2>/dev/null || true
[[ -d "$work/ff" ]] || die "no CSS extracted from omni.ja under $res"

version=$(defaults read "$res/../Info.plist" CFBundleShortVersionString 2>/dev/null || echo "unknown")
echo "Firefox $version — $(find "$work/ff" -name '*.css' | wc -l | tr -d ' ') stylesheets"
echo

# "Defined" is Firefox's tokens plus any the config declares itself.
grep -rhoE -- '--[A-Za-z0-9_-]+[[:space:]]*:' "$work/ff" "$chrome" \
  | sed 's/[[:space:]]*:$//' | sort -u > "$work/defined"

status=0

while IFS= read -r f; do
  stale=$(grep -oE 'var\(--[A-Za-z0-9_-]+' "$f" | sed 's/var(//' | sort -u \
            | comm -23 - "$work/defined")
  rel="${f#"$chrome"/}"

  if [[ -z "$stale" ]]; then
    echo "ok       $rel"
    continue
  fi

  # Vendored code: report, do not gate.
  if [[ "$rel" == onebar/* ]]; then
    echo "upstream $rel (onebar lags Firefox; informational)"
  else
    echo "STALE    $rel"
    status=1
  fi
  printf '           %s\n' $stale
done < <(find "$chrome" -name '*.css' -not -path '*/.git/*' | sort)

# -moz-box was removed as a display value; Firefox's own CSS has zero uses.
if dead=$(grep -rnE 'display:[[:space:]]*-moz-box\b' "$chrome" --include='*.css'); then
  echo
  echo "DEAD     display: -moz-box (removed from Firefox)"
  printf '           %s\n' "$dead"
  status=1
fi

echo
if (( status == 0 )); then
  echo "No stale tokens in files we own."
else
  echo "Stale references above resolve to nothing and silently drop their declaration."
fi
exit "$status"
