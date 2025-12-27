-- lua/plugins/dap.lua
return {
  -- Core DAP (no setup() call)
  { "mfussenegger/nvim-dap" },

  -- Auto-install adapters (codelldb for C/C++)
  {
    "jay-babu/mason-nvim-dap.nvim",
    dependencies = { "mason-org/mason.nvim", "mfussenegger/nvim-dap" },
    opts = {
      ensure_installed = { "codelldb" },
      automatic_installation = true,
      handlers = {}, -- keep default handlers
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
      dapui.setup() -- valid
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
      -- mason-nvim-dap wires the adapter; define configurations:
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
