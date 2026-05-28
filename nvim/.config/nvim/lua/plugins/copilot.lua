return {
  {
    "zbirenbaum/copilot.lua",
    opts = {
      suggestion = {
        enabled = true,
        auto_trigger = true,
        -- Show copilot ghost text alongside the cmp dropdown so you can
        -- compare both before deciding.
        hide_during_completion = false,
        keymap = {
          accept = "<C-y>",
          accept_word = "<M-l>",
          accept_line = "<M-;>",
          next = "<M-]>",
          prev = "<M-[>",
          dismiss = "<C-]>",
        },
      },
      panel = { enabled = false },
    },
  },
  -- Disable copilot-cmp to avoid duplicate ghost text
  {
    "zbirenbaum/copilot-cmp",
    enabled = false,
  },
}
