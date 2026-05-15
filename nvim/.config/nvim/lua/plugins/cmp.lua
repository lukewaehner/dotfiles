return {
  "hrsh7th/nvim-cmp",
  opts = function(_, opts)
    local cmp = require("cmp")

    local function noop_fallback(fallback)
      fallback()
    end

    opts.mapping = vim.tbl_extend("force", opts.mapping or {}, {
      ["<CR>"] = cmp.mapping(function(fallback)
        if cmp.visible() then
          cmp.close()
          vim.api.nvim_feedkeys(
            vim.api.nvim_replace_termcodes("<CR>", true, true, true),
            "n",
            true
          )
        else
          fallback()
        end
      end, { "i", "s" }),

      -- Tab never accepts completions. Insert a literal tab.
      ["<Tab>"] = cmp.mapping(noop_fallback, { "i", "s" }),
      ["<S-Tab>"] = cmp.mapping(noop_fallback, { "i", "s" }),

      -- Unified accept key: cmp item if menu is open, else copilot ghost text.
      ["<C-y>"] = cmp.mapping(function(fallback)
        if cmp.visible() then
          cmp.confirm({ select = true })
          return
        end
        local ok, suggestion = pcall(require, "copilot.suggestion")
        if ok and suggestion.is_visible() then
          suggestion.accept()
          return
        end
        fallback()
      end, { "i", "s" }),
    })
    return opts
  end,
}
