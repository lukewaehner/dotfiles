-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- Spell checking: <leader>z autocorrect, <leader>zw interactive walk, :SpellWalk
require("config.spell")

-- NOTE: Custom WQ to save all, close explorer, and quit
vim.api.nvim_create_user_command("WQ", function()
  vim.cmd("wa") -- write all modified buffers

  -- close neo-tree if available
  pcall(function()
    require("neo-tree.command").execute({ action = "close" })
  end)

  vim.cmd("qa") -- quit all
end, {})

vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    local bufnr = args.buf

    vim.defer_fn(function()
      -- Remove LazyVim's buffer-local "gr" (Snacks picker)
      pcall(vim.keymap.del, "n", "gr", { buffer = bufnr })

      -- Set buffer-local LSP references on "gr" (no nowait)
      vim.keymap.set("n", "gr", vim.lsp.buf.references, {
        buffer = bufnr,
        desc = "LSP References",
      })
    end, 0)
  end,
})
