return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        pyright = {
          -- Never run rootless: venv-selector can't restart a rootless pyright
          -- on this Neovim, so scratch dirs without markers fall back to the
          -- file's directory (the same fallback venv-selector uses).
          root_dir = function(bufnr, on_dir)
            local markers = { "pyrightconfig.json", "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "Pipfile", ".git" }
            local file = vim.api.nvim_buf_get_name(bufnr)
            on_dir(vim.fs.root(file, markers) or vim.fs.dirname(file))
          end,
        },
        ruff_lsp = {
          on_attach = function(client, _)
            -- Turn off features that overlap with Pyright
            client.server_capabilities.hoverProvider = false
            client.server_capabilities.completionProvider = false
            client.server_capabilities.definitionProvider = false
            client.server_capabilities.referencesProvider = false
            client.server_capabilities.renameProvider = false
            client.server_capabilities.documentFormattingProvider = false
            client.server_capabilities.documentRangeFormattingProvider = false
          end,
        },
      },
    },
  },
  {
    -- venv-selector only restores venvs you picked by hand. This activates a
    -- project-local .venv/venv on its own; on activation the plugin restarts
    -- the python LSPs (pyright) so they resolve imports from that venv.
    "linux-cultist/venv-selector.nvim",
    init = function()
      -- LspAttach rather than FileType: the plugin can only reconfigure a
      -- python LSP that is already running, and pyright attaches late.
      vim.api.nvim_create_autocmd("LspAttach", {
        group = vim.api.nvim_create_augroup("AutoProjectVenv", { clear = true }),
        callback = function(args)
          local client = vim.lsp.get_client_by_id(args.data.client_id)
          if not client or client.name ~= "pyright" then
            return
          end
          local dir = vim.fs.dirname(vim.api.nvim_buf_get_name(args.buf))
          local venv_dir = vim.fs.find({ ".venv", "venv" }, { path = dir, upward = true, type = "directory" })[1]
          local python = venv_dir and (venv_dir .. "/bin/python")
          if not python or vim.fn.executable(python) ~= 1 then
            return
          end
          -- Stop once pyright was restarted by venv-selector on this venv.
          if client.config._venv_selector == true and require("venv-selector").python() == python then
            return
          end
          -- Deferred: the plugin restarts clients, which can't happen inside their attach callback.
          vim.schedule(function()
            require("venv-selector.venv").activate_for_buffer(python, "venv", args.buf, { save_cache = false })
          end)
        end,
      })
    end,
  },
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        python = { "ruff_format", "ruff_organize_imports" },
      },
    },
  },
}
