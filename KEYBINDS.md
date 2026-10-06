# Keybinds

Cheat sheet for tmux, workmux and Zed. Sources of truth:
`tmux/.config/tmux/tmux.conf`, `workmux/.config/workmux/config.yaml`,
`zed/.config/zed/keymap.json` — update this file when those change.

## tmux

Prefix is **`C-Space`**. Everything below is `prefix` + key unless marked
*(no prefix)*.

### Sessions

| Key | Action |
|---|---|
| `T` | sesh picker (see below) |
| `o` | sessionx picker (see below) |
| `s` | Session tree |
| `c` | New session (unnamed) |
| `$` | Rename session |
| `d` | Detach |
| `C-s` / `C-r` | Save / restore sessions (tmux-resurrect) |

### Windows

| Key | Action |
|---|---|
| `N` | New window |
| `n` | Next window |
| `Tab` | Last window |
| `1`–`5` | Go to window 1–5 |
| `w` | Window tree |
| `X` | Kill window (asks first) |

### Panes

| Key | Action |
|---|---|
| `\` | Split side by side |
| `-` | Split top / bottom |
| `h` `j` `k` `l` | Move between panes |
| `C-h` `C-j` `C-k` `C-l` *(no prefix)* | Move between panes **and** nvim splits |
| `H` `J` `K` `L` | Resize by 5 (repeatable) |
| `z` | Zoom pane |
| `=` / `+` | Even horizontal / even vertical layout |
| `x` | Kill pane (no confirmation) |

### Popups & tools

| Key | Action |
|---|---|
| `g` | Scratch shell popup (persistent; `g` again closes it) |
| `C-g` | lazygit popup |
| `e` | Config menu → `z` .zshrc · `p` .zprofile · `t` tmux.conf · `v` nvim |
| `r` | Reload tmux config |

### Copy mode

| Key | Action |
|---|---|
| `Enter` | Enter copy mode |
| `v` | Start selection |
| `r` | Toggle rectangle selection |
| `y` | Copy and exit |
| `Y` | Copy to macOS clipboard (pbcopy) and exit |
| `P` | Paste |

### sesh picker (`prefix T`)

| Key | Action |
|---|---|
| `Tab` / `S-Tab` | Down / up |
| `C-a` | All |
| `C-t` | Running tmux sessions |
| `C-g` | sesh configs |
| `C-x` | zoxide dirs |
| `C-f` | Find dirs under `~` |
| `C-d` | Kill selected session |
| `Enter` | Connect (creates the session if needed) |

### sessionx picker (`prefix o`)

| Key | Action |
|---|---|
| `Enter` | Switch — or create a session if the name is new |
| `Esc` | Close |
| `C-n` / `C-p` | Down / up |
| `C-d` / `C-u` | Scroll preview |
| `alt-Bksp` | Kill session |
| `C-r` | Rename session |
| `C-w` | Window list (all sessions) |
| `C-t` | Tree view |
| `C-e` | Dirs under current dir → new session |
| `C-f` | zoxide dirs → new session |
| `C-x` | Dirs under `~/.config` → new session |
| `C-b` | Back to session list |

## workmux

One git worktree + tmux window per task, Claude in the focused pane.

| Key | Action |
|---|---|
| `prefix W` | New worktree + window (prompts for branch) |
| `prefix a` | Agents dashboard popup |
| `prefix A` | Jump to agent that finished / needs me (repeat to cycle) |
| `prefix C-t` | Toggle agent sidebar |

Tab markers: **`W`** working · **`Q`** waiting on me (question or
permission prompt) · **`D`** done.

| Command | Action |
|---|---|
| `wm add <branch>` | Worktree + window (branched from main) |
| `wm merge` | Rebase onto main, then remove worktree, window and branch |
| `wm rm` | Clean up without merging (PR workflow) |
| `wm ls` | List worktrees |
| `wm open <name>` / `wm close <name>` | Reopen / close a worktree's window |

### Dashboard (`prefix a`)

| Key | Action |
|---|---|
| `j` / `k` | Down / up |
| `Enter` | Go to agent |
| `1`–`9` | Jump to agent |
| `p` | Peek (dashboard stays open) |
| `i` | Type to the agent |
| `d` | View diff |
| `Bksp` | Toggle current / last agent |
| `Tab` | Switch to worktrees view (`a` add · `r` remove · `c` close window) |
| `o` / `O` | Open PR / PR checks |
| `X` | Kill agent |
| `R` | Sweep merged / gone worktrees |
| `/` | Filter |
| `q` | Quit |

## Zed

Vim mode, `space` is leader (LazyVim-style). Normal / visual mode unless
noted.

### Find & navigate

| Key | Action |
|---|---|
| `space space` / `space f f` | Find file |
| `space /` / `space s g` | Search in project |
| `space S` | Search & replace in project |
| `space ,` | Open-buffer switcher |
| `space s s` | Symbol outline |
| `space f p` | Recent projects |
| `H` / `L` | Previous / next buffer |
| `ctrl-6` | Alternate file |
| `C-h` `C-j` `C-k` `C-l` | Move between panes (editor, explorer, terminal, git) |

### Code

| Key | Action |
|---|---|
| `K` | Hover |
| `g d` | Go to definition |
| `g v` | Go to definition in split |
| `g r` | References |
| `] d` / `[ d` | Next / previous diagnostic |
| `space c a` | Code actions |
| `space c r` | Rename symbol |
| `space c f` | Format |
| `space c d` | Diagnostics panel |
| `space c p` | Markdown preview to the side |
| `alt-j` / `alt-k` | Move line(s) down / up |
| `ctrl-y` *(completion menu)* | Accept completion |
| `ctrl-h` *(insert)* | Signature help |
| `ctrl-c` | Escape |

### Git

| Key | Action |
|---|---|
| `] h` / `[ h` | Next / previous hunk |
| `space h p` | Preview hunk diff |
| `space h s` | Stage / unstage hunk |
| `space h r` | Reset hunk |
| `space h b` | Blame |
| `space g g` | Git panel |

### Windows & UI

| Key | Action |
|---|---|
| `space e` | Toggle file explorer (right dock) |
| `space t f` | Terminal panel |
| `space \|` / `space -` | Split right / down |
| `space w m` | Zoom pane |
| `space b d` | Close buffer |
| `space u h` | Toggle inlay hints |
| `space u z` | Zen (centered) layout |

### File explorer

| Key | Action |
|---|---|
| `a` / `A` | New file / directory |
| `r` | Rename |
| `d` | Delete |
| `x` / `c` / `p` | Cut / copy / paste |
| `q` / `space e` | Close explorer |
