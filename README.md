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
stow --restow zsh git nvim starship atuin ghostty bat eza

# Install npm globals
npm i -g $(cat npmglobal.txt | tr '\n' ' ')

# Build bat theme cache
bat cache --build
```

## Repository Structure

```
dotfiles/
├── bootstrap.sh          # One-shot macOS setup script
├── npmglobal.txt         # npm global packages list
├── brew/
│   └── Brewfile          # Homebrew formulae, casks, and VS Code extensions
├── zsh/
│   ├── .zshrc            # Interactive shell configuration
│   ├── .zprofile         # Login environment (PATH, exports)
│   └── .zshenv           # Minimal env for all shells
├── git/
│   ├── .gitconfig        # Git user, defaults, and aliases
│   └── .gitignore_global # Global gitignore (.DS_Store, etc.)
├── nvim/
│   └── .config/nvim/     # Neovim config (LazyVim framework)
│       ├── init.lua
│       ├── lua/config/   # Options, keymaps, autocmds, completion
│       └── lua/plugins/  # Plugin specs (themes, LSP, git, DAP, etc.)
├── ghostty/
│   └── .config/ghostty/  # Ghostty terminal config
├── starship/
│   └── .config/starship.toml  # Starship prompt (Catppuccin Mocha)
├── atuin/
│   └── .config/atuin/    # Atuin shell history config
├── bat/
│   └── .config/bat/      # Bat themes (TokyoNight Day/Night)
└── eza/
    └── .config/eza/      # Eza color theme
```

Each top-level directory is a Stow package. Running `stow <package>` symlinks its contents into `$HOME`, mirroring the internal directory structure.

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
- **Opacity:** 30% with background blur
- **Theme:** System-aware (Zenbones Dark / Seoulbones Light)
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

### Shell History (Atuin)

Fuzzy search mode, secrets filtering enabled (blocks AWS keys, tokens, etc.), sync v2.

### Brewfile

~200+ items covering formulae, casks, and VS Code extensions. Includes language toolchains (Node, Python, Ruby, Rust, Go, Java), databases (PostgreSQL, MongoDB), and dev tools.

### NPM Globals

```
@google/clasp  eslint  npm-check-updates  pnpm
prettier       tsx     typescript          yarn
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

# Re-stow after adding/changing modules
stow --restow */

# Rebuild bat themes after changes
bat cache --build
```
