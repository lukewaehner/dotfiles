-- File runner: <leader>tr compiles and runs the current file in a toggleterm float.
-- To add a new language, add one line to the `commands` table below.
-- To make a language cd to its project root, add its marker file to `project_markers`.

local project_markers = {
  rust = "Cargo.toml",
  go   = "go.mod",
}

local function find_root(start_dir, marker)
  local dir = start_dir
  while true do
    if vim.fn.filereadable(dir .. "/" .. marker) == 1 then
      return dir
    end
    local parent = vim.fn.fnamemodify(dir, ":h")
    if parent == dir then return nil end
    dir = parent
  end
end

local function commands(file, output)
  return {
    python     = "python3 " .. file,
    c          = "gcc -std=c11 " .. file .. " -o " .. output .. " && ./" .. output,
    cpp        = "g++ " .. file .. " -o " .. output .. " && ./" .. output,
    rust       = "cargo run",
    java       = "javac " .. file .. " && java " .. output,
    go         = "go run .",
    javascript = "node " .. file,
    typescript = "tsx " .. file,
    lua        = "lua " .. file,
    sh         = "bash " .. file,
  }
end

local runner_term = nil

local function get_runner()
  if not runner_term then
    local Terminal = require("toggleterm.terminal").Terminal
    runner_term = Terminal:new({
      direction = "float",
      float_opts = {
        border   = "curved",
        winblend = 0,
        width    = function() return math.floor(vim.o.columns * 0.45) end,
        height   = function() return math.floor(vim.o.lines * 0.75) end,
        col      = function() return vim.o.columns - math.floor(vim.o.columns * 0.45) - math.floor(vim.o.columns * 0.03) end,
        row      = function() return math.floor(vim.o.lines * 0.08) end,
      },
      on_open = function(term)
        vim.keymap.set("n", "<Esc>", function() term:close() end, { buffer = term.bufnr, silent = true })
        vim.keymap.set("t", "<Esc>", function() term:close() end, { buffer = term.bufnr, silent = true })
      end,
    })
  end
  return runner_term
end

return {
  "akinsho/toggleterm.nvim",
  keys = {
    { "<leader>tr", function()
      vim.cmd("write")
      local file_dir  = vim.fn.expand("%:p:h")
      local file_name = vim.fn.expand("%:t")
      local out_name  = vim.fn.expand("%:t:r")
      local filetype  = vim.bo.filetype

      local cmd = commands(file_name, out_name)[filetype]
      if not cmd then
        vim.notify("No run command configured for filetype: " .. filetype, vim.log.levels.WARN)
        return
      end

      local marker  = project_markers[filetype]
      local run_dir = (marker and find_root(file_dir, marker)) or file_dir
      local term    = get_runner()

      local function send_cmd()
        term:send(string.char(3))  -- Ctrl-C: interrupt any running process
        term:send(string.char(21)) -- Ctrl-U: clear the line
        term:send(string.char(12)) -- Ctrl-L: clear the screen
        term:send("cd '" .. run_dir .. "' && " .. cmd)
      end

      if term.job_id then
        -- Process already running: send commands invisibly, then reveal
        send_cmd()
        vim.defer_fn(function() term:open() end, 50)
      else
        -- First run: shell is fresh, just send the command
        term:open()
        vim.defer_fn(function()
          term:send("cd '" .. run_dir .. "' && " .. cmd)
        end, 100)
      end
    end, desc = "Run file" },
  },
}
