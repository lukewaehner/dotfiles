# Firefox chrome customizations

Custom `userChrome.css` for Firefox on macOS, layered on top of
[onebar](https://git.gay/Freeplay/firefox-onebar) (vendored as a submodule),
which merges the tab strip and the URL bar into a single toolbar row.

```
firefox/
├── chrome/
│   ├── userChrome.css   # the customizations
│   └── onebar/          # submodule, pinned to cf1ddf9 (1.8.4, branch waf)
└── user.js              # prefs the CSS depends on
```

## Installing into a profile

`firefox/` is **not** a stow package. Stow mirrors a package tree into `$HOME`,
and the directory this needs to land in is the Firefox profile, whose name is
random (`m8zz0fwi.default-release`). There is no fixed path to mirror, so a
script resolves the profile from `profiles.ini` instead:

```sh
link-firefox.sh --dry-run   # show what would change
link-firefox.sh             # symlink chrome/ and user.js into the profile
```

Then **restart Firefox** — `userChrome.css` and `user.js` are read only at
startup.

Re-running is safe and idempotent. Anything real already sitting at a target
path is moved to `<name>.pre-link.<timestamp>` rather than deleted.

After a fresh clone, populate the submodule first:

```sh
git submodule update --init
```

## Prefs

`user.js` holds the prefs the CSS depends on; see the comments in the file for
what each one is load-bearing for. It is re-applied on **every** startup, so
changing one of those keys in `about:config` reverts on restart. Edit `user.js`,
not `about:config`.

`prefs.js` in the profile is Firefox's own file — don't edit or version it.

## After a Firefox update

Firefox renames CSS custom properties without notice, and the failure is
silent: a `var()` that resolves to nothing makes the whole declaration invalid
at computed-value time, so the property falls back to its initial value with no
error anywhere. Three tokens had already gone stale before anyone noticed.

```sh
check-userchrome-vars.sh    # exits 1 if anything we own went stale
```

Drift inside `onebar/` is reported but does not fail the check — upstream lags
Firefox, and we don't patch the vendored copy.

Currently onebar reads four tokens Firefox 156 no longer defines. One matters:
`--tab-block-margin` (renamed `--tab-margin-block`) is what `onebar.css:41,57`
use for tab padding and margin, so both declarations are dropped. The pill
sizing in `userChrome.css` section 5 depends on that. Shimming the old name
would give the tabs ~6px of block margin and the pills would need retuning.

## Iterating on the CSS

`user.js` enables the Browser Toolbox (Tools > Browser Tools > Browser
Toolbox). Its Style Editor reloads `userChrome.css` in place, so you don't need
to restart for every tweak, and the Inspector shows which `!important` is
beating which.

## Updating onebar

```sh
git submodule update --remote firefox/chrome/onebar
```

Deliberate by design — onebar is `!important` almost everywhere and
`userChrome.css` overrides it in specific places, so an update can change the
layout. Review the diff and re-check section 5 and section 7.
