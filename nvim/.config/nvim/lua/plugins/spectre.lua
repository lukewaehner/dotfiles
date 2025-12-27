return {
  {
    "nvim-pack/nvim-spectre",
    opts = {},
    keys = {
      {
        "<leader>sf",
        '<cmd>lua require("spectre").open_file_search({select_word=true})<CR>',
        desc = "Search in current file",
        mode = "n",
      },
      {
        "<leader>sr",
        '<cmd>lua require("spectre").open()<CR>',
        desc = "Search and Replace (project)",
        mode = "n",
      },
    },
  },
}
