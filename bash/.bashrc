# =============================================================
# .bashrc - bash config file (ported from .zshrc, minus plugins)
# =============================================================
#
# TABLE OF CONTENTS
#   1.  Bootstrap        - non-interactive guard
#   2.  Completion       - bash-completion, case-insensitive matching
#   3.  Keybindings      - emacs keymap, custom binds
#   4.  Environment      - EDITOR / VISUAL / MANPAGER
#   5.  Lazy loaders     - defer rbenv until first use
#   6.  VM functions     - startvm / stopvm / vmstatus
#   7.  Theme            - dark/light detection, bat theme
#   8.  Cached tool init - _bcache helper, zoxide, atuin
#   9.  Aliases          - sourced from ~/.bash_aliases
#   10. Exports          - FZF defaults
#   11. Functions        - kbashcache, fp, cdd, cdf, tools
#   12. Prompt           - starship (loaded late)
#   13. Late hooks       - bun, theme init
#
# HOW TO UPDATE
#
#   Add an alias        Put it in ~/.bash_aliases. An inline `# comment` becomes
#                       the description shown by `tools`.
#                         alias gco="git checkout"  # Git checkout
#
#   Add a function      Put it under Section 11 (or 6 for VM helpers). The
#                       comment ON THE LINE ABOVE the function name
#                       becomes the `tools` description. Functions whose
#                       names start with `_` are treated as private and
#                       hidden from `tools`.
#                         # Fuzzy-find a file and cd to its directory
#                         cdf() { ... }
#
#   Add an env var      Put it under Section 4 (or 10 if FZF-related).
#                         export FOO="bar"
#
#   Add a keybind       Put it under Section 3.
#                         bind '"\C-g": some-widget'
#
#   After editing       Run `kbashcache && exec bash` to clear the tool-init
#                       cache and restart the shell.
#
#   See what's here     Run `tools` - prints every alias/function in this
#                       file with the description parsed from comments.
#
# NOTE: Plugins from the zsh config (zsh-autosuggestions,
#       zsh-syntax-highlighting) have no bash equivalent here and were
#       intentionally left out.
# =============================================================


# -------------------------------------------------------------
# 1. Bootstrap
# -------------------------------------------------------------

# Skip the rest for non-interactive shells (scripts, scp, etc.)
case $- in
  *i*) ;;
  *) return ;;
esac


# -------------------------------------------------------------
# 2. Completion
# -------------------------------------------------------------

# Homebrew bash-completion (v2)
if [[ -r /opt/homebrew/etc/profile.d/bash_completion.sh ]]; then
  source /opt/homebrew/etc/profile.d/bash_completion.sh
elif [[ -r /etc/profile.d/bash_completion.sh ]]; then
  source /etc/profile.d/bash_completion.sh
fi

# Case-insensitive + smart hyphen/underscore expansion (readline analog of
# the zsh matcher-list)
bind "set completion-ignore-case on"
bind "set completion-map-case on"
bind "set show-all-if-ambiguous on"


# -------------------------------------------------------------
# 3. Keybindings
# -------------------------------------------------------------

# bash defaults to the emacs keymap, but be explicit so EDITOR=nvim never
# nudges it toward vi mode.
set -o emacs

# Ctrl-O clears the screen (Ctrl-L is taken by vim-tmux-navigator)
bind '"\C-o": clear-screen'


# -------------------------------------------------------------
# 4. Environment
# -------------------------------------------------------------

# Prefer nvim for tools
export MANPAGER="nvim +Man!"
export EDITOR="nvim"
export VISUAL="nvim"

# Tuxedo config
export TODO_DIR="$HOME/Documents/todo"
export TODO_FILE="$TODO_DIR/todo.txt"
export DONE_FILE="$TODO_DIR/done.txt"


# -------------------------------------------------------------
# 5. Lazy-loaded version managers
# -------------------------------------------------------------

# Defer rbenv init until the first use of ruby/gem/bundle/rails/rake/rbenv.
# Each stub unsets all the stubs, runs the real `rbenv init`, then re-invokes
# itself - which now resolves to the real command / shim.
_lazy_rbenv() {
  unset -f ruby gem bundle rails rake rbenv 2>/dev/null
  eval "$(rbenv init - bash)"
}
for cmd in ruby gem bundle rails rake rbenv; do
  eval "${cmd}() { _lazy_rbenv; ${cmd} \"\$@\"; }"
done
unset cmd


# -------------------------------------------------------------
# 6. VM functions
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
# 7. Theme (dark / light mode)
# -------------------------------------------------------------

# macOS-only dark mode detection
# non-macOS falls through to the light branch
_is_dark_mode() {
  [[ $(defaults read -g AppleInterfaceStyle 2>/dev/null) == "Dark" ]]
}

if _is_dark_mode; then
  export BAT_THEME="TokyoNight Night"
else
  export BAT_THEME="TokyoNight Day"
fi

# Starship palette is swapped by theme-switch.sh (sed-edits starship.toml),
# since starship 1.25 ignores the STARSHIP_PALETTE env var.

unset -f _is_dark_mode


# -------------------------------------------------------------
# 8. Cached tool init
# -------------------------------------------------------------

[[ -d ~/.cache/bash ]] || mkdir -p ~/.cache/bash

# Cache `<tool> init bash` output once and source it on every startup. Don't
# cache tools whose init output depends on the current shell state (rbenv,
# pyenv, etc.).
_bcache() {
  local cache_file="$HOME/.cache/bash/$1.bash"

  if [[ ! -f "$cache_file" ]]; then
    case $1 in
      zoxide)   zoxide init bash > "$cache_file" ;;
      atuin)    atuin init bash --disable-up-arrow > "$cache_file" ;;
      starship) starship init bash > "$cache_file" ;;
      *) return ;;
    esac
  fi

  [[ -f "$cache_file" ]] && source "$cache_file"
}

_bcache "zoxide"
_bcache "atuin"


# -------------------------------------------------------------
# 9. Aliases
# -------------------------------------------------------------

[[ -f ~/.bash_aliases ]] && source ~/.bash_aliases


# -------------------------------------------------------------
# 10. Exports
# -------------------------------------------------------------

# Use fd for fzf (ignores node_modules / .git)
export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# fzf palette (prompt / header / pointer colors)
export FZF_DEFAULT_OPTS='--color=fg+:7,bg:-1,hl:4,hl+:4,info:6,prompt:5,spinner:5,pointer:5,marker:2,header:6'


# -------------------------------------------------------------
# 11. Functions
# -------------------------------------------------------------

# Nuke the bash tool-init cache (zoxide / atuin / starship)
kbashcache() {
  rm -f ~/.cache/bash/*.bash
  echo "bash caches cleared - re-source to rebuild"
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
  printf "\n\033[1;35mCustom Bash Tools & Aliases\033[0m\n\n"

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
  ' ~/.bashrc $([[ -f ~/.bash_aliases ]] && echo ~/.bash_aliases)

  echo ""
}


# -------------------------------------------------------------
# 12. Prompt (loaded late)
# -------------------------------------------------------------

_bcache "starship"


# -------------------------------------------------------------
# 13. Late hooks (must come after everything else)
# -------------------------------------------------------------

# bun completions
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# Theme init - applies the correct light/dark tmux+nvim theme to new
# terminal windows. Live theme switching is handled by the dark-notify
# launchd agent on macOS.
if [[ "$OSTYPE" == "darwin"* ]]; then
  "$HOME/.local/bin/theme-switch.sh" auto
else
  "$HOME/.local/bin/theme-switch.sh" light
fi
