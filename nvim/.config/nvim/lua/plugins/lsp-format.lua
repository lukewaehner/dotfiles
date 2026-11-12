return {
  {
    "neovim/nvim-lspconfig",
    init = function()
      -- vtsls's formatter re-indents curried arrow bodies after eslint's
      -- prettier fix-all has run, leaving files that fail `prettier/prettier`.
      -- Leave JS/TS formatting to eslint.
      vim.api.nvim_create_autocmd("LspAttach", {
        callback = function(args)
          local client = vim.lsp.get_client_by_id(args.data.client_id)
          if client and client.name == "vtsls" then
            client.server_capabilities.documentFormattingProvider = false
            client.server_capabilities.documentRangeFormattingProvider = false
          end
        end,
      })
    end,
  },
}
