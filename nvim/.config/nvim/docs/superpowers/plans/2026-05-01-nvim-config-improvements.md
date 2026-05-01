# Neovim Config Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add neotest (pytest + rspec), fix lua_ls, wire DAP keymaps, relocate cmp config, and enable Copilot ghost text in a LazyVim-based Neovim config.

**Architecture:** Each change is a self-contained Lua plugin spec or config file modification. LazyVim's plugin override system means all changes merge cleanly with existing defaults — no destructive edits to LazyVim internals.

**Tech Stack:** Neovim + LazyVim, Lua, neotest, nvim-dap, nvim-cmp, copilot.lua

---

## File Map

| Action | File | Purpose |
|--------|------|---------|
| Create | `lua/plugins/neotest.lua` | neotest core + pytest + rspec adapters + keymaps |
| Modify | `lua/plugins/swift-lsp.lua` | Remove `lua_ls = false` (line 6) |
| Modify | `lua/plugins/dap.lua` | Add `keys` block to nvim-dap spec |
| Create | `lua/plugins/cmp.lua` | cmp CR/C-l mapping (moved from keymaps.lua) |
| Modify | `lua/config/keymaps.lua` | Remove the cmp.setup() block |
| Create | `lua/plugins/copilot.lua` | Copilot ghost text + Tab accept keymap |

---

### Task 1: Fix `lua_ls = false` in swift-lsp.lua

**Files:**
- Modify: `lua/plugins/swift-lsp.lua`

- [ ] **Step 1: Remove the offending line**

Open `lua/plugins/swift-lsp.lua`. The current content is:

```lua
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
	lua_ls = false,
        sourcekit = {
          cmd = { "sourcekit-lsp" },
          filetypes = { "swift" },
        },
      },
    },
  },
}
```

Change it to:

```lua
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        sourcekit = {
          cmd = { "sourcekit-lsp" },
          filetypes = { "swift" },
        },
      },
    },
  },
}
```

- [ ] **Step 2: Verify**

Open a `.lua` file in Neovim (e.g. `:e lua/config/keymaps.lua`).
Run `:LspInfo` — you should see `lua_ls` attached. Previously it would show nothing.

- [ ] **Step 3: Commit**

```bash
git add lua/plugins/swift-lsp.lua
git commit -m "fix: restore lua_ls — was accidentally disabled in swift-lsp config"
```

---

### Task 2: Move cmp Config Out of `keymaps.lua`

**Files:**
- Create: `lua/plugins/cmp.lua`
- Modify: `lua/config/keymaps.lua`

- [ ] **Step 1: Create `lua/plugins/cmp.lua`**

```lua
return {
  "hrsh7th/nvim-cmp",
  opts = function(_, opts)
    local cmp = require("cmp")
    opts.mapping = vim.tbl_extend("force", opts.mapping or {}, {
      ["<CR>"] = cmp.mapping(function(fallback)
        if cmp.visible() then
          cmp.close()
          vim.api.nvim_feedkeys(
            vim.api.nvim_replace_termcodes("<CR>", true, true, true),
            "n",
            true
          )
        else
          fallback()
        end
      end, { "i", "s" }),
      ["<C-l>"] = cmp.mapping.confirm({ select = true }),
    })
    return opts
  end,
}
```

- [ ] **Step 2: Remove the cmp block from `lua/config/keymaps.lua`**

Delete lines 5–19 (the entire cmp block). The file should start at the `WQ` user command. Final result:

```lua
-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- NOTE: Custom WQ to save all, close explorer, and quit
vim.api.nvim_create_user_command("WQ", function()
  vim.cmd("wa") -- write all modified buffers

  -- close neo-tree if available
  pcall(function()
    require("neo-tree.command").execute({ action = "close" })
  end)

  vim.cmd("qa") -- quit all
end, {})

vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    local bufnr = args.buf

    vim.defer_fn(function()
      -- Remove LazyVim's buffer-local "gr" (Snacks picker)
      pcall(vim.keymap.del, "n", "gr", { buffer = bufnr })

      -- Set buffer-local LSP references on "gr" (no nowait)
      vim.keymap.set("n", "gr", vim.lsp.buf.references, {
        buffer = bufnr,
        desc = "LSP References",
      })
    end, 0)
  end,
})
```

- [ ] **Step 3: Verify**

Open Neovim, enter insert mode in any buffer with completions, trigger a completion popup.
- `<CR>` should close the popup and insert a newline (not confirm the completion)
- `<C-l>` should confirm and accept the selected item

- [ ] **Step 4: Commit**

```bash
git add lua/plugins/cmp.lua lua/config/keymaps.lua
git commit -m "refactor: move cmp mapping config from keymaps.lua into plugin spec"
```

---

### Task 3: Wire DAP Keymaps

**Files:**
- Modify: `lua/plugins/dap.lua`

- [ ] **Step 1: Add keys block to the core nvim-dap spec**

Replace the first spec entry `{ "mfussenegger/nvim-dap" }` with:

```lua
{
  "mfussenegger/nvim-dap",
  keys = {
    { "<leader>dc", function() require("dap").continue() end,          desc = "DAP Continue" },
    { "<leader>db", function() require("dap").toggle_breakpoint() end, desc = "DAP Toggle Breakpoint" },
    { "<leader>dB", function()
        require("dap").set_breakpoint(vim.fn.input("Breakpoint condition: "))
      end, desc = "DAP Conditional Breakpoint" },
    { "<leader>do", function() require("dap").step_over() end,         desc = "DAP Step Over" },
    { "<leader>di", function() require("dap").step_into() end,         desc = "DAP Step Into" },
    { "<leader>dO", function() require("dap").step_out() end,          desc = "DAP Step Out" },
    { "<leader>dr", function() require("dap").repl.open() end,         desc = "DAP REPL" },
    { "<leader>dl", function() require("dap").run_last() end,          desc = "DAP Run Last" },
    { "<leader>du", function() require("dapui").toggle() end,          desc = "DAP Toggle UI" },
  },
},
```

The full `lua/plugins/dap.lua` should look like:

```lua
-- lua/plugins/dap.lua
return {
  -- Core DAP with keymaps
  {
    "mfussenegger/nvim-dap",
    keys = {
      { "<leader>dc", function() require("dap").continue() end,          desc = "DAP Continue" },
      { "<leader>db", function() require("dap").toggle_breakpoint() end, desc = "DAP Toggle Breakpoint" },
      { "<leader>dB", function()
          require("dap").set_breakpoint(vim.fn.input("Breakpoint condition: "))
        end, desc = "DAP Conditional Breakpoint" },
      { "<leader>do", function() require("dap").step_over() end,         desc = "DAP Step Over" },
      { "<leader>di", function() require("dap").step_into() end,         desc = "DAP Step Into" },
      { "<leader>dO", function() require("dap").step_out() end,          desc = "DAP Step Out" },
      { "<leader>dr", function() require("dap").repl.open() end,         desc = "DAP REPL" },
      { "<leader>dl", function() require("dap").run_last() end,          desc = "DAP Run Last" },
      { "<leader>du", function() require("dapui").toggle() end,          desc = "DAP Toggle UI" },
    },
  },

  -- Auto-install adapters (codelldb for C/C++)
  {
    "jay-babu/mason-nvim-dap.nvim",
    dependencies = { "mason-org/mason.nvim", "mfussenegger/nvim-dap" },
    opts = {
      ensure_installed = { "codelldb" },
      automatic_installation = true,
      handlers = {},
    },
  },

  -- UI + required dependency
  {
    "rcarriga/nvim-dap-ui",
    dependencies = {
      "mfussenegger/nvim-dap",
      "nvim-neotest/nvim-nio",
    },
    config = function()
      local dap, dapui = require("dap"), require("dapui")
      dapui.setup()
      dap.listeners.after.event_initialized["dapui"] = function()
        dapui.open()
      end
      dap.listeners.before.event_terminated["dapui"] = function()
        dapui.close()
      end
      dap.listeners.before.event_exited["dapui"] = function()
        dapui.close()
      end
    end,
  },

  -- Optional inline variable text
  { "theHamsta/nvim-dap-virtual-text", opts = { commented = true } },

  -- C/C++ configurations for codelldb
  {
    "mfussenegger/nvim-dap",
    ft = { "c", "cpp" },
    config = function()
      local dap = require("dap")
      dap.configurations.c = {
        {
          name = "Launch",
          type = "codelldb",
          request = "launch",
          program = function()
            return vim.fn.input("Path to executable: ", vim.fn.getcwd() .. "/a.out", "file")
          end,
          cwd = "${workspaceFolder}",
          stopOnEntry = false,
          args = function()
            local a = vim.fn.input("Args: ")
            return (a == "" and {}) or vim.split(a, "%s+")
          end,
        },
      }
      dap.configurations.cpp = dap.configurations.c
    end,
  },
}
```

- [ ] **Step 2: Verify**

Open Neovim and run `:WhichKey <leader>d` — you should see all 9 DAP keys listed.

- [ ] **Step 3: Commit**

```bash
git add lua/plugins/dap.lua
git commit -m "feat: add DAP keymaps (continue, breakpoints, stepping, UI toggle)"
```

---

### Task 4: Copilot Ghost Text

**Files:**
- Create: `lua/plugins/copilot.lua`

- [ ] **Step 1: Create `lua/plugins/copilot.lua`**

```lua
return {
  {
    "zbirenbaum/copilot.lua",
    opts = {
      suggestion = {
        enabled = true,
        auto_trigger = true,
        keymap = {
          accept = "<Tab>",
          accept_word = "<M-l>",
          next = "<M-]>",
          prev = "<M-[>",
          dismiss = "<C-]>",
        },
      },
      panel = { enabled = false },
    },
  },
  -- Tell copilot-cmp to defer to ghost text (disable cmp source to avoid duplication)
  {
    "zbirenbaum/copilot-cmp",
    enabled = false,
  },
}
```

- [ ] **Step 2: Verify**

Open a Python or Ruby file. Start typing a function — after a brief pause, you should see a grayed-out ghost suggestion appear inline. Press `<Tab>` to accept it. Press `<M-]>` to cycle to the next suggestion.

If `<Tab>` interferes with other insert-mode tab behavior (e.g. snippet jumping), change `accept` to `"<M-CR>"` or another unused key.

- [ ] **Step 3: Commit**

```bash
git add lua/plugins/copilot.lua
git commit -m "feat: enable Copilot inline ghost text with Tab accept"
```

---

### Task 5: Neotest (pytest + rspec)

**Files:**
- Create: `lua/plugins/neotest.lua`

- [ ] **Step 1: Create `lua/plugins/neotest.lua`**

```lua
return {
  {
    "nvim-neotest/neotest",
    dependencies = {
      "nvim-neotest/nvim-nio",
      "nvim-lua/plenary.nvim",
      "antoinemadec/FixCursorHold.nvim",
      "nvim-treesitter/nvim-treesitter",
      "nvim-neotest/neotest-python",
      "olimorris/neotest-rspec",
    },
    config = function()
      require("neotest").setup({
        adapters = {
          require("neotest-python")({
            dap = { justMyCode = false },
            runner = "pytest",
          }),
          require("neotest-rspec"),
        },
      })
    end,
    keys = {
      {
        "<leader>nt",
        function() require("neotest").run.run() end,
        desc = "Neotest: Run nearest test",
      },
      {
        "<leader>nf",
        function() require("neotest").run.run(vim.fn.expand("%")) end,
        desc = "Neotest: Run file",
      },
      {
        "<leader>ns",
        function() require("neotest").summary.toggle() end,
        desc = "Neotest: Toggle summary",
      },
      {
        "<leader>no",
        function() require("neotest").output.open({ enter = true }) end,
        desc = "Neotest: Show output",
      },
    },
  },
}
```

- [ ] **Step 2: Install plugins**

Open Neovim and run `:Lazy sync` to install `neotest`, `neotest-python`, and `neotest-rspec`.

- [ ] **Step 3: Verify with Python**

Open a Python file that has a pytest test (e.g. a file with `def test_something():`).
Press `<leader>nt` with cursor on the test function.
Expected: test runs and result appears as a sign in the gutter (green check or red X).

Press `<leader>ns` to open the summary panel — should show pass/fail tree.

- [ ] **Step 4: Verify with Ruby**

Open a Ruby spec file (e.g. `spec/models/user_spec.rb`).
Press `<leader>nf` to run all tests in the file.
Expected: results appear in gutter and summary.

- [ ] **Step 5: Commit**

```bash
git add lua/plugins/neotest.lua
git commit -m "feat: add neotest with pytest and rspec adapters"
```
