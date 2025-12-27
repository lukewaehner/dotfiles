#!/usr/bin/env bash
set -euo pipefail

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/repos/dotfiles}"
BREWFILE="${BREWFILE:-$DOTFILES_DIR/brew/Brewfile}"
STOW_TARGET="${STOW_TARGET:-$HOME}"

log() { printf "\n==> %s\n" "$*"; }
warn() { printf "\n[warn] %s\n" "$*" >&2; }
die() {
  printf "\n[err] %s\n" "$*" >&2
  exit 1
}

require_dir() {
  [[ -d "$1" ]] || die "Missing directory: $1"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

install_xcode_clt_if_needed() {
  # Homebrew and many dev tools assume CLT on macOS
  if xcode-select -p >/dev/null 2>&1; then
    return 0
  fi
  log "Installing Xcode Command Line Tools (required for Homebrew)"
  xcode-select --install || true
  warn "If a GUI prompt appeared, complete the install, then re-run this script."
  exit 1
}

install_homebrew_if_needed() {
  if command_exists brew; then
    return 0
  fi

  log "Homebrew not found. Installing Homebrew"
  # Official install script is fetched from GitHub; requires network access.
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

  # Ensure brew is on PATH for this session (Apple Silicon default)
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi

  command_exists brew || die "Homebrew install failed or brew not on PATH"
}

brew_bundle_if_present() {
  if [[ -f "$BREWFILE" ]]; then
    log "Running Brewfile: $BREWFILE"
    brew bundle --file "$BREWFILE"
  else
    warn "No Brewfile found at $BREWFILE (skipping brew bundle)"
  fi
}

install_stow_if_needed() {
  if command_exists stow; then
    return 0
  fi
  log "Installing stow"
  brew install stow
  command_exists stow || die "stow install failed"
}

stow_modules() {
  require_dir "$DOTFILES_DIR"
  cd "$DOTFILES_DIR"

  mkdir -p "$HOME/.config" "$HOME/.local/bin"

  # Stow all top-level directories except known non-modules
  local excludes_regex='^(brew|\.git|\.github)$'
  local modules=()
  local d
  for d in */; do
    d="${d%/}"
    [[ "$d" =~ $excludes_regex ]] && continue
    # Only stow if it looks like a stow package (has dotfiles or .config etc.)
    [[ -d "$DOTFILES_DIR/$d" ]] && modules+=("$d")
  done

  if [[ "${#modules[@]}" -eq 0 ]]; then
    warn "No stow modules found in $DOTFILES_DIR"
    return 0
  fi

  log "Stowing modules into $STOW_TARGET: ${modules[*]}"
  # --restow makes this idempotent (relinks cleanly)
  stow -t "$STOW_TARGET" --restow "${modules[@]}"
}

main() {
  require_dir "$DOTFILES_DIR"

  log "Bootstrap starting"
  log "Dotfiles dir: $DOTFILES_DIR"

  [[ "$OSTYPE" == "darwin"* ]] || die "macOS only"

  install_xcode_clt_if_needed
  install_homebrew_if_needed

  # Homebrew env
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi

  brew_bundle_if_present
  install_stow_if_needed

  # -------------------------------------------------
  # Language toolchains
  # -------------------------------------------------

  log "Ensuring Rust (latest stable)"
  if ! command -v rustup >/dev/null 2>&1; then
    rustup-init -y
  fi
  export PATH="$HOME/.cargo/bin:$PATH"
  rustup toolchain install stable
  rustup default stable

  # Make pyenv / rbenv usable in this script
  export PYENV_ROOT="$HOME/.pyenv"
  export RBENV_ROOT="$HOME/.rbenv"
  export PATH="$PYENV_ROOT/bin:$RBENV_ROOT/bin:$PATH"
  eval "$(pyenv init - bash 2>/dev/null || true)"
  eval "$(rbenv init - bash 2>/dev/null || true)"

  log "Ensuring Python via pyenv"
  pyenv install -s 3.9.6
  # Latest stable Python version
  LATEST_PYTHON="$(
    pyenv install -l |
      sed 's/^[[:space:]]*//' |
      grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' |
      grep -vE '(a|b|rc)' |
      tail -n 1
  )"

  log "Latest Python detected: $LATEST_PYTHON"

  pyenv install -s "$LATEST_PYTHON"
  pyenv global 3.9.6

  log "Ensuring Ruby via rbenv"
  RB_VER="${RB_VER:-3.3.6}"
  rbenv install -s "$RB_VER"
  rbenv global "$RB_VER"

  # -------------------------------------------------
  # Dotfiles
  # -------------------------------------------------
  stow_modules

  log "Rebuilding bat themes cache"
  bat cache --build

  log "Bootstrap complete"
}

main "$@"
