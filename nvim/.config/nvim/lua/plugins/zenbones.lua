return {
  {
    "zenbones-theme/zenbones.nvim",
    dependencies = { "rktjmp/lush.nvim" },
    lazy = false,
    priority = 1000,
    config = function()
      vim.g.transparent_background = true
      vim.o.pumblend = 0
      vim.o.winblend = 0
    end,
  },
}
