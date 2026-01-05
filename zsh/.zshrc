# Check for zshrdc changes and recompile
if [[ -s ~/.zshrc && ( ! -s ~/.zshrc.zwc || ~/.zshrc -nt ~/.zshrc.zwc ) ]]; then
  zcompile ~/.zshrc
fi

# Early exit if non-interactive
[[ -o interactive ]] || return

# Zsh Completion Cache
zstyle ':completion:*' use-cache yes
zstyle ':completion:*' cache-path ~/.zcompcache
mkdir -p ~/.zcompcache

# -------------------------------------------------------------
# Zsh core init
# -------------------------------------------------------------

# Completion system (fast, no security re-scan)

# Case-insensitive + smart completion
zstyle ':completion:*' matcher-list \
  'm:{a-zA-Z}={A-Za-z}' \
  'r:|[._-]=* r:|=*'

autoload -Uz compinit
compinit -C

# Autosuggestions
[[ -r /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]] && \
  source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# -------------------------------------------------------------

# Prefer nvim for man
export MANPAGER="nvim +Man!"

# -------------------------------------------------------------
# Important Version Managers
# -------------------------------------------------------------

eval "$(rbenv init - zsh)"

# -------------------------------------------------------------
# VM Functions 
# -------------------------------------------------------------
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

# Companion function to stop VM
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

# Autosuggestion + syntax colors (more visible in light/dark)
typeset -A ZSH_HIGHLIGHT_STYLES
ZSH_HIGHLIGHT_STYLES[command]='fg=cyan'
ZSH_HIGHLIGHT_STYLES[builtin]='fg=blue'
ZSH_HIGHLIGHT_STYLES[alias]='fg=magenta'
ZSH_HIGHLIGHT_STYLES[path]='fg=yellow'

# -------------------------------------------------------------
# Dark / Light Mode Settings
# -------------------------------------------------------------

# NOTE: Dark / Light mode settings are added here

# Single check for darkmode
_is_dark_mode() {
  [[ $(defaults read -g AppleInterfaceStyle 2>/dev/null) == "Dark" ]]
}

if _is_dark_mode; then
  # ZSH Autosuggest
  ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#777777'
  # Bat theme
  export BAT_THEME="TokyoNight Night"
else
  ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#333333'
  export BAT_THEME="TokyoNight Day"
fi

# Removed function after use
unset -f _is_dark_mode

# -------------------------------------------------------------
# Modern Unix Tools
# -------------------------------------------------------------

# NOTE: Add other tools here as needed for quick loading

# Create a cache directory
[[ -d ~/.cache/zsh ]] || mkdir -p ~/.cache/zsh

# Caching function
# NOTE: Do not cache things with important changes (rbenv, pyenv, etc)
zcache() {
  local cache_file="$HOME/.cache/zsh/$1.zsh"

  if [[ ! -f "$cache_file" ]]; then
    case $1 in
      zoxide)   zoxide init zsh > "$cache_file" ;;
      atuin)    atuin init zsh > "$cache_file" ;;
      starship) starship init zsh > "$cache_file" ;;
      *) return ;;
    esac
  fi

  [[ -f "$cache_file" ]] && source "$cache_file"
}

zcache "zoxide"
zcache "atuin"

# -------------------------------------------------------------
# Aliases
# -------------------------------------------------------------

# Re-map cd to z
alias cd="z"

# Re-map lg to lazygit
alias lg="lazygit"

# Eza
alias ls="eza --icons --group-directories-first"
alias ll="eza -lgh --icons --git --group-directories-first"
alias lt="eza --tree --level=2 --icons"

# Lazy fuck usage
alias fuck='eval $(thefuck $(fc -ln -1))'

# Sort Downloads custom command
alias sort-downloads="~/Code/Python/sort-downloads/main.py"

# -------------------------------------------------------------
# Exports
# -------------------------------------------------------------

# Use fd for fzf (ignores node_modules/git)
export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# fzf palette (prompt/header pointers)
export FZF_DEFAULT_OPTS='--color=fg+:7,bg:-1,hl:4,hl+:4,info:6,prompt:5,spinner:5,pointer:5,marker:2,header:6'

# -------------------------------------------------------------
# Functions
# --------------------------------------------------------------

# Type 'fp' to fuzzy find a file and preview its contents with 'bat'
fp() {
  fzf --preview 'bat --style=numbers --color=always --line-range :500 {}'
}

# -------------------------------------------------------------
# Prompt, load at end
# --------------------------------------------------------------

# Auto-detect system theme for Starship and set palette
export STARSHIP_PALETTE="catppuccin_mocha"
zcache "starship"

# -------------------------------------------------------------

# Syntax highlighting - very end to see full state
[[ -r /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && \
  source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# -------------------------------------------------------------

