if true then
  return {}
end

return {
  "f-person/auto-dark-mode.nvim",
  config = {
    update_interval = 1000,
    set_dark_mode = function()
      vim.opt.background = "dark"
      -- vim.cmd("colorscheme tokyonight-night")
      vim.cmd("colorscheme zenwritten")
    end,
    set_light_mode = function()
      vim.opt.background = "light"
      -- vim.cmd("colorscheme tokyonight-day")
      vim.cmd("colorscheme seoulbones")
    end,
  },
}
