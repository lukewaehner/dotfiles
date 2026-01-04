return {
  "lewis6991/gitsigns.nvim",
  opts = {
    on_attach = function(bufnr)
      local gs = package.loaded.gitsigns

      local function map(mode, lhs, rhs, desc)
        vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, desc = desc })
      end

      -- navigation
      map("n", "]h", gs.next_hunk, "Next hunk")
      map("n", "[h", gs.prev_hunk, "Prev hunk")

      -- actions
      map("n", "<leader>hp", gs.preview_hunk, "Preview hunk")
      map("n", "<leader>hs", gs.stage_hunk, "Stage hunk")
      map("n", "<leader>hr", gs.reset_hunk, "Reset hunk")

      map("n", "<leader>hS", gs.stage_buffer, "Stage buffer")
      map("n", "<leader>hR", gs.reset_buffer, "Reset buffer")

      map("n", "<leader>hb", gs.blame_line, "Blame line")
    end,
  },
}
