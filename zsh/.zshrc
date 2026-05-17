# =============================================================
# .zshrc - zsh config file
# =============================================================
#
# TABLE OF CONTENTS
#   1.  Bootstrap        - bytecode compile + non-interactive guard
#   2.  Completion       - compinit, cache, matcher rules
#   3.  Plugins          - zsh-autosuggestions (syntax-highlighting)
#   4.  Keybindings      - emacs keymap, custom binds
#   5.  Environment      - EDITOR / VISUAL / MANPAGER
#   6.  Lazy loaders     - defer rbenv until first use
#   7.  VM functions     - startvm / stopvm / vmstatus
#   8.  Theme            - dark/light detection, highlight styles
#   9.  Cached tool init - _zcache helper, zoxide, atuin
#   10. Aliases          - ls, git, tmux, misc.
#   11. Exports          - FZF defaults
#   12. Functions        - kzshcache, fp, cdd, cdf, tools
#   13. Prompt           - starship (loaded late)
#   14. Late hooks       - syntax-highlighting, bun, theme init
#
# HOW TO UPDATE
#
#   Add an alias        Put it under Section 10. An inline `# comment` becomes
#                       the description shown by `tools`.
#                         alias gco="git checkout"  # Git checkout
#
#   Add a function      Put it under Section 12 (or 7 for VM helpers). The
#                       comment ON THE LINE ABOVE the function name
#                       becomes the `tools` description. Functions whose
#                       names start with `_` are treated as private and
#                       hidden from `tools`.
#                         # Fuzzy-find a file and cd to its directory
#                         cdf() { ... }
#
#   Add an env var      Put it under Section 5 (or 11 if FZF-related).
#                         export FOO="bar"
#
#   Add a keybind       Put it under Section 4.
#                         bindkey '^G' some-widget
#
#   After editing       Run `kzshcache && exec zsh` to clear the bytecode
#                       + completion cache and restart the shell.
#
#   See what's here     Run `tools` - prints every alias/function in this
#                       file with the description parsed from comments.
# =============================================================


# -------------------------------------------------------------
# 1. Bootstrap
# -------------------------------------------------------------

# Recompile .zshrc -> .zshrc.zwc whenever the source is newer (faster startup)
if [[ -s ~/.zshrc && ( ! -s ~/.zshrc.zwc || ~/.zshrc -nt ~/.zshrc.zwc ) ]]; then
  zcompile ~/.zshrc
fi

# Skip the rest for non-interactive shells (scripts, scp, etc.)
[[ -o interactive ]] || return


# -------------------------------------------------------------
# 2. Completion
# -------------------------------------------------------------

# Persist completion data to disk so re-init is cheap
zstyle ':completion:*' use-cache yes
zstyle ':completion:*' cache-path ~/.zcompcache
mkdir -p ~/.zcompcache

# Case-insensitive + smart hyphen/underscore expansion
zstyle ':completion:*' matcher-list \
  'm:{a-zA-Z}={A-Za-z}' \
  'r:|[._-]=* r:|=*'

# `-C` skips the security re-scan of $fpath (saves boot time)
autoload -Uz compinit
compinit -C


# -------------------------------------------------------------
# 3. Plugins (early - syntax-highlighting loads in Section 14 on purpose)
# -------------------------------------------------------------

[[ -r /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]] && \
  source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh


# -------------------------------------------------------------
# 4. Keybindings
# -------------------------------------------------------------

# Force emacs keymap - without this, EDITOR=nvim makes zsh default to vi
# mode (because "nvim" contains "vi") and breaks Ctrl-A / Ctrl-E / etc
bindkey -e

# Ctrl-O clears the screen (Ctrl-L is taken by vim-tmux-navigator)
bindkey '^O' clear-screen


# -------------------------------------------------------------
# 5. Environment
# -------------------------------------------------------------

# Prefer nvim for tools
export MANPAGER="nvim +Man!"
export EDITOR="nvim"
export VISUAL="nvim"


# -------------------------------------------------------------
# 6. Lazy-loaded version managers
# -------------------------------------------------------------

# Defer rbenv init until the first use of ruby/gem/bundle/rails/rake/rbenv
# The stub replaces itself with the real comman after running `rbenv init`.
_lazy_rbenv() {
  unfunction ruby gem bundle rails rake rbenv 2>/dev/null
  eval "$(rbenv init - zsh)"
  "$0" "$@"
}
for cmd in ruby gem bundle rails rake rbenv; do
  function $cmd { _lazy_rbenv "$@" }
done


# -------------------------------------------------------------
# 7. VM functions
# -------------------------------------------------------------

# Start linux dev vm
startvm() {
    VM_IP="192.168.64.3"
    VM_NAME="Linux"

    echo "Checking VM status..."

    # Check if UTM is running
    if ! pgrep -x "UTM" > /dev/null; then
        echo "UTM is not running. Starting UTM..."
        open -a UTM
        echo "Waiting for UTM to load..."
        sleep 3
    else
        echo "UTM is already running"
    fi

    # Check if VM is responding
    if ! ping -c 1 -W 1 $VM_IP > /dev/null 2>&1; then
        echo "VM is not running. Starting VM..."

    # Use AppleScript to start the VM in UTM
    osascript <<EOF
          tell application "UTM"
              activate
              delay 1
              tell virtual machine "$VM_NAME"
                  start
              end tell
          end tell
EOF

        echo "Waiting for VM to boot (this may take 30-60 seconds)..."

        # Wait for VM to be accessible
        counter=0
        while ! ping -c 1 -W 1 $VM_IP > /dev/null 2>&1; do
            sleep 2
            counter=$((counter + 2))
            if [ $counter -gt 60 ]; then
                echo "VM failed to start after 60 seconds"
                echo "Please check UTM and start the VM manually"
                return 1
            fi
            echo -n "."
        done
        echo ""

        # Extra wait for SSH to be ready
        echo "Waiting for SSH service..."
        while ! nc -zv $VM_IP 22 > /dev/null 2>&1; do
            sleep 2
        done

        echo "VM is now running."
    else
        echo "VM is already running"
    fi

    # Connect via SSH
    echo "Connecting to Ubuntu VM..."
    ssh waehner@$VM_IP
}

# Shut down the Ubuntu VM over SSH
stopvm() {
    VM_IP="192.168.64.3"

    if ping -c 1 -W 1 $VM_IP > /dev/null 2>&1; then
        echo "Shutting down Ubuntu VM..."
        ssh waehner@$VM_IP "sudo shutdown -h now"
        echo "Shutdown command sent"
    else
        echo "VM is not running"
    fi
}

# Check VM status without connecting
vmstatus() {
    VM_IP="192.168.64.3"

    echo "Checking status..."

    if pgrep -x "UTM" > /dev/null; then
        echo "UTM: Running"
    else
        echo "UTM: Not running"
    fi

    if ping -c 1 -W 1 $VM_IP > /dev/null 2>&1; then
        echo "VM: Running at $VM_IP"
        if nc -zv $VM_IP 22 > /dev/null 2>&1; then
            echo "SSH: Available"
        else
            echo "SSH: Not ready"
        fi
    else
        echo "VM: Not running"
    fi
}


# -------------------------------------------------------------
# 8. Theme (dark / light mode)
# -------------------------------------------------------------

# Syntax-highlight colors (consumed by zsh-syntax-highlighting in 14)
typeset -A ZSH_HIGHLIGHT_STYLES
ZSH_HIGHLIGHT_STYLES[command]='fg=cyan'
ZSH_HIGHLIGHT_STYLES[builtin]='fg=blue'
ZSH_HIGHLIGHT_STYLES[alias]='fg=magenta'
ZSH_HIGHLIGHT_STYLES[path]='fg=yellow'

# macOS-only dark mode detection
# non-macOS falls through to the light branch
_is_dark_mode() {
  [[ $(defaults read -g AppleInterfaceStyle 2>/dev/null) == "Dark" ]]
}

if _is_dark_mode; then
  ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#777777'
  export BAT_THEME="TokyoNight Night"
else
  ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#333333'
  export BAT_THEME="TokyoNight Day"
fi

# Starship palette is swapped by theme-switch.sh (sed-edits starship.toml),
# since starship 1.25 ignores the STARSHIP_PALETTE env var.

unset -f _is_dark_mode


# -------------------------------------------------------------
# 9. Cached tool init
# -------------------------------------------------------------

[[ -d ~/.cache/zsh ]] || mkdir -p ~/.cache/zsh

# Cache `<tool> init zsh` output once and source it on every startup. Don't
# cache tools whose init output depends on the current shell state (rbenv,
# pyenv, etc.).
_zcache() {
  local cache_file="$HOME/.cache/zsh/$1.zsh"

  if [[ ! -f "$cache_file" ]]; then
    case $1 in
      zoxide)   zoxide init zsh > "$cache_file" ;;
      atuin)    atuin init zsh --disable-up-arrow > "$cache_file" ;;
      starship) starship init zsh > "$cache_file" ;;
      *) return ;;
    esac
  fi

  [[ -f "$cache_file" ]] && source "$cache_file"
}

_zcache "zoxide"
_zcache "atuin"


# -------------------------------------------------------------
# 10. Aliases
# -------------------------------------------------------------

# Re-map cd to z
alias cd="z" # Remap cd to zoxide

# Re-map lg to lazygit
alias lg="lazygit" # LazyGit

# Eza
alias ls="eza --icons --group-directories-first" # Default ls with icons
alias ll="eza -lagh --icons --git --group-directories-first" # Long listing with git status
alias la="eza -a --icons --group-directories-first" # All files, including hidden
alias lt="eza --tree --level=2 --icons" # Tree view (2 levels)
alias l1="eza -1 --icons" # Single column

# git
alias g="git" # Git
alias gs="git status" # Git status
alias ga="git add" # Git add
alias gc="git commit" # Git commit
alias gcm="git commit -m" # Git commit with message
alias gp="git push" # Git push
alias gpl="git pull" # Git pull
alias gl="git log --oneline --graph --decorate" # Git log oneline
alias gd="git diff" # Git diff
alias gdm="git diff origin/main..HEAD" # Git diff unpushed commits vs origin/main
alias gdml="git diff main..HEAD" # Git diff unpushed commits vs local main
alias gco="git checkout" # Git checkout
alias gb="git branch" # Git branch
alias gsw="git switch" # Git switch
alias gst="git stash" # Git stash

# tmux
alias t='tmux new-session -A -s main' # Attach to main session, or create if it doesn't exist
alias tls="tmux ls" # List active sessions
alias tm="tmux new-session -s" # Create a new session with a specific name (e.g., tm dotfiles)
alias ta="tmux attach-session -t" # Attach to an existing session by name (e.g., ta dotfiles)
alias tk="tmux kill-session -t" # Kill a specific session (e.g., tk main)
alias tka="tmux kill-server" # Nuke all tmux sessions entirely

# misc
alias claude-school="CLAUDE_CONFIG_DIR=~/.claude-school claude" # Claude code with school account
alias fuck='eval "$(thefuck --alias)" && fuck' # Lazy thefuck init
alias sort-downloads="~/Code/Python/sort-downloads/main.py" # Sort Downloads


# -------------------------------------------------------------
# 11. Exports
# -------------------------------------------------------------

# Use fd for fzf (ignores node_modules / .git)
export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# fzf palette (prompt / header / pointer colors)
export FZF_DEFAULT_OPTS='--color=fg+:7,bg:-1,hl:4,hl+:4,info:6,prompt:5,spinner:5,pointer:5,marker:2,header:6'


# -------------------------------------------------------------
# 12. Functions
# -------------------------------------------------------------

# Nuke all zsh caches (bytecode + completion + tool-init cache)
kzshcache() {
  rm -f ~/.cache/zsh/*.zsh ~/.zshrc.zwc
  rm -rf ~/.zcompcache
  echo "zsh caches cleared - re-source to rebuild"
}

# Fuzzy find a file and preview its contents
fp() {
  fzf --preview 'bat --style=numbers --color=always --line-range :500 {}'
}

# Cd to a directory while previewing its contents
cdd() {
  local dir
  dir=$(fd -t d | fzf --preview 'eza --tree --level=1 --icons --color=always {}') || return
  cd "$dir"
}

# Cd to a file's parent directory using fzf
cdf() {
  local file
  file=$(find . -type f 2>/dev/null | fzf) || return
  cd "$(dirname "$file")"
}

# List every alias / function in this file with its description
tools() {
  printf "\n\033[1;35mCustom Zsh Tools & Aliases\033[0m\n\n"

  awk '
    # 1. Match standalone comments
    /^[ \t]*#[^-]/ {
      comment = $0
      sub(/^[ \t]*#[ \t]*/, "", comment)
      if (comment == "") next
      last_comment = comment
      next
    }

    # 2. Ignore dashed divider lines
    /^[ \t]*#[-]+/ { next }

    # 3. Match aliases
    /^[ \t]*alias[ \t]+[^=]+=/ {
      raw_line = $0

      # Extract inline comment (if it exists) and remove it from raw_line
      inline_comment = ""
      if (match(raw_line, /#[ \t]*.*/)) {
        inline_comment = substr(raw_line, RSTART+1)
        sub(/^[ \t]*/, "", inline_comment)
        raw_line = substr(raw_line, 1, RSTART-1)
      }

      # Extract alias name
      match(raw_line, /alias[ \t]+[^=]+/)
      name = substr(raw_line, RSTART+6, RLENGTH-6)

      # Extract the actual command (everything after =)
      cmd = substr(raw_line, RSTART+RLENGTH+1)

      # Strip leading/trailing spaces and quotes from the command
      # \047 is the octal code for a single quote, preventing bash parsing errors
      sub(/^[ \t]*[\047"]?/, "", cmd)
      sub(/[\047"]?[ \t]*$/, "", cmd)

      # Determine description: Inline > Block Comment > Raw Command
      if (inline_comment != "") {
        desc = inline_comment
      } else if (last_comment != "") {
        desc = last_comment
      } else {
        # Use the raw command with a subtle arrow prefix
        desc = "\033[90m→ " cmd "\033[0m"
      }

      printf "  \033[36m%-15s\033[0m %s\n", name, desc

      last_comment = ""
      next
    }

    # 4. Match functions
    /^[ \t]*[A-Za-z0-9_-]+[ \t]*\(\)[ \t]*\{?/ {
      match($0, /^[ \t]*[A-Za-z0-9_-]+/)
      name = substr($0, RSTART, RLENGTH)
      sub(/^[ \t]*/, "", name)

      # IGNORE local functions starting with an underscore
      if (name ~ /^_/) {
        last_comment = ""
        next
      }

      if (last_comment != "") {
        printf "  \033[32m%-15s\033[0m %s\n", name, last_comment
      }
      last_comment = ""
      next
    }

    # 5. Ignore blank lines
    /^[ \t]*$/ { next }

    # 6. Any other code clears the comment
    { last_comment = "" }
  ' ~/.zshrc

  echo ""
}


# -------------------------------------------------------------
# 13. Prompt (loaded late)
# -------------------------------------------------------------

_zcache "starship"


# -------------------------------------------------------------
# 14. Late hooks (must come after everything else)
# -------------------------------------------------------------

# Syntax highlighting - load last so it sees the final keybindings / aliases
[[ -r /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && \
  source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# bun completions
[ -s "/Users/lukewaehner/.bun/_bun" ] && source "/Users/lukewaehner/.bun/_bun"

# Theme init - applies the correct light/dark tmux+nvim theme to new
# terminal windows. Live theme switching is handled by the dark-notify
# launchd agent on macOS.
if [[ "$OSTYPE" == "darwin"* ]]; then
  "$HOME/.local/bin/theme-switch.sh" auto
else
  "$HOME/.local/bin/theme-switch.sh" light
fi
