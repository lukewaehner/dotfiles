// ============================================================
// user.js — prefs the chrome customizations depend on
//
// These are load-bearing for chrome/userChrome.css. They used to live
// only in prefs.js, which Firefox rewrites and which is not meant to be
// versioned, so a fresh profile meant clicking through about:config from
// memory.
//
// user.js is re-applied on every startup. Anything set here reverts on
// restart if you change it in about:config — that is the point, but it
// surprises people. Change it here, not there.
// ============================================================

// Load chrome/userChrome.css at all. Without this, nothing else matters.
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// Compact density. Sets --tab-min-height and --urlbar-height, both of
// which userChrome.css sizes against.
user_pref("browser.uidensity", 1);
user_pref("browser.compactmode.show", true);

// ---- onebar ----

// Keep the URL bar left-anchored; userChrome.css sec 4 assumes this.
user_pref("onebar.disable-centering-of-URLbar", true);

// Turn off onebar's single-tab mode. onebar otherwise collapses a lone
// tab and hides its close button, and undoing that from CSS meant
// fighting `display: none !important` with a `display` value that no
// longer exists (-moz-box, removed from Firefox). Disabling the mode
// removes the whole block at the source.
user_pref("onebar.disable-single-tab", true);

// ---- Browser Toolbox ----
// Tools > Browser Tools > Browser Toolbox. Its Style Editor reloads
// userChrome.css in place, so iterating on the CSS does not need a
// restart, and the Inspector shows which !important is winning.
user_pref("devtools.chrome.enabled", true);
user_pref("devtools.debugger.remote-enabled", true);
