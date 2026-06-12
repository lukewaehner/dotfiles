-- Ported from ghostty config — see ghostty/.config/ghostty/config
local wezterm = require("wezterm")
local act = wezterm.action
local config = wezterm.config_builder()

------------------------------------------------------------
-- Appearance: window, background, padding
------------------------------------------------------------
config.window_background_opacity = 0.10
config.macos_window_background_blur = 60

config.window_padding = {
  left = 10,
  right = 10,
  top = 10,
  bottom = 10,
}

-- ghostty: macos-titlebar-style=tabs, macos-window-buttons=hidden,
-- macos-titlebar-proxy-icon=hidden. wezterm equivalent: hide the native
-- titlebar and let the fancy tab bar act as the title strip.
config.window_decorations = "RESIZE"
config.use_fancy_tab_bar = true
config.tab_bar_at_bottom = false
config.hide_tab_bar_if_only_one_tab = false
config.show_new_tab_button_in_tab_bar = false

------------------------------------------------------------
-- Font
------------------------------------------------------------
config.font = wezterm.font("JetBrainsMono Nerd Font Mono", { weight = "Regular" })
config.font_size = 18
-- ghostty: font-feature = -calt
config.harfbuzz_features = { "calt=0", "clig=0", "liga=0" }

------------------------------------------------------------
-- Cursor
------------------------------------------------------------
config.default_cursor_style = "SteadyBlock"
config.cursor_blink_rate = 0
-- cursor-invert-fg-bg: applied per-scheme below via cursor_bg/cursor_fg.

------------------------------------------------------------
-- Theme: follow macOS appearance, tokyonight night/day
------------------------------------------------------------
config.color_schemes = {
  ["tokyonight_night"] = {
    foreground = "#c0caf5",
    background = "#1a1b26",
    cursor_bg = "#c0caf5",
    cursor_fg = "#1a1b26",
    cursor_border = "#c0caf5",
    selection_bg = "#283457",
    selection_fg = "#c0caf5",
    ansi = {
      "#15161e", "#f7768e", "#9ece6a", "#e0af68",
      "#7aa2f7", "#bb9af7", "#7dcfff", "#a9b1d6",
    },
    brights = {
      "#414868", "#ff899d", "#9fe044", "#faba4a",
      "#8db0ff", "#c7a9ff", "#a4daff", "#c0caf5",
    },
  },
  ["tokyonight_day"] = {
    foreground = "#3760bf",
    background = "#e1e2e7",
    cursor_bg = "#3760bf",
    cursor_fg = "#e1e2e7",
    cursor_border = "#3760bf",
    selection_bg = "#b7c1e3",
    selection_fg = "#3760bf",
    ansi = {
      "#b4b5b9", "#f52a65", "#587539", "#8c6c3e",
      "#2e7de9", "#9854f1", "#007197", "#6172b0",
    },
    brights = {
      "#a1a6c5", "#ff4774", "#5c8524", "#a27629",
      "#358aff", "#a463ff", "#007ea8", "#3760bf",
    },
  },
}

local function scheme_for_appearance(appearance)
  if appearance:find("Dark") then
    return "tokyonight_night"
  end
  return "tokyonight_day"
end

config.color_scheme = scheme_for_appearance(wezterm.gui.get_appearance())

-- Live-update when macOS appearance flips
wezterm.on("window-config-reloaded", function(window)
  local overrides = window:get_config_overrides() or {}
  local new = scheme_for_appearance(window:get_appearance())
  if overrides.color_scheme ~= new then
    overrides.color_scheme = new
    window:set_config_overrides(overrides)
  end
end)

------------------------------------------------------------
-- Behavior
------------------------------------------------------------
config.send_composed_key_when_left_alt_is_pressed = false
config.send_composed_key_when_right_alt_is_pressed = false
config.hide_mouse_cursor_when_typing = true
config.window_close_confirmation = "NeverPrompt"
config.check_for_updates = true
config.audible_bell = "Disabled"
config.scrollback_lines = 10000

-- ghostty: copy-on-select = clipboard
config.mouse_bindings = {
  {
    event = { Up = { streak = 1, button = "Left" } },
    mods = "NONE",
    action = act.CompleteSelection("ClipboardAndPrimarySelection"),
  },
  -- preserve click-through for hyperlinks
  {
    event = { Up = { streak = 1, button = "Left" } },
    mods = "CMD",
    action = act.OpenLinkAtMouseCursor,
  },
}

------------------------------------------------------------
-- Keybinds — mirror ghostty's cmd+b leader (tmux-style)
------------------------------------------------------------
config.leader = { key = "b", mods = "SUPER", timeout_milliseconds = 1000 }

config.keys = {
  -- super+i: debug overlay (ghostty inspector analog)
  { key = "i", mods = "SUPER", action = act.ShowDebugOverlay },

  -- leader r: reload config
  { key = "r", mods = "LEADER", action = act.ReloadConfiguration },
  -- leader x: close current pane (ghostty close_surface)
  { key = "x", mods = "LEADER", action = act.CloseCurrentPane({ confirm = false }) },
  -- leader c: new tab
  { key = "c", mods = "LEADER", action = act.SpawnTab("CurrentPaneDomain") },
  -- leader n: new window
  { key = "n", mods = "LEADER", action = act.SpawnWindow },

  -- leader 1..9: goto tab
  { key = "1", mods = "LEADER", action = act.ActivateTab(0) },
  { key = "2", mods = "LEADER", action = act.ActivateTab(1) },
  { key = "3", mods = "LEADER", action = act.ActivateTab(2) },
  { key = "4", mods = "LEADER", action = act.ActivateTab(3) },
  { key = "5", mods = "LEADER", action = act.ActivateTab(4) },
  { key = "6", mods = "LEADER", action = act.ActivateTab(5) },
  { key = "7", mods = "LEADER", action = act.ActivateTab(6) },
  { key = "8", mods = "LEADER", action = act.ActivateTab(7) },
  { key = "9", mods = "LEADER", action = act.ActivateTab(8) },

  -- splits
  { key = "\\", mods = "LEADER", action = act.SplitHorizontal({ domain = "CurrentPaneDomain" }) },
  { key = "-",  mods = "LEADER", action = act.SplitVertical({ domain = "CurrentPaneDomain" }) },
  -- leader e: rebalance splits (closest wezterm equivalent)
  { key = "e",  mods = "LEADER", action = act.PaneSelect({ mode = "SwapWithActive" }) },

  -- split nav (hjkl)
  { key = "h", mods = "LEADER", action = act.ActivatePaneDirection("Left") },
  { key = "j", mods = "LEADER", action = act.ActivatePaneDirection("Down") },
  { key = "k", mods = "LEADER", action = act.ActivatePaneDirection("Up") },
  { key = "l", mods = "LEADER", action = act.ActivatePaneDirection("Right") },
}

-- ghostty has `super+b>,=toggle_quick_terminal` — wezterm has no native
-- dropdown/quick terminal. Skipped.

return config
