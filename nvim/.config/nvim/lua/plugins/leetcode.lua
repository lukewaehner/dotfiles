return {
  {
    "kawre/leetcode.nvim",
    build = ":TSUpdate html",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "MunifTanjim/nui.nvim",
      "nvim-telescope/telescope.nvim", -- LazyVim includes telescope
    },
    opts = {
      lang = "python3",
      picker = { provider = "telescope" },
      plugins = { non_standalone = true },
      description = { position = "left", width = "40%", show_stats = true },
      console = { open_on_runcode = true },
    },
  },
}
