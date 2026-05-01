return {
  "hrsh7th/nvim-cmp",
  opts = function(_, opts)
    local cmp = require("cmp")
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
      ["<C-l>"] = cmp.mapping.confirm({ select = true }),
    })
    return opts
  end,
}
