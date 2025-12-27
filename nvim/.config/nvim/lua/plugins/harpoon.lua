-- lua/plugins/harpoon.lua
return {
  {
    "ThePrimeagen/harpoon",
    branch = "harpoon2",
    opts = {},
    keys = {
      {
        "<leader>a",
        function()
          require("harpoon"):list():add()
        end,
        desc = "Harpoon add",
      },
      {
        "<C-e>",
        function()
          require("harpoon").ui:toggle_quick_menu(require("harpoon"):list())
        end,
        desc = "Harpoon menu",
      },
      {
        "<M-1>",
        function()
          require("harpoon"):list():select(1)
        end,
      },
      {
        "<M-2>",
        function()
          require("harpoon"):list():select(2)
        end,
      },
      {
        "<M-3>",
        function()
          require("harpoon"):list():select(3)
        end,
      },
      {
        "<M-4>",
        function()
          require("harpoon"):list():select(4)
        end,
      },
    },
  },
}
