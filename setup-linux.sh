#!/usr/bin/env bash
# setup-linux.sh — interactive bootstrap for a Linux dev environment
#
# Usage:
#   bash setup-linux.sh [night|day]   — interactive menu (default theme: night)
#   bash setup-linux.sh --uninstall   — remove installed files with confirmation
#
# Safe to run multiple times — all steps are idempotent.

if [ -z "$BASH_VERSION" ]; then exec bash "$0" "$@"; fi
set -euo pipefail

# ── Output helpers ─────────────────────────────────────────────────────────────
RED='\033[0;31m'; YEL='\033[0;33m'; GRN='\033[0;32m'
DIM='\033[2m'; BOLD='\033[1m'; NC='\033[0m'

info() { echo -e "  $*"; }
ok()   { echo -e "  ${GRN}✓${NC} $*"; }
warn() { echo -e "  ${YEL}!${NC} $*"; }
hdr()  { echo -e "\n${BOLD}  ── $* ──${NC}"; }

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_THEME="night"

# ── Helpers ────────────────────────────────────────────────────────────────────
confirm_remove() {
  local label="$1" path="$2"
  [[ ! -e "$path" ]] && { info "$label not found at $path — skipping"; return 1; }
  printf "  Confirm: remove %s at %s? [y/N] " "$label" "$path"
  read -r answer </dev/tty
  [[ "$answer" =~ ^[Yy]$ ]] || { info "Skipped $label"; return 1; }
}

pkg_installed() {
  case "$1" in
    ripgrep) command -v rg     &>/dev/null ;;
    fd-find) command -v fdfind &>/dev/null || command -v fd  &>/dev/null ;;
    bat)     command -v batcat &>/dev/null || command -v bat &>/dev/null ;;
    *)       command -v "$1"   &>/dev/null ;;
  esac
}

expand_theme() {
  local src="$1" dst="$2" sed_args=() line key val
  while IFS= read -r line; do
    if [[ "$line" =~ ^([A-Z_]+)=\"([^\"]*)\"$ ]]; then
      key="${BASH_REMATCH[1]}"; val="${BASH_REMATCH[2]}"
      sed_args+=(-e "s/\${${key}}/${val}/g")
    fi
  done < "$src"
  if [[ ${#sed_args[@]} -gt 0 ]]; then sed "${sed_args[@]}" "$src" > "$dst"
  else cp "$src" "$dst"; fi
}

# ══════════════════════════════════════════════════════════════════════════════
# STATUS CHECKS  (sets global STATUS_<key>: "ok" | "partial" | "missing")
# ══════════════════════════════════════════════════════════════════════════════

PACKAGES=(tmux ncdu htop curl git unzip ripgrep fd-find fzf bat tree stow direnv jq snapd vim)

check_all_statuses() {
  # system_packages
  local miss=0
  for p in "${PACKAGES[@]}"; do pkg_installed "$p" || (( miss++ )) || true; done
  if   (( miss == 0 ));                 then STATUS_system_packages="ok"
  elif (( miss == ${#PACKAGES[@]} ));   then STATUS_system_packages="missing"
  else                                       STATUS_system_packages="partial ($miss missing)"
  fi

  # github_cli
  command -v gh    &>/dev/null && STATUS_github_cli="ok"    || STATUS_github_cli="missing"

  # neovim
  command -v nvim  &>/dev/null && STATUS_neovim="ok"        || STATUS_neovim="missing"

  # ruff
  command -v ruff  &>/dev/null && STATUS_ruff="ok"          || STATUS_ruff="missing"

  # shell_tools
  local st=0
  command -v starship &>/dev/null && (( st++ )) || true
  command -v atuin    &>/dev/null && (( st++ )) || true
  command -v zoxide   &>/dev/null && (( st++ )) || true
  if   (( st == 3 )); then STATUS_shell_tools="ok"
  elif (( st == 0 )); then STATUS_shell_tools="missing"
  else                     STATUS_shell_tools="partial ($st/3)"
  fi

  # cli_tools
  local ct=0
  command -v eza     &>/dev/null && (( ct++ )) || true
  command -v lazygit &>/dev/null && (( ct++ )) || true
  if   (( ct == 2 )); then STATUS_cli_tools="ok"
  elif (( ct == 0 )); then STATUS_cli_tools="missing"
  else                     STATUS_cli_tools="partial ($ct/2)"
  fi

  # nodejs
  local nt=0
  command -v node &>/dev/null && (( nt++ )) || true
  { command -v claude &>/dev/null || [[ -x "$HOME/.npm-global/bin/claude" ]]; } && (( nt++ )) || true
  if   (( nt == 2 )); then STATUS_nodejs="ok"
  elif (( nt == 0 )); then STATUS_nodejs="missing"
  else                     STATUS_nodejs="partial ($nt/2)"
  fi

  # dotfiles
  local dl=0
  [[ -L "$HOME/.config/nvim"            ]] && (( dl++ )) || true
  [[ -L "$HOME/.vimrc"                  ]] && (( dl++ )) || true
  [[ -L "$HOME/.config/starship.toml"   ]] && (( dl++ )) || true
  [[ -L "$HOME/.zshrc"                  ]] && (( dl++ )) || true
  if   (( dl == 4 )); then STATUS_dotfiles="ok"
  elif (( dl == 0 )); then STATUS_dotfiles="missing"
  else                     STATUS_dotfiles="partial ($dl/4 symlinks)"
  fi

  # vim_plugins
  if   [[ -f "$HOME/.vim/autoload/plug.vim" && -d "$HOME/.vim/plugged" ]]; then STATUS_vim_plugins="ok"
  elif [[ -f "$HOME/.vim/autoload/plug.vim" ]];                             then STATUS_vim_plugins="partial (plug.vim only)"
  else                                                                           STATUS_vim_plugins="missing"
  fi

  # tmux
  [[ -f "$HOME/.config/tmux/tmux.conf" ]] && STATUS_tmux="ok" || STATUS_tmux="missing"

  # bashrc
  grep -qF "# ── dotfiles ──" "$HOME/.bashrc" 2>/dev/null \
    && STATUS_bashrc="ok" || STATUS_bashrc="missing"
}

status_badge() {
  case "$1" in
    ok)      echo -e "${GRN}✓ installed${NC}" ;;
    missing) echo -e "${RED}✗ missing${NC}" ;;
    *)       echo -e "${YEL}~ $1${NC}" ;;   # partial with detail
  esac
}

# ══════════════════════════════════════════════════════════════════════════════
# INSTALL FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

install_system_packages() {
  hdr "System packages"
  local MISSING=()
  for pkg in "${PACKAGES[@]}"; do pkg_installed "$pkg" || MISSING+=("$pkg"); done

  if [[ ${#MISSING[@]} -gt 0 ]]; then
    if ! command -v apt-get &>/dev/null; then
      warn "apt-get not found. Install manually: ${MISSING[*]}"; return 1
    fi
    info "Installing: ${MISSING[*]}"
    sudo apt-get update -qq
    sudo apt-get install -y "${MISSING[@]}"
  fi

  mkdir -p "$HOME/.local/bin"
  if command -v fdfind &>/dev/null && ! command -v fd &>/dev/null; then
    ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd" && ok "fd → fdfind shim"
  fi
  if command -v batcat &>/dev/null && ! command -v bat &>/dev/null; then
    ln -sf "$(command -v batcat)" "$HOME/.local/bin/bat" && ok "bat → batcat shim"
  fi
  ok "System packages ready"
}

install_github_cli() {
  hdr "GitHub CLI"
  if command -v gh &>/dev/null; then ok "Already installed"; return; fi
  info "Installing GitHub CLI..."
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  sudo apt-get update -qq && sudo apt-get install -y gh
  ok "GitHub CLI installed"
}

install_neovim() {
  hdr "Neovim"
  if command -v nvim &>/dev/null; then ok "Already installed ($(nvim --version | head -1))"; return; fi
  info "Installing neovim via snap..."
  sudo snap install nvim --classic
  ok "Neovim installed"
}

install_ruff() {
  hdr "Ruff"
  if command -v ruff &>/dev/null; then ok "Already installed ($(ruff --version))"; return; fi
  info "Installing ruff..."
  curl -LsSf https://astral.sh/ruff/install.sh | sh
  ok "Ruff installed"
}

install_shell_tools() {
  hdr "Shell tools"
  if ! command -v starship &>/dev/null; then
    info "Installing starship..."
    curl -fsSL https://starship.rs/install.sh | sh -s -- --yes && ok "starship installed"
  else ok "starship already installed"; fi

  if ! command -v atuin &>/dev/null; then
    info "Installing atuin..."
    curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh && ok "atuin installed"
  else ok "atuin already installed"; fi

  if ! command -v zoxide &>/dev/null; then
    info "Installing zoxide..."
    curl -fsSL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh && ok "zoxide installed"
  else ok "zoxide already installed"; fi
}

install_cli_tools() {
  hdr "CLI tools"
  if ! command -v eza &>/dev/null; then
    if apt-cache show eza &>/dev/null 2>&1; then
      info "Installing eza via apt..." && sudo apt-get install -y eza
    else
      info "Installing eza from GitHub release..."
      local EZA_VER
      EZA_VER=$(curl -fsSL https://api.github.com/repos/eza-community/eza/releases/latest \
        | grep '"tag_name"' | cut -d'"' -f4)
      curl -fsSL "https://github.com/eza-community/eza/releases/download/${EZA_VER}/eza_x86_64-unknown-linux-gnu.tar.gz" \
        | tar -xz -C "$HOME/.local/bin" eza
    fi
    ok "eza installed"
  else ok "eza already installed"; fi

  if ! command -v lazygit &>/dev/null; then
    info "Installing lazygit from GitHub release..."
    local LG_VER
    LG_VER=$(curl -fsSL https://api.github.com/repos/jesseduffield/lazygit/releases/latest \
      | grep '"tag_name"' | cut -d'"' -f4 | sed 's/^v//')
    curl -fsSL "https://github.com/jesseduffield/lazygit/releases/download/v${LG_VER}/lazygit_${LG_VER}_Linux_x86_64.tar.gz" \
      | tar -xz -C "$HOME/.local/bin" lazygit
    ok "lazygit installed"
  else ok "lazygit already installed"; fi
}

install_nodejs() {
  hdr "Node.js + Claude Code"
  if ! command -v node &>/dev/null; then
    info "Installing Node.js 22 via NodeSource..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y nodejs
    ok "Node.js installed"
  else ok "Node.js already installed ($(node --version))"; fi

  [[ ! -d "$HOME/.npm-global" ]] && mkdir -p "$HOME/.npm-global" && npm config set prefix "$HOME/.npm-global"

  if ! command -v claude &>/dev/null && [[ ! -x "$HOME/.npm-global/bin/claude" ]]; then
    info "Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code && ok "Claude Code installed"
  else ok "Claude Code already installed"; fi
}

install_dotfiles() {
  hdr "Dotfiles (stow)"
  mkdir -p "$HOME/.config"
  stow --dir="$DOTFILES_DIR" -t "$HOME" --restow atuin bat eza git lazygit nvim starship vim zsh \
    || warn "Some stow modules had conflicts — run 'stow --adopt' manually to resolve"
  ok "Dotfiles stowed → $HOME"

  if command -v bat &>/dev/null; then
    bat cache --build &>/dev/null && ok "bat theme cache rebuilt"
  elif command -v batcat &>/dev/null; then
    batcat cache --build &>/dev/null && ok "bat theme cache rebuilt"
  fi
}

install_vim_plugins() {
  hdr "Vim plugins"
  local plug="$HOME/.vim/autoload/plug.vim"
  if [[ ! -f "$plug" ]]; then
    info "Installing vim-plug..."
    curl -fLo "$plug" --create-dirs \
      https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    ok "vim-plug installed"
  else ok "vim-plug already installed"; fi

  if command -v vim &>/dev/null && [[ -f "$HOME/.vimrc" ]]; then
    info "Installing vim plugins..."
    vim +PlugInstall +qall </dev/null && ok "Plugins installed"
  else warn "vim or ~/.vimrc not found — stow dotfiles first, then re-run this step"; fi
}

install_tmux() {
  hdr "tmux config"
  mkdir -p "$HOME/.config/tmux/themes"
  if [[ -f "$HOME/.config/tmux/tmux.conf" ]]; then
    cp "$HOME/.config/tmux/tmux.conf" "$HOME/.config/tmux/tmux.conf.bak"
    warn "Existing tmux.conf backed up → tmux.conf.bak"
  fi
  cp           "$DOTFILES_DIR/tmux/.config/tmux/tmux.conf"         "$HOME/.config/tmux/tmux.conf"
  expand_theme "$DOTFILES_DIR/tmux/.config/tmux/themes/night.conf" "$HOME/.config/tmux/themes/night.conf"
  expand_theme "$DOTFILES_DIR/tmux/.config/tmux/themes/day.conf"   "$HOME/.config/tmux/themes/day.conf"
  ok "tmux config → ~/.config/tmux/"

  if [[ "$DEFAULT_THEME" == "night" ]]; then
    ln -sf "$HOME/.config/tmux/themes/night.conf" "$HOME/.config/tmux/themes/current.conf"
  else
    ln -sf "$HOME/.config/tmux/themes/day.conf"   "$HOME/.config/tmux/themes/current.conf"
  fi
  ok "Theme set to: $DEFAULT_THEME"

  mkdir -p "$HOME/.local/bin"
  cp "$DOTFILES_DIR/tmux/.config/tmux/theme-switch.sh" "$HOME/.local/bin/theme-switch"
  chmod +x "$HOME/.local/bin/theme-switch"
  ok "theme-switch → ~/.local/bin/theme-switch"

  if tmux list-sessions &>/dev/null; then
    tmux source-file "$HOME/.config/tmux/tmux.conf" 2>/dev/null \
      && ok "tmux config reloaded" || warn "tmux reload failed (non-fatal)"
  fi
}

install_bashrc() {
  hdr "Bash wiring"
  if grep -qF "# ── dotfiles ──" "$HOME/.bashrc" 2>/dev/null; then
    ok "~/.bashrc already configured — skipping"; return
  fi
  info "Appending dotfiles block to ~/.bashrc..."
  cat >> "$HOME/.bashrc" << 'BASHRC_BLOCK'

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

# Cached tool inits
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
}

# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT REGISTRY
# ══════════════════════════════════════════════════════════════════════════════

COMP_KEYS=(
  system_packages
  github_cli
  neovim
  ruff
  shell_tools
  cli_tools
  nodejs
  dotfiles
  vim_plugins
  tmux
  bashrc
)

COMP_LABELS=(
  "System packages (apt)"
  "GitHub CLI"
  "Neovim"
  "Ruff (Python linter)"
  "Shell tools       (starship, atuin, zoxide)"
  "CLI tools         (eza, lazygit)"
  "Node.js + Claude Code"
  "Dotfiles          (stow)"
  "Vim plugins       (vim-plug + :PlugInstall)"
  "tmux config"
  "Bash wiring       (~/.bashrc)"
)

run_component() {
  case "$1" in
    system_packages) install_system_packages ;;
    github_cli)      install_github_cli ;;
    neovim)          install_neovim ;;
    ruff)            install_ruff ;;
    shell_tools)     install_shell_tools ;;
    cli_tools)       install_cli_tools ;;
    nodejs)          install_nodejs ;;
    dotfiles)        install_dotfiles ;;
    vim_plugins)     install_vim_plugins ;;
    tmux)            install_tmux ;;
    bashrc)          install_bashrc ;;
  esac
}

get_status_var() {
  local varname="STATUS_$1"
  echo "${!varname:-?}"
}

is_missing_or_partial() {
  local s; s=$(get_status_var "$1")
  [[ "$s" != "ok" ]]
}

# ══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE MENU
# ══════════════════════════════════════════════════════════════════════════════

show_menu() {
  check_all_statuses
  echo ""
  echo -e "${BOLD}╔══════════════════════════════════════════════════════╗${NC}"
  echo -e "${BOLD}║       Linux Dev Environment Bootstrap                ║${NC}"
  echo -e "${BOLD}╚══════════════════════════════════════════════════════╝${NC}"
  echo -e "  ${DIM}Dotfiles: $DOTFILES_DIR  Theme: $DEFAULT_THEME${NC}"
  echo ""

  local i=0
  for key in "${COMP_KEYS[@]}"; do
    local s badge
    s=$(get_status_var "$key")
    badge=$(status_badge "$s")
    printf "  ${DIM}[%2d]${NC}  %-44s %b\n" "$((i+1))" "${COMP_LABELS[$i]}" "$badge"
    (( i++ )) || true
  done

  echo ""
  echo -e "  ${BOLD}a${NC}  Install all"
  echo -e "  ${BOLD}m${NC}  Install missing / partial only"
  echo -e "  ${BOLD}q${NC}  Quit"
  echo ""
  echo -e "  ${DIM}Or enter space-separated numbers, e.g: 1 4 9${NC}"
  echo ""
}

run_menu() {
  while true; do
    show_menu
    printf "  Selection: "
    read -r input </dev/tty
    echo ""

    [[ "$input" == "q" || "$input" == "Q" ]] && { info "Bye."; exit 0; }

    local selected=()

    if [[ "$input" == "a" || "$input" == "A" ]]; then
      selected=("${COMP_KEYS[@]}")

    elif [[ "$input" == "m" || "$input" == "M" ]]; then
      for key in "${COMP_KEYS[@]}"; do
        is_missing_or_partial "$key" && selected+=("$key") || true
      done
      if [[ ${#selected[@]} -eq 0 ]]; then
        echo -e "  ${GRN}Everything looks installed already!${NC}"
        echo ""
        printf "  Press enter to refresh or q to quit: "
        read -r again </dev/tty
        [[ "$again" == "q" ]] && exit 0
        continue
      fi

    else
      for token in $input; do
        if [[ "$token" =~ ^[0-9]+$ ]] && (( token >= 1 && token <= ${#COMP_KEYS[@]} )); then
          selected+=("${COMP_KEYS[$((token-1))]}")
        else
          warn "Ignoring invalid selection: '$token'"
        fi
      done
      [[ ${#selected[@]} -eq 0 ]] && continue
    fi

    echo -e "  ${BOLD}Running:${NC} ${selected[*]}"
    echo ""

    for key in "${selected[@]}"; do
      run_component "$key"
    done

    echo ""
    echo -e "  ${GRN}${BOLD}Done!${NC}"
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
      echo ""
      warn "~/.local/bin not in PATH yet — run: source ~/.bashrc"
    fi
    echo ""
    printf "  Back to menu? [Y/n] "
    read -r again </dev/tty
    [[ "$again" =~ ^[Nn]$ ]] && break
  done
}

# ══════════════════════════════════════════════════════════════════════════════
# UNINSTALL
# ══════════════════════════════════════════════════════════════════════════════

run_uninstall() {
  info "Uninstalling dotfiles from this machine..."
  echo ""

  if confirm_remove "tmux.conf"    "$HOME/.config/tmux/tmux.conf";           then rm -f "$HOME/.config/tmux/tmux.conf";           ok "Removed tmux.conf"; fi
  if confirm_remove "night.conf"   "$HOME/.config/tmux/themes/night.conf";   then rm -f "$HOME/.config/tmux/themes/night.conf";   ok "Removed night.conf"; fi
  if confirm_remove "day.conf"     "$HOME/.config/tmux/themes/day.conf";     then rm -f "$HOME/.config/tmux/themes/day.conf";     ok "Removed day.conf"; fi
  if confirm_remove "current.conf" "$HOME/.config/tmux/themes/current.conf"; then rm -f "$HOME/.config/tmux/themes/current.conf"; ok "Removed current.conf"; fi
  if confirm_remove "theme-switch" "$HOME/.local/bin/theme-switch";          then rm -f "$HOME/.local/bin/theme-switch";          ok "Removed theme-switch"; fi

  if command -v stow &>/dev/null; then
    info "Removing stowed dotfile symlinks..."
    stow --dir="$DOTFILES_DIR" -t "$HOME" --delete atuin bat eza git lazygit nvim starship vim zsh 2>/dev/null || true
    ok "Stow symlinks removed"
  fi

  if grep -qF "# ── dotfiles ──" "$HOME/.bashrc" 2>/dev/null; then
    info "Removing dotfiles block from ~/.bashrc..."
    sed -i '/# ── dotfiles ──/,/# ── end dotfiles ──/d' "$HOME/.bashrc"
    ok "~/.bashrc block removed"
  fi

  echo ""
  info "Uninstall complete."
}

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if [[ "${1:-}" == "--uninstall" ]]; then run_uninstall; exit 0; fi

case "${1:-}" in
  day)   DEFAULT_THEME="day" ;;
  night) DEFAULT_THEME="night" ;;
  "")    DEFAULT_THEME="night" ;;
  *)     echo "Usage: bash setup-linux.sh [night|day|--uninstall]" >&2; exit 1 ;;
esac

# Make tools installed earlier in the session immediately available
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$HOME/.npm-global/bin:$PATH"

run_menu
