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

# ── 0. Install system packages ─────────────────────────────────────────────────
# Debian/Ubuntu ships fd as fdfind and bat as batcat — check for either binary.
pkg_installed() {
  case "$1" in
    ripgrep) command -v rg      &>/dev/null ;;
    fd-find) command -v fdfind  &>/dev/null || command -v fd  &>/dev/null ;;
    bat)     command -v batcat  &>/dev/null || command -v bat &>/dev/null ;;
    *)       command -v "$1"    &>/dev/null ;;
  esac
}

PACKAGES=(tmux ncdu htop curl git unzip ripgrep fd-find fzf bat tree)
MISSING=()
for pkg in "${PACKAGES[@]}"; do
  pkg_installed "$pkg" || MISSING+=("$pkg")
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
  if ! command -v apt-get &>/dev/null; then
    echo "Error: apt-get not found. Install these packages manually:" >&2
    printf "  %s\n" "${MISSING[@]}" >&2
    exit 1
  fi
  info "Installing: ${MISSING[*]}"
  sudo apt-get update -qq
  sudo apt-get install -y "${MISSING[@]}"
fi
ok "System packages ready"

# Add ~/.local/bin shims so fd and bat work by their canonical names.
mkdir -p "$HOME/.local/bin"
if command -v fdfind &>/dev/null && ! command -v fd &>/dev/null; then
  ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd"
  ok "fd → fdfind shim added to ~/.local/bin"
fi
if command -v batcat &>/dev/null && ! command -v bat &>/dev/null; then
  ln -sf "$(command -v batcat)" "$HOME/.local/bin/bat"
  ok "bat → batcat shim added to ~/.local/bin"
fi

# ── expand_theme <src> <dst> ───────────────────────────────────────────────────
# Theme files use VAR="value" / ${VAR} syntax added in tmux 3.4.
# This reads those assignments and inlines the values via sed, so the installed
# file works on any tmux version without requiring 3.4+.
expand_theme() {
  local src="$1" dst="$2"
  local sed_args=() line key val
  while IFS= read -r line; do
    if [[ "$line" =~ ^([A-Z_]+)=\"([^\"]*)\"$ ]]; then
      key="${BASH_REMATCH[1]}"
      val="${BASH_REMATCH[2]}"
      sed_args+=(-e "s/\${${key}}/${val}/g")
    fi
  done < "$src"
  if [[ ${#sed_args[@]} -gt 0 ]]; then
    sed "${sed_args[@]}" "$src" > "$dst"
  else
    cp "$src" "$dst"
  fi
}

# ── 1. tmux config files ───────────────────────────────────────────────────────
# tmux reads its config from ~/.config/tmux/tmux.conf.
# The themes directory holds the color definitions; current.conf is the symlink
# that tmux.conf sources to apply whichever theme is active.
info "Installing tmux config..."
mkdir -p "$HOME/.config/tmux/themes"

if [[ -f "$HOME/.config/tmux/tmux.conf" ]]; then
  cp "$HOME/.config/tmux/tmux.conf" "$HOME/.config/tmux/tmux.conf.bak"
  warn "Existing tmux.conf backed up → ~/.config/tmux/tmux.conf.bak"
fi

cp           "$DOTFILES_DIR/tmux/.config/tmux/tmux.conf"         "$HOME/.config/tmux/tmux.conf"
expand_theme "$DOTFILES_DIR/tmux/.config/tmux/themes/night.conf" "$HOME/.config/tmux/themes/night.conf"
expand_theme "$DOTFILES_DIR/tmux/.config/tmux/themes/day.conf"   "$HOME/.config/tmux/themes/day.conf"
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
if tmux list-sessions &>/dev/null; then
  tmux source-file "$HOME/.config/tmux/tmux.conf" 2>/dev/null && ok "tmux config reloaded" || warn "tmux reload failed (non-fatal)"
fi

# ── 5. PATH check ──────────────────────────────────────────────────────────────
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo ""
  warn "~/.local/bin is not in your PATH — theme-switch won't be found by name."
  warn "Add this to your ~/.bashrc or ~/.zshrc:"
  warn "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
ok "Done. Default theme: $DEFAULT_THEME"
echo ""
echo "  Toggle theme:  theme-switch dark"
echo "                 theme-switch light"
echo ""
