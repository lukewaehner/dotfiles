# Neovim Config Improvements Design

## Scope

Five targeted improvements to an existing LazyVim-based Neovim config. User primarily writes Python, Ruby, and Rust on macOS.

---

## 1. Neotest (Testing Framework)

**Goal:** Run and inspect tests without leaving Neovim.

**Plugins:**
- `nvim-neotest/neotest` (core)
- `nvim-neotest/neotest-python` (pytest adapter)
- `olimorris/neotest-rspec` (RSpec adapter)

**File:** `lua/plugins/neotest.lua`

**Keymaps** (using `<leader>n` prefix to avoid `<leader>t` conflict with toggleterm):
- `<leader>nt` — run nearest test
- `<leader>nf` — run current file
- `<leader>ns` — toggle summary panel
- `<leader>no` — show output for nearest test

**Config notes:**
- Python adapter configured to use `pytest`
- RSpec adapter uses defaults (works with `bundle exec rspec`)
- Summary opens in a side panel

---

## 2. Fix `lua_ls = false` in `swift-lsp.lua`

**Problem:** `lua_ls = false` disables Lua LSP globally — meaning no LSP while editing the Neovim config itself.

**Fix:** Remove the `lua_ls = false` line from `lua/plugins/swift-lsp.lua`. It was likely added to prevent lua_ls conflicting with Swift files, but sourcekit is already scoped to `filetypes = { "swift" }` so the conflict doesn't exist.

---

## 3. DAP Keymaps

**Goal:** Make the existing DAP + dap-ui setup actually drivable.

**File:** Extend `lua/plugins/dap.lua` with a `keys` block on `nvim-dap`.

**Keymaps** (Mac-friendly — avoids F-keys which require `Fn` on MacBooks):
- `<leader>dc` — continue / start
- `<leader>db` — toggle breakpoint
- `<leader>dB` — conditional breakpoint
- `<leader>do` — step over
- `<leader>di` — step into
- `<leader>dO` — step out
- `<leader>du` — toggle dap-ui
- `<leader>dr` — open REPL
- `<leader>dl` — run last

---

## 4. Move cmp Config Out of `keymaps.lua`

**Problem:** The `cmp.setup()` call with custom mappings lives in `keymaps.lua`, which is semantically wrong and makes it hard to find.

**Fix:**
- Create `lua/plugins/cmp.lua` with the existing mapping (CR doesn't confirm, `<C-l>` confirms)
- Remove the cmp block from `keymaps.lua`

---

## 5. Copilot Ghost Text

**Goal:** Enable inline ghost text suggestions (fish-shell style) while typing code.

**Approach:** Configure `copilot.lua` (already installed via LazyVim extras) with `suggestion.auto_trigger = true` and add a keymap to accept suggestions. Also enable `experimental.ghost_text` in nvim-cmp so the two don't fight.

**File:** `lua/plugins/copilot.lua` (new)

**Keymaps:**
- `<Tab>` — accept copilot suggestion (if visible)
- `<M-l>` — accept word
- `<M-]>` / `<M-[>` — next / prev suggestion

**Note:** Since `<C-l>` already confirms cmp, we keep that and use `<Tab>` purely for copilot acceptance (only fires when a suggestion is shown).
