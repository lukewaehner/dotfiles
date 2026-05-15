return {
  {
    "mrcjkb/rustaceanvim",
    -- Pinned: v9.0.4 introduced a regression in ftplugin/rust.lua
    -- (runSingle codelens crashes with `attempt to index 'runnable' (a nil value)`).
    -- Bump once upstream ships a fix.
    version = "v9.0.3",
    lazy = false,
  },
}
