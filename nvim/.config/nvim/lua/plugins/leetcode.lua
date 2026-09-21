-- `nvim leetcode.nvim` still opens the dashboard; otherwise the plugin (and its
-- plenary/nui/telescope dependencies) waits for `:Leet`.
local leet_arg = "leetcode.nvim"

return {
  {
    "kawre/leetcode.nvim",
    build = ":TSUpdate html",
    cmd = "Leet",
    lazy = leet_arg ~= vim.fn.argv()[1],
    dependencies = {
      "nvim-lua/plenary.nvim",
      "MunifTanjim/nui.nvim",
      { "nvim-telescope/telescope.nvim", lazy = true },
    },
    opts = {
      arg = leet_arg,
      lang = "python3",
      picker = { provider = "telescope" },
      plugins = { non_standalone = true },
      description = { position = "left", width = "40%", show_stats = true },
      console = { open_on_runcode = true },
    },
  },
}
