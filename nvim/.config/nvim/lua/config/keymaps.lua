-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
-- Custom keymaps for cmp to prevent <CR> from accepting
local cmp = require("cmp")
cmp.setup({
  mapping = cmp.mapping.preset.insert({
    ["<CR>"] = cmp.mapping(function(fallback)
      if cmp.visible() then
        cmp.close() -- Close the completion menu
        vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("<CR>", true, true, true), "n", true) -- Insert newline
      else
        fallback() -- If no menu, just insert newline
      end
    end, { "i", "s" }),
    ["<C-l>"] = cmp.mapping.confirm({ select = true }), -- Keep your dedicated accept key
  }),
})

vim.api.nvim_create_user_command("WQ", function()
  vim.cmd("w") -- Save current file
  pcall(vim.cmd, "Neotree close") -- Close Neo-tree safely if installed
  vim.cmd("enew") -- Create an empty scratch buffer
  vim.cmd("bufdo bwipeout") -- Wipe out all listed buffers
  vim.cmd("q") -- Quit Neovim
end, {})
