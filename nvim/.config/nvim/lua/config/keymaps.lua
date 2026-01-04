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
