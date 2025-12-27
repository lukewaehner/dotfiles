# Dotfiles

My personal configuration files, managed with [GNU Stow](https://www.gnu.org/software/stow/) and [Homebrew](https://brew.sh/).

## Installation

### Automated Bootstrap (macOS)

The included `bootstrap.sh` script handles everything: installs Homebrew, bundles dependencies, sets up languages (Rust, Python, Ruby), and stows dotfiles.

```bash
# Clone the repository
git clone https://github.com/lukewaehner/dotfiles.git ~/repos/dotfiles

# Run the bootstrap script
cd ~/repos/dotfiles
./bootstrap.sh
```

### Manual Steps

If you prefer to run things manually:

1.  **Install Homebrew & Bundle**:

    ```bash
    brew bundle --file=brew/Brewfile
    ```

2.  **Stow Configurations**:
    ```bash
    stow --restow zsh git nvim starship atuin ghostty
    ```

## Key Tools

- **Shell**: `zsh` with [Oh My Zsh](https://ohmyz.sh/) (customized) + [Starship](https://starship.rs/) prompt.
- **Package Management**: Homebrew (`brew` & `cask`) + `mas`.
- **Navigation**: `zoxide` (smart cd), `eza` (better ls), `bat` (better cat).
- **Editor**: Neovim (`nvim`) & VS Code.
- **Terminal**: `ghostty` / `iterm2`.
- **Search**: `fzf`, `ripgrep` (`rg`), `fd`.
- **Dev**: `git`, `gh`, `lazygit`, `tmux`, `zellij`.

## Structure

- **`bootstrap.sh`**: Main setup script.
- **`brew/`**: Contains the `Brewfile` defining all system packages, casks, and VS Code extensions.
- **`zsh/`**: Zsh configuration (`.zshrc`, `.zprofile`, `.zshenv`).
- **`git/`**: Git config.
- **`nvim/`**: Neovim configuration.
- **`starship/`**: Starship prompt config.
- **`ghostty/`**: Ghostty terminal config.

## Aliases & Functions

A few notable shortcuts (see `.zshrc` for full list):

- `cd` → `z` (Zoxide)
- `ls` → `eza`
- `lg` → `lazygit`
- `fp` → Fuzzy find file & preview with `bat`
- `spinvm` / `stopvm` → Control Linux VM in UTM

## Updates

To update Brew packages and system tools:

```bash
brew update && brew upgrade
```

To refresh dotfiles links:

```bash
stow --restow */
```
