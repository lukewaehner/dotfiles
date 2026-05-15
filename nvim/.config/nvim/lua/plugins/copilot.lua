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
          -- Accept is handled by <C-y> in the cmp mapping.
          accept = false,
          accept_word = "<M-l>",
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
