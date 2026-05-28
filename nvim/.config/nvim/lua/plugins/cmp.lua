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

      -- Accept cmp item when menu is open; copilot owns <C-y> when it is not.
      ["<C-y>"] = cmp.mapping(function(fallback)
        if cmp.visible() then
          cmp.confirm({ select = true })
        else
          fallback()
        end
      end, { "i", "s" }),
    })
    return opts
  end,
}
