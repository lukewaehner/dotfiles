#!/usr/bin/env bash
# setup-linux.sh — install tmux dotfiles on a Linux dev server
#
# Usage:
#   bash setup-linux.sh [night|day]   — install (default: night)
#   bash setup-linux.sh --uninstall   — remove installed files with confirmation
#
set -euo pipefail

info()  { echo "[setup] $*"; }
ok()    { echo "[setup] ✓ $*"; }
warn()  { echo "[setup] ! $*"; }

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Confirmation helper ────────────────────────────────────────────────────────
# confirm_remove <label> <path>
# Returns 0 if user confirmed, 1 if skipped.
confirm_remove() {
  local label="$1"
  local path="$2"
  if [[ ! -e "$path" ]]; then
    info "  $label not found at $path — skipping"
    return 1
  fi
  printf "[setup] Confirm: remove %s at %s? [y/N] " "$label" "$path"
  read -r answer </dev/tty
  if [[ "$answer" =~ ^[Yy]$ ]]; then
    return 0
  else
    info "  Skipped $label"
    return 1
  fi
}

# ── Uninstall ──────────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--uninstall" ]]; then
  info "Uninstalling dotfiles from this machine..."
  echo ""

  if confirm_remove "tmux.conf"    "$HOME/.config/tmux/tmux.conf";            then rm -f "$HOME/.config/tmux/tmux.conf";            ok "Removed tmux.conf"; fi
  if confirm_remove "night.conf"   "$HOME/.config/tmux/themes/night.conf";    then rm -f "$HOME/.config/tmux/themes/night.conf";    ok "Removed night.conf"; fi
  if confirm_remove "day.conf"     "$HOME/.config/tmux/themes/day.conf";      then rm -f "$HOME/.config/tmux/themes/day.conf";      ok "Removed day.conf"; fi
  if confirm_remove "current.conf" "$HOME/.config/tmux/themes/current.conf";  then rm -f "$HOME/.config/tmux/themes/current.conf";  ok "Removed current.conf"; fi
  if confirm_remove "theme-switch" "$HOME/.local/bin/theme-switch";           then rm -f "$HOME/.local/bin/theme-switch";           ok "Removed theme-switch"; fi

  echo ""
  info "Uninstall complete."
  exit 0
fi

# ── Install ────────────────────────────────────────────────────────────────────
DEFAULT_THEME="${1:-night}"
if [[ "$DEFAULT_THEME" != "night" && "$DEFAULT_THEME" != "day" ]]; then
  echo "Usage: bash setup-linux.sh [night|day|--uninstall]" >&2
  exit 1
fi

# ── 1. tmux config files ───────────────────────────────────────────────────────
# tmux reads its config from ~/.config/tmux/tmux.conf.
# The themes directory holds the color definitions; current.conf is the symlink
# that tmux.conf sources to apply whichever theme is active.
info "Installing tmux config..."
mkdir -p "$HOME/.config/tmux/themes"

cp "$DOTFILES_DIR/tmux/.config/tmux/tmux.conf"         "$HOME/.config/tmux/tmux.conf"
cp "$DOTFILES_DIR/tmux/.config/tmux/themes/night.conf" "$HOME/.config/tmux/themes/night.conf"
cp "$DOTFILES_DIR/tmux/.config/tmux/themes/day.conf"   "$HOME/.config/tmux/themes/day.conf"
ok "tmux config → ~/.config/tmux/"

# ── 2. current.conf symlink ────────────────────────────────────────────────────
# tmux.conf sources current.conf rather than a hard-coded theme file.
# The symlink is what lets theme-switch change the active theme at runtime
# without touching tmux.conf itself.
if [[ "$DEFAULT_THEME" == "night" ]]; then
  ln -sf "$HOME/.config/tmux/themes/night.conf" "$HOME/.config/tmux/themes/current.conf"
else
  ln -sf "$HOME/.config/tmux/themes/day.conf"   "$HOME/.config/tmux/themes/current.conf"
fi
ok "current.conf → $DEFAULT_THEME theme"

# ── 3. theme-switch command ────────────────────────────────────────────────────
# Installs the manual toggle to ~/.local/bin/theme-switch so it is callable
# by name from the terminal. Accepts: dark | light | auto.
mkdir -p "$HOME/.local/bin"
cp "$DOTFILES_DIR/tmux/.config/tmux/theme-switch.sh" "$HOME/.local/bin/theme-switch"
chmod +x "$HOME/.local/bin/theme-switch"
ok "theme-switch → ~/.local/bin/theme-switch"

# ── 4. Reload tmux if running ─────────────────────────────────────────────────
# Applies the new config to any open tmux sessions immediately.
if tmux list-sessions &>/dev/null 2>&1; then
  tmux source-file "$HOME/.config/tmux/tmux.conf" 2>/dev/null && ok "tmux config reloaded" || warn "tmux reload failed (non-fatal)"
fi

echo ""
ok "Done. Default theme: $DEFAULT_THEME"
echo ""
echo "  Toggle theme:  theme-switch dark"
echo "                 theme-switch light"
echo ""
