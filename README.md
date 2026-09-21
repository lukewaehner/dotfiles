# Dotfiles

Personal macOS configuration files, managed with [GNU Stow](https://www.gnu.org/software/stow/) and [Homebrew](https://brew.sh/).

## Installation

### Automated Bootstrap (macOS)

The `bootstrap.sh` script handles the full setup: installs Xcode CLT, Homebrew, bundles all dependencies, sets up language toolchains (Rust, Python, Ruby), stows dotfiles, installs npm globals, and builds the bat theme cache.

```bash
git clone https://github.com/lukewaehner/dotfiles.git ~/repos/dotfiles
cd ~/repos/dotfiles
./bootstrap.sh
```

### Manual Setup

```bash
# Install packages from Brewfile
brew bundle --file=brew/Brewfile

# Stow all configuration modules into $HOME
# (every top-level directory except brew/ and macos/, which aren't stow packages)
stow --restow zsh bash git nvim vim zed ghostty wezterm tmux herdr \
  starship atuin bat eza lazygit mactop aerospace scripts ptpython \
  claude antigravity raycast

# Install npm globals
npm i -g $(cat npmglobal.txt | tr '\n' ' ')

# Install Python globals into every pyenv version
for v in $(pyenv versions --bare | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$'); do
  "$PYENV_ROOT/versions/$v/bin/python" -m pip install --upgrade \
    $(grep -vE '^\s*(#|$)' pyglobal.txt | tr '\n' ' ')
done
pyenv rehash

# Build bat theme cache
bat cache --build
```

## Repository Structure

```
dotfiles/
├── bootstrap.sh          # One-shot macOS setup script
├── setup-linux.sh        # Equivalent setup for Linux hosts
├── npmglobal.txt         # npm global packages list
├── pyglobal.txt          # Python CLI tools, installed per pyenv version
├── .stowrc               # Stow defaults (--target=~)
│
│   # Shell
├── zsh/
│   ├── .zshrc            # Interactive shell configuration
│   ├── .zsh_aliases      # Aliases and functions
│   ├── .zprofile         # Login environment (PATH, exports)
│   └── .zshenv           # Minimal env for all shells
├── bash/
│   ├── .bashrc           # Linux/fallback shell, bridged to the zsh config
│   ├── .bash_aliases
│   └── .bash_profile
├── starship/
│   └── .config/starship.toml  # Starship prompt (Catppuccin Mocha)
├── atuin/
│   └── .config/atuin/    # Atuin shell history config
│
│   # Terminals and multiplexers
├── ghostty/
│   └── .config/ghostty/  # Ghostty terminal config and themes
├── wezterm/
│   └── .config/wezterm/  # WezTerm config
├── tmux/
│   └── .config/tmux/     # tmux config, themes, and theme-switch hook
├── herdr/
│   └── .config/herdr/    # herdr multiplexer config and plugins
│
│   # Editors
├── nvim/
│   └── .config/nvim/     # Neovim config (LazyVim framework)
│       ├── init.lua
│       ├── lua/config/   # Options, keymaps, autocmds, completion
│       └── lua/plugins/  # Plugin specs (themes, LSP, git, DAP, etc.)
├── vim/
│   └── .vimrc            # Plain vim fallback
├── zed/
│   └── .config/zed/      # Zed settings and keymap
│
│   # AI assistants
├── claude/
│   ├── .claude/          # Claude Code rules, skills, commands, agents, hooks
│   └── .agents/          # Shared skill set
├── antigravity/
│   └── .gemini/config/   # Antigravity rules and skills (mirrors claude/)
│
│   # CLI tools
├── git/
│   ├── .gitconfig        # Git user, defaults, and aliases
│   └── .gitignore_global # Global gitignore (.DS_Store, etc.)
├── bat/
│   └── .config/bat/      # Bat themes (TokyoNight Day/Night)
├── eza/
│   └── .config/eza/      # Eza color theme
├── lazygit/
│   └── .config/lazygit/  # Lazygit config and themes
├── mactop/
│   └── .mactop/          # mactop system monitor config
├── ptpython/
│   └── .config/ptpython/ # ptpython REPL config (vi mode)
│
│   # macOS desktop
├── aerospace/
│   └── .config/aerospace/  # AeroSpace tiling window manager
├── scripts/
│   └── .local/bin/       # theme-switch, appearance-watcher, sync-claude-settings
├── raycast/              # Raycast script commands
│
│   # Consumed directly, not stowed
├── brew/
│   └── Brewfile          # Homebrew formulae, casks, and VS Code extensions
└── macos/
    └── com.user.appearance-watcher.plist  # launchd agent, installed to
                                           # ~/Library/LaunchAgents by bootstrap.sh
```

Every top-level directory except `brew/` and `macos/` is a Stow package. Running `stow <package>` symlinks its contents into `$HOME`, mirroring the internal directory structure; `bootstrap.sh` stows them all, skipping those two.

## What's Configured

### Shell (zsh)

No framework -- plain zsh with a few Homebrew plugins:

- **zsh-autosuggestions** and **zsh-syntax-highlighting** via Homebrew
- Case-insensitive smart tab completion with caching
- Automatic `.zshrc` bytecode compilation (`zcompile`)
- Tool init caching (`zcache`) for zoxide, atuin, and starship to speed up shell startup
- System dark/light mode detection -- auto-switches bat theme and autosuggestion colors

### Prompt (Starship)

[Starship](https://starship.rs/) with the **Catppuccin Mocha** palette. Format: `username in directory on branch *`.

### Terminal (Ghostty)

- **Font:** JetBrainsMono Nerd Font, size 18
- **Opacity:** 85% with background blur (a 45% preset is commented in the config)
- **Theme:** System-aware (TokyoNight Night / TokyoNight Day)
- macOS native tab style, block cursor

### Editor (Neovim)

Built on [LazyVim](https://www.lazyvim.org/) with additional plugins:

| Plugin | Purpose |
|---|---|
| zenbones / tokyonight | Color schemes (dark/light) |
| auto-dark-mode | Follows macOS appearance |
| gitsigns | Git hunks, blame, staging |
| harpoon | Quick file marks |
| toggleterm | Floating terminal + compile/run |
| conform | Formatter integration (rubocop, etc.) |
| vim-rails / vim-ruby | Ruby/Rails support |
| swift-lsp | Swift LSP |
| dap + codelldb | C/C++ debugging |
| dash | Documentation lookup |
| leetcode | LeetCode practice |

### Git

```
user: Luke Waehner
default branch: main
pull strategy: merge
auto-setup remote: true
```

### CLI Tools

| Tool | Replaces | Notes |
|---|---|---|
| [zoxide](https://github.com/ajeetdsouza/zoxide) | `cd` | Smart directory jumping |
| [eza](https://github.com/eza-community/eza) | `ls` | Icons, git status, tree view |
| [bat](https://github.com/sharkdp/bat) | `cat` | Syntax highlighting, TokyoNight themes |
| [fd](https://github.com/sharkdp/fd) | `find` | Used by fzf for file discovery |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | `grep` | Fast regex search |
| [fzf](https://github.com/junegunn/fzf) | -- | Fuzzy finder with custom color palette |
| [lazygit](https://github.com/jesseduffield/lazygit) | -- | Terminal git UI |
| [atuin](https://github.com/atuinsh/atuin) | `history` | Fuzzy shell history with sync |
| [thefuck](https://github.com/nvbn/thefuck) | -- | Command correction |
| [ptpython](https://github.com/prompt-toolkit/ptpython) | `python` REPL | Vi mode, completion, signatures |

### Shell History (Atuin)

Fuzzy search mode, secrets filtering enabled (blocks AWS keys, tokens, etc.), sync v2.

### Python REPL (ptpython)

Vi editing with a modal cursor, multi-column fuzzy completion, dict-key
completion, jedi signatures and docstrings, auto-suggest from history, and a
pager for tall output. Picks its Pygments theme from the current macOS
appearance at startup, since ptpython can't be re-themed live.

Not in the Brewfile. It's listed in `pyglobal.txt` and installed into every
pyenv-managed Python by `bootstrap.sh`, so the `ptpython` shim resolves no
matter which version is active -- and the REPL sees that version's packages.
A project virtualenv gets its own copy (`pip install ptpython`) or runs the
base interpreter's with `python -m ptpython`.

On macOS ptpython looks for its config in `~/Library/Application Support/`
rather than XDG, so the shell rc files export
`PTPYTHON_CONFIG_HOME=$HOME/.config/ptpython` to point it at the stowed file.

### Brewfile

~200+ items covering formulae, casks, and VS Code extensions. Includes language toolchains (Node, Python, Ruby, Rust, Go, Java), databases (PostgreSQL, MongoDB), and dev tools.

### NPM Globals

```
@google/clasp  eslint  npm-check-updates  pnpm
prettier       tsx     typescript          yarn
```

### Python Globals

`pyglobal.txt`, installed into each pyenv version rather than once globally:

```
ptpython
```

## Aliases & Functions

### Aliases

| Alias | Expands To |
|---|---|
| `cd` | `z` (zoxide) |
| `ls` | `eza --icons --group-directories-first` |
| `ll` | `eza -lgh --icons --git --group-directories-first` |
| `lt` | `eza --tree --level=2 --icons` |
| `lg` | `lazygit` |
| `fuck` | thefuck correction |

### Functions

| Function | Description |
|---|---|
| `fp` | Fuzzy-find a file and preview with bat |
| `cdd` | Fuzzy-find a directory and cd into it |
| `cdf` | Fuzzy-find a file and cd to its directory |
| `startvm` | Start UTM Linux VM and SSH in |
| `stopvm` | Shut down the UTM Linux VM |
| `vmstatus` | Check UTM and VM status |

## Language Toolchains

Managed via version managers, installed by `bootstrap.sh`:

- **Python** -- pyenv (3.9.6 default + latest stable)
- **Ruby** -- rbenv (latest stable)
- **Rust** -- rustup (stable)
- **Node.js** -- nvm (via Brewfile)
- **Go, Java (OpenJDK 17)** -- via Homebrew

## Updating

```bash
# Update Homebrew packages
brew update && brew upgrade

# Re-stow after adding/changing a module
stow --restow <package>

# Rebuild bat themes after changes
bat cache --build
```
