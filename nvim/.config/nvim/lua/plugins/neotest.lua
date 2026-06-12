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
      "rouge8/neotest-rust",
    },
    config = function()
      require("neotest").setup({
        adapters = {
          require("neotest-python")({
            dap = { justMyCode = false },
            runner = "pytest",
          }),
          require("neotest-rspec"),
          require("neotest-rust"),
        },
      })
    end,
    keys = {
      {
        "<leader>Tt",
        function() require("neotest").run.run() end,
        desc = "Run nearest test",
      },
      {
        "<leader>Tf",
        function() require("neotest").run.run(vim.fn.expand("%")) end,
        desc = "Run file",
      },
      {
        "<leader>Ts",
        function() require("neotest").summary.toggle() end,
        desc = "Toggle summary",
      },
      {
        "<leader>To",
        function() require("neotest").output.open({ enter = true }) end,
        desc = "Show output",
      },
    },
  },
}
