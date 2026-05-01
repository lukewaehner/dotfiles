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
