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
