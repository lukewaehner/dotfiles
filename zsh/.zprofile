# ---- login environment (runs once) ----

# Homebrew
if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
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
