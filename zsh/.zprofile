# ---- login environment (runs once) ----

# Homebrew
if [ -x /opt/homebrew/bin/brew ]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Tooling PATH
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"
export PATH="$HOME/.elan/bin:$PATH"
export PATH="$HOME/.npm-global/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

# Version managers (roots only; init happens in .zshrc)
export PYENV_ROOT="$HOME/.pyenv"
export RBENV_ROOT="$HOME/.rbenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PATH="$RBENV_ROOT/bin:$PATH"
