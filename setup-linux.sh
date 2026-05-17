#!/usr/bin/env bash
# setup-linux.sh — bootstrap a Linux dev environment from dotfiles
#
# Usage:
#   bash setup-linux.sh [night|day]   — install (default: night)
#   bash setup-linux.sh --uninstall   — remove installed files with confirmation
#
# Safe to run multiple times — all steps are idempotent.
#
# If invoked via `sh setup-linux.sh`, re-exec under bash automatically.
if [ -z "$BASH_VERSION" ]; then
  exec bash "$0" "$@"
fi
set -euo pipefail

info()  { echo "[setup] $*"; }
ok()    { echo "[setup] ✓ $*"; }
warn()  { echo "[setup] ! $*"; }

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Confirmation helper ────────────────────────────────────────────────────────
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

  if command -v stow &>/dev/null; then
    info "Removing stowed dotfile symlinks..."
    stow --dir="$DOTFILES_DIR" -t "$HOME" --delete atuin bat eza git lazygit nvim starship zsh 2>/dev/null || true
    ok "Stow symlinks removed"
  fi

  if grep -qF "# ── dotfiles ──" "$HOME/.bashrc" 2>/dev/null; then
    info "Removing dotfiles block from ~/.bashrc..."
    sed -i '/# ── dotfiles ──/,/# ── end dotfiles ──/d' "$HOME/.bashrc"
    ok "~/.bashrc block removed"
  fi

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

# ── 0. System packages ─────────────────────────────────────────────────────────
# Debian/Ubuntu ships fd as fdfind and bat as batcat — check for either binary.
pkg_installed() {
  case "$1" in
    ripgrep) command -v rg      &>/dev/null ;;
    fd-find) command -v fdfind  &>/dev/null || command -v fd  &>/dev/null ;;
    bat)     command -v batcat  &>/dev/null || command -v bat &>/dev/null ;;
    *)       command -v "$1"    &>/dev/null ;;
  esac
}

PACKAGES=(tmux ncdu htop curl git unzip ripgrep fd-find fzf bat tree stow direnv jq snapd)
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

# ── 0a. GitHub CLI ─────────────────────────────────────────────────────────────
if ! command -v gh &>/dev/null; then
  info "Installing GitHub CLI..."
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  sudo apt-get update -qq
  sudo apt-get install -y gh
  ok "GitHub CLI installed"
else
  ok "GitHub CLI already installed"
fi

# ── 0b. ~/.local/bin shims ─────────────────────────────────────────────────────
# Debian/Ubuntu names differ — add shims so tools work by canonical name.
mkdir -p "$HOME/.local/bin"
if command -v fdfind &>/dev/null && ! command -v fd &>/dev/null; then
  ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd"
  ok "fd → fdfind shim added to ~/.local/bin"
fi
if command -v batcat &>/dev/null && ! command -v bat &>/dev/null; then
  ln -sf "$(command -v batcat)" "$HOME/.local/bin/bat"
  ok "bat → batcat shim added to ~/.local/bin"
fi

# ── 1. Neovim ─────────────────────────────────────────────────────────────────
if ! command -v nvim &>/dev/null; then
  info "Installing neovim via snap..."
  sudo snap install nvim --classic
  ok "neovim installed"
else
  ok "neovim already installed"
fi

# ── 2. Curl-installed tools ────────────────────────────────────────────────────
if ! command -v starship &>/dev/null; then
  info "Installing starship..."
  curl -fsSL https://starship.rs/install.sh | sh -s -- --yes
  ok "starship installed"
else
  ok "starship already installed"
fi

if ! command -v atuin &>/dev/null; then
  info "Installing atuin..."
  curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
  ok "atuin installed"
else
  ok "atuin already installed"
fi

if ! command -v zoxide &>/dev/null; then
  info "Installing zoxide..."
  curl -fsSL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
  ok "zoxide installed"
else
  ok "zoxide already installed"
fi

# ── 3. Binary tools ────────────────────────────────────────────────────────────
# eza — prefer apt (available Ubuntu 24+), fallback to GitHub release
if ! command -v eza &>/dev/null; then
  if apt-cache show eza &>/dev/null 2>&1; then
    info "Installing eza via apt..."
    sudo apt-get install -y eza
  else
    info "Installing eza from GitHub release..."
    EZA_VER=$(curl -fsSL https://api.github.com/repos/eza-community/eza/releases/latest \
      | grep '"tag_name"' | cut -d'"' -f4)
    curl -fsSL "https://github.com/eza-community/eza/releases/download/${EZA_VER}/eza_x86_64-unknown-linux-gnu.tar.gz" \
      | tar -xz -C "$HOME/.local/bin" eza
  fi
  ok "eza installed"
else
  ok "eza already installed"
fi

# lazygit — not in apt, always from GitHub release
if ! command -v lazygit &>/dev/null; then
  info "Installing lazygit from GitHub release..."
  LG_VER=$(curl -fsSL https://api.github.com/repos/jesseduffield/lazygit/releases/latest \
    | grep '"tag_name"' | cut -d'"' -f4 | sed 's/^v//')
  curl -fsSL "https://github.com/jesseduffield/lazygit/releases/download/v${LG_VER}/lazygit_${LG_VER}_Linux_x86_64.tar.gz" \
    | tar -xz -C "$HOME/.local/bin" lazygit
  ok "lazygit installed"
else
  ok "lazygit already installed"
fi

# ── 3b. Node.js & Claude Code ─────────────────────────────────────────────────
# Node via NodeSource; npm globals go to ~/.npm-global to avoid sudo.
if ! command -v node &>/dev/null; then
  info "Installing Node.js 22 via NodeSource..."
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt-get install -y nodejs
  ok "Node.js installed"
else
  ok "Node.js already installed ($(node --version))"
fi

if [[ ! -d "$HOME/.npm-global" ]]; then
  mkdir -p "$HOME/.npm-global"
  npm config set prefix "$HOME/.npm-global"
fi

if ! command -v claude &>/dev/null && [[ ! -x "$HOME/.npm-global/bin/claude" ]]; then
  info "Installing Claude Code..."
  npm install -g @anthropic-ai/claude-code
  ok "Claude Code installed"
else
  ok "Claude Code already installed"
fi

# ── 4. Stow dotfile modules ────────────────────────────────────────────────────
# tmux is handled manually below (needs expand_theme).
# ghostty/macos/scripts are macOS-only. brew has no dotfile structure.
info "Stowing dotfile modules..."
mkdir -p "$HOME/.config"
stow --dir="$DOTFILES_DIR" -t "$HOME" --restow atuin bat eza git lazygit nvim starship zsh \
  || warn "Some stow modules had conflicts — run 'stow --adopt' manually to resolve"
ok "Dotfiles stowed → $HOME"

# Rebuild bat theme cache so custom themes are available
if command -v bat &>/dev/null; then
  bat cache --build &>/dev/null && ok "bat theme cache rebuilt"
elif command -v batcat &>/dev/null; then
  batcat cache --build &>/dev/null && ok "bat theme cache rebuilt"
fi

# ── 5. ~/.bashrc wiring ────────────────────────────────────────────────────────
BASHRC="$HOME/.bashrc"
if ! grep -qF "# ── dotfiles ──" "$BASHRC" 2>/dev/null; then
  info "Appending dotfiles block to ~/.bashrc..."
  cat >> "$BASHRC" << 'BASHRC_BLOCK'

# ── dotfiles ──────────────────────────────────────────────────────────────────
# PATH
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$HOME/.npm-global/bin:$PATH"
[[ -d "$HOME/.pyenv" ]] && export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:$PATH"
[[ -d "$HOME/.rbenv" ]] && export PATH="$HOME/.rbenv/shims:$HOME/.rbenv/bin:$PATH"

export MANPAGER="nvim +Man!"
export BAT_THEME="TokyoNight Night"
export STARSHIP_PALETTE="catppuccin_mocha"
export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_DEFAULT_OPTS='--color=fg+:7,bg:-1,hl:4,hl+:4,info:6,prompt:5,spinner:5,pointer:5,marker:2,header:6'

# bash-completion
[[ -f /usr/share/bash-completion/bash_completion ]] && \
  source /usr/share/bash-completion/bash_completion

# Aliases
alias ls="eza --icons --group-directories-first"
alias ll="eza -lgh --icons --git --group-directories-first"
alias lt="eza --tree --level=2 --icons"
alias lg="lazygit"
alias cd="z"
alias t='tmux new-session -A -s main'

# Functions
fp() {
  fzf --preview 'bat --style=numbers --color=always --line-range :500 {}'
}
cdd() {
  local dir
  dir=$(fd -t d | fzf) || return
  builtin cd "$dir"
}
cdf() {
  local file
  file=$(find . -type f 2>/dev/null | fzf) || return
  builtin cd "$(dirname "$file")"
}

# Lazy rbenv — defer init until first use (~80ms saved per shell)
if command -v rbenv &>/dev/null; then
  _lazy_rbenv() {
    unset -f ruby gem bundle rails rake rbenv
    eval "$(rbenv init - bash)"
    "$@"
  }
  for _cmd in ruby gem bundle rails rake rbenv; do
    eval "${_cmd}() { _lazy_rbenv ${_cmd} \"\$@\"; }"
  done
  unset _cmd
fi

# Cached tool inits — same pattern as macOS .zshrc zcache
mkdir -p "$HOME/.cache/bash"
_dotcache() {
  local name="$1" cache="$HOME/.cache/bash/$1.bash"
  if [[ ! -f "$cache" ]]; then
    case "$name" in
      zoxide)   zoxide init bash > "$cache" ;;
      atuin)    atuin init bash --disable-up-arrow > "$cache" ;;
      starship) starship init bash > "$cache" ;;
    esac
  fi
  [[ -f "$cache" ]] && source "$cache"
}
_dotcache zoxide
_dotcache atuin

# fzf keybindings
[[ -f /usr/share/doc/fzf/examples/key-bindings.bash ]] && \
  source /usr/share/doc/fzf/examples/key-bindings.bash

# Starship prompt (load last)
_dotcache starship

# theme-switch on login (Linux always uses dark)
"$HOME/.local/bin/theme-switch" dark
# ── end dotfiles ──────────────────────────────────────────────────────────────
BASHRC_BLOCK
  ok "~/.bashrc updated"
else
  ok "~/.bashrc already contains dotfiles block — skipping"
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

# ── 6. tmux config ────────────────────────────────────────────────────────────
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

# ── 7. current.conf symlink ───────────────────────────────────────────────────
# tmux.conf sources current.conf rather than a hard-coded theme file.
if [[ "$DEFAULT_THEME" == "night" ]]; then
  ln -sf "$HOME/.config/tmux/themes/night.conf" "$HOME/.config/tmux/themes/current.conf"
else
  ln -sf "$HOME/.config/tmux/themes/day.conf"   "$HOME/.config/tmux/themes/current.conf"
fi
ok "current.conf → $DEFAULT_THEME theme"

# ── 8. theme-switch command ───────────────────────────────────────────────────
cp "$DOTFILES_DIR/tmux/.config/tmux/theme-switch.sh" "$HOME/.local/bin/theme-switch"
chmod +x "$HOME/.local/bin/theme-switch"
ok "theme-switch → ~/.local/bin/theme-switch"

# ── 9. Reload tmux if running ─────────────────────────────────────────────────
if tmux list-sessions &>/dev/null; then
  tmux source-file "$HOME/.config/tmux/tmux.conf" 2>/dev/null && ok "tmux config reloaded" || warn "tmux reload failed (non-fatal)"
fi

# ── 10. PATH check ────────────────────────────────────────────────────────────
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo ""
  warn "~/.local/bin is not in your PATH yet."
  warn "Open a new shell or run: source ~/.bashrc"
fi

echo ""
ok "Done. Default theme: $DEFAULT_THEME"
echo ""
echo "  Toggle theme:  theme-switch dark"
echo "                 theme-switch light"
echo ""
echo "  Reload shell:  source ~/.bashrc"
echo ""
