-- File runner: <leader>tr / <leader>tR run the current file in a toggleterm float.
--
-- Simple languages: add one line to `commands` and optionally a root marker to `roots`.
-- Multi-target languages: add an adapter to `adapters`.

-- Root markers for simple languages that need project-root cd
local roots = {
  go = "go.mod",
}

local function find_root(start_dir, marker)
  local dir = start_dir
  while true do
    if vim.fn.filereadable(dir .. "/" .. marker) == 1 then return dir end
    local parent = vim.fn.fnamemodify(dir, ":h")
    if parent == dir then return nil end
    dir = parent
  end
end

-- One-command languages
local function commands(file, output)
  return {
    python     = "python3 " .. file,
    c          = "gcc -std=c11 " .. file .. " -o " .. output .. " && ./" .. output,
    cpp        = "g++ " .. file .. " -o " .. output .. " && ./" .. output,
    java       = "javac " .. file .. " && java " .. output,
    go         = "go run .",
    javascript = "node " .. file,
    typescript = "tsx " .. file,
    lua        = "lua " .. file,
    sh         = "bash " .. file,
  }
end

-- Multi-target adapters.
-- Each adapter must provide:
--   marker    string           root marker file (Cargo.toml, package.json, etc.)
--   discover  fn(root)         returns a list of all runnable target names
--   build_cmd fn(target)       returns the shell command for a given target
-- Optionally:
--   infer     fn(root) → str   derive a target from the current buffer; return nil to fall through

local function cargo_package_name(root)
  for line in io.lines(root .. "/Cargo.toml") do
    local name = line:match('^name%s*=%s*"([^"]+)"')
    if name then return name end
  end
end

local adapters = {
  rust = {
    marker = "Cargo.toml",
    infer = function(root)
      local path = vim.fn.expand("%:p")
      local bin = path:match("/src/bin/([^/]+)%.rs$")
      if bin then return bin end
      if path:match("/src/main%.rs$") then return cargo_package_name(root) end
    end,
    discover = function(root)
      local bins = {}
      if vim.fn.filereadable(root .. "/src/main.rs") == 1 then
        table.insert(bins, cargo_package_name(root))
      end
      for _, f in ipairs(vim.fn.glob(root .. "/src/bin/*.rs", false, true)) do
        table.insert(bins, vim.fn.fnamemodify(f, ":t:r"))
      end
      return bins
    end,
    build_cmd = function(target)
      return "cargo run --bin " .. target
    end,
  },
}

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

local function do_send(term, run_dir, cmd)
  local full = "cd '" .. run_dir .. "' && " .. cmd
  if term.job_id then
    term:send(string.char(3))  -- Ctrl-C: interrupt any running process
    term:send(string.char(21)) -- Ctrl-U: clear the line
    term:send(string.char(12)) -- Ctrl-L: clear the screen
    term:send(full)
    vim.defer_fn(function() term:open() end, 50)
  else
    term:open()
    vim.defer_fn(function() term:send(full) end, 100)
  end
end

local function run_adapted(adapter, run_dir, term, force_pick)
  -- Try buffer-inferred target first (skipped when force_pick)
  if not force_pick and adapter.infer then
    local target = adapter.infer(run_dir)
    if target then
      do_send(term, run_dir, adapter.build_cmd(target))
      return
    end
  end

  local targets = adapter.discover(run_dir)

  if #targets == 0 then
    vim.notify("No runnable targets found", vim.log.levels.WARN)
    return
  end

  if #targets == 1 and not force_pick then
    do_send(term, run_dir, adapter.build_cmd(targets[1]))
    return
  end

  vim.ui.select(targets, { prompt = "Run: " }, function(choice)
    if choice then do_send(term, run_dir, adapter.build_cmd(choice)) end
  end)
end

local function run_file(force_pick)
  vim.cmd("write")
  local file_dir  = vim.fn.expand("%:p:h")
  local file_name = vim.fn.expand("%:t")
  local out_name  = vim.fn.expand("%:t:r")
  local filetype  = vim.bo.filetype
  local term      = get_runner()

  local adapter = adapters[filetype]
  if adapter then
    local run_dir = find_root(file_dir, adapter.marker) or file_dir
    run_adapted(adapter, run_dir, term, force_pick)
    return
  end

  local cmd = commands(file_name, out_name)[filetype]
  if not cmd then
    vim.notify("No run command configured for filetype: " .. filetype, vim.log.levels.WARN)
    return
  end

  local marker  = roots[filetype]
  local run_dir = (marker and find_root(file_dir, marker)) or file_dir
  do_send(term, run_dir, cmd)
end

return {
  "akinsho/toggleterm.nvim",
  keys = {
    { "<leader>tr", function() run_file(false) end, desc = "Run file" },
    { "<leader>tR", function() run_file(true)  end, desc = "Run file (pick target)" },
  },
}
