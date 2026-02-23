return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
	lua_ls = false,
        sourcekit = {
          cmd = { "sourcekit-lsp" },
          filetypes = { "swift" },
        },
      },
    },
  },
}
