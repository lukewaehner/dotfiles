# Lightweight Vim Config Design

**Date:** 2026-05-27
**Status:** Approved

## Goal

A single `.vimrc` for plain Vim 8/9 (no Lua, no Neovim) that is RAM-efficient enough for low-power systems while preserving the core editing workflow from the neovim/LazyVim config. Managed by GNU Stow from `dotfiles/vim/.vimrc`.

## Non-Goals

- LSP (no language server process stays alive)
- Copilot / AI completion
- DAP / debugging UI
- Test runner (neotest equivalent)
- Ruby-specific plugins
- Treesitter-quality syntax highlighting
- Harpoon (replaced by vim built-in marks)

## File Structure

```
dotfiles/
└── vim/
    └── .vimrc            ← stowed to ~/.vimrc
```

No subdirectory split. Everything lives in `.vimrc` organized into sections:
- `PLUGINS` — vim-plug block
- `OPTIONS` — set commands
- `THEME` — colorscheme + true color
- `PLUGIN CONFIG` — per-plugin settings
- `KEYMAPS` — all custom mappings
- `AUTOCMDS` — filetype and event hooks
- `FILE RUNNER` — vimscript run function

## Plugin List (8 plugins)

| Plugin | Purpose |
|---|---|
| `junegunn/fzf` | Fuzzy engine binary wrapper |
| `junegunn/fzf.vim` | `:Files` and `:Rg` commands |
| `tpope/vim-fugitive` | Git client — `:G`, `:G blame` |
| `airblade/vim-gitgutter` | Gutter signs, hunk nav, stage/undo/preview |
| `christoomey/vim-tmux-navigator` | `<C-h/j/k/l>` across vim + tmux |
| `dense-analysis/ale` | Async lint/fix on save (ruff for Python) |
| `sheerun/vim-polyglot` | Lazy-loaded syntax for Rust, TS, and others |
| `folke/tokyonight.nvim` | Colorscheme — vim-compatible port |

vim-plug itself is installed by a bootstrap curl command (see install notes).

## Options

Ported from LazyVim defaults:

- `number` + `relativenumber`
- `expandtab`, `shiftwidth=2`, `tabstop=2`
- `smartindent`
- `ignorecase` + `smartcase`
- `splitright` + `splitbelow`
- `clipboard=unnamedplus`
- `scrolloff=8`
- `updatetime=100` (makes gitgutter signs feel instant)
- `hidden` (allow switching buffers without saving)
- `termguicolors` (true color — requires vim 8+ and a modern terminal)
- `signcolumn=yes` (always show gutter so it doesn't shift layout)
- `incsearch` + `hlsearch`
- `wildmenu` + `wildmode=longest:full,full`

## Colorscheme

`folke/tokyonight.nvim` — has a vim-compatible port. Style: `night`, transparent background. Same visual as neovim config. Falls back gracefully if `termguicolors` is unavailable.

## Keymaps

### Core (mirroring neovim config)

| Key | Action |
|---|---|
| `<Space>` | Leader key |
| `<leader>ff` | `:Files<CR>` |
| `<leader>sg` | `:Rg<CR>` |
| `<leader>tf` | Open `:terminal` in horizontal split |
| `<leader>tr` | Run current file (see File Runner) |
| `<C-h/j/k/l>` | vim-tmux-navigator (identical to neovim) |

### Git (gitgutter + fugitive)

| Key | Action |
|---|---|
| `]h` | Next hunk |
| `[h` | Prev hunk |
| `<leader>hs` | Stage hunk |
| `<leader>hr` | Undo hunk |
| `<leader>hp` | Preview hunk |
| `<leader>hb` | `:G blame` (fugitive) |

### File navigation

Harpoon is replaced by vim's built-in marks. No plugin needed:

| Key | Action |
|---|---|
| `<leader>a` | `ma` — mark slot a (mnemonic match) |
| `<M-1>` | `'a` — jump to mark a |
| `<M-2>` | `'b` — jump to mark b |
| `<M-3>` | `'c` — jump to mark c |
| `<M-4>` | `'d` — jump to mark d |

### Misc

| Key | Action |
|---|---|
| `<leader>sr` | `:vimgrep // **<Left><Left><Left><Left>` — project search into quickfix |
| `<Esc>` | `:nohlsearch<CR>` — clear search highlight |

## ALE Config

Async linting only on file save. No LSP, no inline completion.

```vim
let g:ale_linters = { 'python': ['ruff'] }
let g:ale_fixers  = { 'python': ['ruff_format'], '*': ['remove_trailing_lines'] }
let g:ale_fix_on_save = 1
let g:ale_lint_on_text_changed = 'never'
let g:ale_lint_on_enter = 0
let g:ale_lsp_suggestions = 0
let g:ale_sign_error = '✗'
let g:ale_sign_warning = '▲'
```

## File Runner

A vimscript function that:
1. Saves the current file
2. Looks up the filetype in a command table
3. Rust: walks up to find `Cargo.toml`, runs `cargo run`
4. Go: walks up to find `go.mod`, runs `go run .`
5. Others: runs directly on the file
6. Opens result in a `:terminal` horizontal split at the bottom

Languages: Python, C, C++, Go, Rust, JavaScript, TypeScript, Lua, Bash.

Bound to `<leader>tr`. No "pick target" variant (the `<leader>tR` force-pick is dropped — too complex for vimscript without UI primitives).

## Status Line

No plugin. Vimscript `statusline` configured to show: filename, modified flag, filetype, ALE error/warning counts, line/col, and percentage. Looks clean without the overhead of airline or lightline.

## Completion

Built-in only: `<C-n>` / `<C-p>` for keyword completion, `<C-x><C-f>` for path completion. No completion plugin — keeps insert mode fast.

## System Requirements

The target system must have:
- `vim` 8.0+ (for `:terminal` and async jobs)
- `fzf` binary
- `ripgrep` (`rg` binary) — for `:Rg`
- `git` — for fugitive + gitgutter
- Internet access once for `vim-plug` install + `:PlugInstall`

Optional (for Python lint):
- `ruff` binary

## Install Notes

Bootstrap one-liner (installs vim-plug):
```sh
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

Then open vim and run `:PlugInstall`.
