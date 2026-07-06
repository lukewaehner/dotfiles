-- Spell checking helpers.
-- Spell is enabled by LazyVim's `lazyvim_wrap_spell` autocmd for markdown/text/
-- gitcommit; these keymaps work in any buffer regardless.

local M = {}

-- Replace the word under the cursor with Vim's best spelling suggestion (`1z=`).
function M.fix_word()
  vim.cmd("normal! 1z=")
end

-- Return the best suggestion for `word`, or nil if there is none.
local function best_suggestion(word)
  local suggestions = vim.fn.spellsuggest(word, 1)
  return suggestions[1]
end

-- Return the misspelled word under the cursor, or "" if the cursor is not on one.
local function bad_word_under_cursor()
  local cword = vim.fn.expand("<cword>")
  if cword == "" then
    return ""
  end
  return vim.fn.spellbadword(cword)[1]
end

-- Replace the word starting at the cursor with `replacement`.
local function replace_word_at_cursor(word, replacement)
  local pos = vim.api.nvim_win_get_cursor(0)
  local row = pos[1] - 1
  local scol = pos[2]
  local line = vim.api.nvim_get_current_line()
  local ecol = math.min(scol + #word, #line)
  vim.api.nvim_buf_set_text(0, row, scol, row, ecol, { replacement })
end

-- Prompt for a single word. Returns "quit" to stop the walk, or nil to continue.
-- Increments the counters table in place.
local function prompt_word(word, counters)
  local suggestion = best_suggestion(word)
  if not suggestion then
    vim.api.nvim_echo({ { "No suggestion for '" .. word .. "', skipping.", "WarningMsg" } }, false, {})
    counters.skipped = counters.skipped + 1
    return nil
  end

  vim.cmd("normal! zz")
  vim.cmd("redraw")
  vim.api.nvim_echo({
    { string.format("Replace '%s' → '%s'?  ", word, suggestion), "Question" },
    { "[y]es  [n]o  [q]uit", "MoreMsg" },
  }, false, {})

  local ok, code = pcall(vim.fn.getchar)
  if not ok then
    return "quit"
  end
  local key = type(code) == "number" and vim.fn.nr2char(code) or code

  if key == "y" or key == "Y" then
    replace_word_at_cursor(word, suggestion)
    counters.fixed = counters.fixed + 1
    return nil
  elseif key == "q" or key == "Q" or key == "\27" then -- q or <Esc>
    return "quit"
  else
    counters.skipped = counters.skipped + 1
    return nil
  end
end

-- Walk every misspelling in the buffer, prompting y/n/q for each.
function M.walk()
  local had_spell = vim.wo.spell
  local had_wrapscan = vim.o.wrapscan
  local start_pos = vim.api.nvim_win_get_cursor(0)

  vim.wo.spell = true
  vim.o.wrapscan = false

  local counters = { fixed = 0, skipped = 0 }
  local quit = false

  vim.cmd("normal! gg0")

  -- Handle a misspelling sitting at the very first position, which `]s` skips.
  if bad_word_under_cursor() ~= "" then
    quit = prompt_word(bad_word_under_cursor(), counters) == "quit"
  end

  while not quit do
    local before = vim.api.nvim_win_get_cursor(0)
    pcall(vim.cmd, "normal! ]s")
    local after = vim.api.nvim_win_get_cursor(0)
    if before[1] == after[1] and before[2] == after[2] then
      break -- no more misspellings ahead
    end

    local word = bad_word_under_cursor()
    if word ~= "" then
      quit = prompt_word(word, counters) == "quit"
    end
  end

  vim.wo.spell = had_spell
  vim.o.wrapscan = had_wrapscan
  pcall(vim.api.nvim_win_set_cursor, 0, start_pos) -- col may shift after edits

  local verb = quit and "Spell walk stopped" or "Spell walk done"
  vim.api.nvim_echo({
    { string.format("%s: %d fixed, %d skipped", verb, counters.fixed, counters.skipped), "MoreMsg" },
  }, false, {})
end

vim.api.nvim_create_user_command("SpellWalk", M.walk, { desc = "Walk through misspellings interactively" })

vim.keymap.set("n", "<leader>z", M.fix_word, { desc = "Autocorrect word (best suggestion)" })
vim.keymap.set("n", "<leader>zw", M.walk, { desc = "Spell walk (interactive)" })

return M
