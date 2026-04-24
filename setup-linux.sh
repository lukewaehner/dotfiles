#!/usr/bin/env bash
# setup-linux.sh — install dotfiles config on a Linux dev server (no stow needed)
# Run from the dotfiles repo root: bash setup-linux.sh
set -euo pipefail

info()  { echo "[setup] $*"; }
ok()    { echo "[setup] ✓ $*"; }
warn()  { echo "[setup] ! $*"; }

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── 1. tmux config ────────────────────────────────────────────────────────────
info "Installing tmux config..."
mkdir -p "$HOME/.config/tmux/themes"
cp "$DOTFILES_DIR/tmux/.config/tmux/tmux.conf"         "$HOME/.config/tmux/tmux.conf"
cp "$DOTFILES_DIR/tmux/.config/tmux/theme-switch.sh"   "$HOME/.config/tmux/theme-switch.sh"
cp "$DOTFILES_DIR/tmux/.config/tmux/themes/night.conf" "$HOME/.config/tmux/themes/night.conf"
cp "$DOTFILES_DIR/tmux/.config/tmux/themes/day.conf"   "$HOME/.config/tmux/themes/day.conf"
chmod +x "$HOME/.config/tmux/theme-switch.sh"
ok "tmux config → ~/.config/tmux/"

# Create the current.conf symlink (default: night)
DEFAULT_THEME="${1:-night}"
if [[ "$DEFAULT_THEME" == "night" ]]; then
  SWITCH_ARG="dark"
else
  SWITCH_ARG="light"
fi
"$HOME/.config/tmux/theme-switch.sh" "$SWITCH_ARG"
ok "current.conf symlink → $DEFAULT_THEME theme"

# ── 2. nvim config (optional) ─────────────────────────────────────────────────
if command -v nvim &>/dev/null; then
  info "nvim found — installing nvim config..."
  mkdir -p "$HOME/.config/nvim"
  cp -r "$DOTFILES_DIR/nvim/.config/nvim/." "$HOME/.config/nvim/"
  ok "nvim config → ~/.config/nvim/"
  warn "Run :Lazy sync inside nvim to install plugins"
else
  info "nvim not found — skipping"
fi

# ── 3. Shell rc snippet ───────────────────────────────────────────────────────
RC_FILE=""
if [[ -f "$HOME/.zshrc" ]]; then
  RC_FILE="$HOME/.zshrc"
elif [[ -f "$HOME/.bashrc" ]]; then
  RC_FILE="$HOME/.bashrc"
fi

if [[ -n "$RC_FILE" ]]; then
  if grep -q "theme-switch.sh" "$RC_FILE" 2>/dev/null; then
    info "theme-switch already in $RC_FILE — skipping"
  else
    printf '\n# tmux tokyonight — apply theme on new shell sessions\n' >> "$RC_FILE"
    printf '"%s/.config/tmux/theme-switch.sh" %s\n' "$HOME" "$SWITCH_ARG" >> "$RC_FILE"
    ok "Shell snippet appended to $RC_FILE"
  fi
else
  warn "No .zshrc or .bashrc found — add this line manually:"
  echo "  \"\$HOME/.config/tmux/theme-switch.sh\" $SWITCH_ARG"
fi

# ── 4. Reload tmux if running ─────────────────────────────────────────────────
if tmux list-sessions &>/dev/null 2>&1; then
  tmux source-file "$HOME/.config/tmux/tmux.conf" 2>/dev/null && ok "tmux config reloaded" || true
fi

echo ""
echo "Done. Default theme: $DEFAULT_THEME"
echo "Usage: bash setup-linux.sh [night|day]"
