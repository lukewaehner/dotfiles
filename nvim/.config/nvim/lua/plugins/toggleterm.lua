return {
  "akinsho/toggleterm.nvim",
  version = "*",
  config = function()
    require("toggleterm").setup({
      size = 20,
      open_mapping = [[<leader>tf]],
      hide_numbers = true,
      shade_terminals = true,
      start_in_insert = true,
      insert_mappings = true,
      terminal_mappings = true,
      persist_size = true,
      direction = "float",
      close_on_exit = true,
      shell = vim.o.shell,
      float_opts = {
        border = "curved",
        winblend = 0,
      },
    })

    -- Compile and run files based on filetype
    vim.keymap.set("n", "<leader>cc", function()
      vim.cmd("write")
      local file_dir = vim.fn.expand("%:p:h")
      local file_name = vim.fn.expand("%:t")
      local output_name = vim.fn.expand("%:t:r")
      local filetype = vim.bo.filetype

      local commands = {
        python = "python3 " .. file_name,
        c = "gcc -std=c11 " .. file_name .. " -o " .. output_name .. " && ./" .. output_name,
        cpp = "g++ " .. file_name .. " -o " .. output_name .. " && ./" .. output_name,
        rust = "rustc " .. file_name .. " -o " .. output_name .. " && ./" .. output_name,
        java = "javac " .. file_name .. " && java " .. output_name,
        go = "go run " .. file_name,
        javascript = "node " .. file_name,
        typescript = "ts-node " .. file_name,
        lua = "lua " .. file_name,
        sh = "bash " .. file_name,
        asm = "nasm -f elf64 "
          .. file_name
          .. " && ld "
          .. output_name
          .. ".o -o "
          .. output_name
          .. " && ./"
          .. output_name,
      }

      local cmd = commands[filetype]
      if cmd then
        local term = require("toggleterm.terminal").get_or_create_term(1)
        term:open() -- Open first
        vim.defer_fn(function()
          -- Send Ctrl-C and Ctrl-U to clear any junk
          term:send(string.char(3)) -- Ctrl-C
          term:send(string.char(21)) -- Ctrl-U
          term:send("cd " .. file_dir .. " && " .. cmd)
        end, 100) -- Small delay to ensure terminal is ready
      else
        vim.notify("No run command configured for filetype: " .. filetype, vim.log.levels.WARN)
      end
    end, { desc = "Compile and run file" })
  end,
}
