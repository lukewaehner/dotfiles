# ---- login environment (runs once) ----

# Homebrew. `brew shellenv` is a ~50ms bash script whose output is static for
# a given install, so cache it and source the cache; it is regenerated when
# the brew binary changes, and `kzshcache` clears it.
if [ -x /opt/homebrew/bin/brew ]; then
  _brew_env="$HOME/.cache/zsh/brew-shellenv.zsh"
  if [[ ! -s "$_brew_env" || /opt/homebrew/bin/brew -nt "$_brew_env" ]]; then
    mkdir -p "${_brew_env:h}"
    /opt/homebrew/bin/brew shellenv > "$_brew_env"
  fi
  source "$_brew_env"
  unset _brew_env
fi

# Version manager roots
export PYENV_ROOT="$HOME/.pyenv"
export RBENV_ROOT="$HOME/.rbenv"

# Tooling PATH (static -- no eval needed)
export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$RBENV_ROOT/shims:$RBENV_ROOT/bin:$PATH"
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"
export PATH="$HOME/.elan/bin:$PATH"
# npm globals live under the active nvm version (~/.nvm/versions/node/<v>/bin),
# which nvm prepends on load. The old fixed ~/.npm-global prefix was removed
# because npm's `prefix` setting and nvm are mutually incompatible.
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/bin:$PATH"

export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"

export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"


# Added by Antigravity CLI installer
export PATH="/Users/lukewaehner/.local/bin:$PATH"
