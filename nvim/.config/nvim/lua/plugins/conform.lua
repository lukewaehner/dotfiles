-- return {
--   {
--     "stevearc/conform.nvim",
--     opts = {
--       formatters_by_ft = {
--         swift = { "swift_format" },
--         ruby = { "rubocop" },
--       },
--       formatters = {
--         rubocop = {
--           command = "bundle",
--           args = { "exec", "rubocop", "-a", "--stdin", "$FILENAME", "--stderr" },
--           stdin = true,
--         },
--       },
--     },
--   },
-- }

return {
  {
    "stevearc/conform.nvim",
    opts = function(_, opts)
      opts.formatters_by_ft = opts.formatters_by_ft or {}
      opts.formatters_by_ft.ruby = { "rubocop" }

      -- Prettier ignores the project's eslint config (e.g. @stylistic rules), so
      -- leave JS/TS formatting to the eslint LSP fix-all.
      for _, ft in ipairs({ "typescript", "typescriptreact", "javascript", "javascriptreact" }) do
        opts.formatters_by_ft[ft] = {}
      end

      opts.formatters = opts.formatters or {}
      opts.formatters.rubocop = {
        command = "rubocop",
        args = { "-a", "--stdin", "$FILENAME", "--stderr" },
        stdin = true,
      }

      return opts
    end,
  },
}
