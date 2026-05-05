# Design: Expand setup-linux.sh

**Date:** 2026-05-05
**Scope:** Expand `setup-linux.sh` from tmux-only to a full Linux dev environment bootstrap, targeting Debian/Ubuntu with bash as the shell.

---

## Goal

Run one script on a fresh Linux machine and get a fully configured dev environment: neovim, starship, atuin, zoxide, eza, lazygit, fzf, ripgrep, fd, bat, gh — all with dotfiles stowed and a bash config that mirrors the macOS `.zshrc` experience.

---

## Architecture

Single script (`setup-linux.sh`) expanded with new numbered sections. Existing sections (tmux, theme-switch, reload) are unchanged. New sections insert above the existing tmux block.

### Script section order

| # | Section | Method |
|---|---------|--------|
| 0 | System packages (apt) | Existing — add `stow`, `direnv`, `jq` |
| 0a | GitHub CLI | GitHub's official apt repo (separate, needs key+source) |
| 1 | Neovim | `snap install nvim --classic` |
| 2 | Curl-installed tools | starship, atuin, zoxide — official install scripts |
| 3 | Binary tools | eza (apt on Ubuntu 24+, else GitHub release), lazygit (GitHub release) |
| 4 | Stow dotfile modules | `atuin bat eza git nvim starship scripts` |
| 5 | `~/.bashrc` block | Append once, guarded by marker |
| 6–9 | Existing tmux sections | Unchanged |

### Stowed modules

- `atuin` → `~/.config/atuin/config.toml`
- `bat` → `~/.config/bat/themes/`
- `eza` → `~/.config/eza/theme.yml`
- `git` → `~/.gitconfig`, `~/.gitignore_global`
- `nvim` → `~/.config/nvim/`
- `starship` → `~/.config/starship.toml`
- `scripts` → `~/.local/bin/theme-switch.sh`
- `tmux` — stays manual (needs `expand_theme` processing, not a straight symlink)

### `~/.bashrc` block

Appended once, guarded with `# ── dotfiles ──` marker to make re-runs idempotent.

**Ported from `.zshrc` / `.zprofile`:**

| Item | Notes |
|------|-------|
| PATH | `~/.local/bin`, `~/.cargo/bin`, `~/.pyenv/{bin,shims}`, `~/.rbenv/{bin,shims}` |
| `MANPAGER` | `nvim +Man!` |
| `BAT_THEME` | Hardcoded `TokyoNight Night` (no auto-detect on Linux) |
| `STARSHIP_PALETTE` | `catppuccin_mocha` |
| FZF exports | `FZF_DEFAULT_COMMAND`, `FZF_CTRL_T_COMMAND`, `FZF_DEFAULT_OPTS` |
| eza aliases | `ls`, `ll`, `lt` |
| General aliases | `lg=lazygit`, `cd=z`, `t=tmux new-session -A -s main` |
| `fp()` | fzf file preview with bat |
| `cdd()` | cd via fd+fzf |
| `cdf()` | cd to file's dir via fzf |
| Lazy rbenv | bash version: `unset -f` + `eval` loop |
| `_dotcache` | Same cached-init pattern as `zcache` in `.zshrc` |
| zoxide init | `_dotcache zoxide` |
| atuin init | `_dotcache atuin` (with `--disable-up-arrow`) |
| starship init | `_dotcache starship` (last, after other inits) |
| fzf keybindings | Source `/usr/share/doc/fzf/examples/key-bindings.bash` |
| bash-completion | Source `/usr/share/bash-completion/bash_completion` |
| `theme-switch dark` | Called on login (Linux always uses dark) |

**Skipped (macOS/zsh-only):**
- Homebrew paths
- `defaults read` dark mode detection
- VM management functions (`startvm`, `stopvm`, `vmstatus`)
- `thefuck` alias
- bun completions
- zsh completion system (`compinit`, `zstyle`)
- `zsh-autosuggestions` / `zsh-syntax-highlighting`
- Postgres.app, Solana, Elan paths
- `sort-downloads` alias

---

## Tool install strategies

| Tool | Method | Rationale |
|------|--------|-----------|
| neovim | `snap install nvim --classic` | Always latest, simple |
| starship | `curl starship.rs/install.sh \| sh -s -- --yes` | Official, idempotent |
| atuin | `curl setup.atuin.sh \| sh` | Official, idempotent |
| zoxide | `curl ajeetdsouza/zoxide install.sh \| sh` | Official, idempotent |
| eza | apt if available, else GitHub release binary | apt on Ubuntu 24+; fallback for older |
| lazygit | GitHub release tarball → `~/.local/bin` | Not in apt |
| gh | GitHub's official apt repo | Stable, managed |

---

## Idempotency

- apt installs: idempotent by nature
- snap: `snap install` skips if already installed
- curl scripts: all three check for existing install and skip/upgrade
- eza/lazygit binary: overwrite is fine (same binary)
- stow: `--restow` flag makes it safe to re-run
- `~/.bashrc` block: guarded by `# ── dotfiles ──` marker, not appended twice

---

## Out of scope

- Language toolchains (pyenv, rbenv, Rust) — not installed by this script; PATH entries are added so they work if the user installs them separately
- Non-Debian distros
- GUI tools
- zsh (bash only on Linux)
