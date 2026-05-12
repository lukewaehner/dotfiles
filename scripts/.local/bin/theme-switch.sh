#!/usr/bin/env bash
# ~/dotfiles/scripts/theme-switch.sh
#
# Usage:
#   theme-switch.sh dark    — switch everything to tokyonight night
#   theme-switch.sh light   — switch everything to tokyonight day
#   theme-switch.sh auto    — detect current macOS appearance and apply
#
# On Linux: call with "light" from your shell rc, or don't call it at all
# (tmux.conf defaults to night.conf, so just call with "light" once in .bashrc/.zshrc)
#
# On macOS: called automatically by the dark-notify launchd agent.
# The agent passes "dark" or "light" as $1.

TMUX_THEMES="$HOME/.config/tmux/themes"
LAZYGIT_THEMES="$HOME/.config/lazygit/themes"
STARSHIP_CONFIG="$HOME/.config/starship.toml"
NVIM_LISTEN_GLOB="/tmp/nvim*.sock"  # LazyVim default socket pattern

# ── Resolve mode ───────────────────────────────────────────────────────────────
MODE="${1:-auto}"

if [[ "$MODE" == "auto" ]]; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    APPEARANCE=$(defaults read -g AppleInterfaceStyle 2>/dev/null)
    if [[ "$APPEARANCE" == "Dark" ]]; then
      MODE="dark"
    else
      MODE="light"
    fi
  else
    # Linux: no auto detection, default to light
    MODE="light"
  fi
fi

# ── Apply tmux theme ───────────────────────────────────────────────────────────
apply_tmux() {
  local theme_file="$TMUX_THEMES/$1.conf"
  if [[ ! -f "$theme_file" ]]; then
    echo "theme-switch: missing $theme_file" >&2
    return 1
  fi
  # Update the symlink that tmux.conf sources
  ln -sf "$theme_file" "$TMUX_THEMES/current.conf"
  # Reload all running tmux sessions
  if tmux list-sessions &>/dev/null; then
    tmux source-file "$theme_file"
  fi
}

# ── Apply lazygit theme ────────────────────────────────────────────────────────
# Swaps themes/current.yml symlink (config.yml itself is a symlink to it).
# lazygit picks the new theme on next launch — no live reload mechanism.
apply_lazygit() {
  local theme_file="$LAZYGIT_THEMES/$1.yml"
  if [[ ! -f "$theme_file" ]]; then
    echo "theme-switch: missing $theme_file" >&2
    return 1
  fi
  ln -sf "$1.yml" "$LAZYGIT_THEMES/current.yml"
}

# ── Apply starship palette ─────────────────────────────────────────────────────
# starship 1.25 ignores STARSHIP_PALETTE env var; only the `palette = "..."` line
# in the config controls the active palette. So we edit it in place.
# Next prompt picks it up automatically — no reload needed.
apply_starship() {
  local palette="catppuccin_$1"  # mocha or latte
  [[ -f "$STARSHIP_CONFIG" ]] || return
  # Edit through the stow symlink: `sed -i` refuses symlinks on macOS, so
  # render to a temp file and pipe back through the symlink.
  local tmp
  tmp=$(mktemp) || return
  sed "s/^palette = .*/palette = \"$palette\"/" "$STARSHIP_CONFIG" > "$tmp" \
    && cat "$tmp" > "$STARSHIP_CONFIG"
  rm -f "$tmp"
}

# ── Apply Neovim theme ─────────────────────────────────────────────────────────
# Signals all running nvim instances via their unix sockets
apply_nvim() {
  local bg="$1"          # "dark" or "light"
  local style="$2"       # "night" or "day"
  for sock in $NVIM_LISTEN_GLOB; do
    [[ -S "$sock" ]] || continue
    nvim --server "$sock" --remote-send \
      "<Cmd>set background=${bg}<CR><Cmd>colorscheme tokyonight-${style}<CR>" \
      2>/dev/null
  done
}

# ── Dispatch ───────────────────────────────────────────────────────────────────
case "$MODE" in
  dark)
    apply_tmux "night"
    apply_lazygit "night"
    apply_starship "mocha"
    apply_nvim "dark" "night"
    ;;
  light)
    apply_tmux "day"
    apply_lazygit "day"
    apply_starship "latte"
    apply_nvim "light" "day"
    ;;
  *)
    echo "Usage: theme-switch.sh [dark|light|auto]" >&2
    exit 1
    ;;
esac
