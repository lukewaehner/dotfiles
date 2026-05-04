return {
  "akinsho/toggleterm.nvim",
  version = "*",
  event = "VeryLazy",
  config = function()
    require("toggleterm").setup({
      hide_numbers = true,
      start_in_insert = true,
      insert_mappings = true,
      terminal_mappings = true,
      persist_size = true,
      direction = "float",
      close_on_exit = true,
      shell = vim.o.shell,
      float_opts = {
        border   = "curved",
        winblend = 0,
        width    = function() return math.floor(vim.o.columns * 0.85) end,
        height   = function() return math.floor(vim.o.lines * 0.80) end,
      },
    })
    vim.keymap.set({ "n", "t" }, "<leader>tf", function()
      require("toggleterm.terminal").get_or_create_term(1):toggle()
    end, { desc = "Toggle terminal" })
  end,
}
